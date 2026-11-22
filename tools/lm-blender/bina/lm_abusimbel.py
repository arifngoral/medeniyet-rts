# Abu Simbel (lm_abusimbel): the rock-cut temples of Ramesses II above the Nile. The great temple's battered facade cut
# into the sandstone hill: four seated colossi of the king (nemes, double crown, false beard, hands on the knees, family
# statues at the feet; the second from the left broken, its head lying on the terrace), the door and the niche of
# Ra-Horakhty, cartouche frieze, torus, cavetto and the row of adoring baboons; the terrace with falcons and its stair to
# the river. Beside it the small temple of Nefertari: six standing statues between battered buttresses.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from mathutils import Matrix
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05            # river bank
ZW = 0.012           # the Nile
HT = 'kum_acik'      # statue stone
FT = 'kum'           # facade stone
KY = 'kaya'          # the hill

KAVETTO = [(0, 0), (0.16, 0.03), (0.2, 0.1), (0.12, 0.17), (0.04, 0.19), (0.07, 0.36), (0.18, 0.56), (0.4, 0.75),
           (0.72, 0.88), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]


# ---------------------------------------------------------------- helpers
def levha(P, s0, s1, t0, t1, key, n, d=0.003):
    y.yuz_yon([P(s0, t0, d), P(s1, t0, d), P(s1, t1, d), P(s0, t1, d)], key, n)


def donustur(bas, M, t):
    """turn the faces added since index bas by the rotation M about the origin, then move them by t"""
    t = Vector(t)
    for i in range(bas, len(y.faces)):
        pts, key = y.faces[i]
        y.faces[i] = ([tuple(M @ Vector(p) + t) for p in pts], key)


def halka(cx, cy, z, hw, hd, n=16, p=2.4):
    """a superellipse ring (CCW): hw half width (x), hd half depth (y); p > 2 squarer"""
    out = []
    for i in range(n):
        a = TAU * i / n
        c, s = math.cos(a), math.sin(a)
        out.append(V(cx + hw * math.copysign(abs(c) ** (2 / p), c), cy + hd * math.copysign(abs(s) ** (2 / p), s), z))
    return out


def plaka(pts, key, yon, kalin=0.003):
    """a thin closed plate: the face pts toward yon, its back kalin behind, the rims round it"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    arka = [p - yon * kalin for p in pts]
    y.yuz_yon(pts, key, yon); y.yuz_yon(arka, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        y.yuz_yon([pts[i], pts[j], arka[j], arka[i]], key, (pts[i] + pts[j]) / 2 - c)


def halka_kapak(dis_, ic_, key, yon):
    """the flat strip between two rings of the same length (the top of a band laid round a body)"""
    for i in range(len(dis_)):
        j = (i + 1) % len(dis_)
        y.yuz_yon([dis_[i], dis_[j], ic_[j], ic_[i]], key, yon)


def loft(halkalar, keys, kapak=None):
    """bands between successive rings (bottom to top); keys: one key or a list per band; kapak: cap the top ring"""
    for k in range(len(halkalar) - 1):
        y.serit(halkalar[k], halkalar[k + 1], keys[k % len(keys)] if isinstance(keys, list) else keys)
    if kapak:
        y.yuz_yon(halkalar[-1], kapak, Z)


def yazi_sutunu(P, n, s0, t0, t1, w=0.012, key='kum_koyu', adim=0.016, d=0.003, tohum=0):
    """a vertical column of hieroglyphs: small marks of varying shape"""
    k = 0
    t = t1 - adim
    while t > t0:
        r = (tohum * 7 + k * 13) % 5
        if r == 0: levha(P, s0, s0 + w, t, t + adim * 0.55, key, n, d)
        elif r == 1: levha(P, s0 + w * 0.2, s0 + w * 0.8, t, t + adim * 0.7, key, n, d)
        elif r == 2:
            levha(P, s0, s0 + w * 0.42, t, t + adim * 0.6, key, n, d); levha(P, s0 + w * 0.58, s0 + w, t + adim * 0.15, t + adim * 0.7, key, n, d)
        elif r == 3: levha(P, s0, s0 + w, t + adim * 0.25, t + adim * 0.45, key, n, d)
        else: y.yuz_yon([P(s0, t, d), P(s0 + w, t, d), P(s0 + w / 2, t + adim * 0.7, d)], key, n)
        t -= adim; k += 1


def yazi_bandi(P, n, s0, s1, t0, h, key='kum_koyu', d=0.003, tohum=0):
    """a horizontal register of hieroglyphs between s0 and s1"""
    w = h * 0.7; s = s0; k = 0
    while s + w < s1:
        r = (tohum * 5 + k * 7) % 4
        if r == 0: levha(P, s, s + w, t0, t0 + h, key, n, d)
        elif r == 1: levha(P, s, s + w, t0 + h * 0.3, t0 + h * 0.6, key, n, d)
        elif r == 2: y.yuz_yon([P(s, t0, d), P(s + w, t0, d), P(s + w * 0.5, t0 + h, d)], key, n)
        else: levha(P, s + w * 0.3, s + w * 0.7, t0, t0 + h, key, n, d)
        s += w * 1.5; k += 1


def kartus(P, n, sc, t0, w, h, d=0.003, tohum=0):
    """a royal cartouche: an oval ring with a bar under it, glyphs inside"""
    k = 12
    dis_ = [(sc + w / 2 * math.cos(TAU * i / k), t0 + h / 2 + h / 2 * math.sin(TAU * i / k)) for i in range(k)]
    ic_ = [(sc + (w / 2 - w * 0.14) * math.cos(TAU * i / k), t0 + h / 2 + (h / 2 - w * 0.14) * math.sin(TAU * i / k)) for i in range(k)]
    for i in range(k):
        j = (i + 1) % k
        y.yuz_yon([P(*dis_[i], d), P(*dis_[j], d), P(*ic_[j], d), P(*ic_[i], d)], 'kum_koyu', n)
    y.yuz_yon([P(*q, d) for q in ic_], 'boya_sari', n)
    levha(P, sc - w * 0.45, sc + w * 0.45, t0 - h * 0.08, t0 + h * 0.02, 'kum_koyu', n, d)
    for m in range(3):
        tt = t0 + h * (0.22 + m * 0.22)
        r = (tohum + m) % 3
        if r == 0: levha(P, sc - w * 0.12, sc + w * 0.12, tt, tt + h * 0.14, 'boya_kirmizi', n, d + 0.0008)
        elif r == 1: levha(P, sc - w * 0.2, sc + w * 0.2, tt + h * 0.04, tt + h * 0.1, 'lacivert', n, d + 0.0008)
        else: y.yuz_yon([P(sc - w * 0.15, tt, d + 0.0008), P(sc + w * 0.15, tt, d + 0.0008), P(sc, tt + h * 0.15, d + 0.0008)], 'boya_kirmizi', n)


# ---------------------------------------------------------------- the seated colossus (statue units: 1 = to the crown top)
def bas_ve_tac(K=HT):
    """head, nemes, beard, uraeus and double crown of the king (statue units, facing -y, centred on x = 0)"""
    # neck and head (an egg)
    boru(y, [V(0, -0.12, 0.6), V(0, -0.125, 0.675)], 0.042, K, n=10)
    donel(y, (0, -0.13), [(0, 0.628), (0.036, 0.634), (0.051, 0.66), (0.055, 0.695), (0.05, 0.73), (0.03, 0.752), (0, 0.758)], K, n=12)
    # face: arched brows, almond eyes lined in kohl with dark pupils, a straight nose, full lips with the archaic smile
    def yuzde(x, z, d=0.0015):   # a point on the face's surface (the egg) at x, z, d in front of it
        pr_ = [(0.634, 0.036), (0.66, 0.051), (0.695, 0.055), (0.73, 0.05), (0.752, 0.03)]
        r_ = pr_[0][1]
        for (za_, ra_), (zb_, rb_) in zip(pr_, pr_[1:]):
            if za_ <= z <= zb_: r_ = ra_ + (rb_ - ra_) * (z - za_) / (zb_ - za_)
        return V(x, -0.13 - math.sqrt(max(1e-6, r_ * r_ - x * x)) - d, z)
    for sg in (-1, 1):
        kas = [yuzde(sg * 0.009, 0.711), yuzde(sg * 0.02, 0.716), yuzde(sg * 0.034, 0.712), yuzde(sg * 0.034, 0.709), yuzde(sg * 0.02, 0.712), yuzde(sg * 0.009, 0.708)]
        y.yuz_yon(kas, 'kum_koyu', -Y)
        goz = [yuzde(sg * 0.01, 0.699), yuzde(sg * 0.02, 0.704), yuzde(sg * 0.033, 0.701), yuzde(sg * 0.02, 0.695)]
        y.yuz_yon(goz, 'beyaz', -Y)
        y.yuz_yon([yuzde(sg * 0.033, 0.701, 0.0022), yuzde(sg * 0.04, 0.699, 0.0022), yuzde(sg * 0.04, 0.6975, 0.0022), yuzde(sg * 0.031, 0.6995, 0.0022)], 'koyu', -Y)
        y.yuz_yon([yuzde(sg * 0.0165, 0.696, 0.002), yuzde(sg * 0.0235, 0.696, 0.002), yuzde(sg * 0.0235, 0.703, 0.002), yuzde(sg * 0.0165, 0.703, 0.002)], 'koyu', -Y)
    cubuk(y, V(0, -0.183, 0.708), V(0, -0.193, 0.678), 0.012, K, 0.011)                     # the nose
    cubuk(y, V(-0.007, -0.19, 0.677), V(0.007, -0.19, 0.677), 0.006, K, 0.006)             # its wings
    dud = [(-0.016, 0.664), (-0.006, 0.667), (0.0, 0.666), (0.006, 0.667), (0.016, 0.664), (0.008, 0.66), (-0.008, 0.66)]
    y.yuz_yon([yuzde(x_, z_, 0.002) for x_, z_ in dud], 'kirmizi', -Y)
    y.yuz_yon([yuzde(-0.012, 0.6635, 0.0026), yuzde(0.012, 0.6635, 0.0026), yuzde(0.012, 0.6645, 0.0026), yuzde(-0.012, 0.6645, 0.0026)], 'koyu', -Y)
    cubuk(y, V(0, -0.176, 0.652), V(0, -0.18, 0.645), 0.026, K, 0.012)                       # the chin
    # nemes headcloth: a striped hood flaring to the shoulders
    seviyeler = [(0.585, 0.14, 0.052, -0.1), (0.6, 0.135, 0.056, -0.1), (0.625, 0.112, 0.058, -0.098), (0.65, 0.095, 0.06, -0.096),
                 (0.67, 0.083, 0.062, -0.096), (0.69, 0.076, 0.063, -0.097), (0.71, 0.072, 0.064, -0.1), (0.73, 0.066, 0.064, -0.104),
                 (0.748, 0.056, 0.058, -0.11), (0.762, 0.034, 0.04, -0.115), (0.768, 0.0, 0.0, -0.118)]
    hs = []
    for z, hw, hd, cy in seviyeler:
        hs.append(halka(0, cy, z, max(hw, 1e-4), max(hd, 1e-4), n=16, p=2.2))
    for k in range(len(hs) - 1):
        key = K if k % 2 else 'kum'
        if k == len(hs) - 2:
            for i in range(16):
                y.yuz_yon([hs[k][i], hs[k][(i + 1) % 16], hs[k + 1][0]], key, hs[k][i] - V(0, -0.115, 0.74))
        else:
            y.serit(hs[k], hs[k + 1], key)
    y.yuz_yon(hs[0], 'kum', -Z)   # (its underside: seen when the head lies fallen)
    # the forehead band of the nemes
    boru(y, [V(-0.06, -0.163, 0.72), V(-0.03, -0.18, 0.735), V(0.03, -0.18, 0.735), V(0.06, -0.163, 0.72)], 0.006, K, n=6)
    # lappets falling on the chest, striped
    for sg in (-1, 1):
        a, b = V(sg * 0.088, -0.168, 0.645), V(sg * 0.098, -0.208, 0.48)
        for m in range(6):
            cubuk(y, a.lerp(b, m / 6), a.lerp(b, (m + 1) / 6), 0.044, K if m % 2 else 'kum', 0.016)
    # false beard, uraeus
    cubuk(y, V(0, -0.168, 0.646), V(0, -0.176, 0.598), 0.022, 'kum', 0.02)
    boru(y, [V(0, -0.176, 0.722), V(0, -0.186, 0.742), V(0, -0.182, 0.762), V(0, -0.176, 0.768)], 0.0065, 'altin', n=6)
    kure(y, (0, -0.178, 0.77), 0.009, 'altin', n=8, kat=4)
    # double crown: the red crown of Lower Egypt round the white crown of Upper Egypt
    donel(y, (0, -0.112), [(0, 0.748), (0.06, 0.748), (0.062, 0.79), (0.064, 0.826), (0.046, 0.826), (0, 0.826)], 'kirmizi', n=14)
    kutu_merkez(y, (0, -0.06), 0.05, 0.026, 0.13, 'kirmizi', z0=0.79)
    boru(y, [V(0, -0.158, 0.8), V(0, -0.176, 0.83), V(0, -0.19, 0.86), V(0, -0.18, 0.88), V(0, -0.168, 0.874)], 0.005, 'kirmizi', n=5)
    donel(y, (0, -0.115), [(0, 0.827), (0.046, 0.827), (0.048, 0.87), (0.042, 0.93), (0.03, 0.968), (0.02, 0.985), (0, 0.99)], 'mermer', n=14)
    kure(y, (0, -0.115, 0.99), 0.019, 'mermer', n=10, kat=5)


def oturan_kolos(px, py, pz, s, kirik=False):
    """a seated colossus of Ramesses II (built facing -y; back at y = 0 against the facade)"""
    K = HT
    with parca(y, (px, py, pz), 0.0, s):
        # the throne block and its back slab merging into the facade
        kutu_merkez(y, (0, -0.15), 0.4, 0.3, 0.34, K)
        kutu_merkez(y, (0, 0.02), 0.3, 0.14, 0.5 if kirik else 0.64, K)
        for sg in (-1, 1):   # sema-tawy relief on the throne's sides: two Nile gods binding the Two Lands
            Pt = lambda s_, t_, d=0.002, sg=sg: V(sg * 0.2, -s_, t_) + X * (sg * d)
            levha(Pt, 0.025, 0.275, 0.03, 0.31, FT, X * sg, 0.0015)
            levha(Pt, 0.14, 0.16, 0.05, 0.27, 'kum_koyu', X * sg)
            levha(Pt, 0.11, 0.19, 0.25, 0.27, 'kum_koyu', X * sg)
            for c_ in (0.075, 0.225):
                levha(Pt, c_ - 0.022, c_ + 0.022, 0.05, 0.2, 'boya_kirmizi', X * sg)
                levha(Pt, c_ - 0.012, c_ + 0.012, 0.2, 0.235, 'boya_kirmizi', X * sg)
                levha(Pt, c_ - 0.03, c_ + 0.03, 0.12, 0.135, 'boya_yesil', X * sg, 0.0035)
        # feet, shins, knees, thighs
        for sg in (-1, 1):
            xl = sg * 0.075
            kutu_merkez(y, (xl, -0.375), 0.068, 0.12, 0.034, K)
            boru(y, [V(xl - 0.032, -0.435, 0.016), V(xl + 0.032, -0.435, 0.016)], 0.016, K, n=6)
            boru(y, [V(xl, -0.355, 0.03), V(xl, -0.362, 0.17), V(xl, -0.356, 0.3)], 0.034, K, n=8, r_son=0.043)
            kure(y, (xl, -0.352, 0.312), 0.047, K, n=8, kat=5)
            boru(y, [V(xl, -0.35, 0.325), V(xl * 1.08, -0.2, 0.336), V(xl * 1.12, -0.07, 0.342)], 0.05, K, n=8, r_son=0.058)
        # the pleated kilt over the lap, belt and the apron between the knees
        kx, k0, k1 = 0.138, -0.33, -0.06
        L0, L1 = V(0, k0), V(0, k1)
        zf, zb = 0.372, 0.398
        q = [V(-kx, k0, zf), V(kx, k0, zf), V(kx, k1, zb), V(-kx, k1, zb)]
        y.yuz_yon(q, K, Z)
        y.yuz_yon([V(-kx, k0, 0.33), V(kx, k0, 0.33), V(kx, k0, zf), V(-kx, k0, zf)], K, -Y)
        for sg in (-1, 1):
            y.yuz_yon([V(sg * kx, k0, 0.33), V(sg * kx, k1, 0.33), V(sg * kx, k1, zb), V(sg * kx, k0, zf)], K, X * sg)
        for m in range(1, 8):
            xx = -kx + 2 * kx * m / 8
            cubuk(y, V(xx, k0 + 0.004, zf + 0.002), V(xx, k1, zb + 0.002), 0.004, 'kum', 0.003)
        y.yuz_yon([V(-0.028, k0 - 0.004, zf), V(0.028, k0 - 0.004, zf), V(0.036, k0 - 0.012, 0.19), V(-0.036, k0 - 0.012, 0.19)], 'kum', -Y)
        for sg in (-1, 1):
            y.yuz_yon([V(sg * 0.028, k0 - 0.004, zf), V(sg * 0.036, k0 - 0.012, 0.19), V(sg * 0.036, k0, 0.19), V(sg * 0.028, k0, zf)], 'kum', X * sg)
        # torso
        tz = [(0.37, 0.1, 0.068, -0.112), (0.42, 0.102, 0.07, -0.114), (0.47, 0.11, 0.074, -0.117), (0.52, 0.128, 0.08, -0.12),
              (0.56, 0.143, 0.08, -0.12), (0.59, 0.148, 0.074, -0.118), (0.615, 0.12, 0.062, -0.116), (0.632, 0.055, 0.046, -0.118)]
        if kirik:
            tz = tz[:3]
        hs = [halka(0, cy, z, hw, hd, n=16, p=2.6) for z, hw, hd, cy in tz]
        loft(hs, K, None)
        # belt with the cartouche buckle
        def govde(z):   # the torso ring at height z
            for (za, wa, da, ca), (zb, wb, db, cb) in zip(tz, tz[1:]):
                if za <= z <= zb:
                    t = (z - za) / (zb - za)
                    return halka(0, ca + (cb - ca) * t, z, wa + (wb - wa) * t, da + (db - da) * t, 16, 2.6)
            return halka(0, tz[-1][3], z, tz[-1][1], tz[-1][2], 16, 2.6)
        kemer = halka(0, -0.113, 0.405, 0.105, 0.072, 16, 2.6)
        loft([halka(0, -0.112, 0.385, 0.104, 0.071, 16, 2.6), kemer], 'boya_sari')
        halka_kapak(kemer, govde(0.405), 'boya_sari', Z)
        kutu_merkez(y, (0, -0.186), 0.026, 0.008, 0.03, 'boya_sari', z0=0.38)
        if kirik:
            # the broken stump: a jagged top
            r0 = hs[-1]
            r1 = [p + V(0, 0, 0.012 * math.sin(i * 2.7) + 0.01 * math.cos(i * 1.3)) for i, p in enumerate(halka(0, -0.12, 0.49, 0.114, 0.075, 16, 2.6))]
            y.serit(r0, r1, K)
            tepe = V(0.01, -0.11, 0.505)
            for i in range(16):
                y.yuz_yon([r1[i], r1[(i + 1) % 16], tepe], 'kum', Z)
            for sg in (-1, 1):   # forearms on the lap, broken at the elbows
                boru(y, [V(sg * 0.15, -0.14, 0.43), V(sg * 0.12, -0.25, 0.4), V(sg * 0.095, -0.33, 0.39)], 0.033, K, n=8, r_son=0.028)
                kutu_merkez(y, (sg * 0.085, -0.355), 0.054, 0.07, 0.02, K, z0=0.357)
            return
        # broad collar (wesekh): a crescent of bead rows lying on the chest, narrower towards the bottom
        for zz, key, xl in ((0.546, 'turkuaz', 0.075), (0.56, 'boya_kirmizi', 0.115), (0.574, 'turkuaz', 0.14), (0.588, 'altin', 0.16)):
            a = halka(0, -0.12, zz, 0.143 * 1.012, 0.08 * 1.03, 16, 2.6)
            b = halka(0, -0.119, zz + 0.014, 0.146 * 1.012, 0.077 * 1.03, 16, 2.6)
            g = govde(zz + 0.014)
            for i in range(16):
                j = (i + 1) % 16
                if a[i].y < -0.13 and a[j].y < -0.13 and max(abs(a[i].x), abs(a[j].x)) <= xl:
                    y.serit([a[i], a[j]], [b[i], b[j]], key, kapali=False)
                    y.yuz_yon([b[i], b[j], g[j], g[i]], key, Z)
        # shoulders, arms, hands on the knees
        for sg in (-1, 1):
            kure(y, (sg * 0.145, -0.116, 0.585), 0.05, K, n=8, kat=5)
            boru(y, [V(sg * 0.152, -0.116, 0.58), V(sg * 0.158, -0.122, 0.5), V(sg * 0.156, -0.13, 0.428)], 0.043, K, n=8, r_son=0.037)
            kure(y, (sg * 0.155, -0.132, 0.42), 0.037, K, n=8, kat=4)
            boru(y, [V(sg * 0.155, -0.136, 0.415), V(sg * 0.12, -0.25, 0.4), V(sg * 0.095, -0.33, 0.39)], 0.034, K, n=8, r_son=0.028)
            kutu_merkez(y, (sg * 0.085, -0.355), 0.054, 0.072, 0.02, K, z0=0.357)
            # a cartouche on the upper arm
            kure(y, (sg * 0.19, -0.13, 0.53), 0.012, 'boya_sari', n=6, kat=3)
        bas_ve_tac(K)


def ayakta(px, py, pz, H, tur='kral', aci=0.0, K=HT):
    """a standing statue (units: 1 = its height), facing -y then turned by aci: tur 'kral' (kilt, left foot forward,
    double crown), 'kralice' (sheath dress, wig, Hathor crown of disk, horns and plumes), 'sahin' (falcon-headed god with
    the sun disk), 'cocuk' (a small figure)"""
    with parca(y, (px, py, pz), aci, H):
        kutu_merkez(y, (0, 0.03), 0.18, 0.05, 0.7, K)               # back pillar
        if tur == 'kralice':
            donel(y, (0, -0.01), [(0.07, 0.0), (0.072, 0.1), (0.078, 0.3), (0.085, 0.46), (0.078, 0.58), (0.08, 0.66), (0.1, 0.74), (0.04, 0.775), (0, 0.776)], K, n=10)
            for sg in (-1, 1):   # arms: one down, one across the chest holding a flower
                boru(y, [V(sg * 0.09, -0.01, 0.74), V(sg * 0.1, -0.02, 0.6), V(sg * 0.075, -0.06, 0.52 if sg < 0 else 0.62)], 0.022, K, n=6)
            kutu_merkez(y, (0, -0.088), 0.11, 0.006, 0.045, 'turkuaz', z0=0.67)
        else:
            for sg, yf in ((-1, -0.11), (1, 0.0)):
                kutu_merkez(y, (sg * 0.04, yf - 0.02), 0.045, 0.1, 0.028, K)
                boru(y, [V(sg * 0.04, yf, 0.03), V(sg * 0.04, yf * 0.55, 0.26), V(sg * 0.045, -0.01, 0.46)], 0.026, K, n=6, r_son=0.04)
            donel(y, (0, -0.01), [(0, 0.36), (0.07, 0.36), (0.085, 0.38), (0.078, 0.5), (0.07, 0.52), (0, 0.52)], 'beyaz' if tur != 'cocuk' else K, n=10)
            y.yuz_yon([V(-0.02, -0.092, 0.5), V(0.02, -0.092, 0.5), V(0.026, -0.098, 0.37), V(-0.026, -0.098, 0.37)], 'boya_sari', -Y)
            hs = [halka(0, -0.01, z, hw, hd, 12, 2.4) for z, hw, hd in ((0.5, 0.07, 0.05), (0.62, 0.095, 0.055), (0.72, 0.12, 0.055), (0.75, 0.09, 0.045), (0.77, 0.04, 0.035))]
            loft(hs, K, K)
            for sg in (-1, 1):
                kure(y, (sg * 0.115, -0.01, 0.715), 0.035, K, n=8, kat=4)
                boru(y, [V(sg * 0.122, -0.01, 0.71), V(sg * 0.13, -0.015, 0.6), V(sg * 0.12, -0.02, 0.47)], 0.025, K, n=6, r_son=0.02)
                kure(y, (sg * 0.12, -0.022, 0.46), 0.026, K, n=6, kat=3)
            kutu_merkez(y, (0, -0.06), 0.18, 0.012, 0.03, 'turkuaz', z0=0.69)
        # head
        if tur == 'sahin':
            kure(y, (0, -0.015, 0.83), 0.06, K, n=8, kat=5)
            boru(y, [V(0, -0.06, 0.84), V(0, -0.095, 0.82), V(0, -0.1, 0.8)], 0.016, 'kum_koyu', n=5, r_son=0.005)
            for sg in (-1, 1):
                kutu_merkez(y, (sg * 0.05, -0.01), 0.025, 0.05, 0.11, 'lacivert', z0=0.7)
            # the sun disk with the uraeus
            n_ = 16
            dz_ = 0.95
            ring = [V(0.075 * math.cos(TAU * i / n_), -0.015, dz_ + 0.075 * math.sin(TAU * i / n_)) for i in range(n_)]
            y.yuz_yon(ring, 'boya_kirmizi', -Y)
            y.yuz_yon([p + Y * 0.02 for p in ring], 'boya_kirmizi', Y)
            for i in range(n_):
                j = (i + 1) % n_
                yuz_dis(y, [ring[i], ring[j], ring[j] + Y * 0.02, ring[i] + Y * 0.02], 'boya_kirmizi', V(0, -0.005, dz_))
            boru(y, [V(0, -0.02, 0.87), V(0, -0.03, 0.9), V(0, -0.025, 0.92)], 0.008, 'altin', n=5)
        else:
            donel(y, (0, -0.02), [(0, 0.775), (0.04, 0.78), (0.052, 0.81), (0.05, 0.85), (0.03, 0.875), (0, 0.88)], K, n=10)
            cubuk(y, V(0, -0.066, 0.835), V(0, -0.078, 0.815), 0.014, K, 0.012)
            if tur == 'kralice':
                donel(y, (0, 0.012), [(0.064, 0.72), (0.066, 0.8), (0.058, 0.87), (0.04, 0.89), (0, 0.895)], 'koyu', n=10)   # (behind the face)
                kutu_merkez(y, (0, -0.044), 0.11, 0.02, 0.022, 'koyu', z0=0.866)   # wig over the brow
                donel(y, (0, -0.005), [(0.04, 0.89), (0.04, 0.91), (0, 0.912)], 'altin', n=10)
                for sg in (-1, 1):   # cow horns round the disk, two tall plumes
                    boru(y, [V(sg * 0.012, -0.005, 0.905), V(sg * 0.06, -0.005, 0.93), V(sg * 0.065, -0.005, 0.99), V(sg * 0.04, -0.005, 1.03)], 0.007, 'koyu', n=5)
                    cubuk(y, V(sg * 0.012, 0.0, 0.94), V(sg * 0.012, 0.0, 1.16), 0.022, 'beyaz', 0.008)
                n_ = 14
                ring = [V(0.045 * math.cos(TAU * i / n_), -0.012, 0.965 + 0.045 * math.sin(TAU * i / n_)) for i in range(n_)]
                plaka(ring, 'boya_kirmizi', -Y, 0.006)
            elif tur == 'cocuk':
                kure(y, (0.035, -0.02, 0.86), 0.022, 'koyu', n=6, kat=3)   # side lock of youth
            else:
                for sg in (-1, 1):
                    kutu_merkez(y, (sg * 0.055, -0.04), 0.022, 0.03, 0.1, 'kum', z0=0.72)   # nemes lappets
                donel(y, (0, -0.02), [(0.052, 0.84), (0.054, 0.9), (0.04, 0.905)], 'kirmizi', n=10)
                kutu_merkez(y, (0, 0.025), 0.035, 0.018, 0.08, 'kirmizi', z0=0.87)
                donel(y, (0, -0.02), [(0.04, 0.9), (0.04, 0.95), (0.03, 0.99), (0, 1.0)], 'mermer', n=10)
                kure(y, (0, -0.02, 0.995), 0.016, 'mermer', n=8, kat=4)
                boru(y, [V(0, -0.072, 0.85), V(0, -0.078, 0.875)], 0.006, 'altin', n=5)


def sahin(px, py, pz, s, aci=0.0):
    """a falcon of Horus standing on a block, the double crown on its head (units: 1 = its height)"""
    with parca(y, (px, py, pz), aci, s):
        kutu_merkez(y, (0, 0.0), 0.5, 0.7, 0.12, FT)
        silme(y, dikdortgen(-0.25, 0.25, -0.35, 0.35), 0.12, 0.04, 0.03, FT, 'tac')
        y.yuz_yon([V(p.x, p.y, 0.16) for p in dikdortgen(-0.25, 0.25, -0.35, 0.35)], FT, Z)
        donel(y, (0, 0.02), [(0, 0.16), (0.16, 0.17), (0.2, 0.3), (0.2, 0.45), (0.16, 0.58), (0.1, 0.66), (0, 0.68)], HT, n=12)
        for sg in (-1, 1):   # folded wings
            plaka([V(sg * 0.2, -0.1, 0.55), V(sg * 0.2, 0.18, 0.5), V(sg * 0.19, 0.3, 0.2), V(sg * 0.19, 0.05, 0.26)], 'kum', X * sg, 0.03)
        boru(y, [V(0, 0.15, 0.3), V(0, 0.3, 0.18)], 0.06, HT, n=5, r_son=0.03)
        kure(y, (0, -0.03, 0.74), 0.11, HT, n=10, kat=5)
        boru(y, [V(0, -0.12, 0.76), V(0, -0.18, 0.72), V(0, -0.17, 0.68)], 0.03, 'kum_koyu', n=5, r_son=0.01)
        donel(y, (0, -0.02), [(0.1, 0.8), (0.11, 0.86), (0.08, 0.87)], 'kirmizi', n=10)
        donel(y, (0, -0.02), [(0.075, 0.86), (0.075, 0.95), (0.05, 1.0), (0, 1.02)], 'mermer', n=10)


def babun(px, py, pz, s):
    """a baboon standing on its hind legs, forepaws raised to the rising sun (units: 1 = its height)"""
    with parca(y, (px, py, pz), 0.0, s):
        donel(y, (0, 0.0), [(0, 0.0), (0.32, 0.02), (0.36, 0.25), (0.3, 0.5), (0.16, 0.6), (0, 0.62)], HT, n=8)
        kure(y, (0, -0.04, 0.72), 0.2, HT, n=8, kat=4)
        cubuk(y, V(0, -0.15, 0.72), V(0, -0.26, 0.66), 0.13, 'kum', 0.11)
        for sg in (-1, 1):
            cubuk(y, V(sg * 0.22, -0.05, 0.5), V(sg * 0.32, -0.16, 0.9), 0.1, HT)
            kure(y, (sg * 0.2, -0.1, 0.82), 0.12, 'kum', n=6, kat=3)   # the mane


# ---------------------------------------------------------------- layout
GC = -0.25                    # great temple axis
FY = 0.08                     # facade foot line
FB = 0.065                    # its batter (setback at the top)
FH = 0.95                     # facade height
FW0, FW1 = 0.66, 0.6          # half widths at the foot / top
ZT = Z0 + 0.045               # terrace
YB = 1.1
NX0, NX1, NY, NH = 0.465, 1.105, 0.1, 0.4
ZN = Z0 + 0.03
YR0 = FY + FB                 # the line along which the hill starts
GX0, GX1, GY0 = -1.2, 1.2, -1.15

# ---------------------------------------------------------------- ground and the Nile
y.bolum('Zemin ve Nil')
YK, YS = -0.62, -0.8          # bank top edge, water edge
prof = [(GY0, ZW), (YS, ZW), (YK, Z0), (YB, Z0)]
for sx in (-1, 1):
    xx = GX0 if sx < 0 else GX1
    pts = [V(xx, GY0, 0), V(xx, YB, 0)] + [V(xx, yy, zz) for yy, zz in reversed(prof)]
    y.yuz_yon(pts, 'kaya_koyu', X * sx)
y.yuz_yon([V(GX0, GY0, 0), V(GX1, GY0, 0), V(GX1, GY0, ZW), V(GX0, GY0, ZW)], 'kaya_koyu', -Y)
y.yuz_yon([V(GX0, YB, 0), V(GX1, YB, 0), V(GX1, YB, Z0), V(GX0, YB, Z0)], 'kaya_koyu', Y)
y.yuz_yon([V(GX0, GY0, ZW), V(GX1, GY0, ZW), V(GX1, YS, ZW), V(GX0, YS, ZW)], 'su', Z)
y.yuz_yon([V(GX0, YS, ZW), V(GX1, YS, ZW), V(GX1, YK, Z0), V(GX0, YK, Z0)], 'kum', Z)
y.yuz_yon([V(GX0, YK, Z0), V(GX1, YK, Z0), V(GX1, YB, Z0), V(GX0, YB, Z0)], 'kum_acik', Z)
# a stone quay where the stair meets the river
kutu(y, V(GC - 0.16, YS - 0.06, 0.0), X, 0.32, 0.17, Z0 - 0.005, FT, 'onsagsolust')
for k in range(4):
    kutu(y, V(GC - 0.1, YK - 0.03 - k * 0.04, 0.0), X, 0.2, 0.045 + k * 0.04, Z0 + 0.004 - k * 0.01, FT, 'onsagsolust')

# ---------------------------------------------------------------- the hill
y.bolum('Tepe')


def z_on(x):
    """the hill's front edge height (the facade tops, rock elsewhere)"""
    if x <= GC - 0.68:
        t = (x - GX0) / (GC - 0.68 - GX0)
        return 0.3 + (ZT + FH - 0.3) * (t ** 1.4)
    if x <= GC + 0.68:
        return ZT + FH
    if x <= NX0 - 0.01:
        t = (x - (GC + 0.68)) / (NX0 - 0.01 - (GC + 0.68))
        return ZT + FH + (ZN + NH - ZT - FH) * t
    if x <= NX1 + 0.01:
        return ZN + NH
    t = (x - NX1 - 0.01) / (GX1 - NX1 - 0.01)
    return ZN + NH - (ZN + NH - 0.3) * t


xs = sorted(set([round(GX0 + k * 0.05, 4) for k in range(49)] + [GC - 0.68, GC + 0.68, NX0 - 0.01, NX1 + 0.01]))
xs = [x for x in xs if GX0 - 1e-9 <= x <= GX1 + 1e-9]


def tepe_z(x):
    # the crest: the front edge height smoothed along x, a little above it
    w = [(math.exp(-((x - xx) / 0.22) ** 2), z_on(xx)) for xx in xs]
    return sum(a * b for a, b in w) / sum(a for a, _ in w) + 0.07


NV = 15
VC = 0.16


def tumsek(x, yy):
    """rolling relief of the hill: weathered ribs and hollows, a few rocky knolls"""
    z = 0.05 * (math.sin(11 * x + 2.3 * yy) * 0.6 + math.sin(7 * yy - 4 * x + 1) * 0.4)
    z += 0.025 * math.sin(23 * x - 9 * yy + 2) * math.cos(17 * yy + 3 * x)
    for (kx, ky, kr, kh) in ((-0.75, 0.6, 0.16, 0.1), (-0.05, 0.75, 0.2, 0.08), (0.75, 0.55, 0.14, 0.09), (-1.0, 0.85, 0.13, 0.07)):
        z += kh * math.exp(-((x - kx) ** 2 + (yy - ky) ** 2) / kr ** 2)
    return z


def tepe_yuk(x, v):
    """the hill's height at x, v (0: its front edge, 1: the back of the plot)"""
    yy = YR0 + (YB - YR0) * v
    zf, zc, zb = z_on(x), max(z_on(x), tepe_z(x)), Z0 + 0.02
    if v <= VC:
        z = zf + (zc - zf) * math.sin(math.pi / 2 * v / VC)
    else:
        z = zb + (zc - zb) * math.cos(math.pi / 2 * (v - VC) / (1 - VC)) ** 1.15
    if 0 < v < 1:
        z += tumsek(x, yy) * min(1, v * 4) * (1 - v) ** 0.7
    return z


sat = []
for k in range(NV + 1):
    v = k / NV
    sat.append([V(x, YR0 + (YB - YR0) * v, tepe_yuk(x, v)) for x in xs])
for k in range(NV):
    for i in range(len(xs) - 1):
        a, b, c, d = sat[k][i], sat[k][i + 1], sat[k + 1][i + 1], sat[k + 1][i]
        y.yuz([a, b, c], KY); y.yuz([a, c, d], KY)
# weathered boulders and ledges of darker rock on the hill
for k in range(18):
    bx = GX0 + 0.12 + ((k * 0.613) % 1) * (GX1 - GX0 - 0.24)
    bv = 0.25 + ((k * 0.377 + 0.1) % 1) * 0.68
    by = YR0 + (YB - YR0) * bv
    r_ = 0.02 + 0.025 * ((k * 0.71) % 1)
    bz = tepe_yuk(bx, bv)
    donel(y, (bx, by), [(r_, bz - r_ * 0.6), (r_ * 0.95, bz + r_ * 0.15), (r_ * 0.6, bz + r_ * 0.55), (0, bz + r_ * 0.65)], 'kaya_koyu', n=6, kat=k * 0.7)
for k in range(NV):   # side skirts
    for sx, i in ((-1, 0), (1, -1)):
        a, b = sat[k][i], sat[k + 1][i]
        y.yuz_yon([V(a.x, a.y, Z0), V(b.x, b.y, Z0), b, a], KY, X * sx)
for i in range(len(xs) - 1):   # back skirt
    a, b = sat[NV][i], sat[NV][i + 1]
    y.yuz_yon([V(a.x, a.y, Z0), V(b.x, b.y, Z0), b, a], KY, Y)
# the front edge skirt (behind the facades it is hidden; between them the rock face)
for i in range(len(xs) - 1):
    a, b = sat[0][i], sat[0][i + 1]
    y.yuz_yon([V(a.x, a.y, Z0), V(b.x, b.y, Z0), b, a], KY, -Y)
    # (and its back a little behind: closes the facade slabs when seen past their tops)
    y.yuz_yon([V(a.x, a.y + 0.004, Z0), V(b.x, b.y + 0.004, Z0), b + Y * 0.004 - Z * 0.004, a + Y * 0.004 - Z * 0.004], FT, Y)


def yanak(x0, x1, yf0, yf1, zf0, zf1, yan0, yan1):
    """a rock spur in front of the hill between x0 and x1: front edge from (yf0, zf0) to (yf1, zf1) (low, wavering),
    rising steeply and bulging to the hill's front edge; yan0 / yan1: close its side at x0 / x1 (the cut beside a facade)"""
    cols = [x for x in xs if x0 - 1e-9 <= x <= x1 + 1e-9]
    if cols[0] > x0 + 1e-9: cols = [x0] + cols
    if cols[-1] < x1 - 1e-9: cols = cols + [x1]
    NR = 6
    grid = []
    for k in range(NR + 1):
        v = k / NR
        row = []
        for x in cols:
            t = (x - x0) / (x1 - x0)
            yf, zf = yf0 + (yf1 - yf0) * t + 0.025 * math.sin(13 * x), zf0 + (zf1 - zf0) * t
            yy = yf + (YR0 - yf) * v
            zb = z_on(x)
            z = zf + (zb - zf) * (1 - (1 - v) ** 2.2)
            if 0 < k < NR:
                z += 0.025 * math.sin(17 * x + 5 * yy) * math.sin(math.pi * v) + 0.015 * math.sin(31 * x - 11 * yy)
            row.append(V(x, yy, z))
        grid.append(row)
    for k in range(NR):
        for i in range(len(cols) - 1):
            a, b, c, d = grid[k][i], grid[k][i + 1], grid[k + 1][i + 1], grid[k + 1][i]
            nz = (c - a).cross(d - b).normalized().z
            key = KY
            y.yuz([a, b, c], key); y.yuz([a, c, d], key)
    for i in range(len(cols) - 1):
        a, b = grid[0][i], grid[0][i + 1]
        y.yuz_yon([V(a.x, a.y, Z0), V(b.x, b.y, Z0), b, a], KY, -Y)
    for uc, yon, var in ((0, -X, yan0), (-1, X, yan1)):
        if not var: continue
        for k in range(NR):
            a, b = grid[k][uc], grid[k + 1][uc]
            y.yuz_yon([V(a.x, a.y, Z0), V(b.x, b.y, Z0), b, a], KY, yon)


yanak(GX0, GC - 0.68, -0.2, -0.12, 0.12, 0.32, True, True)
yanak(GC + 0.68, NX0 - 0.01, -0.1, -0.1, 0.38, 0.3, True, True)
yanak(NX1 + 0.01, GX1, -0.06, -0.1, 0.22, 0.12, True, True)
# the Marriage Stela cut into the rock south of the great temple: a round-topped slab, the winged sun, the king
# before the gods, registers of text
SX, SYY, SW, SH = -1.06, -0.205, 0.14, 0.25
dis_ = [(-SW / 2, 0.0), (SW / 2, 0.0), (SW / 2, SH - SW / 2)] + [(SW / 2 * math.cos(math.pi * k / 8), SH - SW / 2 + SW / 2 * math.sin(math.pi * k / 8)) for k in range(1, 8)] + [(-SW / 2, SH - SW / 2)]
plaka([V(SX + s_, SYY, Z0 + t_) for s_, t_ in dis_], 'kum', -Y, 0.06)
Ps_ = lambda s_, t_, d=0.002: V(SX + s_, SYY, Z0 + t_) - Y * d
y.yuz_yon([Ps_(0, SH - SW / 2 + 0.018, 0.003) + X * (0.012 * math.cos(TAU * i / 10)) + Z * (0.012 * math.sin(TAU * i / 10)) for i in range(10)], 'boya_kirmizi', -Y)
for sg in (-1, 1):
    y.yuz_yon([Ps_(sg * 0.012, SH - SW / 2 + 0.02, 0.003), Ps_(sg * 0.055, SH - SW / 2 + 0.035, 0.003), Ps_(sg * 0.055, SH - SW / 2 + 0.022, 0.003), Ps_(sg * 0.012, SH - SW / 2 + 0.008, 0.003)], 'lacivert', -Y)
for k, sc in enumerate((-0.04, -0.012, 0.03)):
    levha(Ps_, sc - 0.007, sc + 0.007, 0.135, 0.19, 'kirmizi' if k else 'kum_koyu', -Y, 0.003)
    levha(Ps_, sc - 0.005, sc + 0.005, 0.19, 0.205, 'beyaz' if k == 2 else 'kum_koyu', -Y, 0.0035)
for r in range(5):
    yazi_bandi(Ps_, -Y, -SW / 2 + 0.012, SW / 2 - 0.012, 0.02 + r * 0.022, 0.011, 'kum_koyu', 0.003, tohum=r)
# fallen boulders at the foot of the rock
for (bx, by, r_) in ((-1.17, -0.32, 0.03), (-0.95, -0.27, 0.022), (1.16, -0.18, 0.035), (0.44, -0.16, 0.022)):
    donel(y, (bx, by), [(r_, Z0 - 0.003), (r_ * 0.85, Z0 + r_ * 0.5), (r_ * 0.4, Z0 + r_ * 0.9), (0, Z0 + r_ * 0.95)], KY, n=7)

# ---------------------------------------------------------------- great temple: terrace
y.bolum('Teras')
TY0 = -0.5
kutu(y, V(GC - 0.68, TY0, 0), X, 1.36, FY + 0.03 - TY0, ZT, FT, 'onsagsol')
y.yuz_yon([V(GC - 0.68, TY0, ZT), V(GC + 0.68, TY0, ZT), V(GC + 0.68, FY + 0.03, ZT), V(GC - 0.68, FY + 0.03, ZT)], 'zemin', Z)
silme(y, [V(GC - 0.68, TY0), V(GC + 0.68, TY0)], ZT - 0.008, 0.008, 0.006, FT, 'duz', kapali=False)
# the parapet along the front, broken by the stair
PW = 0.1
for (xa, xb) in ((GC - 0.68, GC - PW), (GC + PW, GC + 0.68)):
    kutu(y, V(xa, TY0, ZT), X, xb - xa, 0.03, 0.03, FT)
    kornis(y, xa, xb, TY0, TY0 + 0.03, ZT + 0.03, 0.006, 0.004, FT, 'tac')
    y.yuz([V(xa, TY0, ZT + 0.036), V(xb, TY0, ZT + 0.036), V(xb, TY0 + 0.03, ZT + 0.036), V(xa, TY0 + 0.03, ZT + 0.036)], FT)
merdiven(y, (GC, TY0 - 0.06), math.pi / 2, 2 * PW, Z0, ZT, n=5, d=0.012, key=FT)
merdiven(y, (GC, TY0 - 0.06 - 0.06), math.pi / 2, 2 * PW - 0.02, 0.0, Z0, n=4, d=0.015, key=FT)
for sg in (-1, 1):   # the stair's flanking blocks
    kutu_merkez(y, (GC + sg * (PW + 0.0), TY0 - 0.03), 0.03, 0.06, ZT + 0.035, FT, z0=0.0)
# falcons and king statues along the parapet
for k, sx in enumerate((-0.6, -0.42, -0.24, 0.24, 0.42, 0.6)):
    if k % 2 == 0:
        sahin(GC + sx, TY0 + 0.015, ZT + 0.036, 0.085)
    else:
        kutu_merkez(y, (GC + sx, TY0 + 0.015), 0.04, 0.04, 0.012, FT, z0=ZT + 0.036)
        ayakta(GC + sx, TY0 + 0.02, ZT + 0.048, 0.1, 'kral')

# ---------------------------------------------------------------- great temple: the facade
y.bolum('Buyuk tapinak cephesi')
NF = V(0, -1, FB / FH).normalized()
hw = lambda t: FW0 + (FW1 - FW0) * t / FH
FP = lambda s, t, d=0.0: V(GC + s, FY + FB * t / FH, ZT + t) + NF * d
DW, D0, D1 = 0.036, 0.045, 0.29          # door half width, bottom, top
NW, N0, N1 = 0.042, 0.37, 0.6            # niche
bantlar = [(0.0, D0, None), (D0, D1, DW), (D1, N0, None), (N0, N1, NW), (N1, FH, None)]
for t0, t1, a in bantlar:
    if a is None:
        y.yuz_yon([FP(-hw(t0), t0), FP(hw(t0), t0), FP(hw(t1), t1), FP(-hw(t1), t1)], FT, NF)
    else:
        y.yuz_yon([FP(-hw(t0), t0), FP(-a, t0), FP(-a, t1), FP(-hw(t1), t1)], FT, NF)
        y.yuz_yon([FP(a, t0), FP(hw(t0), t0), FP(hw(t1), t1), FP(a, t1)], FT, NF)
# the facade's sides (inside the rock cheeks)
for sg in (-1, 1):
    a0, a1 = FP(sg * hw(0), 0), FP(sg * hw(FH), FH)
    iki_yuzlu(y, [a0, a0 + Y * 0.12, a1 + Y * 0.06, a1], FT, X * sg)   # (two-sided: seen past the rock spur from the far side)
# door and niche: reveals and backs
for (a, t0, t1, der, arka) in ((DW, D0, D1, 0.04, 'koyu'), (NW, N0, N1, 0.045, FT)):
    ic_ = [(-a, t0), (a, t0), (a, t1), (-a, t1)]
    m = FP(0, (t0 + t1) / 2, -der / 2)
    for k in range(4):
        p, q = ic_[k], ic_[(k + 1) % 4]
        mid = FP((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, -der / 2)
        y.yuz_yon([FP(*p), FP(*q), FP(*q, -der), FP(*p, -der)], FT if k else 'kum_acik', m - mid)
    y.yuz_yon([FP(-a, t0, -der), FP(a, t0, -der), FP(a, t1, -der), FP(-a, t1, -der)], arka, NF)
# the door frame (jambs carved with text) and the lintel with the winged sun
for sg in (-1, 1):
    levha(FP, sg * DW, sg * (DW + 0.018), D0, D1 + 0.018, 'kum_acik', NF, 0.004) if sg > 0 else levha(FP, -(DW + 0.018), -DW, D0, D1 + 0.018, 'kum_acik', NF, 0.004)
    yazi_sutunu(FP, NF, (DW + 0.004) * sg - (0.01 if sg < 0 else 0), D0 + 0.02, D1, 0.01, 'kum_koyu', 0.014, 0.0055, tohum=3 + sg)
levha(FP, -(DW + 0.018), DW + 0.018, D1, D1 + 0.022, 'kum_acik', NF, 0.0045)
o = FP(0, D1 + 0.011, 0.0055)
y.yuz_yon([o + X * (0.018 * math.cos(TAU * i / 12)) + Z * (0.009 * math.sin(TAU * i / 12)) for i in range(12)], 'boya_kirmizi', NF)
for sg in (-1, 1):
    y.yuz_yon([o + X * sg * 0.016, o + X * sg * 0.045 + Z * 0.004, o + X * sg * 0.045 - Z * 0.006, o + X * sg * 0.016 - Z * 0.008], 'lacivert', NF)
# Ra-Horakhty in his niche, the king offering Maat in relief on either side
nz = FP(0, N0, -0.03)
ayakta(nz.x, nz.y + 0.012, nz.z, 0.2, 'sahin')
for sg in (-1, 1):
    sc = sg * 0.085
    levha(FP, sc - 0.03, sc + 0.03, N0 + 0.01, N0 + 0.16, 'kum_acik', NF, 0.002)
    # the king (striding, arms out to the god) and the little Maat figure he holds up
    levha(FP, sc - 0.01, sc + 0.01, N0 + 0.04, N0 + 0.12, 'kirmizi', NF, 0.0035)
    levha(FP, sc - 0.014, sc + 0.014, N0 + 0.04, N0 + 0.07, 'beyaz', NF, 0.004)
    levha(FP, sc - 0.007, sc + 0.007, N0 + 0.12, N0 + 0.14, 'kirmizi', NF, 0.0035)
    levha(FP, sc - 0.008, sc + 0.008, N0 + 0.137, N0 + 0.155, 'mermer', NF, 0.004)
    levha(FP, sc - sg * 0.012 - 0.012, sc - sg * 0.012 + 0.012, N0 + 0.1, N0 + 0.106, 'kirmizi', NF, 0.0035)
    levha(FP, sc - sg * 0.03 - 0.004, sc - sg * 0.03 + 0.004, N0 + 0.106, N0 + 0.125, 'boya_sari', NF, 0.004)
    levha(FP, sc - 0.02, sc + 0.02, N0 + 0.015, N0 + 0.032, 'kum_koyu', NF, 0.0035)
# dedication band, cartouche frieze, torus, cavetto with uraei, baboons
yazi_bandi(FP, NF, -hw(0.7) + 0.03, hw(0.7) - 0.03, 0.7, 0.022, 'kum_koyu', 0.003, tohum=4)
# columns of the king's titles between the colossi's crowns and by the facade's edges
for k, (sc, t0, t1, w_) in enumerate(((-0.32, 0.48, 0.68, 0.02), (0.32, 0.48, 0.68, 0.02), (-0.616, 0.1, 0.68, 0.014), (0.616, 0.1, 0.68, 0.014))):
    levha(FP, sc - w_ / 2 - 0.006, sc + w_ / 2 + 0.006, t0 - 0.008, t1 + 0.004, 'kum_acik', NF, 0.0015)
    yazi_sutunu(FP, NF, sc - w_ / 2, t0, t1, w_, 'kum_koyu', 0.017, 0.003, tohum=k + 5)
levha(FP, -hw(0.74), hw(0.74), 0.735, 0.738, 'kum_koyu', NF, 0.0025)
n_k = 17
for k in range(n_k):
    sc = -hw(0.76) + 0.04 + k * (2 * hw(0.76) - 0.08) / (n_k - 1)
    if k % 2 == 0:
        kartus(FP, NF, sc, 0.748, 0.03, 0.05, 0.003, tohum=k)
    else:
        o = FP(sc, 0.776, 0.004)
        y.yuz_yon([o + X * (0.011 * math.cos(TAU * i / 10)) + Z * (0.011 * math.sin(TAU * i / 10)) for i in range(10)], 'boya_kirmizi', NF)
        levha(FP, sc - 0.004, sc + 0.004, 0.75, 0.765, 'boya_sari', NF, 0.004)
TT = 0.81
boru(y, [FP(-hw(TT), TT, 0.008), FP(hw(TT), TT, 0.008)], 0.011, FT, n=8)
for sg in (-1, 1):
    boru(y, [FP(sg * (hw(0) - 0.008), 0.0, 0.008), FP(sg * (hw(TT) - 0.008), TT, 0.008)], 0.011, FT, n=8)
ct = TT + 0.012
cl = [FP(-hw(ct), ct), FP(hw(ct), ct)]
silme(y, [V(p.x, p.y) for p in cl], ZT + ct, 0.06, 0.04, FT, KAVETTO, kapali=False)
ctop = ZT + ct + 0.06
y.yuz_yon([V(cl[0].x, cl[0].y, ctop), V(cl[1].x, cl[1].y, ctop), V(cl[1].x, cl[1].y - 0.04, ctop), V(cl[0].x, cl[0].y - 0.04, ctop)], FT, Z)
# the cornice's frieze of rearing cobras
n_u = 28
for k in range(n_u):
    sc = -hw(ct) + 0.03 + k * (2 * hw(ct) - 0.06) / (n_u - 1)
    p = V(GC + sc, cl[0].y - 0.038, ctop + 0.026)
    plaka([p + V(-0.006, -0.012, -0.02), p + V(0.006, -0.012, -0.02), p + V(0.004, -0.014, -0.004), p + V(-0.004, -0.014, -0.004)], 'altin', -Y, 0.003)
    kure(y, p + V(0, -0.012, 0.0), 0.0065, 'boya_kirmizi', n=6, kat=3)
for k in range(22):
    sc = -hw(ct) + 0.035 + k * (2 * hw(ct) - 0.07) / 21
    babun(GC + sc, cl[0].y - 0.018, ctop, 0.07)

# ---------------------------------------------------------------- the four colossi
y.bolum('Ramses heykelleri')
S = 0.64
PED = 0.04
for k, sx in enumerate((-0.47, -0.17, 0.17, 0.47)):
    x = GC + sx
    # a pedestal with bound captives carved on its front
    kutu(y, V(x - 0.14, FY - 0.31, ZT), X, 0.28, 0.31 + 0.02, PED, FT, 'onsagsolust')
    kornis(y, x - 0.14, x + 0.14, FY - 0.31, FY + 0.02, ZT + PED - 0.006, 0.006, 0.004, FT, 'tac')
    Pp = lambda s_, t_, d=0.002, x=x: V(x + s_, FY - 0.31, ZT + t_) - Y * d
    for m in range(5):
        sc = -0.1 + m * 0.05
        levha(Pp, sc - 0.008, sc + 0.008, 0.006, 0.022, 'koyu' if m % 2 else 'kirmizi', -Y)
        levha(Pp, sc - 0.005, sc + 0.005, 0.022, 0.03, 'koyu' if m % 2 else 'kirmizi', -Y)
        levha(Pp, sc - 0.012, sc + 0.012, 0.014, 0.017, 'saz_koyu', -Y, 0.003)
    oturan_kolos(x, FY - 0.0, ZT + PED, S, kirik=(k == 1))
    # the family at his feet: the queen between the legs, children by the throne
    ayakta(x, FY - 0.258 * 1, ZT + PED, 0.14, 'kralice')
    for sg in (-1, 1):
        ayakta(x + sg * 0.115, FY - 0.22, ZT + PED, 0.12, 'kralice' if (k + sg) % 2 else 'cocuk')

# the fallen head and shoulders of the second colossus lying on the terrace
y.bolum('Yikik bas')
bas = len(y.faces)
with parca(y, (0, 0, 0), 0.0, S):
    bas_ve_tac(HT)
    # the broken chest piece below the head
    hs = [halka(0, cy, z, hw_, hd, 16, 2.6) for z, hw_, hd, cy in ((0.52, 0.128, 0.08, -0.12), (0.56, 0.143, 0.08, -0.12), (0.59, 0.148, 0.074, -0.118), (0.615, 0.12, 0.062, -0.116), (0.632, 0.055, 0.046, -0.118))]
    loft(hs, HT)
    r0 = [p + V(0, 0, 0.01 * math.sin(i * 2.1)) for i, p in enumerate(hs[0])]
    tepe = V(0, -0.12, 0.5)
    for i in range(16):
        y.yuz_yon([hs[0][(i + 1) % 16], hs[0][i], tepe], 'kum', -Z)
    for sg in (-1, 1):
        kure(y, (sg * 0.145, -0.116, 0.585), 0.05, HT, n=10, kat=5)
M = Matrix.Rotation(0.55, 3, 'Z') @ Matrix.Rotation(-1.62, 3, 'X')
donustur(bas, M, (0, 0, 0))
zmin = min(p[2] for f in y.faces[bas:] for p in f[0])
xs_ = [p[0] for f in y.faces[bas:] for p in f[0]]; ys_ = [p[1] for f in y.faces[bas:] for p in f[0]]
donustur(bas, Matrix.Identity(3), (GC - 0.2 - (min(xs_) + max(xs_)) / 2, -0.33 - (min(ys_) + max(ys_)) / 2, ZT - zmin - 0.006))
# broken blocks round it
for (bx, by, w_, a_) in ((GC - 0.06, -0.29, 0.04, 0.4), (GC - 0.36, -0.4, 0.03, 1.1), (GC - 0.1, -0.42, 0.025, 0.2)):
    kutu_merkez(y, (bx, by), w_, w_ * 0.8, w_ * 0.7, HT, z0=ZT, aci=a_)

# ---------------------------------------------------------------- the small temple of Nefertari
y.bolum('Nefertari tapinagi')
NC = (NX0 + NX1) / 2
NB = 0.045
TN0 = -0.25
kutu(y, V(NX0 - 0.01, TN0, 0), X, NX1 - NX0 + 0.02, NY + 0.03 - TN0, ZN, FT, 'onsagsol')
y.yuz_yon([V(NX0 - 0.01, TN0, ZN), V(NX1 + 0.01, TN0, ZN), V(NX1 + 0.01, NY + 0.03, ZN), V(NX0 - 0.01, NY + 0.03, ZN)], 'zemin', Z)
merdiven(y, (NC, TN0 - 0.04), math.pi / 2, 0.12, 0.0, ZN, n=4, d=0.01, key=FT)
NNF = V(0, -1, NB / NH).normalized()
NP = lambda s, t, d=0.0: V(NC + s, NY + NB * t / NH, ZN + t) + NNF * d
HWN = (NX1 - NX0) / 2
y.yuz_yon([NP(-HWN, 0), NP(HWN, 0), NP(HWN, NH), NP(-HWN, NH)], FT, NNF)
for sg in (-1, 1):
    a0, a1 = NP(sg * HWN, 0), NP(sg * HWN, NH)
    y.yuz_yon([a0, a0 + Y * 0.08, a1 + Y * 0.04, a1], FT, X * sg)
# buttresses (strongly battered, inscribed), statues in the bays, the door in the middle
BW_, SW_, DWN = 0.022, 0.068, 0.05
seq = ['B', 'S', 'B', 'S', 'B', 'S', 'B', 'D', 'B', 'S', 'B', 'S', 'B', 'S', 'B']
genis = {'B': BW_, 'S': SW_, 'D': DWN}
toplam = sum(genis[c] for c in seq)
s = -toplam / 2
heykel = ['kral', 'kralice', 'kral', 'kral', 'kralice', 'kral']
hk = 0
for c in seq:
    w_ = genis[c]
    if c == 'B':
        # a battered pier projecting from the face: deep at the foot, flush at the top
        a, b = s, s + w_
        f0, f1 = 0.05, 0.004
        pts_on = [NP(a, 0, f0), NP(b, 0, f0), NP(b, NH - 0.05, f1), NP(a, NH - 0.05, f1)]
        y.yuz_yon(pts_on, FT, NNF + V(0, -0.3, 0.3))
        for (u, yon) in ((a, -X), (b, X)):
            y.yuz_yon([NP(u, 0, 0), NP(u, 0, f0), NP(u, NH - 0.05, f1), NP(u, NH - 0.05, 0)], FT, yon)
        y.yuz_yon([NP(a, NH - 0.05, f1), NP(b, NH - 0.05, f1), NP(b, NH - 0.05, 0), NP(a, NH - 0.05, 0)], FT, Z)
        Pb = lambda u, t, d=0.0, a=a: NP(a + u, t, 0.05 - (0.05 - 0.004) * t / (NH - 0.05) + d)
        yazi_sutunu(Pb, NNF + V(0, -0.3, 0.3), w_ / 2 - 0.006, 0.04, NH - 0.08, 0.012, 'kum_koyu', 0.016, 0.003, tohum=int(s * 100))
    elif c == 'S':
        p = NP(s + w_ / 2, 0, 0.0)
        tur = heykel[hk]; hk += 1
        kutu_merkez(y, (p.x, p.y - 0.035), w_ * 0.9, 0.07, 0.02, FT, z0=ZN)
        ayakta(p.x, p.y - 0.01, ZN + 0.02, 0.33 if tur == 'kral' else 0.3, tur)
        for sg in (-1, 1):   # a prince and a princess at the knees
            ayakta(p.x + sg * 0.024, p.y - 0.05, ZN + 0.02, 0.07, 'cocuk')
    else:
        # the door: a deep dark doorway with a framed lintel; Hathor above
        a, b = s, s + w_
        dh = 0.17
        m = NP(s + w_ / 2, dh / 2, -0.02)
        ic_ = [(a + 0.012, 0.0), (b - 0.012, 0.0), (b - 0.012, dh), (a + 0.012, dh)]
        for k in range(4):
            p_, q_ = ic_[k], ic_[(k + 1) % 4]
            mid = NP((p_[0] + q_[0]) / 2, (p_[1] + q_[1]) / 2, -0.02)
            y.yuz_yon([NP(*p_, 0.003), NP(*q_, 0.003), NP(*q_, -0.04), NP(*p_, -0.04)], FT, m - mid)
        y.yuz_yon([NP(a + 0.012, 0, -0.04), NP(b - 0.012, 0, -0.04), NP(b - 0.012, dh, -0.04), NP(a + 0.012, dh, -0.04)], 'koyu', NNF)
        for (u0, u1, t0, t1) in ((a, a + 0.012, 0, dh + 0.012), (b - 0.012, b, 0, dh + 0.012), (a, b, dh, dh + 0.016)):
            y.yuz_yon([NP(u0, t0, 0.003), NP(u1, t0, 0.003), NP(u1, t1, 0.003), NP(u0, t1, 0.003)], 'kum_acik', NNF)
        o = NP(s + w_ / 2, dh + 0.06, 0.004)
        y.yuz_yon([o + X * (0.016 * math.cos(TAU * i / 12)) + Z * (0.016 * math.sin(TAU * i / 12)) for i in range(12)], 'boya_kirmizi', NNF)
        for sg in (-1, 1):
            boru(y, [o + X * sg * 0.012 - Z * 0.012, o + X * sg * 0.026 + Z * 0.004, o + X * sg * 0.018 + Z * 0.026], 0.004, 'kum_koyu', n=5)
    s += w_
# torus, cartouche band and cavetto along the top
yazi_bandi(NP, NNF, -HWN + 0.02, HWN - 0.02, NH - 0.045, 0.018, 'kum_koyu', 0.003, tohum=2)
boru(y, [NP(-HWN, NH - 0.02, 0.006), NP(HWN, NH - 0.02, 0.006)], 0.008, FT, n=8)
for sg in (-1, 1):
    boru(y, [NP(sg * (HWN - 0.006), 0, 0.006), NP(sg * (HWN - 0.006), NH - 0.02, 0.006)], 0.008, FT, n=8)
silme(y, [V(NC - HWN, NY + NB * (NH - 0.012) / NH), V(NC + HWN, NY + NB * (NH - 0.012) / NH)], ZN + NH - 0.012, 0.04, 0.03, FT, KAVETTO, kapali=False)
yt = NY + NB * (NH - 0.012) / NH
y.yuz_yon([V(NC - HWN, yt, ZN + NH + 0.028), V(NC + HWN, yt, ZN + NH + 0.028), V(NC + HWN, yt - 0.03, ZN + NH + 0.028), V(NC - HWN, yt - 0.03, ZN + NH + 0.028)], FT, Z)
for k in range(20):
    sc = -HWN + 0.02 + k * (2 * HWN - 0.04) / 19
    p = V(NC + sc, yt - 0.022, ZN + NH + 0.028)
    plaka([p + V(-0.005, 0, 0), p + V(0.005, 0, 0), p + V(0.003, 0, 0.018), p + V(-0.003, 0, 0.018)], 'altin', -Y, 0.003)
    kure(y, p + V(0, 0, 0.022), 0.006, 'boya_kirmizi', n=6, kat=3)

# ---------------------------------------------------------------- river bank: palms, papyrus, a felucca, banners
y.bolum('Nil kiyisi')
for (px, py, b) in ((-1.1, -0.48, 0.2), (-1.0, -0.56, 0.16), (-1.14, -0.62, 0.17), (0.98, -0.42, 0.19), (1.1, -0.5, 0.17), (0.36, -0.6, 0.15)):
    agac(y, px, py, Z0, b, 'palmiye')
for (px, py) in ((-0.8, -0.79), (-0.72, -0.82), (-0.66, -0.8), (0.5, -0.8), (0.58, -0.83), (0.85, -0.79), (0.93, -0.82)):
    for k in range(5):
        a = TAU * k / 5 + px * 3
        boru(y, [V(px, py, ZW), V(px + 0.012 * math.cos(a), py + 0.012 * math.sin(a), ZW + 0.05 + 0.01 * (k % 2))], 0.0025, 'boya_yesil', n=4)
        kure(y, (px + 0.014 * math.cos(a), py + 0.014 * math.sin(a), ZW + 0.056 + 0.01 * (k % 2)), 0.008, 'boya_yesil', n=6, kat=3)
# a felucca on the Nile: hull, mast, lateen sail
FXC, FYC = 0.55, -1.0
with parca(y, (FXC, FYC, ZW), 0.15):
    hal = []
    for k in range(9):
        t = -1 + 2 * k / 8
        w_ = 0.04 * (1 - t * t) ** 0.55 + 0.002
        z_ = 0.012 + 0.012 * t * t
        xx = t * 0.16
        hal.append([V(xx, -w_, z_), V(xx, -w_ * 0.6, -0.004), V(xx, 0, -0.006), V(xx, w_ * 0.6, -0.004), V(xx, w_, z_)])
    for k in range(8):
        for m in range(4):
            q = [hal[k][m], hal[k + 1][m], hal[k + 1][m + 1], hal[k][m + 1]]
            yuz_dis(y, q, 'ahsap', V((q[0].x + q[1].x) / 2, 0, 0.03))
        y.yuz_yon([hal[k][0], hal[k][4], hal[k + 1][4], hal[k + 1][0]], 'ahsap_acik', Z)
    y.silindir((0.02, 0), 0.004, 0.0, 0.26, 'ahsap', n=6)
    plaka([V(-0.13, 0.004, 0.03), V(0.07, 0.004, 0.06), V(0.03, 0.004, 0.3)], 'kumas', Y, 0.003)
    cubuk(y, V(-0.14, 0.006, 0.026), V(0.04, 0.006, 0.31), 0.004, 'ahsap_koyu')
sancak(y, GC + 0.14, TY0 + 0.015, ZT + 0.036, boy=0.26, en=0.13, yuk=0.075, aci=-math.pi * 0.15)
sancak(y, NX0 + 0.02, TN0 + 0.03, ZN, boy=0.2, en=0.1, yuk=0.06, aci=-math.pi * 0.2)

calistir(y, 'lm_abusimbel')
