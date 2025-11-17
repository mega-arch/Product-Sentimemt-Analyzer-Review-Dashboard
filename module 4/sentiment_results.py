import sqlite3
import pandas as pd

df = pd.read_csv("sentiment_output.csv")

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO sentiment_results (product_name, review_text, sentiment, score)
        VALUES (?, ?, ?, ?)
    """, (
        None,                               # No product name available in CSV
        row["review"],                       # review text
        row["vader_sentiment"],              # sentiment label
        float(row["vader_score"])            # sentiment score
    ))

conn.commit()
conn.close()

print("Inserted sentiment results into SQLite!")
