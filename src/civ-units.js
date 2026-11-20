// Unique units: every civilization has one. It REPLACES a standard unit for that civilization: the building, the age,
// the hotkey and the AI's build orders stay the standard unit's, Game.train() swaps the type (civs.js civUnit).
// A unique unit is the base unit with a few numbers changed, so every tech and bonus of its class applies to it.
//   base   the standard unit it replaces
//   hp / speed / rof   multipliers of the base value (rof < 1 = attacks faster)
//   atk / armor / range / time   added to the base value
//   cost / pop / bonus / proj   replace the base's (bonus is merged over the base's)
//   kit    changes to the base's look (render/entities.js KIT): crest / cape (a colour), scale, coat, weapon, shield,
//          mount ('elephant' | 'camel': its own model in place of the horse); and the unit's own parts, the same in
//          every age: head, body, wpn, shieldLook (render/entities.js uHead / uBody / uWeapon / uShield), skin
// Costs are a little above the base when the unit is plainly better.
// Balance: tools/lig.mjs (win % against an AI without a civilization; target ~75 for every civilization, 72-78 left
// alone). Measured once on 2026-11-20 (80 matches each), then adjusted by distance from 75 - the adjusted numbers of
// most civilizations are estimates, not re-measured.
export const CIV_UNITS = {
  turk: { id: 'akinci', base: 'lightcav', name: 'Akıncı', icon: '🌙', speed: 1.12, atk: 2, hp: 1.1, bonus: { building: 0.8 },
    desc: 'Osmanlı akıncısı: daha hızlı, daha sert vurur. Baskın için biçilmiş kaftan.', kit: { head: 'bork', body: 'coat', wpn: 'tug', crest: 0xb8322a, coat: 0x6b4a2e } },
  roma: { id: 'lejyoner', base: 'swordsman', name: 'Lejyoner', icon: '🦅', hp: 1.08, armor: 1, cost: { food: 55, gold: 30 },
    desc: 'Disiplinli Roma piyadesi: daha dayanıklı, daha zırhlı.', kit: { head: 'galea', body: 'bands', wpn: 'gladius', shield: 1, shieldLook: 'scutum', crest: 0xc0392b, cape: 0x8e2a22, armor: 1 } },
  japon: { id: 'samuray', base: 'heavyinf', name: 'Samuray', icon: '⛩️', atk: 2, speed: 1.08, cost: { food: 55, gold: 65 },
    desc: 'Usta kılıç savaşçısı: daha sert vurur, daha çevik.', kit: { head: 'kabuto', body: 'lamellar', wpn: 'katana', shield: 0, crest: 0xc9302c } },
  misir: { id: 'nubyali', base: 'archer', name: 'Nubyalı Okçu', icon: '🏺', range: 1, cost: { wood: 35, gold: 20 }, time: -3,
    desc: 'Nubya’nın ünlü okçuları: daha uzağa atar, daha ucuz ve çabuk yetişir.', kit: { head: 'band', skin: 'dark', wpn: 'bow', crest: 0xe8c66a } },
  viking: { id: 'berserker', base: 'swordsman', name: 'Berserker', icon: '🪓', atk: 3, hp: 1.1, armor: -1, speed: 1.1,
    desc: 'Zırhsız, gözü dönmüş savaşçı: çok sert vurur, hızlı koşar, az korunur.', kit: { head: 'pelt', body: 'bare', wpn: 'axe', two: 1, shield: 0, cape: 0x6f5236 } },
  mogol: { id: 'mangudai', base: 'lightcav', name: 'Mangudai', icon: '🐎', range: 4, proj: 'arrow', rof: 1.05, bonus: { ranged: 1, infantry: 1.3 }, cost: { food: 60, gold: 20 },
    desc: 'Atlı okçu: at sırtından ok atar, piyadeyi uzaktan eritir.', kit: { head: 'furcap', body: 'coat', weapon: 'bow', wpn: 'bow', crest: 0x2e6fa8 } },
  cin: { id: 'chukonu', base: 'crossbow', name: 'Chu-Ko-Nu', icon: '🐉', rof: 0.68,
    desc: 'Tekrarlı arbalet: çok daha sık atar.', kit: { head: 'douli', body: 'coat', wpn: 'repeater', crest: 0xc9302c } },
  pers: { id: 'olumsuz', base: 'spearman', name: 'Ölümsüz', icon: '🦁', hp: 1.4, atk: 2, cost: { food: 40, wood: 20, gold: 10 },
    desc: 'Şahın seçkin muhafızı: sıradan mızrakçıdan çok daha dayanıklı ve güçlü.', kit: { head: 'tiara', body: 'robe', wpn: 'dory', shield: 1, shieldLook: 'wicker', crest: 0xd9a441 } },
  yunan: { id: 'hoplit', base: 'spearman', name: 'Hoplit', icon: '🏛️', hp: 1.2, armor: 2, speed: 0.92, cost: { food: 35, wood: 25 },
    desc: 'Tunç kalkanlı falanks piyadesi: ağır zırhlı, biraz yavaş.', kit: { head: 'corinth', body: 'linen', wpn: 'dory', shield: 1, shieldLook: 'aspis', crest: 0x2f6fb5, armor: 1 } },
  bizans: { id: 'katafrakt', base: 'knight', name: 'Katafrakt', icon: '☦️', armor: 2, hp: 1.1, bonus: { infantry: 1.3 }, cost: { food: 75, gold: 95 },
    desc: 'Tepeden tırnağa zırhlı süvari: piyadeyi ezer.', kit: { head: 'cataphract', body: 'scale', wpn: 'lance', shield: 1, shieldLook: 'kite', crest: 0x8e1b4a, coat: 0x3a3a44 } },
  frank: { id: 'paladin', base: 'knight', name: 'Paladin', icon: '⚜️', atk: 3, hp: 1.2,
    desc: 'Şövalyelerin en iyisi: daha sert vurur, daha zor düşer.', kit: { head: 'paladin', body: 'surcoat', wpn: 'lance', shield: 1, shieldLook: 'kite', crest: 0xe6c15c, cape: 0x2a4d9c } },
  ingiliz: { id: 'uzunyay', base: 'archer', name: 'Uzun Yaylı Okçu', icon: '🏹', range: 2, atk: 1,
    desc: 'Boy uzunluğunda porsuk yay: herkesten uzağa atar.', kit: { head: 'hood', body: 'coat', wpn: 'longbow', crest: 0x2f7a3a } },
  ispanyol: { id: 'almogavar', base: 'swordsman', name: 'Almogavar', icon: '🏰', speed: 1.15, atk: 1,
    desc: 'Hafif donanımlı sınır baskıncısı: hızlı koşar, sert vurur.', kit: { head: 'net', wpn: 'falchion', shield: 0, crest: 0xd4a017 } },
  arap: { id: 'deve', base: 'lightcav', name: 'Deve Süvarisi', icon: '🐪', hp: 1.3, bonus: { cavalry: 1.8 }, cost: { food: 60, gold: 15 },
    desc: 'Atları ürküten deve süvarisi: düşman süvarisine karşı çok güçlü.', kit: { mount: 'camel', coat: 0xc9a66b, head: 'turban', body: 'coat', crest: 0x1e7a4a } },
  hint: { id: 'fil', base: 'knight', name: 'Savaş Fili', icon: '🐘', hp: 1.9, atk: 5, speed: 0.8, pop: 2, time: 5, bonus: { building: 1.2 }, cost: { food: 95, gold: 95 },
    desc: 'Yürüyen kale: çok dayanıklı, çok güçlü, yavaş. 2 nüfus tutar.', kit: { mount: 'elephant', head: 'turban', body: 'coat', wpn: 'lance', crest: 0xe07b1a, shield: 0 } },
  kore: { id: 'hwarang', base: 'archer', name: 'Hwarang', icon: '🐢', hp: 1.2, armor: 1, atk: 1,
    desc: 'Seçkin soylu okçu: zırhlı, dayanıklı ve keskin nişancı.', kit: { head: 'gat', body: 'coat', wpn: 'bow', crest: 0x1f8f98 } },
  aztek: { id: 'jaguar', base: 'swordsman', name: 'Jaguar Savaşçısı', icon: '🐆', bonus: { infantry: 1.2 }, cost: { food: 60, gold: 25 },
    desc: 'Obsidyen kılıçlı seçkin savaşçı: düşman piyadesine karşı güçlü.', kit: { head: 'jaguar', body: 'pelt', wpn: 'macua', shield: 1, shieldLook: 'chimalli', crest: 0xf0a830 } },
  kartaca: { id: 'numidya', base: 'lightcav', name: 'Numidyalı Atlı', icon: '⚓', speed: 1.08, atk: 1, time: -4, cost: { food: 50, gold: 5 },
    desc: 'Paralı hafif süvari: ucuz, hızlı ve çabuk toplanır.', kit: { head: 'band', skin: 'dark', wpn: 'javelins', coat: 0x9a6a3a, crest: 0x7a3fa0 } },
  rus: { id: 'druzhina', base: 'heavyinf', name: 'Druzhina', icon: '❄️', hp: 1.25,
    desc: 'Knezin baltalı muhafızı: çok dayanıklı.', kit: { head: 'conic', body: 'scale', wpn: 'axe', shield: 1, shieldLook: 'kite', crest: 0xb02a2a, cape: 0x8a2c2c } },
  mali: { id: 'mandinka', base: 'spearman', name: 'Mandinka Mızraklısı', icon: '🪙', atk: 2, time: -5, cost: { food: 25, wood: 15 },
    desc: 'Kalabalık ve ucuz mızraklı: çabuk yetişir, biraz daha sert vurur.', kit: { head: 'wrap', skin: 'dark', body: 'robe', shield: 1, shieldLook: 'hide', crest: 0xd4a017 } },
};
