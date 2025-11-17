import sqlite3

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

print("\nTABLES:")
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(tables)

print("\nPRODUCTS (first 5 rows):")
print(cursor.execute("SELECT * FROM products LIMIT 5").fetchall())

print("\nREVIEWS (first 5 rows):")
print(cursor.execute("SELECT * FROM reviews LIMIT 5").fetchall())

print("\nSENTIMENT_RESULTS (first 5 rows):")
print(cursor.execute("SELECT * FROM sentiment_results LIMIT 5").fetchall())

conn.close()
