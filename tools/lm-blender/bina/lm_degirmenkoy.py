# Değirmen Köyü (lm_degirmenkoy): a Frankish mill village. A stream crosses the front with a stone weir; a timber
# mill race on trestles carries water from the pond above the weir onto the overshot wheel of a stone-and-timber
# water mill. Behind: half-timbered thatched houses round a green with a well and a lime tree, a great barn, a
# Romanesque church with a west tower and spire, strip fields with stooks, and a post mill on its mound (the
# silhouette: the sails).
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ortak import *
from bina_ortak import calistir

import doku

y = Yapi()

G = 0.05                      # ground top
doku.KOSE_RENK['cimen'] = cayir_renk(G)
XA, XB = -1.2, 1.2
YA, YB = -1.05, 1.0
YS0, YS1 = -0.84, -0.56       # the stream's banks
XW = -0.98                    # the weir
ZW1, ZW = 0.032, 0.016        # water above / below the weir

# ---------------------------------------------------------------- ground and stream
y.bolum('Zemin, dere ve bent')
zemin_blok(y, XA, XB, YA, YS0, G, yanlar='onsagsol')
zemin_blok(y, XA, XB, YS1, YB, G, yanlar='arkasagsol')
# the banks: stone revetment by the mill, earth elsewhere
# (bank walls facing into the channel: the south bank faces +y, the north bank -y)
for x0, x1, k in ((XA, -0.86, 'toprak'), (-0.86, -0.36, 'tas_koyu'), (-0.36, XB, 'toprak')):
    y.yuz_yon([V(x0, YS1, 0), V(x1, YS1, 0), V(x1, YS1, G), V(x0, YS1, G)], k, -Y)
y.yuz_yon([V(XA, YS0, 0), V(XB, YS0, 0), V(XB, YS0, G), V(XA, YS0, G)], 'toprak', Y)
# water: the pond above the weir and the stream below it
y.yuz_yon([V(XA, YS0, ZW1), V(XW - 0.02, YS0, ZW1), V(XW - 0.02, YS1, ZW1), V(XA, YS1, ZW1)], 'su', Z)
y.yuz_yon([V(XW + 0.02, YS0, ZW), V(XB, YS0, ZW), V(XB, YS1, ZW), V(XW + 0.02, YS1, ZW)], 'su', Z)
for x, zz in ((XA, ZW1), (XB, ZW)):
    y.yuz_yon([V(x, YS0, 0), V(x, YS1, 0), V(x, YS1, zz), V(x, YS0, zz)], 'toprak', V(1 if x > 0 else -1, 0))
# the weir: a stone sill across the stream, water spilling over it
kutu(y, V(XW - 0.02, YS0, 0), X, 0.04, YS1 - YS0, ZW1 + 0.006, 'tas_koyu', 'onarkasagsolust')
for k in range(9):
    yy = YS0 + 0.015 + (YS1 - YS0 - 0.03) * k / 8
    y.yuz_yon([V(p.x, p.y, ZW + 0.002) for p in cokgen((XW + 0.032 + 0.01 * (k % 2), yy), 0.011, 6, 0.3 * k)], 'beyaz', Z)
for k in range(6):
    yy = YS0 + 0.03 + (YS1 - YS0 - 0.06) * k / 5
    kutu_merkez(y, (XW + 0.002, yy), 0.03, 0.04, 0.008, 'tas', z0=ZW1 + 0.004, aci=0.15 * k)
# stones along the banks
for k, (x, yy) in enumerate(((-0.3, YS0 + 0.012), (0.02, YS1 - 0.012), (0.42, YS0 + 0.015), (0.7, YS1 - 0.014), (0.95, YS0 + 0.01),
                            (-1.12, YS1 - 0.012), (-0.2, YS0 + 0.01), (1.1, YS1 - 0.01))):
    kutu_merkez(y, (x, yy), 0.04 + 0.01 * (k % 3), 0.028, 0.03 + 0.008 * (k % 2), 'granit' if k % 2 else 'granit_koyu', z0=ZW - 0.01, aci=0.5 * k)

# ---------------------------------------------------------------- the water mill
y.bolum('Su değirmeni: taş bina')
MX0, MX1, MY0, MY1 = -0.82, -0.42, -0.52, -0.28
zm1 = G + 0.15                 # the stone storey's top
zm2 = zm1 + 0.11               # the timber storey's top
kutu(y, V(MX0 - 0.01, MY0 - 0.01, G - 0.01), X, MX1 - MX0 + 0.02, MY1 - MY0 + 0.02, 0.02, 'granit_koyu', 'onarkasagsolust')
mk = dikdortgen(MX0, MX1, MY0, MY1)
z0 = G + 0.01
for i in range(4):
    a, b = mk[i], mk[(i + 1) % 4]
    L = (b - a).length
    if i == 1:   # east side: the door and a window
        dikdortgen_acik(y, a, a.lerp(b, 0.5), z0, zm1 - z0, 0.3, 0.7, 0.0, (zm1 - z0) * 0.72, ('granit', 'tas_koyu', 'tas_acik', 'ahsap_dikey'),
                        derin=0.016, cerceve=(0.007, 'kirec'))
        dikdortgen_acik(y, a.lerp(b, 0.5), b, z0, zm1 - z0, 0.35, 0.65, (zm1 - z0) * 0.4, (zm1 - z0) * 0.75, ('granit', 'tas_koyu', 'tas_acik', 'koyu'),
                        derin=0.016, cerceve=(0.006, 'kirec'))
    elif i == 0:   # the wheel side: a small window either side of the axle
        dikdortgen_acik(y, a, a.lerp(b, 0.25), z0, zm1 - z0, 0.3, 0.7, (zm1 - z0) * 0.45, (zm1 - z0) * 0.78, ('granit', 'tas_koyu', 'tas_acik', 'koyu'),
                        derin=0.016, cerceve=(0.006, 'kirec'))
        duz_duvar(y, a.lerp(b, 0.25), a.lerp(b, 0.75), z0, zm1, 'granit')
        dikdortgen_acik(y, a.lerp(b, 0.75), b, z0, zm1 - z0, 0.3, 0.7, (zm1 - z0) * 0.45, (zm1 - z0) * 0.78, ('granit', 'tas_koyu', 'tas_acik', 'koyu'),
                        derin=0.016, cerceve=(0.006, 'kirec'))
    else:
        n = max(1, int(round(L / 0.13)))
        for j in range(n):
            p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
            if j % 2 == (0 if n > 2 else 1):
                dikdortgen_acik(y, p, q, z0, zm1 - z0, 0.36, 0.64, (zm1 - z0) * 0.45, (zm1 - z0) * 0.78, ('granit', 'tas_koyu', 'tas_acik', 'koyu'),
                                derin=0.016, cerceve=(0.006, 'kirec'))
            else:
                duz_duvar(y, p, q, z0, zm1, 'granit')
# quoins
for p in mk:
    for j in range(int((zm1 - z0) / 0.03)):
        s = 0.022 if j % 2 == 0 else 0.015
        kutu_merkez(y, (p.x, p.y), s, s, 0.018, 'kirec', z0=z0 + j * 0.03 + 0.004)
silme(y, mk, zm1 - 0.006, 0.01, 0.008, 'kirec', 'duz')
y.bolum('Su değirmeni: yarı ahşap kat ve çatı')
J = 0.014   # the jetty: the timber storey overhangs the stone one
jk = disa(mk, J)
for i in range(4):
    j_ = (i + 1) % 4
    y.yuz_yon([V(mk[i].x, mk[i].y, zm1 + 0.004), V(mk[j_].x, mk[j_].y, zm1 + 0.004), V(jk[j_].x, jk[j_].y, zm1 + 0.004), V(jk[i].x, jk[i].y, zm1 + 0.004)], 'ahsap_koyu', -Z)
    a, b = jk[i], jk[j_]
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    n = max(2, int(round(L / 0.1)))
    bos = []
    for j in range(n):
        if (i in (0, 2) and j % 2 == 1) or (i in (1, 3) and j == n // 2):
            u0, u1 = (j + 0.3) / n, (j + 0.7) / n
            bos.append((u0, u1))
    u = 0.0
    for u0, u1 in bos:
        duz_duvar(y, a.lerp(b, u), a.lerp(b, u0 - 0.008 / L), zm1 + 0.004, zm2, 'siva_krem')
        dikdortgen_acik(y, a.lerp(b, u0 - 0.008 / L), a.lerp(b, u1 + 0.008 / L), zm1 + 0.004, zm2 - zm1 - 0.004, 0.2, 0.8, 0.035, 0.085,
                        ('siva_krem', 'ahsap_koyu', 'ahsap_acik', 'koyu'), derin=0.008)
        u = u1 + 0.008 / L
    duz_duvar(y, a.lerp(b, u), b, zm1 + 0.004, zm2, 'siva_krem')
    yari_ahsap(y, a, b, zm1 + 0.004, zm2, [(u0 - 0.004 / L, u1 + 0.004 / L, 0.03, 0.09) for u0, u1 in bos], 'ahsap_koyu', aralik=0.04)
    # the jetty's beam ends
    for j in range(int(L / 0.035) + 1):
        p = a.lerp(b, (j + 0.5) / (int(L / 0.035) + 1)) - nc * (J * 0.5)
        kutu3(y, p + Z * (zm1 - 0.004), nc, e, Z, J + 0.006, 0.008, 0.008, 'ahsap_koyu')
xs = [p.x for p in jk]; ys = [p.y for p in jk]
rz = cati_besik(y, min(xs), max(xs), min(ys), max(ys), zm2, 0.16, 0.03, 'kiremit', 'kiremit2', ucluk_key='siva_krem', alt_key='ahsap_koyu',
                ns=8, nr=6, uc_sacak=0.02)
for sx in (-1, 1):   # gable timbers and a hoist door with its beam on the east gable
    xg = (MX1 + J + 0.003) if sx > 0 else (MX0 - J - 0.003)
    cubuk(y, V(xg, (MY0 + MY1) / 2, zm2), V(xg, (MY0 + MY1) / 2, zm2 + 0.15), 0.007, 'ahsap_koyu', 0.004)
    for s2 in (-1, 1):
        cubuk(y, V(xg, (MY0 + MY1) / 2 + s2 * 0.12, zm2 + 0.004), V(xg, (MY0 + MY1) / 2, zm2 + 0.09), 0.006, 'ahsap_koyu', 0.004)
xg = MX1 + J + 0.004
y.yuz_yon([V(xg, -0.43, zm2 + 0.02), V(xg, -0.37, zm2 + 0.02), V(xg, -0.37, zm2 + 0.075), V(xg, -0.43, zm2 + 0.075)], 'ahsap_dikey', X)
cubuk(y, V(MX1 + J - 0.01, -0.4, zm2 + 0.1), V(MX1 + J + 0.07, -0.4, zm2 + 0.1), 0.01, 'ahsap_koyu')
boru(y, [V(MX1 + J + 0.062, -0.4, zm2 + 0.094), V(MX1 + J + 0.062, -0.4, zm2 + 0.03)], 0.0018, 'ahsap_acik', n=4)
kutu_merkez(y, (MX1 + J + 0.062, -0.4), 0.02, 0.02, 0.018, 'kumas', z0=zm2 + 0.012)
# a chimney
kutu_merkez(y, (MX0 + 0.08, (MY0 + MY1) / 2 + 0.05), 0.035, 0.035, 0.2, 'granit', z0=zm2 + 0.02)
kutu_merkez(y, (MX0 + 0.08, (MY0 + MY1) / 2 + 0.05), 0.042, 0.042, 0.01, 'kirec', z0=zm2 + 0.22)
# sacks and a millstone leaning by the door
for k, (xx, yy) in enumerate(((MX1 + 0.04, -0.47), (MX1 + 0.06, -0.445), (MX1 + 0.045, -0.425))):
    donel(y, (xx, yy), [(0.0, G), (0.013, G + 0.004), (0.012, G + 0.02), (0.005, G + 0.03), (0.0, G + 0.031)], 'kumas', n=8)
boru(y, [V(MX1 + 0.02, -0.33, G + 0.035), V(MX1 + 0.034, -0.33, G + 0.035)], 0.035, 'granit', n=14)

y.bolum('Su çarkı ve savak kanalı')
WX, WY, WZ, WR = -0.6, -0.70, 0.152, 0.152
WB = 0.07   # wheel width
for s in (-1, 1):   # two rims of segments, eight spokes each
    yy = WY + s * WB / 2
    n = 20
    pts = [V(WX + WR * math.cos(TAU * i / n), yy, WZ + WR * math.sin(TAU * i / n)) for i in range(n)]
    for i in range(n):
        cubuk(y, pts[i], pts[(i + 1) % n] + (pts[(i + 1) % n] - pts[i]) * 0.04, 0.012, 'ahsap', 0.016)
    pts2 = [V(WX + WR * 0.72 * math.cos(TAU * i / n), yy, WZ + WR * 0.72 * math.sin(TAU * i / n)) for i in range(n)]
    for i in range(n):
        cubuk(y, pts2[i], pts2[(i + 1) % n] + (pts2[(i + 1) % n] - pts2[i]) * 0.04, 0.008, 'ahsap_koyu', 0.008)
    for i in range(8):
        a_ = TAU * i / 8 + 0.2
        cubuk(y, V(WX, yy, WZ), V(WX + WR * math.cos(a_), yy, WZ + WR * math.sin(a_)), 0.01, 'ahsap_koyu', 0.008)
# buckets: boards between the rims, slanted
for i in range(20):
    a_ = TAU * (i + 0.5) / 20
    d = V(math.cos(a_), 0, math.sin(a_)); t = V(-math.sin(a_), 0, math.cos(a_))
    c = V(WX, WY, WZ) + d * (WR * 0.86)
    kutu3(y, c, (d + t * 0.6).normalized(), Y, (d + t * 0.6).normalized().cross(Y), WR * 0.3, WB, 0.005, 'ahsap_acik')
# hub and the axle into the mill
boru(y, [V(WX, WY - WB / 2 - 0.012, WZ), V(WX, WY + WB / 2 + 0.012, WZ)], 0.024, 'ahsap_koyu', n=10)
boru(y, [V(WX, WY + WB / 2, WZ), V(WX, MY0 + 0.01, WZ)], 0.011, 'kutuk', n=8)
boru(y, [V(WX, MY0 - 0.006, WZ), V(WX, MY0 + 0.002, WZ)], 0.022, 'demir', n=10)
# the pier on the far side carrying the axle's outer bearing
kutu_merkez(y, (WX, WY - WB / 2 - 0.036), 0.036, 0.026, WZ - 0.01 - ZW + 0.012, 'granit_koyu', z0=ZW - 0.012)
kutu_merkez(y, (WX, WY - WB / 2 - 0.036), 0.044, 0.032, 0.008, 'ahsap_koyu', z0=WZ - 0.012)
boru(y, [V(WX, WY - WB / 2 - 0.05, WZ), V(WX, WY - WB / 2, WZ)], 0.008, 'kutuk', n=8)
# water churned white under the wheel
for k in range(7):
    y.yuz_yon([V(p.x, p.y, ZW + 0.002) for p in cokgen((WX - 0.1 + 0.034 * k, WY + 0.012 * ((k % 3) - 1)), 0.016 + 0.004 * (k % 2), 6, 0.5 * k)], 'beyaz', Z)

# the race: a timber trough on trestles from the pond above the weir to the wheel's top
TZ = WZ + WR + 0.022          # trough floor
TX0, TX1 = XA + 0.03, WX + 0.02
TW = 0.064
kutu3(y, V((TX0 + TX1) / 2, WY, TZ - 0.004), X, Y, Z, TX1 - TX0, TW, 0.008, 'ahsap')
for s in (-1, 1):
    kutu3(y, V((TX0 + TX1) / 2, WY + s * (TW / 2 - 0.004), TZ + 0.016), X, Y, Z, TX1 - TX0, 0.008, 0.032, 'ahsap')
y.yuz_yon([V(TX0, WY - TW / 2 + 0.008, TZ + 0.024), V(TX1, WY - TW / 2 + 0.008, TZ + 0.024), V(TX1, WY + TW / 2 - 0.008, TZ + 0.024),
           V(TX0, WY + TW / 2 - 0.008, TZ + 0.024)], 'su', Z)
kutu3(y, V(TX0 + 0.004, WY, TZ + 0.016), X, Y, Z, 0.008, TW - 0.016, 0.032, 'ahsap')   # the upstream end, closed by the sluice board
# battens round the trough
for k in range(int((TX1 - TX0) / 0.06) + 1):
    x = TX0 + 0.02 + k * 0.06
    if x > TX1 - 0.01: break
    for s in (-1, 1):
        kutu3(y, V(x, WY + s * (TW / 2 + 0.003), TZ + 0.014), X, Y, Z, 0.008, 0.006, 0.04, 'ahsap_koyu')
    kutu3(y, V(x, WY, TZ - 0.011), X, Y, Z, 0.008, TW + 0.012, 0.006, 'ahsap_koyu')
# the water falling from the trough's end onto the buckets
fall = [V(TX1 + 0.002, WY, TZ + 0.022), V(TX1 + 0.018, WY, TZ + 0.012), V(TX1 + 0.026, WY, TZ - 0.012), V(TX1 + 0.03, WY, TZ - 0.03)]
for k in range(3):
    p, q = fall[k], fall[k + 1]
    levha(y, [p + V(0, -0.024, 0), q + V(0, -0.024, 0), q + V(0, 0.024, 0), p + V(0, 0.024, 0)], 'su', V(q.z - p.z, 0, p.x - q.x) * -1 + V(0.2, 0, 1))
# trestles: pairs of posts with a cross beam and a brace
for x in (-1.12, -0.96, -0.8, -0.68):
    zb = ZW1 if x < XW else ZW
    for s in (-1, 1):
        cubuk(y, V(x, WY + s * 0.04, zb - 0.01), V(x, WY + s * 0.04, TZ - 0.008), 0.012, 'kutuk', 0.012)
    cubuk(y, V(x, WY - 0.05, TZ - 0.014), V(x, WY + 0.05, TZ - 0.014), 0.012, 'ahsap_koyu', 0.012)
    cubuk(y, V(x, WY - 0.04, zb + 0.02), V(x, WY + 0.04, TZ - 0.03), 0.007, 'ahsap_koyu', 0.006)
# the sluice gate at the head of the race: two posts, a lintel, the gate board and its winch
SX = TX0 + 0.03
for s in (-1, 1):
    cubuk(y, V(SX, WY + s * (TW / 2 + 0.008), ZW1 - 0.01), V(SX, WY + s * (TW / 2 + 0.008), TZ + 0.11), 0.014, 'ahsap_koyu', 0.014)
cubuk(y, V(SX, WY - TW / 2 - 0.02, TZ + 0.1), V(SX, WY + TW / 2 + 0.02, TZ + 0.1), 0.014, 'ahsap_koyu', 0.016)
kutu3(y, V(SX, WY, TZ + 0.045), X, Y, Z, 0.008, TW - 0.004, 0.05, 'ahsap_acik')
cubuk(y, V(SX, WY, TZ + 0.07), V(SX, WY, TZ + 0.1), 0.006, 'demir')
boru(y, [V(SX - 0.012, WY, TZ + 0.118), V(SX + 0.012, WY, TZ + 0.118)], 0.018, 'ahsap', n=10)

# ---------------------------------------------------------------- the bridge and the roads
y.bolum('Köprü ve yollar')
BX = 0.12
for s in (-1, 1):
    for yy in (YS0 + 0.05, (YS0 + YS1) / 2, YS1 - 0.05):
        y.prizma((BX + s * 0.06, yy), 0.008, ZW - 0.01, G + 0.02, 'kutuk', n=6)
for k in range(12):   # deck planks across the road
    yy = YS0 - 0.03 + (YS1 - YS0 + 0.06) * (k + 0.5) / 12
    kutu3(y, V(BX, yy, G + 0.024), X, Y, Z, 0.15, (YS1 - YS0 + 0.06) / 12 - 0.002, 0.008, 'ahsap' if k % 3 else 'ahsap_acik')
for s in (-1, 1):
    cubuk(y, V(BX + s * 0.068, YS0 - 0.03, G + 0.024), V(BX + s * 0.068, YS1 + 0.03, G + 0.024), 0.01, 'ahsap_koyu', 0.014)
    for yy in (YS0 - 0.02, YS0 + 0.08, YS1 - 0.08, YS1 + 0.02):
        cubuk(y, V(BX + s * 0.07, yy, G + 0.028), V(BX + s * 0.07, yy, G + 0.075), 0.008, 'ahsap_koyu')
    cubuk(y, V(BX + s * 0.07, YS0 - 0.02, G + 0.072), V(BX + s * 0.07, YS1 + 0.02, G + 0.072), 0.007, 'ahsap', 0.007)


def yol(pts, en, key='toprak', dz=0.0025):
    """a dirt road along a polyline: a flat ribbon a hair above the ground"""
    pts = [V(p[0], p[1]) for p in pts]
    sol = disa(pts, -en / 2, False); sag = disa(pts, en / 2, False)
    for i in range(len(pts) - 1):
        y.yuz_yon([sag[i] + Z * (G + dz), sag[i + 1] + Z * (G + dz), sol[i + 1] + Z * (G + dz), sol[i] + Z * (G + dz)], key, Z)


yol([(BX, YA + 0.002), (BX, YS0 - 0.03)], 0.13)
yol([(BX, YS1 + 0.03), (BX, -0.42), (0.0, -0.12), (-0.05, 0.12), (0.12, 0.34), (0.4, 0.42)], 0.1)
yol([(XA + 0.002, -0.95), (BX - 0.065, -0.95)], 0.08)
yol([(BX + 0.065, -0.95), (XB - 0.002, -0.92)], 0.08)
yol([(0.1, -0.47), (MX1 + 0.01, -0.46)], 0.06, dz=0.0045)

# ---------------------------------------------------------------- the village
y.bolum('Köy evleri')
ev(y, -0.2, -0.35, G, 0.2, 0.12, 0.1, 0.0, 'saz', tohum=0)
ev(y, -0.44, 0.0, G, 0.21, 0.13, 0.1, -math.pi / 2, 'saz', tohum=1, kapi_u=0.4)
ev(y, 0.15, -0.18, G, 0.18, 0.12, 0.095, math.pi / 2 + 0.15, 'kiremit', tohum=2)
ev(y, 0.32, 0.17, G, 0.19, 0.12, 0.1, math.pi + 0.1, 'saz', tohum=3, kapi_u=0.6)
ev(y, -0.42, 0.42, G, 0.18, 0.12, 0.095, -math.pi / 2 - 0.1, 'kiremit', tohum=4)
ev(y, 0.05, 0.78, G, 0.17, 0.11, 0.09, math.pi + 0.05, 'saz', tohum=5)
ev(y, -0.6, 0.86, G, 0.17, 0.11, 0.09, math.pi, 'saz', tohum=6)
y.bolum('Ambar')
ambar(y, -0.1, 0.45, G, 0.34, 0.2, 0.13, 0.0, 'saz', cati_h=0.17)

y.bolum('Köy meydanı: kuyu, ıhlamur, araba, köylüler')
# the well: a round stone curb, two posts, a little roof, a bucket
KX, KY = -0.07, -0.06
donel(y, (KX, KY), [(0.034, G), (0.034, G + 0.04), (0.026, G + 0.04), (0.026, G + 0.03)], 'granit', n=14)
y.yuz_yon([V(p.x, p.y, G + 0.03) for p in cokgen((KX, KY), 0.026, 14)], 'su', Z)
for s in (-1, 1):
    cubuk(y, V(KX + s * 0.03, KY, G + 0.03), V(KX + s * 0.03, KY, G + 0.1), 0.007, 'ahsap_koyu')
boru(y, [V(KX - 0.034, KY, G + 0.085), V(KX + 0.034, KY, G + 0.085)], 0.005, 'ahsap', n=6)
cati_besik(y, KX - 0.045, KX + 0.045, KY - 0.035, KY + 0.035, G + 0.1, 0.035, 0.008, 'saz', 'saz_koyu', ucluk_key='ahsap_dikey', ns=3, nr=3,
           uc_sacak=0.006, mahya_en=0.008)
y.prizma((KX + 0.01, KY), 0.008, G + 0.05, G + 0.064, 'ahsap', n=8)
# the lime tree on the green
kure(y, (0.12, 0.05, G + 0.2), 0.09, 'boya_yesil', n=12, kat=6)
kure(y, (0.07, 0.09, G + 0.15), 0.06, 'yesil_koyu', n=10, kat=5)
kure(y, (0.17, 0.0, G + 0.14), 0.055, 'zeytin', n=10, kat=5)
boru(y, [V(0.12, 0.05, G), V(0.12, 0.05, G + 0.12)], 0.014, 'ahsap_koyu', n=8)
donel(y, (0.12, 0.05), [(0.045, G), (0.045, G + 0.014), (0.0, G + 0.014)], 'ahsap', n=10)   # a bench round it
# a hay cart
with parca(y, (0.0, -0.3, G), 0.5):
    kutu(y, V(-0.05, -0.025, 0.026), X, 0.1, 0.05, 0.006, 'ahsap', 'onarkasagsolust')
    for s in (-1, 1):
        kutu(y, V(-0.05, s * 0.025 - (0.004 if s > 0 else 0), 0.032), X, 0.1, 0.004, 0.014, 'ahsap_koyu', 'onarkasagsolust')
        boru(y, [V(0.0, s * 0.032, 0.022), V(0.0, s * 0.038, 0.022)], 0.022, 'ahsap_koyu', n=10)
    donel(y, (0.0, 0.0), [(0.048, 0.038), (0.05, 0.05), (0.035, 0.068), (0.0, 0.074)], 'saz', n=10)
    cubuk(y, V(0.05, 0, 0.03), V(0.12, 0, 0.004), 0.006, 'ahsap_koyu')
for (x, yy, k, a_, kol) in ((-0.02, -0.15, 'boya_kirmizi', 0.4, 0.0), (-0.12, -0.12, 'kumas', 1.6, 0.6), (0.22, -0.02, 'boya_yesil', 2.6, 0.0),
                            (-0.25, 0.12, 'ahsap_acik', 0.0, 0.0), (0.19, -0.46, 'boya_sari', 1.2, 0.0),
                            (MX1 + 0.08, -0.37, 'kumas', 3.0, 0.5), (0.13, -0.71, 'boya_kirmizi', 1.5, 0.0)):
    insan(y, x, yy, G if abs(yy + 0.71) > 0.01 else G + 0.028, k, 1.0, aci=a_, kol=kol, sapka='saz' if k == 'kumas' else None)

# ---------------------------------------------------------------- the church
y.bolum('Köy kilisesi ve mezarlık')
CX, CY = -0.86, 0.22
tip_c = koy_kilisesi(y, CX, CY, G, 0.0, 1.0, 'arduvaz', 'kirec', 'granit', kule_h=0.47, kule_cati=0.34)
# the churchyard wall
cw = [V(CX - 0.2, CY - 0.26), V(CX + 0.19, CY - 0.26), V(CX + 0.19, CY + 0.56), V(CX - 0.2, CY + 0.56)]
alcak_duvar(y, [cw[0].lerp(cw[1], 0.64), cw[1], cw[2], cw[3], cw[0], cw[0].lerp(cw[1], 0.36)], G, 0.03, 0.02, 'granit', 'kirec')
for (gx, gy) in ((-1.0, 0.36), (-1.0, 0.5), (-1.01, 0.64), (-0.72, 0.38), (-0.72, 0.52), (-0.71, 0.66), (-0.97, 0.06), (-0.75, 0.06)):
    kutu_merkez(y, (gx, gy), 0.03, 0.012, 0.012, 'granit', z0=G - 0.004)
    kutu_merkez(y, (gx, gy - 0.004), 0.006, 0.004, 0.05, 'granit_koyu', z0=G)
    kutu_merkez(y, (gx, gy - 0.004), 0.026, 0.004, 0.006, 'granit_koyu', z0=G + 0.032)
agac(y, -1.1, 0.12, G, boy=0.26, tur='servi', key='yesil_koyu')
agac(y, -0.63, 0.7, G, boy=0.22, tur='servi', key='yesil_koyu')
yol([(CX, CY - 0.17), (CX, CY - 0.3), (-0.6, -0.12), (-0.34, -0.2), (-0.02, -0.13)], 0.055, dz=0.0045)

# ---------------------------------------------------------------- fields
y.bolum('Tarla şeritleri')
FX0, FX1, FY0, FY1 = 0.36, 1.14, -0.5, 0.06
SER = ['saz', 'toprak', 'cimen', 'cimen_kuru', 'saz', 'toprak']
ns = len(SER)
for i, k in enumerate(SER):
    x0 = FX0 + (FX1 - FX0) * i / ns + 0.006
    x1 = FX0 + (FX1 - FX0) * (i + 1) / ns - 0.006
    if k == 'saz':   # standing wheat: a tall block with a ragged top
        kutu(y, V(x0, FY0, G - 0.002), X, x1 - x0, FY1 - FY0, 0.032, 'saz_koyu', 'onarkasagsol')
        y.yuz_yon([V(x0, FY0, G + 0.03), V(x1, FY0, G + 0.03), V(x1, FY1, G + 0.03), V(x0, FY1, G + 0.03)], 'saz', Z)
        for j in range(5):   # ridged rows of ears, a darker furrow between
            xx = x0 + (x1 - x0) * (j + 0.5) / 5
            w = (x1 - x0) / 5 * 0.46
            for s in (-1, 1):
                y.yuz_yon([V(xx + s * w, FY0 + 0.002, G + 0.03), V(xx + s * w, FY1 - 0.002, G + 0.03), V(xx, FY1 - 0.002, G + 0.042),
                           V(xx, FY0 + 0.002, G + 0.042)], 'boya_sari' if j % 2 else 'saz', V(s, 0, 0.9))
            for yy_, nn_ in ((FY0 + 0.002, -Y), (FY1 - 0.002, Y)):
                y.yuz_yon([V(xx - w, yy_, G + 0.03), V(xx + w, yy_, G + 0.03), V(xx, yy_, G + 0.042)], 'saz_koyu', nn_)
    elif k == 'toprak':   # ploughed: furrow ridges along the strip
        kutu(y, V(x0, FY0, G - 0.002), X, x1 - x0, FY1 - FY0, 0.006, 'toprak', 'onarkasagsolust')
        for j in range(6):
            xx = x0 + (x1 - x0) * (j + 0.5) / 6
            w = (x1 - x0) / 6 * 0.42
            for s in (-1, 1):
                y.yuz_yon([V(xx + s * w, FY0, G + 0.004), V(xx + s * w, FY1, G + 0.004), V(xx, FY1, G + 0.012), V(xx, FY0, G + 0.012)], 'kerpic_koyu', V(s, 0, 1.2))
            y.yuz_yon([V(xx - w, FY0, G + 0.004), V(xx + w, FY0, G + 0.004), V(xx, FY0, G + 0.012)], 'kerpic_koyu', -Y)
            y.yuz_yon([V(xx + w, FY1, G + 0.004), V(xx - w, FY1, G + 0.004), V(xx, FY1, G + 0.012)], 'kerpic_koyu', Y)
    elif k == 'cimen':    # young crop in rows
        kutu(y, V(x0, FY0, G - 0.002), X, x1 - x0, FY1 - FY0, 0.006, 'toprak', 'onarkasagsolust')
        for j in range(5):
            xx = x0 + (x1 - x0) * (j + 0.5) / 5
            cubuk(y, V(xx, FY0 + 0.006, G + 0.008), V(xx, FY1 - 0.006, G + 0.008), 0.014, 'boya_yesil', 0.012)
    else:                 # harvested stubble with stooks
        kutu(y, V(x0, FY0, G - 0.002), X, x1 - x0, FY1 - FY0, 0.007, 'cimen_kuru', 'onarkasagsolust')
        for j in range(4):
            for m in (0.3, 0.7):
                cx_, cy_ = x0 + (x1 - x0) * m, FY0 + (FY1 - FY0) * (j + 0.5) / 4
                donel(y, (cx_, cy_), [(0.016, G + 0.005), (0.014, G + 0.02), (0.006, G + 0.04), (0.0, G + 0.046)], 'saz', n=7)
# a post-and-rail fence round the fields (a gap on the road side)
fe = [V(FX0 - 0.03, FY0 - 0.03), V(FX1 + 0.03, FY0 - 0.03), V(FX1 + 0.03, FY1 + 0.03), V(FX0 - 0.03, FY1 + 0.03)]
for i in range(4):
    a, b = fe[i], fe[(i + 1) % 4]
    if i == 3: b = a.lerp(b, 0.7)
    L = (b - a).length
    n = max(1, int(L / 0.08))
    for j in range(n + 1):
        p = a.lerp(b, j / n)
        cubuk(y, p + Z * (G - 0.005), p + Z * (G + 0.05), 0.007, 'ahsap_koyu')
    for zz in (G + 0.022, G + 0.042):
        cubuk(y, a + Z * zz, b + Z * zz, 0.005, 'ahsap', 0.005)
# reapers and a scarecrow
insan(y, 0.62, -0.3, G + 0.006, 'kumas', aci=0.4, kol=0.4, sapka='saz')
insan(y, 0.66, -0.12, G + 0.006, 'boya_kirmizi', aci=2.0, kol=0.0)
cubuk(y, V(0.95, -0.2, G), V(0.95, -0.2, G + 0.1), 0.006, 'ahsap_koyu')
cubuk(y, V(0.92, -0.2, G + 0.075), V(0.98, -0.2, G + 0.075), 0.005, 'ahsap_koyu')
kure(y, (0.95, -0.2, G + 0.1), 0.01, 'saz', n=6, kat=3)
donel(y, (0.95, -0.2), [(0.0, G + 0.04), (0.012, G + 0.045), (0.01, G + 0.08), (0.0, G + 0.085)], 'boya_kirmizi', n=6)
# hay stacks beside the fields and across the stream
for (hx, hy, hs) in ((0.3, 0.0, 1.0), (1.0, 0.3, 1.2), (0.62, -0.95, 1.1), (0.85, -0.93, 0.9), (-0.55, -0.95, 1.0)):
    donel(y, (hx, hy), [(0.045 * hs, G), (0.048 * hs, G + 0.03 * hs), (0.035 * hs, G + 0.07 * hs), (0.012 * hs, G + 0.095 * hs), (0.0, G + 0.1 * hs)],
          'saz', n=12, dilim=['saz', 'saz_koyu'])
    y.prizma((hx, hy), 0.003, G + 0.095 * hs, G + 0.12 * hs, 'ahsap_koyu', n=4)

# ---------------------------------------------------------------- the post mill
y.bolum('Yel değirmeni: tepe ve ayaklar')
YX, YY = 0.72, 0.56
ZH = G + 0.13                 # the mound's top
HPROF = [(0.38, G), (0.34, G + 0.03), (0.26, G + 0.09), (0.18, ZH - 0.006), (0.12, ZH), (0.0, ZH)]
donel(y, (YX, YY), HPROF, 'cimen', n=28)


def hm(r):
    """the mound's height at radius r"""
    for (r0, z0), (r1, z1) in zip(HPROF, HPROF[1:]):
        if r1 <= r <= r0:
            return z0 + (z1 - z0) * (r0 - r) / (r0 - r1)
    return G if r > HPROF[0][0] else ZH
yol([(0.38, 0.41), (0.48, 0.44)], 0.08, dz=0.0045)
# the mound: a worn path up to the ladder, boulders, bramble clumps, a few sheep
for k, (a, r) in enumerate(((0.3, 0.3), (1.2, 0.26), (2.2, 0.31), (2.9, 0.24), (3.9, 0.3), (4.7, 0.27), (5.6, 0.32))):
    px, py = YX + r * math.cos(a), YY + r * math.sin(a)
    zz = hm(r)
    if k % 3 == 1:
        kutu_merkez(y, (px, py), 0.03, 0.022, 0.016, 'granit' if k % 2 else 'kaya', z0=zz - 0.008, aci=a)
    else:
        kure(y, (px, py, zz + 0.004), 0.02, 'yesil_koyu' if k % 2 else 'zeytin', n=7, kat=4)
for k, (a, r) in enumerate(((4.5, 0.28), (4.85, 0.33), (5.3, 0.25))):
    px, py = YX + r * math.cos(a), YY + r * math.sin(a)
    zz = hm(r)
    with parca(y, (px, py, zz - 0.003), a + 1.2 * k, 0.5):
        boru(y, [V(-0.014, 0, 0.042), V(0.014, 0, 0.042)], 0.017, 'beyaz', n=8)
        for xx in (-0.014, 0.014):
            kure(y, (xx, 0, 0.042), 0.017, 'beyaz', n=8, kat=4)
        kure(y, (0.036, 0, 0.05), 0.009, 'koyu', n=6, kat=3)
        for (lx, ly) in ((-0.016, -0.01), (-0.016, 0.01), (0.018, -0.01), (0.018, 0.01)):
            cubuk(y, V(lx, ly, 0.0), V(lx, ly, 0.03), 0.005, 'koyu')
YAC = -0.52                    # the mill turned to the wind: its breast faces front-left
with parca(y, (YX, YY, ZH), YAC):
    for (px, py) in ((-0.13, 0), (0.13, 0), (0, -0.13), (0, 0.13)):
        kutu_merkez(y, (px, py), 0.045, 0.045, 0.045, 'tugla', z0=-0.01)
        kutu_merkez(y, (px, py), 0.05, 0.05, 0.006, 'tas', z0=0.035)
    cubuk(y, V(-0.155, 0, 0.055), V(0.155, 0, 0.055), 0.024, 'ahsap_koyu', 0.024)
    cubuk(y, V(0, -0.155, 0.081), V(0, 0.155, 0.081), 0.024, 'ahsap_koyu', 0.024)
    for (qx, qy) in ((-0.12, 0), (0.12, 0), (0, -0.12), (0, 0.12)):
        zq = 0.067 if qx else 0.093
        cubuk(y, V(qx, qy, zq), V(qx * 0.12, qy * 0.12, 0.25), 0.016, 'ahsap', 0.016)
    y.prizma((0, 0), 0.024, 0.04, 0.3, 'kutuk', n=10)
    # the buck (body): weatherboarded box turning on the post
    BW, BD, BZ0, BZ1 = 0.17, 0.23, 0.29, 0.5
    bk = dikdortgen(-BW / 2, BW / 2, -BD / 2, BD / 2)
    y.yuz_yon([V(p.x, p.y, BZ0) for p in bk], 'ahsap_koyu', -Z)
    for i in range(4):
        a, b = bk[i], bk[(i + 1) % 4]
        nb = 7
        for j in range(nb):   # weatherboards: each course a hair proud at its foot
            za, zb_ = BZ0 + (BZ1 - BZ0) * j / nb, BZ0 + (BZ1 - BZ0) * (j + 1) / nb
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            y.yuz_yon([a + nn * 0.003 + Z * za, b + nn * 0.003 + Z * za, b + Z * zb_, a + Z * zb_], 'ahsap_acik' if j % 2 else 'ahsap', nn + Z * 0.1)
            y.yuz_yon([a + Z * za, b + Z * za, b + nn * 0.003 + Z * za, a + nn * 0.003 + Z * za], 'ahsap_koyu', -Z)
        # corner posts
        cubuk(y, V(a.x, a.y, BZ0), V(a.x, a.y, BZ1), 0.012, 'ahsap_koyu')
    for (fx, fz) in ((0.0, 0.36), ):
        for s in (-1, 1):   # small windows on the sides
            xx = s * (BW / 2 + 0.004)
            y.yuz_yon([V(xx, -0.03, fz), V(xx, 0.03, fz), V(xx, 0.03, fz + 0.04), V(xx, -0.03, fz + 0.04)], 'koyu', V(s, 0))
    # the back door and its landing
    y.yuz_yon([V(-0.03, BD / 2 + 0.004, BZ0 + 0.005), V(0.03, BD / 2 + 0.004, BZ0 + 0.005), V(0.03, BD / 2 + 0.004, BZ0 + 0.1), V(-0.03, BD / 2 + 0.004, BZ0 + 0.1)], 'ahsap_koyu', Y)
    kutu(y, V(-0.045, BD / 2, BZ0 - 0.01), X, 0.09, 0.04, 0.01, 'ahsap', 'onarkasagsolust')
    rz = cati_besik(y, -BW / 2, BW / 2, -BD / 2, BD / 2, BZ1, 0.1, 0.014, 'sindira', 'ahsap_koyu', ucluk_key='ahsap', ns=5, nr=6,
                    uc_sacak=0.012)
    # the ladder and the tail pole down to the mound's foot
    for s in (-1, 1):
        cubuk(y, V(s * 0.035, BD / 2 + 0.03, BZ0 - 0.005), V(s * 0.035, 0.37, -0.115), 0.01, 'ahsap_koyu', 0.008)
    for k in range(9):
        t = (k + 0.5) / 9
        p = V(0, BD / 2 + 0.03, BZ0 - 0.005).lerp(V(0, 0.37, -0.115), t)
        cubuk(y, p + V(-0.035, 0, 0), p + V(0.035, 0, 0), 0.006, 'ahsap', 0.004)
    cubuk(y, V(0, BD / 2, BZ0 + 0.02), V(0, 0.44, -0.12), 0.016, 'ahsap_koyu', 0.016)
    boru(y, [V(-0.012, 0.44, -0.1), V(0.012, 0.44, -0.1)], 0.028, 'ahsap', n=10)
    # windshaft, poll end and sails
    HUB = V(0, -BD / 2 - 0.05, 0.44)
    boru(y, [V(0, -BD / 2 + 0.03, 0.43), HUB], 0.016, 'kutuk', n=8)
    kutu3(y, HUB, X, Y, Z, 0.04, 0.03, 0.04, 'ahsap_koyu')
    SR = 0.4
    for k in range(4):
        th = math.radians(20) + math.pi / 2 * k
        d = V(math.cos(th), 0, math.sin(th)); s = V(-math.sin(th), 0, math.cos(th))
        o = HUB + V(0, -0.012, 0)
        cubuk(y, o, o + d * SR, 0.013, 'ahsap_koyu', 0.013)
        r0, W = 0.075, 0.085
        # the lattice: hemlath and a middle bar along the stock, sail bars across
        for off in (W * 0.5, W):
            cubuk(y, o + d * r0 + s * off, o + d * SR + s * off, 0.006, 'ahsap', 0.006)
        nb = 9
        for j in range(nb + 1):
            r = r0 + (SR - r0) * j / nb
            cubuk(y, o + d * r - s * 0.018, o + d * r + s * W, 0.005, 'ahsap', 0.005)
        # the cloth spread on the lattice (behind it)
        q = [o + d * (r0 + 0.01) + s * 0.006, o + d * (SR - 0.012) + s * 0.006, o + d * (SR - 0.012) + s * (W - 0.004),
             o + d * (r0 + 0.01) + s * (W - 0.004)]
        levha(y, [p + V(0, 0.006, 0) for p in q], 'kumas', -Y, 0.0015)
    # the banner on the roof's back
    sancak(y, 0, BD / 2 - 0.01, rz - 0.01, boy=0.14, en=0.1, yuk=0.06, aci=math.pi * 0.85)

y.bolum('Ağaçlar ve çit')
for (tx, ty, tb, tt) in ((1.1, 0.88, 0.2, 'yaprakli'), (0.92, 0.9, 0.16, 'yaprakli'), (-0.25, 0.88, 0.2, 'yaprakli'),
                         (1.12, -0.7, 0.15, 'yaprakli'), (-1.12, -0.97, 0.16, 'yaprakli'), (-0.95, -0.95, 0.14, 'yaprakli'),
                         (0.38, -0.66, 0.16, 'yaprakli'), (1.12, 0.45, 0.22, 'servi'), (-0.25, -0.62, 0.14, 'yaprakli'),
                         (0.42, 0.85, 0.18, 'yaprakli'), (1.12, 0.12, 0.17, 'yaprakli')):
    agac(y, tx, ty, G, boy=tb, tur=tt, key='boya_yesil' if (int(tx * 10) % 2) else 'zeytin')
# a wattle fence round a vegetable plot behind the first house
for (a, b) in (((-0.3, -0.24), (-0.1, -0.24)), ((-0.1, -0.24), (-0.1, -0.15)), ((-0.3, -0.15), (-0.3, -0.24))):
    a, b = V(*a), V(*b)
    L = (b - a).length; n = max(1, int(L / 0.03))
    for j in range(n + 1):
        p = a.lerp(b, j / n)
        cubuk(y, p + Z * G, p + Z * (G + 0.03), 0.004, 'ahsap_koyu')
    cubuk(y, a + Z * (G + 0.02), b + Z * (G + 0.02), 0.012, 'ahsap', 0.004)
for j in range(4):
    cubuk(y, V(-0.28, -0.22 + 0.02 * j, G + 0.006), V(-0.12, -0.22 + 0.02 * j, G + 0.006), 0.01, 'boya_yesil', 0.008)

y.bolum('Ayrıntılar: kovanlar, odun yığını, meyve bahçesi, çalılar')
# straw bee skeps on a bench by the west house
cubuk(y, V(-0.34, 0.08, G + 0.02), V(-0.34, 0.2, G + 0.02), 0.02, 'ahsap', 0.006)
for k in range(3):
    donel(y, (-0.34, 0.1 + 0.04 * k), [(0.014, G + 0.023), (0.015, G + 0.033), (0.011, G + 0.045), (0.005, G + 0.051), (0.0, G + 0.052)], 'saz', n=10)
for yy in (0.085, 0.195):
    cubuk(y, V(-0.34, yy, G), V(-0.34, yy, G + 0.02), 0.008, 'ahsap_koyu')
# a stacked woodpile against the mill's west wall, a chopping block with an axe
for j in range(3):
    for k in range(7 - j):
        boru(y, [V(MX0 - 0.006, -0.47 + 0.02 * k + 0.01 * j, G + 0.01 + 0.017 * j), V(MX0 - 0.05, -0.47 + 0.02 * k + 0.01 * j, G + 0.01 + 0.017 * j)],
             0.0085, 'kutuk' if (j + k) % 3 else 'ahsap_acik', n=6)
y.prizma((MX0 - 0.08, -0.36), 0.016, G, G + 0.02, 'kutuk', n=8)
cubuk(y, V(MX0 - 0.08, -0.36, G + 0.02), V(MX0 - 0.1, -0.36, G + 0.045), 0.004, 'ahsap')
# an orchard behind the fields: two rows of small apple trees with fruit
for r in range(2):
    for c in range(4):
        tx, ty = 0.86 + 0.08 * c + 0.03 * r, 0.14 + 0.1 * r
        boru(y, [V(tx, ty, G), V(tx + 0.004, ty, G + 0.05)], 0.006, 'ahsap_koyu', n=5)
        kure(y, (tx + 0.004, ty, G + 0.075), 0.034, 'boya_yesil' if (r + c) % 2 else 'zeytin', n=9, kat=5)
        for f in range(4):
            a_ = TAU * f / 4 + r + c
            kure(y, (tx + 0.004 + 0.03 * math.cos(a_), ty + 0.03 * math.sin(a_), G + 0.07 + 0.012 * (f % 2)), 0.006, 'boya_kirmizi', n=5, kat=3)
# a hedge of bushes along the far bank of the stream and the front road
for k in range(16):
    x = XA + 0.08 + k * 0.15
    if abs(x - BX) < 0.12: continue
    kure(y, (x, YA + 0.04, G + 0.018), 0.026 + 0.006 * (k % 3), 'yesil_koyu' if k % 2 else 'boya_yesil', n=8, kat=4)
# a wayside cross where the roads meet beyond the stream
kutu_merkez(y, (BX + 0.11, -0.99), 0.03, 0.03, 0.02, 'granit', z0=G)
kutu_merkez(y, (BX + 0.11, -0.99), 0.012, 0.012, 0.09, 'granit_koyu', z0=G + 0.02)
kutu_merkez(y, (BX + 0.11, -0.99), 0.05, 0.012, 0.012, 'granit_koyu', z0=G + 0.085)
# by the post mill: two spare millstones, sacks, the miller with a sack on his back, a donkey
for k, (mx, my) in enumerate(((0.52, 0.34), (0.55, 0.3))):
    boru(y, [V(mx, my, G + 0.035), V(mx + 0.012 * (1 - 2 * k), my - 0.006, G + 0.035)], 0.034, 'granit', n=14)
for k in range(3):
    donel(y, (0.9 + 0.03 * k, 0.45 + 0.012 * k), [(0.0, G + 0.06), (0.013, G + 0.064), (0.012, G + 0.08), (0.005, G + 0.09), (0.0, G + 0.091)], 'kumas', n=8)
insan(y, 0.88, 0.52, G + 0.085, 'kumas', aci=2.4, sapka='saz')
at(y, 0.47, 0.5, G + 0.004, aci=-0.6, s=0.75, key='granit', yele='granit_koyu')
donel(y, (0.47, 0.5), [(0.0, G + 0.054), (0.02, G + 0.056), (0.018, G + 0.064), (0.0, G + 0.066)], 'kumas', n=8)

calistir(y, 'lm_degirmenkoy')
