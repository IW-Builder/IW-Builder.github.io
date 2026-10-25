"""Regression checks for distribution assembly; no IW runtime execution."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parent.parent

class DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)/'kit'
        shutil.copytree(SOURCE, cls.root, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__', 'samples', '*.zip'))
        cls.script = cls.root/'tools/build_distribution.py'
        cls.run_build()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @classmethod
    def run_build(cls):
        return subprocess.run([sys.executable, str(cls.script)], cwd=cls.temp.name,
                              capture_output=True, text=True, check=True)

    def test_manifest_bytes_and_scope(self):
        m = json.loads((self.root/'manifest.json').read_text())
        paths = set()
        for entry in m['files']:
            paths.add(entry['path'])
            data = (self.root/entry['path']).read_bytes()
            self.assertEqual(entry['bytes'], len(data))
            self.assertEqual(entry['sha256'], hashlib.sha256(data).hexdigest())
        self.assertIn('checker/index.html', paths)
        self.assertIn('chat/IW-Tools.txt', paths)
        self.assertNotIn('manifest.json', paths)
        self.assertFalse(any(p.startswith('samples/') or p.endswith('.zip') for p in paths))

    def test_llms_index_covers_published_files(self):
        text = (self.root/'llms.txt').read_text()
        self.assertTrue(text.endswith('END OF DOCUMENT: llms.txt\n'))
        m = json.loads((self.root/'manifest.json').read_text())
        folder_pages = {f + '/index.html' for f in ['reference', 'examples', 'library', 'tools', 'samples']}
        for entry in m['files']:
            path = entry['path']
            if path in folder_pages or path == 'llms.txt':
                continue
            self.assertIn('[' + path + '](', text, path)
        self.assertIn('llms.txt', {e['path'] for e in m['files']})
        self.assertIn('https://iw-builder.github.io/reference/PawScript.md', text)
        self.assertIn('https://iw-builder.github.io/examples/Payloads.md', text)

    def test_reference_editions_are_split_and_bounded(self):
        sources = {k: v['sourceFiles'] for k, v in json.loads((self.root/'chat/sources.json').read_text()).items()}
        self.assertEqual(set(sources), {'IW-Authoring-Guide.txt', 'IW-Technical-Reference.txt', 'IW-Behavior.txt',
                                        'IW-Payloads.txt', 'IW-Mechanics-Examples.txt', 'IW-Narrative-Examples.txt',
                                        'IW-Sample-Blocks.txt', 'IW-Storymaster.txt', 'IW-Tools.txt'})
        self.assertIn('library/Integration.md', sources['IW-Authoring-Guide.txt'])
        self.assertFalse((self.root/'chat/IW-Sample-Library.txt').exists())
        self.assertLess((self.root/'chat/IW-Payloads.txt').stat().st_size, 60_000)
        self.assertFalse((self.root/'chat/IW-Examples.txt').exists())
        for name in ['IW-Authoring-Guide.txt', 'IW-Technical-Reference.txt', 'IW-Behavior.txt']:
            self.assertLess((self.root/'chat'/name).stat().st_size, 90_000, name)
        every = [p for files in sources.values() for p in files]
        self.assertNotIn('reference/Roadmap.md', every)
        self.assertIn('reference/Story-Tools.md', sources['IW-Tools.txt'])
        self.assertIn('reference/Engineering-Tools.md', sources['IW-Tools.txt'])
        self.assertEqual(len(every), len(set(every)), 'a source appears in two editions')
        guide = (self.root/'chat/IW-Authoring-Guide.txt').read_text()
        for name in sources:
            self.assertIn('- ' + name + ': ', guide)

    def test_kit_version_consistent(self):
        spec = importlib.util.spec_from_file_location('bd', self.root/'tools/build_distribution.py')
        bd = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd)
        self.assertIn('Kit version is ' + bd.KIT_VERSION + ';', (self.root/'reference/Evidence.md').read_text())
        self.assertIn('Kit ' + bd.KIT_VERSION, (self.root/'index.html').read_text())
        self.assertTrue((self.root/'llms.txt').read_text().startswith('# IW-Builder: Infinite Worlds Authoring Kit ' + bd.KIT_VERSION))

    def test_folder_pages_list_files_without_redirect(self):
        for folder in ['reference', 'examples', 'library', 'tools']:
            page = (self.root/folder/'index.html').read_text()
            self.assertNotIn('http-equiv="refresh"', page)
            self.assertNotIn('rel="canonical"', page)
            self.assertIn('https://iw-builder.github.io/' + folder + '/', page)

    def test_missing_description_fails(self):
        extra = self.root/'reference/Undescribed.md'
        try:
            extra.write_text('# Undescribed\n')
            result = subprocess.run([sys.executable, str(self.script)], cwd=self.temp.name, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('No index description for: reference/Undescribed.md', result.stderr)
        finally:
            extra.unlink()
            self.run_build()

    def test_repeat_build_is_identical(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.run_build()
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_tools_bundle_and_markers(self):
        text = (self.root/'chat/IW-Tools.txt').read_text()
        self.assertIn('===== BEGIN FILE: tools/validate_iw_export.py =====', text)
        self.assertNotIn('===== BEGIN FILE: tools/build_distribution.py =====', text)
        self.assertNotIn('===== BEGIN FILE: tools/test_validator.py =====', text)
        self.assertTrue(text.endswith('END OF DOCUMENT: chat/IW-Tools.txt\n'))
        self.assertEqual((self.root/'Authoring-Prompt.md').read_text().count('END OF DOCUMENT: Authoring-Prompt.md'), 1)
        self.assertFalse((self.root/'prompt.txt').exists())

    def test_checker_matches_tools(self):
        page = (self.root/'checker/index.html').read_text()
        for ident, filename in [('src-validate','validate_iw_export.py'), ('src-static','static_checks.py'), ('src-schema','iw-export.schema.json')]:
            content = re.search(r'<script\b[^>]*id="'+ident+r'"[^>]*>([\s\S]*?)</script>', page)[1]
            self.assertEqual(content.strip('\n'), (self.root/'tools'/filename).read_text().strip('\n'))

    def test_missing_input_fails_before_output(self):
        p = self.root/'World-Template.json'
        data = p.read_bytes()
        manifest = (self.root/'manifest.json').read_bytes()
        try:
            p.unlink()
            result = subprocess.run([sys.executable,str(self.script)], cwd=self.temp.name, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Build failed:', result.stderr)
            self.assertEqual(manifest, (self.root/'manifest.json').read_bytes())
        finally:
            p.write_bytes(data)

    def test_duplicate_source_markers_normalized(self):
        spec = importlib.util.spec_from_file_location('distribution_marker_test', self.script)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        name = 'reference/Example.md'
        text = 'First section\n\n---\n\nEND OF DOCUMENT: '+name+'\n\nSecond section\n\n---\n\nEND OF DOCUMENT: '+name+'\n'
        actual = module.marked(text, name)
        self.assertEqual(actual.count('END OF DOCUMENT: '+name), 1)
        self.assertIn('First section', actual)
        self.assertIn('Second section', actual)

    def test_marker_rename(self):
        spec = importlib.util.spec_from_file_location('distribution', self.script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.marked('Body\n\n---\n\nEND OF DOCUMENT: old.md\n','new.md'),
                         'Body\n\n---\n\nEND OF DOCUMENT: new.md\n')

if __name__ == '__main__':
    unittest.main()
