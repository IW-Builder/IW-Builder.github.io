"""Validate distributed worlds, references and documentation links. Does not execute IW."""
from pathlib import Path
from urllib.parse import unquote
import json,re,copy,collections
from validate_iw_export import validate, Draft202012Validator
from build_distribution import manifest_paths
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
 results[str(path.relative_to(ROOT))]={'errors':0,'warnings':dict(collections.Counter(f['code'] for f in findings))}
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
report={'kitVersion':'1.4.0','schemaProfileVersion':schema['x-profileVersion'],'structuralValidation':results,'negativeChecks':negative,'localMarkdownLinks':'passed','nativeRuntimeExecutedByChecker':False,'scope':'Structural and explicit-reference validation; runtime status is listed separately in examples/index.json.'}
(ROOT/'tools/Validation-Report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'worldFilesChecked':len(results),'structuralErrors':0,'localLinks':'passed','negativeChecks':len(negative),'nativeRuntimeExecuted':False}))
