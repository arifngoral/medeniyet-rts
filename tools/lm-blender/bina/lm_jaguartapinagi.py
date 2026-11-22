# Jaguar Tapınağı (lm_jaguartapinagi): the Cuauhcalli of Malinalco, house of the eagle and jaguar warriors: a round
# temple on a three-tier talud-tablero platform cut against the hillside, its door the open mouth of a feathered
# serpent (fangs, eyes, the forked tongue on the floor), a tall tiered conical thatch roof; crouching jaguars on the
# stair and the top, braziers, the gladiatorial stone (temalacatl), a huehuetl drum, a side shrine and the rocky hill.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from aztek_parca import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04                         # ground top
PC = V(0.0, 0.18)                 # platform centre
W0, D0, W1, D1, NT, PH = 1.2, 1.0, 0.78, 0.62, 3, 0.4
ZT = Z0 + PH                      # platform top
C = V(0.0, 0.2)                   # round temple centre
R = 0.22                          # its wall radius
ZW = ZT + 0.03                    # wall foot (on the stone ring)
ZH = ZW + 0.18                    # wall top


def prizma_duz(pts, z0, z1, key, ust=None):
    """a flat slab from a CCW outline (tongue, mats)"""
    duvarlar(y, [V(p[0], p[1]) for p in pts], z0, z1, key, ust=ust or key)


y.bolum('Zemin: yamaç ve meydan')
zemin(y, -1.15, 1.15, -1.12, 1.12, Z0, 'kaya_koyu', 'cimen_kuru', basamak=(), silmeli=False)
# the paved way up to the stair and the plaza before it
y.yuz_yon([V(-0.2, -1.12, Z0 + 0.002), V(0.2, -1.12, Z0 + 0.002), V(0.2, -0.6, Z0 + 0.002), V(-0.2, -0.6, Z0 + 0.002)], 'zemin', Z)
y.yuz_yon([V(-0.95, -0.78, Z0 + 0.001), V(0.95, -0.78, Z0 + 0.001), V(0.95, -0.3, Z0 + 0.001), V(-0.95, -0.3, Z0 + 0.001)], 'toprak', Z)

# ---------------- the stepped platform ----------------
y.bolum('Basamaklı teras (talud-tablero)')
basamakli_piramit(y, (PC.x, PC.y), W0, W1, NT, PH, 'kirec', talud=0.6, tablero_key='boya_kirmizi', merdiven=False, z0=Z0, d0=D0, d1=D1)
# white discs (chalchihuitl, precious jade) along every red tablero
th = PH / NT
for k in range(NT):
    t0, t1 = k / NT, (k + 1) / NT
    hw0, hd0 = (W0 + (W1 - W0) * t0) / 2, (D0 + (D1 - D0) * t0) / 2
    hw1 = (W0 + (W1 - W0) * t1) / 2
    ins = (hw0 - hw1) * 0.75
    tw, td = hw0 - ins * 0.85, hd0 - ins * 0.85
    zm, zb = Z0 + th * k + th * 0.6, Z0 + th * (k + 1)
    zc = (zm + th * 0.06 + zb - th * 0.08) / 2
    kose = dikdortgen(PC.x - tw, PC.x + tw, PC.y - td, PC.y + td)
    for i in range(4):
        a, b = kose[i], kose[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        m = int(L / 0.085)
        for j in range(m):
            p = a.lerp(b, (j + 0.5) / m)
            if i == 0 and abs(p.x - PC.x) < 0.2: continue      # (behind the stair)
            y.oculus(p + nn * 0.0005 + Z * zc, e, nn, th * 0.075, 'beyaz', 'siva', f=0.004, k=10)

y.bolum('Merdiven ve korkuluklar')
YB, YS = -0.62, PC.y - D1 / 2
ayak = alfarda_merdiven(y, PC.x, YB, YS, Z0, ZT, 0.26, n=16, key='kirec', alfarda_key='siva', alfarda_en=0.045, dado=0.14, dado_h=0.06)
# red bands on the balustrades' dados
for sx in (-1, 1):
    x0 = PC.x + sx * (0.13 + 0.0225)
    kutu_merkez(y, (x0, YS - 0.035), 0.049, 0.004, 0.02, 'boya_kirmizi', z0=ZT + 0.025)
    y.oculus(V(x0, YS - 0.0375 - 0.0005, ZT + 0.035), X, -Y, 0.007, 'beyaz', 'boya_kirmizi', f=0.003, k=8)

# ---------------- the round temple (Cuauhcalli) ----------------
y.bolum('Yuvarlak tapınak duvarı')
NW = 32
ring = cokgen((C.x, C.y), R, NW, kat=-math.pi / 2)
# the stone ring it stands on
y.prizma((C.x, C.y), R + 0.03, ZT, ZW, 'kaya', n=NW, kat=-math.pi / 2)
for i in range(NW):
    a, b = ring[i], ring[(i + 1) % NW]
    ang = math.degrees(math.atan2((a.y + b.y) / 2 - C.y, (a.x + b.x) / 2 - C.x))
    if abs(ang + 90) < 34: continue        # the portal stands there
    duz_duvar(y, a, b, ZW, ZH, 'siva')
# painted bands: a red dado, a red frieze with white discs, a turquoise band under the eaves
silme(y, ring, ZW, 0.035, 0.004, 'boya_kirmizi')
silme(y, ring, ZH - 0.06, 0.03, 0.003, 'boya_kirmizi')
silme(y, ring, ZH - 0.022, 0.016, 0.005, 'turkuaz')
for i in range(NW):
    a, b = ring[i], ring[(i + 1) % NW]
    m_ = (a + b) / 2
    ang = math.degrees(math.atan2(m_.y - C.y, m_.x - C.x))
    if abs(ang + 90) < 40: continue
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    y.oculus(m_ + nn * 0.0035 + Z * (ZH - 0.045), e, nn, 0.009, 'beyaz', 'boya_kirmizi', f=0.002, k=8)

y.bolum('Yılan ağızlı kapı')
PWh = R * math.sin(math.radians(33.75))           # the portal's half width (meets the wall's cut ends)
YF = C.y - R - 0.05                               # its front
YBk = C.y - R * math.cos(math.radians(33.75))
PHt = 0.19
dikdortgen_acik(y, V(-PWh, YF), V(PWh, YF), ZT, PHt, 0.3, 0.7, 0.03, 0.15, ('siva', 'boya_kirmizi', 'boya_kirmizi', 'koyu'), derin=0.05)
duz_duvar(y, V(PWh, YF), V(PWh, YBk), ZT, ZT + PHt, 'siva')
duz_duvar(y, V(-PWh, YBk), V(-PWh, YF), ZT, ZT + PHt, 'siva')
y.yuz_yon([V(-PWh, YF, ZT + PHt), V(PWh, YF, ZT + PHt), V(PWh, YBk, ZT + PHt), V(-PWh, YBk, ZT + PHt)], 'siva', Z)
silme(y, [V(PWh, YBk), V(PWh, YF), V(-PWh, YF), V(-PWh, YBk)], ZT + PHt - 0.012, 0.012, 0.005, 'turkuaz', kapali=False)
# the serpent's head round the door: a turquoise mask with a red mouth (the reveal), white fangs, eyes, a feather crest
K = 0.012
o = V(0, YF - K + 0.001, ZT)
u0 = PWh * 2 * 0.2
hw_ = PWh * 0.92
levha(y, o, X, [(-hw_, 0), (-u0 - 0.004, 0), (-u0 - 0.004, 0.154), (u0 + 0.004, 0.154), (u0 + 0.004, 0), (hw_, 0), (hw_, 0.15),
                (hw_ - 0.02, 0.172), (hw_ - 0.05, 0.18), (-hw_ + 0.05, 0.18), (-hw_ + 0.02, 0.172), (-hw_, 0.15)], K, 'turkuaz', 'boya_yesil')
o2 = V(0, YF - K - 0.006 + 0.0005, ZT)
for s in (-1, 1):
    levha(y, o2, X, [(s * (u0 + 0.004), 0.154), (s * (u0 - 0.022), 0.154), (s * (u0 - 0.006), 0.098)], 0.006, 'beyaz')
    levha(y, o2, X, [(s * (u0 + 0.004), 0.03), (s * (u0 - 0.016), 0.03), (s * (u0 - 0.002), 0.07)], 0.006, 'beyaz')   # lower fangs
    for k in range(2):   # small teeth
        ux = s * (u0 - 0.032 - k * 0.016)
        levha(y, o2, X, [(ux - 0.006, 0.154), (ux + 0.006, 0.154), (ux, 0.138)], 0.006, 'beyaz')
    # eyes with a red brow, a scroll on the cheek
    pe = V(s * 0.072, YF - K, ZT + 0.162)
    y.oculus(pe, X, -Y, 0.014, 'beyaz', 'boya_kirmizi', f=0.004, k=12)
    y.oculus(pe - Y * 0.002, X, -Y, 0.006, 'koyu', 'koyu', f=0.001, k=8)
    levha(y, V(0, YF - K - 0.004 + 0.0005, ZT), X, [(s * 0.05, 0.176), (s * 0.095, 0.176), (s * 0.09, 0.184), (s * 0.055, 0.184)], 0.004, 'boya_kirmizi')
    y.oculus(V(s * 0.085, YF - K, ZT + 0.07), X, -Y, 0.016, 'boya_yesil', 'boya_kirmizi', f=0.004, k=12)
    y.oculus(V(s * 0.085, YF - K - 0.002, ZT + 0.07), X, -Y, 0.006, 'turkuaz', 'beyaz', f=0.002, k=8)
# feather crest over the head
for k in range(9):
    ux = -hw_ + 0.03 + (2 * hw_ - 0.06) * k / 8
    levha(y, V(0, YF - 0.006 + 0.001, ZT), X, [(ux - 0.011, 0.176), (ux + 0.011, 0.176), (ux + 0.006, 0.2), (ux, 0.21), (ux - 0.006, 0.2)], 0.006,
          'boya_yesil' if k % 2 else 'boya_kirmizi')
# the forked tongue spread on the floor down to the stair
tl = [(-0.03, YF), (0.03, YF), (0.022, YF - 0.05), (0.04, YS + 0.005), (0.012, YS + 0.02), (0.0, YF - 0.065), (-0.012, YS + 0.02), (-0.04, YS + 0.005), (-0.022, YF - 0.05)]
tl = [(p[0], p[1]) for p in tl]
prizma_duz(tl[::-1] if sum(tl[i][0] * tl[(i + 1) % len(tl)][1] - tl[(i + 1) % len(tl)][0] * tl[i][1] for i in range(len(tl))) < 0 else tl, ZT, ZT + 0.005, 'boya_kirmizi')

y.bolum('Kademeli konik saz çatı')
RH = 0.6
saz_konik(y, (C.x, C.y), R, ZH, RH, kat=5, sacak=0.11, kalin=0.026, n=48, yiv=0.07)
# rafter ends under the eaves
for i in range(24):
    t = TAU * (i + 0.5) / 24
    d = V(math.cos(t), math.sin(t))
    if d.y < -0.8: continue
    cubuk(y, V(C.x, C.y) + d * (R + 0.002) + Z * (ZH - 0.016), V(C.x, C.y) + d * (R + 0.075) + Z * (ZH - 0.022), 0.008, 'ahsap_koyu')
# the crowning: binding rings, a clay finial with a little flag of paper
zt = ZH + RH
for k, zz in enumerate((0.42, 0.62, 0.8)):
    rr = (R + 0.11) * (1 - zz) + 0.004
    y.prizma((C.x, C.y), rr, ZH + RH * zz - 0.006, ZH + RH * zz + 0.006, 'ahsap_koyu', n=20, ust=False)
donel(y, (C.x, C.y), [(0.0, zt + 0.015), (0.022, zt + 0.02), (0.03, zt + 0.045), (0.018, zt + 0.07), (0.024, zt + 0.08), (0.0, zt + 0.085)], 'siva_oker', n=12)
y.prizma((C.x, C.y), 0.031, zt + 0.038, zt + 0.048, 'boya_kirmizi', n=12, ust=False)
y.prizma((C.x, C.y), 0.004, zt + 0.08, zt + 0.16, 'ahsap', n=6)
iki_yuzlu(y, [V(C.x + 0.004, C.y, zt + 0.12), V(C.x + 0.05, C.y, zt + 0.13), V(C.x + 0.046, C.y, zt + 0.155), V(C.x + 0.004, C.y, zt + 0.158)], 'beyaz', -Y)

# ---------------- sculpture and fire on the top ----------------
y.bolum('Jaguar heykelleri')
for sx in (-1, 1):
    jaguar(y, PC.x + sx * 0.27, YS + 0.06, ZT, 0.16, -math.pi / 2 + sx * 0.12, tohum=3 + sx)
    jaguar(y, PC.x + sx * 0.235, YB - 0.04, Z0, 0.19, -math.pi / 2, tohum=7 + sx, taban_h=0.2)
for sx in (-1, 1):   # eagles on low pedestals at the front corners of the top (the house of the eagle and the jaguar)
    kutu_merkez(y, (PC.x + sx * 0.36, YS + 0.045), 0.07, 0.06, 0.035, 'kirec', z0=ZT)
    kutu_merkez(y, (PC.x + sx * 0.36, YS + 0.045), 0.074, 0.064, 0.008, 'boya_kirmizi', z0=ZT + 0.027)
    kartal(y, PC.x + sx * 0.36, YS + 0.045, ZT + 0.035, 0.13, -math.pi / 2, taban=None)
y.bolum('Mangallar')
for sx in (-1, 1):
    kutu_merkez(y, (sx * 0.32, C.y - 0.02), 0.05, 0.05, 0.012, 'kaya', z0=ZT)
    mangal(y, sx * 0.32, C.y - 0.02, ZT + 0.012, 0.09)

# ---------------- the plaza ----------------
y.bolum('Gladyatör taşı (temalacatl)')
GC = V(0.62, -0.56)
y.prizma((GC.x, GC.y), 0.17, Z0, Z0 + 0.025, 'siva', n=28)
halka_kornis(y, (GC.x, GC.y), 0.17, Z0 + 0.018, 0.007, 0.005, 28, 'boya_kirmizi')
y.prizma((GC.x, GC.y), 0.09, Z0 + 0.025, Z0 + 0.07, 'bazalt', n=28, ust=False)
halka_kornis(y, (GC.x, GC.y), 0.09, Z0 + 0.045, 0.01, 0.004, 28, 'kaya')
y.yuz_yon([V(p.x, p.y, Z0 + 0.07) for p in cokgen((GC.x, GC.y), 0.09, 28)], 'kaya', Z)
for k in range(16):   # sun rays carved on its face
    t = TAU * k / 16
    d = V(math.cos(t), math.sin(t)); sd = V(-d.y, d.x)
    p0, p1 = V(GC.x, GC.y) + d * 0.03, V(GC.x, GC.y) + d * 0.08
    y.yuz_yon([p0 + sd * 0.006 + Z * (Z0 + 0.0705), p1 + Z * (Z0 + 0.0705), p0 - sd * 0.006 + Z * (Z0 + 0.0705)], 'bazalt', Z)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0706) for p in cokgen((GC.x, GC.y), 0.018, 12)], 'koyu', Z)
boru(y, [V(GC.x + 0.01, GC.y, Z0 + 0.071), V(GC.x + 0.05, GC.y - 0.06, Z0 + 0.08), V(GC.x + 0.12, GC.y - 0.12, Z0 + 0.03), V(GC.x + 0.17, GC.y - 0.16, Z0 + 0.004)],
     0.004, 'saz_koyu', n=5)
for k in range(4):   # obsidian-edged clubs and round shields laid out for the fighters
    t = TAU * k / 4 + 0.4
    p = V(GC.x, GC.y) + V(math.cos(t), math.sin(t)) * 0.135
    donel(y, (p.x, p.y), [(0.0, Z0 + 0.025), (0.024, Z0 + 0.025), (0.024, Z0 + 0.03), (0.0, Z0 + 0.033)], 'boya_sari' if k % 2 else 'turkuaz', n=12)
    halka_kornis(y, (p.x, p.y), 0.024, Z0 + 0.025, 0.005, 0.003, 12, 'boya_kirmizi')

# an eagle warrior and a jaguar warrior squaring up by the stone
kartal_savasci(y, GC.x - 0.235, GC.y + 0.07, Z0, 0.17, -0.25, takim='kiremit', tuy='siva', taban=None)
kartal_savasci(y, GC.x + 0.03, GC.y + 0.25, Z0, 0.17, -math.pi / 2 - 0.2, takim='boya_sari', tuy='kiremit', taban=None)

y.bolum('Huehuetl davulu')
DC = V(0.78, -0.12)
donel(y, (DC.x, DC.y), [(0.042, Z0), (0.046, Z0 + 0.03), (0.038, Z0 + 0.04), (0.036, Z0 + 0.13), (0.04, Z0 + 0.14), (0.0, Z0 + 0.142)], 'ahsap', n=16)
y.prizma((DC.x, DC.y), 0.0385, Z0 + 0.06, Z0 + 0.075, 'boya_kirmizi', n=16, ust=False)
y.prizma((DC.x, DC.y), 0.0385, Z0 + 0.1, Z0 + 0.108, 'boya_sari', n=16, ust=False)
y.yuz_yon([V(p.x, p.y, Z0 + 0.1425) for p in cokgen((DC.x, DC.y), 0.034, 16)], 'siva_oker', Z)
for k in range(5):
    t = TAU * k / 5
    kure(y, (DC.x + 0.02 * math.cos(t), DC.y + 0.02 * math.sin(t), Z0 + 0.1425), 0.005, 'koyu', n=5, kat=3)
for k in range(3):   # the cut-out feet
    t = TAU * k / 3 + 0.5
    kutu_merkez(y, (DC.x + 0.04 * math.cos(t), DC.y + 0.04 * math.sin(t)), 0.012, 0.016, 0.03, 'koyu', z0=Z0, aci=t)
mangal(y, 0.6, -0.15, Z0, 0.1)

y.bolum('Yan tapınak')
SC = V(-0.68, -0.32)
kutu_merkez(y, (SC.x, SC.y), 0.36, 0.3, 0.07, 'siva', z0=Z0)
kornis(y, SC.x - 0.18, SC.x + 0.18, SC.y - 0.15, SC.y + 0.15, Z0 + 0.05, 0.02, 0.006, 'boya_kirmizi')
y.yuz_yon([V(p.x, p.y, Z0 + 0.0705) for p in dikdortgen(SC.x - 0.18, SC.x + 0.18, SC.y - 0.15, SC.y + 0.15)], 'zemin', Z)
alfarda_merdiven(y, SC.x, SC.y - 0.15 - 0.07, SC.y - 0.15, Z0, Z0 + 0.07, 0.11, n=4, key='kirec', alfarda_key='siva', alfarda_en=0.02, dado=0.0, dado_h=0.0)
zs0 = Z0 + 0.07
sx0, sx1, sy0, sy1 = SC.x - 0.12, SC.x + 0.12, SC.y - 0.08, SC.y + 0.1
dikdortgen_acik(y, V(sx0, sy0), V(sx1, sy0), zs0, 0.12, 0.36, 0.64, 0.0, 0.085, ('siva', 'boya_kirmizi', 'kirec', 'koyu'), derin=0.03)
duz_duvar(y, V(sx1, sy0), V(sx1, sy1), zs0, zs0 + 0.12, 'siva')
duz_duvar(y, V(sx1, sy1), V(sx0, sy1), zs0, zs0 + 0.12, 'siva')
duz_duvar(y, V(sx0, sy1), V(sx0, sy0), zs0, zs0 + 0.12, 'siva')
silme(y, dikdortgen(sx0, sx1, sy0, sy1), zs0, 0.025, 0.004, 'boya_kirmizi')
silme(y, dikdortgen(sx0, sx1, sy0, sy1), zs0 + 0.095, 0.016, 0.004, 'turkuaz')
saz_cati(y, sx0, sx1, sy0, sy1, zs0 + 0.12, 0.2, sacak=0.045, nr=7, kalin=0.018)
jaguar(y, SC.x + 0.1, SC.y - 0.235, Z0, 0.11, -math.pi / 2, tohum=21, taban_h=0.16)
jaguar(y, SC.x - 0.1, SC.y - 0.235, Z0, 0.11, -math.pi / 2, tohum=22, taban_h=0.16)

y.bolum('Kayalık tepe ve ağaçlar')
import random
rn = random.Random(5)


def kaya_yigini(cx, cy, rx, ry, h, adet):
    """a craggy outcrop: faceted boulders, the big ones in the middle, smaller ones round them"""
    for i in range(adet):
        t = rn.uniform(0, TAU); u = rn.uniform(0, 1) ** 0.7
        x, yy = cx + rx * u * math.cos(t), cy + ry * u * math.sin(t)
        s = (1 - 0.6 * u) * rn.uniform(0.7, 1.1)
        r = 0.09 * s + 0.03
        elipsoid(y, (x, yy, Z0), (r * rn.uniform(1.0, 1.5), r * rn.uniform(0.8, 1.2), h * s * rn.uniform(0.7, 1.1)),
                 rn.choice(('kaya', 'kaya_koyu', 'kaya')), n=7, kat=4, aci=rn.uniform(0, TAU), ust_yarim=True)


kaya_yigini(-0.88, 0.92, 0.26, 0.18, 0.2, 9)
kaya_yigini(0.86, 0.94, 0.28, 0.16, 0.22, 9)
kaya_yigini(-1.0, 0.5, 0.12, 0.2, 0.12, 5)
kaya_yigini(0.0, 1.03, 0.4, 0.06, 0.09, 7)
for (x, yy, b) in ((-0.62, 1.0, 0.12), (0.55, 0.98, 0.1), (-1.02, 0.72, 0.1), (1.02, 0.66, 0.11)):
    for k in range(3):
        kure(y, (x + 0.04 * math.cos(k * 2.1), yy + 0.03 * math.sin(k * 2.1), Z0 + b * 0.35), b * 0.42, 'yesil_koyu' if k % 2 else 'boya_yesil', n=8, kat=4)
for (x, yy, b, kk) in ((-0.95, -0.95, 0.24, 'boya_yesil'), (-0.6, 0.75, 0.3, 'yesil_koyu'), (0.62, 0.78, 0.28, 'boya_yesil'), (0.98, -0.85, 0.22, 'yesil_koyu'),
                       (-1.0, 0.25, 0.26, 'boya_yesil'), (1.0, 0.2, 0.24, 'yesil_koyu'), (-0.35, -0.95, 0.18, 'zeytin'), (0.35, -0.98, 0.18, 'zeytin')):
    agac(y, x, yy, Z0, b, 'yapraklı', kk)
for (x, yy, r) in ((-0.9, -0.55, 0.05), (0.92, -0.38, 0.045), (-0.3, 0.8, 0.06), (0.28, 0.82, 0.05), (-0.85, 0.05, 0.04)):
    elipsoid(y, (x, yy, Z0), (r, r * 0.8, r * 0.5), 'kaya', n=7, kat=4, aci=x * 3, ust_yarim=True)

y.bolum('Sancaklar')
for sx in (-1, 1):
    sancak(y, PC.x + sx * 0.33, PC.y + D1 / 2 - 0.06, ZT, boy=0.36, en=0.11, yuk=0.07, aci=-math.pi / 2 + sx * 0.5, direk_key='ahsap_koyu', kuyruk=True)
    sancak(y, sx * 0.24, -1.02, Z0, boy=0.3, en=0.09, yuk=0.06, aci=-math.pi / 2 - sx * 0.4, direk_key='ahsap_koyu')

calistir(y, 'lm_jaguartapinagi')
