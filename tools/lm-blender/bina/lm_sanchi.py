# Great Stupa at Sanchi (lm_sanchi): the hemispherical anda on its raised drum (medhi) with the upper walkway railing
# and the double stair on the south, the harmika and the three-tiered chattra on top; the ground railing (vedika) with
# the four carved toranas (two posts, elephant capitals, three scrolled architraves, yakshi brackets, wheel and
# triratna on top); Ashoka's lion pillar, Stupa 3, the Gupta Temple 17, the apsidal Temple 18's pillars, a monastery.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from hint_ortak import *

y = Yapi()
H0 = 0.05                       # the hill terrace's top
C = (0.0, 0.06)                 # the Great Stupa's centre
TAS, TAS2, TAS3 = 'kum', 'kum_koyu', 'kum_acik'

# ---------------- the terrace ----------------
y.bolum('Teras')
X0, X1, Y0, Y1 = -1.18, 1.18, -1.2, 1.12
zemin(y, X0, X1, Y0, Y1, H0, TAS2, ust='cimen', basamak=(('on', 0.36),), n_basamak=3)
# the paved circumambulation ground inside the railing
donel(y, C, [(0.97, H0), (0.97, H0 + 0.006), (0.0, H0 + 0.006)], 'zemin', n=64)
ZG = H0 + 0.006
# paved paths from the gates (0.003 lower than the disc: no coplanar overlap)
for th in (-math.pi / 2, 0.0, math.pi / 2, math.pi):
    d = V(math.cos(th), math.sin(th)); t = V(-d.y, d.x)
    p0 = V(*C) + d * 0.95
    p1 = V(*C) + d * (1.28 if th == -math.pi / 2 else 1.14)
    pts = [p0 - t * 0.07, p1 - t * 0.07, p1 + t * 0.07, p0 + t * 0.07]
    # clip to the terrace
    pts = [V(max(X0 + 0.01, min(X1 - 0.01, p.x)), max(Y0 + 0.002, min(Y1 - 0.01, p.y))) for p in pts]
    y.yuz_yon([V(p.x, p.y, H0 + 0.003) for p in pts], 'zemin', Z)
    for a, b in ((pts[0], pts[1]), (pts[2], pts[3])):
        duz_duvar(y, a, b, H0, H0 + 0.003, 'zemin')
    duz_duvar(y, pts[1], pts[2], H0, H0 + 0.003, 'zemin')

# ---------------- the drum (medhi) and the double stair ----------------
y.bolum('Medhi ve çifte merdiven')
RM = 0.64
ZM = ZG + 0.14
donel(y, C, [(RM + 0.02, ZG), (RM + 0.02, ZG + 0.012), (RM, ZG + 0.02), (RM, ZM - 0.012)], TAS, n=60)
halka_kornis(y, C, RM, ZM - 0.014, 0.014, 0.01, 60, TAS3)
# the walkway on top of the drum (paved) and its railing
halka(y, C, RM + 0.01, 0.53, ZM, ZM + 0.003, 'zemin', n=60, atla=(2, 3))
vedika_yay(y, C, RM - 0.015, ZM + 0.003, 0.05, -math.pi / 2 + 0.16, 3 * math.pi / 2 - 0.16, TAS3, aralik=0.04, w=0.009, alt=False)
# the stair: two flights climbing towards each other along the south face, a landing in the middle
YS = C[1] - RM - 0.04
SW = 0.075
for s in (-1, 1):
    merdiven(y, (C[0] + s * 0.36, YS), 0.0 if s < 0 else math.pi, SW, ZG, ZM, n=14, d=0.3 / 14, key=TAS)
# the landing and the walls behind the flights (filling the gap to the drum)
kutu_merkez(y, (C[0], YS + 0.01), 0.13, SW + 0.02, ZM - ZG + 0.003, TAS, z0=ZG)
for s in (-1, 1):
    # a sloping solid wall behind each flight, up against the drum
    xa, xb = C[0] + s * 0.36, C[0] + s * 0.06
    ya, yb = YS + SW / 2, C[1] - math.sqrt(RM * RM - 0.06 ** 2) + 0.01
    kutu_merkez(y, ((xa + xb) / 2, (ya + yb) / 2 + 0.002), abs(xa - xb), yb - ya + 0.004, (ZM - ZG) * 0.55, TAS2, z0=ZG)
    # its railing along the flight's outer edge
    yr = YS - SW / 2 - 0.006
    pa, pb = V(xa, yr, ZG + 0.045), V(xb, yr, ZM + 0.045)
    cubuk(y, pa, pb, 0.012, TAS3, 0.01)
    for k in range(6):
        p = pa.lerp(pb, k / 5)
        cubuk(y, V(p.x, yr, ZG + (ZM - ZG) * k / 5 - 0.002), V(p.x, yr, p.z), 0.009, TAS3)
vedika_duz(y, V(C[0] - 0.07, YS - SW / 2 - 0.004), V(C[0] + 0.07, YS - SW / 2 - 0.004), ZM, 0.045, TAS3, aralik=0.028, w=0.009)

# ---------------- the dome (anda), harmika, chattra ----------------
y.bolum('Anda, harmika, chattra')
RA = 0.555
HA = 0.42
ZA = ZM + 0.003
pr = []
for k in range(15):
    t = k / 14
    ph = t * math.pi / 2 * 0.9
    pr.append((RA * math.cos(ph), ZA + HA * math.sin(ph) / math.sin(math.pi / 2 * 0.9)))
pr[0] = (RA + 0.004, ZA)
pr.append((0.0, pr[-1][1]))
donel(y, C, pr, TAS2, n=60)
ZT = pr[-1][1]
# a garland band (carved) round the anda's lower part
# harmika: a square stone railing on a plinth, a capping slab
HW = 0.095
zemin_h = 0.02
kutu_merkez(y, C, HW * 2 + 0.02, HW * 2 + 0.02, zemin_h + 0.012, TAS, z0=ZT - 0.012)
zh = ZT + zemin_h
hk = dikdortgen(C[0] - HW, C[0] + HW, C[1] - HW, C[1] + HW)
kutu_merkez(y, C, HW * 2 - 0.02, HW * 2 - 0.02, 0.055, TAS2, z0=zh)
for i in range(4):
    vedika_duz(y, hk[i], hk[(i + 1) % 4], zh, 0.06, TAS3, aralik=0.024, w=0.009)
kutu_merkez(y, C, HW * 2 + 0.024, HW * 2 + 0.024, 0.01, TAS3, z0=zh + 0.06)
silme(y, disa(hk, 0.012), zh + 0.07, 0.008, 0.006, TAS3, 'kaba')
y.yuz_yon([V(p.x, p.y, zh + 0.078) for p in disa(hk, 0.012)], TAS3, Z)
zc = zh + 0.078
# the chattra: a stone mast with three umbrellas
y.prizma(C, 0.011, zc, zc + 0.27, TAS3, n=10)
for zz, rr in ((zc + 0.085, 0.1), (zc + 0.165, 0.08), (zc + 0.235, 0.06)):
    donel(y, C, [(0.0, zz - 0.004), (rr * 0.25, zz - 0.004), (rr, zz + 0.002), (rr, zz + 0.009), (rr * 0.7, zz + 0.018), (0.012, zz + 0.026), (0.0, zz + 0.026)], TAS3, n=24)
kalasa(y, C[0], C[1], zc + 0.27, 0.7, TAS3)


# ---------------- the toranas ----------------
# relief figures: convex parts in unit coordinates (u right, v up, base at v 0); each part a flat face standing a hair
# proud of a dark carved panel, so the light figures read against it
FIL_S = [[(-0.5, 0.0), (-0.32, 0.0), (-0.32, 0.38), (-0.5, 0.38)], [(0.12, 0.0), (0.3, 0.0), (0.3, 0.38), (0.12, 0.38)],
         [(-0.6, 0.38), (0.38, 0.38), (0.38, 0.95), (-0.3, 1.0), (-0.6, 0.72)],
         [(0.38, 0.45), (0.62, 0.4), (0.72, 0.68), (0.6, 0.98), (0.38, 0.95)],
         [(0.62, 0.4), (0.699, 0.62), (0.78, 0.08), (0.68, 0.04)]]                      # an elephant facing +u
STUPA_S = [[(-0.36, 0.0), (0.36, 0.0), (0.36, 0.14), (-0.36, 0.14)],
           [(0.3 * math.cos(math.pi * i / 6), 0.14 + 0.42 * math.sin(math.pi * i / 6)) for i in range(7)],
           [(-0.08, 0.56), (0.08, 0.56), (0.08, 0.66), (-0.08, 0.66)], [(-0.02, 0.66), (0.02, 0.66), (0.02, 0.73), (-0.02, 0.73)],
           [(-0.2, 0.73), (0.2, 0.73), (0.0, 0.84)]]
AGAC_S = [[(-0.05, 0.0), (0.05, 0.0), (0.05, 0.42), (-0.05, 0.42)],
          [(0.3 * math.cos(math.pi * i / 3), 0.68 + 0.3 * math.sin(math.pi * i / 3)) for i in range(6)]]
YAKSHI_S = [[(-0.28, 0.0), (0.28, 0.0), (0.16, 0.5), (-0.16, 0.5)], [(-0.16, 0.5), (0.16, 0.5), (0.22, 0.8), (-0.22, 0.8)],
            [(0.0 + 0.1 * math.cos(math.pi * i / 3 + math.pi / 6), 0.91 + 0.1 * math.sin(math.pi * i / 3 + math.pi / 6)) for i in range(6)]]


def kabartma(sekil, u, v, s, duz_y, nn, key=TAS3, ters=False):
    """a flat relief figure at (u, v), scale s, on the plane y = duz_y facing nn (ters: mirrored)"""
    for pc in sekil:
        y.yuz_yon([V(u + (-px if ters else px) * s, duz_y, v + py * s) for px, py in pc], key, nn)


def torana(cx, cy, aci, s=1.0, cap='fil', z=ZG):
    """a Sanchi gateway at (cx, cy) facing away from the stupa (local -y), scale s"""
    with parca(y, (cx, cy, z), aci, s):
        PX, PW, PH = 0.07, 0.026, 0.17
        K = TAS3
        for sx in (-1, 1):
            x = sx * PX
            kutu_merkez(y, (x, 0), PW * 1.4, PW * 1.4, 0.012, TAS)
            kutu_merkez(y, (x, 0), PW, PW, PH - 0.012, K, z0=0.012, yuzler='onarkasagsol')
            # carved panels on the posts' faces (front and back)
            for yy, nn in ((-PW / 2, -Y), (PW / 2, Y)):
                for k in range(3):
                    z0 = 0.03 + k * 0.045
                    pts = [V(x - PW * 0.36, yy + nn.y * 0.0015, z0), V(x + PW * 0.36, yy + nn.y * 0.0015, z0),
                           V(x + PW * 0.36, yy + nn.y * 0.0015, z0 + 0.036), V(x - PW * 0.36, yy + nn.y * 0.0015, z0 + 0.036)]
                    y.yuz_yon(pts, TAS2, nn)
                    # (the panel's edges: it stands 0.0015 proud)
                    for a, b in ((pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[3]), (pts[3], pts[0])):
                        o = (a + b) / 2 - (pts[0] + pts[2]) / 2
                        y.yuz_yon([a, b, b - nn * 0.0015, a - nn * 0.0015], TAS2, o)
                    # its carving: a yakshi, a stupa, a Bodhi tree (light figures on the dark ground)
                    sek, s = ((YAKSHI_S, 0.032), (STUPA_S, 0.024), (AGAC_S, 0.03))[k]
                    kabartma(sek, x, z0 + 0.003, s, yy + nn.y * 0.0035, nn)
            # capital: a bell, an abacus and the beasts (back to back)
            donel(y, (x, 0), [(PW * 0.55, PH), (PW * 0.75, PH + 0.008), (PW * 0.7, PH + 0.012), (0.0, PH + 0.012)], K, n=12)
            kutu_merkez(y, (x, 0), PW * 1.6, PW * 1.6, 0.008, K, z0=PH + 0.012)
            if cap == 'fil':
                for sy in (-1, 1):
                    fil(y, x - sx * 0.0, sy * 0.012, PH + 0.02, -sy * math.pi / 2, 0.21, K, az=True)
            else:   # dwarfs (the west gate): squat figures holding up the architrave
                for sy in (-1, 1):
                    for sxx in (-1, 1):
                        elipsoid(y, (x + sxx * 0.008, sy * 0.009, PH + 0.03), 0.007, 0.006, 0.01, K, n=6, kat=3)
                        kure(y, (x + sxx * 0.008, sy * 0.009, PH + 0.043), 0.004, K, n=6, kat=3)
            # the posts carry on up through the architraves
        Z1 = PH + 0.046
        AH, AG = 0.024, 0.034
        AL = 0.122
        for k in range(3):
            za = Z1 + k * (AH + AG)
            al = AL - k * 0.004
            kutu_merkez(y, (0, 0), al * 2, 0.03, AH, K, z0=za)
            # carved relief on both faces between the posts and on the overhangs
            for yy, nn in ((-0.015, -Y), (0.015, Y)):
                for (u0, u1) in ((-PX + PW * 0.6, PX - PW * 0.6), (-al + 0.022, -PX - PW * 0.6), (PX + PW * 0.6, al - 0.022)):
                    pts = [V(u0, yy + nn.y * 0.0012, za + 0.005), V(u1, yy + nn.y * 0.0012, za + 0.005), V(u1, yy + nn.y * 0.0012, za + AH - 0.005),
                           V(u0, yy + nn.y * 0.0012, za + AH - 0.005)]
                    y.yuz_yon(pts, TAS2, nn)
                    for a, b in ((pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[3]), (pts[3], pts[0])):
                        o = (a + b) / 2 - (pts[0] + pts[2]) / 2
                        y.yuz_yon([a, b, b - nn * 0.0012, a - nn * 0.0012], TAS2, o)
                    # the carving: Jataka scenes as light figures on the dark ground
                    yf = yy + nn.y * 0.0032
                    zf = za + 0.0055
                    if u0 < -PX + PW and u1 > PX - PW:
                        if k == 1:      # a procession of elephants between two trees
                            for uu in (-0.026, 0.0, 0.026):
                                kabartma(FIL_S, uu - 0.002, zf, 0.0115, yf, nn)
                            for uu in (-0.046, 0.046):
                                kabartma(AGAC_S, uu, zf, 0.0125, yf, nn)
                        else:           # the stupa worshipped by elephants, trees at the ends
                            kabartma(STUPA_S, 0.0, zf, 0.0145, yf, nn)
                            for sg in (-1, 1):
                                kabartma(FIL_S, sg * 0.021, zf, 0.0115, yf, nn, ters=sg > 0)
                                kabartma(AGAC_S, sg * 0.044, zf, 0.0125, yf, nn)
                    else:
                        kabartma(AGAC_S if k != 1 else STUPA_S, (u0 + u1) / 2, zf, 0.0125, yf, nn)
            # the scrolled (volute) ends
            for sx in (-1, 1):
                for yy in (-0.0165, 0.0165):
                    cxv, czv = sx * (al - 0.013), za + AH / 2
                    spir = [V(cxv + sx * 0.012 * (1 - u / 10) * math.cos(u * 0.9 - 1.2), yy, czv + 0.012 * (1 - u / 10) * math.sin(u * 0.9 - 1.2)) for u in range(8)]
                    boru(y, spir, 0.0022, K, n=4)
            # between the architraves: dies over the posts, short balusters and riders
            if k < 2:
                zb = za + AH
                for sx in (-1, 1):
                    kutu_merkez(y, (sx * PX, 0), PW, PW, AG, K, z0=zb)
                    kutu_merkez(y, (sx * (al - 0.02), 0), 0.016, 0.016, AG, K, z0=zb)
                    # a horse and rider on the overhang
                    elipsoid(y, (sx * (al - 0.045), 0, zb + 0.012), 0.011, 0.005, 0.006, K, n=6, kat=3)
                    kure(y, (sx * (al - 0.045), 0, zb + 0.024), 0.004, K, n=6, kat=3)
                for u in (-0.03, 0.0, 0.03):
                    kutu_merkez(y, (u, 0), 0.008, 0.012, AG, K, z0=zb, yuzler='onarkasagsol')
        zt = Z1 + 3 * AH + 2 * AG
        # yakshi brackets: a figure leaning from the capital out under the lowest architrave
        for sx in (-1, 1):
            p0 = V(sx * (PX + PW * 0.55), 0, PH - 0.02)
            p1 = V(sx * (AL - 0.02), 0, Z1 - 0.002)
            boru(y, [p0, p0.lerp(p1, 0.5) + V(sx * 0.004, 0, 0), p1], 0.0045, K, n=6, r_son=0.003)
            kure(y, p0.lerp(p1, 0.82) + V(sx * 0.006, 0, 0.004), 0.0045, K, n=6, kat=3)
            boru(y, [p1 - V(0, 0, 0.001), p1 + V(-sx * 0.02, 0, 0.006)], 0.003, TAS2, n=4)   # the tree branch she holds
        # the top: a dharmachakra in the middle on a pedestal, triratnas over the posts
        kutu_merkez(y, (0, 0), 0.02, 0.014, 0.01, K, z0=zt)
        wc = V(0, 0, zt + 0.01 + 0.027)
        ring = [wc + V(0.024 * math.cos(TAU * i / 16), 0, 0.024 * math.sin(TAU * i / 16)) for i in range(17)]
        boru(y, ring, 0.0035, K, n=5, kapat=False)
        for i in range(8):
            a = TAU * i / 8
            cubuk(y, wc, wc + V(0.022 * math.cos(a), 0, 0.022 * math.sin(a)), 0.0025, K)
        kure(y, wc, 0.006, K, n=8, kat=4)
        for sx in (-1, 1):
            b = V(sx * PX, 0, zt)
            kutu_merkez(y, (b.x, 0), 0.016, 0.014, 0.012, K, z0=zt)
            kure(y, b + V(0, 0, 0.024), 0.009, K, n=8, kat=4)
            for u in (-1, 0, 1):
                boru(y, [b + V(u * 0.009, 0, 0.026), b + V(u * 0.012, 0, 0.04 + (0.006 if u == 0 else 0))], 0.0025, K, n=4, r_son=0.001)
            # a yaksha with a flywhisk beside the wheel
            elipsoid(y, (sx * 0.038, 0, zt + 0.018), 0.006, 0.005, 0.016, K, n=6, kat=4)
            kure(y, (sx * 0.038, 0, zt + 0.038), 0.005, K, n=6, kat=3)
        return zt


y.bolum('Vedika ve toranalar')
RV = 0.9
GAP = 0.085
for k in range(4):
    th = -math.pi / 2 + k * math.pi / 2
    vedika_yay(y, C, RV, ZG, 0.11, th + GAP, th + math.pi / 2 - GAP, TAS, aralik=0.034, w=0.014, ust_key=TAS3, alt=False)
RT = 1.0
for k, (th, cap) in enumerate(((-math.pi / 2, 'fil'), (0.0, 'fil'), (math.pi / 2, 'fil'), (math.pi, 'cuce'))):
    d = V(math.cos(th), math.sin(th)); t = V(-d.y, d.x)
    pc = V(*C) + d * RT
    torana(pc.x, pc.y, th + math.pi / 2, 1.2, cap)
    # railing returns from the gap out to the posts
    for s in (-1, 1):
        a = V(*C) + V(math.cos(th + s * GAP), math.sin(th + s * GAP)) * RV
        b = pc + t * (s * 0.1)
        vedika_duz(y, a, b, ZG, 0.11, TAS, aralik=0.034, w=0.014, ust_key=TAS3)

# ---------------- Ashoka's pillar ----------------
y.bolum('Asoka sütunu')
AX, AY = -0.42, C[1] - 1.0
kutu_merkez(y, (AX, AY), 0.06, 0.06, 0.016, TAS2, z0=H0)
donel(y, (AX, AY), [(0.014, H0 + 0.016), (0.0125, H0 + 0.2), (0.0105, H0 + 0.36), (0.0, H0 + 0.36)], 'kum_acik', n=12)
zp = H0 + 0.36
donel(y, (AX, AY), [(0.009, zp - 0.001), (0.022, zp + 0.004), (0.022, zp + 0.008), (0.016, zp + 0.022), (0.01, zp + 0.03), (0.0, zp + 0.03)], 'kum_acik', n=16)
y.prizma((AX, AY), 0.02, zp + 0.03, zp + 0.04, 'kum_acik', n=16)
for i in range(4):
    a = TAU * i / 4 + math.pi / 4
    d = V(math.cos(a), math.sin(a))
    lp = V(AX, AY) + d * 0.009
    elipsoid(y, (lp.x, lp.y, zp + 0.05), 0.008, 0.008, 0.01, 'kum_acik', n=6, kat=3)
    hp = V(AX, AY) + d * 0.015
    kure(y, (hp.x, hp.y, zp + 0.062), 0.0065, 'kum_acik', n=8, kat=4)
    fp = V(AX, AY) + d * 0.014
    cubuk(y, V(fp.x, fp.y, zp + 0.04), V(fp.x, fp.y, zp + 0.05), 0.004, 'kum_acik')

# ---------------- the banner ----------------
sancak(y, 0.27, C[1] - 1.05, H0, boy=0.3, en=0.13, yuk=0.08, aci=-0.4)
kutu_merkez(y, (0.27, C[1] - 1.05), 0.04, 0.04, 0.012, TAS2, z0=H0)

# ---------------- Stupa 3 ----------------
y.bolum('Stupa 3')
S3 = (0.86, 0.8)
r3 = 0.17
donel(y, S3, [(0.235, H0), (0.235, H0 + 0.005), (0.0, H0 + 0.005)], 'zemin', n=40)
z3 = H0 + 0.005
donel(y, S3, [(r3 + 0.012, z3), (r3 + 0.012, z3 + 0.008), (r3, z3 + 0.012), (r3, z3 + 0.06)], TAS, n=40)
halka_kornis(y, S3, r3, z3 + 0.052, 0.008, 0.006, 40, TAS3)
pr3 = [(r3 * 0.86 * math.cos(t * math.pi / 2 * 0.9), z3 + 0.06 + 0.13 * math.sin(t * math.pi / 2 * 0.9) / math.sin(math.pi / 2 * 0.9)) for t in [k / 8 for k in range(9)]]
pr3.append((0.0, pr3[-1][1]))
donel(y, S3, [(r3, z3 + 0.06)] + pr3, TAS, n=40)
z3t = pr3[-1][1]
kutu_merkez(y, S3, 0.07, 0.07, 0.03, TAS3, z0=z3t - 0.006)
kutu_merkez(y, S3, 0.085, 0.085, 0.006, TAS3, z0=z3t + 0.024)
y.prizma(S3, 0.006, z3t + 0.03, z3t + 0.1, TAS3, n=8)
donel(y, S3, [(0.0, z3t + 0.07), (0.04, z3t + 0.074), (0.035, z3t + 0.082), (0.0, z3t + 0.088)], TAS3, n=16)
vedika_yay(y, S3, 0.225, z3, 0.065, -math.pi / 2 + 0.3, 3 * math.pi / 2 - 0.3, TAS, aralik=0.03, w=0.011, ust_key=TAS3, alt=False)
torana(S3[0], S3[1] - 0.25, 0.0, 0.62, 'fil', z=z3)

# ---------------- Temple 17 (Gupta) ----------------
y.bolum('Tapınak 17')
T17 = (0.84, -0.8)
kutu_merkez(y, T17, 0.26, 0.24, 0.025, TAS2, z0=H0)
silme(y, dikdortgen(T17[0] - 0.13, T17[0] + 0.13, T17[1] - 0.12, T17[1] + 0.12), H0 + 0.019, 0.006, 0.005, TAS3, 'duz')
zt7 = H0 + 0.025
# the cella: plain walls, a door in front (south), a flat slab roof with a moulded edge
ck = dikdortgen(T17[0] - 0.08, T17[0] + 0.08, T17[1] - 0.02, T17[1] + 0.1)
kapi(y, ck[0], ck[1], zt7, 0.32, 0.12, (TAS, TAS2, TAS3, 'koyu'), derin=0.015, cerceve=(0.006, TAS3))
for i in (1, 2, 3):
    duz_duvar(y, ck[i], ck[(i + 1) % 4], zt7, zt7 + 0.12, TAS)
# the portico: four pillars with bell capitals and lions, the roof slab carried forward over them
for u in (-0.066, -0.022, 0.022, 0.066):
    x = T17[0] + u; yy = T17[1] - 0.09
    kutu_merkez(y, (x, yy), 0.02, 0.02, 0.016, TAS3, z0=zt7)
    y.prizma((x, yy), 0.0075, zt7 + 0.016, zt7 + 0.086, TAS3, n=8, kat=math.pi / 8)
    donel(y, (x, yy), [(0.006, zt7 + 0.086), (0.011, zt7 + 0.094), (0.0105, zt7 + 0.1), (0.0, zt7 + 0.1)], TAS3, n=10)
    kutu_merkez(y, (x, yy), 0.024, 0.024, 0.02, TAS3, z0=zt7 + 0.1)
kutu_merkez(y, (T17[0], T17[1] - 0.09), 0.18, 0.026, 0.016, TAS3, z0=zt7 + 0.12 - 0.016 + 0.004)   # architrave
rk = dikdortgen(T17[0] - 0.095, T17[0] + 0.095, T17[1] - 0.11, T17[1] + 0.11)
kutu(y, V(rk[0].x, rk[0].y, zt7 + 0.124), X, 0.19, 0.22, 0.016, TAS, 'onarkasagsolust')
silme(y, rk, zt7 + 0.124, 0.016, 0.008, TAS3, 'kaba')
y.yuz_yon([V(p.x, p.y, zt7 + 0.14 + 0.0005) for p in rk], TAS3, Z)
y.yuz_yon([V(rk[0].x, rk[0].y, zt7 + 0.124), V(rk[3].x, rk[3].y, zt7 + 0.124), V(rk[2].x, rk[2].y, zt7 + 0.124), V(rk[1].x, rk[1].y, zt7 + 0.124)], TAS2, -Z)
merdiven(y, (T17[0], T17[1] - 0.12 - 0.04), math.pi / 2, 0.09, H0, zt7, n=3, d=0.014, key=TAS2)

# ---------------- Temple 18 (apsidal, its pillars standing) ----------------
y.bolum('Tapınak 18')
T18 = (-0.84, -0.74)
kutu_merkez(y, T18, 0.3, 0.36, 0.022, TAS2, z0=H0)
zt8 = H0 + 0.022
# the apse wall at the back (+y), low
yay_kesit(y, (T18[0], T18[1] + 0.06), [(0.11, zt8), (0.11, zt8 + 0.07), (0.09, zt8 + 0.07), (0.09, zt8)], 0.0, math.pi, 16, TAS)
for s in (-1, 1):
    kutu_merkez(y, (T18[0] + s * 0.1, T18[1] - 0.02), 0.02, 0.16, 0.07, TAS, z0=zt8)
# the hall's tall square pillars (some still carrying their lintels)
for i, (u, v) in enumerate(((-0.065, -0.16), (0.065, -0.16), (-0.065, -0.09), (0.065, -0.09), (-0.065, -0.02), (0.065, -0.02),
                            (-0.065, 0.05), (0.065, 0.05))):
    x, yy = T18[0] + u, T18[1] + v
    hh = 0.21 if i not in (5, 6) else 0.13
    kutu_merkez(y, (x, yy), 0.024, 0.024, 0.014, TAS2, z0=zt8)
    kutu_merkez(y, (x, yy), 0.018, 0.018, hh, TAS3, z0=zt8 + 0.014)
    kutu_merkez(y, (x, yy), 0.026, 0.026, 0.012, TAS3, z0=zt8 + 0.014 + hh)
for (u, v0, v1) in ((-0.065, -0.16, -0.09), (0.065, -0.16, -0.09), (-0.065, -0.09, -0.02)):
    kutu_merkez(y, (T18[0] + u, T18[1] + (v0 + v1) / 2), 0.024, v1 - v0 + 0.026, 0.016, TAS3, z0=zt8 + 0.014 + 0.21 + 0.012)
kutu_merkez(y, (T18[0], T18[1] - 0.16), 0.156, 0.024, 0.016, TAS3, z0=zt8 + 0.014 + 0.21 + 0.012 + 0.016)

# ---------------- a monastery's ruins ----------------
y.bolum('Manastır kalıntıları')
MX0, MX1, MY0, MY1 = -1.1, -0.66, 0.5, 1.02
kutu(y, V(MX0, MY0, H0), X, MX1 - MX0, MY1 - MY0, 0.012, TAS2, 'onarkasagsolust')
zm0 = H0 + 0.012
mk = dikdortgen(MX0 + 0.01, MX1 - 0.01, MY0 + 0.01, MY1 - 0.01)
ic = dikdortgen(MX0 + 0.1, MX1 - 0.1, MY0 + 0.1, MY1 - 0.1)
for poly, h in ((mk, 0.045), (ic, 0.035)):
    for i in range(4):
        a, b = poly[i], poly[(i + 1) % 4]
        L = (b - a).length; e = (b - a) / L
        n = 4
        for j in range(n):
            p, q = a.lerp(b, j / n + 0.03), a.lerp(b, (j + 1) / n - 0.03)
            if poly is ic and j == 1 and i == 0: continue    # the court's door
            kutu(y, p + Z * zm0, e, (q - p).length, 0.016, h * (0.75 + 0.25 * ((i + j) % 2)), TAS, 'onarkasagsolust')
# cell partitions between the two rings
for i in range(4):
    a, b, ai, bi = mk[i], mk[(i + 1) % 4], ic[i], ic[(i + 1) % 4]
    for t in (0.25, 0.5, 0.75):
        p = a.lerp(b, t)
        ee = (b - a).normalized()
        q = p + V(-ee.y, ee.x) * 0.09
        e = (q - p).normalized()
        kutu(y, p + Z * zm0 + V(-e.y, e.x) * 0.006, e, (q - p).length, 0.012, 0.03, TAS, 'onarkasagsolust')
y.yuz_yon([V(p.x, p.y, zm0 + 0.0005) for p in ic], 'zemin', Z)
# a small votive stupa in its court
cm = ((MX0 + MX1) / 2, (MY0 + MY1) / 2)
donel(y, cm, [(0.04, zm0), (0.04, zm0 + 0.02), (0.034, zm0 + 0.03), (0.026, zm0 + 0.05), (0.012, zm0 + 0.06), (0.0, zm0 + 0.062)], TAS, n=16)
y.prizma(cm, 0.003, zm0 + 0.06, zm0 + 0.09, TAS3, n=6)
donel(y, cm, [(0.0, zm0 + 0.08), (0.016, zm0 + 0.083), (0.0, zm0 + 0.087)], TAS3, n=10)

# votive stupas along the paths
for (x, yy) in ((0.42, -0.98), (0.55, -0.62), (-0.5, -0.98), (0.95, 0.2), (1.0, -0.25), (-1.0, 0.25), (-0.98, -0.3), (0.45, 0.98)):
    donel(y, (x, yy), [(0.03, H0), (0.03, H0 + 0.014), (0.024, H0 + 0.022), (0.016, H0 + 0.036), (0.006, H0 + 0.043), (0.0, H0 + 0.044)], TAS, n=12)
    y.prizma((x, yy), 0.0025, H0 + 0.043, H0 + 0.065, TAS3, n=5)
    donel(y, (x, yy), [(0.0, H0 + 0.056), (0.011, H0 + 0.058), (0.0, H0 + 0.062)], TAS3, n=8)

# ---------------- trees, monks ----------------
y.bolum('Ağaçlar, keşişler')
for (x, yy, b) in ((-1.05, -0.2, 0.2), (-0.62, -1.05, 0.17), (1.06, -0.5, 0.18), (1.07, 0.45, 0.2), (0.3, 1.0, 0.16), (-0.3, 1.0, 0.18),
                   (-0.55, 0.98, 0.15), (0.6, 0.95, 0.14), (-1.08, -1.05, 0.15), (1.08, -1.08, 0.14)):
    agac(y, x, yy, H0, boy=b, tur='yaprakli', key='yesil_koyu' if int(x * 10) % 2 else 'boya_yesil')
for k, a in enumerate((-2.4, -1.9, -0.5, 0.35, 1.2, 2.0, 2.7, 3.6)):
    rr = 0.79 if k % 2 else 0.83
    adam(y, C[0] + rr * math.cos(a), C[1] + rr * math.sin(a), ZG, a + math.pi / 2, 'siva_oker', 'ahsap_acik', boy=0.045)
for (x, yy, a) in ((0.0, C[1] - 1.12, 1.6), (0.05, C[1] - 1.17, 1.4), (0.84, -0.98, 1.57)):
    adam(y, x, yy, H0 + 0.003, a, 'siva_oker', 'ahsap_acik', boy=0.045)

bolum_say(y)
calistir(y, 'lm_sanchi')
