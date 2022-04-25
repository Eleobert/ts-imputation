import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose

n_seasons = 8
size = 8 * 9
x = np.linspace(0, n_seasons * 2 * np.pi, size)

seasons = np.sin(x) * 2.5
trend = (x * x) / 100
noise = np.random.normal(scale=0.7, size=size)
series = trend + seasons + noise

import matplotlib.pyplot as plt
plt.style.use('bmh')

result = seasonal_decompose(series, model='additive', period=round(size/n_seasons))
result.plot()
plt.show()

result._trend = trend
result._seasonal = seasons
result._resid = noise

result.plot()
plt.show()