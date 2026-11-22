# Karnak Tapınağı (lm_karnak): the Amun precinct at Karnak, compressed: an avenue of ram-headed sphinxes and a pair of
# obelisks before the great first pylon (battered sandstone towers with torus rolls, cavetto cornices, flagpole niches
# with coloured pennants, painted smiting reliefs, a gate under the winged sun disk); a court with the Taharqa column
# and two colossi; the great hypostyle hall (tall open-papyrus nave columns, closed-bud aisle columns, screen walls,
# a raised nave with grilled clerestory windows, flat roof); the White Chapel of Senusret and the sacred lake.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05
TAS = 'kum'
KOYU = 'kum_koyu'
ACIK = 'kum_acik'

# cavetto cornice (Egyptian gorge): a torus roll, then the hollow flaring out, a flat top band
KAVETTO = [(0, 0), (0.16, 0.03), (0.2, 0.1), (0.12, 0.17), (0.04, 0.19), (0.07, 0.36), (0.18, 0.56), (0.4, 0.75),
           (0.72, 0.88), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]


# ---------------------------------------------------------------- helpers
def kavetto(kose, z, h, c, key=TAS, kapali=True, ust=True):
    """a cavetto cornice on top of a wall polygon kose (z: its foot), its top capped (ust)"""
    silme(y, kose, z, h, c, key, KAVETTO, kapali)
    if ust and kapali:
        y.yuz_yon([V(p.x, p.y, z + h) for p in kose], key, Z)


def egik_blok(x0, x1, y0, y1, z0, h, ix, iy, key=TAS, yuzler=(0, 1, 2, 3)):
    """a battered block (pylon tower, mastaba): the top inset ix in x and iy in y; returns base and top corners"""
    B = dikdortgen(x0, x1, y0, y1, z0); T = dikdortgen(x0 + ix, x1 - ix, y0 + iy, y1 - iy, z0 + h)
    for i in yuzler:
        j = (i + 1) % 4
        e = B[j] - B[i]; n = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], key, n + Z * 0.2)
    return B, T


def cerceve_yuz(o, ex, up, n):
    """a frame on a (possibly battered) face: P(s, t, d) = o + ex s + up t + n d"""
    o, ex, up, n = V(*o), V(*ex), V(*up), V(*n).normalized()
    return lambda s, t, d=0.003: o + ex * s + up * t + n * d


def levha(P, s0, s1, t0, t1, key, n, d=0.003):
    y.yuz_yon([P(s0, t0, d), P(s1, t0, d), P(s1, t1, d), P(s0, t1, d)], key, n)


def yazi_sutunu(P, n, s0, t0, t1, w=0.012, key=KOYU, adim=0.016, d=0.003, tohum=0):
    """a vertical column of hieroglyphs: small marks of varying shape, alternating sides"""
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


def yazi_bandi(P, n, s0, s1, t0, h, key=KOYU, d=0.003, tohum=0):
    """a horizontal register of hieroglyphs between s0 and s1"""
    w = h * 0.7; s = s0; k = 0
    while s + w < s1:
        r = (tohum * 5 + k * 7) % 4
        if r == 0: levha(P, s, s + w, t0, t0 + h, key, n, d)
        elif r == 1: levha(P, s, s + w, t0 + h * 0.3, t0 + h * 0.6, key, n, d)
        elif r == 2: y.yuz_yon([P(s, t0, d), P(s + w, t0, d), P(s + w * 0.5, t0 + h, d)], key, n)
        else: levha(P, s + w * 0.3, s + w * 0.7, t0, t0 + h, key, n, d)
        s += w * 1.5; k += 1


def firavun_kabartma(P, n, sc, t0, H, yon=1, d=0.0035):
    """a painted relief of the pharaoh smiting his enemies (stylised from quads), centre s = sc, feet at t0, H tall.
    yon: +1 faces +s"""
    # polygons in figure units (s forward, t up, both x H); every body part also casts a dark rim down and behind it,
    # so the figure reads as carved relief standing out of the wall, not as a sticker
    def F(pts, key, kat=1, golge=True):
        dd = d + 0.0012 * kat
        Pw = lambda s, t, dz: P(sc + yon * s * H, t0 + t * H, dz)
        if golge:
            y.yuz_yon([Pw(s + 0.012, t - 0.014, d - 0.0008) for s, t in pts], KOYU, n)
        y.yuz_yon([Pw(s, t, dd) for s, t in pts], key, n)
    def kol(a, b, w):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); px, py = -dy / L * w / 2, dx / L * w / 2
        return [(a[0] + px, a[1] + py), (a[0] - px, a[1] - py), (b[0] - px, b[1] - py), (b[0] + px, b[1] + py)]
    def daire(c, r, k=8):
        return [(c[0] + r * math.cos(TAU * i / k), c[1] + r * math.sin(TAU * i / k)) for i in range(k)]
    ten = 'kirmizi'
    # two captives kneeling before him, arms raised, held by the hair (drawn first: they stand behind his hand)
    for i, (ds, dt, key) in enumerate(((0.07, 0.04, 'ahsap_acik'), (0.0, 0.0, 'kerpic_koyu'))):
        F([(0.27 + ds, 0.0 + dt), (0.44 + ds, 0.0 + dt), (0.41 + ds, 0.08 + dt), (0.29 + ds, 0.3 + dt)], key)
        F([(0.27 + ds, 0.28 + dt), (0.35 + ds, 0.3 + dt), (0.33 + ds, 0.58 + dt), (0.27 + ds, 0.58 + dt)], key)
        F(kol((0.31 + ds, 0.52 + dt), (0.4 + ds, 0.74 + dt), 0.035), key)
        F(daire((0.3 + ds, 0.63 + dt), 0.045), 'koyu' if i else 'kerpic_koyu')
        F([(0.26 + ds, 0.24 + dt), (0.36 + ds, 0.24 + dt), (0.355 + ds, 0.3 + dt), (0.265 + ds, 0.3 + dt)], 'beyaz', 2, False)
    # striding legs and feet
    F([(-0.125, 0.0), (-0.07, 0.0), (-0.04, 0.35), (-0.095, 0.35)], ten)
    F([(0.055, 0.0), (0.11, 0.0), (0.075, 0.35), (0.02, 0.35)], ten)
    F([(-0.165, 0.0), (-0.07, 0.0), (-0.075, 0.03), (-0.15, 0.03)], ten)
    F([(0.055, 0.0), (0.175, 0.0), (0.165, 0.03), (0.06, 0.03)], ten)
    # the shendyt kilt with its gold apron and belt
    F([(-0.11, 0.33), (0.15, 0.3), (0.1, 0.52), (-0.095, 0.52)], 'beyaz', 2)
    F([(-0.012, 0.32), (0.03, 0.32), (0.026, 0.5), (-0.008, 0.5)], 'altin', 3, False)
    F([(-0.095, 0.5), (0.1, 0.5), (0.1, 0.535), (-0.095, 0.535)], 'altin', 3, False)
    # torso widening to the shoulders, the broad collar
    F([(-0.075, 0.53), (0.08, 0.53), (0.115, 0.75), (0.07, 0.79), (-0.07, 0.79), (-0.115, 0.75)], ten)
    F([(-0.1, 0.73), (0.1, 0.73), (0.075, 0.785), (-0.075, 0.785)], 'turkuaz', 2, False)
    # head in profile, the eye, the white crown and its uraeus
    F([(-0.025, 0.78), (0.03, 0.78), (0.03, 0.81), (-0.025, 0.81)], ten)
    F([(-0.045, 0.8), (0.04, 0.8), (0.05, 0.83), (0.048, 0.89), (-0.045, 0.89)], ten)
    F([(0.046, 0.83), (0.068, 0.845), (0.046, 0.866)], ten)
    F([(0.012, 0.848), (0.036, 0.848), (0.036, 0.86), (0.012, 0.86)], 'koyu', 2, False)
    F([(-0.05, 0.885), (0.045, 0.885), (0.04, 0.94), (0.022, 1.0), (0.008, 1.04), (-0.012, 1.04), (-0.028, 1.0), (-0.042, 0.94)], 'beyaz', 2)
    F(daire((-0.002, 1.05), 0.02), 'beyaz', 2)
    F([(0.04, 0.89), (0.06, 0.9), (0.052, 0.935), (0.038, 0.925)], 'altin', 3, False)
    # the raised arm swinging the pear-shaped mace behind his head; the other arm forward, gripping the captives' hair
    F(kol((-0.08, 0.755), (-0.19, 0.86), 0.04), ten)
    F(kol((-0.19, 0.86), (-0.15, 1.0), 0.036), ten)
    F(kol((-0.15, 1.0), (-0.29, 1.07), 0.014), 'altin', 2)
    F(daire((-0.3, 1.075), 0.032), 'beyaz', 3)
    F(kol((0.07, 0.745), (0.29, 0.705), 0.036), ten)
    F(daire((0.3, 0.7), 0.024), ten, 2)
    # his cartouche over the captives
    F([(0.15, 0.86), (0.25, 0.86), (0.25, 1.05), (0.15, 1.05)], 'beyaz', 1)
    F([(0.165, 0.88), (0.235, 0.88), (0.235, 1.03), (0.165, 1.03)], 'lacivert', 2, False)


def kanatli_gunes(o, ex, n, en, h, d=0.004):
    """the winged sun disk over a gate: o centre on the wall, ex along, n out"""
    o, ex, n = V(*o), V(*ex), V(*n).normalized()
    P = lambda s, t, dd=d: o + ex * s + Z * t + n * dd
    r = h * 0.5
    y.yuz_yon([P(r * math.cos(TAU * i / 14), r * math.sin(TAU * i / 14), d + 0.001) for i in range(14)], 'altin', n)
    for s in (-1, 1):
        for k, key in enumerate(('lacivert', 'turkuaz', 'boya_kirmizi')):
            a0 = -h * 0.42 + k * h * 0.26
            y.yuz_yon([P(s * r * 0.9, a0), P(s * en / 2, a0 + h * 0.12 + k * 0.004), P(s * en / 2, a0 + h * 0.3 + k * 0.004), P(s * r * 0.9, a0 + h * 0.26)], key, n)
        # uraeus cobras by the disk
        y.yuz_yon([P(s * r, -r * 0.9, d + 0.0012), P(s * (r + h * 0.12), -r * 0.9, d + 0.0012), P(s * (r + h * 0.1), r * 0.3, d + 0.0012), P(s * r, r * 0.3, d + 0.0012)], 'boya_yesil', n)


def flama(x, yy, z, key, en=0.16, yuk=0.035, aci=0.0, dalga=0.014, n=7):
    """a long pennant on a pole (top z), in key; 'mavi' is the team colour"""
    e = V(math.cos(aci), math.sin(aci)); nn = V(-e.y, e.x)
    o = V(x, yy, z - 0.012 - yuk)
    def P(u, v, s):
        w = math.sin(u * math.pi * 1.7) * dalga * u
        sag = -0.5 * u * u * yuk * 0.6
        return o + e * (0.007 + u * en) + nn * (w + s * 0.0015) + Z * (v * (1 - 0.55 * u) + sag + yuk * 0.275 * u)
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        y.yuz_yon([P(u0, 0, 1), P(u1, 0, 1), P(u1, yuk, 1), P(u0, yuk, 1)], key, nn)
        y.yuz_yon([P(u0, 0, -1), P(u1, 0, -1), P(u1, yuk, -1), P(u0, yuk, -1)], key, -nn)
        y.yuz_yon([P(u0, yuk, 1), P(u1, yuk, 1), P(u1, yuk, -1), P(u0, yuk, -1)], key, Z)
        y.yuz_yon([P(u0, 0, 1), P(u1, 0, 1), P(u1, 0, -1), P(u0, 0, -1)], key, -Z)
        if i == n - 1:
            y.yuz_yon([P(1, 0, 1), P(1, yuk, 1), P(1, yuk, -1), P(1, 0, -1)], key, e)


def tomurcuk_sutun(cx, cy, z0, z1, r, key=TAS, bant='boya_kirmizi', bant2='turkuaz'):
    """a papyrus-bundle column with a closed-bud capital (the hypostyle aisles): disc base, six-lobed shaft narrowing
    at the foot, tie bands, a bud capital painted in strips, an abacus"""
    H = z1 - z0; c = (cx, cy)
    donel(y, c, [(r * 1.4, z0), (r * 1.4, z0 + H * 0.035), (r * 1.1, z0 + H * 0.045)], key, n=12)
    zb = z1 - H * 0.2
    prev = None
    for t in (0, 0.08, 0.5, 1.0):
        rr = r * (0.86 + 0.14 * min(1, t / 0.08)) * (1 - 0.07 * t)
        ring = [V(cx + rr * (1 if i % 2 == 0 else 0.84) * math.cos(TAU * i / 12), cy + rr * (1 if i % 2 == 0 else 0.84) * math.sin(TAU * i / 12),
                  z0 + H * 0.045 + (zb - z0 - H * 0.045) * t) for i in range(12)]
        if prev: y.serit(prev, ring, key)
        prev = ring
    for j in range(2):
        halka_kornis(y, c, r * 0.92, zb - H * 0.05 + j * H * 0.025, H * 0.014, r * 0.1, 12, bant if j == 0 else bant2)
    donel(y, c, [(r * 0.93, zb), (r * 1.18, zb + H * 0.06), (r * 1.15, zb + H * 0.12), (r * 0.8, zb + H * 0.175), (r * 0.7, zb + H * 0.185)],
          key, n=12, dilim=[key, bant2, key, bant])
    kutu_merkez(y, c, r * 1.6, r * 1.6, H * 0.015, key, z0=z1 - H * 0.015)


def koc_sfenks(x, yy, aci, z0):
    """a ram-headed sphinx (criosphinx) on its pedestal, built facing +x then turned to aci; a small Amun-protected
    king stands between its paws"""
    with parca(y, (x, yy, z0), aci, 1.15):
        kutu_merkez(y, (0, 0), 0.16, 0.062, 0.03, TAS, z0=0)
        kornis(y, -0.08, 0.08, -0.031, 0.031, 0.03, 0.006, 0.004, ACIK, 'tac')
        y.yuz([V(-0.08, -0.031, 0.036), V(0.08, -0.031, 0.036), V(0.08, 0.031, 0.036), V(-0.08, 0.031, 0.036)], ACIK)
        z = 0.036
        # couchant lion body: a low haunch rising to the shoulders, folded hind legs, outstretched forelegs
        boru(y, [V(-0.06, 0, z + 0.016), V(-0.03, 0, z + 0.019), V(0.0, 0, z + 0.022), V(0.022, 0, z + 0.026)], 0.017, TAS, n=10, r_son=0.02)
        kure(y, (-0.058, 0, z + 0.016), 0.017, TAS, n=10, kat=5)
        for s in (-1, 1):
            boru(y, [V(-0.064, s * 0.012, z + 0.007), V(-0.04, s * 0.016, z + 0.012), V(-0.022, s * 0.015, z + 0.006)], 0.008, TAS, n=6)   # hind leg
            cubuk(y, V(0.022, s * 0.012, z + 0.006), V(0.07, s * 0.012, z + 0.005), 0.012, TAS, 0.011)   # forelegs
            kutu_merkez(y, (0.073, s * 0.012), 0.012, 0.014, 0.008, ACIK, z0=z)
        boru(y, [V(-0.072, 0.012, z + 0.003), V(-0.05, 0.022, z + 0.002), V(-0.02, 0.024, z + 0.003)], 0.0028, TAS, n=4)   # tail
        # chest and the striped lappets of the headcloth falling on it
        donel(y, (0.03, 0), [(0.022, z + 0.006), (0.024, z + 0.03), (0.02, z + 0.05), (0.0, z + 0.054)], TAS, n=10)
        for s in (-1, 1):
            for k in range(3):
                kutu_merkez(y, (0.044, s * 0.016), 0.01, 0.012, 0.007, 'lacivert' if k % 2 else 'boya_sari', z0=z + 0.026 + k * 0.009)
        # ram head: a long muzzle, the drooping ears, a sun disk with uraeus on the brow
        boru(y, [V(0.03, 0, z + 0.06), V(0.055, 0, z + 0.062), V(0.08, 0, z + 0.05)], 0.0155, TAS, n=10, r_son=0.0085)
        kure(y, (0.031, 0, z + 0.06), 0.0155, TAS, n=10, kat=5)
        kure(y, (0.026, 0, z + 0.083), 0.0095, 'altin', n=8, kat=4)
        # the curled horns: a flat spiral round each side of the head, curving down and forward
        for s in (-1, 1):
            pts = []
            for k in range(9):
                a = 1.75 * math.pi * k / 8
                rr = 0.017 * (1 - 0.62 * k / 8)
                pts.append(V(0.036 - rr * math.sin(a), s * (0.015 + 0.006 * k / 8), z + 0.068 - rr * (1 - math.cos(a)) * 0.95))
            boru(y, pts, 0.0048, ACIK, n=5, r_son=0.0024)
            boru(y, [V(0.04, s * 0.012, z + 0.06), V(0.046, s * 0.024, z + 0.052)], 0.004, TAS, n=4, r_son=0.002)   # ear
        # the little king statue between the paws
        kutu_merkez(y, (0.058, 0), 0.012, 0.012, 0.03, ACIK, z0=z)
        kure(y, (0.058, 0, z + 0.034), 0.006, ACIK, n=6, kat=3)


def kolos(x, yy, aci, z0, s=1.0):
    """a standing colossus of the king in nemes and double crown on a block base, built facing +x"""
    with parca(y, (x, yy, z0), aci, s):
        kutu_merkez(y, (0, 0), 0.1, 0.08, 0.04, 'granit', z0=0)
        silme(y, dikdortgen(-0.05, 0.05, -0.04, 0.04), 0.04, 0.006, 0.004, 'granit', 'tac')
        y.yuz([V(-0.05, -0.04, 0.046), V(0.05, -0.04, 0.046), V(0.05, 0.04, 0.046), V(-0.05, 0.04, 0.046)], 'granit')
        z = 0.046
        kutu_merkez(y, (-0.012, 0), 0.05, 0.075, 0.24, 'granit', z0=z)          # back pillar
        for sy, dx in ((-1, 0.012), (1, -0.004)):
            kutu_merkez(y, (dx, sy * 0.012), 0.022, 0.018, 0.09, 'granit', z0=z)  # legs (left leg forward)
            kutu_merkez(y, (dx + 0.008, sy * 0.012), 0.038, 0.02, 0.008, 'granit', z0=z)
        kutu_merkez(y, (0.004, 0), 0.034, 0.056, 0.04, 'beyaz', z0=z + 0.088)    # shendyt kilt
        kutu_merkez(y, (0.014, 0), 0.006, 0.014, 0.034, 'altin', z0=z + 0.088)
        donel(y, (0.002, 0), [(0.026, z + 0.128), (0.032, z + 0.17), (0.034, z + 0.19), (0, z + 0.192)], 'granit', n=8)   # torso
        kutu_merkez(y, (0.006, 0), 0.03, 0.068, 0.012, 'turkuaz', z0=z + 0.17)  # broad collar
        for sy in (-1, 1):
            cubuk(y, V(0.004, sy * 0.034, z + 0.18), V(0.006, sy * 0.034, z + 0.11), 0.012, 'granit')   # arms at the sides
        kure(y, (0.006, 0, z + 0.205), 0.016, 'granit', n=10, kat=5)             # head
        # nemes: striped lappets and the flaring headcloth
        for sy in (-1, 1):
            kutu_merkez(y, (0.008, sy * 0.017), 0.012, 0.008, 0.035, 'boya_sari', z0=z + 0.168)
        donel(y, (0.002, 0), [(0.024, z + 0.2), (0.02, z + 0.215), (0.0, z + 0.222)], 'boya_sari', n=8)
        # double crown: the red outer and the white inner
        donel(y, (0.0, 0), [(0.017, z + 0.215), (0.017, z + 0.235), (0.012, z + 0.24), (0.0, z + 0.24)], 'boya_kirmizi', n=8)
        donel(y, (-0.002, 0), [(0.01, z + 0.238), (0.009, z + 0.262), (0.006, z + 0.272), (0, z + 0.276)], 'beyaz', n=8)
        kutu_merkez(y, (0.024, 0), 0.004, 0.004, 0.022, 'granit', z0=z + 0.178)   # beard


# ---------------------------------------------------------------- ground
y.bolum('Zemin')
XW, YF, YB = 1.18, -1.22, 1.0
zemin(y, -XW, XW, YF, YB, Z0, KOYU, ACIK, basamak=(('on', 0.5),), n_basamak=3)
LX0, LX1, LY0, LY1 = 0.8, 1.1, -0.05, 0.84      # the sacred lake (sunk into the platform)


def zemin_delik(x0, x1, y0, y1):
    """cut a rectangular hole in the platform's paved top (the sacred lake)"""
    for i, (pts, key) in enumerate(y.faces):
        if key == ACIK and len(pts) == 4 and all(abs(p[2] - Z0) < 1e-9 for p in pts) and abs(pts[1][0] - pts[0][0]) > 2:
            break
    del y.faces[i]
    xs, ys = [-XW, x0, x1, XW], [YF, y0, y1, YB]
    for a in range(3):
        for b in range(3):
            if a == 1 and b == 1: continue
            y.yuz([V(xs[a], ys[b], Z0), V(xs[a + 1], ys[b], Z0), V(xs[a + 1], ys[b + 1], Z0), V(xs[a], ys[b + 1], Z0)], ACIK)


zemin_delik(LX0, LX1, LY0, LY1)
# paved processional way, the court and the hall floor
for x0, x1, y0, y1 in ((-0.26, 0.26, YF + 0.01, -0.62), (-0.74, 0.74, -0.38, 0.92)):
    y.yuz([V(x0, y0, Z0 + 0.002), V(x1, y0, Z0 + 0.002), V(x1, y1, Z0 + 0.002), V(x0, y1, Z0 + 0.002)], 'zemin')

# ---------------------------------------------------------------- sphinx avenue, obelisks
y.bolum('Koc basli sfenksler')
for k in range(3):
    yy = YF + 0.12 + k * 0.14
    koc_sfenks(-0.18, yy, 0.0, Z0 + 0.002)
    koc_sfenks(0.18, yy, math.pi, Z0 + 0.002)

y.bolum('Dikilitaslar')
for sx in (-1, 1):
    dikilitas(y, (sx * 0.36, -0.79), 0.06, 0.56, 'granit_kizil', 'altin', z0=Z0, yazi_key='granit_kizil_koyu')

# ---------------------------------------------------------------- the first pylon
y.bolum('Pilon')
PY0, PY1 = -0.63, -0.38          # tower base front / back
PH = 0.68                        # tower height
GX = 0.15                        # gate half width
TX = 0.78                        # tower outer x
IX, IY = 0.06, 0.04              # batter
PZ = Z0
CORN = 0.07                      # cornice height
for sx in (-1, 1):
    x0, x1 = (GX, TX) if sx > 0 else (-TX, -GX)
    B = dikdortgen(x0, x1, PY0, PY1, PZ)
    T = dikdortgen(x0 + IX, x1 - IX, PY0 + IY, PY1 - IY, PZ + PH)
    # the front face with four flagpole niches (real depth), the back and the sides plain
    up = V(0, IY / PH, 1)
    nf = V(0, -1, IY / PH).normalized()
    P = cerceve_yuz(B[0], X, up, nf)
    W0 = x1 - x0
    # niche s-ranges, measured from x0 (in the middle of the face so the battered sides do not cut them)
    nis = [(0.07, 0.11), (0.155, 0.195), (W0 - 0.195, W0 - 0.155), (W0 - 0.11, W0 - 0.07)]
    sinir = [0.0] + [v for ab in nis for v in ab] + [W0]
    # the face strips between the niches; at the outer edges the strip follows the side batter
    def fp(s, t, d=0.0):
        # point on the front face: the side batter narrows the face towards the top
        lo = x0 + IX * t / PH; hi = x1 - IX * t / PH
        xx = min(max(x0 + s, lo), hi)
        return V(xx, PY0 + IY * t / PH, PZ + t) + nf * d
    for k in range(0, len(sinir) - 1):
        s0, s1 = sinir[k], sinir[k + 1]
        if k % 2 == 1:   # a niche: recessed back, two cheeks
            dn = 0.022
            y.yuz_yon([fp(s0, 0, -dn), fp(s1, 0, -dn), fp(s1, PH, -dn), fp(s0, PH, -dn)], KOYU, nf)
            y.yuz_yon([fp(s0, 0, -dn), fp(s0, 0), fp(s0, PH), fp(s0, PH, -dn)], KOYU, X)
            y.yuz_yon([fp(s1, 0, -dn), fp(s1, 0), fp(s1, PH), fp(s1, PH, -dn)], KOYU, -X)
            y.yuz_yon([fp(s0, 0, -dn), fp(s1, 0, -dn), fp(s1, 0), fp(s0, 0)], KOYU, -Z)
        else:
            if k == 0:
                y.yuz_yon([B[0], fp(s1, 0), fp(s1, PH), T[0]], TAS, nf)
            elif k == len(sinir) - 2:
                y.yuz_yon([fp(s0, 0), B[1], T[1], fp(s0, PH)], TAS, nf)
            else:
                y.yuz_yon([fp(s0, 0), fp(s1, 0), fp(s1, PH), fp(s0, PH)], TAS, nf)
    for i in (1, 2, 3):
        j = (i + 1) % 4
        e = B[j] - B[i]; n = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], TAS, n + Z * 0.08)
    # reliefs on the back and the outer side: registers of offering scenes and text bands
    for i in (2, 1 if sx > 0 else 3):
        j = (i + 1) % 4
        Lb = (B[j] - B[i]).length
        e = B[j] - B[i]; nn = V(e.y, -e.x).normalized()
        nfz = (nn + Z * ((B[i] - T[i]).dot(nn) / PH)).normalized()
        def Pf(s_, t_, d_=0.003, i=i, j=j, Lb=Lb, nfz=nfz):
            u = s_ / Lb
            return B[i].lerp(B[j], u).lerp(T[i].lerp(T[j], u), t_ / PH) + nfz * d_
        if i == 2:
            levha(Pf, 0.08, Lb - 0.08, 0.12, 0.5, ACIK, nfz, 0.0015)
            firavun_kabartma(Pf, nfz, Lb * 0.36, 0.17, 0.26, yon=1)
            firavun_kabartma(Pf, nfz, Lb * 0.74, 0.17, 0.2, yon=-1)
            yazi_bandi(Pf, nfz, 0.1, Lb - 0.1, 0.45, 0.022, 'lacivert', 0.0035, tohum=9)
            yazi_bandi(Pf, nfz, 0.1, Lb - 0.1, 0.135, 0.016, KOYU, 0.0035, tohum=2)
        else:
            for t_ in (0.2, 0.42):
                yazi_bandi(Pf, nfz, 0.04, Lb - 0.04, t_, 0.018, KOYU, 0.003, tohum=int(t_ * 10))
    # torus rolls up the corners and along the top
    for i in range(4):
        boru(y, [B[i] + Z * 0.0, T[i]], 0.011, ACIK, n=6)
    silme(y, T, PZ + PH - 0.016, 0.016, 0.006, ACIK, 'yarim')
    kavetto(T, PZ + PH, CORN, 0.05, TAS)
    # the tower top: the joints of its paving slabs, the stairhead of the stair inside the tower
    zt_ = PZ + PH + CORN
    for k in range(1, 6):
        yy_ = T[0].y + (T[3].y - T[0].y) * k / 6
        kutu(y, V(T[0].x + 0.02, yy_ - 0.003, zt_), X, T[1].x - T[0].x - 0.04, 0.006, 0.0025, KOYU, 'onarkaust')
    if sx < 0:
        hx_, hy_ = (T[0].x + T[1].x) / 2 + 0.1, (T[0].y + T[3].y) / 2
        kutu_merkez(y, (hx_, hy_), 0.08, 0.07, 0.05, TAS, z0=zt_)
        kornis(y, hx_ - 0.04, hx_ + 0.04, hy_ - 0.035, hy_ + 0.035, zt_ + 0.05, 0.008, 0.005, ACIK, 'tac')
        y.yuz([V(hx_ - 0.045, hy_ - 0.04, zt_ + 0.058), V(hx_ + 0.045, hy_ - 0.04, zt_ + 0.058), V(hx_ + 0.045, hy_ + 0.04, zt_ + 0.058), V(hx_ - 0.045, hy_ + 0.04, zt_ + 0.058)], ACIK)
        y.yuz_yon([V(hx_ - 0.016, hy_ - 0.0375, zt_), V(hx_ + 0.016, hy_ - 0.0375, zt_), V(hx_ + 0.016, hy_ - 0.0375, zt_ + 0.036), V(hx_ - 0.016, hy_ - 0.0375, zt_ + 0.036)], 'koyu', -Y)
    # painted relief in the middle panel: the king smiting, framed by hieroglyph columns
    sm = (nis[1][1] + nis[2][0]) / 2
    Pr = lambda s, t, d=0.003: fp(s, t, d)
    rel_n = nf
    levha(Pr, nis[1][1] + 0.025, nis[2][0] - 0.025, 0.1, 0.58, ACIK, rel_n, 0.0015)
    firavun_kabartma(Pr, rel_n, sm + sx * 0.03, 0.16, 0.34, yon=-sx)
    yazi_bandi(Pr, rel_n, nis[1][1] + 0.03, nis[2][0] - 0.03, 0.115, 0.018, KOYU, 0.0035, tohum=5)
    # small square windows near the top (they held the flagpole beams), with real depth
    for (a_, b_) in ((nis[0][1], nis[1][0]), (nis[2][1], nis[3][0])):
        m_ = (a_ + b_) / 2
        for t_ in (PH * 0.8,):
            w_ = 0.012
            levha(Pr, m_ - w_ - 0.005, m_ + w_ + 0.005, t_ - 0.005, t_ + 2 * w_ + 0.005, ACIK, nf, 0.0022)
            levha(Pr, m_ - w_, m_ + w_, t_, t_ + 2 * w_, 'koyu', nf, 0.0032)
    # smaller reliefs on the outer panels: offering figures
    for s0, s1 in ((0.03, nis[0][0] - 0.015), (nis[0][1] + 0.015, nis[1][0] - 0.015), (nis[2][1] + 0.015, nis[3][0] - 0.015), (nis[3][1] + 0.015, W0 - 0.03)):
        if s1 - s0 < 0.03: continue
        yazi_sutunu(Pr, rel_n, (s0 + s1) / 2 - 0.006, 0.14, 0.5, 0.012, KOYU, tohum=int(s0 * 100) + 1)
    # flagpoles in the niches: cedar masts held by clamps, gilded tips, long pennants
    for k, (s0, s1) in enumerate(nis):
        sx_ = x0 + (s0 + s1) / 2
        py = PY0 + IY - 0.006
        top = PZ + PH + 0.3
        y.silindir((sx_, py), 0.0075, PZ, top, 'ahsap', n=6)
        y.koni((sx_, py), 0.01, top, 0.03, 'altin', n=6)
        for t in (0.45, 0.66):
            cubuk(y, fp(s0 + 0.004, PH * t, -0.01), V(sx_, py - 0.008, PZ + PH * t), 0.006, 'ahsap_koyu')
            cubuk(y, fp(s1 - 0.004, PH * t, -0.01), V(sx_, py - 0.008, PZ + PH * t), 0.006, 'ahsap_koyu')
        renk = [['boya_kirmizi', 'beyaz', 'boya_sari', 'boya_yesil'], ['boya_sari', 'boya_kirmizi', 'beyaz', 'boya_yesil']][sx > 0][k]
        aci = -0.25 if sx < 0 else -0.35
        if sx < 0 and k == 1:
            sancak(y, sx_, py, top - 0.18, boy=0.18, en=0.15, yuk=0.075, aci=aci, direk_key='ahsap')
        else:
            flama(sx_, py, top - 0.02, renk, 0.17, 0.034, aci)

# the gate between the towers: a taller-than-wide portal with its own cornice, cedar doors, the winged sun
y.bolum('Pilon kapisi')
GH = 0.44
GY0, GY1 = PY0 - 0.035, PY1 + 0.035
kutu(y, V(-GX, GY0, PZ), X, 2 * GX, GY1 - GY0, GH, TAS, 'sagsolust')
for (a, b, nn) in ((V(-GX, GY0), V(GX, GY0), -1), (V(GX, GY1), V(-GX, GY1), 1)):
    W_, e_, nc_, L_ = dikdortgen_acik(y, a, b, PZ, GH, 0.27, 0.73, 0.0, 0.27, (TAS, KOYU, ACIK, 'ahsap'), derin=0.03,
                                      cerceve=(0.012, ACIK))
    # bronze-studded double doors, a gilded lintel band
    cc = (a + b) / 2
    kanatli_gunes(cc + Z * (PZ + 0.335) + nc_ * 0.0, e_, nc_, 2 * GX * 0.8, 0.05)
    yazi_bandi(lambda s, t, d=0.003: a + e_ * s + Z * (PZ + t) + nc_ * d, nc_, 0.02, 2 * GX - 0.02, GH * 0.88, 0.016, KOYU, 0.003, tohum=7)
silme(y, dikdortgen(-GX, GX, GY0, GY1), PZ + GH - 0.012, 0.012, 0.005, ACIK, 'yarim')
kavetto(dikdortgen(-GX, GX, GY0, GY1), PZ + GH, 0.055, 0.04, TAS)
# the door leaves: studded bands on the dark back
for (yy, nn) in ((GY0 + 0.03, -1), (GY1 - 0.03, 1)):
    for k in range(4):
        z = PZ + 0.04 + k * 0.06
        kutu_merkez(y, (0, yy - nn * 0.002), 2 * GX * 0.44, 0.003, 0.006, 'bronz', z0=z)

# ---------------------------------------------------------------- the court: Taharqa column, colossi
y.bolum('Avlu')
# side walls of the court with a plain cornice
for sx in (-1, 1):
    a, b = (V(sx * 0.74, PY1 - 0.01), V(sx * 0.74, 0.0)) if sx < 0 else (V(sx * 0.74, 0.0), V(sx * 0.74, PY1 - 0.01))
    a2 = V(a.x - sx * 0.04, a.y); b2 = V(b.x - sx * 0.04, b.y)
    kutu_merkez(y, (sx * 0.72, (PY1 + 0.0) / 2), 0.04, abs(PY1), 0.2, TAS, z0=Z0)
    silme(y, dikdortgen(sx * 0.72 - 0.02, sx * 0.72 + 0.02, PY1 - 0.0, 0.0), Z0 + 0.2, 0.035, 0.022, TAS, KAVETTO)
    y.yuz([V(sx * 0.72 - 0.02, PY1, Z0 + 0.235), V(sx * 0.72 + 0.02, PY1, Z0 + 0.235), V(sx * 0.72 + 0.02, 0.0, Z0 + 0.235), V(sx * 0.72 - 0.02, 0.0, Z0 + 0.235)], TAS)
    # a row of bud columns along the court wall (the Bubastite colonnade)
    for k in range(3):
        tomurcuk_sutun(sx * 0.62, PY1 + 0.07 + k * 0.11, Z0, Z0 + 0.2, 0.02)
    x_a, x_b = sorted((sx * 0.6, sx * 0.72))
    kutu(y, V(x_a, PY1 + 0.03, Z0 + 0.2), X, x_b - x_a, 0.0 - PY1 - 0.06 + 0.03, 0.025, TAS)
# Taharqa's single column, off axis
sutun(y, 0.3, -0.16, Z0, Z0 + 0.5, 0.036, TAS, 'misir', bant_key='boya_kirmizi')
kutu_merkez(y, (0.3, -0.16), 0.1, 0.1, 0.018, TAS, z0=Z0)
for sx in (-1, 1):
    kolos(sx * 0.2, -0.06, -math.pi / 2, Z0, 1.15)

# ---------------------------------------------------------------- hypostyle hall
y.bolum('Hipostil salon')
HX = 0.66                     # outer x (perimeter column line)
HY0, HY1 = 0.03, 0.86         # front column line, back wall
NAVE_X = 0.13
AIS_X = (0.32, 0.49, HX)
ROWS = [HY0 + (HY1 - 0.06 - HY0) * k / 4 for k in range(5)]   # 5 rows of columns front to back
ZA = Z0 + 0.32                # aisle column top
ZN = Z0 + 0.48                # nave column top
EP = 0.035                    # architrave depth
SCR = 0.13                    # screen wall height
# nave: the great open-papyrus columns
for yy in ROWS:
    for sx in (-1, 1):
        sutun(y, sx * NAVE_X, yy, Z0, ZN, 0.04, TAS, 'misir', bant_key='turkuaz')
        for xx in AIS_X:
            tomurcuk_sutun(sx * xx, yy, Z0, ZA, 0.026)
# architraves on the aisle rows (along y) and over the front / back
for sx in (-1, 1):
    for xx in AIS_X:
        kutu_merkez(y, (sx * xx, (ROWS[0] + HY1) / 2), 0.046, HY1 - ROWS[0] + 0.04, EP, TAS, z0=ZA)
    kutu_merkez(y, (sx * NAVE_X, (ROWS[0] + HY1) / 2), 0.07, HY1 - ROWS[0] + 0.04, EP, TAS, z0=ZN)
    # painted inscription bands on the outer architrave
    for xx, zz in ((HX, ZA), (NAVE_X, ZN)):
        if xx == NAVE_X: continue
        P = lambda s, t, d=0.003, xx=xx: V(sx * (xx + 0.023), ROWS[0] - 0.02 + s, zz + t) + V(sx, 0, 0) * d
        yazi_bandi(P, V(sx, 0, 0), 0.02, HY1 - ROWS[0], EP * 0.25, EP * 0.5, 'lacivert', 0.002, tohum=11)
# aisle roofs: slabs spanning from the clerestory row to the outer row
ZR = ZA + EP
RT = 0.025
for sx in (-1, 1):
    xa, xb = sorted((sx * (AIS_X[0] - 0.03), sx * (HX + 0.035)))
    kutu(y, V(xa, ROWS[0] - 0.04, ZR), X, xb - xa, HY1 - ROWS[0] + 0.06, RT, TAS)
    y.yuz_yon([V(xa, ROWS[0] - 0.04, ZR - 0.0005), V(xb, ROWS[0] - 0.04, ZR - 0.0005), V(xb, HY1 + 0.02, ZR - 0.0005), V(xa, HY1 + 0.02, ZR - 0.0005)], 'lacivert', -Z)
    # cavetto cornice round the outer edges of the aisle roof
    xo = sx * (HX + 0.035)
    yo0, yo1 = ROWS[0] - 0.04, HY1 + 0.02
    pts = [V(sx * (AIS_X[0] - 0.03), yo0), V(xo, yo0), V(xo, yo1), V(sx * (AIS_X[0] - 0.03), yo1)]
    if sx < 0: pts = [pts[3], pts[2], pts[1], pts[0]]
    silme(y, pts, ZR + RT, 0.035, 0.022, TAS, KAVETTO, kapali=False)
    for i in range(3):   # the cornice's inner face, towards the roof
        duz_duvar(y, pts[i + 1], pts[i], ZR + RT, ZR + RT + 0.035, TAS)
# clerestory: walls on the inner aisle row up to the nave roof, stone-grilled windows
ZC0 = ZR + RT
ZNR = ZN + EP
for sx in (-1, 1):
    xx = sx * (AIS_X[0] + 0.012)
    nseg = len(ROWS) - 1
    for k in range(nseg + 1):
        y0_ = ROWS[0] - 0.04 if k == 0 else (ROWS[k - 1] + ROWS[k]) / 2
        y1_ = HY1 + 0.02 if k == nseg else (ROWS[k] + ROWS[k + 1]) / 2
        a, b = (V(xx, y1_), V(xx, y0_)) if sx < 0 else (V(xx, y0_), V(xx, y1_))
        if k in (0, nseg):
            duz_duvar(y, a, b, ZC0, ZNR, TAS)
            continue
        W_, e_, nc_, L_ = dikdortgen_acik(y, a, b, ZC0, ZNR - ZC0, 0.14, 0.86, 0.02, ZNR - ZC0 - 0.018, (TAS, KOYU, ACIK, 'koyu'), derin=0.02)
        kafes(y, a, b, ZC0, 0.14, 0.86, 0.02, ZNR - ZC0 - 0.018, TAS, nu=6, nv=1, en=0.01, ileri=0.012)
    yi = sx * (AIS_X[0] + 0.012 - 0.026)
    a, b = (V(yi, ROWS[0] - 0.04), V(yi, HY1 + 0.02)) if sx < 0 else (V(yi, HY1 + 0.02), V(yi, ROWS[0] - 0.04))
    duz_duvar(y, a, b, ZC0, ZNR, TAS)
    xo_ = sx * (AIS_X[0] + 0.012)
    for yy_, ny_ in ((ROWS[0] - 0.04, -1), (HY1 + 0.02, 1)):
        y.yuz_yon([V(yi, yy_, ZC0), V(xo_, yy_, ZC0), V(xo_, yy_, ZNR), V(yi, yy_, ZNR)], TAS, V(0, ny_, 0))
    # the inner face of the clerestory wall (seen across the nave roof? no: under it) - its top edge
    kutu_merkez(y, (sx * (AIS_X[0] + 0.012 - 0.012), (ROWS[0] - 0.04 + HY1 + 0.02) / 2), 0.024, HY1 - ROWS[0] + 0.06, 0.001, TAS, z0=ZNR - 0.001, yuzler='ust')
# the nave roof
NX = AIS_X[0] + 0.035
kutu(y, V(-NX, ROWS[0] - 0.05, ZNR), X, 2 * NX, HY1 - ROWS[0] + 0.07, RT, TAS)
silme(y, dikdortgen(-NX, NX, ROWS[0] - 0.05, HY1 + 0.02), ZNR + RT, 0.04, 0.025, TAS, KAVETTO)
# the nave roof lies inside its cornice like a parapet: the cornice's inner faces, then the great slabs
NR = dikdortgen(-NX, NX, ROWS[0] - 0.05, HY1 + 0.02)
for i in range(4):
    duz_duvar(y, NR[(i + 1) % 4], NR[i], ZNR + RT, ZNR + RT + 0.04, TAS)
y.yuz_yon([V(-NX, ROWS[0] - 0.05, ZNR - 0.0005), V(NX, ROWS[0] - 0.05, ZNR - 0.0005), V(NX, HY1 + 0.02, ZNR - 0.0005), V(-NX, HY1 + 0.02, ZNR - 0.0005)], 'lacivert', -Z)
# roof slabs: the great stone beams laid side by side, a little uneven in height and shade (the joints between them
# open to the darker roof below), rain spouts through the cornice
y.bolum('Dam')
def dam_levhalari(x_a, x_b, ya, yb, zz, n, tohum, kes=()):
    """the beams run from architrave to architrave: each row of slabs is cut at the architrave lines kes"""
    L = (yb - ya) / n
    xs = [x_a] + [x for x in sorted(kes) if x_a < x < x_b] + [x_b]
    for k in range(n):
        for m in range(len(xs) - 1):
            r = (k * 7 + m * 3 + tohum) % 5
            h = 0.005 + 0.0015 * (r % 3)
            key = (TAS, ACIK, TAS, TAS, ACIK)[r]
            kutu(y, V(xs[m] + 0.003, ya + k * L + 0.0025, zz), X, xs[m + 1] - xs[m] - 0.006, L - 0.005, h, key, 'onarkasagsolust')
for sx in (-1, 1):
    xa_, xb_ = sorted((sx * (AIS_X[0] + 0.015), sx * (HX + 0.035)))
    dam_levhalari(xa_, xb_, ROWS[0] - 0.04, HY1 + 0.02, ZR + RT, 13, 2 if sx > 0 else 5, (sx * AIS_X[1],))
dam_levhalari(-NX, NX, ROWS[0] - 0.05, HY1 + 0.02, ZNR + RT, 13, 0, (-NAVE_X, NAVE_X))
for sx in (-1, 1):
    for k in range(4):
        yy = (ROWS[k] + ROWS[k + 1]) / 2
        boru(y, [V(sx * (HX + 0.035), yy, ZR + RT + 0.01), V(sx * (HX + 0.075), yy, ZR + RT + 0.004)], 0.007, ACIK, n=6)
# skylight slots and a roof stair kiosk on the nave roof
for yy in (0.25, 0.55):
    kutu_merkez(y, (0, yy), 0.08, 0.06, 0.012, 'koyu', z0=ZNR + RT + 0.001)
kutu_merkez(y, (-0.18, 0.74), 0.09, 0.08, 0.1, TAS, z0=ZNR + RT, yuzler='arkasagsol')
kavetto(dikdortgen(-0.225, -0.135, 0.7, 0.78), ZNR + RT + 0.1, 0.018, 0.01, TAS)
dikdortgen_acik(y, V(-0.225, 0.7), V(-0.135, 0.7), ZNR + RT, 0.1, 0.33, 0.67, 0.01, 0.075, (TAS, KOYU, ACIK, 'koyu'), derin=0.015)
# the nave front: a lintel over the central passage with the winged sun
kanatli_gunes(V(0, ROWS[0] - 0.05, ZNR + RT * 0.5 + 0.004), X, -Y, 0.24, 0.04, d=0.002)

# screen walls between the perimeter columns (front, sides), with a cavetto cornice and painted registers
y.bolum('Perde duvarlar')
def perde(a, b, h=SCR):
    a, b = V(a.x, a.y), V(b.x, b.y)
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    L = (b - a).length
    kutu(y, a - nc * 0.012 + Z * Z0, e, L, 0.024, h, TAS, 'onarkasagsolust')
    silme(y, [a - nc * 0.0, b - nc * 0.0], Z0 + h, 0.028, 0.014, TAS, KAVETTO, kapali=False)
    silme(y, [b - nc * 0.024, a - nc * 0.024], Z0 + h, 0.028, 0.014, TAS, KAVETTO, kapali=False)
    y.yuz_yon([a + Z * (Z0 + h + 0.028), b + Z * (Z0 + h + 0.028), b - nc * 0.024 + Z * (Z0 + h + 0.028), a - nc * 0.024 + Z * (Z0 + h + 0.028)], TAS, Z)
    P = lambda s, t, d=0.003: a + e * s + Z * (Z0 + t) + nc * (0.012 + d)
    yazi_bandi(P, nc, 0.025, L - 0.025, 0.1, 0.018, KOYU, tohum=int(L * 100))
    levha(P, 0.02, L - 0.02, 0.025, 0.03, 'boya_kirmizi', nc, 0.002)
    levha(P, 0.02, L - 0.02, 0.085, 0.09, 'boya_kirmizi', nc, 0.002)
xs = sorted([-HX, -AIS_X[1], -AIS_X[0], -NAVE_X, NAVE_X, AIS_X[0], AIS_X[1], HX])
for i in range(len(xs) - 1):
    if abs(xs[i] + NAVE_X) < 1e-6: continue   # the central passage stays open
    perde(V(xs[i] + 0.028, ROWS[0]), V(xs[i + 1] - 0.028, ROWS[0]))
for sx in (-1, 1):
    for k in range(len(ROWS) - 1):
        a, b = V(sx * HX, ROWS[k] + 0.028), V(sx * HX, ROWS[k + 1] - 0.028)
        if sx < 0: a, b = b, a
        perde(a, b)
    a, b = V(sx * HX, ROWS[-1] + 0.028), V(sx * HX, HY1 - 0.01)
    if sx < 0: a, b = b, a
    perde(a, b)
# the back wall: solid up to the roofs, with a great relief of the king before Amun
y.bolum('Arka duvar')
kutu(y, V(HX + 0.035, HY1 + 0.02, Z0), -X, 2 * (HX + 0.035), 0.03, ZR + RT - Z0, TAS, 'onarkasagsol')
kutu(y, V(NX, HY1 + 0.02, ZR + RT), -X, 2 * NX, 0.03, ZNR - ZR, TAS, 'onarkasagsol')
Pb = lambda s, t, d=0.003: V(HX + 0.035 - s, HY1 + 0.05, Z0 + t) + Y * d
for k, sc in enumerate((0.32, 0.98)):
    levha(Pb, sc - 0.17, sc + 0.17, 0.03, 0.31, ACIK, Y, 0.0015)
    firavun_kabartma(Pb, Y, sc, 0.05, 0.24, yon=1 if k else -1)
    yazi_bandi(Pb, Y, sc - 0.15, sc + 0.15, 0.285, 0.018, 'lacivert', 0.0035, tohum=k)

# ---------------------------------------------------------------- the White Chapel and the sacred lake
y.bolum('Beyaz sapel')
CX, CY = -0.95, 0.4
zemin(y, CX - 0.17, CX + 0.17, CY - 0.2, CY + 0.2, 0.07, 'kirec', 'kirec', basamak=(('on', 0.08), ('arka', 0.08)), n_basamak=4)
zc = 0.07
for i in range(4):
    for j in range(4):
        px, py = CX - 0.12 + i * 0.08, CY - 0.15 + j * 0.1
        kutu_merkez(y, (px, py), 0.034, 0.034, 0.16, 'kirec', z0=zc)
        P = lambda s, t, d=0.003, px=px, py=py: V(px - 0.017 + s, py - 0.017, zc + t) - Y * d
        if j == 0:
            yazi_sutunu(P, -Y, 0.011, 0.02, 0.15, 0.012, KOYU, adim=0.014, tohum=i)
kutu_merkez(y, (CX, CY), 0.3, 0.38, 0.03, 'kirec', z0=zc + 0.16)
kavetto(dikdortgen(CX - 0.15, CX + 0.15, CY - 0.19, CY + 0.19), zc + 0.19, 0.035, 0.02, 'kirec')
kutu_merkez(y, (CX, CY), 0.07, 0.12, 0.07, 'altin', z0=zc)   # the bark stand

y.bolum('Kutsal gol')
havuz(y, LX0, LX1, LY0, LY1, Z0, derin=0.075, kenar=0.022, key=TAS)
merdiven(y, V((LX0 + LX1) / 2, LY0 + 0.1), -math.pi / 2, 0.1, Z0 - 0.03, Z0, n=4, key=TAS)
for (px, py, b) in ((0.92, -0.32, 0.22), (-0.98, -0.25, 0.2), (-1.06, 0.82, 0.2), (-0.88, 0.86, 0.17)):
    agac(y, px, py, Z0, b, 'palmiye')
# a scarab on a column by the lake (Amenhotep III)
kutu_merkez(y, (0.95, 0.93), 0.05, 0.05, 0.04, 'granit', z0=Z0)
kure(y, (0.95, 0.93, Z0 + 0.052), 0.022, 'granit', n=10, kat=4)

# ---------------------------------------------------------------- the forecourt: a bark way-station, priests' houses
y.bolum('On avlu')
# a way-station for the sacred bark: a square kiosk of four papyrus columns with screen walls, on a podium
BX, BY = 0.78, -0.88
zemin(y, BX - 0.14, BX + 0.14, BY - 0.12, BY + 0.12, 0.04, TAS, ACIK, basamak=(('sol', 0.08),), n_basamak=2)
zb = Z0 + 0.04 - 0.05 + 0.0
zb = 0.04
for i in (-1, 1):
    for j in (-1, 1):
        sutun(y, BX + i * 0.09, BY + j * 0.075, zb, zb + 0.2, 0.017, TAS, 'misir', bant_key='boya_kirmizi')
for (a, b) in ((V(BX - 0.073, BY - 0.075), V(BX + 0.073, BY - 0.075)), (V(BX + 0.09, BY - 0.058), V(BX + 0.09, BY + 0.058)),
               (V(BX + 0.073, BY + 0.075), V(BX - 0.073, BY + 0.075))):
    kutu(y, a + Z * zb - V((b - a).normalized().y, -(b - a).normalized().x) * 0.008, (b - a).normalized(), (b - a).length, 0.016, 0.08, TAS, 'onarkasagsolust')
kutu_merkez(y, (BX, BY), 0.22, 0.19, 0.02, TAS, z0=zb + 0.2)
kavetto(dikdortgen(BX - 0.11, BX + 0.11, BY - 0.095, BY + 0.095), zb + 0.22, 0.03, 0.016, TAS)
# the gilded bark of Amun on its stand inside
kutu_merkez(y, (BX, BY), 0.05, 0.03, 0.03, 'granit', z0=zb)
boru(y, [V(BX - 0.06, BY, zb + 0.05), V(BX - 0.02, BY, zb + 0.038), V(BX + 0.02, BY, zb + 0.038), V(BX + 0.06, BY, zb + 0.05)], 0.012, 'altin', n=8)
kutu_merkez(y, (BX, BY), 0.035, 0.022, 0.025, 'altin', z0=zb + 0.045)
kure(y, (BX - 0.062, BY, zb + 0.056), 0.01, 'altin', n=8, kat=4)
kure(y, (BX + 0.062, BY, zb + 0.056), 0.01, 'altin', n=8, kat=4)

# priests' houses: whitewashed mud brick, a roof terrace with a parapet, small windows, a palm and jars
def ev(cx, cy, w, d, h, aci=0.0):
    with parca(y, (cx, cy, Z0), aci):
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            if i == 0:
                dikdortgen_acik(y, a, b, 0, h, 0.4, 0.6, 0.0, h * 0.62, ('siva_krem', 'kerpic_koyu', 'kerpic', 'ahsap'), derin=0.012)
            else:
                dikdortgen_acik(y, a, b, 0, h, 0.42, 0.58, h * 0.6, h * 0.82, ('siva_krem', 'kerpic_koyu', 'kerpic', 'koyu'), derin=0.01)
        parapet(y, k, h, 0.03, 0, 0.012, 'siva_krem')
        y.yuz([V(-w / 2 + 0.012, -d / 2 + 0.012, h + 0.003), V(w / 2 - 0.012, -d / 2 + 0.012, h + 0.003), V(w / 2 - 0.012, d / 2 - 0.012, h + 0.003), V(-w / 2 + 0.012, d / 2 - 0.012, h + 0.003)], 'kerpic')
        # a reed shade on the roof
        for (px, py) in ((-w / 4, 0.0), (-w / 4, d / 4), (0.0, 0.0), (0.0, d / 4)):
            y.prizma((px, py), 0.003, h, h + 0.05, 'ahsap', n=4)
        kutu_merkez(y, (-w / 8, d / 8), w / 4 + 0.012, d / 4 + 0.012, 0.004, 'saz', z0=h + 0.05)
ev(-0.82, -0.95, 0.2, 0.16, 0.1)
ev(-0.56, -1.05, 0.16, 0.14, 0.085)
for (px, py) in ((-0.68, -0.85), (-0.66, -0.88), (-0.7, -0.89)):
    donel(y, (px, py), [(0.006, Z0), (0.011, Z0 + 0.012), (0.01, Z0 + 0.024), (0.005, Z0 + 0.03), (0.006, Z0 + 0.034), (0, Z0 + 0.034)], 'kerpic_koyu', n=8)
for (px, py, b) in ((-1.05, -0.72, 0.19), (0.55, -1.05, 0.16), (1.02, -1.08, 0.2), (1.06, -0.6, 0.17)):
    agac(y, px, py, Z0, b, 'palmiye')

calistir(y, 'lm_karnak')
