# Shared helpers for the Russian landmarks (lm_kurkpazari, lm_ahsapkremlin, lm_novgorod, lm_kremlin): the Orthodox
# cross, helmet and onion domes (plain, striped, scaled aspen shingles), a windowed drum with its cornice, a stone
# church body with zakomara gables over a curved roof, apses, swallowtail (Moscow) merlons, log houses with carved
# window frames (nalichniki) and barge boards, snow on roofs and ground, spruces and birches.
import math, random
from mathutils import Vector
from parcalar import *
from frank_ortak import kutu3, levha, zemin_blok, cayir_renk, insan, at, _ss
import doku


# ---------------------------------------------------------------- crosses, domes, drums
def ortodoks_hac(y, cx, cy, z, h=0.08, key='altin', aci=0.0, top=True):
    """a gilded Orthodox cross (three bars, the lowest slanted) on a knob, its bars across the angle aci (0: facing
    -y). Returns the top z"""
    with parca(y, (cx, cy, z), aci):
        if top:
            kure(y, (0, 0, h * 0.06), h * 0.075, key, n=8, kat=3)
        kutu_merkez(y, (0, 0), h * 0.065, h * 0.065, h * 0.98, key, z0=h * 0.02)
        kutu_merkez(y, (0, 0), h * 0.28, h * 0.05, h * 0.05, key, z0=h * 0.80)
        kutu_merkez(y, (0, 0), h * 0.52, h * 0.055, h * 0.062, key, z0=h * 0.6)
        cubuk(y, V(-h * 0.2, 0, h * 0.24), V(h * 0.2, 0, h * 0.37), h * 0.055, key)
    return z + h


def kubbe_profil(tur, r, z, h):
    """the outline [(radius, z)] of a dome: 'sogan' onion, 'shlem' helmet (Novgorod / Vladimir), 'yarim' a raised
    hemisphere"""
    if tur == 'shlem':
        f = [(1.0, 0), (1.035, 0.1), (1.045, 0.22), (1.0, 0.38), (0.88, 0.54), (0.69, 0.69), (0.46, 0.81), (0.25, 0.9),
             (0.1, 0.96), (0.0, 1.0)]
    elif tur == 'yarim':
        f = [(math.cos(math.pi / 2 * k / 8), math.sin(math.pi / 2 * k / 8)) for k in range(9)]
    else:
        f = [(0.56, 0), (0.86, 0.04), (1.06, 0.14), (1.13, 0.26), (1.1, 0.37), (0.96, 0.49), (0.72, 0.61), (0.47, 0.72),
             (0.26, 0.82), (0.12, 0.9), (0.04, 0.96), (0.0, 1.0)]
    return [(r * a, z + h * b) for a, b in f]


def _ince(pr, alt):
    """the profile with alt points per segment (smooth Catmull-Rom between the given points)"""
    out = []
    P = [Vector((a, b)) for a, b in pr]
    m = len(P)
    for i in range(m - 1):
        p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, m - 1)]
        for k in range(alt):
            t = k / alt
            q = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
            out.append((max(0.0, q.x), q.y))
    out.append(pr[-1])
    return out


def kubbe(y, c, r, z, tur='sogan', h=None, key='altin', n=24, dilim=None, pul=None, alt=2):
    """a dome of type tur on (c, z): dilim = keys for meridian stripes (painted onions), pul = two keys in a checker
    (scaled aspen shingles, lemekh); alt: smoothing points per profile segment. Returns the tip z"""
    h = h or r * (1.75 if tur == 'sogan' else 1.0 if tur == 'shlem' else 0.9)
    pr = _ince(kubbe_profil(tur, r, z, h), alt)
    if pul:
        rings = [[V(c[0] + rr * math.cos(TAU * (i + 0.5 * (k % 2)) / n), c[1] + rr * math.sin(TAU * (i + 0.5 * (k % 2)) / n), zz)
                  for i in range(n)] for k, (rr, zz) in enumerate(pr)]
        for k in range(len(pr) - 1):
            A, B = rings[k], rings[k + 1]
            sh = k % 2   # (every other ring turned half a step: the shingles overlap like scales)
            for i in range(n):
                j = (i + 1) % n
                kk = pul[(i + k) % len(pul)]
                if pr[k + 1][0] < 1e-9:
                    y.yuz([A[i], A[j], B[i]], kk)
                else:
                    # ring k+1 is shifted by half a step against ring k
                    if sh == 0:
                        y.yuz([A[i], A[j], B[i]], kk); y.yuz([A[j], B[j], B[i]], pul[(i + k + 1) % len(pul)])
                    else:
                        y.yuz([A[i], A[j], B[j]], kk); y.yuz([A[i], B[j], B[i]], pul[(i + k + 1) % len(pul)])
    else:
        donel(y, c, pr, key, n=n, dilim=dilim)
    return z + h


def boyun(y, c, r, z, h, key='kursun', n=24):
    """the short neck (sheia) between a drum's cornice and an onion: a waisted ring"""
    donel(y, c, [(r * 1.0, z), (r * 0.86, z + h * 0.45), (r * 0.9, z + h * 0.8), (r * 1.02, z + h)], key, n=n)
    y.yuz_yon([V(p.x, p.y, z + h) for p in cokgen(c, r * 1.02, n)], key, Z)
    return z + h


def baraban(y, c, r, z0, h, key='siva', n=12, pencere=6, cam='koyu', kornis_key=None, arkatur=True, kat=0.0, sivri=0.0,
            pen_en=0.36, yan_key=None, cerceve=True):
    """a church drum: an n-sided wall with pencere narrow arched windows evenly round it, a plinth, a cornice and
    (arkatur) a band of small blind arches under it. Returns the top z (the cornice's top)"""
    k = cokgen(c, r, n, kat)
    adim = n // pencere if pencere else 0
    yk = yan_key or key
    for i in range(n):
        a, b = k[i], k[(i + 1) % n]
        if adim and i % adim == 0:
            y.kemerli(a, b, z0, h, (key, yk, kornis_key or key, cam), v0=h * 0.22, en=pen_en, ust=h * 0.2, derin=0.012, k_say=6,
                      sivri=sivri, cerceve=(0.0045, kornis_key or key) if cerceve else None)
        else:
            duz_duvar(y, a, b, z0, z0 + h, key)
    silme(y, k, z0, 0.014, 0.006, kornis_key or key, 'kaide')
    zt = z0 + h
    if arkatur:
        # a band of little hanging arches (the arcature frieze) under the cornice
        for i in range(n):
            a, b = k[i], k[(i + 1) % n]
            e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
            for j in range(2):
                u0, u1 = L * (0.08 + 0.46 * j), L * (0.46 + 0.46 * j)
                um, R = (u0 + u1) / 2, (u1 - u0) / 2
                zb = zt - h * 0.13
                pts = [a + e * u0 + Z * zb] + [a + e * (um - R * math.cos(math.pi * t / 6)) + Z * (zb - R * 0.9 * math.sin(math.pi * t / 6)) for t in range(1, 6)] + \
                      [a + e * u1 + Z * zb]
                for t in range(len(pts) - 1):
                    p, q = pts[t], pts[t + 1]
                    y.yuz_yon([p + nn * 0.004, q + nn * 0.004, q + nn * 0.004 + Z * 0.006, p + nn * 0.004 + Z * 0.006], kornis_key or key, nn)
                    y.yuz_yon([p + nn * 0.004, q + nn * 0.004, q, p], kornis_key or key, -Z)
        silme(y, k, zt - h * 0.13, h * 0.03, 0.005, kornis_key or key, 'duz')
    silme(y, k, zt - 0.012, 0.012, 0.012, kornis_key or key, 'kaba')
    y.yuz_yon([V(p.x, p.y, zt) for p in disa(k, 0.006)], kornis_key or key, Z)
    return zt


def kubbe_kule(y, c, r, z0, h_drum, tur='sogan', dome_key='altin', key='siva', n=12, pencere=6, dome_r=None, dome_h=None,
               hac_h=None, hac_key='altin', kornis_key=None, dilim=None, pul=None, n_dome=None, boyun_key=None, sivri=0.0,
               boyun_h=None, arkatur=None, alt=None):
    """drum + neck + dome + cross (a small one cheaper: no arcature, fewer sides). Returns the cross's top z"""
    buyuk = r >= 0.08
    n_dome = n_dome or (28 if buyuk else 16)
    alt = alt or (2 if buyuk else 1)
    zt = baraban(y, c, r, z0, h_drum, key, n, pencere, kornis_key=kornis_key, sivri=sivri, arkatur=buyuk if arkatur is None else arkatur,
                 cerceve=r >= 0.07)
    dr = dome_r or r * (1.0 if tur == 'shlem' else 0.86)
    if tur == 'sogan':
        zt = boyun(y, c, dr * 0.62, zt, boyun_h if boyun_h is not None else r * 0.22, boyun_key or dome_key, n=n_dome)
        zd = kubbe(y, c, dr, zt - 0.001, 'sogan', dome_h, dome_key, n=n_dome, dilim=dilim, pul=pul, alt=alt)
    else:
        y.yuz_yon([V(p.x, p.y, zt) for p in cokgen(c, r * 1.0, n)], kornis_key or key, Z)
        zd = kubbe(y, c, dr, zt, tur, dome_h, dome_key, n=n_dome, dilim=dilim, pul=pul, alt=alt)
    return ortodoks_hac(y, c[0], c[1], zd - 0.004, hac_h or dr * 1.0, hac_key)


# ---------------------------------------------------------------- the stone church: zakomaras and a vaulted roof
def _kemer_h(bolum, zs, x, stilt=1.0):
    """the height over x of a row of round arches springing at zs on the bay boundaries bolum"""
    for a, b in zip(bolum, bolum[1:]):
        if a - 1e-9 <= x <= b + 1e-9:
            R = (b - a) / 2; m = (a + b) / 2
            return zs + stilt * math.sqrt(max(0.0, R * R - (x - m) ** 2))
    return zs


def _orneklem(bolum, m):
    out = []
    for a, b in zip(bolum, bolum[1:]):
        for k in range(m):
            t = k / m
            out.append(a + (b - a) * (0.5 - 0.5 * math.cos(math.pi * t)))
    out.append(bolum[-1])
    return out


def zakomara_govde(y, xb, yb, z0, zs, duvar='siva', cati='kursun', stilt=1.0, m=8, sacak=0.012, kalin=0.008,
                   pencere=None, lesene=True, kemer_bant=True, kaide=True, yuzler=('on', 'sag', 'arka', 'sol'), arka_duvar=True,
                   cam='koyu', pen_key=None):
    """a cross-in-square church body: bay boundaries xb (along x) and yb (along y), walls from z0 with round
    zakomara gables springing at zs (stilt: their rise / half span), the roof following them (the curved vaults
    meet in groins: max of the two arch rows). pencere(side, i, a, b) -> None or a list of window specs
    (u_centre, v_bottom, w, h) along a bay (u from a), drawn as arched openings. lesene: flat pilasters on the bay
    lines; kemer_bant: a raised band round each zakomara. Returns a function h(x, y) giving the roof height"""
    x0, x1, y0, y1 = xb[0], xb[-1], yb[0], yb[-1]
    hx = lambda x: _kemer_h(xb, zs, min(max(x, x0), x1), stilt)
    hy = lambda yy: _kemer_h(yb, zs, min(max(yy, y0), y1), stilt)
    H = lambda x, yy: max(hx(x), hy(yy))
    pk = pen_key or 'tas_acik'
    # walls: each side a list of bays; below zs the wall with its windows, above it the gable's strips
    kenarlar = {'on': (V(x0, y0), V(x1, y0), xb, lambda u: H(u, y0), False),
                'sag': (V(x1, y0), V(x1, y1), yb, lambda u: H(x1, u), False),
                'arka': (V(x1, y1), V(x0, y1), xb, lambda u: H(u, y1), True),
                'sol': (V(x0, y1), V(x0, y0), yb, lambda u: H(x0, u), True)}
    for ad in ('on', 'sag', 'arka', 'sol'):
        a, b, bol, hf, ters = kenarlar[ad]
        if ad not in yuzler and not arka_duvar: continue
        e = (b - a).normalized(); nc = V(e.y, -e.x)
        bs = list(bol)
        # positions along the side (u from a)
        if ters: us = [(bs[-1] - q) for q in reversed(bs)]
        else: us = [q - bs[0] for q in bs]
        coord = (lambda u: bs[-1] - u) if ters else (lambda u: bs[0] + u)
        for i in range(len(us) - 1):
            ua, ub = us[i], us[i + 1]
            pa, pb = a + e * ua, a + e * ub
            spec = pencere(ad, i, ua, ub) if (pencere and ad in yuzler) else None
            if not spec:
                duz_duvar(y, pa, pb, z0, zs, duvar)
            else:
                spec = [(b0, b1, [(q[0] - ua,) + tuple(q[1:]) for q in ac]) for (b0, b1, ac) in spec]   # (u along the bay)
                bantli_duvar(y, pa, pb, z0, zs, spec, duvar, cam, pk)
            # the gable above zs
            ss = _orneklem([ua, ub], m)
            for k in range(len(ss) - 1):
                p, q = a + e * ss[k], a + e * ss[k + 1]
                hp, hq = hf(coord(ss[k])), hf(coord(ss[k + 1]))
                y.yuz_yon([p + Z * zs, q + Z * zs, q + Z * hq, p + Z * hp], duvar, nc)
            if ad in yuzler and kemer_bant:
                # a raised band (archivolt) following the gable, set a little below its edge
                bw, bd = 0.011, 0.005
                R = (ub - ua) / 2; um = (ua + ub) / 2
                ring = [(um + R * math.cos(math.pi * t / 12), R * math.sin(math.pi * t / 12)) for t in range(13)]
                for k in range(12):
                    (u1, v1), (u2, v2) = ring[k], ring[k + 1]
                    def P(u, v, s, d):
                        rr = math.hypot(u - um, v)
                        f = (rr - s) / rr if rr > 1e-9 else 0
                        return a + e * (um + (u - um) * f) + Z * (zs + v * f * stilt) + nc * d
                    q = [P(u1, v1, 0.006, bd), P(u2, v2, 0.006, bd), P(u2, v2, 0.006 + bw, bd), P(u1, v1, 0.006 + bw, bd)]
                    y.yuz_yon(q, pk, nc)
                    y.yuz_yon([P(u1, v1, 0.006, bd), P(u2, v2, 0.006, bd), P(u2, v2, 0.006, 0), P(u1, v1, 0.006, 0)], pk,
                              (P(u1, v1, 0, 0) + P(u2, v2, 0, 0)) / 2 - (a + e * um + Z * zs))
                    y.yuz_yon([P(u1, v1, 0.006 + bw, bd), P(u2, v2, 0.006 + bw, bd), P(u2, v2, 0.006 + bw, 0), P(u1, v1, 0.006 + bw, 0)], pk,
                              (a + e * um + Z * zs) - (P(u1, v1, 0, 0) + P(u2, v2, 0, 0)) / 2)
        if ad in yuzler and lesene:
            for i, u in enumerate(us):
                w = 0.034 if 0 < i < len(us) - 1 else 0.03
                uu = min(max(u - w / 2, 0.0), us[-1] - w)
                kutu(y, a + e * uu + nc * 0.011 + Z * z0, e, w, 0.011, zs - z0 - 0.004, duvar, 'onsagsolust')
        if ad in yuzler and kaide:
            silme(y, [a, b], z0, 0.03, 0.012, duvar, 'kaide', kapali=False)
    # the roof: a height field over the plan, overhanging the walls by sacak
    gx = [x0 - sacak] + _orneklem(xb, m) + [x1 + sacak]
    gy = [y0 - sacak] + _orneklem(yb, m) + [y1 + sacak]
    top = [[V(x, yy, H(x, yy)) for yy in gy] for x in gx]
    # lead sheets: every other strip down the vault in the darker key (seams along the vault's axis), so the curved
    # roof reads as sheet metal and not as a soft cushion
    cati2 = cati + '2' if (cati + '2') in doku.MALZEME else cati
    for i in range(len(gx) - 1):
        for j in range(len(gy) - 1):
            a, b, c, d = top[i][j], top[i + 1][j], top[i + 1][j + 1], top[i][j + 1]
            xm, ym = (gx[i] + gx[i + 1]) / 2, (gy[j] + gy[j + 1]) / 2
            kk = cati if ((i if hx(xm) >= hy(ym) else j) % 2 == 0) else cati2
            # split along the diagonal whose midpoint lies nearest the true surface (follows the groins and the valleys
            # between the vaults: a fixed diagonal left them as wavy, draped creases)
            hc = H(xm, ym)
            if abs((a.z + c.z) / 2 - hc) <= abs((b.z + d.z) / 2 - hc):
                y.yuz_yon([a, b, c], kk, Z); y.yuz_yon([a, c, d], kk, Z)
            else:
                y.yuz_yon([a, b, d], kk, Z); y.yuz_yon([b, c, d], kk, Z)
    # the roof's edge (fascia) and its underside back to the wall
    ring = [top[i][0] for i in range(len(gx))] + [top[-1][j] for j in range(1, len(gy))] + \
           [top[i][-1] for i in range(len(gx) - 2, -1, -1)] + [top[0][j] for j in range(len(gy) - 2, 0, -1)]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for k in range(len(ring)):
        p, q = ring[k], ring[(k + 1) % len(ring)]
        out = V(1 if p.x > cx else -1, 0) if abs(p.x - q.x) < 1e-9 else V(0, 1 if p.y > cy else -1)
        y.yuz_yon([p, q, q - Z * kalin, p - Z * kalin], cati, out)
        w = lambda s: V(min(max(s.x, x0), x1), min(max(s.y, y0), y1), s.z - kalin)
        y.yuz_yon([p - Z * kalin, q - Z * kalin, w(q), w(p)], cati, -Z)
    return H


def bantli_duvar(y, a, b, z0, z1, bantlar, duvar='siva', cam='koyu', pk='tas_acik'):
    """a wall a->b from z0 to z1 cut in horizontal bands: bantlar = [(v0, v1, [opening, ...]), ...] (v above z0); an
    opening = (u_centre, v_bottom, w, h[, back key[, frame]]) with u along a->b and v_bottom above the band's v0; the
    rest plain wall"""
    v = 0.0
    for (b0, b1, ac) in sorted(bantlar, key=lambda q: q[0]):
        if b0 > v + 1e-6: duz_duvar(y, a, b, z0 + v, z0 + b0, duvar)
        _pencereli_bant(y, a, b, z0 + b0, b1 - b0, ac, duvar, cam, pk)
        v = b1
    if z0 + v < z1 - 1e-6: duz_duvar(y, a, b, z0 + v, z1, duvar)


def _pencereli_bant(y, a, b, z0, Hb, spec, duvar, cam, pk):
    """the wall a->b from z0 (Hb high) with round-arched openings (see bantli_duvar), cut in vertical strips"""
    a, b = V(a.x, a.y), V(b.x, b.y)
    W = (b - a).length; e = (b - a) / W
    u = 0.0
    for sp in sorted(spec):
        uc, v0, w, h = sp[:4]
        arka = sp[4] if len(sp) > 4 and sp[4] else cam
        cer = sp[5] if len(sp) > 5 else None
        if uc - w / 2 > u + 1e-6:
            duz_duvar(y, a + e * u, a + e * (uc - w / 2), z0, z0 + Hb, duvar)
        p, q = a + e * (uc - w / 2), a + e * (uc + w / 2)
        y.kemerli(p, q, z0, Hb, (duvar, duvar, pk, arka), v0=v0, en=0.999, ust=max(Hb - v0 - h, 0.002), derin=0.018, k_say=6,
                  cerceve=cer)
        u = uc + w / 2
    if W - u > 1e-6:
        duz_duvar(y, a + e * u, b, z0, z0 + Hb, duvar)


def apsis(y, c, r, z0, h, aci=math.pi / 2, duvar='siva', cati='kursun', n=10, pencere=True, cam='koyu', pen_key='tas_acik'):
    """a semicircular apse bulging towards angle aci from the wall it leans on (its centre c on the wall line): walls,
    a window in the middle, a cornice and a half-dome roof"""
    t0 = aci - math.pi / 2
    pts = [V(c[0] + r * math.cos(t0 + math.pi * i / n), c[1] + r * math.sin(t0 + math.pi * i / n)) for i in range(n + 1)]
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        if pencere and i in (n // 2 - 2, n // 2 + 1) or (pencere and n % 2 and i == n // 2):
            y.kemerli(a, b, z0, h, (duvar, duvar, pen_key, cam), v0=h * 0.4, en=0.32, ust=h * 0.14, derin=0.015, k_say=6,
                      cerceve=(0.004, pen_key))
        else:
            duz_duvar(y, a, b, z0, z0 + h, duvar)
    silme(y, pts, z0, 0.03, 0.012, duvar, 'kaide', kapali=False)
    silme(y, pts, z0 + h - 0.012, 0.012, 0.008, pen_key, 'kaba', kapali=False)
    return y.kubbe(c, r + 0.01, z0 + h, r * 0.75, cati, n=2 * n, kat=6, t0=t0, t1=t0 + math.pi, kapak=duvar)


# ---------------------------------------------------------------- Moscow walls: swallowtail merlons
def kirlangic(y, a, b, z, h, kalinlik=0.024, key='tugla', w=None, g=None, centik=None, yarik_key='koyu'):
    """swallowtail (Ghibelline) merlons along a->b, their outer face on the line facing the right: each an M-shaped
    block (a V notch in its top) with an arrow slit"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-6: return
    e = (b - a) / L; nc = V(e.y, -e.x); ni = -nc
    w = w or h * 0.62; g = g or h * 0.42; ct = centik or h * 0.28
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g
    for i in range(k):
        u0 = i * (w + g); u1 = u0 + w; um = (u0 + u1) / 2
        P = lambda u, v, d: a + e * u + ni * d + Z * (z + v)
        for d, yon in ((0, nc), (kalinlik, ni)):
            y.yuz_yon([P(u0, 0, d), P(um, 0, d), P(um, h - ct, d), P(u0, h, d)], key, yon)
            y.yuz_yon([P(um, 0, d), P(u1, 0, d), P(u1, h, d), P(um, h - ct, d)], key, yon)
        y.yuz_yon([P(u0, 0, 0), P(u0, h, 0), P(u0, h, kalinlik), P(u0, 0, kalinlik)], key, -e)
        y.yuz_yon([P(u1, 0, 0), P(u1, h, 0), P(u1, h, kalinlik), P(u1, 0, kalinlik)], key, e)
        y.yuz_yon([P(u0, h, 0), P(um, h - ct, 0), P(um, h - ct, kalinlik), P(u0, h, kalinlik)], key, Z + e * 0.5)
        y.yuz_yon([P(um, h - ct, 0), P(u1, h, 0), P(u1, h, kalinlik), P(um, h - ct, kalinlik)], key, Z - e * 0.5)
        if yarik_key and w > 0.02:
            yarik(y, P(0, 0, 0), e, nc, um - 0.003, h * 0.22, 0.006, h * 0.3, yarik_key)


# ---------------------------------------------------------------- timber: log houses, carved frames
def kutuk_duvar2(y, a, b, z0, z1, r=0.014, key='kutuk', uzanti=0.02, ic=False, cekirdek=None, n=6):
    """a wall of horizontal hewn logs a->b (outer side to the right), ends sticking out uzanti past a and b: six-sided
    logs whose flats meet above and below (parcalar.kutuk_duvar's octagons left a V gap between them that showed what
    lay behind, and cost more); the hidden flats between logs are left out. ic: a plain inner face; cekirdek: a plane
    on the logs' axis facing out"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    m = max(1, int(round((z1 - z0) / (2 * r))))
    rr = (z1 - z0) / m / 2
    R = rr / math.cos(math.pi / n)
    yon = lambda t: nc * math.cos(t) + Z * math.sin(t)
    for k in range(m):
        zc = z0 + rr * (2 * k + 1)
        p = a - e * uzanti + Z * zc - nc * rr * 0.2
        q = b + e * uzanti + Z * zc - nc * rr * 0.2
        A = [p + yon(TAU * i / n) * R for i in range(n)]
        B = [q + yon(TAU * i / n) * R for i in range(n)]
        for i in range(n):
            tm = TAU * (i + 0.5) / n
            ust, alt = math.sin(tm) > 0.99, math.sin(tm) < -0.99
            if (ust and k < m - 1) or (alt and k > 0): continue
            j = (i + 1) % n
            y.yuz_yon([A[i], B[i], B[j], A[j]], key, yon(tm))
        y.yuz_yon(A, key, -e); y.yuz_yon(B, key, e)
    if ic:
        duz_duvar(y, b - nc * rr * 1.25, a - nc * rr * 1.25, z0, z1, key)
    if cekirdek:
        duz_duvar(y, a - nc * (rr * 0.25), b - nc * (rr * 0.25), z0, z1, cekirdek)


def kutuk_kutu(y, x0, x1, y0, y1, z0, h, r=0.013, key='kutuk', uzanti=None, ic=False):
    """four log walls round a rectangle with crossed, projecting ends (the pairs half a log apart). Returns the
    wall top z"""
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        off = r if i % 2 else 0
        kutuk_duvar2(y, k[i], k[(i + 1) % 4], z0 + off, z0 + h + off, r, key, uzanti=uzanti if uzanti is not None else r * 2.4, ic=ic)
    return z0 + h + r


def nalichnik(y, o, e, w, h, cer='beyaz', cam='koyu', panjur='turkuaz', tepe='ucgen', t=0.007, ileri=0.0, sus='beyaz'):
    """a carved window frame (nalichnik) on a wall: o the bottom centre of the opening on the wall face, e along the
    wall (the frame faces the right of e); a dark pane, jambs, a sill with a carved apron, a lintel and a crest
    (tepe 'ucgen' pediment, 'kemer' round kokoshnik, None), shutters (panjur key or None)"""
    o = Vector(o); e = Vector(e); e.z = 0; e.normalize(); n = V(e.y, -e.x)
    f = max(0.007, w * 0.16)
    gom = 0.012   # (sunk into the logs behind)
    o = o + n * ileri
    def K(c, sx, sd, sz, key, d0=0.0):
        kutu3(y, c + n * ((sd - gom) / 2 + d0), e, n, Z, sx, sd + gom, sz, key, ('+x', '-x', '+y', '+z', '-z'))
    K(o + Z * (h / 2), w, 0.002, h, cam)
    for s in (-1, 1):
        K(o + e * (s * (w / 2 + f / 2)) + Z * (h / 2), f, t, h + f, cer)
    K(o + Z * (-f * 0.45), w + 2 * f + 0.014, t * 1.5, f * 0.9, cer)
    # the apron under the sill: a board cut in a scallop, painted
    ap = o + Z * (-f * 0.9) + n * (t * 0.55)
    pts = [ap + e * (-(w / 2 + f)), ap + e * (w / 2 + f), ap + e * (w / 2 + f * 0.5) - Z * (f * 1.1), ap + e * (w * 0.18) - Z * (f * 1.6),
           ap - Z * (f * 1.3), ap + e * (-w * 0.18) - Z * (f * 1.6), ap + e * (-(w / 2 + f * 0.5)) - Z * (f * 1.1)]
    for i in range(1, len(pts) - 1):
        y.yuz_yon([pts[0], pts[i], pts[i + 1]], cer, n)
    K(o + Z * (h + f * 0.5), w + 2 * f + 0.01, t * 1.25, f, cer)
    zt = h + f
    if tepe == 'ucgen':
        ph = (w + 2 * f) * 0.42
        d = n * (t * 1.05)
        A, B, C = o + e * (-(w / 2 + f * 1.3)) + Z * zt, o + e * (w / 2 + f * 1.3) + Z * zt, o + Z * (zt + ph)
        y.yuz_yon([A + d, B + d, C + d], cer, n)
        y.yuz_yon([A + d, C + d, C - n * gom, A - n * gom], cer, Z - e)
        y.yuz_yon([C + d, B + d, B - n * gom, C - n * gom], cer, Z + e)
        # an inner triangle in the accent colour and a carved knob on top
        A2, B2, C2 = o + e * (-(w / 2) * 0.62) + Z * (zt + ph * 0.18), o + e * ((w / 2) * 0.62) + Z * (zt + ph * 0.18), o + Z * (zt + ph * 0.7)
        y.yuz_yon([A2 + d * 1.25, B2 + d * 1.25, C2 + d * 1.25], panjur or 'boya_kirmizi', n)
        kure(y, o + Z * (zt + ph + f * 0.4) + n * (t * 0.5), f * 0.55, sus, n=6, kat=3)
    elif tepe == 'kemer':
        R = w / 2 + f * 1.2
        ring = [o + e * (R * math.cos(math.pi * k / 10)) + Z * (zt + R * 0.8 * math.sin(math.pi * k / 10)) for k in range(11)]
        d = n * (t * 1.05)
        c0 = o + Z * zt
        for k in range(10):
            y.yuz_yon([c0 + d, ring[k] + d, ring[k + 1] + d], cer, n)
            y.yuz_yon([ring[k] + d, ring[k + 1] + d, ring[k + 1] - n * gom, ring[k] - n * gom], cer, ring[k] + ring[k + 1] - c0 * 2)
        ring2 = [o + e * (R * 0.55 * math.cos(math.pi * k / 8)) + Z * (zt + R * 0.44 * math.sin(math.pi * k / 8)) for k in range(9)]
        for k in range(8):
            y.yuz_yon([c0 + d * 1.25, ring2[k] + d * 1.25, ring2[k + 1] + d * 1.25], panjur or 'boya_kirmizi', n)
        kure(y, o + Z * (zt + R * 0.8 + f * 0.4) + n * (t * 0.5), f * 0.5, sus, n=6, kat=3)
    if panjur:
        ws = w * 0.52
        for s in (-1, 1):
            c = o + e * (s * (w / 2 + f + ws / 2 + 0.002)) + Z * (h / 2)
            K(c, ws, 0.004, h * 0.98, panjur)
            K(c, ws * 0.5, 0.0055, h * 0.55, cer)
    return o + Z * zt


def oymali_sacak(y, p0, p1, n, key='beyaz', en=0.016, dis=8, d=0.004):
    """a carved fretwork board (prichelina / under-eave valance) from p0 to p1, hanging en down with dis teeth, its
    face towards n, a hair (d) out"""
    p0, p1, n = Vector(p0), Vector(p1), Vector(n).normalized()
    m = dis
    for k in range(m):
        a, b = p0.lerp(p1, k / m) + n * d, p0.lerp(p1, (k + 1) / m) + n * d
        c = (a + b) / 2 - Z * en
        levha(y, [a, b, b - Z * en * 0.45, c, a - Z * en * 0.45], key, n, kil=0.003)


def ahsap_cati(y, x0, x1, y0, y1, z, h, sacak=0.03, uc_sacak=0.035, dilim=('sindira', 'sindira2'), oyma='beyaz', konek=True,
               nr=12, ns=8, ucluk='ahsap_dikey', mahya='ahsap_koyu'):
    """a steep plank / shingle gable roof (ridge along the longer side) with carved white barge boards (prichelina)
    hanging a towel board (polotentse) at the apex, and a horse-head ridge finial (konek) at each end. Returns the
    ridge z"""
    zr = cati_besik(y, x0, x1, y0, y1, z, h, sacak, dilim[0], mahya, kalinlik=0.01, alt_key='ahsap_koyu', ucluk_key=ucluk,
                    uc_sacak=uc_sacak, nr=nr, ns=ns, dilim=list(dilim), mahya_en=0.012)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    boy_x = (x1 - x0) >= (y1 - y0)
    # work in a frame where the ridge runs along local x
    if boy_x:
        L, Wb, rot = (x1 - x0) / 2 + uc_sacak, (y1 - y0) / 2 + sacak, 0.0
    else:
        L, Wb, rot = (y1 - y0) / 2 + uc_sacak, (x1 - x0) / 2 + sacak, math.pi / 2
    with parca(y, (cx, cy, 0), rot):
        for sx in (-1, 1):
            xg = sx * (L + 0.004)
            top = V(xg, 0, zr - 0.004)
            for sy in (-1, 1):
                eave = V(xg, sy * Wb, z - 0.004)
                d = (eave - top)
                if oyma:
                    # the barge board: a wide plank down the verge, a scalloped lower edge
                    m = 7
                    for k in range(m):
                        a, b = top.lerp(eave, k / m), top.lerp(eave, (k + 1) / m)
                        levha(y, [a, b, b - Z * 0.022, (a + b) / 2 - Z * 0.03, a - Z * 0.022], oyma, V(sx, 0), kil=0.006)
            if oyma:
                # the towel board hanging from the apex
                tb = V(xg + sx * 0.001, 0, zr - 0.02)
                q = [tb + V(0, -0.016, 0), tb + V(0, 0.016, 0), tb + V(0, 0.016, -0.06), tb + V(0, 0, -0.075), tb + V(0, -0.016, -0.06)]
                levha(y, q, oyma, V(sx, 0), kil=0.005)
                kure(y, tb + V(sx * 0.003, 0, -0.035), 0.009, 'boya_kirmizi', n=6, kat=3)
            if konek:
                # the horse head on the ridge end (an ochlupen's carved end)
                p = V(sx * (L - 0.01), 0, zr + 0.002)
                boru(y, [p, p + V(sx * 0.03, 0, 0.012), p + V(sx * 0.042, 0, 0.04), p + V(sx * 0.06, 0, 0.046)], 0.008, 'ahsap_koyu', n=6, r_son=0.005)
                kure(y, p + V(sx * 0.044, 0, 0.044), 0.011, 'ahsap_koyu', n=6, kat=3)
    return zr


def kar_besik(y, x0, x1, y0, y1, z, h, sacak=0.03, uc_sacak=0.035, kapsam=0.6, tohum=1, kalin=0.006, key='beyaz', n=10,
              taraflar=(-1, 1)):
    """snow lying on a cati_besik roof (same arguments): a sheet down from the ridge with a ragged lower edge, kapsam
    of the slope covered"""
    rng = random.Random(tohum)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    boy_x = (x1 - x0) >= (y1 - y0)
    if boy_x: a, b, rot = (x1 - x0) / 2 + uc_sacak, (y1 - y0) / 2 + sacak, 0.0
    else: a, b, rot = (y1 - y0) / 2 + uc_sacak, (x1 - x0) / 2 + sacak, math.pi / 2
    with parca(y, (cx, cy, 0), rot):
        for sy in taraflar:
            xs = [-a * 0.97 + 2 * a * 0.97 * i / n for i in range(n + 1)]
            ts = [max(0.05, min(0.97, 1 - kapsam + rng.uniform(-0.12, 0.12))) for _ in xs]
            P = lambda x, t, d: V(x, sy * b * (1 - t), z + h * t + d)
            for i in range(n):
                y.yuz_yon([P(xs[i], ts[i], kalin), P(xs[i + 1], ts[i + 1], kalin), P(xs[i + 1], 1, kalin), P(xs[i], 1, kalin)], key, Z)
                y.yuz_yon([P(xs[i], ts[i], kalin), P(xs[i + 1], ts[i + 1], kalin), P(xs[i + 1], ts[i + 1], -0.001), P(xs[i], ts[i], -0.001)], key,
                          V(0, sy, 0.2))
            for i, s in ((0, -1), (n, 1)):
                y.yuz_yon([P(xs[i], ts[i], kalin), P(xs[i], 1, kalin), P(xs[i], 1, -0.001), P(xs[i], ts[i], -0.001)], key, V(s, 0))


def kar_yigin(y, x, yy, z, r, h, key='beyaz', n=10, tohum=0, uz=1.0, aci=0.0):
    """a soft snow drift: a low lumpy dome"""
    rng = random.Random(tohum)
    with parca(y, (x, yy, z), aci):
        kk = [1 + rng.uniform(-0.15, 0.15) for _ in range(n)]
        rings = []
        for j, (fr, fz) in enumerate(((1.0, -0.004), (0.85, 0.45), (0.55, 0.85), (0.0, 1.0))):
            rings.append([V(r * fr * kk[i] * uz * math.cos(TAU * i / n), r * fr * kk[i] * math.sin(TAU * i / n), h * fz) for i in range(n)])
        for j in range(3):
            A, B = rings[j], rings[j + 1]
            for i in range(n):
                k = (i + 1) % n
                if j == 2: y.yuz_yon([A[i], A[k], B[0] * 0 + V(0, 0, h)], key, Z)
                else: y.yuz_yon([A[i], A[k], B[k], B[i]], key, (A[i] + A[k]) / 2)


def ladin(y, x, yy, z, boy=0.3, r=None, kar=True, key='yesil_koyu', n=8, kat=4, tohum=0):
    """a spruce: a trunk and stacked cones (kat tiers), snow on the upper side of each tier (kar)"""
    r = r or boy * 0.3
    y.prizma((x, yy), boy * 0.03, z, z + boy * 0.2, 'ahsap', n=5)
    for k in range(kat):
        t = k / kat
        z0 = z + boy * (0.12 + 0.72 * t)
        rr = r * (1 - 0.72 * t)
        hh = boy * (0.42 - 0.12 * t)
        ring = cokgen((x, yy), rr, n, kat=0.3 * k)
        ring2 = cokgen((x, yy), rr * 0.62, n, kat=0.3 * k)
        tepe = V(x, yy, z0 + hh)
        for i in range(n):
            j = (i + 1) % n
            a, b = ring[i] + Z * z0, ring[j] + Z * z0
            c, d = ring2[j] + Z * (z0 + hh * 0.38), ring2[i] + Z * (z0 + hh * 0.38)
            y.yuz_yon([a, b, c, d], key, (a + b) / 2 - V(x, yy, z0 + hh * 0.3))
            y.yuz_yon([d, c, tepe], 'beyaz' if kar else key, (c + d) / 2 - V(x, yy, z0 + hh * 0.5))
        y.yuz_yon([p + Z * z0 for p in ring], key, -Z)


def kayin(y, x, yy, z, boy=0.3, yaprak=True, tohum=0):
    """a birch: a white trunk with dark marks, a few branches and a light crown (yaprak) or bare twigs"""
    rng = random.Random(tohum)
    boru(y, [V(x, yy, z), V(x + 0.006, yy, z + boy * 0.5), V(x - 0.004, yy + 0.004, z + boy * 0.85)], boy * 0.035, 'beyaz', n=6, r_son=boy * 0.018)
    for k in range(4):
        zz = z + boy * (0.12 + 0.13 * k)
        t = rng.uniform(0, TAU)
        kutu3(y, V(x + 0.0005 * k + math.cos(t) * boy * 0.03, yy + math.sin(t) * boy * 0.03, zz), V(-math.sin(t), math.cos(t), 0),
              V(math.cos(t), math.sin(t), 0), Z, boy * 0.03, 0.006, boy * 0.012, 'koyu')
    for k in range(4):
        t = TAU * k / 4 + rng.uniform(-0.4, 0.4)
        p = V(x, yy, z + boy * (0.45 + 0.1 * k))
        boru(y, [p, p + V(math.cos(t) * boy * 0.16, math.sin(t) * boy * 0.16, boy * 0.15)], boy * 0.012, 'beyaz', n=4, r_son=boy * 0.005)
    if yaprak:
        for i, (dx, dy, dz, rr) in enumerate(((0, 0, 0.78, 0.2), (0.09, 0.04, 0.66, 0.15), (-0.08, -0.05, 0.64, 0.15), (0.02, 0.09, 0.9, 0.14))):
            kure(y, (x + dx * boy, yy + dy * boy, z + dz * boy), rr * boy, 'boya_yesil' if i % 2 else 'zeytin', n=9, kat=4)


# ---------------------------------------------------------------- timber church parts
BOCHKA = [(1.0, 0.0), (1.05, 0.16), (1.0, 0.34), (0.82, 0.54), (0.56, 0.7), (0.3, 0.83), (0.11, 0.93), (0.0, 1.0)]


def bochka(y, c, w, L, z, h, aci=0.0, key='ahsap_acik', alin='ahsap_dikey', sogan=True, sogan_r=None, pul=('ahsap_acik', 'kutuk'),
           hac=True, sacak=0.006):
    """a 'barrel' roof (bochka) of the Russian timber churches: an ogee (keel) arched section w wide and h high,
    running L along angle aci from c (its inner end at c, the gable facing out), boards on its gable, and (sogan) a
    small scaled onion with a cross at its outer end. Returns the onion's top z (or the ridge z)"""
    pr = [(s, t) for s, t in BOCHKA]
    yarim = [((w / 2 + sacak) * s, h * t) for s, t in pr]
    prof = [(-u, v) for u, v in yarim] + [(u, v) for u, v in reversed(yarim[:-1])]   # left foot -> apex -> right foot
    with parca(y, (c[0], c[1], z), aci):
        # local x: along the barrel (0 inner end .. L outer end), y across, z up
        for k in range(len(prof) - 1):
            (u0, v0), (u1, v1) = prof[k], prof[k + 1]
            q = [V(0, u0, v0), V(L, u0, v0), V(L, u1, v1), V(0, u1, v1)]
            mid = V(L / 2, (u0 + u1) / 2, (v0 + v1) / 2)
            y.yuz_yon(q, key, mid - V(L / 2, 0, h * 0.25))
        for xx, s in ((L, 1), (0, -1)):
            for k in range(len(prof) - 1):
                (u0, v0), (u1, v1) = prof[k], prof[k + 1]
                y.yuz_yon([V(xx, 0, 0), V(xx, u0, v0), V(xx, u1, v1)], alin if s > 0 else key, V(s, 0, 0))
        # the eave's underside
        y.yuz_yon([V(0, -w / 2 - sacak, 0), V(L, -w / 2 - sacak, 0), V(L, w / 2 + sacak, 0), V(0, w / 2 + sacak, 0)], 'ahsap_koyu', -Z)
        # a carved board round the gable
        for k in range(len(prof) - 1):   # (a flat band, its outer edge closed)
            (u0, v0), (u1, v1) = prof[k], prof[k + 1]
            d0 = V(0, u0, v0 - h * 0.3).normalized() * 0.008; d1 = V(0, u1, v1 - h * 0.3).normalized() * 0.008
            y.yuz_yon([V(L + 0.003, u0, v0), V(L + 0.003, u1, v1), V(L + 0.003, u1, v1) - d1, V(L + 0.003, u0, v0) - d0], 'beyaz', X)
            y.yuz_yon([V(L + 0.003, u0, v0), V(L + 0.003, u1, v1), V(L, u1, v1), V(L, u0, v0)], 'beyaz', (d0 + d1))
        top = z + h
    if sogan:
        r = sogan_r or w * 0.17
        e = V(math.cos(aci), math.sin(aci))
        cx, cy = c[0] + e.x * L * 0.78, c[1] + e.y * L * 0.78
        zb = z + h * 0.86
        zn = boyun(y, (cx, cy), r * 0.5, zb, r * 0.9, 'ahsap_acik', n=10)
        top = kubbe(y, (cx, cy), r, zn - 0.001, 'sogan', r * 1.8, 'ahsap_acik', n=10, pul=list(pul), alt=1)
        if hac: top = ortodoks_hac(y, cx, cy, top - 0.003, r * 1.5, 'altin', top=False)
    return top


def kutuk_sekizgen(y, c, r, z0, h, rl=0.011, key='kutuk', kat=math.pi / 8, cekirdek=None):
    """an octagonal log tier (vosmerik): eight log walls with crossed ends, alternate walls half a log up. Returns
    the top z"""
    k = cokgen(c, r, 8, kat)
    for i in range(8):
        off = rl if i % 2 else 0
        kutuk_duvar2(y, k[i], k[(i + 1) % 8], z0 + off, z0 + h + off, rl, key, uzanti=rl * 1.2, cekirdek=cekirdek)
    return z0 + h + rl
