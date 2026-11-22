# Donanma Komutanlığı (lm_komutanlik): Tongjeyeong, the Joseon naval command. Sebyeonggwan, the great open hall of
# 9 x 5 bays under one paljak roof on a high granite base, raised on a walled terrace with stairs and the Jigwamun gate;
# the two-storey Mangilru gate over the parade court with drilling marines; Yi Sun-sin's shrine in its walls with the red
# hongsalmun and a tortoise stele; the granite quay with a timber pier, a panokseon and a geobukseon in the harbour.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ek import *
from bina_ortak import calistir
import random

y = Yapi()
rs = random.Random(3)
GX0, GX1, GY0, GY1 = -1.15, 1.15, -1.15, 1.13
KY = -0.5
Z0, ZW = 0.05, 0.018
AX = 0.14
HX0, HX1, HY0, HY1 = -0.62, 0.9, 0.18, 1.1     # the terrace
Z1 = Z0 + 0.12

# ---------------------------------------------------------------- land, harbour, quay
y.bolum('Kara, liman ve rıhtım')
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, KY - GY0, ZW - 0.0005, 'kaya_koyu', 'onsagsol')
y.yuz_yon([V(GX0, GY0, ZW), V(GX1, GY0, ZW), V(GX1, KY, ZW), V(GX0, KY, ZW)], 'su', Z)
kutu(y, V(GX0, KY, 0), X, GX1 - GX0, GY1 - KY, Z0, 'tas_koyu', 'arkasagsol')
silme(y, [V(GX1, KY), V(GX1, GY1), V(GX0, GY1), V(GX0, KY)], Z0 - 0.008, 0.008, 0.006, 'tas_koyu', 'duz', kapali=False)
duz_duvar(y, V(GX0, KY), V(GX1, KY), ZW - 0.006, Z0, 'granit')
silme(y, [V(GX0, KY), V(GX1, KY)], Z0 - 0.007, 0.009, 0.007, TAS2, 'duz', kapali=False)
xs = sorted({GX0, -0.62, 0.98, GX1, -0.01, 0.29})
ys = sorted({KY, -0.22, 0.18, GY1})


def ust(x, yy):
    if yy < -0.22:
        return 'zemin'
    if -0.62 < x < 0.98 and yy < 0.18:
        return TAS2                      # the parade court
    return 'toprak_ot'


xs = [GX0, -0.62, 0.98, GX1]
for i in range(len(xs) - 1):
    for j in range(len(ys) - 1):
        mx, my = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
        y.yuz_yon([V(xs[i], ys[j], Z0), V(xs[i + 1], ys[j], Z0), V(xs[i + 1], ys[j + 1], Z0), V(xs[i], ys[j + 1], Z0)], ust(mx, my), Z)
for k in range(12):
    x = -1.05 + k * 0.19
    if 0.78 < x < 0.92:
        continue
    y.prizma((x, KY + 0.02), 0.007, Z0, Z0 + 0.02, 'granit_koyu', n=8)
    kure(y, (x, KY + 0.02, Z0 + 0.022), 0.008, 'granit_koyu', n=8, kat=3)
dalgalar(y, GX0 + 0.03, GX1 - 0.03, GY0 + 0.03, KY - 0.03, ZW, 34, 4, 0.035, [(0.02, 0.8, -1.06, -0.6), (-0.93, -0.18, -1.05, -0.58), (0.8, 0.9, -1.0, KY)])

# ---------------------------------------------------------------- the terrace
y.bolum('Teras')
tk = dikdortgen(HX0, HX1, HY0, HY1)
duvarlar(y, tk, Z0, Z1, 'granit', ust='zemin')
silme(y, tk, Z0, 0.014, 0.006, 'granit_koyu', 'kaide')
silme(y, tk, Z1 - 0.01, 0.01, 0.007, TAS2, 'kaba')
merdiven(y, (AX, HY0 - 0.15), math.pi / 2, 0.2, Z0, Z1, 12, key='granit')
for sx in (-1, 1):
    cubuk(y, V(AX + sx * 0.106, HY0 - 0.15, Z0 + 0.01), V(AX + sx * 0.106, HY0, Z1 + 0.012), 0.012, TAS2, 0.024)
kore_sur(y, [(HX1 - 0.01, HY0 + 0.01), (HX1 - 0.01, HY1 - 0.01), (HX0 + 0.01, HY1 - 0.01), (HX0 + 0.01, HY0 + 0.01)], Z1, 0.05, t=0.024, key='tas',
         ust=DUVAR)
# the Jigwamun gate at the head of the stairs, the wall either side of it on the terrace edge
kore_salon(y, AX, HY0 + 0.06, 0.28, 0.09, Z1, 0.085, 0.08, sacak=0.045, tur='paljak', kivrim=0.34, yukari=0.035, nx=3, ny=1,
           on=['tahta', 'tahta', 'tahta'], yan='duvar', arka=['tahta', 'tahta', 'tahta'], gidan=(0.01, TAS, 0), japsang=2, chwidu=0.8, r=0.008,
           mahya_en=0.011)
kore_sur(y, [(AX + 0.16, HY0 + 0.03), (HX1 - 0.03, HY0 + 0.03)], Z1, 0.05, t=0.024, key='tas', ust=DUVAR)
kore_sur(y, [(HX0 + 0.03, HY0 + 0.03), (AX - 0.16, HY0 + 0.03)], Z1, 0.05, t=0.024, key='tas', ust=DUVAR)
for sx in (-1, 1):
    sancak(y, AX + sx * 0.2, HY0 - 0.05, Z0, boy=0.3, en=0.13, yuk=0.08, aci=-math.pi / 2 + sx * 0.7)

# ---------------------------------------------------------------- Sebyeonggwan
y.bolum('Sebyeonggwan')
kore_salon(y, AX, 0.66, 1.1, 0.46, Z1, 0.19, 0.22, sacak=0.11, tur='paljak', kivrim=0.36, yukari=0.055, nx=9, ny=5, on='acik', yan='acik',
           arka='acik', gidan=(0.06, 'granit', 3), japsang=6, chwidu=1.6, r=0.011, levha=False, mahya_en=0.018, gongpo_h=0.026)
hyeonpan(y, (AX, 0.66 - 0.23), Z1 + 0.06 + 0.008 + 0.19 * 0.9, 0.12)
# officers in the hall
for k, (x, yy) in enumerate(((AX - 0.1, 0.62), (AX + 0.05, 0.6), (AX + 0.2, 0.66), (AX - 0.25, 0.7))):
    insan(y, x, yy, Z1 + 0.068, -math.pi / 2 + 0.3 * k, 'boya_kirmizi' if k else 'kobalt', 'koyu', 0.055)

# ---------------------------------------------------------------- the parade court and Mangilru
y.bolum('Mangilru ve tören avlusu')
kore_sur(y, [(0.29, -0.22), (0.98, -0.22), (0.98, 0.16)], Z0, 0.07, t=0.03, key='tas', ust=DUVAR)
kore_sur(y, [(-0.62, 0.16), (-0.62, -0.22), (-0.01, -0.22)], Z0, 0.07, t=0.03, key='tas', ust=DUVAR)
kore_salon(y, AX, -0.22, 0.3, 0.13, Z0, 0.1, 0.12, sacak=0.06, tur='paljak', kivrim=0.35, yukari=0.04, nx=3, ny=1,
           on=['tahta', 'tahta', 'tahta'], yan='duvar', arka=['tahta', 'tahta', 'tahta'], cift=True, alt_yuk=0.03, alt_sacak=0.05, ic=0.018,
           ust_h=0.06, gidan=(0.014, TAS, 1), japsang=3, chwidu=1.0, r=0.008, mahya_en=0.012)
# marines drilling in ranks, an officer and a drum (the ranks kept clear of the court wall, which hid the front row
# up to the hats, and the officer and the drum off the terrace stair)
for i in range(5):
    for j in range(3):
        insan(y, -0.4 + i * 0.07, -0.02 + j * 0.065, Z0, math.pi / 2, 'boya_kirmizi' if j != 1 else 'kobalt', 'koyu', 0.05)
for i in range(5):
    for j in range(3):
        insan(y, 0.42 + i * 0.07, -0.02 + j * 0.065, Z0, math.pi / 2, 'boya_kirmizi' if j != 1 else 'kobalt', 'koyu', 0.05)
insan(y, AX, -0.04, Z0, math.pi / 2, 'kobalt', 'koyu', 0.06)
donel(y, (AX + 0.14, -0.04), [(0.0, Z0), (0.02, Z0 + 0.002), (0.024, Z0 + 0.018), (0.02, Z0 + 0.034), (0.0, Z0 + 0.036)], 'boya_kirmizi', n=10)

# ---------------------------------------------------------------- Yi Sun-sin's shrine
y.bolum('Türbe')
SX = -0.91
kore_sur(y, [(SX + 0.05, 0.04), (-0.71, 0.04), (-0.71, 0.76), (-1.11, 0.76), (-1.11, 0.04), (SX - 0.05, 0.04)], Z0, 0.07, t=0.026, key='tas', ust=DUVAR)
kore_salon(y, SX, 0.04, 0.1, 0.05, Z0, 0.07, 0.05, sacak=0.03, tur='matbae', nx=1, ny=1, on=['tahta'], yan='duvar', arka=['tahta'], chwidu=0.0,
           levha=False, r=0.007, mahya_en=0.008)
hongsalmun(y, SX, -0.12, Z0, 0.17, 0.17)
bigak(y, SX, 0.24, Z0, 0.1, 0.07)
kore_salon(y, SX, 0.56, 0.28, 0.16, Z0, 0.1, 0.1, sacak=0.05, tur='paljak', kivrim=0.35, yukari=0.04, nx=3, ny=2, on='kapi', yan='duvar',
           arka='duvar', gidan=(0.03, TAS, 1), japsang=2, chwidu=0.8, r=0.008, mahya_en=0.011)
for k in range(2):
    sonamu(y, SX + (-0.13 if k else 0.13), 0.36, Z0, 0.13, tohum=40 + k)

# ---------------------------------------------------------------- the harbour: pier and ships
y.bolum('Liman ve gemiler')
PX = 0.85
kutu(y, V(PX - 0.045, -1.02, Z0 - 0.012), X, 0.09, KY - (-1.02), 0.008, 'ahsap', 'onsagsolust')
for k in range(5):
    yy = -1.0 + k * 0.12
    for sx in (-1, 1):
        y.prizma((PX + sx * 0.04, yy), 0.006, 0.0, Z0 + 0.004, 'ahsap_koyu', n=6)
for k in range(9):
    yy = -1.01 + k * 0.06
    y.yuz_yon([V(PX - 0.045, yy, Z0 - 0.0035), V(PX + 0.045, yy, Z0 - 0.0035), V(PX + 0.045, yy + 0.004, Z0 - 0.0035), V(PX - 0.045, yy + 0.004, Z0 - 0.0035)],
              'ahsap_koyu', Z)
panokseon(y, (0.43, -0.83), math.pi, 1.0, ZW - 0.07 * 0.3, yelken=False, kurek=False, tohum=1)
geobukseon(y, (-0.55, -0.8), math.pi * 0.95, 1.0, ZW - 0.075 * 0.32, su=0.075 * 0.32, tohum=4)
for (x, yy, a) in ((-0.05, -1.05, 0.3), (1.02, -0.75, 1.5)):
    with parca(y, (x, yy, ZW), a):
        P, Du, hb = kore_gemi_govde(0.12, 0.022, 0.018, bas_egim=0.008, kic_egim=0.006)
        us = [-1 + 2 * i / 6 for i in range(7)]
        for sd in (-1, 1):
            for i in range(6):
                q = [P(us[i], sd, 0.0), P(us[i + 1], sd, 0.0), P(us[i + 1], sd, 1.0), P(us[i], sd, 1.0)]
                q = [p - Z * 0.006 for p in q]
                m = sum(q, Vector()) / 4
                yuz_dis(y, q, 'ahsap', V(m.x, 0, m.z))
        for u, sg in ((1.0, 1), (-1.0, -1)):
            y.yuz_yon([P(u, -1, 0.0) - Z * 0.006, P(u, 1, 0.0) - Z * 0.006, P(u, 1, 1.0) - Z * 0.006, P(u, -1, 1.0) - Z * 0.006], 'ahsap', V(sg, 0, 0.3 * sg))
        y.yuz_yon([P(u, -1, 1.0) - Z * 0.006 for u in us] + [P(u, 1, 1.0) - Z * 0.006 for u in reversed(us)], 'ahsap_acik', Z)
        insan(y, 0.0, 0.0, 0.004, 0.0, 'kece', 'saz', 0.045)
insan(y, PX, -0.7, Z0 - 0.004, 1.0, 'boya_kirmizi', 'koyu', 0.05)
insan(y, PX - 0.01, -0.9, Z0 - 0.004, 2.4, 'kece', 'saz', 0.05)

# ---------------------------------------------------------------- trees
y.bolum('Ağaçlar')
for k, (tx, ty) in enumerate(((-1.06, 0.95), (-0.8, 1.05), (-0.62, 1.02) if False else (-0.7, 0.92), (1.06, 0.3), (1.05, 0.75), (1.06, 1.05),
                              (-0.5, 1.0), (0.75, 1.0), (-0.56, 0.28), (0.84, 0.28), (-1.07, -0.35), (1.07, -0.35))):
    zt = Z1 if (HX0 < tx < HX1 and HY0 < ty < HY1) else Z0
    sonamu(y, tx, ty, zt, 0.15 + 0.03 * (k % 3), tohum=k + 60)

sayim(y)
calistir(y, 'lm_komutanlik')
