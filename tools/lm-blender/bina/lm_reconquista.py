# Reconquista frontier castle (lm_reconquista): a Castilian hill castle of the 13th-15th century (Penafiel, La Mota,
# Belmonte). A rocky hill ringed by a thick honey-stone curtain wall with round cubo towers; a great square keep
# (torre del homenaje) with corbelled bartizans at its corners and mid-sides and a machicolated crown; the gate
# between two towers behind an offset barbican, a ramp up the slope; inside a Romanesque chapel with a bell gable
# (espadana), barracks and stables under tiled roofs, a well.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import kutu3, levha
from arap_ortak import kup, adam
from bina_ortak import calistir
import doku

y = Yapi()
rng = y.rng

ZT = 0.2                     # the hill's top
TAS = 'kum'                  # honey limestone
TAS_K = 'kum_koyu'
TRIM = 'kum_acik'
PEN = (TAS, TAS_K, TRIM, 'koyu')
FY = -0.6                    # the front wall line (gate)
GX, GW = 0.06, 0.17          # main gate
WZ0, WH = ZT - 0.03, 0.25    # curtain wall foot, height


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def tepe_renk(x, yy, z):
    """the hill per corner: dry Castilian scrub at the foot, ochre earth, bare rock up under the walls"""
    n = math.sin(x * 4.7 + 0.3) * math.cos(yy * 5.1 - 0.8) * 0.7 + math.sin(x * 10.0 - yy * 8.0 + 1.0) * 0.3
    h = z / ZT
    c = _mix((0.50, 0.52, 0.30), (0.57, 0.53, 0.33), 0.5 + 0.5 * n)
    c = _mix(c, (0.64, 0.52, 0.36), _ss(0.15, 0.5, h + 0.12 * n))
    if h > 0.999:   # the plateau: dry grass and bare earth in broad patches
        n2 = math.sin(x * 7.3 - 1.0) * math.cos(yy * 6.1 + 0.4) * 0.6 + math.sin(x * 15.0 + yy * 11.0) * 0.4
        return _mix((0.60, 0.58, 0.36), (0.71, 0.61, 0.45), 0.5 + 0.5 * n2)
    c = _mix(c, (0.70, 0.63, 0.53), _ss(0.55, 0.95, h + 0.15 * n))
    return c


doku.KOSE_RENK['toprak_ot'] = tepe_renk


def cubo(c, r, z0, h, key, mazgal_h=0.03, **kw):
    """a round tower whose merlons stand on every other side of its crown ring (kule_yuvarlak's own merlons fill
    each short side of a round ring, leaving a plain band without crenels)"""
    zr = kule_yuvarlak(y, c, r, z0, h, key, mazgal_h=0, **kw)
    n = kw.get('n', 24)
    rr = r + (0.016 if kw.get('konsol', True) else 0.0)
    ring = cokgen(c, rr, n)
    zt = z0 + h + 0.012
    for i in range(0, n - 1, 2):
        a, b = ring[i], ring[i + 1]
        e = (b - a); e.z = 0; L = e.length; e.normalize()
        nn = V(e.y, -e.x)
        m = a.lerp(b, 0.5) - nn * 0.008
        kutu3(y, m + Z * (zt + mazgal_h / 2), e, nn, Z, L, 0.016, mazgal_h, key, ('+x', '-x', '+y', '-y', '+z'))
    return zr

# ---------------------------------------------------------------- the hill
y.bolum('Tepe')
TP = [V(-0.55, -0.95), V(0.6, -0.95), V(1.0, -0.42), V(0.98, 0.55), V(0.38, 0.92), V(-0.55, 0.9), V(-1.0, 0.42), V(-0.98, -0.45)]
TPS = []
for i in range(len(TP)):
    a, b = TP[i], TP[(i + 1) % len(TP)]
    m = max(1, int(round((b - a).length / 0.1)))
    TPS += [a.lerp(b, k / m) for k in range(m)]
NRM = [(q - p) / 0.001 for p, q in zip(TPS, disa(TPS, 0.001))]
TPS = [p + n * (0.025 * math.sin(i * 1.7) + 0.015 * math.sin(i * 4.3 + 1.0)) for i, (p, n) in enumerate(zip(TPS, NRM))]   # (a natural edge)
HALKA = [(0.14, 0.0), (0.11, 0.04), (0.075, 0.09), (0.04, 0.14), (0.012, ZT - 0.012), (0.0, ZT), (-0.07, ZT), (-0.17, ZT)]
rings = []
for k, (off, zz) in enumerate(HALKA):
    j = 0.0 if k == 0 else 0.022
    rings.append([V(p.x, p.y, zz) + n * (off + j * (rng.random() - 0.5)) + Z * (0.012 * (rng.random() - 0.5) if (k > 0 and zz < ZT - 1e-6) else 0)
                  for p, n in zip(TPS, NRM)])
for k in range(len(HALKA) - 1):
    y.serit(rings[k], rings[k + 1], 'toprak_ot')
y.yuz_yon(rings[-1], 'toprak_ot', Z)
# crags and scrub on the slopes
for i in range(len(TPS)):
    if rng.random() < 0.5:
        k = rng.choice((1, 2, 3))
        p = rings[k][i].lerp(rings[k + 1][i], 0.5)
        n = NRM[i]
        kutu_merkez(y, (p.x, p.y), 0.04 + 0.05 * rng.random(), 0.035 + 0.02 * rng.random(), 0.03 + 0.03 * rng.random(), 'kaya' if rng.random() < 0.5 else 'kaya_koyu',
                    z0=p.z - 0.025, aci=math.atan2(n.y, n.x) + math.pi / 2 + 0.5 * (rng.random() - 0.5))
    if rng.random() < 0.4:
        k = rng.choice((0, 1))
        p = rings[k][i].lerp(rings[k + 1][i], 0.6)
        kure(y, (p.x, p.y, p.z + 0.008), 0.014 + 0.01 * rng.random(), 'zeytin' if rng.random() < 0.6 else 'yesil_koyu', n=7, kat=3)
# stones and broom bushes along the plateau's rim (outside the walls)
for i in range(len(TPS)):
    p = rings[5][i].lerp(rings[6][i], 0.2 + 0.4 * rng.random())
    if abs(p.x + 0.12) < 0.14 and p.y < -0.7: continue      # (the ramp)
    r_ = rng.random()
    if r_ < 0.35:
        kure(y, (p.x, p.y, ZT + 0.006), 0.012 + 0.008 * rng.random(), 'zeytin' if rng.random() < 0.5 else 'cimen_kuru', n=7, kat=3)
    elif r_ < 0.55:
        kutu_merkez(y, (p.x, p.y), 0.02 + 0.02 * rng.random(), 0.018, 0.012, 'kaya', z0=ZT - 0.004, aci=rng.random() * 3)
# a few holm oaks at the foot
for (tx, ty) in ((-1.05, -0.75), (1.08, 0.15), (-0.2, 1.06), (0.85, 0.85), (-1.05, 0.7)):
    agac(y, tx, ty, 0.0, boy=0.13, key='yesil_koyu')

# ---------------------------------------------------------------- curtain wall and cubos
y.bolum('Sur ve kuleler')
WP = [V(GX + GW / 2, FY), V(0.5, FY), V(0.82, -0.28), V(0.8, 0.42), V(0.3, 0.72), V(-0.45, 0.7), V(-0.84, 0.32), V(-0.82, -0.3),
      V(-0.45, FY), V(GX - GW / 2, FY)]
WC = WP[1:-1]                # the corners with towers
sur(y, WP, WZ0, WH, kalinlik=0.05, key=TAS, kapali=False, mazgal_h=0.028, parapet_h=0.014, ust_key='zemin', konsol=True)
# the inside ground of the bailey
ICK = [V(GX + GW / 2, FY)] + WP[1:-1] + [V(GX - GW / 2, FY)]
y.yuz_yon([V(p.x, p.y, ZT + 0.003) for p in disa(ICK, -0.045)], 'toprak_ot', Z)
# arrow loops (saeteras: a cross slit) along the curtain
for i in range(len(WP) - 1):
    a, b = WP[i], WP[i + 1]
    L = (b - a).length
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    nl = int(L / 0.2)
    for j in range(nl):
        p = a.lerp(b, (j + 1) / (nl + 1))
        yarik(y, p + nn * 0.001 + Z * WZ0, e, nn, -0.004, 0.1, 0.008, 0.06, 'koyu')
        yarik(y, p + nn * 0.001 + Z * WZ0, e, nn, -0.011, 0.122, 0.022, 0.008, 'koyu')
# the round cubos at the corners
for i, p in enumerate(WC):
    if abs(p.y - FY) < 1e-6:
        continue         # (the front corners: below, the bigger towers)
    q = WC[i - 1] if i > 0 else WP[0]
    r_ = WC[i + 1] if i + 1 < len(WC) else WP[-1]
    d = ((p - q).normalized() + (p - r_).normalized()).normalized()
    c = p + d * 0.02
    cubo((c.x, c.y), 0.072, WZ0, WH + 0.1, TAS, cati='duz', mazgal_h=0.03, n=18, egim=0.08, yarik_say=3, konsol=True, bolum=2)
for p in (WP[1], WP[-2]):
    cubo((p.x, p.y - 0.01), 0.08, WZ0, WH + 0.12, TAS, cati='duz', mazgal_h=0.03, n=18, egim=0.08, yarik_say=3, konsol=True, bolum=2)

# ---------------------------------------------------------------- the gate and the barbican
y.bolum('Kapı ve barbakan')
kale_kapisi(y, GX, FY, GW, WZ0, WH + 0.06, derin=0.1, key=TAS, kule=None, kapi_key='ahsap_dikey')
for sx in (-1, 1):
    cubo((GX + sx * (GW / 2 + 0.05), FY - 0.03), 0.07, WZ0, WH + 0.16, TAS, cati='duz', mazgal_h=0.03, n=18, egim=0.08, yarik_say=2, konsol=True, bolum=2)
# the coat of arms over the gate (castle and lion quarters)
ga = V(GX, FY - 0.05 - 0.002, WZ0 + WH * 0.78)
for (dx, dz, k) in ((-0.012, 0.012, 'boya_kirmizi'), (0.012, 0.012, 'mermer'), (-0.012, -0.012, 'mermer'), (0.012, -0.012, 'boya_kirmizi')):
    kutu3(y, ga + V(dx, -0.003, dz), X, Y, Z, 0.022, 0.004, 0.022, k, ('-y', '+x', '-x', '+z', '-z'))
kutu3(y, ga + V(0, 0.0, 0.03), X, Y, Z, 0.05, 0.006, 0.008, TRIM, ('-y', '+x', '-x', '+z', '-z'))
# barbican: a lower wall in front of the gate, its own gate offset to the left
BY = -0.83
BX0, BX1 = -0.32, 0.44
BG = -0.12                    # barbican gate x
sur(y, [V(BX0, FY - 0.012), V(BX0, BY), V(BG - 0.08, BY)], WZ0, 0.15, kalinlik=0.04, key=TAS, kapali=False, mazgal_h=0.024, parapet_h=0.012, ust_key='zemin')
sur(y, [V(BG + 0.08, BY), V(BX1, BY), V(BX1, FY - 0.012)], WZ0, 0.15, kalinlik=0.04, key=TAS, kapali=False, mazgal_h=0.024, parapet_h=0.012, ust_key='zemin')
kale_kapisi(y, BG, BY + 0.02, 0.16, WZ0, 0.17, derin=0.07, key=TAS, kule=None, kapi_key='ahsap_dikey')
for (bx, r_) in ((BX0, 0.048), (BX1, 0.048)):
    cubo((bx, BY), r_, WZ0, 0.22, TAS, cati='duz', mazgal_h=0.026, n=14, egim=0.06, yarik_say=2, konsol=True)
# the court between the walls and the path to the gate
y.yuz_yon([V(BX0 + 0.04, BY + 0.04, ZT + 0.004), V(BX1 - 0.04, BY + 0.04, ZT + 0.004), V(BX1 - 0.04, FY - 0.09, ZT + 0.004), V(BX0 + 0.04, FY - 0.09, ZT + 0.004)], 'zemin', Z)
# the ramp up to the barbican gate: an earthen causeway with a paved road and low walls (it covers the slope under it)
RW = 0.055
# (the slope ends at the plateau's rim ~y -0.97: the ramp climbs to there, then a flat paved stretch to the gate)
ry0, ry1, ry2 = -1.34, -1.0, BY - 0.015
ZR = ZT + 0.004
y.yuz_yon([V(BG - RW, ry0, 0.004), V(BG + RW, ry0, 0.004), V(BG + RW, ry1, ZR), V(BG - RW, ry1, ZR)], 'zemin', Z)
y.yuz_yon([V(BG - RW, ry1, ZR), V(BG + RW, ry1, ZR), V(BG + RW, ry2, ZR), V(BG - RW, ry2, ZR)], 'zemin', Z)
for sx in (-1, 1):
    xx = BG + sx * RW
    y.yuz_yon([V(xx, ry0, 0.004), V(xx, ry1, ZR), V(xx + sx * 0.17, ry1, -0.01), V(xx + sx * 0.02, ry0, -0.01)], 'toprak_ot', V(sx, 0, 0.6))
    y.yuz_yon([V(xx, ry1, ZR), V(xx, ry2, ZR), V(xx, ry2, ZT - 0.05), V(xx, ry1, ZT - 0.05)], 'toprak_ot', V(sx, 0, 0))
    # low parapet walls along both edges (solid blocks: a sloped one up the ramp, a level one on the flat)
    for (pa, pb) in ((V(xx - sx * 0.007, ry0, 0.004), V(xx - sx * 0.007, ry1, ZR)), (V(xx - sx * 0.007, ry1, ZR), V(xx - sx * 0.007, ry2 - 0.02, ZR))):
        d = (pb - pa); L = d.length; d.normalize()
        kutu3(y, (pa + pb) / 2 + Z * 0.012, d, V(1, 0, 0), Z.cross(d).cross(d) * -1, L, 0.014, 0.024, TAS_K, ('+x', '-x', '+y', '-y', '+z'))
y.yuz_yon([V(BG - RW - 0.02, ry0, -0.01), V(BG + RW + 0.02, ry0, -0.01), V(BG + RW, ry0, 0.004), V(BG - RW, ry0, 0.004)], 'toprak_ot', -Y)

# ---------------------------------------------------------------- the keep (torre del homenaje)
y.bolum('Kale kulesi (torre del homenaje)')
KX, KY = -0.36, 0.24
KW, KD = 0.44, 0.4
KZ0, KZT = ZT - 0.02, ZT + 0.84
kk = dikdortgen(KX - KW / 2, KX + KW / 2, KY - KD / 2, KY + KD / 2)


def bant(a, b, z0, z1, desen, en=0.42, v0=None, ust=None, sivri=0.0, cer=True, derin=0.02):
    """a wall band a->b split into len(desen) bays: '0' plain, '1' an arched window, '2' a paired window (ajimez),
    'k' an arched door"""
    n = len(desen)
    H = z1 - z0
    for j, c in enumerate(desen):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        if c == '0':
            duz_duvar(y, p, q, z0, z1, TAS)
        elif c == '1':
            y.kemerli(p, q, z0, H, PEN, v0=v0 if v0 is not None else H * 0.15, en=en, ust=ust if ust is not None else H * 0.12, derin=derin, k_say=6,
                      sivri=sivri, cerceve=(0.005, TRIM) if cer else None)
        elif c == '2':
            m = p.lerp(q, 0.5)
            for pp, qq in ((p, m), (m, q)):
                y.kemerli(pp, qq, z0, H, PEN, v0=H * 0.15, en=en * 1.5, ust=H * 0.12, derin=derin, k_say=6, sivri=sivri, cerceve=(0.004, TRIM))
        elif c == 'k':
            y.kemerli(p, q, z0, H, (TAS, TAS_K, TRIM, 'ahsap_dikey'), v0=0.0, en=min(0.75, en * 1.6), ust=H * 0.2, derin=0.025, k_say=8, cerceve=(0.007, TRIM))


bands = [  # (z0, z1, patterns per side: front, right, back, left)
    (KZ0, ZT + 0.2, ('00k00', '0', '0', '0')),
    (ZT + 0.2, ZT + 0.33, ('0', '0', '0', '0')),
    (ZT + 0.33, ZT + 0.44, ('00100', '00100', '00100', '00100')),
    (ZT + 0.44, ZT + 0.56, ('0', '0', '0', '0')),
    (ZT + 0.56, ZT + 0.68, ('02020', '00200', '02020', '00200')),
    (ZT + 0.68, KZT, ('0', '0', '0', '0')),
]
for z0, z1, des in bands:
    for i in range(4):
        bant(kk[i], kk[(i + 1) % 4], z0, z1, des[i])
silme(y, kk, KZ0, 0.05, 0.014, TAS_K, 'kaide')
for zz in (ZT + 0.33, ZT + 0.56):
    silme(y, kk, zz - 0.008, 0.008, 0.007, TRIM, 'duz')
# slits in the lower plain band
for i in range(4):
    a, b = kk[i], kk[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for t in (0.3, 0.7):
        yarik(y, a.lerp(b, t) + nn * 0.001 + Z * KZ0, e, nn, -0.005, 0.27, 0.01, 0.06, 'koyu')
# the arms panel over the door and the steps up to it
dc = kk[0].lerp(kk[1], 0.5)
for (dx, dz, k) in ((-0.014, 0.014, 'boya_kirmizi'), (0.014, 0.014, 'mermer'), (-0.014, -0.014, 'mermer'), (0.014, -0.014, 'boya_kirmizi')):
    kutu3(y, V(dc.x + dx, dc.y - 0.004, ZT + 0.255 + dz), X, Y, Z, 0.026, 0.005, 0.026, k, ('-y', '+x', '-x', '+z', '-z'))
for (dx, dz) in ((-0.014, 0.014), (0.014, -0.014)):   # little castles (gold) on the red quarters
    kutu3(y, V(dc.x + dx, dc.y - 0.0075, ZT + 0.252 + dz), X, Y, Z, 0.012, 0.002, 0.012, 'altin', ('-y', '+x', '-x', '+z', '-z'))
# machicolated crown: corbels, a parapet with merlons, the roof terrace
konsol_halka(y, kk, KZT - 0.045, 0.045, 0.02, TAS, 3)
kd = disa(kk, 0.02)
for i in range(4):   # the corbel teeth under the crown (machicolation brackets)
    a, b = kk[i], kk[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    nb = int(L / 0.035)
    for j in range(1, nb):
        p = a.lerp(b, j / nb)
        kutu3(y, p + nn * 0.012 + Z * (KZT - 0.065), e, nn, Z, 0.01, 0.024, 0.04, TAS_K, ('+y', '+x', '-x', '-z', '+z'))
parapet(y, kd, KZT, 0.016, 0.036, 0.022, TAS)
y.yuz_yon([V(p.x, p.y, KZT + 0.0005) for p in disa(kd, -0.022)], 'zemin', Z)


def garita(c, r, zb, h, n=12):
    """a bartizan: a round turret on a corbelled cone, slit, merloned top"""
    donel(y, c, [(0.0, zb - r * 2.2), (r * 0.25, zb - r * 2.0), (r * 0.6, zb - r * 1.2), (r * 0.9, zb - r * 0.4), (r, zb)], TAS, n=n)
    for k in range(3):
        silme(y, cokgen(c, r * (0.55 + 0.15 * k), n), zb - r * (1.5 - 0.5 * k), 0.006, 0.006, TAS_K, 'duz')
    return cubo(c, r, zb, h, TAS, cati='duz', mazgal_h=0.024, n=n, egim=0.0, yarik_say=2, konsol=True)


for p in kk:   # corner bartizans
    d = (p - V(KX, KY)).normalized()
    garita(p + d * 0.022, 0.045, KZT - 0.17, 0.2)
for i in range(4):   # mid-side bartizans
    a, b = kk[i], kk[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    garita(a.lerp(b, 0.5) + nn * 0.03, 0.036, KZT - 0.12, 0.13, n=10)
# the stair turret on the roof and the banner
kule_kare(y, KX + 0.1, KY + 0.08, 0.1, KZT, 0.08, TAS, cati='piramit', cati_key='kiremit', cati_h=0.07, mazgal_h=0, sacak=0.012, yarik_say=1, konsol=False,
          cati_ns=4, cati_nr=3)
sancak(y, KX - 0.08, KY - 0.06, KZT, boy=0.24, en=0.14, yuk=0.085, aci=-0.4)

# ---------------------------------------------------------------- the chapel
y.bolum('Şapel')
CX0, CX1, CY0, CY1 = 0.38, 0.6, -0.12, 0.36
CH = 0.15
ck = dikdortgen(CX0, CX1, CY0, CY1)
bant(ck[0], ck[1], ZT, ZT + CH, '0k0', en=0.55)
for (a, b) in ((ck[1], ck[2]), (ck[3], ck[0])):
    bant(a, b, ZT, ZT + CH, '01010', en=0.32, v0=CH * 0.45, ust=CH * 0.12, derin=0.012)
duz_duvar(y, ck[2], ck[3], ZT, ZT + CH, TAS)
silme(y, ck, ZT + CH - 0.008, 0.008, 0.007, TRIM, 'tac')
for (a, b) in ((ck[1], ck[2]), (ck[3], ck[0])):   # buttresses
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for t in (0.2, 0.4, 0.6, 0.8):
        p = a.lerp(b, t)
        kutu3(y, p + nn * 0.01 + Z * (ZT + CH * 0.42), e, nn, Z, 0.018, 0.02, CH * 0.84, TAS, ('+y', '+x', '-x', '+z'))
cati_besik(y, CX0, CX1, CY0, CY1, ZT + CH, 0.075, 0.016, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=8, nr=4, dilim=['kiremit', 'kiremit2'])
# the semicircular apse at the east (+y) end
ac = V((CX0 + CX1) / 2, CY1)
apr = 0.075
yay = [V(ac.x + apr * math.cos(math.pi * i / 8), ac.y + apr * math.sin(math.pi * i / 8)) for i in range(9)]
for i in range(8):
    if i in (3, 4):
        y.kemerli(yay[i], yay[i + 1], ZT, CH * 0.85, PEN, v0=CH * 0.4, en=0.45, ust=CH * 0.12, derin=0.01, k_say=4)
    else:
        duz_duvar(y, yay[i], yay[i + 1], ZT, ZT + CH * 0.85, TAS)
silme(y, yay, ZT + CH * 0.85 - 0.006, 0.006, 0.006, TRIM, 'tac', kapali=False)
for i in range(8):
    a, b = yay[i], yay[i + 1]
    y.yuz_yon([V(a.x, a.y, ZT + CH * 0.85), V(b.x, b.y, ZT + CH * 0.85), V(ac.x, ac.y, ZT + CH * 0.85 + 0.05)], 'kiremit', V((a.x + b.x) / 2 - ac.x, (a.y + b.y) / 2 - ac.y, 0.7))
# the bell gable (espadana) rising over the west front
EZ = ZT + CH + 0.075
ex0, ex1 = CX0 + 0.03, CX1 - 0.03
EY = CY0 + 0.004
EH = 0.13
kemer_dizisi(y, V(ex0, EY), V(ex1, EY), 2, EZ - 0.02, EH, 0.024, renk=(TAS, TAS_K, TRIM, 'koyu'), en=0.56, ust=0.025, acik=True)
# its gable cap and cross
tz = EZ - 0.02 + EH
for (p, q) in ((V(ex0, EY - 0.003), V(ex1, EY - 0.003)),):
    tri = [V(ex0 + 0.01, EY - 0.002, tz), V(ex1 - 0.01, EY - 0.002, tz), V((ex0 + ex1) / 2, EY - 0.002, tz + 0.045)]
    kutu3(y, V((ex0 + ex1) / 2, EY + 0.012, tz + 0.012), X, Y, Z, 0.1, 0.022, 0.024, TAS, ('+x', '-x', '+y', '-y', '+z'))
    for s in (-1, 1):
        cubuk(y, V((ex0 + ex1) / 2 + s * 0.055, EY + 0.012, tz + 0.024), V((ex0 + ex1) / 2, EY + 0.012, tz + 0.05), 0.012, TRIM, 0.026)
cubuk(y, V((ex0 + ex1) / 2, EY + 0.012, tz + 0.05), V((ex0 + ex1) / 2, EY + 0.012, tz + 0.09), 0.006, 'demir')
cubuk(y, V((ex0 + ex1) / 2 - 0.014, EY + 0.012, tz + 0.077), V((ex0 + ex1) / 2 + 0.014, EY + 0.012, tz + 0.077), 0.006, 'demir')
# the bells
for xb in (ex0 + (ex1 - ex0) * 0.25, ex0 + (ex1 - ex0) * 0.75):
    zb = EZ + 0.02
    donel(y, (xb, EY + 0.012), [(0.0, zb), (0.017, zb), (0.015, zb + 0.008), (0.011, zb + 0.022), (0.008, zb + 0.032), (0.0, zb + 0.034)], 'bronz', n=10)
    cubuk(y, V(xb - 0.022, EY + 0.012, zb + 0.036), V(xb + 0.022, EY + 0.012, zb + 0.036), 0.005, 'ahsap_koyu')
# the bell gable's foot stands on the front gable: fill the wall between
kutu3(y, V((ex0 + ex1) / 2, EY + 0.012, (ZT + CH + EZ - 0.02) / 2), X, Y, Z, ex1 - ex0, 0.024, EZ - 0.02 - ZT - CH, TAS, ('+x', '-x', '+y', '-y'))

# ---------------------------------------------------------------- barracks, stables, well
y.bolum('Kışla, ahır, kuyu')


def bina(x0, x1, y0, y1, h, desen_on, cati_h=0.05, duvar=TAS):
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        d = desen_on[i] if i < len(desen_on) else '0'
        bant(k[i], k[(i + 1) % 4], ZT, ZT + h, d, en=0.42, v0=h * 0.45, ust=h * 0.15, derin=0.01, cer=False)
    silme(y, k, ZT + h - 0.006, 0.006, 0.005, TRIM, 'duz')
    cati_besik(y, x0, x1, y0, y1, ZT + h, cati_h, 0.014, 'kiremit', 'kiremit2', ucluk_key=duvar, ns=6, nr=3, dilim=['kiremit', 'kiremit2'])


# barracks along the back wall
bina(-0.05, 0.45, 0.47, 0.6, 0.12, ('01k10', '0', '0', '0'))
# stables along the left wall
bina(-0.78, -0.63, -0.3, 0.02, 0.1, ('0', 'k0k', '0', '0'))
# a lean-to store at the front right
bina(0.3, 0.55, -0.52, -0.4, 0.09, ('0', '0', '0k0', '0'))
# the well (aljibe) in the court
WLX, WLY = 0.12, -0.12
donel(y, (WLX, WLY), [(0.0, ZT), (0.032, ZT), (0.032, ZT + 0.03), (0.024, ZT + 0.03), (0.024, ZT + 0.008), (0.0, ZT + 0.008)], TAS_K, n=12)
for sx in (-1, 1):
    cubuk(y, V(WLX + sx * 0.026, WLY, ZT + 0.03), V(WLX + sx * 0.026, WLY, ZT + 0.07), 0.005, 'ahsap_koyu')
cubuk(y, V(WLX - 0.032, WLY, ZT + 0.07), V(WLX + 0.032, WLY, ZT + 0.07), 0.006, 'ahsap_koyu')
# carts, barrels, jars, a few soldiers in the court
for (px, py_) in ((0.24, 0.38), (0.27, 0.42), (0.22, 0.43)):
    donel(y, (px, py_), [(0.0, ZT), (0.014, ZT), (0.017, ZT + 0.018), (0.014, ZT + 0.036), (0.0, ZT + 0.036)], 'ahsap', n=8)
for (px, py_) in ((-0.6, -0.42), (-0.57, -0.47), (-0.63, -0.47)):
    kup(y, px, py_, ZT, r=0.014, h=0.04, key='kiremit')
# a paved way from the gate to the keep's door and the chapel
def yol(a, b, w=0.05):
    e = (b - a).normalized(); nn = V(e.y, -e.x) * (w / 2)
    y.yuz_yon([V(p.x, p.y, ZT + 0.0045) for p in (a + nn, b + nn, b - nn, a - nn)], 'zemin', Z)


yol(V(GX, FY + 0.04), V(GX, -0.2))
yol(V(GX, -0.2), V(KX + 0.02, KY - KD / 2 - 0.035))
yol(V(GX + 0.02, -0.17), V((CX0 + CX1) / 2, CY0 - 0.02))
# the smithy: an open lean-to against the front curtain (its roof falls to the court) with a forge, anvil, quench tub
FX0, FX1, FY0, FY1 = -0.38, -0.2, -0.545, -0.44
for px in (FX0 + 0.008, FX1 - 0.008):
    y.prizma((px, FY1), 0.007, ZT, ZT + 0.085, 'ahsap_koyu', n=4)
cubuk(y, V(FX0 - 0.01, FY1, ZT + 0.085), V(FX1 + 0.01, FY1, ZT + 0.085), 0.012, 'ahsap_koyu')
rp = [V(FX0 - 0.015, FY1 + 0.02, ZT + 0.08), V(FX1 + 0.015, FY1 + 0.02, ZT + 0.08), V(FX1 + 0.015, FY0, ZT + 0.13), V(FX0 - 0.015, FY0, ZT + 0.13)]
rd = (rp[3] - rp[0]).normalized()
rn = rd.cross(X).normalized()
rc = (rp[0] + rp[2]) / 2 - rn * 0.004
for yz, k in ((('+z',), 'kiremit'), (('-z', '+x', '-x', '+y', '-y'), 'ahsap_koyu')):
    kutu3(y, rc, X, rd, rn, (rp[1] - rp[0]).length, (rp[3] - rp[0]).length, 0.008, k, yz)
for sx in (-1, 1):   # the side gables of the lean-to
    x_ = FX0 if sx < 0 else FX1
    y.yuz_yon([V(x_, FY1, ZT), V(x_, FY0, ZT), V(x_, FY0, ZT + 0.128), V(x_, FY1, ZT + 0.08)], TAS, V(sx, 0, 0))
fc = V(-0.25, FY0 + 0.03)
kutu_merkez(y, (fc.x, fc.y), 0.06, 0.05, 0.045, 'tugla', z0=ZT)
kure(y, (fc.x, fc.y + 0.005, ZT + 0.047), 0.013, 'boya_kirmizi', n=6, kat=3)
kutu_merkez(y, (fc.x, fc.y - 0.006), 0.04, 0.03, 0.16, 'tugla', z0=ZT + 0.05)    # (the flue runs up through the lean-to)
kutu_merkez(y, (-0.33, FY1 + 0.03), 0.026, 0.012, 0.028, 'demir', z0=ZT)
donel(y, (-0.36, FY1 + 0.035), [(0.0, ZT), (0.016, ZT), (0.016, ZT + 0.02), (0.0, ZT + 0.02)], 'ahsap', n=8)
# horses tied at the stables, hay, a cart, firewood, shields and spear racks
for (hx, hy, a) in ((-0.58, -0.22, 0.0), (-0.58, -0.12, 0.2), (-0.58, -0.02, -0.15)):
    with parca(y, (hx, hy, ZT), a):
        h = 0.045
        boru(y, [V(-0.03, 0, h), V(0.03, 0, h + 0.004)], 0.015, 'ahsap_koyu', n=8)
        kure(y, (-0.03, 0, h), 0.015, 'ahsap_koyu', n=6, kat=3); kure(y, (0.03, 0, h + 0.004), 0.016, 'ahsap_koyu', n=6, kat=3)
        boru(y, [V(0.04, 0, h + 0.01), V(0.058, 0, h + 0.035), V(0.075, 0, h + 0.026)], 0.008, 'ahsap_koyu', n=5, r_son=0.006)
        for s_ in (-1, 1):
            for lx in (-0.03, 0.026):
                cubuk(y, V(lx, s_ * 0.007, h - 0.006), V(lx, s_ * 0.007, 0.0), 0.006, 'ahsap_koyu')
        kutu_merkez(y, (0.0, 0), 0.03, 0.034, 0.005, 'boya_kirmizi', z0=h + 0.011)
for (px, py_) in ((-0.5, 0.0), (-0.47, -0.05)):
    kutu_merkez(y, (px, py_), 0.05, 0.035, 0.03, 'saz', z0=ZT, aci=0.3)
for i in range(4):
    for j in range(3 - (i // 2)):
        cubuk(y, V(-0.25 + j * 0.014, 0.46, ZT + 0.007 + i * 0.012), V(-0.25 + j * 0.014, 0.4, ZT + 0.007 + i * 0.012), 0.012, 'kutuk')
for k in range(5):   # a spear rack by the barracks
    cubuk(y, V(0.1 + k * 0.012, 0.44, ZT), V(0.1 + k * 0.012, 0.447, ZT + 0.1), 0.004, 'ahsap')
    kure(y, (0.1 + k * 0.012, 0.447, ZT + 0.104), 0.004, 'demir', n=4, kat=2)
cubuk(y, V(0.09, 0.442, ZT + 0.06), V(0.16, 0.442, ZT + 0.06), 0.005, 'ahsap_koyu')
for (px, py_, a) in ((0.0, -0.3, 0.3), (0.2, -0.35, -1.0), (-0.1, 0.0, 2.0), (0.3, 0.05, 1.0), (-0.52, -0.25, 0.0), (0.66, -0.12, 3.1),
                     (0.05, 0.38, -1.6)):
    adam(y, px, py_, ZT, a, govde='boya_kirmizi' if px > 0.1 else 'kumas', bas='demir', boy=0.05)

calistir(y, 'lm_reconquista')
