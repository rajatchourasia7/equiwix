import logging
from datetime import timedelta

import pandas as pd
import yfinance as yf

from ..base_sync import DataSync
from ..db.tables import YFinanceTickerData
from ..ticker_univ import TickerUniv


class YFinanceDataSync(DataSync):
    @property
    def table(self):
        return YFinanceTickerData

    def get_data_to_sync(self):
        tickers = TickerUniv().get_tickers(all_univ=True)
        all_data = []

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)

                # yfinance expects end_date to be the last queried date + 1
                end_date = self.sync_end_date + timedelta(days=1)

                # Get historical prices
                hist = stock.history(start=self.sync_start_date, end=end_date, back_adjust=True)

                if hist.empty:
                    continue

                data = hist[['Open', 'High', 'Low', 'Close']].reset_index()
                data['datetime_utc'] = (
                    data['Date'].dt.tz_convert('UTC').dt.strftime('%Y-%m-%d %H:%M:%S')
                )
                data = data[['datetime_utc', 'Open', 'High', 'Low', 'Close']]
                data = data.rename(
                    columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}
                )

                # Get shares outstanding
                data['num_shares_outstanding'] = stock.info.get('sharesOutstanding', None)

                data['ticker'] = ticker
                all_data.append(data)

            except Exception as e:
                logging.error(f"Error fetching {ticker}: {str(e)}")
                continue

        return pd.concat(all_data, ignore_index=True)
