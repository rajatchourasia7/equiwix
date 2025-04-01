"""
Module to compute index constituents and index levels using yfinance dataset
and sync to the respective tables.
"""

from sqlalchemy import desc
from sqlalchemy import func as F
from sqlalchemy import literal, select

from ..base_sync import SelectQuerySync
from ..db.tables import IndexConstituents, IndexLevel, YFinanceTickerData
from .constants import NUM_STOCKS_IN_INDEX
from .divisor import IndexLevelDivisorDAO


class YFinanceIndexConstituentsComputer(SelectQuerySync):
    """
    Compute the index constituents on a daily basis and sync to the index_consituents table.

    Note: Index for day X is computed based on market cap on day X - 1.
    """

    source = "yfinance"

    @property
    def table(self):
        return IndexConstituents

    def check_data_availability(self):
        raise NotImplementedError

    def get_select_query(self):
        src_tbl = YFinanceTickerData

        # This is designed in a generic manner to account for those datasets as well that have
        # OHLC at intervals granular than 1 day.
        # Pick the close value of the last interval of the day to rank tickers based on market cap.
        latest_per_day_data = (
            select(
                src_tbl.ticker,
                F.date(src_tbl.datetime_utc).label("date"),
                src_tbl.close,
                src_tbl.num_shares_outstanding,
                F.row_number()
                .over(
                    partition_by=(src_tbl.ticker, F.date(src_tbl.datetime_utc)),
                    order_by=desc(src_tbl.datetime_utc),
                )
                .label("recent_rank"),
            )
            .where(
                (F.date(src_tbl.datetime_utc) >= self.sync_start_date)
                & (F.date(src_tbl.datetime_utc) <= self.sync_end_date)
            )
            .cte("latest_per_day_data")
        )

        # Calculate market capitalization
        market_cap = latest_per_day_data.c.close * latest_per_day_data.c.num_shares_outstanding

        # Order and assign rank to rows based on descending market cap
        market_cap_rank = (
            F.row_number()
            .over(partition_by=latest_per_day_data.c.date, order_by=desc(market_cap))
            .label("market_cap_rank")
        )

        market_cap_rank_data = (
            select(
                latest_per_day_data.c.date,
                latest_per_day_data.c.ticker,
                market_cap_rank,
            )
            .where(latest_per_day_data.c.recent_rank == 1)
            .cte("market_cap_rank_data")
        )

        return select(
            F.date(market_cap_rank_data.c.date, "+1 day").label("date"),
            market_cap_rank_data.c.ticker,
            literal(self.source).label("source"),
        ).where(market_cap_rank_data.c.market_cap_rank <= NUM_STOCKS_IN_INDEX)


class YFinanceIndexLevelComputer(SelectQuerySync):
    """
    Compute the index level (OHLC).
    The table index_level supports storing levels for any interval and start time.
    YFinance supports computing levels only for 1-day intervals.
    """

    source = "yfinance"

    time_interval = "1day"

    @property
    def table(self):
        return IndexLevel

    def check_data_availability(self):
        raise NotImplementedError

    def get_select_query(self):
        price_src_tbl = YFinanceTickerData
        constituents_src_tbl = IndexConstituents

        # Join condition
        join_condition = [
            F.date(price_src_tbl.datetime_utc) == constituents_src_tbl.date,
            price_src_tbl.ticker == constituents_src_tbl.ticker,
        ]

        ticker_count = F.count(F.distinct(price_src_tbl.ticker))

        idx_divisor = IndexLevelDivisorDAO(source=self.source).get(self.sync_end_date)

        # Select statement
        stmt = (
            select(
                price_src_tbl.datetime_utc,
                literal(self.time_interval).label("time_interval"),
                *[
                    (F.sum(1 / getattr(price_src_tbl, level_type)) / idx_divisor).label(level_type)
                    for level_type in ('open', 'high', 'low', 'close')
                ],
                ticker_count.label("num_constituents"),
                literal(self.source).label("source"),
            )
            .where(
                *join_condition,
                F.date(price_src_tbl.datetime_utc) >= self.sync_start_date,
                F.date(price_src_tbl.datetime_utc) <= self.sync_end_date,
            )
            .group_by(price_src_tbl.datetime_utc)
        )

        return stmt
