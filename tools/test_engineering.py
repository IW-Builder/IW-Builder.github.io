"""Offline contract tests. No claims about authenticated Playwright/IW integration."""
import copy,json,tempfile,unittest
from pathlib import Path
from plot_compile import analyze,compile_world
from static_checks import lint
from iw_browser import export_current,capture,inspect_capture,selected_page

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

class Box:
    def __init__(self,text):self.text=text
    def is_visible(self):return True
    def input_value(self):return self.text
    def fill(self,text):self.text=text
class Button:
    def __init__(self,page):self.page=page
    def count(self):return 1
    def is_visible(self):return True
    def click(self):self.page.clicked+=1
class Locator:
    def __init__(self,page):self.page=page
    def all(self):return self.page.boxes
    def inner_text(self):return 'Retained turn 1'
    def aria_snapshot(self):
        if self.page.fail_capture:raise ValueError('Disconnected')
        return 'Retained turn 1'
class Page:
    url='https://infiniteworlds.app/'
    def __init__(self,mode='ok'):
        self.original=json.dumps({'title':'Demo','schemaVersion':2.4});self.boxes=[Box(self.original)]
        self.mode=mode;self.clicked=0;self.waits=0;self.fail_capture=False
    def title(self):return 'Infinite Worlds'
    def locator(self,name):return Locator(self)
    def get_by_role(self,*a,**kw):return Button(self)
    def wait_for_timeout(self,ms):
        self.waits+=1
        if self.mode=='ok' and self.waits==2:self.boxes[0].text=self.original
        if self.mode=='wrong':self.boxes[0].text=json.dumps({'title':'Other','schemaVersion':2.4})
        if self.mode=='disconnect':raise RuntimeError('Disconnected')

class HarnessTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def test_same_json_after_marker_is_fresh(self):
        p=Page();out=self.root/'out.json';export_current(p,out,'Demo',3)
        self.assertEqual(out.read_text(),p.original);self.assertEqual(p.waits,2)
        r=json.loads((self.root/'out.json.receipt.json').read_text());self.assertIn('marker',r['freshness'])
    def test_stale_timeout_restores_and_retains_backup(self):
        p=Page('stale');out=self.root/'out.json'
        with self.assertRaisesRegex(ValueError,'deadline'):export_current(p,out,'Demo',2)
        self.assertFalse(out.exists());self.assertEqual(p.boxes[0].text,p.original)
        self.assertEqual((self.root/'out.json.before.json').read_text(),p.original)
    def test_wrong_title_not_overwritten(self):
        p=Page('wrong');out=self.root/'out.json'
        with self.assertRaises(ValueError):export_current(p,out,'Demo',2)
        self.assertEqual(json.loads(p.boxes[0].text)['title'],'Other');self.assertFalse(out.exists())
    def test_disconnected_no_retry(self):
        p=Page('disconnect')
        with self.assertRaises(RuntimeError):export_current(p,self.root/'out.json','Demo',2)
        self.assertEqual(p.clicked,1);self.assertTrue((self.root/'out.json.before.json').exists())
    def test_preflight_collision_and_ambiguity(self):
        p=Page();out=self.root/'out.json';out.write_text('keep')
        with self.assertRaises(ValueError):export_current(p,out,'Demo')
        self.assertEqual(out.read_text(),'keep');self.assertEqual(p.clicked,0)
        p.boxes.append(Box(p.original))
        with self.assertRaises(ValueError):export_current(p,self.root/'other.json','Demo')
        self.assertEqual(p.clicked,0)
    def test_capture_integrity_and_failed_capture_unpublished(self):
        p=Page();out=capture(p,self.root/'capture');self.assertEqual(inspect_capture(out)['verifiedFiles'],3)
        (out/'page.txt').write_text('changed')
        with self.assertRaises(ValueError):inspect_capture(out)
        p.fail_capture=True
        with self.assertRaises(ValueError):capture(p,self.root/'failed')
        self.assertFalse((self.root/'failed').exists())
    def test_manifest_traversal_and_missing_entries(self):
        out=capture(Page(),self.root/'capture')
        (out/'manifest.json').write_text(json.dumps({'files':[{'path':'../outside','sha256':'x'}]}))
        with self.assertRaises(ValueError):inspect_capture(out)
    def test_tab_identity(self):
        class Context:pass
        b=Context();c=Context();b.contexts=[c];p=Page();q=Page();q.url='https://infiniteworlds.app.evil.example/'
        c.pages=[p,q];self.assertIs(selected_page(b,None),p)
        c.pages=[p,Page()]
        with self.assertRaises(ValueError):selected_page(b,None)
if __name__=='__main__':unittest.main()
