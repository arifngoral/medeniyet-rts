# Yasak Şehir (lm_yasaksehir): the Forbidden City's ceremonial heart. Taihedian (Hall of Supreme Harmony), double-eaved
# with a yellow-glazed hipped roof, chiwen and roof beasts, on its three-tier white marble terrace with balustrades and
# dragon ramps; the courtyard with the bowed Golden Water stream and its five marble bridges; the U-shaped Meridian Gate
# (Wumen) with its five-phoenix pavilions; side galleries and pavilions, crenellated red walls and corner towers.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ek import *
from bina_ortak import calistir

y = Yapi()
SARI, SARI2 = 'kiremit_sari', 'boya_sari'
KIR = 'siva_kirmizi'

# ---------------------------------------------------------------- ground
y.bolum('Zemin')
Z0 = zemin(y, -1.2, 1.2, -1.22, 1.2, 0.03, 'tas_koyu', 'zemin', basamak=(('on', 0.5),), n_basamak=2)

# ---------------------------------------------------------------- outer walls and corner towers
y.bolum('Surlar')
WH = 0.13
sur(y, [(0.57, -0.88), (1.14, -0.88), (1.14, 1.14), (-1.14, 1.14), (-1.14, -0.88), (-0.57, -0.88)], Z0, WH, 0.06, KIR,
    kapali=False, mazgal_h=0.026, parapet_h=0.012, ust_key='zemin')
silme(y, [V(0.57, -0.88), V(1.14, -0.88), V(1.14, 1.14), V(-1.14, 1.14), V(-1.14, -0.88), V(-0.57, -0.88)], Z0 + 0.001, 0.016, 0.006,
      'mermer', 'kaide', kapali=False)


def kose_kulesi(cx, cy):
    """a corner tower: a marble-railed platform over the wall corner, a lacquered pavilion with a double eave, two
    crossing hip-and-gable roofs under a gilt knob and little porch gables on the lower eave"""
    zb = Z0 + WH + 0.05
    k = dikdortgen(cx - 0.1, cx + 0.1, cy - 0.1, cy + 0.1)
    duvarlar(y, k, Z0 + WH - 0.02, zb, KIR, ust='zemin')
    silme(y, k, zb - 0.008, 0.008, 0.005, 'mermer', 'kaba')
    korkuluk(y, disa(k, -0.008), zb, 0.02, 'mermer', 0.05)
    w, d, ic = 0.13, 0.09, 0.018
    tepe = salon(y, cx, cy, w, d, zb, 0.075, 0.07, sacak=0.045, cati_key=SARI, mahya=SARI2, kivrim=0.5, yukari=0.03, cift=True,
                 alt_yuk=0.03, ic=ic, ust_h=0.03, bay=0.065, chiwenli=False, hayvan=0, cati='irimoya', mahya_en=0.01, ust_kafes=False)
    z1 = zb + 0.075 + 0.02
    zc = z1 + 0.03 + 0.004 + 0.03 + 0.02
    # the crossing roof: a second hip-and-gable turned across the first, on its own walls
    bx, by = d / 2 - ic, w / 2 - ic
    duvarlar(y, dikdortgen(cx - bx, cx + bx, cy - by, cy + by), z1, zc, KIR)
    cati_irimoya(y, cx - bx, cx + bx, cy - by, cy + by, zc, 0.07, 0.045, SARI, SARI2, 0.5, 0.03, 'lake_koyu', KIR, ns=4, nr=4, ns2=3, nr2=3)
    kure(y, (cx, cy, tepe + 0.012), 0.013, 'altin', n=8, kat=4)


for cx, cy in ((-1.1, 1.1), (1.1, 1.1), (-1.1, -0.85), (1.1, -0.85)):
    kose_kulesi(cx, cy)

# ---------------------------------------------------------------- Meridian Gate (Wumen)
y.bolum('Meridyen Kapısı')
GH = 0.2
WX0, WX1, WY0, WY1 = 0.42, 0.58, -1.2, -0.98       # the wings (x mirrored), the main block y -0.98 .. -0.78
MY0, MY1 = -0.98, -0.78
KAPI = (KIR, KIR, 'mermer', 'lake_koyu')
# main block: front with three portals, back with three, plain sides above the wings
for i in range(7):
    a, b = V(-0.42 + 0.84 * i / 7, MY0), V(-0.42 + 0.84 * (i + 1) / 7, MY0)
    if i in (1, 3, 5):
        y.kemerli(a + Z * Z0, b + Z * Z0, 0, GH, KAPI, v0=0.0, en=0.62 if i == 3 else 0.52, ust=0.07, derin=0.05, k_say=8,
                  cerceve=(0.006, 'mermer'))
    else:
        duz_duvar(y, a, b, Z0, Z0 + GH, KIR)
for i in range(9):
    a, b = V(0.58 - 1.16 * i / 9, MY1), V(0.58 - 1.16 * (i + 1) / 9, MY1)
    if i in (3, 4, 5):
        y.kemerli(a + Z * Z0, b + Z * Z0, 0, GH, KAPI, v0=0.0, en=0.55, ust=0.07, derin=0.05, k_say=8, cerceve=(0.006, 'mermer'))
    else:
        duz_duvar(y, a, b, Z0, Z0 + GH, KIR)
for s in (-1, 1):
    # the wing: outer side, front, inner side
    pts = [V(s * WX1, MY1), V(s * WX1, WY0), V(s * WX0, WY0), V(s * WX0, MY0)]
    if s > 0:
        pts = [V(WX0, MY0), V(WX0, WY0), V(WX1, WY0), V(WX1, MY1)]
    for k in range(3):
        duz_duvar(y, pts[k], pts[k + 1], Z0, Z0 + GH, KIR)
# base course and the cornice round the U, the paved top
U = [V(-WX1, WY0), V(-WX0, WY0), V(-WX0, MY0), V(WX0, MY0), V(WX0, WY0), V(WX1, WY0), V(WX1, MY1), V(-WX1, MY1)]
silme(y, U, Z0 + 0.001, 0.02, 0.007, 'mermer', 'kaide')
silme(y, U, Z0 + GH - 0.012, 0.012, 0.007, 'mermer', 'kaba')
ZG = Z0 + GH
for r in ((-WX1, WX1, MY0, MY1), (-WX1, -WX0, WY0, MY0), (WX0, WX1, WY0, MY0)):
    y.yuz_yon(dikdortgen(*r, ZG), 'zemin', Z)
korkuluk(y, [V(p.x, p.y) for p in disa(U, -0.008)], ZG, 0.022, 'mermer', 0.058, True,
         bosluk=())
# the gate hall on the main block
tepe_w = salon(y, 0, (MY0 + MY1) / 2 + 0.005, 0.6, 0.13, ZG, 0.075, 0.1, sacak=0.055, cati_key=SARI, mahya=SARI2, kivrim=0.45,
               yukari=0.03, cift=True, alt_yuk=0.03, ic=0.02, ust_h=0.03, bay=0.06, hayvan=4, mahya_en=0.012)
# long galleries on the wings and the four phoenix pavilions at their ends
for s in (-1, 1):
    kucuk_salon(y, s * WX1 - s * 0.03 if s < 0 else WX0 + 0.03, s * WX0 + s * 0.03 if s < 0 else WX1 - 0.03, WY0 + 0.1, MY0 - 0.005, ZG,
                0.05, 0.04, 0.025, KIR, 'lake', SARI, SARI2, 'besik', 0.4, 0.02, 0.0, kapi_yon=1 if s < 0 else 3, bay=0.05)
    for yc in (WY0 + 0.055, MY1 - 0.055):
        xc = s * (WX0 + WX1) / 2
        kosk_kapali = salon(y, xc, yc, 0.1, 0.08, ZG, 0.06, 0.07, sacak=0.035, cati_key=SARI,
                            mahya=SARI2, kivrim=0.5, yukari=0.025, cift=False, bay=0.05, chiwenli=False, hayvan=0, mahya_en=0.008)
        kure(y, (xc, yc, kosk_kapali + 0.01), 0.011, 'altin', n=8, kat=4)
# banners on the gate's front corners
for s in (-1, 1):
    sancak(y, s * 0.385, MY0 + 0.022, ZG, boy=0.26, en=0.12, yuk=0.075, aci=math.pi / 2 + s * 0.4)

# ---------------------------------------------------------------- the courtyard: Golden Water stream and bridges
y.bolum('Altın Su Deresi')


def dere_y(x):
    return -0.5 - 0.1 * (1 - (x / 0.92) ** 2)


DX = [(-0.86 + 1.72 * i / 30) for i in range(31)]
orta = [V(x, dere_y(x)) for x in DX]
SW = 0.05   # half width of the water
for sg in (-1, 1):
    # each bank: a kerb line along the stream
    kenar = [V(p.x, p.y) for p in disa(orta, sg * SW, kapali=False)]
    dis_ = [V(p.x, p.y) for p in disa(orta, sg * (SW + 0.016), kapali=False)]
    for k in range(len(orta) - 1):
        # (sg > 0: the right of travel is -y side)
        a, b, a2, b2 = kenar[k], kenar[k + 1], dis_[k], dis_[k + 1]
        nn = V((b - a).y, -(b - a).x) * sg
        y.yuz_yon([a + Z * (Z0 + 0.006), b + Z * (Z0 + 0.006), b + Z * (Z0 + 0.016), a + Z * (Z0 + 0.016)], 'mermer', -nn)   # towards the water
        y.yuz_yon([a2 + Z * Z0, b2 + Z * Z0, b2 + Z * (Z0 + 0.016), a2 + Z * (Z0 + 0.016)], 'mermer', nn)
        y.yuz_yon([a + Z * (Z0 + 0.016), b + Z * (Z0 + 0.016), b2 + Z * (Z0 + 0.016), a2 + Z * (Z0 + 0.016)], 'mermer', Z)
    for k in (0, len(orta) - 1):
        a, a2 = kenar[k], dis_[k]
        e = (orta[1] - orta[0]) if k == 0 else (orta[-1] - orta[-2])
        y.yuz_yon([a + Z * Z0, a2 + Z * Z0, a2 + Z * (Z0 + 0.016), a + Z * (Z0 + 0.016)], 'mermer', -e if k == 0 else e)
    mid = [V(p.x, p.y) for p in disa(orta, sg * (SW + 0.008), kapali=False)]
    korkuluk(y, mid, Z0 + 0.016, 0.022, 'mermer', 0.06, kapali=False,
             bosluk=[((bx, dere_y(bx)), 0.095 if bx == 0 else 0.078) for bx in (-0.32, -0.16, 0.0, 0.16, 0.32)])
# the water (just above the paving, inside the kerbs) and the ends of the channel
for k in range(len(orta) - 1):
    a0 = disa(orta, -SW, kapali=False); a1 = disa(orta, SW, kapali=False)
    y.yuz_yon([a0[k] + Z * (Z0 + 0.006), a0[k + 1] + Z * (Z0 + 0.006), a1[k + 1] + Z * (Z0 + 0.006), a1[k] + Z * (Z0 + 0.006)], 'su', Z)
a0 = disa(orta, -SW, kapali=False); a1 = disa(orta, SW, kapali=False)
for k, s in ((0, -1), (len(orta) - 1, 1)):
    e = (orta[1] - orta[0]) if k == 0 else (orta[-1] - orta[-2])
    y.yuz_yon([a0[k] + Z * Z0, a1[k] + Z * Z0, a1[k] + Z * (Z0 + 0.006), a0[k] + Z * (Z0 + 0.006)], 'mermer', e * s)


def kopru(bx, en):
    """a humped marble bridge across the stream at x = bx: a deck rising over the water, solid sides with an arch
    painted dark under it, balustrades on the hump, flared ends"""
    yc = dere_y(bx)
    L = 0.09
    pts = [(-L + 2 * L * k / 8, 0.016 + 0.014 * math.sin(math.pi * k / 8)) for k in range(9)]
    with parca(y, (bx, yc, Z0)):
        for k in range(8):
            (ya, za), (yb, zb_) = pts[k], pts[k + 1]
            y.yuz_yon([V(-en / 2, ya, za), V(en / 2, ya, za), V(en / 2, yb, zb_), V(-en / 2, yb, zb_)], 'mermer', Z)
        for sx in (-1, 1):
            prof = [V(sx * en / 2, ya, 0.0) for ya, _ in pts[:1]] + [V(sx * en / 2, ya, za) for ya, za in pts] + [V(sx * en / 2, pts[-1][0], 0.0)]
            y.yuz_yon(prof, 'mermer', V(sx, 0, 0))
            # the arch under it, painted dark on the side
            arc = [V(sx * (en / 2 + 0.0015), -0.045 + 0.09 * k / 6, 0.0 + 0.016 * math.sin(math.pi * k / 6)) for k in range(7)]
            y.yuz_yon(arc, 'koyu', V(sx, 0, 0))
            # parapet: a solid low rail with posts along the hump
            for k in range(8):
                (ya, za), (yb, zb_) = pts[k], pts[k + 1]
                p0, p1 = V(sx * (en / 2 - 0.003), ya, za), V(sx * (en / 2 - 0.003), yb, zb_)
                cubuk(y, p0 + Z * 0.008, p1 + Z * 0.008, 0.005, 'mermer', 0.016)
            for k in (0, 4, 8):
                ya, za = pts[k]
                dikme(y, V(sx * (en / 2 - 0.003), ya), V(0, 1), za, 0.024, 'mermer', 0.0075)
        for ya, s in ((-L, -1), (L, 1)):
            y.yuz_yon([V(-en / 2, ya, 0), V(en / 2, ya, 0), V(en / 2, ya, 0.016), V(-en / 2, ya, 0.016)], 'mermer', V(0, s, 0))


for bx in (-0.32, -0.16, 0.0, 0.16, 0.32):
    kopru(bx, 0.07 if bx == 0 else 0.055)

# the imperial way: a marble path from the gate to the terrace stairs
for ya, yb in ((MY1, dere_y(0) - 0.09), (dere_y(0) + 0.09, -0.32)):
    kutu(y, V(-0.05, ya, Z0), X, 0.1, yb - ya, 0.003, 'mermer', 'onarkasagsolust')
for ya, yb in ((MY1, dere_y(0) - 0.09), (dere_y(0) + 0.09, -0.32)):
    for sx in (-1, 1):
        kutu(y, V(sx * 0.07 - 0.012, ya, Z0), X, 0.024, yb - ya, 0.002, 'tas_acik', 'onarkasagsolust')

# ---------------------------------------------------------------- side galleries and pavilions
y.bolum('Yan revaklar')
for s in (-1, 1):
    x0, x1 = (-1.07, -0.92) if s < 0 else (0.92, 1.07)
    for ya, yb in ((-0.7, -0.08), (0.42, 0.97)):
        kucuk_salon(y, x0, x1, ya, yb, Z0, 0.065, 0.05, 0.03, KIR, 'lake', SARI, SARI2, 'besik', 0.4, 0.02, 0.012, 'mermer',
                    kapi_yon=1 if s < 0 else 3, bay=0.085, arka_duz=True)
    # the pavilion in the middle (Tirenge / Hongyige): two storeys, facing the courtyard
    with parca(y, (s * 0.97, 0.17, 0), -s * math.pi / 2):
        tp = salon(y, 0, 0, 0.32, 0.17, Z0, 0.09, 0.09, sacak=0.05, cati_key=SARI, mahya=SARI2, kivrim=0.45, yukari=0.03, cift=True,
                   alt_yuk=0.03, ic=0.022, ust_h=0.06, bay=0.064, cati='irimoya', kaide=(0.025, 'mermer'), hayvan=0, chiwenli=False,
                   mahya_en=0.01)

# ---------------------------------------------------------------- the three-tier marble terrace
y.bolum('Mermer teras')
TC = 0.32
KAT = [(0.72, 0.54), (0.64, 0.46), (0.56, 0.38)]   # half sizes x, y
TH = 0.065
z = Z0
for i, (hx, hy) in enumerate(KAT):
    k = dikdortgen(-hx, hx, TC - hy, TC + hy)
    stair = [((0, TC - hy), 0.24), ((0, TC + hy), 0.16)]
    zt = teras(y, k, z, TH, 'mermer', 'zemin', True, stair, 0.056, 0.024, 0.008, oluk='tas_acik' if i == 2 else None)
    teras_merdiven(y, (0, TC - hy - TH * 1.15), math.pi / 2, 0.22, z, zt, 6, 'mermer', rampa='mermer', rampa_en=0.08)
    teras_merdiven(y, (0, TC + hy + TH * 1.15), -math.pi / 2, 0.14, z, zt, 6, 'mermer')
    z = zt
ZT = z

# ---------------------------------------------------------------- Taihedian
y.bolum('Taihedian')
HC = TC + 0.11
tepe = salon(y, 0, HC, 0.94, 0.38, ZT, 0.18, 0.235, sacak=0.09, cati_key=SARI, mahya=SARI2, kivrim=0.42, yukari=0.04, cift=True,
             alt_yuk=0.06, alt_sacak=0.085, ic=0.05, ust_h=0.08, bay=0.085, hayvan=6, mahya_en=0.02, kaide=(0.012, 'mermer'))

# ---------------------------------------------------------------- the terrace furniture
y.bolum('Teras süsleri')
FY = TC - KAT[2][1] + 0.12
for s in (-1, 1):
    tutsu(y, s * 0.18, FY, ZT, 1.2)
    kazan(y, s * 0.42, FY + 0.02, ZT, 1.3)
    kazan(y, s * 0.42, TC + 0.28, ZT, 1.1)
    # the sundial (east) and the grain measure (west) on little marble stands
    kutu_merkez(y, (s * 0.3, FY - 0.04), 0.04, 0.04, 0.02, 'mermer', z0=ZT)
    if s > 0:
        p = V(0.3, FY - 0.04, ZT + 0.03)
        y.prizma((p.x, p.y), 0.004, ZT + 0.02, p.z + 0.01, 'mermer', n=6)
        donel(y, (p.x, p.y), [(0.0, p.z), (0.018, p.z + 0.002), (0.018, p.z + 0.006), (0.0, p.z + 0.006)], 'mermer', n=12)
    else:
        kutu_merkez(y, (-0.3, FY - 0.04), 0.022, 0.022, 0.02, 'bronz', z0=ZT + 0.02)
        kucuk = cati_kirma(y, -0.315, -0.285, FY - 0.055, FY - 0.025, ZT + 0.04, 0.014, 0.006, SARI, SARI2, 0.004, 0.4, 0.004, 'lake_koyu',
                           ns=4, nr=3, mahya_en=0.004)
    # bronze crane and tortoise
    kure(y, (s * 0.12, FY - 0.06, ZT + 0.012), 0.012, 'bronz', n=8, kat=4)
    cubuk(y, V(s * 0.12, FY - 0.06, ZT + 0.018), V(s * 0.12, FY - 0.066, ZT + 0.05), 0.004, 'bronz')
# guardian lions at the foot of the front stairs
for s in (-1, 1):
    aslan(y, s * 0.17, TC - KAT[0][1] - 0.11, Z0, math.pi / 2, 1.2)
# vats along the courtyard
for s in (-1, 1):
    for yy in (-0.2, 0.62):
        kazan(y, s * 0.82, yy, Z0, 1.25)

sayim(y)
calistir(y, 'lm_yasaksehir')
