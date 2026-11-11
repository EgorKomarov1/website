from pydantic import BaseModel
from datetime import date


class news_schema(BaseModel):
    title: str
    published_at: date | None
    text: str
    images: list
    source_url: str
