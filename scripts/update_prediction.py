import torch
import pandas as pd
from datetime import datetime, timedelta
from transformers import PatchTSTConfig, PatchTSTForPrediction
from sklearn.preprocessing import RobustScaler


def norm_data_st(norm_df, df, col, window_size=90):
    denorm_df = norm_df.copy()

    # Moving through each row starting at 
    # window_size and going to df length
    for i in range(window_size, len(norm_df)):
        # Grabs data from past
        time_window = df.iloc[i - window_size:i]


        # Grab current time
        current_time = norm_df.iloc[i:i+1]

        # Create scaler on based on window
        robust_scaler = RobustScaler()
        robust_scaler.fit(time_window[col])

        # Apply scaler to current index feature
        denomralized_values = robust_scaler.inverse_transform(current_time[col])
        denorm_df.loc[norm_df.index[i], col] = denomralized_values[0]
    return denorm_df

# Function to advance date to next business day
def next_business_day(date):
    # Add one day initially
    next_date = date + timedelta(days=1)
    
    # Keep adding days until we reach a weekday (Monday-Friday)
    while next_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        next_date = next_date + timedelta(days=1)
        
    return next_date

# Used for denormalizing data
WINDOW_SIZE = int(365 * 1.5)
# How many features we are including 
NUM_INPUT = 4
# For What we are predicting
NUM_TARGET = 4
# How many steps we take in the context length
CONTEXT_LEN = 150
# How many steps we take in the context length
PATCH_LEN = 10
# How far we move our patch length
PATCH_STRD = 5
# How many days to predict into the future
PRED_LEN = 3 # Three Day Prediction
# For past predictions
PRIOR_DAYS = 40
# For past week
PRIOR_WEEK = 6

ft_config = PatchTSTConfig(
    num_input_channels = NUM_INPUT,
    num_targets = NUM_TARGET,
    context_length = CONTEXT_LEN,
    patch_length = PATCH_LEN,
    patch_stride = PATCH_STRD,
    prediction_length=PRED_LEN
)

features_to_pred = ['^GSPC Close', '^DJI Close', 'ES=F Close', 'YM=F Close']

ft_model = PatchTSTForPrediction(ft_config)

# Load in our model
state_dict = torch.load('./model/pt_1*5yn_v1_ft_3d_v1.bin', map_location=torch.device('cpu'))
ft_model.load_state_dict(state_dict)

# Get the normalized economic data
pred_and_original_data = pd.read_csv('./data/model_data/Post_Norm_Model_Data.csv')

# Filter out data to only contain features needed and Date for merging
pred_and_original_data = pred_and_original_data[['Date']+features_to_pred]
pred_and_original_data_50_prior = pred_and_original_data[['Date']+features_to_pred]
pred_and_original_data_week_prior = pred_and_original_data[['Date']+features_to_pred]

pred_and_original_data_50_prior = pred_and_original_data_50_prior[0:len(pred_and_original_data_50_prior) - PRIOR_DAYS]
pred_and_original_data_week_prior = pred_and_original_data_week_prior[0:len(pred_and_original_data_week_prior) - PRIOR_WEEK]

# How many predictions we will recursively make
NUM_ITER = 7

# Autoregression
for day in range(NUM_ITER):
    
    ft_model.eval()
    
    # Drop the date for prediction
    df_copy = pred_and_original_data.drop(['Date'], axis=1)
    df_copy_50 = pred_and_original_data_50_prior.drop(['Date'], axis=1)
    df_copy_week = pred_and_original_data_week_prior.drop(['Date'], axis=1)
    
    with torch.no_grad():
        # Grab the last instance of CONTEXT_LEN days
        features = df_copy.iloc[-CONTEXT_LEN:].values
        features_50 = df_copy_50.iloc[-CONTEXT_LEN:].values
        features_week = df_copy_week.iloc[-CONTEXT_LEN:].values
        
        # Convert to proper format for model
        features = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        features_50 = torch.tensor(features_50, dtype=torch.float32).unsqueeze(0)
        features_week = torch.tensor(features_week, dtype=torch.float32).unsqueeze(0)

        predictions = ft_model(past_values=features)
        predictions_50 = ft_model(past_values=features_50)
        predictions_week = ft_model(past_values=features_week)
        
        forcast = predictions.prediction_outputs
        forcast_50 = predictions_50.prediction_outputs
        forcast_week = predictions_week.prediction_outputs
    
    # Convert predictions back to prior format
    predictions = forcast.squeeze(0).numpy()
    predictions_50 = forcast_50.squeeze(0).numpy()
    predictions_week = forcast_week.squeeze(0).numpy()
    
    pred_np = predictions
    pred_np_50 = predictions_50
    pred_np_week = predictions_week
    
    # Get the last dates in the datasets
    last_date = pd.to_datetime(pred_and_original_data['Date']).iloc[-1]
    last_date_50 = pd.to_datetime(pred_and_original_data_50_prior['Date']).iloc[-1]
    last_date_week = pd.to_datetime(pred_and_original_data_week_prior['Date']).iloc[-1]

    if last_date.weekday() >= 5:
        last_date = last_date + timedelta(days=1)
        if last_date.weekday() >= 5:
            last_date = last_date + timedelta(days=1)
            
    if last_date_50.weekday() >= 5:
        last_date_50 = last_date_50 + timedelta(days=1)
        if last_date_50.weekday() >= 5:
            last_date_50 = last_date_50 + timedelta(days=1)
            
    if last_date_week.weekday() >= 5:
        last_date_week = last_date_week + timedelta(days=1)
        if last_date_week.weekday >= 5:
            last_date_week = last_date_week + timedelta(days=1)

    # Create date range for predictions
    future_dates = pd.date_range(
        start=last_date + timedelta(days=1),
        periods=PRED_LEN,
        freq='B'
    )
    
    future_dates_50 = pd.date_range(
        start=last_date_50 + timedelta(days=1),
        periods=PRED_LEN,
        freq='B'
    )
    
    future_dates_week = pd.date_range(
        start=last_date_week + timedelta(days=1),
        periods=PRED_LEN,
        freq='B'
    )
    
    # Create a dataframe of our predictions with their corresponding dates
    pred_df = pd.DataFrame(pred_np, columns=features_to_pred)
    pred_df['Date'] = future_dates
    
    pred_df_50 = pd.DataFrame(pred_np_50, columns=features_to_pred)
    pred_df_50['Date'] = future_dates_50
    
    pred_df_week = pd.DataFrame(pred_np_week, columns=features_to_pred)
    pred_df_week['Date'] = future_dates_week

    # Add predictions to dataset
    pred_and_original_data = pd.concat([pred_and_original_data, pred_df], ignore_index=True)
    pred_and_original_data['Date'] = pd.to_datetime(pred_and_original_data['Date'])
    
    pred_and_original_data_50_prior = pd.concat([pred_and_original_data_50_prior, pred_df_50], ignore_index=True)
    pred_and_original_data_50_prior['Date'] = pd.to_datetime(pred_and_original_data_50_prior['Date'])
    
    pred_and_original_data_week_prior = pd.concat([pred_and_original_data_week_prior, pred_df_week], ignore_index=True)
    pred_and_original_data_week_prior['Date'] = pd.to_datetime(pred_and_original_data_week_prior['Date'])
    
# Load in unnormalized data and format to match features we are predicting
original_df = pd.read_csv('./data/model_data/Pre_Norm_Model_Data.csv')
original_df_50 = original_df[0:len(original_df) - PRIOR_DAYS]
original_df_week = original_df[0:len(original_df) - PRIOR_WEEK]

original_df = original_df[['Date'] + features_to_pred]
original_df['Date'] = pd.to_datetime(original_df['Date'])

original_df_50 = original_df_50[['Date'] + features_to_pred]
original_df_50['Date'] = pd.to_datetime(original_df_50['Date'])

original_df_week = original_df_week[['Date'] + features_to_pred]
original_df_week['Date'] = pd.to_datetime(original_df_week['Date'])

# Get columns to normalize that doesn't include date.
columns_to_unnormalize = pred_and_original_data.drop(['Date'], axis=1).columns
unnorm_df = norm_data_st(pred_and_original_data, original_df, columns_to_unnormalize,WINDOW_SIZE)    

# Filter for when to start data for visual
filtered_start = int(len(unnorm_df) * .95)

# Exporting predictions
unnorm_df[filtered_start:len(unnorm_df) - NUM_ITER*PRED_LEN].to_csv('./data/model_projections/pre_prediction_stocks.csv')
unnorm_df[len(unnorm_df) - NUM_ITER*PRED_LEN:len(unnorm_df)].to_csv('./data/model_projections/prediction_stocks.csv')


# Predictions from 50 days prior
columns_to_unnormalize_50 = pred_and_original_data_50_prior.drop(['Date'], axis=1).columns
unnorm_df_50 = norm_data_st(pred_and_original_data_50_prior, original_df_50, columns_to_unnormalize,WINDOW_SIZE)    

filtered_start_50 = int(len(unnorm_df_50) * .95)
    
unnorm_df_50[filtered_start_50:len(unnorm_df_50) - NUM_ITER*PRED_LEN].to_csv('./data/model_projections/pre_prediction_stocks_50_prior.csv')
original_df[len(original_df_50):len(original_df_50) + (NUM_ITER * PRED_LEN)].to_csv('./data/model_projections/actual_stock_50_prior.csv')

unnorm_df_50[len(unnorm_df_50) - NUM_ITER*PRED_LEN:len(unnorm_df_50)].to_csv('./data/model_projections/prediction_stocks_50_prior.csv')

# Predictions from a week days prior
columns_to_unnormalize_week = pred_and_original_data_week_prior.drop(['Date'], axis=1).columns
unnorm_df_week = norm_data_st(pred_and_original_data_week_prior, original_df_week, columns_to_unnormalize,WINDOW_SIZE)    

filtered_start_week = int(len(original_df_week) * .985)
    
unnorm_df_week[filtered_start_week:len(original_df_week)].to_csv('./data/model_projections/pre_prediction_stocks_week_prior.csv')
original_df[len(original_df_week):len(original_df_week) + PRIOR_WEEK].to_csv('./data/model_projections/actual_stock_week_prior.csv')

unnorm_df_week[len(unnorm_df_week) - NUM_ITER*PRED_LEN:(len(unnorm_df_week) - NUM_ITER*PRED_LEN) + PRIOR_WEEK + 5].to_csv('./data/model_projections/prediction_stocks_week_prior.csv')
