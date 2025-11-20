from flask import Blueprint, request, jsonify
import joblib

sentiment_bp = Blueprint('sentiment', __name__)

# Load trained model and vectorizer
model = joblib.load('models/sentiment_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

@sentiment_bp.route('/predict', methods=['POST'])
def predict_sentiment():
    data = request.json
    review = data.get('review', '')
    review_vec = vectorizer.transform([review])
    sentiment = model.predict(review_vec)[0]
    return jsonify({"sentiment": sentiment})
