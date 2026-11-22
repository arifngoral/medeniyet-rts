# Güneş Taşı Tapınağı (lm_taktakvim): the Aztec Sun Stone (Piedra del Sol) set upright on a stepped platform: the
# carved and painted calendar disc (Tonatiuh's face with the knife tongue, the four Ollin cartouches, the twenty day
# signs, the sun rays, the two fire serpents round the rim, the 13 Reed date), priests and braziers before it; behind
# it a round temple of Ehecatl (circular talud platform, cylindrical shrine with a serpent-mouth door, conical thatch).
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mexika_ortak import *

y = Yapi()
R = random.Random(31)
Z0 = 0.04

# ---------------------------------------------------------------- ground
y.bolum('Zemin')
zemin(y, -1.15, 1.15, -1.17, 1.2, Z0, 'kaya_koyu', 'cimen_kuru', basamak=(), silmeli=True)
kutu(y, V(-1.0, -1.08, Z0), X, 2.0, 2.16, 0.003, 'zemin', 'onarkasagsolust')
PZ = Z0 + 0.003
# a painted way to the stair
y.yuz_yon([V(-0.2, -1.08, PZ + 0.001), V(0.2, -1.08, PZ + 0.001), V(0.2, -0.86, PZ + 0.001), V(-0.2, -0.86, PZ + 0.001)], 'kirec', Z)

# ---------------------------------------------------------------- the platform
y.bolum('Platform')
PC = (0.0, 0.03)
bw, bd, z1 = kademe(y, PC, 0.88, 0.8, PZ, 0.095, 0.03, talud=0.66, key='kirec', bant_key='siva', ust_key='zemin', cizgi='boya_kirmizi')
bant_diskleri(y, PC, bw, bd, PZ + 0.095 * 0.66 + 0.014, 0.0095, 0.08, lambda p: 'turkuaz' if (int((p.x + p.y) * 12) % 2) else 'boya_kirmizi', 'beyaz',
              atla=lambda p: abs(p.x) < 0.33 and p.y < 0)
bw2, bd2, ZP = kademe(y, PC, bw - 0.035, bd - 0.035, z1, 0.085, 0.03, talud=0.66, key='kirec', bant_key='siva', ust_key='zemin', cizgi='boya_kirmizi')
bant_diskleri(y, PC, bw2, bd2, z1 + 0.085 * 0.66 + 0.012, 0.0095, 0.08, lambda p: 'boya_kirmizi' if (int((p.x - p.y) * 12) % 2) else 'turkuaz', 'beyaz',
              atla=lambda p: abs(p.x) < 0.33 and p.y < 0)
PF = PC[1] - bd2
ayak = alfarda_merdiven(y, 0.0, PC[1] - 0.8 - 0.17, PF, PZ, ZP, 0.56, key='kirec', alf_key='siva', alf_en=0.04, dado=0.16, dado_h=0.03)
for p in ayak:
    yilan_basi(y, (p.x, p.y - 0.045, PZ), -math.pi / 2, 0.075, 'kirec', tuy='boya_yesil')
for sx in (-1, 1):
    yilan_basi(y, (sx * (bw - 0.03), PC[1] - bd - 0.04, PZ), -math.pi / 2, 0.07, 'kirec')
    sancak(y, sx * (bw2 - 0.04), PF + 0.04, ZP, boy=0.26, en=0.11, yuk=0.07, aci=math.pi / 2 + sx * 0.5)

# ---------------------------------------------------------------- the Sun Stone
y.bolum('Gunes tasi')
SY = -0.3
RS = 0.34
T = 0.034                      # half thickness
# the pedestal: a stepped block, a red band, carved discs
kutu_merkez(y, (0, SY), 0.62, 0.24, 0.045, 'kirec', z0=ZP)
silme(y, dikdortgen(-0.31, 0.31, SY - 0.12, SY + 0.12), ZP + 0.035, 0.01, 0.004, 'boya_kirmizi')
kutu_merkez(y, (0, SY), 0.5, 0.15, 0.05, 'bazalt', z0=ZP + 0.045)
for k in range(5):
    y.oculus(V(-0.2 + k * 0.1, SY - 0.0751, ZP + 0.07), X, -Y, 0.012, 'turkuaz', 'boya_sari', f=0.004, k=10)
ZC = ZP + 0.095 + RS - 0.03
C = V(0, SY, ZC)
N = V(0, -1, 0)
for sx in (-1, 1):   # stone wedges steadying the disc
    kesik(y, (sx * 0.2, SY), 0.07, 0.15, 0.035, 0.1, ZP + 0.095, ZP + 0.15, 'bazalt')
halka_disk(y, C, N, 0.0, RS, -T, T, 'granit_koyu', m=64, arka=True)
F = T


def kat(r0, r1, h, key, a0=0.0, a1=TAU, m=48, d=None):
    halka_disk(y, C, N, r0, r1, F, F + h, key, m=m, a0=a0, a1=a1)


def oyma(uv, h, key, h0=None):
    kabartma(y, C, N, uv, F if h0 is None else F + h0, F + h, key)


def kutup(r, t):
    return (r * math.cos(t), r * math.sin(t))


# the background layers
kat(0.272, 0.336, 0.003, 'siva_oker', m=64)                     # outer band (the fire serpents lie on it)
kat(0.17, 0.272, 0.002, 'boya_kirmizi', m=64)                   # the sun-ray field
kat(0.0, 0.17, 0.0025, 'siva_oker', m=48)                       # the inner field
# the two fire serpents (xiuhcoatl): segmented bodies round the rim from the top, their heads meeting at the bottom
seg = 13
for sgn in (-1, 1):
    for k in range(seg):
        t0 = math.pi / 2 + sgn * (0.17 + k * (math.pi - 0.17 - 0.33) / seg)
        t1 = math.pi / 2 + sgn * (0.17 + (k + 0.8) * (math.pi - 0.17 - 0.33) / seg)
        a0, a1 = min(t0, t1), max(t0, t1)
        kat(0.282, 0.328, 0.007, 'turkuaz' if k % 2 == 0 else 'boya_kirmizi', a0, a1, m=4)
        # flame tufts on each segment
        tm = (a0 + a1) / 2
        oyma([kutup(0.31, tm - 0.04), kutup(0.31, tm + 0.04), kutup(0.338, tm)], 0.009, 'boya_sari')
    # the head at the bottom, its jaws open towards the other's (a human face emerges between)
    th = -math.pi / 2 + sgn * 0.2
    cu, cv = kutup(0.3, th)
    oyma(daire(0.04, 14, cu, cv), 0.009, 'turkuaz')
    oyma(daire(0.022, 10, cu - sgn * 0.012, cv + 0.008), 0.012, 'boya_kirmizi')
    oyma(daire(0.008, 8, cu + sgn * 0.01, cv + 0.012), 0.014, 'koyu')
    oyma([(cu - sgn * 0.035, cv - 0.02), (cu - sgn * 0.06, cv - 0.03), (cu - sgn * 0.04, cv)], 0.01, 'beyaz')     # fangs
oyma(daire(0.024, 12, 0, -0.312), 0.011, 'boya_sari')            # the faces emerging from the jaws
for sx in (-1, 1):
    oyma(daire(0.005, 6, sx * 0.008, -0.308), 0.013, 'koyu')
# the 13 Reed date cartouche at the top
oyma([(-0.03, 0.276), (0.03, 0.276), (0.03, 0.334), (-0.03, 0.334)], 0.008, 'beyaz')
oyma([(-0.018, 0.288), (0.018, 0.288), (0.018, 0.322), (-0.018, 0.322)], 0.011, 'boya_kirmizi')
for k in range(3):
    oyma(daire(0.004, 6, -0.012 + k * 0.012, 0.305), 0.013, 'koyu')
# a ring of beads round the ray field
for k in range(56):
    t = TAU * (k + 0.5) / 56
    oyma(daire(0.0055, 6, *kutup(0.262, t)), 0.005, 'beyaz')
# the sun rays: eight great points (the four cardinal ones larger) and eight small ones
for k in range(8):
    t = math.pi / 2 + TAU * k / 8
    buyuk = k % 2 == 0
    w = 0.11 if buyuk else 0.085
    oyma([kutup(0.18, t - w / 2 / 0.18 * 0.9), kutup(0.18, t + w / 2 / 0.18 * 0.9), kutup(0.255 if buyuk else 0.24, t)], 0.007, 'boya_sari')
    oyma([kutup(0.185, t - w / 2 / 0.18 * 0.55), kutup(0.185, t + w / 2 / 0.18 * 0.55), kutup(0.235 if buyuk else 0.222, t)], 0.0095, 'siva_oker')
    t2 = t + TAU / 16
    oyma([kutup(0.19, t2 - 0.12), kutup(0.19, t2 + 0.12), kutup(0.235, t2)], 0.006, 'turkuaz')
# the ring of the twenty day signs
kat(0.168, 0.176, 0.006, 'beyaz', m=64)
kat(0.118, 0.126, 0.006, 'beyaz', m=64)
for k in range(20):
    t = math.pi / 2 - TAU * (k + 0.5) / 20
    cu, cv = kutup(0.147, t)
    ex, ey = math.cos(t), math.sin(t)
    s = 0.0135
    q = [(cu + (-ey * a + ex * b) * s, cv + (ex * a + ey * b) * s) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    oyma(q, 0.008, ('boya_kirmizi', 'turkuaz', 'beyaz', 'boya_sari')[k % 4])
    oyma(daire(0.0045, 6, cu, cv), 0.01, 'koyu' if k % 4 != 1 else 'beyaz')
    tt = t - TAU / 40
    oyma([kutup(0.127, tt - 0.01), kutup(0.127, tt + 0.01), kutup(0.167, tt + 0.006), kutup(0.167, tt - 0.006)], 0.007, 'beyaz')
# Ollin: the four cartouches of the previous suns on the diagonals, the claws holding hearts at the sides
for k in range(4):
    t = math.pi / 4 + k * math.pi / 2
    cu, cv = kutup(0.083, t)
    ex, ey = math.cos(t), math.sin(t)
    q = [(cu + (-ey * a * 0.028 + ex * b * 0.03), cv + (ex * a * 0.028 + ey * b * 0.03)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    oyma(q, 0.008, 'turkuaz')
    q2 = [(cu + (-ey * a * 0.019 + ex * b * 0.021), cv + (ex * a * 0.019 + ey * b * 0.021)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    oyma(q2, 0.011, 'boya_kirmizi')
    oyma(daire(0.006, 6, cu, cv), 0.013, 'beyaz')
for sx in (-1, 1):
    cu = sx * 0.088
    oyma(daire(0.021, 10, cu, 0.0), 0.009, 'boya_sari')                  # the clawed hand
    for k in range(3):
        oyma([(cu + sx * 0.012, -0.014 + k * 0.012), (cu + sx * 0.032, -0.02 + k * 0.014), (cu + sx * 0.016, -0.008 + k * 0.012)], 0.011, 'beyaz')
    oyma(daire(0.011, 8, cu - sx * 0.004, 0.0), 0.012, 'boya_kirmizi')  # the heart
# Tonatiuh's face in the centre
oyma(daire(0.058, 20), 0.012, 'boya_sari')
oyma(daire(0.05, 20, 0, 0.004), 0.0135, 'siva_oker')
for sx in (-1, 1):
    oyma([(sx * 0.012, 0.016), (sx * 0.034, 0.02), (sx * 0.034, 0.03), (sx * 0.012, 0.026)], 0.0155, 'koyu')      # brows
    oyma(daire(0.0075, 8, sx * 0.022, 0.006), 0.016, 'beyaz')                                                       # eyes
    oyma(daire(0.0038, 6, sx * 0.022, 0.006), 0.0175, 'koyu')
    oyma(daire(0.011, 10, sx * 0.063, -0.004), 0.013, 'turkuaz')                                                    # ear spools
    oyma(daire(0.005, 8, sx * 0.063, -0.004), 0.0145, 'beyaz')
oyma([(-0.006, 0.0), (0.006, 0.0), (0.009, -0.012), (-0.009, -0.012)], 0.016, 'siva_oker')                          # nose
oyma([(-0.018, -0.02), (0.018, -0.02), (0.014, -0.03), (-0.014, -0.03)], 0.016, 'boya_kirmizi')                      # mouth
oyma([(-0.009, -0.024), (0.009, -0.024), (0.0, -0.068)], 0.019, 'beyaz')                                             # the knife tongue
oyma([(-0.03, 0.04), (0.03, 0.04), (0.022, 0.054), (-0.022, 0.054)], 0.015, 'turkuaz')                               # headband
# the back: dressed stone with a red-painted ring, a carved sun (eight rays round a turquoise boss) and two rings
NB = V(0, 1, 0)
halka_disk(y, C, NB, 0.25, 0.27, T, T + 0.004, 'boya_kirmizi', m=48)
halka_disk(y, C, NB, 0.1, 0.115, T, T + 0.004, 'granit', m=32)
halka_disk(y, C, NB, 0.0, 0.05, T, T + 0.006, 'turkuaz', m=20)
ub, vb, _ = taban(NB)
for k in range(8):
    t = math.pi / 2 + TAU * k / 8
    w = 0.05 if k % 2 == 0 else 0.035
    kabartma(y, C + NB * T, NB, [kutup(0.125, t - w / 0.125), kutup(0.125, t + w / 0.125), kutup(0.235 if k % 2 == 0 else 0.2, t)], 0.0, 0.004,
             'granit')
# the rim: a carved band of star (Venus) eyes round the edge
for k in range(56):
    t = TAU * (k + 0.5) / 56
    rd = ub * math.cos(t) + vb * math.sin(t)
    if rd.z < -0.6: continue                           # (hidden in the pedestal)
    kabartma(y, C + rd * RS, rd, daire(0.009, 8), 0.0, 0.003, 'beyaz' if k % 2 else 'boya_sari', u=N.cross(rd).normalized() * -1)

# priests and braziers before the stone
for sx in (-1, 1):
    donel(y, (sx * 0.4, SY - 0.06), [(0, ZP), (0.035, ZP), (0.035, ZP + 0.012), (0.024, ZP + 0.02), (0.024, ZP + 0.07), (0.034, ZP + 0.08), (0, ZP + 0.08)],
          'kirec', n=12)
    mangal(y, sx * 0.4, SY - 0.06, ZP + 0.08, 0.06, 'siva_oker', 'boya_kirmizi')
    mangal(y, sx * 0.62, PF + 0.05, ZP, 0.05, 'siva_oker', 'turkuaz')
for (px, py, a_, kol, pel) in ((-0.15, SY - 0.2, math.pi / 2, 'kalk', 'boya_kirmizi'), (0.12, SY - 0.22, math.pi / 2 + 0.2, 'kalk', 'koyu'),
                               (0.0, SY - 0.28, math.pi / 2, 'asa', 'turkuaz'), (-0.3, SY - 0.15, math.pi / 2 - 0.4, 'one', 'koyu'),
                               (0.3, SY - 0.17, math.pi / 2 + 0.5, 'one', 'boya_kirmizi')):
    kisi(y, px, py, ZP, a_, 0.05, 'koyu', 'koyu', kol=kol, pelerin=pel, bas='boya_yesil' if kol == 'asa' else None)
for (px, py, a_) in ((-0.1, PF - 0.12, math.pi / 2), (0.14, PF - 0.25, math.pi / 2), (-0.5, -0.95, 0.6), (0.55, -0.98, 2.4)):
    zz = ZP * 0.5 + PZ * 0.5 if py > PF - 0.2 else PZ
    if py < PC[1] - 0.8 - 0.17: zz = PZ
    kisi(y, px, py, zz if py > PC[1] - 0.8 - 0.17 else PZ, a_, 0.05, 'kiremit', 'beyaz', kol='yan', bas='boya_sari')

# ---------------------------------------------------------------- the round temple of Ehecatl behind
y.bolum('Ehecatl tapinagi')
EC = (0.0, 0.42)
r = 0.37
z = ZP
for k, (hh, ins) in enumerate(((0.085, 0.04), (0.08, 0.04), (0.075, 0.035))):
    zm, zt = z + hh * 0.7, z + hh
    rn = r - ins * 0.85 - 0.015
    donel(y, EC, [(r, z), (r - ins, zm), (r - ins * 0.85, zm), (r - ins * 0.85, zt), (rn, zt)], 'kirec', n=48)
    halka_kornis(y, EC, r - ins * 0.85, zt - 0.008, 0.008, 0.003, 48, 'boya_kirmizi')
    for j in range(24):
        t = TAU * j / 24
        if abs(t - 1.5 * math.pi) < 0.35: continue
        p = V(EC[0] + (r - ins * 0.85 + 0.0005) * math.cos(t), EC[1] + (r - ins * 0.85 + 0.0005) * math.sin(t), (zm + zt) / 2 - 0.003)
        nn = V(math.cos(t), math.sin(t))
        y.oculus(p, V(-nn.y, nn.x), nn, 0.008, 'turkuaz' if (j + k) % 2 else 'boya_kirmizi', 'beyaz', f=0.003, k=8)
    r, z = rn, zt
y.yuz_yon([V(p_.x, p_.y, z) for p_ in cokgen(EC, r, 48)], 'kirec', Z)
ZE = z
# the front stair of the round platform
ayak = alfarda_merdiven(y, 0.0, EC[1] - 0.37 - 0.19, EC[1] - r + 0.02, ZP, ZE, 0.17, key='kirec', alf_key='siva', alf_en=0.03, dado=0.14, dado_h=0.03)
for p in ayak:
    yilan_basi(y, (p.x, p.y - 0.032, ZP), -math.pi / 2, 0.055, 'kirec', tuy='boya_yesil')
# the cylindrical shrine
RC = 0.19
HC = 0.17
n = 24
kose = cokgen(EC, RC, n, kat=-math.pi / 2 - math.pi / n * 3)
for i in range(n):
    if i in (0, 1, 2): continue
    duz_duvar(y, kose[i], kose[(i + 1) % n], ZE, ZE + HC, 'siva')
a, b = kose[0], kose[3]
W_, e_, nc_, L_ = dikdortgen_kapi(y, a, b, ZE, HC, 0.22, 0.78, 0.115, 'boya_kirmizi', 'koyu', derin=0.035)
# the serpent mouth round the door: upper fangs, eyes and snout above, the forked tongue on the threshold
for k in range(5):
    u = 0.26 + k * 0.12
    p = L_(u, 0.115, -0.003)
    y.yuz_yon([p - e_ * 0.008, p + e_ * 0.008, p - Z * 0.018], 'beyaz', nc_)
for sx in (-1, 1):
    p = L_(0.5 + sx * 0.3, 0.14, -0.004)
    kabartma(y, p, nc_, daire(0.012, 10), 0.0, 0.004, 'beyaz', u=e_)
    kabartma(y, p, nc_, daire(0.006, 8), 0.0, 0.007, 'koyu', u=e_)
    p2 = L_(0.5 + sx * 0.08, 0.152, -0.004)
    kabartma(y, p2, nc_, daire(0.01, 8), 0.0, 0.006, 'turkuaz', u=e_)
boru(y, [L_(0.5, 0.001, 0.0) + Z * 0.002, L_(0.5, 0.001, -0.045) + Z * 0.002], 0.006, 'boya_kirmizi', n=4)
for sx in (-1, 1):
    boru(y, [L_(0.5, 0.001, -0.045) + Z * 0.002, L_(0.5 + sx * 0.08, 0.001, -0.06) + Z * 0.002], 0.005, 'boya_kirmizi', n=4, r_son=0.002)
# bands round the drum: red dado, a frieze of turquoise discs and red
halka_kornis(y, EC, RC, ZE, 0.018, 0.003, n, 'boya_kirmizi', kat=-math.pi / 2 - math.pi / n * 3)
halka_kornis(y, EC, RC, ZE + HC - 0.03, 0.03, 0.003, n, 'lacivert', kat=-math.pi / 2 - math.pi / n * 3)
for j in range(n):
    if j in (0, 1, 2): continue
    t = -math.pi / 2 - math.pi / n * 3 + TAU * (j + 0.5) / n
    nn = V(math.cos(t), math.sin(t))
    rr = RC * math.cos(math.pi / n) + 0.0035
    y.oculus(V(EC[0], EC[1], ZE + HC - 0.015) + nn * rr, V(-nn.y, nn.x), nn, 0.0085, 'turkuaz', 'beyaz', f=0.003, k=8)
# the conical thatch roof, the finial with wind-shell discs
zr = ZE + HC
y.yuz_yon([V(p_.x, p_.y, zr) for p_ in cokgen(EC, RC, n, kat=-math.pi / 2 - math.pi / n * 3)], 'siva', Z)
tepe = saz_konik(y, EC, RC + 0.01, zr, 0.4, kat=4, sacak=0.045, kalin=0.018, n=32, tepe='altin')
donel(y, EC, [(0.0, tepe - 0.004), (0.006, tepe), (0.006, tepe + 0.05), (0.0, tepe + 0.056)], 'ahsap', n=6)
for k in range(3):
    halka_disk(y, V(EC[0], EC[1], tepe + 0.015 + k * 0.014), Z, 0.0, 0.016 - k * 0.003, -0.002, 0.002, 'boya_kirmizi' if k % 2 else 'beyaz', m=12, arka=True)
sancak(y, 0.24, EC[1] + 0.1, ZE, boy=0.3, en=0.12, yuk=0.075, aci=0.3)
for sx in (-1, 1):
    mangal(y, sx * 0.13, EC[1] - r - 0.0, ZE, 0.045, 'siva_oker', 'boya_kirmizi')

# ---------------------------------------------------------------- small thatched shrines at the platform's back corners
y.bolum('Yan tapinaklar')
for sx in (-1, 1):
    cx, cy = sx * 0.58, 0.5
    vurgu = 'boya_kirmizi' if sx > 0 else 'turkuaz'
    bw_, bd_, zs = kademe(y, (cx, cy), 0.15, 0.14, ZP, 0.07, 0.016, talud=0.6, key='kirec', bant_key='siva', ust_key='kirec', cizgi=vurgu)
    alfarda_merdiven(y, cx, cy - 0.14 - 0.08, cy - bd_, ZP, zs, 0.1, key='kirec', alf_key='siva', alf_en=0.018, dado=0.15, dado_h=0.012)
    w, d = 0.18, 0.15
    kose = dikdortgen(cx - w / 2, cx + w / 2, cy - d / 2 + 0.01, cy + d / 2 + 0.01)
    dikdortgen_kapi(y, kose[0], kose[1], zs, 0.1, 0.33, 0.67, 0.075, 'siva', 'koyu', cerceve=(0.008, vurgu), derin=0.02)
    for i in (1, 2, 3):
        duz_duvar(y, kose[i], kose[(i + 1) % 4], zs, zs + 0.1, 'siva')
    silme(y, kose, zs, 0.014, 0.003, vurgu)
    silme(y, kose, zs + 0.1 - 0.02, 0.02, 0.003, vurgu)
    cati_kirma(y, cx - w / 2, cx + w / 2, cy - d / 2 + 0.01, cy + d / 2 + 0.01, zs + 0.1, 0.17, 0.03, 'saz', 'saz_koyu', kalinlik=0.016, nr=5, ns=8,
               dilim=['saz', 'saz_koyu'], mahya_en=0.014)
    kure(y, (cx, cy + 0.01, zs + 0.272), 0.012, 'altin', n=8, kat=4)
    mangal(y, cx + sx * 0.1, cy - bd_ + 0.02, zs, 0.035, 'siva_oker', vurgu)
# great fire-serpent heads on pedestals flanking the stone
for sx in (-1, 1):
    kutu_merkez(y, (sx * 0.56, -0.38), 0.12, 0.16, 0.06, 'bazalt', z0=ZP)
    silme(y, dikdortgen(sx * 0.56 - 0.06, sx * 0.56 + 0.06, -0.46, -0.3), ZP + 0.05, 0.01, 0.003, 'boya_kirmizi')
    yilan_basi(y, (sx * 0.56, -0.355, ZP + 0.06), -math.pi / 2, 0.15, 'turkuaz', agiz='boya_kirmizi', pul='boya_sari', tuy='boya_kirmizi')

# ---------------------------------------------------------------- trees and a small tzompantli-free corner: offerings at the back
y.bolum('Cevre')
for (tx, ty, b) in ((-0.98, 0.98, 0.16), (-0.78, 1.06, 0.13), (0.95, 1.0, 0.15), (1.02, 0.78, 0.12), (-1.02, -1.0, 0.12), (1.0, -1.02, 0.13)):
    agac(y, tx, ty, PZ, b, 'yapraklı', 'boya_yesil' if tx < 0 else 'zeytin')
for sx in (-1, 1):
    mangal(y, sx * 0.5, -1.0, PZ, 0.05, 'siva_oker', 'boya_kirmizi')

calistir(y, 'lm_taktakvim')
