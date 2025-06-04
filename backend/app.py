from flask import Flask, jsonify
from backend.services import search_service

app = Flask(__name__)

@app.route('/api/info', methods=['GET'])
def hello():
    return """[
    {"api/info": "returns this info output"}, 
    {"api/search/$search_therm": "outputs all websites containing the $search_therm"}
]"""

@app.route('/api/search/<string:search_term>', methods=['GET'])
def search(search_term: str):
    return search_service.search_urls_by_therm(search_term)

if __name__ == '__main__':
    app.run(debug=True)