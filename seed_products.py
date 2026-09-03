"""
Seed script: adds ~100 common grocery products to Virumart's database.
Run this once: python seed_products.py
Safe to re-run - skips products that already exist (matched by name).
"""
import sqlite3
import os

DB_PATH = os.path.join('database', 'grocery.db')

PRODUCTS = [
    # Grains & Rice
    ("Basmati Rice 5kg", "Grains", 350, 420, 30, 5),
    ("Sona Masoori Rice 5kg", "Grains", 280, 340, 30, 5),
    ("Brown Rice 1kg", "Grains", 90, 120, 25, 5),
    ("Wheat Flour (Atta) 5kg", "Grains", 200, 250, 40, 8),
    ("Poha (Flattened Rice) 500g", "Grains", 35, 50, 30, 5),
    ("Semolina (Rava/Suji) 1kg", "Grains", 45, 60, 25, 5),
    ("Vermicelli 500g", "Grains", 30, 45, 20, 5),
    ("Maida (Refined Flour) 1kg", "Grains", 40, 55, 25, 5),
    ("Besan (Gram Flour) 1kg", "Grains", 75, 95, 25, 5),
    ("Corn Flour 500g", "Grains", 40, 55, 20, 5),

    # Pulses & Lentils
    ("Toor Dal 1kg", "Pulses", 110, 140, 40, 10),
    ("Moong Dal 1kg", "Pulses", 100, 130, 35, 10),
    ("Chana Dal 1kg", "Pulses", 85, 110, 35, 10),
    ("Masoor Dal 1kg", "Pulses", 90, 115, 30, 10),
    ("Urad Dal 1kg", "Pulses", 105, 135, 30, 10),
    ("Rajma (Kidney Beans) 1kg", "Pulses", 110, 145, 25, 5),
    ("Chole (Chickpeas) 1kg", "Pulses", 90, 120, 30, 5),
    ("Green Moong Whole 1kg", "Pulses", 95, 125, 25, 5),
    ("Black Chana 1kg", "Pulses", 80, 105, 25, 5),
    ("Soya Chunks 200g", "Pulses", 35, 50, 30, 5),

    # Cooking Oil & Ghee
    ("Sunflower Oil 1L", "Cooking Oil", 130, 160, 30, 5),
    ("Groundnut Oil 1L", "Cooking Oil", 170, 210, 25, 5),
    ("Mustard Oil 1L", "Cooking Oil", 150, 185, 25, 5),
    ("Refined Soyabean Oil 1L", "Cooking Oil", 125, 155, 30, 5),
    ("Cow Ghee 500ml", "Cooking Oil", 280, 350, 20, 5),
    ("Coconut Oil 500ml", "Cooking Oil", 140, 175, 20, 5),
    ("Olive Oil 500ml", "Cooking Oil", 320, 400, 10, 3),

    # Dairy
    ("Amul Milk 500ml", "Dairy", 25, 30, 60, 15),
    ("Toned Milk 1L", "Dairy", 48, 58, 50, 15),
    ("Curd (Dahi) 400g", "Dairy", 30, 40, 40, 10),
    ("Paneer 200g", "Dairy", 70, 90, 25, 5),
    ("Butter 100g", "Dairy", 45, 58, 30, 8),
    ("Cheese Slices 200g", "Dairy", 90, 120, 20, 5),
    ("Fresh Cream 200ml", "Dairy", 45, 60, 15, 5),
    ("Buttermilk (Chaas) 200ml", "Dairy", 12, 18, 30, 10),
    ("Flavoured Yogurt 100g", "Dairy", 20, 30, 25, 5),

    # Bakery
    ("Brown Bread 400g", "Bakery", 35, 45, 25, 5),
    ("White Bread 400g", "Bakery", 30, 40, 25, 5),
    ("Milk Bread 400g", "Bakery", 32, 42, 20, 5),
    ("Rusk 200g", "Bakery", 25, 35, 20, 5),
    ("Bun Pav (6pc)", "Bakery", 20, 30, 25, 5),
    ("Cake Slice 100g", "Bakery", 30, 45, 15, 5),

    # Essentials / Spices
    ("Tata Salt 1kg", "Essentials", 18, 25, 100, 20),
    ("Sugar 1kg", "Essentials", 40, 50, 60, 15),
    ("Jaggery (Gur) 500g", "Essentials", 35, 48, 25, 5),
    ("Turmeric Powder 200g", "Essentials", 30, 45, 30, 5),
    ("Red Chilli Powder 200g", "Essentials", 40, 55, 30, 5),
    ("Coriander Powder 200g", "Essentials", 28, 40, 30, 5),
    ("Garam Masala 100g", "Essentials", 35, 50, 25, 5),
    ("Cumin Seeds (Jeera) 200g", "Essentials", 55, 75, 25, 5),
    ("Mustard Seeds 100g", "Essentials", 18, 28, 25, 5),
    ("Black Pepper 100g", "Essentials", 70, 95, 20, 5),
    ("Tea Powder 250g", "Essentials", 90, 120, 40, 10),
    ("Instant Coffee 100g", "Essentials", 150, 190, 25, 5),
    ("Green Tea 25 Bags", "Essentials", 80, 110, 15, 5),
    ("Honey 250g", "Essentials", 110, 145, 20, 5),
    ("Vinegar 500ml", "Essentials", 30, 42, 15, 5),
    ("Baking Soda 100g", "Essentials", 15, 22, 20, 5),
    ("Baking Powder 100g", "Essentials", 18, 26, 20, 5),

    # Snacks
    ("Potato Chips 90g", "Snacks", 18, 25, 50, 10),
    ("Banana Chips 150g", "Snacks", 35, 48, 30, 5),
    ("Namkeen Mixture 200g", "Snacks", 30, 42, 35, 8),
    ("Bhujia 200g", "Snacks", 32, 45, 35, 8),
    ("Popcorn 70g", "Snacks", 20, 30, 25, 5),
    ("Biscuits (Marie) 150g", "Snacks", 20, 28, 50, 10),
    ("Cream Biscuits 150g", "Snacks", 25, 35, 40, 10),
    ("Digestive Biscuits 200g", "Snacks", 40, 55, 30, 5),
    ("Salted Peanuts 200g", "Snacks", 30, 42, 30, 5),
    ("Cashew Nuts 200g", "Snacks", 180, 230, 15, 5),
    ("Almonds 200g", "Snacks", 160, 210, 15, 5),
    ("Raisins 200g", "Snacks", 55, 75, 20, 5),
    ("Instant Noodles (4-pack)", "Snacks", 48, 60, 60, 15),
    ("Ready-to-Eat Poha 80g", "Snacks", 25, 35, 20, 5),
    ("Chocolate Bar 50g", "Snacks", 30, 40, 40, 10),

    # Beverages
    ("Cola 750ml", "Beverages", 35, 45, 40, 10),
    ("Lemon Soda 750ml", "Beverages", 32, 42, 30, 8),
    ("Orange Juice 1L", "Beverages", 90, 115, 20, 5),
    ("Mango Juice 1L", "Beverages", 90, 115, 20, 5),
    ("Mineral Water 1L", "Beverages", 15, 20, 60, 15),
    ("Energy Drink 250ml", "Beverages", 90, 110, 20, 5),
    ("Soda Water 750ml", "Beverages", 25, 35, 25, 5),

    # Fruits & Vegetables
    ("Onion 1kg", "Vegetables", 25, 35, 50, 15),
    ("Potato 1kg", "Vegetables", 20, 30, 50, 15),
    ("Tomato 1kg", "Vegetables", 25, 38, 40, 10),
    ("Garlic 250g", "Vegetables", 30, 45, 25, 5),
    ("Ginger 250g", "Vegetables", 25, 38, 25, 5),
    ("Green Chilli 100g", "Vegetables", 8, 15, 30, 8),
    ("Banana (Dozen)", "Fruits", 40, 55, 30, 8),
    ("Apple 1kg", "Fruits", 120, 160, 25, 5),
    ("Orange 1kg", "Fruits", 60, 85, 25, 5),
    ("Lemon 250g", "Fruits", 15, 25, 30, 8),

    # Personal Care & Cleaning
    ("Toothpaste 150g", "Personal Care", 60, 80, 30, 8),
    ("Toothbrush (Pack of 2)", "Personal Care", 30, 45, 30, 8),
    ("Bathing Soap (Pack of 3)", "Personal Care", 80, 105, 40, 10),
    ("Shampoo 200ml", "Personal Care", 120, 155, 25, 5),
    ("Hand Sanitizer 200ml", "Personal Care", 70, 95, 20, 5),
    ("Detergent Powder 1kg", "Cleaning", 90, 120, 30, 8),
    ("Dishwash Liquid 500ml", "Cleaning", 75, 100, 30, 8),
    ("Floor Cleaner 1L", "Cleaning", 85, 115, 25, 5),
    ("Toilet Cleaner 500ml", "Cleaning", 60, 82, 25, 5),
    ("Garbage Bags (30pc)", "Cleaning", 60, 80, 30, 8),
]

os.makedirs('database', exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

added = 0
skipped = 0

for name, category, cost_price, selling_price, qty, reorder in PRODUCTS:
    existing = conn.execute('SELECT 1 FROM products WHERE name = ?', (name,)).fetchone()
    if existing:
        skipped += 1
        continue
    conn.execute(
        '''INSERT INTO products
           (name, category, cost_price, selling_price, quantity_in_stock, reorder_threshold, image_path)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (name, category, cost_price, selling_price, qty, reorder, None)
    )
    added += 1

conn.commit()
conn.close()

print(f"Added {added} new products.")
print(f"Skipped {skipped} products that already existed.")
print(f"Total products in list: {len(PRODUCTS)}")