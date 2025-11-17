import pandas as pd
import re

# Load your raw review file
df = pd.read_csv("sample_reviews.csv")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["cleaned_review"] = df["review"].apply(clean_text)
df["id"] = range(1, len(df)+1)

df.to_csv("cleaned_reviews.csv", index=False)

print("cleaned_reviews.csv created successfully!")
