// Release notes of this fork: the "Yenilikler" window of the main menu (ui.js _menuNews) and the 3D showcase
// (vitrin.html) read this. Newest first - inside a version too: a new group goes above the others and a new line to
// the top of its group (owner 2026-11-20: the latest change must be the first thing you read). The game's version is
// the first entry's v.
//   items     what changed, in plain words (grouped: [heading, [lines]])
//   showcase  the models this version added or changed: { id, kind: 'unit' | 'building', tags, note }
//             tags: 'yeni' (new model), 'gorunus' (new look), 'animasyon' (new animation); note: what to look at.
//             The showcase shows these first, in this order (newest first as well); a version without any has no
//             "Vitrinde gör" button.
// Rule of thumb (same as the card game): changes made on the same day go into the same version.
export const VERSIONS = [
  {
    v: '1.0', date: '2026-11-20', title: 'Medeniyetler',
    intro: 'Aevum çatalının ilk sürümü: 20 medeniyet, her birinin bonusları, iki özel birliği ve kendi oynayış tarzı.',
    items: [
      ['Çağ binaları ve efsaneler', [
        'AoE4 gibi çağ atlama (şimdilik 5 medeniyette: Türkler, Romalılar, Japonlar, Mısırlılar, Vikingler): Şehir Merkezi\'nden çağ atlanmaz, köylüler bir çağ binası kurar, bina bitince çağ atlanır. Bina türü şartı ve çağda bekleme süresi yok; bedel, çağın bedelidir.',
        'Her çağ geçişi için iki bina var, birini seçersin: biri çoğunlukla ekonomi, öteki savaş. Her binanın ayakta durduğu sürece işleyen kendi etkisi var (toplama, üretim hızı, düzenli altın, iyileştirme, kendisi ok atan kaleler...). Yıkılırsa etkisi biter, çağ kalır.',
        '40 yeni bina modeli: Söğüt Kervansarayı, Ulu Cami, Rumeli Hisarı, Süleymaniye, Dolmabahçe; Forum, Pantheon, Kolezyum, Su Kemeri, Zafer Takı; Altın Köşk, Himeji Kalesi, Fushimi torileri; Karnak, Büyük Sfenks, Büyük Piramit, Abu Simbel, İskenderiye Feneri; Uzun Ev, Hof Tapınağı, Uppsala, Jomsborg, Valhalla...',
        'Efsane karakterler: Fatih Sultan Mehmed, Julius Caesar, Miyamoto Musashi, II. Ramses (altın savaş arabasında), Ragnar Lothbrok. Çağ binalarından basılır, aynı anda yalnız bir tane olur, ölürse yeniden basılır; çağ atladıkça güçlenir, yanındaki askerlere +%15 saldırı ve +1 zırh verir. Ayaklarının altında altın halka var.',
        'Çağ Atla düğmesi bu medeniyetlerde köylüleri seçip iki binayı gösterir; köylü menüsünde "Çağ Binası" sayfası da var. Botlar da çağ binası kurar ve efsanesini basar.',
        'Vitrinde "Çağ binaları" ve "Efsaneler" sekmeleri.',
        'Öteki 15 medeniyet şimdilik eski usulle (Şehir Merkezi\'nden) atlar. Çağ binalı medeniyetler daha erken çağ atlıyor; denge ölçülmedi.',
      ]],
      ['İkinci özel birlikler', [
        'Her medeniyete ikinci bir özel birlik geldi (20 yeni birlik). İlkinden farklı bir standart birliğin yerine geçer: Türklerde Yeniçeri (Tüfekçi), Romalılarda Praetoryan (Ağır Piyade), Japonlarda Teppō Ashigaru (Tüfekçi), Mısırlılarda Savaş Arabası (Hafif Süvari), Vikinglerde Huskarl (Mızrakçı), Moğollarda Keşik (Şövalye), Çinlilerde Ateş Mızraklı (Mızrakçı), Perslerde Tırpanlı Araba (Şövalye), Yunanlarda Peltast (Okçu), Bizanslılarda Varang Muhafızı (Ağır Piyade), Franklarda Franciska Baltacısı (Kılıç Ustası), İngilizlerde Kırmızı Ceketli (Piyade Tüfekçisi), İspanyollarda Konkistador (Zırhlı Süvari), Araplarda Memlûk (Zırhlı Süvari), Hintlilerde Racput (Kılıç Ustası), Korelilerde Woldo Muhafızı (Mızrakçı), Azteklerde Kartal Savaşçısı (Okçu), Kartacalılarda Balear Sapancısı (Okçu), Ruslarda Kazak (Hafif Süvari), Malililerde Farima Atlısı (Şövalye).',
        'Hepsinin kendi başlığı, gövdesi, silahı ve kalkanı var: Yeniçeri börkü, ayı postu kalpak, kartal gagalı miğfer, morion, hilal kalkan, hilal ağızlı pala, sapan...',
        'Savaş arabası modeli: önde at, arkada iki tekerlekli araba, okçu ayakta durur; tekerlekler yürürken döner. Pers arabasının tekerleklerinde tırpan var.',
        'Yeni dövüş biçimleri: tüfekçiler yan dönüp nişan alır ve tepmeyle namlu kalkar, Woldo Muhafızı palayı iki elle yatay savurur, sapancı taşı fırlatıp sapanı başının üstünde yeniden döndürür, Varang baltayı iki elle indirir.',
        'Peltastın ciridi, Kartal Savaşçısının oku ve sapancının taşı havada kendi biçimiyle uçar.',
        'Botlar iki özel birliğin türünü de daha çok basar. Denge: ikinci birlikler ilklerden biraz daha ılımlı tutuldu; bot ligiyle henüz ölçülmedi.',
      ]],
      ['Oyun ve menü', [
        'Ana menünün kapak resmi baştan çizildi: aynı sahne (kale, cami, piramitler, pagoda, nehir boyunca ordugâhlar), çok daha keskin ve ayrıntılı (2752×1536).',
        'Ana ekranın alt menüsü yenilendi: Sandbox, Yenilikler, Vitrin, Nasıl Oynanır ve Ayarlar karoların altında simgeli yuvarlak düğmeler, adı altında yazar; okunmamış yenilikte altın nokta yanar. Google ile Giriş menüden ayrıldı, sağ üstte kendi düğmesi var.',
        "Devam Et ve Kayıtlı Oyunlar ana menüden Tek Oyunculu'nun içine taşındı: yarıda kalan oyunun varsa Tek Oyunculu'ya tıklayınca kaldığın yerden devam etmek isteyip istemediğin sorulur, öteki kayıtlar da orada listelenir.",
        'Yenilikler penceresi ve 3B vitrin eklendi. Yenilikler en yeniden eskiye sıralanır: en son değişiklik en üstte.',
        'Yeni menü görünümü: kapak resmi, iki karolu ana ekran, altın çerçeveli pencereler, portreli medeniyet şeridi.',
        'Giriş gerekmez: oyun doğrudan açılır, çok oyunculu oda koduyla çalışır, adını lobide değiştirirsin.',
      ]],
      ['Oyun içi arayüz', [
        'Kaynaklar üst çubuktan mini haritanın yanına taşındı. Her kaynağın yanında o an o kaynakta çalışan köylü sayısı yazar (dakikalık gelir yerine); balıkçı tekneleri yiyeceğe sayılır. Boşta köylü düğmesi ve nüfus panelin en üstünde, yan yana.',
        'Arayüz ekran boyutuna göre ölçeklenir: 2K ekranda tam boy, Full HD ve daha küçük ekranlarda küçülür, oyun alanını daraltmaz.',
        'Kısayol grupları (1-9) panellerin altından sağ alt köşeye taşındı; alttaki paneller artık en alta oturuyor.',
        'Sonraki çağın gerektirdikleri mini haritanın üstünde simgelerle görünür (kaynak bedeli, bina türü sayısı, gereken yapılar, bekleme süresi): karşılanan yeşil, eksik kırmızı. Yanındaki Çağ Atla düğmesi hazır olunca altın renkte parlar; şehir merkezini seçmeden oradan çağ atlanır.',
        'Oyun içindeki bütün paneller menülerle aynı görünüme geçti: seçim paneli, yapıların üretim kuyruğu, komut kartı, ipuçları, görevler, bildirimler, teknoloji ağacı, istatistikler, duraklatma menüsü.',
      ]],
      ['Sandbox', [
        'Sandbox önce bir seçim ekranı açar: medeniyet, harita türü, iklim ve başlangıç çağı seçilir.',
        'Sağ üstteki Sandbox panelinden istediğin çağa tek tıkla geçilir (geri de dönülür); bekleme, bina şartı ve bedel yok.',
        '⚡ Anında (açık gelir): binalar yerleştirildiği anda biter, birlik / teknoloji / çağ sırası beklemeden tamamlanır, kaynaklar hiç bitmez. Kapatınca eski 2 kat hız kalır.',
      ]],
      ['Topluluk', [
        'Ana menünün sol altında Genel Sohbet: siteye giren herkes okur, Google ile giriş yapanlar yazar. Son 60 satır gösterilir; giriş yapanların yazdıkları kalıcıdır, sunucu yeniden başlasa da kaybolmaz.',
        'Google ile giriş (isteğe bağlı): ad, avatar, TP, maç geçmişi ve kayıtlı oyunlar hesaba bağlanır, her bilgisayarda seninle gelir. Giriş yapmayan misafir olarak oynar; kayıtları o tarayıcıda kalır.',
        'Giriş yapınca arkadaş ekleyebilir, çevrim içi oyuncuları görüp odana davet edebilirsin. Misafirler de odalara katılabilir.',
      ]],
      ['Medeniyetler', [
        '20 medeniyet eklendi. Her birinin maç başından geçerli pasif bonusları var (can, saldırı, kaynak toplama, ticaret...).',
        'Tek oyunculuda Yeni Oyun ekranından, çok oyunculuda lobiden seçilir. Zarı atarsan şerit döner ve şansına biri çıkar.',
        'Her medeniyetin özel birlikleri var: her biri standart bir birliğin yerine geçer, aynı binadan aynı çağda üretilir (düğmede ★).',
      ]],
      ['Görünüş ve animasyon', [
        'Özel birliklerin her birinin kendi başlığı, gövdesi, silahı ve kalkanı var.',
        'Savaş Fili gerçek bir filin, Deve Süvarisi gerçek bir devenin sırtında: hortum, kulak ve boyun kendi başına oynar.',
        'Her özel birliğin kendi dövüş biçimi var: yandan kesme, kalkan arkasından saplama, kargı hücumu, yukarı atış...',
        'Ölüm animasyonları: yayalar üç ayrı biçimde düşer (sırtüstü, dizlerinin üstüne çöküp yüzüstü, dönerek yana); at şaha kalkıp devrilir, deve ön ayaklarını kırar, fil başını kaldırıp ağır ağır yana yatar.',
      ]],
      ['Yapay zekâ', [
        'Botlar medeniyetine göre oynar: Baskıncı, Ekonomist, Savunmacı, Taktikçi ya da Dengeli.',
        'Bot, medeniyetinin özel birliklerini ve bonus aldığı birlik türlerini daha çok basar.',
      ]],
      ['Denge', [
        'Medeniyetler bot maçlarıyla ölçüldü (1600 maç); uçtakiler ortaya doğru ayarlandı. Ayarlar tahmindir, yeniden ölçülmedi.',
      ]],
      ['Düzeltmeler', [
        'Özel birlikler düğmeden basılamıyordu, düzeldi.',
      ]],
    ],
    showcase: [
      { id: 'fatih', tags: ['yeni'], note: 'Efsane: sorguçlu beyaz kavuk, kürk yakalı kaftan, eğri kılıç; beyaz at. Ayağının altında altın halka.' },
      { id: 'sezar', tags: ['yeni'], note: 'Efsane: altın defne tacı, tunç zırh, kırmızı pelerin, kısa kılıç.' },
      { id: 'musashi', tags: ['yeni'], note: 'Efsane: tepe topuzu, alın bandı, koyu kimono; iki kılıç, iki elde.' },
      { id: 'ramses', tags: ['yeni'], note: 'Efsane: mavi savaş tacı, altın yakalık; savaş arabasından ok atar.' },
      { id: 'ragnar', tags: ['yeni'], note: 'Efsane: yanları tıraşlı, örgülü saç, çatal sakal; balta ve boyalı kalkan.' },
      { id: 'lm_suleymaniye', kind: 'building', tags: ['yeni'], note: 'Büyük kurşun kubbe, yarım kubbeler, dört minare, iki yanda medrese sıraları.' },
      { id: 'lm_rumelihisari', kind: 'building', tags: ['yeni'], note: 'Üç büyük yuvarlak kule, kurşun külahlar, aralarında surlar.' },
      { id: 'lm_kolezyum', kind: 'building', tags: ['yeni'], note: 'Üç kat kemerli oval arena.' },
      { id: 'lm_pantheon', kind: 'building', tags: ['yeni'], note: 'Kubbeli rotunda, sütunlu revak, üçgen alınlık.' },
      { id: 'lm_himeji', kind: 'building', tags: ['yeni'], note: 'Eğimli taş temel üstünde beş çatılı beyaz kale.' },
      { id: 'lm_kinkakuji', kind: 'building', tags: ['yeni'], note: 'Gölün kıyısında üç katlı altın köşk.' },
      { id: 'lm_sfenks', kind: 'building', tags: ['yeni'], note: 'Aslan gövdeli, mavi çizgili başlıklı sfenks; arkasında küçük piramit.' },
      { id: 'lm_feneri', kind: 'building', tags: ['yeni'], note: 'Kare kaide, sekizgen kat, ateşli fener kulesi.' },
      { id: 'lm_ulfsalon', kind: 'building', tags: ['yeni'], note: 'Altın çatılı büyük salon, duvarlarda kalkanlar, kapıda iki kurt.' },
      { id: 'lm_naust', kind: 'building', tags: ['yeni'], note: 'Çim çatılı tekne sundurması, kızakta çizgili yelkenli drakkar.' },
      { id: 'arabaci', tags: ['yeni', 'animasyon'], note: 'Savaş arabası modeli: önde at, arkada iki tekerlekli araba; okçu ayakta, mavi savaş tacıyla. Tekerlekler yürürken döner.' },
      { id: 'tirpanli', tags: ['yeni', 'animasyon'], note: 'Aynı araba, tekerlek göbeklerinde tırpanlarla. Arabacı uzun başlıklı, kare sakallı; mızrağını indirip saplar.' },
      { id: 'yeniceri', tags: ['gorunus', 'animasyon'], note: 'Arkaya dökülen beyaz börk, önünde altın kaşıklık; mavi dolama, pirinç halkalı uzun tüfek. Yan dönüp nişan alır, tepmeyle namlu kalkar.' },
      { id: 'teppo', tags: ['gorunus', 'animasyon'], note: 'Düz konik hasır şapka, koyu zırh; fitili yanan kara tüfek. Yan dönüp nişan alır.' },
      { id: 'kirmiziceket', tags: ['gorunus', 'animasyon'], note: 'Ayı postu uzun kalpak, kırmızı ceket, çapraz beyaz kayışlar, altın düğmeler.' },
      { id: 'praetoryan', tags: ['gorunus', 'animasyon'], note: 'Yaldızlı miğfer, kulaktan kulağa sorguç; tunç kaslı zırh, mor oval kalkan, uzun kılıç.' },
      { id: 'varang', tags: ['gorunus', 'animasyon'], note: 'Altın bantlı sivri miğfer, sarı uzun sakal, kırmızı kaftan; iki elli baltayı tepeden indirir.' },
      { id: 'huskarl', tags: ['gorunus', 'animasyon'], note: 'Gözlüklü yuvarlak miğfer, kızıl sakal, zincir zırh; boyalı yuvarlak kalkanın arkasından mızrak saplar.' },
      { id: 'woldo', tags: ['gorunus', 'animasyon'], note: 'Kırmızı püsküllü uzun miğfer, altın çivili kaftan; hilal ağızlı palayı iki elle yatay savurur.' },
      { id: 'atesmizrak', tags: ['gorunus', 'animasyon'], note: 'Kırmızı püsküllü çelik miğfer; mızrağın ucunda kırmızı sarılı barut borusu, ağzında kıvılcım.' },
      { id: 'balear', tags: ['gorunus', 'animasyon'], note: 'Kıvırcık saç, başına sarılı yedek sapan. Taşı kolunu kamçılayarak atar, sonra sapanı başının üstünde yeniden döndürür.' },
      { id: 'peltast', tags: ['gorunus', 'animasyon'], note: 'Öne kıvrık Frig başlığı, hilal hasır kalkan, bir tutam cirit; havada cirit uçar.' },
      { id: 'kartal', tags: ['gorunus', 'animasyon'], note: 'Yüz kartalın açık gagasından bakar, tüylü giysi; atlatl ile ok fırlatır.' },
      { id: 'racput', tags: ['gorunus', 'animasyon'], note: 'Yakutlu safran sarık, beyaz sorguç, geniş bıyık; eğri kılıç ve dört göbekli yuvarlak kalkan.' },
      { id: 'franciska', tags: ['gorunus', 'animasyon'], note: 'Altın bantlı dilimli miğfer, uzun saç; kısa balta, belinde yedeği, demir göbekli yuvarlak kalkan.' },
      { id: 'konkistador', tags: ['gorunus', 'animasyon'], note: 'Kalkık kenarlı morion, kırmızı sorguç, çelik göğüslük; uzun ince kılıç. Art arda iki hızlı kesiş.' },
      { id: 'memluk', tags: ['gorunus', 'animasyon'], note: 'Sarıklı sivri miğfer, küçük pirinç kalkan, eğri kılıç; beyaz Arap atı.' },
      { id: 'kazak', tags: ['gorunus', 'animasyon'], note: 'Kırmızı tepeli kalpak, göğsü fişeklikli uzun çerkeska; kabzasız eğri kılıç.' },
      { id: 'kesik', tags: ['gorunus', 'animasyon'], note: 'Uzun sivri, sorguçlu çelik miğfer, kürk kenar; deri pullu zırh, kargı.' },
      { id: 'farima', tags: ['gorunus', 'animasyon'], note: 'Altın bantlı kapitone başlık, yüzü saran beyaz örtü; nakışlı geniş kaftan, kargı ve deri kalkan.' },
      { id: 'fil', tags: ['yeni', 'animasyon'], note: 'Fil modeli: hortum, dişler, çırpan kulaklar, sırtında örtü. Saldırırken başını kaldırıp hortumunu savurur; ölürken dizlerinin üstüne çöküp yana yatar.' },
      { id: 'deve', tags: ['yeni', 'animasyon'], note: 'Deve modeli: tek hörgüç, uzun boyun, ince bacaklar. Rahvan yürür, boynu sallanır; ölürken ön ayaklarını kırar.' },
      { id: 'samuray', tags: ['gorunus', 'animasyon'], note: 'Altın boynuzlu miğfer, bağcıklı zırh, uzun kılıç. Bir sağdan bir soldan yatay keser; dizlerinin üstüne çökerek ölür.' },
      { id: 'lejyoner', tags: ['gorunus', 'animasyon'], note: 'Kırmızı sorguçlu miğfer, şeritli zırh, uzun kırmızı kalkan. Kısa kılıcı kalkanın yanından saplar.' },
      { id: 'berserker', tags: ['gorunus', 'animasyon'], note: 'Ayı postu, çıplak göğüs, uzun saplı balta. Baltayı iki elle savurur; darbeyle dönerek düşer.' },
      { id: 'hoplit', tags: ['gorunus', 'animasyon'], note: 'Kapalı tunç miğfer, uzun sorguç, büyük yuvarlak kalkan. Mızrağı omuz hizasında dümdüz saplar.' },
      { id: 'jaguar', tags: ['gorunus', 'animasyon'], note: 'Jaguar başı ve postu, yeşil tüyler, obsidyenli tahta kılıç. Sıçrayarak çapraz vurur.' },
      { id: 'olumsuz', tags: ['gorunus', 'animasyon'], note: 'Başa sarılı başlık, uzun kaftan, hasır kalkan, altın topuzlu mızrak. Kalkanın arkasından alçak saplar.' },
      { id: 'druzhina', tags: ['gorunus', 'animasyon'], note: 'Sivri çelik miğfer, pullu zırh, badem kalkan. Yukarıdan ağır balta darbesi.' },
      { id: 'almogavar', tags: ['gorunus', 'animasyon'], note: 'Deri başlık, geniş pala, sırtında ciritler. Art arda iki hızlı kesiş.' },
      { id: 'mandinka', tags: ['gorunus', 'animasyon'], note: 'Altın renkli sarık, uzun kaftan, uzun deri kalkan. Art arda iki hızlı dürtme.' },
      { id: 'uzunyay', tags: ['gorunus', 'animasyon'], note: 'Yeşil kukuleta, boyu kadar yay. Yan dönüp geriye yaslanarak uzun çeker.' },
      { id: 'hwarang', tags: ['gorunus', 'animasyon'], note: 'Siyah geniş kenarlı şapka. Yayı yukarı kaldırıp kavisli atar.' },
      { id: 'nubyali', tags: ['gorunus', 'animasyon'], note: 'Bant ve tüy, renkli tüylü oklar. Çömelik, yan duruşta hızlı atar.' },
      { id: 'chukonu', tags: ['gorunus', 'animasyon'], note: 'Geniş hasır şapka, üstü hazneli arbalet. Her ok için kolu pompalar.' },
      { id: 'paladin', tags: ['gorunus', 'animasyon'], note: 'Altın haçlı kapalı miğfer, cübbe, flamalı kargı. Kargıyı indirip uzun saplar; atı şaha kalkıp devrilir.' },
      { id: 'katafrakt', tags: ['gorunus', 'animasyon'], note: 'Yüzü zincirle kapalı miğfer, pullu zırh, flamalı kargı.' },
      { id: 'akinci', tags: ['gorunus', 'animasyon'], note: 'Kürk kenarlı kırmızı börk, tuğlu hafif mızrak.' },
      { id: 'mangudai', tags: ['gorunus', 'animasyon'], note: 'Kürklü sivri başlık, yay. Eyerde sağa sola dönerek ok atar.' },
      { id: 'numidya', tags: ['gorunus', 'animasyon'], note: 'Bant ve tüy, bir tutam cirit. Kolu geriye gidip ciridi savurur.' },
    ],
  },
];
export const VERSION = VERSIONS[0].v;
export const TAG_TR = { yeni: 'Yeni model', gorunus: 'Yeni görünüş', animasyon: 'Yeni animasyon' };
