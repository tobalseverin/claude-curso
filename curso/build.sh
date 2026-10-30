#!/usr/bin/env bash
# Build the bilingual course: Spanish at the root of build/site, English under build/site/en.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf build
uv run curso/build_en.py --output build/en
cp -R build/en build/es
uv run curso/translate_site.py build/en build/es
uv run curso/localize_extras.py build/es
uv run curso/finalize.py build/es
uv run curso/lang_switch.py build/es build/en
uv run curso/validate.py build/es build/en

mkdir -p build/site
cp -R build/es/. build/site/
cp -R build/en build/site/en
echo "Site ready in build/site ($(find build/site -name '*.html' | wc -l | tr -d ' ') pages)"
