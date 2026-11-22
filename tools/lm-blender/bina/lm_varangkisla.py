# Varangian Guard Barracks (lm_varangkisla): the Emperor's Norse axe-men quartered against the Great Palace. A walled
# drill yard: a banded two-storey stone barracks with a timber gallery on dragon-headed posts and a gable roof with
# crossed dragon barge boards, a banded keep crowned by a timber hoarding and a steep shingle spire with dragon heads,
# a palace wing with a porphyry-columned loggia and a domed chapel, a gate with a carved Norse timber portal, guards
# drilling with Dane axes and round shields, weapon racks, a runestone, and blue banners.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from bizans_ek import *

y = Yapi()
Z0 = 0.04
KALKAN = ['boya_kirmizi', 'boya_sari', 'beyaz', 'boya_yesil', 'lacivert', 'kirmizi']


# ---------------------------------------------------------------- Norse helpers
def ejder(p, d, s=1.0, key='ahsap_koyu', goz='boya_kirmizi'):
    """a carved dragon head on a neck rising from p towards d (gaping jaws, horns, red eyes)"""
    p = Vector(p); d = Vector(d); d.z = 0; d.normalize()
    yan = Z.cross(d).normalized()
    neck = [p, p + d * (0.02 * s) + Z * (0.008 * s), p + d * (0.034 * s) + Z * (0.022 * s)]
    boru(y, neck, 0.0062 * s, key, n=6, r_son=0.0052 * s)
    h0 = neck[-1]
    boru(y, [h0, h0 + d * (0.024 * s) + Z * (0.002 * s)], 0.0056 * s, key, n=6, r_son=0.0028 * s)          # upper jaw
    boru(y, [h0 - Z * (0.005 * s), h0 + d * (0.019 * s) - Z * (0.011 * s)], 0.0032 * s, key, n=5, r_son=0.0014 * s)   # lower jaw
    for sg in (-1, 1):
        boru(y, [h0 + Z * (0.004 * s) + yan * (sg * 0.003 * s), h0 - d * (0.014 * s) + Z * (0.016 * s) + yan * (sg * 0.005 * s)],
             0.0022 * s, key, n=4, r_son=0.0008 * s)                                                          # horns
        kure(y, h0 + d * (0.008 * s) + Z * (0.004 * s) + yan * (sg * 0.0048 * s), 0.0019 * s, goz, n=5, kat=3)   # eyes
    boru(y, [p - d * (0.004 * s) + Z * (0.004 * s), p + d * (0.006 * s) + Z * (0.026 * s), p + d * (0.02 * s) + Z * (0.03 * s)], 0.002 * s, key, n=4,
         r_son=0.0008 * s)   # the curl on the neck


def kalkan_duvar(p, n, r=0.022, key='boya_kirmizi'):
    """a round shield hung flat on a wall at p facing n: painted face with a rim, a boss, a quartering stripe"""
    p, n = Vector(p), Vector(n); n.z = 0; n.normalize()
    u = Z.cross(n).normalized()
    ring = [p + n * 0.004 + (u * math.cos(TAU * i / 10) + Z * math.sin(TAU * i / 10)) * r for i in range(10)]
    y.yuz_yon(ring, key, n)
    for i in range(10):
        j = (i + 1) % 10
        y.yuz_yon([ring[i], ring[j], ring[j] - n * 0.004, ring[i] - n * 0.004], 'demir', ring[i] + ring[j] - p * 2)
    y.yuz_yon([p + n * 0.0045 - u * r * 0.92 - Z * 0.003, p + n * 0.0045 + u * r * 0.92 - Z * 0.003, p + n * 0.0045 + u * r * 0.92 + Z * 0.003,
               p + n * 0.0045 - u * r * 0.92 + Z * 0.003], 'beyaz' if key != 'beyaz' else 'boya_kirmizi', n)
    kure(y, p + n * 0.006, r * 0.24, 'bronz', n=6, kat=3)
    y.yuz_yon([q - n * 0.004 for q in ring], 'ahsap', -n)   # (its back: a propped shield is seen from behind)


# ---------------------------------------------------------------- ground and the yard
y.bolum('Zemin ve talim avlusu')
zemin(y, -1.2, 1.06, -0.98, 0.95, Z0, 'tas_koyu', basamak=(('on', 0.36),), n_basamak=3)
y.yuz_yon([V(-0.6, -0.82, Z0 + 0.0015), V(0.56, -0.82, Z0 + 0.0015), V(0.56, 0.22, Z0 + 0.0015), V(-0.6, 0.22, Z0 + 0.0015)], 'toprak', Z)
# a paved path from the gate to the barracks door
y.yuz_yon([V(-0.25, -0.82, Z0 + 0.003), V(-0.15, -0.82, Z0 + 0.003), V(-0.15, 0.22, Z0 + 0.003), V(-0.25, 0.22, Z0 + 0.003)], 'zemin', Z)

# ---------------------------------------------------------------- the barracks
y.bolum('Kışla binası')
KX0, KX1, KY0, KY1 = -0.5, 0.98, 0.34, 0.86
H1, H2 = 0.18, 0.15
kk = dikdortgen(KX0, KX1, KY0, KY1)
for i, (n1, n2) in enumerate(((7, 7), (3, 3), (6, 6), (3, 3))):
    almasik(y, kk[i], kk[(i + 1) % 4], Z0, H1, n1, en=0.36, v0=0.05, kapi_bay=(2 if i == 0 else None), ust=0.03, k_say=8)
    almasik(y, kk[i], kk[(i + 1) % 4], Z0 + H1, H2, n2, en=0.34, v0=0.04, ust=0.03, k_say=8)
kornis(y, KX0, KX1, KY0, KY1, Z0, 0.026, 0.012, 'kirec', 'kaide')
silme(y, kk, Z0 + H1 - 0.006, 0.012, 0.009, 'kirec', 'duz')
ZK = Z0 + H1 + H2
silme(y, kk, ZK - 0.014, 0.018, 0.012, 'kirec', 'tac')
for p in kk:
    kutu_merkez(y, (p.x, p.y), 0.045, 0.045, H1 + H2, 'kirec', z0=Z0)
ZR = cati_besik(y, KX0, KX1, KY0, KY1, ZK, 0.17, sacak=0.03, key='kiremit', mahya='kiremit2', kalinlik=0.01, ucluk_key='kirec', alinlik_key='ahsap_koyu',
                uc_sacak=0.03)
for cx in (-0.1, 0.6):   # brick chimneys of the guards' hearths
    cy = (KY0 + KY1) / 2 + 0.1
    kutu_merkez(y, (cx, cy), 0.05, 0.05, ZR + 0.05 - ZK, 'tugla_roma', z0=ZK)
    kutu_merkez(y, (cx, cy), 0.062, 0.062, 0.012, 'kirec', z0=ZR + 0.05)
    y.yuz_yon([V(p.x, p.y, ZR + 0.0625) for p in dikdortgen(cx - 0.02, cx + 0.02, cy - 0.02, cy + 0.02)], 'koyu', Z)
# crossed dragon barge boards on both gables (Norse)
for sx in (-1, 1):
    xg = (KX1 if sx > 0 else KX0) + sx * 0.035
    tepe = V(xg, (KY0 + KY1) / 2, ZR - 0.004)
    for sy in (-1, 1):
        alt = V(xg, (KY0 + KY1) / 2 + sy * ((KY1 - KY0) / 2 + 0.03), ZK + 0.004)
        cubuk(y, alt.lerp(tepe, 0.15), tepe + (tepe - alt).normalized() * 0.03, 0.014, 'ahsap_koyu', 0.008)
        ejder(tepe + (tepe - alt).normalized() * 0.028, V(0, -sy, 0), 1.2)
# the timber gallery along the yard face: carved posts, a balcony with a railing, a shingle lean-to
y.bolum('Ahşap galeri (ejder başlı direkler)')
GY = KY0 - 0.08
ZB = Z0 + H1                       # balcony floor
xs = [KX0 + 0.04 + (KX1 - KX0 - 0.08) * k / 9 for k in range(10)]
for x in xs:
    kutu_merkez(y, (x, GY), 0.016, 0.016, ZK + 0.02 - Z0, 'ahsap_koyu', z0=Z0)
    donel(y, (x, GY), [(0.014, Z0), (0.014, Z0 + 0.01), (0.0, Z0 + 0.01)], 'kirec', n=8)
    for zq in (Z0 + 0.06, ZB + 0.06):   # carved bands
        kutu_merkez(y, (x, GY), 0.02, 0.02, 0.008, 'boya_kirmizi', z0=zq)
    cubuk(y, V(x, GY + 0.004, ZB - 0.035), V(x, KY0, ZB - 0.004), 0.008, 'ahsap_koyu')   # brace
# the balcony: floor boards, a beam, a railing with a red top rail
kutu(y, V(KX0, GY - 0.012, ZB - 0.012), X, KX1 - KX0, KY0 - GY + 0.012, 0.012, 'ahsap')
for k in range(int((KX1 - KX0) / 0.045)):
    x = KX0 + 0.02 + 0.045 * k
    cubuk(y, V(x, GY - 0.008, ZB), V(x, GY - 0.008, ZB + 0.045), 0.005, 'ahsap_koyu')
cubuk(y, V(KX0, GY - 0.008, ZB + 0.047), V(KX1, GY - 0.008, ZB + 0.047), 0.01, 'boya_kirmizi', 0.006)
# the lean-to over the gallery
ra, rb = V(0, KY0 + 0.002, ZK - 0.004), V(0, GY - 0.03, ZK - 0.045)
for j in range(3):
    pa, pb = ra.lerp(rb, j / 3), ra.lerp(rb, (j + 1) / 3)
    for i in range(10):
        x0, x1 = KX0 - 0.02 + (KX1 - KX0 + 0.04) * i / 10, KX0 - 0.02 + (KX1 - KX0 + 0.04) * (i + 1) / 10
        y.yuz_yon([V(x0, pa.y, pa.z), V(x1, pa.y, pa.z), V(x1, pb.y, pb.z), V(x0, pb.y, pb.z)], 'sindira' if j % 2 == 0 else 'sindira2', Z - Y * 0.3)
y.yuz_yon([V(KX0 - 0.02, ra.y, ra.z - 0.008), V(KX1 + 0.02, ra.y, ra.z - 0.008), V(KX1 + 0.02, rb.y, rb.z - 0.008), V(KX0 - 0.02, rb.y, rb.z - 0.008)], 'ahsap_koyu', -Z)
y.yuz_yon([V(KX0 - 0.02, rb.y, rb.z), V(KX1 + 0.02, rb.y, rb.z), V(KX1 + 0.02, rb.y, rb.z - 0.008), V(KX0 - 0.02, rb.y, rb.z - 0.008)], 'ahsap_koyu', -Y)
for xe, s in ((KX0 - 0.02, -1), (KX1 + 0.02, 1)):
    y.yuz_yon([V(xe, ra.y, ra.z), V(xe, rb.y, rb.z), V(xe, rb.y, rb.z - 0.008), V(xe, ra.y, ra.z - 0.008)], 'ahsap_koyu', V(s, 0, 0))
cubuk(y, V(KX0 - 0.02, GY, ZK - 0.03), V(KX1 + 0.02, GY, ZK - 0.03), 0.014, 'ahsap_koyu', 0.016)
for x in (xs[0], xs[-1]):   # dragon heads at the ends of the eave beam
    ejder(V(x + (-0.03 if x < 0.2 else 0.03), GY, ZK - 0.03), V(-1 if x < 0.2 else 1, 0, 0), 1.0)
for x in xs[1:-1]:          # small dragon post-tops through the eave
    ejder(V(x, GY - 0.02, ZK - 0.036), V(0, -1, 0), 0.6)
# shields hung along the balcony
for k, x in enumerate(xs[:-1]):
    kalkan_duvar(V(x + (xs[1] - xs[0]) / 2, GY - 0.012, ZB + 0.022), V(0, -1, 0), 0.018, KALKAN[k % len(KALKAN)])
# banners at the barracks door
for sx in (-1, 1):
    dx = KX0 + (KX1 - KX0) * 2.5 / 7 + sx * 0.07
    sancak(y, dx, GY - 0.04, Z0, boy=0.27, en=0.08, yuk=0.06, aci=-math.pi / 2 + sx * 0.4, kuyruk=True)

# ---------------------------------------------------------------- the keep
y.bolum('Kule (taş gövde, ahşap hasar, şindıra külah)')
TC = (0.74, -0.5)
TW = 0.36
tk = dikdortgen(TC[0] - TW / 2, TC[0] + TW / 2, TC[1] - TW / 2, TC[1] + TW / 2)
kornis(y, tk[0].x, tk[1].x, tk[0].y, tk[2].y, Z0, 0.03, 0.014, 'kirec', 'kaide')
zz = Z0
for kat, (h, n) in enumerate(((0.22, 1), (0.2, 2), (0.18, 2))):
    for i in range(4):
        kb = 0 if (kat == 0 and i == 3) else None
        almasik(y, tk[i], tk[(i + 1) % 4], zz, h, n, en=0.4 if n == 1 else 0.34, v0=0.0 if kb == 0 else 0.06, ust=0.03, kapi_bay=kb, k_say=8)
    zz += h
    silme(y, tk, zz - 0.012, 0.014, 0.01, 'kirec', 'duz')
for p in tk:
    kutu_merkez(y, (p.x, p.y), 0.04, 0.04, zz - Z0, 'kirec', z0=Z0)
# the timber hoarding: corbelled out on brackets, plank walls with slits, posts
HW = TW / 2 + 0.035
hk = dikdortgen(TC[0] - HW, TC[0] + HW, TC[1] - HW, TC[1] + HW)
for i in range(4):
    a, b = tk[i], tk[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(5):
        p = a.lerp(b, (k + 0.5) / 5)
        cubuk(y, p + nn * 0.002 + Z * (zz - 0.05), p + nn * 0.038 + Z * (zz + 0.002), 0.012, 'ahsap_koyu', 0.01)
y.yuz_yon([V(p.x, p.y, zz) for p in hk], 'ahsap_koyu', -Z)   # (the overhang's underside: the tower top lies inside it)
HH = 0.12
for i in range(4):
    a, b = hk[i], hk[(i + 1) % 4]
    duz_duvar(y, a, b, zz, zz + HH, 'ahsap_dikey')
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(4):
        yarik(y, a.lerp(b, (k + 0.5) / 4) + Z * zz, e, nn, -0.006, HH * 0.3, 0.012, HH * 0.45, 'koyu')
for i in range(4):
    a, b = hk[i], hk[(i + 1) % 4]
    for k in range(3):
        p = a.lerp(b, k / 2)
        kutu_merkez(y, (p.x, p.y), 0.016, 0.016, HH + 0.006, 'ahsap_koyu', z0=zz - 0.003)
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    cubuk(y, a + nn * 0.004 + Z * (zz + 0.006), b + nn * 0.004 + Z * (zz + 0.006), 0.01, 'boya_kirmizi', 0.004)
zz += HH
ZT = cati_kirma(y, hk[0].x, hk[1].x, hk[0].y, hk[2].y, zz, 0.3, sacak=0.035, key='sindira', mahya='ahsap_koyu', kalinlik=0.012,
                ns=8, nr=6, dilim=['sindira', 'sindira2'])
for p in hk:   # dragon heads at the eave corners
    d = V(p.x - TC[0], p.y - TC[1]).normalized()
    ejder(V(p.x, p.y, zz + 0.006) + d * 0.04, d, 1.3)
kure(y, (TC[0], TC[1], ZT + 0.012), 0.014, 'altin', n=8, kat=4)
sancak(y, TC[0], TC[1], ZT + 0.02, boy=0.22, en=0.15, yuk=0.09, aci=math.pi * 0.85)

# ---------------------------------------------------------------- the palace wing
y.bolum('Saray kanadı (porfir sütunlu revak, şapel kubbesi)')
PX0, PX1, PY0, PY1 = -1.05, -0.74, -0.6, 0.86
PH1, PH2 = 0.2, 0.17
pk = dikdortgen(PX0, PX1, PY0, PY1)
for i, (n1, n2) in enumerate(((2, 2), (6, 6), (2, 2), (0, 6))):
    almasik(y, pk[i], pk[(i + 1) % 4], Z0, PH1, n1, en=0.36, v0=0.05, ust=0.03, k_say=8, duvar='mermer', bant='tugla_roma',
            kapi_bay=(3 if i == 3 else 2 if i == 1 else None))
    almasik(y, pk[i], pk[(i + 1) % 4], Z0 + PH1, PH2, n2, en=0.36, v0=0.04, ust=0.03, k_say=8, duvar='mermer', bant='tugla_roma')
kornis(y, PX0, PX1, PY0, PY1, Z0, 0.026, 0.012, 'mermer', 'kaide')
silme(y, pk, Z0 + PH1 - 0.006, 0.012, 0.009, 'mermer', 'duz')
ZP = Z0 + PH1 + PH2
silme(y, pk, ZP - 0.014, 0.018, 0.012, 'mermer', 'tac')
y.yuz_yon([V(p.x, p.y, ZP + 0.004) for p in pk], 'kursun', Z)
for p in pk:
    kutu_merkez(y, (p.x, p.y), 0.04, 0.04, PH1 + PH2, 'mermer', z0=Z0)
# the loggia before its outer (palace) face, towards the viewer: porphyry columns, arches, a terrace with a balustrade on top
LX = PX0 - 0.09
arkad(y, V(LX, PY1 - 0.06), V(LX, PY0 + 0.06), 7, Z0, PH1, en=0.74, ust=0.025, sivri=0.0, derin=0.086, cerceve=(0.007, ['mermer', 'tugla_roma']),
      sutun_key='granit_kizil', sutun_tur='iyon', sutun_r=0.011, sutun_yiv=14, renk=('mermer', 'tas_koyu', 'mermer', 'siva_krem'))
for yq, s in ((PY0 + 0.06, -1), (PY1 - 0.06, 1)):
    y.yuz_yon([V(PX0, yq, Z0), V(LX, yq, Z0), V(LX, yq, Z0 + PH1), V(PX0, yq, Z0 + PH1)], 'mermer', V(0, s, 0))
y.yuz_yon([V(PX0, PY0 + 0.06, Z0 + 0.001), V(LX, PY0 + 0.06, Z0 + 0.001), V(LX, PY1 - 0.06, Z0 + 0.001), V(PX0, PY1 - 0.06, Z0 + 0.001)], 'mermer', Z)
kornis(y, LX, PX0, PY0 + 0.06, PY1 - 0.06, Z0 + PH1 - 0.01, 0.014, 0.008, 'mermer', 'tac')
y.yuz_yon([V(PX0, PY0 + 0.06, Z0 + PH1 + 0.004), V(LX, PY0 + 0.06, Z0 + PH1 + 0.004), V(LX, PY1 - 0.06, Z0 + PH1 + 0.004), V(PX0, PY1 - 0.06, Z0 + PH1 + 0.004)],
          'zemin', Z)
for k in range(15):
    yq = PY0 + 0.07 + (PY1 - PY0 - 0.14) * k / 14
    y.prizma((LX - 0.004, yq), 0.004, Z0 + PH1 + 0.004, Z0 + PH1 + 0.034, 'mermer', n=6, ust=False)
kutu(y, V(LX + 0.004, PY0 + 0.06, Z0 + PH1 + 0.034), Y, PY1 - PY0 - 0.12, 0.016, 0.006, 'mermer')
# the chapel dome over the wing, a small one at each end
PC = ((PX0 + PX1) / 2, (PY0 + PY1) / 2 + 0.1)
kutu_merkez(y, PC, 0.26, 0.26, 0.03, 'tugla_roma', z0=ZP + 0.004)
kornis(y, PC[0] - 0.13, PC[0] + 0.13, PC[1] - 0.13, PC[1] + 0.13, ZP + 0.022, 0.012, 0.008, 'mermer', 'tac')
y.yuz_yon([V(p.x, p.y, ZP + 0.035) for p in dikdortgen(PC[0] - 0.13, PC[0] + 0.13, PC[1] - 0.13, PC[1] + 0.13)], 'kursun', Z)
biz_kubbe(y, PC, 0.105, ZP + 0.035, kasnak_h=0.06, n_pencere=10, kubbe_h=0.1)
for yq in (PY0 + 0.14, PY1 - 0.14):
    kucuk_kubbe(y, PC[0], yq, ZP + 0.004, 0.06, kasnak=0.03, n=20, son=False, key='kursun', kasnak_key='tugla_roma')
    y.yuz_yon([V(p.x, p.y, ZP + 0.0335) for p in cokgen((PC[0], yq), 0.06 * 1.02, 28)], 'tugla_roma', Z)   # (the drum's top ring)
    hac(y, PC[0], yq, ZP + 0.004 + 0.03 + 0.054, 0.035)
# a covered passage from the palace to the barracks (the guards' own door to the Emperor)
almasik(y, V(PX1, 0.6), V(KX0, 0.6), Z0, 0.2, 1, kapi_bay=0, ust=0.03, k_say=10)
almasik(y, V(KX0, 0.82), V(PX1, 0.82), Z0, 0.2, 0)
y.yuz_yon([V(PX1, 0.6, Z0 + 0.2), V(KX0, 0.6, Z0 + 0.2), V(KX0, 0.82, Z0 + 0.2), V(PX1, 0.82, Z0 + 0.2)], 'kursun', Z)
silme(y, [V(PX1, 0.6), V(KX0, 0.6)], Z0 + 0.19, 0.014, 0.01, 'kirec', 'tac', kapali=False)

# ---------------------------------------------------------------- the yard walls, the corner tower, the gate with its Norse portal
y.bolum('Avlu surları ve Kuzey kapısı')
WY = -0.88
GX0, GX1 = -0.33, -0.07
sur(y, [V(-1.05, WY), V(GX0, WY)], Z0, 0.14, kalinlik=0.05, key='kirec', mazgal_h=0.03, parapet_h=0.012, ust_key='zemin')
sur(y, [V(GX1, WY), V(TC[0] - TW / 2, WY)], Z0, 0.14, kalinlik=0.05, key='kirec', mazgal_h=0.03, parapet_h=0.012, ust_key='zemin')
sur(y, [V(1.02, TC[1] + TW / 2), V(1.02, KY0)], Z0, 0.14, kalinlik=0.05, key='kirec', mazgal_h=0.03, parapet_h=0.012, ust_key='zemin')
sur(y, [V(-1.05, PY0), V(-1.05, WY)], Z0, 0.14, kalinlik=0.05, key='kirec', mazgal_h=0.03, parapet_h=0.012, ust_key='zemin')
for a, b in ((V(-1.05, WY), V(GX0, WY)), (V(GX1, WY), V(TC[0] - TW / 2, WY))):
    serit_tas(y, a, b, Z0, 0, (b - a).length, 0.05, 0.016, 'tugla_roma', 0.003)
    serit_tas(y, a, b, Z0, 0, (b - a).length, 0.1, 0.016, 'tugla_roma', 0.003)
kule_yuvarlak(y, (-1.0, WY + 0.02), 0.085, Z0, 0.26, 'kirec', cati='konik', cati_key='sindira', mazgal_h=0.03, n=20, yarik_say=3, bolum=3)
# the gatehouse: two banded piers and a stone arch, the gate leaves open
for gx in (GX0 - 0.04, GX1 + 0.04):
    kutu_merkez(y, (gx, WY - 0.025), 0.08, 0.11, 0.24, 'kirec', z0=Z0)
    for zb_ in (0.05, 0.12, 0.19):
        kutu_merkez(y, (gx, WY - 0.025), 0.084, 0.114, 0.016, 'tugla_roma', z0=Z0 + zb_)
    kornis(y, gx - 0.04, gx + 0.04, WY - 0.08, WY + 0.03, Z0 + 0.23, 0.014, 0.01, 'kirec', 'tac')
    y.yuz_yon([V(p.x, p.y, Z0 + 0.246) for p in dikdortgen(gx - 0.04, gx + 0.04, WY - 0.08, WY + 0.03)], 'zemin', Z)
    mazgal(y, V(gx - 0.04, WY - 0.08), V(gx + 0.04, WY - 0.08), Z0 + 0.244, 0.028, 0.014, 'kirec')
gm = (GX0 + GX1) / 2
kutu(y, V(GX0, WY - 0.08, Z0 + 0.17), X, GX1 - GX0, 0.11, 0.07, 'kirec')
pts = [V(gm - (GX1 - GX0) / 2 * math.cos(math.pi * k / 10), WY - 0.081, Z0 + 0.12 + 0.05 * math.sin(math.pi * k / 10)) for k in range(11)]
for p, q in zip(pts, pts[1:]):
    y.yuz_yon([p, q, V(q.x, q.y, Z0 + 0.17), V(p.x, p.y, Z0 + 0.17)], 'kirec', -Y)
    y.yuz_yon([p, q, q + Y * 0.11, p + Y * 0.11], 'tas_koyu', V(gm, p.y, Z0 + 0.12) - (p + q) / 2)
    y.yuz_yon([p + Y * 0.11, q + Y * 0.11, V(q.x, q.y + 0.11, Z0 + 0.17), V(p.x, p.y + 0.11, Z0 + 0.17)], 'kirec', Y)   # (the arch's back face)
boru(y, [p - Y * 0.002 for p in pts], 0.008, 'tugla_roma', n=5)
for s in (-1, 1):
    hx = gm + s * (GX1 - GX0) / 2
    with parca(y, (hx, WY - 0.02, Z0), 1.2 if s < 0 else math.pi - 1.2):
        kutu(y, V(0, -0.005, 0), X, (GX1 - GX0) / 2 - 0.004, 0.01, 0.15, 'ahsap_koyu')
        for zq in (0.025, 0.07, 0.115):
            kutu(y, V(0.003, -0.0065, zq), X, (GX1 - GX0) / 2 - 0.01, 0.013, 0.008, 'demir')
# the Norse portal in front: two carved posts, a crossbeam, a gabled canopy with crossed dragon boards
NY = WY - 0.1
for gx in (GX0 - 0.005, GX1 + 0.005):
    kutu_merkez(y, (gx, NY), 0.022, 0.022, 0.2, 'ahsap_koyu', z0=Z0)
    for zq in (Z0 + 0.04, Z0 + 0.09, Z0 + 0.14):
        kutu_merkez(y, (gx, NY), 0.026, 0.026, 0.01, 'boya_kirmizi', z0=zq)
    boru(y, [V(gx, NY - 0.012, Z0 + 0.03 + 0.03 * k) for k in range(6)], 0.004, 'ahsap', n=4)   # carved serpent along the post
cubuk(y, V(GX0 - 0.03, NY, Z0 + 0.2), V(GX1 + 0.03, NY, Z0 + 0.2), 0.024, 'ahsap_koyu', 0.022)
# the canopy: a steep shingle gable facing the street, its ridge running back to the gatehouse
HWc, ZE, ZRc = (GX1 - GX0) / 2 + 0.05, Z0 + 0.212, Z0 + 0.34
yf, yb = NY - 0.025, WY - 0.083
for sx in (-1, 1):
    e0, r0 = V(gm + sx * HWc, 0, ZE), V(gm, 0, ZRc)
    for j in range(3):
        pa, pb = e0.lerp(r0, j / 3), e0.lerp(r0, (j + 1) / 3)
        y.yuz_yon([V(pa.x, yf, pa.z), V(pa.x, yb, pa.z), V(pb.x, yb, pb.z), V(pb.x, yf, pb.z)], 'sindira' if j % 2 == 0 else 'sindira2', Z + X * (sx * 0.5))
    y.yuz_yon([V(e0.x, yf, ZE - 0.008), V(e0.x, yb, ZE - 0.008), V(gm, yb, ZRc - 0.008), V(gm, yf, ZRc - 0.008)], 'ahsap_koyu', -Z - X * (sx * 0.5))
    y.yuz_yon([V(e0.x, yf, ZE), V(e0.x, yb, ZE), V(e0.x, yb, ZE - 0.008), V(e0.x, yf, ZE - 0.008)], 'ahsap_koyu', X * sx)
    for yq, sy in ((yf, -1), (yb, 1)):
        y.yuz_yon([V(e0.x, yq, ZE), V(gm, yq, ZRc), V(gm, yq, ZRc - 0.008), V(e0.x, yq, ZE - 0.008)], 'ahsap_koyu', Y * sy)
# the gable walls (vertical boards), set back a little under the verge
for yq, sy in ((yf + 0.008, -1), (yb, 1)):
    y.yuz_yon([V(gm - HWc, yq, ZE - 0.008), V(gm + HWc, yq, ZE - 0.008), V(gm, yq, ZRc - 0.008)], 'ahsap_dikey', Y * sy)
y.yuz_yon([V(gm - HWc, yf + 0.008, ZE - 0.008), V(gm + HWc, yf + 0.008, ZE - 0.008), V(gm + HWc, yb, ZE - 0.008),
           V(gm - HWc, yb, ZE - 0.008)], 'ahsap_koyu', -Z)
kure(y, (gm, yf + 0.004, (ZE + ZRc) / 2 - 0.01), 0.016, 'altin', n=10, kat=5)   # a gilt sun disc in the gable
cubuk(y, V(gm, yf, ZRc + 0.004), V(gm, yb, ZRc + 0.004), 0.012, 'ahsap_koyu')
# crossed barge boards ending in dragon heads above the ridge
tepe = V(gm, yf - 0.006, ZRc)
for sx in (-1, 1):
    alt = V(gm + sx * HWc, yf - 0.006, ZE)
    d = (tepe - alt).normalized()
    cubuk(y, alt, tepe + d * 0.035, 0.014, 'ahsap_koyu', 0.008)
    ejder(tepe + d * 0.03, V(-sx, 0, 0), 1.3)
sancak(y, GX1 + 0.04, WY - 0.025, Z0 + 0.246, boy=0.2, en=0.1, yuk=0.065, aci=math.pi * 1.15)

# ---------------------------------------------------------------- the guards: a drilling company, sparring pairs, the officer
y.bolum('Varang muhafızları')
for r_ in range(3):
    for c_ in range(4):
        x = -0.39 + 0.085 * c_ + 0.0425 * (r_ % 2)
        yy = -0.2 + 0.09 * r_
        muhafiz(y, x, yy, Z0 + 0.0015, aci=-math.pi / 2, s=1.0, giysi='boya_kirmizi', kalkan=KALKAN[(r_ * 5 + c_) % len(KALKAN)], silah='balta',
                kalkan_on=(r_ == 0))
muhafiz(y, -0.24, -0.4, Z0 + 0.0015, aci=math.pi / 2, s=1.1, giysi='lacivert', kalkan='altin', silah='mizrak')   # the officer
for (x, yy, a, k) in ((0.2, -0.55, 0.0, 0), (0.29, -0.55, math.pi, 1), (0.1, -0.68, 0.5, 2), (0.19, -0.64, math.pi + 0.5, 3)):
    muhafiz(y, x, yy, Z0 + 0.0015, aci=a, s=1.0, giysi='kirmizi', kalkan=KALKAN[(k + 2) % len(KALKAN)], silah='balta', kalkan_on=True)
for x, yy in ((GX0 - 0.06, NY - 0.05), (GX1 + 0.06, NY - 0.05)):
    muhafiz(y, x, yy, Z0, aci=-math.pi / 2, s=1.0, giysi='boya_kirmizi', kalkan='lacivert', silah='balta', kalkan_on=True)

# ---------------------------------------------------------------- training gear: pells, racks, a target, a brazier, the runestone
y.bolum('Talim takımları, silah sehpaları, runik taş')
for k, (x, yy) in enumerate(((0.38, -0.3), (0.46, -0.24), (0.38, -0.16))):   # pells (chopping posts)
    donel(y, (x, yy), [(0.0, Z0), (0.014, Z0), (0.013, Z0 + 0.09), (0.0, Z0 + 0.09)], 'kutuk', n=8)
    for zq in (0.035, 0.06):
        cubuk(y, V(x - 0.012, yy - 0.013, Z0 + zq), V(x + 0.012, yy - 0.013, Z0 + zq + 0.004), 0.003, 'ahsap_koyu')
    if k != 1:
        muhafiz(y, x - 0.05, yy - 0.03, Z0 + 0.0015, aci=0.5, s=1.0, giysi='kirmizi', kalkan=KALKAN[k], silah='balta')


def sehpa(cx, cy, aci, L=0.18):
    """an A-frame weapon rack: Dane axes and spears leaning on a rail, shields propped at its foot"""
    with parca(y, (cx, cy, Z0), aci):
        for sx in (-L / 2, L / 2):
            cubuk(y, V(sx, -0.025, 0), V(sx, 0, 0.09), 0.008, 'ahsap')
            cubuk(y, V(sx, 0.025, 0), V(sx, 0, 0.09), 0.008, 'ahsap')
        cubuk(y, V(-L / 2 - 0.01, 0, 0.088), V(L / 2 + 0.01, 0, 0.088), 0.009, 'ahsap_koyu')
        for k in range(6):
            x = -L / 2 + 0.02 + (L - 0.04) * k / 5
            if k % 2 == 0:   # an axe
                cubuk(y, V(x, -0.03, 0), V(x, 0.002, 0.11), 0.004, 'ahsap')
                levha(y, [V(x, -0.0, 0.098), V(x, 0.002, 0.11), V(x + 0.016, 0.006, 0.112), V(x + 0.016, -0.002, 0.092)], 'demir', V(0, -1, 0.2), 0.0016)
            else:            # a spear
                cubuk(y, V(x, -0.03, 0), V(x, 0.004, 0.13), 0.0035, 'ahsap')
                boru(y, [V(x, 0.004, 0.13), V(x, 0.0055, 0.15)], 0.004, 'demir', n=4, r_son=0.0005)
        for k in range(3):
            x = -L / 2 + 0.03 + (L - 0.06) * k / 2
            kalkan_duvar(V(x, -0.032, 0.02), V(0, -1, 0.35), 0.02, KALKAN[(k + 1) % len(KALKAN)])


sehpa(0.47, -0.02, 0.0)
sehpa(-0.5, -0.6, math.pi / 2 + 0.2)
# a straw archery target and a brazier
donel(y, (0.47, -0.74), [(0.0, Z0 + 0.03), (0.035, Z0 + 0.03), (0.035, Z0 + 0.04), (0.0, Z0 + 0.04)], 'saz', n=12)
with parca(y, (0.47, -0.74, Z0), 0.0):
    for sx in (-0.03, 0.03):
        cubuk(y, V(sx, 0.01, 0), V(sx * 0.6, 0.0, 0.1), 0.006, 'ahsap')
bh = len(y.faces)
donel(y, (0, 0), [(0.0, 0.0), (0.04, 0.0), (0.04, 0.01), (0.0, 0.01)], 'saz', n=16)
for rr, key in ((0.03, 'beyaz'), (0.02, 'boya_kirmizi'), (0.009, 'boya_sari')):
    y.yuz_yon([V(rr * math.cos(TAU * i / 16), rr * math.sin(TAU * i / 16), 0.0105 + 0.0003 * (0.03 - rr) * 100) for i in range(16)], key, Z)
donustur(y, bh, egik(0.0, math.pi / 2 - 0.25), (0.47, -0.74, Z0 + 0.075))
for x, yy in ((-0.05, 0.12), (0.3, 0.12)):
    for k in range(3):
        a = TAU * k / 3
        cubuk(y, V(x + 0.03 * math.cos(a), yy + 0.03 * math.sin(a), Z0), V(x, yy, Z0 + 0.06), 0.005, 'demir')
    donel(y, (x, yy), [(0.0, Z0 + 0.055), (0.03, Z0 + 0.065), (0.032, Z0 + 0.075), (0.0, Z0 + 0.075)], 'demir', n=10)
    kure(y, (x, yy, Z0 + 0.08), 0.017, 'altin', n=8, kat=4)
    kure(y, (x + 0.004, yy - 0.003, Z0 + 0.093), 0.01, 'boya_sari', n=8, kat=4)
# the runestone: a grey slab with a red-painted serpent band
RS = (-0.5, -0.32)
bh = len(y.faces)
donel(y, (0, 0), [(0.0, 0.0), (0.04, 0.0), (0.042, 0.06), (0.036, 0.11), (0.02, 0.135), (0.0, 0.14)], 'granit', n=12)
donustur(y, bh, ((1, 0, 0), (0, 0.35, 0), (0, 0, 1)), (RS[0], RS[1], Z0))
pts = [V(RS[0] + 0.036 * math.cos(math.pi * (0.05 + 0.9 * k / 12)), RS[1] - 0.0145, Z0 + 0.015 + 0.105 * math.sin(math.pi * (0.05 + 0.9 * k / 12)))
       for k in range(13)]
boru(y, pts, 0.004, 'boya_kirmizi', n=4)
kutu_merkez(y, RS, 0.12, 0.06, 0.008, 'tas_koyu', z0=Z0)
# ale barrels and a long bench by the barracks
for k, x in enumerate((-0.42, -0.38, -0.4)):
    zb_ = Z0 + (0.042 if k == 2 else 0.0)
    yb = 0.2 if k < 2 else 0.2
    xb = x if k < 2 else -0.4
    donel(y, (xb, yb), [(0.0, zb_), (0.017, zb_), (0.02, zb_ + 0.021), (0.017, zb_ + 0.042), (0.0, zb_ + 0.042)], 'ahsap', n=10)
    for zq in (0.008, 0.034):
        halka_kornis(y, (xb, yb), 0.018, zb_ + zq, 0.004, 0.0015, 10, 'demir')
kutu(y, V(0.05, 0.22, Z0), X, 0.2, 0.035, 0.022, 'ahsap')
kutu(y, V(0.045, 0.218, Z0 + 0.022), X, 0.21, 0.039, 0.006, 'ahsap_acik')

calistir(y, 'lm_varangkisla')
