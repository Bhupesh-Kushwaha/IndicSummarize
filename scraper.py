def extract_article_text(url: str) -> dict:
    """
    Extract main article text from a URL using newspaper3k.
    Returns {"title": str, "text": str}
    """
    try:
        from newspaper import Article
    except ImportError:
        raise RuntimeError(
            "newspaper3k is not installed. Run: pip install newspaper3k lxml_html_clean"
        )

    try:
        article = Article(url)
        article.download()
        article.parse()

        text  = article.text.strip()
        title = (article.title or "Untitled").strip()

        if not text:
            raise ValueError(
                "No article text could be extracted. "
                "The page may require JavaScript or block scrapers."
            )

        return {"title": title, "text": text}

    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to fetch article: {str(e)}")
