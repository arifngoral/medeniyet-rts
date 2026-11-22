# Athenian Agora (lm_agora): the two-storey Stoa of Attalos along the east side (Doric below, Ionic gallery above,
# an inner Ionic row, a row of shop rooms behind, tiled gable roof, the outside stair at its end), the earthen square
# crossed by the paved Panathenaic Way with market stalls, the Altar of the Twelve Gods, statues and plane trees, the
# round Tholos, a Doric fountain house, and the Hephaisteion (a small Doric peripteros) high on its rocky hill behind.
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


# ================================================================ platform, square, Panathenaic Way
y.bolum('Meydan zemini ve Panathenaia yolu')
X0, X1, Y0, Y1 = -1.15, 1.17, -1.02, 1.06
zemin(y, X0, X1, Y0, Y1, Z0, 'tas_koyu', ust='toprak', basamak=(('on', 0.5), ('sol', 0.4)), n_basamak=3)
ZP = Z0 + 0.0015
# the paved way, crossing the square diagonally from the front-left gate to the back
yol = [V(-0.45, Y0 + 0.01), V(-0.1, -0.35), V(0.25, 0.3), V(0.42, Y1 - 0.01)]
L_ = disa(yol, -0.085, False); R_ = disa(yol, 0.085, False)
KL = disa(yol, -0.1, False); KR = disa(yol, 0.1, False)
for k in range(len(yol) - 1):
    y.yuz_yon([R_[k] + Z * ZP, R_[k + 1] + Z * ZP, L_[k + 1] + Z * ZP, L_[k] + Z * ZP], 'zemin', Z)
    y.yuz_yon([L_[k] + Z * ZP, L_[k + 1] + Z * ZP, KL[k + 1] + Z * ZP, KL[k] + Z * ZP], 'kirec', Z)
    y.yuz_yon([KR[k] + Z * ZP, KR[k + 1] + Z * ZP, R_[k + 1] + Z * ZP, R_[k] + Z * ZP], 'kirec', Z)

# ================================================================ Stoa of Attalos
y.bolum('Attalos Stoası: alt kat Dor revak')
SX, SB = 0.62, 1.10            # front column line, back wall (inner face)
SY0, SY1 = -0.80, 0.90         # column line ends
SE0, SE1 = -0.86, 0.96         # end walls (outer faces)
ZS = Z0 + 0.03
H1, HE1 = 0.17, 0.046
H2, HE2 = 0.135, 0.038
R1 = 0.0135
# stylobate: two steps along the front
for k, (dx, hh) in enumerate(((0.05, 0.015), (0.03, 0.03))):
    kutu(y, V(SX - dx, SE0, Z0), X, SB + 0.05 - SX + dx, SE1 - SE0, hh, 'mermer', 'onarkasagsol')
    y.yuz([V(SX - dx, SE0, Z0 + hh), V(SB + 0.05, SE0, Z0 + hh), V(SB + 0.05, SE1, Z0 + hh), V(SX - dx, SE1, Z0 + hh)], 'mermer' if k else 'kirec')
NB = 18
for i in range(NB + 1):
    yy = SY0 + (SY1 - SY0) * i / NB
    kolon(SX, yy, ZS, ZS + H1, R1, 'dor', 'mermer')
# the inner Ionic row
for i in range(NB // 2 + 1):
    yy = SY0 + (SY1 - SY0) * i / (NB // 2)
    kolon((SX + SB) / 2 + 0.01, yy, ZS, ZS + H1 + HE1 * 0.4, R1 * 0.9, 'iyon', 'mermer')
Z2 = saciklik(V(SX, SY1), V(SX, SY0), ZS + H1, HE1, R1 * 2.6, 'dor', 'mermer', uz=SY0 - SE0 - 0.004, metop='boya_kirmizi', n_tri=NB * 2)
# lower ceiling with beams, the upper floor
ZL = ZS + H1 + HE1 * 0.4
y.yuz_yon([V(SX + R1 * 1.3, SE0, ZL), V(SB, SE0, ZL), V(SB, SE1, ZL), V(SX + R1 * 1.3, SE1, ZL)], 'ahsap_koyu', -Z)
for i in range(NB + 1):
    yy = SY0 + (SY1 - SY0) * i / NB
    cubuk(y, V(SX + R1 * 1.3, yy, ZL - 0.003), V(SB, yy, ZL - 0.003), 0.008, 'ahsap', 0.006)
y.yuz_yon([V(SX + R1 * 1.3, SE0, Z2), V(SB, SE0, Z2), V(SB, SE1, Z2), V(SX + R1 * 1.3, SE1, Z2)], 'zemin', Z)

y.bolum('Attalos Stoası: dükkânlar')
NS = 14
for i in range(NS):
    a = V(SB, SE1 - 0.01 - (SE1 - SE0 - 0.02) * i / NS); b = V(SB, SE1 - 0.01 - (SE1 - SE0 - 0.02) * (i + 1) / NS)
    Wd, e_, nc_, Ld = dikdortgen_acik(y, a, b, ZS, ZL - ZS, 0.3, 0.7, 0.0, 0.105, ('siva_krem', 'kirec', 'kirec', 'koyu' if i % 3 else 'ahsap'),
                                      derin=0.016, cerceve=(0.006, 'mermer'))
    # a small window over each door, wares in front of some
    y.pencere(Ld(0.42, 0.13), e_, nc_, 0, 0, Wd * 0.16, 0.022, 'koyu', kemer=False)
    if i % 3 == 1:
        for k in range(3):
            amfora(Ld(0.16 + 0.05 * k, 0).x - 0.02, Ld(0.16 + 0.05 * k, 0).y, ZS, 1.0, 'siva_oker' if k % 2 else 'kirmizi')
silme(y, [V(SB, SE1), V(SB, SE0)], ZS, 0.012, 0.004, 'mermer', 'kaide', kapali=False)
# outer back wall (east face), plain ashlar with small high windows in two rows
TB = 0.035
ZTOP = Z2 + H2 + HE2
for i in range(NS):
    a = V(SB + TB, SE0 + (SE1 - SE0) * i / NS); b = V(SB + TB, SE0 + (SE1 - SE0) * (i + 1) / NS)
    # each bay: a recessed slit window in each storey, framed; a pilaster strip at the bay's edge
    dikdortgen_acik(y, a, b, Z0, Z2 - Z0, 0.4, 0.6, ZS + 0.07 - Z0, ZS + 0.13 - Z0, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.01,
                    cerceve=(0.004, 'mermer'))
    dikdortgen_acik(y, a, b, Z2, ZTOP - Z2, 0.4, 0.6, 0.04, 0.1, ('kirec', 'kirec', 'mermer', 'koyu'), derin=0.01, cerceve=(0.004, 'mermer'))
    if i:
        kutu(y, a + V(0.005, -0.009, Z0), Y, 0.018, 0.005, ZTOP - Z0 - 0.002, 'kirec', 'onsagsol')
silme(y, [V(SB + TB, SE0), V(SB + TB, SE1)], Z0, 0.02, 0.008, 'kirec', 'kaide', kapali=False)
silme(y, [V(SB + TB, SE0), V(SB + TB, SE1)], Z2 - 0.012, 0.014, 0.008, 'kirec', 'tac', kapali=False)

y.bolum('Attalos Stoası: üst kat İyon galeri')
for i in range(NB + 1):
    yy = SY0 + (SY1 - SY0) * i / NB
    kolon(SX, yy, Z2, Z2 + H2, R1 * 0.82, 'iyon', 'mermer')
# balustrade panels between the upper columns (both faces, a coping)
for i in range(NB):
    ya_ = SY0 + (SY1 - SY0) * i / NB + R1; yb_ = SY0 + (SY1 - SY0) * (i + 1) / NB - R1
    kutu(y, V(SX + 0.006, yb_, Z2), -Y, yb_ - ya_, 0.012, 0.045, 'mermer', 'onarkaust')
    y.yuz_yon([V(SX - 0.0062, ya_ + 0.008, Z2 + 0.008), V(SX - 0.0062, yb_ - 0.008, Z2 + 0.008), V(SX - 0.0062, yb_ - 0.008, Z2 + 0.037),
               V(SX - 0.0062, ya_ + 0.008, Z2 + 0.037)], 'kirec', -X)
Z3 = saciklik(V(SX, SY1), V(SX, SY0), Z2 + H2, HE2, R1 * 2.3, 'iyon', 'mermer', uz=SY0 - SE0 - 0.004)
# upper rooms: doors and windows on the back wall, the ceiling
for i in range(NS):
    a = V(SB, SE1 - 0.01 - (SE1 - SE0 - 0.02) * i / NS); b = V(SB, SE1 - 0.01 - (SE1 - SE0 - 0.02) * (i + 1) / NS)
    dikdortgen_acik(y, a, b, Z2, Z2 + H2 + HE2 * 0.4 - Z2, 0.33, 0.67, 0.0, 0.09, ('siva_krem', 'kirec', 'kirec', 'koyu' if i % 2 else 'ahsap'),
                    derin=0.014, cerceve=(0.005, 'mermer'))
ZU = Z2 + H2 + HE2 * 0.4
y.yuz_yon([V(SX + R1, SE0, ZU), V(SB, SE0, ZU), V(SB, SE1, ZU), V(SX + R1, SE1, ZU)], 'ahsap_koyu', -Z)
duz_duvar(y, V(SB, SE1 - 0.01), V(SB, SE1), ZS, ZU, 'siva_krem'); duz_duvar(y, V(SB, SE0), V(SB, SE0 + 0.01), ZS, ZU, 'siva_krem')
duz_duvar(y, V(SB, SE0), V(SB, SE1), ZU, Z3, 'kirec')

y.bolum('Attalos Stoası: uç duvarlar, dış merdiven')
for yy, sg in ((SE0, -1), (SE1, 1)):
    ti = 0.05
    yi = yy - sg * ti
    kose = [V(SX - R1 * 1.5, yy), V(SB + TB, yy)] if sg < 0 else [V(SB + TB, yy), V(SX - R1 * 1.5, yy)]
    # outer face: a door below, a window above, a raised anta pilaster at the front corner
    a, b = kose
    dikdortgen_acik(y, a, b, ZS, ZL - ZS, *((0.1, 0.24) if sg < 0 else (0.55, 0.75)), 0.0, 0.12, ('kirec', 'kirec', 'mermer', 'ahsap'), derin=0.016, cerceve=(0.007, 'mermer'))
    duz_duvar(y, a, b, Z0, ZS, 'mermer')
    dikdortgen_acik(y, a, b, ZL, Z3 - ZL, *((0.8, 0.92, Z2 - ZL + 0.002, Z2 - ZL + 0.1) if sg < 0 else (0.4, 0.6, 0.05, 0.13)), ('kirec', 'kirec', 'mermer', 'ahsap' if sg < 0 else 'koyu'), derin=0.016, cerceve=(0.006, 'mermer'))
    silme(y, [a, b], Z2 - 0.012, 0.014, 0.008, 'mermer', 'tac', kapali=False)
    # inner face, the front edge
    duz_duvar(y, V(SB, yi) if sg < 0 else V(SX - R1 * 1.5, yi), V(SX - R1 * 1.5, yi) if sg < 0 else V(SB, yi), ZS, Z3, 'siva_krem')
    y.yuz_yon([V(SX - R1 * 1.5, yy, Z0), V(SX - R1 * 1.5, yi, Z0), V(SX - R1 * 1.5, yi, Z3), V(SX - R1 * 1.5, yy, Z3)], 'kirec', -X)
    kutu(y, V(SX - R1 * 1.5 - 0.006, yy - sg * 0.0, Z0) if sg < 0 else V(SX - R1 * 1.5 - 0.006 + 0.03, yy, Z0), X if sg < 0 else -X, 0.03,
         0.006 if sg < 0 else -0.006, Z3 - Z0, 'mermer', 'onarkasagsol')
# the outside stair at the south end, up to the gallery, with a parapet
ys = SE0 - 0.031
merdiven(y, (0.745, ys), 0.0, 0.058, Z0, Z2, n=14, d=0.0225, key='kirec')
kutu(y, V(0.745 + 14 * 0.0225, ys - 0.029, Z0), X, SB + TB - 0.745 - 14 * 0.0225, 0.06, Z2 - Z0, 'kirec', 'onsagsolust')
for k in range(8):      # a balustrade of posts and a rail on the stair's outer edge
    t = (k + 0.5) / 8
    xx = 0.745 + 14 * 0.0225 * t; zz = Z0 + (Z2 - Z0) * t
    y.prizma((xx, ys - 0.026), 0.0025, zz, zz + 0.035, 'mermer', n=5, ust=False)
boru(y, [V(0.745, ys - 0.026, Z0 + 0.035), V(0.745 + 14 * 0.0225, ys - 0.026, Z2 + 0.035), V(SB + TB, ys - 0.026, Z2 + 0.035)], 0.0028, 'mermer', n=5)

y.bolum('Attalos Stoası: çatı')
cati_besik(y, SX - R1 * 3.5, SB + TB, SE0, SE1, Z3, 0.085, 0.022, 'kiremit', ucluk_key='kirec', alinlik_key='mermer', mahya='kiremit2',
           uc_sacak=0.012)
kiremit_serit(SX - R1 * 3.5 - 0.022, SB + TB + 0.022, SE0, SE1, Z3, 0.085, 'y')
for yy in (SE0 - 0.012, SE1 + 0.012):   # acroteria on the gable apexes
    donel(y, ((SX - R1 * 3.5 + SB + TB) / 2, yy), [(0.0, Z3 + 0.09), (0.012, Z3 + 0.094), (0.016, Z3 + 0.11), (0.01, Z3 + 0.122), (0, Z3 + 0.126)],
          'altin', n=8)
sancak(y, (SX + SB) / 2 + 0.02, SE0 - 0.012, Z3 + 0.12, boy=0.16, en=0.1, yuk=0.06, aci=math.pi * 0.85)
sancak(y, (SX + SB) / 2 + 0.02, SE1 + 0.012, Z3 + 0.12, boy=0.16, en=0.1, yuk=0.06, aci=math.pi * 0.9)

# ================================================================ Hephaisteion on its hill
y.bolum('Agoraios tepesi')
HX0, HX1, HY0, HY1 = -1.12, -0.1, 0.32, 1.03
ZH = Z0 + 0.23


def tepe(alt, ust, z0, z1, key='toprak', n=3, key_ust='cimen'):
    """a battered rocky mound between two CCW outlines (same number of corners), in n bands, a grassy top"""
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n
        ra = [V(p.x + (q.x - p.x) * t0, p.y + (q.y - p.y) * t0, z0 + (z1 - z0) * t0) for p, q in zip(alt, ust)]
        rb = [V(p.x + (q.x - p.x) * t1, p.y + (q.y - p.y) * t1, z0 + (z1 - z0) * t1) for p, q in zip(alt, ust)]
        y.serit(ra, rb, key if k % 2 == 0 else 'kum_koyu')
    y.yuz_yon([V(p.x, p.y, z1) for p in ust], key_ust, Z)


alt = [V(HX0, HY0 - 0.02), V(HX1 - 0.08, HY0 - 0.04), V(HX1 + 0.02, HY0 + 0.12), V(HX1, HY1 - 0.1), V(HX1 - 0.1, HY1), V(HX0, HY1)]
ust = [V(HX0 + 0.02, HY0 + 0.07), V(HX1 - 0.14, HY0 + 0.06), V(HX1 - 0.08, HY0 + 0.16), V(HX1 - 0.09, HY1 - 0.12), V(HX1 - 0.16, HY1 - 0.04),
       V(HX0 + 0.02, HY1 - 0.04)]
tepe(alt, ust, Z0, ZH)
# rock outcrops and a polygonal retaining wall along the front
for (xx, yy, r) in ((-0.95, 0.36, 0.05), (-0.62, 0.33, 0.04), (-0.33, 0.33, 0.045), (-0.17, 0.5, 0.04), (-0.15, 0.78, 0.05), (-0.8, 0.35, 0.03)):
    donel(y, (xx, yy), [(r, Z0), (r * 1.05, Z0 + r * 0.6), (r * 0.7, Z0 + r * 1.2), (0, Z0 + r * 1.4)], 'granit', n=7, kat=xx * 7)
for (xx, yy) in ((-1.05, 0.95), (-0.25, 0.9), (-1.05, 0.42), (-0.2, 0.42)):
    selvi(xx, yy, ZH - 0.004 if abs(xx) > 0.3 else ZH - 0.004, 0.16)
# rocks and shrubs scattered over the slopes
import random as _r
_g = _r.Random(7)
for i in range(len(alt)):
    p, q = alt[i], alt[(i + 1) % len(alt)]
    pu, qu = ust[i], ust[(i + 1) % len(ust)]
    L = (q - p).length
    for k in range(int(L / 0.07)):
        u = (k + 0.5) / int(L / 0.07); t = _g.uniform(0.25, 0.75)
        a = p.lerp(q, u); b = pu.lerp(qu, u)
        c = a.lerp(b, t); zc = Z0 + (ZH - Z0) * t
        if abs(c.x + 0.5) < 0.1 and c.y < HY0 + 0.1: continue      # keep the stair clear
        if k % 2 == 0:
            r = _g.uniform(0.012, 0.022)
            donel(y, (c.x, c.y), [(r, zc - r * 0.5), (r * 1.1, zc + r * 0.2), (r * 0.6, zc + r * 0.8), (0, zc + r)], 'granit' if k % 4 else 'tas_koyu', n=6,
                  kat=_g.uniform(0, 1))
        else:
            kure(y, (c.x, c.y, zc + 0.008), _g.uniform(0.012, 0.018), 'cimen' if k % 3 else 'boya_yesil', n=8, kat=4)
# the stair up from the square
merdiven(y, (-0.5, HY0 - 0.17), math.pi / 2, 0.11, Z0, ZH, n=15, d=0.016, key='kirec', yanlik='tas')
kutu(y, V(-0.555, HY0 + 0.07, Z0), X, 0.11, 0.06, ZH - Z0, 'kirec', 'sagsol')
y.yuz([V(-0.555, HY0 + 0.072, ZH + 0.0005), V(-0.445, HY0 + 0.072, ZH + 0.0005), V(-0.445, HY0 + 0.13, ZH + 0.0005), V(-0.555, HY0 + 0.13, ZH + 0.0005)],
      'kirec')

y.bolum('Hephaistos tapınağı')
with parca(y, (-0.62, 0.66, 0), -math.pi / 2):
    tapinak(0.66, 0.29, 11, 6, ZH, 0.165, 0.0125, key='mermer', cati='kiremit')

# ================================================================ Tholos
y.bolum('Tholos')
TC = (-0.82, -0.12)
TR = 0.13
for k, (rr, hh) in enumerate(((TR + 0.035, 0.012), (TR + 0.02, 0.024))):
    y.prizma(TC, rr, Z0, Z0 + hh, 'mermer', n=32)
ZT = Z0 + 0.024
ring = cokgen(TC, TR, 24)
pencereli_duvar(y, ring, ZT, 0.13, [1 if i in (5, 11, 17, 23) else 0 for i in range(24)], renk=('kirec', 'tas_koyu', 'mermer', 'koyu'),
                v0=0.06, en=0.45, ust=0.03, derin=0.012, k_say=6)
silme(y, ring, ZT, 0.012, 0.006, 'mermer', 'kaide')
silme(y, ring, ZT + 0.13 - 0.016, 0.016, 0.014, 'mermer', 'tac')
# a porch on the east (towards the square)
with parca(y, (TC[0] + TR - 0.01, TC[1], 0), math.pi / 2):
    kutu(y, V(-0.07, -0.06, Z0), X, 0.14, 0.06, 0.024, 'mermer', 'onsagsol')
    y.yuz([V(-0.07, -0.06, Z0 + 0.024), V(0.07, -0.06, Z0 + 0.024), V(0.07, 0.0, Z0 + 0.024), V(-0.07, 0.0, Z0 + 0.024)], 'mermer')
    for xx in (-0.05, 0.05):
        kolon(xx, -0.04, ZT, ZT + 0.11, 0.009, 'dor', 'mermer')
    zp = saciklik(V(-0.05, -0.04), V(0.05, -0.04), ZT + 0.11, 0.03, 0.02, 'dor', 'mermer', uz=0.015, n_tri=4)
    alinlik(y, V(-0.068, -0.052), V(0.068, -0.052), zp, 0.035, derin=0.068, key='mermer', ic_key='boya_kirmizi', c=0.007, cati_key='kiremit')
    Wd, e_, nc_, Ld = dikdortgen_acik(y, V(-0.035, 0.0), V(0.035, 0.0), ZT, 0.1, 0.2, 0.8, 0.0, 0.085, ('kirec', 'kirec', 'mermer', 'ahsap'), derin=0.01)
# the conical tiled roof with radial cover-tile ribs and a finial
ZTr = ZT + 0.13
donel(y, TC, [(TR + 0.03, ZTr), (TR + 0.03, ZTr + 0.006), (TR * 0.5, ZTr + 0.07), (0.018, ZTr + 0.098), (0, ZTr + 0.1)], 'kiremit', n=32)
y.yuz_yon([V(p.x, p.y, ZTr) for p in cokgen(TC, TR + 0.03, 32)], 'ahsap_koyu', -Z)
for i in range(32):
    a = TAU * (i + 0.5) / 32
    d = V(math.cos(a), math.sin(a))
    p0 = V(TC[0], TC[1], 0) + d * (TR + 0.03) + Z * (ZTr + 0.0075)
    p1 = V(TC[0], TC[1], 0) + d * 0.024 + Z * (ZTr + 0.097)
    kiremit_kaburga(p0, p1, 0.006)
donel(y, TC, [(0.02, ZTr + 0.096), (0.022, ZTr + 0.106), (0.012, ZTr + 0.12), (0.016, ZTr + 0.13), (0, ZTr + 0.142)], 'bronz', n=10)

# ================================================================ fountain house
y.bolum('Çeşme evi')
FX, FY = -0.86, -0.76
with parca(y, (FX, FY, 0), 0.0):
    FW, FD = 0.26, 0.26
    kutu(y, V(-FW / 2 - 0.025, -FD / 2 - 0.03, Z0), X, FW + 0.05, FD + 0.045, 0.02, 'mermer', 'onarkasagsol')
    y.yuz([V(-FW / 2 - 0.025, -FD / 2 - 0.03, Z0 + 0.02), V(FW / 2 + 0.025, -FD / 2 - 0.03, Z0 + 0.02), V(FW / 2 + 0.025, FD / 2 + 0.015, Z0 + 0.02),
           V(-FW / 2 - 0.025, FD / 2 + 0.015, Z0 + 0.02)], 'mermer')
    zf = Z0 + 0.02
    HF = 0.15
    PD = 0.085                                   # porch depth
    # the water room behind (walls with a pilaster at each corner), a porch of four Doric columns in front (-y)
    duvarlar(y, dikdortgen(-FW / 2, FW / 2, -FD / 2 + PD, FD / 2), zf, zf + HF, 'kirec')
    for xx, yy in ((-FW / 2, FD / 2), (FW / 2, FD / 2)):
        kutu_merkez(y, (xx, yy), 0.022, 0.022, HF, 'mermer', z0=zf, yuzler='onarkasagsol')
    for xx in (-0.09, -0.03, 0.03, 0.09):
        kolon(xx, -FD / 2, zf, zf + HF, 0.0105, 'dor', 'mermer')
    for s in (-1, 1):   # antae
        kutu(y, V(s * FW / 2 - (0.022 if s > 0 else 0), -FD / 2 - 0.008, zf), X, 0.022, PD + 0.008, HF, 'kirec', 'onsagsol')
    for (xa_, xb_, ya_, yb_) in ((-FW / 2, FW / 2, -FD / 2, -FD / 2 + PD),):
        zfe = saciklik(V(-FW / 2 + 0.011, -FD / 2), V(FW / 2 - 0.011, -FD / 2), zf + HF, 0.04, 0.026, 'dor', 'mermer', uz=0.012, n_tri=8)
    # entablature along the sides and back (plain band at the same height)
    for a, b in ((V(FW / 2, -FD / 2 + 0.013), V(FW / 2, FD / 2)), (V(FW / 2, FD / 2), V(-FW / 2, FD / 2)), (V(-FW / 2, FD / 2), V(-FW / 2, -FD / 2 + 0.013))):
        duz_duvar(y, a, b, zf + HF, zfe, 'kirec')
    silme(y, [V(FW / 2, -FD / 2 + 0.013), V(FW / 2, FD / 2), V(-FW / 2, FD / 2), V(-FW / 2, -FD / 2 + 0.013)], zfe - 0.012, 0.012, 0.01, 'mermer', 'tac', kapali=False)
    y.yuz_yon([V(-FW / 2, -FD / 2, zf + HF), V(FW / 2, -FD / 2, zf + HF), V(FW / 2, -FD / 2 + PD, zf + HF), V(-FW / 2, -FD / 2 + PD, zf + HF)],
              'ahsap_koyu', -Z)
    # the draw basin across the porch, lion-head spouts on the water room's wall, water running down
    havuz(y, -FW / 2 + 0.03, FW / 2 - 0.03, -FD / 2 + PD - 0.035, -FD / 2 + PD - 0.008, zf + 0.014, kenar=0.007)
    duvarlar(y, disa(dikdortgen(-FW / 2 + 0.03, FW / 2 - 0.03, -FD / 2 + PD - 0.035, -FD / 2 + PD - 0.008), 0.007), zf, zf + 0.0145, 'mermer')   # the basin's skirt
    for xx in (-0.07, 0.0, 0.07):
        yw = -FD / 2 + PD
        kutu_merkez(y, (xx, yw - 0.002), 0.03, 0.004, 0.03, 'mermer', z0=zf + 0.06)
        kure(y, (xx, yw - 0.006, zf + 0.075), 0.008, 'bronz', n=8, kat=4)
        boru(y, [V(xx, yw - 0.012, zf + 0.072), V(xx, yw - 0.02, zf + 0.06), V(xx, yw - 0.021, zf + 0.026)], 0.0022, 'su', n=4)
    # the pediment and roof
    alinlik(y, V(-FW / 2 - 0.01, -FD / 2 - 0.014), V(FW / 2 + 0.01, -FD / 2 - 0.014), zfe, 0.045, derin=FD + 0.024, key='mermer',
            ic_key='boya_kirmizi', c=0.008, cati_key='kiremit')
    alinlik(y, V(FW / 2 + 0.01, FD / 2 + 0.01), V(-FW / 2 - 0.01, FD / 2 + 0.01), zfe, 0.045, derin=0.003, key='mermer', ic_key='kirec', c=0.008,
            cati_key='kiremit')
    kiremit_serit(-FW / 2 - 0.01, FW / 2 + 0.01, -FD / 2 - 0.008, FD / 2 + 0.004, zfe + 0.0064, 0.045, 'y')
    cubuk(y, V(0, -FD / 2 - 0.014, zfe + 0.056), V(0, FD / 2 + 0.01, zfe + 0.056), 0.009, 'kiremit2')
    donel(y, (0, -FD / 2 - 0.014), [(0.0, zfe + 0.05), (0.009, zfe + 0.054), (0.013, zfe + 0.066), (0.008, zfe + 0.076), (0, zfe + 0.079)], 'altin', n=8)
    # a girl's hydria on the step, more on the platform
    for k, (xx, yy) in enumerate(((-0.11, -FD / 2 - 0.022), (0.105, -FD / 2 - 0.02), (-0.03, -FD / 2 + PD - 0.045))):
        amfora(xx, yy, zf if k < 2 else zf, 0.8, 'kirmizi' if k % 2 else 'siva_oker')

# ================================================================ Altar of the Twelve Gods, stalls, statues, trees
y.bolum('On İki Tanrı sunağı')
AX, AY = -0.32, -0.22
AW = 0.24
kutu_merkez(y, (AX, AY), AW + 0.02, AW + 0.02, 0.008, 'mermer', z0=Z0)
y.yuz([V(AX - AW / 2, AY - AW / 2, Z0 + 0.0085), V(AX + AW / 2, AY - AW / 2, Z0 + 0.0085), V(AX + AW / 2, AY + AW / 2, Z0 + 0.0085),
       V(AX - AW / 2, AY + AW / 2, Z0 + 0.0085)], 'zemin')
# the parapet of carved slabs on posts, an opening in front
for i in range(4):
    k4 = dikdortgen(AX - AW / 2, AX + AW / 2, AY - AW / 2, AY + AW / 2)
    p, q = k4[i], k4[(i + 1) % 4]
    e = (q - p).normalized()
    parcs = [(0, 0.38), (0.62, 1)] if i == 0 else [(0, 1)]
    for u0, u1 in parcs:
        a, b = p.lerp(q, u0), p.lerp(q, u1)
        kutu(y, a + Z * (Z0 + 0.008), e, (b - a).length, 0.008, 0.048, 'kirec', 'onarkasagsol')
        silme(y, [a, b], Z0 + 0.05, 0.006, 0.004, 'mermer', 'duz', kapali=False)
        y.yuz_yon([a + Z * (Z0 + 0.056), b + Z * (Z0 + 0.056), b - V(e.y, -e.x) * 0.008 + Z * (Z0 + 0.056), a - V(e.y, -e.x) * 0.008 + Z * (Z0 + 0.056)],
                  'mermer', Z)
    for u in (0, 0.38, 0.62, 1) if i == 0 else (0, 0.5, 1):
        c = p.lerp(q, u)
        kutu_merkez(y, (c.x, c.y), 0.016, 0.016, 0.06, 'mermer', z0=Z0 + 0.008)
# the altar with volute cushions and a fire
kutu_merkez(y, (AX, AY + 0.02), 0.1, 0.07, 0.012, 'mermer', z0=Z0 + 0.008)
kutu_merkez(y, (AX, AY + 0.02), 0.084, 0.054, 0.045, 'kirec', z0=Z0 + 0.02)
kornis(y, AX - 0.042, AX + 0.042, AY + 0.02 - 0.027, AY + 0.02 + 0.027, Z0 + 0.058, 0.01, 0.006, 'mermer', 'tac')
for s in (-1, 1):
    boru(y, [V(AX + s * 0.042, AY - 0.007, Z0 + 0.074), V(AX + s * 0.042, AY + 0.047, Z0 + 0.074)], 0.007, 'mermer', n=8)
donel(y, (AX, AY + 0.02), [(0.012, Z0 + 0.068), (0.016, Z0 + 0.076), (0.011, Z0 + 0.088), (0.005, Z0 + 0.097), (0, Z0 + 0.104)], 'boya_sari', n=10)
# a garland of painted relief on the altar's front
y.yuz_yon([V(AX - 0.03, AY - 0.0071, Z0 + 0.03), V(AX + 0.03, AY - 0.0071, Z0 + 0.03), V(AX + 0.03, AY - 0.0071, Z0 + 0.046), V(AX - 0.03, AY - 0.0071, Z0 + 0.046)],
          'boya_kirmizi', -Y)

y.bolum('Pazar tezgâhları')


def tezgah(x, yy, aci, renk):
    """a market stall: four poles, a striped cloth awning, a counter with amphorae and baskets"""
    with parca(y, (x, yy, 0), aci):
        w, d, h = 0.11, 0.07, 0.085
        for (px, py) in ((-w / 2, -d / 2), (w / 2, -d / 2), (-w / 2, d / 2), (w / 2, d / 2)):
            y.prizma((px, py), 0.0028, Z0, Z0 + h + (0.012 if py > 0 else 0), 'ahsap', n=5, ust=False)
        for k in range(4):   # awning in stripes, sloping to the front
            x0_, x1_ = -w / 2 - 0.008 + (w + 0.016) * k / 4, -w / 2 - 0.008 + (w + 0.016) * (k + 1) / 4
            q = [V(x0_, -d / 2 - 0.012, Z0 + h - 0.004), V(x1_, -d / 2 - 0.012, Z0 + h - 0.004), V(x1_, d / 2 + 0.004, Z0 + h + 0.014),
                 V(x0_, d / 2 + 0.004, Z0 + h + 0.014)]
            y.yuz_yon(q, renk if k % 2 == 0 else 'kumas', Z)
            y.yuz_yon([p - Z * 0.0025 for p in q], 'kumas', -Z)          # the underside, a cloth thickness below
            vl = [q[0], q[1], q[1] - Z * 0.014, q[0] - Z * 0.014]           # the front valance, both faces
            y.yuz_yon(vl, renk if k % 2 == 0 else 'kumas', -Y)
            y.yuz_yon([p + Y * 0.0025 for p in vl], 'kumas', Y)
            if k in (0, 3):                                                  # the cloth's side edge
                xs = x0_ if k == 0 else x1_
                y.yuz_yon([V(xs, q[0].y, q[0].z), V(xs, q[3].y, q[3].z), V(xs, q[3].y, q[3].z - 0.0025), V(xs, q[0].y, q[0].z - 0.0025)],
                          'kumas', V(-1 if k == 0 else 1, 0))
                i0 = 0 if k == 0 else 1                                   # the valance's end cap
                y.yuz_yon([vl[i0], vl[i0] + Y * 0.0025, vl[3 - i0] + Y * 0.0025, vl[3 - i0]], 'kumas', V(-1 if k == 0 else 1, 0))
            y.yuz_yon([q[3], q[2], q[2] - Z * 0.0025, q[3] - Z * 0.0025], 'kumas', Y)   # the back edge
        kutu_merkez(y, (0, -d / 2 + 0.012), w * 0.9, 0.022, 0.034, 'ahsap_acik', z0=Z0)
        for k in range(3):
            amfora(-0.03 + 0.03 * k, d / 2 - 0.012, Z0, 0.9, 'siva_oker' if k != 1 else 'kirmizi')
        for k in range(3):
            donel(y, (-0.03 + 0.03 * k, -d / 2 + 0.012), [(0.0, Z0 + 0.034), (0.008, Z0 + 0.034), (0.011, Z0 + 0.044), (0.0, Z0 + 0.042)],
                  ['saz', 'boya_sari', 'boya_kirmizi'][k], n=8)


for (x, yy, a, r) in ((0.05, -0.73, 0.0, 'boya_kirmizi'), (0.2, -0.75, 0.1, 'lacivert'), (0.36, -0.69, -0.15, 'boya_sari'),
                      (0.3, -0.5, math.pi / 2 + 0.1, 'boya_kirmizi'), (0.3, -0.33, math.pi / 2, 'boya_yesil'), (-0.12, 0.08, 0.3, 'lacivert'),
                      (-0.5, -0.64, 0.25, 'boya_sari'), (0.12, -0.56, -0.1, 'boya_kirmizi')):
    tezgah(x, yy, a, r)

y.bolum('Heykeller, ağaçlar, sancak')
# the Monument of the Eponymous Heroes: a long base with ten bronze heroes, tripods at the ends, a post-and-rail fence
EX, EY, EL = 0.24, -0.945, 0.36
kutu_merkez(y, (EX, EY), EL + 0.02, 0.05, 0.01, 'mermer', z0=Z0)
kutu_merkez(y, (EX, EY), EL, 0.036, 0.042, 'kirec', z0=Z0 + 0.01)
kornis(y, EX - EL / 2, EX + EL / 2, EY - 0.018, EY + 0.018, Z0 + 0.052, 0.008, 0.005, 'mermer', 'tac')
for k in range(10):
    heykel(EX - EL / 2 + 0.03 + (EL - 0.06) * k / 9, EY, Z0 + 0.06, 0.62, 'bronz', kaide=False, aci=-1.4 + 0.3 * (k % 3))
for s_ in (-1, 1):
    xx = EX + s_ * (EL / 2 - 0.004)
    donel(y, (xx, EY), [(0.0, Z0 + 0.06), (0.012, Z0 + 0.062), (0.014, Z0 + 0.075), (0.01, Z0 + 0.08), (0.016, Z0 + 0.092), (0, Z0 + 0.093)], 'bronz', n=8)
fk = dikdortgen(EX - EL / 2 - 0.03, EX + EL / 2 + 0.03, EY - 0.042, EY + 0.042)
for i in range(4):
    p_, q_ = fk[i], fk[(i + 1) % 4]
    n_ = max(2, int((q_ - p_).length / 0.05))
    for k in range(n_):
        c_ = p_.lerp(q_, k / n_)
        kutu_merkez(y, (c_.x, c_.y), 0.008, 0.008, 0.032, 'mermer', z0=Z0)
    cubuk(y, p_ + Z * (Z0 + 0.026), q_ + Z * (Z0 + 0.026), 0.004, 'mermer', 0.004)
heykel(0.05, -0.12, Z0, 1.15, 'bronz', aci=-1.0)
heykel(0.42, 0.42, Z0, 1.0, 'bronz', aci=2.4)
heykel(-0.6, -0.48, Z0, 1.0, 'bronz', aci=0.3)
# herms along the way (square pillars with a head)
for (x, yy) in ((-0.58, -0.92), (-0.36, -0.92), (0.16, 0.12), (0.34, 0.12)):
    kutu_merkez(y, (x, yy), 0.016, 0.016, 0.06, 'mermer', z0=Z0)
    kure(y, (x, yy, Z0 + 0.068), 0.009, 'mermer', n=8, kat=4)
for (x, yy, b) in ((0.48, -0.15, 0.2), (0.5, 0.2, 0.19), (0.47, 0.6, 0.2), (-0.05, 0.5, 0.18), (0.1, 0.85, 0.2), (-0.55, -0.05, 0.17),
                   (0.25, 0.95, 0.17), (-1.04, -0.42, 0.17), (-0.66, 0.2, 0.15)):
    cinar(x, yy, Z0, b)
sancak(y, -0.32, -0.34, Z0, boy=0.3, en=0.11, yuk=0.07, aci=-0.4)

calistir(y, 'lm_agora')
