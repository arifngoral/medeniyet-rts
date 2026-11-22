# More shared helpers for the Carthaginian landmarks lm_morboya, lm_kartacasur, lm_tanit, lm_hannibalkamp (not a
# building). On top of parcalar.py and kartaca_ortak.py: closed ellipsoids, a stylised war elephant and horse, dye
# cauldrons and vats, cloth hung to dry, a stake palisade, Tophet stelae, army tents (Carthaginian ridge tent,
# Numidian mapalia hut) and campfires.
import math, random
from mathutils import Vector
from parcalar import *
from kartaca_ortak import levha_kapali, prizma2, tanit_kabartma, insan


def elipsoid(y, c, rx, ry, rz, key, n=10, kat=6, aci=0.0, egim=0.0, ust_yari=False):
    """a closed ellipsoid centred at c (x, y, z), radii rx (along aci), ry, rz; egim pitches it (the +x end up);
    ust_yari: only the upper half, open at the bottom (a hut on the ground)"""
    cx, cy, cz = c
    ca, sa, ce, se = math.cos(aci), math.sin(aci), math.cos(egim), math.sin(egim)
    k0 = kat // 2 if ust_yari else 0

    def P(k, i):
        ph = -math.pi / 2 + math.pi * k / kat
        t = TAU * i / n
        lx, ly, lz = rx * math.cos(ph) * math.cos(t), ry * math.cos(ph) * math.sin(t), rz * math.sin(ph)
        lx, lz = lx * ce - lz * se, lx * se + lz * ce
        return V(cx + ca * lx - sa * ly, cy + sa * lx + ca * ly, cz + lz)
    C = V(cx, cy, cz)
    for k in range(k0, kat):
        for i in range(n):
            j = (i + 1) % n
            if k == 0: q = [P(0, 0), P(1, j), P(1, i)]
            elif k == kat - 1: q = [P(k, i), P(k, j), P(kat, 0)]
            else: q = [P(k, i), P(k, j), P(k + 1, j), P(k + 1, i)]
            yuz_dis(y, q, key, C - V(0, 0, rz * 0.5) if ust_yari else C)


def ic_halka(y, c, r, z0, z1, key, n=12):
    """the inside of a round rim (faces the axis)"""
    A = cokgen(c, r, n, z=z0); B = cokgen(c, r, n, z=z1)
    for i in range(n):
        j = (i + 1) % n
        q = [A[i], A[j], B[j], B[i]]
        m = sum(q, Vector()) / 4
        y.yuz_yon(q, key, V(c[0] - m.x, c[1] - m.y, 0))


# ---------------------------------------------------------------- animals
def fil(y, x, yy, z, aci=0.0, s=1.0, key='fil', ortu=None, binici=None, kule=None, hortum=0.0):
    """a stylised (North African forest) war elephant facing aci, ~0.085 tall at s 1: body, legs, head, big ears,
    trunk (hortum > 0 raises it), tusks, tail; ortu a saddle-cloth key, binici a mahout's robe key, kule a key for a
    small fighting tower on its back"""
    with parca(y, (x, yy, z), aci, s):
        elipsoid(y, (0, 0, 0.054), 0.05, 0.029, 0.03, key, n=12, kat=6)
        for lx in (-0.03, 0.028):
            for ly in (-0.016, 0.016):
                donel(y, (lx, ly), [(0.0098, 0.0), (0.0092, 0.004), (0.0085, 0.032), (0.0088, 0.046), (0.0, 0.05)], key, n=7)
        elipsoid(y, (0.052, 0, 0.066), 0.021, 0.02, 0.024, key, n=10, kat=6, egim=0.3)
        for sg in (-1, 1):   # ears: thin closed flaps behind the head
            levha_kapali(y, [V(0.04, sg * 0.021, 0.08), V(0.026, sg * 0.034, 0.083), V(0.018, sg * 0.04, 0.064),
                             V(0.026, sg * 0.036, 0.046), V(0.042, sg * 0.022, 0.05)], key, V(0.25, sg, 0), 0.0025)
        h = hortum
        boru(y, [V(0.068, 0, 0.058), V(0.08, 0, 0.044 + h * 0.01), V(0.086 + h * 0.012, 0, 0.026 + h * 0.03), V(0.09 + h * 0.02, 0, 0.01 + h * 0.05)],
             0.0062, key, n=6, r_son=0.0028)
        for sg in (-1, 1):
            boru(y, [V(0.064, sg * 0.01, 0.05), V(0.079, sg * 0.013, 0.038), V(0.092, sg * 0.011, 0.043)], 0.0024, 'beyaz', n=5, r_son=0.001)
            kure(y, (0.067, sg * 0.016, 0.074), 0.0028, 'koyu', n=5, kat=3)   # eyes
        boru(y, [V(-0.049, 0, 0.064), V(-0.056, 0, 0.045), V(-0.057, 0, 0.032)], 0.0015, key, n=4)
        if ortu:   # a saddle-cloth: a flat top sheet and two side flaps tucked under its edges (closed thin sheets)
            levha_kapali(y, [V(-0.032, -0.014, 0.0872), V(0.01, -0.014, 0.0872), V(0.01, 0.014, 0.0872), V(-0.032, 0.014, 0.0872)], ortu, Z, 0.0022)
            for sg in (-1, 1):
                q = [V(-0.032, sg * 0.0115, 0.0843), V(0.01, sg * 0.0115, 0.0843), V(0.01, sg * 0.032, 0.055), V(-0.032, sg * 0.032, 0.055)]
                levha_kapali(y, q, ortu, V(0, sg, 0.8), 0.0022)
        if kule:   # a small wooden fighting tower (howdah)
            kutu_merkez(y, (-0.004, 0), 0.034, 0.03, 0.022, kule, z0=0.084)
            for sx in (-1, 1):
                for sy in (-1, 1):
                    y.prizma((-0.004 + sx * 0.015, sy * 0.013), 0.0015, 0.106, 0.118, 'ahsap_koyu', n=4, ust=False)
            kutu_merkez(y, (-0.004, 0), 0.036, 0.032, 0.003, kule, z0=0.118)
        if binici:
            insan(y, 0.035, 0, 0.074, binici, s=0.75)


def at(y, x, yy, z, aci=0.0, s=1.0, key='ahsap', yele='koyu', eger=None, binici=None, bas_egik=0.0):
    """a stylised horse facing aci, ~0.08 tall at the head at s 1: barrel, legs, neck, head, mane, tail; eger a
    saddle-cloth key, binici a rider's robe key; bas_egik > 0 lowers the head (grazing)"""
    with parca(y, (x, yy, z), aci, s):
        elipsoid(y, (0, 0, 0.05), 0.032, 0.0115, 0.014, key, n=10, kat=6)
        for lx in (-0.022, 0.021):
            for ly in (-0.0065, 0.0065):
                cubuk(y, V(lx, ly, 0.05), V(lx + (0.002 if lx > 0 else -0.002), ly, 0.0), 0.0055, key, 0.0055)
                kutu_merkez(y, (lx + (0.002 if lx > 0 else -0.002), ly), 0.0065, 0.0062, 0.004, yele)   # hooves
        b = bas_egik
        nz, hz = 0.066 - b * 0.035, 0.07 - b * 0.05
        boru(y, [V(0.022, 0, 0.054), V(0.036, 0, nz)], 0.0068, key, n=6, r_son=0.005)
        elipsoid(y, (0.043, 0, hz - 0.006), 0.012, 0.0052, 0.0058, key, n=8, kat=4, egim=-0.85 - b * 0.5)
        boru(y, [V(0.02, 0, 0.064), V(0.033, 0, nz + 0.004)], 0.003, yele, n=4, kapat=True)   # mane
        for sg in (-1, 1):
            boru(y, [V(0.036, sg * 0.003, hz - 0.002), V(0.035, sg * 0.0035, hz + 0.005)], 0.0016, key, n=3, r_son=0.0005)
        boru(y, [V(-0.031, 0, 0.056), V(-0.039, 0, 0.045), V(-0.04, 0, 0.03)], 0.0026, yele, n=4, r_son=0.0012)
        if eger:
            levha_kapali(y, [V(-0.01, -0.006, 0.0668), V(0.012, -0.006, 0.0668), V(0.012, 0.006, 0.0668), V(-0.01, 0.006, 0.0668)], eger, Z, 0.0018)
            for sg in (-1, 1):
                levha_kapali(y, [V(-0.01, sg * 0.0045, 0.0655), V(0.012, sg * 0.0045, 0.0655), V(0.012, sg * 0.0135, 0.048), V(-0.01, sg * 0.0135, 0.048)], eger, V(0, sg, 1.2), 0.0018)
        if binici:
            insan(y, -0.002, 0, 0.058, binici, s=0.8)


# ---------------------------------------------------------------- dye works
def kazan(y, cx, cy, z, r=0.035, sivi='boya_mor', ocak='tas_koyu', buhar=3, tohum=0):
    """a bronze dye cauldron on a stone hearth with a fire mouth; the liquid a little below the rim; buhar: steam
    puffs rising (white blobs). Returns the rim z"""
    g = random.Random(tohum)
    hh = r * 0.8
    y.prizma((cx, cy), r * 1.2, z, z + hh, ocak, n=8, kat=math.pi / 8)
    halka_kornis(y, (cx, cy), r * 1.2, z + hh - 0.006, 0.006, 0.004, 8, 'tas_acik', kat=math.pi / 8)
    a = g.uniform(0, TAU)   # the fire mouth
    d = V(math.cos(a), math.sin(a)); e = V(-d.y, d.x)
    ap = r * 1.2 * math.cos(math.pi / 8)
    o = V(cx, cy, z) + d * ap
    kutu(y, o - e * (r * 0.3) + d * 0.0012, e, r * 0.6, 0.008, hh * 0.5, 'boya_sari', 'onsagsolust')
    kutu(y, o - e * (r * 0.2) + d * 0.0024 + Z * 0.002, e, r * 0.4, 0.008, hh * 0.3, 'boya_kirmizi', 'onsagsolust')
    zb = z + hh
    donel(y, (cx, cy), [(r * 0.6, zb), (r * 0.95, zb + r * 0.32), (r * 1.04, zb + r * 0.62), (r * 1.1, zb + r * 0.7),
                        (r * 0.96, zb + r * 0.7), (r * 0.93, zb + r * 0.56)], 'bronz', n=12)
    donel(y, (cx, cy), [(r * 0.93, zb + r * 0.56), (0, zb + r * 0.56)], sivi, n=12)
    zt = zb + r * 0.7
    if buhar:   # steam: a low soft cloud over the liquid, rising and thinning
        yx, yy_ = g.uniform(0.35, 0.6), g.uniform(0.1, 0.4)
        for k in range(2):   # two strands of different height, leaning the same way
            a = g.uniform(0, TAU)
            duman(y, cx + r * 0.35 * math.cos(a) * (1 - 2 * k), cy + r * 0.35 * math.sin(a) * (1 - 2 * k), zb + r * 0.58, r * (0.42 - 0.1 * k),
                  buhar + 1 - k, 'buhar', tohum * 7 + k, (yx, yy_))
    return zt


def tekne(y, cx, cy, z, w, d, h, sivi='boya_mor', key='tas', aci=0.0, kenar=0.007, derin=0.012):
    """a raised rectangular dye vat (w x d, h high on z): outer sides, the rim, the inner sides down to the liquid"""
    with parca(y, (cx, cy, z), aci):
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        duvarlar(y, k, 0, h, key)
        ic = disa(k, -kenar)
        for i in range(4):
            j = (i + 1) % 4
            y.yuz_yon([k[i] + Z * h, k[j] + Z * h, ic[j] + Z * h, ic[i] + Z * h], 'tas_acik', Z)
            duz_duvar(y, ic[j], ic[i], h - derin, h, key)
        y.yuz_yon([V(p.x, p.y, h - derin) for p in ic], sivi, Z)


def kumas_as(y, a, b, z, h, renkler, n=3, tohum=0, sarkma=0.75):
    """a drying rack: two posts a, b, a bar on top (z + h) and n pleated cloths hanging from it (closed thin sheets,
    keys from renkler in turn), a little different in length"""
    g = random.Random(tohum)
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    for p in (a, b):
        cubuk(y, p + Z * z, p + Z * (z + h + 0.008), 0.0055, 'ahsap')
        cubuk(y, p - e * 0.012 + Z * z, p + Z * (z + h * 0.45), 0.0035, 'ahsap_koyu')   # a brace
    cubuk(y, a - e * 0.006 + Z * (z + h), b + e * 0.006 + Z * (z + h), 0.0045, 'ahsap_acik')
    gap = 0.004
    cw = (L - 0.012 - gap * (n - 1)) / n
    for i in range(n):
        u0 = 0.006 + i * (cw + gap)
        hl = h * sarkma * g.uniform(0.75, 1.0)
        key = renkler[(i + tohum) % len(renkler)]
        np_ = 3
        for k in range(np_):
            p0 = a + e * (u0 + cw * k / np_) + nc * (0.0035 * (k % 2))
            p1 = a + e * (u0 + cw * (k + 1) / np_) + nc * (0.0035 * ((k + 1) % 2))
            zt = z + h - 0.003
            pts = [p0 + Z * (zt - hl), p1 + Z * (zt - hl), p1 + Z * zt, p0 + Z * zt]
            dd = p1 - p0; nn = V(dd.y, -dd.x)
            levha_kapali(y, pts, key, nn, 0.0016)


def kabuk_tepe(y, cx, cy, z, R, H, key='kabuk', n=22, nr=7, tohum=0, Ry=None, kabuk_say=None):
    """a heap of crushed shells: a lumpy radial heightfield (its foot a hair below z), an apex"""
    g = random.Random(tohum)
    Ry = Ry or R
    fz = [g.uniform(0, TAU) for _ in range(3)]
    fz += [g.uniform(0, TAU) for _ in range(3)]

    def r_h(t, k):
        rr = k / nr
        bump = 1 + 0.12 * math.sin(3 * t + fz[0]) + 0.07 * math.sin(5 * t + fz[1]) + 0.05 * math.sin(8 * t + fz[2])
        lump = 0.028 * math.sin(11 * t + 2.3 * k + fz[3]) + 0.018 * math.sin(17 * t - 3.1 * k + fz[4]) + 0.01 * math.sin(29 * t + 5 * k)
        hh = H * (1 - rr ** 2.1) * (1 + lump * min(1.0, rr * 3))
        return rr * bump, hh
    rings = []
    for k in range(nr + 1):
        ring = []
        for i in range(n):
            t = TAU * i / n
            rr, hh = r_h(t, nr - k)
            ring.append(V(cx + R * rr * math.cos(t), cy + Ry * rr * math.sin(t), z - 0.004 + hh if k else z - 0.006))
        rings.append(ring)
    for k in range(nr):
        for i in range(n):
            j = (i + 1) % n
            q = [rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]]
            if k == nr - 1: q = [rings[k][i], rings[k][j], V(cx, cy, z - 0.004 + H)]
            y.yuz_yon(q, key, Z)
    # loose shells on the slopes: small spiky knobs
    for m in range(kabuk_say if kabuk_say is not None else int(R * 160)):
        t = g.uniform(0, TAU); k = g.uniform(1.2, nr - 0.8)
        k0 = int(k); f = k - k0          # (on the mesh's own facet: between the two rings, not on a finer curve)
        (r0, h0), (r1, h1) = r_h(t, k0), r_h(t, k0 + 1)
        rr, hh = r0 + (r1 - r0) * f, h0 + (h1 - h0) * f
        p = V(cx + R * rr * math.cos(t), cy + Ry * rr * math.sin(t), z - 0.004 + hh)
        s = g.uniform(0.8, 1.4)
        donel(y, (p.x, p.y), [(0.0, p.z - 0.004), (0.0055 * s, p.z), (0.0032 * s, p.z + 0.006 * s), (0.0, p.z + 0.012 * s)],
              g.choice(('kum_acik', 'kabuk', 'boya_mor_acik', 'kum')), n=5)
    return r_h


def duman(y, x, yy, z, r=0.012, n=4, key='duman', tohum=0, yon=(0.4, 0.3)):
    """a rising column of soft smoke / steam: each level a cluster of overlapping lobes (a big one, smaller ones round
    it) that swells a little as it rises and then thins out into a few small wisps, drifting along yon. key 'buhar'
    (steam) / 'duman' (smoke) bake a soft shadow (doku.YUMUSAK_AO)"""
    # one continuous lofted plume (separate balls read as stacked snowmen): rings up a bending axis, the radius
    # swelling into soft bulges and tapering to a wisp at the top
    g = random.Random(tohum)
    h = r * (1.8 + 1.15 * n)
    ph, ph2 = g.uniform(0, TAU), g.uniform(0, TAU)
    dx, dy = yon[0] * h * 0.45, yon[1] * h * 0.45
    m, nr = 12, 10
    hal, mer = [], []
    for k in range(m + 1):
        t = k / m
        c = V(x + dx * t ** 1.4 + r * 0.14 * math.sin(4.0 * t + ph), yy + dy * t ** 1.4 + r * 0.14 * math.cos(3.3 * t + ph), z + h * t)
        rad = r * (0.35 + 0.75 * math.sin(math.pi * min(t, 0.5))) * max(0.0, 1 - t ** 2.2) ** 0.5 * \
            (1 + 0.2 * math.sin(TAU * 2.4 * t + ph2))   # (swelling, then a rounded top, not a needle)
        rad = max(rad, r * 0.06) if k < m else 0.0
        el = 0.82 + 0.12 * math.sin(2.1 * t + ph)
        dn = ph + t * 1.3
        hal.append([c + V(rad * math.cos(TAU * i / nr + dn), rad * el * math.sin(TAU * i / nr + dn), 0) for i in range(nr)])
        mer.append(c)
    alt = V(x, yy, z - r * 0.35)
    for i in range(nr):
        j = (i + 1) % nr
        yuz_dis(y, [hal[0][j], hal[0][i], alt], key, V(x, yy, z + r))
        for k in range(m):
            q = [hal[k][i], hal[k][j], hal[k + 1][j], hal[k + 1][i]] if k < m - 1 else [hal[k][i], hal[k][j], hal[m][0]]
            yuz_dis(y, q, key, (mer[k] + mer[k + 1]) / 2 if k < m - 1 else mer[k])
    ust = mer[-1] + V(dx * 0.15, dy * 0.15, r * 0.6)     # a small puff torn off the top, drifting on
    elipsoid(y, (ust.x, ust.y, ust.z), r * 0.4, r * 0.34, r * 0.27, key, n=8, kat=4, aci=ph)


# ---------------------------------------------------------------- earthworks, palisades
def palisad(y, yol, zf=lambda x, yy: 0.0, h=0.07, aralik=0.017, r=0.0058, key='kutuk', tohum=0, ray=True):
    """sharpened stakes along a polyline, zf(x, y) the ground height; ray: two rails behind (to the left of travel)"""
    g = random.Random(tohum)
    for i in range(len(yol) - 1):
        a, b = V(*yol[i][:2]), V(*yol[i + 1][:2])
        L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
        m = max(1, int(round(L / aralik)))
        for k in range(m + (1 if i == len(yol) - 2 else 0)):
            p = a.lerp(b, k / m)
            z0 = zf(p.x, p.y) - 0.006
            hh = h * g.uniform(0.85, 1.08)
            y.prizma((p.x, p.y), r, z0, z0 + hh, key, n=5, ust=False)
            y.koni((p.x, p.y), r, z0 + hh, r * 3.2, key, n=5)
        if ray:
            for f in (0.3, 0.72):
                pa, pb = a - nc * (r * 1.7), b - nc * (r * 1.7)
                cubuk(y, pa + Z * (zf(a.x, a.y) + h * f), pb + Z * (zf(b.x, b.y) + h * f), 0.005, 'ahsap_koyu', 0.004)


# ---------------------------------------------------------------- the Tophet
def stel(y, x, yy, z, aci=0.0, s=1.0, key='kirec', tur=0, isaret='tas_koyu'):
    """a votive stele facing aci on a small base: tur 0 pointed top, 1 round top, 2 a cippus (block with a small
    cavetto-like cap); the sign of Tanit in low relief on the front (isaret key)"""
    e = V(math.cos(aci), math.sin(aci)); ex = V(-e.y, e.x)
    w, h, d = 0.03 * s, 0.062 * s, 0.011 * s
    kutu_merkez(y, (x, yy), w * 1.35, d * 1.9, 0.008 * s, 'tas_koyu', z0=z, aci=math.atan2(ex.y, ex.x))
    zb = z + 0.008 * s
    o = V(x, yy, zb) - e * (d / 2)
    P = lambda u, v, dd: o + ex * u + Z * v + e * dd
    if tur == 0:
        pts = [(-w / 2, 0), (w / 2, 0), (w / 2, h * 0.78), (0, h), (-w / 2, h * 0.78)]
    elif tur == 1:
        pts = [(-w / 2, 0), (w / 2, 0)] + [(w / 2 * math.cos(math.pi * k / 6), h * 0.8 + w / 2 * math.sin(math.pi * k / 6)) for k in range(7)] + [(-w / 2, 0)]
        pts = pts[:-1]
    else:
        pts = [(-w / 2, 0), (w / 2, 0), (w / 2, h * 0.7), (-w / 2, h * 0.7)]
    prizma2(y, pts, P, d, key, e, arka=True)
    if tur == 2:   # the cippus cap: a wider slab and a small pyramid
        kutu_merkez(y, (x, yy), w * 1.2, d * 1.25, h * 0.08, key, z0=zb + h * 0.7, aci=math.atan2(ex.y, ex.x))
        c = V(x, yy)
        k4 = [c + ex * (sx * w * 0.6) + e * (sy * d * 0.62) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        zt = zb + h * 0.78
        for i in range(4):
            j = (i + 1) % 4
            y.yuz_yon([k4[i] + Z * zt, k4[j] + Z * zt, V(x, yy, zt + h * 0.16)], key, (k4[i] + k4[j]) / 2 - c + Z * 0.3)
    tanit_kabartma(y, o + e * d + ex * 0 + Z * (h * 0.12), ex, e, h * 0.5, isaret, d=0.0012)
    return zb + h


def urn(y, x, yy, z, s=1.0, key='kiremit'):
    """a small clay urn (Tophet burial jar) with a lid"""
    donel(y, (x, yy), [(0.004 * s, z), (0.008 * s, z + 0.006 * s), (0.0085 * s, z + 0.012 * s), (0.005 * s, z + 0.018 * s),
                       (0.0052 * s, z + 0.02 * s), (0.0, z + 0.022 * s)], key, n=8)


# ---------------------------------------------------------------- army camp
def cadir_besik(y, cx, cy, aci, L, W, H, key='kumas', serit=None, kapi='ahsap_koyu', ip=True, duvar=0.22):
    """a ridge tent (a wedge on short walls) L long along aci, W wide, H high: closed cloth, a dark door flap at the
    +aci end, poles at the ridge ends and guy ropes. serit: a key for alternate cloth widths"""
    with parca(y, (cx, cy, 0), aci):
        hw = H * duvar
        kes = [V(0, -W / 2, 0), V(0, -W / 2, hw), V(0, 0, H), V(0, W / 2, hw), V(0, W / 2, 0)]
        ns = 4
        for k in range(ns):
            x0, x1 = -L / 2 + L * k / ns, -L / 2 + L * (k + 1) / ns
            kk = serit if (serit and k % 2) else key
            for i in range(4):
                p, q = kes[i], kes[i + 1]
                m = (p + q) / 2
                y.yuz_yon([V(x0, p.y, p.z), V(x1, p.y, p.z), V(x1, q.y, q.z), V(x0, q.y, q.z)], kk, V(0, m.y, m.z - H * 0.3))
        for sg in (-1, 1):
            y.yuz_yon([V(sg * L / 2, p.y, p.z) for p in kes], key, V(sg, 0, 0))
        # the door: a dark triangle proud of the front end, a flap tied back
        y.yuz_yon([V(L / 2 + 0.0015, -W * 0.16, 0), V(L / 2 + 0.0015, W * 0.16, 0), V(L / 2 + 0.0015, 0, H * 0.72)], kapi, X)
        levha_kapali(y, [V(L / 2 + 0.003, W * 0.02, 0.0), V(L / 2 + 0.003, W * 0.2, 0.0), V(L / 2 + 0.003, W * 0.02, H * 0.62)], serit or key, X, 0.0015)
        for sg in (-1, 1):
            y.prizma((sg * (L / 2 + 0.004), 0), 0.0025, 0, H + 0.016, 'ahsap', n=4)
            if ip:
                cubuk(y, V(sg * (L / 2 + 0.004), 0, H + 0.008), V(sg * (L / 2 + H * 0.9), 0, 0), 0.0018, 'ahsap_koyu')
        if ip:
            for sx in (-0.3, 0.3):
                for sg in (-1, 1):
                    cubuk(y, V(sx * L, sg * W / 2, hw), V(sx * L, sg * (W / 2 + H * 0.55), 0), 0.0016, 'ahsap_koyu')


def mapalia(y, cx, cy, aci, L, W, H, key='saz_koyu', serit='ahsap_acik'):
    """a Numidian mapalia hut: an elongated rounded hut (an upturned boat), hide-covered, with bands and a dark door"""
    elipsoid(y, (cx, cy, 0), L / 2, W / 2, H, key, n=12, kat=8, aci=aci, ust_yari=True)
    e = V(math.cos(aci), math.sin(aci)); s = V(-e.y, e.x)
    for f in (-0.45, 0.0, 0.45):   # bands round the hut
        pts = []
        for k in range(9):
            ph = math.pi * k / 8
            xr = math.sqrt(max(0, 1 - f * f))
            p = V(cx, cy) + e * (f * L / 2) + s * (W / 2 * xr * math.cos(ph) * 1.03)
            pts.append(p + Z * (H * xr * math.sin(ph) * 1.03))
        boru(y, pts, 0.0022, serit, n=4, kapat=True)
    # the door on the long side (-s), leaning with the hut's curve
    c = V(cx, cy)
    b0, b1 = c - s * (W / 2 * 1.012), c - s * (W / 2 * 0.88 + 0.002)
    dw = L * 0.09
    y.yuz_yon([b0 - e * dw, b0 + e * dw, b1 + e * dw * 0.8 + Z * (H * 0.5), b1 - e * dw * 0.8 + Z * (H * 0.5)], 'koyu', -s)


def pon_kule(y, cx, cy, z0, w, d, katlar, kat_h, alt='kum', ust='siva', kornis='siva_krem', mazgal_h=0.026, pencere=2,
             kapi=None, kav_h=None):
    """a Punic tower (w x d): a sandstone ground storey with slits, whitewashed storeys above with framed windows,
    a string course between them, a cavetto cornice and merlons. kapi: a door on the -y face (key). Returns the
    top of the cornice (the roof level) and the merlon top"""
    from kartaca_ortak import kavetto, pencere_kutu
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2)
    z = z0
    for kt in range(katlar):
        key = alt if kt == 0 else ust
        duvarlar(y, k, z, z + kat_h, key)
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            L = (b - a).length; ex = (b - a) / L; nrm = V(ex.y, -ex.x)
            if kt == 0:
                if kapi and i == 0: continue
                for j in range(2):
                    yarik(y, a + Z * z + nrm * 0.001, ex, nrm, L * (j + 1) / 3 - 0.004, kat_h * 0.4, 0.008, kat_h * 0.3, 'koyu')
            else:
                for j in range(pencere):
                    ww = min(0.024, L * 0.12)
                    pencere_kutu(y, a + Z * z, ex, nrm, L * (j + 1) / (pencere + 1) - ww / 2, kat_h * 0.32, ww, kat_h * 0.42, 'koyu', cerceve=kornis)
        if kt < katlar - 1:
            silme(y, k, z + kat_h - 0.004, 0.009, 0.006, kornis, 'duz')
        z += kat_h
    if kapi:
        a, b = k[0], k[1]
        dw = min(0.05, w * 0.3)
        pencere_kutu(y, a + Z * z0, X, -Y, w / 2 - dw / 2, 0.0, dw, kat_h * 0.62, kapi, cerceve=kornis)
    kh = kav_h or min(0.05, w * 0.22)
    kavetto(y, k, z, kh, kh * 0.55, kornis)
    zt = z + kh
    ring = disa(k, kh * 0.5)
    parapet(y, ring, zt, 0.01, mazgal_h, 0.014, ust)
    return zt, zt + 0.01 + mazgal_h


def ates(y, x, yy, z, r=0.02, tohum=0, duman_n=2):
    """a campfire: a ring of stones, crossed logs, a flame and (duman_n) smoke puffs"""
    g = random.Random(tohum)
    for k in range(8):
        a = TAU * k / 8 + g.uniform(-0.15, 0.15)
        kure(y, (x + r * math.cos(a), yy + r * math.sin(a), z + 0.002), 0.0055, g.choice(('kaya', 'kaya_koyu')), n=6, kat=3)
    for k in range(3):
        a = TAU * k / 3 + 0.4
        d = V(math.cos(a), math.sin(a))
        cubuk(y, V(x, yy, z + 0.014) - d * (r * 0.1), V(x, yy, z) + d * (r * 0.85), 0.005, 'ahsap_koyu')
    donel(y, (x, yy), [(r * 0.55, z + 0.002), (r * 0.5, z + 0.012), (r * 0.25, z + 0.03), (0, z + 0.048)], 'boya_kirmizi', n=7)
    donel(y, (x + 0.002, yy), [(r * 0.3, z + 0.008), (r * 0.24, z + 0.03), (r * 0.1, z + 0.05), (0, z + 0.066)], 'boya_sari', n=6)
    if duman_n:
        duman(y, x + 0.006, yy, z + 0.07, 0.0065, duman_n + 1, 'duman', tohum, (1.0, 0.6))


def sfenks(y, x, yy, z, aci=0.0, s=1.0, key='kum_acik', kanat='altin', kaide='kum'):
    """a Phoenician winged sphinx couchant on a moulded base, facing aci (~0.09 tall at s 1): lion body, forepaws,
    a human head with a striped headdress, wings swept up from the shoulders"""
    with parca(y, (x, yy, z), aci, s):
        kutu_merkez(y, (0, 0), 0.1, 0.045, 0.018, kaide)
        silme(y, dikdortgen(-0.05, 0.05, -0.0225, 0.0225), 0.014, 0.006, 0.004, 'kum_acik', 'duz')
        elipsoid(y, (-0.008, 0, 0.034), 0.034, 0.014, 0.016, key, n=10, kat=6)
        elipsoid(y, (0.018, 0, 0.044), 0.013, 0.013, 0.02, key, n=8, kat=5)          # chest
        for sg in (-1, 1):
            cubuk(y, V(0.02, sg * 0.008, 0.024), V(0.046, sg * 0.008, 0.022), 0.007, key, 0.006)     # forepaws
            cubuk(y, V(-0.03, sg * 0.01, 0.022), V(-0.012, sg * 0.012, 0.021), 0.008, key, 0.007)   # hind legs
        kure(y, (0.026, 0, 0.068), 0.0095, key, n=8, kat=5)
        # the headdress: a block behind the face, lappets down to the shoulders
        kutu_merkez(y, (0.022, 0), 0.012, 0.022, 0.016, kanat, z0=0.06)
        for sg in (-1, 1):
            levha_kapali(y, [V(0.03, sg * 0.0095, 0.066), V(0.03, sg * 0.0095, 0.05), V(0.02, sg * 0.0115, 0.048), V(0.019, sg * 0.0115, 0.066)], kanat, V(0, sg, 0), 0.002)
            # the wing: a curved, layered sheet rising from the shoulder
            levha_kapali(y, [V(0.012, sg * 0.012, 0.05), V(-0.028, sg * 0.013, 0.05), V(-0.04, sg * 0.01, 0.086), V(-0.004, sg * 0.009, 0.07)], kanat, V(0, sg, 0), 0.0025)
        boru(y, [V(-0.04, 0, 0.03), V(-0.052, 0.006, 0.024), V(-0.05, 0.012, 0.02)], 0.002, key, n=4)
