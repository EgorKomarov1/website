SELECT title
       ,published_at
       ,text
       ,images
       ,source_url
FROM news
ORDER BY :limit OFFSET :offset;