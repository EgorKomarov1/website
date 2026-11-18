CREATE TABLE news(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
    ,code UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE
    ,title TEXT NOT NULL
    ,published_at DATE
    ,text TEXT NOT NULL
    ,images jsonb NOT NULL DEFAULT '[]'::jsonb
);
