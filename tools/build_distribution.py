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
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
KIT_VERSION = '1.6.0'  # also stated in reference/Evidence.md (checked by tests)

# Combined text editions for chats without web access. Each stays well under
# common fetch/attachment limits; models load companions only when needed.
GROUPS = {
    'IW-Authoring-Guide.txt': [
        'Authoring-Prompt.md',
        'World-Template.json',
        'reference/Evidence.md',
        'reference/Craft.md',
        'reference/Trackers.md',
        'reference/Triggers.md',
        'reference/Trigger-Catalog.md',
        'reference/Portable-Banks.md',
        'library/Integration.md',
    ],
    'IW-Technical-Reference.txt': [
        'reference/Schema.md',
        'reference/PawScript.md',
        'reference/Capabilities.md',
        'reference/Recipes.md',
        'reference/Import-Integrity.md',
        'reference/Default-Evaluation.txt',
        'reference/Current-AI-Profiles.json',
    ],
    'IW-Behavior.txt': [
        'reference/Notable-Findings.md',
        'reference/Editor-UI.md',
        'reference/Verified-Behavior.md',
        'reference/Known-Limits.md',
    ],
    'IW-Payloads.txt': [
        'examples/Payloads.md',
        'examples/index.json',
    ],
    'IW-Mechanics-Examples.txt': [
        'examples/recipe-request-commit.json',
        'examples/recipe-completion-award.json',
        'examples/recipe-candidate-acceptance.json',
        'examples/recipe-archive-reactivate.json',
        'examples/recipe-cached-random.json',
        'examples/recipe-consumed-timer.json',
        'examples/recipe-choice-domain.json',
        'examples/recipe-compiled-plot.json',
        'examples/recipe-choice-followup.json',
        'examples/recipe-threshold-unlock.json',
        'examples/optional-block.json',
        'examples/character-starting-values.json',
        'examples/showcase-glass-ledger.json',
    ],
    'IW-Narrative-Examples.txt': [
        'examples/narrative-vendemmia.json',
        'examples/narrative-listening-road.json',
        'examples/narrative-address-after-midnight.json',
    ],
    'IW-Sample-Blocks.txt': [
        'library/Sample-Blocks.json',
    ],
    'IW-Storymaster.txt': [
        'library/Storymaster-Suite.json',
    ],
}
# Purpose of each edition, used in every edition's header so a model with only
# one file knows which companion holds a given path.
EDITION_PURPOSE = {
    'IW-Authoring-Guide.txt': 'start here: prompt, template, narrative craft, trackers, triggers, data banks and library integration',
    'IW-Technical-Reference.txt': 'exact payloads, PawScript, capabilities, recipes and import integrity',
    'IW-Behavior.txt': 'notable findings, editor/UI workflows, verified runtime behavior and known limits',
    'IW-Payloads.txt': 'exact native payload snippets for every condition and effect, plus the example index',
    'IW-Mechanics-Examples.txt': 'complete mechanics example worlds: recipes, optional block, starting values and a showcase',
    'IW-Narrative-Examples.txt': 'complete narrative example worlds: ensemble romance, fantasy expedition and contained horror',
    'IW-Sample-Blocks.txt': 'optional library modules (read library/Integration.md first)',
    'IW-Storymaster.txt': 'the Storymaster narrative-direction framework (read library/Integration.md first)',
    'IW-Tools.txt': 'Python tools and their guides, for models that can run code',
}

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
    <p>Send this page's link to your AI together with your request, for example:
       <code>Use https://IW-Builder.github.io/ to build: [your idea]</code>.
       The supporting kit supplies its templates and references. Kit __KIT_VERSION__.</p>
    <nav aria-label="Resources">
      <a href="chat/">Plain-text prompt</a>
      <a href="full-package.zip">Download ZIP package</a>
      <a href="checker/">Validator</a>
      <a href="llms.txt">File index</a>
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
    'tools/Usage.md', 'reference/Story-Tools.md', 'reference/Engineering-Tools.md',
    'tools/validate_iw_export.py', 'tools/static_checks.py',
    'tools/iw-export.schema.json', 'tools/data_bank.py',
    'tools/import_audit.py', 'tools/story_export.py',
    'tools/plot_compile.py',
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
    content = re.sub(r'\n(?:---\n\n)?' + re.escape('END OF DOCUMENT: ' + path) + r'(?=\n|$)\n?', '\n', content)
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

def edition_header(name):
    lines = ['Infinite Worlds Authoring Kit: ' + name + ' (' + EDITION_PURPOSE[name] + ').',
             'Generated text edition. BEGIN FILE / END FILE sections identify package-relative source paths. '
             'This is reference material, not one IW world.']
    if name == 'IW-Tools.txt':
        lines.append('To use the tools, recreate files at their BEGIN FILE paths, excluding boundary lines and '
                     'separator newlines, and preserve indentation and escaping. See tools/Usage.md for dependencies '
                     'and commands. Distribution builders and maintainer tests are omitted. Reading these sources is '
                     'not running them; report validation only after execution.')
    else:
        lines.append('Follow Authoring-Prompt.md (in IW-Authoring-Guide.txt). Load companion editions only when the task needs them.')
    lines.append('Editions and their contents:')
    editions = {**GROUPS, 'IW-Tools.txt': TOOL_SOURCES}
    for other, purpose in EDITION_PURPOSE.items():
        lines.append('- ' + other + ': ' + purpose + '. Files: ' + ', '.join(editions[other]))
    lines.append('Every file is also available individually: https://iw-builder.github.io/llms.txt')
    return '\n'.join(lines) + '\n'

def build_chat():
    source_manifest = {}
    groups = {**GROUPS, 'IW-Tools.txt': TOOL_SOURCES}
    for name, paths in groups.items():
        parts = [edition_header(name)]
        for path in paths:
            parts.extend(['\n===== BEGIN FILE: ' + path + ' =====\n', read(path),
                          '\n===== END FILE: ' + path + ' =====\n'])
        text = ''.join(parts).rstrip() + '\n\nEND OF DOCUMENT: chat/' + name + '\n'
        write('chat/' + name, text)
        source_manifest[name] = {'sourceFiles': paths,
                                'sha256': hashlib.sha256(text.encode('utf-8')).hexdigest()}
    write('chat/sources.json', json.dumps(source_manifest, indent=2) + '\n')
    guide = read('chat/IW-Authoring-Guide.txt')
    links = ',\n    '.join('<a href="' + n + '">' + html.escape(n) + '</a> (' + html.escape(EDITION_PURPOSE[n]) + ')'
                           for n in EDITION_PURPOSE if n != 'IW-Authoring-Guide.txt')
    page = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IW Builder Authoring Guide</title>
  <style>body { max-width: 960px; margin: 40px auto; padding: 0 24px; font: 16px/1.6 system-ui, sans-serif; } pre { white-space: pre-wrap; overflow-wrap: anywhere; font: inherit; }</style>
</head>
<body>
  <h1>IW Builder Authoring Guide</h1>
  <p>Start here. This page contains IW-Authoring-Guide.txt: the prompt, template and core references. Companion editions, only when needed:
    __LINKS__.
    Individual files: <a href="https://iw-builder.github.io/llms.txt">llms.txt</a>.</p>
  <main><pre>__GUIDE_CONTENT__</pre></main>
</body>
</html>
"""
    write('chat/index.html', page.replace('__LINKS__', links).replace('__GUIDE_CONTENT__', html.escape(guide)))


def manifest_paths():
    # Explicit publication scope excludes samples, Git internals, caches and archives.
    paths = {ROOT/p for p in ['Authoring-Prompt.md', 'World-Template.json',
                              'README.md', 'LICENSE', 'index.html', 'llms.txt'] if (ROOT/p).is_file()}
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

# ---------------------------------------------------------------------------
# File index (llms.txt) and folder pages
# ---------------------------------------------------------------------------
# One description per published file. llms.txt and the folder index pages are
# generated from this table; example worlds take their purpose from
# examples/index.json. The build fails if a published file has no description.

SITE = 'https://iw-builder.github.io/'
GITHUB_TREE = 'https://github.com/IW-Builder/IW-Builder.github.io/tree/main/'

DESCRIPTIONS = {
    # Start here
    'index.html': 'Homepage: the authoring prompt (same text as Authoring-Prompt.md). Start here.',
    'Authoring-Prompt.md': 'The authoring prompt: task modes, which reference to read for each feature, construction, timing, validation and delivery rules.',
    'World-Template.json': 'Empty importable world; the starting point for new builds.',
    'README.md': 'Human guide: workflows, starter requests, import/export steps. Rendered at /guide/; models can skip it.',
    'LICENSE': 'MIT license.',
    # Combined text editions
    'chat/index.html': 'HTML page containing IW-Authoring-Guide.txt, with links to the companion editions.',
    'chat/IW-Authoring-Guide.txt': 'Combined text, start here: prompt, template, Evidence, Craft, Trackers, Triggers, Trigger-Catalog, Portable-Banks and library Integration.',
    'chat/IW-Technical-Reference.txt': 'Combined text: Schema, PawScript, Capabilities, Recipes, Import-Integrity, Default Evaluation and AI profile IDs.',
    'chat/IW-Behavior.txt': 'Combined text: Notable-Findings, Editor-UI, Verified-Behavior and Known-Limits.',
    'chat/IW-Payloads.txt': 'Combined text: payload cookbook (every condition and effect) and the example index. Small and essential for mechanics.',
    'chat/IW-Mechanics-Examples.txt': 'Combined text: complete mechanics example worlds (recipes, optional block, starting values, showcase).',
    'chat/IW-Narrative-Examples.txt': 'Combined text: complete narrative example worlds (ensemble romance, fantasy expedition, contained horror).',
    'chat/IW-Sample-Blocks.txt': 'Combined text: library modules (Sample-Blocks.json). Integration guide is in IW-Authoring-Guide.txt.',
    'chat/IW-Storymaster.txt': 'Combined text: the Storymaster framework (Storymaster-Suite.json). Integration guide is in IW-Authoring-Guide.txt.',
    'chat/IW-Tools.txt': 'Combined text: tool usage guide, Story-Tools and plot-compiler guides, plus validator, schema and helper sources to recreate locally.',
    'chat/README.md': 'Human guide to the combined text files.',
    'chat/sources.json': 'Which source files make up each combined text file, with hashes.',
    # Reference
    'reference/Capabilities.md': 'Turn lifecycle, Skills, NPC cards and keyword blocks, specialist requests, template timing, endings, images, video and model-specific blocks.',
    'reference/Craft.md': 'Narrative design: what goes in each field, openings, character cards, romance and adult worlds, prose style, names, example worlds by genre.',
    'reference/Current-AI-Profiles.json': 'Storyteller models, current and retired: block IDs, underlying real-world model, isCurrent flag and typical credits per turn.',
    'reference/Default-Evaluation.txt': "IW's built-in Evaluation instructions, verbatim; the baseline for a custom Evaluation.",
    'reference/Editor-UI.md': 'Editor labels and their JSON fields, import/export steps, debug tools, visibility, permissions and troubleshooting by symptom.',
    'reference/Engineering-Tools.md': 'Literal-Scenario plot compiler: commands and limits.',
    'reference/Evidence.md': 'Platform baseline, version numbers and the evidence labels used across the kit.',
    'reference/Import-Integrity.md': 'ID conventions, checks before and after import, editing live copies, and the import audit tool.',
    'reference/Known-Limits.md': 'Platform behavior that remains unverified, by area.',
    'reference/PawScript.md': 'PawScript language guide: syntax, collections, randomness, formatting, debugging, system roots and common mistakes.',
    'reference/Portable-Banks.md': 'Data mode: portable character/data bank format, dependencies, full-content build reports and data_bank.py commands.',
    'reference/README.md': 'Human-friendly index of the reference guides.',
    'reference/Recipes.md': 'Ways to combine features: situation triggers, thresholds, choices, optional blocks, dynamic content, request/commit and guarded state patterns.',
    'reference/Schema.md': 'Export structure: field groups, trackers, starting values, condition and effect payloads, comparators and value-effect operations.',
    'reference/Story-Tools.md': 'Import comparison and story-text extraction/merge tools: commands and limits.',
    'reference/Trackers.md': 'Tracker fields, data types, visibility, update ownership, starting values and memory/context cost.',
    'reference/Trigger-Catalog.md': "Every identified trigger condition and effect type in one table. Check it before saying a trigger can't do something.",
    'reference/Triggers.md': 'Trigger timing flags, ordering, effect semantics, choosing native effects or PawScript, and start-of-game restrictions.',
    'reference/Notable-Findings.md': 'Plain-language list of the behavior most likely to surprise an author or break a world, with what to do.',
    'reference/Verified-Behavior.md': 'Consolidated runtime findings: triggers, imports, PawScript, visibility, memory, forms, images and endings.',
    # Library
    'library/Integration.md': 'How to choose and adapt library modules: Storymaster versus lightweight direction, token costs, dependency checklists. Read before using the library JSON.',
    'library/README.md': 'Human-friendly overview of the library.',
    'library/Sample-Blocks.json': 'Library modules in world-file format: time/location, characterization, craft, pacing, trackers, image styles and more. Copy whole content values by name.',
    'library/Storymaster-Suite.json': 'The Storymaster narrative-direction framework in world-file format. Substantial; read Integration.md first.',
    # Examples (individual worlds are described by examples/index.json)
    'examples/README.md': 'Human guide to the examples, grouped by what you want to do.',
    'examples/Payloads.md': 'Compact native payload snippets for every condition and effect, taken from the example worlds.',
    'examples/index.json': 'Machine index of every example world: purpose, evidence label and verification scope.',
    # Tools
    'tools/README.md': 'Human overview of the tools.',
    'tools/Usage.md': 'Commands, checks, warning meanings and limits for the validator and other tools.',
    'tools/validate_iw_export.py': 'World validator: schema, references and lint; --diff compares with an original. The main tool to run.',
    'tools/iw-export.schema.json': 'JSON Schema (Draft 2020-12) profile of the IW export format, used by the validator.',
    'tools/static_checks.py': 'Lint and reference checks used by the validator.',
    'tools/data_bank.py': 'Create, check, pack/unpack and restore portable data banks and full-content build reports. Standard library only.',
    'tools/import_audit.py': 'Read-only comparison of a source world with its re-exported import: ID changes and dangling references.',
    'tools/story_export.py': 'Plan, build and verify reviewed extractions of IW story exports; merges only non-conflicting histories.',
    'tools/plot_compile.py': 'Builds a fresh world from a literal-Scenario prerequisite plan.',
    'tools/example-plot-plan.json': 'Sample input for plot_compile.py.',
    'tools/Validation-Report.json': 'Latest package check results (maintainer output).',
    'tools/build_distribution.py': 'Maintainer: rebuilds the homepage, combined text files, folder pages, llms.txt, checker and manifest.',
    'tools/check_package.py': 'Maintainer: validates every example world and local link; writes Validation-Report.json.',
    'tools/test_validator.py': 'Maintainer tests for the validator.',
    'tools/test_data_bank.py': 'Maintainer tests for data_bank.py.',
    'tools/test_distribution.py': 'Maintainer tests for the distribution build.',
    'tools/test_engineering.py': 'Maintainer tests for the browser harness and plot compiler.',
    'tools/test_native_compat.py': 'Maintainer tests for native export compatibility.',
    'tools/test_story_export.py': 'Maintainer tests for story_export.py.',
    # Checker
    'checker/index.html': "Browser validator: paste a world or a model's whole reply; runs validate_iw_export.py locally, joins numbered chunks and copies a report for the AI.",
}

# Folder pages are generated, so they are not listed in the index themselves.
FOLDER_PAGES = {
    'reference': 'Reference guides',
    'examples': 'Example worlds',
    'library': 'Sample library',
    'tools': 'Tools',
    'samples': 'Sample worlds and design conversations',
}

def site_url(path):
    """Direct public URL for a published file."""
    if path == 'index.html':
        return SITE
    if path == 'README.md':
        return SITE + 'guide/'
    if path.endswith('/index.html'):
        return SITE + path[:-len('index.html')]
    return SITE + quote(path)

def size_label(nbytes):
    return str(max(1, round(nbytes / 1024))) + ' KB'

def front_matter(text):
    match = re.match(r'---\r?\n(.*?)\r?\n---', text, re.S)
    fields = {}
    if match:
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(':')
            if sep:
                fields[key.strip()] = value.strip().strip('"')
    return fields

def sample_entries():
    """Finished sample worlds paired with their rendered design conversations."""
    entries = []
    folder = ROOT/'samples'
    if not folder.is_dir():
        return entries
    for world in sorted(folder.glob('*.json')):
        conversation = world.with_suffix('.md')
        meta = front_matter(conversation.read_text(encoding='utf-8')) if conversation.is_file() else {}
        title = meta.get('title', world.stem).removesuffix('.md')
        rel = world.relative_to(ROOT).as_posix()
        entries.append({'path': rel, 'url': SITE + quote(rel), 'bytes': world.stat().st_size,
                        'description': 'Finished world: ' + title + '. Optional inspiration, not documentation.'})
        if meta.get('permalink'):
            entries.append({'path': conversation.relative_to(ROOT).as_posix(),
                            'url': SITE + meta['permalink'].lstrip('/'),
                            'bytes': conversation.stat().st_size,
                            'description': 'Design conversation for ' + title + '. Long; may include mature content.'})
    return entries

def index_entries():
    """Every published file except generated folder pages, grouped for the index."""
    examples = {item['file']: item for item in json.loads(read('examples/index.json'))}
    folder_pages = {name + '/index.html' for name in FOLDER_PAGES}
    groups = {}
    missing = []
    for p in manifest_paths():
        rel = p.relative_to(ROOT).as_posix()
        if rel in folder_pages or rel == 'llms.txt':
            continue
        if rel in DESCRIPTIONS:
            description = DESCRIPTIONS[rel]
        elif rel.startswith('examples/') and rel.endswith('.json') and p.name in examples:
            item = examples[p.name]
            description = item['purpose'].rstrip('.') + '. Evidence: ' + item['evidence'] + '.'
        else:
            missing.append(rel)
            continue
        group = rel.split('/')[0] if '/' in rel else 'root'
        groups.setdefault(group, []).append({'path': rel, 'url': site_url(rel),
                                             'bytes': p.stat().st_size, 'description': description})
    if missing:
        raise ValueError('No index description for: ' + ', '.join(missing)
                         + '. Add it to DESCRIPTIONS in build_distribution.py or examples/index.json.')
    # Curated order: the DESCRIPTIONS table order first, then remaining files by path.
    rank = {path: i for i, path in enumerate(DESCRIPTIONS)}
    for entries in groups.values():
        entries.sort(key=lambda e: (rank.get(e['path'], len(rank)), e['path']))
    samples = sample_entries()
    if samples:
        groups['samples'] = samples
    return groups

INDEX_SECTIONS = [
    ('root', 'Start here', None),
    ('reference', 'Reference guides', 'Read only what the task needs; Authoring-Prompt.md says which guide covers which feature.'),
    ('examples', 'Examples', 'Each JSON file is a complete importable world demonstrating one feature or combination.'),
    ('library', 'Sample library', 'Optional modules to adapt into worlds.'),
    ('tools', 'Tools', 'Python tools for models or users that can run code. Without Python, use the checker.'),
    ('checker', 'Browser checker', None),
    ('chat', 'Combined text editions', 'Single-file bundles for chats without web access or with tool limits. Web-browsing models should prefer the individual files above.'),
    ('samples', 'Sample worlds', 'Worlds made with the kit, with the conversations that produced them. Not documentation.'),
]

def build_llms():
    groups = index_entries()
    lines = ['# IW-Builder: Infinite Worlds Authoring Kit ' + KIT_VERSION, '',
             '> Reference kit for AI models that build, edit, review and debug Infinite Worlds (IW) games. '
             'Start with the authoring prompt at ' + SITE + ' (or Authoring-Prompt.md), then fetch only the '
             'files the task needs. Every published file is listed below with its direct URL, size and purpose.',
             '',
             'Independent and unaffiliated with Infinite Worlds. Sizes are approximate. '
             'Integrity hashes for these files are in ' + SITE + 'manifest.json (for verification only; not needed to author).']
    for key, title, note in INDEX_SECTIONS:
        if key not in groups:
            continue
        lines += ['', '## ' + title, '']
        if note:
            lines += [note, '']
        for e in groups[key]:
            lines.append('- [' + e['path'] + '](' + e['url'] + ') (' + size_label(e['bytes']) + '): ' + e['description'])
    lines += ['', '---', '', 'END OF DOCUMENT: llms.txt', '']
    write('llms.txt', '\n'.join(lines))
    return groups

FOLDER_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IW Builder: __TITLE__</title>
  <style>body { max-width: 960px; margin: 40px auto; padding: 0 24px; color: #202820; background: #fafbf7; font: 16px/1.6 system-ui, sans-serif; } a { color: #235e4b; } li { margin: 6px 0; } code { font: 14px ui-monospace, Consolas, monospace; } .size { color: #5b665b; }</style>
</head>
<body>
  <h1>__TITLE__</h1>
  <p>__NOTE__</p>
  <p><a href="__SITE__">Authoring prompt (start here)</a> · <a href="__SITE__llms.txt">Full file index</a> · <a href="__GITHUB__">Browse on GitHub</a></p>
  <ul>
__ITEMS__
  </ul>
</body>
</html>
"""

def build_folder_pages(groups):
    notes = {key: note for key, _, note in INDEX_SECTIONS}
    for folder, title in FOLDER_PAGES.items():
        entries = groups.get(folder)
        if not entries:
            continue
        items = '\n'.join('    <li><a href="' + html.escape(e['url']) + '"><code>' + html.escape(e['path'].split('/', 1)[1])
                          + '</code></a> <span class="size">(' + size_label(e['bytes']) + ')</span>: '
                          + html.escape(e['description']) + '</li>' for e in entries)
        page = (FOLDER_PAGE.replace('__TITLE__', html.escape(title))
                .replace('__NOTE__', html.escape(notes.get(folder) or ''))
                .replace('__SITE__', SITE).replace('__GITHUB__', GITHUB_TREE + folder)
                .replace('__ITEMS__', items))
        write(folder + '/index.html', page)


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
    write('index.html', PAGE.replace('__KIT_VERSION__', KIT_VERSION).replace('__PROMPT_CONTENT__', html.escape(read('Authoring-Prompt.md'))))
    write('checker/index.html', checker)
    build_chat()
    build_folder_pages(build_llms())
    build_manifest()
    print('Build complete. Validation and ZIP packaging are separate steps.')

if __name__ == '__main__':
    try:
        build()
    except (OSError, ValueError) as exc:
        raise SystemExit('Build failed: ' + str(exc))
