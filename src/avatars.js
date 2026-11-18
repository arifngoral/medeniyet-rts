// Aevum - player avatars: original low-poly emblems (inline SVG, made for Aevum), gold on dark like the UI.
// Data only (no DOM): the cloud profile stores the avatar id; src/ui/avatar-ui.js draws them.
// Every account starts with defaultAvatar(uid) and can pick another one in Profil.

const G1 = '#f0cf7a', G2 = '#c99a45', G3 = '#8a6326', DK = '#1a1408';
const poly = (pts, fill) => `<polygon points="${pts}" fill="${fill}"/>`;
const leaf = (cx, cy, rot, fill) => `<ellipse cx="${cx}" cy="${cy}" rx="2.6" ry="5.4" transform="rotate(${rot} ${cx} ${cy})" fill="${fill}"/>`;
function laurel() {
  let s = '';
  for (let i = 0; i < 6; i++) {
    const deg = 250 - i * 22, a = deg * Math.PI / 180, r = 18;
    const x = 32 + Math.cos(a) * r, y = 33 - Math.sin(a) * r;
    const xs = x.toFixed(1), ys = y.toFixed(1), xm = (64 - x).toFixed(1);
    s += leaf(xs, ys, (180 - deg).toFixed(0), i % 2 ? G2 : G1) + leaf(xm, ys, (deg - 180).toFixed(0), i % 2 ? G1 : G2);
  }
  return s + poly('29,51 32,47 35,51 32,55', G2);
}
function gear() {
  let pts = '';
  for (let i = 0; i < 16; i++) {
    const a = i * Math.PI / 8 + Math.PI / 16, r = i % 2 ? 13 : 18;
    for (const d of [-0.16, 0.16]) pts += (32 + Math.cos(a + d) * r).toFixed(1) + ',' + (32 + Math.sin(a + d) * r).toFixed(1) + ' ';
  }
  return poly(pts.trim(), G1) + `<circle cx="32" cy="32" r="8" fill="${G3}"/><circle cx="32" cy="32" r="4.5" fill="${DK}"/>` +
    poly('32,19 38,24 32,26', G2) + poly('45,32 40,38 38,32', G2);
}

// [id, Turkish name, background, glyph markup]
const DEFS = [
  ['helm', 'Miğfer', '#3a1c1c', poly('20,31 23,19 32,13 41,19 44,31', G1) + poly('32,13 41,19 44,31 32,28', G2) + poly('20,31 32,28 32,34 26,35', G2) +
    poly('20,31 26,35 27,49 20,46', G1) + poly('44,31 38,35 37,49 44,46', G2) + poly('29,35 35,35 33,49 31,49', DK) + poly('22,15 32,5 42,15 37,13 32,9 27,13', '#c0452f')],
  ['crown', 'Taç', '#2a1a3a', poly('15,43 15,23 24,32 32,16 40,32 49,23 49,43', G1) + poly('32,16 40,32 49,23 49,43 32,43', G2) + poly('15,43 49,43 49,50 15,50', G3) +
    `<circle cx="32" cy="36" r="3.2" fill="#c0452f"/><circle cx="22" cy="40" r="2.2" fill="#3f8fc0"/><circle cx="42" cy="40" r="2.2" fill="#3f8fc0"/>`],
  ['laurel', 'Defne', '#1c2f22', laurel() + poly('32,22 35,30 43,30 37,35 39,43 32,38 25,43 27,35 21,30 29,30', G1) + poly('32,22 35,30 43,30 37,35 39,43 32,38', G2)],
  ['tower', 'Kale', '#1d2433', poly('20,24 20,17 24,17 24,21 28,21 28,17 32,17 32,21 36,21 36,17 40,17 40,21 44,21 44,17 44,24', G1) +
    poly('22,24 42,24 42,52 22,52', G2) + poly('32,24 42,24 42,52 32,52', G3) + poly('28,52 28,43 32,39 36,43 36,52', DK) + poly('30,30 34,30 34,35 30,35', DK)],
  ['swords', 'Kılıçlar', '#33261a', `<g transform="rotate(45 32 32)">${poly('30,8 34,8 34,42 32,46 30,42', G1)}${poly('32,8 34,8 34,42 32,46', G2)}${poly('25,42 39,42 39,45 25,45', G3)}${poly('30.5,45 33.5,45 33.5,54 30.5,54', G3)}</g>` +
    `<g transform="rotate(-45 32 32)">${poly('30,8 34,8 34,42 32,46 30,42', G1)}${poly('32,8 34,8 34,42 32,46', G2)}${poly('25,42 39,42 39,45 25,45', G3)}${poly('30.5,45 33.5,45 33.5,54 30.5,54', G3)}</g>`],
  ['shield', 'Kalkan', '#1a2a3a', poly('16,14 48,14 48,32 32,54 16,32', G1) + poly('32,14 48,14 48,32 32,54', G2) + poly('16,22 32,34 48,22 48,28 32,40 16,28', '#2c5d8a') +
    poly('32,34 48,22 48,28 32,40', '#22486c')],
  ['bow', 'Yay', '#22301c', `<path d="M24 10 Q48 32 24 54" stroke="${G1}" stroke-width="4.5" fill="none" stroke-linecap="round"/>` +
    `<line x1="24" y1="10" x2="24" y2="54" stroke="${G3}" stroke-width="1.5"/>` + poly('14,31 46,31 46,33 14,33', G2) + poly('46,28 54,32 46,36', G1) + poly('12,28 17,32 12,36 15,32', '#c0452f')],
  ['ship', 'Gemi', '#14283a', poly('12,40 52,40 46,50 18,50', G2) + poly('32,40 52,40 46,50 32,50', G3) + poly('31,12 33,12 33,40 31,40', G3) +
    poly('33,14 50,36 33,36', G1) + poly('31,18 16,36 31,36', G2) + poly('33,10 41,13 33,16', '#c0452f')],
  ['eagle', 'Kartal', '#2e2318', poly('32,20 36,26 32,44 28,26', G1) + poly('28,26 8,18 14,30 26,34', G1) + poly('36,26 56,18 50,30 38,34', G2) +
    poly('26,34 14,30 18,38', G2) + poly('38,34 50,30 46,38', G3) + poly('29,44 32,52 35,44', G2) + poly('30,16 34,16 36,21 32,23 28,21', G1) + poly('34,18 39,19 35,21', '#c0452f')],
  ['wolf', 'Kurt', '#262a30', poly('18,12 26,24 20,30', G2) + poly('46,12 38,24 44,30', G3) + poly('20,30 26,24 32,26 38,24 44,30 40,42 32,52 24,42', G1) +
    poly('32,26 38,24 44,30 40,42 32,52', G2) + poly('24,32 29,34 25,36', DK) + poly('40,32 35,34 39,36', DK) + poly('29,46 35,46 32,51', DK)],
  ['axe', 'Balta', '#3a2216', poly('31,8 33,8 33,56 31,56', G3) + poly('33,14 50,8 54,24 50,40 33,34', G1) + poly('33,24 54,24 50,40 33,34', G2) +
    poly('31,16 18,12 14,24 18,34 31,30', G2) + poly('31,24 14,24 18,34 31,30', G3)],
  ['pyramid', 'Piramit', '#33280f', `<circle cx="44" cy="18" r="6" fill="#e07a2f"/>` + poly('10,50 32,16 54,50', G1) + poly('32,16 54,50 36,50', G2) + poly('20,50 32,32 36,50', G3) +
    poly('8,50 56,50 56,53 8,53', G3)],
  ['banner', 'Sancak', '#341a24', poly('16,8 19,8 19,56 16,56', G3) + poly('19,10 48,14 42,23 48,32 19,30', '#c0452f') + poly('19,20 44,22 42,23 48,32 19,30', '#8f2f22') +
    poly('26,16 30,13 34,16 32,22 28,22', G1) + `<circle cx="17.5" cy="7" r="3" fill="${G1}"/>`],
  ['gear', 'Çark', '#1f2a2a', gear()],
  ['star', 'Yıldız', '#151b33', `<ellipse cx="32" cy="32" rx="24" ry="9" transform="rotate(-25 32 32)" stroke="${G3}" stroke-width="2" fill="none"/>` +
    poly('32,12 37,26 52,26 40,35 44,50 32,41 20,50 24,35 12,26 27,26', G1) + poly('32,12 37,26 52,26 40,35 44,50 32,41', G2) + `<circle cx="51" cy="22" r="2.5" fill="#3f8fc0"/>`],
  ['horse', 'At', '#2a2033', poly('22,52 24,34 18,30 22,18 30,12 38,14 46,24 44,30 38,26 34,30 38,52', G1) + poly('30,12 38,14 46,24 44,30 38,26', G2) +
    poly('22,18 30,12 28,22 20,26', '#c0452f') + `<circle cx="37" cy="19" r="1.6" fill="${DK}"/>` + poly('34,30 38,52 30,52', G2)],
];

export const AVATARS = DEFS.map(([id, name, bg, glyph]) => ({
  id, name, bg,
  svg: `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">` +
    `<circle cx="32" cy="32" r="31" fill="${bg}"/><circle cx="32" cy="32" r="29" fill="none" stroke="${G2}" stroke-opacity="0.55" stroke-width="1.5"/>${glyph}</svg>`,
}));
export const AVATAR_IDS = AVATARS.map((a) => a.id);
export const isAvatar = (id) => typeof id === 'string' && AVATAR_IDS.includes(id);
// the automatic avatar of a new account: picked from the profile uid (stable, spread over the set)
export function defaultAvatar(uid) {
  const s = String(uid || '');
  let h = 2166136261 >>> 0;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return AVATAR_IDS[h % AVATAR_IDS.length];
}
export const avatarOf = (id, uid) => (isAvatar(id) ? id : defaultAvatar(uid));
export const avatarById = (id) => AVATARS.find((a) => a.id === id) || null;
