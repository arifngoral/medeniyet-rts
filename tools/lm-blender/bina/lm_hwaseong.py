# Hwaseong Kalesi (lm_hwaseong): the Joseon fortress at Suwon, drawn to a square: granite walls with an earthen bank inside
# and the grey brick crenellated parapet (yeojang) with gun holes, bastions (chi); the Janganmun gate (an arched stone gate
# under a two-storey timber pavilion) behind its half-moon brick barbican (ongseong) and two flanking platforms; the
# Hwahongmun water gate (seven arches over the stream, a pavilion on top); the Bongdon beacon platform with five chimneys;
# the Seobuk Gongsimdon watchtower; Banghwasuryujeong on the corner bastion above the Yongyeon pond; the haenggung halls inside.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ortak import *
from cin_ek import egim_icin
from bina_ortak import calistir

y = Yapi()
rn = random.Random(9)
Z0 = 0.03
ZW = Z0 - 0.025                       # the stream's water
FY, BY, LX, RX = -0.5, 0.92, -0.95, 0.95
WH = 0.15                             # wall top above Z0
W, BANK = 0.07, 0.1                   # walkway width, the earth bank inside
SX0, SX1 = 0.51, 0.81                 # the stream
TG, TGK = 'tugla_gri', 'tugla_gri_koyu'
GX0, GX1, GY0, GY1 = -1.08, 1.14, -1.03, 1.08

# ---------------- ground and stream ----------------
y.bolum('Zemin ve dere')
kutu(y, V(GX0, GY0, 0), X, SX0 - GX0, GY1 - GY0, Z0, 'kaya_koyu', 'onarkasol')
kutu(y, V(SX1, GY0, 0), X, GX1 - SX1, GY1 - GY0, Z0, 'kaya_koyu', 'onarkasag')
kutu(y, V(SX0, GY0, 0), X, SX1 - SX0, GY1 - GY0, ZW - 0.005, 'kaya_koyu', 'onarka')
for (a0, a1) in ((GX0, SX0), (SX1, GX1)):
    y.yuz_yon([V(a0, GY0, Z0), V(a1, GY0, Z0), V(a1, GY1, Z0), V(a0, GY1, Z0)], 'cimen', Z)
y.yuz_yon([V(SX0, GY0, ZW), V(SX1, GY0, ZW), V(SX1, GY1, ZW), V(SX0, GY1, ZW)], 'su', Z)
duz_duvar(y, V(SX0, GY0), V(SX0, GY1), 0.0, Z0, 'granit')
duz_duvar(y, V(SX1, GY1), V(SX1, GY0), 0.0, Z0, 'granit')
for (x, s) in ((SX0, -1), (SX1, 1)):   # a dressed kerb along the banks
    kutu_merkez(y, (x + s * 0.007, (GY0 + GY1) / 2), 0.014, GY1 - GY0, 0.006, 'granit_acik', z0=Z0, yuzler='onarkasagsolust')
# roads
for (x0, x1, y0, y1) in ((-0.07, 0.07, GY0, FY - 0.32), (-0.07, 0.07, FY + 0.12, 0.42)):
    y.yuz_yon([V(x0, y0, Z0 + 0.002), V(x1, y0, Z0 + 0.002), V(x1, y1, Z0 + 0.002), V(x0, y1, Z0 + 0.002)], 'toprak', Z)
y.yuz_yon([V(-0.3, 0.42, Z0 + 0.002), V(0.07, 0.42, Z0 + 0.002), V(0.07, 0.5, Z0 + 0.002), V(-0.3, 0.5, Z0 + 0.002)], 'toprak', Z)
# the space inside the barbican
y.yuz_yon([V(-0.24, FY - 0.28, Z0 + 0.002), V(0.24, FY - 0.28, Z0 + 0.002), V(0.24, FY - 0.07, Z0 + 0.002), V(-0.24, FY - 0.07, Z0 + 0.002)], 'toprak', Z)


# ---------------- walls ----------------
def yeojang(a, b, z, ph=0.045, t=0.022, sw=0.062, gap=0.011, key=TG, delik=True):
    """the brick parapet along a->b (outer face on the line, facing the right): crenels with gaps, capped, gun holes"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 0.02: return
    e = (b - a) / L; nn = V(e.y, -e.x)
    k = max(1, int(round((L + gap) / (sw + gap))))
    w = (L + gap) / k - gap
    for i in range(k):
        o = a + e * (i * (w + gap)) + Z * z
        kutu(y, o, e, w, t, ph, key, 'onarkasagsol')
        kutu(y, o + nn * 0.003 - e * 0.002 + Z * ph, e, w + 0.004, t + 0.006, 0.007, TGK)
        if delik:
            yarik(y, o, e, nn, w * 0.5 - 0.005, ph * 0.5, 0.01, 0.013, 'koyu')
            yarik(y, o, e, nn, w * 0.2 - 0.004, ph * 0.08, 0.008, 0.008, 'koyu')


def seong(yol, nopar=(), parapet=True):
    """a fortress wall along an open polyline (outer face to the right): the granite face with a plinth, a paved walkway,
    the earth bank sloping down inside, the brick parapet on the outer edge (not on the segments in nopar: a bastion or
    a tower stands there)"""
    O = [V(p[0], p[1]) for p in yol]
    n = len(O)
    I = disa(O, -W, False)
    B = disa(O, -(W + BANK), False)
    zt = Z0 + WH
    for i in range(n - 1):
        j = i + 1
        e = (O[j] - O[i]).normalized(); nn = V(e.y, -e.x)
        duz_duvar(y, O[i], O[j], Z0 - 0.01, zt, 'granit')
        kutu(y, O[i] + nn * 0.006 + Z * (Z0 - 0.01), e, (O[j] - O[i]).length, 0.006, 0.025, 'granit_koyu', 'onust')
        y.yuz_yon([O[i] + Z * zt, O[j] + Z * zt, I[j] + Z * zt, I[i] + Z * zt], 'zemin', Z)
        y.yuz_yon([I[i] + Z * zt, I[j] + Z * zt, B[j] + Z * (Z0 - 0.002), B[i] + Z * (Z0 - 0.002)], 'cimen_kuru', -nn + Z)
        if parapet and i not in nopar:
            yeojang(O[i], O[j], zt)
    for k, s in ((0, -1), (n - 1, 1)):
        e = (O[1] - O[0]) if k == 0 else (O[-1] - O[-2]); e.z = 0; e.normalize()
        y.yuz_yon([O[k] + Z * (Z0 - 0.01), B[k] + Z * (Z0 - 0.01), B[k] + Z * (Z0 - 0.002), I[k] + Z * zt, O[k] + Z * zt], 'granit', e * s)


def burc(x0, x1, y0, y1, h, kenarlar, key='granit'):
    """a bastion box from the ground to h above Z0, the brick parapet along the sides in kenarlar (0 -y, 1 +x, 2 +y, 3 -x)"""
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, Z0 - 0.01, Z0 + h, key, ust='zemin')
    silme(y, k, Z0 - 0.01, 0.025, 0.006, 'granit_koyu', 'duz')
    for i in kenarlar:
        yeojang(k[i], k[(i + 1) % 4], Z0 + h)
    return Z0 + h


y.bolum('Surlar ve burçlar')
seong([(0.24, FY), (0.32, FY), (0.42, FY), (0.5, FY)], nopar={1})
seong([(0.82, FY), (RX - 0.08, FY), (RX, FY), (RX, FY + 0.08), (RX, 0.15), (RX, 0.45), (RX, BY), (SX1, BY)], nopar={1, 2, 4})
seong([(SX0, BY), (0.1, BY), (-0.1, BY), (LX, BY), (LX, 0.3), (LX, 0.1), (LX, FY), (-0.42, FY), (-0.32, FY), (-0.24, FY)],
      nopar={1, 4, 7})
# chi bastions and the gate's flanking platforms (jeokdae)
burc(-0.1, 0.1, BY, BY + 0.09, WH, (1, 2, 3))
burc(LX - 0.09, LX, 0.1, 0.3, WH, (0, 2, 3))
for x0 in (0.32, -0.42):
    burc(x0, x0 + 0.1, FY - 0.12, FY, WH + 0.01, (0, 1, 3))

# ---------------- Janganmun ----------------
y.bolum('Janganmun: taş kapı')
GH = WH + 0.035
ZG = Z0 + GH
gy0, gy1 = FY - 0.07, FY + 0.12
for (a, b, kapi_) in ((V(-0.24, gy0), V(0.24, gy0), 'ahsap_dikey'), (V(0.24, gy1), V(-0.24, gy1), 'koyu')):
    y.kemerli(a, b, Z0 - 0.01, GH + 0.01, ('granit', 'granit_koyu', 'granit_koyu', kapi_), v0=0.0, en=0.34, ust=GH * 0.3, derin=0.07,
              k_say=10, cerceve=(0.013, ['granit_acik', 'granit']))
duz_duvar(y, V(0.24, gy0), V(0.24, gy1), Z0 - 0.01, ZG, 'granit')
duz_duvar(y, V(-0.24, gy1), V(-0.24, gy0), Z0 - 0.01, ZG, 'granit')
y.yuz_yon([V(-0.24, gy0, ZG), V(0.24, gy0, ZG), V(0.24, gy1, ZG), V(-0.24, gy1, ZG)], 'zemin', Z)
silme(y, dikdortgen(-0.24, 0.24, gy0, gy1), ZG - 0.012, 0.012, 0.006, 'granit_acik', 'duz')
yeojang(V(-0.24, gy0), V(0.24, gy0), ZG)
yeojang(V(0.24, gy0), V(0.24, gy1), ZG, delik=False)
yeojang(V(-0.24, gy1), V(-0.24, gy0), ZG, delik=False)
# iron-studded door leaves
for sx in (-1, 1):
    for k in range(3):
        for m in range(2):
            kure(y, (sx * (0.025 + m * 0.03), gy0 + 0.068, Z0 + 0.02 + k * 0.03), 0.003, 'demir', n=6, kat=3)

y.bolum('Janganmun: iki katlı köşk')
LW, LD = 0.19, 0.085                  # lower storey half sizes
LC = (0.0, (gy0 + gy1) / 2)
z1 = ZG + 0.004
zt1 = hanok_govde(y, -LW, LW, LC[1] - LD, LC[1] + LD, z1, 0.14, bay=0.095, direk='kirmizi', duvar='ahsap_dikey', cerceve='lake_koyu',
                  kagit='koyu', desen=lambda i, j, nb: 'pencere' if i in (0, 2) else 'duvar', yuvarlak=True, ust_bant=None, direk_en=0.018)
zd1 = dancheong(y, dikdortgen(-LW, LW, LC[1] - LD, LC[1] + LD), zt1, 0.018, adim=0.06, cikinti=0.02)
# the pent roof round the upper storey
ASX, ALT = 0.065, 0.045
a_, b_ = LW + ASX, LD + ASX
m_ = min(a_, b_)
IC = 0.02
r_ust = 1 - (LD - IC - 0.012) / m_
cati_kirma(y, -LW, LW, LC[1] - LD, LC[1] + LD, zd1, egim_icin(ALT, r_ust, 0.25), ASX, KIR, KIR2, 0.012, 0.25, 0.03, 'boya_yesil', ns=10, nr=3,
           r_ust=r_ust, mahya_en=0.012)
UW, UD = a_ - m_ * r_ust + 0.004, b_ - m_ * r_ust + 0.004
zt2 = hanok_govde(y, -UW, UW, LC[1] - UD, LC[1] + UD, zd1, ALT + 0.12, bay=0.07, direk='kirmizi', duvar='ahsap_dikey', cerceve='lake_koyu',
                  kagit='koyu', desen=lambda i, j, nb: 'pencere' if i in (0, 2) else 'duvar', yuvarlak=True, ust_bant=None, direk_en=0.015)
zd2 = dancheong(y, dikdortgen(-UW, UW, LC[1] - UD, LC[1] + UD), zt2, 0.016, adim=0.05, cikinti=0.018)
tepe_g = kore_cati(y, -UW, UW, LC[1] - UD, LC[1] + UD, zd2, 0.21, sacak=0.1, tur='ujingak', kivrim=0.42, yukari=0.04, alt_key='boya_yesil',
                   sirt_h=0.026, uc='mangwa', ns=12)
# the name board
kutu(y, V(-0.05, LC[1] - UD - 0.026, zd1 + 0.05), X, 0.1, 0.006, 0.04, 'lake_koyu')
kutu(y, V(-0.04, LC[1] - UD - 0.0275, zd1 + 0.056), X, 0.08, 0.0016, 0.028, 'altin', 'onsagsolust')
sancak(y, -0.37, FY - 0.06, Z0 + WH + 0.01, boy=0.36, en=0.12, yuk=0.075, aci=math.pi + 0.4)
sancak(y, 0.37, FY - 0.06, Z0 + WH + 0.01, boy=0.36, en=0.12, yuk=0.075, aci=-0.4)

# ---------------- ongseong ----------------
y.bolum('Ongseong (yarım ay barbakan)')
OR, OT, OH = 0.3, 0.05, WH - 0.01
g = math.asin(0.08 / OR)


def ongseong(t0, t1, n=8):
    O = [V(OR * math.cos(t0 + (t1 - t0) * k / n), FY + OR * math.sin(t0 + (t1 - t0) * k / n)) for k in range(n + 1)]
    I = disa(O, -OT, False)
    zt = Z0 + OH
    for i in range(n):
        j = i + 1
        e = (O[j] - O[i]).normalized(); nn = V(e.y, -e.x)
        duz_duvar(y, O[i], O[j], Z0 - 0.01, zt, TG)
        kutu(y, O[i] + nn * 0.005 + Z * (Z0 - 0.01), e, (O[j] - O[i]).length, 0.005, 0.03, 'granit', 'onust')
        duz_duvar(y, I[j], I[i], Z0 - 0.01, zt, TG)
        y.yuz_yon([O[i] + Z * zt, O[j] + Z * zt, I[j] + Z * zt, I[i] + Z * zt], 'zemin', Z)
        yeojang(O[i], O[j], zt, ph=0.04, sw=0.055)
    for k, s in ((0, -1), (n, 1)):
        e = (O[1] - O[0]) if k == 0 else (O[-1] - O[-2]); e.z = 0; e.normalize()
        y.yuz_yon([O[k] + Z * (Z0 - 0.01), I[k] + Z * (Z0 - 0.01), I[k] + Z * zt, O[k] + Z * zt], TG, e * s)


ongseong(math.pi, 1.5 * math.pi - g)
ongseong(1.5 * math.pi + g, 2 * math.pi)
# its gate: an arch through a brick block
kemer_dizisi(y, V(-0.085, FY - OR - 0.01), V(0.085, FY - OR - 0.01), 1, Z0 - 0.01, OH + 0.03, OT + 0.03, (TG, 'granit_koyu', 'granit', 'koyu'),
             en=0.5, ust=0.03, acik=True, taban=False)
yeojang(V(-0.085, FY - OR - 0.01), V(0.085, FY - OR - 0.01), Z0 + OH + 0.02, ph=0.04, sw=0.05)

# ---------------- Hwahongmun ----------------
y.bolum('Hwahongmun su kapısı')
HD = 0.12
kemer_dizisi(y, V(0.5, FY), V(0.82, FY), 7, ZW, Z0 + WH - ZW, HD, ('granit', 'granit_koyu', 'granit_acik', 'koyu'), en=0.72, ust=0.045,
             acik=True, taban=False)
# cutwaters between the arches
for k in range(1, 7):
    x = 0.5 + 0.32 * k / 7
    pts = [V(x - 0.008, FY, ZW), V(x + 0.008, FY, ZW), V(x, FY - 0.02, ZW)]
    for i in range(3):
        a, b = pts[i], pts[(i + 1) % 3]
        if i == 0: continue
        y.yuz_yon([a, b, b + Z * 0.05, a + Z * 0.05], 'granit_acik', (a + b) / 2 - V(x, FY - 0.007, ZW))
    y.yuz_yon([p + Z * 0.05 for p in pts], 'granit_acik', Z)
yeojang(V(0.5, FY), V(0.82, FY), Z0 + WH)
yeojang(V(0.82, FY + HD), V(0.5, FY + HD), Z0 + WH, ph=0.03, delik=False)


def pavyon(x0, x1, y0, y1, z, h, cati_h, sacak, uc='mangwa', korkuluk=True, adim=0.07):
    """an open pavilion: a board floor, red round posts, a low railing, dancheong with brackets, a painted ceiling and a
    paljak roof. Returns the top z"""
    kutu(y, V(x0 - 0.008, y0 - 0.008, z), X, x1 - x0 + 0.016, y1 - y0 + 0.016, 0.01, 'ahsap_acik', 'onarkasagsolust')
    zf = z + 0.01
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        m = max(1, int(round((b - a).length / adim)))
        for j in range(m):
            p = a.lerp(b, j / m)
            y.prizma((p.x, p.y), 0.0075, zf, zf + h, 'kirmizi', n=8, ust=False)
        if korkuluk:
            cubuk(y, a + Z * (zf + 0.025), b + Z * (zf + 0.025), 0.006, 'kirmizi', 0.006)
            for j in range(1, m * 3):
                p = a.lerp(b, j / (m * 3))
                cubuk(y, p + Z * zf, p + Z * (zf + 0.025), 0.003, 'ahsap_acik')
    zd = dancheong(y, k, zf + h, h * 0.18, adim=adim, cikinti=0.018)
    y.yuz_yon([V(p.x, p.y, zd) for p in k], 'boya_yesil', -Z)
    return kore_cati(y, x0, x1, y0, y1, zd, cati_h, sacak=sacak, tur='paljak', kivrim=0.42, yukari=0.035, alt_key='boya_yesil', ucluk='lake_koyu',
                     uc=uc, sirt_h=min(0.026, cati_h * 0.14), ns=max(5, int((x1 - x0) / 0.04)))


pavyon(0.56, 0.76, FY + 0.03, FY + 0.095, Z0 + WH, 0.07, 0.1, 0.05)

# ---------------- Bongdon ----------------
y.bolum('Bongdon işaret kulesi')
zb = burc(RX, RX + 0.17, 0.15, 0.45, WH + 0.03, (0, 1, 2), key=TG)
duz_duvar(y, V(RX + 0.17 + 0.004, 0.15), V(RX + 0.17 + 0.004, 0.45), Z0 - 0.01, Z0 + 0.06, 'granit')
for k in range(5):
    cy = 0.19 + k * 0.055
    cx = RX + 0.09
    kutu_merkez(y, (cx, cy), 0.044, 0.044, 0.075, TG, z0=zb)
    kutu_merkez(y, (cx, cy), 0.05, 0.05, 0.008, TGK, z0=zb + 0.075)
    donel(y, (cx, cy), [(0.02, zb + 0.083), (0.016, zb + 0.095), (0.012, zb + 0.1), (0.0, zb + 0.101)], TG, n=8, kat=math.pi / 4)
    # the fire mouth on its outer face
    y.yuz_yon([V(cx + 0.0228, cy - 0.008, zb), V(cx + 0.0228, cy + 0.008, zb), V(cx + 0.0228, cy + 0.008, zb + 0.026), V(cx + 0.0228, cy - 0.008, zb + 0.026)], 'koyu', X)
# the signal: fire and smoke from the first chimney
cy0 = 0.19
for i in range(4):
    a = TAU * i / 4
    y.koni((RX + 0.09 + 0.006 * math.cos(a), cy0 + 0.006 * math.sin(a)), 0.008, zb + 0.1, 0.03, 'boya_kirmizi' if i % 2 else 'boya_sari', n=6)
for k in range(7):
    t = k / 6
    r = 0.018 + 0.028 * t
    kure(y, (RX + 0.09 - 0.05 * t * t, cy0 + 0.02 * t, zb + 0.14 + 0.32 * t), r, 'granit' if k < 2 else ('tas_acik' if k % 2 else 'beyaz'), n=10, kat=5)

# ---------------- Gongsimdon ----------------
y.bolum('Seobuk Gongsimdon')
GC = V(-0.68, FY + 0.01)
burc(GC.x - 0.12, GC.x + 0.12, GC.y - 0.12, GC.y + 0.1, WH, ())
zg0 = Z0 + WH
TW_ = 0.095
k_ = dikdortgen(GC.x - TW_, GC.x + TW_, GC.y - TW_, GC.y + TW_ * 0.8)
duvarlar(y, k_, zg0, zg0 + 0.26, TG, ust='zemin')
silme(y, k_, zg0 + 0.26 - 0.012, 0.012, 0.008, TGK, 'duz')
for i in range(4):
    a, b = k_[i], k_[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    for row in range(4):
        for c in range(3):
            yarik(y, a + Z * zg0, e, nn, L * (c + 0.5) / 3 - 0.005, 0.03 + row * 0.055, 0.011, 0.016, 'koyu')
for i in range(4):
    yeojang(k_[i], k_[(i + 1) % 4], zg0 + 0.26, ph=0.035, sw=0.05)
dikdortgen_acik(y, k_[2], k_[3], zg0, 0.26, 0.4, 0.6, 0.0, 0.07, (TG, TGK, TGK, 'ahsap_dikey'), derin=0.01)
pavyon(GC.x - 0.05, GC.x + 0.05, GC.y - 0.045, GC.y + 0.035, zg0 + 0.26, 0.055, 0.08, 0.04, korkuluk=False, adim=0.05)

# ---------------- Banghwasuryujeong ----------------
y.bolum('Banghwasuryujeong ve Yongyeon')
zk = burc(RX - 0.08, RX + 0.12, FY - 0.12, FY + 0.08, WH + 0.02, (0, 1, 2, 3))
pavyon(RX - 0.05, RX + 0.09, FY - 0.09, FY + 0.04, zk, 0.07, 0.11, 0.05, uc='chimi')
PC = (1.0, -0.86)
donel(y, PC, [(0.13, Z0), (0.13, Z0 + 0.02), (0.118, Z0 + 0.02), (0.118, Z0 + 0.012), (0.0, Z0 + 0.012)], 'granit', n=24)
y.yuz_yon([V(PC[0] + 0.118 * math.cos(TAU * i / 24), PC[1] + 0.118 * math.sin(TAU * i / 24), Z0 + 0.0125) for i in range(24)], 'su', Z)
donel(y, PC, [(0.04, Z0 + 0.012), (0.04, Z0 + 0.024), (0.034, Z0 + 0.03), (0.0, Z0 + 0.03)], 'cimen', n=12)
sonamu(y, PC[0], PC[1], Z0 + 0.03, boy=0.2, tohum=77, yon=2.3)

# ---------------- haenggung ----------------
y.bolum('Haenggung (iç saray)')
HG = (-0.48, 0.6)
tepe_h = None
zb_ = gidan(y, HG[0] - 0.24, HG[0] + 0.24, HG[1] - 0.13, HG[1] + 0.13, Z0, 0.04, basamak=((0, 0.5, 0.12),))
zt_ = hanok_govde(y, HG[0] - 0.2, HG[0] + 0.2, HG[1] - 0.09, HG[1] + 0.09, zb_, 0.13, bay=0.1, direk='kirmizi', duvar='siva', cerceve='ahsap',
                  desen=lambda i, j, nb: 'kapi' if i == 0 else 'pencere' if j == nb // 2 else 'duvar', yuvarlak=True, ust_bant=None)
zd_ = dancheong(y, dikdortgen(HG[0] - 0.2, HG[0] + 0.2, HG[1] - 0.09, HG[1] + 0.09), zt_, 0.022, adim=0.1)
kore_cati(y, HG[0] - 0.2, HG[0] + 0.2, HG[1] - 0.09, HG[1] + 0.09, zd_, 0.19, sacak=0.08, tur='paljak', kivrim=0.42, yukari=0.035,
          alt_key='boya_yesil', ucluk='lake_koyu', ns=14)
for (x0, x1, y0, y1) in ((0.02, 0.3, 0.55, 0.7), (-0.78, -0.62, 0.05, 0.3)):
    zz = gidan(y, x0 - 0.02, x1 + 0.02, y0 - 0.02, y1 + 0.02, Z0, 0.025)
    ztt = hanok_govde(y, x0, x1, y0, y1, zz, 0.1, bay=0.08, desen=lambda i, j, nb: 'kapi' if i in (0, 1) and j % 2 else 'duvar')
    kore_cati(y, x0, x1, y0, y1, ztt, 0.12, sacak=0.05, tur='matbae', kivrim=0.35, alt_key='ahsap', ucluk='siva', sirt_h=0.016)
toprak_duvar(y, [V(-0.78, 0.4), V(-0.1, 0.4)], Z0, 0.09, govde='siva', kaide_h=0.03)

y.bolum('Sazdam evler (choga)')
for (cx_, cy_, a_) in ((-0.55, -0.22, 0.0), (-0.3, -0.05, 0.3), (0.2, 0.1, -0.2), (0.38, 0.32, 0.1), (-0.62, 0.05, 1.57)):
    with parca(y, (cx_, cy_, 0), a_):
        zz = gidan(y, -0.1, 0.1, -0.055, 0.055, Z0, 0.018, key='kaya', ust='toprak', kat=1)
        ztt = hanok_govde(y, -0.085, 0.085, -0.04, 0.04, zz, 0.075, bay=0.06, duvar='siva_krem', direk='ahsap',
                          desen=lambda i, j, nb: 'kapi' if i == 0 and j == 1 else 'pencere' if i == 0 else 'duvar')
        cati_kirma(y, -0.085, 0.085, -0.04, 0.04, ztt, 0.075, 0.035, 'saz', 'saz_koyu', 0.012, 0.0, 0.0, 'saz_koyu', ns=6, nr=4,
                   mahya_en=0.016)
y.bolum('Ağaçlar ve askerler')
for k, (tx, ty, boy) in enumerate(((-0.55, 0.2, 0.3), (-0.2, 0.8, 0.3), (0.35, 0.2, 0.32), (0.3, -0.25, 0.26), (-0.4, -0.25, 0.28),
                                   (-0.99, -0.8, 0.3), (-0.6, -0.95, 0.26), (1.05, 0.75, 0.3), (-0.25, 0.28, 0.3), (0.92, -0.1, 0.24))):
    sonamu(y, tx, ty, Z0, boy=boy, tohum=k + 40, yon=rn.uniform(0, TAU))
for (x, yy, a, zz) in ((-0.12, gy0 + 0.04, -math.pi / 2, ZG), (0.12, gy0 + 0.04, -math.pi / 2, ZG), (-0.5, FY + 0.035, -math.pi / 2, Z0 + WH),
                       (0.3, FY + 0.035, -math.pi / 2, Z0 + WH), (RX - 0.035, -0.1, 0.0, Z0 + WH), (LX + 0.035, 0.55, math.pi, Z0 + WH),
                       (0.05, FY - 0.45, math.pi / 2, Z0), (-0.04, FY - 0.6, math.pi / 2, Z0)):
    kisi(y, x, yy, zz, aci=a, boy=0.075, govde='lake_koyu' if zz > Z0 else 'beyaz', kusak='boya_sari', sapka='gat', kol='on')

calistir(y, 'lm_hwaseong')
