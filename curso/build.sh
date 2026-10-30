#!/usr/bin/env bash
# Build the Claude Code course: Spanish in build/es, English in build/en.
# sitio/build.sh assembles them into the full site.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf build
uv run curso/build_en.py --output build/en
cp -R build/en build/es
uv run curso/translate_site.py build/en build/es
uv run curso/localize_extras.py build/es
uv run curso/finalize.py build/es
uv run curso/lang_switch.py build/es build/en
uv run curso/brand.py build/es build/en
uv run curso/validate.py build/es build/en

