# Pirinç Terasları (lm_pirincteras): a hillside of wet-rice terraces (Longji / Yuanyang manner): curved contour terraces
# climbing to a hilltop, each with an earthen bund, flooded paddies with rows of seedlings (a few grown green or
# ripening), a stream cascading down the gully between them, a bamboo water wheel lifting water into a flume, a stone
# slab bridge, farmhouses with hipped tile roofs, haystacks, a water buffalo at the plough, farmers in straw hats,
# bamboo groves, and on the hilltop a village shrine hall with a five-storey timber pagoda.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ortak import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(12)
GX0, GX1, GY0, GY1 = -1.15, 1.15, -1.12, 1.12
ZV = 0.04                    # the valley floor
N = 11                       # terraces
DH = 0.036
SX0, SX1 = 0.31, 0.39        # the stream's channel
BUND = 0.014


def g(x):
    """the hillside's shape across x: a spur (contours bulging forward) and the stream's gully (bulging back)"""
    return 0.17 * math.exp(-((x + 0.35) / 0.38) ** 2) - 0.13 * math.exp(-((x - 0.35) / 0.22) ** 2) + 0.035 * math.sin(3.1 * x + 0.6)


def c(k, x):
    """the front edge of terrace k (k = N: the hilltop's edge)"""
    return -0.62 + k * 0.12 + g(x) * (1 - 0.25 * k / N)


def zk(k):
    return ZV + (k + 1) * DH


XS_L = [GX0 + (SX0 - GX0) * i / 30 for i in range(31)]
XS_R = [SX1 + (GX1 - SX1) * i / 20 for i in range(21)]

# the state of each terrace: flooded with seedlings (most), grown green, ripening
DURUM = ['su', 'su', 'yesil', 'su', 'su', 'sari', 'su', 'su', 'yesil', 'su', 'su']


# the cut faces of the hillside's block: strata of rock and soil with wavering boundaries, not one flat brown wall
STRATA = [(0.045, 'kaya_koyu'), (0.08, 'kaya'), (0.15, 'kaya_koyu'), (0.185, 'toprak'), (0.25, 'kaya'), (0.31, 'kaya_koyu'),
          (0.345, 'kaya'), (0.42, 'kaya_koyu'), (0.46, 'toprak'), (0.53, 'kaya'), (9.0, 'kaya_koyu')]


def kesit(p0, p1, ztop, yon):
    """a vertical cut face from p0 to p1 (2D), from 0 up to ztop, in strata"""
    p0, p1 = V(p0[0], p0[1]), V(p1[0], p1[1])
    L = (p1 - p0).length
    nseg = max(1, int(math.ceil(L / 0.05)))
    dalga = lambda m, u: 0.007 * math.sin(u * 13 + m * 1.7) + 0.004 * math.sin(u * 31 + m * 2.3)
    for i in range(nseg):
        pa, pb = p0.lerp(p1, i / nseg), p0.lerp(p1, (i + 1) / nseg)
        ua, ub = pa.x + pa.y, pb.x + pb.y
        la, lb = 0.0, 0.0
        for m, (b, key) in enumerate(STRATA):
            ha, hb = min(ztop, b + dalga(m, ua)), min(ztop, b + dalga(m, ub))
            if max(ha - la, hb - lb) > 1e-5:
                # (the hard rock layers stand a little proud of the softer ones, with a ledge above and below)
                o = yon * (0.005 if key == 'kaya' else 0.0)
                qa, qb = pa + V(o.x, o.y), pb + V(o.x, o.y)
                y.yuz_yon([V(qa.x, qa.y, la), V(qb.x, qb.y, lb), V(qb.x, qb.y, hb), V(qa.x, qa.y, ha)], key, yon)
                if key == 'kaya':
                    y.yuz_yon([V(pa.x, pa.y, ha), V(pb.x, pb.y, hb), V(qb.x, qb.y, hb), V(qa.x, qa.y, ha)], key, Z)
                    y.yuz_yon([V(pa.x, pa.y, la), V(pb.x, pb.y, lb), V(qb.x, qb.y, lb), V(qa.x, qa.y, la)], 'kaya_koyu', -Z)
                    e_ = (p1 - p0) / L
                    if i == 0:
                        y.yuz_yon([V(pa.x, pa.y, la), V(qa.x, qa.y, la), V(qa.x, qa.y, ha), V(pa.x, pa.y, ha)], key, -e_)
                    if i == nseg - 1:
                        y.yuz_yon([V(pb.x, pb.y, lb), V(qb.x, qb.y, lb), V(qb.x, qb.y, hb), V(pb.x, pb.y, hb)], key, e_)
            la, lb = max(la, ha), max(lb, hb)
            if la >= ztop - 1e-6 and lb >= ztop - 1e-6:
                break


def serit(xs, f0, f1, z0, z1, key, yon):
    """a band of quads between the curves f0(x) at z0 and f1(x) at z1 (each f returns y)"""
    for i in range(len(xs) - 1):
        a, b = xs[i], xs[i + 1]
        y.yuz_yon([V(a, f0(a), z0), V(b, f0(b), z0), V(b, f1(b), z1), V(a, f1(a), z1)], key, yon)


y.bolum('Teraslar')
for k in range(N):
    zf = zk(k)
    z_alt = zk(k - 1) if k > 0 else ZV - 0.012 + 0.006
    durum = DURUM[k]
    for xs in (XS_L, XS_R):
        # the riser (earth; the lowest ones stone-faced), the bund's top and inner side, the paddy surface
        serit(xs, lambda x: c(k, x), lambda x: c(k, x), z_alt - 0.004, zf + 0.012, 'kaya' if k < 2 else 'toprak', -Y)
        serit(xs, lambda x: c(k, x), lambda x: c(k, x) + BUND, zf + 0.012, zf + 0.012, 'cimen', Z)
        serit(xs, lambda x: c(k, x) + BUND, lambda x: c(k, x) + BUND, zf + 0.012, zf + 0.004, 'toprak_ot', Y)
        yuzey = {'su': 'su', 'yesil': 'cimen', 'sari': 'cimen_kuru'}[durum]
        serit(xs, lambda x: c(k, x) + BUND, lambda x: c(k + 1, x), zf + 0.004, zf + 0.004, yuzey, Z)
        # rows of seedlings (dashes along the contour), or ripe ears in rows
        satir = 3 if durum == 'su' else 4
        for j in range(satir):
            t = (j + 0.7) / (satir + 0.4)
            f = lambda x, t=t: c(k, x) + BUND + (c(k + 1, x) - c(k, x) - BUND) * t
            for i in range(len(xs) - 1):
                if (i + j) % 2: continue
                a, b = xs[i], xs[i + 1]
                if durum == 'su':
                    kk, hh, w = 'boya_yesil', 0.006, 0.006
                else:
                    kk, hh, w = ('yesil_koyu' if durum == 'yesil' else 'saz'), 0.004, 0.009
                pa, pb = V(a, f(a), zf + 0.004), V(b, f(b), zf + 0.004)
                nn = V(0, 1, 0) * (w / 2)
                # a low ridge of plants: two slopes meeting in a crest
                y.yuz_yon([pa - nn, pb - nn, pb + Z * hh, pa + Z * hh], kk, -Y + Z)
                y.yuz_yon([pa + Z * hh, pb + Z * hh, pb + nn, pa + nn], kk, Y + Z)
                y.yuz_yon([pa - nn, pa + Z * hh, pa + nn], kk, -X)
                y.yuz_yon([pb - nn, pb + nn, pb + Z * hh], kk, X)
    # the platform's sides: a slice under each terrace at both edges, the stream's channel walls
    for (x, s) in ((GX0, -1), (GX1, 1)):
        # bedrock below, the terrace's own soil above (the cut shows the steps as layers)
        zs_ = zf - 0.026
        kesit((x, c(k, x)), (x, c(k + 1, x)), zs_, V(s, 0, 0))
        y.yuz_yon([V(x, c(k, x), zs_), V(x, c(k + 1, x), zs_), V(x, c(k + 1, x), zf + 0.004), V(x, c(k, x) + BUND, zf + 0.004),
                   V(x, c(k, x) + BUND, zf + 0.012), V(x, c(k, x), zf + 0.012)], 'toprak', V(s, 0, 0))
    for (x, s) in ((SX0, 1), (SX1, -1)):
        y.yuz_yon([V(x, c(k, x), zf - 0.006), V(x, c(k + 1, x), zf - 0.006), V(x, c(k + 1, x), zf + 0.004), V(x, c(k, x) + BUND, zf + 0.004),
                   V(x, c(k, x) + BUND, zf + 0.012), V(x, c(k, x), zf + 0.012)], 'kaya', V(s, 0, 0))
    # the stream: a pool at this level and the fall into the one below
    y.yuz_yon([V(SX0, c(k, SX0), zf - 0.006), V(SX1, c(k, SX1), zf - 0.006), V(SX1, c(k + 1, SX1), zf - 0.006), V(SX0, c(k + 1, SX0), zf - 0.006)],
              'su', Z)
    y.yuz_yon([V(SX0, c(k, SX0), z_alt - 0.006 - (0.0 if k else 0.004)), V(SX1, c(k, SX1), z_alt - 0.006 - (0.0 if k else 0.004)),
               V(SX1, c(k, SX1), zf - 0.006), V(SX0, c(k, SX0), zf - 0.006)], 'su', -Y)
    # white water at the foot of each fall
    y.yuz_yon([V(SX0 + 0.004, c(k, SX0) - 0.01, z_alt - 0.0038), V(SX1 - 0.004, c(k, SX1) - 0.01, z_alt - 0.0038),
               V(SX1 - 0.004, c(k, SX1) - 0.002, z_alt - 0.0038), V(SX0 + 0.004, c(k, SX0) - 0.002, z_alt - 0.0038)], 'kece', Z)

# the hilltop
y.bolum('Tepe ve köy tapınağı')
ZT = zk(N - 1) + DH * 0.5
for xs in (XS_L, XS_R):
    serit(xs, lambda x: c(N, x), lambda x: c(N, x), zk(N - 1) - 0.004, ZT, 'toprak', -Y)
    serit(xs, lambda x: c(N, x), lambda x: GY1, ZT, ZT, 'cimen', Z)
for (x, s) in ((GX0, -1), (GX1, 1)):
    kesit((x, c(N, x)), (x, GY1), ZT - 0.022, V(s, 0, 0))
    y.yuz_yon([V(x, c(N, x), ZT - 0.022), V(x, GY1, ZT - 0.022), V(x, GY1, ZT), V(x, c(N, x), ZT)], 'toprak', V(s, 0, 0))
kesit((GX1, GY1), (GX0, GY1), ZT - 0.022, Y)
y.yuz_yon([V(GX1, GY1, ZT - 0.022), V(GX0, GY1, ZT - 0.022), V(GX0, GY1, ZT), V(GX1, GY1, ZT)], 'toprak', Y)
# the spring at the stream's head: a small pond
for (x, s) in ((SX0, 1), (SX1, -1)):
    y.yuz_yon([V(x, c(N, x), ZT - 0.012), V(x, c(N, x) + 0.12, ZT - 0.012), V(x, c(N, x) + 0.12, ZT), V(x, c(N, x), ZT)], 'kaya', V(s, 0, 0))
y.yuz_yon([V(SX0, c(N, SX0), ZT - 0.006), V(SX1, c(N, SX1), ZT - 0.006), V(SX1, c(N, SX1) + 0.12, ZT - 0.006), V(SX0, c(N, SX0) + 0.12, ZT - 0.006)],
          'su', Z)
y.yuz_yon([V(SX1, c(N, SX1) + 0.12, ZT - 0.012), V(SX0, c(N, SX0) + 0.12, ZT - 0.012), V(SX0, c(N, SX0) + 0.12, ZT), V(SX1, c(N, SX1) + 0.12, ZT)],
          'kaya', -Y)
y.yuz_yon([V(SX0, c(N, SX0), zk(N - 1) - 0.006), V(SX1, c(N, SX1), zk(N - 1) - 0.006), V(SX1, c(N, SX1), ZT - 0.006), V(SX0, c(N, SX0), ZT - 0.006)],
          'su', -Y)
# (the hilltop surface over the channel: closed between the pond and the back)
y.yuz_yon([V(SX0, c(N, SX0) + 0.12, ZT), V(SX1, c(N, SX1) + 0.12, ZT), V(SX1, GY1, ZT), V(SX0, GY1, ZT)], 'cimen', Z)

# the five-storey pagoda on the spur's head, the shrine hall, a stone stair down to the terraces
PG = (-0.42, 0.98)
kutu_merkez(y, PG, 0.24, 0.24, 0.02, 'granit', z0=ZT)
silme(y, dikdortgen(PG[0] - 0.12, PG[0] + 0.12, PG[1] - 0.12, PG[1] + 0.12), ZT + 0.016, 0.004, 0.003, 'tas_acik')
z = ZT + 0.02
w = 0.18
tepe = z
for kk in range(5):
    tepe, z2 = pagoda_kati(y, PG, w, z, 0.065 if kk == 0 else 0.05, 0.05, 0.05, key_duvar='lake', key_direk='lake', key_cati='kiremit_koyu',
                           mahya='kiremit_koyu2', kivrim=0.55, yukari=0.03, korkuluk=kk > 0, balkon=0.016 if kk > 0 else 0, alt_key='lake_koyu')
    z = z2 - 0.004
    w *= 0.84
sorin(y, PG[0], PG[1], tepe - 0.004, 0.13)
sancak(y, PG[0] + 0.13, PG[1] - 0.13, ZT, boy=0.24, en=0.1, yuk=0.06, aci=-0.4)
salon(y, 0.0, 0.26, 0.86, 1.02, ZT, 0.07, 0.07, sacak=0.035, tur='irimoya', kapi_yon=0, kaide=0.022, sus='kiremit_koyu2', duvar='siva_kirmizi')
# incense burner and two cypresses before the shrine
y.prizma((0.13, 0.8), 0.014, ZT, ZT + 0.02, 'bronz', n=8)
y.koni((0.13, 0.8), 0.02, ZT + 0.02, 0.02, 'bronz', n=8)
for xx in (0.03, 0.23):
    agac(y, xx, 0.8, ZT, boy=0.14, tur='servi', key='yesil_koyu')

# ---------------- the valley floor ----------------
y.bolum('Vadi, dere, su çarkı')
for xs in (XS_L, XS_R):
    serit(xs, lambda x: GY0, lambda x: c(0, x), ZV, ZV, 'cimen_kuru', Z)
for (x, s) in ((GX0, -1), (GX1, 1)):
    y.yuz_yon([V(x, GY0, 0), V(x, c(0, x), 0), V(x, c(0, x), ZV), V(x, GY0, ZV)], 'kaya_koyu', V(s, 0, 0))
for xs in (XS_L, XS_R):
    serit(xs, lambda x: GY0, lambda x: GY0, 0, ZV, 'kaya_koyu', -Y)
# the stream across the valley
ZS = ZV - 0.012
for (x, s) in ((SX0, 1), (SX1, -1)):
    y.yuz_yon([V(x, GY0, ZS - 0.004), V(x, c(0, x), ZS - 0.004), V(x, c(0, x), ZV), V(x, GY0, ZV)], 'kaya', V(s, 0, 0))
y.yuz_yon([V(SX0, GY0, ZS), V(SX1, GY0, ZS), V(SX1, c(0, SX1), ZS), V(SX0, c(0, SX0), ZS)], 'su', Z)
y.yuz_yon([V(SX0, GY0, 0), V(SX1, GY0, 0), V(SX1, GY0, ZS), V(SX0, GY0, ZS)], 'kaya_koyu', -Y)
# a stone slab bridge
for k in range(3):
    kutu(y, V(SX0 - 0.03, -0.62 + 0.0 - k * 0.026, ZV), X, SX1 - SX0 + 0.06, 0.024, 0.008, 'granit' if k % 2 else 'kaya', 'onarkasagsolust')
for xx in (SX0 + 0.004, SX1 - 0.004):
    kutu_merkez(y, (xx, -0.65), 0.012, 0.075, ZV - ZS + 0.002, 'kaya_koyu', z0=ZS - 0.002)

# the bamboo water wheel (tongche) lifting water into a flume
WC = V((SX0 + SX1) / 2, -0.93, ZV + 0.06)
R = 0.1
for sx in (-1, 1):
    pts = [WC + V(sx * 0.014, R * math.cos(TAU * k / 20), R * math.sin(TAU * k / 20)) for k in range(21)]
    boru(y, pts, 0.003, 'ahsap', n=4, kapat=False)
for k in range(10):
    a = TAU * k / 10
    d = V(0, math.cos(a), math.sin(a))
    cubuk(y, WC - V(0.014, 0, 0), WC + d * R - V(0.014, 0, 0), 0.0035, 'ahsap_acik')
    cubuk(y, WC + V(0.014, 0, 0), WC + d * R + V(0.014, 0, 0), 0.0035, 'ahsap_acik')
    # paddles and bamboo tubes on the rim
    p = WC + d * (R + 0.006)
    kutu_merkez(y, (p.x, p.y), 0.034, 0.006, 0.016, 'ahsap', z0=p.z - 0.008, aci=0.0) if abs(math.cos(a)) > 0.3 else \
        kutu_merkez(y, (p.x, p.y), 0.034, 0.016, 0.006, 'ahsap', z0=p.z - 0.003)
    boru(y, [p + V(0.022, 0, 0), p + V(0.022, 0, 0) + V(0, -math.sin(a), math.cos(a)) * 0.02], 0.004, 'boya_yesil', n=5)
boru(y, [WC - V(0.04, 0, 0), WC + V(0.04, 0, 0)], 0.006, 'ahsap_koyu', n=8)
for sx in (-1, 1):   # the trestles on the banks
    for sy in (-1, 1):
        cubuk(y, V(WC.x + sx * 0.05, WC.y + sy * 0.03, ZV), V(WC.x + sx * 0.04, WC.y, WC.z), 0.007, 'ahsap')
# the flume carrying the water to the valley fields (towards -x)
FL = WC + V(-0.03, 0.0, R + 0.012)
for (a, b) in ((FL, FL + V(-0.25, 0.04, -0.05)), (FL + V(-0.25, 0.04, -0.05), FL + V(-0.45, 0.06, -0.08))):
    cubuk(y, a, b, 0.016, 'boya_yesil', 0.008)
    m = (a + b) / 2
    cubuk(y, V(m.x, m.y, ZV), V(m.x, m.y, m.z - 0.005), 0.006, 'ahsap')

# farmhouses with hipped tile roofs, courtyards, haystacks
y.bolum('Çiftlik evleri ve harman')
for (x0, y0_, w_, d_, yon) in ((-1.0, -1.0, 0.24, 0.15, 2), (-0.68, -0.98, 0.2, 0.14, 2), (0.62, -1.0, 0.24, 0.15, 3), (0.72, -0.78, 0.2, 0.13, 3)):
    salon(y, x0, x0 + w_, y0_, y0_ + d_, ZV, 0.065, 0.065, sacak=0.03, duvar='kerpic', direk='ahsap_koyu', tur='kirma', kapi_yon=yon,
          kaide=0.012, kivrim=0.35, yukari=0.015, basamak=False)
# the threshing floor and haystacks
y.prizma((-0.35, -0.86), 0.09, ZV, ZV + 0.004, 'kum_acik', n=16)
for (hx, hy) in ((-0.45, -0.95), (-0.25, -0.98), (-0.2, -0.74), (0.95, -0.55)):
    donel(y, (hx, hy), [(0.0, ZV), (0.032, ZV), (0.034, ZV + 0.03), (0.022, ZV + 0.05), (0.006, ZV + 0.06), (0.0, ZV + 0.062)], 'saz', n=10)
# low walls round the yards
for (pts_) in ([V(-0.72, -0.8), V(-1.04, -0.8)], [V(0.58, -0.62), V(0.58, -0.88)]):
    cin_duvar(y, pts_, ZV, 0.035, t=0.014, key='kerpic', kaide='kerpic_koyu')
# the buffalo at the plough in a dry field by the stream
y.bolum('Manda, çiftçiler, bambu')
FX0_, FX1_, FY0_, FY1_ = -0.12, 0.26, -1.07, -0.72
y.yuz_yon([V(FX0_, FY0_, ZV + 0.002), V(FX1_, FY0_, ZV + 0.002), V(FX1_, FY1_, ZV + 0.002), V(FX0_, FY1_, ZV + 0.002)], 'kerpic_koyu', Z)
for k in range(13):   # furrows
    yy = FY0_ + 0.015 + k * 0.026
    cubuk(y, V(FX0_ + 0.01, yy, ZV + 0.003), V(FX1_ - 0.01, yy, ZV + 0.003), 0.007, 'toprak', 0.003)
with parca(y, (0.12, -0.9, ZV + 0.002), math.pi):
    boru(y, [V(-0.03, 0, 0.034), V(0.03, 0, 0.036)], 0.019, 'kaya_koyu', n=8)
    boru(y, [V(0.03, 0, 0.04), V(0.055, 0, 0.032)], 0.011, 'kaya_koyu', n=6, r_son=0.008)
    for (lx, ly) in ((-0.022, -0.01), (-0.022, 0.01), (0.022, -0.01), (0.022, 0.01)):
        cubuk(y, V(lx, ly, 0.0), V(lx, ly, 0.028), 0.008, 'kaya_koyu')
    for sy in (-1, 1):   # sweeping horns
        boru(y, [V(0.05, sy * 0.006, 0.044), V(0.048, sy * 0.022, 0.05), V(0.036, sy * 0.028, 0.054)], 0.0035, 'mermer', n=4, r_son=0.0012)
    cubuk(y, V(-0.035, 0, 0.034), V(-0.04, 0, 0.012), 0.004, 'kaya_koyu')
    # yoke, shafts and the plough
    cubuk(y, V(0.035, -0.02, 0.05), V(0.035, 0.02, 0.05), 0.005, 'ahsap')
    cubuk(y, V(0.035, 0, 0.05), V(-0.1, 0, 0.02), 0.005, 'ahsap')
    cubuk(y, V(-0.1, 0, 0.02), V(-0.12, 0, 0.0), 0.007, 'ahsap_koyu')
    cubuk(y, V(-0.1, 0, 0.02), V(-0.13, 0, 0.045), 0.004, 'ahsap')
insan(y, 0.27, -0.9, ZV + 0.002, aci=0.0, govde='lacivert')
# farmers planting in the paddies (bent), others on the bunds
for (fx, k, eg) in ((-0.8, 1, 0.8), (-0.5, 2, 0.8), (0.0, 1, 0.8), (0.7, 3, 0.8), (-0.95, 4, 0.0), (0.15, 4, 0.8), (-0.3, 6, 0.8), (0.75, 6, 0.0),
                    (-0.65, 8, 0.8), (0.9, 9, 0.8)):
    fy = (c(k, fx) + c(k + 1, fx)) / 2
    insan(y, fx, fy, zk(k) + 0.004, aci=rn.uniform(0, TAU), govde=rn.choice(['kumas', 'lacivert', 'siva_oker']), egik=eg)
for (px, py) in ((-0.2, -0.85), (0.5, -0.7), (-0.85, -0.7)):
    insan(y, px, py, ZV, aci=rn.uniform(0, TAU), govde=rn.choice(['kumas', 'lacivert']))
# bamboo groves and trees: in the valley, on the hilltop
for (bx, by) in ((-1.08, -0.62), (-0.55, -0.64), (0.5, -1.04), (1.08, -0.95), (-0.95, -0.55)):
    bambu(y, bx, by, ZV, boy=0.14, n=8, tohum=int(bx * 100 + by * 10), serpinti=True)
for (bx, by) in ((0.55, 1.04), (0.78, 1.06), (1.08, 0.8), (-0.75, 1.05), (-0.95, 0.95)):
    if by > c(N, bx) + 0.04:
        bambu(y, bx, by, ZT, boy=0.16, n=9, tohum=int(bx * 50), serpinti=True)
# a hamlet on the hilltop's right: houses, a drying rack
for (x0, y0_, w_, d_, yon) in ((0.62, 0.86, 0.2, 0.13, 0), (0.88, 0.9, 0.18, 0.13, 3)):
    if y0_ > c(N, x0) + 0.03:
        salon(y, x0, x0 + w_, y0_, y0_ + d_, ZT, 0.06, 0.06, sacak=0.03, duvar='kerpic', direk='ahsap_koyu', tur='kirma', kapi_yon=yon,
              kaide=0.012, kivrim=0.35, yukari=0.015, basamak=False)
for xx in (0.48, 0.58):
    cubuk(y, V(xx, 0.82, ZT), V(xx, 0.82, ZT + 0.05), 0.005, 'ahsap')
cubuk(y, V(0.47, 0.82, ZT + 0.045), V(0.59, 0.82, ZT + 0.045), 0.004, 'ahsap_koyu')
for k in range(5):
    boru(y, [V(0.49 + k * 0.022, 0.82, ZT + 0.045), V(0.49 + k * 0.022, 0.82, ZT + 0.015)], 0.004, 'saz', n=4)
# a flagged path from the shrine to the hamlet
for k in range(9):
    px = 0.3 + k * 0.035
    py = 0.82 + 0.01 * math.sin(k)
    kutu_merkez(y, (px, py), 0.028, 0.03, 0.003, 'granit' if k % 2 else 'kaya', z0=ZT, aci=0.2 * math.sin(k * 1.3))
for (tx, ty) in ((-1.05, 1.06), (0.42, 0.96), (-0.15, 1.05), (1.06, 1.06)):
    if ty > c(N, tx) + 0.04:
        agac(y, tx, ty, ZT, boy=0.14, key='boya_yesil')

calistir(y, 'lm_pirincteras')
