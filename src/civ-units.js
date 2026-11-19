// Unique units: every civilization has one. It REPLACES a standard unit for that civilization: the building, the age,
// the hotkey and the AI's build orders stay the standard unit's, Game.train() swaps the type (civs.js civUnit).
// A unique unit is the base unit with a few numbers changed, so every tech and bonus of its class applies to it.
//   base   the standard unit it replaces
//   hp / speed / rof   multipliers of the base value (rof < 1 = attacks faster)
//   atk / armor / range / time   added to the base value
//   cost / pop / bonus / proj   replace the base's (bonus is merged over the base's)
//   kit    changes to the base's look (render/entities.js KIT): crest / cape (a colour), scale, coat, weapon, shield, ...
// Costs are a little above the base when the unit is plainly better. Balance is a first guess (not measured yet).
export const CIV_UNITS = {
  turk: { id: 'akinci', base: 'lightcav', name: 'Akıncı', icon: '🌙', speed: 1.12, atk: 1, bonus: { building: 0.8 },
    desc: 'Osmanlı akıncısı: daha hızlı, daha sert vurur. Baskın için biçilmiş kaftan.', kit: { crest: 0xb8322a, coat: 0x6b4a2e } },
  roma: { id: 'lejyoner', base: 'swordsman', name: 'Lejyoner', icon: '🦅', hp: 1.2, armor: 1, cost: { food: 55, gold: 25 },
    desc: 'Disiplinli Roma piyadesi: daha dayanıklı, daha zırhlı.', kit: { crest: 0xc0392b, cape: 0x8e2a22, armor: 1 } },
  japon: { id: 'samuray', base: 'heavyinf', name: 'Samuray', icon: '⛩️', atk: 3, speed: 1.08, cost: { food: 55, gold: 65 },
    desc: 'Usta kılıç savaşçısı: daha sert vurur, daha çevik.', kit: { crest: 0xf3efe6, shield: 0 } },
  misir: { id: 'nubyali', base: 'archer', name: 'Nubyalı Okçu', icon: '🏺', range: 1, cost: { wood: 35, gold: 20 }, time: -3,
    desc: 'Nubya’nın ünlü okçuları: daha uzağa atar, daha ucuz ve çabuk yetişir.', kit: { crest: 0xe8c66a } },
  viking: { id: 'berserker', base: 'swordsman', name: 'Berserker', icon: '🪓', atk: 3, hp: 1.1, armor: -1, speed: 1.1,
    desc: 'Zırhsız, gözü dönmüş savaşçı: çok sert vurur, hızlı koşar, az korunur.', kit: { shield: 0, cape: 0x4f6e86 } },
  mogol: { id: 'mangudai', base: 'lightcav', name: 'Mangudai', icon: '🐎', range: 4, proj: 'arrow', atk: -1, rof: 1.15, bonus: { ranged: 1, infantry: 1.3 }, cost: { food: 60, wood: 20, gold: 20 },
    desc: 'Atlı okçu: at sırtından ok atar, piyadeyi uzaktan eritir.', kit: { weapon: 'bow', crest: 0x2e6fa8 } },
  cin: { id: 'chukonu', base: 'crossbow', name: 'Chu-Ko-Nu', icon: '🐉', rof: 0.68, atk: -1,
    desc: 'Tekrarlı arbalet: tek atışı biraz zayıf ama çok daha sık atar.', kit: { crest: 0xc9302c } },
  pers: { id: 'olumsuz', base: 'spearman', name: 'Ölümsüz', icon: '🦁', hp: 1.3, atk: 2, cost: { food: 40, wood: 20, gold: 10 },
    desc: 'Şahın seçkin muhafızı: sıradan mızrakçıdan çok daha dayanıklı ve güçlü.', kit: { crest: 0xd9a441, cape: 0x6a3d9a } },
  yunan: { id: 'hoplit', base: 'spearman', name: 'Hoplit', icon: '🏛️', hp: 1.2, armor: 2, speed: 0.92, cost: { food: 35, wood: 25 },
    desc: 'Tunç kalkanlı falanks piyadesi: ağır zırhlı, biraz yavaş.', kit: { crest: 0x2f6fb5, armor: 1 } },
  bizans: { id: 'katafrakt', base: 'knight', name: 'Katafrakt', icon: '☦️', armor: 2, hp: 1.1, bonus: { infantry: 1.3 }, cost: { food: 75, gold: 95 },
    desc: 'Tepeden tırnağa zırhlı süvari: piyadeyi ezer.', kit: { crest: 0x8e1b4a, coat: 0x3a3a44 } },
  frank: { id: 'paladin', base: 'knight', name: 'Paladin', icon: '⚜️', atk: 3, hp: 1.15, cost: { food: 75, gold: 95 },
    desc: 'Şövalyelerin en iyisi: daha sert vurur, daha zor düşer.', kit: { crest: 0x2a4d9c, cape: 0x2a4d9c } },
  ingiliz: { id: 'uzunyay', base: 'archer', name: 'Uzun Yaylı Okçu', icon: '🏹', range: 2, atk: 1, time: 3, cost: { wood: 45, gold: 30 },
    desc: 'Boy uzunluğunda porsuk yay: herkesten uzağa atar.', kit: { crest: 0xb02a2a } },
  ispanyol: { id: 'almogavar', base: 'swordsman', name: 'Almogavar', icon: '🏰', speed: 1.15, atk: 1,
    desc: 'Hafif donanımlı sınır baskıncısı: hızlı koşar, sert vurur.', kit: { shield: 0, crest: 0xd4a017 } },
  arap: { id: 'deve', base: 'lightcav', name: 'Deve Süvarisi', icon: '🐪', hp: 1.15, bonus: { cavalry: 1.8 }, cost: { food: 65, gold: 20 },
    desc: 'Atları ürküten deve süvarisi: düşman süvarisine karşı çok güçlü.', kit: { coat: 0xc9a66b, crest: 0x1e7a4a, scale: 1.08 } },
  hint: { id: 'fil', base: 'knight', name: 'Savaş Fili', icon: '🐘', hp: 1.9, atk: 5, speed: 0.68, pop: 2, time: 10, bonus: { building: 1.2 }, cost: { food: 120, gold: 110 },
    desc: 'Yürüyen kale: çok dayanıklı, çok güçlü, yavaş. 2 nüfus tutar.', kit: { coat: 0x77777f, scale: 1.4, crest: 0xe07b1a } },
  kore: { id: 'hwarang', base: 'archer', name: 'Hwarang', icon: '🐢', hp: 1.2, armor: 1, atk: 1, cost: { wood: 45, gold: 30 },
    desc: 'Seçkin soylu okçu: zırhlı, dayanıklı ve keskin nişancı.', kit: { crest: 0x1f8f98, armor: 1 } },
  aztek: { id: 'jaguar', base: 'swordsman', name: 'Jaguar Savaşçısı', icon: '🐆', atk: 1, hp: 1.1, bonus: { infantry: 1.5 }, cost: { food: 60, gold: 15 },
    desc: 'Obsidyen kılıçlı seçkin savaşçı: düşman piyadesine karşı çok güçlü, az altın ister.', kit: { crest: 0xf0a830, cape: 0xc8902a } },
  kartaca: { id: 'numidya', base: 'lightcav', name: 'Numidyalı Atlı', icon: '⚓', speed: 1.08, time: -4, cost: { food: 50, gold: 5 },
    desc: 'Paralı hafif süvari: ucuz, hızlı ve çabuk toplanır.', kit: { coat: 0x9a6a3a, crest: 0x7a3fa0 } },
  rus: { id: 'druzhina', base: 'heavyinf', name: 'Druzhina', icon: '❄️', hp: 1.25, speed: 0.95, cost: { food: 55, gold: 65 },
    desc: 'Knezin baltalı muhafızı: çok dayanıklı, biraz ağır.', kit: { crest: 0xb0c4d8, cape: 0x8a2c2c } },
  mali: { id: 'mandinka', base: 'spearman', name: 'Mandinka Mızraklısı', icon: '🪙', atk: 1, time: -5, cost: { food: 25, wood: 15 },
    desc: 'Kalabalık ve ucuz mızraklı: çabuk yetişir, biraz daha sert vurur.', kit: { crest: 0xd4a017 } },
};
