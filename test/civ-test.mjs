// Civilizations: data shape, bonuses reach the simulation, deterministic. Run from ROOT: node test/civ-test.mjs
import { UNITS } from '../src/data.js';
import { CIVS, CIV_IDS, resolveCiv, civLines, civUnit } from '../src/civs.js';
import { BUILDINGS } from '../src/data.js';
import { AI_STYLES, civStyle, tuneDiff, civRoleBias } from '../src/civ-ai.js';
import { Game } from '../src/sim/game.js';
import { NetSession } from '../src/net/session.js';

const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); console.log((c ? '  ok ' : '  FAIL ') + m); return !!c; };
const base = { mapSize: 96, seed: 7, startRes: 'normal', startAge: 0, enemies: 1 };

// --- data: every fx key is a mod the simulation knows, in the same shape (number / per-class object)
{
  const g = new Game({ ...base }), m0 = g.players[0].mods;
  let bad = [];
  for (const id of CIV_IDS) {
    const c = CIVS[id];
    if (c.id !== id || !c.name || !c.icon || !c.passive) bad.push(id + ': incomplete');
    for (const k in c.fx) {
      if (!(k in m0)) bad.push(`${id}: unknown mod ${k}`);
      else if ((typeof c.fx[k] === 'number') !== (typeof m0[k] === 'number')) bad.push(`${id}: wrong shape ${k}`);
      else if (typeof c.fx[k] === 'object') for (const s in c.fx[k]) if (k === 'gather' ? !(s in m0.gather) : !(Object.values(UNITS).some(u => u.cls === s) || UNITS[s])) bad.push(`${id}: ${k}.${s} is no class / unit`);
    }
    const lines = civLines(id);
    if (!lines.length || lines.some(l => !/[a-zçğıöşü]/i.test(l) || /^[a-z]+$/i.test(l))) bad.push(`${id}: bonus text missing (${lines.join(' | ')})`);
  }
  ok(!bad.length, `${CIV_IDS.length} civilizations: data and bonus texts` + (bad.length ? ' - ' + bad.join('; ') : ''));
  ok(!g.players.some(p => p.civ), 'no cfg.civ: nobody has a civilization (old behaviour)');
}

// --- picking
{
  ok(resolveCiv('roma', 1, 0) === 'roma' && resolveCiv('nope', 1, 0) === null && resolveCiv(undefined, 1, 0) === null, 'resolveCiv: id / unknown / missing');
  const a = [0, 1, 2, 3].map(i => resolveCiv('random', 99, i)), b = [0, 1, 2, 3].map(i => resolveCiv('random', 99, i));
  ok(a.every(x => CIVS[x]) && a.join() === b.join(), 'random is a real civilization and repeatable: ' + a.join(','));
  const seen = new Set(); for (let s = 1; s <= 400; s++) seen.add(resolveCiv('random', s * 7919, 1));
  ok(seen.size === CIV_IDS.length, `random reaches every civilization (${seen.size}/${CIV_IDS.length})`);
  const g = new Game({ ...base, civ: 'viking', enemies: 2 });
  ok(g.players[0].civ === 'viking' && CIVS[g.players[1].civ] && CIVS[g.players[2].civ], `single player: mine viking, AIs ${g.players[1].civ}, ${g.players[2].civ}`);
  const m = new Game({ ...base, mp: true, me: 0, players: [{ kind: 'human', team: 1, civ: 'roma' }, { kind: 'ai', team: 2, difficulty: 'normal', civ: 'random' }, { kind: 'ai', team: 2, difficulty: 'normal' }] });
  ok(m.players[0].civ === 'roma' && CIVS[m.players[1].civ] && !m.players[2].civ, 'multiplayer: per slot (id / random / none)');
  const cfg = NetSession.cfgFrom({ seed: 5, settings: {}, slots: [{ kind: 'human', peer: 'a', team: 1, name: 'A', civ: 'mogol' }, { kind: 'ai', team: 2, name: 'B' }, { kind: 'human', peer: 'b', team: 2, name: 'C', civ: '__proto__' }] }, 'a');
  ok(cfg.players[0].civ === 'mogol' && cfg.players[1].civ === 'random' && cfg.players[2].civ === 'random', 'lobby -> cfg: chosen kept, missing / forged become random');
}

// --- effects
{
  const none = new Game({ ...base }), roma = new Game({ ...base, civ: 'roma' });
  const hp = (g, t) => g._uMaxHp(t, 0);
  const rf = CIVS.roma.fx.hp, tg = CIVS.turk.fx.gather.gold;
  ok(rf.infantry > 0 && rf.spearman > 0 && hp(roma, 'swordsman') === Math.round(UNITS.swordsman.hp * (1 + rf.infantry)) && hp(roma, 'spearman') === Math.round(UNITS.spearman.hp * (1 + rf.infantry + rf.spearman)) && hp(roma, 'archer') === hp(none, 'archer'), `roma: infantry hp (${hp(none, 'swordsman')} -> ${hp(roma, 'swordsman')}), spearman class + type (${hp(none, 'spearman')} -> ${hp(roma, 'spearman')}), archers unchanged`);
  ok(roma._bMaxHp('house', 0) > none._bMaxHp('house', 0), 'roma: buildings are tougher');
  const turk = new Game({ ...base, civ: 'turk' });
  ok(tg > 0 && Math.abs(turk.players[0].mods.gather.gold - (1 + tg)) < 1e-9 && turk.players[0].mods.gather.food === 1 && turk.players[1].civ !== undefined, 'turk: gold gathering x' + (1 + tg) + ', food untouched');
  // a tech on top of a civilization bonus adds up
  turk.players[0].techs.add('pickaxe'); turk._mods(turk.players[0]);
  ok(Math.abs(turk.players[0].mods.gather.gold - (1.25 + tg)) < 1e-9, 'civilization bonus + tech add up (gold ' + (1.25 + tg).toFixed(2) + ')');
  // gold for a kill
  const vik = new Game({ ...base, civ: 'viking' }), p0 = vik.players[0];
  const victim = vik.units.find(u => u.owner === 1), mine = vik.units.find(u => u.owner === 0), own = vik.units.filter(u => u.owner === 0)[1];
  const g0 = p0.res.gold; vik._kill(victim, mine);
  ok(CIVS.viking.fx.killGold > 0 && p0.res.gold === g0 + CIVS.viking.fx.killGold, `viking: +${CIVS.viking.fx.killGold} gold for an enemy unit (${g0} -> ${p0.res.gold})`);
  const g1 = p0.res.gold; vik._kill(own, mine);
  ok(p0.res.gold === g1, 'viking: nothing for killing your own unit');
}

// --- unique units: one per civilization, replacing a standard unit
{
  const bad = [], ids = new Set();
  for (const id of CIV_IDS) {
    const u = UNITS[CIVS[id].unit];
    if (!u) { bad.push(id + ': no unique unit'); continue; }
    const b = UNITS[u.base];
    if (ids.has(u.id)) bad.push(id + ': id used twice'); ids.add(u.id);
    if (u.civ !== id || !b || b.civ) bad.push(id + ': civ / base');
    if (!u.name || !u.desc || u.name === b.name) bad.push(id + ': name / text');
    if (u.cls !== b.cls || u.age !== b.age) bad.push(id + ': class and age must be the base unit\'s');
    if (!(u.hp > 0 && u.atk > 0 && u.speed > 0 && u.rof > 0 && u.time > 0 && Object.keys(u.cost).length)) bad.push(id + ': numbers');
    if (u.range > 0 && !u.proj) bad.push(id + ': a ranged unit needs a projectile');
    if (civUnit(id, u.base) !== u.id || civUnit(id, 'villager') !== 'villager' || civUnit(null, u.base) !== u.base) bad.push(id + ': swap');
    if (!civLines(id).some(l => l.includes(u.name))) bad.push(id + ': not in the bonus text');
  }
  ok(!bad.length, CIV_IDS.length + ' unique units: data' + (bad.length ? ' - ' + bad.join('; ') : ''));
  // training the standard unit gives the unique one (also when the AI asks for the standard name); others get the standard one
  const g = new Game({ ...base, startAge: 2, startRes: 'high', mp: true, me: 0, players: [{ kind: 'human', team: 1, civ: 'roma' }, { kind: 'human', team: 2, civ: 'mogol' }, { kind: 'human', team: 3 }] });
  const got = [];
  for (const pid of [0, 1, 2]) {
    const p = g.players[pid]; Object.assign(p.res, { food: 5000, wood: 5000, gold: 5000, stone: 5000 }); p.popCap = 50;
    const bar = g._addBuilding('barracks', pid, Math.round(p.startX) + 8, Math.round(p.startZ) + 8, true), stb = g._addBuilding('stable', pid, Math.round(p.startX) - 12, Math.round(p.startZ) + 8, true);
    const gold0 = p.res.gold, food0 = p.res.food;
    const a = g.train(bar.id, 'swordsman'), b2 = g.train(stb.id, 'lightcav');
    got.push([a && bar.queue[0].id, b2 && stb.queue[0].id, food0 - p.res.food, gold0 - p.res.gold].join(':'));
  }
  const sw = UNITS.swordsman.cost, lc = UNITS.lightcav.cost, lj = UNITS.lejyoner.cost, mg = UNITS.mangudai.cost;
  ok(got[0] === ['lejyoner', 'lightcav', lj.food + lc.food, lj.gold + lc.gold].join(':'), 'roma trains Lejyoner for swordsman, pays its cost: ' + got[0]);
  ok(got[1] === ['swordsman', 'mangudai', sw.food + mg.food, sw.gold + mg.gold].join(':'), 'mogol trains Mangudai for lightcav: ' + got[1]);
  ok(got[2] === ['swordsman', 'lightcav', sw.food + lc.food, sw.gold + lc.gold].join(':'), 'no civilization: standard units');
  ok(!g.train(g.buildings.find(b => b.owner === 0 && b.type === 'barracks').id, 'mangudai') && !Object.values(BUILDINGS).some(b => b.trains.includes('lejyoner')), 'a unique unit cannot be asked for directly from the wrong building');
  // they come out, fight and keep both sides in sync
  for (let t = 0; t < 30 * 60; t++) g.update(1 / 30);
  const types = new Set(g.units.map(u => u.type));
  ok(types.has('lejyoner') && types.has('mangudai'), 'the unique units are produced');
  const lej = g.units.find(u => u.type === 'lejyoner'), man = g.units.find(u => u.type === 'mangudai');
  ok(lej.maxHp === Math.round(UNITS.lejyoner.hp * (1 + CIVS.roma.fx.hp.infantry)) && lej.maxHp > UNITS.lejyoner.hp, 'the civilization bonus applies to its unique unit (Lejyoner hp ' + lej.maxHp + ')');
  // a mounted archer shoots from range
  const foe = g.units.find(u => u.owner === 0 && u.type === 'lejyoner'), hp0 = foe.hp;
  man.x = foe.x + 3; man.z = foe.z; foe.stance = 'hold';
  g.cmdAttack([man.id], foe.id);
  let shot = false; for (let t = 0; t < 30 * 8 && !shot; t++) { g.update(1 / 30); if (g.projectiles.length) shot = true; }
  ok(shot, 'Mangudai attacks with a projectile from range');
}

// --- AI: play style and unit taste per civilization
{
  const bad = [];
  for (const id of CIV_IDS) { if (!AI_STYLES[CIVS[id].style]) bad.push(id + ': style ' + CIVS[id].style); if (!civRoleBias(id) || !Object.keys(civRoleBias(id)).length) bad.push(id + ': no unit taste'); }
  ok(!bad.length && new Set(CIV_IDS.map(civStyle)).size >= 4, 'every civilization has an AI style and a unit taste' + (bad.length ? ' - ' + bad.join('; ') : ''));
  const g = new Game({ ...base, mp: true, me: 0, players: [{ kind: 'ai', team: 1, difficulty: 'hard', civ: 'mogol' }, { kind: 'ai', team: 2, difficulty: 'hard', civ: 'kore' }, { kind: 'ai', team: 3, difficulty: 'hard' }, { kind: 'ai', team: 4, difficulty: 'hard', civ: 'turk' }] });
  const [mo, ko, no, tu] = g.ais.map(a => a.d);
  ok(mo.raidFrom < no.raidFrom && mo.pushFrom < no.pushFrom && mo.army[1] > no.army[1], `raider (mogol): attacks earlier (raid ${mo.raidFrom} < ${no.raidFrom} min), more army`);
  ok(ko.towers[2] > no.towers[2] && ko.wallFrom < no.wallFrom && ko.pushFrom > no.pushFrom, `defender (kore): more towers (${ko.towers[2]} > ${no.towers[2]}), walls earlier, pushes later`);
  ok(tu === no && g.ais[2].roleBias === null && g.ais[3].roleBias && g.ais[0].roleBias.cav > 1, 'balanced style / no civilization: the plain difficulty row; unit taste only with a civilization');
  ok(tuneDiff('hard', no, 'mogol') === mo && JSON.stringify(tuneDiff('hard', no, 'mogol')) === JSON.stringify(mo) && Number.isInteger(mo.raidSize) && mo.towers.every(t => t >= 0), 'tuning is cached, repeatable and keeps whole numbers whole');
  const off = new Game({ ...base, noCivAi: true, mp: true, me: 0, players: [{ kind: 'ai', team: 1, difficulty: 'hard', civ: 'mogol' }, { kind: 'ai', team: 2, difficulty: 'hard' }] });
  ok(off.ais[0].d === off.ais[1].d && off.ais[0].roleBias === null, 'cfg.noCivAi switches it off');
  // a saved match restores the same style
  for (let t = 0; t < 30 * 20; t++) g.update(1 / 30);
  const c = Game.deserialize(JSON.parse(JSON.stringify(g.serialize())));
  ok(c.ais[0].d.raidFrom === mo.raidFrom && c.ais[1].d.wallFrom === ko.wallFrom && c.ais[0].roleBias.cav === g.ais[0].roleBias.cav && c.hash() === g.hash(), 'save / load keeps the AI style');
}

// --- save / load keeps the civilization and its mods; two runs stay in sync
{
  const mk = () => new Game({ ...base, civ: 'mogol', enemies: 2 });
  const a = mk(), b = mk();
  for (let t = 0; t < 30 * 90; t++) { a.update(1 / 30); b.update(1 / 30); }
  ok(a.hash() === b.hash(), 'two runs with civilizations: same hash after 90 s');
  const c = Game.deserialize(JSON.parse(JSON.stringify(a.serialize())));
  ok(c.players.map(p => p.civ).join() === a.players.map(p => p.civ).join() && c.players[0].mods.killGold === CIVS.mogol.fx.killGold && c.hash() === a.hash(), 'save / load: civilizations, mods and hash survive');
}

console.log(fails.length ? 'FAILED: ' + fails.length : 'ALL OK');
process.exit(fails.length ? 1 : 0);
