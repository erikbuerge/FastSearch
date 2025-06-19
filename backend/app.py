from crypt import methods

from flask import Flask, jsonify
from flask.cli import load_dotenv

from backend.services import search_service
from backend.services import url_title_service
from backend import crawler
import os
import dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/api/info', methods=['GET'])
def hello():
    return """[
    {"api/info": "returns this info output"}, 
    {"api/search/$search_therm": "outputs all websites containing the $search_therm"}
]"""

@app.route('/api/search/<string:search_term>', methods=['GET'])
def search(search_term: str):
    result = search_service.search_by_therm(search_term)
    if result == "Search term not found" or result == "No URLs for the search term":
        return jsonify(result)
    else:
        urls_with_title = url_title_service.get_titles_from_urls(result)
        return jsonify(urls_with_title)

@app.route('/api/crawler/<string:url>', methods=['GET'])
def start_crawler(url: str):
    crawler.start_crawl(url, 4)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)