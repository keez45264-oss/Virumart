"""
One-time migration: copies data from local SQLite (grocery.db) into
the PostgreSQL database on Render.
Run: python migrate_data.py
"""
import sqlite3
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB = os.path.join('database', 'grocery.db')
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found. Check your .env file.")

sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_conn.row_factory = sqlite3.Row
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

# Clear existing data first so migration starts clean (safe since this is a one-time setup)
pg_cursor.execute("TRUNCATE order_items, orders, users, products RESTART IDENTITY CASCADE")
pg_conn.commit()
print("Cleared existing Postgres data before migration.")

TABLES_IN_ORDER = [
    ('products', ['product_id', 'name', 'category', 'cost_price', 'selling_price',
                  'quantity_in_stock', 'reorder_threshold', 'image_path']),
    ('users', ['user_id', 'name', 'email', 'phone', 'password_hash', 'created_at']),
    ('orders', ['order_id', 'user_id', 'customer_name', 'customer_phone',
                'delivery_address', 'order_status', 'order_date', 'total_amount']),
    ('order_items', ['order_item_id', 'order_id', 'product_id', 'quantity', 'price_at_order']),
]

for table_name, columns in TABLES_IN_ORDER:
    rows = sqlite_conn.execute(f'SELECT * FROM {table_name}').fetchall()
    if not rows:
        print(f"No rows in {table_name}, skipping.")
        continue

    col_list = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    insert_sql = f'INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})'

    count = 0
    for row in rows:
        values = tuple(row[col] for col in columns)
        pg_cursor.execute(insert_sql, values)
        count += 1

    print(f"Migrated {count} rows into {table_name}.")

# Reset auto-increment sequences so future inserts don't collide with migrated IDs
for table_name, columns in TABLES_IN_ORDER:
    id_column = columns[0]
    pg_cursor.execute(
        f"SELECT setval(pg_get_serial_sequence('{table_name}', '{id_column}'), "
        f"COALESCE((SELECT MAX({id_column}) FROM {table_name}), 1))"
    )

pg_conn.commit()
pg_cursor.close()
pg_conn.close()
sqlite_conn.close()

print("Migration complete.")