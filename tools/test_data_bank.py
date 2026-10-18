"""Data bank transport checks; no IW runtime execution."""
import copy
from decimal import Decimal
from pathlib import Path
import tempfile
import unittest
import data_bank as db
from static_checks import lint

ROOT=Path(__file__).resolve().parent.parent

class DataTests(unittest.TestCase):
    def sample(self):
        return db.loads('{"title":"Demo","NPCs":[{"name":"Mara","unknown":{"future":true},"detail":"Text\\nwith \\\"quotes\\\" and \\\\ escapes"}],"trackedItems":[],"unknownRoot":{"huge":90071992547409931234567890,"precise":0.12345678901234567890123456789,"wholeDecimal":1.0,"null":null},"skills":["Generic"],"empty":{},"x/y~z":"unicode \\u00e9"}')

    def parse_rendered(self,bank):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'Bank.txt';p.write_text(db.render(bank),encoding='utf-8')
            return db.read_bank(p)

    def test_all_worlds_round_trip(self):
        paths=[ROOT/'World-Template.json',ROOT/'library/Sample-Blocks.json',*sorted((ROOT/'examples').glob('*.json'))]
        for p in paths:
            if p.name=='index.json': continue
            with self.subTest(world=p.name):
                doc=db.loads(p.read_text(encoding='utf-8'))
                restored=db.restore(self.parse_rendered(db.export(doc)))
                self.assertEqual(db.digest(doc),db.digest(restored))
                self.assertEqual(list(doc),list(restored))

    def test_precision_types_and_unknowns(self):
        original=self.sample();bank=db.export(original)
        bank['futureMetadata']={'retain':'yes'}
        rebuilt=self.parse_rendered(bank)
        self.assertEqual(rebuilt['futureMetadata'],bank['futureMetadata'])
        restored=db.restore(rebuilt)
        self.assertEqual(db.dumps(restored),db.dumps(original))
        self.assertIsInstance(restored['unknownRoot']['wholeDecimal'],Decimal)

    def test_selected_bundle_and_tags(self):
        bank=db.export(self.sample(),['/NPCs/0','/trackedItems'],['fantasy','cast'],'Cast bundle')
        self.assertEqual(len(bank['entries']),1)
        entry=bank['entries'][0]
        self.assertEqual(entry['kind'],'bundle');self.assertEqual(len(entry['components']),2)
        self.assertIn('[fantasy] [cast]',db.render(bank))
        with self.assertRaises(ValueError): db.restore(bank)

    def test_pointer_escaping(self):
        bank=db.export(self.sample(),['/x~1y~0z'])
        self.assertEqual(bank['entries'][0]['components'][0]['payload'],'unicode é')

    def test_duplicate_and_overlap(self):
        with self.assertRaises(ValueError):db.loads('{"x":1,"x":2}')
        for paths in [['/NPCs','/NPCs/0'],['/title','/title']]:
            with self.assertRaises(ValueError):db.export(self.sample(),paths)

    def test_tampered_hash(self):
        bank=db.export(self.sample())
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bank.txt';p.write_text(db.render(bank).replace('"Demo"','"Changed"'),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):db.read_bank(p)

    def test_unverified_chat_bank(self):
        bank=db.export(self.sample())
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bank.txt';p.write_text(db.render(bank).replace(db.digest(bank),'UNVERIFIED'))
            self.assertEqual(db.digest(db.read_bank(p)),db.digest(bank))

    def test_dependencies_and_duplicate_ids(self):
        bank=db.export(self.sample());bank['entries'][0]['dependencies']['included']=['absent']
        with self.assertRaises(ValueError):db.validate(bank)
        bank['entries'][0]['dependencies']['included']=[bank['entries'][1]['id']]
        db.validate(bank)
        bank['entries'][1]['id']=bank['entries'][0]['id']
        with self.assertRaises(ValueError):db.validate(bank)

    def test_restore_missing_extra_and_changed(self):
        for mode in ['missing','extra','changed']:
            bank=db.export(self.sample())
            if mode=='missing':bank['entries'].pop()
            if mode=='extra':bank['entries'][0]['components'].append({'kind':'world-field','sourcePath':'/extra','payload':True})
            if mode=='changed':bank['entries'][0]['components'][0]['payload']='Changed'
            with self.assertRaises((ValueError,KeyError)):db.restore(bank)

    def test_overwrite_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'out';db.write(p,'original')
            with self.assertRaises(FileExistsError):db.write(p,'replacement')
            self.assertEqual(p.read_text(),'original')

    def test_substitution_lint(self):
        findings=lint({'instructions':'<#REPLACE01#>Safe replacement.<#END_REPLACE01#>'})
        matches=[f for f in findings if f['code']=='content-substitution']
        self.assertEqual(len(matches),1);self.assertEqual(matches[0]['severity'],'warning')
        self.assertFalse(any(f['code']=='authoring-placeholder' for f in findings))

if __name__=='__main__':unittest.main()
