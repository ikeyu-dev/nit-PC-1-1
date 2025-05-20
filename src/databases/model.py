from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class theme(Base):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True, index=True)
    tag = Column(String, unique=True, index=True)
    ja = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
