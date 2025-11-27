import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 1️⃣ Pie chart of sentiment distribution
def sentiment_pie_chart(reviews):
    if not reviews:
        st.warning("No reviews to visualize.")
        return

    df = pd.DataFrame(reviews)
    if 'sentiment_label' not in df.columns:
        st.warning("'sentiment_label' column not found.")
        return

    sentiment_counts = df['sentiment_label'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']

    fig = px.pie(
        sentiment_counts,
        names='Sentiment',
        values='Count',
        title="Sentiment Distribution",
        color='Sentiment',
        color_discrete_map={'positive':'green', 'neutral':'gray', 'negative':'red'}
    )
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# 2️⃣ Sentiment trend line over time (if 'date' exists)
def sentiment_trend_line(reviews):
    if not reviews:
        st.warning("No reviews to visualize.")
        return

    df = pd.DataFrame(reviews)
    if 'date' not in df.columns or 'sentiment_label' not in df.columns:
        st.info("No 'date' column for trend visualization.")
        return

    df['date'] = pd.to_datetime(df['date'])
    trend_df = df.groupby([df['date'].dt.date, 'sentiment_label']).size().reset_index(name='Count')

    fig = px.line(
        trend_df,
        x='date',
        y='Count',
        color='sentiment_label',
        title="Sentiment Trend Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# Main function to call all visualizations
def visualize_reviews(reviews):
    if not reviews:
        st.info("No reviews to visualize.")
        return

    st.header("📊 Visualizations")
    sentiment_pie_chart(reviews)
