from database.db import engine, get_sql


def get_news_repository(limit: int = 50, page: int = 1):
    news_query = get_sql('select_news')

    offset = (page - 1) * limit

    with engine.begin() as conn:
        result = conn.execute(news_query, {'limit': limit, 'offset': offset})
    return result.mappings().all()


def get_news_by_code_repository(code):
    with engine.connect() as connection:
        result = connection.execute(get_sql('select_news_by_code'), {'code': code})
        return result.mappings().first()
