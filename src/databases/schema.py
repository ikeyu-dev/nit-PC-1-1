from pydantic import BaseModel


class Question(BaseModel):
    question: str
    tag: str
    detail: str
