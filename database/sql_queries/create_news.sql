CREATE TABLE news(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
    ,title TEXT NOT NULL
    ,published_at DATE
    ,text TEXT NOT NULL
    ,images jsonb NOT NULL DEFAULT '[]'::jsonb
    ,source_url TEXT NOT NULL UNIQUE
);