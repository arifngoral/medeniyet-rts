# Great Caravan Inn (lm_kervanhani), after Aleppo's Khan al-Gumruk: a two-storey stone khan round an arcaded court.
# The street front is a row of shops with timber awnings and goods, the monumental gate in black-and-yellow ablaq
# with a muqarnas hood in the middle; inside, pointed arcades below and a balustraded gallery above, a domed fountain
# kiosk in the centre, the khan's mosque with its dome and a square Syrian minaret at the back; rows of small domes on
# the roofs; laden and kneeling camels, bales, jars and merchants in the court and a caravan arriving outside.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from arap_ortak import *

y = Yapi()

Z0 = 0.04
TAS, ACIK, KOYU, KARA = 'kum', 'kum_acik', 'kum_koyu', 'bazalt'
AB = [ACIK, KARA]                          # Aleppo ablaq: pale limestone and black basalt
REN = (TAS, KOYU, ACIK, 'koyu')
H1, H2 = 0.18, 0.16
ZR = Z0 + H1 + H2
XO, YO0, YO1 = 0.95, -0.62, 0.86           # outer walls: x +-XO, y YO0..YO1
CX, CY0, CY1 = 0.62, -0.32, 0.56           # court: x +-CX, y CY0..CY1

y.bolum('Zemin ve sokak')
zemin(y, -1.12, 1.12, -1.0, 0.98, Z0, 'kum_koyu', 'zemin', basamak=(('on', 0.6),), n_basamak=2)
y.yuz_yon([V(-1.1, -0.98, Z0 + 0.002), V(1.1, -0.98, Z0 + 0.002), V(1.1, YO0 - 0.16, Z0 + 0.002), V(-1.1, YO0 - 0.16, Z0 + 0.002)], 'toprak', Z)

# ---------------- the street front: shops either side of the gate ----------------
y.bolum('Sokak cephesi: dükkânlar')
GW = 0.44                                  # the gate block's width


def dukkan(a, b, k):
    """a shop bay a->b on the street front: an open stall with a dark inside, a basalt frame, a timber awning on
    brackets, a rug hanging from it and goods set out before it"""
    W, e, nc, L = dikdortgen_acik(y, a, b, Z0, H1, 0.1, 0.9, 0.0, 0.13, (TAS, KOYU, ACIK, 'koyu'), derin=0.035, cerceve=(0.006, KARA))
    # the awning: a thin closed slab sloping out from the wall
    zt = Z0 + 0.15
    p0, p1 = L(0.04, 0.15 - 0.0), L(0.96, 0.15)
    q0, q1 = p0 + nc * 0.07 - Z * 0.025, p1 + nc * 0.07 - Z * 0.025
    dz = Z * 0.005
    y.yuz_yon([p0, p1, q1, q0], 'ahsap_dikey', Z + nc * 0.3)
    y.yuz_yon([p0 - dz, p1 - dz, q1 - dz, q0 - dz], 'ahsap_koyu', -Z)
    y.yuz_yon([q0, q1, q1 - dz, q0 - dz], 'ahsap_koyu', nc)
    y.yuz_yon([p0, q0, q0 - dz, p0 - dz], 'ahsap_koyu', -e)
    y.yuz_yon([p1, q1, q1 - dz, p1 - dz], 'ahsap_koyu', e)
    for u in (0.1, 0.9):
        cubuk(y, L(u, 0.1, 0) + nc * 0.003, L(u, 0.145, 0) + nc * 0.05 - Z * 0.02, 0.004, 'ahsap_koyu')
    # a rug hung from the awning's edge
    if k % 2 == 0:
        m = (q0 + q1) / 2 + e * (W * 0.18)
        w2 = W * 0.16
        r = [m - e * w2 - dz, m + e * w2 - dz, m + e * w2 - Z * 0.07, m - e * w2 - Z * 0.07]
        iki_yuzlu(y, r, ('boya_kirmizi', 'lacivert', 'turkuaz', 'boya_sari')[k // 2 % 4], nc)
        y.yuz_yon([r[0] + nc * 0.0006, r[1] + nc * 0.0006, r[1] + nc * 0.0006 - Z * 0.008, r[0] + nc * 0.0006 - Z * 0.008], 'boya_sari', nc)
    # goods: bales, jars, a basket of produce
    g = L(0.3, 0) + nc * 0.035
    if k % 3 == 0:
        denk(y, g.x, g.y, Z0 + 0.002, 'kumas', math.atan2(e.y, e.x), w=0.05, d=0.035, h=0.03)
        denk(y, g.x + e.x * 0.05, g.y + e.y * 0.05, Z0 + 0.002, 'boya_kirmizi', math.atan2(e.y, e.x) + 0.2, w=0.045, d=0.035, h=0.028)
    elif k % 3 == 1:
        for j in range(3):
            p = g + e * (0.03 * j)
            kup(y, p.x, p.y, Z0 + 0.002, r=0.014, h=0.04, key='kiremit' if j % 2 else 'kiremit2')
    else:
        donel(y, (g.x + e.x * 0.03, g.y + e.y * 0.03), [(0.0, Z0 + 0.002), (0.02, Z0 + 0.002), (0.026, Z0 + 0.022), (0.0, Z0 + 0.0225)], 'saz', n=10)
        for j in range(5):
            kure(y, (g.x + e.x * (0.022 + 0.006 * j), g.y + e.y * (0.022 + 0.006 * j) + 0.003 * (j % 2), Z0 + 0.026), 0.007, 'boya_sari' if j % 2 else 'boya_kirmizi', n=6, kat=3)


NS = 4
for sx in (-1, 1):
    xa, xb = sx * (GW / 2), sx * XO
    for k in range(NS):
        p, q = V(xa + (xb - xa) * k / NS, YO0), V(xa + (xb - xa) * (k + 1) / NS, YO0)
        if sx < 0: p, q = q, p           # (run +x: facing the street)
        dukkan(p, q, k + (0 if sx > 0 else 1))
    # the upper storey: small pointed windows over the shops, an ablaq string course
    a, b = (V(-XO, YO0), V(-GW / 2, YO0)) if sx < 0 else (V(GW / 2, YO0), V(XO, YO0))
    kat_pencere(y, a, b, Z0 + H1, ZR, Z0 + H1 + 0.05, Z0 + H1 + 0.12, NS * 2, REN, en=0.34, sivri=0.6, derin=0.012)
    ablak(y, a, b, Z0 + H1 - 0.0, Z0 + H1 + 0.02, AB, 0.01, on=0.0025)
    silme(y, [a, b], ZR - 0.022, 0.012, 0.008, ACIK, 'tac', kapali=False)
    silme(y, [a, b], Z0, 0.02, 0.006, KOYU, 'kaide', kapali=False)


def masrabiye(cx, z, w=0.13, d=0.05, h=0.11):
    """a projecting timber oriel (mashrabiya) on the street front: a lattice front and sides, corbels under it, a
    small hood on top"""
    o = V(cx - w / 2, YO0 - d)
    kutu(y, o + Z * z, X, w, d, h, 'ahsap', 'onsagsolust')
    kutu(y, o + Z * (z + h) - V(0.006, 0.006), X, w + 0.012, d + 0.006, 0.008, 'ahsap_koyu', 'onsagsolust')
    y.yuz_yon([o + Z * z, o + X * w + Z * z, o + X * w + Y * d + Z * z, o + Y * d + Z * z], 'ahsap_koyu', -Z)
    for (a, b, nu) in ((o, o + X * w, 6), (o + Y * d, o, 2), (o + X * w, o + X * w + Y * d, 2)):
        W_ = (b - a).length; e = (b - a) / W_; nc = V(e.y, -e.x)
        L = lambda u, v: a + e * (u * W_) + nc * 0.0015 + Z * (z + v)
        y.yuz_yon([L(0.08, 0.015), L(0.92, 0.015), L(0.92, h - 0.012), L(0.08, h - 0.012)], 'koyu', nc)
        kafes(y, a, b, z, 0.08, 0.92, 0.015, h - 0.012, 'ahsap_acik', nu * 2, 6, 0.003, -0.0045)
    for k in range(3):   # corbels under it
        xk = cx - w / 2 + 0.015 + (w - 0.03) * k / 2
        kutu(y, V(xk - 0.006, YO0 - d * 0.8, z - 0.025), X, 0.012, d * 0.8, 0.025, 'ahsap_koyu', 'onsagsol')
        y.yuz_yon([V(xk - 0.006, YO0 - d * 0.8, z - 0.025), V(xk + 0.006, YO0 - d * 0.8, z - 0.025), V(xk + 0.006, YO0, z - 0.04), V(xk - 0.006, YO0, z - 0.04)], 'ahsap_koyu', -Z - Y)
        for s in (-1, 1):
            y.yuz_yon([V(xk + s * 0.006, YO0 - d * 0.8, z - 0.025), V(xk + s * 0.006, YO0, z - 0.04), V(xk + s * 0.006, YO0, z - 0.025)], 'ahsap_koyu', V(s, 0))


for cx in (-0.62, 0.62):
    masrabiye(cx, Z0 + H1 + 0.035)

# ---------------- the gate ----------------
y.bolum('Ablak taçkapı')
GH = 0.6
GY = YO0 - 0.04
gtop = tackapi_mukarnas(y, 0.0, GY, Z0, en=GW, H=GH, derin=0.17, nis=0.52, sivri=0.62, kapi_key='ahsap', key=TAS,
                        bordur=(KARA, ACIK), mk_kat=6, cerceve=(0.016, AB), tonlar=(ACIK, KARA))
# the flanks and the back above the roof in ablaq courses; carved roundels on the front
for sx in (-1, 1):
    x = sx * GW / 2 + sx * 0.0025
    a, b = (V(x, GY + 0.1725), V(x, GY)) if sx < 0 else (V(x, GY), V(x, GY + 0.1725))
    ablak(y, a, b, ZR, Z0 + GH, AB, 0.026)
ablak(y, V(GW / 2 + 0.0025, GY + 0.1725), V(-GW / 2 - 0.0025, GY + 0.1725), ZR, Z0 + GH, AB, 0.026)
for sx in (-1, 1):
    yildiz(y, (sx * GW * 0.31, GY - 0.006, Z0 + GH * 0.8), X, -Y, 0.022, ACIK, k=12, ic=0.7, yan_key=KARA)
    # stone benches at the gate's foot
    kutu_merkez(y, (sx * GW * 0.28, GY - 0.03), 0.07, 0.035, 0.03, ACIK, z0=Z0)
# a crown of stepped merlons over the gate
mazgalli_kenar(y, dikdortgen(-GW / 2, GW / 2, GY, GY + 0.17), Z0 + GH + 0.002, TAS, kal=0.016, h=0.03, ust_key=ACIK, dolu=0.01, w=0.024, g=0.014, kademe=True)

# ---------------- the outer walls ----------------
y.bolum('Dış duvarlar')
for (a, b, n) in ((V(XO, YO0), V(XO, YO1), 8), (V(XO, YO1), V(-XO, YO1), 10), (V(-XO, YO1), V(-XO, YO0), 8)):
    kat_pencere(y, a, b, Z0, ZR, Z0 + H1 + 0.05, Z0 + H1 + 0.12, n, REN, en=0.3, sivri=0.6, derin=0.012)
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(n):
        p = a.lerp(b, (k + 0.5) / n)
        yarik(y, p + nn * 0.001, e, nn, -0.005, Z0 + 0.06, 0.01, 0.07, 'koyu')
    ablak(y, a, b, Z0 + H1, Z0 + H1 + 0.02, AB, 0.01, on=0.0025)
    silme(y, [a, b], ZR - 0.022, 0.012, 0.008, ACIK, 'tac', kapali=False)
    silme(y, [a, b], Z0, 0.02, 0.006, KOYU, 'kaide', kapali=False)
# quoins: ablaq blocks up the corners
for (cx, cy) in ((XO, YO0), (XO, YO1), (-XO, YO1), (-XO, YO0)):
    for j in range(int((ZR - Z0) / 0.04)):
        s = 0.03 if j % 2 == 0 else 0.022
        kutu_merkez(y, (cx, cy), s + 0.006, s + 0.006, 0.02, AB[j % 2], z0=Z0 + j * 0.04 + 0.01)
for yol_ in ([V(GW / 2, YO0), V(XO, YO0), V(XO, YO1), V(0.2, YO1)], [V(-0.2, YO1), V(-XO, YO1), V(-XO, YO0), V(-GW / 2, YO0)]):   # (broken at the mosque's back)
    mazgalli_kenar(y, yol_, ZR, TAS, kal=0.016, h=0.024, kapali=False, ust_key=ACIK, dolu=0.012, w=0.03, g=0.022)

# ---------------- the court ----------------
y.bolum('Avlu: alt revaklar ve üst galeri')
ck = dikdortgen(-CX, CX, CY0, CY1)
y.yuz_yon([V(p.x, p.y, Z0 + 0.002) for p in ck], 'zemin', Z)
# (side 0 front, 1 east, 2 back, 3 west)
avlu_revak(y, (-CX, CX, CY0, CY1), Z0, H1, [7, 5, 7, 5], REN, en=0.72, ust=0.025, derin=0.08, sivri=0.62, sutunlu=False,
           cerceve=(0.009, AB), atla=(2,))
avlu_revak(y, (-CX, CX, CY0, CY1), Z0 + H1, H2, [7, 5, 7, 5], REN, en=0.62, ust=0.022, derin=0.06, sivri=0.62, sutunlu=False,
           atla=(2,), korkuluk=0.035)
for i in (0, 1, 3):
    a, b = ck[(i + 1) % 4], ck[i]
    silme(y, [a, b], Z0 + H1 - 0.01, 0.012, 0.009, ACIK, 'duz', kapali=False)
    ablak(y, a + (V(b.y - a.y, a.x - b.x).normalized() * 0.0025), b + (V(b.y - a.y, a.x - b.x).normalized() * 0.0025), ZR - 0.02, ZR - 0.004, AB, 0.008)
# the back side: arcades either side of the mosque
a, b = ck[3], ck[2]                         # (run +x: faces the court)
MW = 0.2
for (pa, pb, n) in ((a, V(-MW - 0.02, CY1), 3), (V(MW + 0.02, CY1), b, 3)):
    for j in range(n):
        p, q = pa.lerp(pb, j / n), pa.lerp(pb, (j + 1) / n)
        y.kemerli(p, q, Z0, H1, REN, en=0.72, ust=0.025, derin=0.08, k_say=10, sivri=0.62, cerceve=(0.009, AB))
        y.kemerli(p, q, Z0 + H1, H2, REN, v0=0.0, en=0.62, ust=0.022, derin=0.06, k_say=10, sivri=0.62, korkuluk=0.035)
    silme(y, [pa, pb], Z0 + H1 - 0.01, 0.012, 0.009, ACIK, 'duz', kapali=False)
duz_duvar(y, V(-MW - 0.02, CY1), V(-MW, CY1), Z0, ZR, TAS)
duz_duvar(y, V(MW, CY1), V(MW + 0.02, CY1), Z0, ZR, TAS)
cp = [ck[3], ck[2], ck[1], ck[0]]
parapet(y, cp, ZR, 0.016, 0, 0.012, TAS, ust_key=ACIK)

y.bolum('Damlar ve kubbecikler')
for (x0, x1, y0, y1) in ((-XO, XO, YO0, CY0), (CX, XO, CY0, CY1), (-XO, XO, CY1, YO1), (-XO, -CX, CY0, CY1)):   # (no overlaps)
    y.yuz_yon([V(x0, y0, ZR), V(x1, y0, ZR), V(x1, y1, ZR), V(x0, y1, ZR)], 'zemin', Z)
    dam_bolme(y, x0, x1, y0, y1, ZR, ACIK)
# stone spouts under the parapets
for (a, b, n) in ((V(XO, YO0), V(XO, YO1), 7), (V(XO, YO1), V(-XO, YO1), 8), (V(-XO, YO1), V(-XO, YO0), 7)):
    oluk(y, a, b, n, ZR - 0.024, KOYU)
KUB = []
for k in range(7):
    x = -0.8 + k * 0.267
    if abs(x) > 0.2: KUB.append((x, (YO0 + CY0) / 2))
    if abs(x) > 0.3: KUB.append((x, (YO1 + CY1) / 2))
for k in range(4):
    yy = CY0 + 0.1 + k * 0.23
    KUB += [(-(XO + CX) / 2, yy), ((XO + CX) / 2, yy)]
for (cx, cy) in KUB:
    y.prizma((cx, cy), 0.06, ZR, ZR + 0.018, ACIK, n=12, ust=False)
    y.kubbe((cx, cy), 0.06, ZR + 0.018, 0.045, ACIK, n=12, kat=4)
    kure(y, (cx, cy, ZR + 0.066), 0.006, ACIK, n=6, kat=3)

# ---------------- the mosque and minaret ----------------
y.bolum('Han mescidi: kubbe ve Şam tipi minare')
MY0, MY1 = CY1 - 0.06, CY1 + 0.3
mk = dikdortgen(-MW, MW, MY0, MY1)
ZMQ = ZR + 0.07
for i in range(4):
    a, b = mk[i], mk[(i + 1) % 4]
    if i == 0:   # the court front: a pointed portal and windows
        n = 3
        for j in range(n):
            p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
            if j == 1:
                kemer_nis(y, p, q, Z0, ZMQ - Z0 - 0.02, en=0.7, ust=0.03, sivri=0.62, derin=0.03, key=TAS, yan_key=KOYU, alt_key=ACIK,
                          arka_key='ahsap', k_say=10, cerceve=(0.01, AB))
                duz_duvar(y, p, q, ZMQ - 0.02, ZMQ, TAS)
            else:
                kat_pencere(y, p, q, Z0, Z0 + 0.15, Z0 + 0.06, Z0 + 0.14, 1, REN, en=0.42, derin=0.012, cerceve=(0.006, KARA))   # (up to the upper row only)
                kat_pencere(y, p, q, Z0 + 0.15, ZMQ, Z0 + 0.22, Z0 + 0.31, 1, REN, en=0.4, sivri=0.6, derin=0.012)
    else:
        if i == 2:   # (the back: its top above the roofs with two windows)
            kat_pencere(y, a, b, ZR, ZMQ, ZR + 0.012, ZMQ - 0.012, 2, REN, en=0.32, sivri=0.6, derin=0.01)
        else:
            duvar_bant(y, a, b, Z0, ZMQ, TAS, n=3)
ablak(y, mk[0], mk[1], ZMQ - 0.06, ZMQ - 0.01, AB, 0.0125, on=0.0025)
silme(y, mk, ZMQ - 0.012, 0.012, 0.008, ACIK, 'tac')
mazgalli_kenar(y, mk, ZMQ, TAS, kal=0.014, h=0.024, ust_key=ACIK, dolu=0.01, w=0.024, g=0.016)
y.yuz_yon([V(p.x, p.y, ZMQ) for p in disa(mk, -0.014)], 'zemin', Z)
MC = (0.0, (MY0 + MY1) / 2)
RD = 0.13
zd = kubbe_kasnakli(y, MC, RD, ZMQ, 0.06, n_pencere=12, kubbe_h=RD * 1.05, key=ACIK, duvar=(TAS, KOYU, ACIK, 'koyu'), payanda=False,
                    alem_olcek=1.0, n=32, kat=10, en=0.45, cerceve=None)
# the square Syrian minaret over the back range
NX_, NY_ = 0.34, MY1 - 0.08
NW = 0.11
nq = dikdortgen(NX_ - NW / 2, NX_ + NW / 2, NY_ - NW / 2, NY_ + NW / 2)
Z1, Z2 = ZR + 0.22, ZR + 0.42
for i in range(4):
    a, b = nq[i], nq[(i + 1) % 4]
    duvar_bant(y, a, b, ZR, Z1, TAS, n=2)
    kemer_nis(y, a, b, Z1, Z2 - Z1, en=0.56, ust=0.02, sivri=0.6, derin=0.012, key=TAS, yan_key=KOYU, alt_key=ACIK, arka_key='koyu',
              v0=0.03, k_say=8)
    ablak(y, a, b, Z1 - 0.04, Z1, AB, 0.01, on=0.0025)
    e = (b - a).normalized(); nn = V(e.y, -e.x); m = (a + b) / 2
    yarik(y, m + nn * 0.001, e, nn, -0.005, ZR + 0.08, 0.01, 0.06, 'koyu')
for zz in (ZR + 0.1, Z1 - 0.056):
    silme(y, nq, zz, 0.008, 0.006, ACIK, 'duz')
konsol_halka(y, nq, Z2 - 0.03, 0.03, 0.022, ACIK, 3)
nq2 = disa(nq, 0.022)
y.yuz_yon([V(p.x, p.y, Z2) for p in nq2], ACIK, Z)
parapet(y, nq2, Z2, 0.022, 0, 0.007, ACIK, ust_key=ACIK)
# the lantern: an open arcaded top storey and a ribbed cap
LW = 0.075
lq = dikdortgen(NX_ - LW / 2, NX_ + LW / 2, NY_ - LW / 2, NY_ + LW / 2)
for i in range(4):
    a, b = lq[i], lq[(i + 1) % 4]
    y.kemerli(a, b, Z2, 0.09, (TAS, KOYU, ACIK, 'koyu'), v0=0.01, en=0.6, ust=0.012, derin=0.012, k_say=8, sivri=0.6)
halka_kornis(y, (NX_, NY_), LW / 2 * 1.42, Z2 + 0.09, 0.008, 0.008, 4, ACIK, kat=math.pi / 4)
donel(y, (NX_, NY_), [(LW * 0.62, Z2 + 0.098), (LW * 0.58, Z2 + 0.12), (LW * 0.4, Z2 + 0.15), (LW * 0.15, Z2 + 0.17), (0.0, Z2 + 0.178)], ACIK, n=12)
alem(y, NX_, NY_, Z2 + 0.176, 0.7)

# ---------------- the fountain kiosk ----------------
y.bolum('Avlu ortası: kubbeli çeşme köşkü')
FC = (0.0, (CY0 + CY1) / 2 - 0.04)
RF = 0.1
fo = cokgen(FC, RF, 8, math.pi / 8)
y.prizma(FC, RF + 0.025, Z0, Z0 + 0.012, ACIK, n=8, kat=math.pi / 8)
for i in range(8):
    kemer_dizisi(y, fo[i], fo[(i + 1) % 8], 1, Z0 + 0.012, 0.13, 0.014, (TAS, KOYU, ACIK, KOYU), en=0.72, ust=0.022, sivri=0.6, acik=True, taban=False)
ZF = Z0 + 0.142
y.yuz_yon([V(p.x, p.y, ZF - 0.0005) for p in disa(fo, -0.014)], 'ahsap', -Z)
halka_kornis(y, FC, RF, ZF, 0.01, 0.01, 8, ACIK, kat=math.pi / 8)
for i in range(8):
    a, b = fo[i], fo[(i + 1) % 8]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    cini_bant(y, a, b, ZF - 0.016, 0.012, AB, n=4)
y.kubbe(FC, RF * 0.9, ZF + 0.01, RF * 0.85, ACIK, n=24, kat=7)
y.prizma(FC, RF * 0.92, ZF + 0.006, ZF + 0.012, ACIK, n=24, ust=False)
alem(y, FC[0], FC[1], ZF + 0.01 + RF * 0.85, 0.6)
y.prizma(FC, 0.055, Z0 + 0.012, Z0 + 0.04, 'mermer', n=8, kat=math.pi / 8)
y.prizma(FC, 0.048, Z0 + 0.04, Z0 + 0.0405, 'su', n=8, kat=math.pi / 8)
y.prizma(FC, 0.008, Z0 + 0.04, Z0 + 0.07, 'mermer', n=6)
# the four paths to it
for (xa, xb, ya, yb) in ((-0.04, 0.04, CY0, FC[1] - RF - 0.025), (-0.04, 0.04, FC[1] + RF + 0.025, MY0), (-CX, -RF - 0.025, FC[1] - 0.04, FC[1] + 0.04),
                         (RF + 0.025, CX, FC[1] - 0.04, FC[1] + 0.04)):
    y.yuz_yon([V(xa, ya, Z0 + 0.003), V(xb, ya, Z0 + 0.003), V(xb, yb, Z0 + 0.003), V(xa, yb, Z0 + 0.003)], KOYU, Z)

# ---------------- camels, goods, people ----------------
y.bolum('Kervan: develer, yükler, tüccarlar')
for (x, yy, a, c, cu, cok) in ((-0.42, -0.12, 0.3, 'ahsap_acik', 'boya_kirmizi', True), (-0.3, 0.3, -0.4, 'kum_koyu', 'turkuaz', True),
                                (0.36, -0.16, 2.6, 'ahsap_acik', 'lacivert', False), (0.42, 0.3, 3.5, 'kum_koyu', 'boya_kirmizi', True)):
    deve(y, x, yy, Z0 + 0.002, a, renk=c, cul=cu, yuk=True, cok=cok, olcek=1.2)
# unloaded goods under the arcades and in heaps
for (x, yy, key, a) in ((-0.55, -0.22, 'kumas', 0.0), (-0.55, -0.16, 'boya_kirmizi', 0.0), (-0.54, -0.19, 'kece', 0.3), (0.55, 0.05, 'kumas', 1.57),
                        (0.55, 0.12, 'boya_sari', 1.57), (0.52, 0.42, 'kece', 0.4), (-0.15, -0.25, 'boya_kirmizi', 0.2), (0.15, 0.42, 'kumas', -0.2)):
    denk(y, x, yy, Z0 + 0.002, key, a, w=0.055, d=0.04, h=0.032)
denk(y, -0.548, -0.19, Z0 + 0.034, 'turkuaz', 0.1, w=0.05, d=0.04, h=0.028)
denk(y, 0.55, 0.085, Z0 + 0.034, 'kece', 1.5, w=0.05, d=0.04, h=0.028)
for (x, yy) in ((-0.2, 0.42), (-0.17, 0.45), (-0.23, 0.46), (0.25, -0.24), (0.28, -0.21)):
    kup(y, x, yy, Z0 + 0.002, r=0.016, h=0.045)
for (x, yy, a, g) in ((-0.36, -0.03, 0.5, 'boya_kirmizi'), (0.3, -0.05, 2.0, 'kumas'), (0.1, 0.4, -1.0, 'lacivert'), (-0.08, -0.22, 0.3, 'boya_sari')):
    adam(y, x, yy, Z0 + 0.002, a, govde=g, boy=0.065)
# the caravan arriving along the street
for (x, yy, a, c, cu) in ((0.38, YO0 - 0.27, math.pi, 'ahsap_acik', 'boya_kirmizi'), (0.62, YO0 - 0.27, math.pi, 'kum_koyu', 'turkuaz'),
                          (0.86, YO0 - 0.27, math.pi, 'ahsap_acik', 'lacivert')):
    deve(y, x, yy, Z0 + 0.002, a, renk=c, cul=cu, yuk=True, olcek=1.2)
adam(y, 0.17, YO0 - 0.27, Z0 + 0.002, math.pi, govde='beyaz', boy=0.07)
for (x, yy, a, g) in ((-0.3, YO0 - 0.12, 0.0, 'kumas'), (-0.62, YO0 - 0.14, 2.0, 'boya_kirmizi'), (0.66, YO0 - 0.12, 1.0, 'boya_sari')):
    adam(y, x, yy, Z0 + 0.002, a, govde=g, boy=0.065)
for (x, yy) in ((-1.05, -0.92), (1.05, -0.92), (-1.05, 0.9), (1.05, 0.9)):
    agac(y, x, yy, Z0, boy=0.22, tur='palmiye', key='boya_yesil')
sancak(y, 0.12, GY + 0.1, gtop, boy=0.18, en=0.11, yuk=0.07, aci=-0.3)

calistir(y, 'lm_kervanhani')
