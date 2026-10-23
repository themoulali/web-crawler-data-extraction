import csv
import json
import tempfile
import unittest
from pathlib import Path
from web_crawler.exporter import export_csv, export_json

class ExporterTests(unittest.TestCase):
    def setUp(self):
        self.records = [{
            "url": "https://example.com",
            "title": "Example",
            "description": "Demo",
            "headings": ["Hello", "World"],
            "text": "Example page",
            "links": ["https://example.com/about"],
            "fetched_at": "2026-01-01T00:00:00+00:00",
        }]

    def test_exports_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_json(self.records, Path(tmp) / "nested" / "data.json")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), self.records)

    def test_exports_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = export_csv(self.records, Path(tmp) / "data.csv")
            with path.open(encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(rows[0]["title"], "Example")
            self.assertEqual(rows[0]["headings"], "Hello | World")

if __name__ == "__main__":
    unittest.main()
