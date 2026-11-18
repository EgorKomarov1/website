from pydantic import BaseModel
from datetime import date
from uuid import UUID


class news_schema(BaseModel):
    code: UUID
    title: str
    published_at: date | None
    text: str
    images: list
