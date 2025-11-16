from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def vader_predict(text):
    scores = analyzer.polarity_scores(text)

    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "model": "VADER",
        "text": text,
        "compound": compound,          # ✔ THIS IS WHAT train.py NEEDS
        "sentiment": sentiment,
        "raw_scores": scores
    }
