# The Theodosian Land Walls (lm_theodosius), a corner of the triple line turned round the plot: the water-filled moat
# with its crenellated breastwork and cross-dams, the low outer wall with small square towers, the terraces, the tall
# inner wall in limestone with brick bands and its big square and octagonal towers; in the front run the Golden Gate
# (a three-arched marble triumphal gate between two marble towers, gilded doors, Theodosius' elephant quadriga on top)
# with its outer gate and bridge; behind the walls a corner of the city: a domed church, houses, the Mese, and the
# Column of Arcadius.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from bizans_ortak import *

y = Yapi(tohum=3)
R = random.Random(5)

Z0 = 0.06                       # ground (city, terraces)
ZW, ZM = 0.026, 0.012           # moat water, moat floor
XI, YI = -0.67, -0.47           # the inner wall's outer face: the left run (x = XI) and the front run (y = YI)
XE, YE = 1.13, 0.93             # where the runs leave the plot
XG = 0.25                       # the Golden Gate
HI, HO = 0.3, 0.14              # inner, outer wall heights
DO, DB, DC, DP = 0.16, 0.28, 0.42, 0.48   # outer wall face, breastwork / scarp, counterscarp, plot edge (outward from the inner wall)


def P(d):
    """the L line d outward of the inner wall: down the left run, round the corner, along the front (outer side right)"""
    return [V(XI - d, YE), V(XI - d, YI - d), V(XE, YI - d)]


def serit(d0, d1, z, key):
    a, b = P(d0), P(d1)
    for i in range(2):
        y.yuz_yon([a[i] + Z * z, a[i + 1] + Z * z, b[i + 1] + Z * z, b[i] + Z * z], key, Z)


def bant_yol(yol, z0, H, adim=0.07, h=0.018, key='tugla_roma', ic=None):
    """brick bands along a polyline's outer face (and, ic = thickness, its inner face)"""
    for i in range(len(yol) - 1):
        a, b = yol[i], yol[i + 1]
        L = (b - a).length
        for zb, hb in bantlar(H, adim, h):
            serit_tas(y, a, b, z0, 0, L, zb, hb, key)
    if ic:
        iy = disa(yol, -ic, False)
        for i in range(len(iy) - 1):
            a, b = iy[i + 1], iy[i]
            L = (b - a).length
            for zb, hb in bantlar(H, adim, h):
                serit_tas(y, a, b, z0, 0, L, zb, hb, key)


# ---------------------------------------------------------------- ground, moat
y.bolum('Zemin ve hendek')
serit(DC, DP, Z0, 'cimen_kuru')
serit(DB, DC, ZW, 'su')
serit(DO, DB - 0.025, Z0, 'cimen')
serit(0.0, DO - 0.04, Z0, 'cimen')
y.yuz_yon([V(XI + 0.07, YI + 0.07, Z0), V(XE, YI + 0.07, Z0), V(XE, YE, Z0), V(XI + 0.07, YE, Z0)], 'toprak_ot', Z)
pd = P(DP)
for i in range(2):
    duz_duvar(y, pd[i], pd[i + 1], 0, Z0, 'tas_koyu')
pc = P(DC)
for i in range(2):   # counterscarp (facing the moat)
    duz_duvar(y, pc[i + 1], pc[i], ZM, Z0, 'kirec')
pb = P(DB)
for i in range(2):   # scarp under the breastwork
    duz_duvar(y, pb[i], pb[i + 1], ZM, Z0, 'kirec')
    L = (pb[i + 1] - pb[i]).length
    serit_tas(y, pb[i], pb[i + 1], ZM, 0, L, 0.022, 0.012, 'tugla_roma')
# the cut ends of the plot (moat in section)
y.yuz_yon([V(XE, YI - DP, 0), V(XE, YE, 0), V(XE, YE, Z0), V(XE, YI - DB, Z0), V(XE, YI - DB, ZW), V(XE, YI - DC, ZW), V(XE, YI - DC, Z0),
           V(XE, YI - DP, Z0)], 'tas_koyu', X)
y.yuz_yon([V(XI - DP, YE, 0), V(XE, YE, 0), V(XE, YE, Z0), V(XI + 0.0, YE, Z0), V(XI - DB, YE, Z0), V(XI - DB, YE, ZW), V(XI - DC, YE, ZW),
           V(XI - DC, YE, Z0), V(XI - DP, YE, Z0)], 'tas_koyu', Y)
# cross-dams in the moat
for a, b in ((V(XI - DB, 0.25), V(XI - DC, 0.25)), (V(-0.2, YI - DB), V(-0.2, YI - DC)), (V(0.75, YI - DB), V(0.75, YI - DC))):
    e = (b - a).normalized()
    kutu(y, a - Z.cross(e) * 0.012 + Z * ZM, e, (b - a).length, 0.024, Z0 - ZM - 0.006, 'kirec', 'onarkaust')
    for t in (0.33, 0.66):   # little turrets on the dams
        p = a.lerp(b, t)
        y.prizma((p.x, p.y), 0.016, Z0 - 0.006, Z0 + 0.03, 'kirec', n=8, ust=True)

# ---------------------------------------------------------------- breastwork
y.bolum('Hendek göğüs duvarı')
for yol in ([V(XI - DB, YE), V(XI - DB, YI - DB), V(XG - 0.06, YI - DB)], [V(XG + 0.06, YI - DB), V(XE, YI - DB)]):
    sur(y, yol, Z0, 0.028, 0.026, 'kirec', mazgal_h=0.016, parapet_h=0.006, ust_key='kirec')

# ---------------------------------------------------------------- the outer wall
y.bolum('Dış sur ve kuleleri')
OY = YI - DO
for yol in ([V(XI - DO, YE), V(XI - DO, OY), V(XG - 0.08, OY)], [V(XG + 0.08, OY), V(XE, OY)]):
    sur(y, yol, Z0, HO, 0.04, 'kirec', mazgal_h=0.022, parapet_h=0.012, ust_key='zemin')
    bant_yol(yol, Z0, HO, 0.06, 0.014, ic=0.04)


def dis_kule(c, yon):
    """a small square tower of the outer wall, projecting outward (yon: the outward unit vector)"""
    e = V(-yon.y, yon.x)
    w = 0.085
    o = V(c[0], c[1]) - e * (w / 2) + yon * 0.055
    k = [o, o - e * 0.0 + e * w, o + e * w - yon * 0.1, o - yon * 0.1]
    k = [k[1], k[0], k[3], k[2]] if (k[1] - k[0]).cross(k[3] - k[0]).z < 0 else k
    k = dikdortgen(min(p.x for p in k), max(p.x for p in k), min(p.y for p in k), max(p.y for p in k))
    H = HO + 0.07
    for i in range(4):
        almasik(y, k[i], k[(i + 1) % 4], Z0, H, 1, en=0.28, v0=H * 0.6, ust=0.03, derin=0.014, bant_list=bantlar(H, 0.06, 0.014), cer=None)
    parapet(y, k, Z0 + H, 0.01, 0.02, 0.014, 'kirec')
    y.yuz_yon([V(p.x, p.y, Z0 + H + 0.0005) for p in disa(k, -0.014)], 'zemin', Z)


for yy in (-0.27, 0.12, 0.52):
    dis_kule((XI - DO, yy), V(-1, 0))
for xx in (-0.48, -0.14, 0.66, 1.0):
    dis_kule((xx, OY), V(0, -1))
dis_kule((XI - DO - 0.02, OY - 0.02), V(-0.7, -0.7).normalized())

# the outer gate and the bridge over the moat
y.bolum('Dış kapı ve köprü')
gx0, gx1 = XG - 0.08, XG + 0.08
gy0, gy1 = OY - 0.05, OY + 0.04
y.kemerli(V(gx0, gy0), V(gx1, gy0), Z0, HO + 0.04, ('kirec', 'tas_koyu', 'mermer', 'koyu'), v0=0, en=0.5, ust=0.06, derin=0.03, k_say=8,
          cerceve=(0.01, ['mermer', 'tugla_roma']))
y.kemerli(V(gx1, gy1), V(gx0, gy1), Z0, HO + 0.04, ('kirec', 'tas_koyu', 'mermer', 'koyu'), v0=0, en=0.5, ust=0.06, derin=0.03, k_say=8)
duz_duvar(y, V(gx1, gy0), V(gx1, gy1), Z0, Z0 + HO + 0.04, 'kirec')
duz_duvar(y, V(gx0, gy1), V(gx0, gy0), Z0, Z0 + HO + 0.04, 'kirec')
gk = dikdortgen(gx0, gx1, gy0, gy1)
bant_yol(gk + [gk[0]], Z0, HO + 0.04, 0.06, 0.014)
parapet(y, gk, Z0 + HO + 0.04, 0.012, 0.022, 0.014, 'kirec')
y.yuz_yon([V(p.x, p.y, Z0 + HO + 0.0405) for p in disa(gk, -0.014)], 'zemin', Z)
# bridge
by0, by1 = YI - DC - 0.004, YI - DB + 0.004
kutu(y, V(XG - 0.05, by0, ZM), X, 0.1, by1 - by0, Z0 - ZM, 'kirec', 'sagsol')
y.yuz_yon([V(XG - 0.05, by0, Z0 + 0.001), V(XG + 0.05, by0, Z0 + 0.001), V(XG + 0.05, by1, Z0 + 0.001), V(XG - 0.05, by1, Z0 + 0.001)], 'zemin', Z)
for sx in (-1, 1):
    kutu(y, V(XG + sx * 0.05 - (0.008 if sx > 0 else 0), by0, Z0), X, 0.008, by1 - by0, 0.016, 'kirec')
    # a dark arch under the deck on each side
    xs = XG + sx * 0.0505
    pts = [V(xs, by0 + 0.03 + 0.08 * (0.5 - 0.5 * math.cos(math.pi * k / 8)), ZW + 0.002 + 0.024 * math.sin(math.pi * k / 8)) for k in range(9)]
    y.yuz_yon(pts, 'koyu', V(sx, 0, 0))

# ---------------------------------------------------------------- the inner wall
y.bolum('İç sur (almaşık)')
for yol in ([V(XI, YE), V(XI, YI), V(XG - 0.35, YI)], [V(XG + 0.35, YI), V(XE, YI)]):
    sur(y, yol, Z0, HI, 0.07, 'kirec', mazgal_h=0.028, parapet_h=0.016, ust_key='zemin')
    bant_yol(yol, Z0, HI, 0.075, 0.022, ic=0.07)
    silme(y, yol, Z0, 0.016, 0.01, 'kirec', 'kaide', kapali=False)
# stairs up the inside of the wall
for a, yon in ((V(XI + 0.07 + 0.03, 0.1), math.pi / 2), (V(0.7, YI + 0.07 + 0.03), 0.0), (V(-0.3, YI + 0.07 + 0.03), math.pi)):
    merdiven(y, a, yon, 0.05, Z0, Z0 + HI, n=12, key='kirec', yanlik='tugla_roma')


def ic_kule(c, yon, tur='kare', H=0.46, w=0.15, sancakli=False):
    """a big tower of the inner wall projecting outward (yon): banded limestone, arched windows above, a merloned top"""
    yon = Vector(yon).normalized()
    cx, cy = c[0] + yon.x * 0.03, c[1] + yon.y * 0.03
    if tur == 'kare':
        k = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
    else:
        k = cokgen((cx, cy), w * 0.56, 8, math.pi / 8)
    n = len(k)
    for i in range(n):
        a, b = k[i], k[(i + 1) % n]
        m = (a + b) / 2 - V(cx, cy)
        dis_ = m.dot(yon) > -0.01
        almasik(y, a, b, Z0, H, 1 if dis_ else 0, en=0.3 if tur == 'kare' else 0.42, v0=H * 0.62, ust=0.045, derin=0.016,
                bant_list=bantlar(H, 0.075, 0.022))
        if dis_ and tur == 'kare':   # a lower slit
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            yarik(y, a + Z * Z0, e, nn, (b - a).length / 2 - 0.006, H * 0.3, 0.012, H * 0.12, 'koyu')
    silme(y, k, Z0, 0.016, 0.01, 'kirec', 'kaide')
    silme(y, k, Z0 + H - 0.022, 0.022, 0.01, 'tugla_roma', 'kaba')
    parapet(y, k, Z0 + H, 0.012, 0.028, 0.016, 'kirec')
    y.yuz_yon([V(p.x, p.y, Z0 + H + 0.0005) for p in disa(k, -0.016)], 'zemin', Z)
    if sancakli:
        sancak(y, cx, cy, Z0 + H, boy=0.24, en=0.13, yuk=0.075, aci=math.pi * 0.8)
    return k


y.bolum('İç sur kuleleri')
ic_kule((XI, YI), V(-1, -1), 'sekiz', H=0.5, w=0.2, sancakli=True)
for k, yy in enumerate((-0.08, 0.32, 0.72)):
    ic_kule((XI, yy), V(-1, 0), 'sekiz' if k == 1 else 'kare')
for k, xx in enumerate((-0.32, 0.92)):
    ic_kule((xx, YI), V(0, -1), 'kare' if k == 0 else 'sekiz')
# soldiers on the walls
for x, yy, z in ((XI + 0.035, -0.28, Z0 + HI), (XI + 0.035, 0.5, Z0 + HI), (-0.5, YI + 0.035, Z0 + HI), (0.75, YI + 0.035, Z0 + HI),
                 (XI - DO + 0.02, 0.3, Z0 + HO), (-0.3, OY + 0.02, Z0 + HO), (0.5, OY + 0.02, Z0 + HO)):
    insan(y, x, yy, z, 'boya_kirmizi', 1.35, aci=-math.pi / 2, sapka='demir')

# ---------------------------------------------------------------- the Golden Gate
y.bolum('Altınkapı')
GY0, GY1 = YI - 0.065, YI + 0.07
GH = 0.35
bays = ((XG - 0.26, XG - 0.11, 0.56, 0.12, 'ahsap'), (XG - 0.11, XG + 0.11, 0.66, 0.07, 'altin'), (XG + 0.11, XG + 0.26, 0.56, 0.12, 'ahsap'))
for x0, x1, en, ust, kk in bays:
    y.kemerli(V(x0, GY0), V(x1, GY0), Z0, GH, ('mermer', 'tas_koyu', 'mermer', kk), v0=0.0, en=en, ust=ust, derin=0.045, k_say=10,
              cerceve=(0.012, ['mermer', 'tas_acik']))
    y.kemerli(V(x1, GY1), V(x0, GY1), Z0, GH, ('mermer', 'tas_koyu', 'mermer', kk), v0=0.0, en=en, ust=ust, derin=0.045, k_say=10)
for xx in (XG - 0.26, XG - 0.11, XG + 0.11, XG + 0.26):   # pilasters
    kutu(y, V(xx - 0.011, GY0, Z0), X, 0.022, -0.01, GH - 0.03, 'mermer', 'arkasagsol')
    kutu(y, V(xx - 0.016, GY0 + 0.002, Z0 + GH - 0.03), X, 0.032, -0.016, 0.02, 'mermer', 'arkasagsolust')
gk = dikdortgen(XG - 0.26, XG + 0.26, GY0, GY1)
silme(y, gk, Z0, 0.02, 0.012, 'mermer', 'kaide')
silme(y, gk, Z0 + GH - 0.016, 0.022, 0.016, 'mermer', 'tac')
# the wall tops between the two faces (the gap under the attic showed the back wall's inside)
y.yuz_yon([V(XG - 0.26, GY0, Z0 + GH), V(XG + 0.26, GY0, Z0 + GH), V(XG + 0.26, GY1, Z0 + GH), V(XG - 0.26, GY1, Z0 + GH)], 'mermer', Z)
# gilded wreaths in the spandrels over the side arches, victories over the middle one (both faces)
for yy_, nn_ in ((GY0 - 0.0015, -Y), (GY1 + 0.0015, Y)):
    for xx in (XG - 0.185, XG + 0.185):
        c = V(xx, yy_, Z0 + GH - 0.06)
        y.yuz_yon([c + V(0.022 * math.cos(TAU * k / 14), 0, 0.022 * math.sin(TAU * k / 14)) for k in range(14)], 'bronz', nn_)
        y.yuz_yon([c + nn_ * 0.001 + V(0.013 * math.cos(TAU * k / 12), 0, 0.013 * math.sin(TAU * k / 12)) for k in range(12)], 'mermer', nn_)
    for sx in (-1, 1):   # gilded crosses either side of the middle arch's crown
        c = V(XG + sx * 0.078, yy_, Z0 + GH - 0.052)
        y.yuz_yon([c + V(-0.003, 0, -0.018), c + V(0.003, 0, -0.018), c + V(0.003, 0, 0.018), c + V(-0.003, 0, 0.018)], 'altin', nn_)
        y.yuz_yon([c + nn_ * 0.0006 + V(-0.012, 0, 0.003), c + nn_ * 0.0006 + V(0.012, 0, 0.003), c + nn_ * 0.0006 + V(0.012, 0, 0.009),
                   c + nn_ * 0.0006 + V(-0.012, 0, 0.009)], 'altin', nn_)
# attic over the arches: pilaster panels and a bronze-lettered inscription band, and the elephant quadriga
ZA = Z0 + GH + 0.006
kutu(y, V(XG - 0.24, GY0 + 0.004, Z0 + GH), X, 0.48, GY1 - GY0 - 0.008, 0.05, 'mermer')
for yy_, nn_ in ((GY0 + 0.0025, -Y), (GY1 - 0.0025, Y)):
    for xx in (XG - 0.235, XG - 0.165, XG + 0.165, XG + 0.235):   # attic pilasters over the gate's pilasters
        kutu_merkez(y, (xx, yy_ + nn_.y * 0.0035), 0.024, 0.007, 0.044, 'mermer', z0=Z0 + GH)
    y.yuz_yon([V(XG - 0.145, yy_, ZA + 0.01), V(XG + 0.145, yy_, ZA + 0.01), V(XG + 0.145, yy_, ZA + 0.034), V(XG - 0.145, yy_, ZA + 0.034)],
              'tas_koyu', nn_)
    for i in range(14):
        x = XG - 0.14 + i * 0.0215
        y.yuz_yon([V(x, yy_ + nn_.y * 0.001, ZA + 0.016), V(x + 0.012, yy_ + nn_.y * 0.001, ZA + 0.016), V(x + 0.012, yy_ + nn_.y * 0.001, ZA + 0.028),
                   V(x, yy_ + nn_.y * 0.001, ZA + 0.028)], 'altin', nn_)
kornis(y, XG - 0.24, XG + 0.24, GY0 + 0.01, GY1 - 0.01, Z0 + GH + 0.044, 0.01, 0.008, 'mermer', 'tac')
ZQ = Z0 + GH + 0.055


def fil(x, yy, z, aci, s=1.0, key='altin'):
    """an elephant (statue): body, four pillar legs, a domed head, ears, a hanging trunk, tusks"""
    with parca(y, (x, yy, z), aci, s):
        boru(y, [V(-0.026, 0, 0.042), V(0.0, 0, 0.044), V(0.022, 0, 0.044)], 0.02, key, n=10)
        kure(y, (0.022, 0, 0.044), 0.02, key, n=10, kat=5)
        kure(y, (-0.026, 0, 0.042), 0.02, key, n=10, kat=5)
        for lx in (0.018, -0.022):
            for ly in (0.011, -0.011):
                boru(y, [V(lx, ly, 0.032), V(lx, ly, 0.0)], 0.0075, key, n=7)
        kure(y, (0.044, 0, 0.054), 0.014, key, n=10, kat=5)
        boru(y, [V(0.056, 0, 0.05), V(0.064, 0, 0.032), V(0.062, 0, 0.012), V(0.068, 0, 0.004)], 0.0055, key, n=6, r_son=0.0028)
        for sy in (-1, 1):
            iki_yuzlu(y, [V(0.04, sy * 0.012, 0.064), V(0.034, sy * 0.022, 0.06), V(0.032, sy * 0.024, 0.04), V(0.04, sy * 0.013, 0.04)], key, V(0, sy, 0))
            boru(y, [V(0.054, sy * 0.006, 0.042), V(0.066, sy * 0.008, 0.034)], 0.0022, 'mermer', n=4, r_son=0.001)
        boru(y, [V(-0.045, 0, 0.044), V(-0.05, 0, 0.022)], 0.002, key, n=4)


kutu_merkez(y, (XG, (GY0 + GY1) / 2 - 0.01), 0.24, 0.1, 0.014, 'mermer', z0=ZQ - 0.004)
for k, dx in enumerate((-0.078, -0.026, 0.026, 0.078)):
    fil(XG + dx, (GY0 + GY1) / 2 - 0.03, ZQ + 0.01, -math.pi / 2, 0.85)
# the chariot and Theodosius behind the team
kutu_merkez(y, (XG, (GY0 + GY1) / 2 + 0.035), 0.06, 0.03, 0.025, 'altin', z0=ZQ + 0.01)
heykel(y, XG, (GY0 + GY1) / 2 + 0.04, ZQ + 0.012, 1.0, 'altin', aci=-math.pi / 2, kol=0.8)
# the two marble towers
for sx in (-1, 1):
    tx, ty, tw = XG + sx * 0.355, YI + 0.02, 0.19
    kk = dikdortgen(tx - tw / 2, tx + tw / 2, ty - tw / 2, ty + tw / 2)
    H = 0.54
    for i in range(4):
        almasik(y, kk[i], kk[(i + 1) % 4], Z0, GH, 1 if i != 2 else 0, en=0.2, v0=GH * 0.42, ust=0.1, derin=0.016, duvar='mermer', bant='kirec',
                bant_list=bantlar(GH, 0.09, 0.012), cer=(0.008, 'kirec'))
        almasik(y, kk[i], kk[(i + 1) % 4], Z0 + GH, H - GH, 2 if i != 2 else 1, en=0.42, v0=0.035, ust=0.045, derin=0.016, duvar='mermer',
                bant='kirec', bant_list=[(0.0, 0.012)], cer=(0.008, 'kirec'))
    silme(y, kk, Z0, 0.02, 0.012, 'mermer', 'kaide')
    silme(y, kk, Z0 + GH - 0.016, 0.022, 0.012, 'mermer', 'tac')
    silme(y, kk, Z0 + H - 0.024, 0.024, 0.012, 'mermer', 'kaba')
    parapet(y, kk, Z0 + H, 0.012, 0.03, 0.016, 'mermer')
    y.yuz_yon([V(p.x, p.y, Z0 + H + 0.0005) for p in disa(kk, -0.016)], 'zemin', Z)
    y.prizma((tx, ty), 0.03, Z0 + H, Z0 + H + 0.04, 'mermer', n=8, kat=math.pi / 8)
    y.koni((tx, ty), 0.036, Z0 + H + 0.04, 0.05, 'kursun', n=8)
    hac(y, tx, ty, Z0 + H + 0.09, 0.04)

# ---------------------------------------------------------------- the city behind
y.bolum('Şehir: Mese, kilise, evler')
# the paved road from the bridge through both gates to the church
for y0_, y1_ in ((YI - DC, YI - DB), (YI - DB + 0.03, OY - 0.05), (OY + 0.04, GY0), (GY1, 0.2)):
    y.yuz_yon([V(XG - 0.045, y0_, Z0 + 0.0015), V(XG + 0.045, y0_, Z0 + 0.0015), V(XG + 0.045, y1_, Z0 + 0.0015), V(XG - 0.045, y1_, Z0 + 0.0015)], 'zemin', Z)
y.yuz_yon([V(-0.55, 0.0, Z0 + 0.0015), V(XG - 0.045, 0.0, Z0 + 0.0015), V(XG - 0.045, 0.07, Z0 + 0.0015), V(-0.55, 0.07, Z0 + 0.0015)], 'zemin', Z)
# a domed church (cross-in-square, banded walls, a high drum)
CX, CY = 0.42, 0.52
CW = 0.36
ck = dikdortgen(CX - CW / 2, CX + CW / 2, CY - CW / 2, CY + CW / 2)
for i in range(4):
    almasik(y, ck[i], ck[(i + 1) % 4], Z0, 0.24, 3, en=0.4, v0=0.1, ust=0.03, kapi_bay=1 if i == 0 else None, derin=0.02)
silme(y, ck, Z0 + 0.24 - 0.014, 0.018, 0.012, 'kirec', 'tac')
silme(y, ck, Z0, 0.014, 0.008, 'kirec', 'kaide')
y.yuz_yon([V(p.x, p.y, Z0 + 0.244) for p in ck], 'kursun', Z)
# the arms of the cross: barrel-vault-like gables on the four sides, the drum and the dome
for (ax0, ax1, ay0, ay1) in ((CX - 0.07, CX + 0.07, CY - CW / 2, CY + CW / 2), (CX - CW / 2, CX + CW / 2, CY - 0.07, CY + 0.07)):
    duvarlar(y, dikdortgen(ax0, ax1, ay0, ay1), Z0 + 0.244, Z0 + 0.3, 'kirec')
    kiremit_cati(y, ax0, ax1, ay0, ay1, Z0 + 0.3, 0.05, sacak=0.012)
kutu_merkez(y, (CX, CY), 0.2, 0.2, 0.09, 'kirec', z0=Z0 + 0.244)
biz_kubbe(y, (CX, CY), 0.09, Z0 + 0.334, 0.09, 12, kubbe_h=0.075)
for sx in (-1, 1):
    for sy in (-1, 1):
        kucuk_kubbe(y, CX + sx * 0.13, CY + sy * 0.13, Z0 + 0.244, 0.035, kasnak=0.03, n=16, son=False, key='kursun', kasnak_key='tugla_roma')
# narthex porch on the front (towards the road)
arkad(y, V(CX - CW / 2, CY - CW / 2 - 0.06), V(CX + CW / 2, CY - CW / 2 - 0.06), 5, Z0, 0.13, en=0.62, ust=0.02, sivri=0.0, derin=0.06,
      cerceve=(0.007, ['tugla_roma', 'kirec']), renk=('kirec', 'kirec', 'mermer', 'tas_koyu'), sutun_r=0.009)
duz_duvar(y, V(CX - CW / 2, CY - CW / 2), V(CX - CW / 2, CY - CW / 2 - 0.06), Z0, Z0 + 0.13, 'kirec')
duz_duvar(y, V(CX + CW / 2, CY - CW / 2 - 0.06), V(CX + CW / 2, CY - CW / 2), Z0, Z0 + 0.13, 'kirec')
kiremit_cati(y, CX - CW / 2, CX + CW / 2, CY - CW / 2 - 0.065, CY - CW / 2, Z0 + 0.13, 0.03, sacak=0.012)
# apse on the back
donel(y, (CX, CY + CW / 2), [(0.07, Z0), (0.07, Z0 + 0.2), (0.0, Z0 + 0.2)], 'tugla_roma', n=12)
halka_kornis(y, (CX, CY + CW / 2), 0.07, Z0 + 0.19, 0.012, 0.008, 12, 'kirec')


def ev(x, yy, w, d, h, aci=0.0, key='siva_krem', tohum=0):
    """a city house: plastered walls with small windows, a red-tile roof"""
    with parca(y, (x, yy, 0), aci):
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        duvarlar(y, k, Z0, Z0 + h, key)
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            L = (b - a).length
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            m = max(1, int(L / 0.05))
            for j in range(m):
                y.pencere(a + Z * Z0, e, nn, L * (j + 0.5) / m - 0.007, h * 0.55, 0.014, h * 0.28, 'koyu', kemer=True, k_say=3)
        kiremit_cati(y, -w / 2, w / 2, -d / 2, d / 2, Z0 + h, min(w, d) * 0.4, sacak=0.012)


for i, (x, yy, w, d, h, a) in enumerate(((-0.45, -0.25, 0.14, 0.1, 0.1, 0), (-0.25, -0.24, 0.12, 0.1, 0.12, 0), (-0.5, 0.2, 0.12, 0.16, 0.1, 0),
                                       (-0.48, 0.45, 0.16, 0.11, 0.13, 0), (-0.45, 0.72, 0.14, 0.12, 0.1, 0), (0.0, 0.73, 0.16, 0.12, 0.12, 0),
                                       (0.8, 0.0, 0.14, 0.12, 0.11, 0), (0.95, 0.25, 0.12, 0.14, 0.1, 0), (0.92, 0.6, 0.14, 0.12, 0.13, 0),
                                       (0.78, 0.82, 0.16, 0.1, 0.1, 0), (0.62, -0.25, 0.14, 0.1, 0.1, 0), (0.95, -0.22, 0.12, 0.12, 0.12, 0),
                                       (-0.05, 0.2, 0.12, 0.1, 0.1, 0), (0.05, -0.27, 0.1, 0.1, 0.11, 0))):
    ev(x, yy, w, d, h, a, ('siva_krem', 'siva', 'siva_oker', 'tugla_roma')[i % 4], i)
for x, yy in ((-0.3, 0.6), (0.15, 0.45), (0.7, 0.35), (0.62, 0.72), (-0.1, -0.05), (0.85, -0.38), (-0.55, -0.05), (0.2, 0.85)):
    agac(y, x, yy, Z0, boy=0.16, tur='servi' if R.random() < 0.5 else 'yapraklı', key='yesil_koyu' if R.random() < 0.5 else 'zeytin')

# the Column of Arcadius: stepped base, a pedestal with reliefs, the spiral-relief shaft, the emperor
y.bolum('Arkadios Sütunu')
AX, AY = -0.18, 0.43
for k, (w, h) in enumerate(((0.16, 0.012), (0.14, 0.012), (0.12, 0.012))):
    kutu_merkez(y, (AX, AY), w, w, h, 'mermer', z0=Z0 + 0.012 * k)
zz = Z0 + 0.036
kutu_merkez(y, (AX, AY), 0.1, 0.1, 0.11, 'mermer', z0=zz)
kornis(y, AX - 0.05, AX + 0.05, AY - 0.05, AY + 0.05, zz, 0.012, 0.008, 'mermer', 'kaide')
kornis(y, AX - 0.05, AX + 0.05, AY - 0.05, AY + 0.05, zz + 0.1, 0.012, 0.008, 'mermer', 'tac')
for e, n_ in ((X, -Y), (Y, X), (-X, Y), (-Y, -X)):
    c = V(AX, AY) + n_ * 0.0502 + Z * (zz + 0.03)
    y.yuz_yon([c - e * 0.036, c + e * 0.036, c + e * 0.036 + Z * 0.05, c - e * 0.036 + Z * 0.05], 'tas_acik', n_)
    for k in range(5):
        p = c - e * 0.03 + e * (0.015 * k) + n_ * 0.0005
        kutu(y, p - e * 0.003 + Z * 0.008, e, 0.006, -0.0025, 0.026, 'mermer', 'arkasagsolust')
zz += 0.122
H = 0.58
donel(y, (AX, AY), [(0.032, zz), (0.032, zz + 0.01), (0.026, zz + 0.016), (0.026, zz + H), (0.034, zz + H + 0.004), (0.034, zz + H + 0.018),
                     (0.0, zz + H + 0.018)], 'mermer', n=16)
# the spiral relief band
pts = [V(AX + 0.0272 * math.cos(TAU * 7 * t / 140), AY + 0.0272 * math.sin(TAU * 7 * t / 140), zz + 0.02 + (H - 0.03) * t / 140) for t in range(141)]
boru(y, pts, 0.0028, 'tas_acik', n=4)
heykel(y, AX, AY, zz + H + 0.018, 1.1, 'bronz', aci=-math.pi / 2, kol=0.8)

calistir(y, 'lm_theodosius')
