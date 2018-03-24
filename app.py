
import logging
import sys

from flask import Flask, jsonify, render_template, request, abort
from flask_cors import CORS

from spam_utils import ham_or_spam

app = Flask(__name__)

CORS(app)

app.config['CACHE_TYPE'] = 'simple'
# http://127.0.0.1:5000/api/classify/
# for debugging purposes
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# REST API
@app.route('/api/classify', methods=['POST'])
@app.route('/api/classify/', methods=['POST'])
def classify_spam():
    if not request.json or not 'input_text' in request.json:
        abort(400)

    input_class = ham_or_spam(request.json['input_text'])["category"]
    json_data = {
        'status': 200,
        'input_text': request.json['input_text'],
        'input_class': input_class
    }

    return jsonify(json_data), 200


if __name__ == "__main__":
    app.run()
