import sqlite3
import pandas as pd

# Load the final 300 reviews
df = pd.read_csv("final_reviews_300.csv")

# Connect to DB
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

product_id_counter = 1  # Since you don't have product_id in the CSV

for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO reviews (product_id, raw_review, cleaned_review, sentiment_label, sentiment_score)
    VALUES (?, ?, ?, ?, ?)
    """, (
        product_id_counter,
        row["Review_Text"],
        row["Review_Text"],  # using same data as cleaned_review
        row["Sentiment"],
        0.0  # default sentiment score
    ))

    product_id_counter += 1

conn.commit()
conn.close()

print("Inserted all 300 rows successfully into REVIEWS table!")
