import pandas as pd
import numpy as np
np.NaN = np.nan # For pandas_ta
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader as pdr
import pandas_ta as ta
import datetime
from datetime import timedelta

# adds data to data frame
def get_data_frame(fred_code, start_date, end_date):
    df = pdr.get_data_fred(fred_code, start=start_date, end=end_date)
    df = df.reset_index()
    df['Date'] = df['DATE']
    return df


today = datetime.date.today()
previous_date = today - timedelta(days=50)

sp_ticker = '^GSPC'
dj_ticker = '^DJI'

# S&P data
SP500_2000_2025 = yf.download(sp_ticker, start=previous_date, end=end_date)

# Dow Jones data
Dow_Jones_Inflation = yf.download(dj_ticker, start=start_date, end=end_date)

print(yesterday)
