// Headless sim smoke test: node test/sim-smoke.mjs [minutes]
import { Game } from '../src/sim/game.js';
import { AGES, RES, UNITS, BUILDINGS, TECHS, PLAYER_COLORS } from '../src/data.js';

const MIN = +(process.argv[2] || 25);
const fails = [], warns = [];
const ok = (c, m) => { if (!c) fails.push(m); return !!c; };
const warn = (c, m) => { if (!c) warns.push(m); };

// ---- data checks
ok(AGES.length === 5 && RES.length === 4 && PLAYER_COLORS.length >= 8, 'data arrays');
for (const id of ['villager', 'spearman', 'swordsman', 'archer', 'lightcav', 'heavyinf', 'crossbow', 'knight', 'ram', 'catapult', 'tradecart', 'musketeer', 'cannon', 'cuirassier', 'rifleman', 'artillery']) ok(UNITS[id], 'unit ' + id);
for (const id of ['towncenter', 'house', 'farm', 'barracks', 'archery', 'stable', 'blacksmith', 'market', 'storage', 'tower', 'wall', 'gate', 'university', 'castle', 'siege', 'factory']) ok(BUILDINGS[id], 'building ' + id);
for (const b of Object.values(BUILDINGS)) { for (const u of b.trains || []) ok(UNITS[u], b.id + ' trains unknown ' + u); for (const t of b.researches || []) ok(TECHS[t], b.id + ' researches unknown ' + t); }

let g = new Game({ mapSize: 256, enemies: 1, difficulty: 'hard', startRes: 'normal', startAge: 0, sandbox: false, seed: 7 });   // (the smallest size since 2026-11-13)
for (const m of ['update', 'getEntity', 'canAfford', 'isUnlocked', 'canPlace', 'placeBuilding', 'cmdMove', 'cmdAttack', 'cmdGather', 'cmdBuild', 'cmdStop', 'train', 'research', 'ageUp', 'canAgeUp', 'cancelQueue', 'setRally', 'trade', 'tradeRate', 'deleteEntity', 'isEntityVisible', 'resourceNear', 'unitsOf', 'buildingsOf', 'serialize']) ok(typeof g[m] === 'function', 'method ' + m);
ok(typeof Game.deserialize === 'function', 'Game.deserialize');
for (const f of ['cfg', 'time', 'map', 'players', 'entities', 'projectiles', 'fog', 'fogVersion', 'events', 'quests', 'ais']) ok(g[f] !== undefined, 'field ' + f);
ok(g.entities instanceof Map, 'entities Map');
ok(g.map.heights.length === 257 * 257 && g.map.tiles.length === 256 * 256 && g.map.blocked.length === 256 * 256, 'map arrays');
ok(typeof g.map.heightAt === 'function' && typeof g.map.isWalkable === 'function', 'map fns');
ok(g.players.length === 2 && g.ais.length === 1 && Array.isArray(g.quests.list), 'players/ai/quests');

const ev = {};
let aiAttackOnP0 = 0;
function hook(game) {
  for (const n of ['spawn', 'remove', 'death', 'attack', 'hit', 'gatherTick', 'deposit', 'treeFelled', 'buildStart', 'buildComplete', 'trained', 'researched', 'ageUpStart', 'ageUp', 'questDone', 'notify', 'underAttack', 'farmStage', 'gameOver'])
    game.events.on(n, (p) => { ev[n] = (ev[n] || 0) + 1; if (n === 'attack' && p.attacker && p.target && p.attacker.owner === 1 && p.target.owner === 0) aiAttackOnP0++; });
}
hook(g);

const res0 = { ...g.players[0].res };
const fogV0 = g.fogVersion;
const farmStages = new Set();
const jobs = new Map(); // villager id -> job
let attackSent = false, roundTripDone = false;

function findSpot(game, type, r0 = 4, r1 = 22) {
  const p = game.players[0], cx = Math.floor(p.startX), cz = Math.floor(p.startZ);
  for (let r = r0; r <= r1; r++) for (let dz = -r; dz <= r; dz++) for (let dx = -r; dx <= r; dx++) {
    if (Math.max(Math.abs(dx), Math.abs(dz)) !== r) continue;
    if (game.canPlace(type, cx + dx, cz + dz, 0)) return { tx: cx + dx, tz: cz + dz };
  }
  return null;
}
function nearestRes(game, types, x, z) {
  let best = null, bd = 1e9;
  for (const e of game.entities.values()) { if (e.kind !== 'resource' || e.dead || !types.includes(e.type) || e.amount <= 0) continue; const d = (e.x - x) ** 2 + (e.z - z) ** 2; if (d < bd) { bd = d; best = e; } }
  return best;
}
function build(game, type) {
  if (!game.isUnlocked(0, 'building', type) || !game.canAfford(0, BUILDINGS[type].cost)) return null;
  const s = findSpot(game, type); if (!s) return null;
  const vs = game.unitsOf(0).filter(u => u.type === 'villager');
  const b = vs.slice(0, 2).map(u => u.id);
  const id = game.placeBuilding(0, type, s.tx, s.tz, b);
  return id;
}
function human(game) {
  const p = game.players[0];
  const vs = game.unitsOf(0).filter(u => u.type === 'villager');
  const bs = game.buildingsOf(0);
  const cnt = (t) => bs.filter(b => b.type === t).length;
  const tc = bs.find(b => b.type === 'towncenter' && b.done);
  // unfinished buildings: make sure someone builds
  for (const b of bs) if (!b.done && !vs.some(u => u.state === 'build' && u.targetId === b.id) && vs.length) game.cmdBuild([vs[(b.id) % vs.length].id], b.id);
  // idle villagers -> jobs, rotating
  const order = ['food', 'wood', 'food', 'gold', 'wood', 'stone', 'food', 'wood'];
  vs.forEach((u, i) => {
    if (u.state !== 'idle') return;
    const want = order[i % order.length];
    let t = null;
    if (want === 'food') { const farm = bs.find(b => b.type === 'farm' && b.done && vs.filter(v => v.targetId === b.id).length < 8) || bs.find(b => b.type === 'pasture' && b.done && vs.filter(v => v.targetId === b.id).length < 3); t = farm || nearestRes(game, ['berries', 'deer'], u.x, u.z); }
    else t = nearestRes(game, [want === 'wood' ? 'tree' : want], u.x, u.z);
    if (t) game.cmdGather([u.id], t.id);
  });
  if (tc && tc.queue.length < 2 && vs.length < 26) game.train(tc.id, 'villager');
  if (p.pop + 4 >= p.popCap && p.popCap < 200 && bs.filter(b => b.type === 'house' && !b.done).length === 0) build(game, 'house');
  if (cnt('farm') < 2) build(game, 'farm');   // (8 farmers per farm; farms come with the Bronze Age since 2026-11-14)
  if (cnt('pasture') < 1) build(game, 'pasture');   // (the first age's food building)
  if (cnt('barracks') < 1 && cnt('farm') + cnt('pasture') >= 1) build(game, 'barracks');
  if (cnt('storage') < 1 && cnt('barracks') >= 1) build(game, 'storage');
  for (const t of ['archery', 'stable', 'blacksmith', 'market', 'tower', 'university', 'siege', 'castle', 'factory']) if (cnt(t) < 1 && cnt('barracks') >= 1) build(game, t);
  const army = game.unitsOf(0).filter(u => UNITS[u.type].cls !== 'civil');
  for (const b of bs) {
    if (!b.done || b.type === 'towncenter') continue;
    const d = BUILDINGS[b.type];
    if (d.trains && d.trains.length && b.queue.length < 2 && army.length < 40) { const opts = d.trains.filter(t => game.isUnlocked(0, 'unit', t) && UNITS[t].cls !== 'civil'); if (opts.length) game.train(b.id, opts[opts.length - 1]); }
    if (d.researches && b.queue.length < 1) for (const t of d.researches) if (game.isUnlocked(0, 'tech', t) && !p.techs.has(t) && game.research(b.id, t)) break;
  }
  if (tc && game.canAgeUp(0).ok && !tc.queue.some(q => q.kind === 'age')) game.ageUp(tc.id);
  for (const b of bs) if (b.type === 'farm' && b.farm) { if (b.farm.plots) for (const q of b.farm.plots) farmStages.add(q.s); else farmStages.add(b.farm.stage); }
  // attack at minute 14+ with 12+ soldiers
  if (game.time > 14 * 60 && army.length >= 12) {
    const idle = army.filter(u => u.state === 'idle');
    const tgt = game.buildingsOf(1)[0] || game.unitsOf(1)[0];
    if (tgt && idle.length) { if (game.cmdAttack(idle.map(u => u.id), tgt.id)) attackSent = true; }
  }
}

const dt = 1 / 30, steps = Math.round(MIN * 60 / dt);
let tTotal = 0, tMax = 0, maxUnits = 0, slow = 0;
const log = [];
try {
  for (let i = 0; i < steps; i++) {
    if (i % 30 === 0 && !g.over) human(g);
    const t0 = performance.now();
    g.update(dt);
    const el = performance.now() - t0; tTotal += el; if (el > tMax) tMax = el; if (el > 8) slow++;
    if (i % 300 === 0) { let n = 0; for (const e of g.entities.values()) if (e.kind === 'unit') n++; if (n > maxUnits) maxUnits = n; for (const e of g.entities.values()) { if (!Number.isFinite(e.x) || !Number.isFinite(e.z) || !Number.isFinite(e.hp)) { fails.push('NaN entity ' + e.type + ' at t=' + g.time.toFixed(1)); i = steps; break; } } }
    if (i % (30 * 150) === 0) {
      const s = (pl) => `age${pl.age} pop${pl.pop}/${pl.popCap} f${pl.res.food | 0} w${pl.res.wood | 0} s${pl.res.stone | 0} g${pl.res.gold | 0} vil${g.unitsOf(pl.id).filter(u => u.type === 'villager').length} army${g.unitsOf(pl.id).filter(u => UNITS[u.type].cls !== 'civil').length} bld${g.buildingsOf(pl.id).length}`;
      log.push(`t=${(g.time / 60).toFixed(1)}m | P0 ${s(g.players[0])} | AI ${s(g.players[1])} | over=${JSON.stringify(g.over)}`);
    }
    if (!roundTripDone && g.time >= 8 * 60) {
      roundTripDone = true;
      const json = JSON.stringify(g.serialize());
      const g2 = Game.deserialize(JSON.parse(json));
      ok(Math.abs(g2.time - g.time) < 1e-6, 'deserialize time');
      ok(g2.entities.size === g.entities.size, `deserialize entity count ${g2.entities.size} vs ${g.entities.size}`);
      ok(g2.players[0].techs instanceof Set, 'deserialize techs Set');
      ok(g2.players[1].age === g.players[1].age && g2.players[0].res.food === g.players[0].res.food, 'deserialize players');
      ok(g2.fog.length === g.fog.length && g2.map.heights instanceof Float32Array && g2.map.tiles instanceof Uint8Array, 'deserialize map/fog typed arrays');
      ok(g2.ais.length === 1 && g2.quests.list.length === g.quests.list.length, 'deserialize ai/quests');
      log.push(`-- save/load at 8m: ${(json.length / 1024) | 0} KB, continuing on the deserialized game`);
      g = g2; hook(g);
    }
  }
} catch (e) { fails.push('EXCEPTION at t=' + g.time.toFixed(2) + ': ' + (e && e.stack || e)); }

const p0 = g.players[0], p1 = g.players[1];
ok(roundTripDone, 'round trip executed');
ok(RES.some(r => p0.stats.gathered[r] > 0) && RES.every(r => p0.stats.gathered[r] > 0), 'P0 gathered all 4 resources: ' + JSON.stringify(p0.stats.gathered));
ok(ev.buildComplete > 3, 'buildings complete');
ok(farmStages.size >= 5, 'farm stages cycle, saw ' + [...farmStages].join(','));
ok(p0.stats.unitsTrained > 10, 'P0 units trained ' + p0.stats.unitsTrained);
ok(p0.age >= 1, 'P0 aged up, age ' + p0.age);
ok(p1.stats.unitsTrained > 10, 'AI trained ' + p1.stats.unitsTrained);
ok(p1.stats.buildingsBuilt >= 4, 'AI built ' + p1.stats.buildingsBuilt);
ok(p1.age >= 1 || g.over, 'AI aged up, age ' + p1.age);
ok(aiAttackOnP0 > 0, 'AI attacked player 0');
ok(g.fogVersion > fogV0, 'fog changes');
ok(ev.deposit > 0 && ev.gatherTick > 0 && ev.trained > 0 && ev.spawn > 0, 'core events fired');
warn(attackSent, 'P0 never sent an attack');
warn(ev.questDone > 0, 'no quest completed');
warn(ev.researched > 0, 'no tech researched');
warn(ev.treeFelled > 0, 'no tree felled');
warn(ev.underAttack > 0, 'no underAttack event');
const avg = tTotal / steps;
ok(avg < 3, 'avg ms/step ' + avg.toFixed(3));

console.log(log.join('\n'));
console.log('events:', JSON.stringify(ev));
console.log('P0 stats:', JSON.stringify(p0.stats), 'techs', p0.techs.size);
console.log('AI stats:', JSON.stringify(p1.stats), 'techs', p1.techs.size, 'aiAttacksOnP0', aiAttackOnP0);
console.log('quests done:', g.quests.list.filter(q => q.done).length + '/' + g.quests.list.length);
console.log(`perf: avg ${avg.toFixed(3)} ms/step, max ${tMax.toFixed(1)} ms, steps>8ms ${slow}, peak units ${maxUnits}, sim ${(g.time / 60).toFixed(1)} min in ${(tTotal / 1000).toFixed(1)} s`);
if (warns.length) console.log('WARN:\n - ' + warns.join('\n - '));
if (fails.length) { console.log('FAIL:\n - ' + fails.join('\n - ')); process.exit(1); }
console.log('ALL OK');
