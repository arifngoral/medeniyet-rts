// The model showcase (vitrin.html): an asset-library page of the game's 3D models. Every card shows one unit or
// building, alive: units loop through idle -> walk -> attack -> death (or stay in one of them), buildings turn slowly.
// The cards a version added or changed (versions.js showcase) come first, with a note on what to look at.
// One WebGL canvas covers the window; each card's viewport is drawn into with a scissor rectangle, so dozens of
// models cost one context. Models are the game's own (render/entities.js), posed by the game's own animation code.
import * as THREE from 'three';
import { UNITS, BUILDINGS, AGES } from './data.js';
import { CIVS } from './civs.js';
import { VERSIONS, TAG_TR } from './versions.js';
import { makeUnitModel, makeBuildingModel, poseUnitModel } from './render/entities.js';
import { loadEra, glbVersion } from './render/glb-models.js';

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const qs = new URLSearchParams(location.search);
const CLS_TR = { civil: 'Sivil', infantry: 'Piyade', ranged: 'Menzilli', cavalry: 'Süvari', siege: 'Kuşatma', ship: 'Gemi', train: 'Tren' };
const STATE_TR = { idle: 'Bekliyor', walk: 'Yürüyor', attack: 'Saldırıyor', die: 'Ölüyor' };
const MODES = [['loop', 'Döngü'], ['idle', 'Dur'], ['walk', 'Yürü'], ['attack', 'Saldır'], ['die', 'Öl']];
const DEF_COLOR = 0x2e7bff;

// ---------- what to show ----------
const ver = VERSIONS.find((v) => v.v === qs.get('v')) || VERSIONS[0];
const noteOf = new Map(); for (const v of VERSIONS) for (const s of v.showcase || []) if (!noteOf.has(s.id)) noteOf.set(s.id, { ...s, ver: v.v });
const unitItem = (id) => {
  const u = UNITS[id], n = noteOf.get(id), civ = u.civ && CIVS[u.civ];
  return { key: 'u:' + id, kind: 'unit', id, name: u.name, sub: civ ? `${civ.icon} ${civ.name.replace(/\s*\(.*\)$/, '')} · ${UNITS[u.base].name} yerine` : `${CLS_TR[u.cls] || u.cls} · ${AGES[u.age].name}`,
    note: n ? n.note : '', desc: u.desc || '', tags: n ? n.tags : [], minAge: u.age, color: civ ? parseInt(civ.color.slice(1), 16) : DEF_COLOR };
};
const buildItem = (id) => {
  const b = BUILDINGS[id], n = noteOf.get(id);
  return { key: 'b:' + id, kind: 'building', id, name: b.name, sub: `Yapı · ${AGES[b.age].name}`, note: n ? n.note : '', desc: b.desc || '', tags: n ? n.tags : [], minAge: b.age, color: DEF_COLOR };
};
const TABS = {
  yeni: { label: 'Bu sürüm', lead: () => `<b>Sürüm ${esc(ver.v)} · ${esc(ver.title)}</b> ile gelen ya da değişen modeller. Her kartın altında neye bakacağın yazıyor; animasyonlar döngüde oynar.`,
    items: () => (ver.showcase || []).filter((s) => (s.kind === 'building' ? BUILDINGS[s.id] : UNITS[s.id])).map((s) => (s.kind === 'building' ? buildItem(s.id) : unitItem(s.id))) },
  birlik: { label: 'Tüm birlikler', lead: () => 'Oyundaki bütün birlikler: standart olanlar ve medeniyetlerin özel birlikleri. Çağı değiştirince kıyafetleri de değişir.',
    items: () => Object.keys(UNITS).map(unitItem) },
  yapi: { label: 'Yapılar', lead: () => 'Oyundaki bütün yapılar, seçtiğin çağın görünümüyle. Yavaşça dönerler.',
    items: () => Object.keys(BUILDINGS).filter((k) => !BUILDINGS[k].legacy).map(buildItem) },
};
let tab = TABS[qs.get('tab')] ? qs.get('tab') : (ver.showcase || []).length ? 'yeni' : 'birlik';
let age = 2;

// ---------- one WebGL canvas for every card ----------
const canvas = $('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05; renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setClearColor(0x000000, 0); renderer.setScissorTest(true);
const GROUND = new THREE.CircleGeometry(1, 40).rotateX(-Math.PI / 2);
const GROUND_M = new THREE.MeshStandardMaterial({ color: 0x5a4226, roughness: 1 });
const box3 = new THREE.Box3(), vec = new THREE.Vector3();

let cards = [];   // { item, el, view, stateEl, scene, cam, model, mode, ... }

function buildModel(c) {
  const it = c.item, a = Math.max(age, it.minAge);
  const scene = new THREE.Scene();
  scene.add(new THREE.HemisphereLight(0xd6eaff, 0x7a6845, 1.25));
  const sun = new THREE.DirectionalLight(0xffedcf, 2.6); sun.position.set(3, 6, 4); scene.add(sun);
  let root, h, r;
  if (it.kind === 'unit') {
    const u = makeUnitModel(it.id, it.color, a);
    c.v = Object.assign(u, { tool: '', carry: '', az0: undefined, phase: 0 });
    root = u.root;
  } else {
    try { loadEra(a); } catch (e) { /* the box model is drawn instead */ }
    root = makeBuildingModel(it.id, BUILDINGS[it.id].size, a, it.color, 0, 7);
    c.v = null;
  }
  scene.add(root);
  root.updateMatrixWorld(true);
  box3.setFromObject(root);
  if (box3.isEmpty()) { box3.set(new THREE.Vector3(-1, 0, -1), new THREE.Vector3(1, 1, 1)); }
  h = Math.max(.6, box3.max.y); r = Math.max(.5, Math.hypot(box3.max.x - box3.min.x, box3.max.z - box3.min.z) / 2);
  const g = new THREE.Mesh(GROUND, GROUND_M); g.scale.setScalar(r * 1.25 + .4); g.position.y = -.01; scene.add(g);
  const cam = new THREE.PerspectiveCamera(28, 4 / 3, .1, 400);
  // (a unit lies down when it dies and swings its weapon: leave room around it)
  const fit = it.kind === 'unit' ? Math.max(h * 1.45, r * 1.8) : Math.max(h * 1.15, r * 1.4);
  const dist = fit / Math.tan(14 * Math.PI / 180) * .62;
  const ty = it.kind === 'unit' ? h * .32 : h * .36;
  cam.position.set(dist * .62, ty + dist * .42, dist * .72); cam.lookAt(0, ty, 0);
  Object.assign(c, { scene, cam, root, built: true, age: a, glb: it.kind === 'building' ? glbVersion() : 0 });
}
function drop(c) { c.built = false; c.scene = null; c.root = null; c.v = null; }

// ---------- animation: the stand-in entity of a card ----------
const CYCLE = [['idle', 2.0], ['walk', 3.0], ['attack', 4.4], ['die', 3.6]];
function entityAt(c, now) {
  const e = c.e || (c.e = { id: (c.i * 7) | 0, type: c.item.id, anim: 'idle', attackT: null, deathTime: null, dead: false, carry: null });
  const u = UNITS[c.item.id], dieLen = u.kit && u.kit.mount === 'elephant' ? 4.6 : 3.6;
  let st = c.mode, k;   // k: seconds into the state
  if (c.mode === 'loop') {
    const total = CYCLE.reduce((s, x) => s + (x[0] === 'die' ? dieLen : x[1]), 0);
    let x = (now - c.t0) % total;
    if ((now - c.t0) / total >= (c.turn | 0) + 1) { c.turn = Math.floor((now - c.t0) / total); e.id += 1; }   // (the next way of dying next time round)
    for (const [name, len0] of CYCLE) { const len = name === 'die' ? dieLen : len0; if (x < len) { st = name; k = x; break; } x -= len; }
  } else if (c.mode === 'die') { const len = dieLen + .8; k = (now - c.t0) % len; st = k < dieLen ? 'die' : 'idle'; if (Math.floor((now - c.t0) / len) !== (c.turn | 0)) { c.turn = Math.floor((now - c.t0) / len); e.id += 1; } }
  else k = now - c.t0;
  e.anim = st; e.dead = st === 'die';
  e.deathTime = st === 'die' ? now - k : null;
  if (st === 'attack') { const gap = Math.max(1.3, Math.min(2.4, u.rof || 1.5)); e.attackT = now - (k % gap); } else e.attackT = null;
  return e;
}

// ---------- page ----------
function draw() {
  const T = TABS[tab], items = T.items();
  $('lead').innerHTML = T.lead();
  $('tabs').innerHTML = ''; for (const [k, t] of Object.entries(TABS)) {
    const n = t.items().length; if (!n && k === 'yeni') continue;
    const b = document.createElement('button'); b.type = 'button'; b.className = k === tab ? 'on' : ''; b.innerHTML = `${esc(t.label)}<small>${n}</small>`;
    b.onclick = () => { tab = k; history.replaceState(null, '', '?tab=' + k + (qs.get('v') ? '&v=' + encodeURIComponent(qs.get('v')) : '')); draw(); }; $('tabs').append(b);
  }
  $('ages').innerHTML = ''; AGES.forEach((a, i) => {
    const b = document.createElement('button'); b.type = 'button'; b.className = i === age ? 'on' : ''; b.textContent = a.name.split(' ')[0]; b.title = a.name;
    b.onclick = () => { age = i; cards.forEach(drop); draw(); }; $('ages').append(b);
  });
  const grid = $('grid'); grid.innerHTML = ''; cards = [];
  if (!items.length) { grid.innerHTML = '<div class="empty">Bu sürümde model değişikliği yok.</div>'; return; }
  const now = performance.now() / 1000;
  items.forEach((it, i) => {
    const el = document.createElement('article'); el.className = 'card';
    const animated = it.kind === 'unit' && !['ship', 'train'].includes(UNITS[it.id].cls);
    el.innerHTML = `<div class="view"><div class="tags">${it.tags.map((t) => `<span class="tag ${esc(t)}">${esc(TAG_TR[t] || t)}</span>`).join('')}</div>${animated ? '<div class="state"></div>' : ''}</div>
      <div class="body"><div class="name"><b>${esc(it.name)}</b><span>${esc(it.sub)}</span></div>
      ${it.note ? `<p class="note">${esc(it.note)}</p>` : ''}${it.desc ? `<p class="desc">${esc(it.desc)}</p>` : ''}
      ${animated ? `<div class="acts">${MODES.map(([k, t]) => `<button type="button" data-m="${k}"${k === 'loop' ? ' class="on"' : ''}>${t}</button>`).join('')}</div>` : ''}</div>`;
    const c = { item: it, i, el, view: el.querySelector('.view'), stateEl: el.querySelector('.state'), mode: 'loop', t0: now - i * .37, built: false, animated };
    for (const b of el.querySelectorAll('.acts button')) b.onclick = () => { c.mode = b.dataset.m; c.t0 = performance.now() / 1000; c.turn = 0; el.querySelectorAll('.acts button').forEach((x) => x.classList.toggle('on', x === b)); };
    grid.append(el); cards.push(c);
  });
}

function frame() {
  requestAnimationFrame(frame);
  const w = window.innerWidth, hgt = window.innerHeight;
  if (canvas.width !== Math.round(w * renderer.getPixelRatio()) || canvas.height !== Math.round(hgt * renderer.getPixelRatio())) renderer.setSize(w, hgt, false);
  renderer.setScissor(0, 0, w, hgt); renderer.setViewport(0, 0, w, hgt); renderer.clear();
  const now = performance.now() / 1000, gv = glbVersion();
  let builds = 0;
  for (const c of cards) {
    const r = c.view.getBoundingClientRect();
    if (r.bottom < 0 || r.top > hgt || r.right < 0 || r.left > w || r.width < 4) continue;
    if (c.built && c.item.kind === 'building' && c.glb !== gv) drop(c);   // (its real model arrived)
    if (!c.built) { if (builds++ >= 3) continue; try { buildModel(c); } catch (err) { console.warn('[vitrin]', c.item.id, err); c.built = true; c.scene = null; } }
    if (!c.scene) continue;
    if (c.v && c.animated) {
      const e = entityAt(c, now);
      try { poseUnitModel(c.v, e, now + c.i * .7, now); } catch (err) { if (!c.warned) { c.warned = true; console.warn('[vitrin] pose', c.item.id, err); } }
      if (c.stateEl && c.stateEl.dataset.s !== e.anim) { c.stateEl.dataset.s = e.anim; c.stateEl.textContent = STATE_TR[e.anim] || ''; }
      c.root.rotation.y = -.5 + Math.sin(now * .25 + c.i) * .45;        // a slow look from both sides
    } else c.root.rotation.y = now * (c.item.kind === 'building' ? .22 : .35) + c.i;   // a turntable
    const x = Math.max(0, r.left), y = Math.max(0, hgt - r.bottom);
    renderer.setViewport(r.left, hgt - r.bottom, r.width, r.height);
    renderer.setScissor(x, y, Math.min(w, r.right) - x, Math.min(hgt, hgt - r.top) - y);
    c.cam.aspect = r.width / r.height; c.cam.updateProjectionMatrix();
    renderer.render(c.scene, c.cam);
  }
}
draw();
frame();
