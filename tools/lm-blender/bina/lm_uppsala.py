# Uppsala Temple (lm_uppsala): the pagan temple Adam of Bremen described, built as a stave-church-like wooden hall:
# a low arcaded ambulatory under a skirt roof, the board-walled nave with a second skirt, a clerestory with crossed
# gable roofs ending in dragon heads, and a belfry tower with a shingled spire; a golden chain hangs round the eaves.
# Beside it the evergreen sacred tree and the sacred well, behind it the three great royal mounds (turf tumuli).
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from doku import MALZEME

MALZEME.setdefault('altin_v', ('duz', (0.97, 0.66, 0.13), {'leke': 0.04}))   # warm gold (Adam of Bremen: "all adorned with gold")
MALZEME.setdefault('yesil_porsuk', ('duz', (0.29, 0.44, 0.22), {'leke': 0.07}))   # lighter needle tips of the sacred yew
AL = 'altin_v'

y = Yapi()
Z0 = 0.04                       # ground top
TC = (0.12, -0.22)              # temple centre
SH = ['sindira', 'sindira2']    # shingle courses
DUV = 'ahsap_dikey'


# ---------------------------------------------------------------- helpers (Norse timber)
def kare(c, h, z=0.0):
    return dikdortgen(c[0] - h, c[0] + h, c[1] - h, c[1] + h, z)


def etek_cati(c, h_out, h_in, h_duvar, z0, z1, nr=6, kal=0.012, fas='ahsap_koyu', mahya='ahsap_koyu'):
    """a skirt (lean-to) roof round a square: its eave h_out from the centre at z0, rising to h_in at z1; a fascia
    and a soffit back to the wall (half size h_duvar) under it; hip caps on the corners"""
    out = kare(c, h_out); inn = kare(c, h_in)
    rings = [[o.lerp(i, k / nr) + Z * (z0 + (z1 - z0) * k / nr) for o, i in zip(out, inn)] for k in range(nr + 1)]
    for k in range(nr):
        y.serit(rings[k], rings[k + 1], SH[k % 2])
    y.serit([p - Z * kal for p in rings[0]], rings[0], fas)
    wall = kare(c, h_duvar, z0 - kal)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([rings[0][i] - Z * kal, rings[0][j] - Z * kal, wall[j], wall[i]], 'ahsap_koyu', -Z)
    for i in range(4):
        cubuk(y, rings[0][i] + Z * 0.004, rings[-1][i] + Z * 0.004, 0.008, mahya, 0.006)


def ejder(p, d, s=1.0, key='ahsap_koyu'):
    """a carved dragon head on a ridge end: a neck curving out (d: outward, horizontal) and up, a long snout, a
    curled crest"""
    d = V(d[0], d[1]).normalized() * s
    up = Z * s
    neck = [p - d * 0.01, p + d * 0.018 + up * 0.016, p + d * 0.03 + up * 0.042, p + d * 0.026 + up * 0.068]
    boru(y, neck, 0.012 * s, key, n=8, r_son=0.01 * s)
    hp = neck[-1]
    kure(y, hp, 0.012 * s, key, n=8, kat=4)
    boru(y, [hp, hp + d * 0.026 + up * 0.004, hp + d * 0.05 + up * 0.002], 0.009 * s, key, n=6, r_son=0.005 * s)     # upper jaw
    boru(y, [hp - up * 0.006, hp + d * 0.02 - up * 0.012, hp + d * 0.04 - up * 0.02], 0.005 * s, key, n=5, r_son=0.003 * s)   # open lower jaw
    boru(y, [hp + d * 0.048, hp + d * 0.044 - up * 0.012], 0.0028 * s, 'boya_kirmizi', n=4, r_son=0.002 * s)                 # tongue
    boru(y, [hp - d * 0.006 + up * 0.008, hp - d * 0.018 + up * 0.026, hp - d * 0.034 + up * 0.028, hp - d * 0.038 + up * 0.016],
         0.005 * s, key, n=5, r_son=0.002 * s)   # curled crest
    for sd in (-1, 1):   # gilded eyes
        w = V(-d.y, d.x).normalized()
        kure(y, hp + d * 0.012 + up * 0.008 + w * (sd * 0.008 * s), 0.0034 * s, 'altin', n=6, kat=3)

def elips(c, rx, rz, key, n=14, kat=6):
    """a flattened round clump of foliage (ellipsoid), centre c"""
    pr = [(rx * math.sin(math.pi * k / kat), c[2] - rz * math.cos(math.pi * k / kat)) for k in range(kat + 1)]
    pr[0] = (0.0, pr[0][1]); pr[-1] = (0.0, pr[-1][1])
    donel(y, c, pr, key, n=n)


def zincir(pts, sark=0.025, r=0.0028, halka=0):
    """a golden chain hanging in loops between the points of a closed ring; halka: that many links (beads) per loop"""
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        m = 12
        yol = [a.lerp(b, t / m) - Z * (sark * 4 * (t / m) * (1 - t / m)) for t in range(m + 1)]
        boru(y, yol, r, AL, n=6, kapat=True)
        kure(y, a, r * 2.4, AL, n=8, kat=4)
        for k in range(1, halka):
            t = k / halka
            kure(y, a.lerp(b, t) - Z * (sark * 4 * t * (1 - t)), r * 1.6, AL, n=6, kat=3)


# ---------------------------------------------------------------- ground
y.bolum('Zemin: çimenli düzlük, yollar')
GX0, GX1, GY0, GY1 = -1.18, 1.18, -0.98, 1.08
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'toprak', 'onarkasagsol')
y.yuz_yon([V(GX0, GY0, Z0), V(GX1, GY0, Z0), V(GX1, GY1, Z0), V(GX0, GY1, Z0)], 'cimen', Z)
silme(y, dikdortgen(GX0, GX1, GY0, GY1), Z0 - 0.012, 0.012, 0.004, 'cimen_kuru', 'duz')
ZP = Z0 + 0.003


def yol(pts, en):
    """a trodden earth path along a polyline, its edge stones"""
    for k in range(len(pts) - 1):
        a, b = V(*pts[k]), V(*pts[k + 1])
        e = (b - a).normalized(); n = V(-e.y, e.x) * (en / 2)
        y.yuz_yon([a - n + Z * ZP, b - n + Z * ZP, b + n + Z * ZP, a + n + Z * ZP], 'toprak', Z)
        L = (b - a).length
        m = int(L / 0.06)
        for j in range(m):
            for s in (-1, 1):
                p = a.lerp(b, (j + 0.5) / m) + n * s * 1.12
                kutu_merkez(y, (p.x, p.y), 0.018, 0.013, 0.008, 'granit' if (j + s) % 3 else 'granit_koyu', z0=Z0, aci=0.5 * j + s)


yol([(TC[0], GY0 + 0.01), (TC[0], TC[1] - 0.47)], 0.12)
yol([(TC[0] - 0.06, TC[1] - 0.6), (-0.62, -0.62)], 0.07)
yol([(TC[0] + 0.4, TC[1] + 0.1), (0.56, 0.38), (0.0, 0.52)], 0.07)

# ---------------------------------------------------------------- royal mounds
y.bolum('Kraliyet höyükleri')


def hoyuk(c, R, H):
    pr = [(R * 1.04, Z0 - 0.004), (R, Z0 + H * 0.06), (R * 0.93, Z0 + H * 0.3), (R * 0.8, Z0 + H * 0.56), (R * 0.62, Z0 + H * 0.78),
          (R * 0.4, Z0 + H * 0.93), (R * 0.18, Z0 + H * 0.99), (0.0, Z0 + H)]
    donel(y, c, pr, 'cimen', n=40)
    # a ring of kerb stones at the foot
    for i in range(18):
        a = TAU * (i + 0.3) / 18
        kutu_merkez(y, (c[0] + R * 1.08 * math.cos(a), c[1] + R * 1.08 * math.sin(a)), 0.028, 0.02, 0.016 + 0.006 * (i % 2),
                    'granit' if i % 3 else 'granit_koyu', z0=Z0 - 0.002, aci=a)


HOY = [((-0.74, 0.66), 0.36, 0.3), ((0.06, 0.74), 0.34, 0.27), ((0.8, 0.62), 0.33, 0.25)]
for c, R, H in HOY:
    hoyuk(c, R, H)


def hoy_z(c, R, H, d):
    """the height of a mound's surface at distance d from its centre (the profile above, interpolated)"""
    pr = [(R * 1.04, Z0 - 0.004), (R, Z0 + H * 0.06), (R * 0.93, Z0 + H * 0.3), (R * 0.8, Z0 + H * 0.56), (R * 0.62, Z0 + H * 0.78),
          (R * 0.4, Z0 + H * 0.93), (R * 0.18, Z0 + H * 0.99), (0.0, Z0 + H)]
    for (r0, z0), (r1, z1) in zip(pr, pr[1:]):
        if r1 <= d <= r0: return z0 + (z1 - z0) * (r0 - d) / max(r0 - r1, 1e-9)
    return Z0


# juniper bushes and tufts of dry grass on the mounds' flanks, a trodden path up the middle one
for m, (c, R, H) in enumerate(HOY):
    for i in range(9):
        a = TAU * (i * 0.37 + m * 0.21)
        d = R * (0.35 + 0.5 * ((i * 3 + m) % 5) / 4)
        p = V(c[0] + d * math.cos(a), c[1] + d * math.sin(a))
        z = hoy_z(c, R, H, d)
        if i % 3 == 0:
            donel(y, (p.x, p.y), [(0.012, z - 0.006), (0.02, z + 0.012), (0.012, z + 0.04), (0.0, z + 0.06)], 'yesil_koyu', n=7)
        else:
            elips(V(p.x, p.y, z + 0.004), 0.016 + 0.004 * (i % 2), 0.012, 'cimen_kuru' if i % 2 else 'yesil_koyu', n=7, kat=3)

# ---------------------------------------------------------------- the temple
y.bolum('Tapınak: taş temel ve dış galeri (svalgang)')
HA = 0.36          # ambulatory half size
ZA0 = Z0 + 0.035   # sill top
ZA1 = ZA0 + 0.15   # ambulatory wall top
kutu(y, V(TC[0] - HA - 0.025, TC[1] - HA - 0.025, Z0 - 0.01), X, 2 * HA + 0.05, 2 * HA + 0.05, ZA0 - Z0 + 0.01, 'granit', 'onarkasagsolust')
silme(y, kare(TC, HA + 0.025), ZA0 - 0.008, 0.008, 0.005, 'granit_koyu', 'duz')
k = kare(TC, HA)
RENK = (DUV, 'ahsap_koyu', 'ahsap_acik', 'koyu')
NB = 5
for i in range(4):
    a, b = k[i], k[(i + 1) % 4]
    for j in range(NB):
        p, q = a.lerp(b, j / NB), a.lerp(b, (j + 1) / NB)
        if i == 0 and j == NB // 2:
            kapi(y, p, q, ZA0, 0.6, 0.15, (DUV, 'ahsap_koyu', 'ahsap_acik', 'ahsap'), derin=0.03, cerceve=(0.007, ['ahsap_acik', 'boya_kirmizi']))
        else:
            y.kemerli(p, q, ZA0, 0.15, RENK, v0=0.055, en=0.56, ust=0.02, derin=0.03, k_say=8, cerceve=(0.005, 'ahsap_acik'))
    # posts at the bay lines (small carved columns), a sill rail
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for j in range(NB + 1):
        p = a.lerp(b, j / NB) + nn * 0.005
        kutu_merkez(y, (p.x, p.y), 0.016, 0.016, ZA1 - ZA0, 'ahsap', z0=ZA0, aci=math.atan2(e.y, e.x))
        kutu_merkez(y, (p.x, p.y), 0.02, 0.02, 0.012, AL, z0=ZA1 - 0.03, aci=math.atan2(e.y, e.x))
    kutu(y, a + nn * 0.006 + Z * (ZA0 + 0.05) - e * 0.008, e, (b - a).length + 0.016, 0.012, 0.01, 'ahsap', 'onust')
    kutu(y, a + nn * 0.006 + Z * (ZA1 - 0.016) - e * 0.008, e, (b - a).length + 0.016, 0.012, 0.016, 'ahsap', 'onust')
HB = 0.25          # nave half size
ZB1 = 0.56
etek_cati(TC, HA + 0.05, HB, HA, ZA1, ZA1 + 0.12, nr=6, fas='boya_kirmizi', mahya=AL)

y.bolum('Tapınak: ana gövde (nef) ve ikinci etek çatı')
kB = kare(TC, HB)
for i in range(4):
    a, b = kB[i], kB[(i + 1) % 4]
    duz_duvar(y, a, b, ZA1 + 0.1, ZB1, DUV)
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    # battens over the board joints
    for j in range(1, 14):
        p = a.lerp(b, j / 14) + nn * 0.003
        kutu_merkez(y, (p.x, p.y), 0.006, 0.006, ZB1 - ZA1 - 0.1, 'ahsap', z0=ZA1 + 0.1, aci=math.atan2(e.y, e.x))
    # small round windows high on the wall
    for u in (0.3, 0.7):
        o = a.lerp(b, u) + Z * (ZB1 - 0.075)
        y.oculus(o, e, nn, 0.016, 'koyu', 'ahsap_acik', f=0.006, k=10)
    for cp in (a, ):   # corner posts
        kutu_merkez(y, (cp.x, cp.y), 0.026, 0.026, ZB1 - ZA1 - 0.1 + 0.01, 'ahsap_koyu', z0=ZA1 + 0.1, aci=0.0)
HC = 0.17
ZC1 = 0.79
etek_cati(TC, HB + 0.045, HC, HB, ZB1, ZB1 + 0.1, nr=6, fas=AL, mahya='boya_kirmizi')
# the golden chain round the second skirt
zincir([p + Z * (ZB1 - 0.016) for p in kare(TC, HB + 0.052)], sark=0.06, r=0.0048, halka=14)
# a second chain hung in deep loops between the corner posts of the ambulatory eave
zincir([p + Z * (ZA1 - 0.004) for p in kare(TC, HA + 0.056)], sark=0.05, r=0.004, halka=16)

y.bolum('Tapınak: üst kat, çapraz kırma çatılar, ejder başları')
kC = kare(TC, HC)
for i in range(4):
    a, b = kC[i], kC[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    duz_duvar(y, a, b, ZB1 + 0.08, ZC1, DUV)
    # three small arched windows (a gallery of light under the roofs)
    for u in (0.25, 0.5, 0.75):
        o = a.lerp(b, u) - e * 0.014
        y.pencere(o + Z * 0.0, e, nn, 0, ZC1 - 0.12, 0.028, 0.07, 'koyu', kemer=True, k_say=5)
        cubuk(y, o + nn * 0.004 + Z * (ZC1 - 0.124), o + e * 0.028 + nn * 0.004 + Z * (ZC1 - 0.124), 0.006, 'ahsap_acik', 0.004)
    kutu_merkez(y, (a.x, a.y), 0.024, 0.024, ZC1 - ZB1 - 0.08, 'ahsap_koyu', z0=ZB1 + 0.08)
silme(y, kC, ZC1 - 0.012, 0.012, 0.008, 'ahsap', 'duz')
HR = 0.26          # gable roof height
SAC = 0.04
cx, cy = TC
r1 = cati_besik(y, cx - HC, cx + HC, cy - HC + 0.004, cy + HC - 0.004, ZC1, HR, SAC, 'sindira', 'ahsap_koyu', ucluk_key=DUV,
                dilim=SH, nr=8, alinlik_key='ahsap_acik')
r2 = cati_besik(y, cx - HC + 0.004, cx + HC - 0.004, cy - HC, cy + HC, ZC1, HR - 0.002, SAC, 'sindira', 'ahsap_koyu', ucluk_key=DUV,
                dilim=SH, nr=8, alinlik_key='ahsap_acik')
ZR = ZC1 + HR
for d in (X, -X, Y, -Y):
    w = V(-d.y, d.x)
    g = V(cx, cy, 0) + d * (HC + SAC + 0.006)
    for s in (-1, 1):   # barge boards (painted red, a gilded edge) from the eave up past the ridge
        p0 = g + w * s * (HC + 0.035) + Z * (ZC1 - 0.01)
        p1 = g + Z * (ZR + 0.004)
        cubuk(y, p0, p1 + (p1 - p0).normalized() * 0.03, 0.02, 'boya_kirmizi', 0.01)
        cubuk(y, p0 + d * 0.006 - Z * 0.008, p1 + d * 0.006 - Z * 0.008, 0.006, AL, 0.012)
    o = V(cx, cy, 0) + d * (HC + 0.003) + Z * (ZC1 + HR * 0.38)
    for k, (r, key) in enumerate(((0.05, AL), (0.036, 'boya_kirmizi'), (0.02, AL))):
        ring = [o + d * (0.003 * k) + w * (r * math.cos(TAU * i / 14)) + Z * (r * math.sin(TAU * i / 14)) for i in range(14)]
        y.yuz_yon(ring, key, d)
        for i in range(14):
            yuz_dis(y, [ring[i], ring[(i + 1) % 14], ring[(i + 1) % 14] - d * 0.003, ring[i] - d * 0.003], key, o - d * 0.01)
    for i in range(8):   # rays
        a = TAU * (i + 0.5) / 8
        q = w * math.cos(a) + Z * math.sin(a)
        cubuk(y, o + q * 0.05 + d * 0.002, o + q * 0.075 + d * 0.002, 0.008, AL, 0.005)
for d in (X, -X, Y, -Y):
    ejder(V(cx, cy, ZR + 0.02) + d * (HC + SAC + 0.02), d, 1.35)

y.bolum('Tapınak: çan kulesi ve sivri kule')
HT = 0.08
ZT0 = ZC1 + 0.1
ZT1 = ZR + 0.1
kT = kare(TC, HT)
duvarlar(y, kT, ZT0, ZT1, DUV)
etek_cati(TC, HT + 0.045, HT - 0.02, HT, ZT1, ZT1 + 0.05, nr=4, fas=AL)
HT2 = HT - 0.02
ZT2 = ZT1 + 0.04
ZT3 = ZT2 + 0.12
kT2 = kare(TC, HT2)
for i in range(4):
    a, b = kT2[i], kT2[(i + 1) % 4]
    for j in range(2):
        p, q = a.lerp(b, j / 2), a.lerp(b, (j + 1) / 2)
        y.kemerli(p, q, ZT2, ZT3 - ZT2, RENK, v0=0.02, en=0.5, ust=0.015, derin=0.02, k_say=6, cerceve=(0.004, 'ahsap_acik'))
silme(y, kT2, ZT3 - 0.006, 0.01, 0.006, 'ahsap', 'duz')
top = cati_kirma(y, cx - HT2, cx + HT2, cy - HT2, cy + HT2, ZT3, 0.36, 0.035, 'sindira', 'ahsap_koyu', dilim=SH, ns=6, nr=10)
# small dragon heads at the spire's eaves and a gilded finial
for d in (V(1, 1), V(1, -1), V(-1, 1), V(-1, -1)):
    ejder(V(cx, cy, ZT3 + 0.006) + d.normalized() * (HT2 + 0.035) * 1.41, d, 0.8)
y.prizma(TC, 0.005, top - 0.01, top + 0.07, 'altin', n=6)
kure(y, (cx, cy, top + 0.025), 0.011, 'altin', n=8, kat=4)
kure(y, (cx, cy, top + 0.07), 0.008, 'altin', n=8, kat=4)

y.bolum('Tapınak: giriş sundurması')
# a gabled porch before the door, on carved posts, with its own dragon head
PY0 = TC[1] - HA - 0.13
for sx in (-1, 1):
    for yy in (PY0 + 0.01, TC[1] - HA - 0.01):
        sutun(y, cx + sx * 0.06, yy, ZA0 - 0.02, ZA0 + 0.13, 0.008, 'ahsap', 'ahsap')
kutu(y, V(cx - 0.085, PY0 - 0.01, Z0), X, 0.17, TC[1] - HA - PY0 + 0.01, ZA0 - Z0 - 0.02, 'granit', 'onsagsolust')
merdiven(y, (cx, PY0 - 0.01 - 0.06), math.pi / 2, 0.12, Z0, ZA0 - 0.02, n=2, d=0.03, key='granit')
rp = cati_besik(y, cx - 0.07, cx + 0.07, PY0, TC[1] - HA + 0.02, ZA0 + 0.13, 0.1, 0.02, 'sindira', 'ahsap_koyu', ucluk_key=DUV,
                dilim=SH, nr=5, alinlik_key='ahsap_acik')
ejder(V(cx, PY0 - 0.02, rp + 0.002), -Y, 0.9)

# ---------------------------------------------------------------- sacred tree
y.bolum('Kutsal ağaç')
AT = (-0.72, -0.2)
gov = [V(AT[0], AT[1], Z0 - 0.01), V(AT[0] + 0.01, AT[1], Z0 + 0.15), V(AT[0] - 0.005, AT[1] + 0.01, Z0 + 0.32), V(AT[0], AT[1], Z0 + 0.46)]
boru(y, gov, 0.032, 'ahsap_koyu', n=10, r_son=0.016)
for i in range(5):   # roots
    a = TAU * i / 5 + 0.3
    d = V(math.cos(a), math.sin(a))
    boru(y, [V(AT[0], AT[1], Z0 + 0.04) + d * 0.015, V(AT[0], AT[1], Z0 + 0.01) + d * 0.06, V(AT[0], AT[1], Z0 - 0.004) + d * 0.09], 0.012, 'ahsap_koyu', n=5, r_son=0.004)




# a broad old evergreen (yew-like): spreading limbs carrying layered flat clumps of dark needles
# many smaller layered clumps (two shades of needles) in tiers on limbs: reads as a dense old yew, not a few balls
DAL = []
for k in range(30):
    a = TAU * k * 0.618 + 0.3
    t = ((k * 7) % 30) / 29                       # 0 low .. 1 high
    rr = (0.25 - 0.13 * t) * (0.5 + 0.5 * ((k * 5) % 7) / 6)
    DAL.append((rr * math.cos(a), rr * math.sin(a), 0.36 + 0.5 * t, 0.085 - 0.03 * t, 0.042 - 0.012 * t))
DAL.append((0.0, 0.0, 0.9, 0.06, 0.04))
for k, (dx, dy, dz, r, rz) in enumerate(DAL):
    c = V(AT[0] + dx, AT[1] + dy, Z0 + dz)
    if abs(dx) + abs(dy) > 0.03:
        boru(y, [V(AT[0], AT[1], Z0 + min(0.44, dz - 0.08)), V(AT[0] + dx * 0.6, AT[1] + dy * 0.6, Z0 + dz - 0.03), c - Z * rz * 0.5],
             0.009, 'ahsap_koyu', n=5, r_son=0.004)
    elips(c, r, rz * 1.25, 'yesil_koyu' if k % 3 else 'yesil_porsuk', n=12)
    elips(c + Z * rz * 0.7 + V(r * 0.15, -r * 0.1, 0), r * 0.62, rz * 0.9, 'yesil_koyu', n=10, kat=4)


def cam(x, yy, boy, r=None):
    """a spruce of the sacred grove: a trunk and three stacked cones of dark needles"""
    r = r or boy * 0.3
    y.prizma((x, yy), 0.008, Z0 - 0.004, Z0 + boy * 0.25, 'ahsap_koyu', n=5)
    for k in range(3):
        z = Z0 + boy * (0.14 + 0.26 * k)
        rr = r * (1 - 0.24 * k)
        donel(y, (x, yy), [(rr * 0.35, z), (rr, z + 0.012), (rr * 0.45, z + boy * 0.3), (0.0, z + boy * (0.42 if k == 2 else 0.34))], 'yesil_koyu', n=10)
        y.yuz_yon([V(p.x, p.y, z) for p in cokgen((x, yy), rr * 0.35, 10)], 'yesil_koyu', -Z)


y.bolum('Kutsal koru: ladinler')
for (tx, ty, tb) in ((-1.06, 0.16, 0.34), (-0.98, -0.02, 0.26), (-0.3, 0.2, 0.3), (0.45, 0.3, 0.32), (1.06, 0.22, 0.3),
                     (1.04, 0.98, 0.28), (-1.08, 0.98, 0.3), (-0.34, 0.98, 0.24), (0.46, 0.99, 0.26)):
    cam(tx, ty, tb)

y.bolum('Kutsal kuyu ve kurban taşı')
KU = (-0.5, -0.66)
RW, RI = 0.07, 0.052
donel(y, KU, [(RW + 0.004, Z0 - 0.004), (RW, Z0 + 0.05), (RI, Z0 + 0.05)], 'granit', n=20)
donel(y, KU, [(RI, Z0 + 0.05), (RI, Z0 + 0.005)], 'granit_koyu', n=20)
y.yuz_yon([V(p.x, p.y, Z0 + 0.02) for p in cokgen(KU, RI, 20)], 'su', Z)
for k in range(10):   # rough stones on the rim
    a = TAU * k / 10
    kutu_merkez(y, (KU[0] + (RW + RI) / 2 * math.cos(a), KU[1] + (RW + RI) / 2 * math.sin(a)), 0.026, 0.02, 0.012, 'granit' if k % 2 else 'granit_koyu', z0=Z0 + 0.048, aci=a + 0.2)
# the timber frame and the windlass
for sx in (-1, 1):
    cubuk(y, V(KU[0] + sx * 0.085, KU[1], Z0), V(KU[0] + sx * 0.085, KU[1], Z0 + 0.15), 0.012, 'ahsap')
cubuk(y, V(KU[0] - 0.1, KU[1], Z0 + 0.125), V(KU[0] + 0.1, KU[1], Z0 + 0.125), 0.016, 'kutuk')
cati_besik(y, KU[0] - 0.1, KU[0] + 0.1, KU[1] - 0.05, KU[1] + 0.05, Z0 + 0.15, 0.06, 0.015, 'ahsap_koyu', 'ahsap_koyu', ucluk_key='ahsap', ns=4, nr=3)
boru(y, [V(KU[0], KU[1], Z0 + 0.12), V(KU[0], KU[1], Z0 + 0.06)], 0.0018, 'ahsap_koyu', n=4)
kutu_merkez(y, KU, 0.02, 0.02, 0.022, 'ahsap', z0=Z0 + 0.04)
# the offering stone (hörgr): a pile of stones with a flat slab
HG = (-0.32, -0.5)
for k, (dx, dy, w) in enumerate(((0, 0, 0.09), (0.03, 0.03, 0.07), (-0.03, 0.02, 0.06), (0.02, -0.03, 0.06))):
    kutu_merkez(y, (HG[0] + dx, HG[1] + dy), w, w * 0.8, 0.03 - 0.005 * k, 'granit_koyu' if k % 2 else 'granit', z0=Z0 - 0.004, aci=0.4 * k)
kutu_merkez(y, HG, 0.11, 0.08, 0.012, 'granit', z0=Z0 + 0.026, aci=0.2)

y.bolum('Runik taşlar, meşaleler')


def runtasi(x, yy, h, aci):
    with parca(y, (x, yy, Z0 - 0.004), aci):
        kutu_merkez(y, (0, 0), 0.05, 0.022, h, 'granit')
        # the painted serpent band (red) on the face
        for k in range(6):
            t0, t1 = k / 6, (k + 1) / 6
            p0 = V(-0.018 * math.cos(math.pi * t0), -0.0115, h * (0.15 + 0.75 * t0))
            p1 = V(-0.018 * math.cos(math.pi * t1), -0.0115, h * (0.15 + 0.75 * t1))
            y.yuz_yon([p0 - X * 0.004, p0 + X * 0.004, p1 + X * 0.004, p1 - X * 0.004], 'boya_kirmizi', -Y)


runtasi(0.6, -0.78, 0.13, 0.3)
runtasi(0.78, -0.7, 0.11, -0.2)
runtasi(-0.95, -0.72, 0.12, 0.5)

# a stone ship (skeppssättning): standing stones in a ship's outline, tallest at the stem and stern
SS = (0.86, -0.08)
for k in range(18):
    t = TAU * k / 18
    px, py = SS[0] + 0.1 * math.sin(t), SS[1] + 0.25 * math.cos(t)
    uc = abs(math.cos(t))
    h = 0.03 + 0.05 * uc ** 6
    kutu_merkez(y, (px, py), 0.026, 0.018, h, 'granit' if k % 3 else 'granit_koyu', z0=Z0 - 0.004, aci=t)


def mesale(x, yy):
    cubuk(y, V(x, yy, Z0), V(x, yy, Z0 + 0.13), 0.008, 'ahsap_koyu')
    donel(y, (x, yy), [(0.006, Z0 + 0.12), (0.014, Z0 + 0.135), (0.012, Z0 + 0.142), (0.0, Z0 + 0.142)], 'demir', n=8)
    donel(y, (x, yy), [(0.009, Z0 + 0.142), (0.006, Z0 + 0.16), (0.0, Z0 + 0.175)], 'boya_sari', n=6)


for sx in (-1, 1):
    mesale(cx + sx * 0.12, PY0 - 0.12)
    mesale(cx + sx * 0.12, GY0 + 0.1)

y.bolum('Çit (gärdesgård)')


def cit(pts, adim=0.085, h=0.07):
    """a Scandinavian roundpole fence: pairs of upright posts tied together, slanted poles laid between them"""
    for k in range(len(pts) - 1):
        a, b = V(*pts[k]), V(*pts[k + 1])
        e = (b - a).normalized(); nn = V(-e.y, e.x)
        n = max(1, int((b - a).length / adim))
        for j in range(n + 1):
            p = a.lerp(b, j / n)
            for s in (-1, 1):
                cubuk(y, p + nn * (s * 0.006) + Z * (Z0 - 0.004), p + nn * (s * 0.006) + Z * (Z0 + h), 0.006, 'ahsap_koyu')
            if j < n:
                q = a.lerp(b, (j + 1) / n)
                for t in (0.0, 0.33, 0.66):
                    p0 = p.lerp(q, t) + Z * (Z0 + 0.008)
                    p1 = p.lerp(q, t + 0.55) + Z * (Z0 + h * 0.85)
                    cubuk(y, p0, p1, 0.006, 'ahsap', 0.005)


cit([(GX0 + 0.06, GY0 + 0.06), (TC[0] - 0.12, GY0 + 0.06)])
cit([(TC[0] + 0.12, GY0 + 0.06), (GX1 - 0.06, GY0 + 0.06)])
cit([(GX0 + 0.06, GY0 + 0.06), (GX0 + 0.06, -0.35)])
cit([(GX1 - 0.06, GY0 + 0.06), (GX1 - 0.06, -0.4)])

y.bolum('Sancak')
sancak(y, 0.6, -0.5, Z0, boy=0.42, en=0.12, yuk=0.075, aci=0.4, kuyruk=True)

calistir(y, 'lm_uppsala')
