#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["jinja2==3.1.4"]
# ///
"""Render the course catalog and the redirects from the old Claude URLs.
Usage: uv run sitio/build_portada.py <site>
"""
import json
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = Path(__file__).resolve().parent
SITE = Path(sys.argv[1])
REDIRECT = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<title>Cursos</title>
</head>
<body><a href="{url}">Esta página se movió</a></body>
</html>
"""

courses = json.loads((HERE / "cursos.json").read_text())
for course in courses:
    if not (SITE / course["carpeta"] / "index.html").is_file():
        raise SystemExit(f"Course without index.html: {course['carpeta']}")

env = Environment(
    loader=FileSystemLoader(HERE / "portada"), autoescape=select_autoescape()
)
(SITE / "index.html").write_text(
    env.get_template("index.html.j2").render(courses=courses)
)
shutil.copy(HERE / "portada/portada.css", SITE / "portada.css")
shutil.copy(HERE.parent / "curso/favicon.svg", SITE / "favicon.svg")

# The Claude course used to live at the root; keep its old URLs working.
claude = SITE / "claude"
count = 0
for page in claude.rglob("*.html"):
    rel = page.relative_to(claude)
    if rel.as_posix() == "index.html":
        continue
    target = SITE / rel
    if target.exists():
        raise SystemExit(f"Redirect would overwrite {target}")
    url = "/claude/" + rel.as_posix()
    if page.name == "index.html":
        url = url.removesuffix("index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(REDIRECT.format(url=url))
    count += 1
print(f"Catalog with {len(courses)} courses; {count} redirects")
