# More helpers for the Indian landmarks lm_kizilkale, lm_racputkisla, lm_baharatpazari (not a building: imported by
# those scripts, next to hint_ortak.py): Mughal engrailed (multifoil) arches, rounded merlons with loopholes, an extruded
# profile block, a curved Bengal (bangla) roof, striped awnings, spice heaps in baskets, carts, spiked gate leaves.
import math
from mathutils import Vector
from parcalar import *


def dilim_yolu(x0, x1, hs, sivri=0.3, dilim=5, gir=0.07, k=4):
    """the outline (u, v) of a Mughal engrailed arch from (x0, hs) over the crown to (x1, hs): a pointed arch
    (kemer_yolu) whose curve is cut into dilim lobes, the cusps between them pointing down into the opening by gir x
    span. u stays monotone (the cusps only move the points down): the wall quads above it stay valid"""
    w = x1 - x0
    tp = kemer_yolu(x0, x1, hs, sivri, max(2, dilim * k))
    # arc-length parameter along the curve
    s = [0.0]
    for i in range(1, len(tp)):
        s.append(s[-1] + math.hypot(tp[i][0] - tp[i - 1][0], tp[i][1] - tp[i - 1][1]))
    L = s[-1] or 1.0
    out = []
    for (u, v), si in zip(tp, s):
        t = si / L
        d = gir * w * (1 - abs(math.sin(math.pi * dilim * t))) * math.sin(math.pi * t) ** 0.7
        out.append((u, v - d))
    out[0] = tp[0]; out[-1] = tp[-1]
    return out


def dilimli(y, a, b, z0, H, renk, v0=0.0, en=0.62, ust=0.03, derin=0.03, sivri=0.3, dilim=5, gir=0.07, k=None,
            cerceve=None, korkuluk=None, arka=True):
    """one wall bay a->b (facing the right of a->b) with a Mughal engrailed arch: the wall round it, the reveal, the
    sill and (arka) the dark back plate. renk = (wall, reveal, sill, back). cerceve = (width, key): a raised frame
    following the cusps; korkuluk: a low balustrade height in the opening. Returns (L, x0, x1, hs, apex)"""
    duvar, koyu, acik, delik = renk
    k = k or (2 if dilim <= 3 else 3)
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    Lf = lambda u, v, d=0.0: a + e * u - nc * d + Z * (z0 + v)
    x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
    w = x1 - x0
    hs = H - ust - sivri * w
    tp = dilim_yolu(x0, x1, hs, sivri, dilim, gir, k)
    y.yuz_yon([Lf(0, 0), Lf(x0, 0), Lf(x0, H), Lf(0, H)], duvar, nc)
    y.yuz_yon([Lf(x1, 0), Lf(W, 0), Lf(W, H), Lf(x1, H)], duvar, nc)
    if v0 > 0: y.yuz_yon([Lf(x0, 0), Lf(x1, 0), Lf(x1, v0), Lf(x0, v0)], duvar, nc)
    for i in range(len(tp) - 1):
        (ua, va), (ub, vb) = tp[i], tp[i + 1]
        y.yuz_yon([Lf(ua, va), Lf(ub, vb), Lf(ub, H), Lf(ua, H)], duvar, nc)
    yol = [(x0, v0)] + tp + [(x1, v0)]
    xm = (x0 + x1) / 2
    for i in range(len(yol) - 1):
        p, q = yol[i], yol[i + 1]
        vm = min(max((p[1] + q[1]) / 2, v0), hs)
        mid = (Lf(*p) + Lf(*q)) / 2
        y.yuz_yon([Lf(*p), Lf(*q), Lf(*q, derin), Lf(*p, derin)], koyu, Lf(xm, vm) - mid)
    y.yuz_yon([Lf(x0, v0), Lf(x1, v0), Lf(x1, v0, derin), Lf(x0, v0, derin)], acik, Z)
    if arka:
        y.yuz_yon([Lf(*p, derin) for p in yol], delik, nc)
    if korkuluk:
        d0, d1, hh = derin * 0.3, derin * 0.55, v0 + korkuluk
        kutu(y, Lf(x0, v0, d1), e, w, d1 - d0, korkuluk, acik, 'onarkaust')
    if cerceve:
        f, mk = cerceve
        d = -0.002
        def dis(p):
            u, v = p
            if v <= hs + 1e-9:
                return (u - f if u < xm else u + f, v)
            kk = Vector((u - xm, v - (hs - w * 0.15))).normalized()
            return (u + kk.x * f, v + kk.y * f)
        for i in range(len(yol) - 1):
            p, q = yol[i], yol[i + 1]
            y.yuz_yon([Lf(*p, d), Lf(*q, d), Lf(*dis(q), d), Lf(*dis(p), d)], mk, nc)
            orta = (Lf(*dis(p)) + Lf(*dis(q))) / 2
            y.yuz_yon([Lf(*dis(p), d), Lf(*dis(q), d), Lf(*dis(q), 0), Lf(*dis(p), 0)], mk, orta - Lf(xm, (v0 + hs) / 2))
            vm = min(max((p[1] + q[1]) / 2, v0), hs)
            ic_ = (Lf(*p) + Lf(*q)) / 2
            y.yuz_yon([Lf(*p, d), Lf(*q, d), Lf(*q, 0), Lf(*p, 0)], mk, Lf(xm, vm) - ic_)
    return Lf, x0, x1, hs, H - ust


def dilimli_sira(y, a, b, n, z0, H, renk, **kw):
    """n engrailed bays along a->b"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    for i in range(n):
        dilimli(y, a.lerp(b, i / n), a.lerp(b, (i + 1) / n), z0, H, renk, **kw)


def profil_blok(y, o, e, prof, kal, key, atla=()):
    """a block whose front is the convex polygon prof [(u, v), ...] (CCW seen from the front) on the vertical plane
    through o along e, facing the right of e, extruded kal back (to the left of e); atla: side faces (edge i -> i+1)
    left out (a bottom sitting on a parapet)"""
    o = Vector(o); e = Vector(e); e.z = 0; e.normalize(); nc = V(e.y, -e.x)
    F = [o + e * u + Z * v for u, v in prof]
    B = [p - nc * kal for p in F]
    c = sum(F, Vector()) / len(F) - nc * (kal / 2)
    y.yuz_yon(F, key, nc)
    y.yuz_yon(B, key, -nc)
    m = len(F)
    for i in range(m):
        if i in atla: continue
        j = (i + 1) % m
        yuz_dis(y, [F[i], F[j], B[j], B[i]], key, c)


def kangura(y, a, b, z, h=0.03, kal=0.016, key='kirmizi_tas', w=None, g=None, delik='koyu', n_yay=4, alt=False):
    """Mughal / Rajput merlons along a->b (their outer face on the line, facing its right): each a block with a round
    (slightly pointed) head, and a dark loophole in it (delik=None: none). alt: their bottom face too (it sits on the
    parapet and is never seen)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-5: return
    e = (b - a) / L; nc = V(e.y, -e.x)
    w = w or h * 0.75; g = g or h * 0.5
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g
    if w <= 0.003: return
    hs = h - w * 0.55
    prof = [(0, 0), (w, 0), (w, hs)]
    for i in range(1, n_yay):
        t = math.pi * i / n_yay
        prof.append((w / 2 + w / 2 * math.cos(t), hs + w * 0.55 * math.sin(t) ** 0.8))
    prof.append((0, hs))
    for i in range(k):
        o = a + e * (i * (w + g)) + Z * z
        profil_blok(y, o, e, prof, kal, key, atla=() if alt else (0,))
        if delik:   # (a dark slot a hair proud of the flat front)
            q0 = o + e * (w / 2 - w * 0.12) + nc * 0.0015 + Z * (h * 0.22)
            y.yuz_yon([q0, q0 + e * (w * 0.24), q0 + e * (w * 0.24) + Z * (h * 0.32), q0 + Z * (h * 0.32)], delik, nc)


def kangura_halka(y, kose, z, h=0.03, kal=0.016, key='kirmizi_tas', kapali=True, **kw):
    n = len(kose)
    for i in range(n if kapali else n - 1):
        kangura(y, kose[i], kose[(i + 1) % n], z, h, kal, key, **kw)


def bangla_cati(y, x0, x1, y0, y1, z, h, key='mermer', sacak=0.012, alt_key=None, nu=10, nv=8, kalin=0.006, egik=0.35,
                bicim='yastik', sarkma=0.55, sirt_key=None, alin_z=None):
    """a curved Bengal (bangla) roof over the rectangle (ridge along x): the section across is an arch, the eaves droop
    towards both ends (egik x h). Top surface, the eave fascia all round and the soffit back to the walls. Returns the
    ridge z. bicim='dochala': the hut roof proper: a crisp ridge arching down to its ends (egik x h), two slopes
    bulging a little and eave corners hanging well down (sarkma x h under z): set it on pillars / walls that stop
    under z. sirt_key: a ridge roll; alin_z: closed gable ends (tympana) from that z up to the roof at the wall line"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2 + sacak, (y1 - y0) / 2 + sacak
    def P(u, v):   # u, v in -1..1
        if bicim == 'dochala':
            t = abs(v)
            sirt, sz = h * (1 - egik * u * u), -h * sarkma * u * u
            return V(cx + a * u, cy + b * v, z + sz + (sirt - sz) * (1 - t + 0.4 * t * (1 - t)))
        zz = z + h * (1 - abs(v) ** 1.6) - h * egik * (u * u) * (1 - 0.5 * (1 - abs(v) ** 1.6))
        return V(cx + a * u, cy + b * v, zz)
    U = [-1 + 2 * i / nu for i in range(nu + 1)]
    W = [-1 + 2 * j / nv for j in range(nv + 1)]
    for i in range(nu):
        for j in range(nv):
            q = [P(U[i], W[j]), P(U[i + 1], W[j]), P(U[i + 1], W[j + 1]), P(U[i], W[j + 1])]
            y.yuz_yon(q, key, Z)
    ak = alt_key or key
    if bicim == 'dochala':
        if sirt_key:
            boru(y, [P(-1 + 2 * i / nu, 0) + Z * 0.001 for i in range(nu + 1)], max(0.0025, kalin * 0.55), sirt_key, n=6)
        if alin_z is not None:
            uw, vb = (a - sacak) / a, (b - sacak) / b
            for s in (-1, 1):
                ust = [P(s * uw, vb * (-1 + 2 * j / nv)) for j in range(nv + 1)]
                xw = cx + s * (a - sacak)
                pol = [V(xw, cy - b + sacak, alin_z), V(xw, cy + b - sacak, alin_z)] + [V(xw, p.y, p.z) for p in reversed(ust)]
                y.yuz_yon(pol if s > 0 else pol[::-1], ak, V(s, 0, 0))
                # (the long sides too: a frieze from alin_z up under the eave, so no slit shows the roof's underside)
                ust = [P(uw * (-1 + 2 * i / nu), s * vb) for i in range(nu + 1)]
                yw = cy + s * (b - sacak)
                pol = [V(cx - a + sacak, yw, alin_z), V(cx + a - sacak, yw, alin_z)] + [V(p.x, yw, p.z) for p in reversed(ust)]
                y.yuz_yon(pol, ak, V(0, s, 0))
    ring = [(U[i], -1) for i in range(nu)] + [(1, W[j]) for j in range(nv)] + [(U[i], 1) for i in range(nu, 0, -1)] + [(-1, W[j]) for j in range(nv, 0, -1)]
    m = len(ring)
    for k in range(m):
        p, q = P(*ring[k]), P(*ring[(k + 1) % m])
        out = V((p.x + q.x) / 2 - cx, (p.y + q.y) / 2 - cy)
        y.yuz_yon([p, q, q - Z * kalin, p - Z * kalin], ak, out)
        # soffit: from the fascia's foot in to the wall line, at the eave height
        pw = V(cx + (p.x - cx) * (1 - sacak / a if abs(p.x - cx) > a - 1e-6 else 1), cy + (p.y - cy) * ((b - sacak) / b), 0)
        qw = V(cx + (q.x - cx) * (1 - sacak / a if abs(q.x - cx) > a - 1e-6 else 1), cy + (q.y - cy) * ((b - sacak) / b), 0)
        pw.x = max(x0, min(x1, pw.x)); qw.x = max(x0, min(x1, qw.x))
        y.yuz_yon([p - Z * kalin, q - Z * kalin, V(qw.x, qw.y, min(q.z, p.z) - kalin), V(pw.x, pw.y, min(q.z, p.z) - kalin)], ak, -Z)
    return z + h


def tente(y, a, b, z, derin, dus, keys=('boya_kirmizi', 'beyaz'), n=None, direk='ahsap_koyu', direkli=True, kil=0.0015):
    """a striped cloth awning from the wall line a->b (at height z) sloping out derin to its right and dus lower, seen
    from both sides (top and underside); stripes run outward. direkli: two (or more) thin poles under its front edge"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    n = n or max(2, int(round(L / 0.022)))
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        # (the sag follows the corners: one sag per stripe left steps between stripes that showed the twin's back)
        sp, sq = 0.003 * math.sin(math.pi * i / n), 0.003 * math.sin(math.pi * (i + 1) / n)
        pts = [p + Z * z, q + Z * z, q + nc * derin + Z * (z - dus - sq), p + nc * derin + Z * (z - dus - sp)]
        nr = (nc * dus + Z * derin).normalized()
        iki_yuzlu(y, pts, keys[i % len(keys)], nr, kil=kil)
        # the cloth's rims (back edge, the two ends): seen edge-on the two sheets showed each other's backs
        y.yuz_yon([pts[0], pts[1], pts[1] - nr * kil, pts[0] - nr * kil], keys[i % len(keys)], -nc)
        if i == 0: y.yuz_yon([pts[0], pts[3], pts[3] - nr * kil, pts[0] - nr * kil], keys[0], -e)
        if i == n - 1: y.yuz_yon([pts[1], pts[2], pts[2] - nr * kil, pts[1] - nr * kil], keys[i % len(keys)], e)
        # the hanging valance: a short flap at the front edge
        f0, f1 = pts[3], pts[2]
        iki_yuzlu(y, [f0, f1, f1 - Z * 0.008, f0 - Z * 0.008], keys[(i + 1) % len(keys)], nc, kil=kil)
    if direkli:
        m = max(2, int(round(L / 0.12)) + 1)
        for k in range(m):
            p = a.lerp(b, (k + 0.06) / (m - 1) * 0.88 if m > 1 else 0.5) + nc * (derin - 0.004)
            p = a.lerp(b, 0.04 + 0.92 * k / (m - 1)) + nc * (derin - 0.004)
            y.prizma((p.x, p.y), 0.0022, 0.0, z - dus - 0.003, direk, n=4, ust=True)


def tente_z0(y, a, b, z, derin, dus, z_yer, keys=('boya_kirmizi', 'beyaz'), direk='ahsap_koyu', **kw):
    """tente with poles standing on z_yer"""
    tente(y, a, b, z, derin, dus, keys, direkli=False, direk=direk, **kw)
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    m = max(2, int(round(L / 0.12)) + 1)
    for k in range(m):
        p = a.lerp(b, 0.04 + 0.92 * k / (m - 1)) + nc * (derin - 0.004)
        y.prizma((p.x, p.y), 0.0022, z_yer, z - dus - 0.003, direk, n=4, ust=True)


def sepet(y, x, yy, z, r=0.018, h=0.012, key='saz', ic='koyu', n=10):
    """a low round basket (its rim, and the inside shown by a slightly lower disc)"""
    donel(y, (x, yy), [(0.0, z), (r * 0.85, z), (r, z + h), (r * 0.9, z + h)], key, n=n)
    return z + h


def yigin(y, x, yy, z, r, h, key, sepetli=True, sepet_key='saz', n=12):
    """a conical spice heap (rounded tip), in a basket if sepetli. Returns its top z"""
    r0 = r * 0.98
    if sepetli:
        z = sepet(y, x, yy, z, r * 1.08, h * 0.32, sepet_key, n=n)
        r0 = r * 1.08 * 0.9      # (the heap starts at the basket's rim: no gap into it)
    donel(y, (x, yy), [(r0, z), (r * 0.72, z + h * 0.42), (r * 0.36, z + h * 0.82), (r * 0.12, z + h * 0.97), (0.0, z + h)], key, n=n)
    return z + h


def cuval(y, x, yy, z, key='kumas', r=0.011, h=0.022, aci=0.0, ag='boya_sari'):
    """an open sack (jute) with its rolled rim and the spice showing (ag)"""
    donel(y, (x, yy), [(0.0, z), (r * 0.9, z), (r * 1.08, z + h * 0.45), (r, z + h * 0.85), (r * 1.06, z + h), (r * 0.95, z + h * 1.04)], key, n=8)
    donel(y, (x, yy), [(r * 0.95, z + h * 1.04), (r * 0.5, z + h * 1.12), (0.0, z + h * 1.15)], ag, n=8)


def araba(y, x, yy, z, aci=0.0, s=1.0, key='ahsap', teker='ahsap_koyu', yuk=None, okuz=None):
    """a two-wheeled bullock cart (bed, side rails, big spoked-look wheels, a shaft forward along +x); yuk: a key for a
    load (sacks); okuz: a key for a humped zebu ox in the shafts"""
    with parca(y, (x, yy, z), aci, s):
        kutu_merkez(y, (0, 0), 0.08, 0.05, 0.006, key, z0=0.028)
        for sy in (-1, 1):
            kutu_merkez(y, (0, sy * 0.024), 0.08, 0.003, 0.016, key, z0=0.034)
            # the wheel: a thick ring (rim) with a hub and spokes
            c = V(0.0, sy * 0.032, 0.026)
            n = 12
            rim = [c + V(0.024 * math.cos(TAU * i / n), 0, 0.024 * math.sin(TAU * i / n)) for i in range(n)]
            rin = [c + V(0.019 * math.cos(TAU * i / n), 0, 0.019 * math.sin(TAU * i / n)) for i in range(n)]
            for i in range(n):
                j = (i + 1) % n
                for (A, B, dy) in ((rim, rin, 0.003), (rim, rin, -0.003)):
                    pass
                o3, i3 = [p + V(0, 0.003, 0) for p in (rim[i], rim[j])], [p + V(0, 0.003, 0) for p in (rin[j], rin[i])]
                o4, i4 = [p - V(0, 0.003, 0) for p in (rim[i], rim[j])], [p - V(0, 0.003, 0) for p in (rin[j], rin[i])]
                y.yuz_yon(o3 + i3, teker, V(0, 1, 0))
                y.yuz_yon(o4 + i4, teker, V(0, -1, 0))
                y.yuz_yon([o3[0], o3[1], o4[1], o4[0]], teker, (rim[i] + rim[j]) / 2 - c)
                y.yuz_yon([i3[1], i3[0], i4[0], i4[1]], teker, c - (rin[i] + rin[j]) / 2)
            for k in range(4):
                t = math.pi * k / 4
                d = V(math.cos(t), 0, math.sin(t))
                cubuk(y, c - d * 0.019, c + d * 0.019, 0.0025, teker)
            boru(y, [c - V(0, 0.005, 0), c + V(0, 0.005, 0)], 0.005, teker, n=6)
        boru(y, [V(0, -0.032, 0.026), V(0, 0.032, 0.026)], 0.0025, teker, n=4, kapat=False)
        if not okuz: cubuk(y, V(0.04, 0, 0.03), V(0.12, 0, 0.036), 0.005, key)
        if yuk:
            for i, (px, py) in enumerate(((-0.022, -0.011), (-0.022, 0.011), (0.008, -0.011), (0.008, 0.011), (-0.007, 0.0))):
                hz = 0.034 + (0.012 if i == 4 else 0)
                elips = [(0.0, hz), (0.011, hz + 0.002), (0.012, hz + 0.008), (0.009, hz + 0.014), (0.0, hz + 0.016)]
                donel(y, (px, py), elips, yuk if isinstance(yuk, str) else yuk[i % len(yuk)], n=8)
        if okuz:
            # a pair of zebu oxen under a yoke, the pole running up to it
            ox = 0.135
            for sy in (-1, 1):
                zebu(y, ox, sy * 0.021, 0.0, 0.0, okuz, boynuz=('boya_kirmizi', 'kum_acik')[sy > 0])
            cubuk(y, V(ox + 0.036, -0.036, 0.061), V(ox + 0.036, 0.036, 0.061), 0.0032, key)
            for sy in (-1, 1):
                cubuk(y, V(ox + 0.031, sy * 0.021 - 0.006 * sy, 0.061), V(ox + 0.031, sy * 0.021 - 0.006 * sy, 0.048), 0.0016, 'ahsap_koyu')
                cubuk(y, V(ox + 0.031, sy * 0.021 + 0.006 * sy, 0.061), V(ox + 0.031, sy * 0.021 + 0.006 * sy, 0.048), 0.0016, 'ahsap_koyu')
            cubuk(y, V(0.04, 0, 0.03), V(ox + 0.036, 0, 0.058), 0.0035, key)


def zebu(y, x, yy, z, aci=0.0, key='beyaz', boynuz='kum_acik', s=1.0):
    """a humped zebu ox facing aci (+x local), hooves at z, ~0.1 s long, withers ~0.055 s: a deep barrel, the tall
    hump over the shoulders, a hanging dewlap, a long down-turned face, lyre horns rising from the poll (boynuz: their
    key, often painted), drooping ears, legs with dark hooves and a tufted tail"""
    from hint_ortak import elipsoid
    with parca(y, (x, yy, z), aci, s):
        for lx in (-0.03, 0.026):
            for sy in (-1, 1):
                boru(y, [V(lx, sy * 0.0085, 0.04), V(lx + 0.001, sy * 0.0085, 0.02), V(lx, sy * 0.0085, 0.004)], 0.0042, key, n=6, r_son=0.003)
                y.prizma((lx, sy * 0.0085), 0.0034, 0.0, 0.005, 'koyu', n=6)
        elipsoid(y, (-0.004, 0, 0.044), 0.04, 0.0165, 0.0165, key, n=12, kat=6)        # barrel
        elipsoid(y, (0.022, 0, 0.043), 0.022, 0.0175, 0.02, key, n=10, kat=5)         # chest
        elipsoid(y, (0.018, 0, 0.066), 0.0125, 0.009, 0.016, key, n=10, kat=5)        # the hump
        elipsoid(y, (0.036, 0, 0.033), 0.015, 0.0035, 0.012, key, n=8, kat=4)        # dewlap
        elipsoid(y, (0.041, 0, 0.053), 0.012, 0.0085, 0.0105, key, n=8, kat=4)       # neck
        boru(y, [V(0.048, 0, 0.058), V(0.059, 0, 0.051), V(0.067, 0, 0.041)], 0.0072, key, n=7, r_son=0.0048)   # long face
        kure(y, (0.068, 0, 0.0395), 0.005, 'koyu', n=6, kat=3)                         # muzzle
        for sy in (-1, 1):
            boru(y, [V(0.051, sy * 0.0045, 0.061), V(0.052, sy * 0.011, 0.07), V(0.055, sy * 0.009, 0.08), V(0.058, sy * 0.005, 0.085)],
                 0.0021, boynuz, n=5, r_son=0.0008)
            elipsoid(y, (0.053, sy * 0.011, 0.055), 0.004, 0.005, 0.0016, key, n=6, kat=3)   # ear
            kure(y, (0.058, sy * 0.0055, 0.055), 0.0013, 'koyu', n=5, kat=2)                  # eye
        boru(y, [V(-0.043, 0, 0.05), V(-0.047, 0, 0.032), V(-0.047, 0, 0.016)], 0.0013, key, n=4, r_son=0.001)
        kure(y, (-0.047, 0, 0.014), 0.0028, 'koyu', n=6, kat=3)


def civili_kanat(y, a, b, z0, H, key='ahsap', civi='demir', nu=4, nv=5, d=0.002, r=0.0026, boy=0.007):
    """a gate leaf on the wall line a->b (facing its right): planks, iron bands and rows of conical iron spikes against
    war elephants (Rajput / Mughal fort gates)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    kutu(y, a + Z * z0, e, L, d, H, key, 'onsagsolust')   # (its front d proud of the line, its back into the wall)
    o = a + nc * d
    for j in range(3):
        zz = z0 + H * (0.18 + 0.32 * j)
        kutu(y, o + Z * zz, e, L, 0.0015, H * 0.035, civi, 'onsagsolust')
    for i in range(nu):
        for j in range(nv):
            p = o + e * (L * (i + 0.5) / nu) + Z * (z0 + H * (0.12 + 0.76 * j / max(1, nv - 1)))
            donel(y, (0, 0), [(r, 0.0), (r * 0.4, boy * 0.6), (0.0, boy)], civi, n=6)
            # turn the spike just added (built along +z at the origin) to point out of the leaf
            n6 = 12
            for f in range(len(y.faces) - n6, len(y.faces)):
                pts, kk = y.faces[f]
                q = []
                for (px, py, pz) in pts:
                    q.append(tuple(p + e * px + Z * py + nc * pz))
                y.faces[f] = (q, kk)


def chhatri2(y, cx, cy, z, r, n=8, kolon='kum_acik', kubbe='kum_acik', kaide='kum', kat=math.pi / 8, h=None, nk=16, kaide_h=None,
             yaprak=None, s_son=1.0, sogan=False):
    """a lighter chhatri (hint_ortak.chhatri with fewer faces, for the many on walls and roofs): a plinth, n pillars
    with bracket capitals, a lintel ring, a chhajja, a drum and a lotus-crowned dome of nk segments. Returns the tip z"""
    from hint_ortak import chhajja, lotus_kubbe
    h = h or r * 1.35
    kh = kaide_h if kaide_h is not None else r * 0.22
    rk = r * 1.18
    if kh > 0:
        y.prizma((cx, cy), rk, z, z + kh, kaide, n=n, kat=kat)
    z0 = z + kh
    kose = cokgen((cx, cy), r, n, kat)
    w = max(0.005, r * 0.16)
    for p in kose:
        a = math.atan2(p.y - cy, p.x - cx)
        kutu_merkez(y, (p.x, p.y), w, w, h * 0.86, kolon, z0=z0, aci=a, yuzler='onarkasagsol')
        kutu_merkez(y, (p.x, p.y), w * 1.5, w * 1.5, h * 0.07, kolon, z0=z0 + h * 0.86, aci=a, yuzler='onarkasagsol')
    zl = z0 + h * 0.93
    hl = h * 0.12
    dis = cokgen((cx, cy), r + w * 0.75, n, kat)
    ic = cokgen((cx, cy), r - w * 0.75, n, kat)
    duvarlar(y, dis, zl, zl + hl, kolon)
    duvarlar(y, [ic[(n - i) % n] for i in range(n)], zl, zl + hl, kolon)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([ic[i] + Z * zl, ic[j] + Z * zl, dis[j] + Z * zl, dis[i] + Z * zl], kolon, -Z)
    zc = zl + hl
    # (the lintel ring closed: its top and a ceiling under the dome, seen through the pillars)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([ic[i] + Z * zc, ic[j] + Z * zc, dis[j] + Z * zc, dis[i] + Z * zc], kolon, Z)
    y.yuz_yon([p + Z * zl for p in ic], kolon, -Z)
    chhajja(y, dis, zc - r * 0.16, r * 0.16, r * 0.28, kolon)
    rd = r * 0.92
    y.prizma((cx, cy), rd, zc, zc + r * 0.12, kolon, n=nk, ust=True)
    return lotus_hafif(y, (cx, cy), rd * 0.98, zc + r * 0.12, rd * 0.9, kubbe, n=nk, yaprak=yaprak or kolon, s_son=s_son, sogan=sogan)


def lotus_hafif(y, c, r, z, h=None, key='mermer', n=16, yaprak='tas_acik', s_son=1.0, sogan=False, finial='altin'):
    """a light Mughal dome (for the many small ones): a hemisphere (or a squat onion), a lotus cushion at its crown and
    a short gilded finial (pot and spike). Returns the tip z"""
    h = h or r * 0.95
    if sogan:
        tz = sogan_kubbe(y, c, r, z, h * 1.25, key, n=n, boyun=0.7, sivri=0.1)
        zt = tz - h * 0.1
        rt = r * 0.16
    else:
        tz = y.kubbe(c, r, z, h, key, n=n, kat=4).z
        zt = tz - h * 0.05
        rt = r * 0.3
    donel(y, c, [(rt * 1.1, zt - h * 0.06), (rt * 0.9, zt + r * 0.03), (rt * 0.45, zt + r * 0.08), (0.0, zt + r * 0.08)], yaprak, n=6)
    s = s_son * max(0.5, r / 0.06)
    zf = zt + r * 0.08
    donel(y, c, [(0.0, zf), (0.011 * s, zf + 0.01 * s), (0.005 * s, zf + 0.02 * s), (0.008 * s, zf + 0.026 * s), (0.0, zf + 0.05 * s)], finial, n=6)
    return zf + 0.05 * s


def agac2(y, x, yy, z=0.0, boy=0.08, key='boya_yesil', govde='ahsap', n=7):
    """a light round-crowned tree (for many in a garden)"""
    y.prizma((x, yy), boy * 0.05, z, z + boy * 0.5, govde, n=4, ust=False)
    kure(y, (x, yy, z + boy * 0.68), boy * 0.32, key, n=n, kat=4)


def jharokha2(y, a, b, z, w, h, d, key='kirmizi_tas', trim='kirmizi_tas_acik', cati='bangla', cati_key=None, perde=None,
              bicim='yastik'):
    """a light jharokha centred on the wall line a->b, projecting d to its right: a floor slab on two brackets, an
    engrailed opening in front, closed sides, and a curved bangla roof (cati='bangla') or a little dome ('kubbe').
    perde: a key for a jali in the lower part of the opening. bicim: the bangla's form ('yastik' / 'dochala', see
    bangla_cati). Returns the top z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    m = (a + b) / 2
    p0, p1 = m - e * (w / 2), m + e * (w / 2)
    f0, f1 = p0 + nc * d, p1 + nc * d
    # floor slab (its top at z) and two brackets under it
    kutu(y, p1 + e * 0.004 + Z * (z - 0.008), -e, w + 0.008, d + 0.004, 0.008, trim, 'arkasagsolust')
    y.yuz_yon([p0 - e * 0.004 + Z * (z - 0.008), p1 + e * 0.004 + Z * (z - 0.008), p1 + e * 0.004 + nc * (d + 0.004) + Z * (z - 0.008),
               p0 - e * 0.004 + nc * (d + 0.004) + Z * (z - 0.008)], trim, -Z)
    for t in (0.18, 0.82):
        q = p0.lerp(p1, t)
        cubuk(y, q + Z * (z - h * 0.45), q + nc * (d * 0.85) + Z * (z - 0.009), 0.006, trim)
    dilimli(y, f0, f1, z, h, (key, key, trim, 'koyu'), v0=h * 0.06, en=0.66, ust=h * 0.14, derin=min(0.008, d * 0.5), sivri=0.3, dilim=3,
            gir=0.06)
    if perde:
        kafes(y, f0, f1, z, 0.2, 0.8, h * 0.06, h * 0.4, perde, 4, 2, 0.002, 0.0015)
    duz_duvar(y, p0, f0, z, z + h, key)
    duz_duvar(y, f1, p1, z, z + h, key)
    zt = z + h
    k4 = [p0, f0, f1, p1]
    from hint_ortak import chhajja
    chhajja(y, k4, zt - h * 0.1, h * 0.1, h * 0.18, trim, kapali=False)
    y.yuz_yon([pp + Z * zt for pp in (p0, p1, f1, f0)], trim, Z)
    ck = cati_key or trim
    if cati == 'bangla' and abs(e.y) < 1e-6:
        xs = sorted((p0.x, p1.x)); ys = sorted((p0.y, f0.y))
        if bicim == 'dochala':
            hh = h * 0.42
            return bangla_cati(y, xs[0], xs[1], ys[0], ys[1], zt + hh * 0.45, hh, ck, sacak=0.008, alt_key=trim, nu=8, nv=4,
                               kalin=0.004, egik=0.4, bicim='dochala', sarkma=0.45, alin_z=zt)
        return bangla_cati(y, xs[0], xs[1], ys[0], ys[1], zt, h * 0.38, ck, sacak=0.006, nu=6, nv=4, kalin=0.004)
    cc = (p0 + f1) / 2
    rr = min(w, d) * 0.42
    return lotus_hafif(y, (cc.x, cc.y), rr, zt, rr * 0.95, ck, n=12, yaprak=trim, s_son=0.5)


def cikinti_kenar(y, a, b, z0, z1, d, key):
    """the four edges of a panel a->b (z0..z1) set d proud of its wall (a, b on the proud line): closes the slit that
    showed the panel's back from the side"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x); g = -nc * d
    y.yuz_yon([a + Z * z0, a + Z * z1, a + g + Z * z1, a + g + Z * z0], key, -e)
    y.yuz_yon([b + Z * z0, b + Z * z1, b + g + Z * z1, b + g + Z * z0], key, e)
    y.yuz_yon([a + Z * z1, b + Z * z1, b + g + Z * z1, a + g + Z * z1], key, Z)
    y.yuz_yon([a + Z * z0, b + Z * z0, b + g + Z * z0, a + g + Z * z0], key, -Z)
