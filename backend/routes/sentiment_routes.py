from flask import Blueprint, request, jsonify
import joblib

sentiment_bp = Blueprint("sentiment", __name__)

# Load trained model + vectorizer
model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

@sentiment_bp.route("/predict", methods=["POST"])
def predict_sentiment():
    data = request.json
    cleaned_review = data.get("cleaned_review", "")

    if not cleaned_review:
        return jsonify({"error": "cleaned_review is required"}), 400

    # Vectorize review
    review_vec = vectorizer.transform([cleaned_review])

    # Label
    sentiment_label = model.predict(review_vec)[0]

    # Probability score
    sentiment_prob = model.predict_proba(review_vec).max()

    return jsonify({
        "sentiment_label": sentiment_label,
        "sentiment_score": float(sentiment_prob)
    })
