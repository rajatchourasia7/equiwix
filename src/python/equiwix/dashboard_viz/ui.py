from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from .data_fetcher import DataFetcher
from .metrics import compute_index_metrics, detect_composition_changes

PRODUCTION_SOURCE = 'yfinance'


def render_header():
    st.title("📈 Equiwix")
    st.markdown(
        """
        Equiwix performance and composition changes.
    """
    )


def render_date_selector():
    today = datetime.today()
    default_start = today - timedelta(days=30)
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(default_start, today),
        min_value=today - timedelta(days=730),
        max_value=today,
    )
    return date_range


def load_data(start_date, end_date):
    data_fetcher = DataFetcher(source=PRODUCTION_SOURCE)

    index_df = data_fetcher.get_index_levels(start_date, end_date)
    constituents_df = data_fetcher.get_constituents(start_date, end_date)
    change_dates = detect_composition_changes(constituents_df)

    return index_df, constituents_df, change_dates


def add_composition_change_lines(fig, index_df, change_dates):
    for change_date in change_dates:
        change_date_dt = pd.to_datetime(change_date).to_pydatetime()

        fig.add_trace(
            go.Scatter(
                x=[change_date_dt, change_date_dt],
                y=[index_df["close"].min(), index_df["close"].max()],
                mode="lines",
                line=dict(color="red", dash="dash"),
            )
        )

        fig.add_annotation(
            x=change_date_dt,
            y=index_df["close"].max(),
            text="Change",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40,
            font=dict(color="red"),
        )


def render_performance_chart(index_df, change_dates):
    st.subheader("📊 Index Performance")
    import plotly.graph_objs as go

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=index_df.index,
            y=index_df["close"],
            mode="lines+markers",
            name="Close",
            line=dict(color="royalblue"),
        )
    )

    add_composition_change_lines(fig, index_df, change_dates)

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Index Close",
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_composition_view(constituents_df):
    st.subheader("🧩 Index Composition")
    selected_date = st.date_input(
        "Select Date to View Composition",
        value=constituents_df.index.max().date(),
        min_value=constituents_df.index.min().date(),
        max_value=constituents_df.index.max().date(),
    )

    try:
        tickers = constituents_df.loc[selected_date.strftime("%Y-%m-%d")]
        st.write(f"**Constituents on {selected_date}:**")
        st.write(tickers)
    except KeyError:
        st.warning(f"No composition data available for {selected_date}.")


def render_summary_metrics(index_df, change_dates):
    st.subheader("📌 Summary Metrics")

    index_metrics = compute_index_metrics(index_df)
    cum_returns = index_metrics['cumulative_return']
    pct_change = index_metrics['daily_pct_change']

    col1, col2, col3 = st.columns(3)

    col1.metric("Cumulative Return", f"{cum_returns.iloc[-1]:.2%}")
    col2.metric("Max Daily Change", f"{pct_change.max():.2%}")
    col3.metric("# of Composition Changes", len(change_dates))


def render_dashboard():
    render_header()

    date_range = render_date_selector()
    if not date_range or len(date_range) != 2:
        st.error("Please select a valid date range.")
        return

    start_date, end_date = date_range
    st.info(f"Fetching data from {start_date} to {end_date}")

    index_df, constituents_df, change_dates = load_data(start_date, end_date)

    if index_df.empty:
        st.warning("No index data available for selected date range.")
        return

    render_performance_chart(index_df, change_dates)
    render_composition_view(constituents_df)
    render_summary_metrics(index_df, change_dates)
