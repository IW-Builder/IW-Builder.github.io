// Builds debug/index.html from the template and the readable bookmarklet source.
// Run from the repo root: node debug/build.js
const fs = require('fs');
const src = fs.readFileSync('debug/IW-Debug-Exporter-bookmarklet.js', 'utf8');
new Function(src); // syntax check
const bookmark = 'javascript:' + encodeURIComponent(src);
const html = fs.readFileSync('debug/index.template.html', 'utf8').replace('"__BOOKMARK__"', JSON.stringify(bookmark));
fs.writeFileSync('debug/index.html', html);
console.log('debug/index.html written, bookmark', bookmark.length, 'chars');
