# 🇮🇳 IndicSummarize

> **Paste a URL. Get an English summary. In seconds.**  
> An NLP web application that extracts, translates, and summarizes Indian-language articles automatically.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 What Is This?

**IndicSummarize** is a beginner-friendly NLP web application built with Flask and HuggingFace Transformers. It accepts a URL to any blog or news article written in a supported Indian language, and returns a clean, concise English summary — no manual copy-pasting or translation needed.

---

## ✨ Features

- 🔗 **URL-based input** — just paste a link, no file uploads needed
- 🌐 **Automatic language detection** using `langdetect`
- 🔄 **Neural machine translation** via Facebook's NLLB-200 model
- 📝 **Abstractive summarization** using Facebook's BART-large-CNN model
- 📊 **Word count stats** — original vs summary
- 💻 **Clean Bootstrap UI** with loading indicators
- ⚡ **REST API** — easily integrable with other tools

---

## 🗣️ Supported Languages

| Language   | Script     | Status  |
|------------|------------|---------|
| Hindi      | Devanagari | ✅ Live |
| Gujarati   | Gujarati   | ✅ Live |
| Punjabi    | Gurmukhi   | ✅ Live |
| Tamil      | Tamil      | ✅ Live |
| Telugu     | Telugu     | ✅ Live |
| Malayalam  | Malayalam  | ✅ Live |
| Marathi    | Devanagari | 🔜 Soon |
| Bengali    | Bengali    | 🔜 Soon |
| Kannada    | Kannada    | 🔜 Soon |
| Odia       | Odia       | 🔜 Soon |

> 🌐 We currently support major Indian languages and are **continuously expanding regional language coverage**.

---

## 🧠 NLP Pipeline

```
User URL
   │
   ▼
┌─────────────────────┐
│  1. Scrape Article  │  newspaper3k extracts clean article text
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Detect Language │  langdetect identifies the source language
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Translate → EN  │  facebook/nllb-200-distilled-600M
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. Summarize       │  facebook/bart-large-cnn
└────────┬────────────┘
         │
         ▼
   JSON Response
   (language, word counts, summary)
```

---

## 🗂️ Project Structure

```
indic-summarizer/
│
├── app.py              # Flask application & REST API routes
├── scraper.py          # Article extraction (newspaper3k)
├── translator.py       # Language detection + NLLB translation
├── summarizer.py       # BART summarization
│
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment start command
├── runtime.txt         # Python version pin
│
└── templates/
    └── index.html      # Bootstrap single-page frontend
```

---

## ⚙️ Tech Stack

| Layer          | Technology                              |
|----------------|-----------------------------------------|
| Backend        | Python 3.10, Flask 3.0                  |
| Scraping       | newspaper3k                             |
| Lang Detection | langdetect                              |
| Translation    | HuggingFace · NLLB-200-distilled-600M   |
| Summarization  | HuggingFace · BART-large-CNN            |
| Frontend       | HTML5, Bootstrap 5, Vanilla JS          |
| Deployment     | Gunicorn, Render / HuggingFace Spaces   |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- pip
- ~4 GB free disk space (for model downloads)
- ~4 GB RAM

### 1. Clone the repository

```bash
git clone https://github.com/your-username/indic-summarizer.git
cd indic-summarizer
```

### 2. Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate — macOS/Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

> ⏳ **First launch takes a few minutes** — the NLLB and BART models (~3 GB total) are downloaded from HuggingFace Hub and cached locally. Every subsequent launch is instant.

---

## 📡 API Reference

### `POST /summarize`

Summarizes the article at the given URL.

**Request**
```http
POST /summarize
Content-Type: application/json
```
```json
{
  "url": "https://example.com/hindi-article"
}
```

**Success Response — `200 OK`**
```json
{
  "title": "Article Title Here",
  "detected_language": "Hindi",
  "original_word_count": 430,
  "summary_word_count": 68,
  "summary": "A concise English summary of the article content..."
}
```

**Error Response — `422 Unprocessable Entity`**
```json
{
  "error": "Language 'Unsupported (xx)' is not yet supported. We are continuously expanding regional language coverage."
}
```

---

## ☁️ Deployment

### Option 1 — HuggingFace Spaces *(Recommended — Free)*

HuggingFace Spaces is the best free option for ML apps with large models.

1. Create an account at [huggingface.co](https://huggingface.co)
2. Go to **Spaces → Create new Space**
3. Choose **Docker** as the SDK
4. Upload all project files
5. Your app gets a free public URL like `https://your-username-indic-summarizer.hf.space`

### Option 2 — Render.com

1. Push the project to a GitHub repository
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo and configure:

   | Setting        | Value                                              |
   |----------------|----------------------------------------------------|
   | Build Command  | `pip install -r requirements.txt`                  |
   | Start Command  | `gunicorn app:app --timeout 300 --workers 1`       |
   | Environment    | Python 3                                           |

4. Click **Create Web Service**

> ⚠️ **RAM Note:** The free Render tier provides only 512 MB RAM. NLLB + BART together require ~3–4 GB. Use the **Starter plan ($7/mo)** or switch to lighter models (see below).

### Option 3 — Google Colab + ngrok *(Great for demos)*

Ideal for academic presentations with zero hosting cost.

```python
# In a Colab cell:
!pip install flask pyngrok -q
from pyngrok import ngrok
ngrok.set_auth_token("YOUR_NGROK_TOKEN")
public_url = ngrok.connect(5000)
print("Live URL:", public_url)
!python app.py
```

---

## 🔧 Extending the App

### Adding a new language

Open `translator.py` and add one line to `LANGUAGE_MAP`:

```python
LANGUAGE_MAP = {
    "hi": ("Hindi",   "hin_Deva"),
    "mr": ("Marathi", "mar_Deva"),   # ← add this
    "bn": ("Bengali", "ben_Beng"),   # ← add this
    # ...
}
```

That's it. No other changes needed anywhere.

### Switching to lighter models (low-RAM environments)

In `translator.py`, replace the model name:
```python
# Heavy (default)
model="facebook/nllb-200-distilled-600M"

# Light alternative (per-language, ~300 MB each)
model="Helsinki-NLP/opus-mt-hi-en"   # Hindi → English only
```

In `summarizer.py`, replace the model name:
```python
# Heavy (default)
model="facebook/bart-large-cnn"

# Light alternative (~half the size)
model="sshleifer/distilbart-cnn-12-6"
```

---

## 📋 Requirements

```
flask==3.0.3
newspaper3k==0.2.8
lxml_html_clean==0.4.1
langdetect==1.0.9
transformers==4.41.2
torch==2.3.1
sentencepiece==0.2.0
sacremoses==0.1.1
gunicorn==22.0.0
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `No article text extracted` | The site may block scrapers. Try a different article URL. |
| `Language 'unknown' not supported` | Article text too short for detection. Try a longer article. |
| App crashes on startup | Not enough RAM — need at least 4 GB free. |
| Slow first response | Models loading for the first time (~60 sec). Subsequent calls are fast. |
| `lxml` import error | Run `pip install lxml_html_clean` separately. |
| `sentencepiece` not found | Run `pip install sentencepiece sacremoses`. |

---

## 🎓 Academic Notes

This project demonstrates a complete **transfer learning NLP pipeline** using only pretrained models — no custom training required:

- **Extraction:** Rule-based DOM parsing (newspaper3k)
- **Detection:** Statistical n-gram language model (langdetect)
- **Translation:** Encoder-decoder transformer — NLLB-200 (Meta AI, 2022)
- **Summarization:** Fine-tuned sequence-to-sequence model — BART (Lewis et al., 2019)

### References

- Lewis et al. (2019). *BART: Denoising Sequence-to-Sequence Pre-training.* [arXiv:1910.13461](https://arxiv.org/abs/1910.13461)
- NLLB Team (2022). *No Language Left Behind.* [arXiv:2207.04672](https://arxiv.org/abs/2207.04672)
- [newspaper3k Documentation](https://newspaper.readthedocs.io/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  Built with ❤️ using Flask &amp; HuggingFace 🤗 &nbsp;|&nbsp; Supporting Indian languages, one summary at a time.
</div>
