# Arabacı Ahırı (lm_arabaciahiri): a New Kingdom chariotry stable (after the Qantir / Pi-Ramesses stables and the
# Amarna tomb reliefs): a small limestone pylon gate with flagpoles and a painted chariot scene, a mud-brick
# enclosure; the long stable hall with a papyrus-column shade portico, stalls with stone mangers and tethered horses,
# a raised clerestory; an open chariot shed with six-spoked chariots, a tack and bow store, a well and troughs, and the
# sand training track with turning posts where a span of horses runs a chariot.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05
KER = 'kerpic_tugla'
SIV = 'siva_krem'
TAS = 'kirec'
KAVETTO = [(0, 0), (0.16, 0.03), (0.2, 0.1), (0.12, 0.17), (0.04, 0.19), (0.07, 0.36), (0.18, 0.56), (0.4, 0.75),
           (0.72, 0.88), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]


def kavetto(kose, z, h, c, key):
    silme(y, kose, z, h, c, key, KAVETTO)
    y.yuz_yon([V(p.x, p.y, z + h) for p in kose], key, Z)


def flama(x, yy, z, key, en=0.15, yuk=0.032, aci=0.0, dalga=0.013, n=7):
    """a long pennant on a pole (top z)"""
    e = V(math.cos(aci), math.sin(aci)); nn = V(-e.y, e.x)
    o = V(x, yy, z - 0.012 - yuk)
    def P(u, v, s):
        w = math.sin(u * math.pi * 1.7) * dalga * u
        return o + e * (0.007 + u * en) + nn * (w + s * 0.0015) + Z * (v * (1 - 0.55 * u) - 0.3 * u * u * yuk + yuk * 0.275 * u)
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        y.yuz_yon([P(u0, 0, 1), P(u1, 0, 1), P(u1, yuk, 1), P(u0, yuk, 1)], key, nn)
        y.yuz_yon([P(u0, 0, -1), P(u1, 0, -1), P(u1, yuk, -1), P(u0, yuk, -1)], key, -nn)
        y.yuz_yon([P(u0, yuk, 1), P(u1, yuk, 1), P(u1, yuk, -1), P(u0, yuk, -1)], key, Z)
        y.yuz_yon([P(u0, 0, 1), P(u1, 0, 1), P(u1, 0, -1), P(u0, 0, -1)], key, -Z)
        if i == n - 1:
            y.yuz_yon([P(1, 0, 1), P(1, yuk, 1), P(1, yuk, -1), P(1, 0, -1)], key, e)


# ---------------------------------------------------------------- horses and chariots (built facing +x at the origin)
def at(x, yy, z, aci, renk='ahsap', tuy=True, kosu=0.0, olcek=1.0):
    """a horse: barrel body, chest and haunch, four legs (kosu > 0: galloping, legs stretched), arched neck, head,
    a mane, a tail, and the red plume of a chariot horse"""
    with parca(y, (x, yy, z), aci, olcek):
        H = 0.062   # withers height over the hooves
        boru(y, [V(-0.042, 0, H - 0.012), V(-0.01, 0, H - 0.014), V(0.03, 0, H - 0.01)], 0.017, renk, n=10)
        kure(y, (-0.043, 0, H - 0.012), 0.017, renk, n=10, kat=5)
        kure(y, (0.032, 0, H - 0.008), 0.017, renk, n=10, kat=5)
        for lx, front in ((-0.04, False), (0.03, True)):
            for s in (-1, 1):
                sw = kosu * (0.03 if front else -0.03) * (1 if s > 0 else 0.6)
                top = V(lx, s * 0.009, H - 0.018)
                knee = V(lx + sw * 0.6, s * 0.009, H * 0.45)
                hoof = V(lx + sw, s * 0.009, 0.004 + abs(sw) * 0.3)
                boru(y, [top, knee, hoof], 0.0045, renk, n=5, r_son=0.003)
                kutu_merkez(y, (hoof.x, hoof.y), 0.008, 0.007, 0.006, 'koyu', z0=hoof.z - 0.004)
        # neck and head
        boru(y, [V(0.035, 0, H - 0.004), V(0.05, 0, H + 0.016), V(0.058, 0, H + 0.03)], 0.01, renk, n=8, r_son=0.008)
        boru(y, [V(0.056, 0, H + 0.034), V(0.078, 0, H + 0.022)], 0.0075, renk, n=8, r_son=0.0055)
        for s in (-1, 1):
            boru(y, [V(0.054, s * 0.004, H + 0.04), V(0.052, s * 0.005, H + 0.05)], 0.0022, renk, n=4, r_son=0.001)
        boru(y, [V(0.03, 0, H + 0.004), V(0.046, 0, H + 0.026), V(0.054, 0, H + 0.04)], 0.004, 'ahsap_koyu', n=5)   # mane
        boru(y, [V(-0.058, 0, H - 0.008), V(-0.07, 0, H - 0.02 + kosu * 0.012), V(-0.074, 0, H - 0.045 + kosu * 0.03)], 0.0042, 'ahsap_koyu', n=5, r_son=0.002)
        if tuy:   # the plume and a fringed caparison
            boru(y, [V(0.056, 0, H + 0.044), V(0.054, 0, H + 0.064), V(0.048, 0, H + 0.072)], 0.004, 'boya_kirmizi', n=5, r_son=0.0015)
            kutu_merkez(y, (-0.005, 0), 0.05, 0.038, 0.006, 'boya_kirmizi', z0=H + 0.0)
            kutu_merkez(y, (-0.005, 0), 0.05, 0.04, 0.003, 'boya_sari', z0=H - 0.004)


def tekerlek(c, R=0.038, gen=0.006, key='ahsap'):
    """a six-spoked chariot wheel in the x-z plane at c (axle along y)"""
    c = V(*c)
    n = 18
    # the felloe: a ring of short beams
    pts = [c + V(R * math.cos(TAU * i / n), 0, R * math.sin(TAU * i / n)) for i in range(n)]
    for i in range(n):
        cubuk(y, pts[i], pts[(i + 1) % n], 0.006, key, gen)
    for i in range(6):
        a = TAU * i / 6 + math.pi / 6
        cubuk(y, c, c + V(R * math.cos(a), 0, R * math.sin(a)), 0.0035, key, 0.0035)
    boru(y, [c + V(0, -gen * 1.4, 0), c + V(0, gen * 1.4, 0)], 0.007, 'bronz', n=8)


def araba(x, yy, z, aci, kosu=False, atli=True, surucu=True, eg=0.0):
    """a war chariot: a light D-shaped cab of bent wood with a leather / gilded front, the axle at its rear, two
    six-spoked wheels, the pole curving up to the yoke (eg: the pole tipped up when parked), a quiver and bow case;
    atli: a span of two horses yoked; surucu: a charioteer and an archer"""
    with parca(y, (x, yy, z), aci):
        R = 0.038
        for s in (-1, 1):
            tekerlek((-0.02, s * 0.052, R), R)
        cubuk(y, V(-0.02, -0.058, R), V(-0.02, 0.058, R), 0.006, 'ahsap_koyu')
        # cab: floor, the D-shaped rail, the side screens
        kutu_merkez(y, (0.0, 0), 0.05, 0.07, 0.004, 'ahsap_koyu', z0=R + 0.002)
        rail = [V(-0.02 + 0.045 * math.sin(math.pi * k / 8), 0.035 * math.cos(math.pi * k / 8), R + 0.05) for k in range(9)]
        boru(y, rail, 0.0025, 'ahsap', n=4)
        for k in range(8):
            p, q = rail[k], rail[k + 1]
            bot = lambda v: V(v.x, v.y, R + 0.006)
            m = (p + q) / 2
            yuz_dis(y, [bot(p), bot(q), q - Z * 0.008, p - Z * 0.008], 'altin' if 2 <= k <= 5 else 'boya_kirmizi', V(-0.02, 0, R + 0.03))
            ic = lambda v: v - (V(v.x, v.y, 0) - V(-0.02, 0, 0)).normalized() * 0.0018
            yuz_dis(y, [ic(bot(q)), ic(bot(p)), ic(p - Z * 0.008), ic(q - Z * 0.008)], 'ahsap_koyu', m + (m - V(-0.02, 0, m.z)) * 1.0)
        # the pole and the yoke
        pole_end = V(0.2, 0, R + 0.04 + eg)
        boru(y, [V(-0.02, 0, R + 0.004), V(0.04, 0, R + 0.006), V(0.12, 0, R + 0.02 + eg * 0.5), pole_end], 0.0035, 'ahsap', n=5)
        cubuk(y, pole_end + V(0, -0.045, 0.004), pole_end + V(0, 0.045, 0.004), 0.005, 'ahsap_koyu')
        # quiver and bow case on the side
        cubuk(y, V(0.01, 0.037, R + 0.01), V(0.035, 0.04, R + 0.055), 0.008, 'boya_kirmizi')
        cubuk(y, V(-0.015, -0.037, R + 0.012), V(0.03, -0.04, R + 0.05), 0.006, 'ahsap_koyu')
        if atli:
            for s in (-1, 1):
                at(0.18 + 0.03, s * 0.026, 0.0, 0.0, 'ahsap_acik' if s < 0 else 'ahsap', kosu=1.0 if kosu else 0.0)
            for s in (-1, 1):   # reins
                boru(y, [V(-0.005, s * 0.01, R + 0.07), V(0.1, s * 0.02, R + 0.06), V(0.27, s * 0.026, 0.092)], 0.0012, 'ahsap_koyu', n=3)
        if surucu:
            for k, (dx, dy) in enumerate(((0.0, -0.012), (-0.008, 0.014))):
                kutu_merkez(y, (dx, dy), 0.014, 0.016, 0.03, 'beyaz', z0=R + 0.006)
                donel(y, (dx, dy), [(0.008, R + 0.036), (0.01, R + 0.05), (0.007, R + 0.06), (0, R + 0.062)], 'kirmizi', n=6)
                kure(y, (dx + 0.002, dy, R + 0.069), 0.0075, 'lacivert' if k == 0 else 'koyu', n=6, kat=3)   # the blue war crown / wig
            boru(y, [V(-0.005, 0.022, R + 0.1), V(0.02, 0.03, R + 0.065), V(-0.005, 0.022, R + 0.03)], 0.0018, 'ahsap_koyu', n=3)   # the bow


# ---------------------------------------------------------------- ground
y.bolum('Zemin')
XW, YF, YB = 1.15, -1.15, 1.15
zemin(y, -XW, XW, YF, YB, Z0, 'kerpic_koyu', 'kum_acik', basamak=(('on', 0.5),), n_basamak=3)
# the road to the gate
y.yuz([V(-0.14, YF + 0.005, Z0 + 0.002), V(0.14, YF + 0.005, Z0 + 0.002), V(0.14, -0.86, Z0 + 0.002), V(-0.14, -0.86, Z0 + 0.002)], 'zemin')

# ---------------------------------------------------------------- the enclosure wall
y.bolum('Avlu duvari')
EX0, EX1, EY0, EY1 = -1.06, 1.06, -0.84, 1.06
HW, TW = 0.13, 0.045
GX = 0.13


def duvar(a, b):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x); L = (b - a).length
    kutu(y, a + Z * Z0, e, L, TW, HW, KER, 'onarkaust')
    for p, s in ((a, -1), (b, 1)):
        y.yuz_yon([p + Z * Z0, p - nc * TW + Z * Z0, p - nc * TW + Z * (Z0 + HW), p + Z * (Z0 + HW)], KER, e * s)
    boru(y, [a - nc * (TW / 2) + Z * (Z0 + HW), b - nc * (TW / 2) + Z * (Z0 + HW)], TW * 0.48, 'kerpic', n=8)
    kutu(y, a + Z * Z0 + nc * 0.004, e, L, 0.004, 0.03, SIV, 'onust')
    n = max(1, int(L / 0.24))
    for m in range(1, n):
        p = a.lerp(b, m / n)
        kutu(y, p - e * 0.016 + Z * Z0 + nc * 0.014, e, 0.032, 0.014, HW - 0.01, KER, 'onsagsolust')
        boru(y, [p - e * 0.016 + nc * 0.007 + Z * (Z0 + HW - 0.01), p + e * 0.016 + nc * 0.007 + Z * (Z0 + HW - 0.01)], 0.008, 'kerpic', n=6)


k = [V(EX0, EY0), V(-GX - 0.17, EY0), V(GX + 0.17, EY0), V(EX1, EY0), V(EX1, EY1), V(EX0, EY1)]
duvar(k[0], k[1]); duvar(k[2], k[3]); duvar(k[3], k[4]); duvar(k[4], k[5]); duvar(k[5], k[0])

# ---------------------------------------------------------------- the pylon gate
y.bolum('Pilon kapi')
PH = 0.64
PY0, PY1 = EY0 - 0.07, EY0 + 0.09


def boya(P, n, s0, s1, t0, t1, key, d=0.003):
    y.yuz_yon([P(s0, t0, d), P(s1, t0, d), P(s1, t1, d), P(s0, t1, d)], key, n)


def araba_kabartma(P, n, sc, t0, H, yon):
    """a painted relief of the king in his chariot drawing the bow, horses at the gallop (flat quads)"""
    # polygons in figure units (s forward, t up, x H); each part casts a dark rim down and behind it (carved relief)
    def F(pts, key, kat=1, golge=True):
        Pw = lambda s, t, dz: P(sc + yon * s * H, t0 + t * H, dz)
        if golge:
            y.yuz_yon([Pw(s + 0.012, t - 0.014, 0.0027) for s, t in pts], 'kum_koyu', n)
        y.yuz_yon([Pw(s, t, 0.0035 + 0.0012 * kat) for s, t in pts], key, n)
    def kol(a, b, w):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); px, py = -dy / L * w / 2, dx / L * w / 2
        return [(a[0] + px, a[1] + py), (a[0] - px, a[1] - py), (b[0] - px, b[1] - py), (b[0] + px, b[1] + py)]
    def halka(c, r0, r1, key, kat, k=14):
        for i in range(k):
            a0, a1 = TAU * i / k, TAU * (i + 1) / k
            F([(c[0] + r1 * math.cos(a0), c[1] + r1 * math.sin(a0)), (c[0] + r1 * math.cos(a1), c[1] + r1 * math.sin(a1)),
               (c[0] + r0 * math.cos(a1), c[1] + r0 * math.sin(a1)), (c[0] + r0 * math.cos(a0), c[1] + r0 * math.sin(a0))], key, kat, False)
    # two horses at the gallop, the far one a step ahead and higher: barrel, chest, arched neck, head, forelegs
    # reaching, hind legs thrust back, the tail streaming, a tall plume
    for k, key in enumerate(('ahsap', 'ahsap_acik')):
        o, h = 0.05 * (1 - k), 0.03 * (1 - k)
        kk = 1 + k
        F([(0.08 + o, 0.34 + h), (0.38 + o, 0.33 + h), (0.42 + o, 0.42 + h), (0.38 + o, 0.5 + h), (0.1 + o, 0.5 + h), (0.05 + o, 0.43 + h)], key, kk)
        F([(0.36 + o, 0.44 + h), (0.42 + o, 0.42 + h), (0.5 + o, 0.62 + h), (0.45 + o, 0.66 + h)], key, kk)
        F([(0.45 + o, 0.6 + h), (0.52 + o, 0.65 + h), (0.6 + o, 0.58 + h), (0.58 + o, 0.55 + h), (0.5 + o, 0.57 + h)], key, kk)
        F(kol((0.38 + o, 0.38 + h), (0.55 + o, 0.3 + h), 0.035), key, kk)
        F(kol((0.36 + o, 0.36 + h), (0.5 + o, 0.2 + h), 0.035), key, kk)
        F(kol((0.1 + o, 0.38 + h), (-0.02 + o, 0.22 + h), 0.04), key, kk)
        F(kol((0.12 + o, 0.36 + h), (0.02 + o, 0.18 + h), 0.035), key, kk)
        F(kol((0.06 + o, 0.47 + h), (-0.04 + o, 0.4 + h), 0.02), 'ahsap_koyu', kk + 1, False)
        F([(0.47 + o, 0.66 + h), (0.5 + o, 0.66 + h), (0.5 + o, 0.8 + h), (0.47 + o, 0.78 + h)], 'boya_kirmizi', kk + 1, False)
        F([(0.12 + o, 0.47 + h), (0.36 + o, 0.47 + h), (0.36 + o, 0.5 + h), (0.12 + o, 0.5 + h)], 'boya_kirmizi' if k else 'boya_sari', kk + 1, False)
    # the chariot: the six-spoked wheel, the D-shaped cab with its gilded side, the pole running to the yoke
    halka((-0.18, 0.13), 0.095, 0.125, 'ahsap_koyu', 3)
    for i in range(3):
        b = math.pi * i / 3 + math.pi / 6
        F(kol((-0.18 + 0.1 * math.cos(b), 0.13 + 0.1 * math.sin(b)), (-0.18 - 0.1 * math.cos(b), 0.13 - 0.1 * math.sin(b)), 0.018), 'ahsap_koyu', 3, False)
    F([(-0.32, 0.24), (-0.04, 0.24), (-0.04, 0.3), (-0.3, 0.46), (-0.32, 0.44)], 'altin', 2)
    F(kol((-0.04, 0.27), (0.1, 0.4), 0.02), 'ahsap_koyu', 2, False)
    # the king drawing the bow: kilt, torso, the blue war crown, both arms out to the bow and the string
    F([(-0.24, 0.3), (-0.12, 0.3), (-0.13, 0.48), (-0.22, 0.48)], 'beyaz', 1)
    F([(-0.22, 0.47), (-0.13, 0.47), (-0.11, 0.68), (-0.23, 0.68)], 'kirmizi', 1)
    F([(-0.2, 0.67), (-0.13, 0.67), (-0.12, 0.76), (-0.2, 0.76)], 'kirmizi', 1)
    F([(-0.215, 0.75), (-0.12, 0.75), (-0.11, 0.82), (-0.15, 0.89), (-0.2, 0.88)], 'lacivert', 2)
    F(kol((-0.13, 0.65), (0.05, 0.66), 0.03), 'kirmizi', 2)
    F(kol((-0.13, 0.62), (-0.03, 0.64), 0.03), 'kirmizi', 2)
    for (a, b) in (((0.04, 0.42), (0.08, 0.55)), ((0.08, 0.55), (0.08, 0.77)), ((0.08, 0.77), (0.04, 0.9))):
        F(kol(a, b, 0.016), 'ahsap_koyu', 3, False)
    F(kol((0.04, 0.42), (-0.03, 0.645), 0.006), 'beyaz', 3, False)
    F(kol((0.04, 0.9), (-0.03, 0.645), 0.006), 'beyaz', 3, False)
    F(kol((-0.03, 0.645), (0.2, 0.65), 0.008), 'altin', 3, False)


def kule(x0, x1, h, bt=0.03, sx=1):
    B = dikdortgen(x0, x1, PY0, PY1, Z0); T = dikdortgen(x0 + bt, x1 - bt, PY0 + bt * 0.7, PY1 - bt * 0.7, Z0 + h)
    for i in range(4):
        j = (i + 1) % 4
        e = B[j] - B[i]; nn = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], TAS, nn + Z * 0.06)
    for i in range(4):
        boru(y, [B[i], T[i]], 0.009, 'kum_acik', n=6)
    silme(y, T, Z0 + h - 0.012, 0.012, 0.005, 'kum_acik', 'yarim')
    kavetto(T, Z0 + h, 0.05, 0.035, TAS)
    for k in range(1, 5):   # the joints of the paving slabs on the tower top
        yy_ = T[0].y + (T[3].y - T[0].y) * k / 5
        kutu(y, V(T[0].x + 0.015, yy_ - 0.0025, Z0 + h + 0.05), X, T[1].x - T[0].x - 0.03, 0.005, 0.002, 'kum_acik', 'onarkaust')
    nf = V(0, -h, bt * 0.7).normalized()
    P = lambda s, t, d=0.003: B[0].lerp(B[1], s / (x1 - x0)).lerp(T[0].lerp(T[1], s / (x1 - x0)), t / h) + nf * d
    W = x1 - x0
    boya(P, nf, 0.05, W - 0.05, 0.06, 0.5, 'kum_acik', 0.0015)
    araba_kabartma(P, nf, W / 2 + sx * 0.165 * 0.33, 0.085, 0.33, -sx)
    # above the scene: a register of hieroglyphs between two cartouches
    for m in range(13):
        s_ = 0.07 + m * (W - 0.14) / 12
        r = (m * 5 + (sx > 0)) % 4
        if m in (0, 12):
            boya(P, nf, s_ - 0.012, s_ + 0.012, 0.425, 0.475, 'beyaz', 0.0035); boya(P, nf, s_ - 0.008, s_ + 0.008, 0.43, 0.47, 'lacivert', 0.0045)
        elif r == 0: boya(P, nf, s_ - 0.007, s_ + 0.007, 0.435, 0.462, 'kum_koyu', 0.0035)
        elif r == 1: boya(P, nf, s_ - 0.01, s_ + 0.01, 0.444, 0.452, 'kum_koyu', 0.0035)
        elif r == 2: y.yuz_yon([P(s_ - 0.009, 0.435, 0.0035), P(s_ + 0.009, 0.435, 0.0035), P(s_, 0.465, 0.0035)], 'kum_koyu', nf)
        else: boya(P, nf, s_ - 0.004, s_ + 0.004, 0.432, 0.468, 'kum_koyu', 0.0035)
    # the back (towards the court): the same painted frieze, a framed register of the king offering, text columns
    nb = V(0, h, bt * 0.7).normalized()
    Pb = lambda s, t, d=0.003: B[2].lerp(B[3], s / W).lerp(T[2].lerp(T[3], s / W), t / h) + nb * d
    for t0, key in ((h * 0.8, 'lacivert'), (h * 0.84, 'boya_kirmizi'), (h * 0.88, 'turkuaz')):
        boya(Pb, nb, 0.04, W - 0.04, t0, t0 + h * 0.025, key)
    boya(Pb, nb, 0.06, W - 0.06, 0.08, 0.42, 'kum_acik', 0.0015)
    for m in range(7):
        s_ = 0.09 + m * (W - 0.18) / 6
        for k in range(9):
            t_ = 0.11 + k * 0.032
            r = (m * 3 + k * 5 + (sx > 0)) % 4
            if r == 0: boya(Pb, nb, s_ - 0.008, s_ + 0.008, t_, t_ + 0.016, 'kum_koyu', 0.0035)
            elif r == 1: boya(Pb, nb, s_ - 0.01, s_ + 0.01, t_ + 0.006, t_ + 0.012, 'kum_koyu', 0.0035)
            elif r == 2: y.yuz_yon([Pb(s_ - 0.009, t_, 0.0035), Pb(s_ + 0.009, t_, 0.0035), Pb(s_, t_ + 0.02, 0.0035)], 'kum_koyu', nb)
            else: boya(Pb, nb, s_ - 0.004, s_ + 0.004, t_, t_ + 0.02, 'lacivert', 0.0035)
    for t0, key in ((h * 0.8, 'lacivert'), (h * 0.84, 'boya_kirmizi'), (h * 0.88, 'turkuaz')):
        boya(P, nf, 0.04, W - 0.04, t0, t0 + h * 0.025, key)
    # two flagpoles against the front
    for k, u in enumerate((0.1, 0.9)):
        px = x0 + W * u
        py = PY0 + bt * 0.7 - 0.012
        top = Z0 + h + 0.24
        y.silindir((px, py), 0.006, Z0, top, 'ahsap', n=6)
        y.koni((px, py), 0.008, top, 0.022, 'altin', n=6)
        for t in (0.5, 0.75):
            p = P(W * u, h * t, 0.0)
            cubuk(y, V(px - 0.014, p.y + 0.002, p.z), V(px + 0.014, p.y + 0.002, p.z), 0.005, 'ahsap_koyu')
        if sx < 0 and k == 1:
            sancak(y, px, py, top - 0.16, boy=0.16, en=0.13, yuk=0.07, aci=-0.3)
        else:
            flama(px, py, top - 0.01, ['boya_kirmizi', 'beyaz', 'boya_sari', 'boya_yesil'][k + (0 if sx < 0 else 2)], aci=-0.3)


kule(-GX - 0.42, -GX, PH, sx=-1)
kule(GX, GX + 0.42, PH, sx=1)
GH = 0.43
kutu(y, V(-GX, PY0 - 0.02, Z0), X, 2 * GX, PY1 - PY0 + 0.04, GH, TAS, 'sagsolust')
for (a, b) in ((V(-GX, PY0 - 0.02), V(GX, PY0 - 0.02)), (V(GX, PY1 + 0.02), V(-GX, PY1 + 0.02))):
    W_, e_, nc_, L_ = dikdortgen_acik(y, a, b, Z0, GH, 0.24, 0.76, 0.0, 0.3, (TAS, 'kum_koyu', 'kum_acik', 'koyu'), derin=0.03, cerceve=(0.01, 'kum_acik'))
    o = (a + b) / 2 + Z * (Z0 + 0.36) + nc_ * 0.003
    y.yuz_yon([o + e_ * (0.018 * math.cos(TAU * i / 12)) + Z * (0.018 * math.sin(TAU * i / 12)) for i in range(12)], 'altin', nc_)
    for s in (-1, 1):
        y.yuz_yon([o + e_ * (s * 0.02) - Z * 0.01, o + e_ * (s * 0.11), o + e_ * (s * 0.11) + Z * 0.016, o + e_ * (s * 0.02) + Z * 0.012], 'lacivert', nc_)
silme(y, dikdortgen(-GX, GX, PY0 - 0.02, PY1 + 0.02), Z0 + GH - 0.01, 0.01, 0.005, 'kum_acik', 'yarim')
kavetto(dikdortgen(-GX, GX, PY0 - 0.02, PY1 + 0.02), Z0 + GH, 0.04, 0.028, TAS)
# the gate leaves standing open inside
for s in (-1, 1):
    kutu_merkez(y, (s * (GX * 0.52 + 0.04), PY1 + 0.07), 0.008, 0.12, 0.3, 'ahsap', z0=Z0, aci=s * 0.25)

# ---------------------------------------------------------------- the stable hall
y.bolum('Ahir')
SX0, SX1, SY0, SY1 = -0.88, 0.88, 0.58, 0.98
SH = 0.22
ks = dikdortgen(SX0, SX1, SY0, SY1)
for i in (1, 2, 3):
    a, b = ks[i], ks[(i + 1) % 4]
    L = (b - a).length; n = max(1, int(L / 0.2))
    for m in range(n):
        dikdortgen_acik(y, a.lerp(b, m / n), a.lerp(b, (m + 1) / n), Z0, SH, 0.38, 0.62, SH * 0.6, SH * 0.82, (SIV, 'kerpic_koyu', 'kerpic', 'koyu'), derin=0.015)
# the front wall (under the portico): a stall door per bay
NB = 8
for m in range(NB):
    a, b = ks[0].lerp(ks[1], m / NB), ks[0].lerp(ks[1], (m + 1) / NB)
    dikdortgen_acik(y, a, b, Z0, SH, 0.24, 0.76, 0.0, SH * 0.72, (SIV, 'kerpic_koyu', 'kerpic', 'koyu'), derin=0.03, cerceve=(0.008, 'kirec'))
silme(y, ks, Z0, 0.025, 0.006, 'kerpic_koyu', 'kaide')
kavetto(ks, Z0 + SH, 0.035, 0.022, SIV)
# the clerestory: a raised central block with grilled windows
CX0, CX1, CY0, CY1 = -0.4, 0.4, 0.66, 0.92
ZC = Z0 + SH + 0.035
kc = dikdortgen(CX0, CX1, CY0, CY1)
CH = 0.1
for i in range(4):
    a, b = kc[i], kc[(i + 1) % 4]
    L = (b - a).length; n = max(1, int(L / 0.13))
    for m in range(n):
        p, q = a.lerp(b, m / n), a.lerp(b, (m + 1) / n)
        dikdortgen_acik(y, p, q, ZC, CH, 0.2, 0.8, 0.02, CH - 0.022, (SIV, 'kerpic_koyu', 'kerpic', 'koyu'), derin=0.015)
        kafes(y, p, q, ZC, 0.2, 0.8, 0.02, CH - 0.022, 'kirec', nu=5, nv=1, en=0.008, ileri=0.004)
kavetto(kc, ZC + CH, 0.03, 0.02, SIV)
# the shade portico: papyrus columns, an architrave, a reed-mat roof on beams
PY = SY0 - 0.15
for m in range(NB + 1):
    px = SX0 + (SX1 - SX0) * m / NB
    sutun(y, px, PY, Z0, Z0 + SH - 0.02, 0.017, 'kirec', 'misir', bant_key='boya_kirmizi')
kutu(y, V(SX0 - 0.025, PY - 0.022, Z0 + SH - 0.02), X, SX1 - SX0 + 0.05, 0.044, 0.025, 'kirec')
for m in range(NB * 2 + 1):   # the beams from the architrave to the wall
    px = SX0 + (SX1 - SX0) * m / (NB * 2)
    cubuk(y, V(px, PY, Z0 + SH + 0.009), V(px, SY0, Z0 + SH + 0.009), 0.008, 'ahsap_koyu')
kutu(y, V(SX0 - 0.025, PY - 0.03, Z0 + SH + 0.013), X, SX1 - SX0 + 0.05, SY0 - PY + 0.03, 0.006, 'saz')
y.yuz_yon([V(SX0 - 0.025, PY - 0.03, Z0 + SH + 0.0125), V(SX1 + 0.025, PY - 0.03, Z0 + SH + 0.0125), V(SX1 + 0.025, SY0, Z0 + SH + 0.0125), V(SX0 - 0.025, SY0, Z0 + SH + 0.0125)], 'saz_koyu', -Z)
# stone mangers and the horses tethered in the shade
for m in range(NB):
    px = SX0 + (SX1 - SX0) * (m + 0.5) / NB
    kutu_merkez(y, (px, SY0 - 0.025), 0.12, 0.035, 0.03, 'kirec', z0=Z0)
    kutu_merkez(y, (px, SY0 - 0.025), 0.1, 0.022, 0.002, 'boya_sari', z0=Z0 + 0.03)
    if m % 3 != 1:
        at(px + 0.01 * (m % 2), SY0 - 0.12, Z0, math.pi / 2 + 0.15 * ((m % 3) - 1), 'ahsap' if m % 2 else 'ahsap_acik', tuy=False, olcek=1.1)

# ---------------------------------------------------------------- the chariot shed (left)
y.bolum('Araba sundurmasi')
AX0, AX1, AY0, AY1 = -1.0, -0.62, -0.62, 0.3
AH = 0.18
duz_duvar(y, V(AX0, AY1), V(AX0, AY0), Z0, Z0 + AH, KER)
duz_duvar(y, V(AX0, AY0), V(AX1, AY0), Z0, Z0 + AH, KER)
duz_duvar(y, V(AX1, AY1), V(AX0, AY1), Z0, Z0 + AH, KER)
duz_duvar(y, V(AX0 + 0.03, AY0 + 0.03), V(AX0 + 0.03, AY1 - 0.03), Z0, Z0 + AH, SIV)       # the inner face of the back wall
duz_duvar(y, V(AX1, AY0 + 0.03), V(AX0 + 0.03, AY0 + 0.03), Z0, Z0 + AH, SIV)
duz_duvar(y, V(AX0 + 0.03, AY1 - 0.03), V(AX1, AY1 - 0.03), Z0, Z0 + AH, SIV)
for yy, s in ((AY0, -1), (AY1, 1)):
    y.yuz_yon([V(AX1, yy, Z0), V(AX1, yy - s * 0.03, Z0), V(AX1, yy - s * 0.03, Z0 + AH), V(AX1, yy, Z0 + AH)], KER, X)
for (x0_, x1_, y0_, y1_) in ((AX0, AX0 + 0.03, AY0, AY1), (AX0 + 0.03, AX1, AY0, AY0 + 0.03), (AX0 + 0.03, AX1, AY1 - 0.03, AY1)):
    y.yuz([V(x0_, y0_, Z0 + AH), V(x1_, y0_, Z0 + AH), V(x1_, y1_, Z0 + AH), V(x0_, y1_, Z0 + AH)], KER)
for m in range(5):
    sutun(y, AX1, AY0 + 0.03 + (AY1 - AY0 - 0.06) * m / 4, Z0, Z0 + AH, 0.015, 'kirec', 'misir', bant_key='turkuaz')
# the roof: an architrave on the columns, rafters, a reed mat over the back half (the chariots show through the front)
kutu(y, V(AX1 + 0.018, AY0 - 0.02, Z0 + AH), Y, AY1 - AY0 + 0.04, 0.036, 0.022, 'kirec')
kutu(y, V(AX0 + 0.03, AY0 - 0.02, Z0 + AH), Y, AY1 - AY0 + 0.04, 0.05, 0.016, 'kirec')
for m in range(17):
    yy = AY0 - 0.01 + (AY1 - AY0 + 0.02) * m / 16
    cubuk(y, V(AX0 - 0.01, yy, Z0 + AH + 0.026), V(AX1 + 0.03, yy, Z0 + AH + 0.026), 0.008, 'ahsap_koyu')
kutu(y, V(AX0 - 0.012, AY0 - 0.015, Z0 + AH + 0.031), X, 0.2, AY1 - AY0 + 0.03, 0.006, 'saz')
y.yuz_yon([V(AX0 - 0.012, AY0 - 0.015, Z0 + AH + 0.0305), V(AX0 + 0.188, AY0 - 0.015, Z0 + AH + 0.0305), V(AX0 + 0.188, AY1 + 0.015, Z0 + AH + 0.0305), V(AX0 - 0.012, AY1 + 0.015, Z0 + AH + 0.0305)], 'saz_koyu', -Z)
# parked chariots, poles tipped up, and spare wheels on the wall
for yy in (-0.44, -0.16, 0.12):
    araba(-0.86, yy, Z0, 0.0, atli=False, surucu=False, eg=0.06)
for yy in (-0.52, 0.22):
    tekerlek((AX0 + 0.045, yy, Z0 + 0.09), 0.038)

# ---------------------------------------------------------------- the tack and bow store, the well (right)
y.bolum('Silah deposu')
DX0, DX1, DY0, DY1 = 0.64, 1.0, -0.5, 0.18
DH = 0.19
kd = dikdortgen(DX0, DX1, DY0, DY1)
for i in range(4):
    a, b = kd[i], kd[(i + 1) % 4]
    if i == 3:
        L = (b - a).length
        dikdortgen_acik(y, a, a.lerp(b, 0.5), Z0, DH, 0.3, 0.7, 0.0, DH * 0.68, (SIV, 'kerpic_koyu', 'kerpic', 'ahsap_koyu'), derin=0.02, cerceve=(0.008, 'kirec'))
        dikdortgen_acik(y, a.lerp(b, 0.5), b, Z0, DH, 0.35, 0.65, DH * 0.55, DH * 0.8, (SIV, 'kerpic_koyu', 'kerpic', 'koyu'), derin=0.015)
    else:
        duz_duvar(y, a, b, Z0, Z0 + DH, SIV)
silme(y, kd, Z0, 0.02, 0.005, 'kerpic_koyu', 'kaide')
kavetto(kd, Z0 + DH, 0.03, 0.02, SIV)
# racks of spears and bows by the door, shields
for m in range(6):
    yy = DY0 + 0.04 + m * 0.018
    boru(y, [V(DX0 - 0.012, yy, Z0), V(DX0 - 0.004, yy, Z0 + 0.15)], 0.0018, 'ahsap', n=3)
    y.koni((DX0 - 0.004, yy), 0.004, Z0 + 0.15, 0.014, 'bronz', n=4)
cubuk(y, V(DX0 - 0.012, DY0 + 0.03, Z0 + 0.09), V(DX0 - 0.012, DY0 + 0.15, Z0 + 0.09), 0.004, 'ahsap_koyu')
for m in range(3):   # cowhide shields, round-topped
    yy = -0.05 + m * 0.06
    with parca(y, (DX0 - 0.006, yy, Z0 + 0.02), 0.0):
        y.yuz_yon([V(0, -0.016, 0), V(0, 0.016, 0), V(0, 0.016, 0.04), V(0, 0.0, 0.052), V(0, -0.016, 0.04)], 'kumas', -X)
        y.yuz_yon([V(-0.001, -0.008, 0.012), V(-0.001, 0.008, 0.012), V(-0.001, 0.008, 0.03), V(-0.001, -0.008, 0.03)], 'ahsap_koyu', -X)
# the well with a shaduf and a long trough
WX, WY = 0.78, 0.35
halka_kornis(y, (WX, WY), 0.05, Z0, 0.035, 0.012, 12, 'kirec')
y.yuz_yon(cokgen((WX, WY), 0.05, 12, z=Z0 + 0.03), 'su', Z)
for s in (-1, 1):
    cubuk(y, V(WX + 0.08, WY + s * 0.03, Z0), V(WX + 0.08, WY + s * 0.03, Z0 + 0.13), 0.01, 'ahsap')
cubuk(y, V(WX + 0.08, WY - 0.04, Z0 + 0.13), V(WX + 0.08, WY + 0.04, Z0 + 0.13), 0.009, 'ahsap')
boru(y, [V(WX + 0.2, WY, Z0 + 0.06), V(WX, WY, Z0 + 0.2)], 0.004, 'ahsap_koyu', n=5)
kure(y, (WX + 0.21, WY, Z0 + 0.055), 0.022, 'kerpic_koyu', n=8, kat=4)
boru(y, [V(WX, WY, Z0 + 0.2), V(WX, WY, Z0 + 0.07)], 0.0012, 'saz_koyu', n=3)
kutu(y, V(0.3, 0.4, Z0), X, 0.36, 0.05, 0.035, 'kirec', 'onarkasagsolust')
y.yuz([V(0.31, 0.41, Z0 + 0.03), V(0.65, 0.41, Z0 + 0.03), V(0.65, 0.44, Z0 + 0.03), V(0.31, 0.44, Z0 + 0.03)], 'su')
at(0.4, 0.33, Z0, math.pi / 2, 'ahsap_acik', tuy=False)
at(0.55, 0.32, Z0, math.pi / 2 + 0.2, 'ahsap', tuy=False)

# ---------------------------------------------------------------- the training track
y.bolum('Talim alani')
TC = (0.0, -0.2)
# an oval track of trodden sand with a low kerb, turning posts at both ends
def oval(rx, ry, n=28):
    return [V(TC[0] + rx * math.cos(TAU * i / n), TC[1] + ry * math.sin(TAU * i / n)) for i in range(n)]
dis_, ic_ = oval(0.5, 0.3), oval(0.36, 0.17)
for i in range(len(dis_)):
    j = (i + 1) % len(dis_)
    y.yuz_yon([dis_[i] + Z * (Z0 + 0.002), dis_[j] + Z * (Z0 + 0.002), ic_[j] + Z * (Z0 + 0.002), ic_[i] + Z * (Z0 + 0.002)], 'toprak', Z)
silme(y, ic_, Z0, 0.012, 0.008, 'kerpic', 'yarim')
for s in (-1, 1):
    px = TC[0] + s * 0.43
    kutu_merkez(y, (px, TC[1]), 0.04, 0.04, 0.02, 'kirec', z0=Z0)
    dikilitas(y, (px, TC[1]), 0.022, 0.13, 'kirmizi_tas', 'altin', z0=Z0 + 0.02, kaide=False)
# a span galloping round, and an archery target with a trainer
araba(-0.08, TC[1] + 0.235, Z0, 0.0, kosu=True)
kutu_merkez(y, (-0.08, TC[1] + 0.02), 0.012, 0.012, 0.09, 'ahsap', z0=Z0)
kutu_merkez(y, (-0.08, TC[1] + 0.02), 0.012, 0.07, 0.07, 'bronz', z0=Z0 + 0.04)
kutu_merkez(y, (-0.08, TC[1] + 0.02), 0.014, 0.03, 0.03, 'boya_kirmizi', z0=Z0 + 0.06)
# fodder on the roofs: bundles of clover and straw drying
for (px, py) in ((-0.7, 0.88), (-0.62, 0.9), (0.55, 0.7), (0.65, 0.84), (0.72, 0.72)):
    donel(y, (px, py), [(0.03, Z0 + SH + 0.035), (0.028, Z0 + SH + 0.05), (0.016, Z0 + SH + 0.066), (0, Z0 + SH + 0.07)], 'saz', n=8)
for (px, py) in ((0.75, -0.3), (0.86, -0.22), (0.9, 0.05)):
    donel(y, (px, py), [(0.026, Z0 + DH + 0.03), (0.024, Z0 + DH + 0.042), (0.012, Z0 + DH + 0.056), (0, Z0 + DH + 0.06)], 'saz_koyu', n=8)
# wind catchers (malqaf) on the roofs, their mouths turned to the north breeze, and reed mats of fodder spread to dry
def malkaf(x, yy, z, w=0.07, d=0.05, h=0.1, key=SIV):
    x0, x1, y0, y1 = x - w / 2, x + w / 2, yy - d / 2, yy + d / 2
    zt, zb = z + h + 0.028, z + h
    y.yuz_yon([V(x0, y0, z), V(x0, y1, z), V(x0, y1, zt), V(x0, y0, zb)], key, -X)
    y.yuz_yon([V(x1, y0, z), V(x1, y1, z), V(x1, y1, zt), V(x1, y0, zb)], key, X)
    y.yuz_yon([V(x0, y1, z), V(x1, y1, z), V(x1, y1, zt), V(x0, y1, zt)], key, Y)
    zm = z + h * 0.42
    y.yuz_yon([V(x0, y0, z), V(x1, y0, z), V(x1, y0, zm), V(x0, y0, zm)], key, -Y)
    y.yuz_yon([V(x0 + 0.006, y0 + 0.012, zm), V(x1 - 0.006, y0 + 0.012, zm), V(x1 - 0.006, y0 + 0.012, zb), V(x0 + 0.006, y0 + 0.012, zb)], 'koyu', -Y)
    for xa, xb, s in ((x0, x0 + 0.006, 1), (x1 - 0.006, x1, -1)):
        y.yuz_yon([V(xa, y0, zm), V(xb, y0, zm), V(xb, y0, zb), V(xa, y0, zb)], key, -Y)
        xi = xb if s > 0 else xa
        y.yuz_yon([V(xi, y0, zm), V(xi, y0 + 0.012, zm), V(xi, y0 + 0.012, zb), V(xi, y0, zb)], key, V(s, 0, 0))
    y.yuz_yon([V(x0 + 0.006, y0, zm), V(x1 - 0.006, y0, zm), V(x1 - 0.006, y0 + 0.012, zm), V(x0 + 0.006, y0 + 0.012, zm)], key, Z)
    o = 0.008
    R = [V(x0 - o, y0 - o * 1.5, zb), V(x1 + o, y0 - o * 1.5, zb), V(x1 + o, y1 + o, zt), V(x0 - o, y1 + o, zt)]
    y.yuz_yon([p + Z * 0.006 for p in R], 'ahsap_koyu', Z)
    y.yuz_yon(R, 'ahsap_koyu', -Z)
    for i in range(4):
        j = (i + 1) % 4
        e = R[j] - R[i]; nn = V(e.y, -e.x)
        y.yuz_yon([R[i], R[j], R[j] + Z * 0.006, R[i] + Z * 0.006], 'ahsap_koyu', nn)
ZH = Z0 + SH + 0.035
for (mx, my) in ((-0.75, 0.72), (-0.5, 0.76), (0.52, 0.8), (0.82, 0.7)):
    malkaf(mx, my, ZH)
malkaf(0.95, -0.35, Z0 + DH + 0.03, 0.06, 0.045, 0.085)
for (x0_, x1_, y0_, y1_) in ((-0.84, -0.6, 0.62, 0.69), (0.45, 0.82, 0.62, 0.68), (-0.84, -0.66, 0.86, 0.95)):
    y.yuz([V(x0_, y0_, ZH + 0.002), V(x1_, y0_, ZH + 0.002), V(x1_, y1_, ZH + 0.002), V(x0_, y1_, ZH + 0.002)], 'saz')
    for k in range(int((x1_ - x0_) / 0.03)):
        xx = x0_ + 0.015 + k * 0.03
        y.yuz([V(xx, y0_ + 0.004, ZH + 0.0035), V(xx + 0.012, y0_ + 0.004, ZH + 0.0035), V(xx + 0.012, y1_ - 0.004, ZH + 0.0035), V(xx, y1_ - 0.004, ZH + 0.0035)], 'boya_yesil' if k % 2 else 'saz_koyu')
# palms outside the wall
for (px, py, b) in ((-0.5, -1.02, 0.2), (-0.75, -0.98, 0.17), (0.48, -1.04, 0.19), (0.8, -0.98, 0.16), (1.1, -0.95, 0.18), (-1.1, -0.95, 0.18)):
    agac(y, px, py, Z0, b, 'palmiye')

calistir(y, 'lm_arabaciahiri')
