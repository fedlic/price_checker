from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Path to the JSON data file
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'products.json')


def load_products():
    """Load product data from the JSON file."""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    products = load_products()
    results = []
    if query:
        for product in products:
            if query in product['name'].lower():
                results.append(product)
    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
