from flask import Flask, jsonify
from flask.cli import load_dotenv

from backend.services import search_service
import os
import dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/api/info', methods=['GET'])
def hello():
    return """[
    {"api/info": "returns this info output"}, 
    {"api/search/$search_therm": "outputs all websites containing the $search_therm"}
]"""

@app.route('/api/search/<string:search_term>', methods=['GET'])
def search(search_term: str):
    result = search_service.search_by_therm(search_term)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)