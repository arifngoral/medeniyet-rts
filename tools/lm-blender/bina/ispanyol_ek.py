# Helpers for the later Spanish landmarks (lm_altinkule, lm_tercio, lm_escorial, lm_armada): a galleon (lofted hull
# with tumblehome, castles, gunports, masts, square and lateen sails, rigging) and its bare frame on a slipway,
# horseshoe-arched niches, stepped Almohad merlons, walls, soldiers (pikemen, arquebusiers), a crane, timber, guns.
# (lm_zeytinlik / lm_reconquista / lm_santiago / lm_toledo do not use this file.)
import math, random
from mathutils import Vector
from parcalar import *
from frank_ek import eksen, kutu3, levha


# ---------------------------------------------------------------- small things on walls
def pencere_k(y, a, b, u, v, w, h, key='koyu', d=0.006, cik=0.0012):
    """a small dark (or wooden) block set into the wall a->b (the wall faces the right of a->b): u along (units from a),
    v up (absolute z), w x h; standing cik proud"""
    a, b, L, e, nc = eksen(a, b)
    o = a + e * u + nc * cik
    kutu(y, o + Z * v + nc * 0.0, e, w, d, h, key, 'onsagsolust')


def almena(y, a, b, z, h, kalin=0.02, key='kum', w=None, g=None, tepe=0.5, uclar=True):
    """stepped-top (pyramid-capped) Almohad merlons along a->b, outer face on the line facing its right: boxes h high,
    kalin deep, each capped by a little pyramid tepe x h high"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-6: return
    e = (b - a) / L; nc = V(e.y, -e.x); ey = -nc
    w = w or h * 0.9; g = g or h * 0.75
    k = max(1, int(round((L + g) / (w + g))))
    if uclar: w = (L + g) / k - g
    for i in range(k):
        u = i * (w + g)
        ww = min(w, L - u)
        o = a + e * u + Z * z
        kutu(y, o, e, ww, kalin, h, key, 'onarkasagsol')
        p = [o + Z * h, o + e * ww + Z * h, o + e * ww + ey * kalin + Z * h, o + ey * kalin + Z * h]
        ap = (p[0] + p[2]) / 2 + Z * (h * tepe)
        for j in range(4):
            q0, q1 = p[j], p[(j + 1) % 4]
            y.yuz_yon([q0, q1, ap], key, (q0 + q1) / 2 - (p[0] + p[2]) / 2)


def sur_duvar(y, yol, z0, h, kalin=0.05, key='kum', ust_key='zemin', almena_h=0.035, kapali=False, ic=True, kornis_key=None):
    """a curtain wall along a polyline (outer face on the right of travel): faces both sides, the walk on top, a solid
    breastwork band and Almohad merlons on the outer edge, end faces when open. Returns the walk z"""
    yol = [V(p[0], p[1]) for p in yol]
    n = len(yol); m = n if kapali else n - 1
    icy = disa(yol, -kalin, kapali)
    zt = z0 + h
    for i in range(m):
        j = (i + 1) % n
        duz_duvar(y, yol[i], yol[j], z0, zt, key)
        if ic: duz_duvar(y, icy[j], icy[i], z0, zt, key)
        y.yuz_yon([yol[i] + Z * zt, yol[j] + Z * zt, icy[j] + Z * zt, icy[i] + Z * zt], ust_key, Z)
    if not kapali:
        for i, s in ((0, -1), (n - 1, 1)):
            e = (yol[1] - yol[0]) if i == 0 else (yol[-1] - yol[-2])
            y.yuz_yon([yol[i] + Z * z0, icy[i] + Z * z0, icy[i] + Z * zt, yol[i] + Z * zt], key, e * s)
    if kornis_key:
        silme(y, yol, zt - 0.012, 0.012, 0.006, kornis_key, 'duz', kapali)
    if almena_h:
        bk = kalin * 0.35
        for i in range(m):
            j = (i + 1) % n
            a, b = yol[i], yol[j]
            ee = (b - a).normalized()
            a2 = a + ee * (bk if (kapali or i > 0) else 0)
            almena(y, a2, b, zt, almena_h, bk, key)
    return zt


# ---------------------------------------------------------------- horseshoe arches (Andalusian / Mudejar)
def nal_nis(y, a, b, z0, H, en=0.6, ust=0.03, alfa=0.42, derin=0.012, key='tugla_sari', yan_key='tas_koyu',
            arka_key='koyu', v0=0.0, k_say=12, cerceve=None, alfiz=None):
    """a wall bay a->b (facing the right of a->b) with a horseshoe-arched opening derin deep: the arc runs past the
    half circle by alfa (radians) on each side, its widest part wider than the jambs. The wall face round it (fanned
    from the arc's centre), the reveal, a back (arka_key; None leaves it open), cerceve = (width, key): a raised arc
    band, alfiz = (width, key): the raised rectangular frame round the arch. Returns (L, x0, x1, hs, crown)"""
    a, b, W, e, nc = eksen(a, b)
    L = lambda u, v, d=0.0: a + e * u - nc * d + Z * (z0 + v)
    w = en * W; x0, x1 = (W - w) / 2, (W + w) / 2; xm = W / 2
    Rr = (w / 2) / math.cos(alfa)
    hc = H - ust - Rr
    hs = hc - Rr * math.sin(alfa)
    t0, t1 = math.pi + alfa, -alfa
    th = [t0 + (t1 - t0) * k / k_say for k in range(k_say + 1)]
    for tc in (math.atan2(H - hc, -xm), math.atan2(H - hc, W - xm)):
        if t1 < tc < t0: th.append(tc)
    th = sorted(set(th), reverse=True)
    A = lambda t: (xm + Rr * math.cos(t), hc + Rr * math.sin(t))

    def B(t):
        c, s = math.cos(t), math.sin(t)
        cand = []
        if c < -1e-9: cand.append((0 - xm) / c)
        if c > 1e-9: cand.append((W - xm) / c)
        if s > 1e-9: cand.append((H - hc) / s)
        tt = min(cand)
        return (xm + c * tt, hc + s * tt)
    for k in range(len(th) - 1):
        p, q = th[k], th[k + 1]
        pts = [L(*A(p)), L(*A(q)), L(*B(q)), L(*B(p))]
        y.yuz_yon(pts, key, nc)
    vl, vr = B(t0)[1], B(t1)[1]
    y.yuz_yon([L(0, 0), L(x0, 0), L(x0, hs), L(0, vl)], key, nc)
    y.yuz_yon([L(x1, 0), L(W, 0), L(W, vr), L(x1, hs)], key, nc)
    if v0 > 0:
        y.yuz_yon([L(x0, 0), L(x1, 0), L(x1, v0), L(x0, v0)], key, nc)
    yol = [(x0, v0), (x0, hs)] + [A(t) for t in [t0 + (t1 - t0) * k / k_say for k in range(1, k_say)]] + [(x1, hs), (x1, v0)]
    for k in range(len(yol) - 1):
        p, q = yol[k], yol[k + 1]
        vm = min(max((p[1] + q[1]) / 2, v0), hc)
        mid = (L(*p) + L(*q)) / 2
        y.yuz_yon([L(*p), L(*q), L(*q, derin), L(*p, derin)], yan_key, L(xm, vm) - mid)
    if v0 > 0:
        y.yuz_yon([L(x0, v0), L(x1, v0), L(x1, v0, derin), L(x0, v0, derin)], yan_key, Z)
    if arka_key:
        y.yuz_yon([L(*p, derin) for p in yol], arka_key, nc)
    if cerceve:
        f, ck = cerceve
        d = -0.0022
        ts = [t0 + (t1 - t0) * k / k_say for k in range(k_say + 1)]
        P = lambda t, r, dd: L(xm + r * math.cos(t), hc + r * math.sin(t), dd)
        for k in range(k_say):
            p, q = ts[k], ts[k + 1]
            y.yuz_yon([P(p, Rr, d), P(q, Rr, d), P(q, Rr + f, d), P(p, Rr + f, d)], ck, nc)
            y.yuz_yon([P(p, Rr + f, d), P(q, Rr + f, d), P(q, Rr + f, 0), P(p, Rr + f, 0)], ck, (P(p, 1, 0) + P(q, 1, 0)) / 2 - L(xm, hc))
            y.yuz_yon([P(p, Rr, d), P(q, Rr, d), P(q, Rr, 0), P(p, Rr, 0)], ck, L(xm, hc) - (P(p, 1, 0) + P(q, 1, 0)) / 2)
        for t in (t0, t1):   # the band's ends
            y.yuz_yon([P(t, Rr, d), P(t, Rr + f, d), P(t, Rr + f, 0), P(t, Rr, 0)], ck, -Z)
    if alfiz:
        f, ck = alfiz
        ua, ub = xm - Rr - f * 2.2, xm + Rr + f * 2.2
        va, vb = hs, min(H - f * 0.2, hc + Rr + f * 2.2)
        dd = 0.0035
        for (pu0, pv0, pu1, pv1) in ((ua, va, ua + f, vb), (ub - f, va, ub, vb), (ua + f, vb - f, ub - f, vb)):
            o = L(pu0, pv0) + nc * dd
            kutu(y, o, e, pu1 - pu0, dd, pv1 - pv0, ck, 'onsagsolust')
    return L, x0, x1, hs, hc + Rr


# ---------------------------------------------------------------- galleon
def _kesit(t, L, B, H, D):
    """the hull's section at t (0 stern .. 1 bow): x, rows (half-width, z) from the keel up, the rail z"""
    x = -L / 2 + L * t
    if t <= 0.4: f = 0.76 + 0.24 * math.sin(math.pi / 2 * t / 0.4)
    elif t <= 0.55: f = 1.0
    else: f = max(0.06, math.cos(math.pi / 2 * (t - 0.55) / 0.45) ** 0.8)
    w = B / 2 * f
    zt = H * ((1 + 0.36 * ((0.5 - t) / 0.5) ** 2) if t < 0.5 else (1 + 0.22 * ((t - 0.5) / 0.5) ** 2))
    if t < 0.14: kz = -D + D * 0.45 * ((0.14 - t) / 0.14) ** 1.5
    elif t < 0.74: kz = -D
    else: kz = -D + D * 1.1 * ((t - 0.74) / 0.26) ** 1.7
    rows = [(0.0, kz), (0.7, -D * 0.62), (0.97, 0.0), (1.0, zt * 0.36), (0.95, zt * 0.68), (0.86, zt)]
    out = []; zp = None
    for k, (fw, fz) in enumerate(rows):
        if zp is not None: fz = max(fz, zp + 0.0015)
        out.append((w * fw, fz)); zp = fz
    return x, out, zt, w


GOVDE = ('ahsap_koyu', 'ahsap_koyu', 'ahsap', 'boya_kirmizi', 'boya_sari')


def _yelken(y, c, sw, sh, bombe, keys=('beyaz', 'boya_kirmizi'), nu=12, nv=9, kalin=0.0022, carpi=True, daral=0.12):
    """a square sail hanging from a yard centred at c (3D, local frame: x forward), sw wide, sh deep, bellied forward
    by bombe: a closed thin sheet, the ragged red saltire (cross of Burgundy) in its cells if carpi"""
    c = Vector(c)
    def F(u, v):
        b = bombe * (0.4 + 0.6 * math.sin(math.pi * u)) * math.sin(math.pi * 0.5 * v)
        return c + V(b + 0.004, (u - 0.5) * sw * (1 - daral * v), -v * sh)
    Bk = lambda u, v: F(u, v) - X * kalin
    for i in range(nu):
        for j in range(nv):
            u0, u1, v0, v1 = i / nu, (i + 1) / nu, j / nv, (j + 1) / nv
            uc, vc = (u0 + u1) / 2, (v0 + v1) / 2
            k = keys[1] if carpi and (abs(uc - vc) < 0.065 or abs(uc + vc - 1) < 0.065) else keys[0]
            y.yuz_yon([F(u0, v0), F(u1, v0), F(u1, v1), F(u0, v1)], k, X)
            y.yuz_yon([Bk(u0, v0), Bk(u1, v0), Bk(u1, v1), Bk(u0, v1)], k, -X)
    for i in range(nu):   # top and foot edges
        u0, u1 = i / nu, (i + 1) / nu
        y.yuz_yon([F(u0, 0), F(u1, 0), Bk(u1, 0), Bk(u0, 0)], keys[0], Z)
        y.yuz_yon([F(u0, 1), F(u1, 1), Bk(u1, 1), Bk(u0, 1)], keys[0], -Z)
    for j in range(nv):   # the leeches
        v0, v1 = j / nv, (j + 1) / nv
        y.yuz_yon([F(0, v0), F(0, v1), Bk(0, v1), Bk(0, v0)], keys[0], -Y)
        y.yuz_yon([F(1, v0), F(1, v1), Bk(1, v1), Bk(1, v0)], keys[0], Y)


def _flama(y, p, L, h, key='boya_kirmizi', yon=1.0):
    """a long tapering pennant from the point p streaming along +x (yon -1: -x)"""
    p = Vector(p)
    n = 4
    pts_u = [p + V(yon * L * k / n, 0.0, -h * 0.5 * k / n + 0.004 * math.sin(k * 1.7)) for k in range(n + 1)]
    for k in range(n):
        a0, a1 = pts_u[k], pts_u[k + 1]
        h0, h1 = h * (1 - k / n), h * (1 - (k + 1) / n) + 0.0008
        levha(y, [a0, a1, a1 - Z * h1, a0 - Z * h0], key, V(0, 1, 0), kil=0.0012)


def kalyon(y, cx, cy, z, aci, L=0.6, B=0.15, yelken='acik', renk=GOVDE, sancakli=True, flama='boya_kirmizi', tohum=1,
           direkler=True, topcu=True):
    """a 16th-century galleon at (cx, cy) with its waterline at z, the bow towards aci: a lofted hull with tumblehome
    (dark below the waterline, a red gun deck band with gunports and guns, a yellow upper band), the decks and
    bulwarks, a two-tier sterncastle with a galleried transom and a lantern, a forecastle, the beakhead and the
    bowsprit, four masts (fore and main square-rigged: yelken 'acik' set sails with the red saltire, 'sarili' furled on
    the yards; mizzen and bonaventure lateen), shrouds and stays, pennants (sancakli: the team flag on the main)"""
    H, D = B * 0.5, B * 0.42
    n = 16
    with parca(y, (cx, cy, z), aci):
        K = [_kesit(i / n, L, B, H, D) for i in range(n + 1)]
        P = lambda i, j, s: V(K[i][0], s * K[i][1][j][0], K[i][1][j][1])
        for i in range(n):
            for s in (-1, 1):
                for j in range(5):
                    y.yuz_yon([P(i, j, s), P(i + 1, j, s), P(i + 1, j + 1, s), P(i, j + 1, s)], renk[j], V(0, s, 0))
        for i, sg in ((0, -1), (n, 1)):
            pts = [P(i, j, -1) for j in range(6)] + [P(i, j, 1) for j in range(5, 0, -1)]
            y.yuz_yon(pts, 'ahsap_koyu' if sg > 0 else renk[3], V(sg, 0, 0))
        # deck, bulwarks' inner faces, rail caps
        Dk = lambda i, s: V(K[i][0], s * K[i][3] * 0.8, K[i][2] * 0.8)
        R = lambda i, s, f=0.86: V(K[i][0], s * K[i][3] * f, K[i][2])
        for i in range(n):
            y.yuz_yon([Dk(i, -1), Dk(i + 1, -1), Dk(i + 1, 1), Dk(i, 1)], 'ahsap_acik', Z)
            for s in (-1, 1):
                y.yuz_yon([Dk(i, s), Dk(i + 1, s), R(i + 1, s, 0.8), R(i, s, 0.8)], 'ahsap', V(0, -s, 0.2))
                y.yuz_yon([R(i, s), R(i + 1, s), R(i + 1, s, 0.8), R(i, s, 0.8)], 'boya_sari', Z)
        # (the stern's inside is under the castle; the bow's inner face a hair behind the stem's cap)
        y.yuz_yon([Dk(n, 1) - X * 0.002, Dk(n, -1) - X * 0.002, R(n, -1, 0.8) - X * 0.002, R(n, 1, 0.8) - X * 0.002], 'ahsap', -X)
        # a wale (rubbing strake) along the top of the red band, the sternpost rudder
        for s in (-1, 1):
            pts = [P(i, 4, s) + V(0, s * 0.002, 0) for i in range(1, n)]
            boru(y, pts, B * 0.018, 'ahsap_koyu', n=4)
        kutu3(y, V(-L / 2 - 0.005, 0, (K[0][1][0][1] + K[0][1][3][1]) / 2), X, Y, Z, 0.012, 0.008, K[0][1][3][1] - K[0][1][0][1], 'ahsap_koyu')
        # gunports and guns on the red band
        if topcu:
            for i in range(3, n - 3):
                if i % 2: continue
                for s in (-1, 1):
                    q = [P(i, 3, s), P(i + 1, 3, s), P(i + 1, 4, s), P(i, 4, s)]
                    c = sum(q, Vector()) / 4
                    nr = (q[1] - q[0]).cross(q[3] - q[0]).normalized()
                    if nr.y * s < 0: nr = -nr
                    ex = (q[1] - q[0]).normalized(); ez = nr.cross(ex).normalized()
                    if ez.z < 0: ez = -ez
                    g = L * 0.022
                    y.yuz_yon([c + nr * 0.0012 + ex * gx + ez * gz for gx, gz in ((-g / 2, -g / 2), (g / 2, -g / 2), (g / 2, g / 2), (-g / 2, g / 2))], 'koyu', nr)
                    cubuk(y, c - nr * 0.002, c + nr * (L * 0.022), g * 0.42, 'bronz')
        # the sterncastle: two tiers
        def kasara(i0, i1, za_of, hh, wf, key, ust_key='ahsap_acik', pencere=True, ray=True, kic_pencere=True):
            ids = list(range(i0, i1 + 1))
            alt = [(K[i][0], -K[i][3] * wf, za_of(i)) for i in ids] + [(K[i][0], K[i][3] * wf, za_of(i)) for i in reversed(ids)]
            ust = [(p[0], p[1], p[2] + hh) for p in alt]
            m = len(alt)
            for k in range(m):
                a, b = V(*alt[k]), V(*alt[(k + 1) % m])
                ee = (b - a); ee.z = 0; ee.normalize()
                y.yuz_yon([a, b, V(*ust[(k + 1) % m]), V(*ust[k])], key, V(ee.y, -ee.x))
            h2 = len(ids)
            for k in range(h2 - 1):
                y.yuz_yon([V(*ust[k]), V(*ust[k + 1]), V(*ust[m - 2 - k]), V(*ust[m - 1 - k])], ust_key, Z)
            # trim band along the top, windows along the sides
            for k in range(m):
                a, b = V(*ust[k]), V(*ust[(k + 1) % m])
                ee = (b - a); ee.z = 0
                if ee.length < 1e-6: continue
                ee.normalize(); nn = V(ee.y, -ee.x)
                cubuk(y, a + nn * 0.0015 - Z * 0.004, b + nn * 0.0015 - Z * 0.004, 0.006, 'boya_sari', 0.003)
                kic = max(a.x, b.x) < -L / 2 + 1e-4   # (the transom: its own framed windows are drawn below)
                if pencere and (b - a).length > hh * 0.9 and (kic_pencere or not kic):
                    nw = max(1, int((b - a).length / (hh * 1.1)))
                    for q in range(nw):
                        mm = a.lerp(b, (q + 0.5) / nw)
                        ww = min(hh * 0.4, (b - a).length / nw * 0.5)
                        y.yuz_yon([mm + nn * 0.0012 + ee * (-ww / 2) - Z * hh * 0.72, mm + nn * 0.0012 + ee * (ww / 2) - Z * hh * 0.72,
                                   mm + nn * 0.0012 + ee * (ww / 2) - Z * hh * 0.3, mm + nn * 0.0012 + ee * (-ww / 2) - Z * hh * 0.3], 'koyu', nn)
            if ray:   # a light railing round the top
                for k in range(m):
                    a, b = V(*ust[k]), V(*ust[(k + 1) % m])
                    if (b - a).length < 1e-6: continue
                    cubuk(y, a + Z * 0.012, b + Z * 0.012, 0.003, 'ahsap_koyu')
                    nst = max(1, int((b - a).length / 0.02))
                    for q in range(nst):
                        pp = a.lerp(b, q / nst)
                        cubuk(y, pp, pp + Z * 0.012, 0.0025, 'ahsap_koyu')
            return ust
        ia, ib = int(n * 0.3), int(n * 0.16)
        hc1, hc2 = H * 0.62, H * 0.5
        u1 = kasara(0, ia, lambda i: K[i][2] * 0.8, hc1 + K[0][2] * 0.2, 0.84, 'boya_kirmizi', ray=False, kic_pencere=False)
        zt1 = lambda i: K[i][2] * 0.8 + hc1 + K[0][2] * 0.2
        u2 = kasara(0, ib, zt1, hc2, 0.78, 'boya_kirmizi')
        # the galleried transom: a balcony across the stern under the top tier, posts, the lantern
        x0 = -L / 2
        zg = zt1(0)
        kutu3(y, V(x0 - 0.012, 0, zg - 0.002), X, Y, Z, 0.024, K[0][3] * 1.5, 0.004, 'ahsap_koyu')
        for k in range(7):
            yy = -K[0][3] * 0.72 + K[0][3] * 1.44 * k / 6
            cubuk(y, V(x0 - 0.022, yy, zg), V(x0 - 0.022, yy, zg + hc2 * 0.42), 0.003, 'boya_sari')
        cubuk(y, V(x0 - 0.022, -K[0][3] * 0.74, zg + hc2 * 0.42), V(x0 - 0.022, K[0][3] * 0.74, zg + hc2 * 0.42), 0.0035, 'boya_sari')
        for k in range(3):   # stern windows on the lower tier's transom, each in a gilt frame
            yy = (k - 1) * K[0][3] * 0.5
            y.yuz_yon([V(x0 - 0.0015, yy - 0.008, zg - hc1 * 0.75), V(x0 - 0.0015, yy + 0.008, zg - hc1 * 0.75),
                       V(x0 - 0.0015, yy + 0.008, zg - hc1 * 0.3), V(x0 - 0.0015, yy - 0.008, zg - hc1 * 0.3)], 'koyu', -X)
            fz0, fz1, fw = zg - hc1 * 0.75, zg - hc1 * 0.3, 0.0028
            for (ya, yb, za, zb_) in ((yy - 0.008 - fw, yy - 0.008, fz0 - fw, fz1 + fw), (yy + 0.008, yy + 0.008 + fw, fz0 - fw, fz1 + fw),
                                      (yy - 0.008, yy + 0.008, fz1, fz1 + fw), (yy - 0.008, yy + 0.008, fz0 - fw, fz0)):
                kutu3(y, V(x0 - 0.0015, (ya + yb) / 2, (za + zb_) / 2), X, Y, Z, 0.003, yb - ya, zb_ - za, 'altin', ('-x', '+y', '-y', '+z', '-z'))
        # the royal arms carved on the upper tier's transom, behind the gallery's balusters
        za_ = zg + hc2 * 0.5
        sh = [V(x0 - 0.0016, -0.012, za_ + 0.012), V(x0 - 0.0016, 0.012, za_ + 0.012), V(x0 - 0.0016, 0.012, za_ - 0.004),
              V(x0 - 0.0016, 0.0, za_ - 0.014), V(x0 - 0.0016, -0.012, za_ - 0.004)]
        y.yuz_yon(sh, 'altin', -X)
        y.yuz_yon([V(x0 - 0.0024, -0.0085, za_ + 0.009), V(x0 - 0.0024, 0.0, za_ + 0.009), V(x0 - 0.0024, 0.0, za_ - 0.001),
                   V(x0 - 0.0024, -0.0085, za_ - 0.001)], 'boya_kirmizi', -X)
        y.yuz_yon([V(x0 - 0.0024, 0.0, za_ - 0.001), V(x0 - 0.0024, 0.0085, za_ - 0.001), V(x0 - 0.0024, 0.0085, za_ - 0.007),
                   V(x0 - 0.0024, 0.0, za_ - 0.01)], 'boya_kirmizi', -X)
        zl = zt1(0) + hc2
        donel(y, (x0 + 0.02, 0), [(0.0, zl), (0.006, zl), (0.012, zl + 0.006), (0.01, zl + 0.026), (0.013, zl + 0.03), (0.0, zl + 0.046)], 'altin', n=6)
        # the forecastle
        f0, f1 = int(n * 0.78), n - 1
        hf = H * 0.55
        kasara(f0, f1, lambda i: K[i][2] * 0.8, hf + H * 0.2, 0.84, 'boya_kirmizi', pencere=False)
        # beakhead and bowsprit, a figurehead
        xb, zb = L / 2, K[n][2]
        bp = [V(xb - 0.01, 0, zb * 0.45), V(xb + L * 0.11, 0, zb * 0.78)]
        cubuk(y, bp[0], bp[1], B * 0.14, 'boya_kirmizi', B * 0.1)
        kure(y, bp[1] + V(0.004, 0, 0.004), B * 0.06, 'altin', n=8, kat=4)
        bs0, bs1 = V(xb - L * 0.05, 0, zb + hf * 0.8), V(xb + L * 0.3, 0, zb + L * 0.2)
        boru(y, [bs0, bs1], L * 0.006, 'ahsap', n=6, r_son=L * 0.004)
        if not direkler:
            return
        # masts
        Lm = L * 0.95
        direk = [(0.79, 0.78, True), (0.5, 0.92, True), (0.25, 0.6, False), (0.08, 0.42, False)]
        tepeler = []
        for t, hm, kare in direk:
            i = t * n
            xm = -L / 2 + L * t
            i0 = int(i)
            zd = K[i0][2] * 0.8
            if t < 0.32: zd = zt1(min(i0, ia)) if t > 0.17 else zl - 0.002
            h = Lm * hm
            rm = L * (0.011 if kare else 0.008)
            ztop = zd + h
            y.prizma((xm, 0), rm, zd - 0.01, zd + h * 0.62, 'ahsap', n=6)
            y.prizma((xm, 0), rm * 0.65, zd + h * 0.62, ztop, 'ahsap', n=6)
            tepeler.append((xm, ztop, zd, h, kare))
            if kare:   # the top (crow's nest)
                zn = zd + h * 0.6
                donel(y, (xm, 0), [(0.0, zn - 0.004), (rm * 1.3, zn - 0.004), (rm * 2.8, zn + 0.004), (rm * 2.9, zn + 0.016), (rm * 2.2, zn + 0.016),
                                   (0.0, zn + 0.0161)], 'ahsap_koyu', n=8)
                sw = B * (2.5 if hm > 0.85 else 2.15)
                for zy, ww, hh in ((zd + h * 0.55, sw, h * 0.37), (zd + h * 0.93, sw * 0.7, h * 0.27)):
                    boru(y, [V(xm + rm * 1.2, -ww * 0.56, zy), V(xm + rm * 1.2, ww * 0.56, zy)], L * 0.005, 'ahsap', n=5, r_son=None)
                    if yelken == 'acik':
                        _yelken(y, V(xm + rm * 1.2, 0, zy - 0.003), ww, hh, ww * 0.14, carpi=hh > h * 0.3)
                    elif yelken == 'sarili':
                        boru(y, [V(xm + rm * 2.2, -ww * 0.47, zy - 0.006), V(xm + rm * 2.2, ww * 0.47, zy - 0.006)], L * 0.011, 'kumas', n=6)
            else:   # lateen yard and sail
                A_ = V(xm - L * 0.15, 0, zd + h * 0.28)
                B_ = V(xm + L * 0.1, 0, zd + h * 1.02)
                boru(y, [A_, B_], L * 0.0045, 'ahsap', n=5)
                if yelken == 'acik':
                    C_ = V(xm + L * 0.06, 0, zd + h * 0.1)
                    levha(y, [A_ + V(0, 0.004, 0), B_ + V(0, 0.004, -0.004), C_ + V(0, 0.004, 0)], 'beyaz', Y, kil=0.0022)
                elif yelken == 'sarili':
                    boru(y, [A_.lerp(B_, 0.1) - Z * 0.006, A_.lerp(B_, 0.85) - Z * 0.006], L * 0.008, 'kumas', n=6)
        # shrouds and stays
        for xm, ztop, zd, h, kare in tepeler:
            i0 = min(n, max(0, int((xm + L / 2) / L * n + 0.5)))
            for s in (-1, 1):
                for k in (-1, 0, 1):
                    xr = xm + k * L * 0.022 - L * 0.015
                    ii = min(n, max(0, int((xr + L / 2) / L * n + 0.5)))
                    cubuk(y, V(xm, 0, zd + h * (0.6 if kare else 0.7)), V(xr, s * K[ii][3] * 0.86, max(K[ii][2], zd - 0.004) + 0.002), 0.0016, 'ahsap_koyu')
        (xf, zf, _, _, _), (xmn, zmn, _, _, _) = tepeler[0], tepeler[1]
        cubuk(y, V(xmn, 0, zmn - 0.01), V(xf, 0, K[int(0.79 * n)][2] * 0.8 + 0.02), 0.0016, 'ahsap_koyu')
        cubuk(y, V(xf, 0, zf - 0.01), bs1, 0.0016, 'ahsap_koyu')
        cubuk(y, V(tepeler[2][0], 0, tepeler[2][1] - 0.01), V(xmn, 0, tepeler[1][2] + tepeler[1][3] * 0.5), 0.0016, 'ahsap_koyu')
        # pennants on the mast heads, the team flag on the main
        for k, (xm, ztop, zd, h, kare) in enumerate(tepeler):
            if k == 1 and sancakli:
                y.prizma((xm, 0), 0.0025, ztop, ztop + 0.03, 'ahsap', n=4)
                levha(y, [V(xm + 0.003, 0, ztop + 0.03), V(xm + 0.07, 0, ztop + 0.026), V(xm + 0.07, 0, ztop + 0.0), V(xm + 0.003, 0, ztop + 0.004)], 'mavi', Y, kil=0.0015)
            elif flama:
                _flama(y, V(xm, 0, ztop + 0.002), L * 0.14, 0.014, flama)


def kalyon_iskelet(y, cx, cy, z, aci, L=0.9, B=0.22, kaplama=0.45, iskele=True):
    """a galleon being built, its waterline-to-be at z (the keel D below): keel, stem and sternpost, the ribs (frames)
    over the whole length with the planking done on the lower hull over kaplama of the length (from the stern), deck
    beams; shores propping it and, with iskele, scaffold posts with walkway planks along both sides"""
    H, D = B * 0.5, B * 0.42
    n = 16
    with parca(y, (cx, cy, z), aci):
        K = [_kesit(i / n, L, B, H, D) for i in range(n + 1)]
        P = lambda i, j, s: V(K[i][0], s * K[i][1][j][0], K[i][1][j][1])
        # keel, stem, sternpost
        cubuk(y, V(-L / 2, 0, -D - 0.004), V(L * 0.24, 0, -D - 0.004), B * 0.06, 'ahsap_koyu', B * 0.07)
        stem = [P(i, 0, 1) for i in range(int(n * 0.74), n + 1)] + [P(n, 5, 1) + V(0.01, 0, 0.0)]
        boru(y, [V(L * 0.24, 0, -D - 0.004)] + stem[1:], B * 0.035, 'ahsap_koyu', n=4)
        cubuk(y, V(-L / 2 - 0.004, 0, -D - 0.006), V(-L / 2 - 0.014, 0, K[0][2] + 0.01), B * 0.05, 'ahsap_koyu', B * 0.06)
        # frames
        np_ = int(n * kaplama)
        for i in range(1, n):
            ust = 5 if i % 2 == 0 else 4
            for s in (-1, 1):
                pts = [P(i, j, s) + V(0, s * 0.002, 0) for j in range(0, ust + 1)]
                boru(y, pts, B * 0.022, 'ahsap_acik', n=4, kapat=True)
            if i % 2 == 0:   # a deck beam
                cubuk(y, V(K[i][0], -K[i][3] * 0.9, K[i][2] * 0.68), V(K[i][0], K[i][3] * 0.9, K[i][2] * 0.68), B * 0.035, 'ahsap')
        # planking on the stern part, rows up to the waterline-band; each plank strake a closed thin skin
        for i in range(np_):
            for s in (-1, 1):
                for j in range(3):
                    q = [P(i, j, s), P(i + 1, j, s), P(i + 1, j + 1, s), P(i, j + 1, s)]
                    y.yuz_yon(q, 'ahsap', V(0, s, 0))
                    y.yuz_yon([p - V(0, s * 0.004, 0) for p in q], 'ahsap_koyu', V(0, -s, 0))
            if i == np_ - 1:   # the planking's raw edge (closed)
                for s in (-1, 1):
                    for j in range(3):
                        a, b = P(i + 1, j, s), P(i + 1, j + 1, s)
                        y.yuz_yon([a, b, b - V(0, s * 0.004, 0), a - V(0, s * 0.004, 0)], 'ahsap_acik', X)
        y.yuz_yon([P(0, j, -1) for j in range(4)] + [P(0, j, 1) for j in range(3, 0, -1)], 'ahsap', -X)
        y.yuz_yon([P(0, j, 1) - V(0.004, 0, 0) for j in range(4)] + [P(0, j, -1) - V(0.004, 0, 0) for j in range(3, 0, -1)], 'ahsap_koyu', X)
        for s in (-1, 1):   # the top edge of the planking strake at row 3
            for i in range(np_):
                a, b = P(i, 3, s), P(i + 1, 3, s)
                y.yuz_yon([a, b, b - V(0, s * 0.004, 0), a - V(0, s * 0.004, 0)], 'ahsap_acik', Z)
        # shores and scaffold
        zg = -D - 0.004 - B * 0.035 - 0.03   # (the caller's keel blocks are 0.03 high)
        for i in range(2, n - 1, 2):
            for s in (-1, 1):
                p = P(i, 2, s)
                cubuk(y, p, V(p.x, s * (abs(p.y) + B * 0.5), zg), B * 0.028, 'ahsap')
        if iskele:
            for s in (-1, 1):
                yo = s * (B * 0.5 + B * 0.25)
                xs = [-L * 0.45 + L * 0.9 * k / 6 for k in range(7)]
                for xx in xs:
                    cubuk(y, V(xx, yo, zg), V(xx, yo, H * 1.25), B * 0.025, 'ahsap_koyu')
                for zz in (H * 0.15, H * 0.95):
                    kutu3(y, V(0, yo - s * B * 0.06, zz), X, Y, Z, L * 0.92, B * 0.14, 0.004, 'ahsap_acik')
                    cubuk(y, V(-L * 0.45, yo, zz + 0.025), V(L * 0.45, yo, zz + 0.025), B * 0.015, 'ahsap_koyu')
                for k in range(6):   # cross braces
                    cubuk(y, V(xs[k], yo, zg + 0.01), V(xs[k + 1], yo, H * 0.15), B * 0.015, 'ahsap_koyu')


# ---------------------------------------------------------------- people
TEN = 'siva_krem'


def asker(y, x, yy, z, s=1.0, aci=0.0, silah='pike', govde='boya_kirmizi', pantolon='boya_sari', zirh=True, ates=False, tohum=0):
    """a Spanish soldier about 0.07 x s tall facing aci: legs, a doublet (govde) or a steel corselet (zirh), a morion
    helmet with its comb and brim, arms; silah: 'pike' (upright pike), 'pike_egik' (levelled), 'arkebuz' (aimed;
    ates: a smoke puff at the muzzle), 'tufek_omuz' (shouldered), 'halbert', None"""
    with parca(y, (x, yy, z), aci, s):
        e = X; n_ = Y
        for k in (-1, 1):   # legs (dark shoes at the foot)
            kutu3(y, V(0, k * 0.0055, 0.015), X, Y, Z, 0.006, 0.0055, 0.026, pantolon, ('+x', '-x', '+y', '-y'))
            kutu3(y, V(0.0015, k * 0.0055, 0.001), X, Y, Z, 0.009, 0.0062, 0.004, 'ahsap_koyu', ('+x', '-x', '+y', '-y', '+z'))
        # puffed breeches, torso
        donel(y, (0, 0), [(0.0, 0.026), (0.012, 0.028), (0.0115, 0.035), (0.0, 0.0361)], pantolon, n=6)
        donel(y, (0, 0), [(0.0, 0.034), (0.0105, 0.04), (0.0105, 0.054), (0.006, 0.058), (0.0, 0.0581)],
              'demir' if zirh else govde, n=6)
        kure(y, (0, 0, 0.0645), 0.0058, TEN, n=6, kat=3)
        # morion: brim, dome, comb
        donel(y, (0, 0), [(0.0, 0.0655), (0.0105, 0.0655), (0.0075, 0.0685), (0.0045, 0.073), (0.0, 0.0745)], 'demir', n=6)
        levha(y, [V(-0.006, 0, 0.0705), V(0.006, 0, 0.0705), V(0.004, 0, 0.0775), V(-0.004, 0, 0.0775)], 'demir', Y, kil=0.0016)
        kol = govde
        sh = V(0, 0.0095, 0.054); sh2 = V(0, -0.0095, 0.054)
        if silah in ('pike', 'halbert'):
            el = V(0.006, 0.012, 0.04)
            boru(y, [sh, el], 0.0026, kol, n=4)
            boru(y, [sh2, V(0.003, -0.011, 0.034)], 0.0026, kol, n=4)
            top = 0.21 if silah == 'pike' else 0.11
            cubuk(y, V(0.006, 0.014, 0.004), V(0.006, 0.014, top), 0.0022, 'ahsap')
            if silah == 'pike':
                boru(y, [V(0.006, 0.014, top), V(0.006, 0.014, top + 0.012)], 0.0022, 'demir', n=4, r_son=0.0004)
            else:
                levha(y, [V(0.006, 0.014, top - 0.012), V(0.016, 0.014, top - 0.008), V(0.016, 0.014, top + 0.002), V(0.006, 0.014, top)], 'demir', Y)
                boru(y, [V(0.006, 0.014, top), V(0.006, 0.014, top + 0.012)], 0.0016, 'demir', n=4, r_son=0.0003)
        elif silah == 'pike_egik':
            boru(y, [sh, V(0.012, 0.006, 0.046)], 0.0026, kol, n=4)
            boru(y, [sh2, V(0.0, -0.004, 0.044)], 0.0026, kol, n=4)
            cubuk(y, V(-0.05, 0.004, 0.036), V(0.17, 0.004, 0.05), 0.0022, 'ahsap')
            boru(y, [V(0.17, 0.004, 0.05), V(0.183, 0.004, 0.051)], 0.0022, 'demir', n=4, r_son=0.0004)
        elif silah in ('arkebuz', 'tufek_omuz'):
            if silah == 'arkebuz':
                boru(y, [sh, V(0.016, 0.004, 0.053)], 0.0026, kol, n=4)
                boru(y, [sh2, V(0.026, -0.002, 0.052)], 0.0026, kol, n=4)
                cubuk(y, V(-0.002, 0.004, 0.056), V(0.06, 0.0, 0.054), 0.0032, 'ahsap_koyu')
                cubuk(y, V(0.03, 0.0, 0.0545), V(0.07, 0.0, 0.0535), 0.0018, 'demir')
                cubuk(y, V(0.05, 0.0, 0.0), V(0.05, 0.0, 0.052), 0.0015, 'ahsap')   # the forked rest
                if ates:
                    kure(y, (0.082, 0.0, 0.055), 0.008, 'beyaz', n=7, kat=4)
                    kure(y, (0.094, 0.004, 0.06), 0.0055, 'beyaz', n=6, kat=3)
            else:
                boru(y, [sh, V(0.004, 0.012, 0.064)], 0.0026, kol, n=4)
                boru(y, [sh2, V(0.004, -0.008, 0.038)], 0.0026, kol, n=4)
                cubuk(y, V(-0.004, 0.012, 0.03), V(0.014, 0.012, 0.11), 0.0028, 'ahsap_koyu')
        else:
            boru(y, [sh, V(0.004, 0.012, 0.036)], 0.0026, kol, n=4)
            boru(y, [sh2, V(0.004, -0.012, 0.036)], 0.0026, kol, n=4)


# ---------------------------------------------------------------- yard and port things
def varil(y, x, yy, z, r=0.012, h=0.03, key='ahsap', cember='demir'):
    pr = [(r * 0.82, 0.0), (r * 0.95, h * 0.2), (r, h * 0.5), (r * 0.95, h * 0.8), (r * 0.82, h)]
    donel(y, (x, yy), [(0.0, z)] + [(rr, z + zz) for rr, zz in pr] + [(0.0, z + h)], key, n=8)
    for zz in (0.18, 0.82):   # hoops (closed down onto the staves)
        donel(y, (x, yy), [(r * 0.92, z + h * zz - 0.002), (r * 0.975, z + h * zz - 0.001), (r * 0.975, z + h * zz + 0.001), (r * 0.92, z + h * zz + 0.002)], cember, n=8)


def sandik(y, x, yy, z, w=0.03, d=0.024, h=0.022, aci=0.0, key='ahsap_acik', bant='ahsap_koyu'):
    """a crate with dark battens"""
    ex = V(math.cos(aci), math.sin(aci)); ey = V(-ex.y, ex.x)
    kutu3(y, V(x, yy, z + h / 2), ex, ey, Z, w, d, h, key, ('+x', '-x', '+y', '-y', '+z'))
    for u in (-0.32, 0.32):
        kutu3(y, V(x, yy, z + h / 2) + ex * (u * w), ex, ey, Z, w * 0.12, d + 0.002, h + 0.002, bant, ('+x', '-x', '+y', '-y', '+z'))


def gulle_yigini(y, x, yy, z, n=3, r=0.007, key='demir'):
    for k in range(n):
        m = n - k
        for i in range(m):
            for j in range(m):
                u = (i - (m - 1) / 2) * 2 * r; v = (j - (m - 1) / 2) * 2 * r
                kure(y, (x + u, yy + v, z + r + k * r * 1.414), r, key, n=6, kat=3)


def top_namlu(y, o, yon, L=0.12, r=0.014, key='bronz', agiz=True):
    """a gun barrel along yon from its breech at o: tapered, reinforce rings, the cascabel, a dark muzzle"""
    o = Vector(o); yon = Vector(yon).normalized()
    b = o + yon * L
    boru(y, [o, o + yon * (L * 0.35), b], r, key, n=10, r_son=r * 0.72)
    for t, rr in ((0.04, 1.12), (0.35, 1.06), (0.97, 0.86)):
        p = o + yon * (L * t)
        boru(y, [p - yon * 0.004, p + yon * 0.004], r * rr * (1 - 0.28 * t), key, n=10)
    kure(y, o - yon * (r * 0.5), r * 0.5, key, n=6, kat=3)
    if agiz:
        u = Z.cross(yon)
        if u.length < 1e-4: u = X.copy()
        u.normalize(); w = yon.cross(u)
        y.yuz_yon([b + yon * 0.0045 + (u * math.cos(TAU * i / 8) + w * math.sin(TAU * i / 8)) * (r * 0.42) for i in range(8)], 'koyu', yon)


def top_kizak(y, x, yy, z, aci, L=0.12, r=0.013, key='bronz', govde='ahsap'):
    """a gun on a four-truck carriage, muzzle towards aci"""
    with parca(y, (x, yy, z), aci):
        for s in (-1, 1):
            for (u0, u1, h) in ((-0.04, 0.035, 0.016), (-0.04, 0.012, 0.026), (-0.04, -0.012, 0.034)):
                kutu3(y, V((u0 + u1) / 2, s * 0.013, h / 2 + 0.006), X, Y, Z, u1 - u0, 0.006, h, govde)
        kutu3(y, V(0.0, 0.0, 0.009), X, Y, Z, 0.07, 0.02, 0.006, govde, ('+x', '-x', '+y', '-y', '+z'))
        for u in (-0.03, 0.026):
            boru(y, [V(u, -0.022, 0.006), V(u, 0.022, 0.006)], 0.0025, 'demir', n=5)
            for s in (-1, 1):
                boru(y, [V(u, s * 0.017, 0.006), V(u, s * 0.021, 0.006)], 0.006, govde, n=8)
        top_namlu(y, V(-0.035, 0, 0.03), V(1, 0, 0.04), L, r, key)


def kereste(y, x, yy, z, L=0.14, n=4, kat=3, en=0.014, key='ahsap_acik', aci=0.0, uc='ahsap'):
    """a stack of squared timbers along aci: kat layers of n baulks on crossed sticks"""
    with parca(y, (x, yy, z), aci):
        for k in range(kat):
            zz = k * (en + 0.004)
            for i in range(n):
                v = (i - (n - 1) / 2) * en * 1.15
                kutu3(y, V(0, v, zz + 0.004 + en / 2), X, Y, Z, L, en, en, key, ('+y', '-y', '+z'))
                for s in (-1, 1):
                    y.yuz_yon([V(s * L / 2, v - en / 2, zz + 0.004), V(s * L / 2, v + en / 2, zz + 0.004), V(s * L / 2, v + en / 2, zz + 0.004 + en),
                               V(s * L / 2, v - en / 2, zz + 0.004 + en)], uc, V(s, 0, 0))
            for s in (-0.35, 0.35):
                kutu3(y, V(s * L, 0, zz + 0.002), X, Y, Z, 0.006, n * en * 1.15 + 0.004, 0.004, 'ahsap_koyu', ('+x', '-x', '+y', '-y', '+z'))


def tomruk(y, x, yy, z, L=0.18, n=3, r=0.01, aci=0.0, key='kutuk', uc='ahsap_acik'):
    """a pile of round logs (a bottom row of n, the next row nestled on it)"""
    with parca(y, (x, yy, z), aci):
        k = 0; m = n
        while m > 0:
            for i in range(m):
                v = (i - (m - 1) / 2) * 2 * r
                boru(y, [V(-L / 2, v, r + k * r * 1.73), V(L / 2, v, r + k * r * 1.73)], r, key, n=7, kapat=False)
                for sg in (-1, 1):
                    y.yuz_yon([V(sg * L / 2, v + r * math.cos(TAU * q / 7 + 0.0), r + k * r * 1.73 + r * math.sin(TAU * q / 7)) for q in range(7)], uc, V(sg, 0, 0))
            k += 1; m -= 1


def vinc(y, x, yy, z, aci=0.0, boy=0.3, kol=0.18, key='ahsap', yuk=None, ip_boy=None):
    """a timber derrick: a stepped base, a mast, a slanting jib towards aci with a brace, the rope and hook, an
    optional hanging load ('kereste' a baulk, 'sandik' a crate, 'top' a gun barrel)"""
    with parca(y, (x, yy, z), aci):
        kutu3(y, V(0, 0, 0.008), X, Y, Z, 0.05, 0.05, 0.016, 'tas_koyu')
        for sg in (-1, 1):
            cubuk(y, V(sg * 0.02, -0.02, 0.016), V(0, 0, boy * 0.55), 0.007, key)
            cubuk(y, V(sg * 0.02, 0.02, 0.016), V(0, 0, boy * 0.55), 0.007, key)
        cubuk(y, V(0, 0, 0.016), V(0, 0, boy), 0.012, key)
        tip = V(kol, 0, boy * 1.05)
        cubuk(y, V(0, 0, boy * 0.45), tip, 0.009, key)
        cubuk(y, V(0, 0, boy + 0.006), tip, 0.004, 'ahsap_koyu')
        # winch drum at the foot
        boru(y, [V(-0.024, -0.018, 0.05), V(-0.024, 0.018, 0.05)], 0.008, 'ahsap_koyu', n=8)
        ib = ip_boy or boy * 0.55
        cubuk(y, tip, tip - Z * ib, 0.0018, 'ahsap_koyu')
        boru(y, [tip - Z * ib, tip - Z * (ib + 0.006), tip - Z * (ib + 0.01) + X * 0.004], 0.0018, 'demir', n=4)
        p = tip - Z * (ib + 0.012)
        if yuk == 'kereste':
            for sg in (-1, 1):
                cubuk(y, p, p + V(sg * 0.03, 0, -0.016), 0.0014, 'ahsap_koyu')
            kutu3(y, p + V(0, 0, -0.024), X, Y, Z, 0.11, 0.014, 0.014, 'ahsap_acik')
        elif yuk == 'sandik':
            sandik(y, p.x, p.y, p.z - 0.026, 0.028, 0.024, 0.022)
        elif yuk == 'top':
            for sg in (-1, 1):
                cubuk(y, p, p + V(sg * 0.025, 0, -0.016), 0.0014, 'ahsap_koyu')
            top_namlu(y, p + V(-0.045, 0, -0.022), V(1, 0, 0), 0.1, 0.011, 'bronz')


def sandal(y, x, yy, z, aci=0.0, L=0.09, B=0.022, key='ahsap', ic='ahsap_acik', kurek=True):
    """a small rowing boat floating at z (waterline) along aci: a closed lofted hull (keel, chine, gunwale), its
    floor, the inner sides and the rim, thwarts and oars"""
    n = 8
    us = [-1 + 2 * i / n for i in range(n + 1)]
    hb = lambda u: B * max(0.08, 1 - abs(u) ** 2.2)
    g, k = 0.012, -0.006
    with parca(y, (x, yy, z), aci):
        S = lambda i, j, s: [V(us[i] * L / 2, 0, k), V(us[i] * L / 2, s * hb(us[i]) * 0.62, k * 0.2), V(us[i] * L / 2, s * hb(us[i]), g + 0.003 * abs(us[i]) ** 2)][j]
        for s in (-1, 1):
            for i in range(n):
                for j in range(2):
                    y.yuz_yon([S(i, j, s), S(i + 1, j, s), S(i + 1, j + 1, s), S(i, j + 1, s)], key if j else 'ahsap_koyu', V(0, s, 0))
        for i, sg in ((0, -1), (n, 1)):
            y.yuz_yon([S(i, 2, -1), S(i, 1, -1), S(i, 0, 1), S(i, 1, 1), S(i, 2, 1)], key, V(sg, 0, 0))
        # the rim (outer gunwale to the inner side), the inner sides down to the floor, the floor, end decks
        I = lambda i, s, zz, f=0.86: V(us[i] * L / 2, s * hb(us[i]) * f, zz)
        for i in range(1, n - 1):
            for s in (-1, 1):
                y.yuz_yon([S(i, 2, s), S(i + 1, 2, s), I(i + 1, s, S(i + 1, 2, s).z), I(i, s, S(i, 2, s).z)], 'ahsap_koyu', Z)
                y.yuz_yon([I(i, s, g * 0.3, 0.7), I(i + 1, s, g * 0.3, 0.7), I(i + 1, s, S(i + 1, 2, s).z), I(i, s, S(i, 2, s).z)], key, V(0, -s, 0.3))
            y.yuz_yon([I(i, -1, g * 0.3, 0.7), I(i + 1, -1, g * 0.3, 0.7), I(i + 1, 1, g * 0.3, 0.7), I(i, 1, g * 0.3, 0.7)], ic, Z)
        for i, i2 in ((0, 1), (n - 1, n)):   # end decks over the narrow ends
            zz = lambda q: S(q, 2, 1).z
            y.yuz_yon([S(i, 2, -1), S(i2, 2, -1), S(i2, 2, 1), S(i, 2, 1)], 'ahsap_koyu', Z)
        for i, sg in ((1, 1), (n - 1, -1)):   # the inner end walls under the end decks
            y.yuz_yon([I(i, -1, g * 0.3, 0.7), I(i, 1, g * 0.3, 0.7), I(i, 1, S(i, 2, 1).z), I(i, -1, S(i, 2, 1).z)], key, V(sg, 0, 0))
        for u in (-0.3, 0.25):
            kutu3(y, V(u * L / 2, 0, g * 0.75), X, Y, Z, 0.008, 2 * hb(u) * 0.86, 0.003, 'ahsap_koyu')
        if kurek:
            for s in (-1, 1):
                cubuk(y, V(0.0, s * B * 0.9, g), V(-0.012, s * B * 2.6, -0.002), 0.0022, 'ahsap_acik')


def dalga(y, x0, x1, y0, y1, zw, n=30, tohum=3, key='beyaz', boy=0.03, kacin=None):
    """small light ripple strokes a hair above a water surface; kacin(x, y) -> True skips a spot"""
    r = random.Random(tohum)
    k = 0
    while k < n:
        x, yy = r.uniform(x0, x1), r.uniform(y0, y1)
        if kacin and kacin(x, yy):
            k += 0.25; continue
        k += 1
        L = boy * r.uniform(0.6, 1.3)
        y.yuz_yon([V(x - L / 2, yy, zw + 0.0012), V(x + L / 2, yy, zw + 0.0012), V(x + L * 0.3, yy + 0.003, zw + 0.0012), V(x - L * 0.3, yy + 0.003, zw + 0.0012)], key, Z)


def ev(y, x0, x1, y0, y1, z0, h, duvar='siva', cati='kiremit', cati_h=None, pencere=True, kapi_yon='on', tohum=0, balkon=False):
    """a whitewashed town house: walls, small dark windows, a door, a hipped tile roof. Returns the ridge z"""
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, z0, z0 + h, duvar)
    r = random.Random(tohum)
    if pencere:
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            Lw = (b - a).length
            nw = max(1, int(Lw / 0.07))
            for q in range(nw):
                u = Lw * (q + 0.5) / nw - 0.006
                for zz in ([z0 + h * 0.58] if h < 0.13 else [z0 + h * 0.32, z0 + h * 0.68]):
                    if i == 0 and kapi_yon == 'on' and q == nw // 2 and zz < z0 + h * 0.5:
                        continue
                    pencere_k(y, a, b, u, zz, 0.012, 0.018, 'koyu' if r.random() < 0.75 else 'ahsap_koyu')
    if kapi_yon == 'on':
        a, b = k[0], k[1]
        Lw = (b - a).length
        nw = max(1, int(Lw / 0.07))
        pencere_k(y, a, b, Lw * (nw // 2 + 0.5) / nw - 0.009, z0, 0.018, min(0.04, h * 0.55), 'ahsap')
    return cati_kirma(y, x0, x1, y0, y1, z0 + h, cati_h or min(x1 - x0, y1 - y0) * 0.32, 0.012, cati, ns=4, nr=2, mahya_en=0.008)


def palmiye(y, x, yy, z=0.0, boy=0.16, key='boya_yesil', govde='ahsap', tohum=0):
    """a date palm: a curving ringed trunk, a crown of drooping fronds"""
    r = random.Random(tohum)
    lean = V(r.uniform(-1, 1), r.uniform(-1, 1)) * 0.015
    pts = [V(x, yy, z), V(x, yy, z) + lean * 0.4 + Z * boy * 0.5, V(x, yy, z) + lean + Z * boy * 0.92]
    boru(y, pts, 0.0055, govde, n=6, r_son=0.004)
    top = pts[-1]
    for i in range(8):
        a = TAU * i / 8 + r.uniform(-0.2, 0.2)
        d = V(math.cos(a), math.sin(a))
        boru(y, [top, top + d * 0.03 + Z * 0.012, top + d * 0.058 - Z * 0.008], 0.006, key, n=3, r_son=0.0012)


# ---------------------------------------------------------------- courtyard buildings
def halka_cati(y, dis, ic, z, h, sacak=0.03, key='kiremit', mahya='kiremit2', alt_key='ahsap_koyu', kalin=0.01, ns=6):
    """a hipped ring roof over a courtyard building: dis (outer wall line) and ic (courtyard wall line) are CCW
    rectangles at the wall top z; both eaves overhang by sacak, the ridge runs round the middle h higher; hips at the
    corners (ridge and hip caps). Returns the ridge z"""
    dis = [V(p.x, p.y) for p in dis]; ic = [V(p.x, p.y) for p in ic]
    Eo = disa(dis, sacak); Ei = disa(ic, -sacak)
    Rg = [(p + q) / 2 for p, q in zip(dis, ic)]
    zr = z + h
    zo = z - h * sacak / max(1e-6, (Rg[0] - dis[0]).length)   # (the slope continued down past the wall line)
    for i in range(4):
        j = (i + 1) % 4
        for k in range(ns):   # the outer slope, strips along the side
            t0, t1 = k / ns, (k + 1) / ns
            q = [Eo[i].lerp(Eo[j], t0), Eo[i].lerp(Eo[j], t1), Rg[i].lerp(Rg[j], t1), Rg[i].lerp(Rg[j], t0)]
            y.yuz_yon([q[0] + Z * zo, q[1] + Z * zo, q[2] + Z * zr, q[3] + Z * zr], key, Z)
            q = [Rg[i].lerp(Rg[j], t0), Rg[i].lerp(Rg[j], t1), Ei[i].lerp(Ei[j], t1), Ei[i].lerp(Ei[j], t0)]
            y.yuz_yon([q[0] + Z * zr, q[1] + Z * zr, q[2] + Z * zo, q[3] + Z * zo], key, Z)
        # fascias and soffits, outer and inner
        nn = V((dis[j] - dis[i]).y, -(dis[j] - dis[i]).x).normalized()
        y.yuz_yon([Eo[i] + Z * zo, Eo[j] + Z * zo, Eo[j] + Z * (zo - kalin), Eo[i] + Z * (zo - kalin)], alt_key, nn)
        y.yuz_yon([Eo[i] + Z * (zo - kalin), Eo[j] + Z * (zo - kalin), dis[j] + Z * z, dis[i] + Z * z], alt_key, -Z)
        y.yuz_yon([Ei[i] + Z * zo, Ei[j] + Z * zo, Ei[j] + Z * (zo - kalin), Ei[i] + Z * (zo - kalin)], alt_key, -nn)
        y.yuz_yon([Ei[i] + Z * (zo - kalin), Ei[j] + Z * (zo - kalin), ic[j] + Z * z, ic[i] + Z * z], alt_key, -Z)
        cubuk(y, Rg[i] + Z * (zr + 0.004), Rg[j] + Z * (zr + 0.004), 0.012, mahya)
        cubuk(y, Eo[i] + Z * (zo + 0.004), Rg[i] + Z * (zr + 0.004), 0.009, mahya)
        cubuk(y, Ei[i] + Z * (zo + 0.004), Rg[i] + Z * (zr + 0.004), 0.009, mahya)
    return zr


def cephe(y, a, b, z0, katlar, n, atla=(), renk=('siva_krem', 'tas_koyu', 'tas_acik', 'koyu'), cerceve=(0.006, 'kirec'), kafes_key='demir', atla_tum=()):
    """a wall a->b (facing its right) in n bays and storeys: katlar = [(H, u0, u1, v0, v1, kafesli), ...] from the
    bottom (u: share of the bay, v: height in the storey; None: a plain storey). Bays in atla are left out of the
    ground storey (a portal drawn by the caller goes there). Returns the top z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    z = z0
    for k, kat in enumerate(katlar):
        H = kat[0]
        for i in range(n):
            p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
            if (k == 0 and i in atla) or i in atla_tum: continue
            if kat[1] is None:
                duz_duvar(y, p, q, z, z + H, renk[0]); continue
            _, u0, u1, v0, v1, kaf = kat
            dikdortgen_acik(y, p, q, z, H, u0, u1, v0, v1, renk, derin=0.012, cerceve=cerceve, ic_kenar=True)
            if kaf:
                kafes(y, p, q, z, u0, u1, v0, v1, kafes_key, nu=4, nv=2, en=0.0028, ileri=0.004)
        z += H
    return z


def kose_taslari(y, p, z0, z1, key='kirec', adim=0.04, buyuk=0.03, kucuk=0.02, h=0.022):
    """alternating long and short quoin blocks up a corner at p"""
    for j in range(int((z1 - z0) / adim)):
        s = buyuk if j % 2 == 0 else kucuk
        kutu_merkez(y, (p.x, p.y), s, s, h, key, z0=z0 + j * adim + (adim - h) / 2)


def mizrak_sehpa(y, a, b, z, n=12, boy=0.22, key='ahsap', uc='demir'):
    """a rack of pikes leaning on a rail a->b (the pikes stand on the ground on its right side, their tips leaning on
    the rail's left)"""
    a, b, L, e, nc = eksen(a, b)
    for s in (0.05, 0.95):
        p = a.lerp(b, s)
        cubuk(y, p + Z * z, p + Z * (z + boy * 0.55), 0.008, 'ahsap_koyu')
    cubuk(y, a + Z * (z + boy * 0.55), b + Z * (z + boy * 0.55), 0.007, 'ahsap_koyu')
    for k in range(n):
        p = a.lerp(b, (k + 0.5) / n)
        f = p + nc * 0.03 + Z * z
        t = p - nc * 0.012 + Z * (z + boy)
        cubuk(y, f, t, 0.0028, key)
        d = (t - f).normalized()
        boru(y, [t, t + d * 0.014], 0.0026, uc, n=4, r_son=0.0004)


def hedef(y, x, yy, z, aci=0.0, r=0.03, h=0.06):
    """an archery / musketry butt: a straw disc on a trestle, a painted bull's-eye, facing aci"""
    d = V(math.cos(aci), math.sin(aci)); e = V(-d.y, d.x)
    c = V(x, yy, z + h)
    for s in (-1, 1):
        cubuk(y, V(x, yy) + e * (s * r * 0.6) - d * 0.012 + Z * z, c + e * (s * r * 0.3) - d * 0.004, 0.005, 'ahsap')
    P = lambda rr, t, dd: c + e * (rr * math.cos(t)) + Z * (rr * math.sin(t)) + d * dd
    n = 12
    for i in range(n):
        t0, t1 = TAU * i / n, TAU * (i + 1) / n
        y.yuz_yon([P(0, 0, 0.006), P(r, t0, 0.006), P(r, t1, 0.006)], 'saz', d)
        y.yuz_yon([P(0, 0, -0.006), P(r, t0, -0.006), P(r, t1, -0.006)], 'saz', -d)
        y.yuz_yon([P(r, t0, 0.006), P(r, t1, 0.006), P(r, t1, -0.006), P(r, t0, -0.006)], 'saz_koyu', (P(r, t0, 0) + P(r, t1, 0)) / 2 - c)
        y.yuz_yon([P(r * 0.55, t0, 0.0075), P(r * 0.7, t0, 0.0075), P(r * 0.7, t1, 0.0075), P(r * 0.55, t1, 0.0075)], 'beyaz', d)
        y.yuz_yon([P(0, 0, 0.0075), P(r * 0.25, t0, 0.0075), P(r * 0.25, t1, 0.0075)], 'boya_kirmizi', d)


def kuyu(y, x, yy, z, r=0.04, key='kirec'):
    """a well: a round stone curb, two posts and a little tiled roof with the windlass"""
    donel(y, (x, yy), [(r, z), (r, z + 0.035), (r * 0.8, z + 0.035), (r * 0.8, z + 0.03)], key, n=14)
    y.yuz_yon(cokgen((x, yy), r * 0.8, 14, z=z + 0.03), 'koyu', Z)
    for s in (-1, 1):
        cubuk(y, V(x + s * r * 0.9, yy, z + 0.03), V(x + s * r * 0.9, yy, z + 0.1), 0.008, 'ahsap')
    boru(y, [V(x - r * 0.9, yy, z + 0.075), V(x + r * 0.9, yy, z + 0.075)], 0.006, 'ahsap_koyu', n=6)
    cati_besik(y, x - r * 1.1, x + r * 1.1, yy - r * 0.55, yy + r * 0.55, z + 0.1, 0.03, 0.01, 'kiremit', ns=2, nr=2, mahya_en=0.006,
               ucluk_key='ahsap')


# ---------------------------------------------------------------- Herrerian (El Escorial)
def ucuz_cephe(y, a, b, z0, H, satir, n, key='granit_acik', pencere='koyu', w=0.3, h=0.45, atla=(), ince=False):
    """a plain wall a->b, z0..z0 + H, with satir rows of n small dark windows standing a hair proud (for the far and
    the courtyard sides, where recessed openings would cost too much); bays in atla stay blank. ince: each window
    only a flat dark quad 0.002 in front of the wall (for sides the game's camera never sees: a fifth of the cost)"""
    duz_duvar(y, a, b, z0, z0 + H, key)
    a2, b2, L, e, nc = eksen(a, b)
    hh = H / satir
    for r in range(satir):
        for i in range(n):
            if i in atla: continue
            bw = L / n
            u, v = bw * i + bw * (1 - w) / 2, z0 + hh * r + hh * (1 - h) * 0.55
            if ince:
                o = a2 + e * u + nc * 0.002
                y.yuz_yon([o + Z * v, o + e * (bw * w) + Z * v, o + e * (bw * w) + Z * (v + hh * h), o + Z * (v + hh * h)], pencere, nc)
            else:
                pencere_k(y, a2, b2, u, v, bw * w, hh * h, pencere, d=0.004, cik=0.0012)


def bilye(y, x, yy, z, s=1.0, key='granit_acik', top_key=None):
    """a Herrerian finial: a little stepped base, a pyramid pedestal and a stone ball"""
    kutu_merkez(y, (x, yy), 0.016 * s, 0.016 * s, 0.006 * s, key, z0=z)
    donel(y, (x, yy), [(0.0075 * s, z + 0.006 * s), (0.0035 * s, z + 0.02 * s), (0.0, z + 0.0201 * s)], key, n=4, kat=math.pi / 4)
    kure(y, (x, yy, z + 0.026 * s), 0.0075 * s, top_key or key, n=7, kat=3)


def igne(y, x, yy, z, boy=0.07, key='demir', top='altin'):
    """an iron spire needle with a gilt ball and a cross"""
    y.prizma((x, yy), 0.003, z, z + boy, key, n=4)
    kure(y, (x, yy, z + boy * 0.55), 0.007, top, n=8, kat=4)
    cubuk(y, V(x, yy, z + boy * 0.82), V(x + 0.012, yy, z + boy * 0.82), 0.003, key)
    cubuk(y, V(x, yy, z + boy * 0.82), V(x - 0.012, yy, z + boy * 0.82), 0.003, key)


def herrera_kule(y, cx, cy, w, z0, h, kat, cati_h, key='granit_acik', iz='granit', cati='arduvaz', girintili=True, igne_boy=0.08,
                 gizli_ince=False):
    """a square Herrerian tower: storeys of plain deep-set windows, string courses, a crowning cornice with stone
    balls at the corners and a steep slate spire (chapitel) with its iron needle. Returns the needle's top z.
    gizli_ince: the faces turned away from the game's camera (+x, +y) get flat window quads (ucuz_cephe ince)"""
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
    hh = h / kat
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        nc = V((b - a).y, -(b - a).x).normalized()
        if gizli_ince and (nc.x > 0.7 or nc.y > 0.7):
            ucuz_cephe(y, a, b, z0, h, kat, 1, key, w=0.28, h=0.5, ince=True)
        elif girintili:
            cephe(y, a, b, z0, [(hh, 0.36, 0.64, hh * 0.22, hh * 0.72, False)] * kat, 1, renk=(key, iz, 'tas_acik', 'koyu'), cerceve=None)
        else:
            ucuz_cephe(y, a, b, z0, h, kat, 1, key)
    silme(y, k, z0, 0.02, 0.008, iz, 'kaide')
    for j in range(1, kat):
        silme(y, k, z0 + hh * j - 0.003, 0.006, 0.004, iz, 'duz')
    zt = z0 + h
    silme(y, k, zt - 0.016, 0.018, 0.012, iz, 'tac')
    y.yuz_yon([V(p.x, p.y, zt + 0.002) for p in k], iz, Z)   # (inside the cornice's own top ring: not over it)
    for p in disa(k, 0.004):
        bilye(y, p.x, p.y, zt + 0.002, 1.1, key)
    tepe = cati_kirma(y, cx - w / 2 + 0.012, cx + w / 2 - 0.012, cy - w / 2 + 0.012, cy + w / 2 - 0.012, zt + 0.002, cati_h, 0.006, cati, mahya='kursun',
                      ns=4, nr=6)
    igne(y, cx, cy, tepe - 0.004, igne_boy)
    return tepe + igne_boy


def cati_penceresi(y, x, yy, z, nn, w=0.032, d=0.05, h=0.042, key='granit_acik', cati='arduvaz'):
    """a dormer on a slate roof: a little walled box facing nn (one of +-x, +-y) with a dark window, a gabled cap"""
    nn = V(nn[0], nn[1]).normalized(); e = V(-nn.y, nn.x)
    kutu3(y, V(x, yy, z + h / 2), e, -nn, Z, w, d, h, key, ('+x', '-x', '-y'))
    f = V(x, yy) + nn * (d / 2)
    pencere_k(y, f - e * (w / 2), f + e * (w / 2), w * 0.3, z + h * 0.35, w * 0.4, h * 0.45, 'koyu', d=0.004, cik=0.0012)
    xs = sorted([(V(x, yy) + e * (w / 2 + 0.003)).x, (V(x, yy) - e * (w / 2 + 0.003)).x, (V(x, yy) + nn * (d / 2)).x, (V(x, yy) - nn * (d / 2)).x])
    ys = sorted([(V(x, yy) + e * (w / 2 + 0.003)).y, (V(x, yy) - e * (w / 2 + 0.003)).y, (V(x, yy) + nn * (d / 2)).y, (V(x, yy) - nn * (d / 2)).y])
    cati_besik(y, xs[0] + 0.003, xs[-1] - 0.003, ys[0] + 0.003, ys[-1] - 0.003, z + h, w * 0.5, 0.005, cati, mahya='kursun', ns=2, nr=2,
               mahya_en=0.005, ucluk_key=key, kalinlik=0.004)


def sade_sutun(y, x, yy, z0, z1, r, key='granit_acik', n=8):
    """a cheap plain column for long rows: a square plinth, a many-sided shaft, a torus-like ring and a square abacus"""
    h = z1 - z0
    kutu_merkez(y, (x, yy), r * 2.8, r * 2.8, h * 0.05, key, z0=z0)
    y.prizma((x, yy), r, z0 + h * 0.05, z1 - h * 0.08, key, n=n, ust=False, kat=math.pi / n)
    donel(y, (x, yy), [(r * 0.98, z1 - h * 0.08), (r * 1.3, z1 - h * 0.05)], key, n=n, kat=math.pi / n)
    kutu_merkez(y, (x, yy), r * 2.8, r * 2.8, h * 0.05, key, z0=z1 - h * 0.05)


def kapali_alinlik(y, a, b, z, h, derin, key='granit_acik', ic_key=None, c=0.008, cati_key=None):
    """a closed triangular pediment over the front a->b (facing its right) at z, h high, derin deep: a solid prism
    (front, back, the two raking tops, the bottom), raking and level cornices standing proud, an inset darker
    tympanum. Returns the apex z"""
    a, b, W, e, nc = eksen(a, b)
    D = -nc * derin
    A, B, T = a + Z * z, b + Z * z, (a + b) / 2 + Z * (z + h)
    m = (A + B + T) / 3 + D / 2
    y.yuz_yon([A, B, T], key, nc)
    y.yuz_yon([A + D, B + D, T + D], key, -nc)
    for p, q in ((A, T), (T, B)):
        yuz_dis(y, [p, q, q + D, p + D], cati_key or key, m)
    y.yuz_yon([A, B, B + D, A + D], key, -Z)
    if ic_key:
        k = 0.22
        Ai, Bi, Ti = A.lerp(m - D / 2, k) + nc * 0.0015, B.lerp(m - D / 2, k) + nc * 0.0015, T.lerp(m - D / 2, k) + nc * 0.0015
        y.yuz_yon([Ai, Bi, Ti], ic_key, nc)
    u = Z * (c * 0.4) + nc * (c * 0.5)
    for p, q in ((A - e * c, T), (T, B + e * c)):
        cubuk(y, p + u, q + u, c * 1.4, key, c * 1.1)
    cubuk(y, A - e * c + nc * (c * 0.5) + Z * (c * 0.2), B + e * c + nc * (c * 0.5) + Z * (c * 0.2), c * 1.2, key, c * 1.1)
    return T.z


def capa(y, x, yy, z, aci=0.0, s=1.0, key='demir'):
    """an iron anchor lying flat: the shank, the wooden stock across its head, curved arms with flukes, the ring"""
    with parca(y, (x, yy, z), aci, s):
        r = 0.004
        cubuk(y, V(-0.05, 0, r), V(0.05, 0, r), 0.007, key, 0.006)
        cubuk(y, V(-0.042, -0.04, r * 1.6), V(-0.042, 0.04, r * 1.6), 0.008, 'ahsap', 0.008)
        for sg in (-1, 1):
            pts = [V(0.05, 0, r), V(0.058, sg * 0.016, r), V(0.052, sg * 0.032, r), V(0.04, sg * 0.04, r)]
            boru(y, pts, 0.0035, key, n=5)
            levha(y, [V(0.045, sg * 0.03, r + 0.0025), V(0.032, sg * 0.046, r + 0.0025), V(0.038, sg * 0.033, r + 0.0025)], key, Z, kil=0.002)
        boru(y, [V(-0.05 - 0.008 * (1 - math.cos(TAU * k / 8)), 0.008 * math.sin(TAU * k / 8), r) for k in range(9)], 0.002, key, n=4)


def halat(y, x, yy, z, R=0.022, r=0.006, kat=2, key='saz_koyu'):
    """a coil of rope: kat stacked tori and the coil's top"""
    for k in range(kat):
        zz = z + k * r * 1.7
        RR = R * (1 - 0.12 * k)
        pr = [(RR + r * math.cos(t), zz + r + r * math.sin(t)) for t in [-math.pi / 2 + TAU * i / 8 for i in range(9)]]
        donel(y, (x, yy), pr, key, n=12)
    y.yuz_yon(cokgen((x, yy), R * (1 - 0.12 * (kat - 1)) - r * 0.6, 12, z=z + (kat - 1) * r * 1.7 + r * 1.2), 'saz', Z)


def direk_yigini(y, x, yy, z, L=0.4, n=5, r=0.009, aci=0.0, key='ahsap_acik'):
    """spars and masts laid on trestles: a row of long tapering poles"""
    with parca(y, (x, yy, z), aci):
        for s in (-0.32, 0.32):
            kutu3(y, V(s * L, 0, 0.008), X, Y, Z, 0.012, n * r * 2.6 + 0.01, 0.016, 'ahsap_koyu', ('+x', '-x', '+y', '-y', '+z'))
        for i in range(n):
            v = (i - (n - 1) / 2) * r * 2.5
            boru(y, [V(-L / 2, v, 0.016 + r), V(L / 2, v, 0.016 + r)], r, key, n=7, r_son=r * 0.65)
