/* IW Cost Exporter - bookmarklet edition (readable source).
 * Use on infiniteworlds.app: open Credit activity, then click the bookmark.
 * Collects your full credit history and downloads CSV + JSON. Read-only.
 */
(() => {
  if (window.__iwCostsRunning) { alert('IW Cost Exporter is already running.'); return; }
  if (!/infiniteworlds\.app$/.test(location.hostname)) { alert('Open infiniteworlds.app first, then click the bookmark.'); return; }
  window.__iwCostsRunning = true;

  // Status box
  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;z-index:2147483647;right:16px;bottom:16px;max-width:320px;padding:12px 14px;border-radius:10px;background:#1b1830;color:#eee;font:14px/1.4 system-ui,sans-serif;box-shadow:0 4px 20px rgba(0,0,0,.5);border:1px solid #6b5fb5';
  const text = document.createElement('div');
  const close = document.createElement('button');
  close.textContent = 'Stop and save';
  close.style.cssText = 'margin-top:8px;padding:3px 10px;border-radius:6px;border:1px solid #888;background:#2a2645;color:#eee;cursor:pointer';
  box.append(text, close);
  document.body.appendChild(box);
  const say = msg => { text.textContent = 'IW Cost Exporter: ' + msg; };

  const originalSend = WebSocket.prototype.send;
  const pending = new Map(), late = new Set();
  let socket, template, stopped = false, wrapped = null, original = null;
  const records = [];

  function finish(msg) {
    stopped = true;
    if (WebSocket.prototype.send === hookedSend) WebSocket.prototype.send = originalSend;
    if (socket && wrapped && socket.onmessage === wrapped) socket.onmessage = original;
    for (const w of pending.values()) clearTimeout(w.timer);
    pending.clear();
    delete window.__iwCostsRunning;
    say(msg);
    close.textContent = 'Close';
    close.onclick = () => box.remove();
  }
  // Stop now and download whatever has been collected so far.
  close.onclick = () => {
    if (stopped) return;
    if (!records.length) return finish('Stopped. Nothing had been collected yet.');
    save(false, 'Stopped. ');
  };

  // DateTime values arrive beside the response in message.objects.
  function applyObjects(message) {
    for (const o of message.objects || []) {
      const p = o.path || [];
      if (p[0] !== 'response' || p.length < 2) continue;
      let t = message.response;
      for (let i = 1; i < p.length - 1 && t != null; i++) t = t[p[i]];
      if (t == null || typeof t !== 'object') continue;
      const key = p[p.length - 1];
      const type = Array.isArray(o.type) ? o.type[0] : o.type;
      if (type === 'DateTime' && typeof o.value === 'string') {
        const d = new Date(o.value.replace(' ', 'T').replace(/(\.\d{3})\d*/, '$1').replace(/([+-]\d{2})(\d{2})$/, '$1:$2'));
        t[key] = isNaN(d) ? o.value : d.toISOString();
      } else if (t[key] == null) t[key] = o.value;
    }
  }
  // Consume replies to our own requests so IW never sees them.
  function receive(data) {
    if (typeof data !== 'string' || !(pending.size || late.size)) return false;
    let m; try { m = JSON.parse(data); } catch { return false; }
    if (late.delete(m.id)) return true; // reply to a request that already timed out
    const w = pending.get(m.id);
    if (!w) return false;
    pending.delete(m.id); clearTimeout(w.timer);
    if (Array.isArray(m.response)) { applyObjects(m); w.resolve(m.response); }
    else w.reject(new Error('Unexpected reply from IW.'));
    return true;
  }
  function wrap(ws) {
    if (ws.onmessage === wrapped && wrapped) return;
    original = ws.onmessage;
    wrapped = function (e) { if (receive(e.data)) return; if (typeof original === 'function') return original.call(this, e); };
    ws.onmessage = wrapped;
  }
  function hookedSend(data) {
    if (!template && typeof data === 'string') {
      try {
        const m = JSON.parse(data);
        if (m.type === 'CALL' && m.command === 'getRecentCreditTransactions') {
          socket = this; template = m; wrap(this);
          setTimeout(run, 0);
        }
      } catch { /* other traffic */ }
    }
    return originalSend.call(this, data);
  }
  WebSocket.prototype.send = hookedSend;

  function request(offset, limit) {
    return new Promise((resolve, reject) => {
      if (stopped) return reject(new Error('Cancelled.'));
      if (socket.readyState !== WebSocket.OPEN) return reject(new Error('Connection to IW closed. Reload the page and try again.'));
      wrap(socket);
      const id = crypto.randomUUID();
      const timer = setTimeout(() => { pending.delete(id); late.add(id); reject(new Error('IW did not answer in time.')); }, 45000);
      pending.set(id, {resolve, reject, timer});
      originalSend.call(socket, JSON.stringify({...template, id, kwargs: {...template.kwargs, offset, limit, transaction_type: null}}));
    });
  }

  function flatten(v, prefix = '', out = {}) {
    for (const [k, item] of Object.entries(v)) {
      const name = prefix ? prefix + '.' + k : k;
      if (item !== null && typeof item === 'object' && !Array.isArray(item)) flatten(item, name, out);
      else out[name] = Array.isArray(item) ? JSON.stringify(item) : item;
    }
    return out;
  }
  function csv() {
    const rows = records.map((r, i) => flatten({history_index: i, ...r}));
    const cols = [...new Set(rows.flatMap(r => Object.keys(r)))];
    if (cols.includes('datetime')) { cols.splice(cols.indexOf('datetime'), 1); cols.splice(1, 0, 'datetime'); }
    const cell = v => {
      let s = v == null ? '' : String(v);
      if (typeof v === 'string' && /^[=+\-@\t\r\n]/.test(s)) s = "'" + s;
      return '"' + s.replaceAll('"', '""') + '"';
    };
    return '﻿' + [cols.map(cell).join(','), ...rows.map(r => cols.map(c => cell(r[c])).join(','))].join('\r\n');
  }
  function download(content, ext, mime) {
    const url = URL.createObjectURL(new Blob([content], {type: mime}));
    const a = document.createElement('a');
    a.href = url; a.download = 'IW-Cost-History-' + new Date().toISOString().replaceAll(':', '-').slice(0, 19) + ext;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  }

  async function run() {
    let offset = 0, previous = null, complete = false, reason = '';
    // A slow or dropped reply is retried up to 4 times, with smaller batches and a pause.
    async function fetchBatch() {
      let size = 50;
      for (let attempt = 1; ; attempt++) {
        try { return await request(offset, size); }
        catch (e) {
          if (stopped || attempt > 4 || /closed|Unexpected/.test(e.message)) throw e;
          size = Math.max(10, Math.floor(size / 2));
          say('IW is slow to answer; retrying (' + attempt + '/4) at ' + records.length + ' transactions...');
          await new Promise(r => setTimeout(r, 3000 * attempt));
        }
      }
    }
    try {
      while (!stopped) {
        const batch = await fetchBatch();
        if (!batch.length) { complete = true; break; }
        const sig = JSON.stringify(batch);
        if (sig === previous) throw new Error('IW repeated a batch; stopping.');
        previous = sig;
        records.push(...batch);
        offset += batch.length;
        say('collected ' + records.length + ' transactions...');
        await new Promise(r => setTimeout(r, 300));
      }
    } catch (e) {
      if (stopped) return;
      if (!records.length) return finish('Failed: ' + e.message);
      reason = e.message;
    }
    if (stopped) return;
    save(complete, complete ? 'Done. ' : 'Partial export (' + reason + ' Click the bookmark again to retry). ');
  }
  function save(complete, prefix) {
    finish('saving...'); // stops collection first, so no more records arrive
    download(csv(), '.csv', 'text/csv;charset=utf-8');
    download(JSON.stringify({exported_at: new Date().toISOString(), complete, records}, null, 2), '.json', 'application/json');
    say(prefix + records.length + ' transactions downloaded as CSV and JSON.');
  }

  // Trigger IW's own request: click Show more if the dialog is open.
  const more = [...document.querySelectorAll('a,button,span,div')].find(e => e.children.length === 0 && e.textContent.trim() === 'Show more' && e.offsetParent);
  if (more) { say('starting...'); more.click(); }
  else say('open Credit activity (click your credits balance at the top), then click Show more.');
})();
