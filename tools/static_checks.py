"""Conservative static diagnostics. Not a PawScript parser or JSON Schema implementation."""
from __future__ import annotations
import json,re,hashlib

SYSTEM_ROOTS={'game','player','turn_number'}
ROOT=re.compile(r'\$([A-Za-z_][A-Za-z_0-9]*)')
PLACEHOLDERS=re.compile(r'\[(?:LIST [A-Z _]+|DESCRIBE [A-Z _]+|Author Style|title|blurb)\]|<#\s*(?:time period|Copy in|DESCRIBE|LIST |VARIABLE BLOCK)[\s\S]*?#>',re.I)

def escaped(k):return str(k).replace('~','~0').replace('/','~1')
def walk(value,path=''):
    if isinstance(value,dict):
        for k,v in value.items():yield from walk(v,path+'/'+escaped(k))
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from walk(v,path+'/'+str(i))
    elif isinstance(value,str):yield path,value

def mask_literals(code):
    """Mask single/double quoted strings and # comments without changing line positions."""
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\#[^\n]*',lambda m:''.join('\n' if c=='\n' else ' ' for c in m.group()),code)

def templates(text):
    """Extract <<...>> while respecting quoted >>; unmatched delimiters are not parsed."""
    text=re.sub(r'<#[\s\S]*?#>',lambda m:' '*len(m.group()),text)
    pos=0
    while True:
        start=text.find('<<',pos)
        if start<0:return
        i=start+2;quote=None;escape=False
        while i<len(text):
            ch=text[i]
            if quote:
                if escape:escape=False
                elif ch=='\\':escape=True
                elif ch==quote:quote=None
            elif ch in ['"',"'"]:quote=ch
            elif text.startswith('>>',i):
                yield text[start+2:i];pos=i+2;break
            i+=1
        else:return

def lint(doc):
    findings=[]
    def add(code,path,message):findings.append(dict(severity='warning',code=code,path=path or '/',message=message))
    declared={x.get('variableName') for x in doc.get('trackedItems',[]) if isinstance(x,dict) and isinstance(x.get('variableName'),str)}
    snippets=[];script_paths=set()
    def nodes(x,path=''):
        if isinstance(x,dict):
            typ=x.get('type')
            if typ in ['effectRunScript','triggerOnPawScript','triggerOnRandomChance'] and isinstance(x.get('data'),str):
                sp=path+'/data';snippets.append((sp,x['data'],typ=='effectRunScript'));script_paths.add(sp)
            for k,v in x.items():
                kp=path+'/'+escaped(k)
                if k in ['initialPCValueChoicesScript','initialValueChoicesScript'] and isinstance(v,str) and v.strip():snippets.append((kp,v,False));script_paths.add(kp)
                nodes(v,kp)
        elif isinstance(x,list):
            for i,v in enumerate(x):nodes(v,path+'/'+str(i))
    nodes(doc)
    for path,text in walk(doc):
        markers=sorted(set(re.findall(r'<#\s*(?:END_)?(REPLACE\d+)\b[\s\S]*?#>',text)))
        if markers:add('content-substitution',path,'Intentional content substitution marker(s): '+', '.join(markers)+'. Review the separate Authoring report and intended behavior; these are not import errors.')
        if PLACEHOLDERS.search(text):add('authoring-placeholder',path,'Possible unresolved library editing slot. Review; intentional runtime notation and ordinary comments need not be removed.')
        if path not in script_paths:
            for expr in templates(text):snippets.append((path,expr,False))
    for path,code,is_script in snippets:
        clean=mask_literals(code)
        locals_=set(re.findall(r'\b(?:set|for\s+each)\s+\$([A-Za-z_][A-Za-z_0-9]*)',clean)) if is_script else set()
        unknown=set(ROOT.findall(clean))-declared-SYSTEM_ROOTS-locals_
        for name in sorted(unknown):
            if path.startswith('/videoPromptInstructions') and name in ['videoDuration','videoStyle']:
                add('context-root-unverified',path,'Video-context $'+name+' is not a declared tracker; availability in this field is not established by this kit.')
            else:add('unknown-script-root',path,'$'+name+' is not a declared tracker variableName, script local, or known system root. Check missing dependencies; lint is not a full language/context parser.')
        for token in ['==','&&','||']:
            if token in clean:add('borrowed-syntax',path,'Review '+token+'; PawScript uses =, and, or in expressions.')
        if re.search(r'^\s*(?:if\b|else\s+if\b|else\b|for\b).*:\s*$',clean,re.M):add('borrowed-syntax',path,'Branch/loop header ends with a colon; PawScript uses indentation without a colon.')
        if re.search(r'[{};]',clean):add('borrowed-syntax',path,'Unquoted braces or semicolon found; review for borrowed block/object syntax.')
        # Identify quoted-string + operand without looking inside literal text.
        lit=re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
        for m in lit.finditer(code):
            if re.match(r'\s*\+\s*(?:\$|["\'])',clean[m.end():]) or re.search(r'\$[\w.()]+\s*\+\s*$',clean[:m.start()]):
                add('string-plus',path,'Possible string concatenation with +; use &. Review this heuristic warning.');break
    findings.extend(pattern_advisories(doc))
    return findings

def basic_errors(value,schema,root=None,path=''):
    """A limited type/requiredness guard used without jsonschema. Coverage is explicitly reduced."""
    root=root or schema;out=[]
    if not isinstance(schema,dict):return out
    if '$ref' in schema:
        target=root
        for part in schema['$ref'].lstrip('#/').split('/'):target=target.get(part,{})
        return basic_errors(value,target,root,path)
    if schema.get('x-discriminator') and isinstance(value,dict):
        prefix='effect' if str(value.get('type','')).startswith('effect') else 'condition'
        target=root.get('$defs',{}).get(prefix+'_'+str(value.get('type')))
        if target:return basic_errors(value,target,root,path)
    if 'anyOf' in schema:
        branches=[basic_errors(value,s,root,path) for s in schema['anyOf']]
        if any(not x for x in branches):return []
        return [dict(severity='error',code='basic-structure',path=path or '/',message='Value does not match the checked type alternatives (reduced validation).')]
    if 'not' in schema and not basic_errors(value,schema['not'],root,path):
        return [dict(severity='error',code='basic-structure',path=path or '/',message='Excluded alternative (reduced validation).')]
    for sub in schema.get('allOf',[]):out+=basic_errors(value,sub,root,path)
    typ=schema.get('type')
    types={'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str),'boolean':isinstance(value,bool),'integer':isinstance(value,int) and not isinstance(value,bool),'number':isinstance(value,(int,float)) and not isinstance(value,bool),'null':value is None}
    def error(msg):out.append(dict(severity='error',code='basic-structure',path=path or '/',message=msg))
    if typ and not any(types.get(t,False) for t in (typ if isinstance(typ,list) else [typ])):error('Expected '+str(typ));return out
    if 'const'in schema and value!=schema['const']:error('Constant value mismatch.')
    if 'enum'in schema and value not in schema['enum']:error('Value is outside the declared enum.')
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        if 'minimum'in schema and value<schema['minimum']:error('Below minimum.')
        if 'maximum'in schema and value>schema['maximum']:error('Above maximum.')
    if isinstance(value,dict):
        for k in schema.get('required',[]):
            if k not in value:error('Missing required field '+k)
        for k,v in value.items():
            sub=schema.get('properties',{}).get(k,schema.get('additionalProperties',{}))
            if isinstance(sub,dict):out+=basic_errors(v,sub,root,path+'/'+escaped(k))
    if isinstance(value,list):
        if len(value)<schema.get('minItems',0):error('Too few items.')
        if 'maxItems'in schema and len(value)>schema['maxItems']:error('Too many items.')
        for i,v in enumerate(value):out+=basic_errors(v,schema.get('items',{}),root,path+'/'+str(i))
    return out

def edit_diff(old,new):
    changes=[]
    def brief(v):
        if isinstance(v,str) and len(v)>160:return {'preview':v[:160],'characters':len(v),'sha256':hashlib.sha256(v.encode('utf-8')).hexdigest()}
        return v
    def compare(a,b,path=''):
        if type(a)!=type(b):changes.append({'path':path or '/','change':'type/value','before':brief(a),'after':brief(b)});return
        if isinstance(a,dict):
            for k in sorted(set(a)|set(b)):
                q=path+'/'+escaped(k)
                if k not in a:changes.append({'path':q,'change':'added','after':brief(b[k])})
                elif k not in b:changes.append({'path':q,'change':'removed','before':brief(a[k])})
                else:compare(a[k],b[k],q)
        elif isinstance(a,list):
            if a!=b:
                for i in range(max(len(a),len(b))):
                    q=path+'/'+str(i)
                    if i>=len(a):changes.append({'path':q,'change':'added','after':brief(b[i])})
                    elif i>=len(b):changes.append({'path':q,'change':'removed','before':brief(a[i])})
                    else:compare(a[i],b[i],q)
        elif a!=b:changes.append({'path':path,'change':'changed','before':brief(a),'after':brief(b)})
    compare(old,new)
    objects={}
    for field,idkey in [('trackedItems','id'),('triggerEvents','id'),('possibleCharacters','characterId'),('instructionBlocks','id'),('loreBookEntries','id'),('NPCs','id')]:
        def lookup(w):return {x[idkey]:x for x in w.get(field,[]) if isinstance(x,dict) and isinstance(x.get(idkey),str)} if isinstance(w,dict) and isinstance(w.get(field,[]),list) else {}
        a,b=lookup(old),lookup(new)
        objects[field]={'added':sorted(b.keys()-a.keys()),'removed':sorted(a.keys()-b.keys()),'changed':sorted(k for k in a.keys()&b.keys() if a[k]!=b[k]),'orderChanged':list(a)!=list(b)}
    return {'objects':objects,'changes':changes,'note':'Reports differences, not whether they are authorized. Array indices are positional; object summaries match IDs.'}


def pattern_advisories(doc):
    """Narrow review prompts, never proof of a missing guard or invalid runtime behavior."""
    out=[]
    def add(code,path,message):out.append(dict(severity='warning',code=code,path=path,message=message))
    triggers=doc.get('triggerEvents',[])
    if not isinstance(triggers,list):return out
    for i,t in enumerate(triggers):
        if not isinstance(t,dict):continue
        effects=t.get('triggerEffects',[])
        if not isinstance(effects,list):continue
        for j,e in enumerate(effects):
            if not isinstance(e,dict):continue
            typ=e.get('type');d=e.get('data');path=f'/triggerEvents/{i}/triggerEffects/{j}/data'
            if typ=='effectRunScript' and isinstance(d,str):
                clean=mask_literals(d)
                if t.get('canTriggerMoreThanOnce') and re.search(r'^\s*\$[\w.]+\s*\+=',clean,re.M):
                    add('review-repeat-accumulation',path,'Repeatable script accumulates a value. Review its completion/consumption guard if this is a one-time reward; recurring counters are valid. No missing guard is inferred.')
                if any(isinstance(x,dict) and x.get('type')=='effectRunScript' for x in effects[:j]):
                    add('review-script-boundary',path,'Earlier Run Script effects have separate locals and rollback. Keep an accepted-state commit and its completion flag together if they must succeed together.')
            if typ=='effectPresentChoice' and isinstance(d,dict):
                if d.get('selectionMode')=='multiple':
                    add('review-choice-storage',path,'Multiple selections can be newline-delimited text. Validate the intended domain and representation before treating this value as a YAML list.')
                if isinstance(d.get('choices'),str) and '<<' in d['choices']:
                    add('review-choice-domain',path,'Choices are computed. Review blank/duplicate values, fallback and membership checks at the point where the answer is consumed; display choices alone do not validate all write paths.')
    draws=[]
    for path,text in walk(doc):
        if not any(k in path for k in ('/content','/instructions','/descriptionRequest')):continue
        for expr in templates(text):
            if re.search(r'\b(?:random|random_between|dice_roll)\s*\(',mask_literals(expr)):draws.append(path)
    if len(draws)>1:
        add('review-independent-random',draws[0],'Several rendered expressions draw independently. Cache a single choice in a tracker when these consumers must agree; independent draws are otherwise valid.')
    return out
