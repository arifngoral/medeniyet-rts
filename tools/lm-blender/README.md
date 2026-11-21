# Blender'da kurulan çağ binası modelleri

Hunyuan 3D yoluna (`tools/lm-glb/`) seçenek: bina Gemini çizimine bakılarak Blender'da Python betiğiyle yüz yüz kurulur. Kota ya da oturum gerekmez,
üçgen sayısı baştan denetlenir. Çıktı dokusuz, köşe renkli tek parça GLB'dir: oyun bunu `glb-models.js`'in dokusuz yolundan okur, doygun mavi
(sancak) oyuncu rengine boyanır.

1. **Çizim**: Gemini'de "Isometric 3/4 top-down view of <bina> as a stylized hand-painted low-poly strategy game building asset, Age of Empires 4 style ...
   one small blue banner ..., single building centered, plain white background, no ground, no shadow, no text." Çizim yalnız göz için kullanılır, diske yazılmaz.
2. **Betik**: `tools/lm-blender/<ad>.py` (ortak araçlar `ortak.py`: `Yapi.yuz` / `serit` / `kutu` / `silindir`, `nesne(ad, dikey)` köşe renkli tek mesh,
   `disa_aktar`, `onizle` workbench önizlemesi). Renkler sRGB yazılır; sancak mavisi ör. `(0.12, 0.33, 0.86)`.
3. **Üretim**: `"C:/Program Files/Blender Foundation/Blender 5.3/blender.exe" -b --factory-startup --python tools/lm-blender/kolezyum.py -- assets/models/lm/lm_kolezyum.glb onizleme.png`
   (konsolda `UCGEN` üçgen sayısı; hedef ~9 bin). Sonra id'yi `glb-models.js` `LM_GLB` listesine ekle, vitrinin "Çağ binaları" sekmesinde bak.

Yapılanlar: Kolezyum (2026-11-22).
