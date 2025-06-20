import threading

from flask import Flask, jsonify
from flask.cli import load_dotenv

from services import url_title_service, search_service
import crawler
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
    thread = threading.Thread(target=crawler.start_crawl, args=(url, 4))
    thread.start()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    #crawler.continuous_crawl()
    #app.run(debug=True)

    # Thread für die Flask-App
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()

    # Thread für den Crawler
    crawler_thread = threading.Thread(target=crawler.continuous_crawl())
    crawler_thread.start()