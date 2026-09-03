import sqlite3
conn = sqlite3.connect('database/grocery.db')
rows = conn.execute('SELECT name FROM sqlite_master').fetchall()
for r in rows:
    print(r[0])
