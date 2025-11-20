import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os
import pandas as pd

csv_path = os.path.join(os.path.dirname(__file__), 'data', 'sentiment_output.csv')
data = pd.read_csv(csv_path)


# Load CSV
data = pd.read_csv('data/sentiment_output.csv')

# Use 'review' as X and 'vader_sentiment' as y
X = data['review'].astype(str)
y = data['vader_sentiment']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Save model & vectorizer
joblib.dump(model, 'models/sentiment_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("Sentiment model and vectorizer saved successfully!")
