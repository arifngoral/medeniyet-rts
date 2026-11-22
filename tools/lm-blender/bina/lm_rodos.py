# The harbour of Rhodes (lm_rodos): two moles walled and towered on the sea side closing the harbour, the bronze
# Colossus of Helios standing on his marble base at the head of the west mole (one figure, torch raised, radiate
# crown, cloak to a stump), the lighthouse on the east mole's head, the ship sheds (neosoikoi) with their slipways
# and long tiled roofs, the merchants' stoa on the quay with its goods and crane, a Doric temple of Helios in the
# upper town, houses, the towered city wall, and ships: a trireme rowing out, a merchantman, a galley, a trader.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
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
        kure(y, (x + dx * s, yy + dy * s, z + boy * dz + 0.02 * s), r * s, 'zeytin', n=9, kat=5)


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


def dor_tapinak(L, W, nl, nw, z0, HC, r, key='kirec', cati='kiremit', kaburga='kiremit2', sb=0.025, porch_n=2, heykel=True):
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
        kolon(p.x, p.y, zs, zc, r, 'dor', key, yiv=8)
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
            hs = HC / 0.42
            kutu_merkez(y, (pc.x, pc.y), 0.08 * hs, 0.02, 0.12 * hs, 'altin', z0=zs)
            donel(y, (pc.x, pc.y), [(0.03 * hs, zs + 0.06 * hs), (0.026 * hs, zs + 0.15 * hs), (0.018 * hs, zs + 0.2 * hs), (0.0, zs + 0.215 * hs)], 'altin', n=10)
            kure(y, (pc.x, pc.y, zs + 0.23 * hs), 0.014 * hs, 'tas_acik', n=8, kat=4)
        duz_duvar(y, a, b, zc, zc + ha, key)
        for i in range(porch_n):
            xx = -cx + 2 * cx * (i + 1) / (porch_n + 1)
            kolon(xx, sg * ya, zs, zc, r * 0.9, 'dor', key, yiv=8)
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
    kiremit_serit(xa, xb, ya_ + 0.012, yb_ - 0.012, ze + 0.0096, ph, adim=0.026, key=kaburga)
    cubuk(y, V(0, ya_, ze + ph + 0.013), V(0, yb_, ze + ph + 0.013), 0.013, kaburga)
    sp = 0.012 * 1.6
    zt0 = ze + sp
    HT = ph - 2.9 * sp
    hw = (xb - xa) / 2

    def H(x):
        return max(0.004, HT * (1 - abs(x) / (hw * 0.93)) * 0.9)
    for yy, sg in ((ya_, -1), (yb_, 1)):
        yt = yy - sg * 0.0005
        zap = ze + ph + 0.013
        if not heykel:   # a small temple: a gilded disc of the sun in the pediment, palmette acroteria
            y.yuz_yon([V(0.03 * math.cos(TAU * a / 16), yt - sg * 0.001, zt0 + HT * 0.42 + 0.03 * math.sin(TAU * a / 16)) for a in range(16)], 'altin', V(0, sg, 0))
            donel(y, (0, yy), [(0.0, zap), (0.01, zap + 0.004), (0.014, zap + 0.016), (0.008, zap + 0.026), (0, zap + 0.032)], 'altin', n=8)
            for xx in (xa + 0.012, xb - 0.012):
                kure(y, (xx, yy - sg * 0.004, ze + 0.016), 0.008, 'altin', n=8, kat=4)
            continue
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
        nike(0, yy, zap, 0.8 * max(0.5, HC / 0.42), 'altin', aci=math.pi / 2 * (-sg))
        for xx in (xa + 0.016, xb - 0.016):
            kutu_merkez(y, (xx, yy - sg * 0.006), 0.026, 0.026, 0.008, key, z0=ze + 0.008)
            tripod(xx, yy - sg * 0.006, ze + 0.016, 1.3 * max(0.5, HC / 0.42))
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
    donel(y, (x, yy), [(0.0065, z), (0.0055, z + h * 0.6), (0.0035, z + h), (0.0, z + h + 0.001)], k, n=6, kat=g.random())
    kure(y, (x, yy, z + h + 0.004), 0.0042, 'kerpic', n=6, kat=3)


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


ZS = 0.025                  # the water surface
ZK = 0.075                  # the quays and the moles


def gemi(cx, cy, aci, L=0.34, B=0.052, H=0.03, kurek=True, yelken=True, tur='trieres', tohum=1, dz=0.0):
    """a ship on the water at (cx, cy) heading towards aci: a lofted hull (dark wood, a red wale, a painted eye),
    a bronze ram and a curling stern post (trieres) or a round merchant hull (holkas), oars, a mast with a sail"""
    g = random.Random(tohum)
    with parca(y, (cx, cy, dz), aci):
        n = 12
        st = []
        for i in range(n + 1):
            t = i / n
            x = -L / 2 + L * t
            if tur == 'trieres':
                w = B / 2 * max(0.12, math.sin(math.pi * min(1, max(0, (t - 0.02) / 0.96))) ** 0.55)
                h = H + (0.04 * ((0.18 - t) / 0.18) ** 2 if t < 0.18 else 0) + (0.012 * ((t - 0.85) / 0.15) if t > 0.85 else 0)
            else:
                w = B / 2 * max(0.18, math.sin(math.pi * t) ** 0.4)
                h = H + 0.018 * (abs(t - 0.5) * 2) ** 3
            st.append((x, w, h))
        kz = ZS - 0.012
        for i in range(n):
            (x0, w0, h0), (x1, w1, h1) = st[i], st[i + 1]
            for s in (-1, 1):
                pk0, pk1 = V(x0, 0, kz), V(x1, 0, kz)
                m0, m1 = V(x0, s * w0, ZS + h0 * 0.45), V(x1, s * w1, ZS + h1 * 0.45)
                r0, r1 = V(x0, s * w0 * 1.02, ZS + h0 * 0.62), V(x1, s * w1 * 1.02, ZS + h1 * 0.62)
                g0, g1 = V(x0, s * w0, ZS + h0), V(x1, s * w1, ZS + h1)
                for (a0, a1, b1, b0), key in (((pk0, pk1, m1, m0), 'ahsap_koyu'), ((m0, m1, r1, r0), 'boya_kirmizi'), ((r0, r1, g1, g0), 'ahsap')):
                    y.yuz_yon([a0, a1, b1, b0], key, V(0, s, 0.2))
            # the deck
            y.yuz_yon([V(x0, -w0, ZS + h0 * 0.92), V(x1, -w1, ZS + h1 * 0.92), V(x1, w1, ZS + h1 * 0.92), V(x0, w0, ZS + h0 * 0.92)], 'ahsap_acik', Z)
            # the bulwark's inner face down to the deck
            for s in (-1, 1):
                y.yuz_yon([V(x0, s * w0, ZS + h0 * 0.92), V(x1, s * w1, ZS + h1 * 0.92), V(x1, s * w1, ZS + h1), V(x0, s * w0, ZS + h0)], 'ahsap', V(0, -s, 0))
                y.yuz_yon([V(x0, s * w0, ZS + h0), V(x1, s * w1, ZS + h1), V(x1, s * w1 * 0.97, ZS + h1 + 0.0001), V(x0, s * w0 * 0.97, ZS + h0 + 0.0001)],
                          'ahsap', Z)
        for i, sg in ((0, -1), (n, 1)):   # end caps
            x, w, h = st[i]
            y.yuz_yon([V(x, -w, ZS + h), V(x, -w * 1.02, ZS + h * 0.62), V(x, -w, ZS + h * 0.45), V(x, 0, kz), V(x, w, ZS + h * 0.45),
                       V(x, w * 1.02, ZS + h * 0.62), V(x, w, ZS + h)], 'ahsap_koyu', V(sg, 0, 0))
        xb, wb, hb = st[-1]
        if tur == 'trieres':
            boru(y, [V(xb - 0.01, 0, ZS - 0.002), V(xb + 0.035, 0, ZS - 0.001)], 0.007, 'bronz', n=8, r_son=0.002)       # the ram
            for s in (-1, 1):   # the eyes
                c = V(xb - 0.03, s * (st[-3][1] + 0.0015), ZS + st[-3][2] * 0.78)
                y.yuz_yon([c + V(0.008 * math.cos(TAU * k / 8), 0, 0.005 * math.sin(TAU * k / 8)) for k in range(8)], 'beyaz', V(0, s, 0))
                y.yuz_yon([c + V(0, s * 0.0005, 0) + V(0.003 * math.cos(TAU * k / 6), 0, 0.003 * math.sin(TAU * k / 6)) for k in range(6)], 'koyu', V(0, s, 0))
            # the stern post curling forward over the steersman
            x0, w0, h0 = st[0]
            boru(y, [V(x0, 0, ZS + h0 - 0.005), V(x0 - 0.012, 0, ZS + h0 + 0.02), V(x0 - 0.002, 0, ZS + h0 + 0.042), V(x0 + 0.014, 0, ZS + h0 + 0.046)],
                 0.004, 'ahsap', n=6, r_son=0.002)
            for s in (-1, 1):   # steering oars
                cubuk(y, V(x0 + 0.03, s * (w0 + 0.01), ZS + h0 * 0.7), V(x0 - 0.01, s * (w0 + 0.02), ZS - 0.004), 0.0035, 'ahsap_acik')
        else:
            boru(y, [V(xb - 0.005, 0, ZS + hb - 0.004), V(xb + 0.012, 0, ZS + hb + 0.012), V(xb + 0.008, 0, ZS + hb + 0.026)], 0.0035, 'ahsap', n=5)
            boru(y, [V(st[0][0] + 0.004, 0, ZS + st[0][2] - 0.004), V(st[0][0] - 0.012, 0, ZS + st[0][2] + 0.014), V(st[0][0] - 0.004, 0, ZS + st[0][2] + 0.03)],
                 0.0045, 'ahsap', n=5)
        if kurek:
            m = 13
            for k in range(m):
                x = -L * 0.32 + L * 0.62 * k / (m - 1)
                w = B / 2 * 1.02
                for s in (-1, 1):
                    for row, dz in enumerate((0.0, 0.009)):
                        a = V(x, s * w, ZS + H * 0.5 + dz)
                        b = V(x + 0.012 + 0.004 * row, s * (w + 0.075 + 0.012 * row), ZS - 0.002)
                        cubuk(y, a, b, 0.0022, 'ahsap_acik')
        if yelken:
            mh = 0.2 if tur == 'trieres' else 0.17
            y.prizma((0.0 if tur == 'trieres' else 0.01, 0), 0.0035, ZS + H * 0.9, ZS + H + mh, 'ahsap', n=6)
            ys = ZS + H + mh - 0.012
            sw = B * 1.25 if tur == 'trieres' else B * 1.1
            cubuk(y, V(0.0, -sw * 0.62, ys), V(0.0, sw * 0.62, ys), 0.004, 'ahsap')
            sh = mh * 0.62
            for k in range(4):
                z0_, z1_ = ys - sh * k / 4, ys - sh * (k + 1) / 4
                b0, b1 = 0.012 * math.sin(math.pi * k / 4), 0.012 * math.sin(math.pi * (k + 1) / 4)
                key = 'boya_kirmizi' if k == 1 else ('beyaz' if tur == 'trieres' else 'kumas')
                for d in (1, -1):
                    o0, o1 = 0.0008 * d + 0.002 + b0, 0.0008 * d + 0.002 + b1
                    y.yuz_yon([V(o0, -sw / 2, z0_), V(o0, sw / 2, z0_), V(o1, sw / 2, z1_), V(o1, -sw / 2, z1_)], key, V(d, 0, 0))
                for sy_ in (-1, 1):   # the sail's side edges (so the two sheets close)
                    y.yuz_yon([V(0.0012 + b0, sy_ * sw / 2, z0_), V(0.0028 + b0, sy_ * sw / 2, z0_), V(0.0028 + b1, sy_ * sw / 2, z1_),
                               V(0.0012 + b1, sy_ * sw / 2, z1_)], key, V(0, sy_, 0))
                if k == 3:
                    y.yuz_yon([V(0.0012 + b1, -sw / 2, z1_), V(0.0028 + b1, -sw / 2, z1_), V(0.0028 + b1, sw / 2, z1_), V(0.0012 + b1, sw / 2, z1_)], key, -Z)


def loft(rings, key, kapat=(True, True)):
    """a closed skin through rings of points (each ring the same count, CCW seen from its far end), capped"""
    n = len(rings[0])
    cs = [sum(r, Vector()) / n for r in rings]
    for k in range(len(rings) - 1):
        A, B = rings[k], rings[k + 1]
        for i in range(n):
            j = (i + 1) % n
            q = [A[i], A[j], B[j], B[i]]
            c = (cs[k] + cs[k + 1]) / 2
            yuz_dis(y, q, key, c)
    if kapat[0]:
        y.yuz_yon(rings[0], key, cs[0] - cs[1])
    if kapat[1]:
        y.yuz_yon(rings[-1], key, cs[-1] - cs[-2])


def uzuv(pts, rr, key, n=12, yass=1.0, kapat=(True, True)):
    """a limb along pts with a radius per point (muscle swell); yass: the ring's depth / width (a flattened limb)"""
    pts = [Vector(p) for p in pts]
    m = len(pts)
    rings = []
    u0 = None
    for k in range(m):
        t = (pts[min(k + 1, m - 1)] - pts[max(k - 1, 0)]).normalized()
        u = Y.cross(t) if abs(t.y) < 0.9 else X.cross(t)
        u.normalize()
        if u0 is not None and u.dot(u0) < 0: u = -u
        u0 = u; w = t.cross(u).normalized()
        rings.append([pts[k] + u * (rr[k] * math.cos(TAU * i / n)) + w * (rr[k] * yass * math.sin(TAU * i / n)) for i in range(n)])
    loft(rings, key, kapat)


def elips(c, rx, ry, rz, key, n=14, kat=8):
    """an ellipsoid (head, pectoral, calf)"""
    c = Vector(c)
    rings = []
    for k in range(1, kat):
        a = math.pi * k / kat
        zz, rr = -math.cos(a), math.sin(a)
        rings.append([c + V(rx * rr * math.cos(TAU * i / n), ry * rr * math.sin(TAU * i / n), rz * zz) for i in range(n)])
    loft(rings, key, (False, False))
    for ring, sg in ((rings[0], -1), (rings[-1], 1)):
        tip = c + V(0, 0, sg * rz)
        for i in range(n):
            j = (i + 1) % n
            yuz_dis(y, [ring[i], ring[j], tip] if sg > 0 else [ring[j], ring[i], tip], key, c)


def kolossos(x, yy, z, s=1.0, key='bronz'):
    """the Colossus of Helios: a nude youth standing in contrapposto on his pedestal, looking out to sea (-y): the
    radiate crown of the sun god, the right hand raising a torch, the cloak over the left forearm falling in folds
    to the ground as the statue's third support; about s * 1.0 tall to the flame"""
    with parca(y, (x, yy, z), 0.0, s):
        # ---- legs: the weight on the right (straight), the left relaxed, its knee forward and the heel lifted
        for kn, ank, ayak, hip in (((0.048, -0.004, 0.225), (0.05, 0.004, 0.04), ((0.05, 0.02, 0.012), (0.052, -0.015, 0.012), (0.054, -0.058, 0.008)),
                                    (0.044, 0.0, 0.41)),
                                   ((-0.056, -0.034, 0.23), (-0.066, -0.006, 0.05), ((-0.066, 0.01, 0.03), (-0.069, -0.025, 0.016), (-0.072, -0.064, 0.008)),
                                    (-0.044, 0.0, 0.405))):
            hip, kn, ank = V(*hip), V(*kn), V(*ank)
            # one continuous skin from the hip over the knee to the ankle (no mannequin joint)
            uzuv([hip + V(0, 0, 0.02), hip.lerp(kn, 0.2), hip.lerp(kn, 0.45), hip.lerp(kn, 0.7), hip.lerp(kn, 0.9), kn + V(0, -0.003, 0),
                  kn.lerp(ank, 0.12) + V(0, 0.002, 0), kn.lerp(ank, 0.3) + V(0, 0.007, 0), kn.lerp(ank, 0.55) + V(0, 0.004, 0), kn.lerp(ank, 0.8), ank],
                 [0.044, 0.043, 0.039, 0.033, 0.027, 0.025, 0.025, 0.028, 0.023, 0.017, 0.015], key, n=14)
            uzuv([V(*p) for p in ayak], [0.011, 0.012, 0.008], key, n=10, yass=1.5)        # the foot (flat: wider than high)
        # ---- the trunk: hips, waist, ribcage, shoulders (elliptical rings, the chest pushed forward)
        rings = []
        for zz, rx, ry, dy in ((0.36, 0.046, 0.04, 0.0), (0.4, 0.07, 0.05, 0.0), (0.44, 0.074, 0.052, -0.002), (0.49, 0.064, 0.046, -0.004),
                               (0.54, 0.068, 0.05, -0.006), (0.6, 0.08, 0.056, -0.008), (0.645, 0.088, 0.05, -0.004), (0.675, 0.072, 0.042, 0.0),
                               (0.695, 0.034, 0.03, 0.0)):
            rings.append([V(rx * math.cos(TAU * i / 18), dy + ry * math.sin(TAU * i / 18), zz) for i in range(18)])
        loft(rings, key)
        # chest, belly and the shoulder caps
        for sx in (-1, 1):
            elips((sx * 0.034, -0.054, 0.605), 0.034, 0.014, 0.024, key, n=12, kat=6)
            elips((sx * 0.08, 0.0, 0.655), 0.03, 0.03, 0.028, key, n=12, kat=6)
        # ---- neck and head: the face to the sea, a nose, brows, curls under the crown
        uzuv([V(0, 0.0, 0.69), V(0, -0.004, 0.735)], [0.027, 0.025], key, n=12)
        elips((0, -0.006, 0.775), 0.034, 0.038, 0.045, key, n=16, kat=8)
        boru(y, [V(0, -0.041, 0.789), V(0, -0.047, 0.77)], 0.0055, key, n=8, r_son=0.0035)        # nose
        elips((0, 0.004, 0.795), 0.038, 0.04, 0.034, 'bronz', n=16, kat=6)                         # hair mass
        # the radiate crown: a gilded band and nine long rays fanning up and out
        donel(y, (0, -0.002), [(0.041, 0.795), (0.043, 0.802), (0.041, 0.812), (0.0, 0.812)], 'altin', n=18)
        for k in range(9):
            a = -math.pi / 2 + (k - 4) * 0.5
            d = V(math.cos(a), math.sin(a), 0)
            p0 = V(0, -0.002, 0.808) + d * 0.036
            uzuv([p0, p0 + d * 0.03 + Z * 0.05, p0 + d * 0.05 + Z * 0.085], [0.007, 0.004, 0.0008], 'altin', n=5)
        # ---- the right arm raised high with the torch
        sh, el, hd = V(0.086, -0.004, 0.655), V(0.124, -0.014, 0.765), V(0.13, -0.024, 0.885)
        uzuv([sh, sh.lerp(el, 0.4), sh.lerp(el, 0.85), el.lerp(hd, 0.12), el.lerp(hd, 0.4), hd], [0.03, 0.028, 0.022, 0.021, 0.022, 0.015], key, n=12)
        kure(y, hd, 0.018, key, n=10, kat=5)
        uzuv([hd - Z * 0.03, hd + Z * 0.04, hd + Z * 0.07], [0.008, 0.01, 0.017], 'bronz', n=10)
        donel(y, (hd.x, hd.y), [(0.017, hd.z + 0.07), (0.024, hd.z + 0.08), (0.0, hd.z + 0.082)], 'altin', n=12)
        donel(y, (hd.x, hd.y), [(0.02, hd.z + 0.082), (0.022, hd.z + 0.1), (0.012, hd.z + 0.13), (0.0, hd.z + 0.16)], 'boya_sari', n=10)
        donel(y, (hd.x, hd.y - 0.004), [(0.011, hd.z + 0.09), (0.009, hd.z + 0.12), (0.0, hd.z + 0.17)], 'boya_kirmizi', n=8)
        # ---- the left arm lowered, the forearm forward carrying the cloak
        sh2, el2, hd2 = V(-0.086, -0.004, 0.655), V(-0.108, 0.006, 0.535), V(-0.104, -0.05, 0.47)
        uzuv([sh2, sh2.lerp(el2, 0.4), sh2.lerp(el2, 0.85), el2.lerp(hd2, 0.12), el2.lerp(hd2, 0.4), hd2], [0.03, 0.028, 0.022, 0.021, 0.022, 0.015], key, n=12)
        kure(y, hd2, 0.017, key, n=10, kat=5)
        # the cloak: folded over the forearm, falling in a fluted mass to the ground (the third support)
        cr = []
        for k, (cx_, cy_, cz, rx, ry) in enumerate(((-0.104, -0.03, 0.5, 0.028, 0.026), (-0.11, -0.012, 0.44, 0.032, 0.03), (-0.106, 0.012, 0.33, 0.032, 0.032),
                                                    (-0.098, 0.03, 0.2, 0.033, 0.032), (-0.092, 0.04, 0.08, 0.035, 0.032), (-0.09, 0.042, 0.0, 0.038, 0.034))):
            rows = []
            for i in range(20):
                a = TAU * i / 20
                f = 1 + 0.16 * math.sin(6 * a + k * 0.5) * min(1, k / 2)
                rows.append(V(cx_ + rx * f * math.cos(a), cy_ + ry * f * math.sin(a), cz))
            cr.append(rows)
        loft(cr, key)


def kule_fener(x, yy, z):
    """a harbour lighthouse: a square stone base, an octagonal shaft, a round lantern stage with the fire"""
    kutu_merkez(y, (x, yy), 0.13, 0.13, 0.12 + z, 'kirec', z0=0.0)
    for zz in (z + 0.04, z + 0.08):
        silme(y, dikdortgen(x - 0.065, x + 0.065, yy - 0.065, yy + 0.065), zz, 0.004, 0.002, 'tas_koyu', 'duz')
    kornis(y, x - 0.065, x + 0.065, yy - 0.065, yy + 0.065, z + 0.11, 0.012, 0.008, 'tas_acik', 'tac')
    y.yuz_yon([V(x - 0.073, yy - 0.073, z + 0.122), V(x + 0.073, yy - 0.073, z + 0.122), V(x + 0.073, yy + 0.073, z + 0.122), V(x - 0.073, yy + 0.073, z + 0.122)],
              'tas_acik', Z)
    parapet(y, dikdortgen(x - 0.073, x + 0.073, yy - 0.073, yy + 0.073), z + 0.122, 0.008, 0.012, 0.01, 'kirec')
    z1 = z + 0.122
    oc = cokgen((x, yy), 0.045, 8, math.pi / 8)
    for i in range(8):
        a, b = oc[i], oc[(i + 1) % 8]
        y.kemerli(a, b, z1, 0.14, ('kirec', 'tas_koyu', 'tas_acik', 'koyu'), v0=0.06, en=0.35, ust=0.03, derin=0.01, k_say=6)
    halka_kornis(y, (x, yy), 0.045, z1 + 0.13, 0.012, 0.008, 8, 'tas_acik', kat=math.pi / 8, profil='tac')
    y.yuz_yon([V(p.x, p.y, z1 + 0.142) for p in cokgen((x, yy), 0.053, 8, math.pi / 8)], 'tas_acik', Z)
    z2 = z1 + 0.142
    for i in range(8):
        a = TAU * (i + 0.5) / 8
        y.prizma((x + 0.028 * math.cos(a), yy + 0.028 * math.sin(a)), 0.004, z2, z2 + 0.05, 'mermer', n=6, ust=False)
    donel(y, (x, yy), [(0.036, z2 + 0.05), (0.036, z2 + 0.058), (0.0, z2 + 0.058)], 'mermer', n=16)
    donel(y, (x, yy), [(0.014, z2), (0.018, z2 + 0.014), (0.012, z2 + 0.03), (0.0, z2 + 0.044)], 'boya_sari', n=8)
    donel(y, (x, yy), [(0.008, z2 + 0.01), (0.006, z2 + 0.03), (0.0, z2 + 0.046)], 'boya_kirmizi', n=6)
    donel(y, (x, yy), [(0.032, z2 + 0.058), (0.0, z2 + 0.08)], 'bronz', n=16)
    figur(x, yy, z2 + 0.078, 0.5, 'altin', kol=0.9)
    return z2 + 0.12


def mendirek(yol, en=0.1, duvar=True, bas_kes=0.0, son_kes=0.0):
    """a harbour mole along the polyline (the open sea on its right): a stone causeway en wide to the left, its
    paved top at ZK, a merloned wall on the sea side with small towers at the bends"""
    yol = [V(p[0], p[1]) for p in yol]
    ic = disa(yol, -en, kapali=False)
    for i in range(len(yol) - 1):
        a, b, ai, bi = yol[i], yol[i + 1], ic[i], ic[i + 1]
        duz_duvar(y, a, b, 0, ZK, 'tas')
        duz_duvar(y, bi, ai, 0, ZK, 'tas')
        silme(y, [a, b], ZS - 0.004, 0.012, 0.006, 'kaya_koyu', 'duz', kapali=False)
        silme(y, [bi, ai], ZS - 0.004, 0.012, 0.006, 'kaya_koyu', 'duz', kapali=False)
        y.yuz_yon([a + Z * ZK, b + Z * ZK, bi + Z * ZK, ai + Z * ZK], 'zemin', Z)
    a, ai = yol[-1], ic[-1]
    e = (yol[-1] - yol[-2]).normalized()
    y.yuz_yon([a, ai, ai + Z * ZK, a + Z * ZK], 'tas', e)
    e0 = (yol[1] - yol[0]).normalized()
    y.yuz_yon([yol[0], ic[0], ic[0] + Z * ZK, yol[0] + Z * ZK], 'tas', -e0)
    if duvar:
        e0 = (yol[1] - yol[0]).normalized()
        sur(y, [yol[0] + e0 * bas_kes] + yol[1:-1] + [yol[-1] - e * son_kes], ZK, 0.06, 0.035, 'kirec', mazgal_h=0.022, parapet_h=0.01)


# ================================================================ the sea, the land
y.bolum('Deniz ve rıhtımlar')
X0, X1, Y0, Y1 = -1.15, 1.15, -1.05, 1.05
kutu(y, V(X0, Y0, 0), X, X1 - X0, Y1 - Y0, ZS, 'kaya_koyu', 'onarkasagsol')
y.yuz_yon([V(X0, Y0, ZS), V(X1, Y0, ZS), V(X1, Y1, ZS), V(X0, Y1, ZS)], 'su', Z)
QY = 0.25
SH0, SH1 = -0.8, -0.1                        # the ship sheds' cut in the quay


def kara(x0, x1, y0, y1, on=True, sag=True, sol=True):
    """a raised land block with a stone quay face on its sea / cut sides"""
    yz = ('on' if on else '') + ('sag' if sag else '') + ('sol' if sol else '')
    if yz: kutu(y, V(x0, y0, ZS), X, x1 - x0, y1 - y0, ZK - ZS, 'tas', yz)
    y.yuz_yon([V(x0, y0, ZK), V(x1, y0, ZK), V(x1, y1, ZK), V(x0, y1, ZK)], 'zemin', Z)
    if on:
        silme(y, [V(x0, y0), V(x1, y0)], ZK - 0.01, 0.01, 0.006, 'tas_acik', 'tac', kapali=False)
        silme(y, [V(x0, y0), V(x1, y0)], ZS - 0.004, 0.01, 0.005, 'kaya_koyu', 'duz', kapali=False)


kara(X0, X1, 0.62, Y1, on=False, sag=False, sol=False)
duz_duvar(y, V(SH1, 0.62), V(SH0, 0.62), ZS, ZK, 'tas')
kara(X0, SH0, QY, 0.62, sag=True, sol=False)
kara(SH1, X1, QY, 0.62, sag=False, sol=True)
for xx, sx in ((X0, -1), (X1, 1)):
    y.yuz_yon([V(xx, QY, ZS), V(xx, Y1, ZS), V(xx, Y1, ZK), V(xx, QY, ZK)] if sx > 0 else [V(xx, Y1, ZS), V(xx, QY, ZS), V(xx, QY, ZK), V(xx, Y1, ZK)],
              'tas', V(sx, 0))
duz_duvar(y, V(X1, Y1), V(X0, Y1), ZS, ZK, 'tas')
# bollards and mooring rings along the quay
for k in range(12):
    xx = SH1 + 0.06 + (X1 - SH1 - 0.12) * k / 11
    y.prizma((xx, QY + 0.015), 0.006, ZK, ZK + 0.016, 'kirec', n=8)
for k in range(3):
    xx = X0 + 0.07 + 0.1 * k
    y.prizma((xx, QY + 0.015), 0.006, ZK, ZK + 0.016, 'kirec', n=8)

y.bolum('Mendirekler, Kolossos')
mendirek([(-0.86, QY + 0.02), (-0.86, -0.8), (-0.22, -0.86)], 0.1, son_kes=0.2)
mendirek([(0.2, -0.86), (0.96, -0.76), (0.96, QY + 0.02)], 0.1, bas_kes=0.16)
# the Colossus on its marble base at the west mole's head, guarding the harbour mouth
CX, CY = -0.31, -0.82
kutu_merkez(y, (CX, CY), 0.27, 0.27, ZK + 0.016, 'kirec', z0=0.0)
zc = ZK + 0.016
kutu_merkez(y, (CX, CY), 0.23, 0.23, 0.02, 'mermer', z0=zc)
silme(y, dikdortgen(CX - 0.115, CX + 0.115, CY - 0.115, CY + 0.115), zc, 0.014, 0.006, 'mermer', 'kaide')
oc = cokgen((CX, CY), 0.1, 8, math.pi / 8)
zc2 = zc + 0.02
for i in range(8):
    a, b = oc[i], oc[(i + 1) % 8]
    duz_duvar(y, a, b, zc2, zc2 + 0.12, 'mermer')
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    if i % 2 == 0:
        kalkan(a.lerp(b, 0.5) + Z * (zc2 + 0.062), e, nn, 0.022, 'bronz')
halka_kornis(y, (CX, CY), 0.1, zc2, 0.014, 0.009, 8, 'mermer', kat=math.pi / 8, profil='kaide')
halka_kornis(y, (CX, CY), 0.1, zc2 + 0.104, 0.016, 0.013, 8, 'mermer', kat=math.pi / 8, profil='tac')
y.yuz_yon([V(p.x, p.y, zc2 + 0.12) for p in cokgen((CX, CY), 0.113, 8, math.pi / 8)], 'mermer', Z)
kolossos(CX, CY, zc2 + 0.12, 0.88)
sancak(y, CX + 0.115, CY - 0.115, zc, boy=0.2, en=0.1, yuk=0.065, aci=-math.pi * 0.7)

y.bolum('Deniz feneri')
kule_fener(0.275, -0.8, ZK)

y.bolum('Gemi hangarları (neosoikoi)')
NSH = 5
WS = (SH1 - SH0) / NSH
for k in range(NSH):
    x0 = SH0 + WS * k
    x1 = x0 + WS
    # the slipway: a stone ramp from the back wall down into the water
    y.yuz_yon([V(x0, 0.16, ZS - 0.006), V(x1, 0.16, ZS - 0.006), V(x1, 0.62, ZK), V(x0, 0.62, ZK)], 'zemin', V(0, -0.2, 1))
# the dividing walls / pier rows and the roofs
for k in range(NSH + 1):
    xx = SH0 + WS * k
    for j in range(5):
        yy = 0.27 + 0.085 * j
        y.prizma((xx, yy), 0.009, ZS - 0.01, ZK + 0.1, 'kirec', n=8)
        kutu_merkez(y, (xx, yy), 0.024, 0.024, 0.008, 'tas_acik', z0=ZK + 0.1)
    kutu_merkez(y, (xx, 0.44), 0.012, 0.4, 0.012, 'kirec', z0=ZK + 0.108)
for k in range(NSH):
    x0 = SH0 + WS * k
    cati_besik(y, x0 + 0.002, x0 + WS - 0.002, 0.23, 0.64, ZK + 0.12, 0.045, 0.014, 'kiremit', mahya='kiremit2', ucluk_key='kirec',
               alinlik_key='tas_acik', alt_key='ahsap_koyu', kalinlik=0.006, ns=4, nr=3, dilim=['kiremit', 'kiremit2'])
    iki_yuzlu(y, [V(x0, 0.23, ZK + 0.1195), V(x0 + WS, 0.23, ZK + 0.1195), V(x0 + WS, 0.64, ZK + 0.1195), V(x0, 0.64, ZK + 0.1195)], 'ahsap_koyu', -Z)   # (seen from above in the roof valleys too)
# ships drawn up in two of the sheds
for k in (1, 3):
    xc = SH0 + WS * (k + 0.5)
    gemi(xc, 0.4, math.pi / 2 * -1, L=0.28, B=0.05, kurek=False, yelken=False, tohum=k, dz=0.032)

y.bolum('Ticaret stoası ve Helios tapınağı')
SX0, SX1, SY0, SY1 = 0.02, 0.86, 0.3, 0.46
kutu(y, V(SX0 - 0.01, SY0 - 0.01, ZK), X, SX1 - SX0 + 0.02, SY1 - SY0 + 0.02, 0.01, 'kirec', 'onarkasagsolust')
zb = ZK + 0.01
SHH = 0.12
duz_duvar(y, V(SX1, SY1 + 0.004), V(SX0, SY1 + 0.004), zb, zb + SHH, 'kirec')
for xx, sx in ((SX0, -1), (SX1, 1)):
    kutu(y, V(xx - (0.012 if sx > 0 else 0), SY1 + 0.004, zb), -Y, SY1 + 0.004 - SY0 - 0.02, 0.012, SHH, 'kirec', 'onarkasagsol')   # the end walls (thick: seen from inside through the colonnade)
for k in range(6):   # shop doors on the inner back wall
    xd = SX0 + 0.07 + (SX1 - SX0 - 0.14) * k / 5
    dikdortgen_acik(y, V(xd - 0.03, SY1), V(xd + 0.03, SY1), zb, SHH, 0.25, 0.75, 0.0, SHH * 0.6, ('kirec', 'tas_acik', 'tas_acik', 'koyu'),
                    derin=0.003)
XD = [SX0 + 0.07 + (SX1 - SX0 - 0.14) * k / 5 for k in range(6)]
for xa_, xb_ in zip([SX0] + [x + 0.03 for x in XD], [x - 0.03 for x in XD] + [SX1]):
    duz_duvar(y, V(xa_, SY1), V(xb_, SY1), zb, zb + SHH, 'kirec')
for k in range(15):
    kolon(SX0 + 0.012 + (SX1 - SX0 - 0.024) * k / 14, SY0 + 0.01, zb, zb + SHH, 0.009, 'dor', 'kirec', yiv=8)
kutu(y, V(SX0 - 0.004, SY0 - 0.004, zb + SHH), X, SX1 - SX0 + 0.008, SY1 - SY0 + 0.008, 0.014, 'kirec', 'onarkasagsolust')
y.yuz_yon([V(SX0, SY0 - 0.004, zb + SHH), V(SX1, SY0 - 0.004, zb + SHH), V(SX1, SY1, zb + SHH), V(SX0, SY1, zb + SHH)], 'tas_koyu', -Z)
triglif_dizi(V(SX0 - 0.004, SY0 - 0.0045), V(SX1 + 0.004, SY0 - 0.0045), zb + SHH + 0.004, 0.009, 28, w=0.006, metop='boya_kirmizi', rolyef=False)
cati_besik(y, SX0 - 0.004, SX1 + 0.004, SY0 - 0.004, SY1 + 0.004, zb + SHH + 0.014, 0.05, 0.016, 'kiremit', mahya='kiremit2', ucluk_key='kirec',
           alinlik_key='tas_acik', alt_key='kirec', kalinlik=0.007, ns=14, nr=3, dilim=['kiremit', 'kiremit2'])
# goods on the quay: amphorae, bales, a crane
for k in range(14):
    x = 0.08 + 0.05 * (k % 7) + (0.01 if k > 6 else 0)
    amfora(x, 0.28 if k < 7 else 0.265, ZK, 1.1, 'siva_oker' if k % 3 else 'kirmizi')
for k, xx in enumerate((0.5, 0.56, 0.62)):
    kutu_merkez(y, (xx, 0.275), 0.04, 0.03, 0.025, 'kumas' if k % 2 else 'saz', z0=ZK, aci=0.2 * k)
TP = V(0.75, 0.24, ZK + 0.22)
for a in (math.radians(60), math.radians(120)):
    cubuk(y, V(0.75 + 0.05 * math.cos(a), 0.3 + 0.03 * math.sin(a), ZK), TP, 0.008, 'ahsap')
cubuk(y, TP, TP + V(0, -0.0, -0.13), 0.002, 'ahsap_koyu')
kutu_merkez(y, (0.75, 0.24), 0.03, 0.03, 0.03, 'saz', z0=ZK + 0.06)
y.yuz_yon([V(0.735, 0.225, ZK + 0.06), V(0.765, 0.225, ZK + 0.06), V(0.765, 0.255, ZK + 0.06), V(0.735, 0.255, ZK + 0.06)], 'saz', -Z)

# the Temple of Helios on the upper town
with parca(y, (0.5, 0.76, 0), -math.pi / 2):
    dor_tapinak(0.46, 0.2, 11, 6, ZK, 0.17, 0.011, key='kirec', cati='kiremit', kaburga='kiremit2', sb=0.012, heykel=False)

y.bolum('Kent surları ve evler')
SY_ = 0.99
for a, b in (((X1 - 0.04, QY + 0.06), (X1 - 0.04, SY_)), ((X1 - 0.04, SY_), (X0 + 0.04, SY_)), ((X0 + 0.04, SY_), (X0 + 0.04, QY + 0.06))):
    sur(y, [V(*a), V(*b)], ZK, 0.1, 0.04, 'kirec', mazgal_h=0.025, parapet_h=0.012)
for (tx, ty) in ((X1 - 0.06, SY_ - 0.02), (X0 + 0.06, SY_ - 0.02), (0.0, SY_ - 0.02), (-0.55, SY_ - 0.02), (X1 - 0.06, 0.55), (X0 + 0.06, 0.55)):
    kule_kare(y, tx, ty, 0.1, ZK, 0.17, 'kirec', 'piramit', 'kiremit', cati_h=0.06, mazgal_h=0.0, kose_tas='tas_acik', cati_ns=4, cati_nr=3)
sancak(y, X0 + 0.06, SY_ - 0.02, ZK + 0.25, boy=0.2, en=0.1, yuk=0.065, aci=-math.pi * 0.25)
# houses of the town: whitewashed blocks with tiled hip roofs and small courtyards
g = random.Random(12)
for k, (hx, hy) in enumerate(((-1.0, 0.75), (-0.86, 0.86), (-0.72, 0.74), (-0.58, 0.86), (-0.44, 0.74), (-0.3, 0.86), (-0.16, 0.74), (-0.98, 0.42),
                              (0.94, 0.62), (0.02, 0.82))):
    w, d = g.uniform(0.09, 0.12), g.uniform(0.08, 0.1)
    hh = g.uniform(0.05, 0.08)
    kutu_merkez(y, (hx, hy), w, d, hh, 'siva' if k % 3 else 'siva_krem', z0=ZK)
    for sx in (-1, 1):
        kutu_merkez(y, (hx + sx * w * 0.25, hy - d / 2 - 0.0005), 0.012, 0.002, 0.016, 'koyu', z0=ZK + hh * 0.55)
    kutu_merkez(y, (hx, hy - d / 2 - 0.0005), 0.016, 0.002, 0.03, 'ahsap', z0=ZK)
    cati_kirma(y, hx - w / 2, hx + w / 2, hy - d / 2, hy + d / 2, ZK + hh, 0.03, 0.01, 'kiremit', mahya='kiremit2', kalinlik=0.004, ns=4, nr=2)
for x, yy in ((-0.08, 0.66), (0.14, 0.56), (0.86, 0.72)):
    agac(y, x, yy, ZK, 0.12, 'servi')

y.bolum('Gemiler')
gemi(0.0, -0.3, math.pi / 2 * -1 + 0.25, tohum=7)
gemi(0.45, 0.12, 0.0, L=0.26, B=0.075, H=0.03, kurek=False, tur='holkas', tohum=8)
gemi(-0.5, -0.45, math.pi * 0.62, L=0.22, B=0.05, H=0.026, kurek=True, yelken=False, tohum=9)
gemi(0.62, -0.98, 0.15, L=0.24, B=0.07, H=0.028, kurek=False, tur='holkas', tohum=10)

calistir(y, 'lm_rodos')
