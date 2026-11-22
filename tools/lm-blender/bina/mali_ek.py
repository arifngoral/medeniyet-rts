# A copy of mali_ortak.py (frozen 2026-11-22) plus extra helpers for the Mali landmarks lm_sankore, lm_altinmadeni,
# lm_mansasaray, lm_timbuktukale (not a building: imported by those scripts). Sudano-Sahelian mud architecture on top of parcalar.py: thick plastered mud walls with
# tapering pilasters crowned by cone pinnacles, toron palm beams, through gates and recessed doors / windows; Djenne
# town houses, thatched market shades and goods, round huts, baobab and acacia trees, pirogues, caparisoned horses
# and people in boubous.
import math
from mathutils import Vector
from parcalar import *

K, KK, KT = 'kerpic', 'kerpic_koyu', 'siva_oker'
TORON = 'ahsap_acik'


# ---------------------------------------------------------------- thin sheets
def ince_levha(y, pts, key, yon, kal=0.0015, arka_key=None):
    """a thin closed slab: the face pts toward yon, its back kal behind it and the edges between them closed, so it
    reads from both sides and nothing open shows a back face (a fringe tooth, a flap)"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    arka = [p - yon * kal for p in pts]
    y.yuz_yon(pts, key, yon)
    y.yuz_yon(arka, arka_key or key, -yon)
    c = (sum(pts, Vector()) + sum(arka, Vector())) / (2 * len(pts))
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        q = [pts[i], pts[j], arka[j], arka[i]]
        y.yuz_yon(q, key, (q[0] + q[1]) / 2 - c - yon * ((q[0] + q[1]) / 2 - c).dot(yon))


# ---------------------------------------------------------------- walls with holes
def delikli(y, o, e, n, L, z0, z1, delikler, key):
    """a flat wall face from o along e (horizontal unit), L long, z0..z1, facing n, with holes cut in it.
    delikler: list of (u0, u1, v0, ust) - u along e, v0 the sill z, ust the hole's top outline as (u, z) points from
    (u0, ...) to (u1, ...) (a square head: [(u0, v1), (u1, v1)]). Holes must not overlap"""
    o, e, n = V(o[0], o[1]), V(e[0], e[1]), V(n[0], n[1])
    P = lambda u, z: o + e * u + Z * z
    u = 0.0
    for u0, u1, v0, ust in sorted(delikler, key=lambda d: d[0]):
        if u0 > u + 1e-6:
            y.yuz_yon([P(u, z0), P(u0, z0), P(u0, z1), P(u, z1)], key, n)
        if v0 > z0 + 1e-6:
            y.yuz_yon([P(u0, z0), P(u1, z0), P(u1, v0), P(u0, v0)], key, n)
        for (ua, va), (ub, vb) in zip(ust, ust[1:]):
            if min(va, vb) < z1 - 1e-6:
                y.yuz_yon([P(ua, va), P(ub, vb), P(ub, z1), P(ua, z1)], key, n)
        u = u1
    if L > u + 1e-6:
        y.yuz_yon([P(u, z0), P(L, z0), P(L, z1), P(u, z1)], key, n)


def delik_yan(y, o, e, n, u0, u1, v0, ust, derin, key, alt_key=None, arka=None):
    """the reveals of a hole (see delikli) going derin into the wall (against n), facing into the hole; arka: a key
    for a back face at that depth (a blind door / window), None for a through opening"""
    o, e, n = V(o[0], o[1]), V(e[0], e[1]), V(n[0], n[1])
    P = lambda u, z, d=0.0: o + e * u + Z * z - n * d
    yol = [(u0, v0)] + list(ust) + [(u1, v0)]
    um = (u0 + u1) / 2; vm = (v0 + min(p[1] for p in ust)) / 2
    for k in range(len(yol)):
        p, q = yol[k], yol[(k + 1) % len(yol)]
        if (V(*p) - V(*q)).length < 1e-7: continue
        alt = k == len(yol) - 1
        mid = P((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        hedef = P(um, v0 + 1) if alt else P(um, vm)
        y.yuz_yon([P(*p), P(*q), P(*q, derin), P(*p, derin)], (alt_key or key) if alt else key, hedef - mid)
    if arka:
        y.yuz_yon([P(u, v, derin) for u, v in yol], arka, n)


def kemer_ust(u0, u1, hs, sivri=0.35, k_say=8):
    """the top outline of a Sahel opening: a low pointed arch from (u0, hs) to (u1, hs)"""
    return kemer_yolu(u0, u1, hs, sivri, k_say)


# ---------------------------------------------------------------- pinnacles, pilasters, torons
def tepecik(y, c, r, z, h, key=K, n=8, yumurta=False):
    """a rounded cone pinnacle (the Sahel 'sarafar'); yumurta: an ostrich egg on its tip"""
    donel(y, c, [(r, z), (r * 0.93, z + h * 0.35), (r * 0.62, z + h * 0.72), (r * 0.22, z + h * 0.94), (0.0, z + h)], key, n=n)
    if yumurta:
        kure(y, (c[0], c[1], z + h + r * 0.32), r * 0.36, 'beyaz', n=8, kat=4)
    return z + h


def payanda(y, p, e, n, z0, z1, w=0.03, d=0.02, key=K, tepe=0.05, taper=0.78, tepe_key=None, kademe=False, arka_z=None):
    """a tapering pilaster standing on the wall line at p (its back on the wall), e along the wall, n out; it rises
    from z0 to z1 and ends in a cone pinnacle tepe high (0: a flat top). kademe: stepped - a wide lower block to half
    height with a sloping ledge, a narrower shaft above it. arka_z: close the back from that z up (where the pilaster
    stands above the wall top and is seen from behind). Returns the pinnacle's tip z"""
    if kademe:
        zm = z0 + (z1 - z0) * 0.5
        payanda(y, p, e, n, z0, zm, w * 1.25, d * 1.45, key, 0, taper=0.92)
        return payanda(y, p, e, n, zm - 0.002, z1, w * 0.95, d * 0.95, key, tepe, taper, tepe_key, arka_z=arka_z)
    p, e, n = V(p[0], p[1]), V(e[0], e[1]).normalized(), V(n[0], n[1]).normalized()
    a0, b0 = p - e * (w / 2), p + e * (w / 2)
    a1, b1 = p - e * (w * taper / 2), p + e * (w * taper / 2)
    d1 = d * taper
    A = [a0 + Z * z0, b0 + Z * z0, b0 + n * d + Z * z0, a0 + n * d + Z * z0]
    B = [a1 + Z * z1, b1 + Z * z1, b1 + n * d1 + Z * z1, a1 + n * d1 + Z * z1]
    y.yuz_yon([A[3], A[2], B[2], B[3]], key, n)
    y.yuz_yon([A[2], A[1], B[1], B[2]], key, e)
    y.yuz_yon([A[0], A[3], B[3], B[0]], key, -e)
    y.yuz_yon(B, key, Z)
    if arka_z is not None and arka_z < z1:
        t = (arka_z - z0) / (z1 - z0)
        y.yuz_yon([b0.lerp(b1, t) + Z * arka_z, a0.lerp(a1, t) + Z * arka_z, B[0], B[1]], key, -n)
    if tepe:
        c = (B[0] + B[2]) / 2
        r = min(w * taper, d1 * 1.6) * 0.52
        return tepecik(y, (c.x, c.y), r, z1 - 0.001, tepe, tepe_key or key, n=7)
    return z1


def toron(y, p, n, uzun=0.024, en=0.0055, key=TORON):
    """one toron (a palm beam end sticking out of a mud wall): p on the wall face, n out"""
    p, n = Vector(p), V(n[0], n[1]).normalized()
    cubuk(y, p - n * 0.004, p + n * uzun, en, key, en)


# ---------------------------------------------------------------- the Sahel building block
def sahel_kutu(y, kose, z0, h, key=K, kalin=0.03, dam=None, dam_key='toprak', yanlar=None, payanda_ara=0.13,
               payanda_w=0.03, payanda_d=0.02, payanda_tepe=0.045, kose_w=0.055, kose_tepe=0.075, toron_sira=(0.42, 0.74),
               toron_ara=0.055, ic=True, crest=0.012, ust_key=None, kose_yumurta=False, kose_ust=0.03, payanda_ust=0.022,
               ic_payanda=False, kademe=False, etek=0.022):
    """mud walls round a CCW rectangle-like polygon (right-angled corners), z0..z0 + h, kalin thick, with a rounded
    crest; pilasters every payanda_ara along each side and fat corner buttresses, all rising above the crest into cone
    pinnacles; rows of torons. dam: the z of a flat roof inside (None: an open court, the inner faces go to z0).
    yanlar[i]: per side i (from kose[i] to kose[i+1]) a dict: 'n' (bays between pilasters), 'acik' {bay: spec},
    'payanda' False (no pilasters), 'toron' False. An opening spec: dict tip 'kapi' | 'pencere' | 'gecit' | 'nis',
    en (width as a share of the bay), v0, v1 (sill and head heights above z0), 'kemer' (a low pointed head),
    'derin', 'arka' (key of the back), 'kafes' (a grille), 'ic' (the gecit also cuts the inner face).
    Returns the top z of the walls"""
    m = len(kose)
    yanlar = yanlar or [{}] * m
    z1 = z0 + h
    ic_k = disa(kose, -kalin)
    zi = z0 if dam is None else dam
    tum = []
    for i in range(m):
        a, b = kose[i], kose[(i + 1) % m]
        a = V(a.x, a.y); b = V(b.x, b.y)
        L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
        sp = yanlar[i] if i < len(yanlar) else {}
        if sp.get('yok'): continue
        nb = sp.get('n') or max(1, int(round(L / payanda_ara)))
        bw = L / nb
        acik = sp.get('acik', {})
        holes, ic_holes = [], []
        for bay, s in [(b_, s_) for b_, v_ in acik.items() for s_ in (v_ if isinstance(v_, (list, tuple)) else [v_])]:
            uc = bw * (bay + 0.5)
            en = s.get('en', 0.55) * bw
            u0, u1 = uc - en / 2, uc + en / 2
            v0, v1 = z0 + s.get('v0', 0.0), z0 + s.get('v1', h * 0.6)
            if s.get('kemer'):
                ust = kemer_yolu(u0, u1, v1 - en * s['kemer'], s['kemer'], 8)
            else:
                ust = [(u0, v1), (u1, v1)]
            holes.append((u0, u1, v0, ust))
            tip = s.get('tip', 'kapi')
            if tip == 'gecit':
                delik_yan(y, a, e, nc, u0, u1, v0, ust, kalin, s.get('yan', KK), alt_key=s.get('alt', 'toprak'))
                if s.get('ic', True):
                    ic_holes.append((u0 - kalin, u1 - kalin, v0, [(u - kalin, v) for u, v in ust]))
            else:
                dr = s.get('derin', 0.014 if tip != 'kapi' else 0.016)
                arka = s.get('arka', 'koyu' if tip in ('pencere', 'nis') else 'ahsap_koyu')
                delik_yan(y, a, e, nc, u0, u1, v0, ust, dr, s.get('yan', KK), arka=arka)
                if tip == 'kapi' and s.get('civi', True):
                    # the door's studs and its two leaves' meeting line
                    um = (u0 + u1) / 2; P = lambda u, z: a + e * u - nc * (dr - 0.0015) + Z * z
                    y.yuz_yon([P(um - 0.0015, v0), P(um + 0.0015, v0), P(um + 0.0015, v1 - 0.004), P(um - 0.0015, v1 - 0.004)], 'koyu', nc)
                    for zz in (0.3, 0.62):
                        zc = v0 + (v1 - v0) * zz
                        y.yuz_yon([P(u0 + 0.003, zc), P(u1 - 0.003, zc), P(u1 - 0.003, zc + 0.003), P(u0 + 0.003, zc + 0.003)], 'demir', nc)
                if s.get('kafes'):
                    kafes(y, a + e * u0, a + e * u1, 0, 0, 1, v0, v1 if not s.get('kemer') else v1 - en * s['kemer'], key='ahsap_koyu', nu=3, nv=3,
                          en=0.003, ileri=dr * 0.45)
        delikli(y, a, e, nc, L, z0, z1, holes, key)
        # a darker footing (re-plastered base) along the wall, broken at the ground-level openings
        if etek:
            kes = sorted((h0[0], h0[1]) for h0 in holes if h0[2] <= z0 + 0.002)
            u = 0.0
            for u0, u1 in kes + [(L, L)]:
                if u0 - u > 0.01:
                    silme(y, [a + e * u, a + e * u0], z0, etek, 0.007, KK, 'kaide', kapali=False)
                u = u1
        # the inner face
        if ic:
            ai = V(ic_k[i].x, ic_k[i].y); bi = V(ic_k[(i + 1) % m].x, ic_k[(i + 1) % m].y)
            Li = (bi - ai).length
            delikli(y, ai, e, -nc, Li, zi, z1, ic_holes, key)
        # pilasters (between bays; the corners have their own buttress)
        if sp.get('payanda', True):
            for k in range(1, nb):
                p = a + e * (bw * k)
                payanda(y, p, e, nc, z0, z1 + payanda_ust, payanda_w, payanda_d, key, payanda_tepe, kademe=kademe, arka_z=z1)
                if ic_payanda and dam is None:
                    pi_ = a + e * (bw * k) - nc * kalin
                    payanda(y, pi_, e, -nc, z0, z1 + payanda_ust, payanda_w * 0.8, payanda_d * 0.7, key, 0, arka_z=z1)
        # torons in rows, kept off the holes and pilasters
        if sp.get('toron', True) and toron_sira:
            nt = max(1, int(round(L / toron_ara)))
            for rr in toron_sira:
                zz = z0 + h * rr
                for k in range(nt):
                    u = L * (k + 0.5) / nt
                    if u < kose_w * 0.7 or u > L - kose_w * 0.7: continue
                    if sp.get('payanda', True) and min(abs(u - bw * j) for j in range(nb + 1)) < payanda_w * 0.75: continue
                    if any(h0[0] - 0.012 < u < h0[1] + 0.012 and h0[2] - 0.012 < zz < max(q[1] for q in h0[3]) + 0.012 for h0 in holes): continue
                    toron(y, a + e * u + Z * zz, nc)
        tum.append((a, b, e, nc, L))
    # the crest: a rounded ridge over the wall's thickness
    halkalar = [[V(p.x, p.y, z1) for p in kose],
                [V(p.x, p.y, z1 + crest * 0.75) for p in disa(kose, -kalin * 0.18)],
                [V(p.x, p.y, z1 + crest) for p in disa(kose, -kalin * 0.5)],
                [V(p.x, p.y, z1 + crest * 0.75) for p in disa(kose, -kalin * 0.82)],
                [V(p.x, p.y, z1) for p in ic_k]]
    for i in range(m):
        if (yanlar[i] if i < len(yanlar) else {}).get('yok'): continue
        j = (i + 1) % m
        for r0, r1 in zip(halkalar, halkalar[1:]):
            y.yuz([r0[i], r0[j], r1[j], r1[i]], ust_key or key)
    if dam is not None:
        y.yuz_yon([V(p.x, p.y, dam) for p in ic_k], dam_key, Z)
    # corner buttresses: fat tapering piers centred on the corners, rising highest
    for i in range(m):
        p = kose[i]
        yp = yanlar[i] if i < len(yanlar) else {}
        if yp.get('kose') is False: continue
        kose_payanda(y, (p.x, p.y), z0, z1 + kose_ust, kose_w, key, kose_tepe, yumurta=kose_yumurta)
    return z1


def kose_payanda(y, c, z0, z1, w, key=K, tepe=0.07, yumurta=False, taper=0.8, n=4):
    """a fat square pier centred on c (a building's corner buttress), tapering, crowned with a cone"""
    a0 = [V(c[0] + w / 2 * sx, c[1] + w / 2 * sy, z0) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    a1 = [V(c[0] + w * taper / 2 * sx, c[1] + w * taper / 2 * sy, z1) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    y.serit(a0, a1, key)
    y.yuz_yon(a1, key, Z)
    return tepecik(y, c, w * taper * 0.5, z1 - 0.001, tepe, key, n=8, yumurta=yumurta)


def sahel_minare(y, c, w0, w1, z0, h, key=K, kaburga=3, toron_sira=8, pencereler=((-Y, (0.2, 0.42, 0.62)),), ust=0.06,
                 kose_w=None, egg=True, kapi=None, fener=True):
    """the great tapering minaret of a Sahel mosque (Djinguereber, Sankore): a square pyramid trunk w0 -> w1 wide over
    h, kaburga vertical ribs on each face and fat corner piers leaning with the batter, all rising above the top in
    cone pinnacles, rows of torons between the ribs, small dark openings (pencereler: (face normal, heights as share
    of h)), a crowning lantern with a pinnacle and an ostrich egg; kapi: the face normal of a door at its foot.
    Returns the tip z"""
    cx, cy = c
    z1 = z0 + h
    A = dikdortgen(cx - w0 / 2, cx + w0 / 2, cy - w0 / 2, cy + w0 / 2, z0)
    B = dikdortgen(cx - w1 / 2, cx + w1 / 2, cy - w1 / 2, cy + w1 / 2, z1)
    kw = kose_w or w0 * 0.16
    for i in range(4):
        j = (i + 1) % 4
        e = (A[j] - A[i]); e.z = 0; e.normalize(); nc = V(e.y, -e.x)
        ns = None
        for nrm, hs in pencereler:
            if V(*nrm).dot(nc) > 0.9: ns = hs
        holes = []
        o0 = A[i]
        # the face is a trapezoid: cut the openings as small recesses (a flat quad set in front, then its reveal)
        y.yuz_yon([A[i], A[j], B[j], B[i]], key, nc + Z * ((w0 - w1) / 2 / h))
        tilt = (w0 - w1) / 2 / h
        def F(s, zz, d=0.0):
            t = (zz - z0) / h
            pa, pb = A[i].lerp(A[j], s), B[i].lerp(B[j], s)
            return V(pa.x + (pb.x - pa.x) * t, pa.y + (pb.y - pa.y) * t, zz) + nc * d
        rib_s = [(k + 1) / (kaburga + 1) for k in range(kaburga)]
        sm = 0.5 if kaburga % 2 == 0 else 0.5 + 0.5 / (kaburga + 1)
        for s in rib_s:
            # a rib: a pilaster leaning with the face
            rw0, rw1, d0, d1 = w0 * 0.05, w1 * 0.05, w0 * 0.045, w1 * 0.04
            zt = z1 + ust * 0.55
            p0, p1 = F(s, z0), F(s, zt)
            if kapi is not None and V(*kapi).dot(nc) > 0.9 and 0.33 < s < 0.67:
                # (a rib over the door: it starts above the door frame, its foot closed)
                zr = z0 + h * 0.16 + 0.014
                p0 = F(s, zr)
                q0_ = [p0 - e * rw0, p0 + e * rw0, p0 + e * rw0 + nc * d0, p0 - e * rw0 + nc * d0]
                y.yuz_yon(q0_, key, -Z)
            q0 = [p0 - e * rw0, p0 + e * rw0, p0 + e * rw0 + nc * d0, p0 - e * rw0 + nc * d0]
            q1 = [p1 - e * rw1, p1 + e * rw1, p1 + e * rw1 + nc * d1, p1 - e * rw1 + nc * d1]
            y.yuz_yon([q0[3], q0[2], q1[2], q1[3]], key, nc + Z * tilt)
            y.yuz_yon([q0[2], q0[1], q1[1], q1[2]], key, e)
            y.yuz_yon([q0[0], q0[3], q1[3], q1[0]], key, -e)
            y.yuz_yon(q1, key, Z)
            t1 = (z1 - z0) / (zt - z0); pm = p0.lerp(p1, t1); rw = rw0 + (rw1 - rw0) * t1
            y.yuz_yon([pm + e * rw, pm - e * rw, q1[0], q1[1]], key, -nc)
            cc = (q1[0] + q1[2]) / 2
            tepecik(y, (cc.x, cc.y), min(rw1 * 1.1, d1 * 0.8), zt - 0.001, ust * 0.7, key, n=7)
        if toron_sira:
            cuts = [0.0] + rib_s + [1.0]
            for r in range(toron_sira):
                zz = z0 + h * (0.1 + 0.8 * r / max(1, toron_sira - 1))
                for k in range(len(cuts) - 1):
                    for f in ((0.5,) if k in (0, len(cuts) - 2) else (0.33, 0.67)):
                        s = cuts[k] + (cuts[k + 1] - cuts[k]) * f
                        if k == 0 and s < 0.12: s = 0.14
                        if k == len(cuts) - 2 and s > 0.88: s = 0.86
                        if ns and any(abs(zz - (z0 + h * hh)) < h * 0.06 for hh in ns) and abs(s - sm) < 0.09: continue
                        if kapi is not None and V(*kapi).dot(nc) > 0.9 and 0.3 < s < 0.7 and zz < z0 + h * 0.16 + 0.02: continue
                        toron(y, F(s, zz), nc + Z * tilt, 0.026, 0.006)
        if ns:
            for hh in ns:
                zz = z0 + h * hh
                ww = (w0 + (w1 - w0) * hh) * 0.06
                kk = 0.04 * (1 - 0.3 * hh)
                # a small dark opening between the middle ribs (kaburga odd: beside the middle one) in a frame standing
                # proud of the (uncut) face: the dark pane just in front of the face, the frame's inner reveals and
                # its front ring in front of that, the frame's outer edges closed back into the wall
                pc = F(sm, zz)
                o = [pc - e * ww + Z * 0, pc + e * ww, pc + e * ww + Z * kk, pc - e * ww + Z * kk]
                DP, DF = 0.0012, 0.0055
                mo = (o[0] + o[2]) / 2
                y.yuz_yon([p + nc * DP for p in o], 'koyu', nc)
                for k2 in range(4):
                    p, q = o[k2], o[(k2 + 1) % 4]
                    y.yuz_yon([p + nc * DF, q + nc * DF, q + nc * DP, p + nc * DP], KK, mo - (p + q) / 2)
                fr = [o[0] - e * 0.004 - Z * 0.004, o[1] + e * 0.004 - Z * 0.004, o[2] + e * 0.004 + Z * 0.004, o[3] - e * 0.004 + Z * 0.004]
                for (a_, b_, c_, d_) in ((fr[0], fr[1], o[1], o[0]), (fr[1], fr[2], o[2], o[1]), (fr[2], fr[3], o[3], o[2]), (fr[3], fr[0], o[0], o[3])):
                    y.yuz_yon([a_ + nc * DF, b_ + nc * DF, c_ + nc * DF, d_ + nc * DF], KK, nc)
                    y.yuz_yon([a_ + nc * DF, b_ + nc * DF, b_ - nc * 0.0015, a_ - nc * 0.0015], KK, (a_ + b_) / 2 - mo)
        if kapi is not None and V(*kapi).dot(nc) > 0.9:
            u0, u1 = 0.36, 0.64
            kh = h * 0.16
            pa, pb = F(u0, z0), F(u1, z0)
            # (the face is not cut: the door leaf sits just in front of it, its reveals and frame in front of that)
            q = [pa, pb, pb + Z * kh, pa + Z * kh]
            y.yuz_yon([p + nc * 0.0008 for p in q], 'ahsap_koyu', nc)
            for zz_ in (0.3, 0.65):
                zc = z0 + kh * zz_
                y.yuz_yon([F(u0, zc, 0.0012) + e * 0.002, F(u1, zc, 0.0012) - e * 0.002, F(u1, zc + 0.003, 0.0012) - e * 0.002,
                           F(u0, zc + 0.003, 0.0012) + e * 0.002], 'demir', nc)
            for k2 in range(1, 4):
                p, r_ = q[k2], q[(k2 + 1) % 4]
                y.yuz_yon([p + nc * 0.003, r_ + nc * 0.003, r_ + nc * 0.0008, p + nc * 0.0008], KK, (q[0] + q[2]) / 2 - (p + r_) / 2)
            fr = [pa - e * 0.008, pb + e * 0.008, pb + e * 0.008 + Z * (kh + 0.01), pa - e * 0.008 + Z * (kh + 0.01)]
            for (a_, b_, c_, d_) in ((fr[1], pb, q[2], fr[2]), (fr[0], fr[3], q[3], pa), (q[3], q[2], fr[2], fr[3])):
                y.yuz_yon([a_ + nc * 0.003, b_ + nc * 0.003, c_ + nc * 0.003, d_ + nc * 0.003], KK, nc)
            y.yuz_yon([fr[3] + nc * 0.003, fr[2] + nc * 0.003, fr[2] - nc * 0.004, fr[3] - nc * 0.004], KK, Z)
            for (a_, b_) in ((fr[0], fr[3]), (fr[2], fr[1])):
                y.yuz_yon([a_ + nc * 0.003, b_ + nc * 0.003, b_ - nc * 0.004, a_ - nc * 0.004], KK, (a_ + b_) / 2 - (pa + pb) / 2)
    # corner piers leaning with the batter, crowned higher than the ribs
    for i in range(4):
        c0, c1 = A[i], B[i]
        zt = z1 + ust
        c1 = c1 + (c1 - c0) * ((zt - z1) / h)
        c1.z = zt
        s0 = dikdortgen(c0.x - kw / 2, c0.x + kw / 2, c0.y - kw / 2, c0.y + kw / 2, z0)
        s1 = dikdortgen(c1.x - kw * 0.36, c1.x + kw * 0.36, c1.y - kw * 0.36, c1.y + kw * 0.36, zt)
        y.serit(s0, s1, key)
        y.yuz_yon(s1, key, Z)
        tepecik(y, (c1.x, c1.y), kw * 0.4, zt - 0.001, ust * 1.3, key, n=8, yumurta=egg)
    # the top: a rounded crest, the roof and the lantern
    halkalar = [B, [V(p.x, p.y, z1 + 0.012) for p in disa(B, -0.01)], [V(p.x, p.y, z1 + 0.012) for p in disa(B, -0.02)],
                [V(p.x, p.y, z1 - 0.008) for p in disa(B, -0.03)]]
    for r0, r1 in zip(halkalar, halkalar[1:]):
        y.serit(r0, r1, key)
    y.yuz_yon(halkalar[-1], 'toprak', Z)
    if not fener:   # a terrace for the next stage of a stepped minaret
        return z1 - 0.008
    lw = w1 * 0.36
    lk = dikdortgen(cx - lw / 2, cx + lw / 2, cy - lw / 2, cy + lw / 2)
    zl = z1 - 0.008
    for i in range(4):
        j = (i + 1) % 4
        e = (lk[j] - lk[i]).normalized(); nc = V(e.y, -e.x)
        if nc.dot(V(0, -1, 0)) > 0.9:
            delikli(y, lk[i], e, nc, lw, zl, zl + lw * 0.8, [(lw * 0.3, lw * 0.7, zl, kemer_yolu(lw * 0.3, lw * 0.7, zl + lw * 0.42, 0.4, 6))], key)
            delik_yan(y, lk[i], e, nc, lw * 0.3, lw * 0.7, zl, kemer_yolu(lw * 0.3, lw * 0.7, zl + lw * 0.42, 0.4, 6), 0.012, KK, arka='koyu')
        else:
            duz_duvar(y, lk[i], lk[j], zl, zl + lw * 0.8, key)
    y.yuz_yon([V(p.x, p.y, zl + lw * 0.8) for p in lk], key, Z)
    for p in lk:
        tepecik(y, (cx + (p.x - cx) * 0.9, cy + (p.y - cy) * 0.9), lw * 0.12, zl + lw * 0.8 - 0.001, lw * 0.3, key, n=6)
    zt = tepecik(y, (cx, cy), lw * 0.3, zl + lw * 0.8 - 0.001, lw * 0.9, key, n=10)
    if egg:
        kure(y, (cx, cy, zt + lw * 0.06), lw * 0.1, 'beyaz', n=8, kat=4)
        return zt + lw * 0.16
    return zt


def oluk(y, p, n, z, uzun=0.04, key='ahsap_acik'):
    """a wooden / terracotta roof gutter (gargoyle) sticking out of a wall at p (on the face), n out, under z"""
    p, n = V(p[0], p[1]), V(n[0], n[1]).normalized()
    e = V(-n.y, n.x)
    o = p - n * 0.004 + Z * (z - 0.012)
    a, b = o, o + n * uzun - Z * 0.004
    w = 0.009
    # a U channel: bottom and two sides (both faces), so it reads hollow from above
    for s in (-1, 1):
        q = [a + e * (s * w / 2), b + e * (s * w / 2), b + e * (s * w / 2) + Z * 0.008, a + e * (s * w / 2) + Z * 0.008]
        y.yuz_yon(q, key, e * s)
        y.yuz_yon([pp - e * (s * 0.0015) for pp in q], key, -e * s)
        y.yuz_yon([q[3], q[2], q[2] - e * (s * 0.0015), q[3] - e * (s * 0.0015)], key, Z)
        y.yuz_yon([q[1], q[2], q[2] - e * (s * 0.0015), q[1] - e * (s * 0.0015)], key, n)
    y.yuz_yon([a - e * (w / 2), b - e * (w / 2), b + e * (w / 2), a + e * (w / 2)], key, -Z)
    y.yuz_yon([a - e * (w / 2 - 0.0015) + Z * 0.0015, b - e * (w / 2 - 0.0015) + Z * 0.0015, b + e * (w / 2 - 0.0015) + Z * 0.0015,
               a + e * (w / 2 - 0.0015) + Z * 0.0015], 'koyu', Z)
    y.yuz_yon([b - e * (w / 2), b + e * (w / 2), b + e * (w / 2) + Z * 0.0015, b - e * (w / 2) + Z * 0.0015], key, n)


def fener(y, cx, cy, z, w=0.04, key=K, kapak='ahsap_acik'):
    """a roof skylight of a Sahel mosque: a low mud box with a dark mouth and a lifted lid (a pot / a board)"""
    kutu_merkez(y, (cx, cy), w, w, 0.018, key, z0=z, yuzler='onarkasagsol')
    i = w * 0.36
    o = [V(cx - w / 2, cy - w / 2, z + 0.018), V(cx + w / 2, cy - w / 2, z + 0.018), V(cx + w / 2, cy + w / 2, z + 0.018), V(cx - w / 2, cy + w / 2, z + 0.018)]
    ii = [V(cx - i, cy - i, z + 0.018), V(cx + i, cy - i, z + 0.018), V(cx + i, cy + i, z + 0.018), V(cx - i, cy + i, z + 0.018)]
    for k in range(4):
        y.yuz_yon([o[k], o[(k + 1) % 4], ii[(k + 1) % 4], ii[k]], key, Z)
    y.yuz_yon([p - Z * 0.008 for p in ii], 'koyu', Z)
    for k in range(4):
        p, q = ii[k], ii[(k + 1) % 4]
        y.yuz_yon([p, q, q - Z * 0.008, p - Z * 0.008], KK, V(cx, cy, z) - (p + q) / 2)
    # the lid on four little stubs
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        kutu_merkez(y, (cx + sx * w * 0.36, cy + sy * w * 0.36), 0.006, 0.006, 0.012, key, z0=z + 0.018, yuzler='onarkasagsol')
    kutu_merkez(y, (cx, cy), w * 1.12, w * 1.12, 0.006, kapak, z0=z + 0.03)


# ---------------------------------------------------------------- the Djenne town house
def djenne_ev(y, cx, cy, w, d, h, aci=0.0, kat=2, key=KT, tukolor=True, ust_oda=True, tohum=0, pencere_key='ahsap_koyu', z=0.0):
    """a Djenne town house facing -y (before turning by aci) on the ground z of its centre: a box w x d x h with a
    flat roof and parapet, pilasters and corner buttresses with cone pinnacles, torons; tukolor: the grand facade -
    a door between two fat pilasters rising above the roof, the 'potige' overhang over the door, rows of small
    windows with wooden grilles, five pinnacles in the parapet; ust_oda: a small room on the roof terrace"""
    cz = 0.0
    with parca(y, (cx, cy, z), aci):
        x0, x1, y0, y1 = -w / 2, w / 2, -d / 2, d / 2
        kose = dikdortgen(x0, x1, y0, y1)
        n_on = 5 if tukolor else max(3, int(round(w / 0.1)) | 1)
        bw = w / n_on
        acik = {}
        kh = h * (0.42 if kat >= 2 else 0.62)
        acik[n_on // 2] = dict(tip='kapi', en=0.5, v0=0.0, v1=kh)
        for b in range(n_on):
            if b == n_on // 2: continue
            if kat >= 2:
                acik[b] = [dict(tip='pencere', en=0.36, v0=h * 0.16, v1=h * 0.28, kafes=True),
                           dict(tip='pencere', en=0.4, v0=h * 0.58, v1=h * 0.74, kafes=True)]
            elif b % 2 == 1:
                acik[b] = dict(tip='pencere', en=0.4, v0=h * 0.3, v1=h * 0.48, kafes=True)
        yanlar = [dict(n=n_on, acik=acik, payanda=not tukolor),
                  dict(n=max(1, int(round(d / 0.13))), acik={0: dict(tip='pencere', en=0.4, v0=h * 0.56, v1=h * 0.7, kafes=True)} if kat >= 2 else {}),
                  dict(n=max(1, int(round(w / 0.13)))), dict(n=max(1, int(round(d / 0.13))))]
        sahel_kutu(y, kose, cz, h, key, kalin=0.026, dam=h - 0.03, dam_key='toprak', yanlar=yanlar, payanda_ara=0.13,
                   kose_w=0.04, kose_tepe=0.05, toron_sira=(0.48, 0.8) if kat >= 2 else (0.7,), kose_ust=0.025)
        if kat >= 2:
            # a string course at the floor line
            silme(y, [V(x0 + 0.02, y0), V(x1 - 0.02, y0)], h * 0.47, 0.012, 0.007, key, 'duz', kapali=False)
        if tukolor:
            # the two great pilasters flanking the door, rising above the parapet
            pw = min(0.034, bw * 0.45)
            for s in (-1, 1):
                payanda(y, V(s * bw * 0.5, y0), X, -Y, 0, h + 0.06, pw, 0.028, key, 0.06, arka_z=h)
            # the inner pilasters at the other bay lines (thinner)
            for b in range(1, n_on):
                if b in (n_on // 2, n_on // 2 + 1): continue
                payanda(y, V(x0 + bw * b, y0), X, -Y, 0, h + 0.03, pw * 0.62, 0.016, key, 0.04, arka_z=h)
            # the potige: a projecting box over the door bay, carried on the great pilasters
            pz = kh + 0.03
            kutu_merkez(y, (0, y0 - 0.016), bw * 1.3, 0.036, 0.04, key, z0=pz, yuzler='onsagsolust')
            y.yuz_yon([V(-bw * 0.65, y0 + 0.002, pz), V(bw * 0.65, y0 + 0.002, pz), V(bw * 0.65, y0 - 0.034, pz), V(-bw * 0.65, y0 - 0.034, pz)], KK, -Z)
            for k in range(5):   # the toron ends along its lip
                toron(y, V(-bw * 0.5 + bw * k * 0.25, y0 - 0.034, pz + 0.02), -Y, 0.014, 0.0045)
            # the small pinnacles of the parapet over the potige
            for k in range(3):
                tepecik(y, (-bw * 0.32 + bw * 0.32 * k, y0 - 0.006), 0.009, h + 0.008, 0.035, key, n=6)
        if ust_oda and kat >= 2:
            ow, od = w * 0.42, d * 0.42
            ox, oy = x1 - ow / 2 - 0.035, y1 - od / 2 - 0.035
            k2 = dikdortgen(ox - ow / 2, ox + ow / 2, oy - od / 2, oy + od / 2)
            sahel_kutu(y, k2, h - 0.03, 0.09, key, kalin=0.02, dam=h - 0.03 + 0.075, dam_key='toprak',
                       yanlar=[dict(n=2, acik={0: dict(tip='kapi', en=0.55, v0=0, v1=0.065)}, payanda=False), dict(n=2, payanda=False),
                               dict(n=2, payanda=False), dict(n=2, payanda=False)],
                       kose_w=0.026, kose_tepe=0.03, toron_sira=(0.6,), kose_ust=0.015, crest=0.008)
        # gutters on the sides
        for s in (-1, 1):
            oluk(y, V(s * w / 2, y0 + d * 0.3), V(s, 0), h - 0.02, 0.03)
    return h


# ---------------------------------------------------------------- market shades and goods
def golgelik(y, cx, cy, z, w, d, h, aci=0.0, mal=None, tohum=0, sergi='saz_koyu', ortu=('saz',)):
    """a market shade: forked poles, two beams and a sagging mat of thatch / reeds over a raised stall bed with
    goods. mal: a list of good kinds laid on it (tuz, altin, kola, kumas, kabak, sepet, kup, balik); ortu: keys of the
    cover's strips in turn (a reed mat, or a striped cloth awning)"""
    import random
    rng = random.Random(tohum)
    with parca(y, (cx, cy, z), aci):
        # the stall bed (a low mud bench)
        kutu_merkez(y, (0, 0.0), w * 0.86, d * 0.6, 0.03, KK, yuzler='onarkasagsol')
        kutu_merkez(y, (0, 0.0), w * 0.86, d * 0.6, 0.0, KK, z0=0.03, yuzler='')
        y.yuz_yon([V(-w * 0.43, -d * 0.3, 0.03), V(w * 0.43, -d * 0.3, 0.03), V(w * 0.43, d * 0.3, 0.03), V(-w * 0.43, d * 0.3, 0.03)], sergi, Z)
        # poles
        for sx in (-1, 1):
            for sy in (-1, 1):
                hh = h if sy > 0 else h * 0.92
                p = V(sx * w * 0.46, sy * d * 0.42)
                cubuk(y, p, p + V(sx * 0.004, 0, hh), 0.007, 'ahsap')
                cubuk(y, p + Z * (hh - 0.006), p + V(sx * 0.01, sy * 0.005, hh + 0.004), 0.004, 'ahsap')   # the fork
        for sy in (-1, 1):
            hh = h if sy > 0 else h * 0.92
            cubuk(y, V(-w * 0.52, sy * d * 0.42, hh - 0.008), V(w * 0.52, sy * d * 0.42, hh - 0.008), 0.007, 'ahsap_koyu')
        # the mat: a slightly sagging, ragged sheet with its rim (both faces)
        nx = 4
        top, alt = [], []
        for i in range(nx + 1):
            t = i / nx
            xx = -w * 0.56 + w * 1.12 * t
            sag = 0.005 * math.sin(math.pi * t)
            yo = -d * 0.52 - (0.01 * rng.uniform(-1, 1) if 0 < i < nx else 0)
            top.append((V(xx, yo, h * 0.92 + 0.012 - sag), V(xx, d * 0.54, h + 0.012 - sag)))
        for i in range(nx):
            (a0, a1), (b0, b1) = top[i], top[i + 1]
            q = [a0, b0, b1, a1]
            ok = ortu[i % len(ortu)]
            y.yuz_yon(q, ok, Z)
            y.yuz_yon([p - Z * 0.004 for p in q], 'saz_koyu' if ok == 'saz' else ok, -Z)
            y.yuz_yon([a0, b0, b0 - Z * 0.004, a0 - Z * 0.004], 'saz_koyu', -Y)
            y.yuz_yon([a1, b1, b1 - Z * 0.004, a1 - Z * 0.004], 'saz_koyu', Y)
        for i, s in ((0, -1), (nx, 1)):
            a0, a1 = top[i]
            y.yuz_yon([a0, a1, a1 - Z * 0.004, a0 - Z * 0.004], 'saz_koyu', X * s)
        # the reed fringe (or the cloth's valance) hanging at the front
        fk = ('saz_koyu', 'saz') if ortu[0] == 'saz' else (ortu[-1], ortu[-1])
        for i in range(nx):
            (a0, _), (b0, _) = top[i], top[i + 1]
            y.yuz_yon([a0 - Z * 0.004, b0 - Z * 0.004, b0 - Z * 0.016, a0 - Z * 0.016], fk[0], -Y)
            y.yuz_yon([b0 - Z * 0.004 + Y * 0.0012, a0 - Z * 0.004 + Y * 0.0012, a0 - Z * 0.016 + Y * 0.0012, b0 - Z * 0.016 + Y * 0.0012], fk[1], Y)
            y.yuz_yon([a0 - Z * 0.016, b0 - Z * 0.016, b0 - Z * 0.016 + Y * 0.0012, a0 - Z * 0.016 + Y * 0.0012], fk[0], -Z)
        # goods on the bed
        mal = mal or []
        nm = len(mal)
        for k, tur in enumerate(mal):
            mx = -w * 0.3 + (w * 0.6) * (k / max(1, nm - 1) if nm > 1 else 0.5)
            my = rng.uniform(-d * 0.08, d * 0.08)
            mal_koy(y, tur, mx, my, 0.03, rng)


def mal_koy(y, tur, x, yy, z, rng=None):
    """one heap of goods at (x, yy) on z"""
    if tur == 'tuz':     # salt slabs from Taghaza: long grey-white slabs with dark bands, stacked
        for k in range(3):
            a = 0.08 * (k - 1)
            kutu_merkez(y, (x, yy + 0.004 * k), 0.07, 0.03, 0.009, 'beyaz' if k % 2 == 0 else 'granit_acik', z0=z + 0.0095 * k, aci=a)
            kutu_merkez(y, (x, yy + 0.004 * k), 0.012, 0.0305, 0.0092, 'granit_koyu', z0=z + 0.0095 * k, aci=a)
    elif tur == 'altin':   # a gold dealer's tray: a wooden bowl heaped with gold, rings and a small scale
        donel(y, (x, yy), [(0.0, z), (0.014, z), (0.022, z + 0.008), (0.024, z + 0.011), (0.0, z + 0.011)], 'ahsap', n=10)
        donel(y, (x, yy), [(0.021, z + 0.0105), (0.016, z + 0.016), (0.0, z + 0.019)], 'altin', n=10)
        for s in (-1, 1):
            kure(y, (x + 0.03 * s, yy + 0.012, z + 0.004), 0.004, 'altin', n=6, kat=3)
        cubuk(y, V(x + 0.03, yy - 0.012, z), V(x + 0.03, yy - 0.012, z + 0.03), 0.002, 'bronz')
        cubuk(y, V(x + 0.018, yy - 0.012, z + 0.03), V(x + 0.042, yy - 0.012, z + 0.03), 0.0018, 'bronz')
        for s in (-1, 1):
            donel(y, (x + 0.03 + 0.012 * s, yy - 0.012), [(0.0, z + 0.014), (0.006, z + 0.014), (0.0065, z + 0.016), (0.0, z + 0.016)], 'bronz', n=6)
    elif tur == 'kola':    # baskets of red and white kola nuts
        for s, c in ((-1, 'kiremit'), (1, 'beyaz')):
            sepet(y, x + s * 0.018, yy, z, 0.016, 0.014, dolu=c if c != 'beyaz' else 'kum_acik')
    elif tur == 'kumas':   # folded cloth: indigo-dyed (kept dark), red, ochre, white
        for k, c in enumerate(('kobalt', 'boya_kirmizi', 'boya_sari', 'beyaz', 'lacivert')):
            kutu_merkez(y, (x, yy), 0.05 - k * 0.003, 0.034 - k * 0.002, 0.006, c, z0=z + 0.006 * k, aci=0.05 * (k % 2))
    elif tur == 'kabak':   # calabashes (gourds): some whole, one cut open
        for k, (dx, dy) in enumerate(((-0.014, 0), (0.012, 0.006), (0.0, -0.014))):
            kure(y, (x + dx, yy + dy, z + 0.009), 0.011, 'boya_sari' if k % 2 else 'ahsap_acik', n=8, kat=4)
    elif tur == 'sepet':
        sepet(y, x, yy, z, 0.022, 0.02, dolu='boya_sari')
    elif tur == 'kup':
        kup_(y, x, yy, z, 0.016, 0.04)
    elif tur == 'balik':   # dried fish laid in rows
        for k in range(4):
            cubuk(y, V(x - 0.022, yy - 0.015 + 0.01 * k, z + 0.003), V(x + 0.022, yy - 0.015 + 0.01 * k, z + 0.003), 0.007, 'kum_koyu', 0.004)
    elif tur == 'tahil':   # a heap of millet in a calabash bowl
        donel(y, (x, yy), [(0.0, z), (0.016, z), (0.024, z + 0.01), (0.0, z + 0.01)], 'ahsap_acik', n=10)
        donel(y, (x, yy), [(0.023, z + 0.0095), (0.015, z + 0.02), (0.0, z + 0.026)], 'boya_sari', n=10)


def sepet(y, x, yy, z, r, h, dolu=None, key='saz'):
    """a woven basket (a rim band in a darker straw); dolu: the key of what heaps out of it"""
    donel(y, (x, yy), [(0.0, z), (r * 0.75, z), (r, z + h * 0.7), (r * 1.02, z + h)], key, n=10)
    donel(y, (x, yy), [(r * 1.02, z + h), (r * 1.08, z + h + 0.002)], 'saz_koyu', n=10)
    if dolu:
        donel(y, (x, yy), [(r * 1.08, z + h + 0.002), (r * 0.7, z + h + r * 0.45), (0.0, z + h + r * 0.6)], dolu, n=10)
    else:
        donel(y, (x, yy), [(r * 1.08, z + h + 0.002), (r * 0.95, z + h + 0.0025)], 'saz_koyu', n=10)
        y.yuz_yon([V(x + r * 0.95 * math.cos(TAU * i / 10), yy + r * 0.95 * math.sin(TAU * i / 10), z + h + 0.0025) for i in range(10)], 'koyu', Z)


def kup_(y, x, yy, z, r=0.018, h=0.05, key='kiremit'):
    """a clay water jar with a dark mouth"""
    donel(y, (x, yy), [(0.0, z), (r * 0.6, z), (r, z + h * 0.35), (r * 0.85, z + h * 0.75), (r * 0.45, z + h * 0.9), (r * 0.52, z + h), (r * 0.36, z + h)], key, n=10)
    y.yuz_yon([V(x + r * 0.36 * math.cos(TAU * i / 10), yy + r * 0.36 * math.sin(TAU * i / 10), z + h) for i in range(10)], 'koyu', Z)


def hasir(y, cx, cy, z, w, d, aci=0.0, key='saz', serit='saz_koyu'):
    """a woven mat laid on the ground (goods spread on it): a thin slab with darker stripes"""
    kutu_merkez(y, (cx, cy), w, d, 0.003, key, z0=z, aci=aci)
    ex = V(math.cos(aci), math.sin(aci)); ey = V(-ex.y, ex.x)
    for k in (-0.3, 0.3):
        c = V(cx, cy) + ex * (w * k)
        y.yuz_yon([c - ex * 0.004 - ey * d / 2 + Z * (z + 0.0032), c + ex * 0.004 - ey * d / 2 + Z * (z + 0.0032),
                   c + ex * 0.004 + ey * d / 2 + Z * (z + 0.0032), c - ex * 0.004 + ey * d / 2 + Z * (z + 0.0032)], serit, Z)


# ---------------------------------------------------------------- people
def kisi(y, x, yy, z, aci=0.0, govde='beyaz', bas='beyaz', ten='ahsap_koyu', boy=0.056, yuk=None, mizrak=None,
         kalkan=None, kol=0.0, sarik=True):
    """a person in a wide boubou: robe, sleeves held out a little, a dark face, a turban / head wrap (sarik) or a
    bare head; yuk: a key for a calabash / basket carried on the head; mizrak: a spear's key held upright;
    kalkan: a round hide shield's key on the left arm; kol: raise the right arm (0..1)"""
    s = boy / 0.056
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0, 0.0), (0.0115, 0.0), (0.0122, 0.004), (0.0095, 0.022), (0.0085, 0.036), (0.006, 0.041), (0.0, 0.042)], govde, n=8)
        # the wide sleeves of the boubou
        for sg in (-1, 1):
            boru(y, [V(0.0, sg * 0.007, 0.037), V(0.003, sg * 0.0125, 0.027), V(0.005, sg * 0.013, 0.02)], 0.0035, govde, n=5, r_son=0.0042)
            if not (sg > 0 and kol):
                kure(y, (0.0055, sg * 0.0132, 0.0175), 0.0022, ten, n=5, kat=3)
        if kol:
            boru(y, [V(0.0, 0.007, 0.037), V(0.004, 0.012, 0.037 + 0.016 * kol)], 0.0028, govde, n=5)
            kure(y, (0.0045, 0.0125, 0.039 + 0.017 * kol), 0.0022, ten, n=5, kat=3)
        kure(y, (0.0, 0.0, 0.0475), 0.0056, ten, n=8, kat=4)
        if sarik:
            donel(y, (0, 0.0), [(0.0058, 0.0485), (0.0066, 0.051), (0.0055, 0.0545), (0.0, 0.0555)], bas, n=8)
        if yuk:
            if yuk in ('saz', 'saz_koyu'):
                sepet(y, 0, 0, 0.0545, 0.011, 0.008, dolu='boya_sari')
            else:
                donel(y, (0, 0), [(0.0, 0.0545), (0.007, 0.0545), (0.012, 0.059), (0.0105, 0.064), (0.0, 0.0655)], yuk, n=8)
        if mizrak:
            cubuk(y, V(0.006, -0.014, 0.0), V(0.006, -0.014, 0.085), 0.0022, mizrak)
            donel(y, (0.006, -0.014), [(0.0, 0.085), (0.0028, 0.087), (0.0, 0.098)], 'demir', n=4)
            kure(y, (0.005, -0.0135, 0.0175), 0.0022, ten, n=5, kat=3)
    if kalkan:
        ca, sa = math.cos(aci), math.sin(aci)
        c = V(x, yy, z) + V(ca * 0.006 * s - sa * 0.016 * s, sa * 0.006 * s + ca * 0.016 * s, 0.026 * s)
        n = V(-sa, ca, 0)
        e1 = V(ca, sa, 0)
        rr = 0.012 * s
        pts = [c + n * 0.0008 + (e1 * math.cos(TAU * i / 10) + Z * math.sin(TAU * i / 10)) * rr for i in range(10)]
        y.yuz_yon(pts, kalkan, n)
        y.yuz_yon([p - n * 0.0022 for p in pts], kalkan, -n)
        for i in range(10):
            p, q = pts[i], pts[(i + 1) % 10]
            y.yuz_yon([p, q, q - n * 0.0022, p - n * 0.0022], 'ahsap_koyu', (p + q) / 2 - c)
        kure(y, (c + n * 0.0012).to_tuple(), 0.0028, 'bronz', n=6, kat=3)


def oturan(y, x, yy, z, aci=0.0, govde='beyaz', bas='beyaz', ten='ahsap_koyu', boy=0.056):
    """a trader sitting cross-legged on a mat behind the goods"""
    s = boy / 0.056
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0, 0.0), (0.016, 0.0), (0.0165, 0.004), (0.011, 0.009), (0.0085, 0.024), (0.006, 0.029), (0.0, 0.03)], govde, n=8)
        kure(y, (0.0, 0.0, 0.0355), 0.0056, ten, n=8, kat=4)
        donel(y, (0, 0.0), [(0.0058, 0.0365), (0.0066, 0.039), (0.0055, 0.0425), (0.0, 0.0435)], bas, n=8)
        for sg in (-1, 1):
            boru(y, [V(0.0, sg * 0.007, 0.025), V(0.006, sg * 0.01, 0.016), V(0.011, sg * 0.006, 0.013)], 0.0032, govde, n=5)


# ---------------------------------------------------------------- horses and riders
def mali_at(y, x, yy, z, aci=0.0, renk='ahsap', cul='boya_kirmizi', cul2='boya_sari', poz='dur', binici=None, faz=0.0,
            s=1.0, sorguc='boya_kirmizi', yele=None, bas_egik=0.0):
    """a sturdy Malian war horse (head towards +x before turning by aci, ~0.1 long, withers at the shoulder of a
    0.056 person) in a quilted caparison of two colours (cul, hem cul2) with a red pompom on the poll; poz 'dur'
    (standing) or 'kos' (galloping, faz 0..1 shifts the stride); bas_egik > 0 lowers the head (grazing / drinking);
    binici = (robe key, turban key, spear key or None, shield key or None): a rider"""
    yk = yele or ('koyu' if renk not in ('koyu', 'ahsap_koyu') else 'ahsap_koyu')
    with parca(y, (x, yy, z), aci, s):
        gz = 0.042
        # the barrel, chest and rump
        boru(y, [V(-0.034, 0, gz + 0.001), V(-0.01, 0, gz + 0.003), V(0.014, 0, gz + 0.004), V(0.03, 0, gz + 0.003)], 0.0145, renk, n=8)
        kure(y, (-0.034, 0, gz + 0.002), 0.0148, renk, n=8, kat=4)
        kure(y, (0.031, 0, gz + 0.004), 0.0142, renk, n=8, kat=4)
        # neck and head
        eg = bas_egik
        n0, n1 = V(0.033, 0, gz + 0.008), V(0.05 + eg * 0.012, 0, gz + 0.034 - eg * 0.04)
        boru(y, [n0, n1], 0.0095, renk, n=7, r_son=0.0072)
        h0 = n1 + V(0.0, 0, 0.002)
        h1 = h0 + V(0.022, 0, -0.016 - eg * 0.008)
        boru(y, [h0, h1], 0.0072, renk, n=7, r_son=0.0048)
        kure(y, (h1.x, h1.y, h1.z), 0.0049, renk, n=6, kat=3)
        for sg in (-1, 1):
            boru(y, [h0 + V(-0.002, sg * 0.0035, 0.004), h0 + V(-0.004, sg * 0.004, 0.012)], 0.0018, renk, n=4, r_son=0.0006)
        cubuk(y, n0 + V(-0.004, 0, 0.012), n1 + V(-0.006, 0, 0.006), 0.003, yk, 0.006)    # mane
        kure(y, (h0.x - 0.001, 0, h0.z + 0.009), 0.0042, sorguc, n=6, kat=3)                  # the pompom on the poll
        # tail
        if poz == 'kos':
            boru(y, [V(-0.046, 0, gz + 0.008), V(-0.062, 0, gz + 0.01), V(-0.074, 0, gz + 0.002)], 0.0035, yk, n=5, r_son=0.0015)
        else:
            boru(y, [V(-0.047, 0, gz + 0.006), V(-0.054, 0, gz - 0.008), V(-0.053, 0, gz - 0.028)], 0.0035, yk, n=5, r_son=0.0016)
        # legs: thigh -> knee -> hoof
        f = faz * TAU
        for lx, sy, ph, on in ((0.026, 0.0075, 0.0, True), (0.026, -0.0075, 0.9, True), (-0.03, 0.008, 2.6, False), (-0.03, -0.008, 3.4, False)):
            if poz == 'kos':
                t = math.sin(f + ph)
                if on:
                    knee = V(lx + 0.012 + 0.008 * t, sy, 0.024 + 0.006 * abs(t))
                    hoof = V(lx + 0.016 + 0.018 * t, sy, 0.004 + 0.012 * max(0, t))
                else:
                    knee = V(lx - 0.008 - 0.006 * t, sy, 0.022)
                    hoof = V(lx - 0.012 - 0.02 * t, sy, 0.004 + 0.01 * max(0, -t))
            else:
                knee = V(lx + (0.001 if on else -0.003), sy, 0.02)
                hoof = V(lx + (0.0 if on else -0.001), sy, 0.003)
            top = V(lx, sy * 0.9, gz - 0.004)
            boru(y, [top, knee, hoof], 0.0052 if on else 0.0058, renk, n=5, r_son=0.0034)
            kutu_merkez(y, (hoof.x + 0.001, hoof.y), 0.0075, 0.0065, 0.005, 'koyu', z0=hoof.z - 0.003)
        # the caparison: a rounded quilted cover over the back and down the flanks, a hem band, quilting lines
        x0, x1 = -0.044, 0.034
        prof = [(-0.0168, gz - 0.016), (-0.0168, gz + 0.006), (-0.0118, gz + 0.0158), (0.0, gz + 0.0185), (0.0118, gz + 0.0158), (0.0168, gz + 0.006), (0.0168, gz - 0.016)]
        A = [V(x0, p[0], p[1]) for p in prof]; B = [V(x1, p[0], p[1]) for p in prof]
        for i in range(len(prof) - 1):
            q = [A[i], B[i], B[i + 1], A[i + 1]]
            yuz_dis(y, q, cul, V((x0 + x1) / 2, 0, gz - 0.004))
        for P_, yon in ((A, -X), (B, X)):
            y.yuz_yon(P_, cul, yon)
        y.yuz_yon([A[0], B[0], B[-1], A[-1]], cul, -Z)
        for sg in (-1, 1):
            yy_ = sg * 0.0178
            ii = sg * 0.0168
            q = [V(x0 - 0.001, yy_, gz - 0.0168), V(x1 + 0.001, yy_, gz - 0.0168), V(x1 + 0.001, yy_, gz - 0.009), V(x0 - 0.001, yy_, gz - 0.009)]
            y.yuz_yon(q, cul2, V(0, sg, 0))
            y.yuz_yon([q[3], q[2], V(x1 + 0.001, ii, gz - 0.009), V(x0 - 0.001, ii, gz - 0.009)], cul2, Z)
            y.yuz_yon([q[0], q[1], V(x1 + 0.001, ii, gz - 0.0168), V(x0 - 0.001, ii, gz - 0.0168)], cul2, -Z)
            for xe, yon in ((x0 - 0.001, -X), (x1 + 0.001, X)):
                y.yuz_yon([V(xe, yy_, gz - 0.0168), V(xe, yy_, gz - 0.009), V(xe, ii, gz - 0.009), V(xe, ii, gz - 0.0168)], cul2, yon)
            for k in range(1, 4):
                xx = x0 + (x1 - x0) * k / 4
                y.yuz_yon([V(xx - 0.0007, sg * 0.0172, gz - 0.009), V(xx + 0.0007, sg * 0.0172, gz - 0.009), V(xx + 0.0007, sg * 0.0172, gz + 0.005), V(xx - 0.0007, sg * 0.0172, gz + 0.005)], cul2, V(0, sg, 0))
        # a breast collar with a brass disc
        boru(y, [V(0.034, -0.0125, gz + 0.004), V(0.046, 0, gz - 0.002), V(0.034, 0.0125, gz + 0.004)], 0.0022, cul2, n=4)
        kure(y, (0.047, 0, gz - 0.003), 0.0028, 'bronz', n=6, kat=3)
        if binici is None:
            kutu_merkez(y, (-0.004, 0), 0.018, 0.014, 0.004, 'ahsap_koyu', z0=gz + 0.0175)
            kutu_merkez(y, (-0.0125, 0), 0.003, 0.012, 0.01, 'ahsap_koyu', z0=gz + 0.0175)
        if binici:
            govde, bas_, mz, kk = binici
            bx = -0.004
            bz = gz + 0.019
            kutu_merkez(y, (-0.004, 0), 0.02, 0.016, 0.003, 'ahsap_koyu', z0=gz + 0.0175)
            for sg in (-1, 1):
                boru(y, [V(bx, sg * 0.004, bz + 0.002), V(bx + 0.01, sg * 0.0195, bz - 0.006), V(bx + 0.008, sg * 0.0205, bz - 0.024)], 0.0036, govde, n=5)
                kutu_merkez(y, (bx + 0.011, sg * 0.0208), 0.008, 0.004, 0.004, 'ahsap_koyu', z0=bz - 0.028)
            donel(y, (bx, 0), [(0.0, bz), (0.0085, bz), (0.0088, bz + 0.006), (0.0072, bz + 0.022), (0.0055, bz + 0.028), (0.0, bz + 0.029)], govde, n=8)
            kure(y, (bx + 0.001, 0, bz + 0.034), 0.0054, 'ahsap_koyu', n=8, kat=4)
            donel(y, (bx + 0.001, 0), [(0.0057, bz + 0.035), (0.0068, bz + 0.0375), (0.0058, bz + 0.042), (0.0, bz + 0.044)], bas_, n=8)
            boru(y, [V(bx - 0.004, 0, bz + 0.039), V(bx - 0.01, 0, bz + 0.03)], 0.002, bas_, n=4, r_son=0.001)
            for sg in (-1, 1):
                boru(y, [V(bx, sg * 0.0068, bz + 0.025), V(bx + 0.007, sg * 0.0095, bz + 0.015), V(bx + 0.013, sg * 0.006, bz + 0.012)], 0.0027, govde, n=5)
            if mz:
                cubuk(y, V(bx + 0.013, -0.009, bz - 0.02), V(bx + 0.016, -0.009, bz + 0.07), 0.002, mz)
                donel(y, (bx + 0.016, -0.009), [(0.0, bz + 0.07), (0.0026, bz + 0.072), (0.0, bz + 0.083)], 'demir', n=4)
            if kk:
                c = V(bx + 0.002, 0.0135, bz + 0.016)
                pts = [c + V(math.cos(TAU * i / 10) * 0.009, 0, math.sin(TAU * i / 10) * 0.009) for i in range(10)]
                y.yuz_yon(pts, kk, Y)
                y.yuz_yon([p - Y * 0.002 for p in pts], kk, -Y)
                for i in range(10):
                    p, q = pts[i], pts[(i + 1) % 10]
                    y.yuz_yon([p, q, q - Y * 0.002, p - Y * 0.002], 'ahsap_koyu', (p + q) / 2 - c)
                kure(y, (c + Y * 0.001).to_tuple(), 0.0022, 'bronz', n=6, kat=3)


# ---------------------------------------------------------------- huts and trees
def kulube(y, cx, cy, z, r, h, cati_h, key=K, cati='saz', kapi_aci=-math.pi / 2, n=14, sacak=0.022, tepe=True):
    """a round hut: a mud wall drum with a dark doorway facing kapi_aci, a conical thatched roof overhanging it
    with a ragged eave, ridge rings of tied straw and a finial knot"""
    zt = z + h
    # the drum, the doorway cut into it as a recess with reveals
    rng_ = [V(cx + r * math.cos(TAU * i / n), cy + r * math.sin(TAU * i / n)) for i in range(n)]
    kd = int(round(((kapi_aci % TAU) / TAU) * n - 0.5)) % n
    for i in range(n):
        j = (i + 1) % n
        a, b = rng_[i], rng_[j]
        if i == kd:
            e = (b - a); L = e.length; e.normalize(); nc = V(e.y, -e.x)
            u0, u1 = L * 0.12, L * 0.88
            ust = kemer_yolu(u0, u1, z + h * 0.48, 0.0, 6)
            delikli(y, a, e, nc, L, z, zt, [(u0, u1, z, ust)], key)
            delik_yan(y, a, e, nc, u0, u1, z, ust, 0.012, KK, alt_key=KK, arka='koyu')
        else:
            y.yuz_yon([a + Z * z, b + Z * z, b + Z * zt, a + Z * zt], key, (a + b) / 2 - V(cx, cy))
    # a darker footing band
    y.serit([V(p.x * 1.0 + (p.x - cx) * 0.06, p.y + (p.y - cy) * 0.06, z) for p in rng_],
            [V(p.x + (p.x - cx) * 0.06, p.y + (p.y - cy) * 0.06, z + 0.012) for p in rng_], KK)
    y.serit([V(p.x + (p.x - cx) * 0.06, p.y + (p.y - cy) * 0.06, z + 0.012) for p in rng_], [V(p.x, p.y, z + 0.014) for p in rng_], KK)
    # the roof: eave underside, a slightly concave cone
    R = r + sacak
    pr = [(R, zt - 0.006), (R * 0.72, zt + cati_h * 0.34), (R * 0.38, zt + cati_h * 0.72), (R * 0.1, zt + cati_h * 0.96), (0.0, zt + cati_h)]
    donel(y, (cx, cy), pr, cati, n=n + 2, kat=0.13)
    # (the soffit, seen from below the eave)
    y.serit([V(cx + R * math.cos(0.13 + TAU * i / (n + 2)), cy + R * math.sin(0.13 + TAU * i / (n + 2)), zt - 0.006) for i in range(n + 2)][::-1],
            [V(cx + r * 0.96 * math.cos(0.13 + TAU * i / (n + 2)), cy + r * 0.96 * math.sin(0.13 + TAU * i / (n + 2)), zt) for i in range(n + 2)][::-1], 'saz_koyu')
    # the ragged eave fringe: short drooping strips
    for i in range(n + 2):
        t0 = 0.13 + TAU * i / (n + 2); t1 = 0.13 + TAU * (i + 0.55) / (n + 2)
        p0 = V(cx + R * math.cos(t0), cy + R * math.sin(t0), zt - 0.006)
        p1 = V(cx + R * math.cos(t1), cy + R * math.sin(t1), zt - 0.006)
        q = [p0, p1, p1 - Z * 0.008 + (p1 - V(cx, cy, p1.z)).normalized() * 0.002, p0 - Z * 0.008 + (p0 - V(cx, cy, p0.z)).normalized() * 0.002]
        ince_levha(y, q, 'saz_koyu', (p0 + p1) / 2 - V(cx, cy, p0.z), 0.0015)
    # tied rings on the cone and a finial knot
    for t in (0.55, 0.8):
        rr = R * (1 - t) * 0.98 + 0.002
        zz = zt + cati_h * t * 0.98
        donel(y, (cx, cy), [(rr + 0.001, zz - 0.004), (rr + 0.003, zz), (rr + 0.001, zz + 0.004)], 'saz_koyu', n=n + 2, kat=0.13)
    if tepe:
        boru(y, [V(cx, cy, zt + cati_h - 0.004), V(cx, cy, zt + cati_h + 0.022), V(cx + 0.006, cy, zt + cati_h + 0.032)], 0.004, 'saz_koyu', n=5, r_son=0.0012)
    return zt + cati_h


def baobab(y, x, yy, z, boy=0.3, tohum=0, yaprak='zeytin'):
    """a baobab: a fat bottle trunk, short thick branches spreading like roots and sparse tufts of leaves"""
    import random
    rng = random.Random(tohum)
    g = boy
    donel(y, (x, yy), [(g * 0.2, z), (g * 0.18, z + g * 0.12), (g * 0.165, z + g * 0.35), (g * 0.13, z + g * 0.55), (g * 0.09, z + g * 0.62), (0.0, z + g * 0.64)],
          'kutuk', n=12, kat=rng.uniform(0, 1))
    # root flare
    for k in range(5):
        a = TAU * k / 5 + rng.uniform(-0.3, 0.3)
        d = V(math.cos(a), math.sin(a))
        boru(y, [V(x, yy, z + g * 0.1) + d * g * 0.12, V(x, yy, z + 0.004) + d * g * 0.26], g * 0.04, 'kutuk', n=5, r_son=g * 0.012)
    tepe = V(x, yy, z + g * 0.6)
    def puf(px, py, pz, rr, key):
        # a loose tuft of leaves: a flattened, lumpy cushion (round, not a faceted ball)
        donel(y, (px, py), [(0.0, pz - rr * 0.32), (rr * 0.72, pz - rr * 0.26), (rr, pz), (rr * 0.86, pz + rr * 0.34), (rr * 0.45, pz + rr * 0.6),
                            (0.0, pz + rr * 0.66)], key, n=9, kat=rng.uniform(0, 1))
    for k in range(7):
        a = TAU * k / 7 + rng.uniform(-0.25, 0.25)
        d = V(math.cos(a), math.sin(a))
        L = g * rng.uniform(0.32, 0.46)
        p1 = tepe + d * L * 0.5 + Z * g * rng.uniform(0.12, 0.2)
        p2 = tepe + d * L + Z * g * rng.uniform(0.22, 0.34)
        boru(y, [tepe + d * g * 0.05, p1, p2], g * 0.045, 'kutuk', n=5, r_son=g * 0.014)
        # two twigs off the end
        for s in (-1, 1):
            p3 = p2 + V(-d.y, d.x) * (s * L * 0.25) + d * L * 0.15 + Z * g * 0.06
            boru(y, [p2, p3], g * 0.012, 'kutuk', n=4, r_son=g * 0.005)
            puf(p3.x, p3.y, p3.z + g * 0.008, g * rng.uniform(0.04, 0.052), 'yesil_koyu' if s > 0 and yaprak == 'zeytin' else yaprak)
        puf(p2.x, p2.y, p2.z + g * 0.016, g * rng.uniform(0.055, 0.068), yaprak)


def akasya(y, x, yy, z, boy=0.22, tohum=0, yaprak='zeytin'):
    """an umbrella acacia: a leaning trunk forking into branches under a flat, wide, layered crown"""
    import random
    rng = random.Random(tohum)
    g = boy
    a0 = rng.uniform(0, TAU)
    d = V(math.cos(a0), math.sin(a0))
    tepe = V(x, yy, z) + d * g * 0.08 + Z * g * 0.62
    boru(y, [V(x, yy, z), V(x, yy, z) + d * g * 0.03 + Z * g * 0.35, tepe], g * 0.035, 'kutuk', n=6, r_son=g * 0.022)
    tc = []
    for k in range(3):
        a = a0 + TAU * k / 3 + rng.uniform(-0.3, 0.3)
        dd = V(math.cos(a), math.sin(a))
        p = tepe + dd * g * 0.28 + Z * g * 0.22
        boru(y, [tepe, p], g * 0.018, 'kutuk', n=5, r_son=g * 0.008)
        tc.append(p)
    # the flat crown: a cluster of flattened lumps at the branch ends and over the middle, darker ones between
    c = sum(tc, V(0, 0, 0)) / 3
    def yastik(px, py, pz, rr, hh, key):
        donel(y, (px, py), [(0.0, pz - hh * 0.35), (rr * 0.7, pz - hh * 0.3), (rr, pz), (rr * 0.82, pz + hh * 0.5), (rr * 0.4, pz + hh * 0.75), (0.0, pz + hh * 0.8)],
              key, n=9, kat=rng.uniform(0, 1))
    for p in tc:
        q = p + (p - c) * 0.35
        yastik(q.x, q.y, p.z + g * 0.02, g * rng.uniform(0.2, 0.25), g * 0.1, yaprak)
    yastik(c.x, c.y, c.z + g * 0.05, g * 0.26, g * 0.11, yaprak)
    for k in range(3):
        a = a0 + TAU * (k + 0.5) / 3
        q = c + V(math.cos(a), math.sin(a)) * g * 0.27
        yastik(q.x, q.y, c.z, g * rng.uniform(0.15, 0.19), g * 0.08, 'yesil_koyu' if yaprak == 'zeytin' else yaprak)


def palmiye(y, x, yy, z, boy=0.3, tohum=0):
    """a doum / date palm: a slim curving trunk with ring scars and a crown of drooping fronds"""
    import random
    rng = random.Random(tohum)
    a0 = rng.uniform(0, TAU)
    d = V(math.cos(a0), math.sin(a0))
    pts = [V(x, yy, z) + d * (boy * 0.12 * (t ** 2)) + Z * (boy * t) for t in (0, 0.33, 0.66, 1.0)]
    boru(y, pts, boy * 0.03, 'kutuk', n=6, r_son=boy * 0.022)
    top = pts[-1]
    for k in range(8):
        a = TAU * k / 8 + rng.uniform(-0.2, 0.2)
        dd = V(math.cos(a), math.sin(a))
        L = boy * rng.uniform(0.36, 0.44)
        boru(y, [top, top + dd * L * 0.5 + Z * boy * 0.07, top + dd * L - Z * boy * 0.1], boy * 0.026, 'boya_yesil', n=3, r_son=boy * 0.004)
    kure(y, (top.x, top.y, top.z), boy * 0.035, 'kutuk', n=6, kat=3)


# ---------------------------------------------------------------- pirogues
def pirogue(y, cx, cy, z, aci=0.0, L=0.4, B=0.05, H=0.022, bantlar=('boya_kirmizi', 'boya_sari'), key='ahsap', tente=False,
            yuk=None, kurekci=None, tohum=0):
    """a long Niger pirogue along its local x: a slim hull with upswept pointed ends, painted bands under the
    gunwale, the inside hollow (decked at the ends, with thwarts); tente: an arched reed mat awning; yuk: a list of
    good kinds stowed amidships; kurekci: (robe key, head key) a boatman standing at the stern with a long pole"""
    import random
    rng = random.Random(tohum)
    with parca(y, (cx, cy, z), aci):
        N = 14
        t_ = [i / N for i in range(N + 1)]
        def kesit(t):
            s = math.sin(math.pi * min(max(t, 0.0), 1.0))
            w = B / 2 * max(0.05, s ** 0.55)
            gun = H + H * 1.4 * (abs(2 * t - 1) ** 3.2)
            alt = -H * 0.15 * s ** 0.6 + (H * 0.9 * (abs(2 * t - 1) ** 4))
            xx = -L / 2 + L * t
            # cross-section from the left gunwale down round the keel to the right one
            prof = [(w, gun), (w * 0.98, gun - H * 0.35), (w * 0.86, (gun + alt) / 2 - H * 0.1), (w * 0.5, alt + H * 0.1), (0.0, alt)]
            pts = [V(xx, -p[0], p[1]) for p in prof] + [V(xx, p[0], p[1]) for p in reversed(prof[:-1])]
            return pts, w, gun, alt, xx
        S = [kesit(t) for t in t_]
        cols = [bantlar[0], bantlar[1], key, key, key, key, bantlar[1], bantlar[0]]
        for k in range(N):
            A, B_ = S[k][0], S[k + 1][0]
            mx = (S[k][4] + S[k + 1][4]) / 2
            for i in range(len(A) - 1):
                q = [A[i], B_[i], B_[i + 1], A[i + 1]]
                yuz_dis(y, q, cols[i], V(mx, 0, (S[k][2] + S[k + 1][2]) / 2))
        # end caps (the tips)
        for k, yon in ((0, -X), (N, X)):
            y.yuz_yon(S[k][0], key, yon)
        # the inside: hollow amidships, decked at the ends
        e0, e1 = 3, N - 3
        th = 0.003
        def ic_kesit(k):
            pts, w, gun, alt, xx = S[k]
            return [V(p.x, p.y * (w - th) / max(w, 1e-6), p.z + (th if p.z < gun - 1e-6 else 0)) for p in pts]
        for k in range(e0, e1):
            A, B_ = ic_kesit(k), ic_kesit(k + 1)
            mx = (S[k][4] + S[k + 1][4]) / 2
            for i in range(len(A) - 1):
                q = [A[i], B_[i], B_[i + 1], A[i + 1]]
                y.yuz_yon(q, 'ahsap_koyu' if i in (3, 4) else key, V(mx, 0, S[k][2] + 0.05) - sum(q, V(0, 0, 0)) / 4)
            # the rims (gunwale tops)
            for i in (0, len(A) - 1):
                y.yuz_yon([S[k][0][i], S[k + 1][0][i], B_[i], A[i]], bantlar[0], Z)
        for k in list(range(0, e0)) + list(range(e1, N)):
            P0, P1 = S[k][0], S[k + 1][0]
            y.yuz_yon([P0[0], P1[0], P1[-1], P0[-1]], key, Z)
        for k, yon in ((e0, X), (e1, -X)):
            pts = ic_kesit(k)
            y.yuz_yon(pts, 'ahsap', yon)
        # thwarts
        for k in range(e0 + 2, e1 - 1, 3):
            pts, w, gun, alt, xx = S[k]
            cubuk(y, V(xx, -w + 0.004, gun - 0.006), V(xx, w - 0.004, gun - 0.006), 0.006, 'ahsap_koyu', 0.003)
        mid = S[N // 2]
        if tente:
            R = mid[1] * 0.95; xa, xb = -L * 0.12, L * 0.16
            na = 7
            arc = [(R * math.cos(math.pi * i / na), mid[2] - 0.004 + R * 1.05 * math.sin(math.pi * i / na)) for i in range(na + 1)]
            for i in range(na):
                (y0_, z0_), (y1_, z1_) = arc[i], arc[i + 1]
                q = [V(xa, y0_, z0_), V(xb, y0_, z0_), V(xb, y1_, z1_), V(xa, y1_, z1_)]
                yuz_dis(y, q, 'saz', V(0, 0, mid[2] - 0.004))
                y.yuz_yon([p + (V(0, 0, mid[2] - 0.004) - V(0, p.y, p.z)).normalized() * 0.0025 for p in q], 'saz_koyu',
                          V(0, 0, mid[2] - 0.004) - sum(q, V(0, 0, 0)) / 4)
                for xe, yon in ((xa, -X), (xb, X)):
                    p0, p1 = V(xe, y0_, z0_), V(xe, y1_, z1_)
                    c0 = p0 + (V(xe, 0, mid[2] - 0.004) - p0).normalized() * 0.0025
                    c1 = p1 + (V(xe, 0, mid[2] - 0.004) - p1).normalized() * 0.0025
                    y.yuz_yon([p0, p1, c1, c0], 'saz_koyu', yon)
            for xe in (xa, xb, (xa + xb) / 2):
                boru(y, [V(xe, arc[i][0], arc[i][1] + 0.001) for i in range(na + 1)], 0.0018, 'ahsap_koyu', n=4)
        if yuk:
            for k, tur in enumerate(yuk):
                xx = -L * 0.2 + L * 0.4 * (k / max(1, len(yuk) - 1)) if len(yuk) > 1 else 0.0
                zz = mid[3] + 0.004
                if tur == 'tuz':
                    for j in range(2):
                        kutu_merkez(y, (xx, 0), 0.045, 0.022, 0.007, 'beyaz' if j == 0 else 'granit_acik', z0=zz + 0.007 * j, aci=0.02 * j)
                elif tur == 'cuval':
                    kutu_merkez(y, (xx, 0), 0.04, 0.026, 0.02, 'kumas', z0=zz)
                    kure(y, (xx, 0, zz + 0.02), 0.012, 'kumas', n=6, kat=3)
                elif tur == 'kup':
                    kup_(y, xx, 0, zz, 0.011, 0.03)
                elif tur == 'kabak':
                    kure(y, (xx, 0, zz + 0.01), 0.011, 'boya_sari', n=8, kat=4)
        if kurekci:
            g, b_ = kurekci
            px = L * 0.34
            pts, w, gun, alt, xx = S[int(N * 0.84)]
            kisi(y, px, 0, alt + 0.004, math.pi, g, b_)
            cubuk(y, V(px - 0.006, -0.012, alt + 0.14), V(px + 0.03, -0.02, alt - 0.03), 0.0028, 'ahsap_acik')


# ---------------------------------------------------------------- stables
def sundurma(y, a, b, z_ust, z_on, derin, n_direk=4, key='saz', kalin=0.006):
    """a lean-to shed against a wall: a->b on the wall's face (the shed lies to the RIGHT of a->b), its thatched
    roof sloping from z_ust at the wall down to z_on derin out, on forked posts with a beam; the eave ragged"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    sac = 0.02
    A0, B0 = a + Z * z_ust, b + Z * z_ust
    A1, B1 = a + nc * (derin + sac) + Z * (z_on - sac * (z_ust - z_on) / derin), b + nc * (derin + sac) + Z * (z_on - sac * (z_ust - z_on) / derin)
    nseg = max(1, int(round(L / 0.15)))
    up = (Z * derin + nc * (z_ust - z_on)).normalized()
    for k in range(nseg):
        t0, t1 = k / nseg, (k + 1) / nseg
        q = [A0.lerp(B0, t0), A1.lerp(B1, t0), A1.lerp(B1, t1), A0.lerp(B0, t1)]
        y.yuz_yon(q, key if k % 2 == 0 else ('saz_koyu' if key == 'saz' else key), up)
        y.yuz_yon([p - Z * kalin for p in q], 'saz_koyu', -up)
    # the tie battens holding the thatch down: one down the slope at each strip joint, two along it
    for k in range(nseg + 1):
        t = min(max(k / nseg, 0.012), 0.988)
        cubuk(y, A0.lerp(B0, t) + up * 0.002 + nc * 0.01, A1.lerp(B1, t) + up * 0.002 - nc * 0.004, 0.004, 'ahsap_koyu', 0.003)
    for f in (0.35, 0.75):
        cubuk(y, A0.lerp(A1, f) + up * 0.002 + e * 0.006, B0.lerp(B1, f) + up * 0.002 - e * 0.006, 0.0035, 'ahsap_koyu', 0.003)
    # the eave and the end edges
    y.yuz_yon([A1, B1, B1 - Z * kalin, A1 - Z * kalin], 'saz_koyu', nc)
    for P0, P1, s in ((A0, A1, -e), (B0, B1, e)):
        y.yuz_yon([P0, P1, P1 - Z * kalin, P0 - Z * kalin], 'saz_koyu', s)
    # the ragged fringe under the eave (two-sided, with a hair of thickness)
    for k in range(nseg * 2):
        t0, t1 = k / (nseg * 2), (k + 0.8) / (nseg * 2)
        p0, p1 = A1.lerp(B1, t0) - Z * kalin, A1.lerp(B1, t1) - Z * kalin
        dz = 0.012 + 0.006 * ((k * 7) % 3) / 2
        ince_levha(y, [p0, p1, p1 - Z * dz, p0 - Z * dz], 'saz_koyu', nc, 0.0015, arka_key='saz')
    # posts and the beam under the eave
    zb = z_on - kalin - 0.006
    for k in range(n_direk + 1):
        p = a.lerp(b, (k + 0.02) / (n_direk + 0.04)) + nc * derin
        z0 = 0.0
        cubuk(y, V(p.x, p.y, ZEMIN_Z[0]), V(p.x, p.y, zb), 0.008, 'ahsap')
    cubuk(y, a + nc * derin + Z * (zb - 0.004), b + nc * derin + Z * (zb - 0.004), 0.008, 'ahsap_koyu')


ZEMIN_Z = [0.0]   # the ground z for sundurma's posts (a script sets ZEMIN_Z[0])


def yalak(y, a, b, z, en=0.04, h=0.025, su=True, key='ahsap', ic='su'):
    """a trough a->b (a hollowed log / wooden box) with water or fodder in it"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L
    c = (a + b) / 2
    aci = math.atan2(e.y, e.x)
    kutu_merkez(y, (c.x, c.y), L, en, h, key, z0=z, aci=aci, yuzler='onarkasagsol')
    t = 0.005
    ex, ey = e, V(-e.y, e.x)
    o = [c - ex * (L / 2) - ey * (en / 2), c + ex * (L / 2) - ey * (en / 2), c + ex * (L / 2) + ey * (en / 2), c - ex * (L / 2) + ey * (en / 2)]
    i_ = [c - ex * (L / 2 - t) - ey * (en / 2 - t), c + ex * (L / 2 - t) - ey * (en / 2 - t), c + ex * (L / 2 - t) + ey * (en / 2 - t), c - ex * (L / 2 - t) + ey * (en / 2 - t)]
    for k in range(4):
        y.yuz_yon([o[k] + Z * (z + h), o[(k + 1) % 4] + Z * (z + h), i_[(k + 1) % 4] + Z * (z + h), i_[k] + Z * (z + h)], key, Z)
        p, q = i_[k], i_[(k + 1) % 4]
        y.yuz_yon([p + Z * (z + h), q + Z * (z + h), q + Z * (z + h * 0.45), p + Z * (z + h * 0.45)], 'ahsap_koyu', c - (p + q) / 2)
    y.yuz_yon([p + Z * (z + h * 0.45) for p in i_], ic, Z)


def saman(y, x, yy, z, r=0.06, h=0.07, key='saz'):
    """a hay / fodder stack: a rounded heap with a darker crown"""
    donel(y, (x, yy), [(r, z), (r * 1.02, z + h * 0.3), (r * 0.85, z + h * 0.65), (r * 0.45, z + h * 0.92), (0.0, z + h)], key, n=12)
    donel(y, (x, yy), [(r * 0.5, z + h * 0.9), (r * 0.52, z + h * 0.93), (0.0, z + h * 1.04)], 'saz_koyu', n=12)


# ---------------------------------------------------------------- fortification, regalia
def burc(y, c, r, z0, h, key=K, egim=0.14, n=16, dis_aci=None, tepe_n=8, yumurta=True):
    """a round Sahel bastion: a battered mud drum (top radius r(1 - egim)) with ribs, rows of torons and slits, a
    crest of cone pinnacles round a parapet and a flat top. dis_aci: the angle the slits face (None: all round).
    Returns the top z"""
    cx, cy = c
    r1 = r * (1 - egim)
    zt = z0 + h
    donel(y, c, [(r, z0), (r1, zt)], key, n=n)
    # the parapet: a ring wall with its inner face and the flat floor
    donel(y, c, [(r1, zt), (r1 * 1.02, zt + 0.006), (r1 * 1.0, zt + 0.032), (r1 * 0.92, zt + 0.038), (r1 * 0.82, zt + 0.032),
                 (r1 * 0.82, zt + 0.008), (0.0, zt + 0.008)], key, n=n)
    for i in range(tepe_n):
        t = TAU * (i + 0.5) / tepe_n
        tepecik(y, (cx + r1 * 0.91 * math.cos(t), cy + r1 * 0.91 * math.sin(t)), min(0.014, r1 * 0.12), zt + 0.036, 0.04, key, n=6)
    # ribs (half-round pilasters) leaning with the batter
    for i in range(8):
        t = TAU * i / 8
        d = V(math.cos(t), math.sin(t))
        boru(y, [V(cx, cy, z0) + d * (r - 0.004), V(cx, cy, zt + 0.02) + d * (r1 - 0.003)], 0.011, key, n=5, r_son=0.008)
    for k in range(3):
        zz = z0 + h * (0.3 + 0.27 * k)
        rr = r + (r1 - r) * (zz - z0) / h
        for i in range(12):
            t = TAU * (i + 0.5) / 12 + 0.1 * k
            d = V(math.cos(t), math.sin(t))
            toron(y, V(cx, cy, zz) + d * (rr - 0.003), d, 0.022)
    for i in range(8):
        t = TAU * (i + 0.5) / 8
        if dis_aci is not None and math.cos(t - dis_aci) < 0.2: continue
        d = V(math.cos(t), math.sin(t))
        zz = z0 + h * 0.72
        rr = r + (r1 - r) * 0.72
        yarik(y, V(cx, cy, 0) + d * rr, V(-d.y, d.x), d, -0.005, zz, 0.01, 0.03)
    return zt + 0.038


def semsiye(y, x, yy, z, boy=0.16, r=0.07, key='boya_kirmizi', sacak_key='altin', kus=True):
    """the Mansa's state parasol: a tall pole, a domed silk canopy with a gold fringe and a golden bird on top"""
    cubuk(y, V(x, yy, z), V(x, yy, z + boy + 0.02), 0.005, 'ahsap_koyu')
    zt = z + boy
    donel(y, (x, yy), [(r, zt), (r * 0.85, zt + r * 0.3), (r * 0.5, zt + r * 0.5), (0.0, zt + r * 0.56)], key, n=14)
    y.yuz_yon([V(x + r * math.cos(TAU * i / 14), yy + r * math.sin(TAU * i / 14), zt) for i in range(14)], key, -Z)
    # the fringe: a short gold band hanging from the rim
    for i in range(14):
        t0, t1 = TAU * i / 14, TAU * (i + 1) / 14
        a, b = V(x + r * math.cos(t0), yy + r * math.sin(t0), zt), V(x + r * math.cos(t1), yy + r * math.sin(t1), zt)
        iki_yuzlu(y, [a, b, b - Z * 0.012, a - Z * 0.012], sacak_key, (a + b) / 2 - V(x, yy, zt), 0.0008)
    if kus:
        bz = zt + r * 0.56
        kure(y, (x, yy, bz + 0.008), 0.007, 'altin', n=7, kat=4)
        kure(y, (x + 0.007, yy, bz + 0.014), 0.0042, 'altin', n=6, kat=3)
        boru(y, [V(x + 0.01, yy, bz + 0.014), V(x + 0.016, yy, bz + 0.012)], 0.0016, 'altin', n=4, r_son=0.0004)
        for s in (-1, 1):
            iki_yuzlu(y, [V(x - 0.002, yy + s * 0.004, bz + 0.012), V(x + 0.004, yy + s * 0.004, bz + 0.012), V(x - 0.008, yy + s * 0.02, bz + 0.024)], 'altin', Z, 0.0008)
        boru(y, [V(x - 0.006, yy, bz + 0.008), V(x - 0.016, yy, bz + 0.012)], 0.0028, 'altin', n=4, r_son=0.001)


# ================================================================ extra helpers (lm_sankore, lm_altinmadeni, lm_mansasaray, lm_timbuktukale)
def kademeli_minare(y, c, katlar, z0, key=K, kaburga=(3, 2, 1), toron_sira=(5, 4, 3), pencere=-Y, egg=True, kapi=None):
    """the stepped pyramid minaret of the Sankore: stages katlar = [(w0, w1, h), ...] each a battered trunk with ribs
    and corner piers rising into pinnacles, set back on the terrace of the one below; the last one carries the
    crowning lantern. Returns (tip z, [terrace z of each stage])"""
    z = z0
    teras = []
    for i, (w0, w1, h) in enumerate(katlar):
        son = i == len(katlar) - 1
        kb = kaburga[min(i, len(kaburga) - 1)]
        ts = toron_sira[min(i, len(toron_sira) - 1)]
        pn = ((pencere, (0.3, 0.62) if not son else (0.45,)),) if pencere is not None else ()
        z = sahel_minare(y, c, w0, w1, z, h, key, kaburga=kb, toron_sira=ts, pencereler=pn, ust=0.05 if not son else 0.06,
                         kose_w=w0 * 0.15, egg=egg, kapi=kapi if i == 0 else None, fener=son)
        teras.append(z)
    return z, teras


def el_yazmasi(y, x, yy, z, aci=0.0, n=3, tohum=0):
    """a stack of Timbuktu manuscripts: loose leaves between leather covers, the stack slightly askew"""
    import random
    g = random.Random(tohum)
    zz = z
    for k in range(n):
        a = aci + g.uniform(-0.25, 0.25)
        w, d = g.uniform(0.022, 0.03), g.uniform(0.016, 0.02)
        kutu_merkez(y, (x, yy), w, d, 0.0016, 'ahsap_koyu', z0=zz, aci=a)
        kutu_merkez(y, (x, yy), w * 0.94, d * 0.92, 0.004, 'kum_acik', z0=zz + 0.0016, aci=a, yuzler='onarkasagsol')
        kutu_merkez(y, (x, yy), w, d, 0.0016, g.choice(('ahsap_koyu', 'boya_kirmizi', 'ahsap')), z0=zz + 0.0056, aci=a)
        zz += 0.0072
    return zz


def levha(y, x, yy, z, aci=0.0, egim=1.1, boy=0.032):
    """a Koranic writing board (allo): a pale wooden paddle with a handle, its foot at (x, yy, z), leaning back at egim
    (rad from flat), dark ink lines on its front. aci: the direction its face looks"""
    e = V(math.cos(aci + math.pi / 2), math.sin(aci + math.pi / 2))   # across the board
    f = V(math.cos(aci), math.sin(aci))                               # the way the face looks (horizontal part)
    up = (Z * math.sin(egim) - f * math.cos(egim))                    # up the board
    nrm = (f * math.sin(egim) + Z * math.cos(egim)).normalized()
    o = V(x, yy, z)
    w = boy * 0.6
    pts = [o - e * (w / 2), o + e * (w / 2), o + e * (w / 2) + up * boy, o + e * (w * 0.36) + up * (boy * 1.12), o - e * (w * 0.36) + up * (boy * 1.12),
           o - e * (w / 2) + up * boy]
    ince_levha(y, pts, 'ahsap_acik', nrm, 0.0018)
    cubuk(y, o + up * (boy * 1.1), o + up * (boy * 1.32), 0.0035, 'ahsap_acik', 0.0018)
    for k in range(4):
        t = 0.2 + 0.18 * k
        p = o + up * (boy * t) + nrm * 0.0004
        y.yuz_yon([p - e * (w * 0.36), p + e * (w * 0.36), p + e * (w * 0.36) + up * 0.0025, p - e * (w * 0.36) + up * 0.0025], 'koyu', nrm)


def kuyu(y, x, yy, z, r=0.04, key=K, cikrik_=True, su_key='su'):
    """a well: a round mud curb with water in its mouth, a frame with a pulley and a rope with a bucket"""
    n = 14
    donel(y, (x, yy), [(r, z), (r * 1.02, z + 0.028), (r * 0.96, z + 0.034), (r * 0.74, z + 0.034), (r * 0.72, z + 0.02)], key, n=n)
    y.yuz_yon([V(x + r * 0.72 * math.cos(TAU * i / n), yy + r * 0.72 * math.sin(TAU * i / n), z + 0.02) for i in range(n)], su_key, Z)
    if cikrik_:
        for s in (-1, 1):
            cubuk(y, V(x + s * r * 0.9, yy, z + 0.03), V(x + s * r * 0.9, yy, z + 0.11), 0.007, 'ahsap')
        cubuk(y, V(x - r * 1.0, yy, z + 0.107), V(x + r * 1.0, yy, z + 0.107), 0.006, 'ahsap_koyu')
        donel(y, (x, yy), [(0.0, z + 0.094), (0.01, z + 0.094), (0.01, z + 0.116), (0.0, z + 0.116)], 'ahsap_koyu', n=8)
        cubuk(y, V(x, yy, z + 0.094), V(x, yy, z + 0.05), 0.0018, 'saz_koyu')
        donel(y, (x, yy), [(0.0, z + 0.036), (0.008, z + 0.036), (0.01, z + 0.05), (0.0, z + 0.05)], 'ahsap', n=8)


def cikrik(y, x, yy, z, aci=0.0, r=0.045, derin=0.05, kova=True, key='ahsap'):
    """a mine shaft: a round dark pit edged with a ring of heaped earth and logs, a windlass on two forked posts
    across it (a crank handle), its rope down into the shaft with a leather bucket. Returns the windlass top z"""
    n = 12
    with parca(y, (x, yy, z), aci):
        # the earth rim
        donel(y, (0, 0), [(r * 1.65, 0.0), (r * 1.35, 0.016), (r * 1.08, 0.02), (r, 0.012)], 'toprak', n=n)
        # the pit's wall seen from inside (wound inward) and its dark bottom
        for i in range(n):
            j = (i + 1) % n
            a0, a1 = TAU * i / n, TAU * j / n
            for (za, zb, ra, rb, kk) in ((0.012, -0.012, 1.0, 0.985, 'kerpic_koyu'), (-0.012, -derin, 0.985, 0.95, 'koyu')):
                q = [V(r * ra * math.cos(a0), r * ra * math.sin(a0), za), V(r * rb * math.cos(a0), r * rb * math.sin(a0), zb),
                     V(r * rb * math.cos(a1), r * rb * math.sin(a1), zb), V(r * ra * math.cos(a1), r * ra * math.sin(a1), za)]
                mid = (q[0] + q[3]) / 2
                y.yuz_yon(q, kk, V(-mid.x, -mid.y, 0))
        y.yuz_yon([V(r * 0.95 * math.cos(TAU * i / n), r * 0.95 * math.sin(TAU * i / n), -derin) for i in range(n)], 'koyu', Z)
        # the log curb
        for k in range(4):
            a = TAU * k / 4 + 0.4
            d = V(math.cos(a), math.sin(a)); s = V(-d.y, d.x)
            p = d * (r * 1.12) + Z * 0.02
            cubuk(y, p - s * r * 0.9, p + s * r * 0.9, 0.009, 'kutuk', 0.009)
        # the windlass on forked posts
        for sg in (-1, 1):
            p = V(sg * r * 1.25, 0)
            cubuk(y, p, p + Z * 0.085, 0.008, key)
            cubuk(y, p + Z * 0.08, p + V(0, 0.008, 0.096), 0.004, key)
            cubuk(y, p + Z * 0.08, p + V(0, -0.008, 0.096), 0.004, key)
        boru(y, [V(-r * 1.4, 0, 0.088), V(r * 1.4, 0, 0.088)], 0.0055, 'ahsap_koyu', n=6)
        cubuk(y, V(r * 1.4, 0, 0.088), V(r * 1.4 + 0.004, 0, 0.066), 0.004, 'ahsap')
        cubuk(y, V(r * 1.4 + 0.004, 0, 0.066), V(r * 1.4 + 0.016, 0, 0.066), 0.004, 'ahsap')
        boru(y, [V(-0.014, 0, 0.088), V(0.014, 0, 0.088)], 0.009, 'saz_koyu', n=6)
        cubuk(y, V(0, -0.009, 0.086), V(0, -0.009, 0.03), 0.0022, 'saz_koyu')
        if kova:
            donel(y, (0, -0.009), [(0.0, 0.014), (0.008, 0.014), (0.011, 0.028), (0.0105, 0.03), (0.0, 0.03)], 'ahsap_koyu', n=8)
    return z + 0.096


def yigin(y, x, yy, z, r=0.08, h=0.06, key='toprak', tohum=0, n=12, uzun=1.0, aci=0.0):
    """a lumpy heap of spoil earth / gravel (uzun > 1 stretches it along aci)"""
    import random
    g = random.Random(tohum)
    ca, sa = math.cos(aci), math.sin(aci)
    kats = [(1.0, 0.0), (0.9, 0.28), (0.7, 0.58), (0.4, 0.84)]
    rings = []
    for fr, fz in kats:
        ring = []
        for i in range(n):
            t = TAU * i / n
            jj = 1 + g.uniform(-0.13, 0.13) if fz > 0 else 1 + g.uniform(-0.06, 0.06)
            lx, ly = math.cos(t) * r * fr * jj * uzun, math.sin(t) * r * fr * jj
            ring.append(V(x + lx * ca - ly * sa, yy + lx * sa + ly * ca, z + h * fz))
        rings.append(ring)
    tepe = V(x, yy, z + h)
    for k in range(len(rings) - 1):
        for i in range(n):
            jn = (i + 1) % n
            q = [rings[k][i], rings[k][jn], rings[k + 1][jn], rings[k + 1][i]]
            y.yuz_yon(q, key, ((q[0] + q[1]) / 2 - V(x, yy, z - h)))
    for i in range(n):
        jn = (i + 1) % n
        q = [rings[-1][i], rings[-1][jn], tepe]
        y.yuz_yon(q, key, ((q[0] + q[1]) / 2 - V(x, yy, z - h)))


def terazi(y, x, yy, z, aci=0.0, boy=0.05, key='bronz'):
    """a balance for weighing gold dust: an upright, a beam and two hanging pans"""
    with parca(y, (x, yy, z), aci):
        kutu_merkez(y, (0, 0), 0.014, 0.014, 0.004, 'ahsap_koyu')
        cubuk(y, V(0, 0, 0.004), V(0, 0, boy), 0.0024, key)
        cubuk(y, V(-boy * 0.42, 0, boy - 0.002), V(boy * 0.42, 0, boy - 0.002), 0.002, key)
        for s in (-1, 1):
            px = s * boy * 0.4
            for d in (-1, 1):
                cubuk(y, V(px, 0, boy - 0.002), V(px + d * 0.007, 0, boy * 0.44), 0.001, key)
            donel(y, (px, 0), [(0.0, boy * 0.4), (0.0095, boy * 0.42), (0.0105, boy * 0.445), (0.0, boy * 0.44)], key, n=8)


def tuz_levha(y, x, yy, z, aci=0.0, n=4, tohum=0):
    """a stack of Taghaza rock-salt slabs (long, grey-white, dark bands where they were tied / marked)"""
    import random
    g = random.Random(tohum)
    for k in range(n):
        a = aci + g.uniform(-0.12, 0.12)
        zz = z + k * 0.0115
        ca, sa = math.cos(a), math.sin(a)
        kutu_merkez(y, (x, yy), 0.085, 0.034, 0.011, 'beyaz' if k % 2 == 0 else 'granit_acik', z0=zz, aci=a)
        for t in (-0.25, 0.25):
            kutu_merkez(y, (x + ca * 0.085 * t, yy + sa * 0.085 * t), 0.006, 0.0352, 0.0112, 'granit_koyu', z0=zz - 0.0001, aci=a)


def tuareg(y, x, yy, z, aci=0.0, mizrak='ahsap_koyu', kalkan='ahsap', boy=0.058):
    """a Tuareg guard: indigo robe and veil (tagelmust), a spear and a hide shield"""
    kisi(y, x, yy, z, aci, govde='lacivert', bas='lacivert', ten='ahsap_koyu', boy=boy, mizrak=mizrak, kalkan=kalkan)
    s = boy / 0.056
    donel(y, (x, yy), [(0.0059 * s, z + 0.0425 * s), (0.0063 * s, z + 0.0455 * s), (0.0058 * s, z + 0.0478 * s)], 'lacivert', n=8)
