# Mamluk Barracks (lm_memlukkisla), Cairo: a cut-limestone barracks round a sand training yard. The front shows the
# Mamluk vocabulary: an ablaq (red / white striped) muqarnas portal, tall recessed window panels with muqarnas heads,
# stepped merlons; at the corner the founder's mausoleum with a stepped zone of transition, a windowed drum and a
# pointed stone dome carved with an interlacing lattice (after Qaytbay); beside the portal the slender minaret
# (square, octagonal and round stages, corbelled balconies, a pavilion of columns with a bulb). Inside: two-storey
# arcades with ablaq voussoirs, an iwan, the stables, horsemen at drill, targets, a lance rack, wind-catchers.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from arap_ortak import *

y = Yapi()

Z0 = 0.04
ZR = Z0 + 0.32                     # the ranges' roof
TAS, ACIK, KOYU = 'kum', 'kum_acik', 'kum_koyu'
KIZIL = 'kirmizi_tas'
REN = (TAS, KOYU, ACIK, 'koyu')
ABLAK = ['kirec', KIZIL]
XO0, XO1, YO0, YO1 = -1.0, 1.0, -0.78, 0.82        # the outer walls
CX0, CX1, CY0, CY1 = -0.5, 0.78, -0.52, 0.56       # the court

y.bolum('Zemin')
zemin(y, -1.14, 1.14, -1.0, 0.96, Z0, 'kum_koyu', 'zemin', basamak=(('on', 0.5),), n_basamak=2)


def merlon_hatti(kose, z, kapali=False, kademe=True):
    """a parapet with stepped Mamluk merlons along a polyline (outer face on its right)"""
    mazgalli_kenar(y, kose, z, TAS, kal=0.018, h=0.034, kapali=kapali, ust_key=ACIK, dolu=0.014, w=0.024 if kademe else 0.028, g=0.014 if kademe else 0.02, uc=0.012, kademe=kademe)


def pano(a, b, z0, H, d=0.03, pencere=True):
    """a tall recessed Mamluk window panel in the bay a->b (facing its right): a grilled rectangular window below, a
    pair of pointed windows and an oculus above, the recess capped by a muqarnas hood"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v, dd=0.0: a + e * u - nc * dd + Z * (z0 + v)
    x0, x1 = 0.16 * W, 0.84 * W
    v0, v1 = 0.03, H - 0.03
    vw, vo, vm = H * 0.42, H * 0.7, H * 0.8
    for q in ([L(0, 0), L(x0, 0), L(x0, H), L(0, H)], [L(x1, 0), L(W, 0), L(W, H), L(x1, H)],
              [L(x0, 0), L(x1, 0), L(x1, v0), L(x0, v0)], [L(x0, v1), L(x1, v1), L(x1, H), L(x0, H)]):
        y.yuz_yon(q, TAS, nc)
    y.yuz_yon([L(x0, v0), L(x0, v1), L(x0, v1, d), L(x0, v0, d)], KOYU, e)
    y.yuz_yon([L(x1, v0), L(x1, v1), L(x1, v1, d), L(x1, v0, d)], KOYU, -e)
    y.yuz_yon([L(x0, v0), L(x1, v0), L(x1, v0, d), L(x0, v0, d)], ACIK, Z)
    a2, b2 = L(x0, -z0, d), L(x1, -z0, d)
    m2 = a2.lerp(b2, 0.5)
    if pencere:
        dikdortgen_acik(y, a2, b2, z0 + v0, vw - v0, 0.2, 0.8, 0.02, vw - v0 - 0.02, REN, derin=0.012, cerceve=(0.006, KIZIL))
        kafes(y, a2, b2, z0 + v0, 0.2, 0.8, 0.02, vw - v0 - 0.02, 'demir', 4, 3, 0.0025, 0.004)
        for p, q in ((a2, m2), (m2, b2)):
            y.kemerli(p, q, z0 + vw, vo - vw, REN, v0=0.01, en=0.56, ust=0.008, derin=0.012, k_say=6, sivri=0.6)
        duz_duvar(y, a2, b2, z0 + vo, z0 + vm, TAS)
        y.oculus((a2 + b2) / 2 + Z * (z0 + (vo + vm) / 2), e, nc, 0.011, 'koyu', ACIK, f=0.004, k=10)
    else:
        duz_duvar(y, a2, b2, z0 + v0, z0 + vm, TAS)
    # the lintel band with a joggled ablaq look over the lower window
    kutu(y, a2 + Z * (z0 + vw - 0.006) + nc * 0.004, e, (b2 - a2).length, 0.004, 0.006, KIZIL, 'onust')
    # the hood: three corbelled courses stepping forward to the face, each a row of alternating light / mid blocks
    # (a muqarnas read at the game's scale; the library's cell hood was mush this small and left gaps from above)
    n_k = 3
    hh = (v1 - vm) / n_k
    onceki = d
    for i in range(n_k):
        dd = d * (1 - (i + 1) / n_k)
        za = vm + i * hh
        m = 3 + i
        for j in range(m):
            ua, ub = x0 + (x1 - x0) * j / m, x0 + (x1 - x0) * (j + 1) / m
            y.yuz_yon([L(ua, za, dd), L(ub, za, dd), L(ub, za + hh, dd), L(ua, za + hh, dd)], (ACIK, TAS)[(j + i) % 2], nc)
        y.yuz_yon([L(x0, za, onceki), L(x1, za, onceki), L(x1, za, dd), L(x0, za, dd)], KOYU, -Z)
        onceki = dd


# ---------------- the front: mausoleum, portal, minaret, panels ----------------
y.bolum('Ön cephe: ablak taçkapı ve pencere panoları')
PX = -0.3
PEN = 0.28
ptop = tackapi_mukarnas(y, PX, YO0 - 0.02, Z0, en=PEN, H=0.54, derin=0.13, nis=0.56, sivri=0.6, kapi_key='ahsap', key='kirec',
                        bordur=(KIZIL, 'kirec'), mk_kat=6, cerceve=(0.016, ABLAK), tonlar=('kirec', KIZIL))
# its striped flanks and back above the roof
for sx in (-1, 1):
    x = PX + sx * PEN / 2
    a, b = (V(x, YO0 - 0.02 + 0.13), V(x, YO0 - 0.02)) if sx < 0 else (V(x, YO0 - 0.02), V(x, YO0 - 0.02 + 0.13))
    for k in range(11, 18):
        duz_duvar(y, a + V(sx * 0.0025, 0), b + V(sx * 0.0025, 0), Z0 + k * 0.03, Z0 + (k + 1) * 0.03, ABLAK[k % 2])
ablak(y, V(PX + PEN / 2, YO0 - 0.02 + 0.13), V(PX - PEN / 2, YO0 - 0.02 + 0.13), ZR, Z0 + 0.54, ABLAK, 0.03)
# the portal's crown: a cresting of stepped (fleur-like) merlons round its top
mazgalli_kenar(y, dikdortgen(PX - PEN / 2 + 0.004, PX + PEN / 2 - 0.004, YO0 - 0.016, YO0 + 0.106), ptop, 'kirec', kal=0.014, h=0.034,
               ust_key='kirec', dolu=0.008, w=0.022, g=0.012, uc=0.012, kademe=True)
# the walls either side of the portal: ablaq courses
ablak(y, V(-0.5, YO0), V(PX - PEN / 2, YO0), Z0, ZR, ABLAK, 0.032)
ablak(y, V(PX + PEN / 2, YO0), V(-0.14, YO0), Z0, ZR, ABLAK, 0.032)
# a stone bench (mastaba) each side of the portal's foot
for sx in (-1, 1):
    kutu_merkez(y, (PX + sx * 0.1, YO0 - 0.045), 0.05, 0.03, 0.025, ACIK, z0=Z0)
# the panels along the front
PAN = [-0.02 + (0.92 + 0.02) * k / 6 for k in range(7)]
for k in range(6):
    pano(V(PAN[k], YO0), V(PAN[k + 1], YO0), Z0, 0.3)
duz_duvar(y, V(PAN[0], YO0), V(PAN[-1], YO0), Z0 + 0.3, ZR, TAS)
duz_duvar(y, V(0.92, YO0), V(XO1, YO0), Z0, ZR, TAS)
silme(y, [V(-0.5, YO0), V(XO1, YO0)], ZR - 0.03, 0.014, 0.008, ACIK, 'tac', kapali=False)
silme(y, [V(-0.5, YO0), V(XO1, YO0)], Z0, 0.025, 0.008, KOYU, 'kaide', kapali=False)

y.bolum('Türbe: geçiş kuşağı, kasnak, oymalı taş kubbe')
MX, MY, MH = -0.75, -0.55, 0.25        # mausoleum centre and half size
ZM = Z0 + 0.42
mk = dikdortgen(MX - MH, MX + MH, MY - MH, MY + MH)
for i in range(4):
    a, b = mk[i], mk[(i + 1) % 4]
    n = 2 if i in (0, 3) else 0
    for j in range(n):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        pano(p, q, Z0 + 0.02, 0.36)
    if i == 1:   # (the east side: only its end on the court shows; the rest is inside the front range)
        m = V(a.x, CY0)
        duvar_bant(y, a, m, Z0 + 0.02, Z0 + 0.38, TAS, n=2)
        pano(m, b, Z0 + 0.02, 0.36)
    elif i == 2:
        duvar_bant(y, a, b, Z0 + 0.02, Z0 + 0.38, TAS, n=2)
    ablak(y, a, b, Z0, Z0 + 0.02, ABLAK, 0.02)
    ablak(y, a, b, Z0 + 0.38, ZM, [TAS, ACIK], 0.02)
    # an inscription band under the cornice
    cini_bant(y, a, b, ZM - 0.03, 0.014, (KOYU, ACIK), n=12)
silme(y, mk, ZM - 0.012, 0.012, 0.008, ACIK, 'tac')
silme(y, mk, Z0, 0.025, 0.008, KOYU, 'kaide')
merlon_hatti(mk, ZM, kapali=True)
y.yuz_yon([V(p.x, p.y, ZM) for p in disa(mk, -0.018)], 'zemin', Z)
# zone of transition: an octagon with stepped triangular corners
RO = 0.21
oc = cokgen((MX, MY), RO / math.cos(math.pi / 8), 8, math.pi / 8)
ZT1 = ZM + 0.08
for i in range(8):
    duvar_bant(y, oc[i], oc[(i + 1) % 8], ZM, ZT1, TAS, n=1)
y.yuz_yon([V(p.x, p.y, ZT1) for p in oc], ACIK, Z)
for sx in (-1, 1):
    for sy in (-1, 1):
        for k in range(3):
            s = 0.1 - k * 0.028
            cc = V(MX + sx * (RO * 0.82 - k * 0.012), MY + sy * (RO * 0.82 - k * 0.012))
            kutu_merkez(y, (cc.x, cc.y), s, s, 0.026, TAS if k % 2 == 0 else ACIK, z0=ZM + k * 0.026, aci=math.pi / 4)
halka_kornis(y, (MX, MY), RO / math.cos(math.pi / 8), ZT1 - 0.012, 0.012, 0.008, 8, ACIK, kat=math.pi / 8)
# the drum: sixteen pointed windows
RD = 0.19
dk = cokgen((MX, MY), RD, 16)
ZD = ZT1 + 0.09
for i in range(16):
    y.kemerli(dk[i], dk[(i + 1) % 16], ZT1, ZD - ZT1, ('kirec', KOYU, ACIK, 'koyu'), v0=0.012, en=0.5, ust=0.012, derin=0.012, k_say=6, sivri=0.6,
              cerceve=(0.004, ABLAK) if i % 2 == 0 else None)
halka_kornis(y, (MX, MY), RD, ZD - 0.006, 0.012, 0.01, 16, ACIK)
# the pointed dome: a slightly stilted ogive, the carved lattice raised on it
R, HD = RD + 0.004, 0.29
rho = (R * R + HD * HD) / (2 * R)
cc_ = R - rho
tmax = math.acos(-cc_ / rho)
z_b = ZD + 0.006 + 0.018
pr = [(R, ZD + 0.006), (R, z_b)] + [(cc_ + rho * math.cos(tmax * k / 12), z_b + rho * math.sin(tmax * k / 12)) for k in range(1, 12)] + [(0.0, z_b + HD)]
donel(y, (MX, MY), pr, TAS, n=32)


def kubbe_nokta(phi, t, ek=0.0):
    th = tmax * t
    rr = cc_ + rho * math.cos(th)
    nr = V(math.cos(th) * math.cos(phi), math.cos(th) * math.sin(phi), math.sin(th))
    return V(MX + rr * math.cos(phi), MY + rr * math.sin(phi), z_b + rho * math.sin(th)) + nr * ek


NL = 12
for yon in (-1, 1):
    for j in range(NL):
        phi0 = TAU * j / NL
        pts = [kubbe_nokta(phi0 + yon * (TAU / NL) * 1.6 * (t / 10), 0.02 + 0.84 * t / 10, 0.003) for t in range(11)]
        boru(y, pts, 0.003, ACIK, n=3)
# a carved band at the dome's foot and the finial
halka_kornis(y, (MX, MY), R, z_b - 0.006, 0.014, 0.004, 32, ACIK)
alem(y, MX, MY, z_b + HD - 0.004, 1.0)

y.bolum('Minare: kare, sekizgen, yuvarlak gövde, köşk ve soğan tepelik')
NX_, NY_ = -0.08, YO0 + 0.065
W1 = 0.145
sq = dikdortgen(NX_ - W1 / 2, NX_ + W1 / 2, NY_ - W1 / 2, NY_ + W1 / 2)
Z1 = Z0 + 0.6
for i in range(4):
    a, b = sq[i], sq[(i + 1) % 4]
    duvar_bant(y, a, b, Z0, ZR, TAS, n=3)
    L_, x0, x1, hs, ap = kemer_nis(y, a, b, ZR, Z1 - ZR - 0.06, en=0.5, ust=0.015, sivri=0.6, derin=0.012, key=TAS, yan_key=KOYU, alt_key=ACIK,
                                    arka_key='koyu', v0=0.02, k_say=8, cerceve=(0.005, ABLAK))
    ablak(y, a, b, Z1 - 0.06, Z1, ABLAK, 0.015)
konsol_halka(y, sq, Z1 - 0.035, 0.035, 0.02, ACIK, 3)
sq2 = disa(sq, 0.02)
y.yuz_yon([V(p.x, p.y, Z1) for p in sq2], ACIK, Z)
parapet(y, sq2, Z1, 0.024, 0, 0.007, ACIK, ust_key=ACIK)
# octagonal stage: keel-arched niches, alternate ones open
R2 = 0.063
o8 = cokgen((NX_, NY_), R2, 8, math.pi / 8)
Z2 = Z1 + 0.3
for i in range(8):
    kemer_nis(y, o8[i], o8[(i + 1) % 8], Z1, Z2 - Z1, en=0.62, ust=0.03, sivri=0.65, derin=0.01, key=TAS, yan_key=KOYU, alt_key=ACIK,
              arka_key='koyu' if i % 2 == 0 else KOYU, v0=0.03, k_say=8, cerceve=(0.004, ABLAK))
for p in o8:
    y.prizma((p.x, p.y), 0.004, Z1, Z2 - 0.03, ACIK, n=6)
konsol_halka(y, o8, Z2 - 0.035, 0.035, 0.028, ACIK, 4)
o8b = disa(o8, 0.028)
y.yuz_yon([V(p.x, p.y, Z2) for p in o8b], ACIK, Z)
parapet(y, o8b, Z2, 0.022, 0, 0.006, ACIK, ust_key=ACIK)
# round stage with small windows
R3 = 0.042
Z3 = Z2 + 0.16
y.prizma((NX_, NY_), R3, Z2, Z3, TAS, n=16, ust=False)
for k in range(4):
    a = TAU * k / 4 + math.pi / 4
    nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
    y.pencere(V(NX_, NY_) + nn * (R3 + 0.0005) + Z * Z2, e, nn, -0.006, 0.05, 0.012, 0.035, 'koyu')
for k in range(3):
    halka_kornis(y, (NX_, NY_), R3, Z2 + 0.02 + k * 0.045, 0.006, 0.004, 16, ABLAK[k % 2])
r3c = cokgen((NX_, NY_), R3, 16)
konsol_halka(y, r3c, Z3 - 0.03, 0.03, 0.022, ACIK, 3)
r3b = disa(r3c, 0.022)
y.yuz_yon([V(p.x, p.y, Z3) for p in r3b], ACIK, Z)
parapet(y, r3b, Z3, 0.02, 0, 0.005, ACIK, ust_key=ACIK)
# the pavilion of columns and the bulb
Z4 = Z3 + 0.085
for k in range(8):
    a = TAU * k / 8
    y.prizma((NX_ + 0.03 * math.cos(a), NY_ + 0.03 * math.sin(a)), 0.0045, Z3, Z4, ACIK, n=6, ust=False)
y.prizma((NX_, NY_), 0.016, Z3, Z4, 'koyu', n=8, ust=False)
y.prizma((NX_, NY_), 0.04, Z4, Z4 + 0.012, ACIK, n=16)
halka_kornis(y, (NX_, NY_), 0.04, Z4, 0.004, 0.005, 16, ACIK)
tb = sogan_kubbe(y, (NX_, NY_), 0.032, Z4 + 0.012, 0.075, TAS, n=20, boyun=0.5, sivri=0.4)
alem(y, NX_, NY_, tb - 0.004, 0.75)

# ---------------- the outer walls of the ranges ----------------
y.bolum('Dış duvarlar, köşe burçları, mazgallar')
for (a, b, n) in ((V(XO1, YO0), V(XO1, YO1), 9), (V(XO1, YO1), V(XO0, YO1), 11), (V(XO0, YO1), V(XO0, MY + MH), 6)):
    kat_pencere(y, a, b, Z0, ZR, Z0 + 0.18, Z0 + 0.26, n, REN, en=0.28, sivri=0.6, derin=0.012)
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(n):       # slits in the lower storey
        p = a.lerp(b, (k + 0.5) / n)
        yarik(y, p + nn * 0.001, e, nn, -0.005, Z0 + 0.06, 0.01, 0.06, 'koyu')
    silme(y, [a, b], ZR - 0.03, 0.014, 0.008, ACIK, 'tac', kapali=False)
    silme(y, [a, b], Z0 + 0.16, 0.008, 0.006, ACIK, 'duz', kapali=False)
    silme(y, [a, b], Z0, 0.025, 0.008, KOYU, 'kaide', kapali=False)
merlon_hatti([V(-0.5, YO0), V(XO1, YO0)], ZR)
merlon_hatti([V(XO1, YO0), V(XO1, YO1), V(XO0, YO1), V(XO0, MY + MH)], ZR, kademe=False)
for (cx, cy, r, h) in ((XO1, YO0, 0.11, 0.42), (XO1, YO1, 0.1, 0.4), (XO0, YO1, 0.1, 0.4)):
    zt = kule_yuvarlak(y, (cx, cy), r, Z0, h, TAS, cati=None, mazgal_h=0, n=16, egim=0.05, yarik_say=3, konsol=True, bolum=3)
    ring = cokgen((cx, cy), r + 0.016, 16)
    for i in range(0, 16, 2):
        sivri_mazgal(y, ring[i], ring[i + 1], Z0 + h + 0.012, 0.032, 0.016, TAS, g=0.002, kademe=False)
    for zz in (Z0 + h * 0.33, Z0 + h * 0.66):
        halka_kornis(y, (cx, cy), r * (1 + 0.05 * (1 - (zz - Z0) / h)), zz, 0.012, 0.004, 16, KIZIL)

# ---------------- the court ----------------
y.bolum('Avlu: iki katlı revaklar, eyvan')
ck = dikdortgen(CX0, CX1, CY0, CY1)
y.yuz_yon([V(p.x, p.y, Z0 + 0.002) for p in ck], 'zemin', Z)
y.yuz_yon([V(p.x, p.y, Z0 + 0.003) for p in dikdortgen(CX0 + 0.08, CX1 - 0.08, CY0 + 0.08, CY1 - 0.08)], 'toprak', Z)
H1, H2 = 0.16, 0.16
# side 0 south (front range), 1 east, 2 north (stables: own), 3 west (iwan: own)
avlu_revak(y, (CX0, CX1, CY0, CY1), Z0, H1, [8, 7, 0, 0], REN, en=0.72, ust=0.025, derin=0.07, sivri=0.62, sutunlu=False,
           cerceve=(0.009, ABLAK), atla=(2, 3))
avlu_revak(y, (CX0, CX1, CY0, CY1), Z0 + H1, H2, [8, 7, 0, 0], REN, en=0.6, ust=0.02, derin=0.05, sivri=0.62, sutunlu=False,
           atla=(2, 3), korkuluk=0.03)
for i in (0, 1):
    a, b = ck[(i + 1) % 4], ck[i]
    silme(y, [a, b], Z0 + H1 - 0.008, 0.01, 0.008, ACIK, 'duz', kapali=False)
# west: the iwan (a tall pointed vault open to the court) between two-storey bays
a, b = ck[0], ck[3]          # (x = CX0, from south to north: facing +x, the court)
n = 5
for j in range(n):
    p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
    if j == 2:
        RA, ND = 0.012, 0.16
        L_, x0, x1, hs, ap = kemer_nis(y, p, q, Z0, ZR - Z0, en=0.86, ust=0.03, sivri=0.62, derin=RA, key=TAS, yan_key=KOYU,
                                       alt_key=ACIK, arka_key=None, k_say=12, cerceve=(0.012, ABLAK))
        # the iwan: its sides, floor, back wall (a door and a grilled window) and a muqarnas hood in the vault's head
        zs = hs * 0.8
        for u in (x0, x1):
            s = 1 if u == x0 else -1
            y.yuz_yon([L_(u, 0, RA), L_(u, 0, ND), L_(u, ap + 0.002, ND), L_(u, ap + 0.002, RA)], KOYU, (q - p).normalized() * s)
        y.yuz_yon([L_(x0, 0.002, 0), L_(x1, 0.002, 0), L_(x1, 0.002, ND), L_(x0, 0.002, ND)], 'mermer', Z)
        a2, b2 = L_(x0, -Z0, ND), L_(x1, -Z0, ND)
        dikdortgen_acik(y, a2, b2, Z0, zs * 0.62, 0.3, 0.7, 0.0, zs * 0.45, (TAS, KOYU, ACIK, 'ahsap'), derin=0.01, cerceve=(0.006, KIZIL))
        dikdortgen_acik(y, a2, b2, Z0 + zs * 0.62, zs * 0.38, 0.3, 0.7, 0.02, zs * 0.38 - 0.02, (TAS, KOYU, ACIK, 'koyu'), derin=0.01, cerceve=(0.005, ACIK))
        kafes(y, a2, b2, Z0 + zs * 0.62, 0.3, 0.7, 0.02, zs * 0.38 - 0.02, 'demir', 4, 3, 0.0025, 0.004)
        mukarnas(y, L_(x0, 0, RA), L_(x1, 0, RA), Z0 + zs, ap + 0.002 - zs, ND - RA, kat=5, keys=(ACIK, TAS, KOYU))
    else:
        y.kemerli(p, q, Z0, H1, REN, v0=0.0, en=0.5, ust=0.03, derin=0.03, k_say=8, sivri=0.62, cerceve=(0.007, ABLAK))
        y.kemerli(p, q, Z0 + H1, H2, REN, v0=0.03, en=0.42, ust=0.025, derin=0.02, k_say=8, sivri=0.62)
cp = [ck[3], ck[2], ck[1], ck[0]]          # (clockwise: the parapet faces the court)
parapet(y, cp, ZR, 0.02, 0, 0.012, TAS, ust_key=ACIK)
silme(y, [cp[2], cp[3]], ZR - 0.016, 0.016, 0.01, ACIK, 'tac', kapali=False)
silme(y, [cp[1], cp[2]], ZR - 0.016, 0.016, 0.01, ACIK, 'tac', kapali=False)

y.bolum('Ahırlar')
a, b = ck[3], ck[2]          # (the north side, run +x: it faces the court)
n = 8
for j in range(n):
    p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
    y.kemerli(p, q, Z0, H1, (TAS, KOYU, ACIK, 'koyu'), v0=0.0, en=0.66, ust=0.03, derin=0.05, k_say=8, sivri=0.6, cerceve=(0.008, ABLAK) if j % 2 == 0 else None)
    y.kemerli(p, q, Z0 + H1, H2, REN, v0=0.04, en=0.36, ust=0.03, derin=0.015, k_say=6, sivri=0.6)
    # a horse's head looking out of the stall
    m = (p + q) / 2
    hx = m + V(0, -0.02)
    boru(y, [V(hx.x, CY1 + 0.03, Z0 + 0.08), V(hx.x, CY1 - 0.004, Z0 + 0.09), V(hx.x, CY1 - 0.022, Z0 + 0.075)], 0.008,
         'ahsap' if j % 3 else 'ahsap_koyu', n=6, r_son=0.0055)
    for s in (-1, 1):
        cubuk(y, V(hx.x + s * 0.004, CY1 - 0.0, Z0 + 0.097), V(hx.x + s * 0.005, CY1 + 0.002, Z0 + 0.106), 0.0025, 'ahsap_koyu')
silme(y, [a, b], Z0 + H1 - 0.008, 0.01, 0.008, ACIK, 'duz', kapali=False)
# a timber awning on posts in front of the stalls, the troughs under it
AW = 0.08
for k in range(9):
    x = CX0 + 0.04 + (CX1 - CX0 - 0.08) * k / 8
    cubuk(y, V(x, CY1 - AW, Z0), V(x, CY1 - AW, Z0 + 0.12), 0.007, 'ahsap_koyu')
cubuk(y, V(CX0 + 0.03, CY1 - AW, Z0 + 0.12), V(CX1 - 0.03, CY1 - AW, Z0 + 0.12), 0.008, 'ahsap', 0.01)
fa, fb = V(CX0 + 0.02, CY1 - AW - 0.015, Z0 + 0.124), V(CX1 - 0.02, CY1 - AW - 0.015, Z0 + 0.124)
ba, bb = V(CX0 + 0.02, CY1, Z0 + 0.15), V(CX1 - 0.02, CY1, Z0 + 0.15)
dz = Z * 0.006
y.yuz_yon([fa, fb, bb, ba], 'ahsap_dikey', V(0, -0.5, 1))
y.yuz_yon([fa - dz, fb - dz, bb - dz, ba - dz], 'ahsap_koyu', -Z)
y.yuz_yon([fa, fb, fb - dz, fa - dz], 'ahsap_koyu', -Y)
y.yuz_yon([fa, ba, ba - dz, fa - dz], 'ahsap_koyu', -X)
y.yuz_yon([fb, bb, bb - dz, fb - dz], 'ahsap_koyu', X)
for x0_, x1_ in ((CX0 + 0.04, CX0 + 0.5), (CX0 + 0.62, CX1 - 0.04)):
    kutu(y, V(x0_, CY1 - 0.06, Z0), X, x1_ - x0_, 0.035, 0.03, KOYU, 'onarkasagsolust')
    y.yuz_yon([V(x0_ + 0.006, CY1 - 0.054, Z0 + 0.0305), V(x1_ - 0.006, CY1 - 0.054, Z0 + 0.0305), V(x1_ - 0.006, CY1 - 0.031, Z0 + 0.0305), V(x0_ + 0.006, CY1 - 0.031, Z0 + 0.0305)], 'su', Z)

# ---------------- roofs ----------------
y.bolum('Damlar ve rüzgâr bacaları')
for (x0, x1, y0, y1) in ((CX0, XO1, YO0, CY0), (CX1, XO1, CY0, YO1), (CX0, CX1, CY1, YO1), (XO0, CX0, MY + MH, YO1)):
    y.yuz_yon([V(x0, y0, ZR), V(x1, y0, ZR), V(x1, y1, ZR), V(x0, y1, ZR)], 'zemin', Z)
    # raised stone copings dividing the terrace into drainage bays, across the range every ~0.17
    uzun_x = (x1 - x0) > (y1 - y0)
    n_ = max(1, int(round(max(x1 - x0, y1 - y0) / 0.17)))
    for k in range(1, n_):
        t = k / n_
        if uzun_x:
            xx = x0 + (x1 - x0) * t
            kutu(y, V(xx + 0.004, y0 + 0.012, ZR), Y, y1 - y0 - 0.024, 0.008, 0.005, ACIK, 'onarkasagsolust')
        else:
            yy = y0 + (y1 - y0) * t
            kutu(y, V(x0 + 0.012, yy - 0.004, ZR), X, x1 - x0 - 0.024, 0.008, 0.005, ACIK, 'onarkasagsolust')
for (cx, cy) in ((0.3, -0.66), (0.62, -0.66), (0.89, 0.1), (0.89, 0.45), (0.1, 0.7), (-0.3, 0.7), (-0.75, 0.2), (-0.75, 0.55)):
    malqaf(y, cx, cy, ZR, 0.0, key=ACIK)
# stone water spouts (mizab) under the parapets of the outer walls
for (a, b, n) in ((V(XO1, YO0), V(XO1, YO1), 8), (V(XO1, YO1), V(XO0, YO1), 9), (V(XO0, YO1), V(XO0, MY + MH), 4)):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(n):
        p = a.lerp(b, (k + 1) / (n + 1)) + nn * 0.03
        kutu(y, p - e * 0.005 + Z * (ZR - 0.014), e, 0.01, 0.03, 0.009, KOYU, 'onsagsolust')
# shallow plastered domes over the rooms (each with a small light-hole drum)
for (cx, cy) in ((-0.38, -0.65), (0.15, -0.66), (0.46, -0.66), (0.76, -0.66), (0.89, -0.05), (0.89, 0.27), (0.89, 0.62),
                 (0.62, 0.7), (0.32, 0.7), (-0.1, 0.7), (-0.75, 0.0), (-0.75, 0.38), (-0.75, 0.7)):
    y.prizma((cx, cy), 0.05, ZR, ZR + 0.014, ACIK, n=16, ust=False)
    y.kubbe((cx, cy), 0.05, ZR + 0.014, 0.03, ACIK, n=16, kat=4)
# a rooftop kiosk (a small domed pavilion over the east range)
kutu_merkez(y, (0.89, -0.3), 0.12, 0.12, 0.09, TAS, z0=ZR)
for i, (a, b) in enumerate(zip(dikdortgen(0.83, 0.95, -0.36, -0.24), dikdortgen(0.83, 0.95, -0.36, -0.24)[1:] + dikdortgen(0.83, 0.95, -0.36, -0.24)[:1])):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    y.pencere((a + b) / 2 + nn * 0.0005 + Z * ZR, e, nn, -0.012, 0.025, 0.024, 0.05, 'koyu')
silme(y, dikdortgen(0.83, 0.95, -0.36, -0.24), ZR + 0.085, 0.01, 0.008, ACIK, 'tac')
kucuk_kubbe(y, 0.89, -0.3, ZR + 0.095, 0.055, kasnak=0.02, n=20, son=False, key=TAS, kasnak_key=TAS)
alem(y, 0.89, -0.3, ZR + 0.095 + 0.02 + 0.05, 0.6)

# ---------------- the training yard ----------------
y.bolum('Talim avlusu: atlılar, hedefler, mızrak sehpası')


def at(x, yy, aci, renk='ahsap', cul='boya_kirmizi', binici='boya_sari', mizrak=True, olcek=1.25):
    """a stylised horse (head towards +x) with a Mamluk rider in a turban, a lance raised"""
    with parca(y, (x, yy, Z0 + 0.003), aci, olcek):
        h = 0.062
        boru(y, [V(-0.034, 0, h), V(-0.005, 0, h + 0.004), V(0.032, 0, h + 0.002)], 0.016, renk, n=6)
        kure(y, (-0.034, 0, h), 0.016, renk, n=8, kat=4)
        kure(y, (0.032, 0, h + 0.002), 0.016, renk, n=8, kat=4)
        boru(y, [V(0.036, 0, h + 0.008), V(0.05, 0, h + 0.03), V(0.058, 0, h + 0.046)], 0.01, renk, n=6, r_son=0.008)
        boru(y, [V(0.056, 0, h + 0.05), V(0.078, 0, h + 0.034)], 0.0075, renk, n=6, r_son=0.005)
        for s in (-1, 1):
            cubuk(y, V(0.054, s * 0.004, h + 0.054), V(0.052, s * 0.004, h + 0.064), 0.0025, renk)
        boru(y, [V(0.03, 0, h + 0.03), V(0.046, 0, h + 0.05), V(0.054, 0, h + 0.056)], 0.003, 'ahsap_koyu', n=4)   # mane
        boru(y, [V(-0.05, 0, h + 0.006), V(-0.06, 0, h - 0.015), V(-0.058, 0, h - 0.04)], 0.0045, 'ahsap_koyu', n=4, r_son=0.002)
        for lx, ileri in ((-0.03, -0.008), (0.028, 0.01)):
            for s in (-1, 1):
                boru(y, [V(lx, s * 0.008, h - 0.004), V(lx + ileri * 0.5, s * 0.008, h * 0.5), V(lx + ileri, s * 0.008, 0.004)], 0.0045, renk, n=5, r_son=0.0035)
                kutu_merkez(y, (lx + ileri, s * 0.008), 0.008, 0.007, 0.005, 'ahsap_koyu')
        kutu_merkez(y, (0.0, 0), 0.038, 0.036, 0.004, cul, z0=h + 0.012)
        if binici:
            donel(y, (0.002, 0), [(0.0, h + 0.016), (0.012, h + 0.016), (0.011, h + 0.04), (0.008, h + 0.056), (0.0, h + 0.058)], binici, n=8)
            for s in (-1, 1):
                boru(y, [V(0.004, s * 0.009, h + 0.02), V(0.012, s * 0.016, h + 0.005)], 0.0035, binici, n=4)
            kure(y, (0.002, 0, h + 0.064), 0.0065, 'ahsap_acik', n=8, kat=4)
            donel(y, (0.002, 0), [(0.007, h + 0.066), (0.009, h + 0.071), (0.005, h + 0.077), (0.0, h + 0.078)], 'beyaz', n=8)
            if mizrak:
                cubuk(y, V(-0.02, 0.012, h + 0.0), V(0.06, 0.012, h + 0.11), 0.0025, 'ahsap_koyu')
                boru(y, [V(0.06, 0.012, h + 0.11), V(0.066, 0.012, h + 0.119)], 0.003, 'demir', n=4, r_son=0.0005)


for (x, yy, a, r, c, b) in ((-0.2, -0.12, 0.3, 'ahsap', 'boya_kirmizi', 'boya_sari'), (0.06, 0.05, 0.3, 'ahsap_koyu', 'turkuaz', 'boya_kirmizi'),
                            (0.3, 0.22, 0.25, 'beyaz', 'boya_kirmizi', 'kumas'), (0.35, -0.3, math.pi - 0.2, 'ahsap_acik', 'lacivert', 'boya_sari')):
    at(x, yy, a, r, c, b)


def hedef(x, yy, aci):
    """an archery target: a round straw boss on two legs"""
    with parca(y, (x, yy, Z0 + 0.003), aci):
        o = V(0, 0, 0.065)
        for k, (rr, key) in enumerate(((0.04, 'saz'), (0.03, 'boya_kirmizi'), (0.019, 'beyaz'), (0.009, 'boya_kirmizi'))):
            d = 0.004 + k * 0.0008
            pts = [o + V(0, -d, 0) + V(rr * math.cos(TAU * i / 10), 0, rr * math.sin(TAU * i / 10)) for i in range(10)]
            y.yuz_yon(pts, key, -Y)
            if k == 0:
                y.yuz_yon([p + V(0, 2 * d, 0) for p in pts], 'saz', Y)
                for i in range(10):
                    p, q = pts[i], pts[(i + 1) % 10]
                    y.yuz_yon([p, q, q + V(0, 2 * d, 0), p + V(0, 2 * d, 0)], 'saz_koyu', (p + q) / 2 - o)
        for s in (-1, 1):
            cubuk(y, V(s * 0.03, 0.012, 0.0), V(s * 0.012, 0.004, 0.065), 0.005, 'ahsap_koyu')


for k in range(3):
    hedef(0.6, -0.25 + k * 0.17, math.pi / 2)
# the lance rack
RX, RY = -0.38, 0.38
for s in (0, 1):
    cubuk(y, V(RX + s * 0.14, RY, Z0), V(RX + s * 0.14, RY, Z0 + 0.06), 0.008, 'ahsap_koyu')
cubuk(y, V(RX - 0.01, RY, Z0 + 0.055), V(RX + 0.15, RY, Z0 + 0.055), 0.007, 'ahsap', 0.008)
for k in range(7):
    x = RX + 0.012 + k * 0.019
    cubuk(y, V(x, RY - 0.02, Z0), V(x, RY + 0.006, Z0 + 0.15), 0.0035, 'ahsap_koyu')
    boru(y, [V(x, RY + 0.006, Z0 + 0.15), V(x, RY + 0.008, Z0 + 0.165)], 0.003, 'demir', n=4, r_son=0.0004)
# the fountain (an octagonal basin) and palms
y.prizma((0.1, -0.3), 0.07, Z0, Z0 + 0.03, ACIK, n=8, kat=math.pi / 8)
y.prizma((0.1, -0.3), 0.06, Z0 + 0.03, Z0 + 0.0305, 'su', n=8, kat=math.pi / 8)
donel(y, (0.1, -0.3), [(0.012, Z0 + 0.03), (0.01, Z0 + 0.06), (0.03, Z0 + 0.07), (0.03, Z0 + 0.075), (0.0, Z0 + 0.076)], ACIK, n=12)
for (x, yy) in ((-0.42, -0.44), (0.7, -0.44), (-0.42, 0.25), (0.7, 0.4)):
    agac(y, x, yy, Z0, boy=0.22, tur='palmiye', key='boya_yesil')
# a mounting block and saddles
kutu_merkez(y, (-0.3, -0.4), 0.06, 0.04, 0.03, ACIK, z0=Z0)

# outside: the banner over the portal, a few figures and a tethered horse before the front
sancak(y, PX + 0.08, YO0 + 0.03, ptop, boy=0.18, en=0.11, yuk=0.07, aci=-0.2)
at(0.35, YO0 - 0.13, 0.05, 'ahsap', 'turkuaz', 'boya_kirmizi', mizrak=False)
for (x, yy, a, g) in ((-0.15, YO0 - 0.1, 0.4, 'boya_kirmizi'), (0.1, YO0 - 0.12, -0.3, 'kumas'), (-0.48, YO0 - 0.1, 0.2, 'boya_sari')):
    adam(y, x, yy, Z0, a, govde=g, boy=0.065)
for (x, yy) in ((-1.06, -0.9), (1.06, -0.9), (-1.06, 0.9), (1.06, 0.9)):
    agac(y, x, yy, Z0, boy=0.2, tur='palmiye', key='boya_yesil')

calistir(y, 'lm_memlukkisla')
