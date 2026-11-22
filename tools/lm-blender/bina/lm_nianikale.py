# Niani Citadel (lm_nianikale): the royal town of the Mansas of Mali - a battered mud curtain wall with round
# ribbed bastions, entered by a great gate between two tapering towers; inside, the palace court with its own wall
# and, on a terrace, the domed audience hall (the qubba es-Saheli built for Mansa Musa, lime-plastered and painted)
# between two mud wings; before it the Mansa's dais under the silk parasol with its golden bird, guards and
# kneeling courtiers; round huts with conical thatch and granaries inside and outside the walls, baobabs.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mali_ortak import *
from arap_ortak import cini_bant

y = Yapi()
Z0 = 0.03
SX0, SX1, SY0, SY1 = -0.88, 0.88, -0.72, 0.86
SH, SK = 0.2, 0.04
SV = 'siva_krem'

y.bolum('Zemin')
zemin(y, -1.15, 1.15, -1.08, 1.1, Z0, KK, 'toprak_ot', basamak=(), silmeli=True)
# the trodden earth inside the walls
y.yuz_yon([V(SX0 + SK, SY0 + SK, Z0 + 0.002), V(SX1 - SK, SY0 + SK, Z0 + 0.002), V(SX1 - SK, SY1 - SK, Z0 + 0.002), V(SX0 + SK, SY1 - SK, Z0 + 0.002)], 'toprak', Z)
# the road to the gate
y.yuz_yon([V(-0.08, -1.08, Z0 + 0.002), V(0.08, -1.08, Z0 + 0.002), V(0.08, SY0 - 0.002, Z0 + 0.002), V(-0.08, SY0 - 0.002, Z0 + 0.002)], 'toprak', Z)

# ---------------- the curtain wall ----------------
y.bolum('Sur')
yan = [dict(n=9, acik={4: dict(tip='gecit', en=0.75, v0=0, v1=0.16, kemer=0.3)}, kose=False),
       dict(n=8, kose=False), dict(n=9, kose=False), dict(n=8, kose=False)]
sahel_kutu(y, dikdortgen(SX0, SX1, SY0, SY1), Z0 + 0.001 * 0, SH, K, kalin=SK, dam=None, yanlar=yan, payanda_w=0.032,
           payanda_d=0.024, payanda_tepe=0.045, payanda_ust=0.026, toron_sira=(0.45, 0.75), ic_payanda=True, kademe=True)
y.bolum('Burclar')
for (bx, by, r, h) in ((SX0, SY0, 0.11, 0.31), (SX1, SY0, 0.11, 0.31), (SX1, SY1, 0.11, 0.31), (SX0, SY1, 0.11, 0.31),
                       (SX0, 0.07, 0.085, 0.27), (SX1, 0.07, 0.085, 0.27), (0.0, SY1, 0.09, 0.27)):
    burc(y, (bx, by), r, Z0, h, K, dis_aci=math.atan2(by, bx))

# ---------------- the great gate ----------------
y.bolum('Buyuk kapi')
for s in (-1, 1):
    sahel_minare(y, (s * 0.165, SY0), 0.19, 0.125, Z0, 0.48, K, kaburga=2, toron_sira=5, pencereler=((-Y, (0.62,)),), ust=0.055)
kutu_merkez(y, (0, SY0), 0.16, 0.075, 0.07, K, z0=Z0 + SH - 0.004, yuzler='onarkasagsolust')
for k in range(3):
    tepecik(y, (-0.05 + 0.05 * k, SY0 - 0.02), 0.012, Z0 + SH + 0.066, 0.045, K, n=6)
for k in range(5):
    toron(y, V(-0.06 + 0.03 * k, SY0 - 0.0375, Z0 + SH + 0.035), -Y, 0.016, 0.005)
# the gate's leaves standing open inside, studded
for s in (-1, 1):
    kutu_merkez(y, (s * 0.068, SY0 + SK + 0.04), 0.006, 0.075, 0.13, 'ahsap_koyu', z0=Z0)
    for zz in (0.04, 0.09):
        kutu_merkez(y, (s * 0.0645, SY0 + SK + 0.04), 0.0012, 0.07, 0.004, 'demir', z0=Z0 + zz)
for s in (-1, 1):
    kisi(y, s * 0.1, SY0 - 0.08, Z0, -math.pi / 2, 'boya_kirmizi', 'beyaz', mizrak='ahsap', kalkan='kiremit')
    kisi(y, s * 0.1, SY0 + SK + 0.07, Z0, -math.pi / 2, 'boya_kirmizi', 'beyaz', mizrak='ahsap', kalkan='kiremit')

# ---------------- the palace court ----------------
y.bolum('Saray avlusu')
PX0, PX1, PY0, PY1 = -0.5, 0.5, -0.14, 0.7
yanp = [dict(n=5, acik={2: dict(tip='gecit', en=0.55, v0=0, v1=0.095, kemer=0.3)}), dict(n=4), dict(n=5), dict(n=4)]
sahel_kutu(y, dikdortgen(PX0, PX1, PY0, PY1), Z0, 0.115, K, kalin=0.026, dam=None, yanlar=yanp, payanda_w=0.026,
           payanda_d=0.018, payanda_tepe=0.035, kose_w=0.05, kose_tepe=0.06, kose_ust=0.03, payanda_ust=0.02, toron_sira=(0.6,))
# the gate of the court: two pinnacled piers
for s in (-1, 1):
    payanda(y, V(s * 0.1, PY0), X, -Y, Z0, Z0 + 0.19, 0.04, 0.032, K, 0.06, arka_z=Z0 + 0.115)

# ---------------- the audience hall ----------------
y.bolum('Kabul salonu')
T = Z0 + 0.045
with parca(y, (0, 0, Z0)):
    zemin(y, -0.42, 0.42, 0.12, 0.62, 0.045, KK, 'kum_acik', basamak=(('on', 0.22),), n_basamak=3)
HC = (0.0, 0.4)
HW = 0.38
HH = 0.40
hk = dikdortgen(HC[0] - HW / 2, HC[0] + HW / 2, HC[1] - HW / 2, HC[1] + HW / 2)
yanh = [dict(n=3, acik={1: dict(tip='kapi', en=0.55, v0=0, v1=0.19, kemer=0.35), 0: dict(tip='pencere', en=0.35, v0=0.13, v1=0.2, kafes=True),
                         2: dict(tip='pencere', en=0.35, v0=0.13, v1=0.2, kafes=True)}),
        dict(n=3, acik={1: dict(tip='pencere', en=0.35, v0=0.13, v1=0.2, kafes=True)}),
        dict(n=3), dict(n=3, acik={1: dict(tip='pencere', en=0.35, v0=0.13, v1=0.2, kafes=True)})]
HD = T + HH - 0.035
sahel_kutu(y, hk, T, HH, SV, kalin=0.035, dam=HD, dam_key='toprak', yanlar=yanh, payanda_w=0.034, payanda_d=0.026,
           payanda_tepe=0.06, kose_w=0.07, kose_tepe=0.1, kose_ust=0.05, payanda_ust=0.035, toron_sira=(0.4, 0.7),
           kose_yumurta=True)
# the painted frieze under the parapet (red, black and white triangles of the court's designs)
for i in range(4):
    a, b = hk[i], hk[(i + 1) % 4]
    cini_bant(y, a, b, T + HH * 0.82, 0.028, keys=('boya_kirmizi', 'koyu', 'beyaz', 'koyu'), n=14, d=0.0025)
# the drum and the dome
DR_ = 0.15
donel(y, HC, [(DR_, HD - 0.002), (DR_, HD + 0.06), (DR_ * 1.06, HD + 0.066), (DR_ * 1.06, HD + 0.072), (DR_, HD + 0.072)], SV, n=24)
for i in range(16):
    t = TAU * (i + 0.5) / 16
    d = V(math.cos(t), math.sin(t))
    toron(y, V(HC[0], HC[1], HD + 0.032) + d * (DR_ - 0.003), d, 0.02)
y.kubbe(HC, DR_, HD + 0.072, 0.29, SV, n=24, kat=7)
for i in range(8):   # ribs over the dome
    t = TAU * i / 8
    pts = [V(HC[0] + DR_ * 1.01 * math.cos(ph) * math.cos(t), HC[1] + DR_ * 1.01 * math.cos(ph) * math.sin(t), HD + 0.072 + 0.29 * 1.01 * math.sin(ph))
           for ph in (0.02, 0.45, 0.9, 1.25)]
    boru(y, pts, 0.008, SV, n=5, r_son=0.005)
zt = tepecik(y, HC, 0.03, HD + 0.072 + 0.285, 0.08, SV, n=10, yumurta=True)
sancak(y, HC[0] - HW / 2 + 0.03, HC[1] - HW / 2 + 0.03, HD + 0.035, boy=0.22, en=0.11, yuk=0.07, aci=math.pi * 0.85)
# the wings
for s in (-1, 1):
    if s < 0:
        wk = dikdortgen(-0.4, -HW / 2 + 0.01, 0.2, 0.58)
        yw = [dict(n=2, acik={0: dict(tip='kapi', en=0.5, v0=0, v1=0.12, kemer=0.3)}), dict(yok=True, kose=False), dict(n=2, kose=False), dict(n=3)]
    else:
        wk = dikdortgen(HW / 2 - 0.01, 0.4, 0.2, 0.58)
        yw = [dict(n=2, acik={1: dict(tip='kapi', en=0.5, v0=0, v1=0.12, kemer=0.3)}, kose=False), dict(n=3), dict(n=2), dict(yok=True, kose=False)]
    sahel_kutu(y, wk, T, 0.2, K, kalin=0.028, dam=T + 0.17, yanlar=yw, payanda_w=0.028, payanda_d=0.02, payanda_tepe=0.04,
               kose_w=0.05, kose_tepe=0.06, kose_ust=0.03, payanda_ust=0.022, toron_sira=(0.55,))

# ---------------- the Mansa's audience ----------------
y.bolum('Mansa')
DX, DY = 0.0, 0.03
kutu_merkez(y, (DX, DY), 0.2, 0.12, 0.025, SV, z0=T)
kutu_merkez(y, (DX, DY - 0.075), 0.14, 0.03, 0.012, SV, z0=T)
hasir(y, DX, DY, T + 0.025, 0.16, 0.09, 0.0, 'boya_kirmizi', 'altin')
oturan(y, DX, DY + 0.02, T + 0.028, -math.pi / 2, 'boya_kirmizi', 'altin', boy=0.062)
semsiye(y, DX + 0.03, DY + 0.035, T + 0.025, boy=0.13, r=0.075)
for s in (-1, 1):
    kisi(y, DX + s * 0.13, DY + 0.02, T, -math.pi / 2, 'beyaz', 'boya_kirmizi', mizrak='ahsap', kalkan='kiremit')
    kisi(y, DX + s * 0.07, DY + 0.07, T + 0.025, -math.pi / 2, 'boya_sari', 'beyaz', kol=0.5)      # bow-bearers, fanners
# courtiers kneeling before the dais and guards lining the way
for i in range(5):
    oturan(y, -0.16 + 0.08 * i, -0.06, Z0, math.pi / 2, ('beyaz', 'kumas', 'boya_yesil', 'beyaz', 'kobalt')[i], 'beyaz')
for i in range(3):
    for s in (-1, 1):
        kisi(y, s * 0.075, -0.2 - 0.07 * i, Z0, s * math.pi / 2 * 0 + (0 if s < 0 else math.pi), 'boya_kirmizi', 'beyaz', mizrak='ahsap', kalkan='kiremit')
# drummers by the court gate
for s in (-1, 1):
    donel(y, (s * 0.2, PY0 - 0.06), [(0.0, Z0), (0.013, Z0), (0.018, Z0 + 0.035), (0.0, Z0 + 0.035)], 'ahsap', n=10)
    donel(y, (s * 0.2, PY0 - 0.06), [(0.0185, Z0 + 0.0348), (0.0, Z0 + 0.036)], 'kece', n=10)
    kisi(y, s * 0.2 + s * 0.03, PY0 - 0.06, Z0, math.pi if s > 0 else 0.0, 'boya_sari', 'boya_kirmizi', kol=0.8)

# ---------------- huts and granaries ----------------
y.bolum('Kulubeler')
for (hx, hy, r, a) in ((-0.68, -0.48, 0.07, 0.3), (-0.72, -0.22, 0.06, 0.1), (-0.66, 0.36, 0.065, 0.0), (-0.7, 0.62, 0.06, -0.3),
                       (0.68, -0.46, 0.07, 3.0), (0.7, 0.4, 0.065, 3.2), (0.68, 0.64, 0.06, 3.4), (-0.32, -0.5, 0.055, 1.6)):
    kulube(y, hx, hy, Z0, r, 0.075, 0.09, K, kapi_aci=a, n=14)
for (gx_, gy_) in ((-0.55, -0.6), (0.55, -0.6), (0.36, -0.5)):
    for a_ in range(4):
        kutu_merkez(y, (gx_ + 0.026 * math.cos(a_ * TAU / 4 + 0.7), gy_ + 0.026 * math.sin(a_ * TAU / 4 + 0.7)), 0.016, 0.016, 0.018, 'kaya', z0=Z0)
    kulube(y, gx_, gy_, Z0 + 0.018, 0.038, 0.06, 0.06, K, kapi_aci=-1.6, n=12, sacak=0.014)
# outside the walls: a hamlet of huts and granaries, cattle-pen fences, baobabs
for (hx, hy, r, a) in ((-1.0, -0.86, 0.065, -1.0), (-0.78, -0.95, 0.055, -1.4), (1.0, 0.62, 0.06, 0.5), (1.02, 0.92, 0.055, 0.0)):
    kulube(y, hx, hy, Z0, r, 0.07, 0.085, K, kapi_aci=a, n=14)
baobab(y, 0.62, -0.12, Z0, boy=0.32, tohum=5)
baobab(y, 0.98, -0.88, Z0, boy=0.34, tohum=1)
baobab(y, -1.0, 0.92, Z0, boy=0.3, tohum=8)
akasya(y, -1.02, 0.3, Z0, boy=0.22, tohum=9)

# ---------------- townsfolk ----------------
y.bolum('Insanlar')
for k, (px, py, a, g, b, yk) in enumerate(((0.04, -0.85, 1.6, 'beyaz', 'beyaz', None), (-0.05, -0.95, 1.5, 'boya_sari', 'boya_kirmizi', 'kabak'),
                                            (-0.55, -0.35, 0.4, 'kobalt', 'beyaz', None), (0.5, 0.1, 2.0, 'kumas', 'beyaz', 'saz'),
                                            (-0.6, 0.15, 1.0, 'boya_kirmizi', 'boya_sari', 'kiremit'), (0.55, -0.3, 2.5, 'boya_yesil', 'beyaz', None),
                                            (-0.9, -0.98, 0.2, 'beyaz', 'beyaz', None), (0.95, 0.75, 3.0, 'boya_sari', 'beyaz', 'saz'))):
    kisi(y, px, py, Z0, a, g, b, yuk={'kabak': 'boya_sari'}.get(yk, yk))
mali_at(y, 0.22, -0.92, Z0, math.pi / 2, 'beyaz', 'boya_kirmizi', 'boya_sari', binici=('beyaz', 'beyaz', 'ahsap', 'kiremit'))

calistir(y, 'lm_nianikale')
