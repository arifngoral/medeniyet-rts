# Toledo sword forge (lm_toledo): a smiths' quarter on the bank of the Tagus under the city's rock. A stone-and-brick
# workshop (aparejo toledano: rubble panels framed by brick courses) with tiled roofs, an open forge shed with brick
# hearths, hoods and tall chimneys, anvils, bellows, a grinding wheel, quenching tanks and sword racks; a hammer mill
# on the quay driven by a big water wheel, a weir across the river, the Alcantara bridge with its gate tower; up on the
# rock the city wall, houses, a Mudejar brick church tower and an Alcazar wing with its square tower and slate spire.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import kutu3
from arap_ortak import kup, adam, halka_cati
from bina_ortak import calistir
import doku

y = Yapi()
rng = y.rng

ZG = 0.08                        # the yard level
ZU = 0.26                        # the city rock's top
QY = -0.705                      # the quay line
WZ = 0.015                       # the river's water level
B = 1.15                         # half size of the ground
TAS, TUG = 'kum', 'tugla'


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def gurultu(x, yy):
    return math.sin(x * 6.1 + 0.3) * math.cos(yy * 5.3 - 0.8) * 0.6 + math.sin(x * 13.0 - yy * 9.0 + 2.0) * 0.4


def yer(x, yy):
    """the ground's height: the yard, the rock rising behind, the river channel in front, all falling to 0 at the edge"""
    if yy >= QY:
        z = ZG + (ZU - ZG) * _ss(0.28, 0.5, yy)
        band = _ss(0.24, 0.36, yy) * (1 - _ss(0.44, 0.52, yy))
        z += 0.018 * gurultu(x, yy) * band
    elif yy >= -1.03:
        z = -0.03
    else:
        z = -0.03 + 0.075 * _ss(-1.03, -1.09, yy)
    d = min(x + B, B - x, yy + B, B - yy)
    return z * _ss(0.0, 0.11, d)


def yer_renk(x, yy, z):
    n = gurultu(x, yy)
    if yy < QY - 0.01:      # the river banks: reeds and wet earth
        return _mix((0.45, 0.50, 0.30), (0.52, 0.47, 0.33), 0.5 + 0.5 * n)
    if yy < 0.27:           # the yard: trodden dust, sooty near the forge
        c = _mix((0.70, 0.62, 0.48), (0.64, 0.57, 0.44), 0.5 + 0.5 * n)
        s = math.exp(-((x + 0.1) ** 2 / 0.2 + (yy + 0.4) ** 2 / 0.03))
        return _mix(c, (0.45, 0.41, 0.37), 0.45 * s)
    if yy < 0.5:            # the rock's face: ochre rock and scrub
        return _mix(_mix((0.66, 0.56, 0.42), (0.56, 0.47, 0.36), 0.5 + 0.5 * n), (0.48, 0.50, 0.30), 0.3 * max(0.0, n))
    n2 = math.sin(x * 9.0 + 1.3) * math.cos(yy * 7.0) * 0.5 + 0.5 * n
    return _mix((0.76, 0.67, 0.50), (0.55, 0.56, 0.35), 0.5 + 0.5 * n2)


doku.KOSE_RENK['toprak_ot'] = yer_renk

# ---------------------------------------------------------------- ground, river, quay
y.bolum('Arazi ve Tajo nehri')
xs = [-B + 2 * B * i / 46 for i in range(47)]
ys = sorted(set([round(-B + 0.05 * i, 4) for i in range(47)] + [QY, QY - 0.04, -1.03, -1.06, -1.09, 0.28, 0.5]))
ys = [v for v in ys if -B - 1e-6 <= v <= B + 1e-6]
G = [[V(x, yy, yer(x, yy)) for x in xs] for yy in ys]
for j in range(len(ys) - 1):
    for i in range(len(xs) - 1):
        y.yuz_yon([G[j][i], G[j][i + 1], G[j + 1][i + 1], G[j + 1][i]], 'toprak_ot', Z)
# the water: a flat sheet over the channel, its cut ends at the model's sides
WY0, WY1 = -1.075, QY + 0.004
y.yuz_yon([V(-B, WY0, WZ), V(B, WY0, WZ), V(B, WY1, WZ), V(-B, WY1, WZ)], 'su', Z)
for sx in (-1, 1):
    iki_yuzlu(y, [V(sx * B, WY0, 0.0), V(sx * B, WY1, 0.0), V(sx * B, WY1, WZ), V(sx * B, WY0, WZ)], 'su', V(sx, 0))
# the quay wall with a coping (a gap where the bridge lands)
for (qa, qb) in ((-1.0, -0.93), (-0.77, 1.0)):
    duz_duvar(y, V(qa, QY), V(qb, QY), -0.03, ZG + 0.006, 'tas_koyu')
    kutu3(y, V((qa + qb) / 2, QY + 0.004, ZG + 0.011), X, Y, Z, qb - qa + 0.006, 0.026, 0.01, 'tas_acik', ('+x', '-x', '-y', '+y', '+z', '-z'))
    for xx in (qa, qb):
        s = -1 if xx == qa else 1
        y.yuz_yon([V(xx, QY, -0.03), V(xx, QY + 0.02, -0.03), V(xx, QY + 0.02, ZG + 0.006), V(xx, QY, ZG + 0.006)], 'tas_koyu', V(s, 0))
# the weir (azud) slanting across the river, foam below it
wa, wb = V(-0.35, -1.06), V(0.32, QY - 0.01)
e = (wb - wa).normalized()
kutu(y, wa + Z * (-0.03), e, (wb - wa).length, 0.03, WZ + 0.012 + 0.03, 'tas_koyu', 'onarkasagsolust')
nn = V(e.y, -e.x)
for k in range(40):   # white water tumbling off the weir: a broken band of spray, thinning downstream
    t = (k + rng.random()) / 40
    off = 0.016 + 0.03 * rng.random() ** 2
    p = wa.lerp(wb, t) + nn * off
    r_ = (0.009 + 0.008 * rng.random()) * (1.0 - 8.0 * (off - 0.016))
    kure(y, (p.x, p.y, WZ - 0.004), r_, 'beyaz', n=6, kat=3)
# reeds and rocks on the far bank, rocks on the city rock's face
for i in range(28):
    x = -1.05 + 2.1 * rng.random()
    if -0.95 < x < -0.75: continue
    yy = -1.09 + 0.03 * rng.random()
    for k in range(3):
        cubuk(y, V(x + 0.006 * k, yy, yer(x, yy) - 0.005), V(x + 0.006 * k + 0.004 * (rng.random() - 0.5), yy + 0.004, yer(x, yy) + 0.04 + 0.02 * rng.random()), 0.003, 'cimen_kuru')
for i in range(34):
    x = -1.05 + 2.1 * rng.random()
    yy = 0.3 + 0.18 * rng.random()
    if -0.45 < x < 0.75 and yy > 0.42: continue
    kutu_merkez(y, (x, yy), 0.03 + 0.04 * rng.random(), 0.03 + 0.03 * rng.random(), 0.03 + 0.03 * rng.random(), 'kaya' if rng.random() < 0.6 else 'kaya_koyu',
                z0=yer(x, yy) - 0.02, aci=rng.random() * 3)
    if rng.random() < 0.4:
        kure(y, (x + 0.03, yy - 0.02, yer(x + 0.03, yy - 0.02) + 0.006), 0.014, 'zeytin', n=7, kat=3)


# ---------------------------------------------------------------- helpers
def toledano(a, b, z0, z1, desen, v0=0.4, v1=0.78, en=0.45, kapi_en=0.6):
    """an aparejo toledano wall a->b: rubble panels framed by brick courses and piers; bays per desen: '0' plain,
    '1' an arched window in a brick frame, 'k' an arched door, 'g' a wide arched opening (dark inside)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    n = len(desen); H = z1 - z0
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    for j, c in enumerate(desen):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        if c == '0':
            duz_duvar(y, p, q, z0, z1, TAS)
        elif c == '1':
            y.kemerli(p, q, z0, H, (TAS, TUG, TUG, 'koyu'), v0=H * v0, en=en, ust=H * (1 - v1), derin=0.014, k_say=6, cerceve=(0.006, [TUG, 'tugla_koyu']))
        elif c in 'kg':
            y.kemerli(p, q, z0, H, (TAS, TUG, 'tas_koyu', 'ahsap_dikey' if c == 'k' else 'koyu'), v0=0.0, en=kapi_en, ust=H * 0.25, derin=0.02, k_say=8,
                      cerceve=(0.008, [TUG, 'tugla_koyu']))
    # brick piers at the bay lines and courses below the sills and above the heads
    d = 0.003
    for j in range(n + 1):
        p = a.lerp(b, j / n)
        u0 = -0.007 if j > 0 else 0.0
        u1 = 0.007 if j < n else 0.0
        kutu(y, p + e * u0 + nc * d + Z * z0, e, u1 - u0, d, H, TUG, 'onsagsolust')
    for zz in [z0 + 0.012] + [z0 + H * v0 - 0.012] + [z0 + H * v1 + 0.016]:
        if zz + 0.008 > z1: continue
        kutu(y, a + nc * d + Z * zz, e, L, d, 0.008, TUG, 'onsagsolust')


def tekne(x0, x1, y0, y1, z, h, t=0.012, key='tas_koyu'):
    """a raised stone tank of water (quenching trough)"""
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, z, z + h, key)
    ki = disa(k, -t)
    duvarlar(y, [ki[3], ki[2], ki[1], ki[0]], z + h - 0.01, z + h, key)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([k[i] + Z * (z + h), k[j] + Z * (z + h), ki[j] + Z * (z + h), ki[i] + Z * (z + h)], 'tas_acik', Z)
    y.yuz_yon([V(p.x, p.y, z + h - 0.008) for p in ki], 'su', Z)


def kilic(p, e, nn, z, s=1.0):
    """a sword hanging point down: blade, cross guard, grip, pommel"""
    kutu3(y, p + Z * (z + 0.035 * s), e, nn, Z, 0.006 * s, 0.002, 0.058 * s, 'kursun')
    kutu3(y, p + Z * (z + 0.066 * s), e, nn, Z, 0.022 * s, 0.004, 0.004, 'altin')
    kutu3(y, p + Z * (z + 0.076 * s), e, nn, Z, 0.004, 0.004, 0.016 * s, 'ahsap_koyu')
    kure(y, (p.x, p.y, z + 0.087 * s), 0.0035 * s, 'altin', n=5, kat=3)


def kilic_rafi(cx, cy, z, aci, n=8, w=0.12):
    """a wooden sword rack: two posts, a top bar, swords hanging from it"""
    e = V(math.cos(aci), math.sin(aci)); nn = V(-e.y, e.x)
    c = V(cx, cy)
    for s in (-1, 1):
        cubuk(y, c + e * (s * w / 2) + Z * z, c + e * (s * w / 2) + Z * (z + 0.1), 0.008, 'ahsap_koyu')
        cubuk(y, c + e * (s * w / 2) - nn * 0.02 + Z * z, c + e * (s * w / 2) + nn * 0.02 + Z * z, 0.008, 'ahsap_koyu')   # feet
    cubuk(y, c - e * (w / 2 + 0.006) + Z * (z + 0.094), c + e * (w / 2 + 0.006) + Z * (z + 0.094), 0.008, 'ahsap')
    cubuk(y, c - e * (w / 2) + Z * (z + 0.02), c + e * (w / 2) + Z * (z + 0.02), 0.006, 'ahsap')
    for k in range(n):
        p = c + e * (-w / 2 + w * (k + 0.5) / n) + nn * 0.006
        kilic(p, e, nn, z + 0.006)


def ocak(cx, cy, z, z_baca, w=0.11, d=0.09):
    """a forge hearth: a brick box with a glowing coal bed, a hood and a brick chimney up to z_baca"""
    kutu_merkez(y, (cx, cy), w, d, 0.06, TUG, z0=z)
    kutu_merkez(y, (cx, cy - 0.005), w * 0.7, d * 0.55, 0.004, 'koyu', z0=z + 0.06)
    kutu_merkez(y, (cx, cy - 0.005), w * 0.32, d * 0.25, 0.006, 'boya_kirmizi', z0=z + 0.062)
    kutu_merkez(y, (cx, cy - 0.005), w * 0.16, d * 0.12, 0.008, 'boya_sari', z0=z + 0.063)
    # hood: a brick frustum on two corbels
    zh = z + 0.13
    donel(y, (cx, cy + 0.01), [(w * 0.74, zh), (w * 0.74, zh + 0.01), (0.028, zh + 0.08)], TUG, n=4, kat=math.pi / 4)
    y.yuz_yon([V(p.x, p.y, zh) for p in cokgen((cx, cy + 0.01), w * 0.74, 4, math.pi / 4)], 'koyu', -Z)
    y.prizma((cx, cy + 0.01), 0.028, zh + 0.08, z_baca, TUG, n=4, kat=math.pi / 4, ust=False)
    # the chimney's cap: a brick lip and a little tiled roof on four posts
    y.prizma((cx, cy + 0.01), 0.036, z_baca - 0.012, z_baca, 'tugla_koyu', n=4, kat=math.pi / 4)
    for (dx, dy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        cubuk(y, V(cx + dx * 0.018, cy + 0.01 + dy * 0.018, z_baca), V(cx + dx * 0.018, cy + 0.01 + dy * 0.018, z_baca + 0.022), 0.008, TUG)
    cati_kirma(y, cx - 0.026, cx + 0.026, cy + 0.01 - 0.026, cy + 0.01 + 0.026, z_baca + 0.022, 0.018, 0.006, 'kiremit', ns=2, nr=1)
    # bellows beside it
    kutu3(y, V(cx + w / 2 + 0.03, cy, z + 0.035), X, Y, Z, 0.05, 0.03, 0.02, 'ahsap_koyu')
    cubuk(y, V(cx + w / 2 + 0.055, cy, z + 0.045), V(cx + w / 2 + 0.085, cy, z + 0.07), 0.005, 'ahsap')
    # the fire's mouth on the hearth's front: a glowing opening
    kutu3(y, V(cx, cy - d / 2 - 0.001, z + 0.03), X, Y, Z, w * 0.5, 0.002, 0.03, 'koyu', ('-y', '+x', '-x', '+z', '-z'))
    kutu3(y, V(cx, cy - d / 2 - 0.0025, z + 0.026), X, Y, Z, w * 0.36, 0.002, 0.018, 'boya_kirmizi', ('-y', '+x', '-x', '+z', '-z'))
    kutu3(y, V(cx, cy - d / 2 - 0.004, z + 0.023), X, Y, Z, w * 0.2, 0.002, 0.01, 'boya_sari', ('-y', '+x', '-x', '+z', '-z'))


def ors(cx, cy, z, aci=0.0):
    """an anvil on a log"""
    donel(y, (cx, cy), [(0.0, z), (0.02, z), (0.019, z + 0.032), (0.0, z + 0.032)], 'ahsap', n=8)
    with parca(y, (cx, cy, z + 0.032), aci):
        kutu3(y, V(0, 0, 0.006), X, Y, Z, 0.02, 0.014, 0.012, 'demir')
        kutu3(y, V(0, 0, 0.017), X, Y, Z, 0.036, 0.016, 0.01, 'demir')
        boru(y, [V(0.018, 0, 0.018), V(0.036, 0, 0.018)], 0.006, 'demir', n=5, r_son=0.001)


def disk(c, r, th, key='tas', n=14):
    """a vertical disc (grinding wheel) centred at c, its axis along x"""
    c = Vector(c)
    P = lambda s, i: c + V(s * th / 2, r * math.cos(TAU * i / n), 0) + Z * (r * math.sin(TAU * i / n))
    y.yuz_yon([P(1, i) for i in range(n)], key, X)
    y.yuz_yon([P(-1, i) for i in range(n)], key, -X)
    for i in range(n):
        j = (i + 1) % n
        q = [P(-1, i), P(-1, j), P(1, j), P(1, i)]
        yuz_dis(y, q, key, c)


def sundurma(x0, x1, y_duvar, y_on, z_ust, z_alt, key='kiremit', n_direk=5):
    """an open lean-to roof against a wall at y_duvar (the yard towards -y): tiles on top, boards under it, the eave's
    fascia, posts and a beam at the front"""
    k = 0.008
    A, Bq = V(x0 - 0.02, y_on, z_alt), V(x1 + 0.02, y_on, z_alt)
    C, D = V(x1 + 0.02, y_duvar, z_ust), V(x0 - 0.02, y_duvar, z_ust)
    y.yuz_yon([A, Bq, C, D], key, V(0, -0.4, 1))
    y.yuz_yon([A - Z * k, Bq - Z * k, C - Z * k, D - Z * k], 'ahsap_koyu', V(0, 0.4, -1))
    y.yuz_yon([A, Bq, Bq - Z * k, A - Z * k], 'ahsap_koyu', -Y)
    for p, q, s in ((A, D, -1), (Bq, C, 1)):
        y.yuz_yon([p, q, q - Z * k, p - Z * k], 'ahsap_koyu', V(s, 0))
    cubuk(y, V(x0, y_on + 0.03, z_alt - k - 0.008), V(x1, y_on + 0.03, z_alt - k - 0.008 + 0.0), 0.016, 'ahsap')
    for i in range(n_direk):
        xx = x0 + (x1 - x0) * i / (n_direk - 1)
        cubuk(y, V(xx, y_on + 0.03, ZG), V(xx, y_on + 0.03, z_alt - k - 0.016), 0.014, 'ahsap')
        kutu_merkez(y, (xx, y_on + 0.03), 0.024, 0.024, 0.01, 'tas_koyu', z0=ZG)


# ---------------------------------------------------------------- the forge hall and wing
y.bolum('Kılıç ocağı: atölye')
HX0, HX1, HY0, HY1 = -0.5, 0.3, -0.32, 0.0
HZ = ZG + 0.2
hk = dikdortgen(HX0, HX1, HY0, HY1)
toledano(hk[0], hk[1], ZG, HZ, '0g0g0g0g0', v0=0.38, v1=0.8, kapi_en=0.7)
toledano(hk[2], hk[3], ZG, HZ, '0101010101', v0=0.45, v1=0.8)
toledano(hk[3], hk[0], ZG, HZ, '0k0', v0=0.4, v1=0.78)
silme(y, hk, HZ - 0.01, 0.01, 0.008, 'tugla_koyu', 'tac')
cati_besik(y, HX0, HX1, HY0, HY1, HZ, 0.1, 0.024, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=10, nr=4, dilim=['kiremit', 'kiremit2'])
sancak(y, HX0 + 0.02, (HY0 + HY1) / 2, ZG + 0.3, boy=0.2, en=0.13, yuk=0.08, aci=math.pi * 0.85)
# the side wing (stores, the master's house) to the right, two storeys
WX0, WX1, WYa, WYb = 0.3, 0.56, -0.36, 0.24
WZt = ZG + 0.27
wk = dikdortgen(WX0, WX1, WYa, WYb)
for (z0, z1, des) in ((ZG, ZG + 0.13, ['0k0', '01010', '0', None]), (ZG + 0.13, WZt, ['010', '01010', '0101', None])):
    for i in range(4):
        if des[i] is None: continue
        toledano(wk[i], wk[(i + 1) % 4], z0, z1, des[i], v0=0.35, v1=0.8)
duz_duvar(y, wk[3], V(WX0, HY1), ZG, WZt, TAS)          # (the wing's left side: the hall stands against its middle)
duz_duvar(y, V(WX0, HY1), V(WX0, HY0), HZ, WZt, TAS)
duz_duvar(y, V(WX0, HY0), wk[0], ZG, WZt, TAS)
silme(y, wk, WZt - 0.01, 0.01, 0.008, 'tugla_koyu', 'tac')
silme(y, wk, ZG + 0.13, 0.008, 0.005, TUG, 'duz')
cati_kirma(y, WX0, WX1, WYa, WYb, WZt, 0.1, 0.024, 'kiremit', 'kiremit2', ns=6, nr=4, dilim=['kiremit', 'kiremit2'])
# a wooden gallery (balcony) on the wing's upper front
cubuk(y, V(WX0 + 0.02, WYa - 0.03, ZG + 0.135), V(WX1 - 0.02, WYa - 0.03, ZG + 0.135), 0.006, 'ahsap_koyu')
kutu3(y, V((WX0 + WX1) / 2, WYa - 0.016, ZG + 0.132), X, Y, Z, WX1 - WX0 - 0.04, 0.032, 0.006, 'ahsap')
for k in range(9):
    xx = WX0 + 0.02 + (WX1 - WX0 - 0.04) * k / 8
    cubuk(y, V(xx, WYa - 0.03, ZG + 0.135), V(xx, WYa - 0.03, ZG + 0.165), 0.004, 'ahsap_koyu')
cubuk(y, V(WX0 + 0.02, WYa - 0.03, ZG + 0.166), V(WX1 - 0.02, WYa - 0.03, ZG + 0.166), 0.006, 'ahsap_koyu')

# ---------------------------------------------------------------- the open forge shed
y.bolum('Ocaklar, örsler, su verme havuzları')
SY = HY0 - 0.15
sundurma(HX0 + 0.02, HX1 - 0.04, HY0, SY, ZG + 0.19, ZG + 0.135, n_direk=6)
for k, xx in enumerate((-0.38, -0.14, 0.1)):
    ocak(xx, HY0 - 0.055, ZG, HZ + 0.2 + 0.03 * (k % 2))
    ors(xx + 0.03, HY0 - 0.13, ZG, 0.3 * k)
    adam(y, xx - 0.02, HY0 - 0.125, ZG, 0.4, govde='ahsap_koyu', bas='koyu', boy=0.05, kol=(0.01, 0.03))
# the grinding wheel
GX, GY = 0.2, HY0 - 0.12
disk((GX, GY, ZG + 0.05), 0.035, 0.014, 'tas')
cubuk(y, V(GX - 0.025, GY, ZG + 0.05), V(GX + 0.025, GY, ZG + 0.05), 0.006, 'demir')
for sx in (-1, 1):
    cubuk(y, V(GX + sx * 0.018, GY - 0.012, ZG), V(GX + sx * 0.018, GY, ZG + 0.05), 0.007, 'ahsap')
    cubuk(y, V(GX + sx * 0.018, GY + 0.012, ZG), V(GX + sx * 0.018, GY, ZG + 0.05), 0.007, 'ahsap')
kutu_merkez(y, (GX, GY), 0.05, 0.04, 0.012, 'ahsap_koyu', z0=ZG)
# quenching tanks in the yard
tekne(-0.42, -0.24, -0.66, -0.58, ZG, 0.035)
tekne(-0.1, 0.06, -0.66, -0.58, ZG, 0.035)
# sword racks, crates, iron bars, charcoal
for (cx_, cy_, a) in ((-0.17, -0.62, 0.0), (0.16, -0.62, 0.0), (0.33, -0.5, math.pi / 2), (-0.55, -0.45, math.pi / 2)):
    kilic_rafi(cx_, cy_, ZG, a)
for (px, py_) in ((0.25, -0.66), (0.29, -0.64)):
    kutu_merkez(y, (px, py_), 0.04, 0.035, 0.03, 'ahsap_acik', z0=ZG, aci=0.3)
for k in range(5):
    cubuk(y, V(-0.6, -0.6 + 0.008 * k, ZG + 0.004), V(-0.5, -0.6 + 0.008 * k, ZG + 0.004), 0.006, 'demir')
donel(y, (-0.62, -0.18), [(0.07, ZG), (0.05, ZG + 0.035), (0.0, ZG + 0.06)], 'koyu', n=12)
for k in range(4):   # a stack of firewood
    for j in range(4 - k):
        boru(y, [V(-0.7 + 0.022 * j + 0.011 * k, 0.05, ZG + 0.01 + 0.018 * k), V(-0.7 + 0.022 * j + 0.011 * k, 0.17, ZG + 0.01 + 0.018 * k)], 0.01, 'kutuk', n=6)
adam(y, 0.02, -0.55, ZG, 2.4, govde='kumas', bas='koyu', boy=0.05)
adam(y, -0.3, -0.52, ZG, 0.9, govde='boya_kirmizi', bas='koyu', boy=0.05)

# the charcoal and ore store at the right: an open shed on posts, sacks, an ore heap, an ox cart, trees
y.bolum('Kömürlük, araba')
KX0, KX1, KY0, KY1 = 0.68, 0.98, -0.08, 0.2
for (xx, yy) in ((KX0, KY0), (KX1, KY0), (KX0, KY1), (KX1, KY1), ((KX0 + KX1) / 2, KY0), ((KX0 + KX1) / 2, KY1)):
    cubuk(y, V(xx, yy, ZG), V(xx, yy, ZG + 0.12), 0.014, 'ahsap')
cati_besik(y, KX0, KX1, KY0, KY1, ZG + 0.12, 0.06, 0.02, 'kiremit', 'kiremit2', ucluk_key='ahsap_dikey', ns=6, nr=3, dilim=['kiremit', 'kiremit2'])
donel(y, (0.78, 0.06), [(0.08, ZG), (0.06, ZG + 0.04), (0.0, ZG + 0.07)], 'koyu', n=12)
for (px, py_) in ((0.9, 0.0), (0.92, 0.06), (0.88, 0.11), (0.93, 0.14)):
    donel(y, (px, py_), [(0.0, ZG), (0.02, ZG), (0.022, ZG + 0.03), (0.012, ZG + 0.042), (0.0, ZG + 0.044)], 'kumas', n=8)
donel(y, (0.82, -0.25), [(0.07, ZG), (0.05, ZG + 0.03), (0.0, ZG + 0.05)], 'kirmizi_tas', n=10)    # iron ore
# the ox cart
with parca(y, (0.95, -0.28, ZG), 0.9):
    kutu3(y, V(0, 0, 0.045), X, Y, Z, 0.11, 0.06, 0.008, 'ahsap')
    for s in (-1, 1):
        kutu3(y, V(0, s * 0.03, 0.06), X, Y, Z, 0.11, 0.004, 0.024, 'ahsap_dikey')
    for s in (-1, 1):
        P = lambda r, t: V(0.0 + r * math.cos(t), s * 0.04, 0.035 + r * math.sin(t))
        y.yuz_yon([P(0.035, TAU * i / 10) for i in range(10)], 'ahsap_koyu', V(0, s))
        y.yuz_yon([P(0.035, TAU * i / 10) + V(0, -s * 0.008) for i in range(10)], 'ahsap_koyu', V(0, -s))
        for i in range(10):
            a_, b_ = P(0.035, TAU * i / 10), P(0.035, TAU * (i + 1) / 10)
            y.yuz_yon([a_, b_, b_ + V(0, -s * 0.008), a_ + V(0, -s * 0.008)], 'ahsap_koyu', (a_ + b_) / 2 - V(0, s * 0.04, 0.035))
    cubuk(y, V(0.055, 0, 0.045), V(0.15, 0, 0.03), 0.008, 'ahsap')
    for k in range(3):
        donel(y, (-0.02 + 0.03 * k, 0), [(0.0, 0.049), (0.014, 0.049), (0.016, 0.07), (0.0, 0.072)], 'kumas', n=7)
for (px, py_) in ((0.75, 0.38), (0.98, 0.32), (0.62, 0.36), (1.0, -0.12), (-0.98, -0.5), (-1.0, -0.2), (-0.7, -0.6)):
    kure(y, (px, py_, yer(px, py_) + 0.045), 0.035, 'zeytin', n=8, kat=4)
    y.prizma((px, py_), 0.005, yer(px, py_) - 0.01, yer(px, py_) + 0.03, 'ahsap', n=5)

# the swordsmiths' guild house in the left yard: two storeys of aparejo toledano, a tiled roof, a wooden balcony
y.bolum('Lonca evi ve yol')
LX0, LX1, LY0, LY1 = -1.04, -0.78, -0.06, 0.22
LZ = ZG + 0.24
lk = dikdortgen(LX0, LX1, LY0, LY1)
for (z0, z1, des) in ((ZG, ZG + 0.12, ['0k0', '010', '0', '010']), (ZG + 0.12, LZ, ['01010', '010', '0', '010'])):
    for i in range(4):
        toledano(lk[i], lk[(i + 1) % 4], z0, z1, des[i], v0=0.35, v1=0.8)
silme(y, lk, ZG + 0.12, 0.008, 0.005, TUG, 'duz')
silme(y, lk, LZ - 0.01, 0.01, 0.008, 'tugla_koyu', 'tac')
cati_besik(y, LX0, LX1, LY0, LY1, LZ, 0.09, 0.022, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=8, nr=4, dilim=['kiremit', 'kiremit2'])
kutu3(y, V((LX0 + LX1) / 2, LY0 - 0.016, ZG + 0.127), X, Y, Z, LX1 - LX0 - 0.06, 0.032, 0.006, 'ahsap')
for k in range(9):
    xx = LX0 + 0.03 + (LX1 - LX0 - 0.06) * k / 8
    cubuk(y, V(xx, LY0 - 0.03, ZG + 0.13), V(xx, LY0 - 0.03, ZG + 0.16), 0.004, 'ahsap_koyu')
cubuk(y, V(LX0 + 0.03, LY0 - 0.03, ZG + 0.161), V(LX1 - 0.03, LY0 - 0.03, ZG + 0.161), 0.006, 'ahsap_koyu')
kutu_merkez(y, (LX0 + 0.06, (LY0 + LY1) / 2 + 0.04), 0.028, 0.028, 0.11, TUG, z0=LZ + 0.02)
# a trodden path from the bridge gate across the yard to the forge
for (pa, pb) in ((V(-0.85, QY + 0.14), V(-0.72, -0.42)), (V(-0.72, -0.42), V(-0.5, -0.47))):
    d = (pb - pa).normalized(); nn_ = V(d.y, -d.x) * 0.032
    y.yuz_yon([V(p.x, p.y, ZG + 0.0015) for p in (pa + nn_, pb + nn_, pb - nn_, pa - nn_)], 'kum_acik', Z)
# a well with a sweep (cigonal) in the left yard
donel(y, (-0.8, -0.35), [(0.0, ZG), (0.03, ZG), (0.03, ZG + 0.03), (0.024, ZG + 0.03), (0.024, ZG + 0.01), (0.0, ZG + 0.01)], 'tas_koyu', n=12)
cubuk(y, V(-0.75, -0.35, ZG), V(-0.75, -0.35, ZG + 0.1), 0.01, 'ahsap_koyu')
cubuk(y, V(-0.84, -0.35, ZG + 0.06), V(-0.66, -0.35, ZG + 0.14), 0.007, 'ahsap')
cubuk(y, V(-0.82, -0.35, ZG + 0.069), V(-0.82, -0.35, ZG + 0.025), 0.003, 'ahsap_koyu')

# ---------------------------------------------------------------- the hammer mill and the water wheel
y.bolum('Çekiç değirmeni ve su çarkı')
MX0, MX1, MY0, MY1 = 0.5, 0.82, QY + 0.02, -0.44
MZ = ZG + 0.15
mk = dikdortgen(MX0, MX1, MY0, MY1)
toledano(mk[0], mk[1], ZG, MZ, '0101', v0=0.4, v1=0.78)
toledano(mk[1], mk[2], ZG, MZ, '010', v0=0.4, v1=0.78)
toledano(mk[2], mk[3], ZG, MZ, '0101', v0=0.4, v1=0.78)
toledano(mk[3], mk[0], ZG, MZ, '0k0', v0=0.4, v1=0.78)
silme(y, mk, MZ - 0.01, 0.01, 0.007, 'tugla_koyu', 'tac')
cati_besik(y, MX0, MX1, MY0, MY1, MZ, 0.08, 0.02, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=8, nr=4, dilim=['kiremit', 'kiremit2'])
# the wheel: in the river in front of the quay, turning on an axle into the mill
CX_, CY_, CZ_, R = 0.66, -0.8, 0.1, 0.14
for s in (-1, 1):   # two rims of 16 felloes, eight spokes
    yy = CY_ + s * 0.026
    rim = [V(CX_ + R * math.cos(TAU * i / 16), yy, CZ_ + R * math.sin(TAU * i / 16)) for i in range(16)]
    for i in range(16):
        cubuk(y, rim[i], rim[(i + 1) % 16], 0.012, 'ahsap', 0.01)
    for i in range(0, 16, 2):
        cubuk(y, V(CX_, yy, CZ_), rim[i], 0.008, 'ahsap_koyu', 0.008)
for i in range(16):   # the paddles across the rims
    a = TAU * (i + 0.5) / 16
    d = V(math.cos(a), 0, math.sin(a))
    c = V(CX_, CY_, CZ_) + d * (R + 0.004)
    t = V(-math.sin(a), 0, math.cos(a))
    kutu3(y, c, d, Y, t, 0.04, 0.064, 0.005, 'ahsap_acik')
cubuk(y, V(CX_, CY_ - 0.045, CZ_), V(CX_, QY + 0.06, CZ_), 0.018, 'ahsap_koyu')
# the head race: a wooden flume bringing water onto the wheel's top
FZ = CZ_ + R + 0.035
for s in (-1, 1):
    cubuk(y, V(CX_ - 0.32, CY_ + s * 0.03, FZ + 0.012), V(CX_ + 0.02, CY_ + s * 0.03, FZ + 0.012), 0.006, 'ahsap', 0.024)
cubuk(y, V(CX_ - 0.32, CY_, FZ), V(CX_ + 0.02, CY_, FZ), 0.066, 'ahsap', 0.006)
y.yuz_yon([V(CX_ - 0.32, CY_ - 0.026, FZ + 0.012), V(CX_ + 0.02, CY_ - 0.026, FZ + 0.012), V(CX_ + 0.02, CY_ + 0.026, FZ + 0.012), V(CX_ - 0.32, CY_ + 0.026, FZ + 0.012)], 'su', Z)
for xx in (CX_ - 0.3, CX_ - 0.16):
    for s in (-1, 1):
        cubuk(y, V(xx, CY_ + s * 0.03, -0.03), V(xx, CY_ + s * 0.03, FZ - 0.003), 0.01, 'ahsap_koyu')

# ---------------------------------------------------------------- the Alcantara bridge
y.bolum('Alcántara köprüsü')
BXc = -0.85
# (the Alcantara has one great arch and a smaller one: the pier between them carries the cutwater)
BM = -0.83
kemer_dizisi(y, V(BXc + 0.065, -1.07), V(BXc + 0.065, BM), 1, -0.03, ZG + 0.03, 0.13, renk=(TAS, 'tas_koyu', 'tas_acik', 'koyu'), en=0.8, ust=0.014,
             acik=True, taban=False)
kemer_dizisi(y, V(BXc + 0.065, BM), V(BXc + 0.065, QY), 1, -0.03, ZG + 0.03, 0.13, renk=(TAS, 'tas_koyu', 'tas_acik', 'koyu'), en=0.66, ust=0.03,
             acik=True, taban=False)
for s in (-1, 1):   # parapets
    xx = BXc + s * 0.059
    kutu3(y, V(xx, (-1.07 + QY) / 2, ZG + 0.012), X, Y, Z, 0.012, QY + 1.07, 0.024, 'tas_koyu', ('+x', '-x', '+y', '-y', '+z'))
# the cutwater on the middle pier (upstream side, +x)
my = BM
y.yuz_yon([V(BXc + 0.065, my - 0.025, -0.03), V(BXc + 0.11, my, -0.03), V(BXc + 0.11, my, ZG - 0.04), V(BXc + 0.065, my - 0.025, ZG - 0.02)], 'tas_koyu', V(0.5, -1))
y.yuz_yon([V(BXc + 0.11, my, -0.03), V(BXc + 0.065, my + 0.025, -0.03), V(BXc + 0.065, my + 0.025, ZG - 0.02), V(BXc + 0.11, my, ZG - 0.04)], 'tas_koyu', V(0.5, 1))
y.yuz_yon([V(BXc + 0.065, my - 0.025, ZG - 0.02), V(BXc + 0.11, my, ZG - 0.04), V(BXc + 0.065, my + 0.025, ZG - 0.02)], 'tas_acik', V(0.3, 0, 1))
# the far gate on the opposite bank: a plinth up to the deck, an arched gate block with merlons
kutu_merkez(y, (BXc, -1.105), 0.18, 0.09, ZG + 0.058, 'tas_koyu', z0=-0.03)
kale_kapisi(y, BXc, -1.105, 0.17, ZG + 0.028, 0.17, derin=0.08, key=TAS, kule=None, kapi_key='koyu')
# the gate tower at the city end
kale_kapisi(y, BXc, QY + 0.08, 0.16, ZG - 0.01, 0.2, derin=0.11, key=TAS, kule=None, kapi_key='koyu')
sancak(y, BXc + 0.05, QY + 0.1, ZG + 0.23, boy=0.16, en=0.1, yuk=0.06, aci=0.4)
y.yuz_yon([V(BXc - 0.06, QY, ZG + 0.002), V(BXc + 0.06, QY, ZG + 0.002), V(BXc + 0.06, QY + 0.02, ZG + 0.002), V(BXc - 0.06, QY + 0.02, ZG + 0.002)], 'tas_acik', Z)

# ---------------------------------------------------------------- the city: wall, houses
y.bolum('Şehir suru ve evler')
sur(y, [V(-1.06, 0.45), V(-0.42, 0.45)], ZU - 0.075, 0.15, kalinlik=0.04, key=TAS, kapali=False, mazgal_h=0.024, parapet_h=0.012, ust_key='zemin')
for xx in (-0.98, -0.7):
    kule_kare(y, xx, 0.45, 0.09, ZU - 0.085, 0.21, TAS, cati='duz', mazgal_h=0.024, yarik_say=1, konsol=True)


def ev(cx, cy, w, d, h, aci, z, duvar='siva_krem'):
    """a small town house: walls, tiny windows and a door, a tiled gable roof"""
    with parca(y, (cx, cy, 0), aci):
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        duvarlar(y, k, z - 0.03, z + h, duvar)
        for u in (-0.3, 0.3):
            kutu3(y, V(u * w, -d / 2 - 0.0008, z + h * 0.66), X, Y, Z, 0.009, 0.0016, 0.012, 'koyu', ('-y',))
        cati_besik(y, -w / 2, w / 2, -d / 2, d / 2, z + h, d * 0.38, 0.01, 'kiremit', 'kiremit2', ucluk_key=duvar, ns=3, nr=2, kalinlik=0.006)


for (cx, cy, w, d, h, a, dv) in ((-1.0, 0.62, 0.1, 0.08, 0.1, 0.0, 'siva_krem'), (-0.86, 0.6, 0.09, 0.08, 0.13, 0.1, 'kum'),
                                 (-0.72, 0.62, 0.1, 0.08, 0.09, -0.05, 'siva'), (-0.58, 0.6, 0.08, 0.08, 0.12, 0.0, 'siva_krem'),
                                 (-0.98, 0.78, 0.1, 0.09, 0.12, 0.1, 'siva'), (-0.82, 0.79, 0.11, 0.08, 0.1, -0.1, 'siva_oker'),
                                 (-0.66, 0.78, 0.09, 0.08, 0.14, 0.05, 'kum'), (-0.5, 0.8, 0.08, 0.09, 0.1, 0.0, 'siva_krem'),
                                 (-0.92, 0.94, 0.12, 0.07, 0.09, 0.0, 'siva_krem'), (-0.74, 0.95, 0.1, 0.07, 0.1, 0.1, 'siva'),
                                 (-0.56, 0.96, 0.1, 0.07, 0.11, -0.05, 'kum'), (-0.36, 0.96, 0.09, 0.08, 0.1, 0.0, 'siva_krem'),
                                 (-0.42, 0.62, 0.09, 0.08, 0.1, 0.05, 'siva'), (0.0, 0.96, 0.1, 0.07, 0.1, 0.0, 'siva'),
                                 (0.16, 0.6, 0.1, 0.08, 0.11, 0.0, 'siva_krem'), (0.04, 0.6, 0.09, 0.08, 0.09, 0.1, 'kum')):
    ev(cx, cy, w, d, h, a, ZU, dv)
for (cx, cy) in ((-1.05, 0.7), (-0.47, 0.7), (-0.27, 0.6), (0.27, 0.62), (-1.04, 0.9), (0.12, 0.94)):
    agac(y, cx, cy, ZU, boy=0.16, tur='servi', key='yesil_koyu')
for (cx, cy) in ((-0.62, 0.7), (-0.9, 0.7), (0.3, 0.96)):
    kure(y, (cx, cy, ZU + 0.03), 0.03, 'zeytin', n=8, kat=4)
    y.prizma((cx, cy), 0.004, ZU, ZU + 0.02, 'ahsap', n=5)

# ---------------------------------------------------------------- a Mudejar church: brick tower with blind arches
y.bolum('Mudéjar kilise kulesi')
CX0, CX1, CY0, CY1 = -0.22, 0.08, 0.72, 0.86
CZ = ZU + 0.15
ck = dikdortgen(CX0, CX1, CY0, CY1)
for i in range(4):
    a, b = ck[i], ck[(i + 1) % 4]
    L = (b - a).length
    n = max(2, int(round(L / 0.05)))
    for j in range(n):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        if i in (0, 2) and j % 2:
            y.kemerli(p, q, ZU - 0.03, CZ - ZU + 0.03, (TUG, 'tugla_koyu', 'tas_acik', 'koyu'), v0=0.1, en=0.4, ust=0.02, derin=0.01, k_say=6, sivri=0.5)
        else:
            duz_duvar(y, p, q, ZU - 0.03, CZ, TUG)
silme(y, ck, CZ - 0.01, 0.01, 0.007, 'tugla_koyu', 'tac')
cati_besik(y, CX0, CX1, CY0, CY1, CZ, 0.07, 0.016, 'kiremit', 'kiremit2', ucluk_key=TUG, ns=6, nr=3, dilim=['kiremit', 'kiremit2'])
MTX, MTY, MW = CX0 - 0.03, CY0 + 0.02, 0.12
mt = dikdortgen(MTX - MW / 2, MTX + MW / 2, MTY - MW / 2, MTY + MW / 2)
MZ0 = ZU - 0.03
levels = [(MZ0, MZ0 + 0.14, None), (MZ0 + 0.14, MZ0 + 0.24, 'nis'), (MZ0 + 0.24, MZ0 + 0.34, 'nis'), (MZ0 + 0.34, MZ0 + 0.45, 'can')]
for z0, z1, tur in levels:
    for i in range(4):
        a, b = mt[i], mt[(i + 1) % 4]
        if tur is None:
            duz_duvar(y, a, b, z0, z1, TUG)
        elif tur == 'nis':   # two blind horseshoe-ish arches
            m = a.lerp(b, 0.5)
            for p, q in ((a, m), (m, b)):
                kemer_nis(y, p, q, z0, z1 - z0, en=0.56, ust=0.016, sivri=0.35, derin=0.006, key=TUG, yan_key='tugla_koyu', alt_key='tugla_koyu',
                          arka_key='tugla_koyu', v0=0.012, k_say=8)
        else:                # the belfry: one arched opening each side
            y.kemerli(a, b, z0, z1 - z0, (TUG, 'tugla_koyu', 'tas_acik', 'koyu'), v0=0.012, en=0.5, ust=0.016, derin=0.022, k_say=8, cerceve=(0.005, 'tas_acik'))
    silme(y, mt, z1 - 0.007, 0.007, 0.006, 'tugla_koyu' if z1 < MZ0 + 0.4 else 'tas_acik', 'duz')
for i in range(4):   # a glazed tile band under the belfry
    a, b = mt[i], mt[(i + 1) % 4]
    e_ = (b - a).normalized(); n_ = V(e_.y, -e_.x)
    for k in range(6):
        p = a.lerp(b, (k + 0.5) / 6) + n_ * 0.0012
        kutu3(y, p + Z * (MZ0 + 0.33), e_, n_, Z, 0.012, 0.002, 0.012, 'turkuaz' if k % 2 else 'beyaz', ('+y', '+x', '-x', '+z', '-z'))
mtop = cati_kirma(y, MTX - MW / 2, MTX + MW / 2, MTY - MW / 2, MTY + MW / 2, MZ0 + 0.45, 0.09, 0.012, 'kiremit', 'kiremit2', ns=4, nr=3)
y.prizma((MTX, MTY), 0.003, mtop - 0.01, mtop + 0.05, 'demir', n=4)
cubuk(y, V(MTX - 0.012, MTY, mtop + 0.032), V(MTX + 0.012, MTY, mtop + 0.032), 0.004, 'demir')

# ---------------------------------------------------------------- the Alcazar
# a square block of three storeys round a courtyard, a square tower at each corner under a slate spire (chapitel), the
# Plateresque north front (towards the river) with its pedimented portal and the imperial arms
y.bolum('Alcázar: cephe ve kuleler')
AX0, AX1, AY0, AY1 = 0.27, 0.71, 0.62, 0.99
AZ = ZU + 0.22
AK = 'kirec'
AR = (AK, 'tas_koyu', 'tas_acik', 'koyu')
ak = dikdortgen(AX0, AX1, AY0, AY1)
TW = 0.1                         # the corner towers


def kat(a, b, z0, z1, n, kapi=None, v0=0.3, v1=0.82):
    """a storey a->b in n bays of framed rectangular windows (an arched door in bay kapi)"""
    for j in range(n):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        if kapi is not None and j == kapi:
            y.kemerli(p, q, z0, z1 - z0, (AK, 'tas_koyu', 'tas_acik', 'ahsap_dikey'), v0=0.0, en=0.62, ust=(z1 - z0) * 0.12, derin=0.02, k_say=8,
                      cerceve=(0.007, 'granit'))
        else:
            dikdortgen_acik(y, p, q, z0, z1 - z0, 0.3, 0.7, (z1 - z0) * v0, (z1 - z0) * v1, AR, derin=0.012, cerceve=(0.005, 'granit'), ic_kenar=True)


# the four fronts between the towers (each tower takes TW/2 off both ends)
for i in range(4):
    a, b = ak[i], ak[(i + 1) % 4]
    e = (b - a).normalized()
    a, b = a + e * (TW / 2), b - e * (TW / 2)
    L = (b - a).length
    n = max(3, int(round(L / 0.07)))
    n += (n + 1) % 2                     # (an odd count: a middle bay for the portal)
    kat(a, b, ZU - 0.04, ZU + 0.07, n, kapi=n // 2 if i == 0 else None)
    kat(a, b, ZU + 0.07, ZU + 0.145, n)
    kat(a, b, ZU + 0.145, AZ, n, v0=0.25, v1=0.72)
for zz in (ZU + 0.07, ZU + 0.145):
    silme(y, ak, zz - 0.006, 0.006, 0.005, 'granit', 'duz')
silme(y, ak, ZU - 0.04, 0.03, 0.008, 'granit', 'kaide')
silme(y, ak, AZ - 0.016, 0.016, 0.012, 'granit', 'tac')
# the courtyard (patio): its inner walls with an arcade at the bottom, the roof ring round it
IC = (AX0 + 0.11, AX1 - 0.11, AY0 + 0.1, AY1 - 0.1)
ik = dikdortgen(*IC)
ikr = [ik[1], ik[0], ik[3], ik[2]]      # (walking it clockwise: the walls face into the court)
for i in range(4):
    a, b = ikr[i], ikr[(i + 1) % 4]
    L = (b - a).length
    arkad(y, a, b, max(3, int(round(L / 0.05))), ZU, 0.07, en=0.7, ust=0.012, sivri=0.0, derin=0.025, sutun_key='granit', sutun_r=0.005,
          renk=(AK, AK, 'tas_acik', 'tas_koyu'), cerceve=None)
    duz_duvar(y, a, b, ZU + 0.07, AZ - 0.01, AK)
    e_ = (b - a).normalized(); nc_ = V(e_.y, -e_.x)     # (the gallery's back wall: the arcade alone left the wing hollow)
    duz_duvar(y, a - nc_ * 0.026 - e_ * 0.03, b - nc_ * 0.026 + e_ * 0.03, ZU, ZU + 0.07, 'tas_koyu')
y.yuz_yon([V(p.x, p.y, ZU + 0.002) for p in ik], 'zemin', Z)
halka_cati(y, IC, (AX0, AX1, AY0, AY1), AZ, AZ + 0.06, AZ, sacak=0.014, sacak_dis=0.016)
# the Plateresque portal: paired columns, an entablature, a pediment with the arms over it
pc = V((AX0 + AX1) / 2, AY0)
for sx in (-1, 1):
    for dx in (0.03, 0.044):
        sutun(y, pc.x + sx * dx, AY0 - 0.01, ZU - 0.04, ZU + 0.06, 0.0055, 'granit', 'korint')
kutu3(y, V(pc.x, AY0 - 0.01, ZU + 0.066), X, Y, Z, 0.11, 0.024, 0.012, 'granit', ('-y', '+x', '-x', '+z', '-z'))
alin = [V(pc.x - 0.05, AY0 - 0.018, ZU + 0.072), V(pc.x + 0.05, AY0 - 0.018, ZU + 0.072), V(pc.x, AY0 - 0.018, ZU + 0.1)]
y.yuz_yon(alin, 'tas_acik', -Y)
for p, q in ((alin[0], alin[2]), (alin[2], alin[1])):
    m = (p + q) / 2
    y.yuz_yon([p, q, q + Y * 0.018, p + Y * 0.018], 'granit', V(m.x - pc.x, -0.2, 1))
# the double-headed eagle's shield above the portal (a gold field, a red-and-white quartered shield)
kutu3(y, V(pc.x, AY0 - 0.004, ZU + 0.12), X, Y, Z, 0.044, 0.006, 0.04, 'altin', ('-y', '+x', '-x', '+z', '-z'))
for (dx, dz, k) in ((-0.008, 0.008, 'boya_kirmizi'), (0.008, 0.008, 'mermer'), (-0.008, -0.008, 'mermer'), (0.008, -0.008, 'boya_kirmizi')):
    kutu3(y, V(pc.x + dx, AY0 - 0.0085, ZU + 0.12 + dz), X, Y, Z, 0.015, 0.003, 0.015, k, ('-y', '+x', '-x', '+z', '-z'))


def alcazar_kule(cx, cy, w, z0, h, spire):
    """a corner tower: plain base, two storeys of windows, granite quoins, a cornice and the slate spire"""
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
    zt = z0 + h
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        duz_duvar(y, a, b, z0, z0 + h * 0.5, AK)
        kat(a, b, z0 + h * 0.5, z0 + h * 0.75, 1)
        kat(a, b, z0 + h * 0.75, zt, 1, v0=0.2, v1=0.7)
    for p in k:   # granite quoins
        d = (p - V(cx, cy)).normalized()
        for j in range(int(h / 0.04)):
            s = 0.022 if j % 2 == 0 else 0.016
            kutu_merkez(y, (p.x - d.x * 0.002, p.y - d.y * 0.002), s, 0.038 - s, 0.034, 'granit', z0=z0 + 0.004 + j * 0.04)
    silme(y, k, z0, 0.03, 0.01, 'granit', 'kaide')
    for zz in (z0 + h * 0.5, z0 + h * 0.75):
        silme(y, k, zz - 0.006, 0.006, 0.006, 'granit', 'duz')
    silme(y, k, zt - 0.018, 0.018, 0.012, 'granit', 'tac')
    tepe = cati_kirma(y, cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2, zt, spire, 0.014, 'arduvaz', 'kursun', ns=4, nr=6)
    y.prizma((cx, cy), 0.004, tepe - 0.01, tepe + 0.06, 'demir', n=4)
    kure(y, (cx, cy, tepe + 0.018), 0.009, 'altin', n=8, kat=4)
    kure(y, (cx, cy, tepe + 0.038), 0.0055, 'altin', n=6, kat=3)
    # a dormer on each face of the spire's foot
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        m = a.lerp(b, 0.5)
        kutu3(y, m + Z * (zt + 0.022) - nn * 0.008, e, nn, Z, 0.026, 0.026, 0.03, AK, ('+y', '+x', '-x', '+z'))
        kutu3(y, m + Z * (zt + 0.02) + nn * 0.0055, e, nn, Z, 0.012, 0.002, 0.018, 'koyu', ('+y',))
        tri = [m - e * 0.016 + nn * 0.005 + Z * (zt + 0.037), m + e * 0.016 + nn * 0.005 + Z * (zt + 0.037), m + nn * 0.005 + Z * (zt + 0.054)]
        y.yuz_yon(tri, AK, nn)
        for p, q in ((tri[0], tri[2]), (tri[2], tri[1])):
            d_ = (q - p).normalized()
            y.yuz_yon([p + nn * 0.002, q + nn * 0.002, q - nn * 0.03, p - nn * 0.03], 'arduvaz', Z - d_ * d_.z)
    return tepe + 0.06


for p in ak:
    alcazar_kule(p.x, p.y, TW, ZU - 0.045, 0.37, 0.2)
# the esplanade in front of the Alcazar
y.yuz_yon([V(AX0 - 0.06, 0.53, ZU + 0.002), V(AX1 + 0.08, 0.53, ZU + 0.002), V(AX1 + 0.08, AY0 - 0.055, ZU + 0.002), V(AX0 - 0.06, AY0 - 0.055, ZU + 0.002)],
          'zemin', Z)

calistir(y, 'lm_toledo')
