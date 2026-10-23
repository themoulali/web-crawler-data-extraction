import unittest
from web_crawler.url_utils import normalize_url, resolve_link, same_domain

class URLUtilsTests(unittest.TestCase):
    def test_normalize_removes_fragment_and_tracking(self):
        self.assertEqual(
            normalize_url("HTTPS://Example.COM/page/?utm_source=x&keep=yes#section"),
            "https://example.com/page?keep=yes",
        )

    def test_rejects_non_http_urls(self):
        self.assertEqual(normalize_url("mailto:test@example.com"), "")

    def test_resolves_relative_link(self):
        self.assertEqual(resolve_link("https://example.com/docs/start", "../about"), "https://example.com/about")

    def test_same_domain_ignores_www(self):
        self.assertTrue(same_domain("https://www.example.com/a", "https://example.com/b"))
        self.assertFalse(same_domain("https://example.com", "https://other.com"))

if __name__ == "__main__":
    unittest.main()
