import logging

from sqlalchemy import func as F
from sqlalchemy import insert, update

from equiwix.db import atomic_session, fetch_query_results, get_session
from equiwix.db.tables import IndexLevel, IndexLevelDivisor

from ..util import EQUIWIX_END_OF_TIME, EQUIWIX_OPENING_LEVEL, Date
from .selectors import IndexLevelDateSelector


class IndexLevelDivisorDAO:
    def __init__(self, source):
        self.source = source

    @property
    def table(self):
        return IndexLevelDivisor

    def set(self, divisor, start_date):
        start_date = Date(start_date)

        upd_qry = (
            update(self.table)
            .where(
                self.table.knowledge_end_date == str(EQUIWIX_END_OF_TIME),
                self.table.source == self.source,
            )
            .values(knowledge_end_date=str(start_date))
        )

        ins_qry = insert(self.table).values(
            source=self.source,
            knowledge_start_date=str(start_date),
            knowledge_end_date=str(EQUIWIX_END_OF_TIME),
            divisor=divisor,
        )

        with atomic_session() as session:
            session.execute(upd_qry)
            session.execute(ins_qry)

        logging.info(f'Divisor data synced into {self.table.__tablename__} for {start_date}')

    def set_as_first_date_open(self, start_date):
        selector = IndexLevelDateSelector(source=self.source)
        first_date_open = selector.select(date=selector.first_date).open.iloc[0]
        self.set(first_date_open / EQUIWIX_OPENING_LEVEL, start_date)

    def get(self, date=None):
        date = Date.today() if date is None else Date(date)

        session = get_session()
        qry = session.query(self.table.divisor).where(
            self.table.source == self.source,
            self.table.knowledge_start_date <= str(date),
            self.table.knowledge_end_date > str(date),
        )
        res = fetch_query_results(session, qry)
        session.close()

        if len(res) > 1:
            raise ValueError(f'Got {len(res)} rows for {date} from {self.table.__tablename__}.')

        return res.divisor.iloc[0]

    def normalize_levels(self, divisor_as_of_date, start_date=None, end_date=None):
        divisor = self.get(divisor_as_of_date)

        tbl = IndexLevel
        upd_qry = (
            update(tbl)
            .values(
                **{
                    level_type: getattr(tbl, level_type) / divisor
                    for level_type in ['open', 'high', 'low', 'close']
                }
            )
            .where(tbl.source == self.source)
        )

        if start_date is not None:
            upd_qry = upd_qry.where(F.date(tbl.datetime_utc) >= start_date)
        if end_date is not None:
            upd_qry = upd_qry.where(F.date(tbl.datetime_utc) <= end_date)

        with atomic_session() as session:
            session.execute(upd_qry)
