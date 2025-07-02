import json
import os
import re
from typing import List, Dict

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://kaitori.app/"
SEARCH_TERM = "iPhone16"


def fetch_iphone16_prices() -> List[Dict[str, int]]:
    """Fetch iPhone 16 series prices from kaitori.app."""
    try:
        resp = requests.get(BASE_URL, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to fetch {BASE_URL}: {exc}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')

    products = []

    # The actual HTML structure of kaitori.app is unknown in this environment.
    # This implementation searches for any element that contains the text
    # "iPhone16" and attempts to locate a nearby price.
    for elem in soup.find_all(string=re.compile(r"iPhone\s*16", re.I)):
        text = elem.strip()
        parent = elem.parent
        price_elem = parent.find_next(string=re.compile(r"\d+[\,\d]*"))
        if price_elem:
            price_text = re.search(r"\d+[\,\d]*", price_elem).group()
            price = int(price_text.replace(',', ''))
            products.append({"name": text, "price": price})

    return products


def save_products(products: List[Dict[str, int]], path: str) -> None:
    """Save product list to JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(__file__), 'data', 'products.json')
    items = fetch_iphone16_prices()
    save_products(items, data_file)
