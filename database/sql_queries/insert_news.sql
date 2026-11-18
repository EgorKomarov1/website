WITH incoming_news AS (
    SELECT CAST(:title AS TEXT) AS title
          ,CAST(:published_at AS DATE) AS published_at
          ,CAST(:text AS TEXT) AS text
          ,CAST(:images AS JSONB) AS images
)
INSERT INTO news (title, published_at, text, images)
SELECT incoming.title, incoming.published_at, incoming.text, incoming.images
FROM incoming_news AS incoming
WHERE NOT EXISTS (
    SELECT 1
    FROM news AS existing
    WHERE existing.title = incoming.title
      AND existing.published_at IS NOT DISTINCT FROM incoming.published_at
      AND existing.text = incoming.text
      AND existing.images = incoming.images
)
ON CONFLICT DO NOTHING;
