# Çağ binalarının üretilmiş 3B modelleri

Ana binalar gibi (çizim → 3B → küçültme) çağ binası modelleri. Oyun bir binanın dosyası varsa onu, yoksa `src/render/lm/`
içindeki kodla çizilmiş modeli kullanır. Dosyası olanlar `src/render/glb-models.js` `LM_GLB` listesinde; dosyalar
`assets/models/lm/<id>.glb`.

1. **Çizim** (bedava, FLUX.1-schnell, Apache 2.0; Hugging Face oturumsuz kotası günde ~1-2 çizim):
   `node flux.mjs out/lm_xxx.png "Isometric 3/4 view of <bina>: ... Stylized hand-painted low-poly strategy game building asset like Age of Empires 4, warm colors, a small blue banner, single building centered, whole building visible, plain white background, no ground, no shadow, no text."`
   Mavi sancak önemli: oyun o maviyi oyuncu rengine boyar.
2. **3B** (Hunyuan 3D, https://hy3d.tencent.ai, oturum açık; bedava günde 5): çizim sayfaya GitHub'daki `lm-cizim` dalından
   (raw.githubusercontent.com) aktarılır (sayfa yerel adresten dosya alamıyor), Image-to-3D, yüz sayısı 50k. Bitince
   `/api/3d/creations/detail?creationsId=…` yanıtındaki `textureGlb` adresinden indirilir.
3. **Küçültme**: `node kucult.mjs ham.glb ../../assets/models/lm/lm_xxx.glb 9000 512` (tek parça, ~9 bin üçgen, 512 px jpeg
   doku, meshopt). Sonra `LM_GLB` listesine ekle.

Bağımlılıklar repoda değil; geçici bir klasörde: `npm i @gltf-transform/core @gltf-transform/extensions @gltf-transform/functions meshoptimizer sharp`
(betikleri oradan çalıştır).
