from newspaper import Article

def extract_article_text(url: str) -> dict:
    """
    Extract main article text from a given URL using newspaper3k.
    Returns a dict with 'text' and 'title' keys, or raises an exception.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text.strip()
        title = article.title.strip() if article.title else "Untitled"

        if not text:
            raise ValueError("No article text could be extracted from the provided URL.")

        return {"title": title, "text": text}

    except Exception as e:
        raise RuntimeError(f"Failed to extract article: {str(e)}")
