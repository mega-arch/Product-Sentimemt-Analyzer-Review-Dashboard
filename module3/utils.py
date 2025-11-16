def clean_text(text):
    """Basic text cleaning before sentiment analysis."""
    if not isinstance(text, str):
        return ""
    return text.strip()
