import yfinance as yf
import numpy as np
import pandas as pd
from sys import argv


def ticker_hist (Ticker):
    """
    returns pandas dataframe containing yahoo finance history for given ticker
    """
    ticker = yf.Ticker(Ticker)
    df = ticker.history(period="max")
    df.insert(0, 'Ticker', Ticker)

    return df


def date_framing(df, window):
    """
    Filters dataframe for date window of interest
    """
    if window == 'Daily':
        pass
    elif window == 'Weekly':
        df = df.resample('W').last()
    elif window == 'BiWeekly':
        df = df.resample('W').last()
        df = df.loc[::2, :] # only every other
    elif window == 'Monthly':
        df = df.resample('M').last()
    elif window == 'Yearly':
        df = df.groupby([df.index.year]).tail(1)
    else:
        raise ValueError('Enter a valid return period (Daily, Weekly, BiWeekly, Monthly, Yearly).')

    df.insert(1, 'ReturnPeriod', window)

    return df


def attribution(df):
    """
    Returns performance attribution calcs
    """
    df['PrevClose'] = df['Close'].shift(1)
    df['DeltaPrice'] = df['Close'] - df['PrevClose']
    df['Delta'] = df['DeltaPrice'] + df['Dividends']
    df['Return'] = df['Delta'] / df['PrevClose'] * 100
    df['Sigma'] = df.Return.rolling(30).std() * np.sqrt(252)
    
    return df


def returns(Ticker, ReturnPeriod):
    df = ticker_hist(Ticker)
    df = date_framing(df, ReturnPeriod)
    df = attribution(df)

    df = df.drop(columns=['Stock Splits','PrevClose'],axis=1)

    return df


if __name__ == '__main__':
    script, Ticker, ReturnPeriod = argv
    print(returns(Ticker, ReturnPeriod).sort_index(ascending=False).head(20))
