"""Loss-aware read-only comparison of source and native re-exported worlds.
Usage: python tools/import_audit.py SOURCE.json IMPORTED.json
Reports differences and possible reminting, never rewrites either input.
"""
from pathlib import Path
import argparse, hashlib, json
from static_checks import edit_diff
from validate_iw_export import validate, Draft202012Validator

def audit_import(before, after):
    def rows(w): return [x for x in w.get('trackedItems',[]) if isinstance(x,dict)]
    old,new=rows(before),rows(after)
    old_ids={x.get('id') for x in old if isinstance(x.get('id'),str)}
    new_ids={x.get('id') for x in new if isinstance(x.get('id'),str)}
    changes=[]
    for x in old:
        if x.get('id') in new_ids: continue
        candidates=[y for y in new if isinstance(x.get('name'),str) and x['name'] and isinstance(x.get('variableName'),str) and x['variableName'] and y.get('id') not in old_ids and y.get('name')==x.get('name') and y.get('variableName')==x.get('variableName')]
        changes.append({'objectName':x.get('name'),'variableName':x.get('variableName'),'oldId':x.get('id'),'status':'possible-remint' if len(candidates)==1 else 'removed-or-ambiguous','candidateIds':[y.get('id') for y in candidates]})
    dangling=[]
    def scan(value,path=''):
        if isinstance(value,dict):
            for k,v in value.items():
                q=path+'/'+str(k).replace('~','~0').replace('/','~1')
                is_pc=k=='id' and '/initialTrackedItemValues/' in q
                if (k in ('trackedItemID','targetTrackedItemId') or is_pc) and isinstance(v,str) and v in old_ids-new_ids:
                    names=[x.get('name') for x in old if x.get('id')==v]
                    dangling.append({'path':q,'targetNames':names,'oldId':v})
                scan(v,q)
        elif isinstance(value,list):
            for i,v in enumerate(value):scan(v,path+'/'+str(i))
    scan(after)
    return {'trackerIdentityChanges':changes,'referencesToRemovedTrackers':dangling,'diff':edit_diff(before,after),'note':'Possible reminting is a name/handle-based candidate, not an automatic identity decision. Positional changes and omissions are preserved in diff; no repair performed.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('imported',type=Path);a=p.parse_args()
    try:
        raw=[p.read_bytes() for p in (a.source,a.imported)]; docs=[json.loads(b.decode('utf-8-sig')) for b in raw]
        if not all(isinstance(d,dict) for d in docs):raise ValueError('World roots must be objects')
        schema=json.loads(Path(__file__).with_name('iw-export.schema.json').read_text())
        out=audit_import(*docs);out['sourceHashes']=[hashlib.sha256(b).hexdigest() for b in raw]
        out['importFindings']=validate(docs[1],schema);out['fullSchema']=Draft202012Validator is not None
    except (OSError,ValueError) as e:p.exit(2,str(e)+'\n')
    print(json.dumps(out,indent=2,ensure_ascii=False))
    return int(bool(out['referencesToRemovedTrackers']) or any(f['severity']=='error' for f in out['importFindings']))
if __name__=='__main__':raise SystemExit(main())
