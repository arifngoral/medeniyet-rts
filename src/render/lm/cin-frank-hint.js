// Age-up building models (landmarks.js looks) of the Chinese, the Franks and the Indians. See index.js.
export default function (K) {
  const { THREE, PI, G, MT, XM, LMM, mat, mk, bx, cy, cn, py, sp, lmFlag, lmDome, lmGable, lmMinaret, lmCols, lmCren, lmTower, lmWall, lmPagoda, lmSteps, lmArch, lmShip } = K;
  const M = {
    yel: mat(0xd9a52a, .5), grn: mat(0x3e8a5a, .45), blu: mat(0x2c4c9c, .45), gb: mat(0x86827a, .9), terra: mat(0xb07048, .95),
    porc: mat(0xf3f2ec, .35), door: mat(0x2a2a30, .8), junk: mat(0x8a4a2a, .9),
    slate: mat(0x4a5262, .7), lime: mat(0xd9d0bb, .9), cream: mat(0xe6dac0, .85), cstone: mat(0xcab98f, .9),
    rose: mat(0x3a54a8, .3), rosered: mat(0xa83030, .3),
    redsand: mat(0xa64a32, .9), ochre: mat(0xd6b066, .9), pink: mat(0xd88c6c, .9), granite: mat(0xbcae94, .95), elef: mat(0x7c7670, .9),
    sandst: mat(0xc9a676, .95), rock: mat(0x9a8468, .95), taj: mat(0xf2eee6, .55), shade: mat(0xcfc8b8, .8), paint: mat(0x3c7a6a, .8),
    stambha: mat(0xd2b07a, .9), tent: mat(0xe08a22, .9),
  };
  const SPICE = [mat(0xe0a81c, .95), mat(0xb42a1a, .95), mat(0xe06a18, .95), mat(0x8c5a2c, .95), mat(0x6e8c3a, .95), mat(0x2e2620, .95)];

  // a Chinese hip-and-gable roof over an X × Z hall (ridge along x), the eave at y: upturned corners, ridge beasts
  function hip(c, m, X, Z, h, x, y, z) {
    py(c.roof, m, X, h * .5, Z, x, y, z);
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = PI / 2; c.roof.add(g); mk(G.prism, g, m, Z * .55, h, X * .7, 0, 0, 0);
    bx(c.roof, m, X * .74, .06, .07, x, y + h - .03, z);
    for (const s of [-1, 1]) bx(c.roof, MT.gold, .06, .14, .06, x + s * X * .36, y + h - .04, z);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const o = cn(c.roof, m, .045, .22, x + sx * X * .46, y + .02, z + sz * Z * .46); o.rotation.z = -sx * .9; o.rotation.x = sz * .9; }
  }
  // an Indian chhatri: a domed kiosk on four slim pillars
  function chhatri(c, x, y, z, s, m = LMM.white, dm = m) {
    bx(c.body, m, s, s * .12, s, x, y, z);
    for (const a of [-1, 1]) for (const b of [-1, 1]) cy(c.body, m, s * .07, s * .7, x + a * s * .38, y + s * .12, z + b * s * .38);
    bx(c.body, m, s * 1.1, s * .1, s * 1.1, x, y + s * .82, z);
    lmDome(c, dm, s * .42, x, y + s * .92, z, 1.15);
    sp(c.roof, MT.gold, s * .05, x, y + s * 1.42, z);
  }
  const grp = (c, x, z, ry = 0) => { const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; c.body.add(g); return g; };

  return {
    // ================= Çinliler =================
    pirincteras(c) {   // rice terraces down a hillside: earth steps, flooded paddies, young rice, a farmhouse at the top
      for (let i = 0; i < 5; i++) {
        const d = 3.5 - i * .62, z = -1.75 + d / 2, y = i * .26, w = 3.6 - i * .12, x = (i & 1) ? .07 : -.07, fz = z + d / 2;
        bx(c.body, i & 1 ? MT.soil2 : MT.soil, w, .26, d, x, y, z);
        if (i < 4) {
          bx(c.body, i & 1 ? MT.sprout : LMM.water, w - .2, .025, .5, x, y + .26, fz - .32);
          bx(c.body, LMM.turf, w, .06, .07, x, y + .26, fz - .04);
          if (!(i & 1)) for (let k = 0; k < 6; k++) bx(c.body, MT.green, .09, .1, .3, -1.35 + k * .54 + x, y + .27, fz - .32);
        }
      }
      bx(c.body, MT.plaster, .9, .45, .55, -.7, 1.3, -1.3); bx(c.body, MT.dwood, .2, .3, .03, -.7, 1.3, -1.01);
      hip(c, LMM.dtile, 1.15, .78, .42, -.7, 1.75, -1.3); c.chim.push(-.45, 2.3, -1.3);
      bx(c.body, mat(0x4a4a48, .9), .2, .2, .42, 1.0, .3, 1.38); bx(c.body, mat(0x4a4a48, .9), .14, .14, .16, 1.0, .38, 1.66);
      for (const s of [-1, 1]) { const h = cn(c.body, XM.bone, .02, .12, 1.0 + s * .07, .5, 1.66); h.rotation.z = -s * 1.1; }
      bx(c.body, LMM.blue, .1, .25, .08, -.4, .26, 1.4); cn(c.body, MT.hay, .14, .1, -.4, .5, 1.4);
      lmFlag(c, 1.3, -1.45, 2.4);
    },
    topraksavasci(c) {   // the terracotta army: a pit of warriors in rows between earth ridges, the workshop and its kiln
      const T = M.terra;
      bx(c.body, MT.soil, 3.5, .03, 2.0, 0, 0, .75);
      for (const s of [-1, 1]) bx(c.body, MT.soil2, .18, .35, 2.1, s * 1.7, 0, .75);
      bx(c.body, MT.soil2, 3.58, .35, .18, 0, 0, 1.75); bx(c.body, MT.soil2, 3.58, .35, .18, 0, 0, -.25);
      for (const x of [-.84, 0, .84]) bx(c.body, MT.soil2, .14, .26, 1.7, x, 0, .78);
      for (const x of [-1.27, -.42, .42, 1.27]) for (const z of [.2, .75, 1.3]) {
        bx(c.body, T, .17, .26, .13, x, 0, z); bx(c.body, T, .21, .2, .15, x, .26, z); sp(c.body, T, .065, x, .53, z);
      }
      bx(c.body, MT.plaster, 2.2, .85, 1.0, -.6, 0, -1.25); bx(c.body, MT.black, .35, .55, .04, -.6, 0, -.74);
      hip(c, LMM.dtile, 2.6, 1.35, .55, -.6, .85, -1.25);
      cy(c.body, MT.brick, .42, .45, 1.2, 0, -1.2); lmDome(c, MT.brick, .42, 1.2, .45, -1.2, .8); bx(c.body, MT.glow, .22, .24, .04, 1.2, .05, -.79);
      cy(c.body, MT.brick, .08, .4, 1.2, .72, -1.2); c.chim.push(1.2, 1.2, -1.2);
      bx(c.body, MT.wood, .7, .2, .22, .45, 0, -.55); for (let i = 0; i < 3; i++) sp(c.body, T, .07, .25 + i * .2, .27, -.55);
      lmFlag(c, 1.75, -.5, 2.0);
    },
    buyukkanal(c) {   // the Grand Canal: stone quays, a moon bridge, a junk and a sampan, a warehouse and a crane, a pailou gate
      const S = MT.stone;
      bx(c.body, LMM.water, 3.8, .03, 1.2, 0, 0, .35);
      bx(c.body, S, 3.8, .22, 1.6, 0, 0, -1.05); bx(c.body, S, 3.8, .22, .9, 0, 0, 1.4);
      bx(c.body, MT.plaster, 2.0, .75, .85, .6, .22, -1.35); for (const x of [.1, 1.1]) bx(c.body, MT.dwood, .3, .45, .03, x, .22, -.92);
      hip(c, LMM.dtile, 2.4, 1.2, .5, .6, .97, -1.35);
      for (let i = 0; i < 3; i++) bx(c.body, MT.wood, .24, .24, .24, -.2 + i * .3, .22, -.5); cy(c.body, MT.canvas, .1, .22, .75, .22, -.5); cy(c.body, MT.canvas, .1, .22, .97, .22, -.45);
      cy(c.body, MT.dwood, .05, 1.35, -1.5, .22, -.65); bx(c.body, MT.dwood, .06, .06, 1.0, -1.5, 1.5, -.25);
      cy(c.body, MT.canvas, .01, .7, -1.5, .8, .2); bx(c.body, MT.wood, .2, .2, .2, -1.5, .62, .2);
      const b = grp(c, -.6, .35);   // the moon bridge: a solid half disc with the arch cut through it
      mk(G.wheel, b, S, .48, 1.2, 1.2, 0, .0, 0); mk(G.wheel, b, mat(0x1e2a36, .9), .5, .66, .66, 0, -.02, 0);
      for (const s of [-1, 1]) bx(b, LMM.white, .03, .1, .5, s * .25, .6, 0);
      const j = grp(c, .8, .4);   // a junk with battened sails
      bx(j, MT.dwood, 1.3, .2, .42, 0, .02, 0); bx(j, MT.dwood, .3, .2, .42, -.55, .2, 0); bx(j, MT.wood, .4, .2, .3, -.25, .22, 0);
      cy(j, MT.wood, .025, 1.3, .1, .22, 0); bx(j, M.junk, .6, .75, .02, .12, .55, 0); for (let i = 0; i < 4; i++) bx(j, MT.dwood, .62, .025, .03, .12, .6 + i * .18, 0);
      cy(j, MT.wood, .02, .8, .5, .22, 0); bx(j, M.junk, .3, .4, .02, .5, .5, 0); bx(j, c.cm, .02, .12, .2, .1, 1.45, .1);
      const s = grp(c, -1.4, .7);   // a sampan under its mat roof
      bx(s, MT.wood, .7, .12, .26, 0, .02, 0); mk(G.wheel, s, MT.hay, .35, .3, .3, -.05, .14, 0); cy(s, LMM.blue, .04, .2, .25, .14, 0); cn(s, MT.hay, .08, .06, .25, .34, 0);
      for (const sx of [-1, 1]) cy(c.body, LMM.lacq, .05, 1.0, -.6 + sx * .42, .22, 1.55);
      bx(c.body, LMM.lacq, 1.05, .1, .1, -.6, 1.0, 1.55); bx(c.body, MT.gold, .3, .14, .02, -.6, .82, 1.6); py(c.roof, M.grn, 1.25, .22, .32, -.6, 1.1, 1.55);
      for (const x of [.6, 1.0]) { cy(c.body, MT.dwood, .02, .9, x, .22, 1.2); sp(c.body, MT.red, .08, x, 1.05, 1.2); }
      lmFlag(c, 1.5, 1.3, 2.0);
    },
    seddkalesi(c) {   // a stretch of the Great Wall over a ridge: a gate tower with a pavilion, watchtowers, a barbican, a beacon
      const W = M.gb;
      bx(c.body, LMM.turf, 1.75, .4, 1.0, 1.05, 0, -.2);
      bx(c.body, W, 1.5, 1.0, .6, -1.15, 0, -.2); lmCren(c, W, 1.5, .6, 1.0, -1.15, -.2, .12);
      bx(c.body, W, 1.5, 1.4, .6, 1.15, 0, -.2); lmCren(c, W, 1.5, .6, 1.4, 1.15, -.2, .12);
      lmTower(c, -1.45, -.2, .75, 1.7, W); lmTower(c, 1.45, -.2, .75, 2.0, W);
      for (const [x, y] of [[-1.45, 1.05], [1.45, 1.3]]) bx(c.body, MT.black, .12, .25, .03, x, y, .18);
      sp(c.body, MT.glow, .1, 1.45, 2.2, -.2); c.chim.push(1.45, 2.35, -.2);
      bx(c.body, W, 1.15, 1.6, 1.05, 0, 0, -.2); lmCren(c, W, 1.15, 1.05, 1.6, 0, -.2, .12);
      bx(c.body, MT.black, .4, .72, .04, 0, 0, .33); mk(G.wheel, c.body, MT.black, .04, .4, .4, 0, .72, .33).rotation.y = PI / 2;
      bx(c.body, LMM.lacq, .85, .45, .7, 0, 1.6, -.2); lmCols(c, 4, -.38, .38, .17, .45, LMM.lacq, .035, 1.6);
      py(c.roof, LMM.dtile, 1.2, .2, 1.0, 0, 2.05, -.2); bx(c.body, LMM.lacq, .6, .25, .5, 0, 2.1, -.2); hip(c, LMM.dtile, 1.0, .8, .45, 0, 2.35, -.2);
      for (const s of [-1, 1]) { bx(c.body, W, .5, .7, .22, s * .45, 0, 1.05); bx(c.body, W, .22, .7, .72, s * .6, 0, .69); }
      for (const x of [-.9, .9]) { cy(c.body, MT.dwood, .02, .6, x, x < 0 ? 1.14 : 1.54, .0); bx(c.body, c.cm, .02, .25, .35, x, x < 0 ? 1.45 : 1.85, .17); }
      lmFlag(c, .45, -.55, 3.3);
    },
    yasaksehir(c) {   // the Forbidden City: red walls with yellow tile caps, the Meridian Gate, a great double-roofed hall on a marble terrace
      const R = LMM.lacq, Y = M.yel, W = LMM.white;
      bx(c.body, MT.stone, 3.6, .04, 3.6, 0, 0, 0);
      for (const s of [-1, 1]) { bx(c.body, R, .2, .7, 3.6, s * 1.75, 0, 0); bx(c.roof, Y, .32, .08, 3.6, s * 1.75, .7, 0); }
      bx(c.body, R, 3.3, .7, .2, 0, 0, -1.75); bx(c.roof, Y, 3.3, .08, .32, 0, .7, -1.75);
      for (const s of [-1, 1]) { bx(c.body, R, 1.1, .7, .2, s * 1.1, 0, 1.75); bx(c.roof, Y, 1.1, .08, .32, s * 1.1, .7, 1.75); }
      for (const s of [-1, 1]) { bx(c.body, R, .4, .9, .4, s * 1.6, 0, -1.6); py(c.roof, Y, .6, .35, .6, s * 1.6, .9, -1.6); }
      bx(c.body, R, 1.2, .85, .5, 0, 0, 1.6); bx(c.body, MT.black, .3, .5, .04, 0, 0, 1.86);
      bx(c.body, R, .9, .35, .32, 0, .85, 1.6); hip(c, Y, 1.25, .6, .35, 0, 1.2, 1.6);
      bx(c.body, LMM.water, 2.2, .02, .2, 0, .04, 1.1); for (const x of [-.5, 0, .5]) bx(c.body, W, .22, .06, .3, x, .04, 1.1);
      const t = lmSteps(c, W, 2.7, 1.8, 3, .14, 0, -.6, .2); bx(c.body, W, .5, .2, .3, 0, 0, .42);
      bx(c.body, R, 2.0, .7, 1.0, 0, t, -.65); lmCols(c, 8, -.9, .9, -.12, .7, R, .04, t); bx(c.body, MT.gold, 1.8, .06, .02, 0, t + .58, -.14);
      py(c.roof, Y, 2.6, .28, 1.55, 0, t + .7, -.65); bx(c.body, R, 1.6, .3, .75, 0, t + .82, -.65); hip(c, Y, 2.2, 1.2, .6, 0, t + 1.12, -.65);
      for (const s of [-1, 1]) { bx(c.body, R, .6, .5, 1.1, s * 1.15, 0, .85); lmGable(c, Y, .8, .35, 1.25, s * 1.15, .5, .85); }
      for (const s of [-1, 1]) { bx(c.body, W, .16, .14, .16, s * .45, 0, .75); sp(c.body, MT.bronze, .08, s * .45, .22, .75); }
      lmFlag(c, -1.4, 1.35, 2.0);
    },
    barutatolye(c) {   // the gunpowder works: a workshop with a forge, an earth-covered powder magazine, kegs, rocket carts, a bombard
      bx(c.body, MT.plaster, 2.2, .85, 1.0, -.6, 0, -1.25); hip(c, LMM.dtile, 2.6, 1.35, .5, -.6, .85, -1.25);
      bx(c.body, MT.glow, .3, .35, .04, -1.1, .15, -.74); bx(c.body, MT.black, .3, .55, .04, -.2, 0, -.74);
      cy(c.body, MT.brick, .13, 2.0, -1.4, 0, -1.55); c.chim.push(-1.4, 2.15, -1.55);
      cy(c.body, MT.stone, .55, .4, 1.15, 0, -1.15); lmDome(c, LMM.turf, .55, 1.15, .4, -1.15, .7); bx(c.body, MT.iron, .26, .38, .04, 1.15, 0, -.6);
      for (let i = 0; i < 5; i++) { const x = i < 3 ? .25 + i * .28 : .39 + (i - 3) * .28; cy(c.body, MT.wood, .13, .32, x, i < 3 ? 0 : .32, -.3); }
      for (const [x, z, a] of [[-1.0, .75, .25], [.05, 1.0, -.15]]) {
        const g = grp(c, x, z, a);
        bx(g, MT.dwood, .45, .08, .7, 0, .2, 0); for (const s of [-1, 1]) mk(G.wheel, g, MT.dwood, .05, .36, .36, s * .27, .18, -.1); bx(g, MT.dwood, .05, .05, .5, 0, .2, -.55);
        const l = new THREE.Group(); l.position.set(0, .28, .05); l.rotation.x = -.6; g.add(l);
        bx(l, MT.wood, .42, .34, .3, 0, 0, 0); bx(l, MT.black, .36, .28, .02, 0, .03, .15); bx(l, c.cm, .44, .05, .32, 0, .34, 0);
      }
      const r = cy(c.body, MT.red, .03, .3, 1.35, 1.45, 1.1); r.rotation.z = -.7; sp(c.body, MT.glow, .07, 1.25, 1.38, 1.1); c.chim.push(1.15, 1.3, 1.1);
      bx(c.body, MT.dwood, .35, .18, .8, 1.35, 0, .25); const bb = cy(c.body, MT.iron, .15, .85, 1.35, .3, -.15); bb.rotation.x = 1.35;
      bx(c.body, MT.stone, .2, .6, 1.6, -1.75, 0, .5); bx(c.body, MT.stone, 1.2, .6, .2, -1.25, 0, 1.6);
      for (const x of [-.45, .55]) { cy(c.body, MT.dwood, .025, 1.1, x, 0, 1.65); sp(c.body, MT.red, .09, x, 1.0, 1.65); }
      lmFlag(c, .4, -.65, 2.2);
    },
    porselenkule(c) {   // the Porcelain Tower of Nanjing: nine white tiers under green glazed eaves, a gilded spire, temple halls
      const P = M.porc, z0 = -.3;
      bx(c.body, MT.stone, 3.0, .15, 3.0, 0, 0, -.2); cy(c.body, MT.stone, .95, .3, 0, .15, z0);
      let y = .45, r = .7;
      for (let i = 0; i < 9; i++) {
        cy(c.body, P, r, .34, 0, y, z0); bx(c.body, i & 1 ? M.yel : M.door, .16, .2, .03, 0, y + .06, z0 + r + .005);
        cn(c.roof, M.grn, r * 1.45, .2, 0, y + .3, z0); y += .39; r -= .042;
      }
      cy(c.roof, LMM.goldm, .05, .45, 0, y - .1, z0); sp(c.roof, LMM.goldm, .1, 0, y + .4, z0); cn(c.roof, MT.gold, .04, .25, 0, y + .48, z0);
      for (const s of [-1, 1]) { bx(c.body, LMM.lacq, .8, .45, .55, s * 1.05, .15, .95); hip(c, M.yel, 1.05, .75, .35, s * 1.05, .6, .95); }
      sp(c.body, MT.bronze, .12, 0, .3, 1.1); cy(c.body, MT.stone, .14, .15, 0, .15, 1.1);
      lmFlag(c, 1.5, -1.5, 2.0);
    },
    cennettapinagi(c) {   // the Temple of Heaven: a round hall under three blue roofs on a triple white terrace with railings
      const W = LMM.white, B = M.blu, R = LMM.lacq, z0 = -.25;
      cy(c.body, W, 1.55, .18, 0, 0, z0); cy(c.body, W, 1.25, .18, 0, .18, z0); cy(c.body, W, .98, .18, 0, .36, z0);
      for (const [rr, y, n] of [[1.5, .18, 16], [.94, .54, 12]]) for (let i = 0; i < n; i++) { const a = (i + .5) / n * PI * 2; bx(c.body, W, .05, .13, .05, Math.sin(a) * rr, y, z0 + Math.cos(a) * rr); }
      for (let k = 0; k < 3; k++) bx(c.body, W, .45, .18 * (k + 1), .3, 0, 0, z0 + 1.62 - k * .3);
      cy(c.body, R, .8, .62, 0, .54, z0); cy(c.body, LMM.goldm, .81, .06, 0, 1.0, z0); bx(c.body, LMM.goldm, .3, .42, .03, 0, .56, z0 + .81);
      cn(c.roof, B, 1.08, .38, 0, 1.16, z0); cy(c.body, R, .62, .32, 0, 1.38, z0);
      cn(c.roof, B, .86, .32, 0, 1.68, z0); cy(c.body, R, .44, .3, 0, 1.86, z0);
      cn(c.roof, B, .64, .55, 0, 2.12, z0); sp(c.roof, LMM.goldm, .11, 0, 2.72, z0); cn(c.roof, MT.gold, .03, .2, 0, 2.8, z0);
      for (const x of [-.65, -.2, .2, .65]) { cy(c.body, W, .05, .9, x, 0, 1.72); sp(c.body, W, .07, x, .95, 1.72); }
      bx(c.body, R, 1.45, .08, .07, 0, .78, 1.72);
      for (const [x, z] of [[-1.6, -1.6], [1.6, -1.6], [-1.65, 1.3], [1.65, 1.3]]) { cy(c.body, LMM.bark, .05, .3, x, 0, z); cn(c.roof, LMM.pine, .25, .75, x, .3, z); }
      lmFlag(c, -1.0, 1.3, 1.9);
    },

    // ================= Franklar =================
    degirmenkoy(c) {   // a mill village: a half-timbered watermill with its wheel and flume on the stream, cottages, fields
      bx(c.body, LMM.water, .65, .03, 3.8, 1.4, 0, 0); for (const s of [-1, 1]) bx(c.body, MT.stone, .08, .12, 3.8, 1.4 + s * .36, 0, 0);
      bx(c.body, MT.stone, 1.4, .55, 1.1, .3, 0, -.7); bx(c.body, MT.plaster, 1.4, .6, 1.1, .3, .55, -.7);
      for (const x of [-.38, .1, .5, .98]) bx(c.body, MT.dwood, .06, .6, .03, x, .55, -.14);
      bx(c.body, MT.dwood, 1.42, .05, .03, .3, .84, -.14); bx(c.body, MT.dwood, .05, .66, .03, .3, .55, -.14).rotation.z = .6;
      bx(c.body, MT.dwood, .25, .4, .03, -.15, 0, -.14); lmGable(c, MT.tile, 1.6, .75, 1.25, .3, 1.15, -.7);
      bx(c.body, MT.stone, .16, .5, .16, -.1, 1.4, -1.0); c.chim.push(-.1, 2.0, -1.0);
      mk(G.wheel, c.body, MT.wood, .12, 1.0, 1.0, 1.1, .5, -.7); mk(G.wheel, c.body, MT.dwood, .16, .2, .2, 1.1, .5, -.7);
      for (let i = 0; i < 4; i++) mk(G.cbox, c.body, MT.dwood, .17, 1.08, .06, 1.1, .5, -.7).rotation.x = i * PI / 4;
      bx(c.body, MT.wood, .22, .1, .9, 1.15, 1.0, -1.35); bx(c.body, LMM.water, .14, .02, .9, 1.15, 1.1, -1.35); cy(c.body, MT.dwood, .03, 1.0, 1.15, 0, -1.7);
      bx(c.body, MT.plaster, .8, .55, .65, -1.3, 0, -1.3); lmGable(c, MT.thatch, .8, .55, .95, -1.3, .55, -1.3, PI / 2);
      bx(c.body, MT.plaster, .7, .5, .7, -1.35, 0, -.15); lmGable(c, MT.thatch, .85, .5, .85, -1.35, .5, -.15);
      bx(c.body, MT.dwood, .18, .32, .03, -1.35, 0, .21);
      bx(c.body, MT.wheat, 1.5, .14, .65, -.75, 0, .8); bx(c.body, MT.sprout, 1.5, .08, .65, -.75, 0, 1.55);
      cy(c.body, MT.hay, .25, .25, .55, 0, 1.25); cn(c.roof, MT.hay, .27, .4, .55, .25, 1.25);
      for (let i = 0; i < 3; i++) cy(c.body, MT.canvas, .1, .22, .5 + i * .22, 0, .05);
      bx(c.body, MT.wood, .9, .05, .4, 1.4, .1, 1.1);
      lmFlag(c, -.55, -1.35, 2.2);
    },
    motte(c) {   // motte-and-bailey: a wooden keep on an earth mound ringed by stakes, a flying bridge down to the palisaded bailey
      const mx = -.55, mz = -.6;
      lmDome(c, LMM.turf, 1.1, mx, 0, mz, .9); cy(c.body, MT.soil2, .58, .06, mx, .9, mz);
      bx(c.body, MT.wood, .65, 1.1, .65, mx, .93, mz); bx(c.body, MT.dwood, .85, .35, .85, mx, 2.03, mz); py(c.roof, MT.dwood, 1.05, .6, 1.05, mx, 2.38, mz);
      for (let i = 0; i < 3; i++) bx(c.body, MT.black, .08, .16, .02, mx - .25 + i * .25, 2.13, mz + .43);
      bx(c.body, MT.dwood, .2, .35, .02, mx, .93, mz + .33);
      for (let i = 0; i < 12; i++) { const a = i / 12 * PI * 2; if (i === 1) continue; cy(c.body, MT.dwood, .04, .55, mx + Math.sin(a) * .62, .7, mz + Math.cos(a) * .62); }
      const bc = [.55, .65], R = 1.2;
      for (let i = 0; i < 18; i++) {
        const a = i / 18 * PI * 2, x = bc[0] + Math.sin(a) * R, z = bc[1] + Math.cos(a) * R;
        if (i === 0 || Math.hypot(x - mx, z - mz) < 1.1) continue;
        cy(c.body, MT.dwood, .07, .75, x, 0, z); cn(c.body, MT.dwood, .07, .14, x, .75, z);
      }
      for (const s of [-1, 1]) cy(c.body, MT.dwood, .08, 1.05, bc[0] + s * .24, 0, bc[1] + R);
      bx(c.body, MT.wood, .6, .12, .14, bc[0], .92, bc[1] + R);
      bx(c.body, MT.wood, 1.0, .5, .55, .75, 0, .55); lmGable(c, MT.thatch, .7, .45, 1.15, .75, .5, .55, PI / 2); c.chim.push(1.0, 1.1, .55);
      bx(c.body, MT.dwood, .5, .4, .45, 1.2, 0, 1.25); lmGable(c, MT.thatch, .6, .3, .55, 1.2, .4, 1.25);
      cy(c.body, MT.stone, .14, .2, -.05, 0, 1.3);
      const A = [-.05, 0, 1.0], B = [-.4, .95, -.15], dx = B[0] - A[0], dy = B[1] - A[1], dz = B[2] - A[2], hz = Math.hypot(dx, dz);
      const g = new THREE.Group(); g.position.set((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, (A[2] + B[2]) / 2); g.rotation.y = Math.atan2(dx, dz); c.body.add(g);
      mk(G.cbox, g, MT.wood, .3, .05, Math.hypot(hz, dy), 0, 0, 0).rotation.x = -Math.atan2(dy, hz);
      for (const t of [.33, .66]) cy(c.body, MT.dwood, .03, A[1] + dy * t, A[0] + dx * t, 0, A[2] + dz * t);
      lmFlag(c, mx, mz, 3.5);
    },
    aachen(c) {   // Charlemagne's palace: the octagonal Palatine Chapel with its westwork, the brick aula with its apse
      const S = M.lime, cx = -.55, cz = -.35;
      cy(c.body, S, 1.05, 1.1, cx, 0, cz); cn(c.roof, LMM.lead, 1.12, .35, cx, 1.1, cz);
      cy(c.body, S, .68, .75, cx, 1.2, cz); lmDome(c, M.slate, .7, cx, 1.95, cz, .75);
      cy(c.roof, S, .12, .2, cx, 2.4, cz); sp(c.roof, MT.gold, .07, cx, 2.68, cz);
      for (const a of [-.9, -.3, .3, .9]) { bx(c.body, MT.black, .12, .3, .03, cx + Math.sin(a) * .69, 1.4, cz + Math.cos(a) * .69).rotation.y = a; bx(c.body, MT.black, .14, .35, .03, cx + Math.sin(a * 1.3) * 1.06, .4, cz + Math.cos(a * 1.3) * 1.06).rotation.y = a * 1.3; }
      bx(c.body, S, .75, 2.3, .55, cx, 0, cz + 1.25); py(c.roof, M.slate, .8, 1.2, .62, cx, 2.3, cz + 1.25);
      for (const s of [-1, 1]) { cy(c.body, S, .17, 1.9, cx + s * .5, 0, cz + 1.1); cn(c.roof, M.slate, .19, .45, cx + s * .5, 1.9, cz + 1.1); }
      bx(c.body, LMM.bronze, .3, .6, .03, cx, 0, cz + 1.53); bx(c.body, MT.black, .26, .55, .03, cx, 1.15, cz + 1.53); bx(c.body, c.cm, .36, .4, .02, cx, .68, cz + 1.54);
      bx(c.body, MT.brick, .9, 1.35, 2.5, 1.25, 0, -.15); lmGable(c, MT.tile, 1.0, .55, 2.55, 1.25, 1.35, -.15);
      cy(c.body, MT.brick, .42, 1.2, 1.25, 0, -1.4); lmDome(c, MT.tile, .44, 1.25, 1.2, -1.4, .6);
      for (let i = 0; i < 4; i++) bx(c.body, MT.black, .03, .55, .16, .79, .5, -1.0 + i * .55); bx(c.body, MT.black, .2, .5, .03, 1.25, .6, 1.11);
      bx(c.body, S, .45, 1.9, .45, 1.55, 0, 1.05); py(c.roof, M.slate, .55, .45, .55, 1.55, 1.9, 1.05);
      bx(c.body, S, .45, .8, .45, .65, 0, -.35);
      lmFlag(c, -1.65, 1.2, 2.2);
    },
    turnuva(c) {   // the tournament lists: a striped tilt barrier, two knights charging, striped stands with the royal box, pavilion tents
      bx(c.body, LMM.sand, 3.6, .03, 2.4, 0, 0, .45);
      for (let i = 0; i < 6; i++) bx(c.body, i & 1 ? MT.white : c.cm, .5, .42, .08, -1.25 + i * .5, 0, .3);
      for (const x of [-1.52, 1.52]) cy(c.body, MT.dwood, .05, .55, x, 0, .3);
      bx(c.body, MT.wood, 3.4, .25, .9, 0, 0, -1.35); bx(c.body, MT.wood, 3.4, .25, .6, 0, .25, -1.5); bx(c.body, MT.wood, 3.4, .25, .3, 0, .5, -1.65);
      for (const x of [-1.65, -.55, .55, 1.65]) cy(c.body, MT.dwood, .035, 1.3, x, 0, -.92);
      for (let i = 0; i < 7; i++) bx(c.roof, i & 1 ? MT.white : c.cm, .49, .05, 1.0, -1.47 + i * .49, 1.3, -1.38).rotation.x = .15;
      bx(c.body, LMM.lacq, .7, .3, .25, 0, .75, -1.6); lmGable(c, LMM.goldm, .8, .4, .6, 0, 1.38, -1.38);
      for (let i = 0; i < 4; i++) { const x = -1.3 + i * .87 + (i > 1 ? .1 : 0); bx(c.body, [LMM.blue, LMM.sail1, MT.green, LMM.goldm][i], .14, .16, .1, x, .5, -1.45); sp(c.body, MT.skin, .055, x, .72, -1.45); }
      for (const [x, k] of [[-1.45, 0], [1.45, 1]]) { cy(c.body, MT.white, .36, .5, x, 0, 1.4); cn(c.roof, k ? LMM.sail1 : c.cm, .42, .5, x, .5, 1.4); sp(c.roof, MT.gold, .04, x, 1.02, 1.4); bx(c.body, k ? LMM.sail1 : c.cm, .15, .4, .02, x, 0, 1.76); }
      const knight = (x, z, ry, hm, cm2) => {
        const g = grp(c, x, z, ry);
        for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(g, hm, .035, .36, sx * .09, 0, sz * .24);
        bx(g, hm, .24, .26, .66, 0, .34, 0); bx(g, cm2, .28, .24, .7, 0, .3, 0);
        bx(g, hm, .13, .32, .14, 0, .5, .28).rotation.x = .5; bx(g, hm, .12, .13, .26, 0, .74, .42);
        bx(g, MT.steel, .2, .3, .16, 0, .6, -.05); sp(g, MT.steel, .08, 0, .98, -.05); bx(g, cm2, .04, .24, .18, -.13, .62, 0);
        cy(g, MT.white, .025, 1.3, .13, .78, -.1).rotation.x = PI / 2 - .08;
      };
      knight(-.95, .64, PI / 2, MT.white, c.cm); knight(.95, -.04, -PI / 2, LMM.black, LMM.sail1);
      lmFlag(c, -1.75, .3, 2.0);
    },
    notredame(c) {   // Notre-Dame: a gothic nave and transept under lead roofs, flying buttresses, a spire, twin towers and the rose window
      const S = M.lime, L = LMM.lead;
      bx(c.body, S, 1.2, 1.9, 1.95, 0, 0, -.25); lmGable(c, L, 1.25, .9, 1.95, 0, 1.9, -.25);
      for (const s of [-1, 1]) { bx(c.body, S, .45, 1.0, 1.95, s * .82, 0, -.25); bx(c.roof, L, .5, .06, 1.95, s * .82, 1.0, -.25); }
      bx(c.body, S, 2.6, 1.8, .6, 0, 0, -.55); lmGable(c, L, .62, .85, 2.6, 0, 1.8, -.55, PI / 2);
      for (const s of [-1, 1]) mk(G.wheel, c.body, M.rose, .04, .4, .4, s * 1.3, 1.2, -.55);
      cy(c.body, S, .6, 1.9, 0, 0, -1.2); cn(c.roof, L, .63, .8, 0, 1.9, -1.2);
      for (const z of [-1.05, .05, .5]) for (const s of [-1, 1]) { bx(c.body, S, .14, 1.4, .14, s * 1.18, 0, z); bx(c.body, S, .48, .07, .1, s * .95, 1.45, z).rotation.z = -s * .45; }
      bx(c.roof, L, .3, .35, .3, 0, 2.6, -.55); py(c.roof, L, .3, 1.7, .3, 0, 2.95, -.55);
      bx(c.body, S, 1.95, 2.05, .45, 0, 0, .95);
      for (const s of [-1, 1]) {
        bx(c.body, S, .68, 1.15, .45, s * .62, 2.05, .95); bx(c.body, S, .74, .08, .5, s * .62, 3.2, .95);
        for (const d of [-1, 1]) bx(c.body, MT.black, .12, .75, .02, s * .62 + d * .15, 2.25, 1.18);
      }
      bx(c.body, S, .6, .35, .3, 0, 2.05, .95);
      mk(G.wheel, c.body, S, .05, .78, .78, 0, 1.5, 1.18).rotation.y = PI / 2;
      mk(G.wheel, c.body, M.rose, .04, .62, .62, 0, 1.5, 1.2).rotation.y = PI / 2;
      mk(G.wheel, c.body, M.rosered, .03, .2, .2, 0, 1.5, 1.22).rotation.y = PI / 2;
      bx(c.body, MT.dstone, 1.95, .12, .03, 0, 1.0, 1.18);
      for (const x of [-.62, 0, .62]) { const w = x ? .28 : .34; bx(c.body, MT.black, w, .62, .03, x, 0, 1.18); py(c.body, MT.black, w, .25, .03, x, .62, 1.18); }
      bx(c.body, c.cm, .3, .5, .02, -.62, 1.3, 1.19);
      lmFlag(c, 1.55, 1.2, 1.8);
    },
    carcassonne(c) {   // Carcassonne: two rings of walls, round towers under slate cones, the Narbonne gate, the count's castle inside
      const S = M.cstone, Sl = M.slate;
      bx(c.body, S, 3.3, .75, .2, 0, 0, -1.65); for (const s of [-1, 1]) { bx(c.body, S, .2, .75, 3.3, s * 1.65, 0, 0); bx(c.body, S, 1.2, .75, .2, s * 1.05, 0, 1.65); }
      for (const [x, z] of [[-1.65, -1.65], [1.65, -1.65], [-1.65, 1.65], [1.65, 1.65], [-1.65, 0], [1.65, 0], [0, -1.65]]) { cy(c.body, S, .2, 1.0, x, 0, z); cn(c.roof, Sl, .23, .45, x, 1.0, z); }
      for (const s of [-1, 1]) { cy(c.body, S, .22, 1.15, s * .45, 0, 1.65); cn(c.roof, Sl, .26, .5, s * .45, 1.15, 1.65); }
      bx(c.body, S, 2.0, 1.25, .22, 0, 0, -1.0); lmCren(c, S, 2.0, .22, 1.25, 0, -1.0, .1);
      for (const s of [-1, 1]) { bx(c.body, S, .22, 1.25, 2.0, s * 1.0, 0, 0); bx(c.body, S, .6, 1.25, .22, s * .7, 0, 1.0); lmCren(c, S, .6, .22, 1.25, s * .7, 1.0, .1); }
      for (const [x, z] of [[-1, -1], [1, -1], [-1, 1], [1, 1], [-1, 0], [1, 0], [0, -1]]) { cy(c.body, S, .24, 1.75, x, 0, z); cn(c.roof, Sl, .29, .7, x, 1.75, z); }
      for (const s of [-1, 1]) { cy(c.body, S, .27, 1.95, s * .35, 0, 1.05); cn(c.roof, Sl, .31, .8, s * .35, 1.95, 1.05); }
      bx(c.body, S, .5, 1.5, .4, 0, 0, 1.0); bx(c.body, MT.black, .26, .6, .03, 0, 0, 1.21); bx(c.body, c.cm, .3, .35, .02, 0, .85, 1.21);
      bx(c.body, S, .9, 1.6, .75, 0, 0, -.35); lmGable(c, Sl, .8, .5, .95, 0, 1.6, -.35, PI / 2);
      bx(c.body, S, .4, 2.3, .4, -.3, 0, -.55); py(c.roof, Sl, .5, .6, .5, -.3, 2.3, -.55);
      for (const x of [-.6, .6]) { bx(c.body, MT.plaster, .45, .45, .4, x, 0, .45); lmGable(c, MT.tile, .5, .3, .5, x, .45, .45); }
      lmFlag(c, -.3, -.55, 3.4);
    },
    versay(c) {   // Versailles: a long palace with forward wings and slate roofs, before it the formal garden with parterres and a gilded fountain
      const C = M.cream, Sl = M.slate;
      bx(c.body, LMM.sand, 3.6, .03, 2.2, 0, 0, .75);
      bx(c.body, C, 3.6, 1.0, .7, 0, 0, -1.45); bx(c.roof, Sl, 3.5, .3, .5, 0, 1.0, -1.45); bx(c.roof, MT.gold, 3.5, .04, .06, 0, 1.3, -1.45);
      bx(c.body, C, 1.0, 1.25, .85, 0, 0, -1.35); lmCols(c, 6, -.4, .4, -.88, 1.0, C, .045, .1);
      lmGable(c, C, 1.05, .3, .15, 0, 1.25, -.95); bx(c.roof, Sl, .95, .35, .7, 0, 1.25, -1.4); bx(c.body, MT.gold, .3, .2, .02, 0, .9, -.92);
      for (const s of [-1, 1]) {
        bx(c.body, C, .7, .95, 1.0, s * 1.45, 0, -.65); bx(c.roof, Sl, .6, .3, .9, s * 1.45, .95, -.65);
        for (const x of [.7, .95]) bx(c.body, MT.glass, .13, .45, .03, s * x, .35, -1.09);
        for (const d of [-1, 1]) bx(c.body, MT.glass, .13, .45, .03, s * 1.45 + d * .18, .3, -.14);
      }
      for (const [x, z] of [[-.8, .25], [.8, .25], [-.8, 1.25], [.8, 1.25]]) {
        bx(c.body, MT.dgreen, 1.1, .08, .7, x, 0, z); bx(c.body, MT.green, .7, .1, .3, x, 0, z);
        cn(c.body, LMM.pine, .09, .38, x + Math.sign(x) * .5, .08, z - .3); cn(c.body, LMM.pine, .09, .38, x + Math.sign(x) * .5, .08, z + .3);
      }
      cy(c.body, MT.stone, .38, .12, 0, 0, .75); cy(c.body, LMM.water, .32, .03, 0, .12, .75); cy(c.body, LMM.goldm, .07, .35, 0, .12, .75); sp(c.body, LMM.goldm, .1, 0, .55, .75);
      bx(c.body, LMM.water, .45, .03, .35, 0, 0, 1.7);
      lmFlag(c, 0, -1.55, 2.3);
    },
    invalides(c) {   // Les Invalides: the gilded dome on its columned drum behind the long front of the soldiers' hospital, cannons on the esplanade
      const C = mat(0xe2d6bc, .85), Sl = M.slate, Gd = LMM.goldm;
      bx(c.body, C, 1.6, 1.1, 1.5, 0, 0, -1.05); lmCols(c, 6, -.55, .55, -.25, 1.0, C, .05);
      bx(c.body, C, 1.3, .12, .2, 0, 1.0, -.25); lmGable(c, C, 1.3, .3, .2, 0, 1.1, -.25);
      cy(c.body, C, .62, .75, 0, 1.1, -1.05);
      for (let i = 0; i < 10; i++) { const a = i / 10 * PI * 2; cy(c.body, C, .035, .65, Math.sin(a) * .66, 1.12, -1.05 + Math.cos(a) * .66); }
      cy(c.body, C, .58, .14, 0, 1.85, -1.05); lmDome(c, Gd, .6, 0, 1.99, -1.05, 1.2);
      cy(c.roof, Gd, .11, .3, 0, 2.65, -1.05); cn(c.roof, Gd, .1, .65, 0, 2.95, -1.05); sp(c.roof, MT.gold, .04, 0, 3.62, -1.05);
      bx(c.body, C, 3.6, .8, .45, 0, 0, .35); bx(c.roof, Sl, 3.6, .3, .4, 0, .8, .35);
      for (let i = 0; i < 8; i++) { const x = -1.6 + i * .457; if (Math.abs(x) < .45) continue; bx(c.body, MT.glass, .12, .3, .03, x, .3, .58); bx(c.roof, C, .12, .15, .06, x, .85, .56); }
      bx(c.body, C, .8, 1.15, .55, 0, 0, .38); bx(c.body, MT.black, .3, .55, .03, 0, 0, .66); bx(c.body, MT.gold, .5, .1, .02, 0, .7, .66); lmGable(c, C, .85, .25, .55, 0, 1.15, .38);
      bx(c.body, c.cm, .3, .25, .02, 0, .82, .67);
      for (const s of [-1, 1]) { bx(c.body, C, .45, .95, .55, s * 1.55, 0, .38); py(c.roof, Sl, .5, .35, .6, s * 1.55, .95, .38); }
      bx(c.body, MT.green, 3.4, .03, .7, 0, 0, 1.3);
      for (const x of [-1.2, -.6, .6, 1.2]) { cy(c.body, MT.bronze, .07, .55, x, .17, 1.05).rotation.x = PI / 2; for (const s of [-1, 1]) mk(G.wheel, c.body, MT.dwood, .05, .28, .28, x + s * .12, .14, 1.15); }
      lmFlag(c, 1.55, -1.5, 2.2);
    },

    // ================= Hintliler =================
    basamaklikuyu(c) {   // a stepwell (Chand Baori): square rings of steps down to the water, an arcaded gallery with kiosks behind
      const S = M.sandst, D = LMM.sandD;
      bx(c.body, S, 3.6, .9, .3, 0, 0, 1.65); for (const s of [-1, 1]) bx(c.body, S, .3, .9, 3.6, s * 1.65, 0, 0);
      bx(c.body, S, 3.0, 2.0, .4, 0, 0, -1.6);
      for (let i = 0; i < 5; i++) {
        const o = 1.5 - i * .25, n = o - .25, y = .75 - i * .15, m = i & 1 ? D : S, mid = (o + n) / 2;
        bx(c.body, m, 2 * o, y, .25, 0, 0, mid); bx(c.body, m, 2 * o, y, .25, 0, 0, -mid);
        bx(c.body, m, .25, y, 2 * n, mid, 0, 0); bx(c.body, m, .25, y, 2 * n, -mid, 0, 0);
      }
      bx(c.body, LMM.water, .5, .06, .5, 0, 0, 0);
      for (let r = 0; r < 2; r++) for (let k = 0; k < 4; k++) bx(c.body, MT.black, .3, .42, .03, -1.05 + k * .7, .85 + r * .6, -1.39);
      bx(c.body, S, .8, .4, .4, 0, 2.0, -1.6); lmDome(c, S, .25, 0, 2.4, -1.6, 1.1);
      for (const s of [-1, 1]) chhatri(c, s * 1.0, 2.0, -1.6, .45, S);
      for (const s of [-1, 1]) chhatri(c, s * 1.6, .9, 1.6, .35, S);
      lmFlag(c, 1.65, -1.0, 2.0);
    },
    filahiri(c) {   // the Hampi elephant stables: a long row of chambers under alternating domes, war elephants in caparisons
      const S = M.granite;
      bx(c.body, S, 3.6, 1.0, .9, 0, 0, -1.3); bx(c.body, S, 3.7, .08, .95, 0, 1.0, -1.3);
      for (let i = 0; i < 7; i++) {
        const x = -1.5 + i * .5;
        bx(c.body, MT.black, .26, .55, .03, x, 0, -.84); py(c.body, MT.black, .26, .16, .03, x, .55, -.84);
        if (i === 3) { bx(c.body, S, .6, .55, .7, 0, 1.08, -1.3); lmDome(c, S, .26, 0, 1.63, -1.3, 1.2); sp(c.roof, MT.gold, .04, 0, 1.97, -1.3); }
        else if (i & 1) py(c.roof, S, .38, .4, .38, x, 1.08, -1.3);
        else { cy(c.body, S, .17, .1, x, 1.08, -1.3); lmDome(c, S, .2, x, 1.18, -1.3, 1.15); }
      }
      const fil = (x, z, ry, howdah) => {
        const g = grp(c, x, z, ry), E = M.elef;
        for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(g, E, .085, .5, sx * .15, 0, sz * .24);
        mk(G.sph, g, E, .52, .5, .9, 0, .72, 0); mk(G.sph, g, E, .36, .38, .34, 0, .86, .5);
        for (const s of [-1, 1]) bx(g, E, .04, .32, .26, s * .2, .7, .45);
        cy(g, E, .05, .55, 0, .2, .66);
        for (const s of [-1, 1]) cn(g, XM.bone, .025, .28, s * .09, .7, .6).rotation.x = 1.2;
        bx(g, c.cm, .5, .05, .5, 0, .95, 0); for (const s of [-1, 1]) { bx(g, c.cm, .03, .3, .48, s * .27, .66, 0); bx(g, MT.gold, .035, .04, .5, s * .27, .64, 0); }
        if (howdah) { bx(g, LMM.goldm, .36, .22, .4, 0, 1.0, -.02); for (const a of [-1, 1]) for (const b of [-1, 1]) cy(g, MT.gold, .015, .23, a * .15, 1.22, -.02 + b * .17); py(g, c.cm, .44, .25, .48, 0, 1.45, -.02); }
      };
      fil(-.85, .55, .35, true); fil(.95, .85, -.5, false);
      cy(c.body, MT.hay, .28, .2, -1.5, 0, 1.45); cn(c.roof, MT.hay, .28, .25, -1.5, .2, 1.45);
      bx(c.body, MT.stone, .9, .22, .3, .2, 0, 1.65); bx(c.body, LMM.water, .8, .03, .2, .2, .2, 1.65);
      lmFlag(c, 1.75, -.6, 2.2);
    },
    sanchi(c) {   // the Great Stupa of Sanchi: a hemispherical dome with harmika and parasols, a ring railing, four carved toranas, an Ashoka pillar
      const S = M.sandst, z0 = -.2, R = 1.62;
      cy(c.body, S, 1.3, .32, 0, 0, z0); lmDome(c, S, 1.12, 0, .32, z0, .62);
      bx(c.body, S, .42, .2, .42, 0, .96, z0); bx(c.body, S, .5, .05, .5, 0, 1.16, z0); cy(c.body, S, .025, .75, 0, 1.2, z0);
      for (const [r, y] of [[.25, 1.4], [.19, 1.6], [.13, 1.8]]) cy(c.body, S, r, .04, 0, y, z0);
      const rail = grp(c, 0, z0);
      for (let i = 0; i < 16; i++) {
        const a = i / 16 * PI * 2;
        if (i % 4) bx(rail, S, .08, .5, .08, Math.sin(a) * R, 0, Math.cos(a) * R);
        if (i % 4 === 0 || i % 4 === 3) continue;
        const b = (i + .5) / 16 * PI * 2;
        for (const y of [.2, .42]) bx(rail, S, .64, .07, .07, Math.sin(b) * R * .98, y, Math.cos(b) * R * .98).rotation.y = b;
      }
      const torana = (x, z, ry) => {
        const g = grp(c, x, z, ry);
        for (const s of [-1, 1]) { bx(g, S, .1, 1.15, .1, s * .3, 0, 0); bx(g, S, .16, .14, .14, s * .3, 1.15, 0); }
        for (const [y, w] of [[.85, .95], [1.06, .95], [1.27, .9]]) bx(g, S, w, .07, .08, 0, y, 0);
        for (const s of [-1, 1]) sp(g, S, .05, s * .48, .885, 0);
        mk(G.wheel, g, S, .03, .2, .2, 0, 1.45, 0).rotation.y = PI / 2;
      };
      torana(0, z0 + R + .12, 0); torana(0, z0 - R - .02, PI); torana(R + .08, z0, PI / 2); torana(-R - .08, z0, -PI / 2);
      cy(c.body, S, .06, 1.6, -.95, 0, 1.55); cy(c.body, S, .09, .12, -.95, 1.6, 1.55); sp(c.body, MT.gold, .1, -.95, 1.82, 1.55);
      lmFlag(c, 1.45, 1.3, 1.8);
    },
    amberkalesi(c) {   // Amber Fort: ochre ramparts and bastions climbing a terraced hill above the lake, the painted gate, kiosks, a cannon
      const Y = M.ochre, W = LMM.white;
      const t = lmSteps(c, M.rock, 3.6, 3.3, 3, .3, 0, -.25, .4);
      bx(c.body, LMM.water, 3.6, .03, .45, 0, 0, 1.68); bx(c.body, MT.green, .5, .06, .3, -.9, 0, 1.68);
      bx(c.body, Y, 3.0, .45, .16, 0, .3, 1.3); lmCren(c, Y, 3.0, .16, .75, 0, 1.3, .1);
      for (const s of [-1, 1]) { cy(c.body, Y, .22, 1.0, s * 1.55, 0, 1.25); lmDome(c, Y, .2, s * 1.55, 1.0, 1.25, .8); }
      bx(c.body, Y, 2.2, .9, 1.2, 0, t, -.75); bx(c.body, Y, 1.4, .45, .8, 0, t + .9, -.9);
      for (let i = 0; i < 5; i++) bx(c.body, MT.black, .16, .28, .03, -.9 + i * .45, t + .35, -.14);
      bx(c.body, Y, .8, 1.25, .3, 0, t, -.05); bx(c.body, M.paint, .6, .8, .02, 0, t + .05, .11); bx(c.body, MT.black, .26, .5, .03, 0, t, .12);
      chhatri(c, 0, t + 1.25, -.05, .4, W);
      for (const s of [-1, 1]) chhatri(c, s * .85, t + .9, -.3, .35, Y, W);
      lmTower(c, -1.4, -1.5, .5, 2.4, Y);
      cy(c.body, MT.iron, .08, .6, .9, t + .12, .35).rotation.x = PI / 2; for (const s of [-1, 1]) mk(G.wheel, c.body, MT.dwood, .05, .3, .3, .9 + s * .12, t + .15, .45);
      bx(c.body, MT.green, .6, .04, .5, -.8, t, .5); cy(c.body, LMM.water, .1, .06, -.8, t, .5);
      lmFlag(c, -1.4, -1.5, 3.3);
    },
    baharatpazari(c) {   // the spice bazaar: a pink arcaded bazaar row, stalls under bright awnings heaped with cones of spice, open sacks
      const P = M.pink;
      bx(c.body, MT.stone, 3.6, .03, 2.6, 0, 0, .5);
      bx(c.body, P, 3.4, 1.0, .65, 0, 0, -1.45); bx(c.body, P, 3.5, .1, .75, 0, 1.0, -1.45);
      for (let i = 0; i < 6; i++) {
        const x = -1.4 + i * .56;
        bx(c.body, MT.black, .3, .5, .03, x, 0, -1.11); py(c.body, MT.black, .3, .15, .03, x, .5, -1.11);
        bx(c.roof, i & 1 ? MT.white : c.cm, .44, .03, .3, x, .66, -.98).rotation.x = .3;
      }
      bx(c.body, P, 2.4, .5, .5, 0, 1.1, -1.5); for (const x of [-.8, 0, .8]) lmDome(c, LMM.white, .14, x, 1.6, -1.5, 1.2);
      const tezgah = (x, z, k) => {
        bx(c.body, MT.wood, .8, .32, .42, x, 0, z);
        for (const s of [-1, 1]) cy(c.body, MT.dwood, .025, .95, x + s * .38, 0, z - .18);
        bx(c.roof, k & 1 ? M.tent : c.cm, .9, .03, .62, x, .95, z + .05).rotation.x = .22;
        for (let j = 0; j < 3; j++) cn(c.body, SPICE[(k * 3 + j) % 6], .1, .17, x - .25 + j * .25, .32, z + .02);
      };
      tezgah(-1.05, .05, 0); tezgah(1.05, .05, 1); tezgah(-1.05, 1.05, 2); tezgah(1.05, 1.05, 3);
      for (const [x, k] of [[-1.4, 0], [-1.1, 1], [1.1, 4], [1.4, 3]]) { cy(c.body, MT.canvas, .1, .22, x, 0, 1.62); cy(c.body, SPICE[k], .085, .03, x, .22, 1.62); }
      bx(c.body, LMM.sail1, .7, .02, .7, 0, 0, .55);
      cn(c.body, SPICE[0], .18, .25, -.15, .02, .45); cn(c.body, SPICE[1], .16, .22, .17, .02, .5); cn(c.body, SPICE[2], .14, .2, 0, .02, .78);
      lmFlag(c, 1.75, -.85, 2.2);
    },
    racputkisla(c) {   // the Rajput barracks: a Vijay Stambha victory tower, a crenellated red hall, a training yard with racks, dummies and war drums
      const R = M.redsand, Y = M.stambha, tx = -1.15, tz = -1.0;
      bx(c.body, Y, 1.0, .25, 1.0, tx, 0, tz);
      for (let i = 0; i < 6; i++) {
        const y = .25 + i * .55, w = .62 - i * .025;
        bx(c.body, Y, w, .5, w, tx, y, tz); bx(c.body, Y, w + .16, .05, w + .16, tx, y + .5, tz);
        if (!(i & 1)) bx(c.body, MT.black, .12, .22, .03, tx, y + .12, tz + w / 2 + .01);
      }
      lmDome(c, Y, .3, tx, 3.55, tz, 1.0); cy(c.roof, MT.gold, .015, .3, tx, 3.82, tz); sp(c.roof, MT.gold, .05, tx, 4.15, tz);
      bx(c.body, R, 2.0, .9, .95, .75, 0, -1.25); bx(c.body, R, 2.06, .12, 1.0, .75, .9, -1.25);
      for (let i = 0; i < 4; i++) bx(c.body, MT.black, .26, .5, .03, .05 + i * .46, 0, -.76);
      chhatri(c, .75, 1.02, -1.25, .45, R, LMM.white);
      bx(c.body, LMM.sand, 3.2, .02, 1.9, .1, 0, .55);
      for (const x of [-1.55, -.65]) cy(c.body, MT.dwood, .03, .75, x, 0, .2); bx(c.body, MT.dwood, .95, .05, .05, -1.1, .7, .2);
      for (let i = 0; i < 4; i++) { const x = -1.45 + i * .23; cy(c.body, MT.dwood, .015, 1.0, x, 0, .16); cn(c.body, MT.steel, .03, .12, x, 1.0, .16); }
      for (const x of [-1.3, -.9]) mk(G.wheel, c.body, c.cm, .04, .3, .3, x, .42, .25).rotation.y = PI / 2;
      for (const [x, z] of [[.4, .3], [1.0, .5]]) { cy(c.body, MT.dwood, .03, .8, x, 0, z); bx(c.body, MT.dwood, .5, .05, .05, x, .6, z); bx(c.body, MT.canvas, .18, .3, .12, x, .3, z); sp(c.body, MT.hay, .1, x, .9, z); }
      for (const z of [.2, .65]) { cy(c.body, MT.bronze, .18, .3, 1.5, 0, z); cy(c.body, MT.leather, .185, .02, 1.5, .3, z); }
      for (const s of [-1, 1]) { bx(c.body, R, 1.25, .65, .2, s * 1.15, 0, 1.65); bx(c.body, R, 1.25, .1, .26, s * 1.15, .65, 1.65); bx(c.body, c.cm, .25, .35, .02, s * .35, .55, 1.81); }
      lmArch(c, R, 0, 1.65, 1.0, 1.05, .3);
      lmFlag(c, 1.5, -.6, 2.2);
    },
    tacmahal(c) {   // the Taj Mahal: an octagonal white mausoleum under an onion dome on a plinth, four minarets, red mosques, the long pool and cypresses
      const W = M.taj, Sh = M.shade, z0 = -.6;
      bx(c.body, W, 2.5, .32, 2.5, 0, 0, z0);
      for (const s of [-1, 1]) bx(c.body, MT.green, 1.35, .04, 1.2, s * 1.0, 0, 1.27);
      bx(c.body, LMM.redb, .7, .03, 1.2, 0, 0, 1.27); bx(c.body, LMM.water, .36, .06, 1.15, 0, 0, 1.27);
      for (const z of [.9, 1.3, 1.7]) for (const s of [-1, 1]) cn(c.body, LMM.pine, .08, .5, s * .45, .03, z);
      bx(c.body, W, 1.3, 1.2, .54, 0, .32, z0); bx(c.body, W, .54, 1.2, 1.3, 0, .32, z0);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(c.body, W, .45, 1.2, .45, sx * .3, .32, z0 + sz * .3).rotation.y = PI / 4;
      bx(c.body, W, .5, 1.05, .04, 0, .37, z0 + .66); bx(c.body, Sh, .36, .75, .03, 0, .37, z0 + .68);
      for (const s of [-1, 1]) bx(c.body, Sh, .03, .75, .36, s * .67, .37, z0);
      cy(c.body, W, .42, .38, 0, 1.52, z0); mk(G.sph, c.roof, W, 1.1, 1.2, 1.1, 0, 2.3, z0); cn(c.roof, W, .22, .4, 0, 2.8, z0);
      cy(c.roof, MT.gold, .02, .3, 0, 3.15, z0); sp(c.roof, MT.gold, .04, 0, 3.5, z0);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) { cy(c.body, W, .12, .22, sx * .45, 1.52, z0 + sz * .45); lmDome(c, W, .14, sx * .45, 1.74, z0 + sz * .45, 1.2); }
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) lmMinaret(c, sx * 1.1, z0 + sz * 1.1, 2.5, W, W);
      for (const s of [-1, 1]) { bx(c.body, M.redsand, .5, .7, 1.1, s * 1.62, 0, z0); for (let k = -1; k <= 1; k++) lmDome(c, W, .15, s * 1.62, .7, z0 + k * .35); }
      lmFlag(c, 1.75, 1.2, 1.6);
    },
    kizilkale(c) {   // the Red Fort: red sandstone walls and bastions behind a moat, the Lahori Gate with its kiosk screen, a white marble hall inside
      const R = M.redsand, W = LMM.white;
      bx(c.body, LMM.water, 3.6, .03, .3, 0, 0, 1.72); bx(c.body, R, .5, .1, .45, 0, 0, 1.6);
      for (const s of [-1, 1]) { bx(c.body, R, 1.15, 1.15, .45, s * 1.15, 0, 1.0); lmCren(c, R, 1.15, .45, 1.15, s * 1.15, 1.0, .12); }
      for (const s of [-1, 1]) bx(c.body, R, .4, 1.05, 2.6, s * 1.62, 0, -.4);
      bx(c.body, R, 2.84, .9, .3, 0, 0, -1.6);
      for (const s of [-1, 1]) {
        cy(c.body, R, .32, 1.35, s * 1.55, 0, 1.0); cy(c.body, W, .16, .25, s * 1.55, 1.35, 1.0); lmDome(c, W, .18, s * 1.55, 1.6, 1.0, 1.1);
        cy(c.body, R, .28, 1.2, s * 1.55, 0, -1.55); lmDome(c, R, .2, s * 1.55, 1.2, -1.55);
      }
      bx(c.body, R, 1.15, 1.8, .7, 0, 0, 1.0); bx(c.body, W, 1.16, .06, .71, 0, 1.6, 1.0);
      bx(c.body, W, .5, 1.05, .03, 0, 0, 1.36); bx(c.body, MT.black, .34, .8, .04, 0, 0, 1.37); py(c.body, MT.black, .34, .2, .04, 0, .8, 1.37);
      for (const s of [-1, 1]) { cy(c.body, R, .2, 2.05, s * .6, 0, 1.3); lmDome(c, W, .17, s * .6, 2.05, 1.3, 1.2); sp(c.roof, MT.gold, .03, s * .6, 2.27, 1.3); }
      bx(c.body, W, .85, .22, .3, 0, 1.8, 1.05); for (let i = 0; i < 5; i++) lmDome(c, W, .08, -.32 + i * .16, 2.02, 1.05, 1.2);
      lmSteps(c, W, 1.8, 1.0, 1, .15, 0, -.75); bx(c.body, W, 1.5, .7, .75, 0, .15, -.8); lmCols(c, 6, -.65, .65, -.4, .65, W, .045, .15);
      bx(c.roof, W, 1.6, .08, .85, 0, .85, -.75); for (const sx of [-1, 1]) for (const sz of [-1, 1]) lmDome(c, LMM.goldm, .11, sx * .7, .93, -.75 + sz * .35, 1.2);
      lmFlag(c, 0, .95, 3.0);
    },
  };
}
