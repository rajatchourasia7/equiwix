# Equiwix
## Overview
Equiwix is a dashboard that tracks and visualizes the performance of an equal-weighted index of the top 100 US stocks (by market capitalization). The index is updated daily based on market cap changes, ensuring equal notional contribution per stock.

## Features
- **Index Construction & Rebalancing**
  - Fetches the daily price data and number of outstansing shares data from yfinance dataset.
  - Tracks the top 100 US stocks based on daily closing market cap and shares outstanding.
  - Ensures equal-weighted distribution, rebalancing at market close.
  - Stocks exiting the top 100 are replaced the next trading day.
- **Dashboard to visualize**
  - Change in index levels per day for the selected date-range with days marked where index constituents have changed.
  - Index constituents on the selected day.
  - Aggregated metrics (Cumulative return, max daily change, number of composition changes) for the selected date-range.

## Setup Instructions

  Follow these steps to set up and run the Equiwix project:

  ### 1. Clone the Repository
  ```bash
  git clone https://github.com/rajatchourasia7/equiwix.git
  cd equiwix
  ```

  ### 2. Install Dependencies
  Install the required Python dependencies using the following command:
  ```bash
  pip install -e .
  ```

  ### 3. Initialize the Database
  Run the following command to create the database and tables:
  ```bash
  equiwix-create_db_and_tables
  ```

  ### 4. Sync Ticker Universe
  Populate the database with the initial ticker universe (S&P500 source is the only option for now):
  ```bash
  equiwix-add_ticker_to_univ add-from-source sp500 --log-level INFO
  ```

  ### 5. Sync Market Data
  Fetch and store OHLC data and shares outstanding data from yfinance (replace the "run_date" below):
  ```bash
  equiwix-sync_yfinance_data <run_date> --action sync --mode historical --log-level INFO
  ```
  In "historical" mode, it syncs the data from EQUIWIX start of time (20230701) till the specified "run_date".

  ### 6. Update the Divisor
  Set the divisor value:
  ```bash
  equiwix-update_divisor --source yfinance --divisor 1 --start_date <run_date> --log-level INFO
  ```
  - Divisor represents the value by which all the index levels will be divided. It is used handle stock split type of cases.
  - Divisor can be updated later on. Set it to 1 for now.

  ### 7. Compute Index Constituents
  Calculate the index constituents based on the latest data:
  ```bash
  equiwix-sync_yfinance_data <run_date> --action compute_constituents --mode historical --log-level INFO
  ```

  ### 8. Compute Index Levels
  Generate the index levels for each day:
  ```bash
  equiwix-sync_yfinance_data <run_date> --action compute_levels --mode historical --log-level INFO
  ```

  ### 9. Launch the Dashboard
  Start the Equiwix dashboard to visualize the index performance:
  ```bash
  equiwix-launch_dashboard
  ```
  This will launch the dashboard locally and provide a link. Copy-paste that link in the browser.

  You are now ready to use Equiwix to track and visualize the performance of the equal-weighted index!
