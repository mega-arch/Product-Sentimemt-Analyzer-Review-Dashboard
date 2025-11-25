from flask import Blueprint, request, jsonify
from utils.preprocessing import preprocess_review

preprocessing_bp = Blueprint("preprocessing", __name__)

@preprocessing_bp.route("/clean", methods=["POST"])
def clean_review():
    data = request.json
    raw_review = data.get("review", "")

    if not raw_review:
        return jsonify({"error": "Review text is required"}), 400

    cleaned = preprocess_review(raw_review)

    return jsonify({
        "raw_review": raw_review,
        "cleaned_review": cleaned
    })
