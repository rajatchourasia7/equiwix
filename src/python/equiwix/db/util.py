import pandas as pd
from sqlalchemy import create_engine

from ..util import get_equiwix_home


def get_db_path():
    return f'{get_equiwix_home()}/equiwix.db'


def get_db_uri():
    return f'sqlite:///{get_db_path()}'


def get_engine(db_uri=None):
    """Return a sqlalchemy engine to be used while running queries or creating a session."""
    if db_uri is None:
        db_uri = get_db_uri()

    return create_engine(db_uri)


def fetch_query_results(session, query):
    """Fetch the query results in a pandas.DataFrame object and return."""
    return pd.read_sql(query.statement, session.bind)
