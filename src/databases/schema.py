from pydantic import BaseModel


class Question(BaseModel):
    question: str
    tag: str
    detail: str


class Score(BaseModel):
    score: int
    nickname: str
