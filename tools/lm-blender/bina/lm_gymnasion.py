# Gymnasion (lm_gymnasion), after Olympia: the palaestra - a square Doric peristyle court of sand (with a wrestling
# pit) ringed by rooms and benched exedrae under lean-to tiled roofs, entered through an Ionic propylon - beside the
# xystos, a long covered Doric running stoa, with the open track (marble starting sills, turning posts, a water
# channel), rows of bronze athletes on statue bases, an altar of Hermes, a wash basin and olive trees.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04
TRI = 'lacivert'          # painted triglyphs (blue-black)


# ================================================================ Greek helpers
def kiremit_kaburga(p0, p1, w=0.0055, key='kiremit2'):
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


def kiremit_serit(x0, x1, y0, y1, z, h, eksen='y', adim=0.026, key='kiremit2'):
    """cover-tile ribs on a gable roof (ridge along eksen) from the eaves to the ridge"""
    if eksen == 'y':
        n = max(1, int((y1 - y0) / adim))
        for j in range(n + 1):
            yy = y0 + (y1 - y0) * j / n
            for xe in (x0, x1):
                kiremit_kaburga(V(xe, yy, z + 0.0015), V((x0 + x1) / 2, yy, z + h + 0.0015), key=key)
    else:
        n = max(1, int((x1 - x0) / adim))
        for j in range(n + 1):
            xx = x0 + (x1 - x0) * j / n
            for ye in (y0, y1):
                kiremit_kaburga(V(xx, ye, z + 0.0015), V(xx, (y0 + y1) / 2, z + h + 0.0015), key=key)


def kolon(cx, cy, z0, z1, r, tur='dor', key='mermer'):
    sutun(y, cx, cy, z0, z1, r, key, tur, yiv=12)


def triglif_dizi(p, q, z, h, n, key=TRI, w=0.012, metop=None):
    """n + 1 triglyphs on the frieze face p->q (faces its right), each with two grooves; metop: a key for
    painted metope panels between"""
    W = (q - p).length; e = (q - p) / W; nc = V(e.y, -e.x)
    for i in range(n + 1):
        c = p + e * (W * i / n)
        u = max(0.0, min(W - w, W * i / n - w / 2))
        o = p + e * u + Z * z
        kutu(y, o - nc * 0.0 + nc * 0.0025, e, w, 0.0025, h, key, 'onsagsolust')
        for g in (0.33, 0.67):   # grooves: thin dark strips
            gg = o + e * (w * g) + nc * 0.0027
            y.yuz_yon([gg - e * 0.0012, gg + e * 0.0012, gg + e * 0.0012 + Z * (h * 0.85), gg - e * 0.0012 + Z * (h * 0.85)], 'koyu', nc)
        if metop and i < n:
            m0 = p + e * (W * i / n + w / 2 + 0.002); m1 = p + e * (W * (i + 1) / n - w / 2 - 0.002)
            if (m1 - m0).dot(e) > 0.006:
                y.yuz_yon([m0 + nc * 0.001 + Z * (z + h * 0.12), m1 + nc * 0.001 + Z * (z + h * 0.12), m1 + nc * 0.001 + Z * (z + h * 0.88),
                           m0 + nc * 0.001 + Z * (z + h * 0.88)], metop, nc)


def saciklik(a, b, z, he, D, tur='dor', key='mermer', uz=0.0, arka=True, metop=None, n_tri=None):
    """a straight entablature over the column line a->b (faces the right of a->b), D deep, he high, running uz past
    the ends: Doric (plain architrave with a taenia, a triglyph frieze, a crowning cornice with a mutule band) or
    Ionic (three fasciae, a plain frieze, dentils, the cornice). Returns the top z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    o = a - e * uz + nc * (D / 2)
    L = W + 2 * uz
    ha, hf = he * 0.4, he * 0.38
    kutu(y, o + Z * z, e, L, D, ha, key, 'onarkasagsol' if arka else 'onsagsol')
    y.yuz_yon([o + Z * z, o + e * L + Z * z, o + e * L - nc * D + Z * z, o - nc * D + Z * z], key, -Z)
    kutu(y, o + Z * (z + ha) - nc * 0.003, e, L, D - 0.006, hf, key, 'onarkasagsol' if arka else 'onsagsol')
    y.yuz_yon([o + Z * (z + ha), o + e * L + Z * (z + ha), o + e * L - nc * 0.003 + Z * (z + ha), o - nc * 0.003 + Z * (z + ha)], key, Z)   # the ledge on the architrave
    if tur == 'dor':
        silme(y, [o, o + e * L], z + ha - he * 0.05, he * 0.05, 0.003, key, 'duz', kapali=False)       # taenia
        k = n_tri or max(2, int(round(W / 0.045)))
        triglif_dizi(o - nc * 0.003 + e * uz, o - nc * 0.003 + e * (uz + W), z + ha, hf, k, metop=metop)
    else:
        for t in (0.33, 0.66):
            silme(y, [o, o + e * L], z + ha * t, ha * 0.08, 0.002 * (1 + t), key, 'duz', kapali=False)
        k = int(L / 0.009)
        for j in range(k):
            kutu(y, o - nc * 0.003 + e * (L * (j + 0.2) / k) + Z * (z + ha + hf * 0.62) + nc * 0.004, e, L / k * 0.55, 0.004, hf * 0.22, key, 'onsagsol')
    zc = z + ha + hf
    silme(y, [o, o + e * L], zc, he * 0.22, he * 0.3, key, 'tac', kapali=False)
    if arka:
        silme(y, [o + e * L - nc * D, o - nc * D], zc, he * 0.22, he * 0.12, key, 'tac', kapali=False)
    y.yuz_yon([o + Z * (zc + he * 0.22), o + e * L + Z * (zc + he * 0.22), o + e * L - nc * D + Z * (zc + he * 0.22),
               o - nc * D + Z * (zc + he * 0.22)], key, Z)
    return zc + he * 0.22


def heykel(x, yy, z, s=1.0, key='bronz', kaide=True, aci=0.0):
    """a draped standing figure (on a moulded pedestal), one arm raised"""
    if kaide:
        kutu_merkez(y, (x, yy), 0.058 * s, 0.058 * s, 0.01 * s, 'mermer', z0=z)
        kutu_merkez(y, (x, yy), 0.046 * s, 0.046 * s, 0.058 * s, 'kirec', z0=z + 0.01 * s)
        kornis(y, x - 0.023 * s, x + 0.023 * s, yy - 0.023 * s, yy + 0.023 * s, z + 0.062 * s, 0.007 * s, 0.005 * s, 'mermer', 'tac')
        z += 0.069 * s
    donel(y, (x, yy), [(0.014 * s, z), (0.016 * s, z + 0.02 * s), (0.011 * s, z + 0.055 * s), (0.013 * s, z + 0.068 * s),
                       (0.008 * s, z + 0.077 * s), (0, z + 0.079 * s)], key, n=10)
    kure(y, (x, yy, z + 0.088 * s), 0.008 * s, key, n=8, kat=4)
    e = V(math.cos(aci), math.sin(aci))
    boru(y, [V(x, yy, z + 0.064 * s) + e * 0.01 * s, V(x, yy, z + 0.095 * s) + e * 0.022 * s], 0.0028 * s, key, n=5)


def cinar(x, yy, z, boy=0.2, s=1.0):
    """a plane tree: a pale forked trunk under a broad crown of several lumps"""
    top = V(x, yy, z + boy * 0.55)
    boru(y, [V(x, yy, z), V(x + 0.004 * s, yy, z + boy * 0.3), top], 0.007 * s, 'ahsap_acik', n=6, r_son=0.005 * s)
    for k, (dx, dy, dz, r) in enumerate(((0, 0, 0.62, 0.055), (0.04, 0.02, 0.5, 0.042), (-0.035, 0.025, 0.52, 0.04), (0.01, -0.04, 0.5, 0.042),
                                         (-0.02, -0.02, 0.75, 0.04))):
        c = (x + dx * s, yy + dy * s, z + boy * dz + 0.02 * s)
        kure(y, c, r * s, 'boya_yesil' if k % 2 else 'cimen', n=10, kat=5)


def selvi(x, yy, z, boy=0.18):
    y.prizma((x, yy), 0.004, z, z + boy * 0.12, 'ahsap', n=5)
    donel(y, (x, yy), [(0.0, z + boy * 0.08), (0.017, z + boy * 0.13), (0.022, z + boy * 0.36), (0.018, z + boy * 0.66),
                       (0.008, z + boy * 0.9), (0, z + boy)], 'boya_yesil', n=10)


def amfora(x, yy, z, s=1.0, key='siva_oker'):
    donel(y, (x, yy), [(0.0, z), (0.004 * s, z), (0.011 * s, z + 0.01 * s), (0.012 * s, z + 0.018 * s), (0.006 * s, z + 0.028 * s),
                       (0.004 * s, z + 0.034 * s), (0.0045 * s, z + 0.036 * s), (0, z + 0.036 * s)], key, n=8)


def tapinak(L, W, nl, nw, z0, HC, r, key='mermer', ic_key='boya_kirmizi', cati='kiremit', basamak=3, sb=0.014, ph=None,
            cella_key='mermer', metop='boya_kirmizi'):
    """a Doric peripteral temple at the origin, front (the door) facing -y, long axis y: column centres x in
    -W/2..W/2 (nw columns), y in -L/2..L/2 (nl columns) on a crepidoma of basamak steps (sb high each), the cella
    (pronaos in antis, a bronze door), a triglyph entablature, pediments with figures, a tiled roof, acroteria.
    Returns (the top z, stylobate z)"""
    sx_, sy_ = W / (nw - 1), L / (nl - 1)
    m = r * 2.4
    for k in range(basamak):        # crepidoma
        d = m + 0.018 * (basamak - 1 - k)
        x0, x1, y0, y1 = -W / 2 - d, W / 2 + d, -L / 2 - d, L / 2 + d
        kutu(y, V(x0, y0, z0 + sb * k), X, x1 - x0, y1 - y0, sb, key, 'onarkasagsol')
        y.yuz([V(x0, y0, z0 + sb * (k + 1)), V(x1, y0, z0 + sb * (k + 1)), V(x1, y1, z0 + sb * (k + 1)), V(x0, y1, z0 + sb * (k + 1))], key)
    zs = z0 + sb * basamak
    zc = zs + HC
    pts = [V(-W / 2 + sx_ * i, -L / 2) for i in range(nw - 1)] + [V(W / 2, -L / 2 + sy_ * j) for j in range(nl - 1)] + \
          [V(W / 2 - sx_ * i, L / 2) for i in range(nw - 1)] + [V(-W / 2, L / 2 - sy_ * j) for j in range(nl - 1)]
    for p in pts:
        kolon(p.x, p.y, zs, zc, r, 'dor', key)
    # cella: walls one bay in from the peristyle, a pronaos with two columns in antis, an opisthodomos the same
    cx = W / 2 - sx_ * 0.95
    cy0, cy1 = -L / 2 + sy_ * 1.3, L / 2 - sy_ * 1.3
    cyd0, cyd1 = cy0 + sy_ * 0.9, cy1 - sy_ * 0.9          # the door wall, the back wall
    t = 0.018
    for s in (-1, 1):                                       # long walls (both faces), antae
        duz_duvar(y, V(s * cx, cy0 if s > 0 else cy1), V(s * cx, cy1 if s > 0 else cy0), zs, zc, cella_key)
        duz_duvar(y, V(s * (cx - t), cy1 if s > 0 else cy0), V(s * (cx - t), cy0 if s > 0 else cy1), zs, zc, cella_key)
        for yy in (cy0, cy1):
            sg = -1 if yy == cy0 else 1
            y.yuz_yon([V(s * cx, yy, zs), V(s * (cx - t), yy, zs), V(s * (cx - t), yy, zc), V(s * cx, yy, zc)], cella_key, V(0, sg))
            kutu_merkez(y, (s * (cx - t / 2), yy), t * 1.5, t * 1.3, 0.012, key, z0=zc - 0.012)
    for xx in (-cx / 3, cx / 3):
        kolon(xx, cy0, zs, zc, r * 0.92, 'dor', key)
        kolon(xx, cy1, zs, zc, r * 0.92, 'dor', key)
    Wd, e_, nc_, Ld = dikdortgen_acik(y, V(-cx + t, cyd0), V(cx - t, cyd0), zs, HC, 0.36, 0.64, 0.0, HC * 0.7, (cella_key, key, key, 'bronz'),
                                      derin=0.012, cerceve=(0.008, key))
    y.yuz_yon([Ld(0.498, 0, 0.0115), Ld(0.502, 0, 0.0115), Ld(0.502, HC * 0.7, 0.0115), Ld(0.498, HC * 0.7, 0.0115)], 'koyu', nc_)
    duz_duvar(y, V(cx - t, cyd1), V(-cx + t, cyd1), zs, zc, cella_key)
    silme(y, dikdortgen(-cx, cx, cy0, cy1), zs, 0.012, 0.004, key, 'kaide')
    # entablature round the peristyle
    he = HC * 0.27
    D = r * 2.6
    k4 = dikdortgen(-W / 2, W / 2, -L / 2, L / 2)
    o = disa(k4, D / 2); ii = disa(k4, -D / 2)
    ha, hf = he * 0.4, he * 0.38
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
        triglif_dizi(p, q, zc + ha, hf, n, metop=metop)
    zk = zc + ha + hf
    silme(y, f, zk, he * 0.22, he * 0.32, key, 'tac')
    ze = zk + he * 0.22
    # ceiling of the pteron (coffered) over the cella walls
    y.yuz_yon([V(-W / 2, -L / 2, zc + ha), V(W / 2, -L / 2, zc + ha), V(W / 2, L / 2, zc + ha), V(-W / 2, L / 2, zc + ha)], 'tas_koyu', -Z)
    # pediments front and back, the roof
    g = disa(k4, D / 2 + he * 0.32)
    xa, xb, ya, yb = g[0].x, g[1].x, g[0].y, g[2].y
    ph = ph or (xb - xa) * 0.13
    alinlik(y, V(xa, ya), V(xb, ya), ze, ph, derin=yb - ya - 0.003, key=key, ic_key=ic_key, c=0.01, cati_key=cati)
    alinlik(y, V(xb, yb), V(xa, yb), ze, ph, derin=0.003, key=key, ic_key=ic_key, c=0.01, cati_key=cati)
    kiremit_serit(xa, xb, ya + 0.008, yb - 0.008, ze + 0.008, ph, 'y')
    cubuk(y, V(0, ya, ze + ph + 0.012), V(0, yb, ze + ph + 0.012), 0.011, 'kiremit2')
    for yy, sg in ((ya, -1), (yb, 1)):
        yt = yy - sg * 0.009
        # pediment figures: a standing god in the middle, smaller towards the corners, reclining ones at the ends
        heykel(0, yt, ze + 0.006, 0.5 * ph / 0.06, key, kaide=False)
        for s in (-1, 1):
            heykel(s * (xb - xa) * 0.14, yt, ze + 0.006, 0.36 * ph / 0.06, key, kaide=False, aci=s * 0.5)
            boru(y, [V(s * (xb - xa) * 0.26, yt, ze + 0.012), V(s * (xb - xa) * 0.38, yt, ze + 0.009)], 0.0065 * ph / 0.06, key, n=6, r_son=0.004)
        # acroteria: a palmette on the apex, griffins / urns at the corners
        donel(y, (0, yy), [(0.0, ze + ph + 0.012), (0.012, ze + ph + 0.016), (0.018, ze + ph + 0.032), (0.012, ze + ph + 0.046), (0, ze + ph + 0.05)],
              'altin', n=8)
        for xx in (xa + 0.012, xb - 0.012):
            kutu_merkez(y, (xx, yy - sg * 0.004), 0.018, 0.018, 0.008, key, z0=ze + 0.006)
            amfora(xx, yy - sg * 0.004, ze + 0.014, 0.9, 'altin')
    return ze + ph + 0.05, zs


def zeytin(x, yy, z, boy=0.14, s=1.0, tohum=0):
    """an olive tree: a short gnarled, leaning trunk splitting in two, a low wide silvery crown in lumps"""
    g = math.sin(tohum * 12.9898) * 0.5
    fork = V(x + 0.01 * s * g, yy + 0.006 * s, z + boy * 0.38)
    boru(y, [V(x, yy, z), V(x + 0.008 * s, yy - 0.004 * s, z + boy * 0.18), fork], 0.0085 * s, 'ahsap', n=6, r_son=0.006 * s)
    for k, (dx, dy, dz, r) in enumerate(((0.0, 0.0, 0.72, 0.05), (0.04, 0.015, 0.6, 0.038), (-0.038, 0.02, 0.62, 0.036), (0.012, -0.036, 0.58, 0.036),
                                         (-0.012, 0.03, 0.82, 0.032))):
        c = V(x + (dx + g * 0.01) * s, yy + dy * s, z + boy * dz)
        if k: boru(y, [fork, c - Z * 0.01], 0.004 * s, 'ahsap', n=5, r_son=0.0025 * s)
        donel(y, (c.x, c.y), [(0.0, c.z - r * s * 0.45), (r * s * 0.85, c.z - r * s * 0.25), (r * s, c.z + r * s * 0.1), (r * s * 0.7, c.z + r * s * 0.45),
                              (0, c.z + r * s * 0.6)], 'zeytin' if k % 2 == 0 else 'cimen', n=9, kat=k)


def atlet(x, yy, z, s=1.0, poz=0, aci=0.0):
    """a bronze athlete on a two-stepped marble base: poz 0 a runner, 1 a discus thrower, 2 a victor with a wreath"""
    kutu_merkez(y, (x, yy), 0.07 * s, 0.05 * s, 0.01 * s, 'kirec', z0=z)
    kutu_merkez(y, (x, yy), 0.058 * s, 0.04 * s, 0.045 * s, 'mermer', z0=z + 0.01 * s)
    kornis(y, x - 0.029 * s, x + 0.029 * s, yy - 0.02 * s, yy + 0.02 * s, z + 0.05 * s, 0.006 * s, 0.004 * s, 'mermer', 'tac')
    z += 0.056 * s
    with parca(y, (x, yy, z), aci, s):
        # legs (striding), body, head
        lean = (0.012, 0.0, 0.0)[poz]
        boru(y, [V(-0.006, 0.0, 0.0), V(-0.004, 0.0, 0.025), V(0.0, 0.0, 0.045)], 0.0042, 'bronz', n=5, r_son=0.005)
        boru(y, [V(0.012 if poz == 0 else 0.008, 0.0, 0.0), V(0.008, 0.0, 0.024), V(0.002, 0.0, 0.045)], 0.0042, 'bronz', n=5, r_son=0.005)
        boru(y, [V(0.0, 0, 0.044), V(lean * 0.5, 0, 0.06), V(lean, 0, 0.075)], 0.0075, 'bronz', n=7, r_son=0.0065)
        kure(y, (lean * 1.1, 0, 0.086), 0.0058, 'bronz', n=8, kat=4)
        if poz == 0:      # runner: arms swinging
            boru(y, [V(lean, -0.007, 0.072), V(lean + 0.012, -0.009, 0.062), V(lean + 0.02, -0.01, 0.07)], 0.0025, 'bronz', n=4)
            boru(y, [V(lean, 0.007, 0.072), V(lean - 0.012, 0.009, 0.06), V(lean - 0.016, 0.01, 0.05)], 0.0025, 'bronz', n=4)
        elif poz == 1:    # discus thrower: arm back with the disc
            boru(y, [V(0, -0.007, 0.072), V(-0.016, -0.012, 0.074), V(-0.03, -0.012, 0.08)], 0.0025, 'bronz', n=4)
            donel(y, (-0.033, -0.012), [(0.0, 0.074), (0.008, 0.077), (0.008, 0.08), (0, 0.083)], 'bronz', n=8)
            boru(y, [V(0, 0.007, 0.072), V(0.012, 0.01, 0.062)], 0.0025, 'bronz', n=4)
        else:             # victor: one arm raised with a wreath
            boru(y, [V(0, -0.007, 0.073), V(0.004, -0.012, 0.09), V(0.006, -0.012, 0.104)], 0.0025, 'bronz', n=4)
            boru(y, [V(0.006 + 0.007 * math.cos(TAU * k / 8), -0.012, 0.11 + 0.007 * math.sin(TAU * k / 8)) for k in range(9)], 0.0016, 'altin', n=4, kapat=False)
            boru(y, [V(0, 0.007, 0.073), V(0.004, 0.011, 0.055)], 0.0025, 'bronz', n=4)


def halka_cati(O, d, z_dis, z_ic, key='kiremit', sacak=0.03, adim=0.026):
    """a ring of lean-to roofs over the wings of a peristyle building: O the CCW outer eave rectangle at z_dis, the
    inner (court) eave d inside it at z_ic (lower: the rain runs into the court), hips at the corners, fascias, soffits
    from both eaves to the walls under them, cover-tile ribs, hip caps"""
    I = disa(O, -d)
    n = 4
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([O[i] + Z * z_dis, O[j] + Z * z_dis, I[j] + Z * z_ic, I[i] + Z * z_ic], key, Z)
        y.yuz_yon([O[i] + Z * z_dis, O[j] + Z * z_dis, O[j] + Z * (z_dis - 0.01), O[i] + Z * (z_dis - 0.01)], 'ahsap_koyu', (O[i] + O[j]) / 2 - (I[i] + I[j]) / 2)
        y.yuz_yon([I[i] + Z * z_ic, I[j] + Z * z_ic, I[j] + Z * (z_ic - 0.01), I[i] + Z * (z_ic - 0.01)], 'ahsap_koyu', (I[i] + I[j]) / 2 - (O[i] + O[j]) / 2)
        Ow = disa(O, -sacak); Iw = disa(I, sacak)
        y.yuz_yon([O[i] + Z * (z_dis - 0.01), O[j] + Z * (z_dis - 0.01), Ow[j] + Z * (z_dis - 0.01), Ow[i] + Z * (z_dis - 0.01)], 'ahsap_koyu', -Z)
        y.yuz_yon([I[i] + Z * (z_ic - 0.01), I[j] + Z * (z_ic - 0.01), Iw[j] + Z * (z_ic - 0.01), Iw[i] + Z * (z_ic - 0.01)], 'ahsap_koyu', -Z)
        # cover-tile ribs, cut at the hips
        L = (O[j] - O[i]).length; e = (O[j] - O[i]) / L; nin = V(-e.y, e.x)
        k = int(L / adim)
        for m in range(1, k):
            u = L * m / k
            t = min(d, u, L - u) / d
            p0 = O[i] + e * u + Z * (z_dis + 0.0015)
            p1 = O[i] + e * u + nin * (d * t) + Z * (z_dis + (z_ic - z_dis) * t + 0.0015)
            if t > 0.05: kiremit_kaburga(p0, p1, 0.0055)
        cubuk(y, O[i] + Z * (z_dis + 0.004), I[i] + Z * (z_ic + 0.004), 0.011, 'kiremit2')


def sacak_kapat(x0, x1, y0, y1, z, duvar_x0, duvar_x1, lift=0.0075):
    """the side eaves of a pediment roof (alinlik, ridge along y) from y0 to y1 at height z: the inner side of the fascia
    and a soffit back to the walls at duvar_x0 / duvar_x1"""
    for xe, xw, sg in ((x0, duvar_x0, -1), (x1, duvar_x1, 1)):
        # (the outer fascia is alinlik's own marble edge; only its inner side and the soffit are added)
        xi_ = xe - sg * 0.001     # its inner side (seen past the roof's far edge)
        y.yuz_yon([V(xi_, y0, z), V(xi_, y1, z), V(xi_, y1, z + lift), V(xi_, y0, z + lift)], 'ahsap_koyu', V(-sg, 0))
        y.yuz_yon([V(xe, y0, z), V(xe, y1, z), V(xw, y1, z), V(xw, y0, z)], 'ahsap_koyu', -Z)


def stoa_tek(x_on, x_arka, y0, y1, n, z0, HC, R, kat_key='mermer'):
    """a one-storey Doric stoa along y facing -x: the front colonnade at x_on (n bays), an inner Ionic row, a back
    wall with doors, end walls, a ceiling, a tiled gable roof. Returns the eaves z"""
    for i in range(n + 1):
        kolon(x_on, y0 + (y1 - y0) * i / n, z0, z0 + HC, R, 'dor', kat_key)
    xm = (x_on + x_arka) / 2 + 0.01
    for i in range(n // 2 + 1):
        kolon(xm, y0 + (y1 - y0) * i / (n // 2), z0, z0 + HC + HC * 0.27 * 0.4, R * 0.9, 'iyon', kat_key)
    ze = saciklik(V(x_on, y1), V(x_on, y0), z0 + HC, HC * 0.27, R * 2.6, 'dor', kat_key, uz=0.03, metop='boya_kirmizi', n_tri=n * 2)
    zl = z0 + HC + HC * 0.27 * 0.4
    y.yuz_yon([V(x_on + R * 1.3, y0 - 0.03, zl), V(x_arka, y0 - 0.03, zl), V(x_arka, y1 + 0.03, zl), V(x_on + R * 1.3, y1 + 0.03, zl)], 'ahsap_koyu', -Z)
    for i in range(n + 1):
        cubuk(y, V(x_on + R * 1.3, y0 + (y1 - y0) * i / n, zl - 0.003), V(x_arka, y0 + (y1 - y0) * i / n, zl - 0.003), 0.008, 'ahsap', 0.006)
    return ze


# ================================================================ platform
y.bolum('Zemin')
X0, X1, Y0, Y1 = -1.15, 1.16, -1.1, 1.1
zemin(y, X0, X1, Y0, Y1, Z0, 'tas_koyu', ust='toprak', basamak=(('on', 0.4), ('sol', 0.5)), n_basamak=3)
ZP = Z0 + 0.0015

# ================================================================ palaestra
PX0, PX1, PY0, PY1 = -1.1, 0.12, -0.6, 0.64
O = dikdortgen(PX0, PX1, PY0, PY1)
IW = 0.19                         # rooms' depth (outer wall to the inner wall)
IC = 0.285                        # outer wall to the column line
HC, R = 0.15, 0.0125
ZS = Z0 + 0.02                    # wings' floor
ZC = ZS + HC
HE = HC * 0.27
ZW = ZC + HE + 0.075              # outer wall top (the roof's high edge)
I = disa(O, -IW)
C = disa(O, -IC)
y.bolum('Palaistra: dış duvar')
kutu(y, V(PX0, PY0, Z0), X, PX1 - PX0, PY1 - PY0, ZS - Z0, 'kirec', 'onarkasagsol')
silme(y, O, Z0, 0.018, 0.008, 'kirec', 'kaide')
# outer walls: bays with small high windows and pilasters; the south side has the gateway in its middle
for i in range(4):
    a, b = O[i], O[(i + 1) % 4]
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    nb = 9
    for k in range(nb):
        p, q = a.lerp(b, k / nb), a.lerp(b, (k + 1) / nb)
        if i == 0 and k == nb // 2:
            dikdortgen_acik(y, p, q, ZS, ZW - ZS, 0.22, 0.78, 0.0, HC * 0.95, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.04)
            continue
        dikdortgen_acik(y, p, q, ZS, ZW - ZS, 0.42, 0.58, HC * 0.55, HC * 0.88, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.01, cerceve=(0.004, 'mermer'))
        if k:
            kutu(y, p - e * 0.009 + nc * 0.005 + Z * ZS, e, 0.018, 0.005, ZW - ZS - 0.02, 'kirec', 'onsagsol')
    silme(y, [a, b], ZW - 0.022, 0.022, 0.012, 'kirec', 'tac', kapali=False)
    silme(y, [a, b], ZS + HC * 0.45, 0.008, 0.005, 'kirec', 'duz', kapali=False)
y.bolum('Palaistra: odalar ve eksedralar')
# the rooms' front wall, facing the court: doors, and a wide exedra with two columns and a bench in the middle
Ir = [I[0], I[3], I[2], I[1]]                    # clockwise: faces inward
for i in range(4):
    a, b = Ir[i], Ir[(i + 1) % 4]
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    nb = 7
    for k in range(nb):
        p, q = a.lerp(b, k / nb), a.lerp(b, (k + 1) / nb)
        if k == 3:
            W_, e_, nc_, Lx = dikdortgen_acik(y, p, q, ZS, ZC + HE * 0.4 - ZS, 0.06, 0.94, 0.0, HC * 0.92, ('siva_krem', 'kirec', 'mermer', 'siva_oker'),
                                               derin=0.07)
            for u in (0.36, 0.64):
                c = Lx(u, 0, 0.006)
                kolon(c.x, c.y, ZS, ZS + HC * 0.92, 0.0085, 'iyon', 'mermer')
            c0 = Lx(0.1, 0, 0.068); c1 = Lx(0.9, 0, 0.068)
            kutu(y, c0 + Z * ZS + nc_ * 0.022, e_, (c1 - c0).length, 0.022, 0.03, 'mermer', 'onsagsolust')     # the bench
            continue
        dikdortgen_acik(y, p, q, ZS, ZC + HE * 0.4 - ZS, 0.3, 0.7, 0.0, HC * 0.7, ('siva_krem', 'kirec', 'kirec', 'koyu' if (k + i) % 2 else 'ahsap'),
                        derin=0.016, cerceve=(0.006, 'mermer'))
    silme(y, [a, b], ZS + HC * 0.78, 0.008, 0.003, 'boya_kirmizi', 'duz', kapali=False)
# the wings' floor ring (outside the court) and the ceiling ring
for i in range(4):
    j = (i + 1) % 4
    Cin = disa(O, -(IC + R * 2.2))
    y.yuz_yon([I[i] + Z * ZS, I[j] + Z * ZS, Cin[j] + Z * ZS, Cin[i] + Z * ZS], 'zemin', Z)
    Ce = disa(O, -(IC - R * 1.3))
    y.yuz_yon([I[i] + Z * (ZC + HE * 0.4), I[j] + Z * (ZC + HE * 0.4), Ce[j] + Z * (ZC + HE * 0.4), Ce[i] + Z * (ZC + HE * 0.4)], 'ahsap_koyu', -Z)
y.bolum('Palaistra: peristil')
nC = 8
for i in range(4):
    a, b = C[i], C[(i + 1) % 4]
    for k in range(nC):
        p = a.lerp(b, k / nC)
        kolon(p.x, p.y, ZS, ZC, R, 'dor', 'mermer')
# the peristyle's entablature, its face to the court
Cr = [C[0], C[3], C[2], C[1]]
for i in range(4):
    a, b = Cr[i], Cr[(i + 1) % 4]
    saciklik(a, b, ZC, HE, R * 2.6, 'dor', 'mermer', uz=R * 1.3, metop='boya_kirmizi', n_tri=nC * 2)
# the court: sunk a step, sand, a wrestling pit, athletes and an olive tree
Cin = disa(O, -(IC + R * 2.2))
y.yuz_yon([V(p.x, p.y, Z0 + 0.004) for p in Cin], 'kum_acik', Z)
duvarlar(y, [Cin[0], Cin[3], Cin[2], Cin[1]], Z0 + 0.004, ZS, 'mermer')
cx, cy = (PX0 + PX1) / 2, (PY0 + PY1) / 2
y.yuz_yon([V(cx - 0.18, cy - 0.04, Z0 + 0.005), V(cx - 0.02, cy - 0.04, Z0 + 0.005), V(cx - 0.02, cy + 0.12, Z0 + 0.005), V(cx - 0.18, cy + 0.12, Z0 + 0.005)],
          'kum', Z)
for (xa, ya, xb, yb) in ((cx - 0.19, cy - 0.05, cx - 0.01, cy - 0.04), (cx - 0.19, cy + 0.12, cx - 0.01, cy + 0.13),
                         (cx - 0.19, cy - 0.04, cx - 0.18, cy + 0.12), (cx - 0.02, cy - 0.04, cx - 0.01, cy + 0.12)):
    kutu(y, V(xa, ya, Z0 + 0.004), X, xb - xa, yb - ya, 0.005, 'kirec', 'onarkasagsolust')
atlet(cx + 0.12, cy + 0.1, Z0 + 0.004, 1.2, 2, -2.2)
atlet(cx + 0.1, cy - 0.15, Z0 + 0.004, 1.1, 1, 0.6)
zeytin(cx - 0.12, cy - 0.2, Z0 + 0.004, 0.15, 1.0, 3)
zeytin(cx + 0.2, cy - 0.02, Z0 + 0.004, 0.13, 0.9, 5)
y.bolum('Palaistra: çatı')
halka_cati(disa(O, 0.03), IC + 0.03 + R * 1.3 + HE * 0.3, ZW, ZC + HE + 0.003, 'kiremit')

# ================================================================ ephebeion: the tall hall in the middle of the north wing
y.bolum('Ephebeion salonu')
EX0, EX1 = cx - 0.18, cx + 0.18
EYF, EYB = PY1 - IW, PY1               # its court face on the rooms' front line, its back on the outer wall
EZ0 = ZC + HE * 0.4                    # rises from the wings' ceiling, above the ring roof
EZE = ZW + 0.19
EZT = EZE - 0.03                       # entablature
kose_e = dikdortgen(EX0, EX1, EYF, EYB)
for k in range(3):                     # the court face: three tall clerestory windows above the ring roof
    p_, q_ = V(EX0 + (EX1 - EX0) * k / 3, EYF), V(EX0 + (EX1 - EX0) * (k + 1) / 3, EYF)
    dikdortgen_acik(y, p_, q_, EZ0, EZT - EZ0, 0.3, 0.7, 0.085, EZT - EZ0 - 0.022, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.016,
                    cerceve=(0.006, 'mermer'))
for (p_, q_) in ((V(EX0, EYB), V(EX0, EYF)), (V(EX1, EYF), V(EX1, EYB))):   # the sides: two windows each
    for k in range(2):
        a_, b_ = p_.lerp(q_, k / 2), p_.lerp(q_, (k + 1) / 2)
        dikdortgen_acik(y, a_, b_, EZ0, EZT - EZ0, 0.3, 0.7, 0.1, EZT - EZ0 - 0.024, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.014,
                        cerceve=(0.005, 'mermer'))
duz_duvar(y, V(EX1, EYB), V(EX0, EYB), ZW - 0.012, EZT, 'kirec')
for (xx, yy) in ((EX0, EYF), (EX1, EYF), (EX0, EYB), (EX1, EYB)):              # corner pilasters
    kutu_merkez(y, (xx, yy), 0.026, 0.026, EZT - EZ0, 'mermer', z0=EZ0)
# the entablature round the hall: an architrave, a painted frieze with rosettes, the cornice
silme(y, kose_e, EZT, 0.012, 0.006, 'mermer', 'duz')
duvarlar(y, disa(kose_e, 0.003), EZT + 0.012, EZE - 0.008, 'boya_kirmizi')
for i in range(4):
    p_, q_ = disa(kose_e, 0.003)[i], disa(kose_e, 0.003)[(i + 1) % 4]
    e_ = (q_ - p_).normalized(); nc_ = V(e_.y, -e_.x); n_ = max(2, int((q_ - p_).length / 0.04))
    for k in range(n_):
        c_ = p_.lerp(q_, (k + 0.5) / n_) + nc_ * 0.0025 + Z * ((EZT + EZE) / 2 + 0.002)
        y.yuz_yon([c_ - e_ * 0.006 - Z * 0.006, c_ + e_ * 0.006 - Z * 0.006, c_ + e_ * 0.006 + Z * 0.006, c_ - e_ * 0.006 + Z * 0.006], 'altin', nc_)
silme(y, disa(kose_e, 0.003), EZE - 0.008, 0.012, 0.012, 'mermer', 'tac')
EZR = EZE + 0.004
EH = 0.08
alinlik(y, V(EX0 - 0.02, EYF - 0.02), V(EX1 + 0.02, EYF - 0.02), EZR, EH, derin=EYB - EYF + 0.04, key='mermer', ic_key='boya_kirmizi', c=0.009,
        cati_key='kiremit')
yb_ = EYB + 0.02
y.yuz_yon([V(EX0 - 0.02, yb_ - 0.002, EZR), V(EX1 + 0.02, yb_ - 0.002, EZR), V(cx, yb_ - 0.002, EZR + EH)], 'mermer', -Y)
for p_, q_ in ((V(EX0 - 0.02, yb_, EZR), V(cx, yb_, EZR + EH)), (V(cx, yb_, EZR + EH), V(EX1 + 0.02, yb_, EZR))):
    y.yuz_yon([p_, q_, q_ + Z * 0.0075, p_ + Z * 0.0075], 'mermer', Y)
sacak_kapat(EX0 - 0.02, EX1 + 0.02, EYF - 0.02, yb_, EZR, EX0, EX1)
kiremit_serit(EX0 - 0.02, EX1 + 0.02, EYF - 0.012, yb_ - 0.006, EZR + 0.0072, EH, 'y')
cubuk(y, V(cx, EYF - 0.02, EZR + EH + 0.01), V(cx, yb_, EZR + EH + 0.01), 0.011, 'kiremit2')
# figures in the pediment (Hermes and Herakles, patrons of the gymnasium), acroteria
heykel(cx, EYF - 0.028, EZR + 0.006, 0.62, 'mermer', kaide=False)
for s_ in (-1, 1):
    heykel(cx + s_ * 0.075, EYF - 0.028, EZR + 0.006, 0.42, 'mermer', kaide=False, aci=s_ * 0.6)
for yy in (EYF - 0.02, yb_):
    donel(y, (cx, yy), [(0.0, EZR + EH + 0.012), (0.012, EZR + EH + 0.016), (0.018, EZR + EH + 0.034), (0.012, EZR + EH + 0.048), (0, EZR + EH + 0.052)],
          'altin', n=8)
    for xx in (EX0 - 0.008, EX1 + 0.008):
        kutu_merkez(y, (xx, yy + (0.004 if yy < 0.5 else -0.004)), 0.016, 0.016, 0.008, 'mermer', z0=EZR)
        amfora(xx, yy + (0.004 if yy < 0.5 else -0.004), EZR + 0.008, 0.85, 'altin')

# ================================================================ propylon
y.bolum('Giriş propylonu')
GX = (PX0 + PX1) / 2
GY = PY0
kutu(y, V(GX - 0.17, GY - 0.13, Z0), X, 0.34, 0.13, ZS - Z0, 'mermer', 'onsagsol')
y.yuz([V(GX - 0.17, GY - 0.13, ZS), V(GX + 0.17, GY - 0.13, ZS), V(GX + 0.17, GY, ZS), V(GX - 0.17, GY, ZS)], 'mermer')
merdiven(y, (GX, GY - 0.19), math.pi / 2, 0.26, Z0, ZS, n=3, d=0.02, key='mermer')
HPC = ZW - ZS - 0.02
for xx in (-0.12, -0.04, 0.04, 0.12):
    kolon(GX + xx, GY - 0.1, ZS, ZS + HPC, 0.0135, 'iyon', 'mermer')
for s in (-1, 1):
    kutu(y, V(GX + s * 0.15 - 0.012, GY - 0.11, ZS), X, 0.024, 0.11, HPC, 'mermer', 'onsagsol')
zg = saciklik(V(GX - 0.15, GY - 0.1), V(GX + 0.15, GY - 0.1), ZS + HPC, 0.05, 0.036, 'iyon', 'mermer', uz=0.012)
y.yuz_yon([V(GX - 0.16, GY - 0.12, ZS + HPC), V(GX + 0.16, GY - 0.12, ZS + HPC), V(GX + 0.16, GY, ZS + HPC), V(GX - 0.16, GY, ZS + HPC)], 'ahsap_koyu', -Z)
alinlik(y, V(GX - 0.178, GY - 0.125), V(GX + 0.178, GY - 0.125), zg, 0.06, derin=0.15, key='mermer', ic_key='boya_kirmizi', c=0.009, cati_key='kiremit')
y.yuz_yon([V(GX - 0.178, GY + 0.023, zg), V(GX + 0.178, GY + 0.023, zg), V(GX, GY + 0.023, zg + 0.06)], 'mermer', -Y)   # the back gable's inner face
for p_, q_ in ((V(GX - 0.178, GY + 0.025, zg), V(GX, GY + 0.025, zg + 0.06)), (V(GX, GY + 0.025, zg + 0.06), V(GX + 0.178, GY + 0.025, zg))):
    y.yuz_yon([p_, q_, q_ + Z * 0.0075, p_ + Z * 0.0075], 'mermer', Y)       # close the gap under the roof's back end
for s in (-1, 1):   # the side entablature (closes the porch under the roof), the eave soffit
    xs = GX + s * 0.16
    y.yuz_yon([V(xs, GY - 0.118, ZS + HPC), V(xs, GY, ZS + HPC), V(xs, GY, zg + 0.002), V(xs, GY - 0.118, zg + 0.002)], 'mermer', V(s, 0))
    silme(y, [V(xs, GY - 0.118) if s > 0 else V(xs, GY), V(xs, GY) if s > 0 else V(xs, GY - 0.118)], zg - 0.014, 0.014, 0.01, 'mermer', 'tac', kapali=False)
sacak_kapat(GX - 0.178, GX + 0.178, GY - 0.125, GY + 0.025, zg, GX - 0.16, GX + 0.16)
kiremit_serit(GX - 0.178, GX + 0.178, GY - 0.12, GY + 0.025, zg + 0.0072, 0.06, 'y')
heykel(GX, GY - 0.13, zg + 0.004, 0.55, 'mermer', kaide=False)
for s in (-1, 1):
    heykel(GX + s * 0.08, GY - 0.13, zg + 0.004, 0.38, 'mermer', kaide=False, aci=s)
donel(y, (GX, GY - 0.125), [(0.0, zg + 0.06), (0.01, zg + 0.064), (0.015, zg + 0.08), (0.01, zg + 0.092), (0, zg + 0.096)], 'altin', n=8)
for s in (-1, 1):
    sancak(y, GX + s * 0.2, GY - 0.17, Z0, boy=0.34, en=0.1, yuk=0.065, aci=-math.pi / 2 + s * 0.5)

# ================================================================ track and xystos
y.bolum('Koşu yolu')
TX0, TX1 = 0.24, 0.66
TY0, TY1 = -1.03, 1.03
y.yuz([V(TX0, TY0, ZP), V(TX1, TY0, ZP), V(TX1, TY1, ZP), V(TX0, TY1, ZP)], 'kum_acik')
for xx in (TX0, TX1):
    kutu(y, V(xx - 0.007, TY0, Z0), X, 0.014, TY1 - TY0, 0.008, 'kirec', 'onarkasagsolust')
# the water channel along the stoa with basins
WX = TX1 + 0.025
y.yuz([V(WX - 0.012, TY0, ZP + 0.0005), V(WX + 0.012, TY0, ZP + 0.0005), V(WX + 0.012, TY1, ZP + 0.0005), V(WX - 0.012, TY1, ZP + 0.0005)], 'kirec')
y.yuz([V(WX - 0.006, TY0, ZP + 0.0011), V(WX + 0.006, TY0, ZP + 0.0011), V(WX + 0.006, TY1, ZP + 0.0011), V(WX - 0.006, TY1, ZP + 0.0011)], 'su')
for k in range(5):
    yy = TY0 + 0.2 + (TY1 - TY0 - 0.4) * k / 4
    havuz(y, WX - 0.02, WX + 0.02, yy - 0.025, yy + 0.025, ZP + 0.008, derin=0.01, kenar=0.007)
# starting sills (balbides) with the grooves and post holes, turning posts
for yy in (TY0 + 0.07, TY1 - 0.07):
    kutu(y, V(TX0, yy - 0.018, Z0), X, TX1 - TX0, 0.036, 0.004, 'mermer', 'onarkaust')
    for g in (-0.007, 0.007):
        y.yuz([V(TX0 + 0.005, yy + g - 0.0015, ZP + 0.0035), V(TX1 - 0.005, yy + g - 0.0015, ZP + 0.0035), V(TX1 - 0.005, yy + g + 0.0015, ZP + 0.0035),
               V(TX0 + 0.005, yy + g + 0.0015, ZP + 0.0035)], 'tas_koyu')
    for k in range(9):
        y.prizma((TX0 + (TX1 - TX0) * k / 8, yy), 0.0035, Z0, Z0 + 0.05, 'ahsap', n=5, ust=True)
    for xx in (TX0 + 0.1, TX1 - 0.1):
        y.prizma((xx, yy + (0.09 if yy < 0 else -0.09)), 0.009, Z0, Z0 + 0.07, 'mermer', n=8)
        kure(y, (xx, yy + (0.09 if yy < 0 else -0.09), Z0 + 0.074), 0.009, 'bronz', n=8, kat=4)
# lane lines
for k in range(1, 4):
    xx = TX0 + (TX1 - TX0) * k / 4
    y.yuz([V(xx - 0.0015, TY0 + 0.1, ZP + 0.0006), V(xx + 0.0015, TY0 + 0.1, ZP + 0.0006), V(xx + 0.0015, TY1 - 0.1, ZP + 0.0006),
           V(xx - 0.0015, TY1 - 0.1, ZP + 0.0006)], 'kum')

y.bolum('Ksistos: örtülü koşu stoası')
XS0, XS1 = 0.735, 1.1
SY0, SY1 = -1.0, 1.0
ZX = Z0 + 0.025
for k, (dx, hh) in enumerate(((0.04, 0.0125), (0.025, 0.025))):
    kutu(y, V(XS0 - dx, SY0 - 0.05, Z0), X, XS1 + 0.04 - XS0 + dx, SY1 - SY0 + 0.1, hh, 'mermer', 'onarkasagsol')
    y.yuz([V(XS0 - dx, SY0 - 0.05, Z0 + hh), V(XS1 + 0.04, SY0 - 0.05, Z0 + hh), V(XS1 + 0.04, SY1 + 0.05, Z0 + hh), V(XS0 - dx, SY1 + 0.05, Z0 + hh)],
          'zemin' if k else 'kirec')
HX = 0.2
ze = stoa_tek(XS0, XS1, SY0, SY1, 22, ZX, HX, 0.014)
# the back wall: inside doors to the rooms (apodyteria), outside bays with windows and pilasters
TB = 0.035
zl = ZX + HX + HX * 0.27 * 0.4
for k in range(11):
    a = V(XS1, SY1 + 0.03 - (SY1 - SY0 + 0.06) * k / 11); b = V(XS1, SY1 + 0.03 - (SY1 - SY0 + 0.06) * (k + 1) / 11)
    dikdortgen_acik(y, a, b, ZX, zl - ZX, 0.32, 0.68, 0.0, HX * 0.66, ('siva_krem', 'kirec', 'kirec', 'koyu' if k % 2 else 'ahsap'), derin=0.016,
                    cerceve=(0.006, 'mermer'))
    a2, b2 = V(XS1 + TB, b.y), V(XS1 + TB, a.y)
    dikdortgen_acik(y, a2, b2, Z0, ze - Z0, 0.4, 0.6, HX * 0.55, HX * 0.85, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.01, cerceve=(0.004, 'mermer'))
    if k:
        kutu(y, a2 + V(0.005, -0.009, Z0), Y, 0.018, 0.005, ze - Z0 - 0.002, 'kirec', 'onsagsol')
duz_duvar(y, V(XS1, SY0 - 0.03), V(XS1, SY1 + 0.03), zl, ze, 'kirec')
silme(y, [V(XS1 + TB, SY0 - 0.03), V(XS1 + TB, SY1 + 0.03)], Z0, 0.02, 0.008, 'kirec', 'kaide', kapali=False)
for yy, sg in ((SY0 - 0.03, -1), (SY1 + 0.03, 1)):
    xa_, xb_ = XS0 - 0.025, XS1 + TB
    kutu(y, V(xa_, yy - (0.02 if sg < 0 else 0), Z0), X, xb_ - xa_, 0.02, ze - Z0, 'kirec', 'arkasagsol' if sg < 0 else 'onsagsol')
    a, b = (V(xa_, yy - 0.02), V(xb_, yy - 0.02)) if sg < 0 else (V(xb_, yy + 0.02), V(xa_, yy + 0.02))
    duz_duvar(y, a, b, Z0, ZX, 'mermer')
    # the end face in bays: plain, a window, the door, a window, plain; antae at the corners, a string course
    for u0, u1, tur in ((0, 0.14, 0), (0.14, 0.27, 1), (0.27, 0.73, 2), (0.73, 0.86, 1), (0.86, 1, 0)):
        p, q = a.lerp(b, u0), a.lerp(b, u1)
        if tur == 0:
            duz_duvar(y, p, q, ZX, ze, 'kirec')
        elif tur == 1:
            dikdortgen_acik(y, p, q, ZX, ze - ZX, 0.3, 0.7, HX * 0.4, HX * 0.68, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.01, cerceve=(0.004, 'mermer'))
        else:
            dikdortgen_acik(y, p, q, ZX, ze - ZX, 0.33, 0.67, 0.0, HX * 0.72, ('kirec', 'kirec', 'mermer', 'ahsap'), derin=0.012, cerceve=(0.007, 'mermer'))
    e_ = (b - a).normalized(); W_ = (b - a).length; nc_ = V(e_.y, -e_.x)
    for u in (0.0, W_ - 0.022):
        kutu(y, a + e_ * u + nc_ * 0.005 + Z * Z0, e_, 0.022, 0.005, ze - Z0, 'mermer', 'onsagsol')
    silme(y, [a, b], ZX + HX * 0.8, 0.01, 0.006, 'mermer', 'tac', kapali=False)
cati_besik(y, XS0 - 0.04, XS1 + TB, SY0 - 0.05, SY1 + 0.05, ze, 0.085, 0.022, 'kiremit', ucluk_key='kirec', alinlik_key='mermer', mahya='kiremit2',
           uc_sacak=0.012)
kiremit_serit(XS0 - 0.04 - 0.022, XS1 + TB + 0.022, SY0 - 0.05, SY1 + 0.05, ze, 0.085, 'y')
for yy in (SY0 - 0.062, SY1 + 0.062):
    donel(y, ((XS0 - 0.04 + XS1 + TB) / 2, yy), [(0.0, ze + 0.09), (0.012, ze + 0.094), (0.016, ze + 0.11), (0.01, ze + 0.122), (0, ze + 0.126)], 'altin', n=8)
sancak(y, (XS0 + XS1) / 2, SY0 - 0.062, ze + 0.12, boy=0.16, en=0.1, yuk=0.06, aci=math.pi * 0.8)

# ================================================================ statues, altar, basin, olive trees
y.bolum('Heykel kaideleri')
for k in range(7):
    atlet(0.185, -0.95 + 0.29 * k, Z0, 1.0, k % 3, 0.3 if k % 2 else -0.3)
# a row of honorific bases in front of the palaestra
for k, xx in enumerate((-0.98, -0.82, -0.32, -0.16)):
    atlet(xx, -0.78, Z0, 1.05, (k + 1) % 3, -math.pi / 2 + 0.4 * (1 if k % 2 else -1))
y.bolum('Hermes sunağı, yıkanma havuzu')
# altar of Hermes between two herms
kutu_merkez(y, (-0.49, -0.93), 0.09, 0.06, 0.012, 'mermer', z0=Z0)
kutu_merkez(y, (-0.49, -0.93), 0.074, 0.046, 0.04, 'kirec', z0=Z0 + 0.012)
kornis(y, -0.49 - 0.037, -0.49 + 0.037, -0.953, -0.907, Z0 + 0.05, 0.008, 0.005, 'mermer', 'tac')
donel(y, (-0.49, -0.93), [(0.01, Z0 + 0.058), (0.013, Z0 + 0.066), (0.009, Z0 + 0.077), (0.004, Z0 + 0.085), (0, Z0 + 0.09)], 'boya_sari', n=10)
for xx in (-0.66, -0.32):
    kutu_merkez(y, (xx, -0.95), 0.018, 0.018, 0.07, 'mermer', z0=Z0)
    kure(y, (xx, -0.95, Z0 + 0.079), 0.01, 'mermer', n=8, kat=4)
# the wash basin (loutron) behind the palaestra: a long trough fed by spouts on a wall
LX0, LX1, LY = -0.85, -0.35, 0.85
kutu(y, V(LX0, LY + 0.06, Z0), X, LX1 - LX0, 0.03, 0.11, 'kirec', 'onarkasagsolust')
silme(y, [V(LX0, LY + 0.06), V(LX1, LY + 0.06)], Z0 + 0.1, 0.012, 0.006, 'mermer', 'tac', kapali=False)
havuz(y, LX0 + 0.01, LX1 - 0.01, LY - 0.01, LY + 0.05, Z0 + 0.03, derin=0.02, kenar=0.012)
for k in range(5):
    xx = LX0 + 0.05 + (LX1 - LX0 - 0.1) * k / 4
    kure(y, (xx, LY + 0.058, Z0 + 0.08), 0.009, 'bronz', n=8, kat=4)
    boru(y, [V(xx, LY + 0.052, Z0 + 0.077), V(xx, LY + 0.04, Z0 + 0.07), V(xx, LY + 0.036, Z0 + 0.04)], 0.0022, 'su', n=4)
y.bolum('Zeytin ağaçları')
for k, (xx, yy) in enumerate(((-1.04, -0.95), (-0.86, -1.0), (-0.12, -0.98), (0.02, -0.85), (0.08, -0.7), (-1.02, 0.78), (-1.0, 1.0),
                               (-0.2, 0.84), (-0.06, 1.0), (0.1, 0.8), (0.12, 1.0), (-0.7, 1.0), (-0.45, 1.01))):
    zeytin(xx, yy, Z0, 0.13 + 0.02 * ((k * 7) % 3) / 2, 1.0, k)

calistir(y, 'lm_gymnasion')
