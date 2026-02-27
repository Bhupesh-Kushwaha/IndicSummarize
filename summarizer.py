from transformers import pipeline

# Lazy-load the summarization pipeline
_summarizer = None

# BART token limit is 1024; keep input safe
MAX_INPUT_CHARS = 3000


def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        print("Loading summarization model (facebook/bart-large-cnn)...")
        _summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1,   # CPU; change to 0 for GPU
        )
    return _summarizer


def summarize_english(text: str) -> str:
    """
    Generate a concise English summary of the given English text.
    Handles long texts by truncating to MAX_INPUT_CHARS.
    """
    if not text or not text.strip():
        raise ValueError("No text provided for summarization.")

    # Truncate to model's safe limit
    truncated = text[:MAX_INPUT_CHARS]

    word_count = len(truncated.split())

    # Dynamically set min/max length based on input size
    max_len = min(200, max(50, word_count // 3))
    min_len = min(50, max_len - 10)

    summarizer = _get_summarizer()
    result = summarizer(
        truncated,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
    )

    return result[0]["summary_text"]
