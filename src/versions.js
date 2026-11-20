// Release notes of this fork: the "Yenilikler" window of the main menu (ui.js _menuNews) and the 3D showcase
// (vitrin.html) read this. Newest first. The game's version is the first entry's v.
//   items     what changed, in plain words (grouped: [heading, [lines]])
//   showcase  the models this version added or changed: { id, kind: 'unit' | 'building', tags, note }
//             tags: 'yeni' (new model), 'gorunus' (new look), 'animasyon' (new animation); note: what to look at.
//             The showcase shows these first; a version without any has no "Vitrinde gör" button.
// Rule of thumb (same as the card game): changes made on the same day go into the same version.
export const VERSIONS = [
  {
    v: '1.0', date: '2026-11-20', title: 'Medeniyetler',
    intro: 'Aevum çatalının ilk sürümü: 20 medeniyet, her birinin bonusları, özel birliği ve kendi oynayış tarzı.',
    items: [
      ['Medeniyetler', [
        '20 medeniyet eklendi. Her birinin maç başından geçerli pasif bonusları var (can, saldırı, kaynak toplama, ticaret...).',
        'Tek oyunculuda Yeni Oyun ekranından, çok oyunculuda lobiden seçilir. Zarı atarsan şerit döner ve şansına biri çıkar.',
        'Her medeniyetin bir özel birliği var: standart bir birliğin yerine geçer, aynı binadan aynı çağda üretilir (düğmede ★).',
      ]],
      ['Görünüş ve animasyon', [
        'Özel birliklerin her birinin kendi başlığı, gövdesi, silahı ve kalkanı var.',
        'Savaş Fili gerçek bir filin, Deve Süvarisi gerçek bir devenin sırtında: hortum, kulak ve boyun kendi başına oynar.',
        'Her özel birliğin kendi dövüş biçimi var: yandan kesme, kalkan arkasından saplama, kargı hücumu, yukarı atış...',
        'Ölüm animasyonları: yayalar üç ayrı biçimde düşer (sırtüstü, dizlerinin üstüne çöküp yüzüstü, dönerek yana); at şaha kalkıp devrilir, deve ön ayaklarını kırar, fil başını kaldırıp ağır ağır yana yatar.',
      ]],
      ['Yapay zekâ', [
        'Botlar medeniyetine göre oynar: Baskıncı, Ekonomist, Savunmacı, Taktikçi ya da Dengeli.',
        'Bot, medeniyetinin özel birliğini ve bonus aldığı birlik türlerini daha çok basar.',
      ]],
      ['Topluluk', [
        'Ana menünün sol altında Genel Sohbet: siteye giren herkes okur, Google ile giriş yapanlar yazar. Son 60 satır gösterilir; sunucu yeniden başlayınca sohbet sıfırlanır.',
        'Google ile giriş (isteğe bağlı): ad, avatar, TP, maç geçmişi ve kayıtlı oyunlar hesaba bağlanır, her bilgisayarda seninle gelir. Giriş yapmayan misafir olarak oynar; kayıtları o tarayıcıda kalır.',
        'Giriş yapınca arkadaş ekleyebilir, çevrim içi oyuncuları görüp odana davet edebilirsin. Misafirler de odalara katılabilir.',
      ]],
      ['Denge', [
        'Medeniyetler bot maçlarıyla ölçüldü (1600 maç); uçtakiler ortaya doğru ayarlandı. Ayarlar tahmindir, yeniden ölçülmedi.',
      ]],
      ['Oyun ve menü', [
        'Giriş gerekmez: oyun doğrudan açılır, çok oyunculu oda koduyla çalışır, adını lobide değiştirirsin.',
        'Yeni menü görünümü: kapak resmi, iki karolu ana ekran, altın çerçeveli pencereler, portreli medeniyet şeridi.',
        'Yenilikler penceresi ve 3B vitrin eklendi.',
      ]],
      ['Oyun içi arayüz', [
        'Kaynaklar üst çubuktan mini haritanın yanına taşındı. Her kaynağın yanında o an o kaynakta çalışan köylü sayısı yazar (dakikalık gelir yerine); balıkçı tekneleri yiyeceğe sayılır. Boşta köylü düğmesi panelin en üstünde, nüfus en altında.',
        'Sonraki çağın gerektirdikleri mini haritanın üstünde simgelerle görünür (kaynak bedeli, bina türü sayısı, gereken yapılar, bekleme süresi): karşılanan yeşil, eksik kırmızı. Yanındaki Çağ Atla düğmesi hazır olunca altın renkte parlar; şehir merkezini seçmeden oradan çağ atlanır.',
        'Kısayol grupları (1-9) panellerin altından sağ alt köşeye taşındı; alttaki paneller artık en alta oturuyor.',
        'Arayüz ekran boyutuna göre ölçeklenir: 2K ekranda tam boy, Full HD ve daha küçük ekranlarda küçülür, oyun alanını daraltmaz.',
        'Oyun içindeki bütün paneller menülerle aynı görünüme geçti: seçim paneli, yapıların üretim kuyruğu, komut kartı, ipuçları, görevler, bildirimler, teknoloji ağacı, istatistikler, duraklatma menüsü.',
      ]],
      ['Düzeltmeler', [
        'Özel birlikler düğmeden basılamıyordu, düzeldi.',
      ]],
    ],
    showcase: [
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
