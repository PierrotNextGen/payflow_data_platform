import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "payflow",
    "user": "payflow",
    "password": "postgres"
}


def get_connection():
    return psycopg.connect(
        **DB_CONFIG,
        row_factory=dict_row
    )