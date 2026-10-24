import copy,json,unittest
from pathlib import Path
import validate_iw_export as v
from static_checks import lint
from import_audit import audit_import
R=Path(__file__).resolve().parent.parent
S=json.loads((R/'tools/iw-export.schema.json').read_text())
B=json.loads((R/'World-Template.json').read_text())
def world(node):
 w=copy.deepcopy(B);w['triggerEvents']=[{'id':'TriggerA','name':'Opening gate','triggerConditions':[node],'triggerEffects':[]}];return w
class NativeCompatibility(unittest.TestCase):
 def test_turn_threshold_full_and_reduced(self):
  original=v.Draft202012Validator
  try:
   for validator in (original,None):
    v.Draft202012Validator=validator
    for value,valid in [('2',True),(2,True),(True,False),([],False),({},False)]:
     with self.subTest(validator=bool(validator),value=value):
      f=v.validate(world({'category':'condition','type':'triggerOnTurn','data':value,'id':'Gate'}),S)
      self.assertEqual(not any(x['severity']=='error' for x in f),valid)
  finally:v.Draft202012Validator=original
 def test_more_than_ten_scenarios_not_structural_error(self):
  w=copy.deepcopy(B);w['conditions']=['Scenario '+str(i) for i in range(12)]
  self.assertFalse(any(f['severity']=='error' for f in v.validate(w,S)))
 def test_missing_numeric_comparator_is_advisory(self):
  w=world({'id':'Gate','category':'condition','type':'triggerOnTrackedItem','data':{'trackedItemID':'CoinID','inequality':'is_exactly','requiredValue':'1'}})
  w['trackedItems']=[{'id':'CoinID','name':'Coins','dataType':'number'}]
  self.assertIn('missing-native-comparator',{f['code'] for f in v.validate(w,S)})
 def test_builtin_does_not_mask_typos(self):
  w=world({'category':'condition','type':'triggerOnPawScript','data':'$turn_number > 0 and $turn_numbre > 0','id':'Gate'})
  unknown=[f['message'] for f in lint(w) if f['code']=='unknown-script-root']
  self.assertEqual(len(unknown),1);self.assertIn('$turn_numbre',unknown[0])
 def test_nested_scenario_named_mismatch(self):
  w=world({'category':'logic','operator':'and','id':'Group','data':[{'category':'condition','type':'triggerOnEvent','data':'Door opens. ','id':'Leaf'}]});w['conditions']=['Door opens.']
  f=next(f for f in v.validate(w,S) if f['code']=='unlisted-situation')
  self.assertEqual(f['severity'],'error');self.assertEqual(f['objectName'],'Opening gate');self.assertTrue(f['path'].endswith('/data/0/data'))
 def test_missing_legacy_registry_not_false_hard_failure(self):
  w=world({'id':'Leaf','category':'condition','type':'triggerOnEvent','data':'Door opens.'});w.pop('conditions',None);w['schemaVersion']=2.2
  f=v.validate(w,S);self.assertIn('missing-scenario-registry',{x['code'] for x in f});self.assertNotIn('unlisted-situation',{x['code'] for x in f})
 def test_unknown_effect_stays_forward_compatible(self):
  w=copy.deepcopy(B);w['triggerEvents']=[{'id':'T','triggerEffects':[{'id':'E','type':'futureEffect','data':{'new':1}}]}]
  fs=v.validate(w,S);self.assertFalse(any(f['severity']=='error' for f in fs));self.assertIn('unknown-effect-type',{f['code'] for f in fs})
 def test_native_effect_shapes(self):
  w=copy.deepcopy(B)
  for typ,data in [('effectChangeFirstAction','Begin.'),('effectChangeOtherCharacters',{'action':'modify','character':'Mira','npc':{'name':'Mira','one_liner':'Summary'}})]:
   w['triggerEvents']=[{'id':'T','triggerOnStartOfGame':True,'triggerEffects':[{'id':'E','type':typ,'data':data}]}]
   fs=v.validate(w,S);self.assertFalse(any(f['severity']=='error' for f in fs));self.assertNotIn('unknown-effect-type',{f['code'] for f in fs})
 def test_known_effect_bad_payload_rejected_both_modes(self):
  original=v.Draft202012Validator
  try:
   for validator in (original,None):
    v.Draft202012Validator=validator
    for typ in ('effectChangeFirstAction','effectChangeOtherCharacters'):
     w=copy.deepcopy(B);w['triggerEvents']=[{'id':'T','triggerEffects':[{'id':'E','type':typ,'data':[]}]}]
     self.assertTrue(any(f['severity']=='error' for f in v.validate(w,S)))
  finally:v.Draft202012Validator=original
 def test_remint_and_nested_stale_references(self):
  a=copy.deepcopy(B);a['trackedItems']=[{'id':'old_id','name':'Balance','variableName':'balance'}]
  b=copy.deepcopy(a);b['trackedItems'][0]['id']='NewID';b['triggerEvents']=[{'triggerConditions':[{'data':[{'data':{'trackedItemID':'old_id'}}]}],'triggerEffects':[{'data':{'targetTrackedItemId':'old_id'}}]}]
  frozen=copy.deepcopy((a,b));r=audit_import(a,b)
  self.assertEqual(r['trackerIdentityChanges'][0]['status'],'possible-remint');self.assertEqual(len(r['referencesToRemovedTrackers']),2);self.assertEqual((a,b),frozen)
 def test_remint_ambiguity_not_auto_resolved(self):
  a={'trackedItems':[{'id':'old','name':'A','variableName':'a'}]};b={'trackedItems':[{'id':'new1','name':'A','variableName':'a'},{'id':'new2','name':'A','variableName':'a'}]}
  self.assertEqual(audit_import(a,b)['trackerIdentityChanges'][0]['status'],'removed-or-ambiguous')
 def test_id_risk_only_tracker_advisory(self):
  w=copy.deepcopy(B);w['trackedItems']=[{'id':'a_b','name':'Balance'}];w['triggerEvents']=[{'id':'t_r','triggerEffects':[]}]
  hits=[f for f in v.validate(w,S) if f['code']=='tracker-id-import-risk'];self.assertEqual(len(hits),1);self.assertEqual(hits[0]['severity'],'warning')
if __name__=='__main__':unittest.main()
