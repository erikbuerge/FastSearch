import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)


def url_with_www(url):
    if not url or not isinstance(url, str):
        return "Invalid URL"

    parsed = urlparse(url)
    netloc = parsed.netloc

    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc

    return f"{parsed.scheme}://{netloc}{parsed.path}"


def get_titles_from_urls(urls):
    titles = {}
    valid_urls = [url for url in urls if url and isinstance(url, str)]

    for url in valid_urls:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            if soup.title and soup.title.string.strip():
                title = soup.title.string.strip()
            else:
                title = url_with_www(url)

        except Exception as e:
            logging.error(f"Error with url {url}: {e}")
            title = url_with_www(url)

        titles[url] = title

    return titles
