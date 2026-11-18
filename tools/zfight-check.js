// Aevum - z-fighting detector (dev tool, runs in the browser console of a running game page).
//
//   const z = await import('/tools/zfight-check.js');
//   const r = await z.checkModels();        // every building type x era x mask/neighbour variant + every unit x age
//   z.print(r);                             // console.table of the hits (type, era, the two parts, gap, area, where)
//   await z.checkScene(app, { types: ["wall", "gate", "tower"], age: 2 });   // the live scene: joined walls / gates / towers
//   z.checkObject(obj, 'label');            // any Object3D
//
// A hit is a pair of triangles with a different look (material colour / roughness / metalness / emissive, times the
// vertex colour) that lie in the same plane (normals within ANG degrees, plane distance <= SOFT world units, HARD
// = the tight tier), face the same way and overlap in that plane by more than MIN_AREA. Such faces flicker (the depth
// buffer cannot order them); faces a few mm apart flicker too when seen from afar. Pairs buried inside another solid
// (a ray along the normal leaves more solids than it enters) and undersides at ground level are left out.
import * as THREE from 'three';
import { makeBuildingModel, makeUnitModel } from '../src/render/entities.js';
import { BUILDINGS, UNITS } from '../src/data.js';

export const OPT = { ANG: 1, HARD: .003, SOFT: .01, MIN_AREA: 1e-4 };

const _v = new THREE.Vector3(), _c = new THREE.Color(), _m = new THREE.Matrix4(), _im = new THREE.Matrix4();

function lookOf(mat, geo, vi) {
  _c.set(0xffffff);
  if (mat.color) _c.copy(mat.color);
  const ca = mat.vertexColors && geo.getAttribute('color');
  if (ca) _c.multiply(new THREE.Color(ca.getX(vi), ca.getY(vi), ca.getZ(vi)));
  const e = mat.emissive ? mat.emissive.getHexString() + (mat.emissiveIntensity ?? 1) : '';
  return _c.getHexString() + '|' + (mat.roughness ?? '') + '|' + (mat.metalness ?? '') + '|' + e + '|' + (mat.map ? 'map' : '') + (mat.transparent ? 'T' + mat.opacity : '');
}

// world-space triangles of every visible mesh under root: {a,b,c (Vector3), n, d, look, col, part}
export function collectTris(root) {
  const tris = [];
  root.updateMatrixWorld(true);
  root.traverse(o => {
    if (!o.isMesh || !o.visible) return;
    let vis = true; for (let p = o; p; p = p.parent) if (p.visible === false) { vis = false; break; }
    if (!vis) return;
    const geo = o.geometry, pos = geo.getAttribute('position'); if (!pos) return;
    const idx = geo.index, mats = Array.isArray(o.material) ? o.material : [o.material];
    const groups = geo.groups.length ? geo.groups : [{ start: 0, count: idx ? idx.count : pos.count, materialIndex: 0 }];
    const inst = o.isInstancedMesh ? o.count : 1;
    for (let k = 0; k < inst; k++) {
      if (o.isInstancedMesh) { o.getMatrixAt(k, _im); _m.multiplyMatrices(o.matrixWorld, _im); } else _m.copy(o.matrixWorld);
      for (const gr of groups) {
        const mat = mats[gr.materialIndex | 0]; if (!mat || mat.visible === false) continue;
        const part = (o.parent && o.parent.name) || o.name || o.type;
        const end = Math.min(gr.start + gr.count, idx ? idx.count : pos.count);
        for (let i = gr.start; i + 2 < end; i += 3) {
          const ia = idx ? idx.getX(i) : i, ib = idx ? idx.getX(i + 1) : i + 1, ic = idx ? idx.getX(i + 2) : i + 2;
          const a = new THREE.Vector3().fromBufferAttribute(pos, ia).applyMatrix4(_m);
          const b = new THREE.Vector3().fromBufferAttribute(pos, ib).applyMatrix4(_m);
          const c = new THREE.Vector3().fromBufferAttribute(pos, ic).applyMatrix4(_m);
          const n = new THREE.Vector3().subVectors(b, a).cross(_v.subVectors(c, a));
          const ar = n.length() / 2; if (ar < 1e-7) continue;
          n.normalize();
          tris.push({ a, b, c, n, d: n.dot(a), area: ar, look: lookOf(mat, geo, ia), col: '#' + _c.getHexString(), part, side: mat.side });
        }
      }
    }
  });
  return tris;
}

// 2D helpers: clip convex polygon P by convex polygon Q (both CCW), shoelace area
function area2(P) { let s = 0; for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length]; s += a[0] * b[1] - b[0] * a[1]; } return s / 2; }
function ccw(P) { return area2(P) < 0 ? P.slice().reverse() : P; }
function clip(P, Q) {
  let out = P;
  for (let i = 0; i < Q.length && out.length; i++) {
    const A = Q[i], B = Q[(i + 1) % Q.length], inp = out; out = [];
    const side = (p) => (B[0] - A[0]) * (p[1] - A[1]) - (B[1] - A[1]) * (p[0] - A[0]);
    for (let j = 0; j < inp.length; j++) {
      const p = inp[j], q = inp[(j + 1) % inp.length], sp = side(p), sq = side(q);
      if (sp >= 0) out.push(p);
      if ((sp >= 0) !== (sq >= 0)) { const t = sp / (sp - sq); out.push([p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t]); }
    }
  }
  return out;
}

// how many solids contain p: along a ray, (back-face hits - front-face hits) over all triangles
function depthInside(tris, p, dir) {
  let k = 0; const e1 = new THREE.Vector3(), e2 = new THREE.Vector3(), h = new THREE.Vector3(), s = new THREE.Vector3(), q = new THREE.Vector3();
  for (const t of tris) {
    e1.subVectors(t.b, t.a); e2.subVectors(t.c, t.a); h.crossVectors(dir, e2);
    const det = e1.dot(h); if (Math.abs(det) < 1e-12) continue;
    const f = 1 / det; s.subVectors(p, t.a); const u = f * s.dot(h); if (u < 0 || u > 1) continue;
    q.crossVectors(s, e1); const v = f * dir.dot(q); if (v < 0 || u + v > 1) continue;
    if (f * e2.dot(q) <= 1e-6) continue;
    k += t.n.dot(dir) > 0 ? 1 : -1;
  }
  return k;
}

// all z-fighting pairs among tris; returns grouped hits [{a, b, gap, area, n, at:[x,y,z], cnt}]
export function findZFights(tris, opt = OPT, keep) {   // keep(t): false = t takes no part in pairs (still blocks rays)
  const R = 50, cosA = Math.cos(opt.ANG * Math.PI / 180), buckets = new Map();
  const key = (x, y, z) => x + ',' + y + ',' + z;
  for (let i = 0; i < tris.length; i++) {
    const t = tris[i]; t.i = i; t.q = [Math.round(t.n.x * R), Math.round(t.n.y * R), Math.round(t.n.z * R)];
    const k = key(...t.q); let a = buckets.get(k); if (!a) buckets.set(k, a = []); a.push(t);
  }
  for (const a of buckets.values()) a.sort((x, y) => x.d - y.d);
  const groups = new Map();
  for (const t of tris) {
    if (keep && !keep(t)) continue;
    if (t.n.y < -.5 && Math.max(t.a.y, t.b.y, t.c.y) < (t.gy || 0) + .1) continue;   // undersides on the ground
    for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) for (let dz = -1; dz <= 1; dz++) {
      const a = buckets.get(key(t.q[0] + dx, t.q[1] + dy, t.q[2] + dz)); if (!a) continue;
      let lo = 0, hi = a.length; while (lo < hi) { const m = (lo + hi) >> 1; if (a[m].d < t.d - opt.SOFT) lo = m + 1; else hi = m; }
      for (let j = lo; j < a.length && a[j].d <= t.d + opt.SOFT; j++) {
        const u = a[j]; if (u.i <= t.i || u.look === t.look || t.n.dot(u.n) < cosA || (keep && !keep(u))) continue;
        if (u.n.y < -.5 && Math.max(u.a.y, u.b.y, u.c.y) < (u.gy || 0) + .1) continue;
        // bounding boxes (grown by the gap)
        const g = opt.SOFT;
        if (Math.max(t.a.x, t.b.x, t.c.x) + g < Math.min(u.a.x, u.b.x, u.c.x) || Math.max(u.a.x, u.b.x, u.c.x) + g < Math.min(t.a.x, t.b.x, t.c.x)) continue;
        if (Math.max(t.a.y, t.b.y, t.c.y) + g < Math.min(u.a.y, u.b.y, u.c.y) || Math.max(u.a.y, u.b.y, u.c.y) + g < Math.min(t.a.y, t.b.y, t.c.y)) continue;
        if (Math.max(t.a.z, t.b.z, t.c.z) + g < Math.min(u.a.z, u.b.z, u.c.z) || Math.max(u.a.z, u.b.z, u.c.z) + g < Math.min(t.a.z, t.b.z, t.c.z)) continue;
        // project both on t's plane
        const n = t.n, ax = Math.abs(n.x) < .9 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0);
        const e1 = new THREE.Vector3().crossVectors(n, ax).normalize(), e2 = new THREE.Vector3().crossVectors(n, e1);
        const pr = (p) => [p.dot(e1), p.dot(e2)];
        const P = ccw([pr(t.a), pr(t.b), pr(t.c)]), Q = ccw([pr(u.a), pr(u.b), pr(u.c)]);
        const I = clip(P, Q); if (I.length < 3) continue;
        const ar = Math.abs(area2(I)); if (ar < opt.MIN_AREA * .05) continue;
        const gap = Math.abs(u.d - t.d);
        // a point in the overlap, just off the faces: buried inside another solid?
        let cx = 0, cy2 = 0; for (const p of I) { cx += p[0]; cy2 += p[1]; } cx /= I.length; cy2 /= I.length;
        const at = new THREE.Vector3().addScaledVector(e1, cx).addScaledVector(e2, cy2).addScaledVector(n, Math.max(t.d, u.d) + 2e-4);
        const k = [t.look, u.look].sort().join(' / ') + ' | n ' + [n.x, n.y, n.z].map(v => v.toFixed(2)).join(',') + ' | d ' + t.d.toFixed(3) + ' | ' + [t.part, u.part].sort().join(' ');
        let G = groups.get(k);
        if (!G) groups.set(k, G = { a: t.look < u.look ? t : u, b: t.look < u.look ? u : t, gap, area: 0, pd: +t.d.toFixed(3), n: [+n.x.toFixed(2), +n.y.toFixed(2), +n.z.toFixed(2)], pts: [], cnt: 0 });
        if (!G.ex) G.ex = [t, u].map(x => [x.a, x.b, x.c].map(v => v.toArray().map(q => +q.toFixed(3)).join(',')).join(' ; '));
        G.area += ar; G.cnt++; G.gap = Math.min(G.gap, gap); G.pts.push(at);
      }
    }
  }
  const out = [];
  for (const G of groups.values()) {
    if (G.area < opt.MIN_AREA) continue;
    // buried: every sample (up to 6) is inside another solid
    const S = G.pts.length <= 6 ? G.pts : [0, 1, 2, 3, 4, 5].map(i => G.pts[Math.floor(i * (G.pts.length - 1) / 5)]);
    const dir = new THREE.Vector3(.0013, 1, .0007).normalize();   // (up: the open shapes - frustums, logs, domes, prisms - are open at the bottom only)
    const vis = S.filter(p => depthInside(tris, p, dir) < 1);
    if (!vis.length) continue;
    const bb = new THREE.Box3().setFromPoints(vis);
    out.push({ a: G.a.col + ' ' + G.a.part, b: G.b.col + ' ' + G.b.part, lookA: G.a.look, lookB: G.b.look, gap: +G.gap.toFixed(4), tier: G.gap <= OPT.HARD ? 'HARD' : 'soft',
      area: +G.area.toFixed(4), n: G.n.join(','), pd: G.pd, tris: G.cnt, ex: G.ex,
      at: [bb.min.x, bb.min.y, bb.min.z].map(v => +v.toFixed(3)).join(',') + ' .. ' + [bb.max.x, bb.max.y, bb.max.z].map(v => +v.toFixed(3)).join(',') });
  }
  return out.sort((x, y) => y.area - x.area);
}

export function checkObject(obj, label, opt, keep) {
  let tris = collectTris(obj).filter(t => t.part !== 'scaf');   // (scaffold: only while building)
  const hits = findZFights(tris, opt, keep);
  for (const h of hits) h.model = label;
  return hits;
}

const nameGroups = (root) => { const U = root.userData; for (const k of ['body', 'roof', 'scaf', 'spin', 'fur', 'live']) if (U[k] && U[k].isObject3D && !U[k].name) U[k].name = k; root.traverse(o => { if (o.isGroup && !o.name && o.parent === root) o.name = 'slab'; }); };

// the mask variants worth building per type (walls / gates / towers join their neighbours)
function masksOf(type) {
  if (type === 'wall') return [0, 1, 2, 3, 5, 6, 7, 10, 11, 15];
  if (type === 'tower') return [0, 1, 5, 15, 16, 16 | 1, 16 | 5, 16 | 15];
  if (type === 'gate') { const r = []; for (const base of [10, 5]) for (const g of [0, 32, 64, 96, 128, 256, 128 | 32, 256 | 64]) r.push(base | g); return r; }
  if (type === 'rail') return [0, 1, 5, 3, 7, 15];
  if (type === 'dock') return [1, 2, 4, 8];
  return [0];
}

// sweep: every building type x era (x mask) and every unit type x age. Returns hits with model labels.
export async function checkModels({ types, eras = [0, 1, 2, 3, 4], units = true, opt } = {}) {
  const hits = [], seen = new Map();
  const list = types || Object.keys(BUILDINGS);
  for (const type of list) for (const era of eras) for (const mask of masksOf(type)) {
    const def = BUILDINGS[type] || {}, bs = def.baseSize || def.size || 1, k = type === 'tower' && !(mask & 16) ? 1 : (def.size || bs) / bs;   // (a tower without bit 16 is an old 1x1 one)
    let root; try { root = makeBuildingModel(type, bs, era, 0x3a7bd5, mask, 12345); } catch (err) { hits.push({ model: type + ' e' + era, a: 'BUILD FAILED', b: String(err) }); continue; }
    if (k !== 1) root.scale.setScalar(k);
    nameGroups(root);
    // a wall / gate / tower arm ends on the tile edge toward a linked neighbour, whose own arm covers that end face:
    // leave those end faces out here (checkScene sees both pieces together)
    const E = .5 * k, dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]].filter((d, i) => (type === 'wall' || type === 'gate' || type === 'tower' || type === 'rail') && mask & (1 << i));
    const keep = (t) => !dirs.some(d => Math.abs(t.n.x * d[0] + t.n.z * d[1] - 1) < .01 && Math.abs(t.d - E) < .006);
    for (const h of checkObject(root, type + ' e' + era + ' m' + mask, opt, keep)) {
      const key = type + '|' + era + '|' + h.lookA + '|' + h.lookB + '|' + h.n + '|' + h.pd;   // one row per part pair, masks listed
      const s = seen.get(key); if (s) { s.masks.push(mask); s.area = Math.max(s.area, h.area); continue; }
      h.type = type; h.era = era; h.masks = [mask]; seen.set(key, h); hits.push(h);
    }
    root.traverse(o => { if (o.isMesh && o.userData.own) o.geometry.dispose(); });
    await new Promise(r => setTimeout(r, 0));
  }
  if (units) for (const type of Object.keys(UNITS)) for (const age of eras) {
    let u; try { u = makeUnitModel(type, 0x3a7bd5, age); } catch (err) { continue; }
    const root = u.root || u; root.updateMatrixWorld(true);
    for (const h of checkObject(root, 'unit ' + type + ' a' + age, opt)) {
      const key = 'u|' + type + '|' + h.lookA + '|' + h.lookB + '|' + h.n;
      const s = seen.get(key); if (s) { s.ages.push(age); continue; }
      h.type = 'unit:' + type; h.era = age; h.ages = [age]; seen.set(key, h); hits.push(h);
    }
  }
  return hits;
}

// the live scene: every building view at once (catches pieces of neighbouring walls / gates / towers meeting).
// { types: ['wall', 'gate', 'tower'] } only those building types; { age: n } rebuilds those views at age n first (a
// dev look at every era on one layout; the next age change in the game rebuilds them again); { opt } detector options.
export async function checkScene(app, { types, age, opt } = {}) {
  const ev = app.renderer && app.renderer.entityView;
  const tris = [];
  const views = ev && ev.views ? [...ev.views.values()].filter(v => v.kind === 'building' && v.root && (!types || types.includes(v.e.type))) : [];
  if (age != null) for (const v of views) { v.quiet = true; ev._buildBuildingMesh(v, v.e, age); }
  const map = app.game && app.game.map;
  for (const v of views) v.root.position.set(v.e.x, map ? map.heightAt(v.e.x, v.e.z) : v.root.position.y, v.e.z);   // (as the view loop places them; it may not have run yet)
  for (const v of views) {
    nameGroups(v.root); v.root.updateMatrixWorld(true);
    const t = collectTris(v.root).filter(x => x.part !== 'scaf');
    for (const x of t) { x.gy = v.root.position.y; x.part = v.e.type + '#' + v.id + '@' + v.e.tx + ',' + v.e.tz + ':' + x.part; }
    tris.push(...t);
  }
  return findZFights(tris, opt).map(h => Object.assign(h, { model: 'scene' + (age != null ? ' e' + age : '') }));
}

export function print(hits) {
  console.table(hits.map(h => ({ model: h.type ? h.type + ' e' + h.era : h.model, masks: (h.masks || h.ages || []).join(' '), a: h.a, b: h.b, tier: h.tier, gap: h.gap, area: h.area, n: h.n, at: h.at })));
  return hits.length;
}

if (typeof window !== 'undefined') window.zfight = { checkModels, checkScene, checkObject, collectTris, findZFights, print, OPT };
