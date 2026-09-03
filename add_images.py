"""
Bulk-fetch free stock photos for all products missing an image, using
LoremFlickr (free, no API key needed - serves real tagged photos by keyword).
Run this once: python add_images.py
Safe to re-run - only fetches for products that don't already have an image.
"""
import sqlite3
import os
import urllib.request
import time

DB_PATH = os.path.join('database', 'grocery.db')
IMAGE_DIR = os.path.join('app', 'static', 'images', 'products')

CATEGORY_KEYWORDS = {
    'Grains': 'rice,grain',
    'Pulses': 'lentils,beans',
    'Cooking Oil': 'cooking-oil,bottle',
    'Dairy': 'milk,dairy',
    'Bakery': 'bread,bakery',
    'Essentials': 'spices,kitchen',
    'Snacks': 'snacks,chips',
    'Beverages': 'drink,bottle',
    'Vegetables': 'vegetables,fresh',
    'Fruits': 'fruit,fresh',
    'Personal Care': 'cosmetics,toiletries',
    'Cleaning': 'cleaning,detergent',
}

os.makedirs(IMAGE_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

products = conn.execute(
    "SELECT product_id, name, category FROM products WHERE image_path IS NULL"
).fetchall()

print(f"Found {len(products)} products without images.")

updated = 0
failed = 0

for p in products:
    keyword = CATEGORY_KEYWORDS.get(p['category'], 'grocery')
    filename = f"product_{p['product_id']}.jpg"
    filepath = os.path.join(IMAGE_DIR, filename)
    url = f"https://loremflickr.com/400/300/{keyword}"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())

        conn.execute(
            "UPDATE products SET image_path = ? WHERE product_id = ?",
            (filename, p['product_id'])
        )
        conn.commit()
        updated += 1
        print(f"  [{updated}] {p['name']} -> {filename}")
        time.sleep(0.3)

    except Exception as e:
        failed += 1
        print(f"  FAILED: {p['name']} ({e})")

conn.close()

print(f"\nDone. Updated {updated} products, {failed} failed.")
print("Restart your Flask server and refresh the home page to see the images.")