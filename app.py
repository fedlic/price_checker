from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load product data once at startup
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'products.json')
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    PRODUCTS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    if query:
        for product in PRODUCTS:
            if query in product['name'].lower():
                results.append(product)
    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
