import joblib

# Load model & vectorizer once
model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def predict_sentiment(text):
    """Returns (label, score) for a given text."""
    
    # Transform text
    vector = vectorizer.transform([text])

    # Predict label
    label = model.predict(vector)[0]

    # Predict probability
    try:
        score = model.predict_proba(vector).max()
    except:
        score = None  # If model has no probability support (SVM without probability=True)

    return label, score
