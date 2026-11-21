# Kolezyum (lm_kolezyum): oval arena, three tiers of arches, attic with windows, stepped seating, sand floor.
# blender -b --python tools/lm-blender/kolezyum.py -- <out.glb> [preview.png]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
from ortak import Yapi, temizle, disa_aktar, onizle, argumanlar

# ---- dimensions (longest side = 2) ----
A, B = 1.0, 0.83          # outer ellipse half-axes
N = 40                    # bays around
T = 0.10                  # wall thickness (outer face -> gallery face)
ZB = 0.03                 # base plinth height
TIER = [0.13, 0.125, 0.12]
ATTIC = 0.11
K = 6                     # arch segments
D = 0.03                  # arch depth
CD, CW = 0.012, 0.011     # half-column depth / half width
COR = (0.016, 0.014)      # cornice overhang / height
AA, AB = 0.47, 0.30       # arena half-axes (podium line)
Z_FLOOR, Z_POD = 0.045, 0.10
GALLERY = 0.10

TAS = (0.82, 0.67, 0.48)
TAS_ACIK = (0.90, 0.78, 0.60)
TAS_KOYU = (0.62, 0.48, 0.34)
DELIK = (0.24, 0.17, 0.12)
KOLON = (0.88, 0.75, 0.57)
OTURAK = [(0.80, 0.67, 0.50), (0.74, 0.61, 0.45)]
BASAMAK = (0.60, 0.48, 0.35)
DUVAR_IC = (0.70, 0.56, 0.41)
KUM = (0.88, 0.62, 0.34)
KUM_ACIK = (0.93, 0.72, 0.45)
PODYUM = (0.63, 0.51, 0.39)
TABAN_YAN, TABAN_UST = (0.64, 0.55, 0.44), (0.76, 0.67, 0.55)
MAVI = (0.12, 0.33, 0.86)
DIREK = (0.36, 0.26, 0.17)


def elips_noktalari(a, b, n):
    """n points at equal arc length, CCW, first one at the front (-y)."""
    M = 4000
    pts = [(a * math.cos(-math.pi / 2 + 2 * math.pi * i / M), b * math.sin(-math.pi / 2 + 2 * math.pi * i / M)) for i in range(M + 1)]
    L = [0]
    for i in range(M):
        L.append(L[-1] + math.dist(pts[i], pts[i + 1]))
    out, j = [], 0
    for k in range(n):
        s = L[-1] * (k + 0.5) / n          # (a bay boundary half a bay off the front: a bay faces the camera)
        while L[j + 1] < s: j += 1
        f = (s - L[j]) / (L[j + 1] - L[j])
        out.append(Vector((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f, 0)))
    return out


P = elips_noktalari(A, B, N)
NRM = [Vector((p.x / A ** 2, p.y / B ** 2, 0)).normalized() for p in P]
Q = [P[i] - NRM[i] * T for i in range(N)]


def halka(pts, z, ofs=0.0, nrm=NRM):
    return [Vector((p.x + nrm[i].x * ofs, p.y + nrm[i].y * ofs, z)) for i, p in enumerate(pts)]


y = Yapi(tohum=7)

# ---- base plinth ----
y.serit(halka(P, 0, 0.07), halka(P, ZB, 0.07), TABAN_YAN)
y.serit(halka(P, ZB, 0.07), halka(P, ZB), TABAN_UST)


def bay_cerceve(i, z0):
    a, b = P[i], P[(i + 1) % N]
    W = (b - a).length
    e = (b - a) / W
    nc = Vector((e.y, -e.x, 0))
    def L(u, v, d=0.0):
        return a + e * u - nc * d + Vector((0, 0, z0 + v))
    return W, e, nc, L


def kolon(L, e, nc, H, renk=KOLON):
    o = L(-CW, 0, -CD)
    y.kutu(o, e, -nc, 2 * CW, CD, H, renk, 'onsagsol')


def korniş(z):
    c, h = COR
    r0, r1 = halka(P, z - h / 2), halka(P, z + h / 2)
    y.serit(r0, halka(P, z - h / 2, c), TAS_ACIK)
    y.serit(halka(P, z - h / 2, c), halka(P, z + h / 2, c), TAS_ACIK)
    y.serit(halka(P, z + h / 2, c), r1, TAS_ACIK)


def cerceve(a, b, z0):
    """a wall face from a to b (seen from the side of nc = right of a->b): local u along it, v up, d into the wall"""
    W = (b - a).length
    e = (b - a) / W
    nc = Vector((e.y, -e.x, 0))
    def L(u, v, d=0.0):
        return a + e * u - nc * d + Vector((0, 0, z0 + v))
    return W, e, nc, L


def kemerli(a, b, z0, H, v0=0.0, en=0.68, ust=0.017, derin=D, k_say=K, renk=TAS, korkuluk=None):
    """one bay with a round-arched opening (front in convex pieces, reveal, dark back); korkuluk: sill height of a parapet"""
    W, e, nc, L = cerceve(a, b, z0)
    x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
    R = (x1 - x0) / 2
    hs = H - ust - R
    kemer = [(x0 + R + R * math.cos(math.pi - math.pi * k / k_say), hs + R * math.sin(math.pi - math.pi * k / k_say)) for k in range(1, k_say)]
    acik = [(x0, v0), (x0, hs)] + kemer + [(x1, hs), (x1, v0)]
    y.yuz([L(0, 0), L(x0, 0), L(x0, H), L(0, H)], renk)
    y.yuz([L(x1, 0), L(W, 0), L(W, H), L(x1, H)], renk)
    if v0 > 0: y.yuz([L(x0, 0), L(x1, 0), L(x1, v0), L(x0, v0)], renk)
    tepe = [(x0, hs)] + kemer + [(x1, hs)]
    for k in range(len(tepe) - 1):
        (ua, va), (ub, vb) = tepe[k], tepe[k + 1]
        y.yuz([L(ua, va), L(ub, vb), L(ub, H), L(ua, H)], renk)
    for k in range(len(acik)):
        p, q = acik[k], acik[(k + 1) % len(acik)]
        y.yuz([L(*p), L(*p, derin), L(*q, derin), L(*q)], TAS_ACIK if k == len(acik) - 1 else TAS_KOYU)
    y.yuz([L(*acik[0], derin)] + [L(*acik[-1], derin)] + [L(*q, derin) for q in reversed(acik[1:-1])], DELIK)
    if korkuluk:   # a low parapet standing in the opening, a little behind the face
        d0, d1, h = derin * 0.35, derin * 0.6, v0 + korkuluk
        y.yuz([L(x0, v0, d0), L(x1, v0, d0), L(x1, h, d0), L(x0, h, d0)], TAS_ACIK)
        y.yuz([L(x0, h, d0), L(x1, h, d0), L(x1, h, d1), L(x0, h, d1)], TAS_ACIK)
    return W, e, nc, L


# ---- three tiers of arches ----
z = ZB
for t, H in enumerate(TIER):
    for i in range(N):
        W, e, nc, L = kemerli(P[i], P[(i + 1) % N], z, H, v0=0.0 if t == 0 else 0.012, korkuluk=None if t == 0 else 0.018)
        kolon(L, e, nc, H)
    z += H
    korniş(z)

# ---- attic: solid wall, pilasters, small windows ----
for i in range(N):
    W, e, nc, L = bay_cerceve(i, z)
    y.yuz([L(0, 0), L(W, 0), L(W, ATTIC), L(0, ATTIC)], TAS)
    kolon(L, e, nc, ATTIC, TAS_ACIK)
    if i % 2 == 0:
        u0, u1, v0, v1 = 0.38 * W, 0.62 * W, 0.38 * ATTIC, 0.70 * ATTIC
        y.yuz([L(u0, v0, -0.002), L(u1, v0, -0.002), L(u1, v1, -0.002), L(u0, v1, -0.002)], DELIK)
z += ATTIC
ZTOP = z
korniş(ZTOP)
# a thin attic wall on top, then a step down to the roof of the inner gallery (an arched colonnade above the seats)
TA = 0.035
ZT = ZTOP + COR[1] / 2
ZG = ZTOP - 0.03
ZSEAT = ZTOP - GALLERY
y.serit(halka(P, ZT), halka(P, ZT, -TA), TAS_ACIK)
y.serit(halka(P, ZT, -TA), halka(P, ZG, -TA), DUVAR_IC)
y.serit(halka(P, ZG, -TA), halka(Q, ZG), TAS)
for i in range(N):
    kemerli(Q[(i + 1) % N], Q[i], ZSEAT, ZG - ZSEAT, en=0.6, ust=0.008, derin=0.03, k_say=4, renk=DUVAR_IC)

# ---- seating: rings from the gallery wall down to the podium ----
SA, SB = AA / (A - T), AB / (B - T)
POD = [Vector((q.x * SA, q.y * SB, 0)) for q in Q]
DUSUS = [0.027] * 11
PREC = {3, 7}
for k in PREC: DUSUS[k] = 0.045
olc = (ZSEAT - Z_POD) / sum(DUSUS)
DUSUS = [d * olc for d in DUSUS]
S = len(DUSUS)
halkalar = [[Q[i].lerp(POD[i], k / S) for i in range(N)] for k in range(S + 1)]
zk = ZSEAT
for k in range(S):
    r_dis, r_ic = halkalar[k], halkalar[k + 1]
    y.serit([Vector((p.x, p.y, zk)) for p in r_dis], [Vector((p.x, p.y, zk)) for p in r_ic], OTURAK[k % 2])
    z2 = zk - DUSUS[k]
    renk = DUVAR_IC if k in PREC else BASAMAK
    ust, alt = [Vector((p.x, p.y, zk)) for p in r_ic], [Vector((p.x, p.y, z2)) for p in r_ic]
    y.serit(ust, alt, renk)
    # radial stairs: a light strip down every fifth bay, over the seat and its riser
    for i in range(0, N, 5):
        j = (i + 1) % N
        f0, f1 = 0.4, 0.6
        up = Vector((0, 0, 0.0015))
        t0, t1 = r_dis[i].lerp(r_dis[j], f0), r_dis[i].lerp(r_dis[j], f1)
        s0, s1 = r_ic[i].lerp(r_ic[j], f0), r_ic[i].lerp(r_ic[j], f1)
        Z = lambda p, zz: Vector((p.x, p.y, zz))
        y.yuz([Z(t0, zk) + up, Z(s0, zk) + up, Z(s1, zk) + up, Z(t1, zk) + up], TAS_ACIK)
        inw = -(s0 + s1) / 2; inw.z = 0; inw = inw.normalized() * 0.0015
        y.yuz([Z(s1, zk) + inw, Z(s0, zk) + inw, Z(s0, z2) + inw, Z(s1, z2) + inw], TAS_KOYU)
    if k in PREC:   # entrances (vomitoria) in the taller walls
        for i in range(0, N, 5):
            j = (i + 1) % N
            m = lambda p, q, f: p.lerp(q, f)
            a0, a1 = m(ust[i], ust[j], 0.3), m(ust[i], ust[j], 0.7)
            b0, b1 = m(alt[i], alt[j], 0.3), m(alt[i], alt[j], 0.7)
            inw = (Vector((0, 0, 0)) - (a0 + a1) / 2); inw.z = 0; inw = inw.normalized() * 0.002
            lift = Vector((0, 0, (zk - z2) * 0.15))
            y.yuz([a0 + inw - lift, b0 + inw, b1 + inw, a1 + inw - lift], DELIK)
    zk = z2

# ---- podium wall and the sand ----
y.serit([Vector((p.x, p.y, Z_POD)) for p in POD], [Vector((p.x, p.y, Z_FLOOR)) for p in POD], PODYUM)
y.yuz([Vector((p.x, p.y, Z_FLOOR)) for p in POD], KUM)
# raked sand: a lighter oval in the middle
y.yuz([Vector((p.x * 0.78, p.y * 0.72, Z_FLOOR + 0.001)) for p in POD], KUM_ACIK)
# coping stone along the podium top (the last seat row outward of it is the front row)
y.serit([Vector((p.x, p.y, Z_POD + 0.008)) for p in POD], [Vector((p.x, p.y, Z_POD)) for p in POD], TAS_ACIK)

# ---- two blue banners on the wall top (front and back) ----
for s in (-1, 1):
    c = Vector((0, s * (B - T / 2), 0))
    zt = ZTOP + COR[1] / 2
    y.silindir(c, 0.008, zt, zt + 0.19, DIREK)
    o = Vector((c.x + 0.006, c.y - 0.002, zt + 0.11))
    y.kutu(o, Vector((1, 0, 0)), Vector((0, 1, 0)), 0.10, 0.004, 0.07, MAVI)

print('UCGEN', y.ucgen_sayisi())

if __name__ == '__main__':
    arg = argumanlar()
    temizle()
    ob = y.nesne('lm_kolezyum', dikey=1.2)
    if arg:
        disa_aktar(ob, os.path.abspath(arg[0]))
    if len(arg) > 1:
        onizle(os.path.abspath(arg[1]), merkez=(0, 0, 0.2), boy=2.5, aci=(-20, 32))
