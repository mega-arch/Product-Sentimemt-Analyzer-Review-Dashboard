import sqlite3

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    review TEXT,
    sentiment TEXT
)
""")

conn.commit()
conn.close()

print("Reviews table created successfully!")
