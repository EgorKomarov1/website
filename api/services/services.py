from fastapi import HTTPException

from api.repositories.repositories import get_news_repository, get_news_by_code_repository


def news_service(limit, page):
    return get_news_repository(limit, page)


def news_detail_service(code):
    news = get_news_by_code_repository(code)
    if news is None:
        raise HTTPException(status_code=404, detail='Новость не найдена')
    return news
