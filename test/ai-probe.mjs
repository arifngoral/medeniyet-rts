// AI-vs-AI probe: node test/ai-probe.mjs [--min 45] [--seeds 1,2,3,4] [--diff easy,normal,hard] [--old path/to/old-ai.mjs] [--v]
//   --diff hard:easy    asymmetric match (P0 hard vs P1 easy); sides swap on every other seed so map side does not decide
//   --floor             "greedy" floor probe: both sides only do economy + required buildings + age-ups (no army)
//   --av 10,18,24,30    override the per-age villager minimum before the age-up (ageVill), for tuning
//   --dbg [seed]        print P0's decision state every minute (reserve, army target, production, blocks, canAgeUp reason)
// Prints per difficulty: minute each age was reached (and villagers / military at that moment), villagers /
// military / buildings / floating resources at fixed minutes, raids and pushes, kills / losses, winner.
import { Game } from '../src/sim/game.js';
import { AIController as NewAI } from '../src/sim/ai.js';
import { UNITS } from '../src/data.js';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const MIN = +opt('min', 45);
const SEEDS = opt('seeds', '1,2,3,4').split(',').map(Number);
const DIFFS = opt('diff', 'easy,normal,hard').split(',');
const OLD = opt('old', null);
const VERBOSE = args.includes('--v');
const FLOOR = args.includes('--floor');
const PEACE = args.includes('--peace'); // armies are built but nobody raids or pushes: isolates economic tempo
const AV = opt('av', null);
const DBG = args.includes('--dbg') ? (() => { const v = opt('dbg', null); return v && !v.startsWith('--') ? +v : SEEDS[0]; })() : null;
const SNAP = [5, 10, 20, 30, 40, 50, 60].filter(m => m <= MIN);

let AI = NewAI;
if (OLD) AI = (await import(pathToFileURL(OLD).href)).AIController;

const isMil = u => { const d = UNITS[u.type]; return d && d.cls !== 'civil' && d.cls !== 'train' && !d.naval; };

function runGame(diffs, seed) {
  const g = new Game({ mapSize: 96, enemies: 1, difficulty: diffs[1], startRes: 'normal', startAge: 0, sandbox: false, seed });
  const ais = [new AI(g, 0, diffs[0]), new AI(g, 1, diffs[1])];
  for (const a of ais) {
    if (FLOOR) { a.d = { ...a.d, ecoOnly: true, army: [0, 0, 0, 0, 0], minArmy: [0, 0, 0, 0, 0], towers: [0, 0, 0, 0, 0], castle: false, prod: [0, 0, 0, 0, 0], idleChance: 0 }; a.nextRaid = a.nextPush = Infinity; }
    if (AV) a.d = { ...a.d, ageVill: AV.split(',').map(Number) };
    if (PEACE) a.nextRaid = a.nextPush = Infinity;
  }
  if (DBG === seed) ais[0].debug = true;
  // the tutorial quests reward player 0 only (a human-side feature): off, so both AI sides play by the same rules
  g.quests = { list: [], update() {}, serialize() { return null; }, load() {} };
  g.ais.length = 0; g.ais.push(...ais);
  let thinkMs = 0, thinks = 0;
  for (const a of ais) { const th = a.think.bind(a); a.think = (...x) => { const t0 = performance.now(); try { return th(...x); } finally { thinkMs += performance.now() - t0; thinks++; } }; }
  const P = [0, 1];
  const ageAt = P.map(() => [0, null, null, null, null]);
  const ageVM = P.map(() => [null, null, null, null, null]); // villagers / military at each age-up click... and completion
  g.events.on('ageUpStart', p => { const k = p.owner, a = g.players[k].age + 1; if (ageVM[k] && !ageVM[k][a]) { const us = g.unitsOf(k); ageVM[k][a] = { v: us.filter(u => u.type === 'villager').length, m: us.filter(isMil).length, click: g.time / 60 }; } });
  g.events.on('ageUp', p => { if (ageAt[p.owner] && ageAt[p.owner][p.age] == null) ageAt[p.owner][p.age] = g.time / 60; });
  const snaps = P.map(() => ({}));
  let idleSum = 0, idleN = 0, villSum = 0;
  const dt = 1 / 30, steps = Math.round(MIN * 60 / dt);
  const t0 = performance.now();
  let i = 0, nextDbg = 60;
  for (; i < steps && !g.over; i++) {
    g.update(dt);
    if (i % 300 === 0 && g.time > 30) {
      for (const p of P) { const vs = g.unitsOf(p).filter(u => u.type === 'villager'); villSum += vs.length; idleSum += vs.filter(u => !u.order).length; idleN++; }
    }
    if (ais[0].debug && g.time >= nextDbg) {
      nextDbg += 60;
      const di = ais[0].dbgInfo || {}, pl = g.players[0];
      const res = ['food', 'wood', 'stone', 'gold'].map(k => Math.round(pl.res[k] || 0)).join('/');
      console.log(`  [dbg s${seed} ${diffs[0]} ${String(Math.round(g.time / 60)).padStart(2)}m] age${pl.age} ${di.phase} vil ${di.vills}/${di.villCap} mil ${di.mil}/${di.armyT} (minDef ${di.minDef} boost ${di.floatBoost}${di.threatened ? ' THREAT' : ''}) prod ${di.prod} idle ${di.prodIdle} q[${di.q}] tcQ[${di.tcQ}] types ${di.types} pendB ${di.pendingB} | res ${res} R ${JSON.stringify(di.reserve)} shop ${JSON.stringify(di.shop)} | blk ${di.blocked} | ageUp: ${di.age} | techs ${di.techs}+${di.pending} | grp ${di.groups} ${di.extra}`);
    }
    const m = g.time / 60;
    for (const s of SNAP) {
      if (m >= s && snaps[0][s] == null) {
        for (const p of P) {
          const pl = g.players[p], us = g.unitsOf(p);
          snaps[p][s] = { vil: us.filter(u => u.type === 'villager').length, mil: us.filter(isMil).length, bld: g.buildingsOf(p).filter(b => b.type !== 'wall' && b.type !== 'rail').length,
            float: Math.round((pl.res.food || 0) + (pl.res.wood || 0) + (pl.res.stone || 0) + (pl.res.gold || 0)), res: { ...pl.res }, age: pl.age };
        }
      }
    }
  }
  const wall = performance.now() - t0;
  const res = P.map(p => {
    const pl = g.players[p], a = ais[p], st = a.stats || {};
    return { diff: diffs[p], ageAt: ageAt[p], ageVM: ageVM[p], snaps: snaps[p], raids: st.raids != null ? st.raids : 0, pushes: st.pushes != null ? st.pushes : (a.waveCount || 0),
      firstRaid: st.firstRaid, firstPush: st.firstPush,
      kills: pl.stats.kills, lost: pl.stats.unitsLost, razed: pl.stats.razed, defeated: pl.defeated, errors: a.errors || null, age: pl.age };
  });
  return { diffs, seed, res, over: g.over, endMin: g.time / 60, idle: idleN ? idleSum / idleN : 0, idleFrac: villSum ? idleSum / villSum : 0, msThink: thinks ? thinkMs / thinks : 0, thinks, wall };
}

const f1 = v => v == null ? '  -  ' : v.toFixed(1).padStart(5);
const avg = a => { const b = a.filter(x => x != null); return b.length ? b.reduce((s, x) => s + x, 0) / b.length : null; };

console.log(`AI probe: ${OLD ? 'OLD ' + OLD : 'NEW src/sim/ai.js'}${FLOOR ? ' FLOOR (eco only)' : ''}${PEACE ? ' PEACE (no raids / pushes)' : ''}${AV ? ' ageVill ' + AV : ''} | 96 map, seeds ${SEEDS.join(',')}, ${MIN} min, dt 1/30`);
for (const spec of DIFFS) {
  const pair = spec.includes(':') ? spec.split(':') : [spec, spec];
  const asym = pair[0] !== pair[1];
  // asymmetric: alternate which map side the first difficulty plays
  const games = SEEDS.map((s, k) => runGame(asym && k % 2 ? [pair[1], pair[0]] : pair, s));
  console.log(`\n=== ${asym ? pair[0].toUpperCase() + ' vs ' + pair[1].toUpperCase() : spec.toUpperCase()} (${games.length * 2} AI sides) ===`);
  for (const g of games) {
    const w = g.res[0].defeated ? `P1 (${g.res[1].diff}) won` : g.res[1].defeated ? `P0 (${g.res[0].diff}) won` : 'no winner';
    console.log(`  seed ${g.seed}: end ${g.endMin.toFixed(1)}m ${w} | ages P0 [${g.res[0].ageAt.slice(1).map(f1).join(' ')}] P1 [${g.res[1].ageAt.slice(1).map(f1).join(' ')}] | raids ${g.res.map(r => r.raids).join('/')} (1st ${g.res.map(r => r.firstRaid != null ? (r.firstRaid / 60).toFixed(1) : '-').join('/')}) pushes ${g.res.map(r => r.pushes).join('/')} (1st ${g.res.map(r => r.firstPush != null ? (r.firstPush / 60).toFixed(1) : '-').join('/')}) | kills ${g.res.map(r => r.kills).join('/')} lost ${g.res.map(r => r.lost).join('/')} razed ${g.res.map(r => r.razed).join('/')} | idle vil ${(g.idleFrac * 100).toFixed(1)}% | ${g.msThink.toFixed(2)} ms/think, wall ${(g.wall / 1000).toFixed(1)} s`);
    if (VERBOSE) for (const r of g.res) if (r.errors && Object.keys(r.errors).length) console.log('    errors:', JSON.stringify(r.errors));
  }
  for (const diff of asym ? pair : [pair[0]]) {
    const sides = games.flatMap(g => g.res).filter(r => r.diff === diff);
    const tag = asym ? ` [${diff}]` : '';
    const ageLine = [1, 2, 3, 4].map(a => { const v = sides.map(s => s.ageAt[a]); const n = v.filter(x => x != null).length; return `age${a} ${f1(avg(v))}m (${n}/${sides.length})`; }).join(' | ');
    console.log(`  reached${tag} (avg min):`, ageLine);
    const vmLine = [1, 2, 3, 4].map(a => { const v = sides.map(s => s.ageVM[a]).filter(Boolean); return v.length ? `age${a} click ${avg(v.map(x => x.click)).toFixed(1)}m vil ${avg(v.map(x => x.v)).toFixed(0)} mil ${avg(v.map(x => x.m)).toFixed(0)}` : `age${a} -`; }).join(' | ');
    console.log(`  at age-up click${tag}:`, vmLine);
    console.log(`  min |  vil   mil   bld | float (f/w/s/g)${tag}`);
    for (const s of SNAP) {
      const v = k => avg(sides.map(x => x.snaps[s] ? x.snaps[s][k] : null));
      const r = k => avg(sides.map(x => x.snaps[s] ? x.snaps[s].res[k] : null));
      if (v('vil') == null) { console.log(`  ${String(s).padStart(3)} | (game over)`); continue; }
      console.log(`  ${String(s).padStart(3)} | ${f1(v('vil'))} ${f1(v('mil'))} ${f1(v('bld'))} | ${Math.round(v('float'))} (${['food', 'wood', 'stone', 'gold'].map(k => Math.round(r(k))).join('/')})`);
    }
    const tot = k => sides.reduce((s, x) => s + (x[k] || 0), 0);
    console.log(`  totals${tag}: raids ${tot('raids')} (first avg ${f1(avg(sides.map(s => s.firstRaid != null ? s.firstRaid / 60 : null)))}m) pushes ${tot('pushes')} (first avg ${f1(avg(sides.map(s => s.firstPush != null ? s.firstPush / 60 : null)))}m) kills ${tot('kills')} losses ${tot('lost')} razed ${tot('razed')}${asym ? ` | wins ${sides.filter((s, k) => { const gm = games.find(gg => gg.res.includes(s)); const o = gm.res.find(x => x !== s); return o.defeated; }).length}/${games.length}` : ''}`);
  }
  const wins = games.filter(g => g.res.some(r => r.defeated)).length;
  console.log(`  games with a winner ${wins}/${games.length} | idle villagers ${(avg(games.map(g => g.idleFrac)) * 100).toFixed(1)}% | ${avg(games.map(g => g.msThink)).toFixed(2)} ms/think`);
}
