# Timbuktu caravan fort (lm_timbuktukale): a desert fort of thick battered mud walls with pilasters and pinnacles, round
# corner bastions and a great gatehouse whose vaulted passage runs under a tall three-storey gate tower; inside, rows of
# storerooms along the walls, a well with a trough, a Tuareg tent, a salt caravan unloading - camels kneeling among
# stacks of Taghaza salt slabs and bales - and Tuareg guards in indigo on the gate and the bastions.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mali_ek import *
from arap_ortak import deve, denk
from kartaca_ek import duman

y = Yapi()
rn = random.Random(7)
Z0 = 0.035
WX0, WX1, WY0, WY1, WH, WK = -0.9, 0.9, -0.82, 0.95, 0.26, 0.06     # the enclosure
GW, GY0, GY1, GH = 0.42, -1.0, -0.62, 0.32                          # the gatehouse block

y.bolum('Zemin')
zemin(y, -1.13, 1.13, -1.17, 1.13, Z0, KK, 'kum_acik', basamak=(), silmeli=True)

# ---------------- the walls and bastions ----------------
y.bolum('Sur')
on_sur = {4: dict(tip='gecit', en=1.0, v0=0.0015, v1=0.245, kemer=0.3, ic=True)}
yan_sur = [dict(n=9, acik=on_sur, kose=False),
           dict(n=10, acik={b: dict(tip='nis', en=0.3, v0=0.17, v1=0.205, derin=0.014) for b in (2, 5, 8)}, kose=False),
           dict(n=10, kose=False),
           dict(n=10, acik={b: dict(tip='nis', en=0.3, v0=0.17, v1=0.205, derin=0.014) for b in (1, 4, 7)}, kose=False)]
sahel_kutu(y, dikdortgen(WX0, WX1, WY0, WY1), Z0, WH, K, kalin=WK, dam=None, yanlar=yan_sur, payanda_ara=0.18,
           payanda_w=0.04, payanda_d=0.026, payanda_tepe=0.06, kose_w=0.07, toron_sira=(0.36, 0.7), kademe=True, etek=0.03,
           ic_payanda=True)
for i, (bx, by) in enumerate(((WX0, WY0), (WX1, WY0), (WX1, WY1), (WX0, WY1))):
    zt = burc(y, (bx, by), 0.165, Z0, 0.36, K, egim=0.14, n=16, dis_aci=math.atan2(by, bx), tepe_n=9)
    if i in (0, 1, 3):
        tuareg(y, bx + 0.03, by + 0.02, zt - 0.03, math.atan2(-by, -bx) + math.pi)

# ---------------- the gatehouse and the gate tower ----------------
y.bolum('Kapi kulesi')
GX0, GX1 = -GW / 2, GW / 2
D = GY1 - GY0
gk = 0.04
yan_kapi = [dict(n=3, acik={1: dict(tip='gecit', en=0.62, v0=0.0015, v1=0.22, kemer=0.32, ic=False)}, payanda=False),
            dict(n=3, acik={1: dict(tip='pencere', en=0.34, v0=0.2, v1=0.26, kafes=True)}),
            dict(n=3, acik={1: dict(tip='gecit', en=0.62, v0=0.0015, v1=0.22, kemer=0.32, ic=False)}, payanda=False),
            dict(n=3, acik={1: dict(tip='pencere', en=0.34, v0=0.2, v1=0.26, kafes=True)})]
sahel_kutu(y, dikdortgen(GX0, GX1, GY0, GY1), Z0, GH, K, kalin=gk, dam=Z0 + GH - 0.03, yanlar=yan_kapi, kose_w=0.08,
           kose_tepe=0.09, kose_yumurta=True, toron_sira=(0.55, 0.82))
# the vaulted passage lining from the front reveal to the back one
bw = GW / 3
u0, u1 = bw * (1.5 - 0.31), bw * (1.5 + 0.31)
ust = kemer_yolu(u0, u1, Z0 + 0.22 - (u1 - u0) * 0.32, 0.32, 8)
delik_yan(y, V(GX0, GY0 + gk), X, -Y, u0, u1, Z0 + 0.0015, ust, D - 2 * gk, KK, alt_key='toprak')
# the great pilasters flanking the gate, the overhang over it with toron ends
for s in (-1, 1):
    payanda(y, V(s * (u1 - u0) / 2 + s * 0.035, GY0), X, -Y, Z0, Z0 + GH + 0.08, 0.042, 0.034, K, 0.08, arka_z=Z0 + GH)
kutu_merkez(y, (0, GY0 - 0.013), 0.16, 0.026, 0.03, K, z0=Z0 + 0.25, yuzler='onsagsolust')
y.yuz_yon([V(-0.08, GY0, Z0 + 0.25), V(0.08, GY0, Z0 + 0.25), V(0.08, GY0 - 0.026, Z0 + 0.25), V(-0.08, GY0 - 0.026, Z0 + 0.25)], KK, -Z)
for k in range(6):
    toron(y, V(-0.065 + 0.026 * k, GY0 - 0.026, Z0 + 0.266), -Y, 0.016, 0.005)
# the gate leaves standing open against the passage walls (studded)
for s in (-1, 1):
    xx = (u1 - u0) / 2 * s
    xs = xx - s * 0.006
    p0, p1 = V(xs, GY0 + gk + 0.03), V(xs, GY0 + gk + 0.03 + (u1 - u0) / 2 * 0.95)
    kutu(y, V(p0.x - (0.006 if s > 0 else 0), p0.y, Z0), Y, (p1 - p0).length, 0.006, 0.175, 'ahsap_koyu')
    for zz in (0.04, 0.09, 0.14):
        for t in (0.25, 0.5, 0.75):
            kure(y, (xs - s * 0.0035, p0.y + (p1.y - p0.y) * t, Z0 + zz), 0.0025, 'demir', n=5, kat=3)
# the tower storeys over the gatehouse
zt = Z0 + GH - 0.03
for k, (w, h) in enumerate(((0.36, 0.27), (0.29, 0.25), (0.21, 0.2))):
    son = k == 2
    def pen(perde=False):
        return dict(tip='pencere', en=0.42, v0=h * 0.36, v1=h * 0.7, kafes=True, kemer=0.35)
    yan = [dict(n=3, acik={0: pen(), 2: pen()} if not son else {1: pen()}), dict(n=3, acik={1: pen()}), dict(n=3, acik={1: pen()}),
           dict(n=3, acik={1: pen()})]
    kose = dikdortgen(-w / 2, w / 2, (GY0 + GY1) / 2 - w / 2, (GY0 + GY1) / 2 + w / 2)
    sahel_kutu(y, kose, zt, h, K, kalin=0.024, dam=zt + h - 0.026, yanlar=yan, payanda_ara=w / 3, kose_w=0.065 - 0.01 * k,
               kose_tepe=0.08 if not son else 0.12, kose_yumurta=True, toron_sira=(0.25, 0.86), kose_ust=0.03 if not son else 0.07,
               payanda_tepe=0.05 if not son else 0.08)
    zt += h - 0.026
# the top: a small lookout lantern, the banner and a guard
cy_ = (GY0 + GY1) / 2
kutu_merkez(y, (0, cy_ + 0.03), 0.08, 0.08, 0.055, K, z0=zt)
y.yuz_yon(dikdortgen(-0.04, 0.04, cy_ - 0.01, cy_ + 0.07, zt + 0.055), K, Z)
tepecik(y, (0, cy_ + 0.03), 0.032, zt + 0.055, 0.08, K, n=10, yumurta=True)
sancak(y, -0.07, cy_ - 0.07, zt, boy=0.25, en=0.13, yuk=0.08, aci=math.radians(200))
tuareg(y, 0.06, cy_ - 0.06, zt, -math.pi / 2)
for s in (-1, 1):
    tuareg(y, s * 0.15, GY0 - 0.06, Z0, -math.pi / 2 + s * 0.3)

# ---------------- storerooms ----------------
y.bolum('Depolar')
IX0, IX1, IY1 = WX0 + WK, WX1 - WK, WY1 - WK
SH = 0.2
on_d = {b: dict(tip='kapi', en=0.46, v0=0, v1=0.13, kemer=0.3) for b in (0, 2, 4, 6, 8)} | \
       {b: dict(tip='pencere', en=0.34, v0=0.08, v1=0.13, kafes=True) for b in (1, 3, 5, 7)}
sahel_kutu(y, dikdortgen(IX0 + 0.005, 0.52, 0.62, IY1 - 0.003), Z0, SH, K, kalin=0.026, dam=Z0 + SH - 0.028,
           yanlar=[dict(n=9, acik=on_d), dict(n=2, acik={0: dict(tip='kapi', en=0.46, v0=0, v1=0.13, kemer=0.3)}),
                   dict(n=9, payanda=False, toron=False), dict(n=2, payanda=False, toron=False)],
           kose_w=0.05, kose_tepe=0.06, toron_sira=(0.72,))
yan_d = {b: dict(tip='kapi', en=0.46, v0=0, v1=0.13, kemer=0.3) for b in (0, 2, 4)} | \
        {b: dict(tip='pencere', en=0.34, v0=0.08, v1=0.13, kafes=True) for b in (1, 3, 5)}
sahel_kutu(y, dikdortgen(0.6, IX1 - 0.003, -0.46, IY1 - 0.003), Z0, SH, K, kalin=0.026, dam=Z0 + SH - 0.028,
           yanlar=[dict(n=2, acik={0: dict(tip='pencere', en=0.34, v0=0.08, v1=0.13, kafes=True)}), dict(n=8, payanda=False, toron=False),
                   dict(n=2, payanda=False, toron=False), dict(n=8, acik={0: yan_d[0], 1: yan_d[1], 2: yan_d[2], 3: yan_d[3], 4: yan_d[4], 5: yan_d[5]})],
           kose_w=0.05, kose_tepe=0.06, toron_sira=(0.72,))
for xx in (-0.7, -0.4, -0.1, 0.2):
    fener(y, xx, 0.76, Z0 + SH - 0.028, w=0.034)
for yy in (-0.3, 0.05, 0.4):
    fener(y, 0.72, yy, Z0 + SH - 0.028, w=0.034)
# a lean-to in front of the north storerooms (facing the gate, in the game's view): the caravan's shade over bales
# and stacked salt (along the west wall it stood in the wall's shadow, unseen)
ZEMIN_Z[0] = Z0
sundurma(y, V(-0.32, 0.62), V(0.3, 0.62), Z0 + 0.18, Z0 + 0.135, 0.15, n_direk=4)
for k, bx in enumerate((-0.25, 0.04, 0.2)):
    denk(y, bx, 0.56, Z0, ('kumas', 'boya_kirmizi', 'kece')[k], aci=0.0)

# ---------------- the court: well, tent, caravan ----------------
y.bolum('Avlu')
kuyu(y, 0.05, 0.25, Z0, 0.045)
yalak(y, V(-0.12, 0.33), V(-0.12, 0.13), Z0, en=0.035, h=0.022, ic='su')
cadir(y, (-0.45, 0.35), 0.11, 0.13, key='kerpic_koyu', serit_key='boya_kirmizi', n=14)
akasya(y, 0.38, 0.38, Z0, boy=0.26, tohum=4)
# the salt caravan: camels kneeling and standing, slabs of salt stacked, bales
for k, (dx, dy, a, cok) in enumerate(((-0.4, -0.3, 0.4, True), (-0.2, -0.45, 1.2, False), (0.15, -0.3, 2.6, True), (0.35, -0.15, 2.2, False),
                                      (-0.05, -0.1, -0.3, True), (-0.45, -0.56, 0.9, True), (0.45, 0.25, 3.6, False),
                                      (0.36, -0.5, 1.6, False))):
    deve(y, dx, dy, Z0, a, renk=('ahsap_acik', 'kum_koyu', 'ahsap_acik', 'kum', 'ahsap_acik', 'kum_koyu', 'kum', 'ahsap_acik', 'kum_koyu')[k], yuk=not cok, cok=cok, olcek=1.05)
for k, (tx, ty, a) in enumerate(((-0.5, -0.14, 0.2), (0.3, -0.48, 0.5), (0.45, -0.42, 0.1), (0.2, 0.0, 1.0),
                                  (-0.3, 0.05, 0.6), (0.05, -0.55, 0.2), (-0.1, 0.5, 0.0), (0.55, -0.3, 1.2))):
    tuz_levha(y, tx, ty, Z0, a, n=3 + k % 3, tohum=k)
for k, (bx, by) in enumerate(((-0.2, 0.08), (0.5, 0.1), (0.48, -0.02))):
    denk(y, bx, by, Z0, ('kumas', 'boya_kirmizi', 'kece')[k], aci=0.4 * k)
# the caravaneers' cooking fire by the tent: a ring of stones, logs, a pot on three stones, smoke rising
FX, FY = -0.5, 0.08
for k in range(8):
    a = TAU * k / 8
    kure(y, (FX + 0.03 * math.cos(a), FY + 0.03 * math.sin(a), Z0 + 0.003), 0.008, 'kaya', n=6, kat=3)
for k in range(3):
    a = TAU * k / 3 + 0.3
    cubuk(y, V(FX + 0.022 * math.cos(a), FY + 0.022 * math.sin(a), Z0 + 0.004), V(FX - 0.01 * math.cos(a), FY - 0.01 * math.sin(a), Z0 + 0.008), 0.006, 'kutuk')
donel(y, (FX, FY), [(0.0, Z0 + 0.004), (0.012, Z0 + 0.005), (0.0, Z0 + 0.016)], 'boya_kirmizi', n=7)
# (no smoke column: at this size it read as a white figure standing in the fire)
oturan(y, FX - 0.065, FY + 0.03, Z0, -0.4, govde='lacivert', bas='lacivert')
oturan(y, FX + 0.05, FY - 0.05, Z0, 2.4, govde='beyaz', bas='lacivert')
# caravaneers and merchants
kisi(y, -0.3, -0.2, Z0, -0.6, govde='lacivert', bas='lacivert', kol=0.7)
kisi(y, 0.08, -0.4, Z0, 2.0, govde='beyaz', bas='beyaz')
kisi(y, 0.25, -0.12, Z0, 3.0, govde='boya_sari', bas='beyaz', yuk='saz')
oturan(y, -0.5, 0.2, Z0, -0.8, govde='lacivert', bas='lacivert')
oturan(y, -0.38, 0.2, Z0, -2.2, govde='beyaz', bas='beyaz')
kisi(y, 0.12, 0.22, Z0, 2.6, govde='boya_kirmizi', bas='beyaz', yuk='kiremit')
tuareg(y, -0.1, -0.6, Z0, math.pi / 2)
tuareg(y, 0.42, 0.6 - 0.04, Z0, -math.pi / 2)

# ---------------- outside: a caravan arriving ----------------
y.bolum('Dis kervan')
for k, (dx, dy, a) in enumerate(((-0.55, -1.02, 0.05), (-0.82, -1.06, 0.1), (0.62, -1.02, math.pi - 0.1))):
    deve(y, dx, dy, Z0, a, renk=('ahsap_acik', 'kum_koyu', 'kum')[k], yuk=True, olcek=1.0)
kisi(y, -0.38, -1.02, Z0, 0.1, govde='lacivert', bas='lacivert', mizrak='ahsap_koyu')
kisi(y, 0.45, -1.06, Z0, math.pi, govde='beyaz', bas='beyaz')
palmiye(y, 1.04, -0.35, Z0, boy=0.3, tohum=2)
palmiye(y, -1.05, 0.3, Z0, boy=0.28, tohum=5)

calistir(y, 'lm_timbuktukale')
