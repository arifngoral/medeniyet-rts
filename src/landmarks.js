// Age-up buildings (AoE4-style landmarks) and legendary heroes. Pure data, no DOM / three (the simulation imports it).
// A civilization listed in LANDMARKS does not age up at the town center: its villagers build one of the two buildings of
// the next age, and the age comes when it is finished (game.js _complete). Each building has its own lasting effect
// while it stands (fx: the same format as a tech, game.js _mods; trickle: resources every 3 s; atk / range: it shoots
// like a tower), and every one of them trains the civilization's hero. Every civilization has them (the first five
// on 2026-11-20, the other fifteen the same day); cfg.noLandmarks brings back the town center age-up.
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

  // ---- the other fifteen (2026-11-20): look = the id without 'lm_' (models in render/lm/*.js)
  arap: [
    [L('lm_bagdatcarsi', 'Bağdat Çarşısı', '🧺', 'bagdatcarsi', 'Kubbeli çarşı: altın toplama artar, pazar takası iyileşir.', { fx: { gather: { gold: 0.1 }, trade: 0.1 } }),
     L('lm_deveagili', 'Deve Ağılı', '🐪', 'deveagili', 'Develerin ve atların yetiştiği ağıl: süvari daha dayanıklı ve daha hızlı.', { fx: { hp: { cavalry: 0.08 }, speed: { cavalry: 0.06 } } })],
    [L('lm_beytulhikme', 'Beytülhikme', '📚', 'beytulhikme', 'Bilgelik Evi: birlikler daha çabuk yetişir, bütün toplama hızlanır.', { fx: { train: 0.1, gather: { food: 0.05, wood: 0.05, stone: 0.05, gold: 0.05 } } }),
     L('lm_kahirekalesi', 'Kahire Kalesi', '🏰', 'kahirekalesi', 'Selahaddin’in kalesi: kendisi ok atar, surlar sağlamlaşır.', { fx: { wallhp: 0.2 }, atk: 9, range: 8 })],
    [L('lm_elhamra', 'Elhamra Sarayı', '🕌', 'elhamra', 'Kırmızı saray: düzenli altın getirir, yakındaki birlikler iyileşir.', { heal: 1, trickle: { gold: 2 } }),
     L('lm_memlukkisla', 'Memlûk Kışlası', '⚔️', 'memlukkisla', 'Seçkin süvarilerin kışlası: süvari daha sert vurur ve daha zırhlı.', { fx: { atkMul: { cavalry: 0.08 }, armor: { cavalry: 1 } } })],
    [L('lm_kervanhani', 'Büyük Kervan Hanı', '🐫', 'kervanhani', 'Çöl yollarının hanı: kervan kazancı ve pazar takası artar.', { fx: { cart: 0.25, trade: 0.15 } }),
     L('lm_samcelik', 'Şam Çeliği Dökümhanesi', '🗡️', 'samcelik', 'Ünlü çeliğin ocağı: piyade ve süvari daha sert vurur.', { fx: { atk: { infantry: 2, cavalry: 2 } } })],
  ],
  aztek: [
    [L('lm_cinampa', 'Çinampa Bahçeleri', '🌽', 'cinampa', 'Göl üstünde yüzen tarlalar: tarlalar çok daha verimli.', { fx: { farm: 0.2, gather: { food: 0.05 } } }),
     L('lm_kartalevi', 'Kartal Evi', '🦅', 'kartalevi', 'Kartal savaşçılarının evi: piyade daha hızlı ve daha sert.', { fx: { speed: { infantry: 0.08 }, atkMul: { infantry: 0.05 } } })],
    [L('lm_tlatelolco', 'Tlatelolco Pazarı', '🍫', 'tlatelolco', 'Dünyanın en büyük pazarı: pazar takası iyileşir, düzenli yiyecek getirir.', { fx: { trade: 0.15 }, trickle: { food: 2 } }),
     L('lm_jaguartapinagi', 'Jaguar Tapınağı', '🐆', 'jaguartapinagi', 'Jaguar savaşçılarının tapınağı: piyade daha dayanıklı, her öldürülen düşman altın getirir.', { fx: { hp: { infantry: 0.08 }, killGold: 2 } })],
    [L('lm_templomayor', 'Büyük Tapınak', '🛕', 'templomayor', 'Templo Mayor: yakındaki birlikler iyileşir, düzenli altın getirir.', { heal: 1, trickle: { gold: 2 } }),
     L('lm_topsahasi', 'Top Sahası', '⚫', 'topsahasi', 'Tlachtli oyun alanı: piyade daha sert vurur, birlikler daha çabuk yetişir.', { fx: { atkMul: { infantry: 0.08 }, train: 0.1 } })],
    [L('lm_gunespiramidi', 'Güneş Piramidi', '☀️', 'gunespiramidi', 'Teotihuacan’ın dev piramidi: düzenli altın getirir, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, trickle: { gold: 3 } }),
     L('lm_taktakvim', 'Güneş Taşı Tapınağı', '🗿', 'taktakvim', 'Takvim taşının tapınağı: piyade daha zırhlı, menzilliler daha uzağa atar.', { fx: { armor: { infantry: 1 }, range: { ranged: 1 } } })],
  ],
  bizans: [
    [L('lm_bukoleon', 'Bukoleon Limanı', '⚓', 'bukoleon', 'Sarayın limanı: yiyecek toplama artar, pazar takası iyileşir.', { fx: { gather: { food: 0.1 }, trade: 0.1 } }),
     L('lm_hipodrom', 'Hipodrom', '🏇', 'hipodrom', 'Araba yarışlarının pisti: süvari daha hızlı ve daha dayanıklı.', { fx: { speed: { cavalry: 0.08 }, hp: { cavalry: 0.06 } } })],
    [L('lm_ayasofya', 'Ayasofya', '⛪', 'ayasofya', 'Dev kubbeli bazilika: yakındaki birlikler iyileşir, düzenli altın getirir, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, heal: 1, trickle: { gold: 2 } }),
     L('lm_theodosius', 'Theodosius Surları', '🧱', 'theodosius', 'Üç katlı kara surları: kendisi ok atar, surlar ve kuleler çok güçlenir.', { fx: { wallhp: 0.35, towerAtk: 2 }, atk: 8, range: 8 })],
    [L('lm_darphane', 'Darphane', '🪙', 'darphane', 'Altın sikkelerin basıldığı yer: altın toplama artar, düzenli altın getirir.', { fx: { gather: { gold: 0.12 } }, trickle: { gold: 1 } }),
     L('lm_rumatesi', 'Rum Ateşi Atölyesi', '🔥', 'rumatesi', 'Sönmeyen ateşin sırrı: kuşatma silahları ve gemiler daha sert vurur.', { fx: { atkMul: { siege: 0.12, ship: 0.12 } } })],
    [L('lm_yerebatan', 'Yerebatan Sarnıcı', '💧', 'yerebatan', 'Sütunlu yeraltı sarnıcı: köylüler daha dayanıklı, tarlalar daha verimli.', { fx: { vhp: 0.2, farm: 0.15 } }),
     L('lm_varangkisla', 'Varang Kışlası', '🪓', 'varangkisla', 'İmparatorun muhafızları: piyade daha sert vurur ve daha zırhlı.', { fx: { atkMul: { infantry: 0.08 }, armor: { infantry: 1 } } })],
  ],
  cin: [
    [L('lm_pirincteras', 'Pirinç Terasları', '🌾', 'pirincteras', 'Basamak basamak tarlalar: tarlalar daha verimli, yiyecek toplama artar.', { fx: { farm: 0.15, gather: { food: 0.08 } } }),
     L('lm_topraksavasci', 'Pişmiş Toprak Atölyesi', '🏺', 'topraksavasci', 'Toprak ordunun atölyesi: birlikler daha çabuk yetişir.', { fx: { train: 0.12 } })],
    [L('lm_buyukkanal', 'Büyük Kanal Limanı', '🛶', 'buyukkanal', 'İmparatorluğun su yolu: pazar takası ve kervan kazancı artar.', { fx: { trade: 0.15, cart: 0.15 } }),
     L('lm_seddkalesi', 'Çin Seddi Kalesi', '🧱', 'seddkalesi', 'Seddin geçit kalesi: kendisi ok atar, surlar çok güçlenir, kuleler daha uzağa atar.', { fx: { wallhp: 0.35, towerRange: 1 }, atk: 9, range: 8 })],
    [L('lm_yasaksehir', 'Yasak Şehir', '🏯', 'yasaksehir', 'İmparatorun sarayı: düzenli altın getirir, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, trickle: { gold: 3 } }),
     L('lm_barutatolye', 'Barut Atölyesi', '🧨', 'barutatolye', 'Barutun doğduğu yer: menzilliler ve kuşatma silahları daha sert vurur.', { fx: { atk: { ranged: 2 }, atkMul: { siege: 0.1 } } })],
    [L('lm_porselenkule', 'Porselen Kule', '🗼', 'porselenkule', 'Nanjing’in beyaz kulesi: taş ve altın toplama artar, düzenli altın getirir.', { fx: { gather: { stone: 0.1, gold: 0.1 } }, trickle: { gold: 2 } }),
     L('lm_cennettapinagi', 'Cennet Tapınağı', '⛩️', 'cennettapinagi', 'Gök için kurban tapınağı: yakındaki birlikler iyileşir, piyade ve menzilliler daha dayanıklı.', { fx: { hp: { infantry: 0.06, ranged: 0.06 } }, heal: 1 })],
  ],
  frank: [
    [L('lm_degirmenkoy', 'Değirmen Köyü', '🌬️', 'degirmenkoy', 'Su değirmenli köy: tarlalar daha verimli, odun toplama artar.', { fx: { farm: 0.15, gather: { wood: 0.06 } } }),
     L('lm_motte', 'Motte Kalesi', '🏰', 'motte', 'Tepe üstünde ahşap kule: kendisi ok atar, yapılar sağlamlaşır.', { fx: { bhp: 0.08 }, atk: 8, range: 7 })],
    [L('lm_aachen', 'Aachen Sarayı', '👑', 'aachen', 'Şarlman’ın sarayı: birlikler daha çabuk yetişir, düzenli altın getirir.', { fx: { train: 0.12 }, trickle: { gold: 1 } }),
     L('lm_turnuva', 'Turnuva Alanı', '🛡️', 'turnuva', 'Şövalyelerin mızrak dövüşü alanı: süvari daha dayanıklı ve daha zırhlı.', { fx: { hp: { cavalry: 0.1 }, armor: { cavalry: 1 } } })],
    [L('lm_notredame', 'Notre-Dame', '⛪', 'notredame', 'Gotik katedral: yakındaki birlikler iyileşir, köylüler daha dayanıklı, düzenli altın getirir.', { fx: { vhp: 0.15 }, heal: 1, trickle: { gold: 1 } }),
     L('lm_carcassonne', 'Carcassonne', '🏰', 'carcassonne', 'Çifte surlu kale şehri: kendisi ok atar, surlar ve kuleler güçlenir.', { fx: { wallhp: 0.3, towerAtk: 2 }, atk: 9, range: 8 })],
    [L('lm_versay', 'Versay Sarayı', '⚜️', 'versay', 'Güneş Kral’ın sarayı: düzenli altın getirir, pazar takası iyileşir.', { fx: { trade: 0.1 }, trickle: { gold: 3 } }),
     L('lm_invalides', 'Les Invalides', '🎖️', 'invalides', 'Altın kubbeli askerî okul: piyade ve menzilliler daha sert vurur.', { fx: { atk: { infantry: 2, ranged: 2 } } })],
  ],
  hint: [
    [L('lm_basamaklikuyu', 'Basamaklı Kuyu', '💧', 'basamaklikuyu', 'Derin su kuyusu: tarlalar daha verimli, köylüler daha dayanıklı.', { fx: { farm: 0.15, vhp: 0.1 } }),
     L('lm_filahiri', 'Fil Ahırı', '🐘', 'filahiri', 'Savaş fillerinin ahırı: süvari daha dayanıklı, birlikler daha çabuk yetişir.', { fx: { hp: { cavalry: 0.1 }, train: 0.06 } })],
    [L('lm_sanchi', 'Sanchi Stupası', '🛕', 'sanchi', 'Kubbeli stupa: yakındaki birlikler iyileşir, düzenli yiyecek getirir.', { heal: 1, trickle: { food: 2 } }),
     L('lm_amberkalesi', 'Amber Kalesi', '🏰', 'amberkalesi', 'Tepe kalesi: kendisi ok atar, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, atk: 9, range: 8 })],
    [L('lm_baharatpazari', 'Baharat Pazarı', '🌶️', 'baharatpazari', 'Doğunun baharat pazarı: pazar takası çok iyileşir, altın toplama artar.', { fx: { trade: 0.2, gather: { gold: 0.08 } } }),
     L('lm_racputkisla', 'Racput Kışlası', '🗡️', 'racputkisla', 'Savaşçı soyunun kışlası: piyade daha sert vurur ve daha hızlı.', { fx: { atkMul: { infantry: 0.08 }, speed: { infantry: 0.06 } } })],
    [L('lm_tacmahal', 'Tac Mahal', '🕌', 'tacmahal', 'Beyaz mermer anıt mezar: düzenli altın getirir, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, trickle: { gold: 3 } }),
     L('lm_kizilkale', 'Kızıl Kale', '🏯', 'kizilkale', 'Delhi’nin kızıl surları: surlar güçlenir, kuleler ve menzilliler daha sert vurur.', { fx: { wallhp: 0.25, towerAtk: 2, atk: { ranged: 2 } } })],
  ],
  ingiliz: [
    [L('lm_manor', 'Malikâne', '🏡', 'manor', 'Lordun malikânesi: tarlalar daha verimli, yiyecek toplama artar.', { fx: { farm: 0.12, gather: { food: 0.06 } } }),
     L('lm_okcutalim', 'Okçu Talim Alanı', '🎯', 'okcutalim', 'Köy meydanında okçuluk: menzilliler daha sert vurur, birlikler daha çabuk yetişir.', { fx: { atkMul: { ranged: 0.06 }, train: 0.06 } })],
    [L('lm_westminster', 'Westminster Manastırı', '⛪', 'westminster', 'Taç giyme kilisesi: yakındaki birlikler iyileşir, köylüler daha dayanıklı.', { fx: { vhp: 0.15 }, heal: 1 }),
     L('lm_londrakulesi', 'Londra Kulesi', '🏰', 'londrakulesi', 'Beyaz Kule: kendisi ok atar, surlar sağlamlaşır.', { fx: { wallhp: 0.2 }, atk: 9, range: 8 })],
    [L('lm_globe', 'Globe Tiyatrosu', '🎭', 'globe', 'Şehrin tiyatrosu: düzenli altın getirir.', { trickle: { gold: 2 }, fx: { trade: 0.05 } }),
     L('lm_kraliyettersane', 'Kraliyet Tersanesi', '⛵', 'kraliyettersane', 'Donanmanın tersanesi: gemiler daha dayanıklı ve daha sert vurur.', { fx: { hp: { ship: 0.15 }, atkMul: { ship: 0.12 } } })],
    [L('lm_bigben', 'Parlamento ve Saat Kulesi', '🕰️', 'bigben', 'Westminster Sarayı: birlikler daha çabuk yetişir, pazar takası iyileşir.', { fx: { train: 0.15, trade: 0.1 } }),
     L('lm_woolwich', 'Kraliyet Cephaneliği', '💣', 'woolwich', 'Woolwich cephaneliği: kuşatma silahları ve menzilliler daha sert vurur.', { fx: { atkMul: { siege: 0.12 }, atk: { ranged: 2 } } })],
  ],
  ispanyol: [
    [L('lm_zeytinlik', 'Zeytin Değirmeni', '🫒', 'zeytinlik', 'Zeytinlik ve değirmen: yiyecek toplama artar, tarlalar daha verimli.', { fx: { gather: { food: 0.08 }, farm: 0.1 } }),
     L('lm_reconquista', 'Sınır Kalesi', '🏰', 'reconquista', 'Reconquista kalesi: kendisi ok atar, piyade daha dayanıklı.', { fx: { hp: { infantry: 0.06 } }, atk: 8, range: 7 })],
    [L('lm_santiago', 'Santiago Katedrali', '⛪', 'santiago', 'Hacıların katedrali: yakındaki birlikler iyileşir, köylüler daha dayanıklı.', { fx: { vhp: 0.15 }, heal: 1 }),
     L('lm_toledo', 'Toledo Kılıç Ocağı', '🗡️', 'toledo', 'Ünlü kılıçların ocağı: piyade daha sert vurur.', { fx: { atk: { infantry: 2 } } })],
    [L('lm_altinkule', 'Altın Kule', '🪙', 'altinkule', 'Sevilla’nın Torre del Oro’su: altın toplama artar, düzenli altın getirir.', { fx: { gather: { gold: 0.12 } }, trickle: { gold: 2 } }),
     L('lm_tercio', 'Tercio Kışlası', '🎌', 'tercio', 'Mızrak ve tüfek alayı: menzilliler daha sert vurur, piyade daha dayanıklı.', { fx: { atkMul: { ranged: 0.08 }, hp: { infantry: 0.06 } } })],
    [L('lm_escorial', 'El Escorial', '🏛️', 'escorial', 'Kral sarayı ve manastır: birlikler daha çabuk yetişir, düzenli altın getirir.', { fx: { train: 0.12 }, trickle: { gold: 2 } }),
     L('lm_armada', 'Armada Tersanesi', '⛵', 'armada', 'Yenilmez Armada’nın tersanesi: gemiler daha dayanıklı ve daha sert vurur.', { fx: { hp: { ship: 0.15 }, atkMul: { ship: 0.12 } } })],
  ],
  kartaca: [
    [L('lm_kothon', 'Kothon Limanı', '⚓', 'kothon', 'Yuvarlak savaş limanı: pazar takası iyileşir, yiyecek toplama artar.', { fx: { trade: 0.15, gather: { food: 0.08 } } }),
     L('lm_paraliasker', 'Paralı Asker Kampı', '💰', 'paraliasker', 'Paralı askerlerin kampı: birlikler daha çabuk yetişir, her öldürülen düşman altın getirir.', { fx: { train: 0.12, killGold: 1 } })],
    [L('lm_byrsa', 'Byrsa Sarayı', '🏛️', 'byrsa', 'Tepedeki saray: düzenli altın getirir, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, trickle: { gold: 2 } }),
     L('lm_filahirlari', 'Fil Ahırları', '🐘', 'filahirlari', 'Sur içindeki fil ahırları: süvari daha dayanıklı ve daha sert vurur.', { fx: { hp: { cavalry: 0.1 }, atkMul: { cavalry: 0.06 } } })],
    [L('lm_morboya', 'Mor Boya Atölyesi', '🟣', 'morboya', 'Tyros moru: düzenli altın getirir, kervan kazancı artar.', { fx: { cart: 0.15 }, trickle: { gold: 2 } }),
     L('lm_kartacasur', 'Kartaca Surları', '🧱', 'kartacasur', 'Üç sıralı şehir surları: kendisi ok atar, surlar çok güçlenir.', { fx: { wallhp: 0.3 }, atk: 9, range: 8 })],
    [L('lm_tanit', 'Tanit Tapınağı', '🌙', 'tanit', 'Ay tanrıçasının tapınağı: yakındaki birlikler iyileşir, köylüler daha dayanıklı.', { fx: { vhp: 0.15 }, heal: 1 }),
     L('lm_hannibalkamp', 'Hannibal’ın Ordugâhı', '⚔️', 'hannibalkamp', 'Alpleri aşan ordunun kampı: piyade ve süvari daha sert, piyade daha hızlı.', { fx: { atkMul: { infantry: 0.06, cavalry: 0.06 }, speed: { infantry: 0.06 } } })],
  ],
  kore: [
    [L('lm_ambaravlu', 'Küp Avlusu', '🏺', 'ambaravlu', 'Toprak küplerle dolu ambar avlusu: tarlalar daha verimli, yiyecek toplama artar.', { fx: { farm: 0.15, gather: { food: 0.06 } } }),
     L('lm_okculukpavyon', 'Okçuluk Köşkü', '🏹', 'okculukpavyon', 'Okçuların köşkü: menzilliler daha sert vurur, birlikler daha çabuk yetişir.', { fx: { atk: { ranged: 1 }, train: 0.06 } })],
    [L('lm_bulguksa', 'Bulguksa Tapınağı', '🛕', 'bulguksa', 'Taş merdivenli tapınak: yakındaki birlikler iyileşir, düzenli yiyecek getirir.', { heal: 1, trickle: { food: 2 } }),
     L('lm_hwaseong', 'Hwaseong Kalesi', '🏯', 'hwaseong', 'Suwon kalesi: kendisi ok atar, kuleler ve surlar güçlenir.', { fx: { towerAtk: 2, wallhp: 0.2 }, atk: 9, range: 8 })],
    [L('lm_gyeongbok', 'Gyeongbokgung Sarayı', '🏯', 'gyeongbok', 'Kralın sarayı: düzenli altın getirir, birlikler daha çabuk yetişir.', { fx: { train: 0.1 }, trickle: { gold: 2 } }),
     L('lm_hwachaatolye', 'Hwacha Atölyesi', '🎆', 'hwachaatolye', 'Ok yağdıran arabaların atölyesi: kuşatma silahları daha sert vurur ve daha uzağa atar.', { fx: { atkMul: { siege: 0.15 }, range: { siege: 1 } } })],
    [L('lm_kaplumbaga', 'Kaplumbağa Gemisi Tersanesi', '🐢', 'kaplumbaga', 'Zırhlı gemilerin tersanesi: gemiler daha dayanıklı ve daha sert vurur.', { fx: { hp: { ship: 0.2 }, atkMul: { ship: 0.12 } } }),
     L('lm_komutanlik', 'Donanma Komutanlığı', '🎖️', 'komutanlik', 'Amiral Yi’nin karargâhı: piyade ve menzilliler daha zırhlı.', { fx: { armor: { infantry: 1, ranged: 1 } } })],
  ],
  mali: [
    [L('lm_nijerpazari', 'Nijer Pazarı', '🧺', 'nijerpazari', 'Nehir kıyısında pazar: pazar takası iyileşir, yiyecek toplama artar.', { fx: { trade: 0.15, gather: { food: 0.06 } } }),
     L('lm_atliavlusu', 'Atlı Avlusu', '🐎', 'atliavlusu', 'Mansa’nın atlılarının avlusu: süvari daha dayanıklı ve daha hızlı.', { fx: { hp: { cavalry: 0.08 }, speed: { cavalry: 0.06 } } })],
    [L('lm_djinguereber', 'Djinguereber Camii', '🕌', 'djinguereber', 'Kerpiçten büyük cami: yakındaki birlikler iyileşir, köylüler daha dayanıklı.', { fx: { vhp: 0.15 }, heal: 1 }),
     L('lm_nianikale', 'Niani Kalesi', '🏰', 'nianikale', 'Başkentin kalesi: kendisi ok atar, surlar sağlamlaşır.', { fx: { wallhp: 0.2 }, atk: 8, range: 8 })],
    [L('lm_sankore', 'Sankore Medresesi', '📜', 'sankore', 'Timbuktu’nun okulu: birlikler daha çabuk yetişir, düzenli altın getirir.', { fx: { train: 0.12 }, trickle: { gold: 1 } }),
     L('lm_altinmadeni', 'Altın Madeni', '⛏️', 'altinmadeni', 'Bambuk’un altın ocakları: altın toplama çok artar, düzenli altın getirir.', { fx: { gather: { gold: 0.15 } }, trickle: { gold: 2 } })],
    [L('lm_mansasaray', 'Mansa Musa Sarayı', '👑', 'mansasaray', 'Dünyanın en zengin hükümdarının sarayı: düzenli altın getirir, kervan kazancı artar.', { fx: { cart: 0.15 }, trickle: { gold: 3 } }),
     L('lm_timbuktukale', 'Timbuktu Kervan Kalesi', '🐪', 'timbuktukale', 'Çöl yolunun kalesi: piyade ve süvari daha dayanıklı, piyade daha zırhlı.', { fx: { hp: { infantry: 0.06, cavalry: 0.06 }, armor: { infantry: 1 } } })],
  ],
  mogol: [
    [L('lm_surutlagi', 'Sürü Otlağı', '🐑', 'surutlagi', 'Bozkırın otlağı: ağıllar çok daha verimli, yiyecek toplama artar.', { fx: { pasture: 0.25, gather: { food: 0.05 } } }),
     L('lm_atliokcu', 'Atlı Okçu Talim Alanı', '🏹', 'atliokcu', 'Dörtnala ok atma alanı: menzilliler daha sert vurur, süvari daha hızlı.', { fx: { atk: { ranged: 1 }, speed: { cavalry: 0.05 } } })],
    [L('lm_karakurum', 'Karakurum Pazarı', '💰', 'karakurum', 'Başkentin pazarı: pazar takası iyileşir, her öldürülen düşman altın getirir.', { fx: { trade: 0.15, killGold: 2 } }),
     L('lm_kurultay', 'Kurultay Çadırı', '⛺', 'kurultay', 'Büyük meclis çadırı: birlikler daha çabuk yetişir, süvari daha dayanıklı.', { fx: { train: 0.12, hp: { cavalry: 0.06 } } })],
    [L('lm_yamistasyon', 'Yam Posta İstasyonu', '📯', 'yamistasyon', 'Atlı posta istasyonu: köylüler daha hızlı, kervan kazancı artar.', { fx: { vspeed: 0.1, cart: 0.15 } }),
     L('lm_kusatmakamp', 'Kuşatma Mühendisleri Kampı', '🪨', 'kusatmakamp', 'Çinli ve Pers mühendislerin kampı: kuşatma silahları daha sert vurur ve daha uzağa atar.', { fx: { atkMul: { siege: 0.15 }, range: { siege: 1 } } })],
    [L('lm_altincadir', 'Altın Otağ', '⛺', 'altincadir', 'Hanın altın çadırı: düzenli altın getirir.', { trickle: { gold: 3 } }),
     L('lm_kesikordugah', 'Keşik Ordugâhı', '🐎', 'kesikordugah', 'Hanın muhafızlarının ordugâhı: süvari daha sert vurur ve daha zırhlı.', { fx: { atkMul: { cavalry: 0.08 }, armor: { cavalry: 1 } } })],
  ],
  pers: [
    [L('lm_persbahcesi', 'Pers Bahçesi', '🌳', 'persbahcesi', 'Dört bölümlü cennet bahçesi: tarlalar daha verimli, köylüler daha dayanıklı.', { fx: { farm: 0.15, vhp: 0.1 } }),
     L('lm_olumsuzkisla', 'Ölümsüzler Kışlası', '🦁', 'olumsuzkisla', 'On binlerin kışlası: piyade daha dayanıklı, birlikler daha çabuk yetişir.', { fx: { hp: { infantry: 0.08 }, train: 0.06 } })],
    [L('lm_kralyolu', 'Kral Yolu Hanı', '🐎', 'kralyolu', 'Kral Yolu’nun istasyonu: kervan kazancı ve pazar takası artar.', { fx: { cart: 0.15, trade: 0.1 } }),
     L('lm_atestapinagi', 'Ateş Tapınağı', '🔥', 'atestapinagi', 'Sönmeyen ateşin tapınağı: yakındaki birlikler iyileşir, menzilliler daha sert vurur.', { fx: { atkMul: { ranged: 0.06 } }, heal: 1 })],
    [L('lm_persepolis', 'Persepolis Apadanası', '🏛️', 'persepolis', 'Yüz sütunlu taht salonu: düzenli altın getirir.', { trickle: { gold: 3 } }),
     L('lm_pasargad', 'Pasargad Kalesi', '🏰', 'pasargad', 'Kiros’un başkent kalesi: kendisi ok atar, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, atk: 9, range: 8 })],
    [L('lm_kanat', 'Kanat Su Yolları', '💧', 'kanat', 'Yeraltı su kanalları: tarlalar daha verimli, yiyecek toplama artar.', { fx: { farm: 0.15, gather: { food: 0.08 } } }),
     L('lm_savaranahir', 'Savaran Ahırları', '🏇', 'savaranahir', 'Zırhlı atlıların ahırları: süvari daha dayanıklı ve daha zırhlı.', { fx: { hp: { cavalry: 0.1 }, armor: { cavalry: 1 } } })],
  ],
  rus: [
    [L('lm_kurkpazari', 'Kürk Ticaret Evi', '🦊', 'kurkpazari', 'Kürk tüccarlarının evi: odun toplama artar, pazar takası iyileşir.', { fx: { gather: { wood: 0.1 }, trade: 0.1 } }),
     L('lm_ahsapkremlin', 'Ahşap Kremlin', '🪵', 'ahsapkremlin', 'Kütük surlu kale: kendisi ok atar, piyade daha dayanıklı.', { fx: { hp: { infantry: 0.05 } }, atk: 7, range: 7 })],
    [L('lm_novgorod', 'Novgorod Katedrali', '⛪', 'novgorod', 'Altın kubbeli katedral: yakındaki birlikler iyileşir, köylüler daha dayanıklı.', { fx: { vhp: 0.15 }, heal: 1 }),
     L('lm_kremlin', 'Moskova Kremlini', '🏰', 'kremlin', 'Kızıl tuğla kale: kendisi ok atar, surlar ve kuleler güçlenir.', { fx: { wallhp: 0.3, towerAtk: 2 }, atk: 9, range: 8 })],
    [L('lm_volgaliman', 'Volga Limanı', '⛵', 'volgaliman', 'Nehir ticaretinin limanı: kervan kazancı artar, düzenli yiyecek getirir.', { fx: { cart: 0.15 }, trickle: { food: 2 } }),
     L('lm_topdokum', 'Top Döküm Avlusu', '💣', 'topdokum', 'Moskova’nın top dökümhanesi: kuşatma silahları ve menzilliler daha sert vurur.', { fx: { atkMul: { siege: 0.12 }, atk: { ranged: 1 } } })],
    [L('lm_kislaksaray', 'Kışlık Saray', '🏛️', 'kislaksaray', 'Neva kıyısındaki saray: düzenli altın getirir.', { trickle: { gold: 3 } }),
     L('lm_aziz_basil', 'Aziz Basil Katedrali', '⛪', 'aziz_basil', 'Soğan kubbeli katedral: piyade daha zırhlı ve daha dayanıklı.', { fx: { armor: { infantry: 1 }, hp: { infantry: 0.06 } } })],
  ],
  yunan: [
    [L('lm_agora', 'Agora', '🏛️', 'agora', 'Şehrin meydanı: pazar takası iyileşir, yiyecek toplama artar.', { fx: { trade: 0.1, gather: { food: 0.08 } } }),
     L('lm_gymnasion', 'Gymnasion', '🤸', 'gymnasion', 'İdman yeri: piyade daha hızlı ve daha dayanıklı.', { fx: { speed: { infantry: 0.06 }, hp: { infantry: 0.06 } } })],
    [L('lm_delfi', 'Delfi Kahinliği', '🔮', 'delfi', 'Apollon’un kahini: yapılar daha uzağı görür, yakındaki birlikler iyileşir.', { fx: { blos: 2 }, heal: 1 }),
     L('lm_akropolsur', 'Akropolis Surları', '🧱', 'akropolsur', 'Kayalık tepenin surları: kendisi ok atar, surlar güçlenir.', { fx: { wallhp: 0.3 }, atk: 8, range: 8 })],
    [L('lm_parthenon', 'Parthenon', '🏛️', 'parthenon', 'Athena’nın tapınağı: düzenli altın getirir, yapılar sağlamlaşır.', { fx: { bhp: 0.1 }, trickle: { gold: 2 } }),
     L('lm_olimpia', 'Olimpia Stadı', '🏃', 'olimpia', 'Oyunların stadı: piyade daha sert vurur, birlikler daha çabuk yetişir.', { fx: { atkMul: { infantry: 0.08 }, train: 0.08 } })],
    [L('lm_rodos', 'Rodos Limanı', '🗽', 'rodos', 'Dev heykelli liman: pazar takası ve kervan kazancı artar.', { fx: { trade: 0.15, cart: 0.15 } }),
     L('lm_falanks', 'Makedon Falanks Kampı', '🛡️', 'falanks', 'İskender’in ordusunun kampı: piyade daha zırhlı ve daha sert.', { fx: { armor: { infantry: 1 }, atk: { infantry: 1 } } })],
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

  arap: { id: 'selahaddin', name: 'Selahaddin Eyyubi', icon: '🌙', kitBase: 'knight', cls: 'cavalry', hp: 330, atk: 15, armor: 3, speed: 3.6, rof: 1.4, bonus: { cavalry: 1.2, infantry: 1.1 },
    desc: 'Kudüs’ün fatihi, adil sultan. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'slash', head: 'memluk', body: 'kaftan', wpn: 'scimitar', shield: 1, shieldLook: 'kalkan', crest: 0xd9a441, cape: 0x1e7a4a, coat: 0xf0ebe0, scale: 1.12, hero: 1 } },
  aztek: { id: 'moctezuma', name: 'Moctezuma', icon: '🪶', kitBase: 'swordsman', cls: 'infantry', hp: 300, atk: 15, armor: 3, speed: 2.7, rof: 1.3, bonus: { infantry: 1.25 },
    desc: 'Tenochtitlan’ın hükümdarı. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'spin', anim: 'wild', head: 'tuyler', body: 'feather', wpn: 'macua', shield: 1, shieldLook: 'chimalli', crest: 0x1e8a5a, cape: 0x1e8a5a, scale: 1.15, hero: 1 } },
  bizans: { id: 'belisarius', name: 'Belisarius', icon: '☦️', kitBase: 'knight', cls: 'cavalry', hp: 340, atk: 14, armor: 4, speed: 3.4, rof: 1.5, bonus: { infantry: 1.2 },
    desc: 'Justinianus’un büyük komutanı. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'couch', head: 'cataphract', body: 'scale', wpn: 'lance', shield: 1, shieldLook: 'kite', crest: 0x6a1e5a, cape: 0x6a1e5a, coat: 0x3a3a44, scale: 1.12, hero: 1 } },
  cin: { id: 'guanyu', name: 'Guan Yu', icon: '🐉', kitBase: 'heavyinf', cls: 'infantry', hp: 320, atk: 16, armor: 3, speed: 2.6, rof: 1.4, bonus: { infantry: 1.2, cavalry: 1.2 },
    desc: 'Üç Krallık’ın efsane savaşçısı, ay palalı. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'kneel', anim: 'sweep', head: 'cinmigfer', body: 'scale', wpn: 'woldo', two: 1, shield: 0, crest: 0x1e7a3a, cape: 0x1e7a3a, scale: 1.15, hero: 1 } },
  frank: { id: 'sarlman', name: 'Şarlman', icon: '👑', kitBase: 'knight', cls: 'cavalry', hp: 340, atk: 15, armor: 4, speed: 3.4, rof: 1.4, bonus: { infantry: 1.2 },
    desc: 'Frankların imparatoru. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'slash', head: 'tac', body: 'surcoat', wpn: 'spatha', shield: 1, shieldLook: 'kite', crest: 0xd9a441, cape: 0x2a4d9c, coat: 0xf0ebe0, scale: 1.12, hero: 1 } },
  hint: { id: 'lakshmibai', name: 'Rani Lakşmibay', icon: '🗡️', kitBase: 'knight', cls: 'cavalry', hp: 300, atk: 16, armor: 2, speed: 3.8, rof: 1.2, bonus: { infantry: 1.2, ranged: 1.2 },
    desc: 'Jhansi’nin savaşçı kraliçesi. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'raid', head: 'pagri', body: 'angarkha', wpn: 'talwar', shield: 1, shieldLook: 'dhal', crest: 0xe07b1a, coat: 0xf0ebe0, scale: 1.12, hero: 1 } },
  ingiliz: { id: 'richard', name: 'Aslan Yürekli Richard', icon: '🦁', kitBase: 'knight', cls: 'cavalry', hp: 350, atk: 15, armor: 4, speed: 3.3, rof: 1.5, bonus: { infantry: 1.2 },
    desc: 'Haçlı kral. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'slash', head: 'tac', body: 'surcoat', wpn: 'spatha', shield: 1, shieldLook: 'kite', crest: 0xb8222a, cape: 0xb8222a, coat: 0x5a4030, scale: 1.12, hero: 1 } },
  ispanyol: { id: 'elcid', name: 'El Cid', icon: '⚔️', kitBase: 'knight', cls: 'cavalry', hp: 340, atk: 15, armor: 3, speed: 3.5, rof: 1.4, bonus: { infantry: 1.2, cavalry: 1.1 },
    desc: 'Valensiya’nın efsanevi şövalyesi. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'slash', head: 'spangen', body: 'surcoat', wpn: 'spatha', shield: 1, shieldLook: 'kite', crest: 0xd4a017, cape: 0xc0392b, coat: 0xf0ebe0, scale: 1.12, hero: 1 } },
  kartaca: { id: 'hannibal', name: 'Hannibal Barka', icon: '🐘', kitBase: 'knight', cls: 'cavalry', hp: 420, atk: 16, armor: 3, speed: 2.9, rof: 1.6, pop: 2, bonus: { infantry: 1.2, building: 1.4 },
    desc: 'Filleriyle Alpleri aşan komutan. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, mount: 'elephant', anim: 'couch', head: 'attic', body: 'muscle', wpn: 'dory', crest: 0x7a3fa0, cape: 0x7a3fa0, scale: 1.0, hero: 1 } },
  kore: { id: 'yisunsin', name: 'Amiral Yi Sun-sin', icon: '🐢', kitBase: 'heavyinf', cls: 'infantry', hp: 300, atk: 15, armor: 4, speed: 2.6, rof: 1.4, bonus: { infantry: 1.2 },
    desc: 'Yenilmez amiral. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'kneel', anim: 'slash', head: 'korhelm', body: 'dujeong', wpn: 'spatha', shield: 0, crest: 0xb8222a, cape: 0x2a4f9c, scale: 1.15, hero: 1 } },
  mali: { id: 'mansamusa', name: 'Mansa Musa', icon: '👑', kitBase: 'knight', cls: 'cavalry', hp: 320, atk: 14, armor: 3, speed: 3.4, rof: 1.4, bonus: { infantry: 1.2 },
    desc: 'Dünyanın en zengin hükümdarı. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'couch', head: 'tac', skin: 'dark', body: 'boubou', wpn: 'lance', shield: 1, shieldLook: 'hide', crest: 0xd9a441, cape: 0x8a2e1a, coat: 0xf0ebe0, scale: 1.12, hero: 1 } },
  mogol: { id: 'cengiz', name: 'Cengiz Han', icon: '🏹', kitBase: 'lightcav', cls: 'cavalry', hp: 300, atk: 13, armor: 2, speed: 3.9, range: 5, proj: 'arrow', rof: 1.4, bonus: { infantry: 1.3, ranged: 1.1 },
    desc: 'Bozkırın hanı, at üstünden ok atar. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'parthian', head: 'mogolhelm', body: 'mlamellar', weapon: 'bow', wpn: 'bow', crest: 0xd9a441, cape: 0xb03a2e, coat: 0x6a4a2a, scale: 1.12, hero: 1 } },
  pers: { id: 'kiros', name: 'Büyük Kiros', icon: '🦁', kitBase: 'spearman', cls: 'infantry', hp: 320, atk: 14, armor: 4, speed: 2.6, rof: 1.3, bonus: { infantry: 1.2, cavalry: 1.5 },
    desc: 'Pers İmparatorluğu’nun kurucusu. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'kneel', anim: 'guard', head: 'kidaris', body: 'robe', wpn: 'dory', shield: 1, shieldLook: 'wicker', crest: 0xd9a441, cape: 0x6a2a8a, scale: 1.15, hero: 1 } },
  rus: { id: 'nevski', name: 'Aleksandr Nevski', icon: '❄️', kitBase: 'knight', cls: 'cavalry', hp: 340, atk: 15, armor: 4, speed: 3.4, rof: 1.5, bonus: { infantry: 1.2, cavalry: 1.15 },
    desc: 'Buz Savaşı’nın kahramanı knez. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { cav: 1, anim: 'slash', head: 'conic', body: 'scale', wpn: 'spatha', shield: 1, shieldLook: 'kite', crest: 0xd9a441, cape: 0xb02a2a, coat: 0x4a3220, scale: 1.12, hero: 1 } },
  yunan: { id: 'leonidas', name: 'Leonidas', icon: '🛡️', kitBase: 'spearman', cls: 'infantry', hp: 310, atk: 15, armor: 5, speed: 2.6, rof: 1.3, bonus: { infantry: 1.2, cavalry: 1.5 },
    desc: 'Thermopylae’nin Spartalı kralı. Yanındaki askerler daha sert vurur ve daha zırhlıdır.', kit: { die: 'kneel', anim: 'phalanx', head: 'corinth', body: 'muscle', wpn: 'dory', shield: 1, shieldLook: 'aspis', crest: 0xb02a2a, cape: 0xb02a2a, scale: 1.15, hero: 1 } },
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
      speed: h.speed, range: h.range || 0, rof: h.rof, los: 9, pop: h.pop || 1, bonus: { ...h.bonus }, proj: h.proj || null, civ, hero: true, kitBase: h.kitBase, kit: h.kit, look: '' };
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
