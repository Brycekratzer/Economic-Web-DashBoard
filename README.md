# Economic Dashboard

Economic dashboard is a project that will potentially allow for users to view a website that has a data driven insight on the
overall economic state of the United States using FRED and yfinance data

## Updates 

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


## File Structure

TODO