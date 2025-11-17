import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

df = pd.read_csv("cleaned_reviews.csv")

sid = SentimentIntensityAnalyzer()

sentiments = []
for text in df["cleaned_review"]:
    score = sid.polarity_scores(text)["compound"]
    if score >= 0.05:
        sentiments.append("Positive")
    elif score <= -0.05:
        sentiments.append("Negative")
    else:
        sentiments.append("Neutral")

df["sentiment"] = sentiments
df.to_csv("final_reviews.csv", index=False)

print("final_reviews.csv created with 300 sentiment labels!")
