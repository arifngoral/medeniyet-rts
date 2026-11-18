// temporary check (spawn outside dock, sail rule, cmdReturn)
import { Game } from '../src/sim/game.js';
const fails = []; const ok = (c, m) => { if (!c) fails.push(m); else console.log('  ok', m); };
const run = (g, s) => { for (let i = 0; i < s * 10; i++) g.update(0.1); };
let tested = 0;
for (const [size, seed] of [[96, 9], [128, 2], [128, 5], [96, 3]]) {
  const g = new Game({ mapSize: size, enemies: 0, difficulty: 'easy', seed, sandbox: true, startRes: 'high' });
  g.ais.length = 0;
  const P = g.players[0]; P.res = { food: 9000, wood: 9000, stone: 9000, gold: 9000 }; P.age = 2;
  let spot = null, bd = 1e9; const N = g.map.size;
  for (let tz = 2; tz < N - 4; tz++) for (let tx = 2; tx < N - 4; tx++) { const d = Math.hypot(tx - P.startX, tz - P.startZ); if (d < bd && g.canPlace('dock', tx, tz, 0)) { bd = d; spot = [tx, tz]; } }
  if (!spot) continue; tested++;
  const vil = g.unitsOf(0).filter(u => u.type === 'villager').map(u => u.id);
  const id = g.placeBuilding(0, 'dock', spot[0], spot[1], vil); run(g, 90); const b = g.getEntity(id);
  ok(b.done, `[${size}/${seed}] dock at ${spot} done`);
  g.train(id, 'fishboat'); g.train(id, 'galley'); run(g, 40);
  for (const s of g.unitsOf(0).filter(u => u.naval)) {
    const inF = s.x >= b.tx && s.x < b.tx + 3 && s.z >= b.tz && s.z < b.tz + 3;
    ok(!inF && g._navPass(s.x | 0, s.z | 0), `[${size}/${seed}] ${s.type} at ${s.x.toFixed(1)},${s.z.toFixed(1)} outside footprint on sailable tile (tile ${g.map.tiles[(s.z | 0) * N + (s.x | 0)]})`);
  }
  // sail rule sanity: no sailable shallow tile with < 5 water neighbours and no deep neighbour
  let bad = 0; const T = g.map.tiles; const M = g._navSailMask();
  for (let z = 1; z < N - 1; z++) for (let x = 1; x < N - 1; x++) if (M[z * N + x] && T[z * N + x] === 3) { let w = 0, d = 0; for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) { if (!i && !j) continue; const a = T[(z + j) * N + x + i]; if (a === 4) d++; if (a === 3 || a === 4) w++; } if (!d && w < 5) bad++; }
  ok(bad === 0, `[${size}/${seed}] sail mask rule`);
  // cmdReturn
  const boat = g.unitsOf(0).find(u => u.type === 'fishboat'); const sh = g._navNearestShoal(boat.x, boat.z);
  g.cmdGather([boat.id], sh.id);
  for (let s = 0; s < 120 && !(boat.carry && boat.carry.amount >= 5); s++) run(g, 1);
  ok(boat.carry && boat.carry.amount >= 5, `[${size}/${seed}] boat has cargo ${boat.carry && boat.carry.amount}`);
  const dist = Math.hypot(boat.x - sh.x, boat.z - sh.z); ok(dist <= 1.6, `[${size}/${seed}] fishing within ~1 tile (${dist.toFixed(2)})`);
  const f0 = P.stats.gathered.food, tgt = boat.order.targetId; let dep = 0; g.events.on('deposit', e => { if (e.unit === boat) dep++; });
  ok(g.cmdReturn([boat.id], id), 'cmdReturn true');
  for (let s = 0; s < 60 && !dep; s++) run(g, 1);
  ok(dep === 1 && P.stats.gathered.food > f0 && !boat.carry, `[${size}/${seed}] delivered at dock`);
  ok(boat.order && boat.order.type === 'fish' && boat.order.phase === 'go' && boat.order.targetId === tgt, `[${size}/${seed}] resumes fishing same shoal`);
  run(g, 20); ok(boat.order && boat.order.type === 'fish' && boat.carry && boat.carry.amount > 0, 'fishing again');
  // without cargo: park next to dock
  boat.carry = null; g.cmdReturn([boat.id], id); run(g, 30);
  ok(!boat.order && g._edge(boat, b) < 3 && g._navPass(boat.x | 0, boat.z | 0), `[${size}/${seed}] empty boat parked by dock (edge ${g._edge(boat, b).toFixed(2)})`);
}
ok(tested >= 2, 'tested maps ' + tested);
if (fails.length) { console.log('FAIL', fails); process.exit(1); } console.log('ALL OK');
