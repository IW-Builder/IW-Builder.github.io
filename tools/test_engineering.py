"""Offline contract tests for the plot compiler and static lint."""
import copy,json,tempfile,unittest
from pathlib import Path
from plot_compile import analyze,compile_world
from static_checks import lint

ROOT=Path(__file__).resolve().parent.parent

class GraphTests(unittest.TestCase):
    def setUp(self):
        self.plan={'title':'Test','nodes':[{'id':'b','name':'B','scenario':'B happens','requires':['a'],'award':2},{'id':'a','name':'A','scenario':'A happens'}]}
        self.template=json.loads((ROOT/'World-Template.json').read_text(encoding='utf8'))
    def test_dependency_order_and_commit(self):
        w,r=compile_world(self.plan,self.template)
        self.assertEqual(r['order'],['a','b']);self.assertEqual([t['name'] for t in w['triggerEvents']],['A','B'])
        script=w['triggerEvents'][1]['triggerEffects'][0]['data']
        self.assertIn('$plot.a = 1',script);self.assertIn('$plot.b = 0',script)
        self.assertLess(script.index('$plot.score +='),script.index('$plot.b = 1'))
        self.assertEqual(w['conditions'],['B happens','A happens'])
        self.assertEqual(self.template['trackedItems'],[])
    def test_cycle(self):
        self.plan['nodes'][1]['requires']=['b']
        with self.assertRaisesRegex(ValueError,'Cyclic'):analyze(self.plan)
    def test_unknown_dependency(self):
        self.plan['nodes'][0]['requires']=['absent']
        with self.assertRaisesRegex(ValueError,'Unknown prerequisite'):analyze(self.plan)
    def test_duplicate_and_injection(self):
        for value in ['a','bad\ncode']:
            p=copy.deepcopy(self.plan);p['nodes'][0]['id']=value
            with self.assertRaises(ValueError):analyze(p)
    def test_dynamic_and_bad_awards(self):
        for change in [{'scenario':'<<$state>>'},{'award':True},{'award':-1},{'requires':'a'},{'unexpected':1}]:
            p=copy.deepcopy(self.plan);p['nodes'][0].update(change)
            with self.assertRaises(ValueError):analyze(p)
    def test_deterministic_and_shared(self):
        self.plan['nodes'][0]['scenario']='A happens'
        self.assertEqual(compile_world(self.plan,self.template),compile_world(self.plan,self.template))
        self.assertEqual(analyze(self.plan)['sharedScenarios'],{'A happens':['B','A']})
    def test_reserved_and_nonempty_template(self):
        self.plan['nodes'][0]['id']='score'
        with self.assertRaises(ValueError):compile_world(self.plan,self.template)
        self.template['trackedItems']=[{}]
        with self.assertRaises(ValueError):compile_world({'title':'X','nodes':[{'id':'a','name':'A','scenario':'A'}]},self.template)
    def test_generated_full_schema(self):
        from validate_iw_export import validate
        w,_=compile_world(self.plan,self.template)
        schema=json.loads((ROOT/'tools/iw-export.schema.json').read_text(encoding='utf8'))
        self.assertEqual([f for f in validate(w,schema) if f['severity']=='error'],[])

class AdvisoryTests(unittest.TestCase):
    def test_advisory_not_error_and_guard_not_claimed_missing(self):
        w={'trackedItems':[{'variableName':'state'}],'triggerEvents':[{'canTriggerMoreThanOnce':True,'triggerEffects':[{'type':'effectRunScript','data':'if $state.done = 0\n    $state.score += 1\n    $state.done = 1'}]}]}
        f=next(f for f in lint(w) if f['code']=='review-repeat-accumulation')
        self.assertEqual(f['severity'],'warning');self.assertIn('No missing guard is inferred',f['message'])
    def test_literals_do_not_trigger_random_warning(self):
        self.assertFalse(any(f['code']=='review-independent-random' for f in lint({'instructions':'<<"random()">> <<"random()">>'})))
        self.assertTrue(any(f['code']=='review-independent-random' for f in lint({'instructions':'<<random()>> <<random()>>'})))
    def test_choice_and_script_boundaries(self):
        w={'triggerEvents':[{'triggerEffects':[{'type':'effectRunScript','data':'set $x = 1'},{'type':'effectRunScript','data':'set $y = 2'},{'type':'effectPresentChoice','data':{'choices':'<<1>>','selectionMode':'multiple'}}]}]}
        codes={f['code'] for f in lint(w)}
        self.assertTrue({'review-script-boundary','review-choice-domain','review-choice-storage'}<=codes)

if __name__=='__main__':unittest.main()
