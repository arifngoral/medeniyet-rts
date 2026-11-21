# Blender'da kurulan çağ binası modelleri

Hunyuan 3D yoluna (`tools/lm-glb/`) seçenek: bina Gemini çizimine bakılarak Blender'da Python betiğiyle yüz yüz kurulur.
Kota ya da oturum gerekmez, üçgen sayısı baştan denetlenir.

1. **Çizim**: Gemini'de "Isometric 3/4 top-down view of <bina> as a stylized hand-painted low-poly strategy game building asset, Age of Empires 4 style ...
   one small blue banner ..., single building centered, plain white background, no ground, no shadow, no text." Çizim yalnız göz için kullanılır, diske yazılmaz.
2. **Betik** `tools/lm-blender/<ad>.py`. Ortak araçlar `ortak.py`: `Yapi.yuz` / `yuz_yon` / `serit` / `kutu` / `prizma` / `koni` / `kubbe` (yarım kubbe:
   `t0`, `t1`) / `kemerli` (derinliği olan kemer açıklığı; `sivri` > 0 sivri kemer, `v0` pencere denizliği, `korkuluk`) / `pencere`.

## Detay yolu (yeni modeller; ör. `suleymaniye.py`)

Yakınlaşınca da keskin: renkler ve pişirilmiş ortam gölgesi KÖŞE RENKLERİNDE, doku yalnız 512 px tekrarlanan kesme taş deseni (`doku.py` `detayli_aktar`,
`karo_desen`; taş yüzlere model biriminde kutu izdüşümüyle serilir, `KARO` = 4 sıra; öteki malzemeler desenin düz beyaz noktasını okur). Dosya
`extras { detay: 1, yumusak: 1 }`; oyun (`glb-models.js` `prepare` / `look`) köşe rengi × deseni çizer, sancak mavisini köşe renginden boyar.
Canlı izleme: `blender --factory-startup --python tools/lm-blender/canli.py -- suleymaniye cikti.glb [hız]` (pencereli; bölüm adları `Yapi.bolum`).
Sıkıştırma aşağıdaki gibi (jpeg + meshopt). Süleymaniye ~58 bin üçgen, ~1,9 MB (meshopt: `--quantize-color 12 --quantize-normal 12`, yoksa kubbelerde basamak olur). Eğri yüzlere yüz başına ton farkı verilmez (mozaik gibi görünüyordu); kurşun kubbeler meridyen şeritli (`kursun` / `kursun2`).

## Dokulu yol (atlas; eski, yakında pikselleşiyordu)

Yüzlere renk yerine malzeme adı verilir (`doku.py` `MALZEME`: `tas` derzli kesme taş, `kursun`, `altin`, `mermer`, `cam`, `ahsap`, `zemin`, `mavi` sancak ...).
`nesne_dokulu` yüzleri kaynaştırır, açıya göre keskin kenarlı yumuşak gölgeler (kubbe, minare yuvarlak; köşeler keskin), UV açar;
`pisir_ve_aktar` Cycles'ta malzemeleri ve ortam gölgesini (AO) tek 2048 dokuya pişirir (sancak mavisi AO'suz kalır: oyun onu renginden bulur)
ve `extras.yumusak = 1` ile dışa aktarır: oyun (`glb-models.js` `plainGeo`) o dosyanın normallerini korur, öteki dosyalar eskisi gibi düz gölgelenir.

```
blender -b --factory-startup --python tools/lm-blender/suleymaniye.py -- ham.glb onizleme.png
gltf-transform jpeg ham.glb j.glb --quality 70
gltf-transform meshopt j.glb assets/models/lm/lm_suleymaniye.glb --level medium --quantize-color 12 --quantize-normal 12
```
(`gltf-transform`: geçici bir klasörde `npm i @gltf-transform/cli@4`.) Süleymaniye ~27 bin üçgen, ~1 MB.

## Köşe renkli yol (eski; `kolezyum.py`)

Yüzlere sRGB renk verilir, `Yapi.nesne(ad, dikey)` dokusuz köşe renkli tek mesh yapar, oyun düz gölgeler. Sancak mavisi ör. `(0.12, 0.33, 0.86)`.
`blender -b --factory-startup --python tools/lm-blender/kolezyum.py -- assets/models/lm/lm_kolezyum.glb onizleme.png`

Sonra id'yi `glb-models.js` `LM_GLB` listesine ekle; büyük görünüm `model.html?id=<id>`, oyundaki hâli vitrinin "Çağ binaları" sekmesi.

Yapılanlar: Kolezyum, Süleymaniye (dokulu, 2026-11-22).
