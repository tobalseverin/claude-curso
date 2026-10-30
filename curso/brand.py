#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4==4.12.3"]
# ///
"""Apply the Curso – Claude brand to both built sites.
Usage: uv run curso/brand.py <spanish-site> <english-site>
Removes the upstream logo images, writes the "Curso – Claude" wordmark,
swaps the favicon and loads curso/brand.css after the upstream styles.
"""
import shutil,sys
from pathlib import Path
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
NAME='Curso – Claude'
LOGO='claude-howto-logo'
def wordmark(soup):
 span=soup.new_tag('span',attrs={'class':'curso-wordmark'})
 span.append('Curso – ')
 accent=soup.new_tag('span',attrs={'class':'curso-accent'});accent.string='Claude';span.append(accent)
 return span
def drop_empty(tag):
 # Remove wrappers (picture, a, p) left with nothing visible after the logo goes.
 while tag and tag.name in ('picture','a','p','div') and not tag.get_text(strip=True) and not tag.find(['img','svg','video']):
  parent=tag.parent;tag.decompose();tag=parent
for root in map(Path,sys.argv[1:]):
 shutil.copy(HERE/'brand.css',root/'assets/curso-brand.css')
 shutil.copy(HERE/'favicon.svg',root/'assets/curso-favicon.svg')
 for path in root.rglob('*.html'):
  prefix='../'*(len(path.relative_to(root).parts)-1)
  soup=BeautifulSoup(path.read_text(),'html.parser')
  for icon in soup.select('link[rel~="icon"]'):icon['href']=prefix+'assets/curso-favicon.svg'
  if not soup.find('link',href=prefix+'assets/curso-brand.css'):
   soup.head.append(soup.new_tag('link',rel='stylesheet',href=prefix+'assets/curso-brand.css'))
  # Header and footer brands: logos out, wordmark in.
  for brand in soup.select('.nav-brand, .footer-brand, header a[href$="index.html"]'):
   if not brand.find('img',src=lambda s:s and LOGO in s):continue
   for img in brand.find_all('img',src=lambda s:s and LOGO in s):img.decompose()
   label=brand.find('span',class_=lambda c:c and 'text-sm' in c)
   if label:label.clear();label.append(wordmark(soup))
   else:brand.insert(0,wordmark(soup))
   if brand.name=='a':brand['aria-label']=NAME
  # Remaining logos are the banners at the top of each article.
  for node in soup.find_all(['img','source']):
   src=node.get('src','')+node.get('srcset','')
   if LOGO in src:
    parent=node.parent;node.decompose();drop_empty(parent)
  path.write_text(str(soup))
print('Brand applied')
