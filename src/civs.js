// Civilizations: every player may pick one; its passive bonuses (fx) are folded into the player's mods like a tech
// that is researched from the start (Game._mods). Pure data + helpers, no DOM / three (the simulation imports this).
// The table itself is generated (civ-data.js).
import { CIV_DATA } from './civ-data.js';

export const CIVS = CIV_DATA;
export const CIV_IDS = Object.keys(CIVS);   // order = the table's order (the same on every client)

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
  return out;
}
export const civLabel = id => (CIVS[id] ? CIVS[id].icon + ' ' + CIVS[id].name : '');
