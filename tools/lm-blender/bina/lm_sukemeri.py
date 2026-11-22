# The aqueduct (lm_sukemeri), after the Pont du Gard: three tiers of golden limestone arches across a river valley -
# 7 big arches (the widest over the river, cutwaters upstream), 11 middle and 33 small ones carrying the covered water
# channel - with its projecting building stones, string courses and arch rings. The channel turns at the east end on a short arcade
# along the plateau into a round castellum (distribution basin) whose overflow runs down a stepped cascade to a pool.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi(tohum=5)

# ---------------------------------------------------------------- terrain
# A low valley with two green hills the bridge springs from. The plot is a rounded patch whose rim comes down to
# ground level all round, so it sits on the game's ground like a piece of landscape, not a cut-out block; the hills
# stay well under the top tier so the three rows of arches carry the silhouette. The grid's columns are laid on the
# river's edges (straight banks, no staircase) and the slopes are coloured on a five-step ramp (grass -> dry grass
# -> scrub -> earth -> rock) so the zones blend instead of stepping.
XE, YE = 1.3, 1.0            # plot half sizes
ZG = 0.03                    # valley floor
ZR = 0.008                   # river surface
RIV = 0.075                  # river half width (along y, x ~ 0)
HC = 0.29                    # hill crest above the valley floor (the top tier stands at 0.44)
KK, KQ = 0.2, 4              # corner rounding of the plot (grid -> plot mapping)


def ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def plot_xy(u, v):
    """grid point (u, v in -1..1) -> the rounded plot; the middle columns stay straight (the river's banks)"""
    return XE * u * (1 - KK * abs(v) ** KQ), YE * v * (1 - KK * abs(u) ** KQ)


def plot_uv(x, yy):
    u, v = x / XE, yy / YE
    for _ in range(6):
        u = x / (XE * (1 - KK * abs(v) ** KQ)); v = yy / (YE * (1 - KK * abs(u) ** KQ))
    return u, v


def kenar(x, yy):
    """0 on the rim of the rounded plot, 1 from ~0.2 (in grid units) inside it"""
    u, v = plot_uv(x, yy)
    return ss(0.0, 0.2, 1 - max(abs(u), abs(v)))


def ici(x, yy, pay=0.0):
    """inside the plot, pay (grid units) from its rim"""
    u, v = plot_uv(x, yy)
    return max(abs(u), abs(v)) <= 1 - pay


def dus(a, b, t):
    """1 -> 0 from a to b: half linear, half smoothstep (a hillside: no cliff in the middle, no kink at the ends)"""
    k = max(0.0, min(1.0, (t - a) / (b - a)))
    return 1 - 0.5 * k - 0.5 * ss(a, b, t)


def tepe(x, yy):
    """hill height above the valley floor: west a ridge along the bridge, east a broad plateau reaching north to
    the castellum; both rise from the valley and fall away again towards the rim"""
    if x < 0:
        u = -x
        return HC * ss(0.44, 0.92, u) * dus(0.96, 1.3, u) * (1 - ss(0.3, 0.84, abs(yy)))
    u = x + 0.24 * ss(0.1, 0.3, yy)
    return HC * ss(0.44, 0.92, u) * dus(0.98, 1.32, x) * ss(-0.84, -0.3, yy) * dus(0.56, 0.98, yy)


def nehir(x):
    """1 in the river bed, 0 on the banks"""
    return 1 - ss(RIV - 0.005, RIV + 0.035, abs(x))


def yuk(x, yy):
    t = tepe(x, yy)
    h = ZG + t + 0.008 * math.sin(x * 9.1 + yy * 3.3) * math.sin(yy * 7.7 - x * 2.1) * min(1.0, t / 0.1)
    h -= (ZG - ZR) * nehir(x)
    u, v = plot_uv(x, yy)
    m = 1 - max(abs(u), abs(v))
    return (h - t) * ss(0.0, 0.2, m) + t * ss(0.0, 0.05, m)


def leke(x, yy):   # smooth 0..1 noise to break up the colour zones
    return 0.5 + 0.25 * math.sin(x * 13.1 + yy * 5.7) * math.sin(yy * 11.3 - x * 4.1) + 0.25 * math.sin(x * 6.3 - yy * 9.2)


RAMPA = ('cimen', 'cimen_kuru', 'toprak_ot', 'toprak', 'kaya_koyu')
y.bolum('arazi')
# columns: dense and exact over the river (bed edge, bank top, bank foot), even beyond
XC = [0.0, 0.035, RIV - 0.005, RIV + 0.035, RIV + 0.075]
NB = 28
XC += [XC[-1] + (XE - XC[-1]) * k / NB for k in range(1, NB + 1)]
US = sorted({-c / XE for c in XC} | {c / XE for c in XC})
NY = 50
VS = [-1 + 2 * j / NY for j in range(NY + 1)]
G = [[None] * len(VS) for _ in US]
for i, u in enumerate(US):
    for j, v in enumerate(VS):
        x, yy = plot_xy(u, v)
        xr = XE * u                                  # (the river follows the straight columns)
        h = ZG + tepe(x, yy) - (ZG - ZR) * nehir(xr)
        t = tepe(x, yy)
        h += 0.008 * math.sin(x * 9.1 + yy * 3.3) * math.sin(yy * 7.7 - x * 2.1) * min(1.0, t / 0.1)
        m = 1 - max(abs(u), abs(v))
        G[i][j] = V(x, yy, (h - t) * ss(0.0, 0.2, m) + t * ss(0.0, 0.05, m))
for i in range(len(US) - 1):
    xr = abs(XE * (US[i] + US[i + 1]) / 2)
    for j in range(NY):
        q = [G[i][j], G[i + 1][j], G[i + 1][j + 1], G[i][j + 1]]
        cx, cy = sum(p.x for p in q) / 4, sum(p.y for p in q) / 4
        if xr < RIV - 0.005:
            y.yuz_yon(q, 'su', Z); continue
        if xr < RIV + 0.075:                                     # sandy banks, one quad each (straight edges)
            y.yuz_yon(q, 'kum_acik', Z); continue
        tris = ((q[0], q[1], q[2]), (q[0], q[2], q[3])) if (q[0] - q[2]).length <= (q[1] - q[3]).length else                ((q[0], q[1], q[3]), (q[1], q[2], q[3]))
        for tri in tris:
            n = (tri[1] - tri[0]).cross(tri[2] - tri[0])
            if n.length < 1e-12: continue
            n = n.normalized()
            tx, ty = sum(p.x for p in tri) / 3, sum(p.y for p in tri) / 3
            # steepness plus a little noise, and bare tops on the high ground
            w = (1 - n.z) / 0.4 + 0.3 * (leke(tx, ty) - 0.5) + 0.12 * ss(0.2, 0.3, tepe(tx, ty))
            key = RAMPA[0 if w < 0.3 else 1 if w < 0.52 else 2 if w < 0.76 else 3 if w < 1.06 else 4]
            y.yuz_yon(list(tri), key, Z)


def taban(x0, x1, y0, y1, n=4):
    """the lowest ground under a footprint (to stand a structure on the slope)"""
    return min(yuk(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * j / n) for i in range(n + 1) for j in range(n + 1))


# ---------------------------------------------------------------- the bridge
y.bolum('kopru')
RENK = ('kum', 'kum_koyu', 'kum_acik', 'kum_koyu')
K1, K2, K3 = 0.11, 0.085, 0.064            # tier thicknesses
Z1, Z2, Z3 = 0.23, 0.44, 0.52             # tier tops
XS1 = [-0.62, -0.46, -0.29, -0.11, 0.11, 0.29, 0.46, 0.62]
XS2 = [-0.94, -0.78] + XS1 + [0.78, 0.94]
X3 = 1.0


def kemer_halka(x0, x1, z0, Hh, en, ust, k, f=0.011, key='kum_acik', ks=10):
    """a raised ring of voussoirs round one arch on both faces of a tier k thick (centred on y = 0)"""
    W = x1 - x0
    R = en * W / 2
    xc = (x0 + x1) / 2
    zs = z0 + Hh - ust - R
    for sg in (-1, 1):
        yf = sg * (k / 2 + 0.003)
        ic = [V(xc + R * math.cos(math.pi * t / ks), yf, zs + R * math.sin(math.pi * t / ks)) for t in range(ks + 1)]
        dis = [V(xc + (R + f) * math.cos(math.pi * t / ks), yf, zs + (R + f) * math.sin(math.pi * t / ks)) for t in range(ks + 1)]
        duz = [V(p.x, sg * k / 2, p.z) for p in dis]
        for t in range(ks):
            y.yuz_yon([ic[t], ic[t + 1], dis[t + 1], dis[t]], key, V(0, sg))
            y.yuz_yon([dis[t], dis[t + 1], duz[t + 1], duz[t]], key, dis[t] + dis[t + 1] - 2 * V(xc, yf, zs))
        # the imposts: short ledges where the arch springs
        for xx in (xc - R - f, xc + R):
            kutu(y, V(xx, sg * k / 2 - (0.006 if sg < 0 else 0), zs - 0.008), X, f, 0.006, 0.008, key, 'onarkasagsolust')


def kat(xs, k, z0, Hh, ust, ayak):
    for i in range(len(xs) - 1):
        W = xs[i + 1] - xs[i]
        en = 1 - ayak / W
        kemer_dizisi(y, V(xs[i], -k / 2), V(xs[i + 1], -k / 2), 1, z0, Hh, k, RENK, en=en, ust=ust, acik=True, taban=False)
        kemer_halka(xs[i], xs[i + 1], z0, Hh, en, ust, k)
    kornis(y, xs[0], xs[-1], -k / 2, k / 2, z0 + Hh - 0.012, 0.012, 0.008, 'kum_acik')


# abutments where the tiers run into the slopes
for x0, x1, k, z0, z1 in ((-0.74, -0.62, K1, 0, Z1), (0.62, 0.74, K1, 0, Z1), (-1.03, -0.94, K2, Z1 - 0.04, Z2), (0.94, 1.03, K2, Z1 - 0.04, Z2)):
    kutu(y, V(x0, -k / 2, z0), X, x1 - x0, k, z1 - z0, 'kum', 'onarkasagsolust')
kat(XS1, K1, 0.0, Z1, 0.03, 0.075)
kat(XS2, K2, Z1, Z2 - Z1, 0.026, 0.05)
# the top tier: 33 small arches (three over each middle arch, as on the Pont du Gard)
kemer_dizisi(y, V(-X3, -K3 / 2), V(X3, -K3 / 2), 33, Z2, Z3 - Z2, K3, RENK, en=0.64, ust=0.014, acik=True, taban=False)
kornis(y, -X3, X3, -K3 / 2, K3 / 2, Z3 - 0.008, 0.008, 0.006, 'kum_acik')

# cutwaters on the upstream (-y) side of the lower piers by the river
for xp in (-0.29, -0.11, 0.11, 0.29):
    w = 0.075; yb = -K1 / 2; ap = yb - 0.06; zt = 0.09
    a, b, c = V(xp - w / 2, yb), V(xp + w / 2, yb), V(xp, ap)
    y.yuz_yon([a + Z * 0, c + Z * 0, c + Z * zt, a + Z * zt], 'kum', V(-1, -1))
    y.yuz_yon([c + Z * 0, b + Z * 0, b + Z * zt, c + Z * zt], 'kum', V(1, -1))
    uc = V(xp, yb, zt + 0.05)
    y.yuz_yon([a + Z * zt, c + Z * zt, uc], 'kum_acik', V(-1, -1, 1))
    y.yuz_yon([c + Z * zt, b + Z * zt, uc], 'kum_acik', V(1, -1, 1))

# the projecting stones left from the scaffolding, on the piers (both faces)
y.bolum('cikinti taslar')
for xs, k, z0, zz in ((XS1, K1, 0, (0.07, 0.15)), (XS2, K2, Z1, (Z1 + 0.06, Z1 + 0.13))):
    for xp in xs[1:-1]:
        for z_ in zz:
            for sg in (-1, 1):
                kutu_merkez(y, (xp, sg * (k / 2 + 0.006)), 0.014, 0.012, 0.012, 'kum_koyu', z0=z_)

# ---------------------------------------------------------------- the water channel (specus), covered with slabs
y.bolum('kanal')
KW = 0.013          # channel wall
ZC = Z3 + 0.042     # channel wall top


def kanal(a, b, k, z0, bosluk=()):
    """a covered channel from a to b on a base k wide: side walls, water, cover slabs (bosluk: missing slabs)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; n = V(-e.y, e.x)
    kutu(y, a - n * (k / 2) + Z * z0, e, L, KW, ZC - z0, 'kum', 'onarkasagsolust')
    kutu(y, a + n * (k / 2 - KW) + Z * z0, e, L, KW, ZC - z0, 'kum', 'onarkasagsolust')
    y.yuz_yon([a - n * (k / 2 - KW) + Z * (ZC - 0.012), b - n * (k / 2 - KW) + Z * (ZC - 0.012), b + n * (k / 2 - KW) + Z * (ZC - 0.012),
               a + n * (k / 2 - KW) + Z * (ZC - 0.012)], 'su', Z)
    m = max(2, int(round(L / 0.062)))
    s = L / m
    for i in range(m):
        if i in bosluk: continue
        o = a + e * (s * i + 0.003) - n * (k / 2 + 0.004) + Z * ZC
        kutu(y, o, e, s - 0.006, k + 0.008, 0.011, 'kirec', 'onarkasagsolust')


kanal((-X3 + 0.01, 0), (X3 + 0.03, 0), K3, Z3, bosluk=(8, 21))
# the corner: the channel turns north on a short arcade along the plateau, then west into the castellum
CX = X3 - 0.002
XK, YK = 0.8, 0.43          # castellum centre (on the plateau)
RK = 0.13                   # castellum drum radius
ZP = 0.5                    # castellum top (the channel floor Z3 is just above: it spills into the basin)
YN = YK - K3 / 2            # the north run ends at the west run's side
zk = taban(CX - K3 / 2 - 0.008, CX + K3 / 2 + 0.008, -K3 / 2 - 0.008, K3 / 2 + 0.008) - 0.012
kutu(y, V(CX - K3 / 2 - 0.008, -K3 / 2 - 0.008, zk), X, K3 + 0.016, K3 + 0.016, Z3 - zk, 'kum', 'onarkasagsolust')
za = taban(CX - K3 / 2, CX + K3 / 2, K3 / 2 + 0.008, YN) - 0.012
kemer_dizisi(y, V(CX + K3 / 2, K3 / 2 + 0.008), V(CX + K3 / 2, YN), 3, za, Z3 - za, K3, RENK, en=0.6, ust=0.03, acik=True, taban=False)
kornis(y, CX - K3 / 2, CX + K3 / 2, K3 / 2 + 0.008, YN, Z3 - 0.008, 0.008, 0.005, 'kum_acik')
# the corner pier and the short west run to the drum (solid: it stands on the plateau)
XD = XK + RK - 0.004        # the drum's face on the channel line (near enough: the channel is narrow)
zc_ = taban(XD, CX + K3 / 2 + 0.008, YN - 0.008, YK + K3 / 2 + 0.008) - 0.012
kutu(y, V(XD, YN - 0.008, zc_), X, CX + K3 / 2 + 0.008 - XD, K3 + 0.016, Z3 - zc_, 'kum', 'onarkasagsolust')
kornis(y, XD, CX + K3 / 2 + 0.008, YN - 0.008, YK + K3 / 2 + 0.008, Z3 - 0.008, 0.008, 0.005, 'kum_acik')
# over the drum's rim: a block from its top up to the channel floor
kutu(y, V(XK + 0.096, YN, ZP), X, XD - XK - 0.096 + 0.002, K3, Z3 - ZP, 'kum', 'onarkasagsolust')
kanal((CX, K3 / 2), (CX, YN), K3, Z3, bosluk=(3,))
kanal((CX + K3 / 2, YK), (XK + 0.098, YK), K3, Z3)

# ---------------------------------------------------------------- the castellum divisorum
y.bolum('castellum')
zd = taban(XK - RK, XK + RK, YK - RK, YK + RK, n=6) - 0.012     # the drum stands on the plateau: down to the lowest ground
donel(y, (XK, YK), [(RK, zd), (RK, ZP - 0.012), (RK + 0.008, ZP - 0.012), (RK + 0.008, ZP), (0.0, ZP)], 'kirec', n=32)
halka_kornis(y, (XK, YK), RK, ZP - 0.06, 0.012, 0.008, 32, 'kirec', profil='kaide')
# the water falling from the channel into the basin
y.yuz_yon([V(XK + 0.098, YK - 0.012, ZP + 0.012), V(XK + 0.098, YK + 0.012, ZP + 0.012), V(XK + 0.098, YK + 0.012, Z3 + 0.03),
           V(XK + 0.098, YK - 0.012, Z3 + 0.03)], 'su', -X)
# the round basin: a kerb wall, water, ten outlet holes
donel(y, (XK, YK), [(0.1, ZP), (0.1, ZP + 0.03), (0.092, ZP + 0.03), (0.092, ZP + 0.012)], 'mermer', n=32)
y.yuz_yon([V(XK + 0.092 * math.cos(TAU * i / 32), YK + 0.092 * math.sin(TAU * i / 32), ZP + 0.012) for i in range(32)], 'su', Z)
for i in range(10):
    a = math.pi * 0.55 + math.pi * 0.9 * i / 9
    o = V(XK + 0.1 * math.cos(a), YK + 0.1 * math.sin(a), ZP + 0.015)
    y.oculus(o, V(-math.sin(a), math.cos(a)), V(math.cos(a), math.sin(a)), 0.005, 'koyu', 'bronz', f=0.002, k=6)
# a roof on columns over it (tholos)
for i in range(8):
    a = TAU * (i + 0.5) / 8
    cx, cy = XK + 0.118 * math.cos(a), YK + 0.118 * math.sin(a)
    sutun(y, cx, cy, ZP, ZP + 0.1, 0.0075, 'mermer', 'toskan')
silme(y, cokgen((XK, YK), 0.128, 16), ZP + 0.1, 0.014, 0.004, 'mermer', 'duz')
y.serit([V(p.x, p.y, ZP + 0.1) for p in cokgen((XK, YK), 0.128, 16)], [V(p.x, p.y, ZP + 0.1) for p in cokgen((XK, YK), 0.1, 16)], 'mermer')
donel(y, (XK, YK), [(0.104, ZP + 0.1), (0.104, ZP + 0.114)], 'mermer', n=16)
donel(y, (XK, YK), [(0.122, ZP + 0.114), (0.148, ZP + 0.112), (0.148, ZP + 0.118), (0.09, ZP + 0.15), (0.03, ZP + 0.175), (0.0, ZP + 0.18)], 'kiremit', n=32)
kure(y, (XK, YK, ZP + 0.19), 0.012, 'bronz', n=10, kat=5)
y.prizma((XK, YK), 0.004, ZP + 0.178, ZP + 0.2, 'bronz', n=6)
sancak(y, XK, YK, ZP + 0.2, boy=0.2, en=0.12, yuk=0.075, aci=math.radians(200))

# ---------------------------------------------------------------- the cascade and the pool
y.bolum('cagla ve havuz')
YC = YK
xs_c = [XK - 0.13 - 0.05 * i for i in range(14)]
zprev = ZP - 0.02
for i, x in enumerate(xs_c):
    zt = max(yuk(x - 0.025, YC) + 0.012, ZP - 0.02 - (i + 1) * 0.034)
    zt = min(zt, zprev)
    zb = min(yuk(x, YC + 0.04), yuk(x - 0.05, YC + 0.04), yuk(x, YC - 0.04), yuk(x - 0.05, YC - 0.04)) - 0.01
    # side walls
    for sg in (-1, 1):
        kutu(y, V(x - 0.05, YC + sg * 0.035 - (0.012 if sg < 0 else 0), zb), X, 0.05, 0.012, zt + 0.018 - zb, 'kirec', 'onarkasagsolust')
    # the water step and its falling front
    y.yuz_yon([V(x - 0.05, YC - 0.023, zt), V(x, YC - 0.023, zt), V(x, YC + 0.023, zt), V(x - 0.05, YC + 0.023, zt)], 'su', Z)
    y.yuz_yon([V(x - 0.05, YC - 0.023, zb), V(x - 0.05, YC + 0.023, zb), V(x - 0.05, YC + 0.023, zt), V(x - 0.05, YC - 0.023, zt)], 'su', V(-1, 0))
    if i == 0 and zprev > zt:
        y.yuz_yon([V(x, YC - 0.023, zt), V(x, YC + 0.023, zt), V(x, YC + 0.023, zprev), V(x, YC - 0.023, zprev)], 'su', V(-1, 0))
    zprev = zt
    if zt < ZG + 0.03 or x - 0.1 < 0.34: xs_c = xs_c[:i + 1]; break   # (leave room for the pool short of the river bank)
# the pool below, with a kerb, a little statue and benches
x1p = xs_c[-1] - 0.05
PX0, PX1, PY0, PY1 = max(x1p - 0.26, RIV + 0.11), x1p, YC - 0.12, YC + 0.12   # (clear of the river bank)
kutu(y, V(PX0 - 0.03, PY0 - 0.03, 0), X, PX1 - PX0 + 0.06, PY1 - PY0 + 0.06, ZG + 0.012, 'kirec', 'onarkasagsolust')
havuz(y, PX0, PX1, PY0, PY1, ZG + 0.012, derin=0.03, kenar=0.018, key='mermer')
kutu_merkez(y, ((PX0 + PX1) / 2, (PY0 + PY1) / 2), 0.03, 0.03, 0.04, 'mermer', z0=ZG)
kure(y, ((PX0 + PX1) / 2, (PY0 + PY1) / 2, ZG + 0.05), 0.012, 'bronz', n=10, kat=5)
y.prizma(((PX0 + PX1) / 2, (PY0 + PY1) / 2), 0.004, ZG + 0.04, ZG + 0.062, 'bronz', n=6)

# ---------------------------------------------------------------- the settling tank where the channel leaves the western hill
y.bolum('bati kule')
TX = -X3 - 0.06
zt_ = taban(TX - 0.07, TX + 0.07, -0.065, 0.065) - 0.012
kutu_merkez(y, (TX, 0), 0.14, 0.13, Z3 + 0.06 - zt_, 'kum', z0=zt_, yuzler='arkasagsolust')
# the front wall round the window band (dikdortgen_acik draws the band itself: no face behind its opening)
duz_duvar(y, V(TX - 0.07, -0.065), V(TX + 0.07, -0.065), zt_, Z3 - 0.06, 'kum')
duz_duvar(y, V(TX - 0.07, -0.065), V(TX + 0.07, -0.065), Z3 + 0.04, Z3 + 0.06, 'kum')
kornis(y, TX - 0.07, TX + 0.07, -0.065, 0.065, Z3 + 0.045, 0.012, 0.008, 'kum_acik')
dikdortgen_acik(y, V(TX - 0.07, -0.065), V(TX + 0.07, -0.065), Z3 - 0.06, 0.1, 0.36, 0.64, 0.0, 0.065, ('kum', 'kum_koyu', 'kum_acik', 'ahsap'),
                derin=0.012, cerceve=(0.005, 'kum_acik'))
cati_kirma(y, TX - 0.07, TX + 0.07, -0.065, 0.065, Z3 + 0.06, 0.06, 0.018, 'kiremit', 'kiremit2')
sancak(y, TX - 0.03, 0.03, Z3 + 0.11, boy=0.16, en=0.1, yuk=0.06, aci=math.radians(160))

# ---------------------------------------------------------------- trees and rocks
y.bolum('agaclar')
rng = y.rng
AG = [(-0.9, 0.55, 'servi'), (-0.78, 0.7, 'yaprakli'), (-0.55, -0.6, 'yaprakli'), (-0.4, -0.78, 'servi'), (-0.3, 0.68, 'yaprakli'),
      (0.35, -0.7, 'yaprakli'), (0.55, -0.55, 'servi'), (0.8, -0.75, 'yaprakli'), (1.05, -0.4, 'servi'), (0.22, 0.85, 'yaprakli'),
      (-1.05, -0.45, 'servi'), (-0.95, 0.32, 'yaprakli'), (0.98, 0.26, 'servi'), (0.4, 0.3, 'yaprakli'), (-0.22, -0.4, 'servi'),
      (1.12, 0.84, 'servi'), (0.72, 0.84, 'yaprakli'), (-1.12, 0.78, 'yaprakli')]
for x, yy, tur in AG:
    if not ici(x, yy, 0.16): continue
    b = rng.uniform(0.11, 0.16) if tur == 'servi' else rng.uniform(0.09, 0.12)
    agac(y, x, yy, yuk(x, yy) - 0.004, boy=b, tur='servi' if tur == 'servi' else 'yapraklı', key='boya_yesil' if tur == 'servi' else 'cimen')
# holm oaks and olives scattered over the slopes
n_ag = 0
while n_ag < 34:
    x = rng.uniform(-1.2, 1.2); yy = rng.uniform(-0.92, 0.92)
    h = yuk(x, yy)
    if not ici(x, yy, 0.14) or h < 0.1 or abs(yy) < 0.13 or (x > 0.15 and 0.25 < yy < 0.6) or (abs(x - CX) < 0.1 and yy < 0.6)             or (abs(x + X3 + 0.1) < 0.12 and abs(yy) < 0.12): continue
    agac(y, x, yy, h - 0.004, boy=rng.uniform(0.06, 0.1), key=rng.choice(('cimen', 'boya_yesil')))
    n_ag += 1
for _ in range(14):
    x = rng.choice((-1, 1)) * rng.uniform(0.55, 1.0); yy = rng.uniform(-0.5, 0.5)
    if abs(yy) < 0.12 or (x > 0.15 and 0.25 < yy < 0.6): continue
    kutu_merkez(y, (x, yy), rng.uniform(0.03, 0.06), rng.uniform(0.025, 0.05), rng.uniform(0.015, 0.03), 'kaya_koyu', z0=yuk(x, yy) - 0.01,
                aci=rng.uniform(0, math.pi))

calistir(y, 'lm_sukemeri')
