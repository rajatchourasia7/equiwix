from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

from ..util import Date
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
        min_value=Date(19000101),
        max_value=Date(21991231),
    )
    return date_range


def load_data(start_date, end_date):
    data_fetcher = DataFetcher(source=PRODUCTION_SOURCE)

    index_df = data_fetcher.get_index_levels(start_date, end_date)
    constituents_df = data_fetcher.get_constituents(start_date, end_date)
    change_dates = detect_composition_changes(constituents_df)

    return index_df, constituents_df, change_dates


def render_performance_chart(index_df, change_dates):
    st.subheader("📊 Index Performance")

    # Create the line chart representing the index levels
    fig = px.line(index_df['close'], title='Index levels')

    # Customize hover information
    fig.update_traces(mode='lines', hovertemplate='Date: %{x}<br>Close: %{y:.2f}<extra></extra>')

    fig.update_layout(xaxis_title='Date', yaxis_title='Close')

    # Add vertical lines for composition changes
    # compute a constant y-position just below the data
    ymin, ymax = index_df['close'].min(), index_df['close'].max()
    baseline = ymin - (ymax - ymin) * 0.02

    fig.add_trace(
        go.Scatter(
            x=change_dates,
            y=[baseline] * len(change_dates),
            mode='markers',
            marker=dict(
                symbol='line-ns-open',  # vertical tick
                size=8,  # very small
                color='grey',
                line_width=1,
            ),
            hovertemplate='Date: %{x|%Y-%m-%d}<extra></extra>',
            name='Composition change',
        )
    )

    # Show the plot in Streamlit
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
        st.write(f"**Constituents on {selected_date}:**")

        tickers = constituents_df.loc[selected_date.strftime("%Y-%m-%d")]
        tickers_html = f"""
                <div style="
                    border: 2px solid royalblue;
                    padding: 10px;
                    border-radius: 10px;
                    background-color: #f0f0f0;
                    font-family: Arial;
                ">
                    {', '.join(tickers)}
                </div>
            """
        st.markdown(tickers_html, unsafe_allow_html=True)

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
