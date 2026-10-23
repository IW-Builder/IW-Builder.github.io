"""Build the IW distribution from this script's repository location (no arguments).

Standard library only. Updates document markers, homepage, embedded checker tools,
chat editions and SHA-256 manifest. Does not run validation or create ZIP archives.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parent.parent

GUIDE = ['Authoring-Prompt.md',
 'World-Template.json',
 'reference/Evidence.md',
 'reference/Craft.md',
 'reference/Portable-Banks.md',
 'reference/Trackers.md',
 'reference/Triggers.md',
 'reference/Schema.md',
 'reference/PawScript.md',
 'reference/Capabilities.md',
 'reference/Recipes.md',
 'reference/Import-Integrity.md',
 'reference/Known-Limits.md',
 'reference/Default-Evaluation.txt',
 'reference/Current-AI-Profiles.json']
GROUPS = {'IW-Authoring-Guide.txt': ['Authoring-Prompt.md',
                            'World-Template.json',
                            'reference/Evidence.md',
                            'reference/Craft.md',
                            'reference/Portable-Banks.md',
                            'reference/Trackers.md',
                            'reference/Triggers.md',
                            'reference/Schema.md',
                            'reference/PawScript.md',
                            'reference/Capabilities.md',
                            'reference/Recipes.md',
                            'reference/Import-Integrity.md',
                            'reference/Known-Limits.md',
                            'reference/Default-Evaluation.txt',
                            'reference/Current-AI-Profiles.json'],
 'IW-Examples.txt': ['examples/Payloads.md',
                     'examples/index.json',
                     'examples/narrative-vendemmia.json',
                     'examples/recipe-request-commit.json',
                     'examples/recipe-choice-followup.json',
                     'examples/recipe-threshold-unlock.json',
                     'examples/optional-block.json',
                     'examples/showcase-glass-ledger.json',
                     'examples/character-starting-values.json'],
 'IW-Sample-Library.txt': ['library/Integration.md',
                           'library/Sample-Blocks.json',
                           'library/Storymaster-Suite.json']}
PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description"
        content="The Infinite Worlds authoring prompt and supporting tools.">
  <title>Infinite Worlds Authoring Prompt</title>
  <style>
    body {
      max-width: 960px;
      margin: 40px auto;
      padding: 0 24px;
      color: #202820;
      background: #fafbf7;
      font: 16px/1.6 system-ui, sans-serif;
    }
    nav {
      display: flex;
      flex-wrap: wrap;
      gap: 18px;
      margin-bottom: 28px;
    }
    a { color: #235e4b; }
    pre {
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      padding: 24px;
      border: 1px solid #dce2d8;
      border-radius: 10px;
      background: white;
      font: 14px/1.7 ui-monospace, Consolas, monospace;
    }
  </style>
</head>
<body>
  <header>
    <h1>Infinite Worlds Authoring Prompt</h1>
    <p>Give this prompt to your AI along with your world idea.
       The supporting kit supplies its templates and references.</p>
    <nav aria-label="Resources">
      <a href="chat/">Plain-text prompt</a>
      <a href="full-package.zip">Download ZIP package</a>
      <a href="checker/">Validator</a>
      <a href="https://github.com/IW-Builder/IW-Builder.github.io/tree/main">
        README and browse files
      </a>
    </nav>
  </header>
  <main>
    <pre>__PROMPT_CONTENT__</pre>
  </main>
</body>
</html>
"""

TOOL_SOURCES = [
    'tools/Usage.md', 'tools/validate_iw_export.py', 'tools/static_checks.py',
    'tools/iw-export.schema.json', 'tools/data_bank.py',
]
CHECKER_SOURCES = {
    'src-validate': 'tools/validate_iw_export.py',
    'src-static': 'tools/static_checks.py',
    'src-schema': 'tools/iw-export.schema.json',
}

def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def write(path, content):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    raw = content.encode('utf-8')
    if dest.exists() and dest.read_bytes() == raw:
        return
    dest.write_bytes(raw)
    print('Wrote ' + path)

def marked(content, path):
    # Replace only the terminal marker; preserve embedded END FILE boundaries.
    content = re.sub(r'\n(?:---\n\n)?END OF DOCUMENT: [^\n]+\s*\Z', '', content)
    return content.rstrip() + '\n\n---\n\nEND OF DOCUMENT: ' + path + '\n'

def document_paths():
    paths = {'Authoring-Prompt.md', 'library/Integration.md',
             'examples/Payloads.md', 'tools/Usage.md'}
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'reference').glob('*.md')
                 if p.name.lower() != 'readme.md')
    return sorted(paths)

def update_checker():
    page = read('checker/index.html')
    for ident, path in CHECKER_SOURCES.items():
        source = read(path)
        if '</script' in source.lower():
            raise ValueError(path + ' contains an HTML script closing sequence; cannot embed safely.')
        pattern = r'(<script\b[^>]*\bid="' + re.escape(ident) + r'"[^>]*>)[\s\S]*?(</script\s*>)'
        page, count = re.subn(pattern, lambda m: m[1] + '\n' + source.rstrip('\n') + '\n' + m[2], page)
        if count != 1:
            raise ValueError('Expected one checker block: ' + ident)
    return page

def build_chat():
    source_manifest = {}
    groups = {**GROUPS, 'IW-Tools.txt': TOOL_SOURCES}
    for name, paths in groups.items():
        intro = ('Infinite Worlds Authoring Kit: generated text edition. '
                 'BEGIN FILE / END FILE sections identify package-relative sources. '
                 'This upload is reference material, not one IW world. Follow Authoring-Prompt.md; '
                 'load companion material only as needed. The Examples edition contains selected '
                 'complete worlds; additional examples remain available in the repository.\n')
        if name == 'IW-Tools.txt':
            intro = ('Infinite Worlds Authoring Kit: authoring tools. Recreate files at their '
                     'BEGIN FILE paths, excluding boundary lines and separator newlines. '
                     'Preserve code indentation and escaping. See tools/Usage.md for dependencies '
                     'and commands. Includes validator, schema, static lint and data-bank utility. '
                     'Distribution builders and maintainer tests are intentionally omitted. '
                     'Reading these sources is not running them; report validation only after execution.\n')
        parts = [intro]
        for path in paths:
            parts.extend(['\n===== BEGIN FILE: ' + path + ' =====\n', read(path),
                          '\n===== END FILE: ' + path + ' =====\n'])
        text = ''.join(parts).rstrip() + '\n\nEND OF DOCUMENT: chat/' + name + '\n'
        write('chat/' + name, text)
        source_manifest[name] = {'sourceFiles': paths,
                                'sha256': hashlib.sha256(text.encode('utf-8')).hexdigest()}
    write('chat/sources.json', json.dumps(source_manifest, indent=2) + '\n')

def manifest_paths():
    # Explicit publication scope excludes samples, Git internals, caches and archives.
    paths = {ROOT/p for p in ['Authoring-Prompt.md', 'World-Template.json',
                              'README.md', 'LICENSE', 'index.html'] if (ROOT/p).is_file()}
    suffixes = {'.md', '.txt', '.json', '.py', '.html', '.js', '.css', '.svg', '.yml', '.yaml'}
    for folder in ['reference', 'library', 'examples', 'tools', 'chat', 'checker']:
        for p in (ROOT/folder).rglob('*'):
            rel = p.relative_to(ROOT)
            if (p.is_file() and not p.is_symlink() and p.suffix.lower() in suffixes
                and not any(x.startswith('.') or x == '__pycache__' for x in rel.parts)
                and p.name not in {'build_chat_edition.py', 'build_prompt_page.py'}):
                paths.add(p)
    return sorted(paths, key=lambda p: p.relative_to(ROOT).as_posix())

def build_manifest():
    records = []
    for p in manifest_paths():
        data = p.read_bytes()
        records.append({'path': p.relative_to(ROOT).as_posix(), 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
    # Preserve the timestamp when the represented bytes have not changed.
    old = {}
    try:
        old = json.loads(read('manifest.json'))
    except (OSError, ValueError):
        pass
    timestamp = old.get('generatedAt') if old.get('files') == records else None
    result = {'algorithm': 'sha256',
              'generatedAt': timestamp or datetime.now(timezone.utc).isoformat(timespec='seconds'),
              'files': records}
    write('manifest.json', json.dumps(result, indent=2) + '\n')
    print('Manifest: ' + str(len(records)) + ' files')

def build():
    # Preflight every required input and checker embedding before changing outputs.
    required = set(document_paths() + TOOL_SOURCES + list(CHECKER_SOURCES.values()))
    for paths in GROUPS.values():
        required.update(paths)
    for path in sorted(required):
        read(path)
    checker = update_checker()
    for path in document_paths():
        write(path, marked(read(path), path))
    write('index.html', PAGE.replace('__PROMPT_CONTENT__', html.escape(read('Authoring-Prompt.md'))))
    write('checker/index.html', checker)
    build_chat()
    build_manifest()
    print('Build complete. Validation and ZIP packaging are separate steps.')

if __name__ == '__main__':
    try:
        build()
    except (OSError, ValueError) as exc:
        raise SystemExit('Build failed: ' + str(exc))
