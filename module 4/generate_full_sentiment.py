import pandas as pd

# Load your input files
pre = pd.read_csv("flipkart_products_preprocessed.csv")
sent = pd.read_csv("sentiment_output.csv")

# Merge the 196 sentiment rows into the 300 preprocessed rows
merged = pre.merge(sent, on="review", how="left")

# For missing sentiments, fill with Neutral
merged["sentiment"].fillna("Neutral", inplace=True)

# Save full 300 rows
merged.to_csv("full_sentiment_300.csv", index=False)

print("Full sentiment file created: full_sentiment_300.csv")
