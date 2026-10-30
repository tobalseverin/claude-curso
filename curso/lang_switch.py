#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4==4.12.3"]
# ///
"""Add the English/Spanish switch to every page.
Usage: uv run curso/lang_switch.py <spanish-site> <english-site>
Spanish is served at the domain root and English under /en/.
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup
ES,EN=Path(sys.argv[1]),Path(sys.argv[2])
# Same look as the neighbouring buttons, using only classes the upstream templates
# already use so Tailwind compiles them.
PAGE_CLASSES='inline-flex items-center justify-center rounded-md border border-slate-200 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800'
SITES={'es':(ES,'/','/en/','EN','en','Read in English'),'en':(EN,'/en/','/','ES','es','Leer en español')}
for lang,(root,here,there,label,other,title) in SITES.items():
 for path in root.rglob('*.html'):
  rel=path.relative_to(root).as_posix()
  if rel=='index.html' or rel.endswith('/index.html'):rel=rel.removesuffix('index.html')
  soup=BeautifulSoup(path.read_text(),'html.parser')
  toggle=soup.find(id='theme-toggle')
  if toggle and not soup.find(id='lang-switch'):
   a=soup.new_tag('a',href=there+rel,hreflang=other,lang=other,id='lang-switch',title=title)
   a['aria-label']=title
   a['class']='btn btn-ghost btn-sm' if 'theme-toggle' in toggle.get('class',[]) else PAGE_CLASSES
   a.string=label
   toggle.insert_before(a)
  head=soup.head
  if head and not head.find('link',rel='alternate'):
   for code,base in (('es','/'),('en','/en/')):
    head.append(soup.new_tag('link',rel='alternate',hreflang=code,href=base+rel))
  if rel=='':
   # The landing page lists the languages this edition actually ships.
   for stat in soup.select('.hero-stats .stat'):
    if stat.dt and stat.dt.get_text(strip=True) in ('Languages','Idiomas','Idioma'):
     stat.dt.string='Languages' if lang=='en' else 'Idiomas'
     stat.dd.string='2'
   for head_p in soup.select('.footer-head'):
    if head_p.get_text(strip=True) in ('Languages','Idiomas'):
     col=head_p.parent
     for x in col.find_all('a'):x.decompose()
     for code,name in (('es','Español'),('en','English')):
      link=soup.new_tag('a',href='/' if code=='es' else '/en/',hreflang=code);link.string=name;col.append(link)
  path.write_text(str(soup))
print('Language switch added')
