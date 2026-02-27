# Supported Indian languages: langdetect code -> (display name, NLLB flores200 code)
LANGUAGE_MAP = {
    "hi": ("Hindi",     "hin_Deva"),
    "gu": ("Gujarati",  "guj_Gujr"),
    "pa": ("Punjabi",   "pan_Guru"),
    "ta": ("Tamil",     "tam_Taml"),
    "te": ("Telugu",    "tel_Telu"),
    "ml": ("Malayalam", "mal_Mlym"),
}

TARGET_LANG   = "eng_Latn"
MAX_CHARS     = 3000          # safe limit for NLLB-600M
_pipeline     = None          # loaded once, reused


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        try:
            from transformers import pipeline as hf_pipeline
        except ImportError:
            raise RuntimeError(
                "transformers is not installed. Run: pip install transformers torch sentencepiece"
            )
        print("[translator] Loading NLLB model (first time only — may take a minute)...")
        _pipeline = hf_pipeline(
            "translation",
            model="facebook/nllb-200-distilled-600M",
            device=-1,        # CPU; set to 0 for GPU
            max_length=1024,
        )
        print("[translator] NLLB model ready.")
    return _pipeline


def detect_language(text: str) -> str:
    """Return ISO 639-1 language code, or 'unknown' on failure."""
    try:
        from langdetect import detect, LangDetectException
        return detect(text)
    except Exception:
        return "unknown"


def translate_to_english(text: str) -> dict:
    """
    Detect language and translate to English via NLLB-200.

    Returns:
        {
          "lang_code":    str,   # ISO 639-1 code detected
          "lang_name":    str,   # Human-readable name
          "english_text": str | None,
          "supported":    bool,
        }
    """
    lang_code = detect_language(text)
    lang_info = LANGUAGE_MAP.get(lang_code)

    if lang_info is None:
        return {
            "lang_code":    lang_code,
            "lang_name":    f"Unsupported ({lang_code})",
            "english_text": None,
            "supported":    False,
        }

    lang_name, src_nllb = lang_info
    truncated           = text[:MAX_CHARS]

    pipe   = _get_pipeline()
    result = pipe(truncated, src_lang=src_nllb, tgt_lang=TARGET_LANG)

    return {
        "lang_code":    lang_code,
        "lang_name":    lang_name,
        "english_text": result[0]["translation_text"],
        "supported":    True,
    }
