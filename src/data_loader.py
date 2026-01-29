import yfinance as yf
import pandas as pd

def load_nifty_data(period="6mo"):
    """
    Load recent NIFTY 50 data
    """
    df = yf.download("^NSEI", period=period, interval="1d")
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.dropna(inplace=True)
    return df
