# Niger Market (lm_nijerpazari): a riverside market town of the inland Niger delta (Djenne / Mopti): Djenne mud
# houses with the Tukolor facade (great pilasters, the potige over the door, pinnacles, torons, grilled windows), a
# small mud mosque whose tapering minaret marks the skyline, thatched shades over stalls of Taghaza salt slabs, gold,
# kola nuts, cloth and calabashes, traders and porters, a caravan of camels unloading salt, and the river with a
# landing, pirogues (one under a reed awning) and boatmen.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mali_ortak import *
from arap_ortak import deve
import doku

y = Yapi()
Z0 = 0.035           # the market ground
ZS = 0.007           # the river's surface
ZB = -0.022          # the river bed
ZA = -0.035          # the bottom of the terrain block
X0, X1, Y0, Y1 = -1.12, 1.12, -1.02, 1.1


def kiyi(x):
    """the bank line (the land reaches down to the water about here)"""
    return 0.5 + 0.05 * math.sin(2.1 * x + 0.6) + 0.025 * math.sin(5.3 * x)


def yer_z(x, yy):
    t = min(1.0, max(0.0, (yy - (kiyi(x) - 0.09)) / 0.17))
    s = t * t * (3 - 2 * t)
    return Z0 + (ZB - Z0) * s


def arazi_renk(x, yy, z):
    """dusty market ground, a green strip along the bank, dark wet mud under the water"""
    g = 0.03 * math.sin(x * 9.1 + yy * 4.3) + 0.02 * math.sin(x * 23 - yy * 17)
    kuru = (0.79 + g, 0.67 + g, 0.5 + g * 0.8)
    if z < ZS:
        return (0.36, 0.3, 0.22)
    d = kiyi(x) - yy
    if d < 0.16:
        k = max(0.0, min(1.0, (0.16 - d) / 0.1))
        ot = (0.5 + g, 0.52 + g, 0.3)
        if z < ZS + 0.01:
            ot = (0.42, 0.36, 0.25)
        return tuple(kuru[i] + (ot[i] - kuru[i]) * k for i in range(3))
    return kuru


def su_renk(x, yy, z):
    """the brown-green Niger water: lighter at the bank, deeper towards the far side; the cut face darker"""
    if z < ZS - 0.001:
        return (0.2, 0.27, 0.25)
    d = min(1.0, max(0.0, (yy - kiyi(x)) / 0.5))
    g = 0.015 * math.sin(x * 11 + yy * 7)
    return (0.4 - 0.12 * d + g, 0.45 - 0.08 * d + g, 0.38 - 0.03 * d + g)


doku.KOSE_RENK['toprak_ot'] = arazi_renk
doku.KOSE_RENK['su'] = su_renk

# ---------------- the ground and the river ----------------
y.bolum('Arazi')
NX, NY = 36, 34
P = [[V(X0 + (X1 - X0) * i / NX, Y0 + (Y1 - Y0) * j / NY, 0) for j in range(NY + 1)] for i in range(NX + 1)]
for i in range(NX + 1):
    for j in range(NY + 1):
        P[i][j].z = yer_z(P[i][j].x, P[i][j].y)
for i in range(NX):
    for j in range(NY):
        dg = (i + j) % 2 == 0
        for tri in (([P[i][j], P[i + 1][j], P[i + 1][j + 1]], [P[i][j], P[i + 1][j + 1], P[i][j + 1]]) if dg else
                    ([P[i][j], P[i + 1][j], P[i][j + 1]], [P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]])):
            y.yuz(tri, 'toprak_ot')
kenar = [P[i][0] for i in range(NX)] + [P[NX][j] for j in range(NY)] + [P[i][NY] for i in range(NX, 0, -1)] + [P[0][j] for j in range(NY, 0, -1)]
for k in range(len(kenar)):
    a, b = kenar[k], kenar[(k + 1) % len(kenar)]
    e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
    y.yuz_yon([V(a.x, a.y, ZA), V(b.x, b.y, ZA), b, a], 'toprak', nn)
    if a.z < ZS or b.z < ZS:   # the water's cut face above the bed
        y.yuz_yon([V(a.x, a.y, min(a.z, ZS)), V(b.x, b.y, min(b.z, ZS)), V(b.x, b.y, ZS), V(a.x, a.y, ZS)], 'su', nn)
y.yuz_yon([V(X0, Y0, ZA), V(X1, Y0, ZA), V(X1, Y1, ZA), V(X0, Y1, ZA)], 'toprak', -Z)
# the water surface (from just under the bank to the far edge)
y.bolum('Nehir')
NW = 18
for i in range(NW):
    xa, xb = X0 + (X1 - X0) * i / NW, X0 + (X1 - X0) * (i + 1) / NW
    ya, yb_ = kiyi(xa) - 0.02, kiyi(xb) - 0.02
    for j in range(4):
        t0, t1 = j / 4, (j + 1) / 4
        q = [V(xa, ya + (Y1 - ya) * t0, ZS), V(xb, yb_ + (Y1 - yb_) * t0, ZS), V(xb, yb_ + (Y1 - yb_) * t1, ZS), V(xa, ya + (Y1 - ya) * t1, ZS)]
        y.yuz_yon(q, 'su', Z)

# ---------------- the landing ----------------
y.bolum('Iskele')
# a timber jetty on forked posts running into the water, and mud steps down the bank
jx = 0.18
jy0 = kiyi(jx) - 0.08
for k in range(7):
    yy = jy0 + 0.035 * k
    kutu_merkez(y, (jx, yy), 0.1, 0.03, 0.006, 'ahsap_acik' if k % 2 else 'ahsap', z0=Z0 + 0.004 - 0.001 * k, aci=0.02 * (k % 3 - 1))
for k in range(4):
    yy = jy0 + 0.06 + 0.055 * k
    for s in (-1, 1):
        cubuk(y, V(jx + s * 0.045, yy, ZB), V(jx + s * 0.045, yy, Z0 + 0.008), 0.007, 'kutuk')
for k in range(4):
    kutu_merkez(y, (jx - 0.12, kiyi(jx - 0.12) - 0.1 + 0.04 * k), 0.08, 0.04, max(0.004, yer_z(jx - 0.12, kiyi(jx - 0.12) - 0.1 + 0.04 * k) - ZB + 0.004),
                KK, z0=ZB)

# ---------------- pirogues ----------------
y.bolum('Pirogue')
pirogue(y, -0.55, 0.78, ZS - 0.006, 0.12, L=0.52, B=0.064, tente=True, yuk=['cuval', 'kup', 'cuval'], kurekci=('boya_kirmizi', 'beyaz'), tohum=1)
pirogue(y, 0.48, 0.9, ZS - 0.006, -0.08, L=0.46, B=0.058, bantlar=('boya_yesil', 'boya_sari'), yuk=['tuz', 'tuz'], kurekci=('beyaz', 'kobalt'), tohum=2)
pirogue(y, 0.26, 0.6, ZS - 0.006, 1.45, L=0.36, B=0.052, bantlar=('boya_kirmizi', 'beyaz'), yuk=['kabak'], tohum=3)
pirogue(y, -0.12, 0.62, ZS - 0.007, 1.75, L=0.34, B=0.05, bantlar=('boya_sari', 'boya_kirmizi'), tohum=4)
pirogue(y, 0.92, 0.66, ZS - 0.006, 0.6, L=0.32, B=0.048, bantlar=('beyaz', 'boya_kirmizi'), kurekci=('kumas', 'beyaz'), tohum=5)

# ---------------- the mosque ----------------
y.bolum('Cami')
MX0, MX1, MY0, MY1 = -1.02, -0.52, -0.06, 0.34
MH = 0.2
DAM = Z0 + MH - 0.03
yan = [dict(n=5, acik={1: dict(tip='kapi', en=0.5, v1=0.13, kemer=0.3), 3: dict(tip='kapi', en=0.5, v1=0.13, kemer=0.3)}),
       dict(n=4, acik={1: dict(tip='pencere', en=0.32, v0=0.08, v1=0.13, kafes=True), 2: dict(tip='kapi', en=0.5, v1=0.13, kemer=0.3)}),
       dict(n=5), dict(n=4)]
sahel_kutu(y, dikdortgen(MX0, MX1, MY0, MY1), Z0, MH, K, kalin=0.03, dam=DAM, yanlar=yan, payanda_w=0.03, payanda_d=0.022,
           payanda_tepe=0.045, kose_w=0.06, kose_tepe=0.075, kose_ust=0.035, payanda_ust=0.025, kademe=True)
for i in range(3):
    for j in range(2):
        fener(y, MX0 + 0.12 + 0.12 * i, MY0 + 0.14 + 0.13 * j, DAM, 0.036)
for k in range(3):
    oluk(y, V(MX0 + 0.1 + 0.15 * k, MY1), V(0, 1), Z0 + MH - 0.01, 0.045)
    oluk(y, V(MX0, MY0 + 0.08 + 0.12 * k), V(-1, 0), Z0 + MH - 0.01, 0.045)
# the minaret rises from the middle of the court front, a smaller conical one on the qibla (east) end
sahel_minare(y, (-0.77, MY0 - 0.04), 0.2, 0.13, Z0, 0.66, K, kaburga=2, toron_sira=7, pencereler=((-Y, (0.35, 0.6)), (-X, (0.5,))),
             ust=0.06, kapi=-Y)
mc = (MX1 + 0.004, (MY0 + MY1) / 2)
donel(y, mc, [(0.075, Z0), (0.068, Z0 + 0.12), (0.05, Z0 + 0.22), (0.025, Z0 + 0.28), (0.0, Z0 + 0.3)], K, n=12)
kure(y, (mc[0], mc[1], Z0 + 0.308), 0.01, 'beyaz', n=8, kat=4)
for k in range(3):
    for t in (-2, -1, 0, 1, 2):
        a = t * 0.42; zz = Z0 + 0.05 + 0.07 * k
        rr = 0.075 - 0.25 * (zz - Z0)
        toron(y, V(mc[0], mc[1]) + V(math.cos(a), math.sin(a)) * (rr - 0.002) + Z * zz, V(math.cos(a), math.sin(a)), 0.02)

# ---------------- the houses ----------------
y.bolum('Evler')
djenne_ev(y, -0.74, -0.68, 0.38, 0.3, 0.32, 0.0, kat=2, tukolor=True, z=Z0)
sancak(y, -0.62, -0.6, Z0 + 0.32 - 0.03 + 0.075, boy=0.22, en=0.11, yuk=0.07, aci=math.pi * 0.85)
djenne_ev(y, -0.95, -0.33, 0.22, 0.28, 0.2, math.pi / 2 * 0 - math.pi / 2, kat=1, tukolor=False, ust_oda=False, z=Z0)
djenne_ev(y, 0.82, 0.08, 0.36, 0.3, 0.3, -math.pi / 2, kat=2, tukolor=True, z=Z0)
djenne_ev(y, 0.86, -0.42, 0.3, 0.26, 0.21, -math.pi / 2, kat=1, tukolor=False, ust_oda=False, z=Z0)
djenne_ev(y, 0.84, -0.8, 0.28, 0.24, 0.2, -math.pi / 2, kat=1, tukolor=False, ust_oda=False, z=Z0)
# a low mud wall closing the yard behind the corner house, with a doorway
sahel_kutu(y, dikdortgen(0.64, 0.98, 0.28, 0.42), Z0, 0.1, KT, kalin=0.022, dam=None,
           yanlar=[dict(n=3), dict(n=1), dict(n=3), dict(n=1)], payanda_w=0.022, payanda_d=0.014, payanda_tepe=0.03,
           kose_w=0.034, kose_tepe=0.04, kose_ust=0.02, payanda_ust=0.012, toron_sira=(0.6,))

# ---------------- the stalls ----------------
y.bolum('Tezgahlar')
tez = [((-0.3, -0.62), ['tuz', 'tuz']), ((0.02, -0.66), ['altin', 'kola']), ((0.34, -0.62), ['kumas', 'kumas']),
       ((-0.24, -0.28), ['kabak', 'sepet', 'kup']), ((0.1, -0.3), ['balik', 'tahil']), ((0.42, -0.26), ['kola', 'kabak']),
       ((-0.12, 0.04), ['tahil', 'sepet']), ((0.26, 0.06), ['tuz', 'kumas'])]
for k, ((tx, ty), mal) in enumerate(tez):
    ORTU = [('saz',), ('boya_kirmizi', 'beyaz'), ('saz',), ('boya_sari', 'kumas'), ('saz_koyu', 'saz'), ('saz',), ('boya_yesil', 'beyaz'), ('saz',)]
    golgelik(y, tx, ty, Z0, 0.24, 0.17, 0.13, aci=0.06 * ((k * 7) % 5 - 2), mal=mal, tohum=k, ortu=ORTU[k])
# goods spread on mats on the ground
for k, (mx, my, a, mal) in enumerate(((-0.4, -0.95, 0.1, ('kup', 'kup')), (0.12, -0.92, -0.05, ('kabak', 'sepet')), (0.33, -0.9, 0.0, ('balik', 'tahil')),
                                       (0.56, 0.26, 0.3, ('kup', 'kabak')))):
    hasir(y, mx, my, Z0, 0.17, 0.08, a)
    for j, m in enumerate(mal):
        mal_koy(y, m, mx - 0.045 + 0.09 * j, my, Z0 + 0.003)

# ---------------- people ----------------
y.bolum('Insanlar')
rng = random.Random(4)
ROBA = ['boya_kirmizi', 'boya_sari', 'beyaz', 'kobalt', 'lacivert', 'boya_yesil', 'kumas', 'turuncu', 'beyaz', 'mor']
BAS = ['beyaz', 'boya_sari', 'boya_kirmizi', 'beyaz', 'kobalt', 'turuncu']
# traders sitting behind their stalls
for k, ((tx, ty), mal) in enumerate(tez):
    oturan(y, tx + 0.02, ty + 0.05, Z0 + 0.03, -math.pi / 2, ROBA[k % len(ROBA)], BAS[k % len(BAS)])
for k, (mx, my, a, mal) in enumerate(((-0.4, -0.95, 0.1, 0), (0.12, -0.92, -0.05, 0), (0.33, -0.9, 0.0, 0))):
    oturan(y, mx, my + 0.065, Z0, -math.pi / 2, ROBA[(k + 3) % len(ROBA)], BAS[(k + 2) % len(BAS)])
# buyers and passers-by, women with loads on their heads
for k, (px, py) in enumerate(((-0.16, -0.48), (0.18, -0.47), (0.5, -0.45), (-0.05, -0.8), (0.2, -0.8), (-0.42, -0.45), (0.0, -0.14),
                              (0.4, -0.08), (-0.35, -0.08), (0.62, -0.62), (-0.55, -0.4), (0.58, 0.42), (-0.18, 0.24), (0.08, 0.3))):
    yuk = rng.choice([None, None, 'kabak', 'saz', 'kiremit']) if k % 2 else None
    kisi(y, px, py, Z0, rng.uniform(0, TAU), rng.choice(ROBA), rng.choice(BAS), yuk={'kabak': 'boya_sari'}.get(yuk, yuk),
         kol=0.6 if k % 5 == 0 else 0.0)
# porters carrying sacks up from the landing
for k in range(3):
    py = kiyi(jx) - 0.16 - 0.09 * k
    kisi(y, jx + 0.02 * (k - 1), py, Z0, -math.pi / 2, ('kumas', 'beyaz', 'boya_sari')[k], 'beyaz', yuk='saz')

# ---------------- the caravan ----------------
y.bolum('Kervan')
deve(y, -0.34, -0.8, Z0, 0.15, renk='ahsap_acik', yuk=True, olcek=1.0)
deve(y, -0.08, -0.92, Z0, -0.1, renk='kum_koyu', yuk=False, cok=True, olcek=1.0)
deve(y, 0.6, -0.98, Z0, math.pi * 0.95, renk='ahsap_acik', yuk=True, cul='boya_sari', olcek=1.0)
kisi(y, -0.2, -0.98, Z0, 0.3, 'kobalt', 'kobalt', mizrak='ahsap')    # a Tuareg caravaneer, veiled in indigo
for k in range(2):
    mal_koy(y, 'tuz', -0.2 + 0.0 * k, -0.86 + 0.04 * k, Z0 + 0.0)

# ---------------- trees ----------------
y.bolum('Agaclar')
palmiye(y, -0.22, 0.43, yer_z(-0.22, 0.43), boy=0.3, tohum=1)
palmiye(y, 0.02, 0.4, yer_z(0.02, 0.4), boy=0.25, tohum=2)
palmiye(y, 0.62, 0.47, yer_z(0.62, 0.47), boy=0.28, tohum=3)
akasya(y, 0.62, -0.14, Z0, boy=0.22, tohum=4)
baobab(y, -0.32, 0.25, Z0, boy=0.34, tohum=2)

calistir(y, 'lm_nijerpazari')
