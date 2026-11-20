// Age-up building models (landmarks.js looks) of the Arabs, the Aztecs and the Byzantines. See index.js.
export default function (K) {
  const { THREE, PI, G, MT, XM, LMM, mat, mk, bx, cy, cn, py, sp, lmFlag, lmDome, lmGable, lmMinaret, lmCols, lmCren, lmTower, lmWall, lmPagoda, lmSteps, lmArch, lmShip } = K;
  const M = {
    // Arabs
    adobe: mat(0xc9a06a, .9), adobeD: mat(0xa87a48, .92), sandW: mat(0xe2cfa0, .9), green: mat(0x2f7a5a, .5, .2), turq: mat(0x2a9a9a, .5, .15),
    red: mat(0xb4603e, .9), stucco: mat(0xf0e2c4, .85), ablW: mat(0xe8dcc0, .85), ablR: mat(0x9a4a32, .85), rug1: mat(0x8a1f2a, .9), rug2: mat(0x2a3f7a, .9),
    camel: mat(0xc49a5e, .95), horse: mat(0x6b4a30, .9), horse2: mat(0xd8d0c0, .9), lion: mat(0xd9cfb8, .85), gtile: mat(0x3f7a5a, .6),
    // Aztecs
    lime: mat(0xd8cdb0, .95), lime2: mat(0xbfb193, .95), volc: mat(0x8a7560, .95), volcD: mat(0x6e5e4c, .95), basalt: mat(0x5c5650, .9),
    aRed: mat(0xa83224, .85), aBlue: mat(0x3a7ab8, .7), jade: mat(0x3f8f6a, .6), maize: mat(0xe8c33a, .9), cacao: mat(0x5a3220, .9), reed: mat(0xa8955a, 1),
    jag: mat(0xd09a3a, .9), feather: mat(0x2a9a7a, .7), flower: mat(0xe8901a, .9), eagle: mat(0x6a4a2a, .9), clay: mat(0xb0653a, .9),
    // Byzantines
    bzW: mat(0xd8c8a6, .9), bzB: mat(0xa65a3e, .88), bzP: mat(0xd6a487, .9), bzPd: mat(0xbb8a68, .9), granite: mat(0xb07a6a, .7),
    medusa: mat(0x7a8a78, .8), shield: mat(0x8e2a2a, .85), cloak: mat(0x9a2a2a, .85),
  };
  // a sub-group (its parts are placed in its own frame)
  const grp = (c, x, z, ry = 0, y = 0, p = c.body) => { const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; p.add(g); return g; };
  // a gable roof whose ridge runs along x (w: x extent, d: z extent)
  const gableX = (c, m, w, h, d, x, y, z) => mk(G.prism, grp(c, x, z, PI / 2, y, c.roof), m, d, h, w, 0, 0, 0);
  // the front stair of a stepped pyramid built with lmSteps(w, d, n, h, x, z0, k): one block of two steps per tier
  const stairs = (c, m, sw, z0, d, n, h, k, x = 0) => {
    for (let i = 0; i < n; i++) {
      const zf = z0 + (d - i * k) / 2, D = k / 2 + .06;
      bx(c.body, m, sw, h / 2, D, x, i * h, zf + .06 - D / 2); bx(c.body, m, sw, h / 2, D / 2, x, i * h + h / 2, zf + .06 - D * .75);
    }
  };
  const deve = (c, x, z, ry) => {   // a camel facing +z
    const g = grp(c, x, z, ry), C = M.camel;
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, C, .06, .5, .06, sx * .07, 0, sz * .2);
    bx(g, C, .22, .22, .6, 0, .48, 0); sp(g, C, .14, 0, .72, -.02); bx(g, M.rug1, .24, .05, .22, 0, .66, .2);
    bx(g, C, .09, .42, .1, 0, .58, .28).rotation.x = .55; bx(g, C, .1, .1, .22, 0, .9, .5);
    return g;
  };
  const at = (c, x, z, ry, m = M.horse, rider) => {   // a horse facing +z, a rider in the player's colour if asked
    const g = grp(c, x, z, ry);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, m, .06, .45, .06, sx * .07, 0, sz * .2);
    bx(g, m, .2, .22, .55, 0, .42, 0); bx(g, m, .09, .35, .1, 0, .55, .22).rotation.x = .5; bx(g, m, .09, .1, .24, 0, .82, .45);
    bx(g, m, .04, .25, .04, 0, .4, -.28).rotation.x = -.3;
    if (rider) { bx(g, c.cm, .16, .3, .14, 0, .64, -.02); sp(g, MT.skin, .06, 0, 1.0, -.02); cn(g, MT.steel, .065, .12, 0, 1.03, -.02); cy(g, MT.dwood, .015, 1.1, .12, .55, .05).rotation.x = 1.0; }
    return g;
  };
  const aguila = (c, x, y, z, s, m = M.eagle) => {   // an eagle with spread wings
    const g = grp(c, x, z, 0, y);
    sp(g, m, .14 * s, 0, .14 * s, 0); sp(g, LMM.white, .08 * s, 0, .3 * s, .07 * s); cn(g, MT.gold, .03 * s, .1 * s, 0, .29 * s, .13 * s).rotation.x = PI / 2;
    for (const sd of [-1, 1]) bx(g, m, .4 * s, .04 * s, .16 * s, sd * .22 * s, .16 * s, -.02 * s).rotation.z = sd * .45;
    bx(g, m, .1 * s, .04 * s, .16 * s, 0, .05 * s, -.16 * s);
  };
  const jaguar = (c, x, y, z, ry) => {
    const g = grp(c, x, z, ry, y), J = M.jag;
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, J, .06, .18, .06, sx * .07, 0, sz * .18);
    bx(g, J, .2, .18, .5, 0, .18, 0); bx(g, J, .18, .16, .18, 0, .28, .3); for (const sx of [-1, 1]) bx(g, J, .04, .05, .03, sx * .06, .44, .3);
    bx(g, J, .04, .04, .35, 0, .3, -.4); for (let i = 0; i < 4; i++) sp(g, LMM.black, .035, i & 1 ? .1 : -.1, .28, -.15 + i * .1);
  };
  const dromon = (c, x, z, ry, L = 1.8, ates = false) => {   // a Byzantine war galley, the bow at +z
    const g = grp(c, x, z, ry);
    bx(g, MT.dwood, .42, .22, L, 0, .02, 0); bx(g, MT.wood, .36, .05, L * .95, 0, .24, 0); bx(g, MT.bronze, .1, .08, .3, 0, .05, L / 2 + .1);
    bx(g, MT.dwood, .1, .45, .12, 0, .2, -L / 2).rotation.x = -.5; cy(g, MT.wood, .025, 1.2, 0, .25, .1); bx(g, MT.dwood, .03, .03, 1.0, 0, 1.3, .1).rotation.x = .35;
    bx(g, c.cm, .02, .6, .6, 0, .65, .1); for (let i = 0; i < 5; i++) for (const s of [-1, 1]) bx(g, MT.dwood, .4, .02, .03, s * .35, .12, -L * .35 + i * L * .17).rotation.z = s * .35;
    if (ates) { cy(g, MT.bronze, .04, .4, 0, .32, L / 2 - .25).rotation.x = PI / 2; sp(g, MT.bronze, .06, 0, .34, L / 2 + .15); cn(g, MT.glow, .12, .6, 0, .34, L / 2 + .2).rotation.x = PI / 2; }
    return g;
  };
  const muhafiz = (c, x, z) => {   // a Varangian guard with his axe
    bx(c.body, M.cloak, .16, .42, .12, x, 0, z); sp(c.body, MT.skin, .07, x, .5, z); cn(c.body, MT.steel, .075, .12, x, .54, z);
    cy(c.body, MT.dwood, .015, .7, x + .12, 0, z); bx(c.body, MT.steel, .03, .15, .12, x + .12, .55, z + .06);
  };

  return {
    // ---------------- Araplar ----------------
    bagdatcarsi(c) {   // the covered bazaar: a vaulted street under turquoise domes, shop rows with awnings, a tiled gate
      bx(c.body, LMM.sandD, 3.7, .05, 3.5, 0, 0, 0);
      bx(c.body, M.adobe, 1.0, 1.15, 3.1, 0, .05, -.15); bx(c.body, M.adobeD, 1.04, .08, 3.14, 0, 1.15, -.15);
      for (const z of [-1.25, 1.0]) { cy(c.body, M.adobe, .3, .12, 0, 1.23, z); lmDome(c, M.turq, .33, 0, 1.35, z); sp(c.roof, MT.gold, .03, 0, 1.71, z); }
      cy(c.body, M.adobe, .5, .3, 0, 1.23, -.1); lmDome(c, M.turq, .55, 0, 1.53, -.1, 1.05); cy(c.roof, MT.gold, .02, .3, 0, 2.1, -.1); sp(c.roof, MT.gold, .05, 0, 2.42, -.1);
      bx(c.body, M.sandW, 1.3, 1.75, .3, 0, 0, 1.5); bx(c.body, MT.black, .5, .95, .04, 0, .05, 1.66); py(c.body, MT.black, .5, .3, .04, 0, 1.0, 1.66);
      bx(c.body, M.turq, 1.32, .14, .32, 0, 1.45, 1.5); bx(c.body, c.cm, .7, .08, .05, 0, 1.27, 1.67);
      for (const s of [-1, 1]) {
        bx(c.body, M.adobe, .75, .85, 2.8, s * 1.0, .05, -.2); bx(c.body, M.adobeD, .8, .06, 2.85, s * 1.0, .9, -.2);
        for (let i = 0; i < 4; i++) {
          const z = -1.3 + i * .72;
          bx(c.body, MT.black, .04, .5, .38, s * 1.38, .05, z); bx(c.body, i & 1 ? M.rug1 : M.rug2, .34, .03, .5, s * 1.55, .66, z).rotation.z = -s * .35;
          sp(c.body, i & 1 ? MT.hay : MT.canvas, .11, s * 1.64, .14, z + .12); bx(c.body, i & 1 ? M.rug2 : M.rug1, .25, .08, .26, s * 1.64, .05, z - .14);
        }
      }
      lmFlag(c, 1.75, -1.75, 2.0);
    },
    deveagili(c) {   // the camel yard: a mud-brick enclosure, a palm-thatch shade over the mangers, camels and horses, a palm
      const W = M.adobe;
      bx(c.body, LMM.sand, 3.7, .04, 3.7, 0, 0, 0);
      bx(c.body, W, 3.6, .65, .22, 0, 0, -1.7);
      for (const s of [-1, 1]) { bx(c.body, W, .22, .65, 3.6, s * 1.7, 0, 0); bx(c.body, W, 1.2, .65, .22, s * 1.1, 0, 1.7); bx(c.body, M.adobeD, .4, 1.1, .4, s * .6, 0, 1.7); bx(c.body, c.cm, .42, .1, .42, s * .6, 1.0, 1.7); }
      bx(c.body, MT.dwood, 1.0, .1, .12, 0, .95, 1.7);
      for (const x of [-1.3, -.45, .45, 1.3]) cy(c.body, LMM.bark, .05, 1.15, x, 0, -.95);
      bx(c.roof, MT.thatch, 3.2, .08, 1.3, 0, 1.15, -1.3); bx(c.body, MT.wood, 2.4, .25, .3, 0, 0, -1.45); bx(c.body, MT.hay, 2.3, .08, .25, 0, .25, -1.45);
      bx(c.body, MT.stone, 1.0, .22, .3, .9, 0, .55); bx(c.body, LMM.water, .9, .02, .2, .9, .2, .55);
      deve(c, -1.0, .4, .3); deve(c, -.3, -.3, -.5); deve(c, .25, 1.0, 2.6);
      at(c, 1.1, -.35, -1.3); at(c, .5, .05, 1.8, M.horse2);
      cy(c.body, LMM.bark, .07, 2.0, 1.25, 0, 1.2);
      for (let i = 0; i < 5; i++) bx(c.roof, LMM.pine, .7, .04, .15, 1.25 + Math.cos(i * 1.25) * .25, 2.0, 1.2 + Math.sin(i * 1.25) * .25).rotation.y = -i * 1.25;
      lmFlag(c, -1.45, 1.3, 2.0);
    },
    beytulhikme(c) {   // the House of Wisdom: a tiled iwan portal, a green dome, an observatory tower, an armillary sphere, reading tables
      const B = mat(0xcfae78, .9);
      bx(c.body, LMM.marble, 3.6, .12, 3.2, 0, 0, -.1);
      bx(c.body, B, 3.2, 1.3, 2.0, 0, .12, -.7); bx(c.body, M.adobeD, 3.25, .08, 2.05, 0, 1.42, -.7);
      bx(c.body, B, 1.3, 2.2, .45, 0, .12, .45); bx(c.body, M.turq, 1.32, .14, .47, 0, 2.05, .45); for (const s of [-1, 1]) bx(c.body, M.turq, .08, 1.9, .47, s * .6, .12, .45);
      bx(c.body, MT.black, .6, 1.3, .04, 0, .12, .69); py(c.body, MT.black, .6, .35, .04, 0, 1.42, .69);
      for (const x of [-1.35, -.95, .95, 1.35]) { bx(c.body, MT.black, .18, .4, .04, x, .6, .31); py(c.body, MT.black, .18, .12, .04, x, 1.0, .31); }
      cy(c.body, B, .62, .3, 0, 1.5, -.8); lmDome(c, M.green, .65, 0, 1.8, -.8, 1.1); cy(c.roof, MT.gold, .02, .3, 0, 2.5, -.8); sp(c.roof, MT.gold, .05, 0, 2.85, -.8);
      cy(c.body, B, .35, 2.0, 1.25, 0, -1.25); lmDome(c, LMM.white, .37, 1.25, 2.0, -1.25); bx(c.body, MT.black, .06, .3, .04, 1.25, 1.5, -.89);
      cy(c.body, MT.stone, .14, .55, -1.2, .12, .9);
      const r1 = mk(G.ring, c.body, MT.bronze, .55, .55, .55, -1.2, 1.0, .9); r1.rotation.x = PI / 2;
      const r2 = mk(G.ring, c.body, MT.bronze, .55, .55, .55, -1.2, 1.0, .9); r2.rotation.z = PI / 2;
      const r3 = mk(G.ring, c.body, MT.gold, .48, .48, .48, -1.2, 1.0, .9); r3.rotation.x = .4; sp(c.body, MT.gold, .05, -1.2, 1.0, .9);
      bx(c.body, MT.wood, .7, .35, .4, 1.2, .12, .9);
      for (let i = 0; i < 4; i++) bx(c.body, [M.rug1, M.rug2, M.green, MT.leather][i], .12, .16, .28, .99 + i * .14, .47, .9);
      lmFlag(c, -.6, 1.3, 2.2);
    },
    kahirekalesi(c) {   // Saladin's citadel: crenellated walls, round towers, a gate, the keep, a domed mosque with pencil minarets
      const S = mat(0xc8b088, .92), D = mat(0xa8936c, .92);
      const kule = (x, z, r, h) => {
        cy(c.body, S, r, h, x, 0, z); cy(c.body, D, r * 1.1, .1, x, h, z);
        for (let i = 0; i < 5; i++) { const a = i / 5 * PI * 2; bx(c.body, D, .1, .13, .1, x + Math.cos(a) * r * .95, h + .1, z + Math.sin(a) * r * .95); }
        bx(c.body, MT.black, .06, .22, .04, x, h * .6, z + r);
      };
      bx(c.body, S, 3.0, 1.3, .3, 0, 0, -1.5); lmCren(c, D, 3.0, .3, 1.3, 0, -1.5, .12);
      for (const s of [-1, 1]) {
        bx(c.body, S, .3, 1.3, 3.0, s * 1.5, 0, 0); lmCren(c, D, .3, 3.0, 1.3, s * 1.5, 0, .12);
        bx(c.body, S, 1.1, 1.3, .3, s * .95, 0, 1.5); lmCren(c, D, 1.1, .3, 1.3, s * .95, 1.5, .12);
      }
      for (const [x, z] of [[-1.5, -1.5], [1.5, -1.5], [-1.5, 1.5], [1.5, 1.5]]) kule(x, z, .4, 1.9);
      for (const s of [-1, 1]) kule(s * .45, 1.58, .3, 1.7);
      bx(c.body, S, .6, .45, .3, 0, .9, 1.5); bx(c.body, MT.black, .45, .9, .34, 0, 0, 1.5); bx(c.body, c.cm, .5, .1, .04, 0, 1.05, 1.66);
      bx(c.body, S, .8, 2.2, .8, -.95, 0, -.8); lmCren(c, D, .8, .8, 2.2, -.95, -.8, .12);
      bx(c.body, LMM.marble, 1.3, .9, 1.2, .35, 0, -.5); cy(c.body, LMM.marble, .5, .2, .35, .9, -.5); lmDome(c, LMM.lead, .55, .35, 1.1, -.5, .9);
      for (const s of [-1, 1]) { lmDome(c, LMM.lead, .3, .35 + s * .62, .9, -.5, .8); lmDome(c, LMM.lead, .3, .35, .9, -.5 + s * .58, .8); }
      sp(c.roof, MT.gold, .05, .35, 1.65, -.5);
      lmMinaret(c, -.35, .2, 3.4, LMM.marble); lmMinaret(c, 1.05, .2, 3.4, LMM.marble);
      lmFlag(c, -.95, -.8, 3.0);
    },
    elhamra(c) {   // the red palace: red walls, the Comares tower over the myrtle pool, the Court of the Lions with its fountain
      const R = M.red, St = M.stucco;
      bx(c.body, mat(0xa86a48, .95), 3.8, .15, 3.8, 0, 0, 0);
      bx(c.body, R, 3.7, 1.1, .25, 0, .15, -1.75); lmCren(c, R, 3.7, .25, 1.25, 0, -1.75, .12);
      for (const s of [-1, 1]) { bx(c.body, R, .25, 1.1, 3.4, s * 1.75, .15, -.05); lmCren(c, R, .25, 3.4, 1.25, s * 1.75, -.05, .12); }
      bx(c.body, R, 1.1, 2.6, 1.1, -1.05, .15, -1.25); bx(c.body, M.adobeD, 1.15, .08, 1.15, -1.05, 2.75, -1.25); lmCren(c, R, 1.15, 1.15, 2.83, -1.05, -1.25, .12);
      for (const s of [-1, 1]) bx(c.body, MT.black, .18, .45, .04, -1.05 + s * .25, 1.7, -.69);
      bx(c.body, R, .7, 1.8, .7, 1.4, .15, -1.4); lmCren(c, R, .72, .72, 1.95, 1.4, -1.4, .1);
      bx(c.body, LMM.marble, 1.1, .05, 1.7, -1.05, .15, .15); bx(c.body, LMM.water, .55, .03, 1.5, -1.05, .2, .15);
      for (const s of [-1, 1]) bx(c.body, LMM.pine, .15, .2, 1.5, -1.05 + s * .38, .15, .15);
      lmCols(c, 5, -1.45, -.65, 1.05, .8, St, .04, .15); bx(c.body, St, 1.0, .25, .3, -1.05, .95, 1.05);
      bx(c.body, LMM.marble, 2.0, .05, 1.9, .6, .15, .2);
      for (const s of [-1, 1]) {
        lmCols(c, 7, -.25, 1.45, .2 + s * .85, .63, St, .035, .2); bx(c.body, St, 1.9, .12, .1, .6, .83, .2 + s * .85); bx(c.roof, MT.tile, 2.0, .08, .35, .6, .95, .2 + s * .9);
        lmCols(c, 5, -.5, .9, .6 + s * .95, .75, St, .035, .2, true); bx(c.roof, MT.tile, .35, .08, 1.5, .6 + s * .95, .95, .2); py(c.roof, M.gtile, .55, .45, .7, .6 + s * .95, 1.03, .2);
      }
      cy(c.body, LMM.marble, .25, .12, .6, .2, .2);
      for (let i = 0; i < 8; i++) { const a = i / 8 * PI * 2; bx(c.body, M.lion, .07, .1, .12, .6 + Math.cos(a) * .22, .2, .2 + Math.sin(a) * .22).rotation.y = -a; }
      cy(c.body, LMM.marble, .05, .25, .6, .32, .2); cy(c.body, LMM.marble, .18, .06, .6, .57, .2); cy(c.body, LMM.water, .15, .02, .6, .63, .2);
      bx(c.body, LMM.water, 1.8, .02, .08, .6, .2, .2); bx(c.body, LMM.water, .08, .02, 1.7, .6, .2, .2);
      for (const x of [-.2, 1.5]) { cy(c.body, LMM.bark, .04, .3, x, .15, 1.6); cn(c.body, LMM.pine, .14, 1.2, x, .4, 1.6); }
      lmFlag(c, -1.05, -1.25, 3.4);
    },
    memlukkisla(c) {   // the Mamluk barracks: a striped (ablaq) block, a carved dome and minaret, stables, a yard with riders and lances
      const abl = (w, h, d, x, y, z, n) => { for (let i = 0; i < n; i++) bx(c.body, i & 1 ? M.ablR : M.ablW, w, h / n, d, x, y + i * h / n, z); };
      bx(c.body, LMM.sand, 3.7, .04, 3.7, 0, 0, 0);
      abl(3.5, 1.5, 1.0, 0, 0, -1.3, 6); lmCren(c, M.ablW, 3.5, 1.0, 1.5, 0, -1.3, .12);
      abl(1.0, 2.2, .3, 0, 0, -.7, 8); bx(c.body, MT.black, .45, 1.1, .04, 0, 0, -.54); py(c.body, MT.black, .45, .3, .04, 0, 1.1, -.54); bx(c.body, c.cm, 1.02, .1, .32, 0, 1.95, -.7);
      cy(c.body, M.ablW, .45, .45, -1.2, 1.5, -1.3); lmDome(c, M.ablW, .45, -1.2, 1.95, -1.3, 1.3); sp(c.roof, MT.gold, .05, -1.2, 2.58, -1.3);
      lmMinaret(c, 1.45, -.55, 3.0, M.ablW);
      bx(c.body, M.ablW, .8, 1.0, 1.7, 1.45, 0, .6); bx(c.body, M.ablR, .85, .1, 1.75, 1.45, 1.0, .6);
      for (let i = 0; i < 3; i++) bx(c.body, MT.black, .04, .6, .35, 1.04, 0, .05 + i * .55);
      at(c, -.4, .4, .8, M.horse, true); at(c, .35, .95, -2.2, M.horse2, true);
      cy(c.body, MT.dwood, .03, .45, -1.4, 0, .9); mk(G.wheel, c.body, MT.hay, .08, .5, .5, -1.4, .6, .9); mk(G.wheel, c.body, MT.red, .09, .2, .2, -1.4, .6, .9);
      for (const x of [-1.5, -.9]) bx(c.body, MT.dwood, .06, .9, .06, x, 0, -.68); bx(c.body, MT.dwood, .7, .05, .05, -1.2, .8, -.68);
      for (let i = 0; i < 5; i++) { const x = -1.45 + i * .12; cy(c.body, MT.dwood, .015, 1.5, x, 0, -.62); cn(c.body, MT.steel, .03, .12, x, 1.5, -.62); }
      for (const s of [-1, 1]) bx(c.body, M.ablW, 1.2, .6, .2, s * 1.2, 0, 1.75);
      lmFlag(c, 0, -1.3, 2.6);
    },
    kervanhani(c) {   // the great caravan inn: a high tiled portal, arcaded courtyard, domed corner towers, a kiosk mosque, camels
      const W = mat(0xd4b88a, .9), Wd = mat(0xb39466, .9);
      bx(c.body, LMM.sandD, 3.8, .04, 3.8, 0, 0, 0);
      bx(c.body, W, 3.3, 1.5, .4, 0, 0, -1.45);
      for (const s of [-1, 1]) { bx(c.body, W, .4, 1.5, 2.9, s * 1.45, 0, -.2); bx(c.body, W, 1.0, 1.5, .4, s * .95, 0, 1.05); }
      lmCren(c, Wd, 3.3, 2.9, 1.5, 0, -.2, .12);
      for (let i = 0; i < 6; i++) { const x = -1.05 + i * .42; bx(c.body, MT.black, .26, .55, .04, x, .1, -1.24); bx(c.body, MT.black, .2, .35, .04, x, .85, -1.24); }
      for (const s of [-1, 1]) for (let i = 0; i < 4; i++) bx(c.body, MT.black, .04, .55, .26, s * 1.24, .1, -.9 + i * .5);
      for (const [x, z] of [[-1.5, -1.5], [1.5, -1.5], [-1.5, 1.05], [1.5, 1.05]]) { cy(c.body, W, .32, 1.8, x, 0, z); lmDome(c, Wd, .32, x, 1.8, z); }
      bx(c.body, W, 1.2, 2.4, .5, 0, 0, 1.1); bx(c.body, M.turq, 1.22, .18, .52, 0, 2.15, 1.1); for (const s of [-1, 1]) bx(c.body, M.turq, .1, 2.0, .52, s * .55, 0, 1.1);
      bx(c.body, MT.black, .55, 1.3, .04, 0, 0, 1.36); py(c.body, MT.black, .55, .35, .04, 0, 1.3, 1.36); bx(c.body, c.cm, .9, .1, .04, 0, 1.85, 1.37);
      bx(c.body, LMM.marble, .8, .2, .8, 0, 0, -.25); for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(c.body, LMM.marble, .05, .6, sx * .28, .2, -.25 + sz * .28);
      bx(c.body, W, .75, .12, .75, 0, .8, -.25); lmDome(c, M.turq, .3, 0, .92, -.25);
      deve(c, -.8, .35, .6); deve(c, .8, -.55, -2.3); deve(c, -1.2, 1.65, PI / 2); deve(c, 1.2, 1.65, -PI / 2);
      lmFlag(c, 1.5, 1.05, 2.6);
    },
    samcelik(c) {   // the Damascus steel works: an arched forge hall with a dome, chimneys, a crucible furnace, anvils, a sword rack
      const S = mat(0xb8a07a, .9);
      bx(c.body, MT.soil2, 3.7, .04, 3.7, 0, 0, 0);
      bx(c.body, S, 2.6, 1.4, 1.5, -.4, 0, -.9); bx(c.body, M.adobeD, 2.65, .08, 1.55, -.4, 1.4, -.9);
      cy(c.body, S, .42, .2, -.9, 1.4, -.9); lmDome(c, LMM.lead, .45, -.9, 1.6, -.9); sp(c.roof, MT.gold, .04, -.9, 2.1, -.9);
      for (let i = 0; i < 3; i++) { const x = -1.2 + i * .8; bx(c.body, MT.black, .5, .9, .04, x, 0, -.14); py(c.body, MT.black, .5, .25, .04, x, .9, -.14); bx(c.body, MT.glow, .3, .35, .03, x, .1, -.12); }
      for (const x of [-1.4, .5]) { cy(c.body, MT.brick, .18, 2.6, x, 0, -1.35); cy(c.body, MT.dstone, .21, .1, x, 2.6, -1.35); c.chim.push(x, 2.75, -1.35); }
      cy(c.body, MT.brick, .42, .8, 1.25, 0, -.8); cn(c.body, MT.brick, .42, .6, 1.25, .8, -.8); sp(c.body, MT.glow, .08, 1.25, 1.38, -.8); c.chim.push(1.25, 1.5, -.8);
      bx(c.body, MT.glow, .25, .2, .03, 1.25, .1, -.37); bx(c.body, MT.leather, .3, .2, .45, .65, 0, -.45);
      for (const x of [-.8, .2]) { bx(c.body, MT.iron, .18, .35, .18, x, 0, .5); bx(c.body, MT.iron, .4, .12, .18, x, .35, .5); }
      bx(c.body, MT.dwood, .9, .3, .35, 1.0, 0, .75); bx(c.body, LMM.water, .8, .02, .25, 1.0, .29, .75);
      for (const x of [-1.25, .05]) bx(c.body, MT.dwood, .07, .95, .07, x, 0, 1.35); bx(c.body, MT.dwood, 1.4, .08, .1, -.6, .9, 1.35);
      for (let i = 0; i < 5; i++) { const x = -1.05 + i * .22; bx(c.body, MT.steel, .04, .7, .015, x, .2, 1.41); bx(c.body, MT.gold, .14, .03, .03, x, .86, 1.41); }
      sp(c.body, LMM.black, .3, -1.5, .05, .55); bx(c.body, c.cm, .5, .1, .04, -.4, 1.2, -.14);
      lmFlag(c, 1.6, 1.3, 2.0);
    },

    // ---------------- Aztekler ----------------
    cinampa(c) {   // the floating gardens: plots of black soil in the lake, maize, greens and marigolds, willows at the corners, canoes in the canals
      bx(c.body, LMM.water, 3.9, .04, 3.9, 0, 0, 0);
      const xs = [-1.25, 0, 1.25], zs = [-.85, .85];
      xs.forEach((x, i) => zs.forEach((z, j) => {
        bx(c.body, MT.soil, .95, .14, 1.4, x, 0, z);
        if (i === 1 && j === 0) {
          cy(c.body, M.adobe, .3, .45, x, .14, z); cn(c.roof, MT.thatch, .4, .55, x, .59, z); bx(c.body, MT.black, .14, .25, .03, x, .14, z + .3); c.chim.push(x, 1.2, z);
          return;
        }
        const t = (i + j) % 3;
        for (let k = 0; k < 3; k++) {
          const xx = x - .3 + k * .3;
          if (t === 0) { bx(c.body, MT.green, .1, .4, 1.2, xx, .14, z); bx(c.body, M.maize, .1, .06, 1.2, xx, .54, z); }
          else bx(c.body, t === 1 ? LMM.turf : M.flower, .18, t === 1 ? .12 : .1, 1.2, xx, .14, z);
        }
      }));
      for (const [x, z] of [[-1.65, -1.5], [1.65, -1.5], [-1.65, 1.5], [1.65, 1.5]]) { cy(c.body, LMM.bark, .04, .9, x, .14, z); cn(c.body, LMM.pine, .16, 1.3, x, .7, z); }
      const k1 = grp(c, .625, .9);
      bx(k1, MT.wood, .18, .1, .9, 0, .02, 0); bx(k1, c.cm, .1, .25, .08, 0, .1, .1); sp(k1, MT.skin, .05, 0, .42, .1); cy(k1, MT.dwood, .012, 1.0, .06, .1, -.1).rotation.x = .3;
      const k2 = grp(c, -1.2, 0, PI / 2);
      bx(k2, MT.wood, .18, .1, .9, 0, .02, 0); for (let i = 0; i < 3; i++) sp(k2, M.maize, .08, 0, .16, -.25 + i * .2);
      lmFlag(c, 1.25, .5, 1.8);
    },
    kartalevi(c) {   // the House of the Eagles: a stepped platform and stair, a pillared hall with a painted frieze, eagle statues
      const L = M.lime, R = M.aRed;
      bx(c.body, M.lime2, 3.8, .06, 3.8, 0, 0, 0);
      lmSteps(c, L, 3.4, 2.6, 2, .35, 0, -.4, .3); bx(c.body, R, 3.42, .08, 2.62, 0, .22, -.4);
      for (let i = 0; i < 5; i++) bx(c.body, M.lime2, .9, .14 * (i + 1), .14, 0, 0, 1.55 - i * .13);
      for (const s of [-1, 1]) bx(c.body, R, .12, .75, .7, s * .5, 0, 1.25);
      bx(c.body, L, 2.4, .9, 1.4, 0, .7, -.8); bx(c.body, MT.black, 1.9, .7, .04, 0, .7, -.08);
      for (let i = 0; i < 4; i++) bx(c.body, R, .2, .9, .2, -.9 + i * .6, .7, -.05);
      bx(c.body, R, 2.42, .12, 1.42, 0, 1.3, -.8); bx(c.body, L, 2.5, .12, 1.5, 0, 1.6, -.8);
      for (let i = 0; i < 6; i++) bx(c.body, i & 1 ? R : L, .14, .22, .08, -1.0 + i * .4, 1.72, -.08);
      aguila(c, 0, 1.72, -.8, 1.6);
      for (const s of [-1, 1]) { bx(c.body, L, .3, .3, .3, s * .75, 0, 1.55); aguila(c, s * .75, .3, 1.55, .8); }
      for (const s of [-1, 1]) { cy(c.body, MT.dwood, .025, 1.6, s * 1.4, .7, .4); sp(c.body, M.feather, .12, s * 1.4, 2.35, .4); }
      cy(c.body, M.basalt, .14, .3, 1.2, .7, 0); sp(c.body, MT.glow, .08, 1.2, 1.02, 0); c.chim.push(1.2, 1.1, 0);
      lmFlag(c, 1.6, 1.5, 1.8);
    },
    tlatelolco(c) {   // the great market: a paved plaza of stalls under coloured awnings, piles of maize, cacao, chili, jade, a temple at the corner
      bx(c.body, M.lime, 3.8, .05, 3.8, 0, 0, 0);
      lmSteps(c, M.lime2, 1.5, 1.5, 4, .3, -1.1, -1.1, .25); stairs(c, M.lime, .4, -1.1, 1.5, 4, .3, .25, -1.1);
      bx(c.body, LMM.white, .6, .45, .5, -1.1, 1.2, -1.15); py(c.roof, MT.thatch, .75, .4, .65, -1.1, 1.65, -1.15);
      const awn = [c.cm, M.aRed, M.aBlue, MT.white, c.cm, M.maize], goods = [M.maize, M.cacao, MT.red, M.jade, M.feather, MT.white];
      let k = 0;
      for (const z of [.2, 1.3]) for (const x of [-1.15, 0, 1.15]) {
        bx(c.body, M.reed, .8, .02, .7, x, .05, z); bx(c.body, awn[k], .85, .04, .75, x, .72, z).rotation.x = -.25;
        for (const s of [-1, 1]) cy(c.body, MT.dwood, .025, .78, x + s * .38, .05, z + .32);
        sp(c.body, goods[k], .15, x - .17, .12, z - .05); sp(c.body, goods[(k + 2) % 6], .12, x + .18, .1, z + .05); k++;
      }
      for (let i = 0; i < 3; i++) sp(c.body, M.cacao, .16, .5 + i * .33, .18, -1.1);
      for (const x of [1.55, 1.25]) cy(c.body, M.clay, .14, .35, x, .05, -1.5);
      lmFlag(c, 1.7, -.45, 2.0);
    },
    jaguartapinagi(c) {   // the Temple of the Jaguar: a steep nine-stepped pyramid, a tall roof comb, jaguar statues, jungle trees
      const S = mat(0xcfc5a8, .95), S2 = mat(0xa89c80, .95);
      bx(c.body, LMM.turf, 3.8, .04, 3.8, 0, 0, 0);
      lmSteps(c, S, 2.6, 2.4, 9, .3, 0, -.5, .18); stairs(c, S2, .55, -.5, 2.4, 9, .3, .18);
      bx(c.body, S, .9, .8, .7, 0, 2.7, -.6); bx(c.body, MT.black, .25, .45, .04, 0, 2.7, -.24);
      bx(c.body, S2, .95, .15, .75, 0, 3.5, -.6); bx(c.body, S, .7, .9, .25, 0, 3.65, -.75); bx(c.body, S2, .5, .2, .27, 0, 4.0, -.75); bx(c.body, M.aRed, .72, .1, .27, 0, 4.45, -.75);
      for (const s of [-1, 1]) { bx(c.body, S2, .3, .25, .55, s * .7, 0, 1.1); jaguar(c, s * .7, .25, 1.1, 0); }
      for (const [x, z, r] of [[-1.55, 1.4, .4], [1.55, .9, .35], [-1.55, -1.45, .35], [1.55, -1.45, .35]]) { cy(c.body, LMM.bark, .07, .8, x, 0, z); sp(c.roof, MT.dgreen, r, x, .8 + r * .6, z); }
      bx(c.body, S2, .3, .9, .15, 1.0, 0, 1.6); bx(c.body, M.jade, .2, .2, .02, 1.0, .55, 1.68);
      lmFlag(c, .55, -.85, 3.7);
    },
    templomayor(c) {   // the Great Temple: a stepped pyramid with twin stairs and twin shrines (Tlaloc blue and white, Huitzilopochtli red)
      const S = M.lime, S2 = M.lime2;
      bx(c.body, S2, 3.8, .04, 3.8, 0, 0, 0);
      lmSteps(c, S, 3.4, 2.9, 4, .45, 0, -.35, .32);
      for (const sx of [-.55, .55]) stairs(c, S2, .7, -.35, 2.9, 4, .45, .32, sx);
      bx(c.body, M.aRed, .12, 1.8, .9, 0, 0, .7);
      for (const sx of [-.95, -.15, .15, .95]) { bx(c.body, M.jade, .22, .2, .3, sx, 0, 1.25); bx(c.body, MT.red, .04, .02, .12, sx, .02, 1.45); }
      bx(c.body, LMM.white, .95, .75, .9, -.6, 1.8, -.55); for (let i = 0; i < 3; i++) bx(c.body, i & 1 ? LMM.white : M.aBlue, .95, .18, .9, -.6, 2.55 + i * .18, -.55);
      bx(c.body, M.aBlue, .7, .14, .1, -.6, 3.09, -.15);
      bx(c.body, LMM.white, .95, .75, .9, .6, 1.8, -.55); bx(c.body, M.aRed, .95, .55, .9, .6, 2.55, -.55); bx(c.body, M.aRed, .7, .14, .1, .6, 3.1, -.15);
      for (let i = 0; i < 4; i++) sp(c.body, LMM.white, .05, .3 + i * .2, 2.8, -.09);
      for (const s of [-1, 1]) bx(c.body, MT.black, .3, .45, .04, s * .6, 1.8, -.09);
      for (const s of [-1, 1]) { cy(c.body, M.basalt, .1, .25, s * .95, 1.8, .35); sp(c.body, MT.glow, .07, s * .95, 2.1, .35); c.chim.push(s * .95, 2.2, .35); }
      bx(c.body, M.basalt, .25, .12, .4, 0, 1.8, .3); bx(c.body, M.basalt, .14, .14, .12, 0, 1.92, .45);
      mk(G.wheel, c.body, S2, .05, .7, .7, 0, .03, 1.45).rotation.z = PI / 2;
      lmFlag(c, 0, -.9, 3.6);
    },
    topsahasi(c) {   // the ball court: an I-shaped court between sloped walls, stone rings, shrines on the walls, two players and the ball
      const S = M.lime, S2 = M.lime2, P = mat(0xe8dcc0, .9);
      bx(c.body, LMM.turf, 3.8, .04, 3.8, 0, 0, 0);
      bx(c.body, P, .9, .06, 2.4, 0, 0, 0); for (const s of [-1, 1]) bx(c.body, P, 2.4, .06, .7, 0, 0, s * 1.45);
      for (const s of [-1, 1]) {
        bx(c.body, S2, .2, .3, 2.4, s * .55, 0, 0); bx(c.body, S, .08, .9, 2.4, s * .68, .28, 0).rotation.z = -s * .6;
        bx(c.body, S, .8, 1.0, 2.4, s * 1.35, 0, 0); bx(c.body, S2, .82, .1, 2.42, s * 1.35, 1.0, 0);
        bx(c.body, LMM.white, .5, .45, .5, s * 1.35, 1.1, 0); bx(c.body, MT.black, .04, .25, .2, s * 1.09, 1.1, 0); py(c.roof, MT.thatch, .65, .35, .65, s * 1.35, 1.55, 0);
        mk(G.wheel, c.body, S2, .08, .4, .4, s * .9, .8, 0); mk(G.wheel, c.body, MT.black, .09, .2, .2, s * .9, .8, 0);
        bx(c.body, S, 2.4, .5, .2, 0, 0, s * 1.85);
      }
      lmSteps(c, S2, .8, .45, 2, .2, 0, -1.45, .2); bx(c.body, M.aRed, .3, .3, .2, 0, .4, -1.45);
      for (const [x, z, m] of [[-.2, .6, c.cm], [.2, -.5, M.aRed]]) { bx(c.body, m, .14, .3, .1, x, 0, z); bx(c.body, MT.leather, .18, .08, .14, x, .14, z); sp(c.body, MT.skin, .06, x, .38, z); }
      sp(c.body, LMM.black, .08, .1, .1, .2);
      lmFlag(c, -1.6, .9, 2.4);
    },
    gunespiramidi(c) {   // the Pyramid of the Sun: a broad five-tiered pyramid, its stair, the front platform, a shrine under a golden sun
      const S = M.volc, S2 = M.volcD;
      bx(c.body, mat(0xa89078, .95), 3.9, .04, 3.9, 0, 0, 0);
      lmSteps(c, S, 3.4, 3.0, 5, .5, 0, -.45, .5);
      for (let i = 0; i < 5; i++) bx(c.body, S2, 3.44 - i * .5, .06, 3.04 - i * .5, 0, i * .5 + .44, -.45);
      stairs(c, S2, .7, -.45, 3.0, 5, .5, .5);
      lmSteps(c, S, 2.0, .7, 2, .3, 0, 1.4, .2); bx(c.body, S2, .7, .3, .2, 0, 0, 1.82);
      for (const s of [-1, 1]) lmSteps(c, S, .6, .6, 2, .25, s * 1.55, 1.55, .15);
      bx(c.body, M.aRed, .9, .6, .7, 0, 2.5, -.5); bx(c.body, MT.black, .25, .4, .04, 0, 2.5, -.14); py(c.roof, MT.thatch, 1.0, .4, .8, 0, 3.1, -.5);
      const sun = mk(G.wheel, c.roof, LMM.goldm, .06, .7, .7, 0, 3.55, -.1); sun.rotation.y = PI / 2;
      for (let i = 0; i < 8; i++) { const a = i / 8 * PI * 2; bx(c.roof, LMM.goldm, .07, .2, .03, Math.cos(a) * .38, 3.55 + Math.sin(a) * .38, -.08).rotation.z = a - PI / 2; }
      for (const s of [-1, 1]) { cy(c.body, M.basalt, .08, .2, s * .55, 2.5, -.05); sp(c.body, MT.glow, .06, s * .55, 2.74, -.05); c.chim.push(s * .55, 2.85, -.05); }
      lmFlag(c, -.6, -.75, 3.4);
    },
    taktakvim(c) {   // the Sun Stone temple: a platform, the great painted calendar disc in a feathered frame, braziers, shields and darts
      const B = M.basalt, S = M.lime;
      bx(c.body, M.lime2, 3.8, .04, 3.8, 0, 0, 0);
      lmSteps(c, S, 3.4, 2.4, 2, .3, 0, -.5, .3);
      for (let i = 0; i < 4; i++) bx(c.body, M.lime2, 1.0, .15 * (i + 1), .15, 0, 0, .95 - i * .15);
      for (const s of [-1, 1]) bx(c.body, M.aRed, .3, 2.4, .35, s * 1.3, .6, -.7);
      bx(c.body, M.aRed, 2.9, .3, .4, 0, 3.0, -.7);
      for (let i = 0; i < 7; i++) bx(c.body, i & 1 ? c.cm : M.feather, .1, .3, .05, -1.2 + i * .4, 3.3, -.7);
      const disc = (m, D, z) => { mk(G.wheel, c.body, m, .05, D, D, 0, 1.85, z).rotation.y = PI / 2; };
      mk(G.wheel, c.body, B, .25, 2.1, 2.1, 0, 1.85, -.75).rotation.y = PI / 2;
      disc(M.aRed, 1.75, -.6); disc(M.aBlue, 1.35, -.57); disc(LMM.goldm, .95, -.54); disc(S, .55, -.51);
      for (let i = 0; i < 8; i++) { const a = (i + .5) / 8 * PI * 2; bx(c.body, LMM.goldm, .08, .22, .03, Math.cos(a) * .7, 1.85 + Math.sin(a) * .7, -.56).rotation.z = a - PI / 2; }
      sp(c.body, LMM.goldm, .14, 0, 1.85, -.47); bx(c.body, M.aRed, .06, .1, .03, 0, 1.68, -.34);
      for (const s of [-1, 1]) { cy(c.body, B, .14, .35, s * 1.15, .6, .3); sp(c.body, MT.glow, .1, s * 1.15, 1.0, .3); c.chim.push(s * 1.15, 1.1, .3); }
      for (const s of [-1, 1]) {
        mk(G.wheel, c.body, c.cm, .05, .4, .4, s * 1.55, .35, 1.25).rotation.y = PI / 2;
        for (let i = 0; i < 3; i++) { const x = s * 1.55 + (i - 1) * .12; cy(c.body, MT.dwood, .015, 1.2, x, 0, 1.0); cn(c.body, LMM.black, .03, .1, x, 1.2, 1.0); }
      }
      lmFlag(c, 1.6, -1.55, 2.2);
    },

    // ---------------- Bizanslılar ----------------
    bukoleon(c) {   // the harbour palace: a marble façade with great arched windows on the sea wall, a harbour with moles, a dromon
      const W = LMM.marble, St = M.bzW;
      bx(c.body, LMM.water, 3.8, .04, 1.6, 0, 0, 1.15); bx(c.body, St, 3.8, .2, 2.3, 0, 0, -.8);
      bx(c.body, St, 3.6, .9, .4, 0, 0, .25); for (let i = 0; i < 2; i++) bx(c.body, M.bzB, 3.62, .07, .42, 0, .3 + i * .3, .25);
      bx(c.body, W, 2.8, 1.1, 1.1, -.2, .9, -.05);
      for (let i = 0; i < 3; i++) { const x = -1.1 + i * .9; bx(c.body, MT.black, .4, .6, .04, x, 1.1, .51); py(c.body, MT.black, .4, .2, .04, x, 1.7, .51); }
      bx(c.body, W, 2.8, .08, .3, -.2, .9, .6); lmCols(c, 6, -1.5, 1.1, .7, .65, W, .04, .98); bx(c.body, c.cm, 2.8, .08, .04, -.2, 1.85, .52);
      gableX(c, MT.tile, 2.9, .5, 1.2, -.2, 2.0, -.05);
      bx(c.body, M.bzB, .9, 1.4, .9, 1.0, .2, -1.2); cy(c.body, M.bzB, .35, .25, 1.0, 1.6, -1.2); lmDome(c, LMM.lead, .4, 1.0, 1.85, -1.2);
      bx(c.roof, MT.gold, .03, .25, .03, 1.0, 2.25, -1.2); bx(c.roof, MT.gold, .15, .03, .03, 1.0, 2.4, -1.2);
      bx(c.body, St, .6, 2.4, .6, -1.5, .2, -1.4); lmCren(c, St, .62, .62, 2.6, -1.5, -1.4, .1);
      for (const s of [-1, 1]) bx(c.body, St, .3, .3, 1.3, s * 1.6, 0, 1.2);
      bx(c.body, W, .3, .3, .3, 1.6, .3, 1.6); bx(c.body, M.lion, .14, .16, .32, 1.6, .6, 1.6); bx(c.body, M.lion, .16, .16, .12, 1.6, .7, 1.78);
      bx(c.body, St, .8, .2, .3, -.2, 0, .6);
      dromon(c, -.2, 1.3, PI / 2, 1.8);
      lmFlag(c, 1.65, -.5, 2.4);
    },
    hipodrom(c) {   // the Hippodrome: a long track with a curved end, tiered stands, the spina with obelisks and serpent column, the bronze horses
      const W = LMM.marble, St = M.bzW, Sd = LMM.sand, zc = -.6;
      bx(c.body, Sd, 1.7, .04, 2.2, 0, 0, .45); cy(c.body, Sd, .85, .04, 0, 0, zc);
      for (const s of [-1, 1]) {
        bx(c.body, St, .5, .25, 2.0, s * 1.1, 0, .45); bx(c.body, St, .35, .25, 2.0, s * 1.18, .25, .45); bx(c.body, St, .2, .25, 2.0, s * 1.25, .5, .45);
        bx(c.body, St, .1, .9, 2.0, s * 1.37, 0, .45);
      }
      for (let i = 0; i < 7; i++) {
        const a = PI + (i + .5) / 7 * PI, ca = Math.cos(a), sa = Math.sin(a);
        bx(c.body, St, .55, .5, .45, ca * 1.12, 0, zc + sa * 1.12).rotation.y = -a + PI / 2;
        bx(c.body, St, .6, .4, .2, ca * 1.32, .5, zc + sa * 1.32).rotation.y = -a + PI / 2;
      }
      bx(c.body, W, .22, .15, 1.7, 0, 0, .35);
      bx(c.body, W, .25, .25, .25, 0, .15, .8); bx(c.body, M.granite, .14, 1.3, .14, 0, .4, .8); py(c.body, M.granite, .14, .18, .14, 0, 1.7, .8);
      cy(c.body, MT.bronze, .05, .8, 0, .15, .25); for (const x of [-.07, 0, .07]) sp(c.body, MT.bronze, .05, x, .98, .25);
      bx(c.body, St, .18, 1.6, .18, 0, .15, -.3); py(c.body, St, .18, .2, .18, 0, 1.75, -.3);
      for (const z of [-.45, 1.15]) cn(c.body, LMM.goldm, .08, .4, 0, .15, z);
      bx(c.body, W, .5, .5, .7, 1.3, .75, .45); lmGable(c, MT.tile, .6, .3, .8, 1.3, 1.25, .45); bx(c.body, c.cm, .03, .3, .5, 1.04, .8, .45);
      bx(c.body, St, 2.6, .7, .3, 0, 0, 1.65); for (let i = 0; i < 6; i++) bx(c.body, MT.black, .25, .45, .04, -1.0 + i * .4, 0, 1.81);
      for (let i = 0; i < 4; i++) { const x = -.3 + i * .2; bx(c.body, MT.bronze, .1, .22, .32, x, .7, 1.65); bx(c.body, MT.bronze, .07, .14, .1, x, .9, 1.78); }
      at(c, -.62, .1, 0, M.horse2); at(c, -.42, .1, 0, M.horse);
      bx(c.body, c.cm, .3, .25, .2, -.52, .1, -.3); for (const s of [-1, 1]) mk(G.wheel, c.body, MT.dwood, .04, .3, .3, -.52 + s * .18, .15, -.32);
      lmFlag(c, -1.3, 1.0, 1.9);
    },
    ayasofya(c) {   // Hagia Sophia: a great shallow dome on a windowed drum, half domes front and back, buttresses, aisles, four minarets
      const P = M.bzP, Pd = M.bzPd;
      bx(c.body, MT.stone, 3.7, .08, 3.7, 0, 0, 0);
      bx(c.body, P, 2.0, 1.5, 2.0, 0, 0, -.3);
      for (const s of [-1, 1]) { bx(c.body, P, .5, 1.0, 2.4, s * 1.25, 0, -.3); bx(c.roof, LMM.lead, .55, .06, 2.45, s * 1.25, 1.0, -.3); }
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(c.body, Pd, .35, 1.9, .5, sx * 1.05, 0, -.3 + sz * .75);
      cy(c.body, P, .85, .3, 0, 1.5, -.3);
      for (let i = 0; i < 10; i++) { const a = i / 10 * PI * 2; bx(c.body, MT.black, .08, .16, .03, Math.sin(a) * .86, 1.56, -.3 + Math.cos(a) * .86).rotation.y = a; }
      lmDome(c, LMM.lead, .95, 0, 1.8, -.3, .55); cy(c.roof, MT.gold, .02, .3, 0, 2.3, -.3); sp(c.roof, MT.gold, .05, 0, 2.62, -.3);
      cy(c.body, P, .7, 1.5, 0, 0, -1.15); bx(c.body, P, 2.4, 1.2, .6, 0, 0, 1.0); bx(c.body, P, 1.5, .3, .6, 0, 1.2, 1.0); bx(c.roof, LMM.lead, 2.45, .06, .65, 0, 1.2, 1.0);
      for (const s of [-1, 1]) lmDome(c, LMM.lead, .75, 0, 1.5, -.3 + s * .85, .6);
      for (const s of [-1, 1]) lmDome(c, LMM.lead, .35, s * .6, 1.5, -1.05, .6);
      bx(c.body, MT.black, .4, .7, .04, 0, 0, 1.31); bx(c.body, c.cm, .9, .08, .04, 0, .85, 1.32);
      lmMinaret(c, -1.7, -1.7, 3.6, M.bzB); lmMinaret(c, 1.7, -1.7, 3.6); lmMinaret(c, -1.7, 1.45, 3.3); lmMinaret(c, 1.7, 1.45, 3.3, M.bzB);
      lmFlag(c, 1.0, 1.45, 1.8);
    },
    theodosius(c) {   // the Theodosian land walls: a moat, a low parapet, the outer wall with small towers, the tall inner wall, the Golden Gate
      const S = mat(0xc2b49a, .92), B = M.bzB;
      bx(c.body, MT.soil2, 3.9, .04, 3.9, 0, 0, 0);
      bx(c.body, LMM.water, 3.9, .05, .45, 0, 0, 1.65); bx(c.body, MT.wood, .5, .1, .6, 0, 0, 1.6);
      bx(c.body, S, 3.9, .35, .12, 0, 0, 1.38); lmCren(c, S, 3.9, .12, .35, 0, 1.38, .1);
      bx(c.body, S, 3.9, 1.1, .25, 0, 0, .75); for (const y of [.35, .75]) bx(c.body, B, 3.92, .07, .27, 0, y, .75); lmCren(c, S, 3.9, .25, 1.1, 0, .75, .12);
      for (const x of [-1.5, -.75, .75, 1.5]) lmTower(c, x, .8, .45, 1.55, S);
      bx(c.body, MT.black, .4, .75, .27, 0, 0, .75);
      bx(c.body, S, 3.9, 1.9, .4, 0, 0, -.35); for (const y of [.5, 1.0, 1.5]) bx(c.body, B, 3.92, .08, .42, 0, y, -.35); lmCren(c, S, 3.9, .4, 1.9, 0, -.35, .14);
      for (const s of [-1, 1]) { lmTower(c, s * 1.55, -.3, .65, 2.7, S); for (const y of [.8, 1.6]) bx(c.body, B, .67, .08, .67, s * 1.55, y, -.3); lmTower(c, s * .5, -.3, .6, 2.8, LMM.marble); }
      bx(c.body, MT.black, .38, 1.0, .44, 0, 0, -.35); bx(c.body, LMM.goldm, .36, .95, .03, 0, 0, -.13); bx(c.body, LMM.marble, .5, .2, .45, 0, 1.0, -.35);
      bx(c.body, MT.plaster, .6, .6, .5, -1.2, 0, -1.35); lmGable(c, MT.tile, .7, .3, .6, -1.2, .6, -1.35);
      bx(c.body, MT.plaster, .5, .5, .5, 1.5, 0, -1.55); lmGable(c, MT.tile, .6, .3, .6, 1.5, .5, -1.55);
      bx(c.body, B, .7, .8, .7, .45, 0, -1.4); cy(c.body, B, .28, .15, .45, .8, -1.4); lmDome(c, LMM.lead, .3, .45, .95, -1.4); bx(c.roof, MT.gold, .03, .2, .03, .45, 1.25, -1.4);
      lmFlag(c, -.5, -.35, 3.5);
    },
    darphane(c) {   // the mint: a banded stone and brick hall with a giant gold solidus on its front, a domed treasury, a furnace, coin presses and chests
      const S = M.bzW, B = M.bzB;
      const band = (w, h, d, x, z) => { bx(c.body, S, w, h, d, x, 0, z); for (let y = .3; y < h - .1; y += .35) bx(c.body, B, w + .02, .1, d + .02, x, y, z); };
      bx(c.body, MT.stone, 3.7, .05, 3.7, 0, 0, 0);
      band(2.6, 1.5, 1.4, -.4, -1.0); gableX(c, MT.tile, 2.7, .55, 1.5, -.4, 1.5, -1.0);
      mk(G.wheel, c.body, MT.bronze, .04, .9, .9, -.4, .9, -.28).rotation.y = PI / 2; mk(G.wheel, c.body, LMM.goldm, .06, .8, .8, -.4, .9, -.26).rotation.y = PI / 2;
      mk(G.wheel, c.body, c.cm, .07, .3, .3, -.4, .9, -.24).rotation.y = PI / 2;
      bx(c.body, MT.black, .4, .65, .04, .55, 0, -.29); for (const x of [-1.4, -1.0]) bx(c.body, MT.black, .16, .3, .04, x, .7, -.29);
      band(.9, 1.1, .9, 1.45, -1.25); cy(c.body, B, .35, .2, 1.45, 1.1, -1.25); lmDome(c, LMM.lead, .38, 1.45, 1.3, -1.25); sp(c.roof, MT.gold, .04, 1.45, 1.72, -1.25);
      cy(c.body, B, .35, .7, 1.35, 0, .15); bx(c.body, MT.glow, .2, .2, .03, 1.35, .1, .5); cy(c.body, B, .13, 1.6, 1.35, .7, .15); c.chim.push(1.35, 2.4, .15);
      bx(c.body, MT.wood, .9, .4, .45, -.6, 0, .5); bx(c.body, MT.iron, .15, .12, .15, -.85, .4, .5); bx(c.body, MT.dwood, .04, .3, .04, -.7, .4, .5);
      for (const [x, h] of [[-.45, .12], [-.3, .2], [-.15, .08]]) cy(c.body, LMM.goldm, .06, h, x, .4, .55);
      for (let i = 0; i < 2; i++) { const x = .2 + i * .55; bx(c.body, MT.dwood, .45, .3, .3, x, 0, 1.1); bx(c.body, MT.gold, .47, .04, .32, x, .18, 1.1); bx(c.body, LMM.goldm, .4, .05, .25, x, .3, 1.1); }
      cy(c.body, MT.bronze, .02, .55, -1.4, 0, 1.2); bx(c.body, MT.bronze, .45, .02, .02, -1.4, .55, 1.2); for (const s of [-1, 1]) cy(c.body, MT.bronze, .08, .02, -1.4 + s * .2, .4, 1.2);
      lmFlag(c, -1.6, .2, 2.3);
    },
    rumatesi(c) {   // the Greek fire workshop: a brick workshop and chimney, bubbling cauldrons, amphorae and barrels, a siphon, a dromon spraying fire
      const B = M.bzB, S = M.bzW;
      bx(c.body, MT.soil2, 3.8, .04, 2.6, 0, 0, -.6); bx(c.body, LMM.water, 3.8, .04, 1.2, 0, 0, 1.3); bx(c.body, S, 3.8, .25, .2, 0, 0, .75);
      bx(c.body, B, 2.2, 1.3, 1.3, -.7, 0, -1.2); for (const y of [.45, .9]) bx(c.body, S, 2.22, .1, 1.32, -.7, y, -1.2); gableX(c, MT.tile, 2.3, .5, 1.4, -.7, 1.3, -1.2);
      bx(c.body, MT.black, 1.0, .8, .04, -.7, 0, -.54); bx(c.body, MT.glow, .6, .3, .03, -.7, .05, -.53);
      cy(c.body, B, .17, 2.6, .1, 0, -1.6); cy(c.body, MT.dstone, .2, .1, .1, 2.6, -1.6); c.chim.push(.1, 2.75, -1.6);
      for (const x of [-1.3, -.5]) { cn(c.body, MT.glow, .18, .2, x, 0, 0); cy(c.body, MT.iron, .22, .3, x, .15, 0); cy(c.body, LMM.black, .19, .02, x, .45, 0); c.chim.push(x, .7, 0); }
      for (let i = 0; i < 5; i++) { const x = .6 + i * .25; sp(c.body, M.clay, .12, x, .17, -.9); cy(c.body, M.clay, .04, .12, x, .27, -.9); }
      for (const z of [-1.55, -1.15]) cy(c.body, MT.dwood, .16, .4, 1.6, 0, z);
      bx(c.body, MT.wood, .35, .35, .45, 1.0, 0, .1); cy(c.body, MT.bronze, .05, .5, 1.0, .4, .3).rotation.x = PI / 2; sp(c.body, MT.bronze, .07, 1.0, .42, .4);
      dromon(c, -.4, 1.35, PI / 2, 1.7, true);
      bx(c.body, MT.dwood, .5, .08, .5, 1.45, 0, 1.35); cn(c.body, MT.glow, .2, .45, 1.45, .08, 1.35); c.chim.push(1.45, .6, 1.35);
      lmFlag(c, 1.65, -.4, 2.2);
    },
    yerebatan(c) {   // the Basilica Cistern: a forest of marble columns standing in water under brick arches and vaults, a Medusa head, the entrance kiosk
      const W = LMM.marble, B = M.bzB, S = M.bzW;
      bx(c.body, LMM.water, 3.3, .04, 2.6, 0, 0, -.45);
      bx(c.body, S, 3.6, 1.45, .15, 0, 0, -1.82); for (const s of [-1, 1]) bx(c.body, S, .15, 1.45, 2.8, s * 1.72, 0, -.45);
      const xs = [-1.2, -.4, .4, 1.2], zs = [-1.4, -.8, -.2, .4];
      for (const x of xs) for (const z of zs) { cy(c.body, W, .07, 1.15, x, 0, z); bx(c.body, W, .2, .1, .2, x, 1.15, z); }
      for (const z of zs) bx(c.body, B, 2.6, .12, .1, 0, 1.25, z);
      for (const x of xs) bx(c.body, B, .1, .12, 2.0, x, 1.25, -.5);
      bx(c.body, B, 3.3, .1, 1.0, 0, 1.37, -1.3); for (const x of xs) lmDome(c, B, .3, x, 1.47, -1.3, .35);
      sp(c.body, M.medusa, .14, .4, .12, .55);
      for (const [x, z] of [[-1.2, .4], [.4, -.2], [1.2, .4], [-.4, -.8]]) sp(c.body, MT.glow, .05, x, .9, z + .09);
      bx(c.body, S, 3.6, .35, .15, 0, 0, .95);
      bx(c.body, S, .9, .9, .7, -1.2, 0, 1.45); bx(c.body, B, .92, .1, .72, -1.2, .4, 1.45); py(c.roof, MT.tile, 1.1, .45, .9, -1.2, .9, 1.45); bx(c.body, MT.black, .3, .55, .04, -1.2, 0, 1.81);
      bx(c.body, S, .6, .2, .4, .2, 0, 1.4); bx(c.body, c.cm, .5, .08, .04, -1.2, .7, 1.81);
      lmFlag(c, 1.5, 1.4, 2.0);
    },
    varangkisla(c) {   // the Varangian Guard barracks: a banded hall, a tower, a wall of round shields, axe racks, training posts, guards at the gate
      const S = M.bzW, B = M.bzB;
      bx(c.body, MT.soil2, 3.8, .04, 3.8, 0, 0, 0);
      bx(c.body, S, 3.2, 1.2, 1.1, -.1, 0, -1.25); for (const y of [.35, .75]) bx(c.body, B, 3.22, .1, 1.12, -.1, y, -1.25); gableX(c, MT.tile, 3.3, .55, 1.3, -.1, 1.2, -1.25);
      for (const x of [-1.0, .8]) bx(c.body, MT.black, .4, .7, .04, x, 0, -.69);
      lmTower(c, 1.45, -1.3, .8, 2.4, S);
      for (const x of [-1.5, -.5, -.05, .4, 1.25]) { mk(G.wheel, c.body, x === -.05 ? M.shield : c.cm, .05, .42, .42, x, .6, -.66).rotation.y = PI / 2; sp(c.body, MT.iron, .05, x, .6, -.62); }
      for (const x of [-1.6, -.8]) bx(c.body, MT.dwood, .07, 1.0, .07, x, 0, .2); bx(c.body, MT.dwood, .9, .06, .08, -1.2, .9, .2);
      for (let i = 0; i < 4; i++) { const x = -1.5 + i * .2; cy(c.body, MT.dwood, .018, 1.1, x, 0, .27); bx(c.body, MT.steel, .03, .2, .16, x, .85, .33); }
      for (const x of [.3, .9]) { cy(c.body, MT.dwood, .07, 1.0, x, 0, .7); bx(c.body, MT.dwood, .4, .05, .05, x, .7, .7); }
      cn(c.body, MT.glow, .14, .25, -.3, 0, 1.2); for (const r of [.5, -.5]) bx(c.body, MT.dwood, .35, .06, .06, -.3, 0, 1.2).rotation.y = r; c.chim.push(-.3, .5, 1.2);
      for (const s of [-1, 1]) { bx(c.body, S, 1.3, .7, .25, s * 1.25, 0, 1.7); lmCren(c, S, 1.3, .25, .7, s * 1.25, 1.7, .1); bx(c.body, S, .25, .7, 2.2, s * 1.75, 0, .55); }
      lmArch(c, S, 0, 1.7, 1.2, 1.2, .3);
      muhafiz(c, -.45, 1.45); muhafiz(c, .35, 1.45);
      lmFlag(c, 1.45, -1.3, 3.2);
    },
  };
}
