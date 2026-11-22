# Notre-Dame de Paris (lm_notredame): the west front facing -y with its two flat-topped towers, three portals with
# stepped archivolts, the Gallery of Kings, the great rose and the open grand gallery; the nave and choir with
# clerestory lancets, aisles, flying buttresses with pinnacles, the transept with its rose windows, the round apse
# (chevet) with radiating flyers, the lead roofs and the flèche with the copper apostles; the parvis and the Seine.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import *
from bina_ortak import calistir
import doku

# Notre-Dame's lead roofs are a darker, weathered grey (the stock lead reads pale blue next to the limestone)
doku.MALZEME['kursun'] = ('kursun', (0.43, 0.455, 0.50), {})
doku.MALZEME['kursun2'] = ('kursun', (0.395, 0.42, 0.465), {})

y = Yapi()
Z0 = 0.03
FY, TY = -0.95, -0.75          # west front line, the towers' back
NX, AX = 0.10, 0.27            # clerestory wall, aisle wall
KX0, KX1 = 0.20, 0.40          # transept (y range)
TRX = 0.355                    # transept end walls
AY = 0.75                      # apse centre
DUV = 'kirec'
ZW = Z0 + 0.47                 # clerestory wall top
ZC0 = Z0 + 0.31                # clerestory bottom (aisle roof top)
ZA = Z0 + 0.18                 # aisle wall top
ROOF_H = 0.17


def sirala(a, b, dis):
    """(a, b) ordered so the wall a->b faces dis"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized()
    return (a, b) if V(e.y, -e.x).dot(V(dis[0], dis[1])) > 0 else (b, a)


def pencere(a, b, z0, H, dis, **kw):
    a, b = sirala(a, b, dis)
    return gotik_pencere(y, a, b, z0, H, **kw)


def duvar(a, b, z0, z1, dis, key=DUV):
    a, b = sirala(a, b, dis)
    duz_duvar(y, a, b, z0, z1, key)


# ---------------------------------------------------------------- ground: parvis, garden, the Seine
y.bolum('Zemin: meydan ve Seine')
GX0, GX1, GY0, GY1 = -0.9, 0.55, -1.25, 1.25
RX1 = 0.84
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'granit', 'onarkasol')
duz_duvar(y, V(GX1, GY0), V(GX1, GY1), 0.008, Z0, 'granit')
y.yuz_yon([V(GX0, GY0, Z0), V(GX1, GY0, Z0), V(GX1, GY1, Z0), V(GX0, GY1, Z0)], 'zemin', Z)
silme(y, [V(GX0, GY1), V(GX0, GY0), V(GX1, GY0)], Z0 - 0.008, 0.008, 0.006, 'granit', 'duz', kapali=False)
# the river and the far bank
y.yuz_yon([V(GX1, GY0, 0.008), V(RX1, GY0, 0.008), V(RX1, GY1, 0.008), V(GX1, GY1, 0.008)], 'su', Z)
for p, q in ((V(GX1, GY0), V(RX1, GY0)), (V(RX1, GY1), V(GX1, GY1))):
    duz_duvar(y, p, q, 0, 0.008, 'granit')
kutu(y, V(RX1, GY0, 0), X, 0.06, GY1 - GY0, Z0, 'granit', 'onarkasagsol')
y.yuz_yon([V(RX1, GY0, Z0), V(RX1 + 0.06, GY0, Z0), V(RX1 + 0.06, GY1, Z0), V(RX1, GY1, Z0)], 'zemin', Z)
# quay parapets
for x, s in ((GX1, 1), (RX1, -1)):
    a, b = (V(x - 0.012, GY0), V(x - 0.012, GY1)) if s > 0 else (V(x + 0.012, GY1), V(x + 0.012, GY0))
    kutu3(y, V(x - s * 0.006, 0, Z0 + 0.009), Y, X, Z, GY1 - GY0, 0.012, 0.018, 'granit', ('+x', '-x', '+y', '-y', '+z'))
# a stone bridge over the Seine (Pont au Double)
for by_ in (-1.02,):
    kemer_dizisi(y, V(GX1, by_ - 0.035), V(RX1, by_ - 0.035), 3, 0.008, Z0 + 0.006 - 0.008, 0.07, renk=('granit', 'granit_koyu', 'granit', 'koyu'),
                 en=0.7, ust=0.012, acik=True, taban=False)
    for s in (-1, 1):
        kutu3(y, V((GX1 + RX1) / 2, by_ + s * 0.032, Z0 + 0.006 + 0.01), X, Y, Z, RX1 - GX1, 0.008, 0.02, 'granit')
# the parvis paving: strips of lighter stone tracing the old streets
for x0, x1, y0_, y1_ in ((-0.62, 0.42, -1.12, -1.1), (-0.62, -0.6, -1.12, -1.0), (0.4, 0.42, -1.12, -1.0), (-0.11, -0.09, -1.22, -1.12),
                         (0.09, 0.11, -1.22, -1.12)):
    y.yuz_yon([V(x0, y0_, Z0 + 0.002), V(x1, y0_, Z0 + 0.002), V(x1, y1_, Z0 + 0.002), V(x0, y1_, Z0 + 0.002)], 'tas_acik', Z)


def bahce(x0, x1, y0_, y1_, agaclar=(), cit=True):
    """a raised lawn with a box-hedge kerb and trees"""
    zz = Z0 + 0.004
    y.yuz_yon([V(x0, y0_, zz), V(x1, y0_, zz), V(x1, y1_, zz), V(x0, y1_, zz)], 'cimen', Z)
    k = dikdortgen(x0, x1, y0_, y1_)
    duvarlar(y, k, Z0, zz, 'boya_yesil')
    if cit:
        for i in range(4):
            a, b, L, e, nc = eksen(k[i], k[(i + 1) % 4])
            kutu3(y, a.lerp(b, 0.5) - nc * 0.005 + Z * (zz + 0.007), e, nc, Z, L, 0.01, 0.014, 'boya_yesil', ('+x', '-x', '+y', '-y', '+z'))
    for (ax_, ay_, b_, t_) in agaclar:
        agac(y, ax_, ay_, zz, boy=b_, tur=t_)


y.bolum('Bahçeler ve ağaçlar')
bahce(-0.86, -0.5, -0.62, 0.05, [(-0.68, yy, 0.2, 'yapraklı') for yy in (-0.52, -0.33, -0.14)])
bahce(-0.86, -0.5, 0.52, 1.2, [(-0.68, yy, 0.18, 'yapraklı') for yy in (0.64, 0.84, 1.04)])
bahce(-0.4, 0.4, 1.1, 1.22, [(xx, 1.16, 0.12, 'yapraklı') for xx in (-0.3, -0.1, 0.1, 0.3)], cit=True)
bahce(0.42, 0.52, -0.6, 0.9, [(0.47, yy, 0.17, 'yapraklı') for yy in (-0.45, -0.15, 0.15, 0.45, 0.75)], cit=False)
for xx, yy in ((-0.62, -1.18), (0.44, -1.18), (-0.78, -1.0), (0.47, -0.85)):
    agac(y, xx, yy, Z0, boy=0.16)
# lamp posts on the parvis
for xx in (-0.5, -0.25, 0.22, 0.5):
    y.prizma((xx, -1.08), 0.0035, Z0, Z0 + 0.075, 'demir', n=6)
    donel(y, (xx, -1.08), [(0.005, Z0 + 0.075), (0.009, Z0 + 0.082), (0.009, Z0 + 0.094), (0.0, Z0 + 0.102)], 'demir', n=6)

# the Fontaine de la Vierge in the square behind the apse: a Gothic pinnacle on a basin
y.bolum('Meryem çeşmesi')
FC = (0.0, 1.17)
donel(y, FC, [(0.0, Z0 + 0.012), (0.045, Z0 + 0.012), (0.045, Z0), (0.055, Z0), (0.055, Z0 + 0.02), (0.048, Z0 + 0.02), (0.048, Z0 + 0.012)], 'tas_acik', n=16)
y.yuz_yon([V(p.x, p.y, Z0 + 0.016) for p in cokgen(FC, 0.048, 16)], 'su', Z)
fiyal(y, FC[0], FC[1], 0.03, Z0 + 0.016, 0.06, 0.08, 'tas_acik')


# ---------------------------------------------------------------- the west front
y.bolum('Batı cephesi: portaller ve payandalar')
# portals: the central (Last Judgment) one wider and taller
for x0, x1, kat, ust in ((-0.272, -0.128, 3, 0.07), (-0.08, 0.08, 4, 0.035), (0.128, 0.272, 3, 0.07)):
    gotik_portal(y, V(x0, FY), V(x1, FY), Z0, 0.30, kat=kat, en=0.84, sivri=0.58, adim=0.011, ust=ust, duvar=DUV)
# the narrow strips of wall beside the portals (between the portal bays and the buttresses)
for x0, x1 in ((-0.28, -0.272), (-0.128, -0.12), (0.12, 0.128), (0.272, 0.28)):
    duz_duvar(y, V(x0, FY), V(x1, FY), Z0, Z0 + 0.30, DUV)
# the four buttresses
for bx in (-0.30, -0.10, 0.10, 0.30):
    dis_ = abs(bx) > 0.2
    yb = FY + (0.05 if dis_ else 0.0)
    # lower stage
    kutu3(y, V(bx, (FY - 0.036 + yb) / 2, Z0 + 0.15), X, Y, Z, 0.04, yb - FY + 0.036, 0.30, DUV,
          ('+x', '-x', '-y', '+y') if dis_ else ('+x', '-x', '-y'))
    # set-off: a sloped weathering
    q = [V(bx - 0.02, FY - 0.036, Z0 + 0.30), V(bx + 0.02, FY - 0.036, Z0 + 0.30), V(bx + 0.02, FY - 0.024, Z0 + 0.322), V(bx - 0.02, FY - 0.024, Z0 + 0.322)]
    y.yuz_yon(q, 'tas_acik', V(0, -1, 1))
    for s in (-1, 1):
        y.yuz_yon([V(bx + s * 0.02, FY - 0.036, Z0 + 0.30), V(bx + s * 0.02, FY - 0.024, Z0 + 0.30), V(bx + s * 0.02, FY - 0.024, Z0 + 0.322)], DUV, V(s, 0))
    # upper stage up to the grand gallery
    kutu3(y, V(bx, (FY - 0.024 + yb) / 2, Z0 + 0.44), X, Y, Z, 0.036, yb - FY + 0.024, 0.28, DUV,
          ('+x', '-x', '-y', '+y', '+z') if dis_ else ('+x', '-x', '-y', '+z'))
    if dis_:   # under the outer buttress's set-off the gap to the upper stage
        y.yuz_yon([V(bx - 0.02, FY - 0.024, Z0 + 0.3), V(bx + 0.02, FY - 0.024, Z0 + 0.3), V(bx + 0.02, yb, Z0 + 0.3), V(bx - 0.02, yb, Z0 + 0.3)], DUV, Z)
    # niches with statues on the buttresses' fronts (the four saints between the portals)
    kemer_nis(y, V(bx - 0.016, FY - 0.0361), V(bx + 0.016, FY - 0.0361), Z0 + 0.12, 0.13, en=0.72, ust=0.012, sivri=0.6, derin=0.008,
              key=DUV, yan_key='tas_koyu', arka_key='tas_koyu', k_say=8)
    heykel(y, bx, FY - 0.033, Z0 + 0.125, 1.75, 'tas_acik')

# string course over the portals
silme(y, [V(-0.32, FY), V(0.32, FY)], Z0 + 0.296, 0.012, 0.014, 'tas_acik', 'kaba', kapali=False)

y.bolum('Krallar Galerisi')
# the Gallery of Kings: a band of 28 niches with crowned kings, projecting a little
KB0, KB1 = Z0 + 0.308, Z0 + 0.36
GD = 0.012
y.yuz_yon([V(-0.28, FY - GD, KB1), V(0.28, FY - GD, KB1), V(0.28, FY, KB1), V(-0.28, FY, KB1)], 'tas_acik', Z)
N_KRAL = 28
for i in range(N_KRAL):
    xa, xb = -0.28 + 0.56 * i / N_KRAL, -0.28 + 0.56 * (i + 1) / N_KRAL
    L, x0, x1, hs, apex = kemer_nis(y, V(xa, FY - GD), V(xb, FY - GD), KB0, KB1 - KB0, en=0.78, ust=0.006, sivri=0.5, derin=0.009,
                                    key=DUV, yan_key='tas_koyu', arka_key='tas_koyu', k_say=8)
    m = (xa + xb) / 2
    heykel(y, m, FY - GD + 0.0035, KB0 + 0.002, 0.9, 'tas_acik')
    kutu3(y, V(m, FY - GD + 0.0035, KB0 + 0.0435), X, Y, Z, 0.009, 0.007, 0.004, 'altin', ('+x', '-x', '-y', '+y', '+z'))   # crown

y.bolum('Gül pencere katı')
# the Virgin's gallery: a ledge with an open balustrade before the rose
RZ0, RZ1 = KB1, Z0 + 0.58
silme(y, [V(-0.28, FY - GD), V(0.28, FY - GD)], RZ0 - 0.006, 0.012, 0.022, 'tas_acik', 'kaba', kapali=False)
for x0, x1 in ((-0.28, -0.12), (-0.08, 0.08), (0.12, 0.28)):
    acik_korkuluk(y, V(x0, FY - 0.026), V(x1, FY - 0.026), RZ0 + 0.006, 0.026, 'tas_acik', adim=0.012, t=0.008)
# the Virgin and Child between two angels, Adam and Eve on the tower bays
heykel(y, 0, FY - 0.022, RZ0 + 0.006, 1.5, 'tas_acik')
for s in (-1, 1):
    heykel(y, s * 0.05, FY - 0.022, RZ0 + 0.006, 1.2, 'tas_acik')
    heykel(y, s * 0.2, FY - 0.022, RZ0 + 0.006, 1.2, 'tas_acik')
# the rose
duz_duvar(y, V(-0.08, FY), V(0.08, FY), RZ0, RZ1, DUV)
gul_pencere(y, V(0, FY, Z0 + 0.47), X, -Y, 0.068, dis=1.17)
# spandrel roundels beside the rose
for s in (-1, 1):
    y.oculus(V(s * 0.068, FY, RZ1 - 0.02), X, -Y, 0.008, 'kobalt', 'tas_acik', f=0.003, k=10)
# the tower bays: two lancets under a relieving arch with a roundel
for x0, x1 in ((-0.28, -0.12), (0.12, 0.28)):
    L, u0, u1, hs, apex = kemer_nis(y, V(x0, FY), V(x1, FY), RZ0, RZ1 - RZ0 - 0.004, en=0.9, ust=0.012, sivri=0.55, derin=0.01, key=DUV,
                                    yan_key='tas_koyu', k_say=12, cerceve=(0.005, 'tas_acik'))
    pa, pb = L(u0, 0, 0.01), L(u1, 0, 0.01)
    y.yuz_yon([L(u0, 0, 0), L(u1, 0, 0), pb, pa], 'tas_acik', Z)
    pa, pb = V(pa.x, pa.y), V(pb.x, pb.y)
    w = (pb - pa).length
    for k in range(2):
        gotik_pencere(y, pa.lerp(pb, k / 2), pa.lerp(pb, (k + 1) / 2), RZ0, hs * 0.96, en=0.62, sivri=0.85, v0=0.02, ust=0.0, derin=0.02,
                      cam='kobalt', duvar=DUV)
    # the tympanum over the lancets (the niche back above them) with a roundel
    yol = kemer_yolu(u0, u1, hs, 0.55, 12)
    tim = [L(u0, hs * 0.96, 0.01)] + [L(u, v, 0.01) for u, v in yol] + [L(u1, hs * 0.96, 0.01)]
    y.yuz_yon(tim, DUV, -Y)
    y.oculus(L((u0 + u1) / 2, (hs * 0.96 + apex) / 2 - 0.004, 0.01), X, -Y, 0.022, 'kobalt', 'tas_acik', f=0.005, k=14)
silme(y, [V(-0.32, FY), V(0.32, FY)], RZ1 - 0.004, 0.01, 0.012, 'tas_acik', 'tac', kapali=False)

y.bolum('Büyük galeri')
# the grand gallery: an open screen of tall pointed arches on colonnettes across the whole front
GZ0, GZ1 = RZ1, Z0 + 0.68
GF = FY - 0.004
for x0, x1, n, acik in ((-0.30, -0.1, 6, False), (-0.1, 0.1, 5, True), (0.1, 0.30, 6, False)):
    kemer_dizisi(y, V(x0, GF), V(x1, GF), n, GZ0, GZ1 - GZ0, 0.02, renk=(DUV, 'tas_koyu', 'tas_acik', 'koyu'), en=0.74, ust=0.014,
                 sivri=0.7, acik=acik, taban=not acik)
    W = (x1 - x0) / n
    w = W * 0.74
    hs = GZ1 - GZ0 - 0.014 - 0.7 * w
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        if i in (0, n): continue
        y.prizma((xx, GF - 0.004), 0.0032, GZ0, GZ0 + hs, 'tas_acik', n=6, ust=False)
        y.prizma((xx, GF - 0.004), 0.0048, GZ0 + hs - 0.003, GZ0 + hs + 0.002, 'tas_acik', n=6)
# the sides of the open middle part (tower inner faces show behind) and its parapet
silme(y, [V(-0.30, GF), V(0.30, GF)], GZ1 - 0.004, 0.01, 0.012, 'tas_acik', 'tac', kapali=False)
acik_korkuluk(y, V(-0.1, GF + 0.006), V(0.1, GF + 0.006), GZ1 + 0.006, 0.026, 'tas_acik', adim=0.012, t=0.01)
# the terrace behind the gallery (between the towers)
y.yuz_yon([V(-NX, FY, GZ0), V(NX, FY, GZ0), V(NX, TY, GZ0), V(-NX, TY, GZ0)], 'kursun', Z)
duz_duvar(y, V(NX, TY + 0.003), V(-NX, TY + 0.003), Z0 + 0.4, GZ0, DUV)

# ---------------------------------------------------------------- the towers
y.bolum('Kuleler')
BZ0, BZ1 = GZ1, Z0 + 0.97
for sx in (-1, 1):
    x0, x1 = sorted((sx * NX, sx * 0.30))
    xo, xi = sx * 0.30, sx * NX
    # outer side (x = +-0.30) below the belfry: string courses continue, lancets at two levels
    ya, yb = FY + 0.05, TY
    duvar(V(xo, ya), V(xo, yb), Z0, Z0 + 0.06, (sx, 0))
    pencere(V(xo, ya), V(xo, yb), Z0 + 0.06, 0.22, (sx, 0), en=0.4, sivri=0.75, v0=0.02, cam='kobalt')
    duvar(V(xo, ya), V(xo, yb), Z0 + 0.28, RZ0 + 0.01, (sx, 0))
    pencere(V(xo, ya), V(xo, (ya + yb) / 2), RZ0 + 0.01, RZ1 - RZ0 - 0.01, (sx, 0), en=0.5, sivri=0.85, cam='kobalt')
    pencere(V(xo, (ya + yb) / 2), V(xo, yb), RZ0 + 0.01, RZ1 - RZ0 - 0.01, (sx, 0), en=0.5, sivri=0.85, cam='kobalt')
    duvar(V(xo, FY + 0.016), V(xo, yb), GZ0, GZ1, (sx, 0))
    for zz, pr in ((Z0 + 0.296, 'kaba'), (KB1 - 0.002, 'tac'), (RZ1 - 0.004, 'tac'), (GZ1 - 0.004, 'tac')):
        silme(y, [V(xo, ya) if zz < RZ1 else V(xo, FY + 0.016), V(xo, yb)] if sx > 0 else [V(xo, yb), V(xo, ya) if zz < RZ1 else V(xo, FY + 0.016)],
              zz, 0.01, 0.012, 'tas_acik', pr, kapali=False)
    # a buttress at the back corner of the outer side
    kutu3(y, V(xo + sx * 0.017, TY - 0.02, Z0 + 0.32), X, Y, Z, 0.034, 0.04, 0.64, DUV, ('+x', '-x', '+y', '-y', '+z'))
    # back face and the inner face above the terrace
    duvar(V(x0, TY), V(x1, TY), Z0, BZ0, (0, 1))
    duvar(V(xi, FY + 0.016), V(xi, TY), GZ0, BZ0, (-sx, 0))
    # the belfry: two tall louvred lancets on each face, corner buttresses
    k = dikdortgen(x0, x1, FY, TY)
    duvarlar(y, k, BZ0, BZ0 + 0.025, DUV)
    pencereli_duvar(y, k, BZ0 + 0.025, BZ1 - BZ0 - 0.025, [2, 2, 2, 2], renk=(DUV, 'tas_koyu', 'tas_acik', 'koyu'), v0=0.02, en=0.56, ust=0.02,
                    derin=0.018, k_say=8, sivri=0.85, cerceve=(0.005, 'tas_acik'))
    for i in range(4):
        a, b, L_, e, nc = eksen(k[i], k[(i + 1) % 4])
        for kk in range(2):
            # louvres in the openings
            u = L_ * (kk + 0.5) / 2
            for j in range(7):
                zz = BZ0 + 0.06 + j * 0.022
                c = a + e * u - nc * 0.011 + Z * zz
                kutu3(y, c, e, nc, Z, L_ / 2 * 0.5, 0.004, 0.006, 'ahsap_koyu', ('+y', '+z'))
            # the mullion
            c = a + e * u + Z * BZ0
            cubuk(y, c - nc * 0.008 + Z * 0.045, c - nc * 0.008 + Z * (BZ1 - BZ0 - 0.06), 0.006, 'tas_acik', 0.006)
    for p in k:   # angle buttresses at the belfry's corners
        for d_ in ((1 if p.x > (x0 + x1) / 2 else -1, 0), (0, 1 if p.y > (FY + TY) / 2 else -1)):
            dd = V(*d_)
            ee = V(-dd.y, dd.x)
            inward = V((x0 + x1) / 2 - p.x, (FY + TY) / 2 - p.y).normalized()
            along = ee if ee.dot(inward) > 0 else -ee
            c = V(p.x, p.y) + dd * 0.01 + along * 0.012
            kutu3(y, c + Z * ((BZ0 + BZ1 - 0.03) / 2), dd, along, Z, 0.02, 0.024, BZ1 - 0.03 - BZ0, DUV, ('+x', '-x', '+y', '-y', '+z'))
    # the crowning: cornice, flat lead top, open balustrade, corner pinnacles
    silme(y, k, BZ1 - 0.006, 0.012, 0.014, 'tas_acik', 'tac')
    zt = BZ1 + 0.006
    y.yuz_yon([V(p.x, p.y, zt) for p in disa(k, 0.0)], 'kursun', Z)
    kd = disa(k, 0.008)
    for i in range(4):
        acik_korkuluk(y, kd[i], kd[(i + 1) % 4], zt, 0.03, 'tas_acik', adim=0.014, t=0.01)
    for p in kd:
        fiyal(y, p.x, p.y, 0.022, zt, 0.04, 0.06, 'tas_acik')
    # the small stair turret on the north tower's top
    if sx < 0:
        kutu_merkez(y, (x1 - 0.05, TY - 0.05), 0.04, 0.04, 0.05, DUV, z0=zt)
        piramit_cati(y, (x1 - 0.05, TY - 0.05), 0.046, 0.046, zt + 0.05, 0.03, 'kursun')
        sancak(y, (x0 + x1) / 2 - 0.02, (FY + TY) / 2 - 0.02, zt, boy=0.2, en=0.11, yuk=0.065, aci=math.pi * 0.85)

# ---------------------------------------------------------------- nave, choir, aisles, flying buttresses
y.bolum('Nef, yan nefler ve uçan payandalar')
NB = 8
BAY_N = [(TY + (KX0 - TY) * j / NB, TY + (KX0 - TY) * (j + 1) / NB) for j in range(NB)]
CB = 3
BAY_C = [(KX1 + (AY - KX1) * j / CB, KX1 + (AY - KX1) * (j + 1) / CB) for j in range(CB)]


def payanda_ayagi(c, r_, t_, z_ust=Z0 + 0.40):
    """a buttress pier at c (2D), r_ the outward unit vector, t_ along: stepped, a pinnacle on top. Returns the inner
    point (2D) where a flyer starts"""
    c = V(c[0], c[1])
    kutu3(y, c + r_ * 0.0275 + Z * (Z0 + 0.08), r_, t_, Z, 0.055, 0.034, 0.16, DUV, ('+x', '+y', '-y'))
    q = [c + r_ * 0.055 - t_ * 0.017 + Z * (Z0 + 0.16), c + r_ * 0.055 + t_ * 0.017 + Z * (Z0 + 0.16),
         c + r_ * 0.045 + t_ * 0.017 + Z * (Z0 + 0.18), c + r_ * 0.045 - t_ * 0.017 + Z * (Z0 + 0.18)]
    y.yuz_yon(q, 'tas_acik', r_ + Z)
    for s in (-1, 1):
        y.yuz_yon([c + r_ * 0.045 + t_ * (s * 0.017) + Z * (Z0 + 0.16), c + r_ * 0.055 + t_ * (s * 0.017) + Z * (Z0 + 0.16),
                   c + r_ * 0.045 + t_ * (s * 0.017) + Z * (Z0 + 0.18)], DUV, t_ * s)
    kutu3(y, c + r_ * 0.0225 + Z * ((Z0 + 0.16 + z_ust) / 2), r_, t_, Z, 0.045, 0.032, z_ust - Z0 - 0.16, DUV, ('+x', '+y', '-y', '+z'))
    y.yuz_yon([c - t_ * 0.016 + Z * (ZA + 0.002), c + t_ * 0.016 + Z * (ZA + 0.002), c + t_ * 0.016 + Z * z_ust, c - t_ * 0.016 + Z * z_ust], DUV, -r_)
    fiyal(y, c.x + r_.x * 0.0225, c.y + r_.y * 0.0225, 0.026, z_ust, 0.03, 0.075, DUV, aci=math.atan2(r_.y, r_.x))
    return c + r_ * 0.012


def ucus(p_ic, w_pt):
    ucan_payanda(y, p_ic, w_pt, Z0 + 0.33, Z0 + 0.395, Z0 + 0.405, Z0 + 0.448, t=0.013, key=DUV)


for sx in (-1, 1):
    r_ = V(sx, 0)
    for bays in (BAY_N, BAY_C):
        for ya, yb in bays:
            # clerestory and aisle windows
            pencere(V(sx * NX, ya), V(sx * NX, yb), ZC0 - 0.01, ZW - ZC0 + 0.01, (sx, 0), en=0.56, sivri=0.75, v0=0.02, cam='kobalt')
            pencere(V(sx * AX, ya), V(sx * AX, yb), Z0, ZA - Z0, (sx, 0), en=0.46, sivri=0.7, v0=0.035, cam='kobalt', izli=False)
            # the aisle roof (lean-to)
            y.yuz_yon([V(sx * (AX + 0.02), ya, ZA + 0.004), V(sx * (AX + 0.02), yb, ZA + 0.004), V(sx * NX, yb, ZC0), V(sx * NX, ya, ZC0)], 'kursun', V(sx, 0, 1.5))
            y.yuz_yon([V(sx * (AX + 0.02), ya, ZA + 0.004), V(sx * (AX + 0.02), yb, ZA + 0.004), V(sx * (AX + 0.02), yb, ZA - 0.006),
                       V(sx * (AX + 0.02), ya, ZA - 0.006)], 'kursun', V(sx, 0))
            y.yuz_yon([V(sx * (AX + 0.02), ya, ZA - 0.006), V(sx * (AX + 0.02), yb, ZA - 0.006), V(sx * AX, yb, ZA), V(sx * AX, ya, ZA)], 'ahsap_koyu', -Z)
        # piers and flyers on the bay lines
        lines = [b[0] for b in bays] + [bays[-1][1]]
        for yy in lines:
            if abs(yy - TY) < 1e-6 or abs(yy - KX0) < 1e-6 or abs(yy - KX1) < 1e-6:
                continue
            pi_ = payanda_ayagi(V(sx * AX, yy), r_, V(0, 1))
            ucus(pi_, V(sx * NX, yy))
            kutu3(y, V(sx * (NX + 0.004), yy, (ZC0 + ZW) / 2), X, Y, Z, 0.008, 0.02, ZW - ZC0, DUV, ('+x', '-x', '+y', '-y'))
    # eaves cornices
    silme(y, [V(sx * NX, TY), V(sx * NX, AY)] if sx > 0 else [V(sx * NX, AY), V(sx * NX, TY)], ZW - 0.012, 0.012, 0.012, 'tas_acik', 'tac', kapali=False)
    silme(y, [V(sx * AX, TY), V(sx * AX, AY)] if sx > 0 else [V(sx * AX, AY), V(sx * AX, TY)], ZA - 0.01, 0.01, 0.008, 'tas_acik', 'duz', kapali=False)

# ---------------------------------------------------------------- transept
y.bolum('Transept ve gül pencereleri')
for sx in (-1, 1):
    xe = sx * TRX
    # side walls (y = 0.20 facing -y, y = 0.40 facing +y), the outer bit below and the clerestory part
    for yy, dy in ((KX0, -1), (KX1, 1)):
        duvar(V(sx * AX, yy), V(xe, yy), Z0, ZW, (0, dy))
        duvar(V(sx * NX, yy), V(sx * AX, yy), Z0, ZC0 - 0.01, (0, dy))
        duvar(V(sx * NX, yy), V(sx * (NX + 0.02), yy), ZC0 - 0.01, ZW, (0, dy))
        pencere(V(sx * (NX + 0.02), yy), V(sx * (AX - 0.0), yy), ZC0 - 0.01, ZW - ZC0 + 0.01, (0, dy), en=0.5, sivri=0.75, cam='kobalt')
        silme(y, [V(sx * NX, yy), V(xe, yy)] if sx * dy < 0 else [V(xe, yy), V(sx * NX, yy)], ZW - 0.012, 0.012, 0.012, 'tas_acik', 'tac', kapali=False)
    # the end front: portal, rose, gable
    ya, yb = KX0 + 0.018, KX1 - 0.018
    gotik_portal(y, *sirala(V(xe, ya), V(xe, yb), (sx, 0)), Z0, 0.22, kat=3, en=0.8, sivri=0.6, adim=0.01, ust=0.02, duvar=DUV)
    silme(y, [V(xe, ya), V(xe, yb)] if sx > 0 else [V(xe, yb), V(xe, ya)], Z0 + 0.216, 0.01, 0.012, 'tas_acik', 'kaba', kapali=False)
    duvar(V(xe, ya), V(xe, yb), Z0 + 0.22, ZW, (sx, 0))
    gul_pencere(y, V(xe, (KX0 + KX1) / 2, Z0 + 0.355), V(0, -sx), V(sx, 0), 0.058, dis=1.2)
    # corner turrets
    for yy in (KX0, KX1):
        c = V(xe - sx * 0.012, yy)
        kutu_merkez(y, (c.x, c.y), 0.036, 0.036, ZW + 0.03 - Z0, DUV, z0=Z0)
        silme(y, dikdortgen(c.x - 0.018, c.x + 0.018, c.y - 0.018, c.y + 0.018), ZW - 0.01, 0.01, 0.006, 'tas_acik', 'duz')
        fiyal(y, c.x, c.y, 0.03, ZW + 0.03, 0.05, 0.1, DUV)
    # gable ornament: a roundel and an apex pinnacle
    y.oculus(V(xe + sx * 0.0, (KX0 + KX1) / 2, ZW + 0.06), V(0, -sx), V(sx, 0), 0.022, 'kobalt', 'tas_acik', f=0.005, k=14)
    fiyal(y, xe + sx * 0.004, (KX0 + KX1) / 2, 0.02, ZW + ROOF_H - 0.02, 0.025, 0.05, 'tas_acik')

# ---------------------------------------------------------------- apse (chevet)
y.bolum('Apsis ve çevre nef')
NA = 5
ang = [math.pi * k / NA for k in range(NA + 1)]
ic_ = [V(NX * math.cos(t), AY + NX * math.sin(t)) for t in ang]
dis_k = [V(AX * math.cos(t), AY + AX * math.sin(t)) for t in ang]
dis_o = disa(dis_k, 0.02, kapali=False)
dis_o[0], dis_o[-1] = V(AX + 0.02, AY), V(-AX - 0.02, AY)   # (meet the choir aisles' roofs exactly: no crack)
for k in range(NA):
    gotik_pencere(y, ic_[k], ic_[k + 1], ZC0 - 0.01, ZW - ZC0 + 0.01, en=0.5, sivri=0.8, cam='kobalt')
    gotik_pencere(y, dis_k[k], dis_k[k + 1], Z0, ZA - Z0, en=0.42, sivri=0.7, v0=0.035, cam='kobalt', izli=False)
    # ambulatory roof
    a0, a1 = dis_o[k], dis_o[k + 1]
    y.yuz_yon([V(a0.x, a0.y, ZA + 0.004), V(a1.x, a1.y, ZA + 0.004), V(ic_[k + 1].x, ic_[k + 1].y, ZC0), V(ic_[k].x, ic_[k].y, ZC0)], 'kursun', Z)
    nn = V(a0.x + a1.x, a0.y + a1.y - 2 * AY)
    y.yuz_yon([V(a0.x, a0.y, ZA + 0.004), V(a1.x, a1.y, ZA + 0.004), V(a1.x, a1.y, ZA - 0.006), V(a0.x, a0.y, ZA - 0.006)], 'kursun', nn)
    y.yuz_yon([V(a0.x, a0.y, ZA - 0.006), V(a1.x, a1.y, ZA - 0.006), V(dis_k[k + 1].x, dis_k[k + 1].y, ZA), V(dis_k[k].x, dis_k[k].y, ZA)], 'ahsap_koyu', -Z)
silme(y, ic_, ZW - 0.012, 0.012, 0.012, 'tas_acik', 'tac', kapali=False)
silme(y, dis_k, ZA - 0.01, 0.01, 0.008, 'tas_acik', 'duz', kapali=False)
for k in range(1, NA):
    t = ang[k]
    r_ = V(math.cos(t), math.sin(t)); t_ = V(-r_.y, r_.x)
    pi_ = payanda_ayagi(V(0, AY) + r_ * (AX - 0.008), r_, t_)
    ucus(pi_, V(0, AY) + r_ * NX)
    c = V(0, AY) + r_ * (NX + 0.004)
    kutu3(y, c + Z * ((ZC0 + ZW) / 2), r_, t_, Z, 0.008, 0.02, ZW - ZC0, DUV, ('+x', '-x', '+y', '-y'))
# the corner piers where the choir meets the apse
for sx in (-1, 1):
    pi_ = payanda_ayagi(V(sx * AX, AY), V(sx, 0), V(0, 1))
    ucus(pi_, V(sx * NX, AY))

# ---------------------------------------------------------------- roofs
y.bolum('Kurşun çatılar')
cati_besik(y, -NX, NX, TY, AY, ZW, ROOF_H, 0.03, 'kursun', 'kursun2', ucluk_key=DUV, alt_key='ahsap_koyu', uc_sacak=0.0, ns=12, nr=6, mahya_en=0.012)
cati_besik(y, -TRX, TRX, KX0, KX1, ZW, ROOF_H, 0.03, 'kursun', 'kursun2', ucluk_key=DUV, alt_key='ahsap_koyu', uc_sacak=0.012, ns=8, nr=6, mahya_en=0.012)
# standing seams on the lead slopes
def dikis(a, b):
    a, b = Vector(a), Vector(b)
    t = (b - a).normalized(); u = Z.cross(t).normalized(); n = t.cross(u).normalized()
    if n.z < 0: n = -n
    cubuk(y, a + n * 0.0016, b + n * 0.0016, 0.0035, 'kursun2', 0.0025)


EB = NX + 0.03
for sx in (-1, 1):
    k = 0
    yy = TY + 0.03
    while yy < AY - 0.01:
        if not (KX0 - 0.04 < yy < KX1 + 0.04):
            dikis(V(sx * EB, yy, ZW), V(0, yy, ZW + ROOF_H - 0.004))
        yy += 0.042
    for xx0 in (0.15, 0.19, 0.23, 0.27, 0.31, 0.35):
        for sy in (-1, 1):
            yc = (KX0 + KX1) / 2
            dikis(V(sx * xx0, yc + sy * EB, ZW), V(sx * xx0, yc, ZW + ROOF_H - 0.004))
# the apse's half cone
NK = 10
RR = NX + 0.03
tepe = V(0, AY, ZW + ROOF_H)
halka_ = [V(RR * math.cos(math.pi * k / NK), AY + RR * math.sin(math.pi * k / NK), ZW) for k in range(NK + 1)]
for k in range(NK):
    m = (halka_[k] + halka_[k + 1]) / 2
    y.yuz_yon([halka_[k], halka_[k + 1], tepe], 'kursun2' if k % 2 else 'kursun', V(m.x, m.y - AY, 0.5))
    y.yuz_yon([halka_[k], halka_[k + 1], halka_[k + 1] - Z * 0.012, halka_[k] - Z * 0.012], 'ahsap_koyu', V(m.x, m.y - AY, 0))
    w0 = V(NX * math.cos(math.pi * k / NK), AY + NX * math.sin(math.pi * k / NK), ZW)
    w1 = V(NX * math.cos(math.pi * (k + 1) / NK), AY + NX * math.sin(math.pi * (k + 1) / NK), ZW)
    y.yuz_yon([halka_[k] - Z * 0.012, halka_[k + 1] - Z * 0.012, w1, w0], 'ahsap_koyu', -Z)
# the apse's hip ridges
for k in (0, NK // 2, NK):
    cubuk(y, halka_[k] + Z * 0.004, tepe + Z * 0.004, 0.01, 'kursun2')

# ---------------------------------------------------------------- the flèche
y.bolum('Fleş (sivri kule) ve havariler')
FC = V(0, (KX0 + KX1) / 2)
zr = ZW + ROOF_H
# octagonal base on the crossing
fz0 = zr - 0.075
k8 = cokgen(FC, 0.048, 8, math.pi / 8)
for i in range(8):
    y.kemerli(k8[i], k8[(i + 1) % 8], fz0, 0.135, ('kursun', 'ahsap_koyu', 'kursun2', 'koyu'), v0=0.075, en=0.5, ust=0.012, derin=0.008, k_say=6, sivri=0.8)
halka_kornis(y, FC, 0.048, fz0 + 0.13, 0.008, 0.008, 8, 'kursun2', kat=math.pi / 8)
y.yuz_yon([V(p.x, p.y, fz0 + 0.138) for p in k8], 'kursun', Z)
for i in range(8):   # gablets and pinnacles round the base
    a, b, L_, e, nc = eksen(k8[i], k8[(i + 1) % 8])
    m = a.lerp(b, 0.5)
    levha(y, [V(a.x, a.y) + nc * 0.01 + Z * (fz0 + 0.137), V(b.x, b.y) + nc * 0.01 + Z * (fz0 + 0.137), m + nc * 0.01 + Z * (fz0 + 0.175)], 'kursun', nc, 0.0015)
    fiyal(y, k8[i].x, k8[i].y, 0.012, fz0 + 0.085, 0.06, 0.05, 'kursun', gablet=False)
# second stage
fz1 = fz0 + 0.138
k8b = cokgen(FC, 0.036, 8, math.pi / 8)
for i in range(8):
    y.kemerli(k8b[i], k8b[(i + 1) % 8], fz1, 0.08, ('kursun', 'ahsap_koyu', 'kursun2', 'koyu'), v0=0.012, en=0.5, ust=0.01, derin=0.006, k_say=6, sivri=0.8)
halka_kornis(y, FC, 0.036, fz1 + 0.075, 0.008, 0.008, 8, 'kursun2', kat=math.pi / 8)
# the spire with crocket rings
fz2 = fz1 + 0.083
TIP = Z0 + 1.37
donel(y, FC, [(0.038, fz2), (0.03, fz2 + 0.03), (0.0, TIP)], 'kursun', n=8, kat=math.pi / 8)
for f in (0.18, 0.36, 0.54, 0.72):
    zz = fz2 + 0.03 + (TIP - fz2 - 0.03) * f
    rr = 0.03 * (1 - f) + 0.0025
    halka_kornis(y, FC, rr, zz, 0.006, 0.004, 8, 'kursun2', kat=math.pi / 8)
hac_z = TIP
y.prizma((FC.x, FC.y), 0.0025, hac_z - 0.01, hac_z + 0.05, 'altin', n=4)
cubuk(y, V(FC.x - 0.016, FC.y, hac_z + 0.03), V(FC.x + 0.016, FC.y, hac_z + 0.03), 0.004, 'altin')
kure(y, (FC.x, FC.y, hac_z + 0.058), 0.006, 'altin', n=6, kat=3)   # the rooster
# the twelve apostles in green copper, three on each ridge arm, stepping down from the flèche
for d_ in (V(1, 0), V(-1, 0), V(0, 1), V(0, -1)):
    for j in range(3):
        p = FC + d_ * (0.065 + j * 0.026)
        zz = zr - 0.006 - j * 0.012
        kutu_merkez(y, (p.x, p.y), 0.014, 0.014, 0.008 + j * 0.012, 'kursun2', z0=zz - j * 0.012 + 0.0)
        heykel(y, p.x, p.y, zz + 0.008, 0.62, 'bakir', math.atan2(d_.y, d_.x) - math.pi / 2)

# ---------------------------------------------------------------- the Charlemagne statue on the parvis
y.bolum('Charlemagne heykeli')
CX_, CY_ = 0.38, -1.14
atli_heykel(y, CX_, CY_, Z0, math.pi, 1.0, 'bronz', kaide='granit')

calistir(y, 'lm_notredame')
