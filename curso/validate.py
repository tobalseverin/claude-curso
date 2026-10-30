#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4==4.12.3"]
# ///
"""Usage: uv run curso/validate.py <spanish-site> <english-site>
Checks the Spanish site: language, internal links and anchors, assets, and that
executable examples match the English build byte for byte.
"""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
import subprocess,sys
dist=Path(sys.argv[1]);source=Path(sys.argv[2]);pages={p:BeautifulSoup(p.read_text(),'html.parser') for p in dist.rglob('*.html')};errors=[]
for p,s in pages.items():
 if s.html.get('lang')!='es':errors.append(f'{p}: language')
 for a in s.select('a[href]'):
  u=urlsplit(a['href'])
  if u.scheme or u.netloc:continue
  path=unquote(u.path)
  # Absolute links come from the language switch: / is Spanish, /en/ is English.
  if path.startswith('/en/'):target=source/path[4:]
  elif path.startswith('/'):target=dist/path[1:]
  else:target=(p.parent/path).resolve() if path else p
  if target.is_dir():target/='index.html'
  if not target.exists():errors.append(f'{p}: missing {a["href"]}')
  elif u.fragment and target in pages and not pages[target].find(id=unquote(u.fragment)):errors.append(f'{p}: missing anchor {a["href"]}')
 for t in s.select('script[src],link[rel="stylesheet"],img[src]'):
  u=urlsplit(t.get('src',t.get('href','')))
  if not u.scheme and not (p.parent/unquote(u.path)).resolve().exists():errors.append(f'{p}: asset {u.path}')
 original=BeautifulSoup((source/p.relative_to(dist)).read_text(),'html.parser')
 before=[x.get_text().replace('luongnv89/claude-howto','tobalseverin/claude-curso') for x in original.select('pre:not(.mermaid)')]
 after=[x.get_text() for x in s.select('pre:not(.mermaid)')]
 if before!=after:errors.append(f'{p}: executable examples changed')
assert len(pages[dist/'index.html'].select('.lesson[data-lesson]'))==60
subprocess.run(['node','--check',str(dist/'assets/landing.js')],check=True)
print(f'{len(pages)} Spanish pages; 60 lessons; {len(errors)} errors')
for e in errors:print(e)
raise SystemExit(bool(errors))
