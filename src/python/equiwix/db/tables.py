from typing import Optional

from sqlalchemy import REAL, CheckConstraint, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class IndexConstituents(Base):
    __tablename__ = 'index_constituents'

    date: Mapped[str] = mapped_column(Text, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)


class IndexLevel(Base):
    __tablename__ = 'index_level'

    datetime_utc: Mapped[str] = mapped_column(Text, primary_key=True)
    divisor: Mapped[float] = mapped_column(REAL)
    level: Mapped[Optional[float]] = mapped_column(REAL)


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
