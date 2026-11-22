# Kahire Kalesi (lm_kahirekalesi): Saladin's citadel on its rock spur: the cliff of the Muqattam spur with a lower
# terrace before it, Bab al-Azab (a gate between two round, banded towers) in the lower wall, a walled ramp climbing the
# cliff to an upper gate; cut-stone curtain walls with round towers and the great Burj al-Muqattam; on the plateau the
# Mehmed Ali Mosque (alabaster walls, a lead dome on a windowed drum with four half domes, corner domes and turrets, two
# pencil minarets, a domed-arcade courtyard with a clock tower and fountain kiosk), the Mamluk mosque of al-Nasir
# Muhammad with its green-tiled minaret top and dome, the Gawhara palace, cannons on the ramparts and palms.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.04            # the lower ground
ZP = 0.31            # the plateau
SUR, SUR2 = 'kum', 'kum_koyu'
MR, MA = 'mermer', 'tas_acik'
YC = -0.46           # the cliff's top edge (front)

y.bolum('Zemin ve yamaç')
zemin(y, -1.14, 1.14, -1.14, 1.12, Z0, 'kaya_koyu', 'kum_acik', basamak=(), silmeli=False)
# the plateau: its top paved, the rock falling to the lower ground in battered, broken bands
UST = [V(-1.04, YC + 0.01), V(-0.62, YC - 0.03), V(-0.1, YC + 0.01), V(0.42, YC - 0.03), V(0.78, YC), V(1.04, YC - 0.01),
       V(1.06, 0.4), V(1.04, 1.0), V(-1.04, 1.0), V(-1.06, 0.4)]
rng = __import__('random').Random(7)
katlar = [UST]
for k, d in enumerate((0.035, 0.05, 0.075)):
    katlar.append([p + V(rng.uniform(-0.012, 0.012), rng.uniform(-0.012, 0.012)) for p in disa(UST, d)])
zs = [ZP, ZP - 0.07, ZP - 0.13, Z0]
nk = len(UST)
for k in range(3):
    alt, ust = katlar[k + 1], katlar[k]
    for i in range(nk):
        j = (i + 1) % nk
        y.yuz_yon([V(alt[i].x, alt[i].y, zs[k + 1]), V(alt[j].x, alt[j].y, zs[k + 1]), V(ust[j].x, ust[j].y, zs[k]), V(ust[i].x, ust[i].y, zs[k])],
                  'kaya' if k != 1 else 'kaya_koyu', V((alt[j] - alt[i]).y, -(alt[j] - alt[i]).x, 0.3))
y.yuz_yon([V(p.x, p.y, ZP) for p in UST], 'kum_acik', Z)
# a few fallen boulders at the cliff foot
for (bx, by, r) in ((-0.82, -0.58, 0.03), (-0.5, -0.6, 0.022), (0.25, -0.6, 0.026), (0.9, -0.58, 0.03), (-0.2, -0.61, 0.018)):
    kure(y, (bx, by, Z0 + r * 0.4), r, 'kaya', n=7, kat=4)


# ---------------- helpers ----------------
def kademeli_mazgal(a, b, z, t=0.016, key=SUR, w=0.036, g=0.018):
    """Mamluk stepped merlons along a->b (outer face on the line, facing right)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < w: return
    e = (b - a) / L
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g
    for i in range(k):
        o = a + e * (i * (w + g))
        kutu(y, o + Z * z, e, w, t, 0.014, key)
        kutu(y, o + e * (w * 0.25) + Z * (z + 0.014), e, w * 0.5, t, 0.01, key)


def bant_halka(c, R, z, h, key, n):
    """a band ring standing a hair proud of a round tower of radius R (closed at top and bottom)"""
    donel(y, c, [(R, z), (R + 0.0025, z), (R + 0.0025, z + h), (R, z + h)], key, n=n)


def kule(c, r, z0, h, cati='duz', bantli=False, n=None, cati_key='kursun'):
    n = n or 12
    t = kule_yuvarlak(y, c, r, z0, h, key=SUR, cati=cati, cati_key=cati_key, mazgal_h=0.026, n=n, egim=0.08, yarik_say=3, bolum=3)
    if bantli:
        for f in (0.3, 0.55, 0.8):
            zz = z0 + h * f
            R = r * (1 + 0.08 * (1 - f))
            bant_halka(c, R, zz, 0.014, SUR2, n)
    return t


def kubbecik(cx, cy, z, r, kasnak=0.014, n=12, alem_=False, key='kursun', kasnak_key=MR, silmeli=False):
    """a small lead dome on a low drum (with a moulding: silmeli), lighter than parcalar.kucuk_kubbe"""
    y.prizma((cx, cy), r * 1.02, z, z + kasnak, kasnak_key, n=n)
    if silmeli: halka_kornis(y, (cx, cy), r * 1.02, z + kasnak - 0.005, 0.005, 0.005, n, MA)
    t = y.kubbe((cx, cy), r, z + kasnak, r * 0.9, key, n=n, kat=4)
    if alem_: alem(y, cx, cy, t.z, 0.6)
    return t.z


def yarim(c, R, z, aci, kasnak_h=0.05, kubbe_h=0.09, n_pencere=6):
    """a half dome on a windowed half drum, bulging towards aci (lighter than parcalar.yarim_kubbe)"""
    t0 = aci - math.pi / 2
    yay = [V(c[0] + R * math.cos(t0 + math.pi * i / n_pencere), c[1] + R * math.sin(t0 + math.pi * i / n_pencere)) for i in range(n_pencere + 1)]
    for i in range(n_pencere):
        y.kemerli(yay[i], yay[i + 1], z, kasnak_h, (MR, MA, MA, 'cam'), v0=kasnak_h * 0.22, en=0.45, ust=kasnak_h * 0.18, derin=0.016, k_say=4, sivri=0.5)
    zh = z + kasnak_h
    hy = lambda rr, zz: [V(c[0] + rr * math.cos(t0 + math.pi * i / n_pencere), c[1] + rr * math.sin(t0 + math.pi * i / n_pencere), zz) for i in range(n_pencere + 1)]
    y.serit(hy(R, zh), hy(R + 0.01, zh), MA, kapali=False)
    y.serit(hy(R + 0.01, zh), hy(R + 0.01, zh + 0.01), MA, kapali=False)
    y.serit(hy(R + 0.01, zh + 0.01), hy(R + 0.003, zh + 0.01), MA, kapali=False)     # (the moulding's top: open, it showed its underside)
    y.kubbe(c, R + 0.005, zh + 0.01, kubbe_h, 'kursun', n=20, kat=6, t0=t0, t1=t0 + math.pi, kapak=MR)


def palmiye(x, yy, z, boy=0.3):
    tepe = V(x + 0.012, yy + 0.006, z + boy)
    boru(y, [V(x, yy, z), V(x + 0.004, yy + 0.002, z + boy * 0.5), tepe], 0.009, 'ahsap_acik', n=6, r_son=0.007)
    for i in range(6):
        a = TAU * i / 6 + 0.3
        d = V(math.cos(a), math.sin(a))
        L = 0.085 + 0.015 * (i % 2)
        boru(y, [tepe, tepe + d * (L * 0.45) + Z * 0.03, tepe + d * L - Z * 0.02, tepe + d * (L * 1.12) - Z * 0.05], 0.009, 'boya_yesil', n=3, r_son=0.002)
    kure(y, (tepe.x, tepe.y, tepe.z + 0.004), 0.012, 'boya_yesil', n=8, kat=4)


# ---------------- the lower terrace: Bab al-Azab, the lower wall, the ramp ----------------
y.bolum('Bab el-Azab ve aşağı sur')
GX, GY = 0.55, -0.93
# (the lower enceinte is kept low: the cliff, the ramp and the upper walls must read over it from the game's view)
GH, GKH = 0.17, 0.26
top_g = kale_kapisi(y, GX, GY, 0.16, Z0, GH, derin=0.1, key=SUR, kule='yuvarlak', kule_r=0.08, kule_h=GKH, cati='duz', kapi_key='ahsap',
                    sivri=0.5, kule_n=16)
# the towers' banded shafts and the plaque over the gate
for sx in (-1, 1):
    c = (GX + sx * (0.08 + 0.08 * 0.55), GY - 0.1 * 0.1)
    for f in (0.3, 0.55):
        zz = Z0 + GKH * f
        bant_halka(c, 0.08 * (1 + 0.06 * (1 - f)), zz, 0.016, SUR2, 16)
kutu(y, V(GX - 0.045, GY - 0.05 - 0.004, Z0 + 0.122), X, 0.09, 0.004, 0.016, 'mermer', 'onsagsolust')
WL = 0.1
sur(y, [V(-1.02, -0.56), V(-1.02, GY), V(GX - 0.15, GY)], Z0, WL, kalinlik=0.05, key=SUR, mazgal_h=0.022)
sur(y, [V(GX + 0.15, GY), V(1.02, GY), V(1.02, -0.56)], Z0, WL, kalinlik=0.05, key=SUR, mazgal_h=0.022)
for c in ((-1.02, GY), (1.02, GY), (-0.3, GY)):
    kule(c, 0.06, Z0, 0.16)
# the road from the gate to the ramp's foot
y.yuz_yon([V(GX - 0.07, -1.14, Z0 + 0.0015), V(GX + 0.07, -1.14, Z0 + 0.0015), V(GX + 0.07, GY - 0.05, Z0 + 0.0015), V(GX - 0.07, GY - 0.05, Z0 + 0.0015)], 'tas_koyu', Z)
y.yuz_yon([V(GX - 0.07, GY + 0.05, Z0 + 0.0015), V(GX + 0.07, GY + 0.05, Z0 + 0.0015), V(GX + 0.07, -0.67, Z0 + 0.0015), V(GX - 0.07, -0.67, Z0 + 0.0015)], 'tas_koyu', Z)

y.bolum('Yamaçtan çıkan rampa ve yukarı kapı')
RX0, RX1 = -0.05, 0.64          # the ramp: high end at RX0, foot at RX1
RY0, RY1 = -0.68, -0.47
LX0 = -0.5                      # the landing before the upper gate
rz = lambda x: ZP + (Z0 - ZP) * (x - RX0) / (RX1 - RX0)
nr = 8
for k in range(nr):
    xa, xb = RX0 + (RX1 - RX0) * k / nr, RX0 + (RX1 - RX0) * (k + 1) / nr
    # the outer face (a retaining wall), the top (a paved slope)
    y.yuz_yon([V(xa, RY0, Z0), V(xb, RY0, Z0), V(xb, RY0, rz(xb)), V(xa, RY0, rz(xa))], SUR, -Y)
    y.yuz_yon([V(xa, RY0, rz(xa)), V(xb, RY0, rz(xb)), V(xb, RY1, rz(xb)), V(xa, RY1, rz(xa))], 'tas_koyu', Z + X * 0.3)
# the landing
kutu(y, V(LX0, RY0, Z0), X, RX0 - LX0, RY1 - RY0, ZP - Z0, SUR, 'onsolsag')
y.yuz_yon([V(LX0, RY0, ZP), V(RX0, RY0, ZP), V(RX0, RY1, ZP), V(LX0, RY1, ZP)], 'tas_koyu', Z)
# a parapet along the ramp's outer edge and round the landing, stepping up with it
for k in range(nr):
    xa, xb = RX0 + (RX1 - RX0) * k / nr, RX0 + (RX1 - RX0) * (k + 1) / nr
    for (yy, s) in ((RY0, -1), (RY0 + 0.014, 1)):
        a, b = (V(xa, yy), V(xb, yy)) if s < 0 else (V(xb, yy), V(xa, yy))
        e = (b - a).normalized()
        za, zb = rz(a.x), rz(b.x)
        y.yuz_yon([V(a.x, a.y, za), V(b.x, b.y, zb), V(b.x, b.y, zb + 0.03), V(a.x, a.y, za + 0.03)], SUR, V(e.y, -e.x))
    y.yuz_yon([V(xa, RY0, rz(xa) + 0.03), V(xb, RY0, rz(xb) + 0.03), V(xb, RY0 + 0.014, rz(xb) + 0.03), V(xa, RY0 + 0.014, rz(xa) + 0.03)], MA, Z)
y.yuz_yon([V(RX1, RY0, Z0), V(RX1, RY0 + 0.014, Z0), V(RX1, RY0 + 0.014, Z0 + 0.03), V(RX1, RY0, Z0 + 0.03)], SUR, X)
parapet(y, [V(RX0, RY0), V(LX0, RY0), V(LX0, RY1)], ZP, 0.012, 0.022, 0.014, SUR, kapali=False, ust_key=MA)
# the upper gate in the curtain wall
UGX = -0.3
top_ug = kale_kapisi(y, UGX, YC + 0.04, 0.12, ZP, 0.16, derin=0.08, key=SUR, kule='yuvarlak', kule_r=0.06, kule_h=0.24, cati='duz',
                     kapi_key='ahsap', sivri=0.5, kule_n=16)

# ---------------- the curtain walls on the plateau ----------------
y.bolum('Selahaddin surları, burçlar, Mukattam Burcu')
WH = 0.15
WY0, WY1, WX = YC + 0.04, 0.96, 1.0
BURJ = (-0.86, 0.84)
sur(y, [V(UGX + 0.065, WY0), V(WX, WY0), V(WX, WY1), V(-0.78, WY1)], ZP, WH, kalinlik=0.05, key=SUR, mazgal_h=0.026, konsol=True)
sur(y, [V(-WX, 0.78), V(-WX, WY0), V(UGX - 0.065, WY0)], ZP, WH, kalinlik=0.05, key=SUR, mazgal_h=0.026, konsol=True)
for (c, r) in (((WX, WY0), 0.085), ((WX, WY1), 0.085), ((-WX, WY0), 0.085), ((0.38, WY0), 0.06), ((-0.75, WY0), 0.06),
               ((WX, 0.25), 0.065), ((-WX, 0.25), 0.065), ((0.25, WY1), 0.065)):
    kule(c, r, ZP - 0.06, WH + 0.13)
# the Burj al-Muqattam: a great round tower, battered, banded, corbelled, with an open top and a lookout
y.bolum('Mukattam Burcu')
BR, BH = 0.155, 0.36
kule_yuvarlak(y, BURJ, BR, ZP - 0.1, BH + 0.1, key=SUR, cati='duz', mazgal_h=0.034, n=20, egim=0.12, yarik_say=5, bolum=6)
for f in (0.3, 0.5, 0.7):
    zz = ZP - 0.1 + (BH + 0.1) * f
    bant_halka(BURJ, BR * (1 + 0.12 * (1 - f)), zz, 0.016, SUR2, 20)
zt_b = ZP + BH + 0.012
y.prizma(BURJ, 0.05, zt_b, zt_b + 0.08, SUR, n=12, ust=False)
for i in range(4):
    a = TAU * i / 4 + 0.4
    kutu_merkez(y, (BURJ[0] + math.cos(a) * 0.047, BURJ[1] + math.sin(a) * 0.047), 0.008, 0.014, 0.03, 'koyu', z0=zt_b + 0.035, aci=a)
halka_kornis(y, BURJ, 0.05, zt_b + 0.08, 0.012, 0.01, 12, MA)
t = y.kubbe(BURJ, 0.056, zt_b + 0.092, 0.05, 'kursun', n=12, kat=4)
top_b = t.z
sancak(y, BURJ[0], BURJ[1], top_b, boy=0.2, en=0.11, yuk=0.07, aci=-0.5)

# ---------------- the Mehmed Ali Mosque ----------------
y.bolum('Mehmed Ali Camii: harim')
MXc, MYc = 0.05, 0.5
HX0, HX1, HY0, HY1 = MXc - 0.28, MXc + 0.28, MYc - 0.28, MYc + 0.28
H1, H2 = 0.14, 0.12
ZR = ZP + H1 + H2
HK = dikdortgen(HX0, HX1, HY0, HY1)
for i in range(4):
    a, b = HK[i], HK[(i + 1) % 4]
    n = 5
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if i == 0 and k == 2:
            kapi(y, p, q, ZP, 0.5, H1, (MR, MA, MA, 'ahsap'), sivri=0.5, derin=0.02, cerceve=(0.008, MA))
        else:
            dikdortgen_acik(y, p, q, ZP, H1, 0.3, 0.7, 0.03, 0.11, (MR, MA, MA, 'cam'), derin=0.014, cerceve=(0.006, MA))
        y.kemerli(p, q, ZP + H1, H2, (MR, MA, MA, 'cam'), v0=0.02, en=0.42, ust=0.02, derin=0.014, k_say=6, sivri=0.55)
kornis(y, HX0, HX1, HY0, HY1, ZP, 0.02, 0.01, MA, 'kaide')
kornis(y, HX0, HX1, HY0, HY1, ZP + H1 - 0.004, 0.01, 0.008, MA)
kornis(y, HX0, HX1, HY0, HY1, ZR - 0.016, 0.018, 0.014, MA, 'tac')
y.yuz_yon([V(p.x, p.y, ZR + 0.002) for p in HK], 'kursun', Z)
for p in HK:
    kutu_merkez(y, (p.x, p.y), 0.05, 0.05, ZR - ZP + 0.02, MR, z0=ZP)

y.bolum('Mehmed Ali Camii: kubbeler, yarım kubbeler, ağırlık kuleleri')
# the four half domes round the central square, corner domes beyond them
RC = 0.15
for k in range(4):
    a = TAU * k / 4
    c = (MXc + math.cos(a) * RC, MYc + math.sin(a) * RC)
    yarim(c, 0.115, ZR + 0.002, a)
for sx in (-1, 1):
    for sy in (-1, 1):
        kubbecik(MXc + sx * 0.2, MYc + sy * 0.2, ZR + 0.002, 0.058, kasnak=0.03, n=16, alem_=True, silmeli=True)
# the square base of the drum and its weight turrets
y.prizma((MXc, MYc), RC * 1.0, ZR + 0.002, ZR + 0.07, MR, n=16)
for sx in (-1, 1):
    for sy in (-1, 1):
        c = (MXc + sx * 0.122, MYc + sy * 0.122)
        y.prizma(c, 0.03, ZR + 0.002, ZR + 0.15, MR, n=8, kat=math.pi / 8, ust=False)
        halka_kornis(y, c, 0.03, ZR + 0.15, 0.008, 0.006, 8, MA, kat=math.pi / 8)
        y.prizma(c, 0.03, ZR + 0.158, ZR + 0.159, MA, n=8, kat=math.pi / 8)
        tt = y.kubbe(c, 0.026, ZR + 0.158, 0.03, 'kursun', n=12, kat=4)
        alem(y, c[0], c[1], tt.z, 0.45)
top_m = kubbe_kasnakli(y, (MXc, MYc), RC, ZR + 0.07, 0.075, n_pencere=16, kubbe_h=0.17, key='kursun', duvar=(MR, MA, MA, 'cam'), payanda=True,
                       alem_olcek=1.3, sivri=0.5, n=32, kat=10, en=0.5, cerceve=(0.004, MA))

y.bolum('Mehmed Ali Camii: avlu, saat kulesi, şadırvan')
CX0, CX1, CY0, CY1 = MXc - 0.26, MXc + 0.26, -0.3, HY0
CH = 0.15
AK = dikdortgen(CX0, CX1, CY0, CY1)
# outer walls of the court (front, sides): windows, a door in the front under the clock tower
for (a, b, n, kapi_k) in ((AK[3], AK[0], 4, None), (AK[0], AK[1], 5, 2), (AK[1], AK[2], 4, None)):
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if k == kapi_k:
            kapi(y, p, q, ZP, 0.55, CH, (MR, MA, MA, 'ahsap'), sivri=0.5, derin=0.02, cerceve=(0.008, MA))
        else:
            y.kemerli(p, q, ZP, CH, (MR, MA, MA, 'cam'), v0=0.04, en=0.36, ust=0.03, derin=0.014, k_say=6, sivri=0.55, cerceve=(0.005, MA))
silme(y, [AK[3], AK[0], AK[1], AK[2]], ZP, 0.016, 0.008, MA, 'kaide', kapali=False)
silme(y, [AK[3], AK[0], AK[1], AK[2]], ZP + CH - 0.012, 0.014, 0.012, MA, 'tac', kapali=False)
# the riwaq round the court: arches on columns, a small lead dome over each bay
G = 0.075
IK = dikdortgen(CX0 + G, CX1 - G, CY0 + G, CY1 - G)
for (a, b, n) in ((IK[1], IK[0], 3), (IK[0], IK[3], 3), (IK[2], IK[1], 3), (IK[3], IK[2], 4)):
    arkad(y, a, b, n, ZP, CH, en=0.78, ust=0.025, sivri=0.5, derin=G - 0.026, sutun_key=MR, sutun_r=0.01,
          renk=(MR, MR, MA, MA), cerceve=(0.006, MA))
    for k in range(n):
        if a == IK[1] and k == 1: continue      # (the clock tower stands over that bay)
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        e = (q - p).normalized(); nc = V(e.y, -e.x)
        m = (p + q) / 2 - nc * (G / 2)
        kubbecik(m.x, m.y, ZP + CH + 0.002, 0.032, n=8)
for p in IK:
    q = p + (p - V(MXc, (CY0 + CY1) / 2)).normalized() * (G * 0.7)
    kubbecik(q.x, q.y, ZP + CH + 0.002, 0.032, n=8)
for i in range(4):
    a, b, ai, bi = AK[i], AK[(i + 1) % 4], IK[i], IK[(i + 1) % 4]
    y.yuz_yon([a + Z * (ZP + CH + 0.002), b + Z * (ZP + CH + 0.002), bi + Z * (ZP + CH + 0.002), ai + Z * (ZP + CH + 0.002)], 'kursun', Z)
y.yuz_yon([V(p.x, p.y, ZP + 0.002) for p in IK], MR, Z)
FCc = (MXc, (CY0 + CY1) / 2)
sadirvan(y, FCc[0], FCc[1], ZP + 0.002, olcek=0.85)
# the clock tower over the front riwaq
KC = (MXc, CY0 + G / 2)
kutu_merkez(y, KC, 0.07, 0.07, 0.2, MR, z0=ZP + CH + 0.002, yuzler='onarkasagsol')
kornis(y, KC[0] - 0.035, KC[0] + 0.035, KC[1] - 0.035, KC[1] + 0.035, ZP + CH + 0.19, 0.012, 0.008, MA, 'tac')
for (o, ex, nrm) in ((V(KC[0], KC[1] - 0.035), X, -Y), (V(KC[0], KC[1] + 0.035), -X, Y), (V(KC[0] + 0.035, KC[1]), Y, X), (V(KC[0] - 0.035, KC[1]), -Y, -X)):
    y.oculus(o + Z * (ZP + CH + 0.13), ex, nrm, 0.02, 'beyaz', 'altin', f=0.005, k=14)
    for ang in (math.pi / 2, math.pi / 6):
        cubuk(y, o + nrm * 0.0045 + Z * (ZP + CH + 0.13), o + nrm * 0.0045 + Z * (ZP + CH + 0.13) + (ex * math.cos(ang) + Z * math.sin(ang)) * 0.014, 0.002, 'koyu', 0.001)
y.yuz_yon([V(p.x, p.y, ZP + CH + 0.202) for p in dikdortgen(KC[0] - 0.035, KC[0] + 0.035, KC[1] - 0.035, KC[1] + 0.035)], MA, Z)
cati_kirma(y, KC[0] - 0.035, KC[0] + 0.035, KC[1] - 0.035, KC[1] + 0.035, ZP + CH + 0.202, 0.06, 0.008, 'kursun', 'kursun', kalinlik=0.006, ns=4, nr=2)
alem(y, KC[0], KC[1], ZP + CH + 0.262, 0.5, hilal=False)

y.bolum('Mehmed Ali Camii: iki kalem minare')
for sx, mx in ((-1, HX0 - 0.03), (1, HX1 + 0.03)):
    minare(y, mx, HY0 - 0.02, ZP, 0.96, serefe=2, kaide=0.27, r=0.026, key=MR, govde_key=MA, cati_key='kursun')

# ---------------- the mosque of al-Nasir Muhammad ----------------
y.bolum('Nasır Muhammed Camii (yeşil çinili minare)')
NX0, NX1, NY0, NY1 = -0.92, -0.46, -0.34, 0.16
NH = 0.17
NK = dikdortgen(NX0, NX1, NY0, NY1)
for i in range(4):
    a, b = NK[i], NK[(i + 1) % 4]
    n = 3 if i % 2 == 0 else 4
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if i == 0 and k == 1:
            tackapi_mukarnas(y, (p.x + q.x) / 2, NY0 - 0.035, ZP, en=0.12, H=NH + 0.06, derin=0.035, nis=0.6, sivri=0.5, mk_kat=3,
                             kapi_key='ahsap', key=SUR, bordur=(MA, 'tas_koyu'), tonlar=(MA, 'tas_koyu'), cerceve=(0.006, [MA, 'tas_koyu']))
            cxp = (p.x + q.x) / 2
            duz_duvar(y, V(cxp + 0.06, NY0), V(cxp - 0.06, NY0), ZP + NH, ZP + NH + 0.06, SUR)     # (its back above the roof)
            duz_duvar(y, p, V(cxp - 0.06, NY0), ZP, ZP + NH - 0.02, SUR)
            duz_duvar(y, V(cxp + 0.06, NY0), q, ZP, ZP + NH - 0.02, SUR)
            continue
        L_, x0, x1, hs, apex = kemer_nis(y, p, q, ZP, NH - 0.02, en=0.62, ust=0.02, sivri=0.5, derin=0.012, key=SUR, yan_key='tas_koyu',
                                         alt_key=MA, v0=0.025, k_say=6, cerceve=(0.006, [MA, 'tas_koyu']))
        a2, b2 = L_(x0, -ZP, 0.012), L_(x1, -ZP, 0.012)
        y.kemerli(a2, b2, ZP + 0.025, apex - 0.025, (SUR, 'tas_koyu', MA, 'koyu'), v0=0.03, en=0.36, ust=0.02, derin=0.01, k_say=6, sivri=0.5)
    duz_duvar(y, a, b, ZP + NH - 0.02, ZP + NH, SUR)
    # ablaq: dark courses along the wall
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for zz in (ZP + 0.012, ZP + NH - 0.035):
        kutu(y, a + Z * zz + nn * 0.003, e, (b - a).length, 0.003, 0.01, 'tas_koyu', 'onust')
silme(y, NK, ZP + NH - 0.012, 0.014, 0.01, MA, 'tac')
y.yuz_yon([V(p.x, p.y, ZP + NH) for p in NK], 'zemin', Z)
parapet(y, NK, ZP + NH, 0.01, 0, 0.014, SUR, ust_key=MA)
for i in range(4):
    kademeli_mazgal(NK[i], NK[(i + 1) % 4], ZP + NH + 0.01)
# its green-tiled dome over the mihrab
NDc = ((NX0 + NX1) / 2, NY1 - 0.12)
y.prizma(NDc, 0.1, ZP + NH, ZP + NH + 0.05, SUR, n=8, kat=math.pi / 8)
nok = cokgen(NDc, 0.1, 8, math.pi / 8)
for i in range(8):
    p, q = nok[i], nok[(i + 1) % 8]
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    kutu_merkez(y, ((p.x + q.x) / 2 + nn.x * 0.0, (p.y + q.y) / 2 + nn.y * 0.0), 0.016, 0.01, 0.026, 'koyu', z0=ZP + NH + 0.012, aci=math.atan2(nn.y, nn.x))
halka_kornis(y, NDc, 0.1, ZP + NH + 0.05, 0.01, 0.008, 8, MA, kat=math.pi / 8)
t = y.kubbe(NDc, 0.092, ZP + NH + 0.06, 0.1, 'kiremit_yesil', n=24, kat=7)
alem(y, NDc[0], NDc[1], t.z, 0.6)
# the minaret: square base, octagonal shaft, a balcony, a round upper shaft and the green-tiled bulb
MC = (NX1 - 0.02, NY0 + 0.02)
mz = ZP
kutu_merkez(y, MC, 0.08, 0.08, NH + 0.06, SUR, z0=mz, yuzler='onarkasagsol')
kornis(y, MC[0] - 0.04, MC[0] + 0.04, MC[1] - 0.04, MC[1] + 0.04, mz + NH + 0.05, 0.012, 0.008, MA, 'tac')
mz2 = mz + NH + 0.062
y.yuz_yon([V(p.x, p.y, mz2) for p in dikdortgen(MC[0] - 0.048, MC[0] + 0.048, MC[1] - 0.048, MC[1] + 0.048)], MA, Z)
y.prizma(MC, 0.032, mz2, mz2 + 0.14, SUR, n=8, kat=math.pi / 8, ust=False)
ok8 = cokgen(MC, 0.032, 8, math.pi / 8)
for i in range(8):
    p, q = ok8[i], ok8[(i + 1) % 8]
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    m = (p + q) / 2
    kutu_merkez(y, (m.x, m.y), 0.008, 0.01, 0.03, 'koyu', z0=mz2 + 0.07, aci=math.atan2(nn.y, nn.x))
r8 = cokgen(MC, 0.032, 8, math.pi / 8)
konsol_halka(y, r8, mz2 + 0.12, 0.02, 0.016, MA, 3)
rb = disa(r8, 0.016)
y.yuz_yon([V(p.x, p.y, mz2 + 0.1405) for p in rb], MA, Z)
parapet(y, rb, mz2 + 0.14, 0.016, 0, 0.005, SUR, ust_key=MA)
y.prizma(MC, 0.022, mz2 + 0.14, mz2 + 0.22, SUR, n=12)
for i in range(6):
    a = TAU * i / 6
    y.prizma((MC[0] + math.cos(a) * 0.024, MC[1] + math.sin(a) * 0.024), 0.004, mz2 + 0.14, mz2 + 0.22, MA, n=5)
halka_kornis(y, MC, 0.022, mz2 + 0.22, 0.008, 0.008, 12, MA)
tip = sogan_kubbe(y, MC, 0.024, mz2 + 0.228, h=0.07, key='kiremit_yesil', n=16)
alem(y, MC[0], MC[1], tip - 0.004, 0.45, hilal=True)

# ---------------- the Gawhara palace ----------------
y.bolum('Cevhere Sarayı')
PX0, PX1, PY0, PY1 = 0.48, 0.92, 0.36, 0.86
PH1, PH2 = 0.13, 0.11
PKK = dikdortgen(PX0, PX1, PY0, PY1)
for i in range(4):
    a, b = PKK[i], PKK[(i + 1) % 4]
    n = 5 if i % 2 == 0 else 6
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if i == 3 and k == 2:
            kapi(y, p, q, ZP, 0.55, PH1, ('siva', MA, MA, 'ahsap'), sivri=0.0, derin=0.02, cerceve=(0.008, MA))
        else:
            dikdortgen_acik(y, p, q, ZP, PH1, 0.28, 0.72, 0.03, 0.1, ('siva', MA, MA, 'cam'), derin=0.012, cerceve=(0.006, MA))
        dikdortgen_acik(y, p, q, ZP + PH1, PH2, 0.28, 0.72, 0.02, 0.085, ('siva', MA, MA, 'cam'), derin=0.012, cerceve=(0.006, MA))
kornis(y, PX0, PX1, PY0, PY1, ZP, 0.018, 0.008, MA, 'kaide')
kornis(y, PX0, PX1, PY0, PY1, ZP + PH1 - 0.004, 0.01, 0.008, MA)
kornis(y, PX0, PX1, PY0, PY1, ZP + PH1 + PH2 - 0.016, 0.02, 0.016, MA, 'tac')
ZPal = ZP + PH1 + PH2
y.yuz_yon([V(p.x, p.y, ZPal) for p in PKK], 'zemin', Z)
parapet(y, PKK, ZPal, 0.012, 0, 0.012, 'siva', ust_key=MA)
for i in range(4):
    a, b = PKK[i], PKK[(i + 1) % 4]
    e = (b - a).normalized()
    nb = int((b - a).length / 0.035)
    for k in range(nb):
        p = a.lerp(b, (k + 0.5) / nb)
        y.prizma((p.x, p.y), 0.004, ZPal + 0.012, ZPal + 0.032, MA, n=5)
    kutu(y, a + Z * (ZPal + 0.032) - V(e.y, -e.x) * 0.0, e, (b - a).length, 0.01, 0.006, MA, 'onarkasagsolust')
# the belvedere (cihannuma) on the roof: a raised, windowed salon under a hipped lead roof, chimneys round it
BX0, BX1, BY0, BY1 = PX0 + 0.11, PX1 - 0.11, PY0 + 0.13, PY1 - 0.13
BH = 0.075
BK = dikdortgen(BX0, BX1, BY0, BY1)
for i in range(4):
    a, b = BK[i], BK[(i + 1) % 4]
    n = 2
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        y.kemerli(p, q, ZPal, BH, ('siva', MA, MA, 'cam'), v0=0.015, en=0.5, ust=0.012, derin=0.01, k_say=6, sivri=0.0, cerceve=(0.005, MA))
kornis(y, BX0, BX1, BY0, BY1, ZPal, 0.012, 0.006, MA, 'kaide')
kornis(y, BX0, BX1, BY0, BY1, ZPal + BH - 0.012, 0.014, 0.012, MA, 'tac')
y.yuz_yon([V(p.x, p.y, ZPal + BH + 0.002) for p in BK], MA, Z)
tb = cati_kirma(y, BX0 - 0.012, BX1 + 0.012, BY0 - 0.012, BY1 + 0.012, ZPal + BH + 0.002, 0.07, 0.016, 'kursun', 'kursun2', kalinlik=0.008, ns=6, nr=3)
alem(y, (BX0 + BX1) / 2, (BY0 + BY1) / 2, tb, 0.45, hilal=False)
for (cx, cy) in ((PX0 + 0.05, PY0 + 0.05), (PX1 - 0.05, PY0 + 0.05), (PX0 + 0.05, PY1 - 0.05), (PX1 - 0.05, PY1 - 0.05)):
    kutu_merkez(y, (cx, cy), 0.026, 0.026, 0.05, 'siva', z0=ZPal, yuzler='onarkasagsol')
    kornis(y, cx - 0.013, cx + 0.013, cy - 0.013, cy + 0.013, ZPal + 0.044, 0.008, 0.006, MA, 'tac')
    y.prizma((cx, cy), 0.012, ZPal + 0.052, ZPal + 0.068, 'kursun', n=6)
    y.yuz_yon([V(p.x, p.y, ZPal + 0.0525) for p in dikdortgen(cx - 0.019, cx + 0.019, cy - 0.019, cy + 0.019)], MA, Z)
# a columned porch before its door (facing the mosque)
for yy in (0.61, 0.695):
    y.prizma((PX0 - 0.06, yy), 0.008, ZP, ZP + PH1, MR, n=8, ust=False)
    kutu_merkez(y, (PX0 - 0.06, yy), 0.022, 0.022, 0.01, MA, z0=ZP)
kutu(y, V(PX0 - 0.075, 0.59, ZP + PH1), X, 0.075, 0.125, 0.012, MA, 'onarkasagsolust')

# ---------------- ramparts: cannons, trees, paths ----------------
y.bolum('Toplar, ağaçlar, yollar')


def top(cx, cy, aci):
    """a cannon on a wooden carriage pointing towards aci"""
    with parca(y, (cx, cy, ZP), aci):
        kutu_merkez(y, (0, 0), 0.06, 0.035, 0.018, 'ahsap', z0=0.006)
        for s in (-1, 1):
            for wx in (-0.018, 0.018):
                boru(y, [V(wx, s * 0.017, 0.012), V(wx, s * 0.026, 0.012)], 0.012, 'ahsap_koyu', n=8)
        boru(y, [V(-0.035, 0, 0.03), V(0.05, 0, 0.034)], 0.011, 'bronz', n=8, r_son=0.008)
        kure(y, (-0.037, 0, 0.03), 0.01, 'bronz', n=8, kat=4)
        for i in range(3):
            kure(y, (-0.05 + 0.014 * i, 0.03, 0.007), 0.007, 'demir', n=6, kat=3)


for xx in (0.55, 0.7, 0.85):
    top(xx, WY0 + 0.07, -math.pi / 2)
for (tx, ty) in ((0.6, 0.05), (0.85, 0.1), (-0.25, 0.85), (0.65, 0.92), (-0.37, 0.4)):
    palmiye(tx, ty, ZP, boy=0.26)
for (tx, ty) in ((0.48, -0.1), (0.9, -0.12), (0.7, 0.18)):
    agac(y, tx, ty, ZP, boy=0.14, tur='yaprakli', key='zeytin')
for (tx, ty) in ((-0.8, -0.78), (-0.6, -0.8), (0.95, -0.75), (0.15, -0.8), (-0.95, -0.66)):
    palmiye(tx, ty, Z0, boy=0.3)
# paved ways on the plateau: from the upper gate to the mosque court, to the palace
y.yuz_yon([V(UGX - 0.05, WY0 + 0.04, ZP + 0.0015), V(UGX + 0.05, WY0 + 0.04, ZP + 0.0015), V(UGX + 0.05, -0.2, ZP + 0.0015), V(UGX - 0.05, -0.2, ZP + 0.0015)], 'tas_koyu', Z)
y.yuz_yon([V(UGX - 0.05, -0.2, ZP + 0.0015), V(CX0, -0.2, ZP + 0.0015), V(CX0, -0.1, ZP + 0.0015), V(UGX - 0.05, -0.1, ZP + 0.0015)], 'tas_koyu', Z)
y.yuz_yon([V(MXc - 0.05, WY0 + 0.05, ZP + 0.0015), V(MXc + 0.05, WY0 + 0.05, ZP + 0.0015), V(MXc + 0.05, CY0, ZP + 0.0015), V(MXc - 0.05, CY0, ZP + 0.0015)], 'tas_koyu', Z)

calistir(y, 'lm_kahirekalesi')
