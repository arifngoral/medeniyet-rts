# Kartaca Surları (lm_kartacasur): the triple land defence of Carthage across the isthmus (Appian): a water ditch,
# a stake palisade, then the great sandstone wall turning a corner: three storeys thick, its inner face opening into
# elephant stables below and horse stables above, two-storey towers at even intervals, a cavetto cornice and merlons;
# the main gate between two tall towers with a bridge over the ditch; inside, the Megara's houses and gardens.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kartaca_ortak import kavetto, KAVETTO, KAVETTO_H, pon_ev, tanit_kabartma, kanatli_gunes, insan, pencere_kutu, tanit_heykel
from kartaca_ek import *
from bina_ortak import calistir
from hint_ortak import fil as fil_h
import doku

y = Yapi()
rn = random.Random(7)
Z0 = 0.07
GX0, GX1, GY0, GY1 = -1.2, 1.2, -1.15, 1.15
NX, NY = 48, 46
DY, DX = -0.8, 1.0           # ditch centre lines (front, right)
SU = Z0 - 0.035
WY, WX, T = -0.42, 0.66, 0.2  # the wall's outer face lines and thickness
WB = Z0 - 0.012               # its foot (sunk a little)
H1, H2, H3 = 0.15, 0.14, 0.13
WT = Z0 + H1 + H2 + H3        # the wall walk
GA, GB = -0.86, -0.58        # the gate passage (towards the left end: its towers no longer hide the right arm)
GX = (GA + GB) / 2


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def hendek(d):
    if d <= 0.05: return Z0 - 0.06
    if d >= 0.1: return Z0
    return Z0 - 0.06 + 0.06 * (d - 0.05) / 0.05


def yuk(x, yy):
    z = Z0
    if x <= DX + 0.1 + 1e-6: z = min(z, hendek(abs(yy - DY)))
    if yy >= DY - 0.1 - 1e-6: z = min(z, hendek(abs(x - DX)))
    return z


# ---------------- ground, the ditch ----------------
y.bolum('Arazi ve hendek')


def arazi_renk(x, yy, z):
    n = 0.5 + 0.5 * (math.sin(x * 4.7 + 0.3) * math.cos(yy * 3.9 - 0.8) * 0.7 + math.sin(x * 10.3 - yy * 7.7) * 0.3)
    c = tuple(p + (q - p) * n for p, q in zip((0.45, 0.52, 0.28), (0.55, 0.54, 0.33)))        # grass
    ic = 1 - _ss(-0.05, 0.05, min(WX - x, yy - WY))            # outside the wall
    disari = _ss(-0.02, 0.06, max(x - (WX + 0.04), WY - 0.04 - yy))
    c = tuple(p + (q - p) * 0.55 * disari for p, q in zip(c, (0.6, 0.53, 0.38)))              # trampled earth by the wall
    c = tuple(p + (q - p) * _ss(Z0 - 0.003, Z0 - 0.03, z) for p, q in zip(c, (0.55, 0.45, 0.33)))   # the ditch banks
    road = max(0.0, 1 - abs(x - GX) / 0.07) * (1 if yy < WY - 0.08 else 0)
    road = max(road, max(0.0, 1 - abs(x - GX) / 0.06) * (1 if yy > WY + T else 0))
    c = tuple(p + (q - p) * 0.8 * _ss(0, 0.5, road) for p, q in zip(c, (0.7, 0.63, 0.49)))      # the road
    return c


doku.KOSE_RENK['toprak_ot'] = arazi_renk
P = [[V(GX0 + (GX1 - GX0) * i / NX, GY0 + (GY1 - GY0) * j / NY, 0) for j in range(NY + 1)] for i in range(NX + 1)]
for i in range(NX + 1):
    for j in range(NY + 1):
        P[i][j].z = yuk(P[i][j].x, P[i][j].y)
for i in range(NX):
    for j in range(NY):
        q = [P[i][j], P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]]
        # (under the wall body: not drawn)
        if all(WX - T - 1e-6 <= p.x <= WX + 1e-6 and p.y >= WY - 1e-6 for p in q): continue
        if all(WY - 1e-6 <= p.y <= WY + T + 1e-6 and p.x <= WX + 1e-6 for p in q): continue
        dg = (i + j) % 2 == 0
        for tri in (([q[0], q[1], q[2]], [q[0], q[2], q[3]]) if dg else ([q[0], q[1], q[3]], [q[1], q[2], q[3]])):
            y.yuz_yon(tri, 'toprak_ot', Z)
kenar = [P[i][0] for i in range(NX)] + [P[NX][j] for j in range(NY)] + [P[i][NY] for i in range(NX, 0, -1)] + [P[0][j] for j in range(NY, 0, -1)]
for k in range(len(kenar)):
    a, b = kenar[k], kenar[(k + 1) % len(kenar)]
    e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
    m1a, m1b = min(a.z, 0.03 + 0.008 * math.sin(a.x * 9 + a.y * 7)), min(b.z, 0.03 + 0.008 * math.sin(b.x * 9 + b.y * 7))
    y.yuz_yon([V(a.x, a.y, m1a), V(b.x, b.y, m1b), b, a], 'toprak', nn)
    y.yuz_yon([V(a.x, a.y, 0), V(b.x, b.y, 0), V(b.x, b.y, m1b), V(a.x, a.y, m1a)], 'kaya_koyu', nn)
    if a.z < SU or b.z < SU:
        y.yuz_yon([V(a.x, a.y, min(a.z, SU)), V(b.x, b.y, min(b.z, SU)), V(b.x, b.y, SU), V(a.x, a.y, SU)], 'su', nn)
# the water in the ditch (in cells)
HW = 0.072
for k in range(14):
    x0, x1 = GX0 + (DX - HW - GX0) * k / 14, GX0 + (DX - HW - GX0) * (k + 1) / 14
    y.yuz_yon([V(x0, DY - HW, SU), V(x1, DY - HW, SU), V(x1, DY + HW, SU), V(x0, DY + HW, SU)], 'su', Z)
y.yuz_yon([V(DX - HW, DY - HW, SU), V(DX + HW, DY - HW, SU), V(DX + HW, DY + HW, SU), V(DX - HW, DY + HW, SU)], 'su', Z)
for k in range(11):
    y0, y1 = DY + HW + (GY1 - DY - HW) * k / 11, DY + HW + (GY1 - DY - HW) * (k + 1) / 11
    y.yuz_yon([V(DX - HW, y0, SU), V(DX + HW, y0, SU), V(DX + HW, y1, SU), V(DX - HW, y1, SU)], 'su', Z)
for k in range(5):   # the front ditch beyond the corner, to the edge
    x0, x1 = DX + HW + (GX1 - DX - HW) * k / 5, DX + HW + (GX1 - DX - HW) * (k + 1) / 5
    if yuk((x0 + x1) / 2, DY) < SU:
        y.yuz_yon([V(x0, DY - HW, SU), V(x1, DY - HW, SU), V(x1, DY + HW, SU), V(x0, DY + HW, SU)], 'su', Z)

# ---------------- the palisade, the bridge ----------------
y.bolum('Palisad ve köprü')
PY_, PX_ = -0.6, 0.84
palisad(y, [(GX0 + 0.01, PY_), (GA + 0.03, PY_)], yuk, h=0.075, tohum=1)
palisad(y, [(GB - 0.03, PY_), (PX_, PY_), (PX_, GY1 - 0.01)], yuk, h=0.075, tohum=2)
# a gate in the palisade: two posts and a lintel
for x in (GA + 0.03, GB - 0.03):
    cubuk(y, V(x, PY_, Z0 - 0.005), V(x, PY_, Z0 + 0.11), 0.012, 'ahsap_koyu')
cubuk(y, V(GA + 0.02, PY_, Z0 + 0.105), V(GB - 0.02, PY_, Z0 + 0.105), 0.012, 'ahsap_koyu')

for k in range(4):
    for sx in (-1, 1):
        y.prizma((GX + sx * 0.055, DY - 0.09 + k * 0.06), 0.006, Z0 - 0.07, Z0 + 0.004, 'ahsap_koyu', n=6, ust=False)
kutu(y, V(GX - 0.065, DY - 0.13, Z0 + 0.004), X, 0.13, 0.26, 0.012, 'ahsap_acik', 'onarkasagsolust')
for sx in (-1, 1):   # rails
    for k in range(5):
        cubuk(y, V(GX + sx * 0.06, DY - 0.12 + k * 0.06, Z0 + 0.016), V(GX + sx * 0.06, DY - 0.12 + k * 0.06, Z0 + 0.05), 0.006, 'ahsap')
    cubuk(y, V(GX + sx * 0.06, DY - 0.125, Z0 + 0.05), V(GX + sx * 0.06, DY + 0.125, Z0 + 0.05), 0.007, 'ahsap')

# ---------------- the wall ----------------
y.bolum('Sur')
OUT = [V(GX0, WY), V(WX, WY), V(WX, GY1)]
INN = [V(GX0, WY + T), V(WX - T, WY + T), V(WX - T, GY1)]
KULE_ON = [GA - 0.09, GB + 0.09, 0.66]           # tower centres on the front (x): the gate pair and the corner (wide gaps:
KULE_SAG = [0.74]                        # the long wall body and its storeys must read); on the right (y)
KW = 0.14


def kulede(p, w=KW / 2 + 0.005):
    for tx in KULE_ON:
        if abs(p.x - tx) < w + (0.03 if tx == KULE_ON[-1] else 0) and p.y < WY + T + 0.02: return True
    for ty in KULE_SAG:
        if abs(p.y - ty) < w and p.x > WX - T - 0.02: return True
    return False


# the outer face: plinth, three storeys marked by string courses, windows high up
for a, b, parcalar_ in ((OUT[0], OUT[1], [(GX0, GA), (GB, WX)]), (OUT[1], OUT[2], [(WY, GY1)])):
    e = (b - a).normalized(); nrm = V(e.y, -e.x)
    for u0, u1 in parcalar_:
        pa = V(u0, a.y) if e.x else V(a.x, u0)
        pb = V(u1, a.y) if e.x else V(a.x, u1)
        L = (pb - pa).length
        n = max(1, int(L / 0.14))
        for k in range(n):
            duz_duvar(y, pa.lerp(pb, k / n), pa.lerp(pb, (k + 1) / n), WB, WT, 'kum')
        silme(y, [pa, pb], WB, 0.05, 0.016, 'kum_koyu', 'kaide', kapali=False)
        for zz in (Z0 + H1, Z0 + H1 + H2):
            silme(y, [pa, pb], zz - 0.005, 0.01, 0.008, 'kum_acik', 'duz', kapali=False)
        m = max(1, int(L / 0.1))
        for k in range(m):
            c = pa.lerp(pb, (k + 0.5) / m)
            if kulede(c, KW / 2 + 0.03): continue
            for zz, hh in ((Z0 + H1 + 0.05, 0.035), (Z0 + H1 + H2 + 0.045, 0.03)):
                yarik(y, pa + Z * Z0 + nrm * 0.001, e, nrm, (k + 0.5) * L / m - 0.005, zz - Z0, 0.01, hh, 'koyu')
        for k in range(2, m - 1, 2):   # shallow pilaster buttresses between pairs of slits (the long face in bays)
            c = pa.lerp(pb, k / m)
            if kulede(c, KW / 2 + 0.05): continue
            c = c + nrm * 0.0065
            kutu_merkez(y, (c.x, c.y), 0.032, 0.013, WT - 0.044 - WB, 'kum', z0=WB, aci=math.atan2(e.y, e.x), yuzler='onarkasagsolust')
        for k in range(m):   # the lowest storey's slits too (the elephant stalls' air holes), low and wide
            c = pa.lerp(pb, (k + 0.5) / m)
            if kulede(c, KW / 2 + 0.03): continue
            yarik(y, pa + Z * Z0 + nrm * 0.001, e, nrm, (k + 0.5) * L / m - 0.009, 0.075, 0.018, 0.012, 'koyu')
# the cavetto cornice and the merloned parapet along the outer edge
for seg in ([V(GX0, WY), V(GA, WY)], [V(GB, WY), V(WX, WY), V(WX, GY1)]):
    silme(y, seg, WT - 0.045, 0.045, 0.026, 'kum_acik', KAVETTO_H, kapali=False)
    parapet(y, seg, WT, 0.014, 0.036, 0.03, 'kum', kapali=False)
# the walk on top (in cells)
for (a0, a1, b0, b1, n) in ((OUT[0], V(GA, WY), INN[0], V(GA, WY + T), 6), (V(GB, WY), OUT[1], V(GB, WY + T), INN[1], 6),
                            (OUT[1], OUT[2], INN[1], INN[2], 10)):
    for k in range(n):
        q = [a0.lerp(a1, k / n), a0.lerp(a1, (k + 1) / n), b0.lerp(b1, (k + 1) / n), b0.lerp(b1, k / n)]
        y.yuz_yon([p + Z * WT for p in q], 'zemin', Z)
# a low parapet on the inner edge
for seg in ([V(GA, WY + T), V(GX0, WY + T)], [V(WX - T, GY1), V(WX - T, WY + T), V(GB, WY + T)]):
    parapet(y, seg, WT, 0.022, 0.0, 0.014, 'kum', kapali=False)
# the inner face: elephant stables (arches) below, horse stables (square doors) above, small windows on top
# (each storey its own shade of sandstone, so the three levels read from afar; a timber gallery on posts runs along
# the horse storey, with a ramp up to it from the yard)
RENK1 = ('kum_koyu', 'kum', 'kum_acik', 'koyu')
RENK2 = ('kum', 'kum_koyu', 'kum_acik', 'koyu')
GD = 0.05                      # the gallery's depth
for a, b, uc in ((INN[1], INN[0], [(WX - T, GB), (GA, GX0)]), (INN[2], INN[1], [(GY1, WY + T)])):
    e = (b - a).normalized(); nrm = V(e.y, -e.x)
    for u0, u1 in uc:
        pa = V(u0, a.y) if abs(e.x) > 0.5 else V(a.x, u0)
        pb = V(u1, a.y) if abs(e.x) > 0.5 else V(a.x, u1)
        L = (pb - pa).length
        n = max(1, int(round(L / 0.135)))
        acik = []
        for k in range(n):
            p, q = pa.lerp(pb, k / n), pa.lerp(pb, (k + 1) / n)
            if kulede((p + q) / 2, KW / 2 + 0.03):
                duz_duvar(y, p, q, WB, WT, 'kum'); continue
            acik.append((p, q))
            y.kemerli(p + Z * 0, q + Z * 0, WB, H1 + (Z0 - WB), RENK1, v0=0.0, en=0.7, ust=0.016, derin=0.05, k_say=8,
                      cerceve=(0.009, ['kum_acik', 'kum_koyu']))
            dikdortgen_acik(y, p, q, Z0 + H1, H2, 0.3, 0.7, 0.0, 0.11, RENK2, derin=0.03, cerceve=(0.006, 'kum_acik'), ic_kenar=True)
            duz_duvar(y, p, q, Z0 + H1 + H2, WT, 'kum_acik')
            for f in (0.3, 0.7):   # two windows of the stores on the top storey
                pencere_kutu(y, p, e, nrm, L / n * f - 0.008, Z0 + H1 + H2 + 0.04, 0.016, 0.034, 'koyu', cerceve='kum')
        for zz in (Z0 + H1, Z0 + H1 + H2):
            silme(y, [pa, pb], zz - 0.004, 0.008, 0.007, 'kum_acik', 'duz', kapali=False)
        # the gallery: a plank deck on the beams, posts down to the yard, a rail
        for ia, (p, q) in enumerate(acik):
            m_ = (p + q) / 2 + nrm * (GD / 2 + 0.004)
            kutu_merkez(y, (m_.x, m_.y), (q - p).length + (0.002 if ia == len(acik) - 1 or acik[ia + 1][0] != q else 0.0), GD, 0.008,
                        'ahsap', z0=Z0 + H1 - 0.012, aci=math.atan2(e.y, e.x))
            son = ia == len(acik) - 1 or acik[ia + 1][0] != q
            for f in ((0.0, 1.0) if son else (0.0,)):   # (posts on the piers between the arches, not in the openings)
                c = p.lerp(q, f) + nrm * (GD + 0.001) + e * (0.006 if f == 0 else -0.006)
                cubuk(y, V(c.x, c.y, Z0 - 0.002), V(c.x, c.y, Z0 + H1 - 0.012), 0.007, 'ahsap_koyu')
                cubuk(y, V(c.x, c.y, Z0 + H1 - 0.004), V(c.x, c.y, Z0 + H1 + 0.03), 0.004, 'ahsap_koyu')
            cubuk(y, p + nrm * (GD + 0.001) + Z * (Z0 + H1 + 0.028), q + nrm * (GD + 0.001) + Z * (Z0 + H1 + 0.028), 0.004, 'ahsap')
            for f in (0.25, 0.75):   # beam ends under the deck
                c = p.lerp(q, f)
                cubuk(y, c + Z * (Z0 + H1 - 0.016), c + nrm * (GD + 0.006) + Z * (Z0 + H1 - 0.016), 0.006, 'ahsap_koyu', 0.006)
# the wall's cut ends at the model's edge (its rooms in section)
for p, q, yon in ((OUT[0], INN[0], -X), (INN[2], OUT[2], Y)):
    y.yuz_yon([p + Z * WB, q + Z * WB, q + Z * WT, p + Z * WT], 'kum_koyu', yon)
    # the floors and stalls showing in the section
    for zz in (Z0 + H1, Z0 + H1 + H2):
        y.yuz_yon([p + Z * (zz - 0.008) + yon * 0.0015, q + Z * (zz - 0.008) + yon * 0.0015, q + Z * zz + yon * 0.0015, p + Z * zz + yon * 0.0015], 'ahsap', yon)
# a plank ramp up to the horse gallery on the right arm (cleats across it, a rail on posts)
RA, RB = V(WX - T - GD - 0.33, 0.97), V(WX - T - GD - 0.004, 0.97)
cubuk(y, RA + Z * (Z0 - 0.004), RB + Z * (Z0 + H1 - 0.008), 0.05, 'ahsap', 0.008)
for k in range(1, 12):
    c = RA.lerp(RB, k / 12)
    cubuk(y, c + V(0, -0.024, Z0 + (H1 - 0.004) * k / 12), c + V(0, 0.024, Z0 + (H1 - 0.004) * k / 12), 0.004, 'ahsap_koyu', 0.004)
for k in range(1, 4):
    c = RA.lerp(RB, k / 4)
    cubuk(y, c + V(0, 0, Z0 - 0.004), c + V(0, 0, Z0 + (H1 - 0.004) * k / 4 - 0.006), 0.008, 'ahsap_koyu')
    cubuk(y, c + V(0, 0.026, Z0 + (H1 - 0.004) * k / 4), c + V(0, 0.026, Z0 + (H1 - 0.004) * k / 4 + 0.03), 0.003, 'ahsap_koyu')
cubuk(y, RA + V(0, 0.026, Z0 + 0.03), RB + V(0, 0.026, Z0 + H1 + 0.026), 0.0035, 'ahsap')

# ---------------- the towers ----------------
y.bolum('Kuleler')
for tx in KULE_ON[:-1]:
    if tx in KULE_ON[:2]: continue
    zr, zt = pon_kule(y, tx, WY - 0.1 + (T + 0.12) / 2, WB, KW, T + 0.12, 4, 0.142, alt='kum_koyu', ust='kum', kornis='kum_acik', mazgal_h=0.034, pencere=1)
for ty in KULE_SAG:
    zr, zt = pon_kule(y, WX - T - 0.02 + (T + 0.12) / 2, ty, WB, T + 0.12, KW, 4, 0.142, alt='kum_koyu', ust='kum', kornis='kum_acik', mazgal_h=0.034)
# the corner tower: bigger, a roof room and a banner
CW = 0.24
cx, cy = WX - T / 2 + 0.02, WY + T / 2 - 0.02
zr, zt = pon_kule(y, cx, cy, WB, CW, CW, 5, 0.13, alt='kum_koyu', ust='kum', kornis='kum_acik', mazgal_h=0.036, pencere=3)
kutu_merkez(y, (cx - 0.03, cy + 0.03), 0.13, 0.13, 0.08, 'kum', z0=zr)
kavetto(y, dikdortgen(cx - 0.095, cx + 0.035, cy - 0.035, cy + 0.095), zr + 0.08, 0.022, 0.012, 'kum_acik')
sancak(y, cx + 0.09, cy - 0.09, zr, boy=0.26, en=0.13, yuk=0.08, aci=-0.8)
# a bolt-thrower on the corner tower, its crew
BX, BY = cx + 0.04, cy - 0.06
with parca(y, (BX, BY, zr), -math.pi / 2 - 0.6):
    kutu_merkez(y, (0, 0), 0.03, 0.03, 0.02, 'ahsap_koyu', z0=0.0)
    cubuk(y, V(-0.05, 0, 0.026), V(0.05, 0, 0.034), 0.012, 'ahsap', 0.008)
    kutu_merkez(y, (0.035, 0), 0.016, 0.05, 0.018, 'ahsap_koyu', z0=0.025)
    for sg in (-1, 1):
        cubuk(y, V(0.035, sg * 0.024, 0.034), V(0.018, sg * 0.055, 0.036), 0.004, 'ahsap')
        cubuk(y, V(0.018, sg * 0.055, 0.036), V(-0.03, 0, 0.036), 0.0012, 'kumas')
    cubuk(y, V(-0.02, 0, 0.042), V(0.07, 0, 0.044), 0.003, 'bronz')
for a in (0.4, 2.3):
    insan(y, BX + 0.06 * math.cos(a), BY + 0.06 * math.sin(a), zr, 'boya_kirmizi', s=1.1, aci=a + math.pi, kalkan='bronz')

# ---------------- the main gate ----------------
y.bolum('Ana kapı')
for tx in (GA - 0.09, GB + 0.09):
    zr, zt = pon_kule(y, tx, WY - 0.12 + (T + 0.14) / 2, WB, 0.18, T + 0.14, 5, 0.155, alt='kum_koyu', ust='kum', kornis='kum_acik', mazgal_h=0.036, pencere=2)
# the passage: an arch through the wall on both faces, the gate leaves in the middle
y.kemerli(V(GA, WY), V(GB, WY), Z0 + 0.003, WT - Z0 - 0.003, ('kum', 'kum_koyu', 'zemin', 'ahsap'), v0=0.0, en=0.62, ust=0.1, derin=T * 0.5,
          k_say=12, cerceve=(0.014, ['kum_acik', 'kum_koyu']))
y.kemerli(V(GB, WY + T), V(GA, WY + T), Z0 + 0.003, WT - Z0 - 0.003, ('kum', 'kum_koyu', 'zemin', 'ahsap_koyu'), v0=0.0, en=0.62, ust=0.1,
          derin=T * 0.5 - 0.004, k_say=12)
kutu(y, V(GA, WY - 0.004, WB), X, GB - GA, T + 0.008, Z0 + 0.003 - WB, 'tas_koyu', 'onarkasagsol')   # the threshold
# the gatehouse block above the arch, proud of the wall, its cornice level with the towers' third storey
GZ1 = WB + 0.155 * 3 + 0.08
kutu(y, V(GA - 0.01, WY - 0.025, WT - 0.06), X, GB - GA + 0.02, T + 0.05, GZ1 - (WT - 0.06), 'kum', 'onarkasagsol')
kavetto(y, dikdortgen(GA - 0.01, GB + 0.01, WY - 0.025, WY + T + 0.025), GZ1, 0.045, 0.025, 'kum_acik')
parapet(y, disa(dikdortgen(GA - 0.01, GB + 0.01, WY - 0.025, WY + T + 0.025), 0.02), GZ1 + 0.045, 0.012, 0.034, 0.016, 'kum')
for k in range(3):   # windows of the gate chamber
    pencere_kutu(y, V(GA - 0.01, WY - 0.025), X, -Y, 0.05 + k * 0.08 - 0.009, WT - 0.06 + 0.07, 0.018, 0.045, 'koyu', cerceve='kum_acik')
kanatli_gunes(y, V(GX, WY - 0.025, WT - 0.02), X, -Y, 0.16, 0.03)
tanit_kabartma(y, V(GX, WY - 0.025, GZ1 - 0.09), X, -Y, 0.06, 'altin')
sancak(y, GA - 0.09, WY - 0.08, WB + 0.155 * 5 + 0.05, boy=0.22, en=0.12, yuk=0.075, aci=-1.0)
sancak(y, GB + 0.09, WY - 0.08, WB + 0.155 * 5 + 0.05, boy=0.22, en=0.12, yuk=0.075, aci=-1.0)

# ---------------- defenders ----------------
y.bolum('Askerler')
for x in (-0.82, 0.05, 0.42, 0.52):
    insan(y, x, WY + 0.05, WT, 'boya_kirmizi', s=1.1, aci=-math.pi / 2, kalkan='bronz', mizrak='bronz')
for yy in (0.4, 0.92):
    insan(y, WX - 0.05, yy, WT, 'boya_kirmizi', s=1.1, aci=0.0, kalkan='bronz', mizrak='bronz')
for x in (GX - 0.07, GX + 0.07):
    insan(y, x, WY - 0.06, Z0, 'boya_kirmizi', s=1.15, aci=-math.pi / 2, kalkan='bronz', mizrak='bronz')

# ---------------- inside: stables yard, the Megara ----------------
y.bolum('İç taraf')
# war elephants coming out of their stables under the wall, a mahout, fodder
# (the small North African forest elephants of Carthage: hint_ortak.fil(afrika=True), as in lm_filahirlari)
for yy, a, cul, bn in ((0.2, math.pi + 0.35, 'boya_kirmizi', 'kumas'), (0.42, math.pi - 0.15, 'mor', None)):
    fil_h(y, WX - T - GD - 0.14, yy, Z0, a, 0.95, 'fil', cul=cul, binici=bn, hortum=0.02, afrika=True)
fil_h(y, WX - T - 0.03, 0.533, Z0, math.pi, 0.95, 'fil', hortum=0.0, afrika=True)          # one coming out of its stall
fil_h(y, -0.32, WY + T + 0.13, Z0, math.pi / 2 + 0.2, 0.95, 'fil', cul='mor', binici='boya_kirmizi', hortum=0.03, afrika=True)
at(y, 0.0, WY + T + 0.08, Z0, 0.2, s=1.15, key='ahsap', eger='boya_kirmizi')
at(y, 0.07, WY + T + 0.06, Z0, 0.1, s=1.15, key='kum_koyu', eger='mor')
# horses led along the gallery of the right arm, a groom on the ramp
for yy, kk in ((0.2, 'ahsap'), (0.52, 'koyu')):
    at(y, WX - T - GD / 2 - 0.004, yy, Z0 + H1 - 0.004, -math.pi / 2, s=0.95, key=kk, eger='boya_kirmizi')
insan(y, WX - T - GD / 2 - 0.004, 0.3, Z0 + H1 - 0.004, 'kumas', s=1.0, aci=-math.pi / 2, kol=0.6)
insan(y, RA.x + 0.12, RA.y, Z0 + (H1 - 0.004) * 0.36, 'siva_oker', s=1.0, aci=0.0)
for x, yy in ((0.22, 0.02), (0.25, 0.1)):
    donel(y, (x, yy), [(0.03, Z0), (0.028, Z0 + 0.02), (0.016, Z0 + 0.035), (0.0, Z0 + 0.04)], 'saz', n=10)   # hay stacks
# the street from the gate, houses and gardens of the Megara
HOUSES = [(-0.49, 0.3, 0.16, 0.14, 0.12, math.pi), (-0.5, 0.54, 0.16, 0.16, 0.16, math.pi), (-0.2, 0.36, 0.14, 0.16, 0.12, 0.0),
          (-0.19, 0.62, 0.16, 0.14, 0.15, 0.0), (-0.5, 0.8, 0.16, 0.16, 0.13, math.pi), (-0.2, 0.9, 0.18, 0.16, 0.17, 0.0),
          (-1.04, 0.36, 0.18, 0.18, 0.12, 0.0), (-1.04, 0.62, 0.18, 0.16, 0.15, 0.0), (-1.04, 0.88, 0.18, 0.18, 0.13, 0.0),
          (-0.36, -0.02, 0.0, 0.0, 0.0, 0.0)]   # (the strip before the right arm is the stables' yard: no houses)
HOUSES = HOUSES[:-1]
for k, (cx, cy, w, d, h, a) in enumerate(HOUSES):
    pon_ev(y, cx, cy, Z0, w, d, h, aci=a + math.pi / 2, tohum=k + 1, katlar=2 if h > 0.14 else 1)
for k in range(12):   # olive gardens and palms
    x, yy = rn.uniform(-1.15, -0.8), rn.uniform(-0.05, 1.1)
    if any(abs(x - h[0]) < h[2] / 2 + 0.03 and abs(yy - h[1]) < h[3] / 2 + 0.03 for h in HOUSES): continue
    agac(y, x, yy, Z0, rn.uniform(0.09, 0.13), 'yapraklı', 'zeytin', 'ahsap')
for x, yy in ((GX + 0.11, 0.2), (GX - 0.11, 0.2), (GX + 0.11, 0.66), (GX - 0.11, 0.66), (0.05, 0.0), (-0.2, 0.08)):
    agac(y, x, yy, Z0, 0.18, 'palmiye', 'zeytin', 'ahsap')

# a small temple of Baal Hammon at the end of the street: podium, Ionic porch, cavetto, the sign of Tanit
TPX, TPY = GX, 1.0
kutu_merkez(y, (TPX, TPY), 0.24, 0.22, 0.05, 'kum', z0=Z0, yuzler='onarkasagsol')
kavetto(y, dikdortgen(TPX - 0.12, TPX + 0.12, TPY - 0.11, TPY + 0.11), Z0 + 0.03, 0.02, 0.01, 'kum_acik', ust=False)
y.yuz_yon([V(p.x, p.y, Z0 + 0.05) for p in dikdortgen(TPX - 0.12, TPX + 0.12, TPY - 0.11, TPY + 0.11)], 'mermer', Z)
merdiven(y, (TPX, TPY - 0.11 - 0.05), math.pi / 2, 0.1, Z0, Z0 + 0.05, n=5, d=0.0102, key='kum_acik')
kutu(y, V(TPX - 0.09, TPY - 0.03, Z0 + 0.05), X, 0.18, 0.12, 0.14, 'siva_krem', 'onarkasagsol')
pencere_kutu(y, V(TPX - 0.09, TPY - 0.03), X, -Y, 0.07, 0.05, 0.04, 0.08, 'ahsap_koyu', cerceve='mermer')
for x in (TPX - 0.075, TPX - 0.025, TPX + 0.025, TPX + 0.075):
    sutun(y, x, TPY - 0.085, Z0 + 0.05, Z0 + 0.17, 0.009, 'mermer', 'iyon', yiv=12)
kutu(y, V(TPX - 0.09, TPY - 0.1, Z0 + 0.17), X, 0.18, 0.07, 0.02, 'siva_krem', 'onsagsol')
kavetto(y, dikdortgen(TPX - 0.09, TPX + 0.09, TPY - 0.1, TPY + 0.09), Z0 + 0.19, 0.03, 0.016, 'kum_acik')
tanit_heykel(y, TPX, TPY - 0.06, Z0 + 0.22, 0.07, 'altin', aci=-math.pi / 2)
kanatli_gunes(y, V(TPX, TPY - 0.1, Z0 + 0.18), X, -Y, 0.1, 0.014)

# ---------------- outside: the road, scattered stones ----------------
y.bolum('Dış taraf')
for k in range(10):
    x, yy = rn.uniform(-1.15, 1.15), rn.uniform(-1.12, -0.95)
    if abs(x - GX) < 0.1: continue
    kure(y, (x, yy, Z0 - 0.004), rn.uniform(0.01, 0.022), rn.choice(('kaya', 'kaya_koyu')), n=7, kat=4)
for x, yy in ((-1.0, -1.02), (0.4, -1.05), (1.14, -0.3), (1.14, 0.5), (1.13, 1.0), (0.05, -1.0)):
    agac(y, x, yy, Z0, rn.uniform(0.1, 0.14), 'yapraklı', 'zeytin', 'ahsap')
insan(y, GX + 0.03, -1.07, Z0, 'kumas', s=1.1, aci=math.pi / 2)
at(y, GX - 0.02, -1.03, Z0, math.pi / 2, s=1.15, key='ahsap_acik', binici='boya_kirmizi', eger='kumas')

calistir(y, 'lm_kartacasur')
