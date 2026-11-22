# Top Sahası (lm_topsahasi): an Aztec ball court (tlachtli): the I-shaped court with benches, sloping plastered walls and
# upright walls carrying the carved stone rings, spectator terraces stepping down outside, a small talud pyramid with a
# thatched shrine at each end (their stairs come down into the end zones), players and the rubber ball, spectators,
# a tzompantli, braziers, the players' house and trees round the precinct.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mexika_ortak import *

y = Yapi()
R = random.Random(21)
Z0 = 0.04


def profil(x0, x1, prof, keys, cap_key):
    """a profile [(y, z), ...] (counter-clockwise with y to the right, z up) extruded from x0 to x1; keys[i] for the
    edge from point i to i+1 (None: no face, it lies on the ground); end caps cap_key"""
    n = len(prof)
    for i in range(n):
        if keys[i] is None: continue
        (ya, za), (yb, zb) = prof[i], prof[(i + 1) % n]
        y.yuz_yon([V(x0, ya, za), V(x1, ya, za), V(x1, yb, zb), V(x0, yb, zb)], keys[i], V(0, zb - za, -(yb - ya)))
    y.yuz_yon([V(x1, a, b) for a, b in prof], cap_key, X)
    y.yuz_yon([V(x0, a, b) for a, b in prof], cap_key, -X)


def ayna(prof, keys):
    n = len(prof)
    return [(-a, b) for a, b in prof][::-1], [keys[(n - 2 - k) % n] for k in range(n)]


# ---------------------------------------------------------------- ground
y.bolum('Zemin')
GX, GY0, GY1 = 1.215, -1.0, 1.0
zemin(y, -GX, GX, GY0, GY1, Z0, 'kaya_koyu', 'cimen_kuru', basamak=(), silmeli=True)
# the plastered precinct floor round the court
kutu(y, V(-0.8, -0.95, Z0), X, 1.6, 1.85, 0.003, 'kirec', 'onarkasagsolust')
PZ = Z0 + 0.003

# ---------------------------------------------------------------- the court
y.bolum('Saha')
AX, AY = 0.45, 0.155           # the alley's half length and half width
EX, EY = 0.75, 0.32           # the end zones reach the pyramids' feet
# floor: plaster, a red centre line, the three markers
y.yuz_yon([V(-EX, -EY, PZ + 0.001), V(EX, -EY, PZ + 0.001), V(EX, EY, PZ + 0.001), V(-EX, EY, PZ + 0.001)], 'zemin', Z)
y.yuz_yon([V(-EX, -0.006, PZ + 0.002), V(EX, -0.006, PZ + 0.002), V(EX, 0.006, PZ + 0.002), V(-EX, 0.006, PZ + 0.002)], 'boya_kirmizi', Z)
for sx in (-1, 1):
    y.yuz_yon([V(sx * AX - 0.004, -EY, PZ + 0.002), V(sx * AX + 0.004, -EY, PZ + 0.002), V(sx * AX + 0.004, EY, PZ + 0.002),
               V(sx * AX - 0.004, EY, PZ + 0.002)], 'boya_kirmizi', Z)
for xx in (-0.3, 0.0, 0.3):
    halka_disk(y, V(xx, 0, PZ + 0.002), Z, 0.0, 0.03, 0, 0.003, 'kirec', m=16, yan_key='kirec')
    halka_disk(y, V(xx, 0, PZ + 0.002), Z, 0.0, 0.02, 0, 0.0045, 'turkuaz' if xx else 'boya_kirmizi', m=12)
    halka_disk(y, V(xx, 0, PZ + 0.002), Z, 0.0, 0.008, 0, 0.0055, 'koyu', m=8)

# the long side structures: bench, sloping wall, upright wall with the ring, top walk, terraces outside
ZB, ZT_, ZW = PZ + 0.03, PZ + 0.1, PZ + 0.22
YT, YW, YO = 0.235, 0.33, 0.62
basamak = 5
prof = [(AY, PZ), (YO, PZ)]
keys = [None, 'tas']
for k in range(basamak):
    za = PZ + (ZW - PZ) * (k + 1) / basamak
    ya = YO - (YO - YW - 0.06) * k / basamak
    yb = YO - (YO - YW - 0.06) * (k + 1) / basamak
    prof += [(ya, za), (yb, za)]
    keys += ['tas', 'tas' if k < basamak - 1 else 'zemin']
prof[-1] = (YW, ZW)
keys[-1] = 'kirec'
prof += [(YT, ZW), (YT, ZT_), (AY + 0.03, ZB), (AY, ZB)]
keys += ['siva', 'siva', 'siva', 'kirec']
# (the last key closes from (AY, ZB) down to the start)
keys = keys[:len(prof)]
keys[-1] = 'kirec'
for sy in (1, -1):
    pr, ks = (prof, keys) if sy > 0 else ayna(prof, keys)
    profil(-AX, AX, pr, ks, 'siva')
    # a painted band along the lip of each spectator step (alternating red / turquoise), a red frame round the end caps
    for k in range(basamak):
        za = PZ + (ZW - PZ) * (k + 1) / basamak
        ya = YO - (YO - YW - 0.06) * k / basamak + 0.0015
        y.yuz_yon([V(-AX, sy * ya, za - 0.009), V(AX, sy * ya, za - 0.009), V(AX, sy * ya, za - 0.002), V(-AX, sy * ya, za - 0.002)],
                  'boya_kirmizi' if k % 2 == 0 else 'turkuaz', V(0, sy, 0))
    for sx in (-1, 1):
        x_ = sx * (AX + 0.0015)
        for (ya_, yb_, za_, zb_) in ((YT, YW, ZW - 0.012, ZW), (AY + 0.02, YT, ZB - 0.006, ZB)):
            y.yuz_yon([V(x_, sy * ya_, za_), V(x_, sy * yb_, za_), V(x_, sy * yb_, zb_), V(x_, sy * ya_, zb_)], 'boya_kirmizi', V(sx, 0, 0))
        y.oculus(V(x_, sy * (YT + YW) / 2, (ZT_ + ZW) / 2 + 0.01), V(0, -sy * sx, 0), V(sx, 0, 0), 0.016, 'turkuaz', 'beyaz', f=0.005, k=12)
    # painted bands: red along the foot of the upright wall and its top, discs between
    for zz, hh in ((ZT_, 0.012), (ZW - 0.014, 0.014)):
        y.yuz_yon([V(-AX, sy * (YT - 0.0015), zz), V(AX, sy * (YT - 0.0015), zz), V(AX, sy * (YT - 0.0015), zz + hh), V(-AX, sy * (YT - 0.0015), zz + hh)],
                  'boya_kirmizi', V(0, -sy, 0))
    for k in range(10):
        xx = -AX + (k + 0.5) * 2 * AX / 10
        if abs(xx) < 0.08: continue
        y.oculus(V(xx, sy * (YT - 0.002), ZT_ + 0.044), V(sy, 0, 0), V(0, -sy, 0), 0.011, 'turkuaz', 'beyaz', f=0.004, k=10)
    # a feathered-serpent band painted along the sloping wall
    pts = [V(-AX + 0.02 + t * (2 * AX - 0.04), sy * (AY + 0.03 + (YT - AY - 0.03) * (0.5 + 0.18 * math.sin(t * TAU * 3))),
             ZB + (ZT_ - ZB) * (0.5 + 0.18 * math.sin(t * TAU * 3))) for t in [i / 40 for i in range(41)]]
    n_ = V(0, -sy * (ZT_ - ZB), (YT - AY - 0.03)).normalized()
    boru(y, [p + n_ * 0.002 for p in pts], 0.006, 'boya_yesil', n=5)
    yilan_basi(y, (sy * 0 - AX + 0.0, sy * (AY + 0.025), ZB), math.pi, 0.05, 'kirec', tuy='boya_yesil') if sy > 0 else \
        yilan_basi(y, (AX, sy * (AY + 0.025), ZB), 0.0, 0.05, 'kirec', tuy='boya_yesil')
    # the stone ring set in the upright wall, its hole across the court
    rc = V(0, sy * YT, ZT_ + 0.06)
    kutu_merkez(y, (0, sy * (YT - 0.006)), 0.03, 0.012, 0.03, 'kirec', z0=rc.z - 0.015)            # the tenon
    halka_disk(y, rc + V(0, -sy * 0.012, 0), V(0, -sy, 0), 0.02, 0.055, 0.0, 0.016, 'kirec', m=28, arka=True, ic_key='boya_kirmizi')
    halka_disk(y, rc + V(0, -sy * 0.012, 0), V(0, -sy, 0), 0.027, 0.048, 0.016, 0.019, 'turkuaz', m=28)
    for k in range(8):
        t = TAU * k / 8
        p = rc + V(0, -sy * 0.012, 0) + V(math.cos(t) * 0.0375 * sy, 0, math.sin(t) * 0.0375)
        halka_disk(y, p, V(0, -sy, 0), 0.0, 0.006, 0.019, 0.022, 'boya_kirmizi', m=8)
    # spectators on the terraces and the top walk
    for k in range(18):
        st = R.randrange(basamak)
        za = PZ + (ZW - PZ) * (st + 1) / basamak
        yy = YO - (YO - YW - 0.06) * (st + 0.5) / basamak
        if st == basamak - 1: yy = (YW + YO - (YO - YW - 0.06) * (basamak - 1) / basamak) / 2
        xx = R.uniform(-AX + 0.04, AX - 0.04)
        kisi(y, xx, sy * yy, za, -sy * math.pi / 2 + R.uniform(-0.3, 0.3), 0.044, 'kiremit',
             R.choice(['beyaz', 'siva_oker', 'boya_kirmizi', 'turkuaz']), kol=R.choice(['yan', 'kalk', 'yan', 'one']),
             pelerin=R.choice([None, 'boya_kirmizi', 'turkuaz', 'siva_oker']), bas=R.choice([None, None, 'boya_yesil', 'boya_sari']))
    # the lords' seat in the middle of the top walk: an awning on posts
    for (px, py) in ((-0.07, YT + 0.015), (0.07, YT + 0.015), (-0.07, YW - 0.012), (0.07, YW - 0.012)):
        y.silindir((px, sy * py), 0.004, ZW, ZW + 0.075, 'ahsap', n=5)
    iki_yuzlu(y, [V(-0.085, sy * (YT + 0.0), ZW + 0.075), V(0.085, sy * (YT + 0.0), ZW + 0.075), V(0.085, sy * (YW + 0.0), ZW + 0.082),
                  V(-0.085, sy * (YW + 0.0), ZW + 0.082)], 'boya_kirmizi' if sy > 0 else 'turkuaz', Z)
    kisi(y, 0.0, sy * ((YT + YW) / 2), ZW, -sy * math.pi / 2, 0.048, 'kiremit', 'beyaz', kol='kalk', pelerin='turkuaz', bas='boya_yesil')

# the end zones' side walls (low talud walls), the I's caps
for sx in (-1, 1):
    x0, x1 = (AX, EX) if sx > 0 else (-EX, -AX)
    wp = [(EY, PZ), (EY + 0.07, PZ), (EY + 0.07, PZ + 0.15), (EY + 0.025, PZ + 0.15), (EY, PZ + 0.03)]
    wk = [None, 'siva', 'kirec', 'siva', 'siva']
    for sy in (1, -1):
        pr, ks = (wp, wk) if sy > 0 else ayna(wp, wk)
        profil(x0, x1, pr, ks, 'siva')
        y.yuz_yon([V(x0, sy * (EY + 0.0262), PZ + 0.13), V(x1, sy * (EY + 0.0262), PZ + 0.13), V(x1, sy * (EY + 0.0262), PZ + 0.142),
                   V(x0, sy * (EY + 0.0262), PZ + 0.142)], 'boya_kirmizi', V(0, -sy, 0))
        almenalar(y, V(x0, sy * (EY + 0.047)), V(x1, sy * (EY + 0.047)), PZ + 0.15, 0.03, 0.012, 'siva', en=0.026, bosluk=0.01) if sy < 0 else \
            almenalar(y, V(x1, sy * (EY + 0.047)), V(x0, sy * (EY + 0.047)), PZ + 0.15, 0.03, 0.012, 'siva', en=0.026, bosluk=0.01)

# players and the ball
y.bolum('Oyuncular')
for (px, py, a_, tak, kol) in ((-0.18, 0.04, 0.2, 'boya_kirmizi', 'one'), (-0.32, -0.06, 0.0, 'boya_kirmizi', 'yan'),
                               (0.12, -0.03, math.pi + 0.3, 'beyaz', 'kalk'), (0.3, 0.05, math.pi, 'beyaz', 'one'),
                               (-0.6, 0.18, 0.0, 'boya_kirmizi', 'yan'), (0.62, -0.2, math.pi, 'beyaz', 'yan')):
    kisi(y, px, py, PZ + 0.002, a_, 0.05, 'kiremit', tak, kol=kol, bas='boya_yesil' if tak == 'beyaz' else 'boya_sari', egim=0.3)
    # the hip yoke
    kutu_merkez(y, (px, py), 0.016, 0.017, 0.006, 'ahsap_koyu', z0=PZ + 0.002 + 0.021, aci=a_)
kure(y, (-0.03, 0.01, PZ + 0.06), 0.011, 'koyu', n=10, kat=5)

# ---------------------------------------------------------------- the end pyramids with their shrines
y.bolum('Uc piramitler')
for sx in (-1, 1):
    with parca(y, (sx * 0.98, 0, 0), -sx * math.pi / 2):
        hw, hd = 0.3, 0.235
        z = PZ
        TH = 0.115
        for k in range(4):
            bw_, bd_, z1 = kademe(y, (0, 0), hw, hd, z, TH, 0.034, talud=0.72, key='kirec', bant_key='siva', ust_key='zemin' if k < 3 else 'kirec',
                                  cizgi='boya_kirmizi' if sx > 0 else 'turkuaz')
            bant_diskleri(y, (0, 0), bw_, bd_, z + TH * 0.86, 0.008, 0.06, lambda p: 'boya_kirmizi' if sx > 0 else 'turkuaz', 'beyaz',
                          atla=lambda p: abs(p.x) < 0.1 and p.y < 0)
            hw, hd = bw_ - 0.012, bd_ - 0.012
            z = z1
        ZP_ = z
        ayak = alfarda_merdiven(y, 0.0, -0.235 - 0.2, -bd_, PZ, ZP_, 0.15, key='kirec', alf_key='siva', alf_en=0.03, dado=0.13, dado_h=0.03)
        for p in ayak:
            yilan_basi(y, (p.x, p.y - 0.035, PZ), -math.pi / 2, 0.055, 'kirec', tuy='boya_yesil' if sx < 0 else None)
        # the shrine: white walls, dark doorway, painted frieze, a steep thatched hipped roof
        w, d = 0.24, 0.18
        cy_ = 0.01
        kose = dikdortgen(-w / 2, w / 2, cy_ - d / 2, cy_ + d / 2)
        vurgu = 'boya_kirmizi' if sx > 0 else 'turkuaz'
        kutu_merkez(y, (0, cy_), w + 0.03, d + 0.03, 0.015, 'kirec', z0=ZP_)
        zw = ZP_ + 0.015; H = 0.12
        dikdortgen_kapi(y, kose[0], kose[1], zw, H, 0.34, 0.66, 0.085, 'siva', 'koyu', cerceve=(0.01, vurgu), derin=0.025)
        for i in (1, 2, 3):
            duz_duvar(y, kose[i], kose[(i + 1) % 4], zw, zw + H, 'siva')
        silme(y, kose, zw, 0.018, 0.003, vurgu)
        silme(y, kose, zw + H - 0.026, 0.026, 0.003, vurgu)
        for i in range(4):
            a, b = kose[i], kose[(i + 1) % 4]
            e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
            m = int(L / 0.035)
            for j in range(m):
                pp = a.lerp(b, (j + 0.5) / m)
                y.oculus(pp + nn * 0.0035 + Z * (zw + H - 0.013), e, nn, 0.0065, 'beyaz', 'koyu', f=0.002, k=8)
        cati_kirma(y, -w / 2, w / 2, cy_ - d / 2, cy_ + d / 2, zw + H, 0.32, 0.035, 'saz', 'saz_koyu', kalinlik=0.018, nr=6, ns=8,
                   dilim=['saz', 'saz_koyu'], mahya_en=0.016)
        kure(y, (0, cy_, zw + H + 0.322), 0.014, 'altin', n=8, kat=4)
        for sx2 in (-1, 1):
            mangal(y, sx2 * 0.13, -bd_ + 0.03, ZP_, 0.042, 'siva_oker', vurgu)
        sancak(y, 0.13, cy_ + d / 2 + 0.01, ZP_, boy=0.26, en=0.11, yuk=0.07, aci=math.pi * 0.25)
        kisi(y, -0.05, -bd_ + 0.03, ZP_, -math.pi / 2, 0.046, 'koyu', 'koyu', kol='kalk', pelerin=vurgu)

# ---------------------------------------------------------------- the front: tzompantli, braziers, a marker stone
y.bolum('On meydan')
tzompantli(y, -0.5, -0.82, PZ, 0.5, 0.0, satir=4, adim=0.021, h=0.12)
for xx in (-0.82, -0.18):
    mangal(y, xx, -0.82, PZ, 0.05, 'siva_oker', 'boya_kirmizi')
# a small altar platform with a stair and a cuauhxicalli
kademe(y, (0.5, -0.82), 0.13, 0.1, PZ, 0.05, 0.012, talud=0.5, key='siva', ust_key='kirec', cizgi='boya_kirmizi')
alfarda_merdiven(y, 0.5, -0.92 - 0.06, -0.92 + 0.0125, PZ, PZ + 0.05, 0.08, key='kirec', alf_key='siva', alf_en=0.016, dado=0.15, dado_h=0.008)
donel(y, (0.5, -0.81), [(0, PZ + 0.05), (0.045, PZ + 0.05), (0.05, PZ + 0.065), (0.038, PZ + 0.08), (0.0, PZ + 0.072)], 'bazalt', n=16)
halka_disk(y, V(0.5, -0.81, PZ + 0.08), Z, 0.018, 0.034, 0, 0.001, 'boya_kirmizi', m=16)
for xx in (0.32, 0.68):
    mangal(y, xx, -0.84, PZ, 0.045, 'siva_oker', 'turkuaz')
for (px, py, a_) in ((0.42, -0.72, 0.4), (0.6, -0.7, 2.6), (-0.95, -0.7, 1.2), (0.05, -0.75, 1.5), (0.12, -0.72, 1.7)):
    kisi(y, px, py, PZ, a_, 0.046, 'kiremit', R.choice(['beyaz', 'siva_oker']), kol=R.choice(['yan', 'one']), pelerin=R.choice([None, 'turkuaz']))

# ---------------------------------------------------------------- the back: the players' house and trees
y.bolum('Arka')
hx0, hx1, hy0, hy1 = 0.25, 0.65, 0.72, 0.9
kutu(y, V(hx0 - 0.02, hy0 - 0.02, PZ), X, hx1 - hx0 + 0.04, hy1 - hy0 + 0.04, 0.02, 'kirec', 'onarkasagsolust')
kose = dikdortgen(hx0, hx1, hy0, hy1)
dikdortgen_kapi(y, kose[0], kose[1], PZ + 0.02, 0.08, 0.42, 0.58, 0.06, 'siva', 'koyu', cerceve=(0.007, 'boya_kirmizi'))
for i in (1, 2, 3):
    duz_duvar(y, kose[i], kose[(i + 1) % 4], PZ + 0.02, PZ + 0.1, 'siva')
silme(y, kose, PZ + 0.02, 0.014, 0.003, 'boya_kirmizi')
cati_kirma(y, hx0, hx1, hy0, hy1, PZ + 0.1, 0.13, 0.03, 'saz', 'saz_koyu', kalinlik=0.016, nr=5, ns=8, dilim=['saz', 'saz_koyu'], mahya_en=0.014)
for (tx, ty, b) in ((-0.95, 0.78, 0.16), (-0.75, 0.86, 0.13), (-0.2, 0.84, 0.15), (0.9, 0.82, 0.14), (1.08, -0.84, 0.12), (-1.08, -0.85, 0.12),
                    (-0.98, 0.55, 0.12), (1.0, 0.55, 0.13)):
    agac(y, tx, ty, PZ, b, 'yapraklı', 'boya_yesil' if tx < 0 else 'zeytin')
for xx in (-0.55, 0.0):
    mangal(y, xx, 0.82, PZ, 0.045, 'siva_oker', 'boya_kirmizi')

calistir(y, 'lm_topsahasi')
