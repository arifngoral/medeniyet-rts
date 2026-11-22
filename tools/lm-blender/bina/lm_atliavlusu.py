# Horsemen's Court (lm_atliavlusu): the cavalry stables of the Mansa - a great mud-walled yard with pilasters,
# pinnacles and torons, entered through a gatehouse under a tall tapering mud tower; thatched lean-to stables along
# the walls with caparisoned war horses at their fodder troughs, the captain's Djenne house, a well and water
# troughs, hay stacks, riders exercising in the yard and spear-and-shield guards at the gate.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
import mali_ortak
from mali_ortak import *

y = Yapi()
Z0 = 0.03
mali_ortak.ZEMIN_Z[0] = Z0
CX0, CX1, CY0, CY1 = -0.95, 0.95, -0.8, 0.92
CH = 0.17
KAL = 0.03

y.bolum('Zemin')
zemin(y, -1.15, 1.15, -1.08, 1.08, Z0, KK, 'toprak', basamak=(), silmeli=True)

# ---------------- the yard wall ----------------
y.bolum('Avlu duvari')
yan = [dict(n=9, acik={4: dict(tip='gecit', en=0.8, v0=0, v1=0.155, kemer=0.3, ic=True)}),
       dict(n=8, acik={3: dict(tip='nis', en=0.4, v0=0.05, v1=0.12, kemer=0.3)}),
       dict(n=9), dict(n=8, acik={5: dict(tip='nis', en=0.4, v0=0.05, v1=0.12, kemer=0.3)})]
sahel_kutu(y, dikdortgen(CX0, CX1, CY0, CY1), Z0, CH, K, kalin=KAL, dam=None, yanlar=yan, payanda_w=0.03, payanda_d=0.022,
           payanda_tepe=0.045, kose_w=0.075, kose_tepe=0.09, kose_ust=0.05, payanda_ust=0.025, toron_sira=(0.5,), ic_payanda=True,
           kose_yumurta=True)

# ---------------- the gatehouse and its tower ----------------
y.bolum('Kapi kulesi')
GX0, GX1, GY0, GY1 = -0.24, 0.24, -0.93, -0.67
GH = 0.3
GD = Z0 + GH - 0.03
PW, PH = 0.15, 0.135          # the passage
gen = PW / ((GX1 - GX0) / 3)
yang = [dict(n=3, acik={1: dict(tip='gecit', en=gen, v0=0, v1=PH, kemer=0.3, ic=False)}, payanda=False),
        dict(n=2, acik={0: dict(tip='pencere', en=0.3, v0=0.18, v1=0.23, kafes=True)}),
        dict(n=3, acik={1: dict(tip='gecit', en=gen, v0=0, v1=PH, kemer=0.3, ic=False)}),
        dict(n=2, acik={1: dict(tip='pencere', en=0.3, v0=0.18, v1=0.23, kafes=True)})]
sahel_kutu(y, dikdortgen(GX0, GX1, GY0, GY1), Z0, GH, K, kalin=0.03, dam=GD, yanlar=yang, payanda_w=0.03, payanda_d=0.022,
           payanda_tepe=0.045, kose_w=0.07, kose_tepe=0.085, kose_ust=0.05, payanda_ust=0.03, toron_sira=(0.55, 0.85), kademe=True)
# the passage: its walls, the flat ceiling of palm beams, the doors standing open against the walls
py0, py1 = GY0 + 0.03, GY1 - 0.03
for s in (-1, 1):
    xw = s * PW / 2
    y.yuz_yon([V(xw, py0, Z0), V(xw, py1, Z0), V(xw, py1, Z0 + PH), V(xw, py0, Z0 + PH)], KK, V(-s, 0, 0))
    kutu_merkez(y, (xw - s * 0.004, py0 + 0.045), 0.006, 0.07, PH * 0.66, 'ahsap_koyu', z0=Z0)
y.yuz_yon([V(-PW / 2, py0, Z0 + PH), V(PW / 2, py0, Z0 + PH), V(PW / 2, py1, Z0 + PH), V(-PW / 2, py1, Z0 + PH)], 'ahsap', -Z)
for k in range(6):
    yy = py0 + 0.012 + (py1 - py0 - 0.024) * k / 5
    cubuk(y, V(-PW / 2, yy, Z0 + PH - 0.004), V(PW / 2, yy, Z0 + PH - 0.004), 0.007, 'ahsap_koyu')
# the facade: two great pilasters flanking the gate rising over the roof, and the potige over it
for s in (-1, 1):
    payanda(y, V(s * 0.105, GY0), X, -Y, Z0, Z0 + GH + 0.07, 0.04, 0.034, K, 0.075, arka_z=Z0 + GH)
kutu_merkez(y, (0, GY0 - 0.018), 0.25, 0.04, 0.04, K, z0=Z0 + PH + 0.025, yuzler='onsagsolust')
y.yuz_yon([V(-0.125, GY0 + 0.002, Z0 + PH + 0.025), V(0.125, GY0 + 0.002, Z0 + PH + 0.025), V(0.125, GY0 - 0.038, Z0 + PH + 0.025), V(-0.125, GY0 - 0.038, Z0 + PH + 0.025)], KK, -Z)
for k in range(6):
    toron(y, V(-0.1 + 0.04 * k, GY0 - 0.038, Z0 + PH + 0.05), -Y, 0.014, 0.0045)
# the tower
sahel_minare(y, (0, (GY0 + GY1) / 2), 0.25, 0.165, GD, 0.5, K, kaburga=2, toron_sira=6,
             pencereler=((-Y, (0.3, 0.6)), (-X, (0.45,))), ust=0.065)
sancak(y, -0.19, GY0 + 0.05, GD, boy=0.2, en=0.1, yuk=0.065, aci=math.pi * 0.9)

# ---------------- the stables ----------------
y.bolum('Ahirlar')
ZU, ZO, DR = Z0 + CH - 0.016, Z0 + 0.11, 0.19
sundurma(y, (CX0 + KAL, CY0 + 0.26), (CX0 + KAL, CY1 - KAL - 0.01), ZU, ZO, DR, n_direk=6)      # along the west wall
sundurma(y, (-0.64, CY1 - KAL), (0.38, CY1 - KAL), ZU, ZO, DR, n_direk=5)                          # along the north wall
sundurma(y, (CX1 - KAL, CY1 - 0.5), (CX1 - KAL, CY0 + 0.26), ZU, ZO, DR, n_direk=4)               # along the east wall
# fodder troughs at the walls and the horses tied to them
yalak(y, (CX0 + KAL + 0.13, CY0 + 0.32), (CX0 + KAL + 0.13, CY1 - 0.1), Z0, en=0.04, h=0.022, ic='saz')
yalak(y, (-0.6, CY1 - KAL - 0.13), (0.34, CY1 - KAL - 0.13), Z0, en=0.04, h=0.022, ic='saz')
yalak(y, (CX1 - KAL - 0.13, CY0 + 0.3), (CX1 - KAL - 0.13, CY1 - 0.55), Z0, en=0.04, h=0.022, ic='saz')
RENK = ['ahsap', 'beyaz', 'koyu', 'ahsap_acik', 'ahsap', 'kum_koyu', 'beyaz', 'ahsap_koyu']
CUL = [('boya_kirmizi', 'boya_sari'), ('boya_yesil', 'beyaz'), ('boya_sari', 'boya_kirmizi'), ('lacivert', 'boya_sari'),
       ('beyaz', 'boya_kirmizi'), ('boya_kirmizi', 'beyaz'), ('turuncu', 'koyu'), ('boya_yesil', 'boya_sari')]
k = 0
for i in range(6):
    yy = CY0 + 0.36 + (CY1 - CY0 - 0.5) * i / 5
    c1, c2 = CUL[k % 8]
    mali_at(y, CX0 + KAL + 0.235, yy, Z0, math.pi, RENK[k % 8], c1, c2, bas_egik=0.7 * (i % 2)); k += 1
for i in range(6):
    xx = -0.54 + 0.84 * i / 5
    c1, c2 = CUL[k % 8]
    mali_at(y, xx, CY1 - KAL - 0.235, Z0, math.pi / 2, RENK[k % 8], c1, c2, bas_egik=0.7 * ((i + 1) % 2)); k += 1
for i in range(3):
    yy = CY0 + 0.36 + 0.2 * i
    c1, c2 = CUL[k % 8]
    mali_at(y, CX1 - KAL - 0.235, yy, Z0, 0.0, RENK[k % 8], c1, c2, bas_egik=0.7 * (i % 2)); k += 1
# straw bedding under the sheds (mats on the trodden earth)
hasir(y, CX0 + KAL + 0.2, (CY0 + 0.3 + CY1) / 2, Z0, 0.13, CY1 - CY0 - 0.42, 0.0, 'saz', 'saz_koyu')
hasir(y, -0.13, CY1 - KAL - 0.2, Z0, 0.98, 0.13, 0.0, 'saz', 'saz_koyu')
hasir(y, CX1 - KAL - 0.2, CY0 + 0.47, Z0, 0.13, 0.42, 0.0, 'saz', 'saz_koyu')
# grooms with the stabled horses: one carrying fodder, one brushing a horse, one leading a horse out
kisi(y, CX0 + KAL + 0.3, CY0 + 0.56, Z0, 0.0, 'kumas', 'beyaz', yuk='saz')
kisi(y, -0.33, CY1 - KAL - 0.3, Z0, math.pi / 2, 'beyaz', 'boya_sari', kol=0.7)
kisi(y, 0.2, CY1 - KAL - 0.31, Z0, -math.pi / 2, 'boya_yesil', 'beyaz', kol=0.5)
# the saddler's shade by the east stables: saddles, quilted caparisons and spears racked under a reed mat
golgelik(y, 0.58, CY0 + 0.17, Z0, 0.22, 0.16, 0.12, aci=math.pi / 2, mal=['kumas', 'kumas'], tohum=3, ortu=('saz', 'saz_koyu'))
for k2 in range(5):
    cubuk(y, V(CX1 - 0.07, CY0 + 0.05 + 0.025 * k2, Z0), V(CX1 - 0.05, CY0 + 0.05 + 0.025 * k2, Z0 + 0.12), 0.0022, 'ahsap')
    donel(y, (CX1 - 0.05 + 0.0018, CY0 + 0.05 + 0.025 * k2), [(0.0, Z0 + 0.12), (0.0028, Z0 + 0.122), (0.0, Z0 + 0.133)], 'demir', n=4)
cubuk(y, V(CX1 - 0.065, CY0 + 0.04, Z0 + 0.09), V(CX1 - 0.065, CY0 + 0.16, Z0 + 0.09), 0.004, 'ahsap_koyu')
oturan(y, 0.58, CY0 + 0.3, Z0, -math.pi / 2, 'boya_kirmizi', 'beyaz')
# water jars by the well, date palms shading the yard
for k2, (jx_, jy_) in enumerate(((-0.29, 0.31), (-0.27, 0.34), (-0.12, 0.33))):
    kup_(y, jx_, jy_, Z0, 0.015, 0.042)
palmiye(y, 0.05, 0.42, Z0, boy=0.34, tohum=4)
palmiye(y, -0.62, 0.05, Z0, boy=0.3, tohum=7)
# hay stacks and saddles
saman(y, CX0 + 0.12, CY0 + 0.12, Z0, 0.06, 0.08)
saman(y, CX0 + 0.25, CY0 + 0.1, Z0, 0.05, 0.065)
saman(y, CX1 - 0.12, CY1 - 0.62, Z0, 0.055, 0.07)

# granaries: small round mud stores on stone feet with thatched caps
for gx_, gy_ in ((0.3, 0.3), (0.42, 0.24)):
    for a_ in range(4):
        kutu_merkez(y, (gx_ + 0.03 * math.cos(a_ * TAU / 4 + 0.7), gy_ + 0.03 * math.sin(a_ * TAU / 4 + 0.7)), 0.018, 0.018, 0.02, 'kaya', z0=Z0)
    kulube(y, gx_, gy_, Z0 + 0.02, 0.045, 0.07, 0.065, K, kapi_aci=-2.4, n=12, sacak=0.016)

# ---------------- the captain's house ----------------
y.bolum('Ev')
djenne_ev(y, 0.67, 0.64, 0.42, 0.42, 0.29, 0.0, kat=2, tukolor=True, z=Z0)

# ---------------- the yard ----------------
y.bolum('Avlu')
# the well with a pulley frame and the water troughs by it
wx, wy = -0.2, 0.25
donel(y, (wx, wy), [(0.05, Z0), (0.05, Z0 + 0.04), (0.042, Z0 + 0.045), (0.036, Z0 + 0.04), (0.036, Z0 + 0.025)], K, n=12)
y.yuz_yon([V(wx + 0.036 * math.cos(TAU * i / 12), wy + 0.036 * math.sin(TAU * i / 12), Z0 + 0.025) for i in range(12)], 'su', Z)
for s in (-1, 1):
    cubuk(y, V(wx + s * 0.045, wy, Z0 + 0.04), V(wx + s * 0.04, wy, Z0 + 0.12), 0.007, 'ahsap')
cubuk(y, V(wx - 0.055, wy, Z0 + 0.118), V(wx + 0.055, wy, Z0 + 0.118), 0.007, 'ahsap_koyu')
yalak(y, (wx + 0.08, wy - 0.08), (wx + 0.3, wy - 0.08), Z0, en=0.045, h=0.025)
yalak(y, (wx - 0.3, wy - 0.06), (wx - 0.09, wy - 0.06), Z0, en=0.045, h=0.025)
kisi(y, wx + 0.06, wy + 0.03, Z0, math.pi, 'kumas', 'beyaz', kol=0.8)
mali_at(y, wx + 0.2, wy - 0.19, Z0, math.pi / 2, 'beyaz', 'boya_kirmizi', 'boya_sari', bas_egik=0.8)
mali_at(y, wx - 0.2, wy - 0.18, Z0, math.pi / 2 + 0.15, 'ahsap', 'boya_yesil', 'beyaz', bas_egik=0.8)
kisi(y, wx - 0.12, wy - 0.22, Z0, 1.2, 'boya_sari', 'beyaz')
# the riding ring: a raked sand track where riders exercise at the gallop, a captain watching
RX, RY, RR, RW = -0.3, -0.36, 0.27, 0.07
nr = 28
for i in range(nr):
    t0, t1 = TAU * i / nr, TAU * (i + 1) / nr
    P_ = lambda r, t: V(RX + r * math.cos(t), RY + r * math.sin(t), Z0 + 0.0015)
    y.yuz_yon([P_(RR - RW / 2, t0), P_(RR + RW / 2, t0), P_(RR + RW / 2, t1), P_(RR - RW / 2, t1)], 'kum_acik', Z)
    for r_, yon in ((RR + RW / 2, 1), (RR - RW / 2, -1)):
        a_, b_ = P_(r_, t0), P_(r_, t1)
        y.yuz_yon([a_ - Z * 0.0015, b_ - Z * 0.0015, b_, a_], 'kum_acik', (a_ + b_) / 2 - V(RX, RY, a_.z) if yon > 0 else V(RX, RY, a_.z) - (a_ + b_) / 2)
# the ring's low post-and-rail fence on its inner edge
for i in range(10):
    t = TAU * i / 10
    p = V(RX + (RR - RW / 2 - 0.01) * math.cos(t), RY + (RR - RW / 2 - 0.01) * math.sin(t))
    cubuk(y, p + Z * Z0, p + Z * (Z0 + 0.03), 0.005, 'ahsap')
    q = V(RX + (RR - RW / 2 - 0.01) * math.cos(t + TAU / 10), RY + (RR - RW / 2 - 0.01) * math.sin(t + TAU / 10))
    cubuk(y, p + Z * (Z0 + 0.026), q + Z * (Z0 + 0.026), 0.0035, 'ahsap_acik')
BIN = [('beyaz', 'beyaz', 'ahsap', 'kiremit'), ('boya_kirmizi', 'beyaz', 'ahsap', None), ('kobalt', 'kobalt', 'ahsap', 'kiremit'),
       ('boya_sari', 'boya_kirmizi', 'ahsap', 'kiremit')]
ATR = [('koyu', 'boya_kirmizi', 'boya_sari'), ('ahsap_acik', 'lacivert', 'boya_sari'), ('beyaz', 'boya_yesil', 'boya_kirmizi'), ('ahsap', 'boya_sari', 'koyu')]
for i in range(4):
    t = 0.5 + TAU * i / 4 + 0.3 * (i % 2)
    r_, c1, c2 = ATR[i]
    mali_at(y, RX + RR * math.cos(t), RY + RR * math.sin(t), Z0, t + math.pi / 2, r_, c1, c2, poz='kos', faz=0.25 * i, binici=BIN[i])
kisi(y, RX, RY, Z0, 0.3, 'boya_kirmizi', 'boya_sari', kol=0.9)
kisi(y, RX + 0.04, RY - 0.03, Z0, 0.9, 'beyaz', 'beyaz')
# a drummer and a horn-blower by the ring
kisi(y, RX + 0.34, RY - 0.12, Z0, 2.4, 'boya_yesil', 'beyaz', kol=0.6)
donel(y, (RX + 0.3, RY - 0.14), [(0.0, Z0), (0.012, Z0), (0.016, Z0 + 0.03), (0.0, Z0 + 0.03)], 'ahsap', n=10)
donel(y, (RX + 0.3, RY - 0.14), [(0.0165, Z0 + 0.0298), (0.0, Z0 + 0.031)], 'kece', n=10)
mali_at(y, 0.48, -0.1, Z0, 2.6, 'beyaz', 'boya_yesil', 'boya_kirmizi', poz='dur', binici=('kobalt', 'kobalt', 'ahsap', 'kiremit'))
kisi(y, 0.34, 0.08, Z0, 0.6, 'beyaz', 'boya_kirmizi', kol=1.0)      # the master of horse
# guards at the gate, inside and out
for gx_, gy_, a in ((-0.12, GY1 + 0.04, -math.pi / 2), (0.12, GY1 + 0.04, -math.pi / 2), (-0.14, GY0 - 0.07, -math.pi / 2), (0.14, GY0 - 0.07, -math.pi / 2)):
    kisi(y, gx_, gy_, Z0, a, 'boya_kirmizi', 'beyaz', mizrak='ahsap', kalkan='kiremit')

# ---------------- outside ----------------
y.bolum('Dis')
mali_at(y, -0.55, -0.98, Z0, 0.1, 'ahsap', 'boya_sari', 'boya_kirmizi', poz='dur', binici=('beyaz', 'boya_sari', 'ahsap', 'kiremit'))
mali_at(y, 0.55, -0.98, Z0, math.pi - 0.1, 'beyaz', 'boya_kirmizi', 'beyaz', poz='dur', binici=('kobalt', 'beyaz', 'ahsap', None))
kisi(y, 0.4, -1.0, Z0, 2.8, 'kumas', 'beyaz')
akasya(y, -1.03, -0.95, Z0, boy=0.24, tohum=2)
akasya(y, 1.04, 0.95, Z0, boy=0.22, tohum=6)
baobab(y, 1.03, -0.93, Z0, boy=0.3, tohum=3)
saman(y, -1.05, 0.5, Z0, 0.05, 0.07)

calistir(y, 'lm_atliavlusu')
