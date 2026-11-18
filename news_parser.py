import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from datetime import datetime
import json

from database.db import get_sql, engine

base_url = 'https://orel-gym19.obr57.ru'

news_paths = list()


for page in range(1, 32):
    news_records = []
    listing_response = requests.get(base_url + '/news/?page=' + str(page))
    listing_soup = bs(listing_response.text, 'html.parser')

    news_container = listing_soup.find('div', class_='news')
    news_items = news_container.find_all('div', class_='news__item')

    for news_item in news_items:
        news_link = news_item.find('a', class_='news__link')
        news_path = news_link['href']

        response = requests.get(base_url + news_path)
        article_soup = bs(response.text, 'html.parser')

        article_content = article_soup.find('div', class_='wysiwyg_content')

        if article_content is None:
            continue

        image_urls = [
            urljoin(response.url, image_tag["src"])
            for image_tag in article_content.select("img[src]")
            if image_tag["src"].strip()
        ]

        paragraph_texts = []

        for paragraph_tag in article_content.find_all('p'):
            paragraph_text = paragraph_tag.get_text(strip=True)
            if paragraph_text:
                paragraph_texts.append(paragraph_text)

        news_text = "\n\n".join(paragraph_texts)
        publication_date_tag = news_item.find("div", class_="news__date")

        news_records.append({
            "title": news_link.get_text(strip=True),
            "published_at": publication_date_tag.get_text(strip=True),
            "text": news_text,
            "images": image_urls,
            "source_url": response.url,
        })

    insert_news_query = get_sql('insert_news')

    news_rows = []
    for news_record in news_records:
        news_rows.append({
            'title': news_record['title'],
            'published_at': datetime.strptime(news_record['published_at'], '%d.%m.%Y').date(),
            'text': news_record['text'],
            'images': json.dumps(news_record['images'], ensure_ascii=False),
        })

    if news_rows:
        with engine.begin() as connection:
            insert_result = connection.execute(insert_news_query, news_rows)
