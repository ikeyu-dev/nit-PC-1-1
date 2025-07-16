from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True, index=True)
    tag = Column(String, unique=True, index=True)
    detail = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now())


class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    score = Column(Integer, index=True)
    nickname = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now())
