# Palace of Mansa Musa (lm_mansasaray): a mud palace in the Sudano-Sahelian manner - a tall three-storey tower house
# and a long two-storey wing behind, the domed audience hall built by as-Sahili in front of them (plastered, windows
# framed in gold, silk curtains), and a walled court with round bastions and a gatehouse; in the court the Mansa sits
# on an ivory throne on a stepped dais under a golden parasol, guards with golden lances line the red carpet, horses
# in caparisons stand by the stable and camels bring the tribute of gold.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mali_ek import *
from arap_ortak import deve

y = Yapi()
rn = random.Random(4)
Z0 = 0.035
CX0, CX1, CY0, CY1 = -0.98, 0.98, -0.98, 0.55      # the court
BY1, BH = 1.0, 0.25                                 # the back wing
FIL = 'siva_krem'                                   # ivory

y.bolum('Zemin')
zemin(y, -1.13, 1.13, -1.17, 1.13, Z0, KK, 'kum_acik', basamak=(('on', 0.42),), silmeli=True)

# ---------------- the back wing (two storeys) ----------------
y.bolum('Arka kanat')
on = {}
for b in range(14):
    if 5 <= b <= 8: continue    # (behind the audience hall)
    on[b] = [dict(tip='pencere', en=0.4, v0=0.04, v1=0.1, kafes=True, kemer=0.3), dict(tip='pencere', en=0.38, v0=0.15, v1=0.2, kafes=True,
             arka='boya_kirmizi' if b % 3 == 0 else 'koyu')]
on[2] = [dict(tip='kapi', en=0.5, v0=0, v1=0.12, kemer=0.3), dict(tip='pencere', en=0.38, v0=0.15, v1=0.2, kafes=True)]
on[11] = [dict(tip='kapi', en=0.5, v0=0, v1=0.12, kemer=0.3), dict(tip='pencere', en=0.38, v0=0.15, v1=0.2, kafes=True, arka='boya_kirmizi')]
yan_kanat = [dict(n=14, acik=on),
             dict(n=3, acik={1: [dict(tip='pencere', en=0.36, v0=0.05, v1=0.1, kafes=True), dict(tip='pencere', en=0.36, v0=0.15, v1=0.2, kafes=True)]}),
             dict(n=12),
             dict(n=3, acik={b: [dict(tip='pencere', en=0.36, v0=0.05, v1=0.1, kafes=True), dict(tip='pencere', en=0.36, v0=0.15, v1=0.2, kafes=True)] for b in (0, 2)})]
sahel_kutu(y, dikdortgen(CX0, CX1, CY1, BY1), Z0, BH, K, kalin=0.03, dam=Z0 + BH - 0.03, yanlar=yan_kanat, payanda_ara=0.14,
           kose_w=0.06, kose_tepe=0.08, toron_sira=(0.3, 0.72), kademe=True)
silme(y, [V(CX0 + 0.04, CY1), V(-0.28, CY1)], Z0 + BH * 0.5, 0.012, 0.007, K, 'duz', kapali=False)
silme(y, [V(0.28, CY1), V(CX1 - 0.04, CY1)], Z0 + BH * 0.5, 0.012, 0.007, K, 'duz', kapali=False)
for gx in (-0.8, -0.35, 0.05, 0.3):
    fener(y, gx, 0.88, Z0 + BH - 0.03, w=0.036)
for gx in (-0.75, 0.75):
    oluk(y, V(gx, BY1), V(0, 1), Z0 + BH - 0.02, 0.04)

# ---------------- the great tower house (right) and the lesser tower (left) ----------------
y.bolum('Saray kulesi')


def kule_ev(cx, cy, katlar, z, sancakli=False):
    """a stack of shrinking mud storeys, each with windows on every side (some with curtains), pilasters and pinnacles"""
    for k, (w, h) in enumerate(katlar):
        kose = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
        nb = 3
        def pen(perde):
            return dict(tip='pencere', en=0.42, v0=h * 0.38, v1=h * 0.72, kafes=True, kemer=0.35, arka='boya_kirmizi' if perde else 'koyu')
        yan = [dict(n=nb, acik={0: pen(False), 1: pen(True), 2: pen(False)}), dict(n=nb, acik={1: pen(k % 2 == 0)}),
               dict(n=nb, acik={1: pen(False)}), dict(n=nb, acik={0: pen(False), 2: pen(True)})]
        son = k == len(katlar) - 1
        sahel_kutu(y, kose, z, h, K if k % 2 == 0 else KT, kalin=0.026, dam=z + h - 0.026, yanlar=yan, payanda_ara=w / nb,
                   kose_w=0.05 + 0.012 * (len(katlar) - k), kose_tepe=0.07 if not son else 0.11, kose_yumurta=True,
                   toron_sira=(0.22, 0.88), kose_ust=0.03 if not son else 0.06, payanda_tepe=0.045 if not son else 0.07)
        z = z + h - 0.026
    return z


zt = kule_ev(0.6, 0.77, [(0.46, 0.34), (0.36, 0.3), (0.26, 0.27)], Z0)
# the crown: a lantern box with a gold finial
kutu_merkez(y, (0.6, 0.77), 0.09, 0.09, 0.06, K, z0=zt)
y.yuz_yon(dikdortgen(0.555, 0.645, 0.725, 0.815, zt + 0.06), K, Z)
tepecik(y, (0.6, 0.77), 0.035, zt + 0.06, 0.09, K, n=10)
kure(y, (0.6, 0.77, zt + 0.165), 0.016, 'altin', n=10, kat=5)
sancak(y, 0.53, 0.7, zt, boy=0.24, en=0.13, yuk=0.08, aci=math.radians(200))
kule_ev(-0.62, 0.79, [(0.36, 0.3), (0.27, 0.26)], Z0)

# ---------------- the domed audience hall ----------------
y.bolum('Kabul salonu')
AX, AY, AW, AD, AH = 0.0, 0.3, 0.52, 0.46, 0.27
SV = 'siva_oker'
ak = dikdortgen(AX - AW / 2, AX + AW / 2, AY - AD / 2, AY + AD / 2)
renk = (SV, KK, SV, 'boya_kirmizi')
silme(y, ak, Z0, 0.03, 0.012, KK, 'kaide')
# the front: three tall arched openings hung with silk, framed in gold; the sides: two each
pencereli_duvar(y, ak, Z0 + 0.03, AH - 0.03, [3, 2, 0, 2], renk=renk, v0=0.012, en=0.5, ust=0.04, derin=0.03, k_say=8, sivri=0.38,
                cerceve=(0.009, ['altin', 'boya_sari']))
y.yuz_yon(dikdortgen(AX - AW / 2, AX + AW / 2, AY - AD / 2, AY + AD / 2, Z0 + AH), SV, Z)
# painted bands (arabesque friezes) and the cornice
for zz, kk in ((Z0 + AH - 0.028, 'boya_kirmizi'), (Z0 + AH - 0.016, 'boya_sari')):
    silme(y, ak, zz, 0.008, 0.003, kk, 'duz')
kornis(y, AX - AW / 2, AX + AW / 2, AY - AD / 2, AY + AD / 2, Z0 + AH - 0.004, 0.016, 0.014, SV, 'tac')
# the parapet with pinnacles at the corners and along the edge
for i in range(4):
    p = ak[i]
    kose_payanda(y, (p.x, p.y), Z0, Z0 + AH + 0.05, 0.06, SV, 0.09, yumurta=False)
    kure(y, (p.x, p.y, Z0 + AH + 0.05 + 0.093), 0.011, 'altin', n=8, kat=4)
for i in range(4):
    a, b = ak[i], ak[(i + 1) % 4]
    for t in (0.25, 0.5, 0.75):
        pp = a.lerp(b, t)
        tepecik(y, (pp.x + (pp.x - AX) * 0.0, pp.y), 0.012, Z0 + AH + 0.012, 0.045, SV, n=6)
# the drum and the dome
zd = kubbe_kasnakli(y, (AX, AY), 0.16, Z0 + AH + 0.012, 0.07, n_pencere=12, kubbe_h=0.17, key='siva_krem',
                    duvar=('siva_krem', KK, 'siva_krem', 'koyu'), payanda=True, alem_olcek=0, sivri=0.4, n=36, kat=10,
                    cerceve=(0.005, 'altin'))
donel(y, (AX, AY), [(0.03, zd - 0.01), (0.026, zd + 0.006), (0.0, zd + 0.01)], 'siva_krem', n=10)
kure(y, (AX, AY, zd + 0.03), 0.022, 'altin', n=12, kat=6)
donel(y, (AX, AY), [(0.0, zd + 0.048), (0.006, zd + 0.05), (0.0, zd + 0.085)], 'altin', n=6)
# the steps up to the door
for k in range(3):
    kutu_merkez(y, (AX, AY - AD / 2 - 0.015 - 0.016 * k), 0.24 - 0.02 * k, 0.03 + 0.032 * k, 0.03 - 0.009 * k, KK, z0=Z0)

# ---------------- the court walls, bastions and gatehouse ----------------
y.bolum('Avlu suru')
# (one wide gate in the middle bay: two gates side by side left a pilaster standing in their openings, hollow from behind)
yan_avlu = [dict(n=11, acik={5: dict(tip='gecit', en=0.8, v0=0.0015, v1=0.17, kemer=0.3)}, kose=False),
            dict(n=10, kose=False), dict(yok=True, kose=False), dict(n=10, kose=False)]
sahel_kutu(y, dikdortgen(CX0, CX1, CY0, CY1), Z0, 0.2, K, kalin=0.035, dam=None, yanlar=yan_avlu, payanda_ara=0.16,
           kose_w=0.06, kose_tepe=0.07, ic_payanda=True, toron_sira=(0.5,))
for sx in (CX0, CX1):
    burc(y, (sx, CY0), 0.13, Z0, 0.27, K, egim=0.12, n=18, dis_aci=math.atan2(-1, sx))
    sancak(y, sx * 0.995, CY0 + 0.02, Z0 + 0.3, boy=0.14, en=0.08, yuk=0.05, aci=math.radians(200)) if sx < 0 else None
# the gatehouse over the double gate: two fat towers and a bridge storey
for sx in (-1, 1):
    kose_payanda(y, (sx * 0.2, CY0), Z0, Z0 + 0.36, 0.11, K, 0.11, yumurta=True)
    for zz in (0.18, 0.28):
        for k in range(3):
            toron(y, V(sx * 0.2 - 0.03 + 0.03 * k, CY0 - 0.055 + 0.004 * zz, Z0 + zz), -Y, 0.02)
kutu_merkez(y, (0.0, CY0), 0.3, 0.07, 0.1, K, z0=Z0 + 0.2)
for k in range(5):
    tepecik(y, (-0.1 + 0.05 * k, CY0 - 0.02), 0.012, Z0 + 0.3, 0.05, K, n=6)
for k in range(3):
    xk = -0.07 + 0.07 * k
    kutu_merkez(y, (xk, CY0 - 0.0355), 0.03, 0.002, 0.045, 'koyu', z0=Z0 + 0.235)
    kafes(y, V(xk - 0.015, CY0 - 0.0365), V(xk + 0.015, CY0 - 0.0365), Z0 + 0.235, 0, 1, 0, 0.045, key='ahsap_koyu', nu=3, nv=3, en=0.003, ileri=0.0015)
kutu_merkez(y, (0.0, CY0 - 0.045), 0.32, 0.02, 0.012, KK, z0=Z0 + 0.2)

# ---------------- the court: the dais, throne and parasol ----------------
y.bolum('Taht')
DX, DY = 0.0, -0.22
# the red carpet from the gate
kutu_merkez(y, (0, (CY0 + DY) / 2 - 0.08), 0.1, (DY - CY0) - 0.2, 0.002, 'boya_kirmizi', z0=Z0)
for s in (-1, 1):
    kutu_merkez(y, (s * 0.046, (CY0 + DY) / 2 - 0.08), 0.008, (DY - CY0) - 0.2, 0.0022, 'boya_sari', z0=Z0)
# the pempi: a three-stepped platform
for k in range(3):
    kutu_merkez(y, (DX, DY + 0.012 * k), 0.4 - 0.05 * k, 0.3 - 0.04 * k, 0.022 * (k + 1), KK if k < 2 else K, z0=Z0)
zp = Z0 + 0.066
kutu_merkez(y, (DX, DY + 0.04), 0.2, 0.14, 0.002, 'boya_kirmizi', z0=zp)
kutu_merkez(y, (DX, DY + 0.04), 0.17, 0.11, 0.0024, 'boya_sari', z0=zp)
# the ivory throne: a seat with a high back, tusks arching over it
kutu_merkez(y, (DX, DY + 0.06), 0.08, 0.06, 0.028, FIL, z0=zp)
kutu_merkez(y, (DX, DY + 0.094), 0.09, 0.014, 0.09, FIL, z0=zp)
kutu_merkez(y, (DX, DY + 0.06), 0.072, 0.054, 0.004, 'boya_kirmizi', z0=zp + 0.028)
for s in (-1, 1):
    kutu_merkez(y, (DX + s * 0.042, DY + 0.06), 0.012, 0.06, 0.05, FIL, z0=zp)
    boru(y, [V(DX + s * 0.06, DY + 0.1, zp), V(DX + s * 0.075, DY + 0.09, zp + 0.06), V(DX + s * 0.06, DY + 0.07, zp + 0.11),
             V(DX + s * 0.025, DY + 0.06, zp + 0.13)], 0.009, FIL, n=7, r_son=0.002)
kure(y, (DX, DY + 0.094, zp + 0.098), 0.012, 'altin', n=8, kat=4)
# the Mansa in red with a golden cap
oturan(y, DX, DY + 0.055, zp + 0.028, -math.pi / 2, govde='boya_kirmizi', bas='altin', boy=0.07)
# the golden parasol with a bird on top
semsiye(y, DX - 0.02, DY + 0.12, zp, boy=0.2, r=0.1, key='altin', sacak_key='boya_kirmizi')
# attendants: griots with drums, a herald, an umbrella-bearer
for s in (-1, 1):
    kisi(y, DX + s * 0.13, DY + 0.06, zp - 0.022, -math.pi / 2 + s * 0.4, govde='beyaz', bas='boya_kirmizi' if s < 0 else 'beyaz', boy=0.058)
    donel(y, (DX + s * 0.17, DY - 0.03), [(0.0, Z0 + 0.022), (0.014, Z0 + 0.022), (0.017, Z0 + 0.04), (0.013, Z0 + 0.055), (0.0, Z0 + 0.055)], 'ahsap', n=10)
    donel(y, (DX + s * 0.17, DY - 0.03), [(0.0135, Z0 + 0.055), (0.0, Z0 + 0.0555)], 'kum_acik', n=10)
# chests of gold before the throne (the tribute)
for k, sx in enumerate((-0.09, 0.09)):
    kutu_merkez(y, (DX + sx, DY - 0.2), 0.06, 0.04, 0.028, 'ahsap_koyu', z0=Z0)
    donel(y, (DX + sx, DY - 0.2), [(0.026, Z0 + 0.028), (0.016, Z0 + 0.04), (0.0, Z0 + 0.044)], 'altin', n=10)
    kutu_merkez(y, (DX + sx, DY - 0.2 + 0.024), 0.064, 0.008, 0.04, 'ahsap_koyu', z0=Z0 + 0.024)
mal_koy(y, 'altin', DX, DY - 0.26, Z0)

# guards with golden lances lining the carpet
y.bolum('Muhafizlar')
for k in range(5):
    gy = CY0 + 0.2 + 0.11 * k
    for s in (-1, 1):
        kisi(y, s * 0.13, gy, Z0, math.pi if s > 0 else 0.0, govde='beyaz' if k % 2 == 0 else 'boya_kirmizi', bas='beyaz', mizrak='altin',
             kalkan='boya_sari' if k % 2 == 0 else 'boya_kirmizi', boy=0.06)

# ---------------- horses and the stable (west), camels and tribute (east) ----------------
y.bolum('Atlar')
ZEMIN_Z[0] = Z0
sundurma(y, V(CX0 + 0.035, -0.74), V(CX0 + 0.035, 0.08), Z0 + 0.18, Z0 + 0.13, 0.17, n_direk=4)
for k, (hx, hy, a, cu, c2) in enumerate(((-0.64, -0.6, 0.2, 'boya_kirmizi', 'boya_sari'), (-0.62, -0.34, 0.1, 'kobalt', 'beyaz'),
                                          (-0.64, -0.08, -0.1, 'boya_sari', 'boya_kirmizi'))):
    mali_at(y, hx, hy, Z0, a, renk=('ahsap', 'beyaz', 'ahsap_koyu')[k], cul=cu, cul2=c2, s=1.25)
yalak(y, V(-0.91, -0.7), V(-0.91, -0.45), Z0, en=0.035, h=0.02, ic='su')
saman(y, -0.9, -0.2, Z0, r=0.04, h=0.05)
mali_at(y, -0.45, -0.72, Z0, 0.6, renk='beyaz', cul='boya_kirmizi', cul2='altin', binici=('boya_kirmizi', 'beyaz', 'altin', 'boya_sari'), s=1.25)
kisi(y, -0.45, -0.62, Z0, -0.4, govde='beyaz', bas='beyaz')

y.bolum('Develer')
# the treasury stores along the east wall: a row of mud rooms with studded doors opening on the court
sahel_kutu(y, dikdortgen(0.68, CX1 - 0.04, -0.76, 0.32), Z0, 0.165, K, kalin=0.026, dam=Z0 + 0.14,
           yanlar=[dict(n=2, acik={0: dict(tip='pencere', en=0.4, v0=0.08, v1=0.12, kafes=True)}), dict(n=6, payanda=False, toron=False),
                   dict(n=2), dict(n=6, acik={b: dict(tip='kapi', en=0.5, v0=0, v1=0.11, kemer=0.3) for b in (0, 2, 4)} |
                                         {b: dict(tip='pencere', en=0.34, v0=0.07, v1=0.115, kafes=True) for b in (1, 3, 5)})],
           kose_w=0.05, kose_tepe=0.06, toron_sira=(0.7,))
for yy in (-0.55, -0.2, 0.15):
    fener(y, 0.81, yy, Z0 + 0.14, w=0.032)
deve(y, 0.5, -0.66, Z0, math.pi * 0.75, renk='ahsap_acik', yuk=True, olcek=1.0)
deve(y, 0.56, -0.36, Z0, math.pi * 0.9, renk='kum_koyu', yuk=True, olcek=1.0)
deve(y, 0.55, -0.04, Z0, math.pi, renk='ahsap_acik', yuk=False, cok=True, olcek=1.0)
tuareg(y, 0.4, -0.56, Z0, math.pi * 0.8)
kisi(y, 0.62, -0.2, Z0, math.pi, govde='lacivert', bas='beyaz', yuk='saz')
for k, (tx, ty) in enumerate(((0.36, -0.3), (0.36, -0.16), (0.42, -0.1))):
    kutu_merkez(y, (tx, ty), 0.05, 0.036, 0.026, 'ahsap_koyu', z0=Z0, aci=0.2 * k)
    donel(y, (tx, ty), [(0.02, Z0 + 0.026), (0.013, Z0 + 0.036), (0.0, Z0 + 0.04)], 'altin', n=10)
tuz_levha(y, 0.3, -0.48, Z0, 0.4, n=4, tohum=3)
kup_(y, 0.26, 0.0, Z0, 0.016, 0.042)
# a tree in the court
akasya(y, -0.42, 0.2, Z0, boy=0.28, tohum=5)
agac(y, 0.4, 0.3, Z0, boy=0.16)

# ---------------- outside ----------------
y.bolum('Dis')
palmiye(y, -1.07, 0.32, Z0, boy=0.28, tohum=1)
palmiye(y, -1.06, -0.45, Z0, boy=0.24, tohum=6)
akasya(y, 1.06, 0.25, Z0, boy=0.2, tohum=9)
for k in range(3):
    kisi(y, -0.3 + 0.24 * k, -1.08, Z0, math.pi / 2 + rn.uniform(-0.5, 0.5), govde=rn.choice(('beyaz', 'boya_sari', 'kumas')), bas='beyaz',
         yuk='saz' if k == 1 else None)

calistir(y, 'lm_mansasaray')
