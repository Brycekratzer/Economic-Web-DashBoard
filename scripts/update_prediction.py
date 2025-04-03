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
        print(time_window['Date'])

        # Grab current time
        current_time = norm_df.iloc[i:i+1]

        # Create scaler on based on window
        robust_scaler = RobustScaler()
        robust_scaler.fit(time_window[col])

        # Apply scaler to current index feature
        denomralized_values = robust_scaler.inverse_transform(current_time[col])
        denorm_df.loc[norm_df.index[i], col] = denomralized_values[0]
    return denorm_df

# Used for denormalizing data
WINDOW_SIZE = int(365 * 1.5)
# How many features we are including 
NUM_INPUT = 2
# For What we are predicting
NUM_TARGET = 2
# How many steps we take in the context length
CONTEXT_LEN = 120
# How many steps we take in the context length
PATCH_LEN = 20
# How far we move our patch length
PATCH_STRD = 10
# How many days to predict into the future
PRED_LEN = 3 # Three Day Prediction
# For past predictions
PRIOR_DAYS = 50

ft_config = PatchTSTConfig(
    num_input_channels = NUM_INPUT,
    num_targets = NUM_TARGET,
    context_length = CONTEXT_LEN,
    patch_length = PATCH_LEN,
    stride = PATCH_STRD,
    prediction_length=PRED_LEN
)

features_to_pred = ['^GSPC Close', '^DJI Close']

ft_model = PatchTSTForPrediction(ft_config)

# Load in our model
state_dict = torch.load('./model/pt_v2_ft_v1_model.bin', map_location=torch.device('cpu'))
ft_model.load_state_dict(state_dict)
ft_model.eval()

# Get the normalized economic data
pred_and_original_data = pd.read_csv('./data/Post_Norm_Model_Data.csv')

# Filter out data to only contain features needed and Date for merging
pred_and_original_data = pred_and_original_data[['Date']+features_to_pred]
pred_and_original_data_50_prior = pred_and_original_data[['Date']+features_to_pred]

pred_and_original_data_50_prior = pred_and_original_data_50_prior[0:len(pred_and_original_data_50_prior) - PRIOR_DAYS]

# How many predictions we will recursively make
NUM_ITER = 10

# Autoregression
for day in range(NUM_ITER):
    
    # Drop the date for prediction
    df_copy = pred_and_original_data.drop(['Date'], axis=1)
    df_copy_50 = pred_and_original_data_50_prior.drop(['Date'], axis=1)
    
    with torch.no_grad():
        # Grab the last instance of CONTEXT_LEN days
        features = df_copy.iloc[-CONTEXT_LEN:].values
        features_50 = df_copy_50.iloc[-CONTEXT_LEN:].values
        
        # Convert to proper format for model
        features = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        features_50 = torch.tensor(features_50, dtype=torch.float32).unsqueeze(0)

        predictions = ft_model(past_values=features)
        predictions_50 = ft_model(past_values=features_50)
        
        forcast = predictions.prediction_outputs
        forcast_50 = predictions_50.prediction_outputs
    
    # Convert predictions back to prior format
    predictions = forcast.squeeze(0).numpy()
    predictions_50 = forcast_50.squeeze(0).numpy()
    
    pred_np = predictions
    pred_np_50 = predictions_50
    
    # Get the last date in the dataset
    last_date = pd.to_datetime(pred_and_original_data['Date'])
    last_date = last_date[len(pred_and_original_data) - 1]
    
    last_date_50 = pd.to_datetime(pred_and_original_data_50_prior['Date'])
    last_date_50 = last_date_50[len(pred_and_original_data_50_prior) - 1]

    # Create date range for predictions
    future_dates = pd.date_range(
        start=last_date + timedelta(days=1),
        periods=PRED_LEN,
        freq='D'
    )
    
    future_dates_50 = pd.date_range(
        start=last_date_50 + timedelta(days=1),
        periods=PRED_LEN,
        freq='D'
    )
    
    # Create a dataframe of our predictions with their corresponding dates
    pred_df = pd.DataFrame(pred_np, columns=features_to_pred)
    pred_df['Date'] = future_dates
    
    pred_df_50 = pd.DataFrame(pred_np_50, columns=features_to_pred)
    pred_df_50['Date'] = future_dates_50

    # Add predictions to dataset
    pred_and_original_data = pd.concat([pred_and_original_data, pred_df], ignore_index=True)
    pred_and_original_data['Date'] = pd.to_datetime(pred_and_original_data['Date'])
    
    pred_and_original_data_50_prior = pd.concat([pred_and_original_data_50_prior, pred_df_50], ignore_index=True)
    pred_and_original_data_50_prior['Date'] = pd.to_datetime(pred_and_original_data_50_prior['Date'])
    
# Load in unnormalized data and format to match features we are predicting
original_df = pd.read_csv('./data/Pre_Norm_Model_Data.csv')
original_df_50 = original_df[0:len(original_df) - PRIOR_DAYS]

original_df = original_df[['Date'] + features_to_pred]
original_df['Date'] = pd.to_datetime(original_df['Date'])

original_df_50 = original_df_50[['Date'] + features_to_pred]
original_df_50['Date'] = pd.to_datetime(original_df_50['Date'])

# Get columns to normalize that doesn't include date.
columns_to_unnormalize = pred_and_original_data.drop(['Date'], axis=1).columns
unnorm_df = norm_data_st(pred_and_original_data, original_df, columns_to_unnormalize,WINDOW_SIZE)    

filtered_start = int(len(unnorm_df) * .90)
    
unnorm_df[filtered_start:len(unnorm_df) - NUM_ITER*PRED_LEN].to_csv('./data/pre_prediction_stocks.csv')
unnorm_df[len(unnorm_df) - NUM_ITER*PRED_LEN:len(unnorm_df)].to_csv('./data/prediction_stocks.csv')

columns_to_unnormalize_50 = pred_and_original_data_50_prior.drop(['Date'], axis=1).columns
unnorm_df_50 = norm_data_st(pred_and_original_data_50_prior, original_df_50, columns_to_unnormalize,WINDOW_SIZE)    

filtered_start_50 = int(len(unnorm_df_50) * .90)
    
unnorm_df_50[filtered_start_50:len(unnorm_df_50) - NUM_ITER*PRED_LEN].to_csv('./data/pre_prediction_stocks_50_prior.csv')
unnorm_df_50[len(unnorm_df_50) - NUM_ITER*PRED_LEN:len(unnorm_df_50)].to_csv('./data/prediction_stocks_50_prior.csv')
