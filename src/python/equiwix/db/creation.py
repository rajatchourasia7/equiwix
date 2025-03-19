import sqlite3

from .tables import Base
from .util import get_db_path, get_engine


def create_db(db_path=None):
    """Create the sqlite DB if it doesn't exist."""
    if db_path is None:
        db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    conn.close()


def create_tables(db_uri=None):
    """Create all the tables defined in tables.py if they don't exist."""
    engine = get_engine(db_uri)
    Base.metadata.create_all(engine)


def create_db_and_tables():
    create_db()
    create_tables()
