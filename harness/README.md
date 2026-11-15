# IW Harness page helper

The page helper that browser agents load into an open [Infinite Worlds](https://infiniteworlds.app/) game tab to read each turn's debug data, wait for turns and keep per-turn records. It defines `window.IWH`. It reads the page's own data the way the [Debug Exporter](https://iw-builder.github.io/debug/) does, sends nothing anywhere, and holds no keys or account data.

## Loading it

An agent with a JavaScript tool on the IW tab pastes one line. The line fetches that exact build from this folder, checks the file's SHA-256 and the build id, and only then runs it. It answers with the helper's summary, or `ok: false` and the reason (for example a page that refuses to fetch from this site), in which case load the helper the older way, by pasting the parts.

<!-- current -->
Current build: **1.27**, build `c9a0f27575cc`. Paste this line into the IW page's JavaScript tool:

```js
(async(B,H)=>{const u='https://iw-builder.github.io/harness/builds/'+B+'.js';let t;try{const r=await fetch(u,{cache:'no-store'});if(!r.ok)return{ok:false,reason:'HTTP '+r.status+' from '+u+' (not published yet?): paste the parts instead'};t=await r.text()}catch(e){return{ok:false,reason:'This page could not fetch '+u+' (its CSP or the network): paste the parts instead',error:String(e)}}const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(t)))].map(b=>b.toString(16).padStart(2,'0')).join('');if(h!==H)return{ok:false,reason:'The fetched file is not build '+B+': paste the parts instead',got:h.slice(0,12)};const s=await(0,eval)(t);return window.IWH&&IWH.build===B?s:{ok:false,reason:'Loaded, but IWH.build is '+(window.IWH&&IWH.build)}})('c9a0f27575cc','da0eef0ceca905a56fcdcb473ddf7366d0780c69e5382be75ec342631704eb74')
```
<!-- /current -->

After the first load the helper keeps itself in the page's localStorage, so a reload needs only `(0,eval)(localStorage.getItem('IWH_SRC'))`. Then check the build with `IWH.checkBuild('<build>')`; a stored copy can be several releases old, and pasting the loader line again replaces it.

## Files

- `builds/<build>.js`: each released build, never changed once published, so a runbook that names a build always gets the same bytes. The build id is the first 12 hex digits of the SHA-256 of the helper's source.

Only the minified helper is published here. Its source, tests and runbooks are kept in the IW-Builder workshop.
