# Torre del Oro, Seville (lm_altinkule): the twelve-sided Almohad tower on the Guadalquivir bank, its stone plinth
# standing in the river, the plain lower body with horseshoe windows and stepped merlons, the slimmer twelve-sided
# second body with framed blind horseshoe arches and a tile frieze, the 18th-century round top with its yellow
# glazed cupola; the wall (coracha) running to the octagonal Torre de la Plata, the Arenal quay with a crane and goods,
# a moored galleon and one under sail, boats, the harbour chain; the town and the Giralda behind.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from ispanyol_ek import *

y = Yapi()

X0, X1, Y0, Y1 = -1.15, 1.15, -1.0, 1.0
ZS, ZK = 0.02, 0.06                      # water surface, quay top
QY = -0.24                               # the quay line
T = V(-0.5, -0.2)                        # the tower's centre
KAT = math.pi / 12                       # a flat face towards -y

# ================================================================ river and land
y.bolum('Nehir ve rıhtım')
kutu(y, V(X0, Y0, 0), X, X1 - X0, QY - Y0, ZS, 'kaya_koyu', 'onsagsol')
y.yuz_yon([V(X0, Y0, ZS), V(X1, Y0, ZS), V(X1, QY, ZS), V(X0, QY, ZS)], 'su', Z)
kutu(y, V(X0, QY, 0), X, X1 - X0, Y1 - QY, ZK, 'tas', 'arkasagsol')
duz_duvar(y, V(X0, QY), V(X1, QY), ZS - 0.004, ZK, 'tas')
silme(y, [V(X0, QY), V(X1, QY)], ZK - 0.008, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
silme(y, [V(X0, QY), V(X1, QY)], ZS - 0.003, 0.008, 0.005, 'kaya_koyu', 'duz', kapali=False)
# the quay's paved strip, the town's earth behind the wall
y.yuz_yon([V(X0, QY, ZK), V(X1, QY, ZK), V(X1, Y1, ZK), V(X0, Y1, ZK)], 'zemin', Z)
# river steps down to the water (right of the tower) and bollards
merdiven(y, (-0.06, QY - 0.11), math.pi / 2, 0.09, ZS - 0.004, ZK, n=5, key='tas_koyu')
for k in range(11):
    xx = 0.06 + 0.09 * k
    y.prizma((xx, QY + 0.016), 0.0065, ZK, ZK + 0.018, 'kirec', n=8)
    kure(y, (xx, QY + 0.016, ZK + 0.02), 0.0072, 'kirec', n=8, kat=3)
for xx in (-1.08, -0.98):
    y.prizma((xx, QY + 0.016), 0.0065, ZK, ZK + 0.018, 'kirec', n=8)
    kure(y, (xx, QY + 0.016, ZK + 0.02), 0.0072, 'kirec', n=8, kat=3)


# ================================================================ the Torre del Oro
def onikigen(r, z=0.0):
    return cokgen((T.x, T.y), r, 12, KAT, z)


y.bolum('Kaide')
ZP = 0.1
R0, RP, R1 = 0.335, 0.31, 0.27
alt, ust = onikigen(R0, 0.0), onikigen(RP, ZP - 0.012)
y.serit(alt, ust, 'kum_koyu')
silme(y, onikigen(RP), ZP - 0.012, 0.012, 0.008, 'kum_acik', 'tac')
for i in range(12):   # the plinth's top round the tower
    j = (i + 1) % 12
    a, b, ai, bi = onikigen(RP + 0.008, ZP)[i], onikigen(RP + 0.008, ZP)[j], onikigen(R1, ZP)[i], onikigen(R1, ZP)[j]
    y.yuz_yon([a, b, bi, ai], 'zemin', Z)
# a few big blocks round the foot (rubble breakwater)
for k in range(9):
    a = -math.pi / 2 + (k - 4) * 0.27
    p = T + V(math.cos(a), math.sin(a)) * (R0 + 0.025)
    kutu_merkez(y, (p.x, p.y), 0.05, 0.04, 0.03, 'kaya_koyu', z0=ZS - 0.012, aci=a + 0.3 * (k % 3 - 1))

y.bolum('Birinci gövde')
Z1 = ZP + 0.58
K1 = onikigen(R1)
for i in range(12):
    a, b = K1[i], K1[(i + 1) % 12]
    yuz_ac = math.atan2((a.y + b.y) / 2 - T.y, (a.x + b.x) / 2 - T.x)
    if i % 2 == 0:
        zw = ZP + 0.28 if i % 4 == 0 else ZP + 0.17
        duz_duvar(y, a, b, ZP, zw, 'kum')
        nal_nis(y, a, b, zw, 0.13, en=0.32, ust=0.024, alfa=0.42, derin=0.016, key='kum', yan_key='kum_koyu', arka_key='koyu',
                v0=0.018, cerceve=(0.006, 'kum_acik'))
        duz_duvar(y, a, b, zw + 0.13, Z1, 'kum')
    else:
        duz_duvar(y, a, b, ZP, Z1, 'kum')
        if i % 4 == 1:   # small square lights
            ab, bb, Lb, e, nc = eksen(a, b)
            pencere_k(y, a, b, Lb / 2 - 0.009, ZP + 0.4, 0.018, 0.026, 'koyu')
            pencere_k(y, a, b, Lb / 2 - 0.007, ZP + 0.12, 0.014, 0.02, 'koyu')
# door on the land side, its stair from the quay
KD = [i for i in range(12) if (((K1[i] + K1[(i + 1) % 12]) / 2 - T).normalized().y) > 0.95][0]
# (the door face is drawn plain above; its door is a framed block on it)
a, b = K1[KD], K1[(KD + 1) % 12]
ab, bb, Lb, e, nc = eksen(a, b)
pencere_k(y, a, b, Lb / 2 - 0.022, ZP, 0.044, 0.075, 'ahsap', d=0.008, cik=0.003)
pencere_k(y, a, b, Lb / 2 - 0.03, ZP + 0.075, 0.06, 0.012, 'kum_acik', d=0.01, cik=0.006)
for sx in (-1, 1):
    pencere_k(y, a, b, Lb / 2 + sx * 0.026 - 0.004, ZP, 0.008, 0.075, 'kum_acik', d=0.01, cik=0.006)
# the stair from the quay up the plinth to the door, low cheek walls
AP = RP * math.cos(math.pi / 12)
merdiven(y, (T.x, T.y + AP + 0.048), -math.pi / 2, 0.06, ZK, ZP, n=4, d=0.012, key='kum_koyu', yanlik='kum_acik')
# the crown of the first body: a moulded band, corbels, a breastwork and stepped merlons; the terrace
silme(y, K1, Z1 - 0.06, 0.012, 0.006, 'kum_acik', 'duz')
silme(y, K1, ZP + 0.47, 0.01, 0.005, 'kum_acik', 'duz')     # a string course between the window rows
silme(y, K1, ZP, 0.03, 0.007, 'kum_koyu', 'kaide')
for i in range(12):   # corbels under the parapet
    a, b = K1[i], K1[(i + 1) % 12]
    ab, bb, Lb, e, nc = eksen(a, b)
    for k in range(4):
        u = Lb * (k + 0.5) / 4
        p = a + e * u
        kutu3(y, p + nc * 0.007 + Z * (Z1 - 0.013), e, -nc, Z, 0.012, 0.014, 0.026, 'kum_acik', ('+x', '-x', '+y', '-y', '-z'))
KP = onikigen(R1 + 0.014)
silme(y, K1, Z1 - 0.004, 0.004, 0.014, 'kum_acik', 'duz')
parapet(y, KP, Z1, 0.035, 0, 0.024, 'kum')
for i in range(12):
    a, b = KP[i], KP[(i + 1) % 12]
    e = (b - a).normalized()
    almena(y, a + e * 0.014, b - e * 0.014, Z1 + 0.035, 0.05, 0.024, 'kum', w=0.034, g=0.022)
y.yuz_yon(onikigen(R1 - 0.01, Z1 + 0.0005), 'zemin', Z)

y.bolum('İkinci gövde')
R2 = 0.165
Z2 = Z1 + 0.27
K2 = onikigen(R2)
silme(y, K2, Z1, 0.018, 0.008, 'kum_koyu', 'kaide')
for i in range(12):
    a, b = K2[i], K2[(i + 1) % 12]
    duz_duvar(y, a, b, Z1, Z1 + 0.03, 'siva_oker')
    nal_nis(y, a, b, Z1 + 0.03, 0.19, en=0.5, ust=0.03, alfa=0.45, derin=0.011, key='siva_oker', yan_key='kum_koyu',
            arka_key='koyu' if i % 3 == 0 else 'tugla_sari', v0=0.02 if i % 3 == 0 else 0.0, cerceve=(0.005, 'kum_acik'), alfiz=(0.0045, 'kum_acik'))
    duz_duvar(y, a, b, Z1 + 0.22, Z2, 'siva_oker')
    # the tile frieze: glazed squares alternating
    ab, bb, Lb, e, nc = eksen(a, b)
    nt = 5
    for k in range(nt):
        pencere_k(y, a, b, Lb * (k + 0.15) / nt, Z1 + 0.232, Lb / nt * 0.7, 0.013, 'turkuaz' if (k + i) % 2 else 'beyaz', d=0.004, cik=0.0014)
# corner pilasters
for p in K2:
    d = (p - T).normalized()
    kutu_merkez(y, (p.x + d.x * 0.002, p.y + d.y * 0.002), 0.012, 0.012, Z2 - Z1 - 0.03, 'kum_acik', z0=Z1 + 0.018, aci=math.atan2(d.y, d.x))
silme(y, K2, Z2 - 0.02, 0.012, 0.007, 'kum_acik', 'tac')
KP2 = onikigen(R2 + 0.007)
parapet(y, KP2, Z2 - 0.008, 0.026, 0, 0.018, 'siva_oker', ust_key='kum_acik')
for i in range(12):
    a, b = KP2[i], KP2[(i + 1) % 12]
    e = (b - a).normalized()
    almena(y, a + e * 0.01, b - e * 0.01, Z2 + 0.018, 0.034, 0.018, 'siva_oker', w=0.024, g=0.016)
y.yuz_yon(onikigen(R2 - 0.005, Z2 + 0.0005), 'zemin', Z)

y.bolum('Üçüncü gövde ve kubbe')
R3 = 0.088
Z3 = Z2 + 0.12
donel(y, (T.x, T.y), [(R3 + 0.006, Z2), (R3 + 0.006, Z2 + 0.012), (R3, Z2 + 0.016), (R3, Z3)], 'siva_krem', n=24)
for k in range(8):
    a = TAU * k / 8 + TAU / 16
    d = V(math.cos(a), math.sin(a)); e = V(-d.y, d.x)
    p = T + d * R3
    kutu3(y, p + d * 0.0025 + Z * ((Z2 + Z3 + 0.016) / 2), e, d, Z, 0.012, 0.007, Z3 - Z2 - 0.016, 'kum_acik', ('+x', '-x', '+y'))
    if k % 2 == 0:
        q = T + V(math.cos(a + TAU / 16), math.sin(a + TAU / 16)) * R3
        dq = (q - T).normalized()
        yarik(y, q + Z * 0, V(-dq.y, dq.x), dq, -0.008, Z2 + 0.035, 0.016, 0.05, 'koyu')
        yarik(y, q + Z * 0, V(-dq.y, dq.x), dq, -0.011, Z2 + 0.03, 0.022, 0.006, 'kum_acik')
halka_kornis(y, (T.x, T.y), R3, Z3 - 0.01, 0.014, 0.01, 24, 'kum_acik', profil='tac')
# the cupola: yellow glazed tiles, ribs, a little lantern and a gilt ball
ZD = Z3 + 0.004
prof = [(R3 + 0.006, ZD), (R3 + 0.004, ZD + 0.012), (R3 * 0.86, ZD + 0.05), (R3 * 0.55, ZD + 0.078), (R3 * 0.2, ZD + 0.09), (0.0, ZD + 0.092)]
donel(y, (T.x, T.y), prof, 'kiremit_sari', n=24)
y.yuz_yon(cokgen((T.x, T.y), R3 + 0.006, 24, z=ZD), 'kum_acik', -Z)
for k in range(8):
    a = TAU * k / 8
    d = V(math.cos(a), math.sin(a))
    pts = [T + d * (r + 0.0012) + Z * (zz + 0.0012) for r, zz in prof[1:-1]]
    boru(y, pts, 0.003, 'kum_acik', n=4)
zl = ZD + 0.088
y.prizma((T.x, T.y), 0.018, zl, zl + 0.022, 'siva_krem', n=8, ust=False)
for k in range(4):
    a = TAU * k / 4 + TAU / 16
    d = V(math.cos(a), math.sin(a))
    yarik(y, T + d * 0.0175, V(-d.y, d.x), d, -0.004, zl + 0.005, 0.008, 0.012, 'koyu')
donel(y, (T.x, T.y), [(0.024, zl + 0.022), (0.024, zl + 0.026), (0.016, zl + 0.034), (0.006, zl + 0.04), (0.0, zl + 0.041)], 'kiremit_sari', n=12)
y.prizma((T.x, T.y), 0.0025, zl + 0.04, zl + 0.06, 'altin', n=5)
kure(y, (T.x, T.y, zl + 0.066), 0.009, 'altin', n=10, kat=5)
y.prizma((T.x, T.y), 0.0016, zl + 0.074, zl + 0.09, 'altin', n=4)

y.bolum('Sancak')
ps = onikigen(R1 - 0.03)[7]
sancak(y, ps.x, ps.y, Z1, boy=0.26, en=0.13, yuk=0.08, aci=-math.pi * 0.85)

y.bolum('Liman zinciri')
for k in range(14):
    t = k / 13
    p = T + V(-0.08, -1.0).normalized() * (R0 + 0.01) + V(-0.08, -1.0).normalized() * (0.34 * t)
    zz = ZP - 0.02 - 0.09 * t + 0.03 * t * t
    if zz < ZS - 0.004: break
    kutu_merkez(y, (p.x, p.y), 0.012 if k % 2 else 0.006, 0.006 if k % 2 else 0.012, 0.006, 'demir', z0=zz - 0.003)

# ================================================================ the coracha and the Torre de la Plata
y.bolum('Sur (coracha) ve Gümüş Kule')
TP_ = V(0.38, 0.22)
w0 = T + (TP_ - T).normalized() * (R1 - 0.02)
w1 = TP_ - (TP_ - T).normalized() * 0.085
w2 = TP_ + V(0.77, 0.38).normalized() * 0.085
w3 = V(X1, TP_.y + (X1 - TP_.x) * 0.38 / 0.77)
SUR = [(w0, w1), (w2, w3)]
for a_, b_ in SUR:
    sur_duvar(y, [a_, b_], ZK, 0.2, kalin=0.05, key='kum', almena_h=0.034, kornis_key='kum_acik')
# a gate through the coracha: a framed horseshoe-headed door
ee = (w1 - w0).normalized(); nn = V(ee.y, -ee.x)
gp = w0.lerp(w1, 0.62)
pencere_k(y, gp - ee * 0.035, gp + ee * 0.035, 0.0, ZK, 0.07, 0.11, 'ahsap_koyu', d=0.006, cik=0.0015)
pencere_k(y, gp - ee * 0.045, gp + ee * 0.045, 0.0, ZK + 0.11, 0.09, 0.012, 'kum_acik', d=0.008, cik=0.004)
for sx in (-1, 1):
    pencere_k(y, gp - ee * 0.045, gp + ee * 0.045, 0.045 + sx * 0.04 - 0.005, ZK, 0.01, 0.11, 'kum_acik', d=0.008, cik=0.004)
# Torre de la Plata: octagonal, plain, merloned
OP = cokgen((TP_.x, TP_.y), 0.1, 8, math.pi / 8)
duvarlar(y, OP, ZK, ZK + 0.36, 'kum_koyu')
for i in range(8):
    a, b = OP[i], OP[(i + 1) % 8]
    ab, bb, Lb, e, nc = eksen(a, b)
    if i % 2 == 0:
        pencere_k(y, a, b, Lb / 2 - 0.007, ZK + 0.22, 0.014, 0.03, 'koyu')
    else:
        pencere_k(y, a, b, Lb / 2 - 0.004, ZK + 0.1, 0.008, 0.026, 'koyu')
silme(y, OP, ZK, 0.03, 0.008, 'kum_koyu', 'kaide')
silme(y, OP, ZK + 0.33, 0.012, 0.007, 'kum_acik', 'duz')
OP2 = cokgen((TP_.x, TP_.y), 0.107, 8, math.pi / 8)
parapet(y, OP2, ZK + 0.36, 0.02, 0, 0.02, 'kum_koyu')
for i in range(8):
    a, b = OP2[i], OP2[(i + 1) % 8]
    e = (b - a).normalized()
    almena(y, a + e * 0.012, b - e * 0.012, ZK + 0.38, 0.04, 0.02, 'kum_koyu', w=0.026, g=0.018)
y.yuz_yon(cokgen((TP_.x, TP_.y), 0.092, 8, math.pi / 8, ZK + 0.3605), 'zemin', Z)

# ================================================================ the Giralda
y.bolum('Giralda')
G = V(0.8, 0.7)
GW = 0.15
ZG = ZK + 0.6
gk = dikdortgen(G.x - GW / 2, G.x + GW / 2, G.y - GW / 2, G.y + GW / 2)
kutu_merkez(y, (G.x, G.y), GW + 0.024, GW + 0.024, 0.03, 'kum_koyu', z0=ZK)
for i in range(4):
    a, b = gk[i], gk[(i + 1) % 4]
    ab, bb, Lb, e, nc = eksen(a, b)
    # lower part plain with paired windows up the middle; the upper two thirds: sebka panels either side
    zs0 = ZK + 0.2
    duz_duvar(y, a, b, ZK + 0.03, zs0, 'tugla_sari')
    for zz in (ZK + 0.07, ZK + 0.14):
        pencere_k(y, a, b, Lb / 2 - 0.011, zz, 0.009, 0.028, 'koyu')
        pencere_k(y, a, b, Lb / 2 + 0.002, zz, 0.009, 0.028, 'koyu')
    p1, p2 = a.lerp(b, 0.34), a.lerp(b, 0.66)
    for (pa, pb) in ((a, p1), (p2, b)):
        L_ = dikdortgen_acik(y, pa, pb, zs0, ZG - zs0, 0.14, 0.86, 0.03, ZG - zs0 - 0.05, ('tugla_sari', 'tugla_sari_koyu', 'kum_acik', 'tugla_sari_koyu'), derin=0.007)[3]
        # the lattice (rhombs) of raised bars in the panel
        u0, u1, v0, v1 = 0.14, 0.86, 0.03, ZG - zs0 - 0.05
        ww = (pb - pa).length
        nr = 7
        hh = (v1 - v0) / nr
        for r in range(nr):
            for q in range(2):
                ua = u0 + (u1 - u0) * q / 2; ub = u0 + (u1 - u0) * (q + 1) / 2; um = (ua + ub) / 2
                za, zb = v0 + hh * r, v0 + hh * (r + 1)
                pts = [(ua, za + hh * 0.5), (um, za), (ub, za + hh * 0.5), (um, zb), (ua, za + hh * 0.5)]
                for k in range(4):
                    (pu, pv), (qu, qv) = pts[k], pts[k + 1]
                    cubuk(y, L_(pu, pv, 0.0035), L_(qu, qv, 0.0035), 0.0035, 'tugla_sari', 0.006)
    duz_duvar(y, p1, p2, zs0, ZG, 'tugla_sari')
    for k in range(4):
        zz = zs0 + 0.04 + k * 0.095
        pencere_k(y, a, b, Lb / 2 - 0.012, zz, 0.01, 0.032, 'koyu')
        pencere_k(y, a, b, Lb / 2 + 0.002, zz, 0.01, 0.032, 'koyu')
        pencere_k(y, a, b, Lb / 2 - 0.016, zz + 0.034, 0.032, 0.006, 'kum_acik', cik=0.003)
silme(y, gk, ZG - 0.012, 0.012, 0.008, 'kum_acik', 'tac')
y.yuz_yon(dikdortgen(G.x - GW / 2, G.x + GW / 2, G.y - GW / 2, G.y + GW / 2, ZG), 'zemin', Z)
# the Renaissance belfry: a white bell stage with arches, a balustrade, two smaller stages, the Giraldillo
B1 = 0.125
bk = dikdortgen(G.x - B1 / 2, G.x + B1 / 2, G.y - B1 / 2, G.y + B1 / 2)
pencereli_duvar(y, bk, ZG, 0.12, [2, 2, 2, 2], renk=('siva', 'kum_koyu', 'kum_acik', 'koyu'), v0=0.02, en=0.55, ust=0.02, derin=0.014,
                sivri=0.0, cerceve=(0.006, 'boya_sari'))
for p in bk:
    kutu_merkez(y, (p.x, p.y), 0.014, 0.014, 0.12, 'siva_krem', z0=ZG)
silme(y, bk, ZG + 0.12, 0.012, 0.008, 'kum_acik', 'tac')
y.yuz_yon(dikdortgen(G.x - B1 / 2, G.x + B1 / 2, G.y - B1 / 2, G.y + B1 / 2, ZG + 0.132), 'zemin', Z)
for i in range(4):   # the balustrade round the bell stage's top
    a, b = bk[i], bk[(i + 1) % 4]
    ab, bb, Lb, e, nc = eksen(a, b)
    for k in range(9):
        p = a + e * (Lb * (k + 0.5) / 9) - nc * 0.004
        y.prizma((p.x, p.y), 0.0028, ZG + 0.132, ZG + 0.152, 'siva_krem', n=5, ust=False)
    cubuk(y, a - nc * 0.004 + Z * (ZG + 0.154), b - nc * 0.004 + Z * (ZG + 0.154), 0.008, 'siva_krem', 0.005)
B2 = 0.09
b2 = dikdortgen(G.x - B2 / 2, G.x + B2 / 2, G.y - B2 / 2, G.y + B2 / 2)
pencereli_duvar(y, b2, ZG + 0.132, 0.085, [1, 1, 1, 1], renk=('siva_krem', 'kum_koyu', 'kum_acik', 'koyu'), v0=0.015, en=0.5, ust=0.02, derin=0.012,
                sivri=0.0, cerceve=(0.005, 'boya_sari'))
silme(y, b2, ZG + 0.207, 0.01, 0.007, 'kum_acik', 'tac')
y.yuz_yon(dikdortgen(G.x - B2 / 2, G.x + B2 / 2, G.y - B2 / 2, G.y + B2 / 2, ZG + 0.217), 'zemin', Z)
donel(y, (G.x, G.y), [(0.034, ZG + 0.217), (0.034, ZG + 0.272), (0.04, ZG + 0.28), (0.04, ZG + 0.286)], 'siva', n=12)
y.yuz_yon(cokgen((G.x, G.y), 0.04, 12, z=ZG + 0.286), 'kum_acik', Z)
for k in range(6):
    a = TAU * k / 6
    d = V(math.cos(a), math.sin(a))
    yarik(y, V(G.x, G.y) + d * 0.034, V(-d.y, d.x), d, -0.005, ZG + 0.232, 0.01, 0.028, 'koyu')
donel(y, (G.x, G.y), [(0.028, ZG + 0.286), (0.024, ZG + 0.31), (0.012, ZG + 0.326), (0.0, ZG + 0.33)], 'kiremit_yesil', n=12)
y.prizma((G.x, G.y), 0.004, ZG + 0.33, ZG + 0.35, 'bronz', n=5)
# the Giraldillo: a bronze figure with a shield (a weather vane)
donel(y, (G.x, G.y), [(0.008, ZG + 0.35), (0.009, ZG + 0.366), (0.006, ZG + 0.39), (0.0, ZG + 0.392)], 'bronz', n=8)
kure(y, (G.x, G.y, ZG + 0.397), 0.005, 'bronz', n=7, kat=4)
cubuk(y, V(G.x + 0.003, G.y, ZG + 0.36), V(G.x + 0.003, G.y, ZG + 0.43), 0.0025, 'bronz')
levha(y, [V(G.x + 0.005, G.y, ZG + 0.39), V(G.x + 0.03, G.y, ZG + 0.39), V(G.x + 0.03, G.y, ZG + 0.42), V(G.x + 0.005, G.y, ZG + 0.42)], 'bronz', Y, kil=0.002)

# ================================================================ the town
y.bolum('Kent evleri')
import random as _r
rr = _r.Random(5)


def sur_tarafi(px, py):
    """> 0: on the river side of the wall line (the Arenal), < 0: in the town"""
    best = None
    for a_, b_ in ((w0, w3),):
        ab = b_ - a_
        return (px - a_.x) * ab.y - (py - a_.y) * ab.x


def sur_uzak(px, py):
    d = 9.0
    for a_, b_ in ((w0, w1), (w2, w3)):
        ab = b_ - a_; t = max(0, min(1, (V(px, py) - a_).dot(ab) / ab.length_squared))
        d = min(d, (V(px, py) - a_.lerp(b_, t)).length)
    return d


def bina_yeri(x0, x1, y0, y1):
    """keep the houses off the tower, the wall, the Giralda and the Torre de la Plata, inside the town"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = max(x1 - x0, y1 - y0) / 2
    if (V(cx, cy) - T).length < R0 + r + 0.05: return False
    if abs(cx - G.x) < 0.1 + (x1 - x0) / 2 + 0.03 and abs(cy - G.y) < 0.1 + (y1 - y0) / 2 + 0.03: return False
    if (V(cx, cy) - TP_).length < 0.12 + r: return False
    if sur_uzak(cx, cy) < r + 0.05: return False
    if sur_tarafi(cx, cy) > 0: return False
    return True


EVLER = [(-1.06, -0.88, 0.55, 0.76), (-0.84, -0.64, 0.6, 0.84), (-1.06, -0.9, 0.82, 0.97), (-0.6, -0.42, 0.66, 0.95),
         (-0.38, -0.18, 0.72, 0.96), (-0.14, 0.04, 0.8, 0.97), (0.08, 0.24, 0.78, 0.97), (-1.06, -0.9, 0.24, 0.46),
         (-0.86, -0.68, 0.32, 0.52), (-0.62, -0.44, 0.4, 0.58), (-0.4, -0.22, 0.44, 0.64), (-0.16, 0.04, 0.5, 0.68),
         (0.28, 0.44, 0.8, 0.97), (0.48, 0.62, 0.84, 0.97), (0.95, 1.1, 0.84, 0.97), (0.06, 0.22, 0.52, 0.7),
         (-1.07, -0.93, -0.02, 0.18), (0.27, 0.42, 0.56, 0.74), (0.5, 0.64, 0.62, 0.78), (-0.26, -0.1, 0.24, 0.4),
         (-0.04, 0.12, 0.3, 0.46)]
for k, (x0, x1, y0, y1) in enumerate(EVLER):
    if not bina_yeri(x0, x1, y0, y1): continue
    h = 0.08 + 0.06 * rr.random()
    duv = rr.choice(('siva', 'siva', 'siva_krem', 'siva_oker', 'siva'))
    if k % 4 == 3:   # a flat-roofed house (azotea) with a parapet and a little roof pavilion
        kk = dikdortgen(x0, x1, y0, y1)
        duvarlar(y, kk, ZK, ZK + h, duv)
        for i in range(4):
            a, b = kk[i], kk[(i + 1) % 4]
            ab, bb, Lb, e, nc = eksen(a, b)
            nw = max(1, int(Lb / 0.07))
            for q in range(nw):
                pencere_k(y, a, b, Lb * (q + 0.5) / nw - 0.006, ZK + h * 0.55, 0.012, 0.02, 'koyu')
        parapet(y, kk, ZK + h, 0.016, 0, 0.008, duv, ust_key='tas_acik')
        y.yuz_yon(dikdortgen(x0 + 0.008, x1 - 0.008, y0 + 0.008, y1 - 0.008, ZK + h + 0.0005), 'kiremit2', Z)
        cx_, cy_ = x0 + 0.04, y1 - 0.04
        ev(y, cx_ - 0.028, cx_ + 0.028, cy_ - 0.028, cy_ + 0.028, ZK + h, 0.04, duvar=duv, pencere=False, kapi_yon=None)
    else:
        ev(y, x0, x1, y0, y1, ZK, h, duvar=duv, cati=rr.choice(('kiremit', 'kiremit2')), tohum=k, kapi_yon='on')
# palms and orange trees in the open places
for (px, py) in ((-0.95, -0.12), (-1.02, 0.6), (0.2, 0.06), (-0.12, 0.22), (0.55, 0.45), (0.95, 0.2), (1.05, 0.0)):
    palmiye(y, px, py, ZK, 0.17 + 0.03 * rr.random(), tohum=int(px * 100 + py * 7))
for (px, py) in ((-0.68, 0.22), (-0.45, 0.32), (-0.85, 0.12), (0.2, 0.42), (-0.3, 0.12)):
    if bina_yeri(px - 0.03, px + 0.03, py - 0.03, py + 0.03):
        y.prizma((px, py), 0.004, ZK, ZK + 0.03, 'ahsap', n=5)
        kure(y, (px, py, ZK + 0.05), 0.025, 'yesil_koyu', n=9, kat=5)
        for k in range(3):
            a = TAU * k / 3 + px
            kure(y, (px + 0.016 * math.cos(a), py + 0.016 * math.sin(a), ZK + 0.055), 0.004, 'boya_sari', n=5, kat=3)

# ================================================================ the Arenal quay: goods, crane
y.bolum('Arenal: yük, vinç')
vinc(y, 0.3, QY + 0.07, ZK, -math.pi / 2, boy=0.26, kol=0.2, yuk='sandik', ip_boy=0.12)
for xx, yy_ in ((0.52, -0.13), (0.55, -0.1), (0.58, -0.135), (0.54, -0.16), (0.98, -0.13), (1.01, -0.1), (0.04, -0.12)):
    varil(y, xx, yy_, ZK, 0.012, 0.03)
sandik(y, 0.66, -0.14, ZK, aci=0.2); sandik(y, 0.69, -0.11, ZK, aci=-0.1); sandik(y, 0.67, -0.125, ZK + 0.022, aci=0.1, w=0.026, d=0.022, h=0.018)
sandik(y, 1.06, -0.16, ZK, aci=0.3); sandik(y, 0.12, -0.08, ZK, aci=0.5)
kereste(y, 0.84, -0.08, ZK, L=0.14, n=3, kat=2, aci=0.15)
gulle_yigini(y, -0.08, -0.08, ZK, 3, 0.008)
top_kizak(y, -0.98, -0.18, ZK, -math.pi / 2 - 0.3, L=0.1, r=0.011)
top_kizak(y, -0.2, -0.17, ZK, -math.pi / 2 + 0.3, L=0.1, r=0.011)
# merchants' figures on the quay
for k, (xx, yy_, a) in enumerate(((0.46, -0.1, 2.0), (0.6, -0.05, -2.5), (0.9, -0.15, 1.0), (0.2, -0.13, 0.5), (0.75, 0.05, 3.0))):
    asker(y, xx, yy_, ZK, 0.9, a, silah=None, govde=('boya_kirmizi', 'kumas', 'boya_yesil', 'ahsap_acik', 'boya_sari')[k], pantolon='ahsap_koyu', zirh=False)

# ================================================================ ships on the river
y.bolum('Kalyonlar')
kalyon(y, 0.3, -0.47, ZS, math.pi, L=0.56, B=0.14, yelken='sarili', tohum=2, sancakli=False)
kalyon(y, 0.74, -0.79, ZS, math.pi - 0.12, L=0.62, B=0.15, yelken='acik', tohum=3)
sandal(y, -0.18, -0.4, ZS, 0.4)
sandal(y, -1.0, -0.72, ZS, -0.5, kurek=True)
sandal(y, -0.6, -0.86, ZS, 2.6)
dalga(y, X0 + 0.05, X1 - 0.05, Y0 + 0.05, QY - 0.05, ZS, n=46, tohum=4, boy=0.035,
      kacin=lambda x, yy: (V(x, yy) - T).length < R0 + 0.06 or (abs(x - 0.3) < 0.36 and abs(yy + 0.47) < 0.12) or (abs(x - 0.74) < 0.42 and abs(yy + 0.79) < 0.12))

calistir(y, 'lm_altinkule')
