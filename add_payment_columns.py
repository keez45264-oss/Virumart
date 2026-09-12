"""
One-time migration: adds payment_method and payment_status columns to orders.
Run: python add_payment_columns.py
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cur = conn.cursor()

cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'cod'")
cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_status TEXT DEFAULT 'pending'")

conn.commit()
cur.close()
conn.close()

print("Added payment_method and payment_status columns.")