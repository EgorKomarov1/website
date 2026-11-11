import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from datetime import datetime
import json

from database.db import get_sql, engine

url = 'https://orel-gym19.obr57.ru'

href_list = list()
news_list = list()


for page in range(1, 32):
    response = requests.get(url + '/news/?page=' + str(page))
    soup = bs(response.text, 'html.parser')

    news_container = soup.find('div', class_='news')
    news = news_container.find_all('div', class_='news__item')

    for new in news:
        a = new.find('a', class_='news__link')
        href = a['href']

        q = requests.get(url + href)
        s = bs(q.text, 'html.parser')

        all_new = s.find('div', class_='wysiwyg_content')

        if all_new is None:
            continue

        images = [
            urljoin(q.url, img["src"])
            for img in all_new.select("img[src]")
            if img["src"].strip()
        ]

        paragraphs = []

        for p in all_new.find_all('p'):
            text = p.get_text(strip=True)
            if text:
                paragraphs.append(text)

        news_text = "\n\n".join(paragraphs)
        date = new.find("div", class_="news__date")

        news_list.append({
            "title": a.get_text(strip=True),
            "published_at": date.get_text(strip=True),
            "text": news_text,
            "images": images,
            "source_url": q.url,
        })

    query = get_sql('insert_news')

    rows = []
    for item in news_list:
        rows.append({
            'title': item['title'],
            'published_at': datetime.strptime(item['published_at'], '%d.%m.%Y').date(),
            'text': item['text'],
            'images': json.dumps(item['images'], ensure_ascii=False),
            'source_url': item['source_url']
        })

    with engine.begin() as conn:
        result = conn.execute(query, rows)
