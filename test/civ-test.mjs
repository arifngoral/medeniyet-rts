// Civilizations: data shape, bonuses reach the simulation, deterministic. Run from ROOT: node test/civ-test.mjs
import { UNITS } from '../src/data.js';
import { CIVS, CIV_IDS, resolveCiv, civLines } from '../src/civs.js';
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
  ok(hp(roma, 'swordsman') === Math.round(UNITS.swordsman.hp * 1.16) && hp(roma, 'spearman') === Math.round(UNITS.spearman.hp * 1.32) && hp(roma, 'archer') === hp(none, 'archer'), `roma: infantry hp (${hp(none, 'swordsman')} -> ${hp(roma, 'swordsman')}), spearman class + type (${hp(none, 'spearman')} -> ${hp(roma, 'spearman')}), archers unchanged`);
  ok(roma._bMaxHp('house', 0) > none._bMaxHp('house', 0), 'roma: buildings are tougher');
  const turk = new Game({ ...base, civ: 'turk' });
  ok(Math.abs(turk.players[0].mods.gather.gold - 1.1) < 1e-9 && turk.players[0].mods.gather.food === 1 && turk.players[1].civ !== undefined, 'turk: gold gathering x1.1, food untouched');
  // a tech on top of a civilization bonus adds up
  turk.players[0].techs.add('pickaxe'); turk._mods(turk.players[0]);
  ok(Math.abs(turk.players[0].mods.gather.gold - 1.35) < 1e-9, 'civilization bonus + tech add up (gold 1.35)');
  // gold for a kill
  const vik = new Game({ ...base, civ: 'viking' }), p0 = vik.players[0];
  const victim = vik.units.find(u => u.owner === 1), mine = vik.units.find(u => u.owner === 0), own = vik.units.filter(u => u.owner === 0)[1];
  const g0 = p0.res.gold; vik._kill(victim, mine);
  ok(p0.res.gold === g0 + 8, `viking: +8 gold for an enemy unit (${g0} -> ${p0.res.gold})`);
  const g1 = p0.res.gold; vik._kill(own, mine);
  ok(p0.res.gold === g1, 'viking: nothing for killing your own unit');
}

// --- save / load keeps the civilization and its mods; two runs stay in sync
{
  const mk = () => new Game({ ...base, civ: 'mogol', enemies: 2 });
  const a = mk(), b = mk();
  for (let t = 0; t < 30 * 90; t++) { a.update(1 / 30); b.update(1 / 30); }
  ok(a.hash() === b.hash(), 'two runs with civilizations: same hash after 90 s');
  const c = Game.deserialize(JSON.parse(JSON.stringify(a.serialize())));
  ok(c.players.map(p => p.civ).join() === a.players.map(p => p.civ).join() && c.players[0].mods.killGold === 4 && c.hash() === a.hash(), 'save / load: civilizations, mods and hash survive');
}

console.log(fails.length ? 'FAILED: ' + fails.length : 'ALL OK');
process.exit(fails.length ? 1 : 0);
