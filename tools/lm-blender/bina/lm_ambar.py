# Büyük Ambar (lm_ambar): an Egyptian state granary by the Nile (after the Meketre granary model and Old Kingdom
# tomb scenes): a mud-brick enclosure entered through a small whitewashed pylon gate, a raised terrace of beehive
# silos with filling holes at the top reached by ladders, the scribe's office with a papyrus-column porch, grain heaps
# and sacks in the court; outside the river bank with a shaduf, a reed boat, papyrus and palms.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05
KER = 'kerpic'
SIV = 'siva_krem'
KAVETTO = [(0, 0), (0.16, 0.03), (0.2, 0.1), (0.12, 0.17), (0.04, 0.19), (0.07, 0.36), (0.18, 0.56), (0.4, 0.75),
           (0.72, 0.88), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]


def kavetto(kose, z, h, c, key):
    silme(y, kose, z, h, c, key, KAVETTO)
    y.yuz_yon([V(p.x, p.y, z + h) for p in kose], key, Z)


# ---------------------------------------------------------------- ground, the river
y.bolum('Zemin')
XW, YF, YB = 1.15, -1.15, 1.15
NX = -0.8           # the river bank (water x < NX)
ZW = Z0 - 0.028
kutu(y, V(NX, YF, 0), X, XW - NX, YB - YF, Z0, 'kerpic_koyu', 'onarkasag')
silme(y, [V(NX, YF), V(XW, YF), V(XW, YB), V(NX, YB)], Z0 - 0.008, 0.008, 0.006, 'kerpic_koyu', 'duz', kapali=False)
y.yuz([V(NX, YF, Z0), V(XW, YF, Z0), V(XW, YB, Z0), V(NX, YB, Z0)], 'kum_acik')
kutu(y, V(-XW, YF, 0), X, NX - 0.05 + XW, YB - YF, ZW, 'kerpic_koyu', 'onarkasol')
y.yuz([V(-XW, YF, ZW), V(NX - 0.05, YF, ZW), V(NX - 0.05, YB, ZW), V(-XW, YB, ZW)], 'su')
# the sloping mud bank
y.yuz_yon([V(NX - 0.05, YF, ZW), V(NX, YF, Z0), V(NX, YB, Z0), V(NX - 0.05, YB, ZW)], 'toprak', V(-0.5, 0, 1))
for yy, s in ((YF, -1), (YB, 1)):
    y.yuz_yon([V(NX - 0.05, yy, 0), V(NX, yy, 0), V(NX, yy, Z0), V(NX - 0.05, yy, ZW)], 'kerpic_koyu', V(0, s, 0))
# a paved path from the landing to the gate, a stone quay with steps
y.yuz([V(NX, -0.92, Z0 + 0.002), V(0.25, -0.92, Z0 + 0.002), V(0.25, -0.84, Z0 + 0.002), V(NX, -0.84, Z0 + 0.002)], 'zemin')
kutu(y, V(NX - 0.1, -1.0, ZW - 0.01), X, 0.1, 0.24, Z0 - ZW + 0.012, 'kirec', 'onarkasolust')

# ---------------------------------------------------------------- enclosure wall and the gate
y.bolum('Avlu duvari')
EX0, EX1, EY0, EY1 = -0.62, 1.02, -0.72, 0.98
HW, TW = 0.16, 0.05
GX0, GX1 = 0.08, 0.36      # the gate gap in the front wall


def duvar(a, b):
    """a mud-brick wall a->b (outer side on the right): plastered lower band, a rounded coping, drain holes"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x); L = (b - a).length
    kutu(y, a + Z * Z0, e, L, TW, HW, 'kerpic_tugla', 'onarkaust')
    # buttress piers on the outer face, their tops rounded
    n = max(1, int(L / 0.22))
    for m in range(n + 1):
        if m in (0, n): continue
        p = a.lerp(b, m / n)
        kutu(y, p - e * 0.018 + Z * Z0 + nc * 0.016, e, 0.036, 0.016, HW - 0.01, 'kerpic_tugla', 'onsagsolust')
        boru(y, [p - e * 0.018 + nc * 0.008 + Z * (Z0 + HW - 0.01), p + e * 0.018 + nc * 0.008 + Z * (Z0 + HW - 0.01)], 0.009, KER, n=6)
    for p, s in ((a, -1), (b, 1)):
        y.yuz_yon([p + Z * Z0, p - nc * TW + Z * Z0, p - nc * TW + Z * (Z0 + HW), p + Z * (Z0 + HW)], 'kerpic_tugla', e * s)
    boru(y, [a - nc * (TW / 2) + Z * (Z0 + HW), b - nc * (TW / 2) + Z * (Z0 + HW)], TW * 0.48, KER, n=8)
    kutu(y, a + Z * Z0 + nc * 0.004, e, L, 0.004, 0.035, SIV, 'onust')                # plinth band
    # wavy courses (pan-bedding) shown as darker bands
    for zz in (0.06, 0.11):
        kutu(y, a + Z * (Z0 + zz) + nc * 0.0015, e, L, 0.0015, 0.008, 'kerpic_koyu', 'onust')


k = [V(EX0, EY0), V(GX0, EY0), V(GX1, EY0), V(EX1, EY0), V(EX1, EY1), V(EX0, EY1)]
duvar(k[0], k[1]); duvar(k[2], k[3]); duvar(k[3], k[4]); duvar(k[4], k[5]); duvar(k[5], k[0])

y.bolum('Kapi')
GC = (GX0 + GX1) / 2


def kule(x0, x1, y0, y1, h, bt=0.02):
    """a small battered whitewashed gate tower with torus corners and a cavetto cornice"""
    B = dikdortgen(x0, x1, y0, y1, Z0); T = dikdortgen(x0 + bt, x1 - bt, y0 + bt, y1 - bt, Z0 + h)
    for i in range(4):
        j = (i + 1) % 4
        e = B[j] - B[i]; nn = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], SIV, nn + Z * (bt / h))
    for i in range(4):
        boru(y, [B[i], T[i]], 0.007, 'kirec', n=5)
    kavetto(T, Z0 + h, 0.04, 0.03, SIV)
    # a painted band and a framed panel on the front
    nf = V(0, -1, bt / h).normalized()
    P = lambda s, t, d=0.003: B[0].lerp(B[1], s).lerp(T[0].lerp(T[1], s), t / h) + nf * d
    for t0, key in ((h * 0.82, 'boya_kirmizi'), (h * 0.86, 'turkuaz'), (h * 0.9, 'boya_sari')):
        y.yuz_yon([P(0.04, t0), P(0.96, t0), P(0.96, t0 + h * 0.03), P(0.04, t0 + h * 0.03)], key, nf)
    y.yuz_yon([P(0.25, h * 0.25), P(0.75, h * 0.25), P(0.75, h * 0.68), P(0.25, h * 0.68)], 'kirec', nf)
    # a sheaf of grain painted in the panel (the granary's sign)
    for s in (0.4, 0.5, 0.6):
        y.yuz_yon([P(s - 0.02, h * 0.3, 0.004), P(s + 0.02, h * 0.3, 0.004), P(s + 0.012, h * 0.62, 0.004), P(s - 0.012, h * 0.62, 0.004)], 'boya_sari', nf)
    y.yuz_yon([P(0.34, h * 0.4, 0.0045), P(0.66, h * 0.4, 0.0045), P(0.66, h * 0.43, 0.0045), P(0.34, h * 0.43, 0.0045)], 'boya_yesil', nf)


GH = 0.3
kule(GX0 - 0.16, GX0, EY0 - 0.05, EY0 + 0.07, GH)
kule(GX1, GX1 + 0.16, EY0 - 0.05, EY0 + 0.07, GH)
# the lintel over the passage, with the winged sun
kutu(y, V(GX0, EY0 - 0.04, Z0 + GH * 0.72), X, GX1 - GX0, 0.1, GH * 0.16, SIV)
kavetto(dikdortgen(GX0, GX1, EY0 - 0.04, EY0 + 0.06), Z0 + GH * 0.88, 0.03, 0.02, SIV)
o = V(GC, EY0 - 0.044, Z0 + GH * 0.8)
y.yuz_yon([o + V(0.018 * math.cos(TAU * i / 12), 0, 0.018 * math.sin(TAU * i / 12)) for i in range(12)], 'boya_kirmizi', -Y)
for s in (-1, 1):
    y.yuz_yon([o + V(s * 0.02, 0, -0.01), o + V(s * 0.12, 0, 0.0), o + V(s * 0.12, 0, 0.016), o + V(s * 0.02, 0, 0.012)], 'turkuaz', -Y)
# cedar doors standing open
for s, xx in ((-1, GX0), (1, GX1)):
    with parca(y, (xx, EY0 + 0.07, Z0), math.pi / 2 if s < 0 else math.pi / 2):
        kutu_merkez(y, (0.05, -s * 0.006), 0.1, 0.008, GH * 0.7, 'ahsap')
        for zz in (0.04, 0.12, 0.18):
            kutu_merkez(y, (0.05, -s * 0.0105), 0.1, 0.002, 0.008, 'bronz', z0=zz)
sancak(y, GX1 + 0.08, EY0 + 0.01, Z0 + GH + 0.04, boy=0.24, en=0.13, yuk=0.075, aci=0.4)

# ---------------------------------------------------------------- the silo terrace
y.bolum('Silolar')
TX0, TX1, TY0, TY1 = -0.52, 0.94, 0.08, 0.9
TZ = Z0 + 0.09
kutu(y, V(TX0, TY0, Z0), X, TX1 - TX0, TY1 - TY0, TZ - Z0, 'kerpic_koyu', 'onarkasagsolust')
silme(y, dikdortgen(TX0, TX1, TY0, TY1), TZ - 0.012, 0.012, 0.008, SIV, 'duz')
# stairs up the terrace
for xs in (-0.05, 0.55):
    merdiven(y, V(xs, TY0 - 0.12), math.pi / 2, 0.14, Z0, TZ, n=5, d=0.024, key='kerpic_koyu', yanlik=SIV)
# low parapet along the terrace front


def silo(cx, cy, z0, r, h):
    """a beehive grain silo: a mud-brick foot, the whitewashed dome, a filling hole with a rim at the top, an
    emptying hatch at the foot, a ladder to the top"""
    donel(y, (cx, cy), [(r * 1.04, z0), (r * 1.02, z0 + h * 0.08)], KER, n=20)
    halka_kornis(y, (cx, cy), r * 1.0, z0 + h * 0.08, 0.008, 0.006, 20, 'kerpic_koyu')
    # the dome in bands: mud plaster below, whitewash above, a painted frieze between, rope-like tie courses
    PR = [(1.0, 0.08), (1.0, 0.2), (0.995, 0.32), (0.97, 0.42), (0.95, 0.52), (0.9, 0.61), (0.83, 0.7), (0.74, 0.78), (0.63, 0.85),
          (0.5, 0.91), (0.36, 0.95), (0.17, 1.0)]
    def rr(t):
        for k in range(len(PR) - 1):
            if t <= PR[k + 1][1] + 1e-9:
                u = (t - PR[k][1]) / (PR[k + 1][1] - PR[k][1]); return PR[k][0] + (PR[k + 1][0] - PR[k][0]) * u
        return PR[-1][0]
    def bant(t0, t1, key):
        ts = [t0] + [p[1] for p in PR if t0 < p[1] < t1] + [t1]
        donel(y, (cx, cy), [(r * rr(t), z0 + h * t) for t in ts], key, n=30)
    bant(0.08, 0.4, SIV)
    bant(0.4, 0.425, 'boya_kirmizi')
    bant(0.425, 0.465, 'siva')
    bant(0.465, 0.49, 'turkuaz')
    bant(0.49, 1.0, 'siva')
    for t in (0.24, 0.66, 0.84):     # tie courses standing proud of the plaster
        halka_kornis(y, (cx, cy), r * rr(t) * 1.0, z0 + h * t - 0.004, 0.008, 0.004, 30, 'kerpic' if t < 0.4 else 'siva_krem', profil='yarim')
    # the filling hole: a raised clay rim and the dark mouth, a lid leaning on it
    zt = z0 + h
    donel(y, (cx, cy), [(r * 0.17, zt), (r * 0.2, zt + 0.006), (r * 0.15, zt + 0.012), (r * 0.12, zt + 0.006)], KER, n=12)
    y.yuz_yon(cokgen((cx, cy), r * 0.12, 12, z=zt + 0.006), 'koyu', Z)
    # the hatch at the foot (front), with a wooden frame
    nn = V(0, -1, 0)
    for k, (w, hh, key, d) in enumerate(((0.06, 0.075, 'ahsap', 0.002), (0.044, 0.06, 'koyu', 0.0032))):
        zz = z0 + h * 0.1
        y.yuz_yon([V(cx - w / 2, cy - r - d, zz), V(cx + w / 2, cy - r - d, zz), V(cx + w / 2, cy - r - d, zz + hh), V(cx - w / 2, cy - r - d, zz + hh)], key, nn)
    # ladder against the side
    a0 = V(cx + r + 0.09, cy - 0.02, z0); a1 = V(cx + r * 0.42, cy - 0.02, zt - 0.01)
    for s in (-1, 1):
        boru(y, [a0 + V(0, s * 0.014, 0), a1 + V(0, s * 0.014, 0)], 0.003, 'ahsap', n=4)
    for k in range(1, 9):
        p = a0.lerp(a1, k / 9)
        cubuk(y, p + V(0, -0.014, 0), p + V(0, 0.014, 0), 0.003, 'ahsap')


SR, SH = 0.12, 0.56
for j, yy in enumerate((0.33, 0.69)):
    for i in range(4):
        # the back row is the great row: taller, broader, its tops crowning the whole granary
        silo(TX0 + 0.17 + i * 0.36, yy, TZ, SR if j == 0 else 0.13, SH if j == 0 else 0.7)
# a low parapet with a rounded coping along the terrace front, broken by the two stairs
for x0_, x1_ in ((TX0, -0.12), (0.02, 0.48), (0.62, TX1)):
    kutu(y, V(x0_, TY0, TZ), X, x1_ - x0_, 0.022, 0.03, 'kerpic_tugla', 'onarkasagsol')
    boru(y, [V(x0_, TY0 + 0.011, TZ + 0.03), V(x1_, TY0 + 0.011, TZ + 0.03)], 0.011, KER, n=8)
# buttress piers down the terrace's face
for k in range(9):
    px = TX0 + 0.04 + k * (TX1 - TX0 - 0.08) / 8
    if any(abs(px - xs) < 0.1 for xs in (-0.05, 0.55)): continue
    kutu(y, V(px - 0.018, TY0 - 0.014, Z0), X, 0.036, 0.014, TZ - Z0 - 0.012, 'kerpic_tugla', 'onsagsolust')
# sacks waiting at the foot of the ladders, a worker's basket
def cuval(x, yy, z, aci=0.0):
    with parca(y, (x, yy, z), aci):
        donel(y, (0, 0), [(0.012, 0), (0.017, 0.008), (0.016, 0.022), (0.009, 0.03), (0.004, 0.034), (0, 0.034)], 'kumas', n=8)
        halka_kornis(y, (0, 0), 0.006, 0.028, 0.003, 0.002, 6, 'saz_koyu')


for (x, yy, z) in ((-0.2, 0.15, TZ), (-0.17, 0.17, TZ), (0.52, 0.14, TZ), (0.6, 0.16, TZ), (0.2, 0.2, TZ), (0.86, 0.5, TZ)):
    cuval(x, yy, z)

# ---------------------------------------------------------------- the scribe's office with its papyrus porch
y.bolum('Katip odasi')
OX0, OX1, OY0, OY1 = -0.56, -0.18, -0.6, -0.28
OH = 0.17
kp = dikdortgen(OX0, OX1, OY0, OY1)
for i in range(4):
    a, b = kp[i], kp[(i + 1) % 4]
    if i == 1:   # the door to the court
        dikdortgen_acik(y, a, b, Z0, OH, 0.38, 0.62, 0.0, OH * 0.66, (SIV, 'kerpic_koyu', KER, 'ahsap_koyu'), derin=0.02, cerceve=(0.008, 'kirec'))
    else:
        dikdortgen_acik(y, a, b, Z0, OH, 0.4, 0.6, OH * 0.62, OH * 0.82, (SIV, 'kerpic_koyu', KER, 'koyu'), derin=0.015)
kavetto(kp, Z0 + OH, 0.03, 0.02, SIV)
# the porch: papyrus columns carrying a reed-matting roof towards the court
PX1 = OX1 + 0.13
for yy in (OY0 + 0.03, (OY0 + OY1) / 2, OY1 - 0.03):
    sutun(y, PX1, yy, Z0, Z0 + OH - 0.01, 0.014, 'kirec', 'misir', bant_key='boya_kirmizi')
kutu(y, V(OX1, OY0, Z0 + OH - 0.01), X, PX1 - OX1 + 0.02, OY1 - OY0, 0.012, 'ahsap_koyu')
kutu(y, V(OX1, OY0 - 0.005, Z0 + OH + 0.002), X, PX1 - OX1 + 0.025, OY1 - OY0 + 0.01, 0.006, 'saz')
# the scribes at work under the porch: a mat, low desks, papyrus rolls and a tally board
y.yuz([V(OX1 + 0.01, OY0 + 0.03, Z0 + 0.002), V(PX1 - 0.02, OY0 + 0.03, Z0 + 0.002), V(PX1 - 0.02, OY1 - 0.03, Z0 + 0.002), V(OX1 + 0.01, OY1 - 0.03, Z0 + 0.002)], 'saz_koyu')
for yy in (OY0 + 0.09, OY1 - 0.09):
    kutu_merkez(y, (OX1 + 0.05, yy), 0.03, 0.05, 0.02, 'ahsap', z0=Z0)
    boru(y, [V(OX1 + 0.04, yy - 0.015, Z0 + 0.024), V(OX1 + 0.06, yy + 0.015, Z0 + 0.024)], 0.004, 'beyaz', n=5)
    # the scribe: seated cross-legged, white kilt, a wig
    kutu_merkez(y, (OX1 + 0.085, yy), 0.03, 0.034, 0.012, 'beyaz', z0=Z0)
    kutu_merkez(y, (OX1 + 0.088, yy), 0.016, 0.022, 0.03, 'kirmizi', z0=Z0 + 0.012)
    kure(y, (OX1 + 0.088, yy, Z0 + 0.05), 0.01, 'koyu', n=8, kat=4)
# the roof: a reed awning on four posts over the back half, grain spread to dry, the stair hatch, jars
ZT = Z0 + OH + 0.03
for (px, py) in ((OX0 + 0.04, OY0 + 0.04), (OX0 + 0.04, OY1 - 0.12), (OX0 + 0.2, OY0 + 0.04), (OX0 + 0.2, OY1 - 0.12)):
    y.prizma((px, py), 0.005, ZT, ZT + 0.07, 'ahsap', n=5)
kutu(y, V(OX0 + 0.025, OY0 + 0.025, ZT + 0.07), X, 0.19, OY1 - OY0 - 0.13, 0.006, 'saz')
y.yuz_yon([V(OX0 + 0.025, OY0 + 0.025, ZT + 0.0695), V(OX0 + 0.215, OY0 + 0.025, ZT + 0.0695), V(OX0 + 0.215, OY1 - 0.105, ZT + 0.0695), V(OX0 + 0.025, OY1 - 0.105, ZT + 0.0695)], 'saz_koyu', -Z)
y.yuz([V(OX0 + 0.05, OY0 + 0.05, ZT + 0.002), V(OX0 + 0.19, OY0 + 0.05, ZT + 0.002), V(OX0 + 0.19, OY0 + 0.16, ZT + 0.002), V(OX0 + 0.05, OY0 + 0.16, ZT + 0.002)], 'saz_koyu')
donel(y, (OX0 + 0.12, OY0 + 0.105), [(0.05, ZT + 0.003), (0.035, ZT + 0.012), (0.012, ZT + 0.02), (0, ZT + 0.022)], 'boya_sari', n=12)
kutu_merkez(y, (OX1 - 0.07, OY0 + 0.07), 0.06, 0.05, 0.012, 'koyu', z0=ZT - 0.01, yuzler='ust')
for (px, py) in ((OX0 + 0.06, OY1 - 0.06), (OX0 + 0.1, OY1 - 0.05)):
    donel(y, (px, py), [(0.008, Z0 + OH + 0.03), (0.014, Z0 + OH + 0.045), (0.012, Z0 + OH + 0.06), (0.006, Z0 + OH + 0.066), (0, Z0 + OH + 0.066)], 'kerpic_koyu', n=8)

# ---------------------------------------------------------------- the court: grain heaps, measuring, threshing
y.bolum('Avlu')
for (px, py, r, h) in ((0.1, -0.35, 0.09, 0.08), (0.32, -0.3, 0.07, 0.065), (0.66, -0.4, 0.1, 0.085)):
    donel(y, (px, py), [(r, Z0), (r * 0.8, Z0 + h * 0.4), (r * 0.4, Z0 + h * 0.85), (0, Z0 + h)], 'boya_sari', n=14)
# a threshing floor: a ring kerb with a pair of oxen treading the grain
CX_, CY_ = 0.72, -0.12
halka_kornis(y, (CX_, CY_), 0.15, Z0, 0.014, 0.012, 20, KER)
y.yuz_yon(cokgen((CX_, CY_), 0.15, 20, z=Z0 + 0.003), 'boya_sari', Z)
def okuz(x, yy, aci):
    with parca(y, (x, yy, Z0), aci):
        for lx in (-0.022, 0.022):
            for ly in (-0.01, 0.01):
                cubuk(y, V(lx, ly, 0), V(lx, ly, 0.028), 0.007, 'ahsap_acik')
        boru(y, [V(-0.032, 0, 0.04), V(0.03, 0, 0.042)], 0.016, 'ahsap_acik', n=8)
        boru(y, [V(0.03, 0, 0.046), V(0.05, 0, 0.04), V(0.06, 0, 0.032)], 0.009, 'ahsap_acik', n=6, r_son=0.007)
        for s in (-1, 1):
            boru(y, [V(0.048, s * 0.006, 0.05), V(0.05, s * 0.02, 0.058), V(0.056, s * 0.026, 0.066)], 0.0025, 'kirec', n=4, r_son=0.001)
        kutu_merkez(y, (0.01, 0), 0.03, 0.034, 0.003, 'beyaz', z0=0.056)
okuz(CX_ - 0.08, CY_ + 0.03, -math.pi / 2)
okuz(CX_ + 0.08, CY_ - 0.03, math.pi / 2)
# the measurer's bushel and a row of sealed jars by the wall
kutu_merkez(y, (0.4, -0.5), 0.05, 0.05, 0.03, 'ahsap', z0=Z0)
for k in range(6):
    px = 0.55 + k * 0.05
    donel(y, (px, -0.66), [(0.008, Z0), (0.016, Z0 + 0.018), (0.014, Z0 + 0.036), (0.007, Z0 + 0.044), (0.008, Z0 + 0.05), (0, Z0 + 0.05)], 'kerpic_koyu', n=8)
for (x, yy) in ((0.18, -0.46), (0.22, -0.48), (0.2, -0.42), (0.47, -0.25), (0.5, -0.22)):
    cuval(x, yy, Z0)
# workers carrying sacks: up the ladders, along the path from the boat, at the heaps
def isci(x, yy, z, aci=0.0, yuk=True):
    with parca(y, (x, yy, z), aci):
        for s in (-1, 1):
            cubuk(y, V(0, s * 0.005, 0), V(0.002, s * 0.005, 0.028), 0.006, 'kirmizi')
        kutu_merkez(y, (0, 0), 0.016, 0.02, 0.016, 'beyaz', z0=0.022)
        donel(y, (0, 0), [(0.008, 0.036), (0.01, 0.05), (0.007, 0.058), (0, 0.06)], 'kirmizi', n=6)
        kure(y, (0.002, 0, 0.068), 0.0075, 'kirmizi', n=6, kat=3)
        kure(y, (-0.001, 0, 0.071), 0.007, 'koyu', n=6, kat=3)
        if yuk:
            with parca(y, (-0.004, 0.008, 0.052), 0.0, 0.8):
                cuval(0, 0, 0)
for (x, yy, a) in ((-0.3, -0.88, 0.0), (-0.1, -0.87, 0.1), (0.12, -0.89, 0.0), (0.22, -0.62, 1.2), (0.3, -0.12, 1.5), (0.5, -0.3, 2.8)):
    isci(x, yy, Z0, a)
for i in range(4):   # one on each front-row ladder
    cx = TX0 + 0.17 + i * 0.36
    a0 = V(cx + SR + 0.09, 0.31, TZ); a1 = V(cx + SR * 0.42, 0.31, TZ + SH - 0.01)
    p = a0.lerp(a1, 0.45 + 0.1 * (i % 2))
    isci(p.x + 0.012, p.y - 0.012, p.z - 0.01, math.pi, True)
# a sycamore and palms in the court
agac(y, -0.3, -0.05, Z0, 0.18, 'yapraklı', 'boya_yesil')
agac(y, 0.92, 0.0, Z0, 0.2, 'palmiye')

# ---------------------------------------------------------------- the river bank: shaduf, boat, papyrus, palms
y.bolum('Nil kiyisi')
# the shaduf: two posts and a crossbar, the sweep with a clay counterweight and a bucket
SXd, SYd = NX + 0.06, 0.35
for s in (-1, 1):
    cubuk(y, V(SXd, SYd + s * 0.03, Z0), V(SXd, SYd + s * 0.03, Z0 + 0.14), 0.012, 'ahsap')
cubuk(y, V(SXd, SYd - 0.04, Z0 + 0.14), V(SXd, SYd + 0.04, Z0 + 0.14), 0.01, 'ahsap')
boru(y, [V(SXd + 0.12, SYd, Z0 + 0.07), V(SXd - 0.2, SYd, Z0 + 0.22)], 0.004, 'ahsap_koyu', n=5)
kure(y, (SXd + 0.13, SYd, Z0 + 0.065), 0.025, 'kerpic_koyu', n=8, kat=4)
boru(y, [V(SXd - 0.2, SYd, Z0 + 0.22), V(SXd - 0.2, SYd, Z0 + 0.06)], 0.0012, 'saz_koyu', n=3)
donel(y, (SXd - 0.2, SYd), [(0.008, Z0 + 0.03), (0.014, Z0 + 0.04), (0.014, Z0 + 0.06), (0, Z0 + 0.06)], 'kerpic', n=8)
# a papyrus reed boat at the quay, loaded with sacks
with parca(y, (NX - 0.2, -0.88, ZW), math.pi / 2):
    for s in (-1, 1):   # the papyrus-bundle hull: swelling amidships, the ends drawn up thin
        boru(y, [V(0.0, 0, 0.016), V(s * 0.08, 0, 0.018), V(s * 0.13, 0, 0.03), V(s * 0.165, 0, 0.06)], 0.028, 'saz', n=10, r_son=0.005)
    for k in range(5):
        boru(y, [V(-0.1 + k * 0.05, -0.028, 0.02), V(-0.1 + k * 0.05, 0.028, 0.02)], 0.003, 'saz_koyu', n=4)
    for (bx, by) in ((-0.05, -0.008), (0.0, 0.008), (0.05, -0.006)):
        cuval(bx, by, 0.03)
    cubuk(y, V(0.06, 0, 0.03), V(0.06, 0, 0.2), 0.006, 'ahsap')
# papyrus clumps in the shallows, palms along the bank
def papirus(x, yy, n=7, boy=0.12):
    for k in range(n):
        a = TAU * k / n
        tip = V(x + math.cos(a) * 0.03, yy + math.sin(a) * 0.03, ZW + boy * (0.8 + 0.2 * (k % 3) / 2))
        boru(y, [V(x, yy, ZW), tip], 0.0025, 'boya_yesil', n=3)
        donel(y, (tip.x, tip.y), [(0.0, tip.z - 0.002), (0.014, tip.z + 0.012), (0.0, tip.z + 0.016)], 'cimen', n=6)
for (px, py) in ((-1.05, -0.5), (-1.0, 0.0), (-1.08, 0.55), (-0.95, 0.9), (-1.1, -1.05)):
    papirus(px, py)
for (px, py, b) in ((-0.72, -0.3, 0.2), (-0.7, 0.1, 0.17), (-0.74, 0.6, 0.21), (-0.7, 1.05, 0.18), (-0.7, -0.62, 0.16), (0.65, -1.02, 0.19), (1.08, -0.95, 0.17)):
    agac(y, px, py, Z0, b, 'palmiye')
# a field strip outside the wall (emmer, green), with irrigation ditches
for k in range(4):
    x0 = 0.48 + k * 0.16
    y.yuz([V(x0, -1.12, Z0 + 0.003), V(x0 + 0.13, -1.12, Z0 + 0.003), V(x0 + 0.13, -0.82, Z0 + 0.003), V(x0, -0.82, Z0 + 0.003)], 'cimen' if k % 2 else 'cimen_kuru')

calistir(y, 'lm_ambar')
