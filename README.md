# Equiwix
## Overview
Equiwix is a dashboard that tracks and visualizes the performance of an equal-weighted index of the top 100 US stocks (by market capitalization). The index is updated daily based on market cap changes, ensuring equal notional contribution per stock.

## Features
- **Index Construction & Rebalancing**

  - Fetches the daily price data and number of outstansing shares data from yfinance dataset.
  - Tracks the top 100 US stocks based on daily closing market cap.
  - Ensures equal-weighted distribution, rebalancing at market close.
  - Stocks exiting the top 100 are replaced the next trading day.

More details to follow soon.
