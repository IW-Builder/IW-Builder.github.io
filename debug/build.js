// Builds debug/index.html from the template and the readable bookmarklet source.
// Run from the repo root: npm i --no-save terser@5 && node debug/build.js
// The bookmark is minified (local names shortened, comments and indentation
// dropped) and only the characters a URL can't carry are percent-encoded, so
// it stays short enough for bookmark fields and copy-paste.
const fs = require('fs');
let terser;
try { terser = require('terser'); }
catch { console.error('Needs terser: npm i --no-save terser@5'); process.exit(1); }

(async () => {
  const src = fs.readFileSync('debug/IW-Debug-Exporter-bookmarklet.js', 'utf8');
  new Function(src); // syntax check
  const { code } = await terser.minify(src, { compress: false, mangle: true, format: { ascii_only: true } });
  const encoded = code.replace(/[%\s"<>#\\^`{|}]/g, c => '%' + c.charCodeAt(0).toString(16).padStart(2, '0').toUpperCase());
  if (decodeURIComponent(encoded) !== code) throw new Error('encoding does not round-trip');
  new Function(decodeURIComponent(encoded));
  const bookmark = 'javascript:' + encoded;
  const html = fs.readFileSync('debug/index.template.html', 'utf8').replace('"__BOOKMARK__"', () => JSON.stringify(bookmark));
  fs.writeFileSync('debug/index.html', html);
  console.log('debug/index.html written, bookmark', bookmark.length, 'chars');
})();
