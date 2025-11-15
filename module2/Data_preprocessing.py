"""
Data Preprocessing Module for Flipkart Product Reviews
Purpose: Clean and preprocess textual data for sentiment analysis
"""

import pandas as pd
import numpy as np
import re
import string
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

# NLP Libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')


class DataPreprocessor:
    """
    Main class for data preprocessing operations
    """
    
    def __init__(self, use_spacy=False):
        """
        Initialize the preprocessor with required NLP tools
        
        Args:
            use_spacy (bool): Whether to use spaCy for advanced processing
        """
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.use_spacy = use_spacy
        
        if use_spacy:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                print("Downloading spaCy model...")
                import os
                os.system('python -m spacy download en_core_web_sm')
                self.nlp = spacy.load('en_core_web_sm')
        
        # Define spam keywords
        self.spam_keywords = [
            'click here', 'visit now', 'buy now', 'limited offer',
            'act now', 'call now', 'free money', 'earn money',
            'work from home', 'make money fast'
        ]
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load the scraped data from CSV file
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded dataframe
        """
        print(f"Loading data from {filepath}...")
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} records")
        print(f"Columns: {df.columns.tolist()}")
        return df
    
    def explore_data(self, df: pd.DataFrame) -> None:
        """
        Perform exploratory data analysis
        
        Args:
            df (pd.DataFrame): Input dataframe
        """
        print("\n=== DATA EXPLORATION ===")
        print(f"Shape: {df.shape}")
        print(f"\nData Types:\n{df.dtypes}")
        print(f"\nMissing Values:\n{df.isnull().sum()}")
        print(f"\nBasic Statistics:\n{df.describe()}")
        print(f"\nCategory Distribution:\n{df['Category'].value_counts()}")
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with handled missing values
        """
        print("\n=== HANDLING MISSING VALUES ===")
        initial_rows = len(df)
        
        # Handle numeric columns
        numeric_cols = ['Price', 'Total_Ratings', 'Total_Reviews']
        for col in numeric_cols:
            if col in df.columns:
                # Convert to numeric, coercing errors
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Fill missing values with 0
                df[col].fillna(0, inplace=True)
        
        # Handle Rating column (extract numeric value)
        if 'Rating' in df.columns:
            df['Rating_Numeric'] = df['Rating'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
            df['Rating_Numeric'] = pd.to_numeric(df['Rating_Numeric'], errors='coerce')
            df['Rating_Numeric'].fillna(0, inplace=True)
        
        # Handle Discount column
        if 'Discount' in df.columns:
            df['Discount_Numeric'] = df['Discount'].astype(str).str.extract(r'(\d+)')[0]
            df['Discount_Numeric'] = pd.to_numeric(df['Discount_Numeric'], errors='coerce')
            df['Discount_Numeric'].fillna(0, inplace=True)
        
        # Handle text columns
        text_cols = ['Product_Name', 'Category']
        for col in text_cols:
            if col in df.columns:
                df[col].fillna('Unknown', inplace=True)
        
        # Remove rows where Product_Name is missing or 'Not Found'
        df = df[df['Product_Name'] != 'Not Found']
        df = df[df['Product_Name'] != 'Unknown']
        
        final_rows = len(df)
        print(f"Rows before: {initial_rows}, Rows after: {final_rows}")
        print(f"Removed {initial_rows - final_rows} rows")
        
        return df
    
    def clean_text(self, text: str) -> str:
        """
        Clean individual text string
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text
        """
        if pd.isna(text) or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text without stopwords
        """
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords but keep important sentiment words
        sentiment_words = {'not', 'no', 'nor', 'neither', 'never', 'none', 
                          'very', 'too', 'best', 'worst', 'good', 'bad'}
        
        filtered_tokens = [
            word for word in tokens 
            if word not in self.stop_words or word in sentiment_words
        ]
        
        return ' '.join(filtered_tokens)
    
    def lemmatize_text(self, text: str) -> str:
        """
        Lemmatize text using NLTK
        
        Args:
            text (str): Input text
            
        Returns:
            str: Lemmatized text
        """
        tokens = word_tokenize(text)
        lemmatized = [self.lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(lemmatized)
    
    def lemmatize_text_spacy(self, text: str) -> str:
        """
        Lemmatize text using spaCy
        
        Args:
            text (str): Input text
            
        Returns:
            str: Lemmatized text
        """
        doc = self.nlp(text)
        lemmatized = [token.lemma_ for token in doc if not token.is_stop]
        return ' '.join(lemmatized)
    
    def detect_spam(self, text: str) -> bool:
        """
        Detect if text is spam or irrelevant
        
        Args:
            text (str): Input text
            
        Returns:
            bool: True if spam, False otherwise
        """
        text_lower = text.lower()
        
        # Check for spam keywords
        for keyword in self.spam_keywords:
            if keyword in text_lower:
                return True
        
        # Check for excessive punctuation
        if text.count('!') > 5 or text.count('?') > 5:
            return True
        
        # Check for excessive capitalization
        if len(text) > 0 and sum(1 for c in text if c.isupper()) / len(text) > 0.7:
            return True
        
        # Check for very short text (likely not a real review)
        if len(text.split()) < 3:
            return True
        
        return False
    
    def preprocess_product_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess product names column
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with preprocessed product names
        """
        print("\n=== PREPROCESSING PRODUCT NAMES ===")
        
        if 'Product_Name' not in df.columns:
            print("Product_Name column not found")
            return df
        
        # Create cleaned version
        df['Product_Name_Clean'] = df['Product_Name'].apply(self.clean_text)
        
        # Create processed version (for analysis)
        df['Product_Name_Processed'] = df['Product_Name_Clean'].apply(
            lambda x: self.lemmatize_text(self.remove_stopwords(x))
        )
        
        # Extract key features
        df['Product_Brand'] = df['Product_Name'].str.split().str[0]
        
        print("Product names preprocessed successfully")
        return df
    
    def create_sentiment_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create sentiment labels based on ratings
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with sentiment labels
        """
        print("\n=== CREATING SENTIMENT LABELS ===")
        
        if 'Rating_Numeric' not in df.columns:
            print("Rating_Numeric column not found")
            return df
        
        # Create sentiment labels
        def get_sentiment(rating):
            if rating >= 4.0:
                return 'Positive'
            elif rating >= 3.0:
                return 'Neutral'
            elif rating > 0:
                return 'Negative'
            else:
                return 'Unknown'
        
        df['Sentiment'] = df['Rating_Numeric'].apply(get_sentiment)
        
        # Create binary labels for classification
        df['Sentiment_Binary'] = df['Rating_Numeric'].apply(
            lambda x: 1 if x >= 3.5 else 0 if x > 0 else -1
        )
        
        print("Sentiment Distribution:")
        print(df['Sentiment'].value_counts())
        
        return df
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create additional features for analysis
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe with additional features
        """
        print("\n=== CREATING ADDITIONAL FEATURES ===")
        
        # Text length features
        if 'Product_Name_Clean' in df.columns:
            df['Name_Length'] = df['Product_Name_Clean'].str.len()
            df['Name_Word_Count'] = df['Product_Name_Clean'].str.split().str.len()
        
        # Rating features
        if 'Rating_Numeric' in df.columns and 'Total_Ratings' in df.columns:
            df['Rating_Category'] = pd.cut(
                df['Rating_Numeric'], 
                bins=[0, 2, 3, 4, 5], 
                labels=['Poor', 'Fair', 'Good', 'Excellent']
            )
            
            # Popularity score
            df['Popularity_Score'] = (
                df['Rating_Numeric'] * np.log1p(df['Total_Ratings'])
            )
        
        # Price features
        if 'Price' in df.columns:
            df['Price_Category'] = pd.qcut(
                df['Price'], 
                q=4, 
                labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'],
                duplicates='drop'
            )
        
        print("Additional features created successfully")
        return df
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate entries
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: Dataframe without duplicates
        """
        print("\n=== REMOVING DUPLICATES ===")
        initial_rows = len(df)
        
        # Remove exact duplicates
        df = df.drop_duplicates()
        
        # Remove duplicates based on Product_URL
        if 'Product_URL' in df.columns:
            df = df.drop_duplicates(subset=['Product_URL'], keep='first')
        
        final_rows = len(df)
        print(f"Removed {initial_rows - final_rows} duplicate rows")
        
        return df
    
    def preprocess_pipeline(self, input_file: str, output_file: str = None) -> pd.DataFrame:
        """
        Complete preprocessing pipeline
        
        Args:
            input_file (str): Path to input CSV file
            output_file (str): Path to save preprocessed data
            
        Returns:
            pd.DataFrame: Preprocessed dataframe
        """
        print("\n" + "="*60)
        print("STARTING DATA PREPROCESSING PIPELINE")
        print("="*60)
        
        # Load data
        df = self.load_data(input_file)
        
        # Explore data
        self.explore_data(df)
        
        # Remove duplicates
        df = self.remove_duplicates(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Preprocess product names
        df = self.preprocess_product_names(df)
        
        # Create sentiment labels
        df = self.create_sentiment_labels(df)
        
        # Create additional features
        df = self.create_features(df)
        
        # Final data summary
        print("\n=== FINAL DATA SUMMARY ===")
        print(f"Total records: {len(df)}")
        print(f"Total features: {len(df.columns)}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Save preprocessed data
        if output_file:
            df.to_csv(output_file, index=False)
            print(f"\nPreprocessed data saved to: {output_file}")
        
        print("\n" + "="*60)
        print("PREPROCESSING PIPELINE COMPLETED")
        print("="*60)
        
        return df


# Main execution
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = DataPreprocessor(use_spacy=False)
    
    # Run preprocessing pipeline
    input_file = "flipkart_products.csv"  # Update with your file path
    output_file = "flipkart_products_preprocessed.csv"
    
    try:
        df_preprocessed = preprocessor.preprocess_pipeline(
            input_file=input_file,
            output_file=output_file
        )
        
        # Display sample of preprocessed data
        print("\n=== SAMPLE PREPROCESSED DATA ===")
        print(df_preprocessed[['Product_Name', 'Product_Name_Clean', 
                               'Rating_Numeric', 'Sentiment', 
                               'Category']].head(10))
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        print("Please update the input_file path in the script.")
    except Exception as e:
        print(f"Error during preprocessing: {str(e)}")