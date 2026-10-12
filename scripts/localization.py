#!/usr/bin/env python3
"""Catálogo PT → i18n/source.json (offline). Chave = sha256(texto normalizado)[:16].
Uso: python3 scripts/localization.py"""
from pathlib import Path
from bs4 import BeautifulSoup,Comment,Doctype
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
ATTRS=('aria-label','title','alt','placeholder')
SKIP=('OS Coach','AIOS','INEMA.CLUB','PT','EN','ES','OpenClaw','T1','T2','T3','T4','T5')
def norm(s):return re.sub(r'\s+',' ',str(s)).strip()
def ident(s):return hashlib.sha256(s.encode()).hexdigest()[:16]
def pages():return [ROOT/'index.html',*sorted(x for x in (ROOT/'curso').rglob('*.html') if '_shared' not in x.parts)]
def eligible(s):return bool(re.search(r'[A-Za-zÀ-ÿ]{2}',s)) and s not in SKIP
def text_nodes(soup):
 for n in soup.find_all(string=True):
  if isinstance(n,(Comment,Doctype)) or n.parent.name in ('script','style','noscript'):continue
  if n.find_parent(class_='inema-lang'):continue
  pre=n.find_parent('pre')
  # comandos de shell ficam idênticos; templates em prosa traduzem
  if pre and re.search(r'^\s*(?:mkdir |git |python3 |sudo |cd |npm |node |~/|\$ )',str(n)):continue
  if eligible(norm(n)):yield n
def kind(n):return 'pre' if n.find_parent('pre') else 'text'
def key_of(s,k='text'):
 v=norm(s) if k=='text' else s
 return (ident(v),v) if eligible(norm(v)) else (None,v)
def meta_targets(soup):
 return [t for t in soup.find_all('meta') if t.get('name')=='description' or t.get('property') in ('og:title','og:description')]
def catalog():
 out={}
 def add(s,k='text'):
  h,v=key_of(s,k)
  if h:out[h]={'source':v,'kind':k}
 for path in pages():
  soup=BeautifulSoup(path.read_text(),'html.parser')
  for n in text_nodes(soup):add(str(n),kind(n))
  for tag in soup.find_all(True):
   for a in ATTRS:
    if tag.get(a):add(tag[a])
  for t in meta_targets(soup):add(t['content'])
  if soup.title:add(soup.title.get_text())
  m=soup.select_one('[data-inema-manifest]')
  if m:
   for tr in json.loads(m.string)['tracks']:
    add(tr['title'])
    for mo in tr['modules']:add(mo['title'])
 return out
if __name__=='__main__':
 out=catalog();(ROOT/'i18n/source.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(len(out),'segmentos;',sum(len(v['source']) for v in out.values()),'caracteres')
