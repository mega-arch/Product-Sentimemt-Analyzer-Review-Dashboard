import pandas as pd
from .vader_model import vader_predict
from .textblob_model import textblob_predict

def test_model(dataset_path):
    print("Loading dataset:", dataset_path)

    df = pd.read_csv(dataset_path)

    # Find correct review column
    if "review" in df.columns:
        review_col = "review"
    elif "Review" in df.columns:
        review_col = "Review"
    elif "Reviews" in df.columns:
        review_col = "Reviews"
    else:
        print("ERROR: No review column found!")
        print("Available columns:", df.columns.tolist())
        return

    print("Using review column:", review_col)
    print("Running predictions...")

    results = []

    for text in df[review_col].astype(str).fillna(""):
        vader = vader_predict(text)
        blob = textblob_predict(text)

        results.append({
            "review": text,
            "vader_score": vader["compound"],
            "vader_sentiment": vader["sentiment"],
            "textblob_score": blob["polarity"],
            "textblob_sentiment": blob["sentiment"]
        })

    results_df = pd.DataFrame(results)
    output_path = "./module3/sentiment_output.csv"
    results_df.to_csv(output_path, index=False)

    print("Model test completed!")
    print("Total reviews processed:", len(results))
    print(f"Predictions saved to: {output_path}")


if __name__ == "__main__":
    dataset_path = "./sample_data/sample_reviews.csv"
    test_model(dataset_path)
