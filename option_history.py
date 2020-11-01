import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import datetime
import json

# get config
with open('dbconfig.json') as config:
    config = json.load(config)

# set variables
tickers = config['tickers']
engine = create_engine(config['connstr'])

def derived_cols(df, callput):
    """
    derives columns to make output more understandable
    """
    df.insert(0, 'AsOfDate', datetime.datetime.now())
    df.insert(1, 'ticker', ticker)
    df.insert(2, 'expiration', date)
    df.insert(3, 'CallPut', callput)

    df = df.drop(['lastPrice','contractSymbol','lastTradeDate', 'currency'], 1)

    return df


def get_option_chain(ticker_df, date):
    """
    returns concatenated calls/puts for a date
    """
    df_put = ticker_df.option_chain(date).puts
    df_put = derived_cols(df_put, 'put')
    df_call = ticker_df.option_chain(date).calls
    df_call = derived_cols(df_call, 'call')
    
    df = pd.concat([df_put, df_call])

    return df


if __name__ == "__main__":
    for ticker in tickers:
        ticker_df = yf.Ticker(ticker)
        opt_dates = ticker_df.options

        for date in opt_dates:
            df = get_option_chain(ticker_df, date)
            df.to_sql('options', engine, if_exists='append')
