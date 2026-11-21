# Süleymaniye (lm_suleymaniye), textured and smooth-shaded (doku.py): prayer hall with two storeys of pointed
# windows, an upper block under the dome, a 28-window drum with buttresses and the great dome, half domes on windowed
# half drums, weight turrets, cascading small domes, a courtyard with a columned pointed arcade and a domed bay each,
# a şadırvan kiosk, the portal and four minarets with corbelled balconies.
# blender -b --python tools/lm-blender/suleymaniye.py -- <out.glb> [preview.png]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector
from ortak import Yapi, temizle, argumanlar
from doku import nesne_dokulu, detayli_aktar, onizle_dokulu

y = Yapi()
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
PENCERE = ('tas', 'tas_koyu', 'tas_acik', 'cam')
REVAK = ('tas', 'tas', 'tas_acik', 'tas_koyu')


def V(x, yy, z=0.0):
    return Vector((x, yy, z))


def korniş(x0, x1, y0, y1, z, h, c, key='tas_acik'):
    """a moulding round a rectangle (corners CCW): underside, face, top"""
    def r(o, zz):
        return [V(x0 - o, y0 - o, zz), V(x1 + o, y0 - o, zz), V(x1 + o, y1 + o, zz), V(x0 - o, y1 + o, zz)]
    y.serit(r(0, z), r(c, z), key)
    y.serit(r(c, z), r(c, z + h), key)
    y.serit(r(c, z + h), r(0, z + h), key)


def halka_korniş(c, r, z, h, c2, n, key='tas_acik', kat=0.0):
    def ring(rr, zz):
        return [V(c[0] + rr * math.cos(kat + 2 * math.pi * i / n), c[1] + rr * math.sin(kat + 2 * math.pi * i / n), zz) for i in range(n)]
    y.serit(ring(r, z), ring(r + c2, z), key)
    y.serit(ring(r + c2, z), ring(r + c2, z + h), key)
    y.serit(ring(r + c2, z + h), ring(r, z + h), key)


def pencereli_duvar(kose, z0, H, sayilar, **kw):
    """walls round a CCW polygon (corners kose), each side split into its count of window bays"""
    for i, n in enumerate(sayilar):
        a, b = kose[i], kose[(i + 1) % len(kose)]
        for k in range(n):
            y.kemerli(a.lerp(b, k / n), a.lerp(b, (k + 1) / n), z0, H, kw.get('renk', PENCERE),
                      v0=kw.get('v0', 0.03), en=kw.get('en', 0.45), ust=kw.get('ust', 0.03), derin=kw.get('derin', 0.025),
                      k_say=kw.get('k_say', 6), sivri=kw.get('sivri', 0.6), cerceve=kw.get('cerceve', (0.008, 'mermer')))


def duz_duvar(a, b, z0, z1, key='tas'):
    """a plain wall quad from a to b facing the right of a->b"""
    e = (b - a).normalized()
    y.yuz_yon([a + Z * z0, b + Z * z0, b + Z * z1, a + Z * z1], key, V(e.y, -e.x))


def sutun(cx, cy, z0, z1, r=0.015, key='mermer'):
    y.prizma((cx, cy), r, z0 + 0.012, z1 - 0.014, key, n=10, ust=False)
    y.kutu(V(cx - r * 1.45, cy - r * 1.45, z0), X, Y, r * 2.9, r * 2.9, 0.012, key, 'onarkasagsolust')
    y.kutu(V(cx - r * 1.45, cy - r * 1.45, z1 - 0.016), X, Y, r * 2.9, r * 2.9, 0.016, key, 'onarkasagsolust')


def kemer_hs(H, ust, sivri, en, W):
    return H - ust - sivri * en * W


def arkad(a, b, n, z0, H, en=0.8, ust=0.03, sivri=0.5, derin=0.1, korkuluk=None, cerceve=(0.011, ['mermer', 'kirmizi']), son_sutun=True):
    """an open arcade from a to b (facing the right of a->b): pointed arches on columns, striped voussoirs"""
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        W = (q - p).length
        y.kemerli(p + Z * z0, q + Z * z0, 0, H, REVAK, en=en, ust=ust, derin=derin, k_say=10, sivri=sivri, korkuluk=korkuluk, cerceve=cerceve)
        hs = kemer_hs(H, ust, sivri, en, W)
        e = (q - p).normalized(); nc = V(e.y, -e.x)
        for u in ([0.0, 1.0] if (i == n - 1 and son_sutun) else [0.0]):
            cc = p.lerp(q, u) + nc * 0.016
            sutun(cc.x, cc.y, z0, z0 + hs)


def dikdortgen(x0, x1, y0, y1):
    return [V(x0, y0), V(x1, y0), V(x1, y1), V(x0, y1)]


def cokgen(c, r, n, kat=0.0):
    return [V(c[0] + r * math.cos(kat + 2 * math.pi * i / n), c[1] + r * math.sin(kat + 2 * math.pi * i / n)) for i in range(n)]


def alem(cx, cy, z, olcek=1.0):
    s = olcek
    y.prizma((cx, cy), 0.005 * s, z, z + 0.03 * s, 'altin', n=6)
    y.kubbe((cx, cy), 0.012 * s, z + 0.03 * s, 0.012 * s, 'altin', n=8, kat=3)
    y.prizma((cx, cy), 0.003 * s, z + 0.04 * s, z + 0.07 * s, 'altin', n=4)


def kucuk_kubbe(cx, cy, z, r, kasnak=0.025, n=28, son=True):
    y.prizma((cx, cy), r * 1.02, z, z + kasnak, 'tas', n=28, ust=False)
    halka_korniş((cx, cy), r * 1.02, z + kasnak - 0.006, 0.006, 0.006, 28)
    t = y.kubbe((cx, cy), r, z + kasnak, r * 0.9, 'kursun', n=n, kat=8)
    if son: alem(cx, cy, t.z, 0.7)


ODAK = (0, 0.1, 0.35)          # (the live view looks here)

# ---------------- platform ----------------
y.bolum('Zemin ve basamaklar')
Z0 = 0.05
y.kutu((-0.74, -1.16, 0), X, Y, 1.48, 2.52, Z0, 'tas_koyu')
for k in range(3):
    y.kutu((-0.2, -1.16 - 0.03 * (k + 1), 0), X, Y, 0.4, 0.03, Z0 * (3 - k) / 4, 'tas_koyu', 'onsagsolust')
y.yuz([V(-0.74, -1.16, Z0 + 0.001), V(0.74, -1.16, Z0 + 0.001), V(0.74, 1.36, Z0 + 0.001), V(-0.74, 1.36, Z0 + 0.001)], 'zemin')

# ---------------- prayer hall ----------------
y.bolum('Harim duvarları ve çerçeveli pencereler')
HX, HY0, HY1 = 0.6, 0.05, 1.25
CY = (HY0 + HY1) / 2
H1, H2 = 0.17, 0.15
ZR = Z0 + H1 + H2           # hall roof
hall = dikdortgen(-HX, HX, HY0, HY1)
pencereli_duvar(hall, Z0, H1, [7, 7, 7, 7], en=0.4, v0=0.04, ust=0.035, sivri=0.5)
pencereli_duvar(hall, Z0 + H1, H2, [7, 7, 7, 7], en=0.38, v0=0.03, ust=0.03, sivri=0.65)
korniş(-HX, HX, HY0, HY1, Z0, 0.025, 0.012, 'tas_koyu')
korniş(-HX, HX, HY0, HY1, Z0 + H1 - 0.004, 0.008, 0.008)
korniş(-HX, HX, HY0, HY1, ZR - 0.012, 0.014, 0.014)
y.yuz([V(-HX, HY0, ZR + 0.002), V(HX, HY0, ZR + 0.002), V(HX, HY1, ZR + 0.002), V(-HX, HY1, ZR + 0.002)], 'kursun')
for sx in (-1, 1):            # corner buttresses
    for yy in (HY0, HY1):
        y.kutu((sx * HX - 0.025, yy - 0.025, Z0), X, Y, 0.05, 0.05, ZR - Z0 + 0.03, 'tas', 'onarkasagsolust')
# two-storey arcaded galleries along both long sides (columns, striped arches, a balustrade upstairs)
y.bolum('Yan revaklar (iki katlı sütunlu galeriler)')
G, GM, GH1, GH2 = 0.11, 0.1, 0.16, 0.13
ZG = Z0 + GH1 + GH2
for sx in (-1, 1):
    xo = sx * (HX + G)
    a, b = (V(xo, HY0 + GM), V(xo, HY1 - GM)) if sx > 0 else (V(xo, HY1 - GM), V(xo, HY0 + GM))
    arkad(a, b, 6, Z0, GH1, derin=G - 0.005)
    arkad(a, b, 6, Z0 + GH1, GH2, en=0.76, derin=G - 0.005, korkuluk=0.035, cerceve=(0.009, ['mermer', 'kirmizi']))
    xi = sx * HX
    for yy, yon in ((HY0 + GM, -1), (HY1 - GM, 1)):     # the gallery's end walls
        duz_duvar(V(xi, yy) if (yon < 0) == (sx > 0) else V(xo, yy), V(xo, yy) if (yon < 0) == (sx > 0) else V(xi, yy), Z0, ZG)
    x0, x1 = sorted((xi, xo + sx * 0.012))
    y.yuz_yon([V(x0, HY0 + GM - 0.012, ZG), V(x1, HY0 + GM - 0.012, ZG), V(x1, HY1 - GM + 0.012, ZG), V(x0, HY1 - GM + 0.012, ZG)], 'kursun', Z)
    korniş(min(xi, xo), max(xi, xo), HY0 + GM, HY1 - GM, ZG - 0.012, 0.012, 0.01)
    korniş(min(xi, xo), max(xi, xo), HY0 + GM, HY1 - GM, Z0 + GH1 - 0.004, 0.008, 0.008)
# side gallery domes
y.bolum('Çatıdaki küçük kubbeler')
for sx in (-1, 1):
    for k in range(5):
        kucuk_kubbe(sx * 0.51, HY0 + 0.15 + k * 0.225, ZR, 0.07)

# ---------------- upper block under the dome ----------------
y.bolum('Kubbe altı duvarları (sivri ve yuvarlak pencereler)')
U = 0.42
ZU = ZR + 0.2
ust = dikdortgen(-U, U, CY - U, CY + U)
pencereli_duvar(ust, ZR, 0.13, [5, 5, 5, 5], en=0.45, v0=0.03, ust=0.025, sivri=0.6)
korniş(-U, U, CY - U, CY + U, ZR + 0.126, 0.008, 0.008)
for i in range(4):            # the band above with round windows
    a, b = ust[i], ust[(i + 1) % 4]
    duz_duvar(a, b, ZR + 0.13, ZU)
    e = (b - a).normalized(); n = V(e.y, -e.x)
    for k in range(3):
        y.oculus(a.lerp(b, (k + 1) / 4) + Z * (ZR + 0.168), e, n, 0.022, 'cam', 'mermer')
korniş(-U, U, CY - U, CY + U, ZU - 0.012, 0.014, 0.012)
y.yuz([V(-U, CY - U, ZU + 0.002), V(U, CY - U, ZU + 0.002), V(U, CY + U, ZU + 0.002), V(-U, CY + U, ZU + 0.002)], 'tas_acik')
# small domes on the roof beside the half domes
for sx in (-1, 1):
    for yy in (HY0 + 0.11, HY1 - 0.11):
        kucuk_kubbe(sx * 0.3, yy, ZR, 0.075)

# ---------------- half domes on windowed half drums (front and back) ----------------
y.bolum('Yarım kubbeler')
for s in (-1, 1):
    c = (0, CY + s * 0.33)
    t0 = math.pi if s < 0 else 0.0
    R = 0.27
    yay = [V(c[0] + R * math.cos(t0 + math.pi * i / 8), c[1] + R * math.sin(t0 + math.pi * i / 8)) for i in range(9)]
    for i in range(8):
        y.kemerli(yay[i] + Z * 0, yay[i + 1], ZR, 0.11, PENCERE, v0=0.025, en=0.45, ust=0.02, derin=0.02, k_say=4, sivri=0.5)
    zh = ZR + 0.11
    halka_yay = lambda rr, zz: [V(c[0] + rr * math.cos(t0 + math.pi * i / 8), c[1] + rr * math.sin(t0 + math.pi * i / 8), zz) for i in range(9)]
    y.serit(halka_yay(R, zh), halka_yay(R + 0.01, zh), 'tas_acik', kapali=False)
    y.serit(halka_yay(R + 0.01, zh), halka_yay(R + 0.01, zh + 0.01), 'tas_acik', kapali=False)
    y.kubbe(c, R + 0.005, zh + 0.01, 0.2, 'kursun', n=48, kat=14, t0=t0, t1=t0 + math.pi, kapak='tas')

# ---------------- weight turrets ----------------
y.bolum('Ağırlık kuleleri')
for sx in (-1, 1):
    for sy in (-1, 1):
        c = (sx * U, CY + sy * U)
        y.prizma(c, 0.07, ZR, ZU + 0.04, 'tas', n=8, ust=False, kat=math.pi / 8)
        ok = cokgen(c, 0.07, 8, math.pi / 8)
        for i in range(8):
            y.kemerli(ok[i], ok[(i + 1) % 8], ZU + 0.04, 0.1, PENCERE, v0=0.02, en=0.45, ust=0.015, derin=0.012, k_say=4, sivri=0.6)
        halka_korniş(c, 0.07, ZU + 0.04, 0.008, 0.008, 8, kat=math.pi / 8)
        halka_korniş(c, 0.07, ZU + 0.14, 0.012, 0.01, 8, kat=math.pi / 8)
        y.prizma(c, 0.07, ZU + 0.152, ZU + 0.153, 'tas_acik', n=8, ust=True, kat=math.pi / 8)
        t = y.kubbe(c, 0.062, ZU + 0.152, 0.065, 'kursun', n=28, kat=8)
        alem(c[0], c[1], t.z, 0.9)

# ---------------- drum and the great dome ----------------
y.bolum('Kasnak: 32 pencere ve payandalar')
ND, RD, HD = 32, 0.36, 0.12
ZD = ZU
dk = cokgen((0, CY), RD, ND)
for i in range(ND):
    y.kemerli(dk[i], dk[(i + 1) % ND], ZD, HD, PENCERE, v0=0.025, en=0.5, ust=0.018, derin=0.02, k_say=4, sivri=0.5, cerceve=(0.005, 'mermer'))
for i in range(ND):            # buttresses between the windows
    a = math.atan2(dk[i].y - CY, dk[i].x)
    e = V(-math.sin(a), math.cos(a)); n = V(math.cos(a), math.sin(a))
    o = dk[i] - e * 0.012 + n * 0.018
    y.kutu(o + Z * ZD, e, -n, 0.024, 0.02, HD - 0.01, 'tas_acik', 'onsagsol')
y.bolum('Büyük kubbe')
halka_korniş((0, CY), RD, ZD + HD, 0.016, 0.02, ND)
y.prizma((0, CY), RD, ZD + HD + 0.016, ZD + HD + 0.017, 'tas_acik', n=ND)
tepe = y.kubbe((0, CY), RD + 0.005, ZD + HD + 0.016, 0.31, 'kursun', n=96, kat=22)
alem(0, CY, tepe.z, 1.8)

# ---------------- courtyard ----------------
y.bolum('Avlu duvarları')
AX, AY0, AY1, AH = 0.6, -1.0, HY0, 0.2
IX, IY0, IY1 = 0.43, -0.83, -0.12
ZA = Z0 + AH
# outer walls with windows (front, left, right)
pencereli_duvar([V(-AX, AY1), V(-AX, AY0), V(AX, AY0), V(AX, AY1)], Z0, AH, [6, 7, 6], en=0.38, v0=0.05, ust=0.045, sivri=0.6)
korniş(-AX, AX, AY0, AY1, Z0, 0.022, 0.01, 'tas_koyu')
korniş(-AX, AX, AY0, AY1, ZA - 0.012, 0.014, 0.012)
for q in ([(-AX, AY0), (AX, AY0), (IX, IY0), (-IX, IY0)], [(AX, AY0), (AX, AY1), (IX, IY1), (IX, IY0)],
          [(AX, AY1), (-AX, AY1), (-IX, IY1), (IX, IY1)], [(-AX, AY1), (-AX, AY0), (-IX, IY0), (-IX, IY1)]):
    y.yuz_yon([V(p[0], p[1], ZA + 0.002) for p in q], 'tas_acik', Z)
for sx in (-1, 1):
    for yy in (AY0,):
        y.kutu((sx * AX - 0.025, yy - 0.025, Z0), X, Y, 0.05, 0.05, AH + 0.02, 'tas', 'onarkasagsolust')
# the arcade facing the court: pointed arches with red-and-white voussoirs on marble columns, a dome over each bay
# (the bays along the hall, the portico before the doors, carry larger domes)
y.bolum('Avlu revakları (kırmızı-beyaz kemerler)')
def revak(a, b, n, buyuk=False):
    arkad(a, b, n, Z0, AH, en=0.78, ust=0.03, sivri=0.5, derin=0.15, son_sutun=True)
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        e = (q - p).normalized(); nc = V(e.y, -e.x)
        m = p.lerp(q, 0.5) - nc * (0.17 / 2)
        if buyuk: kucuk_kubbe(m.x, m.y, ZA, 0.083, kasnak=0.035, son=True)
        else: kucuk_kubbe(m.x, m.y, ZA, 0.07, kasnak=0.02, son=False)
revak(V(IX, IY0), V(-IX, IY0), 5)
revak(V(-IX, IY1), V(IX, IY1), 5, buyuk=True)
revak(V(-IX, IY0), V(-IX, IY1), 4)
revak(V(IX, IY1), V(IX, IY0), 4)
y.bolum('Revak kubbeleri')
for sx in (-1, 1):            # corner bays
    for yy in ((AY0 + IY0) / 2, (AY1 + IY1) / 2):
        kucuk_kubbe(sx * (AX + IX) / 2, yy, ZA, 0.07, kasnak=0.02, son=False)
# court paving and the şadırvan
y.bolum('Avlu döşemesi ve şadırvan')
y.yuz([V(-IX, IY0, Z0 + 0.003), V(IX, IY0, Z0 + 0.003), V(IX, IY1, Z0 + 0.003), V(-IX, IY1, Z0 + 0.003)], 'mermer')
FY = (IY0 + IY1) / 2
y.prizma((0, FY), 0.08, Z0, Z0 + 0.035, 'mermer', n=8, kat=math.pi / 8)
for k in range(8):
    a = math.pi / 8 + 2 * math.pi * k / 8
    y.prizma((0.065 * math.cos(a), FY + 0.065 * math.sin(a)), 0.006, Z0 + 0.035, Z0 + 0.11, 'mermer', n=6, ust=False)
y.prizma((0, FY), 0.105, Z0 + 0.11, Z0 + 0.122, 'kursun', n=8, kat=math.pi / 8)
t = y.kubbe((0, FY), 0.065, Z0 + 0.122, 0.06, 'kursun', n=28, kat=8)
alem(0, FY, t.z, 0.8)

# ---------------- portal ----------------
y.bolum('Taçkapı')
PY0, PY1, PH = AY0 - 0.05, AY0 + 0.02, 0.31
y.kemerli(V(-0.14, PY0, 0), V(0.14, PY0, 0), Z0, PH, ('tas', 'tas_koyu', 'tas_acik', 'ahsap'), v0=0.0, en=0.6, ust=0.05, derin=0.05, k_say=10, sivri=0.6,
          cerceve=(0.014, ['mermer', 'kirmizi']))
y.kutu((-0.14, PY0, Z0), X, Y, 0.28, PY1 - PY0, PH, 'tas', 'sagsol')
korniş(-0.14, 0.14, PY0, PY1, Z0 + PH - 0.014, 0.016, 0.012)
y.yuz([V(-0.14, PY0, Z0 + PH), V(0.14, PY0, Z0 + PH), V(0.14, PY1, Z0 + PH), V(-0.14, PY1, Z0 + PH)], 'tas_acik')
for sx in (-1, 1):
    y.kutu((sx * 0.14 - 0.02, PY0 - 0.01, Z0), X, Y, 0.04, 0.04, PH + 0.03, 'tas_acik', 'onarkasagsolust')
    y.koni((sx * 0.14, PY0 + 0.01), 0.02, Z0 + PH + 0.03, 0.04, 'kursun', n=8)

# ---------------- minarets ----------------
def minare(cx, cy, boy, serefe):
    zt = ZA + 0.06
    y.kutu((cx - 0.06, cy - 0.06, Z0), X, Y, 0.12, 0.12, zt - Z0, 'tas', 'onarkasagsolust')
    korniş(cx - 0.06, cx + 0.06, cy - 0.06, cy + 0.06, zt - 0.01, 0.012, 0.008)
    y.prizma((cx, cy), 0.052, zt, zt + 0.03, 'tas', n=8, kat=math.pi / 8)       # transition
    top = Z0 + boy
    # fluted shaft: 24 sides, every other one set in
    yiv = lambda zq: [V(cx + (0.036 if i % 2 == 0 else 0.032) * math.cos(2 * math.pi * i / 24), cy + (0.036 if i % 2 == 0 else 0.032) * math.sin(2 * math.pi * i / 24), zq) for i in range(24)]
    y.serit(yiv(zt + 0.03), yiv(top - 0.07), 'tas_acik')
    # the "petek" above the last balcony: plain, a little wider, with a cornice
    y.prizma((cx, cy), 0.038, top - 0.07, top, 'tas_acik', n=16, ust=False)
    for k in range(serefe):
        zz = zt + 0.03 + (top - zt - 0.12) * (k + 1) / (serefe + 0.25)
        # corbelled (muqarnas-like) steps under the balcony
        for j, (rr, hh) in enumerate(((0.042, 0.01), (0.05, 0.01), (0.058, 0.008))):
            y.prizma((cx, cy), rr, zz - 0.028 + j * 0.01, zz - 0.028 + j * 0.01 + hh, 'tas', n=16, ust=False)
            y.serit([V(cx + rr * math.cos(2 * math.pi * i / 16), cy + rr * math.sin(2 * math.pi * i / 16), zz - 0.028 + j * 0.01) for i in range(16)],
                    [V(cx + (rr - 0.008) * math.cos(2 * math.pi * i / 16), cy + (rr - 0.008) * math.sin(2 * math.pi * i / 16), zz - 0.028 + j * 0.01) for i in range(16)], 'tas_koyu')
        y.prizma((cx, cy), 0.062, zz - 0.004, zz, 'tas_acik', n=16)
        # railing: outside and inside faces
        dis = lambda zq: [V(cx + 0.06 * math.cos(2 * math.pi * i / 16), cy + 0.06 * math.sin(2 * math.pi * i / 16), zq) for i in range(16)]
        ic = lambda zq: [V(cx + 0.056 * math.cos(2 * math.pi * i / 16), cy + 0.056 * math.sin(2 * math.pi * i / 16), zq) for i in range(16)]
        y.serit(dis(zz), dis(zz + 0.02), 'tas_acik')
        y.serit(ic(zz + 0.02), ic(zz), 'tas_acik')
        y.serit(dis(zz + 0.02), ic(zz + 0.02), 'tas_acik')
    halka_korniş((cx, cy), 0.036, top - 0.004, 0.008, 0.006, 16)
    y.koni((cx, cy), 0.04, top + 0.004, 0.2, 'kursun', n=24)
    alem(cx, cy, top + 0.2, 0.8)

y.bolum('Minareler (yivli gövde, mukarnaslı şerefeler)')
for sx in (-1, 1):
    minare(sx * AX, AY1, 1.22, 3)
    minare(sx * AX, AY0, 0.98, 2)

# ---------------- banner on the portal ----------------
y.silindir((0.1, PY0 + 0.035), 0.006, Z0 + PH, Z0 + PH + 0.2, 'ahsap')
y.kutu((0.106, PY0 + 0.033, Z0 + PH + 0.11), X, Y, 0.1, 0.004, 0.07, 'mavi')

print('UCGEN', y.ucgen_sayisi())

if __name__ == '__main__':
    arg = argumanlar()
    temizle()
    ob, anahtar = nesne_dokulu(y, 'lm_suleymaniye')
    if arg:
        detayli_aktar(ob, anahtar, os.path.abspath(arg[0]))
    if len(arg) > 1:
        onizle_dokulu(os.path.abspath(arg[1]), merkez=(0, 0.1, 0.45), boy=3.3, aci=(-35, 32))
