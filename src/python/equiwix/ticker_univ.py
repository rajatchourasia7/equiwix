import logging

import pandas as pd
from sqlalchemy import insert

from .db import atomic_session, fetch_query_results, get_session
from .db.tables import TickerUniverse


class TickerUniv:
    univ = 'manual'

    @property
    def table(self):
        return TickerUniverse

    def add(self, ticker):
        data_dict = [{'univ': self.univ, 'ticker': ticker}]
        with atomic_session() as session:
            session.execute(insert(self.table), data_dict)

        logging.info(f'Added {ticker} to the {self.univ} universe.')

    def get_tickers(self, all_univ=False):
        session = get_session()
        qry = session.query(self.table.ticker)
        if not all_univ:
            qry = qry.where(self.table.univ == self.univ)

        data = fetch_query_results(session, qry)
        return data['ticker'].unique()


class SP500TickerUniv(TickerUniv):
    univ = 'sp500'

    def get_tickers_to_sync(self):
        """Fetch current S&P 500 constituents from Wikipedia"""
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        html = pd.read_html(url)
        df = html[0]
        return df['Symbol'].tolist()

    def add(self):
        tickers = self.get_tickers_to_sync()

        data_dict = [{'univ': self.univ, 'ticker': ticker} for ticker in tickers]
        with atomic_session() as session:
            session.execute(insert(self.table), data_dict)

        logging.info(f'Added {len(tickers)} to the {self.univ} universe.')
