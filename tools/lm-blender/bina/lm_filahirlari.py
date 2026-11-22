# Fil Ahırları (lm_filahirlari): the stables built into Carthage's great wall. A U of massive two-storeyed walls round
# an exercise yard: elephant stalls in deep arches below (elephants looking out), horse stables in smaller arches above
# reached by ramps and a corbelled gallery, square towers with cavetto cornices and merlons, the great central tower with
# the elephant gate; outside, the moat and the palisade of the triple wall. In the yard war elephants with crenellated
# towers, mahouts and keepers, a long water trough, fodder stacks, a fodder cart and tethering posts.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir
from kartaca_ortak import *
from hint_ortak import fil
from frank_ortak import at
from hint_ek import araba

y = Yapi()
D = math.radians
Z0 = 0.03
X0, X1, Y0, Y1 = -1.15, 1.15, -1.15, 1.15
KUM, KUMK, KUMA = 'kum', 'kum_koyu', 'kum_acik'
DUV = (KUM, KUMK, KUMA, 'koyu')
HL, HU = 0.22, 0.16                     # the stalls' storey, the horses' storey
ZG = Z0 + HL                            # the gallery / upper floor
ZT = ZG + HU                            # the wall top
BW = (-1.0, 1.0, 0.45, 0.85)            # the back wing
WX = 0.65                               # the side wings' inner faces |x| = WX, outer |x| = 1.0
WY0 = -0.85                             # the wings' front
GD = 0.045                              # the gallery's depth
gr = random.Random(5)

# ================================================================ ground, moat, palisade
y.bolum('Zemin, hendek, palisad')
MY0, MY1 = 0.9, 1.03                    # the moat
kutu(y, V(X0, Y0, 0), X, X1 - X0, Y1 - Y0, Z0, 'kaya', 'onarkasagsol')
y.yuz_yon(dikdortgen(X0, X1, Y0, MY0, Z0), 'toprak', Z)
y.yuz_yon(dikdortgen(X0, X1, MY1, Y1, Z0), 'toprak_ot', Z)
y.yuz_yon(dikdortgen(X0, X1, MY0, MY1, Z0 - 0.018), 'su', Z)
duz_duvar(y, V(X1, MY0), V(X0, MY0), Z0 - 0.02, Z0, KUMK)
duz_duvar(y, V(X0, MY1), V(X1, MY1), Z0 - 0.02, Z0, 'kaya_koyu')
# the moat's ends (seen from inside the channel)
duz_duvar(y, V(X0 + 0.002, MY0), V(X0 + 0.002, MY1), Z0 - 0.02, Z0, 'kaya_koyu')
duz_duvar(y, V(X1 - 0.002, MY1), V(X1 - 0.002, MY0), Z0 - 0.02, Z0, 'kaya_koyu')
# the yard: sand, a paved way from the front to the elephant gate
y.yuz_yon(dikdortgen(-WX, WX, WY0, BW[2], Z0 + 0.002), 'kum_acik', Z)
y.yuz_yon(dikdortgen(-0.09, 0.09, Y0, BW[2] - 0.07, Z0 + 0.004), 'zemin', Z)
# the palisade on the far bank (the outermost line of the triple wall)
for k in range(76):
    x = X0 + 0.02 + (X1 - X0 - 0.04) * k / 75
    h = 0.07 + 0.01 * ((k * 7) % 3)
    y.prizma((x, 1.09), 0.012, Z0 - 0.004, Z0 + h, 'kutuk', n=5, ust=False)
    y.koni((x, 1.09), 0.012, Z0 + h, 0.024, 'ahsap', n=5)
for zz in (0.025, 0.055):
    cubuk(y, V(X0 + 0.01, 1.075, Z0 + zz), V(X1 - 0.01, 1.075, Z0 + zz), 0.008, 'ahsap_koyu', 0.006)


# ================================================================ the walls
def duvar_kemerli(a, b, n, alt=True, ust_=True, ust_n=None, bos=()):
    """one inner face a->b (facing the yard on its right): a row of deep stall arches below (bos: bays left plain),
    a row of horse-stable arches above"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        if alt and i not in bos:
            y.kemerli(p, q, Z0, HL, DUV, v0=0.0, en=0.74, ust=0.03, derin=0.16, k_say=10, cerceve=(0.011, [KUMA, KUM]))
        else:
            duz_duvar(y, p, q, Z0, ZG, KUM)
    m = ust_n or n * 2
    for i in range(m):
        p, q = a.lerp(b, i / m), a.lerp(b, (i + 1) / m)
        y.kemerli(p, q, ZG, HU, DUV, v0=0.0, en=0.6, ust=0.025, derin=0.07, k_say=8, cerceve=(0.008, [KUMA, KUM]))


def galeri(a, b, uclar=''):
    """the corbelled stone gallery along a face a->b (projecting to the right) at the upper floor, with a parapet;
    uclar: 'a' / 'b' close a free end"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    q = [a + Z * ZG, b + Z * ZG, b + nn * GD + Z * ZG, a + nn * GD + Z * ZG]
    y.yuz_yon(q, 'zemin', Z)
    y.yuz_yon([p - Z * 0.012 for p in q], KUMK, -Z)
    y.yuz_yon([q[3], q[2], q[2] - Z * 0.012, q[3] - Z * 0.012], KUMA, nn)
    if 'a' in uclar: y.yuz_yon([q[0], q[3], q[3] - Z * 0.012, q[0] - Z * 0.012], KUMA, -e)
    if 'b' in uclar: y.yuz_yon([q[2], q[1], q[1] - Z * 0.012, q[2] - Z * 0.012], KUMA, e)
    m = int(L / 0.07)
    for j in range(m + 1):   # corbels
        c = a + e * (0.02 + (L - 0.04) * j / m)
        for k in range(3):
            o = c - e * 0.008 + Z * (ZG - 0.012 - 0.012 * (k + 1))
            kutu_merkez(y, (o.x + e.x * 0.008 + nn.x * GD * (1 - 0.3 * k) / 2, o.y + e.y * 0.008 + nn.y * GD * (1 - 0.3 * k) / 2), 0.016,
                        GD * (1 - 0.3 * k), 0.012, KUM, z0=o.z, aci=math.atan2(e.y, e.x))
    # the parapet on the gallery's edge
    pa, pb = a + nn * (GD - 0.008), b + nn * (GD - 0.008)
    kutu(y, pa + Z * ZG, e, L, 0.008, 0.028, KUMA, 'onarkasagsolust')


def dis_duvar(a, b, z0=Z0, z1=ZT):
    """an outer face of the wall a->b: courses, a battered plinth, buttresses, arrow slits, a string course"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    duz_duvar(y, a, b, z0, z1, KUM)
    silme(y, [a, b], z0, 0.03, 0.014, KUMK, 'kaide', kapali=False)
    silme(y, [a, b], ZG, 0.008, 0.006, KUMA, 'duz', kapali=False)
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    m = int(L / 0.16)
    for j in range(1, m):
        c = a + e * (L * j / m) + nn * 0.01
        kutu_merkez(y, (c.x, c.y), 0.03, 0.02, ZG - z0 - 0.03, KUM, z0=z0 + 0.03, aci=math.atan2(e.y, e.x))
    for j in range(m):
        for v in (ZG - 0.11, ZG + 0.06):
            yarik(y, a, e, nn, L * (j + 0.5) / m - 0.005, v, 0.01, 0.045, 'koyu')


def ust_kenar(kose, kapali=False):
    """the wall top: a cavetto cornice and merlons along an outer polyline"""
    silme(y, kose, ZT - 0.03, 0.03, 0.018, KUMA, KAVETTO, kapali=kapali)
    parapet(y, disa(kose, 0.018, kapali), ZT, 0.008, 0.024, 0.012, KUM, kapali=kapali)


y.bolum('Arka kanat: fil ve at ahırları')
x0, x1, y0, y1 = BW
# yard faces of the back wing, either side of the central tower
for a, b in (((-WX, y0), (-0.17, y0)), ((0.17, y0), (WX, y0))):
    duvar_kemerli(a, b, 3, ust_n=6)
    galeri(V(*a), V(*b))
dis_duvar((x1, y1), (x0, y1))
y.yuz_yon(dikdortgen(x0, x1, y0, y1, ZT), 'zemin', Z)
ust_kenar([V(x1, y1), V(x0, y1)])
for a, b in (((-WX, y0), (-0.17, y0)), ((0.17, y0), (WX, y0))):
    parapet(y, [V(*a), V(*b)], ZT, 0.008, 0.02, 0.01, KUM, kapali=False)

y.bolum('Yan kanatlar')
for s in (-1, 1):
    xi, xo = s * WX, s * 1.0
    # the yard face (bays counted from a): stalls behind the ramp's run (the front three) left plain
    a, b = (V(xi, WY0 + 0.26), V(xi, BW[2])) if s < 0 else (V(xi, BW[2]), V(xi, WY0 + 0.26))
    n = 7
    bos = (0, 1, 2) if s < 0 else (4, 5, 6)
    duvar_kemerli(a, b, n, bos=bos, ust_n=10)
    # the gallery runs from the ramp's head landing to the back wing's gallery (not over the ramp, not doubled at the corner)
    ga, gb = V(xi, WY0 + 0.27 + 0.45), V(xi, BW[2] - GD)
    galeri(ga, gb) if s < 0 else galeri(gb, ga)
    dis_duvar(V(xo, BW[3]) if s < 0 else V(xo, WY0 + 0.26), V(xo, WY0 + 0.26) if s < 0 else V(xo, BW[3]))
    xa, xb = sorted((xi, xo))
    y.yuz_yon(dikdortgen(xa, xb, WY0 + 0.26, BW[2], ZT), 'zemin', Z)
    ust_kenar([V(xo, BW[3]), V(xo, WY0 + 0.26)] if s < 0 else [V(xo, WY0 + 0.26), V(xo, BW[3])])
    parapet(y, [a, b], ZT, 0.008, 0.02, 0.01, KUM, kapali=False)


# ================================================================ the towers
def kule(x0, x1, y0, y1, z0, h, yuzler='onarkasagsol', kapi=None, pencere=True):
    """a square Punic tower: courses, a plinth, two rows of windows, a cavetto cornice, merlons, a flat top"""
    kutu(y, V(x0, y0, z0), X, x1 - x0, y1 - y0, h, KUM, yuzler)
    k = dikdortgen(x0, x1, y0, y1)
    if z0 <= Z0 + 1e-6:
        silme(y, k, Z0, 0.03, 0.014, KUMK, 'kaide')
    silme(y, k, ZT, 0.008, 0.006, KUMA, 'duz')
    silme(y, k, z0 + h - 0.04, 0.04, 0.024, KUMA, KAVETTO)
    y.yuz_yon([V(p.x, p.y, z0 + h) for p in k], "zemin", Z)
    parapet(y, disa(k, 0.024), z0 + h, 0.01, 0.026, 0.012, KUM)
    if pencere:
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
            for v in (ZT + 0.05, ZT + 0.05 + (z0 + h - ZT - 0.1) * 0.5):
                if v + 0.06 > z0 + h - 0.045: continue
                for j in range(2):
                    pencere_kutu(y, a, e, nn, L * (0.3 + 0.4 * j) - 0.01, v, 0.02, 0.05, 'koyu', cerceve=KUMA)
    return z0 + h


# ================================================================ barracks on the wall tops (the soldiers' quarters)
y.bolum('Duvar üstü kışlalar')


def kisla(x0, x1, y0, y1, h=0.075):
    """a long barrack block on the wall walk: plastered walls with small windows and doors, a tiled gable roof"""
    kutu(y, V(x0, y0, ZT), X, x1 - x0, y1 - y0, h, 'siva_krem', 'onarkasagsol')
    k = dikdortgen(x0, x1, y0, y1)
    silme(y, k, ZT, 0.01, 0.005, KUM, 'kaide')
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
        m = int(L / 0.06)
        for j in range(m):
            if j % 4 == 2:
                pencere_kutu(y, a, e, nn, L * (j + 0.5) / m - 0.01, ZT, 0.02, 0.045, 'ahsap_koyu', cerceve=KUMA)
            else:
                pencere_kutu(y, a, e, nn, L * (j + 0.5) / m - 0.007, ZT + 0.035, 0.014, 0.022, 'koyu')
    cati_besik(y, x0, x1, y0, y1, ZT + h, min(x1 - x0, y1 - y0) * 0.36, 0.018, 'kiremit', mahya='kiremit2', ucluk_key='siva_krem',
               alinlik_key=KUMA, alt_key='ahsap_koyu', kalinlik=0.006, ns=max(4, int(max(x1 - x0, y1 - y0) / 0.12)), nr=3, dilim=['kiremit', 'kiremit2'])


for s in (-1, 1):
    xa, xb = sorted((s * 0.64, s * 0.19))
    kisla(xa, xb, BW[2] + 0.03, BW[2] + 0.2)
    xa, xb = sorted((s * 0.86, s * 0.675))
    kisla(xa, xb, WY0 + 0.29, BW[2] + 0.11)

y.bolum('Kuleler')
# the corner towers (rising from the wall top), the wings' front towers (from the ground), the great central tower
for s in (-1, 1):
    xa, xb = sorted((s * 0.74, s * 1.0))
    kule(xa, xb, 0.59, 0.85, ZT, 0.3)
    # (their lower part is the wall: faces from the wall top only)
    xa, xb = sorted((s * WX, s * 1.0))
    kule(xa, xb, WY0, WY0 + 0.26, Z0, ZT - Z0 + 0.2)
kule(-0.17, 0.17, BW[2] - 0.08, BW[3] + 0.012, Z0, 0.8, yuzler='arkasagsol')
duz_duvar(y, V(-0.17, BW[2] - 0.08), V(0.17, BW[2] - 0.08), Z0 + 0.3, Z0 + 0.8 - 0.04, KUM)   # (the front above the gate arch)
# the elephant gate in the great tower, with the winged sun and the sign of Tanit
y.kemerli(V(-0.17, BW[2] - 0.08), V(0.17, BW[2] - 0.08), Z0, 0.3, DUV, v0=0.0, en=0.56, ust=0.05, derin=0.06, k_say=12, cerceve=(0.014, [KUMA, KUM]))
kanatli_gunes(y, V(0, BW[2] - 0.08, Z0 + 0.335), X, -Y, 0.22, 0.036)
tanit_kabartma(y, V(0, BW[2] - 0.08, Z0 + 0.46), X, -Y, 0.09, 'altin')
sancak(y, 0.0, BW[3] - 0.15, Z0 + 0.8, boy=0.24, en=0.12, yuk=0.07, aci=D(160))
for s in (-1, 1):
    sancak(y, s * 0.825, WY0 + 0.13, ZT + 0.2, boy=0.15, en=0.08, yuk=0.05, aci=D(200))


# ================================================================ ramps up to the gallery
y.bolum('Rampalar')
for s in (-1, 1):
    xi = s * WX
    xr = xi - s * 0.07                       # the ramp's yard edge
    ry0, ry1 = WY0 + 0.27, WY0 + 0.27 + 0.4   # the ramp's foot and head (along y)
    zf = lambda yy: Z0 + (ZG - Z0) * (yy - ry0) / (ry1 - ry0)
    xa, xb = sorted((xi, xr))
    # top slope, the yard-facing side, the low end
    y.yuz_yon([V(xa, ry0, Z0), V(xb, ry0, Z0), V(xb, ry1, ZG), V(xa, ry1, ZG)], 'zemin', Z + V(0, -0.4, 0))
    side = [V(xr, ry0, Z0), V(xr, ry1, Z0), V(xr, ry1, ZG)]
    y.yuz_yon(side, KUM, V(-s, 0, 0))
    # the ramp's head meets the gallery: a landing block
    y.yuz_yon([V(xr, ry1, Z0), V(xr, ry1 + 0.05, Z0), V(xr, ry1 + 0.05, ZG), V(xr, ry1, ZG)], KUM, V(-s, 0, 0))
    y.yuz_yon(dikdortgen(xa, xb, ry1, ry1 + 0.05, ZG), 'zemin', Z)
    y.yuz_yon([V(xa, ry1 + 0.05, Z0), V(xb, ry1 + 0.05, Z0), V(xb, ry1 + 0.05, ZG), V(xa, ry1 + 0.05, ZG)], KUM, Y)
    # its parapet (sloping) and arched relieving niches on the side
    for zz0 in (0.0,):
        q = [V(xr, ry0, Z0), V(xr, ry1, ZG), V(xr, ry1, ZG + 0.03), V(xr, ry0, Z0 + 0.03)]
        on = [p + V(s * 0.0, 0, 0) for p in q]
        ic = [p + V(s * 0.008, 0, 0) for p in q]
        y.yuz_yon(on, KUMA, V(-s, 0, 0))
        y.yuz_yon(ic, KUMA, V(s, 0, 0))
        y.yuz_yon([on[3], on[2], ic[2], ic[3]], KUMA, Z + V(0, -0.4, 0))
        y.yuz_yon([on[0], on[3], ic[3], ic[0]], KUMA, -Y)
    for j in range(3):
        yy = ry0 + 0.16 + 0.11 * j
        c = V(xr - s * 0.001, yy)
        hh = zf(yy) - Z0 - 0.025
        if hh < 0.04: continue
        e = V(0, -s); nn = V(-s, 0)
        pencere_kutu(y, c, e, nn, -0.02, Z0 + 0.012, 0.04, hh * 0.7, 'kum_koyu')
    # a horse being led up
    yy = ry0 + 0.22
    at(y, xi - s * 0.035, yy, zf(yy), D(90), 0.8, 'ahsap', 'ahsap_koyu', faz=0.3)
    insan(y, xi - s * 0.035, yy + 0.06, zf(yy + 0.06), 'kumas', 0.9, 'kerpic', D(90), 0.4, None)


# ================================================================ the animals
y.bolum('Ahırdaki filler ve atlar')


def savas_kulesi(x, yy, z, aci, s):
    """a crenellated fighting tower on a war elephant's back with two soldiers and painted shields"""
    with parca(y, (x, yy, z), aci, s):
        zt = 0.106
        kutu_merkez(y, (-0.004, 0.0), 0.044, 0.036, 0.03, 'ahsap', z0=zt)
        kutu_merkez(y, (-0.004, 0.0), 0.05, 0.042, 0.006, 'ahsap_koyu', z0=zt - 0.004)
        k = dikdortgen(-0.026, 0.018, -0.018, 0.018)
        parapet(y, k, zt + 0.03, 0.0, 0.01, 0.004, 'ahsap')
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            c = a.lerp(b, 0.5) + nn * 0.0004 + Z * (zt + 0.016)
            prizma2(y, [(0.008 * math.cos(TAU * j / 8), 0.008 * math.sin(TAU * j / 8)) for j in range(8)],
                    lambda u, v, d, c=c, e=e, nn=nn: c + e * u + Z * v + nn * d, 0.0015, ('boya_kirmizi', 'bronz', 'boya_kirmizi', 'bronz')[i], nn)
        for j, (dx, dy) in enumerate(((-0.012, -0.007), (0.004, 0.007))):
            insan(y, dx, dy, zt + 0.008, ('boya_kirmizi', 'mor')[j], 0.62, 'kum_acik', 0.0, 0.6 if j == 0 else 0.0, 'bronz', mizrak='demir' if j else None)


def ahir_fili(cx, cy, aci, olcek=0.82, kaba=True, tohum=0):
    fil(y, cx, cy, Z0, aci, olcek, 'fil', cul=None, hortum=random.Random(tohum).uniform(0.0, 0.02), kaba=kaba, afrika=True)


# elephants in the back wing's stalls (facing the yard: -y) and in the wings' stalls
for k, xx in enumerate((-0.57, -0.41, -0.25, 0.25, 0.41, 0.57)):
    if k in (1, 4): continue
    ahir_fili(xx, BW[2] + 0.07, D(-90), tohum=k)
for s in (-1, 1):
    n = 7
    for j in ((3, 4, 6) if s < 0 else (3, 5, 6)):   # bays counted from the front
        yy = WY0 + 0.26 + (BW[2] - WY0 - 0.26) * (j + 0.5) / n
        ahir_fili(s * (WX + 0.075), yy, 0.0 if s < 0 else math.pi, tohum=10 + j)
# horses looking out of the upper stables
for (x, yy, a) in ((-0.45, BW[2] + 0.04, D(-90)), (0.37, BW[2] + 0.04, D(-90)), (0.61, BW[2] + 0.04, D(-90))):
    at(y, x, yy, ZG, a, 0.7, gr.choice(('ahsap', 'ahsap_acik', 'koyu')), 'ahsap_koyu')
for s in (-1, 1):
    for yy in (0.086, 0.294):
        at(y, s * (WX + 0.035), yy, ZG, 0.0 if s < 0 else math.pi, 0.7, gr.choice(('ahsap', 'ahsap_acik', 'beyaz')), 'ahsap_koyu')

y.bolum('Avlu: savaş filleri, bakıcılar')
for k, (x, yy, a, hortum) in enumerate(((-0.3, -0.25, D(20), 0.03), (0.28, -0.05, D(200), 0.0), (0.32, -0.52, D(150), 0.015), (-0.2, 0.18, D(-60), 0.01))):
    fil(y, x, yy, Z0 + 0.002, a, 1.05, 'fil', cul='boya_kirmizi', sus='altin', hortum=hortum, afrika=True)
    savas_kulesi(x, yy, Z0 + 0.002, a, 1.05)
    e = V(math.cos(a), math.sin(a))
    # the mahout on the neck
    insan(y, x + e.x * 0.04, yy + e.y * 0.04, Z0 + 0.103, 'beyaz', 0.7, 'kerpic', a, 0.0, 'kece')
    # a keeper with a goad walking beside
    sx = V(-e.y, e.x)
    p = V(x, yy) + e * 0.07 + sx * 0.06
    insan(y, p.x, p.y, Z0 + 0.002, 'kumas', 1.05, 'kerpic', a, 0.7, None)
# a young elephant and one being washed at the trough
fil(y, 0.48, 0.2, Z0 + 0.002, D(-150), 0.7, 'fil', hortum=0.035, afrika=True)
fil(y, -0.46, -0.6, Z0 + 0.002, D(80), 0.98, 'fil', hortum=0.04, cul=None, afrika=True)
# the long stone water trough
tk = dikdortgen(-0.58, -0.36, -0.75, -0.69)
duvarlar(y, tk, Z0, Z0 + 0.03, KUM, ust=KUMA, kalinlik=0.008)
y.yuz_yon([V(p.x, p.y, Z0 + 0.024) for p in disa(tk, -0.008)], 'su', Z)
insan(y, -0.4, -0.64, Z0, 'kumas', 1.0, 'kerpic', D(200), 1.0, None)
# fodder stacks and baskets
for (x, yy, r) in ((0.52, -0.72, 0.05), (0.42, -0.76, 0.04), (0.56, -0.62, 0.035), (-0.55, 0.32, 0.04)):
    donel(y, (x, yy), [(r, Z0), (r * 1.05, Z0 + r * 0.6), (r * 0.6, Z0 + r * 1.2), (0.0, Z0 + r * 1.45)], 'saz', n=8)
for k in range(5):
    donel(y, (0.15 + 0.03 * k, -0.78), [(0.01, Z0), (0.013, Z0 + 0.02), (0.0, Z0 + 0.021)], 'saz_koyu', n=6)
# tethering posts with iron rings (the elephants are chained to them for the night), a fodder cart
for k in range(3):
    px = -0.16 + 0.05 * k
    y.prizma((px, -0.4), 0.011, Z0, Z0 + 0.075 + 0.008 * (k % 2), 'kutuk', n=7)
    kure(y, (px, -0.4, Z0 + 0.082 + 0.008 * (k % 2)), 0.011, 'kutuk', n=7, kat=3)
    boru(y, [V(px + 0.011 * math.cos(TAU * i / 8), -0.4 + 0.011 * math.sin(TAU * i / 8), Z0 + 0.05) for i in range(9)], 0.0022, 'demir', n=4, kapat=False)
boru(y, [V(-0.16, -0.389, Z0 + 0.05), V(-0.135, -0.37, Z0 + 0.004), V(-0.11, -0.39, Z0 + 0.05)], 0.0018, 'demir', n=4)
araba(y, 0.4, -0.62, Z0, D(120), 1.3, yuk='saz')
# the street in front: palms
for (x, yy) in ((-0.5, -1.05), (0.5, -1.05), (-1.07, -1.07), (1.07, -1.07)):
    agac(y, x, yy, Z0, 0.16, 'palmiye', 'zeytin', 'ahsap_acik')
for k in range(6):
    insan(y, -0.3 + 0.12 * k, -1.0 + 0.04 * (k % 2), Z0, gr.choice(('kumas', 'beyaz', 'mor', 'boya_kirmizi')), 1.0, 'kerpic', gr.uniform(0, TAU), 0.0, None)

calistir(y, 'lm_filahirlari')
