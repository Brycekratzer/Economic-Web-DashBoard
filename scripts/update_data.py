import pandas as pd
import numpy as np
np.NaN = np.nan # For pandas_ta
import yfinance as yf
import pandas_datareader as pdr
import pandas_ta as ta
import datetime
from datetime import timedelta

# Getting dates to examine previous 50 days and 120 days of the S&P 500 and Dow Jones
today = datetime.date.today()
previous_50_days = today - timedelta(days=50)
previous_120_days = today - timedelta(days=120)

sp_ticker = '^GSPC'

# S&P data
SP500_50_Day = yf.download(sp_ticker, start=previous_50_days, end=today)
SP500_120_Day = yf.download(sp_ticker, start=previous_120_days, end=today)

# Grabbing Necessary Features from data 
SP500_50_Day_Formatted = SP500_50_Day['Close']
SP500_50_Day_Formatted.index = SP500_50_Day.index

SP500_50_Day.to_csv("../data/50_day.csv")
SP500_120_Day.to_csv("../data/120_day.csv")
