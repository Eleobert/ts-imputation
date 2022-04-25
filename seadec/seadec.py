from random import randrange
import pandas as pd
from matplotlib import pyplot
from statsmodels.tsa.seasonal import seasonal_decompose

pyplot.style.use('bmh')

df = pd.read_excel('misc/campylobacter/campylobacter_germany.xlsx')
result = seasonal_decompose(df.case, model='additive', period=53)
result.plot()
pyplot.show()