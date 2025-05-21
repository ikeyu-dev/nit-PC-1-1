from pydantic import BaseModel, ConfigDict
import datetime


class Question(BaseModel):
    question: str
    tag: str
    ja: str


class ThemeResponse(Question):  # レスポンス用モデル
    id: int
    created_at: datetime.datetime  # DBから取得した値を含む

    # Pydantic v2 の場合
    model_config = ConfigDict(from_attributes=True)
