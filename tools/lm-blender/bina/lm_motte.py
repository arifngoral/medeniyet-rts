# Motte Kalesi (lm_motte): a Frankish motte-and-bailey. A steep earthen motte ringed by a water-filled ditch carries a
# palisade and a tall timber donjon with an overhanging fighting gallery and a shingled roof (the silhouette); a
# flying bridge on trestles climbs to it from the bailey. The bailey below: an oval earthen bank with a palisade and
# wall walk, a timber gatehouse with a drawbridge over the front moat, the lord's hall, a stone chapel, a stable,
# a smithy, a well, haystacks and the garrison.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ortak import *
from bina_ortak import calistir

import doku

y = Yapi()

G = 0.05                      # ground top
doku.KOSE_RENK['cimen'] = cayir_renk(G)
doku.KOSE_RENK['cimen_kuru'] = cayir_renk(G, 0.45)
ZW = 0.02                     # water
XA, XB, YA, YB = -1.2, 1.2, -1.08, 1.08
YC0, YC1 = -0.98, -0.86       # the front moat
M = V(-0.55, 0.42)            # the motte's centre
ZT = G + 0.36                 # the motte's top
# the motte's section, from the ground outside to the centre of its top
PROF = [(0.62, G), (0.56, ZW), (0.46, ZW), (0.43, G + 0.01), (0.38, G + 0.1), (0.32, G + 0.24), (0.275, ZT - 0.012), (0.245, ZT), (0.0, ZT)]
BC = V(0.45, -0.3)            # the bailey (an ellipse)
BRX, BRY = 0.6, 0.46
ZB = G + 0.04                 # the bailey bank's top


def hz(x, yy):
    """the ground height at (x, y)"""
    r = (V(x, yy) - M).length
    if r >= PROF[0][0]: return G
    for (r0, z0), (r1, z1) in zip(PROF, PROF[1:]):
        if r1 <= r <= r0:
            t = (r0 - r) / max(1e-9, r0 - r1)
            return z0 + (z1 - z0) * t
    return ZT


# ---------------------------------------------------------------- ground, moats
y.bolum('Zemin, hendekler')
zemin_blok(y, XA, XB, YA, YC0, G, yanlar='onsagsol')
y.yuz_yon([V(XA, YC0, ZW), V(XB, YC0, ZW), V(XB, YC1, ZW), V(XA, YC1, ZW)], 'su', Z)
y.yuz_yon([V(XA, YC0, 0), V(XB, YC0, 0), V(XB, YC0, G), V(XA, YC0, G)], 'toprak', Y)
y.yuz_yon([V(XA, YC1, 0), V(XB, YC1, 0), V(XB, YC1, G), V(XA, YC1, G)], 'toprak', -Y)
for x in (XA, XB):
    y.yuz_yon([V(x, YC0, 0), V(x, YC1, 0), V(x, YC1, ZW), V(x, YC0, ZW)], 'toprak', V(1 if x > 0 else -1, 0))
# the ground behind the moat with the motte's round hole: quads from the hole's rim out to the edge
RH = PROF[0][0]
x0, x1, y0, y1 = XA, XB, YC1, YB
kose_ac = [math.atan2(cy - M.y, cx - M.x) for cx, cy in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
acilar = sorted(set([TAU * i / 64 - math.pi for i in range(64)] + kose_ac))


def kenar(a):
    d = V(math.cos(a), math.sin(a))
    ts = []
    if abs(d.x) > 1e-9: ts += [(x0 - M.x) / d.x, (x1 - M.x) / d.x]
    if abs(d.y) > 1e-9: ts += [(y0 - M.y) / d.y, (y1 - M.y) / d.y]
    t = min(t for t in ts if t > 0)
    return M + d * t


def rim(a):
    """the hole's rim point at angle a, on the 64-gon the motte's rings use (no sliver between them)"""
    k = math.floor((a + math.pi) / (TAU / 64))
    a0 = -math.pi + TAU / 64 * k
    p0, p1 = M + V(math.cos(a0), math.sin(a0)) * RH, M + V(math.cos(a0 + TAU / 64), math.sin(a0 + TAU / 64)) * RH
    d = V(math.cos(a), math.sin(a))
    e = p1 - p0
    t = ((p0 - M).x * e.y - (p0 - M).y * e.x) / (d.x * e.y - d.y * e.x)
    return M + d * t


for i in range(len(acilar)):
    a, b = acilar[i], acilar[(i + 1) % len(acilar)]
    if b < a: b += TAU
    pa, pb = rim(a), rim(b)
    y.yuz_yon([pa + Z * G, kenar(a) + Z * G, kenar(b) + Z * G, pb + Z * G], 'cimen', Z)
for (a, b) in ((V(XB, y0), V(XB, y1)), (V(XB, y1), V(XA, y1)), (V(XA, y1), V(XA, y0))):
    duz_duvar(y, a, b, 0, G, 'toprak')

# ---------------------------------------------------------------- the motte
y.bolum('Motte: toprak tepe ve su dolu hendek')
anahtar = ['toprak', 'su', 'toprak', 'cimen', 'cimen', 'cimen', 'cimen', 'toprak_ot']
for k in range(len(PROF) - 1):
    donel(y, (M.x, M.y), PROF[k:k + 2], anahtar[k], n=64, kat=-math.pi)
# a few stones and tufts on the slope, reeds in the ditch
for k in range(14):
    a = TAU * k / 14 + 0.3
    r = 0.33 + 0.05 * (k % 3)
    p = M + V(math.cos(a), math.sin(a)) * r
    kutu_merkez(y, (p.x, p.y), 0.022, 0.016, 0.012, 'granit' if k % 2 else 'kaya', z0=hz(p.x, p.y) - 0.006, aci=a)
for k in range(22):
    a = TAU * k / 22 + 0.1
    r = 0.535 if k % 2 else 0.475
    p = M + V(math.cos(a), math.sin(a)) * r
    for j in range(3):
        q = p + V(math.cos(a + j * 2.1), math.sin(a + j * 2.1)) * 0.008
        cubuk(y, V(q.x, q.y, ZW - 0.002), V(q.x + 0.004 * (j - 1), q.y, ZW + 0.04 + 0.01 * j), 0.0035, 'cimen_kuru', 0.0025)

# gorse and bramble clumps on the slope, sheep grazing it (kept clear of the bridge)
DK = math.atan2(-0.617, 0.786)
def kopruden(a):
    return abs(math.atan2(math.sin(a - DK), math.cos(a - DK)))
for k in range(20):
    a = TAU * k / 20 + 0.55
    if kopruden(a) < 0.45: continue
    r = 0.29 + 0.11 * ((k * 7) % 5) / 4
    p = M + V(math.cos(a), math.sin(a)) * r
    zz = hz(p.x, p.y)
    rr = 0.022 + 0.008 * (k % 3) / 2
    kure(y, (p.x, p.y, zz + rr * 0.45), rr, 'yesil_koyu' if k % 3 else 'zeytin', n=8, kat=4)
    kure(y, (p.x + rr * 0.8, p.y - rr * 0.4, zz + rr * 0.3), rr * 0.7, 'boya_yesil' if k % 2 else 'yesil_koyu', n=7, kat=4)
    if k % 3 == 1:
        for j in range(3):
            kure(y, (p.x + rr * 0.9 * math.cos(j * 2.1), p.y + rr * 0.9 * math.sin(j * 2.1), zz + rr * 0.8), 0.0045, 'boya_sari', n=5, kat=3)
# a fraise: sharpened stakes driven into the slope at mid height, pointing out and up (not across the bridge)
nf = 64
for k in range(nf):
    a = TAU * (k + 0.5) / nf
    if kopruden(a) < 0.32: continue
    d = V(math.cos(a), math.sin(a))
    r = 0.355 + 0.006 * (k % 2)
    p = M + d * r
    zz = hz(p.x, p.y)
    tip = p + d * (0.042 + 0.006 * ((k * 3) % 2)) + Z * (zz + 0.034)
    boru(y, [V(p.x, p.y, zz - 0.006) - d * 0.006, tip], 0.0055, 'kutuk', n=5, r_son=0.0012)
# a wattle revetment round the motte's foot at the ditch's inner edge
for k in range(56):
    a = TAU * k / 56
    p = M + V(math.cos(a), math.sin(a)) * 0.432
    cubuk(y, V(p.x, p.y, ZW - 0.004), V(p.x, p.y, G + 0.028), 0.006, 'ahsap_koyu')
for zz in (G - 0.004, G + 0.012):
    pts = [M + V(math.cos(TAU * k / 56), math.sin(TAU * k / 56)) * 0.436 + Z * zz for k in range(57)]
    boru(y, pts, 0.0055, 'kutuk', n=4)
for k, (a, r) in enumerate(((2.4, 0.36), (2.7, 0.33), (3.6, 0.4), (4.3, 0.37))):
    p = M + V(math.cos(a), math.sin(a)) * r
    zz = hz(p.x, p.y)
    with parca(y, (p.x, p.y, zz - 0.002), a + 1.7 + 0.4 * k, 0.55):
        boru(y, [V(-0.014, 0, 0.042), V(0.014, 0, 0.042)], 0.017, 'beyaz', n=8)
        for xx in (-0.014, 0.014):
            kure(y, (xx, 0, 0.042), 0.017, 'beyaz', n=8, kat=4)
        kure(y, (0.036, 0, 0.05), 0.009, 'koyu', n=6, kat=3)
        for (lx, ly) in ((-0.016, -0.01), (-0.016, 0.01), (0.018, -0.01), (0.018, 0.01)):
            cubuk(y, V(lx, ly, 0.0), V(lx, ly, 0.03), 0.005, 'koyu')

y.bolum('Motte: palisat')
RP = 0.228
dk_ac = math.atan2(-0.617, 0.786)       # towards the bridge
yay_k = [M + V(math.cos(dk_ac + 0.3 + (TAU - 0.6) * i / 52), math.sin(dk_ac + 0.3 + (TAU - 0.6) * i / 52)) * RP for i in range(53)]
palisad(y, yay_k, lambda x, yy: ZT, 0.1, adim=0.022, r=0.011, tohum=1)
# the gate in the motte palisade: two posts and a lintel
for s in (-1, 1):
    p = M + V(math.cos(dk_ac + s * 0.3), math.sin(dk_ac + s * 0.3)) * RP
    y.prizma((p.x, p.y), 0.014, ZT - 0.02, ZT + 0.14, 'kutuk', n=8)
pa = M + V(math.cos(dk_ac + 0.3), math.sin(dk_ac + 0.3)) * RP
pb = M + V(math.cos(dk_ac - 0.3), math.sin(dk_ac - 0.3)) * RP
cubuk(y, pa + Z * (ZT + 0.13), pb + Z * (ZT + 0.13), 0.018, 'ahsap_koyu', 0.016)


def ahsap_kule(c, w, z0, h, galeri, cati_h, aci=0.0, o=0.025, kapi_yon=True, cati='sindira'):
    """a timber tower w square, built round c and turned by aci: plank walls between corner posts with girts,
    braces and slits (a door on the local -y face), an overhanging fighting gallery (o beyond the walls, galeri
    high) on brackets with shuttered openings, a shingled pyramid roof. Returns the roof's tip z"""
    with parca(y, (c[0], c[1], z0), aci):
        k = dikdortgen(-w / 2, w / 2, -w / 2, w / 2)
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
            if i == 0 and kapi_yon:
                dikdortgen_acik(y, a, b, 0, h, 0.36, 0.64, 0.0, 0.11, ('ahsap_dikey', 'ahsap_koyu', 'ahsap', 'ahsap_koyu'), derin=0.012,
                                cerceve=(0.006, 'ahsap_koyu'))
            else:
                duz_duvar(y, a, b, 0, h, 'ahsap_dikey')
            for zz in (0.005, h * 0.36, h * 0.7, h - 0.006):   # girts
                cubuk(y, a + nn * 0.004 + Z * zz, b + nn * 0.004 + Z * zz, 0.009, 'ahsap_koyu', 0.007)
            cubuk(y, a + nn * 0.004 + Z * 0.0, a + nn * 0.004 + Z * h, 0.014, 'kutuk', 0.012)
            # braces in the upper bays, slits between
            if not (i == 0 and kapi_yon):
                cubuk(y, a.lerp(b, 0.06) + nn * 0.004 + Z * (h * 0.36), a.lerp(b, 0.44) + nn * 0.004 + Z * (h * 0.7), 0.007, 'ahsap_koyu', 0.005)
                cubuk(y, a.lerp(b, 0.94) + nn * 0.004 + Z * (h * 0.36), a.lerp(b, 0.56) + nn * 0.004 + Z * (h * 0.7), 0.007, 'ahsap_koyu', 0.005)
                yarik(y, a + nn * 0.004, e, nn, L / 2 - 0.005, h * 0.42, 0.01, h * 0.2, 'koyu')
            yarik(y, a + nn * 0.004, e, nn, L * 0.25 - 0.005, h * 0.08 if not (i == 0 and kapi_yon) else h * 0.42, 0.01, h * 0.14, 'koyu')
        # the gallery
        kg = disa(k, o)
        for i in range(4):
            j = (i + 1) % 4
            y.yuz_yon([k[i] + Z * h, k[j] + Z * h, kg[j] + Z * h, kg[i] + Z * h], 'ahsap_koyu', -Z)
            a, b = kg[i], kg[j]
            L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
            n = 3
            for m in range(n):
                p, q = a.lerp(b, m / n), a.lerp(b, (m + 1) / n)
                dikdortgen_acik(y, p, q, h, galeri, 0.25, 0.75, galeri * 0.3, galeri * 0.75, ('ahsap', 'ahsap_koyu', 'ahsap_koyu', 'koyu'), derin=0.01)
                # a shutter propped open above each opening
                pm = p.lerp(q, 0.5)
                kutu3(y, pm + nn * 0.012 + Z * (h + galeri * 0.82), e, (nn * 0.6 + Z).normalized(), (Z - nn * 0.6).normalized(),
                      (q - p).length * 0.52, 0.004, galeri * 0.3, 'ahsap_acik')
            for m in range(n + 1):   # brackets
                p = a.lerp(b, m / n)
                pin = k[i].lerp(k[j], m / n)
                cubuk(y, pin + Z * (h - 0.05), p + Z * (h - 0.003) - nn * 0.003, 0.009, 'ahsap_koyu', 0.008)
                cubuk(y, p + Z * h, p + Z * (h + galeri), 0.01, 'ahsap_koyu', 0.01)
            cubuk(y, a + nn * 0.003 + Z * (h + galeri - 0.004), b + nn * 0.003 + Z * (h + galeri - 0.004), 0.009, 'ahsap_koyu', 0.006)
        xs = [p.x for p in kg]
        top = cati_kirma(y, min(xs), max(xs), min(xs), max(xs), h + galeri, cati_h, 0.022, cati, 'ahsap_koyu', ns=6, nr=7, mahya_en=0.012)
        y.prizma((0, 0), 0.004, top - 0.01, top + 0.04, 'demir', n=5)
        kure(y, (0, 0, top + 0.045), 0.009, 'altin', n=8, kat=4)
        return z0 + top + 0.05


y.bolum('Motte: ahşap donjon')
KACI = math.atan2(0.786, 0.617)       # the keep's door faces the bridge
tip = ahsap_kule(M, 0.2, ZT, 0.34, 0.09, 0.27, KACI, o=0.026)
# a stone footing round the keep and a lean-to store against it
kutu_merkez(y, (M.x, M.y), 0.22, 0.22, 0.024, 'granit_koyu', z0=ZT - 0.012, aci=KACI)
with parca(y, (M.x, M.y, ZT), KACI):
    kutu(y, V(-0.07, 0.1, 0.0), X, 0.14, 0.06, 0.068, 'ahsap_dikey', 'arkasagsolust')
    for sx in (-1, 1):
        y.yuz_yon([V(sx * 0.07, 0.1, 0.068), V(sx * 0.07, 0.16, 0.068), V(sx * 0.07, 0.16, 0.0725), V(sx * 0.07, 0.1, 0.1)], 'ahsap_dikey', V(sx, 0))
    levha(y, [V(-0.078, 0.1, 0.1), V(0.078, 0.1, 0.1), V(0.078, 0.172, 0.068), V(-0.078, 0.172, 0.068)], 'sindira', V(0, 0.4, 1), 0.006)
    for k in range(3):   # barrels by the keep's door
        y.prizma((-0.06 + 0.026 * k, -0.135), 0.011, 0.0, 0.028, 'ahsap_acik', n=10)
y.bolum('Sancak')
sancak(y, M.x, M.y, tip - 0.01, boy=0.16, en=0.12, yuk=0.07, aci=math.pi * 0.8)
# guards on the motte
for k, a in enumerate((dk_ac + 0.9, dk_ac + 2.3, dk_ac - 1.6)):
    p = M + V(math.cos(a), math.sin(a)) * 0.19
    insan(y, p.x, p.y, ZT, 'boya_kirmizi' if k % 2 else 'kumas', aci=a, kol=0.0, sapka='demir')

# ---------------------------------------------------------------- the flying bridge
y.bolum('Uçan köprü: tepeye çıkan merdivenli ahşap köprü')
EB = lambda t: BC + V(BRX * math.cos(t), BRY * math.sin(t))
TB = math.radians(141)
B0 = EB(TB)                                  # its foot, on the bailey bank
du = (M - B0).normalized()
B1 = M - du * 0.21                           # its head, inside the motte palisade
z_0, z_1 = ZB + 0.004, ZT + 0.004
Lb = (B1 - B0).length
nb = V(du.y, -du.x)                          # across the bridge
BW = 0.07
P = lambda t, s=0.0: V(B0.x, B0.y).lerp(V(B1.x, B1.y), t) + nb * s + Z * (z_0 + (z_1 - z_0) * t)
for s in (-1, 1):   # stringers
    cubuk(y, P(-0.01, s * BW / 2) - Z * 0.012, P(1.0, s * BW / 2) - Z * 0.012, 0.012, 'ahsap_koyu', 0.022)
nst = 18
for k in range(nst):   # steps
    t = (k + 0.5) / nst
    c = P(t) - Z * ((z_1 - z_0) / nst * 0.5)
    kutu3(y, c, du, nb, Z, Lb / nst * 1.02, BW - 0.004, 0.008, 'ahsap' if k % 2 else 'ahsap_acik')
# railings: posts and a rail on each side
for s in (-1, 1):
    for k in range(7):
        t = k / 6
        p = P(t, s * (BW / 2 + 0.004))
        cubuk(y, p - Z * 0.01, p + Z * 0.06, 0.007, 'ahsap_koyu')
    cubuk(y, P(0, s * (BW / 2 + 0.004)) + Z * 0.058, P(1, s * (BW / 2 + 0.004)) + Z * 0.058, 0.007, 'ahsap', 0.007)
# trestles down to the slope and into the ditch
for t in (0.18, 0.4, 0.62, 0.82):
    p = P(t)
    zg = hz(p.x, p.y)
    zb_ = p.z - 0.022
    if zb_ - zg < 0.02: continue
    for s in (-1, 1):
        q = V(p.x, p.y) + nb * (s * (BW / 2 + 0.012))
        cubuk(y, V(q.x, q.y, zg - 0.015), V(q.x, q.y, zb_), 0.013, 'kutuk', 0.013)
    qa, qb = V(p.x, p.y) - nb * (BW / 2 + 0.02), V(p.x, p.y) + nb * (BW / 2 + 0.02)
    cubuk(y, qa + Z * zb_, qb + Z * zb_, 0.012, 'ahsap_koyu', 0.012)
    if zb_ - zg > 0.06:
        cubuk(y, qa + nb * 0.008 + Z * (zg + 0.01), qb - nb * 0.008 + Z * (zb_ - 0.01), 0.007, 'ahsap_koyu', 0.006)
        cubuk(y, qa + nb * 0.008 + Z * ((zg + zb_) / 2), qb - nb * 0.008 + Z * ((zg + zb_) / 2), 0.008, 'ahsap_koyu', 0.006)
# the landing at the foot
kutu3(y, P(0) + V(0, 0, -0.004) - du * 0.035, du, nb, Z, 0.07, BW + 0.02, 0.01, 'ahsap')

# ---------------------------------------------------------------- the bailey
y.bolum('Bailey: toprak set ve palisat')
NE = 72
E = [EB(TAU * i / NE) for i in range(NE)]
o1, o2, i1, i2 = disa(E, 0.07), disa(E, 0.018), disa(E, -0.018), disa(E, -0.06)
for i in range(NE):
    j = (i + 1) % NE
    nrm = V(E[j].y - E[i].y, -(E[j].x - E[i].x)).normalized()
    y.yuz_yon([o1[i] + Z * G, o1[j] + Z * G, o2[j] + Z * ZB, o2[i] + Z * ZB], 'cimen', nrm + Z)
    y.yuz_yon([o2[i] + Z * ZB, o2[j] + Z * ZB, i1[j] + Z * ZB, i1[i] + Z * ZB], 'toprak', Z)
    y.yuz_yon([i1[i] + Z * ZB, i1[j] + Z * ZB, i2[j] + Z * G, i2[i] + Z * G], 'cimen_kuru', -nrm + Z)
# the trampled yard inside: rings of quads (for the baked shadow) and a centre fan
ring = lambda f: [BC + (p - BC) * f + Z * (G + 0.002) for p in i2]
rs = [ring(f) for f in (0.999, 0.8, 0.55, 0.3)]
for k in range(len(rs) - 1):
    for i in range(NE):
        j = (i + 1) % NE
        y.yuz_yon([rs[k][i], rs[k][j], rs[k + 1][j], rs[k + 1][i]], 'toprak_ot', Z)
for i in range(NE):
    y.yuz_yon([rs[-1][i], rs[-1][(i + 1) % NE], BC + Z * (G + 0.002)], 'toprak_ot', Z)
# the palisade on the bank, with gaps at the gate (front) and at the bridge
L_E = sum((E[(i + 1) % NE] - E[i]).length for i in range(NE))
def s_of(t):   # arc length to the ellipse point at angle t
    return L_E * (t % TAU) / TAU
GT = math.radians(270)
palisad(y, E, lambda x, yy: ZB, 0.11, adim=0.024, r=0.011, tohum=2, kapali=True,
        gecit=[(s_of(GT) - 0.085, s_of(GT) + 0.085), (s_of(TB) - 0.06, s_of(TB) + 0.06)])
for s in (-1, 1):   # posts flanking the bridge's gap
    p = EB(TB + s * 0.13)
    y.prizma((p.x, p.y), 0.015, ZB - 0.02, ZB + 0.15, 'kutuk', n=8)

y.bolum('Bailey: kapı kulesi ve asma köprü')
GP = EB(GT)
with parca(y, (GP.x, GP.y, ZB), 0.0):
    gw, gd, gh = 0.17, 0.12, 0.15
    for sx in (-1, 1):   # the passage's side walls (plank, between posts)
        x = sx * gw / 2
        a, b = (V(x, -gd / 2), V(x, gd / 2)) if sx > 0 else (V(x, gd / 2), V(x, -gd / 2))
        duz_duvar(y, a, b, -0.02, gh, 'ahsap_dikey')
        a2, b2 = V(x - sx * 0.012, gd / 2), V(x - sx * 0.012, -gd / 2)
        if sx < 0: a2, b2 = b2, a2
        duz_duvar(y, a2, b2, -0.02, gh, 'ahsap_dikey')
        for yy in (-gd / 2, gd / 2):
            y.prizma((x, yy), 0.012, -0.02, gh + 0.11, 'kutuk', n=8)
        y.yuz_yon([V(x, -gd / 2, gh), V(x, gd / 2, gh), V(x - sx * 0.012, gd / 2, gh), V(x - sx * 0.012, -gd / 2, gh)], 'ahsap_koyu', Z)
    # the passage's ceiling and the doors standing open inside
    y.yuz_yon([V(-gw / 2 + 0.012, -gd / 2, gh), V(gw / 2 - 0.012, -gd / 2, gh), V(gw / 2 - 0.012, gd / 2, gh), V(-gw / 2 + 0.012, gd / 2, gh)], 'ahsap_koyu', -Z)
    for sx in (-1, 1):
        kutu3(y, V(sx * (gw / 2 - 0.016), -gd / 2 + 0.04, gh * 0.45), Y, X, Z, 0.07, 0.006, gh * 0.88, 'ahsap')
    # the upper room overhanging the passage
    k2 = dikdortgen(-gw / 2 - 0.012, gw / 2 + 0.012, -gd / 2 - 0.012, gd / 2 + 0.012)
    for i in range(4):
        a, b = k2[i], k2[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        n = 2 if L > 0.15 else 1
        for m in range(n):
            p, q = a.lerp(b, m / n), a.lerp(b, (m + 1) / n)
            dikdortgen_acik(y, p, q, gh, 0.1, 0.3, 0.7, 0.035, 0.075, ('ahsap_dikey', 'ahsap_koyu', 'ahsap_koyu', 'koyu'), derin=0.01)
        cubuk(y, a + nn * 0.004 + Z * gh, a + nn * 0.004 + Z * (gh + 0.1), 0.012, 'kutuk', 0.012)
        cubuk(y, a + nn * 0.004 + Z * (gh + 0.005), b + nn * 0.004 + Z * (gh + 0.005), 0.01, 'ahsap_koyu', 0.008)
        y.yuz_yon([a + Z * gh, b + Z * gh, k2[(i + 1) % 4] * 0.93 + Z * gh, a * 0.93 + Z * gh], 'ahsap_koyu', -Z)
    xs = [p.x for p in k2]; ys = [p.y for p in k2]
    cati_kirma(y, min(xs), max(xs), min(ys), max(ys), gh + 0.1, 0.1, 0.018, 'sindira', 'ahsap_koyu', ns=6, nr=5, mahya_en=0.01)
    # the drawbridge lowered over the moat, chains to the tower
    dl = (-gd / 2) - (YC0 - 0.03 - GP.y)
    y0_, y1_ = -gd / 2, YC0 - 0.03 - GP.y
    for k in range(8):
        ya, yb = y0_ + (y1_ - y0_) * k / 8, y0_ + (y1_ - y0_) * (k + 1) / 8
        za, zb_ = 0.0 + (G - ZB) * k / 8, (G - ZB) * (k + 1) / 8
        kutu3(y, V(0, (ya + yb) / 2, (za + zb_) / 2 + 0.004), X, V(0, yb - ya, zb_ - za), V(0, -(zb_ - za), yb - ya), 0.12, abs(yb - ya) * 1.02, 0.008,
              'ahsap' if k % 2 else 'ahsap_acik')
    for sx in (-1, 1):
        cubuk(y, V(sx * 0.055, y0_, 0.012), V(sx * 0.055, y1_, G - ZB + 0.012), 0.01, 'ahsap_koyu', 0.008)
        boru(y, [V(sx * 0.055, y1_ + 0.01, G - ZB + 0.016), V(sx * 0.06, -gd / 2 - 0.006, gh + 0.06)], 0.0025, 'demir', n=4)
# the road on, past the moat
y.yuz_yon([V(GP.x - 0.06, YA + 0.001, G + 0.0025), V(GP.x + 0.06, YA + 0.001, G + 0.0025), V(GP.x + 0.06, YC0 - 0.03, G + 0.0025),
           V(GP.x - 0.06, YC0 - 0.03, G + 0.0025)], 'toprak', Z)
# bridge piers in the moat
for sx in (-1, 1):
    for yy in ((YC0 + YC1) / 2,):
        y.prizma((GP.x + sx * 0.05, yy), 0.009, ZW - 0.01, ZB - 0.01 - (ZB - G) * 0.4, 'kutuk', n=6)

# ---------------------------------------------------------------- inside the bailey
y.bolum('Bailey: salon (aula)')
ev(y, 0.48, -0.03, G, 0.4, 0.17, 0.13, math.pi, 'sindira', tohum=3, cati_h=0.15, duvar='siva_krem', ahsap='ahsap_koyu', taban='granit_koyu')
y.bolum('Bailey: şapel')
koy_kilisesi(y, 0.7, -0.43, G, -math.pi / 2, 0.6, 'arduvaz', 'kirec', 'granit', kule_h=0.4, kule_cati=0.28)

y.bolum('Bailey: ahır')
with parca(y, (0.08, -0.36, G), math.radians(-60)):
    W_, D_, H_ = 0.28, 0.12, 0.085
    # back and side walls of planks, open front with posts, a lean-to roof
    kutu3(y, V(0, D_ / 2 - 0.004, (H_ + 0.03) / 2), X, Y, Z, W_, 0.008, H_ + 0.03, 'ahsap_dikey', ('+y', '-y', '+x', '-x'))
    for sx in (-1, 1):
        a, b = (V(sx * W_ / 2, -D_ / 2), V(sx * W_ / 2, D_ / 2))
        if sx < 0: a, b = b, a
        y.yuz_yon([V(a.x, a.y, 0), V(b.x, b.y, 0), V(b.x, b.y, H_ + (0.03 if b.y > 0 else 0)), V(a.x, a.y, H_ + (0.03 if a.y > 0 else 0))], 'ahsap_dikey', V(sx, 0))
        y.yuz_yon([V(a.x - sx * 0.008, a.y, 0), V(b.x - sx * 0.008, b.y, 0), V(b.x - sx * 0.008, b.y, H_ + (0.03 if b.y > 0 else 0)),
                   V(a.x - sx * 0.008, a.y, H_ + (0.03 if a.y > 0 else 0))], 'ahsap_koyu', V(-sx, 0))
    for k in range(5):
        x = -W_ / 2 + 0.01 + (W_ - 0.02) * k / 4
        cubuk(y, V(x, -D_ / 2, 0), V(x, -D_ / 2, H_), 0.01, 'kutuk')
    cubuk(y, V(-W_ / 2, -D_ / 2, H_), V(W_ / 2, -D_ / 2, H_), 0.012, 'ahsap_koyu')
    q = [V(-W_ / 2 - 0.015, -D_ / 2 - 0.03, H_ - 0.006), V(W_ / 2 + 0.015, -D_ / 2 - 0.03, H_ - 0.006), V(W_ / 2 + 0.015, D_ / 2 + 0.015, H_ + 0.034),
         V(-W_ / 2 - 0.015, D_ / 2 + 0.015, H_ + 0.034)]
    y.yuz_yon(q, 'sindira', V(0, -0.4, 1))
    for k in range(9):   # battens up the slope
        t = (k + 0.5) / 9
        a_, b_ = q[0].lerp(q[1], t), q[3].lerp(q[2], t)
        cubuk(y, a_ + Z * 0.003, b_ + Z * 0.003, 0.006, 'ahsap_koyu', 0.004)
    y.yuz_yon([p - Z * 0.008 for p in q], 'ahsap_koyu', -Z)
    for (a, b, nrm) in ((q[0], q[1], -Y), (q[1], q[2], X), (q[2], q[3], Y), (q[3], q[0], -X)):
        y.yuz_yon([a, b, b - Z * 0.008, a - Z * 0.008], 'saz_koyu', nrm)
    # stalls and horses
    for k in range(3):
        x = -W_ / 2 + W_ * (k + 1) / 4
        kutu3(y, V(x + 0.035, 0.0, 0.03), X, Y, Z, 0.005, D_ * 0.8, 0.06, 'ahsap')
    at(y, -0.07, 0.0, 0.0, -math.pi / 2, 0.8, 'ahsap_acik', 'ahsap_koyu')
    at(y, 0.0, 0.0, 0.0, -math.pi / 2, 0.8, 'koyu', 'koyu')
    at(y, 0.07, 0.0, 0.0, -math.pi / 2, 0.8, 'beyaz', 'granit')
    donel(y, (0.12, -0.03), [(0.025, 0.0), (0.024, 0.02), (0.014, 0.038), (0.0, 0.042)], 'saz', n=10)

y.bolum('Bailey: demirhane')
with parca(y, (0.28, -0.6, G), 0.0):
    W_, D_, H_ = 0.15, 0.1, 0.075
    kutu(y, V(-W_ / 2, -D_ / 2, 0), X, W_, D_, H_, 'granit', 'arkasagsol')
    for sx in (-1, 1):
        y.prizma((sx * (W_ / 2 - 0.008), -D_ / 2), 0.008, 0, H_, 'kutuk', n=6)
    y.yuz_yon([V(-W_ / 2 + 0.002, D_ / 2 - 0.002, 0), V(W_ / 2 - 0.002, D_ / 2 - 0.002, 0), V(W_ / 2 - 0.002, D_ / 2 - 0.002, H_), V(-W_ / 2 + 0.002, D_ / 2 - 0.002, H_)], 'koyu', -Y)
    for sx in (-1, 1):
        y.yuz_yon([V(sx * (W_ / 2 - 0.002), D_ / 2, 0), V(sx * (W_ / 2 - 0.002), -D_ / 2, 0), V(sx * (W_ / 2 - 0.002), -D_ / 2, H_), V(sx * (W_ / 2 - 0.002), D_ / 2, H_)], 'tas_koyu', V(-sx, 0))
    cati_besik(y, -W_ / 2, W_ / 2, -D_ / 2, D_ / 2, H_, 0.06, 0.018, 'sindira', 'ahsap_koyu', ucluk_key='granit', ns=5, nr=4, uc_sacak=0.012)
    # forge with its glow, the chimney, the anvil, a smith
    kutu_merkez(y, (-0.035, D_ / 2 - 0.025), 0.05, 0.04, 0.03, 'granit_koyu')
    y.yuz_yon([V(-0.055, D_ / 2 - 0.04, 0.0305), V(-0.015, D_ / 2 - 0.04, 0.0305), V(-0.015, D_ / 2 - 0.01, 0.0305), V(-0.055, D_ / 2 - 0.01, 0.0305)], 'boya_sari', Z)
    kutu_merkez(y, (-0.035, D_ / 2 - 0.012), 0.032, 0.026, 0.2, 'granit', z0=0.03)
    kutu_merkez(y, (-0.035, D_ / 2 - 0.012), 0.038, 0.032, 0.008, 'granit_koyu', z0=0.23)
    y.prizma((0.03, -0.02), 0.009, 0.0, 0.022, 'kutuk', n=8)
    kutu_merkez(y, (0.03, -0.02), 0.026, 0.011, 0.01, 'demir', z0=0.022)
    insan(y, 0.03, -0.065, 0.0, 'ahsap_koyu', aci=math.pi / 2, kol=0.8)

y.bolum('Bailey: kuyu, samanlıklar, garnizon')
KX, KY = 0.5, -0.36
donel(y, (KX, KY), [(0.03, G), (0.03, G + 0.035), (0.023, G + 0.035), (0.023, G + 0.027)], 'granit', n=14)
y.yuz_yon([V(p.x, p.y, G + 0.027) for p in cokgen((KX, KY), 0.023, 14)], 'su', Z)
for s in (-1, 1):
    cubuk(y, V(KX + s * 0.028, KY, G + 0.03), V(KX + s * 0.028, KY, G + 0.09), 0.006, 'ahsap_koyu')
boru(y, [V(KX - 0.03, KY, G + 0.08), V(KX + 0.03, KY, G + 0.08)], 0.005, 'ahsap', n=6)
cati_besik(y, KX - 0.04, KX + 0.04, KY - 0.03, KY + 0.03, G + 0.09, 0.03, 0.008, 'sindira', 'ahsap_koyu', ucluk_key='ahsap_dikey', ns=3, nr=3,
           uc_sacak=0.006, mahya_en=0.008)
for (hx, hy, hs) in ((0.85, -0.14, 1.0), (0.93, -0.22, 0.85), (0.2, -0.05, 0.9)):
    donel(y, (hx, hy), [(0.045 * hs, G), (0.048 * hs, G + 0.03 * hs), (0.035 * hs, G + 0.07 * hs), (0.012 * hs, G + 0.095 * hs), (0.0, G + 0.1 * hs)],
          'saz', n=12, dilim=['saz', 'saz_koyu'])
# barrels and crates by the hall
for k in range(4):
    y.prizma((0.27 + 0.028 * k, -0.15), 0.012, G, G + 0.028, 'ahsap_acik', n=10)
    halka_kornis(y, (0.27 + 0.028 * k, -0.15), 0.012, G + 0.008, 0.003, 0.001, 10, 'demir')
for k in range(2):
    kutu_merkez(y, (0.68 + 0.035 * k, -0.17), 0.03, 0.03, 0.026, 'ahsap', z0=G, aci=0.2 * k)
# the garrison: spearmen in the yard, a sentry on the gatehouse
for k, (x, yy, a) in enumerate(((0.38, -0.5, 1.2), (0.43, -0.52, 1.4), (0.48, -0.5, 1.6), (0.53, -0.52, 1.8), (0.62, -0.32, 3.0),
                                (0.35, -0.3, 0.2), (0.4, -0.62, 1.5))):
    insan(y, x, yy, G + 0.002, 'boya_kirmizi' if k % 3 else 'kumas', aci=a, sapka='demir')
    cubuk(y, V(x + 0.009, yy, G + 0.002), V(x + 0.009, yy, G + 0.075), 0.0025, 'ahsap')
    y.koni((x + 0.009, yy), 0.003, G + 0.075, 0.01, 'demir', n=4)
sovalye(y, 0.58, -0.6, G + 0.002, math.radians(100), 0.9, 'boya_kirmizi', 'boya_sari', mizrak=False, kosu=0.0, sorguc='boya_sari')

# ---------------------------------------------------------------- outside
y.bolum('Dışarısı: köy evleri (bourg)')
ev(y, -0.78, -0.62, G, 0.18, 0.11, 0.09, 0.15, 'saz', tohum=1)
ev(y, -0.45, -0.67, G, 0.16, 0.11, 0.085, -0.1, 'saz', tohum=2, kapi_u=0.4)
ev(y, -0.12, -0.6, G, 0.15, 0.1, 0.08, 0.3, 'saz', tohum=3)
for (hx, hy) in ((-0.95, -0.42), (-0.6, -0.48)):
    donel(y, (hx, hy), [(0.04, G), (0.043, G + 0.03), (0.032, G + 0.065), (0.011, G + 0.088), (0.0, G + 0.092)], 'saz', n=12, dilim=['saz', 'saz_koyu'])
y.yuz_yon([V(-1.0, -0.79, G + 0.0045), V(0.38, -0.79, G + 0.0045), V(0.38, -0.75, G + 0.0045), V(-1.0, -0.75, G + 0.0045)], 'toprak', Z)
for k, (x, yy, key, a) in enumerate(((-0.62, -0.72, 'kumas', 0.4), (-0.3, -0.78, 'boya_yesil', 2.2), (0.0, -0.74, 'ahsap_acik', 3.1))):
    insan(y, x, yy, G + 0.004, key, aci=a, sapka='saz' if k == 0 else None)
# cattle grazing by the motte ditch
for k, (x, yy, a) in enumerate(((-1.0, -0.2, 0.4), (-0.88, -0.28, 2.0), (0.1, 0.35, 1.2))):
    at(y, x, yy, G, a, 0.7, 'beyaz' if k % 2 else 'kerpic_koyu', 'koyu')

y.bolum('Dışarısı: ağaçlar, yol, tarla')
for (tx, ty, tb, tt) in ((1.1, 0.95, 0.22, 'yaprakli'), (0.95, 0.85, 0.18, 'yaprakli'), (1.12, 0.6, 0.2, 'yaprakli'), (0.2, 0.95, 0.18, 'yaprakli'),
                         (-1.1, -0.75, 0.18, 'yaprakli'), (-1.1, -0.5, 0.15, 'yaprakli'), (1.12, -0.78, 0.17, 'yaprakli'),
                         (0.25, 0.6, 0.2, 'yaprakli'), (0.08, 0.78, 0.16, 'servi'), (-1.12, 1.0, 0.2, 'servi'), (-0.25, -0.42, 0.14, 'yaprakli'),
                         (0.15, -0.83, 0.15, 'yaprakli'), (-1.1, -1.03, 0.14, 'yaprakli'), (-0.7, -1.03, 0.13, 'yaprakli')):
    agac(y, tx, ty, G, boy=tb, tur=tt, key='boya_yesil' if int(abs(tx) * 10) % 2 else 'zeytin')
# strip fields behind the bailey
for i, k in enumerate(('saz', 'toprak', 'cimen_kuru', 'saz')):
    x0_ = 0.45 + 0.17 * i
    kutu(y, V(x0_, 0.32, G - 0.002), X, 0.15, 0.36, 0.014 if k == 'saz' else 0.006, k if k != 'saz' else 'saz_koyu', 'onarkasagsol')
    y.yuz_yon([V(x0_, 0.32, G + (0.012 if k == 'saz' else 0.004)), V(x0_ + 0.15, 0.32, G + (0.012 if k == 'saz' else 0.004)),
               V(x0_ + 0.15, 0.68, G + (0.012 if k == 'saz' else 0.004)), V(x0_, 0.68, G + (0.012 if k == 'saz' else 0.004))], k, Z)
    if k == 'toprak':
        for j in range(5):
            xx = x0_ + 0.15 * (j + 0.5) / 5
            cubuk(y, V(xx, 0.33, G + 0.005), V(xx, 0.67, G + 0.005), 0.012, 'kerpic_koyu', 0.006)
    elif k == 'saz':   # standing grain: ridged rows, a darker furrow between
        for j in range(5):
            xx = x0_ + 0.15 * (j + 0.5) / 5
            w = 0.15 / 5 * 0.46
            for s in (-1, 1):
                y.yuz_yon([V(xx + s * w, 0.322, G + 0.012), V(xx + s * w, 0.678, G + 0.012), V(xx, 0.678, G + 0.024), V(xx, 0.322, G + 0.024)],
                          'boya_sari' if j % 2 else 'saz', V(s, 0, 0.9))
            for yy_, nn_ in ((0.322, -Y), (0.678, Y)):
                y.yuz_yon([V(xx - w, yy_, G + 0.012), V(xx + w, yy_, G + 0.012), V(xx, yy_, G + 0.024)], 'saz_koyu', nn_)
    elif k == 'cimen_kuru':
        for j in range(4):
            for m in (0.3, 0.7):
                donel(y, (x0_ + 0.15 * m, 0.36 + 0.28 * j / 3), [(0.014, G + 0.004), (0.012, G + 0.018), (0.005, G + 0.034), (0.0, G + 0.04)], 'saz', n=7)
# a road from the gate's far side along the moat
y.yuz_yon([V(XA + 0.001, -1.06, G + 0.0045), V(XB - 0.001, -1.06, G + 0.0045), V(XB - 0.001, -1.0, G + 0.0045), V(XA + 0.001, -1.0, G + 0.0045)], 'toprak', Z)

calistir(y, 'lm_motte')
