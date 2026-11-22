# Gyeongbokgung (lm_gyeongbok): the Joseon main palace. Geunjeongjeon, the throne hall: double-roofed paljak hall on the
# two-tier granite woldae with balustrades, beast statues and the carved central stair; the stone-paved court with the
# raised royal way and the rank stones, closed by the heonggak cloisters and the Geunjeongmun gate; Gwanghwamun (a
# double-roofed gate pavilion on a three-arched granite base, haetae in front); Gyeonghoeru, the banquet pavilion on
# stone pillars in its pond, with bridges, islets and pines; the palace wall.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ek import *
from bina_ortak import calistir

y = Yapi()
AX = 0.22                                    # the palace axis
GX0, GX1, GY0, GY1 = -1.2, 1.06, -1.2, 1.16
PX0, PX1, PY0, PY1 = -1.1, -0.6, -0.42, 0.98  # the pond
HX0, HX1, HY0, HY1 = AX - 0.73, AX + 0.73, -0.62, 1.1   # the cloister's outer line
EN = 0.075

# ---------------------------------------------------------------- ground
y.bolum('Zemin')


def ust_fn(x, yy):
    if HX0 + EN < x < HX1 - EN and HY0 + EN < yy < HY1 - EN:
        return TAS2                       # the stone-paved court (bakseok)
    return 'zemin'


KX0, KX1, KY0, KY1 = -0.56, 0.96, -0.79, -0.72   # the Geumcheon stream across the front yard
Z0 = zemin_delikli(y, GX0, GX1, GY0, GY1, 0.04, [(PX0, PX1, PY0, PY1), (KX0, KX1, KY0, KY1)], 'tas_koyu', 'zemin', ust_fn)
for k in range(3):   # steps up to the platform in front of Gwanghwamun
    hh = Z0 * (3 - k) / 4
    kutu(y, V(AX - 0.2, GY0 - 0.025 * (k + 1), 0), X, 0.4, 0.025 * (k + 1) + 0.001, hh, 'tas_koyu', 'onsagsolust')

# ---------------------------------------------------------------- the palace wall
y.bolum('Saray suru')
kore_sur(y, [(AX + 0.3, -0.96), (1.02, -0.96), (1.02, 1.12), (-1.16, 1.12), (-1.16, -0.96), (AX - 0.3, -0.96)], Z0, 0.08)

# ---------------------------------------------------------------- Gwanghwamun
y.bolum('Gwanghwamun')
GH = 0.15
BX0, BX1, BY0, BY1 = AX - 0.3, AX + 0.3, -1.08, -0.88
seg = [(0.07, None), (0.12, 0.66), (0.04, None), (0.14, 0.7), (0.04, None), (0.12, 0.66), (0.07, None)]
KR = (TAS, 'granit_koyu', TAS2, 'koyu')
x = BX0
for w, en in seg:
    a, b = V(x, BY0), V(x + w, BY0)
    if en:
        y.kemerli(a + Z * Z0, b + Z * Z0, 0, GH * (1.0 if w > 0.13 else 0.92), KR, v0=0.0, en=en, ust=0.03, derin=BY1 - BY0 - 0.003, k_say=10,
                  cerceve=(0.007, [TAS2, TAS]))
        if w < 0.13:
            duz_duvar(y, a, b, Z0 + GH * 0.92, Z0 + GH, TAS)
    else:
        duz_duvar(y, a, b, Z0, Z0 + GH, TAS)
    x += w
x = BX1
for w, en in seg:   # the back face (towards the palace), the arches seen from inside
    a, b = V(x, BY1), V(x - w, BY1)
    if en:
        y.kemerli(a + Z * Z0, b + Z * Z0, 0, GH * (1.0 if w > 0.13 else 0.92), KR, v0=0.0, en=en, ust=0.03, derin=0.002, k_say=10)
        if w < 0.13:
            duz_duvar(y, a, b, Z0 + GH * 0.92, Z0 + GH, TAS)
    else:
        duz_duvar(y, a, b, Z0, Z0 + GH, TAS)
    x -= w
for xs, s in ((BX0, -1), (BX1, 1)):
    duz_duvar(y, V(xs, BY1 if s < 0 else BY0), V(xs, BY0 if s < 0 else BY1), Z0, Z0 + GH, TAS)
silme(y, dikdortgen(BX0, BX1, BY0, BY1), Z0, 0.014, 0.006, 'granit_koyu', 'kaide')
silme(y, dikdortgen(BX0, BX1, BY0, BY1), Z0 + GH - 0.012, 0.012, 0.007, TAS2, 'kaba')
y.yuz_yon(dikdortgen(BX0, BX1, BY0, BY1, Z0 + GH), 'zemin', Z)
# the parapet round the top (yeojang) with its little tiled coping
kore_sur(y, [(BX0 + 0.004, BY0 + 0.004), (BX1 - 0.004, BY0 + 0.004), (BX1 - 0.004, BY1 - 0.004), (BX0 + 0.004, BY1 - 0.004)], Z0 + GH, 0.026,
         t=0.014, key=TAS, ust=TAS, kapali=True)
ZG = Z0 + GH
gw = kore_salon(y, AX, (BY0 + BY1) / 2, 0.46, 0.14, ZG, 0.08, 0.12, sacak=0.06, tur='ujingak', kivrim=0.34, yukari=0.035, nx=3, ny=1,
                on='kapi', yan='duvar', arka='kapi', cift=True, alt_yuk=0.03, alt_sacak=0.055, ic=0.022, ust_h=0.05, japsang=4, chwidu=1.0,
                r=0.008, mahya_en=0.013)
for s in (-1, 1):
    haetae(y, AX + s * 0.23, -1.15, Z0, math.pi / 2, 1.25)
    sancak(y, AX + s * 0.27, BY0 + 0.025, ZG, boy=0.24, en=0.11, yuk=0.07, aci=-math.pi / 2 + s * 0.6)

# ---------------------------------------------------------------- the cloisters and Geunjeongmun
y.bolum('Heonggak ve Geunjeongmun')
CH, CHH = 0.075, 0.05
GMW = 0.34
# (the front and back runs reach the corners; the side runs cross them: their ceilings a hair lower)
heonggak(y, (HX0, HY0), (AX - GMW / 2, HY0), EN, Z0, CH, CHH, cati=False)
heonggak(y, (AX + GMW / 2, HY0), (HX1, HY0), EN, Z0, CH, CHH, cati=False)
heonggak(y, (HX1, HY1), (HX0, HY1), EN, Z0, CH, CHH, cati=False)
heonggak(y, (HX1, HY0 + 0.001), (HX1, HY1 - 0.001), EN, Z0, CH, CHH, taban_h=0.0115, alcak=True, cati=False)
heonggak(y, (HX0, HY1 - 0.001), (HX0, HY0 + 0.001), EN, Z0, CH, CHH, taban_h=0.0115, alcak=True, cati=False)
# one roof over the whole ring of galleries: mitred corners (outer hip, inner valley), hipped where it meets the gate
heonggak_cati(y, [(AX + GMW / 2, HY0), (HX1, HY0), (HX1, HY1), (HX0, HY1), (HX0, HY0), (AX - GMW / 2, HY0)], EN, Z0 + 0.012 + CH, CHH)
kore_salon(y, AX, HY0 + 0.035, GMW, 0.13, Z0, 0.1, 0.1, sacak=0.055, tur='paljak', kivrim=0.34, yukari=0.035, nx=3, ny=2,
           on=['tahta', 'tahta', 'tahta'], yan='duvar', arka=['tahta', 'tahta', 'tahta'], gidan=(0.016, TAS, 1), japsang=3, chwidu=0.9,
           r=0.008, mahya_en=0.012)

# ---------------------------------------------------------------- the stream and Yeongjegyo
y.bolum('Geumcheon ve Yeongjegyo')
gol(y, KX0, KX1, KY0, KY1, Z0, Z0 - 0.02)
tas_kopru(y, (AX, (KY0 + KY1) / 2), 0.13, 0.13, Z0, 0.016)
for sx in (-1, 1):
    for sy in (-1, 1):
        haetae(y, AX + sx * 0.1, (KY0 + KY1) / 2 + sy * 0.055, Z0, math.pi / 2 if sy < 0 else -math.pi / 2, 0.6, TAS2, TAS2)
for ya, yb in ((BY1, KY0 - 0.004), (KY1 + 0.004, HY0 - 0.02)):
    kutu(y, V(AX - 0.06, ya, Z0), X, 0.12, yb - ya, 0.003, TAS, 'onarkasagsolust')
    kutu(y, V(AX - 0.025, ya, Z0 + 0.003), X, 0.05, yb - ya, 0.003, TAS2, 'onarkasagsolust')
dalgalar(y, KX0 + 0.02, KX1 - 0.02, KY0 + 0.01, KY1 - 0.01, Z0 - 0.02, 10, 7, 0.03, [(AX - 0.08, AX + 0.08, KY0, KY1)])

# ---------------------------------------------------------------- the court: royal way and rank stones
y.bolum('Avlu')
WC = 0.42                     # the woldae's centre y
yw0 = WC - 0.4                # its first tier's front
for (w_, hh, k) in ((0.13, 0.003, TAS), (0.05, 0.007, TAS)):
    kutu(y, V(AX - w_ / 2, HY0 + 0.1, Z0), X, w_, yw0 - 0.13 - (HY0 + 0.1), hh, k, 'onarkasagsolust')
for s in (-1, 1):
    for k in range(9):
        yy = HY0 + 0.15 + k * 0.05
        x = AX + s * 0.11
        kutu_merkez(y, (x, yy), 0.022, 0.016, 0.004, TAS, z0=Z0)
        kutu_merkez(y, (x, yy), 0.012, 0.008, 0.026 - k * 0.0006, TAS2, z0=Z0 + 0.004)
        donel(y, (x, yy), [(0.0055, Z0 + 0.03 - k * 0.0006), (0.0045, Z0 + 0.034 - k * 0.0006), (0.0, Z0 + 0.036 - k * 0.0006)], TAS2, n=6)
# great vats for fire water on the court
for s in (-1, 1):
    kazan(y, AX + s * 0.5, HY0 + 0.2, Z0, 1.4, 'demir')

# ---------------------------------------------------------------- the woldae
y.bolum('Woldae')
TH = 0.06
KAT = [(0.56, 0.4), (0.48, 0.32)]
z = Z0
for i, (hx, hy) in enumerate(KAT):
    kk = dikdortgen(AX - hx, AX + hx, WC - hy, WC + hy)
    yf = WC - hy
    bos = [((AX, yf), 0.22), ((AX - 0.3, yf), 0.1), ((AX + 0.3, yf), 0.1), ((AX, WC + hy), 0.12)]
    zt = teras(y, kk, z, TH, TAS, TAS2, True, bos, 0.05, 0.026, 0.008)
    teras_merdiven(y, (AX, yf - TH * 1.15), math.pi / 2, 0.2, z, zt, 5, TAS, rampa=TAS2, rampa_en=0.07)
    for s in (-1, 1):
        teras_merdiven(y, (AX + s * 0.3, yf - TH * 1.15), math.pi / 2, 0.08, z, zt, 5, TAS)
    teras_merdiven(y, (AX, WC + hy + TH * 1.15), -math.pi / 2, 0.1, z, zt, 5, TAS)
    # beast statues on the corners and beside the stairs
    for sx in (-1, 1):
        for sy in (-1, 1):
            haetae(y, AX + sx * (hx - 0.03), WC + sy * (hy - 0.03), zt, math.atan2(-sy, -sx) + math.pi, 0.55, TAS2, TAS2)
        haetae(y, AX + sx * 0.135, yf + 0.03, zt, math.pi / 2, 0.55, TAS2, TAS2)
    z = zt
ZT = z
for s in (-1, 1):
    kazan(y, AX + s * 0.42, WC - 0.27, ZT, 1.2, 'bronz')

# ---------------------------------------------------------------- Geunjeongjeon
y.bolum('Geunjeongjeon')
tepe = kore_salon(y, AX, WC, 0.8, 0.5, ZT, 0.19, 0.2, sacak=0.1, tur='paljak', kivrim=0.36, yukari=0.05, nx=5, ny=3,
                  on='kapi', yan='kapi', arka=['duvar', 'kapi', 'kapi', 'kapi', 'duvar'], cift=True, alt_yuk=0.055, alt_sacak=0.09, ic=0.06,
                  ust_h=0.09, gidan=(0.02, TAS, 1), japsang=7, chwidu=1.6, r=0.011, mahya_en=0.018, gongpo_h=0.026)

# ---------------------------------------------------------------- Gyeonghoeru and its pond
y.bolum('Gyeonghoeru ve gölü')
ZS = Z0 - 0.022
gol(y, PX0, PX1, PY0, PY1, Z0, ZS)
GC = (-0.85, 0.32)
GW, GD = 0.3, 0.42
IX0, IX1, IY0, IY1 = GC[0] - GW / 2 - 0.035, GC[0] + GW / 2 + 0.035, GC[1] - GD / 2 - 0.035, GC[1] + GD / 2 + 0.035
ik = dikdortgen(IX0, IX1, IY0, IY1)
duvarlar(y, ik, ZS - 0.008, Z0 + 0.008, TAS, ust='zemin')
silme(y, ik, Z0 + 0.002, 0.006, 0.005, TAS2, 'duz')
# the 48 stone pillars: square outside, round inside
ZP = Z0 + 0.008
PH = 0.1
for i in range(6):
    for j in range(8):
        px, py = GC[0] - GW / 2 + GW * i / 5, GC[1] - GD / 2 + GD * j / 7
        if i in (0, 5) or j in (0, 7):
            kutu_merkez(y, (px, py), 0.018, 0.018, PH, TAS2, z0=ZP)
        else:
            y.prizma((px, py), 0.0085, ZP, ZP + PH, TAS2, n=8, ust=False)
ZF = ZP + PH
# the floor beams and the wooden floor with its railing
kutu(y, V(GC[0] - GW / 2 - 0.022, GC[1] - GD / 2 - 0.022, ZF), X, GW + 0.044, GD + 0.044, 0.014, 'lake_koyu')
kutu(y, V(GC[0] - GW / 2 - 0.02, GC[1] - GD / 2 - 0.02, ZF + 0.014), X, GW + 0.04, GD + 0.04, 0.004, 'ahsap_acik', 'ust')
y.yuz_yon(dikdortgen(GC[0] - GW / 2 - 0.022, GC[0] + GW / 2 + 0.022, GC[1] - GD / 2 - 0.022, GC[1] + GD / 2 + 0.022, ZF), 'lake_koyu', -Z)
kore_korkuluk(y, dikdortgen(GC[0] - GW / 2 - 0.014, GC[0] + GW / 2 + 0.014, GC[1] - GD / 2 - 0.014, GC[1] + GD / 2 + 0.014), ZF + 0.018, 0.022,
              adim=0.06)
kore_salon(y, GC[0], GC[1], GW, GD, ZF + 0.018, 0.075, 0.12, sacak=0.065, tur='paljak', kivrim=0.36, yukari=0.045, nx=5, ny=7,
           on='acik', yan='acik', arka='acik', japsang=5, chwidu=1.1, r=0.0075, levha=False, mahya_en=0.014, acik_taban='ahsap_acik')
# three stone bridges to the east bank
for by in (GC[1] - 0.14, GC[1], GC[1] + 0.14):
    x0, x1 = IX1 - 0.004, PX1 + 0.02
    kutu(y, V(x0, by - 0.026, Z0 - 0.004), X, x1 - x0, 0.052, 0.012, TAS2, 'onarkasagsolust')
    for s in (-1, 1):
        cubuk(y, V(x0 + 0.004, by + s * 0.022, Z0 + 0.016), V(x1 - 0.004, by + s * 0.022, Z0 + 0.016), 0.004, TAS2, 0.006)
        for xx in (x0 + 0.004, (x0 + x1) / 2, x1 - 0.004):
            dikme(y, V(xx, by + s * 0.022), V(1, 0), Z0 + 0.008, 0.016, TAS2, 0.006)
    for xx in ((IX1 + PX1) / 2,):
        kutu_merkez(y, (xx, by), 0.012, 0.04, Z0 - 0.004 - (ZS - 0.005), TAS, z0=ZS - 0.005, yuzler='onarkasagsol')
# islets with pines in the south of the pond, lotus pads
for (ix, iy, r_) in ((-0.97, -0.24, 0.06), (-0.74, -0.27, 0.05)):
    duvarlar(y, cokgen((ix, iy), r_, 10), ZS - 0.008, Z0 - 0.004, TAS, ust='toprak_ot')
    sonamu(y, ix, iy, Z0 - 0.004, 0.17, tohum=int(ix * 100))
for k, (lx, ly) in enumerate(((-1.03, 0.0), (-0.98, 0.72), (-0.66, 0.85), (-0.68, -0.05), (-1.05, 0.88), (-0.86, -0.36))):
    y.yuz_yon([V(p.x, p.y, ZS + 0.0012) for p in cokgen((lx, ly), 0.014, 7, k)], 'boya_yesil', Z)
dalgalar(y, PX0 + 0.02, PX1 - 0.02, PY0 + 0.02, PY1 - 0.02, ZS, 26, 5, 0.03, [(IX0, IX1, IY0, IY1), (-1.04, -0.68, -0.33, -0.18)])

# ---------------------------------------------------------------- trees
y.bolum('Ağaçlar')
for k, (tx, ty) in enumerate(((-0.55, -0.82), (-0.85, -0.8), (-1.08, -0.78), (0.8, -0.8), (0.95, -0.72), (-1.1, 1.05), (-0.62, 1.06),
                              (-1.05, -0.55))):
    sonamu(y, tx, ty, Z0, 0.15 + 0.03 * (k % 3), tohum=k)

sayim(y)
calistir(y, 'lm_gyeongbok')
