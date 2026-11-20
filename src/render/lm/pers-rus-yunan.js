// Age-up building models (landmarks.js looks) of the Persians, the Russians and the Greeks. See index.js.
export default function (K) {
  const { THREE, PI, G, MT, XM, LMM, mat, mk, bx, cy, cn, py, sp, lmFlag, lmDome, lmGable, lmCols, lmCren, lmSteps, lmArch } = K;
  const M = {
    tq: mat(0x2f8fa0, .5), mudb: mat(0xc49a6a, .95), pst: mat(0xc9bda2, .9), pstD: mat(0x8f8572, .9),
    kred: mat(0xa8382a, .88), tgreen: mat(0x3f7a50, .7), pgreen: mat(0x74b49a, .8), roofg: mat(0x7d8c84, .6, .2), granite: mat(0x9a5446, .7),
    tent: mat(0xe6d3a2, .8), onR: mat(0xc0302a, .6), onG: mat(0x2f8a4a, .6), onB: mat(0x2f6fb8, .6), onY: mat(0xe2b23a, .6), aspen: mat(0xa9aca6, .8),
    bz: mat(0xb07a3a, .5, .3), rock: mat(0xa89c84, .95), cliff: mat(0x8c8374, .95), terra: mat(0xb5603a, .85), poly: mat(0xc8bca0, .9),
    horse: mat(0x6a4a30, .9), horse2: mat(0x3a2a20, .9), horseG: mat(0xb8b0a0, .9), purple: mat(0x6a2a7a, .8), fox: mat(0xc06a2a, .95), fish: mat(0x9aa4aa, .5, .2),
  };
  // an onion dome sitting on y: the bulb, the pointed tip, a gold finial with a cross bar; `belt` paints a band round its widest part
  const onion = (c, m, r, x, y, z, belt) => {
    sp(c.roof, m, r, x, y + r * 1.15, z).scale.y = r * 2.4;
    cn(c.roof, m, r * .5, r * 1.1, x, y + r * 1.95, z);
    cy(c.roof, MT.gold, .015, r * .6 + .12, x, y + r * 2.95, z); bx(c.roof, MT.gold, r * .4, .02, .02, x, y + r * 3.4 + .06, z);
    if (belt) cy(c.roof, belt, r * 1.04, r * .3, x, y + r, z);
  };
  // a Persian stepped merlon
  const merlon = (c, m, x, y, z, ry = 0) => { bx(c.body, m, .2, .1, .1, x, y, z).rotation.y = ry; bx(c.body, m, .1, .1, .1, x, y + .1, z).rotation.y = ry; };
  // a horse in its own group (head toward +z of the group): coat, a saddle cloth, a mail caparison with a steel face plate
  const horse = (c, x, z, ry, coat, cloth, armour) => {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; c.body.add(g);
    bx(g, coat, .22, .24, .62, 0, .34, 0);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, coat, .06, .34, .06, sx * .07, 0, sz * .24);
    bx(g, coat, .12, .34, .14, 0, .5, .27).rotation.x = .5; bx(g, coat, .1, .11, .26, 0, .76, .42);
    bx(g, XM.hair, .05, .3, .05, 0, .3, -.33).rotation.x = -.3;
    if (cloth) bx(g, cloth, .26, .1, .3, 0, .56, -.02);
    if (armour) { bx(g, armour, .27, .22, .66, 0, .26, 0); bx(g, MT.steel, .12, .08, .22, 0, .82, .44); }
    return g;
  };
  // a small standing figure (a soldier, an athlete): body, head, optional hat / helmet
  const figure = (c, x, z, body, head, hat, y = 0, ry = 0) => {
    bx(c.body, body, .15, .45, .1, x, y, z).rotation.y = ry; sp(c.body, head, .065, x, y + .52, z);
    if (hat) cy(c.body, hat, .07, .08, x, y + .55, z);
  };

  return {
    // ---- Persians ----
    persbahcesi(c) {   // chahar bagh: four quarters split by water channels, a pool in the middle, a tiled pavilion at the head
      const W = LMM.sand;
      bx(c.body, LMM.turf, 3.6, .06, 3.6, 0, 0, 0);
      for (const s of [-1, 1]) { bx(c.body, W, 3.75, .45, .15, 0, 0, s * 1.8); bx(c.body, W, .15, .45, 3.75, s * 1.8, 0, 0); }
      bx(c.body, LMM.marble, 3.4, .08, .36, 0, 0, .25); bx(c.body, LMM.water, 3.4, .03, .22, 0, .07, .25);
      bx(c.body, LMM.marble, .36, .08, 2.6, 0, 0, .45); bx(c.body, LMM.water, .22, .03, 2.6, 0, .07, .45);
      cy(c.body, LMM.marble, .48, .12, 0, 0, .25); cy(c.body, LMM.water, .4, .03, 0, .1, .25); cy(c.body, LMM.white, .04, .3, 0, .1, .25);
      for (const sx of [-1, 1]) for (const qz of [-.4, 1.05]) {
        const qx = sx * .95;
        cy(c.body, LMM.bark, .03, .15, qx + sx * .5, 0, qz); cn(c.body, LMM.pine, .14, 1.1, qx + sx * .5, .12, qz);
        cy(c.body, LMM.bark, .04, .35, qx - sx * .2, 0, qz); sp(c.body, MT.green, .28, qx - sx * .2, .58, qz);
        bx(c.body, MT.berry, .4, .07, .25, qx - sx * .2, 0, qz + .45);
      }
      bx(c.body, LMM.marble, 1.5, .2, .9, 0, 0, -1.35); bx(c.body, LMM.white, 1.2, .9, .8, 0, .2, -1.35);
      bx(c.body, M.tq, .6, .75, .04, 0, .2, -.94); bx(c.body, MT.black, .32, .55, .04, 0, .2, -.93); bx(c.body, c.cm, 1.22, .08, .82, 0, 1.0, -1.35);
      cy(c.body, LMM.white, .36, .2, 0, 1.1, -1.35); lmDome(c, M.tq, .38, 0, 1.3, -1.35, 1.2); sp(c.roof, MT.gold, .05, 0, 1.78, -1.35);
      lmFlag(c, 1.5, -1.4, 1.8);
    },
    olumsuzkisla(c) {   // the Immortals' barracks: a hall with a glazed archer frieze and stepped merlons, spears with golden apples
      const B = M.mudb;
      bx(c.body, B, 3.5, 1.3, 1.2, 0, 0, -1.2);
      bx(c.body, M.tq, 3.5, .34, .04, 0, .74, -.58);
      for (let i = 0; i < 9; i++) bx(c.body, i & 1 ? MT.gold : c.cm, .12, .24, .03, -1.5 + i * .375, .79, -.55);
      for (let i = 0; i < 9; i++) merlon(c, B, -1.5 + i * .375, 1.3, -.66);
      for (const x of [-1.1, 0, 1.1]) bx(c.body, MT.black, .36, .6, .04, x, 0, -.58);
      for (const s of [-1, 1]) { bx(c.body, B, .55, 1.75, .55, s * 1.6, 0, -1.2); merlon(c, B, s * 1.6, 1.75, -.98); }
      bx(c.body, MT.soil2, 3.4, .03, 2.0, 0, 0, .75);
      cy(c.body, MT.dwood, .04, .9, -1.5, 0, .3); cy(c.body, MT.dwood, .04, .9, -.3, 0, .3); bx(c.body, MT.dwood, 1.3, .05, .05, -.9, .8, .3);
      for (let i = 0; i < 5; i++) {
        const x = -1.35 + i * .25;
        cy(c.body, MT.dwood, .018, 1.9, x, 0, .45).rotation.x = -.2; sp(c.body, MT.gold, .045, x, .05, .45); cn(c.body, MT.steel, .03, .14, x, 1.86, .07).rotation.x = -.2;
      }
      for (let i = 0; i < 4; i++) bx(c.body, MT.thatch, .36, .65, .05, .35 + i * .42, 0, .5).rotation.x = -.15;
      for (const x of [-.45, .45]) { figure(c, x, -.35, c.cm, MT.skin, MT.gold); cy(c.body, MT.dwood, .015, 1.0, x + .12, 0, -.32); }
      cy(c.body, MT.dwood, .03, 2.6, 1.4, 0, 1.2); bx(c.body, LMM.goldm, .6, .12, .04, 1.4, 2.5, 1.2); sp(c.body, LMM.goldm, .08, 1.4, 2.56, 1.23);
      lmFlag(c, -1.6, 1.5, 1.9);
    },
    kralyolu(c) {   // a Royal Road relay station: a domed mud-brick inn with a tiled iwan, a stable shed, a courier on the road
      const Md = LMM.mud;
      bx(c.body, MT.stone, 3.8, .04, .7, 0, 0, 1.3); for (let i = 0; i < 6; i++) bx(c.body, MT.dstone, .04, .045, .7, -1.6 + i * .64, 0, 1.3);
      bx(c.body, Md, 2.2, 1.0, 1.6, -.6, 0, -.9); bx(c.body, LMM.sandD, 2.25, .1, 1.65, -.6, 1.0, -.9);
      for (const x of [-1.2, 0]) { lmDome(c, Md, .36, x, 1.1, -1.1, .9); sp(c.roof, MT.gold, .03, x, 1.45, -1.1); }
      bx(c.body, LMM.sandD, .9, 1.45, .3, -.6, 0, -.05); bx(c.body, M.tq, .6, 1.05, .03, -.6, .1, .11); bx(c.body, MT.black, .38, .8, .04, -.6, 0, .12); bx(c.body, c.cm, .92, .1, .32, -.6, 1.3, -.05);
      for (const [x, z] of [[.9, -1.4], [1.75, -1.4], [.9, -.2], [1.75, -.2]]) cy(c.body, MT.dwood, .04, .95, x, 0, z);
      bx(c.roof, MT.thatch, 1.1, .08, 1.4, 1.32, .95, -.8);
      horse(c, 1.1, -.8, 0, M.horse); horse(c, 1.55, -.8, 0, M.horseG);
      bx(c.body, MT.wood, .9, .2, .2, 1.32, 0, .15); bx(c.body, LMM.water, .8, .02, .14, 1.32, .19, .15);
      const g = horse(c, .3, 1.3, PI / 2, M.horse2, c.cm);
      bx(g, c.cm, .14, .26, .12, 0, .6, -.02); sp(g, MT.skin, .06, 0, .94, -.02); bx(g, MT.leather, .14, .1, .1, 0, .7, -.12);
      cy(c.body, MT.stone, .1, .55, 1.7, 0, .75); bx(c.body, MT.canvas, .3, .25, .3, -1.5, 0, .45); bx(c.body, MT.canvas, .25, .22, .25, -1.2, 0, .5);
      lmFlag(c, .55, .45, 2.0);
    },
    atestapinagi(c) {   // a chahar taq fire temple: four arched piers under a dome on a stepped platform, the eternal fire inside
      const S = M.pst, top = lmSteps(c, S, 3.2, 3.2, 3, .14, 0, 0, .3);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(c.body, S, .55, 1.4, .55, sx * .8, top, sz * .8);
      for (const s of [-1, 1]) { bx(c.body, S, 2.15, .35, .55, 0, top + 1.4, s * .8); bx(c.body, S, .55, .35, 2.15, s * .8, top + 1.4, 0); }
      cy(c.body, S, 1.0, .25, 0, top + 1.75, 0); lmDome(c, MT.plaster, 1.0, 0, top + 2.0, 0, .8); cy(c.roof, S, .2, .1, 0, top + 2.78, 0);
      cy(c.body, S, .22, .5, 0, top, 0); cy(c.body, S, .3, .1, 0, top + .5, 0); cn(c.body, MT.glow, .2, .45, 0, top + .6, 0); sp(c.body, MT.glow, .12, 0, top + .72, 0);
      c.chim.push(0, top + 2.95, 0);
      bx(c.body, LMM.goldm, .9, .1, .03, 0, top + 1.55, 1.09); sp(c.body, LMM.goldm, .07, 0, top + 1.6, 1.1); bx(c.body, LMM.goldm, .2, .12, .03, 0, top + 1.42, 1.09);
      bx(c.body, c.cm, 1.4, .06, .03, 0, top + 1.72, 1.09);
      for (const s of [-1, 1]) {
        cy(c.body, MT.dstone, .05, .5, s * 1.3, 0, 1.35); cy(c.body, MT.dstone, .16, .1, s * 1.3, .5, 1.35); cn(c.body, MT.glow, .12, .25, s * 1.3, .6, 1.35); c.chim.push(s * 1.3, .9, 1.35);
        cn(c.body, LMM.pine, .17, 1.3, s * 1.42, 0, -1.42);
      }
      lmFlag(c, -1.75, .4, 2.0);
    },
    persepolis(c) {   // the Apadana: a raised stone terrace, a double stair, a forest of slender columns with bull capitals
      const S = M.pst, D = M.pstD;
      bx(c.body, S, 3.6, .5, 3.0, 0, 0, -.35); bx(c.body, D, 3.6, .12, .03, 0, .2, 1.16);
      for (let i = 0; i < 4; i++) { const d = .6 - i * .15; bx(c.body, S, 1.4, .125, d, 0, i * .125, 1.15 + d / 2); }
      for (const s of [-1, 1]) { bx(c.body, D, .1, .5, .6, s * .75, 0, 1.45); bx(c.body, D, .32, .42, .6, s * .5, .5, .9); bx(c.body, D, .22, .2, .2, s * .5, .82, 1.25); }
      for (let i = 0; i < 5; i++) for (let j = 0; j < 4; j++) {
        const x = -1.3 + i * .65, z = -1.5 + j * .7;
        cy(c.body, S, .065, 2.0, x, .5, z); bx(c.body, D, .36, .12, .13, x, 2.5, z);
      }
      bx(c.roof, MT.dwood, 3.0, .1, 1.05, 0, 2.62, -1.15); bx(c.roof, c.cm, 3.0, .06, .03, 0, 2.62, -.62);
      for (let i = 0; i < 7; i++) bx(c.body, i & 1 ? LMM.goldm : M.tq, .1, .1, .02, -1.5 + i * .5, .3, 1.17);
      lmFlag(c, 1.6, 1.5, 2.0);
    },
    pasargad(c) {   // Cyrus' citadel: a stone platform, mud-brick walls and towers with stepped merlons, the stepped tomb of Cyrus
      const S = M.pst, B = M.mudb, top = lmSteps(c, S, 3.6, 2.8, 2, .25, 0, -.4, .2);
      bx(c.body, B, 3.0, .9, .25, 0, top, .75); bx(c.body, B, 3.0, .9, .25, 0, top, -1.55);
      for (const s of [-1, 1]) bx(c.body, B, .25, .9, 2.3, s * 1.48, top, -.4);
      for (const x of [-1.5, 1.5]) for (const z of [-1.55, .75]) { bx(c.body, B, .6, 2.1, .6, x, 0, z); merlon(c, B, x, 2.1, z); bx(c.body, MT.black, .08, .3, .04, x, 1.4, z + .31); }
      for (let i = 0; i < 6; i++) { const x = -1.05 + i * .42; if (Math.abs(x) < .3) continue; merlon(c, B, x, top + .9, .75); merlon(c, B, x, top + .9, -1.55); }
      for (let i = 0; i < 4; i++) for (const s of [-1, 1]) merlon(c, B, s * 1.48, top + .9, -1.15 + i * .5, PI / 2);
      for (const s of [-1, 1]) bx(c.body, B, .4, 1.8, .45, s * .38, 0, .85);
      bx(c.body, MT.black, .36, .75, .04, 0, top, .89); bx(c.body, c.cm, .4, .1, .04, 0, top + .8, .9);
      bx(c.body, B, .95, 1.4, .95, .6, top, -.8); for (let i = 0; i < 3; i++) merlon(c, B, .35 + i * .25, top + 1.4, -.35);
      bx(c.body, S, 1.3, .8, .8, -.55, top, -.8); lmCols(c, 4, -1.05, -.05, -.3, .8, S, .05, top);
      const t = lmSteps(c, S, 1.0, .8, 5, .1, -1.1, 1.45, .12);
      bx(c.body, S, .42, .32, .36, -1.1, t, 1.45); lmGable(c, S, .5, .2, .44, -1.1, t + .32, 1.45); bx(c.body, MT.black, .14, .2, .02, -1.1, t, 1.64);
      lmFlag(c, 1.2, 1.5, 2.0);
    },
    kanat(c) {   // qanat: a row of shaft mounds from the mountain to a domed cistern with wind catchers, a channel to the fields
      const So = MT.soil2, Md = LMM.mud;
      cn(c.body, M.cliff, .8, 1.3, -1.1, 0, -1.15); cn(c.body, LMM.white, .3, .48, -1.1, .82, -1.15);
      for (let i = 0; i < 6; i++) { const x = -.45 + i * .25, z = -.5 + i * .17; lmDome(c, So, .2, x, 0, z, .6); cy(c.body, MT.black, .06, .02, x, .1, z); }
      for (const s of [-1, 1]) cy(c.body, MT.dwood, .025, .45, .05 + s * .2, 0, -.16); cy(c.body, MT.dwood, .03, .45, -.15, .42, -.16).rotation.z = -PI / 2;
      cy(c.body, Md, .55, .45, .9, 0, .55); lmDome(c, Md, .55, .9, .45, .55, 1.3); sp(c.roof, Md, .06, .9, 1.18, .55);
      for (const [x, z] of [[.9, -.25], [1.65, .55], [.1, .4]]) {
        bx(c.body, Md, .26, 1.9, .26, x, 0, z); bx(c.body, MT.black, .3, .38, .1, x, 1.35, z); bx(c.body, MT.black, .1, .38, .3, x, 1.35, z); bx(c.body, LMM.sandD, .32, .06, .32, x, 1.9, z);
      }
      bx(c.body, LMM.sandD, .5, .6, .25, .9, 0, 1.15); bx(c.body, MT.black, .26, .42, .04, .9, 0, 1.28); bx(c.body, c.cm, .52, .08, .27, .9, .55, 1.15);
      bx(c.body, MT.stone, 1.9, .05, .22, -.2, 0, 1.45); bx(c.body, LMM.water, 1.9, .02, .12, -.2, .04, 1.45);
      for (let i = 0; i < 4; i++) bx(c.body, i & 1 ? MT.green : MT.wheat, .9, .12, .14, -1.3, 0, .4 + i * .24);
      cy(c.body, LMM.bark, .04, .3, -1.6, 0, 1.6); sp(c.body, MT.dgreen, .22, -1.6, .45, 1.6);
      lmFlag(c, 1.65, -1.3, 1.8);
    },
    savaranahir(c) {   // the Savaran stables: an arched mud-brick stable, armoured horses in a paddock, lances and the Derafsh Kaviani
      const B = M.mudb;
      bx(c.body, B, 3.4, 1.0, 1.0, 0, 0, -1.35); bx(c.body, LMM.sandD, 3.5, .12, 1.1, 0, 1.0, -1.35);
      for (let i = 0; i < 5; i++) { const x = -1.3 + i * .65; bx(c.body, MT.black, .42, .65, .04, x, 0, -.84); if (i & 1) bx(c.body, M.horse, .1, .12, .25, x, .45, -.75); }
      for (let i = 0; i < 6; i++) merlon(c, B, -1.45 + i * .58, 1.12, -.9);
      for (let i = 0; i < 6; i++) cy(c.body, MT.dwood, .03, .55, -1.6 + i * .64, 0, 1.6);
      for (const y of [.28, .48]) { bx(c.body, MT.lwood, 3.3, .04, .04, 0, y, 1.6); for (const s of [-1, 1]) bx(c.body, MT.lwood, .04, .04, 2.3, s * 1.62, y, .45); }
      horse(c, -.55, .55, .5, M.horse2, c.cm, XM.mail); horse(c, .35, .75, -.3, M.horse, c.cm, XM.mail);
      for (let i = 0; i < 5; i++) {
        const x = .85 + i * .17; cy(c.body, MT.dwood, .016, 2.1, x, 0, -.55).rotation.x = -.15; bx(c.body, c.cm, .01, .12, .22, x, 1.85, -.75);
        cn(c.body, MT.steel, .025, .14, x, 2.07, -.86).rotation.x = -.15;
      }
      lmDome(c, MT.hay, .32, -1.35, 0, .9, .7); bx(c.body, MT.wood, .7, .2, .2, 1.1, 0, .2); bx(c.body, LMM.water, .6, .02, .14, 1.1, .19, .2);
      cy(c.body, MT.dwood, .035, 2.8, -1.35, 0, -.3); bx(c.body, MT.gold, .7, .04, .04, -1.35, 2.6, -.28);
      bx(c.body, M.purple, .6, .8, .02, -1.35, 1.8, -.26); mk(G.cbox, c.body, LMM.goldm, .22, .22, .03, -1.35, 2.2, -.25).rotation.z = PI / 4; mk(G.cbox, c.body, LMM.goldm, .22, .22, .03, -1.35, 2.2, -.25);
      for (let i = 0; i < 3; i++) bx(c.body, c.cm, .05, .3, .02, -1.55 + i * .2, 1.5, -.26);
      lmFlag(c, 1.7, -.3, 1.9);
    },
    // ---- Russians ----
    kurkpazari(c) {   // the fur traders' house: a two-storey log terem with white carved windows, pelts on a rack, logs and a sledge
      const L = MT.wood;
      bx(c.body, L, 2.0, 1.6, 1.4, -.6, 0, -1.0);
      for (let i = 0; i < 7; i++) cy(c.body, MT.dwood, .04, 2.04, -1.62, .12 + i * .22, -.29).rotation.z = -PI / 2;
      for (const x of [-1.15, -.6, -.05]) { bx(c.body, LMM.white, .32, .38, .03, x, .95, -.29); bx(c.body, MT.glow, .18, .22, .04, x, 1.03, -.28); }
      bx(c.body, MT.black, .36, .65, .04, -.6, 0, -.28);
      lmGable(c, MT.dwood, 2.3, .95, 1.6, -.6, 1.6, -1.0); bx(c.body, LMM.white, .08, .5, .04, -.6, 1.7, -.18);
      bx(c.body, MT.brick, .2, .8, .2, -1.1, 1.6, -1.3); c.chim.push(-1.1, 2.5, -1.3);
      cy(c.body, MT.dwood, .04, 1.2, .4, 0, .7); cy(c.body, MT.dwood, .04, 1.2, 1.7, 0, .7); bx(c.body, MT.dwood, 1.35, .05, .05, 1.05, 1.12, .7);
      [XM.fur, LMM.white, M.fox, XM.hide].forEach((m, i) => bx(c.body, m, .26, .5, .03, .58 + i * .32, .58, .7));
      for (let r = 0; r < 3; r++) for (let i = 0; i < 3 - r; i++) cy(c.body, LMM.bark, .1, 1.0, -1.45 + r * .1 + i * .21, .1 + r * .17, .3).rotation.x = PI / 2;
      for (const s of [-1, 1]) bx(c.body, MT.dwood, .04, .06, .95, -.1 + s * .2, 0, 1.3); bx(c.body, L, .44, .08, .7, -.1, .08, 1.3); bx(c.body, XM.fur, .34, .2, .4, -.1, .16, 1.3);
      cy(c.body, L, .15, .35, 1.3, 0, -.2); cy(c.body, L, .15, .35, 1.65, 0, -.45); bx(c.body, MT.lwood, .8, .4, .4, 1.1, 0, -1.2); bx(c.body, c.cm, .84, .06, .42, 1.1, .4, -1.2);
      lmFlag(c, 1.7, -1.6, 2.0);
    },
    ahsapkremlin(c) {   // a wooden kremlin: log crib walls under a covered walk, corner towers with tent roofs, a gate tower, a log church
      const L = MT.wood, D = MT.dwood;
      bx(c.body, MT.soil2, 3.8, .15, 3.8, 0, 0, 0);
      for (const s of [-1, 1]) { bx(c.body, L, 3.0, .95, .3, 0, .15, s * 1.5); bx(c.body, L, .3, .95, 3.0, s * 1.5, .15, 0); }
      for (const y of [.45, .75]) { bx(c.body, D, 3.0, .03, .32, 0, y, 1.5); bx(c.body, D, .32, .03, 3.0, 1.5, y, 0); bx(c.body, D, .32, .03, 3.0, -1.5, y, 0); }
      for (const s of [-1, 1]) { lmGable(c, D, .5, .3, 3.0, s * 1.5, 1.1, 0); lmGable(c, D, .5, .3, 3.0, 0, 1.1, s * 1.5, PI / 2); }
      for (const x of [-1.5, 1.5]) for (const z of [-1.5, 1.5]) {
        bx(c.body, L, .65, 1.5, .65, x, 0, z); bx(c.body, L, .78, .3, .78, x, 1.5, z); py(c.roof, D, .9, 1.0, .9, x, 1.8, z); cy(c.roof, D, .02, .3, x, 2.75, z);
      }
      bx(c.body, L, .8, 1.8, .8, 0, 0, 1.5); bx(c.body, L, .92, .3, .92, 0, 1.8, 1.5); py(c.roof, D, 1.05, 1.1, 1.05, 0, 2.1, 1.5); sp(c.roof, M.aspen, .1, 0, 3.2, 1.5);
      bx(c.body, MT.black, .4, .7, .04, 0, 0, 1.9); bx(c.body, LMM.goldm, .18, .22, .02, 0, 1.2, 1.91); for (const s of [-1, 1]) bx(c.body, MT.black, .06, .2, .02, s * .25, 1.88, 1.97);
      bx(c.body, MT.lwood, .8, .9, .8, -.5, 0, -.5); lmGable(c, D, .9, .4, .9, -.5, .9, -.5); cy(c.body, MT.lwood, .2, .5, -.5, 1.05, -.5); onion(c, M.aspen, .24, -.5, 1.55, -.5);
      bx(c.body, L, .9, .7, .8, .6, 0, -.6); lmGable(c, D, 1.0, .5, .9, .6, .7, -.6, PI / 2); c.chim.push(.75, 1.3, -.6);
      lmFlag(c, .9, .7, 2.0);
    },
    novgorod(c) {   // St Sophia of Novgorod: a white cube with arched gables and apses, five golden onions, a stair tower, a bell wall
      const W = LMM.white;
      bx(c.body, MT.stone, 2.6, .15, 2.4, -.2, 0, -.4); bx(c.body, W, 2.2, 1.7, 2.0, -.2, .15, -.4);
      for (const i of [-1, 0, 1]) {
        mk(G.wheel, c.body, W, .1, .72, .72, -.2 + i * .73, 1.85, .57).rotation.y = PI / 2;
        mk(G.wheel, c.body, W, .1, .66, .66, .87, 1.85, -.4 + i * .66);
        cy(c.body, W, .3, 1.3, -.2 + i * .62, .15, -1.4);
        bx(c.body, MT.black, .08, .35, .04, -.2 + i * .62, 1.05, .61);
      }
      bx(c.roof, LMM.lead, 2.1, .15, 1.9, -.2, 1.85, -.4);
      cy(c.body, W, .38, .7, -.2, 2.0, -.4); onion(c, LMM.goldm, .42, -.2, 2.7, -.4);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) { cy(c.body, W, .24, .45, -.2 + sx * .62, 2.0, -.4 + sz * .58); onion(c, LMM.goldm, .27, -.2 + sx * .62, 2.45, -.4 + sz * .58); }
      cy(c.body, W, .3, 2.3, -1.35, 0, .45); onion(c, LMM.goldm, .3, -1.35, 2.3, .45);
      bx(c.body, MT.black, .4, .65, .04, -.2, .15, .61); bx(c.body, MT.bronze, .44, .62, .03, -.2, .15, .63);
      bx(c.body, W, 1.0, 1.6, .35, 1.35, 0, .9); for (let i = 0; i < 3; i++) { const x = 1.05 + i * .3; bx(c.body, MT.black, .18, .35, .04, x, 1.0, 1.07); sp(c.body, MT.gold, .06, x, 1.15, 1.04); }
      lmGable(c, LMM.lead, .4, .2, 1.05, 1.35, 1.6, .9, PI / 2); onion(c, LMM.goldm, .15, 1.35, 1.72, .9);
      lmFlag(c, 1.6, -1.5, 2.0);
    },
    kremlin(c) {   // the Moscow Kremlin: red brick walls with swallowtail merlons, green tent-roofed towers, the Spasskaya, golden domes behind
      const R = M.kred, Gr = M.tgreen, W = LMM.white;
      bx(c.body, R, 3.0, 1.0, .28, 0, 0, 1.45); bx(c.body, R, 3.0, 1.0, .28, 0, 0, -1.35);
      for (const s of [-1, 1]) bx(c.body, R, .28, 1.0, 2.8, s * 1.5, 0, .05);
      for (let i = 0; i < 10; i++) { const x = -1.35 + i * .3; if (Math.abs(x) < .35) continue; for (const d of [-.04, .04]) bx(c.body, R, .06, .24, .1, x + d, 1.0, 1.45); }
      for (let i = 0; i < 7; i++) for (const s of [-1, 1]) bx(c.body, R, .1, .2, .12, s * 1.5, 1.0, -1.05 + i * .38);
      for (let i = 0; i < 7; i++) bx(c.body, R, .12, .2, .1, -1.2 + i * .4, 1.0, -1.35);
      for (const x of [-1.5, 1.5]) for (const z of [-1.35, 1.45]) { cy(c.body, R, .32, 1.6, x, 0, z); cy(c.body, R, .36, .12, x, 1.5, z); cn(c.roof, Gr, .36, 1.0, x, 1.62, z); sp(c.roof, MT.gold, .04, x, 2.62, z); }
      bx(c.body, R, .6, 1.7, .6, 0, 0, 1.45); bx(c.body, W, .5, .45, .5, 0, 1.7, 1.45); bx(c.body, R, .4, .5, .4, 0, 2.15, 1.45); cy(c.body, R, .2, .3, 0, 2.65, 1.45);
      cn(c.roof, Gr, .24, .9, 0, 2.95, 1.45); sp(c.roof, LMM.goldm, .07, 0, 3.88, 1.45);
      mk(G.wheel, c.body, LMM.blue, .04, .32, .32, 0, 1.92, 1.72).rotation.y = PI / 2; bx(c.body, MT.gold, .02, .13, .02, 0, 1.92, 1.75);
      bx(c.body, MT.black, .3, .55, .04, 0, 0, 1.76); bx(c.body, c.cm, .62, .08, .62, 0, 1.6, 1.45);
      bx(c.body, W, 1.1, 1.0, .9, -.55, 0, -.45); cy(c.body, W, .2, .35, -.55, 1.0, -.45); onion(c, LMM.goldm, .24, -.55, 1.35, -.45);
      for (const sx of [-1, 1]) for (const sz of [-1, 1]) { cy(c.body, W, .13, .25, -.55 + sx * .32, 1.0, -.45 + sz * .25); onion(c, LMM.goldm, .16, -.55 + sx * .32, 1.25, -.45 + sz * .25); }
      cy(c.body, W, .32, 1.2, .65, 0, -.6); cy(c.body, W, .26, .9, .65, 1.2, -.6); cy(c.body, W, .2, .6, .65, 2.1, -.6);
      bx(c.body, MT.black, .14, .3, .04, .65, .75, -.27); bx(c.body, MT.black, .12, .3, .04, .65, 1.7, -.33); onion(c, LMM.goldm, .24, .65, 2.7, -.6);
      lmFlag(c, 1.0, .6, 2.2);
    },
    volgaliman(c) {   // the Volga port: a log warehouse, a timber quay and pier, a river boat with a square sail, a crane, drying fish
      bx(c.body, LMM.water, 3.8, .03, 1.5, 0, 0, 1.2); bx(c.body, MT.dwood, 3.8, .2, .2, 0, 0, .4);
      bx(c.body, MT.lwood, .6, .1, 1.3, 1.0, .15, 1.05); for (const x of [.75, 1.25]) for (const z of [.6, 1.6]) cy(c.body, MT.dwood, .04, .25, x, 0, z);
      const b = new THREE.Group(); b.position.set(-.55, 0, 1.3); b.rotation.y = PI / 2; c.body.add(b);
      bx(b, MT.dwood, .45, .2, 1.5, 0, .03, 0); bx(b, MT.wood, .32, .08, 1.3, 0, .2, 0);
      for (const s of [-1, 1]) bx(b, MT.dwood, .12, .4, .12, 0, .1, s * .76).rotation.x = s * .4;
      cy(b, MT.wood, .03, 1.3, 0, .2, 0); bx(b, MT.white, .9, .7, .02, 0, .65, .03); bx(b, c.cm, .9, .1, .03, 0, .95, .03);
      bx(b, MT.canvas, .25, .2, .3, 0, .2, -.45); bx(b, MT.canvas, .22, .18, .25, 0, .2, .45);
      bx(c.body, MT.wood, 2.0, 1.0, 1.2, -.7, 0, -.9); for (const y of [.25, .5, .75]) bx(c.body, MT.dwood, 2.02, .03, 1.22, -.7, y, -.9);
      lmGable(c, MT.dwood, 1.4, .7, 2.2, -.7, 1.0, -.9, PI / 2); bx(c.body, MT.black, .5, .6, .04, -.7, 0, -.29);
      cy(c.body, MT.dwood, .07, 1.6, 1.3, 0, -.3); bx(c.body, MT.dwood, .06, .06, 1.2, 1.3, 1.5, .3); cy(c.body, MT.black, .01, .8, 1.3, .7, .85); bx(c.body, MT.wood, .25, .25, .25, 1.3, .45, .85);
      for (const x of [.35, .85]) cy(c.body, MT.dwood, .03, .8, x, 0, .02); bx(c.body, MT.dwood, .55, .04, .04, .6, .76, .02);
      for (let i = 0; i < 4; i++) bx(c.body, M.fish, .04, .2, .06, .4 + i * .13, .52, .02);
      for (const [x, y] of [[-1.5, .1], [-1.25, .1], [-1.38, .32]]) sp(c.body, MT.canvas, .14, x, y, .05);
      cy(c.body, MT.wood, .14, .35, -.3, 0, .05); cy(c.body, MT.wood, .14, .35, 0, 0, .1);
      lmFlag(c, 1.65, -1.5, 2.0);
    },
    topdokum(c) {   // the Moscow cannon yard: a brick foundry under a tent-roofed tower, the Tsar Cannon with its balls, the Tsar Bell
      const Bz = M.bz;
      bx(c.body, MT.dstone, 3.6, .04, 3.6, 0, 0, 0);
      bx(c.body, MT.brick, 2.6, 1.2, 1.2, -.5, 0, -1.2); lmGable(c, LMM.dtile, 1.4, .6, 2.7, -.5, 1.2, -1.2, PI / 2);
      for (const x of [-1.2, .2]) bx(c.body, MT.glow, .36, .5, .04, x, 0, -.58); for (let i = 0; i < 4; i++) bx(c.body, MT.glow, .14, .18, .04, -1.5 + i * .65, .75, -.58);
      for (const x of [-1.5, .1]) { cy(c.body, MT.brick, .15, 2.6, x, 0, -1.55); c.chim.push(x, 2.7, -1.55); }
      bx(c.body, MT.brick, .8, 1.9, .8, 1.3, 0, -1.2); bx(c.body, LMM.white, .84, .08, .84, 1.3, 1.5, -1.2); py(c.roof, M.tgreen, 1.0, 1.1, 1.0, 1.3, 1.9, -1.2); sp(c.roof, MT.gold, .05, 1.3, 3.0, -1.2);
      bx(c.body, MT.black, .3, .55, .04, 1.3, 0, -.79);
      cy(c.body, MT.dstone, .32, .06, -1.2, 0, -.2); cy(c.body, MT.glow, .25, .03, -1.2, .05, -.2);
      bx(c.body, Bz, .7, .45, 1.2, 0, 0, .55); bx(c.body, c.cm, .72, .06, 1.22, 0, .45, .55);
      for (const s of [-1, 1]) mk(G.wheel, c.body, Bz, .12, .8, .8, s * .42, .4, .4);
      cy(c.body, Bz, .3, 1.9, 0, .72, -.2).rotation.x = PI / 2; cy(c.body, Bz, .36, .14, 0, .72, 1.5).rotation.x = PI / 2; cy(c.body, Bz, .34, .16, 0, .72, -.2).rotation.x = PI / 2;
      cy(c.body, MT.black, .18, .02, 0, .72, 1.64).rotation.x = PI / 2; sp(c.body, Bz, .15, 0, .72, -.3);
      for (const [x, y, z] of [[1.1, .2, 1.2], [1.5, .2, 1.2], [1.3, .2, 1.55], [1.3, .5, 1.32]]) sp(c.body, MT.iron, .2, x, y, z);
      bx(c.body, MT.stone, .9, .15, .9, -1.2, 0, 1.2); cy(c.body, Bz, .36, .22, -1.2, .15, 1.2); cn(c.body, Bz, .34, .62, -1.2, .35, 1.2); sp(c.body, Bz, .1, -1.2, .95, 1.2);
      bx(c.body, Bz, .3, .32, .08, -.7, .15, 1.45).rotation.z = .4;
      lmFlag(c, 1.7, .3, 2.0);
    },
    kislaksaray(c) {   // the Winter Palace: a long mint-green and white baroque front on the Neva, statues on the roof, the Alexander Column
      const Gr = M.pgreen, W = LMM.white;
      bx(c.body, LMM.water, 3.8, .03, .4, 0, 0, -1.75);
      bx(c.body, Gr, 3.6, 1.25, 1.0, 0, 0, -1.0); bx(c.body, Gr, 1.1, 1.5, 1.2, 0, 0, -.95);
      for (const s of [-1, 1]) bx(c.body, Gr, .6, 1.4, 1.15, s * 1.5, 0, -.95);
      bx(c.roof, M.roofg, 3.62, .08, 1.02, 0, 1.25, -1.0); bx(c.roof, M.roofg, 1.12, .08, 1.22, 0, 1.5, -.95);
      for (const s of [-1, 1]) bx(c.roof, M.roofg, .62, .08, 1.17, s * 1.5, 1.4, -.95);
      lmCols(c, 4, -.45, .45, -.32, 1.45, W, .045);
      for (const s of [-1, 1]) { lmCols(c, 3, s * .7, s * 1.1, -.47, 1.2, W, .04); lmCols(c, 3, s * 1.3, s * 1.7, -.35, 1.35, W, .04); }
      for (const x of [-1.0, -.8, .8, 1.0]) for (const y of [.25, .8]) bx(c.body, MT.glass, .12, .26, .03, x, y, -.49);
      bx(c.body, MT.gold, 3.6, .05, .02, 0, 1.17, -.5); bx(c.body, MT.gold, .4, .6, .03, 0, 0, -.34);
      for (let i = 0; i < 11; i++) { const x = -1.6 + i * .32; if (Math.abs(x) < .6) continue; if (i & 1) sp(c.body, MT.gold, .04, x, 1.38, -.55); else cy(c.body, W, .035, .2, x, 1.33, -.55); }
      for (let i = 0; i < 5; i++) cy(c.body, W, .035, .2, -.44 + i * .22, 1.58, -.4);
      bx(c.body, MT.stone, 3.6, .03, 1.5, 0, 0, .95);
      bx(c.body, M.granite, .42, .42, .42, 0, 0, .95); cy(c.body, M.granite, .11, 2.5, 0, .42, .95); bx(c.body, M.bz, .26, .1, .26, 0, 2.92, .95);
      cy(c.body, LMM.goldm, .05, .3, 0, 3.02, .95); sp(c.body, LMM.goldm, .05, 0, 3.38, .95); bx(c.body, LMM.goldm, .02, .34, .02, 0, 3.2, .99); bx(c.body, LMM.goldm, .26, .12, .02, 0, 3.15, .92);
      cy(c.body, MT.dwood, .02, .6, 0, 1.58, -1.05); bx(c.body, c.cm, .02, .22, .34, 0, 1.92, -.88);
      lmFlag(c, 1.3, .9, 1.9);
    },
    aziz_basil(c) {   // St Basil's: a cluster of towers round a tall tent, each under a different coloured, banded onion dome
      const Br = MT.brick, W = LMM.white;
      bx(c.body, Br, 3.0, .45, 3.0, 0, 0, 0); bx(c.body, W, 3.04, .06, 3.04, 0, .4, 0); bx(c.body, Br, 2.0, .5, 2.0, 0, .45, 0);
      bx(c.body, Br, .7, 1.0, .7, 0, .95, 0); cy(c.body, Br, .38, .7, 0, 1.95, 0); cn(c.roof, M.tent, .4, 1.3, 0, 2.65, 0);
      cy(c.roof, M.onG, .31, .06, 0, 2.95, 0); cy(c.roof, M.onG, .22, .06, 0, 3.35, 0); onion(c, LMM.goldm, .13, 0, 3.92, 0);
      const big = [[0, .95, M.onR, M.onG], [0, -.95, M.onG, M.onY], [-.95, 0, M.onB, W], [.95, 0, M.onY, M.onG]];
      for (const [x, z, m, b] of big) { cy(c.body, Br, .3, 1.3, x, .45, z); cy(c.body, W, .33, .08, x, 1.6, z); cy(c.body, Br, .2, .3, x, 1.75, z); onion(c, m, .33, x, 2.05, z, b); }
      const small = [[-.78, .78, M.onG, M.onR], [.78, .78, M.onB, M.onY], [-.78, -.78, LMM.goldm, M.onG], [.78, -.78, M.onR, W]];
      for (const [x, z, m, b] of small) { cy(c.body, Br, .2, .9, x, .45, z); cy(c.body, W, .22, .06, x, 1.25, z); cy(c.body, Br, .14, .2, x, 1.35, z); onion(c, m, .22, x, 1.55, z, b); }
      bx(c.body, MT.black, .2, .45, .04, 0, .45, 1.25); bx(c.body, Br, .7, .22, .4, 0, 0, 1.7);
      bx(c.body, Br, .45, 1.6, .45, 1.55, 0, -1.5); bx(c.body, MT.black, .2, .3, .04, 1.55, 1.15, -1.27); cn(c.roof, M.onG, .26, .7, 1.55, 1.6, -1.5); onion(c, LMM.goldm, .1, 1.55, 2.28, -1.5);
      bx(c.body, c.cm, 2.02, .08, 2.02, 0, .9, 0);
      lmFlag(c, -1.65, 1.4, 1.8);
    },
    // ---- Greeks ----
    agora(c) {   // the agora: a paved square between two stoas, market stalls under awnings, amphorae, a statue
      const W = LMM.marble;
      bx(c.body, MT.stone, 3.7, .06, 3.7, 0, 0, 0);
      bx(c.body, W, 3.5, .1, .85, 0, .06, -1.3); bx(c.body, W, 3.4, 1.0, .12, 0, .16, -1.66);
      lmCols(c, 9, -1.6, 1.6, -.98, 1.0, W, .06, .16); bx(c.body, W, 3.5, .14, .85, 0, 1.16, -1.3); lmGable(c, MT.tile, .95, .3, 3.6, 0, 1.3, -1.3, PI / 2);
      for (let i = 0; i < 4; i++) bx(c.body, MT.black, .25, .5, .02, -1.2 + i * .8, .16, -1.59);
      bx(c.body, W, .85, .1, 2.35, -1.3, .06, .42); bx(c.body, W, .12, 1.0, 2.3, -1.66, .16, .42);
      lmCols(c, 7, -.7, 1.5, -.98, 1.0, W, .06, .16, true); bx(c.body, W, .85, .14, 2.35, -1.3, 1.16, .42); lmGable(c, MT.tile, .95, .3, 2.45, -1.3, 1.3, .42);
      for (const [x, z, i] of [[.5, .2, 0], [1.3, .2, 1], [.9, 1.25, 2]]) {
        bx(c.body, MT.wood, .6, .35, .35, x, .06, z); for (const s of [-1, 1]) cy(c.body, MT.dwood, .02, .75, x + s * .3, .06, z + .2);
        bx(c.roof, i === 1 ? c.cm : MT.canvas, .72, .03, .5, x, .8, z + .05).rotation.x = .2;
      }
      for (const [x, z] of [[.2, .65], [.35, .75], [1.65, .7], [1.5, 1.6]]) { cy(c.body, M.terra, .07, .25, x, .06, z); sp(c.body, M.terra, .06, x, .33, z); }
      bx(c.body, W, .45, .5, .45, -.15, .06, .55); bx(c.body, M.bz, .15, .5, .12, -.15, .56, .55); sp(c.body, M.bz, .07, -.15, 1.13, .55);
      lmFlag(c, 1.7, -.6, 2.0);
    },
    gymnasion(c) {   // the gymnasion: a sanded court inside a four-sided colonnade, wrestlers and a discus thrower, a running track
      const W = LMM.marble;
      bx(c.body, LMM.sand, 3.4, .05, 2.4, 0, 0, -.6); bx(c.body, W, 3.4, .9, .12, 0, 0, -1.74);
      lmCols(c, 8, -1.6, 1.6, .5, .9, W, .055); lmCols(c, 8, -1.6, 1.6, -1.45, .9, W, .055);
      for (const s of [-1, 1]) lmCols(c, 3, -1.0, .1, s * 1.6, .9, W, .055, 0, true);
      bx(c.roof, MT.tile, 3.5, .1, .42, 0, .9, .45); bx(c.roof, MT.tile, 3.5, .1, .5, 0, .9, -1.55);
      for (const s of [-1, 1]) bx(c.roof, MT.tile, .45, .1, 1.5, s * 1.55, .9, -.55);
      lmGable(c, W, .9, .3, .5, 0, 1.0, .45);
      bx(c.body, LMM.sandD, 1.0, .03, .8, -.5, .05, -.5); figure(c, -.62, -.5, MT.skin, MT.skin, null, .05, .3); figure(c, -.4, -.45, MT.skin, MT.skin, null, .05, -.3);
      bx(c.body, W, .3, .3, .3, .7, .05, -.6); bx(c.body, W, .12, .38, .1, .7, .35, -.6); sp(c.body, W, .06, .7, .8, -.6); mk(G.wheel, c.body, M.bz, .03, .14, .14, .8, .55, -.6);
      bx(c.body, LMM.sandD, 3.6, .03, .6, 0, 0, 1.3); bx(c.body, W, .06, .04, .6, -1.5, 0, 1.3); cy(c.body, W, .05, .5, 1.55, 0, 1.3);
      figure(c, -.3, 1.2, MT.skin, MT.skin); figure(c, .25, 1.42, MT.skin, MT.skin); bx(c.body, c.cm, .16, .1, .11, -.3, .15, 1.2); bx(c.body, c.cm, .16, .1, .11, .25, .15, 1.42);
      lmFlag(c, -1.75, .85, 1.9);
    },
    delfi(c) {   // Delphi: terraces under grey cliffs, Apollo's temple and altar, the theatre above, the round tholos below
      const R = M.rock, W = LMM.marble;
      bx(c.body, R, 3.8, .15, 3.8, 0, 0, 0); bx(c.body, R, 3.8, .45, 1.9, 0, 0, -.95); bx(c.body, M.poly, 3.8, .3, .04, 0, .15, .01);
      mk(G.rock, c.body, M.cliff, 1.3, 1.4, .7, 1.1, .55, -1.6); mk(G.rock, c.body, M.cliff, .9, 1.0, .6, -1.5, .7, -1.65);
      bx(c.body, W, 1.6, .1, 1.0, .7, .45, -.75); bx(c.body, W, 1.0, .6, .5, .7, .55, -.75);
      lmCols(c, 6, .05, 1.35, -.3, .65, W, .045, .55); lmCols(c, 6, .05, 1.35, -1.2, .65, W, .045, .55);
      bx(c.body, W, 1.5, .1, .98, .7, 1.2, -.75); lmGable(c, MT.tile, 1.0, .3, 1.55, .7, 1.3, -.75, PI / 2);
      bx(c.body, MT.dstone, .45, .3, .25, .4, .45, -.12); bx(c.body, MT.glow, .3, .04, .15, .4, .75, -.12); c.chim.push(.4, .9, -.12);
      for (let r = 0; r < 3; r++) {
        const R0 = .55 + r * .23, n = 5 + r;
        for (let i = 0; i < n; i++) { const a = PI * (.25 + .65 * i / (n - 1)); bx(c.body, W, .28, .15 * (r + 1), .2, -.9 + Math.cos(a) * R0, .45, -.45 - Math.sin(a) * R0).rotation.y = a + PI / 2; }
      }
      cy(c.body, W, .3, .02, -.9, .45, -.45);
      cy(c.body, W, .72, .1, -.8, .15, 1.0); cy(c.body, W, .42, .8, -.8, .25, 1.0);
      for (let i = 0; i < 10; i++) { const a = i / 10 * PI * 2; cy(c.body, W, .045, .8, -.8 + Math.cos(a) * .6, .25, 1.0 + Math.sin(a) * .6); }
      cy(c.body, W, .68, .1, -.8, 1.05, 1.0); cn(c.roof, MT.tile, .66, .35, -.8, 1.15, 1.0);
      lmDome(c, W, .14, .45, .15, .95, 1.3); bx(c.body, MT.stone, .3, .02, 1.5, .55, .15, 1.0);
      cy(c.body, M.bz, .05, .9, 1.1, .15, .85); cy(c.body, MT.gold, .16, .08, 1.1, 1.05, .85);
      lmFlag(c, 1.7, 1.4, 1.9);
    },
    akropolsur(c) {   // the Acropolis walls: a rock with sheer walls, the Propylaea at the top of the stair, the Nike bastion, Athena's statue
      const R = M.rock, S = MT.stone, W = LMM.marble;
      bx(c.body, R, 3.2, .9, 2.6, 0, 0, -.5);
      for (const [x, z] of [[-1.4, .65], [1.4, .7], [-1.4, -1.55], [1.4, -1.5]]) mk(G.rock, c.body, R, 1.0, .8, .8, x, .25, z);
      bx(c.body, S, 3.3, 1.35, .25, 0, 0, -1.8); for (const s of [-1, 1]) { bx(c.body, S, .25, 1.35, 2.7, s * 1.62, 0, -.5); bx(c.body, S, 1.25, 1.35, .25, s * 1.0, 0, .8); }
      for (let i = 0; i < 8; i++) bx(c.body, S, .14, .14, .27, -1.4 + i * .4, 1.35, -1.8);
      for (let i = 0; i < 6; i++) for (const s of [-1, 1]) bx(c.body, S, .27, .14, .14, s * 1.62, 1.35, -1.6 + i * .4);
      for (const x of [-1.45, -1.05, -.65, .65, 1.05, 1.45]) bx(c.body, S, .14, .14, .27, x, 1.35, .8);
      for (let i = 0; i < 5; i++) { const d = 1.0 - i * .2; bx(c.body, S, .8, .18, d, 0, i * .18, .8 + d / 2); }
      lmCols(c, 4, -.3, .3, .65, .7, W, .05, .9); bx(c.body, W, .8, .12, .45, 0, 1.6, .5); lmGable(c, W, .8, .25, .45, 0, 1.72, .5);
      bx(c.body, S, .7, 1.3, .7, .75, 0, 1.2); bx(c.body, W, .4, .35, .3, .75, 1.3, 1.2); lmCols(c, 2, .6, .9, 1.4, .35, W, .03, 1.3); lmGable(c, W, .45, .15, .4, .75, 1.65, 1.25);
      bx(c.body, S, .3, 1.8, .3, -.65, 0, 1.15); bx(c.body, M.bz, .25, .3, .2, -.65, 1.8, 1.15);
      bx(c.body, W, 1.6, .08, .9, .15, .9, -.9); lmCols(c, 5, -.55, .85, -.5, .6, W, .045, .98); lmCols(c, 5, -.55, .85, -1.3, .6, W, .045, .98);
      bx(c.body, W, 1.55, .1, .88, .15, 1.58, -.9); lmGable(c, W, .88, .25, 1.6, .15, 1.68, -.9, PI / 2);
      bx(c.body, S, .25, .3, .25, -.55, .9, .1); bx(c.body, M.bz, .14, .7, .12, -.55, 1.2, .1); sp(c.body, M.bz, .07, -.55, 1.97, .1);
      cy(c.body, M.bz, .015, 1.2, -.45, 1.2, .1); cn(c.body, MT.gold, .025, .12, -.45, 2.4, .1); mk(G.wheel, c.body, c.cm, .04, .24, .24, -.66, 1.45, .1);
      lmFlag(c, 1.5, 1.4, 2.0);
    },
    parthenon(c) {   // the Parthenon: a Doric temple of eight by eight columns on a three-step base, a painted pediment, gilded shields
      const W = LMM.marble, top = lmSteps(c, W, 2.6, 3.8, 3, .14, 0, -.05, .16);
      lmCols(c, 8, -.98, .98, 1.55, 1.5, W, .095, top); lmCols(c, 8, -.98, .98, -1.65, 1.5, W, .095, top);
      for (const s of [-1, 1]) lmCols(c, 8, -1.3, 1.2, s * .98, 1.5, W, .095, top, true);
      bx(c.body, W, 1.5, 1.5, 2.6, 0, top, -.05); bx(c.body, MT.black, .5, 1.0, .03, 0, top, 1.26);
      bx(c.body, W, 2.2, .22, 3.4, 0, top + 1.5, -.05); bx(c.body, LMM.blue, 2.22, .1, 3.42, 0, top + 1.72, -.05); bx(c.body, W, 2.3, .06, 3.5, 0, top + 1.82, -.05);
      lmGable(c, W, 2.3, .55, 3.5, 0, top + 1.88, -.05);
      mk(G.prism, c.roof, LMM.blue, 1.9, .42, .03, 0, top + 1.9, 1.71);
      for (const [x, h] of [[0, .38], [-.3, .3], [.3, .3], [-.6, .18], [.6, .18]]) bx(c.roof, x ? W : c.cm, .1, h, .05, x, top + 1.9, 1.74);
      sp(c.roof, MT.gold, .06, 0, top + 2.45, 1.72); for (const s of [-1, 1]) bx(c.roof, MT.gold, .1, .14, .05, s * 1.08, top + 1.88, 1.72);
      for (let i = 0; i < 6; i++) mk(G.wheel, c.body, LMM.goldm, .03, .16, .16, -.85 + i * .34, top + 1.61, 1.66).rotation.y = PI / 2;
      lmFlag(c, 1.6, 1.3, 2.0);
    },
    olimpia(c) {   // the stadium of Olympia: a long sand track between earth banks, marble start lines, the vaulted entrance, the flame
      const W = LMM.marble;
      bx(c.body, LMM.sand, 3.6, .04, 1.2, 0, 0, 0);
      for (const s of [-1, 1]) for (let i = 0; i < 4; i++) bx(c.body, i ? LMM.turf : MT.stone, 3.6, .16 * (i + 1), .27, 0, 0, s * (.735 + i * .27));
      lmArch(c, MT.stone, -1.7, 0, 1.2, 1.0, .3, PI / 2);
      for (const x of [-1.4, 1.45]) bx(c.body, W, .08, .045, 1.2, x, 0, 0);
      for (let i = 0; i < 5; i++) cy(c.body, W, .03, .3, 1.45, 0, -.5 + i * .25);
      bx(c.body, W, .9, .75, .5, 0, 0, 1.35); lmCols(c, 4, -.35, .35, 1.15, .5, W, .035, .75); bx(c.body, MT.tile, 1.0, .08, .55, 0, 1.25, 1.35); bx(c.body, c.cm, 1.0, .06, .02, 0, 1.25, 1.63);
      cy(c.body, W, .12, .45, 1.2, .64, -1.56); cy(c.body, M.bz, .2, .12, 1.2, 1.09, -1.56); cn(c.body, MT.glow, .15, .35, 1.2, 1.21, -1.56); c.chim.push(1.2, 1.6, -1.56);
      for (const [x, z] of [[-.4, -.25], [-.1, .2], [.25, -.05]]) { figure(c, x, z, MT.skin, MT.skin, null, .04); bx(c.body, c.cm, .16, .1, .11, x, .2, z); }
      for (const [x, s, i] of [[-1.0, 1, 2], [-.5, -1, 3], [.4, -1, 1], [.9, 1, 3], [-1.3, -1, 2], [.6, 1, 2]]) sp(c.body, i & 1 ? c.cm : XM.linen, .07, x, .16 * (i + 1) + .06, s * (.735 + i * .27));
      lmFlag(c, 1.75, .45, 1.9);
    },
    rodos(c) {   // the harbour of Rhodes: two moles closing a basin, the bronze Colossus astride the entrance with a torch, a ship, warehouses
      const S = MT.stone, Bz = M.bz;
      bx(c.body, S, 3.8, .3, 1.1, 0, 0, -1.4); bx(c.body, LMM.water, 3.8, .03, 2.85, 0, 0, .5);
      for (const s of [-1, 1]) {
        bx(c.body, S, .4, .3, 2.0, s * 1.5, 0, .2); bx(c.body, S, 1.0, .3, .4, s * 1.1, 0, 1.4); cy(c.body, LMM.marble, .22, .55, s * .42, 0, 1.4);
        bx(c.body, Bz, .15, 1.15, .18, s * .42, .55, 1.4).rotation.z = s * .22;
        bx(c.body, MT.plaster, .9, .6, .6, s * 1.0, .3, -1.55); lmGable(c, MT.tile, .7, .3, 1.0, s * 1.0, .9, -1.55, PI / 2);
      }
      cy(c.body, S, .3, 1.2, 1.5, 0, -.5); lmCren(c, S, .6, .6, 1.2, 1.5, -.5, .1);
      bx(c.body, Bz, .42, .75, .24, 0, 1.62, 1.4); bx(c.body, Bz, .46, .2, .27, 0, 1.55, 1.4); cy(c.body, Bz, .06, .1, 0, 2.36, 1.4); sp(c.body, Bz, .13, 0, 2.52, 1.4);
      for (let i = 0; i < 5; i++) { const a = (i - 2) * .45; cn(c.roof, MT.gold, .025, .18, Math.sin(a) * .1, 2.55 + Math.cos(a) * .08, 1.4).rotation.z = -a; }
      bx(c.body, Bz, .1, .75, .1, .24, 2.2, 1.4).rotation.z = -.35; cy(c.body, Bz, .04, .2, .5, 2.9, 1.4); sp(c.body, MT.glow, .09, .5, 3.17, 1.4); c.chim.push(.5, 3.3, 1.4);
      bx(c.body, Bz, .1, .65, .1, -.32, 1.65, 1.4).rotation.z = -.12;
      const g = new THREE.Group(); g.position.set(.3, 0, .1); g.rotation.y = .3; c.body.add(g);
      bx(g, MT.dwood, .4, .22, 1.3, 0, 0, 0); bx(g, MT.dwood, .12, .3, .15, 0, .1, .65).rotation.x = .4; bx(g, MT.dwood, .12, .35, .15, 0, .1, -.65).rotation.x = -.5;
      cy(g, MT.wood, .03, 1.1, 0, .2, 0); bx(g, MT.white, .7, .55, .02, 0, .55, .02); bx(g, c.cm, .7, .1, .03, 0, .8, .02);
      for (let i = 0; i < 3; i++) bx(c.body, MT.canvas, .22, .22, .22, -.3 + i * .28, .3, -1.1);
      lmFlag(c, 0, -1.4, 2.2);
    },
    falanks(c) {   // the Macedonian phalanx camp: tents, the general's tent and the Vergina sun, a pike block drilling, racks of sarissas
      bx(c.body, MT.soil2, 3.6, .03, 3.6, 0, 0, 0); bx(c.body, MT.soil, 3.6, .3, .3, 0, 0, -1.75);
      for (let i = 0; i < 7; i++) { const x = -1.5 + i * .5; cy(c.body, MT.dwood, .04, .45, x, .3, -1.75); cn(c.body, MT.dwood, .04, .12, x, .75, -1.75); }
      for (const [x, z] of [[-1.4, -1.1], [-.75, -1.1], [-1.4, -.3]]) { lmGable(c, MT.canvas, .55, .5, .7, x, 0, z); bx(c.body, MT.black, .14, .2, .02, x, 0, z + .35); }
      lmGable(c, LMM.redb, .95, .8, 1.1, 1.1, 0, -1.0); bx(c.roof, c.cm, .1, .06, 1.12, 1.1, .78, -1.0); bx(c.body, MT.black, .25, .4, .02, 1.1, 0, -.45);
      cy(c.body, MT.dwood, .03, 2.4, .4, 0, -.9); mk(G.wheel, c.body, LMM.goldm, .03, .32, .32, .4, 2.15, -.88).rotation.y = PI / 2;
      for (let i = 0; i < 4; i++) mk(G.cbox, c.body, MT.gold, .5, .025, .02, .4, 2.15, -.86).rotation.z = i * PI / 4;
      for (let r = 0; r < 3; r++) for (let i = 0; i < 3; i++) {
        const x = .1 + i * .42, z = -.1 + r * .4, a = [.1, .7, 1.25][r], L = [2.2, 1.8, 1.3][r];
        bx(c.body, XM.linen, .15, .45, .1, x, 0, z); sp(c.body, MT.bronze, .07, x, .55, z); mk(G.wheel, c.body, c.cm, .04, .32, .32, x, .35, z + .08).rotation.y = PI / 2;
        cy(c.body, MT.dwood, .015, L, x + .1, .4, z).rotation.x = a;
        if (!r) cn(c.body, MT.steel, .025, .12, x + .1, .4 + L * Math.cos(a), z + L * Math.sin(a)).rotation.x = a;
      }
      cy(c.body, MT.dwood, .04, .95, -1.6, 0, .85); cy(c.body, MT.dwood, .04, .95, -.6, 0, .85); bx(c.body, MT.dwood, 1.1, .05, .05, -1.1, .9, .85);
      for (let i = 0; i < 5; i++) cy(c.body, MT.dwood, .015, 2.2, -1.5 + i * .2, 0, 1.3).rotation.x = -.35;
      for (let i = 0; i < 3; i++) mk(G.wheel, c.body, i & 1 ? c.cm : M.bz, .04, .36, .36, -1.3 + i * .32, .18, 1.65).rotation.y = PI / 2;
      lmFlag(c, 1.7, -.2, 1.9);
    },
  };
}
