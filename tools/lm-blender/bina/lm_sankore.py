# Sankore Madrasa, Timbuktu (lm_sankore): the mud mosque-university - its stepped pyramid minaret bristling with
# toron beams rising from the prayer hall, a square court ringed by student cells, a library loggia with shelves of
# manuscripts and a reading room on the roof, a studded entrance portal; scholars teaching circles of students with
# wooden writing boards in the court, a well and a shade tree; flat roofs dotted with skylight lanterns.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mali_ek import *

import doku

y = Yapi()
Z0 = 0.035


# the plaster is renewed piece by piece each year (the crepissage): broad soft patches of fresher / older mud, the
# upper walls and the minaret's top bleached by the sun, the feet darkened by splash and damp - per corner, so the
# tone flows over the (grid-split) faces instead of changing face by face
def _sv(c0, c1, t):
    t = max(0.0, min(1.0, t))
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def siva_renk(taban, taze, eski, gunes, dip):
    def f(x, yy, z):
        n = (math.sin(x * 3.3 + 0.4) * math.cos(yy * 2.9 - 1.1) * 0.45 + math.sin(x * 7.9 - yy * 6.1 + 2.0) * 0.25 +
             math.sin(x * 9.7 + yy * 3.1 + z * 6.0) * math.cos(yy * 8.3 - x * 2.2) * 0.4)
        c = _sv(taban, taze, _ss(0.05, 0.6, n)) if n > 0 else _sv(taban, eski, _ss(0.05, 0.6, -n))
        c = _sv(c, gunes, 0.55 * _ss(Z0 + 0.12, Z0 + 0.9, z) + 0.12 * _ss(0.3, 0.9, math.sin(x * 5.3 + yy * 4.1)))
        return _sv(c, dip, 0.6 * _ss(Z0 + 0.05, Z0 + 0.005, z))
    return f


doku.KOSE_RENK['kerpic'] = siva_renk((0.74, 0.53, 0.35), (0.82, 0.56, 0.31), (0.66, 0.52, 0.42), (0.86, 0.70, 0.50), (0.58, 0.40, 0.27))
doku.KOSE_RENK['siva_oker'] = siva_renk((0.84, 0.62, 0.38), (0.88, 0.64, 0.36), (0.78, 0.60, 0.42), (0.91, 0.76, 0.55), (0.62, 0.44, 0.29))

# the plan: prayer hall behind (+y), the court in front of it ringed by the wings, the entrance portal in the front wing
HX0, HX1, HY0, HY1, HH = -0.98, 0.98, 0.36, 0.98, 0.25
MX, MY = 0.0, 0.36                             # the minaret's centre (on the hall's court wall)
FY0, FY1, FH = -0.98, -0.6, 0.155              # the front wing
WY0, WY1, WH = -0.52, 0.3, 0.165                # the side wings
CX = 0.58                                      # the court's half width

y.bolum('Zemin')
zemin(y, -1.13, 1.13, -1.16, 1.1, Z0, KK, 'kum_acik', basamak=(('on', 0.4),), silmeli=True)

# ---------------- prayer hall ----------------
y.bolum('Ibadet salonu')
n_on = 14
bw = (HX1 - HX0) / n_on
acik_on = {}
for b in range(n_on):
    xc = HX0 + bw * (b + 0.5)
    if abs(xc - MX) < 0.3: continue
    acik_on[b] = dict(tip='nis', en=0.56, v0=0.012, v1=0.175, kemer=0.42, derin=0.05, arka='koyu')
yan_hall = [dict(n=n_on, acik=acik_on),
            dict(n=5, acik={1: dict(tip='pencere', en=0.3, v0=0.11, v1=0.17, kafes=True), 3: dict(tip='pencere', en=0.3, v0=0.11, v1=0.17, kafes=True)}),
            dict(n=12),
            dict(n=5, acik={2: dict(tip='kapi', en=0.42, v0=0, v1=0.16, kemer=0.3), 0: dict(tip='pencere', en=0.3, v0=0.11, v1=0.17, kafes=True),
                            4: dict(tip='pencere', en=0.3, v0=0.11, v1=0.17, kafes=True)})]
sahel_kutu(y, dikdortgen(HX0, HX1, HY0, HY1), Z0, HH, K, kalin=0.03, dam=Z0 + HH - 0.03, yanlar=yan_hall, payanda_ara=0.14,
           kose_w=0.06, kose_tepe=0.08, kose_yumurta=True, kademe=True)
# skylight lanterns and gutters on the hall roof
# the roof's joints: low rounded ridges over the beam lines, the skylights in the bays between them
ZD = Z0 + HH - 0.03
for gy in (0.6, 0.8):
    for xa, xb in ((HX0 + 0.03, -0.31), (0.31, HX1 - 0.03)):
        cubuk(y, V(xa, gy, ZD + 0.004), V(xb, gy, ZD + 0.004), 0.016, K, 0.012)
cubuk(y, V(-0.31, 0.8, ZD + 0.004), V(0.31, 0.8, ZD + 0.004), 0.016, K, 0.012)
for gx in (-0.66, -0.33, 0.33, 0.66):
    cubuk(y, V(gx, HY0 + 0.03, ZD + 0.004), V(gx, HY1 - 0.03, ZD + 0.004), 0.016, K, 0.012)
for gx in (-0.82, -0.5, -0.18, 0.18, 0.5, 0.82):
    for gy in (0.48, 0.7, 0.89):
        if abs(gx) < 0.3 and gy < 0.7: continue
        fener(y, gx, gy, ZD)
for gx in (-0.7, -0.35, 0.35, 0.7):
    oluk(y, V(gx, HY1), V(0, 1), Z0 + HH - 0.02, 0.04)
for gy in (0.5, 0.8):
    oluk(y, V(HX0, gy), V(-1, 0), Z0 + HH - 0.02, 0.04)
    oluk(y, V(HX1, gy), V(1, 0), Z0 + HH - 0.02, 0.04)

# ---------------- the stepped minaret ----------------
y.bolum('Minare')
tepe, teras = kademeli_minare(y, (MX, MY), [(0.56, 0.5, 0.28), (0.38, 0.33, 0.26), (0.25, 0.21, 0.23), (0.14, 0.115, 0.18)], Z0,
                              kaburga=(3, 3, 2, 1), toron_sira=(5, 4, 4, 3), kapi=-Y)
# the wooden ladder poles left in the wall for re-plastering (the crepissage scaffold)
for s in (-1, 1):
    cubuk(y, V(MX + s * 0.12, MY - 0.252, Z0 + 0.1), V(MX + s * 0.12, MY - 0.238, Z0 + 0.34), 0.006, 'ahsap_acik')

# ---------------- side wings: student cells (west), the library loggia (east) ----------------
y.bolum('Ogrenci odalari')
cell = {}
for b in range(6):
    cell[b] = dict(tip='kapi', en=0.42, v0=0, v1=0.12, kemer=0.3) if b % 2 == 0 else dict(tip='pencere', en=0.32, v0=0.07, v1=0.12, kafes=True)
yan_bati = [dict(n=3, acik={1: dict(tip='pencere', en=0.32, v0=0.07, v1=0.12, kafes=True)}), dict(n=6, acik=cell),
            dict(n=3), dict(n=6, acik={1: dict(tip='pencere', en=0.3, v0=0.08, v1=0.12, kafes=True), 4: dict(tip='pencere', en=0.3, v0=0.08, v1=0.12, kafes=True)})]
sahel_kutu(y, dikdortgen(HX0, -CX, WY0, WY1), Z0, WH, KT, kalin=0.026, dam=Z0 + WH - 0.028, yanlar=yan_bati, payanda_ara=0.13,
           kose_w=0.05, kose_tepe=0.06)
yan_dogu = [dict(n=3, acik={1: dict(tip='pencere', en=0.32, v0=0.07, v1=0.12, kafes=True)}),
            dict(n=6, acik={1: dict(tip='pencere', en=0.3, v0=0.08, v1=0.12, kafes=True), 4: dict(tip='pencere', en=0.3, v0=0.08, v1=0.12, kafes=True)}),
            dict(n=3), dict(n=4, acik={0: dict(tip='kapi', en=0.4, v0=0, v1=0.13, kemer=0.3), 2: dict(tip='kapi', en=0.4, v0=0, v1=0.13, kemer=0.3)},
                            payanda=False, toron=False)]
sahel_kutu(y, dikdortgen(CX, HX1, WY0, WY1), Z0, WH, K, kalin=0.026, dam=Z0 + WH - 0.028, yanlar=yan_dogu, payanda_ara=0.13,
           kose_w=0.05, kose_tepe=0.06)
for xx in (-0.86, -0.7):
    for yy in (-0.3, -0.05, 0.12):
        fener(y, xx, yy, Z0 + WH - 0.028, w=0.034)
for yy in (-0.3, -0.05, 0.12):
    fener(y, 0.86, yy, Z0 + WH - 0.028, w=0.034)

y.bolum('Kutuphane revagi')
# the library loggia against the east wing's court wall: a thatched lean-to on posts sheltering the shelves
ZEMIN_Z[0] = Z0
sundurma(y, V(CX, WY1 - 0.04), V(CX, WY0 + 0.04), Z0 + WH - 0.025, Z0 + 0.13, 0.13, n_direk=3)
# shelves (a low wooden rack along the wall) full of manuscript bundles, and chests
for k in range(3):
    y0_ = WY0 + 0.1 + k * 0.2
    xr = CX - 0.022
    for zz in (Z0, Z0 + 0.04, Z0 + 0.08):
        kutu_merkez(y, (xr, y0_ + 0.06), 0.04, 0.15, 0.004, 'ahsap_koyu', z0=zz + 0.036)
    for dy in (0.0, 0.12):
        cubuk(y, V(xr - 0.018, y0_ + dy, Z0), V(xr - 0.018, y0_ + dy, Z0 + 0.124), 0.005, 'ahsap_koyu')
    for zz in (Z0 + 0.04, Z0 + 0.08):
        for j in range(3):
            el_yazmasi(y, xr, y0_ + 0.02 + j * 0.042, zz, math.pi / 2, n=2, tohum=k * 10 + j + int(zz * 100))
    kutu_merkez(y, (CX - 0.05, y0_ + 0.06), 0.04, 0.03, 0.026, 'ahsap', z0=Z0, aci=0.1 * k)
    kutu_merkez(y, (CX - 0.05, y0_ + 0.06), 0.042, 0.032, 0.005, 'ahsap_koyu', z0=Z0 + 0.026, aci=0.1 * k)
# scholars reading in the loggia
oturan(y, CX - 0.1, -0.33, Z0, math.pi, govde='beyaz', bas='beyaz')
el_yazmasi(y, CX - 0.125, -0.36, Z0, 0.3, n=1)
oturan(y, CX - 0.1, 0.03, Z0, math.pi, govde='boya_sari', bas='beyaz')
el_yazmasi(y, CX - 0.125, 0.0, Z0, -0.2, n=2, tohum=4)
hasir(y, CX - 0.1, -0.15, Z0, 0.09, 0.42, 0.0)

# ---------------- front wing and the entrance portal ----------------
y.bolum('On kanat')
yan_on_sol = [dict(n=6, acik={b: dict(tip='pencere', en=0.34, v0=0.09, v1=0.15, kafes=True) for b in (0, 2, 4)} |
                   {b: dict(tip='nis', en=0.4, v0=0.02, v1=0.07, derin=0.012) for b in (1, 3, 5)}),
              dict(n=3), dict(n=6, acik={1: dict(tip='kapi', en=0.4, v0=0, v1=0.13, kemer=0.3), 4: dict(tip='kapi', en=0.4, v0=0, v1=0.13, kemer=0.3)}),
              dict(n=3, acik={1: dict(tip='pencere', en=0.32, v0=0.09, v1=0.15, kafes=True)})]
sahel_kutu(y, dikdortgen(HX0, -0.17, FY0, FY1), Z0, FH, K, kalin=0.028, dam=Z0 + FH - 0.03, yanlar=yan_on_sol, payanda_ara=0.13,
           kose_w=0.055, kose_tepe=0.07, kose_yumurta=True)
yan_on_sag = [dict(n=6, acik={b: dict(tip='pencere', en=0.34, v0=0.09, v1=0.15, kafes=True) for b in (1, 3, 5)} |
                   {b: dict(tip='nis', en=0.4, v0=0.02, v1=0.07, derin=0.012) for b in (0, 2, 4)}),
              dict(n=3, acik={1: dict(tip='pencere', en=0.32, v0=0.09, v1=0.15, kafes=True)}),
              dict(n=6, acik={1: dict(tip='kapi', en=0.4, v0=0, v1=0.13, kemer=0.3), 4: dict(tip='kapi', en=0.4, v0=0, v1=0.13, kemer=0.3)}),
              dict(n=3)]
sahel_kutu(y, dikdortgen(0.17, HX1, FY0, FY1), Z0, FH, K, kalin=0.028, dam=Z0 + FH - 0.03, yanlar=yan_on_sag, payanda_ara=0.13,
           kose_w=0.055, kose_tepe=0.07, kose_yumurta=True)
for xx in (-0.8, -0.55, -0.3, 0.3, 0.55, 0.8):
    fener(y, xx, -0.7, Z0 + FH - 0.03, w=0.034)
# dyed cloth drying on a line on the east roof (indigo, madder red, ochre), mats rolled out beside it
zr_ = Z0 + FH - 0.03
for x0_, x1_ in ((0.36, 0.9),):
    for xx in (x0_, x1_):
        cubuk(y, V(xx, -0.88, zr_), V(xx, -0.88, zr_ + 0.075), 0.006, 'ahsap')
    cubuk(y, V(x0_, -0.88, zr_ + 0.072), V(x1_, -0.88, zr_ + 0.072), 0.003, 'saz_koyu')
    for k, (ka, kb, kk) in enumerate(((0.4, 0.5, 'lacivert'), (0.53, 0.63, 'boya_kirmizi'), (0.66, 0.74, 'boya_sari'), (0.77, 0.86, 'kumas'))):
        dz = 0.04 + 0.006 * (k % 2)
        ince_levha(y, [V(ka, -0.878, zr_ + 0.07 - dz), V(kb, -0.878, zr_ + 0.07 - dz), V(kb, -0.878, zr_ + 0.07), V(ka, -0.878, zr_ + 0.07)],
                   kk, -Y, kal=0.002)
hasir(y, 0.68, -0.76, zr_, 0.15, 0.065, 0.1, key='saz', serit='boya_kirmizi')

# the reading room on the west roof (the library's upper room)
y.bolum('Okuma odasi')
OX0, OX1, OY0, OY1 = -0.9, -0.5, -0.94, -0.66
zr = Z0 + FH - 0.03
sahel_kutu(y, dikdortgen(OX0, OX1, OY0, OY1), zr, 0.12, K, kalin=0.022, dam=zr + 0.095,
           yanlar=[dict(n=3, acik={b: dict(tip='pencere', en=0.42, v0=0.035, v1=0.09, kafes=True, kemer=0.35) for b in range(3)}),
                   dict(n=2, acik={0: dict(tip='pencere', en=0.4, v0=0.035, v1=0.09, kafes=True)}), dict(n=3),
                   dict(n=2, acik={1: dict(tip='kapi', en=0.45, v0=0, v1=0.085)})],
           kose_w=0.036, kose_tepe=0.05, toron_sira=(0.62,), kose_ust=0.02, crest=0.009)
fener(y, -0.7, -0.8, zr + 0.095, w=0.03)

# the portal: a tall mud block with fat pilasters, a studded Timbuktu door and a crown of pinnacles
y.bolum('Giris kapisi')
PX, PW, PY0, PY1, PH = 0.0, 0.34, -1.02, -0.56, 0.27
sahel_kutu(y, dikdortgen(PX - PW / 2, PX + PW / 2, PY0, PY1), Z0, PH, KT, kalin=0.03, dam=Z0 + PH - 0.03,
           yanlar=[dict(n=3, acik={1: dict(tip='kapi', en=0.72, v0=0, v1=0.19, kemer=0.32)}, payanda=False),
                   dict(n=3, acik={1: dict(tip='pencere', en=0.4, v0=0.2, v1=0.25, kafes=True)}),
                   dict(n=3, acik={1: dict(tip='kapi', en=0.72, v0=0, v1=0.17, kemer=0.32)}, payanda=False),
                   dict(n=3, acik={1: dict(tip='pencere', en=0.4, v0=0.2, v1=0.25, kafes=True)})],
           kose_w=0.07, kose_tepe=0.1, kose_yumurta=True, kose_ust=0.05, toron_sira=(0.75,))
# the great pilasters flanking the door, the window over it and the parapet pinnacles
for s in (-1, 1):
    payanda(y, V(PX + s * 0.068, PY0), X, -Y, Z0, Z0 + PH + 0.07, 0.034, 0.03, KT, 0.07, arka_z=Z0 + PH)
kutu_merkez(y, (PX, PY0 - 0.012), 0.1, 0.024, 0.032, KT, z0=Z0 + 0.205, yuzler='onsagsolust')
y.yuz_yon([V(PX - 0.05, PY0, Z0 + 0.205), V(PX + 0.05, PY0, Z0 + 0.205), V(PX + 0.05, PY0 - 0.024, Z0 + 0.205), V(PX - 0.05, PY0 - 0.024, Z0 + 0.205)], KK, -Z)
for k in range(4):
    toron(y, V(PX - 0.036 + 0.024 * k, PY0 - 0.024, Z0 + 0.222), -Y, 0.014, 0.0045)
for k in range(3):
    tepecik(y, (PX - 0.03 + 0.03 * k, PY0 + 0.012), 0.01, Z0 + PH + 0.006, 0.045, KT, n=6)
# the banner over the portal
sancak(y, PX + 0.1, PY0 + 0.24, Z0 + PH - 0.03, boy=0.26, en=0.13, yuk=0.08, aci=math.radians(200))

# ---------------- the court ----------------
y.bolum('Avlu')
akasya(y, -0.38, -0.02, Z0, boy=0.32, tohum=3)
kuyu(y, 0.34, -0.38, Z0, 0.04)
kup_(y, 0.4, -0.31, Z0, 0.012, 0.032)
kup_(y, 0.28, -0.3, Z0, 0.01, 0.028, 'kerpic_koyu')
# a teaching circle: the master on a mat under the tree, students facing him with their writing boards
hasir(y, -0.22, -0.22, Z0, 0.22, 0.2, 0.0)
oturan(y, -0.22, -0.13, Z0 + 0.003, -math.pi / 2, govde='beyaz', bas='beyaz', boy=0.062)
el_yazmasi(y, -0.18, -0.15, Z0 + 0.003, 0.2, n=3, tohum=7)
for k, (dx, dy) in enumerate(((-0.09, -0.24), (-0.03, -0.29), (0.04, -0.29), (0.1, -0.24))):
    ox, oy = -0.22 + dx, dy
    a = math.atan2(-0.13 - oy, -0.22 - ox)
    oturan(y, ox, oy, Z0 + 0.003, a, govde=('beyaz', 'boya_sari', 'kumas', 'beyaz')[k], bas=('beyaz', 'boya_kirmizi', 'beyaz', 'boya_sari')[k], boy=0.048)
    levha(y, ox + math.cos(a) * 0.016, oy + math.sin(a) * 0.016, Z0 + 0.012, a + math.pi, egim=1.15, boy=0.028)
# a second circle by the hall
hasir(y, 0.2, 0.07, Z0, 0.2, 0.16, 0.0)
oturan(y, 0.2, 0.14, Z0 + 0.003, -math.pi / 2, govde='boya_sari', bas='beyaz', boy=0.06)
el_yazmasi(y, 0.24, 0.12, Z0 + 0.003, -0.3, n=2, tohum=9)
for k, dx in enumerate((-0.06, 0.0, 0.06)):
    ox, oy = 0.2 + dx, 0.03
    a = math.atan2(0.14 - oy, 0.2 - ox)
    oturan(y, ox, oy, Z0 + 0.003, a, govde=('beyaz', 'kumas', 'beyaz')[k], bas=('beyaz', 'beyaz', 'boya_kirmizi')[k], boy=0.046)
    levha(y, ox + math.cos(a) * 0.015, oy + math.sin(a) * 0.015, Z0 + 0.012, a + math.pi, egim=1.15, boy=0.026)
# people crossing the court
kisi(y, -0.05, -0.45, Z0, math.pi / 2, govde='beyaz', bas='beyaz')
kisi(y, 0.06, -0.12, Z0, -math.pi / 2, govde='kumas', bas='beyaz', yuk='saz')
kisi(y, -0.46, -0.4, Z0, 0.3, govde='boya_sari', bas='beyaz')

# ---------------- outside ----------------
y.bolum('Dis')
baobab(y, -1.0, -1.02, Z0, boy=0.3, tohum=2)
palmiye(y, 1.03, -0.4, Z0, boy=0.3, tohum=5)
akasya(y, 1.02, 0.7, Z0, boy=0.24, tohum=8)
kisi(y, -0.12, -1.1, Z0, math.pi / 2, govde='beyaz', bas='beyaz')
kisi(y, 0.1, -1.12, Z0, math.pi / 2 + 0.4, govde='kumas', bas='boya_kirmizi', yuk='saz')
kisi(y, 0.32, -1.08, Z0, 2.4, govde='boya_sari', bas='beyaz')

calistir(y, 'lm_sankore')
