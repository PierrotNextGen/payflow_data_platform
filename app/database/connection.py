import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "payflow",
    "user": "postgres",
    "password": "Munga@2001"
}


def get_connection():
    return psycopg.connect(
        **DB_CONFIG,
        row_factory=dict_row
    )