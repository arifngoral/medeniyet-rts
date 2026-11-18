// Archers behind their own wall (2026-11-15, owner: Empire Earth style): node test/archers-wall-test.mjs
// - shooters behind a wall hit enemies on the far side that are in range, without walking out through the gate
// - an out-of-range enemy on the far side is not chased (auto attack / idle scan / call for help); an order still walks
// - a shooter right against the wall reaches a foe right against the far side
// - open field: idle archers still close in on an enemy they see; lobbed arrows land when the sim says (save/load, lockstep)
import { Game } from '../src/sim/game.js';
import { UNITS } from '../src/data.js';
const fails = []; const ok = (c, m) => { if (!c) fails.push(m); else console.log('ok  ', m); };
const mk = () => { const g = new Game({ mapSize: 256, enemies: 1, difficulty: 'easy', startRes: 'normal', startAge: 0, sandbox: false, seed: 11 }); g.ais.length = 0; return g; };
const step = (g, s, fn) => { for (let i = 0; i < s * 30; i++) { g.update(1 / 30); if (fn) fn(); } };
// open field east of player 0's start on seed 11: a closed ring x 82..95, z 57..70 (inside x 83..94, z 58..69),
// a gate in the middle of the north side (z 70); the enemy comes from the north (z > 70)
const X0 = 82, X1 = 95, Z0 = 57, Z1 = 70;
const ring = g => {
  const ws = [];
  for (let x = X0; x <= X1; x++) for (const z of [Z0, Z1]) ws.push(g._addBuilding('wall', 0, x, z, true));
  for (let z = Z0 + 1; z < Z1; z++) for (const x of [X0, X1]) ws.push(g._addBuilding('wall', 0, x, z, true));
  for (const b of ws) g._complete(b);
  const mid = ws.find(b => b.tx === 88 && b.tz === Z1);
  if (!g.cmdOpenGate(mid.id)) throw new Error('gate did not open');
  return ws;
};
const inside = u => u.x > X0 + 1 && u.x < X1 && u.z > Z0 + 1 && u.z < Z1;
const archers = (g, n, type = 'archer') => { const us = []; for (let i = 0; i < n; i++) us.push(g._addUnit(type, 0, 84 + (i % 5) * 2.1, Z1 - 0.7 - Math.floor(i / 5) * 1.1)); return us; };

// 1) 15 archers behind the north wall; 6 swordsmen hack at the wall right in front of them, 4 spearmen stand idle
//    6-7 tiles out (seen, mostly out of range); the archers kill the attackers and never leave the ring
{
  const g = mk(); ring(g);
  const ar = archers(g, 15);
  const wallN = x => g.buildings.find(b => b.type === 'wall' && b.tz === Z1 && b.tx === x);
  const foes = [];
  for (let i = 0; i < 6; i++) { const x = [84, 85, 86, 90, 91, 92][i], f = g._addUnit(i % 2 ? 'swordsman' : 'spearman', 1, x + 0.5, Z1 + 3); g.cmdAttack([f.id], wallN(x).id); foes.push(f); }
  const idle = []; for (let i = 0; i < 4; i++) idle.push(g._addUnit('spearman', 1, 85 + i * 2.5, Z1 + 6.6));
  let left = 0, shots = 0; g.events.on('attack', e => { if (e.attacker.owner === 0 && e.attacker.kind === 'unit') shots++; });
  step(g, 90, () => { for (const a of ar) if (!a.dead && !inside(a)) left++; });
  const dead = foes.filter(f => f.dead).length;
  ok(dead === 6, 'archers behind the wall kill all 6 wall attackers (' + dead + '/6, ' + shots + ' shots)');
  ok(left === 0, 'no archer ever left the ring (ticks outside: ' + left + ')');
  ok(ar.every(a => !a.dead), 'no archer lost (' + ar.filter(a => a.dead).length + ' dead)');
  ok(ar.every(a => a.z > Z1 - 4.5), 'archers stayed by the wall (min z ' + Math.min(...ar.map(a => a.z)).toFixed(1) + ')');
}
// 2) idle archers, an enemy out of range across the wall (in sight): nobody goes after it; once it walks up to the
//    wall it is shot
{
  const g = mk(); ring(g);
  const ar = archers(g, 5), foe = g._addUnit('spearman', 1, 89.5, Z1 + 6.4);
  let left = 0; step(g, 8, () => { for (const a of ar) if (!inside(a)) left++; });
  ok(left === 0 && ar.every(a => !a.order || a.order.type !== 'attack' || Math.hypot(a.x - foe.x, a.z - foe.z) <= g._wRange(a)), 'idle archers do not chase an out-of-range foe across the wall (outside ticks ' + left + ')');
  // the enemy auto-attacks an archer: it cannot get in and ends at the wall, in range
  step(g, 40, () => { for (const a of ar) if (!inside(a)) left++; });
  ok(foe.dead && left === 0, 'the foe that came up to the wall is shot (dead ' + foe.dead + ', outside ticks ' + left + ')');
}
// 3) an archer hit by an enemy crossbowman (range 6) from beyond the wall out of its own range does not walk out to answer
{
  const g = mk(); ring(g);
  const a = g._addUnit('archer', 0, 89.5, Z1 - 0.7), foe = g._addUnit('crossbow', 1, 89.5, Z1 + 5.0); a.hp = 1000;
  g.cmdAttack([foe.id], a.id);
  let left = 0; step(g, 15, () => { if (!inside(a)) left++; });
  ok(left === 0, 'an archer shot at from out of its range across the wall stays inside (outside ticks ' + left + ')');
  // ...but an attack the player orders still walks out through the gate
  g.cmdAttack([a.id], foe.id); let out = false; step(g, 20, () => { if (!inside(a)) out = true; });
  ok(out, 'an ordered attack still walks out through the gate (' + a.x.toFixed(1) + ',' + a.z.toFixed(1) + ')');
}
// 4) reach across the wall: an archer flush against the near side hits a foe flush against the far side
{
  const g = mk(); ring(g);
  const a = g._addUnit('archer', 0, 86.5, Z1 - 0.3), foe = g._addUnit('spearman', 1, 86.5, Z1 + 1.3); foe.hp = 1000;
  const d = Math.hypot(a.x - foe.x, a.z - foe.z), r = g._wRange(a);
  const wall = g.buildings.find(b => b.type === 'wall' && b.tz === Z1 && b.tx === 86); g.cmdAttack([foe.id], wall.id);
  step(g, 6);
  ok(d < r && foe.hp < 1000 && inside(a), 'flush against both sides: distance ' + d.toFixed(2) + ' < range ' + r + ', foe hit (' + (1000 - foe.hp) + ' dmg)');
}
// 5) open field: an idle archer closes in on an enemy it sees beyond its range and kills it; the player's men in the
//    open still answer a call for help
{
  const g = mk();
  const a = g._addUnit('archer', 0, 70.5, 64.5), foe = g._addUnit('spearman', 1, 70.5, 64.5 + UNITS.archer.range + 1.5);
  g.cmdMove([foe.id], 70.5, 64.5 + UNITS.archer.range + 1.5);
  let moved = false; const x0 = a.x, z0 = a.z;
  step(g, 30, () => { if (Math.hypot(a.x - x0, a.z - z0) > 0.5) moved = true; });
  ok(foe.dead && moved, 'open field: an idle archer walks up to an enemy in sight and kills it (dead ' + foe.dead + ', moved ' + moved + ')');
}
// 6) lobbed arrows: the arc grows with distance, crossbow bolts are flatter, damage lands at the end of the flight,
//    and a save mid-volley continues identically (lockstep)
{
  const g = mk(); ring(g);
  const ar = archers(g, 10).concat(archers(g, 5, 'crossbow').map((u, i) => { u.x = 84 + i * 2.1; u.z = Z1 - 3.0; return u; }));
  for (let i = 0; i < 6; i++) { const f = g._addUnit('swordsman', 1, 84 + i * 1.8, Z1 + 2.5); g.cmdAttack([f.id], g.buildings.find(b => b.type === 'wall' && b.tz === Z1 && b.tx === (i < 2 ? 84 + i : 90 + i)).id); }
  const seen = new Map();
  const watch = () => { for (const p of g.projectiles) if (!seen.has(p.id)) seen.set(p.id, { sx: p.sx, sz: p.sz, sy: p.sy, tx: p.tx, tz: p.tz, ty: p.ty, arc: p.arc, dur: p.dur, bolt: !!p.bolt }); };
  step(g, 3, watch);
  const c = Game.deserialize(JSON.stringify(g.serialize())); c.ais.length = 0;   // (the test game runs without its AI)
  step(g, 6, watch); step(c, 6);
  ok(g.hash() === c.hash(), 'save/load mid-volley continues identically (hash ' + g.hash() + ' / ' + c.hash() + ')');
  const arrows = [...seen.values()].filter(s => !s.bolt), bolts = [...seen.values()].filter(s => s.bolt);
  ok(arrows.length > 10 && bolts.length > 3, 'volley fired (' + arrows.length + ' arrows, ' + bolts.length + ' bolts)');
  // every lob across the wall clears its drawn top (~2.7; the sim aims WALL_CLEAR 3.4 high, a target walking up eats a little)
  let low = 0, minClr = 9; for (const s of seen.values()) { const f = (Z1 + 0.5 - s.sz) / (s.tz - s.sz); if (!(f > 0 && f < 1)) continue; const y = s.sy + (s.ty - s.sy) * f + 4 * s.arc * f * (1 - f) - g.map.heightAt(s.sx + (s.tx - s.sx) * f, Z1 + 0.5); minClr = Math.min(minClr, y); if (y < 2.8 && f > 0.12 && f < 0.88) low++; }
  ok(low === 0, 'every arrow / bolt across the wall flies over it (lowest crossing ' + minClr.toFixed(2) + ' over the ground)');
  // open field: the arc and flight time grow with distance; crossbow bolts fly flatter
  const g3 = mk(), sh = (type, dz) => { const a = g3._addUnit(type, 0, 66.5, 60.5), t = g3._addUnit('spearman', 1, 66.5, 60.5 + dz); g3._fire(a, t, 1, 'arrow'); return g3.projectiles[g3.projectiles.length - 1]; };
  const a3 = sh('archer', 3), a5 = sh('archer', 5), b5 = sh('crossbow', 5);
  ok(a5.arc > a3.arc && a5.dur > a3.dur && b5.arc < a5.arc && b5.dur < a5.dur && b5.bolt && !a5.bolt, 'open field: arc / flight grow with distance (3: ' + a3.arc.toFixed(2) + ' / ' + a3.dur.toFixed(2) + 's, 5: ' + a5.arc.toFixed(2) + ' / ' + a5.dur.toFixed(2) + 's), bolt flatter (' + b5.arc.toFixed(2) + ' / ' + b5.dur.toFixed(2) + 's)');
  // flight timing: one arrow at a fresh target, damage exactly when its flight ends
  const g2 = mk(), a = g2._addUnit('archer', 0, 70.5, 60.5), t = g2._addUnit('spearman', 1, 70.5, 64.5); t.hp = 1000; t.order = { type: 'move', x: 70.5, z: 64.5 };
  g2.cmdAttack([a.id], t.id); let fireT = -1, hitT = -1, dur = 0;
  step(g2, 3, () => { if (fireT < 0 && g2.projectiles.length) { fireT = g2.time; dur = g2.projectiles[0].dur; } if (hitT < 0 && t.hp < 1000) hitT = g2.time; });
  ok(fireT > 0 && hitT > 0 && Math.abs(hitT - fireT - dur) < 0.05, 'the hit lands when the arrow does (flight ' + dur.toFixed(2) + ' s, hit after ' + (hitT - fireT).toFixed(2) + ' s)');
}
if (fails.length) { console.log('FAIL', fails); process.exit(1); } else console.log('ALL OK');
