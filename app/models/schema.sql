-- Grocery Store Management System — Database Schema
-- Run this once to set up database/grocery.db

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

CREATE TABLE IF NOT EXISTS orders (
    order_id        INTEGER PRIMARY KEY AUTOINCREMENT,
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
