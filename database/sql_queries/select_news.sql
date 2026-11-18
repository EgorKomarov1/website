SELECT title
       ,code
       ,published_at
       ,text
       ,images
FROM news
ORDER BY published_at DESC NULLS LAST, id DESC
LIMIT :limit OFFSET :offset;
