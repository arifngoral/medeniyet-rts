// Civilizations: every player may pick one; its passive bonuses (fx) are folded into the player's mods like a tech
// that is researched from the start (Game._mods). Pure data + helpers, no DOM / three (the simulation imports this).
// The table itself is generated (civ-data.js).
import { CIV_DATA } from './civ-data.js';
import { UNITS } from './data.js';
import { CIV_UNITS } from './civ-units.js';
import { LANDMARKS, HEROES } from './landmarks.js';   // (also puts the age-up buildings and heroes into data.js's tables)

export const CIVS = CIV_DATA;
export const CIV_IDS = Object.keys(CIVS);   // order = the table's order (the same on every client)

// Unique units (civ-units.js, two per civilization) become ordinary entries of UNITS: the base unit's definition with the
// changes applied, plus civ (whose it is), base (what it replaces), kit (its look) and look (its shots, view only).
// Done once, when this module loads - before the simulation, the icons or the renderer read UNITS. Not in any
// building's trains list: train() swaps the type. CIVS[civ].units = their ids (in order), .unit = the first one.
const r2 = v => Math.round(v * 100) / 100;
const SWAP = {};
for (const civ of CIV_IDS) {
  CIVS[civ].units = [];
  for (const u of CIV_UNITS[civ] || []) {
    const b = UNITS[u.base]; if (!b || b.civ || UNITS[u.id]) throw new Error('civ unit ' + civ + ': bad base or id ' + u.id);
    if (SWAP[civ + ':' + u.base]) throw new Error('civ unit ' + civ + ': two unique units for ' + u.base);
    const bonus = Object.assign({}, b.bonus, u.bonus); for (const k in bonus) if (bonus[k] === 1) delete bonus[k];
    UNITS[u.id] = Object.assign({}, b, {
      id: u.id, name: u.name, desc: u.desc, icon: u.icon || b.icon, civ, base: u.base, kit: u.kit || {}, look: u.look || '',
      hp: Math.round(b.hp * (u.hp || 1)), atk: Math.max(1, b.atk + (u.atk || 0)), armor: Math.max(0, b.armor + (u.armor || 0)),
      speed: r2(b.speed * (u.speed || 1)), range: Math.max(0, b.range + (u.range || 0)), rof: r2(b.rof * (u.rof || 1)),
      time: Math.max(5, b.time + (u.time || 0)), cost: Object.assign({}, u.cost || b.cost), pop: u.pop || b.pop, bonus, proj: u.proj || b.proj,
    });
    CIVS[civ].units.push(u.id);
    SWAP[civ + ':' + u.base] = u.id;
  }
  CIVS[civ].unit = CIVS[civ].units[0];
}
// the unit a player of that civilization gets when it trains `type` (its unique unit instead of the base; else the same)
export const civUnit = (civ, type) => (civ && SWAP[civ + ':' + type]) || type;

// What a cfg entry means: a civ id -> that civ; 'random' -> picked from the match seed and the player index only
// (deterministic, does not touch the simulation's rng); anything else (missing, old saves, tests) -> no civilization.
export function resolveCiv(want, seed, i) {
  if (CIVS[want]) return want;
  if (want !== 'random') return null;
  let h = (Math.imul(seed | 0, 374761393) + Math.imul(i + 1, 668265263) + 1013904223) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177); h = (h ^ (h >>> 16)) >>> 0;
  return CIV_IDS[h % CIV_IDS.length];
}

const CLS_TR = { infantry: 'Piyade', ranged: 'Menzilli', cavalry: 'Süvari', siege: 'Kuşatma', ship: 'Gemi', spearman: 'Mızrakçı' };
const RES_TR = { food: 'Yiyecek', wood: 'Odun', stone: 'Taş', gold: 'Altın' };
const pct = v => '+%' + Math.round(v * 100);
const each = (o, tr, f) => Object.entries(o).map(([k, v]) => f(tr[k] || k, v));
// one line of text per bonus, written from the numbers (so the text can never disagree with the effect)
const LINE = {
  hp: o => each(o, CLS_TR, (n, v) => `${n} canı ${pct(v)}`),
  atkMul: o => each(o, CLS_TR, (n, v) => `${n} saldırısı ${pct(v)}`),
  atk: o => each(o, CLS_TR, (n, v) => `${n} saldırısı +${v}`),
  armor: o => each(o, CLS_TR, (n, v) => `${n} zırhı +${v}`),
  range: o => each(o, CLS_TR, (n, v) => `${n} menzili +${v}`),
  speed: o => each(o, CLS_TR, (n, v) => `${n} hızı ${pct(v)}`),
  gather: o => each(o, RES_TR, (n, v) => `${n} toplama ${pct(v)}`),
  farm: v => [`Tarla verimi ${pct(v)}`],
  pasture: v => [`Ağıl verimi ${pct(v)}`],
  bhp: v => [`Bina dayanıklılığı ${pct(v)}`],
  wallhp: v => [`Sur ve kapı dayanıklılığı ${pct(v)}`],
  towerAtk: v => [`Kule ve kale saldırısı +${v}`],
  towerRange: v => [`Kule ve kale menzili +${v}`],
  train: v => [`Birlik üretimi %${Math.round(v * 100)} daha hızlı`],
  trade: v => [`Pazar takas oranı ${pct(v)}`],
  cart: v => [`Ticaret arabası kazancı ${pct(v)}`],
  killGold: v => [`Öldürülen her düşman birliği için +${v} altın`],
};
export function civLines(id) {
  const c = CIVS[id]; if (!c) return [];
  const out = [];
  for (const k in c.fx) out.push(...(LINE[k] ? LINE[k](c.fx[k]) : [k]));
  for (const id of c.units || []) if (UNITS[id]) out.push(`Özel birlik: ${UNITS[id].name} (${UNITS[UNITS[id].base].name} yerine)`);
  if (LANDMARKS[id]) out.push('Çağ atlama: köylüler her çağ için iki binadan birini kurar (AoE4 gibi)');
  if (HEROES[id] && UNITS[HEROES[id].id]) out.push(`Efsane: ${UNITS[HEROES[id].id].name} (çağ binalarından)`);
  return out;
}
export const civLabel = id => (CIVS[id] ? CIVS[id].icon + ' ' + CIVS[id].name : '');
