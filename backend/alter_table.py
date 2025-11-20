import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="sentiment_db"
)

cursor = conn.cursor()

# Add a new column
cursor.execute("ALTER TABLE reviews ADD COLUMN product_name VARCHAR(255);")

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Column added successfully!")
