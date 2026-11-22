# Forum Romanum style forum (lm_forum): a paved square closed by porticoes - a double colonnade along the front split
# by a triumphal arch (S.P.Q.R. attic, quadriga), a portico with shops (tabernae) on the left - with a hexastyle
# Corinthian temple on a high podium at its head (stairs, altar, sculpted pediment), a two-storey arcaded basilica
# with a clerestoried nave along the right, the brick Curia behind it, the Rostra with bronze ship prows, an
# equestrian statue and an honorific column in the square.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04


# ---------------------------------------------------------------- helpers (Roman)
def seg_quad(o, ex, n, p, q, w, key):
    """a flat stroke from p to q (2D, in the plane o + ex u + z v), w wide, facing n"""
    p, q = V(*p), V(*q)
    d = (q - p); L = d.length
    if L < 1e-9: return
    d /= L; s = V(-d.y, d.x) * (w / 2)
    P = lambda t: o + ex * t.x + Z * t.y + n * 0.0015
    y.yuz_yon([P(p - s - d * w * 0.3), P(q - s + d * w * 0.3), P(q + s + d * w * 0.3), P(p + s - d * w * 0.3)], key, n)


GLIF = {
    'S': [((0.6, 1), (0, 1)), ((0, 1), (0, 0.5)), ((0, 0.5), (0.6, 0.5)), ((0.6, 0.5), (0.6, 0)), ((0.6, 0), (0, 0))],
    'P': [((0, 0), (0, 1)), ((0, 1), (0.55, 1)), ((0.55, 1), (0.55, 0.5)), ((0.55, 0.5), (0, 0.5))],
    'Q': [((0, 0), (0, 1)), ((0, 1), (0.6, 1)), ((0.6, 1), (0.6, 0)), ((0.6, 0), (0, 0)), ((0.35, 0.25), (0.72, -0.12))],
    'R': [((0, 0), (0, 1)), ((0, 1), (0.55, 1)), ((0.55, 1), (0.55, 0.5)), ((0.55, 0.5), (0, 0.5)), ((0.2, 0.5), (0.6, 0))],
    'V': [((0, 1), (0.3, 0)), ((0.3, 0), (0.6, 1))],
    'L': [((0, 1), (0, 0)), ((0, 0), (0.55, 0))],
    'C': [((0.6, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (0.6, 0))],
    'I': [((0.15, 0), (0.15, 1))],
    'A': [((0, 0), (0.3, 1)), ((0.3, 1), (0.6, 0)), ((0.13, 0.38), (0.47, 0.38))],
    'E': [((0.6, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (0.6, 0)), ((0, 0.5), (0.45, 0.5))],
    'D': [((0, 0), (0, 1)), ((0, 1), (0.4, 1)), ((0.4, 1), (0.6, 0.7)), ((0.6, 0.7), (0.6, 0.3)), ((0.6, 0.3), (0.4, 0)), ((0.4, 0), (0, 0))],
    'T': [((0, 1), (0.6, 1)), ((0.3, 1), (0.3, 0))],
    'O': [((0, 0), (0, 1)), ((0, 1), (0.6, 1)), ((0.6, 1), (0.6, 0)), ((0.6, 0), (0, 0))],
    'M': [((0, 0), (0, 1)), ((0, 1), (0.3, 0.35)), ((0.3, 0.35), (0.6, 1)), ((0.6, 1), (0.6, 0))],
    'N': [((0, 0), (0, 1)), ((0, 1), (0.6, 0)), ((0.6, 0), (0.6, 1))],
    'G': [((0.6, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (0.6, 0)), ((0.6, 0), (0.6, 0.45)), ((0.6, 0.45), (0.32, 0.45))],
    '.': [((0.12, 0.42), (0.12, 0.58))],
}


def yazi(o, ex, n, metin, h, key='bronz'):
    """bronze capital letters (simple stroke font) centred on o along ex, h high"""
    gen = lambda ch: 0.3 if ch in '.I' else 0.6
    bos = 0.32
    W = (sum(gen(c) + bos for c in metin if c != ' ') + 0.5 * metin.count(' ') - bos) * h
    u = -W / 2
    for ch in metin:
        if ch == ' ':
            u += 0.5 * h; continue
        for p, q in GLIF[ch]:
            seg_quad(o, ex, n, (u + p[0] * h, p[1] * h), (u + q[0] * h, q[1] * h), h * 0.15, key)
        u += (gen(ch) + bos) * h


def kemer_cizgi(x0, x1, hs, k=10):
    R = (x1 - x0) / 2
    return [(x0, hs)] + [(x0 + R + R * math.cos(math.pi - math.pi * i / k), hs + R * math.sin(math.pi - math.pi * i / k)) for i in range(1, k)] + [(x1, hs)]


def gecit(a, b, z0, H, derin, en=0.5, ust=0.05, key='mermer', ic_key='kirec', alt=True):
    """a wall a->b (facing the right of a->b), derin thick, pierced by a round-arched passage you can see through: the
    front and back faces round the arch, the reveal (jambs and the vault's underside). Returns (L, x0, x1, hs)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v, d=0.0: a + e * u - nc * d + Z * (z0 + v)
    x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
    hs = H - ust - (x1 - x0) / 2
    tp = kemer_cizgi(x0, x1, hs, 14)
    for d, yon in ((0.0, nc), (derin, -nc)):
        y.yuz_yon([L(0, 0, d), L(x0, 0, d), L(x0, H, d), L(0, H, d)], key, yon)
        y.yuz_yon([L(x1, 0, d), L(W, 0, d), L(W, H, d), L(x1, H, d)], key, yon)
        for k in range(len(tp) - 1):
            (ua, va), (ub, vb) = tp[k], tp[k + 1]
            y.yuz_yon([L(ua, va, d), L(ub, vb, d), L(ub, H, d), L(ua, H, d)], key, yon)
    yol = [(x0, 0)] + tp + [(x1, 0)]
    xm = (x0 + x1) / 2
    for k in range(len(yol) - 1):
        p, q = yol[k], yol[k + 1]
        m = L((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, derin / 2)
        y.yuz_yon([L(*p, 0), L(*q, 0), L(*q, derin), L(*p, derin)], ic_key, L(xm, hs * 0.5, derin / 2) - m)
    return L, x0, x1, hs


def entablatur(kose, z, he, key='mermer', dis=True, disli=True, ic=None):
    """an entablature round a CCW rectangle of column centres: architrave with two fasciae, frieze, dentils, a crowning
    cornice; ic = inner rectangle (CCW) whose faces look inward (an open pronaos). Returns the top z"""
    D = he * 0.38
    o = disa(kose, D)
    duvarlar(y, o, z, z + he * 0.42, key)
    for zz in (z + he * 0.13, z + he * 0.26):
        silme(y, o, zz, he * 0.03, 0.0025, key, 'duz')
    silme(y, o, z + he * 0.36, he * 0.06, 0.0035, key, 'tac')
    f = disa(kose, D - 0.003)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * (z + he * 0.42), o[j] + Z * (z + he * 0.42), f[j] + Z * (z + he * 0.42), f[i] + Z * (z + he * 0.42)], key, Z)
    duvarlar(y, f, z + he * 0.42, z + he * 0.82, key)
    if disli:
        for i in range(4):
            p, q = f[i], f[(i + 1) % 4]
            Lq = (q - p).length; e = (q - p) / Lq; nn = V(e.y, -e.x)
            k = int(Lq / 0.01)
            for j in range(k):
                kutu(y, p + e * (Lq * (j + 0.2) / k) + Z * (z + he * 0.72) + nn * 0.006, e, Lq / k * 0.6, 0.006, he * 0.1, key, 'onsagsol')
    silme(y, f, z + he * 0.82, he * 0.18, he * 0.28, key, 'tac')
    ii = disa(kose, -D)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([o[i] + Z * z, o[j] + Z * z, ii[j] + Z * z, ii[i] + Z * z], key, -Z)
    if ic:
        n = len(ic)
        for i in range(n):
            duz_duvar(y, ic[(i + 1) % n], ic[i], z, z + he * 0.5, key)
    return z + he, o


def kiremit_kaburga(p0, p1, w=0.0055, key='kiremit2'):
    """a cover-tile (imbrex) rib along a roof slope from p0 to p1: a low ridge of two faces (cheaper than a beam)"""
    p0, p1 = Vector(p0), Vector(p1)
    t = (p1 - p0).normalized()
    s = Z.cross(t)
    if s.length < 1e-6: s = X.copy()
    s.normalize(); u = t.cross(s).normalized()
    if u.z < 0: u = -u
    h = u * (w * 0.55)
    A0, A1 = p0 - s * (w / 2), p1 - s * (w / 2)
    B0, B1 = p0 + s * (w / 2), p1 + s * (w / 2)
    T0, T1 = p0 + h, p1 + h
    y.yuz_yon([A0, A1, T1, T0], key, u - s)
    y.yuz_yon([T0, T1, B1, B0], key, u + s)


def sutun_hafif(cx, cy, z0, z1, r=0.013, key='kirec', tur='toskan'):
    """a lighter column for the long porticoes (~120 triangles): plinth, torus, a tapering shaft (12 sides; Doric:
    fluted look by alternating radii), echinus and abacus; tur 'iyon' adds volutes"""
    H = z1 - z0
    c = (cx, cy)
    n = 12
    hb = H * 0.05 if tur != 'dor' else 0.0
    if hb:
        kutu_merkez(y, c, r * 2.7, r * 2.7, hb * 0.45, key, z0=z0, yuzler='onarkasagsolust')
        donel(y, c, [(r * 1.3, z0 + hb * 0.45), (r * 1.25, z0 + hb * 0.8), (r * 1.04, z0 + hb)], key, n=n)
    hc = H * 0.09
    za, zb = z0 + hb, z1 - hc
    oran = 0.88 if tur == 'dor' else 1.0
    ring = lambda rr, zz: [V(cx + rr * (1 if i % 2 == 0 or oran == 1 else oran) * math.cos(TAU * i / (2 * n if oran < 1 else n)),
                             cy + rr * (1 if i % 2 == 0 or oran == 1 else oran) * math.sin(TAU * i / (2 * n if oran < 1 else n)), zz)
                           for i in range(2 * n if oran < 1 else n)]
    y.serit(ring(r, za), ring(r * 0.9, za + (zb - za) * 0.6), key)
    y.serit(ring(r * 0.9, za + (zb - za) * 0.6), ring(r * 0.84, zb), key)
    donel(y, c, [(r * 0.84, zb), (r * 0.9, zb + hc * 0.2), (r * 1.3, zb + hc * 0.55)], key, n=n)
    kutu_merkez(y, c, r * 2.8, r * 2.8, hc * 0.45, key, z0=zb + hc * 0.55)
    if tur == 'iyon':
        for sg in (-1, 1):
            boru(y, [V(cx + sg * r * 1.2, cy - r * 1.1, zb + hc * 0.4), V(cx + sg * r * 1.2, cy + r * 1.1, zb + hc * 0.4)], r * 0.38, key, n=6)


def revak_hafif(a, b, n, z0, H, tur='toskan', r=0.013, key='kirec', triglif=None):
    """a straight colonnade a->b (faces the right of a->b) of light columns with an architrave, frieze (Doric
    triglyphs if given) and cornice. Returns the top z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    for i in range(n + 1):
        p = a.lerp(b, i / n)
        sutun_hafif(p.x, p.y, z0, z0 + H, r, key, tur)
    he = H * 0.26
    D = r * 3.2
    z = z0 + H
    o = a - e * (r * 1.6) + nc * (D / 2)
    L = W + r * 3.2
    kutu(y, o, e, L, D, he * 0.42, key, 'onarkasagsol')
    y.yuz_yon([o + Z * z, o + e * L + Z * z, o + e * L - nc * D + Z * z, o - nc * D + Z * z], key, -Z)
    kutu(y, o + Z * (he * 0.42) - nc * 0.002, e, L, D - 0.004, he * 0.4, key, 'onarkasagsol')
    if triglif:
        k = n * 2
        for i in range(k + 1):
            p = o + e * (r * 1.6 + W * i / k) + Z * (he * 0.42)
            y.yuz_yon([p - e * (r * 0.45) - nc * 0.0015, p + e * (r * 0.45) - nc * 0.0015, p + e * (r * 0.45) - nc * 0.0015 + Z * (he * 0.4),
                       p - e * (r * 0.45) - nc * 0.0015 + Z * (he * 0.4)], triglif, nc)
    zc = z + he * 0.82
    silme(y, [o, o + e * L], zc, he * 0.18, r * 0.9, key, 'tac', kapali=False)
    silme(y, [o + e * L - nc * D, o - nc * D], zc, he * 0.18, r * 0.9, key, 'tac', kapali=False)
    return zc + he * 0.18


def cati_kiremit_serit(x0, x1, y0, y1, z, h, eksen='y', adim=0.026, key='kiremit2'):
    """imbrex cover-tile ribs on a gable roof (ridge along eksen) from the eaves to the ridge"""
    if eksen == 'y':
        n = int((y1 - y0) / adim)
        for j in range(n + 1):
            yy = y0 + (y1 - y0) * j / n
            for s, xe in ((-1, x0), (1, x1)):
                kiremit_kaburga(V(xe, yy, z + 0.0015), V((x0 + x1) / 2, yy, z + h + 0.0015), key=key)
    else:
        n = int((x1 - x0) / adim)
        for j in range(n + 1):
            xx = x0 + (x1 - x0) * j / n
            for ye in (y0, y1):
                kiremit_kaburga(V(xx, ye, z + 0.0015), V(xx, (y0 + y1) / 2, z + h + 0.0015), key=key)


def heykel(x, yy, z, s=1.0, key='bronz', kaide=True):
    """a draped standing figure (on a moulded pedestal)"""
    if kaide:
        kutu_merkez(y, (x, yy), 0.06 * s, 0.06 * s, 0.01 * s, 'mermer', z0=z)
        kutu_merkez(y, (x, yy), 0.048 * s, 0.048 * s, 0.06 * s, 'kirec', z0=z + 0.01 * s)
        kornis(y, x - 0.024 * s, x + 0.024 * s, yy - 0.024 * s, yy + 0.024 * s, z + 0.064 * s, 0.007 * s, 0.005 * s, 'mermer', 'tac')
        z += 0.071 * s
    donel(y, (x, yy), [(0.014 * s, z), (0.016 * s, z + 0.02 * s), (0.011 * s, z + 0.055 * s), (0.013 * s, z + 0.068 * s),
                       (0.008 * s, z + 0.077 * s), (0, z + 0.079 * s)], key, n=10)
    kure(y, (x, yy, z + 0.088 * s), 0.008 * s, key, n=8, kat=4)
    boru(y, [V(x + 0.01 * s, yy, z + 0.064 * s), V(x + 0.022 * s, yy - 0.01 * s, z + 0.095 * s)], 0.0028 * s, key, n=5)


def at(x, yy, z, aci=0.0, s=1.0, binici=True, key='bronz'):
    """a bronze horse (one foreleg raised) with an optional rider, facing angle aci"""
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
        if binici:
            donel(y, (0.004, 0), [(0.011, 0.074), (0.012, 0.086), (0.008, 0.11), (0, 0.113)], key, n=8)
            kure(y, (0.006, 0, 0.12), 0.0068, key, n=8, kat=4)
            for sy in (-1, 1):
                boru(y, [V(0.0, sy * 0.012, 0.08), V(0.008, sy * 0.017, 0.062)], 0.0035, key, n=5)
            boru(y, [V(0.006, -0.01, 0.104), V(0.03, -0.016, 0.118)], 0.0028, key, n=5)


def nike(c, ex, n, s=0.05, aci=0.55, key='bronz'):
    """a winged Victory in low relief on a wall (centre c, ex along the wall towards where she flies, n out of the
    wall): a streaming robe, a head, two spread wings, an arm holding out a wreath. s: her length"""
    c, ex, n = V(*c), V(*ex), V(*n)
    ca, sa = math.cos(aci), math.sin(aci)
    P = lambda u, v, d: c + ex * (s * (u * ca - v * sa)) + Z * (s * (u * sa + v * ca)) + n * d
    F = lambda pts, d: y.yuz_yon([P(u, v, d) for u, v in pts], key, n)
    F([(-0.15, 0.08), (-0.05, 0.42), (-0.24, 0.4), (-0.32, 0.18)], 0.0015)         # the far wing
    F([(0.05, 0.06), (0.06, 0.48), (-0.12, 0.46), (-0.2, 0.16)], 0.002)            # the near wing
    F([(-0.56, -0.04), (-0.2, -0.17), (-0.05, 0.07), (-0.5, 0.06)], 0.0025)         # robe streaming behind
    F([(-0.2, -0.17), (0.18, -0.1), (0.3, 0.02), (-0.05, 0.07)], 0.0025)            # body
    F([(0.3 + 0.075 * math.cos(TAU * k / 8), 0.08 + 0.075 * math.sin(TAU * k / 8)) for k in range(8)], 0.003)   # head
    F([(0.16, -0.02), (0.5, 0.12), (0.48, 0.17), (0.14, 0.03)], 0.003)               # arm
    for k in range(8):                                                             # the wreath
        a0, a1 = TAU * k / 8, TAU * (k + 1) / 8
        q = [(0.58 + r * math.cos(a), 0.17 + r * math.sin(a)) for r, a in ((0.07, a0), (0.07, a1), (0.045, a1), (0.045, a0))]
        F(q, 0.003)


def rostrum(p, n, zc, key='bronz'):
    """a captured warship's bronze prow nailed to the Rostra: the bow, the three-finned ram low at the waterline
    and the stem post curling up and back"""
    p, n = V(p.x, p.y), V(n.x, n.y)
    e = V(-n.y, n.x)
    tip = p + n * 0.03
    base = [p - e * 0.013 + Z * (zc - 0.012), p + e * 0.013 + Z * (zc - 0.012), p + Z * (zc + 0.017)]
    for i in range(3):
        yuz_dis(y, [base[i], base[(i + 1) % 3], tip + Z * (zc - 0.006)], key, (p.x - n.x * 0.01, p.y - n.y * 0.01, zc))
    boru(y, [tip - n * 0.006 + Z * (zc - 0.008), p + n * 0.056 + Z * (zc - 0.011)], 0.0055, key, n=6, r_son=0.0025)   # the ram
    for dz in (-0.006, 0.0, 0.006):                                                                              # its fins
        y.yuz_yon([p + n * 0.04 - e * 0.0075 + Z * (zc - 0.0115 + dz), p + n * 0.04 + e * 0.0075 + Z * (zc - 0.0115 + dz),
                   p + n * 0.054 + e * 0.003 + Z * (zc - 0.0115 + dz), p + n * 0.054 - e * 0.003 + Z * (zc - 0.0115 + dz)], key, -Z)
        y.yuz_yon([p + n * 0.04 - e * 0.0075 + Z * (zc - 0.0097 + dz), p + n * 0.04 + e * 0.0075 + Z * (zc - 0.0097 + dz),
                   p + n * 0.054 + e * 0.003 + Z * (zc - 0.0097 + dz), p + n * 0.054 - e * 0.003 + Z * (zc - 0.0097 + dz)], key, Z)
    boru(y, [p + n * 0.004 + Z * (zc + 0.015), p + n * 0.012 + Z * (zc + 0.03), p + n * 0.017 + Z * (zc + 0.042),
             p + n * 0.011 + Z * (zc + 0.051), p + n * 0.003 + Z * (zc + 0.048), p + n * 0.004 + Z * (zc + 0.041)], 0.0032, key, n=5,
         r_son=0.002)                                                                                            # the stem post
    for s_ in (-1, 1):                                                                                           # the eye
        kure(y, (p.x + n.x * 0.016 + e.x * s_ * 0.0062, p.y + n.y * 0.016 + e.y * s_ * 0.0062, zc + 0.001), 0.0028, 'altin', n=6, kat=3)


def selvi(x, yy, z, boy=0.2):
    y.prizma((x, yy), 0.005, z, z + boy * 0.12, 'ahsap', n=5)
    donel(y, (x, yy), [(0.0, z + boy * 0.08), (0.02, z + boy * 0.12), (0.026, z + boy * 0.35), (0.021, z + boy * 0.65),
                       (0.009, z + boy * 0.9), (0, z + boy)], 'cimen', n=10)


# ================================================================ platform and paving
y.bolum('Meydan zemini')
X0, X1, Y0, Y1 = -1.0, 1.22, -1.1, 1.2
zemin(y, X0, X1, Y0, Y1, Z0, 'tas_koyu', basamak=(('on', 0.5),), n_basamak=3)
PX0, PX1, PY0, PY1 = -0.64, 0.62, -0.80, 0.42        # the open square
# travertine slabs: a marble cross-strip and a border
ZP = Z0 + 0.0015
y.yuz([V(-0.05, PY0 + 0.02, ZP), V(0.05, PY0 + 0.02, ZP), V(0.05, 0.22, ZP), V(-0.05, 0.22, ZP)], 'mermer')
for (a0, a1, b0, b1) in ((PX0 + 0.02, PX1 - 0.02, PY0 + 0.02, PY0 + 0.05), (PX0 + 0.02, PX0 + 0.05, PY0 + 0.05, PY1 - 0.15),
                         (PX1 - 0.05, PX1 - 0.02, PY0 + 0.05, PY1 - 0.15)):
    y.yuz([V(a0, b0, ZP), V(a1, b0, ZP), V(a1, b1, ZP), V(a0, b1, ZP)], 'kirec')

# ================================================================ temple
y.bolum('Tapınak: podyum ve merdiven')
TX, TY0, TY1 = 0.28, 0.48, 1.005        # column centres
PH = 0.16                                # (a high Italic podium: the temple is the forum's tallest mass)
ZT = Z0 + PH
PW = 0.335                               # podium half width
kutu(y, V(-PW, 0.42, Z0), X, 2 * PW, 0.71, PH, 'kirec', 'onarkasagsol')
y.yuz([V(-PW, 0.42, ZT), V(PW, 0.42, ZT), V(PW, 1.13, ZT), V(-PW, 1.13, ZT)], 'mermer')
silme(y, dikdortgen(-PW, PW, 0.42, 1.13), Z0, 0.025, 0.012, 'mermer', 'kaide')
silme(y, dikdortgen(-PW, PW, 0.42, 1.13), ZT - 0.018, 0.018, 0.012, 'mermer', 'tac')
merdiven(y, (0, 0.22), math.pi / 2, 0.5, Z0, ZT, n=15, d=0.0133, key='mermer')
for sx in (-1, 1):            # the stair's flanking walls with statues
    kutu(y, V(-PW if sx < 0 else 0.25, 0.22, Z0), X, PW - 0.25, 0.2001, PH, 'kirec', 'onsagsolust')
    kornis(y, min(sx * PW, sx * 0.25), max(sx * PW, sx * 0.25), 0.22, 0.42, ZT - 0.018, 0.018, 0.008, 'mermer', 'tac')
    kornis(y, min(sx * PW, sx * 0.25), max(sx * PW, sx * 0.25), 0.22, 0.42, Z0, 0.02, 0.008, 'mermer', 'kaide')
    heykel(sx * 0.2925, 0.27, ZT, 0.95)
# the altar in front
kutu_merkez(y, (0, 0.08), 0.12, 0.08, 0.012, 'mermer', z0=Z0)
kutu_merkez(y, (0, 0.08), 0.1, 0.06, 0.05, 'kirec', z0=Z0 + 0.012)
kornis(y, -0.05, 0.05, 0.05, 0.11, Z0 + 0.055, 0.01, 0.006, 'mermer', 'tac')
for sx in (-1, 1):
    boru(y, [V(sx * 0.05, 0.05, Z0 + 0.068), V(sx * 0.05, 0.11, Z0 + 0.068)], 0.007, 'mermer', n=8)
donel(y, (0, 0.08), [(0.022, Z0 + 0.067), (0.018, Z0 + 0.074), (0, Z0 + 0.076)], 'bronz', n=10)   # a bronze brazier with its flame
donel(y, (0, 0.08), [(0.012, Z0 + 0.074), (0.015, Z0 + 0.082), (0.011, Z0 + 0.093), (0.005, Z0 + 0.102), (0, Z0 + 0.108)], 'boya_sari', n=10)

y.bolum('Tapınak: sütunlar ve cella')
HC = 0.34
ZC = ZT + HC
XS = [-TX + 2 * TX * i / 5 for i in range(6)]
YS = [TY0 + (TY1 - TY0) * j / 5 for j in range(6)]
YCF = 0.74                       # the cella's front wall
for xx in XS:
    sutun(y, xx, TY0, ZT, ZC, 0.02, 'mermer', 'korint')
for yy in YS[1:3]:
    for sx in (-1, 1):
        sutun(y, sx * TX, yy, ZT, ZC, 0.02, 'mermer', 'korint')
# cella: walls on the column line with engaged half columns (pseudoperipteral, like the Maison Carrée)
cella = [V(-TX, YCF), V(TX, YCF), V(TX, TY1), V(-TX, TY1)]
duz_duvar(y, cella[1], cella[2], ZT, ZC, 'kirec')
duz_duvar(y, cella[2], cella[3], ZT, ZC, 'kirec')
duz_duvar(y, cella[3], cella[0], ZT, ZC, 'kirec')
for yy in YS[3:]:
    for sx in (-1, 1):
        sutun(y, sx * (TX + 0.006), yy, ZT, ZC, 0.02, 'mermer', 'korint')
for xx in XS[1:-1]:
    sutun(y, xx, TY1 + 0.006, ZT, ZC, 0.02, 'mermer', 'korint')
silme(y, cella, ZT, 0.02, 0.006, 'mermer', 'kaide')
# cella front: a tall bronze door in a marble frame
W_, e_, nc_, L_ = dikdortgen_acik(y, V(-TX, YCF), V(TX, YCF), ZT, HC, 0.36, 0.64, 0.0, 0.2, ('kirec', 'mermer', 'mermer', 'bronz'),
                                  derin=0.02, cerceve=(0.012, 'mermer'))
y.yuz_yon([L_(0.498, 0, 0.0185), L_(0.502, 0, 0.0185), L_(0.502, 0.2, 0.0185), L_(0.498, 0.2, 0.0185)], 'koyu', nc_)
kornis(y, -0.07, 0.07, YCF - 0.02, YCF, ZT + 0.215, 0.012, 0.006, 'mermer', 'tac')
y.yuz_yon([V(-TX, TY0, ZC + 0.03), V(TX, TY0, ZC + 0.03), V(TX, YCF, ZC + 0.03), V(-TX, YCF, ZC + 0.03)], 'kirec', -Z)

y.bolum('Tapınak: saçaklık, alınlık, çatı')
HE = HC * 0.26
DD = HE * 0.38
ic = [V(TX - DD, YCF), V(TX - DD, TY0 + DD), V(-TX + DD, TY0 + DD), V(-TX + DD, YCF)]
ZE, dis_ = entablatur(dikdortgen(-TX, TX, TY0, TY1), ZC, HE, 'mermer', ic=None)
for i in range(3):
    duz_duvar(y, ic[i], ic[i + 1], ZC, ZC + HE * 0.42, 'mermer')
yazi(V(0, dis_[0].y + 0.003, ZC + HE * 0.47), X, -Y, 'DIVO IVLIO', HE * 0.22)
HP = 0.135
xa, xb, ya, yb = dis_[0].x, dis_[1].x, dis_[0].y, dis_[2].y
alinlik(y, V(xa, ya), V(xb, ya), ZE, HP, derin=yb - ya - 0.003, key='mermer', ic_key='kirmizi', c=0.012, cati_key='kiremit')
alinlik(y, V(xb, yb), V(xa, yb), ZE, HP, derin=0.003, key='mermer', ic_key='kirmizi', c=0.012, cati_key='kiremit')
cati_kiremit_serit(xa, xb, ya + 0.01, yb - 0.01, ZE + 0.0096, HP, 'y')
cubuk(y, V(0, ya, ZE + HP + 0.014), V(0, yb, ZE + HP + 0.014), 0.012, 'kiremit2')
# pediment sculpture: a seated god in the middle, standing and reclining figures towards the corners
yt = ya + 0.006 - 0.004
heykel(0, yt - 0.002, ZE + 0.012, 0.75, 'mermer', kaide=False)
for s in (-1, 1):
    heykel(s * 0.06, yt - 0.002, ZE + 0.012, 0.55, 'mermer', kaide=False)
    boru(y, [V(s * 0.11, yt, ZE + 0.02), V(s * 0.17, yt, ZE + 0.016), V(s * 0.2, yt, ZE + 0.013)], 0.008, 'mermer', n=6, r_son=0.005)
    kure(y, (s * 0.105, yt, ZE + 0.028), 0.007, 'mermer', n=8, kat=4)
# acroteria: a bronze figure on the apex, winged victories at the corners
heykel(0, ya + 0.01, ZE + HP + 0.006, 0.6, 'altin', kaide=False)
for s, xx in ((-1, xa), (1, xb)):
    kutu_merkez(y, (xx - s * 0.012, ya + 0.012), 0.024, 0.024, 0.014, 'mermer', z0=ZE + 0.008)
    heykel(xx - s * 0.012, ya + 0.012, ZE + 0.022, 0.5, 'bronz', kaide=False)

# ================================================================ front double colonnade with the arch
y.bolum('Ön revak (çift sütun dizisi)')
FY0, FY1 = -0.97, -0.80
AX = 0.19                         # the arch's half width
HF = 0.19
ZF = Z0 + 0.02
for (xa_, xb_, n) in ((-0.94, -AX, 5), (AX, PX1, 3)):
    kutu(y, V(xa_ - 0.02, FY0 - 0.02, Z0), X, xb_ - xa_ + 0.04, FY1 - FY0 + 0.04, 0.02, 'kirec', 'onarkasagsolust')
    zt = revak_hafif(V(xa_, FY0), V(xb_, FY0), n, ZF, HF, 'toskan', r=0.013, key='kirec')
    revak_hafif(V(xb_, FY1), V(xa_, FY1), n, ZF, HF, 'toskan', r=0.013, key='kirec')
    y.yuz_yon([V(xa_, FY0, ZF + HF + 0.004), V(xb_, FY0, ZF + HF + 0.004), V(xb_, FY1, ZF + HF + 0.004), V(xa_, FY1, ZF + HF + 0.004)],
              'ahsap_koyu', -Z)   # coffered ceiling
    for k in range(1, n):
        xx = xa_ + (xb_ - xa_) * k / n
        cubuk(y, V(xx, FY0, ZF + HF + 0.002), V(xx, FY1, ZF + HF + 0.002), 0.008, 'ahsap', 0.004)
    cati_besik(y, xa_ - 0.025, xb_ + 0.025, FY0 - 0.02, FY1 + 0.02, zt, 0.06, 0.02, 'kiremit', ucluk_key='kirec', alinlik_key='mermer',
               mahya='kiremit2', ns=3, nr=2)
    cati_kiremit_serit(xa_ - 0.02, xb_ + 0.02, FY0 - 0.04, FY1 + 0.04, zt, 0.06, 'x')
ZFT = zt

y.bolum('Zafer takı')
AY0, AY1 = -1.0, -0.77
HA = 0.33
ZA = Z0 + 0.02
kutu(y, V(-AX - 0.01, AY0 - 0.012, Z0), X, 2 * AX + 0.02, AY1 - AY0 + 0.024, 0.02, 'mermer', 'onarkasagsolust')
L_, ax0, ax1, ahs = gecit(V(-AX, AY0), V(AX, AY0), ZA, HA, AY1 - AY0, en=0.46, ust=0.085, key='mermer', ic_key='kirec')
duz_duvar(y, V(AX, AY0), V(AX, AY1), ZA, ZA + HA, 'mermer')
duz_duvar(y, V(-AX, AY1), V(-AX, AY0), ZA, ZA + HA, 'mermer')
# coffers in the vault and reliefs in the passage
for yy, s in ((AY0, -1), (AY1, 1)):
    # engaged composite columns on pedestals, the impost moulding, winged victories in the spandrels
    for xx in (-AX + 0.04, -AX + 0.1, AX - 0.1, AX - 0.04):
        kutu_merkez(y, (xx, yy + s * 0.008), 0.034, 0.02, 0.05, 'mermer', z0=ZA)
        kornis(y, xx - 0.017, xx + 0.017, yy + s * 0.008 - 0.01, yy + s * 0.008 + 0.01, ZA + 0.044, 0.006, 0.004, 'mermer', 'tac')
        sutun_hafif(xx, yy + s * 0.006, ZA + 0.05, ZA + HA - 0.05, 0.011, 'mermer', 'iyon')
    for sx in (-1, 1):            # winged Victories in the spandrels, flying towards the keystone
        nike((sx * 0.056, yy, ZA + ahs + 0.094), V(-sx, 0), V(0, s), s=0.046, aci=0.45)
    kutu_merkez(y, (0, yy + s * 0.004), 0.024, 0.008, 0.026, 'mermer', z0=ZA + HA - 0.075)   # keystone
y.bolum('Zafer takı: saçaklık, attika, yazıt, kuadriga')
ZAE = ZA + HA
kornis(y, -AX - 0.01, AX + 0.01, AY0 - 0.012, AY1 + 0.012, ZAE - 0.05, 0.05, 0.014, 'mermer', 'tac')
duvarlar(y, dikdortgen(-AX + 0.005, AX - 0.005, AY0 + 0.0, AY1 - 0.0, 0), ZAE, ZAE + 0.08, 'mermer', ust='mermer')
kornis(y, -AX - 0.0, AX + 0.0, AY0 - 0.004, AY1 + 0.004, ZAE + 0.075, 0.012, 0.01, 'mermer', 'tac')
yazi(V(0, AY0 + 0.0, ZAE + 0.022), X, -Y, 'S.P.Q.R', 0.036)
yazi(V(0, AY1, ZAE + 0.022), -X, Y, 'S.P.Q.R', 0.036)
for yy, nn in ((AY0, -Y), (AY1, Y)):          # framed relief panels either side of the inscription
    for xc in (-0.13, 0.13):
        for (u0, u1, v0, v1) in ((xc - 0.035, xc + 0.035, ZAE + 0.012, ZAE + 0.016), (xc - 0.035, xc + 0.035, ZAE + 0.064, ZAE + 0.068),
                                 (xc - 0.035, xc - 0.031, ZAE + 0.012, ZAE + 0.068), (xc + 0.031, xc + 0.035, ZAE + 0.012, ZAE + 0.068)):
            kutu(y, V(u0, yy + nn.y * 0.003, v0), X, u1 - u0, 0.003 if nn.y > 0 else -0.003, v1 - v0, 'kirec', 'onarkasagsolust')
        for k in range(3):                    # marching figures in low relief
            xx = xc - 0.018 + 0.018 * k
            y.yuz_yon([V(xx - 0.005, yy + nn.y * 0.0012, ZAE + 0.02), V(xx + 0.005, yy + nn.y * 0.0012, ZAE + 0.02),
                       V(xx + 0.003, yy + nn.y * 0.0012, ZAE + 0.052), V(xx - 0.003, yy + nn.y * 0.0012, ZAE + 0.052)], 'kirec', nn)
            kure(y, (xx, yy + nn.y * 0.001, ZAE + 0.057), 0.004, 'kirec', n=6, kat=3)
ZQ = ZAE + 0.087
kutu_merkez(y, (0, (AY0 + AY1) / 2), 0.1, 0.08, 0.01, 'mermer', z0=ZQ)
for k, dx in enumerate((-0.034, -0.012, 0.012, 0.034)):
    at(dx, (AY0 + AY1) / 2 - 0.01, ZQ + 0.01, -math.pi / 2, 0.75, binici=False)
kutu_merkez(y, (0, (AY0 + AY1) / 2 + 0.035), 0.05, 0.03, 0.03, 'bronz', z0=ZQ + 0.01)
heykel(0, (AY0 + AY1) / 2 + 0.035, ZQ + 0.03, 0.55, 'altin', kaide=False)
for sx in (-1, 1):
    sancak(y, sx * (AX - 0.015), (AY0 + AY1) / 2, ZQ - 0.002, boy=0.17, en=0.09, yuk=0.06, aci=-math.pi / 2 + sx * 0.4)

# ================================================================ left portico with shops
y.bolum('Sol revak ve dükkânlar (tabernae)')
LX0, LX1 = -0.94, -0.66
LY0, LY1 = -0.80, 1.12
HL = 0.2
kutu(y, V(LX0, LY0, Z0), X, LX1 - LX0 + 0.02, LY1 - LY0, 0.02, 'kirec', 'onarkasagsolust')
zl = revak_hafif(V(LX1, LY0 + 0.03), V(LX1, LY1 - 0.03), 11, Z0 + 0.02, HL, 'dor', r=0.013, key='kirec', triglif='tas_koyu')
# the back wall: outside (facing -x) two storeys of shop doors and small windows, inside plain with doors
nb = 11
for k in range(nb):
    a = V(LX0, LY1 - (LY1 - LY0) * k / nb); b = V(LX0, LY1 - (LY1 - LY0) * (k + 1) / nb)
    y.kemerli(a, b, Z0, 0.15, ('tugla_roma', 'tugla_roma_koyu', 'kirec', 'koyu'), v0=0.0, en=0.55, ust=0.02, derin=0.02, k_say=8,
              cerceve=(0.006, ['kirec', 'tugla_roma_koyu']))
    W_, e_, nc_, Lk = dikdortgen_acik(y, a, b, Z0 + 0.15, zl - Z0 - 0.15, 0.35, 0.65, 0.035, 0.085, ('tugla_roma', 'tugla_roma_koyu', 'kirec', 'koyu'),
                                      derin=0.012, cerceve=(0.005, 'kirec'))
    # wooden shutters half drawn, a counter
    y.yuz_yon([Lk(0.24, -0.15 + 0.0, 0.019), Lk(0.38, -0.15 + 0.0, 0.019), Lk(0.38, -0.15 + 0.095, 0.019), Lk(0.24, -0.15 + 0.095, 0.019)],
              'ahsap', nc_)
    kutu(y, Lk(0.28, -0.15, -0.012), e_, 0.06, 0.012, 0.035, 'kirec', 'onsagsolust')
silme(y, [V(LX0, LY1), V(LX0, LY0)], Z0 + 0.145, 0.012, 0.008, 'kirec', 'tac', kapali=False)
for a, b in ((V(LX0 + 0.012, LY0), V(LX0 + 0.012, LY1)),):
    duz_duvar(y, a, b, Z0 + 0.02, zl, 'siva_krem')
    for k in range(nb):
        p = a.lerp(b, (k + 0.5) / nb)
        y.yuz_yon([p + V(0.001, -0.02, Z0 + 0.02), p + V(0.001, 0.02, Z0 + 0.02), p + V(0.001, 0.02, Z0 + 0.11), p + V(0.001, -0.02, Z0 + 0.11)], 'koyu', X)
for yy, s in ((LY0, -1), (LY1, 1)):
    duz_duvar(y, V(LX0, yy) if s < 0 else V(LX0 + 0.012, yy), V(LX0 + 0.012, yy) if s < 0 else V(LX0, yy), Z0, zl, 'tugla_roma')
cati_besik(y, LX0 - 0.02, LX1 + 0.045, LY0, LY1, zl, 0.07, 0.02, 'kiremit', ucluk_key='kirec', alinlik_key='mermer', mahya='kiremit2', ns=3, nr=2)
cati_kiremit_serit(LX0 - 0.02, LX1 + 0.045, LY0 - 0.01, LY1 + 0.01, zl, 0.07, 'y')
y.yuz_yon([V(LX0 + 0.012, LY0, zl - 0.03), V(LX1, LY0, zl - 0.03), V(LX1, LY1, zl - 0.03), V(LX0 + 0.012, LY1, zl - 0.03)], 'ahsap_koyu', -Z)

# ================================================================ basilica
y.bolum('Bazilika: iki katlı kemerli cephe')
BX0, BX1, BY0, BY1 = 0.66, 1.16, -0.98, 0.32
H1, H2 = 0.16, 0.13
ZB1 = Z0 + 0.025
kutu(y, V(BX0 - 0.03, BY0 - 0.03, Z0), X, BX1 - BX0 + 0.06, BY1 - BY0 + 0.06, 0.025, 'mermer', 'onarkasagsolust')
merdiven(y, (BX0 - 0.05, -0.33), 0.0, 0.5, Z0, ZB1, n=2, d=0.012, key='mermer')
NB = 8
ARK = ('kirec', 'kirec', 'mermer', 'tas_koyu')
yuzler = [(V(BX0, BY1), V(BX0, BY0), NB), (V(BX0, BY0), V(BX1, BY0), 3)]
for a, b, n in yuzler:
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        y.kemerli(p, q, ZB1, H1, ARK, v0=0.0, en=0.6, ust=0.03, derin=0.05, k_say=10)
        y.kemerli(p, q, ZB1 + H1, H2, ARK, v0=0.0, en=0.58, ust=0.025, derin=0.05, k_say=10, korkuluk=0.035)
    for k in range(0 if n == NB else 1, n + 1):
        p = a.lerp(b, k / n) + nn * 0.008
        sutun_hafif(p.x, p.y, ZB1, ZB1 + H1 - 0.02, 0.011, 'kirec', 'toskan')
        sutun_hafif(p.x, p.y, ZB1 + H1 + 0.012, ZB1 + H1 + H2 - 0.02, 0.0095, 'kirec', 'iyon')
    silme(y, [a, b], ZB1 + H1 - 0.022, 0.022, 0.018, 'mermer', 'tac', kapali=False)
    silme(y, [a, b], ZB1 + H1 + H2 - 0.022, 0.022, 0.018, 'mermer', 'tac', kapali=False)
    silme(y, [a, b], ZB1, 0.012, 0.012, 'mermer', 'kaide', kapali=False)
# the plain back and far end: brick, small windows
for a, b in ((V(BX1, BY0), V(BX1, BY1)), (V(BX1, BY1), V(BX0, BY1))):
    L = (b - a).length; n = max(2, int(L / 0.16))
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        y.kemerli(p, q, ZB1, H1 + H2, ('tugla_roma', 'tugla_roma_koyu', 'kirec', 'cam'), v0=0.16, en=0.35, ust=0.03, derin=0.015, k_say=6)
    silme(y, [a, b], ZB1 + H1 + H2 - 0.022, 0.022, 0.012, 'kirec', 'tac', kapali=False)
ZB2 = ZB1 + H1 + H2
y.bolum('Bazilika: orta nef, yüksek pencereler, çatılar')
NX0, NX1 = 0.80, 1.02
HN = 0.13
# aisle lean-to roofs, from the outer walls up to the nave walls
for (xo, xi) in ((BX0 - 0.012, NX0), (BX1 + 0.012, NX1)):
    s = 1 if xi > xo else -1
    za, zb = ZB2, ZB2 + 0.05
    y.yuz_yon([V(xo, BY0 - 0.012, za), V(xo, BY1 + 0.012, za), V(xi, BY1 + 0.012, zb), V(xi, BY0 - 0.012, zb)], 'kiremit', Z)
    y.yuz_yon([V(xo, BY0 - 0.012, za), V(xo, BY1 + 0.012, za), V(xo, BY1 + 0.012, za - 0.008), V(xo, BY0 - 0.012, za - 0.008)], 'ahsap_koyu', V(-s, 0))
    for yy in (BY0 - 0.012, BY1 + 0.012):
        y.yuz_yon([V(xo, yy, za - 0.008), V(xi, yy, za - 0.008), V(xi, yy, zb), V(xo, yy, za)], 'kirec', V(0, -1 if yy < 0 else 1))
    nr = int((BY1 - BY0) / 0.026)
    for j in range(nr + 1):
        yy = BY0 + (BY1 - BY0) * j / nr
        kiremit_kaburga(V(xo, yy, za + 0.0015), V(xi, yy, zb + 0.0015))
# the clerestory: nave walls with arched windows, a cornice, the gable roof
nave = dikdortgen(NX0, NX1, BY0, BY1)
pencereli_duvar(y, nave, ZB2 + 0.04, HN, [1, 8, 1, 8], renk=('tugla_roma', 'tugla_roma_koyu', 'kirec', 'cam'), v0=0.03, en=0.5, ust=0.025,
                derin=0.015, k_say=8, sivri=0.0, cerceve=(0.005, 'kirec'))
duvarlar(y, nave, ZB2, ZB2 + 0.04, 'tugla_roma')
silme(y, nave, ZB2 + 0.04 + HN - 0.016, 0.016, 0.01, 'kirec', 'tac')
ZN = ZB2 + 0.04 + HN
cati_besik(y, NX0, NX1, BY0, BY1, ZN, 0.08, 0.025, 'kiremit', ucluk_key='kirec', alinlik_key='mermer', mahya='kiremit2', ns=3, nr=2)
cati_kiremit_serit(NX0 - 0.025, NX1 + 0.025, BY0, BY1, ZN, 0.08, 'y')
# statues on the attic above the front arcade
for k in range(1, NB):
    p = V(BX0 + 0.004, BY1 + (BY0 - BY1) * k / NB)
    heykel(p.x, p.y, ZB2, 0.55, 'mermer', kaide=False)

# ================================================================ curia
y.bolum('Curia (senato binası)')
CX0, CX1, CY0, CY1 = 0.68, 1.12, 0.52, 0.94
HCU = 0.38
kutu(y, V(CX0 - 0.02, CY0 - 0.02, Z0), X, CX1 - CX0 + 0.04, CY1 - CY0 + 0.04, 0.03, 'mermer', 'onarkasagsolust')
merdiven(y, (CX0 - 0.1, (CY0 + CY1) / 2), 0.0, 0.16, Z0, Z0 + 0.03, n=4, d=0.02, key='mermer')
ZCU = Z0 + 0.03
# front (facing -x): the bronze door in a marble frame, three tall windows above, corner pilasters
W_, e_, nc_, Lc = dikdortgen_acik(y, V(CX0, CY1), V(CX0, CY0), ZCU, 0.17, 0.38, 0.62, 0.0, 0.13, ('siva_krem', 'mermer', 'mermer', 'bronz'),
                                  derin=0.02, cerceve=(0.01, 'mermer'))
kornis(y, CX0 - 0.012, CX0, (CY0 + CY1) / 2 - 0.06, (CY0 + CY1) / 2 + 0.06, ZCU + 0.135, 0.012, 0.006, 'mermer', 'tac')
pencereli_duvar(y, [V(CX0, CY1), V(CX0, CY0)], ZCU + 0.17, HCU - 0.17, [3], kapali=False, renk=('tugla_roma', 'tugla_roma_koyu', 'kirec', 'cam'),
                v0=0.04, en=0.5, ust=0.03, derin=0.015, k_say=8, sivri=0.0, cerceve=(0.006, 'kirec'))
silme(y, [V(CX0, CY1), V(CX0, CY0)], ZCU + 0.165, 0.012, 0.008, 'mermer', 'tac', kapali=False)
for a, b in ((V(CX0, CY0), V(CX1, CY0)), (V(CX1, CY0), V(CX1, CY1)), (V(CX1, CY1), V(CX0, CY1))):
    duz_duvar(y, a, b, ZCU, ZCU + 0.17, 'siva_krem')
    pencereli_duvar(y, [a, b], ZCU + 0.17, HCU - 0.17, [2], kapali=False, renk=('tugla_roma', 'tugla_roma_koyu', 'kirec', 'cam'), v0=0.06,
                    en=0.35, ust=0.04, derin=0.015, k_say=8, sivri=0.0)
    silme(y, [a, b], ZCU + 0.165, 0.012, 0.008, 'mermer', 'tac', kapali=False)
for (xx, yy) in ((CX0, CY0), (CX0, CY1), (CX1, CY0), (CX1, CY1)):
    kutu_merkez(y, (xx, yy), 0.03, 0.03, HCU, 'tugla_roma', z0=ZCU)
silme(y, dikdortgen(CX0, CX1, CY0, CY1), ZCU + HCU - 0.022, 0.022, 0.02, 'kirec', 'tac')
cati_besik(y, CX0, CX1, CY0, CY1, ZCU + HCU, 0.1, 0.03, 'kiremit', ucluk_key='tugla_roma', alinlik_key='kirec', mahya='kiremit2', ns=3, nr=2)
cati_kiremit_serit(CX0 - 0.03, CX1 + 0.03, CY0 - 0.03, CY1 + 0.03, ZCU + HCU, 0.1, 'x')

# ================================================================ rostra, statues, column, trees, banners
y.bolum('Rostra, atlı heykel, onur sütunu')
RX, RY = -0.34, -0.3
kutu_merkez(y, (RX, RY), 0.34, 0.15, 0.075, 'kirec', z0=Z0)
kornis(y, RX - 0.17, RX + 0.17, RY - 0.075, RY + 0.075, Z0 + 0.065, 0.012, 0.008, 'mermer', 'tac')
kornis(y, RX - 0.17, RX + 0.17, RY - 0.075, RY + 0.075, Z0, 0.012, 0.006, 'mermer', 'kaide')
for k in range(6):              # the bronze ship prows (rostra) nailed to the front
    rostrum(V(RX - 0.14 + 0.056 * k, RY - 0.075), V(0, -1), Z0 + 0.036)
for i in range(13):            # a balustrade on top
    xx = RX - 0.16 + 0.32 * i / 12
    y.prizma((xx, RY - 0.065), 0.004, Z0 + 0.077, Z0 + 0.1, 'mermer', n=6, ust=False)
boru(y, [V(RX - 0.165, RY - 0.065, Z0 + 0.102), V(RX + 0.165, RY - 0.065, Z0 + 0.102)], 0.004, 'mermer', n=6)
merdiven(y, (RX, RY + 0.17), -math.pi / 2, 0.08, Z0, Z0 + 0.075, n=5, d=0.019, key='kirec')
heykel(RX + 0.1, RY + 0.02, Z0 + 0.075, 0.6, 'bronz', kaide=False)
# equestrian statue on a tall pedestal
EX, EY = 0.3, -0.18
kutu_merkez(y, (EX, EY), 0.16, 0.1, 0.012, 'mermer', z0=Z0)
kutu_merkez(y, (EX, EY), 0.14, 0.08, 0.1, 'kirec', z0=Z0 + 0.012)
kornis(y, EX - 0.07, EX + 0.07, EY - 0.04, EY + 0.04, Z0 + 0.1, 0.014, 0.008, 'mermer', 'tac')
kornis(y, EX - 0.07, EX + 0.07, EY - 0.04, EY + 0.04, Z0 + 0.012, 0.01, 0.006, 'mermer', 'kaide')
at(EX - 0.005, EY, Z0 + 0.114, math.pi * 0.85, 1.05)
# honorific column
OX, OY = -0.42, 0.14
for k, w in enumerate((0.11, 0.09, 0.07)):
    kutu_merkez(y, (OX, OY), w, w, 0.014, 'kirec', z0=Z0 + 0.014 * k)
kutu_merkez(y, (OX, OY), 0.055, 0.055, 0.06, 'mermer', z0=Z0 + 0.042)
kornis(y, OX - 0.0275, OX + 0.0275, OY - 0.0275, OY + 0.0275, Z0 + 0.096, 0.01, 0.006, 'mermer', 'tac')
sutun(y, OX, OY, Z0 + 0.106, Z0 + 0.58, 0.021, 'granit', 'korint', bas_key='mermer')
heykel(OX, OY, Z0 + 0.58, 0.9, 'altin', kaide=False)
y.bolum('Ağaçlar ve sancaklar')
for (xx, yy) in ((-0.48, 1.06), (-0.42, 0.92), (0.48, 1.08), (0.42, 0.95), (0.55, 0.47), (-0.52, 0.55)):
    selvi(xx, yy, Z0, 0.2 + 0.03 * math.sin(xx * 31))
for sx in (-1, 1):
    sancak(y, sx * 0.25, 0.2, Z0, boy=0.3, en=0.11, yuk=0.07, aci=math.pi + sx * 0.3 if sx < 0 else sx * 0.3)

calistir(y, 'lm_forum')
