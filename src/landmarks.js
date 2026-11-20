// Age-up buildings (AoE4-style landmarks) and legendary heroes. Pure data, no DOM / three (the simulation imports it).
// A civilization listed in LANDMARKS does not age up at the town center: its villagers build one of the two buildings of
// the next age, and the age comes when it is finished (game.js _complete). Each building has its own lasting effect
// while it stands (fx: the same format as a tech, game.js _mods; trickle: resources every 3 s; atk / range: it shoots
// like a tower), and every one of them trains the civilization's hero. Tried first with 5 civilizations (2026-11-20);
// the others keep the town center age-up.
//   LANDMARKS[civ] = [[to age 1: A, B], [to age 2: A, B], [to 3], [to 4]]
//   look: the model (render/entities.js LM_BUILD)
// Heroes: one per civilization, at most one alive (or in training). Stronger every age (HERO_AGE), and its own units
// near it fight better (HERO_AURA: radius, attack, armour). kitBase: whose model / kit it starts from.
import { UNITS, BUILDINGS, AGES } from './data.js';

export const LM_SIZE = 6, LM_BASE = 4;           // footprint, model design size (like the castle)
export const LM_TIME = 1.6;                      // build time = the age's time x this (one villager; more go faster)
export const LM_HP = 3000;
export const HERO_AGE = 0.2;                     // hero hp and attack +20 % per age after the first
export const HERO_AURA = { r: 7, atk: 0.15, armor: 1 };

const L = (id, name, icon, look, desc, o = {}) => ({ id, name, icon, look, desc, ...o });
export const LANDMARKS = {
  turk: [
    [L('lm_kervansaray', 'Söğüt Kervansarayı', '🐫', 'kervansaray', 'Kervanların konakladığı han: altın ve yiyecek toplama artar, düzenli yiyecek getirir.', { fx: { gather: { gold: 0.1, food: 0.05 } }, trickle: { food: 1 } }),
     L('lm_akinciocagi', 'Akıncı Ocağı', '🏇', 'ocak', 'Akıncıların yetiştiği ocak: süvari daha hızlı, birlikler daha çabuk yetişir.', { fx: { speed: { cavalry: 0.1 }, train: 0.1 } })],
    [L('lm_ulucami', 'Ulu Cami', '🕌', 'cami', 'Şehrin kalbi: köylüler daha dayanıklı, tarlalar daha verimli, yakındaki birlikler iyileşir.', { fx: { vhp: 0.2, farm: 0.15 }, heal: 1 }),
     L('lm_rumelihisari', 'Rumeli Hisarı', '🏰', 'hisar', 'Boğazı tutan hisar: kendisi ok atar; kuleler ve surlar güçlenir.', { fx: { towerAtk: 2, wallhp: 0.2 }, atk: 9, range: 8 })],
    [L('lm_suleymaniye', 'Süleymaniye Külliyesi', '🕌', 'kulliye', 'Cami, medrese, imaret: düzenli altın getirir, bütün toplama hızlanır.', { fx: { gather: { food: 0.06, wood: 0.06, stone: 0.06, gold: 0.06 } }, trickle: { gold: 2 } }),
     L('lm_tophane', 'Tophane-i Âmire', '💣', 'tophane', 'Top dökümhanesi: kuşatma silahları daha uzağa atar, birlikler daha çabuk yetişir.', { fx: { range: { siege: 1 }, train: 0.1 } })],
    [L('lm_dolmabahce', 'Dolmabahçe Sarayı', '🏛️', 'saray', 'Boğaz kıyısında saray: ticaret ve kervan kazancı artar, düzenli altın getirir.', { fx: { trade: 0.2, cart: 0.2 }, trickle: { gold: 3 } }),
     L('lm_harbiye', 'Harbiye Mektebi', '🎖️', 'harbiye', 'Subay okulu: menzilli birlikler daha sert vurur ve daha dayanıklıdır.', { fx: { atk: { ranged: 3 }, hp: { ranged: 0.1 } } })],
  ],
  roma: [
    [L('lm_forum', 'Forum', '🏛️', 'forum', 'Şehrin meydanı: yiyecek ve odun toplama artar, pazar takası iyileşir.', { fx: { gather: { food: 0.08, wood: 0.08 }, trade: 0.1 } }),
     L('lm_castra', 'Castra', '⛺', 'castra', 'Lejyon ordugâhı: piyade daha dayanıklı, birlikler daha çabuk yetişir.', { fx: { hp: { infantry: 0.08 }, train: 0.1 } })],
    [L('lm_pantheon', 'Pantheon', '🏛️', 'pantheon', 'Bütün tanrıların tapınağı: yapılar sağlamlaşır, yakındaki birlikler iyileşir, düzenli altın getirir.', { fx: { bhp: 0.1 }, heal: 1, trickle: { gold: 1 } }),
     L('lm_limes', 'Limes Kalesi', '🧱', 'sur', 'Sınır kalesi: kendisi ok atar; surlar ve kuleler güçlenir.', { fx: { wallhp: 0.3, towerAtk: 2 }, atk: 8, range: 8 })],
    [L('lm_kolezyum', 'Kolezyum', '🏟️', 'kolezyum', 'Gladyatör arenası: piyade daha sert vurur, her öldürülen düşman altın getirir.', { fx: { atkMul: { infantry: 0.1 }, killGold: 2 } }),
     L('lm_sukemeri', 'Su Kemeri', '🌉', 'sukemeri', 'Şehre su taşıyan kemer: tarlalar çok daha verimli, yiyecek toplama artar.', { fx: { farm: 0.2, gather: { food: 0.1 } } })],
    [L('lm_senato', 'Senato', '🏛️', 'senato', 'Cumhuriyetin meclisi: birlikler daha çabuk yetişir, düzenli altın getirir.', { fx: { train: 0.15 }, trickle: { gold: 2 } }),
     L('lm_zafertaki', 'Zafer Takı', '🏛️', 'zafer', 'Zaferlerin anıtı: piyade daha zırhlı ve daha dayanıklı.', { fx: { armor: { infantry: 1 }, hp: { infantry: 0.08 } } })],
  ],
  japon: [
    [L('lm_kura', 'Pirinç Ambarı', '🌾', 'kura', 'Kura ambarı: tarlalar daha verimli, yiyecek toplama artar.', { fx: { farm: 0.15, gather: { food: 0.1 } } }),
     L('lm_dojo', 'Dojo', '🥋', 'dojo', 'Kılıç okulu: piyade daha sert vurur, birlikler daha çabuk yetişir.', { fx: { atkMul: { infantry: 0.06 }, train: 0.1 } })],
    [L('lm_kinkakuji', 'Altın Köşk', '⛩️', 'kinkaku', 'Kinkaku-ji: düzenli altın getirir, yakındaki birlikler iyileşir.', { heal: 1, trickle: { gold: 2 } }),
     L('lm_himeji', 'Himeji Kalesi', '🏯', 'himeji', 'Beyaz Balıkçıl Kalesi: kendisi ok atar; yapılar sağlamlaşır, kuleler daha uzağa atar.', { fx: { bhp: 0.1, towerRange: 1 }, atk: 9, range: 8 })],
    [L('lm_torii', 'Fushimi Tapınağı', '⛩️', 'torii', 'Binlerce torii kapısı: köylüler daha dayanıklı, odun toplama artar.', { fx: { vhp: 0.2, gather: { wood: 0.12 } } }),
     L('lm_teppokisla', 'Teppō Kışlası', '🎌', 'kisla', 'Tüfek ocağı: menzilli birlikler daha sert vurur, birlikler daha çabuk yetişir.', { fx: { atk: { ranged: 2 }, train: 0.1 } })],
    [L('lm_dejima', 'Dejima Limanı', '⚓', 'dejima', 'Yabancılara açık ticaret adası: pazar takası ve kervan kazancı artar.', { fx: { trade: 0.2, cart: 0.25 } }),
     L('lm_osakadokum', 'Osaka Dökümhanesi', '⚙️', 'dokum', 'Çelik dökümhanesi: piyade daha sert vurur, menzilliler daha zırhlı.', { fx: { atk: { infantry: 2 }, armor: { ranged: 1 } } })],
  ],
  misir: [
    [L('lm_ambar', 'Büyük Ambar', '🌾', 'ambar', 'Nil’in bereketi: tarlalar ve ağıllar daha verimli.', { fx: { farm: 0.15, pasture: 0.2 } }),
     L('lm_arabaciahiri', 'Arabacı Ahırı', '🐎', 'ahir', 'Savaş arabalarının ahırı: süvari daha hızlı ve daha dayanıklı.', { fx: { speed: { cavalry: 0.08 }, hp: { cavalry: 0.08 } } })],
    [L('lm_karnak', 'Karnak Tapınağı', '🏛️', 'karnak', 'Dev sütunlu tapınak: yakındaki birlikler iyileşir, altın toplama artar, düzenli yiyecek getirir.', { fx: { gather: { gold: 0.08 } }, heal: 1, trickle: { food: 2 } }),
     L('lm_sfenks', 'Büyük Sfenks', '🦁', 'sfenks', 'Çölün bekçisi: piyade daha zırhlı, kuleler daha sert vurur.', { fx: { armor: { infantry: 1 }, towerAtk: 2 } })],
    [L('lm_piramit', 'Büyük Piramit', '🔺', 'piramit', 'Firavunun mezarı: düzenli altın getirir, taş toplama artar.', { fx: { gather: { stone: 0.15 } }, trickle: { gold: 3 } }),
     L('lm_abusimbel', 'Abu Simbel', '🗿', 'abusimbel', 'Dev heykelli tapınak: süvari daha sert vurur, menzilliler daha dayanıklı.', { fx: { atkMul: { cavalry: 0.1 }, hp: { ranged: 0.08 } } })],
    [L('lm_kutuphane', 'İskenderiye Kütüphanesi', '📜', 'kutuphane', 'Dünyanın bilgisi: birlikler daha çabuk yetişir, bütün toplama hızlanır.', { fx: { train: 0.15, gather: { food: 0.05, wood: 0.05, stone: 0.05, gold: 0.05 } } }),
     L('lm_feneri', 'İskenderiye Feneri', '🗼', 'fener', 'Dünyanın harikası: kendisi ok atar, yapılar daha uzağı görür, kuleler daha uzağa atar.', { fx: { blos: 2, towerRange: 1 }, atk: 10, range: 9 })],
  ],
  viking: [
    [L('lm_uzunev', 'Uzun Ev', '🛖', 'uzunev', 'Reisin uzun evi: odun toplama artar, köylüler daha dayanıklı.', { fx: { gather: { wood: 0.12 }, vhp: 0.1 } }),
     L('lm_hof', 'Hof Tapınağı', '🪓', 'hof', 'Odin’in tapınağı: piyade daha sert vurur, her öldürülen düşman altın getirir.', { fx: { atkMul: { infantry: 0.06 }, killGold: 2 } })],
    [L('lm_thing', 'Thing Meydanı', '🪨', 'thing', 'Özgür adamların meclisi: birlikler daha çabuk yetişir, pazar takası iyileşir.', { fx: { train: 0.12, trade: 0.1 } }),
     L('lm_naust', 'Uzun Gemi Tersanesi', '⛵', 'naust', 'Drakkarların tersanesi: gemiler daha hızlı ve daha dayanıklı.', { fx: { speed: { ship: 0.1 }, hp: { ship: 0.15 } } })],
    [L('lm_uppsala', 'Uppsala Tapınağı', '🌳', 'uppsala', 'Kutsal korudaki tapınak: yakındaki birlikler iyileşir, piyade daha dayanıklı.', { fx: { hp: { infantry: 0.08 } }, heal: 1 }),
     L('lm_jomsborg', 'Jomsborg Kalesi', '🏰', 'jomsborg', 'Jomsviking kalesi: kendisi ok atar, piyade daha zırhlı.', { fx: { armor: { infantry: 1 } }, atk: 9, range: 8 })],
    [L('lm_hedeby', 'Hedeby Pazarı', '⚖️', 'hedeby', 'Kuzeyin büyük pazarı: kervan kazancı artar, düzenli altın getirir.', { fx: { cart: 0.2 }, trickle: { gold: 2 } }),
     L('lm_ulfsalon', 'Valhalla Salonu', '🐺', 'ulfsalon', 'Savaşçıların salonu: piyade daha sert vurur ve daha hızlı koşar.', { fx: { atkMul: { infantry: 0.08 }, speed: { infantry: 0.08 } } })],
  ],
};

// hp / atk / armor / speed / range / rof / los: the hero's own numbers in its first age (they grow every age)
export const HEROES = {
  turk: { id: 'fatih', name: 'Fatih Sultan Mehmed', icon: '👑', kitBase: 'knight', cls: 'cavalry', hp: 330, atk: 15, armor: 3, speed: 3.6, rof: 1.4, bonus: { infantry: 1.2, building: 1.5 },
    desc: 'İstanbul’un fatihi. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'slash', head: 'kavuk', body: 'kaftan', wpn: 'scimitar', crest: 0xd9a441, cape: 0x1e6b3a, coat: 0xf0ebe0, scale: 1.12, hero: 1 } },
  roma: { id: 'sezar', name: 'Julius Caesar', icon: '🌿', kitBase: 'swordsman', cls: 'infantry', hp: 300, atk: 14, armor: 4, speed: 2.5, rof: 1.3, bonus: { infantry: 1.2 },
    desc: 'Galya’nın fatihi. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'kneel', anim: 'stab', head: 'defne', body: 'muscle', wpn: 'gladius', crest: 0x6a2a8a, cape: 0xa82a22, scale: 1.15, hero: 1 } },
  japon: { id: 'musashi', name: 'Miyamoto Musashi', icon: '⚔️', kitBase: 'heavyinf', cls: 'infantry', hp: 260, atk: 17, armor: 2, speed: 2.7, rof: 1.0, bonus: { infantry: 1.25 },
    desc: 'İki kılıçlı efsane kılıç ustası. Çok hızlı vurur; yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'kneel', anim: 'slash', head: 'ronin', body: 'kimono', wpn: 'nitou', shield: 0, crest: 0x2a2a3a, scale: 1.12, hero: 1 } },
  misir: { id: 'ramses', name: 'II. Ramses', icon: '☀️', kitBase: 'lightcav', cls: 'cavalry', hp: 300, atk: 13, armor: 2, speed: 3.2, range: 5, proj: 'arrow', rof: 1.6, bonus: { infantry: 1.2, ranged: 1.1 },
    desc: 'Kadeş’in firavunu, altın savaş arabasında okçu. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, mount: 'chariot', anim: 'bowhigh', head: 'khepresh', body: 'kalasiris', wpn: 'bow', coat: 0xf2ead8, crest: 0xd9a441, scale: 1.1, hero: 1 } },
  viking: { id: 'ragnar', name: 'Ragnar Lothbrok', icon: '🐺', kitBase: 'heavyinf', cls: 'infantry', hp: 320, atk: 15, armor: 3, speed: 2.7, rof: 1.3, bonus: { infantry: 1.2, building: 1.5 },
    desc: 'Efsanevi deniz kralı. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'spin', anim: 'chop', head: 'ragnar', body: 'byrnie', wpn: 'axe', shield: 1, shieldLook: 'round', crest: 0x2b5e8c, cape: 0x4a3a2a, scale: 1.12, hero: 1 } },
};
const HERO_COST = { food: 150, gold: 150 }, HERO_TIME = 40;

// ---- into data.js's tables (once, when this module loads) ----
export const LM_OF = {};     // landmark id -> { civ, to, ... }
for (const civ in LANDMARKS) {
  const h = HEROES[civ];
  if (h) {
    if (UNITS[h.id]) throw new Error('hero id used: ' + h.id);
    const b = UNITS[h.kitBase];
    UNITS[h.id] = { ...b, id: h.id, name: h.name, icon: h.icon, desc: h.desc, cls: h.cls, age: 1, cost: { ...HERO_COST }, time: HERO_TIME, hp: h.hp, atk: h.atk, armor: h.armor,
      speed: h.speed, range: h.range || 0, rof: h.rof, los: 9, pop: 1, bonus: { ...h.bonus }, proj: h.proj || null, civ, hero: true, kitBase: h.kitBase, kit: h.kit, look: '' };
  }
  LANDMARKS[civ].forEach((pair, i) => {
    const to = i + 1, a = AGES[to];
    for (const l of pair) {
      if (BUILDINGS[l.id]) throw new Error('landmark id used: ' + l.id);
      const lm = { civ, to, fx: l.fx || null, trickle: l.trickle || null, heal: l.heal || 0, look: l.look, other: pair.find((x) => x !== l).id };
      BUILDINGS[l.id] = { id: l.id, name: l.name, age: to - 1, cost: { ...a.cost }, time: Math.round(a.time * LM_TIME), hp: LM_HP, size: LM_SIZE, baseSize: LM_BASE, popCap: 0,
        trains: h ? [h.id] : [], researches: [], dropoff: null, atk: l.atk || 0, range: l.range || 0, los: 9, icon: l.icon, desc: l.desc, landmark: lm };
      LM_OF[l.id] = lm;
    }
  });
}
export const isLandmark = (type) => !!(BUILDINGS[type] && BUILDINGS[type].landmark);
// the effects of a landmark in words (from the numbers, like civs.js civLines)
const CLS = { infantry: 'Piyade', ranged: 'Menzilli', cavalry: 'Süvari', siege: 'Kuşatma', ship: 'Gemi' };
const RESN = { food: 'Yiyecek', wood: 'Odun', stone: 'Taş', gold: 'Altın' };
const pc = (v) => '+%' + Math.round(v * 100);
export function landmarkLines(id) {
  const d = BUILDINGS[id], lm = d && d.landmark; if (!lm) return [];
  const out = [], fx = lm.fx || {};
  const all = (o) => Object.keys(o).length === 4 && new Set(Object.values(o)).size === 1;
  for (const k in fx) {
    const v = fx[k];
    if (k === 'gather') { if (all(v)) out.push('Bütün toplama ' + pc(v.food)); else for (const r in v) out.push(`${RESN[r]} toplama ${pc(v[r])}`); }
    else if (k === 'hp') for (const c in v) out.push(`${CLS[c]} canı ${pc(v[c])}`);
    else if (k === 'atkMul') for (const c in v) out.push(`${CLS[c]} saldırısı ${pc(v[c])}`);
    else if (k === 'atk') for (const c in v) out.push(`${CLS[c]} saldırısı +${v[c]}`);
    else if (k === 'armor') for (const c in v) out.push(`${CLS[c]} zırhı +${v[c]}`);
    else if (k === 'range') for (const c in v) out.push(`${CLS[c]} menzili +${v[c]}`);
    else if (k === 'speed') for (const c in v) out.push(`${CLS[c]} hızı ${pc(v[c])}`);
    else out.push({ farm: `Tarla verimi ${pc(v)}`, pasture: `Ağıl verimi ${pc(v)}`, vhp: `Köylü canı ${pc(v)}`, train: `Birlik üretimi ${pc(v)} hızlı`, trade: `Pazar takası ${pc(v)}`,
      cart: `Ticaret arabası kazancı ${pc(v)}`, bhp: `Bina dayanıklılığı ${pc(v)}`, wallhp: `Sur dayanıklılığı ${pc(v)}`, towerAtk: `Kule saldırısı +${v}`, towerRange: `Kule menzili +${v}`,
      killGold: `Öldürülen her düşman +${v} altın`, blos: `Yapıların görüşü +${v}` }[k] || k);
  }
  if (lm.trickle) for (const r in lm.trickle) out.push(`Her dakika +${lm.trickle[r] * 20} ${RESN[r]}`);
  if (lm.heal) out.push('Yakındaki birliklerini iyileştirir');
  if (d.atk) out.push(`Kendisi ok atar (saldırı ${d.atk}, menzil ${d.range})`);
  out.push('Etkiler bina ayaktayken sürer');
  return out;
}
