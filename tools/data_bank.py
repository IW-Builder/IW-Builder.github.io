"""Portable IW Data banks: readable TXT with an authoritative JSON payload.

No dependencies. Does not execute IW/PawScript or automatically integrate worlds.
"""
from pathlib import Path
from decimal import Decimal
import argparse
import hashlib
import json
import re
import sys
import uuid

FORMAT = 'iw-data-bank'
BEGIN = '<!-- BEGIN IW DATA BANK -->'
END = '<!-- END IW DATA BANK -->'
COLLECTIONS = {'NPCs':'npc', 'possibleCharacters':'pc', 'trackedItems':'tracker',
               'triggerEvents':'trigger', 'instructionBlocks':'block', 'loreBookEntries':'keyword'}

def pairs(items):
    result = {}
    for k,v in items:
        if k in result: raise ValueError('Duplicate JSON key: '+k)
        result[k] = v
    return result

def invalid_number(value): raise ValueError('Not a finite JSON number: '+value)

def loads(text):
    return json.loads(text, object_pairs_hook=pairs, parse_float=Decimal,
                      parse_constant=invalid_number)

def dumps(value, depth=0, canonical=False):
    """Preserve decimal precision and JSON value types without a float conversion."""
    if isinstance(value, Decimal):
        if not value.is_finite(): raise ValueError('Non-finite number')
        text = str(value)
        return text if any(c in text for c in '.eE') else text+'.0'
    if isinstance(value, (dict,list)):
        is_dict = isinstance(value,dict)
        opening,closing = ('{','}') if is_dict else ('[',']')
        if not value: return opening+closing
        if is_dict:
            if not all(isinstance(k,str) for k in value): raise ValueError('JSON keys must be strings')
            keys = sorted(value) if canonical else value
            parts = [json.dumps(k,ensure_ascii=True)+(': ' if not canonical else ':')+dumps(value[k],depth+1,canonical) for k in keys]
        else: parts = [dumps(v,depth+1,canonical) for v in value]
        if canonical: return opening+','.join(parts)+closing
        return opening+'\n'+'  '*(depth+1)+(',\n'+'  '*(depth+1)).join(parts)+'\n'+'  '*depth+closing
    return json.dumps(value,ensure_ascii=True,allow_nan=False)

def digest(value): return hashlib.sha256(dumps(value,canonical=True).encode('utf-8')).hexdigest()
def escape(key): return key.replace('~','~0').replace('/','~1')

def tokens(pointer):
    if not pointer.startswith('/'): raise ValueError('Use a JSON Pointer beginning with /')
    if re.search(r'~(?![01])',pointer): raise ValueError('Invalid JSON Pointer escape')
    return [s.replace('~1','/').replace('~0','~') for s in pointer[1:].split('/')]

def get(doc,pointer):
    value = doc
    for token in tokens(pointer):
        if isinstance(value,list):
            if not re.fullmatch(r'0|[1-9][0-9]*',token): raise ValueError('Invalid list index in '+pointer)
            value=value[int(token)]
        elif isinstance(value,dict): value=value[token]
        else: raise ValueError('Path traverses a scalar: '+pointer)
    return value

def validate(bank):
    if not isinstance(bank,dict) or bank.get('format')!=FORMAT or type(bank.get('version')) is not int or bank['version']!=1:
        raise ValueError('Expected an iw-data-bank version 1 object')
    if not isinstance(bank.get('entries'),list): raise ValueError('entries must be a list')
    ids=set()
    for e in bank['entries']:
        if not isinstance(e,dict): raise ValueError('Each entry must be an object')
        for key in ['id','title','kind','summary']:
            if not isinstance(e.get(key),str) or (key!='summary' and not e[key]): raise ValueError('Entry needs text '+key)
        if e['id'] in ids: raise ValueError('Duplicate entry ID: '+e['id'])
        ids.add(e['id'])
        if 'tags' in e and (not isinstance(e['tags'],list) or not all(isinstance(t,str) and t and '\n' not in t and '\r' not in t for t in e['tags'])):
            raise ValueError('tags must be a list of nonempty single-line strings')
        deps=e.get('dependencies')
        if not isinstance(deps,dict) or not all(isinstance(deps.get(k),list) and all(isinstance(x,str) for x in deps[k]) for k in ['included','external','unresolved']):
            raise ValueError('dependencies needs included, external and unresolved string lists')
        if not isinstance(e.get('components'),list) or not e['components']: raise ValueError('Entry needs components')
        for c in e['components']:
            if not isinstance(c,dict) or 'payload' not in c or not isinstance(c.get('kind'),str): raise ValueError('Component needs kind and payload')
            if 'sourcePath' in c: tokens(c['sourcePath'])
    for e in bank['entries']:
        missing=set(e['dependencies']['included'])-ids
        if missing: raise ValueError('Missing included entry dependency: '+', '.join(sorted(missing)))
    return bank

def line(value): return str(value).replace('\n',' ').replace('\r',' ')

def render(bank):
    validate(bank)
    parts=['# IW Data Bank\n\nReadable index only; the JSON section is authoritative. Edit through unpack/pack to update the integrity hash.\n']
    for e in bank['entries']:
        parts.append('\n## '+line(e['title'])+'\nID: '+line(e['id'])+' | Kind: '+line(e['kind'])+'\n')
        if e.get('tags'): parts.append('Tags: '+' '.join('['+line(t)+']' for t in e['tags'])+'\n')
        if e['summary']: parts.append(line(e['summary'])+'\n')
        parts.append('Components: '+str(len(e['components']))+'\n')
    parts.extend(['\n',BEGIN,'\n```json\n',dumps(bank),'\n```\n',END,'\nSHA256: ',digest(bank),'\n'])
    return ''.join(parts)

def read_bank(path):
    text=Path(path).read_text(encoding='utf-8-sig')
    if text.lstrip().startswith('{'): return validate(loads(text))
    pattern=re.compile(r'^'+re.escape(BEGIN)+r'\r?\n```json\r?\n([\s\S]*?)\r?\n```\r?\n'+re.escape(END)+r'\r?\nSHA256: ([a-f0-9]{64}|UNVERIFIED)\s*\Z',re.M)
    matches=list(pattern.finditer(text))
    if len(matches)!=1 or len(re.findall(r'^'+re.escape(BEGIN)+r'\s*$',text,re.M))!=1:
        raise ValueError('Expected one complete Data bank section and SHA256 line')
    bank=validate(loads(matches[0][1]))
    if matches[0][2]!='UNVERIFIED' and digest(bank)!=matches[0][2]: raise ValueError('Integrity hash mismatch. Use the last intact copy or review the edit before repacking the authoritative JSON.')
    return bank

def export(doc,select=None,tags=None,bundle=None):
    if not isinstance(doc,dict): raise ValueError('World must be a JSON object')
    paths=[];layout=[]
    if select:
        if len(select)!=len(set(select)): raise ValueError('Selection repeats a path')
        decoded=[tokens(p) for p in select]
        for i,a in enumerate(decoded):
            for b in decoded[i+1:]:
                if a==b[:len(a)] or b==a[:len(b)]: raise ValueError('Selections overlap; choose parent or child, not both')
        paths=list(select)
    else:
        for k,v in doc.items():
            separate=k in COLLECTIONS and isinstance(v,list) and bool(v)
            layout.append({'key':k,'items':len(v) if separate else None})
            paths.extend('/'+escape(k)+'/'+str(i) for i in range(len(v))) if separate else paths.append('/'+escape(k))
    entries=[]
    for p in paths:
        payload=get(doc,p);key=tokens(p)[0]
        kind=COLLECTIONS.get(key,'world-field') if len(tokens(p))==2 else 'world-field'
        title=(payload.get('name') or payload.get('title') or payload.get('characterName')) if isinstance(payload,dict) else None
        entry={'id':'entry-'+uuid.uuid4().hex[:12],'title':str(title or p),'kind':kind,'summary':'',
               'dependencies':{'included':[],'external':[],'unresolved':['Dependency review required before reuse; extraction does not infer prose or dynamic references.']},
               'components':[{'kind':kind,'sourcePath':p,'payload':payload}]}
        if tags: entry['tags']=list(tags)
        entries.append(entry)
    if bundle and entries:
        first=entries[0];first['title']=bundle;first['kind']='bundle'
        first['components']=[c for e in entries for c in e['components']];entries=[first]
    bank={'format':FORMAT,'version':1,'source':{'title':str(doc.get('title','')),'sha256':digest(doc)},'entries':entries}
    if not select: bank['completeWorld']={'layout':layout}
    return validate(bank)

def restore(bank):
    validate(bank)
    layout=bank.get('completeWorld',{}).get('layout')
    if not isinstance(layout,list): raise ValueError('Only a complete-world report can be restored; selected entries require deliberate integration')
    components={}
    for e in bank['entries']:
        for c in e['components']:
            p=c.get('sourcePath')
            if p is None or p in components: raise ValueError('Missing or duplicate sourcePath')
            components[p]=c['payload']
    doc={};used=set()
    for item in layout:
        key=item['key'];n=item['items'];p='/'+escape(key)
        if key in doc: raise ValueError('Duplicate layout key')
        if n is None: doc[key]=components[p];used.add(p)
        else:
            if type(n) is not int or not 0<=n<=len(components): raise ValueError('Invalid layout length')
            paths=[p+'/'+str(i) for i in range(n)]
            doc[key]=[components[x] for x in paths];used.update(paths)
    if used!=set(components): raise ValueError('Extra components not described by the complete-world layout')
    if digest(doc)!=bank.get('source',{}).get('sha256'): raise ValueError('Restored world differs from the source fingerprint; review and integrate changed data deliberately')
    return doc

def write(path,text):
    # Never silently overwrite an existing bank/world.
    with Path(path).open('x',encoding='utf-8',newline='') as f: f.write(text)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('export');p.add_argument('input');p.add_argument('--out',required=True)
    p.add_argument('--select',action='append');p.add_argument('--tag',action='append');p.add_argument('--bundle')
    for name in ['pack','unpack','restore']:
        p=sub.add_parser(name);p.add_argument('input');p.add_argument('--out',required=True)
    p=sub.add_parser('check');p.add_argument('input')
    args=parser.parse_args()
    try:
        if args.command=='export':
            bank=export(loads(Path(args.input).read_text(encoding='utf-8-sig')),args.select,args.tag,args.bundle)
            text=render(bank)
        else:
            bank=read_bank(args.input)
            if args.command=='check':
                source=Path(args.input).read_text(encoding='utf-8-sig').strip()
                integrity='not supplied' if source.startswith('{') or source.endswith('SHA256: UNVERIFIED') else 'verified'
                print('Bank structure checked. Integrity hash: '+integrity+'. Entries: '+str(len(bank['entries']))+'. Dependencies and IW runtime not verified.');return 0
            text=render(bank) if args.command=='pack' else dumps(restore(bank) if args.command=='restore' else bank)
        write(args.out,text)
        # A real parse-back check, not a model's visual inspection.
        if args.command in ('export','pack'):
            if digest(read_bank(args.out))!=digest(bank): raise ValueError('Round-trip verification failed')
        elif args.command=='restore':
            if digest(loads(Path(args.out).read_text()))!=bank['source']['sha256']: raise ValueError('Restore verification failed')
        print('Wrote '+args.out)
        return 0
    except (ValueError,KeyError,IndexError,TypeError,OSError,RecursionError) as exc:
        print('Data bank error: '+str(exc),file=sys.stderr);return 1

if __name__=='__main__': sys.exit(main())
