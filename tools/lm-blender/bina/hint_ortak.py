# Shared helpers for the Indian landmarks lm_sanchi, lm_filahiri, lm_basamaklikuyu, lm_amberkalesi (not a building:
# imported by those scripts). Rajput / Mughal / early Buddhist details on top of parcalar.py: arc sweeps of a closed
# profile (railings, drums), chhatri kiosks, chhajja eaves, kalasha finials, jharokha balconies, vedika railings,
# lotus mouldings, ellipsoids and stylised elephants with mahouts.
import math
from mathutils import Vector
from parcalar import *
from arap_ortak import adam, sivri_mazgal, mazgalli_kenar

KUM = ('kum', 'kum_koyu', 'kum_acik', 'koyu')               # sandstone wall, reveal, sill, dark back
KIRMIZI = ('kirmizi_tas', 'kirmizi_tas', 'kirmizi_tas_acik', 'koyu')
# chhajja: a thin sloping stone eave: underside from the wall down to the lip, the lip, the top slope back to the wall
CHHAJJA = [(0, 0.55), (1, 0.0), (1, 0.16), (0, 1.0)]


class olcekli:
    """with olcekli(y, merkez, (sx, sy, sz)): faces added inside are scaled about merkez (positive factors keep the
    winding)"""

    def __init__(self, y, merkez, s):
        self.y, self.m, self.s = y, Vector(merkez), s

    def __enter__(self):
        self.bas = len(self.y.faces)
        return self

    def __exit__(self, *e):
        m, (sx, sy, sz) = self.m, self.s
        for i in range(self.bas, len(self.y.faces)):
            pts, key = self.y.faces[i]
            self.y.faces[i] = ([(m.x + (p[0] - m.x) * sx, m.y + (p[1] - m.y) * sy, m.z + (p[2] - m.z) * sz) for p in pts], key)
        return False


def elipsoid(y, c, rx, ry, rz, key, n=12, kat=6):
    """an ellipsoid centred at c (x, y, z)"""
    with olcekli(y, c, (rx / rz, ry / rz, 1.0)):
        kure(y, c, rz, key, n=n, kat=kat)


def yay_kesit(y, c, profil, t0, t1, n, key, uclar=True, keys=None, atla=()):
    """sweep a closed (radius, z) loop round the vertical axis through c from angle t0 to t1 in n steps: the loop must
    run counter-clockwise with the radius to the right (out-face up, top inwards, in-face down, bottom outwards) so the
    faces point out of the solid. uclar: cap the two ends. keys: one key per profile edge (else key). atla: indices of
    profile edges left out (an underside never seen from above)"""
    m = len(profil)
    T = [t0 + (t1 - t0) * i / n for i in range(n + 1)]
    P = lambda k, t: V(c[0] + profil[k][0] * math.cos(t), c[1] + profil[k][0] * math.sin(t), profil[k][1])
    tam = abs(abs(t1 - t0) - TAU) < 1e-6
    for k in range(m):
        if k in atla: continue
        k2 = (k + 1) % m
        kk = keys[k] if keys else key
        for i in range(n):
            a, b = T[i], T[i + 1]
            q = [P(k, a), P(k, b), P(k2, b), P(k2, a)]
            if (q[0] - q[3]).length < 1e-9: q = [q[0], q[1], q[2]]
            elif (q[1] - q[2]).length < 1e-9: q = [q[0], q[1], q[3]]
            if len(q) >= 3:
                y.yuz(q, kk)
    if uclar and not tam:
        for t, s in ((T[0], -1), (T[-1], 1)):
            tg = V(-math.sin(t), math.cos(t)) * s
            y.yuz_yon([P(k, t) for k in range(m)], key, tg)


def halka(y, c, r_dis, r_ic, z0, z1, key, n=48, t0=0.0, t1=TAU, keys=None, atla=()):
    """a closed ring (or arc) of rectangular section: wall drum, terrace edge, railing bar (atla=(3,): no underside)"""
    yay_kesit(y, c, [(r_dis, z0), (r_dis, z1), (r_ic, z1), (r_ic, z0)], t0, t1, n, key, keys=keys, atla=atla)


def kalasa(y, cx, cy, z, s=1.0, key='altin'):
    """a kalasha finial: a lotus cushion, a round pot, a smaller pot and a spike. Returns the tip z"""
    donel(y, (cx, cy), [(0.0, z), (0.014 * s, z + 0.003 * s), (0.009 * s, z + 0.01 * s), (0.014 * s, z + 0.02 * s), (0.009 * s, z + 0.03 * s),
                        (0.008 * s, z + 0.04 * s), (0.003 * s, z + 0.046 * s), (0.0, z + 0.066 * s)], key, n=8)
    return z + 0.066 * s


def chhajja(y, kose, z, h, c, key='kum_acik', kapali=True):
    """a thin sloping stone eave round a CCW polygon (or along a polyline facing its right): its top at z + h at the
    wall, its lip c out and h * 0.55 lower"""
    silme(y, kose, z, h, c, key, CHHAJJA, kapali)


def lotus_kubbe(y, c, r, z, h=None, key='kum_acik', n=24, kat=8, yaprak='kum_acik', son=True, s_son=1.0, sogan=False):
    """a Rajput / Mughal dome: a hemisphere (or a squat onion: sogan) with a lotus crown of petals at its top, an
    amalaka ring and a kalasha. Returns the tip z"""
    h = h or r * 0.95
    if sogan:
        tz = sogan_kubbe(y, c, r, z, h * 1.25, key, n=n, boyun=0.7, sivri=0.1)
        zt = z + h * 1.25 * 0.88
        rt = r * 0.16
    else:
        t = y.kubbe(c, r, z, h, key, n=n, kat=kat)
        tz = t.z
        zt = tz - h * 0.06
        rt = r * 0.32
    # lotus crown: inverted petals round the top
    for i in range(12):
        a = TAU * (i + 0.5) / 12
        d = V(math.cos(a), math.sin(a)); tg = V(-d.y, d.x)
        p = V(c[0], c[1]) + d * rt
        w = rt * 0.42
        q = [p - tg * w + Z * (zt - h * 0.02), p + tg * w + Z * (zt - h * 0.02), p + d * (rt * 0.05) + Z * (zt - h * 0.16)]
        y.yuz_yon(q, yaprak, d + Z * 0.6)
    donel(y, c, [(0.0, tz - 0.001), (rt * 0.55, tz - 0.001), (rt * 0.62, tz + r * 0.04), (rt * 0.4, tz + r * 0.07), (0.0, tz + r * 0.07)], yaprak, n=12)
    top = tz + r * 0.07
    if son:
        top = kalasa(y, c[0], c[1], top, s_son * max(0.5, r / 0.06))
    return top


def chhatri(y, cx, cy, z, r, n=6, kolon='kum_acik', kubbe='kum_acik', kaide='kum', kat=math.pi / 6, h=None, sogan=False, kaide_h=None,
            chh_key=None, yaprak=None, s_son=1.0):
    """a chhatri: an open domed kiosk - a moulded plinth, n slim pillars with bracket capitals, a lintel ring, a
    projecting chhajja, a low drum and a lotus-crowned dome with a kalasha. r: the pillar circle radius. Returns the
    tip z"""
    h = h or r * 1.35
    kh = kaide_h if kaide_h is not None else r * 0.22
    rk = r * 1.18
    if kh > 0:
        y.prizma((cx, cy), rk, z, z + kh, kaide, n=n, kat=kat)
        halka_kornis(y, (cx, cy), rk, z + kh - kh * 0.25, kh * 0.25, r * 0.06, n, kolon, kat=kat)
        silme(y, cokgen((cx, cy), rk, n, kat), z, kh * 0.3, r * 0.06, kaide, 'kaide')
    z0 = z + kh
    kose = cokgen((cx, cy), r, n, kat)
    w = max(0.006, r * 0.16)
    for p in kose:
        kutu_merkez(y, (p.x, p.y), w * 1.35, w * 1.35, h * 0.08, kolon, z0=z0)
        a = math.atan2(p.y - cy, p.x - cx)
        kutu_merkez(y, (p.x, p.y), w, w, h * 0.78, kolon, z0=z0 + h * 0.08, aci=a, yuzler='onarkasagsol')
        # bracket capital: a block and a corbel stepping out on both sides
        kutu_merkez(y, (p.x, p.y), w * 1.5, w * 1.5, h * 0.07, kolon, z0=z0 + h * 0.86, aci=a)
    zl = z0 + h * 0.93
    hl = h * 0.12
    # lintel ring (outer, inner faces and its top under the chhajja)
    dis = cokgen((cx, cy), r + w * 0.75, n, kat)
    ic = cokgen((cx, cy), r - w * 0.75, n, kat)
    duvarlar(y, dis, zl, zl + hl, kolon)
    duvarlar(y, [ic[(n - i) % n] for i in range(n)], zl, zl + hl, kolon)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([ic[i] + Z * zl, ic[j] + Z * zl, dis[j] + Z * zl, dis[i] + Z * zl], kolon, -Z)
        y.yuz_yon([ic[i] + Z * (zl + hl), ic[j] + Z * (zl + hl), dis[j] + Z * (zl + hl), dis[i] + Z * (zl + hl)], kolon, Z)
    zc = zl + hl
    chhajja(y, dis, zc - r * 0.16, r * 0.16, r * 0.3, chh_key or kolon)
    # drum and dome
    rd = r * 0.92
    nd = 16 if r < 0.045 else 20
    y.prizma((cx, cy), rd, zc, zc + r * 0.12, kolon, n=nd, ust=True)
    halka_kornis(y, (cx, cy), rd, zc + r * 0.1, r * 0.03, r * 0.03, nd, kolon)
    return lotus_kubbe(y, (cx, cy), rd * 0.98, zc + r * 0.12, rd * (0.8 if sogan else 0.9), kubbe, n=nd, kat=5,
                       yaprak=yaprak or kolon, sogan=sogan, s_son=s_son)


def vedika_duz(y, a, b, z, h, key='kum', aralik=0.03, w=0.012, d=None, ust_key=None, bar=3):
    """a straight Buddhist stone railing a->b (its outer face to the right): square posts, bar lens-shaped
    crossbars (suchi) between them and a rounded coping (ushnisha) on top"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-5: return
    e = (b - a) / L; nc = V(e.y, -e.x)
    d = d or w * 0.8
    n = max(1, int(round(L / aralik)))
    hc = h * 0.16
    for i in range(n + 1):
        p = a.lerp(b, i / n)
        kutu(y, p - e * (w / 2) + nc * (d / 2) + Z * z, e, w, d, h - hc, key, 'onarkasagsol')
    # crossbars: thinner boxes set back between the posts
    for j in range(bar):
        zz = z + (h - hc) * (j + 0.6) / (bar + 0.2)
        hb = (h - hc) / (bar + 0.2) * 0.62
        kutu(y, a + nc * (d * 0.3) + Z * (zz - hb / 2), e, L, d * 0.6, hb, key, 'onarkaust')
    # coping: a rounded rail on top
    o = a - e * (w / 2) + Z * (z + h - hc)
    kutu(y, o + nc * (d * 0.55), e, L + w, d * 1.1, hc * 0.6, ust_key or key, 'onarkasagsol')
    p0, p1 = o + nc * (d * 0.55) + Z * (hc * 0.6), o + e * (L + w) + nc * (d * 0.55) + Z * (hc * 0.6)
    q0, q1 = p0 - nc * (d * 1.1), p1 - nc * (d * 1.1)
    m0, m1 = (p0 + q0) / 2 + Z * (hc * 0.4), (p1 + q1) / 2 + Z * (hc * 0.4)
    y.yuz_yon([p0, p1, m1, m0], ust_key or key, nc + Z)
    y.yuz_yon([m0, m1, q1, q0], ust_key or key, -nc + Z)
    y.yuz_yon([p0, m0, q0], ust_key or key, -e)
    y.yuz_yon([p1, q1, m1], ust_key or key, e)


def vedika_yay(y, c, r, z, h, t0, t1, key='kum', aralik=0.03, w=0.012, ust_key=None, bar=3, alt=True):
    """a curved Buddhist stone railing on the circle r round c from angle t0 to t1: posts, crossbars, coping
    (alt=False: the crossbars' and the coping's undersides are left out: never seen from above)"""
    L = abs(t1 - t0) * r
    n = max(2, int(round(L / aralik)))
    d = w * 0.8
    hc = h * 0.16
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        p = V(c[0] + r * math.cos(t), c[1] + r * math.sin(t))
        kutu_merkez(y, (p.x, p.y), d, w, h - hc, key, z0=z, aci=t, yuzler='onarkasagsol')
    for j in range(bar):
        zz = z + (h - hc) * (j + 0.6) / (bar + 0.2)
        hb = (h - hc) / (bar + 0.2) * 0.62
        halka(y, c, r + d * 0.3, r - d * 0.3, zz - hb / 2, zz + hb / 2, key, n=n, t0=t0, t1=t1, atla=() if alt else (3,))
    zc = z + h - hc
    yay_kesit(y, c, [(r + d * 0.55, zc), (r + d * 0.55, zc + hc * 0.6), (r, zc + hc), (r - d * 0.55, zc + hc * 0.6), (r - d * 0.55, zc)],
              t0, t1, n, ust_key or key, atla=() if alt else (4,))


def konsol_dizi(y, a, b, z, h, c, key='kum', aralik=0.03, w=0.008):
    """a row of stepped stone brackets under a balcony or an eave along a->b (projecting to its right)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    n = max(1, int(round(L / aralik)))
    for i in range(n + 1):
        p = a.lerp(b, i / n)
        for k in range(3):
            cc = p + nc * (c * (k + 1) / 3 / 2)
            kutu_merkez(y, (cc.x, cc.y), w, c * (k + 1) / 3, h / 3, key, z0=z + h * k / 3,
                        aci=math.atan2(e.y, e.x))


def jharokha(y, a, b, z, w, h, d, key='kum', trim='kum_acik', renk=None, kubbe=True, kubbe_key=None, konsol_key=None,
             n_on=1, perde=None):
    """a jharokha: a balcony window projecting d from the wall line a->b (to its right), centred, w wide, h tall
    from z: stepped brackets under a floor slab, arched openings on the front (n_on) and sides, a chhajja and a
    small domed (or flat) top. perde: a key for a jali screen in the lower part of the openings. Returns the top z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    m = (a + b) / 2
    renk = renk or (key, key, trim, 'koyu')
    p0 = m - e * (w / 2); p1 = m + e * (w / 2)
    f0, f1 = p0 + nc * d, p1 + nc * d
    # brackets and the floor slab
    konsol_dizi(y, p0 + e * 0.004, p1 - e * 0.004, z - h * 0.26, h * 0.22, d, konsol_key or trim, aralik=max(0.012, w / 3), w=min(0.008, w * 0.12))
    kutu(y, p0 - e * 0.004 + nc * (d + 0.006) + Z * (z - h * 0.05), e, w + 0.008, d + 0.006, h * 0.05, trim, 'onsagsolust')
    y.yuz_yon([p0 - e * 0.004 + Z * (z - h * 0.05), p1 + e * 0.004 + Z * (z - h * 0.05),
               p1 + e * 0.004 + nc * (d + 0.006) + Z * (z - h * 0.05), p0 - e * 0.004 + nc * (d + 0.006) + Z * (z - h * 0.05)], trim, -Z)
    # the three open sides
    for k in range(n_on):
        y.kemerli(f0.lerp(f1, k / n_on), f0.lerp(f1, (k + 1) / n_on), z, h, renk, v0=h * 0.06, en=0.66, ust=h * 0.1, derin=0.006,
                  k_say=6, sivri=0.0, korkuluk=h * 0.25 if perde is None else None)
    for s, (u, v) in ((-1, (p0, f0)), (1, (f1, p1))):
        if d > 0.012:
            y.kemerli(u, v, z, h, renk, v0=h * 0.06, en=0.6, ust=h * 0.1, derin=0.005, k_say=6, sivri=0.0)
        else:
            duz_duvar(y, u, v, z, z + h, key)
    if perde:
        for k in range(n_on):
            q0, q1 = f0.lerp(f1, k / n_on), f0.lerp(f1, (k + 1) / n_on)
            kafes(y, q0, q1, z, 0.17, 0.83, h * 0.06, h * 0.42, perde, 4, 2, 0.002, 0.0015)
    zt = z + h
    k4 = [p0, f0, f1, p1]
    # roof slab, chhajja
    y.yuz_yon([pp + Z * zt for pp in (p0, p1, f1, f0)], trim, Z)
    chhajja(y, k4, zt - h * 0.12, h * 0.12, h * 0.22, trim, kapali=False)
    if kubbe:
        cc = (p0 + f1) / 2
        rr = min(w, d) * 0.42
        y.prizma((cc.x, cc.y), rr, zt, zt + h * 0.08, trim, n=16, ust=False)
        return lotus_kubbe(y, (cc.x, cc.y), rr, zt + h * 0.08, rr * 0.95, kubbe_key or trim, n=16, kat=6, yaprak=trim, s_son=0.6)
    return zt


def fil(y, x, yy, z, aci=0.0, olcek=1.0, key='fil', cul=None, haudah=False, binici=None, hortum=0.0, sus='altin', az=False, kaba=False):
    """a stylised elephant facing aci (head towards +x before turning), ~0.12 tall at olcek 1: legs, barrel body,
    domed head, big ear flaps, a trunk (hortum > 0 raises it), tusks, a tail. cul: a key for a caparison (jhool) with a
    gold border; haudah: a canopied howdah on its back; binici: a key for a mahout's robe (sits on the neck); kaba: fewer segments on the round parts (a background elephant)"""
    q = 0.7 if kaba else 1.0
    nq = lambda n, m=3: max(m, int(round(n * q)))
    with parca(y, (x, yy, z), aci, olcek):
        # legs (pillar-like, a little wider at the foot) and toenails
        for lx in (-0.03, 0.026):
            for s in (-1, 1):
                ly = s * 0.016
                if az: kutu_merkez(y, (lx, ly), 0.019, 0.019, 0.062, key, yuzler='onarkasagsol')
                else: donel(y, (lx, ly), [(0.0, 0.0), (0.0115, 0.0), (0.0105, 0.012), (0.0098, 0.04), (0.011, 0.06), (0.0, 0.062)], key, n=nq(8))
                for t in ():
                    kure(y, (lx + 0.0105 * math.cos(t), ly + 0.0105 * math.sin(t) * 0.8, 0.004), 0.0025, 'kum_acik', n=5, kat=2)
        # body
        elipsoid(y, (0.0, 0.0, 0.074), 0.047, 0.027, 0.032, key, n=6 if az else nq(12), kat=3 if az else nq(6))
        # head and forehead dome
        elipsoid(y, (0.048, 0.0, 0.088), 0.022, 0.02, 0.024, key, n=5 if az else nq(12), kat=2 if az else nq(6))
        if not az: elipsoid(y, (0.052, 0.0, 0.105), 0.013, 0.015, 0.011, key, n=nq(10), kat=nq(5))
        # ears: flattened discs at the sides of the head
        for s in (-1, 1):
            elipsoid(y, (0.04, s * 0.022, 0.088), 0.017, 0.0035, 0.022, key, n=5 if az else nq(10), kat=2 if az else nq(6))
            if not az: kure(y, (0.062, s * 0.012, 0.096), 0.0022, 'koyu', n=6, kat=3)      # eye
        # trunk
        tr = [V(0.066, 0, 0.084), V(0.075, 0, 0.066), V(0.079, 0, 0.044), V(0.08 + hortum * 0.2, 0, 0.026 + hortum * 0.6),
              V(0.085 + hortum * 0.5, 0, 0.012 + hortum), V(0.09 + hortum * 0.6, 0, 0.012 + hortum * 1.2)]
        boru(y, tr if not az else tr[::2] + [tr[-1]], 0.0085, key, n=3 if az else nq(8), r_son=0.0035)
        # tusks
        for s in (-1, 1):
            boru(y, [V(0.062, s * 0.01, 0.074), V(0.074, s * 0.012, 0.06), V(0.086, s * 0.011, 0.062), V(0.091, s * 0.009, 0.07)], 0.0028,
                 'beyaz', n=3 if az else nq(6), r_son=0.001)
        # tail
        if not az: boru(y, [V(-0.046, 0, 0.088), V(-0.052, 0, 0.07), V(-0.053, 0, 0.05)], 0.0018, key, n=4, r_son=0.0012)
        if cul:
            # the caparison: a cloth over the back hanging down both flanks, a gold border, and a forehead plate
            for s in (-1, 1):
                y.yuz_yon([V(-0.028, s * 0.0285, 0.06), V(0.024, s * 0.0285, 0.06), V(0.024, s * 0.0265, 0.098), V(-0.028, s * 0.0265, 0.098)],
                          cul, V(0, s))
                y.yuz_yon([V(-0.028, s * 0.029, 0.058), V(0.024, s * 0.029, 0.058), V(0.024, s * 0.029, 0.064), V(-0.028, s * 0.029, 0.064)],
                          sus, V(0, s))
                y.yuz_yon([V(-0.028, s * 0.0265, 0.098), V(0.024, s * 0.0265, 0.098), V(0.024, s * 0.012, 0.1075), V(-0.028, s * 0.012, 0.1075)],
                          cul, V(0, s * 0.5, 1))
            y.yuz_yon([V(-0.028, -0.012, 0.1075), V(0.024, -0.012, 0.1075), V(0.024, 0.012, 0.1075), V(-0.028, 0.012, 0.1075)], cul, Z)
            for xx, sg in ((-0.028, -1), (0.024, 1)):
                y.yuz_yon([V(xx, -0.0265, 0.098), V(xx, -0.012, 0.1075), V(xx, 0.012, 0.1075), V(xx, 0.0265, 0.098), V(xx, 0.0285, 0.06),
                           V(xx, -0.0285, 0.06)], cul, V(sg, 0))
            # (the forehead plate: two-sided, its top edge stands clear of the head and was seen from behind)
            iki_yuzlu(y, [V(0.066, -0.008, 0.094), V(0.066, 0.008, 0.094), V(0.069, 0.006, 0.112), V(0.069, -0.006, 0.112)], sus, V(1, 0, 0.2))
        if haudah:
            hz = 0.108
            kutu_merkez(y, (-0.004, 0.0), 0.036, 0.03, 0.022, haudah if isinstance(haudah, str) else 'altin', z0=hz)
            silme(y, dikdortgen(-0.022, 0.014, -0.015, 0.015), hz + 0.02, 0.004, 0.003, 'kum_acik', 'duz')
            for px in (-0.019, 0.011):
                for py in (-0.012, 0.012):
                    y.prizma((px, py), 0.0018, hz + 0.022, hz + 0.05, 'altin', n=4)
            y.kubbe((-0.004, 0.0), 0.024, hz + 0.05, 0.016, 'boya_kirmizi', n=12, kat=4)
            kure(y, (-0.004, 0.0, hz + 0.068), 0.003, 'altin', n=6, kat=3)
        if binici:
            adam(y, 0.036, 0.0, 0.098, 0.0, binici, 'beyaz', boy=0.034)


def nis_satir(y, a, b, z0, z1, n, renk=KUM, en=0.6, derin=0.008, sivri=0.0, ust=None):
    """a wall a->b from z0 to z1 made of n shallow arched niches (blind arcade panelling)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        y.kemerli(p, q, z0, z1 - z0, renk, v0=(z1 - z0) * 0.08, en=en, ust=ust if ust is not None else (z1 - z0) * 0.12, derin=derin,
                  k_say=6, sivri=sivri)


def bolum_say(y):
    """print the triangle count of each named section (LM_SAY=1)"""
    import os
    if not os.environ.get('LM_SAY'): return
    b = getattr(y, 'bolumler', []) + [(len(y.faces), 'son')]
    for (i0, ad), (i1, _) in zip(b, b[1:]):
        print('BOLUM %-32s %6d' % (ad, sum(len(p) - 2 for p, _ in y.faces[i0:i1])))


def tekil(pts, e=1e-7):
    """drop repeated points of a polygon (a face with a doubled corner is refused by the mesh)"""
    out = []
    for p in pts:
        if not out or (Vector(p) - Vector(out[-1])).length > e:
            out.append(p)
    if len(out) > 1 and (Vector(out[0]) - Vector(out[-1])).length <= e:
        out.pop()
    return out


def bangla(y, x0, x1, y0, y1, z, h, d=None, key='kum_acik', ns=8, nr=6, kenar='kum_acik'):
    """a bangaldar roof over the rectangle (ridge along its longer side): a curved vault across, its ridge and eaves
    bowing up d in the middle and down to the ends (the Bengal hut roof of Mughal / Rajput pavilions); the long sides
    closed down to z, the curved gable ends. Returns the ridge top z"""
    if (x1 - x0) < (y1 - y0):
        with parca(y, ((x0 + x1) / 2, (y0 + y1) / 2, 0), math.pi / 2):
            return bangla(y, -(y1 - y0) / 2, (y1 - y0) / 2, -(x1 - x0) / 2, (x1 - x0) / 2, z, h, d, key, ns, nr, kenar)
    d = h * 0.35 if d is None else d
    arc = lambda u: math.sqrt(max(0.0, 1 - (2 * u - 1) ** 2)) ** 0.8
    bow = lambda t: d * (1 - (2 * t - 1) ** 2)
    P = lambda t, u: V(x0 + (x1 - x0) * t, y0 + (y1 - y0) * u, z + bow(t) + h * arc(u))
    for i in range(ns):
        for j in range(nr):
            t0, t1, u0, u1 = i / ns, (i + 1) / ns, j / nr, (j + 1) / nr
            q = [P(t0, u0), P(t1, u0), P(t1, u1), P(t0, u1)]
            yuz_dis(y, q, key, V((x0 + x1) / 2, (y0 + y1) / 2, z - h))
    # the long sides: the bowed eave down to the wall top
    for i in range(ns):
        t0, t1 = i / ns, (i + 1) / ns
        for uu, yy_, s in ((0.0, y0, -1), (1.0, y1, 1)):
            a, b = P(t0, uu), P(t1, uu)
            q = tekil([V(a.x, yy_, z), V(b.x, yy_, z), b, a])
            if len(q) >= 3:
                y.yuz_yon(q, kenar, V(0, s))
    # the curved gable ends
    for t, s in ((0.0, -1), (1.0, 1)):
        pts = [V(x0 + (x1 - x0) * t, y0, z)] + [P(t, j / nr) for j in range(nr + 1)] + [V(x0 + (x1 - x0) * t, y1, z)]   # (the roof's own corners: finer, it stood proud of the chords)
        y.yuz_yon(tekil(pts), kenar, V(s, 0))
    # a ridge rib and finials
    rid = [P(i / ns, 0.5) + Z * 0.002 for i in range(ns + 1)]
    boru(y, rid, max(0.0025, h * 0.06), kenar, n=4)
    return z + d + h
