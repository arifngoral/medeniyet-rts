# Büyük Piramit (lm_piramit): the pyramid of Khufu at Giza while its casing is being finished: smooth white Tura
# limestone casing with a gilded pyramidion over a stepped sandstone core that still shows along a ragged lower edge;
# a mud-brick construction ramp with a sledge-hauling gang, the enclosure wall, the mortuary temple (granite pillared
# court, basalt floor, causeway), three queens' pyramids, mastaba fields, a boat pit with the cedar ship, a block yard.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
R = random.Random(7)
Z0 = 0.04            # desert ground top

# cavetto cornice (Egyptian gorge): a torus roll, then the hollow flaring out, a flat top band
KAVETTO = [(0, 0), (0.16, 0.03), (0.2, 0.1), (0.12, 0.17), (0.04, 0.19), (0.07, 0.36), (0.18, 0.56), (0.4, 0.75),
           (0.72, 0.88), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]


# ---------------------------------------------------------------- helpers
def kavetto(kose, z, h, c, key='kirec', kapali=True, ust=True):
    """a cavetto cornice on top of a wall polygon kose (z: its foot), its top capped (ust)"""
    silme(y, kose, z, h, c, key, KAVETTO, kapali)
    if ust and kapali:
        y.yuz_yon([V(p.x, p.y, z + h) for p in kose], key, Z)


def egik_blok(x0, x1, y0, y1, z0, h, ix, iy, key='kirec', ust=True):
    """a battered block (mastaba): the top inset ix in x and iy in y; returns base and top corners"""
    B = dikdortgen(x0, x1, y0, y1, z0); T = dikdortgen(x0 + ix, x1 - ix, y0 + iy, y1 - iy, z0 + h)
    for i in range(4):
        j = (i + 1) % 4
        e = B[j] - B[i]; n = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], key, n + Z * 0.2)
    if ust:
        y.yuz_yon(T, key, Z)
    return B, T


def levha(P, s0, s1, t0, t1, key, n, d=0.003):
    y.yuz_yon([P(s0, t0, d), P(s1, t0, d), P(s1, t1, d), P(s0, t1, d)], key, n)


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


def kaplamali_piramit(cx, cy, W, H, z0, kmap, dz, dc, ns, uc_key='altin', key='kirec', cekirdek='kum', uc_oran=0.045):
    """a pyramid whose stepped core (cekirdek, courses dz high) is cased in smooth stone (key) dc thick; on face i the
    casing of block column j starts kmap[i][j] courses up (a ragged lower edge where the casing is still being set).
    Returns the apex z and the casing half-width function"""
    nk = max(max(r) for r in kmap)
    Rk = lambda z: W / 2 * (1 - (z - z0) / H)          # the core plane
    Rc = lambda z: Rk(z) + dc                          # the casing plane
    apex = z0 + H * (1 + 2 * dc / W)
    kose = [V(-1, -1), V(1, -1), V(1, 1), V(-1, 1)]
    C = V(cx, cy)
    P = lambda i, u, r, z: (C + kose[i].lerp(kose[(i + 1) % 4], u) * r) + Z * z
    # the stepped core, as high as the casing leaves it bare
    for k in range(nk):
        za, zb = z0 + k * dz, z0 + (k + 1) * dz
        r0, r1 = Rk(zb), Rk(zb + dz)
        for i in range(4):
            j = (i + 1) % 4
            nn = kose[i] + kose[j]
            y.yuz_yon([P(i, 0, r0, za), P(i, 1, r0, za), P(i, 1, r0, zb), P(i, 0, r0, zb)], cekirdek, nn)
            y.yuz_yon([P(i, 0, r0, zb), P(i, 1, r0, zb), P(i, 1, r1, zb), P(i, 0, r1, zb)], cekirdek, Z)
    zb = z0 + nk * dz
    for i in range(4):
        nn = (kose[i] + kose[(i + 1) % 4]).normalized()
        nf = (nn + Z * (W / (2 * H))).normalized()
        ks = kmap[i]
        for j in range(ns):
            u0, u1 = j / ns, (j + 1) / ns
            zj = z0 + ks[j] * dz
            if ks[j] < nk:
                y.yuz_yon([P(i, u0, Rc(zj), zj), P(i, u1, Rc(zj), zj), P(i, u1, Rc(zb), zb), P(i, u0, Rc(zb), zb)], key, nf)
            if j < ns - 1 and ks[j] != ks[j + 1]:
                lo, hi = sorted((ks[j], ks[j + 1]))
                zl, zh = z0 + lo * dz, z0 + hi * dz
                e = kose[(i + 1) % 4] - kose[i]; e.normalize()
                yon = e if ks[j] < ks[j + 1] else -e
                y.yuz_yon([P(i, u1, Rc(zl), zl), P(i, u1, Rc(zh), zh), P(i, u1, Rk(zh) - 0.01, zh), P(i, u1, Rk(zl) - 0.01, zl)], key, yon)
            # the casing's lower lip (seen from below the band only where it overhangs a step)
        zt = z0 + (apex - z0) * (1 - uc_oran)
        y.yuz_yon([P(i, 0, Rc(zb), zb), P(i, 1, Rc(zb), zb), P(i, 1, Rc(zt), zt), P(i, 0, Rc(zt), zt)], key, nf)
        y.yuz_yon([P(i, 0, Rc(zt), zt), P(i, 1, Rc(zt), zt), C + Z * apex], uc_key, nf)
    return apex, Rc


def yuz_cerceve(cx, cy, W, H, z0, dc, i, z):
    """a frame on face i of a pyramid at height z (centre of the face): (o, e along, s up the slope, n out)"""
    kose = [V(-1, -1), V(1, -1), V(1, 1), V(-1, 1)]
    nn = (kose[i] + kose[(i + 1) % 4]) / 2
    e = kose[(i + 1) % 4] - kose[i]; e.normalize()
    r = W / 2 * (1 - (z - z0) / H) + dc
    o = V(cx, cy) + nn * r + Z * z
    s = (nn * (-W / (2 * H)) + Z).normalized()
    n = (nn + Z * (W / (2 * H))).normalized()
    return o, e, s, n


def adam(x, yy, z, aci, egim=0.0, kol='ip', s=1.0, ten='kirmizi', etek='beyaz'):
    """a small worker, built facing +x then turned to aci: striding legs, white kilt, bare torso leaning forward
    (egim), head with dark hair; kol: 'ip' (both hands forward on a rope), 'asa' (a staff), 'testi' (a jar raised),
    'yan' (arms down)"""
    with parca(y, (x, yy, z), aci, s):
        hip = V(0.0, 0, 0.021)
        cubuk(y, V(0.007 + egim * 0.004, 0.0035, 0.0), hip + V(0, 0.003, 0), 0.0045, ten)
        cubuk(y, V(-0.008 - egim * 0.004, -0.0035, 0.0), hip + V(0, -0.003, 0), 0.0045, ten)
        omuz = hip + V(egim * 0.014, 0, 0.016 - egim * 0.004)
        kutu_merkez(y, (hip.x + egim * 0.002, 0), 0.011, 0.012, 0.008, etek, z0=hip.z - 0.004)
        cubuk(y, hip + V(0, 0, 0.003), omuz, 0.0105, ten, 0.007)
        bas = omuz + V(egim * 0.004, 0, 0.0065)
        kure(y, bas, 0.0045, ten, n=8, kat=4)
        kure(y, bas + V(-0.0012, 0, 0.0012), 0.0042, 'koyu', n=8, kat=4)
        for sg in (-1, 1):
            o = omuz + V(0, sg * 0.0062, -0.001)
            if kol == 'ip':
                cubuk(y, o, o + V(0.012, -sg * 0.002, -0.009), 0.0032, ten)
            elif kol == 'asa' and sg > 0:
                cubuk(y, o, o + V(0.009, 0.002, -0.006), 0.0032, ten)
                cubuk(y, o + V(0.01, 0.003, -0.022), o + V(0.01, 0.003, 0.014), 0.0022, 'ahsap')
            elif kol == 'testi' and sg > 0:
                cubuk(y, o, o + V(0.008, 0.0, 0.004), 0.0032, ten)
                kure(y, o + V(0.011, 0.0, 0.006), 0.004, 'kerpic_koyu', n=8, kat=4)
            else:
                cubuk(y, o, o + V(0.002, sg * 0.001, -0.014), 0.0032, ten)


def kizak(x, yy, z, aci, blok='kirec', bw=0.05, bd=0.034, bh=0.03):
    """a wooden sledge (two upturned runners, cross bars) carrying a stone block, built along +x, turned to aci"""
    with parca(y, (x, yy, z), aci):
        for sg in (-1, 1):
            boru(y, [V(-bw * 0.55, sg * bd * 0.36, 0.004), V(bw * 0.45, sg * bd * 0.36, 0.004), V(bw * 0.62, sg * bd * 0.36, 0.011)],
                 0.0035, 'ahsap', n=5)
        for k in range(3):
            cubuk(y, V(-bw * 0.4 + k * bw * 0.4, -bd * 0.5, 0.008), V(-bw * 0.4 + k * bw * 0.4, bd * 0.5, 0.008), 0.005, 'ahsap_koyu')
        kutu_merkez(y, (0, 0), bw, bd, bh, blok, z0=0.0105)


# ---------------------------------------------------------------- layout
PCX, PCY = 0.05, 0.12        # the great pyramid
W, H = 1.42, 0.905           # base and height (Khufu: 230 m x 146.6 m)
ZP = Z0 + 0.012              # its pavement
DZ, DC = 0.03, 0.016         # core course height, casing thickness
EO = 0.84                    # enclosure wall half size
EX0, EX1, EY0, EY1 = PCX - EO, PCX + EO, PCY - EO, PCY + EO
GX0, GX1, GY0, GY1 = -1.17, 1.13, -1.13, 1.08

# ---------------------------------------------------------------- ground
y.bolum('Zemin')
zemin(y, GX0, GX1, GY0, GY1, Z0, 'kaya_koyu', 'kum_acik', basamak=(), silmeli=True)
# the paved court inside the enclosure, the pyramid's own pavement
y.yuz([V(EX0 + 0.03, EY0 + 0.03, Z0 + 0.002), V(EX1 - 0.03, EY0 + 0.03, Z0 + 0.002), V(EX1 - 0.03, EY1 - 0.03, Z0 + 0.002),
       V(EX0 + 0.03, EY1 - 0.03, Z0 + 0.002)], 'zemin')
AP = W / 2 + DC + 0.035
kutu(y, V(PCX - AP, PCY - AP, Z0), X, 2 * AP, 2 * AP, ZP - Z0, 'kirec')
# drifted sand and a few rocks on the plateau
for (px, py, r_) in ((1.04, 1.0, 0.03), (-1.1, 0.98, 0.025), (0.62, 1.03, 0.02), (1.1, -1.1, 0.018)):
    donel(y, (px, py), [(r_, Z0 - 0.002), (r_ * 0.7, Z0 + r_ * 0.45), (0, Z0 + r_ * 0.6)], 'kaya', n=7)

# ---------------------------------------------------------------- the great pyramid
y.bolum('Buyuk piramit')
NS = 12
# casing start (in courses) for each block column of each face: front (-y), right (+x), back (+y), left (-x).
# The front is where the ramp still stands: the casing is missing highest there
KMAP = [
    [1, 2, 4, 3, 5, 6, 6, 6, 5, 3, 2, 1],
    [1, 1, 2, 1, 3, 2, 2, 1, 2, 3, 2, 1],
    [1, 2, 1, 1, 2, 3, 2, 1, 1, 2, 1, 1],
    [1, 2, 3, 2, 1, 2, 4, 3, 2, 1, 2, 1],
]
APEX, RC = kaplamali_piramit(PCX, PCY, W, H, ZP, KMAP, DZ, DC, NS, 'altin', 'kirec', 'kum', uc_oran=0.05)
# a gilded collar under the pyramidion
zt = ZP + (APEX - ZP) * 0.95
for i in range(4):
    o, e, s, n = yuz_cerceve(PCX, PCY, W, H, ZP, DC, i, zt - 0.012)
    hw = RC(zt - 0.012)
    hw2 = RC(zt)
    kose = [V(-1, -1), V(1, -1), V(1, 1), V(-1, 1)]
    a0 = V(PCX, PCY) + kose[i] * hw + Z * (zt - 0.012); b0 = V(PCX, PCY) + kose[(i + 1) % 4] * hw + Z * (zt - 0.012)
    a1 = V(PCX, PCY) + kose[i] * hw2 + Z * zt; b1 = V(PCX, PCY) + kose[(i + 1) % 4] * hw2 + Z * zt
    y.yuz_yon([a0 + n * 0.002, b0 + n * 0.002, b1 + n * 0.002, a1 + n * 0.002], 'altin', n)

# the entrance on the north (back) face: a dark doorway under two pairs of great gabled chevron stones
o, e, s, n = yuz_cerceve(PCX, PCY, W, H, ZP, DC, 2, ZP + 0.1)
P = lambda u, t, d=0.0: o + e * u + s * t + n * d
off = 0.06
y.yuz_yon([P(off - 0.022, 0, 0.002), P(off + 0.022, 0, 0.002), P(off + 0.022, 0.04, 0.002), P(off - 0.022, 0.04, 0.002)], 'koyu', n)
for k, (w_, t_) in enumerate(((0.045, 0.05), (0.06, 0.065))):
    for sg in (-1, 1):
        cubuk(y, P(off + sg * w_, t_, 0.008 + k * 0.004), P(off, t_ + w_ * 0.75, 0.008 + k * 0.004), 0.016, 'kirec', 0.018)
for sg in (-1, 1):
    cubuk(y, P(off + sg * 0.028, -0.005, 0.006), P(off + sg * 0.028, 0.045, 0.006), 0.01, 'kirec', 0.012)
cubuk(y, P(off - 0.035, 0.045, 0.006), P(off + 0.035, 0.045, 0.006), 0.01, 'kirec', 0.012)

# ---------------------------------------------------------------- the enclosure wall
y.bolum('Cevre duvari')
WT, WH = 0.03, 0.085


def mur(a, b, bas=True, son=True, kose_bas=False):
    """a stretch of the enclosure wall, outer face on the line a->b (faces its right), rounded coping"""
    a, b = V(a.x, a.y), V(b.x, b.y)
    e = (b - a).normalized()
    if kose_bas: a = a + e * WT
    L = (b - a).length
    yz = 'onarkaust' + ('sol' if bas and not kose_bas else '') + ('sag' if son else '')
    kutu(y, V(a.x, a.y, Z0), e, L, WT, WH, 'kirec', yz)
    sol = V(-e.y, e.x)
    boru(y, [a + sol * (WT / 2) + Z * (Z0 + WH), b + sol * (WT / 2) + Z * (Z0 + WH)], WT * 0.5, 'kirec', n=8)
    silme(y, [a, b], Z0, 0.012, 0.006, 'kirec', 'kaide', kapali=False)


K = dikdortgen(EX0, EX1, EY0, EY1)
RX0, RX1 = 0.0, 0.2          # the gap the ramp passes through
SY0, SY1 = -0.05, 0.29       # the mortuary sanctuary cuts the east (left) side
mur(K[0], V(RX0, EY0), bas=True, son=True)
mur(V(RX1, EY0), K[1], bas=True, son=True)
mur(K[1], K[2], kose_bas=True)
mur(K[2], K[3], kose_bas=True)
mur(K[3], V(EX0, SY1), kose_bas=True, son=True)
mur(V(EX0, SY0), K[0], bas=True, son=False)

# ---------------------------------------------------------------- mortuary temple
y.bolum('Cenaze tapinagi')
TX0, TX1, TY0, TY1 = -1.06, -0.88, -0.1, 0.34
YC = (TY0 + TY1) / 2
ZT = Z0 + 0.1
CH = 0.028
AMB = 0.05
ZA = ZT - 0.024
K0 = dikdortgen(TX0, TX1, TY0, TY1)
KI = dikdortgen(TX0 + AMB, TX1 - AMB, TY0 + AMB, TY1 - AMB)
# outer walls (the back stretch only beside the sanctuary)
duz_duvar(y, K0[0], K0[1], Z0, ZT, 'kirec')
duz_duvar(y, K0[1], V(TX1, SY0), Z0, ZT, 'kirec')
duz_duvar(y, V(TX1, SY1), K0[2], Z0, ZT, 'kirec')
duz_duvar(y, K0[2], K0[3], Z0, ZT, 'kirec')
duz_duvar(y, K0[3], K0[0], Z0, ZT, 'kirec')
silme(y, K0, Z0, 0.014, 0.007, 'kirec', 'kaide')
silme(y, K0, ZT, CH, 0.02, 'kirec', KAVETTO)
# roof of the ambulatory round the open court
for i in range(4):
    j = (i + 1) % 4
    y.yuz_yon([K0[i] + Z * (ZT + CH), K0[j] + Z * (ZT + CH), KI[j] + Z * (ZT + CH), KI[i] + Z * (ZT + CH)], 'kirec', Z)
# the architrave facing the court, the walls' inner faces behind the pillars
for i in range(4):
    j = (i + 1) % 4
    duz_duvar(y, KI[j], KI[i], ZA, ZT + CH, 'kirec')
KW = disa(K0, -0.016)
for i in range(4):
    duz_duvar(y, KW[(i + 1) % 4], KW[i], Z0, ZA, 'kirec')
y.yuz([V(p.x, p.y, Z0 + 0.005) for p in KW], 'bazalt')
# red granite pillars round the court, a painted band on the architrave
for i in range(4):
    a, b = KI[i], KI[(i + 1) % 4]
    L = (b - a).length
    n_ = max(2, round(L / 0.055))
    for k in range(n_):
        p = a.lerp(b, k / n_)
        kutu_merkez(y, (p.x, p.y), 0.022, 0.022, ZA - Z0 - 0.005, 'granit_kizil', z0=Z0 + 0.005)
    e = (b - a).normalized(); nc = V(-e.y, e.x)    # (towards the court)
    Pp = lambda s_, t_, d=0.002, a=a, e=e, nc=nc: a + e * s_ + Z * (ZA + t_) + nc * d
    levha(Pp, 0.01, L - 0.01, 0.008, 0.013, 'boya_kirmizi', nc)
    levha(Pp, 0.01, L - 0.01, 0.017, 0.021, 'lacivert', nc)
# an offering altar in the court, seated statues of the king, statue niches in the back wall
kutu_merkez(y, (TX0 + 0.1, YC), 0.04, 0.03, 0.018, 'granit', z0=Z0 + 0.005)
for sy in (-1, 1):
    with parca(y, (TX0 + 0.09, YC + sy * 0.1, Z0 + 0.005), math.pi, 0.06):   # (built facing +x, turned to face the gate)
        kutu_merkez(y, (-0.05, 0), 0.4, 0.42, 0.42, 'granit_kizil')           # throne
        kutu_merkez(y, (-0.25, 0), 0.12, 0.42, 0.95, 'granit_kizil')          # back pillar
        for s2 in (-1, 1):
            kutu_merkez(y, (0.2, s2 * 0.08), 0.14, 0.12, 0.42, 'granit_kizil')     # shins
            kutu_merkez(y, (0.05, s2 * 0.08), 0.32, 0.13, 0.12, 'granit_kizil', z0=0.42)   # thighs
        kutu_merkez(y, (-0.1, 0), 0.2, 0.34, 0.34, 'granit_kizil', z0=0.5)    # torso
        kure(y, (-0.08, 0, 0.96), 0.1, 'granit_kizil', n=8, kat=4)            # head
        kutu_merkez(y, (-0.1, 0), 0.16, 0.3, 0.16, 'boya_sari', z0=0.86)      # nemes
        kutu_merkez(y, (-0.12, 0), 0.14, 0.2, 0.1, 'beyaz', z0=1.02)          # crown
for k in range(5):
    yy = TY0 + AMB + 0.03 + k * (TY1 - TY0 - 2 * AMB - 0.06) / 4
    Pn = lambda s_, t_, d=0.002, yy=yy: V(TX1 - 0.016, yy + s_, Z0 + t_) - X * d
    levha(Pn, -0.012, 0.012, 0.012, 0.06, 'koyu', -X)
    levha(Pn, -0.016, 0.016, 0.06, 0.064, 'kirec', -X, 0.004)

# the portal on the causeway side
PX0 = TX0 - 0.035
kutu(y, V(PX0, YC - 0.065, Z0), X, 0.045, 0.13, 0.135, 'kirec', 'onarkaust')
dikdortgen_acik(y, V(PX0, YC + 0.065), V(PX0, YC - 0.065), Z0, 0.135, 0.3, 0.7, 0.0, 0.085, ('kirec', 'kirec', 'kirec', 'ahsap'),
                derin=0.02, cerceve=(0.008, 'granit_kizil'))
kavetto(dikdortgen(PX0, PX0 + 0.045, YC - 0.065, YC + 0.065), Z0 + 0.135, 0.026, 0.016)
kanatli_gunes(V(PX0, YC, Z0 + 0.112), -Y, -X, 0.1, 0.022)
# the covered causeway running off the plateau, and its stair
CW = 0.075
kutu(y, V(GX0, YC - CW / 2, Z0), X, PX0 - GX0, CW, 0.06, 'kirec', 'onarkaust')
for k in range(4):
    xx = GX0 + 0.012 + k * 0.026
    kutu(y, V(xx, YC - 0.006, Z0 + 0.06), X, 0.012, 0.012, 0.0015, 'koyu', 'onarkasagsolust')
silme(y, [V(PX0, YC - CW / 2), V(GX0, YC - CW / 2)], Z0 + 0.06, 0.012, 0.008, 'kirec', KAVETTO, kapali=False)
silme(y, [V(GX0, YC + CW / 2), V(PX0, YC + CW / 2)], Z0 + 0.06, 0.012, 0.008, 'kirec', KAVETTO, kapali=False)
dikdortgen_acik(y, V(GX0, YC + CW / 2), V(GX0, YC - CW / 2), Z0, 0.06, 0.25, 0.75, 0.0, 0.045, ('kirec', 'kirec', 'kirec', 'koyu'), derin=0.015)
merdiven(y, (GX0 - 0.06, YC), 0.0, CW, 0.0, Z0, n=4, key='kirec')

# the sanctuary against the pyramid: taller, a false door and the winged sun towards the court
SX0, SX1 = TX1, -0.72
ZS = Z0 + 0.16
duvarlar(y, dikdortgen(SX0, SX1, SY0, SY1), Z0, ZS, 'kirec')
silme(y, dikdortgen(SX0, SX1, SY0, SY1), Z0, 0.014, 0.007, 'kirec', 'kaide')
for p in dikdortgen(SX0, SX1, SY0, SY1):
    boru(y, [V(p.x, p.y, Z0 + 0.014), V(p.x, p.y, ZS)], 0.007, 'kirec', n=6)
silme(y, dikdortgen(SX0, SX1, SY0, SY1), ZS - 0.008, 0.008, 0.004, 'kirec', 'yarim')
kavetto(dikdortgen(SX0, SX1, SY0, SY1), ZS, 0.034, 0.024)
Ps = lambda s_, t_, d=0.002: V(SX0, YC + s_, Z0 + t_) - X * d
for k, (w_, key) in enumerate(((0.07, 'kirec'), (0.055, 'granit_kizil'), (0.04, 'kirec'), (0.018, 'koyu'))):
    levha(Ps, -w_ / 2, w_ / 2, ZT + CH - Z0 + 0.002 + k * 0.004, ZS - Z0 - 0.012 - k * 0.003, key, -X, 0.002 + k * 0.0012)
kanatli_gunes(V(SX0, YC - 0.1, ZS - 0.03), -Y, -X, 0.09, 0.02)
kanatli_gunes(V(SX0, YC + 0.1, ZS - 0.03), -Y, -X, 0.09, 0.02)
# the team banner at the portal, painted pennant poles
sancak(y, PX0 - 0.015, YC + 0.085, Z0, boy=0.28, en=0.13, yuk=0.075, aci=math.pi * 0.85)
for yy in (YC - 0.085,):
    y.silindir((PX0 - 0.015, yy), 0.006, Z0, Z0 + 0.24, 'ahsap', n=6)
    y.koni((PX0 - 0.015, yy), 0.008, Z0 + 0.24, 0.025, 'altin', n=6)

# ---------------------------------------------------------------- queens' pyramids
y.bolum('Kralice piramitleri')
QX = -0.97
for k, qy in enumerate((-0.33, -0.6, -0.87)):
    qw, qh = 0.22 - k * 0.012, 0.14 - k * 0.008
    km = [[1] * 6, [1] * 6, [1] * 6, [1] * 6] if k != 1 else [[1, 2, 3, 2, 1, 1], [1, 1, 2, 1, 1, 1], [1, 1, 1, 2, 1, 1], [1, 2, 1, 3, 2, 1]]
    kutu(y, V(QX - qw / 2 - 0.015, qy - qw / 2 - 0.015, Z0), X, qw + 0.03, qw + 0.03, 0.006, 'kirec')
    kaplamali_piramit(QX, qy, qw, qh, Z0 + 0.006, km, 0.015, 0.008, 6, 'kirec', 'kirec', 'kum', uc_oran=0.08)
    # its small offering chapel on the east side
    cx0, cx1 = QX - qw / 2 - 0.075, QX - qw / 2 - 0.02
    kutu(y, V(cx0, qy - 0.04, Z0), X, cx1 - cx0, 0.08, 0.045, 'kirec', 'onarkasagust')
    dikdortgen_acik(y, V(cx0, qy + 0.04), V(cx0, qy - 0.04), Z0, 0.045, 0.35, 0.65, 0.0, 0.03, ('kirec', 'kirec', 'kirec', 'koyu'), derin=0.01)
    kavetto(dikdortgen(cx0, cx1, qy - 0.04, qy + 0.04), Z0 + 0.045, 0.012, 0.008)

# ---------------------------------------------------------------- boat pit with the cedar ship
y.bolum('Gemi cukuru')
BX, BY0, BY1, BW = -0.98, 0.43, 0.87, 0.085
BH = 0.022


def mercek(cx, y0, y1, w, n=14):
    """a lens (boat-shaped) outline along y, CCW"""
    L = (y1 - y0) / 2; yc = (y0 + y1) / 2
    sag = [V(cx + w / 2 * math.sin(math.pi * k / n) ** 0.7, yc - L * math.cos(math.pi * k / n)) for k in range(n + 1)]
    sol = [V(cx - w / 2 * math.sin(math.pi * k / n) ** 0.7, yc + L * math.cos(math.pi * k / n)) for k in range(1, n)]
    return sag + sol


ic = mercek(BX, BY0, BY1, BW)
dis_ = disa(ic, 0.02)
duvarlar(y, dis_, Z0, Z0 + BH, 'kirec')
duvarlar(y, list(reversed(ic)), Z0, Z0 + BH, 'kirec')
for i in range(len(ic)):
    j = (i + 1) % len(ic)
    y.yuz_yon([dis_[i] + Z * (Z0 + BH), dis_[j] + Z * (Z0 + BH), ic[j] + Z * (Z0 + BH), ic[i] + Z * (Z0 + BH)], 'kirec', Z)
y.yuz_yon([V(p.x, p.y, Z0 + 0.002) for p in ic], 'koyu', Z)
# the ship: a long cedar hull rising to papyrus-bundle ends, a cabin and a canopy on poles
yc, L = (BY0 + BY1) / 2, (BY1 - BY0) / 2 - 0.02
halkalar = []
NB = 12
for k in range(NB + 1):
    t = -1 + 2 * k / NB
    hw = 0.03 * (1 - t * t) ** 0.6 + 0.002
    zz = Z0 + 0.012 + 0.008 * t * t
    yy = yc + t * L
    halkalar.append([V(BX - hw, yy, zz + 0.006), V(BX - hw * 0.7, yy, zz - 0.004), V(BX, yy, zz - 0.007), V(BX + hw * 0.7, yy, zz - 0.004), V(BX + hw, yy, zz + 0.006)])
for k in range(NB):
    for m in range(4):
        q = [halkalar[k][m], halkalar[k + 1][m], halkalar[k + 1][m + 1], halkalar[k][m + 1]]
        yuz_dis(y, q, 'ahsap_acik', V(BX, (q[0].y + q[1].y) / 2, Z0 + 0.03))
    y.yuz_yon([halkalar[k][0], halkalar[k][4], halkalar[k + 1][4], halkalar[k + 1][0]], 'ahsap', Z)
for uc, sg in ((0, -1), (NB, 1)):
    p = V(BX, yc + sg * L, Z0 + 0.026)
    boru(y, [p, p + V(0, sg * 0.018, 0.008), p + V(0, sg * 0.026, 0.024), p + V(0, sg * 0.022, 0.034)], 0.004, 'ahsap_acik', n=6, r_son=0.0025)
kutu_merkez(y, (BX, yc + 0.03), 0.03, 0.08, 0.018, 'ahsap', z0=Z0 + 0.018)
kutu_merkez(y, (BX, yc + 0.03), 0.036, 0.088, 0.003, 'ahsap_koyu', z0=Z0 + 0.036)
for sy in (-1, 1):
    for sx in (-1, 1):
        y.silindir((BX + sx * 0.012, yc - 0.06 + sy * 0.02), 0.0018, Z0 + 0.018, Z0 + 0.034, 'ahsap', n=4)
kutu_merkez(y, (BX, yc - 0.06), 0.03, 0.05, 0.002, 'kumas', z0=Z0 + 0.034)
for sg in (-1, 1):   # steering oars at the stern
    cubuk(y, V(BX + sg * 0.018, yc + L - 0.03, Z0 + 0.03), V(BX + sg * 0.03, yc + L + 0.02, Z0 + 0.008), 0.003, 'ahsap')
# limestone roof beams still lying over the north end of the pit
for k in range(4):
    yy = BY1 - 0.035 - k * 0.032
    w_ = (BW + 0.03) * (1 - ((yy - yc) / ((BY1 - BY0) / 2)) ** 2) ** 0.5 + 0.02
    kutu_merkez(y, (BX, yy), max(0.04, w_), 0.028, 0.02, 'kirec', z0=Z0 + BH - 0.002, aci=0.02 * (k - 1.5))

# ---------------------------------------------------------------- construction ramp and the hauling gang
y.bolum('Insaat rampasi')
RCX = (RX0 + RX1) / 2
RY0 = -1.02
ZR = ZP + 0.165
yface = lambda z: PCY - W / 2 + (z - ZP) * (W / 2) / H
RY1 = yface(ZR) + 0.012
WT_, WB_ = 0.055, 0.085   # half widths top / bottom
zr = lambda yy: Z0 + (ZR - Z0) * (yy - RY0) / (RY1 - RY0)
A0, A1, B0, B1 = V(RCX - WT_, RY0, Z0 + 0.001), V(RCX + WT_, RY0, Z0 + 0.001), V(RCX - WT_, RY1, ZR), V(RCX + WT_, RY1, ZR)
y.yuz_yon([A0, A1, B1, B0], 'kerpic', Z)
for sg, (a_, b_) in ((-1, (A0, B0)), (1, (A1, B1))):
    g0, g1 = V(RCX + sg * WB_, RY0, Z0), V(RCX + sg * WB_, RY1, Z0)
    y.yuz_yon([g0, g1, b_, a_], 'kerpic_tugla', V(sg, 0, 0.6))
# the ramp's retaining edge courses and timber sleepers
for k in range(1, 14):
    yy = RY0 + (RY1 - RY0) * k / 14
    cubuk(y, V(RCX - WT_ + 0.004, yy, zr(yy) + 0.002), V(RCX + WT_ - 0.004, yy, zr(yy) + 0.002), 0.006, 'ahsap', 0.004)
for sg in (-1, 1):
    boru(y, [V(RCX + sg * (WT_ + 0.003), RY0 + 0.02, zr(RY0 + 0.02) + 0.003), V(RCX + sg * (WT_ + 0.003), RY1, ZR + 0.003)], 0.004, 'kerpic_koyu', n=5)
# the sledge with a casing block, its haulers up the ramp, the water pourer, the overseer
ramp_dir = math.atan2(RY1 - RY0, 0)
yk = RY0 + (RY1 - RY0) * 0.48
egim = math.atan2(ZR - Z0, RY1 - RY0)
kizak(RCX, yk, zr(yk), math.pi / 2, 'kirec')
# (lift the sledge's front: it sits on the slope)
ip_bas = V(RCX, yk + 0.035, zr(yk + 0.035) + 0.012)
for sg in (-1, 1):
    pts = [ip_bas + V(sg * 0.01, 0, 0)]
    for k in range(3):
        yy = yk + 0.075 + k * 0.045
        pts.append(V(RCX + sg * 0.018, yy, zr(yy) + 0.024))
    boru(y, pts, 0.0016, 'saz_koyu', n=4)
    for k in range(3):
        yy = yk + 0.075 + k * 0.045
        adam(RCX + sg * 0.024, yy - 0.012, zr(yy) + 0.001, math.pi / 2, egim=0.7, kol='ip')
adam(RCX + 0.01, yk + 0.05, zr(yk + 0.05), -math.pi / 2, egim=0.3, kol='testi')
adam(RCX - 0.1, RY0 + 0.04, Z0, math.pi * 0.4, egim=0.0, kol='asa', etek='boya_sari')
adam(RCX + 0.11, RY0 + 0.07, Z0, math.pi * 0.7, egim=0.1, kol='yan')
# the next sledge waiting at the ramp's foot with its gang, a scribe tallying the blocks
kizak(RCX + 0.005, RY0 - 0.06, Z0, math.pi / 2, 'kirec')
for k in range(3):
    for sg in (-1, 1):
        adam(RCX + sg * 0.05, RY0 - 0.08 + k * 0.03, Z0, math.pi / 2 + sg * 0.3, egim=0.2 * (k % 2), kol='yan' if k else 'ip')
with parca(y, (RCX - 0.15, RY0 - 0.04, Z0), 0.3):
    kutu_merkez(y, (0.02, 0), 0.018, 0.026, 0.012, 'ahsap_koyu')
    adam(0.0, 0.0, 0.0, 0.0, egim=0.15, kol='testi', etek='beyaz')
# blocks waiting at the top of the ramp, on the bare core
for k, (dx, key) in enumerate(((-0.035, 'kirec'), (0.03, 'kirec'))):
    kutu_merkez(y, (RCX + dx, RY1 - 0.015), 0.045, 0.03, 0.028, key, z0=ZR, aci=0.05 * k)
# a second sledge high on the ramp with its gang, the foremen with staffs at the top
yk2 = RY0 + (RY1 - RY0) * 0.8
kizak(RCX, yk2, zr(yk2), math.pi / 2, 'kirec')
for sg in (-1, 1):
    for k in range(2):
        yy = yk2 + 0.07 + k * 0.04
        if yy < RY1 - 0.04:
            adam(RCX + sg * 0.024, yy - 0.012, zr(yy) + 0.001, math.pi / 2, egim=0.7, kol='ip')
    adam(RCX + sg * 0.045, RY1 - 0.01, ZR, -math.pi / 2, egim=0.0, kol='asa', etek='boya_sari')
# a mud-brick stair up the ramp's west flank for the water carriers
for k in range(12):
    yy = RY0 + 0.03 + (RY1 - RY0 - 0.06) * k / 12
    zz = zr(yy)
    kutu_merkez(y, (RCX - WB_ - 0.012, yy), 0.022, (RY1 - RY0) / 12 + 0.002, max(0.004, zz - Z0), 'kerpic_tugla', z0=Z0)
for k in range(3):
    yy = RY0 + 0.15 + k * 0.17
    adam(RCX - WB_ - 0.012, yy, zr(yy), math.pi / 2, egim=0.3, kol='testi')
# palms of the valley edge where the causeway leaves the plateau
for (px, py, b) in ((-1.1, 0.47, 0.15), (-1.13, -0.22, 0.14), (1.1, -0.72, 0.16), (-0.25, -1.1, 0.15)):
    agac(y, px, py, Z0, b, 'palmiye')

# masons on the bare core steps setting casing blocks (levers, a block on rollers)
Rkz = lambda z: W / 2 * (1 - (z - ZP) / H)
for (i, u, k, a_, kol) in ((0, 0.3, 1, math.pi / 2, 'yan'), (0, 0.36, 3, math.pi * 0.1, 'ip'), (0, 0.72, 2, math.pi * 0.9, 'asa'),
                           (0, 0.78, 1, math.pi / 2, 'yan'), (3, 0.55, 1, 0.0, 'ip'), (3, 0.52, 2, -0.4, 'yan')):
    zz = ZP + (k + 1) * DZ
    r_ = Rkz(zz) - 0.012
    kose = [V(-1, -1), V(1, -1), V(1, 1), V(-1, 1)]
    p = V(PCX, PCY) + kose[i].lerp(kose[(i + 1) % 4], u) * r_
    adam(p.x, p.y, zz, a_ + (0 if i == 0 else -math.pi / 2), egim=0.5 if kol == 'ip' else 0.1, kol=kol)
for (i, u, k) in ((0, 0.33, 1), (0, 0.75, 1), (3, 0.58, 1)):
    zz = ZP + (k + 1) * DZ
    r_ = Rkz(zz) - 0.02
    kose = [V(-1, -1), V(1, -1), V(1, 1), V(-1, 1)]
    p = V(PCX, PCY) + kose[i].lerp(kose[(i + 1) % 4], u) * r_
    e_ = kose[(i + 1) % 4] - kose[i]
    kutu_merkez(y, (p.x, p.y), 0.045, 0.026, 0.026, 'kirec', z0=zz, aci=math.atan2(e_.y, e_.x))
    cubuk(y, V(p.x, p.y, zz + 0.004) + e_.normalized() * 0.03, V(p.x, p.y, zz + 0.03) + e_.normalized() * 0.05, 0.003, 'ahsap')

# ---------------------------------------------------------------- the block yard
y.bolum('Tas ocagi')
for (bx, by, w_, d_, h_, key, a_) in ((-0.62, -0.92, 0.07, 0.05, 0.04, 'kirec', 0.1), (-0.54, -0.93, 0.06, 0.05, 0.04, 'kirec', -0.05),
                                      (-0.58, -0.92, 0.065, 0.05, 0.035, 'kirec', 0.3), (-0.46, -1.02, 0.08, 0.05, 0.04, 'granit_kizil', 0.0),
                                      (-0.36, -1.0, 0.06, 0.045, 0.035, 'kirec', 0.2), (-0.66, -1.0, 0.05, 0.05, 0.04, 'kum', -0.2),
                                      (-0.27, -0.86, 0.055, 0.045, 0.035, 'kirec', 0.4)):
    zz = Z0 + (0.04 if (bx, by) == (-0.58, -0.92) else 0.0)
    kutu_merkez(y, (bx, by), w_, d_, h_, key, z0=zz, aci=a_)
kizak(-0.32, -0.94, Z0, 0.5, 'granit_kizil', 0.06, 0.04, 0.034)
for (ax, ay, a_, eg, kol) in ((-0.42, -0.9, 0.3, 0.4, 'yan'), (-0.5, -0.82, -1.2, 0.2, 'asa'), (-0.2, -0.98, 2.4, 0.6, 'ip'),
                              (-0.66, -0.97, 1.0, 0.5, 'yan')):
    adam(ax, ay, Z0, a_, egim=eg, kol=kol)
# a workers' awning
for (px, py) in ((-0.2, -0.78), (-0.1, -0.78), (-0.2, -0.86), (-0.1, -0.86)):
    y.silindir((px, py), 0.003, Z0, Z0 + 0.06, 'ahsap', n=4)
iki_yuzlu(y, [V(-0.215, -0.875, Z0 + 0.058), V(-0.085, -0.875, Z0 + 0.058), V(-0.085, -0.765, Z0 + 0.066), V(-0.215, -0.765, Z0 + 0.066)], 'kumas', Z)
for (px, py) in ((-0.17, -0.81), (-0.15, -0.83), (-0.13, -0.8)):
    donel(y, (px, py), [(0.006, Z0), (0.011, Z0 + 0.012), (0.01, Z0 + 0.024), (0.005, Z0 + 0.03), (0.006, Z0 + 0.034), (0, Z0 + 0.034)], 'kerpic_koyu', n=8)

# ---------------------------------------------------------------- mastaba fields
y.bolum('Mastabalar')


def mastaba(cx, cy, w, d, h, key='kirec', yon=0):
    """a mastaba tomb: a battered block with two false doors on its face yon (0: -y, 1: +x, 2: +y, 3: -x), an offering
    chapel against it, the burial shaft on top"""
    ix, iy = w * 0.08, d * 0.08
    B, T = egik_blok(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, Z0, h, ix, iy, key)
    i, j = yon, (yon + 1) % 4
    e = (B[j] - B[i]); L = e.length; e.normalize()
    nn = V(e.y, -e.x)
    up = (T[i] - B[i]) - e * (T[i] - B[i]).dot(e); up = up / h
    nf = (nn + Z * (ix if yon % 2 == 1 else iy) / h).normalized()
    Pm = lambda s_, t_, dd=0.002: B[i] + e * s_ + up * t_ + nf * dd
    for u in (0.22, 0.78):
        sc = L * u
        levha(Pm, sc - 0.022, sc + 0.022, 0.004, h * 0.82, key, nf, 0.003)
        levha(Pm, sc - 0.014, sc + 0.014, 0.004, h * 0.7, 'kirec' if key != 'kirec' else 'kum_acik', nf, 0.0045)
        levha(Pm, sc - 0.006, sc + 0.006, 0.004, h * 0.55, 'koyu', nf, 0.006)
        levha(Pm, sc - 0.016, sc + 0.016, h * 0.62, h * 0.68, 'koyu', nf, 0.0055)
    # the rounded coping along the top, an offering table and a libation jar before the second false door
    silme(y, T, Z0 + h - 0.006, 0.006, 0.003, key, 'yarim')
    c2 = B[i] + e * (L * 0.22) + nn * 0.014
    kutu_merkez(y, (c2.x, c2.y), 0.03, 0.016, 0.006, 'granit', z0=Z0, aci=math.atan2(e.y, e.x))
    donel(y, (c2.x + e.x * 0.008, c2.y + e.y * 0.008), [(0, Z0 + 0.006), (0.004, Z0 + 0.006), (0.005, Z0 + 0.013), (0.0025, Z0 + 0.017), (0, Z0 + 0.017)], 'kerpic_koyu', n=6)
    # the shaft and a low parapet on the roof
    m = (T[0] + T[2]) / 2
    kutu_merkez(y, (m.x, m.y), min(w, d) * 0.22, min(w, d) * 0.22, 0.003, 'koyu', z0=Z0 + h)
    # the offering chapel in front of one false door
    sc = L * 0.78
    c = B[i] + e * sc + nn * 0.03
    with parca(y, (c.x, c.y, Z0), math.atan2(e.y, e.x)):
        kutu(y, V(-0.025, -0.026, 0), X, 0.05, 0.06, h * 0.55, key, "onsagsolust")
        dikdortgen_acik(y, V(-0.025, -0.026), V(0.025, -0.026), 0, h * 0.55, 0.32, 0.68, 0.0, h * 0.38, (key, key, key, 'koyu'), derin=0.008)


def kult_avlu(x0, x1, y0, y1, h=0.024, t=0.009):
    """the mud-brick offering court before a mastaba's south end: three low walls, an open side towards -x with a
    door frame, a stela and an offering basin inside, a priest"""
    kutu(y, V(x0, y0, Z0), X, x1 - x0, t, h, 'kerpic', 'onarkasagsolust')                     # south
    kutu(y, V(x1, y0 + t, Z0), Y, y1 - y0 - t, t, h, 'kerpic', 'onarkasagust')                 # east
    for (ya, yb) in ((y0 + t, y0 + (y1 - y0) * 0.32), (y0 + (y1 - y0) * 0.68, y1)):          # west, a door between
        kutu(y, V(x0 + t, yb, Z0), -Y, yb - ya, t, h, 'kerpic', 'onarkasagsolust')
    boru(y, [V(x0, y0 + t / 2, Z0 + h), V(x1, y0 + t / 2, Z0 + h)], t * 0.5, 'kerpic_koyu', n=5)
    ym = (y0 + y1) / 2
    kutu_merkez(y, (x1 - t - 0.006, ym), 0.008, 0.03, 0.04, 'granit', z0=Z0)                   # the stela
    y.yuz_yon([V(x1 - t - 0.0105, ym - 0.011, Z0 + 0.026), V(x1 - t - 0.0105, ym + 0.011, Z0 + 0.026), V(x1 - t - 0.0105, ym + 0.011, Z0 + 0.034),
               V(x1 - t - 0.0105, ym - 0.011, Z0 + 0.034)], 'boya_sari', -X)
    kutu_merkez(y, (x1 - t - 0.03, ym), 0.016, 0.022, 0.006, 'kirec', z0=Z0)
    adam(x0 + (x1 - x0) * 0.45, ym + 0.01, Z0, 0.0, egim=0.2, kol='testi', etek='beyaz')


for k, my in enumerate((-0.47, -0.15, 0.17, 0.49)):
    mastaba(1.01, my, 0.15, 0.2, 0.065 + 0.012 * (k % 2), 'kirec' if k % 3 else 'kum', yon=3)
    kult_avlu(0.95, 1.075, my - 0.1 - 0.085, my - 0.1 - 0.012)
    # the burial shafts on the roof: stone curbs round two dark mouths
    for sy in (-0.05, 0.05):
        zm = Z0 + 0.065 + 0.012 * (k % 2)
        kutu_merkez(y, (1.01, my + sy), 0.03, 0.03, 0.004, 'kirec', z0=zm)
        kutu_merkez(y, (1.01, my + sy), 0.016, 0.016, 0.0045, 'koyu', z0=zm)
mastaba(1.01, 0.84, 0.13, 0.15, 0.05, 'kerpic_tugla', yon=3)
kult_avlu(0.95, 1.075, 0.66, 0.74)
for k, mx in enumerate((-0.55, -0.25, 0.05, 0.35)):
    mastaba(mx, 1.025, 0.24, 0.08, 0.05, 'kerpic_tugla' if k % 2 else 'kirec', yon=2)

# ---------------------------------------------------------------- the workers' village (Heit el-Ghurab)
y.bolum('Isci koyu')
VX0, VX1, VY0, VY1 = 0.3, 1.1, -1.1, -0.765
VT, VH = 0.014, 0.034          # compound wall thickness, height


def kerpic_mur(a, b, bas=True, son=True, kose_bas=False, h=VH):
    """a mud-brick compound wall, outer face on the line a->b (faces its right), rounded coping, a footing course"""
    a, b = V(a.x, a.y), V(b.x, b.y)
    e = (b - a).normalized()
    if kose_bas: a = a + e * VT
    yz = 'onarkaust' + ('sol' if bas and not kose_bas else '') + ('sag' if son else '')
    kutu(y, V(a.x, a.y, Z0), e, (b - a).length, VT, h, 'kerpic', yz)
    sol = V(-e.y, e.x)
    boru(y, [a + sol * (VT / 2) + Z * (Z0 + h), b + sol * (VT / 2) + Z * (Z0 + h)], VT * 0.5, 'kerpic_koyu', n=6)
    silme(y, [a, b], Z0, 0.006, 0.003, 'kerpic_koyu', 'duz', kapali=False)


GK0, GK1 = -0.965, -0.895      # the gate in the west wall, facing the ramp
VK = dikdortgen(VX0, VX1, VY0, VY1)
kerpic_mur(VK[0], VK[1])
kerpic_mur(VK[1], VK[2], kose_bas=True)
kerpic_mur(VK[2], VK[3], kose_bas=True)
kerpic_mur(VK[3], V(VX0, GK1), kose_bas=True)
kerpic_mur(V(VX0, GK0), VK[0] + Y * VT, son=False)   # (stops at the south wall's inner face: no doubled outer face)
# the gate: two posts with a palm-log lintel, an inspector's booth beside it
for gy in (GK0, GK1):
    kutu_merkez(y, (VX0 + VT / 2, gy), 0.022, 0.022, VH + 0.022, 'kerpic', z0=Z0)
    kutu_merkez(y, (VX0 + VT / 2, gy), 0.026, 0.026, 0.004, 'kerpic_koyu', z0=Z0 + VH + 0.022)
cubuk(y, V(VX0 + VT / 2, GK0 - 0.012, Z0 + VH + 0.03), V(VX0 + VT / 2, GK1 + 0.012, Z0 + VH + 0.03), 0.008, 'kutuk')


def galeri(x0, x1, y0, y1, h, yon):
    """a long barracks gallery of mud brick: a pillared porch along its street side (yon -1: -y, +1: +y) with
    alternating doors and small windows, high slit windows at the back, a flat roof of palm logs and matting with the
    log ends showing, a roof parapet"""
    K = dikdortgen(x0, x1, y0, y1)
    if yon < 0:
        fa, fb, ba, bb = K[0], K[1], K[2], K[3]
    else:
        fa, fb, ba, bb = K[2], K[3], K[0], K[1]
    n = max(3, round((x1 - x0) / 0.052))
    for k in range(n):
        kapi_ = k % 2 == 0
        dikdortgen_acik(y, fa.lerp(fb, k / n), fa.lerp(fb, (k + 1) / n), Z0, h, 0.32, 0.68, 0.0 if kapi_ else h * 0.42,
                        h * 0.7 if kapi_ else h * 0.7, ('kerpic', 'kerpic_koyu', 'kerpic', 'ahsap_koyu' if kapi_ else 'koyu'), derin=0.008)
    for k in range(n):
        dikdortgen_acik(y, ba.lerp(bb, k / n), ba.lerp(bb, (k + 1) / n), Z0, h, 0.38, 0.62, h * 0.66, h * 0.82,
                        ('kerpic', 'kerpic_koyu', 'kerpic', 'koyu'), derin=0.006)
    duz_duvar(y, fb, ba, Z0, Z0 + h, 'kerpic')
    duz_duvar(y, bb, fa, Z0, Z0 + h, 'kerpic')
    # the roof: matting, a mud parapet, palm-log ends along the front
    y.yuz_yon([V(p.x, p.y, Z0 + h) for p in K], 'saz', Z)
    parapet(y, K, Z0 + h, 0.006, 0, 0.006, 'kerpic_koyu')
    e = (fb - fa).normalized(); nf = V(e.y, -e.x)
    L = (fb - fa).length
    for k in range(int(L / 0.022)):
        p = fa + e * (0.011 + k * 0.022)
        cubuk(y, p + Z * (Z0 + h - 0.004) - nf * 0.002, p + Z * (Z0 + h - 0.004) + nf * 0.009, 0.004, 'kutuk')
    # the porch: square mud-brick piers, a log beam, a matting roof a little lower than the gallery's
    PD = 0.03
    ph = h - 0.009
    for k in range(n + 1):
        p = fa + e * (L * k / n) + nf * (PD - 0.005)
        kutu_merkez(y, (p.x, p.y), 0.009, 0.009, ph - Z0 * 0 - 0.0, 'kerpic', z0=Z0)
    pa, pb = fa + nf * (PD - 0.005), fb + nf * (PD - 0.005)
    cubuk(y, pa + Z * (Z0 + ph + 0.002), pb + Z * (Z0 + ph + 0.002), 0.006, 'kutuk')
    q0, q1 = fa + nf * 0.0, fb + nf * 0.0
    q2, q3 = fb + nf * (PD + 0.004), fa + nf * (PD + 0.004)
    zt = Z0 + ph + 0.005
    y.yuz_yon([q0 + Z * zt, q1 + Z * zt, q2 + Z * (zt - 0.003), q3 + Z * (zt - 0.003)], 'saz_koyu', Z)
    y.yuz_yon([q0 + Z * (zt - 0.003), q1 + Z * (zt - 0.003), q2 + Z * (zt - 0.006), q3 + Z * (zt - 0.006)], 'ahsap_koyu', -Z)
    y.yuz_yon([q3 + Z * (zt - 0.006), q2 + Z * (zt - 0.006), q2 + Z * (zt - 0.003), q3 + Z * (zt - 0.003)], 'saz_koyu', nf)
    for (qa, qb, ss) in ((q0, q3, -e), (q1, q2, e)):
        y.yuz_yon([qa + Z * (zt - 0.003), qb + Z * (zt - 0.006), qb + Z * (zt - 0.003), qa + Z * zt], 'saz_koyu', ss)
    return K


def silo(x, yy, r=0.022, h=0.062):
    """a domed mud granary: a filling hatch with a lid on top, an emptying hatch at the foot"""
    donel(y, (x, yy), [(r, Z0), (r * 1.04, Z0 + h * 0.5), (r * 0.9, Z0 + h * 0.76), (r * 0.5, Z0 + h * 0.94), (r * 0.18, Z0 + h)], 'kerpic', n=10)
    donel(y, (x, yy), [(r * 0.24, Z0 + h - 0.001), (r * 0.24, Z0 + h + 0.004), (0, Z0 + h + 0.004)], 'ahsap_koyu', n=6)
    kutu_merkez(y, (x, yy - r - 0.001), 0.01, 0.006, 0.012, 'koyu', z0=Z0 + 0.004)
    kutu_merkez(y, (x, yy - r - 0.002), 0.014, 0.005, 0.003, 'kutuk', z0=Z0 + 0.016)


def firin(x, yy, r=0.013):
    """a bell-shaped bread oven with its dark mouth"""
    donel(y, (x, yy), [(r, Z0), (r * 1.02, Z0 + 0.008), (r * 0.8, Z0 + 0.017), (r * 0.36, Z0 + 0.023), (r * 0.3, Z0 + 0.026), (0, Z0 + 0.026)], 'kerpic_koyu', n=9)
    kutu_merkez(y, (x, yy - r * 0.92), 0.009, 0.004, 0.008, 'koyu', z0=Z0 + 0.002)


def esek(x, yy, aci, yuk='testi'):
    """a donkey (built along +x, turned to aci) with panniers: 'testi' (water jars) or 'saz' (straw bales)"""
    with parca(y, (x, yy, Z0), aci):
        boru(y, [V(-0.015, 0, 0.022), V(0.011, 0, 0.023)], 0.0075, 'granit_koyu', n=6)
        for (lx, ly) in ((-0.011, -0.004), (-0.011, 0.004), (0.008, -0.004), (0.008, 0.004)):
            cubuk(y, V(lx, ly, 0.0), V(lx, ly, 0.02), 0.003, 'granit_koyu')
        boru(y, [V(0.011, 0, 0.024), V(0.019, 0, 0.035), V(0.028, 0, 0.033)], 0.0042, 'granit_koyu', n=5, r_son=0.0034)
        for sg in (-1, 1):
            cubuk(y, V(0.02, sg * 0.002, 0.039), V(0.021, sg * 0.004, 0.048), 0.0022, 'granit_koyu')
            if yuk == 'testi':
                donel(y, (-0.003, sg * 0.011), [(0, 0.012), (0.005, 0.013), (0.0065, 0.02), (0.003, 0.028), (0.0035, 0.031), (0, 0.031)], 'kerpic_koyu', n=6)
            else:
                kutu_merkez(y, (-0.003, sg * 0.011), 0.018, 0.008, 0.012, 'saz', z0=0.016)
        kutu_merkez(y, (-0.002, 0), 0.016, 0.017, 0.002, 'kumas', z0=0.029)


# the two galleries along the street, their roofs used for sleeping and drying
GA_ = galeri(0.33, 0.8, -0.86, -0.79, 0.05, -1)
GB_ = galeri(0.33, 0.8, -1.075, -1.0, 0.046, 1)
for (x0_, y0_, z_) in ((0.36, -0.835, 0.05), (0.62, -0.84, 0.05), (0.42, -1.05, 0.046), (0.7, -1.04, 0.046)):
    kutu_merkez(y, (x0_ + 0.03, y0_ + 0.012), 0.05, 0.022, 0.002, 'kumas' if x0_ < 0.5 else 'saz_koyu', z0=Z0 + z_)
for (x_, y_, z_) in ((0.5, -0.82, 0.05), (0.75, -1.03, 0.046)):
    for k in range(3):
        donel(y, (x_ + k * 0.012, y_), [(0, Z0 + z_), (0.005, Z0 + z_ + 0.001), (0.006, Z0 + z_ + 0.008), (0.003, Z0 + z_ + 0.014), (0, Z0 + z_ + 0.015)], 'kerpic_koyu', n=6)
# ladders up to the roofs
for (lx, ly, z_, s) in ((0.55, -0.885, 0.05, -1), (0.47, -0.975, 0.046, 1)):
    for sg in (-1, 1):
        cubuk(y, V(lx + sg * 0.006, ly, Z0), V(lx + sg * 0.006, ly - s * 0.012, Z0 + z_ + 0.008), 0.0025, 'ahsap')
    for k in range(5):
        t = (k + 0.5) / 5
        cubuk(y, V(lx - 0.006, ly - s * 0.012 * t, Z0 + (z_ + 0.008) * t), V(lx + 0.006, ly - s * 0.012 * t, Z0 + (z_ + 0.008) * t), 0.002, 'ahsap')

# the bakery court: low walls, bell ovens, a stack of bread moulds, the dough vats
BX0, BX1, BY0, BY1 = 0.85, 1.08, -1.08, -0.94
for (a, b) in ((V(BX0, BY1), V(BX0 + 0.08, BY1)), (V(BX0 + 0.13, BY1), V(BX1 - VT, BY1))):
    kutu(y, V(b.x, b.y, Z0), -X, (b - a).length, 0.01, 0.026, 'kerpic', 'onarkasagsolust')
kutu(y, V(BX0, BY0 + VT, Z0), Y, BY1 - BY0 - VT, 0.01, 0.026, 'kerpic', 'onarkasagsolust')
for (fx, fy) in ((0.9, -1.05), (0.93, -1.05), (0.96, -1.05), (0.99, -1.05), (1.02, -1.05)):
    firin(fx, fy)
for k in range(4):   # stacked conical bread moulds
    for m in range(3 - k // 2):
        donel(y, (0.91 + m * 0.012 + k * 0.003, -0.975), [(0, Z0 + k * 0.007), (0.005, Z0 + k * 0.007), (0.002, Z0 + k * 0.007 + 0.01), (0, Z0 + k * 0.007 + 0.011)], 'kerpic', n=6)
for (vx, vy) in ((1.0, -0.99), (1.04, -0.99)):
    donel(y, (vx, vy), [(0, Z0), (0.012, Z0), (0.015, Z0 + 0.014), (0.013, Z0 + 0.016), (0, Z0 + 0.012)], 'kerpic_koyu', n=9)
# the granary court: domed silos, a stair onto the roof of the store, the scribe counting the sacks
for (sx_, sy_) in ((0.885, -0.82), (0.935, -0.82), (0.985, -0.82), (1.035, -0.82)):
    silo(sx_, sy_)
kutu(y, V(0.86, -0.91, Z0), X, 0.2, 0.05, 0.03, 'kerpic', 'onarkasagsolust')
y.yuz_yon([V(0.86, -0.91, Z0 + 0.03), V(1.06, -0.91, Z0 + 0.03), V(1.06, -0.86, Z0 + 0.03), V(0.86, -0.86, Z0 + 0.03)], 'saz', Z)
for k in range(4):
    kutu_merkez(y, (0.88 + k * 0.05, -0.91 - 0.0005), 0.014, 0.004, 0.02, 'koyu', z0=Z0)
merdiven(y, (1.075, -0.925), math.pi / 2, 0.016, Z0, Z0 + 0.03, n=4, key='kerpic')
for k in range(5):
    kutu_merkez(y, (0.885 + k * 0.016, -0.88), 0.012, 0.01, 0.008, 'kumas', z0=Z0 + 0.03, aci=0.3 * k)
# life in the street: donkeys with jars and straw, water carriers, bakers at the ovens, a scribe
esek(0.42, -0.93, 0.1, 'testi'); esek(0.66, -0.94, math.pi + 0.2, 'saz'); esek(0.25, -0.94, -0.2, 'testi')
for (ax, ay, a_, eg, kol, et) in ((0.45, -0.9, math.pi, 0.1, 'testi', 'beyaz'), (0.58, -0.95, 0.0, 0.2, 'yan', 'beyaz'),
                                  (0.72, -0.92, math.pi / 2, 0.0, 'asa', 'boya_sari'), (0.92, -1.02, -math.pi / 2, 0.5, 'yan', 'beyaz'),
                                  (0.97, -1.02, -math.pi / 2, 0.4, 'ip', 'beyaz'), (1.02, -0.97, math.pi, 0.3, 'testi', 'beyaz'),
                                  (0.9, -0.88, -math.pi / 2, 0.1, 'asa', 'boya_sari'), (0.36, -0.95, 0.3, 0.0, 'yan', 'beyaz')):
    adam(ax, ay, Z0, a_, egim=eg, kol=kol, etek=et)
# a shade awning over the street's cooking hearth
for (px, py) in ((0.6, -0.895), (0.68, -0.895), (0.6, -0.965), (0.68, -0.965)):
    y.silindir((px, py), 0.0025, Z0, Z0 + 0.05, 'ahsap', n=4)
iki_yuzlu(y, [V(0.592, -0.973, Z0 + 0.05), V(0.688, -0.973, Z0 + 0.05), V(0.688, -0.887, Z0 + 0.055), V(0.592, -0.887, Z0 + 0.055)], 'kumas', Z)
donel(y, (0.64, -0.93), [(0, Z0), (0.012, Z0), (0.012, Z0 + 0.006), (0, Z0 + 0.006)], 'kaya_koyu', n=8)
donel(y, (0.64, -0.93), [(0, Z0 + 0.006), (0.009, Z0 + 0.007), (0.01, Z0 + 0.018), (0.008, Z0 + 0.02), (0, Z0 + 0.02)], 'bronz', n=8)

# ---------------------------------------------------------------- the quarry face at the plateau's edge
y.bolum('Ocak')
QX0, QX1 = -0.76, -0.3
# a stepped ledge of the plateau rock with blocks being cut out of its benches
for k, (qy0, qy1, qh) in enumerate(((-1.128, -1.095, 0.05), (-1.095, -1.07, 0.034), (-1.07, -1.055, 0.016))):
    xa = QX0 + k * 0.03
    kutu(y, V(xa, qy0, Z0), X, QX1 - xa - k * 0.05, qy1 - qy0, qh, 'kaya' if k == 0 else 'kum', 'onarkasagsolust')
    # the trenches round half-cut blocks on the bench top
    xx = xa + 0.02
    while xx < QX1 - k * 0.05 - 0.05:
        y.yuz_yon([V(xx, qy0 + 0.004, Z0 + qh + 0.0005), V(xx + 0.004, qy0 + 0.004, Z0 + qh + 0.0005), V(xx + 0.004, qy1 - 0.003, Z0 + qh + 0.0005),
                   V(xx, qy1 - 0.003, Z0 + qh + 0.0005)], 'kum_koyu', Z)
        xx += 0.045 + 0.01 * (k % 2)
# blocks prised off the face, levers, quarrymen with mallets
for (bx, by, a_) in ((-0.7, -1.04, 0.1), (-0.52, -1.045, -0.15), (-0.41, -1.04, 0.3)):
    kutu_merkez(y, (bx, by), 0.04, 0.026, 0.024, 'kum', z0=Z0, aci=a_)
for (ax, ay, a_, eg, kol) in ((-0.62, -1.05, math.pi / 2, 0.6, 'asa'), (-0.47, -1.05, math.pi / 2, 0.7, 'ip'), (-0.36, -1.03, 2.2, 0.3, 'asa')):
    adam(ax, ay, Z0, a_, egim=eg, kol=kol)
cubuk(y, V(-0.56, -1.06, Z0 + 0.016), V(-0.54, -1.03, Z0 + 0.004), 0.0028, 'ahsap')
# timber and rope stores, a water-jar line under a second awning
for k in range(4):
    boru(y, [V(-0.3 + k * 0.004, -0.74 - k * 0.011, Z0 + 0.004 + 0.006 * (k // 2)), V(-0.17 + k * 0.004, -0.74 - k * 0.011, Z0 + 0.004 + 0.006 * (k // 2))], 0.0045, 'kutuk', n=6)
for (rx, ry) in ((-0.14, -0.76), (-0.12, -0.745)):
    donel(y, (rx, ry), [(0.004, Z0), (0.011, Z0), (0.011, Z0 + 0.006), (0.004, Z0 + 0.006), (0.004, Z0)], 'saz_koyu', n=8)
for (px, py) in ((-0.46, -0.8), (-0.37, -0.8), (-0.46, -0.86), (-0.37, -0.86)):
    y.silindir((px, py), 0.003, Z0, Z0 + 0.055, 'ahsap', n=4)
iki_yuzlu(y, [V(-0.468, -0.868, Z0 + 0.054), V(-0.362, -0.868, Z0 + 0.054), V(-0.362, -0.792, Z0 + 0.06), V(-0.468, -0.792, Z0 + 0.06)], 'kumas', Z)
for k in range(5):
    donel(y, (-0.45 + k * 0.018, -0.83), [(0, Z0), (0.006, Z0 + 0.003), (0.008, Z0 + 0.014), (0.004, Z0 + 0.022), (0.0045, Z0 + 0.026), (0, Z0 + 0.026)], 'kerpic_koyu', n=7)
adam(-0.4, -0.85, Z0, -math.pi / 2, egim=0.4, kol='testi')

calistir(y, 'lm_piramit')
