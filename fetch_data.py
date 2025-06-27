import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval, group_by='ticker', auto_adjust=True)
    if ticker in df.columns.get_level_values(0):
        df = df[ticker].copy()
    else:
        df = df.loc[:, pd.IndexSlice[:, ticker]].copy()
        df.columns = df.columns.droplevel(1)
    return df