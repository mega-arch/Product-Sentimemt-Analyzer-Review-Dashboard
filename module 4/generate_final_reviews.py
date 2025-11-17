import pandas as pd

# Load data
products = pd.read_csv("flipkart_products_preprocessed.csv")
sent = pd.read_csv("sentiment_output.csv")

# Create a basic review dataset using product name
# Because module2 has no review text at all
df = pd.DataFrame({
    "Product_Name": products["Product_Name"],
    "Review_Text": ["No review available"] * len(products),
    "Sentiment": ["Neutral"] * len(products)
})

# Fill the first 196 rows with real sentiments
for i in range(len(sent)):
    df.loc[i, "Review_Text"] = sent.loc[i, "review"]
    df.loc[i, "Sentiment"] = sent.loc[i, "vader_sentiment"]

# Save output
df.to_csv("final_reviews_300.csv", index=False)

print("Created final_reviews_300.csv with 300 reviews.")
