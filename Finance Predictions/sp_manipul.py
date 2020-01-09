import bs4 as bs
import requests
import os
import pandas as pd
import pandas_datareader.data as web
import datetime as dt


def get_sp_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text.replace('\n', '')
        tickers.append(ticker)

    return tickers

def get_yahoo_data():
    tickers = get_sp_tickers()
    if not os.path.exists('sp500_data'):
        os.makedirs('sp500_data')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2019, 12, 31)

    for ticker in tickers:
        if not os.path.exists('sp500_data/{}.csv'.format(ticker)):
            print('Loading data for {}...'.format(ticker))
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('sp500_data/{}.csv'.format(ticker))
        else:
            print('Already loaded {}'.format(ticker))

get_yahoo_data()


