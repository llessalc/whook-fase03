from os import getenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USER = getenv('DB_USER', 'webhook-api')
DB_PASSWORD = getenv('DB_PASSWORD', 'webhook-api')
DB_NAME = getenv('DB_NAME', 'webhook-api')
DB_HOST = getenv('DB_HOST', 'localhost')  # webhook-db
DB_PORT = getenv('DB_PORT', '33061')

CREATE_ENGINE_ECHO = getenv('CREATE_ENGINE_ECHO', True)

conn_string = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
engine = create_engine(conn_string)
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))

engine = create_engine(conn_string + f"/{DB_NAME}")

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from core.models import payments, orders
    Base.metadata.create_all(bind=engine)
