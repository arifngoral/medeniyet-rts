// AI town walls (2026-11-14): node test/ai-wall-test.mjs [minutes]
// Hard vs normal AI on a 256 map (all-AI multiplayer match). Both must fence their towns (wall pieces / opened gates),
// nothing of theirs may be shut in (every unit, building and worked resource stays reachable from the town
// center), villagers keep working, and a save taken while the walls go up must continue exactly like the original.
import { Game } from '../src/sim/game.js';

const MIN = +(process.argv[2] || 22);
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); console.log((c ? '  ok   ' : '  FAIL ') + m); return !!c; };
const DT = 1 / 30;

const g = new Game({ mapSize: 256, enemies: 1, difficulty: 'normal', startRes: 'normal', startAge: 0, sandbox: false, seed: 3, mp: true });   // (mp: an all-AI match does not end at once)
g.convertToAI(0, 'hard');   // (an AI-run player 0 comes back from a save as an AI too)

// tiles a player's town center reaches; units / buildings that are not next to one of them are shut in
function shutIn(pid) {
  const tc = g.buildingsOf(pid).find(b => b.type === 'towncenter'); if (!tc) return ['no town center'];
  const N = g.map.size; let s0 = null;
  for (let x = tc.tx - 1; x <= tc.tx + tc.size && !s0; x++) for (const z of [tc.tz - 1, tc.tz + tc.size]) if (g._pass(x, z, pid)) { s0 = [x, z]; break; }
  const d = g._ffSweep(s0[0], s0[1], pid, null);
  const near = (x0, z0, s) => { for (let x = x0 - 1; x <= x0 + s; x++) for (let z = z0 - 1; z <= z0 + s; z++) if (x >= 0 && z >= 0 && x < N && z < N && d[z * N + x] >= 0) return true; return false; };
  const out = [];
  for (const u of g.unitsOf(pid)) {
    if (u.naval || u.aboard) continue;
    if (!near(u.x | 0, u.z | 0, 1)) out.push(u.type + '#' + u.id);
    const o = u.order && u.order.type === 'return' ? u.order.resume : u.order, t = o && o.targetId != null ? g.getEntity(o.targetId) : null;
    if (t && !t.dead && t.kind === 'resource' && !near(t.x | 0, t.z | 0, 1)) out.push('resource of ' + u.id);
  }
  for (const b of g.buildingsOf(pid)) if (b.type !== 'wall' && b.type !== 'gate' && !near(b.tx, b.tz, b.size)) out.push(b.type + '#' + b.id);
  return out;
}

// a copy loaded from a save taken while wall pieces are going up runs alongside the original for 3 minutes
let A = null, savedAt = 0, same = true, plansBack = false, worstShut = [[], []];
const T = MIN * 60 * 30;
for (let t = 1; t <= T; t++) {
  g.update(DT);
  if (A) { A.update(DT); if (t % 300 === 0 && A.hash() !== g.hash()) same = false; if (t - savedAt >= 3 * 60 * 30) A = null; }
  if (t % (60 * 30) === 0) for (const pid of [0, 1]) { const s = shutIn(pid); if (s.length > worstShut[pid].length) worstShut[pid] = s; }
  if (!savedAt && g.ais.some(a => a.wall) && g.buildings.some(b => b.type === 'wall' && !b.done)) {
    A = Game.deserialize(JSON.parse(JSON.stringify(g.serialize()))); savedAt = t;
    plansBack = A.ais.length === 2 && A.ais.filter(a => a.wall).length === g.ais.filter(a => a.wall).length;
  }
}
for (const pid of [0, 1]) {
  const bs = g.buildingsOf(pid), ai = g.ais[pid], W = ai.wall;
  const walls = bs.filter(b => b.type === 'wall' && b.done).length, gates = bs.filter(b => b.type === 'gate').length / 3;
  console.log(`P${pid} (${ai.difficulty}): ${walls} wall pieces, ${gates} gates, ${bs.filter(b => b.type === 'tower').length} towers; plan ${W ? `R ${W.R}, sides ${W.sides.join('')}, ${W.tiles.length} tiles, ${W.gates.length} gates` : 'none'}`);
  // (gates go up first, the ring after them: normal starts later and may still be on its gates)
  ok(!!W && (pid === 0 ? walls >= 20 : walls + gates * 3 >= 9), `P${pid} put up a town wall (${walls} pieces + ${gates} gates)`);
  ok(gates >= (pid === 0 ? 2 : 1), `P${pid} opened gates in it (${gates})`);
  ok(!worstShut[pid].length, `P${pid}: nothing shut in by its walls${worstShut[pid].length ? ': ' + worstShut[pid].slice(0, 5).join(', ') : ''}`);
  const vills = g.unitsOf(pid).filter(u => u.type === 'villager'), idle = vills.filter(u => !u.order).length;
  ok(vills.length >= 20 && idle <= 3, `P${pid} villagers keep working (${vills.length}, ${idle} idle)`);
  ok(!Object.keys(ai.errors).length, `P${pid} AI without errors ${JSON.stringify(ai.errors).slice(0, 200)}`);
}
ok(savedAt > 0, 'a save was taken while wall pieces were being built (minute ' + (savedAt / 1800).toFixed(1) + ')');
ok(plansBack, 'the wall plans came back with the save');
ok(same, 'the loaded copy and the original (never saved) stayed in step for 3 minutes');
ok(!g.over, 'the match is still running');
console.log(fails.length ? `\n${fails.length} FAILED` : '\nALL OK');
process.exit(fails.length ? 1 : 0);
