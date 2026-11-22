# Olive mill estate (lm_zeytinlik): an Andalusian cortijo / almazara on a terraced hill of olive groves. White-washed
# courtyard farmhouse with ochre trims, barred windows and a tiled ring of roofs round a patio; the two-storey master's
# house behind; the oil mill's nave with its tall counterweight tower (torre de contrapeso) under a tiled hip roof; the
# animal-driven stone mill (conical rollers on a round bed, a mule at the beam), a screw press with esparto mats, rows of
# tinajas; a small chapel with a bell tower; the threshing floor; olive trees in rows on dry-stone terraces.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import kutu3
from arap_ortak import kup, adam, halka_cati, cini_bant
from bina_ortak import calistir
import doku

y = Yapi()
rng = y.rng

ZT = 0.165                       # the hilltop
L1, L2 = 0.055, 0.11             # the terrace levels
DUV, OKR = 'siva', 'siva_oker'   # white wash, ochre trim (albero)
PX = 0.03                        # the path / gate line


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def toprak_renk(x, yy, z):
    """red-ochre olive soil on the terraces, a pale dusty albero on the hilltop, dry grass in patches"""
    n = math.sin(x * 5.3 + 0.4) * math.cos(yy * 4.7 - 0.9) * 0.6 + math.sin(x * 12.0 - yy * 9.0 + 2.0) * 0.4
    if z > ZT - 1e-4:
        return _mix((0.80, 0.70, 0.52), (0.74, 0.66, 0.46), 0.5 + 0.5 * n)
    c = _mix((0.66, 0.46, 0.31), (0.60, 0.55, 0.34), _ss(0.1, 0.9, 0.5 + 0.5 * n))
    return _mix(c, (0.58, 0.56, 0.34), 0.25 * (1 - z / ZT))


doku.KOSE_RENK['toprak'] = toprak_renk

# ---------------------------------------------------------------- the terraced hill
y.bolum('Tepe ve setler')
X0, X1, Y0, Y1, RC = -0.68, 0.68, -0.58, 0.68, 0.22      # the hilltop (a rounded rectangle)
kose = []
for (cx, cy, a0) in ((X1 - RC, Y0 + RC, -math.pi / 2), (X1 - RC, Y1 - RC, 0.0), (X0 + RC, Y1 - RC, math.pi / 2), (X0 + RC, Y0 + RC, math.pi)):
    for k in range(7):
        a = a0 + (math.pi / 2) * k / 6
        kose.append(V(cx + RC * math.cos(a), cy + RC * math.sin(a)))
TPS = []
for i in range(len(kose)):
    a, b = kose[i], kose[(i + 1) % len(kose)]
    m = max(1, int(round((b - a).length / 0.11)))
    TPS += [a.lerp(b, k / m) for k in range(m)]
NRM = [(q - p) / 0.001 for p, q in zip(TPS, disa(TPS, 0.001))]
# profile outer -> inner: (offset, z, key of the band from the previous ring)
PROF = [(0.41, 0.0, None), (0.29, 0.008, 'toprak'), (0.28, L1, 'tas_koyu'), (0.17, L1, 'toprak'), (0.16, L2, 'tas_koyu'), (0.05, L2, 'toprak'),
        (0.04, ZT, 'tas_koyu'), (0.0, ZT, 'toprak'), (-0.12, ZT, 'toprak')]
rings = []
for k, (off, zz, _) in enumerate(PROF):
    j = 0.012 if k == 0 else 0.0
    rings.append([V(p.x, p.y, zz) + n * (off + j * math.sin(i * 2.3)) for i, (p, n) in enumerate(zip(TPS, NRM))])
for k in range(1, len(PROF)):
    y.serit(rings[k - 1], rings[k], PROF[k][2])
y.yuz_yon(rings[-1], 'toprak', Z)
# the dry-stone walls' copings (a darker lip on each terrace edge)
for k in (3, 5, 7):
    silme(y, [V(p.x, p.y) for p in disa(TPS, PROF[k - 1][0] + 0.004)], PROF[k - 1][1] - 0.006, 0.006, 0.004, 'kaya_koyu', 'duz')


def zeytin(x, yy, z, s=1.0):
    """an olive tree: a short gnarled trunk splitting in two, a few lumpy silvery crowns"""
    a = rng.random() * TAU
    d = V(math.cos(a), math.sin(a))
    t0 = V(x, yy, z)
    t1 = t0 + Z * (0.03 * s) + d * (0.006 * s)
    boru(y, [t0, t0 + Z * (0.014 * s) - d * 0.003, t1], 0.006 * s, 'ahsap', n=5, r_son=0.0045 * s)
    for k in range(3):
        b = a + TAU * k / 3 + 0.4 * rng.random()
        e = V(math.cos(b), math.sin(b))
        c = t1 + e * (0.018 * s) + Z * (0.016 * s + 0.01 * s * rng.random())
        if k < 2:
            boru(y, [t1, c], 0.0035 * s, 'ahsap', n=4, kapat=False)
        kure(y, (c.x, c.y, c.z + 0.008 * s), (0.022 + 0.006 * rng.random()) * s, 'zeytin', n=7, kat=4)


y.bolum('Zeytinlikler')
# rows of olive trees on the terraces (one row per band), the front path kept clear
for (off, zz, adim) in ((0.35, 0.004, 0.14), (0.225, L1, 0.14), (0.105, L2, 0.14)):
    yol = [p + n * off for p, n in zip(TPS, NRM)]
    L = sum((yol[(i + 1) % len(yol)] - yol[i]).length for i in range(len(yol)))
    nt = int(L / adim)
    acc, i, s0 = 0.0, 0, rng.random() * adim
    pts = []
    seg = [(yol[i], yol[(i + 1) % len(yol)]) for i in range(len(yol))]
    tot = 0.0
    for a, b in seg:
        l = (b - a).length
        while s0 <= tot + l:
            pts.append(a.lerp(b, (s0 - tot) / l))
            s0 += adim
        tot += l
    for p in pts:
        if abs(p.x - PX) < 0.09 and p.y < 0: continue
        zeytin(p.x, p.y, zz, 0.95 + 0.25 * rng.random())

# the stairs up the terrace walls on the path, and the path itself
y.bolum('Patika')
yf = Y0
for (off, z0, z1) in ((0.285, 0.008, L1), (0.165, L1, L2), (0.045, L2, ZT)):
    yw = yf - off
    merdiven(y, (PX, yw - 0.06), math.pi / 2, 0.07, z0, z1, n=5, d=0.012, key='kaya_koyu')
for (y_a, y_b, zz) in ((yf - 0.41, yf - 0.345, 0.0085), (yf - 0.275, yf - 0.225, L1), (yf - 0.155, yf - 0.105, L2)):
    y.yuz_yon([V(PX - 0.04, y_a, zz + 0.002), V(PX + 0.04, y_a, zz + 0.002), V(PX + 0.04, y_b, zz + 0.002), V(PX - 0.04, y_b, zz + 0.002)], 'kum_acik', Z)
y.yuz_yon([V(PX - 0.04, yf - 0.01, ZT + 0.002), V(PX + 0.04, yf - 0.01, ZT + 0.002), V(PX + 0.04, -0.22, ZT + 0.002), V(PX - 0.04, -0.22, ZT + 0.002)], 'kum_acik', Z)


# ---------------------------------------------------------------- helpers
def duvar(a, b, z0, z1, desen, renk=DUV, v0=None, v1=None, en=0.5):
    """a white wall a->b split into len(desen) bays: '0' plain, 'p' a barred window with an ochre frame, 'k' a
    door, 'K' a big arched gate, 'a' a small arched window"""
    n = len(desen)
    H = z1 - z0
    for j, c in enumerate(desen):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        W = (q - p).length
        if c == '0':
            duz_duvar(y, p, q, z0, z1, renk)
        elif c == 'p':
            va = v0 if v0 is not None else H * 0.38
            vb = v1 if v1 is not None else H * 0.78
            u0, u1 = 0.5 - en * 0.5 * min(1, 0.06 / W) * 1.2, 0.5 + en * 0.5 * min(1, 0.06 / W) * 1.2
            dikdortgen_acik(y, p, q, z0, H, u0, u1, va, vb, (renk, 'siva_krem', 'siva_krem', 'koyu'), derin=0.012, cerceve=(0.006, OKR))
            kafes(y, p, q, z0, u0, u1, va, vb, 'demir', 3, 3, 0.0025, 0.004)
        elif c == 'k':
            hu = min(0.4, 0.022 / W)
            dikdortgen_acik(y, p, q, z0, H, 0.5 - hu, 0.5 + hu, 0.0, min(H * 0.72, 0.075), (renk, 'siva_krem', 'kum_acik', 'ahsap_dikey'), derin=0.014,
                            cerceve=(0.007, OKR))
        elif c == 'K':
            y.kemerli(p, q, z0, H, (renk, 'siva_krem', 'kum_acik', 'ahsap_dikey'), v0=0.0, en=min(0.8, 0.1 / W), ust=H * 0.12, derin=0.03, k_say=10,
                      cerceve=(0.012, [OKR, 'kum_acik']))
        elif c == 'a':
            y.kemerli(p, q, z0, H, (renk, 'siva_krem', 'kum_acik', 'koyu'), v0=H * 0.45, en=min(0.6, 0.03 / W), ust=H * 0.15, derin=0.012, k_say=6,
                      cerceve=(0.005, OKR))


def bina_duvar(k, z0, z1, desenler, renk=DUV, **kw):
    for i in range(len(k)):
        d = desenler[i] if i < len(desenler) else '0'
        if d is None: continue
        duvar(k[i], k[(i + 1) % len(k)], z0, z1, d, renk, **kw)
    silme(y, k, z0, 0.03, 0.004, OKR, 'duz')            # ochre plinth (zocalo)


def baca(x, yy, z0, h, w=0.03):
    """an Andalusian white chimney with a little tiled cap"""
    kutu_merkez(y, (x, yy), w, w, h, DUV, z0=z0)
    kutu_merkez(y, (x, yy), w + 0.01, w + 0.01, 0.006, OKR, z0=z0 + h)
    cati_kirma(y, x - w / 2 - 0.004, x + w / 2 + 0.004, yy - w / 2 - 0.004, yy + w / 2 + 0.004, z0 + h + 0.018, 0.014, 0.006, 'kiremit', ns=2, nr=1)
    for (dx, dy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        cubuk(y, V(x + dx * (w / 2), yy + dy * (w / 2), z0 + h + 0.006), V(x + dx * (w / 2), yy + dy * (w / 2), z0 + h + 0.018), 0.006, DUV)


# ---------------------------------------------------------------- the cortijo (courtyard farmhouse)
y.bolum('Cortijo: avlulu ev')
DIS = (-0.27, 0.33, -0.2, 0.36)
IC = (-0.11, 0.17, -0.04, 0.2)
ZI, ZR, ZD = ZT + 0.115, ZT + 0.2, ZT + 0.13
F = 0.01
dk = dikdortgen(*DIS)
ik = dikdortgen(*IC)
# outer walls: the gate in the front, barred windows, a side door
bina_duvar(dk, ZT, ZD - F, ['0p0K0p0', '0p00p0', '0', 'p0k0p'])
# the patio: paved, its inner walls with doors and windows, a well, pots and an orange tree
y.yuz_yon([V(p.x, p.y, ZT + 0.002) for p in ik], 'zemin', Z)
ikr = [ik[1], ik[0], ik[3], ik[2]]   # (walking the patio clockwise: the walls face into it)
for i, d in enumerate(['0k0p', 'pk0', '0pk0', 'kp0']):
    a, b = ikr[i], ikr[(i + 1) % 4]
    duvar(a, b, ZT, ZI - F, d)
silme(y, ikr, ZT, 0.025, 0.004, OKR, 'duz')
halka_cati(y, IC, DIS, ZI, ZR, ZD, sacak=0.022, sacak_dis=0.022)
# the gate's raised frame (portada) with a curved crest, a tile panel and the estate's cross
gx = PX
pa, pb = V(gx - 0.075, DIS[2] - 0.012), V(gx + 0.075, DIS[2] - 0.012)
kutu3(y, V(gx - 0.064, DIS[2] - 0.006, ZT + 0.08), X, Y, Z, 0.022, 0.012, 0.16, OKR, ('+x', '-x', '-y', '+z'))
kutu3(y, V(gx + 0.064, DIS[2] - 0.006, ZT + 0.08), X, Y, Z, 0.022, 0.012, 0.16, OKR, ('+x', '-x', '-y', '+z'))
# the crest wall above the eave: a gable with curved shoulders
cz = ZD - F
crest = [V(gx - 0.075, 0, cz), V(gx + 0.075, 0, cz), V(gx + 0.075, 0, cz + 0.05), V(gx + 0.05, 0, cz + 0.07), V(gx + 0.03, 0, cz + 0.1),
         V(gx - 0.03, 0, cz + 0.1), V(gx - 0.05, 0, cz + 0.07), V(gx - 0.075, 0, cz + 0.05)]
CY0, CY1 = DIS[2] - 0.016, DIS[2] + 0.012
y.yuz_yon([V(p.x, CY0, p.z) for p in crest], DUV, -Y)
y.yuz_yon([V(p.x, CY1, p.z) for p in crest], DUV, Y)
for i in range(len(crest)):
    p, q = crest[i], crest[(i + 1) % len(crest)]
    if i == 0: continue
    m = (p + q) / 2
    y.yuz_yon([V(p.x, CY0, p.z), V(q.x, CY0, q.z), V(q.x, CY1, q.z), V(p.x, CY1, p.z)], OKR, V(m.x - gx, 0, m.z - cz - 0.03))
cini_bant(y, V(gx - 0.035, CY0), V(gx + 0.035, CY0), cz + 0.012, 0.035, ('turkuaz', 'beyaz', 'kobalt', 'beyaz'), n=4)
cubuk(y, V(gx, CY0 + 0.014, cz + 0.1), V(gx, CY0 + 0.014, cz + 0.145), 0.006, 'demir')
cubuk(y, V(gx - 0.015, CY0 + 0.014, cz + 0.128), V(gx + 0.015, CY0 + 0.014, cz + 0.128), 0.006, 'demir')
# chimneys
for (cx_, cy_) in ((-0.19, 0.12), (0.25, -0.02), (-0.04, -0.12)):
    baca(cx_, cy_, ZT + 0.12, 0.15)
# the patio's well and plants
WX, WY = 0.03, 0.08
donel(y, (WX, WY), [(0.0, ZT), (0.026, ZT), (0.026, ZT + 0.03), (0.02, ZT + 0.03), (0.02, ZT + 0.01), (0.0, ZT + 0.01)], DUV, n=12)
boru(y, [V(WX - 0.022, WY, ZT + 0.03), V(WX - 0.022, WY, ZT + 0.07), V(WX, WY, ZT + 0.085), V(WX + 0.022, WY, ZT + 0.07), V(WX + 0.022, WY, ZT + 0.03)], 0.0025, 'demir', n=4)
for (px, py_) in ((-0.08, -0.01), (0.14, -0.01), (-0.08, 0.17), (0.14, 0.17), (-0.08, 0.08)):
    kup(y, px, py_, ZT + 0.002, r=0.01, h=0.022, key='kiremit')
    kure(y, (px, py_, ZT + 0.034), 0.014, 'boya_yesil', n=7, kat=4)
y.prizma((0.1, 0.12), 0.004, ZT, ZT + 0.05, 'ahsap', n=5)       # an orange tree
kure(y, (0.1, 0.12, ZT + 0.075), 0.032, 'yesil_koyu', n=9, kat=5)
for (dx, dy, dz) in ((0.015, -0.02, 0.07), (-0.02, 0.01, 0.085), (0.0, 0.025, 0.065), (0.022, 0.012, 0.09)):
    kure(y, (0.1 + dx, 0.12 + dy, ZT + dz), 0.005, 'boya_sari', n=5, kat=3)

# the master's house: two storeys behind the ring, hipped roof, balcony
y.bolum('Ağa evi')
HX0, HX1, HY0, HY1 = -0.24, 0.3, 0.36, 0.55
HZ = ZT + 0.26
hk = dikdortgen(HX0, HX1, HY0, HY1)
bina_duvar(hk, ZT, ZT + 0.13, [None, '0p0p0', 'p0k0p', '0p0p0'])
bina_duvar(hk, ZT + 0.13, HZ, ['0p0p0p0', '0p0p0', 'p0p0p0p', '0p0p0'])
silme(y, hk, ZT + 0.13, 0.008, 0.005, OKR, 'duz')
silme(y, hk, HZ - 0.012, 0.012, 0.008, OKR, 'tac')
for p in hk:   # ochre corner quoins
    d = (p - V((HX0 + HX1) / 2, (HY0 + HY1) / 2)).normalized()
    for j in range(5):
        kutu_merkez(y, (p.x, p.y), 0.024 if j % 2 == 0 else 0.016, 0.024 if j % 2 else 0.016, 0.022, OKR, z0=ZT + 0.04 + j * 0.042)
cati_kirma(y, HX0, HX1, HY0, HY1, HZ, 0.1, 0.025, 'kiremit', 'kiremit2', ns=8, nr=4, dilim=['kiremit', 'kiremit2'])
baca(HX0 + 0.1, (HY0 + HY1) / 2 + 0.04, HZ + 0.02, 0.12)
baca(HX1 - 0.08, (HY0 + HY1) / 2 + 0.04, HZ + 0.02, 0.12)
# the upper front looks over the ring roof: a wrought-iron balcony there (+y side, the garden)
for xx in (-0.02, 0.15):
    kutu3(y, V(xx, HY1 + 0.014, ZT + 0.142), X, Y, Z, 0.07, 0.028, 0.006, OKR)
    boru(y, [V(xx - 0.035, HY1 + 0.026, ZT + 0.17), V(xx + 0.035, HY1 + 0.026, ZT + 0.17)], 0.002, 'demir', n=4)
    for k in range(8):
        u = xx - 0.034 + 0.068 * k / 7
        cubuk(y, V(u, HY1 + 0.026, ZT + 0.145), V(u, HY1 + 0.026, ZT + 0.17), 0.002, 'demir')

# ---------------------------------------------------------------- the oil mill: nave and counterweight tower
y.bolum('Almazara ve contrapeso kulesi')
NX0, NX1, NY0, NY1 = 0.42, 0.62, -0.22, 0.24
NZ = ZT + 0.15
nk = dikdortgen(NX0, NX1, NY0, NY1)
bina_duvar(nk, ZT, NZ, ['0K0', 'a0a0a0a', '0', 'a0a0k0a'])
silme(y, nk, NZ - 0.008, 0.008, 0.006, OKR, 'tac')
for (a, b) in ((nk[1], nk[2]),):   # buttresses on the outer side
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for t in (3 / 14, 0.5, 11 / 14):   # between the arched windows (bays of 1/7)
        p = a.lerp(b, t)
        kutu3(y, p + nn * 0.012 + Z * (ZT + 0.06), e, nn, Z, 0.024, 0.024, 0.12, DUV, ('+y', '+x', '-x', '+z'))
cati_besik(y, NX0, NX1, NY0, NY1, NZ, 0.08, 0.02, 'kiremit', 'kiremit2', ucluk_key=DUV, ns=8, nr=4, dilim=['kiremit', 'kiremit2'])
# the tower
TX0, TX1, TY0, TY1 = 0.4, 0.62, 0.25, 0.47
TZ = ZT + 0.58
tk = dikdortgen(TX0, TX1, TY0, TY1)
bands = [(ZT, ZT + 0.16, ['0k0', '000', '000', '000']), (ZT + 0.16, ZT + 0.3, ['0p0', '0p0', '0p0', '0p0']),
         (ZT + 0.3, ZT + 0.44, ['000', '000', '000', '000']), (ZT + 0.44, TZ, ['0a0a0', '0a0a0', '0a0a0', '0a0a0'])]
for z0, z1, des in bands:
    bina_duvar(tk, z0, z1, des)
for zz in (ZT + 0.16, ZT + 0.44):
    silme(y, tk, zz - 0.008, 0.008, 0.006, OKR, 'duz')
for p in tk:   # ochre quoins up the corners
    for j in range(13):
        kutu_merkez(y, (p.x, p.y), 0.026 if j % 2 == 0 else 0.018, 0.026 if j % 2 else 0.018, 0.034, OKR, z0=ZT + 0.03 + j * 0.04)
silme(y, tk, TZ - 0.02, 0.02, 0.012, OKR, 'tac')
ttop = cati_kirma(y, TX0, TX1, TY0, TY1, TZ, 0.12, 0.03, 'kiremit', 'kiremit2', ns=6, nr=4, dilim=['kiremit', 'kiremit2'])
# the banner on the roof's apex
sancak(y, (TX0 + TX1) / 2, (TY0 + TY1) / 2, ttop - 0.012, boy=0.2, en=0.13, yuk=0.08, aci=-0.6)
# the end of the press beam showing through the tower wall, with its stone counterweight outside
cubuk(y, V(TX1 - 0.02, (TY0 + TY1) / 2, ZT + 0.12), V(TX1 + 0.05, (TY0 + TY1) / 2, ZT + 0.12), 0.026, 'ahsap_koyu')
donel(y, (TX1 + 0.06, (TY0 + TY1) / 2), [(0.0, ZT), (0.04, ZT), (0.042, ZT + 0.05), (0.0, ZT + 0.05)], 'granit', n=12)
cubuk(y, V(TX1 + 0.045, (TY0 + TY1) / 2, ZT + 0.05), V(TX1 + 0.045, (TY0 + TY1) / 2, ZT + 0.12), 0.006, 'demir')

# ---------------------------------------------------------------- the stone mill, press, jars
y.bolum('Taş değirmen, pres, küpler')
MX, MY = 0.46, -0.4
# the round bed (solera) with a raised rim
donel(y, (MX, MY), [(0.0, ZT), (0.11, ZT), (0.11, ZT + 0.03), (0.098, ZT + 0.034), (0.09, ZT + 0.03), (0.09, ZT + 0.024), (0.0, ZT + 0.024)], 'granit', n=24)
y.prizma((MX, MY), 0.008, ZT + 0.024, ZT + 0.13, 'ahsap_koyu', n=6)        # the central post
# two conical rollers (rulos) on a horizontal axle
for s in (-1, 1):
    a = 0.4 + (0 if s > 0 else math.pi)
    d = V(math.cos(a), math.sin(a))
    c0 = V(MX, MY) + d * 0.02
    c1 = V(MX, MY) + d * 0.085
    nn = V(-d.y, d.x)
    # a truncated cone lying on its side: rings round the axle
    rs = [(0.02, 0.022), (0.085, 0.034)]
    def ring(p, r, zc):
        return [p + nn * (r * math.cos(TAU * i / 12)) + Z * (zc + r * math.sin(TAU * i / 12)) for i in range(12)]
    A = ring(c0, 0.026, ZT + 0.024 + 0.034)
    B = ring(c1, 0.034, ZT + 0.024 + 0.034)
    for i in range(12):
        j = (i + 1) % 12
        yuz_dis(y, [A[i], B[i], B[j], A[j]], 'granit', (c0 + c1) / 2 + Z * (ZT + 0.058))
    y.yuz_yon(A, 'granit', -d); y.yuz_yon(B, 'granit', d)
    cubuk(y, V(MX, MY, ZT + 0.058), (c1 + d * 0.012) + Z * (ZT + 0.058), 0.007, 'ahsap_koyu')
# the beam to the mule
mb = V(MX, MY) + V(math.cos(-1.2), math.sin(-1.2)) * 0.2
cubuk(y, V(MX, MY, ZT + 0.11), mb + Z * (ZT + 0.07), 0.008, 'ahsap')


def katir(x, yy, z, aci, renk='ahsap', s=1.0):
    """a mule (head towards +x before turning)"""
    with parca(y, (x, yy, z), aci, s):
        h = 0.045
        boru(y, [V(-0.035, 0, h), V(0.0, 0, h + 0.003), V(0.03, 0, h + 0.002)], 0.016, renk, n=8)
        kure(y, (-0.035, 0, h), 0.016, renk, n=7, kat=4)
        kure(y, (0.03, 0, h + 0.002), 0.017, renk, n=7, kat=4)
        boru(y, [V(0.038, 0, h + 0.008), V(0.055, 0, h + 0.03), V(0.07, 0, h + 0.022)], 0.008, renk, n=6, r_son=0.007)
        boru(y, [V(0.066, 0, h + 0.026), V(0.088, 0, h + 0.012)], 0.008, renk, n=6, r_son=0.006)
        for s_ in (-1, 1):
            cubuk(y, V(0.064, s_ * 0.004, h + 0.032), V(0.06, s_ * 0.008, h + 0.05), 0.004, renk)
            for lx in (-0.03, 0.026):
                cubuk(y, V(lx, s_ * 0.008, h - 0.005), V(lx, s_ * 0.008, 0.0), 0.007, renk)
        boru(y, [V(-0.05, 0, h + 0.004), V(-0.058, 0, h - 0.025)], 0.003, 'ahsap_koyu', n=4, r_son=0.002)
        kutu_merkez(y, (0.0, 0), 0.03, 0.036, 0.006, 'boya_kirmizi', z0=h + 0.012)   # the harness cloth


katir(mb.x + 0.01, mb.y - 0.005, ZT, -1.2 + math.pi / 2 + math.pi, 'ahsap_acik')
# the screw press: a stone bed, a stack of esparto mats, two posts, a crossbeam and the screw
PRX, PRY = 0.26, -0.42
kutu_merkez(y, (PRX, PRY), 0.11, 0.08, 0.025, 'granit', z0=ZT)
for k in range(7):
    donel(y, (PRX, PRY), [(0.0, ZT + 0.025 + k * 0.008), (0.03, ZT + 0.025 + k * 0.008), (0.03, ZT + 0.031 + k * 0.008), (0.0, ZT + 0.031 + k * 0.008)],
          'saz_koyu' if k % 2 else 'saz', n=10)
for sx in (-1, 1):
    cubuk(y, V(PRX + sx * 0.045, PRY, ZT + 0.025), V(PRX + sx * 0.045, PRY, ZT + 0.16), 0.012, 'ahsap_koyu')
cubuk(y, V(PRX - 0.058, PRY, ZT + 0.15), V(PRX + 0.058, PRY, ZT + 0.15), 0.018, 'ahsap_koyu')
y.prizma((PRX, PRY), 0.008, ZT + 0.09, ZT + 0.2, 'ahsap', n=8)
kutu_merkez(y, (PRX, PRY), 0.05, 0.05, 0.008, 'ahsap', z0=ZT + 0.083)
cubuk(y, V(PRX - 0.05, PRY, ZT + 0.18), V(PRX + 0.05, PRY, ZT + 0.18), 0.005, 'ahsap_acik')
# tinajas: rows along the mill's west wall and by the press
for k in range(7):
    kup(y, NX0 - 0.03, NY0 + 0.03 + k * 0.064, ZT, r=0.022, h=0.075, key='kiremit')
for (px, py_) in ((0.34, -0.5), (0.37, -0.52), (0.31, -0.53), (0.2, -0.5)):
    kup(y, px, py_, ZT, r=0.018, h=0.06, key='kiremit2')
# olive baskets and a cart
for (px, py_) in ((0.6, -0.48), (0.63, -0.42), (0.58, -0.53)):
    donel(y, (px, py_), [(0.0, ZT), (0.014, ZT), (0.019, ZT + 0.018), (0.0, ZT + 0.018)], 'saz', n=8)
    kure(y, (px, py_, ZT + 0.016), 0.012, 'koyu', n=6, kat=3)
adam(y, 0.3, -0.36, ZT, 0.5, govde='kumas', bas='siva_krem', boy=0.05)
adam(y, 0.56, -0.3, ZT, 2.6, govde='boya_kirmizi', bas='siva_krem', boy=0.05)

# ---------------------------------------------------------------- the chapel
y.bolum('Şapel')
SX0, SX1, SY0, SY1 = -0.62, -0.44, -0.48, -0.16
SZ = ZT + 0.14
sk = dikdortgen(SX0, SX1, SY0, SY1)
bina_duvar(sk, ZT, SZ, ['0K0', 'a0a0', '0', '0a0a'])
silme(y, sk, SZ - 0.008, 0.008, 0.006, OKR, 'tac')
cati_besik(y, SX0, SX1, SY0, SY1, SZ, 0.07, 0.016, 'kiremit', 'kiremit2', ucluk_key=DUV, alinlik_key=OKR, ns=6, nr=4, dilim=['kiremit', 'kiremit2'])
y.oculus(V((SX0 + SX1) / 2, SY0, SZ + 0.03), X, -Y, 0.014, 'koyu', OKR, f=0.005, k=12)
# the bell tower at the front-right corner
BX, BY, BW = SX1 + 0.035, SY0 + 0.01, 0.09
bk = dikdortgen(BX - BW / 2, BX + BW / 2, BY - BW / 2, BY + BW / 2)
BZ = ZT + 0.3
bina_duvar(bk, ZT, BZ, ['0', '0', '0', '0'])
for zz in (ZT + 0.15, BZ):
    silme(y, bk, zz - 0.008, 0.008, 0.006, OKR, 'duz')
BH = 0.1
for i in range(4):
    a, b = bk[i], bk[(i + 1) % 4]
    y.kemerli(a, b, BZ, BH, (DUV, 'siva_krem', OKR, 'koyu'), v0=0.012, en=0.6, ust=0.015, derin=0.014, k_say=8, cerceve=(0.006, OKR))
silme(y, bk, BZ + BH - 0.01, 0.01, 0.008, OKR, 'tac')
cati_kirma(y, BX - BW / 2, BX + BW / 2, BY - BW / 2, BY + BW / 2, BZ + BH, 0.08, 0.016, 'kiremit', 'kiremit2', ns=4, nr=3)
# the bell in the front opening
zb = BZ + 0.03
donel(y, (BX, BY - BW / 2 + 0.008), [(0.0, zb), (0.017, zb), (0.015, zb + 0.008), (0.011, zb + 0.024), (0.007, zb + 0.034), (0.0, zb + 0.036)], 'bronz', n=10)
cubuk(y, V(BX, BY, BZ + BH + 0.09), V(BX, BY, BZ + BH + 0.14), 0.005, 'demir')
cubuk(y, V(BX - 0.014, BY, BZ + BH + 0.122), V(BX + 0.014, BY, BZ + BH + 0.122), 0.005, 'demir')
# cypresses by the chapel
for (cx_, cy_) in ((-0.66, -0.52), (-0.64, -0.1), (-0.66, -0.3)):
    agac(y, cx_, cy_, ZT, boy=0.2, tur='servi', key='yesil_koyu')

# ---------------------------------------------------------------- threshing floor, garden trees
y.bolum('Harman yeri, bahçe')
EX, EY, ER = -0.45, 0.36, 0.13
donel(y, (EX, EY), [(ER + 0.022, ZT), (ER + 0.02, ZT + 0.016), (ER + 0.012, ZT + 0.016), (ER, ZT + 0.006)], 'tas', n=28)
donel(y, (EX, EY), [(ER + 0.001, ZT + 0.006), (0.0, ZT + 0.006)], 'kum_acik', n=28)
# straw heaps and a threshing sledge on the floor
for (dx, dy, r_) in ((-0.04, 0.03, 0.04), (0.05, -0.03, 0.03)):
    donel(y, (EX + dx, EY + dy), [(r_, ZT + 0.004), (r_ * 0.8, ZT + 0.025), (r_ * 0.4, ZT + 0.04), (0.0, ZT + 0.045)], 'saz', n=10)
kutu_merkez(y, (EX + 0.03, EY + 0.06), 0.06, 0.03, 0.008, 'ahsap', z0=ZT + 0.004, aci=0.5)
# olive and fig trees, a palm at the gate
for (px, py_) in ((-0.2, 0.62), (0.05, 0.62), (0.3, 0.6), (0.55, 0.58), (-0.55, 0.58), (0.64, -0.08), (-0.64, -0.12)):
    zeytin(px, py_, ZT, 1.0)
agac(y, PX + 0.09, -0.28, ZT, boy=0.2, tur='palmiye', key='boya_yesil')

# ---------------------------------------------------------------- the alberca and the huerta
y.bolum('Alberca ve bostan')
# a raised whitewashed irrigation tank (alberca) with water, its spout and a channel (acequia) to the garden beds
AX0, AX1, AY0, AY1, AZ = -0.34, -0.16, -0.34, -0.25, ZT + 0.04
ak = dikdortgen(AX0, AX1, AY0, AY1)
duvarlar(y, disa(ak, 0.014), ZT, AZ + 0.006, DUV)
silme(y, disa(ak, 0.014), ZT, 0.012, 0.004, OKR, 'duz')
o_ = disa(ak, 0.014)
for i in range(4):
    j = (i + 1) % 4
    y.yuz_yon([o_[i] + Z * (AZ + 0.006), o_[j] + Z * (AZ + 0.006), ak[j] + Z * (AZ + 0.006), ak[i] + Z * (AZ + 0.006)], 'kum_acik', Z)
duvarlar(y, [ak[3], ak[2], ak[1], ak[0]], AZ - 0.012, AZ + 0.006, DUV)
y.yuz_yon([V(p.x, p.y, AZ - 0.012) for p in ak], 'su', Z)
# a stone spout on the front and the channel running down to the beds
cubuk(y, V(-0.25, AY0 - 0.012, AZ - 0.004), V(-0.25, AY0 - 0.03, AZ - 0.006), 0.008, 'granit')
for (xa, xb, ya, yb) in ((-0.262, -0.238, -0.42, AY0 - 0.014),):
    duvarlar(y, dikdortgen(xa, xb, ya, yb), ZT, ZT + 0.008, 'tas')
    y.yuz_yon([V(xa + 0.005, ya, ZT + 0.0085), V(xb - 0.005, ya, ZT + 0.0085), V(xb - 0.005, yb, ZT + 0.0085), V(xa + 0.005, yb, ZT + 0.0085)], 'su', Z)
    for (u0, u1) in ((xa, xa + 0.005), (xb - 0.005, xb)):
        y.yuz_yon([V(u0, ya, ZT + 0.008), V(u1, ya, ZT + 0.008), V(u1, yb, ZT + 0.008), V(u0, yb, ZT + 0.008)], 'tas', Z)
# garden beds: dark tilled soil in strips with rows of green plants, a low hedge of prickly pear
for k in range(5):
    bx0 = -0.37 + k * 0.058
    if abs(bx0 + 0.022 + 0.25) < 0.03: continue        # (the channel)
    duvarlar(y, dikdortgen(bx0, bx0 + 0.044, -0.55, -0.43), ZT, ZT + 0.008, 'toprak', ust='kaya_koyu')
    for j in range(4):
        kure(y, (bx0 + 0.022, -0.535 + j * 0.03, ZT + 0.014), 0.011 + 0.003 * ((j + k) % 2), 'boya_yesil' if (j + k) % 3 else 'zeytin', n=6, kat=3)
for (px, py_) in ((-0.13, -0.47), (-0.11, -0.53), (-0.4, -0.5)):
    y.prizma((px, py_), 0.004, ZT, ZT + 0.035, 'ahsap', n=5)       # orange trees
    kure(y, (px, py_, ZT + 0.05), 0.025, 'yesil_koyu', n=8, kat=4)
    for (dx, dy, dz) in ((0.012, -0.016, 0.05), (-0.015, 0.008, 0.06), (0.004, 0.018, 0.042)):
        kure(y, (px + dx, py_ + dy, ZT + dz), 0.004, 'boya_sari', n=5, kat=3)
adam(y, -0.2, -0.48, ZT, 1.2, govde='kumas', bas='siva_krem', boy=0.05)

# ---------------------------------------------------------------- the stable and granary (cuadra), a cart
y.bolum('Ahır ve araba')
CX0, CX1, CY0, CY1 = -0.64, -0.38, -0.06, 0.15
CZ = ZT + 0.11
ck = dikdortgen(CX0, CX1, CY0, CY1)
bina_duvar(ck, ZT, CZ, ['0p0', 'k0K0k', '0p0', 'p0p0p'])
silme(y, ck, CZ - 0.008, 0.008, 0.006, OKR, 'tac')
cati_besik(y, CX0, CX1, CY0, CY1, CZ, 0.07, 0.018, 'kiremit', 'kiremit2', ucluk_key=DUV, ns=6, nr=4, dilim=['kiremit', 'kiremit2'])
# a hayloft door in the gable and a pulley beam
gx_ = (CX0 + CX1) / 2
y.oculus(V(CX1, (CY0 + CY1) / 2, CZ + 0.026), Y, X, 0.012, 'koyu', OKR, f=0.004, k=10)
# the cart: two big wheels, a box, shafts
KX, KY = -0.33, 0.02
for s in (-1, 1):
    with parca(y, (KX, KY + s * 0.03, ZT + 0.028), 0.0):
        pts = [V(0.028 * math.cos(TAU * i / 12), 0, 0.028 * math.sin(TAU * i / 12)) for i in range(12)]
        for i in range(12):
            cubuk(y, pts[i], pts[(i + 1) % 12], 0.005, 'ahsap_koyu')
        for i in range(0, 12, 2):
            cubuk(y, V(0, 0, 0), pts[i], 0.003, 'ahsap')
kutu_merkez(y, (KX, KY), 0.07, 0.054, 0.024, 'ahsap', z0=ZT + 0.03)
for s in (-1, 1):
    cubuk(y, V(KX + 0.035, KY + s * 0.018, ZT + 0.035), V(KX + 0.1, KY + s * 0.018, ZT + 0.006), 0.005, 'ahsap_koyu')
for (dx, dy) in ((-0.015, -0.012), (0.012, 0.01), (0.0, -0.01), (-0.01, 0.014)):
    kure(y, (KX + dx, KY + dy, ZT + 0.058), 0.012, 'saz' if dx < 0 else 'zeytin', n=6, kat=3)
katir(-0.31, 0.12, ZT, 0.3, 'ahsap_koyu')

calistir(y, 'lm_zeytinlik')
