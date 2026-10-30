#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["markdown==3.7", "beautifulsoup4==4.12.3", "jinja2==3.1.4"]
# ///
"""Run the upstream website build without touching scripts/build_website.py.

INDEX.md renders to INDEX.html, which on macOS is the same file as the landing
page index.html. Reserving index.html makes INDEX.md render to INDEX-index.html
on every filesystem, so the build is identical on a Mac and on the server.
Usage: uv run curso/build_en.py --output build/en
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_website  # noqa: E402

_disambiguate = build_website._disambiguate_url


def _reserve_landing(url: str, used_lower: set[str], rel_source: str) -> str:
    return _disambiguate(url, used_lower | {"index.html"}, rel_source)


build_website._disambiguate_url = _reserve_landing

if __name__ == "__main__":
    sys.exit(build_website.main())
