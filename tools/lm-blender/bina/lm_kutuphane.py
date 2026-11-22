# İskenderiye Kütüphanesi (lm_kutuphane): the Mouseion and Great Library of Ptolemaic Alexandria as a Greek-Egyptian
# precinct: an Egyptian pylon gate, a peristyle court of papyrus-capital columns under a Greek entablature and tiled
# stoa roofs with scroll shelves on their back walls, a garden with a pool and Eratosthenes' armillary sphere, two
# exedrae for readers, the great hall (pedimented portico, painted frieze, octagonal drum and copper dome) and two
# book-stack wings with open loggias full of papyrus rolls.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05
DUV = 'kirec'          # walls
SUT = 'mermer'         # columns, mouldings
KAVETTO = [(0, 0), (0.16, 0.03), (0.2, 0.1), (0.12, 0.17), (0.04, 0.19), (0.07, 0.36), (0.18, 0.56), (0.4, 0.75),
           (0.72, 0.88), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]


# ---------------------------------------------------------------- helpers
def levha(P, s0, s1, t0, t1, key, n, d=0.003):
    y.yuz_yon([P(s0, t0, d), P(s1, t0, d), P(s1, t1, d), P(s0, t1, d)], key, n)


def plaka(pts, key, yon, kalin=0.003):
    """a thin closed plate: the face pts toward yon, its back kalin behind, the rims round it"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    arka = [p - yon * kalin for p in pts]
    y.yuz_yon(pts, key, yon); y.yuz_yon(arka, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        y.yuz_yon([pts[i], pts[j], arka[j], arka[i]], key, (pts[i] + pts[j]) / 2 - c)


def kavetto(kose, z, h, c, key=DUV, ust=True):
    silme(y, kose, z, h, c, key, KAVETTO)
    if ust:
        y.yuz_yon([V(p.x, p.y, z + h) for p in kose], key, Z)


def egik_blok(x0, x1, y0, y1, z0, h, ix, iy, key=DUV):
    B = dikdortgen(x0, x1, y0, y1, z0); T = dikdortgen(x0 + ix, x1 - ix, y0 + iy, y1 - iy, z0 + h)
    for i in range(4):
        j = (i + 1) % 4
        e = B[j] - B[i]; n = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], key, n + Z * 0.2)
    return B, T


def yazi_bandi(P, n, s0, s1, t0, h, key='kum_koyu', d=0.003, tohum=0):
    w = h * 0.7; s = s0; k = 0
    while s + w < s1:
        r = (tohum * 5 + k * 7) % 4
        if r == 0: levha(P, s, s + w, t0, t0 + h, key, n, d)
        elif r == 1: levha(P, s, s + w, t0 + h * 0.3, t0 + h * 0.6, key, n, d)
        elif r == 2: y.yuz_yon([P(s, t0, d), P(s + w, t0, d), P(s + w * 0.5, t0 + h, d)], key, n)
        else: levha(P, s + w * 0.3, s + w * 0.7, t0, t0 + h, key, n, d)
        s += w * 1.5; k += 1


PYK = 'kum'            # the pylon's sandstone


def firavun_kabartma(P, n, sc, t0, H, yon=1, d=0.0035):
    """a painted relief of the pharaoh smiting his enemies, centre s = sc, feet at t0, H tall; yon: +1 faces +s"""
    def Q(s0, s1, a0, a1, key, dd=d):
        s0, s1 = sc + yon * s0 * H, sc + yon * s1 * H
        if s0 > s1: s0, s1 = s1, s0
        levha(P, s0, s1, t0 + a0 * H, t0 + a1 * H, key, n, dd)
    ten = 'kirmizi'
    Q(-0.13, -0.06, 0.0, 0.36, ten); Q(0.05, 0.12, 0.0, 0.36, ten)
    Q(-0.16, -0.05, 0.0, 0.03, ten); Q(0.05, 0.16, 0.0, 0.03, ten)
    y.yuz_yon([P(sc + yon * -0.15 * H, t0 + 0.34 * H, d + 0.0005), P(sc + yon * 0.14 * H, t0 + 0.34 * H, d + 0.0005),
               P(sc + yon * 0.09 * H, t0 + 0.52 * H, d + 0.0005), P(sc + yon * -0.1 * H, t0 + 0.52 * H, d + 0.0005)], 'beyaz', n)
    Q(-0.025, 0.025, 0.36, 0.5, 'altin', d + 0.001)
    Q(-0.09, 0.08, 0.5, 0.78, ten)
    Q(-0.1, 0.09, 0.72, 0.79, 'turkuaz', d + 0.0005)
    Q(-0.05, 0.05, 0.79, 0.88, ten)
    Q(-0.055, 0.05, 0.86, 1.02, 'beyaz', d + 0.0005)
    Q(0.05, 0.075, 0.84, 0.87, 'altin', d + 0.0005)
    Q(-0.2, -0.08, 0.74, 0.79, ten)
    Q(-0.22, -0.17, 0.79, 0.98, ten)
    Q(-0.235, -0.155, 0.98, 1.04, 'altin')
    Q(0.07, 0.27, 0.6, 0.65, ten)
    Q(0.255, 0.275, 0.0, 0.92, 'altin', d + 0.001)
    Q(0.24, 0.29, 0.92, 0.95, 'altin', d + 0.001)
    Q(0.1, 0.2, 0.84, 1.0, 'beyaz', d + 0.0005)
    Q(0.12, 0.18, 0.87, 0.97, 'lacivert', d + 0.001)
    # the kneeling enemies
    for k in range(3):
        Q(0.3 + k * 0.08, 0.36 + k * 0.08, 0.0, 0.22 - k * 0.02, 'kum_koyu' if k % 2 else 'koyu')
        Q(0.31 + k * 0.08, 0.35 + k * 0.08, 0.22 - k * 0.02, 0.3 - k * 0.02, 'kum_koyu' if k % 2 else 'koyu')


def kanatli_gunes(o, ex, n, en, h, d=0.004):
    o, ex, n = V(*o), V(*ex), V(*n).normalized()
    P = lambda s, t, dd=d: o + ex * s + Z * t + n * dd
    r = h * 0.5
    y.yuz_yon([P(r * math.cos(TAU * i / 14), r * math.sin(TAU * i / 14), d + 0.001) for i in range(14)], 'altin', n)
    for s in (-1, 1):
        for k, key in enumerate(('lacivert', 'turkuaz', 'boya_kirmizi')):
            a0 = -h * 0.42 + k * h * 0.26
            y.yuz_yon([P(s * r * 0.9, a0), P(s * en / 2, a0 + h * 0.12 + k * 0.004), P(s * en / 2, a0 + h * 0.3 + k * 0.004), P(s * r * 0.9, a0 + h * 0.26)], key, n)


def flama(x, yy, z, key, en=0.16, yuk=0.035, aci=0.0, dalga=0.014, n=7):
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


def halka(cx, cy, z, hw, hd, n=12, p=2.4):
    out = []
    for i in range(n):
        a = TAU * i / n
        c, s = math.cos(a), math.sin(a)
        out.append(V(cx + hw * math.copysign(abs(c) ** (2 / p), c), cy + hd * math.copysign(abs(s) ** (2 / p), s), z))
    return out


def hafif_sutun(cx, cy, z0, z1, r, key, bant):
    """a light papyrus-bundle column (for long colonnades): disc base, eight-lobed shaft, a tie band, an open
    capital painted in alternate strips, an abacus"""
    H = z1 - z0; c = (cx, cy); zb = z1 - H * 0.2
    donel(y, c, [(0, z0), (r * 1.35, z0), (r * 1.35, z0 + H * 0.035), (r * 0.95, z0 + H * 0.05), (0, z0 + H * 0.05)], key, n=8)
    prev = None
    for t in (0.0, 0.15, 1.0):
        rr = r * (0.9 + 0.1 * min(1, t / 0.15)) * (1 - 0.08 * t)
        ring = [V(cx + rr * (1 if i % 2 == 0 else 0.86) * math.cos(TAU * i / 16), cy + rr * (1 if i % 2 == 0 else 0.86) * math.sin(TAU * i / 16), z0 + H * 0.05 + (zb - z0 - H * 0.05) * t) for i in range(16)]
        if prev: y.serit(prev, ring, key)
        prev = ring
    for i in range(16):   # (the shaft's top: the lobes stand out past the capital's foot)
        y.yuz_yon([V(cx, cy, prev[i].z), prev[i], prev[(i + 1) % 16]], key, Z)
    halka_kornis(y, c, r * 0.9, zb - H * 0.05, H * 0.03, r * 0.15, 8, bant)
    donel(y, c, [(r * 0.82, zb), (r * 1.2, zb + H * 0.1), (r * 1.55, zb + H * 0.17), (r * 1.6, zb + H * 0.18), (0, zb + H * 0.18)], key, n=8, dilim=[key, bant])
    kutu_merkez(y, c, r * 1.7, r * 1.7, z1 - zb - H * 0.18, key, z0=zb + H * 0.18)


def heykel(px, py, pz, H, tur='kral', aci=0.0, K='granit_kizil'):
    """a standing statue (1 = its height) facing -y, turned by aci: 'kral' (Ptolemy as pharaoh: kilt, nemes, double
    crown), 'bilgin' (a scholar in a himation holding a scroll), 'kralice' (Arsinoe: sheath dress, vulture crown)"""
    with parca(y, (px, py, pz), aci, H):
        kutu_merkez(y, (0, -0.02), 0.26, 0.3, 0.06, SUT)
        kornis(y, -0.13, 0.13, -0.17, 0.13, 0.06, 0.012, 0.012, SUT, 'tac')
        y.yuz_yon([V(p.x, p.y, 0.072) for p in dikdortgen(-0.13, 0.13, -0.17, 0.13)], SUT, Z)
        z0 = 0.072
        if tur == 'kral':
            kutu_merkez(y, (0, 0.04), 0.16, 0.05, 0.62, K, z0=z0)
            for sg, yf in ((-1, -0.1), (1, 0.0)):
                kutu_merkez(y, (sg * 0.04, yf - 0.02), 0.045, 0.1, 0.028, K, z0=z0)
                boru(y, [V(sg * 0.04, yf, z0 + 0.03), V(sg * 0.04, yf * 0.55, z0 + 0.24), V(sg * 0.045, -0.01, z0 + 0.42)], 0.026, K, n=6, r_son=0.038)
            donel(y, (0, -0.01), [(0, z0 + 0.33), (0.07, z0 + 0.33), (0.082, z0 + 0.35), (0.075, z0 + 0.46), (0, z0 + 0.46)], K, n=10)
            hs = [halka(0, -0.01, z0 + z, hw, hd) for z, hw, hd in ((0.45, 0.068, 0.048), (0.56, 0.09, 0.052), (0.66, 0.115, 0.052), (0.69, 0.085, 0.042), (0.71, 0.035, 0.03))]
            for k in range(len(hs) - 1):
                y.serit(hs[k], hs[k + 1], K)
            y.yuz_yon(hs[-1], K, Z)
            for sg in (-1, 1):
                boru(y, [V(sg * 0.112, -0.01, z0 + 0.65), V(sg * 0.12, -0.015, z0 + 0.54), V(sg * 0.11, -0.02, z0 + 0.42)], 0.024, K, n=6, r_son=0.02)
                kutu_merkez(y, (sg * 0.055, -0.04), 0.024, 0.03, 0.09, K, z0=z0 + 0.6)
            donel(y, (0, -0.02), [(0, z0 + 0.71), (0.04, z0 + 0.715), (0.05, z0 + 0.75), (0.046, z0 + 0.79), (0, z0 + 0.81)], K, n=8)
            donel(y, (0, -0.02), [(0, z0 + 0.77), (0.052, z0 + 0.77), (0.054, z0 + 0.83), (0.04, z0 + 0.835), (0, z0 + 0.835)], K, n=10)
            donel(y, (0, -0.02), [(0.04, z0 + 0.83), (0.04, z0 + 0.88), (0.028, z0 + 0.915), (0, z0 + 0.925)], K, n=10)
        elif tur == 'kralice':
            kutu_merkez(y, (0, 0.04), 0.16, 0.05, 0.62, K, z0=z0)
            donel(y, (0, -0.01), [(0, z0), (0.07, z0), (0.074, z0 + 0.2), (0.082, z0 + 0.42), (0.078, z0 + 0.55), (0.1, z0 + 0.66), (0.04, z0 + 0.7), (0, z0 + 0.705)], K, n=10)
            donel(y, (0, -0.005), [(0, z0 + 0.65), (0.06, z0 + 0.66), (0.062, z0 + 0.74), (0.05, z0 + 0.8), (0, z0 + 0.81)], K, n=10)
            donel(y, (0, -0.005), [(0.045, z0 + 0.8), (0.05, z0 + 0.85), (0, z0 + 0.86)], K, n=10)
            for sg in (-1, 1):
                boru(y, [V(sg * 0.09, -0.01, z0 + 0.65), V(sg * 0.1, -0.02, z0 + 0.52), V(sg * 0.07, -0.06, z0 + 0.46 if sg < 0 else z0 + 0.56)], 0.022, K, n=6)
        else:   # bilgin: a draped Greek scholar
            donel(y, (0, 0), [(0, z0), (0.075, z0), (0.08, z0 + 0.3), (0.085, z0 + 0.5), (0.11, z0 + 0.66), (0.05, z0 + 0.71), (0, z0 + 0.715)], K, n=10)
            boru(y, [V(-0.1, 0.0, z0 + 0.62), V(0.03, -0.06, z0 + 0.42), V(0.08, -0.04, z0 + 0.2)], 0.03, K, n=6)   # the himation's fold
            boru(y, [V(0.1, -0.01, z0 + 0.64), V(0.11, -0.05, z0 + 0.5), V(0.05, -0.09, z0 + 0.46)], 0.024, K, n=6)
            boru(y, [V(0.02, -0.1, z0 + 0.43), V(0.09, -0.1, z0 + 0.48)], 0.014, 'kumas', n=6)   # the scroll
            kure(y, (0, -0.01, z0 + 0.78), 0.06, K, n=10, kat=5)
            kure(y, (0, -0.035, z0 + 0.745), 0.045, K, n=8, kat=4)   # the beard


# ---------------------------------------------------------------- layout
GX0, GX1, GY0, GY1 = -1.12, 1.12, -1.12, 1.1
SX = 0.8                  # stoa outer walls x = +-SX
SY0, SY1 = -0.86, 0.16    # stoa front wall, the back ends
SD = 0.15                 # stoa depth (to the column line)
ZC = Z0 + 0.19            # stoa column tops
HX0, HX1, HY0, HY1 = -0.5, 0.5, 0.16, 1.02   # hall podium
ZH = Z0 + 0.08
ZE = ZH + 0.4             # hall entablature top

# ---------------------------------------------------------------- platform
y.bolum('Zemin')
zemin(y, GX0, GX1, GY0, GY1, Z0, DUV, 'zemin', basamak=(('on', 0.56),), n_basamak=3)

# ---------------------------------------------------------------- pylon gate
y.bolum('Pilon')
PY0, PY1, PHt = -1.0, -0.84, 0.42
for sx in (-1, 1):
    x0, x1 = (0.07, 0.4) if sx > 0 else (-0.4, -0.07)
    B, T = egik_blok(x0, x1, PY0, PY1, Z0, PHt, 0.03, 0.02, PYK)
    y.yuz_yon(T, PYK, Z)
    for i in range(4):
        boru(y, [B[i], T[i]], 0.009, 'kum_acik', n=6)
    silme(y, T, Z0 + PHt - 0.012, 0.012, 0.005, 'kum_acik', 'yarim')
    kavetto(T, Z0 + PHt, 0.05, 0.035, PYK)
    # relief: Ptolemy as pharaoh smiting the enemies of Egypt before the gods, text bands; two flagpole niches
    nf = V(0, -1, 0.02 / PHt).normalized()
    P = lambda s, t, d=0.003, x0=x0: V(x0 + s, PY0 + 0.02 * t / PHt, Z0 + t) + nf * d
    W0 = x1 - x0
    firavun_kabartma(P, nf, W0 / 2, 0.09, 0.24, yon=-sx)
    yazi_bandi(P, nf, 0.07, W0 - 0.07, 0.355, 0.016, 'kum_koyu', 0.0035, tohum=sx + 2)
    yazi_bandi(P, nf, 0.07, W0 - 0.07, 0.06, 0.014, 'lacivert', 0.0035, tohum=sx + 5)
    for k, u in enumerate((0.04, W0 - 0.04)):
        xx = x0 + u
        yy = PY0 + 0.002 - 0.012
        y.silindir((xx, yy), 0.006, Z0, Z0 + PHt + 0.22, 'ahsap', n=6)
        y.koni((xx, yy), 0.008, Z0 + PHt + 0.22, 0.025, 'altin', n=6)
        for t in (0.4, 0.7):
            cubuk(y, V(xx, yy, Z0 + PHt * t), V(xx, yy + 0.016, Z0 + PHt * t), 0.008, 'ahsap_koyu')
        if sx < 0 and k == 1:
            sancak(y, xx, yy, Z0 + PHt - 0.02, boy=0.24, en=0.14, yuk=0.08, aci=-0.4)
        else:
            flama(xx, yy, Z0 + PHt + 0.2, ['boya_kirmizi', 'beyaz', 'boya_sari', 'boya_yesil'][(k + (sx > 0) * 2) % 4], 0.16, 0.034, -0.3)
# the gate between the towers
kutu(y, V(-0.07, -0.985, Z0), X, 0.14, 0.13, 0.3, PYK, 'arkasagsolust')
# (the towers batter away from the gate's upright sides: fill the wedge slits, the court showed through them)
for sx in (-1, 1):
    kutu(y, V(0.07 if sx > 0 else -0.1, -0.982, Z0), X, 0.03, 0.127, 0.3, PYK, 'onust')
dikdortgen_acik(y, V(-0.07, -0.985), V(0.07, -0.985), Z0, 0.3, 0.25, 0.75, 0.0, 0.2, (PYK, PYK, 'kum_acik', 'ahsap'), derin=0.03, cerceve=(0.01, 'kum_acik'))
kanatli_gunes(V(0, -0.985, Z0 + 0.255), X, -Y, 0.12, 0.03)
kavetto(dikdortgen(-0.07, 0.07, -0.985, -0.855), Z0 + 0.3, 0.04, 0.025, PYK)
for k in range(4):
    kutu_merkez(y, (0, -0.985 + 0.03 - 0.0015), 0.07, 0.003, 0.005, 'bronz', z0=Z0 + 0.03 + k * 0.045)
# a pair of obelisks before the towers
for sx in (-1, 1):
    dikilitas(y, (sx * 0.47, -1.05), 0.042, 0.44, 'granit_kizil', 'altin', z0=Z0, kaide=True, yazi_key='granit_kizil_koyu')
# sphinxes flanking the steps (Ptolemaic, with the king's face)
for sx in (-1, 1):
    with parca(y, (sx * 0.17, -1.06, Z0), -math.pi / 2, 1.0):
        kutu_merkez(y, (0, 0), 0.13, 0.05, 0.025, SUT)
        z = 0.025
        boru(y, [V(-0.05, 0, z + 0.014), V(-0.02, 0, z + 0.017), V(0.015, 0, z + 0.022)], 0.014, 'granit', n=8, r_son=0.016)
        for s2 in (-1, 1):
            cubuk(y, V(0.018, s2 * 0.01, z + 0.005), V(0.055, s2 * 0.01, z + 0.004), 0.009, 'granit', 0.008)
        donel(y, (0.025, 0), [(0.018, z + 0.006), (0.02, z + 0.028), (0.016, z + 0.042), (0, z + 0.046)], 'granit', n=8)
        kure(y, (0.03, 0, z + 0.05), 0.012, 'granit', n=8, kat=4)
        for s2 in (-1, 1):
            kutu_merkez(y, (0.032, s2 * 0.012), 0.008, 0.006, 0.022, 'granit', z0=z + 0.028)

# ---------------------------------------------------------------- the peristyle court: stoas round three sides
y.bolum('Revakli avlu')
yol = [V(-SX, SY1), V(-SX, SY0), V(SX, SY0), V(SX, SY1)]          # outer wall line (outside on its right)
ic = disa(yol, -SD, kapali=False)                                 # the column line
ZR_O, ZR_I = Z0 + 0.3, Z0 + 0.245                                  # roof: high at the wall, low over the columns
# outer walls (the front only beside the pylon) with high windows between pilasters, a crowning cornice
parcalar_ = [(yol[0], yol[1]), (yol[1], V(-0.4, SY0)), (V(0.4, SY0), yol[2]), (yol[2], yol[3])]
for a, b in parcalar_:
    L = (b - a).length
    n_ = max(1, round(L / 0.15))
    for k in range(n_):
        pa, pb = a.lerp(b, k / n_), a.lerp(b, (k + 1) / n_)
        dikdortgen_acik(y, pa, pb, Z0, ZR_O - Z0 - 0.009, 0.36, 0.64, 0.15, 0.22, (DUV, DUV, SUT, 'koyu'), derin=0.015, cerceve=(0.006, SUT))
        if k:
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            kutu_merkez(y, (pa.x + nn.x * 0.001, pa.y + nn.y * 0.001), 0.022, 0.016, ZR_O - Z0 - 0.03, SUT, z0=Z0, aci=math.atan2(e.y, e.x))
silme(y, [V(p.x, p.y) for p in yol], Z0, 0.016, 0.008, DUV, 'kaide', kapali=False)
silme(y, [V(p.x, p.y) for p in yol], ZR_O - 0.03, 0.022, 0.016, SUT, 'tac', kapali=False)
# the end walls of the side stoas (towards the hall)
for sx in (-1, 1):
    xo, xi = sx * SX, sx * (SX - SD - 0.02)
    y.yuz_yon([V(xo, SY1, Z0), V(xi, SY1, Z0), V(xi, SY1, ZR_I), V(xo, SY1, ZR_O)], DUV, Y)
    y.yuz_yon([V(xo, SY1 - 0.02, Z0), V(xi, SY1 - 0.02, Z0), V(xi, SY1 - 0.02, ZR_I - 0.008), V(xo, SY1 - 0.02, ZR_O - 0.008)], DUV, -Y)
    y.yuz_yon([V(xi, SY1, Z0), V(xi, SY1 - 0.02, Z0), V(xi, SY1 - 0.02, ZR_I - 0.008), V(xi, SY1, ZR_I - 0.008)], DUV, V(-sx, 0))
# the inner face of the outer walls (behind the columns) with scroll shelves in every bay
icd = disa(yol, -0.02, kapali=False)
for k in range(len(icd) - 1):
    a, b = icd[k + 1], icd[k]
    duz_duvar(y, a, b, Z0, ZR_O - 0.017, DUV)


def raf(a, b, z0, h, nu=4, nv=4, tohum=0):
    """a set of pigeonhole shelves full of papyrus rolls on the wall a->b (faces its right)"""
    a, b = V(a.x, a.y), V(b.x, b.y)
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v, d: a + e * u + Z * (z0 + v) + nc * d
    plaka([L(0, 0, 0.012), L(W, 0, 0.012), L(W, h, 0.012), L(0, h, 0.012)], 'ahsap_koyu', nc, 0.011)
    for i in range(nu + 1):
        u = W * i / nu
        y.yuz_yon([L(max(0, u - 0.002), 0, 0.0135), L(min(W, u + 0.002), 0, 0.0135), L(min(W, u + 0.002), h, 0.0135), L(max(0, u - 0.002), h, 0.0135)], 'ahsap', nc)
    for j in range(nv + 1):
        v = h * j / nv
        y.yuz_yon([L(0, max(0, v - 0.002), 0.0137), L(W, max(0, v - 0.002), 0.0137), L(W, min(h, v + 0.002), 0.0137), L(0, min(h, v + 0.002), 0.0137)], 'ahsap', nc)
    for i in range(nu):
        for j in range(nv):
            n_r = 2 + (tohum + i * 3 + j * 5) % 3
            for m in range(n_r):
                u = W * (i + (m + 0.5) / n_r) / nu
                v = h * (j + 0.35 + 0.15 * ((m + i) % 2)) / nv
                rr = min(W / nu / n_r * 0.4, h / nv * 0.3)
                pts = [L(u + rr * math.cos(TAU * q / 6), v + rr * math.sin(TAU * q / 6), 0.0132) for q in range(6)]
                y.yuz_yon(pts, 'kumas' if (m + j) % 3 else 'kum_acik', nc)


for k in range(len(icd) - 1):
    a, b = icd[k + 1], icd[k]
    L_ = (b - a).length
    n_ = max(1, round(L_ / 0.1))
    for m in range(n_):
        pa, pb = a.lerp(b, (m + 0.12) / n_), a.lerp(b, (m + 0.88) / n_)
        if k == 1 and abs((pa.x + pb.x) / 2) < 0.12: continue      # the passage from the gate
        raf(pa, pb, Z0 + 0.02, 0.15, 3, 4, tohum=m + k * 7)
# the colonnades: papyrus-bundle columns with painted capitals, an architrave with a painted frieze
cols = []
for k in range(len(ic) - 1):
    a, b = ic[k], ic[k + 1]
    L_ = (b - a).length
    n_ = max(1, round(L_ / 0.1))
    for m in range(n_ + (1 if k == len(ic) - 2 else 0)):
        if k == len(ic) - 2 and m == n_:
            p = a.lerp(b, 0.97)
        elif k == 0 and m == 0:
            p = a.lerp(b, 0.03)
        else:
            p = a.lerp(b, m / n_)
        cols.append(p)
for p in cols:
    hafif_sutun(p.x, p.y, Z0, ZC, 0.014, SUT, 'boya_yesil')
icx = disa(yol, -SD + 0.018, kapali=False)
icy = disa(yol, -SD - 0.018, kapali=False)
for k in range(len(icx) - 1):
    # the architrave as a beam (outer face, inner face, soffit) and the frieze band
    a0, a1, b0, b1 = icx[k], icx[k + 1], icy[k], icy[k + 1]
    duz_duvar(y, a0, a1, ZC, ZC + 0.028, SUT)
    duz_duvar(y, b1, b0, ZC, ZC + 0.028, SUT)
    e = (a1 - a0).normalized(); nn = V(-e.y, e.x)
    L_ = (a1 - a0).length
    Pf = lambda s_, t_, d=0.002, b0=b0, e=e, nn=nn: V(b0.x, b0.y) + e * s_ + Z * (ZC + t_) + nn * d
    Lb = (b1 - b0).length
    levha(Pf, 0.0, Lb, 0.014, 0.024, 'lacivert', nn, 0.0015)
    for m in range(int(Lb / 0.05)):
        s_ = 0.025 + m * 0.05
        y.yuz_yon([Pf(s_ + 0.006 * math.cos(TAU * q / 6), 0.019 + 0.004 * math.sin(TAU * q / 6), 0.0025) for q in range(6)], 'altin', nn)
silme(y, [V(p.x, p.y) for p in reversed(icy)], ZC + 0.028, 0.014, 0.01, SUT, 'tac', kapali=False)
# stoa roof: tiled, sloping down to the court
ro = disa(yol, 0.02, kapali=False)
ri = disa(yol, -SD - 0.035, kapali=False)
for k in range(len(ro) - 1):
    nseg = 8 if k == 1 else 6
    for m in range(nseg):
        t0, t1 = m / nseg, (m + 1) / nseg
        q = [ro[k].lerp(ro[k + 1], t0) + Z * ZR_O, ro[k].lerp(ro[k + 1], t1) + Z * ZR_O, ri[k].lerp(ri[k + 1], t1) + Z * ZR_I, ri[k].lerp(ri[k + 1], t0) + Z * ZR_I]
        y.yuz_yon(q, 'kiremit', Z)
    iki_yuzlu(y, [ri[k + 1] + Z * ZR_I, ri[k] + Z * ZR_I, ri[k] + Z * (ZR_I - 0.01), ri[k + 1] + Z * (ZR_I - 0.01)], 'kiremit2', V(*(ri[k] - ro[k]).xy, 0))
    iki_yuzlu(y, [ro[k] + Z * ZR_O, ro[k + 1] + Z * ZR_O, ro[k + 1] + Z * (ZR_O - 0.01), ro[k] + Z * (ZR_O - 0.01)], 'kiremit2', V(*(ro[k] - ri[k]).xy, 0))
    # the soffit of the overhang over the court (seen past the eave)
    y.yuz_yon([ri[k] + Z * (ZR_I - 0.01), ri[k + 1] + Z * (ZR_I - 0.01), icy[k + 1] + Z * (ZC + 0.042), icy[k] + Z * (ZC + 0.042)], 'ahsap_koyu', -Z)
for uc in (0, -1):
    # the roof's open ends at the back
    p, q = ro[uc], ri[uc]
    y.yuz_yon([p + Z * ZR_O, q + Z * ZR_I, q + Z * (ZR_I - 0.01), p + Z * (ZR_O - 0.01)], 'kiremit2', Y)
# ridge tiles along the wall top
for k in range(len(ro) - 1):
    cubuk(y, ro[k] - (ro[k] - ri[k]).normalized() * 0.015 + Z * (ZR_O - 0.001), ro[k + 1] - (ro[k + 1] - ri[k + 1]).normalized() * 0.015 + Z * (ZR_O - 0.001), 0.012, 'kiremit2')

# ---------------------------------------------------------------- the garden court
y.bolum('Bahce')
GA = (-SX + SD + 0.03, SX - SD - 0.03, SY0 + SD + 0.03, SY1 - 0.08)   # inside the colonnades
gx0, gx1, gy0, gy1 = GA
PW = 0.06
YC = -0.32
# raised beds of turf with stone kerbs, paths between them
yataklar = [(gx0, -PW, gy0, YC - PW), (PW, gx1, gy0, YC - PW)]
for (x0, x1, y0, y1) in yataklar:
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, Z0, Z0 + 0.014, SUT)
    y.yuz_yon([V(p.x, p.y, Z0 + 0.014) for p in disa(k, -0.008)], 'cimen', Z)
    for i in range(4):
        j = (i + 1) % 4
        q = disa(k, -0.008)
        y.yuz_yon([k[i] + Z * (Z0 + 0.014), k[j] + Z * (Z0 + 0.014), q[j] + Z * (Z0 + 0.014), q[i] + Z * (Z0 + 0.014)], SUT, Z)
for (px, py, b, tur) in ((-0.48, -0.6, 0.2, 'palmiye'), (-0.3, -0.52, 0.14, 'servi'), (-0.14, -0.62, 0.12, 'yapraklı'), (0.14, -0.6, 0.12, 'yapraklı'),
                         (0.3, -0.52, 0.14, 'servi'), (0.48, -0.6, 0.2, 'palmiye'), (-0.5, -0.44, 0.13, 'servi'), (0.5, -0.44, 0.13, 'servi')):
    agac(y, px, py, Z0 + 0.014, b, tur)
# statues of scholars along the cross path
for (px, py, a_) in ((-0.36, YC + 0.02, 0.0), (0.36, YC + 0.02, 0.0), (-0.2, -0.12, 0.3), (0.2, -0.12, -0.3)):
    heykel(px, py, Z0, 0.13, 'bilgin', a_, 'mermer')
# the pool with the armillary sphere of Eratosthenes
y.bolum('Gok kuresi')
kc = cokgen((0, YC), 0.1, 8, kat=math.pi / 8)
duvarlar(y, disa(kc, 0.02), Z0, Z0 + 0.025, SUT)
duvarlar(y, list(reversed(kc)), Z0 + 0.008, Z0 + 0.025, SUT)
for i in range(8):
    j = (i + 1) % 8
    o = disa(kc, 0.02)
    y.yuz_yon([o[i] + Z * (Z0 + 0.025), o[j] + Z * (Z0 + 0.025), kc[j] + Z * (Z0 + 0.025), kc[i] + Z * (Z0 + 0.025)], SUT, Z)
y.yuz_yon([V(p.x, p.y, Z0 + 0.008) for p in kc], 'su', Z)
sutun(y, 0, YC, Z0 + 0.008, Z0 + 0.12, 0.012, SUT, 'iyon')
AC = V(0, YC, Z0 + 0.19)
AR = 0.06
def cember(n, eks, r, key, kalin=0.0035):
    """a ring of radius r round AC in the plane with normal eks"""
    eks = eks.normalized()
    u = eks.cross(Z if abs(eks.z) < 0.9 else X).normalized(); w = eks.cross(u)
    pts = [AC + (u * math.cos(TAU * i / n) + w * math.sin(TAU * i / n)) * r for i in range(n + 1)]
    boru(y, pts, kalin, key, n=5, kapat=False)
cember(24, Z, AR, 'bronz')                                    # the equator
cember(24, X, AR, 'bronz')                                    # the meridian
cember(24, Y, AR * 0.97, 'bronz')                             # the colure
cember(24, V(0, math.sin(0.41), math.cos(0.41)), AR * 0.92, 'altin', 0.0045)   # the ecliptic band
kure(y, AC, 0.018, 'boya_yesil', n=10, kat=5)                  # the earth
boru(y, [AC - V(0, math.sin(0.5), math.cos(0.5)) * 0.08, AC + V(0, math.sin(0.5), math.cos(0.5)) * 0.08], 0.003, 'bronz', n=5)
for sg in (-1, 1):   # the stand's arc holding it
    boru(y, [V(sg * AR * 1.08, YC, Z0 + 0.12), V(sg * AR * 1.12, YC, AC.z), V(sg * AR * 0.9, YC, AC.z + 0.04)], 0.004, 'bronz', n=5)
cubuk(y, V(-AR * 1.08, YC, Z0 + 0.12), V(AR * 1.08, YC, Z0 + 0.12), 0.008, 'bronz')

# ---------------------------------------------------------------- exedrae for readers
y.bolum('Eksedralar')


def eksedra(cx, cy, r, h, dh):
    """a semicircular exedra opening towards -y: a curved wall with a stone bench inside, a half dome painted blue
    with gold stars inside, a statue of a muse in the middle"""
    t = 0.02
    n = 12
    A = [math.pi * k / n for k in range(n + 1)]                     # 0 .. pi (round the back, +y side)
    dis_ = [V(cx + (r + t) * math.cos(a), cy + (r + t) * math.sin(a)) for a in A]
    ic_ = [V(cx + r * math.cos(a), cy + r * math.sin(a)) for a in A]
    for k in range(n):
        y.yuz_yon([dis_[k] + Z * Z0, dis_[k + 1] + Z * Z0, dis_[k + 1] + Z * (Z0 + h), dis_[k] + Z * (Z0 + h)], DUV, (dis_[k] + dis_[k + 1]) / 2 - V(cx, cy))
        y.yuz_yon([ic_[k] + Z * Z0, ic_[k + 1] + Z * Z0, ic_[k + 1] + Z * (Z0 + h), ic_[k] + Z * (Z0 + h)], 'siva_krem', V(cx, cy) - (ic_[k] + ic_[k + 1]) / 2)
    for uc in (0, n):
        y.yuz_yon([dis_[uc] + Z * Z0, ic_[uc] + Z * Z0, ic_[uc] + Z * (Z0 + h), dis_[uc] + Z * (Z0 + h)], DUV, -Y)
    # the half dome: outer copper-coloured stone, inner blue with stars; its rim facing the court
    K = 5
    def nokta(rr, a, ph):
        return V(cx + rr * math.cos(ph) * math.cos(a), cy + rr * math.cos(ph) * math.sin(a), Z0 + h + dh * (rr / r) * math.sin(ph))
    for j in range(K):
        p0, p1 = math.pi / 2 * j / K, math.pi / 2 * (j + 1) / K
        for k in range(n):
            a0, a1 = A[k], A[k + 1]
            y.yuz_yon([nokta(r + t, a0, p0), nokta(r + t, a1, p0), nokta(r + t, a1, p1), nokta(r + t, a0, p1)], 'kiremit', nokta(r + t, (a0 + a1) / 2, (p0 + p1) / 2) - V(cx, cy, Z0 + h))
            y.yuz_yon([nokta(r, a0, p0), nokta(r, a1, p0), nokta(r, a1, p1), nokta(r, a0, p1)], 'lacivert', V(cx, cy, Z0 + h) - nokta(r, (a0 + a1) / 2, (p0 + p1) / 2))
        for uc in (0, n):
            y.yuz_yon([nokta(r, A[uc], p0), nokta(r + t, A[uc], p0), nokta(r + t, A[uc], p1), nokta(r, A[uc], p1)], SUT, -Y)
    for k in range(n):   # the top ring of the wall under the dome
        y.yuz_yon([dis_[k] + Z * (Z0 + h), dis_[k + 1] + Z * (Z0 + h), ic_[k + 1] + Z * (Z0 + h), ic_[k] + Z * (Z0 + h)], SUT, -Z)
    for (a, ph) in ((0.6, 0.4), (1.2, 0.7), (1.9, 0.5), (2.5, 0.3), (1.57, 1.1), (0.9, 1.0), (2.2, 0.95)):
        p = nokta(r - 0.002, a, ph)
        nn = V(cx, cy, Z0 + h) - p
        nn.normalize()
        u = nn.cross(Z).normalized(); w = nn.cross(u)
        y.yuz_yon([p + (u * math.cos(TAU * q / 5) + w * math.sin(TAU * q / 5)) * (0.007 if q % 2 == 0 else 0.007) for q in range(5)], 'altin', nn)
    silme(y, [V(p.x, p.y) for p in reversed(dis_)], Z0 + h - 0.012, 0.012, 0.006, SUT, 'tac', kapali=False)
    # the bench round the inside, the floor, the step
    for s, (dr, hh) in enumerate(((0.035, 0.03), (0.06, 0.018))):
        bi = [V(cx + (r - dr) * math.cos(a), cy + (r - dr) * math.sin(a)) for a in A]
        for k in range(n):
            y.yuz_yon([bi[k] + Z * Z0, bi[k + 1] + Z * Z0, bi[k + 1] + Z * (Z0 + hh), bi[k] + Z * (Z0 + hh)], SUT, V(cx, cy) - (bi[k] + bi[k + 1]) / 2)
            ib = ic_ if s == 0 else [V(cx + (r - 0.035) * math.cos(a), cy + (r - 0.035) * math.sin(a)) for a in A]
            y.yuz_yon([bi[k] + Z * (Z0 + hh), bi[k + 1] + Z * (Z0 + hh), ib[k + 1] + Z * (Z0 + hh), ib[k] + Z * (Z0 + hh)], SUT, Z)
        for uc in (0, n):
            ib = ic_ if s == 0 else [V(cx + (r - 0.035) * math.cos(a), cy + (r - 0.035) * math.sin(a)) for a in A]
            y.yuz_yon([bi[uc] + Z * Z0, ib[uc] + Z * Z0, ib[uc] + Z * (Z0 + hh), bi[uc] + Z * (Z0 + hh)], SUT, -Y)
    y.yuz_yon([V(cx + r * math.cos(a), cy + r * math.sin(a), Z0 + 0.003) for a in A], 'mermer', Z)
    heykel(cx, cy + r * 0.45, Z0, 0.15, 'kralice', 0.0, 'mermer')
    # a reader with his scroll on the bench
    heykel(cx - r * 0.55, cy + r * 0.3, Z0 + 0.0, 0.1, 'bilgin', -0.9, 'siva_krem')


for sx in (-1, 1):
    eksedra(sx * 0.42, -0.1, 0.12, 0.13, 0.1)

# ---------------------------------------------------------------- the great hall
y.bolum('Buyuk salon')
kutu(y, V(HX0, HY0, Z0), X, HX1 - HX0, HY1 - HY0, ZH - Z0, DUV, 'onarkasagsol')
y.yuz_yon([V(HX0, HY0, ZH), V(HX1, HY0, ZH), V(HX1, HY1, ZH), V(HX0, HY1, ZH)], 'zemin', Z)
silme(y, dikdortgen(HX0, HX1, HY0, HY1), ZH - 0.012, 0.012, 0.008, SUT, 'tac')
silme(y, dikdortgen(HX0, HX1, HY0, HY1), Z0, 0.014, 0.008, SUT, 'kaide')
merdiven(y, (0, HY0 - 0.09), math.pi / 2, 0.76, Z0, ZH, n=6, d=0.015, key=SUT)
for sx in (-1, 1):
    kutu_merkez(y, (sx * 0.4, HY0 - 0.045), 0.04, 0.09, ZH - Z0 + 0.012, SUT, z0=Z0)
    heykel(sx * 0.4, HY0 - 0.05, ZH + 0.012, 0.2, 'kral' if sx < 0 else 'kralice', 0.0, 'granit_kizil')
# the hall walls: windowed bays between pilasters
WX0, WX1, WY0, WY1 = -0.46, 0.46, 0.38, 0.98
HW = 0.3
for (a, b, nbay, kapi_) in ((V(WX0, WY0), V(WX1, WY0), 3, True), (V(WX1, WY0), V(WX1, WY1), 4, False), (V(WX1, WY1), V(WX0, WY1), 3, False),
                            (V(WX0, WY1), V(WX0, WY0), 4, False)):
    for k in range(nbay):
        pa, pb = a.lerp(b, k / nbay), a.lerp(b, (k + 1) / nbay)
        if kapi_ and k == 1:
            dikdortgen_acik(y, pa, pb, ZH, HW, 0.3, 0.7, 0.0, 0.23, (DUV, DUV, SUT, 'ahsap'), derin=0.03, cerceve=(0.012, 'altin'))
        else:
            dikdortgen_acik(y, pa, pb, ZH, HW, 0.3, 0.7, 0.09, 0.25, (DUV, DUV, SUT, 'cam'), derin=0.02, cerceve=(0.009, SUT))
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for pp in ((pa,) if k else ()):
            kutu_merkez(y, (pp.x, pp.y), 0.026, 0.02, HW, SUT, z0=ZH, aci=math.atan2(e.y, e.x))
    for pp in (a,):
        kutu_merkez(y, (pp.x, pp.y), 0.03, 0.03, HW, SUT, z0=ZH)
KH = dikdortgen(WX0, WX1, WY0, WY1)
duvarlar(y, KH, ZH + HW, ZE, DUV)
silme(y, KH, ZH + HW, 0.03, 0.008, SUT, 'duz')
silme(y, KH, ZE - 0.026, 0.026, 0.026, SUT, 'tac')
for i in range(4):   # the painted frieze between architrave and cornice
    a, b = KH[i], KH[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x); L_ = (b - a).length
    Pf = lambda s_, t_, d=0.002, a=a, e=e, nn=nn: V(a.x, a.y) + e * s_ + Z * (ZH + HW + t_) + nn * d
    levha(Pf, 0.01, L_ - 0.01, 0.036, 0.07, 'lacivert', nn, 0.0012)
    for m in range(int((L_ - 0.04) / 0.045)):
        s_ = 0.03 + m * 0.045
        if m % 2:
            y.yuz_yon([Pf(s_ + 0.009 * math.cos(TAU * q / 8), 0.053 + 0.009 * math.sin(TAU * q / 8), 0.0025) for q in range(8)], 'altin', nn)
        else:
            levha(Pf, s_ - 0.004, s_ + 0.004, 0.04, 0.066, 'boya_kirmizi', nn, 0.0025)
# flat roof terrace with a low parapet and corner acroteria
y.yuz_yon([V(p.x, p.y, ZE) for p in disa(KH, 0.026)], DUV, Z)
parapet(y, disa(KH, 0.02), ZE, 0.03, 0, 0.014, SUT)
for p in disa(KH, 0.012):
    kure(y, (p.x, p.y, ZE + 0.04), 0.012, 'altin', n=8, kat=4)
# the astronomers' roof: two round columned observatories (tholoi) at the back corners, a gnomon and a bowl sundial
for sx in (-1, 1):
    tc = (sx * 0.365, 0.875)
    donel(y, tc, [(0, ZE), (0.058, ZE), (0.058, ZE + 0.008), (0.052, ZE + 0.008), (0.052, ZE + 0.016), (0, ZE + 0.016)], SUT, n=16)
    for i in range(8):
        a = TAU * (i + 0.5) / 8
        sutun(y, tc[0] + 0.043 * math.cos(a), tc[1] + 0.043 * math.sin(a), ZE + 0.016, ZE + 0.1, 0.0065, SUT, 'iyon', yiv=8)
    donel(y, tc, [(0, ZE + 0.1), (0.052, ZE + 0.1), (0.052, ZE + 0.114), (0.058, ZE + 0.12), (0.058, ZE + 0.124), (0, ZE + 0.124)], SUT, n=16)
    yt_ = y.kubbe(tc, 0.05, ZE + 0.124, 0.045, 'bakir', n=16, kat=5)
    kure(y, (tc[0], tc[1], ZE + 0.176), 0.009, 'altin', n=8, kat=4)
    # inside: a bronze armillary on a pillar
    y.silindir(tc, 0.006, ZE + 0.016, ZE + 0.05, SUT, n=6)
    kure(y, (tc[0], tc[1], ZE + 0.062), 0.013, 'bronz', n=8, kat=4)
    # in front: the gnomon on its stepped base, a bowl sundial on a pedestal
    gx, gy = sx * 0.37, 0.52
    kutu_merkez(y, (gx, gy), 0.05, 0.05, 0.01, SUT, z0=ZE)
    kutu_merkez(y, (gx, gy), 0.034, 0.034, 0.008, SUT, z0=ZE + 0.01)
    y.koni((gx, gy), 0.005, ZE + 0.018, 0.09, 'bronz', n=6)
    donel(y, (gx, gy + 0.1), [(0, ZE), (0.012, ZE), (0.008, ZE + 0.03), (0.02, ZE + 0.034), (0.022, ZE + 0.046), (0.016, ZE + 0.046), (0, ZE + 0.038)], 'bronz', n=12)
    heykel(gx - sx * 0.02, 0.72, ZE, 0.11, 'bilgin', sx * 1.2, 'mermer')

# the portico: eight papyrus-bundle columns, a painted entablature, the pediment
y.bolum('Revak ve alinlik')
PRY = 0.22
xs_ = [-0.42 + 0.12 * i for i in range(8)]
for xx in xs_:
    sutun(y, xx, PRY, ZH, ZH + HW, 0.022, SUT, 'misir', bant_key='turkuaz')
for sx in (-1, 1):
    sutun(y, sx * 0.42, 0.31, ZH, ZH + HW, 0.022, SUT, 'misir', bant_key='turkuaz')
EB = [V(-0.46, 0.19), V(0.46, 0.19), V(0.46, WY0), V(-0.46, WY0)]
kutu(y, V(-0.46, 0.19, ZH + HW), X, 0.92, 0.06, 0.03, SUT)
for sx in (-1, 1):
    x0 = -0.46 if sx < 0 else 0.4
    kutu(y, V(x0, 0.25, ZH + HW), X, 0.06, WY0 - 0.25, 0.03, SUT, 'arkasagsolust')
kutu(y, V(-0.46, 0.188, ZH + HW + 0.03), X, 0.92, 0.062, ZE - ZH - HW - 0.056, SUT, 'onsagsol')
Pe = lambda s_, t_, d=0.002: V(-0.46 + s_, 0.188, ZH + HW + 0.03 + t_) - Y * d
levha(Pe, 0.01, 0.91, 0.006, 0.036, 'lacivert', -Y, 0.0012)
for m in range(20):
    s_ = 0.03 + m * 0.045
    if m % 2:
        y.yuz_yon([Pe(s_ + 0.009 * math.cos(TAU * q / 8), 0.021 + 0.009 * math.sin(TAU * q / 8), 0.0025) for q in range(8)], 'altin', -Y)
    else:
        levha(Pe, s_ - 0.004, s_ + 0.004, 0.008, 0.034, 'boya_kirmizi', -Y, 0.0025)
silme(y, [V(-0.46, 0.188), V(0.46, 0.188)], ZE - 0.026, 0.026, 0.026, SUT, 'tac', kapali=False)
for sx in (-1, 1):
    a, b = (V(-0.46, WY0), V(-0.46, 0.188)) if sx < 0 else (V(0.46, 0.188), V(0.46, WY0))
    silme(y, [a, b], ZE - 0.026, 0.026, 0.026, SUT, 'tac', kapali=False)
y.yuz_yon([V(-0.46, 0.188, ZE), V(0.46, 0.188, ZE), V(0.46, WY0, ZE), V(-0.46, WY0, ZE)], SUT, Z)
zt = alinlik(y, V(-0.48, 0.165), V(0.48, 0.165), ZE, 0.15, WY0 - 0.165, SUT, 'lacivert', 0.014, 'kiremit')
# the tympanum: gilded figures round the seated Muse, acroteria
Pt = lambda s_, t_, d=0.0: V(s_, 0.165 + 0.0035 - d, ZE + t_)
for (sc, h_, key) in ((0.0, 0.1, 'altin'), (-0.12, 0.07, 'altin'), (0.12, 0.07, 'altin'), (-0.25, 0.045, 'mermer'), (0.25, 0.045, 'mermer')):
    levha(lambda s_, t_, d: Pt(s_, t_, d), sc - 0.016, sc + 0.016, 0.025, 0.025 + h_, key, -Y, -0.0055)
    kure(y, (sc, 0.165 - 0.0035, ZE + 0.025 + h_ + 0.01), 0.011, key, n=8, kat=4)
kure(y, (0, 0.17, zt + 0.02), 0.022, 'altin', n=10, kat=5)
for sx in (-1, 1):
    kure(y, (sx * 0.47, 0.17, ZE + 0.03), 0.016, 'altin', n=8, kat=4)

# the octagonal drum, the copper dome, a lantern carrying a gilded globe
y.bolum('Kubbe')
DC = (0, 0.7)
DR = 0.23
ZD = ZE + 0.02
kutu_merkez(y, DC, 2 * DR + 0.06, 2 * DR + 0.06, 0.02, DUV, z0=ZE)
kd = cokgen(DC, DR, 8, kat=math.pi / 8)
pencereli_duvar(y, kd, ZD, 0.15, [1] * 8, renk=(DUV, DUV, SUT, 'cam'), en=0.42, sivri=0.0, cerceve=(0.008, SUT), v0=0.03)
for p in kd:
    kutu_merkez(y, (p.x * 1.0, p.y), 0.022, 0.022, 0.15, SUT, z0=ZD)
silme(y, kd, ZD + 0.15, 0.022, 0.016, SUT, 'tac')
y.yuz_yon([V(p.x, p.y, ZD + 0.172) for p in disa(kd, 0.016)], DUV, Z)
zk = ZD + 0.172
tepe = y.kubbe(DC, DR - 0.005, zk, 0.21, 'bakir', n=32, kat=8)
for i in range(16):   # ribs
    a = TAU * i / 16
    pts = [V(DC[0] + (DR - 0.002) * math.cos(math.pi / 2 * k / 8) * math.cos(a), DC[1] + (DR - 0.002) * math.cos(math.pi / 2 * k / 8) * math.sin(a), zk + 0.21 * math.sin(math.pi / 2 * k / 8)) for k in range(8)]
    boru(y, pts, 0.005, 'bakir2', n=4)
ZL = zk + 0.2
for i in range(6):
    a = TAU * i / 6
    y.silindir((DC[0] + 0.035 * math.cos(a), DC[1] + 0.035 * math.sin(a)), 0.005, ZL, ZL + 0.05, SUT, n=6)
kutu_merkez(y, DC, 0.09, 0.09, 0.008, SUT, z0=ZL - 0.004)
donel(y, DC, [(0.05, ZL + 0.05), (0.052, ZL + 0.058), (0.03, ZL + 0.075), (0, ZL + 0.082)], 'bakir', n=12)
y.silindir(DC, 0.004, ZL + 0.08, ZL + 0.11, 'altin', n=6)
kure(y, (DC[0], DC[1], ZL + 0.13), 0.025, 'altin', n=12, kat=6)
boru(y, [V(DC[0] - 0.03, DC[1], ZL + 0.13), V(DC[0] + 0.03, DC[1], ZL + 0.13)], 0.003, 'altin', n=4)

# ---------------------------------------------------------------- book-stack wings with open loggias
y.bolum('Kitaplik kanatlari')
for sx in (-1, 1):
    xi, xb, xo = sx * 0.56, sx * 0.9, sx * 1.06     # inner wall, loggia back wall, loggia front edge
    yb0, yb1 = 0.26, 0.96
    zw = Z0 + 0.26
    x0, x1 = min(xi, xo), max(xi, xo)
    # the body
    a_, b_ = (V(xb, yb0), V(xb, yb1)) if sx > 0 else (V(xb, yb1), V(xb, yb0))
    nb = 6
    for k in range(nb):
        pa, pb = a_.lerp(b_, k / nb), a_.lerp(b_, (k + 1) / nb)
        duz_duvar(y, pa, pb, Z0, zw, 'siva_krem')
        raf(pa.lerp(pb, 0.1), pa.lerp(pb, 0.9), Z0 + 0.03, 0.19, 3, 5, tohum=k)
    xin, xbb = sorted((xi, xb))
    for (yy, nn) in ((yb0, -1), (yb1, 1)):
        a, b = (V(xin, yy), V(xbb, yy)) if nn < 0 else (V(xbb, yy), V(xin, yy))
        for k in range(2):
            pa, pb = a.lerp(b, k / 2), a.lerp(b, (k + 1) / 2)
            dikdortgen_acik(y, pa, pb, Z0, zw - Z0, 0.3, 0.7, 0.08, 0.2, ('siva_krem', 'siva_krem', SUT, 'cam'), derin=0.015, cerceve=(0.008, SUT))
        # the loggia's end walls
        a, b = (V(min(xb, xo), yy), V(max(xb, xo), yy)) if nn < 0 else (V(max(xb, xo), yy), V(min(xb, xo), yy))
        duz_duvar(y, a, b, Z0, zw, 'siva_krem')
        duz_duvar(y, b - V(0, nn * 0.02), a - V(0, nn * 0.02), Z0, zw, 'siva_krem')
        y.yuz_yon([V(xo, yy, Z0), V(xo, yy - nn * 0.02, Z0), V(xo, yy - nn * 0.02, zw), V(xo, yy, zw)], 'siva_krem', V(sx, 0))
        y.yuz_yon([V(min(xb, xo), yy - nn * 0.02, zw), V(max(xb, xo), yy - nn * 0.02, zw), V(max(xb, xo), yy, zw), V(min(xb, xo), yy, zw)], 'siva_krem', Z)
    a, b = (V(xi, yb1), V(xi, yb0)) if sx > 0 else (V(xi, yb0), V(xi, yb1))
    duz_duvar(y, a, b, Z0, zw, 'siva_krem')
    # loggia floor (two steps up) and its columns
    kutu(y, V(min(xb, xo), yb0, Z0), X, abs(xo - xb), yb1 - yb0, 0.018, SUT, 'onarkasagsolust')
    for k in range(8):
        yy = yb0 + 0.04 + k * (yb1 - yb0 - 0.08) / 7
        hafif_sutun(xo - sx * 0.025, yy, Z0 + 0.018, zw - 0.025, 0.012, SUT, 'boya_kirmizi')
    kutu(y, V(min(xo, xo - sx * 0.05), yb0, zw - 0.025), X, 0.05, yb1 - yb0, 0.025, SUT)
    y.yuz_yon([V(min(xb, xo), yb0, zw - 0.0005), V(max(xb, xo), yb0, zw - 0.0005), V(max(xb, xo), yb1, zw - 0.0005), V(min(xb, xo), yb1, zw - 0.0005)], 'lacivert', -Z)
    cati_besik(y, x0, x1, yb0, yb1, zw, 0.12, 0.03, 'kiremit', 'kiremit2', ucluk_key='siva_krem', alinlik_key=SUT)
    # a scholar reading in the loggia
    heykel(xb + sx * 0.06, (yb0 + yb1) / 2, Z0 + 0.018, 0.09, 'bilgin', -sx * math.pi / 2, 'siva_krem')

# ---------------------------------------------------------------- outer garden, palms
y.bolum('Dis bahce')
for (px, py, b, tur) in ((-0.96, -0.95, 0.2, 'palmiye'), (-1.04, -0.7, 0.17, 'palmiye'), (-0.95, -0.4, 0.19, 'palmiye'), (-1.02, -0.12, 0.16, 'servi'),
                         (0.96, -0.95, 0.2, 'palmiye'), (1.04, -0.7, 0.17, 'palmiye'), (0.95, -0.4, 0.19, 'palmiye'), (1.02, -0.12, 0.16, 'servi'),
                         (-0.6, -1.06, 0.15, 'palmiye'), (0.6, -1.06, 0.15, 'palmiye'), (0.0, 1.06, 0.14, 'servi'), (-0.3, 1.06, 0.14, 'servi'), (0.3, 1.06, 0.14, 'servi')):
    agac(y, px, py, Z0, b, tur)

calistir(y, 'lm_kutuphane')
