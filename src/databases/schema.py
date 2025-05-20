from pydantic import BaseModel, ConfigDict
import datetime


class Themes(BaseModel):
    question: str
    tag: str
    ja: str


class ThemeResponse(Themes):  # レスポンス用モデル
    id: int
    created_at: datetime.datetime  # DBから取得した値を含む

    # Pydantic v2 の場合
    model_config = ConfigDict(from_attributes=True)
