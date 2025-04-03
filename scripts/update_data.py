import pandas as pd
import numpy as np
np.NaN = np.nan # For pandas_ta
import yfinance as yf
import pandas_datareader as pdr
import pandas_ta as ta
import datetime
from datetime import timedelta

# Rate of change function
def rate_of_change(df, col, days_previous):
    return ((df[col] - df[col].shift(days_previous)) / days_previous)

# Momentum = (Current Price) * (R)
def momentum_calculation(current_price, rate_of_change):
    return (current_price * rate_of_change)

# Grab feature from dataset and get df
def filter_data(raw_df, features):
    raw_df.reset_index()
    df = pd.DataFrame()
    for feature in features:
        df[feature] = raw_df[features]
        
    df['Date'] = raw_df['Date']
    return df

# Gets data from FRED
def get_FRED_data(fred_code, start_date, end_date):
    df = pdr.get_data_fred(fred_code, start=start_date, end=end_date)
    df = df.reset_index()
    df['Date'] = df['DATE']
    df = df.drop('DATE', axis=1)
    return df

# Calculate momentum of feature
def get_momentum(df, feature,date_feature, div_factor=1000000, num_rows=-1):
    df = df.copy()
    df = df.reset_index()
    new_df = pd.DataFrame()
    new_df['Date'] = df[date_feature]
    new_df[feature] = df[feature]
    new_df['ROC'] = rate_of_change(new_df, feature, num_rows)
    new_df['Moment'] = momentum_calculation(new_df[feature], new_df['ROC'])
    new_df = new_df.drop(['ROC', feature], axis=1)
    new_df = new_df.tail(num_rows)
    new_df['Moment'] = (new_df['Moment'] / div_factor).round(2)
    return new_df

# For model output formatting
def get_stock_data(ticker, start_date, end_date):
    copy_df = yf.download(ticker, start=start_date, end=end_date).ffill().bfill()
    copy_df = copy_df.reset_index()
    copy_df = copy_df[['Date','Close']]
    copy_df.columns = copy_df.columns.get_level_values(0)
    copy_df = copy_df.rename(columns={
           'Date'  : 'DATE',
           'Close' : f'{ticker} Close'
    })
    return copy_df

def add_data_based_on_date(main_df, new_data, col_name):
    return pd.merge_asof(
            main_df, 
            new_data,
            on='DATE',
            direction='forward' # How we fill the gaps when adding content
        )[col_name]
    
# Variable from model used to get the right amount of previous days for the model input
CONTEXT_LEN = 120

# Getting dates to examine previous 50 days and 120 days of the S&P 500 and Dow Jones
today = datetime.date.today()
previous_365_days = today - timedelta(days=365)
previous_120_days = today - timedelta(days=CONTEXT_LEN)

sp_ticker = '^GSPC'
dj_ticker = '^DJI'
cpi_code = 'CPIAUCSL'
interest_rate_code = 'DFF'
unempl_rates = 'UNRATE'
initial_claims = 'ICSA'
job_openings_construction = 'JTS2300JOL'
mortgage_30_year = 'MORTGAGE30US'
retail_sales = 'RSAFS'
T10Y2Y = 'T10Y2Y'
T10YFF = 'T10YFF'

# Get Data for SP500
SP500_365_Day = yf.download(sp_ticker, start=previous_365_days, end=today)

# Get Data for model
SP_data = get_stock_data(sp_ticker, previous_120_days, today)
DJ_data = get_stock_data(dj_ticker, previous_120_days, today)

combined_df = pd.DataFrame()

combined_df['DATE'] = SP_data['DATE']

# Adding Stock Markets
combined_df[f'{sp_ticker} Close'] = add_data_based_on_date(combined_df, SP_data, f'{sp_ticker} Close')
combined_df[f'{sp_ticker} Close'] = add_data_based_on_date(combined_df, DJ_data, f'{sp_ticker} Close')

# Get Monetary Policy Data from FRED
cpi_df = get_FRED_data(cpi_code, previous_365_days, today)
interest_df = get_FRED_data(interest_rate_code, previous_365_days, today)
unemployment_df = get_FRED_data(unempl_rates, previous_365_days, today)
initial_claims_df = get_FRED_data(initial_claims, previous_365_days, today)
construction_jobs_df = get_FRED_data(job_openings_construction, previous_365_days, today)
mortgage_rate_df = get_FRED_data(mortgage_30_year, previous_365_days, today)
retail_df = get_FRED_data(retail_sales, previous_365_days, today)
T10Y2Y_df = get_FRED_data(T10Y2Y, previous_365_days, today)
T10YFF_df = get_FRED_data(T10YFF, previous_365_days, today)

# Grab Specified Column(s)
cpi_df = filter_data(cpi_df, [cpi_code]).ffill()
interest_df = filter_data(interest_df, [interest_rate_code]).ffill()
unemployment_df = filter_data(unemployment_df, [unempl_rates]).ffill()
initial_claims_df = filter_data(initial_claims_df, [initial_claims]).ffill()
construction_jobs_df = filter_data(construction_jobs_df, [job_openings_construction]).ffill()
mortgage_rate_df = filter_data(mortgage_rate_df, [mortgage_30_year]).ffill()
retail_df = filter_data(retail_df, [retail_sales]).ffill()
T10Y2Y_df = filter_data(T10Y2Y_df, [T10Y2Y]).ffill()
T10YFF_df = filter_data(T10YFF_df, [T10YFF]).ffill()


SP500_50day_momentum = get_momentum(SP500_365_Day, 'Close', 'Date', num_rows=50)
SP500_120day_momentum = get_momentum(SP500_365_Day, 'Close', 'Date', num_rows=120)

SP500_50day_momentum.to_csv("./data/SP50_day.csv")
SP500_120day_momentum .to_csv("./data/SP120_day.csv")

# Save FRED data frames to CSV files
cpi_df.to_csv("./data/cpi_data.csv")
interest_df.to_csv("./data/interest_rate_data.csv")
unemployment_df.to_csv("./data/unemployment_data.csv")
initial_claims_df.to_csv("./data/initial_claims_data.csv")
construction_jobs_df.to_csv("./data/construction_jobs_data.csv")
mortgage_rate_df.to_csv("./data/mortgage_rate_data.csv")
retail_df.to_csv("./data/retail_sales_data.csv")
T10Y2Y_df.to_csv("./data/T10Y2Y_data.csv")
T10YFF_df.to_csv("./data/T10YFF_data.csv")
combined_df.to_csv("./data/Model_Data.csv")


