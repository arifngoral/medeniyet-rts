// Pasture + railway headless test: node test/land-test.mjs
import { Game } from '../src/sim/game.js';
import { BUILDINGS, UNITS, TECHS } from '../src/data.js';

const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); else console.log('  ok ', m); return !!c; };
const step = (g, sec) => { for (let i = 0; i < sec * 10; i++) g.update(0.1); };

ok(BUILDINGS.pasture && BUILDINGS.station && BUILDINGS.rail && UNITS.train && TECHS.breeding && TECHS.steelrails, 'defs exist');

function spotNear(g, type, cx, cz, r0 = 4, r1 = 30) {
  for (let r = r0; r <= r1; r++) for (let dz = -r; dz <= r; dz++) for (let dx = -r; dx <= r; dx++) {
    if (Math.max(Math.abs(dx), Math.abs(dz)) !== r) continue;
    if (g.canPlace(type, cx + dx, cz + dz, 0)) return [cx + dx, cz + dz];
  }
  return null;
}

// ---------- pasture ----------
function pastureRun(workers) {
  const g = new Game({ mapSize: 96, enemies: 1, difficulty: 'easy', seed: 21 });
  g.ais.length = 0; // keep the test about player 0
  const p = g.players[0]; p.res.wood = 2000; p.res.food = 2000;
  const s = spotNear(g, 'pasture', p.startX + 4, p.startZ + 4);
  const vs = [];
  for (let i = 0; i < workers; i++) { const f = g._freeNear(s[0] + 1.5 + (i % 3) * 0.6, s[1] + 4.5 + (i / 3 | 0) * 0.6, 0); vs.push(g._addUnit('villager', 0, f.x, f.z)); }
  const id = g.placeBuilding(0, 'pasture', s[0], s[1], vs.map(v => v.id));
  const b = g.getEntity(id);
  step(g, 60);
  if (!b.done) return { done: false };
  g.cmdGather(vs.map(v => v.id), id);
  step(g, 8);
  const f0 = p.res.food;
  step(g, 60);
  const inside = vs.every(v => v.x >= b.tx - 0.05 && v.x <= b.tx + b.size + 0.05 && v.z >= b.tz - 0.05 && v.z <= b.tz + b.size + 0.05);
  return { done: true, food: p.res.food - f0, inside, sheep: b.pasture.sheep, anim: vs.map(v => v.anim) };
}
for (const n of [1, 2, 6]) {
  const r = pastureRun(n);
  console.log(`pasture ${n} workers:`, JSON.stringify(r));
  ok(r.done, `pasture built (${n})`);
  ok(r.food > 0, `pasture yields food with ${n} workers (${r.food}/min)`);
  ok(r.inside, `${n} workers stand inside the pen`);
  ok(r.anim && r.anim.every(a => a === 'farm'), `${n} workers animate 'farm'`);
}

// ---------- railway ----------
{
  const g = new Game({ mapSize: 128, enemies: 1, difficulty: 'easy', seed: 5, sandbox: true });
  g.ais.length = 0;
  const p = g.players[0]; p.age = 4;
  const ev = { arrive: 0, dep: 0 };
  g.events.on('trainArrive', () => ev.arrive++);
  g.events.on('deposit', (d) => { if (d.unit && d.unit.type === 'train') ev.dep++; });
  // find a row where two stations 12 tiles apart and a straight rail between them fit
  let cfg = null; const N = g.map.size;
  outer: for (let r = 0; r < 50; r++) for (let dz = -r; dz <= r; dz++) for (let dx = -r; dx <= r; dx++) {
    if (Math.max(Math.abs(dx), Math.abs(dz)) !== r) continue;
    const ax = (p.startX | 0) + dx, az = (p.startZ | 0) + dz, bx = ax + 15;
    if (bx + 4 >= N) continue;
    if (!g.canPlace('station', ax, az, 0) || !g.canPlace('station', bx, az, 0)) continue;
    const rails = []; for (let x = ax + 3; x <= bx - 1; x++) rails.push([x, az + 1]);
    if (rails.every(t => g.canPlace('rail', t[0], t[1], 0))) { cfg = { ax, az, bx, rails }; break outer; }
  }
  ok(cfg, 'found a station/rail layout');
  if (cfg) {
    const v1 = g._addUnit('villager', 0, cfg.ax + 5.5, cfg.az + 3.5), v2 = g._addUnit('villager', 0, cfg.ax + 9.5, cfg.az + 3.5);
    const sa = g.placeBuilding(0, 'station', cfg.ax, cfg.az, [v1.id]);
    const sb = g.placeBuilding(0, 'station', cfg.bx, cfg.az, [v2.id]);
    step(g, 40);
    ok(g.getEntity(sa).done && g.getEntity(sb).done, 'stations built');
    const ids = g.placeLine(0, 'rail', cfg.rails, [v1.id, v2.id]);
    ok(ids.length === cfg.rails.length, `rail line placed (${ids.length}/${cfg.rails.length})`);
    ok(cfg.rails.every(t => g.map.isWalkable(t[0], t[1])), 'rail tiles are walkable');
    step(g, 60);
    ok(ids.every(id => g.getEntity(id) && g.getEntity(id).done), 'rail built segment by segment');
    step(g, 1);
    const trains = () => g.units.filter(u => u.type === 'train' && !u.dead);
    ok(trains().length === 1, 'one train spawned');
    const t = trains()[0];
    if (t) {
      ok(t.train && t.train.a != null && t.train.b != null && Array.isArray(t.train.path) && t.train.path.length === cfg.rails.length, 'train field shape');
      ok(!g.cmdMove([t.id], 5, 5), 'train ignores commands');
      const x0 = t.x, gold0 = p.res.gold;
      step(g, 3);
      ok(Math.abs(t.x - x0) > 1, 'train moves');
      step(g, 30);
      ok(ev.arrive >= 3 && ev.dep >= 3, `train arrivals credit gold (${ev.arrive} arrivals)`);
      ok(p.res.gold > gold0, `gold increased by ${p.res.gold - gold0}`);
      // save / load keeps the train
      const g2 = Game.deserialize(JSON.stringify(g.serialize()));
      step(g2, 2);
      ok(g2.units.filter(u => u.type === 'train' && !u.dead).length === 1, 'train survives save/load (no duplicate)');
      // break the chain
      g.deleteEntity(ids[5]);
      step(g, 1);
      ok(trains().length === 0, 'train removed when the chain breaks');
    }
  }
}

console.log(fails.length ? 'FAIL\n - ' + fails.join('\n - ') : 'ALL OK');
process.exit(fails.length ? 1 : 0);
