# Aachen Sarayı (lm_aachen): Charlemagne's palace. The Palatine Chapel: a sixteen-sided two-storey ambulatory with
# round-arched windows and pilaster strips under a lean-to roof, the octagonal clerestory drum with great arched
# windows and the eight-sided pleated dome (the silhouette); the westwork before it with its tall entrance niche,
# throne loggia and two round stair turrets; a small square choir. A two-storey arcaded gallery with a gate tower
# leads to the Aula Regia, the long basilica-like hall with its apses and the Granus tower. Carolingian stone:
# light limestone with darker sandstone bands and alternating voussoirs. The atrium holds the bronze pine cone.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ortak import *
from bina_ortak import calistir

y = Yapi()

TAS, BANT, KOYU = 'kirec', 'kum_koyu', 'tas_koyu'
KEM = [TAS, BANT]                     # alternating voussoirs
PEN = (TAS, KOYU, 'tas_acik', 'cam')
Z0 = 0.04

# ---------------------------------------------------------------- platform
y.bolum('Zemin ve avlu')
zemin(y, -1.02, 1.1, -0.98, 0.98, Z0, 'kum_koyu', 'zemin', basamak=(), n_basamak=3)
for k in range(3):   # steps up to the atrium gate
    kutu(y, V(-0.36 - 0.16, -0.98 - 0.03 * (k + 1), 0), X, 0.32, 0.03 * (k + 1) + 0.001, Z0 * (3 - k) / 4, 'kum_koyu', 'onsagsolust')


def bant_duvar(a, b, z0, z1, bantlar):
    """a plain wall a->b with string courses: bantlar = list of z heights of thin sandstone bands"""
    duz_duvar(y, a, b, z0, z1, TAS)
    for zz in bantlar:
        e = (V(b[0], b[1]) - V(a[0], a[1])).normalized(); nn = V(e.y, -e.x)
        pa, pb = V(a[0], a[1]) + nn * 0.002, V(b[0], b[1]) + nn * 0.002
        y.yuz_yon([pa + Z * zz, pb + Z * zz, pb + Z * (zz + 0.01), pa + Z * (zz + 0.01)], BANT, nn)


# ---------------------------------------------------------------- the Palatine Chapel
y.bolum('Pfalzkapelle: on altıgen dış koridor (iki kat)')
C = V(-0.36, -0.1)
R16 = 0.4
z1, z2 = Z0 + 0.19, Z0 + 0.36        # the ambulatory's storeys
k16 = cokgen(C, R16, 16, math.pi / 16)
donel(y, (C.x, C.y), [(R16 * 1.04, Z0), (R16 * 1.04, Z0 + 0.025), (R16 * 1.0, Z0 + 0.035)], BANT, n=16, kat=math.pi / 16)
for i in range(16):
    a, b = k16[i], k16[(i + 1) % 16]
    mid = (a + b) / 2
    ang = math.atan2(mid.y - C.y, mid.x - C.x)
    front = abs(ang + math.pi / 2) < 0.3          # the westwork covers these
    if front:
        duz_duvar(y, a, b, Z0, z2, TAS); continue
    y.kemerli(a, b, Z0 + 0.035, z1 - Z0 - 0.035, PEN, v0=0.05, en=0.34, ust=0.03, derin=0.02, k_say=6, cerceve=(0.008, KEM))
    y.kemerli(a, b, z1, z2 - z1, PEN, v0=0.03, en=0.4, ust=0.025, derin=0.02, k_say=6, cerceve=(0.008, KEM))
# pilaster strips on the corners, string courses
for i, p in enumerate(k16):
    d = (p - C).normalized(); t = V(-d.y, d.x)
    kutu3(y, p + d * 0.006 + Z * ((Z0 + 0.035 + z2) / 2), d, t, Z, 0.014, 0.024, z2 - Z0 - 0.035, TAS, ('+x', '+y', '-y', '+z'))
silme(y, k16, z1 - 0.006, 0.012, 0.012, BANT, 'duz')
silme(y, k16, z2 - 0.004, 0.018, 0.02, TAS, 'tac')
# the lean-to roof from the ambulatory's eave up to the drum
R8 = 0.25
ZD0 = z2 + 0.1                    # where the roof meets the drum
r_eave = R16 + 0.03
ring_e = cokgen(C, r_eave, 16, math.pi / 16)
ring_t = cokgen(C, R8 * 0.97, 16, math.pi / 16)
nr = 4
for k in range(nr):
    ra = [p.lerp(q, k / nr) + Z * (z2 + 0.014 + (ZD0 - z2 - 0.014) * k / nr) for p, q in zip(ring_e, ring_t)]
    rb = [p.lerp(q, (k + 1) / nr) + Z * (z2 + 0.014 + (ZD0 - z2 - 0.014) * (k + 1) / nr) for p, q in zip(ring_e, ring_t)]
    for i in range(16):
        j = (i + 1) % 16
        m = (ra[i] + ra[j]) / 2
        y.yuz_yon([ra[i], ra[j], rb[j], rb[i]], 'arduvaz', V(m.x - C.x, m.y - C.y, 0.6))
for i in range(16):   # eave fascia and soffit
    j = (i + 1) % 16
    m = (ring_e[i] + ring_e[j]) / 2
    o = V(m.x - C.x, m.y - C.y)
    y.yuz_yon([ring_e[i] + Z * (z2 + 0.014), ring_e[j] + Z * (z2 + 0.014), ring_e[j] + Z * (z2 + 0.004), ring_e[i] + Z * (z2 + 0.004)], 'ahsap_koyu', o)
    y.yuz_yon([ring_e[i] + Z * (z2 + 0.004), ring_e[j] + Z * (z2 + 0.004), k16[j] + Z * (z2 + 0.014), k16[i] + Z * (z2 + 0.014)], 'ahsap_koyu', -Z)

y.bolum('Pfalzkapelle: sekizgen kasnak ve kubbe')
ZD1 = ZD0 + 0.28
k8 = cokgen(C, R8, 8, math.pi / 8)
duvarlar(y, k8, ZD0 - 0.1, ZD0, TAS)
for i in range(8):
    a, b = k8[i], k8[(i + 1) % 8]
    y.kemerli(a, b, ZD0, ZD1 - ZD0, PEN, v0=0.04, en=0.5, ust=0.04, derin=0.026, k_say=10, cerceve=(0.01, KEM))
for p in k8:
    d = (p - C).normalized(); t = V(-d.y, d.x)
    kutu3(y, p + d * 0.008 + Z * ((ZD0 - 0.03 + ZD1) / 2), d, t, Z, 0.018, 0.03, ZD1 - ZD0 + 0.03, TAS, ('+x', '+y', '-y', '+z'))
# a blind arcade frieze under the cornice: small arches on each face
for i in range(8):
    a, b = k8[i], k8[(i + 1) % 8]
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    for m in range(4):
        u = (m + 0.5) / 4
        p = a.lerp(b, u) + nn * 0.003
        pts = [p + e * (L / 8 * 0.7 * math.cos(math.pi * k / 6)) + Z * (ZD1 - 0.032 + L / 8 * 0.7 * math.sin(math.pi * k / 6)) for k in range(7)]
        q = [p - e * (L / 8 * 0.7) + Z * (ZD1 - 0.05), p + e * (L / 8 * 0.7) + Z * (ZD1 - 0.05)] + \
            [p + e * (L / 8 * 0.7 * math.cos(math.pi * k / 6)) + Z * (ZD1 - 0.032 + L / 8 * 0.7 * math.sin(math.pi * k / 6)) for k in range(7)]
        y.yuz_yon(q, BANT, nn)
silme(y, k8, ZD1 - 0.004, 0.022, 0.024, TAS, 'tac')
# the dome: an eight-sided pleated (cloister) roof in lead, ribs at the corners, a lantern, the orb and cross
ZK = ZD1 + 0.018
pr = [(R8 + 0.03, ZK), (R8 * 0.99, ZK + 0.06), (R8 * 0.86, ZK + 0.13), (R8 * 0.64, ZK + 0.2), (R8 * 0.36, ZK + 0.255), (0.05, ZK + 0.28)]
donel(y, (C.x, C.y), [(0.05, ZK + 0.28), (0.0, ZK + 0.28)], 'kursun', n=16, kat=math.pi / 8)
donel(y, (C.x, C.y), pr, 'kursun', n=16, kat=math.pi / 8, dilim=['kursun', 'kursun2'])
y.yuz_yon([V(p.x, p.y, ZK) for p in cokgen(C, R8 + 0.03, 16, math.pi / 8)], 'ahsap_koyu', -Z)
for i in range(8):   # ribs over the folds
    a = math.pi / 8 + TAU * i / 8
    d = V(math.cos(a), math.sin(a))
    pts = [V(C.x, C.y) + d * (r_ + 0.004) + Z * (zz + 0.004) for r_, zz in pr]
    boru(y, pts, 0.006, 'kursun2', n=5)
ZL = ZK + 0.28
y.prizma((C.x, C.y), 0.05, ZL, ZL + 0.05, 'kursun', n=8, kat=math.pi / 8, ust=False)
donel(y, (C.x, C.y), [(0.06, ZL + 0.05), (0.035, ZL + 0.08), (0.0, ZL + 0.1)], 'kursun', n=8, kat=math.pi / 8)
kure(y, (C.x, C.y, ZL + 0.115), 0.016, 'altin', n=10, kat=5)
hac(y, C.x, C.y, ZL + 0.125, 0.07, 'altin')

y.bolum('Westwerk: giriş nişi, taht locası, merdiven kuleleri')
WX0, WX1 = C.x - 0.14, C.x + 0.14
WY0, WY1 = C.y - R16 - 0.16, C.y - R16 + 0.09
WZ = Z0 + 0.62
wk = dikdortgen(WX0, WX1, WY0, WY1)
kutu(y, V(WX0 - 0.012, WY0 - 0.012, Z0), X, WX1 - WX0 + 0.024, WY1 - WY0 + 0.012, 0.03, BANT, 'onsagsolust')
# the front: a tall round-arched niche two storeys high, the bronze doors at its foot and the throne loggia above
L_, x0n, x1n, hs, apex = kemer_nis(y, V(WX0, WY0), V(WX1, WY0), Z0, WZ - Z0 - 0.08, en=0.5, ust=0.06, sivri=0.0, derin=0.05, key=TAS,
                                   yan_key=KOYU, alt_key='tas_acik', k_say=12, cerceve=(0.012, KEM))
nd = 0.05
duz_duvar(y, V(WX0, WY0), V(WX1, WY0), WZ - 0.08, WZ, TAS)
W_ = WX1 - WX0
# the niche's back: doors below, the loggia's arched opening above, a band between
bx0, bx1 = WX0 + x0n, WX0 + x1n
yb = WY0 + nd
dikdortgen_acik(y, V(bx0, yb), V(bx1, yb), Z0, 0.2, 0.18, 0.82, 0.0, 0.16, (TAS, KOYU, 'tas_acik', 'bronz'), derin=0.012, cerceve=(0.008, BANT))
for s in (0.35, 0.65):   # the bronze doors' panels
    pp = V(bx0, yb).lerp(V(bx1, yb), s)
    cubuk(y, V(pp.x, yb - 0.0115, Z0 + 0.002), V(pp.x, yb - 0.0115, Z0 + 0.158), 0.003, 'altin', 0.002)
y.kemerli(V(bx0, yb), V(bx1, yb), Z0 + 0.2, (Z0 + hs + (apex - hs)) - (Z0 + 0.2), (TAS, KOYU, 'tas_acik', 'koyu'), v0=0.04, en=0.62, ust=0.002,
          derin=0.03, k_say=10, korkuluk=0.03, cerceve=(0.008, KEM))
kutu(y, V(bx0, yb - 0.012, Z0 + 0.19), X, bx1 - bx0, 0.012, 0.012, BANT, 'onust')
# sides and back
for (a, b) in ((wk[1], wk[2]), (wk[3], wk[0])):
    e = (b - a).normalized()
    n2 = 2
    for m in range(n2):
        p, q = a.lerp(b, m / n2), a.lerp(b, (m + 1) / n2)
        if m == 0:
            y.kemerli(p, q, Z0, WZ - Z0 - 0.18, (TAS, KOYU, 'tas_acik', 'cam'), v0=0.24, en=0.36, ust=0.08, derin=0.02, k_say=6, cerceve=(0.007, KEM))
            duz_duvar(y, p, q, WZ - 0.18, WZ, TAS)
        else:
            duz_duvar(y, p, q, Z0, WZ, TAS)
duz_duvar(y, wk[2], wk[3], z2 + 0.06, WZ, TAS)
for zz in (Z0 + 0.2, z2 + 0.06):   # (string courses stop at the niche's frame: they must not cross its opening)
    silme(y, [wk[3], wk[0], V(bx0 - 0.016, WY0)], zz - 0.005, 0.01, 0.01, BANT, 'duz', kapali=False)
    silme(y, [V(bx1 + 0.016, WY0), wk[1], wk[2]], zz - 0.005, 0.01, 0.01, BANT, 'duz', kapali=False)
# pilasters at the corners, the cornice and a hipped roof
for p in wk[:2]:
    kutu_merkez(y, (p.x, p.y), 0.03, 0.03, WZ - Z0, TAS, z0=Z0)
silme(y, wk, WZ - 0.006, 0.016, 0.016, TAS, 'tac')
top_w = cati_kirma(y, WX0, WX1, WY0, WY1, WZ + 0.01, 0.2, 0.024, 'arduvaz', 'arduvaz', ns=6, nr=6)
# the round stair turrets either side
for sx in (-1, 1):
    tc = (C.x + sx * (W_ / 2 + 0.05), WY0 + 0.07)
    r_ = 0.058
    donel(y, tc, [(r_ * 1.15, Z0), (r_ * 1.15, Z0 + 0.03), (r_, Z0 + 0.04)], BANT, n=16)
    for k_ in range(5):
        za = Z0 + 0.04 + (WZ + 0.06 - Z0 - 0.04) * k_ / 5
        zb_ = Z0 + 0.04 + (WZ + 0.06 - Z0 - 0.04) * (k_ + 1) / 5
        y.prizma(tc, r_, za, zb_, TAS, n=16, ust=False)
        if k_ > 0:
            halka_kornis(y, tc, r_, za - 0.004, 0.008, 0.006, 16, BANT)
        for a in (math.pi * (0.25 if sx > 0 else 0.75) - math.pi / 2, math.pi * (0.0 if sx > 0 else 1.0)):
            d = V(math.cos(a), math.sin(a))
            yarik(y, V(tc[0], tc[1]) + d * (r_ + 0.001) + Z * za, V(-d.y, d.x), d, -0.004, (zb_ - za) * 0.3, 0.008, (zb_ - za) * 0.45, 'koyu')
    halka_kornis(y, tc, r_, WZ + 0.055, 0.012, 0.012, 16, TAS)
    donel(y, tc, [(r_ + 0.02, WZ + 0.067), (r_ * 0.6, WZ + 0.13), (0.0, WZ + 0.21)], 'arduvaz', n=16)
    y.yuz_yon([V(p.x, p.y, WZ + 0.067) for p in cokgen(tc, r_ + 0.02, 16)], 'ahsap_koyu', -Z)
    kure(y, (tc[0], tc[1], WZ + 0.22), 0.01, 'altin', n=8, kat=4)
y.bolum('Sancak')
sancak(y, C.x, (WY0 + WY1) / 2, top_w - 0.01, boy=0.17, en=0.12, yuk=0.07, aci=-math.pi * 0.15)

y.bolum('Koro (doğu)')
CH0 = C.y + R16 * 0.9
ck = dikdortgen(C.x - 0.11, C.x + 0.11, CH0, C.y + R16 + 0.17)
for i, (a, b) in enumerate(((ck[0], ck[1]), (ck[1], ck[2]), (ck[2], ck[3]), (ck[3], ck[0]))):
    if i == 0: continue
    n2 = 2 if i != 2 else 1
    for m in range(n2):
        p, q = a.lerp(b, m / n2), a.lerp(b, (m + 1) / n2)
        y.kemerli(p, q, Z0, z2 - 0.04 - Z0, PEN, v0=0.12, en=0.42 if n2 == 2 else 0.3, ust=0.05, derin=0.02, k_say=6, cerceve=(0.007, KEM))
silme(y, ck, z2 - 0.046, 0.016, 0.016, TAS, 'tac')
cati_besik(y, ck[0].x, ck[1].x, ck[0].y, ck[2].y, z2 - 0.04, 0.12, 0.02, 'arduvaz', 'arduvaz', ucluk_key=TAS, ns=5, nr=5, uc_sacak=0.016)

# ---------------------------------------------------------------- the gallery and the gate tower
y.bolum('Galeri ve kapı kulesi')
GY = C.y + 0.02
GW = 0.13
GX0, GX1 = C.x + R16 * 0.92, 0.55
GZ = Z0 + 0.25
for s in (-1, 1):
    yy = GY + s * GW / 2
    a, b = (V(GX0, yy), V(GX1, yy)) if s < 0 else (V(GX1, yy), V(GX0, yy))
    n_ = 6
    for m in range(n_):
        p, q = a.lerp(b, m / n_), a.lerp(b, (m + 1) / n_)
        if (s < 0 and m in (2, 3)) or (s > 0 and m in (2, 3)):
            continue
        y.kemerli(p, q, Z0, 0.13, REVAK, v0=0.0, en=0.62, ust=0.02, derin=0.025, k_say=6, cerceve=(0.006, KEM))
        y.kemerli(p, q, Z0 + 0.13, GZ - Z0 - 0.13, (TAS, KOYU, 'tas_acik', 'cam'), v0=0.03, en=0.36, ust=0.025, derin=0.015, k_say=6)
    silme(y, [a, b], Z0 + 0.128, 0.008, 0.008, BANT, 'duz', kapali=False)
for xa_, xb_ in ((GX0, (GX0 + GX1) / 2 - (GX1 - GX0) / 6), ((GX0 + GX1) / 2 + (GX1 - GX0) / 6, GX1)):   # (not in the gate tower's passage)
    y.yuz_yon([V(xa_, GY - GW / 2, Z0 + 0.13), V(xb_, GY - GW / 2, Z0 + 0.13), V(xb_, GY + GW / 2, Z0 + 0.13), V(xa_, GY + GW / 2, Z0 + 0.13)], 'koyu', -Z)
cati_besik(y, GX0 - 0.02, GX1, GY - GW / 2, GY + GW / 2, GZ, 0.08, 0.018, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=10, nr=5, uc_sacak=0.0)
# the gate tower straddling the gallery
TX, TW_ = (GX0 + GX1) / 2, (GX1 - GX0) / 3 + 0.012
tk = dikdortgen(TX - TW_ / 2, TX + TW_ / 2, GY - GW / 2 - 0.02, GY + GW / 2 + 0.02)
TZ1 = Z0 + 0.46
kemer_dizisi(y, tk[0], tk[1], 1, Z0, 0.2, tk[2].y - tk[0].y, (TAS, KOYU, 'tas_acik', KOYU), en=0.6, ust=0.03, acik=True)
for i in range(4):
    a, b = tk[i], tk[(i + 1) % 4]
    if i in (0, 2):
        y.kemerli(a, b, Z0 + 0.2, TZ1 - Z0 - 0.2, (TAS, KOYU, 'tas_acik', 'cam'), v0=0.06, en=0.36, ust=0.05, derin=0.015, k_say=6,
                  cerceve=(0.006, KEM))
    else:
        duz_duvar(y, a, b, Z0 + 0.2, TZ1, TAS)
silme(y, tk, Z0 + 0.2, 0.01, 0.01, BANT, 'duz')
silme(y, tk, TZ1 - 0.005, 0.014, 0.014, TAS, 'tac')
cati_kirma(y, tk[0].x, tk[1].x, tk[0].y, tk[2].y, TZ1 + 0.008, 0.14, 0.02, 'arduvaz', 'arduvaz', ns=5, nr=5)

# ---------------------------------------------------------------- the Aula Regia
y.bolum('Aula Regia: büyük salon')
AX0, AX1 = 0.55, 0.88
AY0, AY1 = -0.46, 0.64
AZ = Z0 + 0.36
ak = dikdortgen(AX0, AX1, AY0, AY1)
kutu(y, V(AX0 - 0.012, AY0 - 0.012, Z0), X, AX1 - AX0 + 0.024, AY1 - AY0 + 0.024, 0.03, BANT, 'onarkasagsolust')
for i in range(4):
    a, b = ak[i], ak[(i + 1) % 4]
    L = (b - a).length
    n_ = max(1, int(round(L / 0.13)))
    for m in range(n_):
        p, q = a.lerp(b, m / n_), a.lerp(b, (m + 1) / n_)
        mid = (p + q) / 2
        # (the side apse and the gallery cover the west wall's middle)
        if i == 3 and (abs(mid.y - 0.12) < 0.14 or abs(mid.y - GY) < GW / 2 + 0.06):
            duz_duvar(y, p, q, Z0 + 0.03, AZ, TAS); continue
        y.kemerli(p, q, Z0 + 0.03, 0.16, PEN, v0=0.05, en=0.32, ust=0.025, derin=0.018, k_say=6, cerceve=(0.007, KEM))
        y.kemerli(p, q, Z0 + 0.19, AZ - Z0 - 0.19, PEN, v0=0.03, en=0.42, ust=0.03, derin=0.02, k_say=6, cerceve=(0.008, KEM))
    # pilaster strips between the bays
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for m in range(n_ + 1):
        p = a.lerp(b, m / n_)
        kutu3(y, p + nn * 0.005 + Z * ((Z0 + 0.03 + AZ) / 2), e, nn, Z, 0.02, 0.01, AZ - Z0 - 0.03, TAS, ('+y', '+x', '-x', '+z'))
silme(y, ak, Z0 + 0.19, 0.01, 0.01, BANT, 'duz')
silme(y, ak, AZ - 0.006, 0.018, 0.02, TAS, 'tac')
top_a = cati_besik(y, AX0, AX1, AY0, AY1, AZ + 0.01, 0.19, 0.028, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=14, nr=6, uc_sacak=0.018)


def apsis(c, r, z0, h, aci, key_cati='kiremit'):
    """a semicircular apse bulging towards aci, three arched windows, a half-cone roof"""
    t0 = aci - math.pi / 2
    yay = [V(c[0] + r * math.cos(t0 + math.pi * k / 6), c[1] + r * math.sin(t0 + math.pi * k / 6)) for k in range(7)]
    for k in range(6):
        if k in (1, 2, 3, 4):
            y.kemerli(yay[k], yay[k + 1], z0, h, PEN, v0=h * 0.35, en=0.45, ust=h * 0.1, derin=0.016, k_say=6, cerceve=(0.006, KEM))
        else:
            duz_duvar(y, yay[k], yay[k + 1], z0, z0 + h, TAS)
    silme(y, yay, z0 + h - 0.004, 0.012, 0.012, TAS, 'tac', kapali=False)
    tepe = V(c[0], c[1], z0 + h + r * 0.75)
    yr = [V(p.x, p.y) + (V(p.x - c[0], p.y - c[1])).normalized() * 0.02 + Z * (z0 + h + 0.006) for p in yay]
    for k in range(6):
        y.yuz_yon([yr[k], yr[k + 1], tepe], key_cati, V(yr[k].x + yr[k + 1].x - 2 * c[0], yr[k].y + yr[k + 1].y - 2 * c[1], 0.6))
        y.yuz_yon([yr[k], yr[k + 1], V(yay[k + 1].x, yay[k + 1].y, z0 + h + 0.006), V(yay[k].x, yay[k].y, z0 + h + 0.006)], 'ahsap_koyu', -Z)


apsis((AX0, 0.12), 0.12, Z0, 0.27, math.pi)
apsis(((AX0 + AX1) / 2, AY1), 0.12, Z0, 0.29, math.pi / 2)
apsis(((AX0 + AX1) / 2, AY0), 0.12, Z0, 0.29, -math.pi / 2)

y.bolum('Granus kulesi')
GTX, GTY, GTW = AX1 + 0.02, AY0 + 0.22, 0.18
gk = dikdortgen(GTX - GTW / 2, GTX + GTW / 2, GTY - GTW / 2, GTY + GTW / 2)
GTZ = Z0 + 0.72
kutu(y, V(GTX - GTW / 2 - 0.012, GTY - GTW / 2 - 0.012, Z0), X, GTW + 0.024, GTW + 0.024, 0.03, BANT, 'onarkasagsolust')
for i in range(4):
    a, b = gk[i], gk[(i + 1) % 4]
    za = Z0 + 0.03
    for (h_, en_, v0_) in ((0.2, 0.3, 0.08), (0.2, 0.34, 0.05), (GTZ - Z0 - 0.43, 0.5, 0.04)):
        if i == 3 and za < AZ:
            duz_duvar(y, a, b, za, za + h_, TAS)
        else:
            if h_ > 0.25 or za > Z0 + 0.2:
                y.kemerli(a, a.lerp(b, 0.5), za, h_, PEN if h_ < 0.25 else (TAS, KOYU, 'tas_acik', 'koyu'), v0=v0_, en=en_ + 0.15, ust=0.03, derin=0.012,
                          k_say=6, cerceve=(0.006, KEM))
                y.kemerli(a.lerp(b, 0.5), b, za, h_, PEN if h_ < 0.25 else (TAS, KOYU, 'tas_acik', 'koyu'), v0=v0_, en=en_ + 0.15, ust=0.03, derin=0.012,
                          k_say=6, cerceve=(0.006, KEM))
            else:
                y.kemerli(a, b, za, h_, PEN, v0=v0_, en=en_, ust=0.03, derin=0.02, k_say=6, cerceve=(0.007, KEM))
        za += h_
for zz in (Z0 + 0.23, Z0 + 0.43):
    silme(y, gk, zz - 0.005, 0.01, 0.01, BANT, 'duz')
for p in gk:
    for j in range(int((GTZ - Z0) / 0.045)):
        ss = 0.022 if j % 2 == 0 else 0.015
        kutu_merkez(y, (p.x, p.y), ss, ss, 0.024, BANT, z0=Z0 + 0.03 + j * 0.045)
silme(y, gk, GTZ - 0.006, 0.016, 0.016, TAS, 'tac')
top_g = cati_kirma(y, gk[0].x, gk[1].x, gk[0].y, gk[2].y, GTZ + 0.01, 0.2, 0.02, 'arduvaz', 'arduvaz', ns=5, nr=6)
kure(y, (GTX, GTY, top_g + 0.006), 0.01, 'altin', n=8, kat=4)

# ---------------------------------------------------------------- the atrium
y.bolum('Atrium: tunç kozalak, revaklar')
# the atrium: walls round it (a gate in the front), porticoes along the sides under lean-to roofs
AH = 0.11
for sx in (-1, 1):
    x = C.x + sx * 0.38
    alcak_duvar(y, [V(x, -0.92), V(x, WY0 + 0.03)], Z0, AH, 0.03, TAS, 'kiremit')
    xi = x if sx < 0 else x - 0.03                     # the wall's face towards the atrium
    xa = xi - sx * 0.065                                # the arcade's line
    a2, b2 = (V(xa, -0.9), V(xa, WY0 - 0.01)) if sx < 0 else (V(xa, WY0 - 0.01), V(xa, -0.9))
    arkad(y, a2, b2, 4, Z0, 0.075, en=0.66, ust=0.014, sivri=0.0, derin=0.058, cerceve=(0.005, KEM), sutun_key=TAS, sutun_tur='osmanli',
          sutun_r=0.007)
    # the lean-to roof: a slab from the arcade's top up to the wall
    q = [V(xa - sx * 0.012, -0.912, Z0 + 0.079), V(xa - sx * 0.012, WY0 + 0.002, Z0 + 0.079), V(xi, WY0 + 0.002, Z0 + AH - 0.012), V(xi, -0.912, Z0 + AH - 0.012)]
    levha(y, q, 'kiremit', V(-sx * 0.4, 0, 1), 0.008)
    for yy in (-0.9, WY0 - 0.01):   # the porticoes' end walls
        kutu3(y, V((xa + xi) / 2, yy, Z0 + 0.04), X, Y, Z, abs(xi - xa), 0.012, 0.08, TAS)
for (xa_, xb_) in ((C.x - 0.38, C.x - 0.1), (C.x + 0.1, C.x + 0.35)):   # (the right piece stops at the side wall's inner face, so their tops do not overlap)
    alcak_duvar(y, [V(xa_, -0.92), V(xb_, -0.92)], Z0, AH, 0.03, TAS, 'kiremit')
for sx in (-1, 1):
    kutu_merkez(y, (C.x + sx * 0.1, -0.935), 0.045, 0.05, AH + 0.05, TAS, z0=Z0)
    kornis(y, C.x + sx * 0.1 - 0.0225, C.x + sx * 0.1 + 0.0225, -0.96, -0.91, Z0 + AH + 0.046, 0.012, 0.008, BANT, 'tac')
    kure(y, (C.x + sx * 0.1, -0.935, Z0 + AH + 0.075), 0.014, 'bronz', n=8, kat=4)
# the bronze pine cone on its basin
PCX, PCY = C.x, -0.82
donel(y, (PCX, PCY), [(0.07, Z0), (0.072, Z0 + 0.02), (0.06, Z0 + 0.024), (0.058, Z0 + 0.016), (0.0, Z0 + 0.016)], 'kirec', n=16)
y.yuz_yon([V(p.x, p.y, Z0 + 0.019) for p in cokgen((PCX, PCY), 0.058, 16)], 'su', Z)
y.prizma((PCX, PCY), 0.012, Z0 + 0.016, Z0 + 0.04, 'bronz', n=8)
donel(y, (PCX, PCY), [(0.0, Z0 + 0.04), (0.022, Z0 + 0.05), (0.026, Z0 + 0.07), (0.02, Z0 + 0.095), (0.01, Z0 + 0.11), (0.0, Z0 + 0.118)], 'bronz', n=12)
for k in range(5):
    for m in range(8):
        a = TAU * (m + 0.5 * (k % 2)) / 8
        zz = Z0 + 0.05 + 0.012 * k
        rr = [0.023, 0.026, 0.025, 0.021, 0.015][k]
        kure(y, (PCX + rr * math.cos(a), PCY + rr * math.sin(a), zz), 0.0055, 'bronz', n=4, kat=2)
# the processional way: paving
y.yuz_yon([V(C.x - 0.1, -0.98 + 0.001, Z0 + 0.002), V(C.x + 0.1, -0.98 + 0.001, Z0 + 0.002), V(C.x + 0.1, -0.88, Z0 + 0.002), V(C.x - 0.1, -0.88, Z0 + 0.002)], 'tas_acik', Z)
y.yuz_yon([V(C.x - 0.07, -0.76, Z0 + 0.002), V(C.x + 0.07, -0.76, Z0 + 0.002), V(C.x + 0.07, WY0 - 0.012, Z0 + 0.002), V(C.x - 0.07, WY0 - 0.012, Z0 + 0.002)], 'tas_acik', Z)

y.bolum('Kaplıca havuzu')
# Charlemagne's warm-spring pool: a stone pool with steps, a colonnade along the back under a lean-to roof, a bath hall
BX0, BX1, BY0, BY1 = -0.95, -0.6, 0.5, 0.8
havuz(y, BX0, BX1, BY0, BY1, Z0 + 0.02, derin=0.03, kenar=0.025, key='kirec')
kutu(y, V(BX0 - 0.025, BY0 - 0.025, Z0 - 0.002), X, BX1 - BX0 + 0.05, BY1 - BY0 + 0.05, 0.022, 'kirec', 'onarkasagsol')
kutu(y, V(BX0 - 0.03, BY1 + 0.11, Z0), X, BX1 - BX0 + 0.06, 0.022, 0.18, TAS, 'onarkasagsolust')
sutunlu_revak(y, V(BX1 + 0.01, BY1 + 0.05), V(BX0 - 0.01, BY1 + 0.05), 5, Z0, 0.11, 'osmanli', r=0.01, key=TAS)
levha(y, [V(BX0 - 0.035, BY1 + 0.025, Z0 + 0.15), V(BX1 + 0.035, BY1 + 0.025, Z0 + 0.15), V(BX1 + 0.035, BY1 + 0.11, Z0 + 0.172),
          V(BX0 - 0.035, BY1 + 0.11, Z0 + 0.172)], 'kiremit', V(0, -0.3, 1), 0.008)
for x_ in (BX0 - 0.025, BX1 + 0.025):
    kutu3(y, V(x_, BY1 + 0.08, Z0 + 0.075), X, Y, Z, 0.012, 0.06, 0.15, TAS)
# the bath hall at the side: an apsed block
hk = dikdortgen(BX0 - 0.06, BX0 + 0.06, BY0 - 0.2, BY0 + 0.02)
pencereli_duvar(y, hk, Z0, 0.18, [1, 1, 1, 2], renk=PEN, v0=0.06, en=0.4, ust=0.03, derin=0.016, sivri=0.0, cerceve=(0.006, KEM))
silme(y, hk, Z0 + 0.168, 0.012, 0.012, TAS, 'tac')
cati_besik(y, hk[0].x, hk[1].x, hk[0].y, hk[2].y, Z0 + 0.18, 0.08, 0.02, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=4, nr=4, uc_sacak=0.014)

y.bolum('Avlu: atlı heykel, ağaçlar, insanlar, atlılar')
# the bronze equestrian statue brought from Ravenna, on a tall pedestal in the court
HX, HY = 0.27, -0.45
kutu_merkez(y, (HX, HY), 0.11, 0.07, 0.025, 'kirec', z0=Z0)
kutu_merkez(y, (HX, HY), 0.09, 0.052, 0.09, 'mermer', z0=Z0 + 0.025)
kornis(y, HX - 0.045, HX + 0.045, HY - 0.026, HY + 0.026, Z0 + 0.11, 0.01, 0.008, 'kirec', 'tac')
at(y, HX - 0.004, HY, Z0 + 0.12, math.pi * 0.85, 0.85, 'bronz', 'bronz')
donel(y, (HX - 0.004, HY), [(0.008, Z0 + 0.12 + 0.056), (0.009, Z0 + 0.12 + 0.07), (0.006, Z0 + 0.12 + 0.09), (0.0, Z0 + 0.12 + 0.094)], 'bronz', n=8)
kure(y, (HX - 0.004, HY, Z0 + 0.12 + 0.1), 0.007, 'bronz', n=8, kat=4)
boru(y, [V(HX - 0.004, HY - 0.008, Z0 + 0.12 + 0.08), V(HX - 0.02, HY - 0.016, Z0 + 0.12 + 0.1)], 0.0025, 'bronz', n=4)
for (tx, ty, tb) in ((-0.95, 0.15, 0.2), (-0.95, -0.15, 0.17), (-0.15, 0.85, 0.2), (0.1, 0.88, 0.17), (0.3, 0.86, 0.18), (0.22, 0.55, 0.18),
                     (-0.08, 0.55, 0.16), (1.03, 0.85, 0.18), (1.03, 0.35, 0.17), (-0.95, -0.55, 0.16), (1.03, -0.85, 0.15), (0.05, -0.35, 0.15)):
    agac(y, tx, ty, Z0, boy=tb, tur='yaprakli', key='boya_yesil' if int(abs(tx * 10)) % 2 else 'zeytin')
for (tx, ty) in ((-0.95, 0.38), (-0.95, -0.38), (0.4, 0.3), (-0.5, 0.92), (-0.62, 0.92)):
    agac(y, tx, ty, Z0, boy=0.2, tur='servi', key='yesil_koyu')
for k, (x, yy, key, a) in enumerate(((C.x - 0.04, -0.72, 'boya_kirmizi', 1.5), (C.x + 0.05, -0.74, 'kobalt', 1.7), (0.2, -0.3, 'beyaz', 0.3),
                                     (0.25, -0.32, 'kumas', 2.8), (0.3, 0.2, 'boya_yesil', 3.5), (0.33, 0.24, 'ahsap_acik', 0.2),
                                     (C.x + 0.1, -0.9, 'boya_sari', 1.4), (-0.78, 0.44, 'beyaz', 1.0), (-0.7, 0.46, 'boya_kirmizi', 2.0))):
    insan(y, x, yy, Z0, key, aci=a, kol=0.5 if k == 2 else 0.0, sapka='altin' if key == 'kobalt' else None)
sovalye(y, 0.25, -0.75, Z0, math.radians(160), 0.95, 'kobalt', 'altin', mizrak=False, kosu=0.0, sorguc='altin', dokum=True)
sovalye(y, 0.4, -0.72, Z0, math.radians(165), 0.95, 'boya_kirmizi', 'beyaz', mizrak=False, kosu=0.0, dokum=True)

calistir(y, 'lm_aachen')
