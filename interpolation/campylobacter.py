from cProfile import label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')







df = pd.read_excel('../misc/campylobacter/campylobacter_germany.xlsx').head(262)
# print(df)
df_missing = df.copy()
df_missing.case.iloc[50:75] = np.nan
df_missing.case.iloc[123:130] = np.nan

df_actual_values = df.copy()
df_actual_values.case[~df_missing.case.isnull()] = np.nan


linear = df_missing.case.interpolate()
linear[~df_missing.case.isnull()] = np.nan

spline = df_missing.case.interpolate(method='spline', order=2)
spline[~df_missing.case.isnull()] = np.nan

plt.plot(df_missing.date, df_missing.case)
plt.plot(df_actual_values.date, df_actual_values.case, '--')
plt.plot(df_actual_values.date, linear, color='yellow', label='linear')
plt.plot(df_actual_values.date, spline, color='red', label='spline')
plt.legend()
plt.show()
