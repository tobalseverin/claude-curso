#!/usr/bin/env bash
# Build the full site into build/site: catalog at /, one folder per course.
set -euo pipefail
cd "$(dirname "$0")/.."

curso/build.sh

rm -rf build/site
mkdir -p build/site
cp -R build/es build/site/claude
cp -R build/en build/site/claude/en
cp -R sitio/cursos/. build/site/
uv run sitio/build_portada.py build/site
python3 sitio/cache_bust.py build/site
echo "Site ready in build/site ($(find build/site -name '*.html' | wc -l | tr -d ' ') pages)"
