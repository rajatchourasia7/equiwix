"""
Module for selecting index constituent and index level data.

This module provides classes to query equiwix index data efficiently while handling various date
formats and ensuring valid date conversions. It includes:
- `IndexConstituentsDateSelector`: Retrieves index composition for a given date or date range.
- `IndexLevelDateSelector`: Retrieves index daily OHLC for a given date or date-range, ensuring
                            correct timezone conversion.

Key Features:
- Supports multiple input formats for dates (integers, strings, ranges, pandas Series).
- Ensures valid trading days using the NYSE calendar.
- Filters data based on source validation.
- Handles missing data by returning `None` when no records match.

"""

from abc import ABC, abstractmethod
from datetime import date, datetime

import pandas as pd
import pandas_market_calendars as mcal
from sqlalchemy.orm import Session

from ..db import fetch_query_results, get_session
from ..db.tables import IndexConstituents, IndexLevel
from .constants import VALID_SOURCES


def standardize_date_arg(fn):
    """Decorator to standardize the date argument into a pandas Series of trading dates."""

    def wrapper(self, date=None):
        if date is None:
            new_date = None  # No filtering

        elif isinstance(date, int):
            new_date = pd.Series([pd.to_datetime(str(date), format='%Y%m%d').date()])

        elif isinstance(date, str):
            if ':' in date:  # Range case "YYYY-MM-DD:YYYY-MM-DD"
                start_date, end_date = date.split(':')
                start_date = pd.to_datetime(start_date).date()
                end_date = pd.to_datetime(end_date).date()
                # Get the NYSE calendar
                nyse = mcal.get_calendar('NYSE')
                new_date = pd.Series(nyse.valid_days(start_date, end_date).date)
            else:  # Single date
                new_date = pd.Series([pd.to_datetime(date).date()])

        elif isinstance(date, pd.Series):
            new_date = date.dt.date

        elif isinstance(date, date):
            new_date = pd.Series([date])

        else:
            raise ValueError("Invalid date format")

        return fn(self, new_date)

    return wrapper


class BaseSelector(ABC):
    """Base class for common selector functionality."""

    def __init__(self, source):
        if source not in VALID_SOURCES:
            raise ValueError(f"Invalid source: {source}")
        self.source = source

    @property
    @abstractmethod
    def time_interval(self):
        pass

    @abstractmethod
    def select(self):
        pass


class BaseDateSelector(BaseSelector):
    """Base class for common date based selector functionality."""

    @property
    def time_interval(self):
        return '1day'

    @abstractmethod
    def select(self, date=None):
        pass


class IndexConstituentsDateSelector(BaseDateSelector):
    """Selector for index constituents based on date."""

    @standardize_date_arg
    def select(self, date=None):
        """Fetch tickers for the given date(s)."""
        tbl = IndexConstituents
        session = get_session()

        qry = session.query(tbl.date, tbl.ticker).filter(tbl.source == self.source)
        if date is not None:
            qry = qry.filter(tbl.date.in_(date.tolist()))

        df = fetch_query_results(session, qry)
        session.close()

        return df.groupby("date")["ticker"].apply(list).reset_index()


class IndexLevelDateSelector(BaseDateSelector):
    """Selector for index levels on a daily basis, converting UTC to NY time and filtering."""

    @standardize_date_arg
    def select(self, date=None):
        """Fetch index levels for the given date(s)."""
        tbl = IndexLevel
        session = get_session()

        qry = session.query(
            tbl.datetime_utc, tbl.open, tbl.high, tbl.low, tbl.close, tbl.num_constituents
        ).filter(tbl.source == self.source, tbl.time_interval == self.time_interval)

        if date is not None:
            qry = qry.filter(tbl.datetime_utc.between(date.min(), date.max()))

        df = fetch_query_results(session, qry)
        session.close()

        # Convert datetime_utc to New York timezone and extract the latest timestamp per date
        df["datetime_utc"] = pd.to_datetime(df["datetime_utc"])
        df["datetime_ny"] = (
            df["datetime_utc"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")
        )
        df["date"] = df["datetime_ny"].dt.date

        df = df.sort_values("datetime_ny").drop_duplicates("date", keep="last")
        return df.set_index("date").drop(columns=["datetime_utc", "datetime_ny"])
