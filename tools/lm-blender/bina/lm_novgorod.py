# Novgorod Ayasofya Katedrali (lm_novgorod): St Sophia of Novgorod (1045-1050): a whitewashed stone cross-in-square
# body whose walls end in round zakomara gables over a vaulted roof, flat pilasters, narrow slit windows, three apses,
# a west porch with the bronze Magdeburg doors, five helmet domes (the central one gilded, four of lead) and the sixth
# over the round stair tower; beside it the arched bell wall (zvonnitsa) and a corner of the red brick Detinets wall
# with its timber-roofed walk and tent-roofed towers; birches on the green.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from rus_ortak import *
from bina_ortak import calistir
import doku

y = Yapi()
Z0 = 0.04
doku.KOSE_RENK['cimen'] = cayir_renk(Z0)
TC = V(-0.08, 0.14)                     # the cathedral's centre
XB = [TC.x + q for q in (-0.44, -0.17, 0.17, 0.44)]
YB = [TC.y + q for q in (-0.37, -0.125, 0.125, 0.37)]
ZS = Z0 + 0.47                          # the zakomaras spring here
DUV = 'siva'

# ---------------------------------------------------------------- ground
y.bolum('Zemin')
RX, ZW = 0.97, Z0 - 0.022                # the Volkhov: its bank and water level
zemin_blok(y, -1.16, RX, -1.1, 1.1, Z0, 'cimen', 'toprak', yanlar='onarkasol')
duz_duvar(y, V(RX, -1.1), V(RX, 1.1), ZW - 0.004, Z0, 'toprak')
y.yuz_yon([V(RX, -1.1, ZW), V(1.16, -1.1, ZW), V(1.16, 1.1, ZW), V(RX, 1.1, ZW)], 'su', Z)
duz_duvar(y, V(RX, -1.1), V(1.16, -1.1), 0, ZW, 'toprak')
duz_duvar(y, V(1.16, 1.1), V(RX, 1.1), 0, ZW, 'toprak')
duz_duvar(y, V(1.16, -1.1), V(1.16, 1.1), 0, ZW, 'toprak')
yer = lambda pts, k: y.yuz_yon([V(p[0], p[1], Z0 + 0.002) for p in pts], k, Z)
yer([(XB[0] - 0.16, YB[0] - 0.3), (XB[-1] + 0.14, YB[0] - 0.3), (XB[-1] + 0.14, YB[-1] + 0.22), (XB[0] - 0.16, YB[-1] + 0.22)], 'zemin')
yer([(TC.x - 0.09, -1.1), (TC.x + 0.09, -1.1), (TC.x + 0.09, YB[0] - 0.3), (TC.x - 0.09, YB[0] - 0.3)], 'zemin')
yer([(0.3, -0.62), (0.9, -0.62), (0.9, -0.4), (0.3, -0.4)], 'zemin')


# ---------------------------------------------------------------- cathedral body
def pen(ad, i, ua, ub):
    um, w = (ua + ub) / 2, ub - ua
    alt = [(um, 0.0, 0.034, 0.11)] if w < 0.3 else [(um - 0.06, 0.0, 0.032, 0.11), (um + 0.06, 0.0, 0.032, 0.11)]
    ust = [(um, 0.0, 0.03, 0.09)] if w < 0.3 else [(um - 0.055, 0.0, 0.028, 0.09), (um, 0.0, 0.03, 0.1), (um + 0.055, 0.0, 0.028, 0.09)]
    if ad == 'arka':
        return [(0.32, 0.43, ust)]
    if ad == 'sol':   # behind the gallery
        return None
    if ad == 'on' and i == 1:   # behind the porch: only the upper row
        return [(0.32, 0.43, ust)]
    return [(0.1, 0.24, alt), (0.3, 0.42, ust)]


y.bolum('Katedral gövdesi ve zakomaralar')
H = zakomara_govde(y, XB, YB, Z0, ZS, DUV, 'kursun', pencere=pen, pen_key='tas_acik', m=10)
# small round windows in the gables of the two seen fronts
for i in range(3):
    xm, R = (XB[i] + XB[i + 1]) / 2, (XB[i + 1] - XB[i]) / 2
    y.oculus(V(xm, YB[0], ZS + R * 0.42), X, -Y, 0.022, 'koyu', 'tas_acik', f=0.006, k=12)
    ym, R = (YB[i] + YB[i + 1]) / 2, (YB[i + 1] - YB[i]) / 2
    y.oculus(V(XB[-1], ym, ZS + R * 0.42), Y, X, 0.018, 'koyu', 'tas_acik', f=0.006, k=12)
# a thin cornice band at the springing of the gables, round all four sides
silme(y, dikdortgen(XB[0], XB[-1], YB[0], YB[-1]), ZS - 0.008, 0.008, 0.005, 'tas_acik', 'duz')

y.bolum('Apsisler')
for x, r, h in ((XB[0] + 0.135, 0.1, 0.3), (TC.x, 0.15, 0.36), (XB[-1] - 0.135, 0.1, 0.3)):
    apsis(y, (x, YB[-1]), r, Z0, h, math.pi / 2, DUV, 'kursun', n=10, pen_key='tas_acik')

y.bolum('Batı sundurması ve tunç kapı')
PX = [TC.x - 0.12, TC.x + 0.12]
PY = [YB[0] - 0.15, YB[0] + 0.004]
PZ = Z0 + 0.23


def pen_p(ad, i, ua, ub):
    if ad == 'on':
        um = (ua + ub) / 2
        return [(0.0, 0.2, [(um, 0.0, 0.1, 0.17, 'bronz', (0.012, ['tas_acik']))])]
    return [(0.08, 0.2, [((ua + ub) / 2, 0.0, 0.03, 0.08)])]


zakomara_govde(y, PX, PY, Z0, PZ, DUV, 'kursun', pencere=pen_p, yuzler=('on', 'sag', 'sol'), arka_duvar=False, lesene=True)
# the doors' leaves: two bronze panels with studs, a little proud of the back of the opening
for k in range(2):
    for j in range(4):
        kutu_merkez(y, (TC.x - 0.025 + k * 0.05, PY[0] + 0.0175), 0.036, 0.002, 0.03, 'altin', z0=Z0 + 0.012 + j * 0.036)

y.bolum('Kubbeler')
zc = kubbe_kule(y, (TC.x, TC.y), 0.125, ZS + 0.12, 0.28, 'shlem', 'altin', DUV, n=16, pencere=8, dome_h=0.14, hac_h=0.13,
                kornis_key='tas_acik')
for sx in (-1, 1):
    for sy in (-1, 1):
        c = (TC.x + sx * 0.305, TC.y + sy * 0.25)
        kubbe_kule(y, c, 0.075, ZS + 0.1, 0.2, 'shlem', 'kursun', DUV, n=12, pencere=4, dome_h=0.085, hac_h=0.09,
                   kornis_key='tas_acik', n_dome=24, alt=2, arkatur=True)

y.bolum('Sol galeri')
GXB = [XB[0] - 0.17, XB[0] + 0.004]
GYB = [YB[0], YB[0] + 0.245, YB[-1] - 0.245, YB[-1]]
GZ = Z0 + 0.27


def pen_g(ad, i, ua, ub):
    um = (ua + ub) / 2
    if ad == 'sol':
        return [(0.1, 0.22, [(um - 0.05, 0.0, 0.03, 0.1), (um + 0.05, 0.0, 0.03, 0.1)])] if i != 0 else [(0.1, 0.22, [(um + 0.03, 0.0, 0.03, 0.1)])]
    return [(0.1, 0.22, [(um, 0.0, 0.032, 0.1)])]


zakomara_govde(y, GXB, GYB, Z0, GZ, DUV, 'kursun', pencere=pen_g, yuzler=('on', 'sol', 'arka'), arka_duvar=False)

y.bolum('Merdiven kulesi')
SC = V(GXB[0] + 0.01, YB[0] + 0.02)
donel(y, SC, [(0.088, Z0), (0.085, ZS + 0.12)], DUV, n=20)
silme(y, cokgen(SC, 0.088, 20), Z0, 0.03, 0.012, DUV, 'kaide')
for k in range(5):
    a = -math.pi * 0.75 + k * 0.5
    nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
    yarik(y, SC + nn * 0.086 + Z * Z0, e, nn, -0.006, 0.08 + k * 0.085, 0.012, 0.05, 'koyu')
silme(y, cokgen(SC, 0.086, 20), ZS + 0.105, 0.015, 0.01, 'tas_acik', 'kaba')
y.yuz_yon([V(p.x, p.y, ZS + 0.12) for p in cokgen(SC, 0.096, 20)], 'tas_acik', Z)
kubbe_kule(y, SC, 0.06, ZS + 0.12, 0.13, 'shlem', 'kursun', DUV, n=10, pencere=5, dome_h=0.07, hac_h=0.08, kornis_key='tas_acik', n_dome=20, alt=2)

# ---------------------------------------------------------------- the bell wall
y.bolum('Çan duvarı (zvonnitsa)')
BC = V(0.6, -0.5)
BL, BD = 0.5, 0.09
bx0, bx1 = BC.x - BL / 2, BC.x + BL / 2
by0, by1 = BC.y - BD / 2, BC.y + BD / 2
ZA0, ZA1 = Z0 + 0.15, Z0 + 0.34          # the arcade zone
duvarlar(y, dikdortgen(bx0, bx1, by0, by1), Z0, ZA0, DUV)
silme(y, dikdortgen(bx0, bx1, by0, by1), Z0, 0.025, 0.01, DUV, 'kaide')
silme(y, dikdortgen(bx0, bx1, by0, by1), ZA0 - 0.012, 0.012, 0.007, 'tas_acik', 'kaba')
kapi(y, V(BC.x - 0.05, by0 - 0.001), V(BC.x + 0.05, by0 - 0.001), Z0, 0.6, 0.12, (DUV, DUV, 'tas_acik', 'ahsap'), derin=0.015)
for u in (-0.17, 0.17):
    y.pencere(V(BC.x + u, by0 - 0.0015, Z0), X, -Y, -0.008, 0.06, 0.016, 0.04, 'koyu')
# four pass-through arches holding bells
NA = 4
xa = [bx0 + BL * i / NA for i in range(NA + 1)]
for i in range(NA):
    a, b = xa[i], xa[i + 1]
    w = b - a
    o0, o1 = a + w * 0.18, b - w * 0.18
    R = (o1 - o0) / 2; xm = (o0 + o1) / 2
    hs = ZA1 - 0.035 - R
    arc = [(xm - R * math.cos(math.pi * k / 10), hs + R * math.sin(math.pi * k / 10)) for k in range(11)]
    for yy, sy in ((by0, -1), (by1, 1)):
        nn = V(0, sy)
        P = lambda u, z: V(u, yy, z)
        y.yuz_yon([P(a, ZA0), P(o0, ZA0), P(o0, ZA1), P(a, ZA1)], DUV, nn)
        y.yuz_yon([P(o1, ZA0), P(b, ZA0), P(b, ZA1), P(o1, ZA1)], DUV, nn)
        for k in range(10):
            (u1, z1), (u2, z2) = arc[k], arc[k + 1]
            y.yuz_yon([P(u1, z1), P(u2, z2), P(u2, ZA1), P(u1, ZA1)], DUV, nn)
    # the reveal through the wall
    ring = [(o0, ZA0), (o0, hs)] + arc[1:-1] + [(o1, hs), (o1, ZA0)]
    for k in range(len(ring) - 1):
        (u1, z1), (u2, z2) = ring[k], ring[k + 1]
        mid = V((u1 + u2) / 2, BC.y, (z1 + z2) / 2)
        y.yuz_yon([V(u1, by0, z1), V(u2, by0, z2), V(u2, by1, z2), V(u1, by1, z1)], 'tas_acik' if k else DUV, V(xm, BC.y, hs) - mid)
    y.yuz_yon([V(o0, by0, ZA0), V(o1, by0, ZA0), V(o1, by1, ZA0), V(o0, by1, ZA0)], 'tas_acik', Z)
    # the bell on its beam
    cubuk(y, V(o0, BC.y, hs + R * 0.55), V(o1, BC.y, hs + R * 0.55), 0.008, 'ahsap_koyu')
    s = 0.85 if i in (1, 2) else 0.65
    zb = hs + R * 0.55 - 0.004
    donel(y, (xm, BC.y), [(0.0, zb - 0.085 * s), (0.034 * s, zb - 0.085 * s), (0.03 * s, zb - 0.07 * s), (0.02 * s, zb - 0.035 * s),
                          (0.017 * s, zb - 0.01 * s), (0.008 * s, zb), (0.0, zb)], 'bronz', n=14)
for xx, ss in ((bx0, -1), (bx1, 1)):   # the arcade's end walls
    y.yuz_yon([V(xx, by0, ZA0), V(xx, by1, ZA0), V(xx, by1, ZA1), V(xx, by0, ZA1)], DUV, V(ss, 0))
silme(y, dikdortgen(bx0, bx1, by0, by1), ZA1 - 0.01, 0.01, 0.006, 'tas_acik', 'duz')
# the top: a gable over each bay with a small onion on a drum
XBB = [bx0 + BL * i / NA for i in range(NA + 1)]
zakomara_govde(y, XBB, [by0, by1], ZA1 - 0.001, ZA1, DUV, 'kursun', lesene=False, kaide=False, kemer_bant=True, m=6)
for i in range(NA):
    c = ((XBB[i] + XBB[i + 1]) / 2, BC.y)
    kubbe_kule(y, c, 0.034, ZA1 + 0.03, 0.07, 'sogan', 'kursun', DUV, n=8, pencere=0, dome_h=0.065, hac_h=0.055, kornis_key='tas_acik')

# ---------------------------------------------------------------- Detinets wall
y.bolum('Detinets suru')
WY, WX = 0.98, -1.02
yol = [V(0.78, WY), V(WX, WY), V(WX, -0.72)]
WT, WH = 0.075, 0.22
sur(y, yol, Z0, WH, kalinlik=WT, key='tugla', mazgal_h=0.04, parapet_h=0.014, ust_key='zemin', konsol=False)
# the timber roof over the wall walk, segment by segment
for (p, q) in ((yol[0], yol[1]), (yol[1], yol[2])):
    xs, ys = sorted((p.x, q.x)), sorted((p.y, q.y))
    if abs(p.y - q.y) < 1e-6:
        x0, x1, y0, y1 = xs[0] + 0.08, xs[1] - 0.08, p.y - WT, p.y
    else:
        x0, x1, y0, y1 = p.x, p.x + WT, ys[0] + 0.08, ys[1] - 0.08
    cati_besik(y, x0, x1, y0, y1, Z0 + WH + 0.075, 0.06, 0.018, 'sindira', 'ahsap_koyu', kalinlik=0.008, ucluk_key='ahsap_dikey',
               uc_sacak=0.0, nr=3, ns=14, dilim=['sindira', 'sindira2'])
    # posts carrying the roof
    L = (q - p).length; e = (q - p) / L; ni = V(-e.y, e.x)
    for k in range(1, int(L / 0.12)):
        pp = p + e * (k * 0.12) + ni * (WT * 0.85)
        y.prizma((pp.x, pp.y), 0.005, Z0 + WH, Z0 + WH + 0.076, 'ahsap_koyu', n=5, ust=False)
    # two staggered rows of loopholes on the outer face (the ends hidden in the towers skipped)
    no = V(e.y, -e.x)
    for row, (zz, hh) in enumerate(((WH * 0.5, 0.04), (WH * 0.14, 0.03))):
        k = 0
        while True:
            u = 0.17 + 0.15 * k + (0.075 if row else 0)
            k += 1
            if u > L - 0.15: break
            yarik(y, p + Z * Z0, e, no, u - 0.005, zz, 0.01, hh, 'koyu')
# towers: the round corner tower (Kokuy-like, its tent roof with a lookout) and two square ones
t = kule_yuvarlak(y, (WX + 0.01, WY - 0.01), 0.12, Z0, 0.4, 'tugla', cati='konik', cati_key='sindira', cati_h=0.3, n=20,
                  mazgal_h=0.0, konsol=True)
y.prizma((WX + 0.01, WY - 0.01), 0.004, t - 0.01, t + 0.06, 'ahsap_koyu', n=5)
kure(y, (WX + 0.01, WY - 0.01, t + 0.06), 0.01, 'altin', n=8, kat=4)
for (cx, cy) in ((WX + 0.01, -0.72), (0.78, WY - 0.01)):
    kule_kare(y, cx, cy, 0.17, Z0, 0.33, 'tugla', cati='piramit', cati_key='sindira', cati_h=0.22, mazgal_h=0.0, konsol=True,
              cati_ns=6, cati_nr=6)

# ---------------------------------------------------------------- birches, people, banner
y.bolum('Huş ağaçları')
for i, (x, yy, b) in enumerate(((0.6, 0.55, 0.34), (0.8, 0.22, 0.3), (0.86, 0.74, 0.36), (-0.75, -0.85, 0.3), (0.3, -0.95, 0.28),
                                (-0.62, 0.62, 0.3), (0.86, -0.95, 0.26), (0.62, -0.2, 0.26))):
    kayin(y, x, yy, Z0, b, tohum=i)

y.bolum('İskele ve tekne')
# a timber landing stage on posts out into the river, a moored boat (lodya) beside it
PYc = -0.08
for k in range(5):
    x = RX - 0.05 + k * 0.045
    for sy in (-1, 1):
        y.prizma((x, PYc + sy * 0.045), 0.006, ZW - 0.01, Z0 + 0.008, 'ahsap_koyu', n=5, ust=False)
kutu_merkez(y, (RX + 0.04, PYc), 0.2, 0.11, 0.008, 'ahsap', z0=Z0 + 0.004)
for k in range(9):
    kutu_merkez(y, (RX - 0.055 + k * 0.023, PYc), 0.017, 0.112, 0.002, 'ahsap_acik', z0=Z0 + 0.012)
with parca(y, (RX + 0.1, PYc - 0.16, ZW), math.pi / 2 + 0.06):
    L, Wd, Hh = 0.3, 0.07, 0.035
    sec = lambda u: Wd / 2 * (1 - abs(u) ** 2.2)
    us = [-1 + 2 * i / 10 for i in range(11)]
    for i in range(10):
        u0, u1 = us[i], us[i + 1]
        for sy in (-1, 1):
            q = [V(u0 * L / 2, sy * sec(u0) * 0.4, -0.006), V(u1 * L / 2, sy * sec(u1) * 0.4, -0.006),
                 V(u1 * L / 2, sy * sec(u1), Hh * (1 + 0.6 * u1 ** 4)), V(u0 * L / 2, sy * sec(u0), Hh * (1 + 0.6 * u0 ** 4))]
            y.yuz_yon(q, 'ahsap', V(0, sy, 0))
            y.yuz_yon([p - V(0, sy * 0.003, 0) for p in q], 'ahsap_koyu', V(0, -sy, 0))   # (the inside)
            y.yuz_yon([q[3], q[2], q[2] - V(0, sy * 0.005, 0), q[3] - V(0, sy * 0.005, 0)], 'ahsap_koyu', Z)
        y.yuz_yon([V(u0 * L / 2, -sec(u0) + 0.005, Hh * 0.45), V(u1 * L / 2, -sec(u1) + 0.005, Hh * 0.45), V(u1 * L / 2, sec(u1) - 0.005, Hh * 0.45),
                   V(u0 * L / 2, sec(u0) - 0.005, Hh * 0.45)], 'ahsap_koyu', Z)
    y.prizma((0.02, 0), 0.004, 0, 0.26, 'ahsap_koyu', n=5)
    cubuk(y, V(0.02, -0.06, 0.24), V(0.02, 0.06, 0.24), 0.005, 'ahsap_koyu')
    levha(y, [V(0.024, -0.055, 0.08), V(0.024, 0.055, 0.08), V(0.024, 0.06, 0.235), V(0.024, -0.06, 0.235)], 'kumas', X)
    for k in range(3):
        kutu_merkez(y, (-0.07 + k * 0.03, 0.0), 0.022, 0.03, 0.022, 'ahsap_acik' if k % 2 else 'kumas', z0=Hh * 0.45)

y.bolum('Araba ve at')
at(y, 0.42, -0.86, Z0, 0.4, 1.3, 'ahsap', 'ahsap_koyu')
with parca(y, (0.27, -0.92, Z0), 0.4):
    kutu_merkez(y, (0, 0), 0.12, 0.07, 0.008, 'ahsap', z0=0.04)
    for sy in (-1, 1):
        kutu_merkez(y, (0, sy * 0.035), 0.12, 0.004, 0.025, 'ahsap_koyu', z0=0.048)
        boru(y, [V(0.04, sy * 0.025, 0.045), V(0.17, sy * 0.022, 0.055)], 0.003, 'ahsap_koyu', n=4)
        for x in (-0.035, 0.035):
            boru(y, [V(x, sy * 0.038, 0.022), V(x, sy * 0.046, 0.022)], 0.022, 'ahsap_koyu', n=10)
    for k in range(3):
        kutu_merkez(y, (-0.03 + k * 0.03, 0), 0.026, 0.05, 0.03, 'ahsap_acik' if k != 1 else 'kumas', z0=0.048)

y.bolum('İnsanlar')
for i, (x, yy, k) in enumerate(((TC.x - 0.03, -0.62, 'koyu'), (TC.x + 0.05, -0.7, 'boya_kirmizi'), (TC.x + 0.02, -0.84, 'kirmizi'),
                                (0.55, -0.7, 'ahsap'), (0.6, -0.72, 'beyaz'))):
    insan(y, x, yy, Z0, k, s=1.6, aci=math.pi / 2)

y.bolum('Sancak')
sancak(y, TC.x + 0.2, YB[0] - 0.24, Z0, boy=0.4, en=0.11, yuk=0.07, aci=-math.pi / 2 - 0.5, direk_key='ahsap_koyu', kuyruk=True)
sancak(y, TC.x - 0.2, YB[0] - 0.24, Z0, boy=0.4, en=0.11, yuk=0.07, aci=-math.pi / 2 + 0.5, direk_key='ahsap_koyu', kuyruk=True)

calistir(y, 'lm_novgorod')
