# The Senate house (lm_senato), after the Curia Julia: a tall brick hall on a podium with corner pilasters, a stuccoed
# upper front with three great grilled windows under a pediment-shaped gable on modillions, a tiled gable roof,
# bronze doors behind an Ionic porch reached by steps; around it a paved forum with statue bases, two honorific
# columns and colonnaded stoas on either side.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi(tohum=3)

ZF = 0.03                       # forum paving
X0, X1, Y0, Y1 = -0.44, 0.44, -0.25, 0.95     # the Curia's walls
ZP = 0.11                       # podium top (hall floor)
ZS = 0.58                       # string course under the windows
ZE = 0.92                       # eaves
DUVAR = ('tugla_roma', 'tugla_roma_koyu', 'kirec', 'cam')
UST = ('siva_krem', 'kirec', 'kirec', 'cam')


def heykel(x, yy, z, s=1.0, key='bronz', kol=1):
    """a standing toga'd statue: robe, torso, head, one arm raised"""
    donel(y, (x, yy), [(0.016 * s, z), (0.014 * s, z + 0.045 * s), (0.011 * s, z + 0.07 * s), (0.008 * s, z + 0.078 * s), (0, z + 0.078 * s)], key, n=10)
    kure(y, (x, yy, z + 0.088 * s), 0.0085 * s, key, n=8, kat=4)
    sh = V(x + 0.009 * s * kol, yy, z + 0.07 * s)
    cubuk(y, sh, sh + V(0.012 * s * kol, -0.004 * s, 0.028 * s), 0.005 * s, key)
    cubuk(y, V(x - 0.009 * s * kol, yy, z + 0.07 * s), V(x - 0.013 * s * kol, yy - 0.006 * s, z + 0.035 * s), 0.005 * s, key)


def antefiks(af, n, t=0.004):
    """an antefix: the triangle af (its face looking along n) as a little slab t thick, with its edges"""
    bk = [q - n * t for q in af]
    y.yuz_yon(af, 'kiremit2', n); y.yuz_yon(bk[::-1], 'kiremit2', -n)
    m = sum(af, V(0, 0, 0)) / 3
    for i in range(3):
        j = (i + 1) % 3
        y.yuz_yon([af[i], af[j], bk[j], bk[i]], 'kiremit2', (af[i] + af[j]) / 2 - m)


def imbrex(cx, yb, ye, xe, ze, zr, adim=0.042):
    """the cover tiles (imbrices) of a Roman tile roof whose ridge runs along y at x = cx: ribs down both slopes from the
    ridge (zr) to the eaves (xe from cx, ze), with an antefix standing at each eave end"""
    n = int((ye - yb) / adim)
    for i in range(n + 1):
        yy = yb + (ye - yb) * i / n
        for sg in (-1, 1):
            p = V(cx + sg * xe, yy, ze + 0.004)
            q = V(cx + sg * 0.012, yy, zr - 0.006)
            cubuk(y, p, q, 0.009, 'kiremit2', 0.006)
            af = [p + V(sg * 0.002, -0.007, -0.004), p + V(sg * 0.002, 0.007, -0.004), p + V(sg * 0.002, 0, 0.014)]
            antefiks(af, V(sg, 0))


def kaide(x, yy, z, w, h, key='mermer'):
    """a moulded statue pedestal; returns its top"""
    kutu_merkez(y, (x, yy), w * 1.18, w * 1.18, h * 0.16, key, z0=z)
    kutu_merkez(y, (x, yy), w, w, h * 0.7, key, z0=z + h * 0.16)
    kornis(y, x - w / 2, x + w / 2, yy - w / 2, yy + w / 2, z + h * 0.86, h * 0.14, w * 0.09, key, 'tac')
    y.yuz_yon([V(x - w / 2, yy - w / 2, z + h), V(x + w / 2, yy - w / 2, z + h), V(x + w / 2, yy + w / 2, z + h), V(x - w / 2, yy + w / 2, z + h)], key, Z)
    return z + h


# ---------------------------------------------------------------- forum paving
y.bolum('forum')
FX0, FX1, FY0, FY1 = -1.15, 1.15, -1.12, 1.08
kutu(y, V(FX0, FY0, 0), X, FX1 - FX0, FY1 - FY0, ZF, 'kirec', 'onarkasagsol')
y.yuz_yon([V(FX0, FY0, ZF), V(FX1, FY0, ZF), V(FX1, FY1, ZF), V(FX0, FY1, ZF)], 'zemin', Z)
silme(y, dikdortgen(FX0, FX1, FY0, FY1), ZF - 0.008, 0.008, 0.006, 'kirec', 'duz')
# a marble band framing the square in front of the Curia
for (ax, ay, bx, by) in ((-0.9, -1.0, 0.9, -1.0), (-0.9, -0.62, 0.9, -0.62)):
    y.yuz_yon([V(ax, ay - 0.015, ZF + 0.0015), V(bx, by - 0.015, ZF + 0.0015), V(bx, by + 0.015, ZF + 0.0015), V(ax, ay + 0.015, ZF + 0.0015)], 'mermer', Z)
for ax in (-0.9, 0.9):
    y.yuz_yon([V(ax - 0.015, -1.0, ZF + 0.0015), V(ax + 0.015, -1.0, ZF + 0.0015), V(ax + 0.015, -0.62, ZF + 0.0015), V(ax - 0.015, -0.62, ZF + 0.0015)], 'mermer', Z)

# ---------------------------------------------------------------- the Curia: podium, walls
y.bolum('kuria duvarlari')
kutu(y, V(X0 - 0.05, Y0 - 0.3, ZF), X, X1 - X0 + 0.1, Y1 - Y0 + 0.35, ZP - ZF, 'kirec', 'onarkasagsol')
y.yuz_yon([V(X0 - 0.05, Y0 - 0.3, ZP), V(X1 + 0.05, Y0 - 0.3, ZP), V(X1 + 0.05, Y1 + 0.05, ZP), V(X0 - 0.05, Y1 + 0.05, ZP)], 'zemin', Z)
silme(y, dikdortgen(X0 - 0.05, X1 + 0.05, Y0 - 0.3, Y1 + 0.05), ZP - 0.012, 0.012, 0.008, 'kirec', 'tac')
silme(y, dikdortgen(X0 - 0.05, X1 + 0.05, Y0 - 0.3, Y1 + 0.05), ZF, 0.014, 0.008, 'kirec', 'kaide')
# a travertine base course round the hall
kornis(y, X0, X1, Y0, Y1, ZP, 0.07, 0.01, 'kirec', 'kaide')
# the front steps
merdiven(y, (0, Y0 - 0.3 - 0.12), math.pi / 2, 0.6, ZF, ZP, n=6, d=0.02, key='kirec', yanlik='kirec')

W_ = X1 - X0
# front: lower wall with the great bronze door, upper stuccoed zone with three windows
dikdortgen_acik(y, V(X0, Y0), V(X1, Y0), ZP, ZS - ZP, 0.5 - 0.12 / W_ * 1.0, 0.5 + 0.12 / W_ * 1.0, 0.0, 0.33,
                ('tugla_roma', 'kirec', 'kirec', 'bronz'), derin=0.04, cerceve=(0.022, 'mermer'))
for k in range(3):
    a, b = V(X0 + W_ * k / 3, Y0), V(X0 + W_ * (k + 1) / 3, Y0)
    dikdortgen_acik(y, a, b, ZS, ZE - ZS, 0.24, 0.76, 0.05, 0.27, UST, derin=0.03, cerceve=(0.014, 'mermer'))
    kafes(y, a, b, ZS, 0.24, 0.76, 0.05, 0.27, 'bronz', nu=4, nv=3, en=0.005, ileri=0.015)
    # a sill ledge on consoles
    m = (a + b) / 2
    kutu_merkez(y, (m.x, Y0 - 0.013), (b - a).length * 0.62, 0.024, 0.008, 'mermer', z0=ZS + 0.042)
    for s in (-1, 1):
        kutu_merkez(y, (m.x + s * (b - a).length * 0.24, Y0 - 0.009), 0.012, 0.018, 0.018, 'mermer', z0=ZS + 0.024)
# the door's bronze leaves: raised panels and a meeting stile
for col in range(2):
    for row in range(3):
        x0 = -0.108 + col * 0.112; z0 = ZP + 0.02 + row * 0.1
        kutu(y, V(x0, Y0 + 0.04 - 0.004, z0), X, 0.092, 0.004, 0.085, 'bronz', 'onsagsolust')
cubuk(y, V(0, Y0 + 0.034, ZP), V(0, Y0 + 0.034, ZP + 0.33), 0.008, 'bronz')
# a lintel tablet over the door
kutu_merkez(y, (0, Y0 - 0.008), 0.3, 0.016, 0.05, 'mermer', z0=ZP + 0.37)
for i, c in enumerate('SENATVS'):
    x = -0.09 + i * 0.03
    kutu(y, V(x - 0.007, Y0 - 0.0165, ZP + 0.383), X, 0.014, 0.001, 0.024, 'koyu', 'on')

# sides: brick, three tall windows each high up, small ones below
for sx in (-1, 1):
    xw = X1 if sx > 0 else X0
    for k in range(3):
        ya, yb = Y0 + (Y1 - Y0) * k / 3, Y0 + (Y1 - Y0) * (k + 1) / 3
        a, b = (V(xw, ya), V(xw, yb)) if sx > 0 else (V(xw, yb), V(xw, ya))
        dikdortgen_acik(y, a, b, ZP, ZE - ZP, 0.3, 0.7, 0.53, 0.75, DUVAR, derin=0.03, cerceve=(0.012, 'kirec'))
        kafes(y, a, b, ZP, 0.3, 0.7, 0.53, 0.75, 'bronz', nu=3, nv=3, en=0.005, ileri=0.015)
        for u in (0.25, 0.75):   # small square windows below
            p = a.lerp(b, u)
            nn = V(sx, 0)
            y.pencere(p + Z * ZP, (b - a).normalized(), nn, -0.018, 0.2, 0.036, 0.05, 'cam', kemer=True)
# back: three windows, a small door
for k in range(3):
    a, b = V(X0 + W_ * (k + 1) / 3, Y1), V(X0 + W_ * k / 3, Y1)
    dikdortgen_acik(y, a, b, ZP, ZE - ZP, 0.25, 0.75, 0.5, 0.75, DUVAR, derin=0.03, cerceve=(0.014, 'kirec'))
y.pencere(V(0.06, Y1, ZP), V(-1, 0), V(0, 1), 0.0, 0.0, 0.12, 0.2, 'ahsap', kemer=False)

# corner pilasters and the side buttresses (they run up to the eaves)
y.bolum('payandalar')
for (px, py) in ((X0, Y0), (X1, Y0), (X0, Y1), (X1, Y1)):
    kutu_merkez(y, (px, py), 0.09, 0.09, ZE - ZP, 'tugla_roma', z0=ZP)
    kutu_merkez(y, (px, py), 0.105, 0.105, 0.03, 'kirec', z0=ZP)
for sx in (-1, 1):
    for k in (1, 2):
        yy = Y0 + (Y1 - Y0) * k / 3
        kutu_merkez(y, (sx * (X1 + 0.012), yy), 0.044, 0.06, ZE - ZP - 0.02, 'tugla_roma', z0=ZP)
# string course and the eaves cornice on modillions
y.bolum('kornisler')
kornis(y, X0 - 0.045, X1 + 0.045, Y0 - 0.045, Y1 + 0.045, ZS - 0.012, 0.016, 0.012, 'kirec', 'kaba')
kornis(y, X0, X1, Y0, Y1, ZE - 0.03, 0.03, 0.068, 'kirec', 'tac')
for (a, b, n) in ((V(X0 - 0.045, Y0 - 0.045), V(X1 + 0.045, Y0 - 0.045), 15), (V(X1 + 0.045, Y1 + 0.045), V(X0 - 0.045, Y1 + 0.045), 15),
                  (V(X1 + 0.045, Y0 - 0.045), V(X1 + 0.045, Y1 + 0.045), 20), (V(X0 - 0.045, Y1 + 0.045), V(X0 - 0.045, Y0 - 0.045), 20)):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for i in range(1, n):
        p = a.lerp(b, i / n)
        kutu(y, p - e * 0.006 + nn * 0.016 + Z * (ZE - 0.048), e, 0.012, 0.016, 0.02, 'kirec', 'onsagsolust')

# ---------------------------------------------------------------- roof and the front pediment
y.bolum('cati')
SAC = 0.05
zr = cati_besik(y, X0, X1, Y0, Y1, ZE, 0.2, 0.075, 'kiremit', 'kiremit2', kalinlik=0.014, ucluk_key='siva_krem', uc_sacak=0.035)
imbrex(0, Y0 - 0.02, Y1 + 0.02, X1 + 0.075, ZE, ZE + 0.2)
# raking cornices of the front gable and their modillions
A, B, T = V(X0 - 0.075, Y0 - 0.047, ZE), V(X1 + 0.075, Y0 - 0.047, ZE), V(0, Y0 - 0.047, ZE + 0.2)
for p, q in ((A, T), (T, B)):
    cubuk(y, p + Z * 0.002, q + Z * 0.002, 0.03, 'kirec', 0.034)   # (deep enough to hide the roof's verge board)
    d = (q - p).normalized()
    for i in range(1, 9):
        c = p.lerp(q, i / 9)
        kutu_merkez(y, (c.x, c.y + 0.004), 0.012, 0.02, 0.022, 'kirec', z0=c.z - 0.034)   # (under the deep raking cornice)
# the back gable: raking cornices too, and a round window in its tympanum
A2, B2, T2 = V(X1 + 0.075, Y1 + 0.047, ZE), V(X0 - 0.075, Y1 + 0.047, ZE), V(0, Y1 + 0.047, ZE + 0.2)
for p, q in ((A2, T2), (T2, B2)):
    cubuk(y, p + Z * 0.002, q + Z * 0.002, 0.03, 'kirec', 0.034)   # (deep enough to hide the roof's verge board)
y.oculus(V(0, Y1 + 0.002, ZE + 0.075), V(-1, 0), V(0, 1), 0.03, 'cam', 'kirec', f=0.008, k=14)
for p in (A2 + V(-0.03, -0.02, 0.012), B2 + V(0.03, -0.02, 0.012)):
    kutu_merkez(y, (p.x, p.y), 0.04, 0.04, 0.03, 'kirec', z0=p.z)
# acroteria: small bronze statues on the gable ends, a banner on the apex
for p, kol in ((A + V(0.03, 0.02, 0.012), 1), (B + V(-0.03, 0.02, 0.012), -1)):
    kutu_merkez(y, (p.x, p.y), 0.04, 0.04, 0.02, 'kirec', z0=p.z)
    heykel(p.x, p.y, p.z + 0.02, 0.9, 'bronz', kol)
kutu_merkez(y, (T.x, T.y + 0.01), 0.04, 0.04, 0.025, 'kirec', z0=T.z + 0.008)
sancak(y, T.x, T.y + 0.01, T.z + 0.033, boy=0.22, en=0.13, yuk=0.08, aci=math.radians(200))
# a bronze wreath in the stuccoed tympanum
y.oculus(V(0, Y0 - 0.002, ZE + 0.07), X, V(0, -1), 0.028, 'siva_krem', 'bronz', f=0.007, k=16)

# ---------------------------------------------------------------- the Ionic porch in front of the door
y.bolum('revak')
YP = Y0 - 0.25
zt = sutunlu_revak(y, V(X0 + 0.02, YP), V(X1 - 0.02, YP), 5, ZP, 0.3, 'iyon', r=0.017, key='mermer', derin=0.06)
# its lean-to roof against the front wall, a coffered ceiling below
zr0, zr1 = zt, ZS - 0.03
y.yuz_yon([V(X0 - 0.01, YP - 0.04, zr0), V(X1 + 0.01, YP - 0.04, zr0), V(X1 + 0.01, Y0, zr1), V(X0 - 0.01, Y0, zr1)], 'kiremit', V(0, -0.3, 1))
y.yuz_yon([V(X0 - 0.01, YP - 0.04, zr0 - 0.012), V(X1 + 0.01, YP - 0.04, zr0 - 0.012), V(X1 + 0.01, YP - 0.04, zr0), V(X0 - 0.01, YP - 0.04, zr0)], 'mermer', V(0, -1))
for sx, xx in ((-1, X0 - 0.01), (1, X1 + 0.01)):
    y.yuz_yon([V(xx, YP - 0.04, zr0 - 0.012), V(xx, Y0, zr1 - 0.012), V(xx, Y0, zr1), V(xx, YP - 0.04, zr0)], 'mermer', V(sx, 0))
y.yuz_yon([V(X0 - 0.01, YP - 0.04, zr0 - 0.012), V(X1 + 0.01, YP - 0.04, zr0 - 0.012), V(X1 + 0.01, Y0, zr1 - 0.012), V(X0 - 0.01, Y0, zr1 - 0.012)], 'ahsap_koyu', -Z)
for i in range(22):
    xx = X0 + 0.01 + (W_ - 0.02) * i / 21
    p, q = V(xx, YP - 0.036, zr0 + 0.004), V(xx, Y0 - 0.004, zr1 + 0.004)
    cubuk(y, p, q, 0.009, 'kiremit2', 0.006)
    af = [p + V(-0.007, -0.002, -0.004), p + V(0.007, -0.002, -0.004), p + V(0, -0.002, 0.014)]
    antefiks(af, V(0, -1))

# ---------------------------------------------------------------- the stoas on either side
y.bolum('yan revaklar')
for sx in (-1, 1):
    xa, xb = (0.66, 1.08) if sx > 0 else (-1.08, -0.66)
    ya, yb = -0.32, 0.98
    zemin(y, xa, xb, ya, yb, 0.04, 'kirec', basamak=(), silmeli=True)
    # two rows of Tuscan columns, the outer one with a wall behind (shops), the inner one open to the forum
    xi, xo = (xa + 0.04, xb - 0.04) if sx > 0 else (xb - 0.04, xa + 0.04)
    a_i, b_i = (V(xi, yb - 0.04), V(xi, ya + 0.04)) if sx > 0 else (V(xi, ya + 0.04), V(xi, yb - 0.04))
    zt2 = sutunlu_revak(y, a_i, b_i, 7, 0.04, 0.26, 'toskan', r=0.014, key='mermer')
    # the back wall with shop doors (tabernae)
    a_o, b_o = (V(xo, yb - 0.04), V(xo, ya + 0.04)) if sx > 0 else (V(xo, ya + 0.04), V(xo, yb - 0.04))
    for k in range(7):
        p, q = a_o.lerp(b_o, k / 7), a_o.lerp(b_o, (k + 1) / 7)
        dikdortgen_acik(y, q, p, 0.04, zt2 - 0.04, 0.3, 0.7, 0.0, 0.15, ('siva_krem', 'kirec', 'kirec', 'ahsap_koyu'), derin=0.015,
                        cerceve=(0.008, 'kirec'))
        # (the inner face stands 0.03 inside the outer one: the two door recesses must not poke through each other)
        di = V(-sx * 0.03, 0)
        dikdortgen_acik(y, p + di, q + di, 0.04, zt2 - 0.04, 0.3, 0.7, 0.0, 0.15, ('siva_krem', 'kirec', 'kirec', 'ahsap_koyu'), derin=0.015,
                        cerceve=(0.008, 'kirec'))
    # the end walls: a doorway framed by two pilasters, a plinth and a frieze band (the south ends face the forum)
    x_lo, x_hi = min(xi, xo), max(xi, xo)
    for yy, sy in ((ya + 0.04, -1), (yb - 0.04, 1)):
        a_e, b_e = (V(x_lo, yy), V(x_hi, yy)) if sy < 0 else (V(x_hi, yy), V(x_lo, yy))
        dikdortgen_acik(y, a_e, b_e, 0.04, zt2 - 0.04, 0.36, 0.64, 0.0, 0.15, ('siva_krem', 'kirec', 'kirec', 'ahsap_koyu'),
                        derin=0.02, cerceve=(0.009, 'kirec'))
        # a small window over the door
        y.pencere(V(a_e.x, yy, 0.04), (b_e - a_e).normalized(), V(0, sy), (x_hi - x_lo) * 0.43, 0.175, (x_hi - x_lo) * 0.14, 0.04,
                  'cam', kemer=True)
        for xx in (x_lo + 0.022, x_hi - 0.022):
            kutu_merkez(y, (xx, yy + sy * 0.006), 0.028, 0.012, zt2 - 0.04 - 0.012, 'kirec', z0=0.04)
            kutu_merkez(y, (xx, yy + sy * 0.008), 0.036, 0.016, 0.012, 'kirec', z0=zt2 - 0.012)
        kutu_merkez(y, ((x_lo + x_hi) / 2, yy + sy * 0.004), x_hi - x_lo, 0.008, 0.02, 'kirec', z0=0.04)
        kutu_merkez(y, ((x_lo + x_hi) / 2, yy + sy * 0.004), x_hi - x_lo, 0.008, 0.016, 'kirec', z0=zt2 - 0.03)
    y.yuz_yon([V(xi, ya + 0.04, zt2 - 0.002), V(xo, ya + 0.04, zt2 - 0.002), V(xo, yb - 0.04, zt2 - 0.002), V(xi, yb - 0.04, zt2 - 0.002)], 'ahsap_koyu', -Z)
    cati_besik(y, min(xi, xo) - 0.01, max(xi, xo) + 0.01, ya + 0.03, yb - 0.03, zt2, 0.09, 0.03, 'kiremit', 'kiremit2', ucluk_key='siva_krem',
               alinlik_key='kirec')
    imbrex((xi + xo) / 2, ya + 0.02, yb - 0.02, abs(xo - xi) / 2 + 0.04, zt2, zt2 + 0.09)

# ---------------------------------------------------------------- statues and honorific columns in the forum
y.bolum('heykeller')
for sx in (-1, 1):
    # an honorific column with a gilded statue
    x, yy = sx * 0.6, -0.84
    zk = kaide(x, yy, ZF, 0.09, 0.1, 'mermer')
    sutun(y, x, yy, zk, zk + 0.42, 0.024, 'mermer', 'korint')
    kutu_merkez(y, (x, yy), 0.05, 0.05, 0.016, 'mermer', z0=zk + 0.42)
    heykel(x, yy, zk + 0.436, 1.1, 'altin', sx)
    # statue bases with bronze figures
    for (bx, by) in ((sx * 0.27, -0.98), (sx * 0.9, -0.78)):
        zk = kaide(bx, by, ZF, 0.06, 0.07, 'mermer')
        heykel(bx, by, zk, 1.0, 'bronz', -sx)
# two marble fountains (a basin on a pedestal)
for sx in (-1, 1):
    c = (sx * 0.58, -0.6)
    donel(y, c, [(0.07, ZF), (0.07, ZF + 0.012), (0.06, ZF + 0.012), (0.06, ZF + 0.004)], 'mermer', n=24)
    y.yuz_yon([V(c[0] + 0.06 * math.cos(TAU * i / 24), c[1] + 0.06 * math.sin(TAU * i / 24), ZF + 0.004) for i in range(24)], 'su', Z)
    donel(y, c, [(0.012, ZF + 0.004), (0.01, ZF + 0.05), (0.04, ZF + 0.07), (0.045, ZF + 0.078), (0.036, ZF + 0.078), (0.036, ZF + 0.072)], 'mermer', n=16)
    y.yuz_yon([V(c[0] + 0.036 * math.cos(TAU * i / 16), c[1] + 0.036 * math.sin(TAU * i / 16), ZF + 0.072) for i in range(16)], 'su', Z)
    kure(y, (c[0], c[1], ZF + 0.082), 0.008, 'bronz', n=8, kat=4)
# an altar before the steps
kutu_merkez(y, (0, -0.84), 0.12, 0.06, 0.012, 'mermer', z0=ZF)
kutu_merkez(y, (0, -0.84), 0.1, 0.045, 0.045, 'mermer', z0=ZF + 0.012)
kornis(y, -0.05, 0.05, -0.8625, -0.8175, ZF + 0.05, 0.01, 0.006, 'mermer', 'tac')
for s in (-1, 1):
    boru(y, [V(s * 0.043, -0.862, ZF + 0.062), V(s * 0.043, -0.818, ZF + 0.062)], 0.008, 'mermer', n=8)

calistir(y, 'lm_senato')
