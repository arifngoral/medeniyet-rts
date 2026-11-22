# Moskova Kremlini (lm_kremlin): the Moscow Kremlin as a stylised pentagon of red brick walls crowned by swallowtail
# (M-shaped) merlons, round corner towers and square towers with stepped tiers and green tiled tents with lookouts; the
# Spasskaya gate tower on Red Square (tiers, clock faces, a gilded double-headed eagle instead of the star); inside,
# Cathedral Square: the white Dormition (Uspensky) cathedral with five gilded helmet domes, the Archangel cathedral,
# the Ivan the Great bell tower with its gilded dome (the summit), the faceted stone Palace of Facets; before the
# walls the cobbled Red Square with the round Lobnoye Mesto.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from rus_ortak import *
from bina_ortak import calistir
import doku

y = Yapi()
Z0 = 0.04
doku.KOSE_RENK['cimen'] = cayir_renk(Z0)
WH = 0.24                       # wall height above the ground
WT = 0.07                       # wall thickness
TUG, BEY = 'tugla', 'tas_acik'  # red brick, white stone trim
YES = 'kiremit_yesil'           # green glazed tents
# the wall's plan, CCW (outer face to the right of travel)
A, B, C, D, E = V(-1.02, -0.66), V(1.04, -0.66), V(1.04, 0.3), V(0.28, 1.0), V(-1.02, 1.0)
DUV = [A, B, C, D, E]

# ---------------------------------------------------------------- ground, Red Square
y.bolum('Zemin ve Kızıl Meydan')
zemin_blok(y, -1.2, 1.2, -1.16, 1.12, Z0, 'cimen', 'toprak')
yer = lambda pts, k, dz=0.002: y.yuz_yon([V(p[0], p[1], Z0 + dz) for p in pts], k, Z)
yer([(-1.2, -1.16), (1.2, -1.16), (1.2, -0.66), (-1.2, -0.66)], 'zemin')
yer([(-0.78, -0.62), (0.9, -0.62), (0.9, 0.2), (-0.78, 0.2)], 'zemin')


# ---------------------------------------------------------------- towers
def tent(y, c, r, z, h, n=8, kat=math.pi / 8, key=YES, kaburga=BEY, ust=None):
    """a tiled octagonal tent with white ribs on its hips"""
    ring = cokgen(c, r, n, kat)
    tepe = V(c[0], c[1], z + h)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([ring[i] + Z * z, ring[j] + Z * z, tepe], key, (ring[i] + ring[j]) / 2 - V(c[0], c[1]))
        if kaburga:
            cubuk(y, ring[i] + Z * z + (ring[i] - V(c[0], c[1])).normalized() * 0.003, tepe, 0.007, kaburga)
    y.yuz_yon([p + Z * z for p in ring], 'ahsap_koyu', -Z)
    return z + h


def nobet(y, c, r, z, h=0.06, tent_h=0.07, vane=True):
    """the little open lookout (smotrovaya vyshka) on a tent: eight posts, a rail, its own tent and a gilded vane"""
    ring = cokgen(c, r, 8, math.pi / 8)
    y.prizma(c, r * 1.15, z, z + 0.008, BEY, n=8, kat=math.pi / 8)
    for p in ring[::2]:
        y.prizma((p.x, p.y), 0.004, z + 0.008, z + h, BEY, n=5, ust=False)
    silme(y, ring, z + h - 0.006, 0.008, 0.004, BEY, 'duz')
    y.prizma(c, r * 0.5, z + 0.008, z + h, 'koyu', n=8)
    t = tent(y, c, r * 1.12, z + h + 0.002, tent_h, kaburga=None)
    if vane:
        y.prizma(c, 0.003, t - 0.005, t + 0.05, 'altin', n=5)
        kure(y, (c[0], c[1], t + 0.012), 0.008, 'altin', n=8, kat=4)
        levha(y, [V(c[0] + 0.003, c[1], t + 0.026), V(c[0] + 0.03, c[1], t + 0.028), V(c[0] + 0.03, c[1], t + 0.044), V(c[0] + 0.003, c[1], t + 0.046)],
              'altin', -Y)
    return t


def kirlangic_halka(y, kose, z, h, t, key=TUG):
    """a ring (closed CCW polygon) of swallowtail merlons with the solid parapet band under them"""
    n = len(kose)
    ic = disa(kose, -t)
    for i in range(n):
        j = (i + 1) % n
        a, b = kose[i], kose[j]
        duz_duvar(y, a, b, z, z + 0.012, key)
        duz_duvar(y, ic[j], ic[i], z, z + 0.012, key)
        y.yuz_yon([a + Z * (z + 0.012), b + Z * (z + 0.012), ic[j] + Z * (z + 0.012), ic[i] + Z * (z + 0.012)], key, Z)
        L = (b - a).length
        w_, g_ = (L * 0.62, L * 0.38) if L < 0.07 else (0.034, 0.022)
        kirlangic(y, a, b, z + 0.012, h, t, key, w=w_, g=g_, yarik_key=None)


def kule_yuv(y, c, r, h, tier_h=0.13, tent_h=0.3, n=16):
    """a round Kremlin corner tower: battered brick shaft, a white string course, machicolations under swallowtail
    merlons, an octagonal upper tier with arched openings, a green tent with white ribs and a lookout"""
    zt = Z0 + h
    donel(y, c, [(r * 1.06, Z0), (r, Z0 + h * 0.4), (r, zt)], TUG, n=n)
    silme(y, cokgen(c, r * 1.06, n), Z0, 0.03, 0.012, BEY, 'kaide')
    silme(y, cokgen(c, r * 1.0, n), Z0 + h * 0.55, 0.012, 0.006, BEY, 'duz')
    for k in range(6):
        a = TAU * k / 6 + 0.3
        nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
        for t in (0.3, 0.72):
            yarik(y, V(c[0], c[1]) + nn * (r * (1.06 - 0.06 * min(1, t / 0.4)) + 0.0008) + Z * Z0, e, nn, -0.005, h * t, 0.01, 0.04, 'koyu')
    konsol_halka(y, cokgen(c, r, n), zt - 0.04, 0.04, 0.018, TUG, 2)
    ring = cokgen(c, r + 0.018, n)
    kirlangic_halka(y, ring, zt, 0.05, 0.016)
    y.yuz_yon([V(p.x, p.y, zt + 0.0005) for p in disa(ring, -0.016)], 'zemin', Z)
    r2 = r * 0.68
    k8 = cokgen(c, r2, 8, math.pi / 8)
    pencereli_duvar(y, k8, zt, tier_h, [1, 0, 1, 0, 1, 0, 1, 0], renk=(TUG, 'tugla_koyu', BEY, 'koyu'), v0=0.02, en=0.5, ust=0.02,
                    derin=0.014, sivri=0.0, cerceve=None, k_say=6)
    silme(y, k8, zt + tier_h - 0.014, 0.014, 0.01, BEY, 'kaba')
    t = tent(y, c, r2 + 0.012, zt + tier_h, tent_h)
    return nobet(y, c, 0.024, t - tent_h * 0.12, 0.05, 0.055)


def kule_kare_k(y, cx, cy, w, h, tier_h=0.11, tent_h=0.28, d=None, gozcu=True):
    """a square Kremlin wall tower: brick block with white trims and slits, machicolations and swallowtails, a
    smaller square tier with windows, the green tent and lookout"""
    d = d or w
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2)
    zt = Z0 + h
    duvarlar(y, k, Z0, zt, TUG)
    silme(y, k, Z0, 0.03, 0.012, BEY, 'kaide')
    silme(y, k, Z0 + h * 0.5, 0.012, 0.006, BEY, 'duz')
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        for u in (0.33, 0.67):
            yarik(y, a + Z * Z0 + nn * 0.0008, e, nn, L * u - 0.005, h * 0.66, 0.01, 0.045, 'koyu')
        # white stone frame round a blind window on the upper part
        y.pencere(a + Z * Z0 + nn * 0.0015, e, nn, L * 0.5 - 0.015, h * 0.28, 0.03, 0.05, 'koyu')
    konsol_halka(y, k, zt - 0.035, 0.035, 0.016, TUG, 2)
    ring = disa(k, 0.016)
    kirlangic_halka(y, ring, zt, 0.05, 0.016)
    y.yuz_yon([V(p.x, p.y, zt + 0.0005) for p in disa(ring, -0.016)], 'zemin', Z)
    w2 = w * 0.66
    k2 = dikdortgen(cx - w2 / 2, cx + w2 / 2, cy - w2 / 2, cy + w2 / 2)
    pencereli_duvar(y, k2, zt, tier_h, [1, 1, 1, 1], renk=(TUG, 'tugla_koyu', BEY, 'koyu'), v0=0.025, en=0.45, ust=0.02, derin=0.014,
                    sivri=0.0, cerceve=(0.005, BEY), k_say=6)
    silme(y, k2, zt + tier_h - 0.014, 0.014, 0.01, BEY, 'kaba')
    for p in k2:   # white pinnacles on the tier's corners
        y.prizma((p.x, p.y), 0.009, zt + tier_h, zt + tier_h + 0.02, BEY, n=6)
        y.koni((p.x, p.y), 0.009, zt + tier_h + 0.02, 0.035, YES, n=6)
    t = tent(y, (cx, cy), (w2 / 2 + 0.012) * math.sqrt(2), zt + tier_h, tent_h, n=4, kat=math.pi / 4)
    if not gozcu:   # (a small tower: only the gilded vane on its tent)
        y.prizma((cx, cy), 0.003, t - 0.005, t + 0.05, 'altin', n=5)
        kure(y, (cx, cy, t + 0.01), 0.007, 'altin', n=6, kat=3)
        levha(y, [V(cx + 0.003, cy, t + 0.026), V(cx + 0.028, cy, t + 0.028), V(cx + 0.028, cy, t + 0.042), V(cx + 0.003, cy, t + 0.044)], 'altin', -Y)
        return t + 0.05
    return nobet(y, (cx, cy), 0.02, t - tent_h * 0.14, 0.045, 0.05)


# ---------------------------------------------------------------- the walls
y.bolum('Kızıl tuğla surlar')
sur(y, DUV, Z0, WH, kalinlik=WT, key=TUG, kapali=True, mazgal_h=0.0, parapet_h=0.012, ust_key='zemin')
silme(y, DUV, Z0, 0.03, 0.012, BEY, 'kaide')
silme(y, DUV, Z0 + WH - 0.03, 0.01, 0.006, BEY, 'duz')
# the towers along the wall: (point, kind, size); the wall's merlons stop short of them
KULE = {'A': (A, 'y', 0.13), 'B': (B, 'y', 0.13), 'C': (C, 'k', 0.17), 'D': (D, 'y', 0.12), 'E': (E, 'k', 0.17)}
ARA = [(V(-0.45, -0.66), 0.14), (V(0.25, -0.66), 0.25), (V(-1.02, 0.18), 0.15), (V(0.66, 0.65), 0.14), (V(-0.35, 1.0), 0.14)]
for i in range(5):
    a, b = DUV[i], DUV[(i + 1) % 5]
    e = (b - a).normalized()
    L = (b - a).length
    kesik = [(0.0, KULE['ABCDE'[i]][2] * 0.9), (L - KULE['ABCDE'[(i + 1) % 5]][2] * 0.9, L)]
    for p, w in ARA:
        u = (p - a).dot(e)
        if -1e-6 < u < L and (p - a - e * u).length < 1e-3:
            kesik.append((u - w / 2 - 0.01, u + w / 2 + 0.01))
    kesik.sort()
    u = 0.0
    for k0, k1 in kesik:
        if k0 > u + 0.05:
            kirlangic(y, a + e * u, a + e * k0, Z0 + WH + 0.012, 0.055, WT * 0.34, TUG, yarik_key=None)
        u = max(u, k1)
    # loopholes along the outer face
    nn = V(e.y, -e.x)
    for k in range(int(L / 0.16)):
        uu = (k + 0.5) * L / int(L / 0.16)
        if any(k0 - 0.02 < uu < k1 + 0.02 for k0, k1 in kesik): continue
        yarik(y, a + Z * Z0 + nn * 0.0008, e, nn, uu - 0.005, WH * 0.45, 0.01, 0.04, 'koyu')

y.bolum('Köşe ve duvar kuleleri')
for ad, (p, tip, s) in KULE.items():
    if tip == 'y': kule_yuv(y, (p.x, p.y), s, WH + 0.12, 0.13, 0.32)
    else: kule_kare_k(y, p.x, p.y, s, WH + 0.1, 0.11, 0.28)
for p, w in ARA[:1] + ARA[2:]:
    kule_kare_k(y, p.x, p.y, w, WH + 0.06, 0.09, 0.24, gozcu=False)

# ---------------------------------------------------------------- Spasskaya tower
y.bolum('Spasskaya Kulesi')
SX, SY = 0.25, -0.69
SW = 0.25
k1 = dikdortgen(SX - SW / 2, SX + SW / 2, SY - SW / 2, SY + SW / 2)
Z1 = Z0 + 0.44
# the gate front with its arch and the gilded gates, side and back walls
kapi(y, k1[0], k1[1], Z0, 0.5, 0.26, (TUG, 'tugla_koyu', BEY, 'ahsap'), derin=0.03, cerceve=(0.012, [BEY]))
duz_duvar(y, k1[0], k1[1], Z0 + 0.26, Z1, TUG)
for i in (1, 2, 3):
    duz_duvar(y, k1[i], k1[(i + 1) % 4], Z0, Z1, TUG)
silme(y, k1, Z0, 0.035, 0.014, BEY, 'kaide')
for zz in (Z0 + 0.29, Z1 - 0.02):
    silme(y, k1, zz, 0.014, 0.008, BEY, 'kaba')
for i in range(4):
    a, b = k1[i], k1[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for u in (0.3, 0.7):
        y.pencere(a + Z * Z0 + nn * 0.0015, e, nn, SW * u - 0.012, 0.31, 0.024, 0.05, 'koyu')
# gilded icon over the gate (the Saviour icon) in a white frame
y.oculus(V(SX, SY - SW / 2, Z0 + 0.3), X, -Y, 0.022, 'altin', BEY, f=0.007, k=12)
# white corner pinnacles and a balustrade on the first tier
for p in k1:
    y.prizma((p.x, p.y), 0.016, Z1, Z1 + 0.06, BEY, n=8)
    y.koni((p.x, p.y), 0.016, Z1 + 0.06, 0.07, YES, n=8)
    kure(y, (p.x, p.y, Z1 + 0.135), 0.008, 'altin', n=8, kat=4)
kirlangic_halka(y, disa(k1, 0.0), Z1, 0.04, 0.014, BEY)
# second tier: the clock
SW2 = 0.18
k2 = dikdortgen(SX - SW2 / 2, SX + SW2 / 2, SY - SW2 / 2, SY + SW2 / 2)
Z2 = Z1 + 0.2
y.yuz_yon([V(p.x, p.y, Z1 + 0.0005) for p in disa(k1, -0.014)], 'zemin', Z)
duvarlar(y, k2, Z1, Z2, TUG)
silme(y, k2, Z2 - 0.016, 0.016, 0.012, BEY, 'kaba')
for i in range(4):
    a, b = k2[i], k2[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    o = (a + b) / 2 + Z * (Z1 + 0.1)
    # a white square frame, the dark blue dial with gilded rim, numerals and hands
    kutu3(y, o + nn * 0.003, e, nn, Z, 0.15, 0.006, 0.15, BEY, ('+x', '-x', '+y', '+z', '-z'))
    y.oculus(o + nn * 0.006, e, nn, 0.058, 'kobalt', 'altin', f=0.008, k=24)
    for h in range(0, 12, 3):
        t = TAU * h / 12
        kutu3(y, o + nn * 0.0115 + e * (0.048 * math.cos(t)) + Z * (0.048 * math.sin(t)), e, nn, Z, 0.006, 0.002, 0.006, 'altin')
    cubuk(y, o + nn * 0.012, o + nn * 0.012 + Z * 0.04, 0.005, 'altin', 0.002)
    cubuk(y, o + nn * 0.013, o + nn * 0.013 + e * 0.03 - Z * 0.012, 0.005, 'altin', 0.002)
for p in k2:
    y.prizma((p.x, p.y), 0.012, Z2, Z2 + 0.05, BEY, n=8)
    y.koni((p.x, p.y), 0.012, Z2 + 0.05, 0.06, YES, n=8)
    kure(y, (p.x, p.y, Z2 + 0.115), 0.006, 'altin', n=8, kat=4)
# third tier: an octagonal belfry, open arches
y.yuz_yon([V(p.x, p.y, Z2 + 0.0005) for p in k2], 'zemin', Z)
R3 = 0.072
k3 = cokgen((SX, SY), R3, 8, math.pi / 8)
Z3 = Z2 + 0.15
pencereli_duvar(y, k3, Z2, Z3 - Z2, [1] * 8, renk=(TUG, 'tugla_koyu', BEY, 'koyu'), v0=0.02, en=0.55, ust=0.02, derin=0.016, sivri=0.0,
                cerceve=(0.006, BEY), k_say=8)
silme(y, k3, Z2, 0.014, 0.008, BEY, 'kaide')
silme(y, k3, Z3 - 0.014, 0.014, 0.012, BEY, 'kaba')
# tent with dormers (slukhi) and the pommel
ZT = tent(y, (SX, SY), R3 + 0.012, Z3, 0.36)
for i in range(4):
    a = TAU * i / 4 - math.pi / 2
    nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
    with parca(y, (SX + nn.x * 0.06, SY + nn.y * 0.06, Z3 + 0.06), a + math.pi / 2):
        kutu3(y, V(0, -0.008, 0.02), X, Y, Z, 0.03, 0.03, 0.04, BEY, ('+x', '-x', '-y', '+z'))
        y.pencere(V(0, -0.0235, 0), X, -Y, -0.006, 0.006, 0.012, 0.022, 'koyu')
        y.koni((0, -0.008), 0.02, 0.04, 0.03, YES, n=4)
y.prizma((SX, SY), 0.005, ZT - 0.02, ZT + 0.035, 'altin', n=6)
kure(y, (SX, SY, ZT + 0.03), 0.016, 'altin', n=12, kat=6)


def kartal(y, cx, cy, z, s=1.0, key='altin'):
    """the double-headed eagle facing -y: body, spread wings (sheets edged), two necks and crowned heads, a tail"""
    with parca(y, (cx, cy, z), 0.0, s):
        kure(y, (0, 0, 0.03), 0.017, key, n=10, kat=5)
        donel(y, (0, 0), [(0.0, -0.01), (0.012, 0.0), (0.016, 0.02), (0.0, 0.03)], key, n=8)
        for sx in (-1, 1):
            pts = [V(sx * 0.012, 0.0, 0.025), V(sx * 0.05, 0.0, 0.05), V(sx * 0.07, 0.0, 0.07), V(sx * 0.066, 0.0, 0.04),
                   V(sx * 0.055, 0.0, 0.03), V(sx * 0.045, 0.0, 0.012), V(sx * 0.02, 0.0, 0.01)]
            for i in range(1, len(pts) - 1):
                levha(y, [pts[0], pts[i], pts[i + 1]], key, -Y, kil=0.004)
            boru(y, [V(sx * 0.006, 0, 0.04), V(sx * 0.016, 0, 0.058), V(sx * 0.02, 0, 0.068)], 0.0045, key, n=6)
            kure(y, (sx * 0.024, -0.002, 0.072), 0.007, key, n=8, kat=4)
            boru(y, [V(sx * 0.028, -0.002, 0.072), V(sx * 0.036, -0.002, 0.069)], 0.0025, key, n=4, r_son=0.001)
            kure(y, (sx * 0.022, -0.002, 0.082), 0.005, key, n=6, kat=3)
        kure(y, (0, 0, 0.09), 0.008, key, n=8, kat=4)
        y.koni((0, 0), 0.006, 0.096, 0.016, key, n=6)
        donel(y, (0, 0.002), [(0.0, -0.025), (0.014, -0.022), (0.006, 0.0), (0.0, 0.0)], key, n=6)


kartal(y, SX, SY, ZT + 0.04, 1.25)
# the wall walk ending at the tower: a white plaque band either side
for sx in (-1, 1):
    kutu_merkez(y, (SX + sx * (SW / 2 + 0.012), SY + 0.03), 0.024, 0.07, WH + 0.06, TUG, z0=Z0)

# ---------------------------------------------------------------- Dormition cathedral
y.bolum('Uspenski Katedrali')
UC = V(-0.4, 0.05)
UXB = [UC.x + q for q in (-0.27, -0.135, 0.0, 0.135, 0.27)]
UYB = [UC.y + q for q in (-0.2, -0.067, 0.067, 0.2)]
UZ = Z0 + 0.36


def pen_u(ad, i, ua, ub):
    um, w = (ua + ub) / 2, ub - ua
    kor = [(um - w * 0.25 + w * 0.25 * k, 0.0, w * 0.15, 0.05, 'siva') for k in range(3)]   # the blind arcade belt
    pen_ = [(um, 0.0, 0.026, 0.085)]
    if ad in ('arka', 'sag'):   # (the far sides: the windows only)
        return [(0.23, 0.33, pen_)]
    bands = [(0.15, 0.205, kor), (0.23, 0.33, pen_)]
    if ad == 'on' and i == 1:   # the gilded south portal
        bands.append((0.0, 0.13, [(um, 0.0, 0.075, 0.115, 'altin', (0.01, ['altin', BEY]))]))
    elif ad in ('on', 'sol', 'sag'):
        bands.append((0.04, 0.12, [(um, 0.0, 0.026, 0.07)]))
    return bands


H_u = zakomara_govde(y, UXB, UYB, Z0, UZ, 'siva', 'kursun', pencere=pen_u, pen_key=BEY, m=6)
silme(y, dikdortgen(UXB[0], UXB[-1], UYB[0], UYB[-1]), UZ - 0.008, 0.008, 0.005, BEY, 'duz')
y.bolum('Uspenski apsisleri')
# apses on the east (+x) side
for yy, r in ((UC.y - 0.1, 0.06), (UC.y, 0.07), (UC.y + 0.1, 0.06)):
    apsis(y, (UXB[-1], yy), r, Z0, 0.26, 0.0, 'siva', 'kursun', n=6, pen_key=BEY)
y.bolum('Uspenski kubbeleri')
# five gilded helmet domes clustered to the east
UK = [(UC.x + 0.05, UC.y, 0.085, 0.2, 0.1)] + [(UC.x + 0.05 + sx * 0.135, UC.y + sy * 0.1, 0.06, 0.16, 0.075) for sx in (-1, 1) for sy in (-1, 1)]
for cx, cy, r, hd, dh in UK:
    kubbe_kule(y, (cx, cy), r, UZ + 0.06, hd, 'shlem', 'altin', 'siva', n=12, pencere=6 if r > 0.07 else 4, dome_h=dh, hac_h=0.08, kornis_key=BEY)

# ---------------------------------------------------------------- Archangel cathedral
y.bolum('Başmelek Katedrali')
AC_ = V(0.5, 0.1)
AXB = [AC_.x + q for q in (-0.17, -0.06, 0.06, 0.17)]
AYB = [AC_.y + q for q in (-0.15, -0.05, 0.05, 0.15)]
AZ = Z0 + 0.3


def pen_a(ad, i, ua, ub):
    um = (ua + ub) / 2
    if ad in ('arka', 'sag'):
        return [(0.16, 0.25, [(um, 0.0, 0.024, 0.07)])]
    return [(0.04, 0.12, [(um, 0.0, 0.026, 0.07)]), (0.16, 0.25, [(um, 0.0, 0.024, 0.07)])]


zakomara_govde(y, AXB, AYB, Z0, AZ, 'siva_krem', 'kursun', pencere=pen_a, pen_key=BEY, m=6)
silme(y, dikdortgen(AXB[0], AXB[-1], AYB[0], AYB[-1]), Z0 + 0.15, 0.012, 0.008, BEY, 'kaba')
# scallop shells in the gables of the two seen fronts (the Venetian touch of its builder)
for side, bol, sabit, nn, ex in (('on', AXB, AYB[0], -Y, X), ('sol', AYB, AXB[0], -X, -Y)):
    for i in range(3):
        um, R = (bol[i] + bol[i + 1]) / 2, (bol[i + 1] - bol[i]) / 2 - 0.012
        o = (V(um, sabit) if side == 'on' else V(sabit, um)) + Z * AZ
        for k in range(7):
            t0, t1 = math.pi * k / 7, math.pi * (k + 1) / 7
            tm = (t0 + t1) / 2
            p0 = o + ex * (R * 0.25 * math.cos(tm)) + Z * (R * 0.25 * math.sin(tm))
            pa = o + ex * (R * math.cos(t0 + 0.04)) + Z * (R * math.sin(t0 + 0.04))
            pb = o + ex * (R * math.cos(t1 - 0.04)) + Z * (R * math.sin(t1 - 0.04))
            y.yuz_yon([p0 + nn * 0.003, pa + nn * 0.003, pb + nn * 0.003], BEY, nn)
            y.yuz_yon([pa + nn * 0.003, pb + nn * 0.003, pb, pa], BEY, (pa + pb) / 2 - o)
for cx, cy, r, key in ((AC_.x, AC_.y, 0.065, 'altin'), (AC_.x - 0.09, AC_.y - 0.08, 0.045, 'kursun'), (AC_.x + 0.09, AC_.y - 0.08, 0.045, 'kursun'),
                       (AC_.x - 0.09, AC_.y + 0.08, 0.045, 'kursun'), (AC_.x + 0.09, AC_.y + 0.08, 0.045, 'kursun')):
    kubbe_kule(y, (cx, cy), r, AZ + 0.05, 0.14 if r > 0.05 else 0.11, 'shlem', key, 'siva_krem', n=12 if r > 0.05 else 8, pencere=6 if r > 0.05 else 4, dome_h=r * 1.1,
               hac_h=0.07, kornis_key=BEY)

# ---------------------------------------------------------------- Ivan the Great
y.bolum('Büyük İvan Çan Kulesi')
IC = V(0.08, 0.48)
z = Z0
tiers = [(0.115, 0.36, 1), (0.096, 0.3, 1), (0.08, 0.24, 1)]
for k, (r, h, _) in enumerate(tiers):
    ring = cokgen(IC, r, 8, math.pi / 8)
    if k == 0:
        duvarlar(y, ring, z, z + h, 'siva')
        for i in range(8):
            a, b = ring[i], ring[(i + 1) % 8]
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            y.pencere(a + Z * z + nn * 0.0015, e, nn, (b - a).length / 2 - 0.012, h * 0.5, 0.024, 0.06, 'koyu')
        silme(y, ring, z, 0.03, 0.012, 'siva', 'kaide')
    else:
        pencereli_duvar(y, ring, z, h, [1] * 8, renk=('siva', 'siva', BEY, 'koyu'), v0=h * 0.12, en=0.6, ust=0.02, derin=0.02, sivri=0.0,
                        cerceve=(0.006, BEY), k_say=6)
        # bells in the open arches (seen through)
        for i in (range(0, 8, 2) if k == 1 else ()):
            a = TAU * (i + 0.5) / 8
            p = V(IC.x + r * 0.8 * math.cos(a), IC.y + r * 0.8 * math.sin(a))
            zb = z + h * 0.62
            donel(y, (p.x, p.y), [(0.0, zb - 0.05), (0.02, zb - 0.05), (0.017, zb - 0.04), (0.011, zb - 0.02), (0.005, zb), (0.0, zb)], 'bronz', n=10)
    # a gallery cornice with a white balustrade
    silme(y, ring, z + h - 0.018, 0.018, 0.016, BEY, 'kaba')
    rr = cokgen(IC, r + 0.012, 8, math.pi / 8)
    y.yuz_yon([V(p.x, p.y, z + h) for p in rr], 'zemin', Z)
    for i in range(8):
        for t in (0.33, 0.67):
            p = rr[i].lerp(rr[(i + 1) % 8], t)
            y.prizma((p.x, p.y), 0.003, z + h, z + h + 0.022, BEY, n=4, ust=False)
    silme(y, rr, z + h + 0.022, 0.005, 0.003, BEY, 'duz')
    z += h
# the drum with a ring of kokoshnik gables, the gilded dome, the cross
zd = z
y.prizma(IC, 0.066, zd, zd + 0.05, 'siva', n=16, ust=False)
for i in range(8):
    a = TAU * i / 8
    nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
    o = V(IC.x, IC.y) + nn * 0.07
    pts = [o - e * 0.026 + Z * (zd + 0.03)] + [o + e * (0.026 * math.cos(math.pi - math.pi * t / 8)) + Z * (zd + 0.03 + 0.03 * math.sin(math.pi * t / 8) + 0.012 * (1 - abs(t - 4) / 4) ** 3) for t in range(1, 8)] + [o + e * 0.026 + Z * (zd + 0.03)]
    for t in range(len(pts) - 1):
        y.yuz_yon([pts[t], pts[t + 1], pts[t + 1] - nn * 0.012, pts[t] - nn * 0.012], 'altin', Z + nn * 0.5)
    y.yuz_yon([o - e * 0.026 + Z * zd] + pts + [o + e * 0.026 + Z * zd], 'siva', nn)
zt = baraban(y, IC, 0.06, zd + 0.05, 0.13, 'siva', n=12, pencere=6, kornis_key=BEY)
zt = boyun(y, IC, 0.05, zt, 0.012, 'altin', n=24)
zt = kubbe(y, IC, 0.072, zt - 0.002, 'shlem', 0.1, 'altin', n=24)
IVAN_TEPE = ortodoks_hac(y, IC.x, IC.y, zt - 0.004, 0.11, 'altin')
# the Dormition belfry attached to its north (lower, with a small gilded dome)
BL = V(IC.x - 0.2, IC.y + 0.0)
kk = dikdortgen(BL.x - 0.1, BL.x + 0.1, BL.y - 0.08, BL.y + 0.08)
pencereli_duvar(y, kk, Z0, 0.3, [2, 1, 2, 1], renk=('siva', 'siva', BEY, 'koyu'), v0=0.15, en=0.5, ust=0.03, derin=0.02, sivri=0.0,
                cerceve=(0.006, BEY), k_say=8)
silme(y, kk, Z0, 0.03, 0.012, 'siva', 'kaide')
silme(y, kk, Z0 + 0.12, 0.012, 0.008, BEY, 'kaba')
silme(y, kk, Z0 + 0.3 - 0.015, 0.015, 0.012, BEY, 'kaba')
cati_kirma(y, BL.x - 0.1, BL.x + 0.1, BL.y - 0.08, BL.y + 0.08, Z0 + 0.3, 0.05, 0.02, 'kursun', ns=6, nr=4)
kubbe_kule(y, (BL.x, BL.y), 0.045, Z0 + 0.32, 0.1, 'sogan', 'altin', 'siva', n=10, pencere=5, dome_h=0.075, hac_h=0.07, kornis_key=BEY)

# ---------------------------------------------------------------- Palace of Facets
y.bolum('Granovitaya Palata')
PC = V(-0.55, 0.58)
PW_, PD_, PH_ = 0.3, 0.26, 0.26
px0, px1, py0, py1 = PC.x - PW_ / 2, PC.x + PW_ / 2, PC.y - PD_ / 2, PC.y + PD_ / 2


def elmas_cephe(y, a, b, z0, z1, nu, nv, pencereler=(), key='kirec', cikinti=0.012):
    """a wall a->b faced with diamond-point (faceted) stones: a grid of low pyramids; pencereler: (i, j) cells holding
    a framed window instead"""
    a, b = V(a.x, a.y), V(b.x, b.y)
    e = (b - a); L = e.length; e = e / L; nn = V(e.y, -e.x)
    du, dv = L / nu, (z1 - z0) / nv
    for i in range(nu):
        for j in range(nv):
            p = a + e * (i * du) + Z * (z0 + j * dv)
            if (i, j) in pencereler:
                dikdortgen_acik(y, p, p + e * du, z0 + j * dv, dv, 0.18, 0.82, dv * 0.12, dv * 0.85, (key, BEY, BEY, 'koyu'), derin=0.012,
                                cerceve=(0.006, 'altin'))
                continue
            q = [p, p + e * du, p + e * du + Z * dv, p + Z * dv]
            tepe = p + e * (du / 2) + Z * (dv / 2) + nn * cikinti
            for k in range(4):
                y.yuz_yon([q[k], q[(k + 1) % 4], tepe], key, nn + ((q[k] + q[(k + 1) % 4]) / 2 - tepe).normalized() * 0.3)


kp = dikdortgen(px0, px1, py0, py1)
zb = Z0 + 0.08
duvarlar(y, kp, Z0, zb, 'kirec')
for i, (nu, win) in enumerate(((8, {(1, 2), (2, 2), (5, 2), (6, 2), (1, 0), (2, 0), (5, 0), (6, 0)}), (7, {(1, 2), (2, 2), (4, 2), (5, 2)}),
                               (8, set()), (7, {(1, 2), (2, 2), (4, 2), (5, 2), (1, 0), (2, 0), (4, 0), (5, 0)}))):
    a, b = kp[i], kp[(i + 1) % 4]
    if i == 2:
        duz_duvar(y, a, b, zb, Z0 + PH_, 'kirec'); continue
    elmas_cephe(y, a, b, zb, Z0 + PH_, nu, 4, win)
silme(y, kp, zb - 0.01, 0.012, 0.008, BEY, 'kaba')
silme(y, kp, Z0 + PH_ - 0.014, 0.014, 0.014, BEY, 'tac')
cati_kirma(y, px0, px1, py0, py1, Z0 + PH_, 0.14, 0.03, 'kursun', ns=8, nr=6)
# the Red Porch stair up to its door on the front
merdiven(y, (PC.x + 0.06, py0 - 0.14), math.pi / 2, 0.07, Z0, zb + 0.06, n=7, key=BEY, yanlik='altin')

# ---------------------------------------------------------------- Red Square: Lobnoye Mesto, people, banners
y.bolum('Lobnoye Mesto ve meydan')
LC = V(-0.45, -0.94)
ring = cokgen(LC, 0.1, 20)
duvarlar(y, ring, Z0, Z0 + 0.05, 'kirec')
silme(y, ring, Z0, 0.016, 0.008, 'kirec', 'kaide')
y.yuz_yon([V(p.x, p.y, Z0 + 0.05) for p in ring], 'zemin', Z)
for i in range(20):
    if i in (4, 5) or i % 2: continue
    p = ring[i].lerp(ring[(i + 1) % 20], 0.5)
    y.prizma((p.x, p.y), 0.004, Z0 + 0.05, Z0 + 0.08, 'kirec', n=4, ust=False)
silme(y, ring, Z0 + 0.08, 0.008, 0.004, 'kirec', 'duz')
merdiven(y, (LC.x + 0.0, LC.y - 0.16), math.pi / 2, 0.05, Z0, Z0 + 0.05, n=4, key='kirec')
for i, (x, yy, k) in enumerate(((-0.2, -0.9, 'boya_kirmizi'), (-0.15, -0.95, 'koyu'), (0.0, -0.82, 'kirmizi'), (0.4, -0.86, 'ahsap'),
                                (-0.7, -0.82, 'boya_sari'))):
    insan(y, x, yy, Z0, k, s=1.6, aci=math.pi / 2 + i)
# market stalls along the far side of the square
for k in range(4):
    x = 0.55 + k * 0.15
    kutu_merkez(y, (x, -1.06), 0.11, 0.06, 0.04, 'ahsap', z0=Z0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            y.prizma((x + sx * 0.05, -1.06 + sy * 0.028), 0.003, Z0, Z0 + 0.09, 'ahsap_koyu', n=4, ust=False)
    cati_besik(y, x - 0.055, x + 0.055, -1.095, -1.025, Z0 + 0.09, 0.03, 0.012, 'kumas' if k % 2 else 'boya_kirmizi', 'ahsap_koyu',
               kalinlik=0.005, ucluk_key='ahsap_dikey', uc_sacak=0.008, nr=2, ns=3)
    for j in range(3):
        kutu_merkez(y, (x - 0.032 + j * 0.032, -1.06), 0.026, 0.04, 0.012, ('turuncu', 'boya_kirmizi', 'boya_sari')[(j + k) % 3], z0=Z0 + 0.04)
sancak(y, SX - 0.18, SY - 0.2, Z0, boy=0.42, en=0.12, yuk=0.08, aci=-math.pi / 2 - 0.4, direk_key='ahsap_koyu', kuyruk=True)
sancak(y, SX + 0.18, SY - 0.2, Z0, boy=0.42, en=0.12, yuk=0.08, aci=-math.pi / 2 + 0.4, direk_key='ahsap_koyu', kuyruk=True)

y.bolum('Ağaçlar')
for i, (x, yy, b) in enumerate(((0.78, 0.52, 0.26), (-0.85, -0.3, 0.26), (0.2, 0.82, 0.24), (-0.15, 0.85, 0.26))):
    kayin(y, x, yy, Z0, b, tohum=i)

calistir(y, 'lm_kremlin')
