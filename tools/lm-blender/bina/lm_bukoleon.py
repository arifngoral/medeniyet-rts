# The Boukoleon harbour (lm_bukoleon): the sea front of the Great Palace of Constantinople. The banded sea wall rising
# from the Marmara with the Boukoleon palace on it (great marble-framed windows, a marble balcony on corbels, a water
# gate down to the quay), the small walled harbour basin between two moles with chain towers at their heads, marble
# stairs down to the water, the bull-and-lion statue group that named the place, dromons (one moored, one under sail),
# boats, the palace lighthouse tower with its fire, and behind the palace the domed Pharos church and gardens.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from bizans_ortak import *

y = Yapi(tohum=6)
R = random.Random(13)

ZS = 0.025                      # sea level
ZQ = 0.068                      # quays, moles
ZL = 0.1                        # the land behind the sea wall
YW = -0.05                      # the sea wall's face
X0, X1, Y0, Y1 = -1.15, 1.15, -1.0, 0.95

# ---------------------------------------------------------------- sea and land
y.bolum('Deniz ve kara')
kutu(y, V(X0, Y0, 0), X, X1 - X0, YW - Y0, ZS, 'kaya_koyu', 'onsagsol')
y.yuz_yon([V(X0, Y0, ZS), V(X1, Y0, ZS), V(X1, YW, ZS), V(X0, YW, ZS)], 'su', Z)
kutu(y, V(X0, YW, 0), X, X1 - X0, Y1 - YW, ZL, 'tas_koyu', 'sagsolarka')
y.yuz_yon([V(X0, YW, ZL), V(X1, YW, ZL), V(X1, Y1, ZL), V(X0, Y1, ZL)], 'cimen', Z)
duz_duvar(y, V(X0, YW + 0.001), V(X1, YW + 0.001), 0, ZL, 'tas')   # (the land's face where no wall stands before it)
# ripples (lighter streaks) on the open sea
for k in range(18):
    x, yy = R.uniform(-1.05, 1.05), R.uniform(-0.97, -0.8) if k % 2 else R.uniform(-0.97, -0.1)
    if -0.82 < x < 0.6 and yy > -0.8: continue
    L = R.uniform(0.04, 0.09)
    y.yuz_yon([V(x, yy, ZS + 0.0008), V(x + L, yy, ZS + 0.0008), V(x + L, yy + 0.004, ZS + 0.0008), V(x, yy + 0.004, ZS + 0.0008)], 'beyaz', Z)

# ---------------------------------------------------------------- the moles and the basin
y.bolum('Mendirekler, rıhtım, zincir kuleleri')


def mendirek(x0, x1, y0, y1, dis=()):
    """a stone mole from ZS to ZQ; dis: its sea sides ('on', 'sag', 'sol', 'arka') get a low parapet"""
    kutu(y, V(x0, y0, ZS - 0.004), X, x1 - x0, y1 - y0, ZQ - ZS + 0.004, 'tas', 'onarkasagsol')
    y.yuz_yon([V(x0, y0, ZQ), V(x1, y0, ZQ), V(x1, y1, ZQ), V(x0, y1, ZQ)], 'zemin', Z)
    k = dikdortgen(x0, x1, y0, y1)
    silme(y, k, ZS - 0.002, 0.008, 0.006, 'kaya_koyu')
    silme(y, k, ZQ - 0.008, 0.008, 0.005, 'kirec', 'tac')
    kenar = {'on': (k[0], k[1]), 'sag': (k[1], k[2]), 'arka': (k[2], k[3]), 'sol': (k[3], k[0])}
    for d in dis:
        a, b = kenar[d]
        parapet(y, [a, b], ZQ, 0.022, 0.0, 0.016, 'kirec', kapali=False, ust_key='tas_acik')


QY = YW - 0.1                   # the quay's front edge inside the basin
mendirek(-0.8, -0.7, -0.74, YW, ('sol',))
mendirek(-0.8, -0.3, -0.84, -0.74, ('on', 'sol'))
mendirek(0.45, 0.55, -0.74, YW, ('sag',))
mendirek(0.05, 0.55, -0.84, -0.74, ('on', 'sag'))
mendirek(-0.7, 0.45, QY, YW, ())
# bollards on the quay
for k in range(9):
    x = -0.62 + k * 0.13
    y.prizma((x, QY + 0.012), 0.006, ZQ, ZQ + 0.014, 'demir', n=6)
# marble stairs down into the water
for x in (-0.42, 0.22):
    merdiven(y, (x, QY - 0.06), math.pi / 2, 0.09, ZS - 0.004, ZQ, n=6, d=0.01, key='mermer', yanlik='mermer')
# chain towers on the mole heads
for cx in (-0.31, 0.06):
    t = kule_yuvarlak(y, (cx, -0.79), 0.05, ZQ, 0.16, 'kirec', 'kubbe', 'kursun', n=16, yarik_say=2, bolum=2)
    for zb in (0.04, 0.1):
        halka_kornis(y, (cx, -0.79), 0.0515, ZQ + zb, 0.012, 0.0015, 16, 'tugla_roma')
    hac(y, cx, -0.79, t, 0.035)
# the harbour chain hanging between the towers, across the mouth
for k in range(14):
    t0, t1 = k / 14, (k + 1) / 14
    za = ZQ + 0.06 - 0.05 * math.sin(math.pi * t0); zb = ZQ + 0.06 - 0.05 * math.sin(math.pi * t1)
    cubuk(y, V(-0.26 + 0.27 * t0, -0.79, za), V(-0.26 + 0.27 * t1, -0.79, zb), 0.0035, 'demir')

# ---------------------------------------------------------------- the lighthouse
y.bolum('Deniz feneri kulesi')
LX, LY = -0.93, -0.2
kutu(y, V(-1.12, -0.42, ZS - 0.004), X, 0.36, 0.42 - 0.05 + 0.0, ZQ - ZS + 0.004, 'kaya', 'onsagsol')   # its rocky footing
y.yuz_yon([V(-1.12, -0.42, ZQ), V(-0.76, -0.42, ZQ), V(-0.76, YW, ZQ), V(-1.12, YW, ZQ)], 'kaya', Z)
for i, (w, z0, h, nwin) in enumerate(((0.26, ZQ, 0.3, 1), (0.2, ZQ + 0.3, 0.22, 2), (0.165, ZQ + 0.52, 0.15, 2))):
    kk = dikdortgen(LX - w / 2, LX + w / 2, LY - w / 2, LY + w / 2)
    for j in range(4):
        almasik(y, kk[j], kk[(j + 1) % 4], z0, h, nwin, en=0.34 if nwin == 1 else 0.4, v0=h * (0.4 if i < 2 else 0.3), ust=0.035, derin=0.018,
                kapi_bay=0 if (i == 0 and j == 1) else None, kapi_en=0.4)
    silme(y, kk, z0, 0.016, 0.01, 'kirec', 'kaide')
    silme(y, kk, z0 + h - 0.018, 0.022, 0.016, 'kirec', 'tac')
    y.yuz_yon([V(p.x, p.y, z0 + h + 0.004) for p in kk], 'zemin', Z)
    parapet(y, disa(kk, 0.014), z0 + h, 0.016, 0.0, 0.01, 'kirec', ust_key='mermer')
# the lantern: eight arches round the fire, a bronze dome, a cross
zl = ZQ + 0.67
lk = cokgen((LX, LY), 0.07, 8, math.pi / 8)
y.prizma((LX, LY), 0.073, zl, zl + 0.012, 'mermer', n=8, kat=math.pi / 8)
for j in range(8):
    a, b = lk[j], lk[(j + 1) % 8]
    y.kemerli(a, b, zl + 0.012, 0.11, ('mermer', 'mermer', 'mermer', 'boya_kirmizi'), v0=0.02, en=0.56, ust=0.014, derin=0.012, k_say=6)
    # the fire behind each arch
for k, (r, h, key) in enumerate(((0.042, 0.06, 'boya_kirmizi'), (0.03, 0.08, 'boya_sari'), (0.015, 0.095, 'beyaz'))):
    y.koni((LX, LY), r, zl + 0.012, h, key, n=8)
halka_kornis(y, (LX, LY), 0.07, zl + 0.12, 0.012, 0.01, 8, 'mermer', kat=math.pi / 8, profil='tac')
t = y.kubbe((LX, LY), 0.073, zl + 0.132, 0.075, 'bronz', n=24, kat=7)
hac(y, LX, LY, t.z, 0.05)

# ---------------------------------------------------------------- the sea wall and the palace on it
y.bolum('Deniz suru ve Bukoleon sarayı')
PX0, PX1 = -0.7, 0.45
ZB, ZP = 0.22, 0.44
PY1 = 0.32
# the sea wall below the palace: banded, blind arches, a water gate onto the quay
almasik(y, V(-0.76, YW), V(PX0, YW), ZQ, ZB - ZQ, 0)
almasik(y, V(PX0, YW), V(PX1, YW), ZQ, ZB - ZQ, 7, en=0.36, v0=0.06, ust=0.022, kapi_bay=3, kapi_en=0.48, pencere='koyu', derin=0.02,
        bant_list=[(0.0, 0.016), (0.06, 0.016)])
silme(y, [V(-0.76, YW), V(X1, YW)], ZQ, 0.014, 0.008, 'kirec', 'kaide', kapali=False)
# the sea wall's other run (to the east) with merlons and a tower
duz_duvar(y, V(PX1 + 0.1, YW), V(X1, YW), ZS, ZQ, 'tas')
almasik(y, V(PX1, YW), V(X1, YW), ZQ, ZB - ZQ, 0)
parapet(y, [V(PX1, YW), V(X1, YW)], ZB, 0.016, 0.026, 0.03, 'kirec', kapali=False)
duz_duvar(y, V(X1, YW + 0.03), V(PX1, YW + 0.03), ZL, ZB, 'kirec')   # (the sea wall's back towards the land)
y.yuz_yon([V(X1, YW, ZQ), V(X1, YW + 0.03, ZQ), V(X1, YW + 0.03, ZB), V(X1, YW, ZB)], 'kirec', X)
ET = (0.86, YW + 0.06)
ek = dikdortgen(ET[0] - 0.09, ET[0] + 0.09, ET[1] - 0.09, ET[1] + 0.09)
for j in range(4):
    almasik(y, ek[j], ek[(j + 1) % 4], ZS if j == 0 else ZL, (0.38 - ZS) if j == 0 else (0.38 - ZL), 1, en=0.3, v0=0.24 if j == 0 else 0.1,
            ust=0.035, derin=0.016)
parapet(y, ek, 0.38, 0.014, 0.026, 0.016, 'kirec')
y.yuz_yon([V(p.x, p.y, 0.3805) for p in disa(ek, -0.016)], 'zemin', Z)
# the palace front: tall marble-framed windows over a balcony
FW = (PX1 - PX0) / 5
for k in range(5):
    a, b = V(PX0 + FW * k, YW), V(PX0 + FW * (k + 1), YW)
    y.kemerli(a, b, ZB, ZP - ZB, ('kirec', 'tas_koyu', 'mermer', 'cam'), v0=0.012, en=0.5, ust=0.04, derin=0.03, k_say=10,
              cerceve=(0.014, ['mermer', 'mermer', 'tugla_roma']))
    W = (b - a).length
    for zb, hb in ((0.08, 0.016), (0.16, 0.016)):
        serit_tas(y, a, b, ZB, 0, W * 0.25 - 0.018, zb, hb)
        serit_tas(y, a, b, ZB, W * 0.75 + 0.018, W, zb, hb)
    # marble mullion and transom in the window
    m = a.lerp(b, 0.5)
    kutu(y, V(m.x - 0.005, YW - 0.012, ZB + 0.012), X, 0.01, 0.006, ZP - ZB - 0.07, 'mermer')
for k in range(6):   # pilasters between the windows
    x = PX0 + FW * k
    kutu(y, V(x - 0.012, YW, ZB), X, 0.024, -0.012, ZP - ZB, 'mermer', 'onarkasagsolust')
silme(y, [V(PX0, YW), V(PX1, YW)], ZP - 0.02, 0.026, 0.02, 'mermer', 'tac', kapali=False)
# the balcony: a marble slab on corbels with a balustrade
BY = YW - 0.07
kutu(y, V(PX0 + 0.01, BY, ZB - 0.012), X, PX1 - PX0 - 0.02, YW - BY, 0.012, 'mermer', 'onsagsolust')
y.yuz_yon([V(PX0 + 0.01, BY, ZB - 0.012), V(PX1 - 0.01, BY, ZB - 0.012), V(PX1 - 0.01, YW, ZB - 0.012), V(PX0 + 0.01, YW, ZB - 0.012)], 'mermer', -Z)
for k in range(16):
    x = PX0 + 0.03 + (PX1 - PX0 - 0.06) * k / 15
    for j in range(3):   # stepped corbel
        kutu(y, V(x - 0.008, YW, ZB - 0.012 - 0.012 * (j + 1)), X, 0.016, -(0.05 - 0.014 * j), 0.012, 'mermer', 'arkasagsolust')
        y.yuz_yon([V(x - 0.008, YW - (0.05 - 0.014 * j), ZB - 0.012 - 0.012 * (j + 1)), V(x + 0.008, YW - (0.05 - 0.014 * j), ZB - 0.012 - 0.012 * (j + 1)),
                   V(x + 0.008, YW, ZB - 0.012 - 0.012 * (j + 1)), V(x - 0.008, YW, ZB - 0.012 - 0.012 * (j + 1))], 'mermer', -Z)
# balustrade: posts and a rail along the front and the ends
for k in range(41):
    x = PX0 + 0.014 + (PX1 - PX0 - 0.028) * k / 40
    y.prizma((x, BY + 0.005), 0.003, ZB, ZB + 0.028, 'mermer', n=6, ust=False)
kutu(y, V(PX0 + 0.012, BY + 0.0005, ZB + 0.028), X, PX1 - PX0 - 0.024, 0.009, 0.006, 'mermer')
for xs in (PX0 + 0.012, PX1 - 0.021):
    kutu(y, V(xs, BY, ZB), X, 0.009, YW - BY, 0.034, 'mermer', 'onsagsolust')
# drapes and figures on the balcony
for k in (1, 3):
    x = PX0 + FW * (k + 0.5)
    insan(y, x - 0.03, YW - 0.03, ZB, 'lacivert', 1.5, aci=-math.pi / 2, sapka='altin' if k == 1 else None)
    insan(y, x + 0.03, YW - 0.03, ZB, 'beyaz', 1.45, aci=-math.pi / 2)
# the palace block behind the front: banded walls, a tiled hipped roof
for a, b, n in ((V(PX1, YW), V(PX1, PY1), 3), (V(PX1, PY1), V(PX0, PY1), 6), (V(PX0, PY1), V(PX0, YW), 3)):
    almasik(y, a, b, ZL, ZP - ZL, n, en=0.4, v0=0.12, ust=0.04, derin=0.02)
silme(y, [V(PX1, YW), V(PX1, PY1), V(PX0, PY1), V(PX0, YW)], ZP - 0.02, 0.024, 0.018, 'kirec', 'tac', kapali=False)
cati_kirma(y, PX0, PX1, YW, PY1, ZP + 0.004, 0.13, 0.03, 'kiremit', 'kiremit2', kalinlik=0.012)
y.yuz_yon([V(PX0, YW, ZP + 0.004), V(PX1, YW, ZP + 0.004), V(PX1, PY1, ZP + 0.004), V(PX0, PY1, ZP + 0.004)], 'ahsap_koyu', Z)
# the corner pavilion on the west end with a small dome
kk = dikdortgen(PX0 - 0.06, PX0 + 0.12, YW, YW + 0.18)
for j in range(4):
    almasik(y, kk[j], kk[(j + 1) % 4], ZQ if j == 0 else ZL, (ZP + 0.06 - ZQ) if j == 0 else (ZP + 0.06 - ZL), 0 if j == 0 else 1,
            en=0.36, v0=0.2, ust=0.04)
for zz in (ZB + 0.03, ZB + 0.13):
    y.kemerli(V(PX0 - 0.03, YW - 0.0001), V(PX0 + 0.09, YW - 0.0001), zz, 0.08, ('kirec', 'tas_koyu', 'mermer', 'cam'), v0=0.01, en=0.42, ust=0.012,
              derin=0.016, k_say=8, cerceve=(0.008, ['mermer', 'tugla_roma']))
silme(y, kk, ZP + 0.04, 0.022, 0.016, 'kirec', 'tac')
y.yuz_yon([V(p.x, p.y, ZP + 0.064) for p in kk], 'kursun', Z)
biz_kubbe(y, (PX0 + 0.03, YW + 0.09), 0.07, ZP + 0.064, 0.05, 8, kubbe_h=0.06)
# a domed belvedere on the roof ridge, chimneys
BX, BYc = (PX0 + PX1) / 2, (YW + PY1) / 2
bk = dikdortgen(BX - 0.08, BX + 0.08, BYc - 0.08, BYc + 0.08)
for j in range(4):
    almasik(y, bk[j], bk[(j + 1) % 4], ZP + 0.06, 0.13, 2, en=0.5, v0=0.025, ust=0.02, derin=0.014, cer=(0.006, ['mermer', 'tugla_roma']), bant_list=[(0.0, 0.012)])
silme(y, bk, ZP + 0.178, 0.016, 0.012, 'kirec', 'tac')
y.yuz_yon([V(p.x, p.y, ZP + 0.194) for p in bk], 'kursun', Z)
biz_kubbe(y, (BX, BYc), 0.06, ZP + 0.194, 0.04, 8, kubbe_h=0.055)
for x in (PX0 + 0.2, PX1 - 0.2):
    kutu_merkez(y, (x, PY1 - 0.06), 0.035, 0.035, 0.14, 'tugla_roma', z0=ZP + 0.03)
    kutu_merkez(y, (x, PY1 - 0.06), 0.045, 0.045, 0.012, 'kirec', z0=ZP + 0.17)

# ---------------------------------------------------------------- the bull and the lion
y.bolum('Boğa ve aslan heykeli')
HX, HY = -0.58, QY + 0.045
kutu_merkez(y, (HX, HY), 0.17, 0.08, 0.012, 'mermer', z0=ZQ)
kutu_merkez(y, (HX, HY), 0.155, 0.07, 0.04, 'mermer', z0=ZQ + 0.012)
kornis(y, HX - 0.0775, HX + 0.0775, HY - 0.035, HY + 0.035, ZQ + 0.046, 0.008, 0.006, 'mermer', 'tac')
zh = ZQ + 0.054
with parca(y, (HX, HY, zh), math.pi * 0.06, 1.6):
    # the bull: heavy body, short legs, head down with horns
    boru(y, [V(-0.03, 0, 0.038), V(0.0, 0, 0.04), V(0.026, 0, 0.042)], 0.016, 'mermer', n=9)
    kure(y, (0.026, 0, 0.042), 0.017, 'mermer', n=9, kat=4)
    kure(y, (-0.03, 0, 0.038), 0.016, 'mermer', n=9, kat=4)
    for lx in (0.022, -0.028):
        for ly in (0.009, -0.009):
            boru(y, [V(lx, ly, 0.028), V(lx + 0.002, ly, 0.0)], 0.005, 'mermer', n=6)
    boru(y, [V(0.038, 0, 0.044), V(0.054, 0, 0.034), V(0.062, 0, 0.022)], 0.0095, 'mermer', n=8, r_son=0.007)
    for sy in (-1, 1):
        boru(y, [V(0.052, sy * 0.006, 0.04), V(0.054, sy * 0.016, 0.046), V(0.06, sy * 0.016, 0.056)], 0.0028, 'tas_acik', n=5, r_son=0.001)
    boru(y, [V(-0.046, 0, 0.044), V(-0.052, 0, 0.02)], 0.002, 'mermer', n=4)
    # the lion leaping onto the bull's back, its jaws at the neck
    boru(y, [V(-0.05, 0.014, 0.024), V(-0.022, 0.012, 0.058), V(0.006, 0.006, 0.072)], 0.011, 'kirec', n=8, r_son=0.009)
    kure(y, (0.012, 0.005, 0.074), 0.016, 'kirec', n=9, kat=4)            # mane
    kure(y, (0.024, 0.004, 0.068), 0.008, 'kirec', n=8, kat=4)
    for sy in (-0.006, 0.014):
        boru(y, [V(0.008, sy, 0.064), V(0.026, sy - 0.004, 0.052), V(0.03, sy - 0.008, 0.044)], 0.004, 'kirec', n=5)
    for sy in (0.008, 0.02):
        boru(y, [V(-0.048, sy, 0.026), V(-0.054, sy, 0.012), V(-0.05, sy, 0.0)], 0.0045, 'kirec', n=5)
    boru(y, [V(-0.058, 0.014, 0.026), V(-0.072, 0.016, 0.03), V(-0.078, 0.016, 0.046)], 0.0018, 'kirec', n=4)

# rocks heaped along the sea wall's foot and round the lighthouse rock; guards and porters on the quay
for k in range(26):
    if k < 12:
        x, yy = R.uniform(PX1 + 0.12, X1 - 0.02), YW - R.uniform(0.015, 0.05)
    elif k < 20:
        x, yy = R.uniform(-1.12, -0.78), -0.42 - R.uniform(0.01, 0.05)
    else:
        x, yy = -0.76 + R.uniform(0.005, 0.03), R.uniform(-0.4, -0.12)
    rr = R.uniform(0.014, 0.026)
    kure(y, (x, yy, ZS - rr * 0.35), rr, 'kaya_koyu' if k % 3 else 'kaya', n=7, kat=3)
for k, x in enumerate((-0.2, 0.0, 0.32)):
    insan(y, x, QY + 0.03, ZQ, ('boya_kirmizi', 'kumas', 'boya_kirmizi')[k], 1.45, aci=-math.pi / 2, sapka='demir' if k != 1 else None)
for k in range(3):   # crates and amphorae unloaded on the quay
    kutu_merkez(y, (0.1 + 0.035 * k, QY + 0.035), 0.03, 0.03, 0.026, 'ahsap', z0=ZQ, aci=0.2 * k)
    donel(y, (-0.05 + 0.025 * k, QY + 0.04), [(0.0, ZQ), (0.006, ZQ + 0.004), (0.011, ZQ + 0.018), (0.008, ZQ + 0.03), (0.004, ZQ + 0.034), (0.0, ZQ + 0.034)],
          'kiremit', n=8)

# ---------------------------------------------------------------- ships and boats
y.bolum('Dromonlar ve kayıklar')
dromon(y, -0.12, -0.4, ZS, math.pi, L=0.44, tohum=2, yelken=False)
dromon(y, 0.8, -0.56, ZS, math.pi * 1.6, L=0.42, tohum=3, yelken=True)


def kayik(x, yy, aci, renk='ahsap', kurekci=True):
    with parca(y, (x, yy, ZS), aci):
        L, B = 0.09, 0.03
        n = 6
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            w0, w1 = B / 2 * math.sin(math.pi * t0) ** 0.6, B / 2 * math.sin(math.pi * t1) ** 0.6
            x0, x1 = -L / 2 + L * t0, -L / 2 + L * t1
            for s in (-1, 1):
                y.yuz_yon([V(x0, 0, -0.004), V(x1, 0, -0.004), V(x1, s * w1, 0.012), V(x0, s * w0, 0.012)], renk, V(0, s, 0.3))
            y.yuz_yon([V(x0, -w0, 0.0121), V(x1, -w1, 0.0121), V(x1, w1, 0.0121), V(x0, w0, 0.0121)], 'ahsap_acik', Z)
        if kurekci:
            insan(y, 0.0, 0.0, 0.0, 'kumas', 0.85, aci=math.pi)
            for s in (-1, 1):
                cubuk(y, V(0.0, s * 0.012, 0.016), V(0.012, s * 0.045, ZS * 0 - 0.002), 0.002, 'ahsap_acik')


kayik(-0.4, -0.25, 0.3, 'boya_kirmizi')
kayik(0.3, -0.3, -0.4)
kayik(0.75, -0.9, 0.2)
kayik(-0.6, -0.9, 2.8, 'boya_yesil')

# ---------------------------------------------------------------- behind the palace: the Pharos church, gardens
y.bolum('Pharos kilisesi ve bahçeler')
CX, CY = -0.15, 0.62
CW = 0.32
ck = dikdortgen(CX - CW / 2, CX + CW / 2, CY - CW / 2, CY + CW / 2)
for j in range(4):
    almasik(y, ck[j], ck[(j + 1) % 4], ZL, 0.2, 3, en=0.4, v0=0.08, ust=0.03, kapi_bay=1 if j == 0 else None, derin=0.02)
silme(y, ck, ZL + 0.186, 0.018, 0.012, 'kirec', 'tac')
silme(y, ck, ZL, 0.014, 0.008, 'kirec', 'kaide')
y.yuz_yon([V(p.x, p.y, ZL + 0.204) for p in ck], 'kursun', Z)
for (ax0, ax1, ay0, ay1) in ((CX - 0.065, CX + 0.065, CY - CW / 2, CY + CW / 2), (CX - CW / 2, CX + CW / 2, CY - 0.065, CY + 0.065)):
    duvarlar(y, dikdortgen(ax0, ax1, ay0, ay1), ZL + 0.204, ZL + 0.25, 'kirec')
    kiremit_cati(y, ax0, ax1, ay0, ay1, ZL + 0.25, 0.045, sacak=0.012)
kutu_merkez(y, (CX, CY), 0.18, 0.18, 0.08, 'kirec', z0=ZL + 0.204)
biz_kubbe(y, (CX, CY), 0.08, ZL + 0.284, 0.08, 12, kubbe_h=0.07)
for sx in (-1, 1):
    for sy in (-1, 1):
        kucuk_kubbe(y, CX + sx * 0.115, CY + sy * 0.115, ZL + 0.204, 0.03, kasnak=0.026, n=12, son=False, key='kursun', kasnak_key='tugla_roma')
donel(y, (CX, CY + CW / 2), [(0.06, ZL), (0.06, ZL + 0.17), (0.0, ZL + 0.17)], 'tugla_roma', n=12)
# a colonnaded walk from the palace to the church
for x in (CX - 0.06, CX + 0.06):
    for k in range(4):
        yy = PY1 + 0.03 + k * (CY - CW / 2 - PY1 - 0.06) / 3
        sutun(y, x, yy, ZL, ZL + 0.1, 0.008, 'mermer', 'osmanli')
cati_besik(y, CX - 0.075, CX + 0.075, PY1, CY - CW / 2, ZL + 0.1, 0.04, 0.012, 'kiremit', 'kiremit2', kalinlik=0.008, ucluk_key='mermer')
# a fountain, paths, cypresses, a small kiosk
y.yuz_yon([V(0.15, PY1 + 0.04, ZL + 0.002), V(0.6, PY1 + 0.04, ZL + 0.002), V(0.6, PY1 + 0.08, ZL + 0.002), V(0.15, PY1 + 0.08, ZL + 0.002)], 'zemin', Z)
donel(y, (0.4, 0.62), [(0.0, ZL), (0.07, ZL), (0.07, ZL + 0.02), (0.06, ZL + 0.02), (0.06, ZL + 0.01), (0.0, ZL + 0.01)], 'mermer', n=16)
y.yuz_yon([V(p.x, p.y, ZL + 0.016) for p in cokgen((0.4, 0.62), 0.06, 16)], 'su', Z)
y.prizma((0.4, 0.62), 0.01, ZL, ZL + 0.07, 'mermer', n=8)
donel(y, (0.4, 0.62), [(0.0, ZL + 0.06), (0.03, ZL + 0.068), (0.026, ZL + 0.078), (0.0, ZL + 0.074)], 'mermer', n=12)
for x, yy in ((0.2, 0.5), (0.6, 0.5), (0.2, 0.8), (0.62, 0.82), (-0.5, 0.5), (-0.55, 0.78), (-0.85, 0.4), (-0.95, 0.75), (0.95, 0.4), (0.9, 0.8),
              (-0.38, 0.85), (0.08, 0.86)):
    agac(y, x, yy, ZL, boy=0.18, tur='servi' if R.random() < 0.6 else 'yapraklı', key='yesil_koyu' if R.random() < 0.6 else 'zeytin')
# the palace banner
sancak(y, PX1 - 0.06, PY1 - 0.05, ZP + 0.05, boy=0.24, en=0.14, yuk=0.08, aci=math.pi * 0.85)

calistir(y, 'lm_bukoleon')
