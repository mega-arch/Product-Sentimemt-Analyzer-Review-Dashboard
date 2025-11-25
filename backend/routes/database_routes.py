from flask import Blueprint, request, jsonify
import sqlite3
from utils.preprocessing import preprocess_review   # <-- Added preprocessing import

db_bp = Blueprint("database", __name__)

DB_PATH = "sentiment.db"


# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
def get_connection():
    return sqlite3.connect(DB_PATH)


# -----------------------------------
# PRODUCT APIs
# -----------------------------------

@db_bp.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    rating = data.get("rating")

    if not name:
        return jsonify({"error": "Product name is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, category, price, rating) VALUES (?, ?, ?, ?)",
        (name, category, price, rating),
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Product added successfully!"})


@db_bp.route("/get_products", methods=["GET"])
def get_products():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(products)


@db_bp.route("/search_products", methods=["GET"])
def search_products():
    keyword = request.args.get("keyword", "").lower()

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE LOWER(name) LIKE ?",
        (f"%{keyword}%",),
    )

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if results:
        return jsonify({"message": "success", "products": results})
    return jsonify({"message": "No products found", "products": []})


# -----------------------------------
# REVIEW APIs
# -----------------------------------

@db_bp.route("/add_review", methods=["POST"])
def add_review():
    data = request.json
    product_id = data.get("product_id")
    review_text = data.get("review_text")
    sentiment = data.get("sentiment")

    if not (product_id and review_text and sentiment):
        return jsonify({"error": "Missing required fields"}), 400

    # PROCESS TEXT BEFORE STORING
    cleaned_text = preprocess_review(review_text)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reviews (product_id, review_text, sentiment) VALUES (?, ?, ?)",
        (product_id, cleaned_text, sentiment),
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Review added successfully!"})


@db_bp.route("/get_reviews", methods=["GET"])
def get_reviews():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reviews")
    reviews = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(reviews)


@db_bp.route("/search_reviews", methods=["GET"])
def search_reviews():
    product_id = request.args.get("product_id")

    if not product_id:
        return jsonify({"message": "Provide product_id"}), 400

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM reviews WHERE product_id = ?",
        (product_id,),
    )

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if results:
        return jsonify({"message": "success", "reviews": results})
    return jsonify({"message": "No reviews found", "reviews": []})
