// Render benchmark + screenshot harness (headless Chromium via Playwright, SwiftShader WebGL).
// node test/render-bench.mjs [--counts 100,300,500] [--frames 60] [--shots DIR] [--port 5181] [--render-dir DIR]
// Needs a local copy of three@0.160.0 (the page loads it from cdn.jsdelivr.net): set THREE_PKG to the package dir
// (the one holding build/three.module.js and examples/jsm). Frames are driven by a fake requestAnimationFrame
// with a fixed 1/30 s step and a seeded Math.random, so screenshots of the same scene are reproducible.
// Reports per unit count: draw calls and triangles per frame (shadows on), JS ms in EntityView.update, total
// Renderer.render ms (SwiftShader: only relative numbers mean anything), and the same with the camera panned away.
import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const COUNTS = arg('counts', '100,300,500').split(',').map(Number).filter(n => n > 0);
const FRAMES = +arg('frames', 60), SHOTS = arg('shots', ''), PORT = +arg('port', 5181);
const RENDER_DIR = arg('render-dir', '');
const PROFILE = process.argv.includes('--profile');   // print the top self-time JS functions of the measured frames   // serve src/render/* from another folder (A/B against an older copy)
const PKG = process.env.THREE_PKG || '/tmp/claude-0/-home-user-aevum/55272746-57db-5b0e-86bf-fd7372152aa0/scratchpad/three-pkg/package/';
if (!fs.existsSync(path.join(PKG, 'build/three.module.js'))) { console.log('SKIP: no local three@0.160.0 (set THREE_PKG)'); process.exit(0); }
let chromium;
try { ({ chromium } = require('playwright')); } catch (err) { console.log('SKIP: playwright not installed'); process.exit(0); }

const srv = spawn(process.execPath, [path.join(ROOT, 'server.js')], { env: { ...process.env, PORT: String(PORT) }, stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ---- in-page helpers (serialized into the page)
function pageInit() {
  let s = 12345; window.__seed = (v) => { s = v | 0; }; Math.random = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), s | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  window.__raf = []; window.__now = 1000;
  window.requestAnimationFrame = cb => { window.__raf.push(cb); return window.__raf.length; };
  window.__step = (n, dt = 1 / 30) => { for (let i = 0; i < n; i++) { window.__now += dt * 1000; const q = window.__raf.splice(0); for (const cb of q) cb(window.__now); } };
}

function setupScene(opt) {
  const app = window.app;
  window.__seed(777);   // same random stream for the new map's textures whatever ran before
  const g = app.newGame({ mapSize: 96, enemies: 3, players: [{ kind: 'human', team: 1 }, { kind: 'ai', team: 2 }, { kind: 'ai', team: 3 }, { kind: 'ai', team: 4 }, { kind: 'ai', team: 5 }], difficulty: 'normal', startRes: 'high', startAge: 0, sandbox: true, seed: 4242, mapType: 'plains' });
  g.update = function () {};   // the sim is frozen (instance stub only); the bench drives g.time itself
  g.reveal = true; g.fog.fill(2); g.fogVersion++;
  for (const el of document.querySelectorAll('body *')) if (el.id !== 'game' && !el.querySelector('#game') && el.tagName !== 'SCRIPT') el.style.visibility = 'hidden';
  // age per owner: 0 -> 2, 1 -> 0, 2 -> 1, 3 -> 3, 4 -> 4
  const AGE = [2, 0, 1, 3, 4];   // five players: every age on screen
  g.players.forEach((p, i) => { p.age = AGE[i % 5]; });
  if (g.players.length < 5) console.warn('bench: only ' + g.players.length + ' players');
  // remove the start units (keep buildings / resources) so only our units are counted
  for (const u of g.units.slice()) { g.entities.delete(u.id); }
  g.units.length = 0;
  const cx = 48, cz = 48;
  // clear a box of resources around the centre so the units stand on open ground
  for (const e of [...g.entities.values()]) if (e.kind === 'resource' && Math.abs(e.x - cx) < 16 && Math.abs(e.z - cz) < 16) g.entities.delete(e.id);
  const units = [];
  const add = (type, owner, x, z, anim, extra) => {
    const u = g._addUnit(type, owner % g.players.length, x, z); u.anim = anim; u.state = anim === 'idle' ? 'idle' : anim; u.rot = (u.id * 0.7) % 6.28;
    if (anim === 'attack') u.attackT = -((u.id * .37) % 1.2);
    if (extra) Object.assign(u, extra);
    units.push(u); return u;
  };
  if (opt.kind === 'bench') {
    const MIX = ['villager', 'villager', 'villager', 'spearman', 'swordsman', 'archer', 'heavyinf', 'crossbow', 'musketeer', 'rifleman',
      'lightcav', 'knight', 'cuirassier', 'villager', 'spearman', 'archer', 'ram', 'catapult', 'cannon', 'artillery'];
    const n = opt.n, side = Math.ceil(Math.sqrt(n)), sp = opt.spacing || .95;
    for (let i = 0; i < n; i++) {
      const type = MIX[i % MIX.length], owner = (i * 7) % 5;
      const x = cx + ((i % side) - side / 2) * sp, z = cz + (((i / side) | 0) - side / 2) * sp;
      const r = (i * 13) % 20;
      let anim = r < 8 ? 'walk' : r < 14 ? 'attack' : r < 17 ? 'idle' : 'gather';
      if (anim === 'gather') anim = type === 'villager' ? ['chop', 'mine', 'build', 'farm'][i % 4] : 'idle';
      const u = add(type, owner, x, z, anim);
      if (type === 'villager' && i % 5 === 0) u.carry = { type: 'wood', amount: 5 };
    }
  } else {
    // parity scene: a labelled line-up of every land unit type over owners/ages + states
    const T = ['villager', 'spearman', 'swordsman', 'archer', 'heavyinf', 'crossbow', 'musketeer', 'rifleman', 'lightcav', 'knight', 'cuirassier', 'ram', 'catapult', 'cannon', 'artillery', 'tradecart'];
    const ANIMS = ['walk', 'attack', 'idle', 'chop', 'die'];
    for (let r = 0; r < 5; r++) for (let i = 0; i < T.length; i++) {
      let anim = ANIMS[(i + r) % ANIMS.length];
      if (anim === 'chop' && T[i] !== 'villager') anim = 'walk';
      if (T[i] === 'villager') anim = ['chop', 'mine', 'farm', 'build', 'walk'][r];
      const u = add(T[i], r, cx - 9 + i * 1.2, cz - 4 + r * 1.9, anim);
      if (T[i] === 'villager' && r === 4) u.carry = { type: 'gold', amount: 5 };
      if (anim === 'die') { u.dead = true; u.deathTime = -0.3; u.hp = 0; }
    }
    add('galley', 2, cx + 12, cz - 3, 'idle'); add('galleon', 3, cx + 12, cz + 1, 'walk'); add('ironclad', 4, cx + 12, cz + 5, 'idle'); add('fishboat', 0, cx + 12, cz + 8, 'idle');
    g._addRes('deer', cx - 11, cz + 6, 100);
  }
  // dead units would be removed by the sim; we never step it, they stay as fallen bodies
  g.fogVersion++;
  const sel = units.filter((u, i) => !u.dead && i % (opt.kind === 'bench' ? 10 : 3) === 0).map(u => u.id);
  app.select(sel, true);
  units.forEach((u, i) => { if (i % 4 === 1) u.hp = Math.max(1, Math.round(u.maxHp * .45)); });
  const R = app.renderer; R.setQuality && R.setQuality('high');
  return { n: units.length, sel: sel.length };
}

function setCam(o) {
  const R = window.app.renderer; Object.assign(R.cam, o); Object.assign(R._c, o);
}

function instrument() {
  const R = window.app.renderer, ev = R.entityView, g = window.app.game;
  window.__st = { ev: 0, rn: 0, n: 0, calls: 0, tris: 0, maxCalls: 0 };
  if (!ev.__wrapped) {
    ev.__wrapped = true;
    const upd = ev.update.bind(ev);
    ev.update = function (dt, t) {
      // keep the sim clock moving for attack swings / deaths without stepping the sim
      g.time += dt;
      for (const u of g.units) if (u.anim === 'attack' && g.time - u.attackT > 1.2) u.attackT = g.time - ((u.id * .13) % .2);
      const t0 = performance.now(); upd(dt, t); window.__st.ev += performance.now() - t0;
    };
  }
  if (!R.__wrapped) {
    R.__wrapped = true;
    const rnd = R.render.bind(R);
    R.render = function (dt) {
      const t0 = performance.now(); rnd(dt); const s = window.__st; s.rn += performance.now() - t0; s.n++;
      const i = R.renderer.info.render; s.calls += i.calls; s.tris += i.triangles; s.maxCalls = Math.max(s.maxCalls, i.calls);
    };
  }
}

function readStats() {
  const s = window.__st, n = Math.max(1, s.n);
  const ev = window.app.renderer.entityView;
  let meshes = 0, unitsN = 0;
  const cam = window.app.renderer.camera; let inView = 0;
  for (const v of ev.views.values()) if (v.rig && v.e.kind === 'unit') {
    unitsN++; v.root.traverse(o => { if (o.isMesh && o.visible) meshes++; });
    const q = v.root.position.clone().project(cam); if (Math.abs(q.x) <= 1 && Math.abs(q.y) <= 1 && q.z < 1) inView++;
  }
  return { frames: s.n, calls: +(s.calls / n).toFixed(1), tris: Math.round(s.tris / n), evMs: +(s.ev / n).toFixed(2), renderMs: +(s.rn / n).toFixed(1), unitMeshes: meshes, unitViews: unitsN, inView };
}
function resetStats() { const s = window.__st; s.ev = s.rn = s.n = s.calls = s.tris = s.maxCalls = 0; }

(async () => {
  let b;
  try {
    for (let i = 0; i < 50; i++) { try { const r = await fetch('http://localhost:' + PORT + '/'); if (r.ok) break; } catch (err) { /* not up yet */ } await sleep(100); }
    b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
    const p = await b.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
    await p.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => {
      const rel = r.request().url().split('three@0.160.0/')[1];
      r.fulfill({ path: path.join(PKG, rel), contentType: 'application/javascript' });
    });
    if (RENDER_DIR) await p.route('**/src/render/*.js', r => r.fulfill({ path: path.join(RENDER_DIR, r.request().url().split('/src/render/')[1].split('?')[0]), contentType: 'text/javascript' }));
    const errs = [];
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
    await p.addInitScript(pageInit);
    await p.goto('http://localhost:' + PORT + '/', { waitUntil: 'load' });
    await p.waitForFunction(() => window.app && window.app.renderer && window.app.game, null, { timeout: 30000 });
    await p.evaluate(() => window.__step(3));
    const results = [];
    if (SHOTS) {
      fs.mkdirSync(SHOTS, { recursive: true });
      await p.evaluate(setupScene, { kind: 'parity' });
      const views = [
        ['close', { tx: 46, tz: 46, dist: 13, yaw: 0, pitch: .7 }],
        ['close2', { tx: 54, tz: 47, dist: 11, yaw: .6, pitch: .6 }],
        ['rts', { tx: 49, tz: 48, dist: 34, yaw: 0, pitch: .87 }],
      ];
      for (const [name, c] of views) {
        await p.evaluate(setCam, c);
        await p.evaluate(() => window.__step(20));
        await p.screenshot({ path: path.join(SHOTS, name + '.png') });
      }
      await p.evaluate(() => { window.app.renderer.setQuality('low'); });
      await p.evaluate(setCam, views[0][1]); await p.evaluate(() => window.__step(5));
      await p.screenshot({ path: path.join(SHOTS, 'close-low.png') });
      console.log('shots written to', SHOTS);
    }
    // regression: the fixed health-bar batches must survive a long stretch with no bars (idle dispose would orphan them)
    const hpOk = await p.evaluate(() => {
      const ev = window.app.renderer.entityView; if (!ev._hpB) return null;
      for (let i = 0; i < 700; i++) { ev._hpB.flush(); ev._hpF.flush(); }
      return ev._hpB.mesh.parent === ev.scene && ev._hpF.mesh.parent === ev.scene;
    });
    if (hpOk === false) { console.error('FAIL: health-bar batches were disposed after 700 idle frames'); process.exitCode = 1; }
    else if (hpOk) console.log('hp batches survive idle: ok');
    for (const n of COUNTS) {
      const info = await p.evaluate(setupScene, { kind: 'bench', n });
      await p.evaluate(setCam, { tx: 48, tz: 48, dist: 34, yaw: 0, pitch: .87 });
      await p.evaluate(instrument);
      await p.evaluate(() => window.__step(10));        // build meshes, warm up shaders
      await p.evaluate(resetStats);
      let cdp = null;
      if (PROFILE) { cdp = await p.context().newCDPSession(p); await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval', { interval: 100 }); await cdp.send('Profiler.start'); }
      await p.evaluate(f => window.__step(f), FRAMES);
      if (cdp) {
        const { profile } = await cdp.send('Profiler.stop');
        const self = new Map(), byId = new Map(profile.nodes.map(n => [n.id, n])), dts = profile.timeDeltas;
        for (let i = 0; i < profile.samples.length; i++) { const n = byId.get(profile.samples[i]), cf = n.callFrame; const k = (cf.functionName || '(anon)') + ' ' + cf.url.split('/').pop() + ':' + cf.lineNumber; self.set(k, (self.get(k) || 0) + (dts[i] || 0)); }
        self.delete('(program) :-1'); self.delete('(idle) :-1');   // GPU waits (SwiftShader) / idle: not JS
        const tot = [...self.values()].reduce((a, b) => a + b, 0);
        console.log('profile (' + n + ' units), top JS self time (' + (tot / 1000 / FRAMES).toFixed(2) + ' ms/frame sampled):');
        for (const [k, t] of [...self].sort((a, b) => b[1] - a[1]).slice(0, 25)) console.log('  ' + (t / tot * 100).toFixed(1).padStart(5) + '%  ' + k);
      }
      const on = await p.evaluate(readStats);
      // camera looking away from the crowd (units off-screen but fog-visible)
      await p.evaluate(setCam, { tx: 15, tz: 85, dist: 34, yaw: 0, pitch: .87 });
      await p.evaluate(() => window.__step(5));
      await p.evaluate(resetStats);
      await p.evaluate(f => window.__step(f), Math.max(10, FRAMES >> 1));
      const off = await p.evaluate(readStats);
      results.push({ units: info.n, ...on, offEvMs: off.evMs, offCalls: off.calls });
      console.log(JSON.stringify(results[results.length - 1]));
    }
    console.table(results);
    if (errs.length) console.log('page messages:\n' + errs.slice(0, 20).join('\n'));
  } catch (err) { console.error(err); process.exitCode = 1; }
  finally { if (b) await b.close(); srv.kill(); }
})();
