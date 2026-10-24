"""Local validator regression tests, not an IW/model qualification suite."""
import copy,json,subprocess,sys,tempfile,unittest
from pathlib import Path
import validate_iw_export as v
from static_checks import lint,edit_diff,templates
ROOT=Path(__file__).resolve().parent.parent
SCHEMA=json.loads((ROOT/'tools/iw-export.schema.json').read_text(encoding='utf-8'))
BASE=json.loads((ROOT/'examples/effect-effectPresentChoice.json').read_text(encoding='utf-8'))

def codes(w):return {x['code'] for x in lint(w)}
def code_world(code):
 w=copy.deepcopy(BASE);w['triggerEvents']=[{'id':'test','triggerConditions':[],'triggerEffects':[{'id':'effect','type':'effectRunScript','data':code,'name':'Test'}]}];return w

class ValidatorTests(unittest.TestCase):
 def test_start_give_info(self):
  for start in (False, True):
   for mid in (False, True):
    for effect in ('effectGiveInfo', 'effectTellAIWhatToDo', 'effectShowMessage'):
     with self.subTest(start=start, mid=mid, effect=effect):
      w=copy.deepcopy(BASE)
      w['triggerEvents']=[{'id':'check-start','name':'Timing check','triggerOnStartOfGame':start,'triggerMidGame':mid,'canTriggerMoreThanOnce':True,'triggerConditions':[],'triggerEffects':[{'id':'check-effect','type':effect,'data':'Context.'}]}]
      findings=v.validate(w,SCHEMA)
      hits=[f for f in findings if f['code']=='start-incompatible-effect']
      self.assertEqual(bool(hits), start and effect=='effectGiveInfo')
      if hits:
       self.assertEqual(hits[0]['severity'],'warning')
       self.assertEqual(hits[0]['path'],'/triggerEvents/0/triggerEffects/0')
      self.assertNotIn('timing-editor-consistency',{f['code'] for f in findings})
 def test_visible_skills_false_or_omitted(self):
  for value in (False, None):
   w=copy.deepcopy(BASE)
   if value is None:w.pop('hideSkillSystem',None)
   else:w['hideSkillSystem']=value
   self.assertFalse([f for f in v.validate(w,SCHEMA) if f['path']=='/hideSkillSystem'])
 def test_modify_tracker_visibility_vocabulary(self):
  w=json.loads((ROOT/'examples/effect-effectModifyTrackedItemDetails.json').read_text(encoding='utf-8'))
  effect=next(e for t in w['triggerEvents'] for e in t['triggerEffects'] if e['type']=='effectModifyTrackedItemDetails')
  effect['data']['overrideVisibility']=True
  for mode in ('everyone','player_only','ai_only','hidden','ai_only_boring','hidden_boring'):
   with self.subTest(mode=mode):
    effect['data']['visibility']=mode
    self.assertFalse([f for f in v.validate(w,SCHEMA) if f['path'].endswith('/visibility')])
  effect['data']['visibility']='future_mode'
  hits=[f for f in v.validate(w,SCHEMA) if f['path'].endswith('/visibility')]
  self.assertTrue(any(f['code']=='unobserved-value' and f['severity']=='warning' for f in hits))
  self.assertFalse(any(f['severity']=='error' for f in hits))
 def test_root_typo(self):self.assertIn('unknown-script-root',codes(code_world('$missing += 1')))
 def test_locals_system_and_strings(self):self.assertNotIn('unknown-script-root',codes(code_world('set $local = $game.turn_number\nfor each $entry in $player.skills\n  log($entry)\nlog("$not_a_root; == &&")\n# $ignored')))
 def test_template_any_field(self):
  w=copy.deepcopy(BASE);w['firstInput']='Coins <<$missing>>.';self.assertIn('unknown-script-root',codes(w))
 def test_template_quoted_delimiter(self):self.assertEqual(list(templates('A <<choose($answer, ">>", "ok")>> B')),['choose($answer, ">>", "ok")'])
 def test_comment_template(self):self.assertEqual(list(templates('<# <<$ignored>> #>')),[])
 def test_startup_expression(self):
  w=copy.deepcopy(BASE);w['trackedItems'][0]['initialValueChoicesScript']='$missing.all().name';self.assertIn('unknown-script-root',codes(w))
 def test_borrowed_syntax(self):self.assertIn('borrowed-syntax',codes(code_world('if $answer == "A" && $coins > 0:\n  $coins -= 1;')))
 def test_string_plus(self):self.assertIn('string-plus',codes(code_world('$answer = "Coins " + $coins')))
 def test_literals_not_syntax(self):self.assertNotIn('borrowed-syntax',codes(code_world('$answer = "Text == && ; {}"\n# if a:')))
 def test_placeholder(self):
  w=copy.deepcopy(BASE);w['instructions']='[LIST GENRES] <#time period#>';self.assertIn('authoring-placeholder',codes(w))
 def test_runtime_tokens_not_placeholders(self):
  w=copy.deepcopy(BASE);w['instructions']='[npcAction] [worldAction] <# explanatory comment #>';self.assertNotIn('authoring-placeholder',codes(w))
 def test_input_reference(self):
  w=copy.deepcopy(BASE);w['triggerEvents'][0]['triggerEffects'][0]['data']['targetTrackedItemId']='absent';self.assertIn('unresolved-reference',{x['code'] for x in v.validate(w,SCHEMA)})
 def test_no_schema_dependency(self):
  saved=v.Draft202012Validator
  try:
   v.Draft202012Validator=None;w=copy.deepcopy(BASE);w['triggerEvents'][0]['triggerEffects'][0]['data']['targetTrackedItemId']='absent';out=v.validate(w,SCHEMA);self.assertIn('schema-validation-unavailable',{x['code']for x in out});self.assertIn('unresolved-reference',{x['code']for x in out})
  finally:v.Draft202012Validator=saved
 def test_no_schema_bad_container(self):
  saved=v.Draft202012Validator
  try:
   v.Draft202012Validator=None;w=copy.deepcopy(BASE);w['triggerEvents']='bad';self.assertTrue(any(x['severity']=='error'for x in v.validate(w,SCHEMA)))
  finally:v.Draft202012Validator=saved
 def test_diff(self):
  a=copy.deepcopy(BASE);b=copy.deepcopy(a);removed=b['trackedItems'].pop()['id'];b['title']='Changed';d=edit_diff(a,b);self.assertIn(removed,d['objects']['trackedItems']['removed']);self.assertTrue(any(x['path']=='/title' for x in d['changes']))
 def test_cli_newline_and_utf8(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=Path(tmp)/'world.json';w=copy.deepcopy(BASE);w['title']='Caf\u00e9';f.write_text(json.dumps(w,ensure_ascii=False)+'\n',encoding='utf-8')
   r=subprocess.run([sys.executable,str(ROOT/'tools/validate_iw_export.py'),str(f),'--json'],capture_output=True,text=True,encoding='utf-8');self.assertEqual(r.returncode,0,r.stderr);out=json.loads(r.stdout);self.assertIn('trailing-newline',{x['code']for x in out['findings']})

if __name__=='__main__':unittest.main()
