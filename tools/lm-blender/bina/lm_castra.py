# Castra (lm_castra): a permanent legionary fortress in the "playing card" plan - a stone curtain wall with rounded
# corners, merlons and tile-roofed interval and corner towers, an earth rampart behind it, a V ditch with timber
# bridges, four double-arched gatehouses with galleries; inside, the paved via praetoria / principalis / decumana, the
# principia (gate range, colonnaded courtyard, tall cross hall, the standards with the eagle), the praetorium round its
# peristyle, buttressed granaries (horrea), rows of tile-roofed barracks with verandas and workshops.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04
S = 1.13                 # ground half size
W = 0.92                 # wall line (outer face) half size
RC = 0.22                # corner radius of the wall line
GX = 0.14                # half width of the gate zone (the wall breaks there)
HW = 0.21                # wall height (raised over the real proportion: the game shrinks the camp to one tile)
KAL = 0.05               # wall thickness


# ---------------------------------------------------------------- helpers
def rkare(d, n=6):
    """the rounded square ring offset d from the wall line (CCW)"""
    h, r = W + d, max(0.004, RC + d)
    pts = []
    for k, (cx, cy) in enumerate(((h - r, -(h - r)), (h - r, h - r), (-(h - r), h - r), (-(h - r), -(h - r)))):
        a0 = -math.pi / 2 + k * math.pi / 2
        for i in range(n + 1):
            a = a0 + (math.pi / 2) * i / n
            pts.append(V(cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ceyrek(d=0.0, n=6):
    """one quarter of the wall line offset d, from the front gate (x = GX) round the front-right corner to the right
    gate (y = -GX); the other quarters are this turned by 90 degrees"""
    h, r = W + d, max(0.004, RC + d)
    pts = [V(GX, -h)]
    for i in range(n + 1):
        a = -math.pi / 2 + (math.pi / 2) * i / n
        pts.append(V(h - r + r * math.cos(a), -(h - r) + r * math.sin(a)))
    pts.append(V(h, -GX))
    return pts


def dondur(pts, k):
    c, s = math.cos(k * math.pi / 2), math.sin(k * math.pi / 2)
    return [V(c * p.x - s * p.y, s * p.x + c * p.y, p.z) for p in pts]


def halka_yuzey(ic, dis, z_ic, z_dis, key):
    """the band between two rings of the same length (ic inside), faces up"""
    n = len(ic)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([V(ic[i].x, ic[i].y, z_ic), V(ic[j].x, ic[j].y, z_ic), V(dis[j].x, dis[j].y, z_dis), V(dis[i].x, dis[i].y, z_dis)], key, Z)


def kemer_cizgi(x0, x1, hs, k=10):
    R = (x1 - x0) / 2
    return [(x0, hs)] + [(x0 + R + R * math.cos(math.pi - math.pi * i / k), hs + R * math.sin(math.pi - math.pi * i / k)) for i in range(1, k)] + [(x1, hs)]


def gecit(a, b, z0, H, derin, en=0.5, ust=0.05, key='tas', ic_key='tas_koyu'):
    """a wall a->b (facing the right of a->b), derin thick, pierced by a round-arched passage you can see through"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W_ = (b - a).length; e = (b - a) / W_; nc = V(e.y, -e.x)
    L = lambda u, v, d=0.0: a + e * u - nc * d + Z * (z0 + v)
    x0, x1 = (1 - en) / 2 * W_, (1 + en) / 2 * W_
    hs = H - ust - (x1 - x0) / 2
    tp = kemer_cizgi(x0, x1, hs, 12)
    for d, yon in ((0.0, nc), (derin, -nc)):
        y.yuz_yon([L(0, 0, d), L(x0, 0, d), L(x0, H, d), L(0, H, d)], key, yon)
        y.yuz_yon([L(x1, 0, d), L(W_, 0, d), L(W_, H, d), L(x1, H, d)], key, yon)
        for k in range(len(tp) - 1):
            (ua, va), (ub, vb) = tp[k], tp[k + 1]
            y.yuz_yon([L(ua, va, d), L(ub, vb, d), L(ub, H, d), L(ua, H, d)], key, yon)
    yol = [(x0, 0)] + tp + [(x1, 0)]
    xm = (x0 + x1) / 2
    for k in range(len(yol) - 1):
        p, q = yol[k], yol[k + 1]
        m = L((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, derin / 2)
        y.yuz_yon([L(*p, 0), L(*q, 0), L(*q, derin), L(*p, derin)], ic_key, L(xm, hs * 0.5, derin / 2) - m)
    # voussoirs: a raised ring of stones round the arch on both faces
    for d, s in ((-0.002, 1), (derin + 0.002, -1)):
        for k in range(len(tp) - 1):
            if k % 2: continue
            (ua, va), (ub, vb) = tp[k], tp[k + 1]
            m = V(xm, hs)
            da = (V(ua, va) - m).normalized() * 0.012; db = (V(ub, vb) - m).normalized() * 0.012
            y.yuz_yon([L(ua, va, d), L(ub, vb, d), L(ub + db.x, vb + db.y, d), L(ua + da.x, va + da.y, d)], 'tas_acik', nc * s)
    return L, x0, x1, hs


def sutun_hafif(cx, cy, z0, z1, r=0.01, key='kirec'):
    """a light Tuscan column (~110 triangles)"""
    H = z1 - z0; c = (cx, cy); n = 10
    hb, hc = H * 0.06, H * 0.1
    kutu_merkez(y, c, r * 2.6, r * 2.6, hb * 0.5, key, z0=z0)
    donel(y, c, [(r * 1.25, z0 + hb * 0.5), (r * 1.0, z0 + hb)], key, n=n)
    y.prizma(c, r, z0 + hb, z1 - hc, key, n=n, ust=False)
    donel(y, c, [(r * 0.92, z1 - hc), (r * 1.3, z1 - hc * 0.45)], key, n=n)
    kutu_merkez(y, c, r * 2.7, r * 2.7, hc * 0.45, key, z0=z1 - hc * 0.45)


def kiremit_kaburga(p0, p1, w=0.005, key='kiremit2'):
    p0, p1 = Vector(p0), Vector(p1)
    t = (p1 - p0).normalized()
    s = Z.cross(t)
    if s.length < 1e-6: s = X.copy()
    s.normalize(); u = t.cross(s).normalized()
    if u.z < 0: u = -u
    h = u * (w * 0.55)
    y.yuz_yon([p0 - s * (w / 2), p1 - s * (w / 2), p1 + h, p0 + h], key, u - s)
    y.yuz_yon([p0 + h, p1 + h, p1 + s * (w / 2), p0 + s * (w / 2)], key, u + s)


def kaburgali_besik(x0, x1, y0, y1, z, h, sacak=0.02, adim=0.034, **kw):
    """a tiled gable roof (ridge along the longer side) with imbrex ribs"""
    kw.setdefault('ns', 4); kw.setdefault('nr', 3)
    zr = cati_besik(y, x0, x1, y0, y1, z, h, sacak, kw.pop('key', 'kiremit'), mahya=kw.pop('mahya', 'kiremit2'), **kw)
    if (x1 - x0) >= (y1 - y0):
        n = max(2, int((x1 - x0) / adim))
        for j in range(n + 1):
            xx = x0 + (x1 - x0) * j / n
            for ye in (y0 - sacak, y1 + sacak):
                kiremit_kaburga(V(xx, ye, z + 0.0015), V(xx, (y0 + y1) / 2, z + h + 0.0015))
    else:
        n = max(2, int((y1 - y0) / adim))
        for j in range(n + 1):
            yy = y0 + (y1 - y0) * j / n
            for xe in (x0 - sacak, x1 + sacak):
                kiremit_kaburga(V(xe, yy, z + 0.0015), V((x0 + x1) / 2, yy, z + h + 0.0015))
    return zr


def signum(x, yy, z, boy=0.2, kartal=False):
    """a legion standard: a pole with stacked gilt discs (phalerae), a wreath and a spear tip - or the eagle (aquila)"""
    y.silindir((x, yy), 0.003, z, z + boy, 'ahsap', n=5)
    if kartal:
        zt = z + boy
        kure(y, (x, yy, zt + 0.008), 0.007, 'altin', n=8, kat=4)
        for s in (-1, 1):
            y.yuz_yon([V(x, yy, zt + 0.01), V(x + s * 0.03, yy, zt + 0.03), V(x + s * 0.026, yy, zt + 0.012), V(x + s * 0.008, yy, zt + 0.004)],
                      'altin', V(0, -1, 0))
            y.yuz_yon([V(x, yy + 0.001, zt + 0.01), V(x + s * 0.03, yy + 0.001, zt + 0.03), V(x + s * 0.026, yy + 0.001, zt + 0.012),
                       V(x + s * 0.008, yy + 0.001, zt + 0.004)], 'altin', V(0, 1, 0))
        boru(y, [V(x - 0.012, yy, zt - 0.012), V(x + 0.012, yy, zt - 0.012)], 0.004, 'altin', n=5)
    else:
        for k in range(4):
            zz = z + boy * (0.45 + 0.1 * k)
            y.prizma((x, yy), 0.009, zz, zz + 0.006, 'altin', n=10)
        boru(y, [V(x - 0.014, yy, z + boy * 0.9), V(x + 0.014, yy, z + boy * 0.9)], 0.002, 'ahsap', n=4)
        boru(y, [V(x + 0.011 * math.cos(TAU * k / 10), yy, z + boy * 0.97 + 0.011 * math.sin(TAU * k / 10)) for k in range(11)], 0.0025, 'altin',
             n=4, kapat=False)
        y.koni((x, yy), 0.004, z + boy, 0.02, 'demir', n=5)


# ================================================================ ground: grass, ditch, berm, interior
y.bolum('Zemin, hendek, berm')
kutu(y, V(-S, -S, 0), X, 2 * S, 2 * S, Z0, 'tas_koyu', 'onarkasagsol')
R_cim = rkare(0.17)
kare = []
for p in R_cim:
    m = max(abs(p.x), abs(p.y))
    kare.append(p * (S / m))
halka_yuzey(R_cim, kare, Z0, Z0, 'cimen')
ZD = Z0 - 0.04
halka_yuzey(rkare(0.125), rkare(0.17), ZD + 0.006, Z0, 'toprak')     # ditch: outer slope
halka_yuzey(rkare(0.1), rkare(0.125), ZD, ZD + 0.006, 'toprak')
halka_yuzey(rkare(0.03), rkare(0.1), Z0, ZD, 'toprak')               # inner (steeper) slope
halka_yuzey(rkare(-0.01), rkare(0.03), Z0, Z0, 'zemin')                # the berm (under the wall's foot)
ic_zemin = rkare(-0.17)
y.yuz_yon([V(p.x, p.y, Z0) for p in ic_zemin], 'toprak', Z)
# roads (paved): via praetoria, via principalis, via decumana
ZR = Z0 + 0.0015
for (a0, a1, b0, b1) in ((-0.065, 0.065, -W + 0.02, -0.065), (-W + 0.02, W - 0.02, -0.065, 0.065), (-0.055, 0.055, 0.6, W - 0.02)):
    y.yuz([V(a0, b0, ZR), V(a1, b0, ZR), V(a1, b1, ZR), V(a0, b1, ZR)], 'zemin')
    for xx in ((a0, a0 + 0.006), (a1 - 0.006, a1)) if (b1 - b0) > (a1 - a0) else ():
        y.yuz([V(xx[0], b0, ZR + 0.001), V(xx[1], b0, ZR + 0.001), V(xx[1], b1, ZR + 0.001), V(xx[0], b1, ZR + 0.001)], 'tas_koyu')
    if (a1 - a0) > (b1 - b0):
        for yy in ((b0, b0 + 0.006), (b1 - 0.006, b1)):
            y.yuz([V(a0, yy[0], ZR + 0.001), V(a1, yy[0], ZR + 0.001), V(a1, yy[1], ZR + 0.001), V(a0, yy[1], ZR + 0.001)], 'tas_koyu')

# ================================================================ walls, rampart, towers
y.bolum('Sur, toprak set, kuleler')
for k in range(4):
    yol = dondur(ceyrek(0.0), k)
    sur(y, yol, Z0, HW, KAL, 'tas', kapali=False, mazgal_h=0.026, parapet_h=0.014, ust_key='zemin')
    silme(y, yol, Z0, 0.02, 0.01, 'tas_koyu', 'kaide', kapali=False)
    silme(y, yol, Z0 + HW - 0.012, 0.012, 0.006, 'tas_acik', 'duz', kapali=False)
    # the earth rampart (agger) banked against the wall's inside
    a_ = disa(yol, -KAL, False); b_ = disa(yol, -0.17, False)
    zt = Z0 + HW - 0.025
    for i in range(len(a_) - 1):
        y.yuz_yon([V(a_[i].x, a_[i].y, zt), V(a_[i + 1].x, a_[i + 1].y, zt), V(b_[i + 1].x, b_[i + 1].y, Z0), V(b_[i].x, b_[i].y, Z0)], 'cimen', Z)
    for i, sg in ((0, -1), (len(a_) - 1, 1)):
        e = (a_[1] - a_[0]) if i == 0 else (a_[-1] - a_[-2])
        y.yuz_yon([V(a_[i].x, a_[i].y, Z0), V(b_[i].x, b_[i].y, Z0), V(a_[i].x, a_[i].y, zt)], 'toprak', e * sg)
    # towers: two interval towers and a corner tower per quarter
    q = W - RC + RC * math.cos(math.pi / 4)
    for (tx, ty, ac) in ((0.52, -W + 0.035, 0.0), (W - 0.035, -0.52, 0.0), (q - 0.03, -q + 0.03, math.pi / 4)):
        p = dondur([V(tx, ty)], k)[0]
        with parca(y, (p.x, p.y, 0), ac + k * math.pi / 2):
            kule_kare(y, 0, 0, 0.11, Z0, HW + 0.12, 'tas', 'piramit', 'kiremit', cati_h=0.08, mazgal_h=0, sacak=0.015, yarik_say=1, cati_ns=4, cati_nr=3,
                      konsol=False)
            kornis(y, -0.055, 0.055, -0.055, 0.055, Z0 + HW + 0.03, 0.01, 0.006, 'tas_acik', 'duz')
            kornis(y, -0.055, 0.055, -0.055, 0.055, Z0 + HW + 0.11, 0.01, 0.006, 'tas_acik', 'duz')
            for s in range(4):   # an arched window on each face of the top storey
                ex = dondur([V(1, 0)], s)[0]; nn = V(ex.y, -ex.x)
                o = V(0, 0) + nn * 0.0555 - ex * 0.055
                y.pencere(o + Z * Z0, ex, nn, 0.0425, HW + 0.055, 0.025, 0.04, 'koyu')

# ================================================================ gatehouses
y.bolum('Kapılar (çift kemerli, galerili, köprülü)')
for k, (gx, gy) in enumerate(((0, -W), (W, 0), (0, W), (-W, 0))):
    with parca(y, (gx, gy, 0), k * math.pi / 2):
        # ground through the gate zone, the timber bridge over the ditch
        y.yuz([V(-GX, 0.0, Z0), V(GX, 0.0, Z0), V(GX, 0.17, Z0), V(-GX, 0.17, Z0)], 'toprak')
        kutu(y, V(-0.09, -0.19, Z0 - 0.004), X, 0.18, 0.17, 0.01, 'ahsap', 'onarkasagsolust')
        for s in (-1, 1):
            for yy in (-0.18, -0.11, -0.04):
                y.prizma((s * 0.085, yy), 0.004, Z0 + 0.006, Z0 + 0.04, 'ahsap_koyu', n=5)
                y.prizma((s * 0.085, yy), 0.004, ZD, Z0 - 0.004, 'ahsap_koyu', n=5, ust=False)
            boru(y, [V(s * 0.085, -0.185, Z0 + 0.038), V(s * 0.085, -0.035, Z0 + 0.038)], 0.003, 'ahsap', n=5)
        # flanking towers
        HG = HW + 0.24                         # gate towers: the tallest masses of the circuit
        for s in (-1, 1):
            zt_ = kule_kare(y, s * 0.2, -0.02, 0.13, Z0, HG, 'tas', 'piramit', 'kiremit', cati_h=0.1, mazgal_h=0, sacak=0.017, yarik_say=0, cati_ns=4, cati_nr=3,
                            konsol=False)
            silme(y, dikdortgen(s * 0.2 - 0.065, s * 0.2 + 0.065, -0.085, 0.045), Z0, 0.022, 0.01, 'tas_koyu', 'kaide')
            for zz in (Z0 + HW + 0.005, Z0 + HW + 0.12, Z0 + HG - 0.012):
                kornis(y, s * 0.2 - 0.065, s * 0.2 + 0.065, -0.085, 0.045, zz, 0.01, 0.006, 'tas_acik', 'duz')
            for side in range(4):
                ex = dondur([V(1, 0)], side)[0]; nn = V(ex.y, -ex.x)
                o = V(s * 0.2, -0.02) + nn * 0.0655 - ex * 0.065
                for u0 in (0.027, 0.078):
                    y.pencere(o + Z * Z0, ex, nn, u0, HW + 0.035, 0.024, 0.045, 'koyu')
                    y.pencere(o + Z * Z0, ex, nn, u0, HW + 0.15, 0.024, 0.05, 'koyu')
                y.pencere(o + Z * Z0, ex, nn, 0.061, 0.07, 0.008, 0.045, 'koyu', kemer=False)   # an arrow slit low down
            if s > 0:   # the banner flies from the right gate tower's apex
                sancak(y, s * 0.2, -0.02, zt_ - 0.012, boy=0.18, en=0.1, yuk=0.065, aci=-math.pi / 2 + 0.6)
        # the gate block: two arched carriageways, a moulding, a windowed gallery and its roof
        GD0, GD1 = -0.04, 0.05
        for (xa, xb) in ((-0.14, 0.0), (0.0, 0.14)):
            gecit(V(xa, GD0), V(xb, GD0), Z0, HW, GD1 - GD0, en=0.62, ust=0.03, key='tas', ic_key='tas_koyu')
        kornis(y, -0.14, 0.14, GD0, GD1, Z0 + HW - 0.01, 0.012, 0.008, 'tas_acik', 'kaba')
        y.yuz_yon([V(-0.14, GD0, Z0 + HW), V(0.14, GD0, Z0 + HW), V(0.14, GD1, Z0 + HW), V(-0.14, GD1, Z0 + HW)], 'tas', Z)
        ZG = Z0 + HW + 0.002
        HGal = 0.09
        pencereli_duvar(y, [V(-0.14, GD0 + 0.01), V(0.14, GD0 + 0.01)], ZG, HGal, [5], kapali=False, renk=('tas', 'tas_koyu', 'tas_acik', 'koyu'),
                        v0=0.018, en=0.5, ust=0.016, derin=0.012, k_say=6, sivri=0.0, cerceve=(0.005, 'tas_acik'))
        pencereli_duvar(y, [V(0.14, GD1 - 0.01), V(-0.14, GD1 - 0.01)], ZG, HGal, [5], kapali=False, renk=('tas', 'tas_koyu', 'tas_acik', 'koyu'),
                        v0=0.018, en=0.5, ust=0.016, derin=0.012, k_say=6, sivri=0.0)
        kornis(y, -0.14, 0.14, GD0 + 0.01, GD1 - 0.01, ZG + HGal - 0.01, 0.01, 0.006, 'tas_acik', 'duz')
        kaburgali_besik(-0.14, 0.14, GD0 + 0.01, GD1 - 0.01, ZG + HGal, 0.05, sacak=0.014, ucluk_key='tas', alinlik_key='tas_acik', adim=0.034)
        # an inscription panel over the arches
        kutu(y, V(-0.05, GD0 - 0.003, Z0 + HW - 0.032), X, 0.1, 0.003, 0.02, 'kirec', 'onsagsolust')
        for j in range(5):
            y.yuz_yon([V(-0.04 + j * 0.017, GD0 - 0.0045, Z0 + HW - 0.025), V(-0.03 + j * 0.017, GD0 - 0.0045, Z0 + HW - 0.025),
                       V(-0.03 + j * 0.017, GD0 - 0.0045, Z0 + HW - 0.02), V(-0.04 + j * 0.017, GD0 - 0.0045, Z0 + HW - 0.02)], 'koyu', -Y)

# ================================================================ principia
y.bolum('Principia: giriş kanadı, avlu, haç salonu')
PX = 0.25
PY0, PY1 = 0.14, 0.57
# gate range
FR1 = PY0 + 0.075
for a, b in ((V(-PX, PY0), V(-0.06, PY0)), (V(0.06, PY0), V(PX, PY0)), (V(PX, PY0), V(PX, FR1)), (V(PX, FR1), V(0.06, FR1)),
             (V(-0.06, FR1), V(-PX, FR1)), (V(-PX, FR1), V(-PX, PY0))):
    duz_duvar(y, a, b, Z0, Z0 + 0.1, 'siva_krem')
for xs_ in (-0.06, 0.06):
    a, b = (V(xs_, PY0 - 0.002), V(xs_, FR1 + 0.002)) if xs_ > 0 else (V(xs_, FR1 + 0.002), V(xs_, PY0 - 0.002))
    duz_duvar(y, a, b, Z0 + 0.1, Z0 + 0.13, 'tas')
gecit(V(-0.06, PY0 - 0.002), V(0.06, PY0 - 0.002), Z0, 0.13, FR1 - PY0 + 0.004, en=0.55, ust=0.02, key='tas', ic_key='tas_koyu')
for s in (-1, 1):
    for u in (0.1, 0.17):
        y.pencere(V(s * u - 0.012, PY0, Z0), X, -Y, 0, 0.045, 0.024, 0.035, 'koyu')
kaburgali_besik(-PX, -0.06, PY0, FR1, Z0 + 0.1, 0.04, sacak=0.012, ucluk_key='siva_krem')
kaburgali_besik(0.06, PX, PY0, FR1, Z0 + 0.1, 0.04, sacak=0.012, ucluk_key='siva_krem')
kornis(y, -0.065, 0.065, PY0 - 0.004, FR1 + 0.004, Z0 + 0.13, 0.014, 0.01, 'tas_acik', 'tac')
duvarlar(y, dikdortgen(-0.06, 0.06, PY0 - 0.004, FR1 + 0.004), Z0 + 0.144, Z0 + 0.15, 'tas')
cati_kirma(y, -0.06, 0.06, PY0 - 0.004, FR1 + 0.004, Z0 + 0.15, 0.04, 0.012, 'kiremit', 'kiremit2', ns=4, nr=3)
# courtyard: paving, side ranges with inward porticoes, a well
CY0, CY1 = FR1, 0.40
y.yuz([V(-PX + 0.08, CY0, Z0 + 0.002), V(PX - 0.08, CY0, Z0 + 0.002), V(PX - 0.08, CY1, Z0 + 0.002), V(-PX + 0.08, CY1, Z0 + 0.002)], 'zemin')
for s in (-1, 1):
    xo, xi = s * PX, s * (PX - 0.05)
    a, b = (V(xo, CY0), V(xo, CY1)) if s > 0 else (V(xo, CY1), V(xo, CY0))
    duz_duvar(y, a, b, Z0, Z0 + 0.09, 'siva_krem')
    for k in range(3):
        y.pencere(a.lerp(b, (k + 0.5) / 3) - (b - a).normalized() * 0.012 + Z * Z0, (b - a).normalized(), V(s, 0), 0, 0.04, 0.024, 0.032, 'koyu')
    ai, bi = (V(xi, CY1), V(xi, CY0)) if s > 0 else (V(xi, CY0), V(xi, CY1))
    duz_duvar(y, ai, bi, Z0, Z0 + 0.09, 'siva_krem')
    for k in range(4):
        y.pencere(ai.lerp(bi, (k + 0.5) / 4) - (bi - ai).normalized() * 0.01 + Z * Z0, (bi - ai).normalized(), V(-s, 0), 0, 0.0, 0.02, 0.05, 'ahsap_koyu', kemer=False)
    cati_besik(y, min(xo, xi), max(xo, xi), CY0, CY1, Z0 + 0.09, 0.03, 0.012, 'kiremit', mahya='kiremit2', ucluk_key='siva_krem', ns=4, nr=3)
    # portico columns in front of the side range
    xc = s * (PX - 0.075)
    for k in range(5):
        sutun_hafif(xc, CY0 + 0.015 + (CY1 - CY0 - 0.03) * k / 4, Z0, Z0 + 0.075, 0.007, 'kirec')
    y.yuz_yon([V(min(xc, xi) - 0.005, CY0, Z0 + 0.075), V(max(xc, xi) + 0.005, CY0, Z0 + 0.075), V(max(xc, xi) + 0.005, CY1, Z0 + 0.075),
               V(min(xc, xi) - 0.005, CY1, Z0 + 0.075)], 'kiremit', Z)
    kutu_merkez(y, (xc, (CY0 + CY1) / 2), 0.012, CY1 - CY0, 0.007, 'kirec', z0=Z0 + 0.068)
# the standards in the courtyard: the legion's eagle and the cohorts' signa on a tribunal
TRY = 0.3
kutu_merkez(y, (0, TRY), 0.2, 0.06, 0.018, 'tas', z0=Z0)
kornis(y, -0.1, 0.1, TRY - 0.03, TRY + 0.03, Z0 + 0.012, 0.008, 0.005, 'tas_acik', 'tac')
signum(0, TRY, Z0 + 0.02, 0.2, kartal=True)
for s in (-1, 1):
    for u in (0.04, 0.08):
        signum(s * u, TRY - 0.005 + 0.01 * (u > 0.05), Z0 + 0.02, 0.17)
# the cross hall (basilica principiorum): the tallest roof inside the walls, clerestory windows, a gable roof
y.bolum('Principia: haç salonu ve sancaklar')
HY0, HY1 = CY1, 0.53
hall = dikdortgen(-PX, PX, HY0, HY1)
ZH1, ZH2 = Z0 + 0.2, Z0 + 0.3
silme(y, hall, Z0, 0.014, 0.006, 'tas', 'kaide')
silme(y, hall, ZH1 - 0.012, 0.012, 0.007, 'tas_acik', 'duz')
for i, n_ in enumerate((6, 2, 6, 2)):          # tall arched windows in the lower walls
    a, b = hall[i], hall[(i + 1) % 4]
    if i == 0:                                   # (the courtyard side: the door and the side ranges)
        duz_duvar(y, a, b, Z0, ZH1, 'siva_krem'); continue
    duz_duvar(y, a, b, Z0, Z0 + 0.03, 'siva_krem')
    pencereli_duvar(y, [a, b], Z0 + 0.03, 0.15, [n_], kapali=False, renk=('siva_krem', 'tas_koyu', 'tas_acik', 'cam'), v0=0.03, en=0.42,
                    ust=0.025, derin=0.01, k_say=6, sivri=0.0, cerceve=(0.005, 'tas_acik'))
    duz_duvar(y, a, b, Z0 + 0.18, ZH1, 'siva_krem')
pencereli_duvar(y, hall, ZH1, ZH2 - ZH1, [6, 2, 6, 2], renk=('tas', 'tas_koyu', 'tas_acik', 'cam'), v0=0.015, en=0.5, ust=0.015, derin=0.012,
                k_say=6, sivri=0.0)
silme(y, hall, ZH2 - 0.012, 0.012, 0.008, 'tas_acik', 'tac')
kaburgali_besik(-PX, PX, HY0, HY1, ZH2, 0.085, sacak=0.018, ucluk_key='siva_krem', alinlik_key='tas_acik')
for s in (-1, 1):                               # acroteria at the gable ends
    kure(y, (s * (PX + 0.004), (HY0 + HY1) / 2, ZH2 + 0.095), 0.009, 'altin', n=8, kat=4)
# a door from the courtyard into the hall, the aedes (shrine of the standards) projecting at the back
y.pencere(V(-0.03, HY0, Z0), X, -Y, 0, 0, 0.06, 0.1, 'ahsap_koyu')
duvarlar(y, dikdortgen(-0.07, 0.07, HY1, PY1 + 0.02), Z0, Z0 + 0.16, 'tas')
silme(y, [V(0.07, HY1), V(0.07, PY1 + 0.02), V(-0.07, PY1 + 0.02), V(-0.07, HY1)], Z0 + 0.15, 0.012, 0.008, 'tas_acik', 'tac', kapali=False)
alinlik(y, V(0.08, PY1 + 0.025), V(-0.08, PY1 + 0.025), Z0 + 0.162, 0.045, derin=PY1 + 0.025 - HY1, key='tas_acik', ic_key='tas', c=0.008,
        cati_key='kiremit')

# ================================================================ groma
# (the monumental four-way arch over the crossing of the via praetoria and the via principalis, before the
#  principia - as at Lambaesis: two storeys, engaged columns, an inscription, a tiled pyramid roof)
y.bolum('Groma: dört yönlü anıtsal kapı')
GC = V(0.0, -0.012)
GA = 0.1                      # half size
GH = 0.27                     # arch storey
ZG0 = Z0 + 0.012
kutu_merkez(y, (GC.x, GC.y), 2 * GA + 0.02, 2 * GA + 0.02, 0.012, 'tas_koyu', z0=Z0)
for k in range(4):
    with parca(y, (GC.x, GC.y, 0), k * math.pi / 2):
        gecit(V(-GA, -GA), V(GA, -GA), ZG0, GH, 0.03, en=0.56, ust=0.05, key='tas', ic_key='tas_koyu')
        for xx in (-GA + 0.026, GA - 0.026):       # engaged columns on pedestals flanking the arch
            kutu_merkez(y, (xx, -GA - 0.006), 0.028, 0.014, 0.04, 'tas_acik', z0=ZG0)
            sutun_hafif(xx, -GA - 0.006, ZG0 + 0.04, ZG0 + GH - 0.03, 0.0085, 'kirec')
        kornis(y, -GA, GA, -GA - 0.016, -GA + 0.004, ZG0 + GH - 0.032, 0.012, 0.004, 'tas_acik', 'duz')
        kutu(y, V(-0.012, -GA - 0.004, ZG0 + GH - 0.06), X, 0.024, 0.004, 0.026, 'tas_acik', 'onsagsolust')   # keystone
        # upper storey: three arched windows a side
        pencereli_duvar(y, [V(-GA + 0.008, -GA + 0.008), V(GA - 0.008, -GA + 0.008)], ZG0 + GH + 0.012, 0.1, [3], kapali=False,
                        renk=('tas', 'tas_koyu', 'tas_acik', 'koyu'), v0=0.02, en=0.48, ust=0.016, derin=0.012, k_say=6, sivri=0.0,
                        cerceve=(0.004, 'tas_acik'))
        for xx in (-GA + 0.016, GA - 0.016):       # pilasters on the upper storey
            kutu(y, V(xx - 0.007, -GA + 0.004, ZG0 + GH + 0.012), X, 0.014, 0.004, 0.1, 'tas_acik', 'onsagsol')
y.yuz_yon([V(GC.x + p.x, GC.y + p.y, ZG0 + GH - 0.002) for p in dikdortgen(-GA + 0.03, GA - 0.03, -GA + 0.03, GA - 0.03)], 'tas_koyu', -Z)
y.yuz_yon([V(GC.x + p.x, GC.y + p.y, ZG0 + GH) for p in dikdortgen(-GA, GA, -GA, GA)], 'tas', Z)
kornis(y, GC.x - GA, GC.x + GA, GC.y - GA, GC.y + GA, ZG0 + GH - 0.004, 0.016, 0.014, 'tas_acik', 'tac')
ZGU = ZG0 + GH + 0.112
kornis(y, GC.x - GA + 0.008, GC.x + GA - 0.008, GC.y - GA + 0.008, GC.y + GA - 0.008, ZGU - 0.006, 0.014, 0.01, 'tas_acik', 'tac')
# the dedication on the front face over the arch
kutu(y, V(GC.x - 0.05, GC.y - GA - 0.003, ZG0 + GH - 0.03 - 0.022), X, 0.1, 0.003, 0.02, 'kirec', 'onsagsolust')
for j in range(5):
    y.yuz_yon([V(GC.x - 0.04 + j * 0.017, GC.y - GA - 0.0045, ZG0 + GH - 0.045), V(GC.x - 0.03 + j * 0.017, GC.y - GA - 0.0045, ZG0 + GH - 0.045),
               V(GC.x - 0.03 + j * 0.017, GC.y - GA - 0.0045, ZG0 + GH - 0.04), V(GC.x - 0.04 + j * 0.017, GC.y - GA - 0.0045, ZG0 + GH - 0.04)],
              'koyu', -Y)
zr_ = cati_kirma(y, GC.x - GA + 0.008, GC.x + GA - 0.008, GC.y - GA + 0.008, GC.y + GA - 0.008, ZGU + 0.008, 0.09, 0.016, 'kiremit', 'kiremit2', ns=4, nr=3)
sancak(y, GC.x, GC.y, zr_ - 0.01, boy=0.2, en=0.1, yuk=0.065, aci=-math.pi / 2 - 0.5)

# ================================================================ praetorium
y.bolum('Praetorium (komutan evi)')
QX0, QX1, QY0, QY1 = 0.33, 0.71, 0.135, 0.5
RW = 0.08
HQ = 0.085
for (x0, x1, y0, y1) in ((QX0, QX1, QY0, QY0 + RW), (QX0, QX1, QY1 - RW, QY1)):
    duvarlar(y, dikdortgen(x0, x1, y0, y1), Z0, Z0 + HQ, 'siva_krem')
    silme(y, dikdortgen(x0, x1, y0, y1), Z0, 0.014, 0.005, 'siva_kirmizi', 'duz')
    kaburgali_besik(x0, x1, y0, y1, Z0 + HQ, 0.04, sacak=0.014, ucluk_key='siva_krem')
for (x0, x1) in ((QX0, QX0 + RW), (QX1 - RW, QX1)):
    duvarlar(y, dikdortgen(x0, x1, QY0 + RW, QY1 - RW), Z0, Z0 + HQ, 'siva_krem')
    kaburgali_besik(x0, x1, QY0 + RW, QY1 - RW, Z0 + HQ, 0.04, sacak=0.014, ucluk_key='siva_krem')
# windows on the outside, the entrance with a porch
for xx in (0.38, 0.45, 0.6, 0.67):
    y.pencere(V(xx - 0.012, QY0, Z0), X, -Y, 0, 0.04, 0.024, 0.03, 'koyu')
for yy in (0.18, 0.27, 0.36, 0.45):
    y.pencere(V(QX0, yy + 0.012, Z0), -Y, -X, 0, 0.04, 0.024, 0.03, 'koyu')
y.pencere(V(0.505, QY0, Z0), X, -Y, 0, 0.0, 0.04, 0.06, 'ahsap_koyu')
for s in (-1, 1):
    sutun_hafif(0.525 + s * 0.04, QY0 - 0.035, Z0, Z0 + 0.065, 0.006, 'kirec')
alinlik(y, V(0.475, QY0 - 0.045), V(0.575, QY0 - 0.045), Z0 + 0.065, 0.03, derin=0.045, key='kirec', ic_key='siva_krem', c=0.006, cati_key='kiremit')
# the peristyle garden in the middle
gx0, gx1, gy0, gy1 = QX0 + RW, QX1 - RW, QY0 + RW, QY1 - RW
y.yuz([V(gx0, gy0, Z0 + 0.002), V(gx1, gy0, Z0 + 0.002), V(gx1, gy1, Z0 + 0.002), V(gx0, gy1, Z0 + 0.002)], 'zemin')
y.yuz([V(gx0 + 0.03, gy0 + 0.03, Z0 + 0.004), V(gx1 - 0.03, gy0 + 0.03, Z0 + 0.004), V(gx1 - 0.03, gy1 - 0.03, Z0 + 0.004),
       V(gx0 + 0.03, gy1 - 0.03, Z0 + 0.004)], 'cimen')
for (xx, yy) in ((gx0 + 0.015, gy0 + 0.015), (gx1 - 0.015, gy0 + 0.015), (gx1 - 0.015, gy1 - 0.015), (gx0 + 0.015, gy1 - 0.015),
                 ((gx0 + gx1) / 2, gy0 + 0.015), ((gx0 + gx1) / 2, gy1 - 0.015)):
    sutun_hafif(xx, yy, Z0, Z0 + HQ - 0.01, 0.005, 'kirec')
agac(y, (gx0 + gx1) / 2, (gy0 + gy1) / 2, Z0, boy=0.1, tur='servi', key='cimen')

# ================================================================ granaries
y.bolum('Ambarlar (horrea)')
for (y0, y1, porch) in ((0.12, 0.26, True), (0.31, 0.45, False)):
    x0, x1 = -0.71, -0.33
    kutu(y, V(x0 - 0.01, y0 - 0.01, Z0), X, x1 - x0 + 0.02, y1 - y0 + 0.02, 0.025, 'tas_koyu', 'onarkasagsolust')
    zf = Z0 + 0.025
    duvarlar(y, dikdortgen(x0, x1, y0, y1), zf, zf + 0.1, 'tas')
    for k in range(7):        # buttresses and the floor's air vents
        xx = x0 + 0.02 + (x1 - x0 - 0.04) * k / 6
        for yy, s in ((y0, -1), (y1, 1)):
            kutu_merkez(y, (xx, yy + s * 0.01), 0.016, 0.02, 0.085, 'tas', z0=zf)
            if k == 6: continue
            y.yuz_yon([V(xx + 0.014, yy + s * 0.0005, Z0 + 0.008), V(xx + 0.028, yy + s * 0.0005, Z0 + 0.008), V(xx + 0.028, yy + s * 0.0005, Z0 + 0.018),
                       V(xx + 0.014, yy + s * 0.0005, Z0 + 0.018)], 'koyu', V(0, s))
            if k < 6:
                y.pencere(V(xx + 0.016, yy, zf), X if s < 0 else -X, V(0, s), 0 if s < 0 else -0.02, 0.06, 0.008, 0.02, 'koyu', kemer=False)
    silme(y, dikdortgen(x0, x1, y0, y1), zf + 0.09, 0.01, 0.006, 'tas_acik', 'duz')
    kaburgali_besik(x0, x1, y0, y1, zf + 0.1, 0.05, sacak=0.022, ucluk_key='tas', alinlik_key='tas_acik')
    # a door at the east end with a loading platform
    y.pencere(V(x1, (y0 + y1) / 2 - 0.02, zf), Y, X, 0, 0.0, 0.04, 0.06, 'ahsap_koyu', kemer=False)
    kutu_merkez(y, (x1 + 0.02, (y0 + y1) / 2), 0.04, 0.08, 0.025, 'tas', z0=Z0)
    if porch:
        for k in range(3):    # amphorae and sacks stacked by the door
            kure(y, (x1 + 0.03, (y0 + y1) / 2 - 0.03 + 0.03 * k, zf + 0.012), 0.01, 'kerpic', n=8, kat=4)
            y.prizma((x1 + 0.012, (y0 + y1) / 2 - 0.03 + 0.03 * k), 0.007, zf, zf + 0.018, 'kumas', n=6)

# ================================================================ barracks
y.bolum('Kışlalar (contubernia) ve atölyeler')


def kisla(x0, x1, y0, y1, yon):
    """a barrack block along y: rooms in a row with doors under a veranda on the yon side (+1 / -1 in x), the
    centurion's larger house at the y1 end (towards the via principalis)"""
    h = 0.072
    yc = y1 - 0.11
    duvarlar(y, dikdortgen(x0, x1, y0, yc), Z0, Z0 + h, 'siva_krem')
    silme(y, dikdortgen(x0, x1, y0, yc), Z0, 0.012, 0.004, 'tas', 'duz')
    kaburgali_besik(x0, x1, y0, yc, Z0 + h, 0.034, sacak=0.022, ucluk_key='siva_krem', adim=0.045)
    xs = x1 if yon > 0 else x0
    e = -Y if yon > 0 else Y
    nr = 8
    for k in range(nr):
        yy = y0 + (yc - y0) * (k + 0.5) / nr
        sg = 1 if yon > 0 else -1
        y.pencere(V(xs, yy + 0.008 * sg, Z0), e, V(yon, 0), 0, 0.0, 0.016, 0.042, 'ahsap_koyu', kemer=False)
        y.pencere(V(xs, yy - 0.016 * sg, Z0), e, V(yon, 0), 0, 0.025, 0.01, 0.012, 'koyu', kemer=False)
        y.prizma((xs + yon * 0.018, y0 + (yc - y0) * k / nr + 0.002), 0.0028, Z0, Z0 + h - 0.004, 'ahsap', n=4)
    cx0, cx1 = x0 - 0.012, x1 + 0.012
    duvarlar(y, dikdortgen(cx0, cx1, yc, y1), Z0, Z0 + h + 0.02, 'siva_krem')
    silme(y, dikdortgen(cx0, cx1, yc, y1), Z0, 0.012, 0.004, 'siva_kirmizi', 'duz')
    cati_kirma(y, cx0, cx1, yc, y1, Z0 + h + 0.02, 0.04, 0.016, 'kiremit', 'kiremit2', ns=4, nr=3)
    y.pencere(V((cx0 + cx1) / 2 - 0.01, y1, Z0), X, Y, 0, 0.0, 0.02, 0.05, 'ahsap_koyu', kemer=False)
    for xx in (cx0 + 0.014, cx1 - 0.024):
        y.pencere(V(xx, y1, Z0), X, Y, 0, 0.035, 0.01, 0.018, 'koyu', kemer=False)


# front half: four blocks each side of the via praetoria, doors facing in pairs across the lanes; the centurion's
# houses at the via principalis end
BW = 0.085
for s in (-1, 1):
    xs = [(0.72, 0.635, 1), (0.565, 0.48, -1), (0.42, 0.335, 1), (0.265, 0.18, -1)]
    for (xa, xb, yon) in xs:
        x0, x1 = sorted((s * xa, s * xb))
        kisla(x0, x1, -0.7, -0.105, yon * -s)
# back strip: workshops (fabrica) along the back, doors to the front
for s in (-1, 1):
    x0, x1 = sorted((s * 0.1, s * 0.7))
    duvarlar(y, dikdortgen(x0, x1, 0.62, 0.71), Z0, Z0 + 0.065, 'siva_krem')
    silme(y, dikdortgen(x0, x1, 0.62, 0.71), Z0, 0.012, 0.004, 'tas', 'duz')
    kaburgali_besik(x0, x1, 0.62, 0.71, Z0 + 0.065, 0.035, sacak=0.024, ucluk_key='siva_krem', adim=0.03)
    for k in range(8):
        xx = x0 + (x1 - x0) * (k + 0.5) / 8
        y.pencere(V(xx - 0.012, 0.62, Z0), X, -Y, 0, 0.0, 0.024, 0.045, 'ahsap_koyu', kemer=False)
        y.prizma((x0 + (x1 - x0) * k / 8 + 0.004, 0.6), 0.0028, Z0, Z0 + 0.058, 'ahsap', n=4)
    # barrels and crates in front
    for k in range(3):
        y.prizma((s * (0.2 + 0.12 * k), 0.585), 0.008, Z0, Z0 + 0.02, 'ahsap', n=8)
        kutu_merkez(y, (s * (0.25 + 0.12 * k), 0.587), 0.018, 0.018, 0.016, 'ahsap_acik', z0=Z0)

calistir(y, 'lm_castra')
