from pydantic import BaseModel, ConfigDict
import datetime


class Question(BaseModel):
    question: str
    tag: str
    detail: str


class Score(BaseModel):
    score: int
    nickname: str
