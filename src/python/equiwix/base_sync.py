import logging
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import insert

from .db import atomic_session


class BaseSync(ABC):
    def __init__(self, run_date, sync_start_date=None):
        """
        Base class for performing sync to a table.

        :param run_date: Date for/till which data should be synced.
        :param sync_start_date: Date from which data should be synced.
            If None, sync data only for `run_date`.
        """
        if sync_start_date is None:
            sync_start_date = run_date

        self.sync_start_date = datetime.strptime(sync_start_date, '%Y%m%d').date()
        self.sync_end_date = datetime.strptime(run_date, '%Y%m%d').date()

        if self.sync_start_date > self.sync_end_date:
            raise ValueError(f'sync_start_date should be <= run_date.')

    @property
    @abstractmethod
    def table(self):
        pass

    @abstractmethod
    def check_data_availability(self):
        pass

    @abstractmethod
    def sync(self):
        pass


class DataFrameSync(BaseSync):
    @abstractmethod
    def get_data_to_sync(self):
        pass

    def check_data_availability(self):
        data = self.get_data_to_sync()
        if len(data) == 0:
            raise ValueError('Data not available to sync')
        return True

    def sync(self):
        data = self.get_data_to_sync()
        data_dict = data.to_dict(orient='records')

        with atomic_session() as session:
            session.execute(insert(self.table), data_dict)

        logging.info(
            f'Data synced into {self.table.__tablename__} for '
            f'{self.sync_start_date}:{self.sync_end_date}'
        )


class SelectQuerySync(BaseSync):
    @abstractmethod
    def get_select_query(self):
        pass

    def sync(self):
        insert_qry = insert(self.table).from_select(
            [c.name for c in self.table.__table__.columns], self.get_select_query()
        )
        with atomic_session() as session:
            session.execute(insert_qry)

        logging.info(
            f'Data synced into {self.table.__tablename__} for '
            f'{self.sync_start_date}:{self.sync_end_date}'
        )
