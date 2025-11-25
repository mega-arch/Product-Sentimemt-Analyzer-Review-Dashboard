import sqlite3
import random

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

# ------------ SAMPLE POOLS ------------
categories = [
    "Smartphone", "Laptop", "Headphones", "TV", "Tablet",
    "Camera", "Smartwatch", "Speaker", "Printer", "Monitor"
]

sample_reviews = [
    "Excellent product, totally worth the price!",
    "Very bad experience, not recommended.",
    "Average quality, but works fine.",
    "Super fast performance and smooth user experience.",
    "Battery life is not great.",
    "Build quality is amazing.",
    "Stopped working after a week.",
    "Highly recommended for this price range.",
    "The product is okay, but delivery was slow.",
    "Fantastic audio quality!"
]

sentiments = ["positive", "negative", "neutral"]

# ------------ INSERT 200 PRODUCTS ------------
product_ids = []

for i in range(1, 201):
    name = f"Sample Product {i}"
    category = random.choice(categories)
    price = random.randint(500, 80000)
    rating = round(random.uniform(2.5, 5.0), 1)

    cursor.execute(
        "INSERT INTO products (name, category, price, rating) VALUES (?, ?, ?, ?)",
        (name, category, price, rating)
    )

    product_ids.append(cursor.lastrowid)

# ------------ INSERT 200 REVIEWS ------------
for i in range(1, 201):
    product_id = random.choice(product_ids)
    review_text = random.choice(sample_reviews)
    sentiment = random.choice(sentiments)

    cursor.execute(
        "INSERT INTO reviews (product_id, review_text, sentiment) VALUES (?, ?, ?)",
        (product_id, review_text, sentiment)
    )

conn.commit()
conn.close()

print("200 new products + 200 new reviews added successfully!")
