# Turnuva Alanı (lm_turnuva): a Frankish tournament ground. The sanded lists with the cloth-hung tilt barrier down the
# middle and two knights charging with couched lances; behind them the tiered wooden stands under striped awnings full
# of spectators and, in the middle, the royal box: a raised pavilion with a barrel-vaulted striped canopy, heraldic
# hangings and shields. Before the lists the knights' striped round tents with pennants, shield racks, lance racks,
# squires and caparisoned horses; behind it all the castle's curtain wall with a tall round tower (the silhouette).
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ortak import *
from bina_ortak import calistir

import doku

y = Yapi()

G = 0.04
doku.KOSE_RENK['cimen'] = cayir_renk(G)
XA, XB, YA, YB = -1.1, 1.1, -1.0, 1.0
FX0, FX1, FY0, FY1 = -0.9, 0.9, -0.36, 0.16     # the lists
TY = (FY0 + FY1) / 2                             # the tilt

# ---------------------------------------------------------------- ground, lists, tilt
y.bolum('Zemin ve meydan')
zemin_blok(y, XA, XB, YA, YB, G)
y.yuz_yon([V(FX0, FY0, G + 0.003), V(FX1, FY0, G + 0.003), V(FX1, FY1, G + 0.003), V(FX0, FY1, G + 0.003)], 'kum_acik', Z)
# hoof-churned tracks either side of the tilt
for s in (-1, 1):
    yy = TY + s * 0.09
    y.yuz_yon([V(FX0 + 0.04, yy - 0.035, G + 0.005), V(FX1 - 0.04, yy - 0.035, G + 0.005), V(FX1 - 0.04, yy + 0.035, G + 0.005),
               V(FX0 + 0.04, yy + 0.035, G + 0.005)], 'kum', Z)
# a road in from the front and paths to the tents
y.yuz_yon([V(-0.08, YA + 0.001, G + 0.003), V(0.08, YA + 0.001, G + 0.003), V(0.08, FY0 - 0.06, G + 0.003), V(-0.08, FY0 - 0.06, G + 0.003)], 'toprak', Z)

y.bolum('Ayırma çiti (tilt)')
TX0, TX1 = FX0 + 0.14, FX1 - 0.14
n_ = 16
for k in range(n_ + 1):
    x = TX0 + (TX1 - TX0) * k / n_
    cubuk(y, V(x, TY, G), V(x, TY, G + 0.075), 0.01, 'ahsap_koyu')
cubuk(y, V(TX0 - 0.01, TY, G + 0.075), V(TX1 + 0.01, TY, G + 0.075), 0.012, 'ahsap', 0.014)
for k in range(n_):
    xa, xb = TX0 + (TX1 - TX0) * k / n_ + 0.002, TX0 + (TX1 - TX0) * (k + 1) / n_ - 0.002
    kk = 'boya_kirmizi' if k % 2 else 'boya_sari'
    for s in (-1, 1):
        yy = TY + s * 0.009
        levha(y, [V(xa, yy, G + 0.012), V(xb, yy, G + 0.012), V(xb, yy, G + 0.07), V(xa, yy, G + 0.07)], kk, V(0, s), 0.0012)
        # a scalloped hem
        levha(y, [V(xa, yy + s * 0.0004, G + 0.012), V(xb, yy + s * 0.0004, G + 0.012), V((xa + xb) / 2, yy + s * 0.0004, G + 0.004)], kk, V(0, s), 0.0012)
# the lists' fence round the field, gates at the ends
for (a, b) in ((V(FX0, FY0), V(FX1, FY0)), (V(FX1, FY1), V(FX0, FY1))):
    L = (b - a).length; n = int(L / 0.09)
    for k in range(n + 1):
        p = a.lerp(b, k / n)
        cubuk(y, p + Z * G, p + Z * (G + 0.05), 0.008, 'ahsap_koyu')
    for zz in (G + 0.025, G + 0.048):
        cubuk(y, a + Z * zz, b + Z * zz, 0.006, 'ahsap', 0.006)
for sx in (-1, 1):   # the gates: tall posts with a lintel and pennants
    x = FX0 if sx < 0 else FX1
    for yy in (FY0, FY1):
        y.prizma((x, yy), 0.012, G, G + 0.16, 'ahsap_koyu', n=8)
        kure(y, (x, yy, G + 0.168), 0.012, 'altin', n=8, kat=4)
    for yy in (FY0 + 0.1, FY1 - 0.1):
        cubuk(y, V(x, FY0, G + 0.05), V(x, yy, G + 0.05), 0.007, 'ahsap', 0.007) if yy < TY else cubuk(y, V(x, yy, G + 0.05), V(x, FY1, G + 0.05), 0.007, 'ahsap', 0.007)
    cubuk(y, V(x, FY0, G + 0.14), V(x, FY1, G + 0.14), 0.014, 'ahsap', 0.014)
    for k in range(5):
        yy = FY0 + 0.05 + (FY1 - FY0 - 0.1) * k / 4
        levha(y, [V(x, yy - 0.025, G + 0.133), V(x, yy + 0.025, G + 0.133), V(x, yy, G + 0.095)], 'boya_kirmizi' if k % 2 else 'beyaz', V(sx, 0), 0.0012)

y.bolum('Mızrak dövüşü: iki şövalye')
sovalye(y, -0.3, TY - 0.075, G + 0.004, 0.0, 1.35, 'boya_kirmizi', 'boya_sari', 'boya_kirmizi', mizrak=True, kosu=1.0, faz=0.1, sorguc='boya_sari',
        mizrak_egim=0.006, dokum=True)
sovalye(y, 0.26, TY + 0.075, G + 0.004, math.pi, 1.35, 'kobalt', 'beyaz', 'kobalt', mizrak=True, kosu=1.0, faz=0.55, sorguc='beyaz',
        mizrak_egim=0.006, dokum=True)
# a marshal with his baton, a herald
insan(y, 0.0, FY0 + 0.05, G + 0.003, 'altin', aci=math.pi / 2, kol=0.8, sapka='boya_kirmizi')
insan(y, 0.62, FY1 - 0.05, G + 0.003, 'boya_yesil', aci=-math.pi / 2, kol=0.6)


# ---------------------------------------------------------------- stands
def tente(x0, x1, yf, yb, zf, zb, renk=('boya_kirmizi', 'beyaz'), n=None, sacak=True):
    """a striped awning: a cloth sloping from the front edge (yf, zf) up to the back (yb, zb), stripes across x,
    a scalloped valance along the front"""
    n = n or max(2, int(round((x1 - x0) / 0.06)))
    for i in range(n):
        xa, xb = x0 + (x1 - x0) * i / n, x0 + (x1 - x0) * (i + 1) / n
        q = [V(xa, yf, zf), V(xb, yf, zf), V(xb, yb, zb), V(xa, yb, zb)]
        levha(y, q, renk[i % 2], V(0, (zf - zb) * (1 if yb > yf else -1), abs(yb - yf)), 0.0015)
        if sacak:
            levha(y, [V(xa, yf, zf), V(xb, yf, zf), V((xa + xb) / 2, yf, zf - 0.022)], renk[(i + 1) % 2], V(0, -1 if yb > yf else 1), 0.0012)


def tribun(x0, x1, y0, kat=4, derin=0.055, adim=0.04, tohum=0, tente_renk=('boya_kirmizi', 'beyaz')):
    """tiered timber stands along x from x0 to x1, the front row at y0 rising towards +y: plank risers and seats,
    a plank back wall with braces, end walls, spectators, posts carrying a striped awning, pennants on top"""
    y1 = y0 + derin * kat
    zt = G + adim * kat
    for k in range(kat):
        ya, za = y0 + derin * k, G + adim * (k + 1)
        # the riser (front face) and the seat (top) of this tier
        y.yuz_yon([V(x0, ya, za - adim), V(x1, ya, za - adim), V(x1, ya, za), V(x0, ya, za)], 'ahsap_dikey', -Y)
        y.yuz_yon([V(x0, ya, za), V(x1, ya, za), V(x1, ya + derin, za), V(x0, ya + derin, za)], 'ahsap' if k % 2 else 'ahsap_acik', Z)
        cubuk(y, V(x0, ya + 0.004, za - 0.002), V(x1, ya + 0.004, za - 0.002), 0.008, 'ahsap_koyu', 0.006)
    # ends and back
    for sx, x in ((-1, x0), (1, x1)):
        pts = [V(x, y0, G)]
        for k in range(kat):
            pts += [V(x, y0 + derin * k, G + adim * (k + 1)), V(x, y0 + derin * (k + 1), G + adim * (k + 1))]
        pts += [V(x, y1, G)]
        y.yuz_yon(pts, 'ahsap_dikey', V(sx, 0))
    y.yuz_yon([V(x1, y1, G), V(x0, y1, G), V(x0, y1, zt + 0.16), V(x1, y1, zt + 0.16)], 'ahsap_dikey', Y)
    y.yuz_yon([V(x0, y1 - 0.004, zt), V(x1, y1 - 0.004, zt), V(x1, y1 - 0.004, zt + 0.16), V(x0, y1 - 0.004, zt + 0.16)], 'kumas', -Y)
    y.yuz_yon([V(x0, y1 - 0.004, zt + 0.16), V(x1, y1 - 0.004, zt + 0.16), V(x1, y1, zt + 0.16), V(x0, y1, zt + 0.16)], 'ahsap_koyu', Z)
    for x in (x0, x1):   # (the back wall's ends above the tiers)
        y.yuz_yon([V(x, y1 - 0.004, zt), V(x, y1, zt), V(x, y1, zt + 0.16), V(x, y1 - 0.004, zt + 0.16)], 'ahsap_koyu', V(1 if x == x1 else -1, 0))
    # posts on the back wall and braces behind
    n = max(2, int(round((x1 - x0) / 0.12)))
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        cubuk(y, V(x, y1 + 0.006, G), V(x, y1 + 0.006, zt + 0.17), 0.012, 'ahsap_koyu')
        cubuk(y, V(x, y1 + 0.06, G), V(x, y1 + 0.008, zt * 0.8), 0.008, 'ahsap_koyu', 0.006)
        # front posts of the awning
        cubuk(y, V(x, y0 - 0.012, G), V(x, y0 - 0.012, zt + 0.1), 0.008, 'ahsap')
    tente(x0 - 0.015, x1 + 0.015, y0 - 0.03, y1 + 0.01, zt + 0.1, zt + 0.175, tente_renk)
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        if i % 2 == 0:
            y.prizma((x, y1 + 0.006), 0.003, zt + 0.17, zt + 0.25, 'ahsap', n=4)
            levha(y, [V(x + 0.004, y1 + 0.006, zt + 0.245), V(x + 0.06, y1 + 0.006, zt + 0.232), V(x + 0.004, y1 + 0.006, zt + 0.218)],
                  tente_renk[0] if (i // 2) % 2 else 'boya_sari', -Y, 0.0012)
    # the crowd: seated spectators on the tiers, some cheering
    renkler = ['boya_kirmizi', 'boya_yesil', 'kobalt', 'boya_sari', 'kumas', 'beyaz', 'ahsap_acik', 'kirmizi']
    for k in range(kat):
        ya, za = y0 + derin * k, G + adim * (k + 1)
        m = int((x1 - x0) / 0.034)
        for j in range(m):
            if (j * 7 + k * 3 + tohum) % 5 == 0: continue
            x = x0 + 0.02 + (x1 - x0 - 0.04) * j / max(1, m - 1)
            oturan(y, x, ya + derin * 0.45, za, renkler[(j * 3 + k * 5 + tohum) % len(renkler)], aci=-math.pi / 2, s=1.1,
                   kol=((j + k + tohum) % 4 == 0))


y.bolum('Tribünler')
SY0 = FY1 + 0.1
tribun(-1.0, -0.3, SY0, tohum=1)
tribun(0.3, 1.0, SY0, tohum=2, tente_renk=('kobalt', 'boya_sari'))

y.bolum('Kral locası')
LX0, LX1 = -0.25, 0.25
LY0, LY1 = SY0 - 0.02, SY0 + 0.26
LZ = G + 0.15                     # the box's floor
# the platform on posts, its front draped with a striped cloth and shields
for x in (LX0, -0.083, 0.083, LX1):
    for yy in (LY0 + 0.01, LY1 - 0.01):
        y.prizma((x, yy), 0.012, G, LZ, 'ahsap_koyu', n=8)
y.yuz_yon([V(LX0, LY0, LZ), V(LX1, LY0, LZ), V(LX1, LY1, LZ), V(LX0, LY1, LZ)], 'ahsap_acik', Z)
y.yuz_yon([V(LX0, LY0, LZ - 0.012), V(LX1, LY0, LZ - 0.012), V(LX1, LY1, LZ - 0.012), V(LX0, LY1, LZ - 0.012)], 'ahsap_koyu', -Z)
for (a, b, nrm) in ((V(LX0, LY0), V(LX1, LY0), -Y), (V(LX1, LY0), V(LX1, LY1), X), (V(LX1, LY1), V(LX0, LY1), Y), (V(LX0, LY1), V(LX0, LY0), -X)):
    y.yuz_yon([a + Z * (LZ - 0.012), b + Z * (LZ - 0.012), b + Z * LZ, a + Z * LZ], 'ahsap_koyu', nrm)
nb = 10
for i in range(nb):   # the hanging cloth down the front, a parapet above it
    xa, xb = LX0 + (LX1 - LX0) * i / nb, LX0 + (LX1 - LX0) * (i + 1) / nb
    levha(y, [V(xa, LY0 - 0.006, G + 0.02), V(xb, LY0 - 0.006, G + 0.02), V(xb, LY0 - 0.006, LZ + 0.05), V(xa, LY0 - 0.006, LZ + 0.05)],
          'kobalt' if i % 2 else 'altin', -Y, 0.0015)
    levha(y, [V(xa, LY0 - 0.0075, G + 0.02), V(xb, LY0 - 0.0075, G + 0.02), V((xa + xb) / 2, LY0 - 0.0075, G + 0.006)], 'kobalt' if i % 2 else 'altin', -Y, 0.0012)
kutu(y, V(LX0, LY0 - 0.004, LZ + 0.05), X, LX1 - LX0, 0.012, 0.01, 'ahsap_koyu', 'onarkasagsolust')
for k, x in enumerate((-0.19, -0.095, 0.0, 0.095, 0.19)):   # heater shields on the parapet
    kk = ['boya_kirmizi', 'boya_sari', 'kobalt', 'boya_yesil', 'beyaz'][k]
    levha(y, [V(x - 0.022, LY0 - 0.0125, LZ + 0.043), V(x + 0.022, LY0 - 0.0125, LZ + 0.043), V(x + 0.022, LY0 - 0.0125, LZ + 0.02),
              V(x, LY0 - 0.0125, LZ - 0.005), V(x - 0.022, LY0 - 0.0125, LZ + 0.02)], kk, -Y, 0.002)
    kutu3(y, V(x, LY0 - 0.0155, LZ + 0.02), X, Y, Z, 0.006, 0.0012, 0.036, 'altin' if kk != 'boya_sari' else 'boya_kirmizi')
    kutu3(y, V(x, LY0 - 0.0155, LZ + 0.028), X, Y, Z, 0.03, 0.0012, 0.006, 'altin' if kk != 'boya_sari' else 'boya_kirmizi')
# a stair up the side
for k in range(7):
    t = (k + 0.5) / 7
    kutu3(y, V(LX1 + 0.04, LY1 - 0.02 - 0.2 * t, G + (LZ - G) * t), X, Y, Z, 0.06, 0.03, 0.01, 'ahsap')
for s in (-1, 1):
    cubuk(y, V(LX1 + 0.04 + s * 0.032, LY1 - 0.02, G + 0.02), V(LX1 + 0.04 + s * 0.032, LY1 - 0.22, LZ + 0.02), 0.008, 'ahsap_koyu', 0.016)
# the pavilion: posts, a back hanging, and the barrel-vaulted canopy
PZ = LZ + 0.2                    # the vault's springing
for x in (LX0 + 0.008, -0.083, 0.083, LX1 - 0.008):
    y.prizma((x, LY0 + 0.012), 0.008, LZ, PZ, 'altin', n=8)
    y.prizma((x, LY1 - 0.012), 0.008, LZ, PZ, 'altin', n=8)
    kure(y, (x, LY0 + 0.012, PZ - 0.005), 0.011, 'altin', n=8, kat=4)
for i in range(nb):
    xa, xb = LX0 + (LX1 - LX0) * i / nb, LX0 + (LX1 - LX0) * (i + 1) / nb
    levha(y, [V(xb, LY1 - 0.01, LZ), V(xa, LY1 - 0.01, LZ), V(xa, LY1 - 0.01, PZ), V(xb, LY1 - 0.01, PZ)], 'kobalt' if i % 2 else 'boya_kirmizi', -Y, 0.0015)
for sx in (-1, 1):   # side hangings, half drawn
    x = LX0 + 0.004 if sx < 0 else LX1 - 0.004
    levha(y, [V(x, LY1 - 0.012, LZ), V(x, LY1 - 0.09, LZ), V(x, LY1 - 0.07, PZ), V(x, LY1 - 0.012, PZ)], 'boya_kirmizi', V(sx, 0), 0.0015)
RV = (LY1 - LY0) / 2 + 0.02
CY_ = (LY0 + LY1) / 2
na = 12
arc = [(CY_ - RV * math.cos(math.pi * k / na), PZ + RV * 0.9 * math.sin(math.pi * k / na)) for k in range(na + 1)]
ns = 10
for i in range(ns):
    xa, xb = LX0 - 0.025 + (LX1 - LX0 + 0.05) * i / ns, LX0 - 0.025 + (LX1 - LX0 + 0.05) * (i + 1) / ns
    for k in range(na):
        (ya, za), (yb, zb) = arc[k], arc[k + 1]
        nrm = V(0, (ya + yb) / 2 - CY_, ((za + zb) / 2 - PZ) / 0.81)
        levha(y, [V(xa, ya, za), V(xb, ya, za), V(xb, yb, zb), V(xa, yb, zb)], 'boya_kirmizi' if i % 2 else 'altin', nrm, 0.002)
for sx, x in ((-1, LX0 - 0.025), (1, LX1 + 0.025)):   # the vault's end arches, closed with a painted tympanum
    pts = [V(x, yy, zz) for yy, zz in arc]
    levha(y, pts, 'kobalt', V(sx, 0), 0.002)
    oc = V(x + sx * 0.0035, CY_, PZ + RV * 0.4)
    y.yuz_yon([oc + V(0, 0.022 * math.cos(TAU * j / 10), 0.022 * math.sin(TAU * j / 10)) for j in range(10)], 'altin', V(sx, 0))
for i in range(ns):
    xa, xb = LX0 - 0.025 + (LX1 - LX0 + 0.05) * i / ns, LX0 - 0.025 + (LX1 - LX0 + 0.05) * (i + 1) / ns
    levha(y, [V(xa, LY0 - 0.01, PZ + 0.004), V(xb, LY0 - 0.01, PZ + 0.004), V((xa + xb) / 2, LY0 - 0.01, PZ - 0.026)], 'altin' if i % 2 else 'boya_kirmizi', -Y, 0.0012)
ZV = PZ + RV * 0.9
# a crown finial and the royal banner
donel(y, (0, CY_), [(0.0, ZV - 0.004), (0.02, ZV), (0.022, ZV + 0.01), (0.016, ZV + 0.016), (0.0, ZV + 0.016)], 'altin', n=12)
for j in range(6):
    a = TAU * j / 6
    y.koni((0.018 * math.cos(a), CY_ + 0.018 * math.sin(a)), 0.005, ZV + 0.016, 0.018, 'altin', n=5)
y.bolum('Sancak')
sancak(y, 0.0, CY_, ZV + 0.02, boy=0.18, en=0.12, yuk=0.07, aci=-math.pi * 0.2)
# the king and queen on their thrones, courtiers
for x, key, sap in ((-0.04, 'kobalt', 'altin'), (0.04, 'boya_kirmizi', 'altin')):
    kutu_merkez(y, (x, LY1 - 0.07), 0.04, 0.035, 0.028, 'altin', z0=LZ)
    kutu_merkez(y, (x, LY1 - 0.052), 0.04, 0.006, 0.075, 'altin', z0=LZ)
    oturan(y, x, LY1 - 0.08, LZ + 0.028, key, aci=-math.pi / 2, s=1.25)
    donel(y, (x + 0.001, LY1 - 0.08), [(0.0062, LZ + 0.028 + 0.031), (0.0062, LZ + 0.028 + 0.038), (0.0, LZ + 0.028 + 0.038)], 'altin', n=6)
for k, x in enumerate((-0.17, -0.12, 0.12, 0.17)):
    insan(y, x, LY1 - 0.07 - 0.03 * (k % 2), LZ, ['boya_yesil', 'beyaz', 'boya_sari', 'kirmizi'][k], aci=-math.pi / 2, kol=0.5 if k == 1 else 0.0)

# ---------------------------------------------------------------- the knights' camps
y.bolum('Şövalye çadırları')


def pavyon(cx, cy, r, h, renk, serit, flama=None):
    """a knight's round pavilion: striped cone with a scalloped skirt, a door flap, the pole's pennant"""
    cadir(y, (cx, cy), r, h, renk, serit, n=16, ip=True)
    for i in range(16):
        a0, a1 = TAU * i / 16, TAU * (i + 1) / 16
        p0, p1 = V(cx + r * 1.01 * math.cos(a0), cy + r * 1.01 * math.sin(a0)), V(cx + r * 1.01 * math.cos(a1), cy + r * 1.01 * math.sin(a1))
        m = (p0 + p1) / 2
        d = (m - V(cx, cy)).normalized()
        levha(y, [p0 + Z * (h * 0.15), p1 + Z * (h * 0.15), m + d * 0.002 + Z * (h * 0.15 - 0.016)], serit if i % 2 else renk, d, 0.0012)
    # the open door flap towards the lists
    d = V(0, 1)
    o = V(cx, cy) + d * (r * 1.005)
    ot = V(cx, cy) + d * (r * 0.83)
    levha(y, [o + V(-0.02, 0, 0.0), o + V(0.02, 0, 0.0), ot + V(0.011, 0.003, h * 0.3), ot + V(-0.011, 0.003, h * 0.3)], 'koyu', d + Z * 0.3, 0.0012)
    levha(y, [o + V(0.02, 0.003, 0), o + V(0.045, 0.014, 0), ot + V(0.012, 0.006, h * 0.3)], renk, V(0.2, 1, 0.3), 0.0012)
    fl = flama or renk
    levha(y, [V(cx + 0.004, cy, h + 0.03), V(cx + 0.07, cy, h + 0.018), V(cx + 0.004, cy, h + 0.006)], fl, -Y, 0.0012)


def kalkan_rafi(cx, cy, aci, renkler):
    """a rack of heater shields: two posts, a rail, the shields hung on it, facing -y locally"""
    with parca(y, (cx, cy, G), aci):
        w = 0.035 * len(renkler) + 0.02
        for s in (-1, 1):
            cubuk(y, V(s * w / 2, 0, 0), V(s * w / 2, 0, 0.085), 0.008, 'ahsap_koyu')
        cubuk(y, V(-w / 2 - 0.006, 0, 0.08), V(w / 2 + 0.006, 0, 0.08), 0.008, 'ahsap_koyu', 0.008)
        for k, kk in enumerate(renkler):
            x = -w / 2 + 0.027 + 0.035 * k
            levha(y, [V(x - 0.015, -0.006, 0.078), V(x + 0.015, -0.006, 0.078), V(x + 0.015, -0.006, 0.052), V(x, -0.006, 0.03), V(x - 0.015, -0.006, 0.052)],
                  kk, -Y, 0.0025)
            kutu3(y, V(x, -0.0098, 0.06), X, Y, Z, 0.005, 0.0012, 0.038, 'beyaz' if kk != 'beyaz' else 'boya_kirmizi')
            kutu3(y, V(x, -0.0098, 0.066), X, Y, Z, 0.024, 0.0012, 0.005, 'beyaz' if kk != 'beyaz' else 'boya_kirmizi')


def mizrak_rafi(cx, cy, aci, n=5, renk='boya_kirmizi'):
    """a lance rack: a trestle with lances leaning on it"""
    with parca(y, (cx, cy, G), aci):
        for s in (-1, 1):
            cubuk(y, V(s * 0.04, 0, 0), V(s * 0.04, 0.012, 0.06), 0.007, 'ahsap_koyu')
        cubuk(y, V(-0.05, 0.01, 0.058), V(0.05, 0.01, 0.058), 0.007, 'ahsap_koyu', 0.007)
        for k in range(n):
            x = -0.035 + 0.07 * k / (n - 1)
            boru(y, [V(x, -0.04, 0.0), V(x, 0.03, 0.2)], 0.0035, renk if k % 2 else 'beyaz', n=5, r_son=0.002)


# the red camp (left) and the blue camp (right), before the lists
for (cx, cy, r, h, a, b) in ((-0.82, -0.62, 0.1, 0.24, 'boya_kirmizi', 'beyaz'), (-0.56, -0.8, 0.085, 0.21, 'boya_sari', 'boya_kirmizi'),
                              (-0.36, -0.6, 0.075, 0.19, 'beyaz', 'boya_kirmizi')):
    pavyon(cx, cy, r, h, a, b, 'boya_kirmizi')
for (cx, cy, r, h, a, b) in ((0.82, -0.62, 0.1, 0.24, 'kobalt', 'beyaz'), (0.56, -0.8, 0.085, 0.21, 'boya_sari', 'kobalt'),
                              (0.36, -0.6, 0.075, 0.19, 'beyaz', 'boya_yesil')):
    pavyon(cx, cy, r, h, a, b, 'kobalt')
kalkan_rafi(-0.62, -0.47, 0.0, ['boya_kirmizi', 'boya_sari', 'beyaz', 'boya_kirmizi'])
kalkan_rafi(0.62, -0.47, 0.0, ['kobalt', 'beyaz', 'boya_yesil', 'kobalt'])
mizrak_rafi(-0.95, -0.4, 0.3, renk='boya_kirmizi')
mizrak_rafi(0.95, -0.4, -0.3, renk='kobalt')
# waiting knights and squires, tethered horses
sovalye(y, -0.2, -0.47, G, 0.3, 1.1, 'boya_sari', 'boya_kirmizi', 'boya_sari', mizrak=True, kosu=0.0, sorguc='boya_kirmizi', mizrak_egim=0.09, dokum=True)
sovalye(y, 0.22, -0.48, G, math.pi - 0.3, 1.1, 'boya_yesil', 'beyaz', 'boya_yesil', mizrak=True, kosu=0.0, mizrak_egim=0.09, dokum=True)
at(y, -0.9, -0.82, G, 0.8, 1.1, 'koyu', 'koyu', cul='boya_kirmizi', cul2='beyaz', dokum=True)
at(y, 0.92, -0.86, G, 2.4, 1.1, 'beyaz', 'granit', cul='kobalt', cul2='boya_sari', dokum=True)
for k, (x, yy, key, a, kol) in enumerate(((-0.45, -0.5, 'kumas', 0.4, 0.0), (-0.7, -0.88, 'boya_kirmizi', 1.0, 0.6), (0.45, -0.5, 'kumas', 2.6, 0.0),
                                          (0.7, -0.9, 'kobalt', 2.0, 0.4), (-0.12, -0.85, 'ahsap_acik', 1.5, 0.0), (0.12, -0.7, 'boya_yesil', 1.7, 0.0))):
    insan(y, x, yy, G, key, aci=a, kol=kol)
# the standing crowd along the near fence
renk_k = ['boya_kirmizi', 'boya_yesil', 'kumas', 'boya_sari', 'ahsap_acik', 'beyaz', 'kirmizi']
for j in range(26):
    x = FX0 + 0.05 + (FX1 - FX0 - 0.1) * j / 25
    if abs(x) < 0.1: continue
    insan(y, x + 0.008 * ((j * 7) % 3 - 1), FY0 - 0.035 - 0.02 * (j % 2), G, renk_k[(j * 3) % len(renk_k)], aci=math.pi / 2, kol=0.7 if j % 4 == 0 else 0.0,
          sapka='saz' if j % 5 == 2 else None)

# ---------------------------------------------------------------- the castle behind
y.bolum('Arkadaki kale: sur, yuvarlak kule, kare kule')
WY_ = 0.86
for xa_, xb_ in ((-1.06, -0.11), (0.11, 1.06)):
    sur(y, [V(xb_, WY_), V(xa_, WY_)], G, 0.2, 0.06, 'granit', mazgal_h=0.03, parapet_h=0.014, ust_key='zemin', konsol=True)
tip_k = kule_yuvarlak(y, (0.78, WY_ - 0.01), 0.15, G, 0.62, 'granit', 'konik', 'arduvaz', cati_h=0.34, yarik_say=3, bolum=4)
kule_kare(y, -0.78, WY_ - 0.01, 0.2, G, 0.4, 'granit', 'piramit', 'arduvaz', cati_h=0.18, yarik_say=2)
sancak(y, 0.78, WY_ - 0.01, tip_k - 0.01, boy=0.13, en=0.1, yuk=0.06, aci=-math.pi * 0.3)
kale_kapisi(y, 0.0, WY_ - 0.03, 0.22, G, 0.2, derin=0.12, key='granit', kule='yuvarlak', kule_r=0.05, kule_h=0.3, cati='konik', cati_key='arduvaz')

y.bolum('Ağaçlar')
for (tx, ty, tb, tt) in ((-1.03, -0.15, 0.18, 'yaprakli'), (-1.03, 0.1, 0.16, 'yaprakli'), (1.03, -0.15, 0.17, 'yaprakli'), (1.03, 0.12, 0.18, 'yaprakli'),
                         (-1.04, -0.93, 0.14, 'yaprakli'), (1.04, -0.95, 0.14, 'yaprakli'), (-0.25, -0.93, 0.13, 'yaprakli'), (0.27, -0.94, 0.13, 'yaprakli'),
                         (-1.04, 0.62, 0.2, 'servi'), (1.04, 0.6, 0.2, 'servi')):
    agac(y, tx, ty, G, boy=tb, tur=tt, key='boya_yesil' if tx < 0 else 'zeytin')

calistir(y, 'lm_turnuva')
