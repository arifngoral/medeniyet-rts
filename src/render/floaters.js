// Aevum - floating "+13" numbers that rise and fade over a drop-off building when the local player's workers
// deposit resources (view only; owner 2026-11-14). Not a toast, no sound. A small pool of DOM elements, moved
// with a transform each frame; deposits at the same building within a moment add up into one number.
import { RES_ICONS } from '../icons.js';

const MAX = 24;        // pooled elements (at most this many numbers on screen)
const LIFE = 1.6;      // seconds a number lives
const RISE = 42;       // pixels it rises over its life
const MERGE = 0.55;    // a deposit at the same place within this many seconds adds to the young number

export class Floaters {
  constructor(camera) {
    this.camera = camera;
    this.root = null;
    this.free = [];
    this.live = [];
    this._v = null;
  }

  _ensure() {
    if (this.root || typeof document === 'undefined') return !!this.root;
    this.root = document.createElement('div');
    this.root.className = 'floaters';
    document.body.appendChild(this.root);
    for (let i = 0; i < MAX; i++) {
      const node = document.createElement('div');
      node.className = 'floater';
      const ic = document.createElement('span'), txt = document.createElement('b');
      node.append(txt, ic);
      this.root.appendChild(node);
      this.free.push({ node, ic, txt, res: '', key: null, x: 0, y: 0, z: 0, t: 0, amount: 0, shown: false });
    }
    return true;
  }

  // a number at world point (x, y, z); key = the building (or unit) id, for merging
  add(x, y, z, res, amount, key, vec) {
    if (!(amount > 0) || !this._ensure()) return;
    for (let i = 0; i < this.live.length; i++) {
      const f = this.live[i];
      if (f.key === key && f.res === res && f.t < MERGE) { f.amount += amount; f.txt.textContent = '+' + Math.round(f.amount); return; }
    }
    // on screen at all? (off-screen deposits show nothing)
    const v = vec.set(x, y, z).project(this.camera);
    if (v.z < -1 || v.z > 1 || v.x < -1.05 || v.x > 1.05 || v.y < -1.05 || v.y > 1.05) return;
    const f = this.free.pop() || this.live.shift();   // (pool empty: reuse the oldest)
    if (!f) return;
    if (f.res !== res) { f.res = res; f.node.className = 'floater ' + res; f.ic.innerHTML = RES_ICONS[res] || ''; }
    f.key = key; f.x = x; f.y = y; f.z = z; f.t = 0; f.amount = amount;
    f.txt.textContent = '+' + Math.round(amount);
    this.live.push(f);
  }

  update(dt, vec) {
    if (!this.live.length) return;
    const w = window.innerWidth, h = window.innerHeight;
    for (let i = this.live.length - 1; i >= 0; i--) {
      const f = this.live[i];
      f.t += dt;
      if (f.t >= LIFE) { this._hide(f); this.live.splice(i, 1); this.free.push(f); continue; }
      const v = vec.set(f.x, f.y, f.z).project(this.camera);
      if (v.z < -1 || v.z > 1 || v.x < -1.1 || v.x > 1.1 || v.y < -1.1 || v.y > 1.1) { this._hide(f); continue; }
      const k = f.t / LIFE, sx = (v.x * 0.5 + 0.5) * w, sy = (-v.y * 0.5 + 0.5) * h - RISE * (1 - (1 - k) * (1 - k));
      const a = k < 0.12 ? k / 0.12 : k > 0.6 ? 1 - (k - 0.6) / 0.4 : 1;
      const s = k < 0.12 ? 0.85 + 0.15 * (k / 0.12) : 1;
      if (!f.shown) { f.shown = true; f.node.style.display = 'flex'; }
      f.node.style.transform = `translate(${sx.toFixed(1)}px, ${sy.toFixed(1)}px) translate(-50%, -100%) scale(${s.toFixed(3)})`;
      f.node.style.opacity = a.toFixed(3);
    }
  }

  _hide(f) { if (f.shown) { f.shown = false; f.node.style.display = 'none'; } }

  clear() {
    for (const f of this.live) { this._hide(f); this.free.push(f); }
    this.live.length = 0;
  }
}
