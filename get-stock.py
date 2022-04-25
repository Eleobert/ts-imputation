from pandas_datareader import data as pdr
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt



# def get(tickers, start, end):
#     def get_data(ticker):
#         return (pdr.get_data_yahoo(ticker, start=start, end=end))

#     data = map(get_data, tickers)
#     data = pd.concat(data, keys=tickers, names=['Ticker','Date'])
#     data = data[['Adj Close']].reset_index().pivot('Date','Ticker','Adj Close')
#     return data

start = dt.datetime(2016, 1, 1)
end = dt.datetime(2021, 12, 31)
# df = get(['HPE','MRNA','PCG'], start, end)


df = pdr.get_data_yahoo('HPE', start=start, end=end)
df['Adj Close'].plot()
plt.show()
