import sqlite3
import pandas as pd

df = pd.read_csv("flipkart_products_preprocessed.csv")

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO products (product_id, product_name, product_url)
        VALUES (?, ?, ?)
    """, (
        row["Product_ID"],      # Correct column name
        row["Product_Name"],    # Correct column name
        row["Product_URL"]      # Correct column name
    ))

conn.commit()
conn.close()

print("Inserted all products into SQLite!")
