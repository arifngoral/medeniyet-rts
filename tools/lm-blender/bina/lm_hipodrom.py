# The Hippodrome of Constantinople (lm_hipodrom), shortened to fit a square plot: the U of marble seating round the
# sand track with its banded, two-tier arcaded outer wall and the colonnaded gallery on top, the curved sphendone at
# the south end, the spina down the middle (Theodosius' obelisk on its relief base, the bronze Serpent Column, the
# Walled Obelisk, the turning posts, statues on columns), the carceres with twelve starting gates and the four bronze
# horses over the central gate, the imperial kathisma (columned loggia, purple drapes) before a domed palace hall, and
# racing chariots of the red, green and white factions.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from bizans_ortak import *

y = Yapi(tohum=7)
R = random.Random(11)

Z0 = 0.04
XC, XS = -0.98, 0.40          # the carceres line, the sphendone's centre
RI, RO = 0.40, 0.70           # the arena's half width, the outer wall
PH = 0.05                     # podium
N, SH = 7, 0.024              # seat rows, row height
R1, R2 = RI + 0.03, RO - 0.05
ZT = Z0 + PH + N * SH          # top of the seating (promenade)
ZG = ZT + 0.1                  # gallery
RC = RO - 0.062                # gallery columns
NA = 20                        # sphendone segments


def U(r):
    """the U path at radius r: along the front (-y) from the carceres, round the sphendone, back along +y (CCW)"""
    pts = [V(XC, -r), V(XS, -r)]
    for k in range(1, NA):
        a = -math.pi / 2 + math.pi * k / NA
        pts.append(V(XS + r * math.cos(a), r * math.sin(a)))
    return pts + [V(XS, r), V(XC, r)]


def segs(r, i0=0, i1=None):
    P = U(r)
    i1 = len(P) - 1 if i1 is None else i1
    return [(P[i], P[i + 1]) for i in range(i0, i1)]


def nrm(a, b):
    e = (b - a).normalized()
    return V(e.y, -e.x)


def rz(r):
    """the gallery roof's height at radius r (it slopes down towards the arena)"""
    r0, r1 = RC - 0.016, RO + 0.014
    return ZG - 0.004 + (r - r0) / (r1 - r0) * 0.034


# ---------------------------------------------------------------- platform and arena
y.bolum('Zemin ve pist')
zemin(y, -1.205, 1.15, -0.82, 0.95, Z0, 'tas_koyu', basamak=(('on', 0.5), ('sol', 0.36)))
za = Z0 + 0.0025
y.yuz_yon([V(XC, -RI, za), V(XS, -RI, za), V(XS, RI, za), V(XC, RI, za)], 'toprak', Z)
for k in range(4):   # the sphendone's half disc in rings (quads: the baked shadow splits them)
    r0, r1 = RI * k / 4, RI * (k + 1) / 4
    for j in range(NA):
        a0, a1 = -math.pi / 2 + math.pi * j / NA, -math.pi / 2 + math.pi * (j + 1) / NA
        q = [V(XS + r0 * math.cos(a0), r0 * math.sin(a0), za), V(XS + r1 * math.cos(a0), r1 * math.sin(a0), za),
             V(XS + r1 * math.cos(a1), r1 * math.sin(a1), za), V(XS + r0 * math.cos(a1), r0 * math.sin(a1), za)]
        if k == 0: q = [q[0], q[1], q[2]]
        y.yuz_yon(q, 'toprak', Z)
# a white chalk line round the track
for s in (-1, 1):
    y.yuz_yon([V(XC + 0.08, s * 0.205 - 0.003, za + 0.0008), V(XS, s * 0.205 - 0.003, za + 0.0008), V(XS, s * 0.205 + 0.003, za + 0.0008),
               V(XC + 0.08, s * 0.205 + 0.003, za + 0.0008)], 'kum_acik', Z)

# ---------------------------------------------------------------- the seating
y.bolum('Oturma basamakları')
# podium wall towards the track (with a low parapet) and its walkway
for a, b in segs(RI):
    duz_duvar(y, b, a, Z0, Z0 + PH + 0.016, 'kirec')
silme(y, list(reversed(U(RI))), Z0 + PH - 0.006, 0.008, 0.004, 'mermer', 'duz', kapali=False)
P0, P1 = U(RI), U(RI + 0.008)
for i in range(len(P0) - 1):
    y.yuz_yon([P0[i] + Z * (Z0 + PH + 0.016), P0[i + 1] + Z * (Z0 + PH + 0.016), P1[i + 1] + Z * (Z0 + PH + 0.016), P1[i] + Z * (Z0 + PH + 0.016)], 'mermer', Z)
    duz_duvar(y, P1[i], P1[i + 1], Z0 + PH, Z0 + PH + 0.016, 'kirec')
P2 = U(R1)
for i in range(len(P0) - 1):
    y.yuz_yon([P1[i] + Z * (Z0 + PH), P1[i + 1] + Z * (Z0 + PH), P2[i + 1] + Z * (Z0 + PH), P2[i] + Z * (Z0 + PH)], 'zemin', Z)
# the rows: a riser (facing the track) and a marble tread each
for k in range(N):
    rk, rk1 = R1 + (R2 - R1) * k / N, R1 + (R2 - R1) * (k + 1) / N
    zk, zk1 = Z0 + PH + k * SH, Z0 + PH + (k + 1) * SH
    A, B = U(rk), U(rk1 if k < N - 1 else RO)
    for i in range(len(A) - 1):
        duz_duvar(y, A[i + 1], A[i], zk, zk1, 'kirec')
        y.yuz_yon([A[i] + Z * zk1, A[i + 1] + Z * zk1, B[i + 1] + Z * zk1, B[i] + Z * zk1], 'mermer' if k < N - 1 else 'zemin', Z)
# stairways (dark lines of steps) up the seating every so often
for i, (a, b) in enumerate(segs(R1)):
    if i in (0, NA + 1):
        us = [0.2, 0.5, 0.8]
    elif i % 5 == 3:
        us = [0.5]
    else:
        continue
    for u in us:
        p = a.lerp(b, u)
        e = (b - a).normalized(); n_ = nrm(a, b)
        for k in range(N):
            rk = (R2 - R1) * k / N
            hf = (R2 - R1) / N * 0.5
            q = p + n_ * (rk - hf)
            kutu(y, q - e * 0.008 + Z * (Z0 + PH + k * SH), e, 0.016, -hf, SH * 0.5, 'tas_acik', 'onsagsolust')

# spectators on the far side and round the sphendone
y.bolum('Seyirciler')
RENK = ['kirmizi', 'boya_yesil', 'beyaz', 'boya_sari', 'siva_oker', 'kumas', 'lake_koyu', 'boya_kirmizi']
for k in range(N):
    rk = R1 + (R2 - R1) * (k + 0.55) / N
    zk1 = Z0 + PH + (k + 1) * SH
    for i, (a, b) in enumerate(segs(rk)):
        if i == 0: continue
        L = (b - a).length
        m = max(1, int(L / 0.026))
        for j in range(m):
            if R.random() > 0.135: continue
            p = a.lerp(b, (j + 0.5) / m)
            if i == NA + 1 and abs(p.x + 0.3) < 0.27 and (p.y > 0.585 or abs(p.x + 0.3) < 0.13): continue   # (the kathisma, the palace)
            n_ = nrm(a, b)
            oturan(y, p.x, p.y, zk1, R.choice(RENK), aci=math.atan2(-n_.y, -n_.x), s=1.2)

# ---------------------------------------------------------------- the outer wall
y.bolum('Dış duvar (iki kat kemer)')
T1 = 0.12
for i, (a, b) in enumerate(segs(RO)):
    L = (b - a).length
    n = max(1, int(round(L / 0.1)))
    almasik(y, a, b, Z0, T1, n, en=0.5, v0=0.0, ust=0.022, pencere='koyu', derin=0.03,
            bant_list=[(0.05, 0.016)], cer=None)
    almasik(y, a, b, Z0 + T1, ZT - Z0 - T1, n, en=0.44, v0=0.018, ust=0.02, pencere='koyu', derin=0.026, cer=None,
            bant_list=[(0.07, 0.016)])
    # pilasters between the bays
    e = (b - a).normalized(); n_ = nrm(a, b)
    for k in range(n + 1 if i in (0,) else n):
        p = a.lerp(b, k / n)
        kutu(y, p - e * 0.007 + Z * Z0, e, 0.014, -0.008, ZT - Z0, 'kirec', 'arkasagsolust')
UO = U(RO)
silme(y, UO, Z0, 0.016, 0.01, 'kirec', 'kaide', kapali=False)
silme(y, UO, Z0 + T1 - 0.004, 0.012, 0.012, 'kirec', 'kaba', kapali=False)
silme(y, UO, ZT - 0.006, 0.014, 0.012, 'mermer', 'tac', kapali=False)
# the end of the U at the carceres is closed by it; the front run gets a parapet, the rest the gallery
a, b = UO[0], UO[1]
ic = U(RO - 0.016)
duz_duvar(y, a, b, ZT, ZT + 0.03, 'kirec')
duz_duvar(y, ic[1], ic[0], ZT, ZT + 0.03, 'kirec')
y.yuz_yon([a + Z * (ZT + 0.03), b + Z * (ZT + 0.03), ic[1] + Z * (ZT + 0.03), ic[0] + Z * (ZT + 0.03)], 'mermer', Z)

# ---------------------------------------------------------------- the gallery on top (sphendone and far side)
y.bolum('Üst galeri (sütunlu)')
G0 = 1
gw = segs(RO, G0); gi = segs(RO - 0.014, G0); gc = segs(RC, G0)
for (a, b), (ai, bi) in zip(gw, gi):
    L = (b - a).length
    n = max(1, int(round(L / 0.1)))
    zt_o, zt_i = rz(RO) - 0.006, rz(RO - 0.014) - 0.006
    almasik(y, a, b, ZT, zt_o - ZT, n, en=0.34, v0=0.03, ust=0.02, pencere='koyu', derin=0.012, bant_list=[], cer=None)
    duz_duvar(y, bi, ai, ZT, zt_i, 'kirec')
# the roof: tiles sloping in to the column line
ro, ri_ = U(RO + 0.014), U(RC - 0.016)
for i in range(G0, len(ro) - 1):
    ztop = [ro[i] + Z * rz(RO + 0.014), ro[i + 1] + Z * rz(RO + 0.014), ri_[i + 1] + Z * rz(RC - 0.016), ri_[i] + Z * rz(RC - 0.016)]
    y.yuz_yon(ztop, 'kiremit', Z)
    y.yuz_yon([p - Z * 0.008 for p in ztop], 'ahsap_koyu', -Z)
    y.yuz_yon([ztop[3], ztop[2], ztop[2] - Z * 0.008, ztop[3] - Z * 0.008], 'ahsap_koyu', -nrm(ro[i], ro[i + 1]))
    y.yuz_yon([ztop[0], ztop[1], ztop[1] - Z * 0.008, ztop[0] - Z * 0.008], 'ahsap_koyu', nrm(ro[i], ro[i + 1]))
    # ridge tiles along the wall line
    cubuk(y, V(ro[i].x, ro[i].y) + (V(ri_[i].x, ri_[i].y) - V(ro[i].x, ro[i].y)) * 0.25 + Z * (rz(RO) + 0.002),
          V(ro[i + 1].x, ro[i + 1].y) + (V(ri_[i + 1].x, ri_[i + 1].y) - V(ro[i + 1].x, ro[i + 1].y)) * 0.25 + Z * (rz(RO) + 0.002), 0.006, 'kiremit2')
# columns and the architrave on them
UC = U(RC)
zc = rz(RC) - 0.008
for i in range(G0, len(UC) - 1):
    a, b = UC[i], UC[i + 1]
    cubuk(y, a + Z * (zc - 0.007), b + Z * (zc - 0.007), 0.012, 'mermer', 0.014)
    L = (b - a).length
    m = max(1, int(round(L / 0.12)))
    for k in range(m):
        p = a.lerp(b, k / m)
        if i == len(UC) - 2 and abs(p.x + 0.3) < 0.26: continue
        sutun(y, p.x, p.y, ZT, zc - 0.014, 0.0075, 'mermer', 'osmanli')
# the gallery's open end on the front: a pier
kutu_merkez(y, (XS, -(RO + RC) / 2 + 0.006), 0.03, RO - RC + 0.034, rz(RO + 0.014) - ZT + 0.004, 'kirec', z0=ZT)
kornis(y, XS - 0.015, XS + 0.015, -RO - 0.011, -RC + 0.023, ZT - 0.002, 0.01, 0.005, 'mermer')

# ---------------------------------------------------------------- the spina
y.bolum('Spina: dikilitaşlar, Yılanlı Sütun, dönüş direkleri')
SX0, SX1, SW = -0.66, 0.24, 0.045
zs = za + 0.032
kutu(y, V(SX0, -SW, za - 0.001), X, SX1 - SX0, 2 * SW, zs - za + 0.001, 'mermer', 'onarkasagsol')
kornis(y, SX0, SX1, -SW, SW, za, 0.008, 0.006, 'mermer', 'kaide')
kornis(y, SX0, SX1, -SW, SW, zs - 0.008, 0.008, 0.006, 'mermer', 'tac')
y.yuz_yon([V(SX0, -SW, zs), V(SX1, -SW, zs), V(SX1, SW, zs), V(SX0, SW, zs)], 'mermer', Z)
# the euripus: water basins along the top between the monuments
for x0, x1 in ((-0.55, -0.495), (-0.34, -0.22), (-0.125, -0.01)):
    y.yuz_yon([V(x0, -SW * 0.55, zs + 0.0015), V(x1, -SW * 0.55, zs + 0.0015), V(x1, SW * 0.55, zs + 0.0015), V(x0, SW * 0.55, zs + 0.0015)], 'su', Z)
    for (p, q) in ((V(x0, -SW * 0.6), V(x1, -SW * 0.6)), (V(x1, SW * 0.6), V(x0, SW * 0.6))):
        kutu(y, p + Z * zs, (q - p).normalized(), (q - p).length, 0.004 if p.y < 0 else 0.004, 0.006, 'mermer', 'onarkasagsolust')
# panels on the spina's long sides
for s in (-1, 1):
    for k in range(8):
        x0 = SX0 + 0.03 + k * (SX1 - SX0 - 0.06) / 8
        x1 = x0 + (SX1 - SX0 - 0.06) / 8 - 0.014
        yy = s * (SW + 0.0012)
        y.yuz_yon([V(x0, yy, za + 0.011), V(x1, yy, za + 0.011), V(x1, yy, zs - 0.01), V(x0, yy, zs - 0.01)], 'tas_acik', V(0, s, 0))


def meta(x):
    """a turning post: a half-round base with three gilded cones"""
    donel(y, (x, 0), [(0.0, zs), (0.055, zs), (0.055, zs + 0.02), (0.0, zs + 0.02)], 'mermer', n=16)
    halka_kornis(y, (x, 0), 0.055, zs + 0.016, 0.006, 0.004, 16, 'mermer', profil='tac')
    for dy in (-0.026, 0.0, 0.026):
        donel(y, (x, dy), [(0.012, zs + 0.02), (0.012, zs + 0.034), (0.0105, zs + 0.036), (0.008, zs + 0.11), (0.0, zs + 0.13)], 'bronz', n=10)
        kure(y, (x, dy, zs + 0.134), 0.006, 'altin', n=8, kat=4)
        halka_kornis(y, (x, dy), 0.0105, zs + 0.05, 0.004, 0.002, 10, 'altin')


meta(SX0 - 0.03)
meta(SX1 + 0.03)

# the Obelisk of Theodosius on its relief base and four bronze blocks
TX = -0.42
kutu_merkez(y, (TX, 0), 0.13, 0.13, 0.016, 'mermer', z0=zs)
kutu_merkez(y, (TX, 0), 0.11, 0.11, 0.06, 'mermer', z0=zs + 0.016)
kornis(y, TX - 0.055, TX + 0.055, -0.055, 0.055, zs + 0.07, 0.012, 0.008, 'mermer', 'tac')
kutu_merkez(y, (TX, 0), 0.096, 0.096, 0.03, 'mermer', z0=zs + 0.082)
for j, (e, n_) in enumerate(((X, -Y), (Y, X), (-X, Y), (-Y, -X))):   # relief panels: the emperor's court in the kathisma
    c = V(TX, 0) + n_ * 0.0552
    for k in range(7):
        u = -0.04 + k * 0.0133
        p = c + e * u + Z * (zs + 0.028)
        big = (k == 3)
        kutu(y, p - e * 0.003, e, 0.006, -0.003, 0.022 if big else 0.018, 'tas_acik', 'arkasagsolust')
        kure(y, p + n_ * 0.0015 + Z * (0.026 if big else 0.021), 0.0032, 'tas_acik', n=6, kat=3)
    kutu(y, c - e * 0.046 + Z * (zs + 0.024), e, 0.092, -0.002, 0.003, 'tas_acik', 'arkasagsolust')
for sx in (-1, 1):
    for sy in (-1, 1):
        kutu_merkez(y, (TX + sx * 0.028, sy * 0.028), 0.022, 0.022, 0.014, 'bronz', z0=zs + 0.112)
dikilitas(y, (TX, 0), 0.062, 0.46, 'granit_kizil', 'granit_kizil', z0=zs + 0.126, kaide=False, yazi_key='granit_kizil_koyu')

# the Serpent Column: three bronze snakes twisted, their heads spread at the top under a golden bowl
SXc = -0.17
kutu_merkez(y, (SXc, 0), 0.07, 0.07, 0.03, 'mermer', z0=zs)
kornis(y, SXc - 0.035, SXc + 0.035, -0.035, 0.035, zs + 0.024, 0.008, 0.005, 'mermer', 'tac')
zb, Hs = zs + 0.032, 0.2
for j in range(3):
    pts = []
    for k in range(25):
        t = k / 24
        a = TAU * 3.2 * t + TAU * j / 3
        rr = 0.0105 * (1 - 0.25 * t)
        pts.append(V(SXc + rr * math.cos(a), rr * math.sin(a), zb + Hs * t))
    a = TAU * 3.2 + TAU * j / 3
    d = V(math.cos(a), math.sin(a))
    top = pts[-1]
    pts += [top + d * 0.012 + Z * 0.012, top + d * 0.03 + Z * 0.016, top + d * 0.042 + Z * 0.01]
    boru(y, pts, 0.0062, 'bronz', n=6, r_son=0.0045)
    kure(y, top + d * 0.045 + Z * 0.01, 0.0072, 'bronz', n=8, kat=4)
donel(y, (SXc, 0), [(0.0, zb + Hs + 0.022), (0.028, zb + Hs + 0.03), (0.04, zb + Hs + 0.058), (0.036, zb + Hs + 0.06), (0.0, zb + Hs + 0.052)], 'altin', n=18)

# the Walled Obelisk: built of stone courses, bronze plates on it, the tallest thing on the spina
WX = 0.07
wt = dikilitas(y, (WX, 0), 0.075, 0.7, 'tas', 'bronz', z0=zs)
w0 = zs + 0.075 * 0.55
for k in range(1, 12):   # the coursing (projecting joints every few courses)
    t = k / 12
    zz = w0 + 0.63 * t
    wh = 0.075 / 2 * (1 - 0.34 * t) + 0.0012
    kornis(y, WX - wh, WX + wh, -wh, wh, zz, 0.003, 0.001, 'tas_koyu')
for k in (2, 5, 8):   # bronze plates
    t = (k + 0.5) / 12
    zz = w0 + 0.63 * t
    wh = 0.075 / 2 * (1 - 0.34 * t) + 0.0018
    for e, n_ in ((X, -Y), (Y, X), (-X, Y), (-Y, -X)):
        c = V(WX, 0) + n_ * wh + Z * zz
        y.yuz_yon([c - e * wh * 0.7, c + e * wh * 0.7, c + e * wh * 0.68 + Z * 0.03, c - e * wh * 0.68 + Z * 0.03], 'bronz', n_ + Z * 0.03)

# statues on columns at the spina's ends and a gilded quadriga-less Victory
sutun_heykel(y, -0.58, 0.0, zs, 0.2, 1.0, 'mermer', 'bronz', aci=math.pi)
sutun_heykel(y, 0.18, 0.0, zs, 0.18, 1.0, 'mermer', 'altin', aci=0)

# ---------------------------------------------------------------- the carceres
y.bolum('Carceres: başlangıç kapıları, dört bronz at')
CX0, CX1 = XC - 0.19, XC
HC = 0.36
# the front towards the track: 12 starting gates either side of the central gate, the upper storey over them
GW = 0.11
for s in (-1, 1):
    a, b = (V(CX1, -RI), V(CX1, -GW)) if s < 0 else (V(CX1, GW), V(CX1, RI))
    almasik(y, a, b, Z0, 0.11, 6, en=0.72, v0=0.0, ust=0.014, pencere='ahsap', derin=0.02, bant_list=[(0.0, 0.014)],
            cer=(0.005, ['mermer', 'tugla_roma']), duvar='kirec')
    almasik(y, a, b, Z0 + 0.11, HC - 0.11, 3, en=0.4, v0=0.04, ust=0.03, derin=0.02, cer=None)
for a, b in ((V(CX1, -RO), V(CX1, -RI)), (V(CX1, RI), V(CX1, RO))):
    almasik(y, a, b, Z0, HC, 0)
kornis(y, CX0, CX1, -RO, RO, Z0 + 0.105, 0.008, 0.006, 'mermer')
# the back (outside, west), the ends
almasik(y, V(CX0, RO), V(CX0, GW), Z0, HC, 5, en=0.42, v0=0.12, ust=0.03, cer=None)
almasik(y, V(CX0, -GW), V(CX0, -RO), Z0, HC, 5, en=0.42, v0=0.12, ust=0.03, cer=None)
for x0 in (CX0,):
    pass
silme(y, dikdortgen(CX0, CX1, -RO, RO), Z0 + HC - 0.014, 0.018, 0.012, 'kirec', 'tac')
silme(y, dikdortgen(CX0, CX1, -RO, RO), Z0, 0.014, 0.008, 'kirec', 'kaide')
duz_duvar(y, V(CX0, -RO), V(CX1, -RO), Z0, Z0 + HC, 'kirec')
duz_duvar(y, V(CX1, RO), V(CX0, RO), Z0, Z0 + HC, 'kirec')
kiremit_cati(y, CX0, CX1, -RO, RO, Z0 + HC, 0.07, sacak=0.02)
# the end towers
for s in (-1, 1):
    tx, ty, tw = (CX0 + CX1) / 2, s * (RO - 0.03), 0.17
    kk = dikdortgen(tx - tw / 2, tx + tw / 2, ty - tw / 2, ty + tw / 2)
    for i in range(4):
        almasik(y, kk[i], kk[(i + 1) % 4], Z0, 0.47, 1, en=0.32, v0=0.3, ust=0.04, derin=0.02, bant_list=bantlar(0.47, 0.08))
    silme(y, kk, Z0 + 0.47 - 0.014, 0.018, 0.012, 'kirec', 'tac')
    silme(y, kk, Z0, 0.014, 0.008, 'kirec', 'kaide')
    cati_kirma(y, tx - tw / 2, tx + tw / 2, ty - tw / 2, ty + tw / 2, Z0 + 0.47, 0.1, 0.022, 'kiremit', 'kiremit2', kalinlik=0.01)
    if s > 0: hac(y, tx, ty, Z0 + 0.58, 0.04)
    else: sancak(y, tx, ty, Z0 + 0.575, boy=0.2, en=0.12, yuk=0.07, aci=math.pi * 0.85)
# the central gate tower, the four bronze horses on it
GH = 0.48
gk = dikdortgen(CX0 - 0.015, CX1 + 0.015, -GW, GW)
for i in range(4):
    a, b = gk[i], gk[(i + 1) % 4]
    if i in (1, 3):
        y.kemerli(a, b, Z0, 0.26, ('mermer', 'tas_koyu', 'mermer', 'koyu'), v0=0.0, en=0.62, ust=0.04, derin=0.05, k_say=10,
                  cerceve=(0.012, ['mermer', 'tugla_roma']))
        almasik(y, a, b, Z0 + 0.26, GH - 0.26, 3, en=0.45, v0=0.04, ust=0.03, duvar='mermer', bant='kirec', derin=0.018)
    else:
        almasik(y, a, b, Z0, GH, 0, duvar='mermer', bant='kirec')
silme(y, gk, Z0 + 0.255, 0.014, 0.01, 'mermer', 'kaba')
silme(y, gk, Z0 + GH - 0.016, 0.02, 0.014, 'mermer', 'tac')
silme(y, gk, Z0, 0.016, 0.01, 'mermer', 'kaide')
y.yuz_yon([V(p.x, p.y, Z0 + GH + 0.004) for p in gk], 'mermer', Z)
kutu_merkez(y, ((CX0 + CX1) / 2, 0), 0.15, 0.13, 0.024, 'mermer', z0=Z0 + GH + 0.004)
kornis(y, (CX0 + CX1) / 2 - 0.075, (CX0 + CX1) / 2 + 0.075, -0.065, 0.065, Z0 + GH + 0.02, 0.008, 0.005, 'mermer', 'tac')
for k, dy in enumerate((-0.045, -0.015, 0.015, 0.045)):
    at(y, (CX0 + CX1) / 2 - 0.005, dy, Z0 + GH + 0.03, aci=0.0 + (0.12 if dy < 0 else -0.12) * (abs(dy) > 0.03), s=1.15, key='bronz', poz='dur')

# ---------------------------------------------------------------- the kathisma and the palace hall behind it
y.bolum('Kathisma (imparator locası) ve saray salonu')
XK = -0.3
KW = 0.105
KY0, KY1 = RI - 0.03, 0.62
# lower block: arched openings to the track
almasik(y, V(XK - KW, KY0), V(XK + KW, KY0), Z0, ZT - Z0, 3, en=0.55, v0=0.0, ust=0.02, pencere='koyu', derin=0.03, bant_list=[(0.03, 0.014), (0.1, 0.014)])
for a, b in ((V(XK + KW, KY0), V(XK + KW, KY1)), (V(XK - KW, KY1), V(XK - KW, KY0))):
    almasik(y, a, b, Z0, ZT - Z0, 0, bant_list=[(0.03, 0.014), (0.1, 0.014)])
kornis(y, XK - KW, XK + KW, KY0, KY1, ZT - 0.012, 0.014, 0.01, 'mermer', 'tac')
y.yuz_yon([V(XK - KW, KY0, ZT + 0.002), V(XK + KW, KY0, ZT + 0.002), V(XK + KW, KY1, ZT + 0.002), V(XK - KW, KY1, ZT + 0.002)], 'mermer', Z)
# the loggia: five columns, a balustrade with purple drapes, the emperor
ZL = ZT + 0.002
for k in range(5):
    x = XK - KW + 0.012 + (2 * KW - 0.024) * k / 4
    sutun(y, x, KY0 + 0.014, ZL, ZL + 0.12, 0.0085, 'mermer', 'korint', yiv=12)
for k in range(4):
    x0 = XK - KW + 0.012 + (2 * KW - 0.024) * k / 4 + 0.012
    x1 = XK - KW + 0.012 + (2 * KW - 0.024) * (k + 1) / 4 - 0.012
    kutu(y, V(x0, KY0 + 0.002, ZL), X, x1 - x0, 0.016, 0.03, 'mermer')
    # the drape over the balustrade, hanging in folds down the block's face
    for j in range(4):
        u0, u1 = x0 + (x1 - x0) * j / 4, x0 + (x1 - x0) * (j + 1) / 4
        f = 0.0015 if j % 2 else 0.0
        yd = KY0 - 0.0025 - f
        y.yuz_yon([V(u0, yd, ZL - 0.04), V(u1, yd, ZL - 0.04), V(u1, yd, ZL + 0.033), V(u0, yd, ZL + 0.033)], 'lacivert', -Y)
        y.yuz_yon([V(u0, yd, ZL + 0.033), V(u1, yd, ZL + 0.033), V(u1, KY0 + 0.02, ZL + 0.033), V(u0, KY0 + 0.02, ZL + 0.033)], 'lacivert', Z)
    y.yuz_yon([V(x0, KY0 - 0.0055, ZL - 0.04), V(x1, KY0 - 0.0055, ZL - 0.04), V(x1, KY0 - 0.0055, ZL - 0.033), V(x0, KY0 - 0.0055, ZL - 0.033)], 'altin', -Y)
# side walls of the loggia
for sx in (-1, 1):
    a, b = (V(XK + KW, KY0 + 0.03), V(XK + KW, KY1)) if sx > 0 else (V(XK - KW, KY1), V(XK - KW, KY0 + 0.03))
    almasik(y, a, b, ZL, 0.12, 2, en=0.45, v0=0.03, ust=0.02, derin=0.012, bant_list=[(0.06, 0.012)])
    ai, bi = V(a.x - sx * 0.014, a.y), V(b.x - sx * 0.014, b.y)
    duz_duvar(y, bi, ai, ZL, ZL + 0.12, 'kirec')
    y.yuz_yon([V(XK + sx * KW, KY0 + 0.03, ZL), V(XK + sx * KW, KY0 + 0.03, ZL + 0.12), V(XK + sx * (KW - 0.014), KY0 + 0.03, ZL + 0.12),
               V(XK + sx * (KW - 0.014), KY0 + 0.03, ZL)], 'kirec', -Y)
# back wall of the loggia (in the palace's face) with the imperial door, the throne and the emperor
kapi(y, V(XK - 0.06, 0.6 - 0.002), V(XK + 0.06, 0.6 - 0.002), ZL, 0.7, 0.12, ('mermer', 'tas_koyu', 'mermer', 'altin'), derin=0.01,
     cerceve=(0.008, 'altin'))
kutu_merkez(y, (XK, 0.55), 0.05, 0.03, 0.012, 'mermer', z0=ZL)
kutu_merkez(y, (XK, 0.556), 0.034, 0.018, 0.06, 'altin', z0=ZL + 0.012)
insan(y, XK, 0.54, ZL + 0.012, 'lacivert', 1.55, aci=-math.pi / 2, kol=0.6, sapka='altin')
for sx in (-1, 1):   # guards
    insan(y, XK + sx * 0.07, 0.5, ZL, 'boya_kirmizi', 1.45, aci=-math.pi / 2, sapka='demir')
# entablature and the pediment roof
ZE = ZL + 0.12
kutu(y, V(XK - KW - 0.004, KY0 + 0.002, ZE), X, 2 * KW + 0.008, KY1 - KY0 - 0.002, 0.028, 'mermer')
kornis(y, XK - KW - 0.004, XK + KW + 0.004, KY0 + 0.002, KY1, ZE + 0.02, 0.01, 0.008, 'mermer', 'tac')
cati_besik(y, XK - KW, XK + KW, KY0 + 0.004, KY1, ZE + 0.03, 0.075, 0.02, 'kiremit', 'kiremit2', kalinlik=0.01, ucluk_key='mermer', alinlik_key='mermer')
y.yuz_yon([V(XK + 0.022 * math.cos(TAU * k / 12), KY0 + 0.0015, ZE + 0.06 + 0.022 * math.sin(TAU * k / 12)) for k in range(12)], 'altin', -Y)   # a gilded roundel
hac(y, XK, KY0 - 0.008, ZE + 0.104, 0.05)
# the palace hall: banded walls (windows above the seating), a domed roof
PX0, PX1, PY0, PY1 = XK - 0.25, XK + 0.25, 0.6, 0.93
ZP1, ZP = 0.45, 0.62           # the old cornice (now a string course), the raised upper storey's top
almasik(y, V(PX0, PY0), V(PX1, PY0), Z0, ZT - Z0, 0)
almasik(y, V(PX0, PY0), V(PX1, PY0), ZT, ZP1 - ZT, 5, en=0.42, v0=0.04, ust=0.03, bos=(1, 2, 3))
almasik(y, V(PX1, PY0), V(PX1, 0.73), Z0, ZP1 - Z0, 0)
almasik(y, V(PX1, 0.73), V(PX1, PY1), Z0, ZP1 - Z0, 2, en=0.4, v0=0.14, ust=0.04, cer=None)
almasik(y, V(PX1, PY1), V(PX0, PY1), Z0, ZP1 - Z0, 5, en=0.4, v0=0.14, ust=0.04, kapi_bay=2, cer=None)
almasik(y, V(PX0, PY1), V(PX0, 0.73), Z0, ZP1 - Z0, 2, en=0.4, v0=0.14, ust=0.04, cer=None)
almasik(y, V(PX0, 0.73), V(PX0, PY0), Z0, ZP1 - Z0, 0)
pk = dikdortgen(PX0, PX1, PY0, PY1)
# the upper storey: a row of arched windows on every side (the throne hall over the kathisma)
for i, n in enumerate((5, 3, 5, 3)):
    almasik(y, pk[i], pk[(i + 1) % 4], ZP1, ZP - ZP1, n, en=0.5, v0=0.03, ust=0.03, derin=0.022, cer=(0.007, ['mermer', 'tugla_roma']),
            bant_list=[(0.0, 0.014)])
silme(y, pk, ZP1 - 0.01, 0.02, 0.014, 'kirec', 'kaba')
silme(y, pk, ZP - 0.016, 0.022, 0.016, 'kirec', 'tac')
silme(y, pk, ZT + 0.07, 0.01, 0.008, 'kirec', 'duz')
y.yuz_yon([V(p.x, p.y, ZP + 0.006) for p in pk], 'kursun', Z)
parapet(y, disa(pk, 0.012), ZP + 0.006, 0.012, 0.0, 0.014, 'kirec', ust_key='mermer')
kutu_merkez(y, (XK, 0.765), 0.31, 0.31, 0.034, 'kirec', z0=ZP + 0.006)
kornis(y, XK - 0.155, XK + 0.155, 0.765 - 0.155, 0.765 + 0.155, ZP + 0.03, 0.01, 0.008, 'kirec', 'tac')
biz_kubbe(y, (XK, 0.765), 0.135, ZP + 0.04, 0.075, 14, kubbe_h=0.125)
for sx in (-1, 1):
    for sy in (-1, 1):
        kucuk_kubbe(y, XK + sx * 0.2, 0.765 + sy * 0.12, ZP + 0.006, 0.032, kasnak=0.024, n=12, son=False, key='kursun', kasnak_key='tugla_roma')
sancak(y, PX1 - 0.035, PY1 - 0.035, ZP + 0.006, boy=0.27, en=0.13, yuk=0.075, aci=math.pi * 0.9)

# ---------------------------------------------------------------- chariots
y.bolum('Yarış arabaları')


def araba(x, yy, aci, renk, faz=0.0):
    """a racing quadriga: four galloping horses abreast, the pole, a two-wheeled car with its charioteer"""
    with parca(y, (x, yy, za), aci):
        for k, dy in enumerate((-0.027, -0.009, 0.009, 0.027)):
            at(y, 0.06, dy, 0, 0, 0.9, 'kum_koyu' if k % 2 else 'ahsap', 'kos', yele='ahsap_koyu', faz=faz + 0.13 * k)
        cubuk(y, V(-0.004, 0, 0.018), V(0.07, 0, 0.034), 0.003, 'ahsap_koyu')
        cubuk(y, V(0.06, -0.034, 0.038), V(0.06, 0.034, 0.038), 0.003, 'ahsap_koyu')   # the yoke
        for sy in (-1, 1):
            boru(y, [V(-0.012, sy * 0.021, 0.016), V(-0.012, sy * 0.027, 0.016)], 0.0155, 'ahsap_koyu', n=12)
            boru(y, [V(-0.012, sy * 0.0205, 0.016), V(-0.012, sy * 0.0275, 0.016)], 0.005, 'demir', n=6)
        cubuk(y, V(-0.012, -0.029, 0.016), V(-0.012, 0.029, 0.016), 0.003, 'demir')
        kutu_merkez(y, (-0.01, 0), 0.026, 0.034, 0.003, 'ahsap', z0=0.016)
        donel(y, (-0.012, 0), [(0.016, 0.019), (0.017, 0.034), (0.0, 0.034)], renk, n=10, dilim=None)
        insan(y, -0.014, 0, 0.019, renk, 1.2, aci=0.0, kol=0.5, sapka=renk)
        for sy in (-1, 1):   # reins
            cubuk(y, V(-0.008, sy * 0.004, 0.05), V(0.105, sy * 0.012, 0.062), 0.0012, 'ahsap_koyu')


araba(-0.1, -0.24, 0.0, 'boya_kirmizi', 0.1)
araba(XS + 0.22 * math.cos(-0.5), 0.22 * math.sin(-0.5) - 0.0, -0.5 + math.pi / 2, 'boya_yesil', 0.45)

# ---------------------------------------------------------------- around: cypresses, a fountain, statues
y.bolum('Çevre: selviler, heykeller')
for x, yy in ((1.07, -0.72), (1.1, -0.5), (1.1, 0.52), (1.07, 0.78), (0.86, 0.86), (0.82, -0.78), (0.45, 0.86), (0.18, 0.88)):
    agac(y, x, yy, Z0, boy=0.2, tur='servi', key='yesil_koyu')
for x in (-0.35,):
    sutun_heykel(y, x, -0.77, Z0, 0.16, 0.9, 'mermer', 'bronz', aci=-math.pi / 2)
# a round fountain off the sphendone
donel(y, (0.98, -0.6), [(0.0, Z0), (0.05, Z0), (0.05, Z0 + 0.016), (0.042, Z0 + 0.016), (0.042, Z0 + 0.008), (0.0, Z0 + 0.008)], 'mermer', n=16)
y.yuz_yon([V(p.x, p.y, Z0 + 0.012) for p in cokgen((0.98, -0.6), 0.042, 16)], 'su', Z)
y.prizma((0.98, -0.6), 0.008, Z0, Z0 + 0.05, 'mermer', n=8)
donel(y, (0.98, -0.6), [(0.0, Z0 + 0.045), (0.022, Z0 + 0.05), (0.02, Z0 + 0.058), (0.0, Z0 + 0.055)], 'mermer', n=12)

calistir(y, 'lm_hipodrom')
