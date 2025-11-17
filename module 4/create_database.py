import sqlite3
# Step 1: Connect to SQLite (creates database.db automatically)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Step 2: Create Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_url TEXT
)
""")

# Step 3: Create Reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    raw_review TEXT,
    cleaned_review TEXT,
    sentiment_label TEXT,
    sentiment_score REAL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# Step 4: Save & close
conn.commit()
conn.close()

print("Database and tables created successfully!")
