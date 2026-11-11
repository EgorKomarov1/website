from sqlalchemy import create_engine, text
from config import database_url
from pathlib import Path


engine = create_engine(
    database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

sql_dir = Path(__file__).parent / 'sql_queries'


def get_sql(filename: str) -> text:
    filename = filename if filename.endswith('.sql') else f'{filename}.sql'
    sql_path = sql_dir / filename
    with open(sql_path, 'r') as sql_file:
        sql = sql_file.read()
    return text(sql)
