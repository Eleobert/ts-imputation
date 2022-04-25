# # http://archive.ics.uci.edu/ml/datasets/Air+Quality

# %%
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
import matplotlib.pyplot as plt


df = pd.read_csv("datasets/AirQualityUCI.csv", sep=';', decimal=',').iloc[0:9357:, 2:15]
df.plot()
plt.show()


# import numpy as np

# x =[[2.00, 0.03, 1.32, 0.44],
#     [4.38, 7.24, 8.25, 3.36],
#     [0.29, 1.36, 2.43, 3.01],
#     [2.97, 0.71, 4.67, 1.14],
#     [1.00, 4.31, 3.59, 2.76]]

# x = np.array(x)

# print(x)

# cor = np.corrcoef(x, rowvar=False)

# print(cor)

# xnan = x
# xnan[1, 0] = np.nan
# xnan[3, 0] = np.nan

# print(xnan)




