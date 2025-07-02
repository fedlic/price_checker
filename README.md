# Price Checker

This is a simple Flask web application to search buyback prices for products.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Open your browser at [http://localhost:5000](http://localhost:5000) to search for products.

The data is stored in `data/products.json`. You can modify this file to change or add products.

## Scraping iPhone 16 Prices

Use the scraper to fetch the latest iPhone 16 series buyback prices from [kaitori.app](https://kaitori.app/).
This overwrites `data/products.json` with the fetched data.

```bash
python scraper.py
```
