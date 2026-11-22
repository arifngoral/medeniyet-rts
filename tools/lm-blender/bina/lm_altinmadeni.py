# Bambuk gold mines (lm_altinmadeni): a red laterite field pocked with vertical shafts, each with a wooden windlass and
# a heap of spoil, miners hauling ore; by the river women wash the gravel in calabashes and a pirogue waits; traders
# weigh gold dust under a market shade beside camels loaded with Saharan salt; a walled mud village with round huts and
# granaries, and over it all a tall Sahel watchtower flying the banner.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mali_ek import *
from arap_ortak import deve
import doku

y = Yapi()
rn = random.Random(11)
Z0 = 0.03
SU = Z0 - 0.034                       # the river's water level

# ---------------- terrain ----------------
GX0, GX1, GY0, GY1 = -1.16, 1.16, -1.16, 1.16
NX = NY = 38
CS = (GX1 - GX0) / NX
# shafts on grid vertices (each cuts a 2 x 2 cell hole filled by its own ring)
KUYU_IJ = [(14, 9), (19, 6), (24, 10), (17, 13), (22, 15), (28, 7), (12, 14), (31, 13), (34, 6), (26, 18)]
KUYULAR = [(GX0 + i * CS, GY0 + j * CS) for i, j in KUYU_IJ]


def nehir_x(py):
    return -0.9 + 0.07 * math.sin(2.3 * py + 0.6)


def yuk(px, py):
    """ground height"""
    h = 0.006 * math.sin(5.1 * px + 1.3) * math.cos(4.3 * py - 0.4) + 0.004 * math.sin(11 * px - 7 * py)
    # the river channel down the west side
    d = abs(px - nehir_x(py))
    t = max(0.0, 1 - d / 0.2)
    h -= 0.075 * (t * t * (3 - 2 * t))
    # a low rise behind the village
    h += 0.07 * math.exp(-(((px - 0.4) / 0.6) ** 2 + ((py - 1.25) / 0.3) ** 2))
    return Z0 + h


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def arazi_renk(x, yy, z):
    n = math.sin(x * 4.1 + 0.7) * math.cos(yy * 3.3 - 0.2) * 0.7 + math.sin(x * 9.3 - yy * 7.1 + 1.0) * 0.3
    c = _mix((0.70, 0.46, 0.30), (0.62, 0.38, 0.24), 0.5 + 0.5 * n)                 # red laterite, worked earth
    # dry grass away from the diggings
    dk = min(math.hypot(x - kx, yy - ky) for kx, ky in KUYULAR)
    c = _mix(c, (0.66, 0.60, 0.38), 0.75 * _ss(0.25, 0.5, dk + 0.08 * n) * _ss(-0.9, -0.5, -abs(x - 0.55) - 0.0))
    c = _mix(c, (0.62, 0.58, 0.36), 0.5 * _ss(0.6, 1.0, yy + 0.2 * n))
    # wet sand and mud down the banks
    d = abs(x - nehir_x(yy))
    c = _mix(c, (0.74, 0.64, 0.48), _ss(0.3, 0.16, d))
    c = _mix(c, (0.46, 0.38, 0.28), _ss(0.13, 0.07, d))
    return c


doku.KOSE_RENK['toprak_ot'] = arazi_renk
y.bolum('Arazi')
P = [[V(GX0 + CS * i, GY0 + CS * j, 0) for j in range(NY + 1)] for i in range(NX + 1)]
delik = set()
for i, j in KUYU_IJ:
    for di in (-1, 0):
        for dj in (-1, 0):
            delik.add((i + di, j + dj))
for i in range(NX + 1):
    for j in range(NY + 1):
        P[i][j].z = yuk(P[i][j].x, P[i][j].y)
# (the shaft yards are flat: their ring meets the grid)
for i, j in KUYU_IJ:
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            P[i + di][j + dj].z = Z0
for i in range(NX):
    for j in range(NY):
        if (i, j) in delik: continue
        dg = (i + j) % 2 == 0
        for tri in (([P[i][j], P[i + 1][j], P[i + 1][j + 1]], [P[i][j], P[i + 1][j + 1], P[i][j + 1]]) if dg else
                    ([P[i][j], P[i + 1][j], P[i][j + 1]], [P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]])):
            y.yuz(tri, 'toprak_ot')
# the shaft yards: the square of 2 x 2 cells round each shaft, filled from its edge in to the pit's rim
for (i, j), (kx, ky) in zip(KUYU_IJ, KUYULAR):
    n = 16
    R = 0.045 * 1.62
    kare = []
    for k in range(n):
        t = TAU * k / n + math.pi / 4
        cx_, cy_ = math.cos(t), math.sin(t)
        s = CS / max(abs(cx_), abs(cy_))
        kare.append(V(kx + cx_ * s, ky + cy_ * s, Z0))
    ic = [V(kx + R * math.cos(TAU * k / n + math.pi / 4), ky + R * math.sin(TAU * k / n + math.pi / 4), Z0 - 0.001) for k in range(n)]
    for k in range(n):
        q = [kare[k], kare[(k + 1) % n], ic[(k + 1) % n], ic[k]]
        y.yuz_yon(q, 'toprak_ot', Z)
# the skirt round the edge
kenar = [P[i][0] for i in range(NX)] + [P[NX][j] for j in range(NY)] + [P[i][NY] for i in range(NX, 0, -1)] + [P[0][j] for j in range(NY, 0, -1)]
for k in range(len(kenar)):
    a, b = kenar[k], kenar[(k + 1) % len(kenar)]
    e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
    za, zb_ = min(a.z, SU) - 0.03, min(b.z, SU) - 0.03
    y.yuz_yon([V(a.x, a.y, za), V(b.x, b.y, zb_), b, a], 'kerpic_koyu', nn)
    y.yuz_yon([V(a.x, a.y, -0.07), V(b.x, b.y, -0.07), V(b.x, b.y, za), V(a.x, a.y, za)], 'kaya_koyu', nn)
    # the river's cut face at the edge: water down to the bed
    if a.z < SU or b.z < SU:
        y.yuz_yon([V(a.x, a.y, min(a.z, SU)), V(b.x, b.y, min(b.z, SU)), V(b.x, b.y, SU), V(a.x, a.y, SU)], 'su', nn)

# ---------------- the river ----------------
y.bolum('Nehir')
NS = 24
for k in range(NS):
    ya, yb = GY0 + (GY1 - GY0) * k / NS, GY0 + (GY1 - GY0) * (k + 1) / NS
    xa, xb = nehir_x(ya), nehir_x(yb)
    w = 0.14
    y.yuz_yon([V(max(GX0, xa - w), ya, SU), V(xb - w if xb - w > GX0 else GX0, yb, SU), V(xb + w, yb, SU), V(xa + w, ya, SU)], 'su', Z)
pirogue(y, -0.95, 0.55, SU - 0.006, math.pi / 2 + 0.15, L=0.36, B=0.05, H=0.02, yuk=['kabak', 'cuval'], kurekci=('beyaz', 'boya_kirmizi'), tohum=2)
# the washers: women standing in the shallows swirling gravel in calabashes, others carrying it down
for k, (wx, wy, ga) in enumerate(((-0.8, -0.55, 'boya_kirmizi'), (-0.84, -0.3, 'boya_sari'), (-0.79, -0.05, 'kobalt'), (-0.86, 0.2, 'beyaz'))):
    zz = SU - 0.009
    kisi(y, wx, wy, zz, math.pi * 0.95, govde=ga, bas=('boya_sari', 'boya_kirmizi', 'beyaz', 'boya_kirmizi')[k], boy=0.054)
    donel(y, (wx - 0.016, wy + 0.002), [(0.0, zz + 0.016), (0.012, zz + 0.017), (0.019, zz + 0.024), (0.0185, zz + 0.026), (0.0, zz + 0.021)], 'boya_sari', n=10)
    donel(y, (wx - 0.016, wy + 0.002), [(0.0175, zz + 0.0255), (0.0, zz + 0.024)], 'kum_koyu', n=10)
# calabashes floating, gravel heaps on the bank
for gx, gy in ((-0.95, -0.42), (-0.9, -0.16), (-0.96, 0.06)):
    donel(y, (gx, gy), [(0.0, SU - 0.004), (0.012, SU - 0.003), (0.018, SU + 0.004), (0.0, SU + 0.002)], 'boya_sari', n=10)
for gx, gy in ((-0.62, -0.5), (-0.64, -0.12), (-0.6, 0.12)):
    yigin(y, gx, gy, yuk(gx, gy) - 0.004, r=0.05, h=0.03, key='kum_koyu', tohum=int(gx * 100 + gy * 10))
kisi(y, -0.62, -0.3, yuk(-0.62, -0.3), math.pi, govde='boya_sari', bas='boya_kirmizi', yuk='ahsap_acik')
oturan(y, -0.66, 0.0, yuk(-0.66, 0.0) - 0.002, math.pi, govde='boya_kirmizi', bas='beyaz')
donel(y, (-0.69, 0.0), [(0.0, yuk(-0.69, 0) + 0.004), (0.014, yuk(-0.69, 0) + 0.004), (0.02, yuk(-0.69, 0) + 0.012), (0.0, yuk(-0.69, 0) + 0.01)], 'boya_sari', n=10)
donel(y, (-0.69, 0.0), [(0.019, yuk(-0.69, 0) + 0.0115), (0.0, yuk(-0.69, 0) + 0.012)], 'altin', n=10)

# ---------------- the diggings ----------------
y.bolum('Ocaklar')
for k, (kx, ky) in enumerate(KUYULAR):
    a = rn.uniform(0, math.pi)
    cikrik(y, kx, ky, Z0, a, r=0.045, derin=0.09)
    # the spoil heap of red earth beside it
    ha = a + math.pi / 2 + rn.uniform(-0.4, 0.4)
    hx, hy = kx + math.cos(ha) * 0.13, ky + math.sin(ha) * 0.13
    yigin(y, hx, hy, Z0 - 0.004, r=rn.uniform(0.05, 0.07), h=rn.uniform(0.04, 0.06), key='kerpic_koyu', tohum=k, uzun=1.3, aci=ha)
    # a miner at the windlass
    ca, sa = math.cos(a), math.sin(a)
    mx, my = kx + ca * 0.075, ky + sa * 0.075
    kisi(y, mx - sa * 0.02, my + ca * 0.02, Z0, a + math.pi, govde=('beyaz', 'kumas', 'boya_sari')[k % 3], bas=('beyaz', 'boya_kirmizi')[k % 2], kol=0.6, sarik=k % 2 == 0)
    # a basket of ore at the rim
    sepet(y, kx - sa * 0.07, ky + ca * 0.07, Z0, 0.016, 0.014, dolu='kerpic_koyu')
# porters carrying baskets of ore to the river
for px_, py_, a in ((-0.3, -0.32, math.pi), (-0.48, -0.2, math.pi * 0.9), (0.05, -0.86, math.pi * 0.8)):
    kisi(y, px_, py_, Z0, a, govde=rn.choice(('boya_kirmizi', 'beyaz', 'boya_sari')), bas='beyaz', yuk='saz')
# crushing the ore: women pounding it in wooden mortars, sieving it onto mats
for k, (hx, hy) in enumerate(((0.2, -0.75), (0.32, -0.66), (-0.12, -0.96))):
    zz = Z0
    donel(y, (hx, hy), [(0.0, zz), (0.016, zz), (0.013, zz + 0.012), (0.012, zz + 0.026), (0.016, zz + 0.04), (0.0, zz + 0.04)], 'ahsap', n=10)
    donel(y, (hx, hy), [(0.0, zz + 0.0402), (0.012, zz + 0.0402), (0.0, zz + 0.0404)], 'kerpic_koyu', n=10)
    a = 0.8 + k
    kisi(y, hx + math.cos(a) * 0.03, hy + math.sin(a) * 0.03, zz, a + math.pi, govde=('boya_kirmizi', 'kobalt', 'boya_sari')[k], bas=('boya_sari', 'beyaz', 'boya_kirmizi')[k], kol=1.0, sarik=True)
    cubuk(y, V(hx + math.cos(a) * 0.012, hy + math.sin(a) * 0.012, zz + 0.03), V(hx + math.cos(a) * 0.022, hy + math.sin(a) * 0.022, zz + 0.11), 0.005, 'ahsap_acik')
    hasir(y, hx - math.cos(a) * 0.05, hy - math.sin(a) * 0.05, zz, 0.06, 0.05, a)
    yigin(y, hx - math.cos(a) * 0.05, hy - math.sin(a) * 0.05, zz + 0.003, r=0.018, h=0.012, key='kerpic_koyu', tohum=20 + k)
# scattered stones
for k in range(26):
    sx, sy = rn.uniform(-0.6, 1.1), rn.uniform(-1.12, 0.05)
    kure(y, (sx, sy, yuk(sx, sy) - 0.002), rn.uniform(0.006, 0.012), rn.choice(('kaya', 'kaya_koyu', 'kerpic_koyu')), n=6, kat=3)
# a timber pile and digging tools
for k in range(4):
    cubuk(y, V(0.5, -0.95 + k * 0.016, Z0 + 0.006), V(0.72, -0.93 + k * 0.016, Z0 + 0.006), 0.012, 'kutuk', 0.012)
for k in range(3):
    cubuk(y, V(0.52, -0.94 + k * 0.022, Z0 + 0.018), V(0.7, -0.925 + k * 0.022, Z0 + 0.018), 0.012, 'kutuk', 0.012)
for k in range(3):
    cubuk(y, V(0.76 + k * 0.012, -0.82, Z0), V(0.79 + k * 0.012, -0.8, Z0 + 0.07), 0.004, 'ahsap')
    donel(y, (0.792 + k * 0.012, -0.8), [(0.0, Z0 + 0.07), (0.006, Z0 + 0.072), (0.0, Z0 + 0.08)], 'demir', n=4)

# ---------------- the gold traders ----------------
y.bolum('Altin tuccarlari')
golgelik(y, -0.36, 0.3, yuk(-0.36, 0.3), 0.34, 0.22, 0.15, aci=0.0, mal=['altin', 'kola', 'altin', 'kumas'], tohum=3, ortu=('kumas', 'boya_kirmizi'))
hasir(y, -0.36, 0.12, yuk(-0.36, 0.12), 0.2, 0.08, 0.0)
oturan(y, -0.42, 0.13, yuk(-0.42, 0.13), -math.pi / 2, govde='beyaz', bas='beyaz')
oturan(y, -0.3, 0.13, yuk(-0.3, 0.13), -math.pi / 2, govde='boya_sari', bas='beyaz')
terazi(y, -0.36, 0.08, yuk(-0.36, 0.08) + 0.003, 0.0, 0.05)
mal_koy(y, 'altin', -0.27, 0.06, yuk(-0.27, 0.06) + 0.003)
# buyers with salt: camels loaded with slabs, slabs stacked for the exchange
kisi(y, -0.37, -0.02, yuk(-0.37, -0.02), math.pi / 2, govde='lacivert', bas='lacivert', boy=0.058)
kisi(y, -0.3, -0.03, yuk(-0.3, -0.03), math.pi / 2 + 0.3, govde='beyaz', bas='beyaz', boy=0.058)
tuz_levha(y, -0.2, 0.05, yuk(-0.2, 0.05), 0.3, n=4, tohum=1)
tuz_levha(y, -0.12, 0.08, yuk(-0.12, 0.08), -0.2, n=3, tohum=2)
deve(y, -0.08, 0.3, yuk(-0.08, 0.3), math.pi * 0.85, renk='ahsap_acik', yuk=True, olcek=1.0)
deve(y, -0.18, 0.5, yuk(-0.18, 0.5), math.pi * 0.95, renk='kum_koyu', yuk=False, cok=True, olcek=1.0)
tuareg(y, -0.02, 0.18, yuk(-0.02, 0.18), math.pi * 0.9)

# ---------------- the village ----------------
y.bolum('Koy')
VX0, VX1, VY0, VY1 = 0.06, 1.1, 0.12, 1.1
ZEMIN_Z[0] = Z0
kerpic_duvar(y, [V(VX0, VY1), V(VX0, VY0), V(0.44, VY0)], Z0, 0.09, KK, kapali=False, payanda=0.16)
kerpic_duvar(y, [V(0.62, VY0), V(VX1, VY0), V(VX1, VY1)], Z0, 0.09, KK, kapali=False, payanda=0.16)
# piers closing the wall ends (the gate's jambs)
for ex, ey in ((VX0, VY1), (0.44, VY0), (0.62, VY0), (VX1, VY1), (VX0, VY0), (VX1, VY0)):
    kose_payanda(y, (ex, ey), Z0 - 0.005, Z0 + 0.11, 0.055, KK, 0.06)
for hx, hy, r in ((0.22, 0.32, 0.075), (0.92, 0.32, 0.07), (0.2, 0.95, 0.075), (0.93, 0.92, 0.08)):
    kulube(y, hx, hy, yuk(hx, hy), r, 0.075, 0.09, K, kapi_aci=math.atan2(0.55 - hy, 0.55 - hx))
# granaries: small round mud bins on stone feet with thatch caps
for gx, gy in ((0.36, 0.98), (0.48, 1.0), (0.98, 0.56)):
    zg = yuk(gx, gy)
    for k in range(3):
        a = TAU * k / 3
        kutu_merkez(y, (gx + 0.025 * math.cos(a), gy + 0.025 * math.sin(a)), 0.018, 0.018, 0.02, 'kaya', z0=zg)
    donel(y, (gx, gy), [(0.03, zg + 0.02), (0.042, zg + 0.05), (0.038, zg + 0.08), (0.025, zg + 0.09)], K, n=12)
    donel(y, (gx, gy), [(0.052, zg + 0.082), (0.03, zg + 0.11), (0.0, zg + 0.135)], 'saz', n=12)
    y.yuz_yon([V(gx + 0.052 * math.cos(TAU * i / 12), gy + 0.052 * math.sin(TAU * i / 12), zg + 0.082) for i in range(12)], 'saz_koyu', -Z)
# the mine master's house
djenne_ev(y, 0.25, 0.64, 0.28, 0.22, 0.2, aci=-0.35, kat=2, z=yuk(0.25, 0.64))
# village life
kup_(y, 0.4, 0.3, Z0, 0.016, 0.04)
kup_(y, 0.44, 0.28, Z0, 0.013, 0.034, 'kerpic_koyu')
kisi(y, 0.5, 0.24, Z0, math.pi / 2 + 0.6, govde='boya_kirmizi', bas='boya_sari', yuk='kiremit')
oturan(y, 0.74, 0.3, Z0, math.pi / 2, govde='beyaz', bas='beyaz')
# outside: trees
baobab(y, 0.86, -0.25, Z0, boy=0.32, tohum=4)
akasya(y, -0.55, 0.85, yuk(-0.55, 0.85), boy=0.26, tohum=6)
akasya(y, 0.42, -0.6, Z0, boy=0.2, tohum=2)
palmiye(y, -0.62, 0.55, yuk(-0.62, 0.55), boy=0.28, tohum=3)
palmiye(y, -0.66, -0.78, yuk(-0.66, -0.78), boy=0.26, tohum=7)

# ---------------- the watchtower ----------------
y.bolum('Gozcu kulesi')
TX, TY, TW = 0.64, 0.7, 0.36
zb = yuk(TX, TY)
kose = dikdortgen(TX - TW / 2, TX + TW / 2, TY - TW / 2, TY + TW / 2)
sahel_kutu(y, kose, zb - 0.01, 0.22, K, kalin=0.03, dam=zb + 0.18,
           yanlar=[dict(n=3, acik={1: dict(tip='kapi', en=0.5, v0=0, v1=0.13, kemer=0.3)}),
                   dict(n=3, acik={1: dict(tip='pencere', en=0.34, v0=0.13, v1=0.18, kafes=True)}), dict(n=3),
                   dict(n=3, acik={1: dict(tip='pencere', en=0.34, v0=0.13, v1=0.18, kafes=True)})],
           kose_w=0.06, kose_tepe=0.08, kose_yumurta=True)
zt = sahel_minare(y, (TX + 0.02, TY + 0.02), 0.24, 0.17, zb + 0.18, 0.56, K, kaburga=2, toron_sira=6,
                  pencereler=((-Y, (0.3, 0.55, 0.8)), (-X, (0.45, 0.75))), ust=0.06, kose_w=0.045)
sancak(y, TX - 0.12, TY - 0.12, zb + 0.18, boy=0.24, en=0.12, yuk=0.075, aci=math.radians(210))
kisi(y, TX + 0.1, TY - 0.12, zb + 0.18, -math.pi / 2, govde='lacivert', bas='lacivert', mizrak='ahsap_koyu')

calistir(y, 'lm_altinmadeni')
