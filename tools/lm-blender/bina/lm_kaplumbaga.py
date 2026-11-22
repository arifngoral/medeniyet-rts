# Kaplumbağa Gemisi Tersanesi (lm_kaplumbaga): a Joseon naval yard (seonso) for geobukseon. A turtle ship on the
# stone-walled slipway in its scaffolding, one rowing out under sail breathing smoke from its dragon head, one moored at
# the timber pier; the boat hangar, the storehouse, the timber yard with log piles, a saw pit and a plank-steaming
# trough, bronze cannons on the quay; a tall watchtower on a granite bastion at the water's edge.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ek import *
from bina_ortak import calistir
import random

y = Yapi()
rs = random.Random(5)
GX0, GX1, GY0, GY1 = -1.15, 1.15, -1.15, 1.12
KY = -0.22                    # the quay line
Z0, ZW = 0.06, 0.022          # land, water
SX0, SX1, SY1 = -0.98, -0.5, 0.52   # the slipway (cut into the land from the quay to SY1)

# ---------------------------------------------------------------- land, water, quay
y.bolum('Kara, su ve rıhtım')
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, KY - GY0, ZW - 0.0005, 'kaya_koyu', 'onsagsol')
y.yuz_yon([V(GX0, GY0, ZW), V(GX1, GY0, ZW), V(GX1, KY, ZW), V(GX0, KY, ZW)], 'su', Z)
kutu(y, V(GX0, KY, 0), X, GX1 - GX0, GY1 - KY, Z0, 'tas_koyu', 'arkasagsol')
silme(y, [V(GX1, KY), V(GX1, GY1), V(GX0, GY1), V(GX0, KY)], Z0 - 0.008, 0.008, 0.006, 'tas_koyu', 'duz', kapali=False)


def ust(x, yy):
    if -0.38 < x < 0.45 and -0.05 < yy < 0.45:
        return 'toprak'               # the timber yard
    if yy < KY + 0.14:
        return 'zemin'                # the paved quay
    return 'toprak_ot'


xs = [GX0, SX0, SX1, -0.38, 0.45, GX1]
ys = [KY, KY + 0.14, -0.05, 0.45, SY1, GY1]
xs, ys = sorted(set(xs)), sorted(set(ys))
for i in range(len(xs) - 1):
    for j in range(len(ys) - 1):
        mx, my = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
        if SX0 < mx < SX1 and my < SY1:
            continue
        y.yuz_yon([V(xs[i], ys[j], Z0), V(xs[i + 1], ys[j], Z0), V(xs[i + 1], ys[j + 1], Z0), V(xs[i], ys[j + 1], Z0)], ust(mx, my), Z)
for (xa, xb) in ((GX0, SX0), (SX1, GX1)):   # the granite quay wall
    duz_duvar(y, V(xa, KY), V(xb, KY), ZW - 0.006, Z0, 'granit')
    silme(y, [V(xa, KY), V(xb, KY)], Z0 - 0.007, 0.009, 0.007, TAS2, 'duz', kapali=False)
for k in range(10):   # bollards
    x = -0.4 + k * 0.15
    if 0.52 < x < 0.68:
        continue
    y.prizma((x, KY + 0.02), 0.007, Z0, Z0 + 0.02, 'granit_koyu', n=8)
    kure(y, (x, KY + 0.02, Z0 + 0.022), 0.008, 'granit_koyu', n=8, kat=3)
dalgalar(y, GX0 + 0.03, GX1 - 0.03, GY0 + 0.03, KY - 0.03, ZW, 34, 9, 0.035,
         [(-0.3, 0.42, -0.84, -0.4), (0.7, 0.88, -0.9, -0.15), (SX0, SX1, -0.42, KY)])

# ---------------------------------------------------------------- the slipway
y.bolum('Kızak')
ZR1, ZR0 = Z0 - 0.006, ZW - 0.03         # the ramp at its head and at the slip's mouth (under water)
YM = KY - 0.16
zr = lambda yy: ZR0 + (ZR1 - ZR0) * (yy - YM) / (SY1 - YM)
for (xa, ya, xb, yb) in ((SX0, KY, SX0, SY1), (SX1, SY1, SX1, KY)):
    s_ = 1 if xa == SX0 else -1
    y.yuz_yon([V(xa, ya, zr(ya)), V(xb, yb, zr(yb)), V(xb, yb, Z0), V(xa, ya, Z0)], 'granit', V(s_, 0, 0))
y.yuz_yon([V(SX0, SY1, zr(SY1)), V(SX1, SY1, zr(SY1)), V(SX1, SY1, Z0), V(SX0, SY1, Z0)], 'granit', -Y)
for xa in (SX0, SX1):
    silme(y, [V(xa, KY), V(xa, SY1)] if xa == SX1 else [V(xa, SY1), V(xa, KY)], Z0 - 0.007, 0.009, 0.007, TAS2, 'duz', kapali=False)
y.yuz_yon([V(SX0, YM, zr(YM)), V(SX1, YM, zr(YM)), V(SX1, SY1, zr(SY1)), V(SX0, SY1, zr(SY1))], 'ahsap', V(0, -0.05, 1))
# the ground ways (two timber rails) and cross sleepers
for sx in (-1, 1):
    xx = (SX0 + SX1) / 2 + sx * 0.06
    cubuk(y, V(xx, YM + 0.12, zr(YM + 0.12) + 0.004), V(xx, SY1 - 0.02, zr(SY1 - 0.02) + 0.004), 0.018, 'ahsap_koyu', 0.008)
for k in range(9):
    yy = KY + 0.02 + k * 0.08
    cubuk(y, V(SX0 + 0.02, yy, zr(yy) + 0.002), V(SX1 - 0.02, yy, zr(yy) + 0.002), 0.012, 'ahsap_koyu', 0.004)
# the ship on its cradle, level, on blocks rising towards the water
SC = ((SX0 + SX1) / 2, 0.16)
ZK = zr(SC[1] + 0.31) + 0.022
for k in range(7):
    yy = SC[1] - 0.27 + k * 0.09
    kutu_merkez(y, (SC[0], yy), 0.07, 0.03, ZK - 0.002 - zr(yy), 'ahsap', z0=zr(yy))
geobukseon(y, SC, -math.pi / 2, 1.0, ZK, direk=False, kurek=False, duman=False, tohum=3)
# scaffolding along both sides, with staging and shipwrights
for sx in (-1, 1):
    xx = SC[0] + sx * 0.125
    for k in range(6):
        yy = SC[1] - 0.3 + k * 0.12
        y.prizma((xx, yy), 0.0035, zr(yy), ZK + 0.17, 'ahsap_acik', n=4)
    for zz in (ZK + 0.075, ZK + 0.14):
        kutu3(y, V(xx - sx * 0.012, SC[1], zz), X, Y, Z, 0.03, 0.62, 0.004, 'ahsap')
        cubuk(y, V(xx, SC[1] - 0.3, zz + 0.03), V(xx, SC[1] + 0.3, zz + 0.03), 0.003, 'ahsap_acik')
    for k in range(2):
        cubuk(y, V(xx, SC[1] - 0.2 + k * 0.3, zr(SC[1] - 0.2 + k * 0.3)), V(xx, SC[1] - 0.1 + k * 0.3, ZK + 0.075), 0.003, 'ahsap_koyu')
    for k in range(3):
        insan(y, xx - sx * 0.012, SC[1] - 0.2 + k * 0.2, ZK + 0.077 + (0.065 if k == 1 else 0), math.pi if sx > 0 else 0.0, 'kece', 'saz', 0.05,
              egik=0.4)
# a winch (capstan) at the slip's head and the hauling rope
donel(y, (SC[0], SY1 + 0.06), [(0.02, Z0), (0.015, Z0 + 0.01), (0.017, Z0 + 0.03), (0.022, Z0 + 0.034), (0.0, Z0 + 0.036)], 'ahsap', n=8)
for a in (0.3, 0.3 + math.pi / 2):
    cubuk(y, V(SC[0] - math.cos(a) * 0.06, SY1 + 0.06 - math.sin(a) * 0.06, Z0 + 0.032), V(SC[0] + math.cos(a) * 0.06, SY1 + 0.06 + math.sin(a) * 0.06, Z0 + 0.032),
          0.003, 'ahsap_acik')
boru(y, [V(SC[0], SY1 + 0.04, Z0 + 0.02), V(SC[0], SC[1] + 0.34, ZK + 0.05)], 0.0018, 'saz_koyu', n=4)

# ---------------------------------------------------------------- the ships in the water
y.bolum('Sudaki gemiler')
geobukseon(y, (0.05, -0.62), math.pi, 1.05, ZW - 0.075 * 0.32 * 1.05, su=0.075 * 0.32, tohum=1)
# moored at the pier, masts up, sails furled
PX = 0.6
geobukseon(y, (PX + 0.17, -0.55), -math.pi / 2, 0.95, ZW - 0.075 * 0.3 * 0.95, yelken=False, kurek=False, duman=False, tohum=2, sancakli=True)
# the pier on piles
kutu(y, V(PX - 0.045, -0.95, Z0 - 0.012), X, 0.09, KY - (-0.95), 0.008, 'ahsap', 'onsagsolust')
for k in range(6):
    yy = -0.93 + k * 0.14
    for sx in (-1, 1):
        y.prizma((PX + sx * 0.04, yy), 0.006, 0.0, Z0 + 0.004, 'ahsap_koyu', n=6)
for k in range(12):
    yy = -0.94 + k * 0.06
    y.yuz_yon([V(PX - 0.045, yy, Z0 - 0.0035), V(PX + 0.045, yy, Z0 - 0.0035), V(PX + 0.045, yy + 0.004, Z0 - 0.0035), V(PX - 0.045, yy + 0.004, Z0 - 0.0035)],
              'ahsap_koyu', Z)
insan(y, PX, -0.6, Z0 - 0.004, 0.0, 'kece', 'saz', 0.05)
insan(y, PX - 0.02, -0.82, Z0 - 0.004, 2.0, 'boya_kirmizi', 'koyu', 0.05)
# small boats
for (x, yy, a) in ((-0.55, -0.95, 0.4), (0.4, -1.02, -0.2), (1.0, -0.98, 1.6)):
    with parca(y, (x, yy, ZW), a):
        P, Du, hb = kore_gemi_govde(0.12, 0.022, 0.018, bas_egim=0.008, kic_egim=0.006)
        us = [-1 + 2 * i / 6 for i in range(7)]
        for sd in (-1, 1):
            for i in range(6):
                q = [P(us[i], sd, 0.0), P(us[i + 1], sd, 0.0), P(us[i + 1], sd, 1.0), P(us[i], sd, 1.0)]
                q = [p - Z * 0.006 for p in q]
                m = sum(q, Vector()) / 4
                yuz_dis(y, q, 'ahsap', V(m.x, 0, m.z))
        for u, sg in ((1.0, 1), (-1.0, -1)):
            y.yuz_yon([P(u, -1, 0.0) - Z * 0.006, P(u, 1, 0.0) - Z * 0.006, P(u, 1, 1.0) - Z * 0.006, P(u, -1, 1.0) - Z * 0.006], 'ahsap', V(sg, 0, 0.3 * sg))
        y.yuz_yon([P(u, -1, 1.0) - Z * 0.006 for u in us] + [P(u, 1, 1.0) - Z * 0.006 for u in reversed(us)], 'ahsap_acik', Z)
        for sd in (-1, 1):
            boru(y, [P(u, sd, 1.0) - Z * 0.005 for u in us], 0.0018, 'ahsap_koyu', n=4)
        insan(y, 0.0, 0.0, 0.004, 0.0, 'kece', 'saz', 0.045)

# ---------------------------------------------------------------- the hangar and the storehouse
y.bolum('Hangar ve ambar')
kore_salon(y, -0.73, 0.83, 0.56, 0.36, Z0, 0.15, 0.14, sacak=0.06, tur='matbae', kivrim=0.25, nx=5, ny=3,
           on=['karanlik', 'karanlik', 'tahta', 'karanlik', 'karanlik'], yan='duvar', arka='duvar', gidan=(0.015, TAS, 1), chwidu=0.0,
           levha=False, r=0.009, duvar='ahsap_dikey', direk='ahsap', mahya_en=0.014)
kore_salon(y, 0.05, 0.84, 0.6, 0.3, Z0, 0.13, 0.15, sacak=0.065, tur='paljak', kivrim=0.34, yukari=0.04, nx=5, ny=3,
           on=['pencere', 'karanlik', 'tahta', 'karanlik', 'pencere'], yan='pencere', arka='duvar', gidan=(0.02, TAS, 1), japsang=3, chwidu=1.0,
           r=0.009, mahya_en=0.014)

# the yard officers' quarters behind the tower, inside a low wall
kore_salon(y, 0.78, 0.74, 0.4, 0.22, Z0, 0.11, 0.12, sacak=0.055, tur='paljak', kivrim=0.34, yukari=0.04, nx=5, ny=2,
           on=['pencere', 'kapi', 'kapi', 'kapi', 'pencere'], yan='pencere', arka='duvar', gidan=(0.02, TAS, 1), japsang=2, chwidu=0.9,
           r=0.0085, mahya_en=0.013)
kore_sur(y, [(0.98, 0.5), (1.08, 0.5), (1.08, 1.06), (0.5, 1.06), (0.5, 0.5), (0.58, 0.5)], Z0, 0.05, t=0.024, key='tas', ust=DUVAR)

# ---------------------------------------------------------------- the timber yard
y.bolum('Kereste avlusu')


def kutuk_yigini(x, yy, aci, n=4, kat=3, L=0.22, r=0.014):
    with parca(y, (x, yy, Z0), aci):
        for k in range(kat):
            m = n - k
            for i in range(m):
                v = (i - (m - 1) / 2) * r * 2.05
                boru(y, [V(-L / 2, v, r + k * r * 1.75), V(L / 2, v, r + k * r * 1.75)], r, 'kutuk' if (i + k) % 2 else 'ahsap', n=8)


def tahta_yigini(x, yy, aci, n=5, kat=4, L=0.18, en=0.03):
    with parca(y, (x, yy, Z0), aci):
        for k in range(kat):
            zz = k * 0.009
            kutu3(y, V(0, 0, zz + 0.0035), X, Y, Z, L, n * en, 0.007, 'ahsap_acik', ('+x', '-x', '+y', '-y', '+z'))
            for s_ in (-0.35, 0.35):
                kutu3(y, V(s_ * L, 0, zz + 0.0075), X, Y, Z, 0.008, n * en + 0.004, 0.002, 'ahsap_koyu', ('+x', '-x', '+y', '-y', '+z'))


kutuk_yigini(-0.25, 0.32, 0.1)
kutuk_yigini(0.32, 0.36, -0.15, 3, 2)
tahta_yigini(-0.18, 0.06, 1.4)
tahta_yigini(0.05, 0.36, 0.0, 4, 5)
# the saw pit: a trestle with a log on it, two sawyers
for sx in (-1, 1):
    cubuk(y, V(0.12 + sx * 0.05, 0.08, Z0), V(0.12 + sx * 0.05, 0.08, Z0 + 0.06), 0.008, 'ahsap_koyu')
    cubuk(y, V(0.12 + sx * 0.05, 0.08 - 0.02, Z0), V(0.12 + sx * 0.05, 0.08 + 0.02, Z0 + 0.06), 0.005, 'ahsap_koyu')
boru(y, [V(0.0, 0.08, Z0 + 0.07), V(0.24, 0.08, Z0 + 0.07)], 0.013, 'kutuk', n=8)
cubuk(y, V(0.1, 0.08, Z0 + 0.03), V(0.1, 0.08, Z0 + 0.12), 0.003, 'demir')
insan(y, 0.1, 0.03, Z0, math.pi / 2, 'kece', 'saz', 0.05, egik=0.3)
insan(y, 0.1, 0.13, Z0 + 0.0, -math.pi / 2, 'kece', 'saz', 0.05, egik=0.3)
# the plank-steaming trough over a fire
kutu_merkez(y, (0.33, 0.06), 0.2, 0.04, 0.03, 'tas', z0=Z0)
kutu_merkez(y, (0.33, 0.06), 0.18, 0.03, 0.012, 'ahsap', z0=Z0 + 0.03)
for k in range(5):   # (steam rising off the trough, soft puffs)
    kure(y, (0.26 + k * 0.035, 0.06 + 0.006 * (k % 2), Z0 + 0.052 + (k % 2) * 0.012), 0.011 + 0.003 * (k % 3), 'buhar', n=8, kat=4)
y.yuz_yon([V(0.24, 0.04 - 0.0006, Z0 + 0.004), V(0.42, 0.04 - 0.0006, Z0 + 0.004), V(0.42, 0.04 - 0.0006, Z0 + 0.016), V(0.24, 0.04 - 0.0006, Z0 + 0.016)],
          'turuncu', -Y)
insan(y, 0.36, 0.0, Z0, 1.2, 'kece', 'saz', 0.05)
# bronze cannons and shot on the quay
for k in range(4):
    x = -0.35 + k * 0.08
    with parca(y, (x, KY + 0.08, Z0), math.pi / 2 + 0.1 * k):
        kutu3(y, V(0, 0, 0.008), X, Y, Z, 0.07, 0.03, 0.012, 'ahsap_koyu')
        for xx in (-0.025, 0.025):
            for sy in (-1, 1):
                teker(y, V(xx, sy * 0.018, 0.009), Y, 0.009, 0.004, 'ahsap_koyu', 'demir', 4, 8)
        boru(y, [V(-0.04, 0, 0.022), V(0.045, 0, 0.022)], 0.009, 'bronz', n=8, r_son=0.007)
        for xx in (-0.03, -0.005, 0.02, 0.04):
            boru(y, [V(xx - 0.002, 0, 0.022), V(xx + 0.002, 0, 0.022)], 0.0105, 'bronz', n=8)
for k in range(5):
    kure(y, (0.0 + (k % 3) * 0.016, KY + 0.06 + (k // 3) * 0.014, Z0 + 0.008 + (k // 3) * 0.006), 0.007, 'demir', n=6, kat=3)

# ---------------------------------------------------------------- the watchtower on its bastion
y.bolum('Gözcü kulesi')
TC = (0.86, -0.02)
BW = 0.26
kb = dikdortgen(TC[0] - BW / 2, TC[0] + BW / 2, TC[1] - BW / 2, TC[1] + BW / 2)
duvarlar(y, kb, ZW - 0.006, Z0 + 0.12, 'granit', ust='zemin')
silme(y, kb, Z0 + 0.105, 0.015, 0.008, TAS2, 'kaba')
silme(y, kb, ZW - 0.004, 0.016, 0.006, 'granit_koyu', 'kaide')
for i in range(4):   # crenellated parapet
    a_, b_ = kb[i], kb[(i + 1) % 4]
    e = (b_ - a_).normalized()
    nn = V(e.y, -e.x)
    mazgal(y, a_ - nn * 0.006, b_ - nn * 0.006, Z0 + 0.12, 0.028, 0.016, 'granit', dis_en=0.04, bosluk=0.018)
merdiven(y, (TC[0] - BW / 2 - 0.1, TC[1] + BW / 2 - 0.03), 0.0, 0.05, Z0, Z0 + 0.12, 9, key='granit')
ZB = Z0 + 0.12
TW = 0.16
TH = 0.4
for sx in (-1, 1):
    for sy in (-1, 1):
        p0 = V(TC[0] + sx * (TW / 2 + 0.01), TC[1] + sy * (TW / 2 + 0.01), ZB)
        p1 = V(TC[0] + sx * (TW / 2 - 0.008), TC[1] + sy * (TW / 2 - 0.008), ZB + TH)
        cubuk(y, p0, p1, 0.015, 'lake')
        kutu_merkez(y, (p0.x, p0.y), 0.024, 0.024, 0.008, TAS2, z0=ZB, yuzler='onarkasagsolust')
TK = dikdortgen(TC[0] - TW / 2, TC[0] + TW / 2, TC[1] - TW / 2, TC[1] + TW / 2)
for st in range(3):
    za, zb_ = ZB + TH * st / 3, ZB + TH * (st + 1) / 3
    for i in range(4):
        a_, b_ = TK[i], TK[(i + 1) % 4]
        nn = V((b_ - a_).y, -(b_ - a_).x).normalized()
        sh = lambda p, zz: V(p.x, p.y, zz) + nn * 0.004 + (V(p.x, p.y) - V(TC[0], TC[1])).normalized() * (0.01 * (1 - (zz - ZB) / TH))
        cubuk(y, sh(a_, za + 0.01), sh(b_, zb_ - 0.01), 0.006, 'ahsap')
        cubuk(y, sh(b_, za + 0.01), sh(a_, zb_ - 0.01), 0.006, 'ahsap')
        cubuk(y, sh(a_, zb_), sh(b_, zb_), 0.008, 'lake_koyu')
for s in (-1, 1):
    cubuk(y, V(TC[0] - TW / 2 - 0.08, TC[1] + s * 0.016, ZB), V(TC[0] - TW / 2 - 0.006, TC[1] + s * 0.016, ZB + TH), 0.005, 'ahsap_koyu')
for k in range(10):
    t = (k + 0.5) / 10
    p = V(TC[0] - TW / 2 - 0.08 + 0.074 * t, TC[1], ZB + TH * t)
    cubuk(y, p - Y * 0.016, p + Y * 0.016, 0.003, 'ahsap')
ZL = ZB + TH
kutu(y, V(TC[0] - TW / 2 - 0.03, TC[1] - TW / 2 - 0.03, ZL), X, TW + 0.06, TW + 0.06, 0.012, 'lake_koyu')
kutu(y, V(TC[0] - TW / 2 - 0.028, TC[1] - TW / 2 - 0.028, ZL + 0.012), X, TW + 0.056, TW + 0.056, 0.003, 'ahsap_acik', 'ust')
y.yuz_yon(dikdortgen(TC[0] - TW / 2 - 0.03, TC[0] + TW / 2 + 0.03, TC[1] - TW / 2 - 0.03, TC[1] + TW / 2 + 0.03, ZL), 'lake_koyu', -Z)
kore_korkuluk(y, dikdortgen(TC[0] - TW / 2 - 0.022, TC[0] + TW / 2 + 0.022, TC[1] - TW / 2 - 0.022, TC[1] + TW / 2 + 0.022), ZL + 0.015, 0.024, adim=0.05)
kore_salon(y, TC[0], TC[1], TW, TW, ZL + 0.015, 0.07, 0.11, sacak=0.06, tur='ujingak', kivrim=0.36, yukari=0.045, nx=2, ny=2, on='acik', yan='acik',
           arka='acik', japsang=3, chwidu=0.0, r=0.007, levha=False, mahya_en=0.012, ic_direk=False)
sancak(y, TC[0] - TW / 2 - 0.02, TC[1] - TW / 2 - 0.02, ZL + 0.015, boy=0.25, en=0.13, yuk=0.08, aci=-2.4)
insan(y, TC[0] + 0.02, TC[1] - 0.03, ZL + 0.02, -1.6, 'boya_kirmizi', 'koyu', 0.05)
# a war drum on the bastion
donel(y, (TC[0] + 0.07, TC[1] + 0.08), [(0.0, ZB), (0.022, ZB + 0.002), (0.026, ZB + 0.02), (0.022, ZB + 0.038), (0.0, ZB + 0.04)], 'boya_kirmizi', n=10)

# ---------------------------------------------------------------- trees, people
y.bolum('Ağaçlar ve insanlar')
for k, (tx, ty) in enumerate(((-1.08, 0.3), (-1.06, 1.05), (0.42, 1.05), (0.42, 0.62), (1.1, 0.35), (1.1, 1.09), (-0.4, 0.62), (0.55, 0.45))):
    sonamu(y, tx, ty, Z0, 0.15 + 0.03 * (k % 3), tohum=k + 20)
for k, (x, yy, a) in enumerate(((-0.3, -0.12, 0.4), (0.25, -0.15, 2.0), (0.4, -0.1, 3.5), (-0.1, 0.22, 1.0), (0.55, 0.2, 2.2))):
    insan(y, x, yy, Z0, a, 'kece' if k % 2 else 'boya_kirmizi', 'saz' if k % 2 else 'koyu', 0.05)

sayim(y)
calistir(y, 'lm_kaplumbaga')
