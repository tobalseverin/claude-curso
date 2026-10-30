#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4==4.12.3"]
# ///
"""Usage: uv run curso/localize_extras.py <spanish-site>"""
from pathlib import Path
import re,json,sys
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent;DIST=Path(sys.argv[1]);CP=HERE/'es.json';PENDING=HERE/'pending.json';cache=json.loads(CP.read_text())
# Labels only: never translate Mermaid grammar, node identifiers or styling directives.
pattern=re.compile(r'"([^"\n]+)"|\[([^\[\]"\n]+)\]|\|([^|\n]+)\|')
def valid(x):
 return bool(re.search('[A-Za-z]',x)) and not any(v in x for v in ['=>','===','fill:','stroke:','font-size:','color:']) and not re.fullmatch(r'[/@.~]?[\w./@~_-]+',x)
def pieces(text):
 for m in pattern.finditer(text):
  x=next(x for x in m.groups() if x is not None)
  if valid(x):
   for part in re.split(r'(<br\s*/?>)',x):
    if not part.startswith('<') and re.search('[A-Za-z]',part):yield part
pending=set()
for p in DIST.rglob('*.html'):
 soup=BeautifulSoup(p.read_text(),'html.parser')
 for pre in soup.select('pre.mermaid'):pending.update(x for x in pieces(pre.get_text()) if x not in cache)
if pending:
 # Untranslated diagram labels join the page strings waiting for translation.
 waiting=json.loads(PENDING.read_text()) if PENDING.exists() else {}
 waiting.update({x:'' for x in sorted(pending)});PENDING.write_text(json.dumps(waiting,ensure_ascii=False,indent=2))
 print('Diagram labels pending',len(pending))
for p in DIST.rglob('*.html'):
 soup=BeautifulSoup(p.read_text(),'html.parser')
 for pre in soup.select('pre.mermaid'):
  def replace(m):
   label=next(x for x in m.groups() if x is not None)
   if not valid(label):return m[0]
   translated=''.join(part if part.startswith('<') else cache.get(part,part).replace('ganchos','hooks') for part in re.split(r'(<br\s*/?>)',label))
   # ASCII quotes remain structural; keep newly generated punctuation inside the label safe.
   translated=translated.replace('"','“').replace('[','(').replace(']',')').replace('|','/')
   return m[0].replace(label,translated)
  pre.string=pattern.sub(replace,pre.get_text())
 # Localize the remaining runtime messages in inline UI scripts, preserving code logic.
 for script in soup.find_all('script'):
  if script.string:
   s=str(script.string)
   for a,b in {'Diagram':'Diagrama'}.items():s=s.replace("'"+a+"'","'"+b+"'")
   script.string=s
 if p.name=='index.html' and p.parent==DIST:
  soup.title.string='Claude Code — Curso en español · Cris Severin'
  soup.select_one('.hero-title').clear()
  h=soup.select_one('.hero-title');h.append('Dominá ');em=soup.new_tag('em');em.string='Claude Code';h.append(em);h.append(soup.new_tag('br'));h.append('en un fin de semana')
  for sel,text in {
   '.hero-sub':'Pasá de escribir claude a coordinar agentes, hooks, skills y servidores MCP, con tutoriales visuales, plantillas para copiar y pegar y un recorrido guiado.',
   '#why h2':'La documentación te dice qué. Esta guía te muestra cómo.',
   '#why .feature-card:nth-of-type(1) p':'Los diagramas Mermaid muestran cómo funciona cada herramienta por dentro, para entender cómo y por qué usarla.',
  }.items():
   x=soup.select_one(sel)
   if x:x.clear();x.append(text)
  stats=soup.select('.hero-stats .stat')
  if len(stats)>2:stats[2].dt.string='Idioma';stats[2].dd.string='Español'
  for btn in soup.select('[data-copy]'):
   btn['data-copy']=btn['data-copy'].replace('luongnv89/claude-howto','tobalseverin/claude-curso')
  for logo in soup.select('.nav-brand,.footer-brand'):
   if logo.name=='a':logo['aria-label']='Claude Code — Curso en español'
  for term in soup.select('.terminal'):
   for node in term.find_all(string=True):
    s=str(node)
    for a,b in {'working in':'trabajando en','wrote CLAUDE.md — 6 rules, 3 imports':'creó CLAUDE.md — 6 reglas, 3 importaciones','level: intermediate · start at 03-skills':'nivel: intermedio · empezá por 03-skills','add rate limiting to the api':'agregá límites de solicitudes a la API','mapped 14 routes — done':'identificó 14 rutas — listo','— passed':'— correcto'}.items():s=s.replace(a,b)
    if s!=str(node):node.replace_with(s)
 p.write_text(str(soup))
p=DIST/'assets/landing.js';s=p.read_text()
for a,b in {'Copied to clipboard':'Copiado al portapapeles','Unable to copy to clipboard':'No se pudo copiar al portapapeles','"Copied"':'"Copiado"','"Copy failed"':'"No se pudo copiar"'}.items():s=s.replace(a,b)
p.write_text(s)
print('Localized diagram labels and interactive messages')
