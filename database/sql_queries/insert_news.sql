INSERT INTO news
    (title, published_at, text, images, source_url)
VALUES
    (:title, :published_at, :text, :images, :source_url)
ON CONFLICT DO NOTHING;