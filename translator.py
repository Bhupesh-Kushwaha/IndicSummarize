from langdetect import detect, LangDetectException
from transformers import pipeline

# NLLB language code mapping
# langdetect code -> NLLB flores200 code
LANGUAGE_MAP = {
    "hi": ("Hindi",        "hin_Deva"),
    "gu": ("Gujarati",     "guj_Gujr"),
    "pa": ("Punjabi",      "pan_Guru"),
    "ta": ("Tamil",        "tam_Taml"),
    "te": ("Telugu",       "tel_Telu"),
    "ml": ("Malayalam",    "mal_Mlym"),
}

TARGET_LANG = "eng_Latn"

# Lazy-load the translation pipeline (loaded once on first call)
_translator = None

def _get_translator():
    global _translator
    if _translator is None:
        print("Loading translation model (facebook/nllb-200-distilled-600M)...")
        _translator = pipeline(
            "translation",
            model="facebook/nllb-200-distilled-600M",
            device=-1,          # CPU; change to 0 for GPU
            max_length=1024,
        )
    return _translator


def detect_language(text: str) -> str:
    """Return the ISO 639-1 language code of the given text."""
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


def translate_to_english(text: str, max_chars: int = 3000) -> dict:
    """
    Detect the language of `text`, translate it to English using NLLB,
    and return a result dict.

    Returns:
        {
          "lang_code":   str,   # detected ISO code
          "lang_name":   str,   # human-readable name
          "english_text": str,  # translated English text
          "supported":   bool,  # whether language is in LANGUAGE_MAP
        }
    """
    lang_code = detect_language(text)
    lang_info  = LANGUAGE_MAP.get(lang_code)

    if lang_info is None:
        return {
            "lang_code": lang_code,
            "lang_name": f"Unsupported ({lang_code})",
            "english_text": None,
            "supported": False,
        }

    lang_name, src_nllb = lang_info

    # Truncate very long texts to stay within model limits
    truncated = text[:max_chars]

    translator = _get_translator()
    result = translator(
        truncated,
        src_lang=src_nllb,
        tgt_lang=TARGET_LANG,
    )

    english_text = result[0]["translation_text"]

    return {
        "lang_code":    lang_code,
        "lang_name":    lang_name,
        "english_text": english_text,
        "supported":    True,
    }
