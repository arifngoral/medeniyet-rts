# Rumeli Hisarı (lm_rumelihisari): the fortress on a terraced slope rising from the Bosphorus shore (front, -y) to the
# hill: three great towers with storeys of small arched windows, corbelled merloned crowns and conical lead roofs on
# posts (Saruca Paşa round, by the shore; Halil Paşa twelve-sided, on the shore; Zağanos Paşa round, on the hilltop),
# merloned curtain walls stepping up the slope with small towers, a low sea wall with a gate, and the little mosque
# with its minaret in the terraced inner court.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

TAS, TAS2 = 'tas', 'tas_koyu'
XA, XB = -1.15, 1.15
# terraces (y from, y to, ground z)
TER = [(-1.0, -0.42, 0.05), (-0.42, 0.02, 0.14), (0.02, 0.44, 0.25), (0.44, 0.95, 0.36)]


def g(yy):
    for a, b, z in TER:
        if yy < b: return z
    return TER[-1][2]


# ---------------- ground ----------------
y.bolum('Yamaç: basamaklı setler')
for k, (a, b, z) in enumerate(TER):
    if k == 0:
        duz_duvar(y, V(XA, a), V(XB, a), 0, z, 'tas_koyu')
        y.yuz_yon([V(XA, a, z), V(XB, a, z), V(XB, -0.84, z), V(XA, -0.84, z)], 'zemin', Z)     # the quay
        y.yuz_yon([V(XA, -0.84, z), V(XB, -0.84, z), V(XB, b, z), V(XA, b, z)], 'cimen', Z)
    else:
        z_on = TER[k - 1][2]
        duz_duvar(y, V(XA, a), V(XB, a), z_on, z, TAS)                       # retaining wall (riser)
        silme(y, [V(XA, a), V(XB, a)], z - 0.008, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
        y.yuz_yon([V(XA, a, z), V(XB, a, z), V(XB, b, z), V(XA, b, z)], 'cimen', Z)
    duz_duvar(y, V(XB, a), V(XB, b), 0, z, 'toprak')
    duz_duvar(y, V(XA, b), V(XA, a), 0, z, 'toprak')
duz_duvar(y, V(XB, TER[-1][1]), V(XA, TER[-1][1]), 0, TER[-1][2], 'toprak')


# ---------------- great towers ----------------
def duvar_dilim(p, q, za, zb, key=None, n=4):
    """a plain wall cut in n bands (more corners: the baked shadow of a string course stays near it)"""
    for k in range(n):
        duz_duvar(y, p, q, za + (zb - za) * k / n, za + (zb - za) * (k + 1) / n, key or TAS)


def buyuk_kule(c, r, n, z0, H, kat=3, kapi_aci=None, tohum=0):
    """a great tower: a battered stone foot, kat storeys of flat facets with small arched windows here and there,
    string courses, a corbelled crown with merlons, posts on the wall walk carrying a conical lead roof"""
    cx, cy = c
    ring = cokgen(c, r, n, math.pi / n)
    donel(y, c, [(r * 1.1, z0 - 0.06), (r * 1.1, z0 + 0.015), (r * 1.005, z0 + 0.07)], TAS2, n=n, kat=math.pi / n)
    z1 = z0 + 0.06
    zt = z0 + H
    hs = (zt - z1) / kat
    for s in range(kat):
        za = z1 + hs * s
        for i in range(n):
            p, q = ring[i], ring[(i + 1) % n]
            mid = (p + q) / 2
            ang = math.atan2(mid.y - cy, mid.x - cx)
            if s == 0 and kapi_aci is not None and abs((ang - kapi_aci + math.pi) % TAU - math.pi) < math.pi / n:
                kapi(y, p, q, za, 0.62, hs * 0.72, (TAS, 'tas_koyu', 'tas_acik', 'ahsap'), sivri=0.0, derin=0.025, cerceve=(0.006, 'tas_acik'))
                duvar_dilim(p, q, za + hs * 0.72, za + hs, n=2)
            elif s > 0 and (i * 7 + s * 3 + tohum) % (4 if s < kat - 1 else 2) == 0:
                # (the window bay kept clear of the string courses, so their baked shadow does not darken it)
                duvar_dilim(p, q, za, za + hs * 0.25, n=1)
                y.kemerli(p, q, za + hs * 0.25, hs * 0.55, (TAS, 'tas_koyu', 'tas_acik', 'koyu'), v0=hs * 0.08, en=0.32, ust=hs * 0.05,
                          derin=0.02, k_say=6, sivri=0.0, cerceve=(0.005, 'tas_acik'))
                duvar_dilim(p, q, za + hs * 0.8, za + hs, n=1)
            elif s == 0 and i % 4 == 1:
                duvar_dilim(p, q, za, za + hs)
                e = (q - p).normalized(); nn = V(e.y, -e.x)
                yarik(y, p + nn * 0.001, e, nn, (q - p).length / 2 - 0.004, za + hs * 0.4, 0.008, hs * 0.3, 'koyu')
            else:
                duvar_dilim(p, q, za, za + hs)
        if s > 0:
            silme(y, ring, za - 0.004, 0.008, 0.007, 'tas_acik', 'duz')
    if False:
        # quoins on the edges of a polygonal tower (alternating long and short stones)
        for i, p in enumerate(ring):
            d = V(p.x - cx, p.y - cy).normalized()
            k = 0
            zz = z1 + 0.004
            while zz < zt - 0.06:
                s = 0.021 if k % 2 == 0 else 0.013
                kutu_merkez(y, (p.x, p.y), s, s, 0.024, 'tas_acik', z0=zz,
                            aci=math.atan2(d.y, d.x) + math.pi / 4, yuzler='onarkasagsolust')
                zz += 0.034; k += 1
    # crown
    konsol_halka(y, ring, zt - 0.045, 0.045, 0.022, TAS, 3)
    r2 = disa(ring, 0.022)
    parapet(y, r2, zt, 0.016, 0.038, 0.022, TAS, ust_key='tas_acik')
    y.yuz_yon([V(p.x, p.y, zt + 0.0005) for p in disa(r2, -0.022)], 'zemin', Z)
    # roof on posts
    zr = zt + 0.016 + 0.038 + 0.03
    for k in range(8):
        a = TAU * (k + 0.5) / 8
        y.prizma((cx + r * 0.88 * math.cos(a), cy + r * 0.88 * math.sin(a)), 0.006, zt, zr, 'ahsap_koyu', n=5, ust=False)
    y.prizma(c, r * 0.8, zt, zr, 'ahsap', n=n, ust=False, kat=math.pi / n)        # the inner (timber) drum
    hh = r * 1.55
    re = r + 0.05
    donel(y, c, [(re, zr), (re * 0.72, zr + hh * 0.3), (re * 0.38, zr + hh * 0.66), (0.0, zr + hh)], 'kursun', n=max(n, 16) if n > 12 else n,
          kat=math.pi / n, dilim=['kursun', 'kursun2'])
    y.yuz_yon([V(p.x, p.y, zr) for p in cokgen(c, re, max(n, 16) if n > 12 else n, math.pi / n)], 'ahsap_koyu', -Z)
    tip = zr + hh
    kure(y, (cx, cy, tip + 0.012), 0.012, 'altin', n=8, kat=4)
    y.prizma(c, 0.004, tip - 0.01, tip + 0.05, 'altin', n=5)
    return tip + 0.05


y.bolum('Saruca Paşa Kulesi (yuvarlak)')
SAR = (0.7, -0.55)
tip_s = buyuk_kule(SAR, 0.25, 24, g(-0.55), 0.74, kat=4, kapi_aci=math.pi * 0.75, tohum=1)
y.bolum('Halil Paşa Kulesi (on iki köşeli)')
HAL = (-0.3, -0.6)
buyuk_kule(HAL, 0.22, 12, g(-0.6), 0.6, kat=3, kapi_aci=math.pi / 2, tohum=2)
y.bolum('Zağanos Paşa Kulesi (yuvarlak, tepede)')
ZAG = (-0.68, 0.6)
buyuk_kule(ZAG, 0.24, 24, g(0.6), 0.56, kat=3, kapi_aci=-math.pi * 0.25, tohum=3)


# ---------------- curtain walls stepping up the slope ----------------
HWALL = 0.2
KAL = 0.06


def sur_yamac(pts, adim=0.11):
    """a merloned wall along a polyline, cut into short lengths that each stand on the ground below them (the wall
    and its battlements step up the slope)"""
    for k in range(len(pts) - 1):
        p, q = V(*pts[k]), V(*pts[k + 1])
        n = max(1, int(round((q - p).length / adim)))
        for j in range(n):
            a, b = p.lerp(q, j / n), p.lerp(q, (j + 1) / n)
            z0 = min(g(a.y), g(b.y)) - 0.02
            zt = max(g(a.y), g(b.y)) + HWALL
            sur(y, [a, b], z0, zt - z0, KAL, TAS, mazgal_h=0.03, parapet_h=0.014, ust_key='zemin')


y.bolum('Surlar ve küçük kuleler')
KD = (0.95, 0.12)          # small tower, north-east
KK = (0.88, 0.72)          # small tower, north-west corner (hill)
KB = (-0.98, -0.12)        # small tower, south side
sur_yamac([HAL, SAR])
sur_yamac([SAR, KD, KK])
sur_yamac([KK, ZAG])
sur_yamac([ZAG, KB, HAL])
for c, r in ((KD, 0.075), (KK, 0.08), (KB, 0.075)):
    kule_yuvarlak(y, c, r, g(c[1]) - 0.02, HWALL + 0.17, TAS, 'konik', 'kursun', cati_h=r * 1.9, yarik_say=3, bolum=4)
# a square tower midway on the hill wall
MK = (0.1, 0.66)
kule_kare(y, MK[0], MK[1], 0.13, g(MK[1]) - 0.02, HWALL + 0.15, TAS, 'piramit', 'kursun', cati_h=0.12, yarik_say=2)

# ---------------- the sea wall and its gate ----------------
y.bolum('Deniz suru ve kapı')
ZS = TER[0][2]
SY = -0.86
deniz = [V(-0.85, SY), V(-0.07, SY)]
sur(y, deniz, ZS, 0.13, 0.05, TAS, mazgal_h=0.025, parapet_h=0.012, ust_key='zemin')
sur(y, [V(0.17, SY), V(1.02, SY)], ZS, 0.13, 0.05, TAS, mazgal_h=0.025, parapet_h=0.012, ust_key='zemin')
kale_kapisi(y, 0.05, SY + 0.03, 0.24, ZS, 0.16, derin=0.1, key=TAS, kule=None)
for x in (-0.85, 1.02):
    kule_yuvarlak(y, (x, SY + 0.02), 0.055, ZS, 0.2, TAS, 'konik', 'kursun', cati_h=0.1, yarik_say=2, bolum=3)
# the sea wall's ends meet the main walls
sur(y, [V(-0.85, SY), V(-0.85, -0.7)][::-1], ZS, 0.13, 0.04, TAS, mazgal_h=0.025, parapet_h=0.012, ust_key='zemin')
sur(y, [V(1.02, -0.7), V(1.02, SY)][::-1], ZS, 0.13, 0.04, TAS, mazgal_h=0.025, parapet_h=0.012, ust_key='zemin')

# ---------------- inner court: mosque, minaret, stairs, trees ----------------
y.bolum('İç avlu: mescit ve minare')
MX, MY = 0.2, 0.25
zm = g(MY)
mk = dikdortgen(MX - 0.13, MX + 0.13, MY - 0.09, MY + 0.09)
kutu(y, V(MX - 0.15, MY - 0.11, zm), X, 0.3, 0.22, 0.015, 'tas_koyu', 'onarkasagsolust')
pencereli_duvar(y, [V(p.x, p.y) for p in mk], zm + 0.015, 0.11, [3, 2, 3, 2], en=0.4, v0=0.025, ust=0.02, sivri=0.65, derin=0.015,
                cerceve=(0.005, 'tas_acik'))
silme(y, mk, zm + 0.115, 0.012, 0.012, 'tas_acik', 'tac')
cati_kirma(y, MX - 0.13, MX + 0.13, MY - 0.09, MY + 0.09, zm + 0.127, 0.08, 0.03, 'kiremit', 'kiremit2', alt_key='ahsap_koyu')
# a small portico before its door (front)
for k in range(4):
    sutun(y, MX - 0.09 + k * 0.06, MY - 0.135, zm + 0.015, zm + 0.1, 0.008, 'tas_acik')
cati_kirma(y, MX - 0.12, MX + 0.12, MY - 0.15, MY - 0.09, zm + 0.1, 0.035, 0.02, 'kiremit', 'kiremit2', alt_key='ahsap_koyu')
minare(y, MX + 0.17, MY + 0.05, zm, 0.42, serefe=1, kaide=0.09, r=0.022, key=TAS, govde_key='tas_acik')

y.bolum('İç avlu: merdivenler ve ağaçlar')
merdiven(y, (-0.25, 0.02 - 0.12), math.pi / 2, 0.1, g(-0.1), g(0.1), n=5, d=0.024, key='tas', yanlik='tas_acik')
merdiven(y, (0.55, 0.44 - 0.12), math.pi / 2, 0.1, g(0.3), g(0.5), n=5, d=0.024, key='tas', yanlik='tas_acik')
merdiven(y, (0.05, -0.42 - 0.12), math.pi / 2, 0.1, g(-0.5), g(-0.3), n=5, d=0.024, key='tas', yanlik='tas_acik')
# paved paths: gate -> first stair -> second stair -> third stair
YOLLAR = [((0.0, 0.1), (-0.8, -0.54)), ((-0.3, 0.1), (-0.42, -0.31)), ((-0.3, -0.2), (-0.31, -0.1)),
          ((-0.3, 0.6), (0.02, 0.12)), ((0.5, 0.6), (0.12, 0.32)), ((0.5, 0.6), (0.44, 0.56))]
for (xa, xb), (ya, yb) in YOLLAR:
    zz = g((ya + yb) / 2) + 0.003
    y.yuz_yon([V(xa, ya, zz), V(xb, ya, zz), V(xb, yb, zz), V(xa, yb, zz)], 'zemin', Z)


def ev(cx, cy, w, d, h, aci=0.0):
    """a small house of the garrison: plastered walls, half-timbering, a door and windows, a tiled gable roof"""
    z = g(cy)
    with parca(y, (cx, cy, z), aci):
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        kutu(y, V(-w / 2 - 0.006, -d / 2 - 0.006, -0.02), X, w + 0.012, d + 0.012, 0.03, 'tas_koyu', 'onarkasagsolust')
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            L = (b - a).length
            if i == 0:
                dikdortgen_acik(y, a, b, 0.01, h - 0.01, 0.42, 0.58, 0.0, h * 0.62, ('siva_krem', 'ahsap_koyu', 'ahsap', 'ahsap'), derin=0.008)
            else:
                duz_duvar(y, a, b, 0.01, h, 'siva_krem')
            kirma_dikme(y, a, b, 0.01, h, aralik=0.05, en=0.006)
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            for u in ((0.2, 0.8) if i == 0 else (0.3, 0.7) if L > 0.12 else (0.5,)):
                y.pencere(a + e * (L * u - 0.012) + nn * 0.004, e, nn, 0, h * 0.45, 0.024, h * 0.3, 'cam', kemer=False)
        cati_besik(y, -w / 2, w / 2, -d / 2, d / 2, h, h * 0.75, 0.025, 'kiremit', 'kiremit2', ucluk_key='siva_krem', alt_key='ahsap_koyu')
        y.prizma((w * 0.25, 0.0), 0.01, h, h + h * 0.95, 'tas_koyu', n=4, kat=math.pi / 4)      # chimney


y.bolum('İç avlu: garnizon evleri')
ev(0.45, -0.24, 0.2, 0.12, 0.09)
ev(-0.42, 0.24, 0.18, 0.12, 0.085, 0.0)
ev(0.7, 0.55, 0.16, 0.1, 0.08, math.pi)
for (tx, ty, tb, tt) in ((-0.1, 0.32, 0.16, 'yaprakli'), (0.62, 0.05, 0.18, 'servi'), (0.55, -0.15, 0.15, 'servi'), (-0.6, -0.2, 0.14, 'yaprakli'),
                         (0.3, 0.6, 0.15, 'yaprakli'), (-0.2, 0.55, 0.17, 'servi')):
    agac(y, tx, ty, g(ty), boy=tb, tur=tt)
# outside: trees on the slope behind the hill wall and along the quay
for (tx, ty) in ((1.08, 0.5), (-1.05, 0.8), (1.08, -0.3)):
    agac(y, tx, ty, g(ty), boy=0.15, tur='servi')

y.bolum('Boğaz kıyısı: su, iskele, kayık, balyemez toplar')
# the Bosphorus before the quay: water, a rocky edge, a timber landing stage and a moored boat
ZW = 0.015
y.yuz_yon([V(XA, -1.2, ZW), V(XB, -1.2, ZW), V(XB, -1.0, ZW), V(XA, -1.0, ZW)], 'su', Z)
duz_duvar(y, V(XA, -1.2), V(XB, -1.2), 0, ZW, 'tas_koyu')
duz_duvar(y, V(XB, -1.2), V(XB, -1.0), 0, ZW, 'tas_koyu')
duz_duvar(y, V(XA, -1.0), V(XA, -1.2), 0, ZW, 'tas_koyu')
for k, x in enumerate((-1.08, -0.93, -0.74, -0.52, 0.42, 0.66, 0.87, 1.05)):
    kutu_merkez(y, (x, -1.02 + 0.012 * (k % 2)), 0.06 + 0.02 * (k % 3), 0.04, 0.025 + 0.01 * (k % 2), 'granit_koyu', z0=ZW - 0.01, aci=0.4 * k)
# landing stage on piles
for x in (-0.03, 0.13):
    for yy in (-1.0, -1.06, -1.12):
        y.prizma((x, yy), 0.007, 0, TER[0][2] + 0.004, 'kutuk', n=6)
kutu(y, V(-0.04, -1.13, TER[0][2] - 0.004), X, 0.18, 0.13, 0.008, 'ahsap', 'onarkasagsolust')
# a caique: a hull of two curved sides, thwarts and oars
with parca(y, (0.36, -1.1, ZW), 0.08):
    Lk, Wk, Hk = 0.2, 0.035, 0.025
    pr = lambda t, s: V(Lk / 2 * t, s * Wk * (1 - t * t) ** 0.7, 0.0)
    for s in (-1, 1):
        for i in range(10):
            t0, t1 = -1 + 2 * i / 10, -1 + 2 * (i + 1) / 10
            a0, a1 = pr(t0, s), pr(t1, s)
            b0, b1 = V(a0.x, a0.y * 0.45, -0.004), V(a1.x, a1.y * 0.45, -0.004)
            y.yuz_yon([b0, b1, a1 + Z * (Hk + 0.012 * t1 * t1), a0 + Z * (Hk + 0.012 * t0 * t0)], 'lake' if i % 5 else 'ahsap_koyu', V(0, s, 0.2))
            # (the inner side of the planking, seen from above)
            y.yuz_yon([q - V(0, s * 0.0006, 0) for q in (b0, b1, a1 + Z * (Hk + 0.012 * t1 * t1), a0 + Z * (Hk + 0.012 * t0 * t0))], 'ahsap', V(0, -s, 0.5))   # (a hair inside the outer face)
    y.yuz_yon([V(-Lk / 2 * 0.9, -Wk * 0.4, Hk * 0.4), V(Lk / 2 * 0.9, -Wk * 0.4, Hk * 0.4), V(Lk / 2 * 0.9, Wk * 0.4, Hk * 0.4), V(-Lk / 2 * 0.9, Wk * 0.4, Hk * 0.4)], 'ahsap_acik', Z)
    for xx in (-0.04, 0.0, 0.04):
        cubuk(y, V(xx, -Wk * 0.8, Hk * 0.8), V(xx, Wk * 0.8, Hk * 0.8), 0.006, 'ahsap_koyu', 0.004)
    for s in (-1, 1):
        cubuk(y, V(0.0, s * Wk * 0.7, Hk + 0.004), V(0.03, s * Wk * 2.6, 0.002), 0.004, 'ahsap', 0.003)


def balyemez(x, yy, aci, L=0.2, r=0.026):
    """a great bronze bombard on a timber bed, muzzle towards aci, with a pile of stone balls"""
    z = TER[0][2]
    with parca(y, (x, yy, z), aci):
        for s in (-1, 1):
            cubuk(y, V(-L * 0.55, s * 0.025, 0.006), V(L * 0.45, s * 0.025, 0.006), 0.012, 'ahsap_koyu', 0.012)
        for xx in (-L * 0.4, 0.0, L * 0.35):
            cubuk(y, V(xx, -0.04, 0.016), V(xx, 0.04, 0.016), 0.014, 'ahsap', 0.012)
        a, b = V(-L * 0.5, 0, 0.022 + r), V(L * 0.5, 0, 0.026 + r)
        boru(y, [a, a.lerp(b, 0.35)], r * 0.8, 'bronz', n=14)
        boru(y, [a.lerp(b, 0.35), b], r, 'bronz', n=14, r_son=r * 1.06)
        for f in (0.05, 0.33, 0.37, 0.7, 0.9):
            p = a.lerp(b, f)
            boru(y, [p, p + V(0.008, 0, 0)], (r if f > 0.34 else r * 0.8) * 1.14, 'bronz', n=14)
        y.yuz_yon([b + V(0.0011, 0, 0) + V(0, r * 0.8 * math.cos(TAU * i / 12), r * 0.8 * math.sin(TAU * i / 12)) for i in range(12)], 'koyu', X)
        for (bx, by_, bz) in ((-0.03, 0.075, 0), (0.0, 0.075, 0), (-0.015, 0.075, 0.024)):
            kure(y, (bx, by_, bz + 0.013), 0.013, 'granit', n=8, kat=4)


balyemez(-0.62, -0.92, -math.pi / 2 - 0.1)
balyemez(0.55, -0.93, -math.pi / 2 + 0.15)

y.bolum('Sancak')
sancak(y, SAR[0], SAR[1], tip_s - 0.01, boy=0.16, en=0.11, yuk=0.07, aci=0.3)

calistir(y, 'lm_rumelihisari')
