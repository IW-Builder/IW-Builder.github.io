"""Generate the public prompt page from Authoring-Prompt.md."""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "Authoring-Prompt.md"
OUT = ROOT  # Change to ROOT / "docs" if desired.

prompt = SOURCE.read_text(encoding="utf-8")
OUT.mkdir(parents=True, exist_ok=True)

page = """<!doctype html>
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

page = page.replace("__PROMPT_CONTENT__", html.escape(prompt))

for filename, content in [
    ("index.html", page),
    ("prompt.txt", prompt),
]:
    destination = OUT / filename
    with destination.open("w", encoding="utf-8", newline="") as output:
        output.write(content)
    print(f"Wrote {destination}")