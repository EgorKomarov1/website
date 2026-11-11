from pydantic import BaseModel


class news_schema(BaseModel):
    title: str
    published_at: str | None
    text: str
    images: list
    source_url: str
