// Sandbox: any age in one call (devSetAge), "Anında" (cfg.instant) finishes foundations and queues at once
import { Game } from '../src/sim/game.js';
import { BUILDINGS } from '../src/data.js';
let fail = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fail++; };
const g = new Game({ mapSize: 256, enemies: 1, difficulty: 'normal', startRes: 'high', startAge: 0, sandbox: true, seed: 11 });
const p = g.players[g.me];
ok(g.devSetAge(4) && p.age === 4, 'sandbox: son çağa doğrudan geçildi');
ok(g.devSetAge(1) && p.age === 1, 'sandbox: geri çağa da geçilir');
g.devSetAge(4);
// place a building of the last age next to the town centre and check it stands up at once
const tc = g.buildings.find((b) => b.owner === g.me && b.type === 'towncenter');
const late = Object.keys(BUILDINGS).filter((t) => BUILDINGS[t].age >= 3 && !BUILDINGS[t].legacy && g.isUnlocked(g.me, 'building', t));
let placed = null;
outer: for (const t of late) for (let r = 6; r < 30; r += 2) for (let a = 0; a < 16; a++) {
  const x = Math.round(tc.x + Math.cos(a / 16 * 6.283) * r), z = Math.round(tc.z + Math.sin(a / 16 * 6.283) * r);
  if (g.canPlace(t, x, z, g.me)) { placed = g.placeBuilding(g.me, t, x, z, []); if (placed) break outer; }
}
ok(!!placed, 'son çağ binası yerleştirildi: ' + (placed && placed.type));
for (let i = 0; i < 3; i++) g.update(0.05);
const b = placed && (typeof placed === 'object' ? placed : g.entities.get(placed));
ok(b && b.done, 'Anında: bina hemen bitti');
const v = g.units.find((u) => u.owner === g.me && u.type === 'villager');
ok(g.train(tc.id, 'villager'), 'köylü sıraya girdi');
const n = g.units.filter((u) => u.owner === g.me).length; g.update(0.05); g.update(0.05);
ok(g.units.filter((u) => u.owner === g.me).length > n, 'Anında: birlik hemen çıktı');
g.cfg.instant = false;
ok(g.train(tc.id, 'villager'), 'köylü sıraya girdi (Anında kapalı)');
const n2 = g.units.filter((u) => u.owner === g.me).length; g.update(0.05);
ok(g.units.filter((u) => u.owner === g.me).length === n2, 'Anında kapalı: birlik beklemeli');
const g2 = new Game({ mapSize: 256, enemies: 1, startAge: 0, sandbox: false, seed: 11 });
ok(!g2.devSetAge(3), 'normal oyunda çağ atlatılamaz');
console.log(fail ? fail + ' FAIL' : 'hepsi geçti'); process.exit(fail ? 1 : 0);
