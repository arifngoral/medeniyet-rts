# Basilica Cistern (lm_yerebatan): the underground cistern shown as a cut-away. A podium whose front part has lost its
# roof and walls in stepped cuts, so the water and the forest of re-used columns (Corinthian, Ionic, coloured marble)
# with brick arches show from above; one row of brick groin vaults still stands, the rest lies under the street with
# its fill shown in section. Two Medusa-head column bases, a wooden walkway, a boat. On the street: the colonnaded
# court of the Stoa Basilica, the entrance kiosk, a fountain, and the end of the aqueduct with its water tower.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from bizans_ek import *

y = Yapi()
ZW = 0.07            # water
ZS = 0.28            # arch springing (top of the capitals)
ZT = 0.44            # street level (podium top)
S = 0.2              # bay
R = S / 2
T_K = 0.022          # arch ring depth
W_K = 0.034          # arch ring width
X_IC = 0.9           # inner faces of the side walls
Y_ON, Y_ARKA = -0.8, 0.4     # inner faces of the front / back walls
X_DIS, Y_DIS0, Y_DIS1 = 1.0, -0.88, 0.95
KOLON_X = [-0.7 + S * i for i in range(8)]
KOLON_Y = [-0.6 + S * j for j in range(5)]
Y_KESIT = 0.0 - W_K / 2      # the section through the fill (the street's front edge)
# side walls cut in steps: (y0, y1, top)
BASAMAK = [(Y_DIS0, -0.6, 0.12), (-0.6, -0.4, 0.2), (-0.4, -0.2, 0.3), (-0.2, Y_KESIT, 0.42), (Y_KESIT, Y_DIS1, ZT)]


# ---------------------------------------------------------------- helpers
def kemer_bant(a, b, zs, t=T_K, w=W_K, key='tugla_roma', n=10):
    """a free brick arch ring from a to b (column centres) springing at zs: intrados, extrados, both faces, feet"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x); m = (a + b) / 2; Rr = L / 2
    ic = [m - e * (Rr * math.cos(math.pi * k / n)) + Z * (zs + Rr * math.sin(math.pi * k / n)) for k in range(n + 1)]
    di = [m - e * ((Rr + t) * math.cos(math.pi * k / n)) + Z * (zs + (Rr + t) * math.sin(math.pi * k / n)) for k in range(n + 1)]
    o1, o2 = nc * (w / 2), -nc * (w / 2)
    mz = m + Z * zs
    for k in range(n):
        y.yuz_yon([ic[k] + o1, ic[k + 1] + o1, ic[k + 1] + o2, ic[k] + o2], key, mz - (ic[k] + ic[k + 1]) / 2)
        y.yuz_yon([di[k] + o1, di[k + 1] + o1, di[k + 1] + o2, di[k] + o2], key, (di[k] + di[k + 1]) / 2 - mz)
        for o, s in ((o1, nc), (o2, -nc)):
            y.yuz_yon([ic[k] + o, ic[k + 1] + o, di[k + 1] + o, di[k] + o], key, s)
    for i in (0, n):
        y.yuz_yon([ic[i] + o1, di[i] + o1, di[i] + o2, ic[i] + o2], key, -Z)


def capraz_tonoz(cx, cy, zs, tv=0.014, key='tugla_roma', nn=6):
    """the top (extrados) of a brick groin vault over the bay centred on (cx, cy): two crossing barrel crests,
    valleys down the diagonals"""
    h = lambda u, v: zs + tv + max(math.sqrt(max(0.0, R * R - u * u)), math.sqrt(max(0.0, R * R - v * v)))
    P = lambda i, j: V(cx - R + 2 * R * i / nn, cy - R + 2 * R * j / nn, h(-R + 2 * R * i / nn, -R + 2 * R * j / nn))
    for i in range(nn):
        for j in range(nn):
            a, b, c, d = P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)
            if (i - nn / 2 + 0.5) * (j - nn / 2 + 0.5) > 0:
                y.yuz_yon([a, b, c], key, Z); y.yuz_yon([a, c, d], key, Z)
            else:
                y.yuz_yon([a, b, d], key, Z); y.yuz_yon([b, c, d], key, Z)


def sarnic_sutun(x, yy, z0, z1, r, key, tur='korint', bas_key='mermer'):
    """a re-used cistern column: a torus base, a plain shaft with entasis, an astragal and a capital: 'korint' (a bell
    wrapped in two rows of closed leaf blocks), 'iyon' (echinus, volute rolls) or 'sepet' (Byzantine impost / basket)"""
    c = (x, yy)
    H = z1 - z0; hc = H * 0.15; zb = z1 - hc
    donel(y, c, [(r * 1.35, z0), (r * 1.35, z0 + 0.008), (r * 1.12, z0 + 0.014), (r, z0 + 0.018)], bas_key, n=8)
    pr = [(r * (1 - 0.12 * t + 0.04 * math.sin(math.pi * t)), z0 + 0.018 + (zb - z0 - 0.018) * t) for t in (0.0, 0.33, 0.66, 1.0)]
    donel(y, c, pr, key, n=10)
    rt = pr[-1][0]
    halka_kornis(y, c, rt, zb - 0.006, 0.006, 0.003, 10, bas_key)
    if tur == 'korint':
        donel(y, c, [(rt, zb), (rt * 1.02, zb + hc * 0.35), (r * 1.12, zb + hc * 0.7), (r * 1.3, zb + hc * 0.82)], bas_key, n=12)
        y.yuz_yon([V(p.x, p.y, zb + hc * 0.82) for p in cokgen(c, r * 1.3, 12)], bas_key, Z)
        for row, (h0, h1, rr) in enumerate(((0.0, 0.45, 1.0), (0.3, 0.75, 1.08))):
            for i in range(8):
                a = TAU * (i + 0.5 * row) / 8
                d = V(math.cos(a), math.sin(a)); tt = V(-d.y, d.x)
                p0 = V(x, yy) + d * (rt * rr * 0.92)
                w = r * 0.38
                L_, R_ = p0 - tt * w + Z * (zb + hc * h0), p0 + tt * w + Z * (zb + hc * h0)
                tip = p0 + d * (r * 0.42) + Z * (zb + hc * h1)
                ic_ = p0 - d * (r * 0.3) + Z * (zb + hc * (h0 + h1) / 2)
                y.yuz_yon([L_, R_, tip], bas_key, d + Z * 0.2)
                y.yuz_yon([L_, tip, ic_], bas_key, -tt); y.yuz_yon([R_, ic_, tip], bas_key, tt)
                y.yuz_yon([L_, ic_, R_], bas_key, -Z)
        kutu_merkez(y, c, r * 2.7, r * 2.7, hc * 0.18, bas_key, z0=zb + hc * 0.82)
    elif tur == 'iyon':
        donel(y, c, [(rt, zb), (r * 1.12, zb + hc * 0.45), (r * 1.12, zb + hc * 0.5)], bas_key, n=12)
        y.yuz_yon([V(p.x, p.y, zb + hc * 0.5) for p in cokgen(c, r * 1.12, 12)], bas_key, Z)
        kutu_merkez(y, c, r * 2.6, r * 2.1, hc * 0.3, bas_key, z0=zb + hc * 0.4)
        kutu_merkez(y, c, r * 2.5, r * 2.5, hc * 0.3, bas_key, z0=zb + hc * 0.7)
        for sx in (-1, 1):
            boru(y, [V(x + sx * r * 1.25, yy - r * 1.15, zb + hc * 0.4), V(x + sx * r * 1.25, yy + r * 1.15, zb + hc * 0.4)], r * 0.42, bas_key, n=8)
    else:   # sepet: an inverted truncated pyramid with a carved band, an impost block
        alt = dikdortgen(x - rt, x + rt, yy - rt, yy + rt, zb)
        ust = dikdortgen(x - r * 1.4, x + r * 1.4, yy - r * 1.4, yy + r * 1.4, zb + hc * 0.78)
        y.serit(alt, ust, bas_key)
        kornis(y, x - r * 1.18, x + r * 1.18, yy - r * 1.18, yy + r * 1.18, zb + hc * 0.36, hc * 0.14, 0.0025, 'tas_koyu')
        kutu_merkez(y, c, r * 3.0, r * 3.0, hc * 0.22, bas_key, z0=zb + hc * 0.78)


def dikdortgen_yuz(x0, x1, y0, y1, z, key, yon=Z):
    y.yuz_yon([V(x0, y0, z), V(x1, y0, z), V(x1, y1, z), V(x0, y1, z)], key, yon)


# ---------------------------------------------------------------- the ground: a block of earth cut open over the cistern
y.bolum('Toprak kesiti ve sarnıç duvarları')
ZK = ZS + R + 0.016          # the vaults' crown: the cistern's brick walls stop here, fill above up to the street
WT = 0.045                   # cistern wall thickness (seen in the section)
HF = 0.12                    # the front wall, cut down to just above the water
# strata from the bottom up: bedrock, clay, rubble fill (with stones), earth, topsoil, the street's paving
TAB = [(0.0, 'kaya_koyu'), (0.06, 'kum_koyu'), (0.15, 'kaya'), (0.27, 'toprak'), (ZT - 0.045, 'toprak_ot'), (ZT - 0.014, 'tas_koyu')]
tg = random.Random(7)


def katman_z(i, u):
    if i == 0: return 0.0
    if i == len(TAB) - 1: return TAB[i][0]
    return TAB[i][0] + 0.009 * math.sin(u * 8.0 + i * 1.7) + 0.005 * math.sin(u * 21.0 + i * 0.6)


def kesit(a, b, z0=0.0, z1=ZT, adim=0.12, tas=True):
    """the earth seen in section on the cut a->b (faces its right) between z0 and z1: wavy strata, stones in the fill"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-4: return
    e = (b - a) / L; nc = V(e.y, -e.x)
    u0 = a.x * 1.3 + a.y * 0.7
    n = max(1, math.ceil(L / adim))
    for k in range(n):
        ua, ub = L * k / n, L * (k + 1) / n
        pa, pb = a + e * ua, a + e * ub
        for i in range(len(TAB)):
            lo = [katman_z(i, u0 + u) for u in (ua, ub)]
            hi = [katman_z(i + 1, u0 + u) if i + 1 < len(TAB) else ZT for u in (ua, ub)]
            lo = [min(max(v, z0), z1) for v in lo]; hi = [min(max(v, z0), z1) for v in hi]
            if hi[0] - lo[0] < 1e-4 and hi[1] - lo[1] < 1e-4: continue
            if hi[0] - lo[0] < 1e-4:
                y.yuz_yon([pa + Z * lo[0], pb + Z * lo[1], pb + Z * hi[1]], TAB[i][1], nc)
            elif hi[1] - lo[1] < 1e-4:
                y.yuz_yon([pa + Z * lo[0], pb + Z * lo[1], pa + Z * hi[0]], TAB[i][1], nc)
            else:
                y.yuz_yon([pa + Z * lo[0], pb + Z * lo[1], pb + Z * hi[1], pa + Z * hi[0]], TAB[i][1], nc)
    if not tas: return
    # stones and broken brick bedded in the rubble fill, boulders in the bedrock, poking out of the cut
    for k in range(int(L / 0.1)):
        u = tg.uniform(0.03, L - 0.05)
        if tg.random() < 0.75:
            zq, w, h, key = tg.uniform(0.165, 0.25), tg.uniform(0.016, 0.034), tg.uniform(0.01, 0.02), tg.choice(('tas_koyu', 'granit', 'tas', 'tugla_roma_koyu'))
        else:
            zq, w, h, key = tg.uniform(0.008, 0.035), tg.uniform(0.03, 0.05), tg.uniform(0.016, 0.026), tg.choice(('kaya_koyu', 'granit_koyu'))
        if zq < z0 or zq + h > z1: continue
        kutu(y, a + e * u + nc * 0.004 + Z * zq, e, w, 0.012, h, key, 'onsagsolust')


def tugla_kesit(a, b, z0, z1):
    """the cistern's brick wall seen in section on the cut a->b, with a mortar joint every few courses"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    y.yuz_yon([a + Z * z0, b + Z * z0, b + Z * z1, a + Z * z1], 'tugla_roma', nc)
    zq = z0 + 0.04
    while zq < z1 - 0.02:
        y.yuz_yon([a + nc * 0.002 + Z * zq, b + nc * 0.002 + Z * zq, b + nc * 0.002 + Z * (zq + 0.007), a + nc * 0.002 + Z * (zq + 0.007)], 'kirec', nc)
        zq += 0.06


XW = X_IC + WT
for sx in (-1, 1):
    xo, xw, xi = sx * X_DIS, sx * XW, sx * X_IC
    # the outer cut (x = +-X_DIS), full height
    kesit(*((V(xo, Y_DIS1), V(xo, Y_DIS0)) if sx < 0 else (V(xo, Y_DIS0), V(xo, Y_DIS1))))
    # the front cut of the side strip: earth, then the cistern wall in section, the fill above it
    p, q = (V(xo, Y_DIS0), V(xw, Y_DIS0)) if sx < 0 else (V(xw, Y_DIS0), V(xo, Y_DIS0))
    kesit(p, q)
    p, q = (V(xw, Y_DIS0), V(xi, Y_DIS0)) if sx < 0 else (V(xi, Y_DIS0), V(xw, Y_DIS0))
    kesit(p, q, 0.0, ZW - 0.03, tas=False)
    tugla_kesit(p, q, ZW - 0.03, ZK)
    kesit(p, q, ZK, ZT, tas=False)
    # the strip's top: the street's paving with a kerb along the pit
    dikdortgen_yuz(min(xo, xi), max(xo, xi), Y_DIS0, Y_KESIT, ZT, 'zemin')
    # the side strip's face over the low front strip (y from the front to the wall), cut through earth
    p, q = (V(xi, Y_DIS0), V(xi, Y_ON - WT)) if sx < 0 else (V(xi, Y_ON - WT), V(xi, Y_DIS0))
    kesit(p, q, HF, ZT)
    p, q = (V(xi, Y_ON - WT), V(xi, Y_ON)) if sx < 0 else (V(xi, Y_ON), V(xi, Y_ON - WT))
    tugla_kesit(p, q, HF, ZK)
    kesit(p, q, ZK, ZT, tas=False)
    # the pit's side: the cistern's brick wall, the fill above it where the vaults are gone
    ai, bi = (V(xi, Y_ON), V(xi, Y_ARKA)) if sx < 0 else (V(xi, Y_ARKA), V(xi, Y_ON))
    duz_duvar(y, ai, bi, ZW - 0.002, ZK, 'tugla_roma')
    ai, bi = (V(xi, Y_ON), V(xi, Y_KESIT)) if sx < 0 else (V(xi, Y_KESIT), V(xi, Y_ON))
    kesit(ai, bi, ZK, ZT, tas=False)
    silme(y, [ai, bi], ZK - 0.012, 0.012, 0.007, 'kirec', 'duz', kapali=False)   # the wall's coping under the fill
# the back cut (y = Y_DIS1), full height
kesit(V(X_DIS, Y_DIS1), V(-X_DIS, Y_DIS1))
# the front: earth in section below the low cut, the cut-down front wall's brick top
kesit(V(-X_IC, Y_DIS0), V(X_IC, Y_DIS0), 0.0, HF)
dikdortgen_yuz(-X_IC, X_IC, Y_DIS0, Y_ON - WT, HF, 'toprak')
dikdortgen_yuz(-X_IC, X_IC, Y_ON - WT, Y_ON, HF, 'tugla_roma_koyu')
duz_duvar(y, V(X_IC, Y_ON), V(-X_IC, Y_ON), ZW - 0.002, HF, 'tugla_roma')
duz_duvar(y, V(-X_IC, Y_ARKA), V(X_IC, Y_ARKA), ZW - 0.002, ZK, 'tugla_roma')
# the water
dikdortgen_yuz(-X_IC, X_IC, Y_ON, Y_ARKA, ZW, 'su')
# wall piers on the side walls (where the arches spring)
for sx in (-1, 1):
    for yy in KOLON_Y:
        kutu_merkez(y, (sx * (X_IC - 0.008), yy), 0.016, 0.05, ZS - ZW + 0.004, 'tugla_roma', z0=ZW - 0.002)
        kutu_merkez(y, (sx * (X_IC - 0.011), yy), 0.024, 0.058, 0.012, 'kirec', z0=ZS - 0.008)

# ---------------------------------------------------------------- the column forest
y.bolum('Sütun ormanı')
TAS = ['mermer', 'mermer', 'granit', 'mermer', 'kirec', 'granit_kizil', 'mermer', 'granit']
MEDUSA = {(1, 0): 'ters', (2, 0): 'yan'}
for i, x in enumerate(KOLON_X):
    for j, yy in enumerate(KOLON_Y):
        if (i, j) in MEDUSA: continue
        q = (i * 3 + j * 5) % 8
        tur = 'iyon' if q == 0 else 'sepet' if q in (3, 6) else 'korint'
        key = TAS[(i * 5 + j * 3) % len(TAS)]
        sarnic_sutun(x, yy, ZW - 0.02, ZS, 0.02, key, tur)


def medusa(cx, cy, z, r, poz):
    """a Medusa head re-used as a column base, its face to -y: poz 'ters' upside down, 'yan' on its side. Built to read
    from afar: a pale face with deep dark eyes, a heavy nose, an open mouth, and a halo of writhing snakes round it"""
    bas = len(y.faces)
    TEN, YILAN = 'tas_acik', 'granit_koyu'
    donel(y, (0, 0), [(0.0, -r), (r * 0.55, -r * 0.86), (r * 0.9, -r * 0.42), (r, 0.0), (r * 0.92, r * 0.42), (r * 0.58, r * 0.84), (0.0, r)], TEN, n=16)
    fy = lambda x, zz: -math.sqrt(max(0.0, r * r - x * x - zz * zz))
    P = lambda x, zz, d=0.0: V(x, fy(x, zz) - d, zz)
    for sx in (-1, 1):
        kure(y, P(sx * r * 0.34, r * 0.1, -r * 0.02), r * 0.17, 'tas_koyu', n=8, kat=4)                                    # eye socket shadow
        kure(y, P(sx * r * 0.34, r * 0.1, r * 0.06), r * 0.12, TEN, n=8, kat=4)                                          # eyeball
        kure(y, P(sx * r * 0.32, r * 0.09, r * 0.15), r * 0.065, 'koyu', n=6, kat=3)                                       # iris
        boru(y, [P(sx * r * 0.12, r * 0.26, r * 0.08), P(sx * r * 0.36, r * 0.3, r * 0.12), P(sx * r * 0.6, r * 0.18, r * 0.06)], r * 0.075, TEN, n=6)   # brow / lid
        boru(y, [P(sx * r * 0.17, r * 0.02, r * 0.08), P(sx * r * 0.36, -r * 0.04, r * 0.1), P(sx * r * 0.53, r * 0.03, r * 0.06)], r * 0.05, TEN, n=5)
        kure(y, P(sx * r * 0.44, -r * 0.22, -r * 0.1), r * 0.22, TEN, n=8, kat=4)                                       # cheeks
        kure(y, P(sx * r * 0.1, -r * 0.15, r * 0.14), r * 0.075, TEN, n=5, kat=3)                                      # nostril wings
    boru(y, [P(0, r * 0.26, r * 0.02), P(0, r * 0.05, r * 0.1), P(0, -r * 0.13, r * 0.18)], r * 0.09, TEN, n=6, r_son=r * 0.13)   # nose
    kure(y, P(0, -r * 0.41, -r * 0.02), r * 0.1, 'koyu', n=8, kat=4)                                                   # the open mouth
    boru(y, [P(-r * 0.25, -r * 0.37, r * 0.03), P(0, -r * 0.3, r * 0.07), P(r * 0.25, -r * 0.37, r * 0.03)], r * 0.055, TEN, n=5)   # lips
    boru(y, [P(-r * 0.21, -r * 0.45, r * 0.03), P(0, -r * 0.53, r * 0.06), P(r * 0.21, -r * 0.45, r * 0.03)], r * 0.06, TEN, n=5)
    kure(y, P(0, -r * 0.68, -r * 0.08), r * 0.2, TEN, n=8, kat=4)                                                      # chin
    # the snakes: a halo round the face, writhing outwards and curling towards the viewer, each with a head
    N = 13
    for k in range(N):
        a = math.radians(-25 + 230 * k / (N - 1))
        d = V(math.cos(a), 0, math.sin(a)); pp = V(-math.sin(a), 0, math.cos(a))
        b = d * (r * 0.8) + V(0, -r * 0.3, 0)
        Ls = r * (0.85 + 0.15 * ((k * 7) % 3))
        ph = k * 1.9
        pts = [b + d * (Ls * s) + pp * (r * 0.2 * math.sin(TAU * s * 1.2 + ph) * s) + V(0, -r * 0.35 * s * s, 0) for s in (0, 0.25, 0.5, 0.75, 1.0)]
        boru(y, pts, r * 0.11, YILAN, n=5, r_son=r * 0.075)
        hd = pts[-1]; dd = (pts[-1] - pts[-2]).normalized()
        kure(y, hd + dd * (r * 0.04), r * 0.12, YILAN, n=5, kat=3)
        boru(y, [hd + dd * (r * 0.08), hd + dd * (r * 0.2) + V(0, -r * 0.04, 0)], r * 0.08, YILAN, n=5, r_son=r * 0.035)
    # two snakes knotted under the chin
    for sx in (-1, 1):
        pts = [V(sx * r * 0.75, -r * 0.35, -r * 0.55), V(sx * r * 0.45, -r * 0.62, -r * 0.82), V(-sx * r * 0.05, -r * 0.7, -r * 0.95),
               V(-sx * r * 0.35, -r * 0.62, -r * 1.12)]
        boru(y, pts, r * 0.1, YILAN, n=6, r_son=r * 0.07)
        kure(y, pts[-1], r * 0.11, YILAN, n=6, kat=3)
    M = ((-1, 0, 0), (0, 0.75, 0), (0, 0, -1)) if poz == 'ters' else ((0, 0, 1), (0, 0.75, 0), (-1, 0, 0))   # (squashed front to back: a mask, not a ball)
    donustur(y, bas, M, (cx, cy, z))


y.bolum('Medusa başları')
RM = 0.05
for (i, j), poz in MEDUSA.items():
    x, yy = KOLON_X[i], KOLON_Y[j]
    zc = ZW + RM * 0.7
    medusa(x, yy, zc, RM, poz)
    kutu_merkez(y, (x, yy + 0.012), 0.062, 0.05, 0.018, 'tas_koyu', z0=zc + RM * 0.82)
    sarnic_sutun(x, yy + 0.012, zc + RM * 0.82 + 0.018, ZS, 0.02, 'mermer', 'korint')

# ---------------------------------------------------------------- arches, the standing vaults, the section through the fill
y.bolum('Tuğla kemerler ve çapraz tonozlar')
xs = [-X_IC] + KOLON_X + [X_IC]
ys = KOLON_Y + [Y_ARKA]
for yy in KOLON_Y:                         # arches along x on every row (wall pier to wall pier)
    for k in range(len(xs) - 1):
        kemer_bant(V(xs[k], yy), V(xs[k + 1], yy), ZS)
for x in KOLON_X:                          # arches along y between the rows (and back to the back wall)
    for k in range(len(ys) - 1):
        kemer_bant(V(x, ys[k]), V(x, ys[k + 1]), ZS)
for sx in (-1, 1):                        # wall arches on the side walls' piers
    for k in range(len(ys) - 1):
        kemer_bant(V(sx * (X_IC - 0.012), ys[k]), V(sx * (X_IC - 0.012), ys[k + 1]), ZS)
# the one standing row of groin vaults, between the last open row and the section
for k in range(len(xs) - 1):
    capraz_tonoz((xs[k] + xs[k + 1]) / 2, KOLON_Y[2] + R, ZS)
# the section: fill and the street's paving above the arch row at y = 0
for k in range(len(xs) - 1):
    xa, xb = xs[k], xs[k + 1]; xm = (xa + xb) / 2
    Rr = (xb - xa) / 2
    alt = [V(xm - (Rr + T_K) * math.cos(math.pi * q / 12) if 0 < q < 12 else (xa if q == 0 else xb), Y_KESIT,
             ZS + (math.sqrt(max(0, (Rr + T_K) ** 2 - Rr * Rr)) if q in (0, 12) else (Rr + T_K) * math.sin(math.pi * q / 12))) for q in range(13)]
    # (clip the ring at the pier lines so neighbouring sections meet)
    alt = [V(max(xa, min(xb, p.x)), p.y, p.z if xa < p.x < xb else ZS + math.sqrt(max(0, (Rr + T_K) ** 2 - Rr * Rr))) for p in alt]
    y.yuz_yon(alt + [V(xb, Y_KESIT, ZT - 0.022), V(xa, Y_KESIT, ZT - 0.022)], 'toprak', -Y)
y.yuz_yon([V(-X_IC, Y_KESIT, ZT - 0.022), V(X_IC, Y_KESIT, ZT - 0.022), V(X_IC, Y_KESIT, ZT), V(-X_IC, Y_KESIT, ZT)], 'tas_koyu', -Y)
# a few stones fallen from the cut into the water
for k, (x, yy, r) in enumerate(((-0.2, -0.72, 0.016), (0.48, -0.7, 0.012), (0.62, -0.28, 0.014))):
    kutu_merkez(y, (x, yy), r * 2, r * 1.6, r, 'tugla_roma_koyu', z0=ZW - 0.004, aci=k)

# ---------------------------------------------------------------- walkway, lanterns, the boat
y.bolum('Yürüme yolu ve kayık')
ZD = ZW + 0.018
YOL = [[V(0.8, 0.3), V(0.8, -0.5), V(-0.82, -0.5)], [V(-0.4, -0.5), V(-0.4, -0.72)]]
for yol in YOL:
    for p, q in zip(yol, yol[1:]):
        e = (q - p).normalized(); nc = V(e.y, -e.x); L = (q - p).length
        o = p - e * 0.025 + nc * 0.025
        kutu(y, o + Z * (ZD - 0.008), e, L + 0.05, 0.05, 0.008, 'ahsap', 'onarkasagsolust')
        n = max(1, int(L / 0.1))
        for k in range(n + 1):
            for s in (-1, 1):
                c = p.lerp(q, k / n) + nc * (s * 0.023)
                if any(abs(c.x - cx) < 0.03 and abs(c.y - cy) < 0.03 for cx in KOLON_X for cy in KOLON_Y): continue
                cubuk(y, c + Z * (ZW - 0.01), c + Z * (ZD + 0.03), 0.005, 'ahsap_koyu')
        for s in (-1, 1):
            boru(y, [p + nc * (s * 0.023) + Z * (ZD + 0.028), q + nc * (s * 0.023) + Z * (ZD + 0.028)], 0.0022, 'ahsap_koyu', n=4)
for x, yy in ((0.8, 0.05), (0.8, -0.3), (0.3, -0.5), (-0.1, -0.5), (-0.4, -0.72)):   # lanterns
    y.prizma((x + 0.025, yy - 0.025), 0.003, ZD, ZD + 0.06, 'demir', n=4)
    kure(y, (x + 0.025, yy - 0.025, ZD + 0.068), 0.008, 'boya_sari', n=8, kat=4)
    y.koni((x + 0.025, yy - 0.025), 0.009, ZD + 0.074, 0.01, 'demir', n=6)
# a small boat moored between the columns
with parca(y, (0.2, -0.71, ZW), 0.0):
    L_, B_ = 0.06, 0.02
    st = [(-L_, 0.0), (-L_ * 0.7, B_ * 0.8), (0.0, B_), (L_ * 0.7, B_ * 0.8), (L_, 0.0)]
    for k in range(len(st) - 1):
        (x0, w0), (x1, w1) = st[k], st[k + 1]
        for s in (-1, 1):
            y.yuz_yon([V(x0, s * w0, -0.004), V(x1, s * w1, -0.004), V(x1, s * w1, 0.012), V(x0, s * w0, 0.012)], 'ahsap', V(0, s, 0.1))
        y.yuz_yon([V(x0, -w0, 0.004), V(x1, -w1, 0.004), V(x1, w1, 0.004), V(x0, w0, 0.004)], 'ahsap_koyu', Z)
        for s in (-1, 1):   # inner sides above the bottom boards
            y.yuz_yon([V(x0, s * w0 * 0.85, 0.004), V(x1, s * w1 * 0.85, 0.004), V(x1, s * w1 * 0.85, 0.012), V(x0, s * w0 * 0.85, 0.012)], 'ahsap_acik', V(0, -s, 0))
            y.yuz_yon([V(x0, s * w0, 0.012), V(x1, s * w1, 0.012), V(x1, s * w1 * 0.85, 0.012), V(x0, s * w0 * 0.85, 0.012)], 'ahsap_koyu', Z)
    for xq in (-0.02, 0.02):
        kutu_merkez(y, (xq, 0), 0.008, B_ * 1.7, 0.003, 'ahsap_acik', z0=0.009)
    cubuk(y, V(0.0, -0.01, 0.012), V(-0.05, -0.05, -0.002), 0.003, 'ahsap_acik')

# ---------------------------------------------------------------- the street: paving, the Stoa Basilica court
y.bolum('Bazilika avlusu (revaklar)')
dikdortgen_yuz(-X_DIS, X_DIS, Y_KESIT, Y_DIS1, ZT, 'zemin')
silme(y, [V(X_DIS, Y_KESIT), V(-X_DIS, Y_KESIT)], ZT - 0.006, 0.008, 0.006, 'kirec', 'duz', kapali=False)   # the kerb along the cut
DR = 0.12      # portico depth
HR = 0.15      # arcade height


def revak(a, b, n):
    """a portico: an arcade on Corinthian columns facing the right of a->b, a back wall DR behind (its outer face on
    the podium's edge), end walls, and a tile lean-to roof falling towards the court"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x); L = (b - a).length
    arkad(y, a, b, n, ZT, HR, en=0.72, ust=0.022, sivri=0.0, derin=DR - 0.02, renk=('kirec', 'tas_koyu', 'mermer', 'kirec'),
          cerceve=(0.006, ['kirec', 'tugla_roma']), sutun_key='mermer', sutun_tur='iyon', sutun_r=0.0095, sutun_yiv=12)
    ab, bb = a - nc * DR, b - nc * DR
    duz_duvar(y, bb, ab, ZT, ZT + HR + 0.05, 'kirec')                     # the outer back face
    serit_tas(y, bb, ab, ZT, 0.0, L, 0.05, 0.016, 'tugla_roma', 0.003)
    serit_tas(y, bb, ab, ZT, 0.0, L, 0.12, 0.016, 'tugla_roma', 0.003)
    for p, pb, s in ((a, ab, -1), (b, bb, 1)):                           # end walls
        y.yuz_yon([p + Z * ZT, pb + Z * ZT, pb + Z * (ZT + HR + 0.05), p + Z * (ZT + HR)], 'kirec', e * s)
    kornis(y, *(lambda xs_, ys_: (min(xs_), max(xs_), min(ys_), max(ys_)))([a.x, b.x, ab.x, bb.x], [a.y, b.y, ab.y, bb.y]), ZT + HR - 0.01, 0.01, 0.006,
           'kirec', 'duz')
    # the lean-to: from the back wall top down over the arcade, a little past it
    z1, z0 = ZT + HR + 0.06, ZT + HR + 0.002
    fa, fb = a + nc * 0.025 - e * 0.01, b + nc * 0.025 + e * 0.01
    ba, bb2 = ab - nc * 0.012 - e * 0.01, bb - nc * 0.012 + e * 0.01
    zf = z0 - (z1 - z0) * 0.025 / DR
    m = max(1, int(L / 0.15))
    for k in range(m):
        t0, t1 = k / m, (k + 1) / m
        for j in range(3):
            u0, u1 = j / 3, (j + 1) / 3
            P = lambda t, u: fa.lerp(fb, t).lerp(ba.lerp(bb2, t), u) + Z * (zf + (z1 + 0.002 - zf) * u)
            y.yuz_yon([P(t0, u0), P(t1, u0), P(t1, u1), P(t0, u1)], 'kiremit' if j % 2 == 0 else 'kiremit2', Z + nc * 0.3)
    P0 = lambda t, u: fa.lerp(fb, t).lerp(ba.lerp(bb2, t), u) + Z * (zf + (z1 + 0.002 - zf) * u - 0.006)
    y.yuz_yon([P0(0, 0), P0(1, 0), P0(1, 1), P0(0, 1)], 'ahsap_koyu', -Z)   # (the roof's underside)
    # fascia, the under-eave and the ends of the roof
    y.yuz_yon([fa + Z * zf, fb + Z * zf, fb + Z * (zf - 0.008), fa + Z * (zf - 0.008)], 'ahsap_koyu', nc)
    y.yuz_yon([fa + Z * (zf - 0.008), fb + Z * (zf - 0.008), b + Z * (ZT + HR), a + Z * (ZT + HR)], 'ahsap_koyu', -Z)
    for p, q, s in ((fa, ba, -1), (fb, bb2, 1)):
        y.yuz_yon([p + Z * zf, q + Z * (z1 + 0.002), q + Z * (ZT + HR + 0.05), p + Z * (zf - 0.008)], 'ahsap_koyu', e * s)
    cubuk(y, ba + Z * (z1 + 0.006), bb2 + Z * (z1 + 0.006), 0.012, 'kiremit2')
    y.yuz_yon([ab + Z * (ZT + HR + 0.05), bb + Z * (ZT + HR + 0.05), bb2 + Z * (z1 + 0.002), ba + Z * (z1 + 0.002)], 'kirec', -nc + Z)


revak(V(-X_DIS + DR, 0.08), V(-X_DIS + DR, 0.76), 4)            # left (faces +x)
revak(V(-0.08, Y_DIS1 - DR), V(X_DIS - DR, Y_DIS1 - DR), 6)      # back (faces -y)
revak(V(X_DIS - DR, Y_DIS1 - DR), V(X_DIS - DR, 0.3), 4)         # right (faces -x)

# the court: a fountain (phiale) and cypresses
y.bolum('Avlu: şadırvan ve serviler')
FC = (0.28, 0.46)
y.prizma(FC, 0.1, ZT, ZT + 0.03, 'mermer', n=8, kat=math.pi / 8, ust=False)
y.prizma(FC, 0.088, ZT + 0.03, ZT + 0.018, 'mermer', n=8, kat=math.pi / 8, ust=False)
y.yuz_yon([V(p.x, p.y, ZT + 0.03) for p in cokgen(FC, 0.1, 8, math.pi / 8)], 'mermer', Z)
y.yuz_yon([V(p.x, p.y, ZT + 0.0305) for p in cokgen(FC, 0.088, 8, math.pi / 8)], 'su', Z)
donel(y, FC, [(0.02, ZT + 0.03), (0.012, ZT + 0.06), (0.03, ZT + 0.07), (0.032, ZT + 0.075), (0.0, ZT + 0.075)], 'mermer', n=12)
kure(y, (FC[0], FC[1], ZT + 0.085), 0.012, 'bronz', n=8, kat=4)
for x, yy in ((-0.7, 0.12), (-0.62, 0.66), (0.62, 0.62), (-0.25, 0.3)):
    agac(y, x, yy, ZT, 0.2, 'servi', 'yesil_koyu')
for x, yy in ((-0.1, 0.12), (0.62, 0.12)):
    kutu_merkez(y, (x, yy), 0.04, 0.04, 0.012, 'mermer', z0=ZT)
    sarnic_sutun(x, yy, ZT + 0.012, ZT + 0.13, 0.009, 'granit_kizil', 'korint')

# ---------------------------------------------------------------- the entrance kiosk
y.bolum('Giriş köşkü')
KC = (0.78, 0.15)
KW = 0.19
kk = dikdortgen(KC[0] - KW / 2, KC[0] + KW / 2, KC[1] - KW / 2, KC[1] + KW / 2)
for i in range(4):
    almasik(y, kk[i], kk[(i + 1) % 4], ZT, 0.17, 1, en=0.5 if i == 0 else 0.42, v0=0.0 if i == 0 else 0.05, kapi_bay=0 if i == 0 else None,
            ust=0.03, k_say=10)
for p in kk:
    kutu_merkez(y, (p.x, p.y), 0.028, 0.028, 0.18, 'kirec', z0=ZT)
kornis(y, kk[0].x, kk[1].x, kk[0].y, kk[2].y, ZT + 0.165, 0.016, 0.012, 'kirec', 'tac')
dikdortgen_yuz(kk[0].x, kk[1].x, kk[0].y, kk[2].y, ZT + 0.181, 'kursun')
tk = biz_kubbe(y, KC, 0.075, ZT + 0.181, kasnak_h=0.045, n_pencere=8, kubbe_h=0.065)
# steps down from the kiosk's door to the court
for k in range(2):
    kutu(y, V(KC[0] - 0.05, KC[1] - KW / 2 - 0.02 * (k + 1), ZT), X, 0.1, 0.02 * (k + 1) + 0.001, 0.012 * (2 - k), 'mermer', 'onsagsolust')

# ---------------------------------------------------------------- the aqueduct's end and the water tower
y.bolum('Su kemeri ucu ve su kulesi')
AY = Y_DIS1 - 0.085        # the aqueduct's front face
AX0, AX1 = -X_DIS, -0.32
t1 = kemer_dizisi(y, V(AX0, AY), V(AX1, AY), 3, ZT, 0.24, 0.07, ('kirec', 'tas_koyu', 'tas_acik', 'tas_koyu'), en=0.6, ust=0.045, acik=True, taban=False)
for zb in (0.2,):
    serit_tas(y, V(AX0, AY), V(AX1, AY), ZT, 0.0, AX1 - AX0, zb + 0.02, 0.016, 'tugla_roma', 0.003)
    serit_tas(y, V(AX1, AY + 0.07), V(AX0, AY + 0.07), ZT, 0.0, AX1 - AX0, zb + 0.02, 0.016, 'tugla_roma', 0.003)
kornis(y, AX0, AX1, AY, AY + 0.07, t1 - 0.01, 0.012, 0.008, 'kirec', 'duz')
t2 = kemer_dizisi(y, V(AX0, AY + 0.006), V(AX1, AY + 0.006), 6, t1 + 0.002, 0.17, 0.058, ('tas', 'tas_koyu', 'tas_acik', 'tas_koyu'), en=0.55, ust=0.04,
                  acik=True)
serit_tas(y, V(AX0, AY + 0.006), V(AX1, AY + 0.006), t1 + 0.002, 0.0, AX1 - AX0, 0.136, 0.014, 'tugla_roma', 0.003)
# the water channel on top: side walls and cover slabs
for k in range(8):
    x0 = AX0 + (AX1 - AX0) * k / 8
    kutu(y, V(x0 + 0.002, AY + 0.002, t2), X, (AX1 - AX0) / 8 - 0.004, 0.062, 0.03, 'kirec', 'onarkasagsolust' if k else 'onarkasagsolust')
# the water tower (castellum): banded, arched windows, cornices, a little dome, the team banner
CX0, CX1, CY0, CY1 = -0.33, -0.09, 0.73, Y_DIS1
zc = almasik_kutu(y, CX0, CX1, CY0, CY1, ZT, 0.42, (2, 2, 2, 2), ust='kursun', kapilar=(None, None, None, None), en=0.38, v0=0.24, k_say=8)
for p in dikdortgen(CX0, CX1, CY0, CY1):
    kutu_merkez(y, (p.x, p.y), 0.03, 0.03, 0.42, 'kirec', z0=ZT)
kornis(y, CX0, CX1, CY0, CY1, ZT + 0.2, 0.012, 0.008, 'kirec', 'duz')
tc = biz_kubbe(y, ((CX0 + CX1) / 2, (CY0 + CY1) / 2), 0.085, zc, kasnak_h=0.05, n_pencere=8, kubbe_h=0.075)
sancak(y, CX1 - 0.02, CY0 + 0.02, zc, boy=0.25, en=0.13, yuk=0.08, aci=-math.pi * 0.2)
# the spout on its front: a bronze lion head pouring into a half-round basin (nymphaeum)
SC = V((CX0 + CX1) / 2, CY0)
boru(y, [SC + Z * (ZT + 0.11), SC + Z * (ZT + 0.11) - Y * 0.03], 0.01, 'bronz', n=8, r_son=0.008)
kure(y, SC + Z * (ZT + 0.115) - Y * 0.012, 0.016, 'bronz', n=10, kat=5)
boru(y, [SC - Y * 0.032 + Z * (ZT + 0.106), SC - Y * 0.045 + Z * (ZT + 0.08), SC - Y * 0.05 + Z * (ZT + 0.03)], 0.006, 'su', n=6)
BC = (SC.x, CY0 - 0.0)
pts = [V(BC[0] + 0.09 * math.cos(math.pi + math.pi * k / 10), BC[1] + 0.09 * math.sin(math.pi + math.pi * k / 10)) for k in range(11)]
for p, q in zip(pts, pts[1:]):
    duz_duvar(y, p, q, ZT, ZT + 0.03, 'mermer')
    duz_duvar(y, q + (V(BC[0], BC[1]) - q) * 0.15, p + (V(BC[0], BC[1]) - p) * 0.15, ZT + 0.012, ZT + 0.03, 'mermer')
    y.yuz_yon([p + Z * (ZT + 0.03), q + Z * (ZT + 0.03), q + (V(BC[0], BC[1]) - q) * 0.15 + Z * (ZT + 0.03), p + (V(BC[0], BC[1]) - p) * 0.15 + Z * (ZT + 0.03)],
              'mermer', Z)
y.yuz_yon([V(p.x, p.y, ZT + 0.022) for p in [V(BC[0], BC[1])] + [q + (V(BC[0], BC[1]) - q) * 0.15 for q in pts]], 'su', Z)

# ---------------------------------------------------------------- finishing: railings round the pit, paths, people
y.bolum('Korkuluklar, yollar, insanlar')
# marble railings along the pit's long sides, on the street strips
for sx in (-1, 1):
    xb = sx * (X_IC + 0.014)
    n = 9
    for k in range(n + 1):
        yy = Y_DIS0 + 0.02 + (Y_KESIT + 0.012 - Y_DIS0 - 0.02) * k / n
        kutu_merkez(y, (xb, yy), 0.014, 0.014, 0.045, 'mermer', z0=ZT)
    kutu_merkez(y, (xb, (Y_DIS0 + Y_KESIT) / 2 + 0.016), 0.016, Y_KESIT - Y_DIS0 - 0.008, 0.008, 'mermer', z0=ZT + 0.045)
    kutu_merkez(y, (xb, (Y_DIS0 + Y_KESIT) / 2 + 0.016), 0.006, Y_KESIT - Y_DIS0 - 0.008, 0.006, 'mermer', z0=ZT + 0.008)
for x, yy, a, key in ((-0.955, -0.42, 0.1, 'kirmizi'), (-0.958, -0.36, -0.3, 'kum_koyu'), (0.955, -0.62, math.pi, 'ahsap_acik')):
    insan(y, x, yy, ZT, key, s=1.5, aci=a, kol=0.0)
# a marble balustrade along the edge of the cut
YB = Y_KESIT + 0.012
n = 18
for k in range(n + 1):
    x = -X_IC + 2 * X_IC * k / n
    if 0.66 < x < 0.9: continue
    kutu_merkez(y, (x, YB), 0.014, 0.014, 0.045, 'mermer', z0=ZT)
for x0, x1 in ((-X_IC, 0.66),):
    kutu(y, V(x0, YB - 0.008, ZT + 0.045), X, x1 - x0, 0.016, 0.008, 'mermer')
    kutu(y, V(x0, YB - 0.003, ZT + 0.008), X, x1 - x0, 0.006, 0.006, 'mermer')
# marble paths across the court
for x0, x1, y0, y1 in ((0.24, 0.32, 0.05, 0.8), (-0.86, 0.86, 0.42, 0.5), (0.32, 0.72, 0.1, 0.17)):
    dikdortgen_yuz(x0, x1, y0, y1, ZT + 0.0015, 'mermer')
# people on the street
for x, yy, a, key, kol in ((0.05, 0.3, 0.6, 'kirmizi', 0.0), (0.12, 0.27, 3.5, 'kum_koyu', 0.5), (0.5, 0.42, 1.8, 'ahsap_acik', 0.0),
                           (-0.45, 0.55, -0.6, 'boya_kirmizi', 0.0), (0.7, 0.04, -1.4, 'kirmizi', 0.6), (-0.3, 0.12, 2.2, 'kum_koyu', 0.0)):
    insan(y, x, yy, ZT, key, s=1.5, aci=a, kol=kol)
# water jars by the nymphaeum
for k in range(2):
    amfora(y, -0.06 + 0.03 * k, 0.62, ZT, 0.9, kulp=False, n=8)

calistir(y, 'lm_yerebatan')
