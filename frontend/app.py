import streamlit as st
import unicodedata

from services.api import (
    search_product,
    get_reviews,
    compute_sentiment_summary,
    compute_statistics
)

from visualization import visualize_reviews  # ← Added visualization import

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")
st.title("📊 Sentiment Analysis Dashboard")
st.header("🔎 Search Product")

query = st.text_input("Enter product name")

if st.button("Search"):
    if not query.strip():
        st.warning("Enter a product name.")
        st.stop()

    # Normalize input
    normalized_query = unicodedata.normalize("NFKD", query).replace("\xa0", " ").strip()

    # Search products
    product_response = search_product(normalized_query)

    if "error" in product_response:
        st.error(product_response["error"])
        st.stop()

    products = product_response.get("products", [])

    if not products:
        st.error("❌ No product found.")
        st.stop()

    # Take the first product
    product = products[0]
    product_id = product.get("product_id") or product.get("id")

    if not product_id:
        st.error("❌ Product ID not found.")
        st.stop()

    st.success(f"Found product: {product.get('product_name', 'Unknown')} (ID: {product_id})")

    # -------------------------------
    # Get Reviews
    reviews_response = get_reviews(product_id)

    if "error" in reviews_response:
        st.error(reviews_response["error"])
        st.stop()

    reviews = reviews_response.get("reviews", [])

    # -------------------------------
    # Sentiment Summary
    sentiment = compute_sentiment_summary(reviews)

    st.header("🧠 Sentiment Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("😊 Positive", sentiment.get("positive", 0))
    col2.metric("😐 Neutral", sentiment.get("neutral", 0))
    col3.metric("😞 Negative", sentiment.get("negative", 0))

    # -------------------------------
    # Review Statistics
    stats = compute_statistics(reviews)

    st.header("📊 Review Statistics")
    colA, colB, colC = st.columns(3)
    colA.metric("📝 Total Reviews", stats.get("total_reviews", 0))
    colB.metric("📈 Positive %", f"{stats.get('positive_percent', 0)}%")
    colC.metric("📉 Negative %", f"{stats.get('negative_percent', 0)}%")

    # -------------------------------
    # 🔥 Visualizations Section
    visualize_reviews(reviews)

    # -------------------------------
    # Customer Reviews Section
    st.header("📝 Customer Reviews")

    if not reviews:
        st.info("No reviews available.")
    else:
        for r in reviews:
            sentiment_label = r.get("sentiment_label", "neutral").lower()
            color = (
                "#a7f3d0" if sentiment_label == "positive"
                else "#fef3c7" if sentiment_label == "neutral"
                else "#fecaca"
            )
            st.markdown(
                f"""
                <div style='padding:10px;margin-bottom:10px;border-radius:8px;
                background:{color}; font-size:14px;'>
                    <b>{sentiment_label.upper()}</b><br>
                    {r.get("raw_review", "")}
                </div>
                """,
                unsafe_allow_html=True
            )
