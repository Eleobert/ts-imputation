# # http://archive.ics.uci.edu/ml/datasets/Air+Quality

# %%
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer


df = pd.read_csv("../datasets/AirQualityUCI.csv", sep=';', decimal=',').iloc[0:9357:, 2:15]
df

# %%

def plant_nans(x, p):
    mask = np.random.uniform(size=x.shape)
    return x.where(mask > p, np.nan)

df_nans = plant_nans(df, 0.1)

normalized_df =(df - df.min())/(df.max() - df.min())

# %%

p = np.linspace(0, 0.5, 15)
print("proportions:", p)

def benchmark(x, ps, method = None, order = None):
    from sklearn.metrics import mean_squared_error
    np.random.seed(0)
    mean_inputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    mse = [0] * len(ps)
    for i, p in enumerate(ps):
        u = plant_nans(x, p)
        if method:
            u = u.interpolate(method=method, order=order)
        imputed = mean_inputer.fit_transform(u)
            
        mse[i] = mean_squared_error(imputed, x)
    print(mse)
    return mse


w = 'uniform'
ys = [0] * 6

ys[0] = benchmark(normalized_df, p)
print('done')
ys[1] = benchmark(normalized_df, p, 'linear')
print('done')
ys[2] = benchmark(normalized_df, p, 'cubicspline')
print('done')
# ys[3] = benchmark(normalized_df, p, 'polynomial')
# print('done')
# ys[4] = benchmark(KNNImputer(n_neighbors=8, weights=w), normalized_df, p)
# print('done')
# ys[5] = benchmark(KNNImputer(n_neighbors=16, weights=w), normalized_df, p)
# %%
import matplotlib.pyplot as plt
plt.style.use('bmh')

plt.plot(p, ys[0], linestyle=':',color='black', label='mean')
plt.plot(p, ys[1], marker='o', label='linear')
plt.plot(p, ys[2], marker='o', label='cubicspline')
# plt.plot(p, ys[3], marker='o', label='k = 4')
# plt.plot(p, ys[4], marker='o', label='k = 8')
# plt.plot(p, ys[5], marker='o', label='k = 16')
plt.xlabel("Proportion of Missing Values")
plt.ylabel("MSE")
plt.legend()
plt.show()
