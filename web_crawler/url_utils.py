"""URL normalization and filtering helpers."""
from urllib.parse import urljoin, urlparse, urldefrag, urlunparse

def normalize_url(url: str) -> str:
    """Normalize a URL for deduplication: remove fragments and common tracking parameters."""
    if not isinstance(url, str) or not url.strip():
        return ""
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    parts = urlparse(url)
    if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
        return ""
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    path = parts.path or "/"
    # Remove a trailing slash except for the root path.
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    tracking_prefixes = ("utm_",)
    tracking_names = {"fbclid", "gclid", "mc_cid", "mc_eid"}
    kept = []
    for pair in parts.query.split("&") if parts.query else []:
        key = pair.split("=", 1)[0].lower()
        if key in tracking_names or any(key.startswith(prefix) for prefix in tracking_prefixes):
            continue
        kept.append(pair)
    query = "&".join(kept)
    return urlunparse((scheme, netloc, path, "", query, ""))

def resolve_link(base_url: str, href: str) -> str:
    """Resolve a relative href against its page and return a normalized HTTP(S) URL."""
    if not href:
        return ""
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return ""
    return normalize_url(urljoin(base_url, href))

def same_domain(url_a: str, url_b: str) -> bool:
    """Compare hostnames, treating www.example.com and example.com as the same domain."""
    a = (urlparse(url_a).hostname or "").lower()
    b = (urlparse(url_b).hostname or "").lower()
    if a.startswith("www."):
        a = a[4:]
    if b.startswith("www."):
        b = b[4:]
    return bool(a and b and a == b)
