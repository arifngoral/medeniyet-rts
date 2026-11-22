# Okcu Talim Alani (lm_okcutalim): an English village's longbow practice ground. Turf butts with painted straw targets
# at the end of mown lanes, longbowmen loosing from the shooting line with sheaves of arrows stuck in the ground, the
# marshal's striped tent and bow racks, the bowyer's jettied timber workshop with staves drying outside; behind, the
# village church with its tall Perpendicular west tower (the silhouette: buttresses, belfry, battlements, pinnacles,
# the banner), its churchyard and lychgate, spreading oaks and a few cottages.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from ingiliz_ortak import *
from frank_ek import gotik_pencere, fiyal, piramit_cati
from frank_ortak import ev
from bina_ortak import calistir
import doku

y = Yapi()
G = 0.03
doku.KOSE_RENK['cimen'] = cayir_renk(G)
XA, XB, YA, YB = -1.15, 1.15, -1.0, 1.0
DUV, DR = 'kirec', 'tas_acik'
AHS = 'ahsap_koyu'


def sirala(a, b, dis):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized()
    return (a, b) if V(e.y, -e.x).dot(V(dis[0], dis[1])) > 0 else (b, a)


def mese(x, yy, boy=0.3, tohum=0):
    """a broad English oak: a stout trunk forking into limbs, a wide lumpy crown of several masses"""
    z = G
    boru(y, [V(x, yy, z - 0.01), V(x + 0.004, yy, z + boy * 0.3), V(x, yy + 0.004, z + boy * 0.42)], boy * 0.06, 'ahsap', n=7, r_son=boy * 0.04)
    kollar = []
    for k in range(4):
        a = TAU * k / 4 + tohum
        d = V(math.cos(a), math.sin(a))
        tip = V(x, yy, z + boy * 0.42) + d * boy * 0.3 + Z * boy * 0.28
        boru(y, [V(x, yy, z + boy * 0.4), V(x, yy, z + boy * 0.4) + d * boy * 0.14 + Z * boy * 0.12, tip], boy * 0.028, 'ahsap', n=5, r_son=boy * 0.012)
        kollar.append(tip)
    for k, t in enumerate(kollar):
        kure(y, (t.x, t.y, t.z + boy * 0.05), boy * (0.24 + 0.03 * ((k + tohum * 3) % 2)), 'yesil_koyu' if k % 2 else 'zeytin', n=10, kat=5)
    kure(y, (x, yy, z + boy * 0.86), boy * 0.3, 'zeytin', n=10, kat=5)


# ---------------------------------------------------------------- ground
y.bolum('Zemin ve atış şeritleri')
zemin_blok(y, XA, XB, YA, YB, G)
# the mown lanes (lighter stripes) between the shooting line and the butts
RX0, RX1 = -0.32, 0.92
LANES = [-0.6, -0.3, 0.0]
SL = -0.27                         # the shooting line
for k, ly in enumerate(LANES):
    y.yuz_yon([V(RX0, ly - 0.1, G + 0.002), V(RX1, ly - 0.1, G + 0.002), V(RX1, ly + 0.1, G + 0.002), V(RX0, ly + 0.1, G + 0.002)], 'cimen_kuru', Z)
# the shooting line: a chalked strip and stakes with a cord
y.yuz_yon([V(SL - 0.008, -0.74, G + 0.0035), V(SL + 0.007, -0.74, G + 0.0035), V(SL + 0.007, 0.14, G + 0.0035), V(SL - 0.008, 0.14, G + 0.0035)], 'beyaz', Z)
for k in range(5):
    yy = -0.74 + 0.88 * k / 4
    cubuk(y, V(SL, yy, G), V(SL, yy, G + 0.035), 0.006, AHS)
boru(y, [V(SL, -0.74, G + 0.03), V(SL, 0.14, G + 0.03)], 0.0012, 'kumas', n=3)
# distance wands (white-painted stakes) down the lanes
for xx in (0.15, 0.45):
    for ly in LANES:
        for s in (-1, 1):
            cubuk(y, V(xx, ly + s * 0.1, G), V(xx, ly + s * 0.1, G + 0.05), 0.005, 'beyaz')
            y.koni((xx, ly + s * 0.1), 0.006, G + 0.05, 0.008, 'boya_kirmizi', n=4)
# the village street along the front and to the church
y.yuz_yon([V(XA + 0.001, -0.95, G + 0.003), V(XB - 0.001, -0.95, G + 0.003), V(XB - 0.001, -0.87, G + 0.003), V(XA + 0.001, -0.87, G + 0.003)], 'toprak', Z)
y.yuz_yon([V(-0.62, -0.87, G + 0.003), V(-0.55, -0.87, G + 0.003), V(-0.55, 0.4, G + 0.003), V(-0.62, 0.4, G + 0.003)], 'toprak', Z)

# ---------------------------------------------------------------- the butts
y.bolum('Hedef setleri ve saman hedefler')


def set_(cx, cy, L=0.23, d0=0.26, d1=0.08, h=0.2):
    """a turf butt: a trapezoid earth bank along y (front towards -x), grassed slopes, earthen ends"""
    pts = lambda x, z: (V(cx + x, cy - L / 2, G + z), V(cx + x, cy + L / 2, G + z))
    fa, fb = pts(-d0 / 2, -0.004); ta, tb = pts(-d1 / 2, h); ua, ub = pts(d1 / 2, h); ba, bb = pts(d0 / 2, -0.004)
    y.yuz_yon([fa, fb, tb, ta], 'toprak', V(-1, 0, 0.5))
    y.yuz_yon([ua, ub, bb, ba], 'toprak_ot', V(1, 0, 0.5))
    # the stacked turves on the front: grassy courses a hair proud of the earth (the butt reads as a built bank)
    fn = V(-h, 0, (d0 - d1) / 2).normalized() * 0.0015
    for j in range(1, 6):
        t0, t1 = j / 6 - 0.035, j / 6
        P = lambda t, a: (fa if a else fb).lerp(ta if a else tb, t) + fn
        y.yuz_yon([P(t0, 1), P(t0, 0), P(t1, 0), P(t1, 1)], 'cimen_kuru', V(-1, 0, 0.5))
    y.yuz_yon([ta, tb, ub, ua], 'cimen_kuru', Z)
    y.yuz_yon([fa, ta, ua, ba], 'toprak', -Y)
    y.yuz_yon([fb, tb, ub, bb], 'toprak', Y)
    # stacked sods showing on the ends: bands of turf a hair proud
    for s, yy in ((-1, cy - L / 2 - 0.0012), (1, cy + L / 2 + 0.0012)):
        for j in range(1, 5):
            z0_, z1_ = h * j / 5 - 0.008, h * j / 5
            w0, w1 = d0 + (d1 - d0) * z0_ / h, d0 + (d1 - d0) * z1_ / h
            y.yuz_yon([V(cx - w0 / 2 + 0.004, yy, G + z0_), V(cx + w0 / 2 - 0.004, yy, G + z0_), V(cx + w1 / 2 - 0.004, yy, G + z1_),
                       V(cx - w1 / 2 + 0.004, yy, G + z1_)], 'cimen_kuru', V(0, s))
    # a timber revetment along the foot of the front
    cubuk(y, V(cx - d0 / 2 - 0.004, cy - L / 2, G + 0.008), V(cx - d0 / 2 - 0.004, cy + L / 2, G + 0.008), 0.008, AHS, 0.016)


def hedef(cx, cy, r=0.085, z=G + 0.115):
    """a straw target boss on a tripod, facing -x, tilted back, with painted rings and arrows in it"""
    eg = 0.25
    n = V(-math.cos(eg), 0, math.sin(eg))       # its face normal
    up = V(math.sin(eg), 0, math.cos(eg))
    ey = Y
    o = V(cx, cy, z)
    P = lambda rr, t, d: o + ey * (rr * math.cos(t)) + up * (rr * math.sin(t)) + n * d
    N = 20
    # the straw boss: a thick disc
    for i in range(N):
        t0, t1 = TAU * i / N, TAU * (i + 1) / N
        q = [P(r, t0, -0.022), P(r, t1, -0.022), P(r, t1, 0.0), P(r, t0, 0.0)]
        y.yuz_yon(q, 'saz', (q[0] + q[1]) / 2 - (o + n * -0.011))
    y.yuz_yon([P(r, TAU * i / N, -0.022) for i in range(N)], 'saz_koyu', -n)
    # painted face: rings, each a hair in front of the one below
    for k, (rr, key) in enumerate(((r * 0.96, 'beyaz'), (r * 0.78, 'koyu'), (r * 0.6, 'boya_kirmizi'), (r * 0.4, 'beyaz'), (r * 0.2, 'altin'))):
        y.yuz_yon([P(rr, TAU * i / N, 0.0006 + 0.0006 * k) for i in range(N)], key, n)
    y.yuz_yon([P(r, TAU * i / N, 0.0) for i in range(N)], 'saz', n)
    # tripod
    for (dy, dx) in ((-0.03, 0.01), (0.03, 0.01), (0.0, 0.05)):
        cubuk(y, o + up * (-r * 0.2) + n * -0.024, V(cx + dx, cy + dy, G), 0.005, AHS)
    # arrows in the target, their fletchings pointing back to the line
    for k, (rr, t) in enumerate(((0.012, 0.7), (0.026, 2.4), (0.018, 4.1), (0.034, 5.4))):
        p = P(rr, t, 0.002)
        d = (n + V(0, 0.08 * (k - 1.5), -0.06)).normalized()
        cubuk(y, p - d * 0.004, p + d * 0.05, 0.0018, 'ahsap_acik')
        kutu3(y, p + d * 0.045, d, Y, d.cross(Y).normalized(), 0.012, 0.0016, 0.005, 'beyaz')


BX = 0.8
for ly in LANES:
    set_(BX + 0.07, ly)
    hedef(BX - 0.1, ly)
# spent arrows stuck in the turf round the butts
for k in range(14):
    ly = LANES[k % 3] + (((k * 7) % 9) - 4) * 0.022
    x = BX - 0.12 + ((k * 5) % 7) * 0.014
    a = V(x, ly, G - 0.004)
    b = a + V(-0.04, 0.004 * (k % 3 - 1), 0.03)
    cubuk(y, a, b, 0.0018, 'ahsap_acik')
    kutu3(y, b - (b - a).normalized() * 0.005, (b - a).normalized(), Y, (b - a).normalized().cross(Y).normalized(), 0.01, 0.0016, 0.004, 'beyaz')
# a marker flag on each butt (red and white: the shoot is on)
for ly in LANES:
    p = V(BX + 0.07, ly + 0.13)
    cubuk(y, p + Z * (G + 0.1), p + Z * (G + 0.24), 0.004, AHS)
    levha(y, [p + Z * (G + 0.235), p + V(0.045, 0, G + 0.225), p + Z * (G + 0.205)], 'boya_kirmizi', Y, 0.0012)

# arrows in flight (arcing towards the butts)
for k, (x0, ly, z0) in enumerate(((0.05, LANES[0] + 0.02, 0.26), (0.35, LANES[1] - 0.03, 0.28), (0.58, LANES[2], 0.22), (-0.12, LANES[1] + 0.04, 0.18))):
    d = V(1, 0, -0.12 * k + 0.08).normalized()
    a = V(x0, ly, G + z0)
    cubuk(y, a, a + d * 0.06, 0.0022, 'ahsap_acik')
    kutu3(y, a + d * 0.006, d, Y, d.cross(Y).normalized(), 0.012, 0.0016, 0.006, 'beyaz')

# ---------------------------------------------------------------- the archers
y.bolum('Atış çizgisinde okçular')
renkler = ['boya_yesil', 'kumas', 'ahsap_acik', 'boya_yesil', 'kerpic_koyu', 'boya_kirmizi', 'boya_yesil']
k = 0
for ly in LANES:
    for dy in (-0.05, 0.05):
        okcu(y, SL - 0.035, ly + dy, G, aci=0.06 * dy * 10, s=2.0, key=renkler[k % len(renkler)], cek=1.0 if k % 2 else 0.6,
             sapka='kece' if k % 3 else 'ahsap_koyu')
        # a sheaf of arrows stuck in the ground before each archer
        base = V(SL + 0.03, ly + dy + 0.025)
        for j in range(5):
            a = TAU * j / 5
            p = base + V(math.cos(a), math.sin(a)) * 0.005
            tip = p + V(math.cos(a), math.sin(a)) * 0.008 + Z * 0.065
            cubuk(y, V(p.x, p.y, G - 0.004), V(tip.x, tip.y, G + 0.065), 0.002, 'ahsap_acik')
            kutu3(y, V(tip.x, tip.y, G + 0.058), Z, V(math.cos(a), math.sin(a)), V(-math.sin(a), math.cos(a)), 0.012, 0.0016, 0.005, 'beyaz')
        k += 1
# the master of the range in red with a white wand, a boy fetching arrows
insan(y, -0.46, -0.78, G, 'boya_kirmizi', s=1.15, aci=0.6, sapka='koyu')
cubuk(y, V(-0.448, -0.772, G + 0.03), V(-0.43, -0.76, G + 0.1), 0.0025, 'beyaz')
insan(y, 0.66, LANES[1] + 0.09, G, 'kumas', s=0.85, aci=math.pi, kol=0.8)
# onlookers on the side
for k, (x, yy, a) in enumerate(((-0.25, 0.2, -1.6), (-0.2, 0.15, -1.4), (0.6, 0.12, -1.7), (0.3, -0.85, 1.6), (0.38, -0.84, 1.5))):
    insan(y, x, yy, G, ['kumas', 'boya_kirmizi', 'ahsap_acik', 'boya_yesil', 'kece'][k], s=1.05, aci=a, sapka='saz' if k % 2 else None)

# ---------------------------------------------------------------- the spectators' stand
y.bolum('Seyirci locası (ahşap, kiremit sundurmalı)')
SX0_, SX1_, SY0_, SY1_ = -0.12, 0.5, 0.2, 0.32
ZB_ = G + 0.11
# a raised timber floor on posts, a back wall of boards, a lean-to tiled roof on posts, benches, a rail
kutu(y, V(SX0_, SY0_, ZB_ - 0.008), X, SX1_ - SX0_, SY1_ - SY0_, 0.008, 'ahsap', 'onarkasagsolust')
y.yuz_yon([V(SX0_, SY0_, ZB_ - 0.008), V(SX1_, SY0_, ZB_ - 0.008), V(SX1_, SY1_, ZB_ - 0.008), V(SX0_, SY1_, ZB_ - 0.008)], AHS, -Z)
nP = 7
for j in range(nP + 1):
    x = SX0_ + (SX1_ - SX0_) * j / nP
    cubuk(y, V(x, SY0_ + 0.006, G), V(x, SY0_ + 0.006, ZB_ + 0.13), 0.009, AHS)
    cubuk(y, V(x, SY1_ - 0.006, G), V(x, SY1_ - 0.006, ZB_ + 0.17), 0.009, AHS)
    if j < nP:   # cross braces under the floor
        cubuk(y, V(x, SY0_ + 0.006, G + 0.01), V(x + (SX1_ - SX0_) / nP, SY0_ + 0.006, ZB_ - 0.015), 0.005, AHS, 0.004)
duz_duvar(y, V(SX1_, SY1_), V(SX0_, SY1_), ZB_, ZB_ + 0.17, 'ahsap_dikey')
duz_duvar(y, V(SX0_, SY1_ - 0.004), V(SX1_, SY1_ - 0.004), ZB_, ZB_ + 0.17, 'ahsap_dikey')
cubuk(y, V(SX0_, SY0_ + 0.004, ZB_ + 0.045), V(SX1_, SY0_ + 0.004, ZB_ + 0.045), 0.006, AHS)
for (yy, zz) in ((SY0_ + 0.035, 0.022), (SY0_ + 0.075, 0.04)):
    kutu(y, V(SX0_ + 0.01, yy - 0.012, ZB_), X, SX1_ - SX0_ - 0.02, 0.024, zz, 'ahsap_acik', 'onarkasagsolust')
q = [V(SX0_ - 0.02, SY0_ - 0.03, ZB_ + 0.13), V(SX1_ + 0.02, SY0_ - 0.03, ZB_ + 0.13), V(SX1_ + 0.02, SY1_ + 0.01, ZB_ + 0.18), V(SX0_ - 0.02, SY1_ + 0.01, ZB_ + 0.18)]
y.yuz_yon(q, 'kiremit', V(0, -0.6, 1))
y.yuz_yon([p - Z * 0.008 for p in q], AHS, -Z)
for (a, b, nrm) in ((q[0], q[1], -Y), (q[1], q[2], X), (q[2], q[3], Y), (q[3], q[0], -X)):
    y.yuz_yon([a, b, b - Z * 0.008, a - Z * 0.008], AHS, nrm)
for j in range(5):   # tile courses
    t = (j + 0.5) / 5
    cubuk(y, q[0].lerp(q[3], t) + Z * 0.002, q[1].lerp(q[2], t) + Z * 0.002, 0.004, 'kiremit2', 0.002)
# red and white pennants along the eave
for j in range(9):
    p = q[0].lerp(q[1], (j + 0.5) / 9) - Z * 0.008
    levha(y, [p - X * 0.014, p + X * 0.014, p - Z * 0.03], 'boya_kirmizi' if j % 2 else 'beyaz', -Y, 0.001)
# the onlookers, seated
for j in range(12):
    x = SX0_ + 0.03 + (SX1_ - SX0_ - 0.06) * j / 11
    row = j % 2
    insan(y, x, SY0_ + 0.035 + row * 0.04, ZB_ - 0.004 + row * 0.018, ['boya_kirmizi', 'kumas', 'boya_yesil', 'lacivert', 'ahsap_acik', 'kece'][j % 6],
          s=1.0, aci=-math.pi / 2, kol=0.6 if j % 4 == 1 else 0.0, sapka='koyu' if j % 3 == 0 else None)
# an ale stall by the stand
AB = V(0.66, 0.26)
kutu_merkez(y, (AB.x, AB.y), 0.1, 0.05, 0.05, 'ahsap', z0=G)
for sx in (-1, 1):
    for sy in (-1, 1):
        cubuk(y, V(AB.x + sx * 0.05, AB.y + sy * 0.03, G), V(AB.x + sx * 0.05, AB.y + sy * 0.03, G + 0.12), 0.006, AHS)
cati_besik(y, AB.x - 0.06, AB.x + 0.06, AB.y - 0.04, AB.y + 0.04, G + 0.12, 0.05, 0.012, 'beyaz', 'boya_kirmizi', ucluk_key='beyaz', uc_sacak=0.01, ns=4, nr=3,
           mahya_en=0.006, dilim=['beyaz', 'boya_kirmizi'])
for k in range(3):
    y.prizma((AB.x - 0.03 + 0.03 * k, AB.y + 0.045), 0.014, G, G + 0.034, 'ahsap_acik', n=10)
insan(y, AB.x - 0.02, AB.y - 0.06, G, 'kerpic_koyu', aci=math.pi / 2, kol=0.7, sapka='kece')

# ---------------------------------------------------------------- the marshal's tent, the bow racks, arrow barrels
y.bolum('Çadır, yay sehpaları, ok fıçıları')
TC = V(-0.2, -0.78)
with parca(y, (TC.x, TC.y, G)):
    cadir(y, (0, 0), 0.08, 0.2, 'beyaz', 'boya_kirmizi', n=16)
# a pennon on the tent pole (red: the team banner is on the tower)
cubuk(y, V(TC.x, TC.y, G + 0.2), V(TC.x, TC.y, G + 0.27), 0.004, AHS)
levha(y, [V(TC.x, TC.y, G + 0.265), V(TC.x + 0.05, TC.y + 0.01, G + 0.255), V(TC.x, TC.y, G + 0.24)], 'boya_kirmizi', Y, 0.0012)
# a trestle table with a bow on it before the tent
kutu_merkez(y, (TC.x + 0.02, TC.y + 0.13), 0.14, 0.05, 0.006, 'ahsap', z0=G + 0.04)
for sx in (-1, 1):
    cubuk(y, V(TC.x + 0.02 + sx * 0.06, TC.y + 0.13, G), V(TC.x + 0.02 + sx * 0.06, TC.y + 0.13, G + 0.04), 0.008, AHS, 0.04)
boru(y, [V(TC.x - 0.04, TC.y + 0.13, G + 0.048), V(TC.x + 0.02, TC.y + 0.14, G + 0.05), V(TC.x + 0.08, TC.y + 0.13, G + 0.048)], 0.0018, 'ahsap_acik', n=4)
# bow racks: an A-frame with longbows leaning on its rail
for (rx, ry) in ((-0.5, -0.45), (-0.5, -0.05)):
    for s in (-1, 1):
        cubuk(y, V(rx - 0.02, ry + s * 0.08, G), V(rx, ry + s * 0.08, G + 0.08), 0.006, AHS)
        cubuk(y, V(rx + 0.02, ry + s * 0.08, G), V(rx, ry + s * 0.08, G + 0.08), 0.006, AHS)
    cubuk(y, V(rx, ry - 0.09, G + 0.078), V(rx, ry + 0.09, G + 0.078), 0.007, AHS)
    for j in range(7):
        yy = ry - 0.07 + 0.14 * j / 6
        boru(y, [V(rx - 0.028, yy, G), V(rx - 0.008, yy + 0.002, G + 0.06), V(rx + 0.004, yy, G + 0.12)], 0.0022, 'ahsap_acik' if j % 2 else 'ahsap', n=4)
# arrow barrels (the fletchings showing)
for k, (bx, by) in enumerate(((-0.46, -0.25), (-0.46, -0.2), (-0.46, 0.12), (-0.12, -0.72))):
    y.prizma((bx, by), 0.016, G, G + 0.04, 'ahsap_acik', n=10)
    halka_kornis(y, (bx, by), 0.016, G + 0.01, 0.003, 0.001, 10, 'demir')
    halka_kornis(y, (bx, by), 0.016, G + 0.03, 0.003, 0.001, 10, 'demir')
    for j in range(9):
        a = TAU * j / 9
        p = V(bx + 0.009 * math.cos(a), by + 0.009 * math.sin(a))
        cubuk(y, V(p.x, p.y, G + 0.035), V(p.x + 0.003 * math.cos(a), p.y + 0.003 * math.sin(a), G + 0.07), 0.0016, 'ahsap_acik')
        kutu3(y, V(p.x + 0.003 * math.cos(a), p.y + 0.003 * math.sin(a), G + 0.064), Z, V(math.cos(a), math.sin(a)), V(-math.sin(a), math.cos(a)),
              0.012, 0.0016, 0.006, 'beyaz' if j % 3 else 'boya_kirmizi')

# ---------------------------------------------------------------- the bowyer's workshop
y.bolum('Yay ustası atölyesi (yarı ahşap)')
WX0, WX1, WY0, WY1 = -1.02, -0.68, -0.8, -0.56
WZ1 = G + 0.13
WZU = WZ1 + 0.12
JW = 0.022
# ground floor: a timber frame with a wide open shop front (shutter let down as a counter) facing -y
acs = acikli_duvar(y, V(WX0, WY0), V(WX1, WY0), G, WZ1, [(0.3, 0.12, 0.035, 0.11), (0.78, 0.045, 0.0, 0.11)], ('siva', AHS, 'ahsap_acik', 'koyu'), derin=0.02)
yari_ahsap(y, V(WX0, WY0), V(WX1, WY0), G, WZ1, [(0.3 - 0.06 / 0.34 - 0.01, 0.3 + 0.06 / 0.34 + 0.01, 0.035, 0.11), (0.78 - 0.035, 0.78 + 0.035, 0.0, 0.11)],
           AHS, aralik=0.04, en=0.007, capraz=True)
pa, pb, v0, v1, e, nc = acs[0]
kutu3(y, (pa + pb) / 2 + nc * 0.014 + Z * (G + 0.033), e, nc, Z, (pb - pa).length + 0.01, 0.028, 0.005, 'ahsap')   # the counter
for j in range(2):   # brackets under it
    p = pa.lerp(pb, 0.15 + 0.7 * j)
    cubuk(y, p + nc * 0.002 + Z * (G + 0.012), p + nc * 0.026 + Z * (G + 0.031), 0.005, AHS)
for j in range(4):   # bows laid on the counter, staves stood in the shop
    boru(y, [pa.lerp(pb, 0.1) + nc * (0.008 + j * 0.005) + Z * (G + 0.037), pa.lerp(pb, 0.9) + nc * (0.008 + j * 0.005) + Z * (G + 0.038)], 0.0016, 'ahsap_acik', n=4)
for (a, b, dis) in ((V(WX1, WY0), V(WX1, WY1), (1, 0)), (V(WX1, WY1), V(WX0, WY1), (0, 1)), (V(WX0, WY1), V(WX0, WY0), (-1, 0))):
    ahsap_kat(y, a, b, G, WZ1, [(0.5, 0.05, 0.04, 0.1)], 'siva', AHS, aralik=0.04, capraz=True)
silme(y, dikdortgen(WX0, WX1, WY0, WY1), G, 0.014, 0.005, 'granit', 'kaide')
# upper storey jettied over the front
uk = [V(WX0, WY0 - JW), V(WX1, WY0 - JW), V(WX1, WY1), V(WX0, WY1)]
for i, n_ in enumerate((2, 1, 2, 1)):
    a, b = uk[i], uk[(i + 1) % 4]
    ps = [((j + 0.5) / n_, 0.06, 0.03, 0.095) for j in range(n_)]
    ahsap_kat(y, a, b, WZ1, WZU, ps, 'siva', AHS, aralik=0.024)
y.yuz_yon([V(WX0, WY0 - JW, WZ1), V(WX1, WY0 - JW, WZ1), V(WX1, WY0, WZ1), V(WX0, WY0, WZ1)], AHS, -Z)
cubuk(y, V(WX0, WY0 - JW - 0.004, WZ1 + 0.004), V(WX1, WY0 - JW - 0.004, WZ1 + 0.004), 0.012, AHS, 0.01)
for j in range(1, 12):
    p = V(WX0 + (WX1 - WX0) * j / 12, WY0 - JW / 2)
    kutu_merkez(y, (p.x, p.y), 0.008, JW + 0.004, 0.007, AHS, z0=WZ1 - 0.007)
zr = cati_besik(y, WX0, WX1, WY0 - JW, WY1, WZU, 0.14, 0.026, 'saz', 'saz_koyu', ucluk_key='siva', uc_sacak=0.018, ns=6, nr=6, mahya_en=0.016)
for sx in (-1, 1):   # the gables' timbers
    xg = (WX0 if sx < 0 else WX1) + sx * 0.003
    yc = (WY0 - JW + WY1) / 2
    cubuk(y, V(xg, yc, WZU), V(xg, yc, WZU + 0.12), 0.006, AHS, 0.004)
    for s in (-1, 1):
        cubuk(y, V(xg, yc + s * 0.1, WZU + 0.004), V(xg, yc, WZU + 0.07), 0.005, AHS, 0.004)
# the brick chimney at the back corner
kutu_merkez(y, (WX1 - 0.05, WY1 + 0.02), 0.06, 0.04, zr + 0.04 - G, 'tugla', z0=G)
baca(y, WX1 - 0.05, WY1 + 0.02, zr + 0.0, zr + 0.04, 0.06, 0.04, 2, 0.06)
# the hanging sign: a bow on a bracket
bp = V(WX0 + 0.04, WY0 - JW - 0.004)
cubuk(y, V(bp.x, bp.y, WZ1 + 0.06), V(bp.x, bp.y - 0.06, WZ1 + 0.06), 0.005, 'demir')
cubuk(y, V(bp.x, bp.y, WZ1 + 0.02), V(bp.x, bp.y - 0.045, WZ1 + 0.058), 0.003, 'demir')
levha(y, [V(bp.x, bp.y - 0.02, WZ1 + 0.055), V(bp.x, bp.y - 0.058, WZ1 + 0.055), V(bp.x, bp.y - 0.058, WZ1 + 0.015), V(bp.x, bp.y - 0.02, WZ1 + 0.015)],
      'ahsap_acik', X, 0.003)
for s in (-1, 1):
    boru(y, [V(bp.x + s * 0.0022, bp.y - 0.026, WZ1 + 0.05), V(bp.x + s * 0.0022, bp.y - 0.046, WZ1 + 0.035), V(bp.x + s * 0.0022, bp.y - 0.026, WZ1 + 0.02)],
         0.0016, 'boya_kirmizi', n=4)
# staves drying against a rail outside, billets of yew, the bowyer at his bench
for j in range(9):
    xx = WX0 - 0.02 + 0.012 * 0
    yy = WY0 + 0.02 + j * 0.022
    cubuk(y, V(WX0 - 0.045, yy, G), V(WX0 - 0.006, yy, G + 0.15), 0.005, 'ahsap_acik' if j % 2 else 'kum_koyu')
cubuk(y, V(WX0 - 0.004, WY0 + 0.01, G + 0.14), V(WX0 - 0.004, WY0 + 0.22, G + 0.14), 0.007, AHS)
for j in range(6):
    p = V(-0.66 + 0.018 * (j % 3), -0.48 + 0.02 * (j // 3))
    boru(y, [V(p.x - 0.04, p.y, G + 0.008 + 0.014 * (j // 3)), V(p.x + 0.04, p.y, G + 0.008 + 0.014 * (j // 3))], 0.008, 'kutuk', n=6)
kutu_merkez(y, (-0.8, -0.9), 0.12, 0.035, 0.006, 'ahsap', z0=G + 0.035)
for sx in (-1, 1):
    kutu_merkez(y, (-0.8 + sx * 0.05, -0.9), 0.008, 0.03, 0.035, AHS, z0=G)
boru(y, [V(-0.855, -0.9, G + 0.044), V(-0.8, -0.894, G + 0.046), V(-0.745, -0.9, G + 0.044)], 0.0022, 'ahsap_acik', n=4)
insan(y, -0.8, -0.935, G, 'ahsap_koyu', s=1.1, aci=math.pi / 2, kol=0.5, sapka='kece')

# ---------------------------------------------------------------- the village church
y.bolum('Köy kilisesi: nef ve şansel')
CY0, CY1 = 0.46, 0.66              # the nave's sides
CYM = (CY0 + CY1) / 2
TX0, TX1 = -1.08, -0.86            # the west tower
NX1 = -0.42                        # the nave's east end
CX1 = -0.24                        # the chancel's east end
ZN = G + 0.2                       # nave walls
for (yy, dis) in ((CY0, (0, -1)), (CY1, (0, 1))):
    xs = [TX1 + (NX1 - TX1) * k / 4 for k in range(5)]
    for k in range(4):
        gotik_pencere(y, *sirala(V(xs[k], yy), V(xs[k + 1], yy), dis), G, ZN - G, en=0.5, sivri=0.55, v0=0.06, ust=0.025, derin=0.014,
                      cam='cam', duvar=DUV, iz=DR)
    # buttresses between bays
    for k in range(1, 4):
        kutu3(y, V(xs[k], yy + dis[1] * 0.012, G + 0.075), X, Y, Z, 0.022, 0.024, 0.15, DUV, ('+x', '-x', '+y', '-y', '+z'))
        y.yuz_yon([V(xs[k] - 0.011, yy + dis[1] * 0.024, G + 0.15), V(xs[k] + 0.011, yy + dis[1] * 0.024, G + 0.15), V(xs[k] + 0.011, yy, G + 0.17),
                   V(xs[k] - 0.011, yy, G + 0.17)], DR, V(0, dis[1], 1))
        for s in (-1, 1):
            y.yuz_yon([V(xs[k] + s * 0.011, yy + dis[1] * 0.024, G + 0.15), V(xs[k] + s * 0.011, yy, G + 0.17), V(xs[k] + s * 0.011, yy, G + 0.15)], DUV, V(s, 0))
duz_duvar(y, *sirala(V(NX1, CY0), V(NX1, CY0 + 0.03), (1, 0)), G, ZN, DUV)
duz_duvar(y, *sirala(V(NX1, CY1 - 0.03), V(NX1, CY1), (1, 0)), G, ZN, DUV)
silme(y, [V(TX1, CY0), V(NX1, CY0)], ZN - 0.01, 0.012, 0.01, DR, 'tac', kapali=False)
silme(y, [V(NX1, CY1), V(TX1, CY1)], ZN - 0.01, 0.012, 0.01, DR, 'tac', kapali=False)
silme(y, dikdortgen(TX1, NX1, CY0, CY1), G, 0.02, 0.006, 'granit', 'kaide')
cati_besik(y, TX1, NX1, CY0, CY1, ZN, 0.15, 0.022, 'arduvaz', 'kursun', ucluk_key=DUV, uc_sacak=0.0, ns=8, nr=6, mahya_en=0.011)
# the east gable's cross
hac(y, NX1 + 0.002, CYM, ZN + 0.15, 0.05, DR)
# the chancel, lower and narrower, with its east window
ZC = G + 0.17
for (yy, dis) in ((CY0 + 0.03, (0, -1)), (CY1 - 0.03, (0, 1))):
    gotik_pencere(y, *sirala(V(NX1, yy), V(CX1, yy), dis), G, ZC - G, en=0.4, sivri=0.6, v0=0.06, ust=0.02, derin=0.012, cam='cam', duvar=DUV, iz=DR)
gotik_pencere(y, *sirala(V(CX1, CY0 + 0.03), V(CX1, CY1 - 0.03), (1, 0)), G, ZC - G + 0.02, en=0.55, sivri=0.6, v0=0.05, ust=0.02, derin=0.014,
              cam='cam', duvar=DUV, iz=DR)
silme(y, dikdortgen(NX1, CX1, CY0 + 0.03, CY1 - 0.03), G, 0.02, 0.006, 'granit', 'kaide')
cz = cati_besik(y, NX1, CX1, CY0 + 0.03, CY1 - 0.03, ZC + 0.02, 0.12, 0.02, 'arduvaz', 'kursun', ucluk_key=DUV, uc_sacak=0.014, ns=5, nr=5, mahya_en=0.01)
hac(y, CX1 + 0.012, CYM, cz - 0.004, 0.045, DR)
# the south porch (towards the street)
PX0, PX1 = -0.7, -0.6
PY = CY0 - 0.09
kapi(y, *sirala(V(PX0, PY), V(PX1, PY), (0, -1)), G, 0.6, 0.12, (DUV, 'tas_koyu', DR, 'koyu'), sivri=0.5, derin=0.02, cerceve=(0.006, DR))
for (x, dis) in ((PX0, (-1, 0)), (PX1, (1, 0))):
    duz_duvar(y, *sirala(V(x, PY), V(x, CY0), dis), G, G + 0.12, DUV)
cati_besik(y, PX0, PX1, PY, CY0 + 0.04, G + 0.12, 0.07, 0.014, 'arduvaz', 'kursun', ucluk_key=DUV, uc_sacak=0.01, ns=3, nr=4, mahya_en=0.008)
hac(y, (PX0 + PX1) / 2, PY - 0.006, G + 0.19, 0.035, DR)

y.bolum('Köy kilisesi: dik gotik batı kulesi')
TW = TX1 - TX0
TYC = CYM
TY0, TY1 = TYC - TW / 2, TYC + TW / 2
tk = dikdortgen(TX0, TX1, TY0, TY1)
Z1, Z2, Z3 = G + 0.3, G + 0.47, G + 0.68
# stage 1: the west door with a big window over it; plain faces with a lancet
for i in range(4):
    a, b = tk[i], tk[(i + 1) % 4]
    if i == 3:   # -x: the west face
        kapi(y, a, b, G, 0.34, 0.13, (DUV, 'tas_koyu', DR, 'ahsap'), sivri=0.45, derin=0.02, cerceve=(0.007, DR))
        gotik_pencere(y, a, b, G + 0.13, Z1 - G - 0.13, en=0.5, sivri=0.6, v0=0.02, ust=0.02, derin=0.016, cam='cam', duvar=DUV, iz=DR)
    elif i == 1:   # the nave's side: hidden below the roof
        duz_duvar(y, a, b, G, Z1, DUV)
    else:
        duz_duvar(y, a, b, G, G + 0.12, DUV)
        gotik_pencere(y, a, b, G + 0.12, Z1 - G - 0.12, en=0.26, sivri=0.7, v0=0.03, ust=0.025, derin=0.014, cam='cam', duvar=DUV, iz=DR, izli=False)
# stage 2: a small lancet and a clock face
for i in range(4):
    a, b = tk[i], tk[(i + 1) % 4]
    gotik_pencere(y, a, b, Z1, Z2 - Z1, en=0.22, sivri=0.7, v0=0.075, ust=0.02, derin=0.012, cam='koyu', duvar=DUV, iz=DR, izli=False)
    if i in (0, 3):
        a2, b2, L, e, nc = eksen(a, b)
        o = a2.lerp(b2, 0.5) + Z * (Z1 + 0.04)
        y.oculus(o, e, nc, 0.026, 'boya_kirmizi', DR, f=0.005, k=16)
        y.oculus(o + nc * 0.0006, e, nc, 0.02, 'beyaz', 'altin', f=0.002, k=16)
        for (ang, ln) in ((math.pi / 2, 0.016), (math.pi / 6, 0.011)):
            d = e * math.cos(ang) + Z * math.sin(ang)
            cubuk(y, o + nc * 0.0045, o + nc * 0.0045 + d * ln, 0.0025, 'koyu', 0.001)
# stage 3: the belfry, paired louvred lancets on every face
for i in range(4):
    a, b = tk[i], tk[(i + 1) % 4]
    a2, b2, L, e, nc = eksen(a, b)
    for j in range(2):
        p, q = a2.lerp(b2, j / 2), a2.lerp(b2, (j + 1) / 2)
        gotik_pencere(y, p, q, Z2, Z3 - Z2, en=0.56, sivri=0.65, v0=0.02, ust=0.02, derin=0.016, cam='koyu', duvar=DUV, iz=DR, izli=False)
        for jj in range(6):
            zz = Z2 + 0.04 + jj * 0.022
            kutu3(y, p.lerp(q, 0.5) - nc * 0.008 + Z * zz, e, nc, Z, L / 2 * 0.5, 0.003, 0.005, AHS, ('+y', '+z'))
for zz, pr in ((Z1 - 0.004, 'duz'), (Z2 - 0.004, 'duz')):
    silme(y, tk, zz, 0.01, 0.008, DR, pr)
silme(y, tk, Z3 - 0.01, 0.016, 0.012, DR, 'tac')
# angle buttresses at every corner, stepping back in stages
for p in tk:
    sx_ = 1 if p.x > (TX0 + TX1) / 2 else -1
    sy_ = 1 if p.y > TYC else -1
    for (d, along) in ((V(sx_, 0), V(0, -sy_)), (V(0, sy_), V(-sx_, 0))):
        for st, (z0_, z1_, dd) in enumerate(((G, G + 0.2, 0.034), (G + 0.2, Z1 + 0.06, 0.026), (Z1 + 0.06, Z2 + 0.06, 0.018))):
            c = V(p.x, p.y) + d * (dd / 2) + along * 0.016
            kutu3(y, c + Z * ((z0_ + z1_) / 2), d, along, Z, dd, 0.026, z1_ - z0_, DUV, ('+x', '+y', '-y'))
            # the weathering on top of each stage
            c0 = V(p.x, p.y) + along * 0.016
            q = [c0 + d * dd - along * 0.013 + Z * z1_, c0 + d * dd + along * 0.013 + Z * z1_, c0 + d * 0.0 + along * 0.013 + Z * (z1_ + dd * 0.8),
                 c0 + d * 0.0 - along * 0.013 + Z * (z1_ + dd * 0.8)]
            y.yuz_yon(q, DR, d + Z)
            for s in (-1, 1):
                y.yuz_yon([c0 + d * dd + along * (s * 0.013) + Z * z1_, c0 + along * (s * 0.013) + Z * z1_, c0 + along * (s * 0.013) + Z * (z1_ + dd * 0.8)],
                          DUV, along * s)
# battlements and pinnacles
td = disa(tk, 0.012)
parapet(y, td, Z3 + 0.006, 0.02, 0.026, 0.014, DUV, ust_key=DR)
y.yuz_yon([V(p.x, p.y, Z3 + 0.006) for p in tk], 'kursun', Z)
for p in td:
    fiyal(y, p.x, p.y, 0.026, Z3 + 0.006, 0.06, 0.08, DUV, tip_key=DR)
for i in range(4):
    m = td[i].lerp(td[(i + 1) % 4], 0.5)
    fiyal(y, m.x, m.y, 0.016, Z3 + 0.026, 0.03, 0.045, DUV, tip_key=DR, gablet=False)
# the stair turret on the south-east corner, rising above the parapet with a little spirelet
SC = V(TX1 + 0.012, TY0 - 0.012)
y.prizma((SC.x, SC.y), 0.026, G, Z3 + 0.03, DUV, n=8, ust=False, kat=math.pi / 8)
for zz in (Z1 - 0.004, Z2 - 0.004, Z3 - 0.01):
    halka_kornis(y, SC, 0.026, zz, 0.01, 0.006, 8, DR, kat=math.pi / 8)
for zz in (G + 0.1, G + 0.22, Z1 + 0.08, Z2 + 0.08):
    nn = V(-0.7, -0.7).normalized()
    yarik(y, SC + nn * (0.026 * math.cos(math.pi / 8) + 0.001), V(-nn.y, nn.x), nn, -0.003, zz, 0.006, 0.025, 'koyu')
sr = cokgen(SC, 0.03, 8, math.pi / 8)
for i in range(8):
    mazgal(y, sr[i], sr[(i + 1) % 8], Z3 + 0.03, 0.016, 0.008, DUV, dis_en=0.012, bosluk=0.03)
y.yuz_yon([V(p.x, p.y, Z3 + 0.03) for p in sr], 'kursun', Z)
donel(y, SC, [(0.022, Z3 + 0.03), (0.0, Z3 + 0.13)], 'kursun', n=8, kat=math.pi / 8)
y.prizma((SC.x, SC.y), 0.0025, Z3 + 0.125, Z3 + 0.16, 'altin', n=4)
levha(y, [V(SC.x, SC.y, Z3 + 0.15), V(SC.x + 0.026, SC.y, Z3 + 0.146), V(SC.x + 0.026, SC.y, Z3 + 0.158)], 'altin', Y, 0.0015)
y.bolum('Sancak')
sancak(y, (TX0 + TX1) / 2, TYC, Z3 + 0.006, boy=0.24, en=0.14, yuk=0.085, aci=-math.pi * 0.3)

# ---------------------------------------------------------------- churchyard, lychgate
y.bolum('Kilise avlusu, mezar taşları, porsuk, lychgate')
yard = [V(-1.12, 0.3), V(-0.18, 0.3), V(-0.18, 0.88), V(-1.12, 0.88)]
GT0, GT1 = -0.69, -0.61
alcak_duvar(y, [V(GT0, 0.3), V(-1.12, 0.3), V(-1.12, 0.88), V(-0.18, 0.88), V(-0.18, 0.3), V(GT1, 0.3)][::-1], G, 0.04, 0.02, 'granit', DR)
# the lychgate: a timber roofed gate over the path
for x in (GT0, GT1):
    for yy in (0.27, 0.33):
        cubuk(y, V(x, yy, G), V(x, yy, G + 0.08), 0.008, AHS)
    cubuk(y, V(x, 0.27, G + 0.078), V(x, 0.33, G + 0.078), 0.008, AHS)
cubuk(y, V(GT0, 0.27, G + 0.078), V(GT1, 0.27, G + 0.078), 0.008, AHS)
cubuk(y, V(GT0, 0.33, G + 0.078), V(GT1, 0.33, G + 0.078), 0.008, AHS)
cati_besik(y, GT0 - 0.004, GT1 + 0.004, 0.27, 0.33, G + 0.082, 0.05, 0.018, 'arduvaz', 'kursun', ucluk_key=AHS, uc_sacak=0.014, ns=3, nr=3, mahya_en=0.006)
# the path to the porch
y.yuz_yon([V(GT0 + 0.01, 0.27, G + 0.0035), V(GT1 - 0.01, 0.27, G + 0.0035), V(GT1 - 0.01, PY, G + 0.0035), V(GT0 + 0.01, PY, G + 0.0035)], 'tas_acik', Z)
# gravestones, a churchyard cross, the old yew
for k in range(14):
    x = -1.06 + 0.07 * (k % 7) + 0.02 * (k // 7)
    yy = 0.36 + 0.045 * (k // 7)
    if GT0 - 0.03 < x < GT1 + 0.03: continue
    with parca(y, (x, yy, G), 0.08 * ((k * 3) % 5 - 2)):
        kutu_merkez(y, (0, 0), 0.024, 0.006, 0.026, 'granit' if k % 3 else 'granit_koyu')
        y.yuz_yon([V(-0.012, 0.003, 0.026), V(0.012, 0.003, 0.026), V(0.0, 0.003, 0.036)], 'granit' if k % 3 else 'granit_koyu', Y)
        y.yuz_yon([V(-0.012, -0.003, 0.026), V(0.012, -0.003, 0.026), V(0.0, -0.003, 0.036)], 'granit' if k % 3 else 'granit_koyu', -Y)
        for s in (-1, 1):
            y.yuz_yon([V(s * 0.012, -0.003, 0.026), V(s * 0.012, 0.003, 0.026), V(0, 0.003, 0.036), V(0, -0.003, 0.036)], 'granit' if k % 3 else 'granit_koyu', V(s, 0, 1))
kutu_merkez(y, (-0.3, 0.76), 0.04, 0.04, 0.03, 'granit', z0=G)
kutu_merkez(y, (-0.3, 0.76), 0.012, 0.012, 0.12, DR, z0=G + 0.03)
cubuk(y, V(-0.33, 0.76, G + 0.12), V(-0.27, 0.76, G + 0.12), 0.012, DR)
boru(y, [V(-0.3, 0.38, G - 0.01), V(-0.3, 0.38, G + 0.06)], 0.014, 'ahsap_koyu', n=6)
for k, (dx, dy, dz, rr) in enumerate(((0, 0, 0.1, 0.07), (0.04, 0.02, 0.07, 0.05), (-0.04, -0.01, 0.075, 0.05), (0.0, 0.0, 0.15, 0.05))):
    kure(y, (-0.3 + dx, 0.38 + dy, G + dz), rr, 'yesil_koyu', n=10, kat=5)

# ---------------------------------------------------------------- oaks and cottages
y.bolum('Meşe ağaçları ve köy evleri')
for (x, yy, b, t) in ((0.3, 0.52, 0.32, 0.0), (0.72, 0.5, 0.36, 1.0), (1.02, -0.86, 0.3, 2.0), (-0.98, -0.25, 0.28, 0.5), (0.05, 0.62, 0.26, 1.5),
                     (1.0, 0.22, 0.26, 2.5)):
    mese(x, yy, b, t)
ev(y, 0.48, 0.84, G, 0.24, 0.13, 0.1, 0.0, 'saz', tohum=1)
ev(y, 0.9, 0.84, G, 0.2, 0.12, 0.09, 0.0, 'saz', tohum=2, kapi_u=0.4)
ev(y, 0.62, -0.92, G, 0.2, 0.1, 0.085, math.pi, 'kiremit', tohum=3)
# a horse cart waiting by the street, a couple of sheep on the green
at(y, 0.15, -0.91, G, math.pi, 0.85, 'ahsap', 'ahsap_koyu')
kutu_merkez(y, (0.28, -0.91), 0.12, 0.07, 0.01, 'ahsap', z0=G + 0.03)
for s in (-1, 1):
    duz_duvar(y, *sirala(V(0.22, -0.91 + s * 0.035), V(0.34, -0.91 + s * 0.035), (0, s)), G + 0.04, G + 0.065, 'ahsap_acik')
    duz_duvar(y, *sirala(V(0.22, -0.91 + s * 0.031), V(0.34, -0.91 + s * 0.031), (0, -s)), G + 0.04, G + 0.065, 'ahsap_acik')
    y.yuz_yon([V(0.22, -0.91 + s * 0.035, G + 0.065), V(0.34, -0.91 + s * 0.035, G + 0.065), V(0.34, -0.91 + s * 0.031, G + 0.065), V(0.22, -0.91 + s * 0.031, G + 0.065)], 'ahsap', Z)
for s in (-1, 1):
    with parca(y, (0.28, -0.91 + s * 0.042, G + 0.028), 0.0):
        for i in range(10):
            t0, t1 = TAU * i / 10, TAU * (i + 1) / 10
            P = lambda t, d: V(0.028 * math.cos(t), d, 0.028 * math.sin(t))
            y.yuz_yon([P(t0, -0.003), P(t1, -0.003), P(t1, 0.003), P(t0, 0.003)], 'ahsap_koyu', V(math.cos((t0 + t1) / 2), 0, math.sin((t0 + t1) / 2)))
        y.yuz_yon([V(0.028 * math.cos(TAU * i / 10), s * 0.003, 0.028 * math.sin(TAU * i / 10)) for i in range(10)], 'ahsap_acik', V(0, s))
for j in range(3):   # bundles of staves and sheaves in the cart
    boru(y, [V(0.23, -0.93 + j * 0.02, G + 0.05), V(0.33, -0.93 + j * 0.02, G + 0.05)], 0.008, 'saz', n=6)
cubuk(y, V(0.22, -0.91, G + 0.035), V(0.08, -0.91, G + 0.05), 0.006, AHS)

calistir(y, 'lm_okcutalim')
