# Shared helpers for the Korean landmarks (lm_ambaravlu, lm_okculukpavyon, lm_bulguksa, lm_hwaseong): the Korean
# tiled roof (paljak / ujingak / matbae: grey tiles, softly upturned eaves, a heavy ridge with white mortar lines and hip
# ridges), dancheong painted beams and brackets, a hanok body (posts, white plaster panels, paper lattice doors), a granite
# base, onggi jars, a red pine, a persimmon tree, a figure in hanbok with a gat hat (an archer with a Korean bow), a
# stone-and-earth wall with a tiled coping, and a terrain grid.
import math, random
from parcalar import *
from parcalar import _cati_z

KIR, KIR2 = 'kiremit_koyu', 'kiremit_koyu2'


# ---------------------------------------------------------------- roofs
def kore_cati(y, x0, x1, y0, y1, z, h, sacak=0.05, tur='paljak', kivrim=0.4, yukari=0.028, alt_key='boya_yesil', ucluk='ahsap',
              ns=None, sirt_h=None, uc='mangwa', kalinlik=0.012, nr=None, r_ust=0.68, dik=0.78):
    """a Korean tiled roof over the wall rectangle (wall top z, ridge h above at most, eaves sacak out): tur 'paljak'
    (hip-and-gable), 'ujingak' (hipped), 'matbae' (gable); grey tiles, green-painted eave (alt_key), a heavy ridge
    (yongmaru) with white mortar lines, hip ridges running down to upturned corner tips, ridge ends uc 'mangwa' (an
    upturned end tile) or 'chimi' (a tall owl-tail finial) or None. paljak: the hips run up to r_ust and the gable on
    top (hapgak) rises only dik of what they leave: a small, low triangle high on the roof, not the tall steep
    Japanese irimoya gable (r_ust=0.5, dik=1.45 gives the old look). Returns the ridge top z"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if (x1 - x0) < (y1 - y0) - 1e-9:
        with parca(y, (cx, cy, 0), math.pi / 2):
            return kore_cati(y, -(y1 - y0) / 2, (y1 - y0) / 2, -(x1 - x0) / 2, (x1 - x0) / 2, z, h, sacak, tur, kivrim, yukari, alt_key,
                             ucluk, ns, sirt_h, uc, kalinlik, nr, r_ust, dik)
    W = x1 - x0
    ns = ns or max(4, int(W / 0.05))
    nr = nr or (4 if ns < 8 else 6)
    a, b = (x1 - x0) / 2 + sacak, (y1 - y0) / 2 + sacak
    me = 0.012
    sh = sirt_h or min(0.032, max(0.012, h * 0.11))
    if tur == 'paljak':
        top = cati_irimoya(y, x0, x1, y0, y1, z, h, sacak, KIR, KIR2, kivrim, yukari, alt_key, ucluk, ns=ns, nr=nr,
                           ns2=max(3, ns * 2 // 3), nr2=max(3, nr - 1), r_ust=r_ust, dik=dik)
        L = a - b * r_ust
        rmax = r_ust
    elif tur == 'ujingak':
        top = cati_kirma(y, x0, x1, y0, y1, z, h, sacak, KIR, KIR2, kalinlik, kivrim, yukari, alt_key, ns=ns, nr=nr, mahya_en=me)
        L = a - b
        rmax = 1.0
    else:
        top = cati_besik(y, x0, x1, y0, y1, z, h, sacak, KIR, KIR2, kalinlik, kivrim, alt_key, ucluk, None, sacak * 0.8, nr=nr, ns=ns,
                         mahya_en=me)
        L = a - sacak + sacak * 0.8
        rmax = 0.0
    zs = top - me * 0.8                       # the tile surface at the ridge
    # hip ridges: a row of cap blocks down each hip to the corner, its tip turned up
    if rmax > 0:
        hw = sh * 0.55
        for sx in (-1, 1):
            for sy in (-1, 1):
                rs = [rmax * k / 6 for k in range(7)]
                pts = []
                for r in rs:
                    px, py = sx * (a - b * r), sy * b * (1 - r)
                    pts.append(V(cx + px, cy + py, z + _cati_z(px, py, a, b, h, kivrim, yukari) + hw * 0.4))
                for k in range(len(pts) - 1):
                    cubuk(y, pts[k], pts[k + 1], hw, KIR2, hw * 0.9)
                d = V(sx, sy, 0).normalized()
                cubuk(y, pts[0], pts[0] + d * (hw * 1.6) + Z * (hw * 1.4), hw * 0.85, KIR2, hw * 0.8)
        if tur == 'paljak':
            # the verge ridges down the rakes of the upper gable (cati_irimoya's gable roof: rebuilt from its numbers), so
            # the hips run on up to the main ridge
            bi = b * (1 - r_ust)
            zr_ = z + _cati_z(0, bi, a, b, h, kivrim, yukari)
            h2 = max(0.02, (h - (zr_ - z)) * dik)
            k2 = kivrim * 0.5
            b2 = bi + 0.004
            zf2 = lambda t: zr_ - 0.004 + h2 * ((1 - k2) * t + k2 * t * t)
            for sx in (-1, 1):
                for sy in (-1, 1):
                    pts = [V(cx + sx * (L - hw * 0.45), cy + sy * b2 * (1 - t), zf2(t) + hw * 0.3) for t in (0.0, 0.2, 0.4, 0.6, 0.8, 0.97)]
                    for k in range(len(pts) - 1):
                        cubuk(y, pts[k], pts[k + 1], hw * 0.9, KIR2, hw * 0.8)
    # the heavy ridge
    if L > 0.01:
        sw = sh * 0.8
        xa, xb = cx - L - 0.003, cx + L + 0.003
        za, zb = zs - sh * 0.4, zs + sh * 0.6
        kutu(y, V(xa, cy - sw / 2, za), X, xb - xa, sw, zb - za, KIR2, 'onarkasagsolust')
        for s2 in (-1, 1):   # white mortar bands on its sides
            yy = cy + s2 * (sw / 2 + 0.0008)
            y.yuz_yon([V(xa, yy, za + sh * 0.42), V(xb, yy, za + sh * 0.42), V(xb, yy, za + sh * 0.62), V(xa, yy, za + sh * 0.62)], 'siva', V(0, s2))
        # a capping roll on top
        cubuk(y, V(xa - 0.002, cy, zb + sh * 0.12), V(xb + 0.002, cy, zb + sh * 0.12), sw * 0.7, KIR, sh * 0.3)
        zt = zb + sh * 0.27
        for sx in (-1, 1):
            p = V(cx + sx * (L + 0.003), cy, zb - sh * 0.1)
            if uc == 'mangwa':
                boru(y, [p, p + V(sx * sh * 0.25, 0, sh * 0.35), p + V(sx * sh * 0.35, 0, sh * 0.85), p + V(sx * sh * 0.15, 0, sh * 1.2)],
                     sh * 0.32, KIR2, n=6, r_son=sh * 0.16)
                zt = max(zt, p.z + sh * 1.3)
            elif uc == 'chimi':
                chimi(y, p, sx, sh * 2.2)
                zt = max(zt, p.z + sh * 2.2 * 1.05)
        return zt
    return top


def chimi(y, p, sx, H, key=KIR2):
    """an owl-tail ridge finial (chimi) at the ridge end p, its tail curling outward (sx)"""
    p = V(p[0], p[1], p[2])
    w = H * 0.22
    # a tapering block leaning in, its outer face fluted into feather steps
    b0 = [p + V(sx * (w * 0.2) + dx * w, dy * w * 0.5, 0) for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    b1 = [p + V(sx * (w * 0.1) + dx * w * 0.55, dy * w * 0.38, H * 0.75) for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for i in range(4):
        j = (i + 1) % 4
        yuz_dis(y, [b0[i], b0[j], b1[j], b1[i]], key, p + Z * (H * 0.35) + V(sx * w * 0.15, 0, 0))
    y.yuz_yon(b1, key, Z)
    # the tail curling out and down
    t0 = p + V(sx * w * 0.3, 0, H * 0.7)
    boru(y, [t0, t0 + V(sx * w * 0.6, 0, H * 0.22), t0 + V(sx * w * 1.5, 0, H * 0.3), t0 + V(sx * w * 1.9, 0, H * 0.1)], w * 0.45, key, n=6,
         r_son=w * 0.18)


# ---------------------------------------------------------------- dancheong, brackets
def dancheong(y, kose, z, h, adim=0.1, keys=('boya_yesil', 'turkuaz'), konsol=True, cikinti=0.022):
    """painted beams round a CCW polygon under the eaves: the lower beam (changbang) green, the upper (pyeongbang)
    blue-green, at every post the head pattern (red, white, yellow bands), and with konsol a row of bracket arms
    (ikgong) and flower struts over a green frieze. Returns the top z"""
    silme(y, kose, z, h * 0.5, 0.006, keys[0], 'duz')
    silme(y, kose, z + h * 0.5, h * 0.5, 0.01, keys[1], 'duz')
    n = len(kose)
    for i in range(n):
        a, b = V(kose[i].x, kose[i].y), V(kose[(i + 1) % n].x, kose[(i + 1) % n].y)
        L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
        m = max(1, int(round(L / adim)))
        us = [0.016] + [L * j / m for j in range(1, m)] + [L - 0.016]
        for u in us:
            for (o, z0, z1, ws) in ((0.0108, z + h * 0.5, z + h, ((0.009, 'boya_kirmizi'), (0.0055, 'beyaz'), (0.003, 'boya_sari'))),
                                    (0.0068, z, z + h * 0.5, ((0.007, 'boya_kirmizi'), (0.004, 'beyaz')))):
                # (nested stripes: each narrower one a hair further out)
                for k, (w_, key) in enumerate(ws):
                    w2 = min(w_, u, L - u)
                    if w2 < 0.002: continue
                    p = a + e * u + nn * (o + 0.0007 * k)
                    y.yuz_yon([p - e * w2 + Z * (z0 + 0.001), p + e * w2 + Z * (z0 + 0.001), p + e * w2 + Z * (z1 - 0.001), p - e * w2 + Z * (z1 - 0.001)], key, nn)
    zt = z + h
    if not konsol:
        return zt
    hf = h * 0.75
    silme(y, kose, zt, hf, 0.003, keys[0], 'duz')
    for i in range(n):
        a, b = V(kose[i].x, kose[i].y), V(kose[(i + 1) % n].x, kose[(i + 1) % n].y)
        L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
        m = max(1, int(round(L / adim)))
        an = math.atan2(e.y, e.x)
        for j in range(m + 1):
            u = min(max(L * j / m, 0.012), L - 0.012)
            p = a + e * u
            # the bracket arm: a block jutting out with an upturned, red-tipped end
            cubuk(y, p + nn * 0.004 + Z * (zt + hf * 0.45), p + nn * cikinti + Z * (zt + hf * 0.45), 0.01, keys[0], hf * 0.55)
            cubuk(y, p + nn * cikinti + Z * (zt + hf * 0.45), p + nn * (cikinti + 0.006) + Z * (zt + hf * 0.75), 0.009, 'boya_kirmizi', hf * 0.35)
            kutu_merkez(y, (p.x + nn.x * 0.006, p.y + nn.y * 0.006), 0.016, 0.012, hf * 0.3, 'boya_kirmizi', z0=zt + hf * 0.7, aci=an,
                        yuzler='onarkasagsolust')
            if j < m:   # a flower strut (hwaban) between the posts
                q = a + e * (L * (j + 0.5) / m) + nn * 0.004
                kutu_merkez(y, (q.x, q.y), 0.014, 0.006, hf * 0.7, 'boya_kirmizi', z0=zt + hf * 0.1, aci=an, yuzler='onarkasagsolust')
                kure(y, (q.x + nn.x * 0.0035, q.y + nn.y * 0.0035, zt + hf * 0.45), 0.0035, 'boya_sari', n=6, kat=3)
    return zt + hf


# ---------------------------------------------------------------- bodies, bases
def gidan(y, x0, x1, y0, y1, z, h, key='granit', ust='zemin', basamak=(), kat=2):
    """a granite base (gidan) of long dressed blocks in kat courses (each a hair proud of the one above), steps on the
    sides in basamak = ((side 0..3, centre u 0..1, width), ...). Returns the top z"""
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, z, z + h, key, ust=ust)
    for c in range(1, kat):
        silme(y, k, z + h * c / kat - 0.003, 0.003, 0.002, 'granit_koyu' if key == 'granit' else key, 'duz')
    silme(y, k, z + h - 0.004, 0.004, 0.004, key, 'duz')
    for (s, u, w) in basamak:
        a, b = k[s], k[(s + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        p = a.lerp(b, u)
        nst = max(2, int(round(h / 0.022)))
        merdiven(y, p + nn * (0.026 * nst), math.atan2(-nn.y, -nn.x), w, z, z + h, n=nst, d=0.026, key=key)
        # cheek stones
        for sg in (-1, 1):
            q = p + e * (sg * (w / 2 + 0.008))
            cubuk(y, q + nn * (0.026 * nst) + Z * (z + 0.006), q + Z * (z + h + 0.006), 0.014, key, 0.014)
    return z + h


def hanok_govde(y, x0, x1, y0, y1, z, h, bay=0.1, direk='ahsap_acik', duvar='siva', cerceve='ahsap', kagit='kumas',
                desen=None, yuvarlak=False, ust_bant='ahsap', direk_en=0.014, alt_bant=None):
    """the walls of a hanok / hall on the rectangle from z, h high, in bays about `bay` wide between posts: desen(side,
    j, nb) -> 'kapi' (paper lattice door), 'pencere' (lattice window), 'acik' (an open bay, dark inside), 'duvar'
    (white plaster with a timber rail); side 0 front -y, 1 +x, 2 back, 3 -x. Posts (square, or round with yuvarlak) on
    foundation stones, a lintel band ust_bant at the top (None: none, dancheong goes there). Returns the wall top z"""
    desen = desen or (lambda i, j, nb: 'kapi' if i == 0 else 'pencere' if j == nb // 2 else 'duvar')
    k = dikdortgen(x0, x1, y0, y1)
    zt = z + h
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        L = (b - a).length
        nb = max(1, int(round(L / bay)))
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for j in range(nb):
            p, q = a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb)
            t = desen(i, j, nb)
            if t == 'kapi':
                dikdortgen_acik(y, p, q, z, h, 0.1, 0.9, 0.012, h * 0.84, (duvar, cerceve, cerceve, kagit), derin=0.008,
                                cerceve=(0.004, cerceve), ic_kenar=True)
                kafes(y, p, q, z, 0.1, 0.9, 0.012, h * 0.84, cerceve, 5, 7, 0.0022, 0.005)
            elif t == 'pencere':
                dikdortgen_acik(y, p, q, z, h, 0.18, 0.82, h * 0.34, h * 0.76, (duvar, cerceve, cerceve, kagit), derin=0.008,
                                cerceve=(0.004, cerceve), ic_kenar=True)
                kafes(y, p, q, z, 0.18, 0.82, h * 0.34, h * 0.76, cerceve, 4, 4, 0.0022, 0.005)
                kutu(y, p + nn * 0.003 + Z * (z + h * 0.16), e, (q - p).length, 0.006, 0.008, cerceve, 'onust')
            elif t == 'tahta':   # a plank door (storehouse, kitchen)
                dikdortgen_acik(y, p, q, z, h, 0.14, 0.86, 0.012, h * 0.8, (duvar, cerceve, cerceve, 'ahsap_dikey'), derin=0.008,
                                cerceve=(0.005, cerceve), ic_kenar=True)
                for vv in (0.25, 0.6):
                    kutu(y, p.lerp(q, 0.16) - nn * 0.0075 + Z * (z + h * vv), e, (q - p).length * 0.68, 0.0015, 0.006, 'demir', 'on')
            elif t == 'acik':
                dikdortgen_acik(y, p, q, z, h, 0.04, 0.96, 0.0, h * 0.86, (duvar, cerceve, cerceve, 'ahsap_koyu'), derin=0.05)
            else:
                duz_duvar(y, p, q, z, zt, duvar)
                kutu(y, p + nn * 0.003 + Z * (z + h * 0.42), e, (q - p).length, 0.006, 0.009, cerceve, 'onust')
                if alt_bant:
                    kutu(y, p + nn * 0.002 + Z * z, e, (q - p).length, 0.004, h * 0.3, alt_bant, 'onust')
        for j in range(nb + 1):
            p = a.lerp(b, j / nb) + nn * 0.004
            kutu_merkez(y, (p.x, p.y), direk_en * 1.7, direk_en * 1.7, 0.008, 'granit', z0=z, yuzler='onarkasagsolust')
            if yuvarlak:
                y.prizma((p.x, p.y), direk_en * 0.55, z + 0.008, zt, direk, n=8)
            else:
                kutu_merkez(y, (p.x, p.y), direk_en, direk_en, h - 0.008, direk, z0=z + 0.008)
        if ust_bant:
            kutu(y, a + nn * 0.008 + Z * (zt - h * 0.13) - e * 0.008, e, L + 0.016, 0.014, h * 0.13, ust_bant, 'onust')
            kutu(y, a + nn * 0.006 + Z * z - e * 0.006, e, L + 0.012, 0.01, 0.012, cerceve, 'onust')
    y.yuz_yon([V(p.x, p.y, zt) for p in k], 'ahsap_koyu', Z)
    return zt


def maru(y, x0, x1, ya, yb, z, key='ahsap_acik', kalin=0.012):
    """a narrow wooden veranda floor (toenmaru) along a front: the deck from ya (outer edge) to yb (wall line) at z,
    its fascia and plank seams"""
    kutu(y, V(x0, ya, z - kalin), X, x1 - x0, yb - ya, kalin, key, 'onsagsolust')
    m = max(2, int((x1 - x0) / 0.03))
    for k in range(1, m):
        x = x0 + (x1 - x0) * k / m
        y.yuz_yon([V(x - 0.0008, ya + 0.001, z + 0.0006), V(x + 0.0008, ya + 0.001, z + 0.0006), V(x + 0.0008, yb - 0.001, z + 0.0006),
                   V(x - 0.0008, yb - 0.001, z + 0.0006)], 'ahsap', Z)


# ---------------------------------------------------------------- jars, trees, people
def onggi(y, x, yy, z, H, R=None, key='onggi', kapak='onggi2', n=10):
    """an onggi jar: a narrow foot, a full belly, a short neck and rim, a shallow lid (kapak key; None: open, dark
    inside)"""
    R = R or H * 0.42
    pr = [(R * 0.6, z), (R * 0.88, z + H * 0.2), (R, z + H * 0.48), (R * 0.9, z + H * 0.7), (R * 0.64, z + H * 0.85), (R * 0.5, z + H * 0.9),
          (R * 0.55, z + H * 0.93)]
    if kapak:
        donel(y, (x, yy), pr + [(R * 0.53, z + H * 0.95), (0.0, z + H * 0.95)], key, n=n)
        donel(y, (x, yy), [(R * 0.56, z + H * 0.945), (R * 0.56, z + H * 0.965), (R * 0.36, z + H * 1.03), (R * 0.1, z + H * 1.06),
                           (R * 0.12, z + H * 1.09), (0.0, z + H * 1.1)], kapak, n=n)
        y.yuz_yon([V(x + R * 0.56 * math.cos(TAU * i / n), yy + R * 0.56 * math.sin(TAU * i / n), z + H * 0.945) for i in range(n)], kapak, -Z)
        return z + H * 1.1
    donel(y, (x, yy), pr + [(R * 0.47, z + H * 0.93), (R * 0.47, z + H * 0.87)], key, n=n)
    y.yuz_yon([V(x + R * 0.47 * math.cos(TAU * i / n), yy + R * 0.47 * math.sin(TAU * i / n), z + H * 0.87) for i in range(n)], 'koyu', Z)
    return z + H * 0.93


def sonamu(y, x, yy, z, boy=0.3, tohum=0, key='yesil_koyu', govde='kerpic_koyu', yon=None):
    """a Korean red pine: a twisting reddish trunk leaning one way, branches holding flat layered clumps of needles"""
    r = random.Random(tohum)
    a = yon if yon is not None else r.uniform(0, TAU)
    d = V(math.cos(a), math.sin(a))
    s = V(-d.y, d.x)
    pts = [V(x, yy, z - 0.01), V(x, yy, z) + d * (boy * 0.04) + Z * (boy * 0.3), V(x, yy, z) + d * (boy * 0.12) + s * (boy * 0.03) + Z * (boy * 0.58),
           V(x, yy, z) + d * (boy * 0.16) - s * (boy * 0.02) + Z * (boy * 0.82)]
    boru(y, pts, boy * 0.034, govde, n=7, r_son=boy * 0.014)

    def kume(c, rr, hh):
        donel(y, (c.x, c.y), [(0.0, c.z - hh * 0.35), (rr * 0.72, c.z - hh * 0.3), (rr, c.z), (rr * 0.82, c.z + hh * 0.28),
                              (rr * 0.4, c.z + hh * 0.45), (0.0, c.z + hh * 0.5)], key, n=9, kat=r.uniform(0, 1))
    kume(pts[-1] + Z * (boy * 0.06), boy * 0.2, boy * 0.16)
    for k, (t, ln, ang) in enumerate(((0.5, 0.2, 1.6), (0.68, 0.22, -1.9), (0.82, 0.16, 2.8), (0.42, 0.17, -0.6))):
        i0 = 1 if t < 0.6 else 2
        p0 = pts[i0].lerp(pts[i0 + 1], (t * 3) % 1)
        dd = V(math.cos(a + ang), math.sin(a + ang))
        p1 = p0 + dd * (boy * ln) + Z * (boy * 0.07)
        boru(y, [p0, p1], boy * 0.012, govde, n=5, r_son=boy * 0.006)
        kume(p1 + Z * (boy * 0.03), boy * (0.13 + 0.04 * r.random()), boy * 0.11)
    return pts[-1].z + boy * 0.14


def kaki(y, x, yy, z, boy=0.4, tohum=0, yaprak='zeytin', meyve='turuncu', govde='ahsap'):
    """a persimmon tree in autumn: a short trunk forking into crooked boughs, thin leafy clumps and the orange fruit
    hanging all over them"""
    r = random.Random(tohum)
    top = V(x, yy, z + boy * 0.26)
    boru(y, [V(x, yy, z - 0.01), V(x + boy * 0.012, yy, z + boy * 0.13), top], boy * 0.034, govde, n=7, r_son=boy * 0.026)
    yapraklar = (yaprak, 'yesil_koyu', yaprak, 'cimen_kuru')
    for k in range(6):
        a = TAU * k / 6 + r.uniform(-0.3, 0.3)
        d = V(math.cos(a), math.sin(a))
        p1 = top + d * (boy * 0.08) + Z * (boy * 0.14)
        p2 = p1 + d * (boy * r.uniform(0.1, 0.15)) + Z * (boy * r.uniform(0.12, 0.2))
        boru(y, [top, p1, p2], boy * 0.017, govde, n=5, r_son=boy * 0.007)
    # one lumpy crown: overlapping clumps packed in a broad dome
    C = V(x, yy, z + boy * 0.66)
    RH, RV = boy * 0.25, boy * 0.17
    kumeler = []
    for k in range(18):
        a = TAU * k / 18 * 2.618 + r.uniform(-0.2, 0.2)
        t = math.sqrt((k + 0.5) / 18)
        el = r.uniform(-0.35, 1.0)
        c = C + V(math.cos(a) * RH * 0.62 * t * math.cos(el * 0.5), math.sin(a) * RH * 0.62 * t * math.cos(el * 0.5), RV * 0.6 * el * (1.1 - t * 0.5))
        kumeler.append((c, boy * r.uniform(0.085, 0.12)))
    for k, (c, rr) in enumerate(kumeler):
        kure(y, (c.x, c.y, c.z), rr, yapraklar[k % 4], n=10, kat=5)
    # the fruit: on the outside of the crown, more on its lower half
    for k in range(60):
        c, rr = kumeler[r.randrange(len(kumeler))]
        d = (c - C)
        d = V(d.x, d.y, d.z * 0.6 - 0.02) + V(r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 0.6)) * (d.length * 0.8 + 0.01)
        if d.length < 1e-6: continue
        p = c + d.normalized() * (rr + boy * 0.004)
        kure(y, (p.x, p.y, p.z), boy * 0.016, meyve, n=8, kat=4)
    return z + boy


def kisi(y, x, yy, z, aci=0.0, boy=0.06, govde='beyaz', kusak='boya_kirmizi', sapka='gat', yay=False, kol='yan'):
    """a figure in hanbok facing aci: a long robe with a sash, a head and a gat (the wide black horsehair hat), or a
    topknot (sapka 'yok') or a bamboo hat ('saz'); yay: an archer at full draw with a Korean recurve bow"""
    with parca(y, (x, yy, z), aci):
        s = boy / 0.06
        for sx in (-1, 1):
            cubuk(y, V(0, sx * 0.0035 * s, 0), V(0, sx * 0.0035 * s, 0.012 * s), 0.004 * s, 'koyu')
        donel(y, (0, 0), [(0.0, 0.006 * s), (0.0105 * s, 0.006 * s), (0.0092 * s, 0.022 * s), (0.0075 * s, 0.036 * s),
                          (0.0062 * s, 0.043 * s), (0.0, 0.045 * s)], govde, n=8)
        donel(y, (0, 0), [(0.0086 * s, 0.027 * s), (0.0088 * s, 0.03 * s), (0.0082 * s, 0.033 * s)], kusak, n=8)
        hz = 0.0505 * s
        kure(y, (0, 0, hz), 0.0055 * s, 'siva_krem', n=8, kat=4)
        if sapka == 'gat':
            donel(y, (0, 0), [(0.0, hz + 0.0035 * s), (0.0135 * s, hz + 0.0035 * s), (0.0135 * s, hz + 0.0045 * s), (0.0048 * s, hz + 0.0045 * s),
                              (0.0044 * s, hz + 0.0115 * s), (0.0, hz + 0.0118 * s)], 'koyu', n=10)
        elif sapka == 'saz':
            y.koni((0, 0), 0.013 * s, hz + 0.003 * s, 0.009 * s, 'saz', n=10)
            y.yuz_yon([V(0.013 * s * math.cos(TAU * i / 10), 0.013 * s * math.sin(TAU * i / 10), hz + 0.003 * s) for i in range(10)], 'saz', -Z)
        else:
            kure(y, (-0.001 * s, 0, hz + 0.006 * s), 0.0025 * s, 'koyu', n=6, kat=3)
        if yay:
            gx = 0.027 * s
            # the bow hand straight out, the draw hand at the cheek
            cubuk(y, V(0.002 * s, 0.006 * s, 0.04 * s), V(gx, 0.001 * s, 0.041 * s), 0.0032 * s, govde)
            cubuk(y, V(0.0, -0.0065 * s, 0.04 * s), V(-0.002 * s, -0.004 * s, 0.047 * s), 0.0032 * s, govde)
            cubuk(y, V(-0.002 * s, -0.004 * s, 0.047 * s), V(0.002 * s, -0.001 * s, 0.049 * s), 0.003 * s, govde)
            # the recurve bow: the grip at the hand, limbs bending back, tips flicking forward
            bow = [(0.006, 0.019), (0.0, 0.026), (-0.004, 0.034), (-0.002, 0.042), (0.0, 0.041 + 0.0), (0.0, 0.041)]
            pts = [V(gx + dx * s, 0.001 * s, zz * s) for dx, zz in ((0.004, 0.012), (-0.0015, 0.02), (0.0, 0.033), (0.0015, 0.041), (0.0, 0.049),
                                                                    (-0.0015, 0.062), (0.004, 0.07))]
            boru(y, pts, 0.0011 * s, 'ahsap_koyu', n=4)
            # the string drawn back to the cheek, the arrow along it
            cubuk(y, pts[0], V(0.002 * s, -0.001 * s, 0.049 * s), 0.0006 * s, 'beyaz')
            cubuk(y, pts[-1], V(0.002 * s, -0.001 * s, 0.049 * s), 0.0006 * s, 'beyaz')
            cubuk(y, V(0.001 * s, -0.0008 * s, 0.049 * s), V(gx + 0.008 * s, 0.0008 * s, 0.042 * s), 0.0009 * s, 'ahsap_acik')
        else:
            for sy in (-1, 1):
                if kol == 'yan':
                    cubuk(y, V(0, sy * 0.0075 * s, 0.04 * s), V(0.002 * s, sy * 0.0095 * s, 0.024 * s), 0.0034 * s, govde)
                else:   # hands folded in front
                    cubuk(y, V(0, sy * 0.0075 * s, 0.04 * s), V(0.007 * s, sy * 0.002 * s, 0.03 * s), 0.0034 * s, govde)


# ---------------------------------------------------------------- walls, terrain
def toprak_duvar(y, yol, z0, h, t=0.022, govde='siva_krem', kaide='granit', kaide_h=None, kapali=False, cati=KIR):
    """a Korean stone-and-earth wall (doldam) along a polyline (outer face to the right): a rough stone lower part a
    little proud, a pale earth-plaster upper part with stones set in it, a tiled coping with a white-lined ridge"""
    kh = kaide_h if kaide_h is not None else h * 0.45
    O = [V(p[0], p[1]) for p in yol]
    n = len(O)
    I = disa(O, -t, kapali)
    Oe, M, Ie = disa(O, 0.012, kapali), disa(O, -t / 2, kapali), disa(O, -t - 0.012, kapali)
    m = n if kapali else n - 1
    zc, zr = z0 + h - 0.002, z0 + h + 0.017
    rs = random.Random(len(O) * 7 + int(h * 1000))
    for i in range(m):
        j = (i + 1) % n
        e = (O[j] - O[i]); L = e.length; e.normalize(); nn = V(e.y, -e.x)
        for P_, Q_, s in ((O[i], O[j], nn), (I[j], I[i], -nn)):
            ee = (Q_ - P_).normalized()
            Ls = (Q_ - P_).length
            duz_duvar(y, P_, Q_, z0 + kh, z0 + h, govde)
            # (the proud stone base, on the outer face carried on 0.003 past a corner so the two runs meet: a slit
            #  at every outer corner showed the inside)
            ua = 0.003 if (s is nn and (kapali or i > 0)) else 0.0
            ub = 0.003 if (s is nn and (kapali or j < n - 1)) else 0.0
            Pk, Qk = P_ - ee * ua, Q_ + ee * ub
            duz_duvar(y, Pk + s * 0.003, Qk + s * 0.003, z0 - 0.01, z0 + kh, kaide)
            y.yuz_yon([Pk + Z * (z0 + kh), Qk + Z * (z0 + kh), Qk + s * 0.003 + Z * (z0 + kh), Pk + s * 0.003 + Z * (z0 + kh)], kaide, Z)
            # stones set in the earth part (along this face's own length: the inner face is shorter)
            for k in range(int(Ls / 0.05)):
                u = (k + 0.3 + 0.4 * rs.random()) / int(Ls / 0.05) * Ls
                zz = z0 + kh + (h - kh) * rs.uniform(0.2, 0.7)
                w, hh = rs.uniform(0.008, 0.014), rs.uniform(0.006, 0.01)
                c = P_ + ee * u + s * 0.0012
                y.yuz_yon([c - ee * w + Z * zz, c + ee * w + Z * zz, c + ee * (w * 0.8) + Z * (zz + hh), c - ee * (w * 0.8) + Z * (zz + hh)], 'granit', s)
        y.yuz_yon([Oe[i] + Z * zc, Oe[j] + Z * zc, M[j] + Z * zr, M[i] + Z * zr], cati, nn + Z * 1.2)
        y.yuz_yon([Ie[j] + Z * zc, Ie[i] + Z * zc, M[i] + Z * zr, M[j] + Z * zr], cati, -nn + Z * 1.2)
        y.yuz_yon([O[i] + Z * (z0 + h), O[j] + Z * (z0 + h), Oe[j] + Z * zc, Oe[i] + Z * zc], 'ahsap_koyu', -Z)
        y.yuz_yon([I[j] + Z * (z0 + h), I[i] + Z * (z0 + h), Ie[i] + Z * zc, Ie[j] + Z * zc], 'ahsap_koyu', -Z)
        cubuk(y, M[i] + Z * (zr + 0.003), M[j] + Z * (zr + 0.003), 0.008, KIR2, 0.008)
        for s2 in (-1, 1):
            q0, q1 = M[i] + nn * (s2 * 0.0048) + Z * (zr - 0.0005), M[j] + nn * (s2 * 0.0048) + Z * (zr - 0.0005)
            y.yuz_yon([q0, q1, q1 + Z * 0.003, q0 + Z * 0.003], 'siva', nn * s2)
    if not kapali:
        for k, s in ((0, -1), (n - 1, 1)):
            e = (O[1] - O[0]) if k == 0 else (O[-1] - O[-2]); e.z = 0; e.normalize()
            nn = V(e.y, -e.x)
            y.yuz_yon([O[k] + Z * (z0 + kh), I[k] + Z * (z0 + kh), I[k] + Z * (z0 + h), O[k] + Z * (z0 + h)], govde, e * s)
            y.yuz_yon([O[k] + nn * 0.003 + Z * (z0 - 0.01), I[k] - nn * 0.003 + Z * (z0 - 0.01), I[k] - nn * 0.003 + Z * (z0 + kh),
                       O[k] + nn * 0.003 + Z * (z0 + kh)], kaide, e * s)
            y.yuz_yon([Oe[k] + Z * zc, O[k] + Z * (z0 + h), I[k] + Z * (z0 + h), Ie[k] + Z * zc, M[k] + Z * zr], cati, e * s)


def arazi(y, yuk, x0, x1, y0, y1, nx, ny, key='toprak_ot', atla=None, etek=0.0, etek_key='toprak'):
    """a terrain grid over the rectangle (yuk(x, y) the ground height), alternating diagonals; atla(x, y) -> True skips
    a cell (a hole for a pond, or ground hidden under a building); a skirt down to etek round the edge. Returns the
    corner grid"""
    P = [[V(x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny, 0) for j in range(ny + 1)] for i in range(nx + 1)]
    for i in range(nx + 1):
        for j in range(ny + 1):
            P[i][j].z = yuk(P[i][j].x, P[i][j].y)
    for i in range(nx):
        for j in range(ny):
            if atla and atla((P[i][j].x + P[i + 1][j + 1].x) / 2, (P[i][j].y + P[i + 1][j + 1].y) / 2):
                continue
            if (i + j) % 2 == 0:
                tris = ([P[i][j], P[i + 1][j], P[i + 1][j + 1]], [P[i][j], P[i + 1][j + 1], P[i][j + 1]])
            else:
                tris = ([P[i][j], P[i + 1][j], P[i][j + 1]], [P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]])
            for tri in tris:
                y.yuz_yon(tri, key, Z)
    kenar = [P[i][0] for i in range(nx)] + [P[nx][j] for j in range(ny)] + [P[i][ny] for i in range(nx, 0, -1)] + [P[0][j] for j in range(ny, 0, -1)]
    for k in range(len(kenar)):
        a, b = kenar[k], kenar[(k + 1) % len(kenar)]
        e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
        if etek_key != 'katman':
            y.yuz_yon([V(a.x, a.y, etek), V(b.x, b.y, etek), b, a], etek_key, nn)
            continue
        # the soil under the turf, then wavering strata of rock
        za, zb = a.z - 0.02, b.z - 0.02
        y.yuz_yon([V(a.x, a.y, za), V(b.x, b.y, zb), b, a], 'toprak', nn)
        sa, sb = 0.01 * math.sin(a.x * 7 + a.y * 5), 0.01 * math.sin(b.x * 7 + b.y * 5)
        m1a, m1b = min(za, etek + 0.03 + sa), min(zb, etek + 0.03 + sb)
        m2a, m2b = min(za, etek + 0.11 - sa * 1.5), min(zb, etek + 0.11 - sb * 1.5)
        y.yuz_yon([V(a.x, a.y, m2a), V(b.x, b.y, m2b), V(b.x, b.y, zb), V(a.x, a.y, za)], 'kaya_koyu', nn)
        y.yuz_yon([V(a.x, a.y, m1a), V(b.x, b.y, m1b), V(b.x, b.y, m2b), V(a.x, a.y, m2a)], 'kaya', nn)
        y.yuz_yon([V(a.x, a.y, etek), V(b.x, b.y, etek), V(b.x, b.y, m1b), V(a.x, a.y, m1a)], 'kaya_koyu', nn)
    return P


def ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def karis(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))
