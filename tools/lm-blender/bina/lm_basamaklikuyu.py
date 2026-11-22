# Stepwell (lm_basamaklikuyu) in the manner of Chand Baori: an inverted pyramid of nine terraces sunk into a walled
# platform, its east, west and south faces covered in the zigzag double flights of steps, the north face rising in
# three set-back tiers of pillared galleries with balconies and a shrine niche, water at the bottom; above ground the
# multi-storey royal pavilion with jharokhas and chhatris, cloister arcades round the court, kiosks at the well's mouth.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from hint_ortak import *

y = Yapi()
TAS, TAS2, TAS3 = 'kum', 'kum_koyu', 'kum_acik'
KIR, KIR2 = 'kirmizi_tas', 'kirmizi_tas_acik'
SV = (TAS, TAS2, TAS3, 'koyu')
NV = (TAS, TAS2, TAS3, TAS2)                 # blind niches
N = 9                                        # terraces
A0, W = 0.25, 0.05                           # the lowest riser's half size, the terrace depth
ZB, ZG = 0.045, 0.3                          # the lowest walkway (by the water), the court
DZ = (ZG - ZB) / N
a = lambda k: A0 + k * W
z = lambda k: ZB + k * DZ
YF = lambda k: a(3 * (k // 3)) if k >= 0 else a(-1)        # the north edge of terrace k: the gallery tier's facade
PX0, PX1, PY0, PY1 = -1.0, 1.0, -1.0, 0.98   # the platform


def R(k):
    """the rectangle inside riser k: x0, x1, y0, y1"""
    return (-a(k), a(k), -a(k), YF(k))


# ---------------- the platform and its outer walls ----------------
y.bolum('Kaide ve dış duvarlar')
pk = dikdortgen(PX0, PX1, PY0, PY1)
for i in range(4):
    p, q = pk[i], pk[(i + 1) % 4]
    L = (p - q).length
    nis_satir(y, p, q, 0.035, ZG - 0.03, max(4, int(round(L / 0.17))), NV, en=0.6, derin=0.01, sivri=0.45)
    duz_duvar(y, p, q, 0.0, 0.035, TAS2)
    duz_duvar(y, p, q, ZG - 0.03, ZG, TAS)
silme(y, pk, 0.0, 0.035, 0.012, TAS2, 'kaide')
silme(y, pk, ZG - 0.03, 0.012, 0.006, TAS3, 'duz')
# the court: the platform's top round the well's mouth
r8 = R(N - 1)
for (x0, x1, y0, y1) in ((PX0, PX1, PY0, r8[2]), (PX0, PX1, r8[3], PY1), (PX0, r8[0], r8[2], r8[3]), (r8[1], PX1, r8[2], r8[3])):
    y.yuz_yon([V(x0, y0, ZG), V(x1, y0, ZG), V(x1, y1, ZG), V(x0, y1, ZG)], 'zemin', Z)

# ---------------- the terraces ----------------
y.bolum('Teraslar ve basamaklar')
for k in range(N):
    x0, x1, y0, y1 = R(k)
    px0, px1, py0, py1 = R(k - 1)
    zk = z(k)
    # the walkway at level k: R(k) minus R(k-1)
    for (u0, u1, v0, v1) in ((x0, x1, y0, py0), (x0, px0, py0, y1), (px1, x1, py0, y1), (px0, px1, py1, y1)):
        if u1 - u0 > 1e-6 and v1 - v0 > 1e-6:
            y.yuz_yon([V(u0, v0, zk), V(u1, v0, zk), V(u1, v1, zk), V(u0, v1, zk)], 'tas', Z)
    # the risers of the east, west and south faces (looking into the well)
    for (p, q) in ((V(x0, y0), V(x1, y0)), (V(x1, y0), V(x1, y1)), (V(x0, y1), V(x0, y0))):
        duz_duvar(y, q, p, zk, zk + DZ, 'tas_koyu')
        # double flights: stepped triangles against the riser
        e = (q - p).normalized(); nn = V(-e.y, e.x)          # nn: into the well
        L = (q - p).length
        n = max(1, int(L / 0.1))
        P = L / n * 0.8
        for j in range(n):
            uc = p + e * (L * (j + 0.5) / n)
            for s in range(3):
                w_ = P * (1 - s / 3.0)
                o = uc - e * (w_ / 2) + Z * zk
                kutu(y, o, e, w_, W * 0.62, DZ * (s + 1) / 3, 'tas_acik', 'arkasagsolust')
    # a moulded lip at the walkway's edge (the riser's top)
    if k > 0:
        silme(y, [V(px1, py1), V(px1, py0), V(px0, py0), V(px0, py1)], zk - 0.004, 0.004, 0.003, TAS3, 'duz', kapali=False)

# the pool at the bottom
y.bolum('Su')
p0 = R(-1)
pool = dikdortgen(*p0)
for i in range(4):
    duz_duvar(y, pool[(i + 1) % 4], pool[i], ZB - 0.02, ZB, TAS2)
y.yuz_yon([V(p.x, p.y, ZB - 0.012) for p in pool], 'su', Z)
# lotus leaves on the water
for (x, yy, r) in ((-0.07, -0.05, 0.022), (0.08, 0.04, 0.018), (0.02, -0.12, 0.016), (-0.1, 0.1, 0.02)):
    donel(y, (x, yy), [(0.0, ZB - 0.0115), (r, ZB - 0.0115), (r, ZB - 0.0095), (0.0, ZB - 0.0095)], 'boya_yesil', n=10)

# ---------------- the north galleries (three tiers) ----------------
y.bolum('Kuzey galerileri')
for t in range(3):
    k0 = 3 * t
    yf = a(k0)
    za, zt = z(k0), z(k0 + 3)
    xe = a(k0 + 2)
    xc = a(k0)
    # the outer parts (behind the east / west terraces): plain wall
    for (u0, u1) in ((-xe, -xc), (xc, xe)):
        duz_duvar(y, V(u0, yf), V(u1, yf), za, zt, TAS)
    # the gallery: pillared arches with a deep dark veranda behind
    nb = max(3, int(round(2 * xc / 0.075)))
    hh = zt - za
    for j in range(nb):
        p, q = V(-xc + 2 * xc * j / nb, yf), V(-xc + 2 * xc * (j + 1) / nb, yf)
        mid = j == nb // 2 and t == 2
        if mid:
            # the shrine niche: a deeper framed niche with a small idol and a lamp
            y.kemerli(p, q, za, hh, (KIR, KIR2, TAS3, 'koyu'), v0=0.006, en=0.74, ust=hh * 0.12, derin=0.03, k_say=10, sivri=0.5,
                      cerceve=(0.005, [TAS3, KIR]))
            m = (p + q) / 2 + V(0, 0.02)
            elipsoid(y, (m.x, m.y, za + 0.025), 0.009, 0.006, 0.014, 'boya_kirmizi', n=8, kat=4)
            kure(y, (m.x, m.y, za + 0.044), 0.006, 'boya_kirmizi', n=8, kat=4)
            continue
        y.kemerli(p, q, za, hh, SV, v0=hh * 0.1, en=0.7, ust=hh * 0.14, derin=0.03, k_say=8, sivri=0.0, cerceve=(0.004, TAS3))
        if j > 0:
            # (a square pier with a bracket capital in front of the pier: the stepwell's plain pillars)
            kutu_merkez(y, (p.x, yf - 0.007), 0.009, 0.009, hh * 0.47, TAS3, z0=za + hh * 0.1, yuzler='onarkasagsol')
            kutu_merkez(y, (p.x, yf - 0.007), 0.014, 0.013, hh * 0.05, TAS3, z0=za + hh * 0.57)
    # the floor ledge (chhajja) at the tier's top, the parapet in front of the next tier
    chhajja(y, [V(-xe, yf), V(xe, yf)], zt - 0.012, 0.012, 0.016, TAS3, kapali=False)
    if t == 1:
        for s in (-1, 1):
            jharokha(y, V(s * xc * 0.55 - 0.06, yf), V(s * xc * 0.55 + 0.06, yf), za + hh * 0.32, 0.07, hh * 0.55, 0.035,
                     key=KIR, trim=KIR2, kubbe=True)

# ---------------- kiosks at the well's mouth, its parapet ----------------
y.bolum('Ağız korkuluğu ve köşkler')
x0, x1, y0, y1 = r8
lip = [V(x0, y1), V(x0, y0), V(x1, y0), V(x1, y1)]
# a low pierced parapet round the east, west and south edges (outer face to the court)
for i in range(3):
    p, q = lip[i], lip[i + 1]
    e = (q - p).normalized(); nn = V(e.y, -e.x)           # (nn: away from the well)
    # (q -> p: its outer face to the right is the court side)
    kutu(y, p - nn * 0.0 + Z * ZG, e, (q - p).length, 0.018, 0.035, TAS3)
for (cx, cy) in ((x0 - 0.08, y0 - 0.08), (x1 + 0.08, y0 - 0.08), (x0 - 0.08, y1 - 0.12), (x1 + 0.08, y1 - 0.12)):
    chhatri(y, cx, cy, ZG, 0.05, n=6, kolon=TAS3, kubbe=TAS3, kaide=TAS, kat=math.pi / 6)
for (cx, cy) in ((-0.93, -0.93), (0.93, -0.93)):       # kiosks on the cloisters' outer corners
    chhatri(y, cx, cy, ZG + 0.13, 0.04, n=4, kolon=TAS3, kubbe=TAS3, kaide=KIR, kat=math.pi / 4)

# ---------------- the cloisters (east, west, south) ----------------
y.bolum('Revaklar')
KH = 0.13
KD = 0.14


def revak(p, q, nb, kapi=None):
    """a cloister wing p->q (its arcade facing right, its back on the platform's edge): arches, roof, parapet"""
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    L = (q - p).length
    for j in range(nb):
        u0, u1 = p.lerp(q, j / nb), p.lerp(q, (j + 1) / nb)
        if kapi is not None and j == kapi:
            continue
        y.kemerli(u0, u1, ZG, KH, (TAS, TAS2, TAS3, TAS2), v0=0.0, en=0.76, ust=0.02, derin=KD * 0.8, k_say=8, sivri=0.5, cerceve=(0.004, TAS3))
    back = [p - nn * KD, q - nn * KD]
    # roof slab with a chhajja and a parapet with small merlons
    y.yuz_yon([p + Z * (ZG + KH), q + Z * (ZG + KH), back[1] + Z * (ZG + KH), back[0] + Z * (ZG + KH)], 'zemin', Z)
    chhajja(y, [p, q], ZG + KH - 0.014, 0.014, 0.022, TAS3, kapali=False)
    kutu(y, p + Z * (ZG + KH), e, L, 0.012, 0.02, TAS3)                  # a low parapet
    mazgal(y, p, q, ZG + KH + 0.02, 0.012, 0.012, TAS3, dis_en=0.03, bosluk=0.05)   # with sparse pinnacles
    duz_duvar(y, back[1], back[0], ZG, ZG + KH, TAS)
    for u in (p, q):
        y.yuz_yon([u + Z * ZG, u - nn * KD + Z * ZG, u - nn * KD + Z * (ZG + KH), u + Z * (ZG + KH)], TAS, e * (-1 if u is p else 1))


revak(V(PX1 - KD, a(6)), V(PX1 - KD, PY0), 11)
revak(V(PX0 + KD, PY0), V(PX0 + KD, a(6)), 11)
revak(V(PX1 - KD, PY0 + KD), V(PX0 + KD, PY0 + KD), 11, kapi=5)

# ---------------- the south gate ----------------
y.bolum('Güney kapısı')
GW = 1.72 / 11
GX0, GX1 = -GW / 2, GW / 2
GY0, GY1 = PY0 - 0.02, PY0 + KD
GH = 0.26
gk = dikdortgen(GX0, GX1, GY0, GY1)
y.kemerli(gk[0], gk[1], ZG, GH, (TAS, TAS2, TAS3, 'ahsap'), v0=0.0, en=0.58, ust=0.07, derin=0.05, k_say=10, sivri=0.55, cerceve=(0.008, [TAS3, KIR]))
y.kemerli(gk[2], gk[3], ZG, GH, (TAS, TAS2, TAS3, TAS2), v0=0.0, en=0.58, ust=0.07, derin=0.05, k_say=10, sivri=0.55)
duz_duvar(y, gk[1], gk[2], ZG, ZG + GH, TAS)
duz_duvar(y, gk[3], gk[0], ZG, ZG + GH, TAS)
silme(y, gk, ZG + GH - 0.016, 0.016, 0.012, TAS3, 'kaba')
y.yuz_yon([V(p.x, p.y, ZG + GH) for p in gk], 'zemin', Z)
for p in (gk[0], gk[1]):
    chhatri(y, p.x + (0.036 if p is gk[0] else -0.036), p.y + 0.045, ZG + GH, 0.03, n=4, kolon=TAS3, kubbe=TAS3, kaide=KIR, kat=math.pi / 4)
sancak(y, 0.0, GY1 - 0.03, ZG + GH, boy=0.22, en=0.12, yuk=0.07, aci=-0.5)
# the stair up to it from the ground
merdiven(y, (0.0, PY0 - 0.27), math.pi / 2, 0.16, 0.0, ZG, n=12, d=0.25 / 12, key=TAS2, yanlik=TAS3)

# ---------------- the royal pavilion (north) ----------------
y.bolum('Saray köşkü')
YP0, YP1 = a(6), PY1
# the low wings either side (cloister height)
for (u0, u1) in ((PX0, -0.42), (0.42, PX1)):
    k = dikdortgen(u0, u1, YP0, YP1)
    nb = max(2, int(round((u1 - u0) / 0.12)))
    for j in range(nb):
        p, q = V(u0 + (u1 - u0) * j / nb, YP0), V(u0 + (u1 - u0) * (j + 1) / nb, YP0)
        y.kemerli(p, q, ZG, KH, (TAS, TAS2, TAS3, TAS2), v0=0.0, en=0.74, ust=0.02, derin=0.08, k_say=8, sivri=0.5, cerceve=(0.004, TAS3))
    for i in (1, 2, 3):
        duz_duvar(y, k[i], k[(i + 1) % 4], ZG, ZG + KH, TAS)
    y.yuz_yon([V(p.x, p.y, ZG + KH) for p in k], 'zemin', Z)
    chhajja(y, k, ZG + KH - 0.014, 0.014, 0.022, TAS3)
    chhatri(y, (u0 + u1) / 2 + (0.08 if u0 < 0 else -0.08), (YP0 + YP1) / 2, ZG + KH, 0.045, n=4, kolon=TAS3, kubbe=TAS3, kaide=KIR, kat=math.pi / 4)
    for i in range(4):
        kutu(y, k[i] + Z * (ZG + KH), (k[(i + 1) % 4] - k[i]).normalized(), (k[(i + 1) % 4] - k[i]).length, 0.012, 0.02, TAS3)
# the central block: three storeys
KAT = [(-0.42, 0.42, YP0, YP1, 0.15, 7), (-0.36, 0.36, YP0 + 0.03, YP1 - 0.04, 0.13, 5), (-0.22, 0.22, YP0 + 0.08, YP1 - 0.1, 0.11, 3)]
zk = ZG
for si, (u0, u1, v0, v1, h, nb) in enumerate(KAT):
    k = dikdortgen(u0, u1, v0, v1)
    for j in range(nb):
        p, q = V(u0 + (u1 - u0) * j / nb, v0), V(u0 + (u1 - u0) * (j + 1) / nb, v0)
        if si == 0 and j == nb // 2:
            y.kemerli(p, q, zk, h, (TAS, TAS2, TAS3, 'koyu'), v0=0.0, en=0.7, ust=0.025, derin=0.04, k_say=10, sivri=0.55, cerceve=(0.007, [TAS3, KIR]))
        else:
            y.kemerli(p, q, zk, h, SV, v0=h * 0.12, en=0.6, ust=h * 0.16, derin=0.025, k_say=8, sivri=0.5, cerceve=(0.005, TAS3))
    # the back and sides: windows
    for i in (1, 2, 3):
        p, q = k[i], k[(i + 1) % 4]
        L = (q - p).length
        nw = max(1, int(round(L / (0.16 if i == 2 else 0.12))))      # (the back, over the platform edge: fewer, unframed)
        for j in range(nw):
            y.kemerli(p.lerp(q, j / nw), p.lerp(q, (j + 1) / nw), zk, h, SV, v0=h * 0.3, en=0.34, ust=h * 0.24, derin=0.012, k_say=6, sivri=0.5,
                      cerceve=None if i == 2 else (0.004, TAS3))
    chhajja(y, k, zk + h - 0.016, 0.016, 0.028, KIR2)
    silme(y, k, zk, 0.012, 0.006, TAS2, 'kaide')
    zk += h
    y.yuz_yon([V(p.x, p.y, zk) for p in k], 'zemin', Z)
    if si == 1:
        # jharokhas on the second storey's front
        for s in (-1, 1):
            jharokha(y, V(s * 0.18 + 0.045, v0), V(s * 0.18 - 0.045, v0), zk - h + h * 0.25, 0.08, h * 0.6, 0.04, key=KIR, trim=KIR2)
    if si < 2:
        # a parapet on the terrace round the next storey
        mazgal(y, k[0], k[1], zk, 0.018, 0.01, TAS3, dis_en=0.016, bosluk=0.012)
# roof kiosks: chhatris at the corners of the second storey, a domed pavilion crowning the top
u0, u1, v0, v1 = KAT[1][:4]
z2 = ZG + KAT[0][4] + KAT[1][4]
for (cx, cy) in ((u0 + 0.05, v0 + 0.05), (u1 - 0.05, v0 + 0.05), (u0 + 0.05, v1 - 0.05), (u1 - 0.05, v1 - 0.05)):
    chhatri(y, cx, cy, z2, 0.036, n=4, kolon=TAS3, kubbe=TAS3, kaide=KIR, kat=math.pi / 4)
cx, cy = 0.0, (KAT[2][2] + KAT[2][3]) / 2
y.prizma((cx, cy), 0.1, zk, zk + 0.025, TAS, n=24, ust=True)
halka_kornis(y, (cx, cy), 0.1, zk + 0.019, 0.006, 0.006, 24, TAS3)
lotus_kubbe(y, (cx, cy), 0.098, zk + 0.025, 0.1, TAS3, n=24, kat=8, yaprak=TAS3, s_son=1.6)
for s in (-1, 1):
    chhatri(y, s * 0.17, cy, zk, 0.032, n=4, kolon=TAS3, kubbe=TAS3, kaide=KIR, kat=math.pi / 4)

# ---------------- people, trees ----------------
y.bolum('İnsanlar ve ağaçlar')
def yuruyen(yan, k, t, g):
    """a woman carrying a water pot on the walkway of terrace k: yan 0 south, 1 east, 2 west; t 0..1 along it"""
    m = (a(k - 1) + a(k)) / 2
    if yan == 0: x, yy, aa = -m + 2 * m * t, -m, 0.0
    elif yan == 1: x, yy, aa = m, -m + (m + YF(k)) * t, math.pi / 2
    else: x, yy, aa = -m, -m + (m + YF(k)) * t, -math.pi / 2
    adam(y, x, yy, z(k), aa, g, 'beyaz', boy=0.042)
    kure(y, (x, yy, z(k) + 0.049), 0.0075, 'bronz', n=8, kat=4)


for (yan, k, t, g) in ((0, 1, 0.3, 'boya_kirmizi'), (0, 4, 0.62, 'boya_sari'), (1, 2, 0.45, 'turkuaz'), (2, 5, 0.3, 'boya_kirmizi'),
                       (1, 7, 0.7, 'beyaz'), (0, 7, 0.2, 'boya_sari'), (2, 1, 0.6, 'lacivert'), (0, 0, 0.5, 'boya_kirmizi')):
    yuruyen(yan, k, t, g)
for (x, yy) in ((-0.45, -0.77), (0.45, -0.77), (-0.76, -0.25), (0.76, -0.25), (-0.76, 0.12), (0.76, 0.12)):
    agac(y, x, yy, ZG, boy=0.16, tur='yaprakli', key='boya_yesil' if x < 0 else 'yesil_koyu')
for (x, yy) in ((-1.12, -0.4), (1.12, -0.2), (-1.1, 0.6), (1.1, 0.7), (-0.6, -1.12), (0.6, -1.12)):
    agac(y, x, yy, 0.0, boy=0.22, tur='palmiye' if yy < 0 else 'yaprakli', key='boya_yesil')

bolum_say(y)
calistir(y, 'lm_basamaklikuyu')
