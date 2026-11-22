# Armada shipyard (lm_armada): the Atarazanas of Seville - five long parallel brick halls on pointed arcades, their
# gabled tile roofs in a sawtooth, open pointed arches towards the river; a galleon's frame on its stocks on a stone
# slipway with props, scaffolds and shipwrights; a finished great galleon alongside the quay under sail; a quay crane
# swinging a gun aboard, a shear-leg crane; timber and logs; the gun foundry: its hall, the furnace and stack, the
# casting pit with moulds, cast barrels on blocks and shot.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from ispanyol_ek import *

y = Yapi()
X0, X1, Y0, Y1 = -1.15, 1.15, -1.0, 0.98
ZS, ZK = 0.02, 0.06
QY = -0.15
TG = ('tugla', 'tugla_koyu', 'tas_acik', 'koyu')

# ================================================================ river and land
y.bolum('Nehir ve rıhtım')
kutu(y, V(X0, Y0, 0), X, X1 - X0, QY - Y0, ZS, 'kaya_koyu', 'onsagsol')
y.yuz_yon([V(X0, Y0, ZS), V(X1, Y0, ZS), V(X1, QY, ZS), V(X0, QY, ZS)], 'su', Z)
kutu(y, V(X0, QY, 0), X, X1 - X0, Y1 - QY, ZK, 'tas', 'arkasagsol')
duz_duvar(y, V(X0, QY), V(X1, QY), ZS - 0.004, ZK, 'tas')
silme(y, [V(X0, QY), V(X1, QY)], ZK - 0.008, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
silme(y, [V(X0, QY), V(X1, QY)], ZS - 0.003, 0.008, 0.005, 'kaya_koyu', 'duz', kapali=False)
y.yuz_yon([V(X0, QY, ZK), V(X1, QY, ZK), V(X1, Y1, ZK), V(X0, Y1, ZK)], 'zemin', Z)
for k in range(8):   # bollards
    xx = -0.2 + 0.17 * k
    y.prizma((xx, QY + 0.016), 0.0065, ZK, ZK + 0.018, 'kirec', n=8)
    kure(y, (xx, QY + 0.016, ZK + 0.02), 0.0072, 'kirec', n=8, kat=3)

# ================================================================ the slipway with the galleon's frame
y.bolum('Kızak ve kalyon iskeleti')
SX0, SX1, SY0 = -0.86, -0.3, -0.86
# the stone slipway running out into the river
kutu(y, V(SX0, SY0, 0), X, SX1 - SX0, QY - SY0 + 0.001, ZK, 'tas', 'onsagsol')
y.yuz_yon([V(SX0, SY0, ZK), V(SX1, SY0, ZK), V(SX1, QY, ZK), V(SX0, QY, ZK)], 'zemin', Z)
silme(y, [V(SX1, QY), V(SX1, SY0), V(SX0, SY0), V(SX0, QY)], ZS - 0.003, 0.008, 0.005, 'kaya_koyu', 'duz', kapali=False)
silme(y, [V(SX1, QY), V(SX1, SY0), V(SX0, SY0), V(SX0, QY)], ZK - 0.008, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
# the ground ways (two timber runners) and the keel blocks
SCX = (SX0 + SX1) / 2
for sx in (-1, 1):
    cubuk(y, V(SCX + sx * 0.07, SY0 + 0.03, ZK + 0.006), V(SCX + sx * 0.07, 0.02, ZK + 0.006), 0.022, 'ahsap_koyu', 0.012)
LI, BI = 0.78, 0.2
for k in range(9):
    yy_ = -0.8 + k * 0.085
    kutu_merkez(y, (SCX, yy_), 0.04, 0.03, 0.03, 'ahsap', z0=ZK)
kalyon_iskelet(y, SCX, -0.41, ZK + 0.03 + BI * 0.42 + 0.004 + BI * 0.035, -math.pi / 2, L=LI, B=BI, kaplama=0.45)
# shipwrights at work
for k, (xx, yy_, a) in enumerate(((SCX - 0.17, -0.62, 0.3), (SCX + 0.18, -0.3, 2.6), (SCX - 0.16, -0.2, -0.4), (SCX + 0.17, -0.7, 3.2))):
    asker(y, xx, yy_, ZK, 1.1, a, silah=None, govde=('kumas', 'boya_kirmizi', 'ahsap_acik', 'boya_yesil')[k], pantolon='ahsap_koyu', zirh=False)

# ================================================================ the Atarazanas halls
y.bolum('Tersane salonları')
NN, NW = 5, 0.25
HX0 = -1.1
HY0, HY1 = 0.02, 0.94
HH = 0.21
ZH = ZK + HH
for i in range(NN):
    x0, x1 = HX0 + i * NW, HX0 + (i + 1) * NW
    # the river end: a tall pointed arch open into the hall (dark), its voussoirs in stone and brick
    y.kemerli(V(x0, HY0), V(x1, HY0), ZK, HH, (TG[0], TG[1], TG[2], 'koyu'), v0=0.0, en=0.72, ust=0.02, derin=0.07, k_say=12, sivri=0.62,
              cerceve=(0.011, ['tas_acik', 'tugla_koyu']))
    # the back wall
    ucuz_cephe(y, V(x1, HY1), V(x0, HY1), ZK, HH, 2, 3, 'tugla', ince=True)
    cati_besik(y, x0, x1, HY0, HY1, ZH, 0.13, 0.014, 'kiremit', mahya='kiremit2', ucluk_key='tugla', ns=10, nr=4)
    # cover-tile ribs down both slopes
    xc = (x0 + x1) / 2
    for k in range(29):
        yy_ = HY0 + 0.016 + (HY1 - HY0 - 0.032) * k / 28
        for sx in (-1, 1):
            xe = xc + sx * (NW / 2 + 0.012)
            cubuk(y, V(xe, yy_, ZH - 0.001 + 0.0032), V(xc + sx * 0.008, yy_, ZH + 0.13 * (1 - 0.008 / (NW / 2 + 0.014)) + 0.0032), 0.006, 'kiremit2', 0.004)
    # a small oculus in the front gable
    y.oculus(V((x0 + x1) / 2, HY0 + 0.0005, ZH + 0.05), X, -Y, 0.018, 'koyu', 'tas_acik', f=0.005)
# buttresses at the arcade lines on the front
for i in range(NN + 1):
    xx = HX0 + i * NW + (0.015 if i == 0 else (-0.015 if i == NN else 0.0))   # (the end ones kept inside the corner)
    kutu3(y, V(xx, HY0 - 0.009, ZK + HH * 0.48), X, Y, Z, 0.03, 0.018, HH * 0.96, 'tugla_koyu', ('+x', '-x', '-y', '+z'))
    kutu3(y, V(xx, HY0 - 0.011, ZK + 0.014), X, Y, Z, 0.036, 0.022, 0.028, 'tas_acik', ('+x', '-x', '-y', '+z'))
silme(y, [V(HX0, HY0), V(HX0 + NN * NW, HY0)], ZH - 0.012, 0.012, 0.008, 'tas_acik', 'duz', kapali=False)
# the long sides: rows of pointed arches on brick piers (blind towards the street, open towards the yard)
for (a_, b_, koyu) in ((V(HX0, HY1), V(HX0, HY0), 'koyu'), (V(HX0 + NN * NW, HY0), V(HX0 + NN * NW, HY1), 'koyu')):
    n = 7
    for k in range(n):
        p, q = a_.lerp(b_, k / n), a_.lerp(b_, (k + 1) / n)
        y.kemerli(p, q, ZK, HH, (TG[0], TG[1], TG[2], koyu), v0=0.0, en=0.62, ust=0.03, derin=0.03, k_say=10, sivri=0.6,
                  cerceve=(0.008, ['tas_acik', 'tugla_koyu']))
    e_ = (b_ - a_).normalized(); nn = V(e_.y, -e_.x)
    for k in range(n + 1):
        p = a_.lerp(b_, k / n) + e_ * (0.011 if k == 0 else (-0.011 if k == n else 0.0))
        kutu3(y, V(p.x, p.y, ZK + HH * 0.45) + nn * 0.008, e_, -nn, Z, 0.022, 0.016, HH * 0.9, 'tugla_koyu', ('+x', '-x', '-y', '+z'))
    silme(y, [a_, b_], ZH - 0.012, 0.012, 0.008, 'tas_acik', 'duz', kapali=False)
y.bolum('Sancak')
sancak(y, HX0 + 2.5 * NW, HY0 + 0.01, ZH + 0.135, boy=0.2, en=0.14, yuk=0.085, aci=-math.pi * 0.8)

# ================================================================ timber yard
y.bolum('Kereste')
kereste(y, -0.02, -0.05, ZK, L=0.2, n=4, kat=3, aci=0.0)
kereste(y, 0.2, -0.09, ZK, L=0.16, n=3, kat=2, aci=0.3)
tomruk(y, -1.0, -0.06, ZK, L=0.22, n=3, r=0.013, aci=0.1)
tomruk(y, 0.26, 0.04, ZK, L=0.18, n=3, r=0.012, aci=1.3)
# a shear-leg crane lifting a timber by the slipway
vinc(y, -0.26, -0.06, ZK, math.pi * 0.95, boy=0.32, kol=0.2, yuk='kereste', ip_boy=0.12)
for k, (xx, yy_, a) in enumerate(((-0.1, -0.1, 2.0), (0.12, -0.02, -1.0))):
    asker(y, xx, yy_, ZK, 1.1, a, silah=None, govde=('boya_sari', 'kumas')[k], pantolon='ahsap_koyu', zirh=False)

# ================================================================ the gun foundry
y.bolum('Top dökümhanesi')
FX0, FX1, FY0, FY1 = 0.36, 1.08, 0.42, 0.94
FH = 0.18
fk = dikdortgen(FX0, FX1, FY0, FY1)
for k in range(4):   # the yard side: four open arches
    p, q = fk[0].lerp(fk[1], k / 4), fk[0].lerp(fk[1], (k + 1) / 4)
    y.kemerli(p, q, ZK, FH, (TG[0], TG[1], TG[2], 'koyu'), v0=0.0, en=0.66, ust=0.025, derin=0.04, k_say=10, sivri=0.55, cerceve=(0.008, 'tas_acik'))
ucuz_cephe(y, fk[1], fk[2], ZK, FH, 2, 4, 'tugla', ince=True)     # (east and north: never seen from the game's view)
ucuz_cephe(y, fk[2], fk[3], ZK, FH, 2, 6, 'tugla', ince=True)
# the west end towards the halls: two storeys of deep-set windows with stone sills, a door below
cephe(y, fk[3], fk[0], ZK, [(FH * 0.5, 0.34, 0.66, 0.02, 0.07, True), (FH * 0.5, 0.34, 0.66, 0.015, 0.066, False)], 4, atla=(1,),
      renk=TG, cerceve=(0.005, 'tas_acik'))
pd, qd = fk[3].lerp(fk[0], 1 / 4), fk[3].lerp(fk[0], 2 / 4)
y.kemerli(pd, qd, ZK, FH * 0.5, (TG[0], TG[1], TG[2], 'ahsap_koyu'), v0=0.0, en=0.56, ust=0.012, derin=0.02, k_say=8, cerceve=(0.006, 'tas_acik'))
silme(y, fk, ZK, 0.02, 0.008, 'tugla_koyu', 'kaide')
silme(y, fk, ZK + FH - 0.012, 0.012, 0.008, 'tas_acik', 'duz')
cati_besik(y, FX0, FX1, FY0, FY1, ZK + FH, 0.13, 0.025, 'kiremit', mahya='kiremit2', ucluk_key='tugla', ns=10, nr=5)
# the furnace stack rising through the roof, smoke
CX_, CY_ = 0.86, 0.74
kutu_merkez(y, (CX_, CY_), 0.09, 0.09, 0.58, 'tugla', z0=ZK)
for zz in (0.3, 0.5):
    silme(y, dikdortgen(CX_ - 0.045, CX_ + 0.045, CY_ - 0.045, CY_ + 0.045), ZK + zz, 0.01, 0.006, 'tugla_koyu', 'duz')
silme(y, dikdortgen(CX_ - 0.045, CX_ + 0.045, CY_ - 0.045, CY_ + 0.045), ZK + 0.565, 0.018, 0.01, 'tas_acik', 'tac')
y.yuz_yon(dikdortgen(CX_ - 0.03, CX_ + 0.03, CY_ - 0.03, CY_ + 0.03, ZK + 0.578), 'koyu', Z)
y.yuz_yon([V(CX_ - 0.045, CY_ - 0.045, ZK + 0.583), V(CX_ + 0.045, CY_ - 0.045, ZK + 0.583), V(CX_ + 0.03, CY_ - 0.03, ZK + 0.583), V(CX_ - 0.03, CY_ - 0.03, ZK + 0.583)], 'tas_acik', Z)
for (dx, dy, dz, r) in ((0, 0, 0.62, 0.035), (0.03, 0.02, 0.67, 0.045), (0.08, 0.03, 0.72, 0.055)):
    kure(y, (CX_ + dx, CY_ + dy, ZK + dz), r, 'tas_acik', n=9, kat=5)
# the reverberatory furnace in the yard: a brick dome with its fire mouth, a second short stack
FCX, FCY = 0.55, 0.22
donel(y, (FCX, FCY), [(0.1, ZK), (0.1, ZK + 0.05), (0.09, ZK + 0.09), (0.065, ZK + 0.12), (0.03, ZK + 0.135), (0.0, ZK + 0.138)], 'tugla', n=16)
y.kemerli(V(FCX - 0.035, FCY - 0.099), V(FCX + 0.035, FCY - 0.099), ZK, 0.06, ('tugla', 'tugla_koyu', 'tas_acik', 'boya_kirmizi'), v0=0.0, en=0.6, ust=0.008, derin=0.012, k_say=6)
kutu3(y, V(FCX, FCY - 0.1, ZK + 0.03), X, Y, Z, 0.07, 0.006, 0.06, 'tugla', ('+x', '-x', '+z'))
y.prizma((FCX + 0.05, FCY + 0.04), 0.018, ZK + 0.1, ZK + 0.22, 'tugla', n=8, ust=False)
y.yuz_yon(cokgen((FCX + 0.05, FCY + 0.04), 0.012, 8, z=ZK + 0.2195), 'koyu', Z)
y.serit(cokgen((FCX + 0.05, FCY + 0.04), 0.018, 8, z=ZK + 0.22), cokgen((FCX + 0.05, FCY + 0.04), 0.012, 8, z=ZK + 0.22), 'tugla_koyu')
kure(y, (FCX + 0.06, FCY + 0.05, ZK + 0.26), 0.03, 'tas_acik', n=8, kat=4)
# the casting pit: a sunk rim with clay moulds standing in it, a gun being hoisted out by shear legs
PCX, PCY = 0.86, 0.18
kutu_merkez(y, (PCX, PCY), 0.2, 0.14, 0.012, 'tas_koyu', z0=ZK)
y.yuz_yon(dikdortgen(PCX - 0.085, PCX + 0.085, PCY - 0.055, PCY + 0.055, ZK + 0.0125), 'toprak', Z)
for k in range(4):
    y.prizma((PCX - 0.06 + k * 0.04, PCY + 0.01), 0.012, ZK + 0.012, ZK + 0.05, 'kerpic', n=8)
for sx in (-1, 1):
    cubuk(y, V(PCX + sx * 0.09, PCY - 0.05, ZK), V(PCX, PCY - 0.01, ZK + 0.28), 0.008, 'ahsap')
cubuk(y, V(PCX, PCY + 0.1, ZK), V(PCX, PCY - 0.01, ZK + 0.28), 0.008, 'ahsap')
cubuk(y, V(PCX, PCY - 0.01, ZK + 0.28), V(PCX, PCY - 0.01, ZK + 0.17), 0.0018, 'ahsap_koyu')
top_namlu(y, V(PCX - 0.006, PCY - 0.01, ZK + 0.06), V(0.04, 0, 1), 0.11, 0.012, 'bronz')
# cast guns on timber blocks, shot, barrels, gun carriages
for k in range(3):
    yy_ = 0.0 + k * 0.05
    for sx in (-1, 1):
        kutu_merkez(y, (0.62 + sx * 0.05, yy_), 0.014, 0.03, 0.012, 'ahsap_koyu', z0=ZK)
    top_namlu(y, V(0.55, yy_, ZK + 0.024), V(1, 0, 0), 0.15, 0.012, 'bronz')
gulle_yigini(y, 0.78, -0.03, ZK, 4, 0.0075)
gulle_yigini(y, 0.96, -0.02, ZK, 3, 0.0075)
for xx, yy_ in ((1.03, 0.1), (1.06, 0.14), (1.04, 0.19), (1.0, 0.27)):
    varil(y, xx, yy_, ZK, 0.013, 0.032)
top_kizak(y, 0.75, 0.32, ZK, -math.pi / 2, L=0.12, r=0.013)
for k, (xx, yy_, a) in enumerate(((0.7, 0.2, 2.8), (0.95, 0.24, 2.0), (0.6, 0.12, -0.5))):
    asker(y, xx, yy_, ZK, 1.1, a, silah=None, govde=('ahsap_acik', 'boya_kirmizi', 'kumas')[k], pantolon='ahsap_koyu', zirh=False)

# ================================================================ the great galleon and the quay crane
y.bolum('Büyük kalyon')
kalyon(y, 0.33, -0.43, ZS, 0.0, L=0.98, B=0.22, yelken='acik', tohum=7)
y.bolum('Rıhtım vinci, çapalar, halatlar')
capa(y, 0.82, QY + 0.06, ZK, 0.4, 1.3)
capa(y, -0.12, 0.12, ZK, -0.9, 1.2)
for (xx, yy_) in ((0.96, QY + 0.05), (1.02, QY + 0.1), (0.66, QY + 0.04)):
    halat(y, xx, yy_, ZK)
direk_yigini(y, -0.62, 0.1 - 0.02, ZK, L=0.42, n=5, aci=0.0)
for k, (xx, yy_, a) in enumerate(((0.55, QY + 0.04, 1.2), (0.3, QY + 0.05, 2.0), (0.9, QY + 0.11, -2.2), (-0.4, 0.06, 0.3), (-0.8, 0.0, 1.0))):
    asker(y, xx, yy_, ZK, 1.1, a, silah=None, govde=('boya_kirmizi', 'kumas', 'boya_sari', 'boya_yesil', 'ahsap_acik')[k], pantolon='ahsap_koyu', zirh=False)
vinc(y, 0.42, QY + 0.06, ZK, -math.pi / 2, boy=0.42, kol=0.27, yuk='top', ip_boy=0.18)
sandal(y, -1.0, -0.5, ZS, -1.2)
sandal(y, -0.12, -0.78, ZS, 0.6)
sandal(y, 0.98, -0.85, ZS, 2.4)
dalga(y, X0 + 0.05, X1 - 0.05, Y0 + 0.05, QY - 0.05, ZS, n=40, tohum=8, boy=0.035,
      kacin=lambda x, yy: (SX0 - 0.04 < x < SX1 + 0.04 and yy > SY0 - 0.04) or (abs(x - 0.33) < 0.62 and abs(yy + 0.43) < 0.16))

calistir(y, 'lm_armada')
