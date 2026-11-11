from api.repositories.repositories import get_news_repository


def news_service(limit, page):
    return get_news_repository(limit, page)