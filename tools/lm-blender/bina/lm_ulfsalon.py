# Valhalla (lm_ulfsalon): Odin's hall of the slain as a stylised, game-like great hall on a stone terrace: a towering
# gable roof thatched with golden shields, walls of spear shafts, a long row of glowing doors (the "540 doors") and a
# great porch, gilded barge boards ending in dragon heads, the goat Heiðrún and the stag Eikþyrnir standing on the
# roof ridge; before it the golden tree Glasir, the wolves Geri and Freki by the steps, fire bowls and banners.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from doku import MALZEME

# a warmer, more saturated gold for this hall only (the shared 'altin' reads pale beige on the shield roof)
MALZEME.setdefault('altin_v', ('duz', (0.97, 0.66, 0.13), {'leke': 0.04}))
MALZEME.setdefault('altin_v2', ('duz', (0.88, 0.55, 0.10), {'leke': 0.04}))
MALZEME.setdefault('bronz_v', ('duz', (0.66, 0.36, 0.12), {'leke': 0.04}))
AL, AL2, BR = 'altin_v', 'altin_v2', 'bronz_v'

y = Yapi()
ZP = 0.07            # terrace top
HX, HY0, HY1 = 0.78, -0.16, 0.58     # hall: half length, front and back wall lines
HC = (HY0 + HY1) / 2
ZS = ZP + 0.04       # socle top
ZW = ZS + 0.27       # wall top
RH = 0.74            # roof height
SAC = 0.08           # eaves


# ---------------------------------------------------------------- helpers
def levha(pts, key, yon, kil=0.002):
    """a thin sheet seen from both sides: the face toward yon, its twin kil behind, and the rims all round"""
    pts = [V(*p) for p in pts]; yon = V(*yon).normalized()
    iki_yuzlu(y, pts, key, yon, kil)
    c = sum(pts, V(0, 0, 0)) / len(pts) - yon * (kil / 2)
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        if (b - a).length < 1e-7: continue
        yuz_dis(y, [a, b, b - yon * kil, a - yon * kil], key, c)


def ejder(p, d, s=1.0, key=AL):
    """a carved dragon head: a neck curving out (d: outward, horizontal) and up, open jaws, a curled crest"""
    d = V(d[0], d[1]).normalized() * s
    up = Z * s
    neck = [p - d * 0.01, p + d * 0.018 + up * 0.016, p + d * 0.03 + up * 0.042, p + d * 0.026 + up * 0.068]
    boru(y, neck, 0.012 * s, key, n=8, r_son=0.01 * s)
    hp = neck[-1]
    kure(y, hp, 0.012 * s, key, n=8, kat=4)
    boru(y, [hp, hp + d * 0.026 + up * 0.004, hp + d * 0.05 + up * 0.002], 0.009 * s, key, n=6, r_son=0.005 * s)
    boru(y, [hp - up * 0.006, hp + d * 0.02 - up * 0.012, hp + d * 0.04 - up * 0.02], 0.005 * s, key, n=5, r_son=0.003 * s)
    boru(y, [hp + d * 0.048, hp + d * 0.044 - up * 0.012], 0.0028 * s, 'boya_kirmizi', n=4, r_son=0.002 * s)
    boru(y, [hp - d * 0.006 + up * 0.008, hp - d * 0.018 + up * 0.026, hp - d * 0.034 + up * 0.028, hp - d * 0.038 + up * 0.016],
         0.005 * s, key, n=5, r_son=0.002 * s)
    w = V(-d.y, d.x).normalized()
    for sd in (-1, 1):
        kure(y, hp + d * 0.012 + up * 0.008 + w * (sd * 0.008 * s), 0.0034 * s, 'koyu', n=6, kat=3)


def kalkan(c, ex, ey, n, r, key, kal=0.007, gobek=AL, arka=False, kenar=None, m=10):
    """a round shield lying on a surface: face (m-gon) toward n inside a metal rim band (kenar: its key, so each
    shield reads as one at a distance), the rim down to the surface, a pyramidal boss"""
    kenar = kenar or key
    ring = [c + (ex * math.cos(TAU * (k + 0.5) / m) + ey * math.sin(TAU * (k + 0.5) / m)) * r for k in range(m)]
    top = [p + n * kal for p in ring]
    inn = [c + n * kal + (p - c) * 0.8 for p in ring]
    y.yuz_yon(inn, key, n)
    for k in range(m):
        j = (k + 1) % m
        y.yuz_yon([top[k], top[j], inn[j], inn[k]], kenar, n)
    if arka:   # (a shield standing free: its wooden back)
        y.yuz_yon(ring, 'ahsap', -n)
    for k in range(m):
        j = (k + 1) % m
        yuz_dis(y, [ring[k], ring[j], top[j], top[k]], kenar, c)
    b = c + n * kal
    bs = [b + (ex * math.cos(TAU * k / 4) + ey * math.sin(TAU * k / 4)) * r * 0.28 + n * 0.0005 for k in range(4)]
    tip = b + n * r * 0.32
    for k in range(4):
        yuz_dis(y, [bs[k], bs[(k + 1) % 4], tip], gobek, b - n * 0.01)


def elips(c, rx, rz, key, n=12, kat=6):
    pr = [(rx * math.sin(math.pi * k / kat), c[2] - rz * math.cos(math.pi * k / kat)) for k in range(kat + 1)]
    pr[0] = (0.0, pr[0][1]); pr[-1] = (0.0, pr[-1][1])
    donel(y, c, pr, key, n=n)


def hayvan(konum, aci, tur, key=AL, olcek=1.0, kaide=True):
    """a statue of a beast on four legs, facing local +x: tur 'keci' (goat: back-swept horns, beard), 'geyik' (stag:
    branching antlers), 'kurt' (a sitting wolf)"""
    with parca(y, konum, aci, olcek):
        if kaide:
            kutu_merkez(y, (0.0, 0.0), 0.2 if tur != 'kurt' else 0.12, 0.08, 0.03, 'granit_koyu' if tur == 'kurt' else key, z0=-0.03)
        if tur == 'kurt':   # sitting: haunches low, forelegs straight, head up
            boru(y, [V(-0.03, 0, 0.035), V(0.0, 0, 0.07), V(0.022, 0, 0.1)], 0.028, key, n=10, r_son=0.022)
            kure(y, (-0.032, 0, 0.034), 0.034, key, n=10, kat=5)
            for s in (-1, 1):
                cubuk(y, V(0.026, s * 0.014, 0.085), V(0.034, s * 0.014, 0.0), 0.012, key)
                kure(y, (-0.03, s * 0.026, 0.02), 0.022, key, n=8, kat=4)
            hp = V(0.04, 0, 0.13)
            boru(y, [V(0.022, 0, 0.1), hp], 0.02, key, n=8, r_son=0.017)
            kure(y, hp, 0.022, key, n=10, kat=5)
            boru(y, [hp, hp + V(0.04, 0, -0.006)], 0.012, key, n=6, r_son=0.007)
            for s in (-1, 1):
                boru(y, [hp + V(-0.006, s * 0.012, 0.012), hp + V(-0.01, s * 0.014, 0.036)], 0.007, key, n=4, r_son=0.001)
            boru(y, [V(-0.06, 0, 0.012), V(-0.085, 0.02, 0.004), V(-0.1, 0.05, 0.006)], 0.008, key, n=5, r_son=0.004)
            return
        zb = 0.11
        boru(y, [V(-0.06, 0, zb), V(0.0, 0, zb + 0.004), V(0.055, 0, zb + 0.01)], 0.033, key, n=10, r_son=0.03)
        kure(y, (-0.06, 0, zb), 0.034, key, n=10, kat=5)
        kure(y, (0.055, 0, zb + 0.01), 0.031, key, n=10, kat=5)
        for (lx, s) in ((-0.055, -1), (-0.055, 1), (0.05, -1), (0.05, 1)):   # legs with a knee
            k = V(lx + (0.01 if lx < 0 else -0.004), s * 0.018, 0.05)
            boru(y, [V(lx, s * 0.018, zb - 0.01), k, V(lx + (-0.006 if lx < 0 else 0.004), s * 0.018, 0.0)], 0.009, key, n=6, r_son=0.006)
        nb = V(0.07, 0, zb + 0.02)
        hp = V(0.1, 0, zb + 0.085) if tur == 'geyik' else V(0.1, 0, zb + 0.07)
        boru(y, [nb, nb.lerp(hp, 0.5) + V(0.0, 0, 0.01), hp], 0.018, key, n=8, r_son=0.014)
        kure(y, hp, 0.019, key, n=8, kat=4)
        boru(y, [hp, hp + V(0.036, 0, -0.022)], 0.012, key, n=6, r_son=0.007)       # muzzle
        for s in (-1, 1):   # ears
            boru(y, [hp + V(-0.004, s * 0.014, 0.004), hp + V(-0.012, s * 0.034, 0.012)], 0.006, key, n=4, r_son=0.001)
        boru(y, [V(-0.09, 0, zb + 0.01), V(-0.1, 0, zb + 0.03)], 0.007, key, n=4, r_son=0.003)   # tail
        if tur == 'keci':
            for s in (-1, 1):
                boru(y, [hp + V(0.0, s * 0.008, 0.014), hp + V(-0.008, s * 0.012, 0.04), hp + V(-0.03, s * 0.016, 0.052), hp + V(-0.045, s * 0.016, 0.04)],
                     0.006, key, n=5, r_son=0.002)
            boru(y, [hp + V(0.026, 0, -0.03), hp + V(0.022, 0, -0.055)], 0.006, key, n=4, r_son=0.002)   # beard
        else:
            for s in (-1, 1):
                a0 = hp + V(-0.004, s * 0.01, 0.014)
                m1 = a0 + V(-0.012, s * 0.03, 0.05)
                m2 = m1 + V(-0.02, s * 0.02, 0.05)
                m3 = m2 + V(-0.012, s * 0.006, 0.045)
                boru(y, [a0, m1, m2, m3], 0.0055, key, n=5, r_son=0.0025)
                for p, d in ((m1, V(0.03, s * 0.004, 0.03)), (m2, V(0.026, s * 0.01, 0.034)), (m2.lerp(m3, 0.5), V(-0.02, s * 0.016, 0.03))):
                    boru(y, [p, p + d], 0.004, key, n=4, r_son=0.0015)


# ---------------------------------------------------------------- terrace
y.bolum('Taş teras, basamaklar')
TX0, TX1, TY0, TY1 = -1.12, 1.12, -0.98, 0.9
zemin(y, TX0, TX1, TY0, TY1, ZP, 'granit_koyu', 'zemin', basamak=(('on', 0.56),), n_basamak=3)
# a raised kerb of rough stones round the edge, with gaps at the front stairs
for k in range(46):
    t = k / 46
    per = 2 * (TX1 - TX0) + 2 * (TY1 - TY0)
    s = t * per
    if s < TX1 - TX0: p, a = V(TX0 + s, TY0 + 0.025), 0.0
    elif s < TX1 - TX0 + TY1 - TY0: p, a = V(TX1 - 0.025, TY0 + s - (TX1 - TX0)), math.pi / 2
    elif s < 2 * (TX1 - TX0) + TY1 - TY0: p, a = V(TX1 - (s - (TX1 - TX0) - (TY1 - TY0)), TY1 - 0.025), 0.0
    else: p, a = V(TX0 + 0.025, TY1 - (s - 2 * (TX1 - TX0) - (TY1 - TY0))), math.pi / 2
    if abs(p.x) < 0.34 and p.y < TY0 + 0.1: continue
    kutu_merkez(y, (p.x, p.y), 0.034, 0.024, 0.018 + 0.006 * (k % 2), 'granit' if k % 3 else 'granit_koyu', z0=ZP, aci=a + 0.15 * (k % 3 - 1))
# the processional way to the porch
for k in range(9):
    yy = TY0 + 0.06 + k * 0.08
    if yy > HY0 - 0.2: break
    y.yuz_yon([V(-0.16, yy, ZP + 0.003), V(0.16, yy, ZP + 0.003), V(0.16, yy + 0.07, ZP + 0.003), V(-0.16, yy + 0.07, ZP + 0.003)], 'tas_acik' if k % 2 else 'tas', Z)

# ---------------------------------------------------------------- the hall
y.bolum('Salon: taş taban, kalkan ve mızrak duvarları, kapı dizisi')
kh = dikdortgen(-HX, HX, HY0, HY1)
kutu(y, V(-HX - 0.03, HY0 - 0.03, ZP), X, 2 * HX + 0.06, HY1 - HY0 + 0.06, ZS - ZP, 'granit', 'onarkasagsolust')
silme(y, disa(kh, 0.03), ZS - 0.012, 0.012, 0.008, 'tas_acik', 'kaba')
KAPI = ('ahsap_koyu', 'ahsap_koyu', AL, 'boya_sari')    # wall, reveal, sill, the glowing inside


def mizrak(p, nn, z0, z1):
    """a spear standing against the wall: shaft, a gilded collar, a steel blade"""
    q = p + nn * 0.007
    y.prizma((q.x, q.y), 0.0055, z0, z1, 'ahsap', n=5, ust=False)
    y.prizma((q.x, q.y), 0.0075, z1 - 0.008, z1, AL, n=5)
    donel(y, (q.x, q.y), [(0.0075, z1), (0.009, z1 + 0.012), (0.0, z1 + 0.04)], 'demir', n=4)


NB = 11
for i in range(4):
    a, b = kh[i], kh[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    L = (b - a).length
    uzun = i % 2 == 0
    nb = NB if uzun else 5
    for j in range(nb):
        p, q = a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb)
        ana = (i == 0 and j == nb // 2)
        if uzun and j % 2 == 1 and not ana:
            y.kemerli(p, q, ZS, ZW - ZS - 0.03, KAPI, v0=0.0, en=0.62, ust=0.03, derin=0.03, k_say=8, cerceve=(0.008, [AL, BR]))
            duz_duvar(y, p, q, ZW - 0.03, ZW, 'ahsap_koyu')
            # double doors standing open: two gilded leaves turned out
            W_ = (q - p).length
            for s in (-1, 1):
                h0 = p.lerp(q, 0.5 + s * 0.31)
                levha([h0 + Z * ZS, h0 + Z * (ZS + 0.17) , h0 + nn * 0.05 + Z * (ZS + 0.17), h0 + nn * 0.05 + Z * ZS], BR, e * s, 0.004)
        elif ana:
            duz_duvar(y, p, q, ZS, ZW, 'ahsap_koyu')
        else:
            duz_duvar(y, p, q, ZS, ZW, 'ahsap_koyu')
            # walls of spear shafts
            m = 5
            for k in range(m + 1):
                mizrak(p.lerp(q, k / m), nn, ZS, ZW - 0.05)
            kutu(y, p + nn * 0.004 + Z * (ZS + 0.06), e, (q - p).length, 0.012, 0.016, AL, 'onust')   # gilded rails tying them
            kutu(y, p + nn * 0.004 + Z * (ZW - 0.1), e, (q - p).length, 0.012, 0.016, AL, 'onust')
    # a hung shield over every second bay, a beam under the eaves
    kutu(y, a + nn * 0.004 + Z * (ZW - 0.028) - e * 0.01, e, L + 0.02, 0.014, 0.028, 'ahsap', 'onust')
    for j in range(0, nb, 2):
        c = a.lerp(b, (j + 0.5) / nb) + nn * 0.012 + Z * (ZW - 0.06)
        if uzun and j == nb // 2 + 1: continue
        kalkan(c, e, Z, nn, 0.026, 'boya_kirmizi' if (j // 2) % 2 else AL)
for p in kh:   # corner posts carved with spiral bands
    y.prizma((p.x, p.y), 0.03, ZS, ZW + 0.01, 'ahsap_koyu', n=8)
    for zz in (ZS + 0.05, ZS + 0.13, ZS + 0.21):
        y.prizma((p.x, p.y), 0.034, zz, zz + 0.016, AL, n=8)

y.bolum('Salon: kalkan kaplı yüksek çatı')
ZR = cati_besik(y, -HX, HX, HY0, HY1, ZW, RH, SAC, BR, AL, kalinlik=0.016, ucluk_key='ahsap_koyu', alinlik_key=AL, nr=10, ns=14,
                mahya_en=0.03)
# the golden shields, overlapping in courses like scales
b_ = (HY1 - HY0) / 2 + SAC
SL = math.sqrt(b_ * b_ + RH * RH)
for sy in (-1, 1):
    up = V(0, -sy * b_ / SL, RH / SL)                # up the slope
    nrm = V(0, sy * RH / SL, b_ / SL)                # out of the roof
    RK = 0.046                                       # shield radius
    TL = 0.24                                        # tilt: the lower rim stands off the roof (overlapping scales)
    ey_t = up * math.cos(TL) - nrm * math.sin(TL)
    n_t = nrm * math.cos(TL) + up * math.sin(TL)
    nrow = 11
    for r in range(nrow):
        d = 0.05 + (SL - 0.09) * r / (nrow - 1)      # distance up the slope from the eave
        base = V(0, HC + sy * b_, ZW) + up * d
        ncol = 19
        for c_ in range(ncol + 1):
            x = -HX - SAC + RK + 0.006 + (2 * HX + 2 * SAC - 2 * RK - 0.012) * (c_ + (0.5 if r % 2 else 0.0)) / ncol
            if abs(x) > HX + SAC - RK - 0.005: continue
            cc = base + X * x + nrm * (RK * math.sin(TL) + 0.002 + 0.003 * (r % 2))
            h_ = (c_ * 7 + r * 5) % 13
            key = BR if h_ in (0, 6) else (AL2 if h_ % 3 == 1 else AL)
            kalkan(cc, X, ey_t, n_t, RK, key, kal=0.007, gobek=BR if key != BR else AL, kenar=BR if key != BR else AL2)

y.bolum('Salon: alınlıklar, ejder başları')
for sx in (-1, 1):
    xg = sx * (HX + SAC)
    # gilded barge boards crossing at the top, ending in dragon heads
    for sy in (-1, 1):
        p0 = V(xg + sx * 0.008, HC + sy * b_, ZW - 0.006)
        p1 = V(xg + sx * 0.008, HC, ZR + 0.01)
        cubuk(y, p0, p1 + (p1 - p0).normalized() * 0.08, 0.028, AL, 0.014)
    ejder(V(xg + sx * 0.012, HC, ZR + 0.05), V(sx, 0), 2.0)
    # a great gilded sun disc and a wolf's head (the wolf over the west door) on the gable
    xw = sx * HX + sx * 0.004
    for k, (r, key) in enumerate(((0.1, AL), (0.075, BR), (0.045, AL))):
        ring = [V(xw + sx * 0.004 * k, HC + r * math.cos(TAU * i / 16), ZW + 0.3 + r * math.sin(TAU * i / 16)) for i in range(16)]
        y.yuz_yon(ring, key, V(sx, 0))
        for i in range(16):
            q0, q1 = ring[i], ring[(i + 1) % 16]
            yuz_dis(y, [q0, q1, q1 - V(sx * 0.004, 0), q0 - V(sx * 0.004, 0)], key, V(xw - sx * 0.01, HC, ZW + 0.3))
    for i in range(12):   # rays
        a = TAU * i / 12
        d = V(0, math.cos(a), math.sin(a))
        cubuk(y, V(xw, HC, ZW + 0.3) + d * 0.1, V(xw, HC, ZW + 0.3) + d * 0.15, 0.012, AL, 0.008)
    # battens over the gable's boards (the dark triangle read as one flat sheet)
    hw = (HY1 - HY0) / 2
    for j in range(1, 14):
        yy = HC - hw + 2 * hw * j / 14
        h = (ZR - ZW) * (1 - (abs(yy - HC) + 0.008) / hw) - 0.01
        if h < 0.02: continue
        if sx > 0:
            kutu(y, V(HX + 0.0018, yy - 0.005, ZW), Y, 0.01, 0.0018, h, 'ahsap', 'onsagsolust')
        else:
            kutu(y, V(-HX - 0.0018, yy + 0.005, ZW), -Y, 0.01, 0.0018, h, 'ahsap', 'onsagsolust')
    # crossed spears on the gable below the disc
    for s in (-1, 1):
        cubuk(y, V(xw + sx * 0.01, HC - s * 0.2, ZW + 0.03), V(xw + sx * 0.01, HC + s * 0.14, ZW + 0.18), 0.008, 'ahsap')

y.bolum('Salon: büyük giriş sundurması ve kartal')
PX = 0.14
PY0 = HY0 - 0.2
for sx in (-1, 1):
    for yy in (PY0 + 0.02, HY0 - 0.02):
        y.prizma((sx * PX, yy), 0.016, ZS, ZW - 0.02, 'ahsap_koyu', n=8)
        for zz in (ZS + 0.04, ZS + 0.12, ZS + 0.2):
            y.prizma((sx * PX, yy), 0.019, zz, zz + 0.012, AL, n=8)
kutu(y, V(-PX - 0.04, PY0 - 0.02, ZP), X, 2 * PX + 0.08, HY0 - PY0 + 0.02, ZS - ZP, 'granit', 'onsagsolust')
merdiven(y, (0, PY0 - 0.02 - 0.06), math.pi / 2, 2 * PX + 0.04, ZP, ZS, n=2, d=0.03, key='granit')
# the great doors (shut, gilded with bands)
zp = cati_besik(y, -PX - 0.02, PX + 0.02, PY0, HY0 + 0.2, ZW - 0.02, 0.24, 0.03, BR, AL, ucluk_key='ahsap_koyu', alinlik_key=AL, nr=6, ns=6)
# gilded barge boards crossing over the porch gable (as on the hall), the dragon head rising from their crossing
for sx in (-1, 1):
    p0 = V(sx * (PX + 0.05), PY0 - 0.038, ZW - 0.028)
    p1 = V(0.0, PY0 - 0.038, zp + 0.006)
    cubuk(y, p0, p1 + (p1 - p0).normalized() * 0.05, 0.02, AL, 0.012)
ejder(V(0, PY0 - 0.04, zp + 0.03), -Y, 1.4)
for s in (-1, 1):
    levha([V(s * 0.005, HY0 - 0.004, ZS), V(s * (PX - 0.03), HY0 - 0.004, ZS), V(s * (PX - 0.03), HY0 - 0.004, ZS + 0.21), V(s * 0.005, HY0 - 0.004, ZS + 0.21)],
          BR, -Y, 0.003)
    for zz in (0.05, 0.11, 0.17):
        cubuk(y, V(s * 0.012, HY0 - 0.009, ZS + zz), V(s * (PX - 0.036), HY0 - 0.009, ZS + zz), 0.01, AL, 0.004)
    kure(y, (s * 0.022, HY0 - 0.012, ZS + 0.11), 0.008, AL, n=8, kat=4)
# the eagle over the door: a gilded bird with spread wings on the porch gable
ez = ZW + 0.06
kure(y, (0, PY0 - 0.02, ez + 0.02), 0.022, AL, n=8, kat=4)
kure(y, (0, PY0 - 0.03, ez + 0.055), 0.014, AL, n=8, kat=4)
boru(y, [V(0, PY0 - 0.04, ez + 0.055), V(0, PY0 - 0.058, ez + 0.048)], 0.006, AL, n=5, r_son=0.002)
for s in (-1, 1):
    wing = [V(s * 0.012, PY0 - 0.02, ez + 0.03), V(s * 0.07, PY0 - 0.018, ez + 0.08), V(s * 0.12, PY0 - 0.016, ez + 0.085), V(s * 0.1, PY0 - 0.016, ez + 0.06),
            V(s * 0.11, PY0 - 0.016, ez + 0.045), V(s * 0.075, PY0 - 0.018, ez + 0.035), V(s * 0.08, PY0 - 0.018, ez + 0.015), V(s * 0.02, PY0 - 0.02, ez + 0.005)]
    levha(wing, AL, -Y, 0.006)

y.bolum('Çatıda Heiðrún ve Eikþyrnir')
hayvan((-0.34, HC, ZR - 0.005), 0.0, 'keci', olcek=1.35)
hayvan((0.34, HC, ZR - 0.005), math.pi, 'geyik', olcek=1.35)

# ---------------------------------------------------------------- Glasir, wolves, fire bowls, banners
y.bolum('Glasir altın ağacı')
GT = (-0.66, -0.5)
donel(y, GT, [(0.12, ZP), (0.12, ZP + 0.03), (0.105, ZP + 0.045), (0.0, ZP + 0.045)], 'granit', n=16)
kok = V(GT[0], GT[1], ZP + 0.04)
boru(y, [kok, kok + V(0.01, 0.0, 0.14), kok + V(-0.01, 0.01, 0.28), kok + V(0.0, 0.0, 0.36)], 0.03, AL, n=10, r_son=0.014)
for i in range(5):
    a = TAU * i / 5 + 0.4
    d = V(math.cos(a), math.sin(a))
    boru(y, [kok + d * 0.02, kok + d * 0.07 - Z * 0.03], 0.012, AL, n=5, r_son=0.004)
# the crown: many small clumps of golden leaves on spreading limbs, in two shades
for k in range(22):
    a = TAU * k * 0.618
    rr = 0.05 + 0.13 * ((k * 7) % 11) / 10
    dz = 0.3 + 0.32 * ((k * 5) % 9) / 8 - 0.12 * (rr / 0.18) ** 2
    c = V(GT[0] + rr * math.cos(a), GT[1] + rr * math.sin(a), ZP + dz)
    boru(y, [V(GT[0], GT[1], ZP + min(0.34, dz - 0.04)), c - Z * 0.02], 0.007, AL, n=5, r_son=0.003)
    r = 0.07 - 0.015 * (k % 3)
    elips(c, r, r * 0.7, AL if k % 3 else AL2, n=10, kat=5)
# fallen golden leaves round its foot
for k in range(14):
    a = TAU * k / 14 + 0.2
    rr = 0.15 + 0.04 * (k % 3)
    p = V(GT[0] + rr * math.cos(a), GT[1] + rr * math.sin(a), ZP + 0.002)
    y.yuz_yon([p + V(-0.01, -0.006, 0), p + V(0.01, -0.006, 0), p + V(0.006, 0.008, 0), p + V(-0.008, 0.006, 0)], AL, Z)

y.bolum('Geri ve Freki, ateş kapları, silah rafı, sancaklar')
hayvan((-0.36, TY0 + 0.12, ZP + 0.03), math.pi / 2, 'kurt', key=BR, olcek=1.3)
hayvan((0.36, TY0 + 0.12, ZP + 0.03), math.pi / 2, 'kurt', key=BR, olcek=1.3)


def ates(x, yy):
    donel(y, (x, yy), [(0.03, ZP), (0.02, ZP + 0.02), (0.014, ZP + 0.07), (0.04, ZP + 0.1), (0.045, ZP + 0.115), (0.0, ZP + 0.115)], 'demir', n=10)
    donel(y, (x, yy), [(0.0, ZP + 0.112), (0.04, ZP + 0.114), (0.036, ZP + 0.13), (0.02, ZP + 0.15), (0.0, ZP + 0.165)], 'boya_kirmizi', n=10)
    for k in range(3):   # flickering tongues of flame
        a = TAU * k / 3 + 0.4
        c = (x + 0.012 * math.cos(a), yy + 0.012 * math.sin(a))
        hh = 0.07 + 0.02 * k
        donel(y, c, [(0.0, ZP + 0.13), (0.014, ZP + 0.135), (0.01, ZP + 0.13 + hh * 0.5), (0.0, ZP + 0.13 + hh)], 'boya_sari', n=6)


for x in (-0.22, 0.22):
    for yy in (TY0 + 0.3, TY0 + 0.55):
        ates(x, yy)
# weapon racks with shields by the hall's corners
for sx in (-1, 1):
    with parca(y, (sx * 0.62, HY0 - 0.2, ZP), 0.0):
        for x in (-0.12, 0.12):
            cubuk(y, V(x, 0, 0), V(x, 0, 0.1), 0.012, 'ahsap_koyu')
        cubuk(y, V(-0.13, 0, 0.09), V(0.13, 0, 0.09), 0.012, 'ahsap_koyu')
        for k in range(5):
            x = -0.09 + 0.045 * k
            kalkan(V(x, -0.008, 0.055), X, Z, -Y, 0.022, ['boya_kirmizi', AL, 'beyaz', 'boya_sari', 'boya_yesil'][k], kal=0.005, arka=True)
            cubuk(y, V(x + 0.02, 0.01, 0.0), V(x + 0.02, 0.01, 0.15), 0.005, 'ahsap')
            donel(y, (x + 0.02, 0.01), [(0.0045, 0.15), (0.006, 0.16), (0.0, 0.185)], 'demir', n=4)
# rows of standing stones / spears along the terrace sides
for sx in (-1, 1):
    for k in range(6):
        yy = HY0 + 0.05 + k * 0.13
        p = V(sx * (HX + 0.2), yy)
        kutu_merkez(y, (p.x, p.y), 0.04, 0.03, 0.12 + 0.02 * (k % 2), 'granit', z0=ZP - 0.003, aci=0.1 * (k % 3))
        kalkan(V(p.x + sx * 0.0155, p.y, ZP + 0.08), Y, Z, V(sx, 0, 0), 0.018, AL if k % 2 else 'boya_kirmizi', kal=0.004)
y.bolum('Eldhrímnir kazanı ve bal şarabı fıçıları')
KZ = (0.66, -0.6)
for k in range(3):   # the tripod
    a = TAU * k / 3 + 0.3
    cubuk(y, V(KZ[0] + 0.1 * math.cos(a), KZ[1] + 0.1 * math.sin(a), ZP), V(KZ[0], KZ[1], ZP + 0.2), 0.012, 'demir', 0.012)
boru(y, [V(KZ[0], KZ[1], ZP + 0.2), V(KZ[0], KZ[1], ZP + 0.16)], 0.003, 'demir', n=4)
for k in range(8):   # the fire under it: logs and flames
    a = TAU * k / 8
    cubuk(y, V(KZ[0], KZ[1], ZP + 0.006), V(KZ[0] + 0.06 * math.cos(a), KZ[1] + 0.06 * math.sin(a), ZP + 0.004), 0.012, 'kutuk', 0.01)
for k in range(5):
    a = TAU * k / 5
    c = (KZ[0] + 0.022 * math.cos(a), KZ[1] + 0.022 * math.sin(a))
    donel(y, c, [(0.0, ZP + 0.01), (0.016, ZP + 0.014), (0.011, ZP + 0.04), (0.0, ZP + 0.07 + 0.01 * (k % 2))], 'boya_sari' if k % 2 else 'boya_kirmizi', n=6)
# the cauldron: an iron bowl with a rolled lip, broth inside, two ring handles
donel(y, KZ, [(0.0, ZP + 0.06), (0.04, ZP + 0.064), (0.065, ZP + 0.09), (0.072, ZP + 0.12), (0.068, ZP + 0.145), (0.074, ZP + 0.15),
              (0.0705, ZP + 0.153)], 'demir', n=18)
y.yuz_yon([V(p.x, p.y, ZP + 0.1525) for p in cokgen(KZ, 0.0706, 18)], 'kerpic_koyu', Z)
for s in (-1, 1):
    boru(y, [V(KZ[0] + s * 0.07, KZ[1], ZP + 0.14), V(KZ[0] + s * 0.088, KZ[1], ZP + 0.13), V(KZ[0] + s * 0.086, KZ[1], ZP + 0.112),
             V(KZ[0] + s * 0.071, KZ[1], ZP + 0.11)], 0.0035, 'demir', n=4, kapat=False)
for k, (dx, dy) in enumerate(((0.16, 0.06), (0.19, -0.02), (0.15, -0.1))):   # mead barrels with iron hoops
    c = (KZ[0] + dx - 0.05, KZ[1] + dy)
    donel(y, c, [(0.0, ZP), (0.03, ZP), (0.036, ZP + 0.035), (0.03, ZP + 0.07), (0.0, ZP + 0.07)], 'ahsap', n=12)
    for zz in (0.012, 0.058):
        donel(y, c, [(0.0312, ZP + zz), (0.0342, ZP + zz + 0.001), (0.0342, ZP + zz + 0.005), (0.0312, ZP + zz + 0.006)], 'demir', n=12)

for sx in (-1, 1):
    sancak(y, sx * 0.62, TY0 + 0.16, ZP, boy=0.55, en=0.17, yuk=0.1, aci=math.pi / 2 + sx * 0.4, kuyruk=True)

calistir(y, 'lm_ulfsalon')
