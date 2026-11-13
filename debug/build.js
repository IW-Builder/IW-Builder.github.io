// Builds debug/index.html from the template and the readable bookmarklet source.
// Run from the repo root: npm i --no-save terser@5 && node debug/build.js
// The exporter is minified, then deflated and base64-encoded inside a small
// loader, because Edge's favorites editor cuts bookmarks off at about 10,000
// characters. The page also offers the minified code for the browser console.
const fs = require('fs');
const zlib = require('zlib');
let terser;
try { terser = require('terser'); }
catch { console.error('Needs terser: npm i --no-save terser@5'); process.exit(1); }

(async () => {
  const src = fs.readFileSync('debug/IW-Debug-Exporter-bookmarklet.js', 'utf8');
  new Function(src); // syntax check
  const { code } = await terser.minify(src, { compress: false, mangle: true, format: { ascii_only: true } });
  new Function(code);
  const packed = zlib.deflateRawSync(code, { level: 9 }).toString('base64');
  if (zlib.inflateRawSync(Buffer.from(packed, 'base64')).toString() !== code) throw new Error('packing does not round-trip');
  const loader = '(async()=>{try{Function(await new Response(new Blob([Uint8Array.from(atob("' + packed +
    '"),c=>c.charCodeAt(0))]).stream().pipeThrough(new DecompressionStream("deflate-raw"))).text())()}' +
    'catch(e){alert("IW Debug Exporter could not start ("+e.message+"). Use the console method on the install page.")}})()';
  new Function(loader);
  const bookmark = 'javascript:' + loader.replace(/[%\s"<>#\\^`{|}]/g, c => '%' + c.charCodeAt(0).toString(16).padStart(2, '0').toUpperCase());
  const html = fs.readFileSync('debug/index.template.html', 'utf8')
    .replace('"__BOOKMARK__"', () => JSON.stringify(bookmark))
    .replace('"__CONSOLE__"', () => JSON.stringify(code));
  fs.writeFileSync('debug/index.html', html);
  console.log('debug/index.html written, bookmark', bookmark.length, 'chars');
})();
