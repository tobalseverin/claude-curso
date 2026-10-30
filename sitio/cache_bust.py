#!/usr/bin/env python3
"""Add a content hash to every local stylesheet and script link.
Usage: python3 sitio/cache_bust.py <site>
The server caches CSS and JS for years, so a changed file needs a new URL.
"""
import hashlib
import re
import sys
from pathlib import Path

SITE = Path(sys.argv[1]).resolve()
LINK = re.compile(
    r'(<(?:link|script)\b[^>]*?\b(?:href|src)=")([^":?#]+\.(?:css|js))(")'
)


def versioned(page: Path):
    def replace(match: re.Match) -> str:
        path = match[2]
        base = SITE if path.startswith("/") else page.parent
        target = (base / path.lstrip("/")).resolve()
        if not target.is_file():
            return match[0]
        digest = hashlib.sha256(target.read_bytes()).hexdigest()[:10]
        return f"{match[1]}{path}?v={digest}{match[3]}"

    return replace


count = 0
for page in SITE.rglob("*.html"):
    html = page.read_text()
    updated, hits = LINK.subn(versioned(page), html)
    if hits:
        page.write_text(updated)
        count += 1
print(f"Asset links versioned in {count} pages")
