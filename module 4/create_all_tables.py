import sqlite3

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    product_url TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    review TEXT,
    sentiment TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sentiment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    review_text TEXT,
    sentiment TEXT,
    score REAL
)
""")

conn.commit()
conn.close()

print("All tables created successfully!")
