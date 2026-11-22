# Kürk Ticaret Evi (lm_kurkpazari): a northern Russian fur merchant's yard in winter. A two-storey log house (izba) with
# carved white window frames (nalichniki), painted shutters, carved barge boards and a horse-head ridge, a shop counter
# with an awning on the street gable and a covered stair porch (kryltso); a log chapel with an octagon, a tall shingled
# tent and a scaled aspen onion (the silhouette); a log stable with horses and hay, a sweep well, stacks of sable, fox,
# ermine and squirrel pelts on trestles and a drying rack, loaded sledges, a rail fence with a roofed gate, firewood,
# snowy spruces, and snow lying on the roofs and the yard.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from rus_ortak import *
from frank_ortak import _ss
from bina_ortak import calistir
import doku

y = Yapi()
Z0 = 0.04
GX0, GX1, GY0, GY1 = -1.1, 1.1, -1.05, 1.05
RK = 'kobalt'                                    # shutters / accents (a dark blue kept off team blue)


def yol_mesafe(x, yy):
    """distance to the trampled tracks: gate -> yard -> house, -> stable, -> chapel"""
    yollar = [((0.0, -1.05), (0.0, -0.4)), ((0.0, -0.4), (0.16, -0.12)), ((0.0, -0.4), (0.6, -0.3)), ((0.0, -0.4), (-0.55, 0.15)),
              ((0.0, -0.4), (0.45, -0.6))]
    d = 9.0
    for (ax, ay), (bx, by) in yollar:
        vx, vy = bx - ax, by - ay
        t = max(0.0, min(1.0, ((x - ax) * vx + (yy - ay) * vy) / (vx * vx + vy * vy)))
        d = min(d, math.hypot(x - ax - vx * t, yy - ay - vy * t))
    return d


def kar_renk(x, yy, z):
    """snow over the yard: soft drifts, grass showing through in places, trodden tracks to the buildings"""
    n1 = math.sin(x * 5.1 + 0.7) * math.cos(yy * 4.3 - 1.2)
    n2 = math.sin(x * 11.3 - yy * 8.1 + 2.0) * 0.5 + math.sin(x * 17.0 + yy * 13.0) * 0.25
    kar = (0.88, 0.9, 0.93)
    ot = (0.42, 0.44, 0.31)
    t = _ss(0.45, 0.95, n1 * 0.8 + n2 * 0.4)               # bare patches
    c = tuple(p + (q - p) * t * 0.75 for p, q in zip(kar, ot))
    yt = 1 - _ss(0.05, 0.14, yol_mesafe(x, yy) + 0.025 * n2)   # tracks: trodden grey-brown snow
    c = tuple(p + (q - p) * yt * 0.9 for p, q in zip(c, (0.4, 0.34, 0.27)))
    m = 0.97 + 0.03 * n2                                      # a faint undulation
    return tuple(min(1.0, v * m) for v in c)


doku.KOSE_RENK['toprak_ot'] = kar_renk

# ---------------------------------------------------------------- ground
y.bolum('Karlı zemin')
NX, NY = 56, 52   # (fine enough that the trodden tracks keep their edges in the vertex colours)
P = [[V(GX0 + (GX1 - GX0) * i / NX, GY0 + (GY1 - GY0) * j / NY, Z0) for j in range(NY + 1)] for i in range(NX + 1)]
for i in range(NX):
    for j in range(NY):
        if (i + j) % 2 == 0:
            y.yuz([P[i][j], P[i + 1][j], P[i + 1][j + 1]], 'toprak_ot'); y.yuz([P[i][j], P[i + 1][j + 1], P[i][j + 1]], 'toprak_ot')
        else:
            y.yuz([P[i][j], P[i + 1][j], P[i][j + 1]], 'toprak_ot'); y.yuz([P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]], 'toprak_ot')
duz_duvar(y, V(GX0, GY0), V(GX1, GY0), 0, Z0, 'toprak')
duz_duvar(y, V(GX1, GY0), V(GX1, GY1), 0, Z0, 'toprak')
duz_duvar(y, V(GX1, GY1), V(GX0, GY1), 0, Z0, 'toprak')
duz_duvar(y, V(GX0, GY1), V(GX0, GY0), 0, Z0, 'toprak')

# ---------------------------------------------------------------- the merchant's house
y.bolum('Tüccar evi: kütük duvarlar')
HX0, HX1, HY0, HY1 = -0.1, 0.42, -0.06, 0.62
HC = V((HX0 + HX1) / 2, (HY0 + HY1) / 2)
RL = 0.0125
# a stone footing, then the log walls
duvarlar(y, dikdortgen(HX0 - 0.012, HX1 + 0.012, HY0 - 0.012, HY1 + 0.012), Z0 - 0.01, Z0 + 0.03, 'granit')
y.yuz_yon([V(p.x, p.y, Z0 + 0.03) for p in dikdortgen(HX0 - 0.012, HX1 + 0.012, HY0 - 0.012, HY1 + 0.012)], 'granit', Z)
ZW = kutuk_kutu(y, HX0, HX1, HY0, HY1, Z0 + 0.03, 0.38, RL, 'kutuk')
# a carved board between the storeys
for a, b in ((V(HX0, HY0), V(HX1, HY0)), (V(HX0, HY1), V(HX0, HY0))):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    kutu3(y, (a + b) / 2 + nn * 0.016 + Z * (Z0 + 0.215), e, nn, Z, (b - a).length - 0.01, 0.012, 0.02, 'ahsap_koyu', ('+x', '-x', '+y', '+z', '-z'))
    oymali_sacak(y, a + nn * 0.016 + Z * (Z0 + 0.205), b + nn * 0.016 + Z * (Z0 + 0.205), nn, 'beyaz', 0.016, int((b - a).length / 0.035), 0.007)

y.bolum('Tüccar evi: pencereler')
OF = RL * 0.85   # the logs' front
# street gable (-y): three upper windows; the left side (-x): four upper and three lower
for u in (-0.16, 0.0, 0.16):
    nalichnik(y, V(HC.x + u, HY0 - OF, Z0 + 0.255), X, 0.05, 0.075, 'beyaz', 'koyu', RK, 'ucgen')
for yy in (0.07, 0.22, 0.38, 0.52):
    nalichnik(y, V(HX0 - OF, yy, Z0 + 0.255), -Y, 0.05, 0.075, 'beyaz', 'koyu', RK, 'kemer' if yy in (0.22, 0.38) else 'ucgen')
for yy in (0.52,):
    nalichnik(y, V(HX0 - OF, yy, Z0 + 0.08), -Y, 0.04, 0.05, 'beyaz', 'koyu', None, None)
# the right and back sides: plain small windows
for yy in (0.1, 0.3, 0.5):
    nalichnik(y, V(HX1 + OF, yy, Z0 + 0.255), Y, 0.045, 0.07, 'beyaz', 'koyu', None, 'ucgen')
for yy in (0.18, 0.42):
    nalichnik(y, V(HX1 + OF, yy, Z0 + 0.08), Y, 0.04, 0.05, 'beyaz', 'koyu', None, None)
# the yard (back) gable: two upper windows with shutters, a small one below
for u in (-0.1, 0.1):
    nalichnik(y, V(HC.x + u, HY1 + OF, Z0 + 0.255), -X, 0.05, 0.075, 'beyaz', 'koyu', RK, 'ucgen')
nalichnik(y, V(HC.x, HY1 + OF, Z0 + 0.08), -X, 0.04, 0.05, 'beyaz', 'koyu', None, None)

y.bolum('Tüccar evi: dükkân tezgâhı')
# the shop: a wide hatch in the street gable, a counter on brackets with pelts, an awning above
SH0, SH1 = HC.x - 0.2, HC.x + 0.2
kutu3(y, V(HC.x, HY0 - OF + 0.004, Z0 + 0.12), X, -Y, Z, 0.34, 0.01, 0.1, 'koyu', ('+x', '-x', '+y', '+z', '-z'))
for u in (-0.17, 0.17):
    kutu3(y, V(HC.x + u, HY0 - OF - 0.002, Z0 + 0.12), X, -Y, Z, 0.016, 0.012, 0.12, 'ahsap_koyu')
kutu3(y, V(HC.x, HY0 - OF - 0.03, Z0 + 0.07), X, -Y, Z, 0.36, 0.06, 0.012, 'ahsap')
for u in (-0.15, 0.0, 0.15):
    cubuk(y, V(HC.x + u, HY0 - OF - 0.002, Z0 + 0.03), V(HC.x + u, HY0 - OF - 0.05, Z0 + 0.064), 0.008, 'ahsap_koyu')
# the awning: a short lean-to on brackets, snow on it
ay0, ay1 = HY0 - OF - 0.08, HY0 - OF
za0, za1 = Z0 + 0.17, Z0 + 0.205
for xx in (SH0, SH1):
    cubuk(y, V(xx, ay1, Z0 + 0.16), V(xx, ay0 + 0.01, za0 - 0.004), 0.008, 'ahsap_koyu')
q = [V(SH0 - 0.02, ay0, za0), V(SH1 + 0.02, ay0, za0), V(SH1 + 0.02, ay1, za1), V(SH0 - 0.02, ay1, za1)]
y.yuz_yon(q, 'sindira', Z)
y.yuz_yon([p - Z * 0.008 for p in q], 'ahsap_koyu', -Z)
for k, (i0, i1) in enumerate(((0, 1), (1, 2), (3, 0))):
    pa, pb = q[i0], q[i1]
    y.yuz_yon([pa, pb, pb - Z * 0.008, pa - Z * 0.008], 'ahsap_koyu', (pa + pb) / 2 - (q[0] + q[2]) / 2)
oymali_sacak(y, q[0] - Z * 0.008, q[1] - Z * 0.008, -Y, 'beyaz', 0.014, 10, 0.001)
qs = [V(SH0, ay0 + 0.004, za0 + 0.006), V(SH1, ay0 + 0.004, za0 + 0.006), V(SH1, ay1, za1 + 0.006), V(SH0, ay1, za1 + 0.006)]
y.yuz_yon(qs, 'beyaz', Z)
y.yuz_yon([qs[0], qs[1], qs[1] - Z * 0.007, qs[0] - Z * 0.007], 'beyaz', -Y)
for i0, i1, yon in ((1, 2, X), (3, 0, -X)):
    y.yuz_yon([qs[i0], qs[i1], qs[i1] - Z * 0.007, qs[i0] - Z * 0.007], 'beyaz', yon)

y.bolum('Tüccar evi: çatı, kar, baca')
RH = 0.3
zr = ahsap_cati(y, HX0 - RL, HX1 + RL, HY0 - RL, HY1 + RL, ZW, RH, sacak=0.035, uc_sacak=0.04, nr=10, ns=8)
kar_besik(y, HX0 - RL, HX1 + RL, HY0 - RL, HY1 + RL, ZW, RH, sacak=0.035, uc_sacak=0.04, kapsam=0.62, tohum=3, n=12)
# the attic window (svetyolka) in the street gable with its own carved frame
nalichnik(y, V(HC.x, HY0 - RL - 0.042, ZW + 0.07), X, 0.05, 0.07, 'beyaz', 'koyu', None, 'kemer', t=0.006)
nalichnik(y, V(HC.x, HY1 + RL + 0.042, ZW + 0.07), -X, 0.045, 0.065, 'beyaz', 'koyu', None, 'ucgen', t=0.006)
# brick chimney through the right slope with a smoke plume
CXc, CYc = HX1 - 0.09, HC.y + 0.1
zc = ZW + RH * (1 - (CXc - HC.x) / ((HX1 - HX0) / 2 + RL + 0.035)) - 0.02
kutu_merkez(y, (CXc, CYc), 0.05, 0.05, zr - zc + 0.06, 'tugla', z0=zc)
kutu_merkez(y, (CXc, CYc), 0.062, 0.062, 0.014, 'tugla_koyu', z0=zr + 0.046)
y.yuz_yon([V(p.x, p.y, zr + 0.0605) for p in dikdortgen(CXc - 0.019, CXc + 0.019, CYc - 0.019, CYc + 0.019)], 'koyu', Z)
y.yuz_yon([V(p.x, p.y, zr + 0.06) for p in dikdortgen(CXc - 0.031, CXc + 0.031, CYc - 0.031, CYc + 0.031)], 'beyaz', Z)
for k, (dx, dy, dz, r) in enumerate(((0.0, 0.0, 0.02, 0.014), (0.012, 0.006, 0.045, 0.018), (0.03, -0.004, 0.07, 0.022), (0.026, 0.014, 0.09, 0.016),
                                    (0.055, 0.004, 0.1, 0.026), (0.085, 0.012, 0.125, 0.024), (0.07, -0.01, 0.13, 0.018), (0.115, 0.004, 0.15, 0.022))):
    kure(y, (CXc + dx, CYc + dy, zr + 0.06 + dz), r, 'duman', n=8, kat=4)

y.bolum('Tüccar evi: merdivenli sundurma (kryltso)')
# a covered stair up the left side to the upper door
SXc = HX0 - RL - 0.06
ZL = Z0 + 0.205
merdiven(y, (SXc, 0.0), math.pi / 2, 0.075, Z0, ZL, n=8, d=0.036, key='ahsap', yanlik='ahsap_koyu')
LY0, LY1 = 0.288, 0.42
kutu(y, V(SXc - 0.06, LY0, ZL - 0.016), X, 0.12, LY1 - LY0, 0.016, 'ahsap', 'onarkasagsolust')
for xx in (SXc - 0.055, SXc + 0.035):
    for yy in (LY0 + 0.005, LY1 - 0.005):
        y.prizma((xx, yy), 0.007, Z0, ZL + 0.16, 'ahsap_koyu', n=6, ust=False)
# rails round the landing, a door behind with a carved frame
for (a, b) in ((V(SXc - 0.055, LY1 - 0.005), V(SXc - 0.055, LY0 + 0.005)), (V(SXc - 0.055, LY1 - 0.005), V(SXc + 0.035, LY1 - 0.005))):
    cubuk(y, a + Z * (ZL + 0.06), b + Z * (ZL + 0.06), 0.008, 'ahsap_koyu')
    for t in (0.25, 0.5, 0.75):
        p = a.lerp(b, t)
        cubuk(y, p + Z * ZL, p + Z * (ZL + 0.06), 0.006, 'beyaz')
kutu3(y, V(HX0 - OF + 0.004, 0.355, ZL + 0.06), -Y, -X, Z, 0.06, 0.01, 0.12, 'ahsap_dikey', ('+x', '-x', '+y', '+z'))
nalichnik(y, V(HX0 - OF, 0.355, ZL), -Y, 0.06, 0.115, 'beyaz', 'ahsap_dikey', None, 'kemer')
# its little hipped roof with an onion finial
zk = cati_kirma(y, SXc - 0.06, SXc + 0.04, LY0, LY1, ZL + 0.16, 0.08, 0.025, 'sindira', 'ahsap_koyu', kalinlik=0.008, ns=4, nr=3,
                dilim=['sindira', 'sindira2'])
kubbe(y, (SXc - 0.01, (LY0 + LY1) / 2), 0.018, zk - 0.004, 'sogan', 0.04, 'ahsap_acik', n=10, alt=1)
y.prizma((SXc - 0.01, (LY0 + LY1) / 2), 0.0025, zk + 0.03, zk + 0.06, 'ahsap_koyu', n=4)

# ---------------------------------------------------------------- the chapel
y.bolum('Şapel: kütük gövde')
CC = V(-0.6, 0.45)
CW = 0.13
ZC = kutuk_kutu(y, CC.x - CW, CC.x + CW, CC.y - CW, CC.y + CW, Z0, 0.26, 0.012, 'kutuk')
nalichnik(y, V(CC.x - CW - 0.011, CC.y, Z0 + 0.13), -Y, 0.04, 0.06, 'beyaz', 'koyu', None, 'ucgen')
nalichnik(y, V(CC.x + 0.06, CC.y - CW - 0.011, Z0 + 0.13), X, 0.04, 0.06, 'beyaz', 'koyu', None, 'ucgen')
# the porch (trapeza) on its front with a gable roof and a door
PY0 = CC.y - CW - 0.16
kutuk_kutu(y, CC.x - 0.085, CC.x + 0.085, PY0, CC.y - CW + 0.01, Z0, 0.17, 0.011, 'kutuk')
kutu3(y, V(CC.x, PY0 - 0.006, Z0 + 0.06), X, -Y, Z, 0.06, 0.008, 0.12, 'ahsap_dikey', ('+x', '-x', '+y', '+z'))
nalichnik(y, V(CC.x, PY0 - 0.01, Z0), X, 0.064, 0.11, 'beyaz', 'ahsap_dikey', None, 'kemer')
ahsap_cati(y, CC.x - 0.096, CC.x + 0.096, PY0 - 0.011, CC.y - CW + 0.01, Z0 + 0.182, 0.13, sacak=0.025, uc_sacak=0.03, nr=6, ns=5, konek=False)
kar_besik(y, CC.x - 0.096, CC.x + 0.096, PY0 - 0.011, CC.y - CW + 0.01, Z0 + 0.182, 0.13, sacak=0.025, uc_sacak=0.03, kapsam=0.5, tohum=7, n=6)

y.bolum('Şapel: sekizgen, çadır çatı, soğan kubbe')
# the low hipped skirt over the cell, then the octagon (vosmerik) on it
sac = 0.035
rs = (sac + 0.03) / (CW + 0.012 + sac)
zsk = cati_kirma(y, CC.x - CW - 0.012, CC.x + CW + 0.012, CC.y - CW - 0.012, CC.y + CW + 0.012, ZC, 0.06 / rs, sac, 'sindira', 'ahsap_koyu',
                 kalinlik=0.01, r_ust=1 - 0.098 / (CW + 0.012 + sac), nr=4, ns=8, dilim=['sindira', 'sindira2'])
y.yuz_yon([V(p.x, p.y, zsk - 0.001) for p in dikdortgen(CC.x - 0.1, CC.x + 0.1, CC.y - 0.1, CC.y + 0.1)], 'sindira2', Z)   # (the ring's top)
R8 = 0.1
oct8 = cokgen(CC, R8, 8, math.pi / 8)
zo = zsk - 0.004
for i in range(8):
    kutuk_duvar2(y, oct8[i], oct8[(i + 1) % 8], zo + (0.011 if i % 2 else 0), zo + 0.16 + (0.011 if i % 2 else 0), 0.011, 'kutuk', uzanti=0.012, ic=False)
zo2 = zo + 0.172
for i in (5, 6):   # windows on the seen faces
    a, b = oct8[i], oct8[(i + 1) % 8]
    e = (b - a).normalized()
    nalichnik(y, (a + b) / 2 + V(e.y, -e.x) * 0.009 + Z * (zo + 0.06), e, 0.032, 0.05, 'beyaz', 'koyu', None, 'ucgen', t=0.005)
# a flared eave ring (politsa) and the tall tent
silme(y, cokgen(CC, R8 + 0.006, 8, math.pi / 8), zo2 - 0.012, 0.014, 0.022, 'ahsap_koyu', 'kaba')
TH = 0.4
ring = cokgen(CC, R8 + 0.03, 8, math.pi / 8)
tp = V(CC.x, CC.y, zo2 + TH)
mid = cokgen(CC, (R8 + 0.03) * 0.72, 8, math.pi / 8)
zm = zo2 + 0.05
for i in range(8):
    j = (i + 1) % 8
    out = (ring[i] + ring[j]) / 2 - V(CC.x, CC.y)
    y.yuz_yon([ring[i] + Z * zo2, ring[j] + Z * zo2, mid[j] + Z * zm, mid[i] + Z * zm], 'sindira', out + Z * 0.5)
    # the tent in shingle courses
    for k in range(6):
        t0, t1 = k / 6, (k + 1) / 6
        A_, B_ = mid[i].lerp(V(CC.x, CC.y), t0 * 0.86), mid[j].lerp(V(CC.x, CC.y), t0 * 0.86)
        C_, D_ = mid[j].lerp(V(CC.x, CC.y), t1 * 0.86), mid[i].lerp(V(CC.x, CC.y), t1 * 0.86)
        za, zb = zm + (TH * 0.92 - 0.05) * t0, zm + (TH * 0.92 - 0.05) * t1
        y.yuz_yon([A_ + Z * za, B_ + Z * za, C_ + Z * zb, D_ + Z * zb], 'sindira' if k % 2 else 'sindira2', out + Z * 0.15)
    cubuk(y, ring[i] + Z * zo2, mid[i] + Z * zm, 0.008, 'ahsap_koyu')
    y.yuz_yon([ring[i] + Z * zo2, ring[j] + Z * zo2, ring[j] + Z * (zo2 - 0.008), ring[i] + Z * (zo2 - 0.008)], 'ahsap_koyu', out)
y.yuz_yon([p + Z * (zo2 - 0.008) for p in ring], 'ahsap_koyu', -Z)
zt8 = zm + (TH * 0.92 - 0.05)
rt = (R8 + 0.03) * 0.72 * 0.14
y.yuz_yon([V(p.x, p.y, zt8) for p in cokgen(CC, rt, 8, math.pi / 8)], 'sindira', Z)
# the neck, the scaled aspen onion and a cross
zn = boyun(y, CC, 0.026, zt8 - 0.004, 0.03, 'ahsap_acik', n=12)
zd = kubbe(y, CC, 0.064, zn - 0.002, 'sogan', 0.12, 'ahsap_acik', n=16, pul=['ahsap_acik', 'kutuk'], alt=2)
ortodoks_hac(y, CC.x, CC.y, zd - 0.004, 0.08, 'altin')
# a smaller onion on the porch's ridge
kubbe(y, (CC.x, PY0 + 0.03), 0.02, Z0 + 0.182 + 0.13 + 0.006, 'sogan', 0.04, 'ahsap_acik', n=10, pul=['ahsap_acik', 'kutuk'], alt=1)
ortodoks_hac(y, CC.x, PY0 + 0.03, Z0 + 0.182 + 0.13 + 0.044, 0.04, 'altin', top=False)

# ---------------------------------------------------------------- the stable
y.bolum('Ahır')
AX0, AX1, AY0, AY1 = 0.66, 0.96, -0.32, 0.58
AH = 0.17
# log back and end walls, an open front with posts and stall boards
kutuk_duvar2(y, V(AX1, AY0), V(AX1, AY1), Z0, Z0 + AH + 0.024, 0.012, 'kutuk', uzanti=0.025, ic=True)
kutuk_duvar2(y, V(AX1, AY1), V(AX0, AY1), Z0 + 0.012, Z0 + AH + 0.036, 0.012, 'kutuk', uzanti=0.025, ic=True)
kutuk_duvar2(y, V(AX0, AY0), V(AX1, AY0), Z0 + 0.012, Z0 + AH + 0.036, 0.012, 'kutuk', uzanti=0.025, ic=True)
NS = 5
for k in range(NS + 1):
    yy = AY0 + (AY1 - AY0) * k / NS
    y.prizma((AX0, yy), 0.01, Z0, Z0 + AH + 0.02, 'ahsap_koyu', n=6, ust=False)
    if 0 < k < NS:   # stall partitions
        kutu3(y, V((AX0 + AX1) / 2, yy, Z0 + 0.05), X, Y, Z, AX1 - AX0 - 0.02, 0.008, 0.1, 'ahsap_dikey')
cubuk(y, V(AX0, AY0, Z0 + AH + 0.016), V(AX0, AY1, Z0 + AH + 0.016), 0.02, 'ahsap_koyu')
y.yuz_yon([V(AX0 + 0.01, AY0 + 0.01, Z0 + 0.002), V(AX1 - 0.01, AY0 + 0.01, Z0 + 0.002), V(AX1 - 0.01, AY1 - 0.01, Z0 + 0.002),
           V(AX0 + 0.01, AY1 - 0.01, Z0 + 0.002)], 'saz', Z)
duz_duvar(y, V(AX1 - 0.013, AY1 - 0.012), V(AX1 - 0.013, AY0 + 0.012), Z0, Z0 + AH, 'ahsap_koyu')
# small hay hatches in the back wall, one per stall
for k in range(NS):
    nalichnik(y, V(AX1 + 0.0105, AY0 + (AY1 - AY0) * (k + 0.5) / NS, Z0 + 0.1), Y, 0.045, 0.04, 'ahsap_acik', 'koyu', None, None, t=0.005)
zra = cati_besik(y, AX0 - 0.01, AX1 + 0.012, AY0, AY1, Z0 + AH + 0.026, 0.15, 0.04, 'sindira', 'ahsap_koyu', kalinlik=0.01,
                 ucluk_key='ahsap_dikey', uc_sacak=0.03, nr=6, ns=10, dilim=['sindira', 'sindira2'])
kar_besik(y, AX0 - 0.01, AX1 + 0.012, AY0, AY1, Z0 + AH + 0.026, 0.15, sacak=0.04, uc_sacak=0.03, kapsam=0.75, tohum=11, n=12)
# horses looking out of three stalls, hay in the racks
for k, (key, yele) in zip((0, 2, 3), (('ahsap', 'ahsap_koyu'), ('ahsap_koyu', 'koyu'), ('beyaz', 'granit'))):
    yy = AY0 + (AY1 - AY0) * (k + 0.5) / NS
    at(y, AX0 + 0.08, yy, Z0, math.pi, 1.25, key, yele)
for k in range(NS):
    yy = AY0 + (AY1 - AY0) * (k + 0.5) / NS
    kutu3(y, V(AX1 - 0.04, yy, Z0 + 0.09), X, Y, Z, 0.05, 0.12, 0.05, 'saz')
# hay stack and firewood stack beside it
kar_yigin(y, AX0 - 0.1, AY1 - 0.08, Z0, 0.09, 0.14, 'saz', n=10, tohum=2)
kar_yigin(y, AX0 - 0.1, AY1 - 0.08, Z0 + 0.1, 0.055, 0.05, 'beyaz', n=10, tohum=3)
for k in range(3):
    for j in range(7):
        boru(y, [V(AX0 - 0.03 - j * 0.03, AY0 - 0.06, Z0 + 0.014 + k * 0.026), V(AX0 - 0.03 - j * 0.03, AY0 - 0.15, Z0 + 0.014 + k * 0.026)],
             0.013, 'ahsap_acik' if (j + k) % 2 else 'kutuk', n=6)
kutu3(y, V(AX0 - 0.12, AY0 - 0.105, Z0 + 0.085), X, Y, Z, 0.22, 0.1, 0.006, 'beyaz')

# ---------------------------------------------------------------- furs
def post(y, x, yy, z, L, W, H, aci, key, kuyruk=None, uc='beyaz'):
    """a pelt: a flat lumpy oval body, two leg flaps and (kuyruk) a tail ending in a tip"""
    with parca(y, (x, yy, z), aci):
        n, kat = 8, 3
        rings = []
        for k in range(kat + 1):
            ph = -math.pi / 2 + math.pi * k / kat
            rings.append([V(L / 2 * math.cos(ph) * math.cos(TAU * i / n), W / 2 * math.cos(ph) * math.sin(TAU * i / n), H / 2 + H / 2 * math.sin(ph)) for i in range(n)])
        for k in range(kat):
            A_, B_ = rings[k], rings[k + 1]
            for i in range(n):
                j = (i + 1) % n
                yuz_dis(y, [A_[i], A_[j], B_[j], B_[i]], key, V(0, 0, H / 2))
        for sx in (-1, 1):
            for sy in (-1, 1):
                kutu3(y, V(sx * L * 0.32, sy * W * 0.5, H * 0.3), X, Y, Z, L * 0.12, W * 0.28, H * 0.5, key)
        if kuyruk:
            boru(y, [V(L * 0.45, 0, H * 0.5), V(L * 0.75, W * 0.1, H * 0.45), V(L * 0.95, W * 0.05, H * 0.42)], W * 0.17, kuyruk, n=5, r_son=W * 0.08)
            kure(y, (L * 0.98, W * 0.05, H * 0.42), W * 0.09, uc, n=5, kat=3)


KURK = [('ahsap_koyu', 'ahsap_koyu'), ('turuncu', 'turuncu'), ('beyaz', 'beyaz'), ('granit_acik', 'granit_acik'), ('kutuk', 'kutuk')]


def yigin(y, x, yy, z, n, aci, tohum):
    rng = random.Random(tohum)
    for k in range(n):
        key, ky = KURK[rng.randrange(len(KURK))]
        post(y, x + rng.uniform(-0.008, 0.008), yy + rng.uniform(-0.008, 0.008), z + k * 0.014, 0.11, 0.06, 0.016, aci + rng.uniform(-0.35, 0.35),
             key, ky if rng.random() < 0.6 else None, 'beyaz' if key == 'turuncu' else 'koyu')
    return z + n * 0.014


y.bolum('Kürk tezgâhları ve yığınları')
# two trestle tables in the yard with stacks of pelts
for (tx, ty, ta) in ((-0.42, -0.42, 0.1), (-0.15, -0.62, -0.2)):
    with parca(y, (tx, ty, Z0), ta):
        kutu_merkez(y, (0, 0), 0.26, 0.11, 0.012, 'ahsap', z0=0.06)
        for sx in (-1, 1):
            for sy in (-1, 1):
                cubuk(y, V(sx * 0.11, sy * 0.03, 0.0), V(sx * 0.1, sy * 0.045, 0.062), 0.01, 'ahsap_koyu')
    for k, du in enumerate((-0.075, 0.0, 0.075)):
        yigin(y, tx + du * math.cos(ta), ty + du * math.sin(ta), Z0 + 0.072, 3 + (k + int(tx * 10)) % 3, ta + math.pi / 2, int(tx * 100) + k)
# heaps on the ground and on the counter
yigin(y, -0.36, -0.8, Z0, 4, 0.4, 51)
for k, u in enumerate((-0.12, 0.0, 0.12)):
    yigin(y, HC.x + u, HY0 - OF - 0.03, Z0 + 0.076, 2, 0.0, 60 + k)
# a drying rack with pelts hung on it
RX_, RY_ = -0.82, -0.2
for yy in (RY_ - 0.17, RY_ + 0.17):
    y.prizma((RX_, yy), 0.008, Z0, Z0 + 0.22, 'ahsap_koyu', n=6)
cubuk(y, V(RX_, RY_ - 0.19, Z0 + 0.2), V(RX_, RY_ + 0.19, Z0 + 0.2), 0.012, 'ahsap_koyu')
for k in range(5):
    yy = RY_ - 0.13 + k * 0.065
    key = KURK[(k * 3) % 5][0]
    o = V(RX_ + 0.004, yy, Z0 + 0.19)
    pts = [o + V(0, -0.018, 0), o + V(0, 0.018, 0), o + V(0, 0.026, -0.04), o + V(0, 0.016, -0.1), o + V(0, 0.0, -0.13),
           o + V(0, -0.016, -0.1), o + V(0, -0.026, -0.04)]
    levha(y, pts, key, -X, kil=0.004)

# ---------------------------------------------------------------- sledges
def kizak(y, x, yy, aci, yuk=True, tohum=0):
    """a sledge: two runners curling up at the front, posts, a slatted deck, rails and (yuk) a load of pelt bales"""
    with parca(y, (x, yy, Z0), aci):
        L = 0.26
        for sy in (-1, 1):
            boru(y, [V(-L / 2, sy * 0.045, 0.006), V(L / 2 - 0.03, sy * 0.045, 0.006), V(L / 2 + 0.01, sy * 0.045, 0.02), V(L / 2 + 0.02, sy * 0.045, 0.05)],
                 0.006, 'ahsap_koyu', n=5)
            for u in (-0.09, 0.0, 0.08):
                cubuk(y, V(u, sy * 0.045, 0.006), V(u, sy * 0.045, 0.04), 0.008, 'ahsap_koyu')
            cubuk(y, V(-L / 2 + 0.01, sy * 0.05, 0.06), V(L / 2 - 0.02, sy * 0.05, 0.06), 0.006, 'ahsap')
        kutu_merkez(y, (0, 0), L - 0.04, 0.1, 0.01, 'ahsap', z0=0.04)
        if yuk:
            rng = random.Random(tohum)
            for k in range(3):
                key = KURK[rng.randrange(5)][0]
                kutu3(y, V(-0.07 + k * 0.07, 0, 0.075), X, Y, Z, 0.06, 0.085, 0.06, key)
                cubuk(y, V(-0.07 + k * 0.07, -0.045, 0.106), V(-0.07 + k * 0.07, 0.045, 0.106), 0.005, 'ahsap_koyu')
            kutu3(y, V(0.0, 0, 0.12), X, Y, Z, 0.14, 0.07, 0.03, 'kumas')


y.bolum('Kızaklar ve atlar')
kizak(y, 0.2, -0.55, math.pi + 0.35, True, 1)
at(y, 0.02, -0.62, Z0, math.pi + 0.35, 1.35, 'ahsap_koyu', 'koyu')
for sy in (-1, 1):   # shafts and the duga arch over the horse's neck
    with parca(y, (0.2, -0.55, Z0), math.pi + 0.35):
        cubuk(y, V(0.13, sy * 0.04, 0.05), V(0.3, sy * 0.035, 0.07), 0.006, 'ahsap')
with parca(y, (0.2, -0.55, Z0), math.pi + 0.35):
    boru(y, [V(0.26, -0.035, 0.07), V(0.262, -0.025, 0.12), V(0.262, 0.0, 0.135), V(0.262, 0.025, 0.12), V(0.26, 0.035, 0.07)], 0.005, 'boya_kirmizi', n=5)
kizak(y, -0.35, 0.05, 1.2, True, 2)
kizak(y, 0.5, 0.75, 0.2, False, 3)

# ---------------------------------------------------------------- the sweep well
y.bolum('Kuyu (juravl)')
WC = V(0.42, -0.2)
for i in range(4):
    a, b = dikdortgen(WC.x - 0.045, WC.x + 0.045, WC.y - 0.045, WC.y + 0.045)[i], dikdortgen(WC.x - 0.045, WC.x + 0.045, WC.y - 0.045, WC.y + 0.045)[(i + 1) % 4]
    kutuk_duvar2(y, a, b, Z0 + (0.01 if i % 2 else 0), Z0 + 0.08 + (0.01 if i % 2 else 0), 0.01, 'kutuk', uzanti=0.015)
y.yuz_yon([V(p.x, p.y, Z0 + 0.03) for p in dikdortgen(WC.x - 0.035, WC.x + 0.035, WC.y - 0.035, WC.y + 0.035)], 'su', Z)
kar_yigin(y, WC.x, WC.y - 0.05, Z0 + 0.088, 0.045, 0.01, 'beyaz', n=8, tohum=5, uz=1.2)
FP = V(WC.x + 0.16, WC.y + 0.06)
y.prizma((FP.x, FP.y), 0.012, Z0, Z0 + 0.3, 'ahsap_koyu', n=6)
for sy in (-1, 1):
    cubuk(y, V(FP.x, FP.y, Z0 + 0.29), V(FP.x, FP.y + sy * 0.02, Z0 + 0.33), 0.008, 'ahsap_koyu')
piv = V(FP.x, FP.y, Z0 + 0.31)
d = V(WC.x - FP.x, WC.y - FP.y, 0).normalized()
ucu = piv + d * 0.24 + Z * 0.16
arka = piv - d * 0.16 - Z * 0.11
cubuk(y, arka, ucu, 0.009, 'ahsap')
kutu3(y, arka + d * 0.02, d, Z.cross(d), Z, 0.05, 0.03, 0.03, 'granit')
boru(y, [ucu, V(WC.x, WC.y, Z0 + 0.13)], 0.0025, 'ahsap_koyu', n=4)
donel(y, (WC.x, WC.y), [(0.0, Z0 + 0.1), (0.016, Z0 + 0.1), (0.02, Z0 + 0.13), (0.0, Z0 + 0.13)], 'ahsap_acik', n=8)

# ---------------------------------------------------------------- the fence and the gate
y.bolum('Kütük çit ve kapı')
FX0, FX1, FY0, FY1 = -1.0, 1.0, -0.92, 0.96
GW = 0.16
cit = [(V(-GW, FY0), V(FX0, FY0)), (V(FX0, FY0), V(FX0, FY1)), (V(FX0, FY1), V(FX1, FY1)), (V(FX1, FY1), V(FX1, FY0)), (V(FX1, FY0), V(GW, FY0))]
for a, b in cit:
    L = (b - a).length; e = (b - a) / L
    n = max(1, int(round(L / 0.16)))
    for k in range(n + 1):
        p = a + e * (L * k / n)
        y.prizma((p.x, p.y), 0.009, Z0, Z0 + 0.12, 'ahsap_koyu', n=6, ust=False)
        y.koni((p.x, p.y), 0.009, Z0 + 0.12, 0.014, 'beyaz', n=6)
    for zz in (0.035, 0.07, 0.1):
        boru(y, [a + Z * (Z0 + zz), b + Z * (Z0 + zz)], 0.007, 'kutuk', n=6)
    # drifts along the fence's foot
    for k in range(max(1, int(L / 0.45))):
        p = a + e * (L * (k + 0.5) / max(1, int(L / 0.45)))
        kar_yigin(y, p.x, p.y, Z0, 0.11, 0.035, 'beyaz', n=8, tohum=k + int(L * 10), uz=1.8, aci=math.atan2(e.y, e.x))
# the roofed gate: two tall posts, a beam, a little gable roof with snow, two plank leaves standing open
for sx in (-1, 1):
    y.prizma((sx * GW, FY0), 0.018, Z0, Z0 + 0.25, 'ahsap_koyu', n=8)
cubuk(y, V(-GW - 0.03, FY0, Z0 + 0.24), V(GW + 0.03, FY0, Z0 + 0.24), 0.026, 'ahsap_koyu')
oymali_sacak(y, V(-GW + 0.02, FY0 - 0.014, Z0 + 0.227), V(GW - 0.02, FY0 - 0.014, Z0 + 0.227), -Y, 'beyaz', 0.02, 8, 0.0)
ahsap_cati(y, -GW - 0.04, GW + 0.04, FY0 - 0.04, FY0 + 0.04, Z0 + 0.253, 0.08, sacak=0.02, uc_sacak=0.03, nr=4, ns=6, konek=True)
kar_besik(y, -GW - 0.04, GW + 0.04, FY0 - 0.04, FY0 + 0.04, Z0 + 0.253, 0.08, sacak=0.02, uc_sacak=0.03, kapsam=0.6, tohum=13, n=6)
for sx in (-1, 1):
    with parca(y, (sx * GW, FY0, Z0), sx * 0.0 + (math.pi / 2 + 0.25 if sx < 0 else math.pi / 2 - 0.25)):
        kutu3(y, V(sx * 0.0 + 0.075, 0, 0.1), X, Y, Z, 0.14, 0.012, 0.17, 'ahsap_dikey')
        for zz in (0.04, 0.15):
            kutu3(y, V(0.075, -0.008, zz), X, Y, Z, 0.14, 0.004, 0.014, 'ahsap_koyu')
y.bolum('Sancak')
sancak(y, -GW - 0.05, FY0 - 0.05, Z0, boy=0.42, en=0.12, yuk=0.075, aci=-math.pi / 2 - 0.6, direk_key='ahsap_koyu', kuyruk=True)

# ---------------------------------------------------------------- spruces, drifts, people
y.bolum('Ambar (kazıklar üstünde)')
# a raised log storehouse on stumps, an overhanging front gallery on posts, an iron-strapped door, snow on its roof
AMB = V(-0.72, -0.56)
with parca(y, (AMB.x, AMB.y, 0), 0.0):
    for sx in (-1, 1):
        for sy in (-1, 0, 1):
            y.prizma((sx * 0.1, sy * 0.075), 0.014, Z0, Z0 + 0.05, 'ahsap_koyu', n=6)
    za = kutuk_kutu(y, -0.11, 0.11, -0.085, 0.085, Z0 + 0.05, 0.13, 0.011, 'kutuk')
    # the gallery: a plank floor in front, two posts, the roof runs out over it
    kutu(y, V(-0.12, -0.15, Z0 + 0.04), X, 0.24, 0.07, 0.012, 'ahsap', 'onsagsolust')
    for sx in (-1, 1):
        y.prizma((sx * 0.11, -0.142), 0.007, Z0, za + 0.03, 'ahsap_koyu', n=6, ust=False)
    kutu3(y, V(0, -0.085 - 0.0105 + 0.004, Z0 + 0.12), X, -Y, Z, 0.07, 0.008, 0.11, 'ahsap_dikey', ('+x', '-x', '+y', '+z'))
    for zz in (0.09, 0.15):
        kutu3(y, V(0, -0.085 - 0.0105, Z0 + zz), X, -Y, Z, 0.072, 0.004, 0.008, 'demir')
    kure(y, (0.022, -0.1, Z0 + 0.12), 0.005, 'demir', n=6, kat=3)
    ahsap_cati(y, -0.122, 0.122, -0.16, 0.096, za + 0.03, 0.12, sacak=0.025, uc_sacak=0.03, nr=6, ns=6, konek=True)
    kar_besik(y, -0.122, 0.122, -0.16, 0.096, za + 0.03, 0.12, sacak=0.025, uc_sacak=0.03, kapsam=0.7, tohum=17, n=8)
    # a few bales and a barrel on the gallery
    kutu3(y, V(-0.07, -0.13, Z0 + 0.075), X, Y, Z, 0.05, 0.04, 0.045, 'kumas')
    donel(y, (0.07, -0.125), [(0.0, Z0 + 0.052), (0.018, Z0 + 0.052), (0.022, Z0 + 0.08), (0.018, Z0 + 0.108), (0.0, Z0 + 0.108)], 'ahsap_acik', n=10)

y.bolum('Ladinler ve kar yığınları')
for i, (x, yy, b) in enumerate(((-0.92, 0.82, 0.42), (-0.78, 0.92, 0.32), (-0.92, -0.78, 0.34), (0.86, -0.8, 0.36), (0.92, 0.86, 0.4),
                                (-0.2, 0.85, 0.34), (0.62, 0.88, 0.28), (-1.05, 0.2, 0.3))):
    ladin(y, x, yy, Z0, b, tohum=i)
for i, (x, yy, r) in enumerate(((HX0 - 0.03, 0.62, 0.08), (HX1 + 0.05, HY0 - 0.02, 0.07), (CC.x + 0.16, CC.y + 0.1, 0.07), (-0.5, -0.82, 0.09))):
    kar_yigin(y, x, yy, Z0, r, 0.04, 'beyaz', n=9, tohum=20 + i)

y.bolum('Tüccarlar')
for i, (x, yy, k, a) in enumerate(((-0.3, -0.5, 'ahsap_koyu', 0.3), (-0.38, -0.32, 'boya_kirmizi', -1.5), (-0.08, -0.53, 'kutuk', 2.0),
                                   (0.12, -0.2, 'ahsap', 0.8), (0.33, -0.25, 'kobalt', 2.5), (-0.62, -0.75, 'granit', 1.0), (HC.x, HY0 - 0.12, 'boya_kirmizi', math.pi / 2))):
    insan(y, x, yy, Z0, k, s=1.7, aci=a, sapka='ahsap_koyu' if i % 2 else 'granit_acik')

calistir(y, 'lm_kurkpazari')
