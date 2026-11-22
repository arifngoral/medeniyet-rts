# Cennet Tapınağı (lm_cennettapinagi): the Temple of Heaven, Beijing. Qiniandian (Hall of Prayer for Good Harvests), a
# round hall with three tiers of dark blue glazed conical roofs and a gilt finial, on its three-tier round white marble
# altar with balustrades and a carved dragon ramp, inside a red walled court with its gate and annex halls; in front
# the raised Danbi causeway, the Imperial Vault of Heaven within the round Echo Wall, the open three-tier Circular Mound
# Altar (Huanqiu) in its round and square low walls with white marble lingxing gates, and old cypresses.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ek import *
from bina_ortak import calistir

y = Yapi()
MAVI, MAVI2 = 'kiremit_kobalt', 'kobalt'
KIR = 'siva_kirmizi'

# ---------------------------------------------------------------- ground
y.bolum('Zemin')
Z0 = zemin(y, -1.2, 1.2, -1.2, 1.2, 0.03, 'tas_koyu', 'cimen', basamak=(('on', 0.3),), n_basamak=2)


def doseme(x0, x1, y0, y1, key='zemin', h=0.003):
    kutu(y, V(x0, y0, Z0), X, x1 - x0, y1 - y0, h, key, 'onarkasagsolust')


# ---------------------------------------------------------------- Qiniandian court
y.bolum('Avlu duvarı')
QC = (0.0, 0.45)
EX0, EX1, EY0, EY1 = -0.8, 0.8, -0.24, 1.14
doseme(EX0 + 0.02, EX1 - 0.02, EY0 + 0.02, EY1 - 0.02, 'zemin')
kirmizi_sur(y, [V(0.17, EY0), V(EX1, EY0), V(EX1, EY1), V(EX0, EY1), V(EX0, EY0), V(-0.17, EY0)], Z0, 0.085, 0.03, KIR, MAVI, MAVI2,
            kapali=False, baslik=0.026)
# the gate of the court (Qinianmen)
y.bolum('Qinian kapısı')
kucuk_salon(y, -0.19, 0.19, EY0 - 0.055, EY0 + 0.055, Z0 + 0.003, 0.085, 0.07, 0.04, KIR, 'lake', MAVI, MAVI2, 'irimoya', 0.45, 0.025,
            0.02, 'mermer', kapi_yon=0, bay=0.063)
for s in (-1, 1):
    aslan(y, s * 0.13, EY0 - 0.12, Z0, math.pi / 2, 1.0)
# annex halls in the court's back corners
for s in (-1, 1):
    x0, x1 = (0.53, 0.73) if s > 0 else (-0.73, -0.53)
    kucuk_salon(y, x0, x1, 0.8, 1.08, Z0 + 0.003, 0.075, 0.06, 0.035, KIR, 'lake', MAVI, MAVI2, 'irimoya', 0.45, 0.025, 0.02, 'mermer',
                kapi_yon=3 if s > 0 else 1, bay=0.065, arka_duz=True)

# ---------------------------------------------------------------- the round marble altar (Qigu tan)
y.bolum('Mermer sunak')
KAT = (0.6, 0.52, 0.44)
TH = 0.055
YON = (-math.pi / 2, math.pi / 2, 0.0, math.pi)       # south (front), north, east, west
z = Z0 + 0.003
for i, r in enumerate(KAT):
    k = cokgen(QC, r, 40, 0.0)
    bos = [((QC[0] + (r - 0.01) * math.cos(a), QC[1] + (r - 0.01) * math.sin(a)), 0.25 if a == YON[0] else 0.17) for a in YON]
    zt = teras(y, k, z, TH, 'mermer', 'mermer', True, bos, 0.05, 0.024, 0.008, oluk='tas_acik' if i == 2 else None)
    run = TH * 1.15
    for a in YON:
        d = V(math.cos(a), math.sin(a))
        foot = V(QC[0], QC[1]) + d * (r + run - 0.012)
        if a == YON[0]:
            teras_merdiven(y, foot, a + math.pi, 0.22, z, zt, 6, 'mermer', rampa='mermer', rampa_en=0.08)
        else:
            teras_merdiven(y, foot, a + math.pi, 0.14, z, zt, 6, 'mermer')
    z = zt
ZT = z

# ---------------------------------------------------------------- Qiniandian
y.bolum('Qiniandian')
N = 24
R1, R2, R3 = 0.29, 0.235, 0.18
# a low marble plinth under the hall
duvarlar(y, cokgen(QC, R1 + 0.03, N), ZT, ZT + 0.012, 'mermer', ust='mermer')
z = ZT + 0.012
z = yuvarlak_govde(y, QC, R1, N, z, 0.2, pencere=(0.0, 1.0))
z = yuvarlak_konsol(y, QC, R1, N, z)
k1 = 0.25
t = 1 - (R2 - 0.01) / (R1 + 0.095)
z2, _ = cokgen_cati(y, QC, R1, N, z, egim_icin(0.055, t, k1), 0.095, MAVI, MAVI2, k1, 0.0, R2 - 0.01, ns=1, nr=4,
                    alt_key='lake_koyu', sirt=False, kalinlik=0.014)
# the second drum: red walls with a band of lattice windows
duvarlar(y, cokgen(QC, R2, N), z, z2 + 0.004, KIR)
z = yuvarlak_govde(y, QC, R2, N, z2 + 0.004, 0.11, pencere=(0.25, 0.85), direk_r=0.009)
z = yuvarlak_konsol(y, QC, R2, N, z)
t = 1 - (R3 - 0.01) / (R2 + 0.085)
z3, _ = cokgen_cati(y, QC, R2, N, z, egim_icin(0.05, t, k1), 0.085, MAVI, MAVI2, k1, 0.0, R3 - 0.01, ns=1, nr=4,
                    alt_key='lake_koyu', sirt=False, kalinlik=0.013)
duvarlar(y, cokgen(QC, R3, N), z, z3 + 0.004, KIR)
z = yuvarlak_govde(y, QC, R3, N, z3 + 0.004, 0.1, pencere=(0.25, 0.85), direk_r=0.008)
z = yuvarlak_konsol(y, QC, R3, N, z)
tepe, _ = cokgen_cati(y, QC, R3, N, z, 0.2, 0.085, MAVI, MAVI2, 0.38, 0.0, 0.0, ns=1, nr=7, alt_key='lake_koyu', sirt=False,
                      kalinlik=0.013)
# the gilt finial: a lotus collar, a stem and a great ball
donel(y, QC, [(0.03, tepe - 0.02), (0.034, tepe - 0.004), (0.022, tepe + 0.006), (0.012, tepe + 0.012), (0.012, tepe + 0.03),
              (0.0, tepe + 0.03)], 'altin', n=12)
kure(y, (QC[0], QC[1], tepe + 0.058), 0.03, 'altin', n=14, kat=7)
y.prizma(QC, 0.004, tepe + 0.086, tepe + 0.11, 'altin', n=6)
# bronze censers and vats on the altar
for s in (-1, 1):
    tutsu(y, QC[0] + s * 0.16, QC[1] - 0.36, ZT, 1.1)

# ---------------------------------------------------------------- Danbi causeway and paths
y.bolum('Danbi yolu')
VC = (0.0, -0.8)
RE = 0.28
DH = 0.03
# the raised causeway from the Echo Wall's north gate to the court gate
dk = dikdortgen(-0.1, 0.1, VC[1] + RE - 0.02, EY0 - 0.07)
duvarlar(y, dk, Z0, Z0 + DH, 'tas_acik', ust='zemin')
silme(y, dk, Z0 + DH - 0.006, 0.006, 0.004, 'mermer', 'kaba')
kutu(y, V(-0.035, dk[0].y, Z0 + DH), X, 0.07, dk[2].y - dk[0].y, 0.003, 'mermer', 'onarkasagsolust')
merdiven(y, (0, VC[1] + RE - 0.02 - 0.04), math.pi / 2, 0.16, Z0, Z0 + DH, 3, 0.013, 'mermer')
# the paths to the round altar and the side of the court
doseme(-0.06, 0.06, -1.2, VC[1] - RE - 0.015, 'zemin')

# ---------------------------------------------------------------- the Imperial Vault of Heaven in the Echo Wall
y.bolum('Gök Kubbesi Salonu')
ew = cokgen(VC, RE, 40, 0.0)
# the Echo Wall (gaps north for the causeway and south for the gate)
yol = [V(VC[0] + RE * math.cos(a), VC[1] + RE * math.sin(a)) for a in [math.pi / 2 + 0.4 + (TAU / 2 - 0.8) * k / 16 for k in range(17)]]
kirmizi_sur(y, yol, Z0, 0.075, 0.022, KIR, MAVI, MAVI2, kapali=False, baslik=0.02)
yol = [V(VC[0] + RE * math.cos(a), VC[1] + RE * math.sin(a)) for a in [-math.pi / 2 + 0.4 + (TAU / 2 - 0.8) * k / 16 for k in range(17)]]
kirmizi_sur(y, yol, Z0, 0.075, 0.022, KIR, MAVI, MAVI2, kapali=False, baslik=0.02)
# the south gate in the wall (three openings under a blue roof)
kucuk_salon(y, -0.118, 0.118, VC[1] - RE - 0.03, VC[1] - RE + 0.03, Z0, 0.07, 0.05, 0.03, KIR, 'lake', MAVI, MAVI2, 'irimoya', 0.4, 0.02,
            0.0, kapi_yon=0, bay=0.067)
doseme(-0.24, 0.24, VC[1] - 0.24, VC[1] + 0.24, 'zemin')
# the vault: a round hall on a railed marble terrace, one blue conical roof
vz = teras(y, cokgen(VC, 0.15, 32), Z0 + 0.003, 0.045, 'mermer', 'mermer', True, [((VC[0], VC[1] - 0.145), 0.1)], 0.045, 0.02, 0.007)
teras_merdiven(y, (VC[0], VC[1] - 0.15 - 0.045 * 1.15 + 0.008), math.pi / 2, 0.09, Z0 + 0.003, vz, 5, 'mermer')
z = yuvarlak_govde(y, VC, 0.095, 16, vz, 0.11, pencere=(0.0, 1.0), direk_r=0.008)
z = yuvarlak_konsol(y, VC, 0.095, 16, z, adim=0.045, h=0.016)
tv, _ = cokgen_cati(y, VC, 0.095, 16, z, 0.13, 0.055, MAVI, MAVI2, 0.35, 0.0, 0.0, ns=1, nr=6, alt_key='lake_koyu', sirt=False,
                    kalinlik=0.012)
donel(y, VC, [(0.014, tv - 0.01), (0.016, tv + 0.002), (0.006, tv + 0.01), (0.006, tv + 0.02), (0.0, tv + 0.02)], 'altin', n=10)
kure(y, (VC[0], VC[1], tv + 0.036), 0.018, 'altin', n=10, kat=5)
# the two side halls in the court
for s in (-1, 1):
    with parca(y, (VC[0] + s * 0.175, VC[1] + 0.0, 0), -s * math.pi / 2):
        kucuk_salon(y, -0.065, 0.065, -0.032, 0.032, Z0 + 0.003, 0.06, 0.045, 0.03, KIR, 'lake', MAVI, MAVI2, 'besik', 0.4, 0.02, 0.012,
                    'mermer', kapi_yon=0, bay=0.055, arka_duz=True)

# ---------------------------------------------------------------- the Circular Mound Altar (Huanqiu)
y.bolum('Yuvarlak sunak')
AC = (-0.76, -0.8)
# outer square low wall and inner round low wall, white lingxing gates on the four axes
for kose, kap in ((dikdortgen(AC[0] - 0.39, AC[0] + 0.39, AC[1] - 0.37, AC[1] + 0.37), True), (cokgen(AC, 0.275, 40, 0.0), True)):
    # split the ring at the four gates
    P = ornekle(kose, 0.025)
    acik = lambda p: any(abs((p.x - AC[0]) * math.sin(a) - (p.y - AC[1]) * math.cos(a)) < 0.07 and ((p.x - AC[0]) * math.cos(a) + (p.y - AC[1]) * math.sin(a)) > 0
                         for a in YON)
    parca_ = []
    cur = []
    n = len(P)
    bas = next(i for i in range(n) if acik(P[i]))
    for kk in range(1, n + 1):
        p = P[(bas + kk) % n]
        if acik(p):
            if len(cur) >= 2:
                parca_.append(cur)
            cur = []
        else:
            cur.append(p)
    for yol in parca_:
        kirmizi_sur(y, yol, Z0, 0.045, 0.022, KIR, MAVI, MAVI2, kapali=False, baslik=0.016)
for a in YON:
    for rr in (0.275, 0.38):
        d = V(math.cos(a), math.sin(a))
        p = V(AC[0], AC[1]) + d * (rr if rr < 0.3 else (0.39 if abs(d.x) > 0.5 else 0.37))
        tas_kapi(y, p.x, p.y, Z0, 0.12 if rr < 0.3 else 0.15, 0.076 if rr < 0.3 else 0.09, 'mermer', 'tas_acik', 3, 0.011, a + math.pi / 2)
# the three open tiers
doseme(AC[0] - 0.3, AC[0] + 0.3, AC[1] - 0.3, AC[1] + 0.3, 'zemin')
z = Z0 + 0.003
for i, r in enumerate((0.22, 0.17, 0.12)):
    k = cokgen(AC, r, 36, 0.0)
    bos = [((AC[0] + (r - 0.01) * math.cos(a), AC[1] + (r - 0.01) * math.sin(a)), 0.09) for a in YON]
    zt = teras(y, k, z, 0.034, 'mermer', 'mermer', True, bos, 0.045, 0.02, 0.007)
    for a in YON:
        d = V(math.cos(a), math.sin(a))
        teras_merdiven(y, V(AC[0], AC[1]) + d * (r + 0.034 * 1.15 - 0.01), a + math.pi, 0.075, z, zt, 4, 'mermer', yanlik=False)
    z = zt
# the Heart of Heaven stone and the rings of paving round it
for r0, r1 in ((0.0, 0.016), (0.035, 0.04), (0.06, 0.065), (0.085, 0.09)):
    ring = lambda r: [V(AC[0] + r * math.cos(TAU * i / 24), AC[1] + r * math.sin(TAU * i / 24), z + 0.0015) for i in range(24)]
    if r0 == 0:
        y.yuz_yon(ring(r1), 'tas_acik', Z)
    else:
        A, B = ring(r0), ring(r1)
        for i in range(24):
            j = (i + 1) % 24
            y.yuz_yon([A[i], A[j], B[j], B[i]], 'tas_acik', Z)
# the burning stove (green-glazed) and iron braziers
kutu_merkez(y, (AC[0] + 0.32, AC[1] + 0.33), 0.05, 0.04, 0.04, 'kiremit_yesil', z0=Z0)
cati_kirma(y, AC[0] + 0.295, AC[0] + 0.345, AC[1] + 0.31, AC[1] + 0.35, Z0 + 0.04, 0.02, 0.008, 'kiremit_yesil', 'kiremit_yesil', 0.004,
           0.4, 0.004, 'lake_koyu', ns=4, nr=3, mahya_en=0.005)

# ---------------------------------------------------------------- cypresses, a pavilion, the banner
y.bolum('Selviler')
for (x, yy) in ((0.42, -0.62), (0.55, -0.85), (0.72, -0.6), (0.88, -0.82), (0.62, -1.05), (0.95, -1.08), (0.4, -1.05),
                (-1.0, -0.2), (-1.02, 0.15), (-1.0, 0.5), (-1.02, 0.85), (1.0, -0.2), (1.02, 0.15), (1.0, 0.5), (1.02, 0.85),
                (-0.95, 1.08), (0.95, 1.08), (-1.1, -1.12), (-0.45, -1.12), (-0.24, -0.38), (0.3, -0.37)):
    servi(y, x, yy, Z0, 0.17)
kosk(y, (0.76, -0.34), 0.11, Z0, 0.08, 0.06, 0.035, 'lake', MAVI, MAVI2, 0.5, 0.025, 'mermer', n=6)
sancak(y, 0.24, -0.33, Z0, boy=0.3, en=0.13, yuk=0.08, aci=0.3)

sayim(y)
calistir(y, 'lm_cennettapinagi')
