#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["beautifulsoup4==4.12.3"]
# ///
"""Usage: uv run curso/finalize.py <spanish-site>"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(sys.argv[1])
for file in root.rglob('*.html'):
 s=BeautifulSoup(file.read_text(),'html.parser')
 for node in s.find_all(string=True):
  if any(p.name in ['pre','code','script','style'] for p in node.parents):continue
  old=str(node);new=old.replace('diagramas de sirena','diagramas Mermaid').replace('Diagramas de sirena','Diagramas Mermaid').replace('diagramas de Mermaid','diagramas Mermaid')
  if new!=old:node.replace_with(new)
 if file==root/'index.html':
  descriptions=[
   'Los diagramas Mermaid muestran cómo funciona cada herramienta por dentro, para entender cómo y por qué usarla.',
   'Comandos, archivos CLAUDE.md, scripts de hooks, configuraciones MCP y plugins listos para incorporar a tu proyecto.',
   'Diez módulos ordenados para avanzar desde los primeros pasos hasta el uso avanzado en 11–13 horas. Siempre sabés qué aprender después.',
   'Ejecutá /self-assessment o /lesson-quiz dentro de Claude Code para identificar qué necesitás aprender y personalizar tu recorrido.'
  ]
  for card,text in zip(s.select('#why .card'),descriptions):card.p.clear();card.p.append(text)
  s.select_one('.nav-links')['aria-label']='Navegación principal'
  s.select_one('.hero-term')['aria-label']='Demostración de Claude Code: inicio, /init, /self-assessment, hooks y subagentes.'
  term=s.select('#terminal .t-line')
  for i,text in {1:'Claude Code · trabajando en ~/project',3:'✓ creó CLAUDE.md — 6 reglas, 3 importaciones',5:'→ nivel: intermedio · empezá por 03-skills',7:'⚡ hook PreToolUse → ruff check . — correcto',8:'◆ agente Explore → identificó 14 rutas — listo'}.items():term[i].clear();term[i].append(text)
  term[6].select_one('.t-tt').string='agregá límites de solicitudes a la API'
  for a in s.select('a[href*="/vi/README"]'):a.string='Tiếng Việt'
  for a in s.select('a[href="https://code.claude.com/docs/en/overview"]'):a.string='Documentación oficial'
  for x in s.select('.footer-bottom'):
   for n in list(x.find_all(string=True)):
    if 'claude-howto' in str(n):n.replace_with(str(n).replace('claude-howto · MIT con licencia','claude-curso · Licencia MIT'))
 file.write_text(str(s))
print('Final editorial corrections applied')
# Editorially reviewed titles for all sixty roadmap lessons.
titles=[
'Introducción','Referencia de comandos integrados','Comandos personalizados (ahora skills)','Prompts MCP como comandos','Creá tus propios comandos','Buenas prácticas',
'Introducción','Inicio rápido: inicializar la memoria','La jerarquía de la memoria','Sistema modular de reglas','Memoria automática',
'Introducción','Acceder a los puntos de control','Opciones para volver atrás','Patrones de trabajo','Puntos de control y Git',
'Introducción','Comandos de la CLI','Opciones principales','Salida y formatos','Casos de uso destacados',
'Introducción','Carga progresiva de información','Creá skills personalizadas','Controlar la invocación de skills','Ejecutar skills en subagentes','Gestionar skills',
'Introducción','Configuración','Tipos de hooks','Eventos de hooks','Entradas y salidas de hooks','Hooks basados en prompts','Depurar hooks',
'Introducción','Métodos de instalación','Ámbitos de MCP','Recursos mediante menciones con @','Buscar herramientas MCP','Claude como servidor MCP',
'Introducción','Configuración','Subagentes integrados','Encadenar subagentes','Subagentes en segundo plano','Aislamiento con worktrees','Equipos de agentes',
'Introducción','Modo de planificación','Pensamiento extendido','Modo automático','Tareas programadas','Modos de permisos','Modo sin interfaz',
'Introducción','Arquitectura de plugins','Estructura de definición de un plugin','Marketplace de plugins','Probar un plugin','Publicar un plugin']
p=root/'index.html';s=BeautifulSoup(p.read_text(),'html.parser');lessons=s.select('.lesson[data-lesson]');assert len(lessons)==len(titles)==60
for row,title in zip(lessons,titles):
 row.select_one('.lesson-link').string=title
 row.select_one('.check')['aria-label']='Marcar «'+title+'» como completada'
p.write_text(str(s))
# Repair seven inherited upstream cross-references.
fixes={
'07-plugins/index.html#archive-source-v21224':'07-plugins/index.html#archivesource-v21224',
'07-plugins/index.html#command-source-v21229':'07-plugins/index.html#accepting-an-exact-command-with--accept-commandv21271',
'guide.html#use-case-matrix':'guide.html#what-can-you-build-with-this',
'guide.html#troubleshooting':'QUICK_REFERENCE.html#troubleshooting',
'guide.html#feature-comparison':'QUICK_REFERENCE.html#-feature-matrix',
'#claude-agents-cli-command':'#claude-agentscli-command',
'#claude-plugin-details-name-v21139':'#claude-plugin-details-namev21139',
}
for p in root.rglob('*.html'):
 s=BeautifulSoup(p.read_text(),'html.parser')
 for a in s.select('a[href]'):
  if a['href'] in fixes:a['href']=fixes[a['href']]
 for n in s.find_all(string=True):
  if '⁇' in str(n) and not any(t.name in ['code','pre','script','style'] for t in n.parents):n.replace_with(str(n).replace('⁇','').strip())
 p.write_text(str(s))
for p in root.rglob('*.html'):
 s=BeautifulSoup(p.read_text(),'html.parser')
 for a in s.select('a[href*="/vi/README"]'):a.string='Tiếng Việt'
 for n in list(s.find_all(string=True)):
  if any(t.name in ['code','pre','script','style'] for t in n.parents):continue
  old=str(n);new=old
  for a,b in {'Cómo Claude cómo solucionar esto':'Qué aporta esta guía','Terminas esquiando todo':'Terminás revisando todo superficialmente','comandos de barra corta':'comandos de barra','sin cabeza':'sin interfaz','Confiado por los desarrolladores':'Con la confianza de desarrolladores','¿ No está seguro por dónde empezar?':'¿No sabés por dónde empezar?','¿ Qué podemos construir con esto?':'¿Qué podés crear con esta guía?','Empieza a dominar el código de Claude hoy':'Empezá a dominar Claude Code hoy','MCP indica como comandos':'Prompts MCP como comandos','Variables ambientales':'Variables de entorno','Carga caliente':'Recarga automática'}.items():new=new.replace(a,b)
  if new!=old:n.replace_with(new)
 article=s.select_one('article')
 if article:
  for ptag in article.find_all('p'):
   if 'Ngôn' in ptag.get_text() or ('🌐' in ptag.get_text() and '日本語' in ptag.get_text()):
    ptag.clear();ptag.append('Idioma: Español · Adaptación de Cris Severin')
 sfile=p;sfile.write_text(str(s))
import re
for p in root.rglob('*.html'):
 s=BeautifulSoup(p.read_text(),'html.parser');changed=False
 for pre in s.select('pre.mermaid'):
  old=pre.get_text();new=re.sub(r'\|“(.*?)“\|',lambda m:'|"'+m[1]+'"|',old)
  if new!=old:pre.string=new;changed=True
 if changed:p.write_text(str(s))
