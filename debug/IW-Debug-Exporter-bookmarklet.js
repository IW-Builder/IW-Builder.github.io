/* IW Debug Exporter - bookmarklet edition (readable source).
 * Use on infiniteworlds.app with a game open (not while a turn is generating).
 * For every turn of the game it collects what World debug tools shows: the
 * evaluation, thinking (if the model has any), triggers fired, active
 * instruction blocks, matched lore and PawScript results and errors.
 * Downloads a readable .txt and a full .json. Read-only: it takes no game
 * actions, and puts the game back on the turn you were viewing.
 */
(() => {
  if (window.__iwDebugRunning) { alert('IW Debug Exporter is already running.'); return; }
  if (!/infiniteworlds\.app$/.test(location.hostname)) { alert('Open infiniteworlds.app first, then click the bookmark.'); return; }
  window.__iwDebugRunning = true;

  // Status box
  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;z-index:2147483647;right:16px;bottom:16px;max-width:340px;padding:12px 14px;border-radius:10px;background:#1b1830;color:#eee;font:14px/1.4 system-ui,sans-serif;box-shadow:0 4px 20px rgba(0,0,0,.5);border:1px solid #6b5fb5';
  const text = document.createElement('div');
  const close = document.createElement('button');
  close.textContent = 'Stop and save';
  close.style.cssText = 'margin-top:8px;padding:3px 10px;border-radius:6px;border:1px solid #888;background:#2a2645;color:#eee;cursor:pointer';
  box.append(text, close);
  document.body.appendChild(box);
  const say = msg => { text.textContent = 'IW Debug Exporter: ' + msg; };

  const originalSend = WebSocket.prototype.send;
  const pending = new Map(), late = new Set();
  let socket = null, stopped = false, wrapped = null, original = null, gotSocket;
  const socketReady = new Promise(r => { gotSocket = r; });
  const turns = [];
  let meta = {};

  function finish(msg) {
    stopped = true;
    if (WebSocket.prototype.send === hookedSend) WebSocket.prototype.send = originalSend;
    if (socket && wrapped && socket.onmessage === wrapped) socket.onmessage = original;
    for (const w of pending.values()) clearTimeout(w.timer);
    pending.clear();
    delete window.__iwDebugRunning;
    say(msg);
    close.textContent = 'Close';
    close.onclick = () => box.remove();
  }
  close.onclick = () => { if (!stopped) stopRequested = true; };
  let stopRequested = false;

  // Consume replies to our own requests so the IW page never sees them.
  function receive(data) {
    if (typeof data !== 'string' || !(pending.size || late.size)) return false;
    let m; try { m = JSON.parse(data); } catch { return false; }
    if (late.delete(m.id)) return true;
    const w = pending.get(m.id);
    if (!w) return false;
    pending.delete(m.id); clearTimeout(w.timer);
    if (m.response != null) w.resolve(m.response);
    else w.reject(new Error('IW returned an error: ' + JSON.stringify(m.error || m).slice(0, 200)));
    return true;
  }
  function wrap(ws) {
    if (ws.onmessage === wrapped && wrapped) return;
    original = ws.onmessage;
    wrapped = function (e) { if (receive(e.data)) return; if (typeof original === 'function') return original.call(this, e); };
    ws.onmessage = wrapped;
  }
  // Borrow IW's own connection: the next message the page sends (a keep-alive
  // goes out about every 30 seconds) tells us which socket to use.
  function hookedSend(data) {
    if (!socket && this instanceof WebSocket) { socket = this; wrap(this); gotSocket(); }
    return originalSend.call(this, data);
  }
  WebSocket.prototype.send = hookedSend;

  // get_ui_info is what the "Previous turn" / "Next turn" buttons call.
  // change_to_turns_ago is relative to the turn the server is showing:
  // 1 = one turn back, -1 = one turn forward, 0 = stay.
  function step(turnsAgo) {
    return new Promise((resolve, reject) => {
      if (socket.readyState !== WebSocket.OPEN) return reject(new Error('Connection to IW closed. Reload the page and try again.'));
      wrap(socket);
      const id = crypto.randomUUID();
      const timer = setTimeout(() => { pending.delete(id); late.add(id); reject(new Error('IW did not answer in time.')); }, 45000);
      pending.set(id, {resolve, reject, timer});
      originalSend.call(socket, JSON.stringify({type: 'CALL', id, v: 8, args: [], vt_global: [], objects: [], command: 'get_ui_info',
        kwargs: {change_to_turns_ago: turnsAgo, getting_alt_image: false, images_only_just_made: false}}));
    });
  }

  // A turn's reply is a list of fields; the prologue's is a named object.
  // Find fields by shape so a reordering in IW shows up as an error, not bad data.
  function view(r) {
    if (!Array.isArray(r)) return {prologue: true, turn: 0, max: r.max_turn_number, title: r.adventure_title, character: r.character_name, prologue_text: r.prologue_text, debug: r.world_debug_tools_data || null};
    const debug = r.find(x => x && typeof x === 'object' && !Array.isArray(x) && 'fired_triggers' in x && 'script_evaluations' in x);
    if (!debug || typeof r[3] !== 'number' || typeof r[4] !== 'number') throw new Error('IW changed its reply format; this exporter needs an update.');
    return {prologue: false, turn: r[3], max: r[4], action: r[0], narration: r[1], title: r[11], character: r[12], secret_info: r[13],
      tracked_items: (r[14] || []).map(t => ({name: t.name, value: t.value, visibility: t.visibility})),
      evaluation: typeof r[24] === 'string' ? r[24] : '', thinking: typeof r[25] === 'string' ? r[25] : '', debug};
  }
  function record(v) {
    const d = v.debug || {};
    const names = Object.fromEntries((d.trigger_definitions || []).map(t => [t.id, t.name]));
    const blocks = Object.fromEntries((d.instruction_blocks || []).map(b => [b.name, b.content]));
    const evals = (d.script_evaluations || []).map(s => ({trigger: s.trigger_name || names[s.trigger_id] || s.trigger_id, kind: s.kind, status: s.status, effect: s.effect_name, error: s.error}));
    return {
      turn: v.turn, action: v.action, evaluation: v.evaluation, thinking: v.thinking,
      triggers_fired: (d.fired_triggers || []).map(t => ({name: names[t.id] || t.id, count: t.count})),
      active_instruction_blocks: (d.active_instruction_blocks || []).map(n => ({name: n, content: blocks[n] ?? null})),
      matched_lore: d.matched_lorebook_entries || [],
      pawscript: evals,
      pawscript_errors: evals.filter(s => s.error || /error|fail/i.test(s.status || '')),
      world_debug_log: d.world_debug_log || [],
      narration: v.narration, secret_info: v.secret_info, tracked_items: v.tracked_items,
      raw_debug: d
    };
  }

  function txt() {
    const L = [];
    L.push('== ' + (meta.title || 'Infinite Worlds game') + ' - debug export ==', '', 'Character: ' + (meta.character || ''), 'Exported: ' + new Date().toISOString(), 'Turns: ' + turns.length + (meta.complete ? '' : ' (incomplete: ' + meta.reason + ')'), '');
    let prevBlocks = {};
    for (const t of turns) {
      L.push('', '-- Turn ' + t.turn + ' --', '');
      if (t.action) L.push('Action', '------', t.action, '');
      L.push('Evaluation', '----------', t.evaluation || '(none)', '');
      if (t.thinking) L.push('Thinking', '--------', t.thinking, '');
      L.push('Triggers fired', '--------------', t.triggers_fired.length ? t.triggers_fired.map(x => '- ' + x.name + (x.count > 1 ? ' (x' + x.count + ')' : '')).join('\n') : '(none)', '');
      L.push('Active instruction blocks', '-------------------------');
      if (!t.active_instruction_blocks.length) L.push('(none)');
      for (const b of t.active_instruction_blocks) {
        if (b.content == null) L.push('- ' + b.name);
        else if (prevBlocks[b.name] === b.content) L.push('- ' + b.name + ' (unchanged)');
        else L.push('- ' + b.name + ':', b.content.split('\n').map(s => '    ' + s).join('\n'));
      }
      prevBlocks = Object.fromEntries(t.active_instruction_blocks.map(b => [b.name, b.content]));
      L.push('');
      if (t.matched_lore.length) L.push('Lore matched', '------------', t.matched_lore.map(x => '- ' + (typeof x === 'string' ? x : JSON.stringify(x))).join('\n'), '');
      L.push('PawScript', '---------');
      if (!t.pawscript.length) L.push('(nothing ran)');
      for (const s of t.pawscript) L.push('- ' + s.trigger + ' [' + s.kind + (s.effect ? ': ' + s.effect : '') + '] ' + s.status + (s.error ? '  ERROR: ' + (typeof s.error === 'string' ? s.error : JSON.stringify(s.error)) : ''));
      L.push('PawScript errors: ' + t.pawscript_errors.length, '');
      if (t.world_debug_log.length) L.push('World debug log', '---------------', t.world_debug_log.map(x => '- ' + (typeof x === 'string' ? x : JSON.stringify(x))).join('\n'), '');
    }
    return L.join('\n');
  }
  function download(content, ext, mime) {
    if (window.__iwDebugNoDownload) { (window.__iwDebugOutput ||= {})[ext] = content; return; }
    const url = URL.createObjectURL(new Blob([content], {type: mime}));
    const a = document.createElement('a');
    const slug = (meta.title || 'game').replace(/[^\w.-]+/g, '_').slice(0, 60);
    a.href = url; a.download = 'IW-Debug-' + slug + '-' + new Date().toISOString().replaceAll(':', '-').slice(0, 19) + ext;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  }
  function save(prefix) {
    finish('saving...');
    download(txt(), '.txt', 'text/plain;charset=utf-8');
    download(JSON.stringify({exported_at: new Date().toISOString(), ...meta, turns}, null, 2), '.json', 'application/json');
    say(prefix + turns.length + ' turns downloaded as TXT and JSON.');
  }

  async function run() {
    say('waiting for the connection (up to 30 seconds)...');
    await socketReady;
    let start, here, reason = '';
    meta = {complete: false};
    try {
      // Where is the game now?
      start = view(await step(0));
      here = start.turn;
      meta.title = start.title; meta.character = start.character; meta.max_turn = start.max;
      if (!start.max) throw new Error('This game has no turns yet.');
      // Walk back to turn 1, then forward one turn at a time.
      let v = view(await step(here >= 1 ? here - 1 : -1));
      here = v.turn;
      if (v.turn !== 1) throw new Error('Could not reach turn 1 (got turn ' + v.turn + ').');
      for (;;) {
        turns.push(record(v));
        say('collected turn ' + v.turn + ' of ' + v.max + '...');
        if (stopRequested) { reason = 'stopped by you'; break; }
        if (v.turn >= v.max) { meta.complete = true; break; }
        v = view(await step(-1));
        here = v.turn;
        await new Promise(r => setTimeout(r, 150));
      }
    } catch (e) {
      reason = e.message;
    }
    // Put the game back on the turn the player was viewing.
    try {
      if (start && here != null && here !== start.turn) {
        const back = view(await step(here - start.turn));
        if (back.turn !== start.turn) reason += ' Warning: the game is now on turn ' + back.turn + '; reload the page.';
      }
    } catch (e) { reason += ' Warning: could not restore the view (' + e.message + '); reload the page before playing.'; }
    meta.reason = reason;
    if (!turns.length) return finish('Failed: ' + (reason || 'nothing collected'));
    save(meta.complete ? 'Done. ' : 'Partial export (' + reason + '). ');
  }
  run();
})();
