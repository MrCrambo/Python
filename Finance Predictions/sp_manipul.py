import bs4 as bs
import requests
import os
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

style.use("ggplot")

###########################################
##                                       ##
##     Getting all tickers from Wiki     ##
##                                       ##
###########################################
def get_sp_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text.replace('\n', '').replace('.', '-')
        tickers.append(ticker)

    return tickers

###########################################
##                                       ##
##   Loading all sp500 data from yahoo   ##
##                                       ##
###########################################
def get_yahoo_data():
    tickers = get_sp_tickers()
    if not os.path.exists('sp500_data'):
        os.makedirs('sp500_data')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2019, 12, 31)

    for ticker in tickers:
        if not os.path.exists('sp500_data/{}.csv'.format(ticker)):
            print('Loading data for {}...'.format(ticker))
            df = web.get_data_yahoo(ticker, start, end)
            df.to_csv('sp500_data/{}.csv'.format(ticker))
        else:
            print('Already loaded {}'.format(ticker))

###########################################
##                                       ##
##  Combining all adj close in one file   ##
##                                       ##
###########################################
def combine_data():
    tickers = get_sp_tickers()
    main_df = pd.DataFrame()

    for index, ticker in enumerate(tickers):
        df = pd.read_csv('sp500_data/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if index % 10 == 0:
            print(index)

    print(main_df.head())
    main_df.to_csv('sp500_combined_adj_close.csv')

###########################################
##                                       ##
##    Correlation chart for all sp500    ##
##                                       ##
###########################################
def visualise_data():
    df = pd.read_csv('sp500_combined_adj_close.csv')
    df_corr = df.corr()
    print(df_corr.head())


    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)

    plt.tight_layout()
    plt.show()

visualise_data()
