import json
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return 'Ltech Lotto API'

@app.route('/api/v1/lotto/get_total_winnings')
def get_total_winnings():
    with open('total_winnings.json') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


