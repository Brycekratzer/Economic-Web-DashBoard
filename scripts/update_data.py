import pandas as pd
import numpy as np
np.NaN = np.nan # For pandas_ta
import yfinance as yf
import pandas_datareader as pdr
import pandas_ta as ta
import datetime
from datetime import timedelta
from sklearn.preprocessing import RobustScaler


#
# Variables from model used to get the right amount of previous days for the model input
# Variables from FRED and yfinance to gather data
#

CONTEXT_LEN = 150
WINDOW_SIZE = int(365 * 1.5)
sp_ticker = '^GSPC'
dj_ticker = '^DJI'

spf_ticker = 'ES=F'
djf_ticker = 'YM=F'

cpi_code = 'CPIAUCSL'
interest_rate_code = 'DFF'
unempl_rates = 'UNRATE'
initial_claims = 'ICSA'
job_openings_construction = 'JTS2300JOL'
mortgage_30_year = 'MORTGAGE30US'
retail_sales = 'RSAFS'
T10Y2Y = 'T10Y2Y'
T10YFF = 'T10YFF'

#
# Defining Functions 
#

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
           'Close' : f'{ticker} Close'
    })
    return copy_df

# For adding stock data to model data
def add_data_based_on_date(main_df, new_data, col_name):
    return pd.merge_asof(
            main_df, 
            new_data,
            on='Date',
            direction='forward' # How we fill the gaps when adding content
        )[col_name]
    
# For normalizing stock data
def norm_data_st(df, col, window_size=90):
    df_scaled = df.copy()

    # Moving through each row starting at 
    # window_size and going to df length
    for i in range(window_size, len(df)):

        # Grabs data from past
        time_window = df.iloc[i-window_size:i]

        # Grab current time
        current_time = df.iloc[i:i+1]

        # Create scaler on based on window
        robust_scaler = RobustScaler()
        robust_scaler.fit(time_window[col])

        # Apply scaler to current index feature
        scaled_values = robust_scaler.transform(current_time[col])
        df_scaled.loc[df.index[i], col] = scaled_values[0]
    return df_scaled


# For adjusting for inflation
def adjust_for_inflation(df, features, CPI_yearly_amount, CPI_2025):
    df = df.copy()

    # Get Year for both DF's
    df['Year'] = df['Date'].dt.year
    CPI_yearly_amount = CPI_yearly_amount.rename(columns={'Date' : 'Year'})

    # Add a new column to the df that has the CPI for each year
    df = pd.merge_asof(df, CPI_yearly_amount, on='Year', direction='forward')
                        
    # Adjust each value for inflation       
    for feature in features:
        df[feature] = df[feature] * (CPI_2025 / df[cpi_code])
        
    df = df.drop([cpi_code, 'Year'], axis=1)
        
    return df

#
# Getting proper dates for data gathering
#

# Getting dates to examine previous 50 days and 120 days of the S&P 500 and Dow Jones
today = datetime.date.today() + timedelta(days=1)
previous_365_days = today - timedelta(days=365)

# Include a padding for weekends and get a year and half of prior data for normalization
previous_120_days = today - timedelta(days=((CONTEXT_LEN * 2 + WINDOW_SIZE * 2)))


#
# Getting data for analysis portion of website 
#

# Get Data for SP500
SP500_365_Day = yf.download(sp_ticker, start=previous_365_days, end=today)

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

#
# Adjusting Stock Price's for inflation and normalizing data 
# for model development.
#

# Get the average CPI for each year to calculate inflation
CPI_yearly_amount = cpi_df.groupby(cpi_df['Date'].dt.year)[cpi_code].mean().reset_index()

# For later calculations
CPI_2025 = CPI_yearly_amount[CPI_yearly_amount['Date'] == 2025][cpi_code].values[0]

# Get Data for model
SP_data = get_stock_data(sp_ticker, previous_120_days, today)
DJ_data = get_stock_data(dj_ticker, previous_120_days, today)
SPF_data = get_stock_data(spf_ticker, previous_120_days, today)
DJF_data = get_stock_data(djf_ticker, previous_120_days, today)

# Gather Data For model
combined_df = pd.DataFrame()
combined_df['Date'] = SP_data['Date']

# Adding Stock Markets
combined_df[f'{sp_ticker} Close'] = add_data_based_on_date(combined_df, SP_data, f'{sp_ticker} Close')
combined_df[f'{dj_ticker} Close'] = add_data_based_on_date(combined_df, DJ_data, f'{dj_ticker} Close')
combined_df[f'{spf_ticker} Close'] = add_data_based_on_date(combined_df, SPF_data, f'{spf_ticker} Close')
combined_df[f'{djf_ticker} Close'] = add_data_based_on_date(combined_df, DJF_data, f'{djf_ticker} Close')
combined_df = adjust_for_inflation(combined_df, [f'{sp_ticker} Close', f'{dj_ticker} Close', f'{djf_ticker} Close', f'{spf_ticker} Close'], CPI_yearly_amount, CPI_2025)

# For denormilzation of data after prediction
pre_norm_stock_data = combined_df.copy()

# Normalize data for model
post_norm_stock_data = norm_data_st(combined_df, [f'{sp_ticker} Close', f'{dj_ticker} Close', f'{djf_ticker} Close', f'{spf_ticker} Close'], WINDOW_SIZE)

SP500_50day_momentum = get_momentum(SP500_365_Day, 'Close', 'Date', num_rows=50)
SP500_120day_momentum = get_momentum(SP500_365_Day, 'Close', 'Date', num_rows=120)

SP500_50day_momentum.to_csv("./data/stock_momentum/SP50_day.csv")
SP500_120day_momentum .to_csv("./data/stock_momentum/SP120_day.csv")

# Save FRED data frames to CSV files
cpi_df.to_csv("./data/monetary_policy/cpi_data.csv")
interest_df.to_csv("./data/monetary_policy/interest_rate_data.csv")
unemployment_df.to_csv("./data/monetary_policy/unemployment_data.csv")
initial_claims_df.to_csv("./data/monetary_policy/initial_claims_data.csv")
construction_jobs_df.to_csv("./data/monetary_policy/construction_jobs_data.csv")
mortgage_rate_df.to_csv("./data/monetary_policy/mortgage_rate_data.csv")
retail_df.to_csv("./data/monetary_policy/retail_sales_data.csv")
T10Y2Y_df.to_csv("./data/monetary_policy/T10Y2Y_data.csv")
T10YFF_df.to_csv("./data/monetary_policy/T10YFF_data.csv")
post_norm_stock_data.to_csv("./data/model_data/Post_Norm_Model_Data.csv")
pre_norm_stock_data.to_csv("./data/model_data/Pre_Norm_Model_Data.csv")


