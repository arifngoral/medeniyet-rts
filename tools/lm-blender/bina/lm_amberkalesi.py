# Amber Fort (lm_amberkalesi): the Kachhwaha hill palace above Maota Lake. Cream and red sandstone palaces on a walled
# hilltop: Jaleb Chowk's arcaded court entered by the Suraj Pol up the elephant ramp, the stair to the red-columned
# Diwan-i-Aam, the painted three-storey Ganesh Pol, the white Jai Mandir and Sukh Niwas round the Aram Bagh garden, the
# tall Man Singh palace with domed corner kiosks; ramparts with round bastions, the walls climbing the ridge to a
# Jaigarh watchtower; below, the lake with the star-shaped beds of the Kesar Kyari garden and the ghats.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from hint_ortak import *
import doku

y = Yapi()
KR, KR2 = 'siva_krem', 'kum'                  # the palaces' cream plaster and sandstone
TR = 'kum_acik'                               # trim
KIR, KIR2 = 'kirmizi_tas', 'kirmizi_tas_acik'
SUR = 'kum_koyu'                              # rampart stone
SV = (KR, KR2, TR, 'koyu')
ZW, YS = 0.035, -0.56                         # the lake's water, the shore line
ZT, ZJ = 0.33, 0.25                           # the upper terrace, Jaleb Chowk
PX0, PX1, PY0, PY1 = -0.8, 0.88, -0.47, 0.62  # the walled hilltop
JX0 = 0.3                                     # Jaleb Chowk: x JX0..PX1, y PY0..JY1
JY1 = 0.08
EX0, EX1, EY1 = -1.15, 1.15, 1.15


def ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def icinde(x, yy, m=0.0):
    return PX0 - m <= x <= PX1 + m and PY0 - m <= yy <= PY1 + m


def yuk(x, yy):
    """ground height"""
    if icinde(x, yy):
        return (ZJ if (x >= JX0 and yy <= JY1) else ZT) - 0.03
    dx = max(0.0, PX0 - x, x - PX1); dy = max(0.0, PY0 - yy, yy - PY1)
    d = math.hypot(dx, dy)
    h = 0.075 + (ZT - 0.15) * math.exp(-(d / 0.17) ** 2)
    h = max(h, 0.075 + 0.43 * math.exp(-((yy - 1.13) / 0.24) ** 2) * (0.8 + 0.2 * math.sin(4.0 * x + 1.0)))
    h = max(h, 0.075 + 0.2 * math.exp(-(((x + 1.08) / 0.22) ** 2 + ((yy - 0.4) / 0.4) ** 2)))
    h += 0.012 * min(1.0, (h - 0.075) / 0.05) * math.sin(11 * x + 3 * yy) * math.cos(9 * yy - 5 * x)
    s = ss(YS, YS + 0.09, yy)
    return 0.075 + (h - 0.075) * s


# ---------------- the terrain ----------------
y.bolum('Arazi')
NX, NY = 36, 26
xs = [EX0 + (EX1 - EX0) * i / NX for i in range(NX + 1)]
ys = [YS + (EY1 - YS) * j / NY for j in range(NY + 1)]
G = [[V(x, yy, yuk(x, yy)) for yy in ys] for x in xs]


def arazi_renk(x, yy, zz):
    e = 0.012
    gx = (yuk(x + e, yy) - yuk(x - e, yy)) / (2 * e)
    gy = (yuk(x, yy + e) - yuk(x, yy - e)) / (2 * e)
    s = math.hypot(gx, gy)
    n = math.sin(x * 4.3 + 1.1) * math.cos(yy * 3.7 - 0.6) * 0.7 + math.sin(x * 9.1 - yy * 6.3 + 2.0) * 0.3
    c = (0.55, 0.53, 0.33)
    mix = lambda c0, c1, t: tuple(p + (q - p) * t for p, q in zip(c0, c1))
    c = mix(c, (0.47, 0.51, 0.29), 0.5 + 0.5 * n)                              # dry scrub, greener in patches
    c = mix(c, (0.62, 0.52, 0.38), ss(0.5, 1.4, s + 0.3 * n))                 # bare earth on the slopes
    c = mix(c, (0.66, 0.57, 0.46), ss(1.4, 2.4, s + 0.3 * n) * 0.8)            # rock on the steep faces
    return c


doku.KOSE_RENK['toprak_ot'] = arazi_renk
for i in range(NX):
    for j in range(NY):
        a, b, c, d = G[i][j], G[i + 1][j], G[i + 1][j + 1], G[i][j + 1]
        mx, my = (a.x + c.x) / 2, (a.y + c.y) / 2
        if icinde(mx, my, -0.04):
            continue                                       # (under the terrace paving)
        if (i + j) % 2 == 0:
            y.yuz([a, b, c], 'toprak_ot'); y.yuz([a, c, d], 'toprak_ot')
        else:
            y.yuz([a, b, d], 'toprak_ot'); y.yuz([b, c, d], 'toprak_ot')
# the skirt round the land (W, N, E): soil and rock strata
kenar = [G[NX][j] for j in range(NY)] + [G[i][NY] for i in range(NX, 0, -1)] + [G[0][j] for j in range(NY, -1, -1)]
for k in range(len(kenar) - 1):
    a, b = kenar[k], kenar[k + 1]
    e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
    m1a, m1b = min(a.z - 0.02, 0.03 + 0.01 * math.sin(a.x * 7 + a.y * 5)), min(b.z - 0.02, 0.03 + 0.01 * math.sin(b.x * 7 + b.y * 5))
    y.yuz_yon([V(a.x, a.y, a.z - 0.02), V(b.x, b.y, b.z - 0.02), b, a], 'toprak', nn)
    y.yuz_yon([V(a.x, a.y, m1a), V(b.x, b.y, m1b), V(b.x, b.y, b.z - 0.02), V(a.x, a.y, a.z - 0.02)], 'kaya', nn)
    y.yuz_yon([V(a.x, a.y, 0), V(b.x, b.y, 0), V(b.x, b.y, m1b), V(a.x, a.y, m1a)], 'kaya_koyu', nn)

# ---------------- the lake, the ghat, Kesar Kyari ----------------
y.bolum('Maota gölü ve Kesar Kyari')
# the ghat: the stone embankment along the shore, down into the water
for i in range(NX):
    a, b = G[i][0], G[i + 1][0]
    y.yuz_yon([V(a.x, YS, 0.0), V(b.x, YS, 0.0), V(b.x, YS, b.z), V(a.x, YS, a.z)], SUR, -Y)
silme(y, [V(EX0, YS), V(EX1, YS)], 0.068, 0.007, 0.006, TR, 'duz', kapali=False)
# the water and the lake's outer rim
y.yuz_yon([V(EX0, EX0, ZW), V(EX1, EX0, ZW), V(EX1, YS, ZW), V(EX0, YS, ZW)], 'su', Z)
for (p, q) in ((V(EX0, YS), V(EX0, EX0)), (V(EX0, EX0), V(EX1, EX0)), (V(EX1, EX0), V(EX1, YS))):
    duz_duvar(y, p, q, 0.0, ZW + 0.012, SUR)
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    y.yuz_yon([p + Z * (ZW + 0.012), q + Z * (ZW + 0.012), q - nn * 0.025 + Z * (ZW + 0.012), p - nn * 0.025 + Z * (ZW + 0.012)], TR, Z)
    duz_duvar(y, q - nn * 0.025, p - nn * 0.025, ZW, ZW + 0.012, SUR)
# stepped bathing ghats below the ramp's foot
for k in range(4):
    kutu(y, V(0.72, YS - 0.02 * (k + 1), 0.0), X, 0.3, 0.02 * (k + 1) + 0.001, 0.068 - k * 0.012, SUR, 'onsagsolust')
# Kesar Kyari: a terrace in the lake with star-shaped saffron beds
KX0, KX1, KY0, KY1 = -0.62, -0.06, -0.98, -0.7
kutu(y, V(KX0, KY0, 0.0), X, KX1 - KX0, KY1 - KY0, ZW + 0.03, SUR, 'onarkasagsol')
y.yuz_yon([V(KX0, KY0, ZW + 0.03), V(KX1, KY0, ZW + 0.03), V(KX1, KY1, ZW + 0.03), V(KX0, KY1, ZW + 0.03)], 'zemin', Z)
silme(y, dikdortgen(KX0, KX1, KY0, KY1), ZW + 0.024, 0.006, 0.006, TR, 'duz')
zk = ZW + 0.03
for (cx, cy) in ((-0.5, -0.84), (-0.34, -0.84), (-0.18, -0.84)):
    yild = [V(cx + (0.062 if i % 2 == 0 else 0.036) * math.cos(math.pi * i / 8 + math.pi / 8), cy + (0.062 if i % 2 == 0 else 0.036) * math.sin(math.pi * i / 8 + math.pi / 8)) for i in range(16)]
    for i in range(16):
        duz_duvar(y, yild[i], yild[(i + 1) % 16], zk, zk + 0.01, TR)
    y.yuz_yon([V(p.x, p.y, zk + 0.01) for p in yild], 'cimen', Z)
    for i in range(8):
        a = math.pi / 4 * i + math.pi / 8
        kure(y, (cx + 0.04 * math.cos(a), cy + 0.04 * math.sin(a), zk + 0.016), 0.007, 'boya_sari' if i % 2 else 'boya_kirmizi', n=6, kat=3)
    y.prizma((cx, cy), 0.012, zk + 0.01, zk + 0.02, TR, n=8)
for (cx, cy) in ((-0.58, -0.74), (-0.1, -0.74), (-0.58, -0.94), (-0.1, -0.94)):
    kutu_merkez(y, (cx, cy), 0.04, 0.04, 0.012, 'cimen', z0=zk)
# a causeway from the shore
kutu(y, V(-0.36, KY1, 0.0), X, 0.05, YS - KY1 + 0.002, ZW + 0.03, SUR, 'sagsol')
y.yuz_yon([V(-0.36, KY1, ZW + 0.03), V(-0.31, KY1, ZW + 0.03), V(-0.31, YS, ZW + 0.03), V(-0.36, YS, ZW + 0.03)], 'zemin', Z)

# ---------------- ramparts and bastions ----------------
y.bolum('Surlar ve burçlar')
PL = dikdortgen(PX0, PX1, PY0, PY1)
KAL = 0.05
sur(y, PL, 0.0, ZT, kalinlik=KAL, key=SUR, kapali=True, mazgal_h=0.028, parapet_h=0.014, ust_key='zemin', ic=True)
silme(y, PL, ZT - 0.03, 0.012, 0.008, TR, 'duz')
for (cx, cy, r) in ((PX0, PY0, 0.075), (PX1, PY0, 0.075), (PX1, PY1, 0.07), (PX0, PY1, 0.07), (-0.25, PY0, 0.06), (0.42, PY0, 0.06)):
    kule_yuvarlak(y, (cx, cy), r, 0.0, ZT + 0.02, SUR, cati='duz', mazgal_h=0.028, n=12, yarik_say=2, konsol=False)
for (cx, cy) in ((PX0, PY0), (PX1, PY0)):
    chhatri(y, cx, cy, ZT + 0.033, 0.045, n=6, kolon=TR, kubbe=KR, kaide=SUR, kat=math.pi / 6, kaide_h=0.0)

# the pavings inside (inset from the rampart's walk)
I = KAL + 0.001
for (x0, x1, y0, y1, zz) in ((PX0 + I, JX0, PY0 + I, PY1 - I, ZT), (JX0, PX1 - I, JY1, PY1 - I, ZT), (JX0, PX1 - I, PY0 + I, JY1, ZJ)):
    y.yuz_yon([V(x0, y0, zz), V(x1, y0, zz), V(x1, y1, zz), V(x0, y1, zz)], 'zemin', Z)
# Jaleb Chowk's retaining walls up to the upper terrace (its west side with the stair, its north side)
nis_satir(y, V(JX0, PY0 + I), V(JX0, JY1), ZJ, ZT, 6, (KR, KR2, TR, KR2), en=0.5, derin=0.008, sivri=0.45)
duz_duvar(y, V(JX0, JY1), V(PX1 - I, JY1), ZJ, ZT, KR)

# ---------------- the elephant ramp and the Suraj Pol ----------------
y.bolum('Fil yokuşu ve Suraj Pol')
RX0, RX1 = 0.95, 1.06
EB = (JY1 - (PY0 + I)) / 7                  # the east range's bay
Y_A, Y_B = -0.5, JY1 - EB * 3.5


def rampa(p0, p1, z0, z1, en, key=SUR, sag_bas=0.0):
    """a walled ramp from p0 (z0) to p1 (z1), en wide: a solid sloping causeway with low parapets. sag_bas: the
    left-hand side wall (A0) starts that fraction along (another ramp arrives there)"""
    p0, p1 = V(p0[0], p0[1]), V(p1[0], p1[1])
    e = (p1 - p0).normalized(); nn = V(e.y, -e.x)
    A0, A1, B0, B1 = p0 - nn * (en / 2), p0 + nn * (en / 2), p1 - nn * (en / 2), p1 + nn * (en / 2)
    y.yuz_yon([A0 + Z * z0, B0 + Z * z1, B1 + Z * z1, A1 + Z * z0], 'zemin', Z)
    for (a, b, s) in ((A1, B1, 1), (A0, B0, -1)):
        za = z0
        if s < 0 and sag_bas:
            a, za = a.lerp(b, sag_bas), z0 + (z1 - z0) * sag_bas
            y.yuz_yon([a + Z * za, a - nn * s * 0.012 + Z * za, a - nn * s * 0.012 + Z * (za + 0.025), a + Z * (za + 0.025)], key, -e)
        y.yuz_yon([a, b, b + Z * (z1 + 0.025), a + Z * (za + 0.025)], key, nn * s)
        y.yuz_yon([a - nn * s * 0.012 + Z * za, b - nn * s * 0.012 + Z * z1, b - nn * s * 0.012 + Z * (z1 + 0.025), a - nn * s * 0.012 + Z * (za + 0.025)], key, -nn * s)
        y.yuz_yon([a + Z * (za + 0.025), b + Z * (z1 + 0.025), b - nn * s * 0.012 + Z * (z1 + 0.025), a - nn * s * 0.012 + Z * (za + 0.025)], TR, Z)
    y.yuz_yon([A0, A1, A1 + Z * (z0 + 0.025), A0 + Z * (z0 + 0.025)], key, -e)


# the ramp climbs north along the rampart to a landing, turns west through the Suraj Pol (its side wall open where
# the first flight arrives)
Y_C = Y_B - 0.055
rampa((RX0 + 0.055, Y_A - 0.03), (RX0 + 0.055, Y_C), 0.075, ZJ, 0.11)
rampa((RX1, Y_B), (PX1 + 0.03, Y_B), ZJ, ZJ, 0.11, sag_bas=(RX1 - RX0) / (RX1 - PX1 - 0.03))
# Suraj Pol: a gate tower in the east rampart, facing the ramp
SGY = Y_B
sk = dikdortgen(PX1 - I - 0.09, PX1 + 0.03, SGY - EB * 1.5, SGY + EB * 1.5)
y.kemerli(sk[1], sk[2], ZJ, 0.22, (KR, KR2, TR, 'ahsap'), v0=0.0, en=0.52, ust=0.06, derin=0.03, k_say=10, sivri=0.55, cerceve=(0.008, [TR, KIR]))
for i in (0, 2):
    duz_duvar(y, sk[i], sk[(i + 1) % 4], ZJ - 0.03, ZJ + 0.22, KR)
y.kemerli(sk[3], sk[0], ZJ, 0.22, (KR, KR2, TR, 'ahsap'), v0=0.0, en=0.52, ust=0.06, derin=0.03, k_say=10, sivri=0.55)
silme(y, sk, ZJ + 0.205, 0.015, 0.012, TR, 'kaba')
y.yuz_yon([V(p.x, p.y, ZJ + 0.22) for p in sk], 'zemin', Z)
chhatri(y, sk[1].x - 0.035, SGY, ZJ + 0.22, 0.028, n=4, kolon=TR, kubbe=KR, kaide=KIR, kat=math.pi / 4)
y.prizma(((sk[0].x + sk[2].x) / 2, SGY), 0.03, ZJ + 0.22, ZJ + 0.24, KR, n=12)
lotus_kubbe(y, ((sk[0].x + sk[2].x) / 2, SGY), 0.03, ZJ + 0.24, 0.032, KR, n=14, kat=5, yaprak=TR, s_son=0.6)

# ---------------- Jaleb Chowk ----------------
y.bolum('Jaleb Chowk')
KH, KD = 0.1, 0.09


def revak(p, q, nb, z0, h, d, atla=()):
    """an arcaded range p->q facing its right into a court, its back d behind: arches, roof, chhajja, parapet"""
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    L = (q - p).length
    for j in range(nb):
        if j in atla: continue
        u0, u1 = p.lerp(q, j / nb), p.lerp(q, (j + 1) / nb)
        y.kemerli(u0, u1, z0, h, (KR, KR2, TR, KR2), v0=0.0, en=0.72, ust=0.018, derin=d * 0.75, k_say=8, sivri=0.5, cerceve=(0.004, TR))
    back = [p - nn * d, q - nn * d]
    duz_duvar(y, back[1], back[0], z0, z0 + h, KR)            # (it stands above the rampart: its back shows)
    y.yuz_yon([p + Z * (z0 + h), q + Z * (z0 + h), back[1] + Z * (z0 + h), back[0] + Z * (z0 + h)], 'zemin', Z)
    chhajja(y, [p, q], z0 + h - 0.012, 0.012, 0.02, TR, kapali=False)
    kutu(y, p + Z * (z0 + h), e, L, 0.01, 0.018, TR)
    for u in (p, q):
        y.yuz_yon([u + Z * z0, u - nn * d + Z * z0, u - nn * d + Z * (z0 + h), u + Z * (z0 + h)], KR, e * (-1 if u is p else 1))


# south range (backing onto the south rampart), east range (with the gate), north range (under the upper terrace)
revak(V(PX1 - I - KD, PY0 + I + KD), V(JX0, PY0 + I + KD), 7, ZJ, KH, KD)
revak(V(PX1 - I - KD, JY1), V(PX1 - I - KD, PY0 + I), 7, ZJ, KH, KD, atla=(2, 3, 4))
revak(V(JX0, JY1 - KD), V(PX1 - I - KD, JY1 - KD), 7, ZJ, KH, KD)
# the grand stair up the west side to the Diwan-i-Aam court
merdiven(y, (JX0 + 0.11, -0.2), math.pi, 0.12, ZJ, ZT, n=8, d=0.11 / 8, key=KR2, yanlik=TR)
for (x, yy, a, g) in ((0.5, -0.2, 0.0, 'boya_kirmizi'), (0.6, -0.1, 2.0, 'boya_sari'), (0.42, -0.28, 1.0, 'beyaz')):
    adam(y, x, yy, ZJ, a, g, 'boya_kirmizi', boy=0.045)
fil(y, 0.62, -0.2, ZJ, math.pi, 1.0, cul='boya_kirmizi', haudah='altin', binici='boya_sari', kaba=True)

# ---------------- the Diwan-i-Aam ----------------
y.bolum('Divan-ı Am')
DX0, DX1, DY0, DY1 = -0.06, 0.26, -0.42, -0.18
kutu(y, V(DX0 - 0.015, DY0 - 0.015, ZT), X, DX1 - DX0 + 0.03, DY1 - DY0 + 0.03, 0.022, KIR2, 'onarkasagsolust')
zd = ZT + 0.022
DH = 0.12
for i in range(6):
    for j in range(4):
        x = DX0 + 0.015 + (DX1 - DX0 - 0.03) * i / 5
        yy = DY0 + 0.015 + (DY1 - DY0 - 0.03) * j / 3
        dbl = j in (0,) or i in (0, 5)
        for o in ((-0.008, 0.0), (0.008, 0.0)) if dbl else ((0.0, 0.0),):
            cx, cy = x + o[0], yy + o[1]
            kutu_merkez(y, (cx, cy), 0.016, 0.016, 0.01, TR, z0=zd)
            kutu_merkez(y, (cx, cy), 0.011, 0.011, DH - 0.03, KIR, z0=zd + 0.01, yuzler='onarkasagsol')
            kutu_merkez(y, (cx, cy), 0.016, 0.016, 0.02, 'mermer', z0=zd + DH - 0.02)
        for a in (0.0, math.pi / 2):            # elephant-head brackets (stepped corbels) under the beams
            kutu_merkez(y, (x, yy), 0.034, 0.01, 0.01, 'mermer', z0=zd + DH - 0.012, aci=a)
dk = dikdortgen(DX0 - 0.01, DX1 + 0.01, DY0 - 0.01, DY1 + 0.01)
kutu(y, V(dk[0].x, dk[0].y, zd + DH), X, DX1 - DX0 + 0.02, DY1 - DY0 + 0.02, 0.018, KIR, 'onarkasagsolust')
y.yuz_yon([V(p.x, p.y, zd + DH) for p in reversed(dk)], 'mermer', -Z)
chhajja(y, dk, zd + DH, 0.018, 0.025, KIR2)
kk2 = disa(dk, -0.004)
kutu_merkez(y, ((DX0 + DX1) / 2, (DY0 + DY1) / 2), DX1 - DX0 + 0.012, DY1 - DY0 + 0.012, 0.02, KIR, z0=zd + DH + 0.018, yuzler='onarkasagsol')
for i in range(4):
    a, b = kk2[i], kk2[(i + 1) % 4]
    kafes(y, a, b, zd + DH + 0.018, 0.04, 0.96, 0.004, 0.016, KIR2, int((b - a).length / 0.025), 1, 0.003, 0.0015)
y.yuz_yon([V(p.x, p.y, zd + DH + 0.038) for p in disa(dk, -0.004)], 'zemin', Z)
for (x, yy) in ((DX0 + 0.03, DY0 + 0.03), (DX1 - 0.03, DY0 + 0.03)):
    chhatri(y, x, yy, zd + DH + 0.038, 0.028, n=4, kolon=TR, kubbe='mermer', kaide=KIR, kat=math.pi / 4)

# ---------------- the Ganesh Pol ----------------
y.bolum('Ganesh Pol')
GX0, GX1, GY0, GY1 = -0.22, 0.06, -0.08, 0.04
GH = [0.14, 0.09, 0.08]
gk = dikdortgen(GX0, GX1, GY0, GY1)
zg = ZT
BOYA = ('boya_yesil', 'boya_kirmizi', 'boya_sari', 'turkuaz')


def boyali_pano(p, q, z0, z1, keys, f=0.004):
    """a painted panel on a wall p->q (facing its right): a coloured field in a light frame, a hair proud"""
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    d1, d2 = nn * 0.0025, nn * 0.004
    y.yuz_yon([p + d1 + Z * z0, q + d1 + Z * z0, q + d1 + Z * z1, p + d1 + Z * z1], keys[0], nn)
    y.yuz_yon([p + e * f + d2 + Z * (z0 + f), q - e * f + d2 + Z * (z0 + f), q - e * f + d2 + Z * (z1 - f), p + e * f + d2 + Z * (z1 - f)], keys[1], nn)
    for (a, b) in ((p + e * f + Z * (z0 + f), q - e * f + Z * (z0 + f)), (q - e * f + Z * (z1 - f), p + e * f + Z * (z1 - f))):
        y.yuz_yon([a + d1, b + d1, b + d2, a + d2], keys[1], (Z if a.z < z0 + f + 1e-6 else -Z) * -1)
    for (a, b) in ((p + e * f + Z * (z0 + f), p + e * f + Z * (z1 - f)), (q - e * f + Z * (z1 - f), q - e * f + Z * (z0 + f))):
        y.yuz_yon([a + d1, b + d1, b + d2, a + d2], keys[1], -e if a is not None and (a - p).dot(e) < 0.01 + f else e)
    for (a, b, o) in ((p + Z * z0, q + Z * z0, -Z), (q + Z * z1, p + Z * z1, Z), (p + Z * z1, p + Z * z0, -e), (q + Z * z0, q + Z * z1, e)):
        y.yuz_yon([a, b, b + d1, a + d1], keys[0], o)


# storey 1: the great cusped gateway, painted panels either side
y.kemerli(gk[0], gk[1], zg, GH[0], (KR, KR2, TR, 'ahsap'), v0=0.0, en=0.36, ust=0.03, derin=0.04, k_say=12, sivri=0.55, cerceve=(0.008, ['boya_yesil', 'boya_kirmizi']))
for i in (1, 2, 3):
    duz_duvar(y, gk[i], gk[(i + 1) % 4], zg, zg + sum(GH), KR)
for s in (-1, 1):
    xc = (GX0 + GX1) / 2 + s * 0.09
    boyali_pano(V(xc - 0.035, GY0), V(xc + 0.035, GY0), zg + 0.02, zg + 0.11, ('boya_sari', 'boya_yesil'))
boyali_pano(V((GX0 + GX1) / 2 - 0.035, GY0), V((GX0 + GX1) / 2 + 0.035, GY0), zg + GH[0] - 0.026, zg + GH[0] - 0.004, ('boya_sari', 'boya_kirmizi'))
chhajja(y, [V(GX0, GY0), V(GX1, GY0)], zg + GH[0] - 0.012, 0.012, 0.02, TR, kapali=False)
# storey 2: latticed windows (the queens watched through them) and painted bands
z2 = zg + GH[0]
nw = 5
for j in range(nw):
    p, q = V(GX0 + (GX1 - GX0) * j / nw, GY0), V(GX0 + (GX1 - GX0) * (j + 1) / nw, GY0)
    y.kemerli(p, q, z2, GH[1], (KR, KR2, TR, 'koyu'), v0=0.012, en=0.56, ust=0.016, derin=0.01, k_say=8, sivri=0.0, cerceve=(0.004, BOYA[j % 4]))
    kafes(y, p, q, z2, 0.22, 0.78, 0.012, GH[1] - 0.03, TR, 3, 4, 0.0025, 0.004)
chhajja(y, [V(GX0, GY0), V(GX1, GY0)], z2 + GH[1] - 0.012, 0.012, 0.022, TR, kapali=False)
# storey 3: the Suhag Mandir pavilion with jharokhas, set back
z3 = z2 + GH[1]
for j in range(3):
    p, q = V(GX0 + 0.02 + (GX1 - GX0 - 0.04) * j / 3, GY0), V(GX0 + 0.02 + (GX1 - GX0 - 0.04) * (j + 1) / 3, GY0)
    jharokha(y, p, q, z3 + 0.012, 0.06, GH[2] - 0.025, 0.026, key=KR, trim=TR, kubbe=(j != 1), perde=TR, kubbe_key=KR)
duz_duvar(y, V(GX0, GY0), V(GX1, GY0), z3, z3 + GH[2], KR)
zt = z3 + GH[2]
silme(y, gk, zt - 0.014, 0.014, 0.012, TR, 'kaba')
y.yuz_yon([V(p.x, p.y, zt) for p in gk], 'zemin', Z)
# the roof: a central bangla pavilion flanked by two chhatris
bx = (GX0 + GX1) / 2
kutu_merkez(y, (bx, (GY0 + GY1) / 2), 0.09, 0.06, 0.05, KR, z0=zt)
bangla(y, bx - 0.05, bx + 0.05, (GY0 + GY1) / 2 - 0.035, (GY0 + GY1) / 2 + 0.035, zt + 0.05, 0.03, 0.012, KR, ns=8, nr=5, kenar=TR)
for s in (-1, 1):
    chhatri(y, bx + s * 0.105, (GY0 + GY1) / 2, zt, 0.028, n=6, kolon=TR, kubbe=KR, kaide=KIR, kat=math.pi / 6)
# the stair up to the gate from the court

# ---------------- Jai Mandir, Aram Bagh, Sukh Niwas ----------------
y.bolum('Jai Mandir, Aram Bagh, Sukh Niwas')
AX0, AX1, AY0, AY1 = -0.7, -0.28, 0.12, 0.44
# the char-bagh: four sunken beds, water channels, a fountain
y.yuz_yon([V(AX0, AY0, ZT + 0.004), V(AX1, AY0, ZT + 0.004), V(AX1, AY1, ZT + 0.004), V(AX0, AY1, ZT + 0.004)], 'mermer', Z)
cx, cy = (AX0 + AX1) / 2, (AY0 + AY1) / 2
for sx in (-1, 1):
    for sy in (-1, 1):
        bx0, bx1 = (cx + 0.02, AX1 - 0.02) if sx > 0 else (AX0 + 0.02, cx - 0.02)
        by0, by1 = (cy + 0.02, AY1 - 0.02) if sy > 0 else (AY0 + 0.02, cy - 0.02)
        kutu(y, V(bx0, by0, ZT + 0.004), X, bx1 - bx0, by1 - by0, 0.01, 'mermer', 'onarkasagsol')
        y.yuz_yon([V(bx0, by0, ZT + 0.014), V(bx1, by0, ZT + 0.014), V(bx1, by1, ZT + 0.014), V(bx0, by1, ZT + 0.014)], 'cimen', Z)
        # a star bed and cypresses
        mx, my = (bx0 + bx1) / 2, (by0 + by1) / 2
        kutu_merkez(y, (mx, my), 0.05, 0.05, 0.006, 'boya_kirmizi', z0=ZT + 0.014, aci=math.pi / 4)
        agac(y, bx0 + 0.02, by0 + 0.02, ZT + 0.014, boy=0.08, tur='servi', key='yesil_koyu')
        agac(y, bx1 - 0.02, by1 - 0.02, ZT + 0.014, boy=0.08, tur='servi', key='yesil_koyu')
for (a, b) in ((V(AX0 + 0.02, cy), V(AX1 - 0.02, cy)), (V(cx, AY0 + 0.02), V(cx, AY1 - 0.02))):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    y.yuz_yon([a - nn * 0.007 + Z * (ZT + 0.0055), b - nn * 0.007 + Z * (ZT + 0.0055), b + nn * 0.007 + Z * (ZT + 0.0055), a + nn * 0.007 + Z * (ZT + 0.0055)], 'su', Z)
y.prizma((cx, cy), 0.028, ZT + 0.004, ZT + 0.016, 'mermer', n=8, kat=math.pi / 8)
y.prizma((cx, cy), 0.022, ZT + 0.016, ZT + 0.0165, 'su', n=8, kat=math.pi / 8)
# Jai Mandir: the white marble hall on the garden's south: a cusped arcade below, a pavilion storey above, bangla roofs
JM = (AX0, AX1, -0.02, AY0)
jk = dikdortgen(*JM)
for j in range(6):
    p, q = jk[3].lerp(jk[2], j / 6), jk[3].lerp(jk[2], (j + 1) / 6)
    y.kemerli(q, p, ZT, 0.12, ('mermer', 'mermer', 'mermer', 'koyu'), v0=0.0, en=0.72, ust=0.02, derin=0.035, k_say=12, sivri=0.45, cerceve=(0.004, 'altin'))
for i in (0, 1, 3):
    p, q = jk[i], jk[(i + 1) % 4]
    nw = max(1, int(round((q - p).length / 0.2)))
    for j in range(nw):
        y.kemerli(p.lerp(q, j / nw), p.lerp(q, (j + 1) / nw), ZT, 0.12, ('mermer', 'mermer', 'mermer', 'koyu'), v0=0.04, en=0.4, ust=0.025, derin=0.012, k_say=8, sivri=0.45)
chhajja(y, jk, ZT + 0.108, 0.012, 0.02, 'mermer')
y.yuz_yon([V(p.x, p.y, ZT + 0.12) for p in jk], 'zemin', Z)
jm2 = dikdortgen(JM[0] + 0.08, JM[1] - 0.08, JM[2] + 0.02, JM[3] - 0.02)
for i in range(4):
    p, q = jm2[i], jm2[(i + 1) % 4]
    nw = max(1, int(round((q - p).length / 0.09)))
    for j in range(nw):
        y.kemerli(p.lerp(q, j / nw), p.lerp(q, (j + 1) / nw), ZT + 0.12, 0.08, ('mermer', 'mermer', 'mermer', 'koyu'), v0=0.01, en=0.55, ust=0.015, derin=0.01, k_say=8, sivri=0.45, cerceve=(0.003, 'altin'))
bangla(y, jm2[0].x, jm2[1].x, jm2[0].y, jm2[2].y, ZT + 0.2, 0.04, 0.018, 'mermer', ns=10, nr=5, kenar='mermer')
for (x, yy) in ((JM[0] + 0.035, JM[2] + 0.035), (JM[1] - 0.035, JM[2] + 0.035)):
    chhatri(y, x, yy, ZT + 0.12, 0.024, n=4, kolon='mermer', kubbe='mermer', kaide='mermer', kat=math.pi / 4)
# Sukh Niwas: the pavilion on the garden's north, its own bangla roof
SN = (AX0, AX1, AY1, AY1 + 0.12)
sk2 = dikdortgen(*SN)
for j in range(5):
    p, q = sk2[0].lerp(sk2[1], j / 5), sk2[0].lerp(sk2[1], (j + 1) / 5)
    y.kemerli(p, q, ZT, 0.11, ('siva', 'siva_krem', 'mermer', 'koyu'), v0=0.0, en=0.7, ust=0.018, derin=0.03, k_say=10, sivri=0.45, cerceve=(0.004, KIR))
for i in (1, 2, 3):
    duz_duvar(y, sk2[i], sk2[(i + 1) % 4], ZT, ZT + 0.11, 'siva')
chhajja(y, sk2, ZT + 0.098, 0.012, 0.02, TR)
y.yuz_yon([V(p.x, p.y, ZT + 0.11) for p in sk2], 'zemin', Z)
bangla(y, SN[0] + 0.01, SN[1] - 0.01, SN[2] + 0.01, SN[3] - 0.01, ZT + 0.11, 0.045, 0.02, KR, ns=10, nr=5, kenar=TR)
# the garden's west wall with a kiosk
kutu_merkez(y, (AX0 - 0.03, cy), 0.04, AY1 - AY0, 0.06, KR, z0=ZT)
chhatri(y, AX0 - 0.03, cy, ZT + 0.06, 0.026, n=4, kolon=TR, kubbe=KR, kaide=KIR, kat=math.pi / 4)

# ---------------- Sila Devi temple ----------------
y.bolum('Sila Devi tapınağı')
TX, TY = -0.45, -0.28
kutu_merkez(y, (TX, TY), 0.2, 0.16, 0.02, 'mermer', z0=ZT)
zt0 = ZT + 0.02
kutu_merkez(y, (TX, TY + 0.02), 0.1, 0.1, 0.08, 'mermer', z0=zt0)
chhajja(y, dikdortgen(TX - 0.05, TX + 0.05, TY - 0.03, TY + 0.07), zt0 + 0.068, 0.012, 0.012, 'mermer')
zs = zt0 + 0.08
# the shikhara: a curvilinear Nagara tower (square in plan, its storeys marked by small ledges), four half-spires
# (urushringas) clustered on its faces, an amalaka and a kalasha
K2 = math.sqrt(2)
SC = (TX, TY + 0.02)


def egri_kule(c, s0, h, z, key='mermer', kat_say=7):
    """a square curvilinear spire: half-side s0 at z narrowing along a bulging curve to 0.36 s0 at z + h"""
    pr = []
    for k in range(kat_say + 1):
        t = k / kat_say
        s = s0 * (1 - 0.64 * t ** 1.6)
        zz = z + h * t
        if 0 < k < kat_say:
            pr += [(s * K2 * 1.04, zz - h * 0.012), (s * K2, zz)]
        else:
            pr.append((s * K2, zz))
    pr.append((0.0, z + h))
    donel(y, c, pr, key, n=4, kat=math.pi / 4)
    return z + h, s0 * 0.36


for d in (V(1, 0), V(-1, 0), V(0, 1), V(0, -1)):
    egri_kule((SC[0] + d.x * 0.028, SC[1] + d.y * 0.028), 0.022, 0.085, zs, kat_say=4)
zs, st = egri_kule(SC, 0.048, 0.15, zs)
donel(y, SC, [(0.0, zs - 0.002), (0.024, zs - 0.002), (0.03, zs + 0.006), (0.024, zs + 0.014), (0.0, zs + 0.014)], 'mermer', n=16, dilim=['mermer', TR])
zs += 0.012
kalasa(y, TX, TY + 0.02, zs, 0.8)
# its pillared porch (mandapa)
for (u, v) in ((-0.04, -0.07), (0.04, -0.07), (-0.04, -0.03), (0.04, -0.03)):
    kutu_merkez(y, (TX + u, TY + v), 0.012, 0.012, 0.06, 'mermer', z0=zt0)
kutu_merkez(y, (TX, TY - 0.05), 0.1, 0.06, 0.012, 'mermer', z0=zt0 + 0.06)
lotus_kubbe(y, (TX, TY - 0.05), 0.026, zt0 + 0.072, 0.026, 'mermer', n=12, kat=5, yaprak='mermer', s_son=0.5)

# ---------------- the zenana wing (between the gardens and the old palace) ----------------
y.bolum('Zenana')
ZX0, ZX1, ZY0, ZY1 = -0.2, 0.06, 0.12, 0.56
zk_ = dikdortgen(ZX0, ZX1, ZY0, ZY1)
zz_ = ZT
for si, h in enumerate((0.11, 0.09)):
    for i in range(4):
        p, q = zk_[i], zk_[(i + 1) % 4]
        nw = max(1, int(round((q - p).length / 0.1)))
        for j in range(nw):
            y.kemerli(p.lerp(q, j / nw), p.lerp(q, (j + 1) / nw), zz_, h, SV, v0=0.03 if si == 0 else 0.02, en=0.4, ust=0.02, derin=0.01, k_say=6, sivri=0.5)
    chhajja(y, zk_, zz_ + h - 0.012, 0.012, 0.018, KIR2)
    zz_ += h
y.yuz_yon([V(p.x, p.y, zz_) for p in zk_], 'zemin', Z)
for i in range(4):
    a, b = zk_[i], zk_[(i + 1) % 4]
    kutu(y, a + Z * zz_, (b - a).normalized(), (b - a).length, 0.01, 0.016, TR)
for yy_ in (ZY0 + 0.07, ZY1 - 0.07):
    chhatri(y, (ZX0 + ZX1) / 2, yy_, zz_, 0.034, n=6, kolon=TR, kubbe=KR, kaide=KIR, kat=math.pi / 6)
# the Diwan court: a pool, cypress rows, courtiers
havuz(y, -0.7, -0.56, -0.4, -0.12, ZT, derin=0.01, kenar=0.012, key='mermer')
for k in range(5):
    for xx in (-0.74, -0.52):
        agac(y, xx, -0.4 + k * 0.07, ZT, boy=0.1, tur='servi', key='yesil_koyu')
for (x, yy, a, g) in ((-0.2, -0.3, 1.0, 'boya_kirmizi'), (-0.12, -0.25, 2.5, 'boya_sari'), (-0.3, -0.12, 0.3, 'beyaz'), (0.1, -0.12, 1.6, 'turkuaz')):
    adam(y, x, yy, ZT, a, g, 'boya_kirmizi', boy=0.045)

# ---------------- the Man Singh palace ----------------
y.bolum('Man Singh sarayı')
MX0, MX1, MY0, MY1 = 0.12, 0.8, 0.16, 0.58
KATLAR = [0.13, 0.12, 0.11]
mk = dikdortgen(MX0, MX1, MY0, MY1)
# the inner court
CX0, CX1, CY0, CY1 = 0.3, 0.62, 0.28, 0.46
ck = dikdortgen(CX0, CX1, CY0, CY1)
zz = ZT
for si, h in enumerate(KATLAR):
    for i in range(4):
        p, q = mk[i], mk[(i + 1) % 4]
        L = (q - p).length
        nw = max(1, int(round(L / 0.13)))
        for j in range(nw):
            u0, u1 = p.lerp(q, j / nw), p.lerp(q, (j + 1) / nw)
            if si == 0:
                y.kemerli(u0, u1, zz, h, SV, v0=0.035, en=0.32, ust=0.03, derin=0.012, k_say=6, sivri=0.5)
            else:
                y.kemerli(u0, u1, zz, h, SV, v0=0.025, en=0.46 if si == 1 else 0.56, ust=0.02, derin=0.014, k_say=6, sivri=0.5, cerceve=(0.004, KIR) if si == 2 else None)
        # the court's inner faces: the narrow court shows only its top storey from outside, so the lower two are
        # plain plastered walls, the top one an arcade of windows
        a, b = ck[(i + 1) % 4], ck[i]
        if si < 2:
            duz_duvar(y, a, b, zz, zz + h, KR)
        else:
            nb = max(2, int(round((b - a).length / 0.12)))
            for j in range(nb):
                y.kemerli(a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb), zz, h, SV, v0=0.03, en=0.36, ust=0.025, derin=0.01, k_say=6, sivri=0.5)
    chhajja(y, mk, zz + h - 0.012, 0.012, 0.022, KIR2)
    zz += h
    if si == 0:
        # jharokhas on the second storey's south front
        for xj in (0.28, 0.46, 0.64):
            jharokha(y, V(xj - 0.04, MY0), V(xj + 0.04, MY0), zz + 0.02, 0.07, 0.07, 0.03, key=KR, trim=TR, perde=TR)
# roof: the terrace round the court, a parapet
for (x0, x1, y0, y1) in ((MX0, MX1, MY0, CY0), (MX0, MX1, CY1, MY1), (MX0, CX0, CY0, CY1), (CX1, MX1, CY0, CY1)):
    y.yuz_yon([V(x0, y0, zz), V(x1, y0, zz), V(x1, y1, zz), V(x0, y1, zz)], 'zemin', Z)
y.yuz_yon([V(p.x, p.y, ZT + 0.002) for p in ck], 'zemin', Z)
for i in range(4):
    a, b = mk[i], mk[(i + 1) % 4]
    kutu(y, a + Z * zz, (b - a).normalized(), (b - a).length, 0.012, 0.016, TR)
    sivri_mazgal(y, a, b, zz + 0.016, 0.018, 0.012, TR, w=0.018, g=0.04, uc=0.01)
# (the court is too deep and narrow to be seen into from outside: no pavilion in it)
# domed corner kiosks (square towers, a storey above the roof) and a crowning pavilion over the south front
for (x, yy) in ((MX0 + 0.06, MY0 + 0.06), (MX1 - 0.06, MY0 + 0.06), (MX0 + 0.06, MY1 - 0.06), (MX1 - 0.06, MY1 - 0.06)):
    tk = dikdortgen(x - 0.05, x + 0.05, yy - 0.05, yy + 0.05)
    for i in range(4):
        y.kemerli(tk[i], tk[(i + 1) % 4], zz, 0.08, SV, v0=0.012, en=0.5, ust=0.012, derin=0.01, k_say=8, sivri=0.5)
    chhajja(y, tk, zz + 0.07, 0.012, 0.018, KIR2)
    y.yuz_yon([V(p.x, p.y, zz + 0.08) for p in tk], 'zemin', Z)
    y.prizma((x, yy), 0.044, zz + 0.08, zz + 0.095, KR, n=12, ust=True)
    lotus_kubbe(y, (x, yy), 0.043, zz + 0.095, 0.05, KR, n=12, kat=6, yaprak=TR, s_son=0.8, sogan=True)
# the crowning pavilion with a bangla roof and the banner
PCX, PCY = (MX0 + MX1) / 2, MY0 + 0.07
pk = dikdortgen(PCX - 0.09, PCX + 0.09, PCY - 0.05, PCY + 0.05)
for i in range(4):
    nw = 3 if i % 2 == 0 else 2
    for j in range(nw):
        y.kemerli(pk[i].lerp(pk[(i + 1) % 4], j / nw), pk[i].lerp(pk[(i + 1) % 4], (j + 1) / nw), zz, 0.075, SV, v0=0.01, en=0.6, ust=0.01, derin=0.012, k_say=8, sivri=0.0, cerceve=(0.004, KIR))
chhajja(y, pk, zz + 0.063, 0.012, 0.02, KIR2)
bangla(y, PCX - 0.095, PCX + 0.095, PCY - 0.055, PCY + 0.055, zz + 0.075, 0.05, 0.022, KR, ns=10, nr=5, kenar=TR)
sancak(y, PCX + 0.13, PCY - 0.03, zz, boy=0.24, en=0.13, yuk=0.075, aci=-0.5)

# ---------------- the walls climbing the ridge, the Jaigarh watchtower ----------------
y.bolum('Sırt surları ve Jaigarh')


def ornek(yol, adim=0.05):
    pts = []
    for i in range(len(yol) - 1):
        a, b = V(*yol[i]), V(*yol[i + 1])
        n = max(1, int(math.ceil((b - a).length / adim)))
        pts += [a.lerp(b, k / n) for k in range(n)]
    pts.append(V(*yol[-1]))
    return pts


def sirt_suru(yol, W=0.035, H=0.05):
    """a wall following the ridge along yol: its walk slopes with the ground (mitred joints between the sampled
    stretches), both faces down below the ground, merlons on the outer (right) edge stepping along the slope"""
    O = ornek(yol)
    n = len(O)
    sol = lambda v: V(-v.y, v.x)
    T = [sol((O[min(i + 1, n - 1)] - O[max(i - 1, 0)]).normalized()) * (W / 2) for i in range(n)]   # half-width, to the left
    Zt = [yuk(p.x, p.y) + H for p in O]
    Zb = [yuk(p.x, p.y) - 0.035 for p in O]
    for i in range(n - 1):
        a, b = O[i], O[i + 1]
        e = (b - a).normalized(); nr = V(e.y, -e.x)
        R0, R1, L0, L1 = a - T[i], b - T[i + 1], a + T[i], b + T[i + 1]
        y.yuz_yon([R0 + Z * Zb[i], R1 + Z * Zb[i + 1], R1 + Z * Zt[i + 1], R0 + Z * Zt[i]], SUR, nr)
        y.yuz_yon([L1 + Z * Zb[i + 1], L0 + Z * Zb[i], L0 + Z * Zt[i], L1 + Z * Zt[i + 1]], SUR, -nr)
        y.yuz_yon([R0 + Z * Zt[i], R1 + Z * Zt[i + 1], L1 + Z * Zt[i + 1], L0 + Z * Zt[i]], 'zemin', Z)
        # merlons a hair inside the outer face, sunk into the sloping walk as deep as the slope needs
        L = (b - a).length
        k = max(1, int(round(L / 0.042)))
        w = min(0.02, L / k * 0.55)
        egim = abs(Zt[i + 1] - Zt[i]) / max(L, 1e-6)
        for j in range(k):
            u = (j + 0.25) / k
            p = R0.lerp(R1, u) + nr * (-0.0015)
            zz = Zt[i] + (Zt[i + 1] - Zt[i]) * (u + w / L / 2)
            dus = egim * w / 2 + 0.003
            kutu(y, p + Z * (zz - dus), e, w, 0.012, 0.02 + dus, SUR, 'onarkasagsolust')
    # the two ends
    for i, ic in ((0, 1), (n - 1, n - 2)):
        a = O[i]
        yuz_dis(y, [a - T[i] + Z * Zb[i], a + T[i] + Z * Zb[i], a + T[i] + Z * Zt[i], a - T[i] + Z * Zt[i]], SUR, O[ic])
    return O


SIRT1 = [(PX1, 0.45), (1.02, 0.66), (0.96, 0.9), (0.78, 1.06)]
SIRT2 = [(PX0, 0.42), (-0.98, 0.62), (-0.92, 0.88), (-0.6, 1.04), (-0.2, 1.08), (0.3, 1.1), (0.78, 1.06)]
for yol in (SIRT1, SIRT2):
    O = sirt_suru(yol)
    for p in (V(*yol[k]) for k in range(1, len(yol) - 1)):
        zz0 = yuk(p.x, p.y)
        kule_yuvarlak(y, (p.x, p.y), 0.04, zz0 - 0.03, 0.12, SUR, cati='duz', mazgal_h=0.022, n=8, yarik_say=1, konsol=False)
# the Diya Burj: a tall square watchtower with a kiosk on top
JTX, JTY = 0.78, 1.06
zj0 = yuk(JTX, JTY) - 0.03
kule_kare(y, JTX, JTY, 0.11, zj0, 0.26, SUR, cati='duz', mazgal_h=0.026, yarik_say=2, konsol=True)
chhatri(y, JTX, JTY, zj0 + 0.26 + 0.012, 0.038, n=4, kolon=TR, kubbe=KR, kaide=SUR, kat=math.pi / 4, kaide_h=0.0)

# ---------------- elephants on the ramp, trees ----------------
y.bolum('Filler ve ağaçlar')
for (yy, s) in ((-0.42, 1.0), (-0.26, 1.0)):
    t = (yy - (Y_A - 0.03)) / (Y_C - (Y_A - 0.03))
    fil(y, RX0 + 0.055, yy, 0.075 + (ZJ - 0.075) * t, math.pi / 2, 0.95, cul='boya_kirmizi' if yy < -0.3 else 'boya_yesil',
        haudah='altin', binici='boya_sari', kaba=True)
for (x, yy) in ((-1.05, -0.3), (-0.95, -0.45), (1.08, 0.2), (1.1, 0.45), (-0.4, 0.8), (0.2, 0.82), (0.6, 0.78), (-1.05, 0.95),
                (0.45, -0.52), (-0.7, -0.52), (1.1, -0.5)):
    agac(y, x, yy, yuk(x, yy) - 0.005, boy=0.14, tur='yaprakli', key='yesil_koyu' if int(abs(x) * 10) % 2 else 'zeytin')

bolum_say(y)
calistir(y, 'lm_amberkalesi')
