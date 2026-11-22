# Tlatelolco Pazarı (lm_tlatelolco): the great market of Tlatelolco as Bernal Diaz saw it: a paved square of awninged stalls
# in rows by trade (maize, cacao, quetzal feathers, pottery, obsidian blades, cloth, fruit), a canal along one side with a
# canoe landing, a wooden bridge and warehouses, the judges' dais under a canopy; behind it the twin-temple pyramid of
# Tlatelolco with its double stair and serpent heads, the red shrine of Huitzilopochtli and the blue-white one of Tlaloc.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from aztek_parca import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(7)
Z0 = 0.04
KX0, KX1 = 0.6, 0.86              # the canal
ZS = Z0 - 0.026                   # its water

y.bolum('Meydan ve kanal')
for (x0, x1, key, ust) in ((-1.15, KX0, 'kaya_koyu', 'zemin'), (KX1, 1.15, 'kaya_koyu', 'cimen_kuru')):
    kutu(y, V(x0, -1.12, 0), X, x1 - x0, 2.24, Z0, key, 'onarkasagsol')
    y.yuz_yon([V(x0, -1.12, Z0), V(x1, -1.12, Z0), V(x1, 1.12, Z0), V(x0, 1.12, Z0)], ust, Z)
kutu(y, V(KX0, -1.12, 0), X, KX1 - KX0, 2.24, ZS, 'kaya_koyu', 'onarka')
y.yuz_yon([V(KX0, -1.12, ZS), V(KX1, -1.12, ZS), V(KX1, 1.12, ZS), V(KX0, 1.12, ZS)], 'su', Z)
# stone kerbs along the canal
for x, s in ((KX0, 1), (KX1, -1)):
    kutu_merkez(y, (x - s * 0.012, 0), 0.024, 2.24, 0.008, 'kirec', z0=Z0)
# the market floor: a lighter paving with darker aisles
y.yuz_yon([V(-1.08, -1.08, Z0 + 0.001), V(0.54, -1.08, Z0 + 0.001), V(0.54, -0.22, Z0 + 0.001), V(-1.08, -0.22, Z0 + 0.001)], 'kirec', Z)
y.yuz_yon([V(-0.27, -1.12, Z0 + 0.002), V(0.03, -1.12, Z0 + 0.002), V(0.03, -0.22, Z0 + 0.002), V(-0.27, -0.22, Z0 + 0.002)], 'zemin', Z)

# ---------------- the twin pyramid ----------------
y.bolum('İkiz tapınaklı piramit')
PC = V(-0.12, 0.56)
W0, D0, W1, D1, NT, PH = 1.06, 0.76, 0.7, 0.38, 4, 0.56
ZT = Z0 + PH
basamakli_piramit(y, (PC.x, PC.y), W0, W1, NT, PH, 'kirec', talud=0.6, tablero_key='boya_kirmizi', merdiven=False, z0=Z0, d0=D0, d1=D1)
th = PH / NT
for k in range(NT):   # white discs on the tableros
    t0, t1 = k / NT, (k + 1) / NT
    hw0, hd0 = (W0 + (W1 - W0) * t0) / 2, (D0 + (D1 - D0) * t0) / 2
    hw1 = (W0 + (W1 - W0) * t1) / 2
    ins = (hw0 - hw1) * 0.75
    tw, td = hw0 - ins * 0.85, hd0 - ins * 0.85
    zc = Z0 + th * k + th * 0.6 + (th * 0.06 + th * 0.4 - th * 0.08) / 2
    kose = dikdortgen(PC.x - tw, PC.x + tw, PC.y - td, PC.y + td)
    for i in range(4):
        a, b = kose[i], kose[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        m = int(L / 0.08)
        for j in range(m):
            p = a.lerp(b, (j + 0.5) / m)
            if i == 0 and abs(p.x - PC.x) < 0.27: continue
            y.oculus(p + nn * 0.0005 + Z * zc, e, nn, th * 0.075, 'beyaz', 'siva', f=0.004, k=10)
y.bolum('Çifte merdiven ve yılan başları')
YS = PC.y - D1 / 2
YB = YS - 0.56
ayaklar = []
for sx in (-1, 1):
    ayaklar += alfarda_merdiven(y, PC.x + sx * 0.125, YB, YS, Z0, ZT, 0.18, n=20, key='kirec', alfarda_key='siva', alfarda_en=0.035, dado=0.13, dado_h=0.06)
# the two inner balustrades meet in the middle: one serpent head there, not two heads inside each other
orta = [p for p in ayaklar if abs(p.x - PC.x) < 0.06]
dis = [p for p in ayaklar if abs(p.x - PC.x) >= 0.06]
if orta: dis.append(sum(orta, V(0, 0)) / len(orta))
for p in dis:
    yilan_bas(y, V(p.x, p.y - 0.035, Z0 + 0.035), V(0, -1), 0.07)

def kafatasi_frizi(alt_, ust_, s0, s1, r, adim):
    """on each slope of a truncated-pyramid roof: two white bands (at s0 and s1 up the slope) framing two staggered
    rows of small white skull discs with dark eye sockets: a carved frieze, not scattered dots"""
    for i in range(4):
        j = (i + 1) % 4
        e = (alt_[j] - alt_[i]).normalized()
        t = ((ust_[i] + ust_[j]) / 2 - (alt_[i] + alt_[j]) / 2).normalized()
        n = e.cross(t).normalized()
        if n.z < 0: n = -n
        L = lambda s: (alt_[i].lerp(ust_[i], s), alt_[j].lerp(ust_[j], s))
        bw = (s1 - s0) * 0.12
        for sa, sb in ((s0, s0 + bw), (s1 - bw, s1)):
            a0, b0 = L(sa); a1, b1 = L(sb)
            y.yuz_yon([p + n * 0.0012 for p in (a0, b0, b1, a1)], 'beyaz', n)
        for row, s in enumerate((s0 + (s1 - s0) * 0.36, s0 + (s1 - s0) * 0.64)):
            a_, b_ = L(s)
            m = max(2, int((b_ - a_).length / adim))
            for kk in range(m - row):
                c = a_.lerp(b_, (kk + 0.5 + 0.5 * row) / m) + n * 0.0015
                y.yuz_yon([c + (e * math.cos(TAU * u / 8) + t * 1.1 * math.sin(TAU * u / 8)) * r for u in range(8)], 'beyaz', n)
                for sx in (-1, 1):   # the eye sockets
                    q = c + n * 0.0006 + e * (sx * r * 0.42) + t * (r * 0.15)
                    y.yuz_yon([q + (e * math.cos(TAU * u / 5) + t * math.sin(TAU * u / 5)) * r * 0.26 for u in range(5)], 'koyu', n)


# ---------------- the two shrines ----------------
def turbe(cx, cy, w, d, h, renk, cati):
    """a temple-top shrine: walls with a door, painted bands, a tall truncated-pyramid roof, merlons round its top"""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2
    dikdortgen_acik(y, V(x0, y0), V(x1, y0), ZT, h, 0.34, 0.66, 0.0, h * 0.72, ('siva', 'koyu', 'kirec', 'koyu'), derin=0.025, cerceve=(0.012, renk))
    for a, b in ((V(x1, y0), V(x1, y1)), (V(x1, y1), V(x0, y1)), (V(x0, y1), V(x0, y0))):
        duz_duvar(y, a, b, ZT, ZT + h, 'siva')
    k = dikdortgen(x0, x1, y0, y1)
    silme(y, k, ZT, 0.025, 0.004, renk)
    silme(y, k, ZT + h - 0.028, 0.02, 0.004, renk)
    kutu(y, V(x0 - 0.02, y0 - 0.02, ZT + h), X, w + 0.04, d + 0.04, 0.02, 'siva', 'onarkasagsol')
    zr = ZT + h + 0.02
    w0, d0 = w + 0.04, d + 0.04
    zk = zr + 0.2
    if cati == 'tlaloc':        # blue-white vertical stripes
        kesik_piramit(y, (cx, cy), w0, d0, w0 * 0.62, d0 * 0.52, zr, zk, ['turkuaz', 'beyaz'], n_dilim=9)
    else:                       # red with a frieze of white skulls between white bands (Huitzilopochtli)
        kesik_piramit(y, (cx, cy), w0, d0, w0 * 0.62, d0 * 0.52, zr, zk, 'boya_kirmizi')
        alt_ = dikdortgen(cx - w0 / 2, cx + w0 / 2, cy - d0 / 2, cy + d0 / 2, zr)
        ust_ = dikdortgen(cx - w0 * 0.31, cx + w0 * 0.31, cy - d0 * 0.26, cy + d0 * 0.26, zk)
        kafatasi_frizi(alt_, ust_, 0.24, 0.66, 0.0085, 0.028)
    kornis(y, cx - w0 * 0.31, cx + w0 * 0.31, cy - d0 * 0.26, cy + d0 * 0.26, zk - 0.01, 0.01, 0.005, renk)
    almena_halka(y, dikdortgen(cx - w0 * 0.31, cx + w0 * 0.31, cy - d0 * 0.26, cy + d0 * 0.26), zk, 0.055, 0.01, 'siva', bosluk=0.018)
    return zk + 0.055


y.bolum('Huitzilopochtli ve Tlaloc türbeleri')
SY = PC.y + 0.03
turbe(PC.x - 0.17, SY, 0.27, 0.24, 0.13, 'boya_kirmizi', 'huitzilo')
turbe(PC.x + 0.17, SY, 0.27, 0.24, 0.13, 'turkuaz', 'tlaloc')
# the sacrificial stone and braziers on the top
kutu_merkez(y, (PC.x, YS + 0.05), 0.05, 0.035, 0.04, 'bazalt', z0=ZT)
for sx in (-1, 1):
    mangal(y, PC.x + sx * 0.31, YS + 0.05, ZT, 0.06)
    sancak(y, PC.x + sx * 0.32, PC.y + D1 / 2 - 0.04, ZT, boy=0.34, en=0.1, yuk=0.065, aci=-math.pi / 2 + sx * 0.5, direk_key='ahsap_koyu', kuyruk=True)

# ---------------- the market ----------------
y.bolum('Pazar tezgâhları')
MALLAR = ['misir', 'kakao', 'tuy', 'comlek', 'obsidyen', 'kumas', 'meyve', 'misir', 'tuy', 'kakao', 'comlek', 'meyve', 'kumas', 'obsidyen', 'misir']
TENTE = [('saz', 'saz_koyu'), ('kumas',), None, ('saz',), ('kumas', 'kumas', 'boya_kirmizi', 'kumas'), ('saz_koyu', 'saz'), None, ('kumas', 'turkuaz', 'kumas', 'kumas')]
i = 0
for yy in (-0.96, -0.7, -0.44):
    for xx in (-0.96, -0.72, -0.48, 0.2, 0.44):
        tezgah(y, xx, yy, 0.18, 0.13, 0.12, aci=0.0, tente=TENTE[i % len(TENTE)], mal=MALLAR[i % len(MALLAR)], tohum=i, z=Z0 + 0.001, arka_oran=1.35)
        i += 1
# the goods spill out: sacks, jars and bundles in the aisles
for k in range(16):
    x = rn.choice((-1.05, -0.84, -0.6, -0.36, 0.08, 0.32, 0.54)) + rn.uniform(-0.02, 0.02)
    yy = rn.choice((-1.05, -0.83, -0.57, -0.31)) + rn.uniform(-0.02, 0.02)
    if rn.random() < 0.5:
        donel(y, (x, yy), [(0.0, Z0), (0.012, Z0), (0.018, Z0 + 0.018), (0.011, Z0 + 0.032), (0.013, Z0 + 0.036), (0.0, Z0 + 0.034)],
              rn.choice(('kiremit', 'siva_oker', 'kiremit2')), n=8)
    else:
        elipsoid(y, (x, yy, Z0), (0.02, 0.016, 0.022), rn.choice(('kumas', 'saz', 'ahsap_acik')), n=8, kat=4, aci=rn.uniform(0, 3), ust_yarim=True)
y.bolum('Pazar halkı ve hamallar')
for k in range(22):
    x = rn.choice((-1.06, -0.84, -0.6, -0.36, -0.2, -0.05, 0.08, 0.32, 0.55)) + rn.uniform(-0.025, 0.025)
    yy = rn.uniform(-1.05, -0.28)
    if -0.3 < x < 0.06 and yy > -0.4: continue
    insan(y, x, yy, Z0, rn.uniform(0, TAU), 0.065 + rn.uniform(-0.006, 0.006), rn.choice(('beyaz', 'beyaz', 'kumas', 'siva_krem')),
          rn.choice((None, None, 'saz', 'kumas', 'ahsap_acik')), tohum=k)
for (x, yy, a) in ((0.66, -0.9, 0.0), (0.66, -0.78, math.pi), (0.64, -0.62, 0.3)):   # porters unloading at the pier
    insan(y, x, yy, Z0 + 0.014, a, 0.065, 'beyaz', 'saz')

y.bolum('Tüccar revakı')
AX0, AX1, AY0, AY1 = -1.1, -0.9, 0.02, 1.06
AH = 0.13
# an open hall on two rows of painted pillars, a flat roof with a red fascia and merlons
NP = 7
kutu_merkez(y, ((AX0 + AX1) / 2, (AY0 + AY1) / 2), AX1 - AX0 + 0.04, AY1 - AY0 + 0.03, 0.012, 'kirec', z0=Z0)
for xx in (AX0 + 0.015, AX1):
    for k in range(NP + 1):
        yy = AY0 + 0.015 + (AY1 - AY0 - 0.03) * k / NP
        kutu_merkez(y, (xx, yy), 0.03, 0.03, AH - 0.012, 'boya_kirmizi', z0=Z0 + 0.012)
        kutu_merkez(y, (xx, yy), 0.036, 0.036, 0.012, 'turkuaz', z0=Z0 + AH * 0.55)
RX0_, RX1_, RY0_, RY1_ = AX0 - 0.012, AX1 + 0.025, AY0 - 0.01, AY1 + 0.01
kutu(y, V(RX0_, RY0_, Z0 + AH), X, RX1_ - RX0_, RY1_ - RY0_, 0.025, 'siva', 'onarkasagsol')
y.yuz_yon([V(p.x, p.y, Z0 + AH + 0.025) for p in dikdortgen(RX0_, RX1_, RY0_, RY1_)], 'zemin', Z)
silme(y, dikdortgen(RX0_, RX1_, RY0_, RY1_), Z0 + AH + 0.004, 0.016, 0.003, 'boya_kirmizi')
for a, b in ((V(RX1_, RY0_), V(RX1_, RY1_)), (V(RX0_, RY1_), V(RX0_, RY0_)), (V(RX0_, RY0_), V(RX1_, RY0_))):
    almenalar(y, a, b, Z0 + AH + 0.025, 0.035, 0.008, 'siva', bosluk=0.025)
# on the roof terrace: reed mats with dyed cloth and maize laid out to dry, bundles and jars between them
ZRT = Z0 + AH + 0.025
for k in range(6):
    yc = AY0 + 0.1 + k * 0.165
    kk = ('kumas', 'boya_kirmizi', 'boya_sari', 'turkuaz', 'kumas', 'boya_sari')[k]
    y.yuz_yon([V(AX0 + 0.01, yc - 0.05, ZRT + 0.0015), V(AX1 - 0.005, yc - 0.05, ZRT + 0.0015), V(AX1 - 0.005, yc + 0.05, ZRT + 0.0015),
               V(AX0 + 0.01, yc + 0.05, ZRT + 0.0015)], 'saz', Z)
    y.yuz_yon([V(AX0 + 0.03, yc - 0.035, ZRT + 0.003), V(AX1 - 0.025, yc - 0.035, ZRT + 0.003), V(AX1 - 0.025, yc + 0.035, ZRT + 0.003),
               V(AX0 + 0.03, yc + 0.035, ZRT + 0.003)], kk, Z)
    if k % 2 == 0:
        elipsoid(y, ((AX0 + AX1) / 2, yc + 0.082, ZRT), (0.022, 0.018, 0.02), ('ahsap_acik', 'kumas', 'saz')[k // 2], n=8, kat=4, ust_yarim=True)
    else:
        donel(y, ((AX0 + AX1) / 2, yc + 0.082), [(0.0, ZRT), (0.012, ZRT), (0.017, ZRT + 0.018), (0.011, ZRT + 0.03), (0.013, ZRT + 0.034), (0.0, ZRT + 0.032)], 'kiremit', n=8)
ZA = Z0 + 0.012
for k in range(NP):   # goods under the arcade: bales of cloth, jars, sacks
    yy = AY0 + 0.015 + (AY1 - AY0 - 0.03) * (k + 0.5) / NP
    y.yuz_yon([V(AX0 + 0.02, yy - 0.05, ZA + 0.002), V(AX0 + 0.12, yy - 0.05, ZA + 0.002), V(AX0 + 0.12, yy + 0.05, ZA + 0.002), V(AX0 + 0.02, yy + 0.05, ZA + 0.002)], 'saz', Z)
    for j in range(3):
        kk = ('boya_kirmizi', 'kumas', 'turkuaz', 'boya_sari', 'kiremit', 'beyaz')[(k + j) % 6]
        if (k + j) % 3 == 0:
            donel(y, (AX0 + 0.045 + j * 0.03, yy + 0.02 * (j - 1)), [(0.0, ZA + 0.002), (0.011, ZA + 0.002), (0.016, ZA + 0.016), (0.01, ZA + 0.028), (0.012, ZA + 0.032), (0.0, ZA + 0.03)], 'kiremit', n=8)
        else:
            kutu_merkez(y, (AX0 + 0.045 + j * 0.03, yy + 0.02 * (j - 1)), 0.026, 0.03, 0.018, kk, z0=ZA + 0.002, aci=0.3 * j)
    insan(y, (AX0 + AX1) / 2 + 0.03, yy + 0.03, ZA, -0.3 + k, 0.065, ('beyaz', 'kumas')[k % 2], None)

y.bolum('Yargıç kürsüsü')
JC = V(-0.8, -0.12)
kutu_merkez(y, (JC.x, JC.y), 0.3, 0.22, 0.06, 'siva', z0=Z0)
kornis(y, JC.x - 0.15, JC.x + 0.15, JC.y - 0.11, JC.y + 0.11, Z0 + 0.045, 0.015, 0.005, 'boya_kirmizi')
y.yuz_yon([V(p.x, p.y, Z0 + 0.0605) for p in dikdortgen(JC.x - 0.15, JC.x + 0.15, JC.y - 0.11, JC.y + 0.11)], 'saz', Z)
alfarda_merdiven(y, JC.x, JC.y - 0.11 - 0.06, JC.y - 0.11, Z0, Z0 + 0.06, 0.1, n=4, key='kirec', alfarda_key='siva', alfarda_en=0.018, dado=0.0, dado_h=0.0)
for (dx, dy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
    cubuk(y, V(JC.x + dx * 0.13, JC.y + dy * 0.09, Z0 + 0.06), V(JC.x + dx * 0.13, JC.y + dy * 0.09, Z0 + 0.19), 0.01, 'lake')
saz_cati(y, JC.x - 0.13, JC.x + 0.13, JC.y - 0.09, JC.y + 0.09, Z0 + 0.19, 0.12, sacak=0.03, nr=6, kalin=0.012)
# the judges' reed seats (icpalli) with tall backs
for sx in (-1, 0, 1):
    x = JC.x + sx * 0.07
    kutu_merkez(y, (x, JC.y + 0.03), 0.045, 0.04, 0.02, 'saz_koyu', z0=Z0 + 0.06)
    levha(y, V(x - 0.022, JC.y + 0.05, Z0 + 0.06), X, [(0, 0), (0.044, 0), (0.044, 0.06), (0.022, 0.07), (0, 0.06)], 0.008, 'saz', 'saz_koyu')
    kure(y, (x, JC.y + 0.03, Z0 + 0.1), 0.012, 'boya_yesil' if sx else 'turkuaz', n=6, kat=3)

y.bolum('Kano iskelesi ve köprü')
for k in range(12):   # pier along the canal
    yy = -0.95 + k * 0.035
    kutu_merkez(y, (KX0 + 0.05, yy), 0.1, 0.03, 0.006, 'ahsap_acik' if k % 2 else 'ahsap', z0=Z0 + 0.008)
for yy in (-0.95, -0.75, -0.57):
    cubuk(y, V(KX0 + 0.09, yy, ZS - 0.004), V(KX0 + 0.09, yy, Z0 + 0.04), 0.012, 'ahsap_koyu')
for (yy, a, yuk) in ((-0.88, math.pi / 2 + 0.03, ['boya_sari', 'altin', 'boya_sari']), (-0.66, math.pi / 2 - 0.04, ['kiremit', 'siva_oker']),
                     (-0.2, math.pi / 2, ['boya_yesil', 'boya_kirmizi', 'kumas']), (0.35, math.pi / 2 + 0.05, ['ahsap_acik', 'kerpic_koyu']),
                     (0.8, math.pi / 2 - 0.05, None)):
    kano(y, (KX0 + KX1) / 2 + 0.02, yy, ZS + 0.012, 0.22, 0.05, 0.022, a, yuk=yuk)
# a plank bridge
BY = 0.1
for sx in (-1, 1):
    kutu_merkez(y, (KX0 - 0.02 if sx < 0 else KX1 + 0.02, BY), 0.05, 0.14, 0.02, 'kirec', z0=Z0)
y0b = BY - 0.055
for k in range(9):
    t = k / 8
    x = KX0 - 0.02 + (KX1 - KX0 + 0.04) * t
    zz = Z0 + 0.02 + 0.03 * math.sin(math.pi * t)
    kutu_merkez(y, (x, BY), (KX1 - KX0 + 0.04) / 8 + 0.004, 0.11, 0.008, 'ahsap_acik' if k % 2 else 'ahsap', z0=zz)
for sy in (-1, 1):
    pts = [V(KX0 - 0.02 + (KX1 - KX0 + 0.04) * k / 8, BY + sy * 0.05, Z0 + 0.06 + 0.03 * math.sin(math.pi * k / 8)) for k in range(9)]
    boru(y, pts, 0.004, 'ahsap_koyu', n=4)
    for p in pts[::2]:
        cubuk(y, p - Z * 0.035, p, 0.006, 'ahsap_koyu')

y.bolum('Karşı kıyı: ambarlar')
for (cx, cy) in ((1.0, -0.7), (1.0, -0.25)):
    x0, x1, y0, y1 = cx - 0.07, cx + 0.07, cy - 0.15, cy + 0.15
    kutu_merkez(y, (cx, cy), 0.16, 0.32, 0.02, 'kirec', z0=Z0)
    dikdortgen_acik(y, V(x0, y1), V(x0, y0), Z0 + 0.02, 0.1, 0.38, 0.62, 0.0, 0.075, ('siva_krem', 'kerpic_koyu', 'kirec', 'koyu'), derin=0.015)
    for a, b in ((V(x0, y0), V(x1, y0)), (V(x1, y0), V(x1, y1)), (V(x1, y1), V(x0, y1))):
        duz_duvar(y, a, b, Z0 + 0.02, Z0 + 0.12, 'siva_krem')
    silme(y, dikdortgen(x0, x1, y0, y1), Z0 + 0.02, 0.016, 0.003, 'kerpic')
    saz_cati(y, x0, x1, y0, y1, Z0 + 0.12, 0.11, sacak=0.025, nr=6, kalin=0.014, besik=True)
for (x, yy) in ((1.08, 0.3), (0.95, 0.55), (1.08, 0.8), (0.95, 1.02), (1.05, -1.0)):
    sogut(y, x, yy, Z0, 0.3, tohum=int(x * 30 + yy * 90))
for (x, yy) in ((-0.78, 0.3), (-0.78, 0.98), (0.47, 0.95), (0.47, 0.25)):
    agac(y, x, yy, Z0, 0.24, 'yapraklı', 'boya_yesil')

y.bolum('Meydan sancakları')
for sx in (-1, 1):
    sancak(y, PC.x + sx * 0.2, -1.02, Z0, boy=0.32, en=0.1, yuk=0.06, aci=-math.pi / 2 - sx * 0.4, direk_key='ahsap_koyu')

calistir(y, 'lm_tlatelolco')
