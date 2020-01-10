import numpy as np
import pandas as pd


def process_data_for_labels(ticker):
    days_count = 7
    df = pd.read_csv('sp500_combined_adj_close.csv', index_col=0)
    df.fillna(0, inplace=True)

    for i in range(1, days_count + 1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return df

def buy_sell_hold(*args):
    columns = [c for c in args]
    requirement = 0.02
    for col in columns:
        if col > requirement:
            return 1
        elif col < -requirement:
            return -1

    return 0

