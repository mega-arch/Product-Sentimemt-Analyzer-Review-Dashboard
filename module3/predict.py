def analyze_review(text):
    from .vader_model import vader_predict
    from .textblob_model import textblob_predict

    return {
        "review": text,
        "vader_sentiment": vader_predict(text),
        "textblob_sentiment": textblob_predict(text)
    }
if __name__ == "__main__":
    review = input("Enter a review: ")
    print(analyze_review(review))

