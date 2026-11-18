SELECT title
       ,code
       ,published_at
       ,text
       ,images
FROM news
WHERE code = :code;
