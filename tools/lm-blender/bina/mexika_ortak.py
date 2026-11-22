# Shared helpers for the late-age Aztec landmarks lm_templomayor, lm_topsahasi, lm_gunespiramidi, lm_taktakvim
# (not a building: imported by those scripts). Talud-tablero tiers, stairs with alfardas ending in a dado, serpent
# heads, skulls and the tzompantli rack, stepped merlons, braziers, tiered thatch, carved discs and rings (any plane),
# small figures. Built like parcalar.py: faces wound outward, local origin, place with parca().
import math
from mathutils import Vector
from parcalar import *


# ---------------------------------------------------------------- slabs and reliefs in any plane
def taban(n):
    """an (u, v) basis for a plane facing n: u = Z x n (horizontal), v = n x u (up); for a level plane u = X"""
    n = Vector(n).normalized()
    u = Z.cross(n)
    if u.length < 1e-4: u = X.copy()
    u.normalize()
    return u, n.cross(u).normalized(), n


def levha(y, o, e, uv, kalin, key, yan_key=None, arka=True):
    """a slab: the outline uv = [(u along e, v up), ...] (any winding, may be concave) on the plane through o, its
    front facing the right of e, extruded kalin backwards (to the left of e); rims yan_key; arka False: no back face
    (the slab lies on a wall)"""
    o = Vector(o); e = Vector((e[0], e[1], 0)).normalized(); nc = V(e.y, -e.x)
    s = sum(uv[i][0] * uv[(i + 1) % len(uv)][1] - uv[(i + 1) % len(uv)][0] * uv[i][1] for i in range(len(uv)))
    if s < 0: uv = uv[::-1]
    P = lambda u, v, d: o + e * u + Z * v - nc * d
    y.yuz_yon([P(u, v, 0) for u, v in uv], key, nc)
    if arka: y.yuz_yon([P(u, v, kalin) for u, v in uv], key, -nc)
    m = len(uv)
    for i in range(m):
        (ua, va), (ub, vb) = uv[i], uv[(i + 1) % m]
        out = e * (vb - va) - Z * (ub - ua)
        y.yuz_yon([P(ua, va, 0), P(ub, vb, 0), P(ub, vb, kalin), P(ua, va, kalin)], yan_key or key, out)


def kabartma(y, c, n, uv, d0, d1, key, yan_key=None, arka=False, u=None):
    """a relief on a plane facing n through c: the outline uv (in the taban() basis, or u given) raised from depth d0
    to d1 along n (front face at d1); arka: a back face at d0 too"""
    if u is None:
        u, v, n = taban(n)
    else:
        n = Vector(n).normalized(); u = Vector(u).normalized(); v = n.cross(u)
    c = Vector(c)
    s = sum(uv[i][0] * uv[(i + 1) % len(uv)][1] - uv[(i + 1) % len(uv)][0] * uv[i][1] for i in range(len(uv)))
    if s < 0: uv = uv[::-1]
    P = lambda a, b, d: c + u * a + v * b + n * d
    y.yuz_yon([P(a, b, d1) for a, b in uv], key, n)
    if arka: y.yuz_yon([P(a, b, d0) for a, b in uv], key, -n)
    m = len(uv)
    if abs(d1 - d0) < 1e-7: return
    for i in range(m):
        (ua, va), (ub, vb) = uv[i], uv[(i + 1) % m]
        out = u * (vb - va) - v * (ub - ua)
        y.yuz_yon([P(ua, va, d0), P(ub, vb, d0), P(ub, vb, d1), P(ua, va, d1)], yan_key or key, out)


def halka_disk(y, c, n, r0, r1, d0, d1, key, m=32, yan_key=None, ic_key=None, a0=0.0, a1=TAU, arka=False, kat=0.0):
    """an annulus (r0 inner, r1 outer; r0 0: a full disc) on the plane facing n through c, raised from d0 to d1 along
    n; a0..a1 an arc of it (its ends closed); arka: its back face at d0. Angles from the basis u (taban) towards v"""
    u, v, n = taban(n); c = Vector(c)
    tam = abs(a1 - a0 - TAU) < 1e-6
    k = m if tam else m + 1
    A = lambda r, i, d: c + (u * math.cos(kat + a0 + (a1 - a0) * i / m) + v * math.sin(kat + a0 + (a1 - a0) * i / m)) * r + n * d
    for i in range(m):
        j = (i + 1) % k if tam else i + 1
        if r0 > 1e-9:
            y.yuz_yon([A(r0, i, d1), A(r1, i, d1), A(r1, j, d1), A(r0, j, d1)], key, n)
            if arka: y.yuz_yon([A(r0, i, d0), A(r1, i, d0), A(r1, j, d0), A(r0, j, d0)], key, -n)
        else:
            y.yuz_yon([c + n * d1, A(r1, i, d1), A(r1, j, d1)], key, n)
            if arka: y.yuz_yon([c + n * d0, A(r1, i, d0), A(r1, j, d0)], key, -n)
        if abs(d1 - d0) > 1e-7:
            mo = (A(r1, i, 0) + A(r1, j, 0)) / 2 - c
            y.yuz_yon([A(r1, i, d0), A(r1, j, d0), A(r1, j, d1), A(r1, i, d1)], yan_key or key, mo)
            if r0 > 1e-9:
                y.yuz_yon([A(r0, i, d0), A(r0, j, d0), A(r0, j, d1), A(r0, i, d1)], ic_key or yan_key or key, -mo)
    if not tam and abs(d1 - d0) > 1e-7:
        for i, s in ((0, -1), (m, 1)):
            t = kat + a0 + (a1 - a0) * i / m
            tang = (-u * math.sin(t) + v * math.cos(t)) * s
            y.yuz_yon([A(r0, i, d0), A(r1, i, d0), A(r1, i, d1), A(r0, i, d1)], yan_key or key, tang)


def daire(r, m=14, cu=0.0, cv=0.0, kat=0.0):
    """a circle outline as (u, v) points"""
    return [(cu + r * math.cos(kat + TAU * i / m), cv + r * math.sin(kat + TAU * i / m)) for i in range(m)]


def kesik(y, c, w0, d0, w1, d1, z0, z1, keys, ust=True, n_dilim=1, ust_key=None, alt=False):
    """a truncated pyramid w0 x d0 at z0 to w1 x d1 at z1 (battered block, a shrine's tall roof); keys: a key or a
    list alternating over n_dilim vertical strips per side (striped roofs)"""
    keys = keys if isinstance(keys, (list, tuple)) else [keys]
    a = dikdortgen(c[0] - w0 / 2, c[0] + w0 / 2, c[1] - d0 / 2, c[1] + d0 / 2, z0)
    b = dikdortgen(c[0] - w1 / 2, c[0] + w1 / 2, c[1] - d1 / 2, c[1] + d1 / 2, z1)
    for i in range(4):
        j = (i + 1) % 4
        out = V(a[i].x + a[j].x - 2 * c[0], a[i].y + a[j].y - 2 * c[1])
        for k in range(n_dilim):
            t0, t1 = k / n_dilim, (k + 1) / n_dilim
            y.yuz_yon([a[i].lerp(a[j], t0), a[i].lerp(a[j], t1), b[i].lerp(b[j], t1), b[i].lerp(b[j], t0)], keys[k % len(keys)], out)
    if ust: y.yuz_yon(b, ust_key or keys[0], Z)
    if alt: y.yuz_yon(a, keys[0], -Z)
    return a, b


# ---------------------------------------------------------------- tiers, stairs
def kademe(y, c, hw, hd, z0, h, ins, talud=0.72, key='siva', bant_key=None, ust_key='zemin', cizgi=None, cikinti=0.15):
    """one talud-tablero tier on the rectangle 2hw x 2hd round c: a talud sloping in by ins up to talud x h, then an
    upright band (bant_key) set out by cikinti x ins over the talud's top, a terrace on top (ust_key); cizgi: a key
    for a thin painted line along the band's top. Returns the band's half sizes (hw', hd') and its top z"""
    cx, cy = c
    zm, z1 = z0 + h * talud, z0 + h
    alt = dikdortgen(cx - hw, cx + hw, cy - hd, cy + hd, z0)
    ort = dikdortgen(cx - hw + ins, cx + hw - ins, cy - hd + ins, cy + hd - ins, zm)
    y.serit(alt, ort, key)
    bw, bd = hw - ins * (1 - cikinti), hd - ins * (1 - cikinti)
    tb = dikdortgen(cx - bw, cx + bw, cy - bd, cy + bd)
    duvarlar(y, tb, zm, z1, bant_key or key)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([ort[i], ort[j], tb[j] + Z * zm, tb[i] + Z * zm], key, -Z)
    y.yuz_yon([p + Z * z1 for p in tb], ust_key or key, Z)
    if cizgi:
        silme(y, tb, z1 - (z1 - zm) * 0.2, (z1 - zm) * 0.2, 0.003, cizgi)
    return bw, bd, z1


def kademe_kose(y, kose, z0, h, ins, talud=0.4, key='kirec', bant_key=None, ust_key='kirec', cerceve=None):
    """a talud-tablero platform on any CCW outline (a U, an L): talud in by ins up to talud x h, an upright band to z0 + h;
    cerceve: a key for Teotihuacan frame bands (top and bottom) round the band. Returns the band outline and the top z"""
    kose = [V(p.x, p.y) for p in kose]
    zm, z1 = z0 + h * talud, z0 + h
    alt = [p + Z * z0 for p in kose]
    ort = [p + Z * zm for p in disa(kose, -ins)]
    tb = disa(kose, -ins)
    y.serit(alt, ort, key)
    duvarlar(y, tb, zm, z1, bant_key or key)
    y.yuz_yon([p + Z * z1 for p in tb], ust_key, Z)
    if cerceve:
        silme(y, tb, z1 - (z1 - zm) * 0.24, (z1 - zm) * 0.24, 0.007, cerceve)
        silme(y, tb, zm, (z1 - zm) * 0.16, 0.007, cerceve)
    return tb, z1


def bant_diskleri(y, c, bw, bd, z, r, ara, renk, cerceve='beyaz', atla=None):
    """painted discs (chalchihuitl) along the four faces of a band (half sizes bw, bd round c) at height z; renk(p) gives
    the key for the disc at p; atla(p) True: no disc there (behind a stair)"""
    cx, cy = c
    kose = dikdortgen(cx - bw, cx + bw, cy - bd, cy + bd)
    for i in range(4):
        a, b = kose[i], kose[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        m = max(1, int(L / ara))
        for k in range(m):
            p = a.lerp(b, (k + 0.5) / m)
            if atla and atla(p): continue
            y.oculus(p + nn * 0.0006 + Z * z, e, nn, r, renk(p), cerceve, f=r * 0.35, k=10)


def alfarda_merdiven(y, cx, y_bas, y_son, z0, z1, en, n=None, key='siva', alf_key='siva', alf_en=0.035, dado=0.14,
                     dado_h=0.04, sol=True, sag=True, hh=0.026, basamak_key=None):
    """a Mesoamerican stair climbing towards +y: steps from y_bas (on the ground at z0) to y_son (at z1), en wide,
    each step a block from the ground (riser key, tread basamak_key); a balustrade (alfarda) on either side (sol / sag)
    whose top follows the slope hh above the nosings and, in the last dado share of the run, steepens into the
    upright dado block standing dado_h above the top. Returns the balustrades' foot centres"""
    n = n or max(6, int((z1 - z0) / 0.021))
    run = y_son - y_bas
    for k in range(n):
        ya = y_bas + run * k / n
        zt = z0 + (z1 - z0) * (k + 1) / n
        yz = ('on' + ('' if sol else 'sol') + ('' if sag else 'sag'))
        kutu(y, V(cx - en / 2, ya, z0), X, en, run / n, zt - z0, key, yz)
        y.yuz_yon([V(cx - en / 2, ya, zt), V(cx + en / 2, ya, zt), V(cx + en / 2, ya + run / n, zt), V(cx - en / 2, ya + run / n, zt)],
                  basamak_key or key, Z)
    zs = lambda yy: z0 + (z1 - z0) * (yy - y_bas) / run
    yd = y_son - run * dado
    ayak = []
    for sx, var in ((-1, sol), (1, sag)):
        if not var: continue
        xa = cx + en / 2 if sx > 0 else cx - en / 2 - alf_en
        prof = [(y_bas - 0.012, z0), (y_son, z0), (y_son, z1 + dado_h), (yd + run * dado * 0.3, z1 + dado_h),
                (yd, zs(yd) + hh), (y_bas - 0.012, z0 + hh)]
        levha(y, V(xa + alf_en, 0, 0), Y, prof, alf_en, alf_key)
        ayak.append(V(xa + alf_en / 2, y_bas - 0.012))
    return ayak


# ---------------------------------------------------------------- merlons, braziers, thatch
ALMENA = [(0, 0), (1, 0), (1, 0.42), (0.78, 0.42), (0.78, 0.7), (0.62, 0.7), (0.62, 1.0), (0.38, 1.0), (0.38, 0.7),
          (0.22, 0.7), (0.22, 0.42), (0, 0.42)]                       # stepped (cloud / fret) merlon
SALYANGOZ = [(0, 0), (1, 0), (1, 0.55), (0.82, 0.8), (0.58, 0.95), (0.5, 1.0), (0.42, 0.95), (0.18, 0.8), (0, 0.55)]   # cut shell


def almenalar(y, a, b, z, h, kalin=0.008, key='siva', en=None, bosluk=None, bicim=ALMENA):
    """a row of merlons along a->b (their face on the line facing its right), h high"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-6: return
    e = (b - a) / L
    w = en or h * 0.8; g = bosluk or h * 0.28
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g
    for i in range(k):
        levha(y, a + e * (i * (w + g)) + Z * z, e, [(p[0] * w, p[1] * h) for p in bicim], kalin, key)


def almena_halka(y, kose, z, h, kalin=0.008, key='siva', en=None, bosluk=None, bicim=ALMENA):
    for i in range(len(kose)):
        almenalar(y, kose[i], kose[(i + 1) % len(kose)], z, h, kalin, key, en, bosluk, bicim)


def mangal(y, x, yy, z, s=0.05, key='siva_oker', bant='boya_kirmizi', ates=True):
    """a standing clay brazier (an hourglass with a flared bowl, a painted band) with a fire; s its height"""
    c = (x, yy)
    donel(y, c, [(0, z), (s * 0.34, z), (s * 0.36, z + s * 0.06), (s * 0.2, z + s * 0.3), (s * 0.2, z + s * 0.5)], key, n=10)
    donel(y, c, [(s * 0.2, z + s * 0.5), (s * 0.3, z + s * 0.56), (s * 0.3, z + s * 0.68), (s * 0.2, z + s * 0.68)], bant, n=10)
    donel(y, c, [(s * 0.2, z + s * 0.68), (s * 0.44, z + s * 0.92), (s * 0.46, z + s), (s * 0.36, z + s * 0.96), (0, z + s * 0.93)], key, n=10)
    if ates:
        for k, (dx, dy, hh, kk) in enumerate(((0, 0, 0.55, 'boya_sari'), (s * 0.12, s * 0.06, 0.35, 'boya_kirmizi'),
                                             (-s * 0.1, -s * 0.08, 0.4, 'boya_kirmizi'))):
            donel(y, (x + dx, yy + dy), [(s * (0.22 - 0.06 * k), z + s * 0.93), (s * 0.12, z + s * (0.93 + hh * 0.5)), (0, z + s * (0.93 + hh))], kk, n=6,
                  kat=k * 0.7)


def saz_konik(y, c, r, z, h, kat=4, keys=('saz', 'saz_koyu'), n=28, sacak=0.03, kalin=0.014, alt_key='ahsap_koyu', tepe='altin'):
    """a tiered conical thatch roof: kat overlapping cones from the eave radius r + sacak at z up to the apex at z + h,
    each tier's lip a thick edge; tepe: a key for a finial knob (None: none). Returns the apex z"""
    R = r + sacak
    for k in range(kat):
        t0, t1 = k / kat, (k + 1) / kat
        ra, rb = R * (1 - t0), R * (1 - t1)
        za, zb = z + h * t0, z + h * t1
        lip = kalin * (1 - 0.3 * t0)
        pr = [(ra * 0.9 if k else r * 0.97, za + (lip if k else 0)), (ra + lip * 0.5, za - lip * 0.5 + (lip if k else 0)),
              (rb, zb + lip)]
        if k == kat - 1: pr[-1] = (0.0, z + h)
        donel(y, c, pr, keys[k % len(keys)], n=n, kat=TAU / n * 0.5 * (k % 2))
        if k == 0:
            y.yuz_yon([V(p.x, p.y, z) for p in cokgen(c, r * 0.97, n)], alt_key, -Z)
    if tepe:
        donel(y, c, [(0.0, z + h - 0.02), (0.012, z + h - 0.01), (0.013, z + h + 0.008), (0.005, z + h + 0.02), (0.0, z + h + 0.026)], tepe, n=10)
        return z + h + 0.026
    return z + h


# ---------------------------------------------------------------- serpents, skulls
def kama(y, x0, x1, b, f, key, keys=None, yc=0.0, alt=False):
    """a block tapered along x: at x0 half width b[0] from z b[1] to b[2], at x1 f likewise, centred on y = yc;
    keys: per-face keys {'on', 'arka', 'ust', 'alt', 'yan'}; alt: close the bottom too"""
    k = keys or {}
    A = [V(x0, yc - b[0], b[1]), V(x0, yc + b[0], b[1]), V(x0, yc + b[0], b[2]), V(x0, yc - b[0], b[2])]
    B = [V(x1, yc - f[0], f[1]), V(x1, yc + f[0], f[1]), V(x1, yc + f[0], f[2]), V(x1, yc - f[0], f[2])]
    y.yuz_yon(A, k.get('arka', key), -X)
    y.yuz_yon(B, k.get('on', key), X)
    y.yuz_yon([A[3], A[2], B[2], B[3]], k.get('ust', key), Z)
    if alt: y.yuz_yon([A[0], A[1], B[1], B[0]], k.get('alt', key), -Z)
    y.yuz_yon([A[0], A[3], B[3], B[0]], k.get('yan', key), -Y)
    y.yuz_yon([A[1], A[2], B[2], B[1]], k.get('yan', key), Y)


def yilan_basi(y, p, aci, s=0.06, key='kirec', agiz='boya_kirmizi', pul='turkuaz', dis='beyaz', goz='koyu', tuy=None):
    """a carved serpent head (at the foot of a balustrade, on a platform's corner) looking towards angle aci, its jaws
    open: a heavy cranium tapering to the snout, big round eyes at its front corners under projecting brow plates,
    curled nose scrolls, the red mouth with two great fangs above and two below, a forked tongue lolling out, rows of
    scale plates (pul) on its crown and cheeks; tuy: a key for a feather crest (Quetzalcoatl). s its length"""
    sade = s < 0.06                     # small heads (along a wall): no cheek plates, coarser balls
    with parca(y, (p[0], p[1], p[2] if len(p) > 2 else 0), aci, s):
        ust = lambda x: 0.78 + (x + 0.5) / 0.62 * 0.06          # the crown's height along the cranium
        yar = lambda x: 0.40 - (x + 0.5) / 0.62 * 0.03          # its half width
        kama(y, -0.5, 0.12, (0.40, 0.0, 0.78), (0.37, 0.0, 0.84), key)                                       # cranium
        kama(y, 0.08, 0.62, (0.34, 0.36, 0.62), (0.27, 0.40, 0.56), key, {'alt': agiz}, alt=True)           # upper jaw
        kama(y, 0.08, 0.56, (0.32, 0.0, 0.18), (0.24, 0.0, 0.12), key, {'ust': agiz})                       # lower jaw
        y.yuz_yon([V(0.123, -0.33, 0.18), V(0.123, 0.33, 0.18), V(0.123, 0.33, 0.36), V(0.123, -0.33, 0.36)], agiz, X)   # the throat
        for sg in (-1, 1):
            # two great fangs from the upper jaw, two from the lower, small teeth between
            kesik(y, (0.52, sg * 0.19), 0.11, 0.1, 0.02, 0.02, 0.41, 0.14, dis, ust=False, alt=True)
            kesik(y, (0.46, sg * 0.15), 0.08, 0.08, 0.015, 0.015, 0.17, 0.33, dis, ust=False)
            for k in range(2):
                kesik(y, (0.34 - k * 0.12, sg * 0.27), 0.05, 0.05, 0.012, 0.012, 0.38, 0.29, dis, ust=False, alt=True)
            # big round eyes at the cranium's front corners (seen from ahead and from the side) under brow plates
            kure(y, (0.15, sg * 0.23, 0.745), 0.125, 'beyaz', n=8 if sade else 10, kat=4 if sade else 5)
            kure(y, (0.25, sg * 0.255, 0.75), 0.062, goz, n=6, kat=3)
            kama(y, -0.04, 0.22, (0.12, 0.84, 0.89), (0.15, 0.85, 0.95), pul, yc=sg * 0.23)
            # nose scrolls curling up from the snout's tip
            boru(y, [V(0.6, sg * 0.13, 0.5), V(0.67, sg * 0.13, 0.57), V(0.64, sg * 0.13, 0.66), V(0.56, sg * 0.13, 0.66), V(0.53, sg * 0.13, 0.6)],
                 0.04, key, n=4)
        # forked tongue
        boru(y, [V(0.15, 0, 0.19), V(0.5, 0, 0.17), V(0.74, 0, 0.1)], 0.04, agiz, n=4)
        for sg in (-1, 1):
            boru(y, [V(0.74, 0, 0.1), V(0.88, sg * 0.09, 0.05)], 0.03, agiz, n=4, r_son=0.008)
        # scale plates: crown rows (alternating), plates along the cheeks
        for i in range(4):
            for j in range(3):
                x = -0.42 + i * 0.13
                kutu_merkez(y, (x, (j - 1) * 0.22), 0.1, 0.16, 0.035, pul if (i + j) % 2 == 0 else key, z0=ust(x) - 0.012)
        if not sade:
            for sg in (-1, 1):
                for i in range(3):
                    for r_ in range(2):
                        if (i + r_) % 2: continue
                        x = -0.38 + i * 0.16
                        kutu_merkez(y, (x, sg * yar(x)), 0.12, 0.04, 0.12, pul, z0=0.12 + r_ * 0.2)
        if tuy:
            for k in range(7):
                t = (k - 3) * 0.24
                boru(y, [V(-0.36, math.sin(t) * 0.22, 0.8), V(-0.6, math.sin(t) * 0.48, 1.04), V(-0.82, math.sin(t) * 0.62, 0.98)], 0.06,
                     tuy if k % 2 else pul, n=4, r_son=0.02)


def kafatasi(y, p, r, key='beyaz', goz='koyu', yon=(0, -1)):
    """a small skull (a ball with a jaw block and two dark sockets facing yon)"""
    p = Vector(p); d = V(yon[0], yon[1]).normalized(); sd = Z.cross(d)
    kure(y, p, r, key, n=6, kat=4)
    kutu_merkez(y, (p.x + d.x * r * 0.35, p.y + d.y * r * 0.35), r * 1.1, r * 1.1, r * 0.7, key, z0=p.z - r * 1.15, aci=math.atan2(d.y, d.x))
    for sg in (-1, 1):
        q = p + d * (r * 0.93) + sd * (sg * r * 0.38) + Z * (r * 0.05)
        y.yuz_yon([q + sd * (-r * 0.22) - Z * (r * 0.22), q + sd * (r * 0.22) - Z * (r * 0.22), q + sd * (r * 0.22) + Z * (r * 0.22),
                   q + sd * (-r * 0.22) + Z * (r * 0.22)], goz, d)


def tzompantli(y, x, yy, z, L, aci=0.0, satir=4, adim=0.022, h=0.13, taban_h=0.035, taban_key='kirec', key='ahsap', kafa='beyaz', tohum=3):
    """a skull rack on a stone platform with a skull relief: upright posts, horizontal poles strung with skulls, facing
    -y (then turned by aci); L its length. Returns the top z"""
    import random
    rn = random.Random(tohum)
    with parca(y, (x, yy, z), aci):
        D = 0.1
        kutu_merkez(y, (0, 0), L + 0.04, D + 0.04, taban_h, taban_key)
        kornis(y, -(L + 0.04) / 2, (L + 0.04) / 2, -(D + 0.04) / 2, (D + 0.04) / 2, taban_h - 0.006, 0.006, 0.004, taban_key)
        # the platform's carved skulls (a row of white skull faces on its front and back)
        m = int(L / 0.03)
        for sy in (-1, 1):
            for k in range(m):
                u = -L / 2 + (k + 0.5) * L / m
                kafatasi(y, (u, sy * ((D + 0.04) / 2 + 0.002) - sy * 0.006, taban_h * 0.55), taban_h * 0.24, kafa, 'koyu', (0, sy))
        zb = taban_h
        np_ = max(2, int(L / 0.12)) + 1
        dikme = [-L / 2 + L * k / (np_ - 1) for k in range(np_)]
        for u in dikme:   # upright posts, two rows (front and back racks)
            for sy in (-1, 1):
                kutu_merkez(y, (u, sy * D * 0.25), 0.009, 0.009, h, key, z0=zb)
        for sy in (-1, 1):   # the top beams
            cubuk(y, V(-L / 2 - 0.008, sy * D * 0.25, zb + h + 0.004), V(L / 2 + 0.008, sy * D * 0.25, zb + h + 0.004), 0.009, key)
        nk = int(L / adim)
        for r_ in range(satir):
            zr = zb + h * (0.2 + 0.7 * r_ / max(1, satir - 1))
            for sy in (-1, 1):
                yp = sy * D * 0.25
                cubuk(y, V(-L / 2, yp, zr), V(L / 2, yp, zr), 0.0032, key)
                # skulls pierced through the temples, strung along the pole, facing out
                for k in range(nk):
                    u = -L / 2 + (k + 0.5) * L / nk
                    if any(abs(u - d) < 0.008 for d in dikme): continue
                    p = V(u + rn.uniform(-0.0012, 0.0012), yp, zr - 0.001)
                    kure(y, p, 0.0078, kafa, n=5, kat=3)
                    q = p + V(0, sy * 0.006, -0.001)
                    for sg in (-1, 1):
                        y.yuz_yon([q + V(sg * 0.0024 - 0.0011, 0, -0.0011), q + V(sg * 0.0024 + 0.0011, 0, -0.0011),
                                   q + V(sg * 0.0024 + 0.0011, 0, 0.0011), q + V(sg * 0.0024 - 0.0011, 0, 0.0011)], 'koyu', V(0, sy, 0))
    return z + taban_h + h + 0.01


# ---------------------------------------------------------------- shrines, figures
def kisi(y, x, yy, z, aci, boy=0.045, ten='kiremit', giysi='beyaz', sac='koyu', kol='yan', bas=None, pelerin=None, egim=0.0, adim=0.4):
    """a small figure facing angle aci, boy high: legs, a loincloth / kilt (giysi), bare or painted torso (ten), head with
    hair; kol: 'yan' arms down, 'kalk' both raised, 'one' reaching forward, 'asa' a staff; bas: a key for a headdress
    (a tuft of feathers); pelerin: a key for a cloak hanging down the back"""
    s = boy / 0.045
    with parca(y, (x, yy, z), aci, s):
        hip = V(0.0, 0, 0.021)
        cubuk(y, V(0.004 * adim, 0.0035, 0.0), hip + V(0, 0.003, 0), 0.0045, ten)
        cubuk(y, V(-0.004 * adim, -0.0035, 0.0), hip + V(0, -0.003, 0), 0.0045, ten)
        omuz = hip + V(egim * 0.014, 0, 0.016 - egim * 0.004)
        kutu_merkez(y, (hip.x + egim * 0.002, 0), 0.011, 0.013, 0.009, giysi, z0=hip.z - 0.006)
        cubuk(y, hip + V(0, 0, 0.003), omuz, 0.0105, ten, 0.007)
        if pelerin:
            # a thin closed slab (open edges showed the inner sheet's back)
            O = [omuz + V(-0.0045, -0.007, 0.001), omuz + V(-0.0045, 0.007, 0.001), V(-0.007, 0.008, 0.006), V(-0.007, -0.008, 0.006)]
            I = [omuz + V(-0.0033, -0.007, 0.001), omuz + V(-0.0033, 0.007, 0.001), V(-0.0058, 0.008, 0.006), V(-0.0058, -0.008, 0.006)]
            y.yuz_yon(O, pelerin, -X)
            y.yuz_yon(I, pelerin, X)
            y.yuz_yon([O[0], O[3], I[3], I[0]], pelerin, -Y)
            y.yuz_yon([O[1], O[2], I[2], I[1]], pelerin, Y)
            y.yuz_yon([O[3], O[2], I[2], I[3]], pelerin, -Z)
            y.yuz_yon([O[0], O[1], I[1], I[0]], pelerin, Z)
        bas_ = omuz + V(egim * 0.004, 0, 0.0065)
        kure(y, bas_, 0.0045, ten, n=8, kat=4)
        kure(y, bas_ + V(-0.0012, 0, 0.0012), 0.0042, sac, n=8, kat=4)
        if bas:
            for k in range(5):
                t = (k - 2) * 0.35
                boru(y, [bas_ + V(-0.001, 0, 0.004), bas_ + V(-0.003, math.sin(t) * 0.006, 0.012 + 0.002 * math.cos(t))], 0.0018, bas, n=4, r_son=0.0008)
        for sg in (-1, 1):
            o = omuz + V(0, sg * 0.0062, -0.001)
            if kol == 'kalk':
                cubuk(y, o, o + V(0.003, sg * 0.004, 0.013), 0.0032, ten)
            elif kol == 'one':
                cubuk(y, o, o + V(0.012, -sg * 0.001, -0.004), 0.0032, ten)
            elif kol == 'asa' and sg > 0:
                cubuk(y, o, o + V(0.009, 0.002, -0.006), 0.0032, ten)
                cubuk(y, o + V(0.01, 0.003, -0.022), o + V(0.01, 0.003, 0.016), 0.0022, 'ahsap')
            else:
                cubuk(y, o, o + V(0.002, sg * 0.001, -0.014), 0.0032, ten)


def dikdortgen_kapi(y, a, b, z0, H, u0, u1, v1, duvar, koyu='koyu', cerceve=None, derin=0.02, esik=None):
    """a wall a->b (facing its right) with a square-headed doorway u0..u1 (0..1 along), v1 high (from z0), dark inside;
    cerceve = (width, key): a raised painted frame"""
    W, e, nc, L = dikdortgen_acik(y, a, b, z0, H, u0, u1, 0.0, v1, (duvar, duvar, esik or duvar, koyu), derin=derin, cerceve=cerceve)
    return W, e, nc, L
