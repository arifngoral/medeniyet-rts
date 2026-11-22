# Küp Avlusu (lm_ambaravlu): a Korean farmhouse court with its jangdokdae: rows of dark glazed onggi jars (soy, doenjang,
# gochujang) graded by size on a two-tier stone terrace; the hanok main house (granite base, posts, white plaster, paper
# lattice doors, an open wooden hall, a deep paljak roof), a gable-roofed storehouse wing, a stone-and-earth wall with a
# tiled coping and a roofed gate, a persimmon tree heavy with fruit, a well, chillies drying on straw mats, firewood.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ortak import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(11)
Z0 = 0.03

# ---------------- ground ----------------
y.bolum('Zemin ve avlu')
zemin(y, -1.1, 1.1, -1.06, 1.06, Z0, 'granit_koyu', 'cimen', basamak=(), silmeli=False)
# the swept yard inside the wall
y.yuz_yon([V(-1.0, -0.95, Z0 + 0.002), V(1.0, -0.95, Z0 + 0.002), V(1.0, 0.95, Z0 + 0.002), V(-1.0, 0.95, Z0 + 0.002)], 'toprak', Z)
# the path from the gate
y.yuz_yon([V(-0.42, -1.06, Z0 + 0.003), V(-0.28, -1.06, Z0 + 0.003), V(-0.28, -0.97, Z0 + 0.003), V(-0.42, -0.97, Z0 + 0.003)], 'toprak', Z)
for k in range(7):   # stepping stones to the house
    t = k / 6
    p = V(-0.35, -0.9).lerp(V(-0.2, 0.26), t)
    kutu_merkez(y, (p.x + 0.01 * math.sin(k * 2.1), p.y), 0.05, 0.04, 0.006, 'granit_acik', z0=Z0 + 0.002, aci=0.3 * math.sin(k))

# ---------------- main house (anchae) ----------------
y.bolum('Ana ev: kaide ve maru')
HX0, HX1, HY0, HY1 = -0.85, 0.42, 0.45, 0.8
ZB = gidan(y, HX0 - 0.04, HX1 + 0.04, HY0 - 0.12, HY1 + 0.04, Z0 + 0.002, 0.08, basamak=((0, 0.32, 0.16), (0, 0.78, 0.12)))
maru(y, HX0 + 0.0, HX1 - 0.0, HY0 - 0.085, HY0, ZB + 0.012)
y.bolum('Ana ev: gövde')


def desen_ana(i, j, nb):
    if i == 0:
        return 'acik' if j in (4, 5, 6) else 'kapi'
    if i == 2:
        return 'pencere' if j % 3 == 1 else 'duvar'
    return 'pencere' if j == nb // 2 else 'duvar'


zt = hanok_govde(y, HX0, HX1, HY0, HY1, ZB, 0.27, bay=0.1, desen=desen_ana, alt_bant=None)
# the open hall's wooden floor and its back wall with a lattice window
y.bolum('Ana ev: çatı')
tepe_ev = kore_cati(y, HX0, HX1, HY0, HY1, zt, 0.37, sacak=0.11, tur='paljak', kivrim=0.42, yukari=0.04, alt_key='ahsap',
                    ucluk='siva', ns=22, sirt_h=0.032)

# ---------------- storehouse wing ----------------
y.bolum('Ambar kanadı')
WX0, WX1, WY0, WY1 = 0.64, 0.9, -0.2, 0.78
ZW = gidan(y, WX0 - 0.03, WX1 + 0.03, WY0 - 0.03, WY1 + 0.03, Z0 + 0.002, 0.04, basamak=((3, 0.3, 0.1),))


def desen_kanat(i, j, nb):
    if i == 3:
        return 'tahta' if j in (2, 5) else 'pencere' if j == 7 else 'duvar'
    if i == 0:
        return 'tahta'
    return 'duvar'


zt2 = hanok_govde(y, WX0, WX1, WY0, WY1, ZW, 0.2, bay=0.11, desen=desen_kanat, alt_bant='granit')
kore_cati(y, WX0, WX1, WY0, WY1, zt2, 0.15, sacak=0.075, tur='matbae', kivrim=0.35, alt_key='ahsap', ucluk='siva', ns=14)
# firewood stacked against the wing's end
for r_ in range(4):
    for k in range(7 - r_):
        x = WX0 + 0.02 + (k + r_ * 0.5) * 0.032
        boru(y, [V(x, WY0 - 0.06, Z0 + 0.014 + r_ * 0.026), V(x, WY0 - 0.17, Z0 + 0.014 + r_ * 0.026)], 0.013, 'kutuk', n=6)

# ---------------- jangdokdae ----------------
y.bolum('Jangdokdae: taş seki')
JX0, JX1, JY0, JYM, JY1 = -0.08, 0.56, -0.66, -0.4, -0.12
toprak_ = 'granit'
duvarlar(y, dikdortgen(JX0, JX1, JY0, JY1), Z0, Z0 + 0.04, 'granit', ust='granit_acik')
silme(y, dikdortgen(JX0, JX1, JY0, JY1), Z0 + 0.034, 0.006, 0.005, 'granit_acik', 'duz')
duvarlar(y, dikdortgen(JX0 + 0.02, JX1 - 0.02, JYM, JY1 - 0.02), Z0 + 0.04, Z0 + 0.08, 'granit', ust='granit_acik')
silme(y, dikdortgen(JX0 + 0.02, JX1 - 0.02, JYM, JY1 - 0.02), Z0 + 0.074, 0.006, 0.005, 'granit_acik', 'duz')
merdiven(y, V((JX0 + JX1) / 2, JY0 - 0.04), math.pi / 2, 0.1, Z0, Z0 + 0.04, n=2, d=0.02, key='granit')
y.bolum('Jangdokdae: onggi küpleri')
# back rows: the big jars, then smaller ones stepping down to the front
for row, (yy, H, zz, n_) in enumerate(((JY1 - 0.07, 0.125, Z0 + 0.08, 6), (JYM + 0.075, 0.1, Z0 + 0.08, 7),
                                       (JYM - 0.06, 0.08, Z0 + 0.04, 8), (JY0 + 0.05, 0.06, Z0 + 0.04, 10))):
    xs0, xs1 = JX0 + 0.06, JX1 - 0.06
    for k in range(n_):
        x = xs0 + (xs1 - xs0) * (k + 0.5) / n_ + rn.uniform(-0.006, 0.006)
        h_ = H * rn.uniform(0.9, 1.06)
        kap = None if (row, k) in ((1, 3), (2, 5), (3, 2)) else ('onggi2' if rn.random() < 0.7 else 'onggi')
        onggi(y, x, yy + rn.uniform(-0.008, 0.008), zz, h_, key='onggi' if rn.random() < 0.8 else 'onggi2', kapak=kap)
# a few jars on the ground by the terrace and a bowl
for (x, yy, H) in ((JX1 + 0.05, JY0 + 0.02, 0.07), (JX1 + 0.06, JY0 + 0.12, 0.055), (JX0 - 0.05, JY0 + 0.05, 0.05)):
    onggi(y, x, yy, Z0 + 0.002, H)
donel(y, (JX1 + 0.04, JY0 - 0.06), [(0.012, Z0 + 0.002), (0.028, Z0 + 0.016), (0.024, Z0 + 0.016), (0.0, Z0 + 0.008)], 'onggi2', n=10)

# ---------------- wall and gate ----------------
y.bolum('Taş-toprak duvar ve kapı')
GX0, GX1 = -0.43, -0.27
toprak_duvar(y, [V(GX1, -0.97), V(1.02, -0.97), V(1.02, 0.97), V(-1.02, 0.97), V(-1.02, -0.97), V(GX0, -0.97)], Z0, 0.14)
# the gate: two posts, plank doors standing open, a little gable roof
for x in (GX0, GX1):
    kutu_merkez(y, (x, -0.97), 0.022, 0.03, 0.2, 'ahsap', z0=Z0)
    kutu_merkez(y, (x, -0.97), 0.036, 0.04, 0.012, 'granit', z0=Z0)
kutu(y, V(GX0 - 0.02, -0.985, Z0 + 0.19), X, GX1 - GX0 + 0.04, 0.03, 0.018, 'ahsap')
kutu(y, V(GX0 - 0.01, -0.982, Z0 + 0.15), X, GX1 - GX0 + 0.02, 0.024, 0.012, 'ahsap')
for sx, x in ((1, GX0 + 0.011), (-1, GX1 - 0.011)):   # the leaves swung in
    a = -math.pi / 2 + sx * 0.5
    d = V(math.cos(a + math.pi), math.sin(a + math.pi))
    q = V(x, -0.97)
    kutu_merkez(y, (q.x + sx * 0.035 * 0.88, q.y + 0.035 * 0.48), 0.07, 0.008, 0.145, 'ahsap_dikey', z0=Z0 + 0.004, aci=sx * 0.5)
kore_cati(y, GX0 - 0.03, GX1 + 0.03, -1.0, -0.94, Z0 + 0.208, 0.07, sacak=0.035, tur='matbae', kivrim=0.35, alt_key='ahsap', ucluk='ahsap',
          ns=6, sirt_h=0.014)

# ---------------- court ----------------
y.bolum('Hurma ağacı')
kaki(y, -0.74, -0.3, Z0, boy=0.78, tohum=3)
# a wooden platform (pyeongsang) in its shade
kutu(y, V(-0.6, -0.56, Z0 + 0.045), X, 0.2, 0.14, 0.01, 'ahsap_acik')
for (x, yy) in ((-0.59, -0.55), (-0.41, -0.55), (-0.59, -0.43), (-0.41, -0.43)):
    kutu_merkez(y, (x, yy), 0.012, 0.012, 0.045, 'ahsap', z0=Z0)
donel(y, (-0.52, -0.49), [(0.0, Z0 + 0.055), (0.03, Z0 + 0.055), (0.03, Z0 + 0.058), (0.0, Z0 + 0.058)], 'ahsap', n=10)   # a low table
for k in range(4):
    onggi(y, -0.52 + 0.012 * math.cos(k * 1.6), -0.49 + 0.012 * math.sin(k * 1.6), Z0 + 0.058, 0.014, kapak=None, n=8)

y.bolum('Lahana tarhı')
# the kimchi cabbages in a raised bed by the wall
CB = (-0.96, -0.5, -0.9, -0.62)
kutu(y, V(CB[0], CB[2], Z0), X, CB[1] - CB[0], CB[3] - CB[2], 0.014, 'toprak')
for r_ in range(3):
    yy = CB[2] + 0.045 + r_ * 0.095
    y.yuz_yon([V(CB[0] + 0.02, yy - 0.025, Z0 + 0.0145), V(CB[1] - 0.02, yy - 0.025, Z0 + 0.0145), V(CB[1] - 0.02, yy + 0.025, Z0 + 0.0145),
               V(CB[0] + 0.02, yy + 0.025, Z0 + 0.0145)], 'kerpic_koyu', Z)
    for k in range(9):
        x = CB[0] + 0.04 + k * 0.048
        donel(y, (x, yy), [(0.012, Z0 + 0.014), (0.02, Z0 + 0.026), (0.017, Z0 + 0.042), (0.008, Z0 + 0.05), (0.0, Z0 + 0.051)],
              'cimen' if (k + r_) % 3 else 'zeytin', n=8, kat=rn.uniform(0, 1))
        for m in range(3):   # outer leaves splaying
            a = TAU * m / 3 + k
            d = V(math.cos(a), math.sin(a))
            cubuk(y, V(x, yy, Z0 + 0.016) + d * 0.01, V(x, yy, Z0 + 0.03) + d * 0.024, 0.014, 'boya_yesil', 0.003)

y.bolum('Kuyu')
WC = (-0.6, 0.08)
donel(y, WC, [(0.05, Z0), (0.05, Z0 + 0.05), (0.044, Z0 + 0.054), (0.038, Z0 + 0.05), (0.038, Z0 + 0.03)], 'granit', n=14)
y.yuz_yon([V(WC[0] + 0.038 * math.cos(TAU * i / 14), WC[1] + 0.038 * math.sin(TAU * i / 14), Z0 + 0.03) for i in range(14)], 'su', Z)
for sx in (-1, 1):
    kutu_merkez(y, (WC[0] + sx * 0.055, WC[1]), 0.012, 0.012, 0.14, 'ahsap', z0=Z0)
cubuk(y, V(WC[0] - 0.065, WC[1], Z0 + 0.135), V(WC[0] + 0.065, WC[1], Z0 + 0.135), 0.012, 'ahsap')
cubuk(y, V(WC[0], WC[1], Z0 + 0.13), V(WC[0], WC[1], Z0 + 0.09), 0.0015, 'saz')
donel(y, WC, [(0.01, Z0 + 0.075), (0.014, Z0 + 0.09), (0.0, Z0 + 0.09)], 'ahsap', n=8)
onggi(y, WC[0] + 0.08, WC[1] - 0.04, Z0 + 0.002, 0.055, kapak=None)

y.bolum('Kuruyan biberler')
for (mx, my, aci) in ((-0.32, -0.25, 0.1), (-0.1, -0.78, -0.08)):
    with parca(y, (mx, my, Z0 + 0.002), aci):
        kutu(y, V(-0.11, -0.07, 0), X, 0.22, 0.14, 0.004, 'saz')
        for k in range(3):
            cubuk(y, V(-0.11, -0.07 + 0.035 * (k + 1), 0.0045), V(0.11, -0.07 + 0.035 * (k + 1), 0.0045), 0.002, 'saz_koyu', 0.0005)
        for k in range(46):
            px, py = rn.uniform(-0.1, 0.1), rn.uniform(-0.06, 0.06)
            a = rn.uniform(0, TAU)
            d = V(math.cos(a), math.sin(a)) * 0.007
            cubuk(y, V(px, py, 0.0065) - d, V(px, py, 0.0065) + d, 0.0045, 'boya_kirmizi' if k % 5 else 'turuncu', 0.0035)

y.bolum('Baca, saman, insanlar')
# the low chimney behind the house
kutu_merkez(y, (0.25, 0.9), 0.05, 0.05, 0.16, 'granit', z0=Z0)
kutu_merkez(y, (0.25, 0.9), 0.062, 0.062, 0.01, 'kiremit_koyu2', z0=Z0 + 0.16)
for sx in (-1, 1):
    kutu_merkez(y, (0.25 + sx * 0.013, 0.9), 0.014, 0.03, 0.02, 'granit_koyu', z0=Z0 + 0.17)
kutu_merkez(y, (0.25, 0.9), 0.05, 0.03, 0.008, 'kiremit_koyu2', z0=Z0 + 0.19)
# straw stacks by the wall
for (x, yy) in ((-0.9, 0.55), (-0.88, 0.32)):
    donel(y, (x, yy), [(0.055, Z0), (0.06, Z0 + 0.06), (0.04, Z0 + 0.1), (0.0, Z0 + 0.13)], 'saz', n=10)
    donel(y, (x, yy), [(0.03, Z0 + 0.105), (0.034, Z0 + 0.12), (0.0, Z0 + 0.145)], 'saz_koyu', n=10)
kisi(y, 0.3, -0.72, Z0 + 0.04, aci=math.pi / 2, boy=0.1, govde='beyaz', kusak='boya_kirmizi', sapka='yok', kol='on')
kisi(y, -0.15, 0.2, Z0 + 0.002, aci=-math.pi / 2 - 0.3, boy=0.1, govde='siva_krem', kusak='lake_koyu', sapka='gat', kol='on')
kisi(y, -0.24, -0.2, Z0 + 0.002, aci=0.4, boy=0.1, govde='beyaz', kusak='boya_yesil', sapka='yok')

y.bolum('Sancak')
sancak(y, -0.18, -1.02, Z0, boy=0.4, en=0.12, yuk=0.08, aci=math.pi + 0.3)

calistir(y, 'lm_ambaravlu')
