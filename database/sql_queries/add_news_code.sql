ALTER TABLE news
    ADD COLUMN IF NOT EXISTS code UUID NOT NULL DEFAULT gen_random_uuid();

CREATE UNIQUE INDEX IF NOT EXISTS news_code_key ON news (code);
