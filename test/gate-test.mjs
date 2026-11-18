// Opening a gate in a wall (Empire Earth style): node test/gate-test.mjs
import { Game } from '../src/sim/game.js';
import { BUILDINGS } from '../src/data.js';
const fails = []; const ok = (c, m) => { if (!c) fails.push(m); else console.log('ok  ', m); };
const mk = () => { const g = new Game({ mapSize: 256, enemies: 1, difficulty: 'easy', startRes: 'normal', seed: 11 }); g.ais.length = 0; return g; };
const Z = 70, X0 = 70, X1 = 100;   // open field east of player 0 on seed 11
const wallLine = (g, owner) => { const ws = []; for (let x = X0; x <= X1; x++) { const b = g._addBuilding('wall', owner, x, Z, true); g._complete(b); ws.push(b); } return ws; };
{
  const g = mk(), p = g.players[0], ws = wallLine(g, 0), mid = ws[15];
  const stone0 = p.res.stone;
  ok(g.canOpenGate(0, mid.id).ok, 'a wall piece in a straight run can open a gate');
  ok(g.execCommand(0, 'cmdOpenGate', [mid.id]), 'cmdOpenGate runs through execCommand (lockstep path)');
  const gates = g.buildings.filter(b => b.type === 'gate' && b.owner === 0);
  ok(gates.length === 3 && gates.every(b => b.tz === Z && b.done) && gates.map(b => b.tx).sort((a, b) => a - b).join() === [mid.tx - 1, mid.tx, mid.tx + 1].join(), '3 finished gate pieces replace the clicked wall and its neighbours');
  ok(p.res.stone === stone0 - BUILDINGS.gate.cost.stone, 'the gate cost is paid once');
  ok(!g.buildings.some(b => b.type === 'wall' && b.tz === Z && Math.abs(b.tx - mid.tx) <= 1), 'the old wall pieces are gone');
  // own units walk through, the enemy is stopped. (2026-11-14: one at a time - side by side they fought each other -
  // and the enemy is checked on the gate tiles: since the forests became groves the wall's open ends can be walked round)
  const me = g._addUnit('spearman', 0, mid.tx + .5, Z - 6);
  g.cmdMove([me.id], mid.tx + .5, Z + 6);
  for (let i = 0; i < 30 * 25; i++) g.update(1 / 30);
  ok(me.z > Z + 3, 'own soldier walks through the gate (z ' + me.z.toFixed(1) + ')');
  const foe = g._addUnit('spearman', 1, mid.tx + .5, Z - 6); let onGate = false;
  g.cmdMove([foe.id], mid.tx + .5, Z + 6);
  for (let i = 0; i < 30 * 25; i++) { g.update(1 / 30); if ((foe.z | 0) === Z && Math.abs((foe.x | 0) - mid.tx) <= 1) onGate = true; }
  ok(!onGate, 'enemy soldier cannot pass the gate (never on its tiles; ended at ' + foe.x.toFixed(1) + ',' + foe.z.toFixed(1) + ')');
  // a wall with fewer than 3 pieces in a row cannot hold a gate; the enemy cannot open my wall
  const lone = g._addBuilding('wall', 0, 120, 90, true); g._complete(lone);
  ok(!g.canOpenGate(0, lone.id).ok && !g.execCommand(0, 'cmdOpenGate', [lone.id]), 'a lone wall piece cannot open a gate');
  ok(!g.execCommand(1, 'cmdOpenGate', [ws[3].id]), 'another player cannot open my wall');
  // an end piece opens a gate shifted one inward
  ok(g.cmdOpenGate(ws[0].id) && g.buildings.filter(b => b.type === 'gate' && b.tz === Z && b.tx <= X0 + 2).length === 3, 'an end piece opens the gate one tile inward');
  // save / load keeps the gates
  const c = Game.deserialize(JSON.stringify(g.serialize()));
  ok(c.buildings.filter(b => b.type === 'gate').length === 6, 'gates survive save/load');
}
{ // no money, no gate
  const g = mk(), ws = wallLine(g, 0); g.players[0].res.stone = 0;
  ok(!g.cmdOpenGate(ws[10].id) && g.buildings.every(b => b.type !== 'gate'), 'not enough stone: nothing changes');
}
if (fails.length) { console.log('FAIL', fails); process.exit(1); } else console.log('ALL OK');
