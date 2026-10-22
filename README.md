# Price Checker

A small, read-only Flask application for searching a local buyback-price catalog.

The included records in `data/products.json` are sample data, not current market quotes. Edit that file through a reviewed data-update process when prices change; the app does not scrape or overwrite it automatically.

## Setup

Python 3.9 or newer is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000/> and search by product name.

## Product data

`data/products.json` must contain an array of objects with a non-empty `name` and a non-negative numeric `price` in yen:

```json
[{"name": "Example product", "price": 1000}]
```

Invalid or unreadable data is rejected rather than partially displayed.

## Tests

```bash
python -m unittest discover -s tests -v
```
