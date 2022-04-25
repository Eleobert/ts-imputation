from pykalman import KalmanFilter
from pykalman.utils import array1d, array2d, check_random_state, get_params, log_multivariate_normal_density, preprocess_arguments
from pykalman.standard import _filter, _smooth, _smooth_pair, _em
import numpy as np
import pandas as pd

DIM = {
    'transition_matrices': 2,
    'transition_offsets': 1,
    'observation_matrices': 2,
    'observation_offsets': 1,
    'transition_covariance': 2,
    'observation_covariance': 2,
    'initial_state_mean': 1,
    'initial_state_covariance': 2,
}

def interpolate_matrix(X, how):
	#線形補完
	initial_X = pd.DataFrame(X).interpolate(method=how)
	#最後にnanがあるなら直前の値で埋める
	initial_X = initial_X.fillna(method='ffill')
	#最初にnanがあるなら直後の値で埋める
	initial_X = initial_X.fillna(method='bfill')
	return np.array(initial_X)

class KalmanFilter_part(KalmanFilter):

    def em(self, X, y=None, n_iter=10, em_vars=None):
        Z = self._parse_observations(X)

        # initialize parameters
        (self.transition_matrices, self.transition_offsets,
         self.transition_covariance, self.observation_matrices,
         self.observation_offsets, self.observation_covariance,
         self.initial_state_mean, self.initial_state_covariance) = (
            self._initialize_parameters()
        )

        # Create dictionary of variables not to perform EM on
        if em_vars is None:
            em_vars = self.em_vars

        if em_vars == 'all':
            given = {}
        else:
            given = {
                'transition_matrices': self.transition_matrices,
                'observation_matrices': self.observation_matrices,
                'transition_offsets': self.transition_offsets,
                'observation_offsets': self.observation_offsets,
                'transition_covariance': self.transition_covariance,
                'observation_covariance': self.observation_covariance,
                'initial_state_mean': self.initial_state_mean,
                'initial_state_covariance': self.initial_state_covariance
            }
            em_vars = set(em_vars)
            for k in list(given.keys()):
                if k in em_vars:
                    given.pop(k)

        # If a parameter is time varying, print a warning
        for (k, v) in get_params(self).items():
            if k in DIM and (not k in given) and len(v.shape) != DIM[k]:
                warn_str = (
                    '{0} has {1} dimensions now; after fitting, '
                    + 'it will have dimension {2}'
                ).format(k, len(v.shape), DIM[k])
                warnings.warn(warn_str)

        # Actual EM iterations
        for i in range(n_iter):
            (predicted_state_means, predicted_state_covariances,
             kalman_gains, filtered_state_means,
             filtered_state_covariances) = (
                _filter(
                    self.transition_matrices, self.observation_matrices,
                    self.transition_covariance, self.observation_covariance,
                    self.transition_offsets, self.observation_offsets,
                    self.initial_state_mean, self.initial_state_covariance,
                    Z
                )
            )
            (smoothed_state_means, smoothed_state_covariances,
             kalman_smoothing_gains) = (
                _smooth(
                    self.transition_matrices, filtered_state_means,
                    filtered_state_covariances, predicted_state_means,
                    predicted_state_covariances
                )
            )
            sigma_pair_smooth = _smooth_pair(
                smoothed_state_covariances,
                kalman_smoothing_gains
            )
            (self.transition_matrices,  self.observation_matrices,
             self.transition_offsets, self.observation_offsets,
             self.transition_covariance, self.observation_covariance,
             self.initial_state_mean, self.initial_state_covariance) = (
                _em(Z, self.transition_offsets, self.observation_offsets,
                    smoothed_state_means, smoothed_state_covariances,
                    sigma_pair_smooth, given=given
                )
            )
        return self, predicted_state_means, predicted_state_covariances


class LDS:
	def __init__(self, n_dim_state, n_dim_obs, model=None):
		n_dim_state = n_dim_state
		n_dim_obs = n_dim_obs

		if model:
			self.miu = model.miu
			self.A = model.A
			self.C = model.C
			self.Q = model.Q
			self.Q0 = model.Q0
			self.R = model.R
		else:
			self.miu = np.random.randn(n_dim_state)
			self.A = np.eye(n_dim_state, n_dim_state) + np.random.randn(n_dim_state, n_dim_state)
			self.C = np.eye(n_dim_obs, n_dim_state) + np.random.randn(n_dim_obs, n_dim_state)
			self.Q = np.eye(n_dim_state, n_dim_state)
			self.Q0 = self.Q
			self.R = np.eye(n_dim_obs, n_dim_obs)

	def fit(self, X):
		kf = KalmanFilter_part( initial_state_mean=self.miu,
						initial_state_covariance=self.Q0,
						transition_matrices=self.A,
						transition_covariance=self.Q,
						observation_matrices=self.C,
						observation_covariance=self.R)
			
		kf, predict_mean, predict_var = kf.em(X,em_vars=['transition_matrices','transition_covariance', 'observation_matrices','observation_covariance'],n_iter=1)
		self.miu = kf.initial_state_mean
		self.A = kf.transition_matrices
		self.C = kf.observation_matrices
		self.Q = kf.transition_covariance
		self.Q0 = kf.initial_state_covariance
		self.R = kf.observation_covariance

		return predict_mean, predict_var


def isTiny(sigma):
	eps = 1.0e-10
	return (np.linalg.norm(sigma,1) < eps) or (np.any(np.diag(sigma) < eps))

def DynaMMo(initial_X, W, n_dim_state=6, n_iter=10):
	N = initial_X.shape[0]
	H = n_dim_state
	dim = initial_X.shape[1]

	for n in range(n_iter):
		if n==0:
			lds = LDS(n_dim_state=H,n_dim_obs=dim)
		else:
			lds = LDS(n_dim_state=H, n_dim_obs=dim, model=lds)

		predict_mean, predict_var = lds.fit(initial_X)

		Y = np.empty(initial_X.shape)
		for i in range(N):
			Y[i] = lds.C @ predict_mean[i]
			for j in range(dim):
				if W[i,j]==0:
					initial_X[i,j] = Y[i,j]
		
		if (isTiny(lds.Q0) or isTiny(lds.Q) or isTiny(lds.R)):
			print('converged at n_iter=',n)
			break
		if n==n_iter-1:
			print('not converged until n_iter=',n_iter)
	
	return initial_X
