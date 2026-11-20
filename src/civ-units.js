// Unique units: every civilization has two (FIRST and SECOND below, each replacing a different standard unit).
// Each REPLACES a standard unit for that civilization: the building, the age,
// the hotkey and the AI's build orders stay the standard unit's, Game.train() swaps the type (civs.js civUnit).
// A unique unit is the base unit with a few numbers changed, so every tech and bonus of its class applies to it.
//   base   the standard unit it replaces
//   hp / speed / rof   multipliers of the base value (rof < 1 = attacks faster)
//   atk / armor / range / time   added to the base value
//   cost / pop / bonus / proj   replace the base's (bonus is merged over the base's)
//   look   (view only) what its shots look like: 'javelin' | 'dart' | 'sling' (render/entities.js PROJ)
//   kit    changes to the base's look (render/entities.js KIT): crest / cape (a colour), scale, coat, weapon, shield,
//          mount ('elephant' | 'camel' | 'chariot': its own model in place of the horse); and the unit's own parts, the same in
//          every age: head, body, wpn, shieldLook (render/entities.js uHead / uBody / uWeapon / uShield), skin;
//          anim: its own way of fighting (_animHuman styles), die: of dying (_dieHuman: back / kneel / spin),
//          two: a two-handed weapon, sleeve: the colour of its sleeves, scythe: blades on a chariot's hubs
// Costs are a little above the base when the unit is plainly better.
// Balance: tools/lig.mjs (win % against an AI without a civilization; target ~75 for every civilization, 72-78 left
// alone). Measured once on 2026-11-20 (80 matches each), then adjusted by distance from 75 - the adjusted numbers of
// most civilizations are estimates, not re-measured.
const FIRST = {
  turk: { id: 'akinci', base: 'lightcav', name: 'Akıncı', icon: '🌙', speed: 1.12, atk: 2, hp: 1.1, bonus: { building: 0.8 },
    desc: 'Osmanlı akıncısı: daha hızlı, daha sert vurur. Baskın için biçilmiş kaftan.', kit: { anim: 'couch', head: 'bork', body: 'coat', wpn: 'tug', crest: 0xb8322a, coat: 0x6b4a2e } },
  roma: { id: 'lejyoner', base: 'swordsman', name: 'Lejyoner', icon: '🦅', hp: 1.08, armor: 1, cost: { food: 55, gold: 30 },
    desc: 'Disiplinli Roma piyadesi: daha dayanıklı, daha zırhlı.', kit: { die: 'kneel', anim: 'stab', head: 'galea', body: 'bands', wpn: 'gladius', shield: 1, shieldLook: 'scutum', crest: 0xc0392b, cape: 0x8e2a22, armor: 1 } },
  japon: { id: 'samuray', base: 'heavyinf', name: 'Samuray', icon: '⛩️', atk: 2, speed: 1.08, cost: { food: 55, gold: 65 },
    desc: 'Usta kılıç savaşçısı: daha sert vurur, daha çevik.', kit: { die: 'kneel', anim: 'slash', head: 'kabuto', body: 'lamellar', wpn: 'katana', shield: 0, crest: 0xc9302c } },
  misir: { id: 'nubyali', base: 'archer', name: 'Nubyalı Okçu', icon: '🏺', range: 1, atk: 1, cost: { wood: 35, gold: 20 }, time: -3,
    desc: 'Nubya’nın ünlü okçuları: daha uzağa atar, daha ucuz ve çabuk yetişir.', kit: { die: 'back', anim: 'bowquick', head: 'band', skin: 'dark', wpn: 'bow', crest: 0xe8c66a } },
  viking: { id: 'berserker', base: 'swordsman', name: 'Berserker', icon: '🪓', atk: 2, hp: 1.04, armor: -1, speed: 1.1,
    desc: 'Zırhsız, gözü dönmüş savaşçı: çok sert vurur, hızlı koşar, az korunur.', kit: { die: 'spin', head: 'pelt', body: 'bare', wpn: 'axe', two: 1, shield: 0, cape: 0x6f5236 } },
  mogol: { id: 'mangudai', base: 'lightcav', name: 'Mangudai', icon: '🐎', range: 4, proj: 'arrow', rof: 0.95, bonus: { ranged: 1, infantry: 1.3 }, cost: { food: 55, gold: 20 },
    desc: 'Atlı okçu: at sırtından ok atar, piyadeyi uzaktan eritir.', kit: { anim: 'parthian', head: 'furcap', body: 'coat', weapon: 'bow', wpn: 'bow', crest: 0x2e6fa8 } },
  cin: { id: 'chukonu', base: 'crossbow', name: 'Chu-Ko-Nu', icon: '🐉', rof: 0.84,
    desc: 'Tekrarlı arbalet: çok daha sık atar.', kit: { die: 'back', anim: 'pump', head: 'douli', body: 'coat', wpn: 'repeater', crest: 0xc9302c } },
  pers: { id: 'olumsuz', base: 'spearman', name: 'Ölümsüz', icon: '🦁', hp: 1.3, atk: 2, cost: { food: 40, wood: 20, gold: 10 },
    desc: 'Şahın seçkin muhafızı: sıradan mızrakçıdan çok daha dayanıklı ve güçlü.', kit: { die: 'kneel', anim: 'guard', head: 'tiara', body: 'robe', wpn: 'dory', shield: 1, shieldLook: 'wicker', crest: 0xd9a441 } },
  yunan: { id: 'hoplit', base: 'spearman', name: 'Hoplit', icon: '🏛️', hp: 1.06, armor: 1, speed: 0.92, cost: { food: 35, wood: 25 },
    desc: 'Tunç kalkanlı falanks piyadesi: ağır zırhlı, biraz yavaş.', kit: { die: 'kneel', anim: 'phalanx', head: 'corinth', body: 'linen', wpn: 'dory', shield: 1, shieldLook: 'aspis', crest: 0x2f6fb5, armor: 1 } },
  bizans: { id: 'katafrakt', base: 'knight', name: 'Katafrakt', icon: '☦️', armor: 2, hp: 1.15, bonus: { infantry: 1.3 }, cost: { food: 70, gold: 85 },
    desc: 'Tepeden tırnağa zırhlı süvari: piyadeyi ezer.', kit: { anim: 'couch', head: 'cataphract', body: 'scale', wpn: 'lance', shield: 1, shieldLook: 'kite', crest: 0x8e1b4a, coat: 0x3a3a44 } },
  frank: { id: 'paladin', base: 'knight', name: 'Paladin', icon: '⚜️', atk: 3, hp: 1.2,
    desc: 'Şövalyelerin en iyisi: daha sert vurur, daha zor düşer.', kit: { anim: 'couch', head: 'paladin', body: 'surcoat', wpn: 'lance', shield: 1, shieldLook: 'kite', crest: 0xe6c15c, cape: 0x2a4d9c } },
  ingiliz: { id: 'uzunyay', base: 'archer', name: 'Uzun Yaylı Okçu', icon: '🏹', range: 2, atk: 2,
    desc: 'Boy uzunluğunda porsuk yay: herkesten uzağa atar.', kit: { die: 'spin', anim: 'bowlong', head: 'hood', body: 'coat', wpn: 'longbow', crest: 0x2f7a3a } },
  ispanyol: { id: 'almogavar', base: 'swordsman', name: 'Almogavar', icon: '🏰', speed: 1.15, atk: 2, hp: 1.1,
    desc: 'Hafif donanımlı sınır baskıncısı: hızlı koşar, sert vurur.', kit: { die: 'spin', anim: 'raid', head: 'net', wpn: 'falchion', shield: 0, crest: 0xd4a017 } },
  arap: { id: 'deve', base: 'lightcav', name: 'Deve Süvarisi', icon: '🐪', hp: 1.4, atk: 3, bonus: { cavalry: 1.8 }, cost: { food: 60, gold: 15 },
    desc: 'Atları ürküten deve süvarisi: düşman süvarisine karşı çok güçlü.', kit: { anim: 'couch', mount: 'camel', coat: 0xc9a66b, head: 'turban', body: 'coat', crest: 0x1e7a4a } },
  hint: { id: 'fil', base: 'knight', name: 'Savaş Fili', icon: '🐘', hp: 1.9, atk: 5, speed: 0.8, pop: 2, time: 5, bonus: { building: 1.2 }, cost: { food: 95, gold: 95 },
    desc: 'Yürüyen kale: çok dayanıklı, çok güçlü, yavaş. 2 nüfus tutar.', kit: { anim: 'couch', mount: 'elephant', head: 'turban', body: 'coat', wpn: 'lance', crest: 0xe07b1a, shield: 0 } },
  kore: { id: 'hwarang', base: 'archer', name: 'Hwarang', icon: '🐢', hp: 1.05, armor: 1,
    desc: 'Seçkin soylu okçu: zırhlı, dayanıklı ve keskin nişancı.', kit: { die: 'kneel', anim: 'bowhigh', head: 'gat', body: 'coat', wpn: 'bow', crest: 0x1f8f98 } },
  aztek: { id: 'jaguar', base: 'swordsman', name: 'Jaguar Savaşçısı', icon: '🐆', bonus: { infantry: 1.2 }, cost: { food: 60, gold: 25 },
    desc: 'Obsidyen kılıçlı seçkin savaşçı: düşman piyadesine karşı güçlü.', kit: { die: 'spin', anim: 'wild', head: 'jaguar', body: 'pelt', wpn: 'macua', shield: 1, shieldLook: 'chimalli', crest: 0xf0a830 } },
  kartaca: { id: 'numidya', base: 'lightcav', name: 'Numidyalı Atlı', icon: '⚓', speed: 1.08, atk: 1, time: -4, cost: { food: 50, gold: 5 },
    desc: 'Paralı hafif süvari: ucuz, hızlı ve çabuk toplanır.', kit: { anim: 'throw', head: 'band', skin: 'dark', wpn: 'javelins', coat: 0x9a6a3a, crest: 0x7a3fa0 } },
  rus: { id: 'druzhina', base: 'heavyinf', name: 'Druzhina', icon: '❄️', hp: 1.25,
    desc: 'Knezin baltalı muhafızı: çok dayanıklı.', kit: { die: 'back', anim: 'chop', head: 'conic', body: 'scale', wpn: 'axe', shield: 1, shieldLook: 'kite', crest: 0xb02a2a, cape: 0x8a2c2c } },
  mali: { id: 'mandinka', base: 'spearman', name: 'Mandinka Mızraklısı', icon: '🪙', atk: 2, time: -5, cost: { food: 25, wood: 15 },
    desc: 'Kalabalık ve ucuz mızraklı: çabuk yetişir, biraz daha sert vurur.', kit: { die: 'kneel', anim: 'jab', head: 'wrap', skin: 'dark', body: 'robe', shield: 1, shieldLook: 'hide', crest: 0xd4a017 } },
};

// The second unique unit of every civilization (2026-11-20). Its base is never the first one's. A little milder than
// the first ones (the civilizations were balanced with one): not re-measured with tools/lig.mjs yet.
const SECOND = {
  turk: { id: 'yeniceri', base: 'musketeer', name: 'Yeniçeri', icon: '🎺', hp: 1.12, atk: 2, cost: { food: 50, gold: 70 },
    desc: 'Padişahın kapıkulu tüfekçisi: daha dayanıklı, daha isabetli.', kit: { die: 'back', anim: 'aim', head: 'yenicerib', body: 'robe', wpn: 'tufek', crest: 0x2c4f8a } },
  roma: { id: 'praetoryan', base: 'heavyinf', name: 'Praetoryan', icon: '🛡️', hp: 1.08, armor: 1, atk: 1, cost: { food: 55, gold: 70 },
    desc: 'İmparatorun muhafız birliği: ağır zırhlı, sert vuran seçkin piyade.', kit: { die: 'kneel', anim: 'stab', head: 'attic', body: 'muscle', wpn: 'spatha', shield: 1, shieldLook: 'oval', crest: 0x5b2a7a, cape: 0x5b2a7a } },
  japon: { id: 'teppo', base: 'musketeer', name: 'Teppō Ashigaru', icon: '🎌', range: 1, atk: 1, time: -3, cost: { food: 45, gold: 58 },
    desc: 'Fitilli tüfekli ayak askeri: daha uzağa atar, daha ucuz ve çabuk yetişir.', kit: { die: 'kneel', anim: 'aim', head: 'jingasa', body: 'dou', wpn: 'teppo', crest: 0xc9302c } },
  misir: { id: 'arabaci', base: 'lightcav', name: 'Savaş Arabası', icon: '🛞', range: 4, proj: 'arrow', hp: 1.25, speed: 0.92, rof: 1.1, time: 3,
    bonus: { ranged: 1, infantry: 1.2, siege: 1.5 }, cost: { food: 60, wood: 35, gold: 20 },
    desc: 'İki tekerlekli savaş arabasında okçu: koşarken ok atar, dayanıklı ama biraz yavaş.', kit: { mount: 'chariot', anim: 'bowhigh', head: 'khepresh', body: 'kalasiris', wpn: 'bow', coat: 0xd9c7a0, crest: 0x2f5fa8 } },
  viking: { id: 'huskarl', base: 'spearman', name: 'Huskarl', icon: '🛡', hp: 1.3, armor: 1, cost: { food: 35, wood: 20, gold: 10 },
    desc: 'Kalkan duvarının seçkin muhafızı: çok dayanıklı, zırhlı mızraklı.', kit: { die: 'back', anim: 'phalanx', head: 'gjermund', body: 'byrnie', wpn: 'dory', shield: 1, shieldLook: 'round', crest: 0x2b5e8c } },
  mogol: { id: 'kesik', base: 'knight', name: 'Keşik', icon: '🏹', speed: 1.1, atk: 1, cost: { food: 70, gold: 90 },
    desc: 'Hanın muhafız süvarisi: şövalyeden çevik, biraz daha sert vurur.', kit: { anim: 'couch', head: 'mogolhelm', body: 'mlamellar', wpn: 'lance', crest: 0xb03a2e, coat: 0x5a3a24 } },
  cin: { id: 'atesmizrak', base: 'spearman', name: 'Ateş Mızraklı', icon: '🎆', atk: 1, bonus: { building: 1.2, infantry: 1.2 }, cost: { food: 30, wood: 25, gold: 10 },
    desc: 'Ucunda barut borusu olan mızrak: piyadeye ve yapılara da sert vurur.', kit: { die: 'back', anim: 'jab', head: 'cinmigfer', body: 'scale', wpn: 'atesmizrak', shield: 0, crest: 0xc9302c } },
  pers: { id: 'tirpanli', base: 'knight', name: 'Tırpanlı Araba', icon: '⚔️', hp: 1.2, atk: 2, speed: 0.86, time: 3, bonus: { infantry: 1.4 }, cost: { food: 75, wood: 40, gold: 75 },
    desc: 'Tekerleklerinde tırpan olan savaş arabası: piyadeyi biçer, yavaştır.', kit: { mount: 'chariot', scythe: 1, anim: 'couch', head: 'kidaris', body: 'robe', wpn: 'dory', coat: 0x3a2a20, crest: 0xd9a441 } },
  yunan: { id: 'peltast', base: 'archer', name: 'Peltast', icon: '🎯', range: -1, atk: 1, hp: 1.15, speed: 1.08, look: 'javelin', bonus: { ranged: 1.3 }, cost: { food: 25, wood: 30, gold: 15 },
    desc: 'Hilal kalkanlı cirit atıcı: kısa menzil, sert atış, çevik.', kit: { die: 'spin', anim: 'throw', head: 'phrygian', body: 'chiton', wpn: 'javelins', shield: 1, shieldLook: 'pelte', crest: 0x2f6fb5 } },
  bizans: { id: 'varang', base: 'heavyinf', name: 'Varang Muhafızı', icon: '🪓', atk: 3, hp: 1.05, armor: -1, bonus: { cavalry: 1.25 }, cost: { food: 50, gold: 70 },
    desc: 'İmparatorun iskandinav muhafızı: iki elli baltayla çok sert vurur, atlıyı da devirir.', kit: { die: 'spin', anim: 'chop', head: 'varang', body: 'varangcoat', wpn: 'daneaxe', two: 1, shield: 0, crest: 0x8e1b4a } },
  frank: { id: 'franciska', base: 'swordsman', name: 'Franciska Baltacısı', icon: '🪓', atk: 1, speed: 1.06, bonus: { infantry: 1.2 },
    desc: 'Frank baltacısı: hızlı, düşman piyadesine karşı güçlü.', kit: { die: 'back', anim: 'chop', head: 'spangen', body: 'tunic', wpn: 'franciska', shield: 1, shieldLook: 'roundboss', crest: 0x2a4d9c } },
  ingiliz: { id: 'kirmiziceket', base: 'rifleman', name: 'Kırmızı Ceketli', icon: '💂', hp: 1.18, atk: 2, cost: { food: 55, gold: 80 },
    desc: 'Ayı postu kalpaklı muhafız alayı: daha dayanıklı, daha sert vurur.', kit: { die: 'back', anim: 'aim', head: 'bearskin', body: 'redcoat', sleeve: 0xb8222a, crest: 0xb8222a } },
  ispanyol: { id: 'konkistador', base: 'cuirassier', name: 'Konkistador', icon: '🗡️', atk: 2, bonus: { ranged: 1.6, infantry: 1.15 }, cost: { food: 80, gold: 105 },
    desc: 'Morion miğferli atlı fatih: okçuları ve piyadeyi ezer.', kit: { anim: 'raid', head: 'conqmorion', body: 'breast', wpn: 'rapier', crest: 0xc0392b, coat: 0x6b4a2e } },
  arap: { id: 'memluk', base: 'cuirassier', name: 'Memlûk', icon: '🌙', hp: 1.15, speed: 1.06, atk: 2, bonus: { cavalry: 1.2 }, cost: { food: 85, gold: 115 },
    desc: 'Seçkin kölemen süvari: çevik, düşman atlısına karşı güçlü.', kit: { anim: 'slash', head: 'memluk', body: 'coat', wpn: 'scimitar', shield: 1, shieldLook: 'kalkan', crest: 0x1e7a4a, coat: 0xe2d8c4 } },
  hint: { id: 'racput', base: 'swordsman', name: 'Racput', icon: '🗡', atk: 2, hp: 1.1, speed: 1.04, cost: { food: 50, gold: 30 },
    desc: 'Savaşçı soyundan kılıç ustası: sert vurur, zor düşer.', kit: { die: 'spin', anim: 'raid', head: 'pagri', body: 'angarkha', wpn: 'talwar', shield: 1, shieldLook: 'dhal', crest: 0xe07b1a } },
  kore: { id: 'woldo', base: 'spearman', name: 'Woldo Muhafızı', icon: '🌗', atk: 1, hp: 1.1, bonus: { infantry: 1.2 }, cost: { food: 35, wood: 20, gold: 10 },
    desc: 'Hilal ağızlı uzun palalı muhafız: geniş savuruşla piyadeye de güçlü.', kit: { die: 'kneel', anim: 'sweep', head: 'korhelm', body: 'dujeong', wpn: 'woldo', two: 1, shield: 0, crest: 0x2a4f9c } },
  aztek: { id: 'kartal', base: 'archer', name: 'Kartal Savaşçısı', icon: '🦅', range: -1, atk: 2, hp: 1.2, speed: 1.12, look: 'dart', cost: { food: 30, wood: 25, gold: 15 },
    desc: 'Atlatl ile ok fırlatan seçkin savaşçı: hızlı, sert atar, kısa menzil.', kit: { die: 'spin', anim: 'throw', head: 'kartal', body: 'feather', wpn: 'atlatl', crest: 0x8a5a2e } },
  kartaca: { id: 'balear', base: 'archer', name: 'Balear Sapancısı', icon: '🪨', atk: 1, look: 'sling', bonus: { infantry: 1.3, building: 1.3 }, cost: { food: 30, wood: 25, gold: 10 },
    desc: 'Adalı paralı sapancı: ucuz, taşı piyadeye ve yapılara sert iner.', kit: { die: 'back', anim: 'sling', head: 'curly', body: 'tunic', wpn: 'sling', crest: 0x7a3fa0 } },
  rus: { id: 'kazak', base: 'lightcav', name: 'Kazak', icon: '🐴', atk: 2, hp: 1.05, speed: 1.05, bonus: { ranged: 1.6 }, cost: { food: 60, gold: 20 },
    desc: 'Bozkırın kılıçlı atlısı: okçulara karşı daha da güçlü, sert vurur.', kit: { anim: 'slash', head: 'papakha', body: 'cherkeska', wpn: 'shashka', crest: 0x3a4a6a, coat: 0x4a3220 } },
  mali: { id: 'farima', base: 'knight', name: 'Farima Atlısı', icon: '🐎', hp: 1.12, atk: 1, cost: { food: 55, gold: 100 },
    desc: 'Mansa’nın zırhlı atlısı: altınla beslenir, dayanıklı ve sert.', kit: { anim: 'couch', head: 'malicap', body: 'boubou', wpn: 'lance', shield: 1, shieldLook: 'hide', crest: 0x8a2e1a, coat: 0xe2d2b0 } },
};
export const CIV_UNITS = {};
for (const civ of new Set([...Object.keys(FIRST), ...Object.keys(SECOND)])) CIV_UNITS[civ] = [FIRST[civ], SECOND[civ]].filter(Boolean);
