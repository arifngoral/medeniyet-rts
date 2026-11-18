// Aevum - a wall from map edge to map edge must close the way (the outer tile ring is impassable for land units).
// Run: node test/edge-wall-test.mjs
import { Game } from '../src/sim/game.js';

let failed = 0;
const ok = (c, msg) => { if (c) console.log('  ok   ' + msg); else { failed++; console.log('  FAIL ' + msg); } };

const g = new Game({ mapSize: 96, mapType: 'plains', seed: 5, enemies: 1, sandbox: true });
const N = g.map.size, X = 48;
// clear the column (trees, rocks, water) so the wall is the only thing between the halves
for (let z = 0; z < N; z++) { const k = z * N + X; g.map.tiles[k] = 0; g.map.blocked[k] = 0; g.resAt[k] = 0; }
for (const e of [...g.entities.values()]) if (e.kind === 'resource' && (e.x | 0) === X) { e.dead = true; g.entities.delete(e.id); }
let placed = 0;
for (let z = 1; z < N - 1; z++) if (g._addBuilding('wall', 0, X, z, true)) placed++;
ok(placed === N - 2, 'wall placed on every buildable tile of the column (' + placed + ' of ' + (N - 2) + ')');
ok(!g._pass(X, 0, 1) && !g._pass(X, N - 1, 1) && !g._pass(0, 10, 1), 'the outer ring is impassable');
ok(g._pass(X - 2, 10, 1), 'inner tiles stay passable');
// enemy path from the left half to the right half: it must not get across
for (const [z0, z1] of [[2, 2], [1.5, 1.5], [N - 1.5, N - 1.5], [N / 2, N / 2]]) {
  const p = g._findPath(X - 6, z0, X + 6, z1, -1, 1);
  const last = p.length ? [p[p.length - 2], p[p.length - 1]] : [X - 6, z0];
  ok(last[0] < X, 'no way around the wall near z=' + z0 + ' (path ends at x=' + last[0] + ')');
}
// walls / gates / towers may stand on the outer ring (so a wall reaches the edge), other buildings may not
// (towers are 3x3 since 2026-11-14: one must fit flush against the east edge somewhere)
ok(g.canPlace('wall', 20, 0, 0) && g.canPlace('wall', 0, 20, 0) && Array.from({ length: N - 20 }, (_, i) => i + 10).some(z => g.canPlace('tower', N - 3, z, 0)) && g.canPlace('gate', 40, N - 1, 0), 'wall, tower and gate can be placed on the edge tiles');
ok(!g.canPlace('house', 0, 20, 0) && !g.canPlace('barracks', 20, 0, 0) && !g.canPlace('wall', -1, 20, 0) && !g.canPlace('wall', N, 20, 0), 'other buildings stay off the edge; nothing outside the map');
// the wall's owner walks through (own walls are passable for him only as gates; here: also blocked)
console.log(failed ? '\n' + failed + ' check(s) FAILED' : '\nALL OK');
process.exit(failed ? 1 : 0);
