"""Small read-only price search application."""

import json
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "data" / "products.json"
MAX_QUERY_LENGTH = 100


def load_products(path=DATA_FILE):
    """Load and validate the local product catalog."""
    with Path(path).open(encoding="utf-8") as source:
        products = json.load(source)
    if not isinstance(products, list):
        raise ValueError("Product catalog must be a JSON array")

    validated = []
    for index, product in enumerate(products):
        if not isinstance(product, dict):
            raise ValueError(f"Product {index} must be an object")
        name = product.get("name")
        price = product.get("price")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Product {index} has an invalid name")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError(f"Product {index} has an invalid price")
        validated.append({"name": name.strip(), "price": price})
    return validated


@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'; form-action 'self'; base-uri 'none'"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/")
def index():
    return render_template("index.html", max_query_length=MAX_QUERY_LENGTH)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()[:MAX_QUERY_LENGTH]
    results = []
    error = None
    if query:
        try:
            normalized_query = query.casefold()
            results = [
                product
                for product in load_products()
                if normalized_query in product["name"].casefold()
            ]
        except (OSError, json.JSONDecodeError, ValueError):
            app.logger.exception("Could not load the product catalog")
            error = "商品データを読み込めませんでした。管理者にお問い合わせください。"
    return render_template("results.html", query=query, results=results, error=error), (503 if error else 200)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
