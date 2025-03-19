from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from .util import get_engine


def get_session():
    """Return a session which can be used for read operations."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


@contextmanager
def atomic_session():
    """
    Execute multiple queries atomically by wrapping in this `atomic_session`.

    Example:
    with atomic_session() as session:
        ins_qry = insert(...).values(...)
        session.execute(ins_qry)
        upd_qry = update(...).values(...)
        session.execute(pd_qry)

    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
