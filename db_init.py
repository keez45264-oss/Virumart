"""
Grocery Store Management System — Database Schema Setup
Run this once (or after schema changes) to set up database/grocery.db
"""
import sqlite3
import os

DB_PATH = os.path.join('database', 'grocery.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    product_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    category        TEXT,
    cost_price      REAL NOT NULL,
    selling_price   REAL NOT NULL,
    quantity_in_stock INTEGER NOT NULL DEFAULT 0,
    reorder_threshold INTEGER DEFAULT 5,
    image_path      TEXT
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    contact         TEXT
);

CREATE TABLE IF NOT EXISTS purchases (
    purchase_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id     INTEGER REFERENCES suppliers(supplier_id),
    product_id      INTEGER REFERENCES products(product_id),
    quantity        INTEGER NOT NULL,
    purchase_date   TEXT NOT NULL,
    cost            REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER REFERENCES products(product_id),
    quantity_sold   INTEGER NOT NULL,
    sale_date       TEXT NOT NULL,
    total_amount    REAL NOT NULL,
    source          TEXT CHECK(source IN ('in-store', 'online')) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    phone           TEXT,
    password_hash   TEXT NOT NULL,
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER REFERENCES users(user_id),
    customer_name   TEXT NOT NULL,
    customer_phone  TEXT NOT NULL,
    delivery_address TEXT NOT NULL,
    order_status    TEXT CHECK(order_status IN ('pending','confirmed','delivered')) DEFAULT 'pending',
    order_date      TEXT NOT NULL,
    total_amount    REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER REFERENCES orders(order_id),
    product_id      INTEGER REFERENCES products(product_id),
    quantity        INTEGER NOT NULL,
    price_at_order  REAL NOT NULL
);
"""

SAMPLE_PRODUCTS = [
    ('Basmati Rice 5kg', 'Grains', 350.0, 420.0, 25, 5, None),
    ('Toor Dal 1kg', 'Pulses', 110.0, 140.0, 40, 10, None),
    ('Sunflower Oil 1L', 'Cooking Oil', 130.0, 160.0, 30, 5, None),
    ('Amul Milk 500ml', 'Dairy', 25.0, 30.0, 60, 15, None),
    ('Tata Salt 1kg', 'Essentials', 18.0, 25.0, 100, 20, None),
]

os.makedirs('database', exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.executescript(SCHEMA)

count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
if count == 0:
    conn.executemany(
        '''INSERT INTO products
           (name, category, cost_price, selling_price, quantity_in_stock, reorder_threshold, image_path)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        SAMPLE_PRODUCTS
    )
    print(f"Seeded {len(SAMPLE_PRODUCTS)} sample products.")

conn.commit()
conn.close()

print(f"Database created/updated at {DB_PATH}")
print("Done! Run 'python run.py' to see it in action.")