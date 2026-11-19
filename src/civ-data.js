// GENERATED - do not edit by hand. Source: the card game's civilization passives, converted by its
// tools/rts-civ-uret.mjs. fx uses the same keys as TECHS[].fx in data.js (folded into a player's mods at start);
// extra keys: killGold (gold for every enemy unit killed) and hp keyed by a unit type (spearman).
// color / color2 / art: the look in the menus (art: the portrait, copied to assets/civ/).
export const CIV_DATA = {
  arap: {"id":"arap","name":"Araplar","icon":"🐪","passive":"Çöl Gemileri & Kerr ü Ferr","color":"#1e7a4a","color2":"#efe4c4","art":"assets/civ/arap.webp","fx":{"hp":{"cavalry":0.08},"speed":{"cavalry":0.08}}},
  aztek: {"id":"aztek","name":"Aztekler","icon":"🐆","passive":"Çiçek Savaşları & Chinampa","color":"#6b8e23","color2":"#f0a830","art":"assets/civ/aztek.webp","fx":{"gather":{"food":0.1},"farm":0.1,"pasture":0.1,"killGold":4}},
  bizans: {"id":"bizans","name":"Bizanslılar","icon":"☦️","passive":"Tema Ordusu & Solidus","color":"#8e1b4a","color2":"#f0cf72","art":"assets/civ/bizans.webp","fx":{"hp":{"infantry":0.08,"cavalry":0.08},"gather":{"gold":0.1}}},
  cin: {"id":"cin","name":"Çinliler","icon":"🐉","passive":"Seddiçin & Kalabalık Ordular","color":"#c9a227","color2":"#8e1b1b","art":"assets/civ/cin.webp","fx":{"wallhp":0.25,"train":0.1}},
  frank: {"id":"frank","name":"Franklar","icon":"⚜️","passive":"Şövalyelik","color":"#2c3fa8","color2":"#f0cf4a","art":"assets/civ/frank.webp","fx":{"hp":{"cavalry":0.16},"speed":{"cavalry":0.05}}},
  hint: {"id":"hint","name":"Hintliler","icon":"🐘","passive":"Fil Ahırları & Muson Ormanları","color":"#c2185b","color2":"#f39c12","art":"assets/civ/hint.webp","fx":{"hp":{"cavalry":0.08},"atkMul":{"ranged":0.05}}},
  ingiliz: {"id":"ingiliz","name":"İngilizler","icon":"🏹","passive":"Uzun Yay","color":"#c9ccd1","color2":"#c8102e","art":"assets/civ/ingiliz.webp","fx":{"atkMul":{"ranged":0.08},"range":{"ranged":1}}},
  ispanyol: {"id":"ispanyol","name":"İspanyollar","icon":"🏰","passive":"Tercio & Yeni Dünya Gümüşü","color":"#4a2a1a","color2":"#f2c230","art":"assets/civ/ispanyol.webp","fx":{"hp":{"spearman":0.16},"gather":{"gold":0.1}}},
  japon: {"id":"japon","name":"Japonlar","icon":"⛩️","passive":"Bushido & Dar Geçitler","color":"#c9302c","color2":"#f3efe6","art":"assets/civ/japon.webp","fx":{"atkMul":{"infantry":0.08},"armor":{"infantry":1}}},
  kartaca: {"id":"kartaca","name":"Kartacalılar","icon":"⚓","passive":"Akdeniz Ticareti & Savaş Filleri","color":"#8c2a5c","color2":"#f0c873","art":"assets/civ/kartaca.webp","fx":{"hp":{"cavalry":0.08},"gather":{"gold":0.1},"trade":0.15}},
  kore: {"id":"kore","name":"Koreliler","icon":"🐢","passive":"Okçular Ülkesi & Dağ Kaleleri","color":"#5fa58a","color2":"#f1e8d6","art":"assets/civ/kore.webp","fx":{"gather":{"stone":0.1},"atkMul":{"ranged":0.08},"towerAtk":2}},
  mali: {"id":"mali","name":"Malililer","icon":"🪙","passive":"Altın ve Tuz Ticareti","color":"#8a5a2b","color2":"#f4c430","art":"assets/civ/mali.webp","fx":{"gather":{"gold":0.1},"trade":0.15,"cart":0.15}},
  misir: {"id":"misir","name":"Mısırlılar","icon":"🏺","passive":"Nil'in Bereketi & Çöl Savaşçıları","color":"#1f8f98","color2":"#e8c66a","art":"assets/civ/misir.webp","fx":{"gather":{"food":0.1},"farm":0.1,"pasture":0.1,"atkMul":{"cavalry":0.05,"ranged":0.05}}},
  mogol: {"id":"mogol","name":"Moğollar","icon":"🐎","passive":"Bozkır Atlıları & Yam Postası","color":"#3b6ea5","color2":"#e8d48a","art":"assets/civ/mogol.webp","fx":{"atkMul":{"cavalry":0.08},"killGold":4}},
  pers: {"id":"pers","name":"Persler","icon":"🦁","passive":"Kral Yolu & Satraplıklar","color":"#1f5f8b","color2":"#f0c75e","art":"assets/civ/pers.webp","fx":{"hp":{"ranged":0.08},"gather":{"gold":0.1}}},
  roma: {"id":"roma","name":"Romalılar","icon":"🦅","passive":"Disiplin & Mühendislik","color":"#7b3fa3","color2":"#e3c46e","art":"assets/civ/roma.webp","fx":{"hp":{"infantry":0.16,"spearman":0.16},"bhp":0.1}},
  rus: {"id":"rus","name":"Ruslar","icon":"❄️","passive":"Kara Kış & Uçsuz Topraklar","color":"#2e5e45","color2":"#dfe6e9","art":"assets/civ/rus.webp","fx":{"hp":{"infantry":0.13,"ranged":0.05,"cavalry":0.05}}},
  turk: {"id":"turk","name":"Türkler (Osmanlı)","icon":"🌙","passive":"Barut Ustaları & Kervan Yolları","color":"#b8322a","color2":"#e6c15c","art":"assets/civ/turk.webp","fx":{"atkMul":{"siege":0.08},"gather":{"gold":0.1,"wood":0.1}}},
  viking: {"id":"viking","name":"Vikingler","icon":"🪓","passive":"Yağma & Uzun Gemiler","color":"#4f6e86","color2":"#cfd8de","art":"assets/civ/viking.webp","fx":{"killGold":8,"speed":{"ship":0.15}}},
  yunan: {"id":"yunan","name":"Yunanlar","icon":"🏛️","passive":"Falanks & Polis","color":"#c8692c","color2":"#f3e7cf","art":"assets/civ/yunan.webp","fx":{"hp":{"spearman":0.16},"gather":{"stone":0.1}}},
};
