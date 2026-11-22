# Tanit Tapınağı (lm_tanit): the sanctuary of Tanit and Baal Hammon: a Punic temple on a high podium (Ionic porch,
# Egyptian cavetto cornices, an Egyptian door frame under the winged sun, a bronze sign of Tanit on the roof, two
# free-standing pillars), an altar with its fire before the stair, colonnades round the court, the Tophet (rows of
# stelae carved with the sign of Tanit, urns before them) in its own enclosure, a sacred grove with a betyl shrine,
# priests in procession, and a pylon gate in the temenos wall.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kartaca_ortak import kavetto, KAVETTO, KAVETTO_H, iyon_hafif, tanit_kabartma, tanit_heykel, kanatli_gunes, insan, pencere_kutu
from kartaca_ek import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(3)
B = 1.15
PH = 0.045                       # the temenos platform
TOX0, TOX1, TOY0, TOY1 = -1.06, -0.4, -1.0, -0.12    # the Tophet (unpaved)

# ---------------- the platform ----------------
y.bolum('Platform')
kutu(y, V(-B, -B, 0), X, 2 * B, 2 * B, PH, 'kum_koyu', 'onarkasagsol')
silme(y, dikdortgen(-B, B, -B, B), 0, 0.016, 0.01, 'kum_koyu', 'kaide')
silme(y, dikdortgen(-B, B, -B, B), PH - 0.008, 0.008, 0.006, 'kum_acik', 'duz')
NB = 14
xs = [-B + 2 * B * i / NB for i in range(NB + 1)]
for i in range(NB):
    for j in range(NB):
        x0, x1, y0, y1 = xs[i], xs[i + 1], xs[j], xs[j + 1]
        # (cells split at the Tophet's edges so its earth and the paving meet on a line)
        cx_ = sorted({x0, x1} | {v for v in (TOX0, TOX1) if x0 < v < x1})
        cy_ = sorted({y0, y1} | {v for v in (TOY0, TOY1) if y0 < v < y1})
        for a in range(len(cx_) - 1):
            for b in range(len(cy_) - 1):
                mx, my = (cx_[a] + cx_[a + 1]) / 2, (cy_[b] + cy_[b + 1]) / 2
                key = 'toprak' if (TOX0 < mx < TOX1 and TOY0 < my < TOY1) else 'zemin'
                y.yuz_yon([V(cx_[a], cy_[b], PH), V(cx_[a + 1], cy_[b], PH), V(cx_[a + 1], cy_[b + 1], PH), V(cx_[a], cy_[b + 1], PH)], key, Z)
for k in range(3):   # steps at the front
    hh = PH * (3 - k) / 4
    kutu(y, V(-0.25, -B - 0.03 * (k + 1), 0), X, 0.5, 0.03 * (k + 1) + 0.001, hh, 'kum_koyu', 'onsagsolust')

# ---------------- the temenos wall and the pylon gate ----------------
y.bolum('Temenos duvarı ve kapı')
WT_ = 0.024


def duvar_yol(pts, h, key='kum', bas=None, son=None):
    """a free-standing wall along an open polyline (outer face to the right of travel), WT_ thick, a cavetto cornice on
    both faces; bas / son: the end caps from that height up (None: no cap, the end is buried in something)"""
    o = [V(*p) for p in pts]
    ic = disa(o, -WT_, kapali=False)
    zt = PH + h
    for i in range(len(o) - 1):
        L = (o[i + 1] - o[i]).length
        m = max(1, int(L / 0.2))
        for k in range(m):
            duz_duvar(y, o[i].lerp(o[i + 1], k / m), o[i].lerp(o[i + 1], (k + 1) / m), PH, zt, key)
            duz_duvar(y, ic[i].lerp(ic[i + 1], (k + 1) / m), ic[i].lerp(ic[i + 1], k / m), PH, zt, key)
        y.yuz_yon([o[i] + Z * zt, o[i + 1] + Z * zt, ic[i + 1] + Z * zt, ic[i] + Z * zt], 'kum_acik', Z)
    for idx, z0, s in ((0, bas, -1), (-1, son, 1)):
        if z0 is None: continue
        e = (o[1] - o[0]) if idx == 0 else (o[-1] - o[-2])
        y.yuz_yon([o[idx] + Z * z0, ic[idx] + Z * z0, ic[idx] + Z * zt, o[idx] + Z * zt], key, e * s)
    silme(y, o, zt - 0.016, 0.016, 0.009, 'kum_acik', KAVETTO_H, kapali=False)
    silme(y, ic[::-1], zt - 0.016, 0.016, 0.009, 'kum_acik', KAVETTO_H, kapali=False)


GW = 0.2
WL, WH_ = 0.09, 0.24        # the low front walls, the tall walls behind the colonnades
XW = B - 0.04
duvar_yol([(GW / 2 + 0.12, -XW), (XW, -XW), (XW, 0.02)], WL)
duvar_yol([(XW, 0.02), (XW, XW), (-XW, XW), (-XW, 0.02)], WH_, bas=PH + WL, son=PH + WL)
duvar_yol([(-XW, 0.02), (-XW, -XW), (-GW / 2 - 0.12, -XW)], WL)
# the pylon: two battered towers with cavetto crowns, the gate between them, the winged sun
GY = -B + 0.06
for sx in (-1, 1):
    cx = sx * (GW / 2 + 0.07)
    w0, w1, d0, d1, h = 0.17, 0.13, 0.13, 0.095, 0.42
    alt = dikdortgen(cx - w0 / 2, cx + w0 / 2, GY - d0 / 2, GY + d0 / 2, PH)
    ust = dikdortgen(cx - w1 / 2, cx + w1 / 2, GY - d1 / 2, GY + d1 / 2, PH + h)
    for i in range(4):
        j = (i + 1) % 4
        yuz_dis(y, [alt[i], alt[j], ust[j], ust[i]], 'kum', V(cx, GY, PH + h / 2))
    # the torus roll up the corners (a Egyptian pylon's edge)
    for i in range(4):
        boru(y, [alt[i] + (alt[i] - V(cx, GY, PH)).normalized() * 0.002, ust[i] + (ust[i] - V(cx, GY, PH + h)).normalized() * 0.002], 0.006, 'kum_acik', n=6)
    kavetto(y, [V(p.x, p.y) for p in ust], PH + h, 0.04, 0.022, 'kum_acik')
    on = lambda z: GY - d0 / 2 + (d0 - d1) / 2 * (z - PH) / h        # the battered front face at height z
    tanit_kabartma(y, V(cx, on(PH + 0.27) - 0.002, PH + 0.23), X, -Y, 0.1, 'altin')
    sancak(y, cx, GY, PH + h + 0.04, boy=0.2, en=0.11, yuk=0.07, aci=-0.9)
    for zz in (PH + 0.09, PH + 0.15, PH + 0.205, PH + 0.355):   # painted bands across the front
        boru(y, [V(cx - w0 / 2 + (w0 - w1) / 2 * (zz - PH) / h, on(zz) - 0.001, zz), V(cx + w0 / 2 - (w0 - w1) / 2 * (zz - PH) / h, on(zz) - 0.001, zz)],
             0.004, ('boya_kirmizi', 'turkuaz', 'boya_kirmizi', 'turkuaz')[[PH + 0.09, PH + 0.15, PH + 0.205, PH + 0.355].index(zz)], n=4)
# the gate: lintel block with its own cavetto, the leaves
kutu(y, V(-GW / 2 - 0.01, GY - 0.04, PH + 0.22), X, GW + 0.02, 0.08, 0.08, 'kum', 'onarkasagsol')
kavetto(y, dikdortgen(-GW / 2 - 0.01, GW / 2 + 0.01, GY - 0.04, GY + 0.04), PH + 0.3, 0.034, 0.018, 'kum_acik')
kanatli_gunes(y, V(0, GY - 0.04, PH + 0.26), X, -Y, 0.19, 0.04)
for sx in (-1, 1):   # the open leaves turned back into the court
    kutu_merkez(y, (sx * 0.08, GY + 0.07), 0.012, 0.08, 0.215, 'ahsap', z0=PH)

# ---------------- the colonnades round the court ----------------
y.bolum('Revaklar')
for sx in (-1, 1):
    xw = sx * (XW - WT_ / 2)          # (the roof reaches into the tall wall)
    xc = sx * (B - 0.2)
    y0, y1 = 0.06, XW - WT_ / 2
    hh = 0.17
    xin = sx * (XW - WT_)
    w0 = [V(xin, y0), V(xin, y1)] if sx < 0 else [V(xin, y1), V(xin, y0)]
    n = 8
    for k in range(n + 1):
        yy = y0 + 0.03 + (y1 - y0 - 0.06) * k / n
        iyon_hafif(y, xc, yy, PH, PH + hh - 0.025, 0.011, 'siva', 'siva_krem', aci=0.0)
    xa, xb = (xc - 0.025, xw) if sx > 0 else (xw, xc + 0.025)
    kutu(y, V(xa, y0, PH + hh - 0.025), X, xb - xa, y1 - y0, 0.025, 'siva_krem', 'onarkasagsol')
    kavetto(y, dikdortgen(xa, xb, y0, y1), PH + hh, 0.03, 0.016, 'siva_krem')
    y.yuz_yon([V(xa, y0, PH + hh - 0.025), V(xb, y0, PH + hh - 0.025), V(xb, y1, PH + hh - 0.025), V(xa, y1, PH + hh - 0.025)], 'siva_krem', -Z)
    # painted doors in the back wall
    for k in range(3):
        a, b = w0[0], w0[1]
        e = (b - a).normalized(); nrm = V(e.y, -e.x)
        pencere_kutu(y, a, e, nrm, (y1 - y0) * (k + 0.5) / 3 - 0.02, 0.0, 0.04, 0.085, 'ahsap_koyu', cerceve='kum_acik')

# ---------------- the temple ----------------
y.bolum('Tapınak')
PX0, PX1, PY0, PY1, PDH = -0.46, 0.46, 0.08, 0.98, 0.3
PT = PH + PDH
kutu(y, V(PX0, PY0, PH), X, PX1 - PX0, PY1 - PY0, PDH, 'kum', 'onarkasagsol')
silme(y, dikdortgen(PX0, PX1, PY0, PY1), PH, 0.04, 0.018, 'kum_koyu', 'kaide')
silme(y, dikdortgen(PX0, PX1, PY0, PY1), PH + PDH * 0.55, 0.012, 0.008, 'kum_acik', 'yarim')
kavetto(y, dikdortgen(PX0, PX1, PY0, PY1), PT - 0.04, 0.04, 0.02, 'kum_acik', ust=False)
for i in range(6):
    for j in range(6):
        xa, xb = PX0 + (PX1 - PX0) * i / 6, PX0 + (PX1 - PX0) * (i + 1) / 6
        ya, yb = PY0 + (PY1 - PY0) * j / 6, PY0 + (PY1 - PY0) * (j + 1) / 6
        y.yuz_yon([V(xa, ya, PT), V(xb, ya, PT), V(xb, yb, PT), V(xa, yb, PT)], 'mermer', Z)
# relief panels on the podium front: the sign of Tanit between rosettes
for sx in (-1, 1):
    tanit_kabartma(y, V(sx * 0.33, PY0, PH + 0.06), X, -Y, 0.1, 'altin')
# the stair up the podium, with cheek walls
merdiven(y, (0, PY0 - 0.294), math.pi / 2, 0.38, PH, PT, n=17, d=0.3 / 17, key='kum_acik')
for sx in (-1, 1):
    x = sx * 0.205
    p0, p1 = V(x - 0.012, PY0 - 0.3), V(x + 0.012, PY0 - 0.3)
    q = [V(x - 0.012, PY0 - 0.3, PH), V(x + 0.012, PY0 - 0.3, PH), V(x + 0.012, PY0 + 0.006, PH), V(x - 0.012, PY0 + 0.006, PH)]
    top = [V(x - 0.012, PY0 - 0.3, PH + 0.04), V(x + 0.012, PY0 - 0.3, PH + 0.04), V(x + 0.012, PY0 + 0.006, PT + 0.01), V(x - 0.012, PY0 + 0.006, PT + 0.01)]
    for i in range(4):
        j = (i + 1) % 4
        yuz_dis(y, [q[i], q[j], top[j], top[i]], 'kum', V(x, PY0 - 0.15, PH + 0.1))
    y.yuz_yon(top, 'kum_acik', Z)
    # bronze incense burners on the cheek ends
    donel(y, (x, PY0 - 0.29), [(0.01, PH + 0.04), (0.006, PH + 0.06), (0.012, PH + 0.075), (0.014, PH + 0.08), (0.0, PH + 0.082)], 'bronz', n=8)
# the cella
CX0, CX1, CY0, CY1 = -0.32, 0.32, 0.34, 0.92
ZC = PT + 0.4                # column tops
ZE = ZC + 0.05               # the entablature's top, the cornice's foot
dikdortgen_acik(y, V(CX0, CY0), V(CX1, CY0), PT, ZE - PT, 0.36, 0.64, 0.0, 0.3, ('kum_acik', 'kum', 'mermer', 'ahsap_koyu'), derin=0.03,
                cerceve=(0.014, 'mermer'), ic_kenar=True)
duz_duvar(y, V(CX1, CY0), V(CX1, CY1), PT, ZE, 'kum_acik')
duz_duvar(y, V(CX1, CY1), V(CX0, CY1), PT, ZE, 'kum_acik')
duz_duvar(y, V(CX0, CY1), V(CX0, CY0), PT, ZE, 'kum_acik')
# the Egyptian door: a cavetto lintel over the frame, the winged sun above it
silme(y, [V(-0.13, CY0), V(0.13, CY0)], PT + 0.314, 0.032, 0.02, 'mermer', KAVETTO, kapali=False)
kanatli_gunes(y, V(0, CY0, PT + 0.38), X, -Y, 0.2, 0.026)
# pilasters on the cella's sides and back
for (a, b) in ((V(CX1, CY0), V(CX1, CY1)), (V(CX1, CY1), V(CX0, CY1)), (V(CX0, CY1), V(CX0, CY0))):
    L = (b - a).length; e = (b - a) / L
    m = 4
    for k in range(1, m):
        p = a.lerp(b, k / m)
        kutu(y, p - e * 0.014 + Z * PT, e, 0.028, -0.01, ZC - PT, 'kum', 'arkasagsolust')
    for k in range(m):   # tall narrow windows of the cella between the pilasters, framed in marble
        pencere_kutu(y, a + Z * PT, e, V(e.y, -e.x), L * (k + 0.5) / m - 0.012, (ZC - PT) * 0.42, 0.024, 0.1, 'koyu', cerceve='mermer')
# the porch: Ionic columns, the architrave over them
for x in (-0.27, -0.09, 0.09, 0.27):
    sutun(y, x, 0.18, PT, ZC, 0.024, 'mermer', 'iyon', yiv=16)
kutu(y, V(CX0, 0.145, ZC), X, CX1 - CX0, CY0 - 0.145, ZE - ZC, 'kum_acik', 'onsagsol')
y.yuz_yon([V(CX0, 0.145, ZC), V(CX1, 0.145, ZC), V(CX1, CY0, ZC), V(CX0, CY0, ZC)], 'kum_acik', -Z)
for k in range(9):   # the frieze's painted rosettes
    x = CX0 + 0.04 + (CX1 - CX0 - 0.08) * k / 8
    kure(y, (x, 0.145 - 0.001, ZC + 0.026), 0.008, 'boya_kirmizi' if k % 2 else 'altin', n=6, kat=3)
# the cavetto crown, a uraeus-like crest of small stepped merlons, the roof
kavetto(y, dikdortgen(CX0, CX1, 0.145, CY1), ZE, 0.06, 0.034, 'kum_acik')
ZR = ZE + 0.06
ring = disa(dikdortgen(CX0, CX1, 0.145, CY1), 0.03)
parapet(y, ring, ZR, 0.008, 0.024, 0.014, 'kum_acik')
# the bronze sign of Tanit over the front, incense altars at the corners
tanit_heykel(y, 0, 0.2, ZR + 0.016, 0.26, 'bronz', aci=-math.pi / 2, kalin=0.022)
donel(y, (0, 0.2), [(0.062, ZR), (0.062, ZR + 0.012), (0.045, ZR + 0.016), (0.0, ZR + 0.016)], 'kum_acik', n=12)
for sx in (-1, 1):
    for yy in (0.2, CY1 - 0.06):
        donel(y, (sx * 0.27, yy), [(0.018, ZR), (0.014, ZR + 0.03), (0.02, ZR + 0.04), (0.0, ZR + 0.042)], 'kum_acik', n=8)
        donel(y, (sx * 0.27, yy), [(0.008, ZR + 0.042), (0.004, ZR + 0.056), (0.0, ZR + 0.066)], 'boya_kirmizi', n=6)
# the raised adyton over the holy of holies at the back of the roof, a false door on its front
AX0, AX1, AY0, AY1 = -0.2, 0.2, 0.48, 0.84
duvarlar(y, dikdortgen(AX0, AX1, AY0, AY1), ZR, ZR + 0.15, 'kum_acik')
kavetto(y, dikdortgen(AX0, AX1, AY0, AY1), ZR + 0.15, 0.04, 0.022, 'kum_acik')
parapet(y, disa(dikdortgen(AX0, AX1, AY0, AY1), 0.019), ZR + 0.19, 0.006, 0.02, 0.012, 'kum_acik')
pencere_kutu(y, V(AX0, AY0), X, -Y, 0.16, 0.0, 0.08, 0.11, 'ahsap_koyu', cerceve='mermer')
kanatli_gunes(y, V(0, AY0, ZR + 0.13), X, -Y, 0.15, 0.016)
for sx in (-1, 1):
    tanit_kabartma(y, V(sx * 0.13, AY0, ZR + 0.02), X, -Y, 0.09, 'altin')
# on the adyton's roof: the disc and crescent of Tanit and Baal Hammon on a pole, horned incense altars at the corners
ZA = ZR + 0.19
AYM = (AY0 + AY1) / 2
y.prizma((0, AYM), 0.035, ZA, ZA + 0.02, 'kum_acik', n=10)
y.prizma((0, AYM), 0.004, ZA + 0.02, ZA + 0.13, 'bronz', n=6)
kure(y, (0, AYM, ZA + 0.15), 0.02, 'altin', n=12, kat=6)
boru(y, [V(0.03 * math.cos(math.pi * k / 8), AYM, ZA + 0.15 - 0.032 * math.sin(math.pi * k / 8)) for k in range(9)], 0.005, 'altin', n=5)
for sx in (-1, 1):
    for yy in (AY0 + 0.04, AY1 - 0.04):
        kutu_merkez(y, (sx * (AX1 - 0.04), yy), 0.03, 0.03, 0.025, 'kum_acik', z0=ZA)
        for cx_, cy_ in ((-0.011, -0.011), (0.011, -0.011), (0.011, 0.011), (-0.011, 0.011)):
            donel(y, (sx * (AX1 - 0.04) + cx_, yy + cy_), [(0.004, ZA + 0.025), (0.0, ZA + 0.036)], 'kum_acik', n=4)
# the two free-standing pillars before the porch (gold capitals)
for sx in (-1, 1):
    x, yy = sx * 0.4, 0.15
    y.prizma((x, yy), 0.03, PT, PT + 0.02, 'kum_acik', n=12, kat=0)
    donel(y, (x, yy), [(0.021, PT + 0.02), (0.019, PT + 0.4), (0.026, PT + 0.41)], 'turkuaz' if sx < 0 else 'boya_kirmizi', n=12)
    donel(y, (x, yy), [(0.026, PT + 0.41), (0.034, PT + 0.435), (0.03, PT + 0.45), (0.02, PT + 0.455), (0.0, PT + 0.456)], 'altin', n=12)
    kure(y, (x, yy, PT + 0.478), 0.028, 'altin', n=12, kat=6)
    donel(y, (x, yy), [(0.0, PT + 0.505), (0.006, PT + 0.51), (0.0, PT + 0.54)], 'altin', n=6)

# winged sphinxes guarding the stair, a painted band round the cella under the cornice
for sx in (-1, 1):
    sfenks(y, sx * 0.3, PY0 - 0.27, PH, -math.pi / 2, 1.35, 'kum_acik', 'altin', 'kum')
silme(y, [V(CX1, CY0), V(CX1, CY1), V(CX0, CY1), V(CX0, CY0)], ZC + 0.012, 0.014, 0.003, 'turkuaz', 'duz', kapali=False)
silme(y, [V(CX1, CY0), V(CX1, CY1), V(CX0, CY1), V(CX0, CY0)], ZC + 0.004, 0.006, 0.003, 'boya_kirmizi', 'duz', kapali=False)

# ---------------- the altar and the procession ----------------
y.bolum('Sunak ve rahipler')
AX, AY = 0.0, -0.48
for k, (w, d, h) in enumerate(((0.24, 0.18, 0.02), (0.2, 0.14, 0.07), (0.23, 0.17, 0.016))):
    z0 = PH + (0, 0.02, 0.09)[k]
    kutu_merkez(y, (AX, AY), w, d, h, 'kum' if k == 1 else 'kum_acik', z0=z0)
zt = PH + 0.106
for sx in (-1, 1):   # the horned corners
    for sy in (-1, 1):
        c = V(AX + sx * 0.1, AY + sy * 0.07)
        donel(y, (c.x, c.y), [(0.012, zt), (0.0, zt + 0.03)], 'kum_acik', n=4, kat=math.pi / 4)
tanit_kabartma(y, V(AX, AY - 0.07, PH + 0.03), X, -Y, 0.055, 'altin')
ates(y, AX, AY, zt, 0.035, tohum=4, duman_n=4)
# priests in white with tall caps, worshippers bringing offerings
for k, (x, yy, a) in enumerate(((0.14, -0.48, math.pi), (-0.14, -0.48, 0.0), (0.0, -0.65, math.pi / 2),
                                 (0.0, -0.8, math.pi / 2), (0.05, -0.92, math.pi / 2), (-0.05, -1.0, math.pi / 2))):
    insan(y, x, yy, PH, 'beyaz', s=1.25, aci=a, kol=0.8 if k < 2 else 0.0, sapka='beyaz' if k < 4 else None)
for k, (x, yy) in enumerate(((0.12, 0.0), (-0.12, -0.02), (0.08, -0.25), (-0.1, -0.3))):
    insan(y, x, yy, PH, ['mor', 'boya_kirmizi', 'kumas', 'siva_oker'][k], s=1.2, aci=math.pi / 2, kol=0.5)
insan(y, 0.0, PY0 + 0.24, PT, 'beyaz', s=1.25, aci=-math.pi / 2, kol=1.0, sapka='beyaz')

# the paved processional way: raised slabs of pale stone from the gate to the stair, round the altar
for k in range(14):
    y0_ = -1.07 + k * 0.061
    if abs(y0_ + 0.03 - AY) < 0.12: continue
    kutu(y, V(-0.1, y0_, PH), X, 0.2, 0.055, 0.004, 'kum_acik', 'onarkasagsolust')

# the processional way: bronze incense stands from the gate to the altar, palms and offering tables in the court
for k in range(4):
    yy = -0.95 + k * 0.105
    for sx in (-1, 1):
        x = sx * 0.17
        kutu_merkez(y, (x, yy), 0.03, 0.03, 0.012, 'kum_koyu', z0=PH)
        donel(y, (x, yy), [(0.006, PH + 0.012), (0.005, PH + 0.06), (0.014, PH + 0.072), (0.016, PH + 0.078), (0.012, PH + 0.078),
                           (0.0, PH + 0.074)], 'bronz', n=8)
        kure(y, (x, yy, PH + 0.085), 0.006, 'boya_kirmizi', n=6, kat=3)
for sx in (-1, 1):
    for yy in (0.12, 0.42, 0.72):
        x = sx * 0.66
        kutu_merkez(y, (x, yy), 0.06, 0.06, 0.02, 'kum_acik', z0=PH)
        agac(y, x, yy, PH + 0.02, 0.24, 'palmiye', 'zeytin', 'ahsap')
    for yy in (0.27, 0.57):   # offering tables with bowls and jars
        x = sx * 0.66
        kutu_merkez(y, (x, yy), 0.07, 0.045, 0.004, 'mermer', z0=PH + 0.034)
        for dx in (-0.025, 0.025):
            y.prizma((x + dx, yy), 0.004, PH, PH + 0.034, 'mermer', n=6, ust=False)
        donel(y, (x - 0.015, yy), [(0.004, PH + 0.038), (0.01, PH + 0.043), (0.0, PH + 0.044)], 'bronz', n=8)
        urn(y, x + 0.016, yy, PH + 0.038, 0.9, 'kiremit')
for k, (x, yy, a) in enumerate(((-0.6, 0.3, 0.3), (0.62, 0.5, 2.8), (0.55, 0.15, -2.6))):
    insan(y, x, yy, PH, ['beyaz', 'mor', 'beyaz'][k], s=1.2, aci=a, kol=0.4, sapka='beyaz' if k != 1 else None)

# ---------------- the Tophet ----------------
y.bolum('Tofet')
duvar_yol([(TOX1, -1.1), (TOX1, -0.44)], 0.05, 'kum_koyu', son=PH)
duvar_yol([(TOX1, -0.32), (TOX1, TOY1), (-1.1, TOY1)], 0.05, 'kum_koyu', bas=PH)
# rows of stelae facing the camera's side, urns before some of them
TUR = [0, 0, 1, 0, 2, 1, 0, 1]
TAS = ['kirec', 'kirec', 'kum_acik', 'kirec', 'mermer']
for i in range(8):
    for j in range(8):
        x = TOX0 + 0.06 + (TOX1 - TOX0 - 0.12) * i / 7 + rn.uniform(-0.01, 0.01)
        yy = TOY0 + 0.08 + (TOY1 - TOY0 - 0.16) * j / 7 + rn.uniform(-0.01, 0.01)
        s = rn.uniform(0.85, 1.25) * (1.0 if j > 2 else 0.95)
        stel(y, x, yy, PH, -math.pi / 2 - 0.35 + rn.uniform(-0.12, 0.12), s, rn.choice(TAS), TUR[(i * 3 + j) % len(TUR)],
             'tas_koyu' if rn.random() < 0.6 else 'boya_kirmizi')
        if rn.random() < 0.45:
            urn(y, x - 0.012, yy - 0.03, PH, rn.uniform(1.0, 1.3), rn.choice(('kiremit', 'kiremit2', 'kerpic')))
# a bigger stele with a Tanit statue on it, a worshipper
stel(y, -0.72, -0.06, PH, -math.pi / 2, 1.8, 'mermer', 1, 'altin')
for k, (x, yy, a) in enumerate(((-0.55, -0.16, 2.3), (-0.95, -0.3, 0.6))):
    insan(y, x, yy, PH, ['beyaz', 'mor'][k], s=1.2, aci=a, kol=0.6)
for x, yy in ((-0.98, -0.06), (-0.45, -0.95)):
    agac(y, x, yy, PH, 0.2, 'servi', 'yesil_koyu', 'ahsap')

# ---------------- the sacred grove and the betyl shrine ----------------
y.bolum('Kutsal koru')
for k in range(16):
    x, yy = rn.uniform(0.45, 1.05), rn.uniform(-1.0, -0.12)
    if abs(x - 0.75) < 0.15 and abs(yy + 0.5) < 0.15: continue
    agac(y, x, yy, PH, rn.uniform(0.12, 0.2), rn.choice(('servi', 'yapraklı', 'palmiye')), rn.choice(('zeytin', 'yesil_koyu')), 'ahsap')
# the shrine: an Egyptian naiskos on a base holding a conical betyl
SX, SY = 0.75, -0.5
kutu_merkez(y, (SX, SY), 0.2, 0.18, 0.03, 'kum_koyu', z0=PH)
for sx in (-1, 1):
    y.prizma((SX + sx * 0.06, SY - 0.06), 0.012, PH + 0.03, PH + 0.17, 'kum_acik', n=8)
kutu_merkez(y, (SX, SY + 0.03), 0.14, 0.09, 0.14, 'kum', z0=PH + 0.03, yuzler='onarkasagsol')
pencere_kutu(y, V(SX - 0.07, SY - 0.015), X, -Y, 0.03, 0.03, 0.08, 0.105, 'koyu', cerceve='kum_acik')
kutu_merkez(y, (SX, SY), 0.17, 0.16, 0.025, 'kum_acik', z0=PH + 0.17)
kavetto(y, dikdortgen(SX - 0.085, SX + 0.085, SY - 0.08, SY + 0.08), PH + 0.195, 0.03, 0.016, 'kum_acik')
donel(y, (SX, SY - 0.045), [(0.022, PH + 0.03), (0.02, PH + 0.06), (0.012, PH + 0.1), (0.0, PH + 0.125)], 'bazalt', n=10)
kanatli_gunes(y, V(SX, SY - 0.08, PH + 0.182), X, -Y, 0.14, 0.018)
for x, yy in ((0.62, -0.62), (0.88, -0.64)):
    insan(y, x, yy, PH, 'beyaz', s=1.2, aci=math.pi / 2 + (0.4 if x < SX else -0.4), kol=0.7, sapka='beyaz')
# a pool for the rites
havuz(y, 0.5, 0.72, -0.98, -0.78, PH + 0.02, derin=0.03, kenar=0.018, key='kum_acik')
kutu(y, V(0.482, -0.998, PH), X, 0.256, 0.236, 0.02, 'kum_koyu', 'onarkasagsol')

calistir(y, 'lm_tanit')
