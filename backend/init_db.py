import sqlite3

connection = sqlite3.connect("sentiment.db")
cursor = connection.cursor()

# Create Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL,
    rating REAL
);
""")

# Create Reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    review_text TEXT NOT NULL,
    sentiment TEXT,
    FOREIGN KEY(product_id) REFERENCES products(id)
);
""")

# Insert sample products
cursor.execute("""
INSERT INTO products (name, category, price, rating)
VALUES
('Samsung Galaxy M14', 'Smartphone', 12999, 4.3),
('Sony WH-1000XM4 Headphones', 'Electronics', 29990, 4.7),
('Dell Inspiron 3511 Laptop', 'Laptop', 45990, 4.2);
""")

# Insert sample reviews
cursor.execute("""
INSERT INTO reviews (product_id, review_text, sentiment)
VALUES
(1, 'Battery backup is excellent and performance is smooth.', 'positive'),
(1, 'Camera quality could be better.', 'neutral'),
(2, 'Amazing sound clarity and noise cancellation!', 'positive'),
(3, 'Laptop heats up during gaming.', 'negative');
""")

connection.commit()
connection.close()

print("Database created with sample data!")
