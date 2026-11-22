# Racput Kışlası (lm_racputkisla): a Rajput fort-barracks: thick yellow sandstone walls with round bastions and rounded
# merlons, a tall gate (pol) between two bastions with iron-spiked leaves against elephants and a bangla-roofed jharokha
# over it; inside a parade ground with drilling soldiers, the cavalry stables (an arcade of stalls with horses and hay),
# the soldiers' two-storey barracks, the war elephants' stalls, and at the back the commander's red sandstone palace:
# storeys of engrailed arches, jharokhas with curved roofs, a jali storey, a tower and chhatris.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from hint_ortak import *
from hint_ek import *
from frank_ortak import at
import doku

y = Yapi()
KM, KMA, KMK = 'kum', 'kum_acik', 'kum_koyu'
KT, KTA = 'kirmizi_tas', 'kirmizi_tas_acik'
SAR = (KM, KM, KMA, 'koyu')
NIS = (KM, KM, KMA, KMA)
KRM = (KT, KT, KTA, 'koyu')
Z0 = 0.03
WH = 0.22
WK = 0.08
GX0, GX1, GY0, GY1 = -1.16, 1.16, -1.1, 1.06
W = [V(-0.74, -0.85), V(0.74, -0.85), V(0.98, -0.62), V(0.98, 0.72), V(0.75, 0.95), V(-0.75, 0.95), V(-0.98, 0.72), V(-0.98, -0.62)]


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def _icinde(x, yy, kose):
    ic = False
    n = len(kose)
    for i in range(n):
        a, b = kose[i], kose[(i + 1) % n]
        if (a.y > yy) != (b.y > yy) and x < a.x + (b.x - a.x) * (yy - a.y) / (b.y - a.y):
            ic = not ic
    return ic


def arazi_renk(x, yy, z):
    n = math.sin(x * 5.3 + 0.7) * math.cos(yy * 4.1 - 0.4) * 0.6 + math.sin(x * 10.0 - yy * 8.0) * 0.4
    if _icinde(x, yy, W):
        return _mix((0.82, 0.70, 0.50), (0.76, 0.63, 0.44), 0.5 + 0.5 * n)          # the trodden sand of the parade ground
    return _mix((0.62, 0.55, 0.36), (0.55, 0.53, 0.33), 0.5 + 0.5 * n)              # dry scrub of Rajputana


doku.KOSE_RENK['toprak_ot'] = arazi_renk

# ---------------- ground ----------------
y.bolum('Zemin')
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'kaya_koyu', 'onarkasagsol')
silme(y, dikdortgen(GX0, GX1, GY0, GY1), Z0 - 0.008, 0.008, 0.005, 'kaya', 'duz')
S = 0.08
nx, ny = int(round((GX1 - GX0) / S)), int(round((GY1 - GY0) / S))
buyuk = set()
for i in range(0, nx - 1, 2):
    for j in range(0, ny - 1, 2):
        xa, xb, ya, yb = GX0 + S * i, GX0 + S * (i + 2), GY0 + S * j, GY0 + S * (j + 2)
        if yb > GY1 + 1e-6: continue
        c4 = ((xa, ya), (xb, ya), (xb, yb), (xa, yb))
        if all(_icinde(px, py, disa(W, -0.12)) for px, py in c4) or not any(_icinde(px, py, disa(W, 0.12)) for px, py in c4):
            buyuk.add((i, j))
            y.yuz_yon([V(xa, ya, Z0), V(xb, ya, Z0), V(xb, yb, Z0), V(xa, yb, Z0)], 'toprak_ot', Z)
for i in range(nx):
    for j in range(ny):
        if (i - i % 2, j - j % 2) in buyuk: continue
        xa, xb = GX0 + S * i, GX0 + S * (i + 1)
        ya, yb = GY0 + S * j, min(GY1, GY0 + S * (j + 1))
        y.yuz_yon([V(xa, ya, Z0), V(xb, ya, Z0), V(xb, yb, Z0), V(xa, yb, Z0)], 'toprak_ot', Z)
# boulders and scrub outside
for (bx, by, r) in ((-1.05, -0.95, 0.035), (-0.92, -1.0, 0.022), (1.05, -0.9, 0.03), (1.08, 0.5, 0.026), (-1.08, 0.3, 0.03)):
    kure(y, (bx, by, Z0 + r * 0.35), r, 'kaya', n=7, kat=4)
for (tx, ty) in ((-0.5, -1.0), (0.55, -1.02), (1.07, -0.3), (-1.07, -0.4)):
    agac2(y, tx, ty, Z0, boy=0.09, key='zeytin')
# the road to the gate
y.yuz_yon([V(-0.07, GY0, Z0 + 0.002), V(0.07, GY0, Z0 + 0.002), V(0.07, -0.93, Z0 + 0.002), V(-0.07, -0.93, Z0 + 0.002)], 'zemin', Z)


# ---------------- helpers ----------------
def burj(c, r=0.085, h=WH + 0.04, chh=True, cr=0.04):
    """a round bastion: battered yellow shaft, a band, a corbel, rounded merlons, (a chhatri)"""
    zt = kule_yuvarlak(y, c, r, Z0, h, key=KM, cati='duz', mazgal_h=0, n=16, egim=0.1, yarik_say=0, bolum=2, konsol=False)
    rr = r * 1.05
    donel(y, c, [(rr, Z0 + h * 0.5), (rr + 0.004, Z0 + h * 0.5), (rr + 0.004, Z0 + h * 0.5 + 0.008), (rr, Z0 + h * 0.5 + 0.008)], KMA, n=16)
    silme(y, cokgen(c, r, 16), Z0 + h - 0.024, 0.024, 0.014, KMA, 'duz')
    kangura_halka(y, cokgen(c, r, 7, math.pi / 7), zt, h=0.028, kal=0.012, key=KM, delik=None, n_yay=3, w=0.026, g=0.018)
    if chh:
        chhatri2(y, c[0], c[1], zt - 0.012, cr, n=6, kolon=KMA, kubbe=KMA, kaide=KM, kat=0.0, nk=10)


def ic_cati(kose, z, key='zemin'):
    y.yuz_yon([V(p.x, p.y, z) for p in kose], key, Z)


# ---------------- walls ----------------
y.bolum('Surlar')
LG = (V(-0.13, -0.85), V(0.13, -0.85))
yol = [LG[1], W[1], W[2], W[3], W[4], W[5], W[6], W[7], W[0], LG[0]]
sur(y, yol, Z0, WH, kalinlik=WK, key=KM, mazgal_h=0, parapet_h=0.012, ust_key=KMA)
for i in range(len(yol) - 1):
    e_ = (yol[i + 1] - yol[i]).normalized()
    on_ = V(e_.y, -e_.x).dot(V(-0.57, -0.82)) > 0.3
    kangura(y, yol[i], yol[i + 1], Z0 + WH + 0.012, h=0.032, kal=0.016, key=KM, delik='koyu' if on_ else None, n_yay=3, w=0.028, g=0.019)
silme(y, yol, Z0, 0.06, 0.02, KMK, 'kaide', kapali=False)
silme(y, yol, Z0 + WH * 0.5, 0.009, 0.005, KMA, 'duz', kapali=False)
silme(y, yol, Z0 + WH - 0.02, 0.012, 0.008, KMA, 'duz', kapali=False)
y.bolum('Burçlar')
for c in W:
    burj((c.x, c.y), chh=c.y > 0 or True)
for c in (V(-0.42, -0.85), V(0.42, -0.85), V(-0.98, 0.05), V(0.98, 0.05)):
    burj((c.x, c.y), r=0.07, h=WH + 0.03, chh=False)

# ---------------- the gate (pol) ----------------
y.bolum('Kapı: civili kanatlar, jharokha')
GH = 0.34
gx0, gx1, gy0, gy1 = -0.15, 0.15, -0.94, -0.76
L_, a0, a1, hs, apex = kemer_nis(y, V(gx0, gy0), V(gx1, gy0), Z0, GH, en=0.56, ust=0.12, sivri=0.4, derin=0.07, key=KM, yan_key=KM,
                                 alt_key=KMA, k_say=12, cerceve=(0.01, [KMA, KT]))
pa, pb = L_(a0, -Z0, 0.07), L_(a1, -Z0, 0.07)
duz_duvar(y, pa, pb, Z0 + hs * 0.95, Z0 + apex, KM)
m_ = (pa + pb) / 2
# the two leaves, studded with iron spikes against war elephants
civili_kanat(y, pa, m_, Z0, hs * 0.95, 'ahsap', 'demir', nu=3, nv=5)
civili_kanat(y, m_, pb, Z0, hs * 0.95, 'ahsap', 'demir', nu=3, nv=5)
# a jharokha over the arch, a band of blind niches, the top
jharokha2(y, V(-0.06, gy0), V(0.06, gy0), Z0 + apex + 0.03, 0.08, 0.06, 0.04, KM, KMA, cati='bangla', cati_key=KT, bicim='dochala')
for (u0, u1) in ((0.0, a0 - 0.02), (a1 + 0.02, 0.3)):
    nis_satir(y, L_(u0, 0, -0.0025), L_(u1, 0, -0.0025), Z0 + 0.04, Z0 + 0.15, 1, NIS, en=0.6, derin=0.008, sivri=0.3)
    nis_satir(y, L_(u0, 0, -0.0025), L_(u1, 0, -0.0025), Z0 + 0.17, Z0 + 0.28, 1, NIS, en=0.6, derin=0.008, sivri=0.3)
    for (v0_, v1_) in ((0.04, 0.15), (0.17, 0.28)):
        cikinti_kenar(y, L_(u0, 0, -0.0025), L_(u1, 0, -0.0025), Z0 + v0_, Z0 + v1_, 0.0025, KM)
duz_duvar(y, V(gx1, gy0), V(gx1, gy1), Z0, Z0 + GH, KM)
duz_duvar(y, V(gx0, gy1), V(gx0, gy0), Z0, Z0 + GH, KM)
y.kemerli(V(gx1, gy1), V(gx0, gy1), Z0, GH * 0.72, SAR, en=0.5, ust=0.03, derin=0.06, k_say=10, sivri=0.4)
duz_duvar(y, V(gx1, gy1), V(gx0, gy1), Z0 + GH * 0.72, Z0 + GH, KM)
gk = dikdortgen(gx0, gx1, gy0, gy1)
silme(y, gk, Z0, 0.05, 0.016, KMK, 'kaide')
chhajja(y, gk, Z0 + GH - 0.03, 0.016, 0.026, KMA)
# (no band over the walls' top: it flickered)
ic_cati(gk, Z0 + GH, 'zemin')
parapet(y, gk, Z0 + GH, 0.012, 0, 0.012, KM, ust_key=KMA)
kangura_halka(y, gk, Z0 + GH + 0.012, h=0.03, kal=0.012, key=KM, n_yay=3)
# the two gate bastions, taller, with chhatris
for sx in (-1, 1):
    burj((sx * 0.215, -0.87), r=0.095, h=GH + 0.05, chh=True, cr=0.05)
sancak(y, 0.0, -0.85, Z0 + GH + 0.012, boy=0.3, en=0.12, yuk=0.075, aci=-0.6)

# ---------------- the commander's palace ----------------
y.bolum('Komutan sarayı')
PX0, PX1, PY0, PY1 = -0.4, 0.4, 0.5, 0.88
H1, H2, H3 = 0.18, 0.15, 0.13
z1, z2, z3 = Z0 + H1, Z0 + H1 + H2, Z0 + H1 + H2 + H3
pk = dikdortgen(PX0, PX1, PY0, PY1)
# ground storey: an engrailed arcade on the front, blind niches on the sides
dilimli_sira(y, V(PX0, PY0), V(PX1, PY0), 7, Z0, H1, KRM, en=0.66, ust=0.03, derin=0.05, sivri=0.3, dilim=5, gir=0.06, cerceve=(0.004, KTA))
for (a, b, n) in ((V(PX1, PY0), V(PX1, PY1), 4), (V(PX0, PY1), V(PX0, PY0), 4), (V(PX1, PY1), V(PX0, PY1), 7)):
    nis_satir(y, a, b, Z0, z1, n, (KT, KT, KTA, KTA), en=0.6, derin=0.008, sivri=0.3)
silme(y, pk, Z0, 0.03, 0.012, KT, 'kaide')
chhajja(y, pk, z1 - 0.016, 0.016, 0.026, KTA)
# second storey: wall with jharokhas
for (a, b) in ((V(PX1, PY0), V(PX1, PY1)), (V(PX0, PY1), V(PX0, PY0)), (V(PX1, PY1), V(PX0, PY1))):
    duz_duvar(y, a, b, z1, z2, KT)
duz_duvar(y, V(PX0, PY0), V(PX1, PY0), z1, z2, KT)
for i in range(5):
    xm = PX0 + (PX1 - PX0) * (i + 0.5) / 5
    jharokha2(y, V(xm - 0.05, PY0), V(xm + 0.05, PY0), z1 + 0.025, 0.075, 0.07, 0.04, KT, KTA, cati='bangla' if i % 2 == 0 else 'kubbe',
              cati_key=KTA, perde=KTA if i % 2 else None, bicim='dochala')
for (a, b, n) in ((V(PX1, PY0), V(PX1, PY1), 3), (V(PX0, PY1), V(PX0, PY0), 3)):
    for k in range(n):
        p, q = a.lerp(b, (k + 0.5) / n - 0.05), a.lerp(b, (k + 0.5) / n + 0.05)
        jharokha2(y, p, q, z1 + 0.025, 0.06, 0.065, 0.03, KT, KTA, cati='kubbe', cati_key=KTA)
chhajja(y, pk, z2 - 0.014, 0.014, 0.024, KTA)
# third storey: set back, jali windows
P3 = (PX0 + 0.04, PX1 - 0.04, PY0 + 0.04, PY1 - 0.04)
k3 = dikdortgen(*P3)
for i in range(4):
    a, b = k3[i], k3[(i + 1) % 4]
    n = 7 if i % 2 == 0 else 4
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        dikdortgen_acik(y, p, q, z2, H3, 0.28, 0.72, 0.02, 0.08, (KT, KT, KTA, 'koyu'), derin=0.01, cerceve=(0.004, KTA), ic_kenar=True)
        if i == 0:
            kafes(y, p, q, z2, 0.28, 0.72, 0.02, 0.08, KTA, 3, 3, 0.002, 0.0015)
# the terrace round it
for i in range(4):
    j = (i + 1) % 4
    y.yuz_yon([pk[i] + Z * z2, pk[j] + Z * z2, k3[j] + Z * z2, k3[i] + Z * z2], 'zemin', Z)
parapet(y, pk, z2, 0.016, 0, 0.01, KT, ust_key=KTA)
chhajja(y, k3, z3 - 0.014, 0.014, 0.022, KTA)
ic_cati(k3, z3, 'zemin')
parapet(y, k3, z3, 0.012, 0, 0.01, KT, ust_key=KTA)
kangura_halka(y, k3, z3 + 0.012, h=0.022, kal=0.009, key=KT, delik=None, n_yay=3)
# corner chhatris on the terrace
for p in pk:
    q = p + (V(0, (PY0 + PY1) / 2) - V(p.x, (PY0 + PY1) / 2)).normalized() * 0.0
    cx, cy = p.x + (0.03 if p.x < 0 else -0.03), p.y + (0.03 if p.y < 0.7 else -0.03)
    chhatri2(y, cx, cy, z2 + 0.016, 0.028, n=6, kolon=KTA, kubbe=KTA, kaide=KT, kat=0.0, nk=10)
# the tower over the middle: a pavilion storey of arches and a bangla roof flanked by domes
TX0, TX1, TY0, TY1 = -0.14, 0.14, 0.6, 0.78
tk = dikdortgen(TX0, TX1, TY0, TY1)
HT = 0.17
dilimli_sira(y, V(TX0, TY0), V(TX1, TY0), 3, z3, HT, KRM, v0=0.012, en=0.66, ust=0.02, derin=0.03, sivri=0.3, dilim=5, gir=0.06,
             korkuluk=0.02)
for (a, b, n) in ((V(TX1, TY0), V(TX1, TY1), 2), (V(TX0, TY1), V(TX0, TY0), 2), (V(TX1, TY1), V(TX0, TY1), 3)):
    dilimli_sira(y, a, b, n, z3, HT, KRM, v0=0.012, en=0.6, ust=0.02, derin=0.008, sivri=0.3, dilim=5, gir=0.06)
chhajja(y, tk, z3 + HT - 0.014, 0.014, 0.026, KTA)
ic_cati(tk, z3 + HT, KTA)
# (the arcades reach the roof: no second band)
# the bangla pavilion on the tower: a plinth, pillars with bracket capitals, a lintel, and a do-chala (Bengal hut) roof
# whose ridge arches down to its ends and whose eave corners hang low over the pillars
zt_ = z3 + HT
bx0, bx1, by0, by1 = -0.072, 0.072, TY0 + 0.028, TY1 - 0.028
kutu(y, V(bx0 - 0.01, by0 - 0.01, zt_), X, bx1 - bx0 + 0.02, by1 - by0 + 0.02, 0.01, KT, 'onarkasagsolust')
zp_ = zt_ + 0.01
PLH = 0.05
for px in (bx0 + 0.006, 0.0, bx1 - 0.006):
    for py in (by0 + 0.006, by1 - 0.006):
        kutu_merkez(y, (px, py), 0.01, 0.01, PLH, KTA, z0=zp_, yuzler='onarkasagsol')
        kutu_merkez(y, (px, py), 0.016, 0.016, 0.006, KTA, z0=zp_ + PLH - 0.006, yuzler='onarkasagsol')
for px in (bx0 + 0.006, bx1 - 0.006):
    kutu_merkez(y, (px, (by0 + by1) / 2), 0.01, 0.01, PLH, KTA, z0=zp_, yuzler='onarkasagsol')
lk = dikdortgen(bx0, bx1, by0, by1)
zl_ = zp_ + PLH
duvarlar(y, lk, zl_, zl_ + 0.008, KT)
y.yuz_yon([V(p.x, p.y, zl_) for p in lk], KTA, -Z)
ztop = bangla_cati(y, bx0, bx1, by0, by1, zl_ + 0.014, 0.052, KT, sacak=0.018, alt_key=KTA, nu=14, nv=8, kalin=0.007, egik=0.42,
                   bicim='dochala', sarkma=0.5, sirt_key='altin', alin_z=zl_ + 0.008)
for sx in (-1, 1):   # gilded finials at the ridge's ends
    kalasa(y, sx * (bx1 + 0.018 - 0.006), (by0 + by1) / 2, zl_ + 0.014 + 0.052 * (1 - 0.42 * 0.87) - 0.002, s=0.45)
for sx in (-1, 1):
    chhatri2(y, sx * 0.115, (TY0 + TY1) / 2, z3 + HT, 0.032, n=6, kolon=KTA, kubbe=KTA, kaide=KT, kat=0.0, nk=12)
sancak(y, 0.0, (TY0 + TY1) / 2, ztop - 0.004, boy=0.18, en=0.1, yuk=0.06, aci=-0.6, kuyruk=True)
# steps up to the palace
merdiven(y, (0.0, PY0 - 0.12), math.pi / 2, 0.14, Z0, Z0 + 0.03, n=4, key=KMA)
kutu(y, V(-0.2, PY0 - 0.06, Z0), X, 0.4, 0.06, 0.03, KMA, 'onsagsolust')

# ---------------- cavalry stables ----------------
y.bolum('Süvari ahırları ve atlar')
AX0, AX1, AY0, AY1 = -0.9, -0.7, -0.5, 0.4
ak = dikdortgen(AX0, AX1, AY0, AY1)
AH = 0.12
dilimli_sira(y, V(AX1, AY0), V(AX1, AY1), 8, Z0, AH, SAR, en=0.7, ust=0.024, derin=0.06, sivri=0.25, dilim=5, gir=0.05)
for (a, b) in ((V(AX1, AY1), V(AX0, AY1)), (V(AX0, AY0), V(AX1, AY0))):
    duz_duvar(y, a, b, Z0, Z0 + AH, KM)
chhajja(y, [ak[1], ak[2]], Z0 + AH - 0.012, 0.012, 0.03, KMA, kapali=False)
ic_cati(ak, Z0 + AH, 'zemin')
parapet(y, ak, Z0 + AH, 0.014, 0, 0.01, KM, ust_key=KMA)
for k in range(9):
    yy = AY0 + (AY1 - AY0) * k / 8
    kutu(y, V(AX1 - 0.002, yy - 0.006, Z0), Y, 0.012, -0.008, AH - 0.01, KMA, 'onarkasagsolust')
# hitching rail and horses facing their stalls
cubuk(y, V(AX1 + 0.09, AY0 + 0.05, Z0 + 0.035), V(AX1 + 0.09, AY1 - 0.05, Z0 + 0.035), 0.005, 'ahsap')
for yy in (AY0 + 0.05, AY1 - 0.05, (AY0 + AY1) / 2):
    kutu_merkez(y, (AX1 + 0.09, yy), 0.008, 0.008, 0.04, 'ahsap_koyu', z0=Z0)
for k, yy in enumerate((-0.4, -0.22, -0.04, 0.14, 0.31)):
    at(y, AX1 + 0.14, yy, Z0, aci=math.pi, s=0.95, key=('ahsap', 'kum_acik', 'ahsap_koyu', 'beyaz')[k % 4], yele='ahsap_koyu')
for (hx, hy) in ((AX1 + 0.05, -0.47), (AX1 + 0.05, 0.38)):
    yigin(y, hx, hy, Z0, 0.025, 0.035, 'saz', sepetli=False, n=10)

# ---------------- barracks and war elephants ----------------
y.bolum('Kışla ve savaş filleri')
BX0, BX1, BY0, BY1 = 0.7, 0.9, -0.52, 0.4
bk = dikdortgen(BX0, BX1, BY0, BY1)
BH1, BH2 = 0.1, 0.09
dilimli_sira(y, V(BX0, BY1), V(BX0, BY0), 7, Z0, BH1, SAR, en=0.7, ust=0.02, derin=0.04, sivri=0.25, dilim=5, gir=0.05)
dilimli_sira(y, V(BX0, BY1), V(BX0, BY0), 7, Z0 + BH1, BH2, SAR, v0=0.01, en=0.6, ust=0.02, derin=0.02, sivri=0.25, dilim=3, gir=0.05,
             korkuluk=0.016)
silme(y, [V(BX0, BY1), V(BX0, BY0)], Z0 + BH1 - 0.006, 0.01, 0.012, KMA, 'duz', kapali=False)
for (a, b) in ((V(BX0, BY0), V(BX1, BY0)), (V(BX1, BY1), V(BX0, BY1))):
    duz_duvar(y, a, b, Z0, Z0 + BH1 + BH2, KM)
chhajja(y, [bk[3], bk[0]], Z0 + BH1 + BH2 - 0.012, 0.012, 0.026, KMA, kapali=False)
ic_cati(bk, Z0 + BH1 + BH2, 'zemin')
parapet(y, bk, Z0 + BH1 + BH2, 0.014, 0, 0.01, KM, ust_key=KMA)
for (cx, cy) in ((BX0 + 0.04, BY0 + 0.04), (BX0 + 0.04, BY1 - 0.04)):
    chhatri2(y, cx, cy, Z0 + BH1 + BH2, 0.03, n=6, kolon=KMA, kubbe=KMA, kaide=KM, kat=0.0, nk=10)
# elephant stalls: a pillared shed with a flat roof, two war elephants
for k in range(5):
    yy = -0.2 + 0.11 * k
    kutu_merkez(y, (0.52, yy), 0.014, 0.014, 0.17, KMA, z0=Z0)
kutu(y, V(0.5, -0.215, Z0 + 0.17), X, 0.2, 0.47, 0.012, KM, 'onarkasagsolust')
y.yuz_yon([V(0.5, -0.215, Z0 + 0.17), V(0.7, -0.215, Z0 + 0.17), V(0.7, 0.255, Z0 + 0.17), V(0.5, 0.255, Z0 + 0.17)], KM, -Z)
silme(y, [V(0.5, 0.255), V(0.5, -0.215)], Z0 + 0.17, 0.012, 0.008, KMA, 'duz', kapali=False)
fil(y, 0.6, -0.08, Z0, aci=math.pi, olcek=0.85, key='fil', cul='boya_kirmizi', binici='beyaz', kaba=True)
fil(y, 0.6, 0.15, Z0, aci=math.pi, olcek=0.85, key='fil', cul='lacivert', haudah='altin', kaba=True)
fil(y, 0.3, -0.1, Z0, aci=-math.pi * 0.75, olcek=0.85, key='fil', cul='boya_sari', binici='boya_kirmizi')

# ---------------- parade ground ----------------
y.bolum('Talim alanı')
# soldiers drilling in ranks, an officer, practice posts
for r_ in range(3):
    for c_ in range(3):
        px, py = -0.44 + 0.065 * c_, -0.3 + 0.07 * r_
        adam(y, px, py, Z0, -math.pi / 2, 'boya_sari' if r_ != 1 else 'boya_kirmizi', 'boya_kirmizi' if r_ != 1 else 'boya_sari', boy=0.034)
        cubuk(y, V(px + 0.008, py, Z0 + 0.008), V(px + 0.008, py, Z0 + 0.065), 0.0025, 'ahsap')
adam(y, -0.375, -0.39, Z0, math.pi / 2, 'beyaz', 'boya_kirmizi', boy=0.04)
for (px, py) in ((0.1, -0.4), (0.2, -0.4), (0.1, -0.28), (0.2, -0.28)):
    kutu_merkez(y, (px, py), 0.014, 0.014, 0.06, 'ahsap', z0=Z0)
    kure(y, (px, py, Z0 + 0.07), 0.013, 'saz', n=8, kat=4)
# horsemen riding a drill
for k, (px, py, a) in enumerate(((-0.05, -0.12, 0.3), (0.06, -0.05, 0.5), (-0.12, 0.0, 0.2))):
    at(y, px, py, Z0, aci=a, s=1.0, key=('ahsap', 'beyaz', 'ahsap_koyu')[k], yele='ahsap_koyu', kosu=0.6, faz=k * 0.3)
    adam(y, px - 0.004 * math.cos(a), py - 0.004 * math.sin(a), Z0 + 0.06, a, ('boya_kirmizi', 'boya_sari', 'boya_kirmizi')[k], 'boya_sari', boy=0.034)
    cubuk(y, V(px, py + 0.01, Z0 + 0.07), V(px + 0.04 * math.cos(a), py + 0.04 * math.sin(a) + 0.01, Z0 + 0.13), 0.0025, 'ahsap')
# a raised review platform with a chhatri
kutu_merkez(y, (-0.3, 0.2), 0.14, 0.14, 0.03, KMA, z0=Z0)
silme(y, dikdortgen(-0.37, -0.23, 0.13, 0.27), Z0, 0.012, 0.006, KM, 'kaide')
chhatri2(y, -0.3, 0.2, Z0 + 0.03, 0.05, n=8, kolon=KMA, kubbe=KMA, kaide=KM, nk=16)
merdiven(y, (-0.3, 0.07), math.pi / 2, 0.06, Z0, Z0 + 0.03, n=3, key=KMA)
# a well
y.prizma((0.3, 0.32), 0.04, Z0, Z0 + 0.025, KM, n=12, ust=False)
y.yuz_yon([V(p.x, p.y, Z0 + 0.015) for p in cokgen((0.3, 0.32), 0.032, 12)], 'su', Z)
duvarlar(y, [cokgen((0.3, 0.32), 0.032, 12)[(12 - i) % 12] for i in range(12)], Z0 + 0.015, Z0 + 0.025, KM)
for i in range(12):
    p0, p1 = cokgen((0.3, 0.32), 0.04, 12), cokgen((0.3, 0.32), 0.032, 12)
    j = (i + 1) % 12
    y.yuz_yon([p0[i] + Z * (Z0 + 0.025), p0[j] + Z * (Z0 + 0.025), p1[j] + Z * (Z0 + 0.025), p1[i] + Z * (Z0 + 0.025)], KMA, Z)
for sx in (-1, 1):
    cubuk(y, V(0.3 + sx * 0.045, 0.32, Z0), V(0.3 + sx * 0.045, 0.32, Z0 + 0.08), 0.008, 'ahsap')
cubuk(y, V(0.25, 0.32, Z0 + 0.08), V(0.35, 0.32, Z0 + 0.08), 0.008, 'ahsap')
for (tx, ty) in ((-0.55, 0.55), (0.55, 0.55), (-0.15, 0.3), (0.42, 0.62)):
    agac2(y, tx, ty, Z0, boy=0.11, key='boya_yesil')

bolum_say(y)
calistir(y, 'lm_racputkisla')
