import sqlite3
import pandas as pd

df = pd.read_csv("final_reviews.csv")

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO reviews (product_name, review, sentiment)
        VALUES (?, ?, ?)
    """, (
        row["Product_Name"],
        row["Review_Text"],
        row["Sentiment"]
    ))

conn.commit()
conn.close()

print("Inserted reviews into SQLite!")
