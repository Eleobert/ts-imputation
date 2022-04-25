from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer, KNNImputer
from fancyimpute import IterativeSVD, SoftImpute, BiScaler
import numpy as np
import pandas as pd
from CD.cdrec import centroid_recovery
from DynaMMo.dynammo import DynaMMo, interpolate_matrix

def plant_nans(x, p):
    mask = np.random.uniform(size=x.shape)
    return x.where(mask > p, np.nan)

def normalize(x):
    return (x - x.min()) / (x.max() - x.min())

def load_air_quality(p):
    df = pd.read_csv("datasets/AirQualityUCI.csv", sep=';', decimal=',').iloc[0:9357:, 2:15]
    normalized_df = normalize(df)
    return normalized_df, plant_nans(normalized_df, p)


df, df_nans = load_air_quality(0.2)

def benchmark(model, x_thruth, x):
    from sklearn.metrics import mean_squared_error
    np.random.seed(0)
    imputed = model.fit_transform(x)
    return mean_squared_error(imputed, x_thruth)


import matplotlib.pyplot as plt
plt.style.use('bmh')

INTERP = 0
KNN = 1
SVD = 2
AMELIA = 3
MICE = 4
DYNAMMO = 5

labels    = ['Interp', 'KNN', 'SVD', 'AMELIA', 'MICE', 'DynaMMo']
air_quality = [np.nan] * 6
width = 0.35


air_quality[INTERP] = benchmark(SimpleImputer(), df, df_nans.interpolate())
air_quality[KNN] = 0.0001# benchmark(KNNImputer(), df, df_nans)
air_quality[SVD] = 0.0001 #benchmark(IterativeSVD(), df, df_nans)
#air_quality[AMELIA]  = benchmark(SimpleImputer(), df, centroid_recovery(df_nans))
air_quality[AMELIA] = 0.0003528276;
air_quality[MICE] = 0.0002992412

W = np.multiply(np.ones(df_nans.to_numpy().shape), np.isnan(df_nans.to_numpy()))
print(df_nans.to_numpy())
dyna = DynaMMo(interpolate_matrix(df_nans.to_numpy(), how='linear'), W)

air_quality[DYNAMMO] = benchmark(SimpleImputer(), df, dyna)
fig, ax = plt.subplots()

ax.bar(labels, air_quality, width, label='Air Quality')

ax.set_ylabel('MSE')
ax.set_title('MSE by method')
ax.legend()

plt.show()

