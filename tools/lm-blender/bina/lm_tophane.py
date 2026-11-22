# Tophane-i Amire (lm_tophane): the Ottoman cannon foundry. A five-domed casting hall and a single-domed hall in
# almasik (stone-and-brick banded) walls with pointed windows and oculi, lead domes on windowed drums, furnace
# chimneys; in front a walled yard with a portal, cast cannons on carriages, a great bombard on a timber crane,
# stacks of cannon balls, and the Tophane clock tower.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04
DUVAR = ('tugla', 'tas_koyu', 'kirec', 'cam')
CER = (0.008, ['kirec', 'tugla'])          # alternating stone / brick voussoirs


# ---------------------------------------------------------------- helpers
def serit_tas(p, q, z0, u0, u1, zb, hb, key='kirec', d=0.003):
    """a raised stone course on the wall p->q (faces its right) from u0..u1 (distance along) and zb..zb+hb"""
    if u1 - u0 < 0.004: return
    W = (q - p).length; e = (q - p) / W; nc = V(e.y, -e.x)
    A = p + e * u0 + Z * (z0 + zb); B = p + e * u1 + Z * (z0 + zb)
    up = Z * hb; o = nc * d
    y.yuz_yon([A + o, B + o, B + o + up, A + o + up], key, nc)
    y.yuz_yon([A + up, B + up, B + o + up, A + o + up], key, Z)
    y.yuz_yon([A, B, B + o, A + o], key, -Z)
    y.yuz_yon([A, A + o, A + o + up, A + up], key, -e)   # (the ends)
    y.yuz_yon([B, B + o, B + o + up, B + up], key, e)


BANT = [(0.0, 0.022)] + [(0.05 + 0.058 * k, 0.02) for k in range(12)]


def almasik(a, b, z0, H, n, en=0.42, v0=0.035, ust=0.03, sivri=0.55, kapi_bay=None, bantlar=BANT):
    """a banded wall a->b of n bays with pointed windows (bay kapi_bay: a door)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        W = (q - p).length
        kapi_mi = (k == kapi_bay)
        ee, vv = (0.62, 0.0) if kapi_mi else (en, v0)
        if kapi_mi:
            kapi(y, p, q, z0, ee, H, ('tugla', 'tas_koyu', 'kirec', 'ahsap'), sivri=sivri, derin=0.03, cerceve=(0.01, ['kirec', 'tugla']))
        else:
            y.kemerli(p, q, z0, H, DUVAR, v0=vv, en=ee, ust=ust, derin=0.025, k_say=6, sivri=sivri, cerceve=CER)
        x0, x1 = (1 - ee) / 2 * W, (1 + ee) / 2 * W
        tepe = H - (max(0.01, H * 0.08) if kapi_mi else ust)
        m = CER[0] + 0.004
        for zb, hb in bantlar:
            if zb >= H - 0.004: continue
            hb = min(hb, H - 0.004 - zb)
            if zb + hb <= vv - 0.014 or zb >= tepe + m:
                serit_tas(p, q, z0, 0, W, zb, hb)
            else:
                serit_tas(p, q, z0, 0, x0 - m, zb, hb)
                serit_tas(p, q, z0, x1 + m, W, zb, hb)


def oculus_kusak(a, b, z0, H, n, r=0.02):
    """a banded upper zone a->b with a round window in each of n bays"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    duz_duvar(y, a, b, z0, z0 + H, 'tugla')
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    zc = H * 0.48
    for k in range(n):
        u0, u1 = W * k / n, W * (k + 1) / n
        uc = (u0 + u1) / 2
        y.oculus(a + e * uc + Z * (z0 + zc), e, nc, r, 'cam', 'kirec', f=0.006)
        for zb, hb in ((0.006, 0.016), (H - 0.03, 0.016)):
            if zb + hb < zc - r - 0.008 or zb > zc + r + 0.008:
                serit_tas(a, b, z0, u0, u1, zb, hb)
            else:
                serit_tas(a, b, z0, u0, uc - r - 0.01, zb, hb)
                serit_tas(a, b, z0, uc + r + 0.01, u1, zb, hb)


def bina(x0, x1, y0, y1, H1, H2, nx, ny, kapi_on=None, kapi_arka=None):
    """a banded hall: windowed lower zone H1, an oculus zone H2, cornices, corner piers, a lead flat roof. Returns roof z"""
    k = dikdortgen(x0, x1, y0, y1)
    sayi = [nx, ny, nx, ny]
    kapilar = [kapi_on, None, kapi_arka, None]
    for i in range(4):
        almasik(k[i], k[(i + 1) % 4], Z0, H1, sayi[i], kapi_bay=kapilar[i])
        oculus_kusak(k[i], k[(i + 1) % 4], Z0 + H1, H2, sayi[i] if sayi[i] < 8 else (sayi[i] + 1) // 2)
    zr = Z0 + H1 + H2
    kornis(y, x0, x1, y0, y1, Z0, 0.03, 0.012, 'kirec', 'kaide')
    kornis(y, x0, x1, y0, y1, Z0 + H1 - 0.004, 0.012, 0.008, 'kirec')
    silme(y, k, zr - 0.016, 0.022, 0.018, 'kirec', 'tac')
    for p in k:   # corner piers in cut stone
        kutu_merkez(y, (p.x, p.y), 0.05, 0.05, zr - Z0 + 0.008, 'kirec', z0=Z0)
        kutu_merkez(y, (p.x, p.y), 0.058, 0.058, 0.012, 'tas_acik', z0=zr + 0.008)
    y.yuz_yon([V(p.x, p.y, zr + 0.006) for p in k], 'kursun', Z)
    return zr


def baca(cx, cy, z0, h, r=0.026):
    """an octagonal tapering furnace chimney in brick with stone bands and a cap"""
    donel(y, (cx, cy), [(r * 1.25, z0), (r * 1.25, z0 + 0.03), (r, z0 + 0.04), (r * 0.78, z0 + h)], 'tugla', n=8, kat=math.pi / 8)
    for t in (0.35, 0.7):
        rr = r - (r - r * 0.78) * (0.04 + (h - 0.04) * t - 0.04) / (h - 0.04)
        halka_kornis(y, (cx, cy), rr, z0 + 0.04 + (h - 0.04) * t, 0.01, 0.004, 8, 'kirec', kat=math.pi / 8)
    zt = z0 + h
    halka_kornis(y, (cx, cy), r * 0.78, zt - 0.012, 0.014, 0.008, 8, 'kirec', kat=math.pi / 8, profil='tac')
    y.prizma((cx, cy), r * 0.78 + 0.008, zt + 0.002, zt + 0.004, 'kirec', n=8, ust=False, kat=math.pi / 8)
    donel(y, (cx, cy), [(r * 0.78 + 0.008, zt + 0.004), (r * 0.78 + 0.004, zt + 0.004), (r * 0.78 + 0.004, zt + 0.001)], 'kirec', n=8, kat=math.pi / 8)   # (the lip's top and inside)
    y.yuz_yon([V(p.x, p.y, zt + 0.001) for p in cokgen((cx, cy), r * 0.78 + 0.008, 8, math.pi / 8)], 'koyu', Z)
    # a small lead hood on posts over the mouth
    for i in range(4):
        a = math.pi / 4 + TAU * i / 4
        y.prizma((cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)), 0.003, zt, zt + 0.03, 'demir', n=4, ust=False)
    y.koni((cx, cy), r * 1.05, zt + 0.03, 0.03, 'kursun', n=8)


def tekerlek(c, eksen, R, gen, key='ahsap_koyu'):
    """a spoked-look wheel: a short disc along eksen with an iron tyre and a hub"""
    c, e = Vector(c), Vector(eksen).normalized()
    boru(y, [c - e * gen / 2, c + e * gen / 2], R, 'demir', n=14)
    boru(y, [c - e * (gen / 2 + 0.001), c + e * (gen / 2 + 0.001)], R * 0.86, key, n=14)
    boru(y, [c - e * (gen / 2 + 0.006), c + e * (gen / 2 + 0.006)], R * 0.25, 'demir', n=8)


def namlu(a, b, r0, r1, key='bronz'):
    """a cast bronze barrel from breech a to muzzle b: reinforcing rings, muzzle swell, cascabel"""
    a, b = Vector(a), Vector(b)
    t = (b - a).normalized()
    boru(y, [a, b], r0, key, n=14, r_son=r1)
    L = (b - a).length
    for f, s in ((0.06, 1.12), (0.3, 1.08), (0.55, 1.07)):
        rr = (r0 + (r1 - r0) * f) * s
        boru(y, [a + t * (L * f), a + t * (L * f + 0.012)], rr, key, n=14)
    boru(y, [b - t * 0.03, b], r1 * 1.25, key, n=14, r_son=r1 * 1.35)
    y.yuz_yon([b + Z.cross(t).normalized() * (r1 * 0.7 * math.cos(TAU * i / 10)) + t.cross(Z.cross(t)).normalized() * (r1 * 0.7 * math.sin(TAU * i / 10)) + t * 0.0012
               for i in range(10)], 'koyu', t)
    kure(y, a - t * (r0 * 0.7), r0 * 0.55, key, n=10, kat=5)


def top_arabali(x, yy, aci, L=0.2, r=0.024):
    """a field cannon on a two-wheeled carriage, muzzle towards aci (radians)"""
    with parca(y, (x, yy, Z0), aci):
        # built pointing +x: trail on -x
        R = 0.036
        for s in (-1, 1):   # cheeks
            cubuk(y, V(-L * 0.55, s * 0.022, 0.006), V(0.03, s * 0.022, R + 0.004), 0.012, 'ahsap', 0.03)
        cubuk(y, V(-L * 0.52, 0, 0.008), V(-L * 0.3, 0, 0.012), 0.044, 'ahsap', 0.012)
        cubuk(y, V(0, -0.05, R), V(0, 0.05, R), 0.01, 'demir')
        for s in (-1, 1):
            tekerlek(V(0, s * 0.043, R), V(0, 1, 0), R, 0.01)
        namlu(V(-L * 0.42, 0, R + 0.03), V(L * 0.62, 0, R + 0.042), r, r * 0.72)


def gulle_yigini(cx, cy, n=4, r=0.013, key='demir'):
    """a square pyramid of cannon balls"""
    for k in range(n):
        m = n - k
        for i in range(m):
            for j in range(m):
                px = cx + (i - (m - 1) / 2) * 2 * r
                py = cy + (j - (m - 1) / 2) * 2 * r
                kure(y, (px, py, Z0 + r + k * r * 1.41), r, key, n=8, kat=4)


def saat(o, e, n, R):
    """a clock face on a wall: dial, gilt ring, hour ticks, hands"""
    y.oculus(o, e, n, R, 'beyaz', 'altin', f=0.006, k=20)
    up = Z
    for i in range(12):
        t = TAU * i / 12
        d = e * math.cos(t) + up * math.sin(t)
        q = d.cross(n).normalized()
        p0, p1 = o + d * (R * 0.78) + n * 0.0045, o + d * (R * 0.94) + n * 0.0045
        w = 0.0018 if i % 3 else 0.003
        y.yuz_yon([p0 - q * w, p0 + q * w, p1 + q * w, p1 - q * w], 'koyu', n)
    for t, L, w in ((math.radians(60), 0.55, 0.003), (math.radians(-20), 0.82, 0.002)):
        d = e * math.cos(t) + up * math.sin(t)
        q = d.cross(n).normalized()
        p0, p1 = o + n * 0.005, o + d * (R * L) + n * 0.005
        y.yuz_yon([p0 - q * w, p0 + q * w, p1 + q * w * 0.4, p1 - q * w * 0.4], 'koyu', n)
    kure(y, o + n * 0.005, 0.004, 'altin', n=6, kat=3)


# ---------------------------------------------------------------- platform
y.bolum('Zemin')
zemin(y, -1.12, 1.12, -0.92, 0.74, Z0, 'tas_koyu', basamak=(('on', 0.3),))

# ---------------------------------------------------------------- the five-domed casting hall
y.bolum('Beş kubbeli döküm salonu (almaşık duvarlar)')
BX0, BX1, BY0, BY1 = -0.36, 1.02, 0.06, 0.64
H1, H2 = 0.21, 0.09
ZR = bina(BX0, BX1, BY0, BY1, H1, H2, 11, 5, kapi_on=5)
# a projecting stone portal round the door
PC = (BX0 + BX1) / 2
PH = ZR - Z0 + 0.07
kutu(y, V(PC - 0.1, BY0 - 0.035, Z0), X, 0.2, 0.035, PH, 'kirec', 'arkasagsol')   # (its back too: it rises above the roof)
y.kemerli(V(PC - 0.1, BY0 - 0.035), V(PC + 0.1, BY0 - 0.035), Z0, PH, ('kirec', 'tas_koyu', 'tas_acik', 'ahsap'), v0=0, en=0.56,
          ust=0.09, derin=0.03, k_say=10, sivri=0.6, cerceve=(0.011, ['mermer', 'tugla']))
ZP = Z0 + PH
kornis(y, PC - 0.1, PC + 0.1, BY0 - 0.035, BY0, ZP - 0.012, 0.016, 0.01, 'tas_acik', 'tac')
y.yuz_yon([V(PC - 0.1, BY0 - 0.035, ZP + 0.004), V(PC + 0.1, BY0 - 0.035, ZP + 0.004), V(PC + 0.1, BY0, ZP + 0.004), V(PC - 0.1, BY0, ZP + 0.004)], 'tas_acik', Z)
for sx in (-1, 1):
    y.koni((PC + sx * 0.088, BY0 - 0.02), 0.012, ZP + 0.004, 0.035, 'kursun', n=8)
# inscription panel over the door (tughra plaque)
zp0, zp1 = ZP - 0.07, ZP - 0.032
y.yuz_yon([V(PC - 0.05, BY0 - 0.0385, zp0), V(PC + 0.05, BY0 - 0.0385, zp0), V(PC + 0.05, BY0 - 0.0385, zp1), V(PC - 0.05, BY0 - 0.0385, zp1)], 'boya_yesil', -Y)
kutu(y, V(PC - 0.055, BY0 - 0.0395, zp0 - 0.004), X, 0.11, 0.004, 0.004, 'altin', 'onust')
kutu(y, V(PC - 0.055, BY0 - 0.0395, zp1), X, 0.11, 0.004, 0.004, 'altin', 'onust')
for i in range(5):
    kutu(y, V(PC - 0.036 + i * 0.016, BY0 - 0.0392, zp0 + 0.008), X, 0.006, 0.0015, 0.022, 'altin', 'on')

y.bolum('Kubbeler')
SP = (BX1 - BX0) / 5
for i in range(5):
    cx = BX0 + SP * (i + 0.5)
    orta = (i == 2)
    r = 0.122 if orta else 0.108
    # a square base under each drum with a small cornice
    kutu_merkez(y, (cx, (BY0 + BY1) / 2), r * 2 + 0.03, r * 2 + 0.03, 0.025 if orta else 0.012, 'kirec', z0=ZR + 0.006)
    zb = ZR + 0.006 + (0.025 if orta else 0.012)
    kubbe_kasnakli(y, (cx, (BY0 + BY1) / 2), r, zb, 0.07 if orta else 0.055, 12, kubbe_h=r * 0.82, duvar=('kirec', 'tas_koyu', 'tas_acik', 'cam'),
                   alem_olcek=1.0 if orta else 0.8, n=48, kat=12, cerceve=(0.004, 'tugla'))

y.bolum('Ocak bacaları')
for i in (1, 2, 3, 4):
    cx = BX0 + SP * i
    baca(cx, BY1 - 0.04, ZR + 0.006, 0.2 if i in (2, 3) else 0.16)

# ---------------------------------------------------------------- the single-domed hall
y.bolum('Tek kubbeli salon')
TX0, TX1, TY0, TY1 = -1.03, -0.45, -0.02, 0.62
T1, T2 = 0.24, 0.1
ZT = bina(TX0, TX1, TY0, TY1, T1, T2, 5, 5, kapi_on=2)
TC = ((TX0 + TX1) / 2, (TY0 + TY1) / 2)
# octagonal base, the drum and the great dome
y.prizma(TC, 0.27, ZT + 0.006, ZT + 0.05, 'kirec', n=8, kat=math.pi / 8, ust=True)
halka_kornis(y, TC, 0.27, ZT + 0.04, 0.012, 0.01, 8, 'tas_acik', kat=math.pi / 8)
kubbe_kasnakli(y, TC, 0.235, ZT + 0.05, 0.085, 16, kubbe_h=0.2, duvar=('kirec', 'tas_koyu', 'tas_acik', 'cam'), alem_olcek=1.3, n=64, kat=16,
               cerceve=(0.005, 'tugla'))
for sx in (-1, 1):   # small corner domes (weight turrets)
    for sy in (-1, 1):
        kucuk_kubbe(y, TC[0] + sx * 0.215, TC[1] + sy * 0.245, ZT + 0.006, 0.04, kasnak=0.03, n=20, key='kursun', kasnak_key='kirec')

# the link between the halls
y.bolum('Bağlantı ve arka avlu')
LX0, LX1 = TX1, BX0
almasik(V(LX0, 0.14), V(LX1, 0.14), Z0, 0.2, 1)
almasik(V(LX1, 0.52), V(LX0, 0.52), Z0, 0.2, 1)
y.yuz_yon([V(LX0, 0.14, Z0 + 0.2), V(LX1, 0.14, Z0 + 0.2), V(LX1, 0.52, Z0 + 0.2), V(LX0, 0.52, Z0 + 0.2)], 'kursun', Z)
silme(y, [V(LX0, 0.14), V(LX1, 0.14)], Z0 + 0.19, 0.014, 0.01, 'kirec', 'tac', kapali=False)
silme(y, [V(LX1, 0.52), V(LX0, 0.52)], Z0 + 0.19, 0.014, 0.01, 'kirec', 'tac', kapali=False)

# ---------------------------------------------------------------- the yard
y.bolum('Avlu duvarı ve taçkapı')
AY0 = -0.86
YH = 0.075


def avlu_duvari(a, b):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    L = (b - a).length
    kutu(y, a + nc * 0.015 + Z * Z0, e, L, 0.03, YH, 'tas', 'onarka')
    # coping
    kutu(y, a + nc * 0.02 - e * 0.0 + Z * (Z0 + YH), e, L, 0.04, 0.012, 'kirec', 'onarkaust')
    serit_tas(a + nc * 0.015, b + nc * 0.015, Z0, 0, L, 0.035, 0.012, 'tugla', 0.002)
    n = max(1, int(L / 0.18))
    for k in range(n + 1):   # piers
        p = a.lerp(b, k / n)
        kutu_merkez(y, (p.x, p.y), 0.04, 0.045, YH + 0.025, 'kirec', z0=Z0)
        kure(y, (p.x, p.y, Z0 + YH + 0.025 + 0.012), 0.012, 'kirec', n=8, kat=4)


avlu_duvari(V(-1.08, AY0), V(-0.13, AY0))
avlu_duvari(V(-1.08, -0.04), V(-1.08, AY0))
avlu_duvari(V(0.13, AY0), V(1.08, AY0))
avlu_duvari(V(1.08, AY0), V(1.08, -0.04))
y.yuz_yon([V(-1.08, -0.04, Z0 + 0.002), V(-1.08, AY0, Z0 + 0.002), V(1.08, AY0, Z0 + 0.002), V(1.08, -0.04, Z0 + 0.002)], 'toprak', Z)


def tas_doseme(x0, x1, y0, y1, key='granit', bordur=True):
    """a paved strip on the yard floor with a low stone kerb on its open edges"""
    zt = Z0 + 0.0045
    y.yuz_yon([V(x0, y0, zt), V(x1, y0, zt), V(x1, y1, zt), V(x0, y1, zt)], key, Z)
    for a, b in ((V(x0, y0), V(x1, y0)), (V(x1, y0), V(x1, y1)), (V(x1, y1), V(x0, y1)), (V(x0, y1), V(x0, y0))):
        duz_duvar(y, a + Z * (Z0 + 0.002), b + Z * (Z0 + 0.002), Z0 + 0.002, zt, 'kirec')


# paved aprons along the yard walls and in front of the halls (the rest stays beaten earth)
tas_doseme(-1.065, -0.15, AY0 + 0.03, AY0 + 0.085)
tas_doseme(0.15, 1.065, AY0 + 0.03, AY0 + 0.085)
tas_doseme(-1.065, -1.01, AY0 + 0.085, -0.04)
tas_doseme(1.01, 1.065, AY0 + 0.085, -0.04)
tas_doseme(BX0 - 0.01, BX1, -0.045, BY0, 'zemin')
tas_doseme(TX0, TX1 + 0.01, -0.085, TY0, 'zemin')
# the portal: a pishtaq facing the street with a plain back
tackapi(y, 0, AY0, Z0, en=0.24, H=0.22, derin=0.06, kapi_key='ahsap', cerceve=(0.012, ['mermer', 'tugla']))
y.kemerli(V(0.12, AY0 + 0.03), V(-0.12, AY0 + 0.03), Z0, 0.22, ('tas', 'tas_koyu', 'tas_acik', 'ahsap'), v0=0, en=0.6, ust=0.05, derin=0.02,
          k_say=10, sivri=0.6)
sancak(y, 0.1, AY0 - 0.01, Z0 + 0.25, boy=0.2, en=0.12, yuk=0.075, aci=math.pi)

# ---------------------------------------------------------------- cannons, the bombard, the crane
y.bolum('Toplar, gülleler, döküm vinci')
for i, x in enumerate((-0.62, -0.38, 0.36, 0.6)):
    top_arabali(x, -0.6 if i in (0, 3) else -0.66, -math.pi / 2 + (0.08 if x < 0 else -0.08), L=0.2)
gulle_yigini(-0.82, -0.3, 4)
gulle_yigini(-0.72, -0.72, 3)
gulle_yigini(0.18, -0.42, 3)
# a great bombard on timber blocks (Sahi topu), lying along x
for x in (0.38, 0.62):
    kutu_merkez(y, (x, -0.22), 0.04, 0.12, 0.03, 'ahsap', z0=Z0)
namlu(V(0.3, -0.22, Z0 + 0.03 + 0.05), V(0.78, -0.22, Z0 + 0.03 + 0.05), 0.05, 0.04)
# the casting crane: a timber tripod with a chain and block over the bombard
TP = V(0.55, -0.22, Z0 + 0.34)
for a in (math.radians(100), math.radians(220), math.radians(340)):
    cubuk(y, V(0.55 + 0.17 * math.cos(a), -0.22 + 0.15 * math.sin(a), Z0), TP, 0.012, 'ahsap')
kure(y, TP + Z * 0.008, 0.016, 'ahsap_koyu', n=8, kat=4)
cubuk(y, TP - Z * 0.01, V(0.55, -0.22, Z0 + 0.16), 0.004, 'demir')
kutu_merkez(y, (0.55, -0.22), 0.022, 0.016, 0.03, 'ahsap_koyu', z0=Z0 + 0.135)
cubuk(y, V(0.55, -0.22, Z0 + 0.135), V(0.55, -0.22, Z0 + 0.082), 0.003, 'demir')
# casting moulds and crates by the hall
for k, (x, yy) in enumerate(((-0.2, -0.12), (-0.12, -0.18), (0.86, -0.12))):
    kutu_merkez(y, (x, yy), 0.06, 0.05, 0.04, 'ahsap_acik', z0=Z0, aci=0.3 * k)
    kutu_merkez(y, (x, yy), 0.064, 0.008, 0.006, 'ahsap_koyu', z0=Z0 + 0.04, aci=0.3 * k)
y.prizma((-0.28, -0.3), 0.035, Z0, Z0 + 0.06, 'kum_koyu', n=12)           # a clay mould pit rim
y.yuz_yon([V(p.x, p.y, Z0 + 0.0605) for p in cokgen((-0.28, -0.3), 0.025, 12)], 'koyu', Z)

# mortars (havan) aimed high, powder kegs
for k, (x, yy) in enumerate(((0.62, -0.5), (0.7, -0.4))):
    kutu_merkez(y, (x, yy), 0.06, 0.06, 0.02, 'ahsap', z0=Z0)
    a = V(x, yy + 0.012, Z0 + 0.03)
    namlu(a, a + V(0, -0.022, 0.034), 0.03, 0.028)
for x, yy in ((0.2, -0.16), (0.24, -0.13), (0.215, -0.1), (-0.86, -0.12)):
    donel(y, (x, yy), [(0.0, Z0), (0.016, Z0), (0.019, Z0 + 0.02), (0.016, Z0 + 0.04), (0.0, Z0 + 0.04)], 'ahsap_acik', n=10)
    for zz in (Z0 + 0.008, Z0 + 0.03):
        halka_kornis(y, (x, yy), 0.017, zz, 0.004, 0.0015, 10, 'demir')

# a paved way from the gate to the door
y.bolum('Yol ve Tophane çeşmesi')
y.yuz_yon([V(-0.08, AY0 + 0.03, Z0 + 0.004), V(0.08, AY0 + 0.03, Z0 + 0.004), V(0.08, -0.045, Z0 + 0.004), V(-0.08, -0.045, Z0 + 0.004)], 'zemin', Z)
for sx in (-1, 1):
    kutu_merkez(y, (sx * 0.084, (AY0 + 0.03 - 0.045) / 2), 0.008, -0.045 - AY0 - 0.03, 0.007, 'kirec', z0=Z0)

# the Tophane fountain (1732): a square marble kiosk, a niche with a spout on each face, a wide eave, a lead roof
FX, FY = -0.56, -0.34
FW = 0.13
kutu_merkez(y, (FX, FY), FW + 0.05, FW + 0.05, 0.015, 'mermer', z0=Z0)
fk = dikdortgen(FX - FW / 2, FX + FW / 2, FY - FW / 2, FY + FW / 2)
zf = Z0 + 0.015
for j in range(4):
    a, b = fk[j], fk[(j + 1) % 4]
    y.kemerli(a, b, zf, 0.11, ('mermer', 'tas_acik', 'mermer', 'boya_yesil'), v0=0.02, en=0.5, ust=0.02, derin=0.012, k_say=8, sivri=0.4,
              cerceve=(0.006, 'altin'))
    e = (b - a).normalized(); nn = V(e.y, -e.x); m = a.lerp(b, 0.5)
    kutu_merkez(y, (m.x + nn.x * 0.012, m.y + nn.y * 0.012), 0.05 if abs(e.x) > 0.5 else 0.024, 0.024 if abs(e.x) > 0.5 else 0.05, 0.01, 'mermer', z0=zf)
    y.yuz_yon([V(m.x + nn.x * 0.024 + e.x * s, m.y + nn.y * 0.024 + e.y * s, zf + 0.0105) for s in (-0.02, 0.02)] +
              [V(m.x + nn.x * 0.004 + e.x * s, m.y + nn.y * 0.004 + e.y * s, zf + 0.0105) for s in (0.02, -0.02)], 'su', Z)
for p in fk:
    kutu_merkez(y, (p.x, p.y), 0.022, 0.022, 0.11, 'mermer', z0=zf)
kornis(y, FX - FW / 2, FX + FW / 2, FY - FW / 2, FY + FW / 2, zf + 0.1, 0.012, 0.008, 'mermer', 'tac')
cati_kirma(y, FX - FW / 2, FX + FW / 2, FY - FW / 2, FY + FW / 2, zf + 0.112, 0.04, 0.045, 'kursun', alt_key='ahsap_koyu', kalinlik=0.008)
for p in fk:
    kucuk_kubbe(y, p.x, p.y, zf + 0.12, 0.014, kasnak=0.012, n=12, son=False, key='kursun', kasnak_key='mermer')
t = kucuk_kubbe(y, FX, FY, zf + 0.15, 0.025, kasnak=0.02, n=16, son=True, key='kursun', kasnak_key='mermer')

# ---------------------------------------------------------------- the clock tower
y.bolum('Saat kulesi')
SX, SY = 0.86, -0.62
W0 = 0.15
zz = Z0
kutu_merkez(y, (SX, SY), W0 + 0.04, W0 + 0.04, 0.04, 'kirec', z0=zz)                 # plinth
zz += 0.04
for i, (h, w) in enumerate(((0.17, W0), (0.15, W0 - 0.01), (0.12, W0 - 0.02))):
    k = dikdortgen(SX - w / 2, SX + w / 2, SY - w / 2, SY + w / 2)
    for j in range(4):
        a, b = k[j], k[(j + 1) % 4]
        if i == 0:
            y.kemerli(a, b, zz, h, ('kirec', 'tas_koyu', 'tas_acik', 'ahsap' if j == 0 else 'cam'), v0=0.0 if j == 0 else 0.05, en=0.45, ust=0.03,
                      derin=0.02, k_say=8, sivri=0, cerceve=(0.008, 'mermer'))
        elif i == 1:
            y.kemerli(a, b, zz, h, ('kirec', 'tas_koyu', 'tas_acik', 'cam'), v0=0.03, en=0.36, ust=0.025, derin=0.02, k_say=8, sivri=0,
                      cerceve=(0.007, 'mermer'), korkuluk=0.02)
        else:
            duz_duvar(y, a, b, zz, zz + h, 'kirec')
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            saat(a.lerp(b, 0.5) + Z * (zz + h * 0.5), e, nn, w * 0.33)
    for p in k:   # pilasters at the corners
        kutu_merkez(y, (p.x, p.y), 0.02, 0.02, h, 'mermer', z0=zz)
    zz += h
    kornis(y, SX - w / 2, SX + w / 2, SY - w / 2, SY + w / 2, zz - 0.01, 0.016, 0.012, 'mermer', 'tac')
    y.yuz_yon([V(p.x, p.y, zz + 0.006) for p in k], 'tas_acik', Z)
# the lantern and a lead cupola
ok = cokgen((SX, SY), 0.05, 8, math.pi / 8)
for j in range(8):
    y.kemerli(ok[j] + Z * 0.0005 * 0, ok[(j + 1) % 8], zz + 0.006, 0.07, ('kirec', 'tas_koyu', 'tas_acik', 'cam'), v0=0.015, en=0.5, ust=0.01,
              derin=0.008, k_say=4, sivri=0)
halka_kornis(y, (SX, SY), 0.05, zz + 0.072, 0.008, 0.008, 8, 'mermer', kat=math.pi / 8)
t = y.kubbe((SX, SY), 0.056, zz + 0.08, 0.06, 'kursun', n=24, kat=7)
alem(y, SX, SY, t.z, 0.9)

calistir(y, 'lm_tophane')
