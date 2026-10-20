"""Generate upload-oriented text files from the modular sources; no independent edits."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'chat'
GUIDE=['Authoring-Prompt.md','World-Template.json','reference/Evidence.md','reference/Craft.md','reference/Portable-Banks.md','reference/Trackers.md','reference/Triggers.md','reference/Schema.md','reference/PawScript.md','reference/Capabilities.md','reference/Recipes.md','reference/Import-Integrity.md','reference/Known-Limits.md','reference/Default-Evaluation.txt','reference/Current-AI-Profiles.json']
GROUPS={
 'IW-Authoring-Guide.txt':GUIDE,
 'IW-Examples.txt':['examples/Payloads.md','examples/index.json','examples/narrative-vendemmia.json','examples/recipe-request-commit.json','examples/recipe-choice-followup.json','examples/recipe-threshold-unlock.json','examples/optional-block.json','examples/showcase-glass-ledger.json','examples/character-starting-values.json'],
 'IW-Sample-Library.txt':['library/Integration.md','library/Sample-Blocks.json','library/Storymaster-Suite.json']}

def tool_sources():
 """Include tool source, documentation and data; omit caches and binary files."""
 suffixes={'.py','.json','.md','.txt','.js','.mjs','.toml','.yaml','.yml','.sh','.bat','.ps1'}
 files=[]
 for path in (ROOT/'tools').rglob('*'):
  relative=path.relative_to(ROOT)
  if (path.is_file() and path.suffix.lower() in suffixes
      and path.name.lower() != 'readme.md'
      and not any(part.startswith('.') or part=='__pycache__' for part in relative.parts)):
   files.append(relative.as_posix())
 return sorted(files, key=lambda path: (path!='tools/Usage.md',path))

def build():
 OUT.mkdir(exist_ok=True);manifest={}
 groups={**GROUPS,'IW-Tools.txt':tool_sources()}
 for name,files in groups.items():
  intro='Infinite Worlds Authoring Kit: generated text edition. Source paths below identify sections within this upload. This is reference material, not one JSON world to import. The Examples edition includes all native payload snippets plus selected complete recipes; other complete worlds remain in the full kit and can be requested by path. Follow Authoring-Prompt.md for the authoring task. Load referenced material selectively; ask for a missing companion when required. Do not claim the Python validator ran unless actual execution tools and the full tools folder are available.\n\n'
  if name=='IW-Tools.txt':
   intro='Infinite Worlds Authoring Kit: combined tools text edition. Each BEGIN FILE / END FILE section contains one tool source, documentation or data file, identified by its package-relative path. This upload is not a single executable script or an IW world. To run a tool, recreate the needed files at their indicated paths, excluding the boundary lines and separator newlines. Preserve indentation and string escaping. Follow tools/Usage.md for dependencies, commands and coverage limits. This bundle includes the validator, schema, static checks, tests, maintainer utilities and any packaged reports; a report describes its stated inputs, not a newly authored world. Some maintainer tools require examples and other kit files outside this bundle. Reading these sources is not running them; claim validation only after actual execution and report the coverage returned by the validator.\n\n'
  parts=[intro]
  for path in files:
   content=(ROOT/path).read_text(encoding='utf-8')
   parts.extend(['\n===== BEGIN FILE: '+path+' =====\n',content,'\n===== END FILE: '+path+' =====\n'])
  text=''.join(parts);(OUT/name).write_text(text,encoding='utf-8')
  manifest[name]={'sourceFiles':files,'sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}
 (OUT/'sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 print('Generated '+', '.join(groups))
if __name__=='__main__':build()
