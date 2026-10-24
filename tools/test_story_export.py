import copy,json,tempfile,unittest
from pathlib import Path
from story_export import propose,extract,merge,publish,digest,verify_archive

def turn(n,text='hello'):
 return f'-- Turn {n} --\n\nOutcome\n-------\n{text}\n'
class StoryExportTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def plan(self,name,text,names=(),branch='main',session='session'):
  p=self.root/name;p.write_text(text,encoding='utf8');r=propose(p,list(names),session,branch);r['reviewed']=True;return r
 def test_nested_yaml_unicode_and_hidden(self):
  text=turn(1,'café 🐾 中文')+'\nTracked Items\n-------------\nState:\nsetup:\n  nested:\n    value: 3\ninventory:\n  - id: lamp\n\nNotes:\nfirst\nsecond\n\nHidden Tracked Items\n--------------------\nSecret:\nprivate\n'
  r=extract(self.plan('a',text,['State','Notes','Secret']))[0]
  self.assertEqual(set(r['trackedItems']),{'State','Notes'});self.assertIn('  nested:\n    value: 3',r['trackedItems']['State']);self.assertEqual(r['hiddenTrackedItems']['Secret'],'private');self.assertIn('café 🐾 中文',r['sections']['outcome'])
 def test_unknown_heading_kept(self):
  r=extract(self.plan('a',turn(1,'first\nA quoted heading\n----------------\nlast')))[0]
  self.assertIn('A quoted heading\n----------------\nlast',r['sections']['outcome'])
 def test_embedded_marker_quarantined(self):
  p=self.plan('a',turn(1,'quoted\n-- Turn 99 --\nstill prose'))
  self.assertTrue(p['reviewIssues'])
  with self.assertRaises(ValueError):extract(p)
 def test_explicit_corrected_marker_boundary(self):
  p=self.plan('a',turn(1,'quoted\n-- Turn 99 --\nstill prose'));p['turns'][0]['endLine']=p['turns'][-1]['endLine'];p['turns'][0]['sections'][0]['endLine']=p['turns'][-1]['endLine'];p['turns']=p['turns'][:1];p['reviewIssues']=[]
  r=extract(p);self.assertEqual(len(r),1);self.assertIn('-- Turn 99 --',r[0]['sections']['outcome'])
 def test_duplicate_known_heading_quarantined(self):
  p=self.plan('a',turn(1,'Outcome\n-------\nquoted'))
  with self.assertRaises(ValueError):extract(p)
 def test_unreviewed_and_source_hash(self):
  p=self.plan('a',turn(1));p['reviewed']=False
  with self.assertRaises(ValueError):extract(p)
  p['reviewed']=True;Path(p['path']).write_text(turn(1,'changed'))
  with self.assertRaises(ValueError):extract(p)
 def test_empty_tracker(self):
  p=self.plan('a',turn(1)+'\nTracked Items\n-------------\nEmpty:\n',['Empty'])
  self.assertEqual(extract(p)[0]['trackedItems']['Empty'],'')
 def test_conflicts_never_mtime_or_order(self):
  a=self.plan('a',turn(1)+turn(2,'A'));b=self.plan('b',turn(2,'B')+turn(3))
  for ps in ([a,b],[b,a]):
   with self.assertRaises(ValueError):merge(ps)
 def test_same_text_dedup_provenance(self):
  a=self.plan('a',turn(1)+turn(2));b=self.plan('b',turn(2)+turn(3))
  first=merge([a,b]);second=merge([b,a]);self.assertEqual(first,second);self.assertEqual(len(first['turns'][1]['provenance']),2)
 def test_same_raw_text_different_approved_sections_conflicts(self):
  a=self.plan('a',turn(1,'narration\nSecret Information\n------------------\nsecret'));b=copy.deepcopy(a)
  b['turns'][0]['sections'][0]['endLine']=b['turns'][0]['endLine'];b['turns'][0]['sections']=b['turns'][0]['sections'][:1]
  with self.assertRaises(ValueError):merge([a,b])
 def test_manifest_path_escape_rejected(self):
  p=self.plan('a',turn(1));out=self.root/'archive';publish([p],out)
  m=json.loads((out/'manifest.json').read_text());m['files'][0]['path']='../a';(out/'manifest.json').write_text(json.dumps(m))
  with self.assertRaises(ValueError):verify_archive(out)
 def test_identity_and_gap_rejection(self):
  a=self.plan('a',turn(1));b=self.plan('b',turn(2),branch='alternate');c=self.plan('c',turn(3))
  for ps in ([a,b],[a,c]):
   with self.assertRaises(ValueError):merge(ps)
 def test_partial_explicit(self):
  a=self.plan('a',turn(3)+turn(4))
  with self.assertRaises(ValueError):merge([a])
  self.assertTrue(merge([a],True)['partial'])
 def test_invalid_spans(self):
  p=self.plan('a',turn(1));p['turns'][0]['endLine']=999
  with self.assertRaises(ValueError):extract(p)
 def test_unresolved_and_duplicate_tracker_headers(self):
  for content in ['Unknown:\n1','State:\n1\nState:\n2']:
   p=self.plan('a',turn(1)+'\nTracked Items\n-------------\n'+content,['State'])
   with self.assertRaises(ValueError):extract(p)
 def test_atomic_new_output_no_stale_reuse(self):
  p=self.plan('a',turn(1)+'\nTracked Items\n-------------\nState:\n1',['State']);out=self.root/'published';m=publish([p],out)
  for f in m['files']:self.assertEqual(digest((out/f['path']).read_bytes()),f['sha256'])
  prior=(out/'story.json').read_bytes();q=self.plan('b',turn(1,'No trackers'))
  with self.assertRaises(ValueError):publish([q],out)
  self.assertEqual((out/'story.json').read_bytes(),prior)
  fresh=self.root/'fresh';publish([q],fresh);self.assertFalse((fresh/'tracked_state.json').exists());self.assertEqual(json.loads((fresh/'story.json').read_text())['turns'][0]['trackedItems'],{})
 def test_archive_integrity_and_unlisted_stale_data(self):
  p=self.plan('a',turn(1));out=self.root/'archive';publish([p],out)
  (out/'tracked_state.json').write_text('stale')
  self.assertEqual(verify_archive(out)['turns'],1)
  (out/'story.json').write_text('{}')
  with self.assertRaises(ValueError):verify_archive(out)
 def test_unicode_line_separator_preserved(self):
  p=self.plan('a',turn(1,'left\u2028right'))
  self.assertIn('left\u2028right',extract(p)[0]['sections']['outcome'])
 def test_failure_leaves_no_output(self):
  p=self.plan('a',turn(1));p['sha256']='bad';out=self.root/'failed'
  with self.assertRaises(ValueError):publish([p],out)
  self.assertFalse(out.exists());self.assertFalse(list(self.root.glob('.iw-story-*')))
if __name__=='__main__':unittest.main()
