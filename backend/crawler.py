import os
import dotenv

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from flask.cli import load_dotenv

from backend.services import db_service
import re
from collections import Counter

load_dotenv()
start_url = os.getenv('CRAWLER_START_URL')
visited = set(db_service.find_urls_junger_then_one_day())

def get_visible_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Entferne Script- und Style-Tags
        for script in soup(["script", "style", "noscript"]):
            script.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text
    except Exception as e:
        print(f"Fehler bei {url}: {e}")
        return ""

def extract_keywords(text, min_word_length=4, top_n=20):
    # Nur Wörter, mind. 4 Zeichen lang
    words = re.findall(r'\b[a-zA-ZäöüÄÖÜß]{%d,}\b' % min_word_length, text.lower())

    # Optional: Stopwörter ausschließen (z. B. mit nltk oder eigener Liste)
    stopwords = {
        "and", "the", "of", "to", "einer", "eine", "eines", "einem", "einen", "der",
        "die", "das", "dass", "daß", "du", "er", "sie", "es", "was", "wer", "wie",
        "wir", "und", "oder", "ohne", "mit", "am", "im", "in", "aus", "auf", "ist",
        "sein", "war", "wird", "ihr", "ihre", "ihres", "ihnen", "ihrer", "als", "für",
        "von", "mit", "dich", "dir", "mich", "mir", "mein", "sein", "kein", "durch",
        "wegen", "wird", "sich", "bei", "beim", "noch", "den", "dem", "zu", "zur",
        "zum", "auf", "ein", "auch", "werden", "an", "des", "sein", "sind", "vor",
        "nicht", "sehr", "um", "unsere", "ohne", "so", "da", "nur", "diese", "dieser",
        "diesem", "dieses", "nach", "über", "mehr", "hat", "bis", "uns", "unser",
        "unserer", "unserem", "unsers", "euch", "euers", "euer", "eurem", "ihr",
        "ihres", "ihrer", "ihrem", "alle", "vom"
    }
    filtered = [w for w in words if w not in stopwords]

    return Counter(filtered).most_common(top_n)

def word_in_db(word: str):
    if db_service.find_word_by_name(word) is not None:
        return True
    else:
        return False

def crawl(url, depth=1):
    if depth == 0 or url in visited:
        return
    try:
        db_service.add_url(url)
    except Exception as e:
        print(f"Fehler beim einfügen in die Datenbank von {url}: {e}")

    print(f"Crawling: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Text magic
        keywords = extract_keywords(get_visible_text(url), min_word_length=4)

        for word in keywords:
            if word_in_db(word[0]) is not True:
                db_service.add_word(word[0])

                p_url = db_service.find_url_by_name(url)
                p_word = db_service.find_word_by_name(word[0])

                db_service.add_link(p_word, p_url[0][0])

        # Alle Links auf der Seite extrahieren
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            if next_url.startswith("http"):
                crawl(next_url, depth - 1)
    except Exception as e:
        print(f"Fehler bei {url}: {e}")


# Starten
crawl(start_url, depth=int(os.getenv('CRAWLER_DEPTH')))  # Tiefe begrenzen, um Rekursion & Last zu kontrollieren