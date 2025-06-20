import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask.cli import load_dotenv
from services import db_service
import re

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

def extract_keywords(text, min_word_length=os.getenv('KEYWORDS_MIN_LENGTH'), top_n=os.getenv('KEYWORDS_MAX_AMOUNT')):
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

    return filtered

def word_in_db(word: str):
    if db_service.find_word_by_name(word) is not None:
        return True
    else:
        return False

def start_crawl(start_url, depth): #FIXME: test output set
    load_dotenv()
    url = "https://"
    url = url + start_url
    visited_raw = db_service.find_urls_junger_then_one_day_filtered()
    if visited_raw is None:
        visited = set()
    else:
        visited = set(visited_raw) #FIXME: geht net

    crawl(url=url, visited=visited, depth=depth)

def continuous_crawl():
    while True:
        urls = db_service.find_urls_older_then_one_day() #FIXME: test output set

        if urls is not None:
            for url in urls:
                in_url = url[1].split("//")[1]
                start_crawl(in_url, 2)
        else:
            print("Crawler: No urls to crawl")
            time.sleep(10)

def crawl(url, visited, depth=1):
    if depth == 0 or url in visited:
        return
    try:
        db_url = db_service.find_url_by_name(url)
        if db_url is not None:
            db_service.update_url_timestamp(db_url[0][0])
        else:
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
        vis_text = get_visible_text(url)
        keywords = extract_keywords(vis_text, min_word_length=4)

        for word in keywords:
            if word_in_db(word) is not True:
                db_service.add_word(word)

            p_url = db_service.find_url_by_name(url)[0][0]
            p_word = db_service.find_word_by_name(word)

            db_service.add_link(p_word, p_url)


        # Alle Links auf der Seite extrahieren
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            if next_url.startswith("http") or next_url.startswith("https"):
                crawl(next_url, visited, depth - 1)
    except Exception as e:
        print(f"Fehler bei {url}: {e}")

#start_crawl("https://www.youtube.com", 2)