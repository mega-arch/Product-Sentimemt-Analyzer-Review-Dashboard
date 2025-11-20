from flask import Blueprint, request, jsonify
import mysql.connector
from mysql.connector import Error

db_bp = Blueprint('database', __name__)

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',       # or your MySQL server host
    'user': 'root',            # your MySQL username
    'password': '1234',  # your MySQL password
    'database': 'sentiment_db'    # your database name
}

# Function to get connection
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Create table if not exists
def create_table():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(255),
                review TEXT,
                sentiment VARCHAR(20)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

create_table()  # Create table on import

# API to insert review
@db_bp.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    product_name = data.get('product_name')
    review = data.get('review')
    sentiment = data.get('sentiment')

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (product_name, review_text, sentiment) VALUES (%s, %s, %s)",
            (product_name, review, sentiment)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Review added successfully"})
    else:
        return jsonify({"error": "Database connection failed"}), 500

# API to fetch all reviews
@db_bp.route('/get_reviews', methods=['GET'])
def get_reviews():
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reviews")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    else:
        return jsonify({"error": "Database connection failed"}), 500
