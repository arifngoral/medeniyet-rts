// Age-up building models (landmarks.js looks) of the Koreans, the Malians and the Mongols. See index.js.
export default function (K) {
  const { THREE, PI, G, MT, XM, LMM, mat, mk, bx, cy, cn, py, sp, lmFlag, lmDome, lmGable, lmMinaret, lmCols, lmCren, lmTower, lmWall, lmPagoda, lmSteps, lmArch, lmShip } = K;
  const M = {
    // Korea
    kstone: mat(0xb8b2a4, .95), kstoneL: mat(0xd2ccbe, .92), dan: mat(0x3f8a6a, .7), onggi: mat(0x6a3e22, .55), onggiL: mat(0x7d4a28, .55),
    brickG: mat(0x5c5a58, .9), yard: mat(0xb8a586, 1), hull: mat(0x5a3c22, .9), shell: mat(0x4a5a4e, .7), sailK: mat(0xa07850, .95),
    // Mali
    mudD: mat(0x9a7448, .95), mudL: mat(0xc49e6a, .95), indigo: mat(0x2c3e7a, .9), ochre: mat(0xc8862a, .9), laterite: mat(0xb0683a, 1),
    calab: mat(0xc98a3a, .8), salt: mat(0xe8e4da, .8), camel: mat(0xc09a62, .95),
    // Mongols
    felt: mat(0xece4d2, .95), feltD: mat(0x56524c, .95), rope: mat(0x7a5a3a, .95), door: mat(0xd8752a, .7), silver: mat(0xd0d4da, .4, .3),
    // animals
    hBrown: mat(0x7a4a28, .9), hDark: mat(0x3a2a1c, .9), hGrey: mat(0xc8c0b0, .9), hDun: mat(0xb08a58, .9), wool: mat(0xeae2cf, 1),
  };
  const grp = (c, x, z, ry = 0, y = 0) => { const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; c.body.add(g); return g; };

  // a Korean hip-and-gable tiled roof: hipped skirt, gable top, dark ridge, upturned eave tips
  function hanokRoof(c, x, y, z, w, d, h = .8, m = LMM.dtile) {
    py(c.roof, m, w, h * .5, d, x, y, z);
    lmGable(c, m, d * .5, h * .5, w * .62, x, y + h * .32, z, PI / 2);
    bx(c.roof, LMM.black, w * .64, .06, .07, x, y + h * .8, z);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const o = cn(c.roof, m, .05, .22, x + sx * w * .47, y - .02, z + sz * d * .47); o.rotation.z = -sx * .6; o.rotation.x = sz * .6; }
  }
  // a Korean hall: plaster body, red columns in front, a green painted band, a tiled roof
  function hall(c, x, z, w, d, h, y0 = 0, rh = .8, n = 4) {
    bx(c.body, MT.plaster, w * .9, h, d * .85, x, y0, z);
    lmCols(c, n, x - w * .45, x + w * .45, z + d * .45, h, LMM.lacq, .05, y0);
    bx(c.body, M.dan, w * .96, .1, d * .92, x, y0 + h - .1, z);
    bx(c.body, MT.lwood, w * .35, h * .7, .03, x, y0, z + d * .43);
    hanokRoof(c, x, y0 + h, z, w * 1.3, d * 1.45, rh);
  }
  function onggi(c, x, z, r, y = 0, m = M.onggi) { sp(c.body, m, r, x, y + r * .9, z); cy(c.body, m, r * .62, .07, x, y + r * 1.7, z); }

  // Sahel mud building parts: toron beams pushed through a wall or tower, cone pinnacles with ostrich eggs
  const beamX = (c, x, y, z, L) => bx(c.body, MT.dwood, L, .04, .04, x, y, z);
  const beamZ = (c, x, y, z, L) => bx(c.body, MT.dwood, .04, .04, L, x, y, z);
  const pinn = (c, x, y, z, r = .08, h = .25, m = M.mudL) => cn(c.body, m, r, h, x, y, z);
  const egg = (c, x, y, z) => sp(c.roof, LMM.white, .06, x, y, z);
  function mudTower(c, x, z, w, h, m = LMM.mud) {   // a stepped tapering Sahel tower with toron beams and an egg on top
    bx(c.body, m, w, h * .5, w, x, 0, z); bx(c.body, m, w * .76, h * .3, w * .76, x, h * .5, z); cn(c.body, m, w * .4, h * .3, x, h * .8, z);
    for (const t of [.25, .62]) { const k = t < .5 ? w : w * .76; beamX(c, x, h * t, z + k * .2, k + .3); beamZ(c, x + k * .2, h * t + .06, z, k + .3); }
    egg(c, x, h * 1.1 + .05, z);
  }
  const hut = (c, x, z, r = .35, h = .6) => { cy(c.body, LMM.mud, r, h, x, 0, z); cn(c.roof, MT.thatch, r * 1.3, r * 1.4, x, h, z); bx(c.body, MT.black, r * .45, h * .6, .03, x, 0, z + r); };

  // a Mongol ger: felt wall, low dome roof, wooden crown, rope band, a painted door (facing ry)
  function ger(c, x, z, r, h, ry = 0, m = M.felt, roof = m, door = M.door) {
    cy(c.body, m, r, h, x, 0, z); lmDome(c, roof, r * 1.03, x, h, z, .42);
    cy(c.roof, MT.dwood, r * .17, .06, x, h + r * .4, z); cy(c.body, M.rope, r * 1.015, .04, x, h * .55, z);
    bx(c.body, door, r * .4, h * .85, .05, x + Math.sin(ry) * r, 0, z + Math.cos(ry) * r).rotation.y = ry;
  }
  const tug = (c, x, z, h, hair = MT.white) => { cy(c.body, MT.dwood, .025, h, x, 0, z); sp(c.body, hair, .1, x, h - .12, z); cn(c.roof, MT.steel, .035, .18, x, h, z); };

  // animals (each in its own group)
  function horse(c, x, z, ry, coat = M.hBrown, cloth = null, rider = null) {
    const g = grp(c, x, z, ry);
    bx(g, coat, .16, .17, .48, 0, .3, 0);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, coat, .045, .3, .05, sx * .05, 0, sz * .18);
    bx(g, coat, .08, .26, .1, 0, .38, .2).rotation.x = .55; bx(g, coat, .08, .09, .2, 0, .58, .33);
    bx(g, XM.hair, .03, .22, .04, 0, .22, -.25); bx(g, XM.hair, .02, .2, .05, 0, .45, .17).rotation.x = .55;
    if (cloth) bx(g, cloth, .19, .12, .26, 0, .4, -.02);
    if (rider) { bx(g, rider, .12, .24, .1, 0, .47, -.04); bx(g, rider, .2, .06, .08, 0, .43, -.04); sp(g, MT.skin, .045, 0, .76, -.04); cn(g, XM.fur, .055, .08, 0, .79, -.04); }
    return g;
  }
  function camel(c, x, z, ry, load = null) {
    const g = grp(c, x, z, ry), C = M.camel;
    bx(g, C, .18, .2, .55, 0, .45, 0); sp(g, C, .13, 0, .7, -.04);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, C, .05, .46, .05, sx * .06, 0, sz * .2);
    bx(g, C, .07, .32, .08, 0, .5, .26).rotation.x = .7; bx(g, C, .08, .08, .2, 0, .72, .42);
    if (load) for (const s of [-1, 1]) bx(g, load, .06, .18, .3, s * .13, .42, 0);
    return g;
  }
  const sheep = (c, x, z, ry, m = M.wool) => { sp(c.body, m, .12, x, .15, z); sp(c.body, LMM.black, .05, x + Math.sin(ry) * .13, .21, z + Math.cos(ry) * .13); };

  return {
    // ---- Koreans ----
    ambaravlu(c) {   // a jangdokdae courtyard: rows of brown onggi jars on a stone stand, a tiled storehouse, low walls
      bx(c.body, M.yard, 3.6, .04, 3.6, 0, 0, 0);
      for (const s of [-1, 1]) { bx(c.body, M.kstone, .2, .5, 3.0, s * 1.7, 0, .2); bx(c.roof, LMM.dtile, .32, .08, 3.1, s * 1.7, .5, .2); bx(c.body, M.kstone, 1.1, .5, .2, s * 1.15, 0, 1.68); bx(c.roof, LMM.dtile, 1.2, .08, .32, s * 1.15, .5, 1.68); }
      hall(c, 0, -1.3, 2.4, .8, .85, 0, .6, 5);
      bx(c.body, M.kstoneL, 2.9, .15, 1.6, 0, 0, .35);
      for (let i = 0; i < 5; i++) for (let j = 0; j < 3; j++) { const r = .14 + ((i + j) % 3) * .03; onggi(c, -1.15 + i * .575, -.1 + j * .45, r, .15, (i + j) & 1 ? M.onggiL : M.onggi); }
      for (const [x, z, r] of [[-1.35, 1.35, .22], [1.3, 1.3, .2], [-1.4, -.6, .19]]) onggi(c, x, z, r, 0);
      bx(c.body, MT.dwood, .5, .05, .3, .9, .35, 1.3); sp(c.body, M.onggiL, .06, .8, .46, 1.3);
      lmFlag(c, 1.55, -.6, 1.9);
    },
    okculukpavyon(c) {   // a raised archery pavilion (jeong) on red columns, target boards down the range
      bx(c.body, LMM.turf, 3.6, .04, 3.6, 0, 0, 0); bx(c.body, M.yard, .5, .02, 2.4, .9, .04, .4);
      bx(c.body, M.kstone, 1.8, .35, 1.4, -.7, 0, -1.05); bx(c.body, M.kstone, .6, .17, .3, -.7, 0, -.2);
      bx(c.body, MT.lwood, 1.6, .06, 1.2, -.7, .35, -1.05);
      for (const z of [-1.55, -.55]) lmCols(c, 3, -1.4, 0, z, 1.0, LMM.lacq, .05, .41);
      bx(c.body, LMM.lacq, 1.5, .12, .03, -.7, .55, -.47); bx(c.body, M.dan, 1.6, .12, 1.2, -.7, 1.29, -1.05);
      hanokRoof(c, -.7, 1.41, -1.05, 2.3, 1.7, .85);
      cy(c.body, MT.dwood, .03, .5, .0, .41, -1.3); const d = mk(G.wheel, c.body, LMM.lacq, .2, .3, .3, .0, .8, -1.3); d.rotation.y = PI / 2;
      for (const x of [.55, 1.3]) {
        bx(c.body, MT.white, .6, .75, .06, x, .12, 1.45); bx(c.body, LMM.black, .44, .55, .07, x, .22, 1.45); bx(c.body, LMM.lacq, .16, .2, .08, x, .4, 1.45);
        for (const s of [-1, 1]) bx(c.body, MT.dwood, .05, .14, .1, x + s * .25, 0, 1.45);
      }
      cy(c.body, MT.dwood, .02, 1.0, 1.7, 0, 1.1); bx(c.body, MT.wheat, .02, .22, .3, 1.7, .76, 1.25);
      bx(c.body, MT.dwood, .6, .55, .08, .9, 0, -1.1); for (let i = 0; i < 5; i++) cy(c.body, MT.lwood, .012, .7, .7 + i * .1, .05, -1.05);
      lmFlag(c, 1.6, -1.5, 2.2);
    },
    bulguksa(c) {   // Bulguksa: halls on a stone terrace, the stone stair-bridges, Dabotap and Seokgatap in the court
      const S = M.kstone, L = M.kstoneL;
      bx(c.body, S, 3.6, .55, 1.95, 0, 0, -.8); bx(c.body, L, 3.62, .06, 1.97, 0, .55, -.8);
      for (let i = 0; i < 6; i++) bx(c.body, LMM.sandD, .5, .04, .03, -1.5 + i * .6, .25, .16);
      for (const x of [-.85, .85]) {
        for (let i = 0; i < 4; i++) { const dd = (4 - i) * .19; bx(c.body, L, .55, .14, dd, x, i * .14, .17 + dd / 2); }
        for (const s of [-1, 1]) bx(c.body, S, .05, .14, .8, x + s * .3, .3, .55).rotation.x = .55;
        bx(c.body, MT.black, .25, .1, .02, x, 0, .94);
      }
      hall(c, 0, -1.3, 1.9, .75, .8, .61, .75, 5);
      for (const s of [-1, 1]) { bx(c.body, MT.plaster, .55, .5, 1.3, s * 1.55, .61, -.95); bx(c.body, LMM.lacq, .03, .5, 1.3, s * 1.27, .61, -.95); lmGable(c, LMM.dtile, .8, .35, 1.4, s * 1.55, 1.11, -.95); }
      // Seokgatap (plain three storeys) and Dabotap (ornate)
      bx(c.body, L, .4, .15, .4, -.55, .61, -.3); for (let i = 0; i < 3; i++) { bx(c.body, L, .2, .14, .2, -.55, .76 + i * .2, -.3); bx(c.body, L, .32, .05, .32, -.55, .9 + i * .2, -.3); } cy(c.body, MT.bronze, .02, .25, -.55, 1.35, -.3);
      bx(c.body, L, .44, .2, .44, .55, .61, -.3); bx(c.body, L, .26, .25, .26, .55, .81, -.3); bx(c.body, L, .4, .05, .4, .55, 1.06, -.3); cy(c.body, L, .14, .2, .55, 1.11, -.3); cy(c.body, L, .2, .04, .55, 1.31, -.3); cy(c.body, L, .1, .15, .55, 1.35, -.3); cn(c.roof, L, .16, .15, .55, 1.5, -.3); cy(c.body, MT.bronze, .02, .2, .55, 1.65, -.3);
      for (const x of [-1.5, 1.5]) { cy(c.body, LMM.bark, .05, .4, x, 0, 1.3); sp(c.body, LMM.pine, .3, x, .65, 1.3); }
      lmFlag(c, 0, .7, 1.7);
    },
    hwaseong(c) {   // Hwaseong: a stone wall with a brick parapet, Paldalmun's two-roofed gate, the half-moon outer wall, a round lookout
      const S = M.kstone, B = M.brickG;
      for (const s of [-1, 1]) {
        bx(c.body, S, 1.25, 1.1, .5, s * 1.175, 0, -.4);
        for (let i = 0; i < 4; i++) bx(c.body, B, .24, .26, .12, s * (.7 + i * .32), 1.1, -.19);
        bx(c.body, B, 1.25, .1, .12, s * 1.175, 1.1, -.6);
      }
      bx(c.body, S, 1.1, 1.3, .9, 0, 0, -.4); bx(c.body, MT.black, .45, .75, .05, 0, 0, .06); mk(G.wheel, c.body, MT.black, .05, .45, .45, 0, .75, .06).rotation.y = PI / 2;
      bx(c.body, MT.lwood, .8, .45, .6, 0, 1.3, -.4); lmCols(c, 4, -.38, .38, -.12, .45, LMM.lacq, .035, 1.3);
      py(c.roof, LMM.dtile, 1.45, .3, 1.1, 0, 1.75, -.4); bx(c.body, MT.lwood, .6, .4, .45, 0, 1.85, -.4); bx(c.body, M.dan, .64, .08, .5, 0, 2.17, -.4);
      hanokRoof(c, 0, 2.25, -.4, 1.05, .8, .6);
      for (let i = 1; i < 7; i++) { const a = i / 7 * PI, x = Math.cos(a) * .95, z = -.1 + Math.sin(a) * .95; bx(c.body, S, .45, .75, .26, x, 0, z).rotation.y = -a + PI / 2; bx(c.body, B, .3, .18, .1, x * 1.06, .75, z + .04).rotation.y = -a + PI / 2; }
      cy(c.body, B, .38, 1.5, 1.45, 0, .85); cy(c.body, S, .42, .08, 1.45, 1.5, .85); py(c.roof, LMM.dtile, .75, .4, .75, 1.45, 1.58, .85);
      for (const y of [.5, 1.0]) bx(c.body, MT.black, .1, .12, .03, 1.45, y, 1.23);
      for (const [x, z] of [[-1.55, -.55], [-1.05, -.55], [-1.55, -.15], [-1.05, -.15]]) cy(c.body, LMM.lacq, .035, .45, x, 1.1, z);
      hanokRoof(c, -1.3, 1.55, -.35, .8, .7, .45);
      for (const [x, m] of [[-.6, LMM.blue], [.6, MT.wheat], [1.0, LMM.lacq]]) { cy(c.body, MT.dwood, .02, .8, x, 1.1, -.62); bx(c.body, m, .02, .2, .3, x, 1.65, -.47); }
      lmFlag(c, -1.6, -1.6, 2.4);
    },
    gyeongbok(c) {   // Geunjeongjeon: the double-roofed throne hall on a two-tier stone platform inside its cloister
      const S = M.kstone, L = M.kstoneL;
      bx(c.body, L, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, S, 2.6, .25, 2.0, 0, 0, -.7); bx(c.body, S, 2.2, .25, 1.6, 0, .25, -.8); bx(c.body, L, 2.62, .05, .05, 0, .25, .3); bx(c.body, L, 2.22, .05, .05, 0, .5, 0);
      for (let i = 0; i < 3; i++) bx(c.body, L, .5, .17, .3 - i * .1, 0, i * .17, .45 - i * .05);
      bx(c.body, MT.lwood, 1.7, .6, 1.0, 0, .5, -.9); lmCols(c, 6, -.85, .85, -.34, .62, LMM.lacq, .05, .5); bx(c.body, M.dan, 1.85, .1, 1.15, 0, 1.02, -.9);
      py(c.roof, LMM.dtile, 2.5, .35, 1.75, 0, 1.12, -.9); bx(c.body, MT.lwood, 1.2, .45, .7, 0, 1.3, -.9); bx(c.body, M.dan, 1.25, .1, .75, 0, 1.65, -.9);
      hanokRoof(c, 0, 1.75, -.9, 1.85, 1.25, .85);
      for (const s of [-1, 1]) { bx(c.body, LMM.lacq, .32, .5, 2.8, s * 1.62, 0, -.3); lmGable(c, LMM.dtile, .55, .3, 2.9, s * 1.62, .5, -.3); }
      bx(c.body, LMM.lacq, .9, .55, .35, 0, 0, 1.5); bx(c.body, MT.black, .3, .45, .03, 0, 0, 1.68); hanokRoof(c, 0, .55, 1.5, 1.2, .6, .45);
      for (const s of [-1, 1]) { bx(c.body, MT.plaster, .8, .45, .18, s * 1.0, 0, 1.5); bx(c.roof, LMM.dtile, .85, .07, .28, s * 1.0, .45, 1.5); }
      for (let j = 0; j < 2; j++) for (const s of [-1, 1]) bx(c.body, L, .07, .14, .05, s * .45, 0, .75 + j * .35);
      for (const s of [-1, 1]) cy(c.body, MT.bronze, .09, .14, s * .95, .5, -.15);
      lmFlag(c, 1.2, 1.0, 1.9);
    },
    hwachaatolye(c) {   // the hwacha workshop: an open timber shed with a forge, hwacha carts lined up outside
      bx(c.body, M.yard, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, MT.plaster, 3.3, 1.0, .1, 0, 0, -1.72); for (const z of [-1.65, -.75]) lmCols(c, 5, -1.55, 1.55, z, 1.0, MT.dwood, .05);
      hanokRoof(c, 0, 1.0, -1.2, 3.55, 1.3, .6);
      bx(c.body, M.kstone, .6, .4, .5, -1.0, 0, -1.3); bx(c.body, MT.glow, .3, .18, .03, -1.0, .1, -1.04); cy(c.body, MT.brick, .1, 1.95, -1.15, 0, -1.45); c.chim.push(-1.15, 2.05, -1.45);
      for (let i = 0; i < 3; i++) cy(c.body, MT.lwood, .05, .9, .2 + i * .13, .06, -1.3).rotation.z = PI / 2;
      bx(c.body, MT.wood, .7, .06, .5, 1.0, .5, -1.2); for (let i = 0; i < 4; i++) cy(c.body, MT.dwood, .025, .5, .8 + i * .13, .56, -1.2);
      for (const [x, z] of [[-1.0, .55], [0, .75], [1.0, .55]]) {
        const g = grp(c, x, z);
        bx(g, MT.dwood, .55, .05, .05, 0, .2, 0); for (const s of [-1, 1]) { mk(G.wheel, g, MT.dwood, .05, .42, .42, s * .3, .21, 0); bx(g, MT.dwood, .04, .04, .65, s * .18, .2, -.45); }
        bx(g, MT.wood, .48, .06, .7, 0, .24, -.05);
        const r = new THREE.Group(); r.position.set(0, .3, .05); r.rotation.x = .85; g.add(r);
        bx(r, MT.lwood, .5, .42, .3, 0, 0, 0); bx(r, LMM.black, .44, .02, .25, 0, .42, 0);
        for (let i = 0; i < 4; i++) for (const k of [-1, 1]) cy(r, MT.iron, .012, .12, -.16 + i * .11, .44, k * .06);
      }
      for (let i = 0; i < 3; i++) cy(c.body, MT.lwood, .06, .6, -1.5, .06 + i * .1, 1.3 + (i % 2) * .05).rotation.x = PI / 2;
      lmFlag(c, 1.6, 1.5, 2.0);
    },
    kaplumbaga(c) {   // the turtle-ship yard: a geobukseon with a spiked shell and a smoking dragon head, a shed and timber
      bx(c.body, LMM.water, 3.8, .03, 2.4, 0, 0, .7); bx(c.body, M.kstone, 3.6, .3, 1.35, 0, 0, -1.2); bx(c.body, M.kstoneL, 3.6, .05, .1, 0, .3, -.55);
      bx(c.body, MT.plaster, 1.4, .75, .75, 1.0, .3, -1.4); hanokRoof(c, 1.0, 1.05, -1.4, 1.75, .95, .5);
      bx(c.body, MT.black, .4, .5, .03, 1.0, .3, -1.02);
      for (let i = 0; i < 4; i++) cy(c.body, MT.wood, .07, 1.0, -.65, .37 + (i % 2) * .12, -1.45 + (i >> 1) * .5 + (i % 2) * .12).rotation.z = PI / 2;
      cy(c.body, MT.dwood, .035, 1.7, -.4, .3, -.75).rotation.x = .35; bx(c.body, MT.dwood, .03, .6, .03, -.4, .95, -.05);
      const g = grp(c, -.1, .6, PI / 2);
      bx(g, M.hull, .78, .3, 2.4, 0, -.02, 0); bx(g, M.hull, .55, .15, .4, 0, .02, 1.3); bx(g, M.hull, .55, .2, .3, 0, .05, -1.32);
      bx(g, MT.wood, .82, .22, 2.25, 0, .28, 0);
      for (let i = 0; i < 5; i++) for (const s of [-1, 1]) bx(g, MT.black, .03, .07, .1, s * .41, .34, -.9 + i * .45);
      mk(G.dome, g, M.shell, .82, .8, 2.3, 0, .5, 0); bx(g, MT.dwood, .07, .05, 2.0, 0, .86, 0); bx(g, MT.dwood, .7, .05, .07, 0, .86, 0);
      for (let i = 0; i < 6; i++) for (const s of [-1, 1]) {
        const x = s * .22, z = -.9 + i * .36, hh = .4 * Math.sqrt(Math.max(0, 1 - (x / .41) ** 2 - (z / 1.15) ** 2));
        cn(g, MT.iron, .025, .1, x, .47 + hh, z);
      }
      bx(g, M.hull, .2, .26, .24, 0, .32, 1.15); bx(g, LMM.lacq, .22, .18, .3, 0, .5, 1.3); bx(g, MT.black, .16, .04, .08, 0, .54, 1.45);
      for (const s of [-1, 1]) { sp(g, MT.gold, .025, s * .08, .64, 1.36); cn(g, MT.gold, .02, .12, s * .06, .68, 1.24); }
      cy(g, MT.wood, .03, 1.15, 0, .8, -.4); bx(g, M.sailK, .75, .55, .02, 0, 1.25, -.4); for (let i = 0; i < 3; i++) bx(g, MT.dwood, .77, .02, .03, 0, 1.3 + i * .17, -.4);
      for (let i = 0; i < 4; i++) for (const s of [-1, 1]) { const o = bx(g, MT.dwood, .45, .03, .04, s * .6, .1, -.7 + i * .45); o.rotation.z = s * .35; }
      bx(g, M.hull, .05, .3, .15, 0, -.05, -1.45);
      c.chim.push(1.35, .58, .6);
      lmFlag(c, -1.65, -1.55, 2.2);
    },
    komutanlik(c) {   // Admiral Yi's headquarters: the command hall, a watchtower, cannons, the five-colour banners, his statue
      bx(c.body, M.yard, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, M.kstone, 2.4, .3, 1.35, -.4, 0, -1.15);
      hall(c, -.4, -1.2, 1.85, .85, .75, .3, .7, 5);
      for (const [x, z] of [[1.1, -.05], [1.6, -.05], [1.1, .45], [1.6, .45]]) cy(c.body, LMM.lacq, .045, 1.55, x, 0, z);
      bx(c.body, MT.lwood, .7, .06, .7, 1.35, .9, .2); bx(c.body, LMM.lacq, .7, .1, .03, 1.35, 1.05, .55); bx(c.body, M.dan, .66, .1, .66, 1.35, 1.45, .2);
      hanokRoof(c, 1.35, 1.55, .2, .95, .95, .55);
      cy(c.body, MT.dwood, .02, .3, 1.35, .96, .1); const d = mk(G.wheel, c.body, LMM.lacq, .16, .26, .26, 1.35, 1.32, .1); d.rotation.y = PI / 2;
      for (const x of [.5, 1.3]) { bx(c.body, MT.dwood, .3, .14, .55, x, 0, 1.3); const o = cy(c.body, MT.bronze, .08, .75, x, .22, .95); o.rotation.x = PI / 2 - .15; sp(c.body, MT.iron, .06, x + .25, .06, 1.6); }
      bx(c.body, M.kstone, .4, .5, .4, -.15, 0, .55); bx(c.body, MT.bronze, .22, .5, .16, -.15, .5, .55); sp(c.body, MT.bronze, .07, -.15, 1.08, .55); bx(c.body, MT.bronze, .04, .5, .04, -.02, .55, .66);
      [LMM.blue, LMM.lacq, MT.wheat, MT.white, LMM.black].forEach((m, i) => { const x = -1.7 + i * .28; cy(c.body, MT.dwood, .02, 1.5, x, 0, 1.5); bx(c.body, m, .02, .3, .3, x, 1.15, 1.65); });
      lmFlag(c, -1.65, .4, 2.6);
    },

    // ---- Malians ----
    nijerpazari(c) {   // a riverside market: straw-mat stalls, baskets and calabashes, pirogues on the Niger, a granary
      bx(c.body, LMM.water, 3.8, .03, 1.0, 0, 0, 1.4); bx(c.body, LMM.sand, 3.6, .05, 2.7, 0, 0, -.55);
      for (const [x, z, w] of [[-1.1, 1.35, 1.2], [.8, 1.55, 1.0]]) { bx(c.body, MT.dwood, w, .12, .24, x, .02, z); bx(c.body, MT.dwood, .1, .16, .14, x - w / 2, .04, z); bx(c.body, MT.dwood, .1, .16, .14, x + w / 2, .04, z); }
      lmGable(c, MT.thatch, .3, .2, .5, .8, .14, 1.55, PI / 2); cy(c.body, MT.dwood, .015, .9, -1.4, .1, 1.35).rotation.z = .4;
      for (const [x, z] of [[-1.0, .2], [.3, .3]]) {
        for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(c.body, MT.dwood, .025, .75, x + sx * .35, 0, z + sz * .28);
        bx(c.roof, MT.thatch, .85, .06, .7, x, .75, z);
      }
      for (const [x, z] of [[1.3, -.3], [-.35, -.6]]) { cy(c.body, MT.dwood, .03, .8, x, 0, z); cn(c.roof, MT.thatch, .5, .3, x, .75, z); }
      for (const [x, z, m] of [[-1.2, .25, M.ochre], [-.85, .1, M.indigo], [.2, .2, M.calab], [.45, .4, M.ochre], [1.2, -.15, M.indigo], [-.4, -.45, M.calab]]) cy(c.body, m, .12, .14, x, .05, z);
      for (const [x, z] of [[-.7, .35], [.15, .45], [1.45, -.1]]) sp(c.body, M.calab, .09, x, .14, z);
      bx(c.body, M.indigo, .3, .06, .2, .45, .05, .1); bx(c.body, M.ochre, .3, .06, .2, .45, .11, .1);
      cy(c.body, LMM.mud, .38, .8, -1.35, 0, -1.35); cn(c.roof, MT.thatch, .5, .55, -1.35, .8, -1.35);
      bx(c.body, LMM.mud, 1.1, .9, .8, 1.15, 0, -1.35); for (let i = 0; i < 4; i++) pinn(c, .75 + i * .27, .9, -.97); for (let i = 0; i < 3; i++) beamZ(c, .85 + i * .3, .6, -.95, .25);
      bx(c.body, MT.black, .25, .5, .03, 1.15, 0, -.94);
      lmFlag(c, .1, -1.45, 2.0);
    },
    atliavlusu(c) {   // the mansa's horse yard: a mud enclosure, a thatched stable row, horses in bright trappings
      const W = LMM.mud;
      bx(c.body, LMM.sandD, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, W, 3.6, .85, .25, 0, 0, -1.7); for (const s of [-1, 1]) { bx(c.body, W, .25, .85, 3.2, s * 1.68, 0, -.1); bx(c.body, W, 1.1, .85, .25, s * 1.2, 0, 1.45); }
      for (let i = 0; i < 6; i++) pinn(c, -1.5 + i * .6, .85, -1.7);
      for (let i = 0; i < 5; i++) beamZ(c, -1.2 + i * .6, .55, -1.7, .45);
      for (const s of [-1, 1]) { bx(c.body, M.mudL, .4, 1.3, .45, s * .5, 0, 1.45); pinn(c, s * .5, 1.3, 1.45, .14, .4); egg(c, s * .5, 1.75, 1.45); beamX(c, s * .5, .9, 1.45, .7); }
      lmCols(c, 5, -1.4, 1.4, -.95, .9, MT.dwood, .04); bx(c.roof, MT.thatch, 3.2, .08, .8, 0, .9, -1.3);
      horse(c, -.9, -1.25, 0, M.hBrown, M.indigo); horse(c, .1, -1.25, 0, M.hGrey, M.ochre);
      horse(c, -.5, .45, .9, M.hDark, c.cm); horse(c, .65, .2, -.6, M.hDun, LMM.lacq);
      bx(c.body, MT.dwood, .8, .2, .25, 1.0, 0, .95); bx(c.body, LMM.water, .72, .02, .18, 1.0, .19, .95);
      cn(c.body, MT.hay, .3, .35, -1.25, 0, .8);
      lmFlag(c, 1.45, -1.3, 1.9);
    },
    djinguereber(c) {   // the Djinguereber mosque: mud walls bristling with toron beams, buttress pinnacles, a stepped minaret
      const W = LMM.mud;
      bx(c.body, LMM.sand, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, W, 3.0, 1.0, 2.2, .25, 0, -.55);
      for (let i = 0; i < 6; i++) { const x = -.95 + i * .5; cy(c.body, W, .1, 1.15, x, 0, .62); pinn(c, x, 1.15, .62, .1, .3); }
      for (let i = 0; i < 6; i++) beamZ(c, -.7 + i * .5, .7, .6, .35);
      for (let i = 0; i < 5; i++) pinn(c, -.7 + i * .5, 1.0, .5, .07, .2);
      for (const z of [-1.4, -.85, -.3]) beamX(c, 1.75, .65, z, .3);
      bx(c.body, MT.dwood, .35, .6, .04, .3, 0, .56); bx(c.body, MT.dwood, .3, .5, .04, 1.3, 0, .56);
      mudTower(c, -1.35, .3, 1.0, 2.9);
      cy(c.body, W, .42, .5, 1.15, 1.0, -1.15); cn(c.body, W, .42, 1.1, 1.15, 1.5, -1.15); beamX(c, 1.15, 1.7, -1.15, 1.0); beamZ(c, 1.15, 1.95, -1.15, .8); egg(c, 1.15, 2.66, -1.15);
      cn(c.body, M.mudL, .3, .75, 1.5, 1.0, .25); egg(c, 1.5, 1.8, .25);
      lmFlag(c, 1.6, 1.4, 1.7);
    },
    nianikale(c) {   // the Niani fortress: thick mud walls, round buttress towers, a gate with spears, the tall tata keep
      const W = M.mudD, T = LMM.mud;
      for (const s of [-1, 1]) { bx(c.body, W, .4, 1.15, 3.2, s * 1.5, 0, 0); bx(c.body, W, 1.1, 1.15, .4, s * 1.05, 0, 1.5); }
      bx(c.body, W, 3.2, 1.15, .4, 0, 0, -1.5);
      for (let i = 0; i < 4; i++) { pinn(c, -1.05 + i * .7, 1.15, -1.5, .1, .26); pinn(c, -1.5, 1.15, -1.05 + i * .7, .1, .26); pinn(c, 1.5, 1.15, -1.05 + i * .7, .1, .26); }
      for (const [x, z] of [[-1.5, -1.5], [1.5, -1.5], [-1.5, 1.5], [1.5, 1.5]]) { cy(c.body, T, .38, 1.7, x, 0, z); cn(c.body, T, .4, .55, x, 1.7, z); beamX(c, x, 1.2, z, 1.0); beamZ(c, x, 1.3, z, 1.0); }
      bx(c.body, M.mudL, 1.0, 1.65, .55, 0, 0, 1.5); bx(c.body, MT.black, .45, .85, .05, 0, 0, 1.78); bx(c.body, MT.dwood, .5, .06, .06, 0, .85, 1.8);
      for (const s of [-1, 1]) { pinn(c, s * .35, 1.65, 1.5, .12, .35); beamZ(c, s * .3, 1.2, 1.5, .8); }
      for (let i = 0; i < 4; i++) { const x = .62 + i * .1; cy(c.body, MT.dwood, .015, 1.0, x, 0, 1.85); cn(c.body, MT.steel, .03, .12, x, 1.0, 1.85); }
      bx(c.body, LMM.mud, .85, 2.3, .85, 0, 0, -.45); for (const [x, z] of [[-.35, -.8], [.35, -.8], [-.35, -.1], [.35, -.1]]) pinn(c, x, 2.3, z, .1, .35);
      beamX(c, 0, 1.5, -.45, 1.2); beamZ(c, 0, 1.75, -.45, 1.2); egg(c, 0, 2.5, -.45); bx(c.body, MT.black, .2, .25, .03, 0, 1.6, -.02);
      bx(c.body, M.ochre, .3, .5, .04, -.85, .45, 1.73); bx(c.body, M.indigo, .3, .5, .04, .85, .45, 1.73);
      lmFlag(c, 0, -.45, 3.2);
    },
    sankore(c) {   // the Sankore madrasa: a walled court, the stepped pyramid tower, classrooms, students round a teacher
      const W = LMM.mud;
      bx(c.body, LMM.sand, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, W, 3.4, .9, .7, 0, 0, -1.45); for (let i = 0; i < 5; i++) bx(c.body, MT.black, .22, .45, .03, -1.3 + i * .65, 0, -1.09);
      bx(c.body, W, .7, .9, 2.4, -1.45, 0, .1); for (let i = 0; i < 3; i++) bx(c.body, MT.black, .03, .45, .22, -1.09, 0, -.6 + i * .6);
      for (let i = 0; i < 6; i++) pinn(c, -1.5 + i * .6, .9, -1.12, .07, .2);
      bx(c.body, W, 1.9, .55, .2, .6, 0, 1.6); bx(c.body, W, .2, .55, 2.6, 1.6, 0, .2);
      const top = lmSteps(c, M.mudL, 1.3, 1.3, 5, .3, .45, -.35);
      cn(c.body, M.mudL, .14, .35, .45, top, -.35); egg(c, .45, top + .42, -.35);
      for (const y of [.45, 1.05]) { beamX(c, .45, y, -.35 + .2, 1.6 - y * .4); beamZ(c, .45 + .2, y + .05, -.35, 1.6 - y * .4); }
      cy(c.body, LMM.bark, .08, .9, -.55, 0, 1.0); sp(c.body, MT.dgreen, .45, -.55, 1.2, 1.0);
      bx(c.body, M.ochre, .9, .02, .7, -.55, 0, 1.0);
      for (const [x, z] of [[-.85, .8], [-.25, .8], [-.85, 1.25], [-.25, 1.25]]) { bx(c.body, MT.white, .14, .16, .14, x, .02, z); sp(c.body, MT.skin, .04, x, .22, z); }
      bx(c.body, M.indigo, .16, .3, .14, -.55, .02, .6); sp(c.body, MT.skin, .045, -.55, .37, .6);
      for (let i = 0; i < 3; i++) for (let j = 0; j < 3 - i; j++) bx(c.body, j & 1 ? MT.leather : M.ochre, .2, .06, .14, .9 + i * .25, j * .06, .8);
      lmFlag(c, 1.3, -.6, 1.9);
    },
    altinmadeni(c) {   // the Bambuk gold fields: pits with windlasses, gold heaps, a washing basin, miners' huts, a smelting fire
      bx(c.body, M.laterite, 3.6, .04, 3.6, 0, 0, 0);
      for (const [x, z] of [[-1.1, -.9], [.2, -1.2], [1.25, -.4], [-.4, .3]]) {
        cy(c.body, MT.soil2, .42, .14, x, 0, z); cy(c.body, MT.black, .26, .15, x, 0, z);
        for (const s of [-1, 1]) cy(c.body, MT.dwood, .03, .65, x + s * .34, 0, z); const b = cy(c.body, MT.wood, .035, .74, x - .37, .6, z); b.rotation.z = -PI / 2;
        cy(c.body, M.rope, .01, .45, x, .15, z);
      }
      for (const [x, z, r] of [[.6, .5, .3], [1.05, .85, .22], [.15, 1.0, .2]]) cn(c.body, LMM.goldm, r, r * 1.05, x, .04, z);
      bx(c.body, M.mudL, .95, .1, .6, -1.15, 0, .85); bx(c.body, LMM.water, .82, .02, .48, -1.15, .1, .85);
      for (const [x, z] of [[-1.35, .8], [-.95, .95]]) sp(c.body, M.calab, .08, x, .12, z);
      for (let i = 0; i < 3; i++) { cy(c.body, M.ochre, .1, .12, .55 + i * .22, .04, 1.4); sp(c.body, LMM.goldm, .07, .55 + i * .22, .17, 1.4); }
      hut(c, -1.45, -1.5, .32, .55); hut(c, 1.45, -1.45, .32, .55);
      bx(c.body, MT.stone, .35, .22, .35, 1.45, 0, .55); bx(c.body, MT.glow, .2, .05, .2, 1.45, .22, .55); c.chim.push(1.45, .35, .55);
      lmFlag(c, -1.6, 1.5, 1.9);
    },
    mansasaray(c) {   // Mansa Musa's palace: a great mud hall, a gilded domed audience chamber, the royal parasol with its golden bird
      const W = M.mudL;
      bx(c.body, LMM.sand, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, W, 2.8, 1.35, 1.6, 0, 0, -.85);
      for (let i = 0; i < 6; i++) { const x = -1.25 + i * .5; cy(c.body, W, .09, 1.5, x, 0, -.02); pinn(c, x, 1.5, -.02, .09, .3, LMM.mud); }
      for (let i = 0; i < 5; i++) beamZ(c, -1.0 + i * .5, 1.0, -.05, .35);
      bx(c.body, W, 1.0, .75, .9, -.8, 1.35, -1.0); for (const [x, z] of [[-1.2, -1.35], [-.4, -1.35], [-1.2, -.65], [-.4, -.65]]) pinn(c, x, 2.1, z, .09, .3, LMM.mud);
      beamZ(c, -.8, 1.75, -.55, .3);
      cy(c.body, W, .55, .35, .75, 1.35, -1.0); bx(c.body, MT.gold, 1.12, .05, 1.12, .75, 1.68, -1.0); lmDome(c, LMM.goldm, .56, .75, 1.7, -1.0, .9); sp(c.roof, MT.gold, .06, .75, 2.27, -1.0);
      bx(c.body, LMM.mud, 1.0, 1.75, .45, 0, 0, .05); bx(c.body, MT.dwood, .45, .85, .04, 0, 0, .29); bx(c.body, LMM.goldm, .35, .06, .02, 0, .7, .3);
      for (const s of [-1, 1]) pinn(c, s * .35, 1.75, .05, .12, .35, LMM.mud); egg(c, 0, 1.85, .05); beamX(c, 0, 1.35, .1, 1.3);
      cy(c.body, MT.dwood, .03, 1.35, 1.15, 0, 1.0); mk(G.dome, c.roof, LMM.goldm, .9, .3, .9, 1.15, 1.25, 1.0); sp(c.roof, MT.gold, .06, 1.15, 1.42, 1.0);
      bx(c.body, LMM.goldm, .3, .35, .25, 1.15, 0, .95); bx(c.body, LMM.lacq, .26, .05, .2, 1.15, .35, .95);
      for (let i = 0; i < 3; i++) bx(c.body, LMM.goldm, .22, .07, .1, -.9 + (i % 2) * .1, i * .07, 1.0);
      for (const x of [-.6, .6]) { bx(c.body, MT.white, .14, .35, .12, x, 0, .55); sp(c.body, MT.skin, .05, x, .41, .55); cy(c.body, MT.dwood, .012, .75, x + .1, 0, .6); cn(c.body, MT.gold, .025, .1, x + .1, .75, .6); }
      lmFlag(c, -1.55, 1.3, 2.0);
    },
    timbuktukale(c) {   // a desert caravan fort: mud walls with corner buttresses, a gate tower, camels with salt slabs
      const W = LMM.mud;
      bx(c.body, LMM.sand, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, W, 3.0, 1.0, .3, 0, 0, -1.35); for (const s of [-1, 1]) { bx(c.body, W, .3, 1.0, 2.9, s * 1.35, 0, 0); bx(c.body, W, .95, 1.0, .3, s * .92, 0, 1.3); }
      for (const [x, z] of [[-1.35, -1.35], [1.35, -1.35], [-1.35, 1.3], [1.35, 1.3]]) { cn(c.body, M.mudL, .3, 1.55, x, 0, z); egg(c, x, 1.6, z); }
      for (let i = 0; i < 4; i++) { beamZ(c, -.9 + i * .6, .65, -1.35, .45); beamX(c, -1.35, .65, -.9 + i * .6, .45); beamX(c, 1.35, .65, -.9 + i * .6, .45); }
      mudTower(c, 0, 1.35, .7, 2.1, M.mudL); bx(c.body, MT.black, .3, .6, .04, 0, 0, 1.71);
      camel(c, -.6, -.5, .4, M.salt); camel(c, .55, -.2, -.9, M.salt); camel(c, 1.0, 1.75, PI / 2, M.indigo);
      for (let i = 0; i < 4; i++) bx(c.body, M.salt, .4, .06, .22, -.9, i * .06, .5);
      for (const [x, m] of [[.5, M.indigo], [.85, M.ochre]]) bx(c.body, m, .3, .25, .3, x, 0, .7);
      for (let i = 0; i < 3; i++) { const x = -.75 + i * .1; cy(c.body, MT.dwood, .015, 1.0, x, 0, 1.55); cn(c.body, MT.steel, .03, .12, x, 1.0, 1.55); }
      lmFlag(c, 0, 1.35, 2.9);
    },

    // ---- Mongols ----
    surutlagi(c) {   // a steppe pasture: a timber sheep pen full of sheep, herders' gers, a tethered horse, a dung-fuel heap
      bx(c.body, LMM.turf, 3.6, .04, 3.6, 0, 0, 0);
      const x0 = -.55, x1 = 1.7, z0 = -.5, z1 = 1.55;
      for (const y of [.22, .42]) { bx(c.body, MT.dwood, x1 - x0, .04, .04, (x0 + x1) / 2, y, z0); bx(c.body, MT.dwood, .04, .04, z1 - z0, x0, y, (z0 + z1) / 2); bx(c.body, MT.dwood, .04, .04, z1 - z0, x1, y, (z0 + z1) / 2); bx(c.body, MT.dwood, 1.3, .04, .04, x1 - .65, y, z1); }
      for (const [x, z] of [[x0, z0], [x1, z0], [x0, z1], [x1, z1], [.55, z0], [x0, .5], [x1, .5], [1.05, z1], [.4, z1]]) cy(c.body, MT.wood, .035, .55, x, 0, z);
      [[-.2, -.15, .5], [.2, .1, 2], [.6, -.2, 1], [1.0, .05, 4], [1.35, -.2, 3], [.0, .55, 5], [.45, .6, 1.2], [.9, .55, 2.5], [1.35, .8, .3], [.3, 1.1, 4.4], [.85, 1.15, 1.7], [1.35, 1.25, 5.5]]
        .forEach(([x, z, a], i) => sheep(c, x, z, a, i % 5 === 3 ? M.hBrown : M.wool));
      ger(c, -1.2, -1.15, .55, .55, .3); ger(c, .1, -1.45, .38, .42, 0);
      c.chim.push(-1.2, .85, -1.15);
      cy(c.body, MT.dwood, .03, .7, -1.25, 0, .55); horse(c, -1.4, .95, .3, M.hDun);
      cn(c.body, MT.soil2, .3, .35, -1.4, 0, -.1);
      lmFlag(c, -.8, 1.55, 1.8);
    },
    atliokcu(c) {   // the mounted-archery ground: a riding track, straw targets on stands, two horse archers at the gallop, a judges' awning
      bx(c.body, LMM.turf, 3.6, .04, 3.6, 0, 0, 0); bx(c.body, MT.soil2, 3.6, .02, .8, 0, .04, .55);
      for (const x of [-1.2, 0, 1.2]) {
        for (const s of [-1, 1]) bx(c.body, MT.dwood, .04, .55, .04, x + s * .14, 0, -.2);
        mk(G.wheel, c.body, MT.hay, .07, .46, .46, x, .55, -.2).rotation.y = PI / 2; mk(G.wheel, c.body, LMM.lacq, .08, .16, .16, x, .55, -.2).rotation.y = PI / 2;
      }
      for (const [x, ry] of [[-.7, PI / 2], [.9, PI / 2]]) {
        const g = horse(c, x, .6, ry, x < 0 ? M.hBrown : M.hDark, c.cm, LMM.blue);
        mk(G.bow, g, MT.dwood, 1, 1, 1, -.12, .6, .0);
      }
      ger(c, -1.3, -1.3, .5, .5, .4);
      for (const [x, z] of [[.6, -1.6], [1.6, -1.6], [.6, -.9], [1.6, -.9]]) cy(c.body, MT.dwood, .03, .8, x, 0, z);
      bx(c.roof, MT.canvas, 1.2, .05, .9, 1.1, .8, -1.25); bx(c.body, c.cm, 1.2, .1, .02, 1.1, .7, -.8);
      bx(c.body, MT.lwood, .8, .25, .3, 1.1, 0, -1.3);
      tug(c, -1.65, 1.5, 2.0, LMM.black);
      for (let i = 0; i < 4; i++) cy(c.body, MT.lwood, .012, .55, -1.5 + i * .05, 0, -.4);
      for (const x of [-1.7, 1.7]) { cy(c.body, MT.dwood, .015, .5, x, 0, 1.0); bx(c.body, LMM.lacq, .02, .1, .15, x, .38, 1.08); }
      lmFlag(c, 1.6, 1.5, 1.9);
    },
    karakurum(c) {   // the Karakorum bazaar: the Silver Tree fountain, a stone turtle bearing a stele, merchants' awnings
      bx(c.body, MT.stone, 3.6, .04, 3.6, 0, 0, 0);
      cy(c.body, M.kstone, .6, .2, 0, 0, -.5); cy(c.body, LMM.water, .52, .02, 0, .2, -.5);
      cy(c.body, M.silver, .07, 1.6, 0, .2, -.5);
      for (let i = 0; i < 4; i++) { const a = i * PI / 2 + .4, b = bx(c.body, M.silver, .04, .5, .04, Math.cos(a) * .12, 1.2, -.5 + Math.sin(a) * .12); b.rotation.z = -Math.cos(a) * .7; b.rotation.x = Math.sin(a) * .7; sp(c.body, M.silver, .09, Math.cos(a) * .42, 1.6, -.5 + Math.sin(a) * .42); cy(c.body, MT.gold, .025, .2, Math.cos(a) * .4, .2, -.5 + Math.sin(a) * .4); }
      sp(c.body, M.silver, .16, 0, 1.85, -.5); bx(c.body, MT.gold, .08, .2, .06, 0, 2.0, -.5); sp(c.body, MT.gold, .04, 0, 2.24, -.5); const t = cy(c.body, MT.gold, .02, .25, .03, 2.15, -.5); t.rotation.z = -1;
      const T = MT.dstone;
      bx(c.body, T, .9, .12, .7, -1.2, 0, .9); lmDome(c, T, .4, -1.2, .12, .9, .55); bx(c.body, T, .16, .14, .25, -1.2, .1, 1.35); for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(c.body, T, .12, .1, .14, -1.2 + sx * .3, .05, .9 + sz * .28);
      bx(c.body, M.kstoneL, .35, .9, .1, -1.2, .3, .85); bx(c.body, M.kstoneL, .42, .12, .14, -1.2, 1.2, .85);
      for (const [x, z, m] of [[1.1, .8, LMM.lacq], [1.1, -1.25, LMM.blue], [-1.2, -1.3, MT.canvas]]) {
        lmGable(c, m, .9, .35, 1.1, x, .75, z, PI / 2); for (const sx of [-1, 1]) for (const sz of [-1, 1]) cy(c.body, MT.dwood, .025, .75, x + sx * .48, 0, z + sz * .38);
        bx(c.body, MT.wood, .9, .3, .4, x, 0, z);
      }
      bx(c.body, LMM.lacq, .3, .1, .3, 1.0, .3, .8); bx(c.body, MT.wheat, .3, .1, .3, 1.2, .3, .85); sp(c.body, LMM.blue, .08, 1.2, .38, -1.25); sp(c.body, MT.white, .08, .95, .38, -1.2);
      bx(c.body, LMM.redb, .6, .02, .45, .3, .04, .9);
      camel(c, .4, 1.5, -PI / 2, M.indigo);
      lmFlag(c, -1.65, -.3, 2.0);
    },
    kurultay(c) {   // the kurultai: a great white council pavilion with a porch, the nine white standards, lesser gers
      bx(c.body, LMM.turf, 3.6, .04, 3.6, 0, 0, 0);
      cy(c.body, M.felt, 1.05, 1.0, 0, 0, -.6); lmDome(c, M.felt, 1.08, 0, 1.0, -.6, .55);
      cy(c.body, LMM.blue, 1.065, .12, 0, .8, -.6); cy(c.body, M.rope, 1.06, .04, 0, .45, -.6); cy(c.roof, LMM.blue, .45, .08, 0, 1.52, -.6); cy(c.roof, MT.dwood, .2, .1, 0, 1.58, -.6); sp(c.roof, MT.gold, .07, 0, 1.75, -.6);
      for (const s of [-1, 1]) cy(c.body, MT.dwood, .03, .95, s * .4, 0, .8); bx(c.roof, LMM.blue, 1.0, .05, .6, 0, .95, .55); bx(c.body, c.cm, 1.0, .12, .02, 0, .85, .85); bx(c.body, M.door, .45, .85, .05, 0, 0, .46);
      for (let i = 0; i < 9; i++) { const a = PI * (.12 + i * .095), x = -Math.cos(a) * 1.55, z = .35 + Math.sin(a) * 1.15; tug(c, x, z, 1.6 + (i === 4 ? .5 : 0)); }
      ger(c, -1.45, -1.45, .38, .42, .5); ger(c, 1.45, -1.45, .38, .42, -.5);
      c.chim.push(0, 1.75, -.6);
      lmFlag(c, 1.6, -.4, 2.2);
    },
    yamistasyon(c) {   // a yam relay station: the keeper's ger, a hitching rail with fresh horses, a rider galloping off, a store and trough
      bx(c.body, LMM.turf, 3.6, .04, 3.6, 0, 0, 0); bx(c.body, MT.soil2, .7, .02, 3.6, .8, .04, 0);
      ger(c, -1.05, -1.0, .65, .6, .4); c.chim.push(-1.05, .95, -1.0);
      bx(c.body, MT.wood, 1.0, .7, .7, 1.25, 0, -1.35); lmGable(c, MT.dwood, .9, .3, 1.15, 1.25, .7, -1.35, PI / 2); bx(c.body, MT.black, .3, .45, .03, 1.25, 0, -.99);
      for (const x of [-1.5, -.3]) cy(c.body, MT.dwood, .035, .6, x, 0, .55); bx(c.body, MT.dwood, 1.35, .05, .05, -.9, .55, .55);
      for (const [x, m] of [[-1.35, M.hBrown], [-.9, M.hGrey], [-.45, M.hDun]]) horse(c, x, .85, PI, m, LMM.lacq);
      horse(c, .85, .6, 0, M.hDark, c.cm, M.door);
      bx(c.body, MT.dwood, .7, .18, .22, -.4, 0, -.1); bx(c.body, LMM.water, .62, .02, .15, -.4, .17, -.1);
      cy(c.body, MT.dwood, .03, 1.3, .3, 0, -.5); bx(c.body, MT.dwood, .3, .04, .04, .4, 1.2, -.5); cn(c.body, MT.bronze, .07, .14, .5, 1.04, -.5);
      cn(c.body, MT.hay, .3, .35, 1.5, 0, .3); cn(c.body, MT.hay, .25, .3, 1.55, 0, .85);
      bx(c.body, LMM.goldm, .08, .12, .02, .85, .55, .63);
      lmFlag(c, -1.6, 1.5, 1.9);
    },
    kusatmakamp(c) {   // the siege engineers' camp: a counterweight trebuchet, a traction trebuchet, stone shot, timber and a forge
      bx(c.body, MT.soil2, 3.6, .04, 3.6, 0, 0, 0);
      const g = grp(c, -.55, -.3, .25), W = MT.wood;
      for (const s of [-1, 1]) { bx(g, MT.dwood, .1, .1, 1.6, s * .35, 0, 0); for (const k of [-1, 1]) { const o = bx(g, W, .08, 1.6, .08, s * .35, .05, k * .45); o.rotation.x = -k * .28; } }
      bx(g, MT.dwood, .8, .06, .06, 0, 1.55, 0);
      const arm = new THREE.Group(); arm.position.set(0, 1.58, 0); arm.rotation.x = -.55; g.add(arm);
      bx(arm, W, .07, .07, 2.3, 0, -.035, -.45); bx(arm, MT.dwood, .45, .45, .4, 0, -.5, .6); cy(arm, M.rope, .01, .5, 0, -.5, -1.58);
      for (let i = 0; i < 3; i++) bx(g, MT.stone, .3, .05, .3, 0, .1 + i * .05, .6);
      const t = grp(c, 1.05, .2, -.4);
      for (const k of [-1, 1]) { const o = bx(t, W, .07, 1.1, .07, k * .25, 0, 0); o.rotation.z = k * .15; }
      bx(t, MT.dwood, .6, .05, .05, 0, 1.05, 0); const a2 = bx(t, W, .05, .05, 1.5, 0, 1.08, -.2); a2.rotation.x = .3;
      for (let i = 0; i < 6; i++) cy(t, M.rope, .006, .7, -.1 + i * .04, .45, .45);
      for (const [x, z] of [[.1, 1.1], [.3, 1.25], [.2, 1.45], [.45, 1.0], [.55, 1.35], [.33, 1.15]]) sp(c.body, MT.stone, .11, x, .15 + (x === .33 ? .15 : 0), z);
      for (let i = 0; i < 4; i++) cy(c.body, MT.wood, .07, 1.2, -.4, .07 + (i % 2) * .12, 1.1 + (i >> 1) * .2 + (i % 2) * .1).rotation.z = PI / 2;
      lmGable(c, MT.canvas, 1.0, .75, 1.2, 1.25, 0, -1.3); bx(c.body, c.cm, .05, .15, 1.22, 1.25, .7, -1.3);
      bx(c.body, MT.stone, .45, .3, .4, -1.45, 0, -1.4); bx(c.body, MT.glow, .25, .08, .25, -1.45, .3, -1.4); c.chim.push(-1.45, .45, -1.4);
      bx(c.body, MT.dwood, .4, .15, .25, -1.45, 0, -.85); bx(c.body, MT.iron, .25, .1, .12, -1.45, .15, -.85);
      lmFlag(c, 1.6, 1.5, 2.0);
    },
    altincadir(c) {   // the Golden Horde: the khan's huge golden ger on a lacquered dais, a gilded porch, white gers beside it
      bx(c.body, LMM.turf, 3.6, .04, 3.6, 0, 0, 0);
      const top = lmSteps(c, LMM.lacq, 3.0, 3.0, 3, .12, 0, -.35, .25);
      bx(c.body, MT.gold, 2.52, .03, 2.52, 0, top - .02, -.35);
      cy(c.body, LMM.goldm, 1.0, 1.0, 0, top, -.45); lmDome(c, LMM.goldm, 1.03, 0, top + 1.0, -.45, .5);
      cy(c.body, LMM.lacq, 1.012, .1, 0, top + .55, -.45); cy(c.body, LMM.blue, 1.012, .06, 0, top + .88, -.45);
      cy(c.roof, LMM.lacq, .32, .08, 0, top + 1.5, -.45); cy(c.roof, LMM.goldm, .14, .25, 0, top + 1.58, -.45); sp(c.roof, MT.gold, .08, 0, top + 1.9, -.45);
      bx(c.body, LMM.lacq, .5, .85, .05, 0, top, .56); bx(c.body, MT.gold, .58, .06, .06, 0, top + .85, .56);
      for (const s of [-1, 1]) cy(c.body, LMM.goldm, .04, .9, s * .4, top, .85); bx(c.roof, LMM.goldm, 1.0, .06, .55, 0, top + .9, .7); bx(c.body, c.cm, 1.0, .12, .02, 0, top + .78, .98);
      ger(c, -1.45, 1.5, .38, .42, .3); ger(c, 1.45, 1.5, .38, .42, -.3);
      for (const [x, z] of [[-.9, 1.45], [.9, 1.45]]) { bx(c.body, MT.dwood, .3, .2, .22, x, 0, z); bx(c.body, LMM.goldm, .3, .06, .22, x, .2, z); }
      tug(c, -1.6, -1.6, 2.2);
      lmFlag(c, 1.6, -1.6, 2.2);
    },
    kesikordugah(c) {   // the keshig guard camp: dark felt gers round the black war standard, spear racks, armoured horses, a war drum
      bx(c.body, MT.soil2, 3.6, .04, 3.6, 0, 0, 0);
      for (const [x, z, ry] of [[-1.3, -1.3, .8], [1.3, -1.3, -.8], [-1.35, .4, PI / 2 + .3], [1.35, .4, -PI / 2 - .3]]) ger(c, x, z, .45, .45, ry, M.feltD, M.feltD, LMM.lacq);
      cy(c.body, MT.dstone, .25, .12, 0, 0, -.3); cy(c.body, MT.dwood, .035, 2.6, 0, .12, -.3);
      for (let i = 0; i < 4; i++) sp(c.body, LMM.black, .11, Math.cos(i * PI / 2) * .1, 2.25, -.3 + Math.sin(i * PI / 2) * .1);
      cn(c.roof, MT.steel, .05, .3, 0, 2.7, -.3); for (const s of [-1, 1]) cn(c.roof, MT.steel, .025, .18, s * .09, 2.6, -.3);
      for (const z of [.0, 1.0]) {
        bx(c.body, MT.dwood, .05, .05, .7, -.55 + z * .2, .5, z - .3);
        for (let i = 0; i < 4; i++) { const zz = z - .55 + i * .17; cy(c.body, MT.dwood, .014, 1.1, -.55 + z * .2, 0, zz); cn(c.body, MT.steel, .028, .14, -.55 + z * .2, 1.1, zz); }
      }
      for (const [x, m] of [[.3, M.hDark], [.75, M.hBrown], [1.2, M.hDark]]) horse(c, x, 1.3, PI, m, MT.iron);
      bx(c.body, MT.dwood, 1.3, .05, .05, .75, .5, .95); for (const x of [.15, 1.35]) cy(c.body, MT.dwood, .03, .55, x, 0, .95);
      cy(c.body, MT.bronze, .22, .3, -1.2, 0, 1.4); cy(c.body, MT.leather, .23, .03, -1.2, .3, 1.4); cn(c.body, MT.dwood, .02, .2, -1.1, .33, 1.4).rotation.z = .9;
      lmFlag(c, .5, -1.4, 2.2);
    },
  };
}
