from flask import Blueprint, request, jsonify
from utils.preprocessing import preprocess_review

preprocessing_bp = Blueprint('preprocessing', __name__)

@preprocessing_bp.route('/clean', methods=['POST'])
def clean_text():
    data = request.json
    review = data.get('review', '')
    cleaned_review = preprocess_review(review)
    return jsonify({"cleaned_review": cleaned_review})
