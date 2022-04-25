import pandas as pd
from matplotlib import pyplot
from statsmodels.tsa.seasonal import seasonal_decompose

air_passenger = pd.read_csv("datasets/AirPassengers.csv")
air_passenger = air_passenger.set_index('date')
result = seasonal_decompose(list(air_passenger.value), model='additive', period=12)
result.plot()
pyplot.show()


