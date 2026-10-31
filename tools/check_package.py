"""Validate distributed worlds, references and documentation links. Does not execute IW."""
from pathlib import Path
from urllib.parse import unquote
import json,re,copy,collections
from validate_iw_export import validate, Draft202012Validator
from build_distribution import manifest_paths, KIT_VERSION
ROOT=Path(__file__).resolve().parent.parent
assert Draft202012Validator is not None, 'Maintainer package checks require jsonschema; user validation supports reduced coverage.'
schema=json.loads((ROOT/'tools/iw-export.schema.json').read_text(encoding='utf-8'))
worlds=[ROOT/'World-Template.json',ROOT/'library/Sample-Blocks.json',*sorted((ROOT/'examples').glob('*.json'))]
worlds=[p for p in worlds if p.name!='index.json']
results={}
for path in worlds:
 doc=json.loads(path.read_text(encoding='utf-8'));findings=validate(doc,schema)
 assert not [f for f in findings if f['severity']=='error'],(path,findings)
 assert path.read_bytes().endswith(b'}'),path
 if path.parent.name=='examples':
  assert not [f for f in findings if f['code'] in ['unknown-script-root','borrowed-syntax','string-plus','authoring-placeholder']],(path,findings)
 results[path.relative_to(ROOT).as_posix()]={'errors':0,'warnings':dict(collections.Counter(f['code'] for f in findings))}
# Check only publication inputs, not installed packages in a local .venv.
for doc in (p for p in manifest_paths() if p.suffix == '.md'):
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
  if '://' not in link and not link.startswith('#'):
   assert (doc.parent/unquote(link.split('#')[0])).exists(),(doc,link)
for item in json.loads((ROOT/'examples/index.json').read_text(encoding='utf-8')):assert (ROOT/'examples'/item['file']).exists()
base=json.loads((ROOT/'World-Template.json').read_text(encoding='utf-8'));assert not base['trackedItems'] and not base['triggerEvents']
skill=next(iter(base['possibleCharacters'][0]['skills']))
negative=[]
for level in [-1,6]:
 bad=copy.deepcopy(base);bad['possibleCharacters'][0]['skills'][skill]=level
 assert any(f['severity']=='error' for f in validate(bad,schema));negative.append('Out-of-range skill '+str(level))
choice=json.loads((ROOT/'examples/effect-effectPresentChoice.json').read_text(encoding='utf-8'))
for t in choice['triggerEvents']:
 for e in t['triggerEffects']:
  if e['type']=='effectPresentChoice':e['data']['targetTrackedItemId']='missing-tracker'
assert any(f['severity']=='error' for f in validate(choice,schema));negative.append('Missing input tracker target')
sample=json.loads((ROOT/'library/Sample-Blocks.json').read_text(encoding='utf-8'))
def no_previews(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='previewImageOptions':assert v==[]
   no_previews(v)
 elif isinstance(x,list):
  for v in x:no_previews(v)
no_previews(sample)
# Hedge density: a kit-wide caveat belongs in one place (the top of reference/Verified-Behavior.md), not re-attached to
# individual sentences. Count the phrase families that do that and warn when a document leans on them.
HEDGES=[r"\bnot (?:a |an )?(?:guarantee|proof|evidence|substitute|promise)\b",r"\b(?:does|do|did) not (?:prove|certify|establish|guarantee|automatically)\b",
 r"\b(?:do|does) not (?:invent|infer|assume|claim|promise|treat|present|turn|read)\b",r"\bnever (?:invent|assume|claim)\b",r"\bnot established\b",
 r"\bremains? (?:unresolved|unverified|unknown)\b",r"\bnot (?:a |an )?(?:contract|requirement|mandatory)\b",r"\bnot (?:a |an )?(?:official|exhaustive|complete) \w+"]
HEDGE_CEILING=3.0  # per 1,000 words
hedges={};hedge_warnings=[]
from build_distribution import document_paths
for rel in document_paths():
 text=(ROOT/rel).read_text(encoding='utf-8');words=max(1,len(text.split()))
 hits=sum(len(re.findall(h,text,re.I)) for h in HEDGES);density=round(hits/words*1000,1)
 hedges[rel]={'hedgePhrases':hits,'perThousandWords':density}
 if density>HEDGE_CEILING:hedge_warnings.append(rel+' ('+str(density)+'/1k words)')
report={'kitVersion':KIT_VERSION,'hedgeDensity':hedges,'hedgeWarnings':hedge_warnings,'schemaProfileVersion':schema['x-profileVersion'],'structuralValidation':results,'negativeChecks':negative,'localMarkdownLinks':'passed','nativeRuntimeExecutedByChecker':False,'scope':'Structural and explicit-reference validation; runtime status is listed separately in examples/index.json.'}
(ROOT/'tools/Validation-Report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'worldFilesChecked':len(results),'structuralErrors':0,'localLinks':'passed','negativeChecks':len(negative),'hedgeWarnings':hedge_warnings,'nativeRuntimeExecuted':False}))
