# Byrsa Sarayı (lm_byrsa): the citadel hill of Carthage. Three terraces held by buttressed retaining walls, the long
# stair of sixty steps climbing straight up to the walled summit; there the temple of Eshmun on its podium (an Ionic
# porch, cavetto cornices, stepped Phoenician merlons, the winged sun over a bronze door), the two free-standing pillars
# before it and the altar; on the middle terrace the Punic palace round a peristyle court (an upper loggia, a belvedere
# tower); tall whitewashed houses on the lower terrace and at the foot of the hill, gardens, cypresses and palms.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir
from kartaca_ortak import *

y = Yapi()
D = math.radians
Z0 = 0.03
X0, X1, Y0, Y1 = -1.15, 1.15, -1.15, 1.15
T1 = (-1.0, 1.0, -0.78, 1.05, 0.13)        # terrace rectangles and their top levels
T2 = (-0.86, 0.86, -0.48, 0.95, 0.26)
T3 = (-0.15, 0.7, -0.15, 0.86, 0.40)
SX = 0.275                                  # the stair's axis
SW = 0.1                                    # its half width (between the cheeks)
SY0, SY1 = -1.12, T3[2]                     # the stair's foot and top
KUM, KUMK, KUMA = 'kum', 'kum_koyu', 'kum_acik'
SIV = 'siva'


def stair_z(yy):
    t = (yy - SY0) / (SY1 - SY0)
    return Z0 + (T3[4] - Z0) * min(1.0, max(0.0, t))


# ================================================================ the ground and the terraces
y.bolum('Zemin ve teraslar')
kutu(y, V(X0, Y0, 0), X, X1 - X0, Y1 - Y0, Z0, 'kaya', 'onarkasagsol')


def halka_ust(dis, ic, z, key):
    """the top of a terrace between its outline and the next terrace's (both rectangles x0, x1, y0, y1)"""
    A = dikdortgen(dis[0], dis[1], dis[2], dis[3], z); B = dikdortgen(ic[0], ic[1], ic[2], ic[3], z)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([A[i], A[j], B[j], B[i]], key, Z)


def istinat(t, z_alt, key=KUM, payanda=0.16, kes=None):
    """a terrace's retaining wall from z_alt up to its top: battered faces in courses, buttresses, a coping;
    kes: (x0, x1) left open on the front side (the stair)"""
    x0, x1, y0, y1, zt = t
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        parcalar_ = [(a, b)]
        if i == 0 and kes:
            parcalar_ = [(a, V(kes[0], y0)), (V(kes[1], y0), b)]
        for p, q in parcalar_:
            duz_duvar(y, p, q, z_alt, zt, key)
            silme(y, [p, q], zt - 0.012, 0.012, 0.007, KUMA, 'tac', kapali=False)
            silme(y, [p, q], z_alt, 0.014, 0.008, KUMK, 'kaide', kapali=False)
            L = (q - p).length; e = (q - p) / L; nn = V(e.y, -e.x)
            m = int(L / payanda)
            for j in range(1, m):
                c = p + e * (L * j / m) + nn * 0.01
                kutu_merkez(y, (c.x, c.y), 0.026, 0.02, zt - 0.012 - z_alt - 0.014, key, z0=z_alt + 0.014, aci=math.atan2(e.y, e.x),
                            yuzler='onarkasagsolust')


istinat(T1, Z0, kes=(SX - SW - 0.03, SX + SW + 0.03))
istinat(T2, T1[4], kes=(SX - SW - 0.03, SX + SW + 0.03))
istinat(T3, T2[4], kes=(SX - SW - 0.03, SX + SW + 0.03))
halka_ust((X0, X1, Y0, Y1), T1[:4], Z0, 'toprak_ot')
halka_ust(T1[:4], T2[:4], T1[4], 'zemin')
halka_ust(T2[:4], T3[:4], T2[4], 'zemin')
y.yuz_yon(dikdortgen(T3[0], T3[1], T3[2], T3[3], T3[4]), 'zemin', Z)

# ================================================================ the stair of sixty steps
y.bolum('Altmış basamak')
N = 60
dy = (SY1 - SY0) / N
for k in range(N):
    ya, yb = SY0 + dy * k, SY0 + dy * (k + 1)
    za, zb = stair_z(ya), stair_z(yb)
    y.yuz_yon([V(SX - SW, ya, za), V(SX + SW, ya, za), V(SX + SW, ya, zb), V(SX - SW, ya, zb)], KUMA, -Y)    # riser
    y.yuz_yon([V(SX - SW, ya, zb), V(SX + SW, ya, zb), V(SX + SW, yb, zb), V(SX - SW, yb, zb)], 'tas' if k % 10 else KUMA, Z)   # tread
# the cheek walls: sloping parapets either side with plinths at each terrace line
CW = 0.03
for s in (-1, 1):
    xi, xo = SX + s * SW, SX + s * (SW + CW)
    ca, cb = V(xi, SY0), V(xi, SY1)
    top = lambda yy: stair_z(yy) + 0.035
    alt = lambda yy: stair_z(yy) - 0.02
    # (the inner face from below the steps up to the parapet top; the outer face from the ground / terrace up)
    pts_i = [V(xi, SY0, Z0), V(xi, SY1, alt(SY1)), V(xi, SY1, top(SY1)), V(xi, SY0, top(SY0))]
    y.yuz_yon(pts_i, KUM, V(-s, 0, 0))
    y.yuz_yon([V(xo, SY0, Z0 - 0.002), V(xo, SY1, Z0 - 0.002), V(xo, SY1, top(SY1)), V(xo, SY0, top(SY0))], KUM, V(s, 0, 0))
    y.yuz_yon([V(xi, SY0, top(SY0)), V(xo, SY0, top(SY0)), V(xo, SY1, top(SY1)), V(xi, SY1, top(SY1))], KUMA, Z + V(0, -0.4, 0))
    y.yuz_yon([V(xi, SY0, Z0), V(xo, SY0, Z0 - 0.002), V(xo, SY0, top(SY0)), V(xi, SY0, top(SY0))], KUM, -Y)
    # newel blocks where the stair crosses the terrace edges, and bronze lamp stands on them
    for yy in (T1[2], T2[2], SY0 + 0.02):
        zz = top(yy)
        kutu_merkez(y, (SX + s * (SW + CW / 2), yy), CW + 0.016, 0.05, 0.03, KUMA, z0=zz - 0.012)
        kavetto(y, dikdortgen(SX + s * (SW + CW / 2) - CW / 2 - 0.008, SX + s * (SW + CW / 2) + CW / 2 + 0.008, yy - 0.025, yy + 0.025), zz + 0.018, 0.012,
                0.006, KUMA)
        donel(y, (SX + s * (SW + CW / 2), yy), [(0.004, zz + 0.03), (0.003, zz + 0.06), (0.01, zz + 0.064), (0.0, zz + 0.07)], 'bronz', n=6)
# the stair's foot: a paved forecourt
y.yuz_yon([V(SX - 0.2, -1.15, Z0 + 0.002), V(SX + 0.2, -1.15, Z0 + 0.002), V(SX + 0.2, SY0, Z0 + 0.002), V(SX - 0.2, SY0, Z0 + 0.002)], 'zemin', Z)

# ================================================================ the summit: citadel wall, gate, pillars, temple
y.bolum('Akropol suru ve kapı')
x0, x1, y0, y1, z3 = T3
for a, b in (((SX + SW + 0.06, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0)), ((x0, y0), (SX - SW - 0.06, y0))):
    sur(y, [V(*a), V(*b)], z3, 0.075, 0.035, KUM, mazgal_h=0.02, parapet_h=0.01, ust_key='zemin')
for (tx, ty) in ((x0 + 0.06, y0 + 0.06), (x1 - 0.06, y0 + 0.06), (x1 - 0.06, y1 - 0.06), (x0 + 0.06, y1 - 0.06)):
    kutu(y, V(tx - 0.06, ty - 0.06, z3), X, 0.12, 0.12, 0.14, KUM, 'onarkasagsol')
    kk = dikdortgen(tx - 0.06, tx + 0.06, ty - 0.06, ty + 0.06)
    kavetto(y, kk, z3 + 0.14, 0.03, 0.018, KUMA)
    parapet(y, disa(kk, 0.018), z3 + 0.17, 0.008, 0.02, 0.01, KUM)
    for i in range(4):
        a, b = kk[i], kk[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        yarik(y, a, e, nn, 0.055, z3 + 0.07, 0.01, 0.04, 'koyu')
# the gate at the stair's head: two pylons with cavetto cornices and the winged sun on the lintel
for s in (-1, 1):
    gx = SX + s * (SW + 0.06)
    kutu(y, V(gx - 0.05, y0 - 0.03, z3), X, 0.1, 0.07, 0.16, KUMA, 'onarkasagsol')
    kk = dikdortgen(gx - 0.05, gx + 0.05, y0 - 0.03, y0 + 0.04)
    kavetto(y, kk, z3 + 0.16, 0.03, 0.016, KUMA)
    silme(y, kk, z3, 0.016, 0.008, KUMK, 'kaide')
    tanit_kabartma(y, V(gx, y0 - 0.03, z3 + 0.06), X, -Y, 0.05, 'altin', d=0.002)
kutu(y, V(SX - SW - 0.01, y0 - 0.025, z3 + 0.12), X, 2 * SW + 0.02, 0.06, 0.04, KUMA, 'onarkasagsolust')
y.yuz_yon(dikdortgen(SX - SW - 0.01, SX + SW + 0.01, y0 - 0.025, y0 + 0.035, z3 + 0.12), KUMK, -Z)
kanatli_gunes(y, V(SX, y0 - 0.025, z3 + 0.14), X, -Y, 0.16, 0.03)

y.bolum('Eşmun tapınağı')
TPX0, TPX1, TPY0, TPY1 = SX - 0.2, SX + 0.2, 0.1, 0.72
ZP = z3 + 0.07
kutu(y, V(TPX0, TPY0, z3), X, TPX1 - TPX0, TPY1 - TPY0, ZP - z3, KUM, 'onarkasagsol')
kp = dikdortgen(TPX0, TPX1, TPY0, TPY1)
silme(y, kp, z3, 0.018, 0.01, KUMK, 'kaide')
kavetto(y, kp, ZP - 0.022, 0.022, 0.012, KUMA)
merdiven(y, (SX, TPY0 - 0.084), D(90), 0.2, z3, ZP, n=7, d=0.012, key=KUMA, yanlik=KUM)
# the cella
CX0, CX1, CY0, CY1 = SX - 0.155, SX + 0.155, 0.27, 0.68
HC = 0.26
kc = dikdortgen(CX0, CX1, CY0, CY1)
for i in range(1, 4):
    duz_duvar(y, kc[i], kc[(i + 1) % 4], ZP, ZP + HC, KUMA)
# the front wall with the door: a bronze door in a stepped frame, the winged sun over it
dikdortgen_acik(y, V(CX0, CY0), V(CX1, CY0), ZP, HC, 0.36, 0.64, 0.0, HC * 0.64, (KUMA, KUM, KUMA, 'bronz'), derin=0.02, cerceve=(0.012, KUM), ic_kenar=True)
kanatli_gunes(y, V(SX, CY0 - 0.0025, ZP + HC * 0.76), X, -Y, 0.2, 0.034)
silme(y, kc, ZP, 0.016, 0.008, KUM, 'kaide')
# antae and pilasters
for (px, py) in ((CX0, CY0), (CX1, CY0), (CX1, CY1), (CX0, CY1)):
    kutu_merkez(y, (px, py), 0.03, 0.03, HC - 0.016, KUM, z0=ZP + 0.016)
for i in (1, 2, 3):
    a, b = kc[i], kc[(i + 1) % 4]
    for j in range(1, 4 if i != 2 else 5):
        c = a.lerp(b, j / (4 if i != 2 else 5))
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        c = c + nn * 0.005
        kutu_merkez(y, (c.x, c.y), 0.02, 0.012, HC - 0.03, KUM, z0=ZP + 0.016, aci=math.atan2(e.y, e.x))
# the porch: four Ionic columns, the entablature, one cavetto cornice round porch and cella
PY = 0.15
for j in range(4):
    sutun(y, SX - 0.135 + 0.09 * j, PY, ZP, ZP + HC - 0.04, 0.016, KUMA, 'iyon', yiv=12)
kutu(y, V(CX0 - 0.015, PY - 0.022, ZP + HC - 0.04), X, CX1 - CX0 + 0.03, CY0 - PY + 0.022, 0.04, KUMA, 'onsagsol')
y.yuz_yon(dikdortgen(CX0 - 0.015, CX1 + 0.015, PY - 0.022, CY0, ZP + HC - 0.04), KUMK, -Z)
for j in range(10):   # rosettes on the frieze
    c = V(CX0 + 0.02 + (CX1 - CX0 - 0.04) * j / 9, PY - 0.022, ZP + HC - 0.018)
    prizma2(y, [(0.006 * math.cos(TAU * i / 8), 0.006 * math.sin(TAU * i / 8)) for i in range(8)], lambda u, v, d: c + X * u + Z * v - Y * d, 0.002,
            'boya_kirmizi' if j % 2 else 'altin', -Y)
kt = dikdortgen(CX0 - 0.015, CX1 + 0.015, PY - 0.022, CY1 + 0.015)
for a, b in ((V(CX1 + 0.015, CY0), V(CX1 + 0.015, CY1 + 0.015)), (V(CX1 + 0.015, CY1 + 0.015), V(CX0 - 0.015, CY1 + 0.015)),
             (V(CX0 - 0.015, CY1 + 0.015), V(CX0 - 0.015, CY0))):
    duz_duvar(y, a, b, ZP + HC - 0.04, ZP + HC, KUMA)
    # the frieze continues round the sides and the back: red and gilt rosettes, a painted band below them
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    silme(y, [a, b], ZP + HC - 0.042, 0.006, 0.003, 'boya_kirmizi', 'duz', kapali=False)
    for j in range(int(L / 0.045)):
        c = a + e * (L * (j + 0.5) / int(L / 0.045)) + Z * (ZP + HC - 0.018)
        prizma2(y, [(0.006 * math.cos(TAU * i / 8), 0.006 * math.sin(TAU * i / 8)) for i in range(8)],
                lambda u, v, d, c=c, e=e, nn=nn: c + e * u + Z * v + nn * d, 0.002, 'boya_kirmizi' if j % 2 else 'altin', nn)
ZC = ZP + HC
kavetto(y, kt, ZC, 0.04, 0.022, KUMA)
ZR = ZC + 0.04


def basamakli_mazgal(a, b, z, h, kal=0.016, key=KUMA):
    """Phoenician stepped merlons along a->b (outer face on the line, facing right): each a three-stepped block"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    w = h * 1.3; g = h * 0.55
    m = max(1, int((L + g) / (w + g)))
    w = (L + g) / m - g
    for i in range(m):
        u = i * (w + g)
        for k in range(3):
            ww = w * (1 - 0.3 * k)
            kutu(y, a + e * (u + (w - ww) / 2) - nn * (0.0005 * k) + Z * (z + h * k / 3), e, ww, kal - 0.001 * k, h / 3 + 0.0005, key)


for i in range(4):
    a, b = kt[i], kt[(i + 1) % 4]
    o = disa([a, b], 0.022, kapali=False)
    basamakli_mazgal(o[0], o[1], ZR, 0.036)
# acroteria and incense altars on the roof's corners, a banner
for p_ in kt:
    pp = V(SX, (PY + CY1) / 2) + (V(p_.x, p_.y) - V(SX, (PY + CY1) / 2)) * 0.92
    kutu_merkez(y, (pp.x, pp.y), 0.03, 0.03, 0.03, KUMA, z0=ZR)
    donel(y, (pp.x, pp.y), [(0.012, ZR + 0.03), (0.008, ZR + 0.04), (0.014, ZR + 0.05), (0.0, ZR + 0.052)], 'bronz', n=6)
tanit_heykel(y, SX, PY - 0.005, ZR + 0.004, 0.08, 'altin', aci=D(-90))
# the raised roof over the holy of holies (adyton) at the back, with its own cavetto and merlons
AX0, AX1, AY0, AY1 = SX - 0.1, SX + 0.1, CY0 + 0.12, CY1 - 0.03
kutu(y, V(AX0, AY0, ZR), X, AX1 - AX0, AY1 - AY0, 0.06, KUMA, 'onarkasagsol')
ka = dikdortgen(AX0, AX1, AY0, AY1)
for i in range(4):
    a, b = ka[i], ka[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    L = (b - a).length
    for j in range(int(L / 0.05)):
        pencere_kutu(y, a, e, nn, L * (j + 0.5) / int(L / 0.05) - 0.006, ZR + 0.018, 0.012, 0.026, 'koyu')
kavetto(y, ka, ZR + 0.06, 0.025, 0.014, KUMA)
for i in range(4):
    a, b = ka[i], ka[(i + 1) % 4]
    o = disa([a, b], 0.014, kapali=False)
    basamakli_mazgal(o[0], o[1], ZR + 0.085, 0.026, kal=0.012)
sancak(y, SX + 0.12, CY1 - 0.05, ZR, boy=0.22, en=0.11, yuk=0.065, aci=D(150))

y.bolum('İki sütun, sunak')
for s, key, bant in ((-1, 'altin', 'turkuaz'), (1, 'turkuaz', 'altin')):
    px, py = SX + s * 0.17, -0.02
    kutu_merkez(y, (px, py), 0.07, 0.07, 0.04, KUM, z0=z3)
    kavetto(y, dikdortgen(px - 0.035, px + 0.035, py - 0.035, py + 0.035), z3 + 0.04, 0.012, 0.008, KUMA)
    sutun(y, px, py, z3 + 0.052, z3 + 0.3, 0.02, key, 'misir', bas_key='altin', bant_key=bant)
    kure(y, (px, py, z3 + 0.322), 0.022, 'altin', n=10, kat=5)
# the altar: stepped, with its fire
for k, w in enumerate((0.1, 0.075)):
    kutu_merkez(y, (SX, 0.04), w, w * 0.8, 0.02 * (k + 1), KUM if k == 0 else KUMA, z0=z3)
kavetto(y, dikdortgen(SX - 0.034, SX + 0.034, 0.04 - 0.027, 0.04 + 0.027), z3 + 0.04, 0.012, 0.006, KUMA)
donel(y, (SX, 0.04), [(0.018, z3 + 0.052), (0.012, z3 + 0.066), (0.0, z3 + 0.09)], 'boya_sari', n=6)
donel(y, (SX, 0.04), [(0.009, z3 + 0.054), (0.0, z3 + 0.076)], 'boya_kirmizi', n=5)

# ================================================================ the palace on the middle terrace
y.bolum('Saray')
PX0, PX1, PY0_, PY1_ = -0.82, -0.22, -0.12, 0.72
z2 = T2[4]
HP = 0.2
CXA, CXB, CYA, CYB = -0.68, -0.36, 0.06, 0.52              # the court
ko = dikdortgen(PX0, PX1, PY0_, PY1_)
ki = dikdortgen(CXA, CXB, CYA, CYB)
# outer walls with two rows of windows, the front (-y) with a door below and an open loggia above
for i in range(4):
    a, b = ko[i], ko[(i + 1) % 4]
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    if i == 0:
        duz_duvar(y, a, b, z2, z2 + HP * 0.5, SIV)
        m = 8
        for j in range(m + 1):   # the loggia's columns
            p = a.lerp(b, 0.06 + 0.88 * j / m) + nn * 0.004
            iyon_hafif(y, p.x, p.y, z2 + HP * 0.5, z2 + HP - 0.012, 0.007, SIV, 'siva_krem', n=6, aci=-math.pi / 2)
        # the loggia's back wall, its floor and ceiling, its end walls
        ab, bb = a + V(0, 0.045), b + V(0, 0.045)
        duz_duvar(y, ab, bb, z2 + HP * 0.5, z2 + HP, 'siva_krem')
        for j in range(m):
            q = ab.lerp(bb, (j + 0.5) / m)
            pencere_kutu(y, q, X, -Y, -0.009, z2 + HP * 0.52, 0.018, HP * 0.3, 'koyu', cerceve='kum_acik')
        y.yuz_yon(dikdortgen(a.x, b.x, a.y, ab.y, z2 + HP * 0.5), 'boya_kirmizi', Z)
        y.yuz_yon(dikdortgen(a.x, b.x, a.y, ab.y, z2 + HP - 0.012), 'ahsap_koyu', -Z)
        duz_duvar(y, a, ab, z2 + HP * 0.5, z2 + HP, SIV)   # (the loggia's ends face in)
        duz_duvar(y, bb, b, z2 + HP * 0.5, z2 + HP, SIV)
        kutu(y, a + Z * (z2 + HP - 0.012), e, L, 0.045, 0.012, 'siva_krem', 'onsagsol')
        silme(y, [a, b], z2 + HP * 0.5 - 0.006, 0.008, 0.006, 'siva_krem', 'duz', kapali=False)
        # the gate: a tall door with a cavetto hood
        c = a.lerp(b, 0.5)
        pencere_kutu(y, c, e, nn, -0.025, z2, 0.05, 0.075, 'ahsap_koyu', cerceve=KUMA)
        silme(y, [c - e * 0.04, c + e * 0.04], z2 + 0.083, 0.016, 0.012, KUMA, KAVETTO, kapali=False)
        for j in range(6):
            if j in (2, 3): continue
            pencere_kutu(y, a, e, nn, L * (j + 0.5) / 6 - 0.008, z2 + HP * 0.22, 0.016, 0.03, 'koyu', cerceve='kum_acik')
    else:
        duz_duvar(y, a, b, z2, z2 + HP, SIV)
        m = max(1, int(L / 0.07))
        for j in range(m):
            for v in (0.22, 0.66):
                pencere_kutu(y, a, e, nn, L * (j + 0.5) / m - 0.008, z2 + HP * v, 0.016, 0.03, 'koyu', cerceve='kum_acik' if v > 0.5 else None)
        silme(y, [a, b], z2 + HP * 0.5 - 0.006, 0.008, 0.006, 'siva_krem', 'duz', kapali=False)
silme(y, ko, z2, 0.014, 0.008, KUM, 'kaide')
kavetto(y, ko, z2 + HP, 0.03, 0.018, 'siva_krem', ust=False)
# the roof: a terrace between the outer and the court walls, with a low parapet
ZPR = z2 + HP + 0.03
halka_ust((PX0, PX1, PY0_, PY1_), (CXA - 0.06, CXB + 0.06, CYA - 0.06, CYB + 0.06), ZPR, 'siva_krem')
parapet(y, disa(ko, 0.018), ZPR, 0.012, 0.0, 0.008, SIV)
# the court: walls facing in, a colonnade on all four sides under a tiled lean-to roof, a pool, a Tanit mosaic
kr = dikdortgen(CXA - 0.06, CXB + 0.06, CYA - 0.06, CYB + 0.06)
for i in range(4):   # the court-facing walls (wound inward)
    a, b = kr[(i + 1) % 4], kr[i]
    duz_duvar(y, a, b, z2, ZPR, SIV)
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    m = max(1, int(L / 0.07))
    for j in range(m):
        pencere_kutu(y, a, e, nn, L * (j + 0.5) / m - 0.008, z2 + HP * 0.68, 0.016, 0.028, 'koyu')
        pencere_kutu(y, a, e, nn, L * (j + 0.5) / m - 0.01, z2, 0.02, 0.05, 'koyu')
y.yuz_yon(dikdortgen(CXA - 0.06, CXB + 0.06, CYA - 0.06, CYB + 0.06, z2 + 0.002), 'boya_kirmizi', Z)
y.yuz_yon(dikdortgen(CXA + 0.03, CXB - 0.03, CYA + 0.05, CYB - 0.05, z2 + 0.0035), 'beyaz', Z)
for kk, pc in enumerate(tanit_sekli(0.09)):   # the mosaic Tanit, laid flat
    y.yuz_yon([V((CXA + CXB) / 2 + u, CYA + 0.08 + v, z2 + 0.005) for u, v in pc], 'boya_kirmizi', Z)
havuz(y, (CXA + CXB) / 2 - 0.05, (CXA + CXB) / 2 + 0.05, CYB - 0.17, CYB - 0.08, z2 + 0.014, derin=0.02, kenar=0.012, key=KUMA)
HCOL = 0.11
cols = []
for i in range(4):
    a, b = ki[i], ki[(i + 1) % 4]
    m = max(2, int(round((b - a).length / 0.07)))
    for j in range(m):
        cols.append(a.lerp(b, j / m))
for p in cols:
    iyon_hafif(y, p.x, p.y, z2 + 0.002, z2 + HCOL, 0.007, SIV, 'siva_krem', n=6, aci=0.0)
for i in range(4):
    a, b = ki[i], ki[(i + 1) % 4]
    e = (b - a).normalized()
kb = disa(ki, 0.008)
duvarlar(y, [V(p.x, p.y) for p in kb], z2 + HCOL, z2 + HCOL + 0.014, 'siva_krem', ust='siva_krem', kalinlik=0.016)
for i in range(4):   # the colonnade's lean-to roof from the court wall down to the beam, and its soffit
    a, b = kr[i], kr[(i + 1) % 4]
    ai, bi = kb[i], kb[(i + 1) % 4]
    q = [V(ai.x, ai.y, z2 + HCOL + 0.014), V(bi.x, bi.y, z2 + HCOL + 0.014), V(b.x, b.y, z2 + HCOL + 0.05), V(a.x, a.y, z2 + HCOL + 0.05)]
    y.yuz_yon(q, 'kiremit', Z)
    y.yuz_yon([V(ai.x, ai.y, z2 + HCOL), V(bi.x, bi.y, z2 + HCOL), V(b.x, b.y, z2 + HCOL), V(a.x, a.y, z2 + HCOL)], 'ahsap_koyu', -Z)
# the belvedere tower on the palace's front corner
BX, BY = PX0 + 0.07, PY0_ + 0.07
kutu(y, V(BX - 0.07, BY - 0.07, ZPR), X, 0.14, 0.14, 0.18, SIV, 'onarkasagsol')
kb_ = dikdortgen(BX - 0.07, BX + 0.07, BY - 0.07, BY + 0.07)
for i in range(4):
    a, b = kb_[i], kb_[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for j in range(2):
        pencere_kutu(y, a, e, nn, 0.035 + 0.05 * j, ZPR + 0.1, 0.02, 0.05, 'koyu', cerceve='kum_acik')
kavetto(y, kb_, ZPR + 0.18, 0.03, 0.018, 'siva_krem')
parapet(y, disa(kb_, 0.018), ZPR + 0.21, 0.008, 0.02, 0.01, SIV)
sancak(y, BX, BY, ZPR + 0.21, boy=0.18, en=0.09, yuk=0.055, aci=D(200))
# on the roof terrace: a reed-shaded pergola at the back corner, stair huts, cisterns' well heads, potted palms
GX0, GX1, GY0, GY1 = PX1 - 0.2, PX1 - 0.03, PY1_ - 0.12, PY1_ - 0.03
for px in (GX0, (GX0 + GX1) / 2, GX1):
    for py in (GY0, GY1):
        y.prizma((px, py), 0.004, ZPR, ZPR + 0.06, 'ahsap', n=5, ust=False)
for py in (GY0, GY1):
    cubuk(y, V(GX0 - 0.008, py, ZPR + 0.062), V(GX1 + 0.008, py, ZPR + 0.062), 0.006, 'ahsap_koyu', 0.006)
kutu(y, V(GX0 - 0.01, GY0 - 0.01, ZPR + 0.066), X, GX1 - GX0 + 0.02, GY1 - GY0 + 0.02, 0.004, 'saz', 'onarkasagsolust')
y.yuz_yon(dikdortgen(GX0 - 0.01, GX1 + 0.01, GY0 - 0.01, GY1 + 0.01, ZPR + 0.066), 'saz', -Z)
for k in range(5):
    cubuk(y, V(GX0 - 0.01, GY0 + (GY1 - GY0) * k / 4, ZPR + 0.071), V(GX1 + 0.01, GY0 + (GY1 - GY0) * k / 4, ZPR + 0.071), 0.003, 'saz_koyu', 0.003)
for (hx, hy, aci_) in ((PX0 + 0.05, PY1_ - 0.08, 0.0), (PX1 - 0.04, PY0_ + 0.2, -math.pi / 2)):
    with parca(y, (hx, hy, ZPR), aci_):
        kutu(y, V(-0.035, -0.03, 0), X, 0.07, 0.06, 0.05, SIV, 'onarkasagsol')
        y.yuz_yon(dikdortgen(-0.035, 0.035, -0.03, 0.03, 0.05), 'siva_krem', Z)
        duvarlar(y, dikdortgen(-0.035, 0.035, -0.03, 0.03), 0.05, 0.056, SIV, ust='siva_krem', kalinlik=0.004)
        pencere_kutu(y, V(-0.035, -0.03), X, -Y, 0.025, 0.0, 0.02, 0.036, 'ahsap_koyu', cerceve=KUMA)
for (wx, wy) in ((-0.5, PY0_ + 0.04), (-0.62, PY1_ - 0.035)):
    y.prizma((wx, wy), 0.014, ZPR, ZPR + 0.016, KUMA, n=8)
    y.yuz_yon(cokgen((wx, wy), 0.009, 8, z=ZPR + 0.0165), 'koyu', Z)
for (qx, qy) in ((PX0 + 0.16, PY0_ + 0.03), (PX0 + 0.3, PY0_ + 0.03), (PX1 - 0.25, PY0_ + 0.03)):
    donel(y, (qx, qy), [(0.008, ZPR), (0.012, ZPR + 0.012), (0.01, ZPR + 0.018), (0.0, ZPR + 0.018)], 'kerpic', n=6)
    agac(y, qx, qy, ZPR + 0.016, 0.05, 'palmiye', 'zeytin', 'ahsap_acik')

# ================================================================ the town on the slopes
y.bolum('Kent: yamaçtaki evler')
gh = random.Random(4)
evler = []


def ev(cx, cy, z, w, d, h, aci, tohum, duvar, katlar):
    """pon_ev and, by chance, a cavetto cornice under its parapet (the Punic houses of the Byrsa quarter were stuccoed
    with Egyptianising cornices)"""
    g = random.Random(tohum * 7 + 3)
    if g.random() < 0.1: duvar = 'siva_krem'
    pon_ev(y, cx, cy, z, w, d, h, aci=aci, tohum=tohum, duvar=duvar, katlar=katlar)
    if g.random() < 0.65:
        with parca(y, (cx, cy, z), aci):
            silme(y, dikdortgen(-w / 2, w / 2, -d / 2, d / 2), h - 0.014, 0.014, 0.005, 'siva_krem', KAVETTO_H)


def ev_koy(x0, x1, y0, y1, z, adim=0.13, derin=(0.09, 0.12), kapi_yon=0.0, hmin=0.09, hmax=0.17, bosluk=None):
    """a row of tall houses along x0..x1 at y0..y1 (the row's depth), doors toward kapi_yon"""
    x = x0
    while x < x1 - 0.06:
        w = min(gh.uniform(0.08, adim), x1 - x)
        if bosluk and bosluk[0] - 0.02 < x + w / 2 < bosluk[1] + 0.02:
            x = bosluk[1] + 0.02; continue
        d = gh.uniform(*derin); d = min(d, y1 - y0)
        cy = (y0 + y1) / 2 + gh.uniform(-0.01, 0.01)
        h = gh.uniform(hmin, hmax)
        kat = 3 if h > 0.14 else 2
        ww, dd = (w, d) if abs(math.sin(kapi_yon)) < 0.5 else (d, w)
        ev(x + w / 2, cy, z, ww - 0.012, dd, h, kapi_yon, gh.randint(0, 999), gh.choice((SIV, SIV, SIV, 'siva_krem')),
           kat)
        x += w


# at the foot of the hill: two rows either side of the stair's forecourt
for (xa, xb) in ((X0 + 0.03, SX - 0.24), (SX + 0.24, X1 - 0.03)):
    ev_koy(xa, xb, -1.12, -0.99, Z0, kapi_yon=0.0)
    ev_koy(xa, xb, -0.95, -0.82, Z0, kapi_yon=0.0, hmin=0.1, hmax=0.17)
# on the lower terrace, before the middle terrace's wall
for (xa, xb) in ((T1[0] + 0.02, SX - SW - 0.06), (SX + SW + 0.06, T1[1] - 0.02)):
    ev_koy(xa, xb, T1[2] + 0.04, T2[2] - 0.05, T1[4], kapi_yon=0.0, hmin=0.09, hmax=0.15)
# the sides of the lower terrace and the ground beside it
for s in (-1, 1):
    xa, xb = sorted((s * 0.995, s * 0.88))
    for k in range(5):
        yy = -0.38 + 0.26 * k
        ev((xa + xb) / 2, yy, T1[4], 0.1, 0.11, gh.uniform(0.09, 0.15), s * math.pi / 2, 200 + k + (10 if s > 0 else 0), SIV, 2)
    for k in range(7):
        yy = -0.68 + 0.26 * k if k < 6 else 0.92
        if k == 6: continue
        ev(s * 1.08, yy, Z0, 0.1, 0.12, gh.uniform(0.08, 0.13), s * math.pi / 2, 300 + k + (10 if s > 0 else 0), SIV, 2)
# the back of the hill
ev_koy(X0 + 0.05, X1 - 0.05, 1.07, 1.14, Z0, derin=(0.06, 0.07), hmin=0.06, hmax=0.1, kapi_yon=math.pi)
# the middle terrace's right side and back: gardens with cypresses and palms
for k in range(6):
    agac(y, 0.79, -0.4 + 0.22 * k, T2[4], 0.15, 'servi', 'yesil_koyu')
for (x, yy) in ((-0.1, 0.91), (0.3, 0.91), (0.6, 0.91), (-0.5, 0.86), (-0.75, -0.3), (-0.5, -0.36), (-0.2, -0.36), (0.05, -0.38)):
    agac(y, x, yy, T2[4], 0.13, 'palmiye', 'zeytin', 'ahsap_acik')
for (x, yy) in ((-0.95, 0.98), (0.95, 0.98), (-0.95, -0.72), (0.95, -0.72)):
    agac(y, x, yy, T1[4], 0.12, 'servi', 'yesil_koyu')

calistir(y, 'lm_byrsa')
