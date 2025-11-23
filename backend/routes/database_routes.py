from flask import Blueprint, request, jsonify
import mysql.connector
from mysql.connector import Error

db_bp = Blueprint('database', __name__)

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'sentiment_db'
}

# Function to get a connection
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# -------------------------------
# CREATE TABLES
# -------------------------------
def create_tables():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(255)
            )
        """)
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

create_tables()

# ===============================
# PRODUCT APIs
# ===============================

# Add product
@db_bp.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    product_name = data.get('product_name')
    if not product_name:
        return jsonify({"error": "Missing product_name"}), 400

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (product_name) VALUES (%s)",
            (product_name,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"error": "Database connection failed"}), 500

# Get all products
@db_bp.route('/get_products', methods=['GET'])
def get_products():
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    return jsonify({"error": "Database connection failed"}), 500

# Search products
@db_bp.route('/search_products', methods=['GET'])
def search_products():
    keyword = request.args.get('keyword', '').lower()
    if not keyword:
        return jsonify({"message": "Provide a search keyword", "products": []})

    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM products WHERE LOWER(product_name) LIKE %s",
            ("%" + keyword + "%",)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if not results:
            return jsonify({"message": "No products found", "products": []})
        return jsonify({"message": "success", "products": results})
    return jsonify({"error": "Database connection failed"}), 500

# ===============================
# REVIEW APIs
# ===============================

# Add review
@db_bp.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    product_name = data.get('product_name')
    review = data.get('review_text')
    sentiment = data.get('sentiment')

    if not (product_name and review and sentiment):
        return jsonify({"error": "Missing data"}), 400

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
    return jsonify({"error": "Database connection failed"}), 500

# Get all reviews
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
    return jsonify({"error": "Database connection failed"}), 500

# Search reviews by product
@db_bp.route('/search_reviews', methods=['GET'])
def search_reviews():
    product_name = request.args.get('product_name', '').lower()
    if not product_name:
        return jsonify({"message": "Provide a product_name", "reviews": []})

    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM reviews WHERE LOWER(product_name) LIKE %s",
            ("%" + product_name + "%",)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if not results:
            return jsonify({"message": "No reviews found", "reviews": []})
        return jsonify({"message": "success", "reviews": results})
    return jsonify({"error": "Database connection failed"}), 500
