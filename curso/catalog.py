#!/usr/bin/env python3
"""Merge reviewed translations into es.json.
Usage: python3 curso/catalog.py <translations.json>
The input maps English source strings to Spanish. Entries whose Spanish text
drops or alters a URL from the English text are rejected.
"""
import json,re,sys
from pathlib import Path
CACHE=Path(__file__).parent/'es.json';URL=re.compile(r'https?://[^\s<>"\')\]]+')
cache=json.loads(CACHE.read_text());new=json.loads(Path(sys.argv[1]).read_text());bad=[]
for en,es in new.items():
 if not es or not all(u in es for u in URL.findall(en)):bad.append(en);continue
 cache[en]=es
CACHE.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
print(f'Merged {len(new)-len(bad)}; rejected {len(bad)}')
for en in bad:print(' -',en[:100])
raise SystemExit(bool(bad))
