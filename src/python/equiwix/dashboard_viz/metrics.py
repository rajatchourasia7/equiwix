import pandas as pd


def compute_index_metrics(df):
    df = df.copy()
    df["daily_pct_change"] = df["close"].pct_change()
    df["cumulative_return"] = (1 + df["daily_pct_change"]).cumprod() - 1
    return df


def detect_composition_changes(constituents_series):
    change_dates = []
    prev = None
    for date, tickers in constituents_series.items():
        if prev is not None and set(tickers) != set(prev):
            change_dates.append(date)
        prev = tickers
    return change_dates
