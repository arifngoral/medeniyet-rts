// Checks the age-up building models of src/render/lm/<file>.js without three.js or a browser:
//   node tools/lm-model-check.mjs src/render/lm/arap-aztek-bizans.js
// - every look of the civilizations the file is for (landmarks.js) is there, no unknown ones
// - each one runs without an error and uses only materials / geometries / helpers that exist (MT, XM, LMM, G: read from
//   render/entities.js)
// - how big it is: the extent of the boxes etc. placed straight into c.body / c.roof (footprint about -1.9..1.9, height
//   up to ~5; parts inside your own groups are not measured) and how many pieces
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const file = process.argv[2]; if (!file) { console.log('usage: node tools/lm-model-check.mjs src/render/lm/<file>.js'); process.exit(1); }
const src = fs.readFileSync(path.join(ROOT, 'src/render/entities.js'), 'utf8');
const keysOf = (name) => { const m = src.match(new RegExp('const ' + name + ' = \\{([\\s\\S]*?)\\n\\};')); if (!m) return new Set(); return new Set([...m[1].matchAll(/(?:^|[\s,{])([a-zA-Z_][a-zA-Z0-9_]*)\s*:/g)].map(x => x[1])); };
const KEYS = { MT: keysOf('MT'), XM: keysOf('XM'), LMM: keysOf('LMM'), G: keysOf('G') };

const { LANDMARKS } = await import(pathToFileURL(path.join(ROOT, 'src/landmarks.js')));
const errors = [];
const strict = (name) => new Proxy({}, { get(_, k) { if (typeof k !== 'string') return undefined; if (!KEYS[name].has(k)) { errors.push(`${name}.${k} yok`); } return { _m: name + '.' + k }; } });
const v3 = () => ({ x: 0, y: 0, z: 0, set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }, setScalar(s) { this.x = this.y = this.z = s; return this; }, copy() { return this; } });
const obj = () => ({ position: v3(), rotation: v3(), scale: Object.assign(v3(), { x: 1, y: 1, z: 1 }), quaternion: {}, userData: {}, children: [], add(...o) { this.children.push(...o); return this; }, visible: true });
const THREE = new Proxy({}, { get(_, k) { return function () { return obj(); }; } });
let cur = null;
const track = (p, xs, ys, zs) => { if (!cur || (p !== cur.c.body && p !== cur.c.roof)) return; cur.n++; for (const x of xs) { cur.x0 = Math.min(cur.x0, x); cur.x1 = Math.max(cur.x1, x); } for (const y of ys) cur.y1 = Math.max(cur.y1, y); for (const z of zs) { cur.z0 = Math.min(cur.z0, z); cur.z1 = Math.max(cur.z1, z); } };
const need = (p, m, what) => { if (!p || typeof p.add !== 'function') errors.push(`${cur && cur.look}: ${what} için geçersiz ebeveyn`); if (!m) errors.push(`${cur && cur.look}: ${what} için malzeme yok (undefined)`); };
const num = (...a) => { if (a.some(v => typeof v !== 'number' || !isFinite(v))) errors.push(`${cur && cur.look}: sayı değil (${a.join(', ')})`); };
const mk = (geo, p, m, sx, sy, sz, x, y, z) => { need(p, m, 'mk'); num(sx, sy, sz, x, y, z); if (!geo) errors.push(`${cur && cur.look}: geometri yok`); const o = obj(); p && p.add && p.add(o); track(p, [x - sx / 2, x + sx / 2], [y + sy], [z - sz / 2, z + sz / 2]); return o; };
const bx = (p, m, w, h, d, x, y, z) => { need(p, m, 'bx'); num(w, h, d, x, y, z); const o = obj(); p && p.add && p.add(o); track(p, [x - w / 2, x + w / 2], [y + h], [z - d / 2, z + d / 2]); return o; };
const cy = (p, m, r, h, x, y, z) => bx(p, m, r * 2, h, r * 2, x, y, z);
const cn = cy, py = bx;
const sp = (p, m, r, x, y, z) => bx(p, m, r * 2, r * 2, r * 2, x, y - r, z);
const K = { THREE, PI: Math.PI, G: strict('G'), MT: strict('MT'), XM: strict('XM'), LMM: strict('LMM'), mat: () => ({ _m: 'mat' }), mk, bx, cy, cn, py, sp };
// the shared helpers (the same signatures as in entities.js), drawn with the stubs
Object.assign(K, {
  lmFlag: (c, x, z, h) => { cy(c.body, {}, .025, h, x, 0, z); bx(c.body, c.cm, .02, .3, .45, x, h - .32, z + .23); },
  lmDome: (c, m, r, x, y, z, k = 1) => mk({}, c.roof, m, r * 2, r * 2 * k, r * 2, x, y, z),
  lmGable: (c, m, w, h, d, x, y, z) => mk({}, c.roof, m, w, h, d, x, y, z),
  lmMinaret: (c, x, z, h) => { cy(c.body, {}, .11, h, x, 0, z); cy(c.roof, {}, .12, h + .6, x, 0, z); },
  lmCols: (c, n, x0, x1, z, h, m, r = .08, y = 0, alongZ = false) => { for (let i = 0; i < n; i++) { const a = x0 + (x1 - x0) * (n > 1 ? i / (n - 1) : 0); cy(c.body, m, r, h, alongZ ? z : a, y, alongZ ? a : z); } },
  lmCren: (c, m, w, d, y, x = 0, z = 0, s = .14) => bx(c.body, m, w, y + s, d, x, 0, z),
  lmTower: (c, x, z, w, h, m) => bx(c.body, m, w * 1.3, h + w * 1.3, w * 1.3, x, 0, z),
  lmWall: (c, m, a, b, h, t = .28) => { bx(c.body, m, t, h, t, a[0], 0, a[1]); bx(c.body, m, t, h, t, b[0], 0, b[1]); return obj(); },
  lmPagoda: (c, x, z, w, tiers, wallM, roofM, th = .5, y0 = 0) => { const y = y0 + tiers * th * 1.15; bx(c.body, wallM, w * 1.6, y, w * 1.6, x, 0, z); return y; },
  lmSteps: (c, m, w, d, n, h, x = 0, z = 0) => { bx(c.body, m, w, n * h, d, x, 0, z); return n * h; },
  lmArch: (c, m, x, z, w, h, d) => { bx(c.body, m, w, h, d, x, 0, z); return obj(); },
  lmShip: (c, x, z, ry, L = 2.2) => { bx(c.body, {}, .9, 1.9, L, x, 0, z); return obj(); },
});

const mod = await import(pathToFileURL(path.resolve(ROOT, file)));
const looks = mod.default(K);
const civs = path.basename(file, '.js').split('-').map(c => c === 'aziz' ? null : c).filter(c => LANDMARKS[c]);
const want = civs.flatMap(c => LANDMARKS[c].flat().map(l => l.look));
const missing = want.filter(l => !looks[l]), extra = Object.keys(looks).filter(l => !want.includes(l));
console.log(`${file}: ${civs.join(', ')} — ${Object.keys(looks).length}/${want.length} model`);
if (missing.length) console.log('  EKSİK: ' + missing.join(', '));
if (extra.length) console.log('  FAZLA (landmarks.js\'de yok): ' + extra.join(', '));
let bad = missing.length + extra.length;
for (const l of want) {
  if (!looks[l]) continue;
  const c = { body: obj(), roof: obj(), cm: { _m: 'cm' }, chim: [], P: new Proxy({}, { get: () => ({ _m: 'P' }) }), era: 2, s: 4 };
  cur = { look: l, c, n: 0, x0: 9, x1: -9, y1: 0, z0: 9, z1: -9 };
  const e0 = errors.length;
  try { looks[l](c); } catch (err) { errors.push(`${l}: HATA ${err.message}`); }
  const over = cur.x0 < -2.05 || cur.x1 > 2.05 || cur.z0 < -2.05 || cur.z1 > 2.05 || cur.y1 > 5.5;
  const fresh = errors.slice(e0);
  if (fresh.length || over || cur.n < 6) bad++;
  console.log(`  ${fresh.length ? '✗' : over ? '!' : cur.n < 6 ? '?' : '✓'} ${l.padEnd(16)} parça ${String(cur.n).padStart(3)}  x ${cur.x0.toFixed(1)}..${cur.x1.toFixed(1)}  z ${cur.z0.toFixed(1)}..${cur.z1.toFixed(1)}  yük ${cur.y1.toFixed(1)}${over ? '  (taşıyor: -2..2, yükseklik ≤ 5.5)' : ''}${cur.n < 6 ? '  (çok az parça)' : ''}`);
  for (const e of fresh) console.log('      ' + e);
}
console.log(bad ? `SORUN VAR: ${bad}` : 'TAMAM');
process.exit(bad ? 1 : 0);
