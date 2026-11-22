# Kartal Evi (lm_kartalevi): the House of the Eagle Warriors beside the Templo Mayor: an L-plan palace on a talud-tablero
# platform, the stair's balustrades ending in eagle heads, a pillared portico before the main hall, clay eagle warriors at
# the stair head, an upper sanctuary crowned by merlons and a great eagle; behind it the courtyard with painted
# banquettes (the warrior procession frieze), an altar with the eagle vessel, braziers and a sweat bath; a thatched wing.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from aztek_parca import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04
PH = 0.18
ZP = Z0 + PH                     # platform top
PL = [V(-0.92, -0.5), V(0.92, -0.5), V(0.92, 0.92), V(-0.92, 0.92)]
HX0, HX1, HY0, HY1 = -0.8, 0.8, -0.2, 0.07     # main hall walls
HH = 0.22
ZH = ZP + HH                     # hall wall top
WX0, WX1, WY1 = 0.36, 0.8, 0.87               # the wing (from the hall's back wall to WY1)

y.bolum('Zemin: tören alanı')
zemin(y, -1.15, 1.15, -1.1, 1.12, Z0, 'kaya_koyu', 'zemin', basamak=(), silmeli=False)
for (x0, x1, y0, y1, k) in ((-1.1, -0.98, -1.05, 1.05, 'cimen'), (0.98, 1.1, -1.05, 1.05, 'cimen'), (-0.22, 0.22, -1.1, -0.8, 'kirec')):
    y.yuz_yon([V(x0, y0, Z0 + 0.002), V(x1, y0, Z0 + 0.002), V(x1, y1, Z0 + 0.002), V(x0, y1, Z0 + 0.002)], k, Z)

# ---------------- platform and stair ----------------
y.bolum('Talud-tablero kaide')
tb, _ = talud_tablero(y, PL, Z0, PH, talud=0.5, ins=0.05, key='kirec', tablero_key='boya_kirmizi', ust_key='zemin',
                      cerceve_key='boya_sari', disk=('beyaz', 'siva', 0.11))
YS = PL[0].y + 0.04
YB = YS - 0.3
y.bolum('Kartal başlı merdiven')
ayak = alfarda_merdiven(y, 0.0, YB, YS, Z0, ZP, 0.32, n=9, key='kirec', alfarda_key='siva', alfarda_en=0.05, dado=0.22, dado_h=0.04)
for p in ayak:
    kutu_merkez(y, (p.x, p.y - 0.004), 0.05, 0.06, 0.05, 'siva', z0=Z0)
    kartal_bas(y, V(p.x, p.y - 0.03, Z0 + 0.075), V(0, -1), 0.11, 'siva_oker', 'boya_sari', 'koyu', 'ahsap')
for sx in (-1, 1):   # painted bands on the dados
    x0 = sx * (0.16 + 0.025)
    kutu_merkez(y, (x0, YS - 0.0045), 0.051, 0.006, 0.02, 'boya_kirmizi', z0=ZP + 0.01)

# ---------------- main hall ----------------
y.bolum('Ana salon duvarları')


def pencereler(a, b, n, z0, H, kapi=()):
    """a wall a->b in n bays, each with a small square window high up (bay numbers in kapi: a door)"""
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if k in kapi:
            dikdortgen_acik(y, p, q, z0, H, 0.3, 0.7, 0.0, H * 0.58, ('siva', 'boya_kirmizi', 'kirec', 'koyu'), derin=0.03, cerceve=(0.008, 'boya_sari'))
        else:
            dikdortgen_acik(y, p, q, z0, H, 0.38, 0.62, H * 0.5, H * 0.72, ('siva', 'boya_kirmizi', 'kirec', 'koyu'), derin=0.02, cerceve=(0.006, 'turkuaz'))


# front wall with three doors
fr = [(HX0, -0.34), (-0.34, -0.1), (-0.1, 0.1), (0.1, 0.34), (0.34, HX1)]
for i, (u0, u1) in enumerate(fr):
    if i in (1, 3) or i == 2:
        w = u1 - u0
        dikdortgen_acik(y, V(u0, HY0), V(u1, HY0), ZP, HH, 0.5 - 0.06 / w, 0.5 + 0.06 / w if i != 2 else 0.5 + 0.06 / w, 0.0, 0.13 if i != 2 else 0.15,
                        ('siva', 'boya_kirmizi', 'kirec', 'koyu'), derin=0.035, cerceve=(0.01, 'boya_sari'))
    else:
        duz_duvar(y, V(u0, HY0), V(u1, HY0), ZP, ZH, 'siva')
pencereler(V(HX1, HY0), V(HX1, HY1), 2, ZP, HH)
pencereler(V(WX0, HY1), V(HX0, HY1), 6, ZP, HH, kapi=(1, 4))
pencereler(V(HX0, HY1), V(HX0, HY0), 2, ZP, HH)
hall = dikdortgen(HX0, HX1, HY0, HY1)
silme(y, hall, ZP, 0.035, 0.004, 'boya_kirmizi')
# an eagle head over the middle door
kartal_bas(y, V(0, HY0 - 0.02, ZP + 0.185), V(0, -1), 0.075, 'siva_oker', 'boya_sari', 'koyu', 'ahsap')

y.bolum('Revak sütunları')
PY = -0.4
NP = 9
for i in range(NP):
    x = -0.76 + 1.52 * i / (NP - 1)
    kutu_merkez(y, (x, PY), 0.06, 0.06, 0.02, 'kirec', z0=ZP)
    kutu_merkez(y, (x, PY), 0.044, 0.044, HH - 0.045, 'boya_kirmizi', z0=ZP + 0.02)
    for zz in (0.06, 0.14):
        kutu_merkez(y, (x, PY), 0.048, 0.048, 0.012, 'turkuaz', z0=ZP + zz)
    y.oculus(V(x, PY - 0.022, ZP + 0.105), X, -Y, 0.012, 'beyaz', 'boya_sari', f=0.003, k=10)
    kutu_merkez(y, (x, PY), 0.064, 0.064, 0.025, 'kirec', z0=ZH - 0.025)

y.bolum('Çatı, saçak frizi ve almenalar')
RX0, RX1, RY0, RY1 = HX0 - 0.03, HX1 + 0.03, PY - 0.045, HY1 + 0.02
ZR = ZH + 0.035
kutu(y, V(RX0, RY0, ZH), X, RX1 - RX0, RY1 - RY0, 0.035, 'siva', 'onarkasagsol')
y.yuz_yon([V(p.x, p.y, ZR) for p in dikdortgen(RX0, RX1, RY0, RY1)], 'zemin', Z)
silme(y, dikdortgen(RX0, RX1, RY0, RY1), ZH + 0.004, 0.022, 0.003, 'boya_kirmizi')
for i in range(4):   # white discs on the red fascia
    a, b = dikdortgen(RX0, RX1, RY0, RY1)[i], dikdortgen(RX0, RX1, RY0, RY1)[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    m = int(L / 0.06)
    for k in range(m):
        p = a.lerp(b, (k + 0.5) / m)
        if i == 2 and p.x > WX0 - 0.05: continue      # (under the wing's roof)
        y.oculus(p + nn * 0.0035 + Z * (ZH + 0.015), e, nn, 0.0065, 'beyaz', 'boya_sari', f=0.002, k=8)
rk = dikdortgen(RX0, RX1, RY0, RY1)
almenalar(y, rk[0], rk[1], ZR, 0.04, 0.01, 'siva', bosluk=0.035)
almenalar(y, rk[1], rk[2], ZR, 0.04, 0.01, 'siva', bosluk=0.035)
almenalar(y, rk[3], rk[0], ZR, 0.04, 0.01, 'siva', bosluk=0.035)
almenalar(y, V(WX0 - 0.02, RY1), rk[3], ZR, 0.04, 0.01, 'siva', bosluk=0.035)

# ---------------- upper sanctuary ----------------
y.bolum('Üst tapınak')
UX0, UX1, UY0, UY1 = -0.5, 0.5, -0.2, 0.06
UH = 0.24
ZU = ZR + UH
dikdortgen_acik(y, V(UX0, UY0), V(UX1, UY0), ZR, UH, 0.44, 0.56, 0.0, 0.15, ('siva', 'boya_kirmizi', 'kirec', 'koyu'), derin=0.03,
                cerceve=(0.012, 'turkuaz'))
for (a, b) in ((V(UX1, UY0), V(UX1, UY1)), (V(UX1, UY1), V(UX0, UY1)), (V(UX0, UY1), V(UX0, UY0))):
    duz_duvar(y, a, b, ZR, ZU, 'siva')
uk = dikdortgen(UX0, UX1, UY0, UY1)
silme(y, uk, ZR, 0.04, 0.004, 'boya_kirmizi')
silme(y, uk, ZU - 0.04, 0.025, 0.004, 'turkuaz')
# carved panels with warrior shields: flanking the door, on both ends and along the back
def kalkan_pano(cx, cy, aci):
    with parca(y, (cx, cy, 0), aci):
        kutu(y, V(-0.06, -0.006, ZR + 0.05), X, 0.12, 0.006, 0.09, 'boya_sari', 'onsagsolust')
        y.oculus(V(0, -0.0065, ZR + 0.095), X, -Y, 0.03, 'turkuaz', 'boya_kirmizi', f=0.006, k=14)
        y.oculus(V(0, -0.0085, ZR + 0.095), X, -Y, 0.012, 'beyaz', 'koyu', f=0.003, k=10)
        for k in range(5):   # the feathers round the shield
            t = math.pi * (0.15 + 0.7 * k / 4)
            p = V(0.042 * math.cos(t + math.pi), -0.007, ZR + 0.095 - 0.042 * math.sin(t))
            boru(y, [p, p + V(-0.012 * math.cos(t), 0, -0.022 * math.sin(t))], 0.005, 'boya_yesil' if k % 2 else 'boya_kirmizi', n=4, r_son=0.002)


for sx in (-1, 1):
    kalkan_pano(sx * 0.3, UY0, 0.0)
    kalkan_pano(UX1 if sx > 0 else UX0, (UY0 + UY1) / 2, sx * math.pi / 2)
for xc in (-0.3, 0.0, 0.3):
    kalkan_pano(xc, UY1, math.pi)
kutu(y, V(UX0 - 0.025, UY0 - 0.025, ZU), X, UX1 - UX0 + 0.05, UY1 - UY0 + 0.05, 0.025, 'siva', 'onarkasagsol')
silme(y, dikdortgen(UX0 - 0.025, UX1 + 0.025, UY0 - 0.025, UY1 + 0.025), ZU + 0.004, 0.016, 0.003, 'boya_kirmizi')
# the shrine roof of the codices: a tall striped truncated pyramid, merlons round its top
UC = ((UX0 + UX1) / 2, (UY0 + UY1) / 2)
w0, d0 = UX1 - UX0 + 0.05, UY1 - UY0 + 0.05
ZK = ZU + 0.025 + 0.17
kesik_piramit(y, UC, w0, d0, w0 * 0.78, d0 * 0.42, ZU + 0.025, ZK, 'boya_kirmizi')
# rows of white jade roundels lying on the slopes, a turquoise band at the foot
alt_ = dikdortgen(UC[0] - w0 / 2, UC[0] + w0 / 2, UC[1] - d0 / 2, UC[1] + d0 / 2, ZU + 0.025)
ust_ = dikdortgen(UC[0] - w0 * 0.39, UC[0] + w0 * 0.39, UC[1] - d0 * 0.21, UC[1] + d0 * 0.21, ZK)
for i in range(4):
    j = (i + 1) % 4
    e = (alt_[j] - alt_[i]).normalized()
    t = ((ust_[i] + ust_[j]) / 2 - (alt_[i] + alt_[j]) / 2).normalized()
    n = e.cross(t).normalized()
    if n.z < 0: n = -n
    # the band at the foot
    q = [alt_[i], alt_[j], alt_[j].lerp(ust_[j], 0.14), alt_[i].lerp(ust_[i], 0.14)]
    y.yuz_yon([p + n * 0.0015 for p in q], 'turkuaz', n)
    # a carved frieze between two white bands: two staggered rows of small round shields (chimalli) with a dark boss
    Ls = lambda s: (alt_[i].lerp(ust_[i], s), alt_[j].lerp(ust_[j], s))
    for sa, sb in ((0.3, 0.345), (0.775, 0.82)):
        a0, b0 = Ls(sa); a1, b1 = Ls(sb)
        y.yuz_yon([p + n * 0.0012 for p in (a0, b0, b1, a1)], 'beyaz', n)
    for row, s in enumerate((0.46, 0.66)):
        a_, b_ = Ls(s)
        m = max(2, int((b_ - a_).length / 0.045))
        for k in range(m - row):
            c = a_.lerp(b_, (k + 0.5 + 0.5 * row) / m) + n * 0.0015
            r = 0.0115
            y.yuz_yon([c + (e * math.cos(TAU * u / 10) + t * math.sin(TAU * u / 10)) * r for u in range(10)], 'beyaz', n)
            y.yuz_yon([c + n * 0.0006 + (e * math.cos(TAU * u / 6) + t * math.sin(TAU * u / 6)) * r * 0.38 for u in range(6)], 'turkuaz', n)
kornis(y, UC[0] - w0 * 0.39, UC[0] + w0 * 0.39, UC[1] - d0 * 0.21, UC[1] + d0 * 0.21, ZK - 0.012, 0.012, 0.006, 'turkuaz')
almena_halka(y, dikdortgen(UC[0] - w0 * 0.39, UC[0] + w0 * 0.39, UC[1] - d0 * 0.21, UC[1] + d0 * 0.21), ZK, 0.05, 0.01, 'siva', bosluk=0.02)
y.bolum('Büyük kartal')
kutu_merkez(y, UC, 0.14, d0 * 0.4, 0.03, 'bazalt', z0=ZK)
kartal(y, UC[0], UC[1], ZK + 0.03, 0.34, -math.pi / 2, taban=None)

# ---------------- eagle warriors, braziers, banners on the platform ----------------
y.bolum('Kartal savaşçıları')
for sx in (-1, 1):
    kartal_savasci(y, sx * 0.285, -0.415, ZP, 0.2, -math.pi / 2, tuy='kiremit2')
for sx in (-1, 1):
    mangal(y, sx * 0.62, -0.44, ZP, 0.08)
    mangal(y, sx * 0.64, -0.3, ZR, 0.07)

# ---------------- the wing ----------------
y.bolum('Yan kanat (kışla)')
ZW = ZP + 0.2
wk = [V(WX0, HY1), V(WX1, HY1), V(WX1, WY1), V(WX0, WY1)]
pencereler(wk[1], wk[2], 5, ZP, 0.2)
pencereler(wk[2], wk[3], 3, ZP, 0.2)
# the courtyard side: three doors
for k in range(3):
    a = V(WX0, WY1).lerp(V(WX0, HY1), k / 3); b = V(WX0, WY1).lerp(V(WX0, HY1), (k + 1) / 3)
    dikdortgen_acik(y, a, b, ZP, 0.2, 0.38, 0.62, 0.0, 0.12, ('siva', 'boya_kirmizi', 'kirec', 'koyu'), derin=0.03, cerceve=(0.008, 'boya_sari'))
silme(y, [wk[1], wk[2], wk[3]], ZP, 0.03, 0.004, 'boya_kirmizi', kapali=False)
silme(y, [wk[1], wk[2], wk[3], wk[0]], ZW - 0.03, 0.02, 0.004, 'turkuaz', kapali=False)
saz_cati(y, WX0, WX1, HY1, WY1, ZW, 0.2, sacak=0.04, nr=8, kalin=0.02, besik=True)

# ---------------- courtyard ----------------
y.bolum('Avlu: boyalı sıralar')
CX0, CY1 = -0.845, 0.845
# a low wall with merlons round the open sides
for a, b in ((V(CX0, HY1 + 0.03), V(CX0, CY1)), (V(CX0, CY1), V(WX0, CY1))):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    kutu(y, a - nn * 0.0 + Z * ZP, e, (b - a).length, 0.035, 0.06, 'siva')
    almenalar(y, a, b, ZP + 0.06, 0.032, 0.008, 'siva', bosluk=0.04)
# banquettes with the warrior procession: along the north wall (facing the front) and the wing (facing west)
BH = 0.05
BD = 0.05                         # bench depth
kutu(y, V(CX0 + BD, CY1 - BD, ZP), X, WX0 - CX0 - 2 * BD, BD, BH, 'siva_oker', 'onust')
alay_frizi(y, V(CX0 + BD, CY1 - BD), V(WX0 - BD, CY1 - BD), ZP, BH * 0.92)
kapilar = [WY1 - (k + 0.5) * (WY1 - HY1) / 3 for k in range(3)]
lo_all, hi_all = HY1 + 0.04, CY1
segs, cur = [], lo_all
for a_, b_ in sorted((c - 0.045, c + 0.045) for c in kapilar):   # (the bench stops at the doors)
    if a_ > cur: segs.append((cur, min(a_, hi_all)))
    cur = max(cur, b_)
if cur < hi_all: segs.append((cur, hi_all))
for lo, hi in segs:
    if hi - lo > 0.03:
        kutu(y, V(WX0 - BD, hi, ZP), -Y, hi - lo, BD, BH, 'siva_oker', 'onustsag' + ('sol' if hi < CY1 - 1e-6 else ''))
        alay_frizi(y, V(WX0 - BD, min(hi, CY1 - BD)), V(WX0 - BD, lo), ZP, BH * 0.92)
kutu(y, V(CX0 + BD, HY1 + 0.03, ZP), Y, CY1 - HY1 - 0.03, BD, BH, 'siva_oker', 'onustsol')
alay_frizi(y, V(CX0 + BD, HY1 + 0.03), V(CX0 + BD, CY1 - BD), ZP, BH * 0.92)
y.bolum('Avlu: sunak ve kartal kabı')
AC = V(-0.26, 0.5)
talud_tablero(y, dikdortgen(AC.x - 0.12, AC.x + 0.12, AC.y - 0.12, AC.y + 0.12), ZP, 0.07, talud=0.45, ins=0.02, key='kirec',
              tablero_key='boya_kirmizi', ust_key='kirec', cerceve_key='boya_sari')
# cuauhxicalli: a stone eagle carrying a bowl on its back
with parca(y, (AC.x, AC.y, ZP + 0.07), -math.pi / 2):
    elipsoid(y, (0, 0, 0.04), (0.06, 0.045, 0.04), 'siva_oker', n=10, kat=5)
    for s in (-1, 1):   # folded wings along the flanks
        elipsoid(y, (-0.01, s * 0.04, 0.045), (0.055, 0.012, 0.028), 'kiremit', n=8, kat=4)
    donel(y, (-0.01, 0), [(0.035, 0.06), (0.045, 0.085), (0.04, 0.088), (0.0, 0.08)], 'bazalt', n=12)
    halka_kornis(y, (-0.01, 0), 0.044, 0.078, 0.005, 0.002, 12, 'boya_kirmizi')
    kartal_bas(y, V(0.06, 0, 0.07), V(1, 0), 0.07, 'siva_oker', 'boya_sari', 'koyu', 'kiremit')
for (x, yy) in ((-0.68, 0.16), (-0.68, 0.72), (0.18, 0.72)):
    mangal(y, x, yy, ZP, 0.08)
y.bolum('Avlu: buhar banyosu (temazcal) ve ağaçlar')
TC = V(-0.6, 0.55)
elipsoid(y, (TC.x, TC.y, ZP), (0.1, 0.09, 0.08), 'kerpic', n=14, kat=8, ust_yarim=True)
y.prizma((TC.x, TC.y + 0.075), 0.012, ZP + 0.04, ZP + 0.1, 'kerpic_koyu', n=6)
# the low entrance tunnel with its dark door, a woodpile for the fire
kutu_merkez(y, (TC.x, TC.y - 0.085), 0.07, 0.06, 0.055, 'kerpic', z0=ZP)
y.yuz_yon([V(TC.x - 0.02, TC.y - 0.1155, ZP), V(TC.x + 0.02, TC.y - 0.1155, ZP), V(TC.x + 0.02, TC.y - 0.1155, ZP + 0.04), V(TC.x - 0.02, TC.y - 0.1155, ZP + 0.04)], 'koyu', -Y)
for k in range(4):
    cubuk(y, V(TC.x + 0.11, TC.y - 0.06 + k * 0.012, ZP + 0.006 + (k % 2) * 0.01), V(TC.x + 0.17, TC.y - 0.06 + k * 0.012, ZP + 0.006 + (k % 2) * 0.01), 0.01, 'ahsap')
for (x, yy, b) in ((-0.05, 0.75, 0.2), (-0.55, 0.25, 0.17)):
    y.prizma((x, yy), 0.035, ZP, ZP + 0.03, 'kirec', n=10)
    agac(y, x, yy, ZP + 0.03, b, 'yapraklı', 'boya_yesil')

# ---------------- outside the platform ----------------
y.bolum('Meydan: sancaklar, ağaçlar')
for sx in (-1, 1):
    sancak(y, sx * 0.3, -0.92, Z0, boy=0.42, en=0.12, yuk=0.075, aci=-math.pi / 2 - sx * 0.5, direk_key='ahsap_koyu', kuyruk=True)
    sancak(y, sx * 0.78, -0.33, ZR, boy=0.28, en=0.09, yuk=0.055, aci=math.pi / 2 + sx * 0.6, direk_key='ahsap_koyu')
    mangal(y, sx * 0.5, -0.85, Z0, 0.1)
for (x, yy, b, kk) in ((-1.04, -0.9, 0.24, 'boya_yesil'), (1.04, -0.9, 0.24, 'yesil_koyu'), (-1.04, 0.0, 0.22, 'yesil_koyu'), (1.04, 0.05, 0.22, 'boya_yesil'),
                       (-1.04, 0.85, 0.24, 'boya_yesil'), (1.04, 0.85, 0.24, 'yesil_koyu')):
    agac(y, x, yy, Z0, b, 'yapraklı', kk)

calistir(y, 'lm_kartalevi')
