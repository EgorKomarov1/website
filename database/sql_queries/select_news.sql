SELECT title
       ,published_at
       ,text
       ,images
       ,source_url
FROM news
ORDER BY published_at DESC NULLS LAST
LIMIT :limit OFFSET :offset;