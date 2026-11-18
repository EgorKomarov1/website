from html import escape
from uuid import UUID

from fastapi.testclient import TestClient

from api.main import app
from api.repositories.repositories import get_news_repository


def test_news_api():
    limit = 5
    page = 1
    with TestClient(app) as client:
        response = client.get('/api/news', params={'limit': limit, 'page': page})

    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) <= limit
    if result:
        item = result[0]
        assert 'code' in item
        assert 'title' in item
        assert 'published_at' in item
        assert 'text' in item
        assert 'images' in item


def test_news_detail_api():
    news = get_news_repository(1, 1)

    if news:
        code = news[0]['code']
        with TestClient(app) as client:
            response = client.get(f'/api/news/{code}')

        assert response.status_code == 200
        item = response.json()
        assert isinstance(item, dict)
        assert item['code'] == str(code)
        assert item['title'] == news[0]['title']
        assert item['text'] == news[0]['text']
        assert item['images'] == news[0]['images']


def test_news_page():
    news = get_news_repository(1, 1)

    if news:
        item = news[0]
        with TestClient(app) as client:
            response = client.get(f'/news/{item["code"]}')
            reloaded_response = client.get(f'/news/{item["code"]}')

        assert response.status_code == 200
        assert reloaded_response.status_code == 200
        assert reloaded_response.text == response.text
        assert 'text/html' in response.headers['content-type']
        assert f'<h1>{escape(item["title"])}</h1>' in response.text
        assert 'href="/css/news.css"' in response.text
        assert 'href="/#news"' in response.text
        for paragraph in item['text'].split('\n\n'):
            if paragraph.strip():
                assert f'<p>{escape(paragraph.strip())}</p>' in response.text


def test_missing_news_returns_404():
    code = UUID('00000000-0000-0000-0000-000000000000')
    with TestClient(app) as client:
        api_response = client.get(f'/api/news/{code}')
        page_response = client.get(f'/news/{code}')

    assert api_response.status_code == 404
    assert page_response.status_code == 404
    assert 'Новость не найдена' in api_response.text
    assert 'Новость не найдена' in page_response.text


def test_invalid_news_page_returns_404():
    with TestClient(app) as client:
        response = client.get('/news/invalid-code')

    assert response.status_code == 404


def test_home_and_assets_available():
    urls = ['/', '/index.html', '/css/styles.css', '/css/news.css', '/js/script.js']
    with TestClient(app) as client:
        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, url


def test_project_files_are_not_exposed():
    urls = ['/.env', '/config.py', '/database/db.py']
    with TestClient(app) as client:
        for url in urls:
            response = client.get(url)
            assert response.status_code == 404, url
