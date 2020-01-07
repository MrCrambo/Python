import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import pandas_datareader.data as web

register_matplotlib_converters()

style.use("ggplot")

# # user for saving data to csv file using pandas datareader
# start = dt.datetime(2000, 1, 1)
# end = dt.datetime(2019, 12, 31)
# df = web.DataReader("TSLA", "yahoo", start, end) # need to know from which sources it is possible to read the data
# df.to_csv('Tesla.csv')

df = pd.read_csv('Tesla.csv', parse_dates=True, index_col=0)

df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

# # for dropping NaN rows
# df.dropna(inplace=True)

# in case we want few charts in one plot need to show shape like i.e.: (5, 1) and to pass rowspan value
# ax = plt.subplot2grid((1, 1), (0, 0))
#
# ax.plot(df.index, df['Adj Close'])
# ax.plot(df.index, df['100ma'])
#
# plt.show()


# for sampling data by 10 days range

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()
df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=4, colspan=1)
ax2 = plt.subplot2grid((6, 1), (4, 0), rowspan=2, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
