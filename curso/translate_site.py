#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4==4.12.3"]
# ///
"""Translate rendered HTML without changing IDs, links, executable examples or structure.
Usage: uv run curso/translate_site.py <english-site> <spanish-site>
Strings missing from es.json stay in English and are listed in curso/pending.json.
"""
from pathlib import Path
import json,re,sys
from bs4 import BeautifulSoup,Comment,Doctype
SOURCE=Path(sys.argv[1]);DEST=Path(sys.argv[2]);CACHE=Path(__file__).parent/'es.json';PENDING=Path(__file__).parent/'pending.json'
manual={
'Claude Code How-To Guide':'Claude Code — Curso en español',
'Master Claude Code in a Weekend':'Dominá Claude Code en un fin de semana',
'Master Claude Code':'Dominá Claude Code', 'in a Weekend':'en un fin de semana',
'Why':'Por qué','vs Docs':'Comparación','Roadmap':'Recorrido','Guide':'Guía',
'Start learning':'Empezar a aprender','Start the roadmap':'Comenzar el recorrido','Read the guide':'Leer la guía',
'~/claude-howto · a weekend curriculum':'~/claude-curso · un curso para el fin de semana',
'Synced to v2.1.310':'Basado en v2.1.310','Modules':'Módulos','Time':'Duración','Languages':'Idiomas',
'Overview':'Introducción','Memory':'Memoria','Slash Commands':'Comandos de barra','Slash commands':'Comandos de barra',
'Skills':'Skills','Hooks':'Hooks','Plugins':'Plugins','Subagents':'Subagentes','Checkpoints':'Puntos de control',
'Advanced Features':'Funciones avanzadas','MCP Protocol':'Protocolo MCP','CLI Reference':'Referencia de la CLI',
'Introduction':'Introducción','Learning Roadmap':'Recorrido de aprendizaje','Quick Reference':'Referencia rápida',
'Claude Concepts Guide':'Guía de conceptos de Claude','Feature Catalog':'Catálogo de funciones','Index':'Índice',
'Style Guide':'Guía de estilo','Resources':'Recursos','Getting started':'Primeros pasos','Building workflows':'Crear flujos de trabajo',
'Power user':'Uso avanzado','Level 1 — Beginner':'Nivel 1 — Principiante','Level 2 — Intermediate':'Nivel 2 — Intermedio',
'Level 3 — Advanced':'Nivel 3 — Avanzado','Not started':'Sin empezar','In progress':'En curso','Done':'Completada',
'done':'completadas','in progress':'en curso','not started':'sin empezar','complete':'completado',
'Continue':'Continuar','Reset progress':'Reiniciar progreso','lessons':'lecciones','1 hour':'1 hora','1.5 hours':'1,5 horas','2 hours':'2 horas','2–3 hours':'2–3 horas',
'All done — roadmap complete.':'¡Terminaste! Recorrido completado.',
'Why this guide':'Por qué esta guía','The docs tell you what.':'La documentación te dice qué.',
'This shows you how.':'Esta guía te muestra cómo.','Visual by default':'Visual desde el principio',
'Copy-paste templates':'Plantillas para copiar y pegar','A guided path':'Un recorrido guiado',
'Self-assessment built in':'Autoevaluación incluida','Official docs vs this guide':'Documentación oficial y esta guía',
'Different jobs, same tool':'Distintos propósitos, la misma herramienta','Official docs':'Documentación oficial','This guide':'Esta guía',
'The roadmap':'El recorrido','Ten stations, one line':'Diez estaciones, un recorrido',
'Get started':'Empezá','Fifteen minutes to your first workflow':'Tu primer flujo de trabajo en quince minutos',
'Clone the repo':'Cloná el repositorio','Take the self-assessment':'Hacé la autoevaluación','Follow the roadmap':'Seguí el recorrido',
'Start at your level →':'Empezá en tu nivel →','Back to top ↑':'Volver arriba ↑','Project':'Proyecto','Docs':'Documentación',
'MIT license':'Licencia MIT','Changelog':'Registro de cambios','Edit on GitHub':'Ver fuente en GitHub',
'On this page':'En esta página','Previous':'Anterior','Next':'Siguiente','Copy':'Copiar','Copied!':'¡Copiado!',
'Open navigation':'Abrir navegación','Toggle theme':'Cambiar tema','Skip to content':'Saltar al contenido',
'Switch to light theme':'Activar tema claro','Switch to dark theme':'Activar tema oscuro',
'Go from typing':'Pasá de escribir','to orchestrating agents, hooks, skills, and MCP servers — with visual tutorials, copy‑paste templates, and a guided learning path.':'a coordinar agentes, hooks, skills y servidores MCP, con tutoriales visuales, plantillas listas para usar y un recorrido de aprendizaje guiado.',
'Built-in commands, custom commands and team shortcuts.':'Comandos integrados, comandos personalizados y atajos para tu equipo.',
'CLAUDE.md, rules and auto memory that persist across sessions.':'CLAUDE.md, reglas y memoria automática que persisten entre sesiones.',
'Try bold ideas and rewind in one keystroke.':'Probá ideas y volvé atrás con un atajo de teclado.',
'Interactive and print mode, flags and scripting.':'Modo interactivo y de impresión, opciones y scripts.',
'Reusable expertise Claude loads only when it needs it.':'Conocimiento reutilizable que Claude carga cuando lo necesita.',
'Quality gates and automation on every tool call and event.':'Controles de calidad y automatización en cada llamada a herramientas y evento.',
'Connect GitHub, databases and APIs as live tools.':'Conectá GitHub, bases de datos y APIs como herramientas.',
'Delegate to specialists with their own context and tools.':'Delegá en especialistas con su propio contexto y herramientas.',
'Planning, auto mode, permissions, headless runs and more.':'Planificación, modo automático, permisos, ejecución sin interfaz y más.',
'Bundle commands, agents, hooks and MCP into one install.':'Reuní comandos, agentes, hooks y MCP en una sola instalación.',
'Three levels, 10 modules, 60 lessons. Progress is saved in your browser — check lessons off as you go.':'Tres niveles, 10 módulos y 60 lecciones. Tu progreso se guarda en este navegador: marcá las lecciones a medida que avanzás.',
'Get productive on day one: commands, memory, safe rewinds and the CLI basics.':'Empezá a trabajar desde el primer día: comandos, memoria, puntos de control y fundamentos de la CLI.',
'Automate with skills and hooks, then connect live data and delegate to subagents.':'Automatizá con skills y hooks, conectá datos y delegá tareas en subagentes.',
'Plan, run headless and on a schedule, then package everything as a plugin for your team.':'Planificá, ejecutá sin interfaz y programá tareas; después reuní todo en un plugin para tu equipo.',
'Everything is markdown — templates included, nothing to install.':'Todo está en Markdown, incluidas las plantillas. No necesitás instalar nada para leerlo.',
'Inside Claude Code, find your level and skip what you know.':'Dentro de Claude Code, identificá tu nivel y avanzá desde lo que ya sabés.',
'Work through the modules at your level — progress is tracked above.':'Completá los módulos de tu nivel. Tu progreso queda registrado en el recorrido.',
'A community guide to Claude Code. Markdown is the source of truth.':'Una guía comunitaria de Claude Code. Versión en español de Cris Severin, basada en el proyecto de luongnv89.',
'Format':'Formato','Depth':'Profundidad','Examples':'Ejemplos','Structure':'Estructura','Onboarding':'Inicio','Self-assessment':'Autoevaluación',
'Reference documentation':'Documentación de referencia','Visual tutorials with Mermaid diagrams':'Tutoriales visuales con diagramas Mermaid',
'Feature descriptions':'Descripción de funciones','How it works under the hood':'Cómo funciona por dentro','Basic snippets':'Fragmentos básicos',
'Production-ready templates you use immediately':'Plantillas listas para usar en proyectos reales','Feature-organized':'Organizada por funciones',
'Progressive learning path (beginner to advanced)':'Aprendizaje progresivo, de principiante a avanzado','Self-directed':'Por tu cuenta',
'Guided roadmap with time estimates':'Recorrido guiado con tiempos estimados','None':'Ninguna','Interactive quizzes that build a personalized path':'Cuestionarios interactivos para crear un recorrido personalizado',
}
cache=json.loads(CACHE.read_text()) if CACHE.exists() else {}
cache.update(manual)
SKIP={'script','style','code','pre','noscript'}
def normalize(s):return re.sub(r'\s+',' ',s).strip()
def eligible(s):return bool(re.search('[A-Za-z]',s)) and not re.fullmatch(r'[\w./~:@=+\-]+',s) and not s.startswith(('https://','http://'))
# Also translate single-word prose, but leave known identifiers and brand names intact.
brands={'Claude','Claude Code','GitHub','MCP','CLI','API','JSON','YAML','Markdown','Mermaid','MIT','TypeScript','JavaScript','Python','React','Node.js','Bash','Docker','VS Code','macOS','Windows','Linux','PreToolUse','PostToolUse','Stop','SubagentStop','PermissionRequest','UserPromptSubmit','SessionStart','SessionEnd'}
def should(s):
 if re.fullmatch(r'[^\s]+',s) and ('/' in s or re.search(r'\.(?:md|json|yaml|yml|py|sh|ts|js)$',s)):return False
 return bool(re.search('[A-Za-z]',s)) and s not in brands and not s.startswith(('https://','http://')) and not re.fullmatch(r'[/~.$@][\w./~:$@=+\-]+',s)
def scan(soup):
 for node in soup.find_all(string=True):
  if isinstance(node,(Comment,Doctype)) or any(p.name in SKIP for p in node.parents):continue
  text=normalize(str(node))
  if should(text):yield node,None,text
 for tag in soup.find_all(True):
  for attr in ['alt','title','aria-label','placeholder']:
   text=normalize(tag.get(attr,''))
   if should(text):yield tag,attr,text
  if tag.name=='meta' and tag.get('name') in ['description']:
   text=normalize(tag.get('content',''))
   if should(text):yield tag,'content',text
URL=re.compile(r'https?://[^\s<>"\')\]]+')
def usable(text):
 # A translation that altered any URL is worse than the English original.
 value=cache.get(text)
 return value is not None and all(u in value for u in URL.findall(text))
files=sorted(SOURCE.rglob('*.html'));pending={}
for path in files:
 soup=BeautifulSoup(path.read_text(),'html.parser')
 for _,_,text in scan(soup):
  if not usable(text):pending.setdefault(text,cache.get(text,''))
PENDING.write_text(json.dumps(pending,ensure_ascii=False,indent=2))
print('Pages',len(files),'pending',len(pending),'words',sum(len(s.split()) for s in pending),'→',PENDING.name,flush=True)
# Never translate executable strings, paths, IDs or link fragments.
def polish(s):
 for a,b in [('ganchos','hooks'),('Ganchos','Hooks'),('gancho','hook'),('Gancho','Hook'),('Subagentes','Subagentes'),('Código Claude','Claude Code'),('Claudio','Claude')]:s=s.replace(a,b)
 for a,b in [('sin cabeza','sin interfaz'),('Sin cabeza','Sin interfaz'),('forcado','bifurcado'),('cáscara','shell'),('caparazón','shell'),('Habilidades','Skills'),('habilidades','skills'),('Competencias','Skills'),('competencias','skills'),('Desperdicios a','Inicia un'),('código Claude','Claude Code')]:s=s.replace(a,b)
 return s
for path in files:
 soup=BeautifulSoup(path.read_text(),'html.parser');soup.html['lang']='es'
 for node,attr,text in list(scan(soup)):
  value=polish(cache[text]) if usable(text) else text
  if attr:node[attr]=value
  else:
   old=str(node);node.replace_with((' ' if old[:1].isspace() else '')+value+(' ' if old[-1:].isspace() else ''))
 # Own fork and original attribution remain distinct.
 for tag in soup.find_all(['a','img','source','link']):
  for attr in ['href','src','srcset']:
   if tag.has_attr(attr):tag[attr]=tag[attr].replace('https://github.com/luongnv89/claude-howto','https://github.com/tobalseverin/claude-curso')
 for code in soup.find_all('code'):
  if 'git clone https://github.com/luongnv89/claude-howto.git' in code.get_text():code.string=code.get_text().replace('luongnv89/claude-howto','tobalseverin/claude-curso')
 # Main language count now describes this localized edition.
 if path.relative_to(SOURCE).as_posix()=='index.html':
  for x in soup.select('.stat'):
   if 'Idiomas' in x.get_text():
    n=x.select_one('.stat-value')
    if n:n.string='1'
  for f in soup.select('.footer-brand p'):
   f.string='Versión en español de Cris Severin. Proyecto original de luongnv89, bajo licencia MIT.'
 for footer in soup.select('main > footer'):
  footer.clear()
  p=soup.new_tag('p');p.string='Versión en español de Cris Severin. Basado en Claude How To de luongnv89, bajo licencia MIT. ';footer.append(p)
  a=soup.new_tag('a',href='https://github.com/luongnv89/claude-howto');a.string='Proyecto original';p.append(a)
 out=DEST/path.relative_to(SOURCE);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(str(soup))
print('Wrote',len(files),'Spanish pages',flush=True)
