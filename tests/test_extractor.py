import unittest
from web_crawler.extractor import extract_page

class ExtractorTests(unittest.TestCase):
    def test_extracts_metadata_headings_text_and_links(self):
        html = """
        <html><head><title>Demo Page</title>
        <meta name="description" content="A useful demo"></head>
        <body><h1>Welcome</h1><h2>Details</h2><p>Hello crawler.</p>
        <a href="/next">Next</a><a href="/next#top">Duplicate link</a>
        <script>secret = 'do not include';</script></body></html>
        """
        record = extract_page(html, "https://example.com/")
        self.assertEqual(record["title"], "Demo Page")
        self.assertEqual(record["description"], "A useful demo")
        self.assertEqual(record["headings"], ["Welcome", "Details"])
        self.assertIn("Hello crawler.", record["text"])
        self.assertNotIn("do not include", record["text"])
        self.assertEqual(record["links"], ["https://example.com/next"])

if __name__ == "__main__":
    unittest.main()
