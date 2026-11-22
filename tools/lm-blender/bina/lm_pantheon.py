# Pantheon (lm_pantheon): the brick rotunda in three cornice-divided zones with relieving-arch niches, the stepped
# rings and the lead-sheeted concrete dome with its open oculus; the intermediate block with its "ghost" upper
# pediment; the deep Corinthian portico (8 granite columns in front, 16 in all, bronze-lettered frieze, pediment with
# a wreath, bronze doors between apse niches) on a stepped podium, in a paved piazza with statues and stone pines.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.05                      # piazza top
C = (0.0, 0.30)                # rotunda centre
R = 0.74                       # rotunda outer radius
N = 48                         # rotunda sides
ZW = Z0 + 0.74                 # rotunda wall top
Z1, Z2 = Z0 + 0.25, Z0 + 0.50  # the two lower cornices
PX = 0.43                      # portico column centres x -PX..PX
PY0, PY1 = -0.955, -0.52       # front column line, block face
ZS = Z0 + 0.045                # stylobate top
HC = 0.32                      # column height
ZC = ZS + HC
HE = HC * 0.26                 # entablature height
ZE = ZC + HE
D = 0.034                      # entablature half depth
BX, BY1 = 0.49, -0.2           # intermediate block half width, back (inside the rotunda)
ZB = Z0 + 0.62                 # block top


def seg_quad(o, ex, n, p, q, w, key):
    """a flat stroke from p to q (2D, in the plane o + ex u + z v), w wide, facing n"""
    p, q = V(*p), V(*q)
    d = (q - p); L = d.length
    if L < 1e-9: return
    d /= L; s = V(-d.y, d.x) * (w / 2)
    P = lambda t: o + ex * t.x + Z * t.y + n * 0.0015
    y.yuz_yon([P(p - s - d * w * 0.3), P(q - s + d * w * 0.3), P(q + s + d * w * 0.3), P(p + s - d * w * 0.3)], key, n)


GLIF = {
    'M': [((0, 0), (0, 1)), ((0, 1), (0.3, 0.35)), ((0.3, 0.35), (0.6, 1)), ((0.6, 1), (0.6, 0))],
    'A': [((0, 0), (0.3, 1)), ((0.3, 1), (0.6, 0)), ((0.13, 0.38), (0.47, 0.38))],
    'G': [((0.6, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (0.6, 0)), ((0.6, 0), (0.6, 0.45)), ((0.6, 0.45), (0.32, 0.45))],
    'R': [((0, 0), (0, 1)), ((0, 1), (0.55, 1)), ((0.55, 1), (0.55, 0.5)), ((0.55, 0.5), (0, 0.5)), ((0.2, 0.5), (0.6, 0))],
    'I': [((0.15, 0), (0.15, 1))],
    'P': [((0, 0), (0, 1)), ((0, 1), (0.55, 1)), ((0.55, 1), (0.55, 0.5)), ((0.55, 0.5), (0, 0.5))],
    'L': [((0, 1), (0, 0)), ((0, 0), (0.55, 0))],
    'F': [((0, 0), (0, 1)), ((0, 1), (0.55, 1)), ((0, 0.5), (0.42, 0.5))],
    'C': [((0.6, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (0.6, 0))],
    'O': [((0, 0), (0, 1)), ((0, 1), (0.6, 1)), ((0.6, 1), (0.6, 0)), ((0.6, 0), (0, 0))],
    'S': [((0.6, 1), (0, 1)), ((0, 1), (0, 0.5)), ((0, 0.5), (0.6, 0.5)), ((0.6, 0.5), (0.6, 0)), ((0.6, 0), (0, 0))],
    'T': [((0, 1), (0.6, 1)), ((0.3, 1), (0.3, 0))],
    'E': [((0.6, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (0.6, 0)), ((0, 0.5), (0.45, 0.5))],
    'V': [((0, 1), (0.3, 0)), ((0.3, 0), (0.6, 1))],
    '.': [((0.12, 0.42), (0.12, 0.58))],
}


def yazi(o, ex, n, metin, h, key='bronz'):
    """bronze capital letters (simple stroke font) along ex from o, h high, centred on o"""
    gen = lambda ch: 0.3 if ch == '.' else (0.3 if ch == 'I' else 0.6)
    bos = 0.32
    W = sum(gen(c) + bos for c in metin) - bos
    u = -W * h / 2
    for ch in metin:
        for p, q in GLIF[ch]:
            seg_quad(o, ex, n, (u + p[0] * h, p[1] * h), (u + q[0] * h, q[1] * h), h * 0.15, key)
        u += (gen(ch) + bos) * h


def heykel(x, yy, z, s=1.0, aci=-math.pi / 2):
    """a statue on a moulded pedestal: a draped bronze figure"""
    kutu_merkez(y, (x, yy), 0.07 * s, 0.07 * s, 0.012 * s, 'mermer', z0=z)
    kutu_merkez(y, (x, yy), 0.056 * s, 0.056 * s, 0.07 * s, 'kirec', z0=z + 0.012 * s)
    kornis(y, x - 0.028 * s, x + 0.028 * s, yy - 0.028 * s, yy + 0.028 * s, z + 0.075 * s, 0.008 * s, 0.006 * s, 'mermer', 'tac')
    zt = z + 0.083 * s
    donel(y, (x, yy), [(0.016 * s, zt), (0.018 * s, zt + 0.02 * s), (0.013 * s, zt + 0.06 * s), (0.015 * s, zt + 0.075 * s),
                       (0.009 * s, zt + 0.085 * s), (0, zt + 0.087 * s)], 'bronz', n=10)
    kure(y, (x, yy, zt + 0.097 * s), 0.009 * s, 'bronz', n=8, kat=4)
    e = V(math.cos(aci), math.sin(aci))
    boru(y, [V(x, yy, zt + 0.07 * s) + V(-e.y, e.x) * 0.012 * s, V(x, yy, zt + 0.07 * s) + V(-e.y, e.x) * 0.02 * s + e * 0.02 * s + Z * 0.03 * s],
         0.003 * s, 'bronz', n=5)


def pinus(x, yy, z, boy=0.22, s=1.0):
    """an Italian stone pine: a leaning bare trunk forking under a wide, flat umbrella crown of several lumps"""
    top = V(x + 0.02 * s, yy + 0.01 * s, z + boy)
    fork = V(x + 0.012 * s, yy + 0.004 * s, z + boy * 0.72)
    boru(y, [V(x, yy, z), V(x + 0.006 * s, yy, z + boy * 0.4), fork], 0.0075 * s, 'ahsap', n=6, r_son=0.005 * s)
    lumps = [(0, 0, 0.06, 0.034)] + [(0.055 * math.cos(TAU * k / 5 + 0.4), 0.055 * math.sin(TAU * k / 5 + 0.4), 0.045, 0.026) for k in range(5)]
    for dx, dy, r, h in lumps:
        c = V(top.x + dx * s, top.y + dy * s)
        zz = top.z - (0.0 if dx == 0 else 0.008 + 0.004 * math.sin(dx * 90))
        if dx: boru(y, [fork, V(c.x, c.y, zz - 0.004)], 0.0035 * s, 'ahsap', n=5, r_son=0.002 * s)
        donel(y, (c.x, c.y), [(0.0, zz - 0.006), (r * s * 0.75, zz - 0.002), (r * s, zz + h * 0.3), (r * s * 0.85, zz + h * 0.7), (0, zz + h)],
              'cimen', n=12)


# ================================================================ piazza
y.bolum('Meydan')
zemin(y, -0.93, 0.93, -1.2, 1.15, Z0, 'tas_koyu', basamak=(('on', 0.9),), n_basamak=3)
# a paving border and a pattern of slabs in front of the portico
for k in range(7):
    xx = -0.72 + k * 0.24
    y.yuz([V(xx - 0.1, -1.17, Z0 + 0.0015), V(xx + 0.1, -1.17, Z0 + 0.0015), V(xx + 0.1, -1.13, Z0 + 0.0015), V(xx - 0.1, -1.13, Z0 + 0.0015)], 'mermer')
for sx in (-1, 1):
    heykel(sx * 0.665, -1.02, Z0, 1.15)
    pinus(sx * 0.78, 0.98, Z0, 0.25, 1.15)
    pinus(sx * 0.8, -0.3, Z0, 0.21, 0.95)
    # bollards along the piazza edge
    for k in range(4):
        y.prizma((sx * 0.62, -0.86 + k * 0.1), 0.008, Z0, Z0 + 0.03, 'kirec', n=8)
        kure(y, (sx * 0.62, -0.86 + k * 0.1, Z0 + 0.033), 0.009, 'kirec', n=8, kat=4)

# ================================================================ forecourt porticoes
# (in Roman times the Pantheon stood at the head of a long colonnaded court: a portico ran down each side)
y.bolum('Ön avlu revakları')
FY0_, FY1_ = -1.13, -0.46      # colonnade ends
for sx in (-1, 1):
    xc, xw, xo = sx * 0.79, sx * 0.905, sx * 0.92      # column line, wall inner / outer face
    ZS_ = Z0 + 0.015
    kutu(y, V(min(xc, xo) - 0.025 * (sx > 0) - 0.0, FY0_ - 0.025, Z0), X, abs(xo - xc) + 0.025, FY1_ - FY0_ + 0.05, 0.015, 'mermer',
         'onarkasagsolust')
    a, b = (V(xc, FY1_), V(xc, FY0_)) if sx > 0 else (V(xc, FY0_), V(xc, FY1_))
    zt = sutunlu_revak(y, a, b, 7, ZS_, 0.2, tur='iyon', r=0.011, key='mermer', derin=0.034)
    # back wall: blind arched niches outside, plaster with painted panels inside
    ao, bo = (V(xo, FY0_ - 0.02), V(xo, FY1_ + 0.02)) if sx > 0 else (V(xo, FY1_ + 0.02), V(xo, FY0_ - 0.02))
    pencereli_duvar(y, [ao, bo], ZS_, zt + 0.056 - ZS_, [7], kapali=False, renk=('tugla_roma', 'tugla_roma_koyu', 'kirec', 'tugla_roma_koyu'), v0=0.03,
                    en=0.5, ust=0.09, derin=0.012, k_say=8, sivri=0.0, cerceve=(0.006, 'kirec'))
    silme(y, [ao, bo], ZS_, 0.016, 0.008, 'kirec', 'kaide', kapali=False)
    ai, bi = (V(xw, FY1_ + 0.02), V(xw, FY0_ - 0.02)) if sx > 0 else (V(xw, FY0_ - 0.02), V(xw, FY1_ + 0.02))
    duz_duvar(y, ai, bi, ZS_, zt, 'siva_krem')
    for k in range(7):
        p = ai.lerp(bi, (k + 0.5) / 7); e_ = (bi - ai).normalized()
        y.yuz_yon([p - e_ * 0.03 + V(-sx * 0.0015, 0, ZS_ + 0.05), p + e_ * 0.03 + V(-sx * 0.0015, 0, ZS_ + 0.05),
                   p + e_ * 0.03 + V(-sx * 0.0015, 0, ZS_ + 0.16), p - e_ * 0.03 + V(-sx * 0.0015, 0, ZS_ + 0.16)], 'siva_kirmizi', V(-sx, 0))
    for yy, s_ in ((FY0_ - 0.02, -1), (FY1_ + 0.02, 1)):     # wall ends
        a_, b_ = (V(xw, yy), V(xo, yy)) if (s_ * sx) < 0 else (V(xo, yy), V(xw, yy))
        duz_duvar(y, a_, b_, ZS_, zt + 0.056, 'tugla_roma')   # (up to the back wall's top: above the inner face it was open)
    # a lean-to tiled roof from the colonnade up to the back wall, the coffered ceiling
    xi_ = xc - sx * 0.022
    zr = zt + 0.004
    for yy0, yy1 in ((FY0_ - 0.035, FY1_ + 0.035),):
        pts = [V(xi_, yy0, zr), V(xi_, yy1, zr), V(xo + sx * 0.012, yy1, zr + 0.055), V(xo + sx * 0.012, yy0, zr + 0.055)]
        y.yuz_yon(pts, 'kiremit', Z)
        y.yuz_yon([V(xi_, yy0, zr - 0.006), V(xi_, yy1, zr - 0.006), V(xi_, yy1, zr), V(xi_, yy0, zr)], 'ahsap_koyu', V(-sx, 0))
        for yy in (yy0, yy1):
            iki_yuzlu(y, [V(xi_, yy, zr - 0.006), V(xo + sx * 0.012, yy, zr - 0.006), V(xo + sx * 0.012, yy, zr + 0.055), V(xi_, yy, zr)], 'kirec',
                      V(0, 1 if yy == yy1 else -1))   # (the far end faces +y; two-sided: seen from inside the aisle too)
        iki_yuzlu(y, [V(xi_, yy0, zr - 0.006), V(xi_, yy1, zr - 0.006), V(xw, yy1, zr - 0.006), V(xw, yy0, zr - 0.006)],
                  'ahsap_koyu', -Z)   # (two-sided: its top shows under the lean-to's end)
        nr = int((yy1 - yy0) / 0.024)
        for j in range(nr + 1):
            yy = yy0 + (yy1 - yy0) * j / nr
            cubuk(y, V(xi_, yy, zr + 0.003), V(xo + sx * 0.012, yy, zr + 0.058), 0.0055, 'kiremit2', 0.004)
        y.yuz_yon([V(xo + sx * 0.012, yy0, zr + 0.047), V(xo + sx * 0.012, yy1, zr + 0.047), V(xo + sx * 0.012, yy1, zr + 0.055),
                   V(xo + sx * 0.012, yy0, zr + 0.055)], 'ahsap_koyu', V(sx, 0))
        y.yuz_yon([V(xo, yy0, zr + 0.047), V(xo, yy1, zr + 0.047), V(xo + sx * 0.012, yy1, zr + 0.047), V(xo + sx * 0.012, yy0, zr + 0.047)],
                  'ahsap_koyu', -Z)
    iki_yuzlu(y, [V(xc + sx * 0.02, FY0_, ZS_ + 0.2), V(xc + sx * 0.02, FY1_, ZS_ + 0.2), V(xw, FY1_, ZS_ + 0.2), V(xw, FY0_, ZS_ + 0.2)], 'kirec', -Z)   # (two-sided: seen from above past the aisle roof)

# ================================================================ rotunda
y.bolum('Rotunda: üç kuşaklı tuğla duvar')
ring = cokgen(C, R, N, kat=math.pi / N)
silme(y, cokgen(C, R, N, kat=math.pi / N), Z0, 0.03, 0.02, 'kirec', 'kaide')
ARK = ('tugla_roma', 'tugla_roma_koyu', 'kirec', 'tugla_roma_koyu')
# zone 1: tall blind relieving arches in every other bay
pencereli_duvar(y, ring, Z0 + 0.03, Z1 - Z0 - 0.03, [1 if i % 2 == 0 else 0 for i in range(N)], renk=ARK, v0=0.02, en=0.56, ust=0.035,
                derin=0.016, k_say=8, sivri=0.0, cerceve=(0.007, ['kirec', 'tugla_roma_koyu']))
# zone 2: arched windows framed in stone, every other bay (offset)
pencereli_duvar(y, ring, Z1, Z2 - Z1, [1 if i % 2 == 1 else 0 for i in range(N)], renk=('tugla_roma', 'tugla_roma_koyu', 'kirec', 'cam'), v0=0.06,
                en=0.42, ust=0.05, derin=0.02, k_say=8, sivri=0.0, cerceve=(0.006, 'kirec'))
# zone 3 (attic): low square windows
for i in range(N):
    a, b = ring[i], ring[(i + 1) % N]
    if i % 3 == 1:
        dikdortgen_acik(y, a, b, Z2, ZW - Z2, 0.3, 0.7, 0.08, 0.15, ('tugla_roma', 'tugla_roma_koyu', 'kirec', 'koyu'), derin=0.014,
                        cerceve=(0.005, 'kirec'))
    else:
        duz_duvar(y, a, b, Z2, ZW, 'tugla_roma')
# cornices: the two string courses and the great crowning cornice with dentils
y.bolum('Rotunda kornişleri')
silme(y, ring, Z1 - 0.012, 0.02, 0.016, 'kirec', 'tac')
silme(y, ring, Z2 - 0.012, 0.02, 0.016, 'kirec', 'tac')
silme(y, ring, ZW - 0.008, 0.016, 0.012, 'kirec', 'kaba')
for i in range(N * 3):        # dentils under the crowning cornice
    t = math.pi / N + TAU * (i + 0.5) / (N * 3)
    nn = V(math.cos(t), math.sin(t)); e = V(-nn.y, nn.x)
    p = V(C[0], C[1]) + nn * R
    kutu(y, p - e * 0.006 + nn * 0.012 + Z * (ZW + 0.008), e, 0.012, 0.012, 0.01, 'kirec', 'onsagsolust')
ZK = ZW + 0.018
duvarlar(y, ring, ZW, ZK, 'kirec')
silme(y, ring, ZK, 0.022, 0.03, 'mermer', 'tac')
ZK += 0.022

# ================================================================ dome
y.bolum('Kubbe: basamaklı halkalar')
pr = [(R, ZK), (R - 0.01, ZK)]
r, z = R - 0.01, ZK
for k in range(7):            # the step rings
    z += 0.024
    pr.append((r, z))
    r -= 0.026 if k < 6 else 0.0
    pr.append((r, z))
donel(y, C, pr, 'kirec', n=N, kat=math.pi / N)
# lead sheets: a flat spherical cap from the last step to the oculus
y.bolum('Kubbe: kurşun kaplama ve oculus')
rs, zs = r, z
RO, ZT = 0.11, ZK + 0.33
zc = ((rs * rs + zs * zs) - (RO * RO + ZT * ZT)) / (2 * (zs - ZT))
rho = math.hypot(rs, zs - zc)
a0, a1 = math.asin(rs / rho), math.asin((RO + 0.018) / rho)
cap = [(rs, zs)] + [(rho * math.sin(a0 + (a1 - a0) * k / 10), zc + rho * math.cos(a0 + (a1 - a0) * k / 10)) for k in range(1, 11)]
donel(y, C, cap, 'kursun', n=64, dilim=['kursun', 'kursun2'])
zo = cap[-1][1]
# the oculus: a bronze lip and the dark opening
donel(y, C, [(RO + 0.018, zo), (RO + 0.018, zo + 0.01), (RO, zo + 0.01)], 'bronz', n=32)
donel(y, C, [(RO, zo + 0.01), (RO, zo - 0.06)], 'kirec', n=32)       # (wound inward: the shaft's inner face)
y.yuz_yon([V(C[0] + RO * math.cos(TAU * i / 32), C[1] + RO * math.sin(TAU * i / 32), zo - 0.06) for i in range(32)], 'koyu', Z)

# ================================================================ intermediate block
y.bolum('Ara blok ve üst alınlık')
# sides: brick with two tiers of tall niches and the rotunda's string courses carried across
for sx in (-1, 1):
    a, b = (V(-BX, BY1), V(-BX, PY1)) if sx < 0 else (V(BX, PY1), V(BX, BY1))
    duz_duvar(y, a, b, Z0, Z0 + 0.03, 'kirec')
    for z0, h in ((Z0 + 0.03, Z1 - Z0 - 0.03), (Z1, Z2 - Z1)):
        y.kemerli(a, b, z0, h, ARK, v0=0.03, en=0.5, ust=0.04, derin=0.03, k_say=8, cerceve=(0.007, ['kirec', 'tugla_roma_koyu']))
    duz_duvar(y, a, b, Z2, ZB, 'tugla_roma')
    silme(y, [a, b], Z1 - 0.012, 0.02, 0.016, 'kirec', 'tac', kapali=False)
    silme(y, [a, b], Z2 - 0.012, 0.02, 0.016, 'kirec', 'tac', kapali=False)
# front face above the portico (brick), with the block's crowning cornice across front and sides
duz_duvar(y, V(-BX, PY1), V(BX, PY1), ZC, ZB, 'tugla_roma')
duz_duvar(y, V(-BX, PY1), V(-PX - D - 0.01, PY1), Z0, ZC, 'tugla_roma')
duz_duvar(y, V(PX + D + 0.01, PY1), V(BX, PY1), Z0, ZC, 'tugla_roma')
silme(y, [V(-BX, BY1), V(-BX, PY1), V(BX, PY1), V(BX, BY1)], ZB - 0.022, 0.022, 0.016, 'kirec', 'tac', kapali=False)
# the ghost pediment: a stone raking cornice on brick, its roof running back into the rotunda
alinlik(y, V(-BX - 0.012, PY1 - 0.012), V(BX + 0.012, PY1 - 0.012), ZB, 0.125, derin=0.34, key='kirec', ic_key='tugla_roma', c=0.012,
        cati_key='kursun')
for j in range(9):            # standing seams on the block roof
    yy = PY1 + 0.03 + 0.26 * j / 8
    for s_ in (-1, 1):
        cubuk(y, V(s_ * (BX + 0.012), yy, ZB + 0.0136), V(0, yy, ZB + 0.125 + 0.0136), 0.006, 'kursun2', 0.006)

# ================================================================ portico
y.bolum('Portiko: basamaklı kaide')
for k, (w, d0, h) in enumerate(((0.56, 0.12, 0.015), (0.535, 0.095, 0.03), (0.51, 0.07, 0.045))):
    kutu(y, V(-w, PY0 - d0, Z0), X, 2 * w, PY1 - (PY0 - d0), h, 'mermer' if k == 2 else 'kirec', 'onsagsolust')
y.bolum('Portiko: Korint sütunları')
XS = [-PX + 2 * PX * i / 7 for i in range(8)]
YM, YB = -0.80, -0.645
for xx in XS:
    sutun(y, xx, PY0, ZS, ZC, 0.02, 'granit', 'korint', bas_key='mermer')
for yy in (YM, YB):
    for i in (0, 2, 5, 7):
        sutun(y, XS[i], yy, ZS, ZC, 0.02, 'granit_koyu' if i in (2, 5) else 'granit', 'korint', bas_key='mermer')
# pilasters (antae) on the block face behind the columns
for i in (0, 2, 5, 7):
    xx = XS[i]
    kutu(y, V(xx - 0.02, PY1 - 0.008, ZS), X, 0.04, 0.008, HC, 'mermer', 'onsagsol')
    kutu(y, V(xx - 0.026, PY1 - 0.014, ZC - 0.03), X, 0.052, 0.014, 0.03, 'mermer', 'onsagsolust')

y.bolum('Portiko: arka duvar, tunç kapı, nişler')
XD = 0.13
# central door bay between the inner columns
W_, e_, nc_, L_ = dikdortgen_acik(y, V(-XD - 0.08, PY1), V(XD + 0.08, PY1), ZS, HC, 0.27, 0.73, 0.0, 0.26,
                                  ('kirec', 'mermer', 'mermer', 'bronz'), derin=0.03, cerceve=(0.014, 'mermer'))
kafes(y, V(-XD - 0.08, PY1 + 0.03), V(XD + 0.08, PY1 + 0.03), ZS, 0.27, 0.73, 0.2, 0.26, 'bronz', nu=6, nv=2, en=0.004, ileri=0.003)
dw = 0.0025
y.yuz_yon([L_(0.498, 0.0, 0.0285), L_(0.502, 0.0, 0.0285), L_(0.502, 0.195, 0.0285), L_(0.498, 0.195, 0.0285)], 'koyu', nc_)
for uu in (0.335, 0.435, 0.565, 0.665):           # door panels and studs
    for vv in (0.04, 0.12):
        y.yuz_yon([L_(uu - 0.04, vv, 0.028), L_(uu + 0.04, vv, 0.028), L_(uu + 0.04, vv + 0.06, 0.028), L_(uu - 0.04, vv + 0.06, 0.028)],
                  'bronz', nc_)
# side bays: apse niches with statues of Augustus and Agrippa
for s in (-1, 1):
    a, b = (V(-PX - D - 0.01, PY1), V(-XD - 0.08, PY1)) if s < 0 else (V(XD + 0.08, PY1), V(PX + D + 0.01, PY1))
    y.kemerli(a, b, ZS, HC, ('kirec', 'kirec', 'mermer', 'tas_koyu'), v0=0.05, en=0.42, ust=0.05, derin=0.05, k_say=10,
              cerceve=(0.01, 'mermer'))
    m = (a + b) / 2
    heykel(m.x, PY1 + 0.03, ZS + 0.05, 0.72)
y.yuz_yon([V(-PX - D, PY0 + D, ZC + HE * 0.4), V(PX + D, PY0 + D, ZC + HE * 0.4), V(PX + D, PY1, ZC + HE * 0.4), V(-PX - D, PY1, ZC + HE * 0.4)],
          'kirec', -Z)   # the ceiling

y.bolum('Portiko: saçaklık, tunç yazıt, dişler')
ox0, ox1, oy0 = -PX - D, PX + D, PY0 - D
ix0, ix1, iy0 = -PX + D, PX - D, PY0 + D
dis_ = [V(ox0, PY1), V(ox0, oy0), V(ox1, oy0), V(ox1, PY1)]
ic_ = [V(ix1, PY1), V(ix1, iy0), V(ix0, iy0), V(ix0, PY1)]
for i in range(3):
    duz_duvar(y, dis_[i], dis_[i + 1], ZC, ZC + HE * 0.42, 'mermer')
    duz_duvar(y, ic_[i], ic_[i + 1], ZC, ZC + HE * 0.42, 'mermer')
for q in ([dis_[0], dis_[1], ic_[2], ic_[3]], [dis_[1], dis_[2], ic_[1], ic_[2]], [dis_[2], dis_[3], ic_[0], ic_[1]]):
    y.yuz_yon([V(p.x, p.y, ZC) for p in q], 'mermer', -Z)
for zz in (ZC + HE * 0.13, ZC + HE * 0.26):   # the architrave's fasciae
    silme(y, dis_, zz, HE * 0.03, 0.003, 'mermer', 'duz', kapali=False)
silme(y, dis_, ZC + HE * 0.36, HE * 0.06, 0.004, 'mermer', 'tac', kapali=False)
friz = disa(dis_, -0.003, False)
for i in range(3):
    y.yuz_yon([dis_[i] + Z * (ZC + HE * 0.42), dis_[i + 1] + Z * (ZC + HE * 0.42), friz[i + 1] + Z * (ZC + HE * 0.42), friz[i] + Z * (ZC + HE * 0.42)], 'mermer', Z)
for i in range(3):
    duz_duvar(y, friz[i], friz[i + 1], ZC + HE * 0.42, ZC + HE * 0.82, 'mermer')
yazi(V(0, oy0 + 0.003, ZC + HE * 0.46), X, -Y, 'M.AGRIPPA.L.F.COS.TERTIVM.FECIT', HE * 0.22)
# dentils under the cornice
for i in range(3):
    p, q = friz[i], friz[i + 1]
    Lq = (q - p).length; e = (q - p) / Lq
    k = int(Lq / 0.011)
    for j in range(k):
        kutu(y, p + e * (Lq * (j + 0.2) / k) + Z * (ZC + HE * 0.72) + V(e.y, -e.x) * 0.007, e, Lq / k * 0.6, 0.007, HE * 0.1, 'mermer', 'onsagsolust')
silme(y, friz, ZC + HE * 0.82, HE * 0.18, 0.02, 'mermer', 'tac', kapali=False)

y.bolum('Portiko: alınlık ve çatı')
ZP = ZE
HP = 0.16
alinlik(y, V(ox0, oy0), V(ox1, oy0), ZP, HP, derin=PY1 - oy0 + 0.02, key='mermer', ic_key='kirec', c=0.014, cati_key='kursun')
# the bronze wreath (with an eagle's spread wings) once fixed in the tympanum
cw = V(0, oy0 + 0.006 - 0.003, ZP + HP * 0.42)
boru(y, [cw + V(0.028 * math.cos(TAU * k / 16), 0, 0.028 * math.sin(TAU * k / 16)) for k in range(17)], 0.004, 'bronz', n=5, kapat=False)
for s in (-1, 1):
    y.yuz_yon([cw + V(s * 0.03, 0, 0.012), cw + V(s * 0.09, 0, 0.002), cw + V(s * 0.085, 0, -0.012), cw + V(s * 0.03, 0, -0.004)], 'bronz', -Y)
# roof: lead with standing seams (cover strips running eave to ridge)
xr = ox1
zr0 = ZP + 0.014 * 0.8
for j in range(13):
    yy = oy0 + 0.02 + (PY1 - oy0 - 0.03) * j / 12
    for s in (-1, 1):
        cubuk(y, V(s * xr, yy, zr0 + 0.004), V(0, yy, ZP + HP + 0.014 * 0.8 + 0.004), 0.006, 'kursun2', 0.006)
cubuk(y, V(0, oy0, ZP + HP + 0.016), V(0, PY1, ZP + HP + 0.016), 0.012, 'kursun2')
# acroteria
for p in (V(0, oy0, ZP + HP + 0.012), V(ox0, oy0, ZP + 0.012), V(ox1, oy0, ZP + 0.012)):
    kutu_merkez(y, (p.x, p.y + 0.01), 0.026, 0.02, 0.022, 'mermer', z0=p.z)
    kure(y, (p.x, p.y + 0.01, p.z + 0.03), 0.01, 'bronz', n=8, kat=4)

# ================================================================ banners
y.bolum('Sancaklar')
for sx in (-1, 1):
    sancak(y, sx * 0.6, -1.14, Z0, boy=0.36, en=0.13, yuk=0.085, aci=math.pi / 2 + sx * 0.25)
    kutu_merkez(y, (sx * 0.6, -1.14), 0.03, 0.03, 0.02, 'mermer', z0=Z0)

calistir(y, 'lm_pantheon')
