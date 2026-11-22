# Hwacha Atölyesi (lm_hwachaatolye): a Joseon military workshop for hwacha rocket carts. The tiled workshop hall with
# its open bays, the arrow-fletching shed, the gunpowder shed (stone mortars, a saltpetre cauldron, barrels, sacks), the
# stone powder magazine, carts being built in the yard; a tall timber watchtower; on the proving ground in front two
# hwacha fire volleys of singijeon whose smoke trails arc over to the targets.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ek import *
from bina_ortak import calistir
import random

y = Yapi()
rs = random.Random(11)
GX0, GX1, GY0, GY1 = -1.15, 1.15, -1.15, 1.12
WY = -0.42                     # the compound's front wall (the proving ground in front of it)

# ---------------------------------------------------------------- ground
y.bolum('Zemin')


def ust_fn(x, yy):
    return 'cimen' if yy < WY else 'toprak'


Z0 = zemin_delikli(y, GX0, GX1, GY0, GY1, 0.04, [], 'tas_koyu', 'toprak', None)
# (the slab top split: grass on the proving ground, packed earth in the yard)
y.faces.pop()
y.yuz_yon([V(GX0, GY0, Z0), V(GX1, GY0, Z0), V(GX1, WY, Z0), V(GX0, WY, Z0)], 'cimen', Z)
y.yuz_yon([V(GX0, WY, Z0), V(GX1, WY, Z0), V(GX1, GY1, Z0), V(GX0, GY1, Z0)], 'toprak', Z)

# ---------------------------------------------------------------- the compound wall and its gate
y.bolum('Avlu duvarı ve kapı')
KAPI_X = 0.05
kore_sur(y, [(KAPI_X + 0.11, WY), (1.1, WY), (1.1, 1.08), (-1.1, 1.08), (-1.1, WY), (KAPI_X - 0.11, WY)], Z0, 0.075, t=0.03, key='tas', ust=DUVAR)
kore_salon(y, KAPI_X, WY - 0.015, 0.22, 0.075, Z0, 0.1, 0.07, sacak=0.04, tur='matbae', nx=1, ny=1, on=['karanlik'], yan='duvar',
           arka=['karanlik'], gidan=(0.012, TAS, 1), chwidu=0.0, levha=False, r=0.008, mahya_en=0.01)
hyeonpan(y, (KAPI_X, WY - 0.015 - 0.0375), Z0 + 0.012 + 0.1 * 0.9, 0.06)

# ---------------------------------------------------------------- the workshop hall
y.bolum('Atölye')
HC = (0.05, 0.62)
HW, HD = 0.92, 0.38
kore_salon(y, HC[0], HC[1], HW, HD, Z0, 0.15, 0.16, sacak=0.075, tur='paljak', kivrim=0.34, yukari=0.04, nx=7, ny=3,
           on=['pencere', 'karanlik', 'karanlik', 'tahta', 'karanlik', 'karanlik', 'pencere'], yan='pencere', arka='duvar',
           gidan=(0.02, TAS, 3), japsang=3, chwidu=1.0, r=0.0095, mahya_en=0.014)
hyeonpan(y, (HC[0], HC[1] - HD / 2), Z0 + 0.02 + 0.15 * 0.92, 0.09)
# a cart half out of the middle door, timber and wheels against the front
for k in range(3):
    teker(y, V(HC[0] - 0.36 + k * 0.018, HC[1] - HD / 2 - 0.045, Z0 + 0.032), V(0.2, 1, -0.7), 0.028, 0.006)
for k in range(2):
    teker(y, V(HC[0] + 0.38 - k * 0.02, HC[1] - HD / 2 - 0.045, Z0 + 0.032), V(-0.2, 1, -0.7), 0.028, 0.006)

# ---------------------------------------------------------------- carts being built in the yard
y.bolum('Avludaki arabalar')
hwacha(y, -0.28, 0.17, Z0, -math.pi / 2 + 0.25, 0.5, 1.15, tohum=1)
hwacha(y, 0.36, 0.2, Z0, -math.pi / 2 - 0.2, 0.45, 1.15, tohum=2)
hwacha(y, 0.06, 0.05, Z0, -math.pi / 2, 0.5, 1.15, rafli=False, tohum=3)
# a launcher box on trestles being drilled
for sx in (-1, 1):
    kutu_merkez(y, (0.06 + sx * 0.035, 0.27), 0.01, 0.06, 0.03, 'ahsap_koyu', z0=Z0)
kutu_merkez(y, (0.06, 0.27), 0.08, 0.07, 0.05, 'ahsap', z0=Z0 + 0.03)
for i in range(6):
    for j in range(6):
        q = V(0.06 - 0.03 + 0.06 * (i + 0.5) / 6, 0.27 - 0.03 + 0.06 * (j + 0.5) / 6, Z0 + 0.0806)
        y.yuz_yon([q + V(-0.0025, -0.0025), q + V(0.0025, -0.0025), q + V(0.0025, 0.0025), q + V(-0.0025, 0.0025)], 'koyu', Z)
for k, (x, yy, a) in enumerate(((-0.12, 0.3, 0.3), (0.2, 0.33, 2.5), (-0.4, 0.05, 1.2), (0.5, 0.05, 2.0), (0.14, 0.12, 4.0))):
    insan(y, x, yy, Z0, a, 'kece', 'saz', 0.055, egik=0.6 if k % 2 else 0.0)
ok_demeti(y, -0.45, 0.32, Z0, 0.2, 4, 0.1)
ok_demeti(y, 0.55, 0.32, Z0, -0.3, 3, 0.1)

# ---------------------------------------------------------------- the fletching shed (west)
y.bolum('Ok sundurması')
SX0, SX1, SY0, SY1 = -1.02, -0.62, 0.28, 0.95
sundurma(y, SX0, SX1, SY0, SY1, Z0, 0.12, 0.09, 'matbae', arka_duvar=False)
for k in range(3):   # work tables with arrow bundles
    yy = SY0 + 0.12 + k * 0.2
    kutu_merkez(y, (-0.82, yy), 0.2, 0.06, 0.028, 'ahsap', z0=Z0)
    ok_demeti(y, -0.82, yy, Z0 + 0.012, 0.0, 3, 0.15)
    insan(y, -0.82, yy - 0.06, Z0, math.pi / 2, 'kece', 'saz', 0.05, egik=0.5)
for k in range(4):   # bundles of bamboo shafts leaning on the wall
    x = -1.06
    yy = 0.35 + k * 0.15
    for m in range(5):
        cubuk(y, V(x + 0.01 + m * 0.004, yy - 0.02 + m * 0.009, Z0), V(x - 0.006, yy - 0.02 + m * 0.009, Z0 + 0.1), 0.004, 'boya_yesil' if m % 2 else 'saz')

# ---------------------------------------------------------------- the gunpowder shed and the magazine (east)
y.bolum('Barut sundurması ve cephanelik')
BX0, BX1, BY0, BY1 = 0.6, 1.02, -0.32, 0.16
sundurma(y, BX0, BX1, BY0, BY1, Z0, 0.11, 0.1, 'ujingak', arka_duvar=True)
for k, (x, yy) in enumerate(((0.68, -0.22), (0.78, -0.2), (0.88, -0.24), (0.7, -0.05))):
    havan(y, x, yy, Z0, 1.2)
    insan(y, x - 0.03, yy - 0.03, Z0, 0.6, 'kece', 'saz', 0.05, egik=0.7)
# the saltpetre cauldron on its stove
kutu_merkez(y, (0.92, 0.02), 0.08, 0.08, 0.03, 'tugla', z0=Z0)
kazan(y, 0.92, 0.02, Z0 + 0.024, 1.6, 'demir')
for k in range(3):   # (steam over the cauldron, kept under the shed's roof)
    kure(y, (0.92 + rs.uniform(-0.008, 0.008), 0.02 + k * 0.006, Z0 + 0.078 + k * 0.016), 0.011 + k * 0.004, 'buhar', n=8, kat=4)
for k in range(5):
    fici(y, 0.66 + (k % 3) * 0.042, 0.06 + (k // 3) * 0.045, Z0, 0.9)
for k in range(4):
    cuval(y, 0.83 + k * 0.03, 0.1, Z0, 1.1)
# the magazine: thick stone walls, an iron door, a hipped roof
MX0, MX1, MY0, MY1 = 0.62, 1.0, 0.46, 0.92
mk = dikdortgen(MX0, MX1, MY0, MY1)
for i in range(4):
    a_, b_ = mk[i], mk[(i + 1) % 4]
    if i == 3:
        n = 3
        for j in range(n):
            p, q = a_.lerp(b_, j / n), a_.lerp(b_, (j + 1) / n)
            if j == 1:
                dikdortgen_acik(y, p, q, Z0, 0.12, 0.2, 0.8, 0.0, 0.085, ('tas', 'tas_koyu', 'tas_acik', 'demir'), derin=0.014, cerceve=(0.006, TAS2), ic_kenar=True)
            else:
                duz_duvar(y, p, q, Z0, Z0 + 0.12, 'tas')
                yarik(y, V(p.x, p.y, Z0), (q - p), V((q - p).y, -(q - p).x), 0.06, 0.05, 0.012, 0.035, 'koyu')
    else:
        duz_duvar(y, a_, b_, Z0, Z0 + 0.12, 'tas')
silme(y, mk, Z0, 0.014, 0.006, 'tas_koyu', 'kaide')
silme(y, mk, Z0 + 0.11, 0.01, 0.006, TAS2, 'duz')
kore_cati(y, MX0, MX1, MY0, MY1, Z0 + 0.12, 0.12, 0.05, 'ujingak', 0.32, 0.03, 0, 0.0, 0.012, yongmaru=False, mahya=CATI2)

# ---------------------------------------------------------------- the watchtower
y.bolum('Gözcü kulesi')
TC = (-0.7, -0.08)
TW = 0.17
kutu_merkez(y, TC, TW + 0.06, TW + 0.06, 0.07, TAS, z0=Z0)
silme(y, dikdortgen(TC[0] - TW / 2 - 0.03, TC[0] + TW / 2 + 0.03, TC[1] - TW / 2 - 0.03, TC[1] + TW / 2 + 0.03), Z0 + 0.064, 0.006, 0.005, TAS2)
ZB = Z0 + 0.07
TH = 0.5
for sx in (-1, 1):
    for sy in (-1, 1):
        p0 = V(TC[0] + sx * (TW / 2 + 0.012), TC[1] + sy * (TW / 2 + 0.012), ZB)
        p1 = V(TC[0] + sx * (TW / 2 - 0.01), TC[1] + sy * (TW / 2 - 0.01), ZB + TH)
        cubuk(y, p0, p1, 0.016, 'lake')
        kutu_merkez(y, (p0.x, p0.y), 0.026, 0.026, 0.008, TAS2, z0=ZB, yuzler='onarkasagsolust')
# cross braces on every side, in two stages, and the tie rings
TK = dikdortgen(TC[0] - TW / 2, TC[0] + TW / 2, TC[1] - TW / 2, TC[1] + TW / 2)
for st in range(3):
    za, zb_ = ZB + TH * st / 3, ZB + TH * (st + 1) / 3
    for i in range(4):
        a_, b_ = TK[i], TK[(i + 1) % 4]
        nn = V((b_ - a_).y, -(b_ - a_).x).normalized()
        sh = lambda p, zz: V(p.x, p.y, zz) + nn * 0.004 + (V(p.x, p.y) - V(TC[0], TC[1])).normalized() * (0.012 * (1 - (zz - ZB) / TH * 1.0) - 0.0)
        cubuk(y, sh(a_, za + 0.01), sh(b_, zb_ - 0.01), 0.006, 'ahsap')
        cubuk(y, sh(b_, za + 0.01), sh(a_, zb_ - 0.01), 0.006, 'ahsap')
        cubuk(y, sh(a_, zb_), sh(b_, zb_), 0.008, 'lake_koyu')
# a ladder up the front
for s in (-1, 1):
    cubuk(y, V(TC[0] + s * 0.018, TC[1] - TW / 2 - 0.09, ZB), V(TC[0] + s * 0.018, TC[1] - TW / 2 - 0.008, ZB + TH), 0.005, 'ahsap_koyu')
for k in range(12):
    t = (k + 0.5) / 12
    p = V(TC[0], TC[1] - TW / 2 - 0.09 + 0.082 * t, ZB + TH * t)
    cubuk(y, p - X * 0.018, p + X * 0.018, 0.003, 'ahsap')
# the lookout: a floor with a railing, an open pavilion with a hip-and-gable roof, a drum, the banner
ZL = ZB + TH
kutu(y, V(TC[0] - TW / 2 - 0.03, TC[1] - TW / 2 - 0.03, ZL), X, TW + 0.06, TW + 0.06, 0.012, 'lake_koyu')
kutu(y, V(TC[0] - TW / 2 - 0.028, TC[1] - TW / 2 - 0.028, ZL + 0.012), X, TW + 0.056, TW + 0.056, 0.003, 'ahsap_acik', 'ust')
y.yuz_yon(dikdortgen(TC[0] - TW / 2 - 0.03, TC[0] + TW / 2 + 0.03, TC[1] - TW / 2 - 0.03, TC[1] + TW / 2 + 0.03, ZL), 'lake_koyu', -Z)
kore_korkuluk(y, dikdortgen(TC[0] - TW / 2 - 0.022, TC[0] + TW / 2 + 0.022, TC[1] - TW / 2 - 0.022, TC[1] + TW / 2 + 0.022), ZL + 0.015, 0.024, adim=0.05)
tt = kore_salon(y, TC[0], TC[1], TW, TW, ZL + 0.015, 0.075, 0.11, sacak=0.06, tur='ujingak', kivrim=0.36, yukari=0.045, nx=2, ny=2,
                on='acik', yan='acik', arka='acik', japsang=3, chwidu=0.8, r=0.007, levha=False, mahya_en=0.012, ic_direk=False)
donel(y, (TC[0] + 0.03, TC[1] + 0.02), [(0.0, ZL + 0.04), (0.018, ZL + 0.042), (0.021, ZL + 0.055), (0.018, ZL + 0.068), (0.0, ZL + 0.07)], 'boya_kirmizi', n=10)
sancak(y, TC[0] - TW / 2 - 0.02, TC[1] - TW / 2 - 0.02, ZL + 0.015, boy=0.26, en=0.13, yuk=0.08, aci=-0.5)
insan(y, TC[0] - 0.03, TC[1] - 0.04, ZL + 0.023, -1.2, 'boya_kirmizi', 'koyu', 0.05)

# ---------------------------------------------------------------- the proving ground
y.bolum('Deneme alanı')
FY = -0.8
# the firing line: a gravel pad, two hwacha firing towards the targets in the east, gunners
for (x0_, x1_, y0_, y1_) in ((-1.02, -0.68, -1.05, -0.55),):
    y.yuz_yon([V(x0_, y0_, Z0 + 0.0012), V(x1_, y0_, Z0 + 0.0012), V(x1_, y1_, Z0 + 0.0012), V(x0_, y1_, Z0 + 0.0012)], 'toprak', Z)
ucus = []
for k, yy in enumerate((-0.68, -0.92)):
    r_ = hwacha(y, -0.88, yy, Z0 + 0.0012, 0.0, 0.62, 1.25, oklu=(k == 1), ates=(k == 0), tohum=10 + k)
    ucus.append(r_)
    insan(y, -0.99, yy + 0.07, Z0 + 0.0012, 0.2, 'kece', 'saz', 0.055)
    insan(y, -0.98, yy - 0.06, Z0 + 0.0012, 0.4, 'boya_kirmizi', 'koyu', 0.055)
# the volley in the air from the first cart: trails fanning out and arcing down to the target field (clear of the gate)
mouth, f = ucus[0]
for k in range(6):
    end = V(0.3 + k * 0.1 + rs.uniform(-0.03, 0.03), FY + rs.uniform(-0.16, 0.08), Z0 + 0.06 + rs.uniform(0.0, 0.2) * (k < 4))
    ok_izi(y, mouth + V(0, rs.uniform(-0.01, 0.01), 0), end, 0.22 + rs.uniform(-0.05, 0.06) + 0.05 * (k < 3), n=12, r0=0.0042, r1=0.0014)
# the targets and the scorched ground
for k, (x, yy) in enumerate(((0.75, -0.62), (0.9, -0.82), (0.72, -1.0), (1.02, -0.6), (1.0, -1.02))):
    hedef(y, x, yy, Z0, math.pi * 0.0, 0.04, 0.07)
    for m in range(3):
        a = rs.uniform(0, TAU)
        p = V(x - 0.04 + rs.uniform(-0.04, 0.02), yy + rs.uniform(-0.05, 0.05), Z0)
        cubuk(y, p, p + V(-0.025, rs.uniform(-0.006, 0.006), 0.022), 0.002, 'ahsap_acik')
    y.yuz_yon([V(p.x, p.y, Z0 + 0.0014) for p in cokgen((x - 0.07, yy), 0.05, 9, k)], 'koyu', Z)
# the officers' viewing pavilion with a war drum and a command banner
kore_salon(y, -0.2, -0.98, 0.16, 0.12, Z0, 0.075, 0.08, sacak=0.045, tur='paljak', kivrim=0.36, yukari=0.04, nx=2, ny=1, on='acik', yan='acik',
           arka='acik', gidan=(0.016, TAS, 1), japsang=0, chwidu=0.7, r=0.007, levha=False, mahya_en=0.01, ic_direk=False)
insan(y, -0.2, -0.97, Z0 + 0.024, -0.3, 'boya_kirmizi', 'koyu', 0.055)
for k in range(2):
    cubuk(y, V(-0.06, -0.9 - k * 0.03, Z0), V(-0.06, -0.9 - k * 0.03, Z0 + 0.03), 0.006, 'ahsap_koyu')
boru(y, [V(-0.06, -0.93, Z0 + 0.045), V(-0.06, -0.87, Z0 + 0.045)], 0.024, 'boya_kirmizi', n=10)
sancak(y, -0.3, -0.92, Z0, boy=0.22, en=0.1, yuk=0.06, aci=0.3)
# straw dummies (soldiers' effigies) as further targets
for k, (x, yy) in enumerate(((0.45, -0.95), (0.55, -0.7), (0.4, -0.58))):
    cubuk(y, V(x, yy, Z0), V(x, yy, Z0 + 0.08), 0.008, 'ahsap_koyu')
    donel(y, (x, yy), [(0.0, Z0 + 0.03), (0.016, Z0 + 0.034), (0.018, Z0 + 0.06), (0.012, Z0 + 0.075), (0.0, Z0 + 0.078)], 'saz', n=8)
    kure(y, (x, yy, Z0 + 0.088), 0.01, 'saz', n=8, kat=4)
    cubuk(y, V(x, yy - 0.03, Z0 + 0.065), V(x, yy + 0.03, Z0 + 0.065), 0.006, 'saz')
# a low earth berm behind the targets
for k in range(6):
    x = 1.09
    yy = -1.08 + k * 0.11
    donel(y, (x, yy), [(0.0, Z0), (0.07, Z0), (0.05, Z0 + 0.04), (0.0, Z0 + 0.05)], 'toprak_ot', n=8)

# ---------------------------------------------------------------- trees
y.bolum('Ağaçlar')
for k, (tx, ty) in enumerate(((-1.06, -0.35), (-0.4, 1.0), (0.4, 1.0), (-0.5, -0.3), (0.5, 0.99), (0.05, -1.07), (0.25, -1.08))):
    sonamu(y, tx, ty, Z0, 0.15 + 0.03 * (k % 3), tohum=k + 4)

sayim(y)
calistir(y, 'lm_hwachaatolye')
