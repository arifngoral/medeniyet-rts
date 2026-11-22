# Greek Fire Workshop (lm_rumatesi): the secret Byzantine naphtha works on the Golden Horn. A cross-in-square
# workshop hall in banded stone-and-brick walls with lead barrel vaults and a domed crossing, a banded guard tower
# with a lookout, a store wing; in the walled yard cauldrons on brick hearths, a bench of distilling alembics, racks
# and stacks of naphtha amphorae, a siphon test stand on the quay spitting fire over the water, and a moored dromon.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from bizans_ek import *

y = Yapi()
Z0 = 0.04            # quay / yard level
ZS = 0.014           # sea level
LY = -0.56           # the quay edge (land from here back)

# ---------------------------------------------------------------- ground, quay, sea
y.bolum('Zemin, rıhtım, deniz')
zemin(y, -1.1, 1.1, LY, 1.0, Z0, 'tas_koyu', basamak=(), silmeli=False)
silme(y, [V(1.1, LY), V(-1.1, LY)], Z0 - 0.012, 0.012, 0.008, 'kirec', 'duz', kapali=False)   # the quay's coping
# the sea basin: a breakwater rim round the water
SY0 = -1.08
for a, b in ((V(-1.1, SY0), V(1.1, SY0)), (V(1.1, SY0), V(1.1, LY)), (V(-1.1, LY), V(-1.1, SY0))):
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    L = (b - a).length
    kutu(y, a - nc * 0.0 + Z * 0, e, L, 0.035, ZS + 0.016, 'tas_koyu', 'onarkaust')
for p in (V(-1.1, SY0), V(1.1, SY0)):
    kutu_merkez(y, (p.x + (0.0175 if p.x < 0 else -0.0175), p.y + 0.0175), 0.035, 0.035, ZS + 0.02, 'kirec')
y.yuz_yon([V(-1.065, SY0 + 0.035, ZS), V(1.065, SY0 + 0.035, ZS), V(1.065, LY, ZS), V(-1.065, LY, ZS)], 'su', Z)
# steps down to the water and mooring bollards
for k in range(4):
    kutu(y, V(0.62, LY - 0.022 * (k + 1), 0), X, 0.14, 0.022 * (k + 1) + 0.001, Z0 * (4 - k) / 5, 'tas', 'onsagsolust')
for x in (-0.95, -0.5, -0.05, 0.4, 0.95):
    donel(y, (x, LY + 0.03), [(0.011, Z0), (0.011, Z0 + 0.016), (0.008, Z0 + 0.02), (0.013, Z0 + 0.026), (0.0, Z0 + 0.03)], 'demir', n=8)

# ---------------------------------------------------------------- the workshop hall (cross-in-square)
y.bolum('Atölye: çapraz planlı kubbeli salon')
HX0, HX1, HY0, HY1 = -0.82, -0.02, 0.12, 0.9
HC = ((HX0 + HX1) / 2, (HY0 + HY1) / 2)
H = 0.25
ZH = almasik_kutu(y, HX0, HX1, HY0, HY1, Z0, H, (5, 5, 5, 5), ust='kursun', kapilar=(2, None, None, None), en=0.38, v0=0.05,
                  sivri=0.0, kapi_en=0.55)
kornis(y, HX0, HX1, HY0, HY1, Z0, 0.028, 0.012, 'kirec', 'kaide')
for p in dikdortgen(HX0, HX1, HY0, HY1):   # corner piers
    kutu_merkez(y, (p.x, p.y), 0.045, 0.045, H + 0.008, 'kirec', z0=Z0)
AW = 0.17   # half width of the cross arms
ZV = tonoz(y, HX0, HX1, HC[1] - AW, HC[1] + AW, ZH, rise=0.12, eksen='x')
tonoz(y, HC[0] - AW, HC[0] + AW, HY0, HY1, ZH, rise=0.12, eksen='y')
# the square crossing block, the drum and the dome
zb = ZV + 0.008
kutu_merkez(y, HC, AW * 2 + 0.02, AW * 2 + 0.02, zb - ZH, 'tugla_roma', z0=ZH)
kornis(y, HC[0] - AW - 0.01, HC[0] + AW + 0.01, HC[1] - AW - 0.01, HC[1] + AW + 0.01, zb - 0.012, 0.014, 0.01, 'kirec', 'tac')
y.yuz_yon([V(p.x, p.y, zb + 0.002) for p in dikdortgen(HC[0] - AW - 0.01, HC[0] + AW + 0.01, HC[1] - AW - 0.01, HC[1] + AW + 0.01)], 'kursun', Z)
ZK = biz_kubbe(y, HC, 0.15, zb + 0.002, kasnak_h=0.07, n_pencere=12, kubbe_h=0.13)
# small domes over the corner bays
for sx in (-1, 1):
    for sy in (-1, 1):
        cx = HC[0] + sx * (AW + (HX1 - HX0) / 2) / 2
        cy = HC[1] + sy * (AW + (HY1 - HY0) / 2) / 2
        kucuk_kubbe(y, cx, cy, ZH, 0.055, kasnak=0.028, n=20, son=False, key='kursun', kasnak_key='tugla_roma')
        hac(y, cx, cy, ZH + 0.028 + 0.05, 0.03)
# the porch (exonarthex) before the door: three arches on columns, a flat roof with a cornice
PX0, PX1, PY0 = HC[0] - AW, HC[0] + AW, HY0 - 0.1
arkad(y, V(PX0, PY0), V(PX1, PY0), 3, Z0, 0.17, en=0.74, ust=0.025, sivri=0.0, derin=0.02, cerceve=(0.007, ['kirec', 'tugla_roma']),
      sutun_key='mermer', sutun_tur='korint', sutun_r=0.011)
duz_duvar(y, V(PX0, HY0), V(PX0, PY0), Z0, Z0 + 0.17, 'kirec')
duz_duvar(y, V(PX1, PY0), V(PX1, HY0), Z0, Z0 + 0.17, 'kirec')
kornis(y, PX0, PX1, PY0, HY0, Z0 + 0.158, 0.014, 0.01, 'kirec', 'tac')
y.yuz_yon([V(p.x, p.y, Z0 + 0.172) for p in dikdortgen(PX0, PX1, PY0, HY0)], 'kursun', Z)
y.yuz_yon([V(p.x, p.y, Z0 + 0.001) for p in dikdortgen(PX0, PX1, PY0 + 0.02, HY0)], 'mermer', Z)
# chimneys of the furnaces inside (brick, banded, smoke-blackened caps)
for cx, cy, h in ((HX0 + 0.08, HY1 - 0.08, 0.26), (HX1 - 0.08, HY1 - 0.08, 0.22)):
    donel(y, (cx, cy), [(0.03, ZH), (0.03, ZH + 0.02), (0.024, ZH + 0.03), (0.02, ZH + h)], 'tugla_roma', n=8, kat=math.pi / 8)
    for t in (0.4, 0.75):
        halka_kornis(y, (cx, cy), 0.024 - 0.004 * t, ZH + h * t, 0.008, 0.004, 8, 'kirec', kat=math.pi / 8)
    halka_kornis(y, (cx, cy), 0.02, ZH + h - 0.01, 0.012, 0.007, 8, 'kirec', kat=math.pi / 8, profil='tac')
    y.yuz_yon([V(p.x, p.y, ZH + h + 0.002) for p in cokgen((cx, cy), 0.026, 8, math.pi / 8)], 'koyu', Z)
    for k, (dz, r) in enumerate(((0.03, 0.018), (0.06, 0.024), (0.095, 0.028))):   # a thin smoke plume
        kure(y, (cx - 0.012 * k, cy + 0.01 * k, ZH + h + dz), r, 'granit' if k else 'granit_koyu', n=10, kat=5)

# ---------------------------------------------------------------- the store wing
y.bolum('Ambar kanadı')
SX0, SX1, SY0_, SY1 = -0.02, 0.4, 0.38, 0.9
ZA = almasik_kutu(y, SX0, SX1, SY0_, SY1, Z0, 0.17, (2, 0, 3, 0), ust=None, kapilar=(1, None, None, None), en=0.36, v0=0.04)
kiremit_cati(y, SX0, SX1, SY0_, SY1, ZA - 0.004, 0.1, sacak=0.02)

# ---------------------------------------------------------------- the guard tower
y.bolum('Muhafız kulesi')
TC = (0.6, 0.64)
TW = 0.32
tk = dikdortgen(TC[0] - TW / 2, TC[0] + TW / 2, TC[1] - TW / 2, TC[1] + TW / 2)
zz = Z0
kornis(y, tk[0].x, tk[1].x, tk[0].y, tk[2].y, Z0, 0.03, 0.014, 'kirec', 'kaide')
for kat, (h, n) in enumerate(((0.22, 1), (0.2, 2), (0.19, 2))):
    for i in range(4):
        kb = 0 if (kat == 0 and i == 0) else None
        almasik(y, tk[i], tk[(i + 1) % 4], zz, h, n, en=0.42 if n == 1 else 0.36, v0=0.0 if kb == 0 else 0.06, ust=0.03,
                kapi_bay=kb, k_say=8)
    zz += h
    silme(y, tk, zz - 0.012, 0.014, 0.01, 'kirec', 'tac' if kat == 2 else 'duz')
# machicolation, parapet, merlons, the roof deck
konsol_halka(y, tk, zz, 0.03, 0.016, 'kirec', 3)
ring = disa(tk, 0.016)
zz += 0.03
parapet(y, ring, zz, 0.016, 0.034, 0.018, 'tugla_roma', ust_key='kirec')
y.yuz_yon([V(p.x, p.y, zz + 0.0005) for p in disa(ring, -0.018)], 'zemin', Z)
# the lookout: a small banded pavilion with arched openings and a tile pyramid roof
LW = 0.15
lk = dikdortgen(TC[0] - LW / 2, TC[0] + LW / 2, TC[1] - LW / 2, TC[1] + LW / 2)
for i in range(4):
    y.kemerli(lk[i], lk[(i + 1) % 4], zz, 0.1, ('kirec', 'tas_koyu', 'mermer', 'koyu'), v0=0.02, en=0.5, ust=0.02, derin=0.015, k_say=8,
              cerceve=(0.006, ['tugla_roma', 'kirec']))
for p in lk:
    kutu_merkez(y, (p.x, p.y), 0.022, 0.022, 0.1, 'tugla_roma', z0=zz)
ZL = zz + 0.1
kornis(y, lk[0].x, lk[1].x, lk[0].y, lk[2].y, ZL - 0.008, 0.01, 0.008, 'kirec', 'tac')
ZT = cati_kirma(y, lk[0].x, lk[1].x, lk[0].y, lk[2].y, ZL + 0.002, 0.11, 0.025, 'kiremit', 'kiremit2', alt_key='ahsap_koyu', kalinlik=0.008,
                ns=6, nr=4)
hac(y, TC[0], TC[1], ZT, 0.04)
sancak(y, tk[1].x - 0.02, tk[1].y + 0.02, zz + 0.05, boy=0.24, en=0.13, yuk=0.08, aci=-math.pi * 0.25)
# a link wall between the tower and the store wing
almasik(y, V(SX1, 0.48), V(tk[0].x, 0.48), Z0, 0.15, 0)
kutu(y, V(SX1, 0.48, Z0 + 0.15), X, tk[0].x - SX1, 0.06, 0.012, 'kirec', 'onust')

# ---------------------------------------------------------------- the beehive kiln (left)
y.bolum('Fırın')
FC = (-0.96, 0.62)
donel(y, FC, [(0.11, Z0), (0.11, Z0 + 0.06), (0.1, Z0 + 0.1), (0.075, Z0 + 0.15), (0.04, Z0 + 0.18), (0.024, Z0 + 0.19)], 'tugla_roma', n=20)
halka_kornis(y, FC, 0.11, Z0 + 0.055, 0.01, 0.006, 20, 'kirec')
donel(y, FC, [(0.024, Z0 + 0.19), (0.022, Z0 + 0.23), (0.028, Z0 + 0.24), (0.0, Z0 + 0.24)], 'tugla_roma_koyu', n=8)
# the stoke hole facing the yard, glowing
a0 = -math.pi / 2 + 0.25
o = V(FC[0] + 0.111 * math.cos(a0), FC[1] + 0.111 * math.sin(a0))
e = V(-math.sin(a0), math.cos(a0)); nn = V(math.cos(a0), math.sin(a0))
y.pencere(o + Z * 0, e, nn, -0.025, Z0 + 0.006, 0.05, 0.05, 'altin', kemer=True, k_say=6)
y.pencere(o + nn * 0.001, e, nn, -0.017, Z0 + 0.006, 0.034, 0.032, 'boya_sari', kemer=True, k_say=6)
for k in range(5):   # firewood
    a = -0.8 + 0.06 * k
    cubuk(y, V(FC[0] + 0.06 + 0.012 * k, FC[1] - 0.17, Z0 + 0.006 + 0.008 * (k % 2)), V(FC[0] + 0.06 + 0.012 * k, FC[1] - 0.25, Z0 + 0.006 + 0.008 * (k % 2)),
          0.008, 'kutuk')

# ---------------------------------------------------------------- the yard wall and gate
y.bolum('Avlu duvarı ve kapı')
WY = -0.4
WH = 0.075


def avlu_duvar(a, b):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x); L = (b - a).length
    kutu(y, a + Z * Z0, e, L, 0.03, WH, 'kirec', 'onarka')
    serit_tas(y, a, b, Z0, 0, L, 0.03, 0.014, 'tugla_roma', 0.002)
    serit_tas(y, b - nc * 0.03, a - nc * 0.03, Z0, 0, L, 0.03, 0.014, 'tugla_roma', 0.002)
    kutu(y, a + nc * 0.006 + Z * (Z0 + WH), e, L, 0.042, 0.01, 'tugla_roma', 'onarkaust')
    n = max(1, int(L / 0.16))
    for k in range(n + 1):
        p = a.lerp(b, k / n) - nc * 0.015
        kutu_merkez(y, (p.x, p.y), 0.04, 0.045, WH + 0.025, 'kirec', z0=Z0)
        y.koni((p.x, p.y), 0.016, Z0 + WH + 0.025, 0.022, 'kiremit', n=8)


GX0, GX1 = -0.5, -0.3
avlu_duvar(V(-1.08, WY), V(GX0, WY))
avlu_duvar(V(GX1, WY), V(0.55, WY))
# the gate: two banded piers with an arch over the passage
for gx in (GX0 - 0.03, GX1 + 0.03):
    kutu_merkez(y, (gx, WY - 0.015), 0.06, 0.07, 0.17, 'kirec', z0=Z0)
    for zb_, hb in ((0.04, 0.014), (0.1, 0.014)):
        kutu_merkez(y, (gx, WY - 0.015), 0.064, 0.074, hb, 'tugla_roma', z0=Z0 + zb_)
    kornis(y, gx - 0.03, gx + 0.03, WY - 0.05, WY + 0.02, Z0 + 0.16, 0.012, 0.008, 'kirec', 'tac')
    hac(y, gx, WY - 0.015, Z0 + 0.172, 0.035)
gm = ((GX0 + GX1) / 2, WY - 0.015)
pts = [V(gm[0] - 0.1 * math.cos(math.pi * k / 10), gm[1], Z0 + 0.1 + 0.07 * math.sin(math.pi * k / 10)) for k in range(11)]
for d in (-0.02, 0.02):
    boru(y, [p + V(0, d, 0) for p in pts], 0.01, 'tugla_roma', n=6)
# iron gate leaves, half open
for s, ac in ((-1, 0.9), (1, -0.9)):
    hx = gm[0] + s * 0.1
    with parca(y, (hx, WY - 0.01, Z0), (math.pi if s > 0 else 0) + ac * (-s)):
        kutu(y, V(0, -0.004, 0), X, 0.095, 0.008, 0.12, 'ahsap_koyu')
        for zq in (0.02, 0.06, 0.1):
            kutu(y, V(0.002, -0.0055, zq), X, 0.09, 0.011, 0.006, 'demir')

# ---------------------------------------------------------------- the yard: cauldrons, alembics, amphorae
y.bolum('Kazanlar')
y.yuz_yon([V(-1.08, WY + 0.03, Z0 + 0.002), V(0.75, WY + 0.03, Z0 + 0.002), V(0.75, HY0 - 0.1, Z0 + 0.002), V(-1.08, HY0 - 0.1, Z0 + 0.002)],
          'toprak', Z)


def kazan(cx, cy, r=0.05):
    """a great bronze cauldron of boiling naphtha on a round brick hearth with a glowing fire mouth"""
    hh = 0.05
    y.prizma((cx, cy), r * 1.08, Z0, Z0 + hh, 'tugla_roma', n=12, ust=True)
    halka_kornis(y, (cx, cy), r * 1.08, Z0 + hh - 0.008, 0.01, 0.006, 12, 'kirec')
    for a in (-math.pi / 2, math.pi / 2 + 0.6):
        o = V(cx + r * 1.08 * math.cos(a), cy + r * 1.08 * math.sin(a))
        e = V(-math.sin(a), math.cos(a)); nn = V(math.cos(a), math.sin(a))
        y.pencere(o, e, nn, -0.016, Z0 + 0.004, 0.032, 0.03, 'altin', kemer=True, k_say=6)
        y.pencere(o + nn * 0.001, e, nn, -0.01, Z0 + 0.004, 0.02, 0.018, 'boya_sari', kemer=True, k_say=6)
    z = Z0 + hh
    donel(y, (cx, cy), [(0.0, z - 0.01), (r * 0.6, z - 0.008), (r * 0.95, z + 0.02), (r * 1.02, z + 0.045), (r * 1.06, z + 0.05), (r * 1.06, z + 0.056),
                        (r * 0.98, z + 0.056)], 'bronz', n=16)
    donel(y, (cx, cy), [(r * 0.98, z + 0.056), (r * 0.97, z + 0.045)], 'bronz', n=16)   # (the inner lip, down to the liquid)
    y.yuz_yon([V(p.x, p.y, z + 0.045) for p in cokgen((cx, cy), r * 0.97, 16)], 'koyu', Z)
    for i in range(3):   # bubbles of the boiling pitch
        a = 1.3 * i + 0.4
        kure(y, (cx + r * 0.45 * math.cos(a), cy + r * 0.45 * math.sin(a), z + 0.046), 0.006 - 0.001 * i, 'tas_koyu', n=6, kat=3)
    for s in (-1, 1):   # ring handles
        boru(y, [V(cx + s * r * 1.06, cy - 0.01, z + 0.048), V(cx + s * (r * 1.06 + 0.012), cy, z + 0.044), V(cx + s * r * 1.06, cy + 0.01, z + 0.048)],
             0.003, 'demir', n=4)


kazan(-0.86, -0.18, 0.055)
kazan(-0.66, -0.06, 0.05)
kazan(-0.86, 0.02, 0.045)
# a ladle stirring pole, a tripod hoist over the first cauldron
TP = V(-0.86, -0.18, Z0 + 0.25)
for a in (math.radians(90), math.radians(210), math.radians(330)):
    cubuk(y, V(-0.86 + 0.1 * math.cos(a), -0.18 + 0.1 * math.sin(a), Z0), TP, 0.008, 'ahsap')
cubuk(y, TP, V(-0.86, -0.18, Z0 + 0.16), 0.0025, 'demir')
kutu_merkez(y, (-0.86, -0.18), 0.012, 0.012, 0.03, 'ahsap_koyu', z0=Z0 + 0.13)

y.bolum('Damıtma imbikleri')
BX0, BX1, BY_ = -0.36, 0.34, 0.0
kutu(y, V(BX0, BY_ - 0.04, Z0), X, BX1 - BX0, 0.08, 0.05, 'tugla_roma')
kutu(y, V(BX0 - 0.005, BY_ - 0.045, Z0 + 0.05), X, BX1 - BX0 + 0.01, 0.09, 0.008, 'kirec')
for k in range(6):   # fire mouths along the bench
    x = BX0 + (BX1 - BX0) * (k + 0.5) / 6
    y.pencere(V(x, BY_ - 0.04), X, -Y, -0.012, Z0 + 0.006, 0.024, 0.026, 'altin', kemer=True, k_say=6)
    y.pencere(V(x, BY_ - 0.041), X, -Y, -0.007, Z0 + 0.006, 0.014, 0.016, 'boya_sari', kemer=True, k_say=6)
ZB = Z0 + 0.058
for k in range(6):
    x = BX0 + (BX1 - BX0) * (k + 0.5) / 6
    # the cucurbit (bronze still), its alembic head and the beak running forward to a glass receiver
    donel(y, (x, BY_), [(0.016, ZB), (0.026, ZB + 0.014), (0.026, ZB + 0.03), (0.016, ZB + 0.044), (0.009, ZB + 0.05), (0.009, ZB + 0.056)], 'bronz', n=12)
    donel(y, (x, BY_), [(0.009, ZB + 0.056), (0.016, ZB + 0.06), (0.017, ZB + 0.07), (0.01, ZB + 0.08), (0.0, ZB + 0.083)], 'bakir', n=12)
    tip = V(x + 0.012, BY_ - 0.07, Z0 + 0.04)
    boru(y, [V(x, BY_ - 0.012, ZB + 0.066), V(x + 0.006, BY_ - 0.045, ZB + 0.05), tip], 0.0028, 'bakir', n=5, r_son=0.0018)
    # the receiver on a little stool in front of the bench
    kutu_merkez(y, (tip.x, tip.y - 0.006), 0.026, 0.026, 0.018, 'ahsap', z0=Z0)
    donel(y, (tip.x, tip.y - 0.006), [(0.0, Z0 + 0.018), (0.012, Z0 + 0.022), (0.013, Z0 + 0.03), (0.008, Z0 + 0.038), (0.004, Z0 + 0.042), (0.004, Z0 + 0.046),
                                      (0.0, Z0 + 0.046)], 'cam', n=10)
# shelves of jars on the bench's back
for k in range(9):
    x = BX0 + 0.03 + (BX1 - BX0 - 0.06) * k / 8
    donel(y, (x, BY_ + 0.03), [(0.0, ZB), (0.008, ZB), (0.009, ZB + 0.012), (0.005, ZB + 0.02), (0.0, ZB + 0.02)], ('kiremit', 'kum', 'mermer')[k % 3], n=8)

y.bolum('Neft amforaları ve sundurma')
# an open timber shed with a tile lean-to roof on the right, racks of amphorae under it
RX0, RX1, RY0, RY1 = 0.76, 1.06, -0.3, 0.9
for x in (RX0, RX1):
    for k in range(6):
        yy = RY0 + (RY1 - RY0) * k / 5
        kutu_merkez(y, (x, yy), 0.018, 0.018, 0.26 if x == RX0 else 0.2, 'ahsap', z0=Z0)
        donel(y, (x, yy), [(0.016, Z0), (0.016, Z0 + 0.012), (0.0, Z0 + 0.012)], 'kirec', n=8)
for x, h in ((RX0, 0.26), (RX1, 0.2)):
    cubuk(y, V(x, RY0 - 0.01, Z0 + h - 0.006), V(x, RY1 + 0.01, Z0 + h - 0.006), 0.016, 'ahsap_koyu', 0.014)
# the lean-to: slopes down towards the yard (-x)
ra, rb = V(RX0 - 0.04, 0, Z0 + 0.26 + 0.008), V(RX1 + 0.03, 0, Z0 + 0.2 - 0.01)
nr = 4
for j in range(nr):
    pa, pb = ra.lerp(rb, j / nr), ra.lerp(rb, (j + 1) / nr)
    for i in range(6):
        y0_, y1_ = RY0 - 0.03 + (RY1 - RY0 + 0.06) * i / 6, RY0 - 0.03 + (RY1 - RY0 + 0.06) * (i + 1) / 6
        y.yuz_yon([V(pa.x, y0_, pa.z), V(pa.x, y1_, pa.z), V(pb.x, y1_, pb.z), V(pb.x, y0_, pb.z)], 'kiremit' if j % 2 == 0 else 'kiremit2', Z + X * 0.2)
        y.yuz_yon([V(pa.x, y0_, pa.z - 0.008), V(pa.x, y1_, pa.z - 0.008), V(pb.x, y1_, pb.z - 0.008), V(pb.x, y0_, pb.z - 0.008)], 'ahsap_koyu', -Z)
for yq in (RY0 - 0.03, RY1 + 0.03):
    s = -1 if yq < 0.3 else 1
    y.yuz_yon([ra + V(0, yq, 0), rb + V(0, yq, 0), rb + V(0, yq, -0.008), ra + V(0, yq, -0.008)], 'ahsap_koyu', V(0, s, 0))
y.yuz_yon([V(ra.x, RY0 - 0.03, ra.z), V(ra.x, RY1 + 0.03, ra.z), V(ra.x, RY1 + 0.03, ra.z - 0.008), V(ra.x, RY0 - 0.03, ra.z - 0.008)], 'ahsap_koyu', -X)
y.yuz_yon([V(rb.x, RY1 + 0.03, rb.z), V(rb.x, RY0 - 0.03, rb.z), V(rb.x, RY0 - 0.03, rb.z - 0.008), V(rb.x, RY1 + 0.03, rb.z - 0.008)], 'ahsap_koyu', X)
# the shed's plank back wall (seen from both sides)
for yq0, yq1 in ((RY0 - 0.01, RY1 + 0.01),):
    duz_duvar(y, V(RX1 + 0.01, yq0), V(RX1 + 0.01, yq1), Z0, Z0 + 0.19, 'ahsap_dikey')
    duz_duvar(y, V(RX1 + 0.002, yq1), V(RX1 + 0.002, yq0), Z0, Z0 + 0.19, 'ahsap_dikey')
    y.yuz_yon([V(RX1 + 0.002, yq0, Z0 + 0.19), V(RX1 + 0.01, yq0, Z0 + 0.19), V(RX1 + 0.01, yq1, Z0 + 0.19), V(RX1 + 0.002, yq1, Z0 + 0.19)], 'ahsap_dikey', Z)
    for yq, sg in ((yq0, -1), (yq1, 1)):
        y.yuz_yon([V(RX1 + 0.002, yq, Z0), V(RX1 + 0.01, yq, Z0), V(RX1 + 0.01, yq, Z0 + 0.19), V(RX1 + 0.002, yq, Z0 + 0.19)], 'ahsap_dikey', V(0, sg, 0))
    # outside: battens over the plank joints, two rails, a stone sill, and shuttered hatches for loading jars
    nb = 16
    for k in range(nb + 1):
        yy = yq0 + 0.004 + (yq1 - yq0 - 0.008) * k / nb
        kutu_merkez(y, (RX1 + 0.0115, yy), 0.006, 0.009, 0.19, 'ahsap_koyu', z0=Z0)
    for zq in (0.05, 0.14):
        kutu_merkez(y, (RX1 + 0.0135, (yq0 + yq1) / 2), 0.007, yq1 - yq0, 0.012, 'ahsap_koyu', z0=Z0 + zq)
    kutu_merkez(y, (RX1 + 0.012, (yq0 + yq1) / 2), 0.016, yq1 - yq0 + 0.01, 0.014, 'tas_koyu', z0=Z0)
    for k in range(4):
        yy = yq0 + (yq1 - yq0) * (k + 0.5) / 4
        kutu_merkez(y, (RX1 + 0.012, yy), 0.008, 0.09, 0.06, 'koyu', z0=Z0 + 0.068)
        for s in (-1, 1):   # the two shutters swung open against the wall
            kutu_merkez(y, (RX1 + 0.0175, yy + s * 0.068), 0.005, 0.044, 0.058, 'ahsap', z0=Z0 + 0.069)
            for zq in (0.08, 0.112):
                kutu_merkez(y, (RX1 + 0.0205, yy + s * 0.068), 0.002, 0.04, 0.005, 'demir', z0=Z0 + zq)
# racks: two tiers of amphorae lying with their toes to the back wall, mouths to the yard
for zr in (Z0 + 0.02, Z0 + 0.07):
    for xr in (RX1 - 0.032, RX1 - 0.075):
        cubuk(y, V(xr, RY0 + 0.02, zr - 0.006), V(xr, RY1 - 0.02, zr - 0.006), 0.008, 'ahsap_acik')
    for k in range(15):
        yy = RY0 + 0.05 + (RY1 - RY0 - 0.1) * k / 14
        amfora(y, RX1 - 0.018, yy, zr + 0.012, 1.0, aci_x=math.pi / 2, aci_z=-math.pi / 2, kulp=False, n=8)
for k in range(6):   # the rack's uprights
    yy = RY0 + 0.02 + (RY1 - RY0 - 0.04) * k / 5
    for xr in (RX1 - 0.032, RX1 - 0.075):
        cubuk(y, V(xr, yy, Z0), V(xr, yy, Z0 + 0.075), 0.008, 'ahsap_acik')
# amphorae standing in the yard: a pyramid of lying jars, upright ones in sand
for k in range(5):
    amfora(y, 0.48 + 0.03 * k, -0.33, Z0 + 0.014, 1.0, aci_x=math.pi / 2, aci_z=0.0, kulp=False, n=8)
for k in range(4):
    amfora(y, 0.495 + 0.03 * k, -0.33, Z0 + 0.04, 1.0, aci_x=math.pi / 2, aci_z=0.0, kulp=False, n=8)
for k in range(3):
    amfora(y, 0.51 + 0.03 * k, -0.33, Z0 + 0.066, 1.0, aci_x=math.pi / 2, aci_z=0.0, kulp=False, n=8)
for k, (x, yy) in enumerate(((0.36, -0.3), (0.39, -0.26), (0.34, -0.25), (0.42, -0.21), (0.37, -0.19), (0.62, -0.12), (0.66, -0.16), (0.68, -0.09))):
    amfora(y, x, yy, Z0 - 0.006, 1.05, aci_x=0.12 * (k % 3 - 1), aci_z=k)
# a handcart with amphorae
with parca(y, (0.15, -0.24, Z0), 0.3):
    kutu(y, V(-0.06, -0.035, 0.03), X, 0.12, 0.07, 0.012, 'ahsap')
    for s in (-1, 1):
        kutu(y, V(-0.06, s * 0.035 - (0.004 if s > 0 else 0), 0.042), X, 0.12, 0.004, 0.02, 'ahsap_acik')
        boru(y, [V(0, s * 0.04, 0.026), V(0, s * 0.05, 0.026)], 0.026, 'ahsap_koyu', n=12)
        boru(y, [V(0, s * 0.039, 0.026), V(0, s * 0.051, 0.026)], 0.022, 'ahsap_acik', n=12)
        cubuk(y, V(-0.06, s * 0.03, 0.036), V(-0.13, s * 0.03, 0.02), 0.007, 'ahsap')
    for k in range(3):
        amfora(y, -0.04 + 0.04 * k, 0.0, 0.03 + 0.011, 1.0, aci_x=math.pi / 2, aci_z=0.0, kulp=False, n=8)

# the plaza before the store wing: a well, sulphur crates, resin barrels, firewood
y.bolum('Kuyu, kükürt sandıkları, fıçılar')
WC = (0.2, 0.24)
donel(y, WC, [(0.045, Z0), (0.045, Z0 + 0.04), (0.05, Z0 + 0.045), (0.05, Z0 + 0.052), (0.036, Z0 + 0.052), (0.036, Z0 + 0.03)], 'mermer', n=16)
y.yuz_yon([V(p.x, p.y, Z0 + 0.03) for p in cokgen(WC, 0.036, 16)], 'koyu', Z)
for s_ in (-1, 1):
    cubuk(y, V(WC[0] + s_ * 0.042, WC[1], Z0 + 0.05), V(WC[0] + s_ * 0.042, WC[1], Z0 + 0.12), 0.008, 'ahsap')
boru(y, [V(WC[0] - 0.046, WC[1], Z0 + 0.105), V(WC[0] + 0.046, WC[1], Z0 + 0.105)], 0.009, 'ahsap_acik', n=8)
cubuk(y, V(WC[0], WC[1], Z0 + 0.1), V(WC[0], WC[1], Z0 + 0.06), 0.002, 'demir')
donel(y, (WC[0], WC[1]), [(0.0, Z0 + 0.04), (0.01, Z0 + 0.04), (0.011, Z0 + 0.06), (0.0, Z0 + 0.06)], 'ahsap', n=8)
for k in range(3):   # crates of sulphur
    cx, cy = 0.44 + 0.075 * k, 0.17 + 0.02 * (k % 2)
    kutu_merkez(y, (cx, cy), 0.06, 0.05, 0.035, 'ahsap_acik', z0=Z0, aci=0.1 * k)
    donel(y, (cx, cy), [(0.025, Z0 + 0.034), (0.016, Z0 + 0.046), (0.0, Z0 + 0.052)], 'boya_sari', n=10)
for k, (bx, by_, bz) in enumerate(((0.6, 0.3, 0.0), (0.64, 0.31, 0.0), (0.62, 0.27, 0.0), (0.62, 0.295, 0.042))):   # resin barrels
    donel(y, (bx, by_), [(0.0, Z0 + bz), (0.016, Z0 + bz), (0.019, Z0 + bz + 0.02), (0.016, Z0 + bz + 0.04), (0.0, Z0 + bz + 0.04)], 'ahsap', n=10)
    for zq in (0.008, 0.032):
        halka_kornis(y, (bx, by_), 0.0172, Z0 + bz + zq, 0.004, 0.0015, 10, 'demir')
for k in range(7):   # firewood
    zq = Z0 + 0.008 + 0.014 * (k // 4); yq = 0.24 + 0.016 * (k % 4) + 0.008 * (k // 4)
    cubuk(y, V(-0.0, yq, zq), V(0.1, yq, zq), 0.014, 'kutuk')

# ---------------------------------------------------------------- the siphon test stand on the quay, spitting fire
y.bolum('Sifon deneme tezgâhı ve alev')


def sifon_tezgah(x, yy, aci, ates=True):
    """a fire-siphon rig aimed towards aci: a brick brazier under a bronze tank, a force pump worked by a beam, the
    hose to a swivel nozzle with a lion-head mouth on a forked stand. Returns the muzzle point"""
    bas = len(y.faces)
    kutu(y, V(-0.09, -0.045, 0), X, 0.18, 0.09, 0.008, 'ahsap')
    kutu(y, V(-0.085, -0.03, 0.008), X, 0.06, 0.06, 0.04, 'tugla_roma')
    y.pencere(V(-0.055, -0.03, 0), X, -Y, -0.012, 0.012, 0.024, 0.022, 'altin', kemer=True, k_say=6)
    kure(y, (-0.055, 0, 0.074), 0.03, 'bronz', n=14, kat=7)
    for s in (-1, 1):   # tank bands
        halka_kornis(y, (-0.055, 0), 0.03, 0.068, 0.004, 0.002, 14, 'demir')
    # pump: two cylinders, a post and the rocking beam
    for s in (-1, 1):
        y.prizma((-0.005, s * 0.022), 0.009, 0.008, 0.06, 'bronz', n=10)
        cubuk(y, V(-0.005, s * 0.022, 0.06), V(-0.005, s * 0.022, 0.075), 0.003, 'demir')
    kutu_merkez(y, (-0.005, 0), 0.012, 0.012, 0.085, 'ahsap', z0=0.008)
    cubuk(y, V(-0.005, -0.06, 0.085), V(-0.005, 0.06, 0.095), 0.006, 'ahsap_koyu')
    # hose and nozzle on its fork
    kutu_merkez(y, (0.05, 0), 0.016, 0.016, 0.06, 'ahsap', z0=0.008)
    cubuk(y, V(0.05, -0.012, 0.068), V(0.05, 0.012, 0.068), 0.005, 'demir')
    boru(y, [V(-0.03, 0.0, 0.085), V(0.0, 0.0, 0.1), V(0.03, 0, 0.08), V(0.05, 0, 0.074)], 0.0045, 'ahsap_koyu', n=6)
    boru(y, [V(0.04, 0, 0.074), V(0.11, 0, 0.068)], 0.007, 'bronz', n=10, r_son=0.009)
    for f in (0.3, 0.7):
        boru(y, [V(0.04 + 0.07 * f, 0, 0.074 - 0.006 * f), V(0.044 + 0.07 * f, 0, 0.0735 - 0.006 * f)], 0.0095, 'altin', n=10)
    # the lion's head at the muzzle: a mane ring and a snout
    boru(y, [V(0.104, 0, 0.069), V(0.112, 0, 0.068)], 0.014, 'altin', n=12)
    boru(y, [V(0.112, 0, 0.068), V(0.122, 0, 0.067)], 0.0095, 'bronz', n=10, r_son=0.0075)
    for s in (-1, 1):
        kure(y, (0.11, s * 0.008, 0.08), 0.0035, 'bronz', n=5, kat=3)   # ears
    y.yuz_yon([V(0.1225, 0.0065 * math.cos(TAU * i / 10), 0.067 + 0.0065 * math.sin(TAU * i / 10)) for i in range(10)], 'koyu', X)
    tip = V(0.124, 0, 0.067)
    if ates:
        # the jet: one long licking tongue of fire, thin at the muzzle, swelling, rippling and narrowing to a point as it
        # drops towards the water; flicker tongues curl up off its back, a ragged smoke plume rises from its end
        L = 0.33
        yol = lambda d: tip + V(d, 0.012 * math.sin(TAU * d / 0.15) * (d / L) ** 1.2,
                                -0.12 * d * d + 1.1 * max(0.0, d - 0.7 * L) ** 2 + 0.006 * math.sin(TAU * d / 0.1) * (d / L))
        RENK = ('boya_sari', 'boya_sari', 'altin', 'altin', 'altin', 'kiremit', 'kiremit', 'boya_kirmizi', 'boya_kirmizi')
        alev_dil([yol(L * k / 24) for k in range(25)], 0.03, r0=0.0055, tepe=0.62, renk=RENK, n=12)
        # licks of flame curling up and back off the jet's back (their roots inside it)
        for t0, yan, boy, rr in ((0.46, 1, 0.05, 0.014), (0.6, -1, 0.07, 0.017), (0.76, 0.5, 0.055, 0.014)):
            b = yol(L * t0) + V(0, 0, 0.006)
            ana = RENK[int(len(RENK) * t0)]
            alev_dil([b + V(-boy * (0.55 * s - 0.18 * math.sin(TAU * s)), yan * boy * 0.3 * math.sin(math.pi * s), boy * s)
                      for s in (k / 8 for k in range(9))], rr, r0=rr * 1.1, tepe=0.12, renk=(ana, ana, 'kiremit', 'boya_kirmizi'), n=8, dalga=0.1, yass=0.6)
        # a ragged smoke plume of puffs rising from the flame's end
        e = yol(L * 0.94)
        for k, (dx, dy, dz, r) in enumerate(((0.0, 0.0, 0.045, 0.024), (0.018, 0.012, 0.075, 0.028), (0.006, -0.008, 0.11, 0.032), (0.03, 0.006, 0.14, 0.03),
                                              (0.02, -0.014, 0.172, 0.025))):
            kure(y, e + V(dx, dy, dz), r, 'granit_koyu' if k < 2 else 'granit', n=12, kat=6)
    return bas


def alev_dil(pts, rmax, r0=0.005, tepe=0.6, renk=('boya_sari', 'altin', 'kiremit', 'boya_kirmizi'), n=10, yass=0.8, dalga=0.14):
    """a tongue of flame (or smoke) along the centreline pts: r0 at the start, swelling to rmax at tepe (0..1 along),
    then narrowing to a point; the rim ripples (dalga) and the colour runs through renk from the root to the tip"""
    m = len(pts)
    def yari(t):
        if t <= tepe:
            return r0 + (rmax - r0) * math.sin(math.pi / 2 * t / tepe)
        return rmax * ((1 - t) / (1 - tepe)) ** 0.75
    rings = []
    for k, p in enumerate(pts):
        t = k / (m - 1)
        T = (pts[min(k + 1, m - 1)] - pts[max(k - 1, 0)]).normalized()
        U = T.cross(Z)
        U = U.normalized() if U.length > 1e-6 else V(0, 1, 0)
        W = U.cross(T).normalized()
        r = yari(t)
        dg = dalga * (0.4 + t)
        rings.append([p + (U * math.cos(TAU * i / n) * (1 + dg * math.sin(3 * TAU * i / n + 7 * t)) +
                           W * math.sin(TAU * i / n) * yass * (1 + dg * math.cos(2 * TAU * i / n + 5 * t))) * r for i in range(n)])
    for k in range(m - 1):
        key = renk[min(len(renk) - 1, int(len(renk) * (k + 0.5) / (m - 1)))]
        c = (pts[k] + pts[k + 1]) / 2
        for i in range(n):
            j = (i + 1) % n
            q = [rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]]
            if k == m - 2:
                y.yuz_yon([q[0], q[1], pts[-1]], key, (q[0] + q[1]) / 2 - c)
            else:
                y.yuz_yon(q, key, sum(q, Vector()) / 4 - c)
    y.yuz_yon(rings[0], renk[0], pts[0] - pts[1])


b0 = sifon_tezgah(0, 0, 0)
donustur(y, b0, egik(-0.78, 0.0), (-0.8, LY + 0.075, Z0))   # (aimed across the view: the tongue reads in profile)
b1 = sifon_tezgah(0, 0, 0, ates=False)
donustur(y, b1, egik(-math.pi / 2 + 0.4, 0.0), (0.35, LY + 0.075, Z0))
# a crate of fire grenades (clay pots) by the rig
for k in range(6):
    kure(y, (-0.58 + 0.02 * (k % 3), LY + 0.05 + 0.02 * (k // 3), Z0 + 0.01), 0.01, 'kum_koyu', n=8, kat=4)

# ---------------------------------------------------------------- the dromon, people
y.bolum('Dromon')
bd = len(y.faces)
dromon(y, 0, 0, ZS, 0.0, L=0.42, B=0.06, H=0.034, tohum=3)
donustur(y, bd, ((1.35, 0, 0), (0, 1.35, 0), (0, 0, 1.35)), (0.18, -0.85, ZS * (1 - 1.35)))
# fire from the dromon's bow siphon too (a short jet)
bow = V(0.18 + 0.21 * 1.35 + 0.012 * 1.35, -0.85, ZS + (0.034 + 0.016 + 0.004) * 1.35)
alev_dil([bow + V(0.11 * s, 0.006 * math.sin(math.pi * 2 * s), -0.03 * s * s) for s in (k / 9 for k in range(10))], 0.014, r0=0.003, tepe=0.55)

y.bolum('İnsanlar')
for x, yy, a, key, kol in ((-0.77, -0.2, 2.5, 'kirmizi', 0.6), (-0.6, -0.15, 1.2, 'ahsap_acik', 0.0), (-0.14, -0.08, 1.6, 'kum_koyu', 0.4),
                           (0.12, -0.08, 1.4, 'kirmizi', 0.0), (-0.68, LY + 0.14, -1.6, 'ahsap_acik', 0.7), (0.5, -0.24, 2.8, 'kum_koyu', 0.0)):
    insan(y, x, yy, Z0, key, s=1.5, aci=a, kol=kol)
for gx in (GX0 - 0.08, GX1 + 0.08):
    muhafiz(y, gx, WY - 0.06, Z0, aci=-math.pi / 2, s=0.95, giysi='boya_kirmizi', kalkan='boya_kirmizi', silah='mizrak')

calistir(y, 'lm_rumatesi')
