from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URL = (
    "postgresql://phisical_computing:STRONG_DB_PASSWORD@db:5432/phisical_computing?"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def db_session():
    return scoped_session(SessionLocal)
