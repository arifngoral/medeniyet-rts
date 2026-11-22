# Limes fort (lm_limes): a late Roman frontier fort behind the limes - a grey stone curtain with tall projecting square
# towers (tile-roofed at the corners, merloned between), a twin-towered gatehouse with a gallery, a V ditch round the
# fort with a causeway; inside, barracks with verandas, a buttressed granary, the principia with its portico and
# standards. In front runs the limes itself: a ditch, an earth bank and a pointed log palisade with a timber gate, a
# stone-and-timber signal tower with a gallery and beacon, a timber watchtower on stilts; outside, a vaulted bath
# house with an apse and a few huts of the vicus among pines.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04
SX0, SX1, SY0, SY1 = -1.15, 1.15, -1.06, 1.0     # ground
FX, FY0, FY1 = 0.55, -0.42, 0.68                  # fort walls (outer faces): |x| <= FX, FY0 <= y <= FY1
LY = -0.97                                        # limes ditch centre line
PY = -0.85                                        # palisade line
HW = 0.22
KAL = 0.05


# ---------------------------------------------------------------- helpers
def kemer_cizgi(x0, x1, hs, k=10):
    R = (x1 - x0) / 2
    return [(x0, hs)] + [(x0 + R + R * math.cos(math.pi - math.pi * i / k), hs + R * math.sin(math.pi - math.pi * i / k)) for i in range(1, k)] + [(x1, hs)]


def gecit(a, b, z0, H, derin, en=0.5, ust=0.05, key='granit', ic_key='granit_koyu', tas='tas_acik'):
    """a wall a->b (facing the right of a->b), derin thick, pierced by a round-arched passage, with voussoirs"""
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
    for d, s in ((-0.002, 1), (derin + 0.002, -1)):
        for k in range(len(tp) - 1):
            if k % 2: continue
            (ua, va), (ub, vb) = tp[k], tp[k + 1]
            m = V(xm, hs)
            da = (V(ua, va) - m).normalized() * 0.014; db = (V(ub, vb) - m).normalized() * 0.014
            y.yuz_yon([L(ua, va, d), L(ub, vb, d), L(ub + db.x, vb + db.y, d), L(ua + da.x, va + da.y, d)], tas, nc * s)
    return L, x0, x1, hs


def sutun_hafif(cx, cy, z0, z1, r=0.01, key='kirec'):
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


def kaburgali_besik(x0, x1, y0, y1, z, h, sacak=0.02, adim=0.028, **kw):
    """a tiled gable roof (ridge along the longer side) with imbrex ribs"""
    key = kw.pop('key', 'kiremit')
    kw.setdefault('ns', 4); kw.setdefault('nr', 3)
    zr = cati_besik(y, x0, x1, y0, y1, z, h, sacak, key, mahya=kw.pop('mahya', 'kiremit2'), **kw)
    if key != 'kiremit': return zr
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
    y.silindir((x, yy), 0.003, z, z + boy, 'ahsap', n=5)
    if kartal:
        zt = z + boy
        kure(y, (x, yy, zt + 0.008), 0.007, 'altin', n=8, kat=4)
        for s in (-1, 1):
            for dy, nn in ((0, V(0, -1)), (0.001, V(0, 1))):
                y.yuz_yon([V(x, yy + dy, zt + 0.01), V(x + s * 0.03, yy + dy, zt + 0.03), V(x + s * 0.026, yy + dy, zt + 0.012),
                           V(x + s * 0.008, yy + dy, zt + 0.004)], 'altin', nn)
    else:
        for k in range(4):
            zz = z + boy * (0.45 + 0.1 * k)
            y.prizma((x, yy), 0.009, zz, zz + 0.006, 'altin', n=10)
        boru(y, [V(x + 0.011 * math.cos(TAU * k / 10), yy, z + boy * 0.97 + 0.011 * math.sin(TAU * k / 10)) for k in range(11)], 0.0025, 'altin',
             n=4, kapat=False)
        y.koni((x, yy), 0.004, z + boy, 0.02, 'demir', n=5)


def cam_agaci(x, yy, z, boy=0.2):
    """a fir: a short trunk and three stacked cones"""
    y.prizma((x, yy), 0.006, z, z + boy * 0.2, 'ahsap', n=5)
    for k, (r, z0, z1) in enumerate(((0.05, 0.12, 0.5), (0.04, 0.38, 0.75), (0.028, 0.62, 1.0))):
        donel(y, (x, yy), [(0.0, z + boy * z0 - 0.002), (r * boy / 0.2, z + boy * z0), (0, z + boy * z1)], 'boya_yesil', n=9, kat=k * 0.3)


def kule(cx, cy, w, h, cati='piramit', pencere_say=2):
    """a tall square fort tower: three storeys marked by string courses, slits below, arched windows at the top, a
    tiled pyramid roof (cati 'piramit') or a merloned platform (cati 'duz')"""
    t = kule_kare(y, cx, cy, w, Z0, h, 'granit', cati, 'kiremit', cati_h=w * 0.72, mazgal_h=0.03 if cati == 'duz' else 0, sacak=0.018, cati_ns=4, cati_nr=3,
                  yarik_say=1, konsol=(cati == 'duz'))
    silme(y, dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2), Z0, 0.025, 0.012, 'granit_koyu', 'kaide')
    for zz in (Z0 + 0.07, Z0 + 0.135):
        silme(y, dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2), zz, 0.012, 0.003, 'tugla_roma', 'duz')
    for zz in (Z0 + h * 0.38, Z0 + h * 0.7):
        kornis(y, cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2, zz, 0.01, 0.006, 'tas_acik', 'duz')
    for s in range(4):
        ex = [V(1, 0), V(0, 1), V(-1, 0), V(0, -1)][s]; nn = V(ex.y, -ex.x)
        o = V(cx, cy) + nn * (w / 2 + 0.0005) - ex * (w / 2)
        for k in range(pencere_say):
            u = w * (k + 1) / (pencere_say + 1) - 0.011
            y.pencere(o + Z * Z0, ex, nn, u, h * 0.76, 0.022, h * 0.15, 'koyu')
    return t


# ================================================================ ground with the ditches and the limes bank
y.bolum('Arazi: hendekler ve limes seti')


def kot(x, yy):
    h = 0.0
    d = max(abs(x) - FX, FY0 - yy, yy - FY1)
    if 0.05 < d < 0.17:
        t = (d - 0.05) / 0.05 if d < 0.1 else (1.0 if d < 0.12 else (0.17 - d) / 0.05)
        dep = 0.06 * t
        if yy < FY0 and FY0 - yy >= abs(x) - FX:          # the front ditch: a causeway in front of the gate
            dep *= min(1.0, max(0.0, (abs(x) - 0.08) / 0.06))
        h -= dep
    dy = abs(yy - LY)
    if dy < 0.075:              # the limes ditch: a broad V (Spitzgraben) with a narrow cleaning slot at the bottom
        t = 1.0 if dy < 0.008 else (0.075 - dy) / 0.067
        f = min(1.0, max(0.0, (abs(x) - 0.07) / 0.04)) * min(1.0, max(0.0, (1.08 - abs(x)) / 0.05))
        h -= 0.065 * t * f
    if -0.89 < yy < -0.8:
        t = min(1.0, (yy + 0.89) / 0.02, (-0.8 - yy) / 0.03)
        f = min(1.0, max(0.0, (abs(x) - 0.07) / 0.04)) * min(1.0, max(0.0, (1.1 - abs(x)) / 0.04))
        h += 0.02 * t * f
    return Z0 + h


gx = {SX0, SX1}
for v in (1.1, 1.06, 1.08, 1.03, 0.07, 0.11, 0.08, 0.14, FX + 0.05, FX + 0.1, FX + 0.12, FX + 0.17, FX):
    gx |= {v, -v}
gy = {SY0, SY1, LY - 0.075, LY - 0.04, LY - 0.008, LY + 0.008, LY + 0.04, LY + 0.075, -0.89, -0.87, -0.83, -0.8, FY0, FY1}
for v in (0.05, 0.1, 0.12, 0.17):
    gy |= {FY0 - v, FY1 + v}
gx, gy = sorted(gx), sorted(gy)
kutu(y, V(SX0, SY0, 0), X, SX1 - SX0, SY1 - SY0, Z0, 'tas_koyu', 'onarkasagsol')
for i in range(len(gx) - 1):
    for j in range(len(gy) - 1):
        x0, x1, y0, y1 = gx[i], gx[i + 1], gy[j], gy[j + 1]
        pts = [V(x0, y0, kot(x0, y0)), V(x1, y0, kot(x1, y0)), V(x1, y1, kot(x1, y1)), V(x0, y1, kot(x0, y1))]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        hc = kot(cx, cy)
        if hc < Z0 - 0.002: key = 'toprak'
        elif abs(cx) < FX and FY0 < cy < FY1: key = 'toprak'
        elif hc > Z0 + 0.002: key = 'cimen'
        else: key = 'cimen'
        if abs(pts[0].z - pts[2].z) <= abs(pts[1].z - pts[3].z):
            y.yuz_yon([pts[0], pts[1], pts[2]], key, Z); y.yuz_yon([pts[0], pts[2], pts[3]], key, Z)
        else:
            y.yuz_yon([pts[0], pts[1], pts[3]], key, Z); y.yuz_yon([pts[1], pts[2], pts[3]], key, Z)
# roads: through the limes gate, over the causeway, to the principia; a track along the limes
ZR = Z0 + 0.0015
for (a0, a1, b0, b1) in ((-0.06, 0.06, SY0 + 0.01, FY0 + 0.02), (-0.05, 0.05, FY0 + 0.02, 0.3)):
    y.yuz([V(a0, b0, ZR), V(a1, b0, ZR), V(a1, b1, ZR), V(a0, b1, ZR)], 'zemin')
y.yuz([V(-1.05, -0.78, ZR), V(1.05, -0.78, ZR), V(1.05, -0.74, ZR), V(-1.05, -0.74, ZR)], 'toprak')

# ================================================================ fort walls and towers
y.bolum('Kale suru ve kuleler')
yol = [V(0.1, FY0), V(FX, FY0), V(FX, FY1), V(-FX, FY1), V(-FX, FY0), V(-0.1, FY0)]
sur(y, yol, Z0, HW, KAL, 'granit', kapali=False, mazgal_h=0.028, parapet_h=0.014, ust_key='zemin')
silme(y, yol, Z0, 0.025, 0.012, 'granit_koyu', 'kaide', kapali=False)
silme(y, yol, Z0 + HW - 0.012, 0.012, 0.007, 'tas_acik', 'duz', kapali=False)
for zz in (Z0 + 0.07, Z0 + 0.135):   # late Roman opus mixtum: courses of red tile banding the stone
    silme(y, yol, zz, 0.012, 0.003, 'tugla_roma', 'duz', kapali=False)
# stairs up to the wall walk inside the corners
for sx in (-1, 1):
    merdiven(y, (sx * (FX - KAL - 0.02), FY1 - KAL - 0.2), math.pi / 2, 0.035, Z0, Z0 + HW, n=10, d=0.019, key='granit')
TH = 0.42
for (cx, cy) in ((FX - 0.04, FY0 + 0.04), (FX - 0.04, FY1 - 0.04), (-FX + 0.04, FY1 - 0.04), (-FX + 0.04, FY0 + 0.04)):
    kule(cx + math.copysign(0.065, cx), cy + math.copysign(0.065, cy - 0.13), 0.14, TH, 'piramit')
for (cx, cy) in ((FX + 0.035, (FY0 + FY1) / 2), (-FX - 0.035, (FY0 + FY1) / 2), (0, FY1 + 0.035)):
    kule(cx, cy, 0.12, TH - 0.04, 'duz')
for sx in (-1, 1):
    kule(sx * 0.34, FY0 - 0.035, 0.12, TH - 0.04, 'duz')

y.bolum('Kale kapısı')
GD0, GD1 = FY0 - 0.045, FY0 + 0.05
for s in (-1, 1):
    zt_ = kule(s * 0.17, FY0 - 0.025, 0.15, TH + 0.1, 'piramit')
    if s > 0: sancak(y, s * 0.17, FY0 - 0.025, zt_ - 0.012, boy=0.18, en=0.1, yuk=0.065, aci=-math.pi / 2 + 0.6)
gecit(V(-0.1, GD0), V(0.1, GD0), Z0, HW + 0.01, GD1 - GD0, en=0.64, ust=0.035)
kornis(y, -0.1, 0.1, GD0, GD1, Z0 + HW - 0.004, 0.014, 0.008, 'tas_acik', 'kaba')
y.yuz_yon([V(-0.1, GD0, Z0 + HW + 0.01), V(0.1, GD0, Z0 + HW + 0.01), V(0.1, GD1, Z0 + HW + 0.01), V(-0.1, GD1, Z0 + HW + 0.01)], 'granit', Z)
ZG = Z0 + HW + 0.012
pencereli_duvar(y, [V(-0.1, GD0 + 0.008), V(0.1, GD0 + 0.008)], ZG, 0.07, [3], kapali=False, renk=('granit', 'granit_koyu', 'tas_acik', 'koyu'),
                v0=0.015, en=0.5, ust=0.014, derin=0.012, k_say=6, sivri=0.0, cerceve=(0.005, 'tas_acik'))
pencereli_duvar(y, [V(0.1, GD1 - 0.008), V(-0.1, GD1 - 0.008)], ZG, 0.07, [3], kapali=False, renk=('granit', 'granit_koyu', 'tas_acik', 'koyu'),
                v0=0.015, en=0.5, ust=0.014, derin=0.012, k_say=6, sivri=0.0)
kaburgali_besik(-0.1, 0.1, GD0 + 0.008, GD1 - 0.008, ZG + 0.07, 0.045, sacak=0.016, ucluk_key='granit', alinlik_key='tas_acik')
kutu(y, V(-0.045, GD0 - 0.003, Z0 + HW - 0.03), X, 0.09, 0.003, 0.022, 'kirec', 'onsagsolust')
for j in range(4):
    y.yuz_yon([V(-0.036 + j * 0.02, GD0 - 0.0045, Z0 + HW - 0.022), V(-0.024 + j * 0.02, GD0 - 0.0045, Z0 + HW - 0.022),
               V(-0.024 + j * 0.02, GD0 - 0.0045, Z0 + HW - 0.016), V(-0.036 + j * 0.02, GD0 - 0.0045, Z0 + HW - 0.016)], 'koyu', -Y)
for s in (-1, 1):             # the doors stand open inside the passage
    y.yuz_yon([V(s * 0.062, GD1 - 0.004, Z0), V(s * 0.03, GD1 + 0.03, Z0), V(s * 0.03, GD1 + 0.03, Z0 + 0.1), V(s * 0.062, GD1 - 0.004, Z0 + 0.1)],
              'ahsap', V(-s, -1))
    y.yuz_yon([V(s * 0.062, GD1 - 0.004, Z0), V(s * 0.03, GD1 + 0.03, Z0), V(s * 0.03, GD1 + 0.03, Z0 + 0.1), V(s * 0.062, GD1 - 0.004, Z0 + 0.1)],
              'ahsap_koyu', V(s, 1))
sancak(y, 0, (GD0 + GD1) / 2, ZG + 0.11, boy=0.15, en=0.09, yuk=0.055, aci=-math.pi / 2 + 0.6)

# ================================================================ inside the fort
y.bolum('Principia')
PX0, PX1, PY0_, PY1_ = -0.18, 0.18, 0.36, 0.58
duvarlar(y, dikdortgen(PX0, PX1, PY0_, PY1_), Z0, Z0 + 0.17, 'siva_krem')
silme(y, dikdortgen(PX0, PX1, PY0_, PY1_), Z0, 0.016, 0.006, 'granit', 'kaide')
silme(y, dikdortgen(PX0, PX1, PY0_, PY1_), Z0 + 0.158, 0.012, 0.008, 'tas_acik', 'tac')
for xx in (-0.14, -0.09, 0.07, 0.12):
    y.pencere(V(xx, PY0_, Z0), X, -Y, 0, 0.08, 0.024, 0.05, 'koyu')
y.pencere(V(-0.025, PY0_, Z0), X, -Y, 0, 0, 0.05, 0.085, 'ahsap_koyu')
for xx in (PX0, PX1):
    for yy in (0.4, 0.47, 0.54):
        y.pencere(V(xx, yy - 0.011 * (1 if xx > 0 else -1), Z0), Y if xx > 0 else -Y, V(1 if xx > 0 else -1, 0), 0, 0.08, 0.024, 0.05, 'koyu')
kaburgali_besik(PX0, PX1, PY0_, PY1_, Z0 + 0.17, 0.08, sacak=0.018, ucluk_key='siva_krem', alinlik_key='tas_acik')
for k in range(4):            # a portico before it
    sutun_hafif(-0.11 + 0.22 * k / 3, PY0_ - 0.055, Z0, Z0 + 0.125, 0.009, 'kirec')
alinlik(y, V(-0.135, PY0_ - 0.068), V(0.135, PY0_ - 0.068), Z0 + 0.125, 0.05, derin=0.068, key='kirec', ic_key='siva_krem', c=0.007, cati_key='kiremit')
for s in (-1, 1):
    signum(s * 0.05, PY0_ - 0.1, Z0, 0.17)
signum(0, PY0_ - 0.1, Z0, 0.2, kartal=True)
sancak(y, -0.16, PY0_ - 0.1, Z0, boy=0.24, en=0.09, yuk=0.06, aci=math.pi * 0.8)

y.bolum('Kışlalar')


def kisla(x0, x1, y0, y1, yon):
    """a barrack block along y: doors under a veranda on the yon side, the centurion's house at the y1 end"""
    h = 0.07
    yc = y1 - 0.1
    duvarlar(y, dikdortgen(x0, x1, y0, yc), Z0, Z0 + h, 'siva_krem')
    silme(y, dikdortgen(x0, x1, y0, yc), Z0, 0.012, 0.004, 'granit', 'duz')
    kaburgali_besik(x0, x1, y0, yc, Z0 + h, 0.032, sacak=0.022, ucluk_key='siva_krem', adim=0.03)
    xs = x1 if yon > 0 else x0
    e = -Y if yon > 0 else Y
    sg = 1 if yon > 0 else -1
    nr = 7
    for k in range(nr):
        yy = y0 + (yc - y0) * (k + 0.5) / nr
        y.pencere(V(xs, yy + 0.008 * sg, Z0), e, V(yon, 0), 0, 0.0, 0.016, 0.042, 'ahsap_koyu', kemer=False)
        y.pencere(V(xs, yy - 0.016 * sg, Z0), e, V(yon, 0), 0, 0.025, 0.01, 0.012, 'koyu', kemer=False)
        y.prizma((xs + yon * 0.018, y0 + (yc - y0) * k / nr + 0.002), 0.0028, Z0, Z0 + h - 0.004, 'ahsap', n=4)
    cx0, cx1 = x0 - 0.012, x1 + 0.012
    duvarlar(y, dikdortgen(cx0, cx1, yc, y1), Z0, Z0 + h + 0.02, 'siva_krem')
    silme(y, dikdortgen(cx0, cx1, yc, y1), Z0, 0.012, 0.004, 'siva_kirmizi', 'duz')
    cati_kirma(y, cx0, cx1, yc, y1, Z0 + h + 0.02, 0.04, 0.016, 'kiremit', 'kiremit2', ns=4, nr=3)
    y.pencere(V((cx0 + cx1) / 2 - 0.01, y1, Z0), X, Y, 0, 0.0, 0.02, 0.05, 'ahsap_koyu', kemer=False)


kisla(-0.47, -0.39, -0.32, 0.24, 1)
kisla(-0.3, -0.22, -0.32, 0.24, -1)

y.bolum('Ambar ve atölye')
x0, x1, y0, y1 = 0.25, 0.44, -0.33, 0.02
kutu(y, V(x0 - 0.01, y0 - 0.01, Z0), X, x1 - x0 + 0.02, y1 - y0 + 0.02, 0.025, 'granit_koyu', 'onarkasagsolust')
zf = Z0 + 0.025
duvarlar(y, dikdortgen(x0, x1, y0, y1), zf, zf + 0.1, 'granit')
for k in range(6):
    yy = y0 + 0.02 + (y1 - y0 - 0.04) * k / 5
    for xx, s in ((x0, -1), (x1, 1)):
        kutu_merkez(y, (xx + s * 0.01, yy), 0.02, 0.016, 0.085, 'granit', z0=zf)
        if k < 5:
            y.yuz_yon([V(xx + s * 0.0005, yy + 0.014, Z0 + 0.008), V(xx + s * 0.0005, yy + 0.028, Z0 + 0.008), V(xx + s * 0.0005, yy + 0.028, Z0 + 0.018),
                       V(xx + s * 0.0005, yy + 0.014, Z0 + 0.018)], 'koyu', V(s, 0))
            y.pencere(V(xx, yy + 0.016 + (0.008 if s < 0 else 0), zf), Y if s > 0 else -Y, V(s, 0), 0, 0.06, 0.008, 0.02, 'koyu', kemer=False)
silme(y, dikdortgen(x0, x1, y0, y1), zf + 0.09, 0.01, 0.006, 'tas_acik', 'duz')
kaburgali_besik(x0, x1, y0, y1, zf + 0.1, 0.06, sacak=0.024, ucluk_key='granit', alinlik_key='tas_acik')
y.pencere(V((x0 + x1) / 2 - 0.02, y0, zf), X, -Y, 0, 0, 0.04, 0.06, 'ahsap_koyu', kemer=False)
kutu_merkez(y, ((x0 + x1) / 2, y0 - 0.025), 0.08, 0.04, 0.025, 'granit', z0=Z0)
for k in range(3):
    kure(y, ((x0 + x1) / 2 - 0.03 + 0.03 * k, y0 - 0.03, zf + 0.012), 0.01, 'kerpic', n=8, kat=4)
# workshop / commander's house with a hipped roof
duvarlar(y, dikdortgen(0.23, 0.46, 0.1, 0.3), Z0, Z0 + 0.08, 'siva_krem')
silme(y, dikdortgen(0.23, 0.46, 0.1, 0.3), Z0, 0.014, 0.005, 'siva_kirmizi', 'duz')
cati_kirma(y, 0.23, 0.46, 0.1, 0.3, Z0 + 0.08, 0.07, 0.018, 'kiremit', 'kiremit2', ns=4, nr=3)
for xx in (0.27, 0.33, 0.39):
    y.pencere(V(xx, 0.1, Z0), X, -Y, 0, 0.035, 0.02, 0.03, 'koyu')
y.pencere(V(0.42, 0.1, Z0), X, -Y, 0, 0, 0.022, 0.05, 'ahsap_koyu', kemer=False)
for k in range(4):            # firewood stacks
    boru(y, [V(0.24, 0.32 + 0.012 * k, Z0 + 0.008), V(0.32, 0.32 + 0.012 * k, Z0 + 0.008)], 0.006, 'kutuk', n=6)
    if k < 3: boru(y, [V(0.24, 0.326 + 0.012 * k, Z0 + 0.019), V(0.32, 0.326 + 0.012 * k, Z0 + 0.019)], 0.006, 'kutuk', n=6)
y.prizma((-0.1, 0.0), 0.022, Z0, Z0 + 0.022, 'granit', n=12)           # well
y.yuz_yon([V(-0.1 + 0.016 * math.cos(TAU * i / 12), 0.016 * math.sin(TAU * i / 12), Z0 + 0.023) for i in range(12)], 'su', Z)
for s in (-1, 1):
    y.prizma((-0.1 + s * 0.02, 0), 0.003, Z0 + 0.022, Z0 + 0.065, 'ahsap', n=4)
boru(y, [V(-0.122, 0, Z0 + 0.063), V(-0.078, 0, Z0 + 0.063)], 0.003, 'ahsap', n=5)

y.bolum('Ahır ve demirhane')


def at_(x, yy, aci, key='ahsap_acik'):
    """a horse standing in the stable"""
    with parca(y, (x, yy, 0), aci):
        boru(y, [V(-0.022, 0, Z0 + 0.042), V(0.022, 0, Z0 + 0.044)], 0.011, key, n=7)
        for lx, ly in ((0.016, 0.006), (0.016, -0.006), (-0.017, 0.006), (-0.017, -0.006)):
            boru(y, [V(lx, ly, Z0 + 0.04), V(lx, ly, Z0)], 0.0035, key, n=4)
        boru(y, [V(0.02, 0, Z0 + 0.048), V(0.032, 0, Z0 + 0.066), V(0.044, 0, Z0 + 0.06)], 0.006, key, n=6, r_son=0.0045)
        boru(y, [V(-0.032, 0, Z0 + 0.046), V(-0.038, 0, Z0 + 0.026)], 0.003, 'ahsap_koyu', n=4, r_son=0.0015)


# stable: a back wall, an open front on posts, a tiled roof, horses and hay
SX0_, SX1_, SY0_, SY1_ = 0.22, 0.46, 0.43, 0.58
duz_duvar(y, V(SX1_, SY1_), V(SX0_, SY1_), Z0, Z0 + 0.075, 'ahsap_dikey')
duz_duvar(y, V(SX0_, SY1_), V(SX1_, SY1_), Z0, Z0 + 0.075, 'ahsap_dikey')
for xx in (SX0_, SX1_):
    a_, b_ = (V(xx, SY0_ + 0.04), V(xx, SY1_)) if xx > 0.3 else (V(xx, SY1_), V(xx, SY0_ + 0.04))
    duz_duvar(y, a_, b_, Z0, Z0 + 0.075, 'ahsap_dikey'); duz_duvar(y, b_, a_, Z0, Z0 + 0.075, 'ahsap_dikey')
for k in range(5):
    y.prizma((SX0_ + 0.005 + (SX1_ - SX0_ - 0.01) * k / 4, SY0_ + 0.004), 0.004, Z0, Z0 + 0.075, 'ahsap', n=5)
kaburgali_besik(SX0_, SX1_, SY0_, SY1_, Z0 + 0.075, 0.045, sacak=0.016, ucluk_key='ahsap_dikey')
y.yuz_yon([V(SX0_, SY0_, Z0 + 0.074), V(SX1_, SY0_, Z0 + 0.074), V(SX1_, SY1_, Z0 + 0.074), V(SX0_, SY1_, Z0 + 0.074)], 'ahsap_koyu', -Z)
y.yuz([V(SX0_, SY0_, Z0 + 0.001), V(SX1_, SY0_, Z0 + 0.001), V(SX1_, SY1_, Z0 + 0.001), V(SX0_, SY1_, Z0 + 0.001)], 'saz')
for k, xx in enumerate((0.27, 0.34, 0.41)):
    at_(xx, 0.52, math.pi / 2 + 0.15 * (k - 1), 'ahsap_acik' if k != 1 else 'ahsap_koyu')
for (hx, hy) in ((0.2, 0.38), (0.24, 0.38)):
    kutu_merkez(y, (hx, hy), 0.035, 0.025, 0.022, 'saz', z0=Z0)
kutu_merkez(y, (0.22, 0.38), 0.035, 0.025, 0.02, 'saz', z0=Z0 + 0.022)
# forge: a small house with a chimney and smoke, an anvil and a quench tub outside
duvarlar(y, dikdortgen(-0.46, -0.28, 0.44, 0.58), Z0, Z0 + 0.07, 'granit')
silme(y, dikdortgen(-0.46, -0.28, 0.44, 0.58), Z0 + 0.062, 0.008, 0.005, 'tas_acik', 'duz')
kaburgali_besik(-0.46, -0.28, 0.44, 0.58, Z0 + 0.07, 0.045, sacak=0.016, ucluk_key='granit')
y.pencere(V(-0.37, 0.44, Z0), X, -Y, 0, 0, 0.03, 0.05, 'ahsap_koyu', kemer=False)
y.pencere(V(-0.43, 0.44, Z0), X, -Y, 0, 0.028, 0.02, 0.018, 'boya_sari', kemer=False)
kutu_merkez(y, (-0.31, 0.55), 0.03, 0.03, 0.16, 'tugla_roma', z0=Z0)
for k, (dz, rr) in enumerate(((0.0, 0.014), (0.03, 0.019), (0.062, 0.023))):
    kure(y, (-0.31 - 0.01 * k, 0.55 + 0.005 * k, Z0 + 0.19 + dz), rr, 'beyaz', n=8, kat=4)
kutu_merkez(y, (-0.4, 0.4), 0.03, 0.014, 0.022, 'demir', z0=Z0)
y.prizma((-0.35, 0.4), 0.013, Z0, Z0 + 0.018, 'ahsap', n=10)
y.yuz_yon([V(-0.35 + 0.011 * math.cos(TAU * i / 10), 0.4 + 0.011 * math.sin(TAU * i / 10), Z0 + 0.0185) for i in range(10)], 'su', Z)

# ================================================================ the limes: palisade, gate, towers
y.bolum('Limes: kazık çit ve ahşap kapı')
ZP = Z0 + 0.02
w = 0.017
for (xa, xb) in ((-1.08, -0.1), (0.1, 1.08)):
    n = int((xb - xa) / w)
    for i in range(n):
        x0, x1 = xa + (xb - xa) * i / n, xa + (xb - xa) * (i + 1) / n
        xm = (x0 + x1) / 2
        hh = 0.1 + 0.008 * math.sin(i * 2.3)
        for d, nn in ((-0.006, -Y), (0.006, Y)):
            y.yuz_yon([V(x0, PY + d, ZP - 0.01), V(x1, PY + d, ZP - 0.01), V(x1, PY + d, ZP + hh), V(x0, PY + d, ZP + hh)], 'ahsap_dikey', nn)
        A = V(xm, PY, ZP + hh + 0.016)
        FL, FR, BR, BL = V(x0, PY - 0.006, ZP + hh), V(x1, PY - 0.006, ZP + hh), V(x1, PY + 0.006, ZP + hh), V(x0, PY + 0.006, ZP + hh)
        for tri, nn in (([FL, FR, A], V(0, -1, 0.4)), ([BR, BL, A], V(0, 1, 0.4)), ([BL, FL, A], V(-1, 0, 0.4)), ([FR, BR, A], V(1, 0, 0.4))):
            y.yuz_yon(tri, 'ahsap_dikey', nn)
    for s, xe in ((-1, xa), (1, xb)):
        y.yuz_yon([V(xe, PY - 0.006, ZP - 0.01), V(xe, PY + 0.006, ZP - 0.01), V(xe, PY + 0.006, ZP + 0.1), V(xe, PY - 0.006, ZP + 0.1)], 'ahsap_dikey', V(s, 0))
    boru(y, [V(xa, PY + 0.008, ZP + 0.07), V(xb, PY + 0.008, ZP + 0.07)], 0.004, 'ahsap_koyu', n=5)
# the timber gate: two towers on posts, a fighting platform over the road, a thatched roof
for s in (-1, 1):
    x = s * 0.1
    kutu_merkez(y, (x, PY), 0.05, 0.05, 0.17, 'ahsap_dikey', z0=Z0)
    for (dx, dy) in ((-0.025, -0.025), (0.025, -0.025), (0.025, 0.025), (-0.025, 0.025)):
        y.prizma((x + dx, PY + dy), 0.006, Z0, Z0 + 0.2, 'kutuk', n=6)
    y.pencere(V(x - 0.008, PY - 0.0255, Z0), X, -Y, 0, 0.12, 0.016, 0.025, 'koyu', kemer=False)
kutu(y, V(-0.13, PY - 0.03, Z0 + 0.17), X, 0.26, 0.06, 0.012, 'ahsap', 'onarkasagsolust')
y.yuz_yon([V(-0.075, PY - 0.03, Z0 + 0.17), V(0.075, PY - 0.03, Z0 + 0.17), V(0.075, PY + 0.03, Z0 + 0.17), V(-0.075, PY + 0.03, Z0 + 0.17)], 'ahsap_koyu', -Z)
for k in range(9):            # breastwork posts and rail on the platform
    xx = -0.12 + 0.24 * k / 8
    y.prizma((xx, PY - 0.027), 0.003, Z0 + 0.182, Z0 + 0.22, 'kutuk', n=4)
boru(y, [V(-0.12, PY - 0.027, Z0 + 0.218), V(0.12, PY - 0.027, Z0 + 0.218)], 0.003, 'ahsap', n=4)
cati_besik(y, -0.13, 0.13, PY - 0.03, PY + 0.03, Z0 + 0.235, 0.05, 0.02, 'saz', mahya='saz_koyu', ucluk_key='ahsap_dikey', alt_key='ahsap_koyu')
for s in (-1, 1):
    for (dx, dy) in ((-0.12, -0.028), (-0.12, 0.028)):
        y.prizma((s * -dx, PY + dy), 0.003, Z0 + 0.182, Z0 + 0.235, 'ahsap', n=4)
    y.yuz_yon([V(s * 0.075, PY + 0.03, Z0), V(s * 0.03, PY + 0.07, Z0), V(s * 0.03, PY + 0.07, Z0 + 0.12), V(s * 0.075, PY + 0.03, Z0 + 0.12)], 'ahsap',
              V(-s, -1))
    y.yuz_yon([V(s * 0.075, PY + 0.03, Z0), V(s * 0.03, PY + 0.07, Z0), V(s * 0.03, PY + 0.07, Z0 + 0.12), V(s * 0.075, PY + 0.03, Z0 + 0.12)],
              'ahsap_koyu', V(s, 1))

y.bolum('Gözcü kulesi (taş ve ahşap, işaret ateşi)')
WX, WY = -0.9, -0.68
kutu_merkez(y, (WX, WY), 0.13, 0.13, 0.26, 'granit', z0=Z0)
silme(y, dikdortgen(WX - 0.065, WX + 0.065, WY - 0.065, WY + 0.065), Z0, 0.025, 0.012, 'granit_koyu', 'kaide')
y.pencere(V(WX - 0.018, WY - 0.065, Z0), X, -Y, 0, 0, 0.036, 0.07, 'ahsap_koyu')
for s in range(4):
    ex = [V(1, 0), V(0, 1), V(-1, 0), V(0, -1)][s]; nn = V(ex.y, -ex.x)
    o = V(WX, WY) + nn * 0.0655 - ex * 0.065
    y.pencere(o + Z * Z0, ex, nn, 0.06, 0.17, 0.01, 0.035, 'koyu', kemer=False)
ZW = Z0 + 0.26
kutu(y, V(WX - 0.1, WY - 0.1, ZW), X, 0.2, 0.2, 0.01, 'ahsap', 'onarkasagsolust')          # the gallery floor
for s in range(4):            # brackets under it
    ex = [V(1, 0), V(0, 1), V(-1, 0), V(0, -1)][s]; nn = V(ex.y, -ex.x)
    for u in (-0.04, 0.04):
        p = V(WX, WY) + ex * u
        cubuk(y, p + nn * 0.065 + Z * (ZW - 0.045), p + nn * 0.098 + Z * (ZW - 0.002), 0.008, 'ahsap_koyu')
duvarlar(y, dikdortgen(WX - 0.06, WX + 0.06, WY - 0.06, WY + 0.06), ZW + 0.01, ZW + 0.1, 'ahsap_dikey')
for s in range(4):
    ex = [V(1, 0), V(0, 1), V(-1, 0), V(0, -1)][s]; nn = V(ex.y, -ex.x)
    o = V(WX, WY) + nn * 0.0605 - ex * 0.06
    y.pencere(o + Z * (ZW + 0.01), ex, nn, 0.035, 0.035, 0.05, 0.035, 'koyu', kemer=False)
for k in range(12):           # railing round the gallery
    t = k / 12
    s = int(t * 4); u = t * 4 - s
    ex = [V(1, 0), V(0, 1), V(-1, 0), V(0, -1)][s]; nn = V(ex.y, -ex.x)
    p = V(WX, WY) + nn * 0.095 - ex * 0.095 + ex * (0.19 * u)
    y.prizma((p.x, p.y), 0.0025, ZW + 0.01, ZW + 0.045, 'ahsap', n=4)
rail = [V(WX + 0.095 * a, WY + 0.095 * b, ZW + 0.044) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))]
boru(y, rail, 0.003, 'ahsap', n=4, kapat=False)
kaburgali_besik(WX - 0.06, WX + 0.06, WY - 0.06, WY + 0.06, ZW + 0.1, 0.06, sacak=0.035, ucluk_key='ahsap_dikey')
# the beacon: an iron basket with a fire on a pole, a hay stack and logs for the signal
BX, BY = WX + 0.13, WY + 0.06
y.prizma((BX, BY), 0.005, Z0, Z0 + 0.36, 'ahsap_koyu', n=5)
boru(y, [V(BX + 0.018 * math.cos(TAU * k / 8), BY + 0.018 * math.sin(TAU * k / 8), Z0 + 0.365) for k in range(9)], 0.003, 'demir', n=4, kapat=False)
donel(y, (BX, BY), [(0.0, Z0 + 0.358), (0.016, Z0 + 0.362), (0.018, Z0 + 0.375), (0.01, Z0 + 0.392), (0, Z0 + 0.405)], 'boya_sari', n=8)
donel(y, (BX, BY), [(0.0, Z0 + 0.38), (0.008, Z0 + 0.384), (0, Z0 + 0.415)], 'boya_kirmizi', n=6)
donel(y, (WX - 0.12, WY + 0.03), [(0.04, Z0), (0.038, Z0 + 0.03), (0.02, Z0 + 0.06), (0, Z0 + 0.07)], 'saz', n=10)
for k in range(3):
    boru(y, [V(WX + 0.02 + 0.014 * k, WY + 0.1, Z0 + 0.007), V(WX + 0.02 + 0.014 * k, WY + 0.17, Z0 + 0.007)], 0.0065, 'kutuk', n=6)
boru(y, [V(WX + 0.027, WY + 0.1, Z0 + 0.019), V(WX + 0.027, WY + 0.17, Z0 + 0.019)], 0.0065, 'kutuk', n=6)
sancak(y, WX, WY, ZW + 0.16, boy=0.1, en=0.07, yuk=0.045, aci=-math.pi * 0.25)

y.bolum('Ahşap gözetleme kulesi (direkler üstünde)')
TX, TY = 0.8, -0.68
ZT = Z0 + 0.3
for (dx, dy) in ((-0.04, -0.04), (0.04, -0.04), (0.04, 0.04), (-0.04, 0.04)):
    boru(y, [V(TX + dx * 1.3, TY + dy * 1.3, Z0), V(TX + dx, TY + dy, ZT)], 0.006, 'kutuk', n=6)
for s in range(4):            # cross bracing
    a = [(-0.04, -0.04), (0.04, -0.04), (0.04, 0.04), (-0.04, 0.04)]
    (ax, ay), (bx, by) = a[s], a[(s + 1) % 4]
    for (z0, z1) in ((0.03, 0.155), (0.155, 0.29)):
        f0, f1 = 1.3 - 0.3 * z0 / 0.3, 1.3 - 0.3 * z1 / 0.3
        cubuk(y, V(TX + ax * f0, TY + ay * f0, Z0 + z0), V(TX + bx * f1, TY + by * f1, Z0 + z1), 0.004, 'ahsap')
        cubuk(y, V(TX + bx * f0, TY + by * f0, Z0 + z0), V(TX + ax * f1, TY + ay * f1, Z0 + z1), 0.004, 'ahsap')
kutu(y, V(TX - 0.06, TY - 0.06, ZT), X, 0.12, 0.12, 0.01, 'ahsap', 'onarkasagsolust')
duvarlar(y, dikdortgen(TX - 0.045, TX + 0.045, TY - 0.045, TY + 0.045), ZT + 0.01, ZT + 0.07, 'ahsap_dikey')
for s in range(4):
    ex = [V(1, 0), V(0, 1), V(-1, 0), V(0, -1)][s]; nn = V(ex.y, -ex.x)
    o = V(TX, TY) + nn * 0.0455 - ex * 0.045
    y.pencere(o + Z * (ZT + 0.01), ex, nn, 0.025, 0.03, 0.04, 0.025, 'koyu', kemer=False)
cati_kirma(y, TX - 0.045, TX + 0.045, TY - 0.045, TY + 0.045, ZT + 0.07, 0.06, 0.03, 'saz', 'saz_koyu', ns=4, nr=3)
for s in (-1, 1):             # the ladder
    boru(y, [V(TX + s * 0.014, TY - 0.11, Z0), V(TX + s * 0.014, TY - 0.06, ZT + 0.01)], 0.0025, 'ahsap', n=4)
for k in range(8):
    t = (k + 0.5) / 8
    yy = TY - 0.11 + 0.05 * t; zz = Z0 + (ZT + 0.01 - Z0) * t
    boru(y, [V(TX - 0.014, yy, zz), V(TX + 0.014, yy, zz)], 0.0018, 'ahsap', n=4)
sancak(y, TX + 0.05, TY + 0.05, ZT + 0.01, boy=0.16, en=0.08, yuk=0.05, aci=-math.pi * 0.3)

# ================================================================ outside: bath house, vicus, trees
y.bolum('Hamam (balneum)')
HX0, HX1, HY0, HY1 = 0.82, 1.04, -0.22, 0.24
duvarlar(y, dikdortgen(HX0, HX1, HY0, HY1), Z0, Z0 + 0.09, 'siva_krem')
silme(y, dikdortgen(HX0, HX1, HY0, HY1), Z0, 0.016, 0.006, 'tugla_roma', 'duz')
silme(y, dikdortgen(HX0, HX1, HY0, HY1), Z0 + 0.082, 0.008, 0.006, 'tugla_roma', 'duz')
cx, r = (HX0 + HX1) / 2, (HX1 - HX0) / 2
nv = 12
for k in range(nv):           # the barrel vault, tiled
    a0, a1 = math.pi * k / nv, math.pi * (k + 1) / nv
    p = lambda a, yy: V(cx + (r + 0.008) * math.cos(a), yy, Z0 + 0.09 + (r + 0.008) * math.sin(a) * 0.7)
    y.yuz_yon([p(a0, HY0 - 0.008), p(a1, HY0 - 0.008), p(a1, HY1 + 0.008), p(a0, HY1 + 0.008)], 'kiremit', p((a0 + a1) / 2, 0) - V(cx, 0, Z0 + 0.09))
for yy, s in ((HY0, -1), (HY1, 1)):
    pts = [V(cx + r * math.cos(math.pi * k / nv), yy, Z0 + 0.09 + r * math.sin(math.pi * k / nv) * 0.7) for k in range(nv + 1)]
    y.yuz_yon(pts, 'siva_krem', V(0, s))
for k in range(1, 6):         # the rooms' divisions show as ribs on the vault
    yy = HY0 + (HY1 - HY0) * k / 6
    boru(y, [V(cx + (r + 0.01) * math.cos(math.pi * i / nv), yy, Z0 + 0.09 + (r + 0.01) * math.sin(math.pi * i / nv) * 0.7) for i in range(nv + 1)],
         0.004, 'tugla_roma', n=4, kapat=True)
for yy in (-0.15, -0.05, 0.05, 0.15):
    y.kemerli(V(HX0, yy + 0.04), V(HX0, yy - 0.04), Z0 + 0.02, 0.065, ('siva_krem', 'tugla_roma_koyu', 'tugla_roma', 'cam'), v0=0.0, en=0.45,
              ust=0.008, derin=0.01, k_say=6)
# the apse of the caldarium with a half dome, the furnace chimney
apx = [V(cx + 0.075 * math.cos(math.pi * k / 10), HY1 + 0.075 * math.sin(math.pi * k / 10)) for k in range(11)]
for k in range(10):
    duz_duvar(y, apx[k], apx[k + 1], Z0, Z0 + 0.08, 'siva_krem')
y.kubbe((cx, HY1), 0.08, Z0 + 0.08, 0.06, 'kiremit', n=20, kat=6, t0=0.0, t1=math.pi, kapak='siva_krem')
kutu_merkez(y, (HX1 - 0.02, HY0 + 0.03), 0.03, 0.03, 0.2, 'tugla_roma', z0=Z0)
kutu_merkez(y, (HX1 - 0.02, HY0 + 0.03), 0.036, 0.036, 0.01, 'tugla_roma_koyu', z0=Z0 + 0.2)
for k, (dz, rr) in enumerate(((0.0, 0.016), (0.03, 0.022), (0.065, 0.026))):
    kure(y, (HX1 - 0.02 + 0.012 * k, HY0 + 0.03 + 0.006 * k, Z0 + 0.235 + dz), rr, 'beyaz', n=8, kat=4)
y.pencere(V(HX0 + 0.08, HY0, Z0), X, -Y, 0, 0, 0.05, 0.06, 'ahsap_koyu')

y.bolum('Köy (vicus) ve ağaçlar')
for (vx, vy, aci) in ((-0.95, -0.35, 0.1), (-0.93, 0.08, -0.05), (-0.98, 0.5, 0.15)):
    with parca(y, (vx, vy, 0), aci):
        duvarlar(y, dikdortgen(-0.07, 0.07, -0.05, 0.05), Z0, Z0 + 0.055, 'ahsap_dikey')
        cati_besik(y, -0.07, 0.07, -0.05, 0.05, Z0 + 0.055, 0.06, 0.02, 'saz', mahya='saz_koyu', ucluk_key='ahsap_dikey')
        y.pencere(V(0.02, -0.05, Z0), X, -Y, 0, 0, 0.022, 0.04, 'ahsap_koyu', kemer=False)
        y.pencere(V(0.075 - 0.005, 0.0, Z0), Y, X, 0, 0.025, 0.018, 0.015, 'koyu', kemer=False)
    for k in range(5):        # a wattle fence
        a = V(vx + 0.1, vy - 0.08 + 0.04 * k)
        y.prizma((a.x, a.y), 0.003, Z0, Z0 + 0.035, 'ahsap', n=4)
    boru(y, [V(vx + 0.1, vy - 0.08, Z0 + 0.025), V(vx + 0.1, vy + 0.08, Z0 + 0.025)], 0.004, 'ahsap_koyu', n=4)
for (tx, ty, b) in ((-1.08, -0.48, 0.22), (-0.8, 0.85, 0.24), (-1.0, 0.85, 0.2), (0.82, 0.8, 0.22), (1.0, 0.62, 0.24), (1.06, 0.86, 0.2),
                    (0.66, 0.92, 0.18), (-0.62, 0.92, 0.2), (1.06, -0.55, 0.2), (-0.8, -0.3, 0.17)):
    cam_agaci(tx, ty, Z0, b)

calistir(y, 'lm_limes')
