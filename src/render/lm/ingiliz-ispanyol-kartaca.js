// Age-up building models (landmarks.js looks) of the English, the Spanish and the Carthaginians. See index.js.
export default function (K) {
  const { THREE, PI, G, MT, XM, LMM, mat, mk, bx, cy, cn, py, sp, lmFlag, lmDome, lmGable, lmMinaret, lmCols, lmCren, lmTower, lmWall, lmPagoda, lmSteps, lmArch, lmShip } = K;
  const M = {
    half: mat(0xf0e6cc, .9), otile: mat(0x7e4a3a, .85), slate: mat(0x4a4f58, .7), white: mat(0xe2dccb, .85), rag: mat(0xa8a090, .95),
    abbey: mat(0xcfc3a6, .88), goth: mat(0xc9b37c, .88), brick: mat(0x9c4636, .88), port: mat(0xe2dccb, .85), gravel: mat(0x8e877a, 1),
    granite: mat(0x9e9b92, .92), ochre: mat(0xc9a46e, .92), oro: mat(0xd8b56a, .85), oroL: mat(0xe6c98a, .85), whitew: mat(0xf3eee2, .9),
    terra: mat(0xb8562e, .8), olive: mat(0x7e8a58, .95), oliveD: mat(0x66724a, .95), dry: mat(0xb89a68, 1), santi: mat(0xb9a785, .9),
    stile: mat(0x8f8a80, .8), mbrick: mat(0xb0664a, .88), glaze: mat(0x3f7a6a, .5), rock: mat(0x8a8478, .95),
    punic: mat(0xd8c08e, .9), punW: mat(0xefe7d2, .9), purple: mat(0x6a2470, .65), purpleL: mat(0x8e3a94, .7), murex: mat(0xdcc6b2, .8),
    eleph: mat(0x8c8782, .95), snow: mat(0xf4f6fa, .7), dhide: mat(0x4a3a2a, .95), dial: mat(0xf2ead0, .5, 0, 0x221a08), yew: mat(0xa0703a, .8),
  };
  const D12 = new THREE.CylinderGeometry(.5, .5, 1, 12);   // (centred: placed at y + h / 2)

  // a galleon: hull along local +z (the bow), castles fore and aft, three masts; bare = fitting out, no sails
  function galleon(c, x, z, ry, L, sail, cross, bare) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; c.body.add(g);
    bx(g, MT.dwood, .44, .2, L * .66, 0, -.05, 0); bx(g, MT.dwood, .62, .32, L * .78, 0, .1, -L * .02);
    bx(g, mat(0xc8a040, .6), .64, .05, L * .78, 0, .34, -L * .02); bx(g, c.cm, .64, .05, L * .78, 0, .24, -L * .02);
    bx(g, MT.wood, .6, .45, L * .24, 0, .42, -L * .3); bx(g, MT.wood, .5, .25, L * .12, 0, .87, -L * .36); bx(g, MT.glow, .4, .1, .02, 0, .62, -L * .42 - .01);
    bx(g, MT.wood, .5, .25, L * .16, 0, .42, L * .28); bx(g, MT.dwood, .36, .28, .3, 0, .14, L * .42); bx(g, MT.dwood, .16, .12, .3, 0, .32, L * .52);
    const b = cy(g, MT.wood, .025, .9, 0, .45, L * .45); b.rotation.x = 1.15;
    for (const s of [-1, 1]) for (let i = 0; i < 5; i++) bx(g, MT.black, .02, .07, .09, s * .315, .17, -L * .2 + i * L * .1);
    for (const [mz, h] of [[L * .22, 1.9], [0, 2.4], [-L * .24, 1.7]]) {
      cy(g, MT.wood, .035, h, 0, .4, mz);
      if (bare) { bx(g, MT.wood, .8, .04, .04, 0, 1.3, mz); continue; }
      if (mz < 0) { bx(g, sail, .03, .55, .5, 0, 1.05, mz); continue; }
      bx(g, sail, .8, .52, .03, 0, .95, mz); bx(g, sail, .6, .4, .03, 0, 1.6, mz);
      if (cross) for (const a of [-.58, .58]) mk(G.cbox, g, cross, .8, .07, .035, 0, 1.21, mz + .01).rotation.z = a;
    }
    bx(g, c.cm, .02, .12, .45, 0, 2.62, -.22);
    return g;
  }
  // an elephant facing local +z; war = a saddle cloth in the player's colour and a howdah
  function elephant(c, x, z, ry, s, war) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; g.scale.setScalar(s); c.body.add(g);
    const E = M.eleph;
    mk(G.sph, g, E, .62, .58, 1.0, 0, .78, 0);
    for (const sx of [-.17, .17]) for (const sz of [-.28, .28]) cy(g, E, .1, .6, sx, 0, sz);
    mk(G.sph, g, E, .42, .44, .4, 0, .95, .52);
    for (const k of [-1, 1]) bx(g, E, .04, .34, .3, k * .22, .76, .46).rotation.y = k * .4;
    cy(g, E, .06, .5, 0, .32, .7);
    for (const k of [-1, 1]) cn(g, XM.bone, .03, .28, k * .09, .72, .66).rotation.x = 1.9;
    bx(g, E, .03, .35, .03, 0, .5, -.5);
    if (war) { bx(g, c.cm, .66, .35, .5, 0, .72, -.08); bx(g, MT.wood, .42, .25, .4, 0, 1.04, -.08); bx(g, MT.gold, .44, .04, .42, 0, 1.29, -.08); }
    return g;
  }
  // a palm: a trunk and five fronds
  const palm = (c, x, z, h) => { cy(c.body, LMM.bark, .06, h, x, 0, z); for (let i = 0; i < 5; i++) bx(c.roof, LMM.pine, .7, .04, .15, x + Math.cos(i * 1.25) * .3, h, z + Math.sin(i * 1.25) * .3).rotation.y = -i * 1.25; };

  return {
    // ---- İngilizler ----
    manor(c) {   // a Tudor manor: a half-timbered hall with a jettied upper floor, two gabled wings, tall brick chimneys, a wheat field
      const P = M.half, T = MT.dwood;
      bx(c.body, P, 2.4, .9, 1.0, 0, 0, -.9); bx(c.body, P, 2.5, .75, 1.15, 0, .9, -.9); bx(c.body, T, 2.52, .06, 1.17, 0, .88, -.9);
      for (let i = 0; i < 9; i++) bx(c.body, T, .05, .75, .02, -1.2 + i * .3, .9, -.32);
      for (let i = 0; i < 7; i++) bx(c.body, T, .05, .9, .02, -1.1 + i * .37, 0, -.39);
      for (const x of [-.75, -.45, .45, .75]) bx(c.body, MT.glass, .18, .28, .02, x, 1.15, -.31);
      lmGable(c, M.otile, 1.35, .8, 2.7, 0, 1.65, -.9, PI / 2);
      for (const s of [-1, 1]) {
        const x = s * 1.25;
        bx(c.body, P, .75, 1.65, .9, x, 0, -.15); lmGable(c, M.otile, .85, .65, 1.0, x, 1.65, -.15);
        for (const dx of [-.3, .3]) bx(c.body, T, .05, 1.65, .02, x + dx, 0, .31);
        bx(c.body, T, .7, .05, .02, x, .85, .31); bx(c.body, MT.glass, .26, .3, .02, x, 1.1, .31); bx(c.body, MT.glass, .26, .3, .02, x, .35, .31);
      }
      bx(c.body, P, .6, 1.2, .3, 0, 0, -.27); lmGable(c, M.otile, .65, .35, .35, 0, 1.2, -.27); bx(c.body, MT.black, .3, .6, .02, 0, 0, -.11);
      for (const x of [-.6, .7]) { bx(c.body, MT.brick, .25, 2.9, .25, x, 0, -1.35); for (const d of [-.06, .06]) cy(c.body, MT.brick, .06, .3, x + d, 2.9, -1.35); c.chim.push(x, 3.25, -1.35); }
      bx(c.body, MT.soil, 1.6, .04, .95, -.95, 0, 1.3); for (let i = 0; i < 4; i++) bx(c.body, MT.wheat, 1.5, .22, .12, -.95, .04, .95 + i * .22);
      cy(c.body, MT.hay, .25, .3, .95, 0, 1.35); cn(c.roof, MT.hay, .27, .35, .95, .3, 1.35); bx(c.body, MT.dgreen, 1.3, .25, .15, .9, 0, 1.78);
      lmFlag(c, 1.75, .8, 2.2);
    },
    okcutalim(c) {   // the village archery butts: earth banks with straw targets, a shooting line, a longbow rack, a popinjay pole
      bx(c.body, LMM.turf, 3.7, .04, 3.7, 0, 0, 0);
      for (const x of [-1.2, 0, 1.2]) {
        bx(c.body, MT.soil2, .9, .55, .45, x, 0, -1.55); lmGable(c, LMM.turf, .45, .25, .9, x, .55, -1.55, PI / 2);
        for (const [m, d, z] of [[MT.hay, .6, -1.2], [MT.white, .42, -1.15], [MT.red, .24, -1.13], [MT.gold, .08, -1.11]]) mk(G.wheel, c.body, m, m === MT.hay ? .1 : .02, d, d, x, .62, z).rotation.y = PI / 2;
        for (const d of [-.18, .18]) cy(c.body, MT.dwood, .025, .6, x + d, 0, -1.27);
      }
      bx(c.body, MT.dwood, 3.2, .05, .05, 0, .45, .55); for (const x of [-1.6, 0, 1.6]) cy(c.body, MT.dwood, .04, .5, x, 0, .55);
      for (const s of [-1, 1]) cy(c.body, MT.dwood, .04, 1.0, -1.2 + s * .5, 0, 1.25); bx(c.body, MT.dwood, 1.1, .06, .06, -1.2, .9, 1.25);
      for (let i = 0; i < 5; i++) bx(c.body, M.yew, .03, 1.4, .03, -1.55 + i * .17, 0, 1.12).rotation.x = .2;
      cy(c.body, MT.wood, .15, .4, -.25, 0, 1.3); cy(c.body, MT.lwood, .1, .15, -.25, .4, 1.3); cy(c.body, MT.white, .12, .1, -.25, .55, 1.3);
      for (const [x, z] of [[.75, .75], [1.65, .75], [.75, 1.55], [1.65, 1.55]]) cy(c.body, MT.dwood, .05, 1.0, x, 0, z);
      lmGable(c, MT.thatch, 1.15, .55, 1.1, 1.2, 1.0, 1.15); bx(c.body, MT.wood, .8, .3, .25, 1.2, 0, 1.3);
      cy(c.body, MT.dwood, .04, 3.2, 1.6, 0, -.4); bx(c.body, MT.dwood, .5, .04, .04, 1.6, 2.9, -.4); sp(c.roof, c.cm, .1, 1.6, 3.3, -.4); bx(c.roof, MT.gold, .04, .04, .2, 1.6, 3.28, -.3);
      lmFlag(c, -1.65, -.3, 2.2);
    },
    westminster(c) {   // the gothic abbey: two square west towers with pinnacles, a long nave, flying buttresses, rose windows
      const A = M.abbey, R = LMM.lead;
      bx(c.body, A, 1.1, 1.8, 2.6, 0, 0, -.55); lmGable(c, R, 1.2, .7, 2.7, 0, 1.8, -.55);
      for (const s of [-1, 1]) { bx(c.body, A, .45, 1.0, 2.4, s * .78, 0, -.55); bx(c.roof, R, .5, .06, 2.45, s * .78, 1.0, -.55); }
      for (const s of [-1, 1]) for (const z of [-1.6, -.25, .35]) {
        bx(c.body, A, .15, 1.3, .15, s * 1.08, 0, z); cn(c.roof, A, .08, .35, s * 1.08, 1.3, z);
        bx(c.body, A, .61, .07, .08, s * .815, 1.47, z).rotation.z = -s * .51;
      }
      for (const s of [-1, 1]) for (const z of [-1.3, -.0]) bx(c.body, MT.glass, .02, .5, .2, s * 1.01, .3, z);
      bx(c.body, A, 2.9, 1.6, .75, 0, 0, -.9); lmGable(c, R, .85, .6, 3.0, 0, 1.6, -.9, PI / 2);
      for (const s of [-1, 1]) { mk(G.wheel, c.body, MT.glass, .03, .55, .55, s * 1.46, 1.0, -.9); mk(G.wheel, c.body, MT.gold, .02, .14, .14, s * 1.475, 1.0, -.9); }
      bx(c.body, A, .55, .45, .55, 0, 1.8, -.9); py(c.roof, R, .6, .35, .6, 0, 2.25, -.9);
      for (const s of [-1, 1]) {
        const x = s * .55;
        bx(c.body, A, .5, 3.0, .55, x, 0, 1.0); bx(c.body, MT.black, .16, .5, .02, x, 2.2, 1.28); bx(c.body, MT.black, .16, .5, .02, x, 1.3, 1.28);
        for (const dx of [-.21, .21]) for (const dz of [-.22, .22]) cn(c.roof, A, .06, .45, x + dx, 3.0, 1.0 + dz);
      }
      bx(c.body, A, .62, 2.0, .45, 0, 0, 1.0); lmGable(c, A, .62, .35, .45, 0, 2.0, 1.0);
      bx(c.body, MT.glass, .38, 1.0, .02, 0, .85, 1.23); bx(c.body, MT.black, .26, .55, .02, 0, 0, 1.23); bx(c.body, c.cm, .4, .08, .03, 0, .6, 1.24);
      lmFlag(c, 1.6, 1.3, 2.2);
    },
    londrakulesi(c) {   // the Tower of London: the square White Tower with four domed corner turrets inside a curtain wall with round towers
      const S = M.rag, W = M.white, Q = 1.55;
      bx(c.body, LMM.turf, 3.8, .03, 3.8, 0, 0, 0);
      for (const [a, b] of [[[-Q, -Q], [Q, -Q]], [[Q, -Q], [Q, Q]], [[Q, Q], [-Q, Q]], [[-Q, Q], [-Q, -Q]]]) lmWall(c, S, a, b, 1.0, .28);
      lmCren(c, S, 3.38, 3.38, 1.0, 0, 0, .13);
      for (const x of [-Q, Q]) for (const z of [-Q, Q]) { cy(c.body, S, .32, 1.4, x, 0, z); cy(c.body, S, .35, .08, x, 1.4, z); lmCren(c, S, .6, .6, 1.48, x, z, .1); }
      for (const s of [-1, 1]) { cy(c.body, S, .25, 1.5, s * .38, 0, Q); cy(c.body, S, .27, .08, s * .38, 1.5, Q); }
      bx(c.body, S, .55, 1.2, .4, 0, 0, Q); bx(c.body, MT.black, .3, .65, .02, 0, 0, Q + .21);
      bx(c.body, W, 1.6, 2.0, 1.3, 0, 0, -.2); lmCren(c, W, 1.6, 1.3, 2.0, 0, -.2, .12);
      for (const s of [-1, 1]) bx(c.body, W, .06, 2.0, .04, s * .4, 0, .46);
      for (let r = 0; r < 2; r++) for (const x of [-.6, -.2, .2, .6]) bx(c.body, MT.black, .1, .2, .02, x, .8 + r * .6, .46);
      bx(c.body, W, .45, .9, .45, -.45, 0, .65);
      for (const [x, z] of [[-.8, -.85], [.8, -.85], [-.8, .45], [.8, .45]]) {
        if (x > 0 && z < 0) cy(c.body, W, .2, 2.55, x, 0, z); else bx(c.body, W, .32, 2.55, .32, x, 0, z);
        lmDome(c, LMM.lead, .2, x, 2.55, z, 1.4); cy(c.roof, LMM.lead, .02, .25, x, 2.8, z); sp(c.roof, MT.gold, .04, x, 3.08, z);
      }
      bx(c.body, MT.plaster, .7, .7, .5, 1.0, 0, .8); lmGable(c, MT.tile, .7, .35, .55, 1.0, .7, .8, PI / 2);
      for (let i = 0; i < 5; i++) bx(c.body, MT.dwood, .04, .7, .02, .72 + i * .14, 0, 1.06);
      sp(c.body, MT.black, .05, -.7, .05, 1.0); sp(c.body, MT.black, .05, -.55, .05, 1.15);
      lmFlag(c, 0, -.2, 3.0);
    },
    globe(c) {   // the Globe theatre: a ring of white-and-timber galleries under thatch round an open yard, the stage and its hut
      const N = 16, R = 1.5;
      for (let i = 0; i < N; i++) {
        const a = i / N * PI * 2, x = Math.cos(a) * R, z = Math.sin(a) * R, ry = PI / 2 - a;
        bx(c.body, M.half, .6, 1.4, .5, x, 0, z).rotation.y = ry;
        const t = bx(c.roof, MT.thatch, .68, .1, .8, x, 1.38, z); t.rotation.order = 'YXZ'; t.rotation.y = ry; t.rotation.x = .38;
        const b = (i + .5) / N * PI * 2; cy(c.body, MT.dwood, .035, 1.4, Math.cos(b) * 1.76, 0, Math.sin(b) * 1.76);
      }
      bx(c.body, MT.dwood, .6, .05, .03, 0, .7, 1.76); bx(c.body, MT.black, .32, .62, .03, 0, 0, 1.76);
      cy(c.body, MT.soil2, 1.27, .03, 0, 0, 0);
      bx(c.body, MT.wood, 1.1, .45, .75, 0, 0, -.95); for (const s of [-1, 1]) cy(c.body, LMM.marble, .05, 1.0, s * .38, .45, -.72);
      bx(c.roof, MT.dwood, 1.0, .06, .55, 0, 1.45, -.92); bx(c.body, LMM.blue, .9, .05, .02, 0, 1.4, -.64); bx(c.body, MT.lwood, .9, .7, .02, 0, .45, -1.25);
      bx(c.body, M.half, .7, .5, .5, 0, 1.4, -1.45); lmGable(c, MT.tile, .55, .3, .75, 0, 1.9, -1.45, PI / 2);
      lmFlag(c, 0, -1.55, 2.9);
    },
    kraliyettersane(c) {   // the Royal Dockyard: a galleon fitting out in a stone dry dock, a new hull on the slip, a crane, a store
      bx(c.body, LMM.water, 3.8, .03, 1.1, 0, 0, 1.4); bx(c.body, MT.stone, 3.8, .15, 2.85, 0, 0, -.5);
      bx(c.body, MT.dstone, 1.1, .17, 2.6, -.75, 0, -.4); bx(c.body, MT.dwood, 1.15, .3, .1, -.75, 0, .9);
      for (const z of [-1.2, -.4, .4]) for (const s of [-1, 1]) bx(c.body, MT.dwood, .06, .3, .06, -.75 + s * .38, .17, z);
      galleon(c, -.75, -.4, 0, 2.2, MT.canvas, null, true).position.y = .2;
      bx(c.body, MT.wood, .6, .06, 2.6, .75, .15, -.4); bx(c.body, MT.dwood, .1, .1, 2.0, .75, .21, -.6);
      for (let i = 0; i < 7; i++) for (const s of [-1, 1]) bx(c.body, MT.lwood, .05, .55, .05, .75 + s * .08, .25, -1.45 + i * .28).rotation.z = -s * .35;
      bx(c.body, MT.dwood, .08, .8, .08, .75, .21, .45).rotation.x = .4; bx(c.body, MT.dwood, .08, .7, .08, .75, .21, -1.62);
      bx(c.body, MT.brick, .55, 1.0, 1.3, 1.62, 0, -1.25); lmGable(c, M.slate, .65, .4, 1.4, 1.62, 1.0, -1.25);
      cy(c.body, MT.dwood, .06, 1.8, 1.65, .15, .45); bx(c.body, MT.dwood, .06, .06, 1.0, 1.65, 1.8, .7).rotation.x = .5; mk(G.wheel, c.body, MT.wood, .08, .55, .55, 1.5, .5, .45);
      for (let i = 0; i < 3; i++) cy(c.body, MT.wood, .08, 1.0, 1.3 + i * .17, .15, .2 + (i & 1) * .1).rotation.x = PI / 2;
      lmFlag(c, .1, -1.6, 2.3);
    },
    bigben(c) {   // the Palace of Westminster: a long gothic river front, the Victoria Tower and the clock tower by the Thames
      const S = M.goth;
      bx(c.body, LMM.water, 3.8, .03, .7, 0, 0, 1.55); bx(c.body, MT.stone, 3.8, .12, .25, 0, 0, 1.08); bx(c.body, MT.dwood, .7, .1, .25, -.5, .02, 1.6);
      bx(c.body, S, 2.6, 1.2, 1.1, -.1, 0, -.35); lmGable(c, M.slate, 1.15, .55, 2.6, -.1, 1.2, -.35, PI / 2);
      for (let i = 0; i < 9; i++) cn(c.roof, S, .05, .35, -1.3 + i * .3, 1.2, .2);
      for (let i = 0; i < 8; i++) bx(c.body, MT.glass, .12, .75, .02, -1.2 + i * .32, .25, .21);
      cy(c.body, S, .25, 1.0, -.1, 1.2, -.35); cn(c.roof, S, .26, .8, -.1, 2.2, -.35);
      bx(c.body, S, .85, 3.0, .85, -1.45, 0, -.45); bx(c.body, MT.glass, .3, 1.0, .02, -1.45, 1.6, -.02); bx(c.body, MT.black, .35, .6, .02, -1.45, 0, -.02);
      for (const dx of [-.4, .4]) for (const dz of [-.4, .4]) { cy(c.body, S, .07, 3.4, -1.45 + dx, 0, -.45 + dz); cn(c.roof, S, .08, .3, -1.45 + dx, 3.4, -.45 + dz); }
      bx(c.body, S, .55, 2.7, .55, 1.5, 0, .35); bx(c.body, S, .66, .62, .66, 1.5, 2.7, .35);
      mk(G.wheel, c.body, MT.gold, .03, .52, .52, 1.5, 3.01, .69).rotation.y = PI / 2; mk(G.wheel, c.body, M.dial, .03, .44, .44, 1.5, 3.01, .7).rotation.y = PI / 2;
      mk(G.wheel, c.body, MT.gold, .03, .52, .52, 1.84, 3.01, .35); mk(G.wheel, c.body, M.dial, .03, .44, .44, 1.85, 3.01, .35);
      bx(c.body, MT.black, .03, .17, .02, 1.5, 3.0, .72); bx(c.body, MT.black, .12, .03, .02, 1.55, 3.0, .72); bx(c.body, MT.black, .02, .17, .03, 1.865, 3.0, .35);
      bx(c.body, S, .5, .4, .5, 1.5, 3.32, .35); bx(c.body, MT.black, .3, .25, .02, 1.5, 3.38, .61);
      py(c.roof, M.slate, .62, 1.0, .62, 1.5, 3.72, .35); cy(c.roof, MT.gold, .02, .25, 1.5, 4.6, .35);
      lmFlag(c, -1.45, -.45, 3.7);
    },
    woolwich(c) {   // the Royal Arsenal: a brick foundry with a pedimented gate and a cupola, field guns, a mortar, shot piles
      const B = M.brick, P = M.port;
      bx(c.body, M.gravel, 3.8, .03, 3.8, 0, 0, 0);
      bx(c.body, B, 2.6, 1.3, 1.1, 0, 0, -1.1); bx(c.body, P, 2.62, .08, 1.12, 0, 1.3, -1.1); for (const s of [-1, 1]) bx(c.body, P, .12, 1.3, .12, s * 1.27, 0, -.55);
      lmGable(c, M.slate, 1.15, .5, 2.65, 0, 1.38, -1.1, PI / 2);
      bx(c.body, B, .9, 1.7, 1.25, 0, 0, -1.05); lmGable(c, P, .95, .4, 1.3, 0, 1.7, -1.05);
      bx(c.body, MT.black, .4, .8, .02, 0, 0, -.42); bx(c.body, MT.gold, .22, .22, .02, 0, 1.25, -.42);
      cy(c.body, P, .13, .3, 0, 2.0, -1.05); lmDome(c, LMM.lead, .14, 0, 2.3, -1.05); sp(c.roof, MT.gold, .03, 0, 2.47, -1.05);
      for (let r = 0; r < 2; r++) for (const x of [-1.05, -.65, .65, 1.05]) bx(c.body, MT.glass, .2, .35, .02, x, .3 + r * .5, -.54);
      for (const x of [-.9, .9]) { bx(c.body, B, .22, 2.6, .22, x, 0, -1.5); c.chim.push(x, 2.75, -1.5); }
      for (const x of [-.8, 0, .8]) {
        bx(c.body, MT.wood, .3, .22, .6, x, .08, .1); cy(c.body, MT.iron, .09, .9, x, .34, -.15).rotation.x = PI / 2;
        for (const s of [-1, 1]) mk(G.wheel, c.body, MT.dwood, .05, .36, .36, x + s * .19, .18, .2);
      }
      for (const x of [-1.45, 1.45]) { for (const dx of [-.09, .09]) for (const dz of [-.09, .09]) sp(c.body, MT.iron, .09, x + dx, .09, .95 + dz); sp(c.body, MT.iron, .09, x, .23, .95); }
      bx(c.body, MT.wood, .5, .15, .5, 0, 0, 1.3); cy(c.body, MT.iron, .17, .4, 0, .15, 1.3).rotation.x = .5;
      for (const [x, z, y] of [[1.5, -.2, 0], [1.5, .15, 0], [1.25, -.05, 0], [1.42, -.03, .32]]) cy(c.body, MT.wood, .14, .32, x, y, z);
      lmFlag(c, -1.6, -.2, 2.2);
    },
    // ---- İspanyollar ----
    zeytinlik(c) {   // an olive grove and its almazara: a whitewashed mill house, the stone press, oil jars, rows of olive trees
      const W = M.whitew;
      bx(c.body, M.dry, 3.8, .03, 3.8, 0, 0, 0);
      bx(c.body, W, 2.0, 1.0, 1.0, -.7, 0, -1.3); lmGable(c, M.terra, 1.1, .45, 2.1, -.7, 1.0, -1.3, PI / 2);
      bx(c.body, W, .35, .5, .1, -1.45, 1.0, -.82); bx(c.body, MT.bronze, .1, .14, .04, -1.45, 1.2, -.78);
      bx(c.body, MT.black, .32, .6, .02, -.7, 0, -.79); for (const x of [-1.35, -.1]) bx(c.body, LMM.blue, .22, .26, .02, x, .45, -.79);
      bx(c.body, W, .2, .6, .2, .05, 1.0, -1.55); c.chim.push(.05, 1.7, -1.55);
      cy(c.body, MT.stone, .55, .35, .9, 0, -.9); mk(G.wheel, c.body, MT.dstone, .16, .55, .55, .9, .62, -.9); cy(c.body, MT.dwood, .05, .9, .9, .35, -.9); bx(c.body, MT.dwood, .9, .05, .05, 1.3, .82, -.9);
      for (let i = 0; i < 4; i++) { const x = -1.5 + i * .38; sp(c.body, M.terra, .16, x, .16, -.55); cy(c.body, M.terra, .07, .08, x, .3, -.55); }
      for (let r = 0; r < 2; r++) for (let i = 0; i < 4; i++) {
        const x = -1.35 + i * .9 + r * .3, z = .45 + r * .9;
        cy(c.body, LMM.bark, .07, .45, x, 0, z); mk(G.sph, c.body, (i + r) & 1 ? M.olive : M.oliveD, .75, .45, .7, x, .68, z); sp(c.body, M.olive, .2, x + .15, .9, z - .05);
      }
      for (const x of [.95, 1.25]) { cy(c.body, MT.hay, .14, .15, x, 0, -.2); cy(c.body, mat(0x2c2a24, .6), .12, .02, x, .15, -.2); }
      lmFlag(c, 1.7, -1.6, 2.0);
    },
    reconquista(c) {   // a Castilian frontier castle on a rock: a tall keep with corner bartizans, round towers, a twin-towered gate
      const S = M.ochre;
      lmSteps(c, M.rock, 3.7, 3.5, 3, .2, 0, 0, .35);
      for (const [x, z] of [[-1.6, 1.4], [1.65, -1.0], [1.5, 1.5], [-1.55, -1.3]]) mk(G.rock, c.body, M.rock, .6, .5, .6, x, .1, z);
      for (const s of [-1, 1]) { bx(c.body, S, 2.6, .9, .25, 0, .6, s * 1.2); bx(c.body, S, .25, .9, 2.4, s * 1.3, .6, 0); }
      lmCren(c, S, 2.85, 2.65, 1.5, 0, 0, .12);
      for (const x of [-1.3, 1.3]) for (const z of [-1.2, 1.2]) { cy(c.body, S, .3, 1.3, x, .6, z); cy(c.body, S, .34, .1, x, 1.9, z); }
      bx(c.body, S, 1.0, 2.7, .9, -.35, .6, -.4); lmCren(c, S, 1.0, .9, 3.3, -.35, -.4, .12);
      for (const dx of [-.5, .5]) for (const dz of [-.45, .45]) { cy(c.body, S, .13, .45, -.35 + dx, 2.95, -.4 + dz); cn(c.roof, S, .13, .12, -.35 + dx, 2.95, -.4 + dz).rotation.x = PI; }
      for (const y of [1.4, 2.2]) bx(c.body, MT.black, .06, .3, .02, -.35, y, .06);
      for (const s of [-1, 1]) { bx(c.body, S, .4, 1.4, .4, s * .4, .6, 1.25); lmCren(c, S, .4, .4, 2.0, s * .4, 1.25, .1); }
      bx(c.body, MT.black, .35, .6, .02, 0, .6, 1.33); bx(c.body, MT.dwood, .4, .06, .02, 0, 1.15, 1.34);
      bx(c.body, MT.plaster, .9, .55, .6, .6, .6, -.4); lmGable(c, M.terra, .7, .3, 1.0, .6, 1.15, -.4, PI / 2);
      bx(c.body, MT.red, .02, .25, .35, .4, 2.2, 1.42); bx(c.body, MT.gold, .02, .1, .35, .4, 2.2, 1.42);
      lmFlag(c, -.35, -.4, 3.9);
    },
    santiago(c) {   // Santiago de Compostela: the baroque Obradoiro front with two tiered towers over a double stair, the nave, a domed crossing
      const S = M.santi, R = M.stile;
      lmSteps(c, MT.stone, 2.6, .9, 3, .1, 0, 1.45, .18);
      bx(c.body, S, 1.3, 1.6, 2.4, 0, 0, -.6); lmGable(c, R, 1.4, .6, 2.5, 0, 1.6, -.6);
      bx(c.body, S, 3.0, 1.4, .8, 0, 0, -.9); lmGable(c, R, .9, .5, 3.1, 0, 1.4, -.9, PI / 2);
      cy(c.body, S, .38, .7, 0, 1.9, -.9); lmDome(c, R, .4, 0, 2.6, -.9, .8); cy(c.roof, S, .08, .25, 0, 2.92, -.9);
      bx(c.body, S, .5, 2.6, .5, 1.25, 0, -1.55); py(c.roof, R, .6, .6, .6, 1.25, 2.6, -1.55);
      bx(c.body, S, 1.0, 2.5, .45, 0, 0, .8); bx(c.body, MT.glass, .5, .9, .02, 0, 1.0, 1.03); bx(c.body, MT.black, .3, .55, .02, 0, .3, 1.03);
      for (const s of [-1, 1]) cy(c.body, S, .05, 2.3, s * .4, .1, 1.05);
      bx(c.body, S, .7, .45, .35, 0, 2.5, .8); bx(c.body, S, .12, .3, .1, 0, 2.95, .85); bx(c.body, MT.gold, .25, .2, .02, 0, 2.1, 1.04);
      for (const s of [-1, 1]) {
        const x = s * .75;
        bx(c.body, S, .55, 2.3, .55, x, 0, .8); bx(c.body, S, .46, .55, .46, x, 2.3, .8); bx(c.body, MT.black, .2, .3, .02, x, 2.4, 1.04);
        bx(c.body, S, .34, .45, .34, x, 2.85, .8); cy(c.body, S, .14, .35, x, 3.3, .8); lmDome(c, R, .17, x, 3.65, .8, 1.3); cn(c.roof, MT.gold, .04, .3, x, 3.85, .8);
        for (const dx of [-.25, .25]) for (const dz of [-.25, .25]) sp(c.body, S, .05, x + dx, 2.35, .8 + dz);
      }
      bx(c.body, c.cm, .5, .08, .03, 0, 1.95, 1.04);
      lmFlag(c, -1.5, 1.0, 2.0);
    },
    toledo(c) {   // the Toledo sword forge: a Mudéjar brick workshop with horseshoe arches, a tiled tower, a sword rack, anvil and grindstone
      const B = M.mbrick;
      bx(c.body, MT.stone, 3.6, .03, 3.4, 0, 0, 0);
      bx(c.body, B, 2.6, 1.3, 1.2, -.3, 0, -1.1); lmGable(c, M.terra, 1.3, .5, 2.7, -.3, 1.3, -1.1, PI / 2);
      for (const x of [-1.2, -.3, .6]) {
        const m = x === -.3 ? MT.glow : MT.black;
        bx(c.body, M.whitew, .62, 1.0, .02, x, 0, -.495); bx(c.body, m, .36, .6, .03, x, 0, -.48); mk(G.wheel, c.body, m, .03, .44, .44, x, .62, -.48).rotation.y = PI / 2;
      }
      bx(c.body, B, .55, 2.9, .55, 1.4, 0, -1.3);
      for (const y of [1.6, 2.3]) bx(c.body, M.glaze, .57, .1, .57, 1.4, y, -1.3);
      bx(c.body, MT.black, .2, .35, .02, 1.4, 2.42, -1.02); py(c.roof, M.terra, .65, .5, .65, 1.4, 2.9, -1.3);
      cy(c.body, B, .18, 2.4, -1.3, 0, -1.4); c.chim.push(-1.3, 2.5, -1.4); c.chim.push(-.3, 1.0, -.4);
      bx(c.body, MT.dwood, .18, .3, .18, -.1, 0, .2); bx(c.body, MT.iron, .32, .12, .15, -.1, .3, .2); bx(c.body, MT.iron, .1, .04, .04, -.3, .38, .2);
      bx(c.body, MT.wood, .7, .25, .3, .75, 0, .1); bx(c.body, LMM.water, .62, .02, .22, .75, .25, .1);
      mk(G.wheel, c.body, MT.stone, .1, .5, .5, -1.0, .35, .3); for (const s of [-1, 1]) bx(c.body, MT.dwood, .05, .35, .05, -1.0 + s * .1, 0, .3);
      bx(c.body, MT.dwood, 1.6, .12, .22, .2, 0, 1.25);
      for (let i = 0; i < 6; i++) { const x = -.45 + i * .26; bx(c.body, MT.steel, .05, .8, .015, x, .1, 1.25); bx(c.body, MT.gold, .16, .03, .03, x, .9, 1.25); bx(c.body, MT.leather, .03, .15, .03, x, .93, 1.25); }
      lmFlag(c, 1.6, .6, 2.2);
    },
    altinkule(c) {   // Seville's Torre del Oro: a twelve-sided tower in two stages and a gilded lantern dome by the river, treasure on the quay
      const S = M.oro;
      bx(c.body, MT.stone, 3.8, .1, 2.4, 0, 0, -.7); bx(c.body, LMM.water, 3.8, .03, 1.4, 0, 0, 1.25); bx(c.body, MT.stone, 3.8, .2, .15, 0, 0, .5);
      mk(D12, c.body, S, 2.0, 1.9, 2.0, 0, .95, -.4);
      for (let i = 0; i < 12; i++) { const a = (i + .5) / 12 * PI * 2; bx(c.body, S, .22, .2, .14, Math.cos(a) * .93, 1.9, -.4 + Math.sin(a) * .93).rotation.y = PI / 2 - a; }
      bx(c.body, MT.black, .12, .3, .02, 0, 1.0, .6); bx(c.body, MT.black, .14, .5, .02, 0, .2, .6); for (const s of [-1, 1]) bx(c.body, MT.black, .02, .3, .12, s * 1.0, 1.0, -.4);
      mk(D12, c.body, M.oroL, 1.25, 1.0, 1.25, 0, 2.4, -.4);
      for (let i = 0; i < 12; i++) { const a = (i + .5) / 12 * PI * 2; bx(c.body, M.oroL, .14, .16, .1, Math.cos(a) * .58, 2.9, -.4 + Math.sin(a) * .58).rotation.y = PI / 2 - a; }
      bx(c.body, MT.black, .1, .25, .02, 0, 2.4, .23);
      cy(c.body, M.oroL, .36, .6, 0, 2.9, -.4); lmDome(c, LMM.goldm, .38, 0, 3.5, -.4, 1.1); sp(c.roof, MT.gold, .06, 0, 3.98, -.4); cy(c.roof, MT.gold, .015, .3, 0, 4.02, -.4);
      bx(c.body, LMM.sandD, 1.0, 1.1, .3, -1.45, 0, -.9); lmCren(c, LMM.sandD, 1.0, .3, 1.1, -1.45, -.9, .12);
      for (const [x, z] of [[1.25, .1], [1.6, -.2], [1.15, -.4]]) { bx(c.body, MT.dwood, .35, .22, .25, x, .1, z); bx(c.body, LMM.goldm, .3, .06, .2, x, .32, z); }
      bx(c.body, MT.dwood, .9, .2, .3, -.9, 0, 1.3); cy(c.body, MT.wood, .025, 1.0, -.9, .2, 1.3); bx(c.body, MT.canvas, .55, .5, .02, -.9, .45, 1.3).rotation.z = .3;
      lmFlag(c, 1.7, -1.5, 2.0);
    },
    tercio(c) {   // the tercio barracks: a whitewashed arcaded quarter, a square of pikes in its rack, arquebuses, a drum, the Burgundy cross
      const W = M.whitew;
      bx(c.body, M.dry, 3.8, .03, 3.8, 0, 0, 0);
      bx(c.body, W, 3.4, 1.1, .9, 0, 0, -1.4); lmGable(c, M.terra, 1.0, .45, 3.5, 0, 1.1, -1.4, PI / 2);
      bx(c.body, W, .9, 1.1, 1.6, -1.45, 0, -.15); lmGable(c, M.terra, 1.0, .45, 1.7, -1.45, 1.1, -.15);
      lmCols(c, 7, -.9, 1.5, -.85, .8, MT.stone, .05); bx(c.roof, M.terra, 2.6, .06, .32, .3, .8, -.85);
      for (const x of [-.6, .2, 1.0]) bx(c.body, MT.black, .25, .5, .02, x, 0, -.94);
      for (const z of [-.6, -.1, .4]) bx(c.body, MT.black, .02, .3, .18, -.99, .5, z);
      for (const z of [.15, 1.05]) bx(c.body, MT.dwood, 1.0, .06, .06, .9, .5, z); for (const x of [.45, 1.35]) bx(c.body, MT.dwood, .06, .06, 1.0, x, .5, .6);
      for (const x of [.6, .9, 1.2]) for (const z of [.3, .6, .9]) { cy(c.body, MT.dwood, .018, 2.3, x, 0, z); cn(c.body, MT.steel, .03, .14, x, 2.3, z); }
      for (const s of [-1, 1]) cy(c.body, MT.dwood, .03, .75, -.5 + s * .45, 0, .6); bx(c.body, MT.dwood, .95, .06, .06, -.5, .7, .6);
      for (let i = 0; i < 5; i++) bx(c.body, MT.black, .04, .9, .04, -.82 + i * .16, 0, .5).rotation.x = .25;
      cy(c.body, MT.red, .15, .25, -.5, 0, 1.3); cy(c.body, MT.white, .155, .04, -.5, .25, 1.3);
      cy(c.body, MT.dwood, .025, 2.5, 0, 0, 1.4); bx(c.body, MT.white, .8, .6, .02, -.42, 1.85, 1.4);
      for (const a of [-.6, .6]) mk(G.cbox, c.body, MT.red, .85, .07, .025, -.42, 2.15, 1.41).rotation.z = a;
      lmFlag(c, 1.6, -.5, 2.2);
    },
    escorial(c) {   // El Escorial: a vast grey granite square under slate, spired corner towers, the domed basilica with its two towers
      const S = M.granite, R = LMM.dtile;
      bx(c.body, MT.stone, 3.8, .06, 3.8, 0, 0, 0);
      for (const s of [-1, 1]) {
        bx(c.body, S, 3.2, 1.1, .45, 0, .06, s * 1.4); lmGable(c, R, .55, .35, 3.2, 0, 1.16, s * 1.4, PI / 2);
        bx(c.body, S, .45, 1.1, 2.35, s * 1.4, .06, 0); lmGable(c, R, .55, .35, 2.35, s * 1.4, 1.16, 0);
        bx(c.body, S, .75, .9, .3, s * .85, .06, .55); bx(c.roof, R, .8, .06, .35, s * .85, .96, .55);
      }
      for (const x of [-1.5, 1.5]) for (const z of [-1.5, 1.5]) {
        bx(c.body, S, .6, 1.7, .6, x, 0, z); py(c.roof, R, .55, 1.0, .55, x, 1.7, z); sp(c.roof, MT.gold, .05, x, 2.75, z); cy(c.roof, MT.gold, .012, .25, x, 2.8, z);
      }
      bx(c.body, S, 1.1, 1.5, 1.2, 0, .06, -.45); lmGable(c, R, 1.15, .4, 1.25, 0, 1.56, -.45);
      cy(c.body, S, .38, .5, 0, 1.56, -.6); lmDome(c, R, .42, 0, 2.06, -.6); cy(c.roof, S, .09, .3, 0, 2.48, -.6); cn(c.roof, R, .1, .3, 0, 2.78, -.6); sp(c.roof, MT.gold, .04, 0, 3.1, -.6);
      for (const s of [-1, 1]) { const x = s * .42; bx(c.body, S, .32, 2.0, .32, x, .06, .25); cy(c.body, S, .12, .25, x, 2.06, .25); lmDome(c, R, .13, x, 2.31, .25, 1.3); cn(c.roof, MT.gold, .02, .2, x, 2.48, .25); }
      bx(c.body, S, .8, 1.5, .1, 0, .06, 1.66); lmGable(c, S, .85, .3, .12, 0, 1.56, 1.66); bx(c.body, MT.black, .25, .5, .02, 0, .06, 1.72); bx(c.body, c.cm, .3, .08, .03, 0, .7, 1.72);
      for (let r = 0; r < 2; r++) for (const x of [-1.05, -.75, -.5, .5, .75, 1.05]) bx(c.body, MT.black, .1, .18, .02, x, .35 + r * .4, 1.63);
      lmFlag(c, .95, 1.0, 2.2);
    },
    armada(c) {   // the Armada yard: the long brick naves of the atarazanas on the quay, a galleon with Burgundy-cross sails on the water
      bx(c.body, LMM.water, 3.8, .03, 2.1, 0, 0, .85); bx(c.body, MT.stone, 3.8, .2, .3, 0, 0, -.35);
      for (const x of [-1.35, -.45, .45, 1.35]) {
        bx(c.body, M.mbrick, .85, 1.1, 1.5, x, 0, -1.2); lmGable(c, M.terra, .9, .45, 1.55, x, 1.1, -1.2);
        bx(c.body, MT.black, .45, .65, .02, x, 0, -.44); py(c.body, MT.black, .45, .25, .02, x, .65, -.44);
      }
      galleon(c, -.05, .95, PI / 2, 2.6, MT.white, LMM.sail1);
      bx(c.body, MT.dwood, .7, .12, .3, -1.45, .02, 1.55); for (const s of [-1, 1]) bx(c.body, MT.lwood, .02, .02, .5, -1.45 + s * .2, .14, 1.55);
      cy(c.body, MT.dwood, .05, 1.6, -1.75, .2, -.3); bx(c.body, MT.dwood, .06, .06, .9, -1.75, 1.7, -.05).rotation.x = .6;
      for (const x of [-.5, 1.3]) cy(c.body, MT.iron, .07, .5, x, .27, -.33).rotation.z = PI / 2;
      lmFlag(c, 1.75, -.3, 2.0);
    },
    // ---- Kartacalılar ----
    kothon(c) {   // the Cothon: a round war harbour ringed by ship sheds, the admiral's island tower in the middle, triremes on the water
      const W = M.punW, N = 14, st = PI * 2 / N;
      bx(c.body, M.punic, 3.8, .1, 3.8, 0, 0, 0); cy(c.body, LMM.water, 1.45, .02, 0, .1, 0); bx(c.body, LMM.water, .6, .02, .7, 0, .1, 1.6);
      for (let i = 0; i < N; i++) {
        const a = i * st; if (Math.abs(a - PI / 2) < .3) continue;
        lmGable(c, MT.tile, .62, .3, .5, Math.cos(a) * 1.68, .6, Math.sin(a) * 1.68, PI / 2 - a);
        const b = a + st / 2; bx(c.body, W, .06, .5, .5, Math.cos(b) * 1.68, .1, Math.sin(b) * 1.68).rotation.y = PI / 2 - b;
        cy(c.body, W, .04, .5, Math.cos(b) * 1.43, .1, Math.sin(b) * 1.43);
        if (i & 1) bx(c.body, MT.dwood, .16, .12, .45, Math.cos(a) * 1.66, .12, Math.sin(a) * 1.66).rotation.y = PI / 2 - a;
      }
      cy(c.body, M.punic, .65, .3, 0, .1, 0); for (let i = 0; i < 8; i++) { const a = i / 8 * PI * 2; cy(c.body, W, .04, .6, Math.cos(a) * .48, .4, Math.sin(a) * .48); }
      cy(c.roof, W, .55, .08, 0, 1.0, 0); bx(c.body, W, .38, 1.7, .38, 0, .4, 0); bx(c.body, M.punic, .48, .1, .48, 0, 2.1, 0); lmCren(c, W, .48, .48, 2.2, 0, 0, .1);
      for (const [x, z, r] of [[-.95, .55, -.5], [.9, -.75, 2.4]]) {
        const g = new THREE.Group(); g.position.set(x, .1, z); g.rotation.y = r; c.body.add(g);
        bx(g, MT.dwood, .26, .14, 1.0, 0, 0, 0); bx(g, MT.bronze, .06, .06, .2, 0, .02, .58); bx(g, MT.dwood, .06, .3, .1, 0, .1, -.5).rotation.x = -.4;
        bx(g, c.cm, .27, .04, 1.0, 0, .1, 0); for (let i = 0; i < 5; i++) for (const s of [-1, 1]) bx(g, MT.lwood, .35, .02, .02, s * .28, .08, -.3 + i * .15);
        cy(g, MT.wood, .02, .7, 0, .14, .1);
      }
      lmFlag(c, 0, 0, 2.7);
    },
    paraliasker(c) {   // the mercenary camp: a stake palisade, tents of many peoples, the paymaster's awning with chests of gold, a practice post
      bx(c.body, M.dry, 3.8, .03, 3.8, 0, 0, 0);
      bx(c.body, MT.dwood, 3.5, .8, .12, 0, 0, -1.75); for (let i = 0; i < 11; i++) cn(c.body, MT.dwood, .07, .18, -1.7 + i * .34, .8, -1.75);
      for (const s of [-1, 1]) bx(c.body, MT.dwood, .12, .8, 2.0, s * 1.75, 0, -.8);
      cy(c.body, XM.hide, .45, .4, -1.1, 0, -1.0); cn(c.roof, XM.hide, .48, .7, -1.1, .4, -1.0);
      lmGable(c, M.dhide, .9, .5, 1.1, -1.2, 0, .35);
      lmGable(c, MT.white, .8, .65, 1.0, 1.15, 0, -.95); bx(c.roof, LMM.sail1, .82, .08, 1.02, 1.15, .3, -.95);
      lmGable(c, LMM.sail1, .7, .55, .8, .25, 0, -1.2);
      for (const dx of [-.45, .45]) for (const dz of [-.35, .35]) cy(c.body, MT.dwood, .04, 1.0, dx, 0, .55 + dz);
      py(c.roof, M.purple, 1.2, .35, 1.0, 0, 1.0, .55); bx(c.roof, c.cm, 1.15, .06, .95, 0, .96, .55);
      bx(c.body, MT.wood, .8, .4, .4, 0, 0, .55);
      for (const [x, h] of [[-.25, .12], [-.05, .2], [.15, .08], [.3, .15]]) cy(c.body, LMM.goldm, .06, h, x, .4, .55);
      for (const s of [-1, 1]) { bx(c.body, MT.dwood, .35, .25, .25, s * .7, 0, 1.15); bx(c.body, LMM.goldm, .3, .05, .2, s * .7, .25, 1.15); }
      for (const s of [-1, 1]) cy(c.body, MT.dwood, .03, .7, 1.25 + s * .45, 0, .75); bx(c.body, MT.dwood, 1.0, .06, .06, 1.25, .62, .75);
      [MT.red, LMM.blue, MT.white].forEach((m, i) => { mk(G.wheel, c.body, m, .04, .38, .38, .9 + i * .35, .42, .8).rotation.y = PI / 2; });
      for (let i = 0; i < 3; i++) cy(c.body, MT.dwood, .015, 1.4, 1.0 + i * .25, 0, .7);
      cy(c.body, MT.dwood, .08, 1.2, .3, 0, -.4); bx(c.body, MT.dwood, .6, .06, .06, .3, .9, -.4); sp(c.body, MT.hay, .12, .3, 1.3, -.4);
      cy(c.body, MT.dstone, .22, .07, -.6, 0, 1.3); cn(c.body, MT.glow, .12, .28, -.6, .05, 1.3); c.chim.push(-.6, .4, 1.3);
      lmFlag(c, -1.65, 1.5, 2.0);
    },
    byrsa(c) {   // the Byrsa hill: terraced slopes with whitewashed houses, a long stair, the colonnaded palace and its tower on top
      const W = M.punW, P = M.punic;
      lmSteps(c, P, 3.8, 3.6, 3, .3, 0, 0, .6);
      for (let i = 0; i < 9; i++) bx(c.body, W, .5, .1 * (i + 1), .1, 0, 0, 1.75 - i * .1);
      for (const [x, y, z] of [[-1.75, .3, .6], [-1.75, .3, -.5], [1.75, .3, .2], [1.75, .3, -1.1], [-1.45, .6, -1.0], [1.45, .6, -.6], [1.45, .6, .7]]) {
        bx(c.body, W, .26, .3, .35, x, y, z); bx(c.body, MT.black, .02, .14, .08, x + (x < 0 ? -.135 : .135), y, z);
      }
      bx(c.body, W, 1.8, 1.0, 1.1, 0, .9, -.45); lmCols(c, 7, -.8, .8, .3, .9, LMM.marble, .06, .9);
      bx(c.body, P, 1.9, .14, .5, 0, 1.8, .2); bx(c.body, LMM.goldm, 1.92, .06, .02, 0, 1.84, .46);
      bx(c.body, W, 1.0, .6, .7, 0, 1.9, -.5); bx(c.body, P, 1.05, .08, .75, 0, 2.5, -.5); bx(c.body, c.cm, .5, .1, .02, 0, 2.2, -.14);
      bx(c.body, W, .5, 1.9, .5, .85, .9, -.85); lmCren(c, W, .5, .5, 2.8, .85, -.85, .1);
      bx(c.body, W, .5, .55, .45, -.75, .9, .7); bx(c.body, P, .58, .08, .52, -.75, 1.45, .7); bx(c.body, MT.black, .16, .3, .02, -.75, .9, .93);
      palm(c, .9, .75, 1.9);
      lmFlag(c, -.6, -.6, 3.2);
    },
    filahirlari(c) {   // the elephant stables in the wall: a great stuccoed wall with arched stalls below and stables above, war elephants in front
      const W = M.punW;
      bx(c.body, M.dry, 3.8, .03, 3.8, 0, 0, 0);
      bx(c.body, W, 3.6, 2.0, 1.1, 0, 0, -1.2); lmCren(c, W, 3.6, 1.1, 2.0, 0, -1.2, .13);
      for (const x of [-.9, -.3, .3, .9]) {
        mk(G.wheel, c.body, M.punic, .02, .6, .6, x, .8, -.645).rotation.y = PI / 2; bx(c.body, M.punic, .55, .8, .02, x, 0, -.645);
        bx(c.body, MT.black, .45, .8, .02, x, 0, -.64); mk(G.wheel, c.body, MT.black, .02, .45, .45, x, .8, -.635).rotation.y = PI / 2;
      }
      for (let i = 0; i < 6; i++) bx(c.body, MT.black, .15, .25, .02, -1.5 + i * .6, 1.45, -.64);
      for (const s of [-1, 1]) { bx(c.body, W, .7, 2.6, .7, s * 1.55, 0, -1.25); lmCren(c, W, .75, .75, 2.6, s * 1.55, -1.25, .12); }
      elephant(c, -.7, .35, .3, .95, true); elephant(c, .85, .7, -.5, .9, false);
      cn(c.body, MT.hay, .35, .4, 1.5, 0, 1.4); bx(c.body, MT.hay, .4, .3, .3, -1.5, 0, 1.3); bx(c.body, MT.hay, .35, .3, .3, -1.4, .3, 1.3);
      bx(c.body, MT.stone, .9, .3, .3, -.1, 0, 1.6); bx(c.body, LMM.water, .82, .02, .22, -.1, .3, 1.6);
      lmFlag(c, 1.55, -1.25, 3.2);
    },
    morboya(c) {   // the Tyrian purple works: a flat-roofed workshop, dye vats, a boiling cauldron, purple cloth on the lines, a murex heap
      const W = M.punW, P = M.purple;
      bx(c.body, M.punic, 3.8, .04, 3.8, 0, 0, 0);
      bx(c.body, W, 1.8, 1.1, 1.0, -.85, 0, -1.3); bx(c.body, M.punic, 1.85, .1, 1.05, -.85, 1.1, -1.3); bx(c.body, MT.black, .35, .6, .02, -.85, 0, -.79);
      bx(c.roof, P, .8, .04, .4, -.85, .75, -.6); for (const x of [-1.5, -.2]) bx(c.body, MT.black, .15, .2, .02, x, .6, -.79);
      bx(c.body, W, 1.0, .9, .8, 1.2, 0, -1.4); bx(c.body, M.punic, 1.05, .08, .85, 1.2, .9, -1.4); for (let i = 0; i < 3; i++) bx(c.body, i & 1 ? M.purpleL : P, .22, .18, .1, .9 + i * .3, .3, -.97);
      for (const x of [-1.1, -.45, .2]) for (const z of [-.2, .45]) { cy(c.body, MT.stone, .26, .35, x, 0, z); cy(c.body, P, .22, .02, x, .35, z); }
      bx(c.body, MT.glow, .3, .18, .3, 1.1, 0, .1); cy(c.body, MT.dstone, .3, .08, 1.1, 0, .1); cy(c.body, MT.bronze, .25, .3, 1.1, .2, .1); cy(c.body, P, .22, .02, 1.1, .5, .1); c.chim.push(1.1, .6, .1);
      for (const z of [1.05, 1.55]) {
        for (const x of [-1.5, .3]) cy(c.body, MT.dwood, .03, 1.2, x, 0, z);
        bx(c.body, MT.dwood, 1.85, .03, .03, -.6, 1.15, z);
        for (let i = 0; i < 3; i++) bx(c.body, (i + (z > 1.3 ? 1 : 0)) & 1 ? M.purpleL : P, .45, .6, .02, -1.2 + i * .55, .55, z);
      }
      cn(c.body, M.murex, .45, .45, 1.3, 0, 1.3); for (const [x, z] of [[1.75, 1.1], [.9, 1.55], [1.6, 1.7], [.95, 1.05]]) sp(c.body, M.murex, .07, x, .05, z);
      for (const x of [1.65, 1.8]) { cy(c.body, M.terra, .1, .4, x, 0, .5); cn(c.body, M.terra, .1, .12, x, .4, .5); }
      lmFlag(c, 1.75, -.6, 2.0);
    },
    kartacasur(c) {   // the triple walls of Carthage: a ditch and staked bank, a crenellated middle wall, the great towered wall with its gate
      const W = M.punW, P = M.punic;
      bx(c.body, M.dry, 3.8, .03, 3.8, 0, 0, 0);
      bx(c.body, MT.soil, 3.8, .02, .35, 0, .03, 1.75); bx(c.body, MT.soil2, 3.8, .3, .3, 0, 0, 1.35);
      for (let i = 0; i < 9; i++) cy(c.body, MT.dwood, .04, .4, -1.7 + i * .425, .3, 1.35);
      bx(c.body, P, 3.8, 1.0, .3, 0, 0, .75); lmCren(c, P, 3.8, .3, 1.0, 0, .75, .12); bx(c.body, MT.black, .5, .7, .02, 0, 0, .91);
      bx(c.body, W, 3.8, 2.0, .6, 0, 0, -.6); lmCren(c, W, 3.8, .6, 2.0, 0, -.6, .14);
      for (const x of [-1.45, -.55, .55, 1.45]) {
        bx(c.body, W, .7, 2.8, .8, x, 0, -.6); lmCren(c, W, .7, .7, 2.8, x, -.6, .14); bx(c.body, MT.black, .08, .3, .02, x, 1.8, -.19); bx(c.body, MT.black, .08, .3, .02, x, 1.0, -.19);
      }
      bx(c.body, MT.black, .5, 1.1, .02, 0, 0, -.29); mk(G.wheel, c.body, MT.black, .02, .5, .5, 0, 1.1, -.29).rotation.y = PI / 2; bx(c.body, c.cm, .6, .1, .03, 0, 1.6, -.29);
      bx(c.body, P, 3.0, 1.1, .7, 0, 0, -1.5); bx(c.roof, MT.tile, 3.05, .06, .75, 0, 1.1, -1.5);
      lmFlag(c, .55, -.6, 3.4);
    },
    tanit(c) {   // the temple of Tanit: a podium, a cella under an Egyptian gorge cornice, two free pillars, the sign of Tanit and the crescent, tophet stelae
      const W = M.punW, P = M.punic, Au = LMM.goldm;
      bx(c.body, P, 3.8, .04, 3.8, 0, 0, 0);
      lmSteps(c, P, 2.2, 2.0, 3, .15, 0, -.6, .2);
      bx(c.body, W, 1.3, 1.4, 1.1, 0, .45, -.75); bx(c.body, P, 1.5, .12, 1.3, 0, 1.85, -.75); bx(c.body, W, 1.6, .1, 1.4, 0, 1.97, -.75);
      sp(c.body, Au, .1, 0, 1.65, -.19); bx(c.body, Au, .7, .07, .02, 0, 1.62, -.18); bx(c.body, MT.black, .4, .8, .02, 0, .45, -.19);
      for (const s of [-1, 1]) { cy(c.body, W, .09, 1.3, s * .5, .45, .05); cy(c.body, Au, .13, .12, s * .5, 1.75, .05); }
      py(c.body, Au, .45, .45, .04, 0, 2.07, -.25); bx(c.body, Au, .5, .05, .04, 0, 2.5, -.25); sp(c.body, Au, .1, 0, 2.66, -.25);
      for (let k = -2; k <= 2; k++) { const t = k * .55; mk(G.cbox, c.body, Au, k ? .1 : .13, k ? .05 : .07, .04, Math.sin(t) * .22, 3.08 - Math.cos(t) * .22, -.25).rotation.z = t; }
      for (const s of [-1, 1]) for (let i = 0; i < 4; i++) {
        const x = s * (1.0 + (i & 1) * .35), z = .75 + (i >> 1) * .45;
        bx(c.body, MT.stone, .14, .35, .06, x, 0, z); py(c.body, MT.stone, .14, .1, .06, x, .35, z);
      }
      bx(c.body, P, .55, .45, .45, 0, 0, 1.25); bx(c.body, MT.glow, .3, .1, .25, 0, .45, 1.25); c.chim.push(0, .7, 1.25);
      for (const s of [-1, 1]) palm(c, s * 1.3, -1.45, 1.8);
      lmFlag(c, -1.0, .2, 2.2);
    },
    hannibalkamp(c) {   // Hannibal's camp below the Alps: snowy peaks behind, rows of tents, the purple command tent, the standard, a war elephant
      bx(c.body, mat(0x9a8a62, 1), 3.8, .03, 3.8, 0, 0, 0);
      for (const [x, z, r, h] of [[-1.2, -1.25, .7, 2.3], [0, -1.3, .75, 3.0], [1.2, -1.25, .7, 2.0]]) {
        cn(c.body, M.rock, r, h, x, 0, z); cn(c.roof, M.snow, r * .42, h * .4, x, h * .6, z);
      }
      for (const [x, z] of [[-.6, -.6], [.6, -.55], [-1.6, -.5]]) { cy(c.body, LMM.bark, .04, .2, x, 0, z); cn(c.body, LMM.pine, .2, .6, x, .2, z); }
      for (let r = 0; r < 2; r++) for (let i = 0; i < 3; i++) lmGable(c, MT.canvas, .55, .5, .7, -1.35 + i * .62, 0, .05 + r * .85);
      cy(c.body, M.purple, .5, .55, 1.1, 0, .3); cn(c.roof, M.purple, .55, .65, 1.1, .55, .3); sp(c.roof, MT.gold, .05, 1.1, 1.22, .3); bx(c.body, MT.black, .3, .45, .02, 1.1, 0, .8);
      cy(c.body, MT.dwood, .025, 2.0, .35, 0, .95); bx(c.body, MT.gold, .3, .03, .03, .35, 1.75, .95); mk(G.wheel, c.body, MT.gold, .03, .2, .2, .35, 1.95, .95).rotation.y = PI / 2; bx(c.body, c.cm, .02, .3, .3, .35, 1.4, 1.1);
      elephant(c, 1.15, 1.4, -.9, .8, true);
      cy(c.body, MT.dstone, .22, .06, -.3, 0, 1.5); cn(c.body, MT.glow, .12, .25, -.3, .05, 1.5); c.chim.push(-.3, .4, 1.5);
      for (const a of [0, 2.1, 4.2]) { const o = cy(c.body, MT.dwood, .015, 1.2, -1.0 + Math.cos(a) * .12, 0, 1.55 + Math.sin(a) * .12); o.rotation.x = Math.sin(a) * -.12; o.rotation.z = Math.cos(a) * .12; }
      for (let i = 0; i < 3; i++) mk(G.wheel, c.body, i & 1 ? c.cm : MT.bronze, .04, .36, .36, -1.65 + i * .04, .2 + i * .02, 1.0 + i * .14);
      lmFlag(c, -1.65, 1.35, 2.0);
    },
  };
}
