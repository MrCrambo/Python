import numpy as np
import pandas as pd
from collections import Counter
from sklearn import svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn import linear_model
from sp_manipul import get_sp_tickers

def process_data_for_labels(ticker):
    days_count = 7
    df = pd.read_csv('sp500_combined_adj_close.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, days_count + 1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker] - df[ticker].shift(i)) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):
    columns = [c for c in args]
    requirement = 0.02
    for col in columns:
        if col > requirement:
            return 1
        elif col < -requirement:
            return -1

    return 0

def extract_feature_sets(ticker):
    tickers, df = process_data_for_labels(ticker)

    df['{}_targets'.format(ticker)] = list(map(buy_sell_hold,
                                               df['{}_1d'.format(ticker)],
                                               df['{}_2d'.format(ticker)],
                                               df['{}_3d'.format(ticker)],
                                               df['{}_4d'.format(ticker)],
                                               df['{}_5d'.format(ticker)],
                                               df['{}_6d'.format(ticker)],
                                               df['{}_7d'.format(ticker)]))

    vals = df['{}_targets'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    df.fillna(0, inplace=True)

    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[tkr for tkr in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values
    y = df['{}_targets'.format(ticker)].values

    return X, y, df

def predict_neighbors(ticker):
    X, y, df = extract_feature_sets(ticker)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    classifier = neighbors.KNeighborsClassifier()
    classifier.fit(X_train, y_train)

    confidence = classifier.score(X_test, y_test)
    prediction = classifier.predict(X_test)

    print('Confidence is: ', confidence)
    print('Predicted spread: ', Counter(prediction))
    print('----\n')

def predict_voting(ticker):
    X, y, df = extract_feature_sets(ticker)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    classifier = VotingClassifier([('lsvc', svm.LinearSVC()),
                                ('lr', linear_model.LogisticRegression()),
                                ('knn', neighbors.KNeighborsClassifier()),
                                ('rfor', RandomForestClassifier())])
    classifier.fit(X_train, y_train)

    confidence = classifier.score(X_test, y_test)
    prediction = classifier.predict(X_test)

    print('Confidence is: ', confidence)
    print('Predicted spread: ', Counter(prediction))
    print('----\n')

for ticker in get_sp_tickers()[:20]:
    print(ticker)
    predict_voting(ticker)
