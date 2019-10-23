from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
engine = None

db_session = scoped_session(sessionmaker(bind=engine, autocommit=False))


def init_engine(uri, **kwargs):
    global engine
    engine = create_engine(uri, **kwargs)
    return engine


Base = declarative_base()
Base.query = db_session.query_property()

from contextlib import contextmanager


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from app.core.models.activity_log import ActivityLog
    from app.core.models.permission import Permission
    from app.core.models.role import Role
    from app.core.models.role_permission import RolePermission
    from app.core.models.user import User
    from app.core.models.user_permission import UserPermission
    from app.core.models.user_role import UserRole
    db_session.configure(bind=engine)  # reconfigure the :class:`.sessionmaker` used by this :class:`.scoped_session`
    Base.metadata.create_all(bind=engine)
