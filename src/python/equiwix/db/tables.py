from typing import Optional

from sqlalchemy import REAL, CheckConstraint, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class IndexConstituents(Base):
    __tablename__ = 'index_constituents'

    date: Mapped[str] = mapped_column(Text, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)
    source: Mapped[str] = mapped_column(String(20), primary_key=True)


class IndexLevel(Base):
    __tablename__ = 'index_level'

    datetime_utc: Mapped[str] = mapped_column(Text, primary_key=True)
    time_interval: Mapped[str] = mapped_column(String(10), primary_key=True)
    open: Mapped[Optional[float]] = mapped_column(REAL)
    high: Mapped[Optional[float]] = mapped_column(REAL)
    low: Mapped[Optional[float]] = mapped_column(REAL)
    close: Mapped[Optional[float]] = mapped_column(REAL)
    num_constituents: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(20), primary_key=True)


class IndexLevelDivisor(Base):
    __tablename__ = 'index_level_divisor'

    source: Mapped[str] = mapped_column(String(20), primary_key=True)
    knowledge_start_date: Mapped[str] = mapped_column(Text, primary_key=True)
    knowledge_end_date: Mapped[str] = mapped_column(Text)
    divisor: Mapped[Optional[float]] = mapped_column(REAL)


class YFinanceTickerData(Base):
    __tablename__ = 'yfinance_ticker_data'

    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)
    datetime_utc: Mapped[str] = mapped_column(Text, primary_key=True)
    open: Mapped[Optional[float]] = mapped_column(REAL)
    high: Mapped[Optional[float]] = mapped_column(REAL)
    low: Mapped[Optional[float]] = mapped_column(REAL)
    close: Mapped[Optional[float]] = mapped_column(REAL)
    num_shares_outstanding: Mapped[int] = mapped_column(Integer)


class TickerUniverse(Base):
    __tablename__ = 'ticker_universe'

    univ: Mapped[str] = mapped_column(String(20), primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)
