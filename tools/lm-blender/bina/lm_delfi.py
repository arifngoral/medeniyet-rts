# Sanctuary of Apollo at Delphi (lm_delfi): a hillside in stepped terraces - the lower terrace with the Sacred Way,
# the Doric Treasury of the Athenians and the caryatid Treasury of the Siphnians; the great polygonal retaining wall
# with the Way ramping up along it; the temple terrace with the Doric Temple of Apollo (6 x 15) on its high base, the
# black-and-white Altar of the Chians, the Serpent Column tripod and the Naxian Sphinx; above, the theatre's stepped
# semicircle cut into the slope, the charioteer monument, the Lesche, cypresses, and the Phaedriades cliffs behind.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04
TRI = 'lacivert'          # painted triglyphs (blue-black)
RNG = random.Random(11)


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


def halka_saciklik(k4, zc, he, D, key='mermer', sayilar=(4, 4, 4, 4), metop='boya_kirmizi', tur='dor'):
    """an entablature round a CCW rectangle of column centres / wall lines (as in tapinak): architrave, a triglyph (or
    plain Ionic) frieze, a crowning cornice, the soffit. Returns (top z, the cornice's outer rectangle)"""
    o = disa(k4, D / 2); ii = disa(k4, -D / 2)
    ha, hf = he * 0.4, he * 0.38
    duvarlar(y, o, zc, zc + ha, key)
    if tur == 'dor':
        silme(y, o, zc + ha - he * 0.05, he * 0.05, 0.003, key, 'duz')
    else:
        for t in (0.33, 0.66):
            silme(y, o, zc + ha * t, ha * 0.08, 0.002 * (1 + t), key, 'duz')
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * zc, o[j] + Z * zc, ii[j] + Z * zc, ii[i] + Z * zc], key, -Z)
    f = disa(k4, D / 2 - 0.003)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * (zc + ha), o[j] + Z * (zc + ha), f[j] + Z * (zc + ha), f[i] + Z * (zc + ha)], key, Z)
    duvarlar(y, f, zc + ha, zc + ha + hf, key)
    if tur == 'dor':
        for i in range(4):
            triglif_dizi(f[i], f[(i + 1) % 4], zc + ha, hf, sayilar[i], metop=metop)
    zk = zc + ha + hf
    silme(y, f, zk, he * 0.22, he * 0.32, key, 'tac')
    return zk + he * 0.22, disa(k4, D / 2 + he * 0.32)


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


def hazine(W, L, H, r, tur='dor', key='mermer', frizk=None):
    """a treasury at the origin, its front (-y) a porch with two columns (tur 'dor') or two caryatids ('karyatid',
    with an Ionic sculpted frieze) between antae; a stepped base, a bronze door, pediments, a tiled roof, acroteria.
    W x L the wall rectangle. Returns the top z"""
    pd = L * 0.3
    for k, d in enumerate((0.03, 0.018)):
        x0, x1, y0, y1 = -W / 2 - d, W / 2 + d, -L / 2 - d, L / 2 + d
        kutu(y, V(x0, y0, 0.012 * k), X, x1 - x0, y1 - y0, 0.012, key, 'onarkasagsol')
        y.yuz([V(x0, y0, 0.012 * (k + 1)), V(x1, y0, 0.012 * (k + 1)), V(x1, y1, 0.012 * (k + 1)), V(x0, y1, 0.012 * (k + 1))], key)
    zs = 0.024
    zc = zs + H
    t = W * 0.09
    duz_duvar(y, V(W / 2, -L / 2), V(W / 2, L / 2), zs, zc, key)
    duz_duvar(y, V(W / 2, L / 2), V(-W / 2, L / 2), zs, zc, key)
    duz_duvar(y, V(-W / 2, L / 2), V(-W / 2, -L / 2), zs, zc, key)
    for s in (-1, 1):
        y.yuz_yon([V(s * W / 2, -L / 2, zs), V(s * (W / 2 - t), -L / 2, zs), V(s * (W / 2 - t), -L / 2, zc), V(s * W / 2, -L / 2, zc)], key, -Y)
        duz_duvar(y, V(s * (W / 2 - t), -L / 2 + pd) if s > 0 else V(-(W / 2 - t), -L / 2), V(s * (W / 2 - t), -L / 2) if s > 0 else V(-(W / 2 - t), -L / 2 + pd),
                  zs, zc, key)
    Wd, e_, nc_, Ld = dikdortgen_acik(y, V(-W / 2 + t, -L / 2 + pd), V(W / 2 - t, -L / 2 + pd), zs, H, 0.3, 0.7, 0.0, H * 0.68, (key, key, key, 'bronz'),
                                      derin=0.01, cerceve=(0.006, key))
    y.yuz_yon([Ld(0.497, 0, 0.0095), Ld(0.503, 0, 0.0095), Ld(0.503, H * 0.68, 0.0095), Ld(0.497, H * 0.68, 0.0095)], 'koyu', nc_)
    for xx in (-W * 0.19, W * 0.19):
        if tur == 'dor':
            kolon(xx, -L / 2, zs, zc, r, 'dor', key)
        else:
            kore(xx, -L / 2, zs, zc, r / 0.012, key)
    he = H * 0.3
    k4 = dikdortgen(-W / 2, W / 2, -L / 2, L / 2)
    n_on = 4
    ze, g = halka_saciklik(k4, zc, he, r * 2.6, key, (n_on * 2, int(L / (W / n_on)) * 2, n_on * 2, int(L / (W / n_on)) * 2),
                           tur='dor' if tur == 'dor' else 'iyon')
    if tur != 'dor':        # the sculpted frieze: a painted ground with relief figures, all round
        f = disa(k4, r * 1.3 - 0.003 + 0.0012)
        z1, z2 = zc + he * 0.42, zc + he * 0.76
        for i in range(4):
            p, q = f[i], f[(i + 1) % 4]
            Lq = (q - p).length; e = (q - p) / Lq; nn = V(e.y, -e.x)
            y.yuz_yon([p + Z * z1, q + Z * z1, q + Z * z2, p + Z * z2], frizk or 'lacivert', nn)
            m = int(Lq / 0.022)
            for k in range(m):
                c = p + e * (Lq * (k + 0.5) / m) + nn * 0.0012
                hh = (z2 - z1) * 0.8
                y.yuz_yon([c - e * 0.004 + Z * (z1 + 0.002), c + e * 0.004 + Z * (z1 + 0.002), c + e * 0.003 + Z * (z1 + hh * 0.78),
                           c - e * 0.003 + Z * (z1 + hh * 0.78)], key, nn)
                y.yuz_yon([c - e * 0.0022 + Z * (z1 + hh * 0.8), c + e * 0.0022 + Z * (z1 + hh * 0.8), c + e * 0.0022 + Z * (z1 + hh),
                           c - e * 0.0022 + Z * (z1 + hh)], key, nn)
    y.yuz_yon([V(-W / 2, -L / 2, zc + he * 0.4), V(W / 2, -L / 2, zc + he * 0.4), V(W / 2, -L / 2 + pd, zc + he * 0.4), V(-W / 2, -L / 2 + pd, zc + he * 0.4)],
              'ahsap_koyu', -Z)
    xa, xb, ya, yb = g[0].x, g[1].x, g[0].y, g[2].y
    ph = (xb - xa) * 0.15
    alinlik(y, V(xa, ya), V(xb, ya), ze, ph, derin=yb - ya - 0.003, key=key, ic_key='boya_kirmizi', c=0.008, cati_key='kiremit')
    alinlik(y, V(xb, yb), V(xa, yb), ze, ph, derin=0.003, key=key, ic_key='boya_kirmizi', c=0.008, cati_key='kiremit')
    kiremit_serit(xa, xb, ya + 0.006, yb - 0.006, ze + 0.0064, ph, 'y')
    cubuk(y, V(0, ya, ze + ph + 0.01), V(0, yb, ze + ph + 0.01), 0.009, 'kiremit2')
    heykel(0, ya - 0.007, ze + 0.004, 0.33, key, kaide=False)
    for s in (-1, 1):
        heykel(s * (xb - xa) * 0.15, ya - 0.007, ze + 0.004, 0.22, key, kaide=False, aci=s)
    donel(y, (0, ya), [(0.0, ze + ph + 0.008), (0.009, ze + ph + 0.012), (0.013, ze + ph + 0.026), (0.008, ze + ph + 0.036), (0, ze + ph + 0.04)], 'altin', n=8)
    for xx in (xa + 0.01, xb - 0.01):
        amfora(xx, ya + 0.008, ze + 0.002, 0.7, 'altin')
    return ze + ph + 0.04


def at(x, yy, z, aci=0.0, s=1.0, key='bronz'):
    """a bronze horse, one foreleg raised, facing angle aci"""
    with parca(y, (x, yy, z), aci, s):
        boru(y, [V(-0.032, 0, 0.062), V(0, 0, 0.066), V(0.03, 0, 0.068)], 0.015, key, n=8)
        for lx, ly, up in ((0.024, 0.008, 1), (0.024, -0.008, 0), (-0.026, 0.008, 0), (-0.026, -0.008, 0)):
            if up:
                boru(y, [V(lx, ly, 0.058), V(lx + 0.016, ly, 0.04), V(lx + 0.012, ly, 0.026)], 0.0045, key, n=5)
            else:
                boru(y, [V(lx, ly, 0.058), V(lx + 0.002, ly, 0.028), V(lx, ly, 0.0)], 0.0045, key, n=5, r_son=0.0035)
        boru(y, [V(0.028, 0, 0.072), V(0.042, 0, 0.096), V(0.05, 0, 0.104)], 0.008, key, n=7, r_son=0.006)
        boru(y, [V(0.048, 0, 0.106), V(0.066, 0, 0.094)], 0.0055, key, n=6, r_son=0.004)
        boru(y, [V(-0.044, 0, 0.066), V(-0.054, 0, 0.044), V(-0.052, 0, 0.03)], 0.004, key, n=5, r_son=0.002)


def poligon_duvar(a, b, z0, z1, nx, ny, tas='kirec', derz='tas_koyu', cik=0.004, tohum=3):
    """a wall face a->b (faces its right) of polygonal masonry: irregular many-sided blocks with sunk joints and
    chamfered edges standing cik proud of the dark joint face"""
    g = random.Random(tohum)
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    duz_duvar(y, a, b, z0, z1, derz)
    H = z1 - z0
    P = {}
    for i in range(nx + 1):
        for j in range(ny + 1):
            u, v = W * i / nx, H * j / ny
            if 0 < i < nx: u += g.uniform(-0.32, 0.32) * W / nx
            if 0 < j < ny: v += g.uniform(-0.3, 0.3) * H / ny
            P[i, j] = (u, v)
    L = lambda u, v, d: a + e * u + nc * d + Z * (z0 + v)
    polys = []
    for i in range(nx):
        for j in range(ny):
            q = [P[i, j], P[i + 1, j], P[i + 1, j + 1], P[i, j + 1]]
            if g.random() < 0.35:     # split into two polygons along a diagonal (more irregular joints)
                if g.random() < 0.5: polys += [[q[0], q[1], q[2]], [q[0], q[2], q[3]]]
                else: polys += [[q[0], q[1], q[3]], [q[1], q[2], q[3]]]
            else:
                polys.append(q)
    for pg in polys:
        cu = sum(p[0] for p in pg) / len(pg); cv = sum(p[1] for p in pg) / len(pg)
        ins = []
        for (u, v) in pg:
            du, dv = u - cu, v - cv
            dl = math.hypot(du, dv) or 1
            k = max(0.0, dl - 0.0035) / dl
            ins.append((cu + du * k, cv + dv * k))
        y.yuz_yon([L(u, v, cik) for u, v in ins], tas, nc)
        n = len(pg)
        for k in range(n):
            (u0, v0), (u1, v1) = ins[k], ins[(k + 1) % n]
            (o0, w0), (o1, w1) = pg[k], pg[(k + 1) % n]
            mid = (L(u0, v0, cik * 0.5) + L(u1, v1, cik * 0.5)) / 2
            y.yuz_yon([L(o0, w0, 0.0003), L(o1, w1, 0.0003), L(u1, v1, cik), L(u0, v0, cik)], tas, mid - L(cu, cv, 0) + nc * 0.0)


def kavea(c, z0, r0, r1, n_sira, dz, t0, t1, key='kirec', n=28, aisle=6, diazoma=None):
    """the stepped semicircle of a Greek theatre round c: rows from r0 to r1 rising dz each from z0, between angles
    t0..t1 (the opening faces the other way); radial stairways (aisle of them) and a wider walkway at row diazoma"""
    w = (r1 - r0) / n_sira
    A = lambda r, t, z: V(c[0] + r * math.cos(t), c[1] + r * math.sin(t), z)
    ts = [t0 + (t1 - t0) * i / n for i in range(n + 1)]
    for k in range(n_sira):
        ra, rb = r0 + w * k, r0 + w * (k + 1)
        zt = z0 + dz * (k + 1)
        zb = z0 + dz * k
        for i in range(n):
            ta, tb = ts[i], ts[i + 1]
            y.yuz_yon([A(ra, ta, zt), A(ra, tb, zt), A(rb, tb, zt), A(rb, ta, zt)], 'zemin' if k == diazoma else key, Z)
            ic = V(c[0], c[1], zt) - A(ra, (ta + tb) / 2, zt)
            y.yuz_yon([A(ra, ta, zb), A(ra, tb, zb), A(ra, tb, zt), A(ra, ta, zt)], key if k else 'mermer', ic)
            # the seat's front edge: a thin darker shadow line (the overhanging seat lip)
            y.yuz_yon([A(ra - 0.0006, ta, zt - dz * 0.3), A(ra - 0.0006, tb, zt - dz * 0.3), A(ra - 0.0006, tb, zt - dz * 0.18), A(ra - 0.0006, ta, zt - dz * 0.18)],
                      'tas_koyu', ic)
        # the side ends of each row
        for t, sg in ((t0, -1), (t1, 1)):
            tn = V(-math.sin(t), math.cos(t)) * sg
            y.yuz_yon([A(ra, t, z0), A(rb, t, z0), A(rb, t, zt), A(ra, t, zt)], key, tn)
    # the outer back wall
    zt = z0 + dz * n_sira
    for i in range(n):
        yuz_dis(y, [A(r1, ts[i], z0), A(r1, ts[i + 1], z0), A(r1, ts[i + 1], zt), A(r1, ts[i], zt)], 'tas', (c[0], c[1], zt))
    # radial stairways: small steps (half the row height) down the middle of each aisle
    for m in range(aisle + 1):
        t = t0 + (t1 - t0) * (0.04 + 0.92 * m / aisle)
        e = V(math.cos(t), math.sin(t)); s = V(-e.y, e.x)
        for k in range(n_sira):
            if k == diazoma: continue
            ra = r0 + w * k
            for h in range(2):
                p = V(c[0], c[1]) + e * (ra + w * h * 0.5 + w * 0.25)
                kutu_merkez(y, (p.x, p.y), w * 0.5, 0.016, dz * (k + 0.5 * (h + 1)) + 0.0015, 'tas_acik', z0=z0, aci=t, yuzler='onarkasagsolust')
    return zt


def kayalik(x0, x1, yf, yb, zb, n, hmin, hmax, tohum=5):
    """a jagged cliff band along x (the Phaedriades): a faceted rock face rising from zb and leaning back in
    irregular steps (a grid of jittered points), a rough grassy top, the back and the two ends"""
    g = random.Random(tohum)
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    ht = []
    for i in range(n + 1):     # a ridge line: two long swells plus noise
        t = i / n
        ht.append(zb + hmin + (hmax - hmin) * (0.5 + 0.3 * math.sin(t * 7.0 + 0.6) + 0.2 * math.sin(t * 17.0)) + g.uniform(-0.03, 0.03))
    T = (0.0, 0.22, 0.45, 0.62, 0.8, 1.0)                       # height fractions
    D = (0.0, 0.006, 0.02, 0.03, 0.05, 0.075)                   # set back
    P = {}
    for i in range(n + 1):
        for k, (t, d) in enumerate(zip(T, D)):
            jx = 0 if i in (0, n) else g.uniform(-0.3, 0.3) * (x1 - x0) / n
            jy = g.uniform(-0.01, 0.012) if 0 < k else g.uniform(0, 0.01)
            P[i, k] = V(xs[i] + jx * (1 if 0 < k < len(T) - 1 else 0), yf + d + jy, zb + (ht[i] - zb) * t + (g.uniform(-0.012, 0.012) if 0 < k < len(T) - 1 else 0))
    TB = (0.0, 0.3, 0.6, 0.85, 1.0)                              # the back: height fractions, set forward as it rises
    DB = (0.0, 0.006, 0.012, 0.02, 0.028)
    B = {}
    for i in range(n + 1):
        for k, (t, d) in enumerate(zip(TB, DB)):
            jx = 0 if i in (0, n) or k in (0, len(TB) - 1) else g.uniform(-0.25, 0.25) * (x1 - x0) / n
            B[i, k] = V(xs[i] + jx, yb - d - (g.uniform(0, 0.008) if 0 < k else 0), zb + (ht[i] - 0.02 - zb) * t + (g.uniform(-0.01, 0.01) if 0 < k < len(TB) - 1 else 0))
    for i in range(n):
        for k in range(len(T) - 1):
            q = [P[i, k], P[i + 1, k], P[i + 1, k + 1], P[i, k + 1]]
            key = 'kaya_koyu' if g.random() < 0.35 or k == 0 else 'kaya'
            if g.random() < 0.5:     # split into two facets
                y.yuz_yon([q[0], q[1], q[2]], key, -Y + Z * 0.2)
                y.yuz_yon([q[0], q[2], q[3]], 'kaya' if key == 'kaya_koyu' else 'kaya_koyu', -Y + Z * 0.2)
            else:
                y.yuz_yon(q, key, -Y + Z * 0.2)
        top = len(T) - 1
        y.yuz_yon([P[i, top], P[i + 1, top], B[i + 1, len(TB) - 1], B[i, len(TB) - 1]], 'cimen' if i % 3 else 'toprak', Z)
        for k in range(len(TB) - 1):     # the back: faceted rock too (it shows from the far side)
            q = [B[i, k], B[i + 1, k], B[i + 1, k + 1], B[i, k + 1]]
            key = 'kaya_koyu' if (i * 5 + k * 3) % 3 == 0 else 'kaya'
            if (i * 7 + k) % 2:
                y.yuz_yon([q[0], q[1], q[2]], key, Y + Z * 0.2)
                y.yuz_yon([q[0], q[2], q[3]], key, Y + Z * 0.2)
            else:
                y.yuz_yon(q, key, Y + Z * 0.2)
        if g.random() < 0.45:      # shrubs on the crest
            c = P[i, top].lerp(B[i, len(TB) - 1], 0.4)
            kure(y, (c.x, c.y, c.z + 0.006), g.uniform(0.014, 0.024), 'boya_yesil' if i % 2 else 'zeytin', n=8, kat=4)
    for i, sx in ((0, -1), (n, 1)):
        prof = [P[i, k] for k in range(len(T))]
        y.yuz_yon(prof + [B[i, k] for k in reversed(range(len(TB)))], 'kaya_koyu', V(sx, 0))
    # fallen boulders at the foot
    for k in range(n // 2):
        xx = x0 + 0.05 + (x1 - x0 - 0.1) * g.random()
        r = g.uniform(0.012, 0.026)
        donel(y, (xx, yf - 0.01 - g.uniform(0, 0.03)), [(r, zb), (r * 1.1, zb + r * 0.5), (r * 0.6, zb + r), (0, zb + r * 1.15)], 'kaya', n=6, kat=g.random())


# ================================================================ ground: terraces
X0, X1, Y0, Y1 = -1.15, 1.15, -1.1, 1.1
Z1 = Z0 + 0.2                  # temple terrace
Z2 = Z1 + 0.08                 # theatre terrace
YW1, YW2 = -0.55, 0.25         # the polygonal wall, the upper retaining wall
y.bolum('Teraslar')
zemin(y, X0, X1, Y0, Y1, Z0, 'tas_koyu', ust='toprak', basamak=(), n_basamak=3)
merdiven(y, (0.72, Y0 - 0.09), math.pi / 2, 0.24, 0.0, Z0, n=3, d=0.03, key='tas_koyu')
# temple terrace: sides and back in ashlar, the top
duz_duvar(y, V(X1, Y1), V(X0, Y1), Z0, Z1, 'tas_koyu')
poligon_duvar(V(X1, YW1), V(X1, Y1), Z0, Z1, 22, 4, 'kirec', 'tas_koyu', tohum=8)
poligon_duvar(V(X0, Y1), V(X0, YW1), Z0, Z1, 22, 4, 'kirec', 'tas_koyu', tohum=9)
y.yuz([V(X0, YW1, Z1), V(X1, YW1, Z1), V(X1, YW2, Z1), V(X0, YW2, Z1)], 'toprak')
silme(y, [V(X0, YW1), V(X1, YW1)], Z1 - 0.012, 0.014, 0.008, 'kirec', 'tac', kapali=False)
# the upper terrace
duz_duvar(y, V(X1, Y1), V(X0, Y1), Z1, Z2, 'tas_koyu')
poligon_duvar(V(X1, YW2), V(X1, Y1), Z1, Z2, 12, 2, 'kirec', 'tas_koyu', tohum=10)
poligon_duvar(V(X0, Y1), V(X0, YW2), Z1, Z2, 12, 2, 'kirec', 'tas_koyu', tohum=11)
NW = 14
for k in range(NW):            # the upper retaining wall in ashlar bays with buttresses
    p, q = V(X0 + (X1 - X0) * k / NW, YW2), V(X0 + (X1 - X0) * (k + 1) / NW, YW2)
    duz_duvar(y, p, q, Z1, Z2, 'kirec')
    if k: kutu(y, p + V(-0.012, -0.012, Z1), X, 0.024, 0.012, Z2 - Z1 - 0.012, 'kirec', 'onsagsolust')
silme(y, [V(X0, YW2), V(X1, YW2)], Z2 - 0.01, 0.012, 0.008, 'mermer', 'tac', kapali=False)
y.yuz([V(X0, YW2, Z2), V(X1, YW2, Z2), V(X1, Y1, Z2), V(X0, Y1, Z2)], 'toprak')

y.bolum('Poligonal duvar')
poligon_duvar(V(X0, YW1), V(X1, YW1), Z0, Z1 - 0.012, 34, 4, 'kirec', 'tas_koyu')

y.bolum('Kutsal Yol ve rampa')
ZP = Z0 + 0.0015
yol = [V(0.72, Y0 + 0.005), V(0.62, -0.86), V(-0.45, -0.86), V(-0.62, -0.66)]
Lw = disa(yol, -0.07, False); Rw = disa(yol, 0.07, False)
for k in range(len(yol) - 1):
    y.yuz_yon([Rw[k] + Z * ZP, Rw[k + 1] + Z * ZP, Lw[k + 1] + Z * ZP, Lw[k] + Z * ZP], 'zemin', Z)
# the ramp climbing east along the polygonal wall to the temple terrace
RX0, RX1, RY0 = -0.62, 0.86, YW1 - 0.13
y.yuz_yon([V(RX0, RY0, Z0), V(RX1, RY0, Z1), V(RX1, YW1, Z1), V(RX0, YW1, Z0)], 'zemin', Z)
y.yuz_yon([V(RX0, RY0, Z0), V(RX1, RY0, Z0), V(RX1, RY0, Z1)], 'kirec', -Y)
kutu(y, V(RX1, RY0, Z0), X, X1 - RX1, YW1 - RY0, Z1 - Z0, 'kirec', 'onsag')
y.yuz([V(RX1, RY0, Z1), V(X1, RY0, Z1), V(X1, YW1, Z1), V(RX1, YW1, Z1)], 'zemin')
# a low parapet along the ramp's edge with posts
for k in range(12):
    t = k / 11
    xx = RX0 + 0.12 + (RX1 - RX0 - 0.12) * t
    zz = Z0 + (Z1 - Z0) * (xx - RX0) / (RX1 - RX0)
    y.prizma((xx, RY0 + 0.006), 0.004, zz, zz + 0.03, 'mermer', n=6, ust=False)
boru(y, [V(RX0 + 0.12, RY0 + 0.006, Z0 + (Z1 - Z0) * 0.12 / (RX1 - RX0) + 0.03), V(RX1, RY0 + 0.006, Z1 + 0.03), V(X1 - 0.01, RY0 + 0.006, Z1 + 0.03)],
     0.003, 'mermer', n=5)

# ================================================================ lower terrace: treasuries, votive statues
y.bolum('Atinalıların hazinesi')
with parca(y, (-0.72, -0.74, Z0), 0.0):
    hazine(0.2, 0.3, 0.15, 0.011, 'dor')
# the Marathon base beside it with bronze statues
kutu(y, V(-0.6, -0.98, Z0), X, 0.26, 0.05, 0.03, 'kirec', 'onarkasagsolust')
for k in range(4):
    heykel(-0.57 + 0.065 * k, -0.955, Z0 + 0.03, 0.62, 'bronz', kaide=False, aci=-1.2 + 0.4 * k)
y.bolum('Sifnosluların hazinesi')
with parca(y, (0.52, -0.66, Z0), 0.0):
    hazine(0.17, 0.24, 0.13, 0.0105, 'karyatid')
heykel(0.22, -0.68, Z0, 0.9, 'bronz', aci=-1.8)
heykel(0.08, -0.69, Z0, 0.85, 'bronz', aci=-1.2)
# the Naxian sphinx: a tall Ionic column with a seated sphinx
y.bolum('Naksos sfenksi')
NXc = (-0.95, -0.92)
for k, w in enumerate((0.08, 0.064)):
    kutu_merkez(y, NXc, w, w, 0.014, 'kirec', z0=Z0 + 0.014 * k)
kolon(NXc[0], NXc[1], Z0 + 0.028, Z0 + 0.36, 0.016, 'iyon', 'mermer')
with parca(y, (NXc[0], NXc[1], Z0 + 0.36), -0.8, 1.0):
    kutu_merkez(y, (0, 0), 0.05, 0.03, 0.006, 'mermer')
    boru(y, [V(-0.02, 0, 0.018), V(0.012, 0, 0.022)], 0.009, 'mermer', n=7)          # lion body
    for sx in (-0.016, 0.012):
        for sy in (-0.006, 0.006):
            boru(y, [V(sx, sy, 0.014), V(sx + 0.004, sy, 0.006)], 0.003, 'mermer', n=4)
    boru(y, [V(0.012, 0, 0.026), V(0.016, 0, 0.044)], 0.0065, 'mermer', n=7)        # breast and neck
    kure(y, (0.017, 0, 0.052), 0.0075, 'mermer', n=8, kat=4)
    for sy in (-1, 1):   # the curved wings
        boru(y, [V(0.006, sy * 0.008, 0.03), V(-0.006, sy * 0.01, 0.046), V(-0.02, sy * 0.008, 0.058)], 0.004, 'mermer', n=4, r_son=0.002)

# ================================================================ temple terrace
y.bolum('Apollon tapınağı: kaide')
TCx, TCy = 0.02, -0.15
SP = 0.066
TL, TW = SP * 14, SP * 5
PH = 0.035                               # the high base under the steps
pod = dikdortgen(TCx - TL / 2 - 0.1, TCx + TL / 2 + 0.1, TCy - TW / 2 - 0.1, TCy + TW / 2 + 0.1)
duvarlar(y, pod, Z1, Z1 + PH, 'kirec', ust='kirec')
silme(y, pod, Z1, 0.012, 0.007, 'kirec', 'kaide')
silme(y, pod, Z1 + PH - 0.01, 0.01, 0.007, 'mermer', 'tac')
# the ramp up to the east front
xr = TCx + TL / 2 + 0.1
y.yuz_yon([V(xr, TCy - 0.07, Z1 + PH), V(xr + 0.16, TCy - 0.07, Z1), V(xr + 0.16, TCy + 0.07, Z1), V(xr, TCy + 0.07, Z1 + PH)], 'mermer', Z)
for sg in (-1, 1):
    y.yuz_yon([V(xr, TCy + sg * 0.07, Z1), V(xr + 0.16, TCy + sg * 0.07, Z1), V(xr, TCy + sg * 0.07, Z1 + PH)], 'kirec', V(0, sg))
y.bolum('Apollon tapınağı')
with parca(y, (TCx, TCy, 0), math.pi / 2):
    tapinak(TL, TW, 15, 6, Z1 + PH, 0.2, 0.0145, key='mermer', cati='kiremit', basamak=3, sb=0.013)

y.bolum('Sakızlıların sunağı, yılanlı sütun')
AXc, AYc = 0.86, -0.16
kutu_merkez(y, (AXc, AYc), 0.2, 0.12, 0.012, 'bazalt', z0=Z1)
kutu_merkez(y, (AXc, AYc), 0.18, 0.1, 0.05, 'bazalt', z0=Z1 + 0.012)
kornis(y, AXc - 0.09, AXc + 0.09, AYc - 0.05, AYc + 0.05, Z1 + 0.012, 0.01, 0.006, 'mermer', 'kaide')
kornis(y, AXc - 0.09, AXc + 0.09, AYc - 0.05, AYc + 0.05, Z1 + 0.05, 0.014, 0.01, 'mermer', 'tac')
y.yuz([V(AXc - 0.1, AYc - 0.06, Z1 + 0.064), V(AXc + 0.1, AYc - 0.06, Z1 + 0.064), V(AXc + 0.1, AYc + 0.06, Z1 + 0.064), V(AXc - 0.1, AYc + 0.06, Z1 + 0.064)], 'mermer')
merdiven(y, (AXc + 0.13, AYc), math.pi, 0.07, Z1, Z1 + 0.06, n=4, d=0.012, key='mermer')
for s in (-1, 1):
    boru(y, [V(AXc - 0.08, AYc + s * 0.045, Z1 + 0.072), V(AXc + 0.08, AYc + s * 0.045, Z1 + 0.072)], 0.008, 'mermer', n=8)
donel(y, (AXc, AYc), [(0.02, Z1 + 0.064), (0.024, Z1 + 0.074), (0.016, Z1 + 0.09), (0.007, Z1 + 0.102), (0, Z1 + 0.11)], 'boya_sari', n=10)
# the Serpent Column: three bronze snakes twisted round each other, a golden tripod bowl on their heads
SCx, SCy = 0.9, 0.1
kutu_merkez(y, (SCx, SCy), 0.07, 0.07, 0.03, 'kirec', z0=Z1)
kutu_merkez(y, (SCx, SCy), 0.055, 0.055, 0.012, 'mermer', z0=Z1 + 0.03)
zs_ = Z1 + 0.042
for k in range(3):
    pts = [V(SCx + 0.009 * math.cos(TAU * k / 3 + 2.6 * t * 4), SCy + 0.009 * math.sin(TAU * k / 3 + 2.6 * t * 4), zs_ + 0.25 * t) for t in [i / 16 for i in range(17)]]
    boru(y, pts, 0.0045, 'bronz', n=5)
    kure(y, (pts[-1].x * 1.0 + 0.008 * math.cos(TAU * k / 3), pts[-1].y + 0.008 * math.sin(TAU * k / 3), zs_ + 0.255), 0.006, 'bronz', n=6, kat=3)
donel(y, (SCx, SCy), [(0.012, zs_ + 0.26), (0.03, zs_ + 0.27), (0.036, zs_ + 0.29), (0.0, zs_ + 0.29)], 'altin', n=14)
for k in range(3):
    a = TAU * k / 3 + 0.5
    boru(y, [V(SCx + 0.034 * math.cos(a), SCy + 0.034 * math.sin(a), zs_ + 0.29), V(SCx + 0.04 * math.cos(a), SCy + 0.04 * math.sin(a), zs_ + 0.31)],
         0.0028, 'altin', n=4)
sancak(y, 0.7, -0.38, Z1, boy=0.32, en=0.11, yuk=0.07, aci=math.pi * 0.85)
sancak(y, 0.82, Y0 + 0.08, Z0, boy=0.28, en=0.1, yuk=0.065, aci=math.pi * 0.9)
# the Kings of Argos: a semicircular exedra with a bench, its curved back carrying a row of bronze statues
EXc, EXr = (-0.8, -0.12), 0.13
for k in range(12):
    t0, t1 = math.pi * k / 12, math.pi * (k + 1) / 12
    tm = (t0 + t1) / 2
    for rr, w, h, key in ((EXr, 0.03, 0.026, 'mermer'), (EXr + 0.026, 0.022, 0.06, 'kirec')):
        c = (EXc[0] + rr * math.cos(tm), EXc[1] + rr * math.sin(tm))
        kutu_merkez(y, c, w, 2 * (rr + w / 2) * math.sin(math.pi / 24) + 0.001, h, key, z0=Z1, aci=tm)
for k in range(7):
    t = math.pi * (k + 0.5) / 7
    heykel(EXc[0] + (EXr + 0.026) * math.cos(t), EXc[1] + (EXr + 0.026) * math.sin(t), Z1 + 0.06, 0.6, 'bronz', kaide=False, aci=t + math.pi)
for (xx, yy, s_) in ((-0.62, -0.44, 0.9), (-1.0, -0.44, 0.85), (-0.98, 0.18, 0.9)):
    heykel(xx, yy, Z1, s_, 'bronz', aci=-1.0)
# stair to the theatre terrace, cypresses and laurels on the temple terrace
merdiven(y, (0.4, YW2 - 0.12), math.pi / 2, 0.12, Z1, Z2, n=5, d=0.024, key='kirec')
for (xx, yy) in ((-0.78, -0.42), (-0.95, -0.2), (-0.92, 0.05), (0.75, 0.15), (1.02, -0.4), (1.05, 0.12)):
    selvi(xx, yy, Z1, 0.2)
for (xx, yy, b) in ((-0.65, 0.12, 0.15), (0.62, 0.12, 0.13), (-1.06, -0.62, 0.13), (0.95, -0.82, 0.14)):
    cinar(xx, yy, Z1 if yy > YW1 else Z0, b)

# ================================================================ theatre terrace
y.bolum('Tiyatro')
TC = (-0.45, 0.42)
kavea(TC, Z2, 0.17, 0.55, 10, 0.024, -0.06, math.pi + 0.06, 'kirec', n=30, aisle=6, diazoma=6)
y.yuz_yon([V(TC[0] + 0.15 * math.cos(TAU * i / 24), TC[1] + 0.15 * math.sin(TAU * i / 24), Z2 + 0.001) for i in range(24)], 'zemin', Z)
y.yuz_yon([V(TC[0] + 0.12 * math.cos(TAU * i / 24), TC[1] + 0.12 * math.sin(TAU * i / 24), Z2 + 0.0016) for i in range(24)], 'kum_acik', Z)
donel(y, (TC[0], TC[1]), [(0.018, Z2), (0.018, Z2 + 0.025), (0.022, Z2 + 0.03), (0, Z2 + 0.031)], 'mermer', n=10)   # thymele altar
# the stage building: a low colonnaded front between the orchestra and the terrace edge
SKy = YW2 + 0.03
kutu(y, V(TC[0] - 0.24, SKy, Z2), X, 0.48, 0.055, 0.07, 'kirec', 'onsagsol')
for (u0_, u1_) in ((-0.24, -0.13), (-0.07, -0.03), (0.03, 0.07), (0.13, 0.24)):   # the orchestra face between the doors
    duz_duvar(y, V(TC[0] + u1_, SKy + 0.055), V(TC[0] + u0_, SKy + 0.055), Z2, Z2 + 0.07, 'kirec')
y.yuz([V(TC[0] - 0.24, SKy, Z2 + 0.07), V(TC[0] + 0.24, SKy, Z2 + 0.07), V(TC[0] + 0.24, SKy + 0.055, Z2 + 0.07), V(TC[0] - 0.24, SKy + 0.055, Z2 + 0.07)],
      'zemin')
for k in range(9):
    xx = TC[0] - 0.22 + 0.44 * k / 8
    kutu_merkez(y, (xx, SKy + 0.057), 0.014, 0.006, 0.07, 'mermer', z0=Z2)
for k in range(3):
    xx = TC[0] - 0.1 + 0.1 * k
    dikdortgen_acik(y, V(xx + 0.03, SKy + 0.055), V(xx - 0.03, SKy + 0.055), Z2, 0.07, 0.2, 0.8, 0.0, 0.05, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.008)
silme(y, [V(TC[0] - 0.24, SKy), V(TC[0] + 0.24, SKy)], Z2 + 0.06, 0.01, 0.006, 'mermer', 'tac', kapali=False)

y.bolum('Arabacı anıtı, Lesche')
# the charioteer monument: a quadriga with the bronze charioteer on a tall base
CHx, CHy = 0.42, 0.52
kutu_merkez(y, (CHx, CHy), 0.2, 0.12, 0.012, 'mermer', z0=Z2)
kutu_merkez(y, (CHx, CHy), 0.18, 0.1, 0.06, 'kirec', z0=Z2 + 0.012)
kornis(y, CHx - 0.09, CHx + 0.09, CHy - 0.05, CHy + 0.05, Z2 + 0.066, 0.012, 0.008, 'mermer', 'tac')
zq = Z2 + 0.078
for k, dy in enumerate((-0.03, -0.01, 0.01, 0.03)):
    at(CHx + 0.02, CHy + dy, zq, -math.pi * 0.0, 0.7)
for sy in (-1, 1):
    boru(y, [V(CHx - 0.035 + 0.02 * math.cos(TAU * i / 12), CHy + sy * 0.03, zq + 0.02 + 0.02 * math.sin(TAU * i / 12)) for i in range(13)], 0.0022,
         'bronz', n=4, kapat=False)
kutu_merkez(y, (CHx - 0.045, CHy), 0.03, 0.05, 0.025, 'bronz', z0=zq + 0.012)
donel(y, (CHx - 0.045, CHy), [(0.01, zq + 0.03), (0.011, zq + 0.07), (0.007, zq + 0.085), (0, zq + 0.087)], 'bronz', n=8)
kure(y, (CHx - 0.045, CHy, zq + 0.094), 0.0065, 'bronz', n=8, kat=4)
boru(y, [V(CHx - 0.04, CHy - 0.006, zq + 0.075), V(CHx - 0.0, CHy - 0.006, zq + 0.07)], 0.0022, 'bronz', n=4)
# the Lesche of the Knidians: a long hall with painted walls inside, plain outside
LX0_, LX1_, LY0_, LY1_ = 0.5, 1.06, 0.72, 0.9
for a, b in ((V(LX1_, LY0_), V(LX1_, LY1_)), (V(LX1_, LY1_), V(LX0_, LY1_)), (V(LX0_, LY1_), V(LX0_, LY0_))):
    duz_duvar(y, a, b, Z2, Z2 + 0.13, 'kirec')
silme(y, dikdortgen(LX0_, LX1_, LY0_, LY1_), Z2, 0.012, 0.006, 'kirec', 'kaide')
for k in range(4):
    xx = LX0_ + 0.07 + 0.14 * k
    dikdortgen_acik(y, V(xx - 0.07, LY0_), V(xx + 0.07, LY0_), Z2, 0.13, 0.38, 0.62, 0.0 if k == 1 else 0.06, 0.1 if k == 1 else 0.1,
                    ('kirec', 'kirec', 'mermer', 'ahsap' if k == 1 else 'koyu'), derin=0.01, cerceve=(0.005, 'mermer'))
silme(y, dikdortgen(LX0_, LX1_, LY0_, LY1_), Z2 + 0.118, 0.012, 0.008, 'mermer', 'tac')
cati_besik(y, LX0_ - 0.01, LX1_ + 0.01, LY0_ - 0.01, LY1_ + 0.01, Z2 + 0.13, 0.06, 0.02, 'kiremit', ucluk_key='kirec', alinlik_key='mermer', mahya='kiremit2')
kiremit_serit(LX0_ - 0.03, LX1_ + 0.03, LY0_ - 0.03, LY1_ + 0.03, Z2 + 0.13, 0.06, 'x')
for (xx, yy) in ((0.2, 0.62), (0.18, 0.85), (0.3, 0.32), (0.75, 0.35), (1.0, 0.4), (0.95, 0.6), (0.65, 0.62)):
    selvi(xx, yy, Z2, 0.2 + 0.02 * math.sin(xx * 17))
cinar(0.12, 0.35, Z2, 0.15)

y.bolum('Phaedriades kayalıkları')
kayalik(X0, X1, 0.965, Y1, Z2, 30, 0.22, 0.44)

calistir(y, 'lm_delfi')
