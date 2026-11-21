from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from api.services.services import news_detail_service


pages_router = APIRouter()
project_directory = Path(__file__).resolve().parents[2]


@pages_router.get('/', include_in_schema=False)
@pages_router.get('/index.html', include_in_schema=False)
def home_page():
    return FileResponse(project_directory / 'templates' / 'index.html')


def render_news_page(title, description, content, status_code=200):
    template = Template((project_directory / 'templates' / 'news.html').read_text(encoding='utf-8'))
    return HTMLResponse(template.substitute(
        page_title=escape(title),
        description=escape(description),
        content=content,
    ), status_code=status_code)


@pages_router.get('/news/{code}', response_class=HTMLResponse, include_in_schema=False)
def news_page(code: str):
    try:
        news = news_detail_service(UUID(code))
    except (ValueError, HTTPException) as error:
        if isinstance(error, HTTPException) and error.status_code != 404:
            raise
        return render_news_page(
            'Новость не найдена', 'Запрошенная новость не найдена.',
            '<h1>Новость не найдена</h1><p>Проверьте адрес или вернитесь к новостям на главной странице.</p>',
            status_code=404,
        )

    published_at = news['published_at']
    date_markup = (
        f'<time datetime="{published_at.isoformat()}">{published_at.strftime("%d.%m.%Y")}</time>'
        if published_at else ''
    )
    paragraphs = ''.join(
        f'<p>{escape(paragraph.strip())}</p>'
        for paragraph in news['text'].split('\n\n') if paragraph.strip()
    )
    images = ''.join(
        f'<img src="{escape(image_url)}" alt="" loading="lazy" />'
        for image_url in news['images']
        if isinstance(image_url, str) and urlsplit(image_url).scheme in ('http', 'https')
    )
    content = (
        f'<div class="article-meta"><span class="tag">Новости гимназии</span>{date_markup}</div>'
        f'<h1>{escape(news["title"])}</h1>'
        f'<div class="article-text">{paragraphs}</div>'
        f'<div class="article-gallery">{images}</div>'
    )
    return render_news_page(news['title'], ' '.join(news['text'].split())[:160], content)
