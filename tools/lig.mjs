// Civilization balance league: AI against AI, 1v1, each civilization against an opponent WITHOUT a civilization
// (the baseline). Every seed is played twice with the sides swapped, so the map and the first-player edge cancel out;
// a civilization that is exactly as strong as none wins 50 %.
//   node tools/lig.mjs                      all civilizations, 40 seeds (= 80 matches) each, ~15-20 min on 12 cores
//   node tools/lig.mjs --seeds 20 --only roma,mogol
//   node tools/lig.mjs --no-unit            passives only (unique units off)      --no-fx   unique units only
//   node tools/lig.mjs --no-ai              the AI ignores its civilization's play style and unit taste (civ-ai.js)
//   node tools/lig.mjs --vs roma            against that civilization instead of the baseline
//   node tools/lig.mjs --rr                 round robin: every civilization against every other (target ~50 % each);
//                                           --seeds N = maps per pair (default 2: 4 matches per pair, 76 per civilization)
//   node tools/lig.mjs --set fx.roma.bhp=0.05 --set unit.fil.hp=220 --set unit.mangudai.cost.gold=30
//   other: --diff easy|normal|hard (hard)  --size 96  --cap 60 (minutes; an unfinished match is a draw = half a win)
//          --maps plains,river,highlands  --jobs N
// Target: 44-56 % (also for --rr, against the others). One run of 80 matches has a standard error of about 5.5 points: decide on repeated / larger runs.
import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i < 0 ? d : process.argv[i + 1]; };
const flag = k => process.argv.includes('--' + k);
const all = k => process.argv.flatMap((a, i) => (a === '--' + k ? [process.argv[i + 1]] : []));

async function setup(sets) {
  const { CIVS, CIV_IDS } = await import('../src/civs.js');
  const { UNITS } = await import('../src/data.js');
  // --set fx.<civ>.<path>=n  |  unit.<unitId>.<path>=n
  for (const s of sets) {
    const [path, val] = s.split('='), ks = path.split('.'), kind = ks.shift(), id = ks.shift();
    let o = kind === 'fx' ? CIVS[id] && CIVS[id].fx : kind === 'unit' ? UNITS[id] : null;
    if (!o) throw new Error('--set: unknown ' + path);
    while (ks.length > 1) { const k = ks.shift(); o = o[k] || (o[k] = {}); }
    if (val === 'del') delete o[ks[0]]; else o[ks[0]] = Number(val);
  }
  return { CIVS, CIV_IDS, UNITS };
}

if (!isMainThread) {
  const { sets, opt } = workerData;
  await setup(sets);
  const { Game } = await import('../src/sim/game.js');
  parentPort.on('message', (m) => {
    // m: {civ, seed, side}: the civilization plays player `side`, the opponent the other one
    const players = [0, 1].map(i => ({ kind: 'ai', team: i + 1, difficulty: opt.diff, civ: i === m.side ? m.civ : (m.opp !== undefined ? m.opp : opt.vs) }));
    const g = new Game({ mapSize: opt.size, seed: m.seed, mp: true, me: 0, startRes: 'normal', startAge: 0, mapType: opt.maps[m.seed % opt.maps.length], players, noCivUnit: opt.noUnit, noCivFx: opt.noFx, noCivAi: opt.noAi });
    const MAX = 30 * 60 * opt.cap; let t = 0;
    while (!g.over && t < MAX) { g.update(1 / 30); t++; }
    const w = g.over ? g.over.winnerTeam : 0;   // 1 / 2, 0 = not finished, -1 = nobody
    parentPort.postMessage({ civ: m.civ, opp: m.opp, res: w === m.side + 1 ? 1 : w === 2 - m.side ? 0 : 0.5, min: t / 1800 });
  });
} else {
  const sets = all('set');
  const { CIV_IDS } = await setup(sets);
  const only = arg('only', ''), civs = only ? only.split(',').filter(c => CIV_IDS.includes(c)) : CIV_IDS;
  const rr = flag('rr'), seeds = +arg('seeds', rr ? 2 : 40), jobs = Math.max(1, +arg('jobs', Math.max(1, os.cpus().length - 2)));
  const vs = arg('vs', '') || undefined;
  if (vs && !CIV_IDS.includes(vs)) throw new Error('--vs: unknown civilization ' + vs);
  const opt = { diff: arg('diff', 'hard'), size: +arg('size', 96), cap: +arg('cap', 60), maps: arg('maps', 'plains,river,highlands').split(','), vs, noUnit: flag('no-unit'), noFx: flag('no-fx'), noAi: flag('no-ai') };
  const work = [];
  if (rr) { for (let a = 0; a < civs.length; a++) for (let b = a + 1; b < civs.length; b++) for (let s = 0; s < seeds; s++) for (const side of [0, 1]) work.push({ civ: civs[a], opp: civs[b], seed: 1000 + s * 7 + a * 131 + b * 17, side }); }
  else for (const civ of civs) for (let s = 0; s < seeds; s++) for (const side of [0, 1]) work.push({ civ, seed: 1000 + s * 7, side });
  const R = Object.fromEntries(civs.map(c => [c, { n: 0, w: 0, d: 0, min: 0 }]));
  const t0 = Date.now(); let done = 0, next = 0;
  console.log((rr ? `round robin: ${civs.length} civilizations, ${work.length} matches (${seeds * 2} per pair)` : `${civs.length} civilizations x ${seeds * 2} matches against ${vs || 'no civilization'}`) + `; ${jobs} workers` + (opt.noUnit ? '; unique units OFF' : '') + (opt.noFx ? '; passives OFF' : '') + (sets.length ? '; ' + sets.join(' ') : ''));
  await new Promise((resolve) => {
    for (let j = 0; j < Math.min(jobs, work.length); j++) {
      const w = new Worker(fileURLToPath(import.meta.url), { workerData: { sets, opt } });
      const give = () => { if (next < work.length) w.postMessage(work[next++]); else w.terminate(); };
      w.on('message', (m) => {
        const r = R[m.civ]; r.n++; r.w += m.res; if (m.res === 0.5) r.d++; r.min += m.min;
        if (m.opp && R[m.opp]) { const q = R[m.opp]; q.n++; q.w += 1 - m.res; if (m.res === 0.5) q.d++; q.min += m.min; }   // (round robin: the match counts for both)
        if (++done % 100 === 0) process.stderr.write(`  ${done}/${work.length}  (${((Date.now() - t0) / 60000).toFixed(1)} min)\n`);
        if (done === work.length) resolve(); else give();
      });
      w.on('error', (e) => { console.error(e); process.exit(1); });
      give();
    }
  });
  const rows = civs.map(c => ({ c, p: 100 * R[c].w / R[c].n, ...R[c] })).sort((a, b) => b.p - a.p);
  console.log('\ncivilization   win %   matches  draws  avg min');
  for (const r of rows) console.log(`${r.c.padEnd(13)} ${r.p.toFixed(1).padStart(5)} ${r.p > 56 ? '▲' : r.p < 44 ? '▼' : ' '} ${String(r.n).padStart(7)} ${String(r.d).padStart(6)} ${(r.min / r.n).toFixed(1).padStart(8)}`);
  const se = 50 / Math.sqrt(rows.reduce((t, r) => t + r.n, 0) / rows.length);   // (one row's matches)
  console.log(`\nmean ${(rows.reduce((s, r) => s + r.p, 0) / rows.length).toFixed(1)} %; one row's standard error ~${se.toFixed(1)} points; ${((Date.now() - t0) / 60000).toFixed(1)} min`);
  process.exit(0);
}
