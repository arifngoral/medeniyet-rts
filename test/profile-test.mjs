// Aevum - profile + match history pure logic (src/profile.js) with an in-memory localStorage.
// Run: node test/profile-test.mjs
import * as P from '../src/profile.js';
import { Game } from '../src/sim/game.js';

let failed = 0;
const ok = (c, msg) => { if (c) console.log('  ok   ' + msg); else { failed++; console.log('  FAIL ' + msg); } return !!c; };
const memLS = (init = {}) => { const m = new Map(Object.entries(init)); return { getItem: k => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), removeItem: k => m.delete(k), m }; };
// deterministic fake crypto
let seed = 1;
const fakeCrypto = { getRandomValues(a) { for (let i = 0; i < a.length; i++) { seed = (seed * 1103515245 + 12345) >>> 0; a[i] = seed >>> 24; } return a; } };
const U = (c) => c.repeat(32);   // a valid uid made of one hex digit

console.log('Names');
ok(P.checkName('  Kerem  ').ok && P.checkName('  Kerem  ').name === 'Kerem', 'trims');
ok(P.checkName('A  b').name === 'A b', 'collapses inner whitespace');
ok(!P.checkName('A').ok && !P.checkName(' ').ok && !P.checkName('').ok, 'too short rejected');
ok(P.checkName('x'.repeat(20)).ok && !P.checkName('x'.repeat(21)).ok, '20 ok, 21 rejected');
ok(!P.checkName('ab\u0001c').ok, 'control characters rejected');
ok(!P.checkName(null).ok && !P.checkName(42).ok, 'non-strings rejected');
ok(P.checkName('Çağrı Şükrü').ok, 'Turkish letters ok');

console.log('Profile + migration');
const ls = memLS({ 'aevum.mpName': 'EskiAd' });
ok(P.loadProfile(ls) === null, 'no profile at first');
ok(P.defaultName(ls) === 'EskiAd', 'old mpName is the default name');
ok(P.defaultName(memLS({ 'aevum.mpName': 'x' })) === '', 'unusable old mpName -> empty default');
ok(P.defaultName(memLS({ 'aevum.mpName': 'y'.repeat(30) })) === 'y'.repeat(20), 'long old mpName clipped to 20');
const prof = P.createProfile(ls, P.defaultName(ls), { cryptoObj: fakeCrypto, now: 1000 });
ok(P.isUid(prof.uid) && prof.uid.length === 32, '128-bit hex uid: ' + prof.uid);
ok(JSON.parse(ls.getItem('aevum.profile')).uid === prof.uid && JSON.parse(ls.getItem('aevum.profile')).v === 1, 'stored as aevum.profile {v:1,...}');
const re = P.loadProfile(ls);
ok(re && re.uid === prof.uid && re.name === 'EskiAd' && re.created === 1000, 'loads back');
ok(P.renameProfile(ls, 'YeniAd').ok && P.loadProfile(ls).name === 'YeniAd' && ls.getItem('aevum.mpName') === 'YeniAd', 'rename updates profile and mpName');
ok(!P.renameProfile(ls, 'Z').ok && P.loadProfile(ls).name === 'YeniAd', 'invalid rename keeps the old name');
ok(P.loadProfile(ls).uid === prof.uid, 'uid permanent across renames');
ls.setItem('aevum.profile', '{"v":1,"uid":"XYZ","name":"ab","created":1}');
ok(P.loadProfile(ls) === null, 'corrupt profile ignored');
ls.setItem('aevum.profile', 'not json');
ok(P.loadProfile(ls) === null, 'unparsable profile ignored');
const u2 = P.newUid(fakeCrypto);
ok(u2 !== prof.uid && P.isUid(u2), 'new uids differ');
ok(P.isUid(P.newUid()) , 'real crypto.getRandomValues works in node');
ok(!P.isUid(U('A')) && !P.isUid(U('a') + '0') && !P.isUid(123) && P.isUid(U('a')), 'isUid: lowercase hex, length 32 only');

console.log('Records from a real game');
const g = new Game({ mapSize: 96, seed: 5, enemies: 1, difficulty: 'hard', mapType: 'plains' });
for (let i = 0; i < 300; i++) g.update(1 / 30);
const me = P.loadProfile(memLS({ 'aevum.profile': JSON.stringify(prof) })) || prof;
let r = P.buildRecord(g, { mode: 'sp', id: P.spRecordId('00112233aabbccdd'), uids: [], myUid: me.uid, now: 5000 });
ok(r.result === 'abandoned' && r.mode === 'sp' && r.difficulty === 'hard' && r.mapType === 'plains' && r.mapSize === 96, 'sp record fields (abandoned while running)');
ok(r.gameTime === 10 && r.players.length === 2 && r.players[0].uid === me.uid && r.players[1].ai && r.players[1].uid === null, 'gameTime + players (me with uid, AI without)');
ok(typeof r.stats.gathered.food === 'number' && 'unitsTrained' in r.stats && 'techs' in r.stats, 'stats copied');
ok(P.recordError(r) === null, 'built record passes import validation');
ok(r.players[0].name === 'Oyuncu 1' && P.buildRecord(g, { mode: 'sp', id: 'x', uids: [], myUid: me.uid, myName: 'Kerem' }).players[0].name === 'Kerem', 'sp: my entry uses the profile name');
const hashBefore = g.hash();
P.buildRecord(g, { mode: 'sp', id: 'x', uids: [], myUid: me.uid });
ok(g.hash() === hashBefore && !JSON.stringify(g.serialize()).includes(me.uid), 'building a record does not touch the sim (hash same, uid not in serialize)');
g.over = { won: true, winnerTeam: g.players[0].team };
ok(P.buildRecord(g, { mode: 'sp', id: 'x', uids: [], myUid: me.uid }).result === 'won', 'won when my team won');
g.over = { won: false, winnerTeam: -1 };
ok(P.buildRecord(g, { mode: 'sp', id: 'x', uids: [], myUid: me.uid }).result === 'lost', 'lost on winnerTeam -1');
g.over = null; g.players[0].defeated = true;
ok(P.buildRecord(g, { mode: 'sp', id: 'x', uids: [], myUid: me.uid }).result === 'lost', 'defeated but match running -> lost');
ok(P.mpRecordId('AB-CD', U('a')) === 'mp-ABCD-' + U('a'), 'mp record id: match code + uid');

console.log('Aggregation + head-to-head');
const A = U('a'), B = U('b'), C = U('c');
const mk = (id, result, opts = {}) => ({
  v: 1, id, uid: A, me: 0, endedAt: opts.t || 0, mode: opts.mode || 'mp', mapType: opts.map || 'river', mapSize: 128, difficulty: null, gameTime: opts.time || 600, result, myAge: opts.age || 1,
  stats: { gathered: { food: 100, wood: 50, stone: 0, gold: 10 }, unitsTrained: 5, unitsLost: 1, kills: 2, buildingsBuilt: 3, buildingsLost: 0, razed: 1, techs: 4 },
  players: opts.players || [{ name: 'Ben', uid: A, team: 1, ai: false, difficulty: null, won: result === 'won' }, { name: opts.bName || 'Arkadaş', uid: B, team: opts.bTeam || 2, ai: false, difficulty: null, won: result !== 'won' }],
});
const hist = [
  mk('m1', 'won', { t: 1, bName: 'Bora' }), mk('m2', 'lost', { t: 2, bName: 'Bora' }), mk('m3', 'won', { t: 3, bName: 'BoraYeni', map: 'islands' }),
  mk('m4', 'abandoned', { t: 4, bName: 'BoraYeni', map: 'islands' }),
  mk('m5', 'won', { t: 5, bName: 'BoraYeni', bTeam: 1, map: 'islands', players: [{ name: 'Ben', uid: A, team: 1, ai: false, won: true }, { name: 'BoraYeni', uid: B, team: 1, ai: false, won: true }, { name: 'YZ', uid: null, team: 2, ai: true, difficulty: 'hard', won: false }] }),
  mk('s1', 'lost', { t: 6, mode: 'sp', time: 300, age: 3, players: [{ name: 'Ben', uid: A, team: 1, ai: false, won: false }, { name: 'YZ', uid: null, team: 2, ai: true, difficulty: 'easy', won: true }] }),
  // a second tab of my own profile / a record whose other human has my uid: never an opponent
  mk('m6', 'won', { t: 7, map: 'islands', players: [{ name: 'Ben', uid: A, team: 1, ai: false, won: true }, { name: 'Ben2', uid: A, team: 2, ai: false, won: false }, { name: 'Cem', uid: C, team: 2, ai: false, won: false }, { name: 'Eski', uid: null, team: 2, ai: false, won: false }] }),
];
const t = P.summarize(hist);
ok(t.games === 7 && t.wins === 4 && t.losses === 2 && t.abandoned === 1, 'games/wins/losses/abandoned 7/4/2/1');
ok(Math.abs(t.winRate - 4 / 6) < 1e-9, 'win rate counts only decided games');
ok(t.totalTime === 6 * 600 + 300, 'total game time summed');
ok(t.stats.gathered.food === 700 && t.stats.kills === 14 && t.stats.techs === 28, 'stats summed');
ok(t.topMap === 'islands' && t.mapCounts.islands === 4 && t.mapCounts.river === 3, 'most played map type');
ok(t.maxAge === 3 && t.sp === 1 && t.mp === 6, 'max age, sp/mp counts');
ok(P.summarize([]).games === 0 && P.summarize([]).winRate === 0 && P.summarize([]).topMap === null, 'empty history');
const hh = P.headToHead(hist, A);
const hb = hh.find(x => x.uid === B), hc = hh.find(x => x.uid === C);
ok(hh.length === 2 && hb && hc, 'one entry per other human uid (no AI, no null uid, not my own uid)');
ok(hb.name === 'BoraYeni', 'latest name shown for the opponent');
ok(hb.vs.games === 4 && hb.vs.wins === 2 && hb.vs.losses === 1 && hb.vs.abandoned === 1, 'vs record 2-1 (+1 abandoned)');
ok(hb.with.games === 1 && hb.with.wins === 1, 'same-team games counted separately');
ok(hc.vs.games === 1 && hc.vs.wins === 1 && hh[0].uid === B, 'Cem 1-0; sorted by games');

console.log('Merge / de-dup / cap');
const resumedOld = mk('mp-ABCDE-' + A, 'abandoned', { t: 10 }), resumedEnd = mk('mp-ABCDE-' + A, 'won', { t: 20 });
const mg = P.mergeHistory([resumedOld, ...hist], [resumedEnd, hist[0], hist[1]]);
ok(mg.length === hist.length + 1, 'duplicates by id collapse (' + mg.length + ')');
ok(mg.find(x => x.id === resumedOld.id).result === 'won', 'the newer record of a resumed match wins');
ok(mg[0].endedAt >= mg[1].endedAt && mg[1].endedAt >= mg[mg.length - 1].endedAt, 'newest first');
const many = []; for (let i = 0; i < 520; i++) many.push(mk('x' + i, 'won', { t: i }));
const capped = P.mergeHistory([], many);
ok(capped.length === 500 && capped[0].id === 'x519' && capped[499].id === 'x20', 'capped to the newest 500');
ok(P.overCap(many).length === 20 && P.overCap(many).includes('x0') && !P.overCap(many).includes('x519'), 'overCap lists the oldest extra ids');

console.log('Export / import validation');
const exp = P.exportData(prof, hist, 99);
const v = P.validateImport(JSON.stringify(exp));
ok(v.ok && v.profile.uid === prof.uid && v.history.length === hist.length, 'export round-trips');
ok(JSON.stringify(v.history.map(x => x.id).sort()) === JSON.stringify(hist.map(x => x.id).sort()), 'all ids kept');
const bad = (mut, why) => { const o = JSON.parse(JSON.stringify(exp)); mut(o); const r = P.validateImport(o); ok(!r.ok && r.error, 'rejects ' + why + ' (' + r.error + ')'); };
ok(!P.validateImport('{nope').ok, 'rejects broken JSON');
ok(!P.validateImport('[]').ok && !P.validateImport('null').ok, 'rejects non-objects');
bad(o => { o.format = 'other'; }, 'wrong format');
bad(o => { o.v = 2; }, 'wrong version');
bad(o => { o.profile.uid = 'ABC'; }, 'bad profile uid');
bad(o => { o.profile.name = 'x'; }, 'bad profile name');
bad(o => { o.profile.name = '<img src=x onerror=alert(1)>' + 'x'.repeat(10); }, 'over-long profile name');
bad(o => { o.history = {}; }, 'history not an array');
bad(o => { o.history[0].result = 'draw'; }, 'unknown result');
bad(o => { o.history[0].mode = 'coop'; }, 'unknown mode');
bad(o => { o.history[0].id = 'a b<>'; }, 'bad id characters');
bad(o => { o.history[0].mapSize = 200; }, 'bad map size');
bad(o => { o.history[0].mapType = 'River<script>'; }, 'bad map type');
bad(o => { o.history[0].gameTime = -1; }, 'negative time');
bad(o => { o.history[0].stats.kills = 'many'; }, 'non-numeric stat');
bad(o => { delete o.history[0].stats.gathered; }, 'missing gathered');
bad(o => { o.history[0].players[1].uid = 'zz'; }, 'bad player uid');
bad(o => { o.history[0].players[1].name = 'x'.repeat(100); }, 'over-long player name');
bad(o => { o.history[0].players = []; }, 'empty players');
bad(o => { o.history[0].players[0].team = 99; }, 'bad team');
const extra = JSON.parse(JSON.stringify(exp)); extra.history[0].evil = '<b>'; extra.history[0].players[0].x = 1;
const ve = P.validateImport(extra);
ok(ve.ok && !('evil' in ve.history[0]) && !('x' in ve.history[0].players[0]), 'unknown fields are dropped');
const html = JSON.parse(JSON.stringify(exp)); html.history[0].players[1].name = '<img onerror=x>';
ok(P.validateImport(html).ok, 'names with markup are allowed as data (UI renders them as text)');

console.log('Storage unavailable / full');
{
  const throwing = { getItem() { throw new Error('SecurityError'); }, setItem() { throw new Error('QuotaExceededError'); }, removeItem() {} };
  const tp = P.createProfile(throwing, 'Kerem', { cryptoObj: fakeCrypto, now: 7 });
  ok(P.validProfile(tp) && tp.saved === false && P.loadProfile(throwing) === null, 'createProfile still returns a valid profile, saved=false when storage throws');
  ok(!Object.keys(tp).includes('saved') && !JSON.stringify(tp).includes('saved'), 'saved flag is not part of the stored/exported profile');
  ok(P.createProfile(memLS(), 'Kerem', { cryptoObj: fakeCrypto }).saved === true, 'saved=true on working storage');
  ok(P.createProfile(null, 'Kerem', { cryptoObj: fakeCrypto }).saved === false, 'no storage at all: saved=false');
  const rr = P.renameProfile(throwing, 'Kerem2', tp);
  ok(rr.ok && !rr.saved && rr.profile.uid === tp.uid && rr.profile.name === 'Kerem2', 'rename of the in-memory session profile works without storage');
  ok(!P.renameProfile(throwing, 'Kerem2').ok, 'no storage and no session profile: rename fails cleanly');
  const ls2 = memLS(); const sp = P.createProfile(ls2, 'Eski', { cryptoObj: fakeCrypto });
  const cur = { v: 1, uid: U('e'), name: 'Yeni', created: 1 };
  ok(P.renameProfile(ls2, 'Yeni2', cur).profile.uid === U('e') && sp.uid !== U('e'), 'session profile wins over a stale stored one');
}

console.log('Import hardening');
{
  const NOW = 1.7e12;
  const recAt = (id, t) => Object.assign(mk(id, 'won'), { endedAt: t });
  const file = (h) => ({ format: 'aevum-profile', v: 1, exportedAt: NOW, profile: prof, history: h });
  ok(P.validateImport(file([recAt('ok1', NOW - 1000), recAt('ok2', NOW + 3600e3)]), NOW).ok, 'dates up to now (+ small margin) accepted');
  ok(!P.validateImport(file([recAt('fut', NOW + 3 * 86400e3)]), NOW).ok, 'future-dated record rejected (could push real matches out of the 500 cap)');
  ok(!P.validateImport(file([recAt('fut2', 9e13)])).ok, 'far-future date rejected with the real clock');
  for (const m of ['constructor', 'tostring', 'valueof', 'proto', 'mars']) ok(!P.validateImport(file([Object.assign(mk('mt' + m, 'won'), { mapType: m })]), NOW).ok, 'unknown map type "' + m + '" rejected');
  for (const m of P.MAP_TYPES) ok(P.recordError(Object.assign(mk('mt', 'won'), { mapType: m }), NOW) === null, 'map type ' + m + ' accepted');
  const weird = P.summarize([Object.assign(mk('w1', 'won'), { mapType: 'constructor' }), Object.assign(mk('w2', 'won'), { mapType: 'constructor' }), mk('w3', 'won')]);
  ok(weird.mapCounts.constructor === 2 && weird.topMap === 'constructor', 'summarize counts property-like map names as plain keys');
  // the friend's export of the same match (their view, their uid)
  const mine = mk('mp-ABC-' + A, 'won', { t: 5 });
  const friend = Object.assign(mk('mp-ABC-' + B, 'lost', { t: 5 }), { uid: B, me: 1 });
  const legacy = Object.assign(mk('sp-legacy', 'won', { t: 6 }), { uid: null });
  const own = P.ownRecords([friend, legacy, mine], A);
  ok(own.skipped === 1 && own.keep.length === 2 && !own.keep.includes(friend), 'ownRecords drops another uid\'s records, keeps mine and owner-less ones');
  const s2 = P.summarize(P.mergeHistory([mine], own.keep));
  ok(s2.games === 2 && s2.wins === 2 && s2.losses === 0, 'merged totals do not count the friend\'s view of the same match');
}

console.log('Opponent left the match');
{
  const g2 = new Game({ mapSize: 96, seed: 8, enemies: 1, difficulty: 'easy' });
  for (let i = 0; i < 30; i++) g2.update(1 / 30);
  const ctx = { mode: 'mp', id: 'mp-X-' + A, uids: [A, B], myUid: A };
  ok(P.buildRecord(g2, ctx).result === 'abandoned', 'running, opponent still there: abandoned');
  g2.players[1].left = true;
  const rl = P.buildRecord(g2, ctx);
  ok(rl.result === 'won' && rl.players[0].won === true && rl.players[1].won === false, 'every opponent left / defeated (one left): won');
  g2.players[0].left = false; g2.players[1].left = false; g2.players[1].defeated = true;
  ok(P.buildRecord(g2, ctx).result === 'abandoned', 'opponent only defeated without game over: still abandoned (the sim decides)');
}

console.log(failed ? `\n${failed} check(s) FAILED` : '\nALL OK');
process.exit(failed ? 1 : 0);
