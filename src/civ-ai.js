// How an AI plays its civilization: a play style (when it attacks, how much economy / defence it keeps) and a taste for
// the unit classes its civilization is good at. Both only re-weight the difficulty table and the army mix of ai.js: the
// AI still plays by the same rules, and an AI without a civilization plays exactly as before.
// Pure functions of (difficulty table, civilization): the same on every client, no randomness.
import { UNITS } from './data.js';
import { CIVS } from './civs.js';

// Changes to a difficulty row (ai.js DIFF): mul multiplies, add adds; arrays (one value per age) element by element.
//   raidFrom / pushFrom  minute of the first raid / push      raidGap / pushGap  seconds between them
//   vill  villager targets   army  share of the population that is army   ageVill  villagers needed to age up
//   towers / towersX / wallFrom / wallTowers  defences        carts / banks  trade   techPar  parallel research
export const AI_STYLES = {
  dengeli: { name: 'Dengeli', text: 'Duruma göre oynar.' },
  baskinci: { name: 'Baskıncı', text: 'Erken ve sık saldırır, savunmaya az yatırır.',
    mul: { raidFrom: 0.7, pushFrom: 0.75, raidGap: 0.75, pushGap: 0.8, vill: 0.93, wallFrom: 1.5 }, add: { raidSize: 1, army: 0.06, towers: -1 } },
  ekonomist: { name: 'Ekonomist', text: 'Önce ekonomiyi büyütür, çağ atlar; geç ama kalabalık gelir.',
    mul: { vill: 1.1, ageVill: 0.93, raidFrom: 1.2, pushFrom: 1.2 }, add: { carts: 2, banks: 1, techPar: 1, army: -0.04 } },
  savunmaci: { name: 'Savunmacı', text: 'Sur ve kule örer, ordusu toplanmadan çıkmaz.',
    mul: { wallFrom: 0.7, raidFrom: 1.3, pushFrom: 1.25, pushBase: 1.15 }, add: { towers: 1, towersX: 1, wallTowers: 2, minArmy: 1 } },
  taktikci: { name: 'Taktikçi', text: 'Sık keşif yapar, rakibin ordusuna göre birlik seçer, araştırmaya önem verir.',
    mul: { rescout: 0.7, raidGap: 0.85, pushGap: 0.9, counter: 1.3 }, add: { techPar: 1, raidSize: 1 } },
};
export const civStyle = (civ) => (CIVS[civ] && AI_STYLES[CIVS[civ].style] ? CIVS[civ].style : 'dengeli');

const LIMIT = { army: [0.1, 0.9], towers: [0, 12], vill: [6, 200], ageVill: [6, 200] };
const tuneVal = (k, base, mul, add) => {
  const one = (v) => {
    let x = v * (mul == null ? 1 : mul) + (add || 0);
    if (LIMIT[k]) x = Math.max(LIMIT[k][0], Math.min(LIMIT[k][1], x));
    return Number.isInteger(v) && k !== 'counter' ? Math.round(x) : Math.round(x * 1000) / 1000;
  };
  return Array.isArray(base) ? base.map(one) : one(base);
};
const cache = new Map();
// the difficulty row an AI of that civilization plays with (the same object for the same pair; rows are never mutated)
export function tuneDiff(key, row, civ) {
  const st = AI_STYLES[civStyle(civ)];
  if (!st.mul && !st.add) return row;
  const ck = key + ':' + civStyle(civ);
  if (cache.has(ck)) return cache.get(ck);
  const out = Object.assign({}, row);
  for (const k of new Set([...Object.keys(st.mul || {}), ...Object.keys(st.add || {})])) {
    if (typeof row[k] !== 'number' && !Array.isArray(row[k])) continue;
    out[k] = tuneVal(k, row[k], st.mul && st.mul[k], st.add && st.add[k]);
  }
  cache.set(ck, out);
  return out;
}

// Army mix: weights for the roles of ai.js (pike / inf / gun / bow / cav / siege). The role of the unique unit counts
// most; the classes the civilization's passive bonuses help count a little.
const CLS_ROLES = { infantry: ['inf', 'pike'], ranged: ['bow', 'gun'], cavalry: ['cav'], siege: ['siege'], spearman: ['pike'] };
const BASE_ROLE = { spearman: 'pike', swordsman: 'inf', heavyinf: 'inf', musketeer: 'gun', rifleman: 'gun', archer: 'bow', crossbow: 'bow', lightcav: 'cav', knight: 'cav', cuirassier: 'cav' };
const UNIQUE_W = 1.5, BONUS_W = 1.2;
const biasCache = new Map();
export function civRoleBias(civ) {
  const c = CIVS[civ]; if (!c) return null;
  if (biasCache.has(civ)) return biasCache.get(civ);
  const b = {};
  for (const k of ['hp', 'atk', 'atkMul', 'armor', 'range', 'speed']) for (const cls in (c.fx[k] || {})) for (const r of CLS_ROLES[cls] || []) b[r] = BONUS_W;
  const u = c.unit && UNITS[c.unit], ur = u && BASE_ROLE[u.base];
  if (ur) b[ur] = UNIQUE_W;
  biasCache.set(civ, b);
  return b;
}
