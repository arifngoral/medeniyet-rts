// Aevum - relay outage + multiplayer save/continue over the lockstep (in-memory relay, fake clock, real Game sims).
// Run: node test/net-outage-test.mjs
//  1. 3 humans + 1 AI play; the relay disappears for 20 simulated seconds and comes back EMPTY (like a restarted
//     node server): every session must stall ("Sunucuya yeniden bağlanılıyor…"), drop nobody, re-register with the
//     same peer id, exchange what it missed and end with equal hashes.
//  2. A joiner presses "Kaydet": all clients save at the same tick with equal hashes (verified over 'sync').
//  3. Everybody leaves; new sessions continue the save: the host opens the saved lobby, one player is matched by name
//     (case-insensitive), a stranger waits / claims / is freed, the absent player's slot is taken over by an AI; the
//     save travels as a blob, is hash-checked, deserialized with each client's own `me`, and the lockstep runs on.
import { NetSession, STEP, TURN_TICKS, DROP_SILENT_MS } from '../src/net/session.js';
import { Game } from '../src/sim/game.js';

let failed = 0;
const ok = (c, msg) => { if (c) console.log('  ok   ' + msg); else { failed++; console.log('  FAIL ' + msg); } return !!c; };
function mulberry(a) { return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const netRnd = mulberry(777);

// ---------- fake clock ----------
const clock = {
  t: 0, timers: [], nextId: 1,
  now() { return this.t; },
  setInterval(fn, ms) { const id = this.nextId++; this.timers.push({ id, fn, ms, at: this.t + ms }); return id; },
  clearInterval(id) { this.timers = this.timers.filter(x => x.id !== id); },
  fire() { for (const x of this.timers.slice()) while (x.at <= this.t && this.timers.includes(x)) { x.at += x.ms; x.fn(); } },
};
const fakeClock = { now: () => clock.now(), setInterval: (f, ms) => clock.setInterval(f, ms), clearInterval: id => clock.clearInterval(id) };

// ---------- in-memory relay that can go away (and come back with no rooms) ----------
const LOSS = 0.1, LAT_MAX = 200;
const relay = {
  up: true, rooms: new Map(), queue: [], blobs: new Map(), transports: new Set(),
  deliver() {
    const due = this.queue.filter(m => m.at <= clock.t);
    if (!due.length) return;
    this.queue = this.queue.filter(m => m.at > clock.t);
    for (const m of due) if (!m.to.closed) m.fn();
  },
  later(to, fn, ms) { this.queue.push({ to, fn, at: clock.t + ms }); },
  down() { this.up = false; this.rooms.clear(); this.queue = []; for (const t of this.transports) t._lost(); },
  restart() { this.up = true; },   // empty rooms; transports find out by themselves (backoff)
};
class MemTransport {
  constructor(id) { this.id = id; this.h = new Map(); this.pf = []; this.sf = []; this.room = null; this.closed = false; this.up = false; this.reg = false; this.fails = 0; this.retryAt = null; this._peers = new Set(); relay.transports.add(this); }
  async connect(room) { this.room = room; this._register(); if (!this.reg) throw new Error('relay down'); }
  _register() {
    if (this.closed || !relay.up) return false;
    let r = relay.rooms.get(this.room); if (!r) { r = new Set(); relay.rooms.set(this.room, r); }
    const isNew = !r.has(this);
    r.add(this); this.reg = true; this.fails = 0; this.retryAt = null;
    // hello: the peers currently registered (anyone else looks "left" until it re-registers)
    const before = this._peers; this._peers = new Set([...r].filter(o => o !== this).map(o => o.id));
    const joined = [...this._peers].filter(p => !before.has(p)), left = [...before].filter(p => !this._peers.has(p));
    if (joined.length || left.length) this._emitPeers(joined, left);
    if (isNew) for (const o of r) if (o !== this) o._joinedPeer(this.id);
    this._setUp(true);
    return true;
  }
  _joinedPeer(p) { if (!this._peers.has(p)) { this._peers.add(p); this._emitPeers([p], []); } }
  _leftPeer(p) { if (this._peers.delete(p)) this._emitPeers([], [p]); }
  _lost() { this.reg = false; this._setUp(false); this.fails = 1; this.retryAt = clock.t + 400; }
  tick() { // reconnect loop of a real transport: 0.4 s -> 3 s backoff
    if (this.closed || this.reg || this.retryAt == null || clock.t < this.retryAt) return;
    if (!this._register()) { this.fails++; this.retryAt = clock.t + Math.min(3000, 400 * Math.pow(1.6, this.fails - 1)); }
  }
  _emitPeers(joined, left) { const ch = { joined, left, peers: [...this._peers] }; for (const f of this.pf) f(ch); }
  _setUp(up) { if (this.up === up) return; this.up = up; for (const f of this.sf) f({ up }); }
  send(topic, data) {
    if (this.closed || !this.room || !relay.up || !this.reg) return;
    const s = JSON.stringify(data);
    const r = relay.rooms.get(this.room); if (!r) return;
    for (const o of r) {
      if (o === this || netRnd() < LOSS) continue;
      const d = JSON.parse(s);
      relay.later(o, () => { if (o.reg) o._recv(topic, d, this.id); }, netRnd() * LAT_MAX);
    }
  }
  _recv(topic, data, from) { for (const f of this.h.get(topic) || []) f(data, from); }
  on(topic, fn) { if (!this.h.has(topic)) this.h.set(topic, []); this.h.get(topic).push(fn); }
  onPeers(fn) { this.pf.push(fn); }
  onStatus(fn) { this.sf.push(fn); }
  peers() { return [...this._peers]; }
  async putBlob(text) { if (!relay.up) throw new Error('relay down'); const id = 'b' + relay.blobs.size; relay.blobs.set(this.room + ':' + id, text); return id; }
  async getBlob(id) { const t = relay.blobs.get(this.room + ':' + id); if (t == null) throw new Error('404'); return t; }
  close() {
    if (this.closed) return; this.closed = true; relay.transports.delete(this);
    const r = relay.rooms.get(this.room); if (!r) return;
    r.delete(this); for (const o of r) o._leftPeer(this.id);
  }
}

const flush = async () => { for (let i = 0; i < 6; i++) await Promise.resolve(); };
async function runFor(ms, onFrame, step = 1000 / 60) {
  const end = clock.t + ms;
  while (clock.t < end) {
    clock.t += step;
    for (const t of relay.transports) t.tick();
    relay.deliver(); clock.fire();
    if (onFrame) onFrame(step / 1000);
    await flush();
  }
}
async function until(cond, maxMs = 20000) { for (let t = 0; t < maxMs && !cond(); t += 25) await runFor(25); return cond(); }

function track(s, name) {
  const ev = { stall: 0, resume: 0, relayStall: 0, desync: 0, peerLeft: [], closed: null, start: null, saves: [], verified: [], mismatch: [], texts: new Set() };
  s.on('stall', d => { ev.stall++; if (d && d.relay) ev.relayStall++; if (d && d.text) ev.texts.add(d.text); });
  s.on('stallUpdate', d => { if (d && d.relay) ev.relayStall++; if (d && d.text) ev.texts.add(d.text); });
  s.on('resume', () => ev.resume++);
  s.on('desync', d => { ev.desync++; console.log('  desync on', name, d); });
  s.on('peerLeft', d => ev.peerLeft.push(d));
  s.on('closed', d => { ev.closed = d.reason; });
  s.on('start', d => { ev.start = d; });
  s.on('saveVerified', d => ev.verified.push(d.id));
  s.on('saveMismatch', d => ev.mismatch.push(d.id));
  return ev;
}

// scripted play, same as net-test (random pace, real game commands)
function makeScript(S, games, rnds) {
  return i => {
    if (rnds[i]() > 0.02) return;
    const g = games[i], me = S[i].me;
    const mine = g.units.filter(u => u.owner === me && !u.dead);
    const r = rnds[i](), p = g.players[me];
    if (mine.length && r < 0.7) {
      const ids = mine.filter(() => rnds[i]() < 0.5).map(u => u.id).slice(0, 12); if (!ids.length) ids.push(mine[0].id);
      S[i].issue('cmdMove', [ids, p.startX + (rnds[i]() - 0.5) * 20, p.startZ + (rnds[i]() - 0.5) * 20, false]);
    } else {
      const tc = g.buildings.find(b => b.owner === me && !b.dead && b.type === 'towncenter');
      if (tc) S[i].issue('train', [tc.id, 'villager']);
    }
  };
}
async function syncTo(S, games, extraTurns = 30) {
  const target = Math.max(...S.map(s => s.tick)) + extraTurns * TURN_TICKS;
  for (let k = 0; k < 40000 && S.some(s => s.tick < target); k++) {
    clock.t += 5; for (const t of relay.transports) t.tick(); relay.deliver(); clock.fire();
    for (let i = 0; i < S.length; i++) if (S[i].tick < target) { S[i]._acc = 0; S[i]._slow = false; S[i].advance(games[i], STEP); }
    await flush();
  }
  return S.every(s => s.tick === target);
}

// =====================================================================================
console.log('Part 1 — lobby, match, relay outage');
const names = ['Host', 'Ayse', 'Mehmet'];
const S = names.map((n, i) => new NetSession(new MemTransport('peer' + i), { clock: fakeClock, name: n, log: true }));
const E = S.map((s, i) => track(s, names[i]));
const code = await S[0].host();
let joined = false; Promise.all([S[1].join(code), S[2].join(code)]).then(() => { joined = true; });
ok(await until(() => joined), 'two joiners in the lobby');
S[1].setTeam(1); S[2].setTeam(1); S[0].addAI(2, 'normal'); S[0].setSettings({ mapSize: 96 });
S[1].setReady(true); S[2].setReady(true);
await runFor(3000);
ok(S[0].canStart().ok, 'host can start (3 humans team 1, AI team 2)');
S[0].start();
ok(await until(() => E.every(e => e.start)), 'everybody started');
const cfgs = E.map(e => e.start.cfg);
const games = cfgs.map(c => new Game(Object.assign({}, c)));
const rnds = [mulberry(1), mulberry(2), mulberry(3)];
const script = makeScript(S, games, rnds);
let playing = true;
const frame = dt => { for (let i = 0; i < S.length; i++) { if (S[i].phase !== 'game') continue; if (playing) script(i); S[i].advance(games[i], dt); } };
await runFor(60000, frame);
const tickBefore = S[0].tick;
ok(tickBefore > 60 * 30 * 0.9, 'match running (' + tickBefore + ' ticks)');

relay.down();
await runFor(20000, frame);
const tickDuring = S[0].tick;
ok(tickDuring - tickBefore < 30, 'lockstep stalls while the relay is down (' + (tickDuring - tickBefore) + ' ticks in 20 s)');
ok(E.every(e => e.relayStall > 0), 'every client shows the reconnect stall');
ok(E.every(e => e.texts.has('Sunucuya yeniden bağlanılıyor…')), 'stall text "Sunucuya yeniden bağlanılıyor…"');
ok(S.every(s => s.leftAt.size === 0), 'nobody dropped during the outage');
relay.restart();
await runFor(60000, frame);
ok(S.every(s => s.phase === 'game') && E.every(e => !e.closed), 'all sessions still in the game after the relay came back');
ok(S.every(s => s.leftAt.size === 0) && E.every(e => e.peerLeft.length === 0), 'nobody dropped after the relay came back');
ok(S[0].tick > tickDuring + 50 * 30, 'match continues after the relay came back (' + tickDuring + ' -> ' + S[0].tick + ')');
ok(S.every(s => s.t.reg) && S.every(s => s.t.peers().length === 2), 'all transports re-registered with the same ids (peers: ' + S.map(s => s.t.peers().join('+')).join(' / ') + ')');
ok(E.every(e => e.resume >= 1), 'resume after the outage');

console.log('Part 2 — lockstep save');
const recs = [];
S.forEach((s, i) => s.on('save', ev => {
  recs[i] = { name: 'test', time: 0, mp: true, code: s.match, tick: ev.tick, me: ev.game.me, hash: ev.hash, by: ev.by,
    players: ev.game.players.map(p => ({ name: p.name, team: p.team, kind: p.isAI ? 'ai' : 'human', difficulty: p.difficulty || null, color: p.color })), data: JSON.parse(JSON.stringify(ev.game.serialize())) };
}));
const saveId = S[1].requestSave(false);
ok(typeof saveId === 'string', 'requestSave returns an id');
await runFor(4000, frame);
ok(recs.length === 3 && recs.every(Boolean), 'all 3 clients saved');
ok(recs.every(r => r.tick === recs[0].tick), 'saved at the same game tick (' + recs.map(r => r.tick).join('/') + ')');
ok(recs.every(r => r.hash === recs[0].hash), 'equal save hashes ' + recs.map(r => r.hash).join(' / '));
ok(recs.every(r => r.by === 'Ayse'), 'save attributed to the requester');
ok(E.every(e => e.verified.includes(saveId)) && E.every(e => !e.mismatch.length), 'every client verified the save over sync (no mismatch)') ||
  console.log('    verified', E.map(e => e.verified.join(',')), 'mismatch', E.map(e => e.mismatch.join(',')), S.map(s => JSON.stringify([...s._saveH].map(([k, v]) => [k, v.mine, [...v.peers], v.done, v.tries]))));
playing = false;
ok(await syncTo(S, games), 'all clients brought to the same tick');
const H = games.map(g => g.hash());
ok(H.every(h => h === H[0]), 'equal game.hash() after outage + save: ' + H.join(' / '));
const L = S.map(s => JSON.stringify(s._log));
ok(L.every(l => l === L[0]), 'identical command streams (' + S[0]._log.length + ' commands)');
ok(E.every(e => !e.desync), 'no desync reported');
S.forEach(s => s.close());

console.log('Part 3 — continue the saved match');
const rec = recs[0];
const H2 = new NetSession(new MemTransport('peerH2'), { clock: fakeClock, name: 'Host' });
const J2 = new NetSession(new MemTransport('peerJ2'), { clock: fakeClock, name: 'ayse' });
const Z2 = new NetSession(new MemTransport('peerZ2'), { clock: fakeClock, name: 'Zeynep' });
const E2 = [H2, J2, Z2].map((s, i) => track(s, ['H2', 'J2', 'Z2'][i]));
const code2 = await H2.hostResume(rec);
ok(H2.state.resume && H2.state.slots.length === 4, 'saved lobby opened with the 4 saved slots');
ok(H2.state.slots[rec.me].peer === H2.id, 'host took his saved slot ' + rec.me);
let j2 = false, z2 = false; J2.join(code2).then(() => { j2 = true; }); Z2.join(code2).then(() => { z2 = true; });
ok(await until(() => j2 && z2), 'joiners in the saved lobby');
const ayseSlot = H2.state.slots.findIndex(s => s.name === 'Ayse');
ok(H2.state.slots[ayseSlot].peer === J2.id, '"ayse" matched to slot "Ayse" by name (case-insensitive)');
ok(H2.state.waiting.some(w => w.peer === Z2.id) && !H2.state.slots.some(s => s.peer === Z2.id), 'unmatched "Zeynep" waits for a slot');
const mehmetSlot = H2.state.slots.findIndex(s => s.name === 'Mehmet');
Z2.claimSlot(mehmetSlot);
ok(await until(() => H2.state.slots[mehmetSlot].peer === Z2.id && Z2.state.slots[mehmetSlot].peer === Z2.id), 'Zeynep claimed the free slot "Mehmet"');
await runFor(300);
ok(H2.freeSlot(mehmetSlot) && H2.state.waiting.some(w => w.peer === Z2.id), 'host freed the slot again');
ok(H2.setSlotMode(mehmetSlot, 'ai') && H2.state.slots[mehmetSlot].mode === 'ai', 'host: "Yapay Zekâ devralsın" for the absent player');
J2.setReady(true);
await runFor(2000);
ok(H2.canStart().ok, 'host can start the continued match');
await H2.start();
ok(await until(() => E2[0].start && E2[1].start), 'host and matched joiner started (blob downloaded + hash-checked)');
await runFor(1000);
ok(E2[2].closed === 'notInMatch', 'the stranger without a slot is told the match started without him (' + E2[2].closed + ')');
const S2 = [H2, J2];
const g2 = S2.map((s, i) => {
  const c = E2[i].start.cfg;
  const g = Game.deserialize(s.resumeData, { me: c.me });
  g.applyResume(c.resume);
  return g;
});
ok(g2[0].me === rec.me && g2[1].me === ayseSlot && g2[0].me !== g2[1].me, 'each client got its own me (' + g2.map(g => g.me).join(', ') + ')');
ok(g2.every(g => g.tick === rec.tick), 'loaded at the saved tick ' + rec.tick);
ok(g2.every(g => g.players[mehmetSlot].isAI && g.ais.some(a => a.pid === mehmetSlot)), 'absent player taken over by an AI on both');
ok(g2[0].hash() === g2[1].hash(), 'equal hash right after load: ' + g2[0].hash());
const r2 = [mulberry(5), mulberry(6)];
const script2 = makeScript(S2, g2, r2);
let playing2 = true;
const frame2 = dt => { for (let i = 0; i < 2; i++) { if (S2[i].phase !== 'game') continue; if (playing2) script2(i); S2[i].advance(g2[i], dt); } };
await runFor(45000, frame2);
playing2 = false;
ok(await syncTo(S2, g2), 'continued clients at the same tick');
ok(g2[0].tick > rec.tick + 40 * 30, 'continued match advanced (' + rec.tick + ' -> ' + g2[0].tick + ')');
ok(g2[0].hash() === g2[1].hash(), 'equal game.hash() in the continued match: ' + g2[0].hash() + ' / ' + g2[1].hash());
ok(E2.slice(0, 2).every(e => !e.desync && !e.closed), 'no desync / close in the continued match');
console.log('  (DROP_SILENT_MS = ' + DROP_SILENT_MS + ')');
console.log(failed ? `\n${failed} check(s) FAILED` : '\nAll outage / continue checks passed.');
process.exit(failed ? 1 : 0);
