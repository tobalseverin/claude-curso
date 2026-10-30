#!/usr/bin/env bash
# Bring in the latest upstream (luongnv89/claude-howto) and rebuild.
# Upstream changes to the languages this edition drops are discarded.
# Afterwards curso/pending.json lists the strings that still need Spanish.
set -euo pipefail
cd "$(dirname "$0")/.."

DROPPED=(ja uk vi zh)

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree not clean; commit or stash first." >&2
  exit 1
fi
git remote get-url upstream >/dev/null 2>&1 ||
  git remote add upstream https://github.com/luongnv89/claude-howto.git
git fetch upstream

before=$(git rev-parse HEAD)
if ! git merge --no-edit upstream/main; then
  # Only conflicts inside dropped language folders are resolved automatically.
  for dir in "${DROPPED[@]}"; do
    git ls-files -u -- "$dir" | cut -f2 | sort -u | xargs -r git rm -q --
  done
  if [ -n "$(git diff --name-only --diff-filter=U)" ]; then
    echo "Conflicts left to resolve by hand:" >&2
    git diff --name-only --diff-filter=U >&2
    exit 1
  fi
  git commit --no-edit
fi
# Upstream may add files to a dropped folder without conflicting.
for dir in "${DROPPED[@]}"; do
  if [ -e "$dir" ]; then git rm -rq "$dir"; fi
done
git diff --cached --quiet || git commit -m "chore: drop upstream languages other than English"

echo "Upstream changes since last sync:"
git diff --stat "$before" HEAD -- '*.md' ':!curso' | tail -20

sitio/build.sh
echo "Pending strings: $(python3 -c "import json;print(len(json.load(open('curso/pending.json'))))")"
