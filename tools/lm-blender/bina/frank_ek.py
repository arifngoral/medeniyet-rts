# Helpers for the later Frankish landmarks (lm_notredame, lm_carcassonne, lm_versay, lm_invalides): Gothic rose
# windows, traceried lancets, portals with stepped archivolts, flying buttresses, pinnacles, open balustrades and
# statues; classical balustrades with urns, pilasters, mansard roofs with dormers. (frank_ortak.py belongs to the
# first four Frankish landmarks; this file is separate.)
import math
from mathutils import Vector
from parcalar import *


def eksen(a, b):
    """a, b as 2D points, the length, the unit direction and the outward normal (right of a->b)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    e = (b - a) / L
    return a, b, L, e, V(e.y, -e.x)


def kutu3(y, c, ex, ey, ez, sx, sy, sz, key, yuzler=None):
    """a box centred at c along three axes, sizes sx, sy, sz; every face wound outward. yuzler: which of
    '+x -x +y -y +z -z' to draw (default all)"""
    c = Vector(c); ex, ey, ez = Vector(ex).normalized(), Vector(ey).normalized(), Vector(ez).normalized()
    P = lambda i, j, k: c + ex * (sx / 2 * i) + ey * (sy / 2 * j) + ez * (sz / 2 * k)
    yz = yuzler or ('+x', '-x', '+y', '-y', '+z', '-z')
    for ad, ax, q in (('+x', ex, [P(1, -1, -1), P(1, 1, -1), P(1, 1, 1), P(1, -1, 1)]),
                      ('-x', -ex, [P(-1, -1, -1), P(-1, 1, -1), P(-1, 1, 1), P(-1, -1, 1)]),
                      ('+y', ey, [P(-1, 1, -1), P(1, 1, -1), P(1, 1, 1), P(-1, 1, 1)]),
                      ('-y', -ey, [P(-1, -1, -1), P(1, -1, -1), P(1, -1, 1), P(-1, -1, 1)]),
                      ('+z', ez, [P(-1, -1, 1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, 1)]),
                      ('-z', -ez, [P(-1, -1, -1), P(1, -1, -1), P(1, 1, -1), P(-1, 1, -1)])):
        if ad in yz:
            y.yuz_yon(q, key, ax)


def levha(y, pts, key, yon, kil=0.0012):
    """a thin closed sheet (a gablet, a board) seen from both sides: the face toward yon, its back kil behind, the rims"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    arka = [p - yon * kil for p in pts]
    y.yuz_yon(pts, key, yon)
    y.yuz_yon(arka, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        m = (pts[i] + pts[j]) / 2
        y.yuz_yon([pts[i], pts[j], arka[j], arka[i]], key, m - c)


def halka(y, P, r0, r1, d, key, yon, n=24, t0=0.0, t1=TAU):
    """an annulus r0..r1 at depth d in a frame P(rr, t, d), facing yon"""
    tam = abs(t1 - t0 - TAU) < 1e-6
    for i in range(n):
        a, b = t0 + (t1 - t0) * i / n, t0 + (t1 - t0) * (i + 1) / n
        if r0 < 1e-9:
            y.yuz_yon([P(0, 0, d), P(r1, a, d), P(r1, b, d)], key, yon)
        else:
            y.yuz_yon([P(r0, a, d), P(r1, a, d), P(r1, b, d), P(r0, b, d)], key, yon)


def silindir_yuz(y, P, r, d0, d1, key, merkez_yon, n=24, ic=False):
    """the cylinder r between depths d0..d1 in a frame P(rr, t, d); ic: facing the axis (a reveal)"""
    for i in range(n):
        a, b = TAU * i / n, TAU * (i + 1) / n
        q = [P(r, a, d0), P(r, b, d0), P(r, b, d1), P(r, a, d1)]
        m = (q[0] + q[1]) / 2
        out = m - merkez_yon(d0)
        y.yuz_yon(q, key, -out if ic else out)


def gul_pencere(y, o, ex, n, r, renkler=('kobalt', 'boya_kirmizi', 'lacivert', 'altin'), cerceve='tas_acik', iz='tas_acik',
                yaprak=12, dis=None):
    """a Gothic rose window on a vertical wall: o its centre ON the wall face, ex along the wall, n out. Stepped
    projecting frame rings, the stained glass in three rings of cells (renkler: main, inner, outer, centre), radial
    tracery spokes and rings standing in front of the glass. dis: the outer frame ring radius factor (default 1.2)"""
    o, ex, n = Vector(o), Vector(ex).normalized(), Vector(n).normalized()
    up = Z
    P = lambda rr, t, d: o + ex * (rr * math.cos(t)) + up * (rr * math.sin(t)) + n * d
    ax = lambda d: o + n * d
    N = yaprak * 2
    R2, R1 = r * (dis or 1.2), r * 1.08
    # frame: outer projecting ring, a step, the reveal down to the glass
    halka(y, P, R1, R2, 0.014, cerceve, n, N)
    silindir_yuz(y, P, R2, 0.0, 0.014, cerceve, ax, N)
    halka(y, P, r, R1, 0.008, iz, n, N)
    silindir_yuz(y, P, R1, 0.008, 0.014, 'tas_koyu', ax, N, ic=True)
    silindir_yuz(y, P, r, 0.003, 0.008, 'tas_koyu', ax, N, ic=True)
    # glass
    g = 0.003
    halka(y, P, 0, r * 0.24, g, renkler[3], n, yaprak)
    for i in range(yaprak):
        a, b = TAU * i / yaprak, TAU * (i + 1) / yaprak
        y.yuz_yon([P(r * 0.24, a, g), P(r * 0.6, a, g), P(r * 0.6, b, g), P(r * 0.24, b, g)], renkler[1] if i % 2 else renkler[0], n)
    for i in range(N):
        a, b = TAU * i / N, TAU * (i + 1) / N
        y.yuz_yon([P(r * 0.6, a, g), P(r, a, g), P(r, b, g), P(r * 0.6, b, g)], renkler[2] if i % 2 else renkler[0], n)
    # tracery: rings and spokes, 0.0035 in front of the glass
    t = 0.0065
    halka(y, P, r * 0.22, r * 0.27, t, iz, n, N)
    halka(y, P, r * 0.57, r * 0.63, t, iz, n, N)
    for i, (r0, k) in enumerate(((r * 0.27, yaprak), (r * 0.63, N))):
        r1 = r * 0.57 if i == 0 else r
        for j in range(k):
            a = TAU * (j + 0.5) / k if i == 0 else TAU * j / k
            w = r * (0.045 if i == 0 else 0.03)
            c0, c1 = P(r0, a, 0), P(r1, a, 0)
            s = (c1 - c0).normalized().cross(n).normalized() * w
            q = [c0 - s + n * t, c1 - s + n * t, c1 + s + n * t, c0 + s + n * t]
            y.yuz_yon(q, iz, n)
            for sg in (-1, 1):
                y.yuz_yon([c0 + s * sg + n * g, c1 + s * sg + n * g, c1 + s * sg + n * t, c0 + s * sg + n * t], iz, s * sg)
    # small roundels at the inner petals' heads
    for j in range(yaprak):
        a = TAU * (j + 0.5) / yaprak
        c = P(r * 0.47, a, 0)
        Q = lambda rr, tt, d, c=c: c + ex * (rr * math.cos(tt)) + up * (rr * math.sin(tt)) + n * d
        halka(y, Q, r * 0.055, r * 0.085, t, iz, n, 8)


def gotik_pencere(y, p, q, z0, H, en=0.6, sivri=0.75, v0=0.02, ust=None, derin=0.02, cam='kobalt', duvar='kirec',
                  ic='tas_koyu', esik='tas_acik', izli=True, cerceve=None, iz='tas_acik'):
    """a lancet window bay p->q (Yapi.kemerli, pointed) and, izli, its tracery: a mullion splitting two lights and a
    roundel in the head. Returns (W, e, nc, L, x0, x1, hs)"""
    ust = H * 0.08 if ust is None else ust
    W, e, nc, L = y.kemerli(V(p[0], p[1]), V(q[0], q[1]), z0, H, (duvar, ic, esik, cam), v0=v0, en=en, ust=ust, derin=derin,
                            k_say=8, sivri=sivri, cerceve=cerceve)
    x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
    w = x1 - x0; hr = sivri * w; hs = H - ust - hr
    if izli and w > 0.02:
        dd = derin * 0.45
        cubuk(y, L(W / 2, v0, dd), L(W / 2, hs + hr * 0.12, dd), w * 0.09, iz, derin * 0.3)
        c = L(W / 2, hs + hr * 0.42, dd)
        Q = lambda rr, tt, d: c + e * (rr * math.cos(tt)) + Z * (rr * math.sin(tt)) + nc * d
        halka(y, Q, w * 0.16, w * 0.22, 0.0, iz, nc, 10)
        # the two lights' heads: small pointed arches springing from the mullion
        for s in (-1, 1):
            xa, xb = (x0, W / 2) if s < 0 else (W / 2, x1)
            yol = kemer_yolu(xa, xb, hs, sivri * 0.9, 6)
            for k in range(len(yol) - 1):
                (ua, va), (ub, vb) = yol[k], yol[k + 1]
                cubuk(y, L(ua, va, dd), L(ub, vb, dd), w * 0.06, iz, derin * 0.25)
    return W, e, nc, L, x0, x1, hs


def gotik_portal(y, a, b, z0, H, kat=4, en=0.82, sivri=0.6, adim=0.012, ust=None, keys=('tas_acik', 'kirec'),
                 kapi_key='ahsap_koyu', timpan='tas_acik', duvar='kirec', heykel_key=None, mentese=True):
    """a Gothic portal in the bay a->b (faces the right of a->b): kat nested pointed niches stepping back adim each
    (the archivolts, alternating keys), colonnettes in the jambs, at the back a tympanum with relief registers over a
    lintel and a pair of doors with a trumeau and iron hinges. Returns the archivolts' outer apex height above z0"""
    a, b, W0, e, nc = eksen(a, b)
    ust = H * 0.1 if ust is None else ust
    p, q, HH, ee, u_ = a, b, H, en, ust
    d_top = 0.0
    tepe = None
    son = None
    for k in range(kat):
        L, x0, x1, hs, apex = kemer_nis(y, p, q, z0, HH, en=ee, ust=u_, sivri=sivri, derin=adim,
                                        key=duvar if k == 0 else keys[(k + 1) % 2], yan_key=keys[k % 2], k_say=12)
        if tepe is None: tepe = apex
        # a colonnette at each jamb's corner, up to the springing
        for u in (x0, x1):
            c = L(u, 0, adim * 0.5)
            y.prizma((c.x, c.y), adim * 0.36, z0, z0 + hs, keys[(k + 1) % 2], n=6, ust=False)
            y.prizma((c.x, c.y), adim * 0.52, z0 + hs - 0.004, z0 + hs + 0.002, keys[0], n=6)
        p2, q2 = L(x0, 0, adim), L(x1, 0, adim)
        p, q = V(p2.x, p2.y), V(q2.x, q2.y)
        Wk = x1 - x0
        HH = apex
        st = adim * 0.9
        ee = max(0.3, (Wk - 2 * st) / Wk)
        u_ = st * 0.8
        son = (L, x0, x1, hs, apex)
    # the back: tympanum over a lintel, the doors
    L, x0, x1, hs, apex = son
    nn = nc   # all the same direction
    dback = adim
    vl = hs * 0.82
    yol = kemer_yolu(x0, x1, hs, sivri, 12)
    tim = [L(x0, vl, dback)] + [L(u, v, dback) for u, v in yol] + [L(x1, vl, dback)]
    y.yuz_yon(tim, timpan, nn)
    w = x1 - x0
    # relief registers on the tympanum (thin bands and a mandorla)
    for f in (0.3, 0.62):
        vv = vl + (apex - vl) * f
        us = [u for u, v_ in yol if v_ >= vv]
        ww = ((max(us) - min(us)) if us else w) * 0.84
        if ww > 0.01:
            kutu3(y, L((x0 + x1) / 2, vv, dback - 0.002), e, nn, Z, ww, 0.004, 0.004, keys[1])
    m = L((x0 + x1) / 2, vl + (apex - vl) * 0.45, dback - 0.003)
    Qm = lambda rr, tt, d: m + e * (rr * 0.7 * math.cos(tt)) + Z * (rr * math.sin(tt)) + nn * d
    halka(y, Qm, 0.0, (apex - vl) * 0.22, 0.0, keys[1], nn, 10)
    # lintel
    kutu3(y, L((x0 + x1) / 2, vl - 0.006, dback - 0.003), e, nn, Z, w, 0.006, 0.012, keys[0])
    # doors and trumeau
    y.yuz_yon([L(x0, 0, dback), L(x1, 0, dback), L(x1, vl - 0.012, dback), L(x0, vl - 0.012, dback)], kapi_key, nn)
    tr = L((x0 + x1) / 2, 0, dback - 0.006)
    kutu3(y, tr + Z * ((vl - 0.012) / 2), e, nn, Z, w * 0.1, 0.012, vl - 0.012, keys[0], ('+x', '-x', '+y', '-y'))
    heykel(y, tr.x + nn.x * 0.004, tr.y + nn.y * 0.004, z0 + vl * 0.42, s=vl * 0.5 / 0.048, key=heykel_key or keys[0])
    if mentese:
        for s in (-1, 1):
            for f in (0.25, 0.55):
                u0 = (x0 + x1) / 2 + s * w * 0.06
                u1 = (x0 + x1) / 2 + s * w * 0.46
                kutu3(y, L((u0 + u1) / 2, vl * f, dback - 0.0015), e, nn, Z, abs(u1 - u0), 0.002, 0.003, 'demir', ('+y', '+z', '-z', '+x', '-x'))
                for g in (-1, 1):
                    kutu3(y, L((u0 + u1) / 2 + s * w * 0.05, vl * f + g * 0.006, dback - 0.0015), e, nn, Z, abs(u1 - u0) * 0.5, 0.002, 0.002,
                          'demir', ('+y', '+z', '-z', '+x', '-x'))
    return tepe


def heykel(y, x, yy, z, s=1.0, key='kirec', aci=0.0, n=7):
    """a standing robed statue ~0.048 s tall: a robe flaring at the foot, shoulders, a head"""
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0, 0.0), (0.0085, 0.0), (0.0078, 0.006), (0.0062, 0.028), (0.0068, 0.033), (0.0045, 0.038), (0.0, 0.0385)], key, n=n)
        kure(y, (0, 0, 0.0425), 0.0052, key, n=n, kat=4)


def piramit_cati(y, c, w, d, z, h, key, n_alt=False):
    """a 4-sided pyramid w x d on z, h high (a pinnacle's or a turret's spire)"""
    cx, cy = c
    k = [V(cx - w / 2, cy - d / 2, z), V(cx + w / 2, cy - d / 2, z), V(cx + w / 2, cy + d / 2, z), V(cx - w / 2, cy + d / 2, z)]
    t = V(cx, cy, z + h)
    for i in range(4):
        j = (i + 1) % 4
        m = (k[i] + k[j]) / 2
        y.yuz_yon([k[i], k[j], t], key, V(m.x - cx, m.y - cy, 0.3))
    if n_alt:
        y.yuz_yon(k, key, -Z)
    return z + h


def fiyal(y, cx, cy, w, z0, h, tip_h=None, key='kirec', tip_key=None, gablet=True, aci=0.0):
    """a Gothic pinnacle: a square shaft w wide from z0 to z0 + h, small gablets on its four faces, a steep pyramid
    spire with a knob. Returns the tip z"""
    tip_h = tip_h or w * 3.2
    tk = tip_key or key
    with parca(y, (cx, cy, 0), aci):
        kutu_merkez(y, (0, 0), w, w, h, key, z0=z0, yuzler='onarkasagsolust')
        zt = z0 + h
        silme(y, dikdortgen(-w / 2, w / 2, -w / 2, w / 2), zt - w * 0.18, w * 0.18, w * 0.14, key, 'duz')
        if gablet:
            for (nx, ny) in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                nn = V(nx, ny); ee = V(-ny, nx)
                c = nn * (w / 2 + 0.0008) + Z * zt
                levha(y, [c - ee * (w / 2), c + ee * (w / 2), c + Z * (w * 0.75)], tk, nn, 0.0015)
        t = piramit_cati(y, (0, 0), w * 0.92, w * 0.92, zt, tip_h, tk)
        kure(y, (0, 0, t + w * 0.06), w * 0.16, tk, n=6, kat=3)
    return z0 + h + tip_h + w * 0.2


def ucan_payanda(y, p, w, z_alt_p, z_ust_p, z_alt_w, z_ust_w, t=0.014, key='kirec', kapak='tas_acik', n=8):
    """a flying buttress: an arched arm from the pier at p (2D, the pier's inner face) to the wall at w, t thick: its
    straight sloping top from z_ust_p (pier) to z_ust_w (wall), its soffit a quarter arch from z_alt_p at the pier to
    z_alt_w at the wall; a coping on the top"""
    p, w = V(p[0], p[1]), V(w[0], w[1])
    D = (w - p).length; d = (w - p) / D; s = V(-d.y, d.x)
    alt = [(D - D * math.cos(math.pi / 2 * k / n), z_alt_p + (z_alt_w - z_alt_p) * math.sin(math.pi / 2 * k / n)) for k in range(n + 1)]
    prof = alt + [(D, z_ust_w), (0.0, z_ust_p)]
    P = lambda u, v, sg: p + d * u + s * (sg * t / 2) + Z * v
    y.yuz_yon([P(u, v, 1) for u, v in prof], key, s)
    y.yuz_yon([P(u, v, -1) for u, v in prof], key, -s)
    m = len(prof)
    for i in range(m):
        (ua, va), (ub, vb) = prof[i], prof[(i + 1) % m]
        out = d * (vb - va) - Z * (ub - ua)
        if (ub - ua) ** 2 + (vb - va) ** 2 < 1e-12: continue
        y.yuz_yon([P(ua, va, -1), P(ub, vb, -1), P(ub, vb, 1), P(ua, va, 1)], key, out)
    # coping
    k = 0.004
    a0, a1 = P(0, z_ust_p, 0), P(D, z_ust_w, 0)
    cubuk(y, a0 + Z * (k * 0.5), a1 + Z * (k * 0.5), t + 0.006, kapak, k)


def acik_korkuluk(y, a, b, z, h, key='tas_acik', adim=0.018, t=0.012, ayak_key=None):
    """an open stone balustrade a->b (seen from both sides): a plinth, a top rail and small posts between"""
    a, b, L, e, nc = eksen(a, b)
    m = a.lerp(b, 0.5)
    kutu3(y, m + Z * (z + 0.004), e, nc, Z, L, t, 0.008, key, ('+x', '-x', '+y', '-y', '+z'))
    kutu3(y, m + Z * (z + h - 0.003), e, nc, Z, L + 0.002, t + 0.003, 0.006, key)
    k = max(1, int(round(L / adim)))
    for i in range(k + 1):
        pp = a.lerp(b, i / k)
        kutu3(y, pp + Z * (z + 0.008 + (h - 0.014) / 2), e, nc, Z, 0.0045 if 0 < i < k else 0.008, t * 0.7 if 0 < i < k else t,
              h - 0.014, ayak_key or key, ('+x', '-x', '+y', '-y'))


# ---------------------------------------------------------------- classical (Versailles, Invalides)
def vazo(y, x, yy, z, s=1.0, key='mermer', n=6):
    """an urn finial (Dolmabahce's) ~0.04 s tall"""
    donel(y, (x, yy), [(0, z), (0.009 * s, z), (0.006 * s, z + 0.006 * s), (0.011 * s, z + 0.014 * s), (0.01 * s, z + 0.022 * s),
                       (0.005 * s, z + 0.026 * s), (0.007 * s, z + 0.029 * s), (0.002 * s, z + 0.036 * s), (0, z + 0.04 * s)], key, n=n)


def korkuluk_klasik(y, kose, z, h, kapali=True, key='kirec', aralik=0.02, ayak=0.15, vazolu=True, vazo_key=None, heykelli=False,
                    heykel_key='kirec'):
    """a classical balustrade along a CCW polygon (or polyline): a plinth, turned balusters, a top rail, piers carrying
    urns (or statues: heykelli, alternating)"""
    m = len(kose)
    for i in range(m if kapali else m - 1):
        a, b, L, e, nc = eksen(kose[i], kose[(i + 1) % m])
        t = 0.016
        mid = a.lerp(b, 0.5)
        kutu3(y, mid + nc * (-t / 2 + t) * 0 + Z * (z + 0.005), e, nc, Z, L, t, 0.01, key, ('+y', '-y', '+z'))
        kutu3(y, mid + Z * (z + h - 0.004), e, nc, Z, L, t + 0.004, 0.008, key, ('+y', '-y', '+z', '-z'))
        np_ = max(1, int(round(L / ayak)))
        for j in range(np_ + 1):
            pp = a.lerp(b, j / np_)
            kutu3(y, pp + Z * (z + (h + 0.006) / 2), e, nc, Z, 0.022, 0.022, h + 0.006, key, ('+x', '-x', '+y', '-y', '+z'))
            if heykelli and j % 2 == 1:
                heykel(y, pp.x, pp.y, z + h + 0.006, 0.9, heykel_key, math.atan2(nc.y, nc.x) + math.pi / 2)
            elif vazolu and (j % 2 == 0 or j == np_):
                vazo(y, pp.x, pp.y, z + h + 0.006, 0.85, vazo_key or key)
        nb = int(L / aralik)
        for j in range(nb):
            u = (j + 0.5) / nb * L
            if min(abs(u - L * jj / np_) for jj in range(np_ + 1)) < 0.016: continue
            pp = a + e * u
            donel(y, (pp.x, pp.y), [(0.0032, z + 0.01), (0.0048, z + 0.016), (0.0026, z + h * 0.62), (0.0034, z + h - 0.008)], key, n=5)


def pilaster(y, p, e, nc, z0, h, w=0.02, d=0.006, key='kirec', bas=True):
    """a flat pilaster on a wall at p (e along the wall, nc out): base, shaft, capital"""
    o = V(p[0], p[1])
    kutu3(y, o + nc * (d / 2) + Z * (z0 + h / 2), e, nc, Z, w, d, h, key, ('+x', '-x', '+y', '+z'))
    if bas:
        kutu3(y, o + nc * ((d + 0.004) / 2) + Z * (z0 + 0.008), e, nc, Z, w + 0.008, d + 0.004, 0.016, key, ('+x', '-x', '+y', '+z'))
        kutu3(y, o + nc * ((d + 0.005) / 2) + Z * (z0 + h - 0.007), e, nc, Z, w + 0.01, d + 0.005, 0.014, key, ('+x', '-x', '+y', '+z', '-z'))


def ucgen_alinlik(y, L, e, nc, u0, u1, v, h, key='kirec', c=0.006):
    """a small triangular hood over a window: L(u, v) the wall point (u absolute along, v absolute z)"""
    A, B = L(u0, v), L(u1, v)
    T = (A + B) / 2 + Z * h
    o = nc * c
    y.yuz_yon([A + o, B + o, T + o], key, nc)
    for p, q in ((B, T), (T, A)):
        y.yuz_yon([p, q, q + o, p + o], key, (p + q) / 2 - (A + B) / 2)
    y.yuz_yon([A, B, B + o, A + o], key, -Z)


def kirma_basit(y, x0, x1, y0, y1, z, h, key, mahya=None):
    """a plain hipped roof (four faces) over the rectangle from z, h high at the ridge; mahya: a thin ridge cap key"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2, (y1 - y0) / 2
    if a >= b:
        r0, r1 = V(cx - (a - b), cy, z + h), V(cx + (a - b), cy, z + h)
    else:
        r0, r1 = V(cx, cy - (b - a), z + h), V(cx, cy + (b - a), z + h)
    A, B, C, D = V(x0, y0, z), V(x1, y0, z), V(x1, y1, z), V(x0, y1, z)
    if a >= b:
        y.yuz_yon([A, B, r1, r0], key, V(0, -1, 1)); y.yuz_yon([C, D, r0, r1], key, V(0, 1, 1))
        y.yuz_yon([D, A, r0], key, V(-1, 0, 1)); y.yuz_yon([B, C, r1], key, V(1, 0, 1))
    else:
        y.yuz_yon([B, C, r1, r0], key, V(1, 0, 1)); y.yuz_yon([D, A, r0, r1], key, V(-1, 0, 1))
        y.yuz_yon([A, B, r0], key, V(0, -1, 1)); y.yuz_yon([C, D, r1], key, V(0, 1, 1))
    if mahya and (r1 - r0).length > 1e-4:
        cubuk(y, r0 + Z * 0.0012, r1 + Z * 0.0012, 0.005, mahya, 0.003)
    return z + h


def mansard(y, x0, x1, y0, y1, z, h1, h2, key='arduvaz', ust_key='kursun', egim=0.38, sacak=0.012, alt_key='kirec', kalinlik=0.008,
            yaldiz=None):
    """a French (Mansart) roof over the wall rectangle: a steep lower slope (h1 high, leaning in egim x h1 from the wall
    line, its eave sacak out), a roll moulding at the break and a low hipped upper roof (h2, ust_key); yaldiz: a key
    (gilt) for a crest along the break. Returns (zb, (x0, x1, y0, y1) of the break, top z)"""
    k0 = disa(dikdortgen(x0, x1, y0, y1), sacak)
    w0 = dikdortgen(x0, x1, y0, y1)
    di = egim * h1
    k1 = disa(dikdortgen(x0, x1, y0, y1), -di)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for i in range(4):
        j = (i + 1) % 4
        m = (k0[i] + k0[j]) / 2
        out = V(m.x - cx, m.y - cy)
        y.yuz_yon([k0[i] + Z * z, k0[j] + Z * z, k1[j] + Z * (z + h1), k1[i] + Z * (z + h1)], key, out + Z * 0.2)
        y.yuz_yon([k0[i] + Z * z, k0[j] + Z * z, k0[j] + Z * (z - kalinlik), k0[i] + Z * (z - kalinlik)], alt_key, out)
        y.yuz_yon([k0[i] + Z * (z - kalinlik), k0[j] + Z * (z - kalinlik), w0[j] + Z * z, w0[i] + Z * z], alt_key, -Z)
    zb = z + h1
    xs = [p.x for p in k1]; ys = [p.y for p in k1]
    silme(y, [V(p.x, p.y) for p in k1], zb - 0.007, 0.007, 0.0045, ust_key, 'yarim')
    if yaldiz:
        silme(y, [V(p.x, p.y) for p in k1], zb - 0.0045, 0.002, 0.0062, yaldiz, 'duz')
    top = kirma_basit(y, min(xs), max(xs), min(ys), max(ys), zb - 0.001, h2, ust_key, mahya=yaldiz)
    return zb, (min(xs), max(xs), min(ys), max(ys)), top


def lukarn(y, a, e, nc, z, w, h, k, key='kirec', cati='kursun', cam='cam', yuvarlak=True, yaldiz='altin'):
    """a dormer standing on a mansard's lower slope: a the foot of its front (2D) on the eave line, e along, nc out,
    z the eave height, w x h its front; k the slope's inset per unit of height (the cheeks run back to it). A round-
    headed (or square) window, a small pediment and a lead roof, a gilt finial"""
    a = V(a[0], a[1]); e = V(e[0], e[1]).normalized(); nc = V(nc[0], nc[1]).normalized()
    F = lambda u, d, zz: a + e * u - nc * d + Z * zz
    p, q = F(-w / 2, 0, 0), F(w / 2, 0, 0)
    if yuvarlak:
        y.kemerli(V(p.x, p.y), V(q.x, q.y), z, h, (key, 'tas_koyu', 'tas_acik', cam), v0=h * 0.2, en=0.6, ust=0.005, derin=min(0.005, k * h * 0.15), k_say=4, sivri=0.0)
    else:
        dikdortgen_acik(y, V(p.x, p.y), V(q.x, q.y), z, h, 0.2, 0.8, h * 0.2, h * 0.86, (key, 'tas_koyu', 'tas_acik', cam), derin=min(0.005, k * h * 0.15))
    for s in (-1, 1):
        y.yuz_yon([F(s * w / 2, 0, z), F(s * w / 2, 0, z + h), F(s * w / 2, k * h, z + h)], key, e * s)
    ph = w * 0.36; o = 0.003
    A, B, T = F(-w / 2 - o, -o, z + h), F(w / 2 + o, -o, z + h), F(0, -o, z + h + ph)
    y.yuz_yon([A, B, T], key, nc)
    y.yuz_yon([A, B, F(w / 2 + o, 0.002, z + h), F(-w / 2 - o, 0.002, z + h)], key, -Z)
    for s, E in ((-1, A), (1, B)):
        y.yuz_yon([E, T, F(0, k * (h + ph) + 0.002, z + h + ph), F(s * (w / 2 + o), k * h + 0.002, z + h)], cati, e * s * 0.7 + Z)
    if yaldiz:
        piramit_cati(y, (T.x, T.y), 0.005, 0.005, T.z - 0.002, 0.011, yaldiz)


def korkuluk_hafif(y, kose, z, h, kapali=True, key='kirec', aralik=0.024, ayak=0.12, ust=None, ust_key=None, ust_adim=1):
    """a light classical balustrade along a CCW polygon (or polyline): plinth, square balusters, a top rail, piers;
    ust: 'vazo' urns or 'heykel' statues (alternating with urns) on every ust_adim-th pier"""
    m = len(kose)
    for i in range(m if kapali else m - 1):
        a, b, L, e, nc = eksen(kose[i], kose[(i + 1) % m])
        t = 0.014
        mid = a.lerp(b, 0.5)
        kutu3(y, mid + Z * (z + 0.004), e, nc, Z, L, t, 0.008, key, ('+y', '-y', '+z'))
        kutu3(y, mid + Z * (z + h - 0.0035), e, nc, Z, L, t + 0.004, 0.007, key, ('+y', '-y', '+z', '-z'))
        np_ = max(1, int(round(L / ayak)))
        for j in range(np_ + 1):
            pp = a.lerp(b, j / np_)
            kutu3(y, pp + Z * (z + (h + 0.004) / 2), e, nc, Z, 0.018, 0.019, h + 0.004, key, ('+x', '-x', '+y', '-y', '+z'))
            if ust and j % ust_adim == 0:
                if ust == 'heykel' and j % (2 * ust_adim) == ust_adim:
                    heykel(y, pp.x, pp.y, z + h + 0.004, 0.8, ust_key or key, math.atan2(nc.y, nc.x) + math.pi / 2, n=5)
                else:
                    donel(y, (pp.x, pp.y), [(0, z + h + 0.004), (0.007, z + h + 0.004), (0.005, z + h + 0.009), (0.009, z + h + 0.017),
                                            (0.004, z + h + 0.025), (0.0, z + h + 0.031)], ust_key or key, n=5)
        nb = int(L / aralik)
        for j in range(nb):
            u = (j + 0.5) / nb * L
            if min(abs(u - L * jj / np_) for jj in range(np_ + 1)) < 0.014: continue
            kutu3(y, a + e * u + Z * (z + h / 2), e, nc, Z, 0.0045, 0.0045, h - 0.014, key, ('+x', '-x', '+y', '-y'))


def atli_heykel(y, x, yy, z, aci=0.0, s=1.0, key='bronz', kaide='mermer', kaide_boy=None):
    """an equestrian statue on a moulded pedestal (Charlemagne, Louis XIV): a horse at a walk (barrel, chest, arched
    neck, head, tail, one foreleg raised) and its rider (legs astride, cloak, head, arm with a baton), ~0.07 s long"""
    kb = kaide_boy or 0.07 * s
    kutu_merkez(y, (x, yy), kb, 0.04 * s, 0.03 * s, kaide, z0=z, aci=aci)
    with parca(y, (x, yy, z), aci, s):
        kornis(y, -kb / s / 2, kb / s / 2, -0.02, 0.02, 0.026, 0.006, 0.004, kaide, 'duz')
        kornis(y, -kb / s / 2, kb / s / 2, -0.02, 0.02, 0.0, 0.006, 0.004, kaide, 'duz')
    with parca(y, (x, yy, z + 0.032 * s), aci, s):
        H_ = 0.034
        # the barrel and the chest, the hindquarters
        boru(y, [V(-0.021, 0, H_ + 0.001), V(-0.006, 0, H_), V(0.012, 0, H_ + 0.002)], 0.0088, key, n=8)
        kure(y, (0.013, 0, H_ + 0.002), 0.0092, key, n=8, kat=4)
        kure(y, (-0.02, 0, H_ + 0.002), 0.009, key, n=8, kat=4)
        # legs: hind pair planted, the near foreleg raised
        for lx, sg, up in ((-0.019, -1, 0), (-0.017, 1, 0), (0.014, -1, 0), (0.016, 1, 1)):
            if up:
                boru(y, [V(lx, sg * 0.0045, H_ - 0.004), V(lx + 0.007, sg * 0.0045, H_ - 0.014), V(lx + 0.004, sg * 0.0045, H_ - 0.024)], 0.0026, key, n=5,
                     r_son=0.0019)
            else:
                boru(y, [V(lx, sg * 0.0045, H_ - 0.004), V(lx + 0.001, sg * 0.0045, H_ * 0.45), V(lx, sg * 0.0045, 0.0)], 0.0026, key, n=5, r_son=0.002)
        # the arched neck and the head
        boru(y, [V(0.016, 0, H_ + 0.004), V(0.024, 0, H_ + 0.015), V(0.03, 0, H_ + 0.021)], 0.0052, key, n=6, r_son=0.0038)
        boru(y, [V(0.029, 0, H_ + 0.022), V(0.036, 0, H_ + 0.016), V(0.04, 0, H_ + 0.012)], 0.0036, key, n=6, r_son=0.0024)
        for sg in (-1, 1):   # ears
            boru(y, [V(0.029, sg * 0.0018, H_ + 0.024), V(0.028, sg * 0.0022, H_ + 0.029)], 0.0011, key, n=3, r_son=0.0003)
        boru(y, [V(-0.026, 0, H_ + 0.004), V(-0.031, 0, H_ - 0.004), V(-0.032, 0, H_ - 0.016)], 0.0028, key, n=4, r_son=0.0012)   # tail
        # the rider: legs astride, the body in a flaring cloak, the head, the arm holding the baton forward
        for sg in (-1, 1):
            boru(y, [V(-0.002, sg * 0.006, H_ + 0.009), V(0.004, sg * 0.0095, H_ + 0.001), V(0.002, sg * 0.0095, H_ - 0.009)], 0.0024, key, n=5)
        donel(y, (-0.001, 0), [(0.0085, H_ + 0.007), (0.006, H_ + 0.014), (0.0052, H_ + 0.024), (0.0065, H_ + 0.026), (0.0, H_ + 0.028)], key, n=7)
        kure(y, (0.0, 0, H_ + 0.0315), 0.0042, key, n=6, kat=3)
        boru(y, [V(0.0, -0.0062, H_ + 0.024), V(0.007, -0.009, H_ + 0.02), V(0.013, -0.009, H_ + 0.027)], 0.0016, key, n=4)
        boru(y, [V(0.013, -0.009, H_ + 0.027), V(0.02, -0.009, H_ + 0.033)], 0.0009, key, n=3)


def sutun_hafif(y, cx, cy, z0, z1, r, key='tas_acik', tur='iyon', n=8, bas_key=None):
    """a light classical column for many-columned fronts: a moulded base, a plain shaft, an Ionic (volute block) or
    Doric (echinus) capital with its abacus; ~70 triangles"""
    bk = bas_key or key
    c = (cx, cy)
    donel(y, c, [(r * 1.45, z0), (r * 1.45, z0 + r * 0.5), (r * 1.15, z0 + r * 0.8), (r, z0 + r * 1.1)], bk, n=n)
    zc = z1 - r * 1.6
    y.prizma(c, r, z0 + r * 1.1, zc, key, n=n, ust=False)
    if tur == 'iyon':
        kutu3(y, V(cx, cy, zc + r * 0.45), X, Y, Z, r * 2.8, r * 1.9, r * 0.9, bk, ('+x', '-x', '+y', '-y', '-z'))
    else:
        donel(y, c, [(r * 0.95, zc), (r * 1.35, zc + r * 0.9)], bk, n=n)
    kutu3(y, V(cx, cy, zc + r * 1.25), X, Y, Z, r * 2.9, r * 2.9, r * 0.7, bk, ('+x', '-x', '+y', '-y', '+z', '-z'))
    return z1
