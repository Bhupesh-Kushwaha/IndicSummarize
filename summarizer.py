MAX_INPUT_CHARS = 3000   # BART-large-CNN token limit ~1024 tokens ≈ 3000 chars
_pipeline       = None   # loaded once, reused


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        try:
            from transformers import pipeline as hf_pipeline
        except ImportError:
            raise RuntimeError(
                "transformers is not installed. Run: pip install transformers torch"
            )
        print("[summarizer] Loading BART model (first time only — may take a minute)...")
        _pipeline = hf_pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1,   # CPU; set to 0 for GPU
        )
        print("[summarizer] BART model ready.")
    return _pipeline


def summarize_english(text: str) -> str:
    """
    Generate a concise English summary using BART-large-CNN.
    Truncates input to MAX_INPUT_CHARS to stay within model limits.
    """
    if not text or not text.strip():
        raise ValueError("No text provided for summarization.")

    truncated  = text[:MAX_INPUT_CHARS]
    word_count = len(truncated.split())

    # Dynamic length — summary is ~25–30% of input
    max_len = min(200, max(60, word_count // 3))
    min_len = max(30, min_len := max_len - 20)

    pipe   = _get_pipeline()
    result = pipe(truncated, max_length=max_len, min_length=min_len, do_sample=False)
    return result[0]["summary_text"]
