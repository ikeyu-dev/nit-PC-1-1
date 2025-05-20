from sqlalchemy import create_engine
from databases.model import theme


DATABASE_URL = (
    "postgresql://phisical_computing:STRONG_DB_PASSWORD@db:5432/phisical_computing?"
)
engine = create_engine(DATABASE_URL)
theme.metadata.create_all(bind=engine)
