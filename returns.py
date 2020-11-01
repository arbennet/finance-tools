import yfinance as yf
import math
import pandas as pd
from sys import argv
from stockstats import StockDataFrame as sdf


def ticker_hist (Ticker):
    """
    returns pandas dataframe containing yahoo finance history for given ticker
    """
    df = yf.Ticker(Ticker).history(period="max")
    df.insert(0, 'ticker', Ticker)
    df['cum_dividend'] = df.Dividends.cumsum()
    df.columns= df.columns.str.lower()

    return df


def date_framing(df, horizon):
    """
    Filters dataframe for date horizon of interest
    """
    if horizon == 'Daily':
        pass
    elif horizon == 'Weekly':
        df = df.resample('W').last()
    elif horizon == 'BiWeekly':
        df = df.resample('W').last()
        df = df.loc[::2, :] # only every other
    elif horizon == 'Monthly':
        df = df.resample('M').last()
    elif horizon == 'Yearly':
        df = df.groupby([df.index.year]).tail(1)
    else:
        raise ValueError('Enter a valid return period (Daily, Weekly, BiWeekly, Monthly, Yearly).')

    df.insert(1, 'horizon', horizon)

    return df


def attribution(df):
    """
    Returns performance attribution calcs
    """
    df['return'] = (((df['close'] + (df['cum_dividend'] - df['cum_dividend'].shift(1))) /  df['close'].shift(1)) - 1) * 100

    return df


def technicals(df):
    df['vol30_annualized'] = df['return'].rolling(30).std() * math.sqrt(252)
    df = sdf.retype(df)
    df['macds']
    df['rsi_12']

    return df


def returns(Ticker, ReturnPeriod):
    df = ticker_hist(Ticker)
    df = date_framing(df, ReturnPeriod)
    df = attribution(df)

    if ReturnPeriod == 'Daily':
        df = technicals(df)

    df = df.drop(columns=['stock splits', 'cum_dividend','close_-1_s','close_-1_d','macdh','rs_12'], axis=1, errors='ignore')

    return df


if __name__ == '__main__':
    script, Ticker, ReturnPeriod = argv
    print(returns(Ticker, ReturnPeriod).sort_index(ascending=False).head(20))
