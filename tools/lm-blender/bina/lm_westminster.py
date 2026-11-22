# Westminster Manastiri (lm_westminster): Westminster Abbey. The west front (facing -y) between Hawksmoor's two square
# towers (belfries with clock pediments, pierced parapets and tall crocketed pinnacles) with the great west window;
# the very tall nave with clerestory lancets, aisles and double flying buttresses; the north transept front with its
# rose and three portals between octagonal turrets; the low crossing lantern; the choir and apse with radiating
# flyers; Henry VII's Lady Chapel at the east end (polygonal turret-buttresses with lead cupolas, great bay windows,
# pierced parapets); the cloister with its garth and the octagonal chapter house to the south; lead roofs with seams.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import *
from frank_ortak import cayir_renk
from bina_ortak import calistir
import doku

y = Yapi()
Z0 = 0.03
doku.KOSE_RENK['cimen'] = cayir_renk(Z0)
FY, TY = -0.96, -0.8            # west front line, the towers' back
NX, AX = 0.09, 0.2              # clerestory wall, aisle wall
KX0, KX1 = 0.1, 0.34            # transept (y range)
TRX = 0.5                       # transept end walls
AY = 0.6                        # apse centre
DUV, DR = 'kirec', 'tas_acik'
CAM = 'kobalt'
ZW = Z0 + 0.52                  # clerestory wall top
ZC0 = Z0 + 0.3                  # clerestory bottom
ZA = Z0 + 0.19                  # aisle wall top
ROOF_H = 0.15


def sirala(a, b, dis):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized()
    return (a, b) if V(e.y, -e.x).dot(V(dis[0], dis[1])) > 0 else (b, a)


def pencere(a, b, z0, H, dis, **kw):
    a, b = sirala(a, b, dis)
    kw.setdefault('cam', CAM); kw.setdefault('duvar', DUV); kw.setdefault('iz', DR)
    return gotik_pencere(y, a, b, z0, H, **kw)


def duvar(a, b, z0, z1, dis, key=DUV):
    a, b = sirala(a, b, dis)
    duz_duvar(y, a, b, z0, z1, key)


def payanda_ayagi(c, r_, t_, z_ust=Z0 + 0.42, d=0.06):
    """a buttress pier at c (2D) on the aisle wall, r_ outward, t_ along: two stages, a pinnacle; returns the point
    where its flyers start"""
    c = V(c[0], c[1])
    kutu3(y, c + r_ * (d / 2) + Z * (Z0 + 0.09), r_, t_, Z, d, 0.034, 0.18, DUV, ('+x', '+y', '-y'))
    q = [c + r_ * d - t_ * 0.017 + Z * (Z0 + 0.18), c + r_ * d + t_ * 0.017 + Z * (Z0 + 0.18),
         c + r_ * (d - 0.012) + t_ * 0.017 + Z * (Z0 + 0.2), c + r_ * (d - 0.012) - t_ * 0.017 + Z * (Z0 + 0.2)]
    y.yuz_yon(q, DR, r_ + Z)
    for s in (-1, 1):
        y.yuz_yon([c + r_ * (d - 0.012) + t_ * (s * 0.017) + Z * (Z0 + 0.18), c + r_ * d + t_ * (s * 0.017) + Z * (Z0 + 0.18),
                   c + r_ * (d - 0.012) + t_ * (s * 0.017) + Z * (Z0 + 0.2)], DUV, t_ * s)
    d2 = d - 0.012
    kutu3(y, c + r_ * (d2 / 2) + Z * ((Z0 + 0.18 + z_ust) / 2), r_, t_, Z, d2, 0.032, z_ust - Z0 - 0.18, DUV, ('+x', '+y', '-y', '+z'))
    y.yuz_yon([c - t_ * 0.016 + Z * (ZA + 0.002), c + t_ * 0.016 + Z * (ZA + 0.002), c + t_ * 0.016 + Z * z_ust, c - t_ * 0.016 + Z * z_ust], DUV, -r_)
    fiyal(y, c.x + r_.x * (d2 / 2), c.y + r_.y * (d2 / 2), 0.026, z_ust, 0.035, 0.085, DUV, tip_key=DR, gablet=False, aci=math.atan2(r_.y, r_.x))
    return c + r_ * 0.012


def ucus(p_ic, w_pt):
    """Westminster's double flyers: a lower and an upper arm"""
    ucan_payanda(y, p_ic, w_pt, Z0 + 0.3, Z0 + 0.37, Z0 + 0.36, Z0 + 0.4, t=0.012, key=DUV, n=4)
    ucan_payanda(y, p_ic, w_pt, Z0 + 0.39, Z0 + 0.415, Z0 + 0.46, Z0 + 0.5, t=0.012, key=DUV, n=3)


# ---------------------------------------------------------------- ground: the parvis, Dean's Yard green, paths
y.bolum('Zemin: meydan ve çimen')
GX0, GX1, GY0, GY1 = -0.78, 0.9, -1.12, 1.16
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'granit', 'onarkasagsol')
y.yuz_yon([V(GX0, GY0, Z0), V(GX1, GY0, Z0), V(GX1, -0.78, Z0), V(GX0, -0.78, Z0)], 'zemin', Z)
y.yuz_yon([V(GX0, -0.78, Z0), V(GX1, -0.78, Z0), V(GX1, GY1, Z0), V(GX0, GY1, Z0)], 'cimen', Z)
silme(y, dikdortgen(GX0, GX1, GY0, GY1), Z0 - 0.008, 0.008, 0.006, 'granit', 'duz')
# paved paths round the church (a hair above the lawn)
for (x0, x1, y0_, y1_) in ((-0.32, -0.24, -0.78, 0.98), (-0.62, -0.24, 0.18, 0.3), (0.24, 0.3, -0.78, -0.62)):
    y.yuz_yon([V(x0, y0_, Z0 + 0.002), V(x1, y0_, Z0 + 0.002), V(x1, y1_, Z0 + 0.002), V(x0, y1_, Z0 + 0.002)], 'zemin', Z)
for (x, yy, b) in ((-0.62, -0.6, 0.2), (-0.62, -0.3, 0.19), (-0.62, 0.0, 0.2), (-0.6, 0.55, 0.2), (-0.5, 0.85, 0.18), (0.5, 0.9, 0.19), (0.75, 0.7, 0.18),
                   (0.8, -0.95, 0.18)):
    agac(y, x, yy, Z0, boy=b, key='boya_yesil' if int(abs(x * 10 + yy * 10)) % 2 else 'zeytin')
for xx in (-0.5, -0.3, 0.3, 0.5):   # lamp posts on the parvis
    y.prizma((xx, -1.05), 0.0035, Z0, Z0 + 0.075, 'demir', n=6)
    donel(y, (xx, -1.05), [(0.005, Z0 + 0.075), (0.009, Z0 + 0.082), (0.009, Z0 + 0.094), (0.0, Z0 + 0.102)], 'demir', n=6)

# ---------------------------------------------------------------- the west front
y.bolum('Batı cephesi: portal ve büyük pencere')
WZ = ZW
gotik_portal(y, V(-NX, FY), V(NX, FY), Z0, 0.22, kat=4, en=0.8, sivri=0.6, adim=0.011, ust=0.025, duvar=DUV)
# the great west window over it, in a deep moulded frame
duvar(V(-NX, FY), V(NX, FY), Z0 + 0.22, Z0 + 0.25, (0, -1))
silme(y, [V(-NX, FY), V(NX, FY)], Z0 + 0.22, 0.012, 0.012, DR, 'kaba', kapali=False)
W, e, nc, L, x0, x1, hs = pencere(V(-NX, FY), V(NX, FY), Z0 + 0.25, WZ - Z0 - 0.25, (0, -1), en=0.78, sivri=0.6, v0=0.01, ust=0.03, derin=0.024,
                                  cerceve=(0.008, [DR, DUV]))
# extra tracery: two more mullions and a transom of small arches
for u in (0.25, 0.75):
    cubuk(y, L(x0 + (x1 - x0) * u, 0.01, 0.01), L(x0 + (x1 - x0) * u, hs * 0.9, 0.01), 0.005, DR, 0.006)
cubuk(y, L(x0, hs * 0.45, 0.01), L(x1, hs * 0.45, 0.01), 0.005, DR, 0.006)
# the gable over the west window, with a statue niche and a cross
gab = [V(-NX - 0.03, FY, WZ), V(NX + 0.03, FY, WZ), V(0, FY, WZ + ROOF_H)]
for p, q in ((gab[0], gab[2]), (gab[2], gab[1])):
    cubuk(y, p + V(0, -0.004, 0.006), q + V(0, -0.004, 0.006), 0.012, DR, 0.014)
kemer_nis(y, V(-0.02, FY - 0.002), V(0.02, FY - 0.002), WZ + 0.01, 0.055, en=0.7, ust=0.006, sivri=0.6, derin=0.008, key=DUV, yan_key='tas_koyu', arka_key='tas_koyu')
heykel(y, 0, FY - 0.004, WZ + 0.012, 0.9, DR)
fiyal(y, 0, FY - 0.006, 0.018, WZ + ROOF_H - 0.01, 0.02, 0.05, DR)
silme(y, [V(-NX, FY), V(NX, FY)], WZ - 0.008, 0.01, 0.01, DR, 'tac', kapali=False)

y.bolum('Batı kuleleri (Hawksmoor)')
BZ0, BZ1 = Z0 + 0.7, Z0 + 0.94
for sx in (-1, 1):
    x0, x1 = sorted((sx * NX, sx * 0.27))
    k = dikdortgen(x0, x1, FY, TY)
    xo = sx * 0.27
    cx = (x0 + x1) / 2
    # lower stages: a lancet in each of three registers on the front and outer side, niches with statues
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        a2, b2, L_, e2, n2 = eksen(a, b)
        dis = (n2.x, n2.y)
        inner = abs(n2.x + sx) < 0.1 and abs(n2.y) < 0.1   # the face towards the nave
        if inner:
            duvar(a, b, Z0, BZ0, dis)
            continue
        if i == 0:
            kapi(y, a, b, Z0, 0.38, 0.15, (DUV, 'tas_koyu', DR, 'ahsap_koyu'), sivri=0.6, derin=0.016, cerceve=(0.006, DR))
            duvar(a, b, Z0 + 0.15, Z0 + 0.2, dis)
        else:
            duvar(a, b, Z0, Z0 + 0.04, dis)
            duvar(a, b, Z0 + 0.17, Z0 + 0.2, dis)
            for j in range(2):
                p, q = a2.lerp(b2, j / 2), a2.lerp(b2, (j + 1) / 2)
                kemer_nis(y, p, q, Z0 + 0.04, 0.13, en=0.5, ust=0.01, sivri=0.6, derin=0.01, key=DUV, yan_key='tas_koyu', arka_key='tas_koyu', k_say=8)
                m = p.lerp(q, 0.5)
                heykel(y, m.x - n2.x * 0.004, m.y - n2.y * 0.004, Z0 + 0.042, 1.3, DR, n=5)
        pencere(a, b, Z0 + 0.2, 0.22, dis, en=0.42, sivri=0.65, v0=0.02, ust=0.02, derin=0.016)
        duvar(a, b, Z0 + 0.42, Z0 + 0.46, dis)
        if i == 0 or (i == 3 and sx < 0) or (i == 1 and sx > 0):
            duvar(a, b, Z0 + 0.46, BZ0, dis)
        else:
            pencere(a, b, Z0 + 0.46, BZ0 - Z0 - 0.46, dis, en=0.36, sivri=0.65, v0=0.02, ust=0.02, derin=0.014, izli=False)
    for zz in (Z0 + 0.2, Z0 + 0.42, BZ0 - 0.006):
        silme(y, k, zz, 0.01, 0.01, DR, 'duz')
    # the clock stage's pediment on the front and outer side (Hawksmoor): a clock face in a triangular pediment
    for i in (0, 3 if sx < 0 else 1):
        a, b = k[i], k[(i + 1) % 4]
        a2, b2, L_, e2, n2 = eksen(a, b)
        m = a2.lerp(b2, 0.5)
        o = m + n2 * 0.002 + Z * (Z0 + 0.6)
        y.oculus(o, e2, n2, 0.034, 'koyu', DR, f=0.006, k=18)
        y.oculus(o + n2 * 0.0007, e2, n2, 0.028, 'altin', 'altin', f=0.002, k=18)
        for (ang, ln) in ((math.pi / 2, 0.022), (math.pi * 0.1, 0.016)):
            d = e2 * math.cos(ang) + Z * math.sin(ang)
            cubuk(y, o + n2 * 0.0045, o + n2 * 0.0045 + d * ln, 0.003, 'koyu', 0.0012)
        P_ = [a2 + n2 * 0.006 + Z * (BZ0 - 0.035), b2 + n2 * 0.006 + Z * (BZ0 - 0.035), m + n2 * 0.006 + Z * (BZ0 + 0.03)]
        levha(y, P_, DR, n2, 0.006)
    # the belfry: two tall louvred lancets on each face, octagonal corner buttress-turrets
    pencereli_duvar(y, k, BZ0, BZ1 - BZ0, [2, 2, 2, 2], renk=(DUV, 'tas_koyu', DR, 'koyu'), v0=0.02, en=0.56, ust=0.02,
                    derin=0.018, k_say=6, sivri=0.8, cerceve=(0.005, DR))
    for i in range(4):
        a2, b2, L_, e2, n2 = eksen(k[i], k[(i + 1) % 4])
        for kk in range(2):
            u = L_ * (kk + 0.5) / 2
            for j in range(6):
                zz = BZ0 + 0.06 + j * 0.026
                kutu3(y, a2 + e2 * u - n2 * 0.011 + Z * zz, e2, n2, Z, L_ / 2 * 0.5, 0.004, 0.006, 'ahsap_koyu', ('+y', '+z'))
    for p in k:
        y.prizma((p.x, p.y), 0.02, BZ0 - 0.2, BZ1 + 0.02, DUV, n=8, ust=False, kat=math.pi / 8)
        for zz in (BZ0 - 0.006, BZ1 - 0.012):
            halka_kornis(y, p, 0.02, zz, 0.012, 0.006, 8, DR, kat=math.pi / 8)
        y.yuz_yon([V(q.x, q.y, BZ1 + 0.02) for q in cokgen(p, 0.02, 8, math.pi / 8)], DR, Z)
        # the tall crocketed pinnacle
        donel(y, p, [(0.016, BZ1 + 0.02), (0.016, BZ1 + 0.05), (0.0, BZ1 + 0.2)], DR, n=8, kat=math.pi / 8)
        for f in ():
            halka_kornis(y, p, 0.016 * (1 - f) - 0.001, BZ1 + 0.05 + 0.15 * f, 0.006, 0.004, 8, DR, kat=math.pi / 8)
        kure(y, (p.x, p.y, BZ1 + 0.205), 0.006, 'altin', n=6, kat=3)
    # the crowning: cornice, pierced parapet, a small pinnacle in each side's middle
    silme(y, k, BZ1 - 0.006, 0.014, 0.012, DR, 'tac')
    zt = BZ1 + 0.008
    y.yuz_yon([V(p.x, p.y, zt) for p in k], 'kursun', Z)
    kd = disa(k, 0.008)
    for i in range(4):
        a_, b_ = kd[i], kd[(i + 1) % 4]
        L2 = (b_ - a_).length
        acik_korkuluk(y, a_ + (b_ - a_) * (0.026 / L2), b_ - (b_ - a_) * (0.026 / L2), zt, 0.034, DR, adim=0.022, t=0.01)
        m = a_.lerp(b_, 0.5)
        fiyal(y, m.x, m.y, 0.016, zt, 0.04, 0.07, DR, gablet=False)
    if sx < 0:
        y.bolum('Sancak')
        sancak(y, cx, (FY + TY) / 2, zt, boy=0.24, en=0.14, yuk=0.085, aci=math.pi * 0.85)

# ---------------------------------------------------------------- nave, aisles, flying buttresses
y.bolum('Nef, yan nefler ve çift uçan payandalar')
NB = 7
BAY_N = [(TY + (KX0 - TY) * j / NB, TY + (KX0 - TY) * (j + 1) / NB) for j in range(NB)]
CB = 2
BAY_C = [(KX1 + (AY - KX1) * j / CB, KX1 + (AY - KX1) * (j + 1) / CB) for j in range(CB)]
for sx in (-1, 1):
    r_ = V(sx, 0)
    for bays in (BAY_N, BAY_C):
        for ya, yb in bays:
            pencere(V(sx * NX, ya), V(sx * NX, yb), ZC0 - 0.01, ZW - ZC0 + 0.01, (sx, 0), en=0.6, sivri=0.75, v0=0.02)
            # aisle windows (on the south side the cloister's north walk covers them)
            if sx > 0 and bays is BAY_N and ya > -0.62 - 1e-6:   # hidden behind the cloister's north walk: a plain wall
                duvar(V(sx * AX, ya), V(sx * AX, yb), Z0, ZA, (sx, 0))
            else:
                pencere(V(sx * AX, ya), V(sx * AX, yb), Z0, ZA - Z0, (sx, 0), en=0.5, sivri=0.7, v0=0.035, izli=False)
            # the aisle's lean-to roof
            y.yuz_yon([V(sx * (AX + 0.02), ya, ZA + 0.004), V(sx * (AX + 0.02), yb, ZA + 0.004), V(sx * NX, yb, ZC0), V(sx * NX, ya, ZC0)], 'kursun', V(sx, 0, 1.5))
            y.yuz_yon([V(sx * (AX + 0.02), ya, ZA + 0.004), V(sx * (AX + 0.02), yb, ZA + 0.004), V(sx * (AX + 0.02), yb, ZA - 0.006),
                       V(sx * (AX + 0.02), ya, ZA - 0.006)], 'kursun', V(sx, 0))
            y.yuz_yon([V(sx * (AX + 0.02), ya, ZA - 0.006), V(sx * (AX + 0.02), yb, ZA - 0.006), V(sx * AX, yb, ZA), V(sx * AX, ya, ZA)], 'ahsap_koyu', -Z)
        lines = [b[0] for b in bays] + [bays[-1][1]]
        for yy in lines:
            if abs(yy - TY) < 1e-6 or abs(yy - KX0) < 1e-6 or abs(yy - KX1) < 1e-6:
                continue
            pi_ = payanda_ayagi(V(sx * AX, yy), r_, V(0, 1))
            ucus(pi_, V(sx * NX, yy))
            kutu3(y, V(sx * (NX + 0.004), yy, (ZC0 + ZW) / 2), X, Y, Z, 0.008, 0.02, ZW - ZC0, DUV, ('+x', '-x', '+y', '-y'))
    silme(y, [V(sx * NX, TY), V(sx * NX, AY)] if sx > 0 else [V(sx * NX, AY), V(sx * NX, TY)], ZW - 0.012, 0.012, 0.012, DR, 'tac', kapali=False)
    silme(y, [V(sx * AX, TY), V(sx * AX, AY)] if sx > 0 else [V(sx * AX, AY), V(sx * AX, TY)], ZA - 0.01, 0.01, 0.008, DR, 'duz', kapali=False)
    # a pierced parapet along the clerestory's top
    a_, b_ = (V(sx * (NX + 0.006), TY), V(sx * (NX + 0.006), KX0)) if sx > 0 else (V(sx * (NX + 0.006), KX0), V(sx * (NX + 0.006), TY))
    acik_korkuluk(y, a_, b_, ZW, 0.022, DR, adim=0.026, t=0.008)
    a_, b_ = (V(sx * (NX + 0.006), KX1), V(sx * (NX + 0.006), AY)) if sx > 0 else (V(sx * (NX + 0.006), AY), V(sx * (NX + 0.006), KX1))
    acik_korkuluk(y, a_, b_, ZW, 0.022, DR, adim=0.026, t=0.008)

# ---------------------------------------------------------------- transepts
y.bolum('Transeptler ve gül pencereleri')
for sx in (-1, 1):
    xe = sx * TRX
    for yy, dy in ((KX0, -1), (KX1, 1)):
        duvar(V(sx * AX, yy), V(xe, yy), Z0, ZA, (0, dy))
        duvar(V(sx * NX, yy), V(sx * AX, yy), Z0, ZC0 - 0.01, (0, dy))
        duvar(V(sx * AX, yy), V(xe, yy), ZA, ZC0 - 0.01, (0, dy))
        for j in range(2):
            p0 = sx * (NX + (TRX - NX) * j / 2)
            p1 = sx * (NX + (TRX - NX) * (j + 1) / 2)
            pencere(V(p0, yy), V(p1, yy), ZC0 - 0.01, ZW - ZC0 + 0.01, (0, dy), en=0.42, sivri=0.75)
        silme(y, [V(sx * NX, yy), V(xe, yy)] if sx * dy < 0 else [V(xe, yy), V(sx * NX, yy)], ZW - 0.012, 0.012, 0.012, DR, 'tac', kapali=False)
    # the end front: three portals, a gallery of lancets, the rose, the gable
    ya, yb = KX0 + 0.022, KX1 - 0.022
    pts = [V(xe, ya + (yb - ya) * j / 3) for j in range(4)]
    for j in (range(3) if sx < 0 else ()):
        gotik_portal(y, *sirala(pts[j], pts[j + 1], (sx, 0)), Z0, 0.18 if j == 1 else 0.15, kat=3 if j == 1 else 2, en=0.8, sivri=0.6, adim=0.009,
                     ust=0.02 if j == 1 else 0.05, duvar=DUV)
    if sx < 0:   # the strip over the portals up to the lancet gallery
        for j in range(3):
            duvar(pts[j], pts[j + 1], Z0 + (0.18 if j == 1 else 0.15), Z0 + 0.19, (sx, 0))
    if sx > 0:   # the south end, hidden behind the chapter house: a plain wall below
        duvar(V(xe, ya), V(xe, yb), Z0, Z0 + 0.19, (sx, 0))
    silme(y, [V(xe, ya), V(xe, yb)] if sx > 0 else [V(xe, yb), V(xe, ya)], Z0 + 0.18, 0.01, 0.012, DR, 'kaba', kapali=False)
    for j in range(4):
        p, q = V(xe, ya + (yb - ya) * j / 4), V(xe, ya + (yb - ya) * (j + 1) / 4)
        pencere(p, q, Z0 + 0.19, 0.1, (sx, 0), en=0.55, sivri=0.7, v0=0.01, ust=0.01, derin=0.012, izli=False)
    duvar(V(xe, ya), V(xe, yb), Z0 + 0.29, ZW, (sx, 0))
    gul_pencere(y, V(xe, (KX0 + KX1) / 2, Z0 + 0.41), V(0, -sx), V(sx, 0), 0.08, dis=1.18, yaprak=10)
    # octagonal turrets at the corners
    for yy in (KX0, KX1):
        c = V(xe - sx * 0.006, yy)
        y.prizma((c.x, c.y), 0.024, Z0, ZW + 0.08, DUV, n=8, ust=False, kat=math.pi / 8)
        for zz in (Z0 + 0.18, ZW - 0.01):
            halka_kornis(y, c, 0.024, zz, 0.01, 0.006, 8, DR, kat=math.pi / 8)
        donel(y, c, [(0.024, ZW + 0.08), (0.02, ZW + 0.08), (0.02, ZW + 0.1), (0.0, ZW + 0.2)], DUV, n=8, kat=math.pi / 8)
        for f in (0.45,):
            halka_kornis(y, c, 0.02 * (1 - f) - 0.001, ZW + 0.1 + 0.1 * f, 0.005, 0.004, 8, DR, kat=math.pi / 8)
        kure(y, (c.x, c.y, ZW + 0.204), 0.006, 'altin', n=6, kat=3)
    fiyal(y, xe + sx * 0.004, (KX0 + KX1) / 2, 0.02, ZW + ROOF_H - 0.02, 0.025, 0.06, DR)

# ---------------------------------------------------------------- the crossing lantern
y.bolum('Kesişim feneri')
ck = dikdortgen(-NX - 0.004, NX + 0.004, KX0 - 0.004, KX1 + 0.004)
LZ0, LZ1 = ZW + ROOF_H - 0.06, ZW + ROOF_H + 0.07
for i in range(4):
    a2, b2, L_, e2, n2 = eksen(ck[i], ck[(i + 1) % 4])
    for j in range(2):
        gotik_pencere(y, a2.lerp(b2, j / 2), a2.lerp(b2, (j + 1) / 2), LZ0, LZ1 - LZ0, en=0.5, sivri=0.7, v0=0.03, ust=0.012, derin=0.012, cam=CAM,
                      duvar=DUV, iz=DR, izli=False)
silme(y, ck, LZ1 - 0.008, 0.012, 0.01, DR, 'tac')
y.yuz_yon([V(p.x, p.y, LZ1 + 0.004) for p in ck], 'kursun', Z)
cd_ = disa(ck, 0.006)
for i in range(4):
    acik_korkuluk(y, cd_[i], cd_[(i + 1) % 4], LZ1 + 0.004, 0.026, DR, adim=0.017, t=0.009)
for p in cd_:
    fiyal(y, p.x, p.y, 0.024, LZ1 + 0.004, 0.04, 0.09, DUV, tip_key=DR)

# ---------------------------------------------------------------- apse (chevet)
y.bolum('Apsis ve şapel çelengi')
NA = 5
ang = [math.pi * k / NA for k in range(NA + 1)]
ic_ = [V(NX * math.cos(t), AY + NX * math.sin(t)) for t in ang]
dis_k = [V(AX * math.cos(t), AY + AX * math.sin(t)) for t in ang]
for k in range(NA):
    gotik_pencere(y, ic_[k], ic_[k + 1], ZC0 - 0.01, ZW - ZC0 + 0.01, en=0.5, sivri=0.8, cam=CAM, duvar=DUV, iz=DR)
    gotik_pencere(y, dis_k[k], dis_k[k + 1], Z0, ZA - Z0, en=0.42, sivri=0.7, v0=0.035, cam=CAM, duvar=DUV, iz=DR, izli=False)
    dd_ = [V(0, AY) + V(math.cos(t), math.sin(t)) * ((AX + 0.02) if j in (0, NA) else (AX + 0.02 / math.cos(math.pi / NA / 2))) for j, t in enumerate(ang)]
    a0, a1 = dd_[k], dd_[k + 1]   # (the ends on the aisle roofs' eave line: an open offset left a slit there)
    y.yuz_yon([V(a0.x, a0.y, ZA + 0.004), V(a1.x, a1.y, ZA + 0.004), V(ic_[k + 1].x, ic_[k + 1].y, ZC0), V(ic_[k].x, ic_[k].y, ZC0)], 'kursun', Z)
    nn = V(a0.x + a1.x, a0.y + a1.y - 2 * AY)
    y.yuz_yon([V(a0.x, a0.y, ZA + 0.004), V(a1.x, a1.y, ZA + 0.004), V(a1.x, a1.y, ZA - 0.006), V(a0.x, a0.y, ZA - 0.006)], 'kursun', nn)
    y.yuz_yon([V(a0.x, a0.y, ZA - 0.006), V(a1.x, a1.y, ZA - 0.006), V(dis_k[k + 1].x, dis_k[k + 1].y, ZA), V(dis_k[k].x, dis_k[k].y, ZA)], 'ahsap_koyu', -Z)
silme(y, ic_, ZW - 0.012, 0.012, 0.012, DR, 'tac', kapali=False)
silme(y, dis_k, ZA - 0.01, 0.01, 0.008, DR, 'duz', kapali=False)
for k in range(1, NA):
    t = ang[k]
    r_ = V(math.cos(t), math.sin(t)); t_ = V(-r_.y, r_.x)
    pi_ = payanda_ayagi(V(0, AY) + r_ * (AX - 0.008), r_, t_)
    ucus(pi_, V(0, AY) + r_ * NX)
for sx in (-1, 1):
    pi_ = payanda_ayagi(V(sx * AX, AY), V(sx, 0), V(0, 1))
    ucus(pi_, V(sx * NX, AY))

# ---------------------------------------------------------------- roofs
y.bolum('Kurşun çatılar')
cati_besik(y, -NX, NX, FY, AY, ZW, ROOF_H, 0.03, 'kursun', 'kursun2', ucluk_key=DUV, alt_key='ahsap_koyu', uc_sacak=0.0, ns=14, nr=6, mahya_en=0.012)
cati_besik(y, -TRX, TRX, KX0, KX1, ZW, ROOF_H, 0.03, 'kursun', 'kursun2', ucluk_key=DUV, alt_key='ahsap_koyu', uc_sacak=0.012, ns=10, nr=6, mahya_en=0.012)


def dikis(a, b):
    a, b = Vector(a), Vector(b)
    t = (b - a).normalized(); u = Z.cross(t).normalized(); n = t.cross(u).normalized()
    if n.z < 0: n = -n
    cubuk(y, a + n * 0.0016, b + n * 0.0016, 0.0035, 'kursun2', 0.0025)


EB = NX + 0.03
for sx in (-1, 1):
    yy = FY + 0.03
    while yy < AY - 0.01:
        if not (KX0 - 0.04 < yy < KX1 + 0.04):
            dikis(V(sx * EB, yy, ZW), V(0, yy, ZW + ROOF_H - 0.004))
        yy += 0.09
    xx0 = 0.15
    while xx0 < TRX - 0.01:
        for sy in (-1, 1):
            yc = (KX0 + KX1) / 2
            ww = (KX1 - KX0) / 2 + 0.03
            dikis(V(sx * xx0, yc + sy * ww, ZW), V(sx * xx0, yc, ZW + ROOF_H - 0.004))
        xx0 += 0.09
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
for k in (0, NK // 2, NK):
    cubuk(y, halka_[k] + Z * 0.004, tepe + Z * 0.004, 0.01, 'kursun2')

# ---------------------------------------------------------------- Henry VII's Lady Chapel
y.bolum('VII. Henry Şapeli (yelpaze tonozlu, çok tepelikli)')
HY0_, HY1_ = AY + AX - 0.01, 1.07     # its west and east ends
HN, HA = 0.1, 0.17                    # the clerestory and the aisle walls
HZW, HZA = Z0 + 0.38, Z0 + 0.2
# the polygonal east end: three canted faces
uc = [V(-HN, HY1_ - 0.06), V(-HN * 0.5, HY1_), V(HN * 0.5, HY1_), V(HN, HY1_ - 0.06)]
ucA = [V(-HA, HY1_ - 0.08), V(-HA * 0.45, HY1_ + 0.06), V(HA * 0.45, HY1_ + 0.06), V(HA, HY1_ - 0.08)]
nb = 3
hb = [HY0_ + (HY1_ - 0.06 - HY0_) * j / nb for j in range(nb + 1)]
for sx in (-1, 1):
    for j in range(nb):
        # clerestory: wide traceried windows
        pencere(V(sx * HN, hb[j]), V(sx * HN, hb[j + 1]), HZA + 0.02, HZW - HZA - 0.02, (sx, 0), en=0.66, sivri=0.4, v0=0.02, ust=0.015)
        # aisle: the great bay windows (canted, standing out between the turrets)
        a_, b_ = sirala(V(sx * HA, hb[j] + 0.016), V(sx * HA, hb[j + 1] - 0.016), (sx, 0))
        e_ = (b_ - a_).normalized(); n_ = V(e_.y, -e_.x)
        m_ = a_.lerp(b_, 0.5)
        k_ = [a_, a_ + e_ * 0.01 + n_ * 0.02, b_ - e_ * 0.01 + n_ * 0.02, b_]
        duz_duvar(y, k_[0], k_[1], Z0, HZA, DUV)
        duz_duvar(y, k_[2], k_[3], Z0, HZA, DUV)
        gotik_pencere(y, k_[1], k_[2], Z0, HZA - Z0, en=0.7, sivri=0.35, v0=0.03, ust=0.015, derin=0.012, cam=CAM, duvar=DUV, iz=DR)
        y.yuz_yon([V(p.x, p.y, HZA) for p in k_], 'kursun', Z)
        silme(y, k_, HZA - 0.008, 0.01, 0.006, DR, 'tac', kapali=False)
        # the aisle's flat lead roof
        y.yuz_yon([V(sx * HA, hb[j], HZA), V(sx * HA, hb[j + 1], HZA), V(sx * HN, hb[j + 1], HZA), V(sx * HN, hb[j], HZA)], 'kursun', Z)
        duvar(V(sx * HN, hb[j]), V(sx * HN, hb[j + 1]), Z0, HZA + 0.02, (sx, 0))
    # turret-buttresses on the bay lines: octagonal, panelled, with lead cupolas; flyers to the clerestory
    for j in range(nb + 1):
        c = V(sx * (HA + 0.008), hb[j])
        y.prizma((c.x, c.y), 0.022, Z0, HZW + 0.05, DUV, n=8, ust=False, kat=math.pi / 8)
        for zz in (HZW + 0.04,):
            halka_kornis(y, c, 0.022, zz, 0.008, 0.005, 8, DR, kat=math.pi / 8)
        t_ = y.kubbe((c.x, c.y), 0.024, HZW + 0.05, 0.03, 'kursun', n=8, kat=4)
        y.yuz_yon([V(p.x, p.y, HZW + 0.05) for p in cokgen(c, 0.024, 8)], DR, -Z)
        donel(y, c, [(0.004, t_.z - 0.002), (0.006, t_.z + 0.01), (0.0, t_.z + 0.03)], 'altin', n=6)
        ucan_payanda(y, c - V(sx * 0.016, 0), V(sx * HN, hb[j]), HZA + 0.05, HZA + 0.1, HZW - 0.07, HZW - 0.03, t=0.01, key=DUV, n=4)
    a_, b_ = (V(sx * (HN + 0.006), HY0_), V(sx * (HN + 0.006), HY1_ - 0.06)) if sx > 0 else (V(sx * (HN + 0.006), HY1_ - 0.06), V(sx * (HN + 0.006), HY0_))
    acik_korkuluk(y, a_, b_, HZW, 0.024, DR, adim=0.024, t=0.008)
    silme(y, [a_, b_], HZW - 0.01, 0.01, 0.006, DR, 'tac', kapali=False)
# the east end
for i in range(3):
    gotik_pencere(y, uc[i + 1], uc[i], HZA + 0.02, HZW - HZA - 0.02, en=0.62, sivri=0.4, v0=0.02, ust=0.015, derin=0.014, cam=CAM, duvar=DUV, iz=DR)
    gotik_pencere(y, ucA[i + 1], ucA[i], Z0, HZA - Z0, en=0.66, sivri=0.35, v0=0.03, ust=0.015, derin=0.012, cam=CAM, duvar=DUV, iz=DR)
    duvar(uc[i], uc[i + 1], Z0, HZA + 0.02, tuple((uc[i] + uc[i + 1]) / 2 - V(0, HY1_ - 0.1)))
silme(y, ucA[::-1], HZA - 0.008, 0.01, 0.006, DR, 'tac', kapali=False)
for i in range(3):
    pa, pb = ucA[i], ucA[i + 1]
    qa, qb = uc[i], uc[i + 1]
    y.yuz_yon([V(pa.x, pa.y, HZA), V(pb.x, pb.y, HZA), V(qb.x, qb.y, HZA), V(qa.x, qa.y, HZA)], 'kursun', Z)
for p in ucA:
    c = p
    y.prizma((c.x, c.y), 0.022, Z0, HZW + 0.05, DUV, n=8, ust=False, kat=math.pi / 8)
    for zz in (HZW + 0.04,):
        halka_kornis(y, c, 0.022, zz, 0.008, 0.005, 8, DR, kat=math.pi / 8)
    t_ = y.kubbe((c.x, c.y), 0.024, HZW + 0.05, 0.03, 'kursun', n=8, kat=4)
    y.yuz_yon([V(q.x, q.y, HZW + 0.05) for q in cokgen(c, 0.024, 8)], DR, -Z)
    donel(y, c, [(0.004, t_.z - 0.002), (0.006, t_.z + 0.01), (0.0, t_.z + 0.03)], 'altin', n=6)
for i in range(3):
    acik_korkuluk(y, uc[i] + (uc[i] - V(0, HY1_ - 0.1)).normalized() * 0.006, uc[i + 1] + (uc[i + 1] - V(0, HY1_ - 0.1)).normalized() * 0.006, HZW, 0.024,
                  DR, adim=0.024, t=0.008)
# its low lead roof: a gable along y and the canted end as a hip
cati_besik(y, -HN, HN, HY0_ - 0.03, HY1_ - 0.06, HZW, 0.07, 0.012, 'kursun', 'kursun2', ucluk_key=DUV, alt_key='ahsap_koyu', uc_sacak=0.0, ns=8, nr=4,
           mahya_en=0.008)
tp = V(0, HY1_ - 0.06, HZW + 0.07)
for i in range(3):
    m = (uc[i] + uc[i + 1]) / 2
    y.yuz_yon([V(uc[i].x, uc[i].y, HZW), V(uc[i + 1].x, uc[i + 1].y, HZW), tp], 'kursun2' if i % 2 else 'kursun', V(m.x, m.y - (HY1_ - 0.06), 0.6))

# ---------------------------------------------------------------- the cloister and the chapter house
y.bolum('Manastır avlusu (cloister) ve bölüm evi')
CLX0, CLX1, CLY0, CLY1 = AX + 0.004, 0.8, -0.62, KX0 - 0.004
CW_ = 0.07           # the walks' width
CZ = Z0 + 0.12       # the walks' wall top
gk = dikdortgen(CLX0 + CW_, CLX1 - CW_, CLY0 + CW_, CLY1 - CW_)   # the garth
y.yuz_yon([V(p.x, p.y, Z0 + 0.003) for p in gk], 'cimen', Z)
duvarlar(y, gk, Z0, Z0 + 0.003, DR)
# the walks: an outer wall, the traceried openings towards the garth, lean-to lead roofs
ok_ = dikdortgen(CLX0, CLX1, CLY0, CLY1)
for i in range(4):
    a, b = ok_[i], ok_[(i + 1) % 4]
    a2, b2, L_, e2, n2 = eksen(a, b)
    if i == 3:   # against the nave's south aisle: no outer wall needed
        pass
    else:
        duz_duvar(y, a2, b2, Z0, CZ + 0.02, DUV)
    ia, ib = gk[(i + 1) % 4], gk[i]   # the inner wall line, run so its face looks into the garth
    ia2, ib2, Li, ei, ni = eksen(ia, ib)
    n_ = max(2, int(round(Li / 0.12)))
    for j in range(n_):
        gotik_pencere(y, ia2.lerp(ib2, j / n_), ia2.lerp(ib2, (j + 1) / n_), Z0, CZ - Z0, en=0.7, sivri=0.6, v0=0.025, ust=0.012, derin=0.014, cam='koyu',
                      duvar=DUV, iz=DR, izli=False)
        if j > 0:
            p = ia2.lerp(ib2, j / n_)
            kutu3(y, p + ni * 0.008 + Z * (Z0 + 0.05), ei, ni, Z, 0.012, 0.016, 0.1, DUV, ('+x', '-x', '+y', '+z'))
# lean-to roofs (from the outer wall top down to the inner wall)
for i in range(4):
    a, b = ok_[i], ok_[(i + 1) % 4]
    c, d = gk[(i + 1) % 4], gk[i]
    nrm = V((a.x + b.x) / 2 - (CLX0 + CLX1) / 2, (a.y + b.y) / 2 - (CLY0 + CLY1) / 2).normalized()
    y.yuz_yon([V(a.x, a.y, CZ + 0.05), V(b.x, b.y, CZ + 0.05), V(c.x, c.y, CZ + 0.002), V(d.x, d.y, CZ + 0.002)], 'kursun', -nrm + Z * 3)
silme(y, gk, CZ - 0.006, 0.008, 0.008, DR, 'tac')
for i in range(3):
    a, b = ok_[i], ok_[(i + 1) % 4]
    duz_duvar(y, a, b, CZ + 0.02, CZ + 0.05, DUV)
# a well in the garth with monks around it
gc = V((CLX0 + CLX1) / 2, (CLY0 + CLY1) / 2)
donel(y, gc, [(0.03, Z0), (0.03, Z0 + 0.03), (0.024, Z0 + 0.03), (0.024, Z0 + 0.022)], DR, n=14)
y.yuz_yon([V(p.x, p.y, Z0 + 0.022) for p in cokgen(gc, 0.024, 14)], 'su', Z)
agac(y, gc.x + 0.12, gc.y + 0.12, Z0, boy=0.16, key='boya_yesil')
from frank_ortak import insan
for k, (dx, dy, a) in enumerate(((-0.08, 0.02, 0.2), (0.06, -0.1, 2.2), (-0.12, -0.12, 1.0), (0.1, 0.04, 3.8))):
    insan(y, gc.x + dx, gc.y + dy, Z0 + 0.003, 'kece' if k % 2 else 'koyu', aci=a, s=1.0)
# the chapter house: an octagon with tall windows, flying buttresses and a lead pyramid
CH = V(0.68, 0.24)
RC = 0.1
k8 = cokgen(CH, RC, 8, math.pi / 8)
for i in range(8):
    if i == 4:   # towards the transept: plain
        duz_duvar(y, k8[i], k8[(i + 1) % 8], Z0, Z0 + 0.3, DUV); continue
    gotik_pencere(y, k8[i], k8[(i + 1) % 8], Z0, 0.27, en=0.72, sivri=0.6, v0=0.06, ust=0.02, derin=0.014, cam=CAM, duvar=DUV, iz=DR)
    duz_duvar(y, k8[i], k8[(i + 1) % 8], Z0 + 0.27, Z0 + 0.3, DUV)
silme(y, k8, Z0 + 0.29, 0.012, 0.01, DR, 'tac')
for i in range(8):
    if i in (4, 5): continue
    p = k8[i]
    r_ = (p - CH).normalized(); t_ = V(-r_.y, r_.x)
    q = p + r_ * 0.08
    kutu3(y, q + Z * (Z0 + 0.11), r_, t_, Z, 0.03, 0.024, 0.22, DUV, ('+x', '-x', '+y', '-y', '+z'))
    fiyal(y, q.x, q.y, 0.022, Z0 + 0.22, 0.03, 0.07, DUV, tip_key=DR, aci=math.atan2(r_.y, r_.x))
    ucan_payanda(y, q - r_ * 0.015, p, Z0 + 0.18, Z0 + 0.24, Z0 + 0.24, Z0 + 0.28, t=0.01, key=DUV, n=4)
donel(y, CH, [(RC + 0.012, Z0 + 0.3), (0.0, Z0 + 0.42)], 'kursun', n=8, kat=math.pi / 8, dilim=['kursun', 'kursun2'])
y.yuz_yon([V(p.x, p.y, Z0 + 0.3) for p in cokgen(CH, RC + 0.012, 8, math.pi / 8)], 'ahsap_koyu', -Z)
y.prizma((CH.x, CH.y), 0.003, Z0 + 0.41, Z0 + 0.46, 'altin', n=4)
kure(y, (CH.x, CH.y, Z0 + 0.46), 0.007, 'altin', n=6, kat=3)
# the vestibule linking it to the cloister's east walk
kutu3(y, V(0.68, KX0 + 0.01, Z0 + 0.07), X, Y, Z, 0.08, 0.06, 0.14, DUV, ('+x', '-x', '+z'))

# ---------------------------------------------------------------- people on the parvis: the coronation procession
y.bolum('Meydanda alay')
for k in range(8):
    x = -0.03 + 0.06 * (k % 2)
    yy = -1.08 + 0.025 * (k // 2) * 0 - 0.0
    insan(y, -0.035 + 0.07 * (k % 2), -1.1 + 0.035 * (k // 2), Z0, ['boya_kirmizi', 'altin', 'boya_kirmizi', 'beyaz', 'lacivert'][k % 5], aci=math.pi / 2, s=1.0,
          sapka='altin' if k == 7 else None)
for k, (x, yy, a) in enumerate(((-0.4, -1.0, 0.3), (0.42, -0.98, 2.8), (0.5, -0.85, 3.4), (-0.48, -0.88, 0.0))):
    insan(y, x, yy, Z0, ['kumas', 'boya_yesil', 'kece', 'ahsap_acik'][k], aci=a, s=1.0)

calistir(y, 'lm_westminster')
