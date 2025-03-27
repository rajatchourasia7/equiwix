import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Date, DateTime, Float, Integer, String, Text

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
    """
    Convert DataFrame columns to match SQLAlchemy query schema (handles joins).
    """
    type_map = {}

    # Extract column types from the query metadata
    for desc in query.column_descriptions:
        column = desc["expr"]
        col_name = column.key
        col_type = column.type

        if isinstance(col_type, (Date, DateTime, Text)):
            type_map[col_name] = "datetime"
        elif isinstance(col_type, Integer):
            type_map[col_name] = "integer"
        elif isinstance(col_type, Float):
            type_map[col_name] = "float"
        elif isinstance(col_type, String):
            type_map[col_name] = "string"

    data = pd.read_sql(query.statement, session.bind)

    # Apply transformations
    for col, dtype in type_map.items():
        if col in data:
            if dtype == "datetime":
                data[col] = pd.to_datetime(data[col])
            elif dtype == "integer":
                data[col] = pd.to_numeric(data[col], errors="coerce", downcast="integer")
            elif dtype == "float":
                data[col] = pd.to_numeric(data[col], errors="coerce", downcast="float")
            elif dtype == "string":
                data[col] = data[col].astype(str)

    return data
