"""
Shared PostgreSQL connection helper.
Wraps psycopg2 so existing code (conn.execute(...).fetchall()) keeps working
almost unchanged, with dict-style row access like sqlite3.Row.
"""
import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


class DBConnection:
    def __init__(self, raw_conn):
        self._conn = raw_conn

    def execute(self, sql, params=None):
        cursor = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql, params or [])
        return cursor

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set. Check your .env file.")
    raw_conn = psycopg2.connect(database_url)
    return DBConnection(raw_conn)