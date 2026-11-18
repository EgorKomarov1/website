from database.db import engine, get_sql


def migrate():
    with engine.begin() as connection:
        connection.execute(get_sql('add_news_code'))


if __name__ == '__main__':
    migrate()
