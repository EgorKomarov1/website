from uuid import UUID

from api.repositories.repositories import get_news_repository, get_news_by_code_repository


def test_news_repository():
    limit = 5
    page = 1
    result = get_news_repository(limit, page)

    assert isinstance(result, list)
    assert len(result) <= limit
    if result:
        item = result[0]
        assert 'code' in item
        assert 'title' in item
        assert 'published_at' in item
        assert 'text' in item
        assert 'images' in item
        assert isinstance(item['code'], UUID)
        assert isinstance(item['title'], str)
        assert isinstance(item['text'], str)
        assert isinstance(item['images'], list)


def test_news_repository_pagination():
    limit = 5
    first_page = get_news_repository(limit, 1)
    second_page = get_news_repository(limit, 2)
    combined = get_news_repository(limit * 2, 1)

    assert isinstance(second_page, list)
    assert len(second_page) <= limit
    assert first_page + second_page == combined
    first_page_codes = {item['code'] for item in first_page}
    second_page_codes = {item['code'] for item in second_page}
    assert first_page_codes.isdisjoint(second_page_codes)


def test_news_by_code_repository():
    news = get_news_repository(1, 1)

    if news:
        code = news[0]['code']
        result = get_news_by_code_repository(code)

        assert result is not None
        assert 'code' in result
        assert 'title' in result
        assert 'published_at' in result
        assert 'text' in result
        assert 'images' in result
        assert result['code'] == code
        assert dict(result) == dict(news[0])


def test_news_by_code_repository_not_found():
    code = UUID('00000000-0000-0000-0000-000000000000')
    result = get_news_by_code_repository(code)

    assert result is None
