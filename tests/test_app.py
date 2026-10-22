import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import app, load_products


class CatalogTests(unittest.TestCase):
    def write_catalog(self, value):
        temporary = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
        with temporary:
            json.dump(value, temporary)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        return temporary.name

    def test_valid_catalog_is_loaded(self):
        path = self.write_catalog([{"name": " Product ", "price": 100}])
        self.assertEqual(load_products(path), [{"name": "Product", "price": 100}])

    def test_invalid_catalog_is_rejected(self):
        path = self.write_catalog([{"name": "Product", "price": -1}])
        with self.assertRaises(ValueError):
            load_products(path)


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_search_is_case_insensitive(self):
        with patch("app.load_products", return_value=[{"name": "iPhone 12", "price": 400}]):
            response = self.client.get("/search?q=IPHONE")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"iPhone 12", response.data)

    def test_bad_catalog_returns_503(self):
        with patch("app.load_products", side_effect=ValueError("bad data")):
            response = self.client.get("/search?q=phone")
        self.assertEqual(response.status_code, 503)
        self.assertIn("Content-Security-Policy", response.headers)

    def test_template_escapes_query(self):
        response = self.client.get("/search?q=%3Cscript%3Ealert(1)%3C/script%3E")
        self.assertNotIn(b"<script>alert", response.data)
        self.assertIn(b"&lt;script&gt;", response.data)


if __name__ == "__main__":
    unittest.main()
