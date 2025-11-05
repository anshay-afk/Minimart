import sqlite3


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("Tables in DB:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

print("\nProducts Table:")
cursor.execute("SELECT * FROM products;")
for row in cursor.fetchall():
    print(row)

print("\nCart Table:")
cursor.execute("SELECT * FROM cart;")
for row in cursor.fetchall():
    print(row)

conn.close()
