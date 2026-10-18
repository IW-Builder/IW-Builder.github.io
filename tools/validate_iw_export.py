#!/usr/bin/env python3
"""Validate observed IW export structure, references, and evidence gaps.

Usage: python validate_iw_export.py WORLD.json [--schema SCHEMA.json] [--json]
Exit codes: 0 = no errors (warnings permitted), 1 = validation errors,
2 = input failure. jsonschema is optional; reduced coverage is reported when absent. Never executes PawScript.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from static_checks import lint, basic_errors, edit_diff
try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

def pointer(parts):
    return '/'+'/'.join(str(p).replace('~','~0').replace('/','~1') for p in parts) if parts else '/'

def validate(doc, schema):
    findings=[]
    def add(level,code,path,message):
        findings.append({'severity':level,'code':code,'path':path,'message':message})
    if Draft202012Validator is not None:
        Draft202012Validator.check_schema(schema)
        for e in sorted(Draft202012Validator(schema).iter_errors(doc),key=lambda e:str(list(e.path))):
            add('error','structure',pointer(e.path),e.message)
    else:
        add('warning','schema-validation-unavailable','/','jsonschema is unavailable. Full JSON Schema validation was NOT run; limited type guards, references and static lint remain available.')
        findings.extend(basic_errors(doc,schema))
    if not isinstance(doc,dict): return findings
    if any(f['severity']=='error' for f in findings): return findings
    defs=schema.get('$defs',{})

    def resolved(s,value):
        if '$ref' in s:
            key=s['$ref'].rsplit('/',1)[-1]
            if key=='conditionNode' and isinstance(value,dict):
                if value.get('category')=='logic': return defs[key]['anyOf'][0]
                if value.get('category')=='condition': return resolved(defs['conditionLeaf'],value)
                return {}
            return resolved(defs[key],value)
        tag=s.get('x-discriminator')
        if tag and isinstance(value,dict):
            val=value.get(tag)
            prefix='effect' if tag=='type' and s is defs.get('effect') else 'condition'
            return defs.get(prefix+'_'+str(val),{})
        if 'anyOf' in s:
            matches=[x for x in s['anyOf'] if not basic_errors(value,x,schema)]
            return resolved(matches[0],value) if matches else {}
        return s

    def audit(value,s,path):
        s=resolved(s,value)
        observed=s.get('x-observedValues')
        if observed is not None and value not in observed:
            add('warning','unobserved-value',path,'Value is outside observed vocabulary; not declared invalid: '+repr(value))
        if isinstance(value,dict) and s.get('type')=='object':
            props=s.get('properties',{})
            for k,v in value.items():
                p=path.rstrip('/')+'/'+str(k).replace('~','~0').replace('/','~1')
                if k not in props:
                    extra=s.get('additionalProperties')
                    if isinstance(extra,dict): audit(v,extra,p)
                    else: add('warning','unobserved-field',p,'Field has no characterized schema at this location.')
                else: audit(v,props[k],p)
        elif isinstance(value,list) and s.get('type')=='array':
            for i,v in enumerate(value): audit(v,s.get('items',{}),path.rstrip('/')+'/'+str(i))
    audit(doc,schema,'/')
    if doc.get('schemaVersion') not in schema.get('x-observedSchemaVersions',[]):
        add('warning','schema-version','/schemaVersion','Version missing or outside observed versions; profile coverage is not established.')

    tables={}
    for field,idkey in [('trackedItems','id'),('triggerEvents','id'),('possibleCharacters','characterId'),('instructionBlocks','id'),('loreBookEntries','id'),('NPCs','id')]:
        tables[field]={}
        for i,o in enumerate(doc.get(field,[]) if isinstance(doc.get(field,[]),list) else []):
            if not isinstance(o,dict): continue
            p='/'+field+'/'+str(i)+'/'+idkey
            ident=o.get(idkey)
            if not isinstance(ident,str) or not ident:
                add('warning','missing-id',p,'No usable identifier; requiredness is not established, but references cannot resolve.');continue
            if ident in tables[field]: add('error','duplicate-id',p,'Identifier is duplicated within '+field+': '+ident)
            tables[field][ident]=o
    def ref(ident,namespace,path,condition=False):
        if not isinstance(ident,str): return
        if ident in tables[namespace]: return
        if condition and ident in schema.get('x-observedConditionExternalReferences',[]):
            if ident=='skill_player_skill_1' and 'Player - Skill 1' not in doc.get('skills',[]):
                add('warning','skill-binding',path,'Observed skill variable used without its sample skill name; general binding rule is unknown.')
            return
        if condition and ident.startswith('skill_'):
            add('warning','unknown-skill-reference',path,'Unobserved built-in skill reference; normalization and binding not verified.');return
        add('error','unresolved-reference',path,'No declared '+namespace+' target: '+ident)

    seen_node_ids={}
    def node_id(n,p):
        ident=n.get('id')
        if not isinstance(ident,str) or not ident:
            add('warning','missing-node-id',p+'/id','Condition/effect node has no usable ID; importer requirements unknown.')
        elif ident in seen_node_ids: add('warning','duplicate-node-id',p+'/id','Node ID is reused at '+seen_node_ids[ident])
        else: seen_node_ids[ident]=p
    def compare_wrapper(n,d,p):
        for k in ('trackedItemID','inequality'):
            if k in n and k in d and n[k]!=d[k]:
                add('error','wrapper-payload-mismatch',p+'/'+k,'Wrapper and payload disagree; runtime precedence unknown.')
    def conditions(nodes,p):
        for i,n in enumerate(nodes if isinstance(nodes,list) else []):
            q=p+'/'+str(i)
            if not isinstance(n,dict): continue
            node_id(n,q)
            category=n.get('category')
            if category=='logic':
                if n.get('operator') not in ['and','or','none_of']: add('warning','unknown-logic',q+'/operator','Unobserved operator.')
                if 'data' not in n: add('warning','missing-payload',q+'/data','Logic group has no child list.')
                conditions(n.get('data',[]),q+'/data');continue
            if category!='condition': add('warning','unclassified-condition',q+'/category','Missing or unobserved category.')
            t=n.get('type'); d=n.get('data')
            if t not in defs['conditionLeaf']['x-knownDiscriminators']:
                add('warning','unknown-condition-type',q+'/type','Missing or unobserved condition type: '+repr(t));continue
            if 'data' not in n: add('warning','missing-payload',q+'/data','No condition payload observed.');continue
            if isinstance(d,dict): compare_wrapper(n,d,q)
            if t=='triggerOnCharacter' and isinstance(d,list):
                for j,x in enumerate(d): ref(x,'possibleCharacters',q+'/data/'+str(j))
            elif t=='triggerOnTrackedItem' and isinstance(d,dict):
                ref(d.get('trackedItemID'),'trackedItems',q+'/data/trackedItemID',condition=True)
            elif t in ['triggerPrereqs','triggerBlockers'] and isinstance(d,dict):
                key='prereqs' if t=='triggerPrereqs' else 'blockers'
                for j,x in enumerate(d.get(key,[]) if isinstance(d.get(key,[]),list) else []): ref(x,'triggerEvents',q+'/data/'+key+'/'+str(j))
            elif t=='triggerOnEvent' and isinstance(d,str) and d not in doc.get('conditions',[]):
                add('warning','unlisted-situation',q+'/data','Situation string not in root conditions registry; whether registry membership is mandatory is unknown.')
            elif t=='triggerOnPawScript': add('warning','unverified-expression',q+'/data','Expression is stored text; not parsed or executed.')
    for i,t in enumerate(doc.get('triggerEvents',[]) if isinstance(doc.get('triggerEvents',[]),list) else []):
        if not isinstance(t,dict): continue
        p='/triggerEvents/'+str(i)
        if t.get('triggerMidGame') and not t.get('triggerOnStartOfGame'):
            add('warning','timing-editor-consistency',p,'Mid-game enabled without start-of-game; editor-inconsistent, runtime effect unverified.')
        if not t.get('triggerOnStartOfGame') and not t.get('triggerConditions'):
            add('warning','saved-inactive-trigger',p,'Valid saved trigger with no ordinary automatic firing conditions; explicit random dispatch may still call it.')
        numeric_writes={}
        flat_req=set();flat_block=set()
        for n in t.get('triggerConditions',[]):
            if isinstance(n,dict) and n.get('category')=='condition' and isinstance(n.get('data'),dict):
                data=n['data'];scope=data.get('firedThisTurn',False)
                if n.get('type')=='triggerPrereqs':flat_req.update((x,scope) for x in data.get('prereqs',[]))
                if n.get('type')=='triggerBlockers':flat_block.update((x,scope) for x in data.get('blockers',[]))
        if flat_req & flat_block:add('warning','dependency-editor-conflict',p,'Flat AND prerequisites and blockers conflict within the same scope.')
        for e in t.get('triggerEffects',[]):
            if isinstance(e,dict) and e.get('type')=='effectSetTrackedItemValue' and isinstance(e.get('data'),dict):
                ident=e['data'].get('trackedItemID')
                if tables['trackedItems'].get(ident,{}).get('dataType')=='number':numeric_writes[ident]=numeric_writes.get(ident,0)+1
        for ident,count in numeric_writes.items():
            if count>1:add('warning','numeric-write-overwrite',p,'Multiple numeric writes to '+ident+' can overwrite rather than accumulate within one trigger.')
        conditions(t.get('triggerConditions',[]),p+'/triggerConditions')
        for j,e in enumerate(t.get('triggerEffects',[]) if isinstance(t.get('triggerEffects',[]),list) else []):
            q=p+'/triggerEffects/'+str(j)
            if not isinstance(e,dict):continue
            node_id(e,q); et=e.get('type');d=e.get('data')
            if et not in defs['effect']['x-knownDiscriminators']:
                add('warning','unknown-effect-type',q+'/type','Missing or unobserved effect type: '+repr(et));continue
            if 'data' not in e: add('warning','missing-payload',q+'/data','No effect payload.');continue
            if isinstance(d,dict):
                compare_wrapper(e,d,q)
                if et in ['effectSetTrackedItemValue','effectModifyTrackedItemDetails']:
                    ref(d.get('trackedItemID'),'trackedItems',q+'/data/trackedItemID')
                elif et in ['effectPresentChoice','effectRequestInput']:
                    ref(d.get('targetTrackedItemId'),'trackedItems',q+'/data/targetTrackedItemId')
                elif et=='effectModifyInstructionBlock': ref(d.get('id'),'instructionBlocks',q+'/data/id')
                elif et=='effectModifyKeywordBlock': ref(d.get('id'),'loreBookEntries',q+'/data/id')
                elif et=='effectChangePCSkill' and d.get('name') not in doc.get('skills',[]):
                    add('error','unresolved-skill',q+'/data/name','Skill name is not declared in root skills.')
            if et=='effectFireRandomTrigger' and isinstance(d,list):
                for k,x in enumerate(d):
                    if x!='nothing':ref(x,'triggerEvents',q+'/data/'+str(k))
            if et=='effectRunScript':add('warning','unverified-script',q+'/data','Script is stored text; validity/write capabilities not checked.')

    variables={}
    for i,t in enumerate(doc.get('trackedItems',[]) if isinstance(doc.get('trackedItems',[]),list) else []):
        if not isinstance(t,dict):continue
        p='/trackedItems/'+str(i)
        v=t.get('variableName')
        if isinstance(v,str) and v:
            if v in variables:add('warning','duplicate-variable',p+'/variableName','Repeated variable name; binding ambiguity not resolved.')
            variables[v]=p
        if t.get('dataType')=='number' and t.get('initialValueBasedOnPC')=='same':
            val=t.get('initialValue')
            if isinstance(val,str) and not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?',val.strip()):
                add('warning','numeric-initialization',p+'/initialValue','Number tracker does not contain a plain numeric literal; expression/runtime meaning unverified.')
    for i,c in enumerate(doc.get('possibleCharacters',[]) if isinstance(doc.get('possibleCharacters',[]),list) else []):
        if not isinstance(c,dict):continue
        for name in c.get('skills',{}) if isinstance(c.get('skills'),dict) else []:
            if name not in doc.get('skills',[]):add('warning','undeclared-character-skill','/possibleCharacters/'+str(i)+'/skills/'+name,'Character skill is not in root skill list.')
        for j,v in enumerate(c.get('initialTrackedItemValues',[]) if isinstance(c.get('initialTrackedItemValues',[]),list) else []):
            if not isinstance(v,dict):continue
            q='/possibleCharacters/'+str(i)+'/initialTrackedItemValues/'+str(j)
            ref(v.get('id'),'trackedItems',q+'/id')
            target=tables['trackedItems'].get(v.get('id'),{})
            val=v.get('initialPCValue')
            choices_script=v.get('initialPCValueChoicesScript')
            if isinstance(choices_script,str) and choices_script.strip():
                add('warning','unverified-choice-expression',q+'/initialPCValueChoicesScript','Startup choice expression is stored text; not evaluated. Empty initialPCValue is expected in the observed script mode.')
            elif target.get('dataType')=='number' and isinstance(val,str) and not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?',val.strip()):
                add('warning','numeric-character-initialization',q+'/initialPCValue','Number tracker has a nonnumeric per-character sample; runtime meaning unverified.')
    findings.extend(lint(doc))
    return findings

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('world',type=Path);p.add_argument('--schema',type=Path,default=Path(__file__).with_name('iw-export.schema.json'));p.add_argument('--json',action='store_true');p.add_argument('--diff',type=Path,metavar='OLD.json',help='Compare object IDs and changed fields against an earlier export.')
    args=p.parse_args()
    try:
        raw=args.world.read_bytes();doc=json.loads(raw.decode('utf-8-sig')); schema=json.loads(args.schema.read_text(encoding='utf-8'));findings=validate(doc,schema)
        if raw != raw.rstrip() and (b'\n' in raw[len(raw.rstrip()):] or b'\r' in raw[len(raw.rstrip()):]):findings.append({'severity':'warning','code':'trailing-newline','path':'/','message':'Remove the final newline before pasting into IW; the import text should end at its final brace.'})
        diff=edit_diff(json.loads(args.diff.read_text(encoding='utf-8-sig')),doc) if args.diff else None
    except (OSError,ValueError) as exc:
        print(str(exc),file=sys.stderr);return 2
    result={'file':str(args.world),'errors':sum(f['severity']=='error' for f in findings),'warnings':sum(f['severity']=='warning' for f in findings),'findings':findings,'coverage':{'fullSchema':Draft202012Validator is not None,'staticLint':True,'runtimeExecution':False}}
    if diff is not None:result['diff']=diff
    if args.json:print(json.dumps(result,indent=2,ensure_ascii=False))
    else:
        print(f"{result['errors']} errors; {result['warnings']} warnings")
        if diff is not None:print(json.dumps({'diff':diff},indent=2,ensure_ascii=False))
        for f in findings:print(f"{f['severity'].upper()} {f['code']} {f['path']}: {f['message']}")
    return int(result['errors']>0)

if __name__=='__main__':sys.exit(main())
