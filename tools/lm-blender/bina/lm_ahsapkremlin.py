# Ahşap Kremlin (lm_ahsapkremlin): an early Russian timber fortress. A square earthen rampart (val) carries log crib
# walls with a covered, roofed fighting gallery; square log towers with an overhanging upper storey (oblam), tall
# shingled tents and open lookouts; a gate tower with a ramp up the rampart, the gate icon and a flag. Inside: a
# Kizhi-like timber church (an octagon in tiers ringed by barrel gables, many scaled aspen onions) with its tented
# bell tower, two boyar houses with carved frames and steep roofs, a well, haystacks and people.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from rus_ortak import *
from frank_ortak import _ss
from bina_ortak import calistir
import doku

y = Yapi()
Z0 = 0.04
ZV = Z0 + 0.2                     # the rampart's top
GX0, GX1, GY0, GY1 = -1.18, 1.18, -1.14, 1.16
KOSE = [V(-0.92, -0.82), V(0.92, -0.82), V(0.92, 0.92), V(-0.92, 0.92)]   # the wall line (CCW)
SH = ['sindira', 'sindira2']
PUL = ['ahsap_acik', 'kutuk']


def cayir(x, yy, z):
    """meadow in soft patches; the rampart's slopes drier, worn earth on its crest and along the paths"""
    n1 = math.sin(x * 4.3 + 1.1) * math.cos(yy * 3.7 - 0.6)
    n2 = math.sin(x * 9.1 - yy * 6.3 + 2.0)
    n = n1 * 0.7 + n2 * 0.3
    c0, c1 = (0.38, 0.49, 0.24), (0.5, 0.53, 0.3)
    t = max(0.0, min(1.0, 0.5 + 0.5 * n))
    c = tuple(p + (q - p) * t for p, q in zip(c0, c1))
    # the rampart: dry, sun-burnt turf on its slopes turning to bare trodden earth at the crest, so the bank reads
    # against the meadow
    h = _ss(0.01, 0.08, z - Z0)
    c = tuple(p + (q - p) * h * 0.85 for p, q in zip(c, (0.6, 0.55, 0.3)))
    hc = _ss(0.12, 0.19, z - Z0)
    c = tuple(p + (q - p) * hc * 0.8 for p, q in zip(c, (0.5, 0.39, 0.25)))
    yt = 1 - _ss(0.04, 0.1, abs(x) + 0.02 * n2) if (yy < -0.3 and yy > -1.12) else 0.0
    return tuple(p + (q - p) * yt * 0.7 for p, q in zip(c, (0.55, 0.47, 0.34)))


doku.KOSE_RENK['cimen'] = cayir

# ---------------------------------------------------------------- ground and rampart
y.bolum('Zemin ve toprak set')
NX, NY = 24, 24
P = [[V(GX0 + (GX1 - GX0) * i / NX, GY0 + (GY1 - GY0) * j / NY, Z0) for j in range(NY + 1)] for i in range(NX + 1)]
for i in range(NX):
    for j in range(NY):
        y.yuz([P[i][j], P[i + 1][j], P[i + 1][j + 1]], 'cimen'); y.yuz([P[i][j], P[i + 1][j + 1], P[i][j + 1]], 'cimen')
for a, b in ((V(GX0, GY0), V(GX1, GY0)), (V(GX1, GY0), V(GX1, GY1)), (V(GX1, GY1), V(GX0, GY1)), (V(GX0, GY1), V(GX0, GY0))):
    duz_duvar(y, a, b, 0, Z0, 'toprak')
# the rampart: outer toe -> crest -> inner toe, round the wall line (a gap at the gate is bridged by the ramp)
PROF = [(0.23, Z0 - 0.002), (0.13, Z0 + 0.12), (0.06, ZV), (-0.06, ZV), (-0.14, Z0 + 0.08), (-0.21, Z0 - 0.002)]
rings = [[V(p.x, p.y, z) for p in disa(KOSE, d)] for d, z in PROF]
for k in range(len(rings) - 1):
    A_, B_ = rings[k], rings[k + 1]
    for i in range(4):
        j = (i + 1) % 4
        q = [A_[i], A_[j], B_[j], B_[i]]
        y.yuz_yon(q, 'cimen', Z)
# a row of sharpened stakes (chastik) driven into the outer slope, leaning out (left open at the gate's ramp)
for i in range(4):
    a, b = KOSE[i], KOSE[(i + 1) % 4]
    e = (b - a).normalized(); nc = V(e.y, -e.x); L = (b - a).length
    d0 = 0.18
    zb = Z0 - 0.002 + (0.23 - d0) / 0.1 * 0.122 - 0.012
    yon = (nc * 0.6 + Z * 0.8).normalized()
    k = 0
    while True:
        u = 0.2 + k * 0.05
        k += 1
        if u > L - 0.2: break
        if i == 0 and abs(u - L / 2) < 0.16: continue
        p = a + e * u + nc * d0 + Z * zb
        s = 0.085 + 0.014 * ((k * 7) % 3)
        boru(y, [p, p + yon * s], 0.0085, 'kutuk', n=5, kapat=False)
        boru(y, [p + yon * (s - 0.002), p + yon * (s + 0.03)], 0.0088, 'ahsap_acik', n=5, r_son=0.0008)

# ---------------------------------------------------------------- walls on the rampart
y.bolum('Kütük surlar ve örtülü yol')
WT = 0.07                       # wall thickness
ZW = ZV + 0.12                  # the wall walk
ZP = ZW + 0.06                  # the gallery's eave
for i in range(4):
    a, b = KOSE[i], KOSE[(i + 1) % 4]
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    L = (b - a).length
    t0, t1 = 0.12, L - 0.12
    if i == 0:   # the front: split at the gate tower
        parts = [(t0, L / 2 - 0.14), (L / 2 + 0.14, t1)]
    else:
        parts = [(t0, t1)]
    for u0, u1 in parts:
        pa, pb = a + e * u0, a + e * u1
        # outer and inner log faces of the crib, its earth-filled top as the walk
        kutuk_duvar2(y, pa + nc * (WT / 2), pb + nc * (WT / 2), ZV - 0.03, ZW, 0.012, 'kutuk_gri', uzanti=0.0)
        kutuk_duvar2(y, pb - nc * (WT / 2), pa - nc * (WT / 2), ZV - 0.03, ZW, 0.012, 'kutuk_gri', uzanti=0.0)
        y.yuz_yon([pa + nc * (WT / 2) + Z * ZW, pb + nc * (WT / 2) + Z * ZW, pb - nc * (WT / 2) + Z * ZW, pa - nc * (WT / 2) + Z * ZW], 'ahsap', Z)
        # the gallery's plank breastwork with loopholes on the outer edge
        o = nc * (WT / 2 + 0.012)
        duz_duvar(y, pa + o, pb + o, ZW - 0.02, ZP, 'ahsap_dikey')
        duz_duvar(y, pb + o - nc * 0.008, pa + o - nc * 0.008, ZW, ZP, 'ahsap_dikey')
        y.yuz_yon([pa + o + Z * ZP, pb + o + Z * ZP, pb + o - nc * 0.008 + Z * ZP, pa + o - nc * 0.008 + Z * ZP], 'ahsap_koyu', Z)
        for k in range(int((u1 - u0) / 0.075)):
            u = (k + 0.5) * (u1 - u0) / int((u1 - u0) / 0.075)
            yarik(y, pa + o + Z * ZW, e, nc, u - 0.006, 0.02, 0.012, 0.02, 'koyu')
        # the overhang (oblam) under the breastwork: its underside and a carved board
        y.yuz_yon([pa + nc * (WT / 2) + Z * (ZW - 0.02), pb + nc * (WT / 2) + Z * (ZW - 0.02), pb + o + Z * (ZW - 0.02), pa + o + Z * (ZW - 0.02)], 'ahsap_koyu', -Z)
        # posts on the inner edge and the gable roof over the walk
        for k in range(int((u1 - u0) / 0.15) + 1):
            p = pa + e * min(u1 - u0, k * 0.15) - nc * (WT / 2 - 0.006)
            y.prizma((p.x, p.y), 0.006, ZW, ZP + 0.01, 'ahsap_koyu', n=5, ust=False)
        rc = [pa - nc * (WT / 2), pb + o]
        xs = sorted((rc[0].x, rc[1].x)); ys = sorted((rc[0].y, rc[1].y))
        cati_besik(y, xs[0], xs[1], ys[0], ys[1], ZP, 0.055, 0.02, 'sindira', 'ahsap_koyu', kalinlik=0.008, ucluk_key='ahsap_dikey',
                   uc_sacak=0.0, nr=3, ns=max(4, int((u1 - u0) / 0.12)), dilim=SH)


# ---------------------------------------------------------------- towers
def kule(y, c, w, h, tent_h, gecit=False, bayrak=False):
    """a square log tower from the ground: the log shaft (w), an overhanging upper storey (oblam) with loopholes and
    a carved valance, a tall shingled tent, an open lookout with its own little tent and a vane (or a flag)"""
    cx, cy = c
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2
    zt = Z0 + h
    if not gecit:
        kutuk_kutu(y, x0, x1, y0, y1, Z0 + 0.03, h - 0.03, 0.012, 'kutuk_gri')
    else:
        # the gate: side and back log walls; the front has a passage at the rampart's top with the logs above it
        k = dikdortgen(x0, x1, y0, y1)
        for i in (1, 3):
            kutuk_duvar2(y, k[i], k[(i + 1) % 4], Z0 + 0.012, zt + 0.012, 0.012, 'kutuk_gri', uzanti=0.028)
        for yy, s in ((y0, 1), (y1, -1)):
            a_, b_ = (V(x0, yy), V(x1, yy)) if s > 0 else (V(x1, yy), V(x0, yy))
            pw = 0.075
            ee = (b_ - a_).normalized()
            m = (a_ + b_) / 2
            kutuk_duvar2(y, a_, m - ee * pw, Z0, zt, 0.012, 'kutuk_gri', uzanti=0.028 if s > 0 else 0.028)
            kutuk_duvar2(y, m + ee * pw, b_, Z0, zt, 0.012, 'kutuk_gri', uzanti=0.0)
            kutuk_duvar2(y, m - ee * pw, m + ee * pw, ZV + 0.15, zt, 0.012, 'kutuk_gri', uzanti=0.0)
            kutuk_duvar2(y, m - ee * pw, m + ee * pw, Z0, ZV, 0.012, 'kutuk_gri', uzanti=0.0)
        # the passage: floor, side boards, the lintel, open plank leaves
        y.yuz_yon([V(cx - 0.075, y0, ZV), V(cx + 0.075, y0, ZV), V(cx + 0.075, y1, ZV), V(cx - 0.075, y1, ZV)], 'ahsap', Z)
        for sx in (-1, 1):
            duz_duvar(y, V(cx + sx * 0.075, y0 if sx < 0 else y1), V(cx + sx * 0.075, y1 if sx < 0 else y0), ZV, ZV + 0.15, 'ahsap_dikey')
        y.yuz_yon([V(cx - 0.075, y0, ZV + 0.15), V(cx + 0.075, y0, ZV + 0.15), V(cx + 0.075, y1, ZV + 0.15), V(cx - 0.075, y1, ZV + 0.15)], 'ahsap_koyu', -Z)
        for sx in (-1, 1):
            with parca(y, (cx + sx * 0.075, y0 + 0.012, ZV), -sx * 0.5 + (0 if sx > 0 else math.pi)):
                kutu3(y, V(0.037, 0, 0.074), X, Y, Z, 0.074, 0.01, 0.148, 'ahsap_dikey')
                for zz in (0.03, 0.11):
                    kutu3(y, V(0.037, 0.0055, zz), X, Y, Z, 0.07, 0.003, 0.01, 'demir')
        # the gate icon in a little roofed case above the passage
        kutu3(y, V(cx, y0 - 0.02, ZV + 0.2), X, -Y, Z, 0.07, 0.016, 0.08, 'ahsap_koyu')
        y.oculus(V(cx, y0 - 0.028, ZV + 0.2), X, -Y, 0.024, 'altin', 'boya_kirmizi', f=0.006, k=12)
        cati_besik(y, cx - 0.045, cx + 0.045, y0 - 0.04, y0 - 0.0, ZV + 0.24, 0.035, 0.01, 'sindira', 'ahsap_koyu', kalinlik=0.005,
                   ucluk_key='ahsap_dikey', uc_sacak=0.008, nr=2, ns=3, dilim=SH)
    # loopholes in the shaft
    for i, (a_, b_) in enumerate(zip(dikdortgen(x0, x1, y0, y1), dikdortgen(x0, x1, y0, y1)[1:] + dikdortgen(x0, x1, y0, y1)[:1])):
        ee = (b_ - a_).normalized(); nn = V(ee.y, -ee.x)
        if gecit and i in (0, 2): continue
        yarik(y, a_ + nn * 0.011 + Z * Z0, ee, nn, w / 2 - 0.006, h * 0.6, 0.012, 0.03, 'koyu')
    # the oblam: a wider storey on projecting log ends, loopholes, a valance
    ow = w + 0.06
    ox0, ox1, oy0, oy1 = cx - ow / 2, cx + ow / 2, cy - ow / 2, cy + ow / 2
    zo = zt + 0.012
    for sx in (-1, 1):   # the projecting beam ends that carry it
        for t in (-0.3, 0.3):
            cubuk(y, V(cx + sx * (w / 2 - 0.01), cy + t * w, zo - 0.012), V(cx + sx * (ow / 2), cy + t * w, zo - 0.012), 0.016, 'kutuk_gri')
            cubuk(y, V(cx + t * w, cy + sx * (w / 2 - 0.01), zo - 0.026), V(cx + t * w, cy + sx * (ow / 2), zo - 0.026), 0.016, 'kutuk_gri')
    zoh = kutuk_kutu(y, ox0, ox1, oy0, oy1, zo, 0.1, 0.011, 'kutuk_gri', uzanti=0.02)
    iki_yuzlu(y, [V(p.x, p.y, zo - 0.001) for p in dikdortgen(ox0 + 0.004, ox1 - 0.004, oy0 + 0.004, oy1 - 0.004)], "ahsap_koyu", -Z)   # (the floor, seen from below and through the gaps under the logs)
    for i, (a_, b_) in enumerate(zip(dikdortgen(ox0, ox1, oy0, oy1), dikdortgen(ox0, ox1, oy0, oy1)[1:] + dikdortgen(ox0, ox1, oy0, oy1)[:1])):
        ee = (b_ - a_).normalized(); nn = V(ee.y, -ee.x)
        for u in (0.25, 0.5, 0.75):
            yarik(y, a_ + nn * 0.0095 + Z * zo, ee, nn, ow * u - 0.006, 0.04, 0.012, 0.03, 'koyu')
        oymali_sacak(y, a_ + nn * 0.012 + Z * (zo - 0.002), b_ + nn * 0.012 + Z * (zo - 0.002), nn, 'beyaz', 0.016, 4, 0.0)
    # the tent: a flared skirt then the steep shingled spire
    R = (ow / 2 + 0.03) * math.sqrt(2)
    ring = cokgen(c, R, 4, math.pi / 4)
    mid = cokgen(c, R * 0.6, 4, math.pi / 4)
    zm = zoh + 0.035
    tp = V(cx, cy, zoh + tent_h)
    for i in range(4):
        j = (i + 1) % 4
        out = (ring[i] + ring[j]) / 2 - V(cx, cy)
        y.yuz_yon([ring[i] + Z * zoh, ring[j] + Z * zoh, mid[j] + Z * zm, mid[i] + Z * zm], 'sindira', out + Z * 0.6)
        y.yuz_yon([ring[i] + Z * zoh, ring[j] + Z * zoh, ring[j] + Z * (zoh - 0.008), ring[i] + Z * (zoh - 0.008)], 'ahsap_koyu', out)
        for k in range(5):
            t0_, t1_ = k / 5, (k + 1) / 5
            A_, B_ = mid[i].lerp(V(cx, cy), t0_ * 0.9), mid[j].lerp(V(cx, cy), t0_ * 0.9)
            C_, D_ = mid[j].lerp(V(cx, cy), t1_ * 0.9), mid[i].lerp(V(cx, cy), t1_ * 0.9)
            za, zb = zm + (tent_h * 0.88 - 0.035) * t0_, zm + (tent_h * 0.88 - 0.035) * t1_
            y.yuz_yon([A_ + Z * za, B_ + Z * za, C_ + Z * zb, D_ + Z * zb], SH[k % 2], out + Z * 0.12)
        cubuk(y, mid[i] + Z * zm, mid[i].lerp(V(cx, cy), 0.9) + Z * (zm + tent_h * 0.88 - 0.035), 0.008, 'ahsap_koyu')
    y.yuz_yon([p + Z * (zoh - 0.008) for p in ring], 'ahsap_koyu', -Z)
    zt2 = zm + tent_h * 0.88 - 0.035
    rr = R * 0.6 * 0.1
    y.yuz_yon([V(p.x, p.y, zt2) for p in cokgen(c, rr, 4, math.pi / 4)], 'sindira', Z)
    # the lookout: four posts, a rail, a tiny tent
    lw = 0.032
    for sx in (-1, 1):
        for sy in (-1, 1):
            y.prizma((cx + sx * lw, cy + sy * lw), 0.004, zt2 - 0.01, zt2 + 0.05, 'ahsap_koyu', n=4, ust=False)
    kutu_merkez(y, (cx, cy), lw * 2 + 0.012, lw * 2 + 0.012, 0.006, 'ahsap', z0=zt2)
    silme(y, dikdortgen(cx - lw, cx + lw, cy - lw, cy + lw), zt2 + 0.022, 0.005, 0.004, 'ahsap_koyu', 'duz')
    zl = cati_kirma(y, cx - lw, cx + lw, cy - lw, cy + lw, zt2 + 0.05, 0.06, 0.012, 'sindira', 'ahsap_koyu', kalinlik=0.005, ns=3, nr=3, dilim=SH,
                    mahya_en=0.006)
    if bayrak:
        return sancak(y, cx, cy, zl - 0.01, boy=0.18, en=0.1, yuk=0.06, aci=-math.pi / 2 - 0.5, direk_key='ahsap_koyu', kuyruk=True)
    y.prizma((cx, cy), 0.003, zl - 0.005, zl + 0.045, 'demir', n=4)
    levha(y, [V(cx + 0.003, cy, zl + 0.02), V(cx + 0.03, cy, zl + 0.022), V(cx + 0.03, cy, zl + 0.036), V(cx + 0.003, cy, zl + 0.04)], 'demir', -Y)
    return zl + 0.045


y.bolum('Köşe kuleleri')
for p in KOSE:
    kule(y, (p.x, p.y), 0.2, ZV - Z0 + 0.27, 0.3)
y.bolum('Kapı kulesi')
kule(y, (0.0, KOSE[0].y), 0.26, ZV - Z0 + 0.32, 0.34, gecit=True, bayrak=True)
# the ramp up the rampart to the gate, on trestles
y.bolum('Kapı rampası')
RY0, RY1 = -1.13, KOSE[0].y - 0.13
for k in range(9):
    t0_, t1_ = k / 9, (k + 1) / 9
    ya, yb = RY0 + (RY1 - RY0) * t0_, RY0 + (RY1 - RY0) * t1_
    za, zb = Z0 + 0.004 + (ZV - Z0) * t0_, Z0 + 0.004 + (ZV - Z0) * t1_
    kutu3(y, V(0, (ya + yb) / 2, (za + zb) / 2), X, V(0, yb - ya, zb - za), V(0, -(zb - za), yb - ya), 0.12, math.hypot(yb - ya, zb - za) + 0.002, 0.012, 'ahsap' if k % 2 else 'ahsap_acik')
for sx in (-1, 1):
    cubuk(y, V(sx * 0.064, RY0, Z0 + 0.03), V(sx * 0.064, RY1, ZV + 0.03), 0.008, 'ahsap_koyu')
    for k in range(1, 5):
        t = k / 5
        yy, zz = RY0 + (RY1 - RY0) * t, Z0 + (ZV - Z0) * t
        y.prizma((sx * 0.064, yy), 0.005, Z0, zz + 0.03, 'ahsap_koyu', n=4, ust=False)

# ---------------------------------------------------------------- the timber church (Kizhi-like)
y.bolum('Ahşap kilise: gövde ve kollar')
CC = V(-0.05, 0.14)
R1 = 0.17
z1 = kutuk_sekizgen(y, CC, R1, Z0, 0.28, 0.012)
# a stone footing ring
y.prizma(CC, R1 * 1.06, Z0 - 0.01, Z0 + 0.01, 'granit', n=8, kat=math.pi / 8)
# four log arms (prirub) on the cardinal sides with barrel roofs, windows with frames, a porch on the west (front)
for k in range(4):
    a = -math.pi / 2 + k * math.pi / 2
    e = V(math.cos(a), math.sin(a)); s = V(-e.y, e.x)
    ap = R1 * math.cos(math.pi / 8) - 0.01
    L, W = 0.12 if k else 0.17, 0.17
    p0 = V(CC.x, CC.y) + e * ap
    p1 = p0 + e * L
    k4 = [p0 - s * (W / 2), p1 - s * (W / 2), p1 + s * (W / 2), p0 + s * (W / 2)]
    for i in range(3):
        off = 0.012 if i % 2 else 0
        kutuk_duvar2(y, k4[i], k4[i + 1], Z0 + off, Z0 + 0.21 + off, 0.012, 'kutuk', uzanti=0.022)
    if k == 0:
        kutu3(y, p1 + e * 0.008 + Z * (Z0 + 0.065), s, e, Z, 0.07, 0.006, 0.13, 'ahsap_dikey', ('+x', '-x', '+y', '+z'))
        nalichnik(y, p1 + e * 0.011 + Z * Z0, s, 0.074, 0.12, 'beyaz', 'ahsap_dikey', None, 'kemer')
    else:
        nalichnik(y, p1 + e * 0.011 + Z * (Z0 + 0.08), s, 0.04, 0.06, 'beyaz', 'koyu', None, 'ucgen', t=0.005)
    if k == 0:   # windows on the porch's sides
        for u in (-1, 1):
            mm = (p0 + p1) / 2 + s * (u * (W / 2 + 0.011))
            nalichnik(y, mm + Z * (Z0 + 0.08), -e * u, 0.035, 0.055, 'beyaz', 'koyu', None, 'ucgen', t=0.005)
    bochka(y, (p0.x, p0.y), W + 0.01, L + 0.04, Z0 + 0.22 + 0.012, 0.15, a, 'ahsap_acik', 'ahsap_dikey', True, 0.04)
# windows on the octagon's seen faces
for i in range(8):
    if i % 2 == 0: continue
    kk = cokgen(CC, R1, 8, math.pi / 8)
    aa, bb = kk[i], kk[(i + 1) % 8]
    ee = (bb - aa).normalized(); nn = V(ee.y, -ee.x)
    nalichnik(y, (aa + bb) / 2 + nn * 0.011 + Z * (Z0 + 0.22), ee, 0.035, 0.05, 'beyaz', 'koyu', None, 'ucgen', t=0.005)

y.bolum('Ahşap kilise: kat kat sekizgenler ve fıçı çatılar')
# the tiers: each a smaller octagon ringed by barrel gables, each gable carrying an onion
tiers = [(z1, 0.13, 0.17, 8, 0.085), (None, 0.095, 0.14, 4, 0.07), (None, 0.065, 0.11, 0, 0.0)]
zc = z1
# a hipped skirt over the first octagon up to the second
y.yuz_yon([V(p.x, p.y, zc) for p in cokgen(CC, R1 + 0.012, 8, math.pi / 8)], 'ahsap_acik', Z)
for k, (_, r, h, nb, bw) in enumerate(tiers):
    if nb:
        for i in range(nb):
            a = TAU * i / nb - math.pi / 2 + (math.pi / 8 if nb == 8 else math.pi / 4)
            e = V(math.cos(a), math.sin(a))
            c0 = V(CC.x, CC.y) + e * (r * 0.55)
            bochka(y, (c0.x, c0.y), bw, r * 0.95 + (0.06 if k == 0 else 0.045), zc - 0.004, bw * 1.35, a, 'ahsap_acik', 'ahsap_dikey', True, bw * 0.3)
    zc = kutuk_sekizgen(y, CC, r, zc, h, 0.01)
    silme(y, cokgen(CC, r + 0.008, 8, math.pi / 8), zc - 0.012, 0.012, 0.012, 'ahsap_koyu', 'kaba')
    y.yuz_yon([V(p.x, p.y, zc) for p in cokgen(CC, r + 0.02, 8, math.pi / 8)], 'ahsap_acik', Z)
# the crowning onion
zn = boyun(y, CC, 0.04, zc - 0.002, 0.045, 'ahsap_acik', n=14)
zd = kubbe(y, CC, 0.085, zn - 0.002, 'sogan', 0.17, 'ahsap_acik', n=16, pul=PUL, alt=2)
ortodoks_hac(y, CC.x, CC.y, zd - 0.004, 0.1, 'altin')

# ---------------------------------------------------------------- bell tower
y.bolum('Çan kulesi')
BC = V(0.5, 0.42)
zb = kutuk_kutu(y, BC.x - 0.09, BC.x + 0.09, BC.y - 0.09, BC.y + 0.09, Z0, 0.2, 0.011, 'kutuk')
nalichnik(y, V(BC.x - 0.09 - 0.0095, BC.y, Z0 + 0.1), -Y, 0.035, 0.05, 'beyaz', 'koyu', None, 'ucgen', t=0.005)
cati_kirma(y, BC.x - 0.1, BC.x + 0.1, BC.y - 0.1, BC.y + 0.1, zb, 0.06, 0.03, 'sindira', 'ahsap_koyu', kalinlik=0.008, ns=6, nr=3, dilim=SH,
           r_ust=0.55)
y.yuz_yon([V(p.x, p.y, zb + 0.03) for p in dikdortgen(BC.x - 0.06, BC.x + 0.06, BC.y - 0.06, BC.y + 0.06)], 'ahsap', Z)
zo = kutuk_sekizgen(y, BC, 0.07, zb + 0.025, 0.1, 0.01)
# the open belfry: eight posts, a rail, bells
k8 = cokgen(BC, 0.07, 8, math.pi / 8)
for p in k8:
    y.prizma((p.x, p.y), 0.006, zo, zo + 0.11, 'ahsap_koyu', n=5, ust=False)
silme(y, k8, zo + 0.03, 0.006, 0.004, 'ahsap_koyu', 'duz')
y.yuz_yon([V(p.x, p.y, zo + 0.001) for p in k8], 'ahsap', Z)
for i, s_ in enumerate((0.9, 0.6, 0.6)):
    bx = BC.x + (0 if i == 0 else (0.03 if i == 1 else -0.03))
    by = BC.y + (0 if i == 0 else 0.02)
    zt_ = zo + 0.1
    donel(y, (bx, by), [(0.0, zt_ - 0.05 * s_), (0.022 * s_, zt_ - 0.05 * s_), (0.018 * s_, zt_ - 0.035 * s_), (0.012 * s_, zt_ - 0.012 * s_), (0.005 * s_, zt_), (0.0, zt_)], 'bronz', n=10)
cubuk(y, V(BC.x - 0.07, BC.y, zo + 0.1), V(BC.x + 0.07, BC.y, zo + 0.1), 0.008, 'ahsap_koyu')
zs = zo + 0.11
silme(y, cokgen(BC, 0.078, 8, math.pi / 8), zs, 0.012, 0.016, 'ahsap_koyu', 'kaba')
ring = cokgen(BC, 0.1, 8, math.pi / 8)
tp = V(BC.x, BC.y, zs + 0.24)
for i in range(8):
    j = (i + 1) % 8
    y.yuz_yon([ring[i] + Z * (zs + 0.012), ring[j] + Z * (zs + 0.012), tp], SH[i % 2], (ring[i] + ring[j]) / 2 - V(BC.x, BC.y) + Z * 0.2)
y.yuz_yon([p + Z * (zs + 0.012) for p in ring], 'ahsap_koyu', -Z)
zn = boyun(y, BC, 0.013, zs + 0.22, 0.02, 'ahsap_acik', n=10)
zd = kubbe(y, BC, 0.034, zn - 0.002, 'sogan', 0.065, 'ahsap_acik', n=12, pul=PUL, alt=1)
ortodoks_hac(y, BC.x, BC.y, zd - 0.003, 0.055, 'altin')


# ---------------------------------------------------------------- boyar houses
def boyar_evi(y, x0, x1, y0, y1, h, roof_h, tohum=0):
    """a two-storey boyar house: log walls, carved frames on two seen fronts, a gallery band, a steep shingled roof
    with carved boards, a chimney"""
    zw = kutuk_kutu(y, x0, x1, y0, y1, Z0, h, 0.012, 'kutuk')
    for a, b in ((V(x0, y0), V(x1, y0)), (V(x0, y1), V(x0, y0))):
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        n = max(1, int(L / 0.1))
        for k in range(n):
            o = a + e * (L * (k + 0.5) / n) + nn * 0.0105
            nalichnik(y, o + Z * (Z0 + h * 0.62), e, 0.04, 0.06, 'beyaz', 'koyu', 'boya_kirmizi', 'ucgen' if k % 2 else 'kemer', t=0.006)
            if k % 2 == 0:
                nalichnik(y, o + Z * (Z0 + h * 0.18), e, 0.035, 0.045, 'beyaz', 'koyu', None, None, t=0.005)
        oymali_sacak(y, a + nn * 0.016 + Z * (Z0 + h * 0.5), b + nn * 0.016 + Z * (Z0 + h * 0.5), nn, 'beyaz', 0.014, max(3, int(L / 0.035)), 0.0)
        kutu3(y, (a + b) / 2 + nn * 0.014 + Z * (Z0 + h * 0.5 + 0.008), e, nn, Z, L, 0.01, 0.016, 'ahsap_koyu', ('+x', '-x', '+y', '+z', '-z'))
    zr = ahsap_cati(y, x0 - 0.012, x1 + 0.012, y0 - 0.012, y1 + 0.012, zw, roof_h, sacak=0.03, uc_sacak=0.035, nr=8, ns=6)
    cx, cy = (x0 + x1) / 2 + 0.04, (y0 + y1) / 2
    kutu_merkez(y, (cx, cy), 0.04, 0.04, zr - zw + 0.03 - roof_h * 0.4, 'tugla', z0=zw + roof_h * 0.4)
    return zr


y.bolum('Boyar evleri')
boyar_evi(y, -0.72, -0.44, 0.4, 0.74, 0.24, 0.26, 1)
boyar_evi(y, 0.36, 0.7, -0.6, -0.36, 0.22, 0.22, 2)
# a little stair porch on the first house's front
merdiven(y, (-0.62, 0.4 - 0.13), math.pi / 2, 0.06, Z0, Z0 + 0.1, n=5, key='ahsap', yanlik='ahsap_koyu')

# ---------------------------------------------------------------- yard
y.bolum('Avlu: kuyu, saman, insanlar')
WC = V(0.3, -0.12)
for i in range(4):
    kk = dikdortgen(WC.x - 0.04, WC.x + 0.04, WC.y - 0.04, WC.y + 0.04)
    kutuk_duvar2(y, kk[i], kk[(i + 1) % 4], Z0 + (0.009 if i % 2 else 0), Z0 + 0.07 + (0.009 if i % 2 else 0), 0.009, 'kutuk', uzanti=0.014)
y.yuz_yon([V(p.x, p.y, Z0 + 0.03) for p in dikdortgen(WC.x - 0.03, WC.x + 0.03, WC.y - 0.03, WC.y + 0.03)], 'su', Z)
for sx in (-1, 1):
    y.prizma((WC.x + sx * 0.05, WC.y), 0.006, Z0, Z0 + 0.15, 'ahsap_koyu', n=5)
cati_besik(y, WC.x - 0.065, WC.x + 0.065, WC.y - 0.05, WC.y + 0.05, Z0 + 0.15, 0.05, 0.012, 'sindira', 'ahsap_koyu', kalinlik=0.005,
           ucluk_key='ahsap_dikey', uc_sacak=0.01, nr=2, ns=3, dilim=SH)
for i, (x, yy) in enumerate(((0.62, 0.72), (0.76, 0.6), (-0.72, -0.5))):
    kar_yigin(y, x, yy, Z0, 0.07, 0.12, 'saz', n=10, tohum=i)
    y.prizma((x, yy), 0.004, Z0 + 0.1, Z0 + 0.16, 'ahsap_koyu', n=4)
for i, (x, yy, k, a) in enumerate(((0.05, -0.45, 'boya_kirmizi', 1.0), (-0.1, -0.52, 'kutuk', 2.0), (0.15, -0.6, 'ahsap', 0.3),
                                   (0.0, -0.95, 'granit', 1.6), (-0.35, -0.3, 'boya_yesil', 0.8), (0.45, -0.18, 'kobalt', 2.4))):
    insan(y, x, yy, Z0 if yy > -0.82 else Z0, k, s=1.7, aci=a, sapka='ahsap_koyu' if i % 2 else 'boya_kirmizi')
for i, (x, yy, b) in enumerate(((-0.55, -0.4, 0.28), (0.72, 0.12, 0.26), (-1.05, -1.0, 0.3), (1.05, -0.95, 0.26), (1.06, 0.4, 0.3), (-1.06, 0.3, 0.28))):
    kayin(y, x, yy, Z0, b, tohum=i)

calistir(y, 'lm_ahsapkremlin')
