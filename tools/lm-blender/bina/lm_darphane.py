# The Byzantine mint (lm_darphane): a domed workshop hall in banded stone-and-brick with round-arched windows, a
# great lead dome on a windowed drum and two smaller ones, furnace chimneys; before it a portal whose arch is lined
# with gold mosaic (an enthroned emperor); a walled yard with beehive smelting furnaces, coin-striking anvils with
# their workers, chests and stacks of gold coins and ingots, balances and a steelyard, a treasury, and a tall guard
# tower with the banner over the gate.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from bizans_ortak import *

y = Yapi(tohum=4)
R = random.Random(9)
Z0 = 0.04

# ---------------------------------------------------------------- platform
y.bolum('Zemin')
zemin(y, -1.1, 1.1, -0.95, 0.95, Z0, 'tas_koyu', basamak=(('on', 0.4),))

# ---------------------------------------------------------------- the workshop hall
y.bolum('Atölye salonu (almaşık)')
HX0, HX1, HY0, HY1 = -0.78, 0.62, 0.12, 0.82
HH = 0.27
k = dikdortgen(HX0, HX1, HY0, HY1)
for i, n in enumerate((10, 5, 10, 5)):
    almasik(y, k[i], k[(i + 1) % 4], Z0, HH, n, en=0.42, v0=0.08, ust=0.035, kapi_bay=2 if i == 1 else None, bos=(4, 5) if i == 0 else ())
silme(y, k, Z0, 0.016, 0.01, 'kirec', 'kaide')
silme(y, k, Z0 + HH - 0.016, 0.02, 0.014, 'kirec', 'tac')
for p in k:   # corner piers
    kutu_merkez(y, (p.x, p.y), 0.05, 0.05, HH - 0.006, 'kirec', z0=Z0)
ZR = Z0 + HH + 0.004
# the raised middle (a clerestory carrying the domes) and tiled lean-to roofs over the front and back aisles
CY0, CY1, CH = 0.25, 0.69, 0.12
ZC = ZR + CH
y.yuz_yon([V(p.x, p.y, ZR) for p in k], 'kursun', Z)   # (under the aisle roofs)
ck = dikdortgen(HX0, HX1, CY0, CY1)
for i, n in enumerate((12, 3, 12, 3)):
    almasik(y, ck[i], ck[(i + 1) % 4], ZR, CH, n, en=0.42, v0=0.056, ust=0.014, derin=0.012, k_say=5, bant_list=[(0.04, 0.01)],
            cer=(0.004, ['tugla_roma', 'kirec']))
silme(y, ck, ZC - 0.012, 0.016, 0.012, 'kirec', 'tac')
y.yuz_yon([V(p.x, p.y, ZC + 0.002) for p in ck], 'kursun', Z)
parapet(y, ck, ZC + 0.002, 0.012, 0.0, 0.01, 'kirec', ust_key='tas_acik')
for k_ in range(1, 18):   # lead sheet seams on the clerestory roof
    xx = HX0 + (HX1 - HX0) * k_ / 18
    cubuk(y, V(xx, CY0 + 0.012, ZC + 0.004), V(xx, CY1 - 0.012, ZC + 0.004), 0.005, 'kursun2', 0.004)


def egik_cati(y0, y1, z0, z1, x0, x1, t=0.008):
    """a lean-to tile roof from the eave line y0 (z0) up to y1 (z1), x0..x1: tiles, the boards under it, the edges,
    the triangles closing it over the hall's end walls"""
    s_ = 1 if y1 > y0 else -1
    top = [V(x0, y0, z0), V(x1, y0, z0), V(x1, y1, z1), V(x0, y1, z1)]
    up = Z - Y * s_ * ((z1 - z0) / abs(y1 - y0))
    y.yuz_yon(top, 'kiremit', up)
    y.yuz_yon([p - Z * t for p in top], 'ahsap_koyu', -up)
    y.yuz_yon([top[0], top[1], top[1] - Z * t, top[0] - Z * t], 'ahsap_koyu', -Y * s_)   # the eave's fascia
    y.yuz_yon([top[0], top[3], top[3] - Z * t, top[0] - Z * t], 'ahsap_koyu', -X)
    y.yuz_yon([top[1], top[2], top[2] - Z * t, top[1] - Z * t], 'ahsap_koyu', X)
    cubuk(y, top[0] + V(0, s_ * 0.004, 0.004), top[1] + V(0, s_ * 0.004, 0.004), 0.007, 'kiremit2', 0.005)   # eave course
    ye = y0 + s_ * 0.028
    for xx, nx in ((HX0, -X), (HX1, X)):
        zz = z0 + (z1 - z0) * abs(ye - y0) / abs(y1 - y0) - t
        y.yuz_yon([V(xx, ye, ZR - 0.004), V(xx, y1, ZR - 0.004), V(xx, y1, z1 - t), V(xx, ye, zz)], 'kirec', nx)


egik_cati(HY0 - 0.028, CY0, ZR - 0.004, ZR + 0.044, HX0 - 0.026, HX1 + 0.026)
egik_cati(HY1 + 0.028, CY1, ZR - 0.004, ZR + 0.044, HX0 - 0.026, HX1 + 0.026)

y.bolum('Kubbeler ve bacalar')
DC = ((HX0 + HX1) / 2 - 0.08, (HY0 + HY1) / 2)
kutu_merkez(y, DC, 0.42, 0.42, 0.04, 'kirec', z0=ZC)
kornis(y, DC[0] - 0.21, DC[0] + 0.21, DC[1] - 0.21, DC[1] + 0.21, ZC + 0.03, 0.012, 0.01, 'kirec', 'tac')
for sx in (-1, 1):
    for sy in (-1, 1):   # corner turrets of the dome base
        y.prizma((DC[0] + sx * 0.19, DC[1] + sy * 0.19), 0.025, ZC + 0.04, ZC + 0.07, 'tugla_roma', n=8, kat=math.pi / 8)
        y.koni((DC[0] + sx * 0.19, DC[1] + sy * 0.19), 0.03, ZC + 0.07, 0.04, 'kursun', n=8)
biz_kubbe(y, DC, 0.18, ZC + 0.04, 0.08, 16, kubbe_h=0.15)
for dx in (-0.47, 0.42):
    c = (DC[0] + dx, DC[1] - 0.04)
    kutu_merkez(y, c, 0.22, 0.22, 0.02, 'kirec', z0=ZC)
    biz_kubbe(y, c, 0.09, ZC + 0.02, 0.05, 8, kubbe_h=0.075)


def baca(cx, cy, z0, h, r=0.03):
    """a square brick furnace chimney with stone bands, a cornice and a smoking mouth"""
    w = r * 2
    duvarlar(y, dikdortgen(cx - r * 1.2, cx + r * 1.2, cy - r * 1.2, cy + r * 1.2), z0, z0 + 0.04, 'kirec', ust='kirec')
    kk = dikdortgen(cx - r, cx + r, cy - r, cy + r)
    duvarlar(y, kk, z0 + 0.04, z0 + h, 'tugla_roma')
    for t in (0.3, 0.6):
        silme(y, kk, z0 + 0.04 + (h - 0.04) * t, 0.01, 0.003, 'kirec')
    silme(y, kk, z0 + h - 0.014, 0.016, 0.008, 'kirec', 'tac')
    ic = disa(kk, -0.006)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([kk[i] + Z * (z0 + h + 0.002), kk[j] + Z * (z0 + h + 0.002), ic[j] + Z * (z0 + h + 0.002), ic[i] + Z * (z0 + h + 0.002)], 'kirec', Z)
        duz_duvar(y, ic[j], ic[i], z0 + h - 0.01, z0 + h + 0.002, 'tugla_roma_koyu')
    y.yuz_yon([V(p.x, p.y, z0 + h - 0.01) for p in ic], 'koyu', Z)
    for k_, (dz, rr, dx) in enumerate(((0.03, 0.022, 0.0), (0.07, 0.03, 0.01), (0.12, 0.036, 0.025))):   # smoke puffs
        kure(y, (cx + dx, cy + dx * 0.4, z0 + h + dz), rr, 'beyaz' if k_ == 2 else 'kum_acik', n=8, kat=5)


for x in (HX0 + 0.12, HX1 - 0.12, (HX0 + HX1) / 2 + 0.2):
    baca(x, HY1 - 0.07, ZR, 0.27 if x != (HX0 + HX1) / 2 + 0.2 else 0.33)

# ---------------------------------------------------------------- the mosaic portal
y.bolum('Altın mozaikli giriş')
PX = (HX0 + HX1) / 2 - 0.08
PW, PD, PHH = 0.28, 0.08, 0.38
PY0 = HY0 - PD
y.kemerli(V(PX - PW / 2, PY0), V(PX + PW / 2, PY0), Z0, PHH, ('kirec', 'tas_koyu', 'mermer', 'altin'), v0=0.0, en=0.62, ust=0.07, derin=0.05,
          k_say=12, cerceve=(0.014, ['tugla_roma', 'kirec']))
for a, b in ((V(PX + PW / 2, PY0), V(PX + PW / 2, HY0)), (V(PX - PW / 2, HY0), V(PX - PW / 2, PY0))):
    almasik(y, a, b, Z0, PHH, 0)
kornis(y, PX - PW / 2, PX + PW / 2, PY0, HY0 + 0.002, Z0 + PHH - 0.016, 0.02, 0.014, 'kirec', 'tac')
y.yuz_yon([V(PX - PW / 2, PY0, Z0 + PHH + 0.004), V(PX + PW / 2, PY0, Z0 + PHH + 0.004), V(PX + PW / 2, HY0, Z0 + PHH + 0.004), V(PX - PW / 2, HY0, Z0 + PHH + 0.004)],
          'kursun', Z)
duz_duvar(y, V(PX + PW / 2, HY0), V(PX - PW / 2, HY0), Z0 + HH, Z0 + PHH, 'kirec')   # (its back above the hall's roof)
# a pediment-like stepped crown and a cross
kutu(y, V(PX - 0.06, PY0 + 0.01, Z0 + PHH + 0.004), X, 0.12, PD - 0.02, 0.03, 'kirec')
hac(y, PX, PY0 + PD / 2, Z0 + PHH + 0.034, 0.05)
# inside the arch: the door below, the gold mosaic of the enthroned emperor above
yb = PY0 + 0.05 - 0.0025
y.yuz_yon([V(PX - 0.06, yb, Z0), V(PX + 0.06, yb, Z0), V(PX + 0.06, yb, Z0 + 0.14), V(PX - 0.06, yb, Z0 + 0.14)], 'ahsap', -Y)
for xx in (PX - 0.03, PX + 0.03):
    y.yuz_yon([V(xx - 0.0015, yb - 0.001, Z0 + 0.01), V(xx + 0.0015, yb - 0.001, Z0 + 0.01), V(xx + 0.0015, yb - 0.001, Z0 + 0.13), V(xx - 0.0015, yb - 0.001, Z0 + 0.13)], 'demir', -Y)
y.yuz_yon([V(PX - 0.066, yb - 0.0005, Z0 + 0.14), V(PX + 0.066, yb - 0.0005, Z0 + 0.14), V(PX + 0.066, yb - 0.0005, Z0 + 0.152), V(PX - 0.066, yb - 0.0005, Z0 + 0.152)], 'mermer', -Y)
ym = yb - 0.0008


def disk(cx, cz, r, key, yy, n=12):
    y.yuz_yon([V(cx + r * math.cos(TAU * i / n), yy, cz + r * math.sin(TAU * i / n)) for i in range(n)], key, -Y)


# throne, robe, head, halo, two attendants
y.yuz_yon([V(PX - 0.03, ym, Z0 + 0.16), V(PX + 0.03, ym, Z0 + 0.16), V(PX + 0.03, ym, Z0 + 0.215), V(PX - 0.03, ym, Z0 + 0.215)], 'boya_kirmizi', -Y)
y.yuz_yon([V(PX - 0.018, ym - 0.0006, Z0 + 0.158), V(PX + 0.018, ym - 0.0006, Z0 + 0.158), V(PX + 0.012, ym - 0.0006, Z0 + 0.222), V(PX - 0.012, ym - 0.0006, Z0 + 0.222)],
          'lacivert', -Y)
disk(PX, Z0 + 0.237, 0.017, 'beyaz', ym - 0.0003, 14)
disk(PX, Z0 + 0.233, 0.009, 'kum_acik', ym - 0.0009, 10)
for sx in (-1, 1):
    x = PX + sx * 0.06
    y.yuz_yon([V(x - 0.01, ym, Z0 + 0.158), V(x + 0.01, ym, Z0 + 0.158), V(x + 0.007, ym, Z0 + 0.205), V(x - 0.007, ym, Z0 + 0.205)], 'beyaz', -Y)
    disk(x, Z0 + 0.213, 0.007, 'kum_acik', ym - 0.0004, 8)
# a gold-lined border of stars round the mosaic
for i in range(9):
    a = math.pi * (i + 0.5) / 9
    disk(PX + 0.075 * math.cos(a), Z0 + 0.19 + 0.075 * math.sin(a) * 0.75, 0.004, 'beyaz', ym - 0.0004, 5)
# guards at the door
for sx in (-1, 1):
    insan(y, PX + sx * 0.1, PY0 - 0.03, Z0, 'boya_kirmizi', 1.6, aci=-math.pi / 2, sapka='demir')
    cubuk(y, V(PX + sx * 0.1 + 0.016, PY0 - 0.03, Z0), V(PX + sx * 0.1 + 0.016, PY0 - 0.03, Z0 + 0.1), 0.0026, 'ahsap')
    y.koni((PX + sx * 0.1 + 0.016, PY0 - 0.03), 0.005, Z0 + 0.1, 0.016, 'demir', n=4)

# ---------------------------------------------------------------- the yard wall and gate
y.bolum('Avlu duvarı ve kapı')
AY0 = -0.86
YH = 0.09


def avlu_duvari(a, b):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    L = (b - a).length
    kutu(y, a + nc * 0.015 + Z * Z0, e, L, 0.03, YH, 'kirec', 'onarka')
    serit_tas(y, a + nc * 0.015, b + nc * 0.015, Z0, 0, L, 0.035, 0.014, 'tugla_roma', 0.002)
    kutu(y, a + nc * 0.019 + Z * (Z0 + YH), e, L, 0.038, 0.01, 'tugla_roma', 'onarkaust')
    n = max(1, int(L / 0.2))
    for k in range(n + 1):
        p = a.lerp(b, k / n)
        kutu_merkez(y, (p.x, p.y), 0.04, 0.045, YH + 0.022, 'kirec', z0=Z0)
        y.koni((p.x, p.y), 0.026, Z0 + YH + 0.022, 0.022, 'tugla_roma', n=4)


avlu_duvari(V(-1.04, AY0), V(-0.12, AY0))
avlu_duvari(V(0.12, AY0), V(1.04, AY0))
avlu_duvari(V(-1.04, HY0 - 0.02), V(-1.04, AY0))
avlu_duvari(V(1.04, AY0), V(1.04, HY0 - 0.02))
for xa, xb in ((-1.04, HX0), (HX1, 1.04)):
    avlu_duvari(V(xb, HY0 - 0.02), V(xa, HY0 - 0.02)) if xa < 0 else avlu_duvari(V(xb, HY0 - 0.02), V(xa, HY0 - 0.02))
y.yuz_yon([V(-1.04, AY0, Z0 + 0.002), V(1.04, AY0, Z0 + 0.002), V(1.04, HY0 - 0.02, Z0 + 0.002), V(-1.04, HY0 - 0.02, Z0 + 0.002)], 'toprak', Z)
# paving: the way from the gate to the portal, aprons
y.yuz_yon([V(PX - 0.07, AY0 + 0.03, Z0 + 0.004), V(PX + 0.07, AY0 + 0.03, Z0 + 0.004), V(PX + 0.07, PY0, Z0 + 0.004), V(PX - 0.07, PY0, Z0 + 0.004)], 'zemin', Z)
y.yuz_yon([V(HX0, HY0 - 0.08, Z0 + 0.004), V(HX1, HY0 - 0.08, Z0 + 0.004), V(HX1, HY0 - 0.02, Z0 + 0.004), V(HX0, HY0 - 0.02, Z0 + 0.004)], 'zemin', Z)
y.yuz_yon([V(-0.08, AY0 + 0.03, Z0 + 0.0042), V(PX - 0.07, AY0 + 0.03, Z0 + 0.0042), V(PX - 0.07, AY0 + 0.1, Z0 + 0.0042), V(-0.08, AY0 + 0.1, Z0 + 0.0042)], 'zemin', Z)
# the gate: a small banded gatehouse with a round arch
gx0, gx1, gy0, gy1 = -0.12, 0.12, AY0 - 0.02, AY0 + 0.05
y.kemerli(V(gx0, gy0), V(gx1, gy0), Z0, 0.2, ('kirec', 'tas_koyu', 'mermer', 'ahsap'), v0=0, en=0.5, ust=0.05, derin=0.03, k_say=10,
          cerceve=(0.012, ['tugla_roma', 'kirec']))
y.kemerli(V(gx1, gy1), V(gx0, gy1), Z0, 0.2, ('kirec', 'tas_koyu', 'mermer', 'ahsap'), v0=0, en=0.5, ust=0.05, derin=0.03, k_say=10)
almasik(y, V(gx1, gy0), V(gx1, gy1), Z0, 0.2, 0)
almasik(y, V(gx0, gy1), V(gx0, gy0), Z0, 0.2, 0)
gk = dikdortgen(gx0, gx1, gy0, gy1)
silme(y, gk, Z0 + 0.186, 0.018, 0.012, 'kirec', 'tac')
cati_kirma(y, gx0, gx1, gy0, gy1, Z0 + 0.204, 0.06, 0.02, 'kiremit', 'kiremit2', kalinlik=0.01)
hac(y, 0, (gy0 + gy1) / 2, Z0 + 0.264, 0.04)

# ---------------------------------------------------------------- the guard tower
y.bolum('Muhafız kulesi')
TX, TY, TW = -0.9, -0.72, 0.2
TH = 0.68
tk = dikdortgen(TX - TW / 2, TX + TW / 2, TY - TW / 2, TY + TW / 2)
for i in range(4):
    almasik(y, tk[i], tk[(i + 1) % 4], Z0, 0.26, 1 if i in (0, 1) else 0, en=0.32, v0=0.0 if i == 1 else 0.12, ust=0.03,
            kapi_bay=0 if i == 1 else None, kapi_en=0.42)
    almasik(y, tk[i], tk[(i + 1) % 4], Z0 + 0.26, 0.22, 1, en=0.28, v0=0.07, ust=0.035)
    almasik(y, tk[i], tk[(i + 1) % 4], Z0 + 0.48, TH - 0.48, 2, en=0.42, v0=0.06, ust=0.03, derin=0.02)
silme(y, tk, Z0, 0.016, 0.01, 'kirec', 'kaide')
silme(y, tk, Z0 + 0.255, 0.012, 0.01, 'kirec', 'kaba')
silme(y, tk, Z0 + 0.475, 0.012, 0.01, 'kirec', 'kaba')
konsol_halka(y, tk, Z0 + TH - 0.03, 0.03, 0.014, 'kirec', 3)
tr = disa(tk, 0.014)
parapet(y, tr, Z0 + TH, 0.012, 0.03, 0.016, 'kirec')
y.yuz_yon([V(p.x, p.y, Z0 + TH + 0.0005) for p in disa(tr, -0.016)], 'zemin', Z)
cati_kirma(y, TX - TW / 2 + 0.02, TX + TW / 2 - 0.02, TY - TW / 2 + 0.02, TY + TW / 2 - 0.02, Z0 + TH + 0.04, 0.12, 0.012, 'kiremit', 'kiremit2',
           kalinlik=0.008)
for p in tk:   # posts carrying the roof over the walk
    y.prizma((p.x + (TX - p.x) * 0.18, p.y + (TY - p.y) * 0.18), 0.005, Z0 + TH, Z0 + TH + 0.04, 'ahsap_koyu', n=4, ust=False)
sancak(y, TX, TY, Z0 + TH + 0.15, boy=0.2, en=0.13, yuk=0.075, aci=math.pi * 0.85)
insan(y, TX + 0.07, TY - 0.07, Z0 + TH, 'boya_kirmizi', 1.4, aci=-math.pi / 2, sapka='demir')

# ---------------------------------------------------------------- the furnaces
y.bolum('Eritme ocakları')


def ocak(cx, cy, r=0.075, yon=-math.pi / 2):
    """a beehive smelting furnace of brick: domed, an arched glowing mouth towards yon, a short chimney, a bellows"""
    donel(y, (cx, cy), [(r * 1.08, Z0), (r * 1.08, Z0 + 0.02), (r, Z0 + 0.025), (r * 0.98, Z0 + 0.06), (r * 0.8, Z0 + 0.1), (r * 0.45, Z0 + 0.135),
                        (0.018, Z0 + 0.145)], 'tugla_roma', n=16)
    y.prizma((cx, cy), 0.018, Z0 + 0.14, Z0 + 0.2, 'tugla_roma', n=8)
    halka_kornis(y, (cx, cy), 0.018, Z0 + 0.19, 0.01, 0.005, 8, 'kirec')
    y.yuz_yon([V(p.x, p.y, Z0 + 0.2) for p in cokgen((cx, cy), 0.018, 8)], 'koyu', Z)
    kure(y, (cx + 0.005, cy, Z0 + 0.225), 0.016, 'kum_acik', n=8, kat=4)
    e = V(math.cos(yon), math.sin(yon)); s = V(-e.y, e.x)
    o = V(cx, cy) + e * (r * 1.0 + 0.012)
    # the mouth: a brick arch frame and the glow inside
    kutu(y, o - s * 0.04 + Z * Z0, s, 0.08, -0.03, 0.075, 'tugla_roma', 'onarkasagsolust')
    pts = [o - s * 0.022 + e * 0.0312 + Z * (Z0 + 0.005)] + [o + s * (0.022 * math.cos(math.pi - math.pi * k / 6)) + e * 0.0312 +
                                                              Z * (Z0 + 0.035 + 0.022 * math.sin(math.pi * k / 6)) for k in range(7)] + [o + s * 0.022 + e * 0.0312 + Z * (Z0 + 0.005)]
    y.yuz_yon(pts, 'boya_sari', e)
    inner = [o + (p - o) * 0.6 + e * 0.0008 - Z * 0.004 for p in pts]
    y.yuz_yon([q + e * 0.0004 for q in inner], 'boya_kirmizi', e)
    # bellows beside it
    b = o + s * 0.07 + e * 0.01
    kutu_merkez(y, (b.x, b.y), 0.04, 0.03, 0.012, 'ahsap_koyu', z0=Z0, aci=yon)
    kutu_merkez(y, (b.x, b.y), 0.036, 0.026, 0.01, 'kece', z0=Z0 + 0.012, aci=yon)
    # firewood
    for k in range(4):
        q = o - s * 0.07 + e * 0.02
        cubuk(y, V(q.x, q.y, Z0 + 0.006 + 0.008 * (k // 2)) + s * (0.008 * (k % 2)) - e * 0.025, V(q.x, q.y, Z0 + 0.006 + 0.008 * (k // 2)) + s * (0.008 * (k % 2)) + e * 0.025,
              0.008, 'ahsap')


ocak(0.75, -0.08, 0.08, math.pi)
ocak(0.75, -0.38, 0.07, math.pi)
insan(y, 0.6, -0.12, Z0, 'kumas', 1.5, aci=0.0, kol=0.4)
insan(y, 0.6, -0.42, Z0, 'siva_oker', 1.5, aci=0.0)
# crucibles and moulds by the furnaces
for k in range(3):
    donel(y, (0.58 + 0.04 * k, -0.24), [(0.0, Z0), (0.012, Z0), (0.016, Z0 + 0.022), (0.0125, Z0 + 0.022), (0.0125, Z0 + 0.018), (0.0, Z0 + 0.018)], 'kum_koyu', n=10)
    y.yuz_yon([V(p.x, p.y, Z0 + 0.019) for p in cokgen((0.58 + 0.04 * k, -0.24), 0.0122, 10)], 'altin', Z)

# ---------------------------------------------------------------- coin striking, chests, ingots
y.bolum('Sikke basma tezgâhları, sandıklar')


def ors(cx, cy, aci, renk):
    """a coin-striking station: a log block with an iron die, a worker with a raised hammer, a basket of blanks"""
    with parca(y, (cx, cy, Z0), aci):
        donel(y, (0, 0), [(0.0, 0.0), (0.024, 0.0), (0.022, 0.05), (0.0, 0.05)], 'ahsap', n=10)
        kutu_merkez(y, (0, 0), 0.022, 0.016, 0.014, 'demir', z0=0.05)
        kutu_merkez(y, (0, 0), 0.01, 0.01, 0.012, 'demir', z0=0.064)
        insan(y, -0.05, 0.0, 0.0, renk, 1.5, aci=0.0, kol=1.0)
        cubuk(y, V(-0.046, 0.014, 0.06), V(-0.03, 0.014, 0.086), 0.003, 'ahsap')
        kutu_merkez(y, (-0.029, 0.014), 0.016, 0.01, 0.01, 'demir', z0=0.082)
        donel(y, (0.04, 0.02), [(0.0, 0.0), (0.014, 0.0), (0.018, 0.016), (0.0155, 0.016), (0.0155, 0.012), (0.0, 0.012)], 'saz', n=10)
        y.yuz_yon([V(p.x, p.y, 0.013) for p in cokgen((0.04, 0.02), 0.0155, 10)], 'altin', Z)
        for k in range(3):   # struck coins piling on a cloth
            y.prizma((0.032 + 0.008 * k, -0.026), 0.0055, 0.0, 0.003 + 0.003 * k, 'altin', n=8)
        y.yuz_yon([V(0.02, -0.04, 0.0006), V(0.065, -0.04, 0.0006), V(0.065, -0.012, 0.0006), V(0.02, -0.012, 0.0006)], 'boya_kirmizi', Z)


for k, (x, yy) in enumerate(((-0.55, -0.15), (-0.32, -0.15), (-0.55, -0.4), (-0.32, -0.4))):
    ors(x, yy, -math.pi / 2 + (0.2 if k % 2 else -0.2), ('kumas', 'siva_oker', 'beyaz', 'kirmizi')[k])
# a long table with the overseer and stacks of coins
kutu_merkez(y, (0.18, -0.2), 0.26, 0.07, 0.004, 'ahsap', z0=Z0 + 0.04)
for sx in (-1, 1):
    for sy in (-1, 1):
        y.prizma((0.18 + sx * 0.12, -0.2 + sy * 0.028), 0.004, Z0, Z0 + 0.04, 'ahsap_koyu', n=4, ust=False)
for k in range(7):
    y.prizma((0.08 + 0.03 * k, -0.2 + 0.012 * ((k % 3) - 1)), 0.008, Z0 + 0.044, Z0 + 0.05 + 0.004 * (k % 4), 'altin', n=10)
insan(y, 0.18, -0.12, Z0, 'lacivert', 1.55, aci=-math.pi / 2, kol=0.3, sapka='boya_kirmizi')
insan(y, 0.06, -0.12, Z0, 'kumas', 1.45, aci=-math.pi / 2)


def sandik(cx, cy, aci, acik=True):
    """an iron-bound strongbox, open and full of coins, or shut"""
    with parca(y, (cx, cy, Z0), aci):
        kutu_merkez(y, (0, 0), 0.06, 0.04, 0.034, 'ahsap', z0=0)
        for x in (-0.022, 0.022):
            kutu(y, V(x - 0.003, -0.0205, 0), X, 0.006, 0.041, 0.035, 'demir', 'onarkaust')
        if acik:
            y.yuz_yon([V(-0.028, -0.018, 0.03), V(0.028, -0.018, 0.03), V(0.028, 0.018, 0.03), V(-0.028, 0.018, 0.03)], 'altin', Z)
            for k in range(5):
                kure(y, (-0.018 + 0.009 * k, 0.004 * ((k % 2) * 2 - 1), 0.031), 0.008, 'altin', n=6, kat=3)
            kutu(y, V(-0.03, 0.02, 0.034), X, 0.06, 0.006, 0.04, 'ahsap_koyu')   # the lid standing open
        else:
            kutu_merkez(y, (0, 0), 0.062, 0.042, 0.008, 'ahsap_koyu', z0=0.034)


sandik(0.0, -0.45, 0.1)
sandik(0.09, -0.48, -0.2, False)
sandik(0.05, -0.56, 0.3, True)
# ingots stacked
for k in range(3):
    for j in range(4 - k):
        kutu_merkez(y, (0.25 + 0.022 * j + 0.011 * k, -0.5), 0.02, 0.05, 0.009, 'altin' if (j + k) % 2 else 'bronz', z0=Z0 + 0.009 * k)

# ---------------------------------------------------------------- balances and a steelyard
y.bolum('Teraziler ve kantar')


def terazi(cx, cy, aci, s=1.0):
    """an equal-arm balance on a post: a base, a post, the beam, two pans on cords"""
    with parca(y, (cx, cy, Z0), aci, s):
        kutu_merkez(y, (0, 0), 0.04, 0.04, 0.008, 'kirec', z0=0)
        y.prizma((0, 0), 0.0035, 0.008, 0.11, 'bronz', n=6)
        kure(y, (0, 0, 0.112), 0.005, 'bronz', n=6, kat=3)
        cubuk(y, V(-0.05, 0, 0.104), V(0.05, 0, 0.104), 0.003, 'bronz')
        for sx in (-1, 1):
            for dy in (-0.008, 0.008):
                cubuk(y, V(sx * 0.05, 0, 0.104), V(sx * 0.05, dy, 0.05), 0.0012, 'bronz')
            donel(y, (sx * 0.05, 0), [(0.0, 0.044), (0.016, 0.046), (0.018, 0.05), (0.0, 0.048)], 'bronz', n=10)
        for k in range(3):
            y.prizma((-0.05, 0), 0.006, 0.048, 0.051 + 0.002 * k, 'altin', n=8)


terazi(0.36, -0.2, 0.0)
terazi(-0.12, -0.32, 0.0, 0.9)
# the steelyard: a timber tripod, a long beam with a counterweight, a hook carrying a sack of coin
KX, KY = 0.32, -0.66
top = V(KX, KY, Z0 + 0.26)
for a in (math.radians(90), math.radians(210), math.radians(330)):
    cubuk(y, V(KX + 0.11 * math.cos(a), KY + 0.1 * math.sin(a), Z0), top, 0.01, 'ahsap')
kure(y, top + Z * 0.006, 0.012, 'ahsap_koyu', n=8, kat=4)
cubuk(y, top - Z * 0.005, top - Z * 0.04, 0.002, 'demir')
bm = top - Z * 0.042
cubuk(y, bm + V(-0.06, 0, 0.004), bm + V(0.1, 0, -0.008), 0.004, 'bronz')
cubuk(y, bm + V(-0.05, 0, 0.002), bm + V(-0.05, 0, -0.06), 0.0012, 'demir')
donel(y, (bm.x - 0.05, bm.y), [(0.0, bm.z - 0.12), (0.022, bm.z - 0.11), (0.025, bm.z - 0.085), (0.012, bm.z - 0.062), (0.0, bm.z - 0.06)], 'kumas', n=10)
cubuk(y, bm + V(0.075, 0, -0.006), bm + V(0.075, 0, -0.04), 0.0012, 'demir')
donel(y, (bm.x + 0.075, bm.y), [(0.0, bm.z - 0.06), (0.012, bm.z - 0.055), (0.009, bm.z - 0.04), (0.0, bm.z - 0.038)], 'demir', n=8)

# ---------------------------------------------------------------- the treasury
y.bolum('Hazine odası')
QX0, QX1, QY0, QY1 = 0.55, 0.98, -0.8, -0.55
QH = 0.16
qk = dikdortgen(QX0, QX1, QY0, QY1)
for i, n in enumerate((3, 2, 3, 2)):
    almasik(y, qk[i], qk[(i + 1) % 4], Z0, QH, n, en=0.32, v0=0.06, ust=0.03, kapi_bay=0 if i == 3 else None, kapi_en=0.45, cer=(0.006, ['tugla_roma', 'kirec']))
silme(y, qk, Z0 + QH - 0.012, 0.016, 0.01, 'kirec', 'tac')
kiremit_cati(y, QX0, QX1, QY0, QY1, Z0 + QH, 0.08, sacak=0.02)
for k in range(2):
    insan(y, QX0 - 0.04, -0.62 - 0.07 * k, Z0, 'boya_kirmizi', 1.5, aci=math.pi, sapka='demir')

# ---------------------------------------------------------------- trees, a cart
y.bolum('Ağaçlar, araba')
for x, yy in ((0.95, -0.86 + 0.25 + 0.05), (-0.75, -0.8), (-0.62, -0.8)):
    agac(y, x, yy, Z0, boy=0.16, tur='servi', key='yesil_koyu')
agac(y, -0.15, -0.65, Z0, boy=0.14, tur='yapraklı', key='zeytin')
# a handcart with ingot boxes
with parca(y, (-0.32, -0.66, Z0), 0.4):
    kutu_merkez(y, (0, 0), 0.09, 0.05, 0.006, 'ahsap', z0=0.022)
    for sy in (-1, 1):
        boru(y, [V(0.0, sy * 0.028, 0.02), V(0.0, sy * 0.034, 0.02)], 0.02, 'ahsap_koyu', n=12)
    for k in range(2):
        kutu_merkez(y, (-0.02 + 0.04 * k, 0), 0.034, 0.04, 0.025, 'ahsap_acik', z0=0.028)
    cubuk(y, V(0.045, -0.015, 0.025), V(0.11, -0.015, 0.01), 0.004, 'ahsap')
    cubuk(y, V(0.045, 0.015, 0.025), V(0.11, 0.015, 0.01), 0.004, 'ahsap')

# ---------------------------------------------------------------- the striking shed
y.bolum('Sikke atölyesi revağı')
SX0, SX1, SY0, SY1 = -1.02, -0.86, -0.56, 0.04
SH = 0.14
kutu(y, V(-1.016, SY0, Z0), Y, SY1 - SY0, 0.048, SH + 0.038, 'kirec', 'onarkasagsolust')   # its back wall (wraps the yard wall)
serit_tas(y, V(SX0, SY0), V(SX0, SY1), Z0, 0, SY1 - SY0, 0.05, 0.014, 'tugla_roma')
for zb in (0.05, 0.11, 0.17):
    serit_tas(y, V(-1.064, SY1), V(-1.064, SY0), Z0, 0, SY1 - SY0, zb, 0.014, 'tugla_roma')
arkad(y, V(SX1, SY0), V(SX1, SY1), 5, Z0, SH, en=0.66, ust=0.022, sivri=0.0, derin=0.03, cerceve=(0.007, ['tugla_roma', 'kirec']),
      renk=('kirec', 'kirec', 'mermer', 'tas_koyu'), sutun_r=0.008, sutun_key='mermer')
for a, b in ((V(SX0, SY0), V(SX1, SY0)), (V(SX1, SY1), V(SX0, SY1))):
    almasik(y, a, b, Z0, SH, 0, bant_list=[(0.05, 0.014)])
y.yuz_yon([V(SX0, SY0, Z0 + 0.003), V(SX1, SY0, Z0 + 0.003), V(SX1, SY1, Z0 + 0.003), V(SX0, SY1, Z0 + 0.003)], 'zemin', Z)
# the lean-to roof falling towards the yard
zt, ze = Z0 + SH + 0.06, Z0 + SH + 0.004
xe, xt = SX1 + 0.024, -1.072
rt = [V(xe, SY0 - 0.02, ze), V(xe, SY1 + 0.02, ze), V(xt, SY1 + 0.02, zt), V(xt, SY0 - 0.02, zt)]
upn = Z + X * ((zt - ze) / (xe - xt))
y.yuz_yon(rt, 'kiremit', upn)
y.yuz_yon([p - Z * 0.008 for p in rt], 'ahsap_koyu', -upn)
y.yuz_yon([rt[0], rt[1], rt[1] - Z * 0.008, rt[0] - Z * 0.008], 'ahsap_koyu', X)
y.yuz_yon([rt[3], rt[2], rt[2] - Z * 0.008, rt[3] - Z * 0.008], 'ahsap_koyu', -X)
y.yuz_yon([rt[0], rt[3], rt[3] - Z * 0.008, rt[0] - Z * 0.008], 'ahsap_koyu', -Y)
y.yuz_yon([rt[1], rt[2], rt[2] - Z * 0.008, rt[1] - Z * 0.008], 'ahsap_koyu', Y)
cubuk(y, rt[0] + V(-0.004, 0, 0.004), rt[1] + V(-0.004, 0, 0.004), 0.007, 'kiremit2', 0.005)
zroof = lambda x: ze + (zt - ze) * (xe - x) / (xe - xt) - 0.008
for yy_ in (SY0, SY1):   # the gable triangles over the end walls
    q = [V(SX1, yy_, Z0 + SH), V(-1.016, yy_, Z0 + SH), V(-1.016, yy_, zroof(-1.016) + 0.004), V(SX1, yy_, zroof(SX1) + 0.004)]
    y.yuz_yon(q, 'kirec', -Y if yy_ == SY0 else Y)
    q = [V(-1.016, yy_, Z0 + SH + 0.038), V(-1.064, yy_, Z0 + SH + 0.038), V(-1.064, yy_, zroof(-1.064) + 0.004), V(-1.016, yy_, zroof(-1.016) + 0.004)]
    y.yuz_yon(q, 'kirec', -Y if yy_ == SY0 else Y)
# the back wall's outer face carried up under the roof's slope
y.yuz_yon([V(-1.064, SY1, Z0 + SH + 0.03), V(-1.064, SY0, Z0 + SH + 0.03), V(-1.064, SY0, zroof(-1.064) + 0.004), V(-1.064, SY1, zroof(-1.064) + 0.004)],
          'kirec', -X)
# inside: two more striking blocks, sacks of blanks, gold blanks laid out on shelves on the back wall
ors(-0.935, -0.42, 0.0, 'boya_yesil')
ors(-0.935, -0.12, 0.0, 'siva_oker')
for k in range(4):
    kure(y, (-0.995, -0.3 + 0.03 * k, Z0 + 0.016), 0.016, 'kumas' if k % 2 else 'kece', n=8, kat=4)
for k in range(5):
    kutu_merkez(y, (-1.012, -0.5 + 0.11 * k), 0.016, 0.066, 0.005, 'ahsap_koyu', z0=Z0 + 0.083)
for k in range(5):
    for j in range(3):
        yy0 = -0.52 + 0.11 * k + 0.018 * j
        y.yuz_yon([V(-1.0185, yy0, Z0 + 0.088), V(-1.0185, yy0 + 0.012, Z0 + 0.088), V(-1.0185, yy0 + 0.012, Z0 + 0.1), V(-1.0185, yy0, Z0 + 0.1)],
                  'altin', X)

calistir(y, 'lm_darphane')
