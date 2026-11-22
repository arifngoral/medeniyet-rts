# Barut Atölyesi (lm_barutatolye): a Song / Ming gunpowder and rocket works. A walled yard with a grey-tiled workshop
# hall, edge-runner mills and foot-driven mortars that grind the powder, a charcoal kiln, saltpetre drying trays and heaps
# of saltpetre, sulphur and charcoal, stacks of barrels, racks of fire arrows (huo jian), a hive rocket-box cart and
# launching ramps over a test field with targets and scorch marks; a tall brick-and-timber watchtower with the banner.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ek import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(7)
GRI, GRI2 = 'kiremit_koyu', 'kiremit_koyu2'
TUG = 'granit'

# ---------------------------------------------------------------- ground and wall
y.bolum('Zemin ve duvar')
Z0 = zemin(y, -1.15, 1.15, -1.15, 1.15, 0.03, 'tas_koyu', 'toprak', basamak=(('on', 0.36),), n_basamak=2)
kirmizi_sur(y, [V(0.17, -1.07), V(1.07, -1.07), V(1.07, 1.07), V(-1.07, 1.07), V(-1.07, -1.07), V(-0.17, -1.07)], Z0, 0.085, 0.035,
            'kerpic', GRI, GRI2, kapali=False, baslik=0.024, kaide_key=TUG)
# the gatehouse
kucuk_salon(y, -0.19, 0.19, -1.12, -1.02, Z0, 0.085, 0.065, 0.035, 'kerpic', 'ahsap_koyu', GRI, GRI2, 'irimoya', 0.4, 0.025, 0.014, TUG,
            kapi_yon=0, bay=0.063)
# paved strips: the way in and round the workshop
for x0, x1, y0, y1 in ((-0.07, 0.07, -1.0, 0.5), (-0.5, 0.5, 0.5, 0.6)):
    kutu(y, V(x0, y0, Z0), X, x1 - x0, y1 - y0, 0.003, 'zemin', 'onarkasagsolust')

# ---------------------------------------------------------------- the watchtower
y.bolum('Gözcü kulesi')
WC = V(0.8, 0.8)
WB, WT, WH = 0.14, 0.115, 0.48
alt = dikdortgen(WC.x - WB, WC.x + WB, WC.y - WB, WC.y + WB, Z0)
ust = dikdortgen(WC.x - WT, WC.x + WT, WC.y - WT, WC.y + WT, Z0 + WH)
y.serit(alt, ust, TUG)
for k, (u, v) in enumerate(((0.5, 0.22), (0.5, 0.5), (0.5, 0.75))):
    for i in range(4):
        a, b = alt[i], alt[(i + 1) % 4]
        a2, b2 = ust[i], ust[(i + 1) % 4]
        if i == 0 and k == 0:
            continue
        # arrow slits on the battered faces
        pa, pb = a.lerp(a2, v), b.lerp(b2, v)
        o = pa.lerp(pb, u)
        ex = (pb - pa).normalized(); nn = V(ex.y, -ex.x)
        y.yuz_yon([o - ex * 0.006 + nn * 0.0015, o + ex * 0.006 + nn * 0.0015, o + ex * 0.006 + nn * 0.0015 + Z * 0.035, o - ex * 0.006 + nn * 0.0015 + Z * 0.035],
                  'koyu', nn + Z * 0.06)
# the door at its foot (south face)
o = alt[0].lerp(alt[1], 0.5)
y.yuz_yon([o - X * 0.03 + V(0, -0.0015, 0), o + X * 0.03 + V(0, -0.0015, 0), o + X * 0.03 + V(0, -0.0015 + 0.003, 0.07), o - X * 0.03 + V(0, -0.0015 + 0.003, 0.07)],
          'ahsap_koyu', V(0, -1, 0.04))
silme(y, ust, Z0 + WH - 0.016, 0.016, 0.01, TUG, 'kaba')
kd = disa(ust, 0.008)
y.yuz_yon([V(p.x, p.y, Z0 + WH) for p in kd], 'zemin', Z)
parapet(y, kd, Z0 + WH, 0.01, 0.022, 0.012, TUG, ust_key='granit_koyu')
silme(y, alt, Z0 + 0.001, 0.02, 0.006, 'granit_koyu', 'kaide')
# string courses on the battered tower faces
for t in (0.36, 0.68):
    w_ = WB + (WT - WB) * t
    silme(y, dikdortgen(WC.x - w_, WC.x + w_, WC.y - w_, WC.y + w_), Z0 + WH * t - 0.006, 0.012, 0.006, 'granit_koyu', 'kaba')
ZW = Z0 + WH
tp = salon(y, WC.x, WC.y, 0.17, 0.17, ZW, 0.095, 0.1, sacak=0.055, cati_key=GRI, mahya=GRI2, kivrim=0.5, yukari=0.035, cift=True,
           alt_yuk=0.035, ic=0.022, ust_h=0.07, bay=0.085, chiwenli=False, hayvan=0, cati='irimoya', mahya_en=0.009,
           duvar='lake', kafes_key='ahsap_koyu', boya=('boya_yesil', 'lake_koyu'), sus=GRI2)
# the signal drum on the deck and the banner
donel(y, (WC.x - 0.075, WC.y - 0.075), [(0.0, ZW), (0.018, ZW), (0.02, ZW + 0.018), (0.018, ZW + 0.036), (0.0, ZW + 0.036)], 'boya_kirmizi', n=10)
sancak(y, WC.x + 0.09, WC.y - 0.09, ZW + 0.01, boy=0.42, en=0.16, yuk=0.09, aci=-0.6)

# ---------------------------------------------------------------- the workshop hall
y.bolum('Atölye')
kucuk_salon(y, -0.4, 0.4, 0.62, 0.9, Z0, 0.13, 0.13, 0.05, 'kerpic', 'ahsap_koyu', GRI, GRI2, 'irimoya', 0.42, 0.03, 0.025, TUG,
            kapi_yon=0, bay=0.08, arka_duz=True)
# a lean-to porch in front with posts
for i in range(6):
    x = -0.38 + 0.76 * i / 5
    y.prizma((x, 0.56), 0.007, Z0, Z0 + 0.1, 'ahsap_koyu', n=6)
cati_besik(y, -0.4, 0.4, 0.55, 0.62, Z0 + 0.1, 0.025, 0.02, GRI, GRI2, 0.008, 0.0, 'ahsap_koyu', 'ahsap', ns=8, nr=2)
cubuk(y, V(-0.4, 0.556, Z0 + 0.095), V(0.4, 0.556, Z0 + 0.095), 0.01, 'ahsap_koyu')

# ---------------------------------------------------------------- charcoal kiln
y.bolum('Kömür ocağı')
KC = (-0.78, 0.8)
donel(y, KC, [(0.13, Z0), (0.13, Z0 + 0.04), (0.12, Z0 + 0.09), (0.095, Z0 + 0.14), (0.055, Z0 + 0.175), (0.022, Z0 + 0.185), (0.0, Z0 + 0.186)],
      'tugla_koyu', n=16)
kutu(y, V(KC[0] - 0.05, KC[1] - 0.165, Z0), X, 0.1, 0.06, 0.09, 'tugla_koyu', 'sagsolust')
y.kemerli(V(KC[0] - 0.05, KC[1] - 0.165, Z0), V(KC[0] + 0.05, KC[1] - 0.165, Z0), 0, 0.09, ('tugla_koyu', 'koyu', 'koyu', 'koyu'),
          en=0.56, ust=0.016, derin=0.026, k_say=6)
for dx, dy, h in ((0.07, 0.07, 0.3), (-0.06, 0.08, 0.24)):
    y.prizma((KC[0] + dx, KC[1] + dy), 0.018, Z0 + 0.1, Z0 + h, 'tugla', n=6)
    y.prizma((KC[0] + dx, KC[1] + dy), 0.022, Z0 + h - 0.012, Z0 + h, 'tugla_koyu', n=6)
# smoke from the chimneys
for k, (r, dz, dx) in enumerate(((0.018, 0.025, 0.0), (0.022, 0.058, 0.012), (0.026, 0.095, 0.03))):
    kure(y, (KC[0] + 0.07 + dx, KC[1] + 0.07, Z0 + 0.3 + dz), r, 'granit_koyu', n=8, kat=4)
# charcoal heap and baskets
y.koni((KC[0] + 0.18, KC[1] - 0.12), 0.07, Z0, 0.05, 'koyu', n=10)
for dx in (0.26, 0.3):
    donel(y, (KC[0] + dx, KC[1] - 0.22), [(0.0, Z0), (0.014, Z0), (0.02, Z0 + 0.03), (0.016, Z0 + 0.03), (0.0, Z0 + 0.026)], 'saz', n=8)

# ---------------------------------------------------------------- edge-runner mills
y.bolum('Değirmenler')


def degirmen(cx, cy, aci, catili):
    """an edge-runner mill: a round stone trough, a central post, a stone wheel on an arm running in the trough, a push
    pole; catili: a pavilion roof over it"""
    z = Z0
    donel(y, (cx, cy), [(0.13, z), (0.13, z + 0.03), (0.11, z + 0.03), (0.105, z + 0.018), (0.055, z + 0.018), (0.05, z + 0.03),
                        (0.035, z + 0.03), (0.0, z + 0.03)], 'granit', n=20)
    y.prizma((cx, cy), 0.012, z + 0.03, z + 0.1, 'ahsap_koyu', n=8)
    d = V(math.cos(aci), math.sin(aci)); s = V(-d.y, d.x)
    c = V(cx, cy)
    tek = c + d * 0.08
    zc = z + 0.018 + 0.048
    boru(y, [V(tek.x, tek.y, zc) - d * 0.014, V(tek.x, tek.y, zc) + d * 0.014], 0.048, 'granit_koyu', n=14)
    cubuk(y, V(cx, cy, zc), V(tek.x, tek.y, zc) + d * 0.02, 0.008, 'ahsap')
    cubuk(y, V(cx, cy, z + 0.09), V(cx, cy, z + 0.09) + s * 0.22 + Z * 0.005, 0.008, 'ahsap')
    insan(y, cx + s.x * 0.24, cy + s.y * 0.24, z, aci + math.pi, 'kumas', 'saz', 0.065, 0.6)
    if catili:
        for sx in (-1, 1):
            for sy in (-1, 1):
                y.prizma((cx + sx * 0.15, cy + sy * 0.15), 0.008, z, z + 0.13, 'ahsap_koyu', n=6)
        cati_kirma(y, cx - 0.15, cx + 0.15, cy - 0.15, cy + 0.15, z + 0.13, 0.09, 0.04, GRI, GRI2, 0.01, 0.5, 0.03, 'ahsap_koyu',
                   ns=6, nr=4)


degirmen(-0.6, 0.3, 0.4, True)
degirmen(-0.62, -0.12, 2.2, False)

# ---------------------------------------------------------------- foot-driven mortars under a shed
y.bolum('Havanlar')
SX0, SX1, SY0, SY1 = 0.42, 0.95, 0.06, 0.3
for i in range(4):
    x = SX0 + (SX1 - SX0) * i / 3
    for yy in (SY0, SY1):
        y.prizma((x, yy), 0.008, Z0, Z0 + 0.11 + (0.03 if yy == SY1 else 0.0), 'ahsap_koyu', n=6)
kutu(y, V(SX0, SY1 + 0.002, Z0), X, SX1 - SX0, 0.01, 0.13, 'kerpic')
cati_besik(y, SX0 - 0.02, SX1 + 0.02, SY0 - 0.03, SY1 + 0.03, Z0 + 0.12, 0.06, 0.02, GRI, GRI2, 0.008, 0.3, 'ahsap_koyu', 'kerpic',
           ns=8, nr=3)
for i in range(3):
    x = SX0 + (SX1 - SX0) * (i + 0.5) / 3
    my = (SY0 + SY1) / 2 - 0.02
    # the stone mortar sunk in the ground
    donel(y, (x, my - 0.05), [(0.0, Z0 + 0.012), (0.03, Z0), (0.034, Z0 + 0.02), (0.03, Z0 + 0.024), (0.02, Z0 + 0.024), (0.0, Z0 + 0.012)],
          'granit', n=12)
    # the tilt hammer: a pivot frame, the beam rocking on it, the pestle at its head
    for sx in (-1, 1):
        cubuk(y, V(x + sx * 0.02, my + 0.04, Z0), V(x + sx * 0.02, my + 0.04, Z0 + 0.045), 0.008, 'ahsap_koyu')
    cubuk(y, V(x - 0.024, my + 0.04, Z0 + 0.045), V(x + 0.024, my + 0.04, Z0 + 0.045), 0.006, 'ahsap_koyu')
    tilt = 0.18 if i % 2 else -0.05
    b0 = V(x, my + 0.14, Z0 + 0.045 - 0.1 * math.tan(tilt))
    b1 = V(x, my - 0.05, Z0 + 0.045 + 0.09 * math.tan(tilt) + 0.03)
    cubuk(y, b0, b1, 0.012, 'ahsap', 0.014)
    cubuk(y, b1, b1 - Z * 0.035, 0.016, 'granit_koyu')
    insan(y, x + 0.03, my + 0.14, Z0, -math.pi / 2, 'kumas', 'saz', 0.065)

# ---------------------------------------------------------------- saltpetre drying, heaps, barrels
y.bolum('Güherçile kurutma')
for i in range(3):
    for j in range(3):
        x0, y0_ = -0.92 + i * 0.19, -0.92 + j * 0.15
        kutu(y, V(x0, y0_, Z0), X, 0.16, 0.12, 0.012, 'ahsap', 'onarkasagsol')
        y.yuz_yon(dikdortgen(x0 + 0.008, x0 + 0.152, y0_ + 0.008, y0_ + 0.112, Z0 + 0.008), 'beyaz', Z)
        # the rim's top and inner faces
        kd = dikdortgen(x0, x0 + 0.16, y0_, y0_ + 0.12)
        ki = dikdortgen(x0 + 0.008, x0 + 0.152, y0_ + 0.008, y0_ + 0.112)
        for k in range(4):
            q = (k + 1) % 4
            y.yuz_yon([kd[k] + Z * (Z0 + 0.012), kd[q] + Z * (Z0 + 0.012), ki[q] + Z * (Z0 + 0.012), ki[k] + Z * (Z0 + 0.012)], 'ahsap', Z)
            duz_duvar(y, ki[q], ki[k], Z0 + 0.008, Z0 + 0.012, 'ahsap')
# heaps: saltpetre (white), sulphur (yellow), charcoal (black)
for (x, yy, r, h, key) in ((-0.3, -0.85, 0.07, 0.06, 'beyaz'), (-0.3, -0.68, 0.05, 0.045, 'beyaz'), (-0.18, -0.85, 0.055, 0.05, 'boya_sari'),
                           (-0.3, -0.5, 0.05, 0.04, 'koyu')):
    y.koni((x, yy), r, Z0, h, key, n=10)
insan(y, -0.4, -0.72, Z0, 0.5, 'kumas', 'saz', 0.065, 0.5)
insan(y, -0.66, -0.4, Z0, -1.2, 'kumas', 'saz', 0.065, 0.7)
# barrels: stacks by the workshop and the mortar shed
for (x, yy) in ((0.47, 0.5), (0.51, 0.5), (0.55, 0.5), (0.49, 0.46), (0.53, 0.46), (-0.47, 0.5), (-0.43, 0.5), (0.2, -0.05), (0.24, -0.06)):
    fici(y, x, yy, Z0 + 0.003 if abs(x) < 0.5 and 0.5 <= yy <= 0.6 else Z0, 1.0)
for (x, yy) in ((0.49, 0.5), (0.53, 0.5)):
    fici(y, x, yy, Z0 + 0.044, 1.0, yatik=0.0)
for k in range(3):
    fici(y, 0.32 + k * 0.045, 0.4, Z0, 1.0, yatik=math.pi / 2)

# ---------------------------------------------------------------- fire arrows: racks, the hive cart, launching ramps
y.bolum('Ateş okları')


def ok_rafi(cx, cy, aci, n=7):
    """an A-frame rack of fire arrows leaning on a bar: shafts with a paper rocket tube near the head"""
    with parca(y, (cx, cy, Z0), aci):
        for sx in (-1, 1):
            cubuk(y, V(sx * 0.09, -0.03, 0), V(sx * 0.09, 0.0, 0.07), 0.006, 'ahsap_koyu')
            cubuk(y, V(sx * 0.09, 0.03, 0), V(sx * 0.09, 0.0, 0.07), 0.006, 'ahsap_koyu')
        cubuk(y, V(-0.095, 0, 0.068), V(0.095, 0, 0.068), 0.006, 'ahsap_koyu')
        for i in range(n):
            x = -0.075 + 0.15 * i / (n - 1)
            a, b = V(x, 0.05, 0.0), V(x, -0.012, 0.11)
            cubuk(y, a, b, 0.0025, 'ahsap_acik')
            d = (b - a).normalized()
            boru(y, [b - d * 0.035, b - d * 0.005], 0.0045, 'boya_kirmizi', n=5)
            cubuk(y, b, b + d * 0.012, 0.004, 'demir')


ok_rafi(0.18, 0.22, 0.0)
ok_rafi(-0.22, 0.2, 0.3)


def kovan_araba(cx, cy, aci):
    """a wheelbarrow carrying a hive rocket box: a slanted wooden box with a grid of dark mouths"""
    with parca(y, (cx, cy, Z0), aci):
        for sx in (-1, 1):
            boru(y, [V(sx * 0.04, -0.012, 0.03), V(sx * 0.04, 0.012, 0.03)], 0.03, 'ahsap_koyu', n=12)
            cubuk(y, V(sx * 0.03, 0, 0.03), V(sx * 0.03, 0.14, 0.035), 0.008, 'ahsap')
        cubuk(y, V(-0.045, 0, 0.03), V(0.045, 0, 0.03), 0.006, 'demir')
        # the box: front tilted up
        o = V(0, 0.04, 0.045)
        up = V(0, 0.5, 1).normalized()
        ex = V(1, 0, 0); ey = up.cross(ex).normalized() * -1   # back
        w, h, d = 0.07, 0.06, 0.06
        P = lambda u, v, t: o + ex * u + up * v + V(0, 1, 0) * t
        kose = [(-w / 2, 0), (w / 2, 0), (w / 2, h), (-w / 2, h)]
        on = [P(u, v, 0) for u, v in kose]
        ark = [P(u, v, d) for u, v in kose]
        y.yuz_yon(on, 'ahsap', V(0, -1, 0.5))
        y.yuz_yon(ark, 'ahsap', V(0, 1, -0.3))
        for i in range(4):
            j = (i + 1) % 4
            yuz_dis(y, [on[i], on[j], ark[j], ark[i]], 'ahsap', (sum(on, Vector()) + sum(ark, Vector())) / 8)
        nrm = (on[1] - on[0]).cross(on[3] - on[0]).normalized()
        if nrm.y > 0: nrm = -nrm
        for i in range(4):
            for j in range(3):
                c = o + ex * (-w / 2 + w * (i + 0.5) / 4) + up * (h * (j + 0.5) / 3) + nrm * 0.0015
                y.yuz_yon([c - ex * 0.006 - up * 0.006, c + ex * 0.006 - up * 0.006, c + ex * 0.006 + up * 0.006, c - ex * 0.006 + up * 0.006], 'koyu', nrm)


kovan_araba(0.02, -0.25, -0.3)
kovan_araba(0.58, -0.3, 0.6)


def rampa(cx, cy, aci, L=0.32, egim=0.32, oklu=3):
    """a launching ramp: two rails on trestles rising towards aci, rockets laid on it"""
    d = V(math.cos(aci), math.sin(aci)); s = V(-d.y, d.x)
    a = V(cx, cy, Z0)
    for sg in (-1, 1):
        p0 = a + s * (sg * 0.025) + Z * 0.012
        p1 = p0 + d * L + Z * (L * math.tan(egim))
        cubuk(y, p0, p1, 0.008, 'ahsap', 0.01)
        for t in (0.35, 0.7, 1.0):
            q = p0.lerp(p1, t)
            cubuk(y, V(q.x, q.y, Z0), q, 0.008, 'ahsap_koyu')
    for t in (0.35, 0.7, 1.0):
        q = a + d * (L * t) + Z * (0.012 + L * t * math.tan(egim))
        cubuk(y, q - s * 0.03, q + s * 0.03, 0.007, 'ahsap_koyu')
    for k in range(oklu):
        t0 = 0.12 + 0.28 * k
        p = a + d * (L * t0) + Z * (0.012 + L * t0 * math.tan(egim) + 0.012) + s * ((k - 1) * 0.015)
        q = p + (d + Z * math.tan(egim)).normalized() * 0.11
        cubuk(y, p, q, 0.003, 'ahsap_acik')
        e = (q - p).normalized()
        boru(y, [q - e * 0.04, q - e * 0.005], 0.0055, 'boya_kirmizi', n=6)
        cubuk(y, q, q + e * 0.014, 0.005, 'demir')


rampa(0.32, -0.62, -0.55)
rampa(0.45, -0.45, -0.75)
insan(y, 0.28, -0.56, Z0, -0.55, 'kumas', 'saz', 0.065)

# ---------------------------------------------------------------- the test field
y.bolum('Deneme alanı')
# a low fence marking it, scorch marks, targets
for (x, yy, r) in ((0.72, -0.82, 0.07), (0.86, -0.62, 0.05), (0.62, -0.95, 0.04)):
    y.yuz_yon([V(x + r * math.cos(TAU * i / 12) * rn.uniform(0.8, 1.15), yy + r * math.sin(TAU * i / 12) * rn.uniform(0.8, 1.15), Z0 + 0.0015)
               for i in range(12)], 'koyu', Z)
for (x, yy) in ((0.84, -0.88), (0.94, -0.74), (0.76, -0.68)):
    # a straw dummy on a post
    y.prizma((x, yy), 0.005, Z0, Z0 + 0.1, 'ahsap_koyu', n=5)
    donel(y, (x, yy), [(0.0, Z0 + 0.04), (0.02, Z0 + 0.045), (0.022, Z0 + 0.075), (0.012, Z0 + 0.09), (0.0, Z0 + 0.092)], 'saz', n=8)
    cubuk(y, V(x - 0.04, yy, Z0 + 0.075), V(x + 0.04, yy, Z0 + 0.075), 0.007, 'saz')
# a round target board
TB = V(0.95, -0.95)
for sx in (-1, 1):
    cubuk(y, V(TB.x + sx * 0.035, TB.y, Z0), V(TB.x + sx * 0.035, TB.y + 0.02, Z0 + 0.1), 0.007, 'ahsap_koyu')
for k, (r, key) in enumerate(((0.05, 'beyaz'), (0.035, 'boya_kirmizi'), (0.02, 'beyaz'), (0.008, 'boya_kirmizi'))):
    c = V(TB.x, TB.y - 0.004 - k * 0.0015, Z0 + 0.075)
    nn = V(0, -1, 0.15).normalized()
    pts = [c + V(math.cos(TAU * i / 16) * r, 0, math.sin(TAU * i / 16) * r) for i in range(16)]
    y.yuz_yon(pts, key, nn)
    if k == 0:
        y.yuz_yon([p + V(0, 0.006, 0) for p in pts], 'ahsap', -nn)
        for i in range(16):
            j = (i + 1) % 16
            y.yuz_yon([pts[i], pts[j], pts[j] + V(0, 0.006, 0), pts[i] + V(0, 0.006, 0)], 'ahsap', pts[i] - c)
# a rocket in flight over the field, its smoke trail behind it
yol = [V(0.42 + 0.06 * k, -0.62 - 0.045 * k, Z0 + 0.2 + 0.05 * k - 0.006 * k * k) for k in range(6)]
for k, p in enumerate(yol[:-1]):
    kure(y, (p.x, p.y, p.z), 0.008 + 0.0025 * (4 - k), 'granit_koyu' if k < 2 else 'tas_acik', n=6, kat=3)
e = (yol[-1] - yol[-2]).normalized()
cubuk(y, yol[-1] - e * 0.06, yol[-1] + e * 0.03, 0.0035, 'ahsap_acik')
boru(y, [yol[-1], yol[-1] + e * 0.03], 0.006, 'boya_kirmizi', n=6)
kure(y, (yol[-1].x - e.x * 0.012, yol[-1].y - e.y * 0.012, yol[-1].z - e.z * 0.012), 0.009, 'boya_sari', n=6, kat=3)

# ---------------------------------------------------------------- the powder magazine
y.bolum('Barut deposu')
MX0, MX1, MY0, MY1 = 0.44, 0.64, 0.64, 0.96
kutu(y, V(MX0, MY0, Z0), X, MX1 - MX0, MY1 - MY0, 0.07, TUG, 'onarkasagsol')
y.kemerli(V(MX0 + 0.05, MY0 - 0.0005, Z0), V(MX1 - 0.05, MY0 - 0.0005, Z0), 0, 0.07, (TUG, 'granit_koyu', 'mermer', 'demir'), en=0.55, ust=0.008,
          derin=0.012, k_say=8, cerceve=(0.005, 'granit_koyu'))
# a barrel vault under an earth cover with dry grass on it
n = 10
R_ = (MX1 - MX0) / 2 + 0.012
cx = (MX0 + MX1) / 2
pv = lambda a, yy: V(cx + R_ * math.cos(a), yy, Z0 + 0.07 + R_ * 0.75 * math.sin(a))
for k in range(n):
    a0, a1 = math.pi * k / n, math.pi * (k + 1) / n
    y.yuz_yon([pv(a0, MY0 - 0.012), pv(a1, MY0 - 0.012), pv(a1, MY1 + 0.012), pv(a0, MY1 + 0.012)], 'cimen_kuru',
              V(math.cos((a0 + a1) / 2), 0, math.sin((a0 + a1) / 2)))
for yy, sg in ((MY0 - 0.012, -1), (MY1 + 0.012, 1)):
    y.yuz_yon([pv(math.pi * k / n, yy) for k in range(n + 1)], TUG, V(0, sg, 0))
    y.yuz_yon([V(cx - R_, yy, Z0 + 0.07), V(cx + R_, yy, Z0 + 0.07), V(cx + R_, yy, Z0 + 0.06), V(cx - R_, yy, Z0 + 0.06)], TUG, V(0, sg, 0))
y.yuz_yon([V(cx - R_, MY0 - 0.012, Z0 + 0.06), V(cx + R_, MY0 - 0.012, Z0 + 0.06), V(cx + R_, MY1 + 0.012, Z0 + 0.06),
           V(cx - R_, MY1 + 0.012, Z0 + 0.06)], TUG, -Z)
for sx in (-1, 1):
    y.yuz_yon([V(cx + sx * R_, MY0 - 0.012, Z0 + 0.06), V(cx + sx * R_, MY1 + 0.012, Z0 + 0.06), V(cx + sx * R_, MY1 + 0.012, Z0 + 0.07),
               V(cx + sx * R_, MY0 - 0.012, Z0 + 0.07)], TUG, V(sx, 0, 0))
# a sand heap and a red warning lantern by the door
y.koni((MX1 + 0.04, MY0 - 0.05), 0.04, Z0, 0.03, 'kum', n=8)
cubuk(y, V(MX0 - 0.02, MY0 - 0.02, Z0), V(MX0 - 0.02, MY0 - 0.02, Z0 + 0.1), 0.006, 'ahsap_koyu')
kure(y, (MX0 - 0.02, MY0 - 0.02, Z0 + 0.088), 0.014, 'boya_kirmizi', n=8, kat=4)

# ---------------------------------------------------------------- the store shed, the well, carts
y.bolum('Ambar ve kuyu')
kucuk_salon(y, -1.03, -0.86, -0.42, 0.12, Z0, 0.1, 0.075, 0.035, 'kerpic', 'ahsap_koyu', GRI, GRI2, 'besik', 0.35, 0.02, 0.012, TUG,
            kapi_yon=1, bay=0.09, arka_duz=True)
for (x, yy) in ((-0.82, -0.3), (-0.82, -0.26), (-0.82, 0.02)):
    fici(y, x, yy, Z0, 1.0)
WLC = (-0.18, -0.45)
y.yuz_yon([V(WLC[0] + 0.03 * math.cos(TAU * i / 12), WLC[1] + 0.03 * math.sin(TAU * i / 12), Z0 + 0.025) for i in range(12)], 'su', Z)
donel(y, WLC, [(0.045, Z0), (0.045, Z0 + 0.035), (0.04, Z0 + 0.04),
               (0.03, Z0 + 0.04), (0.03, Z0 + 0.025)], 'granit', n=12)
for sx in (-1, 1):
    cubuk(y, V(WLC[0] + sx * 0.05, WLC[1], Z0), V(WLC[0] + sx * 0.05, WLC[1], Z0 + 0.1), 0.007, 'ahsap_koyu')
cubuk(y, V(WLC[0] - 0.055, WLC[1], Z0 + 0.085), V(WLC[0] + 0.055, WLC[1], Z0 + 0.085), 0.008, 'ahsap')
cati_besik(y, WLC[0] - 0.065, WLC[0] + 0.065, WLC[1] - 0.04, WLC[1] + 0.04, Z0 + 0.1, 0.035, 0.012, GRI, GRI2, 0.006, 0.3, 'ahsap_koyu',
           'ahsap_koyu', ns=3, nr=2, uc_sacak=0.01)
for (x, yy) in ((-0.06, -0.4), (-0.06, -0.5)):
    donel(y, (x, yy), [(0.0, Z0), (0.03, Z0), (0.038, Z0 + 0.03), (0.034, Z0 + 0.05), (0.028, Z0 + 0.05), (0.028, Z0 + 0.046), (0.0, Z0 + 0.046)],
          'tugla_koyu', n=10)
for (cx_, cy_, a) in ((-0.25, 0.1, 0.4), (0.25, 0.38, -0.2)):
    with parca(y, (cx_, cy_, Z0), a):
        for sx in (-1, 1):
            boru(y, [V(0, sx * 0.05, 0.035), V(0, sx * 0.064, 0.035)], 0.035, 'ahsap_koyu', n=12)
        kutu(y, V(-0.09, -0.045, 0.04), X, 0.18, 0.09, 0.012, 'ahsap')
        for sy in (-1, 1):
            cubuk(y, V(-0.09, sy * 0.03, 0.046), V(-0.2, sy * 0.025, 0.02), 0.007, 'ahsap')
        fici(y, -0.04, 0, 0.052, 1.0, yatik=math.pi / 2)
        fici(y, 0.03, 0, 0.052, 1.0, yatik=math.pi / 2)
# dry grass along the walls
for (x0, x1, y0_, y1_) in ((-1.04, 1.04, -1.045, -0.99), (-0.84, 0.4, 0.99, 1.045), (0.99, 1.045, -0.99, 0.62)):
    y.yuz_yon(dikdortgen(x0, x1, y0_, y1_, Z0 + 0.0012), 'cimen_kuru', Z)

# ---------------------------------------------------------------- paved working floors
y.bolum('Taş döşeme')
for x0, x1, y0_, y1_ in ((-0.8, -0.42, -0.3, 0.5), (0.4, 0.97, 0.03, 0.34)):
    kutu(y, V(x0, y0_, Z0), X, x1 - x0, y1_ - y0_, 0.003, 'zemin', 'onarkasagsolust')
    silme(y, dikdortgen(x0, x1, y0_, y1_), Z0, 0.005, 0.004, 'granit_koyu', 'duz')
# a fire-water cistern by the mills
# (a raised stone tank: the library pool sinks its water under the kerb, below this yard's floor)
duvarlar(y, dikdortgen(-0.45, -0.27, -0.31, -0.19), Z0, Z0 + 0.03, TUG, 'granit_koyu', kalinlik=0.014)
y.yuz_yon(dikdortgen(-0.436, -0.284, -0.296, -0.204, Z0 + 0.022), 'su', Z)
silme(y, dikdortgen(-0.45, -0.27, -0.31, -0.19), Z0, 0.008, 0.004, 'granit_koyu', 'kaide')
for (x, yy) in ((-0.48, -0.17), (-0.24, -0.33)):
    donel(y, (x, yy), [(0.0, Z0), (0.02, Z0), (0.028, Z0 + 0.02), (0.026, Z0 + 0.04), (0.02, Z0 + 0.044), (0.0, Z0 + 0.042)], 'tugla_koyu', n=10)

# ---------------------------------------------------------------- wall corner turrets
y.bolum('Köşe burçları')
for cx_, cy_ in ((-1.07, 1.07), (-1.07, -1.07), (1.07, -1.07)):
    kutu_merkez(y, (cx_, cy_), 0.13, 0.13, 0.125, TUG, z0=Z0, yuzler='onarkasagsol')
    kd_ = dikdortgen(cx_ - 0.065, cx_ + 0.065, cy_ - 0.065, cy_ + 0.065)
    silme(y, kd_, Z0 + 0.001, 0.016, 0.006, 'granit_koyu', 'kaide')
    silme(y, kd_, Z0 + 0.113, 0.012, 0.006, TUG, 'kaba')
    y.yuz_yon(dikdortgen(cx_ - 0.065, cx_ + 0.065, cy_ - 0.065, cy_ + 0.065, Z0 + 0.125), 'zemin', Z)
    parapet(y, disa(kd_, 0.006), Z0 + 0.125, 0.008, 0.018, 0.01, TUG, ust_key='granit_koyu')
    kosk(y, (cx_, cy_), 0.07, Z0 + 0.125, 0.06, 0.05, 0.03, 'lake', GRI, GRI2, 0.5, 0.025, TUG, n=4, boya='boya_yesil')

# ---------------------------------------------------------------- the trebuchet on the test field
y.bolum('Mancınık')


def mancinik(cx, cy, aci):
    """a Song traction trebuchet (huopao) throwing towards aci: a timber trestle, the axle, the long arm cocked down to
    the ground with its sling and a bomb, a cross-bar on the short end with the crew's pull ropes"""
    PZ = 0.2
    with parca(y, (cx, cy, Z0), aci):
        for s in (-1, 1):
            cubuk(y, V(-0.14, s * 0.065, 0.0), V(0.14, s * 0.065, 0.0), 0.014, 'ahsap_koyu')
            cubuk(y, V(-0.11, s * 0.065, 0.012), V(0.0, s * 0.052, PZ + 0.01), 0.013, 'ahsap')
            cubuk(y, V(0.11, s * 0.065, 0.012), V(0.0, s * 0.052, PZ + 0.01), 0.013, 'ahsap')
            cubuk(y, V(-0.06, s * 0.062, 0.095), V(0.06, s * 0.062, 0.095), 0.009, 'ahsap_koyu')
            cubuk(y, V(0.0, s * 0.06, 0.012), V(0.0, s * 0.054, PZ - 0.01), 0.011, 'ahsap_koyu')
        for x in (-0.13, 0.13):
            cubuk(y, V(x, -0.072, 0.0), V(x, 0.072, 0.0), 0.014, 'ahsap_koyu')
        cubuk(y, V(-0.05, -0.062, 0.095), V(-0.05, 0.062, 0.095), 0.008, 'ahsap_koyu')
        boru(y, [V(0, -0.08, PZ), V(0, 0.08, PZ)], 0.009, 'demir', n=8)
        # the arm: long end down behind, short end up in front
        u = V(0.3, 0, 0.165).normalized()
        piv = V(0, 0, PZ)
        uzun, kisa = piv - u * 0.34, piv + u * 0.12
        cubuk(y, uzun, kisa, 0.018, 'ahsap', 0.02)
        for t in (-0.22, -0.1, 0.05):
            p = piv + u * t
            cubuk(y, p - u * 0.004, p + u * 0.004, 0.024, 'demir', 0.026)
        cubuk(y, kisa + V(0, -0.06, 0), kisa + V(0, 0.06, 0), 0.008, 'ahsap_koyu')
        # the pull ropes down to the crew
        for i in range(7):
            yy = -0.055 + 0.11 * i / 6
            cubuk(y, kisa + V(0, yy, -0.004), V(0.27 + 0.02 * (i % 2), yy * 2.2, 0.03), 0.0025, 'saz')
        for i, yy in enumerate((-0.1, 0.0, 0.1)):
            insan(y, 0.29 + 0.02 * (i % 2), yy, 0.0, math.pi, 'kumas', 'saz', 0.065, 0.6)
        # the sling lying on the ground under the trestle, a bomb in its pouch
        torba = V(-0.08, 0.0, 0.012)
        cubuk(y, uzun, torba + V(-0.012, 0.004, 0), 0.0025, 'saz')
        cubuk(y, uzun, torba + V(-0.012, -0.004, 0), 0.0025, 'saz')
        kutu_merkez(y, (torba.x, torba.y), 0.03, 0.022, 0.004, 'saz', z0=0.002)
        kure(y, (torba.x, torba.y, 0.02), 0.014, 'koyu', n=8, kat=4)


mancinik(0.82, -0.22, -math.pi / 2)


def bomba_yigini(cx, cy, r=0.013, key='koyu'):
    """a pyramid of round bombs (thunder-crash iron shells): 3 x 3, 2 x 2, 1"""
    for k, n in enumerate((3, 2, 1)):
        for i in range(n):
            for j in range(n):
                x = cx + (i - (n - 1) / 2) * r * 2.02
                yy = cy + (j - (n - 1) / 2) * r * 2.02
                kure(y, (x, yy, Z0 + r + k * r * 1.42), r, key, n=8, kat=4)
        # the fuse stubs on the top course
    cubuk(y, V(cx, cy, Z0 + r * 3.8), V(cx + 0.004, cy, Z0 + r * 4.6), 0.003, 'saz')


bomba_yigini(0.67, -0.04)
bomba_yigini(0.7, -0.12, 0.011, 'demir')
# clay pot bombs in a crate
kutu(y, V(0.88, -0.03, Z0), X, 0.07, 0.05, 0.025, 'ahsap_koyu', 'onarkasagsolust')
for i in range(3):
    for j in range(2):
        donel(y, (0.892 + i * 0.023, -0.017 + j * 0.024), [(0.0, Z0 + 0.018), (0.011, Z0 + 0.022), (0.012, Z0 + 0.032), (0.005, Z0 + 0.04),
                                                          (0.0, Z0 + 0.042)], 'tugla', n=8)

# ---------------------------------------------------------------- the rocket fletching shed along the east wall
y.bolum('Ok atölyesi')
RX0, RX1, RY0, RY1 = 0.93, 1.03, -0.53, -0.07
for i in range(5):
    yy = RY0 + (RY1 - RY0) * i / 4
    y.prizma((RX0, yy), 0.008, Z0, Z0 + 0.1, 'ahsap_koyu', n=6)
kutu(y, V(RX1 - 0.006, RY0, Z0), X, 0.006, RY1 - RY0, 0.13, 'kerpic', 'onarkasagsolust')
cati_besik(y, RX0 - 0.01, RX1, RY0 - 0.02, RY1 + 0.02, Z0 + 0.1, 0.045, 0.02, GRI, GRI2, 0.008, 0.3, 'ahsap_koyu', 'kerpic', ns=8, nr=3)
# workbenches with bundles of fire arrows and rocket tubes drying on them
for yy in (-0.44, -0.24):
    kutu_merkez(y, (0.975, yy), 0.05, 0.13, 0.006, 'ahsap', z0=Z0 + 0.04)
    for sy in (-1, 1):
        for sx in (-1, 1):
            cubuk(y, V(0.975 + sx * 0.02, yy + sy * 0.055, Z0), V(0.975 + sx * 0.02, yy + sy * 0.055, Z0 + 0.04), 0.005, 'ahsap_koyu')
    for k in range(5):
        p = V(0.962 + 0.006 * (k % 2), yy - 0.05 + 0.025 * k, Z0 + 0.05)
        cubuk(y, p, p + V(0, 0.0, 0.0) + V(0.03, 0.006, 0.0), 0.0035, 'boya_kirmizi')
    insan(y, 0.91, yy, Z0, 0.0, 'kumas', 'saz', 0.065, 0.5)
# a sheaf of arrows leaning on the wall
for k in range(6):
    cubuk(y, V(1.0, -0.13 + 0.006 * k, Z0), V(1.025, -0.13 + 0.006 * k, Z0 + 0.1), 0.0025, 'ahsap_acik')

# ---------------------------------------------------------------- bronze cannons trained on the targets
y.bolum('Toplar')


def top(cx, cy, aci):
    """an early bronze cannon (huochong) on a wheeled timber bed, its bulbous breech back, the muzzle a little raised"""
    with parca(y, (cx, cy, Z0), aci):
        kutu_merkez(y, (0, 0), 0.11, 0.05, 0.02, 'ahsap_koyu', z0=0.008)
        for sx in (-1, 1):
            for sy in (-1, 1):
                boru(y, [V(sx * 0.035, sy * 0.026, 0.013), V(sx * 0.035, sy * 0.034, 0.013)], 0.013, 'ahsap', n=8)
        e = V(1, 0, 0.12).normalized()
        b0 = V(-0.04, 0, 0.044)
        boru(y, [b0, b0 + e * 0.13], 0.016, 'bronz', n=10, r_son=0.011)
        kure(y, (b0.x, b0.y, b0.z), 0.02, 'bronz', n=10, kat=5)
        for t in (0.035, 0.085, 0.124):
            p = b0 + e * t
            boru(y, [p - e * 0.004, p + e * 0.004], 0.0185 - t * 0.045, 'bronz', n=10)
        cubuk(y, V(-0.06, 0, 0.05), V(-0.075, 0, 0.065), 0.003, 'saz')


top(0.47, -0.8, -0.15)
top(0.5, -0.93, 0.0)
bomba_yigini(0.39, -0.97, 0.011, 'demir')
insan(y, 0.4, -0.78, Z0, -0.2, 'kumas', 'saz', 0.065)
# a rail fence closing the test field from the yard
for xa, xb in ((0.72, 1.035),):
    n_ = 8
    for k in range(n_ + 1):
        x = xa + (xb - xa) * k / n_
        cubuk(y, V(x, -0.57, Z0), V(x, -0.57, Z0 + 0.05), 0.007, 'ahsap_koyu')
    for zz in (0.022, 0.042):
        cubuk(y, V(xa, -0.57, Z0 + zz), V(xb, -0.57, Z0 + zz), 0.005, 'ahsap')


# ---------------------------------------------------------------- the cross path and red signal pennants
y.bolum('Yollar ve flamalar')
for x0, x1 in ((-0.42, -0.07), (0.07, 0.42)):
    kutu(y, V(x0, -0.045, Z0), X, x1 - x0, 0.09, 0.003, 'zemin', 'onarkasagsolust')
for x0, x1 in ((-0.42, -0.07), (0.07, 0.42)):
    for yy in (-0.045, 0.045):
        cubuk(y, V(x0, yy, Z0 + 0.002), V(x1, yy, Z0 + 0.002), 0.008, 'granit_koyu', 0.004)


def flama(x, yy, z, boy=0.16, yon=0.0, key='boya_kirmizi'):
    """a pole with a red swallow-tailed signal pennant (two-sided)"""
    cubuk(y, V(x, yy, z), V(x, yy, z + boy), 0.005, 'ahsap_koyu')
    d = V(math.cos(yon), math.sin(yon), 0)
    t = z + boy - 0.005
    pts = [V(x, yy, t), V(x, yy, t - 0.045)] + [V(x, yy, 0) + d * 0.07 + V(0, 0, t - 0.04), V(x, yy, 0) + d * 0.05 + V(0, 0, t - 0.022),
                                                 V(x, yy, 0) + d * 0.075 + V(0, 0, t - 0.002)]
    nn = V(-d.y, d.x, 0)
    iki_yuzlu(y, pts, key, nn)
    kure(y, (x, yy, z + boy + 0.004), 0.006, 'altin', n=6, kat=3)


for (x, yy, a) in ((0.72, -0.57, 0.3), (1.03, -0.57, 2.6), (-0.21, -1.0, 2.8), (0.21, -1.0, 0.3), (-0.45, 0.6, 2.5), (0.42, 0.6, 0.4)):
    flama(x, yy, Z0, 0.17, a)
sayim(y)
calistir(y, 'lm_barutatolye')
