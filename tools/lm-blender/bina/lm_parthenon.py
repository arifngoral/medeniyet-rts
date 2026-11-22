# Parthenon on the Athenian Acropolis (lm_parthenon): the Doric peripteros of 8 x 17 columns on its three-stepped
# crepidoma, hexastyle prostyle porches before the cella, the triglyph frieze with 92 sculpted metopes, the Ionic
# Panathenaic frieze round the cella, both pediments with their figure groups, a marble-tiled roof with antefixes and
# acroteria; on the rock plateau (faceted cliffs, Kimon's wall) with the stair, the Propylaia, the Athena Nike temple
# on its bastion, the bronze Athena Promachos, the Erechtheion with its caryatid porch, the great altar and olives.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
RNG = random.Random(7)
TRI = 'lacivert'                  # painted triglyphs (blue-black)
ZK = 0.22                         # top of the rock cliffs
ZT = 0.36                         # the plateau (top of Kimon's wall)


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


# ================================================================ the temple
def parthenon(L, W, nl, nw, z0, HC, r, key='mermer'):
    """the Parthenon at the origin, long axis y, the west front (Propylaia side) facing -y: crepidoma, 8 x 17 Doric
    peristyle, the cella with prostyle hexastyle porches and the Ionic frieze, the triglyph frieze with sculpted
    metopes, both pediments with figures, a marble roof with cover tiles, antefixes and acroteria. Returns the top z"""
    sx_, sy_ = W / (nw - 1), L / (nl - 1)
    sb = 0.017
    m = r * 2.4
    for k in range(3):                                      # crepidoma
        d = m + 0.022 * (2 - k)
        x0, x1, y0, y1 = -W / 2 - d, W / 2 + d, -L / 2 - d, L / 2 + d
        kutu(y, V(x0, y0, z0 + sb * k), X, x1 - x0, y1 - y0, sb, key, 'onarkasagsol')
        y.yuz([V(x0, y0, z0 + sb * (k + 1)), V(x1, y0, z0 + sb * (k + 1)), V(x1, y1, z0 + sb * (k + 1)), V(x0, y1, z0 + sb * (k + 1))], key)
        # the riser's shadow line (a thin set-back band at the foot of each step)
        silme(y, dikdortgen(x0, x1, y0, y1), z0 + sb * k, 0.003, 0.0015, 'tas_acik', 'duz')
    # a ramp up the middle of the east front (as on the real one) and the west
    for sg in (1,):
        yb = sg * (L / 2 + m + 0.044)
        y.yuz_yon([V(-0.07, yb + sg * 0.05, z0), V(0.07, yb + sg * 0.05, z0), V(0.07, yb, z0 + sb * 3), V(-0.07, yb, z0 + sb * 3)], key, V(0, sg * 0.4, 1))
        for sx in (-1, 1):
            y.yuz_yon([V(sx * 0.07, yb + sg * 0.05, z0), V(sx * 0.07, yb, z0), V(sx * 0.07, yb, z0 + sb * 3)], key, V(sx, 0))
    zs = z0 + sb * 3
    zc = zs + HC
    pts = [V(-W / 2 + sx_ * i, -L / 2) for i in range(nw - 1)] + [V(W / 2, -L / 2 + sy_ * j) for j in range(nl - 1)] + \
          [V(W / 2 - sx_ * i, L / 2) for i in range(nw - 1)] + [V(-W / 2, L / 2 - sy_ * j) for j in range(nl - 1)]
    for p in pts:
        kolon(p.x, p.y, zs, zc, r, 'dor', key)
    he = HC * 0.27
    ha, hf = he * 0.4, he * 0.38

    # ---- the cella: long walls with antae, door walls, prostyle porches of six columns, the Ionic frieze
    cx = W / 2 - sx_ * 1.05
    ya = L / 2 - sy_ * 1.25                                   # antae ends
    yd = L / 2 - sy_ * 1.9                                    # door walls
    yp = L / 2 - sy_ * 0.95                                   # porch columns
    t = 0.022
    for s in (-1, 1):
        a, b = (V(s * cx, -ya), V(s * cx, ya)) if s > 0 else (V(s * cx, ya), V(s * cx, -ya))
        duz_duvar(y, a, b, zs, zc, key)
        # the anta ends and their inner faces up to the door walls
        for yy in (-ya, ya):
            sg = 1 if yy > 0 else -1
            y.yuz_yon([V(s * cx, yy, zs), V(s * (cx - t), yy, zs), V(s * (cx - t), yy, zc), V(s * cx, yy, zc)], key, V(0, sg))
            y.yuz_yon([V(s * (cx - t), yy, zs), V(s * (cx - t), sg * yd, zs), V(s * (cx - t), sg * yd, zc + ha), V(s * (cx - t), yy, zc + ha)], key, V(-s, 0))
            kutu_merkez(y, (s * (cx - t / 2), yy - sg * 0.004), t * 1.5, 0.014, 0.014, key, z0=zc - 0.014)    # anta capital
        silme(y, [V(s * cx, -ya if s > 0 else ya), V(s * cx, ya if s > 0 else -ya)], zs, 0.012, 0.004, key, 'kaide', kapali=False)
    for sg in (-1, 1):
        # door wall, its door (west: closed bronze; east: open, the gold-and-ivory Athena glinting inside)
        a, b = (V(-cx + t, sg * yd), V(cx - t, sg * yd)) if sg < 0 else (V(cx - t, sg * yd), V(-cx + t, sg * yd))
        Wd, e_, nc_, Ld = dikdortgen_acik(y, a, b, zs, zc - zs, 0.36, 0.64, 0.0, (zc - zs) * 0.74,
                                          (key, 'tas_acik', 'tas_acik', 'bronz' if sg < 0 else 'koyu'), derin=0.014, cerceve=(0.008, 'tas_acik'))
        if sg < 0:
            y.yuz_yon([Ld(0.498, 0, 0.0135), Ld(0.502, 0, 0.0135), Ld(0.502, (zc - zs) * 0.74, 0.0135), Ld(0.498, (zc - zs) * 0.74, 0.0135)], 'koyu', nc_)
            for i in range(4):
                for j in range(5):
                    kure(y, Ld(0.39 + 0.073 * i + (0.02 if i > 1 else 0), (zc - zs) * (0.08 + 0.14 * j), 0.013), 0.0022, 'altin', n=5, kat=3)
        else:
            # Athena Parthenos far inside: a gilded figure in the dark doorway
            pc = Ld(0.5, 0, 0.012)
            donel(y, (pc.x, pc.y + 0.0), [(0.0, zs), (0.02, zs), (0.016, zs + 0.06), (0.012, zs + 0.1), (0.0, zs + 0.12)], 'altin', n=8)
        # frieze band above the door wall
        duz_duvar(y, a, b, zc, zc + ha, TRI)
        # the porch: six columns, a frieze beam on them
        for i in range(6):
            xx = -cx + t * 0.6 + (2 * cx - t * 1.2) * i / 5
            kolon(xx, sg * yp, zs + 0.006, zc, r * 0.88, 'dor', key)
        kutu_merkez(y, (0, sg * yp), 2 * cx + 0.004, r * 2.4, ha, TRI, z0=zc)
        y.yuz_yon([V(-cx - 0.002, sg * yp - r * 1.2, zc), V(cx + 0.002, sg * yp - r * 1.2, zc), V(cx + 0.002, sg * yp + r * 1.2, zc),
                   V(-cx - 0.002, sg * yp + r * 1.2, zc)], key, -Z)
        kutu_merkez(y, (0, sg * yp), 2 * cx + 0.06, r * 3.2, 0.006, key, z0=zs)        # porch stylobate step
        # the procession on the beam's outer face
        for k in range(26):
            xx = -cx + (2 * cx) * (k + 0.5) / 26
            hh = ha * (0.72 if k % 3 else 0.82)
            kutu_merkez(y, (xx, sg * (yp + r * 1.2 + 0.0012)), 0.006, 0.0024, hh, key, z0=zc + ha * 0.1)
    # Ionic frieze on the long cella walls: blue band with the Panathenaic procession in relief (riders, walkers)
    for s in (-1, 1):
        a, b = (V(s * cx, -ya), V(s * cx, ya)) if s > 0 else (V(s * cx, ya), V(s * cx, -ya))
        duz_duvar(y, a, b, zc, zc + ha, TRI)
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        n = int((2 * ya) / 0.016)
        for k in range(n):
            p = a.lerp(b, (k + 0.5) / n) + nn * 0.0012
            if k % 4 == 1:     # a rider: a horse body and a figure on it
                kutu(y, p + nn * 0.0024 - e * 0.006 + Z * (zc + ha * 0.32), e, 0.014, 0.0024, ha * 0.28, key, 'onsagsolust')
                kutu(y, p + nn * 0.0024 + Z * (zc + ha * 0.1), e, 0.003, 0.0024, ha * 0.22, key, 'onsagsolust')
                kutu(y, p + nn * 0.0024 + Z * (zc + ha * 0.6), e, 0.004, 0.0024, ha * 0.3, key, 'onsagsolust')
            else:
                kutu(y, p + nn * 0.0024 - e * 0.002 + Z * (zc + ha * 0.1), e, 0.0045, 0.0024, ha * (0.78 if k % 2 else 0.72), key, 'onsagsolust')
    # the pteron ceiling
    y.yuz_yon([V(-W / 2, -L / 2, zc + ha), V(W / 2, -L / 2, zc + ha), V(W / 2, L / 2, zc + ha), V(-W / 2, L / 2, zc + ha)], 'tas_koyu', -Z)

    # ---- the outer entablature: architrave with taenia and guttae, triglyphs and metopes, the cornice
    D = r * 2.6
    k4 = dikdortgen(-W / 2, W / 2, -L / 2, L / 2)
    o = disa(k4, D / 2); ii = disa(k4, -D / 2)
    duvarlar(y, o, zc, zc + ha, key)
    silme(y, o, zc + ha - he * 0.05, he * 0.05, 0.003, key, 'duz')
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * zc, o[j] + Z * zc, ii[j] + Z * zc, ii[i] + Z * zc], key, -Z)
        duz_duvar(y, ii[j], ii[i], zc, zc + ha, key)
    # the shields of Alexander (gilded discs on the architrave, east and west fronts)
    for i in (0, 2):
        p, q = o[i], o[(i + 1) % 4]
        e = (q - p).normalized(); nn = V(e.y, -e.x)
        for k in range(nw - 1):
            c = p.lerp(q, (k + 0.5) / (nw - 1)) + Z * (zc + ha * 0.42)
            y.yuz_yon([c + nn * 0.0012 + e * (0.0085 * math.cos(TAU * a / 10)) + Z * (0.0085 * math.sin(TAU * a / 10)) for a in range(10)], 'altin', nn)
    f = disa(k4, D / 2 - 0.003)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * (zc + ha), o[j] + Z * (zc + ha), f[j] + Z * (zc + ha), f[i] + Z * (zc + ha)], key, Z)
    duvarlar(y, f, zc + ha, zc + ha + hf, key)
    for i in range(4):
        p, q = f[i], f[(i + 1) % 4]
        n = (nw - 1) * 2 if i % 2 == 0 else (nl - 1) * 2
        triglif_dizi(p, q, zc + ha, hf, n, metop='boya_kirmizi' if i % 2 == 0 else 'lacivert')
    zk = zc + ha + hf
    silme(y, f, zk, he * 0.22, he * 0.32, key, 'tac')
    ze = zk + he * 0.22
    y.yuz_yon([V(p.x, p.y, ze) for p in f], key, Z)          # (closes the cornice top under the roof)

    # ---- pediments and the roof
    g = disa(k4, D / 2 + he * 0.32)
    xa, xb, ya_, yb = g[0].x, g[1].x, g[0].y, g[2].y
    ph = (xb - xa) * 0.13
    alinlik(y, V(xa, ya_), V(xb, ya_), ze, ph, derin=yb - ya_ - 0.003, key=key, ic_key='lacivert', c=0.011, cati_key='mermer')
    alinlik(y, V(xb, yb), V(xa, yb), ze, ph, derin=0.003, key=key, ic_key='lacivert', c=0.011, cati_key='mermer')
    kiremit_serit(xa, xb, ya_ + 0.01, yb - 0.01, ze + 0.0088, ph, adim=0.024)
    cubuk(y, V(0, ya_, ze + ph + 0.012), V(0, yb, ze + ph + 0.012), 0.012, 'mermer')
    sp = 0.011 * 1.6                                         # (alinlik's frame width)
    zt0 = ze + sp
    HT = ph - 2.9 * sp
    hw = (xb - xa) / 2

    def H(x):   # the height free under the raking cornice at x
        return max(0.004, HT * (1 - abs(x) / (hw * 0.93)) * 0.9)
    for yy, sg in ((ya_, -1), (yb, 1)):
        yt = yy - sg * 0.0005
        # the pediment groups. West: Athena and Poseidon with the olive between them, their chariots rearing away;
        # east: the birth of Athena (Zeus enthroned, Athena striding out), Helios' horses rising, Selene's sinking.
        if sg < 0:
            for x_, a_ in ((-0.035, math.pi * 0.85), (0.035, 0.15)):
                figur(x_, yt, zt0, H(x_) / 0.097, 'mermer', aci=a_)
            boru(y, [V(0, yt, zt0), V(0, yt, zt0 + H(0) * 0.6)], 0.0025, 'ahsap', n=5)
            kure(y, (0, yt, zt0 + H(0) * 0.7), H(0) * 0.16, 'zeytin', n=8, kat=4)
            for s in (-1, 1):
                for f_ in (0.16, 0.24):
                    at(s * hw * f_, yt + sg * 0.002 * (f_ > 0.2), zt0, aci=0 if s > 0 else math.pi, s=H(hw * (f_ + 0.03)) / 0.118)
                figur(s * hw * 0.42, yt, zt0, H(hw * 0.44) / 0.097, 'mermer', aci=(0 if s > 0 else math.pi) + 0.6, kol=0.8)
                figur(s * hw * 0.55, yt, zt0, H(hw * 0.57) / 0.09, 'mermer', kol=0)
                figur(s * hw * 0.66, yt, zt0, H(hw * 0.68) / 0.09, 'mermer', kol=0)
                uzanan(s * hw * 0.88, yt, zt0, -s, 0.55)
        else:
            # Zeus seated on his throne
            h0 = H(0)
            kutu_merkez(y, (0.0, yt), h0 * 0.36, 0.008, h0 * 0.3, 'mermer', z0=zt0)
            figur(0.0, yt, zt0 + h0 * 0.22, h0 * 0.7 / 0.097, 'mermer', kol=0.9)
            figur(0.04, yt, zt0, H(0.045) / 0.097, 'mermer', aci=0.2)
            figur(-0.04, yt, zt0, H(0.045) / 0.097, 'mermer', aci=math.pi, kol=0.7)
            for s in (-1, 1):
                for f_ in (0.2, 0.32, 0.44, 0.56):
                    figur(s * hw * f_, yt, zt0, H(hw * (f_ + 0.02)) / 0.097, 'mermer', kol=0.6 if f_ < 0.4 else 0)
                uzanan(s * hw * 0.72, yt, zt0, -s, 0.6)
                # horses' heads rising (Helios) / sinking (Selene) out of the corners
                for k in range(2):
                    xx = s * hw * (0.84 + 0.05 * k)
                    boru(y, [V(xx, yt, zt0), V(xx - s * 0.006, yt, zt0 + 0.007), V(xx - s * 0.011, yt, zt0 + 0.009)],
                         0.003, 'mermer', n=6, r_son=0.002)
        # acroteria: a floral one on the apex, Nikai on the corners; lion-head spouts
        zap = ze + ph + 0.012
        donel(y, (0, yy), [(0.0, zap), (0.013, zap + 0.004), (0.02, zap + 0.02), (0.014, zap + 0.034), (0.008, zap + 0.04), (0, zap + 0.046)],
              'altin', n=8)
        for s in (-1, 1):
            boru(y, [V(-0.024 * s * 0.0 + s * 0.012, yy, zap + 0.006), V(s * 0.03, yy, zap + 0.024)], 0.0035, 'altin', n=5, r_son=0.002)
        for xx in (xa + 0.014, xb - 0.014):
            kutu_merkez(y, (xx, yy - sg * 0.004), 0.02, 0.02, 0.008, key, z0=ze + 0.006)
            figur(xx, yy - sg * 0.004, ze + 0.014, 0.42, 'altin', aci=math.pi / 2 * (1 if xx > 0 else -1) + (0 if sg > 0 else math.pi), kol=0.9)
    # antefixes along both eaves: small painted palmettes standing on the gutter edge
    nA = int((yb - ya_) / 0.024)
    for sx in (-1, 1):
        xe = xb if sx > 0 else xa
        for j in range(nA + 1):
            yy = ya_ + 0.012 + (yb - ya_ - 0.024) * j / nA
            zb_ = ze + 0.009
            pa = [V(xe + sx * 0.0005, yy - 0.0045, zb_), V(xe + sx * 0.0005, yy + 0.0045, zb_), V(xe + sx * 0.0005, yy + 0.0035, zb_ + 0.008),
                  V(xe + sx * 0.0005, yy, zb_ + 0.012), V(xe + sx * 0.0005, yy - 0.0035, zb_ + 0.008)]
            y.yuz_yon(pa, 'boya_kirmizi' if j % 2 else 'mermer', V(sx, 0))
            pb = [p - V(sx * 0.002, 0) for p in pa]
            y.yuz_yon(pb, 'mermer', V(-sx, 0))
            for k in range(5):
                q0, q1 = pa[k], pa[(k + 1) % 5]
                mid = (q0 + q1) / 2
                yuz_dis(y, [q0, q1, pb[(k + 1) % 5], pb[k]], 'mermer', V(xe, yy, zb_ + 0.005) - V(sx * 0.001, 0))
        # lion-head spouts at the corners
        for yy in (ya_ + 0.004, yb - 0.004):
            boru(y, [V(xe, yy, ze + 0.005), V(xe + sx * 0.012, yy, ze + 0.004)], 0.0035, 'mermer', n=6)
    return ze + ph + 0.06, zs


# ================================================================ the rock and Kimon's wall
y.bolum('Akropolis kayası')
KOSE = [V(*p) for p in ((-1.08, -0.62), (-0.92, -0.8), (-0.34, -0.8), (0.36, -0.79), (0.92, -0.72), (1.1, -0.48), (1.13, 0.16),
                        (1.04, 0.66), (0.66, 0.88), (-0.02, 0.93), (-0.72, 0.9), (-1.04, 0.68), (-1.13, 0.06))]
NK = len(KOSE)
MRK = V(0.0, 0.05)


def rock_ring(off, zz, tohum, zj=0.012):
    """a ring of points round the plateau outline pushed out by off x a per-point factor shared by all rings (so
    the rings never cross and the cliff never folds over), slid along the edge by a shared amount plus a little
    of its own, at height zz (+- zj)"""
    g = random.Random(tohum)
    pts = []
    for (i, k, m, kay, fak) in TABAN:
        a, b = KOSE[i], KOSE[(i + 1) % NK]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        u = k / m + ((kay + g.uniform(-0.08, 0.08)) / m if k else 0)
        p = a.lerp(b, u)
        nrm = (DK[i] - KOSE[i]) if k == 0 else nn
        pts.append(V(p.x, p.y) + nrm * (off * fak) + Z * (zz + (g.uniform(-zj, zj) if 0 < zz < ZK else 0)))
    return pts


DK = disa(KOSE, 1.0)
_g = random.Random(4)
TABAN = []
for i in range(NK):
    m = max(2, int(math.ceil((KOSE[(i + 1) % NK] - KOSE[i]).length / 0.12)))
    for k in range(m):
        TABAN.append((i, k, m, _g.uniform(-0.25, 0.25), _g.uniform(0.7, 1.3)))


# rows: the foot (out), jagged strata (each a steep face and a narrow ledge), the top edge at the wall foot
SIRA = [rock_ring(0.1, 0.0, 1), rock_ring(0.084, 0.05, 2, 0.008), rock_ring(0.074, 0.058, 3, 0.004),
        rock_ring(0.046, 0.12, 4, 0.01), rock_ring(0.037, 0.128, 5, 0.004), rock_ring(0.012, 0.19, 6, 0.008), rock_ring(0.0, ZK, 7)]
g = random.Random(9)
for r in range(len(SIRA) - 1):
    A, B = SIRA[r], SIRA[r + 1]
    n = len(A)
    ledge = r in (1, 3)
    for i in range(n):
        j = (i + 1) % n
        q = [A[i], A[j], B[j], B[i]]
        out = (A[i] + A[j]) / 2 - MRK; out.z = 0; out = out.normalized() + Z * (1.5 if ledge else 0.25)
        dark = g.random() < (0.55 if r == 0 else 0.3)
        k1 = 'toprak' if (ledge and g.random() < 0.5) else ('kaya_koyu' if dark else 'kaya')
        k2 = k1 if g.random() < 0.7 else ('kaya' if k1 == 'kaya_koyu' else 'kaya_koyu')
        if ledge: k2 = k1
        if g.random() < 0.5:
            y.yuz_yon([q[0], q[1], q[2]], k1, out); y.yuz_yon([q[0], q[2], q[3]], k2, out)
        else:
            y.yuz_yon([q[0], q[1], q[3]], k1, out); y.yuz_yon([q[1], q[2], q[3]], k2, out)
R0, R1, R2 = SIRA[0], SIRA[2], SIRA[4]
# scrub on the ledges and boulders at the foot
for i in range(0, len(R1), 3):
    p = R1[i].lerp(R2[i], 0.3)
    kure(y, (p.x, p.y, p.z + 0.006), g.uniform(0.014, 0.022), 'zeytin' if i % 2 else 'boya_yesil', n=7, kat=4)
for i in range(1, len(R0), 4):
    p = R0[i]
    r = g.uniform(0.014, 0.026)
    donel(y, (p.x + (p.x - MRK.x) * 0.03, p.y + (p.y - MRK.y) * 0.03), [(r, 0), (r * 1.1, r * 0.5), (r * 0.6, r), (0, r * 1.15)], 'kaya', n=6, kat=g.random())

y.bolum('Kimon suru')
GAP = (-0.73, -0.47)          # the stair arrives here
ic = disa(KOSE, -0.04)
for i in range(NK):
    j = (i + 1) % NK
    a, b = KOSE[i], KOSE[j]
    segs = [(a, b)]
    if i == 1:                # the front edge with the stair gap
        segs = [(a, V(GAP[0], a.y)), (V(GAP[1], a.y), b)]
    for p, q in segs:
        duz_duvar(y, p, q, ZK, ZT, 'kirec')
        # coursing: a drafted band every few courses and the moulded coping
        silme(y, [p, q], ZK, 0.012, 0.008, 'kirec', 'kaide', kapali=False)
        silme(y, [p, q], ZK + (ZT - ZK) * 0.52, 0.005, 0.003, 'tas_koyu', 'duz', kapali=False)
        silme(y, [p, q], ZT - 0.008, 0.008, 0.006, 'tas_acik', 'tac', kapali=False)
    # the low parapet on the wall top
    pa, pb, qa, qb = KOSE[i], KOSE[j], ic[i], ic[j]
    if i == 1:
        continue
    duz_duvar(y, pa, pb, ZT, ZT + 0.022, 'kirec')
    duz_duvar(y, qb, qa, ZT, ZT + 0.022, 'kirec')
    y.yuz_yon([pa + Z * (ZT + 0.022), pb + Z * (ZT + 0.022), qb + Z * (ZT + 0.022), qa + Z * (ZT + 0.022)], 'tas_acik', Z)
# the front parapet in two pieces round the gap
for p, q in ((KOSE[1], V(GAP[0], KOSE[1].y)), (V(GAP[1], KOSE[1].y), KOSE[2])):
    kutu(y, p + Z * ZT, q - p, (q - p).length, 0.04, 0.022, 'kirec', 'onarkasagsolust')

y.bolum('Düzlük')
# the plateau top in rings (so the baked shadow has vertices), a paved sacred way
rings = [[MRK.lerp(V(p.x, p.y), f) + Z * ZT for p in ic] for f in (0.0, 0.35, 0.7, 1.0)]
for k in range(3):
    A, B = rings[k], rings[k + 1]
    for i in range(NK):
        jj = (i + 1) % NK
        q = [A[i], A[jj], B[jj], B[i]]
        if k == 0:
            y.yuz_yon([A[0], B[i], B[jj]], 'toprak', Z)
        else:
            y.yuz_yon(q, 'toprak', Z)
# the wall gap's floor (the stair landing)
y.yuz_yon([V(GAP[0], KOSE[1].y, ZT), V(GAP[1], KOSE[1].y, ZT), V(GAP[1], KOSE[1].y + 0.04, ZT), V(GAP[0], KOSE[1].y + 0.04, ZT)], 'zemin', Z)


def yol(p, q, en, key='zemin'):
    p, q = V(p[0], p[1]), V(q[0], q[1])
    e = (q - p).normalized(); s = V(-e.y, e.x) * (en / 2)
    zz = ZT + 0.003
    y.yuz_yon([p - s + Z * zz, q - s + Z * zz, q + s + Z * zz, p + s + Z * zz], key, Z)
    for a, b in ((p - s, q - s), (q + s, p + s)):
        duz_duvar(y, a + Z * ZT, b + Z * ZT, ZT, zz, 'kirec')


yol((-0.72, -0.455), (0.9, -0.455), 0.07)

# ================================================================ the stair and the Propylaia
y.bolum('Merdiven')
merdiven(y, (-0.6, -1.2), math.pi / 2, 0.26, 0.0, ZT, n=18, d=0.4 / 18, key='mermer', yanlik='kirec')
for sx in (-1, 1):   # pedestals at the stair foot with bronze horsemen (the Agrippa monument style)
    x = -0.6 + sx * 0.17
    kutu_merkez(y, (x, -1.12), 0.06, 0.08, 0.1, 'kirec', z0=0)
    kornis(y, x - 0.03, x + 0.03, -1.16, -1.08, 0.09, 0.01, 0.006, 'tas_acik', 'tac')
    at(x, -1.12, 0.102, aci=-math.pi / 2, s=0.55, key='bronz')
    figur(x, -1.12 + 0.002, 0.135, 0.35, 'bronz', kol=0)

y.bolum('Propylaia')
PX, PY0, PY1 = -0.6, -0.78, -0.5
PW = 0.32
zp = ZT
kutu(y, V(PX - PW / 2 - 0.02, PY0 - 0.012, zp), X, PW + 0.04, PY1 - PY0 + 0.024, 0.012, 'mermer', 'onarkasagsolust')
zp += 0.012
PH = 0.17
for yy, sg in ((PY0, -1), (PY1, 1)):
    for i in range(6):
        xx = PX - PW / 2 + PW * i / 5
        kolon(xx, yy, zp, zp + PH, 0.0125, 'dor', 'mermer', yiv=10)
# the gate wall with five doorways between the porticoes
gw = V(PX - PW / 2, (PY0 + PY1) / 2 + 0.03)
for k in range(5):
    a = V(PX + PW / 2 - PW * k / 5, gw.y); b = V(PX + PW / 2 - PW * (k + 1) / 5, gw.y)
    hh = 0.6 if k == 2 else (0.5 if k in (1, 3) else 0.42)
    dikdortgen_acik(y, b, a, zp, PH, 0.28, 0.72, 0.0, PH * hh, ('mermer', 'tas_acik', 'tas_acik', 'koyu'), derin=0.006)
    dikdortgen_acik(y, a + V(0, 0.012), b + V(0, 0.012), zp, PH, 0.28, 0.72, 0.0, PH * hh, ('mermer', 'tas_acik', 'tas_acik', 'koyu'), derin=0.006)
for sx in (-1, 1):
    duz_duvar(y, V(PX + sx * (PW / 2 + 0.014), PY0 if sx > 0 else PY1), V(PX + sx * (PW / 2 + 0.014), PY1 if sx > 0 else PY0), zp, zp + PH, 'mermer')
    duz_duvar(y, V(PX + sx * (PW / 2 + 0.002), PY1 if sx > 0 else PY0), V(PX + sx * (PW / 2 + 0.002), PY0 if sx > 0 else PY1), zp, zp + PH, 'mermer')
    for yy, sg in ((PY0, -1), (PY1, 1)):
        y.yuz_yon([V(PX + sx * (PW / 2 + 0.002), yy, zp), V(PX + sx * (PW / 2 + 0.014), yy, zp), V(PX + sx * (PW / 2 + 0.014), yy, zp + PH),
                   V(PX + sx * (PW / 2 + 0.002), yy, zp + PH)], 'mermer', V(0, sg))
hp = 0.045
k4 = dikdortgen(PX - PW / 2, PX + PW / 2, PY0, PY1)
o = disa(k4, 0.016)
duvarlar(y, o, zp + PH, zp + PH + hp * 0.42, 'mermer')
y.yuz_yon([o[0] + Z * (zp + PH), o[1] + Z * (zp + PH), o[2] + Z * (zp + PH), o[3] + Z * (zp + PH)], 'tas_koyu', -Z)
f = disa(k4, 0.013)
duvarlar(y, f, zp + PH + hp * 0.42, zp + PH + hp * 0.8, 'mermer')
for i in range(4):
    triglif_dizi(f[i], f[(i + 1) % 4], zp + PH + hp * 0.42, hp * 0.38, 10 if i % 2 == 0 else 6, w=0.009, metop='mermer', rolyef=False)
silme(y, f, zp + PH + hp * 0.8, hp * 0.2, 0.012, 'mermer', 'tac')
zpe = zp + PH + hp
y.yuz_yon([V(p.x, p.y, zpe) for p in f], 'mermer', Z)
g4 = disa(k4, 0.025)
alinlik(y, V(g4[0].x, g4[0].y), V(g4[1].x, g4[1].y), zpe, 0.045, derin=g4[2].y - g4[0].y - 0.003, key='mermer', ic_key='lacivert', c=0.008,
        cati_key='mermer')
alinlik(y, V(g4[2].x, g4[2].y), V(g4[3].x, g4[3].y), zpe, 0.045, derin=0.003, key='mermer', ic_key='lacivert', c=0.008, cati_key='mermer')
kiremit_serit(g4[0].x, g4[1].x, g4[0].y + 0.008, g4[2].y - 0.008, zpe + 0.0064, 0.045, adim=0.024)
cubuk(y, V(PX, g4[0].y, zpe + 0.045 + 0.01), V(PX, g4[2].y, zpe + 0.045 + 0.01), 0.01, 'mermer')
# the Pinakotheke wing (west): a smaller Doric porch of three columns, a hipped roof
y.bolum('Pinakotheke ve Nike tapınağı')
QX0, QX1, QY0, QY1 = -1.0, -0.79, -0.76, -0.56
kutu(y, V(QX0, QY0, ZT), X, QX1 - QX0, QY1 - QY0, 0.01, 'mermer', 'onarkasagsolust')
QH = 0.12
duvarlar(y, [V(QX0, QY0 + 0.05), V(QX1, QY0 + 0.05), V(QX1, QY1), V(QX0, QY1)], ZT + 0.01, ZT + 0.01 + QH, 'mermer')
dikdortgen_acik(y, V(QX0 + 0.07, QY0 + 0.0501), V(QX1 - 0.07, QY0 + 0.0501), ZT + 0.01, QH, 0.25, 0.75, 0.0, QH * 0.6,
                ('mermer', 'tas_acik', 'tas_acik', 'koyu'), derin=0.01)
for i in range(4):
    kolon(QX0 + 0.012 + (QX1 - QX0 - 0.024) * i / 3, QY0 + 0.01, ZT + 0.01, ZT + 0.01 + QH, 0.01, 'dor', 'mermer', yiv=8)
kutu(y, V(QX0 - 0.004, QY0 - 0.003, ZT + 0.01 + QH), X, QX1 - QX0 + 0.008, QY1 - QY0 + 0.006, 0.014, 'mermer', 'onarkasagsol')
y.yuz_yon([V(QX0 - 0.004, QY0 - 0.003, ZT + 0.01 + QH), V(QX1 + 0.004, QY0 - 0.003, ZT + 0.01 + QH), V(QX1 + 0.004, QY0 + 0.05, ZT + 0.01 + QH),
           V(QX0 - 0.004, QY0 + 0.05, ZT + 0.01 + QH)], 'tas_koyu', -Z)
triglif_dizi(V(QX0 - 0.004, QY0 - 0.0035), V(QX1 + 0.004, QY0 - 0.0035), ZT + 0.016 + QH, 0.008, 8, w=0.007, metop='mermer', rolyef=False)
cati_kirma(y, QX0 - 0.004, QX1 + 0.004, QY0 - 0.003, QY1 + 0.003, ZT + 0.024 + QH, 0.05, 0.016, 'kirec', mahya='mermer', alt_key='mermer',
           kalinlik=0.008, ns=6, nr=3)

# the Nike bastion and the little Ionic temple of Athena Nike
NX0, NX1, NY0, NY1 = -0.36, -0.1, -0.99, -0.79
duvarlar(y, [V(NX0, NY0), V(NX1, NY0), V(NX1, NY1), V(NX0, NY1)], 0.0, ZT, 'kirec')
for zz in (0.08, 0.16, 0.24):
    silme(y, [V(NX0, NY1), V(NX0, NY0), V(NX1, NY0), V(NX1, NY1)], zz, 0.004, 0.002, 'tas_koyu', 'duz', kapali=False)
silme(y, [V(NX0, NY1), V(NX0, NY0), V(NX1, NY0), V(NX1, NY1)], ZT - 0.01, 0.01, 0.007, 'tas_acik', 'tac', kapali=False)
y.yuz_yon([V(NX0, NY0, ZT), V(NX1, NY0, ZT), V(NX1, NY1, ZT), V(NX0, NY1, ZT)], 'zemin', Z)
# the Nike parapet (relief slabs) round the bastion edge
for p, q in ((V(NX0, NY1), V(NX0, NY0)), (V(NX0, NY0), V(NX1, NY0)), (V(NX1, NY0), V(NX1, NY1))):
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    kutu(y, p - nn * 0.0 + Z * ZT, e, (q - p).length, 0.012, 0.028, 'mermer', 'onarkasagsolust')
    nseg = int((q - p).length / 0.03)
    for k in range(nseg):
        c = p.lerp(q, (k + 0.5) / nseg) + nn * 0.0012
        kutu(y, c + nn * 0.002 - e * 0.004 + Z * (ZT + 0.005), e, 0.008, 0.002, 0.018, 'tas_acik', 'onsagsolust')
NC = ((NX0 + NX1) / 2 + 0.01, (NY0 + NY1) / 2 + 0.01)
with parca(y, (NC[0], NC[1], ZT)):
    kutu(y, V(-0.06, -0.08, 0), X, 0.12, 0.16, 0.012, 'mermer', 'onarkasagsolust')
    y.yuz([V(-0.06, -0.08, 0.012), V(0.06, -0.08, 0.012), V(0.06, 0.08, 0.012), V(-0.06, 0.08, 0.012)], 'mermer')
    duvarlar(y, [V(-0.045, -0.035), V(0.045, -0.035), V(0.045, 0.035), V(-0.045, 0.035)], 0.012, 0.11, 'mermer')
    dikdortgen_acik(y, V(-0.045, -0.0352), V(0.045, -0.0352), 0.012, 0.098, 0.3, 0.7, 0.0, 0.07, ('mermer', 'tas_acik', 'tas_acik', 'koyu'), derin=0.008)
    for yy in (-0.066, 0.066):
        for i in range(4):
            kolon(-0.042 + 0.028 * i, yy, 0.012, 0.11, 0.0075, 'iyon', 'mermer', yiv=8)
    duvarlar(y, dikdortgen(-0.052, 0.052, -0.074, 0.074), 0.11, 0.122, 'mermer')
    y.yuz_yon([V(-0.052, -0.074, 0.11), V(0.052, -0.074, 0.11), V(0.052, 0.074, 0.11), V(-0.052, 0.074, 0.11)], 'tas_koyu', -Z)
    duvarlar(y, dikdortgen(-0.0525, 0.0525, -0.0745, 0.0745), 0.122, 0.134, 'lacivert')
    silme(y, dikdortgen(-0.0525, 0.0525, -0.0745, 0.0745), 0.134, 0.005, 0.005, 'mermer', 'tac')
    alinlik(y, V(-0.058, -0.08), V(0.058, -0.08), 0.139, 0.024, derin=0.157, key='mermer', ic_key='lacivert', c=0.006, cati_key='mermer')
    alinlik(y, V(0.058, 0.08), V(-0.058, 0.08), 0.139, 0.024, derin=0.003, key='mermer', ic_key='lacivert', c=0.006, cati_key='mermer')
sancak(y, NX0 + 0.02, NY0 + 0.025, ZT + 0.028, boy=0.24, en=0.11, yuk=0.07, aci=math.pi * 0.95)

# ================================================================ the Parthenon
y.bolum('Parthenon')
TX, TY = 0.06, 0.1
SPC = 0.088
TS = 1.18                         # the temple drawn larger than the rest: it owns the hill
with parca(y, (TX, TY, ZT), -math.pi / 2, TS):
    top, zs_ = parthenon(SPC * 16, SPC * 7, 17, 8, 0.0, 0.25, 0.0205)
# a few votive statues along the way, the Athena Promachos
y.bolum('Athena Promakhos')
AX, AY = -0.945, -0.44
kutu_merkez(y, (AX, AY), 0.12, 0.12, 0.016, 'mermer', z0=ZT)
kutu_merkez(y, (AX, AY), 0.1, 0.1, 0.012, 'mermer', z0=ZT + 0.016)
kutu_merkez(y, (AX, AY), 0.08, 0.08, 0.07, 'kirec', z0=ZT + 0.028)
kornis(y, AX - 0.04, AX + 0.04, AY - 0.04, AY + 0.04, ZT + 0.028, 0.008, 0.005, 'mermer', 'kaide')
kornis(y, AX - 0.04, AX + 0.04, AY - 0.04, AY + 0.04, ZT + 0.086, 0.012, 0.008, 'mermer', 'tac')
zA = ZT + 0.102
S = 1.0
# the figure: peplos falling in folds, aegis, a crested helmet, the spear in the right hand, the shield on the left
donel(y, (AX, AY), [(0.026, zA), (0.027, zA + 0.03), (0.023, zA + 0.12), (0.019, zA + 0.18), (0.022, zA + 0.22), (0.024, zA + 0.25),
                    (0.018, zA + 0.275), (0.008, zA + 0.285), (0.0, zA + 0.287)], 'bronz', n=14)
for k in range(8):
    a = TAU * k / 8 + 0.2
    boru(y, [V(AX + 0.026 * math.cos(a), AY + 0.026 * math.sin(a), zA + 0.003), V(AX + 0.02 * math.cos(a), AY + 0.02 * math.sin(a), zA + 0.16)],
         0.0035, 'bronz', n=4)
donel(y, (AX, AY), [(0.0235, zA + 0.215), (0.026, zA + 0.235), (0.022, zA + 0.255)], 'altin', n=14)      # aegis
kure(y, (AX, AY, zA + 0.305), 0.016, 'bronz', n=12, kat=6)
donel(y, (AX, AY), [(0.017, zA + 0.304), (0.018, zA + 0.316), (0.014, zA + 0.326), (0.0, zA + 0.33)], 'bronz', n=12)
boru(y, [V(AX - 0.016, AY, zA + 0.326), V(AX, AY, zA + 0.345), V(AX + 0.018, AY, zA + 0.33)], 0.005, 'boya_kirmizi', n=6)  # crest
# right arm and spear (towards the sea, -x / -y), left arm and shield
SPA = V(AX + 0.03, AY - 0.024, zA + 0.03)
boru(y, [V(AX + 0.016, AY - 0.012, zA + 0.26), V(AX + 0.03, AY - 0.024, zA + 0.24), V(AX + 0.032, AY - 0.026, zA + 0.2)], 0.0055, 'bronz', n=6)
cubuk(y, SPA, SPA + Z * 0.38, 0.0045, 'bronz')
donel(y, (SPA.x, SPA.y), [(0.004, SPA.z + 0.38), (0.008, SPA.z + 0.392), (0.0, SPA.z + 0.43)], 'altin', n=6)
boru(y, [V(AX - 0.016, AY + 0.01, zA + 0.26), V(AX - 0.03, AY + 0.012, zA + 0.2), V(AX - 0.034, AY + 0.0, zA + 0.16)], 0.0055, 'bronz', n=6)
SH = V(AX - 0.04, AY - 0.008, zA + 0.13)
boru(y, [SH + V(0.006, 0, 0), SH - V(0.006, 0, 0)], 0.055, 'bronz', n=20)
boru(y, [SH - V(0.006, 0, 0), SH - V(0.009, 0, 0)], 0.04, 'altin', n=20)
kure(y, SH - V(0.011, 0, 0), 0.012, 'altin', n=8, kat=4)

y.bolum('Erekhtheion')
EX, EY = -0.55, 0.745
with parca(y, (EX, EY, ZT), 0.0, 0.85):
    # local: long axis x, the caryatid porch on the -y side (faces -x world after the turn: towards the Propylaia)
    L2, W2, H2 = 0.36, 0.18, 0.15
    kutu(y, V(-L2 / 2 - 0.01, -W2 / 2 - 0.01, 0), X, L2 + 0.02, W2 + 0.02, 0.012, 'mermer', 'onarkasagsolust')
    y.yuz([V(-L2 / 2 - 0.01, -W2 / 2 - 0.01, 0.012), V(L2 / 2 + 0.01, -W2 / 2 - 0.01, 0.012), V(L2 / 2 + 0.01, W2 / 2 + 0.01, 0.012),
           V(-L2 / 2 - 0.01, W2 / 2 + 0.01, 0.012)], 'mermer')
    z1 = 0.012
    kc = dikdortgen(-L2 / 2 + 0.05, L2 / 2, -W2 / 2, W2 / 2)
    pencereli_duvar(y, kc, z1, H2, [0, 0, 3, 0], renk=('mermer', 'tas_acik', 'tas_acik', 'koyu'), v0=H2 * 0.45, en=0.4, ust=H2 * 0.25,
                    derin=0.008, sivri=0, cerceve=(0.004, 'tas_acik'))
    for i in range(6):     # the east Ionic porch
        kolon(-L2 / 2 + 0.012, -W2 / 2 + 0.01 + (W2 - 0.02) * i / 5, z1, z1 + H2, 0.0085, 'iyon', 'mermer', yiv=8)
    ze2 = z1 + H2
    duvarlar(y, dikdortgen(-L2 / 2 - 0.004, L2 / 2 + 0.004, -W2 / 2 - 0.004, W2 / 2 + 0.004), ze2, ze2 + 0.012, 'mermer')
    duvarlar(y, dikdortgen(-L2 / 2 - 0.0045, L2 / 2 + 0.0045, -W2 / 2 - 0.0045, W2 / 2 + 0.0045), ze2 + 0.012, ze2 + 0.024, 'bazalt')
    silme(y, dikdortgen(-L2 / 2 - 0.0045, L2 / 2 + 0.0045, -W2 / 2 - 0.0045, W2 / 2 + 0.0045), ze2 + 0.024, 0.006, 0.006, 'mermer', 'tac')
    y.yuz_yon([V(-L2 / 2 - 0.004, -W2 / 2 - 0.004, ze2), V(-L2 / 2 + 0.05, -W2 / 2 - 0.004, ze2), V(-L2 / 2 + 0.05, W2 / 2 + 0.004, ze2),
               V(-L2 / 2 - 0.004, W2 / 2 + 0.004, ze2)], 'tas_koyu', -Z)
    zr2 = ze2 + 0.03
    cati_besik(y, -L2 / 2 - 0.006, L2 / 2 + 0.006, -W2 / 2 - 0.006, W2 / 2 + 0.006, zr2, 0.035, 0.01, 'kirec', mahya='mermer', ucluk_key='lacivert',
               alinlik_key='mermer', alt_key='mermer', kalinlik=0.006, ns=8, nr=3)
    # the Porch of the Maidens on the south side: six caryatids on a high parapet, a flat roof
    CX0, CX1, CY = 0.03, 0.15, -W2 / 2 - 0.06
    duvarlar(y, [V(CX0, CY - 0.01), V(CX1, CY - 0.01), V(CX1, -W2 / 2), V(CX0, -W2 / 2)], z1, z1 + 0.05, 'mermer')
    silme(y, [V(CX0, -W2 / 2), V(CX0, CY - 0.01), V(CX1, CY - 0.01), V(CX1, -W2 / 2)], z1 + 0.044, 0.006, 0.004, 'mermer', 'tac', kapali=False)
    y.yuz_yon([V(CX0, CY - 0.01, z1 + 0.05), V(CX1, CY - 0.01, z1 + 0.05), V(CX1, -W2 / 2, z1 + 0.05), V(CX0, -W2 / 2, z1 + 0.05)], 'mermer', Z)
    for i in range(4):
        kore(CX0 + 0.012 + (CX1 - CX0 - 0.024) * i / 3, CY, z1 + 0.05, z1 + 0.13, 0.85)
    for xx in (CX0 + 0.012, CX1 - 0.012):
        kore(xx, CY + 0.032, z1 + 0.05, z1 + 0.13, 0.85)
    kutu(y, V(CX0 - 0.006, CY - 0.018, z1 + 0.13), X, CX1 - CX0 + 0.012, -CY - W2 / 2 + 0.018, 0.016, 'mermer', 'onarkasagsol')
    y.yuz_yon([V(CX0 - 0.006, CY - 0.018, z1 + 0.13), V(CX1 + 0.006, CY - 0.018, z1 + 0.13), V(CX1 + 0.006, -W2 / 2, z1 + 0.13),
               V(CX0 - 0.006, -W2 / 2, z1 + 0.13)], 'tas_koyu', -Z)
    kutu(y, V(CX0 - 0.009, CY - 0.021, z1 + 0.146), X, CX1 - CX0 + 0.018, -CY - W2 / 2 + 0.021, 0.008, 'mermer', 'onarkasagsolust')
    for k in range(10):     # dentils
        kutu(y, V(CX0 - 0.004 + (CX1 - CX0 + 0.008) * (k + 0.2) / 10, CY - 0.0195, z1 + 0.138), X, 0.006, 0.002, 0.006, 'mermer', 'onsagsol')
# Athena's sacred olive in the Pandroseion beside it
zeytin(-0.84, 0.72, ZT, 0.16, 1.1)

y.bolum('Büyük sunak ve adaklar')
SX_, SY_ = 0.62, -0.6
kutu_merkez(y, (SX_, SY_), 0.1, 0.22, 0.014, 'mermer', z0=ZT)
kutu_merkez(y, (SX_, SY_), 0.08, 0.2, 0.04, 'kirec', z0=ZT + 0.014)
kornis(y, SX_ - 0.04, SX_ + 0.04, SY_ - 0.1, SY_ + 0.1, ZT + 0.014, 0.008, 0.005, 'mermer', 'kaide')
kornis(y, SX_ - 0.04, SX_ + 0.04, SY_ - 0.1, SY_ + 0.1, ZT + 0.044, 0.01, 0.007, 'mermer', 'tac')
for s in (-1, 1):
    boru(y, [V(SX_ - 0.04, SY_ + s * 0.094, ZT + 0.062), V(SX_ + 0.04, SY_ + s * 0.094, ZT + 0.062)], 0.008, 'mermer', n=8)
donel(y, (SX_, SY_), [(0.02, ZT + 0.058), (0.024, ZT + 0.068), (0.014, ZT + 0.084), (0.006, ZT + 0.096), (0, ZT + 0.104)], 'boya_sari', n=10)
donel(y, (SX_, SY_), [(0.012, ZT + 0.08), (0.01, ZT + 0.1), (0, ZT + 0.12)], 'boya_kirmizi', n=8)
# votive statues and bronze bulls along the sacred way
for k, (x, yy) in enumerate(((-0.3, -0.57), (0.0, -0.57), (0.3, -0.57))):
    kutu_merkez(y, (x, yy), 0.05, 0.05, 0.01, 'mermer', z0=ZT)
    kutu_merkez(y, (x, yy), 0.04, 0.04, 0.04, 'kirec', z0=ZT + 0.01)
    kornis(y, x - 0.02, x + 0.02, yy - 0.02, yy + 0.02, ZT + 0.044, 0.006, 0.004, 'mermer', 'tac')
    figur(x, yy, ZT + 0.05, 0.75, 'bronz' if k % 2 else 'mermer', aci=-math.pi / 2, kol=0.9 if k % 2 else 0.7)
for x, yy in ((0.48, -0.62), (0.44, -0.66), (0.4, 0.66), (-0.3, 0.7)):
    amfora(x, yy, ZT, 1.3)
zeytin(0.72, 0.68, ZT, 0.14, 1.0)
zeytin(-0.3, 0.78, ZT, 0.12, 0.85)
sancak(y, 0.9, -0.56, ZT, boy=0.3, en=0.12, yuk=0.075, aci=math.pi * 0.9)

y.bolum('Kaya çıkıntıları')
# the bare rock breaking through the plateau, paving round the temple
g2 = random.Random(21)
for x, yy, r in ((-0.12, 0.68, 0.06), (0.2, 0.72, 0.06), (0.6, 0.68, 0.05), (0.82, -0.62, 0.045), (-0.98, 0.1, 0.05)):
    n = 7
    ring = [V(x + r * (0.7 + 0.3 * g2.random()) * math.cos(TAU * i / n), yy + r * (0.6 + 0.3 * g2.random()) * math.sin(TAU * i / n), ZT) for i in range(n)]
    top = [V(x + (p.x - x) * 0.55, yy + (p.y - yy) * 0.55, ZT + 0.012 + 0.008 * g2.random()) for p in ring]
    y.serit(ring, top, 'kaya')
    y.yuz_yon(top, 'kaya', Z)
# paving: a stone apron round the crepidoma
zz = ZT + 0.002
_hl, _hw = TS * (SPC * 8 + 0.0205 * 2.4 + 0.044), TS * (SPC * 3.5 + 0.0205 * 2.4 + 0.044)
ax0, ax1, ay0, ay1 = TX - _hl, TX + _hl, TY - _hw, TY + _hw
for (p, q) in ((V(ax0, ay0), V(ax1, ay0)), (V(ax1, ay0), V(ax1, ay1)), (V(ax1, ay1), V(ax0, ay1)), (V(ax0, ay1), V(ax0, ay0))):
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    y.yuz_yon([p + Z * zz, q + Z * zz, q + nn * 0.035 + e * 0.035 + Z * zz, p + nn * 0.035 - e * 0.035 + Z * zz], 'zemin', Z)
    duz_duvar(y, p + nn * 0.035 - e * 0.035 + Z * ZT, q + nn * 0.035 + e * 0.035 + Z * ZT, ZT, zz, 'kirec')

calistir(y, 'lm_parthenon')
