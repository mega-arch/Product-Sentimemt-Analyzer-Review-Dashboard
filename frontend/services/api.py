import requests
import unicodedata

BASE_URL = "http://127.0.0.1:5000"

def normalize_query(query: str) -> str:
    """Normalize search query to remove weird unicode characters."""
    return unicodedata.normalize("NFKD", query).replace("\xa0", " ").strip()

def safe_get(url, params=None):
    """Perform a GET request safely and return JSON or error."""
    try:
        response = requests.get(url, params=params)
        print("\n--- API CALL DEBUG ---")
        print("URL:", response.url)
        print("Status:", response.status_code)
        print("Response text:", response.text)

        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}: {response.text}"}

        try:
            return response.json()
        except:
            return {"error": "Backend did not return valid JSON."}

    except Exception as e:
        return {"error": f"Request failed: {e}"}

# -----------------------------
# PRODUCT APIs
# -----------------------------
def search_product(query: str):
    query = normalize_query(query)
    response = safe_get(f"{BASE_URL}/search_products", {"keyword": query})
    products = response.get("products", [])
    # normalize key names
    for p in products:
        if "id" in p and "product_id" not in p:
            p["product_id"] = p["id"]
    return response

# -----------------------------
# REVIEW APIs
# -----------------------------
def get_reviews(product_id):
    return safe_get(f"{BASE_URL}/search_reviews", {"product_id": product_id})

def compute_sentiment_summary(reviews):
    summary = {"positive": 0, "neutral": 0, "negative": 0}
    for r in reviews:
        sentiment = r.get("sentiment_label", "neutral")
        summary[sentiment] += 1
    return summary

def compute_sentiment_summary(reviews):
    summary = {"positive": 0, "neutral": 0, "negative": 0}
    for r in reviews:
        # normalize sentiment to lowercase
        sentiment = r.get("sentiment_label", "neutral")
        if sentiment is None:
            sentiment = "neutral"
        sentiment = sentiment.lower()
        if sentiment in summary:
            summary[sentiment] += 1
        else:
            summary["neutral"] += 1  # fallback
    return summary


def compute_statistics(reviews):
    total = len(reviews)
    summary = compute_sentiment_summary(reviews)

    stats = {
        "total_reviews": total,
        "positive_percent": round((summary["positive"] / total) * 100, 2) if total else 0,
        "negative_percent": round((summary["negative"] / total) * 100, 2) if total else 0,
        "neutral_percent": round((summary["neutral"] / total) * 100, 2) if total else 0
    }
    return stats
