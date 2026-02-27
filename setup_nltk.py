#!/usr/bin/env python3
"""
Run this once before starting the app, or add it to your build command.
Downloads NLTK corpora required by newspaper3k.
"""
import nltk

packages = ["punkt", "punkt_tab", "stopwords"]
for pkg in packages:
    print(f"Downloading NLTK package: {pkg}")
    nltk.download(pkg, quiet=False)

print("\nAll NLTK packages downloaded. You can now run: python app.py")
