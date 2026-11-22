# Elephant Stables of Hampi (lm_filahiri): the long Vijayanagara stable of eleven domed chambers - each with a tall
# pointed arch, a band of niches and a stepped parapet - its domes alternating (plain, fluted, octagonal, stepped
# Hindu shikhara) round a raised central tower with corner chhatris; in front a dusty court with elephants (caparisoned,
# one with a howdah, a calf) and mahouts, a water trough, a granite mandapa, the arcaded guards' quarters, boulders.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from hint_ortak import *

y = Yapi()
DUV, DUV2, TRIM = 'siva_krem', 'kum', 'siva'
PLINTH = 'granit'
SIVA = (DUV, DUV2, TRIM, 'koyu')
NIS = (DUV, DUV2, TRIM, DUV2)                # blind niches: a sandstone back
H0 = 0.03                                  # the ground slab
BX0, BX1, BY0, BY1 = -1.0, 1.0, 0.16, 0.48
ZP = H0 + 0.035                            # the stable's plinth top
HW = 0.29                                  # wall height
ZR = ZP + HW
NB = 11
BW = (BX1 - BX0) / NB
XS = [BX0 + BW * i for i in range(NB + 1)]
YC = (BY0 + BY1) / 2

# ---------------- the ground ----------------
y.bolum('Zemin ve avlu')
GX0, GX1, GY0, GY1 = -1.08, 1.08, -1.17, 0.68
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, H0, 'kaya_koyu', 'onarkasagsol')
y.yuz_yon([V(GX0, GY0, H0), V(GX1, GY0, H0), V(GX1, GY1, H0), V(GX0, GY1, H0)], 'toprak', Z)
silme(y, dikdortgen(GX0, GX1, GY0, GY1), H0 - 0.008, 0.008, 0.005, 'kaya', 'duz')
# the court's paved processional way from the gate to the central arch
y.yuz_yon([V(-0.1, -1.14, H0 + 0.003), V(0.1, -1.14, H0 + 0.003), V(0.1, BY0 - 0.08, H0 + 0.003), V(-0.1, BY0 - 0.08, H0 + 0.003)], 'zemin', Z)
for a, b in ((V(-0.1, BY0 - 0.08), V(-0.1, -1.14)), (V(0.1, -1.14), V(0.1, BY0 - 0.08))):
    duz_duvar(y, a, b, H0, H0 + 0.003, 'zemin')

# ---------------- the stable: plinth, walls, arches ----------------
y.bolum('Ahır: kaide, kemerler')
kutu(y, V(BX0 - 0.03, BY0 - 0.06, H0), X, BX1 - BX0 + 0.06, BY1 - BY0 + 0.09, ZP - H0, PLINTH, 'onarkasagsolust')
silme(y, dikdortgen(BX0 - 0.03, BX1 + 0.03, BY0 - 0.06, BY1 + 0.03), ZP - 0.01, 0.01, 0.006, 'granit_koyu', 'kaide')
# steps up the plinth in front of each arch
for i in range(NB):
    xm = (XS[i] + XS[i + 1]) / 2
    kutu(y, V(xm - 0.05, BY0 - 0.09, H0), X, 0.1, 0.032, (ZP - H0) * 0.5, PLINTH, 'onsagsolust')
for i in range(NB):
    a, b = V(XS[i], BY0), V(XS[i + 1], BY0)
    cen = i == NB // 2
    if cen:
        continue
    # the big pointed arch (a dark stall behind), a moulded band, the niche band above
    y.kemerli(a, b, ZP, HW * 0.76, SIVA, v0=0.0, en=0.64, ust=0.025, derin=0.07, k_say=12, sivri=0.5, cerceve=(0.009, [TRIM, DUV2]))
    nis_satir(y, a, b, ZP + HW * 0.76, ZR, 3, NIS, en=0.56, derin=0.007, sivri=0.4)
    silme(y, [a, b], ZP + HW * 0.76 - 0.004, 0.008, 0.006, TRIM, 'duz', kapali=False)
# pilasters between the bays (proud of the wall), with capitals
for i in range(NB + 1):
    x = XS[i]
    if i in (NB // 2, NB // 2 + 1): continue
    x = min(max(x, BX0 + 0.016), BX1 - 0.016)   # (the end ones kept on the wall: their backs would show past its end)
    kutu(y, V(x - 0.012, BY0 - 0.012, ZP), X, 0.024, 0.012, HW - 0.012, TRIM, 'onsagsolust')
    kutu(y, V(x - 0.016, BY0 - 0.016, ZP + HW * 0.74), X, 0.032, 0.016, 0.016, TRIM, 'onsagsolust')
# the back: a small arched window and a door in each bay
for i in range(NB):
    a, b = V(XS[i + 1], BY1), V(XS[i], BY1)
    if i % 2 == 0:
        dikdortgen_acik(y, a, b, ZP, HW, 0.36, 0.64, 0.0, 0.13, (DUV, DUV2, TRIM, 'ahsap'), derin=0.02, cerceve=(0.007, TRIM))
    else:
        y.kemerli(a, b, ZP, HW, SIVA, v0=HW * 0.42, en=0.26, ust=HW * 0.3, derin=0.02, k_say=6, sivri=0.5, cerceve=(0.006, TRIM))
silme(y, [V(BX1, BY1), V(BX0, BY1)], ZP + HW * 0.76 - 0.004, 0.008, 0.006, TRIM, 'duz', kapali=False)
# the ends: two niches each
for (a, b) in ((V(BX0, BY1), V(BX0, BY0)), (V(BX1, BY0), V(BX1, BY1))):
    nis_satir(y, a, b, ZP, ZR, 2, SIVA, en=0.5, derin=0.012, sivri=0.5)

# the central bay: a projecting portal frame rising above the parapet, the arch taller
y.bolum('Orta kapı')
CX = (XS[NB // 2] + XS[NB // 2 + 1]) / 2
PW_ = BW + 0.05
PY = BY0 - 0.05
ZPP = ZR + 0.08
pk = dikdortgen(CX - PW_ / 2, CX + PW_ / 2, PY, BY0 + 0.001)
y.kemerli(pk[0], pk[1], ZP, ZPP - ZP, SIVA, v0=0.0, en=0.6, ust=ZPP - ZR + 0.012, derin=0.11, k_say=12, sivri=0.55, cerceve=(0.012, [TRIM, DUV2]))
for (a, b) in ((pk[1], pk[2]), (pk[3], pk[0])):
    duz_duvar(y, a, b, ZP, ZPP, DUV)
duz_duvar(y, pk[2], pk[3], ZR - 0.01, ZPP, DUV)   # (its back above the roof)
# the frame's panels either side of the arch and a band of niches on top
for s in (-1, 1):
    xa = CX + s * PW_ / 2
    kutu(y, V(min(xa, xa - s * 0.018), PY - 0.012, ZP), X, 0.018, 0.012, ZPP - ZP - 0.003, TRIM, 'onsagsolust')
silme(y, pk, ZPP - 0.014, 0.014, 0.01, TRIM, 'tac')
y.yuz_yon([V(p.x, p.y, ZPP) for p in pk], TRIM, Z)
mazgal(y, pk[0] - V(0.004, 0.004), pk[1] + V(0.004, -0.004), ZPP, 0.022, 0.012, TRIM, dis_en=0.018, bosluk=0.012)
for p in (pk[0], pk[1]):
    y.prizma((p.x, p.y + 0.012), 0.012, ZPP, ZPP + 0.03, TRIM, n=8)
    lotus_kubbe(y, (p.x, p.y + 0.012), 0.012, ZPP + 0.03, 0.014, TRIM, n=10, kat=4, s_son=0.4)

# ---------------- the roof terrace and parapet ----------------
y.bolum('Dam ve korkuluk')
rk = dikdortgen(BX0, BX1, BY0, BY1)
y.yuz_yon([V(p.x, p.y, ZR) for p in rk], 'zemin', Z)
silme(y, rk, ZR - 0.016, 0.016, 0.01, TRIM, 'kaba')
for i in range(4):
    a, b = rk[i], rk[(i + 1) % 4]
    if i == 0:
        # (the central portal stands in front: the parapet stops either side of it)
        for p, q in ((a, V(CX - PW_ / 2, BY0)), (V(CX + PW_ / 2, BY0), b)):
            sivri_mazgal(y, p, q, ZR, 0.026, 0.014, TRIM, w=0.022, g=0.014, uc=0.01, kademe=True)
    else:
        sivri_mazgal(y, a, b, ZR, 0.026, 0.014, TRIM, w=0.022, g=0.014, uc=0.01, kademe=(i != 2))    # (the back: plain merlons)


# ---------------- the domes ----------------
def taban(cx, w, h=0.055):
    """the square dome base on the roof: a niche on each face, a cornice"""
    k = dikdortgen(cx - w / 2, cx + w / 2, YC - w / 2, YC + w / 2)
    for i in range(4):
        if i % 2: duz_duvar(y, k[i], k[(i + 1) % 4], ZR, ZR + h, DUV)    # (the sides face the next dome: plain)
        else: nis_satir(y, k[i], k[(i + 1) % 4], ZR, ZR + h, 2, NIS, en=0.5, derin=0.006, sivri=0.45)
    silme(y, k, ZR + h - 0.01, 0.01, 0.008, TRIM, 'kaba')
    y.yuz_yon([V(p.x, p.y, ZR + h) for p in k], TRIM, Z)
    return ZR + h


def yivli_kubbe(c, r, z, h, n_yiv=16, key=DUV, kat=6):
    """a fluted (ribbed melon) dome"""
    m = n_yiv * 2
    rings = []
    for k in range(kat):
        ph = math.pi / 2 * k / kat
        rings.append([V(c[0] + r * math.cos(ph) * (1 if i % 2 == 0 else 0.9) * math.cos(TAU * i / m),
                        c[1] + r * math.cos(ph) * (1 if i % 2 == 0 else 0.9) * math.sin(TAU * i / m), z + h * math.sin(ph)) for i in range(m)])
    for k in range(kat - 1):
        y.serit(rings[k], rings[k + 1], key)
    t = V(c[0], c[1], z + h)
    for i in range(m):
        y.yuz([rings[-1][i], rings[-1][(i + 1) % m], t], key)
    return z + h


def kubbe_sec(i, cx):
    tur = ('sade', 'yivli', 'sekiz', 'sikhara', 'yivli', 'sade')[min(abs(i), 5)] if i else None
    w = 0.15
    zb = taban(cx, w)
    rd = 0.068
    if tur == 'sade':
        y.prizma((cx, YC), rd, zb, zb + 0.022, DUV, n=24, ust=False)
        halka_kornis(y, (cx, YC), rd, zb + 0.016, 0.006, 0.006, 24, TRIM)
        lotus_kubbe(y, (cx, YC), rd, zb + 0.022, rd * 1.0, DUV, n=24, kat=7, yaprak=TRIM, s_son=0.9)
    elif tur == 'yivli':
        y.prizma((cx, YC), rd, zb, zb + 0.026, DUV, n=8, ust=True, kat=math.pi / 8)
        halka_kornis(y, (cx, YC), rd, zb + 0.02, 0.006, 0.006, 8, TRIM, kat=math.pi / 8)
        t = yivli_kubbe((cx, YC), rd * 0.98, zb + 0.026, rd * 1.05)
        donel(y, (cx, YC), [(0.0, t - 0.004), (0.016, t - 0.004), (0.02, t + 0.004), (0.012, t + 0.01), (0.0, t + 0.01)], TRIM, n=12)
        kalasa(y, cx, YC, t + 0.01, 0.9, TRIM)
    elif tur == 'sekiz':
        # an eight-sided cloister dome on an octagonal drum with small windows, ribs along the hips
        dk = cokgen((cx, YC), rd, 8, math.pi / 8)
        for j in range(8):
            y.kemerli(dk[j], dk[(j + 1) % 8], zb, 0.04, SIVA, v0=0.008, en=0.42, ust=0.008, derin=0.006, k_say=6, sivri=0.5)
        halka_kornis(y, (cx, YC), rd, zb + 0.04, 0.008, 0.008, 8, TRIM, kat=math.pi / 8)
        t = y.kubbe((cx, YC), rd * 1.02, zb + 0.048, rd * 0.95, DUV, n=8, kat=7)
        for j in range(8):
            a = math.pi / 8 + TAU * j / 8
            pts = [V(cx + rd * 1.03 * math.cos(ph) * math.cos(a), YC + rd * 1.03 * math.cos(ph) * math.sin(a), zb + 0.048 + rd * 0.95 * math.sin(ph))
                   for ph in [math.pi / 2 * k / 6 * 0.97 for k in range(7)]]
            boru(y, pts, 0.0035, TRIM, n=4, kapat=False)
        kalasa(y, cx, YC, t.z - 0.002, 0.9, TRIM)
    elif tur == 'sikhara':
        # a stepped pyramidal Hindu tower: four receding tiers with ledges, an amalaka and a kalasha
        z = zb
        w0 = 0.14
        for k in range(4):
            wk = w0 * (1 - 0.2 * k)
            hk = 0.032 - k * 0.004
            kk = dikdortgen(cx - wk / 2, cx + wk / 2, YC - wk / 2, YC + wk / 2)
            for j in range(4):
                nis_satir(y, kk[j], kk[(j + 1) % 4], z, z + hk, 3 - (k > 1), NIS, en=0.5, derin=0.005, sivri=0.0)
            chhajja(y, kk, z + hk - 0.008, 0.008, 0.008, TRIM)
            y.yuz_yon([V(p.x, p.y, z + hk) for p in kk], DUV, Z)
            z += hk
        donel(y, (cx, YC), [(0.03, z), (0.036, z + 0.008), (0.036, z + 0.016), (0.026, z + 0.022), (0.0, z + 0.022)], DUV, n=16,
              dilim=[DUV, TRIM])
        kalasa(y, cx, YC, z + 0.022, 0.9, TRIM)


y.bolum('On bir kubbe')
for i in range(NB):
    k = i - NB // 2
    if k == 0: continue
    kubbe_sec(k, (XS[i] + XS[i + 1]) / 2)

# ---------------- the central tower ----------------
y.bolum('Orta kule')
TW = 0.19
tk = dikdortgen(CX - TW / 2, CX + TW / 2, YC - TW / 2, YC + TW / 2)
Z1 = ZR + 0.22
for i in range(4):
    a, b = tk[i], tk[(i + 1) % 4]
    for j in range(2):
        p, q = a.lerp(b, j / 2), a.lerp(b, (j + 1) / 2)
        y.kemerli(p, q, ZR, Z1 - ZR, SIVA, v0=0.03, en=0.56, ust=0.03, derin=0.018, k_say=10, sivri=0.5, cerceve=(0.007, TRIM))
silme(y, tk, ZR, 0.02, 0.008, DUV2, 'kaide')
chhajja(y, tk, Z1 - 0.02, 0.02, 0.03, TRIM)
y.yuz_yon([V(p.x, p.y, Z1) for p in tk], 'zemin', Z)
for p in tk:
    q = V(CX, YC).lerp(p, 0.84)
    chhatri(y, q.x, q.y, Z1, 0.024, n=4, kolon=TRIM, kubbe=DUV, kaide=DUV2, kat=math.pi / 4, s_son=0.5)
# the octagonal drum with arched windows, the ribbed dome
rd = 0.078
dk = cokgen((CX, YC), rd, 8, math.pi / 8)
Z2 = Z1 + 0.1
for j in range(8):
    y.kemerli(dk[j], dk[(j + 1) % 8], Z1, Z2 - Z1, SIVA, v0=0.015, en=0.5, ust=0.015, derin=0.007, k_say=8, sivri=0.5, cerceve=(0.005, TRIM))
for j in range(8):   # buttress strips on the drum's corners
    p = dk[j]; d = (p - V(CX, YC)).normalized()
    kutu_merkez(y, (p.x + d.x * 0.004, p.y + d.y * 0.004), 0.012, 0.012, Z2 - Z1, TRIM, z0=Z1, aci=math.atan2(d.y, d.x))
chhajja(y, cokgen((CX, YC), rd + 0.006, 8, math.pi / 8), Z2 - 0.014, 0.014, 0.022, TRIM)
y.prizma((CX, YC), rd, Z2, Z2 + 0.014, DUV, n=8, kat=math.pi / 8, ust=True)
t = yivli_kubbe((CX, YC), rd * 0.98, Z2 + 0.014, rd * 1.15, 20)
donel(y, (CX, YC), [(0.0, t - 0.005), (0.02, t - 0.005), (0.025, t + 0.005), (0.015, t + 0.012), (0.0, t + 0.012)], TRIM, n=12)
kalasa(y, CX, YC, t + 0.012, 1.3, 'altin')
sancak(y, tk[0].x + 0.03, tk[0].y + 0.03, Z1, boy=0.26, en=0.12, yuk=0.075, aci=-0.6)

# ---------------- the court: gate, walls ----------------
y.bolum('Avlu duvarı ve kapı')
WY = -1.07
WH = 0.075
WK = 'granit'
duvar_yol = [V(GX0 + 0.05, BY0 - 0.04), V(GX0 + 0.05, WY), V(-0.12, WY)]
duvar_yol2 = [V(0.12, WY), V(GX1 - 0.05, WY), V(GX1 - 0.05, BY0 - 0.04)]
for yol in (duvar_yol, duvar_yol2):
    # (the court wall: a battered granite wall, coping on top; its outer face to the right of travel)
    n = len(yol)
    for i in range(n - 1):
        a, b = yol[i], yol[i + 1]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        kutu(y, a - e * (0.02 if i == 0 else 0) + nn * 0.02 + Z * H0, e, (b - a).length + (0.02 if i == 0 else 0) + 0.02, 0.04, WH, WK)
        kutu(y, a - e * (0.022 if i == 0 else 0) + nn * 0.024 + Z * (H0 + WH), e, (b - a).length + 0.044 - (0.0 if i else 0.0), 0.048, 0.01, 'granit_koyu')
# the gate: two piers with a lintel and a small stepped tower over it
GW = 0.24
for s in (-1, 1):
    kutu_merkez(y, (s * (GW / 2 - 0.03), WY), 0.07, 0.08, 0.17, WK, z0=H0)
    silme(y, dikdortgen(s * (GW / 2 - 0.03) - 0.035, s * (GW / 2 - 0.03) + 0.035, WY - 0.04, WY + 0.04), H0 + 0.165, 0.008, 0.006, 'granit_koyu')
kutu_merkez(y, (0, WY), GW + 0.02, 0.09, 0.03, WK, z0=H0 + 0.17)
z = H0 + 0.2
for k in range(3):
    w = (GW + 0.02) * (1 - 0.22 * k)
    d = 0.09 * (1 - 0.2 * k)
    kk = dikdortgen(-w / 2, w / 2, WY - d / 2, WY + d / 2)
    for j in range(4):
        nis_satir(y, kk[j], kk[(j + 1) % 4], z, z + 0.03, 3 if j % 2 == 0 else 1, ('granit', 'granit_koyu', 'granit', 'koyu'), en=0.5, derin=0.005)
    chhajja(y, kk, z + 0.022, 0.008, 0.008, 'granit_koyu')
    y.yuz_yon([V(p.x, p.y, z + 0.03) for p in kk], WK, Z)
    z += 0.03
donel(y, (0, WY), [(0.03, z), (0.034, z + 0.012), (0.024, z + 0.022), (0.0, z + 0.022)], WK, n=12)
kalasa(y, 0, WY, z + 0.022, 0.8, 'altin')

# ---------------- the guards' quarters (east) ----------------
y.bolum('Muhafız binası')
QX0, QX1, QY0, QY1 = 0.62, 0.96, -0.9, -0.22
QZ = H0 + 0.04
kutu(y, V(QX0 - 0.02, QY0 - 0.02, H0), X, QX1 - QX0 + 0.04, QY1 - QY0 + 0.04, QZ - H0, PLINTH, 'onarkasagsolust')
silme(y, dikdortgen(QX0 - 0.02, QX1 + 0.02, QY0 - 0.02, QY1 + 0.02), QZ - 0.008, 0.008, 0.005, 'granit_koyu')
QH = 0.17
qk = dikdortgen(QX0, QX1, QY0, QY1)
# the west front: an arcade of six pointed arches with a deep veranda
for j in range(6):
    p, q = qk[3].lerp(qk[0], j / 6), qk[3].lerp(qk[0], (j + 1) / 6)
    y.kemerli(p, q, QZ, QH, SIVA, v0=0.0, en=0.7, ust=0.03, derin=0.06, k_say=10, sivri=0.5, cerceve=(0.006, TRIM))
for (a, b, n) in ((qk[0], qk[1], 2), (qk[1], qk[2], 5), (qk[2], qk[3], 2)):
    for j in range(n):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        y.kemerli(p, q, QZ, QH, SIVA, v0=QH * 0.4, en=0.3, ust=QH * 0.3, derin=0.015, k_say=6, sivri=0.5, cerceve=(0.005, TRIM))
silme(y, qk, QZ + QH - 0.014, 0.014, 0.01, TRIM, 'kaba')
y.yuz_yon([V(p.x, p.y, QZ + QH) for p in qk], 'zemin', Z)
for i in range(4):
    sivri_mazgal(y, qk[i], qk[(i + 1) % 4], QZ + QH, 0.022, 0.012, TRIM, w=0.02, g=0.012, uc=0.009, kademe=True)
# a corner watch kiosk
for (qx, qy) in ((QX1 - 0.05, QY1 - 0.05), (QX0 + 0.05, QY0 + 0.05)):
    chhatri(y, qx, qy, QZ + QH, 0.035, n=4, kolon=TRIM, kubbe=DUV, kaide=DUV2, kat=math.pi / 4)
# a larger kiosk over the middle of the roof (the guards' lookout)
chhatri(y, (QX0 + QX1) / 2, (QY0 + QY1) / 2, QZ + QH, 0.05, n=4, kolon=TRIM, kubbe=DUV, kaide=DUV2, kat=math.pi / 4)
merdiven(y, (QX0 - 0.02 - 0.05, (QY0 + QY1) / 2), 0.0, 0.12, H0, QZ, n=3, d=0.016, key=PLINTH)

# ---------------- the west: trough, mandapa, fodder ----------------
y.bolum('Yalak, mandapa, yem')
havuz(y, -0.94, -0.56, -0.42, -0.3, H0 + 0.03, derin=0.03, kenar=0.02, key='granit')
kutu(y, V(-0.96, -0.44, H0), X, 0.42, 0.16, 0.03, 'granit', 'onarkasagsol')
# a granite mandapa: sixteen square pillars, bracket capitals, a flat slab roof with a parapet
MX, MY = -0.74, -0.8
kutu_merkez(y, (MX, MY), 0.34, 0.3, 0.035, PLINTH, z0=H0)
silme(y, dikdortgen(MX - 0.17, MX + 0.17, MY - 0.15, MY + 0.15), H0 + 0.027, 0.008, 0.005, 'granit_koyu')
zm = H0 + 0.035
for u in (-0.135, -0.045, 0.045, 0.135):
    for v in (-0.115, -0.04, 0.04, 0.115):
        x, yy = MX + u, MY + v
        kutu_merkez(y, (x, yy), 0.024, 0.024, 0.03, 'granit', z0=zm)
        kutu_merkez(y, (x, yy), 0.018, 0.018, 0.08, 'granit', z0=zm + 0.03, yuzler='onarkasagsol')
        kutu_merkez(y, (x, yy), 0.024, 0.024, 0.014, 'granit', z0=zm + 0.11)
        for a in (0.0, math.pi / 2):
            kutu_merkez(y, (x, yy), 0.05, 0.012, 0.01, 'granit_koyu', z0=zm + 0.124, aci=a)
mk = dikdortgen(MX - 0.165, MX + 0.165, MY - 0.145, MY + 0.145)
kutu(y, V(mk[0].x, mk[0].y, zm + 0.134), X, 0.33, 0.29, 0.02, 'granit', 'onarkasagsolust')
chhajja(y, mk, zm + 0.134, 0.02, 0.02, 'granit_koyu')
y.yuz_yon([V(mk[0].x, mk[0].y, zm + 0.134), V(mk[3].x, mk[3].y, zm + 0.134), V(mk[2].x, mk[2].y, zm + 0.134), V(mk[1].x, mk[1].y, zm + 0.134)], 'granit_koyu', -Z)
parapet(y, mk, zm + 0.154, 0.02, 0, 0.014, 'granit')
y.yuz_yon([V(p.x, p.y, zm + 0.1545) for p in disa(mk, -0.014)], 'zemin', Z)
chhatri(y, MX, MY, zm + 0.154, 0.04, n=4, kolon='granit', kubbe='granit', kaide='granit_koyu', kat=math.pi / 4)
# fodder heaps (sugar cane and hay) and a water pot
for (x, yy, r) in ((-0.55, -0.2, 0.05), (-0.45, -0.12, 0.04), (-0.95, -0.12, 0.045)):
    donel(y, (x, yy), [(r, H0), (r * 0.9, H0 + r * 0.5), (r * 0.5, H0 + r * 0.9), (0.0, H0 + r)], 'saz', n=12)
for k in range(5):
    cubuk(y, V(-0.66 + k * 0.012, -0.05, H0 + 0.004), V(-0.56 + k * 0.012, -0.03, H0 + 0.004), 0.007, 'cimen_kuru')

# ---------------- elephants and mahouts ----------------
y.bolum('Filler ve fil bakıcıları')
fil(y, 0.0, -0.55, H0 + 0.003, math.pi / 2, 1.55, cul='boya_kirmizi', haudah='altin', binici='boya_sari', kaba=True)
fil(y, -0.34, -0.14, H0, math.pi / 2 + 0.3, 1.45, cul='turkuaz', binici='beyaz', kaba=True)
fil(y, -0.78, -0.22, H0, -math.pi / 2 + 0.2, 1.4, hortum=-0.004, kaba=True)
fil(y, -0.6, -0.2, H0, -math.pi / 2 - 0.5, 0.75, kaba=True)                  # the calf
fil(y, 0.44, -0.07, H0, math.pi, 1.45, cul='lacivert', binici='boya_kirmizi', hortum=0.03, kaba=True)
fil(y, 0.4, -0.64, H0, math.pi * 0.75, 1.4, kaba=True)
for (x, yy, a, g) in ((0.1, -0.5, 1.6, 'beyaz'), (-0.1, -0.62, 1.4, 'boya_sari'), (0.32, -0.12, 3.0, 'beyaz'), (-0.7, -0.4, -0.4, 'beyaz'),
                      (0.42, -0.78, 2.2, 'boya_kirmizi'), (0.02, -1.03, 1.57, 'lacivert'), (-0.04, -1.03, 1.57, 'lacivert'), (0.72, -0.1, 0.0, 'beyaz')):
    adam(y, x, yy, H0, a, g, 'beyaz', boy=0.05)

# ---------------- boulders and palms ----------------
y.bolum('Kayalar, palmiyeler')
rng = y.rng
for (cx, cy, k) in ((-0.98, -1.12, 3), (0.98, -1.12, 3), (-0.97, 0.08, 2), (0.97, 0.06, 2), (-0.55, 0.6, 2), (0.6, 0.6, 2)):
    for j in range(k):
        x = cx + (rng.random() - 0.5) * 0.12
        yy = cy + (rng.random() - 0.5) * 0.1
        r = 0.04 + 0.035 * rng.random()
        elipsoid(y, (x, yy, H0 + r * 0.55), r * (1 + 0.3 * rng.random()), r * (0.8 + 0.3 * rng.random()), r * 0.8,
                 'granit' if j % 2 else 'kaya', n=8, kat=4)
for (x, yy) in ((-0.97, -0.56), (0.5, -0.96), (-0.92, 0.6), (0.9, 0.6), (-0.3, 0.6), (0.25, 0.6), (-0.38, -1.0), (0.38, -1.0)):
    agac(y, x, yy, H0, boy=0.26, tur='palmiye', key='boya_yesil')

bolum_say(y)
calistir(y, 'lm_filahiri')
