# Süleymaniye (lm_suleymaniye): central dome on a windowed drum, half domes front and back, weight turrets, cascading
# small domes, a front courtyard ringed by a domed arcade, four minarets at its corners.
# blender -b --python tools/lm-blender/suleymaniye.py -- <out.glb> [preview.png]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector
from ortak import Yapi, temizle, disa_aktar, onizle, argumanlar

TAS = (0.86, 0.82, 0.74)
TAS_ACIK = (0.93, 0.90, 0.84)
TAS_KOYU = (0.68, 0.63, 0.55)
KURSUN = (0.60, 0.65, 0.72)        # lead domes and caps (dull blue-grey: not the team blue)
DELIK = (0.20, 0.18, 0.17)
ALTIN = (0.86, 0.68, 0.30)
AVLU = (0.80, 0.77, 0.70)
TABAN = (0.80, 0.77, 0.70)
MAVI = (0.12, 0.33, 0.86)
DIREK = (0.36, 0.26, 0.17)
KEMER = (TAS, TAS_KOYU, TAS_ACIK, DELIK)

y = Yapi(tohum=11)
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))

# ---- platform ----
Z0 = 0.04
y.kutu((-0.7, -1.1, 0), X, Y, 1.4, 2.42, Z0, TABAN)


def blok(x0, x1, y0, y1, z0, h, renk=TAS, yuzler='onarkasagsolust', cati=TAS_ACIK):
    y.kutu((x0, y0, z0), X, Y, x1 - x0, y1 - y0, h, renk, yuzler.replace('ust', ''))
    if 'ust' in yuzler: y.kutu((x0, y0, z0), X, Y, x1 - x0, y1 - y0, h, cati, 'ust')


def pencereler(x0, x1, y0, y1, z, h, n, w, yanlar='onsagsolarka'):
    """a row of n round-headed windows on the walls of a box"""
    for yan, o, ex, nn, L in (('on', (x0, y0, 0), X, -Y, x1 - x0), ('arka', (x0, y1, 0), X, Y, x1 - x0),
                               ('sol', (x0, y0, 0), Y, -X, y1 - y0), ('sag', (x1, y0, 0), Y, X, y1 - y0)):
        if yan not in yanlar: continue
        for i in range(n):
            u = L * (i + 0.5) / n - w / 2
            y.pencere(Vector(o) + Z * z, ex, nn, u, 0, w, h, DELIK)


def kucuk_kubbe(cx, cy, z, r, h=None, finial=True, n=12):
    tepe = y.kubbe((cx, cy), r, z, h or r * 0.85, KURSUN, n=n, kat=3)
    if finial:
        y.prizma((cx, cy), 0.006, tepe.z, tepe.z + r * 0.45, ALTIN, n=4)


# ---- prayer hall ----
HX, HY0, HY1, HH = 0.6, 0.05, 1.25, 0.34
CY = (HY0 + HY1) / 2
blok(-HX, HX, HY0, HY1, Z0, HH)
pencereler(-HX, HX, HY0, HY1, Z0 + 0.05, 0.08, 7, 0.06)
pencereler(-HX, HX, HY0, HY1, Z0 + 0.18, 0.09, 7, 0.06)
# side gallery domes along both long sides
for sx in (-1, 1):
    for k in range(5):
        kucuk_kubbe(sx * 0.5, HY0 + 0.15 + k * 0.225, Z0 + HH, 0.07)
# upper block under the dome (tympanum walls)
U = 0.42
blok(-U, U, CY - U, CY + U, Z0 + HH, 0.18)
pencereler(-U, U, CY - U, CY + U, Z0 + HH + 0.04, 0.10, 5, 0.06, 'sagsol')
# cascading: small domes beside the half domes, low on the hall roof
for sx in (-1, 1):
    for sy in (-1, 1):
        kucuk_kubbe(sx * 0.25, CY + sy * 0.47, Z0 + HH, 0.1)
# half domes front and back
ZH = Z0 + HH + 0.05
y.kubbe((0, CY - 0.33), 0.27, ZH, 0.18, KURSUN, n=12, kat=4, t0=math.pi, t1=2 * math.pi, kapak=TAS)
y.kubbe((0, CY + 0.33), 0.27, ZH, 0.18, KURSUN, n=12, kat=4, t0=0, t1=math.pi, kapak=TAS)
# weight turrets at the corners of the dome square
for sx in (-1, 1):
    for sy in (-1, 1):
        c = (sx * U, CY + sy * U)
        y.prizma(c, 0.06, Z0 + HH, Z0 + 0.66, TAS_ACIK, n=8, ust=False, kat=math.pi / 8)
        kucuk_kubbe(c[0], c[1], Z0 + 0.66, 0.062, n=8)
# drum with windows, then the great dome
ZD = Z0 + 0.52
ring = y.prizma((0, CY), 0.36, ZD, ZD + 0.11, TAS_ACIK, n=20, ust=False)
for i in range(20):
    a, b = ring(ZD)[i], ring(ZD)[(i + 1) % 20]
    m = (a + b) / 2; nn = Vector((m.x, m.y - CY, 0)).normalized()
    y.pencere(a, (b - a).normalized(), nn, (b - a).length * 0.3, 0.02, (b - a).length * 0.4, 0.07, DELIK, k_say=3)
tepe = y.kubbe((0, CY), 0.37, ZD + 0.11, 0.33, KURSUN, n=20, kat=6)
y.prizma((0, CY), 0.009, tepe.z, tepe.z + 0.06, ALTIN, n=4)
y.kubbe((0, CY), 0.018, tepe.z + 0.06, 0.025, ALTIN, n=6, kat=2)

# ---- courtyard ----
AX, AY0, AY1, AH = 0.6, -1.0, HY0, 0.2
IX, IY0, IY1 = 0.44, -0.84, -0.11        # the open court
blok(-AX, AX, AY0, AY1, Z0, AH, yuzler='onsagsol')
pencereler(-AX, AX, AY0, AY1, Z0 + 0.05, 0.09, 6, 0.06, 'onsagsol')
# arcade roof (a ring around the court)
zr = Z0 + AH
for q in ([(-AX, AY0), (AX, AY0), (IX, IY0), (-IX, IY0)], [(AX, AY0), (AX, AY1), (IX, IY1), (IX, IY0)],
          [(AX, AY1), (-AX, AY1), (-IX, IY1), (IX, IY1)], [(-AX, AY1), (-AX, AY0), (-IX, IY0), (-IX, IY1)]):
    y.yuz_yon([Vector((p[0], p[1], zr)) for p in q], TAS_ACIK, Z)
# arches facing the court
def arkad(a, b, n):
    a, b = Vector(a), Vector(b)
    for i in range(n):
        y.kemerli(a.lerp(b, i / n) + Z * Z0, a.lerp(b, (i + 1) / n) + Z * Z0, 0, AH, KEMER, en=0.7, ust=0.03, derin=0.05, k_say=5)
arkad((IX, IY0, 0), (-IX, IY0, 0), 5)
arkad((-IX, IY1, 0), (IX, IY1, 0), 5)
arkad((-IX, IY0, 0), (-IX, IY1, 0), 4)
arkad((IX, IY1, 0), (IX, IY0, 0), 4)
# court floor and the fountain
y.yuz([Vector((-IX, IY0, Z0 + 0.002)), Vector((IX, IY0, Z0 + 0.002)), Vector((IX, IY1, Z0 + 0.002)), Vector((-IX, IY1, Z0 + 0.002))], AVLU)
FY = (IY0 + IY1) / 2
y.prizma((0, FY), 0.07, Z0, Z0 + 0.06, TAS_ACIK, n=8, kat=math.pi / 8)
kucuk_kubbe(0, FY, Z0 + 0.06, 0.07, n=8)
# arcade domes
mx, my0, my1 = 0.52, -0.92, -0.03
for k in range(6):
    xx = -mx + 2 * mx * k / 5
    kucuk_kubbe(xx, my0, zr, 0.065, finial=False, n=10)
    kucuk_kubbe(xx, my1, zr, 0.065, finial=False, n=10)
for k in range(1, 4):
    yy = my0 + (my1 - my0) * k / 4
    for sx in (-1, 1):
        kucuk_kubbe(sx * mx, yy, zr, 0.065, finial=False, n=10)
# entrance portal on the front
blok(-0.12, 0.12, AY0 - 0.04, AY0 + 0.04, Z0, 0.29)
y.pencere((-0.12, AY0 - 0.04, Z0), X, -Y, 0.06, 0.0, 0.12, 0.2, DELIK, k_say=5)
kucuk_kubbe(0, AY0, Z0 + 0.29, 0.07, n=10)

# ---- minarets at the courtyard corners: two tall (three balconies) at the back, two shorter (two) at the front ----
def minare(cx, cy, boy, serefe):
    y.prizma((cx, cy), 0.06, Z0, Z0 + 0.24, TAS_ACIK, n=4, kat=math.pi / 4)
    y.prizma((cx, cy), 0.032, Z0 + 0.24, Z0 + boy, TAS_ACIK, n=12, ust=False)
    for k in range(serefe):
        zz = Z0 + 0.24 + (boy - 0.3) * (k + 1) / (serefe + 0.4)
        y.prizma((cx, cy), 0.05, zz, zz + 0.016, TAS, n=12, ust_renk=TAS_ACIK)
        y.prizma((cx, cy), 0.042, zz - 0.02, zz, TAS_KOYU, n=12, ust=False)
    y.koni((cx, cy), 0.036, Z0 + boy, 0.17, KURSUN, n=12)
    y.prizma((cx, cy), 0.004, Z0 + boy + 0.17, Z0 + boy + 0.21, ALTIN, n=4)

for sx in (-1, 1):
    minare(sx * AX, AY1, 1.15, 3)
    minare(sx * AX, AY0, 0.9, 2)

# ---- blue banner on the portal ----
y.silindir((0.09, AY0 - 0.02), 0.007, Z0 + 0.29, Z0 + 0.46, DIREK)
y.kutu((0.096, AY0 - 0.022, Z0 + 0.39), X, Y, 0.09, 0.004, 0.06, MAVI)

print('UCGEN', y.ucgen_sayisi())

if __name__ == '__main__':
    arg = argumanlar()
    temizle()
    ob = y.nesne('lm_suleymaniye')
    if arg:
        disa_aktar(ob, os.path.abspath(arg[0]))
    if len(arg) > 1:
        onizle(os.path.abspath(arg[1]), merkez=(0, 0.05, 0.4), boy=3.2, aci=(-35, 32))
