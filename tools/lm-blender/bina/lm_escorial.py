# El Escorial (lm_escorial): Philip II's granite monastery-palace on its gridiron plan: the long west front with its
# rows of deep-set windows and the two-storey frontispiece, four corner towers with steep slate spires and iron
# needles, slate roofs with dormers over the ring of ranges and the inner wings, the Court of the Evangelists'
# arcades with its little temple, the Court of the Kings before the basilica's front (Doric half-columns, the six
# kings, the pediment) flanked by its two bell towers, the drummed dome with its lantern; the paved Lonja in front.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from ispanyol_ek import *

y = Yapi()
G, GK = 'granit_acik', 'granit'
REN = (G, GK, 'tas_acik', 'koyu')
ZB = 0.03
H = 0.24                                   # the ranges' wall height
ZT = ZB + H
CH = 0.075                                 # their roof's height
BX, BY = 1.08, 0.82
DW = 0.13
KAT = 4

# ================================================================ platform and the Lonja
y.bolum('Platform ve Lonja')
PX0, PX1, PY0, PY1 = -1.2, 1.2, -1.07, 0.95
kutu(y, V(PX0, PY0, 0), X, PX1 - PX0, PY1 - PY0, ZB, GK, 'onarkasagsol')
for (x0, x1, y0, y1) in ((PX0, PX1, PY0, -BY), (PX0, PX1, BY, PY1), (PX0, -BX, -BY, BY), (BX, PX1, -BY, BY)):   # (none under the ranges and courts)
    y.yuz_yon(dikdortgen(x0, x1, y0, y1, ZB), 'zemin', Z)
silme(y, dikdortgen(PX0, PX1, PY0, PY1), ZB - 0.008, 0.008, 0.006, GK, 'duz')
# the Lonja's low parapet with ball-topped posts, open in the middle (steps down)
for xa, xb in ((PX0 + 0.02, -0.16), (0.16, PX1 - 0.02)):
    a_, b_ = V(xa, PY0 + 0.02), V(xb, PY0 + 0.02)
    kutu(y, a_ + Z * ZB, X, xb - xa, 0.022, 0.03, G, 'onarkasagsolust')
    n = max(1, int(round((xb - xa) / 0.21)))
    for k in range(n + 1):
        p = a_.lerp(b_, k / n) + V(0, 0.011)
        kutu_merkez(y, (p.x, p.y), 0.03, 0.03, 0.045, G, z0=ZB)
        bilye(y, p.x, p.y, ZB + 0.045, 1.3)
merdiven(y, (0.0, PY0 - 0.06), math.pi / 2, 0.3, 0.0, ZB, n=3, key=GK)

# ================================================================ the ring of ranges
y.bolum('Dış kanatlar')
dis = dikdortgen(-BX, BX, -BY, BY)
ic = dikdortgen(-BX + DW, BX - DW, -BY + DW, BY - DW)
hh = H / KAT
PENC = (hh, 0.36, 0.64, hh * 0.2, hh * 0.72, False)
# the west front (-y) and the south side (-x) with deep-set windows; the far sides cheaper
cephe(y, dis[0], dis[1], ZB, [PENC] * KAT, 30, renk=REN, cerceve=None, atla_tum=(12, 13, 14, 15, 16, 17))
for i in (12, 13, 14, 15, 16, 17):
    duz_duvar(y, dis[0].lerp(dis[1], i / 30), dis[0].lerp(dis[1], (i + 1) / 30), ZB, ZT, G)
cephe(y, dis[3], dis[0], ZB, [PENC] * KAT, 23, renk=REN, cerceve=None)
ucuz_cephe(y, dis[1], dis[2], ZB, H, KAT, 23, G, ince=True)      # (east and north: never seen from the game's view)
ucuz_cephe(y, dis[2], dis[3], ZB, H, KAT, 30, G, ince=True)
silme(y, dis, ZB, 0.03, 0.01, GK, 'kaide')
for j in (1, 2, 3):   # (string courses only on the two fronts the game shows; their ends run into the corner towers)
    silme(y, [dis[3], dis[0], dis[1]], ZB + hh * j - 0.003, 0.006, 0.004, GK, 'duz', kapali=False)
silme(y, dis, ZT - 0.016, 0.016, 0.012, GK, 'tac')
# what stands inside the ring (the inner wings, the basilica): wall bays behind them are never seen
IW = 0.11
IX0, IX1, IY0, IY1 = ic[0].x, ic[1].x, ic[0].y, ic[2].y
KANATLAR = [(-0.415, -0.305, IY0 - 0.02, IY1 + 0.02, ('sol', 'sag')),          # A: monastery | basilica
            (0.305, 0.415, IY0 - 0.02, IY1 + 0.02, ('sol', 'sag')),            # B: basilica | college
            (IX0 - 0.02, -0.415, -0.055, 0.055, ('on', 'arka')),               # C: the Evangelists' court's back
            (-0.735, -0.625, 0.055, IY1 + 0.02, ('sol', 'sag')),               # D
            (0.415, IX1 + 0.02, -0.055, 0.055, ('on', 'arka')),                # E
            (0.625, 0.735, IY0 - 0.02, -0.055, ('sol', 'sag')),                # F (front)
            (0.625, 0.735, 0.055, IY1 + 0.02, ('sol', 'sag'))]                 # F (back)
ORTU = [(k[0], k[1], k[2], k[3]) for k in KANATLAR] + [(-0.29, 0.29, -0.28, 0.665)]


def avlu_cephe(a_, b_, satir, n):
    """a courtyard face: towards the game's camera (-x, -y) real recessed windows, the far-facing ones flat dark
    quads; bays standing against a wing or the basilica plain"""
    a2, b2, L_, e, nc = eksen(a_, b_)
    bos = []
    for i in range(n):
        m = a2.lerp(b2, (i + 0.5) / n) + nc * 0.03
        if any(x0 < m.x < x1 and y0 < m.y < y1 for x0, x1, y0, y1 in ORTU): bos.append(i)
    if nc.y < -0.7 or nc.x < -0.7:
        hh_ = H / satir
        cephe(y, a2, b2, ZB, [(hh_, 0.35, 0.65, hh_ * 0.22, hh_ * 0.72, False)] * satir, n, renk=REN, cerceve=None, atla_tum=bos)
        for i in bos:
            duz_duvar(y, a2.lerp(b2, i / n), a2.lerp(b2, (i + 1) / n), ZB, ZT, G)
    else:
        ucuz_cephe(y, a2, b2, ZB, H, satir, n, G, atla=bos, ince=True)


# the courtyard faces of the ring
icr = list(reversed(ic))
for i in range(4):
    a_, b_ = icr[i], icr[(i + 1) % 4]
    avlu_cephe(a_, b_, 3, max(3, int((b_ - a_).length / 0.075)))
silme(y, icr, ZT - 0.012, 0.012, 0.01, GK, 'tac')
y.bolum('Dış kanat çatıları')
halka_cati(y, dis, ic, ZT, CH, sacak=0.03, key='arduvaz', mahya='kursun', alt_key=GK)
# dormers on the slopes seen from the front and the south
for k in range(14):
    xx = -0.9 + k * (1.8 / 13)
    if abs(xx) < 0.22: continue
    cati_penceresi(y, xx, -BY + 0.029, ZT, (0, -1))
for k in range(10):
    yy_ = -0.64 + k * (1.28 / 9)
    cati_penceresi(y, -BX + 0.029, yy_, ZT, (-1, 0))
for (xx, yy_) in ((-0.6, -0.76), (0.6, -0.76), (-1.02, 0.3), (0.5, 0.76), (-0.5, 0.76), (1.02, -0.3)):   # chimneys
    kutu_merkez(y, (xx, yy_), 0.028, 0.028, 0.09, G, z0=ZT + 0.02)
    kutu_merkez(y, (xx, yy_), 0.036, 0.036, 0.008, GK, z0=ZT + 0.11)

# ================================================================ inner wings
y.bolum('İç kanatlar')


def kanat(x0, x1, y0, y1, yuzler, satir=3):
    """an inner range: windowed walls on the given sides ('on' -y, 'arka' +y, 'sol' -x, 'sag' +x), a slate gable roof"""
    k = dikdortgen(x0, x1, y0, y1)
    yon = {'on': (k[0], k[1]), 'sag': (k[1], k[2]), 'arka': (k[2], k[3]), 'sol': (k[3], k[0])}
    for ad, (a_, b_) in yon.items():
        if ad in yuzler:
            avlu_cephe(a_, b_, satir, max(2, int((b_ - a_).length / 0.09)))
    silme(y, k, ZT - 0.012, 0.012, 0.01, GK, 'tac')
    cati_besik(y, x0, x1, y0, y1, ZT, CH, 0.025, 'arduvaz', mahya='kursun', alt_key=GK, ucluk_key=G, ns=8, nr=4)


for k in KANATLAR:
    kanat(*k)
# court floors
for (x0, x1, y0, y1) in ((IX0, -0.415, IY0, -0.055), (IX0, -0.735, 0.055, IY1), (-0.625, -0.415, 0.055, IY1), (-0.305, 0.305, IY0, -0.28),
                         (0.415, 0.625, IY0, -0.055), (0.735, IX1, IY0, -0.055), (0.415, 0.625, 0.055, IY1), (0.735, IX1, 0.055, IY1)):
    y.yuz_yon(dikdortgen(x0, x1, y0, y1, ZB + 0.0006), 'zemin', Z)

# ================================================================ the Court of the Evangelists
y.bolum('Müjdeciler avlusu')
EX0, EX1, EY0, EY1 = IX0, -0.415, IY0, -0.055
ek = dikdortgen(EX0, EX1, EY0, EY1)
ekr = list(reversed(ek))
for i in range(4):
    a_, b_ = ekr[i], ekr[(i + 1) % 4]
    a_ = a_ + (b_ - a_).normalized() * 0.0
    n = max(3, int(round((b_ - a_).length / 0.12)))
    e_ = (b_ - a_).normalized(); nn = V(e_.y, -e_.x)
    a2, b2 = a_ + nn * 0.003, b_ + nn * 0.003
    if nn.x > 0.7 or nn.y > 0.7:   # (the two sides turned away from the game's camera: the arcades only drawn flat)
        ucuz_cephe(y, a2, b2, ZB, 0.16, 2, n, G, w=0.62, h=0.68, ince=True)
        silme(y, [a2, b2], ZB + 0.079, 0.006, 0.006, GK, 'duz', kapali=False)
        continue
    for zz, hk in ((ZB, 0.085), (ZB + 0.085, 0.075)):
        arkad(y, a2, b2, n, zz, hk, en=0.66, ust=0.014, sivri=0.0, derin=0.03, cerceve=(0.005, 'tas_acik') if zz == ZB else None, sutunlu=False, renk=REN)
        w_ = (b2 - a2).length / n
        hs = hk - 0.014 - 0.66 * w_ / 2
        for k in range(n):   # half-columns on the piers
            p = a2.lerp(b2, k / n) + nn * 0.008
            y.prizma((p.x, p.y), 0.0065, zz + 0.006, zz + hs, 'tas_acik', n=6, ust=False)
            kutu_merkez(y, (p.x, p.y), 0.018, 0.018, 0.006, 'tas_acik', z0=zz)
            kutu_merkez(y, (p.x, p.y), 0.018, 0.018, 0.006, 'tas_acik', z0=zz + hs)
        silme(y, [a2, b2], zz + hk - 0.006, 0.006, 0.006, GK, 'duz', kapali=False)
# the temple in the middle (templete): an octagon on steps, arches, a little dome; four pools round it
TCX, TCY = (EX0 + EX1) / 2, (EY0 + EY1) / 2
for k, rr in enumerate((0.085, 0.075)):
    y.prizma((TCX, TCY), rr, ZB + k * 0.008, ZB + (k + 1) * 0.008, G, n=8, kat=math.pi / 8)
ok_ = cokgen((TCX, TCY), 0.06, 8, math.pi / 8)
for i in range(8):
    y.kemerli(ok_[i], ok_[(i + 1) % 8], ZB + 0.016, 0.075, (G, GK, 'tas_acik', 'koyu'), v0=0.0, en=0.6, ust=0.012, derin=0.012, k_say=6)
halka_kornis(y, (TCX, TCY), 0.06, ZB + 0.088, 0.01, 0.008, 8, GK, kat=math.pi / 8, profil='tac')
y.kubbe((TCX, TCY), 0.058, ZB + 0.098, 0.05, 'arduvaz', n=16, kat=5)
y.yuz_yon(cokgen((TCX, TCY), 0.062, 8, math.pi / 8, ZB + 0.098), GK, Z)
igne(y, TCX, TCY, ZB + 0.146, 0.04)
for sx in (-1, 1):
    for sy in (-1, 1):
        hk = dikdortgen(TCX + sx * 0.14 - 0.055, TCX + sx * 0.14 + 0.055, TCY + sy * 0.15 - 0.045, TCY + sy * 0.15 + 0.045)
        hd = disa(hk, 0.012)
        duvarlar(y, hd, ZB, ZB + 0.024, G)                           # a raised stone basin: kerb, rim, inner sides, water
        for i in range(4):
            j = (i + 1) % 4
            y.yuz_yon([hd[i] + Z * (ZB + 0.024), hd[j] + Z * (ZB + 0.024), hk[j] + Z * (ZB + 0.024), hk[i] + Z * (ZB + 0.024)], 'tas_acik', Z)
            duz_duvar(y, hk[j], hk[i], ZB + 0.014, ZB + 0.024, G)
        y.yuz_yon([V(p.x, p.y, ZB + 0.014) for p in hk], 'su', Z)
        # box-hedge parterre on the basin's outer sides, a clipped cone at the corner
        hx, hy = TCX + sx * 0.215, TCY + sy * 0.15
        kutu_merkez(y, (hx, TCY + sy * 0.15), 0.014, 0.11, 0.02, 'yesil_koyu', z0=ZB)
        kutu_merkez(y, (TCX + sx * 0.14, TCY + sy * 0.215), 0.13, 0.014, 0.02, 'yesil_koyu', z0=ZB)
        donel(y, (hx, TCY + sy * 0.215), [(0.0, ZB), (0.012, ZB), (0.0, ZB + 0.05)], 'yesil_koyu', n=6)

# ================================================================ the basilica
y.bolum('Bazilika gövdesi')
BAX, BAY0, BAY1 = 0.29, -0.28, 0.665
ZBA = 0.44
bk = dikdortgen(-BAX, BAX, BAY0, BAY1)
# side and back walls (the lower parts stand inside the wings; the sides start behind the bell towers)
TW_ = 0.13
YT = BAY0 + TW_ - 0.012
for a_, b_ in ((V(BAX, YT), bk[2]), (bk[2], bk[3]), (bk[3], V(-BAX, YT))):
    ab, bb, L_, e, nc = eksen(a_, b_)
    n = max(2, int(L_ / 0.11))
    duz_duvar(y, a_, b_, ZB, ZT + 0.02, G)
    cephe(y, a_, b_, ZT + 0.02, [(ZBA - ZT - 0.02, 0.3, 0.7, 0.03, 0.12, False)], n, renk=REN, cerceve=None)
silme(y, bk, ZBA - 0.016, 0.018, 0.012, GK, 'tac')
y.yuz_yon(dikdortgen(-BAX, BAX, BAY0, BAY1, ZBA + 0.002), 'arduvaz', Z)
# the Greek cross over it: nave and transept arms with gable roofs, thermal windows in the gable ends
NW, CY_ = 0.13, 0.2
ZK = ZBA + 0.06
for (x0, x1, y0, y1) in ((-NW, NW, BAY0, BAY1), (-BAX, BAX, CY_ - NW, CY_ + NW)):
    kk = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, kk, ZBA + 0.002, ZK, G)
    silme(y, kk, ZK - 0.01, 0.01, 0.008, GK, 'tac')
    cati_besik(y, x0, x1, y0, y1, ZK, 0.085, 0.02, 'arduvaz', mahya='kursun', alt_key=GK, ucluk_key=G, ns=8, nr=4)
# thermal (half-round) windows in the gable ends
for (c, e, nn) in ((V(0, BAY1), X, Y), (V(BAX, CY_), Y, X), (V(-BAX, CY_), -Y, -X)):
    P = lambda t, r: c + e * (r * math.cos(t)) + nn * 0.002 + Z * (ZK + 0.004 + r * math.sin(t))
    for k in range(8):
        t0, t1 = math.pi * k / 8, math.pi * (k + 1) / 8
        y.yuz_yon([P(t0, 0), P(t0, 0.05), P(t1, 0.05)], 'koyu', nn)
        y.yuz_yon([P(t0, 0.05), P(t0, 0.058), P(t1, 0.058), P(t1, 0.05)], 'tas_acik', nn)
    for t in (math.pi / 3, 2 * math.pi / 3):
        y.yuz_yon([P(t, 0) + e * 0.002, P(t, 0) - e * 0.002, P(t, 0.05) - e * 0.002 + nn * 0.0005, P(t, 0.05) + e * 0.002 + nn * 0.0005], 'tas_acik', nn)

y.bolum('Kubbe')
CQ = 0.155
kk = dikdortgen(-CQ, CQ, CY_ - CQ, CY_ + CQ)
ZQ = 0.66
duvarlar(y, kk, ZK - 0.01, ZQ, G, ust=GK)
for i in range(4):
    a_, b_ = kk[i], kk[(i + 1) % 4]
    ab, bb, L_, e, nc = eksen(a_, b_)
    for k in range(3):
        pencere_k(y, a_, b_, L_ * (k + 0.5) / 3 - 0.012, ZQ - 0.055, 0.024, 0.032, 'koyu')
silme(y, kk, ZQ - 0.02, 0.02, 0.012, GK, 'tac')
for p in disa(kk, 0.004):
    bilye(y, p.x, p.y, ZQ, 1.5)
zt = kubbe_kasnakli(y, (0, CY_), 0.128, ZQ, 0.16, n_pencere=12, kubbe_h=0.145, key='arduvaz', duvar=REN, payanda=True, alem_olcek=0,
                    sivri=0.0, n=32, kat=10, en=0.45, cerceve=(0.004, 'tas_acik'))
# stone ribs down the dome from the lantern's foot to the drum's cornice
zd0 = ZQ + 0.16 + 0.016
for k in range(8):
    a = TAU * k / 8 + TAU / 16
    pts = [V(0.137 * math.cos(ph) * math.cos(a), CY_ + 0.137 * math.cos(ph) * math.sin(a), zd0 + 0.149 * math.sin(ph))
           for ph in [math.pi / 2 * j / 7 * 0.86 for j in range(8)]]
    boru(y, pts, 0.0055, G, n=4)
# the lantern: a small windowed drum, a little dome, the needle
y.prizma((0, CY_), 0.034, zt - 0.012, zt + 0.05, G, n=12, ust=False)
for k in range(6):
    a = TAU * k / 6
    d = V(math.cos(a), math.sin(a))
    yarik(y, V(0, CY_) + d * 0.033, V(-d.y, d.x), d, -0.005, zt + 0.01, 0.01, 0.028, 'koyu')
halka_kornis(y, (0, CY_), 0.034, zt + 0.046, 0.008, 0.007, 12, GK, profil='tac')
t2 = y.kubbe((0, CY_), 0.036, zt + 0.054, 0.03, 'arduvaz', n=12, kat=4)
igne(y, 0, CY_, t2.z - 0.002, 0.08)

y.bolum('Bazilika cephesi')
FY = BAY0
TW_ = 0.13
FX = BAX - TW_                                   # the front between the towers: -FX..FX
fa, fb = V(-FX, FY), V(FX, FY)
for k in range(3):   # three arched doors in the lower storey
    p, q = fa.lerp(fb, k / 3), fa.lerp(fb, (k + 1) / 3)
    y.kemerli(p, q, ZB, 0.15, (G, GK, 'tas_acik', 'koyu' if k != 1 else 'ahsap_koyu'), v0=0.0, en=0.5, ust=0.02, derin=0.025, k_say=8, cerceve=(0.006, 'tas_acik'))
    cephe(y, p, q, ZB + 0.15, [(ZBA - ZB - 0.15, 0.36, 0.64, 0.03, 0.12, False)], 1, renk=REN, cerceve=(0.005, 'tas_acik'))
# six giant Doric half-columns, the entablature, the six kings on pedestals
for k in range(6):
    xx = -FX + 0.01 + (2 * FX - 0.02) * k / 5
    sade_sutun(y, xx, FY - 0.012, ZB, ZBA - 0.07, 0.011, G, n=10)
    kutu_merkez(y, (xx, FY - 0.016), 0.024, 0.024, 0.02, G, z0=ZBA - 0.032)
    figur_x, figur_y = xx, FY - 0.016
    donel(y, (figur_x, figur_y), [(0.008, ZBA - 0.012), (0.009, ZBA + 0.008), (0.006, ZBA + 0.03), (0.0055, ZBA + 0.036), (0.0, ZBA + 0.037)], 'tas_acik', n=8)
    kure(y, (figur_x, figur_y, ZBA + 0.042), 0.0055, 'tas_acik', n=7, kat=4)
    kure(y, (figur_x, figur_y, ZBA + 0.047), 0.0035, 'altin', n=6, kat=3)
kutu3(y, V(0, FY - 0.012, ZBA - 0.051), X, Y, Z, 2 * FX + 0.02, 0.026, 0.038, G, ('+x', '-x', '-y', '+z', '-z'))
silme(y, [V(-FX - 0.01, FY - 0.025), V(FX + 0.01, FY - 0.025)], ZBA - 0.036, 0.006, 0.006, GK, 'duz', kapali=False)
kapali_alinlik(y, V(-NW - 0.012, FY - 0.006), V(NW + 0.012, FY - 0.006), ZK, 0.085, 0.012, key=G, ic_key=GK, c=0.007)
y.oculus(V(0, FY - 0.007, ZK + 0.03), X, -Y, 0.014, 'koyu', 'tas_acik', f=0.004)
bilye(y, 0, FY - 0.004, ZK + 0.078, 1.2)

y.bolum('Çan kuleleri')
for sx in (-1, 1):
    tx, ty = sx * (BAX - TW_ / 2), FY + TW_ / 2 - 0.012
    tk = dikdortgen(tx - TW_ / 2, tx + TW_ / 2, ty - TW_ / 2, ty + TW_ / 2)
    for i in range(4):
        a_, b_ = tk[i], tk[(i + 1) % 4]
        nc_ = V((b_ - a_).y, -(b_ - a_).x).normalized()
        if nc_.x > 0.7 or nc_.y > 0.7:   # (turned away from the game's camera: flat window quads)
            ucuz_cephe(y, a_, b_, ZB, 0.47, 4, 1, G, w=0.28, h=0.55, ince=True)
        else:
            cephe(y, a_, b_, ZB, [(0.12, 0.36, 0.64, 0.03, 0.09, False), (0.12, 0.36, 0.64, 0.03, 0.09, False), (0.12, 0.36, 0.64, 0.03, 0.09, False),
                                  (0.11, 0.36, 0.64, 0.025, 0.085, False)], 1, renk=REN, cerceve=(0.004, 'tas_acik'))
        y.kemerli(a_, b_, ZB + 0.47, 0.11, (G, GK, 'tas_acik', 'koyu'), v0=0.0, en=0.5, ust=0.02, derin=0.025, k_say=8, korkuluk=0.025,
                  cerceve=(0.005, 'tas_acik'))
    silme(y, tk, ZB, 0.02, 0.008, GK, 'kaide')
    for zz in (ZB + 0.12, ZB + 0.24, ZB + 0.36):
        silme(y, tk, zz - 0.003, 0.006, 0.004, GK, 'duz')
    silme(y, tk, ZB + 0.465, 0.01, 0.008, GK, 'duz')
    ztt = ZB + 0.58
    silme(y, tk, ztt - 0.014, 0.016, 0.012, GK, 'tac')
    y.yuz_yon([V(p.x, p.y, ztt + 0.002) for p in tk], G, Z)
    for p in disa(tk, 0.002):
        bilye(y, p.x, p.y, ztt + 0.002, 1.2)
    # an octagonal lantern, a little slate dome and a tall spire with the needle
    ok2 = cokgen((tx, ty), 0.04, 8, math.pi / 8)
    duvarlar(y, ok2, ztt + 0.002, ztt + 0.06, G)
    for i in range(0, 8, 2):
        a_, b_ = ok2[i], ok2[(i + 1) % 8]
        pencere_k(y, a_, b_, (b_ - a_).length / 2 - 0.007, ztt + 0.015, 0.014, 0.03, 'koyu')
    halka_kornis(y, (tx, ty), 0.04, ztt + 0.054, 0.008, 0.008, 8, GK, kat=math.pi / 8, profil='tac')
    y.yuz_yon(cokgen((tx, ty), 0.048, 8, math.pi / 8, ztt + 0.062), GK, Z)
    donel(y, (tx, ty), [(0.042, ztt + 0.062), (0.04, ztt + 0.08), (0.026, ztt + 0.1), (0.012, ztt + 0.13), (0.006, ztt + 0.16), (0.0, ztt + 0.162)], 'arduvaz', n=8,
          kat=math.pi / 8)
    igne(y, tx, ty, ztt + 0.158, 0.06)

# ================================================================ the west frontispiece
y.bolum('Ana giriş')
FW, FD = 0.36, 0.028
fy = -BY - FD
fk = dikdortgen(-FW / 2, FW / 2, fy, -BY)
ZF1, ZF2, ZF3 = ZB + 0.16, ZB + 0.3, ZB + 0.38
# the projecting block: sides, its lower storey's door and niches, the upper storey's niche
for i in (1, 3):
    duz_duvar(y, fk[i], fk[(i + 1) % 4], ZB, ZF3, G)
duz_duvar(y, fk[2], fk[3], ZT - 0.01, ZF3, G)                     # (its back above the roof)
fa, fb = fk[0], fk[1]
for k in range(5):
    p, q = fa.lerp(fb, k / 5), fa.lerp(fb, (k + 1) / 5)
    if k == 2:
        y.kemerli(p, q, ZB, ZF1 - ZB, (G, GK, 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.68, ust=0.018, derin=0.03, k_say=10, cerceve=(0.007, 'tas_acik'))
    elif k in (1, 3):
        y.kemerli(p, q, ZB, ZF1 - ZB, (G, GK, 'tas_acik', GK), v0=0.03, en=0.5, ust=0.03, derin=0.014, k_say=8)
    else:
        cephe(y, p, q, ZB, [(ZF1 - ZB, 0.34, 0.66, 0.05, 0.1, True)], 1, renk=REN, cerceve=(0.004, 'tas_acik'))
    if k == 2:
        y.kemerli(p, q, ZF1, ZF2 - ZF1, (G, GK, 'tas_acik', GK), v0=0.02, en=0.55, ust=0.02, derin=0.02, k_say=8, cerceve=(0.005, 'tas_acik'))
    else:
        cephe(y, p, q, ZF1, [(ZF2 - ZF1, 0.34, 0.66, 0.04, 0.1, False)], 1, renk=REN, cerceve=(0.004, 'tas_acik'))
duz_duvar(y, fa, fb, ZF2, ZF3, G)
# St Lawrence in the upper niche, the gridiron below him
kutu_merkez(y, (0, fy + 0.012), 0.026, 0.012, 0.012, 'tas_acik', z0=ZF1 + 0.02)
donel(y, (0, fy + 0.012), [(0.009, ZF1 + 0.032), (0.01, ZF1 + 0.06), (0.007, ZF1 + 0.085), (0.0, ZF1 + 0.087)], 'tas_acik', n=8)
kure(y, (0, fy + 0.012, ZF1 + 0.093), 0.0065, 'tas_acik', n=7, kat=4)
for k in range(4):
    cubuk(y, V(-0.012 + 0.008 * k, fy - 0.002, ZF1 + 0.004), V(-0.012 + 0.008 * k, fy - 0.002, ZF1 + 0.016), 0.002, 'demir')
# columns: Doric below, Ionic above, the entablatures, the pediment and the balls
for k in range(6):
    if k in (0, 5): xx = -FW / 2 + 0.012 if k == 0 else FW / 2 - 0.012
    else: xx = -FW / 2 + FW * k / 5
    sade_sutun(y, xx, fy - 0.012, ZB, ZF1 - 0.016, 0.009, G)
    sade_sutun(y, xx, fy - 0.01, ZF1 + 0.004, ZF2 - 0.014, 0.0075, G)
for zz, hh_ in ((ZF1 - 0.016, 0.02), (ZF2 - 0.014, 0.018)):
    kutu3(y, V(0, fy - 0.011, zz + hh_ / 2), X, Y, Z, FW + 0.02, 0.022, hh_, G, ('+x', '-x', '-y', '+z', '-z'))
y.yuz_yon(dikdortgen(-FW / 2, FW / 2, fy, -BY, ZF3), G, Z)
silme(y, fk, ZF3 - 0.012, 0.012, 0.008, GK, 'tac')
kapali_alinlik(y, V(-FW * 0.32, fy - 0.004), V(FW * 0.32, fy - 0.004), ZF3, 0.06, FD - 0.004, key=G, ic_key=GK, c=0.007)
for xx in (-FW / 2 + 0.012, -FW * 0.32, FW * 0.32, FW / 2 - 0.012):
    bilye(y, xx, fy + 0.002, ZF3, 1.5)
sancak(y, 0, fy + 0.004, ZF3 + 0.056, boy=0.2, en=0.13, yuk=0.08, aci=-math.pi * 0.8)

# ================================================================ the corner towers
y.bolum('Köşe kuleleri')
for cx_, cy_ in ((-BX, -BY), (BX, -BY), (BX, BY), (-BX, BY)):
    herrera_kule(y, cx_, cy_, 0.19, ZB, 0.38, 5, 0.29, girintili=(cy_ < 0 or cx_ < 0), igne_boy=0.09, gizli_ince=True)   # (steep slate chapiteles)


calistir(y, 'lm_escorial')
