// Aevum - builds assets/icons/icons.svg (one SVG sprite) from game-icons.net icons (CC BY 3.0).
// The mapping key -> author/name is tools/icons-map.json; every icon is copied into the repo (no runtime
// dependency) and its author is listed in assets/icons/LICENSE.md.
// Run: node tools/build-icons.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const MAP = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools', 'icons-map.json'), 'utf8'));
const BASE = 'https://cdn.jsdelivr.net/gh/game-icons/icons@master/';
const out = [], authors = new Map(), cache = new Map();

for (const [key, src] of Object.entries(MAP)) {
  if (!/^[a-z0-9-]+$/.test(key) || !/^[a-z0-9-]+\/[a-z0-9-]+$/.test(src)) throw new Error('bad entry ' + key);
  let svg = cache.get(src);
  if (!svg) {
    const r = await fetch(BASE + src + '.svg');
    if (!r.ok) throw new Error(src + ': HTTP ' + r.status);
    svg = await r.text(); cache.set(src, svg);
  }
  // keep the drawing paths only: drop the black square background and every fill / style
  const paths = [...svg.matchAll(/<path\b[^>]*\bd="([^"]+)"[^>]*>/g)].map(m => m[1]).filter(d => d !== 'M0 0h512v512H0z');
  if (!paths.length) throw new Error(src + ': no path');
  for (const d of paths) if (!/^[MmLlHhVvCcSsQqTtAaZz0-9.,\s-]+$/.test(d)) throw new Error(src + ': unexpected path data');
  out.push(`<symbol id="gi-${key}" viewBox="0 0 512 512">${paths.map(d => `<path d="${d}"/>`).join('')}</symbol>`);
  const a = src.split('/')[0];
  if (!authors.has(a)) authors.set(a, []);
  authors.get(a).push(src.split('/')[1]);
}

const dir = path.join(ROOT, 'assets', 'icons');
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(path.join(dir, 'icons.svg'), `<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n${out.join('\n')}\n</svg>\n`);
const lic = ['# Icons', '', 'All icons in `icons.svg` come from https://game-icons.net and are licensed under',
  '[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Colours were removed (the game tints them).', '',
  '| Author | Icons |', '|---|---|',
  ...[...authors].sort().map(([a, l]) => `| ${a} | ${[...new Set(l)].sort().join(', ')} |`), ''];
fs.writeFileSync(path.join(dir, 'LICENSE.md'), lic.join('\n'));
console.log('icons:', out.length, 'files:', cache.size, 'bytes:', fs.statSync(path.join(dir, 'icons.svg')).size);
