# Olympia (lm_olimpia): the Temple of Zeus (Doric hexastyle 6 x 13 on its high crepidoma, the in-antis porches with
# the Labours of Herakles, gilded shields and tripod acroteria, the chariot race and the centaur fight in the
# pediments, Zeus' gold statue glinting through the door), the round Ionic Philippeion, the ash altar of Zeus, the
# Nike of Paionios on her tall pillar, the Zanes and the treasury terrace; beside them the stadium: the long clay
# track with its marble start lines between grassy spectator banks, the vaulted crypt tunnel, the judges' stand.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
RNG = random.Random(5)
TRI = 'lacivert'
Z0 = 0.03


# ================================================================ Greek helpers (this building's own)
def kiremit_kaburga(p0, p1, w=0.0055, key='mermer'):
    """a cover-tile rib along a roof slope from p0 to p1 (a low two-faced ridge)"""
    p0, p1 = Vector(p0), Vector(p1)
    t = (p1 - p0).normalized()
    s = Z.cross(t)
    if s.length < 1e-6: s = X.copy()
    s.normalize(); u = t.cross(s).normalized()
    if u.z < 0: u = -u
    h = u * (w * 0.55)
    A0, A1 = p0 - s * (w / 2), p1 - s * (w / 2)
    B0, B1 = p0 + s * (w / 2), p1 + s * (w / 2)
    y.yuz_yon([A0, A1, p1 + h, p0 + h], key, u - s)
    y.yuz_yon([p0 + h, p1 + h, B1, B0], key, u + s)
    y.yuz_yon([A0, B0, p0 + h], key, p0 - p1)


def kiremit_serit(x0, x1, y0, y1, z, h, adim=0.026, key='mermer'):
    """cover-tile ribs on a gable roof (ridge along y) from both eaves to the ridge"""
    n = max(1, int((y1 - y0) / adim))
    for j in range(n + 1):
        yy = y0 + (y1 - y0) * j / n
        for xe in (x0, x1):
            kiremit_kaburga(V(xe, yy, z + 0.0015), V((x0 + x1) / 2, yy, z + h + 0.0015), key=key)


def kolon(cx, cy, z0, z1, r, tur='dor', key='mermer', yiv=12):
    sutun(y, cx, cy, z0, z1, r, key, tur, yiv=yiv)


def figur(x, yy, z, s=1.0, key='mermer', aci=0.0, kol=1.0):
    """a draped standing figure (no pedestal), one arm raised (kol 0: both down)"""
    donel(y, (x, yy), [(0.014 * s, z), (0.016 * s, z + 0.02 * s), (0.011 * s, z + 0.055 * s), (0.013 * s, z + 0.068 * s),
                       (0.008 * s, z + 0.077 * s), (0, z + 0.079 * s)], key, n=10)
    kure(y, (x, yy, z + 0.088 * s), 0.008 * s, key, n=8, kat=4)
    e = V(math.cos(aci), math.sin(aci))
    if kol:
        boru(y, [V(x, yy, z + 0.064 * s) + e * 0.01 * s, V(x, yy, z + 0.095 * s * kol) + e * 0.022 * s], 0.0028 * s, key, n=5)


def uzanan(x, yy, z, yon, s=1.0, key='mermer'):
    """a reclining figure (river god in a pediment corner), lying along yon (+1 / -1 in x), propped on an elbow"""
    boru(y, [V(x, yy, z + 0.006 * s), V(x + yon * 0.03 * s, yy, z + 0.008 * s), V(x + yon * 0.055 * s, yy, z + 0.016 * s)], 0.0075 * s, key, n=7,
         r_son=0.006 * s)
    kure(y, (x + yon * 0.064 * s, yy, z + 0.026 * s), 0.0065 * s, key, n=8, kat=4)
    boru(y, [V(x + yon * 0.05 * s, yy, z + 0.016 * s), V(x + yon * 0.045 * s, yy, z + 0.002 * s)], 0.0025 * s, key, n=4)


def at(x, yy, z, aci=0.0, s=1.0, key='mermer'):
    """a rearing horse (pediment / chariot team), facing angle aci"""
    with parca(y, (x, yy, z), aci, s):
        boru(y, [V(-0.032, 0, 0.062), V(0, 0, 0.068), V(0.03, 0, 0.076)], 0.015, key, n=8)
        for lx, ly, up in ((0.024, 0.008, 1), (0.024, -0.008, 1), (-0.026, 0.008, 0), (-0.026, -0.008, 0)):
            if up:
                boru(y, [V(lx, ly, 0.064), V(lx + 0.018, ly, 0.05), V(lx + 0.014, ly, 0.034)], 0.0045, key, n=5)
            else:
                boru(y, [V(lx, ly, 0.058), V(lx + 0.002, ly, 0.028), V(lx, ly, 0.0)], 0.0045, key, n=5, r_son=0.0035)
        boru(y, [V(0.028, 0, 0.08), V(0.04, 0, 0.104), V(0.048, 0, 0.114)], 0.008, key, n=7, r_son=0.006)
        boru(y, [V(0.046, 0, 0.116), V(0.064, 0, 0.104)], 0.0055, key, n=6, r_son=0.004)
        boru(y, [V(-0.044, 0, 0.066), V(-0.054, 0, 0.044), V(-0.052, 0, 0.03)], 0.004, key, n=5, r_son=0.002)


def amfora(x, yy, z, s=1.0, key='siva_oker'):
    donel(y, (x, yy), [(0.0, z), (0.004 * s, z), (0.011 * s, z + 0.01 * s), (0.012 * s, z + 0.018 * s), (0.006 * s, z + 0.028 * s),
                       (0.004 * s, z + 0.034 * s), (0.0045 * s, z + 0.036 * s), (0, z + 0.036 * s)], key, n=8)


def zeytin(x, yy, z, boy=0.14, s=1.0):
    """an olive: a twisted grey trunk, a silvery crown in lumps"""
    top = V(x + 0.01 * s, yy, z + boy * 0.45)
    boru(y, [V(x, yy, z), V(x - 0.006 * s, yy + 0.003 * s, z + boy * 0.22), top], 0.007 * s, 'ahsap_acik', n=6, r_son=0.005 * s)
    for k, (dx, dy, dz, r) in enumerate(((0, 0, 0.62, 0.05), (0.035, 0.02, 0.52, 0.036), (-0.03, 0.022, 0.55, 0.035), (0.01, -0.035, 0.52, 0.036))):
        kure(y, (x + dx * s, yy + dy * s, z + boy * dz + 0.02 * s), r * s, 'zeytin', n=7, kat=4)


def kore(x, yy, z0, z1, s=1.0, key='mermer'):
    """a caryatid: a draped maiden on a low plinth carrying a polos and a capital block on her head"""
    H = z1 - z0
    kutu_merkez(y, (x, yy), 0.03 * s, 0.03 * s, H * 0.06, key, z0=z0)
    zb = z0 + H * 0.06
    donel(y, (x, yy), [(0.013 * s, zb), (0.014 * s, zb + H * 0.3), (0.011 * s, zb + H * 0.55), (0.012 * s, zb + H * 0.66), (0.008 * s, zb + H * 0.72),
                       (0.0045 * s, zb + H * 0.74)], key, n=10)
    for k in range(5):     # the folds of the chiton
        a = TAU * k / 5 + 0.3
        boru(y, [V(x + 0.0125 * s * math.cos(a), yy + 0.0125 * s * math.sin(a), zb + 0.002), V(x + 0.012 * s * math.cos(a), yy + 0.012 * s * math.sin(a), zb + H * 0.5)],
             0.0018 * s, key, n=4)
    kure(y, (x, yy, zb + H * 0.79), 0.0075 * s, key, n=8, kat=4)
    y.prizma((x, yy), 0.008 * s, zb + H * 0.83, z1 - H * 0.07, key, n=10)
    donel(y, (x, yy), [(0.008 * s, z1 - H * 0.07), (0.016 * s, z1 - H * 0.04)], key, n=10)
    kutu_merkez(y, (x, yy), 0.034 * s, 0.034 * s, H * 0.04, key, z0=z1 - H * 0.04)


def triglif_dizi(p, q, z, h, n, key=TRI, w=0.012, metop=None, rolyef=True):
    """n + 1 triglyphs on the frieze face p->q (faces its right), each with two grooves; between them metope panels
    (metop: the painted background) carrying a two-figure relief (a fight: Lapith and centaur, god and giant)"""
    W = (q - p).length; e = (q - p) / W; nc = V(e.y, -e.x)
    for i in range(n + 1):
        u = max(0.0, min(W - w, W * i / n - w / 2))
        o = p + e * u + Z * z
        kutu(y, o + nc * 0.0025, e, w, 0.0025, h, key, 'onsagsolust')
        for g in (0.33, 0.67):
            gg = o + e * (w * g) + nc * 0.0027
            y.yuz_yon([gg - e * 0.0012, gg + e * 0.0012, gg + e * 0.0012 + Z * (h * 0.85), gg - e * 0.0012 + Z * (h * 0.85)], 'koyu', nc)
        if metop and i < n:
            m0 = p + e * (W * i / n + w / 2 + 0.0015); m1 = p + e * (W * (i + 1) / n - w / 2 - 0.0015)
            mw = (m1 - m0).dot(e)
            if mw > 0.006:
                y.yuz_yon([m0 + nc * 0.001 + Z * (z + h * 0.1), m1 + nc * 0.001 + Z * (z + h * 0.1), m1 + nc * 0.001 + Z * (z + h * 0.9),
                           m0 + nc * 0.001 + Z * (z + h * 0.9)], metop, nc)
                if rolyef:
                    # two figures in relief: a leaning one and an upright one, alternating sides
                    sg = 1 if i % 2 else -1
                    fa = m0 + e * (mw * (0.3 if sg > 0 else 0.6))
                    fb = m0 + e * (mw * (0.66 if sg > 0 else 0.26))
                    kutu(y, fa + nc * 0.004 + Z * (z + h * 0.14), e, mw * 0.16, 0.0028, h * 0.68, 'mermer', 'onsagsolust')
                    kure(y, fa + e * (mw * 0.08) + nc * 0.0025 + Z * (z + h * 0.88), h * 0.09, 'mermer', n=6, kat=3)
                    # the other figure leans in (a slanted block)
                    b0 = fb + Z * (z + h * 0.14); b1 = fb + e * (-sg * mw * 0.12) + Z * (z + h * 0.72)
                    cubuk(y, b0 + nc * 0.0025, b1 + nc * 0.0025, mw * 0.14, 'mermer', 0.003)




def kalkan(c, e, nn, r, key='altin'):
    """a round shield / disc lying on a wall face (centre c, e along the wall, nn out)"""
    y.yuz_yon([c + nn * 0.0012 + e * (r * math.cos(TAU * a / 10)) + Z * (r * math.sin(TAU * a / 10)) for a in range(10)], key, nn)


def tripod(x, yy, z, s=1.0, key='altin'):
    """a bronze tripod cauldron (corner acroterion, prize)"""
    for k in range(3):
        a = TAU * k / 3
        boru(y, [V(x + 0.012 * s * math.cos(a), yy + 0.012 * s * math.sin(a), z), V(x + 0.008 * s * math.cos(a), yy + 0.008 * s * math.sin(a), z + 0.024 * s)],
             0.0016 * s, key, n=4)
    donel(y, (x, yy), [(0.004 * s, z + 0.02 * s), (0.013 * s, z + 0.026 * s), (0.014 * s, z + 0.034 * s), (0.0, z + 0.034 * s)], key, n=10)
    for k in range(2):
        a = math.pi * k
        boru(y, [V(x + 0.012 * s * math.cos(a), yy, z + 0.034 * s), V(x + 0.012 * s * math.cos(a), yy, z + 0.046 * s)], 0.0018 * s, key, n=4)


def nike(x, yy, z, s=1.0, key='altin', aci=0.0):
    """a winged Victory alighting: draped body, spread wings behind (both faces), one arm forward"""
    figur(x, yy, z, s, key, aci=aci, kol=0.7)
    e = V(math.cos(aci), math.sin(aci)); nn = V(-e.y, e.x)
    for sg in (-1, 1):
        b0 = V(x, yy, z + 0.066 * s) - e * (0.006 * s)
        tip = b0 + nn * (sg * 0.045 * s) - e * (0.012 * s) + Z * (0.03 * s)
        low = b0 + nn * (sg * 0.03 * s) - e * (0.01 * s) - Z * (0.012 * s)
        tri = [b0, tip, low]
        for d in (1, -1):
            y.yuz_yon([p_ + e * (0.0008 * d) for p_ in tri], key, e * d)
        mid = (b0 + tip + low) / 3
        for k in range(3):   # the wing's thin rims
            p_, q_ = tri[k], tri[(k + 1) % 3]
            yuz_dis(y, [p_ + e * 0.0008, q_ + e * 0.0008, q_ - e * 0.0008, p_ - e * 0.0008], key, mid)


def dor_tapinak(L, W, nl, nw, z0, HC, r, key='kirec', cati='kiremit', kaburga='kiremit2', sb=0.025, porch_n=2):
    """the Temple of Zeus at the origin, long axis y, the east front facing -y: a high three-stepped crepidoma, a
    Doric peristyle, the cella with porches in antis whose frieze carries the Labours of Herakles, plain exterior
    metopes hung with gilded shields on the front, the pediments (chariot race east, centaurs west), a tiled roof
    with lion-head spouts, a gilded Nike on the apex and tripods at the corners. Returns the top z"""
    sx_, sy_ = W / (nw - 1), L / (nl - 1)
    m = r * 2.4
    for k in range(3):
        d = m + 0.026 * (2 - k)
        x0, x1, y0, y1 = -W / 2 - d, W / 2 + d, -L / 2 - d, L / 2 + d
        kutu(y, V(x0, y0, z0 + sb * k), X, x1 - x0, y1 - y0, sb, key, 'onarkasagsol')
        y.yuz([V(x0, y0, z0 + sb * (k + 1)), V(x1, y0, z0 + sb * (k + 1)), V(x1, y1, z0 + sb * (k + 1)), V(x0, y1, z0 + sb * (k + 1))], key)
        silme(y, dikdortgen(x0, x1, y0, y1), z0 + sb * k, 0.004, 0.0015, 'tas_koyu', 'duz')
    # the ramp up the east front
    yb = -(L / 2 + m + 0.052)
    y.yuz_yon([V(-0.08, yb - 0.1, z0), V(0.08, yb - 0.1, z0), V(0.08, yb, z0 + sb * 3), V(-0.08, yb, z0 + sb * 3)], key, V(0, -0.5, 1))
    for sx in (-1, 1):
        y.yuz_yon([V(sx * 0.08, yb - 0.1, z0), V(sx * 0.08, yb, z0), V(sx * 0.08, yb, z0 + sb * 3)], key, V(sx, 0))
    zs = z0 + sb * 3
    zc = zs + HC
    pts = [V(-W / 2 + sx_ * i, -L / 2) for i in range(nw - 1)] + [V(W / 2, -L / 2 + sy_ * j) for j in range(nl - 1)] + \
          [V(W / 2 - sx_ * i, L / 2) for i in range(nw - 1)] + [V(-W / 2, L / 2 - sy_ * j) for j in range(nl - 1)]
    for p in pts:
        kolon(p.x, p.y, zs, zc, r, 'dor', key, yiv=12)
    he = HC * 0.27
    ha, hf = he * 0.4, he * 0.38

    # ---- the cella: long walls with antae, door walls, two columns in antis at each end, a metope frieze over them
    cx = W / 2 - sx_ * 1.0
    ya = L / 2 - sy_ * 1.2
    yd = L / 2 - sy_ * 2.0
    t = 0.026
    for s in (-1, 1):
        a, b = (V(s * cx, -ya), V(s * cx, ya)) if s > 0 else (V(s * cx, ya), V(s * cx, -ya))
        duz_duvar(y, a, b, zs, zc + ha, key)
        for yy in (-ya, ya):
            sg = 1 if yy > 0 else -1
            y.yuz_yon([V(s * cx, yy, zs), V(s * (cx - t), yy, zs), V(s * (cx - t), yy, zc), V(s * cx, yy, zc)], key, V(0, sg))
            y.yuz_yon([V(s * (cx - t), yy, zs), V(s * (cx - t), sg * yd, zs), V(s * (cx - t), sg * yd, zc + ha), V(s * (cx - t), yy, zc + ha)], key, V(-s, 0))
            kutu_merkez(y, (s * (cx - t / 2), yy - sg * 0.004), t * 1.4, 0.016, 0.016, key, z0=zc - 0.016)
        silme(y, [a, b], zs, 0.014, 0.004, key, 'kaide', kapali=False)
    for sg in (-1, 1):
        a, b = (V(-cx + t, sg * yd), V(cx - t, sg * yd)) if sg < 0 else (V(cx - t, sg * yd), V(-cx + t, sg * yd))
        Wd, e_, nc_, Ld = dikdortgen_acik(y, a, b, zs, zc - zs, 0.33, 0.67, 0.0, (zc - zs) * 0.76,
                                          (key, 'tas_acik', 'tas_acik', 'koyu' if sg < 0 else 'bronz'), derin=0.016, cerceve=(0.009, 'mermer'))
        if sg < 0:
            # the gold-and-ivory Zeus enthroned far inside the open door
            pc = Ld(0.5, 0, 0.016)
            kutu_merkez(y, (pc.x, pc.y), 0.08, 0.02, 0.12, 'altin', z0=zs)
            donel(y, (pc.x, pc.y), [(0.03, zs + 0.06), (0.026, zs + 0.15), (0.018, zs + 0.2), (0.0, zs + 0.215)], 'altin', n=10)
            kure(y, (pc.x, pc.y, zs + 0.23), 0.014, 'tas_acik', n=8, kat=4)
        duz_duvar(y, a, b, zc, zc + ha, key)
        for i in range(porch_n):
            xx = -cx + 2 * cx * (i + 1) / (porch_n + 1)
            kolon(xx, sg * ya, zs, zc, r * 0.9, 'dor', key, yiv=12)
        # the porch beam with the twelve labours (six at each end) on its outer face
        kutu_merkez(y, (0, sg * ya), 2 * cx + 0.004, r * 2.2, ha, key, z0=zc)
        if sg > 0:
            p0, p1 = V(cx + 0.002, ya + r * 1.1), V(-cx - 0.002, ya + r * 1.1)
        else:
            p0, p1 = V(-cx - 0.002, -ya - r * 1.1), V(cx + 0.002, -ya - r * 1.1)
        triglif_dizi(p0, p1, zc + ha * 0.1, ha * 0.85, 6, w=0.01, metop='boya_kirmizi')
        y.yuz_yon([V(-cx - 0.002, sg * ya - r * 1.1, zc), V(cx + 0.002, sg * ya - r * 1.1, zc), V(cx + 0.002, sg * ya + r * 1.1, zc),
                   V(-cx - 0.002, sg * ya + r * 1.1, zc)], key, -Z)
    y.yuz_yon([V(-W / 2, -L / 2, zc + ha), V(W / 2, -L / 2, zc + ha), V(W / 2, L / 2, zc + ha), V(-W / 2, L / 2, zc + ha)], 'tas_koyu', -Z)

    # ---- the outer entablature
    D = r * 2.6
    k4 = dikdortgen(-W / 2, W / 2, -L / 2, L / 2)
    o = disa(k4, D / 2); ii = disa(k4, -D / 2)
    duvarlar(y, o, zc, zc + ha, key)
    silme(y, o, zc + ha - he * 0.05, he * 0.05, 0.003, key, 'duz')
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * zc, o[j] + Z * zc, ii[j] + Z * zc, ii[i] + Z * zc], key, -Z)
        duz_duvar(y, ii[j], ii[i], zc, zc + ha, key)
    f = disa(k4, D / 2 - 0.003)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * (zc + ha), o[j] + Z * (zc + ha), f[j] + Z * (zc + ha), f[i] + Z * (zc + ha)], key, Z)
    duvarlar(y, f, zc + ha, zc + ha + hf, key)
    for i in range(4):
        p, q = f[i], f[(i + 1) % 4]
        n = (nw - 1) * 2 if i % 2 == 0 else (nl - 1) * 2
        triglif_dizi(p, q, zc + ha, hf, n, metop='tas_acik', rolyef=False)
        if i == 0:   # Mummius' gilded shields on the east metopes
            e = (q - p).normalized(); nn = V(e.y, -e.x)
            for k in range(n):
                kalkan(p.lerp(q, (k + 0.5) / n) + Z * (zc + ha + hf * 0.5) + nn * 0.001, e, nn, hf * 0.3)
    zk = zc + ha + hf
    silme(y, f, zk, he * 0.22, he * 0.32, key, 'tac')
    ze = zk + he * 0.22
    y.yuz_yon([V(p.x, p.y, ze) for p in f], key, Z)
    # lion-head spouts along the sima of the long sides
    for s in (-1, 1):
        for j in range(nl):
            yy = -L / 2 + sy_ * j
            boru(y, [V(s * (W / 2 + D / 2 + he * 0.3), yy, ze - he * 0.08), V(s * (W / 2 + D / 2 + he * 0.3 + 0.012), yy, ze - he * 0.1)], 0.004, 'mermer', n=6)

    # ---- pediments and roof
    g = disa(k4, D / 2 + he * 0.32)
    xa, xb, ya_, yb_ = g[0].x, g[1].x, g[0].y, g[2].y
    ph = (xb - xa) * 0.13
    alinlik(y, V(xa, ya_), V(xb, ya_), ze, ph, derin=yb_ - ya_ - 0.003, key=key, ic_key='lacivert', c=0.012, cati_key=cati)
    alinlik(y, V(xb, yb_), V(xa, yb_), ze, ph, derin=0.003, key=key, ic_key='lacivert', c=0.012, cati_key=cati)
    kiremit_serit(xa, xb, ya_ + 0.012, yb_ - 0.012, ze + 0.0096, ph, adim=0.03, key=kaburga)
    cubuk(y, V(0, ya_, ze + ph + 0.013), V(0, yb_, ze + ph + 0.013), 0.013, kaburga)
    sp = 0.012 * 1.6
    zt0 = ze + sp
    HT = ph - 2.9 * sp
    hw = (xb - xa) / 2

    def H(x):
        return max(0.004, HT * (1 - abs(x) / (hw * 0.93)) * 0.9)
    for yy, sg in ((ya_, -1), (yb_, 1)):
        yt = yy - sg * 0.0005
        figur(0, yt, zt0, H(0) / 0.097, 'mermer', kol=0.9)                 # Zeus (east) / Apollo (west) in the middle
        if sg < 0:   # the chariot race of Pelops and Oinomaos about to start
            for s in (-1, 1):
                figur(s * hw * 0.1, yt, zt0, H(hw * 0.12) / 0.097, 'mermer', kol=0)
                figur(s * hw * 0.18, yt, zt0, H(hw * 0.2) / 0.097, 'mermer', kol=0)
                for k in range(4):
                    xx = s * hw * (0.28 + 0.045 * k)
                    at(xx, yt + sg * 0.002 * (k % 2), zt0, aci=0 if s < 0 else math.pi, s=H(hw * 0.46) / 0.118)
                kutu_merkez(y, (s * hw * 0.5, yt), H(hw * 0.5) * 0.5, 0.008, H(hw * 0.5) * 0.35, 'mermer', z0=zt0)   # the chariot
                figur(s * hw * 0.6, yt, zt0, H(hw * 0.62) / 0.09, 'mermer', kol=0)
                uzanan(s * hw * 0.85, yt, zt0, -s, 0.55)
        else:        # Lapiths and centaurs at the wedding feast
            for s in (-1, 1):
                for k, f_ in enumerate((0.16, 0.3, 0.44, 0.58)):
                    if k % 2:
                        at(s * hw * f_, yt, zt0, aci=0 if s > 0 else math.pi, s=H(hw * (f_ + 0.06)) / 0.118)
                        figur(s * hw * (f_ + 0.03), yt, zt0 + H(hw * (f_ + 0.06)) * 0.45, H(hw * (f_ + 0.06)) * 0.5 / 0.097, 'mermer', kol=1)
                    else:
                        figur(s * hw * f_, yt, zt0, H(hw * (f_ + 0.02)) / 0.097, 'mermer', aci=0 if s > 0 else math.pi, kol=1)
                uzanan(s * hw * 0.8, yt, zt0, -s, 0.5)
        zap = ze + ph + 0.013
        nike(0, yy, zap, 0.8, 'altin', aci=math.pi / 2 * (-sg))
        for xx in (xa + 0.016, xb - 0.016):
            kutu_merkez(y, (xx, yy - sg * 0.006), 0.026, 0.026, 0.008, key, z0=ze + 0.008)
            tripod(xx, yy - sg * 0.006, ze + 0.016, 1.3)
    nA = int((yb_ - ya_) / 0.026)
    for sx in (-1, 1):
        xe = xb if sx > 0 else xa
        for j in range(nA + 1):
            yy = ya_ + 0.013 + (yb_ - ya_ - 0.026) * j / nA
            zb_ = ze + 0.0095
            pa = [V(xe + sx * 0.0005, yy - 0.005, zb_), V(xe + sx * 0.0005, yy + 0.005, zb_), V(xe + sx * 0.0005, yy + 0.004, zb_ + 0.009),
                  V(xe + sx * 0.0005, yy, zb_ + 0.013), V(xe + sx * 0.0005, yy - 0.004, zb_ + 0.009)]
            pb = [p - V(sx * 0.002, 0) for p in pa]
            y.yuz_yon(pa, 'boya_kirmizi' if j % 2 else 'mermer', V(sx, 0))
            y.yuz_yon(pb, 'mermer', V(-sx, 0))
            for k in range(5):
                yuz_dis(y, [pa[k], pa[(k + 1) % 5], pb[(k + 1) % 5], pb[k]], 'mermer', V(xe - sx * 0.0005, yy, zb_ + 0.005))
    return ze + ph + 0.1, zs


def set_(eksen, s0, s1, prof, key='cimen', dis=1, ust_key=None):
    """an earth bank running along eksen ('x' or 'y') from s0 to s1, its cross-section prof = [(c, z), ...] across
    (c: the other coordinate) from one foot to the other; slopes face up, a vertical step faces dis; closed ends"""
    def P(c, s, z):
        return V(c, s, z) if eksen == 'y' else V(s, c, z)
    n = max(1, int(math.ceil((s1 - s0) / 0.12)))
    for k in range(len(prof) - 1):
        (c0, z0_), (c1, z1_) = prof[k], prof[k + 1]
        dc, dz = c1 - c0, z1_ - z0_
        if abs(dc) > 1e-6:
            nr = (-dz, dc) if dc > 0 else (dz, -dc)
        else:
            nr = (dis, 0)
        nrm = P(nr[0], 0, nr[1])
        kk = ust_key if (ust_key and abs(dz) < 1e-6) else key
        if abs(dc) < 1e-6: kk = 'tas'          # a vertical step: a stone retaining wall
        for i in range(n):
            sa, sb_ = s0 + (s1 - s0) * i / n, s0 + (s1 - s0) * (i + 1) / n
            y.yuz_yon([P(c0, sa, z0_), P(c1, sa, z1_), P(c1, sb_, z1_), P(c0, sb_, z0_)], kk, nrm)
    for s, sg in ((s0, -1), (s1, 1)):
        y.yuz_yon([P(c, s, z) for c, z in prof], 'toprak', P(0, sg, 0))


def seyirci(x, yy, z, tohum, oturan=True):
    """a spectator: a tunic of a random colour, a head"""
    g = random.Random(tohum)
    k = g.choice(('boya_kirmizi', 'beyaz', 'boya_sari', 'kumas', 'lacivert', 'boya_yesil', 'beyaz', 'siva_oker'))
    h = 0.022 if oturan else 0.03
    donel(y, (x, yy), [(0.0065, z), (0.0055, z + h * 0.6), (0.0035, z + h), (0.0, z + h + 0.001)], k, n=5, kat=g.random())
    kure(y, (x, yy, z + h + 0.004), 0.0042, 'kerpic', n=5, kat=3)


def kosucu(x, yy, z, aci, key='siva_oker'):
    """a running athlete (bare, oiled skin), leaning forward, legs apart"""
    e = V(math.cos(aci), math.sin(aci))
    hip = V(x, yy, z + 0.018)
    for sg in (-1, 1):
        boru(y, [hip, hip + e * (sg * 0.008) - Z * 0.018], 0.002, key, n=4)
    top = hip + e * 0.004 + Z * 0.016
    boru(y, [hip, top], 0.0035, key, n=5)
    kure(y, top + e * 0.002 + Z * 0.005, 0.0038, key, n=6, kat=3)
    for sg in (-1, 1):
        boru(y, [top - Z * 0.002, top - Z * 0.006 + e * (sg * 0.008)], 0.0015, key, n=4)


# ================================================================ ground
y.bolum('Zemin')
zemin(y, -1.15, 1.15, -1.05, 1.05, h=Z0, key='tas_koyu', ust='toprak', basamak=())

# ================================================================ the stadium
y.bolum('Stadyum: seyirci setleri')
HB = 0.13
set_('y', -0.84, 0.98, [(0.38, Z0), (0.47, Z0 + HB), (0.52, Z0 + HB), (0.62, Z0)], 'cimen', ust_key='toprak')
set_('y', -0.84, 1.05, [(0.9, Z0), (1.03, Z0 + 0.17), (1.15, Z0 + 0.17), (1.15, Z0)], 'cimen', dis=1, ust_key='toprak')
set_('x', 0.38, 1.15, [(-0.7, Z0), (-0.8, Z0 + HB), (-0.86, Z0 + HB), (-0.98, Z0)], 'cimen', ust_key='toprak')
set_('x', 0.38, 1.15, [(0.95, Z0), (1.02, Z0 + HB), (1.05, Z0 + HB), (1.05, Z0)], 'cimen', dis=1, ust_key='toprak')

y.bolum('Koşu pisti')
TX0, TX1, TY0, TY1 = 0.62, 0.9, -0.7, 0.95
zt = Z0 + 0.003
y.yuz_yon([V(TX0, TY0, zt), V(TX1, TY0, zt), V(TX1, TY1, zt), V(TX0, TY1, zt)], 'kum_acik', Z)
# the stone water channel along both long sides, with basins
for xx, sg in ((TX0 + 0.006, -1), (TX1 - 0.006, 1)):
    kutu_merkez(y, (xx, (TY0 + TY1) / 2), 0.012, TY1 - TY0, 0.006, 'kirec', z0=Z0)
    y.yuz_yon([V(xx - 0.003, TY0, Z0 + 0.0062), V(xx + 0.003, TY0, Z0 + 0.0062), V(xx + 0.003, TY1, Z0 + 0.0062), V(xx - 0.003, TY1, Z0 + 0.0062)], 'su', Z)
    for k in range(6):
        yy = TY0 + 0.1 + (TY1 - TY0 - 0.2) * k / 5
        kutu_merkez(y, (xx + sg * 0.012, yy), 0.016, 0.03, 0.01, 'kirec', z0=Z0)
        y.yuz_yon([V(xx + sg * 0.012 - 0.005, yy - 0.01, Z0 + 0.0102), V(xx + sg * 0.012 + 0.005, yy - 0.01, Z0 + 0.0102),
                   V(xx + sg * 0.012 + 0.005, yy + 0.01, Z0 + 0.0102), V(xx + sg * 0.012 - 0.005, yy + 0.01, Z0 + 0.0102)], 'su', Z)
# marble start lines with the toe grooves and the lane posts
for yy in (TY0 + 0.04, TY1 - 0.04):
    kutu_merkez(y, ((TX0 + TX1) / 2, yy), TX1 - TX0 - 0.024, 0.024, 0.005, 'mermer', z0=Z0)
    for g_ in (-0.004, 0.004):
        y.yuz_yon([V(TX0 + 0.012, yy + g_ - 0.0012, Z0 + 0.0052), V(TX1 - 0.012, yy + g_ - 0.0012, Z0 + 0.0052),
                   V(TX1 - 0.012, yy + g_ + 0.0012, Z0 + 0.0052), V(TX0 + 0.012, yy + g_ + 0.0012, Z0 + 0.0052)], 'tas_koyu', Z)
    for k in range(9):
        xx = TX0 + 0.016 + (TX1 - TX0 - 0.032) * k / 8
        kutu_merkez(y, (xx, yy), 0.005, 0.005, 0.035, 'mermer', z0=Z0 + 0.005)
# runners in the race
for k, (xx, yy) in enumerate(((0.68, 0.1), (0.72, 0.16), (0.76, 0.13), (0.8, 0.05), (0.84, 0.11))):
    kosucu(xx, yy, zt, math.pi / 2)

y.bolum('Kript tüneli')
# the vaulted tunnel through the south bank: a stone portal on the outer slope, the exit arch at the track end
PX0, PX1 = 0.68, 0.86
PH = 0.18
PY0, PY1 = -1.04, -0.9
y.kemerli(V(PX0, PY0), V(PX1, PY0), Z0, PH, ('kirec', 'tas_koyu', 'tas_acik', 'koyu'), v0=0.0, en=0.5, ust=0.05, derin=0.055, k_say=10,
          cerceve=(0.012, ['kirec', 'tas_koyu']))
for xx, sx in ((PX0, -1), (PX1, 1)):
    y.yuz_yon([V(xx, PY0, Z0), V(xx, PY1, Z0), V(xx, PY1, Z0 + PH), V(xx, PY0, Z0 + PH)], 'kirec', V(sx, 0))
    kutu_merkez(y, (xx - sx * 0.012, PY0 - 0.006), 0.026, 0.014, PH - 0.012, 'kirec', z0=Z0)       # pilasters
duz_duvar(y, V(PX1, PY1), V(PX0, PY1), Z0, Z0 + PH, 'kirec')
kornis(y, PX0 - 0.006, PX1 + 0.006, PY0 - 0.013, PY1, Z0 + PH - 0.012, 0.014, 0.008, 'tas_acik', 'tac')
y.yuz_yon([V(PX0 - 0.006, PY0 - 0.013, Z0 + PH + 0.002), V(PX1 + 0.006, PY0 - 0.013, Z0 + PH + 0.002), V(PX1 + 0.006, PY1, Z0 + PH + 0.002),
           V(PX0 - 0.006, PY1, Z0 + PH + 0.002)], 'tas_acik', Z)
y.kemerli(V(PX1, -0.7), V(PX0, -0.7), Z0, PH * 0.9, ('kirec', 'tas_koyu', 'tas_acik', 'koyu'), v0=0.0, en=0.5, ust=0.04, derin=0.06, k_say=10,
          cerceve=(0.01, ['kirec', 'tas_koyu']))
for xx, sx in ((PX0, -1), (PX1, 1)):
    y.yuz_yon([V(xx, -0.82, Z0), V(xx, -0.7, Z0), V(xx, -0.7, Z0 + PH * 0.9), V(xx, -0.82, Z0 + PH * 0.9)], 'kirec', V(sx, 0))
y.yuz_yon([V(PX0, -0.82, Z0 + PH * 0.9), V(PX1, -0.82, Z0 + PH * 0.9), V(PX1, -0.7, Z0 + PH * 0.9), V(PX0, -0.7, Z0 + PH * 0.9)], 'kirec', Z)
duz_duvar(y, V(PX0, -0.82), V(PX1, -0.82), Z0, Z0 + PH * 0.9, 'kirec')
sancak(y, PX0 + 0.02, -0.95, Z0 + PH + 0.002, boy=0.26, en=0.12, yuk=0.075, aci=math.pi * 0.85)
sancak(y, PX1 - 0.02, -0.95, Z0 + PH + 0.002, boy=0.26, en=0.12, yuk=0.075, aci=math.pi * 0.15)

y.bolum('Hakem kürsüsü, Demeter sunağı, seyirciler')
# the judges' stand cut into the east bank: a stone platform with benches, the Hellanodikai in purple
JY0, JY1 = 0.0, 0.2
JX0 = 0.905
zj = Z0 + 0.06
kutu(y, V(JX0, JY1, Z0), -Y, JY1 - JY0, 0.1, zj - Z0, 'kirec', 'onarkasagsolust')
silme(y, [V(JX0, JY1), V(JX0, JY0)], zj - 0.008, 0.008, 0.005, 'tas_acik', 'tac', kapali=False)
for k in range(2):
    kutu(y, V(JX0 + 0.03 + k * 0.03, JY1 - 0.01, zj), -Y, JY1 - JY0 - 0.02, 0.012, 0.012 + 0.01 * k, 'mermer', 'onarkasagsolust')
for k in range(7):
    seyirci(JX0 + 0.04 + (k % 2) * 0.03, JY0 + 0.02 + 0.16 * k / 6, zj + 0.012 + 0.01 * (k % 2), 300 + k)
for yy in (JY0 + 0.006, JY1 - 0.006):
    y.prizma((JX0 + 0.006, yy), 0.003, zj, zj + 0.06, 'ahsap', n=5)
cati_kirma(y, JX0, JX0 + 0.09, JY0, JY1, zj + 0.06, 0.02, 0.01, 'kumas', alt_key='kumas', kalinlik=0.003, ns=4, nr=2, dilim=['kumas', 'boya_kirmizi'])
# the altar of Demeter Chamyne on the west bank, her priestess the only woman allowed to watch
kutu_merkez(y, (0.495, 0.1), 0.05, 0.08, 0.025, 'mermer', z0=Z0 + HB)
kornis(y, 0.47, 0.52, 0.06, 0.14, Z0 + HB + 0.02, 0.006, 0.004, 'mermer', 'tac')
donel(y, (0.495, 0.1), [(0.008, Z0 + HB + 0.026), (0.006, Z0 + HB + 0.04), (0.0, Z0 + HB + 0.05)], 'boya_sari', n=6)
seyirci(0.5, 0.17, Z0 + HB, 77, oturan=False)
# the crowd on the banks
g = random.Random(31)
for k in range(40):
    c = g.uniform(0.925, 1.01)
    yy = g.uniform(-0.62, 0.9)
    if JY0 - 0.02 < yy < JY1 + 0.02: continue
    seyirci(c, yy, Z0 + (c - 0.9) / 0.13 * 0.17 - 0.002, 1000 + k)
for k in range(16):
    seyirci(g.uniform(0.475, 0.515), g.uniform(-0.7, 0.9), Z0 + HB, 2000 + k, oturan=g.random() < 0.5)
for k in range(14):
    c = g.uniform(-0.79, -0.72)
    xx = g.uniform(0.42, 0.62) if k % 2 else g.uniform(0.9, 1.1)
    seyirci(xx, c, Z0 + (-0.7 - c) / 0.1 * HB - 0.002, 3000 + k)
for k in range(12):
    seyirci(g.uniform(0.42, 1.1), g.uniform(0.97, 1.03), Z0 + (g.uniform(0.95, 1.0) - 0.95) / 0.07 * HB, 4000 + k)

# ================================================================ the Altis
y.bolum('Zeus tapınağı')
TX, TY = -0.38, -0.04
with parca(y, (TX, TY, 0)):
    tepe, zs = dor_tapinak(1.38, 0.575, 13, 6, Z0, 0.42, 0.026)

y.bolum('Philippeion')
FX, FY = -0.94, -0.7
for k, (r, h) in enumerate(((0.135, 0.016), (0.124, 0.016), (0.113, 0.016))):
    donel(y, (FX, FY), [(r, Z0 + h * k), (r, Z0 + h * (k + 1)), (0.0, Z0 + h * (k + 1))], 'mermer', n=24)
zf = Z0 + 0.048
HF = 0.17
for i in range(18):
    a = TAU * (i + 0.5) / 18
    kolon(FX + 0.1 * math.cos(a), FY + 0.1 * math.sin(a), zf, zf + HF, 0.0085, 'iyon', 'mermer', yiv=8)
# the round cella: wall with a door facing the temple, windows between Corinthian half-columns (the gilded statues inside)
cw = cokgen((FX, FY), 0.068, 18, kat=-math.pi / 2 - TAU / 36)
for i in range(18):
    a, b = cw[i], cw[(i + 1) % 18]
    if i == 0:
        dikdortgen_acik(y, a, b, zf, HF, 0.15, 0.85, 0.0, HF * 0.72, ('kirec', 'tas_acik', 'tas_acik', 'bronz'), derin=0.006)
    elif i % 3 == 0:
        dikdortgen_acik(y, a, b, zf, HF, 0.25, 0.75, HF * 0.42, HF * 0.72, ('kirec', 'tas_acik', 'tas_acik', 'koyu'), derin=0.006)
    else:
        duz_duvar(y, a, b, zf, zf + HF, 'kirec')
donel(y, (FX, FY), [(0.112, zf + HF), (0.114, zf + HF + 0.012), (0.114, zf + HF + 0.022), (0.122, zf + HF + 0.03), (0.122, zf + HF + 0.034)], 'mermer', n=24)
donel(y, (FX, FY), [(0.0, zf + HF), (0.112, zf + HF)], 'tas_koyu', n=24)
# dentils round the cornice
for i in range(36):
    a = TAU * i / 36
    kutu_merkez(y, (FX + 0.117 * math.cos(a), FY + 0.117 * math.sin(a)), 0.006, 0.004, 0.005, 'mermer', z0=zf + HF + 0.016, aci=a + math.pi / 2)
zr = zf + HF + 0.034
donel(y, (FX, FY), [(0.13, zr), (0.13, zr + 0.004), (0.09, zr + 0.04), (0.04, zr + 0.065), (0.0, zr + 0.074)], 'kiremit', n=24,
      dilim=['kiremit', 'kiremit2'])
for i in range(24):   # the cover-tile ribs radiating down the cone
    a = TAU * (i + 0.5) / 24
    kiremit_kaburga(V(FX + 0.13 * math.cos(a), FY + 0.13 * math.sin(a), zr + 0.004), V(FX + 0.045 * math.cos(a), FY + 0.045 * math.sin(a), zr + 0.062),
                    w=0.006, key='kiremit2')
donel(y, (FX, FY), [(0.012, zr + 0.068), (0.016, zr + 0.08), (0.008, zr + 0.096), (0.0, zr + 0.1)], 'bronz', n=10)     # the bronze poppy

y.bolum('Zeus sunağı, Paionios Nikesi, Zanes')
# the ash altar of Zeus: a stone base and a cone of ash, a fire smoking on top, steps cut up its side
AX_, AY_ = -0.98, -0.18
donel(y, (AX_, AY_), [(0.08, Z0), (0.08, Z0 + 0.03), (0.0, Z0 + 0.03)], 'kirec', n=20)
halka_kornis(y, (AX_, AY_), 0.08, Z0 + 0.024, 0.008, 0.006, 20, 'tas_acik', profil='tac')
donel(y, (AX_, AY_), [(0.07, Z0 + 0.03), (0.055, Z0 + 0.07), (0.03, Z0 + 0.11), (0.018, Z0 + 0.12), (0.0, Z0 + 0.122)], 'kaya_koyu', n=16)
donel(y, (AX_, AY_), [(0.016, Z0 + 0.12), (0.012, Z0 + 0.14), (0.0, Z0 + 0.16)], 'boya_kirmizi', n=8)
donel(y, (AX_, AY_), [(0.009, Z0 + 0.13), (0.006, Z0 + 0.15), (0.0, Z0 + 0.17)], 'boya_sari', n=6)
merdiven(y, (AX_ + 0.1, AY_), math.pi, 0.03, Z0, Z0 + 0.09, n=7, d=0.011, key='kirec')
# the Nike of Paionios: a tall triangular pillar, the Victory alighting on top
NX, NY = 0.2, -0.7
kutu_merkez(y, (NX, NY), 0.1, 0.1, 0.02, 'kirec', z0=Z0)
y.prizma((NX, NY), 0.045, Z0 + 0.02, Z0 + 0.05, 'mermer', n=3, kat=-math.pi / 2)
donel(y, (NX, NY), [(0.04, Z0 + 0.05), (0.03, Z0 + 0.4)], 'mermer', n=3, kat=-math.pi / 2)
y.prizma((NX, NY), 0.034, Z0 + 0.4, Z0 + 0.412, 'mermer', n=3, kat=-math.pi / 2)
nike(NX, NY, Z0 + 0.412, 0.9, 'mermer', aci=-math.pi / 2)
# the Zanes: bronze Zeus statues paid for by cheats, lined up before the stadium crypt
for k in range(6):
    xx = 0.02 + k * 0.055
    kutu_merkez(y, (xx, -0.97), 0.036, 0.036, 0.035, 'kirec', z0=Z0)
    kornis(y, xx - 0.018, xx + 0.018, -0.988, -0.952, Z0 + 0.03, 0.006, 0.004, 'tas_acik', 'tac')
    figur(xx, -0.97, Z0 + 0.036, 0.6, 'bronz', aci=-math.pi / 2, kol=1.0 if k % 2 else 0.8)

y.bolum('Hazineler terası')
# the terrace of the treasuries at the foot of Mount Kronos: a retaining wall, steps, small Doric temples in antis
QY = 0.84
QX0, QX1 = -1.12, 0.33
QZ = Z0 + 0.05
duz_duvar(y, V(QX0, QY), V(QX1, QY), Z0, QZ, 'kirec')
duz_duvar(y, V(QX1, QY), V(QX1, 1.05), Z0, QZ, 'kirec')
silme(y, [V(QX0, QY), V(QX1, QY), V(QX1, 1.05)], QZ - 0.008, 0.008, 0.005, 'tas_acik', 'tac', kapali=False)
y.yuz_yon([V(QX0, QY, QZ), V(QX1, QY, QZ), V(QX1, 1.05, QZ), V(QX0, 1.05, QZ)], 'toprak', Z)
for k in range(4):   # step flights up from the Altis
    merdiven(y, (QX0 + 0.2 + k * 0.4, QY - 0.06), math.pi / 2, 0.08, Z0, QZ, n=5, d=0.012, key='kirec')
for k, xx in enumerate((-0.98, -0.72, -0.46, -0.2, 0.06)):
    w, d = 0.13, 0.15
    y0 = QY + 0.04
    kutu(y, V(xx - w / 2 - 0.01, y0 - 0.01, QZ), X, w + 0.02, d + 0.02, 0.012, 'kirec', 'onarkasagsolust')
    zb = QZ + 0.012
    hh = 0.1 + 0.01 * (k % 2)
    duz_duvar(y, V(xx + w / 2, y0 + 0.04), V(xx + w / 2, y0 + d), zb, zb + hh, 'kirec')
    duz_duvar(y, V(xx + w / 2, y0 + d), V(xx - w / 2, y0 + d), zb, zb + hh, 'kirec')
    duz_duvar(y, V(xx - w / 2, y0 + d), V(xx - w / 2, y0 + 0.04), zb, zb + hh, 'kirec')
    dikdortgen_acik(y, V(xx - w / 2, y0 + 0.04), V(xx + w / 2, y0 + 0.04), zb, hh, 0.36, 0.64, 0.0, hh * 0.65, ('kirec', 'tas_acik', 'tas_acik', 'bronz'),
                    derin=0.006)
    for sx in (-1, 1):
        y.yuz_yon([V(xx + sx * w / 2, y0, zb), V(xx + sx * w / 2, y0 + 0.04, zb), V(xx + sx * w / 2, y0 + 0.04, zb + hh), V(xx + sx * w / 2, y0, zb + hh)],
                  'kirec', V(sx, 0))
        y.yuz_yon([V(xx + sx * (w / 2 - 0.012), y0 + 0.04, zb), V(xx + sx * (w / 2 - 0.012), y0, zb), V(xx + sx * (w / 2 - 0.012), y0, zb + hh),
                   V(xx + sx * (w / 2 - 0.012), y0 + 0.04, zb + hh)], 'kirec', V(-sx, 0))
        y.yuz_yon([V(xx + sx * w / 2, y0, zb), V(xx + sx * (w / 2 - 0.012), y0, zb), V(xx + sx * (w / 2 - 0.012), y0, zb + hh), V(xx + sx * w / 2, y0, zb + hh)],
                  'kirec', -Y)
        kolon(xx + sx * 0.022, y0 + 0.006, zb, zb + hh, 0.0075, 'dor', 'kirec', yiv=8)
    kutu(y, V(xx - w / 2 - 0.002, y0 - 0.006, zb + hh), X, w + 0.004, d + 0.008, 0.012, 'kirec', 'onarkasagsol')
    y.yuz_yon([V(xx - w / 2, y0 - 0.006, zb + hh), V(xx + w / 2, y0 - 0.006, zb + hh), V(xx + w / 2, y0 + 0.04, zb + hh), V(xx - w / 2, y0 + 0.04, zb + hh)],
              'tas_koyu', -Z)
    triglif_dizi(V(xx - w / 2 - 0.002, y0 - 0.0065), V(xx + w / 2 + 0.002, y0 - 0.0065), zb + hh + 0.004, 0.007, 4, w=0.007,
                 metop='boya_kirmizi' if k % 2 else 'lacivert', rolyef=False)
    zr = zb + hh + 0.012
    y.yuz_yon([V(xx - w / 2 - 0.002, y0 - 0.006, zr), V(xx + w / 2 + 0.002, y0 - 0.006, zr), V(xx + w / 2 + 0.002, y0 + d + 0.002, zr),
               V(xx - w / 2 - 0.002, y0 + d + 0.002, zr)], 'kirec', Z)
    alinlik(y, V(xx - w / 2 - 0.006, y0 - 0.01), V(xx + w / 2 + 0.006, y0 - 0.01), zr, 0.03, derin=d + 0.012, key='kirec', ic_key='lacivert', c=0.006,
            cati_key='kiremit')
    alinlik(y, V(xx + w / 2 + 0.006, y0 + d + 0.002), V(xx - w / 2 - 0.006, y0 + d + 0.002), zr, 0.03, derin=0.003, key='kirec', ic_key='lacivert',
            c=0.006, cati_key='kiremit')
    kiremit_serit(xx - w / 2 - 0.006, xx + w / 2 + 0.006, y0 - 0.004, y0 + d - 0.004, zr + 0.0048, 0.03, adim=0.02, key='kiremit2')
    donel(y, (xx, y0 - 0.01), [(0.0, zr + 0.032), (0.007, zr + 0.036), (0.01, zr + 0.046), (0.0, zr + 0.054)], 'altin', n=6)

y.bolum('Altis duvarı, yollar, ağaçlar')
# the low Altis wall with a gate opposite the temple front
AW = 0.05


def altis_duvari(a, b):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized()
    L = (b - a).length
    kutu(y, a + Z * Z0, e, L, 0.024, AW, 'kirec', 'onarkasagsolust')
    kutu(y, a + V(e.y, -e.x) * 0.004 + Z * (Z0 + AW), e, L, 0.032, 0.008, 'tas_acik', 'onarkasagsolust')
    n = max(1, int(L / 0.16))
    for k in range(n + 1):
        p = a.lerp(b, k / n) + Z.cross(e) * 0.012
        kutu_merkez(y, (p.x, p.y), 0.034, 0.034, AW + 0.02, 'kirec', z0=Z0)


altis_duvari(V(-1.12, -1.02), V(-0.52, -1.02))
altis_duvari(V(-0.24, -1.02), V(0.32, -1.02))
altis_duvari(V(-1.12, QY - 0.08), V(-1.12, -1.02))
# the gate: four columns and a little pediment
for k in range(4):
    kolon(-0.5 + k * 0.08, -1.02, Z0, Z0 + 0.13, 0.008, 'dor', 'kirec', yiv=8)
kutu(y, V(-0.52, -1.035, Z0 + 0.13), X, 0.28, 0.03, 0.02, 'kirec', 'onarkasagsol')
y.yuz_yon([V(-0.52, -1.035, Z0 + 0.13), V(-0.24, -1.035, Z0 + 0.13), V(-0.24, -1.005, Z0 + 0.13), V(-0.52, -1.005, Z0 + 0.13)], 'tas_koyu', -Z)
y.yuz_yon([V(-0.52, -1.035, Z0 + 0.15), V(-0.24, -1.035, Z0 + 0.15), V(-0.24, -1.005, Z0 + 0.15), V(-0.52, -1.005, Z0 + 0.15)], 'kirec', Z)
alinlik(y, V(-0.525, -1.04), V(-0.235, -1.04), Z0 + 0.15, 0.035, derin=0.037, key='kirec', ic_key='lacivert', c=0.006, cati_key='kiremit')
alinlik(y, V(-0.235, -1.0), V(-0.525, -1.0), Z0 + 0.15, 0.035, derin=0.003, key='kirec', ic_key='lacivert', c=0.006, cati_key='kiremit')
# paved ways: gate to the temple ramp, and along the treasuries
y.yuz_yon([V(-0.46, -1.0, Z0 + 0.002), V(-0.3, -1.0, Z0 + 0.002), V(-0.3, -0.94, Z0 + 0.002), V(-0.46, -0.94, Z0 + 0.002)], 'zemin', Z)
y.yuz_yon([V(0.06, -0.94, Z0 + 0.002), V(0.36, -0.94, Z0 + 0.002), V(0.36, -0.88, Z0 + 0.002), V(0.06, -0.88, Z0 + 0.002)], 'zemin', Z)
# wild olives (the victors' crowns were cut from them) and plane trees
for x, yy, s in ((0.24, -0.38, 1.0), (0.22, 0.06, 1.1), (0.26, 0.48, 0.9), (-1.0, 0.32, 1.0), (-1.0, 0.6, 0.9)):
    zeytin(x, yy, Z0, 0.16 * s, s)
for x, yy in ((-1.02, -0.42), (0.3, -0.12)):
    amfora(x, yy, Z0, 1.3)
# votive bronzes along the temple's north side
for k in range(4):
    xx = 0.12
    yy = 0.3 - k * 0.15 + 0.0
    if abs(yy - 0.06) < 0.06: continue
    kutu_merkez(y, (xx, yy), 0.04, 0.04, 0.04, 'kirec', z0=Z0)
    figur(xx, yy, Z0 + 0.04, 0.65, 'bronz', aci=math.pi, kol=0.9)

calistir(y, 'lm_olimpia')
