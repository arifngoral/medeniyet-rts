# Medeniyet RTS (Aevum çatalı)

> Bu depo [Aevum](https://github.com/flickrz/aevum-rts)'un bir çatalıdır (fork): üstüne **medeniyetler** eklenir.
> Kod Aevum gibi AGPL v3. "Aevum" adı ve logosu asıl projeye aittir; bu çatalın oyun içindeki adı "Medeniyet" (`src/brand.js`).
>
> **Menü görünümü:** `menu.css` (kapak resmi, iki karolu ana ekran, altın çerçeveli pencereler, medeniyet afiş şeridi); çizimler
> `assets/ui/` ve `assets/civ/` (CC BY 4.0, bkz. `assets/LICENSE.md`). Oyun içi arayüz asıl projedeki gibidir.
>
> **Girişsiz oynanır (misafir modu):** bu çatalda hesap sistemi kapalı gelir (`src/cloud/config.js` boş). İlk açılışta yerel bir profil
> oluşur, çok oyunculu oda koduyla çalışır, ad lobide değiştirilir. Arkadaş listesi, bulut kaydı ve TP puanı bu modda yoktur.
> Hesapları açmak için kendi Firebase projeni `src/cloud/config.js`'e yaz ve sunucuyu `AEVUM_FIREBASE_PROJECT=<id>` ile başlat.
> Aşağıdaki asıl README'de girişle ilgili yazanlar hesap açıkken geçerlidir.
>
> **Medeniyetler:** 20 medeniyet, her birinin maç başından geçerli pasif bonusları var (`src/civs.js`, veri `src/civ-data.js`).
> Tek oyunculuda Yeni Oyun ekranından, çok oyunculuda lobiden seçilir; "Rastgele" maç tohumundan belirlenir. Test: `node test/civ-test.mjs`.
> Her medeniyetin bir **özel birliği** var (`src/civ-units.js`): standart bir birliğin yerine geçer (Roma'da Kılıç Ustası yerine Lejyoner,
> Moğollarda Hafif Süvari yerine atlı okçu Mangudai...), aynı binadan aynı çağda üretilir; görünüşü temel birliğin donanımına sorguç / pelerin / boy eklenerek çizilir.

# Aevum

**Oyna:** https://aevum-8clf.onrender.com · **English:** see [CONTRIBUTING.md](CONTRIBUTING.md)

Tarayıcıda çalışan, özgün bir 3B gerçek zamanlı strateji oyunu. Taş Devri'nden Sanayi Çağı'na beş çağ boyunca köy kur, kaynak topla, ordu bas, rakibi yık.

## Çalıştırma

- `baslat.bat` dosyasına çift tıkla (Node.js gerekir). Tarayıcıda `http://localhost:5173` açılır.
- Elle: `node server.js`, sonra tarayıcıdan `http://localhost:5173`.
- Arkadaşınla internet üzerinden oynamak için `baslat-online.bat`: sunucuyu başlatır ve localhost.run üzerinden geçici bir adres açar (OpenSSH gerekir).
- Three.js CDN'den yüklenir, ilk açılışta internet gerekir. Kurulum / derleme adımı yok.

## Kontroller

| Tuş / fare | İşlev |
|---|---|
| Sol tık / sürükle | Seç / kutu ile seç |
| Shift + sol tık | Seçime ekle / çıkar |
| Çift tık | Ekrandaki aynı türden tüm birimleri seç |
| Sağ tık | Yürü, saldır, topla, inşa et / onar; bina seçiliyken toplanma noktası |
| Shift + sağ tık | Komutu sıraya ekle |
| WASD / ok tuşları / ekran kenarı | Kamerayı kaydır (WASD yalnızca kamerayı oynatır) |
| Fare tekerleği | İmlece doğru yakınlaş / uzaklaş |
| Orta tuş sürükle | Kamerayı döndür |
| Ctrl+1..9 / 1..9 | Grup ata / seç (çift bas: kamerayı götür) |
| Home / Backspace | Şehir merkezine git |
| Boşluk | Son uyarının olduğu yere git |
| . (nokta) / Tab | Sıradaki boşta köylü |
| Delete | Seçili kendi birimini / binanı sil |
| Esc | Yerleştirmeyi iptal et / seçimi bırak |
| Q E R T Y / F G H J K / Z X C V B | Komut kartı düğmeleri (ızgara sırasıyla) |
| Enter | Sohbet (çok oyunculu) |
| P / F10 | Duraklat (tek oyunculu) |
| F5 | Hızlı kayıt (tek oyunculu) |

Bina yerleştirirken: sol tık yerleştirir, Shift basılıyken yerleştirmeye devam eder, duvarı sürükleyerek hat halinde çekebilirsin, sağ tık / Esc iptal.

## Özellikler

- 5 çağ, 22 birim (gemiler dahil), 26 bina, teknolojiler, pazar ticareti, görevler
- 1-3 yapay zekâ rakip, üç zorluk, üç harita boyu, kum havuzu modu
- Harita türleri: Nehir Vadisi, Kıta, Yaylalar, Ovalar, İç Deniz, Adalar veya Rastgele (tohumdan seçilir)
- Çok oyunculu: oda kodlu lobi, en fazla 8 oyuncu (insan veya yapay zekâ), takımlar, sohbet, deterministik lockstep; kayıtlı çok oyunculu maça devam etme
- Savaş sisi, tarla döngüsü, kayıt / yükleme (tarayıcıda IndexedDB), 90 saniyede bir otomatik kayıt
- Ana menünün arkasında kendi kendine oynayan demo sahne

## Dürüst notlar

- Modüller paralel yazıldı; bu sürümde uçtan uca oyun testi yapılmadı, hata çıkabilir.
- Harita editörü ve senaryo/kampanya yok.
- Kontrol grupları kayda dahil değil (yüklemeden sonra sıfırlanır).
- Duvarı sürüklerken önizleme yalnızca uç karoyu gösterir.
- Kayıtlar tarayıcıya özeldir; tarayıcı verisi silinirse kayıtlar da gider.

## Geliştirmeye katıl

Aevum açık kaynak; herkes geliştirebilir. Nasıl çalıştırılır, testler, PR kuralları: [CONTRIBUTING.md](CONTRIBUTING.md).

- Yerelde (`localhost`) yeni oyun ekranında **Geliştirici modu** çıkar: tüm harita açık, sınırsız kaynak, çağ değiştirme.
- Çok oyunculu ve hesap özellikleri için kendi Firebase projeni bağlayabilirsin (CONTRIBUTING.md).

## Lisans

- **Kod:** [GNU AGPL v3](LICENSE) (veya sonraki sürüm). Kullan, değiştir, paylaş; ama değiştirdiğin kodu, sunucuda çalıştırıp başkalarına açsan bile, aynı lisansla açık paylaşmak zorundasın.
- **3D modeller:** CC BY-NC-SA 4.0 (ticari kullanım yok). **İkonlar:** CC BY 3.0. **Sesler:** dosya dosya, bazıları açık değil. Ayrıntı: [assets/LICENSE.md](assets/LICENSE.md).
- **"Aevum" adı ve logosu** hiçbir lisansa dahil değil; fork'lar başka bir ad kullanmalı.
