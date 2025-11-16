from textblob import TextBlob

def textblob_predict(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "model": "TextBlob",
        "text": text,
        "polarity": polarity,    # ✔ train.py needs this
        "sentiment": sentiment
    }
