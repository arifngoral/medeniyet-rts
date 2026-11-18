// Long-route pathing for a crowd (flow field, 2026-11-14): node test/path-test.mjs
// 300 spearmen / archers are sent from player 0's start to a far tile whose walk is much longer than the straight
// line (forests, ridges). Every move order must end at its own spot (none dropped mid-route among trees), the
// per-tick A* budget must not be overrun, and a save taken mid-route must continue exactly like the original.
import { Game } from '../src/sim/game.js';

const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); console.log((c ? '  ok   ' : '  FAIL ') + m); return !!c; };
const DT = 1 / 30;

function setup(seed, mapSize) {
  const g = new Game({ mapSize, enemies: 1, difficulty: 'easy', seed, startRes: 'normal', startAge: 0 });
  g.ais.length = 0;
  for (const u of [...g.units]) if (u.owner === 1) g._kill(u);
  const p = g.players[0], N = g.map.size, f0 = g._freeNear(p.startX + 4, p.startZ + 4, 0);
  // the reachable tile with the biggest detour (walk minus straight line), at least a third of the map away
  const d = g._ffSweep(f0.x | 0, f0.z | 0, 0, null);
  let best = -1, bs = -1;
  for (let k = 0; k < N * N; k++) { if (d[k] < 0) continue; const x = k % N, z = (k / N) | 0, e = Math.hypot(x - f0.x, z - f0.z); if (e < N * 0.35 || d[k] > 420) continue; const s = d[k] - e; if (s > bs) { bs = s; best = k; } }
  const tx = best % N + 0.5, tz = ((best / N) | 0) + 0.5, ids = [];
  for (let i = 0; i < 300; i++) { const f = g._freeNear(f0.x + (i % 20) * 0.3, f0.z + ((i / 20) | 0) * 0.3, 0); ids.push(g._addUnit(i % 2 ? 'archer' : 'spearman', 0, f.x, f.z).id); }
  return { g, ids, tx, tz, walk: d[best], straight: Math.hypot(tx - f0.x, tz - f0.z) };
}

// fell the tree nearest the crowd (bumps the blocking version: every flow field is rebuilt)
function fell(g) {
  let cx = 0, cz = 0, n = 0; for (const u of g.units) if (u.owner === 0 && !u.dead) { cx += u.x; cz += u.z; n++; }
  const t = g.resourceNear(cx / n, cz / n, 40, 'tree'); if (t) g._kill(t);
}

for (const [seed, size] of [[11, 320], [7, 320], [42, 384]]) {
  console.log(`seed ${seed}, map ${size}`);
  const { g, ids, tx, tz, walk, straight } = setup(seed, size);
  // (1.1x since 2026-11-14: forests became groves split by grass lanes, so the worst detour on these maps fell from ~1.3x+ to ~1.15-1.3x)
  ok(walk > straight * 1.1, `target (${tx}, ${tz}): walk ${walk} tiles vs straight ${straight.toFixed(0)}`);
  const ends = [], idSet = new Set(ids), on = g._next;
  g._next = function (u) { if (idSet.has(u.id) && u.order && u.order.type === 'move') ends.push(Math.hypot(u.x - u.order.x, u.z - u.order.z)); return on.call(this, u); };
  g.cmdMove(ids, tx, tz);
  let over = 0, worst = 0;
  for (let t = 0; t < 400 * 30; t++) {
    const a = performance.now(); g.update(DT); worst = Math.max(worst, performance.now() - a);
    if ((g._pn || 0) > 5000) over++;
    if (seed === 11 && t === 60 * 30 - 20) fell(g);   // the crowd's field goes stale just before the save
    if (seed === 11 && t === 60 * 30) {   // save / load mid-route: the copy must stay in step with the original
      const A = Game.deserialize(JSON.parse(JSON.stringify(g.serialize())));
      A.ais.length = 0;
      const B = Game.deserialize(JSON.parse(JSON.stringify(g.serialize())));
      B.ais.length = 0;
      let same = true;
      for (let k = 0; k < 90 * 30 && same; k++) { A.update(DT); B.update(DT); if (k % 150 === 0 && A.hash() !== B.hash()) same = false; }
      // the original keeps going too: run a copy of it alongside from the same moment
      ok(same, 'two loaded copies taken mid-route stay in step for 90 s');
      const C = Game.deserialize(JSON.parse(JSON.stringify(g.serialize()))); C.ais.length = 0;
      let same2 = true;
      for (let k = 0; k < 60 * 30 && same2; k++) { if (k === 100) { fell(g); fell(C); } g.update(DT); C.update(DT); t++; if (k % 150 === 0 && g.hash() !== C.hash()) same2 = false; }
      ok(same2, 'the original (never saved) and a loaded copy stay in step for 60 s');
    }
  }
  const left = ids.filter(id => { const u = g.getEntity(id); return u && !u.dead && u.order; }).length;
  ok(ends.length === 300 && left === 0, `every unit's move order ended (${ends.length} / 300, still walking ${left})`);
  ok(ends.every(x => x <= 2), `every order ended at its own spot (worst ${Math.max(0, ...ends).toFixed(2)} tiles off)`);
  const far = ids.map(id => g.getEntity(id)).filter(u => Math.hypot(u.x - tx, u.z - tz) > 30).length;
  ok(far === 0, `the whole crowd stands round the target (${far} units further than 30 tiles)`);
  ok(over === 0, `per-tick path budget never overrun (${over} ticks)`);
  console.log(`  (worst tick ${worst.toFixed(1)} ms)`);
}

console.log(fails.length ? `\n${fails.length} FAILED` : '\nALL OK');
process.exit(fails.length ? 1 : 0);
