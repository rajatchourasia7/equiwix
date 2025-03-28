# Index Performance & Composition Dashboard
## Objective
- To build an interactive, user-friendly dashboard in Jupyter Notebook using Streamlit + Plotly, which visualizes:
- Index performance over a selected date range
- Composition of the index on a specific day
- Composition change events over time
- Summary metrics like cumulative returns, daily percentage changes, and the number of composition changes

## Dashboard features
- Date Range Selector
  - User can select any custom date range interactively.

- Performance Line Chart
  - Plot Close Price over selected date range.
  - On hover: show date, close price, daily % change, cumulative return.

- Composition Table
  - Display the list of tickers on the selected date.

- Composition Change Highlights
  - Identify & highlight dates where composition changed (addition/removal).
  - Optionally mark these dates on the line chart with a special marker.

- Summary Metrics
  - Cumulative returns over selected date range.
  - Daily % changes.
  - Number of composition change events in selected date range.


## Data Layer
Reuse existing IndexConstituentsDateSelector & IndexLevelDateSelector classes to fetch data.

## Processing Layer
- compute_index_metrics: Computes the index daily percent change and cumulative returns.
- detect_composition_changes: Finds and returns the dates on which composition changes.

## Visualization Layer
Streamlit App Components:
- Date Range Selector
- Performance Line Chart (Plotly)
- Composition Table (Streamlit)
- Composition Change Highlights (markers on line chart)
- Summary Metrics Display