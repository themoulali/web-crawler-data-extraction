"""Extract useful fields from HTML documents."""
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from .url_utils import resolve_link

def extract_page(html: str, url: str) -> dict:
    """Parse HTML and return a JSON-serializable record."""
    soup = BeautifulSoup(html or "", "html.parser")

    # Remove non-content elements before collecting visible text.
    for element in soup(["script", "style", "noscript", "svg", "iframe"]):
        element.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    description_tag = soup.find("meta", attrs={"name": lambda value: value and value.lower() == "description"})
    description = description_tag.get("content", "").strip() if description_tag else ""

    headings = []
    for tag in soup.find_all(["h1", "h2", "h3"]):
        heading = tag.get_text(" ", strip=True)
        if heading:
            headings.append(heading)

    text = " ".join(soup.get_text(" ", strip=True).split())
    links = []
    seen_links = set()
    for anchor in soup.find_all("a", href=True):
        resolved = resolve_link(url, anchor.get("href", ""))
        if resolved and resolved not in seen_links:
            seen_links.add(resolved)
            links.append(resolved)

    return {
        "url": url,
        "title": title,
        "description": description,
        "headings": headings,
        "text": text[:10000],
        "links": links,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
