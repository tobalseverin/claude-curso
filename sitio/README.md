# Sitio de cursos

Everything published at `curso-claude.p113.io`: a catalog at `/` and one folder per course. All courses share the domain and the deploy.

| Path | Purpose |
| --- | --- |
| `cursos.json` | Courses shown in the catalog, in order |
| `tokens.css` | Colors, fonts and radius shared by the catalog and every course |
| `portada/` | Catalog template and styles |
| `cursos/<folder>/` | Public files of a static course, served at `/<folder>/` |
| `build_portada.py` | Renders the catalog and the redirects from the old Claude URLs |
| `build.sh` | Builds the full site into `build/site/` |

The Claude Code course stays at the repository root because this is a fork of its source. It is built by `curso/` and served at `/claude/`.

## Add a course

1. Put its public files in `sitio/cursos/<folder>/`, with `index.html` at the top and relative paths only.
   Load `../tokens.css` before its own styles and read the theme from the `claude-howto-theme` storage key, as `vibecoding/` does.
2. Add an entry to `cursos.json`.
3. Run `sitio/build.sh`.

Deploy steps are in [`docs/02-trd.md`](../docs/02-trd.md).
