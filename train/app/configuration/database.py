import logging

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from train.app.configuration.LoggingConfig import stream_handler, \
    file_handler

user = "db_user"
password = "db_pass!@#"
host = "127.0.0.1"
database = "db_name"
port = 9999

DATABASE_URL = sqlalchemy.engine.URL.create(
    drivername="mysql",
    username=user,
    password=password,
    host=host,
    port=port,
    database=database,
    )

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DATABASE_URL = "sqlite:///user.db"
# engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_recycle=500)
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def create_tables():
  Base.metadata.create_all(bind=engine)
  logger.debug("Tables created successfully")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()