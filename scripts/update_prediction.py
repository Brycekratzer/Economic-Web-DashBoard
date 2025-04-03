import torch
import pandas as pd
from datetime import datetime, timedelta
from transformers import PatchTSTConfig, PatchTSTForPrediction

# How many features we are including 
NUM_INPUT = 2
# Batch size for training
BATCH_SIZE = 8
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
device = torch.device('cpu')
state_dict = torch.load('pt_v2_ft_v1_model.bin')
ft_model.load_state_dict(state_dict)

ft_model = ft_model.to(device)

# Get the normalized economic data
pred_and_original_data = pd.read_csv('../data/Economic_Data_1994-2025.csv')

# Filter out data to only contain features needed and Date for merging
pred_and_original_data = pred_and_original_data[['DATE']+features_to_pred]

# How many predictions we will recursively make
NUM_ITER = 120

# Autoregression
for day in range(NUM_ITER):
    
    # Drop the date for prediction
    df_copy = pred_and_original_data.drop(['DATE'], axis=1)
    
    
    with torch.no_grad():
        # Grab the last instance of CONTEXT_LEN days
        features = df_copy.iloc[-CONTEXT_LEN:].values
        
        # Convert to proper format for model
        features = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        

        predictions = ft_model(past_values=features)
        forcast = predictions.prediction_outputs
    
    # Convert predictions back to prior format
    predictions = forcast.squeeze(0).numpy()
    pred_np = predictions
    
    # Get the last date in the dataset
    last_date = pd.to_datetime(pred_and_original_data['DATE'])
    last_date = last_date[len(pred_and_original_data) - 1]

    # Create date range for predictions
    future_dates = pd.date_range(
        start=last_date + timedelta(days=1),
        periods=PRED_LEN,
        freq='D'
    )
    
    # Create a dataframe of our predictions with their corresponding dates
    pred_df = pd.DataFrame(pred_np, columns=features_to_pred)
    pred_df['DATE'] = future_dates

    # Add predictions to dataset
    pred_and_original_data = pd.concat([pred_and_original_data, pred_df], ignore_index=True)
    pred_and_original_data['DATE'] = pd.to_datetime(pred_and_original_data['DATE'])