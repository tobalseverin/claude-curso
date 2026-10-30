# Claude Code — Curso en español

Bilingual edition (Spanish and English) of [Claude How To](https://github.com/luongnv89/claude-howto) by luongnv89, published at `curso-claude.p113.io`. Spanish adaptation by Cris Severin. MIT license, same as the original.

This repository is a fork of the original. Everything outside `curso/` is upstream content and is kept identical to it, except that the `ja/`, `uk/`, `vi/` and `zh/` translations are removed.

## How it works

The original Markdown is the source of truth. The build renders it to English HTML with the upstream `scripts/build_website.py`, then translates the rendered text using the catalog `curso/es.json`. Code blocks, commands, links and anchors are never translated.

| File | Purpose |
| --- | --- |
| `build.sh` | Full build. Output: `build/site/` (Spanish at `/`, English at `/en/`) |
| `sync.sh` | Merges the latest upstream, drops other languages, rebuilds |
| `es.json` | Translation catalog: English string → Spanish |
| `pending.json` | Generated. Strings with no usable translation yet (shown in English) |
| `catalog.py` | Merges a JSON file of new translations into `es.json` |
| `build_en.py` | Runs the upstream build so `INDEX.md` does not overwrite the landing page on macOS |
| `translate_site.py`, `localize_extras.py`, `finalize.py` | Translation of pages, diagram labels and the landing page |
| `lang_switch.py` | Adds the ES/EN switch and `hreflang` links |
| `brand.py`, `brand.css`, `favicon.svg` | "Curso – Claude" brand: removes the upstream logos and replaces the emerald accent with orange |
| `validate.py` | Checks links, anchors, assets and that code examples are unchanged |

## Build

Requires `uv`, `python3` and `node`.

```bash
curso/build.sh
```

## Update from the original

```bash
curso/sync.sh
```

Then translate the strings listed in `curso/pending.json` into a JSON file and run `python3 curso/catalog.py <file>`. A translation that drops or changes a URL is rejected. Run `curso/build.sh` again until `pending.json` is empty.

## Translation quality

Most of `es.json` was machine-translated and still needs editorial review. The landing page and the 60 roadmap lesson titles have been reviewed.
