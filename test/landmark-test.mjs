// Age-up buildings and heroes (src/landmarks.js): data, building one ages up, only one of the two, effects while it
// stands, one hero at a time, the aura, save / load, two runs in sync, the AI uses them. Run: node test/landmark-test.mjs
import { UNITS, BUILDINGS, AGES } from '../src/data.js';
import { CIVS } from '../src/civs.js';
import { LANDMARKS, HEROES, HERO_AURA, landmarkLines } from '../src/landmarks.js';
import { Game } from '../src/sim/game.js';

const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); console.log((c ? '  ok ' : '  FAIL ') + m); return !!c; };
const base = { mapSize: 96, seed: 11, startRes: 'high', startAge: 0, enemies: 1 };
const rich = (g) => { for (const p of g.players) Object.assign(p.res, { food: 20000, wood: 20000, stone: 20000, gold: 20000 }); return g; };

// --- data
{
  const bad = [], m0 = new Game({ ...base }).players[0].mods;
  for (const civ in LANDMARKS) {
    if (!CIVS[civ]) bad.push(civ + ': no such civilization');
    if (LANDMARKS[civ].length !== 4 || LANDMARKS[civ].some(p => p.length !== 2)) bad.push(civ + ': 4 ages x 2');
    if (!HEROES[civ] || !UNITS[HEROES[civ].id] || !UNITS[HEROES[civ].id].hero) bad.push(civ + ': hero');
    LANDMARKS[civ].forEach((pair, i) => pair.forEach(l => {
      const d = BUILDINGS[l.id];
      if (!d || !d.landmark || d.landmark.to !== i + 1 || d.age !== i) bad.push(l.id + ': age');
      if (JSON.stringify(d.cost) !== JSON.stringify(AGES[i + 1].cost)) bad.push(l.id + ': cost = the age\'s');
      if (!d.trains.includes(HEROES[civ].id)) bad.push(l.id + ': trains the hero');
      for (const k in d.landmark.fx || {}) if (!(k in m0)) bad.push(l.id + ': unknown fx ' + k);
      if (landmarkLines(l.id).length < 2) bad.push(l.id + ': text');
    }));
  }
  ok(!bad.length, Object.keys(LANDMARKS).length + ' civilizations with age-up buildings: data' + (bad.length ? ' - ' + bad.join('; ') : ''));
}

const site = (g, type, owner = 0) => {
  const tc = g.buildings.find(b => b.owner === owner && b.type === 'towncenter');
  for (let r = 7; r < 30; r++) for (let a = 0; a < 24; a++) { const tx = Math.round(tc.x + Math.cos(a / 24 * 6.283) * r - 3), tz = Math.round(tc.z + Math.sin(a / 24 * 6.283) * r - 3); if (g.canPlace(type, tx, tz, owner)) return [tx, tz]; }
  return null;
};
const vills = (g, n, owner = 0) => g.units.filter(u => u.owner === owner && u.type === 'villager').slice(0, n).map(u => u.id);
const run = (g, s, until) => { for (let i = 0; i < 30 * s; i++) { g.update(1 / 30); if (until && until()) return true; } return false; };

// --- building one ages up; the other is refused; the town center does not age up
{
  const g = rich(new Game({ ...base, civ: 'roma' })), p = g.players[0];
  const tc = g.buildings.find(b => b.owner === 0 && b.type === 'towncenter');
  ok(!g.canAgeUp(0).ok && !g.ageUp(tc.id), 'roma: no age-up at the town center');
  ok(!g.isUnlocked(0, 'building', 'lm_kervansaray') && g.isUnlocked(0, 'building', 'lm_forum') && !g.isUnlocked(0, 'building', 'lm_pantheon'), 'only its own buildings, only the next age\'s');
  const [tx, tz] = site(g, 'lm_forum'), res0 = { ...p.res };
  const id = g.placeBuilding(0, 'lm_forum', tx, tz, vills(g, 4));
  ok(id != null && p.res.food === res0.food - AGES[1].cost.food, 'placed, paid the age\'s cost');
  const [ax, az] = site(g, 'lm_castra');
  ok(g.placeBuilding(0, 'lm_castra', ax, az, vills(g, 1)) == null && g.landmarkWhy(0, 'lm_castra'), 'the other one of the same age is refused: ' + g.landmarkWhy(0, 'lm_castra'));
  const g0 = p.mods.gather.food;
  ok(run(g, 400, () => p.age === 1) && g.getEntity(id).done, `finished -> Bronze Age (at ${g.time.toFixed(0)} s with 4 villagers)`);
  ok(p.mods.gather.food > g0 && p.mods.trade > 0, 'its effects are on (food gathering, trade)');
  ok(g.isUnlocked(0, 'building', 'lm_pantheon') && g.isUnlocked(0, 'building', 'lm_limes') && !g.isUnlocked(0, 'building', 'lm_castra'), 'now the next age\'s two; the missed one stays closed');
  // save / load keeps the effects
  const c = Game.deserialize(JSON.parse(JSON.stringify(g.serialize())));
  ok(c.players[0].age === 1 && c.players[0].mods.gather.food === p.mods.gather.food && c.hash() === g.hash(), 'save / load: age, effects and hash');
  // destroyed: the effects end, the age stays
  g._kill(g.getEntity(id), null);
  ok(p.age === 1 && Math.abs(p.mods.gather.food - g0) < 1e-9 && p.mods.trade === 0, 'destroyed: effects gone, the age kept');
  // deleting an unfinished one gives back what was not built
  const [bx2, bz2] = site(g, 'lm_pantheon'), f1 = p.res.food;
  const id2 = g.placeBuilding(0, 'lm_pantheon', bx2, bz2, vills(g, 2)); run(g, 5);
  const f2 = p.res.food; g.deleteEntity(id2);
  ok(p.res.food - f2 > AGES[2].cost.food * 0.8 && f1 - f2 > 0, 'an unfinished one deleted: most of the cost back');
}

// --- the hero: from an age-up building, one at a time, stronger with the age, its aura
{
  const g = rich(new Game({ ...base, civ: 'viking' })), p = g.players[0];
  const [tx, tz] = site(g, 'lm_uzunev'), id = g.placeBuilding(0, 'lm_uzunev', tx, tz, vills(g, 5));
  run(g, 400, () => p.age === 1);
  const lm = g.getEntity(id);
  ok(g.train(lm.id, 'ragnar') && !g.train(lm.id, 'ragnar') && !g.train(lm.id, 'fatih'), 'the hero trains once; a second one and another civilization\'s are refused');
  run(g, 90, () => g.units.some(u => u.type === 'ragnar'));
  const h = g.units.find(u => u.type === 'ragnar');
  ok(h && p.heroId === h.id && g.heroBusy(0, 'ragnar'), 'Ragnar is out');
  const hp1 = h.maxHp; p.age = 3; g._rescaleUnits(p);
  ok(h.maxHp > hp1 * 1.35, `stronger every age (${hp1} -> ${h.maxHp} in the Gunpowder Age)`);
  const s = g.units.find(u => u.owner === 0 && u.type === 'villager');
  s.x = h.x + 2; s.z = h.z; const near = g._heroNear(s); s.x = h.x + HERO_AURA.r + 3; const far = g._heroNear(s);
  ok(near && !far && !g._heroNear(h), 'the aura: own units near the hero, not far ones, not the hero');
  g._kill(h, null); run(g, 1);
  ok(!g.heroBusy(0, 'ragnar') && g.train(lm.id, 'ragnar'), 'dead: may be trained again');
}

// --- the AI ages up by building, picks one, trains its hero; two runs stay in sync
{
  const mk = () => new Game({ mapSize: 96, seed: 1007, mp: true, me: 0, startRes: 'normal', startAge: 0, mapType: 'plains', players: [{ kind: 'ai', team: 1, difficulty: 'hard', civ: 'misir' }, { kind: 'ai', team: 2, difficulty: 'hard', civ: 'kore' }] });
  const a = mk(), b = mk();
  for (let t = 0; t < 30 * 60 * 9; t++) { a.update(1 / 30); b.update(1 / 30); }
  const lms = a.buildings.filter(x => x.owner === 0 && BUILDINGS[x.type].landmark && x.done);
  ok(a.players[0].age >= 1 && lms.length >= 1, `AI (misir): built ${lms.map(x => BUILDINGS[x.type].name).join(', ')} -> age ${a.players[0].age}`);
  ok(a.players[1].age >= 1 && !a.buildings.some(x => x.owner === 1 && BUILDINGS[x.type].landmark), 'AI (kore, no age-up buildings yet): ages up at the town center as before');
  ok(a.units.some(u => u.owner === 0 && u.type === 'ramses'), 'AI trains its hero');
  ok(a.hash() === b.hash(), 'two runs: same hash after 9 min');
}
// --- cfg.noLandmarks: the old way for everybody (balance measurements)
{
  const g = new Game({ ...base, civ: 'turk', noLandmarks: true });
  ok(!g.lmCiv(0) && !g.isUnlocked(0, 'building', 'lm_kervansaray'), 'cfg.noLandmarks: the town center age-up again');
}

console.log(fails.length ? 'FAILED: ' + fails.length : 'ALL OK');
process.exit(fails.length ? 1 : 0);
