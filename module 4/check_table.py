import sqlite3

conn = sqlite3.connect("sentiment.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(reviews)")
print(cursor.fetchall())

conn.close()
