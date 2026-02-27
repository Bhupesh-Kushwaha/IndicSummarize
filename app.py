from flask import Flask, request, jsonify, render_template

from scraper import extract_article_text
from translator import translate_to_english
from summarizer import summarize_english

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    # ── Step 1: Scrape article ────────────────────────────────────────────────
    try:
        article = extract_article_text(url)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 422

    original_text = article["text"]
    original_word_count = len(original_text.split())

    # ── Step 2: Detect language + translate to English ────────────────────────
    translation = translate_to_english(original_text)

    if not translation["supported"]:
        return jsonify({
            "error": (
                f"Language '{translation['lang_name']}' is not yet supported. "
                "We are continuously expanding regional language coverage."
            )
        }), 422

    english_text = translation["english_text"]

    # ── Step 3: Summarize ─────────────────────────────────────────────────────
    try:
        summary = summarize_english(english_text)
    except Exception as e:
        return jsonify({"error": f"Summarization failed: {str(e)}"}), 500

    summary_word_count = len(summary.split())

    return jsonify({
        "title":               article["title"],
        "detected_language":   translation["lang_name"],
        "original_word_count": original_word_count,
        "summary_word_count":  summary_word_count,
        "summary":             summary,
    })


if __name__ == "__main__":
    app.run(debug=True)
