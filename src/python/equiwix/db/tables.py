from typing import Optional

from sqlalchemy import CheckConstraint, Integer, REAL, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class IndexConstituents(Base):
    __tablename__ = 'index_constituents'

    date: Mapped[str] = mapped_column(Text, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)


class IndexLevel(Base):
    __tablename__ = 'index_level'

    utc_timestamp: Mapped[str] = mapped_column(Text, primary_key=True)
    divisor: Mapped[float] = mapped_column(REAL)
    level: Mapped[Optional[float]] = mapped_column(REAL)


class YFinanceSharesOutstanding(Base):
    __tablename__ = 'yfinance_shares_outstanding'
    __table_args__ = (
        CheckConstraint('date(date) IS NOT NULL'),
    )

    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)
    date: Mapped[str] = mapped_column(Text, primary_key=True)
    num_shares: Mapped[int] = mapped_column(Integer)


class YFinanceTickerPrice(Base):
    __tablename__ = 'yfinance_ticker_price'

    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)
    knowledge_start_utc: Mapped[str] = mapped_column(Text, primary_key=True)
    knowledge_end_utc: Mapped[str] = mapped_column(Text)
    open: Mapped[Optional[float]] = mapped_column(REAL)
    high: Mapped[Optional[float]] = mapped_column(REAL)
    low: Mapped[Optional[float]] = mapped_column(REAL)
    close: Mapped[Optional[float]] = mapped_column(REAL)
    adj_close: Mapped[Optional[float]] = mapped_column(REAL)


class TickerUniverse(Base):
    __tablename__ = 'ticker_universe'

    ticker: Mapped[str] = mapped_column(String(20), primary_key=True)
