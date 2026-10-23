"""Polite, bounded crawler with robots.txt checks and duplicate prevention."""
from collections import deque
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import logging
import time
import requests

from .extractor import extract_page
from .url_utils import normalize_url, same_domain

USER_AGENT = "Week4LearningCrawler/1.0 (+educational project; contact: student@example.com)"

class WebCrawler:
    def __init__(self, max_pages=10, delay=1.0, timeout=10, allow_external=False, session=None):
        if max_pages < 1:
            raise ValueError("max_pages must be at least 1")
        if delay < 0:
            raise ValueError("delay cannot be negative")
        if timeout <= 0:
            raise ValueError("timeout must be greater than 0")
        self.max_pages = max_pages
        self.delay = delay
        self.timeout = timeout
        self.allow_external = allow_external
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
        self.visited = set()
        self.records = []
        self._robots_cache = {}
        self.logger = logging.getLogger("web_crawler")

    def _robots_allowed(self, url: str) -> bool:
        parts = urlparse(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in self._robots_cache:
            parser = RobotFileParser()
            parser.set_url(f"{origin}/robots.txt")
            try:
                response = self.session.get(parser.url, timeout=self.timeout)
                if response.status_code == 404:
                    parser.parse([])
                elif response.ok:
                    parser.parse(response.text.splitlines())
                else:
                    # Fail closed on other robots.txt errors.
                    parser.parse(["User-agent: *", "Disallow: /"])
            except requests.RequestException as exc:
                self.logger.warning("Could not read robots.txt for %s: %s", origin, exc)
                parser.parse(["User-agent: *", "Disallow: /"])
            self._robots_cache[origin] = parser
        return self._robots_cache[origin].can_fetch(USER_AGENT, url)

    def crawl(self, start_url: str) -> list[dict]:
        start_url = normalize_url(start_url)
        if not start_url:
            raise ValueError("Please provide a valid http:// or https:// URL")
        queue = deque([start_url])
        queued = {start_url}

        while queue and len(self.records) < self.max_pages:
            url = queue.popleft()
            if url in self.visited:
                continue
            self.visited.add(url)

            if not self.allow_external and not same_domain(start_url, url):
                continue
            if not self._robots_allowed(url):
                self.logger.info("Skipped by robots.txt: %s", url)
                continue

            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "").lower()
                if content_type and "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                    self.logger.info("Skipped non-HTML response: %s (%s)", url, content_type)
                    continue
                record = extract_page(response.text, url)
                self.records.append(record)
                self.logger.info("Fetched %s", url)

                for link in record["links"]:
                    if link not in queued and link not in self.visited:
                        if self.allow_external or same_domain(start_url, link):
                            queue.append(link)
                            queued.add(link)
            except requests.RequestException as exc:
                self.logger.warning("Failed to fetch %s: %s", url, exc)
            except Exception:
                self.logger.exception("Unexpected error while processing %s", url)

            if queue and self.delay:
                time.sleep(self.delay)

        return self.records
