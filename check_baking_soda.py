import psycopg2, os
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cur = conn.cursor()
cur.execute("SELECT product_id, name, image_path FROM products WHERE name ILIKE '%baking soda%'")
for row in cur.fetchall():
    print(row)
