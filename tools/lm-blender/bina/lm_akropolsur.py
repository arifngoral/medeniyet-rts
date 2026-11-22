# Acropolis walls (lm_akropolsur): the rock of the Acropolis - a faceted limestone hill - ringed by the ashlar
# circuit wall with merlons, buttresses and square towers; on its west front the Propylaia (a Doric hexastyle hall
# with its gate wall of five doors and the two projecting wings, the Pinakotheke and the south wing) reached by a
# great marble stair; on the bastion to the right the small Ionic Temple of Athena Nike with its sculpted parapet;
# inside, the bronze Athena Promachos, the Erechtheion with its maidens' porch, and the Parthenon in mass only.
import sys, os, math, random
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


def yeniden_ornekle(P, adim):
    """a closed polygon resampled so no edge is longer than adim (corners kept)"""
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        k = max(1, int(math.ceil((b - a).length / adim)))
        out += [a.lerp(b, j / k) for j in range(k)]
    return out


def kaya_kitle(Q, z0, z1, taban, tohum=4, bantlar=(0.0, 0.3, 0.55, 0.8, 1.0), ust_key='kaya'):
    """a rocky hill: the CCW plateau outline Q at z1, its foot taban further out at z0, the slope between in jittered
    faceted bands of bare rock (bulging, with ledges), the plateau top"""
    g = random.Random(tohum)
    n = len(Q)
    alt = disa(Q, taban)
    halka = []
    for k, t in enumerate(bantlar):
        r = []
        for i in range(n):
            p = alt[i].lerp(Q[i], t ** 0.8)
            if 0 < k < len(bantlar) - 1:
                nn = (alt[i] - Q[i]); nn.z = 0
                nn = nn.normalized() if nn.length > 1e-6 else V(0, 0)
                p = p + nn * g.uniform(-0.012, 0.03) + V(g.uniform(-0.008, 0.008), g.uniform(-0.008, 0.008))
                zz = z0 + (z1 - z0) * t + g.uniform(-0.012, 0.012)
            else:
                zz = z0 + (z1 - z0) * t
            r.append(V(p.x, p.y, zz))
        halka.append(r)
    mrk = sum(Q, V(0, 0)) / n
    for k in range(len(bantlar) - 1):
        A, B = halka[k], halka[k + 1]
        for i in range(n):
            j = (i + 1) % n
            q = [A[i], A[j], B[j], B[i]]
            out = (A[i] + A[j]) / 2 - V(mrk.x, mrk.y, 0); out.z = 0; out = out.normalized()   # (away from the plateau's centre: robust for jittered facets)
            key = 'kaya_koyu' if (g.random() < 0.18 or k == 0) else 'kaya'
            if g.random() < 0.5:
                y.yuz_yon([q[0], q[1], q[2]], key, out + Z * 0.3)
                y.yuz_yon([q[0], q[2], q[3]], 'kaya' if (key == 'kaya_koyu' or g.random() < 0.6) else 'kaya_koyu', out + Z * 0.3)
            else:
                y.yuz_yon(q, key, out + Z * 0.3)
    y.yuz_yon([V(p.x, p.y, z1) for p in Q], ust_key, Z)
    # boulders at the foot, shrubs in the clefts
    for i in range(0, n, 2):
        p = alt[i]
        r = g.uniform(0.014, 0.03)
        nn = (alt[i] - Q[i]); nn.z = 0; nn = nn.normalized() if nn.length > 1e-6 else V(0, 0)
        c = p + nn * g.uniform(0.0, 0.02)
        donel(y, (c.x, c.y), [(r, z0), (r * 1.1, z0 + r * 0.5), (r * 0.6, z0 + r), (0, z0 + r * 1.15)], 'kaya' if i % 4 else 'kaya_koyu', n=6, kat=g.random())
        if i % 6 == 2:
            m = halka[1][i].lerp(halka[2][i], 0.5)
            kure(y, (m.x, m.y, m.z + 0.006), g.uniform(0.014, 0.022), 'zeytin' if i % 4 else 'boya_yesil', n=8, kat=4)


def sacak_kapat(x0, x1, y0, y1, z, duvar_x0, duvar_x1, lift=0.0075):
    """the side eaves of a pediment roof (alinlik, ridge along y) from y0 to y1 at height z: the inner side of the fascia
    and a soffit back to the walls at duvar_x0 / duvar_x1"""
    for xe, xw, sg in ((x0, duvar_x0, -1), (x1, duvar_x1, 1)):
        # (the outer fascia is alinlik's own marble edge; only its inner side and the soffit are added)
        xi_ = xe - sg * 0.001     # its inner side (seen past the roof's far edge)
        y.yuz_yon([V(xi_, y0, z), V(xi_, y1, z), V(xi_, y1, z + lift), V(xi_, y0, z + lift)], 'ahsap_koyu', V(-sg, 0))
        y.yuz_yon([V(xe, y0, z), V(xe, y1, z), V(xw, y1, z), V(xw, y0, z)], 'ahsap_koyu', -Z)


def nike_tapinagi(W, L, H, r, key='mermer'):
    """the Temple of Athena Nike at the origin, front -y: a small Ionic amphiprostyle (four columns front and back),
    a cella with a door, a continuous sculpted frieze, pediments, a tiled roof, acroteria. Returns the top z"""
    for k, d in enumerate((0.03, 0.018, 0.008)):
        x0, x1, y0, y1 = -W / 2 - d, W / 2 + d, -L / 2 - d, L / 2 + d
        kutu(y, V(x0, y0, 0.009 * k), X, x1 - x0, y1 - y0, 0.009, key, 'onarkasagsol')
        y.yuz([V(x0, y0, 0.009 * (k + 1)), V(x1, y0, 0.009 * (k + 1)), V(x1, y1, 0.009 * (k + 1)), V(x0, y1, 0.009 * (k + 1))], key)
    zs = 0.027
    zc = zs + H
    cy0, cy1 = -L / 2 + L * 0.27, L / 2 - L * 0.27
    cx = W / 2 - r * 0.6
    duvarlar(y, dikdortgen(-cx, cx, cy0, cy1), zs, zc, key)
    dikdortgen_acik(y, V(-cx, cy0 - 0.0005), V(cx, cy0 - 0.0005), zs, H * 0.999, 0.25, 0.75, 0.0, H * 0.7, (key, key, key, 'bronz'), derin=0.01, cerceve=(0.005, key))
    for yy in (-L / 2, L / 2):
        for k in range(4):
            kolon(-W / 2 + W * k / 3, yy, zs, zc, r, 'iyon', key)
    he = H * 0.3
    k4 = dikdortgen(-W / 2, W / 2, -L / 2, L / 2)
    ze, g = halka_saciklik(k4, zc, he, r * 2.6, key, tur='iyon')
    f = disa(k4, r * 1.3 - 0.003 + 0.0012)
    z1_, z2_ = zc + he * 0.42, zc + he * 0.76
    for i in range(4):
        p, q = f[i], f[(i + 1) % 4]
        Lq = (q - p).length; e = (q - p) / Lq; nn = V(e.y, -e.x)
        y.yuz_yon([p + Z * z1_, q + Z * z1_, q + Z * z2_, p + Z * z2_], 'lacivert', nn)
        m = int(Lq / 0.018)
        for k in range(m):
            c = p + e * (Lq * (k + 0.5) / m) + nn * 0.0012
            hh = (z2_ - z1_) * 0.8
            y.yuz_yon([c - e * 0.0035 + Z * (z1_ + 0.002), c + e * 0.0035 + Z * (z1_ + 0.002), c + e * 0.0025 + Z * (z1_ + hh * 0.78),
                       c - e * 0.0025 + Z * (z1_ + hh * 0.78)], key, nn)
            y.yuz_yon([c - e * 0.0018 + Z * (z1_ + hh * 0.8), c + e * 0.0018 + Z * (z1_ + hh * 0.8), c + e * 0.0018 + Z * (z1_ + hh),
                       c - e * 0.0018 + Z * (z1_ + hh)], key, nn)
    y.yuz_yon([V(-W / 2, -L / 2, zc), V(W / 2, -L / 2, zc), V(W / 2, L / 2, zc), V(-W / 2, L / 2, zc)], 'ahsap_koyu', -Z)
    xa, xb, ya, yb = g[0].x, g[1].x, g[0].y, g[2].y
    ph = (xb - xa) * 0.16
    alinlik(y, V(xa, ya), V(xb, ya), ze, ph, derin=yb - ya - 0.003, key=key, ic_key='boya_kirmizi', c=0.007, cati_key='kiremit')
    alinlik(y, V(xb, yb), V(xa, yb), ze, ph, derin=0.003, key=key, ic_key='boya_kirmizi', c=0.007, cati_key='kiremit')
    kiremit_serit(xa, xb, ya + 0.006, yb - 0.006, ze + 0.0056, ph, 'y', adim=0.022)
    cubuk(y, V(0, ya, ze + ph + 0.009), V(0, yb, ze + ph + 0.009), 0.008, 'kiremit2')
    for yy, sg in ((ya, -1), (yb, 1)):
        heykel(0, yy - sg * 0.006, ze + 0.003, 0.28, key, kaide=False)
        donel(y, (0, yy), [(0.0, ze + ph + 0.007), (0.008, ze + ph + 0.011), (0.012, ze + ph + 0.024), (0.007, ze + ph + 0.033), (0, ze + ph + 0.036)],
              'altin', n=8)
        heykel(xa + 0.006, yy, ze, 0.3, 'altin', kaide=False)
        heykel(xb - 0.006, yy, ze, 0.3, 'altin', kaide=False)
    return ze + ph + 0.036


def basit_tapinak(L, W, nl, nw, z0, HC, r, key='mermer'):
    """a temple in mass only (the far Parthenon): steps, plain octagonal columns all round, the cella block, an
    entablature band, pediments and a tiled roof"""
    sx_, sy_ = W / (nw - 1), L / (nl - 1)
    for k in range(3):
        d = r * 2.2 + 0.014 * (2 - k)
        kutu(y, V(-W / 2 - d, -L / 2 - d, z0 + 0.012 * k), X, W + 2 * d, L + 2 * d, 0.012, key, 'onarkasagsol')
        y.yuz([V(-W / 2 - d, -L / 2 - d, z0 + 0.012 * (k + 1)), V(W / 2 + d, -L / 2 - d, z0 + 0.012 * (k + 1)), V(W / 2 + d, L / 2 + d, z0 + 0.012 * (k + 1)),
               V(-W / 2 - d, L / 2 + d, z0 + 0.012 * (k + 1))], key)
    zs = z0 + 0.036
    zc = zs + HC
    pts = [V(-W / 2 + sx_ * i, -L / 2) for i in range(nw - 1)] + [V(W / 2, -L / 2 + sy_ * j) for j in range(nl - 1)] + \
          [V(W / 2 - sx_ * i, L / 2) for i in range(nw - 1)] + [V(-W / 2, L / 2 - sy_ * j) for j in range(nl - 1)]
    for p in pts:
        y.prizma((p.x, p.y), r, zs, zc - HC * 0.06, key, n=8, ust=False)
        kutu_merkez(y, (p.x, p.y), r * 2.6, r * 2.6, HC * 0.06, key, z0=zc - HC * 0.06)
    duvarlar(y, dikdortgen(-W / 2 + sx_ * 0.9, W / 2 - sx_ * 0.9, -L / 2 + sy_ * 1.2, L / 2 - sy_ * 1.2), zs, zc, 'kirec')
    he = HC * 0.27
    k4 = dikdortgen(-W / 2, W / 2, -L / 2, L / 2)
    ze, g = halka_saciklik(k4, zc, he, r * 2.6, key, sayilar=((nw - 1) * 2, (nl - 1) * 2, (nw - 1) * 2, (nl - 1) * 2))
    xa, xb, ya, yb = g[0].x, g[1].x, g[0].y, g[2].y
    ph = (xb - xa) * 0.13
    alinlik(y, V(xa, ya), V(xb, ya), ze, ph, derin=yb - ya - 0.003, key=key, ic_key='boya_kirmizi', c=0.009, cati_key='kiremit')
    alinlik(y, V(xb, yb), V(xa, yb), ze, ph, derin=0.003, key=key, ic_key='boya_kirmizi', c=0.009, cati_key='kiremit')
    cubuk(y, V(0, ya, ze + ph + 0.011), V(0, yb, ze + ph + 0.011), 0.01, 'kiremit2')
    return ze + ph


# ================================================================ ground and the rock
y.bolum('Zemin')
X0, X1, Y0, Y1 = -1.15, 1.15, -1.12, 1.12
zemin(y, X0, X1, Y0, Y1, Z0, 'tas_koyu', ust='toprak', basamak=(('on', 0.5),), n_basamak=3)
ZT = 0.36                                  # the plateau
P = [V(-1.0, -0.3), V(-0.6, -0.46), V(0.48, -0.46), V(0.8, -0.38), V(1.03, -0.1), V(1.05, 0.48), V(0.88, 0.9), V(0.3, 1.0), V(-0.38, 0.98),
     V(-0.92, 0.84), V(-1.04, 0.3)]
y.bolum('Kayalık tepe')
Q = yeniden_ornekle([V(p.x, p.y) for p in disa(P, 0.014)], 0.09)
kaya_kitle(Q, Z0, ZT, 0.1, tohum=4)
# the path up the slope to the stair, olive trees and cypresses at the foot
ZP = Z0 + 0.0015
y.yuz([V(-0.18, Y0 + 0.005, ZP), V(0.18, Y0 + 0.005, ZP), V(0.2, -0.98, ZP), V(-0.2, -0.98, ZP)], 'zemin')
for k, (xx, yy) in enumerate(((-0.75, -0.95), (-1.02, -0.62), (-0.45, -0.9), (0.98, -0.75), (0.35, -1.0), (-1.05, -1.0))):
    if k % 2: selvi(xx, yy, Z0, 0.2)
    else: cinar(xx, yy, Z0, 0.15)

# ================================================================ the walls
y.bolum('Surlar')
duvar = [V(0.52, -0.46), V(0.8, -0.38), V(1.03, -0.1), V(1.05, 0.48), V(0.88, 0.9), V(0.3, 1.0), V(-0.38, 0.98), V(-0.92, 0.84), V(-1.04, 0.3),
         V(-1.0, -0.3), V(-0.6, -0.46), V(-0.56, -0.46)]
HS = 0.13
sur(y, duvar, ZT, HS, kalinlik=0.05, key='kirec', kapali=False, mazgal_h=0.03, parapet_h=0.014, ust_key='zemin')
# string course and the foot moulding along the wall's outer face
silme(y, duvar, ZT, 0.016, 0.008, 'kirec', 'kaide', kapali=False)
silme(y, duvar, ZT + HS * 0.55, 0.008, 0.005, 'kirec', 'duz', kapali=False)
# buttresses on the long north (back) and south stretches
for i in range(len(duvar) - 1):
    a, b = duvar[i], duvar[i + 1]
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    m = int(L / 0.22)
    for k in range(1, m):
        p = a + e * (L * k / m)
        kutu(y, p - e * 0.016 + nc * 0.022 + Z * ZT, e, 0.032, 0.022, HS * 0.8, 'kirec', 'onsagsolust')
y.bolum('Kuleler')
for (cx, cy, w) in ((-1.0, -0.3, 0.15), (1.03, -0.1, 0.14), (0.88, 0.9, 0.14), (-0.92, 0.84, 0.14)):
    kule_kare(y, cx, cy, w, ZT, HS + 0.08, key='kirec', cati='duz', mazgal_h=0.03, yarik_say=2, konsol=False)
sancak(y, -1.0, -0.3, ZT + HS + 0.08 + 0.042, boy=0.2, en=0.1, yuk=0.065, aci=-math.pi * 0.6)
sancak(y, 1.03, -0.1, ZT + HS + 0.08 + 0.042, boy=0.2, en=0.1, yuk=0.065, aci=-math.pi * 0.4)

# ================================================================ Propylaia
y.bolum('Propylaia: merdiven')
ZPS = ZT + 0.03                    # stylobate of the central hall
PFY = -0.47                        # its front column line
SX = 0.25
NS = 18
merdiven(y, (0, -1.0), math.pi / 2, 2 * SX - 0.02, Z0, ZT, n=NS, d=(PFY - 0.06 + 1.0) / NS, key='mermer')
for s in (-1, 1):                  # the stair's side walls with a coping
    x = s * SX
    y.yuz_yon([V(x, -1.0, Z0), V(x, PFY - 0.06, Z0), V(x, PFY - 0.06, ZT + 0.03), V(x, -1.0, Z0 + 0.03)], 'kirec', V(s, 0))
    y.yuz_yon([V(x - s * 0.02, -1.0, Z0), V(x - s * 0.02, PFY - 0.06, Z0), V(x - s * 0.02, PFY - 0.06, ZT + 0.03), V(x - s * 0.02, -1.0, Z0 + 0.03)],
              'kirec', V(-s, 0))
    y.yuz_yon([V(x, -1.0, Z0 + 0.03), V(x, PFY - 0.06, ZT + 0.03), V(x - s * 0.02, PFY - 0.06, ZT + 0.03), V(x - s * 0.02, -1.0, Z0 + 0.03)], 'mermer', Z)
    y.yuz_yon([V(x, -1.0, Z0), V(x - s * 0.02, -1.0, Z0), V(x - s * 0.02, -1.0, Z0 + 0.03), V(x, -1.0, Z0 + 0.03)], 'mermer', -Y)
# the landing and the steps up to the hall
kutu(y, V(-SX, PFY - 0.06, ZT - 0.04), X, 2 * SX, 0.06, 0.04, 'mermer', 'onsagsol')
y.yuz([V(-SX, PFY - 0.06, ZT), V(SX, PFY - 0.06, ZT), V(SX, PFY + 0.02, ZT), V(-SX, PFY + 0.02, ZT)], 'mermer')
for k in range(2):
    kutu(y, V(-SX, PFY - 0.035 + 0.012 * k, ZT + 0.015 * k), X, 2 * SX, 0.2, 0.015, 'mermer', 'onsagsol')
    y.yuz([V(-SX, PFY - 0.035 + 0.012 * k, ZT + 0.015 * (k + 1)), V(SX, PFY - 0.035 + 0.012 * k, ZT + 0.015 * (k + 1)),
           V(SX, PFY - 0.035 + 0.012 * k + 0.2, ZT + 0.015 * (k + 1)), V(-SX, PFY - 0.035 + 0.012 * k + 0.2, ZT + 0.015 * (k + 1))], 'mermer')
y.bolum('Propylaia: orta salon')
HCp, Rp = 0.2, 0.016
XC = [-0.215, -0.135, -0.058, 0.058, 0.135, 0.215]
PBY = -0.14                        # the east portico's column line
for xx in XC:
    kolon(xx, PFY, ZPS, ZPS + HCp, Rp, 'dor', 'mermer')
    kolon(xx, PBY, ZPS, ZPS + HCp * 0.86, Rp * 0.92, 'dor', 'mermer')
for yy in (PFY + 0.055, PFY + 0.11):        # inner Ionic columns flanking the central passage
    for s in (-1, 1):
        kolon(s * 0.058, yy, ZPS, ZPS + HCp + HCp * 0.27 * 0.4, Rp * 0.8, 'iyon', 'mermer')
# side walls (both faces), the gate wall with five doors
for s in (-1, 1):
    x = s * SX
    duz_duvar(y, V(x, PFY) if s > 0 else V(x, PBY), V(x, PBY) if s > 0 else V(x, PFY), ZPS, ZPS + HCp + 0.022, 'mermer')
    duz_duvar(y, V(x - s * 0.02, PBY) if s > 0 else V(x - s * 0.02, PFY), V(x - s * 0.02, PFY) if s > 0 else V(x - s * 0.02, PBY), ZPS, ZPS + HCp, 'mermer')
    y.yuz_yon([V(x, PFY, ZPS), V(x - s * 0.02, PFY, ZPS), V(x - s * 0.02, PFY, ZPS + HCp), V(x, PFY, ZPS + HCp)], 'mermer', -Y)
    y.yuz_yon([V(x, PBY, ZPS), V(x - s * 0.02, PBY, ZPS), V(x - s * 0.02, PBY, ZPS + HCp + 0.022), V(x, PBY, ZPS + HCp + 0.022)], 'mermer', Y)
GY = PFY + 0.18
for (x0, x1, h) in ((-0.23, -0.13, 0.09), (-0.13, -0.05, 0.12), (-0.05, 0.05, 0.16), (0.05, 0.13, 0.12), (0.13, 0.23, 0.09)):
    dikdortgen_acik(y, V(x0, GY), V(x1, GY), ZPS, HCp, 0.2, 0.8, 0.0, h, ('mermer', 'mermer', 'mermer', 'koyu' if h > 0.15 else 'bronz'), derin=0.012,
                    cerceve=(0.005, 'mermer'))
duz_duvar(y, V(-SX + 0.02, GY), V(-0.23, GY), ZPS, ZPS + HCp, 'mermer')
for (x0, x1, h) in ((-0.23, -0.13, 0.09), (-0.13, -0.05, 0.12), (-0.05, 0.05, 0.16), (0.05, 0.13, 0.12), (0.13, 0.23, 0.09)):   # the gate wall's east face
    dikdortgen_acik(y, V(x1, GY + 0.02), V(x0, GY + 0.02), ZPS, HCp, 0.2, 0.8, 0.0, h, ('mermer', 'mermer', 'mermer', 'koyu' if h > 0.15 else 'bronz'),
                    derin=0.008, cerceve=(0.005, 'mermer'))
duz_duvar(y, V(-0.23, GY + 0.02), V(-SX + 0.02, GY + 0.02), ZPS, ZPS + HCp, 'mermer')
duz_duvar(y, V(SX - 0.02, GY + 0.02), V(0.23, GY + 0.02), ZPS, ZPS + HCp, 'mermer')
duz_duvar(y, V(0.23, GY), V(SX - 0.02, GY), ZPS, ZPS + HCp, 'mermer')
y.yuz_yon([V(-SX, PFY, ZPS + HCp + 0.02), V(SX, PFY, ZPS + HCp + 0.02), V(SX, PBY, ZPS + HCp + 0.02), V(-SX, PBY, ZPS + HCp + 0.02)], 'ahsap_koyu', -Z)
y.yuz([V(-SX, PFY + 0.02, ZPS), V(SX, PFY + 0.02, ZPS), V(SX, PBY + 0.03, ZPS), V(-SX, PBY + 0.03, ZPS)], 'mermer')
kutu(y, V(-SX, PFY + 0.02, ZT), X, 2 * SX, PBY - PFY + 0.01, ZPS - ZT, 'mermer', 'arkasagsol')
y.bolum('Propylaia: saçaklık ve alınlıklar')
he = HCp * 0.27
ZE = saciklik(V(-0.215, PFY), V(0.215, PFY), ZPS + HCp, he, Rp * 2.6, 'dor', 'mermer', uz=SX - 0.215 + 0.004, n_tri=10, metop='boya_kirmizi')
zb_ = ZPS + HCp * 0.86
ZEb = saciklik(V(0.215, PBY), V(-0.215, PBY), zb_, he * 0.86, Rp * 2.4, 'dor', 'mermer', uz=SX - 0.215 + 0.004, n_tri=10, metop='boya_kirmizi')
for s in (-1, 1):                 # side entablature bands joining the porticoes
    duz_duvar(y, V(s * SX, PFY) if s > 0 else V(s * SX, PBY), V(s * SX, PBY) if s > 0 else V(s * SX, PFY), ZPS + HCp + 0.022, ZE, 'mermer')
alinlik(y, V(-SX - 0.016, PFY - 0.035), V(SX + 0.016, PFY - 0.035), ZE, 0.075, derin=PBY - PFY + 0.035, key='mermer', ic_key='boya_kirmizi', c=0.01,
        cati_key='kiremit')
kiremit_serit(-SX - 0.016, SX + 0.016, PFY - 0.03, PBY + 0.0, ZE + 0.008, 0.075, 'y')
sacak_kapat(-SX - 0.016, SX + 0.016, PFY - 0.035, PBY, ZE, -SX, SX, 0.008)
y.yuz_yon([V(-SX - 0.016, PBY, ZE), V(SX + 0.016, PBY, ZE), V(0, PBY, ZE + 0.075)], 'mermer', Y)
for p_, q_ in ((V(-SX - 0.016, PBY, ZE), V(0, PBY, ZE + 0.075)), (V(0, PBY, ZE + 0.075), V(SX + 0.016, PBY, ZE))):
    y.yuz_yon([p_, q_, q_ + Z * 0.008, p_ + Z * 0.008], 'mermer', Y)     # close the gap under the roof's back end
y.yuz_yon([V(-SX, PBY, ZEb), V(SX, PBY, ZEb), V(SX, PBY, ZE), V(-SX, PBY, ZE)], 'mermer', Y)     # the step between the two roofs
# the lower east pediment (the eastern hall's roof)
alinlik(y, V(SX + 0.014, PBY + 0.03), V(-SX - 0.014, PBY + 0.03), ZEb, 0.065, derin=0.08, key='mermer', ic_key='boya_kirmizi', c=0.009, cati_key='kiremit')
sacak_kapat(-SX - 0.014, SX + 0.014, PBY - 0.05, PBY + 0.03, ZEb, -SX, SX, 0.0072)
cubuk(y, V(0, PFY - 0.035, ZE + 0.086), V(0, PBY, ZE + 0.086), 0.011, 'kiremit2')
donel(y, (0, PFY - 0.035), [(0.0, ZE + 0.075), (0.012, ZE + 0.08), (0.017, ZE + 0.098), (0.011, ZE + 0.11), (0, ZE + 0.114)], 'altin', n=8)
for s in (-1, 1):
    amfora(s * (SX + 0.004), PFY - 0.03, ZE, 0.8, 'altin')

y.bolum('Propylaia: kanatlar')
WY0, WY1 = -0.66, -0.44
for s, (xi, xo) in ((-1, (-0.27, -0.56)), (1, (0.27, 0.5))):
    xa_, xb_ = min(xi, xo), max(xi, xo)
    # the tall ashlar podium standing on the slope
    kutu(y, V(xa_, WY0, Z0), X, xb_ - xa_, WY1 - WY0, ZPS - Z0, 'kirec', 'onsagsol' if s < 0 else 'onsagsol')
    y.yuz([V(xa_, WY0, ZPS), V(xb_, WY0, ZPS), V(xb_, WY1, ZPS), V(xa_, WY1, ZPS)], 'mermer')
    for zz in (Z0 + 0.08, Z0 + 0.16):
        silme(y, [V(xa_, WY0), V(xb_, WY0)], zz, 0.008, 0.005, 'kirec', 'duz', kapali=False)
    silme(y, dikdortgen(xa_, xb_, WY0, WY1), ZPS - 0.014, 0.014, 0.008, 'mermer', 'tac')
    # the wing: a porch of three Doric columns facing the stair, the room behind
    xc = xi + s * 0.03
    xw = xi + s * 0.085
    for k in range(3):
        kolon(xc, WY0 + 0.02 + (WY1 - WY0 - 0.04) * k / 2, ZPS, ZPS + 0.15, 0.0125, 'dor', 'mermer')
    room = dikdortgen(min(xw, xo + (-s) * 0.0), max(xw, xo), WY0 + 0.005, WY1 - 0.005)
    rx0, rx1 = min(xw, xo), max(xw, xo)
    # front (facing -y): two windows (the Pinakotheke), sides plain, the porch-side wall with a door
    for (u0, u1) in ((0.0, 0.5), (0.5, 1.0)):
        a = V(rx0 + (rx1 - rx0) * u0, WY0 + 0.005); b = V(rx0 + (rx1 - rx0) * u1, WY0 + 0.005)
        dikdortgen_acik(y, a, b, ZPS, 0.15, 0.3, 0.7, 0.05, 0.11, ('mermer', 'mermer', 'mermer', 'koyu'), derin=0.01, cerceve=(0.005, 'mermer'))
    duz_duvar(y, V(rx1, WY0 + 0.005), V(rx1, WY1 - 0.005), ZPS, ZPS + 0.15, 'mermer') if s > 0 else \
        dikdortgen_acik(y, V(rx1, WY0 + 0.005), V(rx1, WY1 - 0.005), ZPS, 0.15, 0.3, 0.7, 0.0, 0.1, ('mermer', 'mermer', 'mermer', 'ahsap'), derin=0.01)
    duz_duvar(y, V(rx1, WY1 - 0.005), V(rx0, WY1 - 0.005), ZPS, ZPS + 0.15, 'mermer')
    duz_duvar(y, V(rx0, WY1 - 0.005), V(rx0, WY0 + 0.005), ZPS, ZPS + 0.15, 'mermer') if s < 0 else \
        dikdortgen_acik(y, V(rx0, WY1 - 0.005), V(rx0, WY0 + 0.005), ZPS, 0.15, 0.3, 0.7, 0.0, 0.1, ('mermer', 'mermer', 'mermer', 'ahsap'), derin=0.01)
    zw = saciklik(V(xc, WY1 - 0.02) if s < 0 else V(xc, WY0 + 0.02), V(xc, WY0 + 0.02) if s < 0 else V(xc, WY1 - 0.02), ZPS + 0.15, 0.04, 0.032, 'dor',
                  'mermer', uz=0.022, n_tri=6, metop='boya_kirmizi')
    pc0, pc1 = min(xw, xi + s * 0.012), max(xw, xi + s * 0.012)      # the porch ceiling (the rooms are closed)
    y.yuz_yon([V(pc0, WY0 + 0.007, ZPS + 0.15), V(pc1, WY0 + 0.007, ZPS + 0.15), V(pc1, WY1 - 0.007, ZPS + 0.15), V(pc0, WY1 - 0.007, ZPS + 0.15)], 'ahsap_koyu', -Z)
    for a, b in ((V(rx0, WY0 + 0.005), V(rx1, WY0 + 0.005)), (V(rx1, WY1 - 0.005), V(rx0, WY1 - 0.005))):
        duz_duvar(y, a, b, ZPS + 0.15, zw, 'mermer')
    duz_duvar(y, V(xo, WY0 + 0.005) if s > 0 else V(xo, WY1 - 0.005), V(xo, WY1 - 0.005) if s > 0 else V(xo, WY0 + 0.005), ZPS + 0.15, zw, 'mermer')
    for yy_, sg_ in ((WY0 + 0.005, -1), (WY1 - 0.005, 1)):     # the porch's end walls (antae) up to the roof
        xa2, xb2 = min(xi + s * 0.012, xw), max(xi + s * 0.012, xw)
        duz_duvar(y, V(xa2, yy_) if sg_ < 0 else V(xb2, yy_), V(xb2, yy_) if sg_ < 0 else V(xa2, yy_), ZPS + 0.142, zw, 'mermer')
    xr_ = xi + s * 0.012                # the roof stops short of the central hall (its eave clears the hall's wall)
    xa_, xb_ = min(xr_, xo), max(xr_, xo)
    duz_duvar(y, V(xr_, WY0 + 0.005) if s < 0 else V(xr_, WY1 - 0.005), V(xr_, WY1 - 0.005) if s < 0 else V(xr_, WY0 + 0.005), ZPS + 0.142, zw,
              'mermer')          # closes the space over the porch ceiling on the hall's side
    cati_kirma(y, xa_, xb_, WY0 + 0.005, WY1 - 0.005, zw, 0.05, 0.02, 'kiremit', mahya='kiremit2')

# ================================================================ Nike bastion and temple
y.bolum('Nike burcu')
NX0, NX1, NY0, NY1 = 0.5, 0.8, -0.9, -0.52
ZN = ZT - 0.01
kutu(y, V(NX0, NY0, Z0), X, NX1 - NX0, NY1 - NY0, ZN - Z0, 'kirec', 'onarkasagsol')
y.yuz([V(NX0, NY0, ZN), V(NX1, NY0, ZN), V(NX1, NY1, ZN), V(NX0, NY1, ZN)], 'zemin')
silme(y, dikdortgen(NX0, NX1, NY0, NY1), Z0, 0.02, 0.01, 'kirec', 'kaide')
for zz in (Z0 + 0.09, Z0 + 0.18):
    silme(y, dikdortgen(NX0, NX1, NY0, NY1), zz, 0.008, 0.005, 'kirec', 'duz')
# the parapet of carved slabs (Nike adjusting her sandal) on three sides
par = [V(NX0, NY1), V(NX0, NY0), V(NX1, NY0), V(NX1, NY1)]
parapet(y, par, ZN, 0.035, 0, kalinlik=0.01, key='mermer', kapali=False)
for i in range(3):
    a, b = par[i], par[i + 1]
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    m = int(L / 0.035)
    for k in range(m):
        c = a + e * (L * (k + 0.5) / m) + nc * 0.0012
        y.yuz_yon([c - e * 0.005 + Z * (ZN + 0.006), c + e * 0.005 + Z * (ZN + 0.006), c + e * 0.004 + Z * (ZN + 0.024), c - e * 0.004 + Z * (ZN + 0.024)],
                  'kirec', nc)
        kure(y, (c.x, c.y, ZN + 0.028), 0.0035, 'kirec', n=6, kat=3)
y.bolum('Athena Nike tapınağı')
with parca(y, ((NX0 + NX1) / 2, (NY0 + NY1) / 2 - 0.01, ZN), 0.0):
    nike_tapinagi(0.13, 0.2, 0.115, 0.0095)
# a little stair from the bastion up to the south wing
merdiven(y, (0.52, -0.5), math.pi, 0.06, ZN, ZPS, n=3, d=0.012, key='mermer')

# ================================================================ inside: Promachos, Erechtheion and Parthenon in mass
y.bolum('Athena Promakhos')
AX_, AY_ = -0.12, 0.1
kutu_merkez(y, (AX_, AY_), 0.11, 0.11, 0.015, 'mermer', z0=ZT)
kutu_merkez(y, (AX_, AY_), 0.085, 0.085, 0.07, 'kirec', z0=ZT + 0.015)
kornis(y, AX_ - 0.0425, AX_ + 0.0425, AY_ - 0.0425, AY_ + 0.0425, ZT + 0.08, 0.012, 0.008, 'mermer', 'tac')
zh = ZT + 0.092
donel(y, (AX_, AY_), [(0.024, zh), (0.026, zh + 0.06), (0.019, zh + 0.14), (0.021, zh + 0.18), (0.014, zh + 0.2), (0.008, zh + 0.205)], 'bronz', n=12)
kure(y, (AX_, AY_, zh + 0.222), 0.012, 'bronz', n=10, kat=5)
boru(y, [V(AX_, AY_, zh + 0.232), V(AX_ - 0.006, AY_ + 0.004, zh + 0.252)], 0.005, 'bronz', n=5, r_son=0.002)          # helmet crest
boru(y, [V(AX_ + 0.03, AY_ - 0.01, zh), V(AX_ + 0.03, AY_ - 0.01, zh + 0.3)], 0.003, 'bronz', n=5)                      # spear
donel(y, (AX_ + 0.03, AY_ - 0.01), [(0.006, zh + 0.3), (0.0, zh + 0.33)], 'altin', n=6)
boru(y, [V(AX_ + 0.012, AY_ - 0.012, zh + 0.15), V(AX_ + 0.03, AY_ - 0.014, zh + 0.16)], 0.005, 'bronz', n=5)
with parca(y, (AX_ - 0.03, AY_ - 0.008, zh + 0.1), -math.pi / 2 - 0.3):          # the shield
    donel(y, (0, 0), [(0.0, 0.0), (0.035, 0.004), (0.04, 0.008), (0.0, 0.012)], 'bronz', n=14)
y.yuz([V(AX_ - 0.03, -0.42, ZT + 0.001), V(AX_ + 0.03, -0.42, ZT + 0.001), V(0.3, 0.38, ZT + 0.001), V(0.24, 0.38, ZT + 0.001)], 'zemin')
y.bolum('Erekhtheion')
EX0, EX1, EY0, EY1 = -0.7, -0.38, 0.38, 0.6
for a, b in ((V(EX1, EY0), V(EX1, EY1)), (V(EX1, EY1), V(EX0, EY1)), (V(EX0, EY1), V(EX0, EY0))):
    duz_duvar(y, a, b, ZT, ZT + 0.15, 'mermer')
silme(y, dikdortgen(EX0, EX1, EY0, EY1), ZT, 0.012, 0.006, 'mermer', 'kaide')
for k in range(4):
    dikdortgen_acik(y, V(EX0 + 0.08 * k, EY0), V(EX0 + 0.08 * (k + 1), EY0), ZT, 0.15, 0.3, 0.7, 0.06, 0.12,
                    ('mermer', 'mermer', 'mermer', 'koyu'), derin=0.008)
ze_e, g_e = halka_saciklik(dikdortgen(EX0, EX1, EY0, EY1), ZT + 0.15, 0.04, 0.02, 'mermer', tur='iyon')
cati_besik(y, g_e[0].x, g_e[1].x, g_e[0].y, g_e[2].y, ze_e, 0.045, 0.012, 'kiremit', ucluk_key='mermer', alinlik_key='mermer', mahya='kiremit2')
# the east porch (six Ionic columns) and the Porch of the Maidens on the south side
for k in range(6):
    kolon(EX1 + 0.05, EY0 + 0.01 + (EY1 - EY0 - 0.02) * k / 5, ZT, ZT + 0.15, 0.009, 'iyon', 'mermer')
kutu(y, V(EX1, EY0 - 0.01, ZT + 0.15), X, 0.065, EY1 - EY0 + 0.02, 0.03, 'mermer', 'onarkasagsolust')
kutu(y, V(EX0 + 0.05, EY0 - 0.09, ZT), X, 0.12, 0.09, 0.05, 'mermer', 'onsagsolust')
for k in range(4):
    kore(EX0 + 0.065 + 0.03 * k, EY0 - 0.075, ZT + 0.05, ZT + 0.13, 0.75)
for k in range(2):
    kore(EX0 + 0.065 + 0.09 * k, EY0 - 0.04, ZT + 0.05, ZT + 0.13, 0.75)
kutu(y, V(EX0 + 0.045, EY0 - 0.095, ZT + 0.13), X, 0.13, 0.095, 0.022, 'mermer', 'onsagsolust')
zeytin(EX0 - 0.08, EY0 - 0.06, ZT, 0.12, 0.9, 2)        # Athena's sacred olive
y.bolum('Parthenon')
with parca(y, (0.48, 0.68, 0), math.pi / 2):
    tapinak(0.5, 0.21, 17, 8, ZT, 0.13, 0.0088, key='mermer', cati='kiremit', basamak=3, sb=0.011)
y.bolum('Eski Athena tapınağının temelleri')
# the foundations of the Old Temple of Athena between the Erechtheion and the Parthenon: a stepped platform, broken
# column stumps of its peristyle, the low cella walls, fallen drums
OX, OY, OL, OW = -0.06, 0.52, 0.32, 0.15
for k, d in enumerate((0.02, 0.008)):
    kutu(y, V(OX - OL / 2 - d, OY - OW / 2 - d, ZT + 0.011 * k), X, OL + 2 * d, OW + 2 * d, 0.011, 'kirec', 'onarkasagsol')
    y.yuz([V(OX - OL / 2 - d, OY - OW / 2 - d, ZT + 0.011 * (k + 1)), V(OX + OL / 2 + d, OY - OW / 2 - d, ZT + 0.011 * (k + 1)),
           V(OX + OL / 2 + d, OY + OW / 2 + d, ZT + 0.011 * (k + 1)), V(OX - OL / 2 - d, OY + OW / 2 + d, ZT + 0.011 * (k + 1))], 'kirec' if k == 0 else 'mermer')
zo = ZT + 0.022
_go = random.Random(13)
for i in range(12):
    for yy in (OY - OW / 2 + 0.012, OY + OW / 2 - 0.012):
        if _go.random() < 0.3: continue
        kolon(OX - OL / 2 + 0.012 + (OL - 0.024) * i / 11, yy, zo, zo + _go.uniform(0.015, 0.07), 0.0082, 'dor', 'mermer')
for j in range(1, 5):
    for xx in (OX - OL / 2 + 0.012, OX + OL / 2 - 0.012):
        if _go.random() < 0.4: continue
        kolon(xx, OY - OW / 2 + 0.012 + (OW - 0.024) * j / 5, zo, zo + _go.uniform(0.015, 0.06), 0.0082, 'dor', 'mermer')
for (x0_, x1_, y0_, y1_) in ((OX - 0.11, OX + 0.11, OY - 0.045, OY - 0.037), (OX - 0.11, OX + 0.11, OY + 0.037, OY + 0.045),
                             (OX - 0.11, OX - 0.102, OY - 0.037, OY + 0.037), (OX + 0.03, OX + 0.038, OY - 0.037, OY + 0.037)):
    kutu(y, V(x0_, y0_, zo), X, x1_ - x0_, y1_ - y0_, 0.018, 'kirec', 'onarkasagsolust')
for (xx, yy, a_) in ((OX + 0.2, OY - 0.11, 0.3), (OX + 0.06, OY - 0.1, -0.2), (OX - 0.22, OY + 0.1, 1.2)):
    e_ = V(math.cos(a_), math.sin(a_))
    boru(y, [V(xx, yy, ZT + 0.008) - e_ * 0.018, V(xx, yy, ZT + 0.008) + e_ * 0.018], 0.008, 'mermer', n=10)
# the Brauronion stoa against the south wall: a Doric front with a lean-to roof
BX, BY0, BY1 = 0.8, -0.2, 0.32
for k in range(9):
    kolon(BX, BY0 + (BY1 - BY0) * k / 8, ZT, ZT + 0.12, 0.009, 'dor', 'mermer')
zb2 = saciklik(V(BX, BY1), V(BX, BY0), ZT + 0.12, 0.032, 0.024, 'dor', 'mermer', uz=0.016, n_tri=16, metop='boya_kirmizi')
duz_duvar(y, V(0.97, BY0 - 0.016), V(0.97, BY1 + 0.016), ZT, zb2 + 0.0437, 'kirec')
y.yuz_yon([V(0.975, BY0 - 0.03, zb2 + 0.036), V(0.975, BY1 + 0.03, zb2 + 0.036), V(0.975, BY1 + 0.03, zb2 + 0.045), V(0.975, BY0 - 0.03, zb2 + 0.045)], 'ahsap_koyu', X)   # the roof's back edge
for yy, sg in ((BY0 - 0.016, -1), (BY1 + 0.016, 1)):
    y.yuz_yon([V(BX - 0.012, yy, ZT), V(0.97, yy, ZT), V(0.97, yy, zb2 + 0.04), V(BX - 0.012, yy, zb2)], 'kirec', V(0, sg))
    y.yuz_yon([V(BX - 0.012, yy - sg * 0.012, ZT), V(0.97, yy - sg * 0.012, ZT), V(0.97, yy - sg * 0.012, zb2 + 0.04), V(BX - 0.012, yy - sg * 0.012, zb2)], 'kirec', V(0, -sg))
    y.yuz_yon([V(BX - 0.012, yy, ZT), V(BX - 0.012, yy - sg * 0.012, ZT), V(BX - 0.012, yy - sg * 0.012, zb2), V(BX - 0.012, yy, zb2)], 'kirec', -X)
y.yuz_yon([V(BX - 0.03, BY0 - 0.03, zb2), V(BX - 0.03, BY1 + 0.03, zb2), V(0.975, BY1 + 0.03, zb2 + 0.045), V(0.975, BY0 - 0.03, zb2 + 0.045)], 'kiremit', Z)
y.yuz_yon([V(BX - 0.03, BY0 - 0.03, zb2), V(BX - 0.03, BY1 + 0.03, zb2), V(BX - 0.03, BY1 + 0.03, zb2 - 0.008), V(BX - 0.03, BY0 - 0.03, zb2 - 0.008)],
          'ahsap_koyu', -X)
y.yuz_yon([V(BX - 0.029, BY0 - 0.03, zb2), V(BX - 0.029, BY1 + 0.03, zb2), V(BX - 0.029, BY1 + 0.03, zb2 - 0.008), V(BX - 0.029, BY0 - 0.03, zb2 - 0.008)],
          'ahsap_koyu', X)     # the fascia's inner side
for k in range(21):
    yy = BY0 - 0.025 + (BY1 - BY0 + 0.05) * k / 20
    kiremit_kaburga(V(BX - 0.03, yy, zb2 + 0.0015), V(0.975, yy, zb2 + 0.0465))
y.yuz_yon([V(BX + 0.012, BY0, ZT + 0.12 + 0.012), V(0.97, BY0, ZT + 0.132), V(0.97, BY1, ZT + 0.132), V(BX + 0.012, BY1, ZT + 0.132)], 'ahsap_koyu', -Z)
for k in range(5):
    yy = BY0 + 0.05 + (BY1 - BY0 - 0.1) * k / 4
    dikdortgen_acik(y, V(0.9699, yy + 0.035), V(0.9699, yy - 0.035), ZT, 0.12, 0.25, 0.75, 0.0, 0.085, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.008)
# the paved courts, bedrock outcrops
for (x0_, x1_, y0_, y1_) in ((-0.3, 0.2, -0.32, -0.1), (0.05, 0.75, 0.28, 0.4), (-0.75, -0.3, 0.25, 0.34)):
    y.yuz([V(x0_, y0_, ZT + 0.0012), V(x1_, y0_, ZT + 0.0012), V(x1_, y1_, ZT + 0.0012), V(x0_, y1_, ZT + 0.0012)], 'zemin')
_g = random.Random(21)
for k in range(10):
    xx, yy_ = _g.uniform(-0.85, 0.7), _g.uniform(-0.25, 0.85)
    if (-0.75 < xx < -0.3 and 0.25 < yy_ < 0.65) or (0.15 < xx < 0.8 and 0.4 < yy_ < 0.95) or abs(xx - AX_) < 0.1 and abs(yy_ - AY_) < 0.1: continue
    r = _g.uniform(0.03, 0.06)
    donel(y, (xx, yy_), [(r, ZT - 0.002), (r * 0.8, ZT + 0.008), (r * 0.4, ZT + 0.013), (0, ZT + 0.014)], 'kaya_koyu' if k % 3 == 0 else 'kaya', n=7, kat=_g.random())
# votive statues and an altar on the rock
for (xx, yy, s_) in ((0.25, -0.2, 0.9), (-0.45, -0.15, 0.85), (-0.7, 0.05, 0.9), (0.6, -0.12, 0.85), (0.0, 0.32, 0.8), (0.38, 0.33, 0.8), (-0.25, -0.33, 0.8)):
    heykel(xx, yy, ZT, s_, 'bronz', aci=-1.2)
# the great altar of Athena: a stepped base, the altar with a cornice and volute bolsters, the fire
AL_ = (0.17, 0.3)
for k, (w, d) in enumerate(((0.17, 0.11), (0.15, 0.09))):
    kutu_merkez(y, AL_, w, d, 0.01, 'mermer', z0=ZT + 0.01 * k)
kutu_merkez(y, AL_, 0.12, 0.065, 0.04, 'kirec', z0=ZT + 0.02)
kornis(y, AL_[0] - 0.06, AL_[0] + 0.06, AL_[1] - 0.0325, AL_[1] + 0.0325, ZT + 0.056, 0.01, 0.007, 'mermer', 'tac')
for s_ in (-1, 1):
    boru(y, [V(AL_[0] - 0.05, AL_[1] + s_ * 0.026, ZT + 0.072), V(AL_[0] + 0.05, AL_[1] + s_ * 0.026, ZT + 0.072)], 0.007, 'mermer', n=8)
y.yuz_yon([V(AL_[0] - 0.04, AL_[1] - 0.0331, ZT + 0.03), V(AL_[0] + 0.04, AL_[1] - 0.0331, ZT + 0.03), V(AL_[0] + 0.04, AL_[1] - 0.0331, ZT + 0.048),
           V(AL_[0] - 0.04, AL_[1] - 0.0331, ZT + 0.048)], 'boya_kirmizi', -Y)
donel(y, AL_, [(0.014, ZT + 0.066), (0.018, ZT + 0.074), (0.012, ZT + 0.086), (0.005, ZT + 0.096), (0, ZT + 0.104)], 'boya_sari', n=10)
for (xx, yy) in ((-0.85, 0.55), (-0.25, 0.75), (0.85, 0.3), (-0.8, -0.15)):
    selvi(xx, yy, ZT, 0.17)

calistir(y, 'lm_akropolsur')
