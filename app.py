import traceback
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


# ── Always return JSON on errors (never HTML) ─────────────────────────────────
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def handle_error(e):
    return jsonify({"error": str(e)}), e.code


# ── Lazy imports — loaded only when first request hits /summarize ─────────────
# This prevents a crash at startup if a package is partially installed.
_scraper     = None
_translator  = None
_summarizer  = None

def get_modules():
    global _scraper, _translator, _summarizer
    if _scraper is None:
        from scraper     import extract_article_text
        from translator  import translate_to_english
        from summarizer  import summarize_english
        _scraper    = extract_article_text
        _translator = translate_to_english
        _summarizer = summarize_english
    return _scraper, _translator, _summarizer


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    # Load modules (catches import errors and returns JSON, not HTML)
    try:
        extract_article_text, translate_to_english, summarize_english = get_modules()
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server setup error: {str(e)}"}), 500

    # Parse request body
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON with a 'url' field."}), 400

    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided."}), 400
    if not url.startswith("http"):
        return jsonify({"error": "Please enter a valid URL starting with http:// or https://"}), 400

    # Step 1 — Scrape
    try:
        article = extract_article_text(url)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Could not extract article: {str(e)}"}), 422

    original_text       = article["text"]
    original_word_count = len(original_text.split())

    # Step 2 — Detect + Translate
    try:
        translation = translate_to_english(original_text)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

    if not translation["supported"]:
        return jsonify({
            "error": (
                f"Language '{translation['lang_name']}' is not yet supported. "
                "We are continuously expanding regional language coverage."
            )
        }), 422

    english_text = translation["english_text"]

    # Step 3 — Summarize
    try:
        summary = summarize_english(english_text)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Summarization failed: {str(e)}"}), 500

    return jsonify({
        "title":               article["title"],
        "detected_language":   translation["lang_name"],
        "original_word_count": original_word_count,
        "summary_word_count":  len(summary.split()),
        "summary":             summary,
    })


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
