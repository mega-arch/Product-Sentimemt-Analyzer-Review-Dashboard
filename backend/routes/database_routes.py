from flask import Blueprint, request, jsonify
import sqlite3
from utils.preprocessing import preprocess_review

db_bp = Blueprint("database", __name__)

DB_PATH = "database.db"


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# PRODUCT APIs
# -----------------------------
@db_bp.route("/add_product", methods=["POST"])
def add_product():
    data = request.json
    name = data.get("product_name")
    url = data.get("product_url")

    if not (name and url):
        return jsonify({"error": "product_name and product_url are required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (product_name, product_url) VALUES (?, ?)",
        (name, url)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Product added successfully!"})


@db_bp.route("/get_products", methods=["GET"])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products)


@db_bp.route("/search_products", methods=["GET"])
def search_products():
    keyword = request.args.get("keyword", "").lower()
    if not keyword:
        return jsonify({"products": []})

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE LOWER(product_name) LIKE ?",
        (f"%{keyword}%",)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"products": results})


# -----------------------------
# REVIEW APIs
# -----------------------------
@db_bp.route("/add_review", methods=["POST"])
def add_review():
    data = request.json
    product_id = data.get("product_id")
    raw_review = data.get("raw_review")

    if not (product_id and raw_review):
        return jsonify({"error": "product_id and raw_review are required"}), 400

    # preprocess review
    cleaned_review = preprocess_review(raw_review)

    # predict sentiment
    sentiment_label, sentiment_score = predict_sentiment(cleaned_review)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reviews
        (product_id, raw_review, cleaned_review, sentiment_label, sentiment_score)
        VALUES (?, ?, ?, ?, ?)
        """,
        (product_id, raw_review, cleaned_review, sentiment_label, sentiment_score)
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Review added successfully!"})


@db_bp.route("/get_reviews", methods=["GET"])
def get_reviews():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews")
    reviews = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(reviews)


@db_bp.route("/search_reviews", methods=["GET"])
def search_reviews():
    product_id = request.args.get("product_id")
    if not product_id:
        return jsonify({"reviews": []})

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM reviews WHERE product_id = ?",
        (product_id,)
    )
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"reviews": results})
