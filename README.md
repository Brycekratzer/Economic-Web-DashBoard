# Economic Dashboard

A data-driven web application that visualizes the current state of the United States economy using FRED (Federal Reserve Economic Data) and Yahoo Finance data. The dashboard offers an intuitive interface to track market trends, economic indicators, and financial metrics while providing machine learning-based stock market projections.

## Key Features

### Predictive Analytics
At the core of this dashboard is the forecasting capability powered by the [PatchTST](https://github.com/yuqinie98/PatchTST) (Patch Time Series Transformer) model. The system provides short-term projections for the S&P 500 and Dow Jones indices by analyzing complex relationships between multiple economic factors. The dashboard displays both current predictions and historical forecast accuracy to demonstrate model performance.

### Automated Data Pipeline
The application maintains data freshness through a fully automated pipeline that:
- Fetches data from authoritative financial sources every other day
- Processes and normalizes time series data using statistical methods
- Applies inflation adjustments for accurate historical comparisons
- Updates visualizations and model predictions automatically

### Interactive Visualizations
All economic indicators and predictions are presented through interactive D3.js visualizations that allow users to:
- Examine stock market momentum over 50-day and 120-day periods
- Monitor critical economic indicators including yield curves, interest rates, and employment metrics
- Compare model predictions with actual market performance

## Technology Stack

### Frontend
- **Languages**: HTML5, CSS3, JavaScript
- **Visualization Library**: D3.js
- **Responsive Design**: Custom CSS implementation for multi-device compatibility

### Backend & Data Processing
- **Languages**: Python 3
- **Data Processing**: pandas, pandas_ta, NumPy
- **Machine Learning**: PyTorch, Hugging Face Transformers, scikit-learn
- **Data Sources**: Yahoo Finance API (yfinance), Federal Reserve Economic Database (FRED) via pandas_datareader

### Machine Learning
- **Architecture**: PatchTST (Patch Time Series Transformer)
- **Training Approach**: Pretrained on historical economic data (1994-2025), fine-tuned for financial forecasting
- **Prediction Horizon**: 3-day forecasts with autoregressive capabilities

### Deployment & DevOps
- **Hosting**: GitHub Pages
- **Automation**: GitHub Actions for scheduled data retrieval and model inference
- **Version Control**: Git

## Data Pipeline Architecture

### Collection
The system collects comprehensive financial and economic data through `update_data.py`, including:

- **Stock Market Indices**: S&P 500, Dow Jones Industrial Average, NASDAQ (Open, High, Low, Close, Volume)
- **Economic Indicators**: 
  - Inflation metrics (CPI)
  - Interest rates (Federal Funds Rate, Treasury yields, mortgage rates)
  - Employment metrics (Unemployment rate, job openings, initial claims)
  - Economic activity indicators (GDP, retail sales, industrial production)
  - Consumer metrics (Personal income, consumer debt, saving rates)

### Processing
The pipeline applies sophisticated data processing techniques:
1. **Missing Value Handling**: Forward-fill methodology for consistent time series
2. **Inflation Adjustment**: CPI-based normalization to ensure value comparability across time
3. **Time Series Normalization**: Rolling window RobustScaler implementation to handle outliers and maintain temporal context
4. **Feature Engineering**: Calculation of momentum indicators and economic relationships

### Modeling
The PatchTST model implementation includes:
1. **Pretraining**: Masked modeling on full economic dataset
2. **Fine-tuning**: Optimization for S&P 500 and Dow Jones prediction
3. **Inference**: Autoregressive prediction with 3-day horizon
4. **Validation**: Historical prediction comparison with actual values

## Visualization Framework

The dashboard presents data through a structured D3.js implementation that:
1. Loads processed CSV data from the data directory
2. Creates responsive line charts with adaptive scales
3. Implements interactive features including tooltips for detailed data points
4. Presents model predictions alongside historical data for context

The clean, minimalist UI design emphasizes data clarity while maintaining accessibility across device types.

## Disclaimer

The projections provided are intended for educational purposes, speculation, and curiosity only, and SHOULD NOT be used as investing advice. Like all predictive models, it has inherent limitations and cannot account for unexpected market events or sentiment shifts. Past performance does not guarantee future results, and users should always consult with qualified financial professionals before making investment decisions.

## File Structure

```
├── .github/
│   └── workflows/
│       ├── static.yml                  # GitHub Pages deployment workflow
│       └── update-data.yml             # Data processing automation (runs every other day)
│
├── static/                             # Frontend assets (corrected location)
│   ├── display.js                      # D3.js visualizations
│   └── styles.css                      # Dashboard styling
│
├── scripts/
│   ├── update_prediction.py            # Model inference script for stock predictions
│   └── update_data.py                  # Data collection from FRED and Yahoo Finance
│
├── data/                               # Processed data storage
│   ├── monetary_policy/                # Economic indicators
│   ├── stock_momentum/                 # Stock momentum metrics
│   ├── model_projections/              # Data for display.js visualizations 
│   └── model_data/                     # Data for model input/output
│      ├── Pre_Norm_Model_Data.csv      # Raw data
│      └── Post_Norm_Model_Data.csv     # Normalized data
│
├── model/                              # ML model development
│   ├── PatchTST.ipynb                  # Model training notebook
│   ├── Gather_Historical_Data.ipynb    # Data preprocessing for training
│   ├── past_models/                    # Models that were used previously, stored for reference
│   └── pretrained_models/              # Saved model weights
│
├── index.html                          # Main dashboard page
└── requirements.txt                    # Python dependencies
```

## Updates 

### April 2025

Implemented a working predicitive pipieline using a pretrained PatchTST model. All
pretraining was done locally using a derived historical csv file from 1994-2025. 

#### TODO

- make the graph on front end able to see points when you hover over the line on
    graph.

- fix weird centering bug for metric containers on front end

- display date for when model and data was last updated
  
- Try a new model **AFTER ALL IS COMPLETED ABOVE**

### March 30th 2025

Added Montary Policy Data, and moved the `updated_data.py` script to run only every Saturday as a good amount of economic indictors don't have readily available data updated daily.

Attempting to use the `PatchTST` model to project economic performance using data from 1994-2025

### March 29th 2025

Updated diretory paths for smooth git action updates. Working on accessing `.csv` files from data directory in the app.js file. Made a simple pipeline structure for data preprocessing in `scripts/update_data.py`

Implemented the `display.js` file that was responsible for updating and adding graphs to the front end by using `D3`. Still need to modify the CSS file to edit how it looks and also include new files from FRED data via `pandas_ta`in the `update_data.py`

Also updated the `update-data.yml` file to only run at 5:30 PM MST every week day to help preserve github's free resources. 

### March 27th 2025

Added a new github action that add's dependency's for preprocessing data from yfinance and and FRED data.

This action adds a cache that has dependency's installed and if a new package is added everything is reinstalled. This helps with time management for deployment.

Also made it so we run the `update_data.py` file located in the `/scripts` directory every 6 hours. In theory, every 6 hours this script will run preprocessing a new set of data from yfinance and FRED then export into a csv file into the `/data` directory.

**Side Note**
Would be more beneficial to run the script at different hours of the day for example:

- First time running: 7:30am MST
    - When the stock market opens
    - New FRED economic data is added

- Second time running: 12pm MST
    - Mid day of trading

- Third time running: 5:30 MST
    - End of trading hours
    - Grabs any new FRED data that was updated later in the day

We could then make it update every weekday and not include weekends
