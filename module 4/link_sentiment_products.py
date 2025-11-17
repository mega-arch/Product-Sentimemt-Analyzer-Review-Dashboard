import sqlite3

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

# fetch all reviews with product names
reviews = cursor.execute("""
    SELECT review, product_name
    FROM reviews
""").fetchall()

# create a mapping: review_text → product_name
review_to_product = {review: product_name for review, product_name in reviews}

# update sentiment_results table with product_name
cursor.execute("SELECT id, review_text FROM sentiment_results")
rows = cursor.fetchall()

for row in rows:
    sentiment_id = row[0]
    review_text = row[1]

    product_name = review_to_product.get(review_text)

    if product_name:
        cursor.execute("""
            UPDATE sentiment_results
            SET product_name = ?
            WHERE id = ?
        """, (product_name, sentiment_id))

conn.commit()
conn.close()

print("Linked sentiment results with product names!")
