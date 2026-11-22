# Okçuluk Köşkü (lm_okculukpavyon): a Korean archery pavilion (hwal-teo) after Hwanghakjeong in Seoul: an open timber
# pavilion with a raised wooden floor on stone pillars, red round posts, a railing, dancheong-painted beams and brackets and
# a deep paljak roof, on a granite base at the top of a pine-covered slope; before it the paved shooting line with archers
# at full draw, the stone stair down the slope, and across the range the target boards before an earth berm, with signal
# flags and the markers' shelter.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ortak import *
from bina_ortak import calistir
import doku

y = Yapi()
rn = random.Random(7)
Z0 = 0.03
HT = 0.2                     # the hilltop above the range
GX0, GX1, GY0, GY1 = -1.15, 1.15, -1.12, 1.12


def yuk(px, py):
    """ground height: the range in front, the slope, the flat hilltop round the pavilion, knolls at the back corners"""
    s = ss(-0.34, 0.26, py + 0.05 * math.cos(px * 2.4))
    h = HT * s
    h += 0.13 * math.exp(-(((px + 0.95) / 0.32) ** 2 + ((py - 0.85) / 0.4) ** 2))
    h += 0.11 * math.exp(-(((px - 0.95) / 0.3) ** 2 + ((py - 0.75) / 0.45) ** 2))
    h += 0.07 * math.exp(-(((px - 1.0) / 0.25) ** 2 + ((py + 0.2) / 0.3) ** 2))
    # the earth berm behind the targets
    h += 0.07 * math.exp(-((py + 1.02) / 0.06) ** 2) * ss(0.78, 0.6, abs(px))
    # keep the pavilion's hilltop and the shooting line flat
    d = math.hypot(max(0.0, abs(px) - 0.62), max(0.0, 0.3 - py, py - 1.0))
    m = ss(0.0, 0.18, d)
    h = h * m + HT * (1 - m)
    return Z0 + h


def arazi_renk(x, yy, z):
    e = 0.012
    gx = (yuk(x + e, yy) - yuk(x - e, yy)) / (2 * e)
    gy = (yuk(x, yy + e) - yuk(x, yy - e)) / (2 * e)
    s = math.hypot(gx, gy)
    n = 0.7 * math.sin(x * 4.1 + 1.3) * math.cos(yy * 3.3 - 0.4) + 0.3 * math.sin(x * 9.3 - yy * 7.1)
    c = karis((0.43, 0.53, 0.27), (0.5, 0.56, 0.3), 0.5 + 0.5 * n)            # turf
    c = karis(c, (0.36, 0.44, 0.24), ss(0.25, 0.8, s) * 0.8)                  # the shaded slope under the pines
    c = karis(c, (0.55, 0.5, 0.36), ss(0.9, 1.6, s + 0.3 * n))                 # bare earth where it is steep
    # the mown range: a lighter strip down the middle
    c = karis(c, (0.55, 0.62, 0.33), ss(0.72, 0.5, abs(x)) * ss(-0.32, -0.42, yy) * 0.7)
    return c


doku.KOSE_RENK['toprak_ot'] = arazi_renk
y.bolum('Arazi: tepe ve atış alanı')
arazi(y, yuk, GX0, GX1, GY0, GY1, 32, 32, 'toprak_ot', etek=0.0, etek_key='katman')
ZT = Z0 + HT

# ---------------- pavilion ----------------
PX0, PX1, PY0, PY1 = -0.46, 0.46, 0.52, 0.9
y.bolum('Köşk: kaide ve taş ayaklar')
zb = gidan(y, PX0 - 0.09, PX1 + 0.09, PY0 - 0.09, PY1 + 0.09, ZT - 0.02, 0.07, basamak=((0, 0.5, 0.22),))
ZF = zb + 0.075
xs = [PX0 + (PX1 - PX0) * i / 4 for i in range(5)]
ys = [PY0, (PY0 + PY1) / 2, PY1]
cevre = [(x, PY0) for x in xs] + [(x, PY1) for x in xs] + [(PX0, ys[1]), (PX1, ys[1])]
for (x, yy) in cevre + [(xs[2], ys[1])]:
    y.prizma((x, yy), 0.02, zb, ZF - 0.016, 'granit', n=8, kat=math.pi / 8)
    y.prizma((x, yy), 0.026, zb, zb + 0.01, 'granit', n=8, kat=math.pi / 8)
# the floor: a deck a little beyond the posts, its fascia, underside, planks
DX0, DX1, DY0, DY1 = PX0 - 0.055, PX1 + 0.055, PY0 - 0.055, PY1 + 0.055
kutu(y, V(DX0, DY0, ZF - 0.016), X, DX1 - DX0, DY1 - DY0, 0.016, 'ahsap')
y.yuz_yon([V(DX0, DY0, ZF - 0.016), V(DX1, DY0, ZF - 0.016), V(DX1, DY1, ZF - 0.016), V(DX0, DY1, ZF - 0.016)], 'ahsap_koyu', -Z)
for k in range(1, 22):
    x = DX0 + (DX1 - DX0) * k / 22
    y.yuz_yon([V(x - 0.0009, DY0 + 0.002, ZF + 0.0006), V(x + 0.0009, DY0 + 0.002, ZF + 0.0006), V(x + 0.0009, DY1 - 0.002, ZF + 0.0006),
               V(x - 0.0009, DY1 - 0.002, ZF + 0.0006)], 'ahsap_koyu', Z)
# beams under the deck between the stone pillars
for yy in ys:
    cubuk(y, V(DX0 + 0.01, yy, ZF - 0.024), V(DX1 - 0.01, yy, ZF - 0.024), 0.016, 'ahsap_koyu', 0.016)
# a wooden stair from the base up to the deck at the front middle
merdiven(y, V(0, DY0 - 0.075), math.pi / 2, 0.16, zb, ZF, n=4, d=0.019, key='ahsap', yanlik='ahsap_koyu')

y.bolum('Köşk: direkler ve korkuluk')
HP = 0.24
for (x, yy) in cevre:
    y.prizma((x, yy), 0.0135, ZF, ZF + HP, 'kirmizi', n=10)
    donel(y, (x, yy), [(0.0, ZF), (0.019, ZF), (0.017, ZF + 0.008), (0.0135, ZF + 0.01)], 'granit_acik', n=10)   # a stone post seat


def korkuluk_kore(a, b, z, h=0.045, key='ahsap_acik', ray='kirmizi'):
    """a gyeja railing along a->b on the deck edge (facing the right): balusters, rails, and the curved brackets standing
    out from the bottom rail to hold the top rail beyond the deck"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    cubuk(y, a + Z * (z + 0.006), b + Z * (z + 0.006), 0.008, key, 0.012)
    cubuk(y, a + Z * (z + h * 0.55), b + Z * (z + h * 0.55), 0.005, key, 0.006)
    cubuk(y, a + nn * 0.012 + Z * (z + h), b + nn * 0.012 + Z * (z + h), 0.007, ray, 0.007)
    m = max(2, int(L / 0.022))
    for k in range(1, m):
        p = a.lerp(b, k / m)
        cubuk(y, p + Z * (z + 0.012), p + Z * (z + h * 0.55), 0.0035, key)
    for k in range(int(L / 0.07) + 1):
        p = a.lerp(b, (k + 0.5) / (int(L / 0.07) + 1))
        boru(y, [p + Z * (z + h * 0.5), p + nn * 0.004 + Z * (z + h * 0.72), p + nn * 0.012 + Z * (z + h * 0.92), p + nn * 0.012 + Z * (z + h)],
             0.003, key, n=4)
    # the lattice panel along the lower part (yeop)
    for k in range(m):
        p = a.lerp(b, (k + 0.5) / m) + nn * 0.0005
        y.yuz_yon([p - e * 0.004 + Z * (z + 0.02), p + e * 0.004 + Z * (z + 0.02), p + e * 0.004 + Z * (z + 0.023), p - e * 0.004 + Z * (z + 0.023)],
                  ray, nn)


RI = 0.012
rk = dikdortgen(DX0 + RI, DX1 - RI, DY0 + RI, DY1 - RI)
korkuluk_kore(rk[0], V(-0.09, rk[0].y), ZF)
korkuluk_kore(V(0.09, rk[0].y), rk[1], ZF)
for i in (1, 2, 3):
    korkuluk_kore(rk[i], rk[(i + 1) % 4], ZF)
for p in rk + [V(-0.09, rk[0].y), V(0.09, rk[0].y)]:
    kutu_merkez(y, (p.x, p.y), 0.012, 0.012, 0.055, 'kirmizi', z0=ZF)
    kure(y, (p.x, p.y, ZF + 0.06), 0.0075, 'kirmizi', n=8, kat=4)

y.bolum('Köşk: dancheong ve tavan')
zd = dancheong(y, dikdortgen(PX0, PX1, PY0, PY1), ZF + HP, 0.04, adim=0.115)
y.yuz_yon([V(PX0, PY0, zd), V(PX1, PY0, zd), V(PX1, PY1, zd), V(PX0, PY1, zd)], 'boya_yesil', -Z)
# painted ceiling coffers seen from under the eaves
for i in range(4):
    for j in range(2):
        cx_, cy_ = PX0 + (PX1 - PX0) * (i + 0.5) / 4, PY0 + (PY1 - PY0) * (j + 0.5) / 2
        y.yuz_yon([V(cx_ - 0.05, cy_ - 0.04, zd - 0.0015), V(cx_ + 0.05, cy_ - 0.04, zd - 0.0015), V(cx_ + 0.05, cy_ + 0.04, zd - 0.0015),
                   V(cx_ - 0.05, cy_ + 0.04, zd - 0.0015)], 'turkuaz', -Z)
# the name board (hyeonpan) hung on the front beam
kutu(y, V(-0.075, PY0 - 0.024, ZF + HP - 0.012), X, 0.15, 0.008, 0.058, 'lake_koyu')
kutu(y, V(-0.062, PY0 - 0.0255, ZF + HP - 0.004), X, 0.124, 0.002, 0.042, 'koyu', 'onsagsolust')
for k in range(3):
    kutu(y, V(-0.05 + k * 0.036, PY0 - 0.0265, ZF + HP + 0.006), X, 0.026, 0.0012, 0.022, 'altin', 'onsagsolust')
y.bolum('Köşk: çatı')
tepe = kore_cati(y, PX0, PX1, PY0, PY1, zd, 0.32, sacak=0.15, tur='paljak', kivrim=0.42, yukari=0.045, alt_key='boya_yesil',
                 ucluk='lake_koyu', ns=20, sirt_h=0.03, uc='chimi')
# people in the pavilion
kisi(y, -0.25, 0.75, ZF, aci=-math.pi / 2 + 0.2, boy=0.1, govde='beyaz', kusak='boya_kirmizi', sapka='gat', kol='on')
kisi(y, 0.22, 0.7, ZF, aci=-math.pi / 2 - 0.4, boy=0.1, govde='siva_krem', kusak='boya_yesil', sapka='gat')

# ---------------- shooting line ----------------
y.bolum('Atış hattı ve okçular')
SY0, SY1 = 0.3, 0.42
y.yuz_yon([V(-0.66, SY0, ZT + 0.004), V(0.66, SY0, ZT + 0.004), V(0.66, PY0 - 0.1, ZT + 0.004), V(-0.66, PY0 - 0.1, ZT + 0.004)], 'zemin', Z)
kutu(y, V(-0.67, SY0 - 0.012, ZT - 0.03), X, 1.34, 0.024, 0.04, 'granit')
for k in range(6):   # the archers' stations
    x = -0.5 + k * 0.2
    y.yuz_yon([V(x - 0.035, SY0 + 0.02, ZT + 0.006), V(x + 0.035, SY0 + 0.02, ZT + 0.006), V(x + 0.035, SY0 + 0.06, ZT + 0.006),
               V(x - 0.035, SY0 + 0.06, ZT + 0.006)], 'granit_acik', Z)
for k, x in enumerate((-0.5, -0.3, -0.1, 0.3, 0.5)):
    kisi(y, x, SY0 + 0.04, ZT + 0.006, aci=-math.pi / 2, boy=0.1, govde=('beyaz', 'siva_krem', 'beyaz', 'beyaz', 'siva_krem')[k],
         kusak=('boya_kirmizi', 'lake_koyu', 'boya_yesil', 'boya_kirmizi', 'turkuaz')[k], sapka='gat', yay=True)
# quivers on a rack, a drum on its stand
for k in range(4):
    x = 0.58 + k * 0.022
    cubuk(y, V(x, SY0 + 0.07, ZT + 0.004), V(x, SY0 + 0.075, ZT + 0.05), 0.012, 'lake_koyu', 0.012)
    for m in range(3):
        cubuk(y, V(x - 0.003 + m * 0.003, SY0 + 0.075, ZT + 0.048), V(x - 0.003 + m * 0.003, SY0 + 0.076, ZT + 0.068), 0.0015, 'beyaz')
DR = V(-0.6, SY0 + 0.08)
for sx in (-1, 1):
    cubuk(y, DR + V(sx * 0.03, 0, ZT + 0.004), DR + V(sx * 0.03, 0, ZT + 0.08), 0.008, 'lake_koyu')
with parca(y, (DR.x, DR.y, ZT + 0.06), 0):
    boru(y, [V(-0.024, 0, 0), V(-0.012, 0, 0), V(0.012, 0, 0), V(0.024, 0, 0)], 0.026, 'kirmizi', n=12)
    for sx in (-1, 1):
        y.yuz_yon([V(sx * 0.0245, 0.025 * math.cos(TAU * i / 12), 0.025 * math.sin(TAU * i / 12)) for i in range(12)], 'beyaz', V(sx, 0, 0))

y.bolum('Yamaçtaki taş merdiven')
# the stair down the slope to the range, stepping with the ground
ny = 12
for k in range(ny):
    yy0 = SY0 - 0.012 - (k + 1) * 0.05
    yy1 = yy0 + 0.05
    zz = yuk(0.0, yy0 + 0.025)
    zn = yuk(0.0, yy1) if k else ZT
    kutu(y, V(-0.1, yy0, zz - 0.04), X, 0.2, 0.05 + 0.002, max(zn, zz) - zz + 0.04 + 0.004, 'granit_acik', 'onsagsolust')
    for sx in (-1, 1):
        kutu(y, V(sx * 0.1 + (0 if sx > 0 else -0.018), yy0, zz - 0.04), X, 0.018, 0.052, max(zn, zz) - zz + 0.058, 'granit', 'onsagsolust')

# ---------------- range ----------------
y.bolum('Hedefler')
TY = -0.95


def hedef(x):
    zg = yuk(x, TY)
    with parca(y, (x, TY, zg), 0):
        for sx in (-1, 1):
            kutu_merkez(y, (sx * 0.085, 0.012), 0.014, 0.014, 0.2, 'ahsap', z0=-0.01)
        kutu(y, V(-0.082, -0.0, 0.03), X, 0.164, 0.012, 0.2, 'siva')
        # the painted face towards the archers (+y), and the same on the back (seen from the game's view)
        for sy, y0b in ((1, 0.012), (-1, 0.0)):
            P = lambda u, v, d=0.0: V(u, y0b + sy * (0.0008 + d), 0.03 + v)
            def kare(u0, u1, v0, v1, key, d):
                y.yuz_yon([P(u0, v0, d), P(u1, v0, d), P(u1, v1, d), P(u0, v1, d)], key, V(0, sy, 0))
            kare(-0.082, 0.082, 0.0, 0.2, 'koyu', 0.0)
            kare(-0.07, 0.07, 0.012, 0.188, 'siva', 0.0007)
            kare(-0.04, 0.04, 0.06, 0.14, 'koyu', 0.0014)
            kare(-0.028, 0.028, 0.072, 0.128, 'boya_kirmizi', 0.0021)
            kare(-0.07, 0.07, 0.16, 0.188, 'boya_kirmizi', 0.0014)
        P = lambda u, v, d=0.0: V(u, 0.012 + 0.0008 + d, 0.03 + v)
        # a little tiled hood over the board
        cati_besik(y, -0.095, 0.095, -0.012, 0.028, 0.235, 0.025, 0.012, KIR, KIR2, 0.005, 0.3, 'ahsap', 'ahsap', uc_sacak=0.006,
                   mahya_en=0.006, nr=2, ns=4)
        # two arrows stuck in it
        for (u, v) in ((0.02, 0.09), (-0.05, 0.15)):
            cubuk(y, P(u, v), P(u, v, 0.035) + V(0, 0, 0.006), 0.0018, 'ahsap_acik')
            cubuk(y, P(u, v, 0.03) + V(0, 0, 0.005), P(u, v, 0.038) + V(0, 0, 0.0065), 0.004, 'beyaz', 0.001)


for x in (-0.36, 0.0, 0.36):
    hedef(x)
# flags beside the targets: the markers wave them for a hit
for (x, key) in ((-0.56, 'boya_kirmizi'), (0.56, 'boya_sari'), (-0.18, 'boya_sari'), (0.18, 'boya_kirmizi')):
    zg = yuk(x, TY + 0.02)
    y.prizma((x, TY + 0.02), 0.004, zg - 0.01, zg + 0.2, 'ahsap_koyu', n=5)
    kutu(y, V(x + 0.004, TY + 0.018, zg + 0.145), X, 0.066, 0.004, 0.05, key)
# the markers' shelter: a low stone wall with a tiled coping, a marker crouching behind it
y.bolum('Gözcü siperi ve uçan oklar')
toprak_duvar(y, [V(-0.86, TY + 0.06), V(-0.66, TY + 0.06)], yuk(-0.76, TY + 0.06) - 0.004, 0.1, govde='siva_krem')
kisi(y, -0.76, TY + 0.02, yuk(-0.76, TY + 0.02), aci=math.pi / 2, boy=0.1, govde='siva_krem', kusak='boya_kirmizi', sapka='saz', kol='on')
# the path down the range, arrow-carriers walking to the targets, spent arrows in the turf
for (x0, y0_, x1, y1_) in ((0.0, -0.3, 0.0, -0.62), (0.0, -0.62, -0.36, -0.86), (0.0, -0.62, 0.36, -0.86), (0.0, -0.62, 0.0, -0.86)):
    a_, b_ = V(x0, y0_), V(x1, y1_)
    e_ = (b_ - a_).normalized(); n_ = V(-e_.y, e_.x) * 0.03
    m_ = 6
    for k in range(m_):
        p0, p1 = a_.lerp(b_, k / m_), a_.lerp(b_, (k + 1) / m_)
        q = [p0 - n_, p1 - n_, p1 + n_, p0 + n_]
        y.yuz_yon([V(p.x, p.y, yuk(p.x, p.y) + 0.003) for p in q], 'toprak', Z)
for (x, yy, a) in ((0.06, -0.5, -math.pi / 2), (-0.2, -0.76, -2.3)):
    kisi(y, x, yy, yuk(x, yy), aci=a, boy=0.1, govde='siva_krem', kusak='boya_sari', sapka='saz')
for k in range(9):
    x, yy = rn.uniform(-0.5, 0.5), rn.uniform(-0.9, -0.55)
    p = V(x, yy, yuk(x, yy))
    d = V(rn.uniform(-0.2, 0.2), -1, -0.8).normalized()
    cubuk(y, p - d * 0.03, p + d * 0.004, 0.002, 'ahsap_acik')
    cubuk(y, p - d * 0.03, p - d * 0.02, 0.005, 'beyaz', 0.001)
# arrows in flight over the range
for (x0, y0_, z_) in ((-0.31, -0.2, 0.34), (0.04, -0.52, 0.3), (0.33, 0.0, 0.36)):
    p = V(x0, y0_, z_)
    d = V(0.0, -1, -0.12).normalized()
    cubuk(y, p, p + d * 0.06, 0.0022, 'ahsap_acik')
    cubuk(y, p - d * 0.002, p + d * 0.012, 0.006, 'beyaz', 0.0012)

y.bolum('Çamlar')
for k, (tx, ty, boy) in enumerate(((-0.92, 0.65, 0.42), (-0.8, 0.98, 0.46), (-1.02, 0.25, 0.36), (-0.7, 0.42, 0.3), (0.86, 0.95, 0.44),
                                   (0.98, 0.55, 0.4), (0.74, 0.3, 0.32), (1.0, -0.15, 0.34), (-0.98, -0.3, 0.3), (0.62, 1.02, 0.36),
                                   (-0.55, 1.02, 0.32), (1.02, -0.62, 0.28), (-1.02, -0.78, 0.3))):
    sonamu(y, tx, ty, yuk(tx, ty), boy=boy, tohum=k, yon=math.atan2(-ty, -tx) + rn.uniform(-0.5, 0.5))
# rocks on the slope
for k in range(16):
    bx, by = rn.uniform(-1.1, 1.1), rn.uniform(-0.4, 1.1)
    if abs(bx) < 0.66 and by > -0.45: continue
    r = rn.uniform(0.016, 0.03)
    kure(y, (bx, by, yuk(bx, by) + r * 0.2), r, rn.choice(['kaya', 'kaya_koyu', 'granit']), n=7, kat=4)

y.bolum('Açelyalar ve mesafe taşları')
# azalea (jindallae) bushes flowering pink on the slope round the pavilion, as on Inwangsan below Hwanghakjeong
ra = random.Random(23)
azalea = []
for k in range(60):
    bx, by = ra.uniform(-1.08, 1.08), ra.uniform(-0.38, 1.05)
    if abs(bx) < 0.7 and by > -0.42: continue            # (not on the range, the stair or the hilltop)
    if any((bx - p) ** 2 + (by - q) ** 2 < 0.012 for p, q in azalea): continue
    azalea.append((bx, by))
for k, (cx_, cy_) in enumerate(azalea):
    for g in range(3):   # a clump of three bushes, the blooms all over the top
        a0 = TAU * g / 3 + k
        bx, by = cx_ + math.cos(a0) * 0.035, cy_ + math.sin(a0) * 0.035
        zg = yuk(bx, by)
        r = ra.uniform(0.026, 0.04)
        kure(y, (bx, by, zg + r * 0.35), r, 'yesil_koyu', n=8, kat=4)
        for m in range(7):
            a = TAU * m / 7 + k + g
            rr = r * (0.75 if m < 6 else 0.0)
            kure(y, (bx + math.cos(a) * rr, by + math.sin(a) * rr, zg + r * (0.75 if m < 6 else 1.2)), r * 0.42,
                 'boya_mor_acik' if (k + m + g) % 5 else 'beyaz', n=6, kat=3)
# granite distance stones down each side of the range
for sx in (-1, 1):
    for k in range(4):
        yy = -0.42 - k * 0.15
        x = sx * 0.66
        zg = yuk(x, yy)
        kutu_merkez(y, (x, yy), 0.024, 0.024, 0.05, 'granit_acik', z0=zg - 0.01)
        kutu_merkez(y, (x, yy), 0.03, 0.03, 0.008, 'granit', z0=zg - 0.004)
        donel(y, (x, yy), [(0.0136, zg + 0.04), (0.0136, zg + 0.044), (0.008, zg + 0.052), (0.0, zg + 0.054)], 'granit_acik', n=8)
# a stone stele on a turtle base on the hilltop beside the pavilion
y.bolum('Taş kitabe')
TX_, TY_ = 0.67, 0.66
with parca(y, (TX_, TY_, yuk(TX_, TY_)), -0.25, 0.7):
    donel(y, (0, 0), [(0.0, -0.005), (0.05, -0.005), (0.052, 0.012), (0.042, 0.03), (0.0, 0.036)], 'granit_koyu', n=10)   # the turtle shell
    kure(y, (0.0, -0.05, 0.018), 0.016, 'granit_koyu', n=8, kat=4)                                                        # its head
    kutu_merkez(y, (0, 0), 0.07, 0.022, 0.14, 'granit_acik', z0=0.03)
    kutu_merkez(y, (0, 0), 0.082, 0.03, 0.026, 'granit', z0=0.168)                                                        # the capstone
    for k in range(5):
        kutu(y, V(-0.024 + k * 0.011, -0.0135, 0.07), X, 0.004, 0.003, 0.075, 'koyu', 'onsagsolust')

y.bolum('Sancak')
sancak(y, 0.66, SY0 + 0.02, ZT, boy=0.42, en=0.13, yuk=0.085, aci=-0.4)

calistir(y, 'lm_okculukpavyon')
