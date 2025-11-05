# --- put this in app.py temporarily and run once ---
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS products')
cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        image TEXT
    )
''')

products = [
    ("Apple", 50, "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=300"),
    ("Banana", 30, "https://images.unsplash.com/photo-1574226516831-e1dff420e12b?w=300"),
    ("Milk", 45, "https://images.unsplash.com/photo-1585238342028-6d4d9f4df2b8?w=300"),
    ("Bread", 25, "https://images.unsplash.com/photo-1608198093002-ad4e0054842f?w=300"),
    ("Eggs", 60, "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300")
]

cursor.executemany("INSERT INTO products (name, price, image) VALUES (?, ?, ?)", products)
conn.commit()
conn.close()

print("✅ Database recreated with online images!")
