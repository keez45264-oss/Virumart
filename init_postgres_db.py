"""
One-time setup: creates all tables in your PostgreSQL database.
Run: python init_postgres_db.py
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ.get('DATABASE_URL')
if not database_url:
    raise RuntimeError("DATABASE_URL not found. Check your .env file.")

with open('app/models/schema_postgres.sql', 'r') as f:
    schema_sql = f.read()

conn = psycopg2.connect(database_url)
cursor = conn.cursor()
cursor.execute(schema_sql)
conn.commit()
cursor.close()
conn.close()

print("PostgreSQL tables created successfully.")