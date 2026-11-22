# Alhambra (lm_elhamra): the Nasrid palace-fortress on the Sabika hill above Granada. A rocky hill ringed by red
# rammed-earth walls with pointed merlons and square towers; the Alcazaba at the west tip (Torre de la Vela with its
# bell gable and banner, the keep, the parade ground's house ruins); the Comares Tower over the Court of the Myrtles
# (long pool, myrtle hedges, arcaded porticoes); the Court of the Lions (slender columns, round arches, two projecting
# pavilions, the twelve-lion fountain and its four channels, the Two Sisters and Abencerrajes halls); the Partal
# portico and pool with the Ladies' Tower; a garden with a water channel and jets; the Gate of Justice up a stair.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from arap_ortak import *

y = Yapi()

ZT = 0.16                                   # the hill's top
DUV = 'kirmizi_tas'                         # red rammed-earth walls
TRIM = 'siva_oker'
BEYAZ = ('siva', 'siva_krem', 'mermer', 'koyu')
KIRMIZI = (DUV, 'tugla_koyu', TRIM, 'koyu')
TP = [V(-1.12, -0.55), V(-0.95, -0.82), V(0.62, -0.82), V(1.12, -0.6), V(1.12, 0.6), V(0.85, 0.85), V(-0.95, 0.85), V(-1.12, 0.55)]
WP = disa(TP, -0.03)                         # the outer wall's line
WH = 0.17                                   # wall height above the hill top

# ---------------- the hill ----------------
y.bolum('Sabika tepesi')
rng = y.rng
# the top outline cut into short steps, each point with its outward (mitred) normal
TPS = []
for i in range(len(TP)):
    a, b = TP[i], TP[(i + 1) % len(TP)]
    m = max(1, int(round((b - a).length / 0.11)))
    TPS += [a.lerp(b, k / m) for k in range(m)]
NRM = [(q - p) / 0.001 for p, q in zip(TPS, disa(TPS, 0.001))]
# rocky slopes: rings out and down, each point jittered (a broken, natural edge); steep crags near the top
HALKA = [(0.13, 0.0, 'kaya_koyu'), (0.103, 0.035, 'kaya_koyu'), (0.07, 0.075, 'kaya'), (0.04, 0.115, 'kaya'), (0.014, ZT - 0.012, 'toprak_ot'), (0.0, ZT, None)]
rings = []
for k, (off, zz, key) in enumerate(HALKA):
    j = 0.0 if k in (0, len(HALKA) - 1) else 0.02
    rings.append([V(p.x, p.y, zz) + n * (off + j * (rng.random() - 0.5)) + Z * (0.012 * (rng.random() - 0.5) if 0 < k < len(HALKA) - 1 else 0) for p, n in zip(TPS, NRM)])
for k in range(len(HALKA) - 1):
    y.serit(rings[k], rings[k + 1], HALKA[k][2])
y.yuz_yon([V(p.x, p.y, ZT) for p in TP], 'cimen_kuru', Z)
# crags and scrub on the slopes
for i in range(len(TPS)):
    if rng.random() < 0.45:
        k = rng.choice((1, 2))
        p = rings[k][i].lerp(rings[k + 1][i], 0.5)
        n = NRM[i]
        kutu_merkez(y, (p.x, p.y), 0.04 + 0.04 * rng.random(), 0.035, 0.03 + 0.025 * rng.random(), 'kaya_koyu', z0=p.z - 0.025,
                    aci=math.atan2(n.y, n.x) + math.pi / 2 + 0.4 * (rng.random() - 0.5))
    if rng.random() < 0.5:
        k = rng.choice((0, 1, 2))
        p = rings[k][i].lerp(rings[k + 1][i], 0.6)
        kure(y, (p.x, p.y, p.z + 0.008), 0.016 + 0.01 * rng.random(), 'yesil_koyu' if rng.random() < 0.6 else 'zeytin', n=8, kat=4)

# ---------------- the outer walls ----------------
y.bolum('Kızıl surlar')
sur(y, WP, ZT - 0.02, WH + 0.02, kalinlik=0.045, key=DUV, kapali=True, mazgal_h=0, parapet_h=0.0001, ust_key='toprak')
for i in range(len(WP)):
    sivri_mazgal(y, WP[i], WP[(i + 1) % len(WP)], ZT + WH + 0.0001, 0.024, 0.016, DUV)
silme(y, WP, ZT + WH - 0.012, 0.01, 0.006, TRIM, 'duz')


def burc(cx, cy, w, d, z0, h, pencere=(0, 1, 2, 3), n_p=2, zp=(0.6, 0.78), cati=None, cati_h=None, key=DUV, renk=KIRMIZI,
         sutuncuk=None, cini=False, en=0.4):
    """a Nasrid square tower: plinth, a band of arched windows high up (ajimez with sutuncuk), a light string course,
    a tile frieze (cini), a parapet with pointed merlons and a flat top, or a pyramid roof (cati='piramit')"""
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2)
    zt = z0 + h
    z_a, z_b = z0 + h * zp[0], z0 + h * zp[1]
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        if i in pencere:
            kat_pencere(y, a, b, z0, zt, z_a, z_b, n_p, renk, en=en, cerceve=(0.004, TRIM), sutuncuk=sutuncuk, derin=0.014)
        else:
            duvar_bant(y, a, b, z0, zt, key, n=3)
        if cini:
            cini_bant(y, a, b, z_b + 0.012, 0.014)
    silme(y, k, z0, 0.03, 0.008, key, 'kaide')
    silme(y, k, z_a - 0.012, 0.008, 0.005, TRIM, 'duz')
    if cati == 'piramit':
        silme(y, k, zt - 0.012, 0.012, 0.01, TRIM, 'tac')
        return cati_kirma(y, k[0].x, k[1].x, k[0].y, k[2].y, zt, cati_h or w * 0.55, 0.025, 'kiremit', 'kiremit2', dilim=['kiremit', 'kiremit2'], ns=6, nr=5)
    konsol_halka(y, k, zt - 0.024, 0.024, 0.01, TRIM, 2)
    k2 = disa(k, 0.01)
    mazgalli_kenar(y, k2, zt, key, kal=0.016, h=0.026, ust_key=TRIM)
    y.yuz_yon([V(p.x, p.y, zt) for p in disa(k2, -0.016)], 'zemin', Z)
    return zt + 0.04


# wall towers (straddling the wall line)
for (cx, cy, w, d, h) in ((0.35, -0.8, 0.12, 0.11, 0.27), (0.9, -0.68, 0.13, 0.13, 0.3), (1.1, -0.15, 0.12, 0.12, 0.28),
                          (1.1, 0.4, 0.12, 0.12, 0.3), (0.98, 0.72, 0.13, 0.13, 0.32), (0.28, 0.83, 0.11, 0.11, 0.26),
                          (-0.66, 0.83, 0.12, 0.11, 0.26)):
    burc(cx, cy, w, d, ZT - 0.05, h + 0.05, n_p=1, zp=(0.62, 0.8))

# ---------------- the Gate of Justice ----------------
y.bolum('Adalet Kapısı')
GX = -0.2
gk = dikdortgen(GX - 0.09, GX + 0.09, -0.9, -0.74)
GH = 0.28
nal_kemerli(y, gk[0], gk[1], ZT - 0.03, GH * 0.82, (DUV, 'tugla_koyu', TRIM, 'ahsap'), en=0.42, ust=0.04, derin=0.03, alfa=0.45,
            alfiz=(0.008, TRIM), tas=[TRIM, 'tugla_koyu'])
ZW = ZT - 0.03 + GH * 0.82            # (the upper window's foot: the wall face round it is split, no faces overlap)
duvar_bant(y, gk[0], gk[1], ZW + 0.05, ZT - 0.03 + GH, DUV, n=1)
duz_duvar(y, gk[0], V(GX - 0.05, -0.9), ZW, ZW + 0.05, DUV)
duz_duvar(y, V(GX + 0.05, -0.9), gk[1], ZW, ZW + 0.05, DUV)
for i in (1, 2, 3):
    duvar_bant(y, gk[i], gk[(i + 1) % 4], ZT - 0.05, ZT - 0.03 + GH, DUV, n=3)
duz_duvar(y, gk[0] + Z * 0, gk[1], ZT - 0.05, ZT - 0.03, DUV)
# the upper window pair and the key / hand carvings over the arch
y.kemerli(V(GX - 0.05, -0.9), V(GX + 0.05, -0.9), ZW, 0.05, KIRMIZI, v0=0.005, en=0.5, ust=0.008, derin=0.01, k_say=6)
yildiz(y, (GX, -0.9, ZT - 0.03 + GH * 0.62), X, -Y, 0.011, 'altin', k=8, ic=0.55)
konsol_halka(y, gk, ZT - 0.03 + GH - 0.02, 0.02, 0.008, TRIM, 2)
mazgalli_kenar(y, disa(gk, 0.008), ZT - 0.03 + GH, DUV, kal=0.016, h=0.026, ust_key=TRIM)
y.yuz_yon([V(p.x, p.y, ZT - 0.03 + GH) for p in disa(gk, -0.008)], 'zemin', Z)
# the stair up the hill to the gate, its cheeks
merdiven(y, (GX, -1.03), math.pi / 2, 0.1, 0.0, ZT - 0.03, n=9, d=0.0145, key='kaya', yanlik=DUV)
y.yuz_yon([V(GX - 0.05, -0.9, ZT - 0.03), V(GX + 0.05, -0.9, ZT - 0.03), V(GX + 0.05, -1.03 + 9 * 0.0145, ZT - 0.03), V(GX - 0.05, -1.03 + 9 * 0.0145, ZT - 0.03)], 'zemin', Z)

# ---------------- the Alcazaba ----------------
y.bolum('Alcazaba: Vela kulesi, iç kale')
AX = -0.5
sur(y, [V(AX, -0.78), V(AX, 0.26), V(-1.07, 0.26)], ZT, 0.15, kalinlik=0.04, key=DUV, mazgal_h=0, parapet_h=0.0001, ust_key='toprak')
sivri_mazgal(y, V(AX, -0.78), V(AX, 0.26), ZT + 0.1501, 0.024, 0.016, DUV)
sivri_mazgal(y, V(AX, 0.26), V(-1.07, 0.26), ZT + 0.1501, 0.024, 0.016, DUV)
# the parade ground: the ruined houses' wall stumps and a cistern
y.yuz_yon([V(-1.02, -0.5, ZT + 0.002), V(AX - 0.05, -0.5, ZT + 0.002), V(AX - 0.05, 0.2, ZT + 0.002), V(-1.02, 0.2, ZT + 0.002)], 'toprak', Z)
for (x0, x1, y0, y1) in ((-0.95, -0.82, -0.42, -0.28), (-0.8, -0.66, -0.42, -0.3), (-0.95, -0.85, -0.22, -0.06), (-0.83, -0.62, -0.22, -0.08),
                         (-0.95, -0.8, 0.0, 0.14), (-0.76, -0.6, 0.02, 0.16)):
    for i, (a, b) in enumerate(zip(dikdortgen(x0, x1, y0, y1), dikdortgen(x0, x1, y0, y1)[1:] + dikdortgen(x0, x1, y0, y1)[:1])):
        if i == 0 and (x1 - x0) > 0.12: continue      # (a doorway)
        e = (b - a).normalized()
        kutu(y, a + Z * (ZT + 0.002), e, (b - a).length, 0.01, 0.018 + 0.012 * ((i + int(x0 * 10)) % 2), 'kirmizi_tas', 'onarkasagsolust')
havuz(y, -0.66, -0.56, -0.48, -0.4, ZT + 0.006, derin=0.005, kenar=0.012, key=DUV)
# Torre de la Vela: the tall watch tower with its bell gable and the banner
VX, VY = -0.82, -0.66
tv = burc(VX, VY, 0.2, 0.19, ZT - 0.06, 0.62, n_p=2, zp=(0.7, 0.86), sutuncuk='mermer')
# a lower window row
for i, (a, b) in enumerate(zip(dikdortgen(VX - 0.1, VX + 0.1, VY - 0.095, VY + 0.095), dikdortgen(VX - 0.1, VX + 0.1, VY - 0.095, VY + 0.095)[1:] + dikdortgen(VX - 0.1, VX + 0.1, VY - 0.095, VY + 0.095)[:1])):
    e = (b - a).normalized(); nn = V(e.y, -e.x); m = (a + b) / 2
    yarik(y, m + nn * 0.001, e, nn, -0.006, ZT + 0.16, 0.012, 0.04, 'koyu')
    yarik(y, m + nn * 0.001, e, nn, -0.006, ZT + 0.28, 0.012, 0.04, 'koyu')
    yarik(y, m + nn * 0.001, e, nn, -0.006, ZT + 0.4, 0.012, 0.04, 'koyu')
zv = ZT - 0.06 + 0.62
# the bell gable (espadaña): a small wall with an arched opening and the bell
eg = (VX + 0.03, VY + 0.04)
y.kemerli(V(eg[0] - 0.035, eg[1]), V(eg[0] + 0.035, eg[1]), zv, 0.075, (TRIM, 'tugla_koyu', TRIM, 'koyu'), en=0.5, ust=0.012, derin=0.004, k_say=6)
y.kemerli(V(eg[0] + 0.035, eg[1] + 0.016), V(eg[0] - 0.035, eg[1] + 0.016), zv, 0.075, (TRIM, 'tugla_koyu', TRIM, 'koyu'), en=0.5, ust=0.012, derin=0.004, k_say=6)
kutu(y, V(eg[0] - 0.035, eg[1], zv), X, 0.07, 0.016, 0.075, TRIM, 'sagsolust')
y.koni((eg[0], eg[1] + 0.008), 0.012, zv + 0.075, 0.02, 'kiremit', n=6)
donel(y, (eg[0], eg[1] + 0.008), [(0.0, zv + 0.03), (0.011, zv + 0.03), (0.009, zv + 0.04), (0.005, zv + 0.052), (0.0, zv + 0.054)], 'bronz', n=10)
sancak(y, VX - 0.05, VY - 0.04, zv, boy=0.2, en=0.12, yuk=0.075, aci=0.3)
# the keep and the broken tower
burc(-0.98, 0.17, 0.15, 0.15, ZT - 0.05, 0.4, n_p=1, zp=(0.66, 0.8))
burc(AX, 0.2, 0.12, 0.12, ZT - 0.02, 0.29, n_p=1, zp=(0.6, 0.78))
burc(AX, -0.3, 0.1, 0.1, ZT - 0.02, 0.24, n_p=1, zp=(0.6, 0.78), pencere=(1,))
burc(-1.1, -0.18, 0.11, 0.11, ZT - 0.05, 0.27, n_p=1, zp=(0.6, 0.78))

# ---------------- the Court of the Myrtles and the Comares Tower ----------------
y.bolum('Mersinli Avlu')
MC = (-0.32, 0.0, -0.4, 0.36)                  # the court
MD = (-0.46, 0.14, -0.5, 0.44)                 # the wings' outer walls
MZI, MZR, MZD = ZT + 0.25, ZT + 0.33, ZT + 0.27
mk = dikdortgen(*MC)
y.yuz_yon([V(p.x, p.y, ZT + 0.002) for p in mk], 'mermer', Z)
# the long pool, the myrtle hedges
havuz(y, -0.205, -0.115, -0.33, 0.29, ZT + 0.006, derin=0.005, kenar=0.012, key='mermer')
for sx in (-1, 1):
    xh = -0.16 + sx * 0.075
    for k in range(4):
        ya, yb = -0.33 + k * 0.155, -0.33 + k * 0.155 + 0.14
        kutu_merkez(y, (xh, (ya + yb) / 2), 0.03, yb - ya, 0.035, 'yesil_koyu', z0=ZT + 0.002)
for yy in (-0.345, 0.305):           # round basins at the pool's ends
    y.prizma((-0.16, yy), 0.022, ZT + 0.002, ZT + 0.012, 'mermer', n=12)
    y.prizma((-0.16, yy), 0.016, ZT + 0.012, ZT + 0.0125, 'su', n=12)
# north portico (the Sala de la Barca's gallery) and south portico with an upper gallery
# (side 0 south, 1 east, 2 north, 3 west)
avlu_revak(y, MC, ZT, 0.14, [7, 0, 7, 0], BEYAZ, en=0.74, ust=0.03, derin=0.06, sutun_r=0.0065, atla=(1, 3), cerceve=(0.004, 'mermer'))
avlu_revak(y, MC, ZT + 0.14, MZI - 0.01 - ZT - 0.14, [7, 0, 7, 0], BEYAZ, en=0.6, ust=0.02, derin=0.04, sutun_r=0.005, atla=(1, 3),
           korkuluk=0.03, sutunlu=False)
for i in (0, 2):
    a, b = mk[(i + 1) % 4], mk[i]
    cini_bant(y, a, b, ZT + 0.14 - 0.004, 0.008, ('turkuaz', 'lacivert', 'altin', 'lacivert'))
# east and west sides: doors with tile dados below, latticed windows above
for i in (1, 3):
    a, b = mk[(i + 1) % 4], mk[i]
    L = (b - a).length; n = 5
    for j in range(n):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        if j % 2 == 0:
            dikdortgen_acik(y, p, q, ZT, 0.13, 0.32, 0.68, 0.0, 0.1, ('siva', 'siva_krem', 'mermer', 'ahsap'), derin=0.012, cerceve=(0.005, 'mermer'))
        else:
            dikdortgen_acik(y, p, q, ZT, 0.13, 0.25, 0.75, 0.045, 0.1, ('siva', 'siva_krem', 'mermer', 'koyu'), derin=0.012, cerceve=(0.005, 'mermer'))
            kafes(y, p, q, ZT, 0.25, 0.75, 0.045, 0.1, 'ahsap_koyu', 4, 3, 0.003, 0.004)
        dikdortgen_acik(y, p, q, ZT + 0.13, MZI - 0.01 - ZT - 0.13, 0.3, 0.7, 0.02, 0.085, ('siva', 'siva_krem', 'mermer', 'koyu'), derin=0.01)
        kafes(y, p, q, ZT + 0.13, 0.3, 0.7, 0.02, 0.085, 'ahsap_koyu', 4, 4, 0.0025, 0.004)
    cini_bant(y, a, b, ZT, 0.03)
    silme(y, [a, b], ZT + 0.128, 0.006, 0.006, 'mermer', 'duz', kapali=False)
halka_cati(y, MC, MD, MZI, MZR, MZD, sacak=0.03, sacak_dis=0.02)
md = dikdortgen(*MD)
for i in range(4):
    a, b = md[i], md[(i + 1) % 4]
    if i == 2:   # (the Comares Tower stands in the middle: only the ends either side of it)
        for p, q in ((a, V(-0.16 + 0.22, a.y)), (V(-0.16 - 0.22, a.y), b)):
            duvar_bant(y, p, q, ZT, MZD - 0.01, 'siva', n=2)
        continue
    L = (b - a).length
    kat_pencere(y, a, b, ZT, MZD - 0.01, ZT + 0.14, ZT + 0.21, max(2, int(L / 0.12)), BEYAZ, en=0.36, derin=0.01, cerceve=(0.004, 'mermer'))
    duz_duvar(y, a, b, ZT - 0.0, ZT + 0.03, 'siva_krem')

y.bolum('Comares kulesi')
CX, CY, CW = -0.16, 0.65, 0.44
CH = 0.74
ck = dikdortgen(CX - CW / 2, CX + CW / 2, CY - CW / 2, CY + CW / 2)
for i in range(4):
    a, b = ck[i], ck[(i + 1) % 4]
    duvar_bant(y, a, b, ZT - 0.06, ZT + 0.3, DUV, n=3)
    kat_pencere(y, a, b, ZT + 0.3, ZT + 0.44, ZT + 0.33, ZT + 0.42, 3, KIRMIZI, en=0.3, cerceve=(0.004, TRIM), derin=0.014)
    kat_pencere(y, a, b, ZT + 0.44, ZT + CH, ZT + 0.5, ZT + 0.64, 3, KIRMIZI, en=0.46, cerceve=(0.005, TRIM), derin=0.018, sutuncuk='mermer')
    cini_bant(y, a, b, ZT + 0.665, 0.016)
    cini_bant(y, a, b, ZT + 0.484, 0.008, ('altin', 'lacivert'))
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for t in (1 / 3, 2 / 3):        # pilaster strips between the window bays
        p = a.lerp(b, t)
        kutu(y, p - e * 0.008 + nn * 0.008 + Z * (ZT + 0.3), e, 0.016, 0.008, CH - 0.3 - 0.03, DUV, 'onsagsolust')   # (proud of the wall: no coplanar faces)
silme(y, ck, ZT + 0.3, 0.012, 0.008, TRIM, 'duz')
silme(y, ck, ZT + 0.44, 0.01, 0.006, TRIM, 'duz')
konsol_halka(y, ck, ZT + CH - 0.03, 0.03, 0.014, TRIM, 3)
ck2 = disa(ck, 0.014)
mazgalli_kenar(y, ck2, ZT + CH, DUV, kal=0.02, h=0.03, ust_key=TRIM, w=0.026, g=0.017)
y.yuz_yon([V(p.x, p.y, ZT + CH) for p in disa(ck2, -0.02)], 'zemin', Z)
# a low lantern on the roof terrace
kutu_merkez(y, (CX, CY), 0.12, 0.12, 0.05, TRIM, z0=ZT + CH)
cati_kirma(y, CX - 0.06, CX + 0.06, CY - 0.06, CY + 0.06, ZT + CH + 0.05, 0.05, 0.015, 'kiremit_yesil', 'kiremit2', ns=4, nr=3)

# ---------------- the Court of the Lions ----------------
y.bolum('Aslanlı Avlu: revaklar')
LC = (0.3, 0.88, -0.19, 0.19)
LD = (0.19, 0.99, -0.31, 0.31)
LZI, LZR, LZD = ZT + 0.15, ZT + 0.21, ZT + 0.17      # (kept low: the court must show from the game's view)
lk = dikdortgen(*LC)
y.yuz_yon([V(p.x, p.y, ZT + 0.002) for p in lk], 'mermer', Z)
avlu_revak(y, LC, ZT, LZI - 0.01 - ZT, [9, 5, 9, 5], BEYAZ, en=0.8, ust=0.04, derin=0.065, sutun_r=0.0055, cerceve=(0.0035, 'mermer'))
for i in range(4):   # the carved stucco band over the arches and a tile dado inside
    a, b = lk[(i + 1) % 4], lk[i]
    cini_bant(y, a, b, LZI - 0.01 - 0.03, 0.012, ('siva_krem', 'beyaz'))
halka_cati(y, LC, LD, LZI, LZR, LZD, sacak=0.018, sacak_dis=0.02)
ld = dikdortgen(*LD)
for i in range(4):
    a, b = ld[i], ld[(i + 1) % 4]
    L = (b - a).length
    kat_pencere(y, a, b, ZT, LZD - 0.01, ZT + 0.1, ZT + 0.16, max(2, int(L / 0.12)), BEYAZ, en=0.34, derin=0.01, cerceve=(0.004, 'mermer'))

y.bolum('Aslanlı Avlu: köşkler, çeşme, su kanalları')
for sx in (-1, 1):   # the two pavilions projecting into the court at the short ends
    xb = LC[0] if sx < 0 else LC[1]
    xf = xb - sx * 0.11
    P0, P1 = -0.06, 0.06
    HP = LZI - 0.01 - ZT + 0.02
    k4 = [V(xf, P0), V(xf, P1)] if sx < 0 else [V(xf, P1), V(xf, P0)]
    # the three open sides: arched screens (see-through)
    if sx < 0:
        sides = [(V(xb, P0), V(xf, P0)), (V(xf, P0), V(xf, P1)), (V(xf, P1), V(xb, P1))]
    else:
        sides = [(V(xb, P1), V(xf, P1)), (V(xf, P1), V(xf, P0)), (V(xf, P0), V(xb, P0))]
    for (a, b) in sides:
        n = 3 if abs((b - a).length - 0.12) < 0.01 else 2
        kemer_dizisi(y, a, b, n, ZT + 0.002, HP, 0.012, ('siva', 'siva_krem', 'mermer', 'siva_krem'), en=0.72, ust=0.035, sivri=0.0, acik=True, taban=False)
    x_lo, x_hi = sorted((xb, xf))
    for (px, py) in ((xf, P0), (xf, P1)):    # clustered columns at the free corners
        for dx, dy in ((0.0, 0.0), (sx * 0.012, 0.0), (0.0, 0.012 if py < 0 else -0.012)):
            sutun(y, px + dx + sx * 0.008, py + dy + (0.008 if py < 0 else -0.008), ZT + 0.002, ZT + HP * 0.62, 0.0045, 'mermer', 'osmanli')
    y.yuz_yon([V(x_lo, P0, ZT + HP - 0.001), V(x_hi, P0, ZT + HP - 0.001), V(x_hi, P1, ZT + HP - 0.001), V(x_lo, P1, ZT + HP - 0.001)], 'ahsap', -Z)
    cini_bant(y, sides[1][0], sides[1][1], ZT + HP - 0.03, 0.012, ('turkuaz', 'altin'))
    # the pyramid roof of glazed tiles
    cati_kirma(y, x_lo, x_hi, P0, P1, ZT + HP, 0.1, 0.025, 'kiremit_yesil', 'kiremit2', ns=6, nr=5)
    kure(y, ((x_lo + x_hi) / 2, 0.0, ZT + HP + 0.11), 0.008, 'altin', n=8, kat=4)
    # its small basin
    y.prizma(((x_lo + x_hi) / 2, 0.0), 0.02, ZT + 0.002, ZT + 0.014, 'mermer', n=12)
    y.prizma(((x_lo + x_hi) / 2, 0.0), 0.015, ZT + 0.014, ZT + 0.0145, 'su', n=12)

# the fountain: twelve lions round a twelve-sided basin, the jet bowl above
FC = ((LC[0] + LC[1]) / 2, 0.0)
y.prizma(FC, 0.075, ZT + 0.002, ZT + 0.008, 'mermer', n=12)
y.prizma(FC, 0.07, ZT + 0.008, ZT + 0.0085, 'su', n=12)
for i in range(12):
    a = TAU * i / 12
    with parca(y, (FC[0] + 0.036 * math.cos(a), FC[1] + 0.036 * math.sin(a), ZT + 0.008), a):
        kutu_merkez(y, (0.0, 0.0), 0.02, 0.011, 0.012, 'mermer')
        kure(y, (0.012, 0.0, 0.016), 0.0075, 'kirec', n=8, kat=4)
        kure(y, (0.017, 0.0, 0.015), 0.0045, 'mermer', n=6, kat=3)
        for s in (-1, 1):
            cubuk(y, V(0.008, s * 0.004, 0.0), V(0.008, s * 0.004, 0.004), 0.004, 'mermer')
donel(y, FC, [(0.0, ZT + 0.02), (0.03, ZT + 0.02), (0.05, ZT + 0.03), (0.056, ZT + 0.038), (0.05, ZT + 0.038), (0.0, ZT + 0.039)], 'mermer', n=12)
y.prizma(FC, 0.048, ZT + 0.0385, ZT + 0.039, 'su', n=12)
y.prizma(FC, 0.008, ZT + 0.039, ZT + 0.06, 'mermer', n=8)
donel(y, FC, [(0.0, ZT + 0.058), (0.02, ZT + 0.062), (0.024, ZT + 0.068), (0.0, ZT + 0.069)], 'mermer', n=12)
donel(y, FC, [(0.0, ZT + 0.068), (0.004, ZT + 0.068), (0.002, ZT + 0.085), (0.0, ZT + 0.088)], 'su', n=6)
# the four channels: to the pavilions and the two halls
for (a, b) in ((V(FC[0] - 0.075, 0), V(LC[0] - 0.11 + 0.11 / 2 + 0.02, 0)), (V(FC[0] + 0.075, 0), V(LC[1] + 0.11 - 0.11 / 2 - 0.02, 0)),
               (V(FC[0], 0.075), V(FC[0], LC[3])), (V(FC[0], -0.075), V(FC[0], LC[2]))):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for s, key, w in ((0, 'mermer', 0.011), (1, 'su', 0.006)):
        z = ZT + 0.003 + s * 0.0006
        y.yuz_yon([a - nn * w + Z * z, b - nn * w + Z * z, b + nn * w + Z * z, a + nn * w + Z * z], key, Z)

y.bolum('İki Kız Kardeş ve Abencerrajes salonları')
# Two Sisters: a cubic hall rising over the north wing, a clerestory and a pyramid roof
TX0, TX1, TY0, TY1 = 0.5, 0.68, 0.2, 0.31
tk = dikdortgen(TX0, TX1, TY0, TY1)
for i in range(4):
    a, b = tk[i], tk[(i + 1) % 4]
    kat_pencere(y, a, b, ZT + 0.12, ZT + 0.33, ZT + 0.24, ZT + 0.3, 2, BEYAZ, en=0.42, derin=0.012, cerceve=(0.004, 'mermer'), sutuncuk='mermer')
    cini_bant(y, a, b, ZT + 0.305, 0.01)
silme(y, tk, ZT + 0.23, 0.008, 0.006, 'mermer', 'duz')
cati_kirma(y, TX0, TX1, TY0, TY1, ZT + 0.33, 0.1, 0.022, 'kiremit', 'kiremit2', dilim=['kiremit', 'kiremit2'], ns=6, nr=5)
# Abencerrajes: an octagonal lantern over the south wing with an eight-sided tiled roof
AC = (0.66, -0.245)
AR = 0.068
ao = cokgen(AC, AR, 8, math.pi / 8)
for i in range(8):
    a, b = ao[i], ao[(i + 1) % 8]
    kat_pencere(y, a, b, ZT + 0.12, ZT + 0.3, ZT + 0.22, ZT + 0.28, 1, BEYAZ, en=0.48, derin=0.01, cerceve=(0.004, 'mermer'))
halka_kornis(y, AC, AR, ZT + 0.3, 0.01, 0.012, 8, 'mermer', kat=math.pi / 8)
donel(y, AC, [(0.0, ZT + 0.31 - 0.0005), (AR + 0.015, ZT + 0.31), (AR * 0.7, ZT + 0.345), (0.0, ZT + 0.385)], 'kiremit', n=8, kat=math.pi / 8)
kure(y, (AC[0], AC[1], ZT + 0.39), 0.008, 'altin', n=8, kat=4)

# ---------------- the Partal ----------------
y.bolum('Partal: revak, havuz, Damas kulesi')
PX0, PX1 = 0.4, 0.82
havuz(y, PX0 + 0.03, PX1 - 0.03, 0.41, 0.55, ZT + 0.004, derin=0.005, kenar=0.014, key='mermer')
pk = dikdortgen(PX0, PX1, 0.6, 0.7)
y.yuz_yon([V(PX0, 0.56, ZT + 0.002), V(PX1, 0.56, ZT + 0.002), V(PX1, 0.6, ZT + 0.002), V(PX0, 0.6, ZT + 0.002)], 'mermer', Z)
for j in range(5):
    p, q = V(PX0, 0.6).lerp(V(PX1, 0.6), j / 5), V(PX0, 0.6).lerp(V(PX1, 0.6), (j + 1) / 5)
    y.kemerli(p, q, ZT, 0.17, BEYAZ, en=0.78 if j != 2 else 0.84, ust=0.035, derin=0.06, k_say=8, cerceve=(0.004, 'mermer'))
    sutun(y, p.x, 0.594, ZT, ZT + 0.17 - 0.035 - 0.78 * 0.084 / 2, 0.006, 'mermer', 'osmanli') if j > 0 else None
for i in (1, 2, 3):
    duvar_bant(y, pk[i], pk[(i + 1) % 4], ZT, ZT + 0.17, 'siva', n=2)
cini_bant(y, V(PX0, 0.6), V(PX1, 0.6), ZT + 0.14, 0.01, ('turkuaz', 'lacivert', 'altin', 'lacivert'))
cati_besik(y, PX0, PX1, 0.6, 0.7, ZT + 0.17, 0.06, 0.025, 'kiremit', 'kiremit2', ucluk_key='siva', dilim=['kiremit', 'kiremit2'], nr=4, ns=8)
# the Ladies' Tower behind: a mirador with windows on all sides and a pyramid roof (straddling the wall)
burc(0.61, 0.79, 0.2, 0.16, ZT - 0.05, 0.36, n_p=2, zp=(0.6, 0.85), cati='piramit', cati_h=0.1, renk=BEYAZ, key='siva_krem', sutuncuk='mermer', cini=True)

# ---------------- gardens ----------------
y.bolum('Bahçeler: su kanalı, fıskiyeler, serviler')
# the water-channel garden in front of the palaces (Generalife's Patio de la Acequia)
GY = -0.6
y.yuz_yon([V(0.18, GY - 0.15, ZT + 0.002), V(1.0, GY - 0.15, ZT + 0.002), V(1.0, GY + 0.15, ZT + 0.002), V(0.18, GY + 0.15, ZT + 0.002)], 'zemin', Z)
havuz(y, 0.24, 0.86, GY - 0.016, GY + 0.016, ZT + 0.006, derin=0.005, kenar=0.012, key='mermer')
for k in range(9):          # arching jets from both sides into the channel
    x = 0.27 + k * 0.07
    for s in (-1, 1):
        boru(y, [V(x, GY + s * 0.03, ZT + 0.018), V(x, GY + s * 0.02, ZT + 0.04), V(x, GY + s * 0.006, ZT + 0.03), V(x, GY, ZT + 0.008)], 0.0018, 'su', n=4)
for s in (-1, 1):           # flower beds and box hedges
    for k in range(4):
        xa = 0.24 + k * 0.16
        kutu_merkez(y, (xa + 0.07, GY + s * 0.075), 0.13, 0.07, 0.012, 'yesil_koyu', z0=ZT + 0.002)
        for m in range(5):
            kure(y, (xa + 0.02 + m * 0.025, GY + s * 0.075 + 0.012 * ((m % 2) * 2 - 1), ZT + 0.018), 0.008, 'boya_kirmizi' if (m + k) % 2 else 'boya_sari', n=6, kat=3)
# a garden pavilion at the channel's end
kemer_dizisi(y, V(0.96, GY - 0.08), V(0.96, GY + 0.08), 3, ZT + 0.002, 0.16, 0.06, BEYAZ, en=0.74, ust=0.035, taban=True, acik=True)
cati_besik(y, 0.9, 0.96, GY - 0.08, GY + 0.08, ZT + 0.162, 0.05, 0.02, 'kiremit', 'kiremit2', ucluk_key='siva', nr=4, ns=6)
# cypress rows
for x in (0.22, 0.3, 0.38, 0.46, 0.54, 0.62, 0.7, 0.78):
    agac(y, x, GY - 0.18, ZT, boy=0.2, tur='servi', key='yesil_koyu')
for (x, yy) in ((-0.42, -0.66), (-0.42, -0.58), (0.06, -0.66), (0.06, -0.58), (-0.06, 0.6), (0.14, 0.62), (0.14, 0.52), (-0.42, 0.55)):
    agac(y, x, yy, ZT, boy=0.22, tur='servi', key='yesil_koyu')
for (x, yy) in ((-0.3, -0.7), (-0.1, -0.62), (-0.32, -0.58), (0.98, -0.2), (0.98, 0.2), (0.3, 0.56), (0.3, 0.45), (0.92, 0.46), (-0.08, -0.72)):
    agac(y, x, yy, ZT, boy=0.12, tur='yaprakli', key='boya_yesil')
# the path from the gate to the palaces
y.yuz_yon([V(GX - 0.05, -0.74, ZT + 0.002), V(GX + 0.05, -0.74, ZT + 0.002), V(GX + 0.05, -0.5, ZT + 0.002), V(GX - 0.05, -0.5, ZT + 0.002)], 'zemin', Z)
# trees on the hill's slopes (the Alhambra woods)
for (x, yy, zz) in ((-1.18, 0.1, 0.075), (-1.17, 0.42, 0.075), (0.0, 0.95, 0.025), (0.5, 0.96, 0.015), (-0.5, 0.95, 0.025), (1.2, 0.0, 0.05),
                    (1.18, -0.4, 0.075), (0.93, 0.9, 0.06), (1.18, 0.42, 0.075)):
    agac(y, x, yy, zz, boy=0.16, tur='yaprakli', key='yesil_koyu')

calistir(y, 'lm_elhamra')
