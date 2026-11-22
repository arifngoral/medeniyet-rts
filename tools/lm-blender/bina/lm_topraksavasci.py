# Pişmiş Toprak Atölyesi (lm_topraksavasci): the workshops of the Terracotta Army: a Qin high-terrace hall (three
# rammed-earth terraces with galleries, a grand stair, a double-eaved hipped hall), the excavated pit with its corridors
# of brick-floored trenches between earth walls, ranks of soldiers, a chariot team and a timber-roofed part; open
# workshop sheds with unfinished figures and moulds, horseshoe-domed kilns with chimneys and smoke, firewood, clay heaps,
# painted soldiers lined up in the yard, an ox cart bringing a new figure, workers.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ortak import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(8)
Z0 = 0.05
GX0, GX1, GY0, GY1 = -1.05, 1.05, -1.02, 1.02
PX0, PX1, PY0, PY1 = -0.97, -0.12, -0.94, -0.3      # the pit
ZP = 0.008                                          # its brick floor
KIL = 'kerpic'                                      # fired clay


# ---------------- figures ----------------
def asker(x, yy, z, aci=-math.pi / 2, boya=None, s=1.0, okcu=False, yarim=False):
    """a terracotta warrior on his plinth, facing aci: boya = (tunic, armour) keys for a painted one; yarim: an
    unfinished figure (no head and arms yet)"""
    tun, zir = boya or (KIL, KIL)
    with parca(y, (x, yy, z), aci - math.pi / 2, s):
        # (built facing -y)
        kutu_merkez(y, (0, 0), 0.026, 0.022, 0.004, KIL)
        for sx in (-1, 1):
            if okcu:   # a kneeling archer
                cubuk(y, V(sx * 0.005, 0.004, 0.004), V(sx * 0.005, -0.004, 0.012), 0.006, KIL)
            else:
                cubuk(y, V(sx * 0.005, 0, 0.004), V(sx * 0.005, 0, 0.02), 0.006, KIL)
        zb = 0.012 if okcu else 0.018
        # the robe flaring at the knee, the armour vest
        donel(y, (0, 0), [(0.0, zb), (0.0105, zb), (0.009, zb + 0.008), (0.0085, zb + 0.02), (0.0, zb + 0.02)], tun, n=8)
        donel(y, (0, 0), [(0.0, zb + 0.008), (0.0095, zb + 0.008), (0.009, zb + 0.016), (0.0075, zb + 0.022), (0.0, zb + 0.022)], zir, n=8)
        if yarim: return
        for sx in (-1, 1):   # arms
            cubuk(y, V(sx * 0.009, 0, zb + 0.019), V(sx * 0.011, -0.004, zb + 0.008), 0.004, tun)
        kure(y, (0, 0, zb + 0.028), 0.0052, 'siva_krem' if boya else KIL, n=8, kat=4)
        kure(y, (0.0, 0.002, zb + 0.034), 0.0025, 'koyu' if boya else KIL, n=6, kat=3)   # the topknot


def at(x, yy, z, aci, key=KIL, s=1.0):
    """a terracotta horse facing aci"""
    with parca(y, (x, yy, z), aci, s):
        boru(y, [V(-0.022, 0, 0.03), V(0.0, 0, 0.032), V(0.02, 0, 0.031)], 0.011, key, n=8)
        boru(y, [V(0.02, 0, 0.032), V(0.03, 0, 0.046), V(0.034, 0, 0.052)], 0.006, key, n=6, r_son=0.004)
        boru(y, [V(0.031, 0, 0.054), V(0.044, 0, 0.046)], 0.005, key, n=6, r_son=0.0035)
        for (lx, ly) in ((-0.016, -0.006), (-0.016, 0.006), (0.015, -0.006), (0.015, 0.006)):
            cubuk(y, V(lx, ly, 0.0), V(lx, ly, 0.026), 0.005, key)
        cubuk(y, V(-0.022, 0, 0.034), V(-0.03, 0, 0.018), 0.004, key)
        kutu_merkez(y, (0, 0), 0.05, 0.02, 0.003, key)


def kalip(x, yy, z, aci=0.0):
    """a pair of mould halves leaning on a stand"""
    with parca(y, (x, yy, z), aci):
        for sx in (-1, 1):
            kutu(y, V(-0.012, sx * 0.006 - 0.003, 0), X, 0.024, 0.006, 0.03, 'kerpic_koyu')
        kutu_merkez(y, (0, 0), 0.034, 0.024, 0.004, 'ahsap')


# ---------------- ground ----------------
y.bolum('Zemin')
for (x0, x1, y0_, y1_) in ((GX0, GX1, PY1, GY1), (GX0, GX1, GY0, PY0), (GX0, PX0, PY0, PY1), (PX1, GX1, PY0, PY1)):
    kutu(y, V(x0, y0_, 0), X, x1 - x0, y1_ - y0_, Z0, 'kaya_koyu', ''.join(s for s, c in (('on', y0_ == GY0), ('arka', y1_ == GY1),
                                                                                         ('sol', x0 == GX0), ('sag', x1 == GX1)) if c))
    y.yuz_yon([V(x0, y0_, Z0), V(x1, y0_, Z0), V(x1, y1_, Z0), V(x0, y1_, Z0)], 'toprak', Z)
# packed-earth yard and paths: lighter strips
for (x0, x1, y0_, y1_) in ((-0.08, 0.16, GY0, 0.1), (-0.95, 1.0, -0.22, -0.1)):
    y.yuz_yon([V(x0, y0_, Z0 + 0.002), V(x1, y0_, Z0 + 0.002), V(x1, y1_, Z0 + 0.002), V(x0, y1_, Z0 + 0.002)], 'kum_acik', Z)


# ---------------- the pit ----------------
y.bolum('Çukur: koridorlar ve toprak ordu')
# the pit's walls (earth) and floor (brick)
for (a, b) in ((V(PX0, PY0), V(PX0, PY1)), (V(PX0, PY1), V(PX1, PY1)), (V(PX1, PY1), V(PX1, PY0)), (V(PX1, PY0), V(PX0, PY0))):
    duz_duvar(y, a, b, ZP, Z0, 'toprak')
y.yuz_yon([V(PX0, PY0, ZP), V(PX1, PY0, ZP), V(PX1, PY1, ZP), V(PX0, PY1, ZP)], 'tugla_koyu', Z)
# the earth partitions between the corridors (along y), the front transverse trench left open
NK = 9
CW = (PX1 - PX0) / NK
YT = PY0 + 0.12                     # the vanguard trench's back edge
YR = PY1 - 0.17                     # the timber-roofed part begins
for i in range(1, NK):
    x = PX0 + CW * i
    kutu(y, V(x - 0.009, YT, ZP), X, 0.018, PY1 - YT, Z0 - 0.006 - ZP, 'toprak', 'onsagsolust')
# soldiers in the corridors, facing the front
PAINT = [('boya_kirmizi', 'lacivert'), ('boya_yesil', 'kerpic_koyu'), ('lacivert', 'boya_kirmizi'), ('siva_oker', 'koyu')]
for i in range(NK):
    cx = PX0 + CW * (i + 0.5)
    if i == 4:   # the chariot team in the middle corridor
        for k in range(4):
            at(cx - 0.018 + 0.012 * k - 0.0, YT + 0.06, ZP, -math.pi / 2, s=0.9)
        # the chariot box and wheels
        kutu_merkez(y, (cx, YT + 0.12), 0.04, 0.032, 0.014, 'ahsap_koyu', z0=ZP + 0.012)
        for sx in (-1, 1):
            pts = [V(cx + sx * 0.024, YT + 0.12 + 0.016 * math.cos(TAU * k / 12), ZP + 0.017 + 0.016 * math.sin(TAU * k / 12)) for k in range(13)]
            boru(y, pts, 0.0022, 'ahsap_koyu', n=4, kapat=False)
        boru(y, [V(cx - 0.026, YT + 0.12, ZP + 0.017), V(cx + 0.026, YT + 0.12, ZP + 0.017)], 0.002, 'ahsap_koyu', n=4)
        cubuk(y, V(cx, YT + 0.105, ZP + 0.02), V(cx, YT + 0.04, ZP + 0.035), 0.004, 'ahsap_koyu')
        for k in range(3):
            asker(cx + (k - 1) * 0.02, YT + 0.17, ZP, boya=PAINT[k % 4] if k == 1 else None, s=0.9)
        continue
    for k in range(6):
        yy = YT + 0.035 + k * 0.07
        if yy > YR - 0.02: break
        boya = PAINT[(i + k) % 4] if (i + k) % 5 == 0 else None
        asker(cx, yy, ZP, boya=boya)
# the vanguard: three ranks of archers across the front trench
for r in range(3):
    for i in range(14):
        x = PX0 + 0.04 + (PX1 - PX0 - 0.08) * i / 13
        asker(x, PY0 + 0.025 + r * 0.035, ZP, okcu=(r == 0), boya=PAINT[(i + r) % 4] if (i * 3 + r) % 7 == 0 else None, s=0.85)
# the unexcavated back: timber roof logs over the corridors and earth on them
for i in range(NK):
    x0 = PX0 + CW * i + (0.009 if i > 0 else 0.0)
    x1 = PX0 + CW * (i + 1) - (0.009 if i < NK - 1 else 0.0)
    for k in range(int((PY1 - YR) / 0.018)):
        yy = YR + 0.009 + k * 0.018
        boru(y, [V(x0 - 0.008, yy, Z0 - 0.012), V(x1 + 0.008, yy, Z0 - 0.012)], 0.0075, 'ahsap' if (i + k) % 3 else 'ahsap_koyu', n=6)
# a mat-covered heap at the back edge (the earth not yet lifted)
for k in range(5):
    x = PX0 + 0.08 + k * 0.17
    kure(y, (x, PY1 - 0.06, Z0 - 0.01), 0.05, 'toprak', n=10, kat=4)
# a wooden ladder down into the pit
boru(y, [V(PX1 - 0.03, PY1 - 0.002, ZP), V(PX1 - 0.03, PY1 + 0.01, Z0 + 0.03)], 0.0025, 'ahsap', n=4)
boru(y, [V(PX1 - 0.06, PY1 - 0.002, ZP), V(PX1 - 0.06, PY1 + 0.01, Z0 + 0.03)], 0.0025, 'ahsap', n=4)
for k in range(6):
    t = (k + 0.5) / 6
    cubuk(y, V(PX1 - 0.062, PY1 - 0.002 + 0.012 * t, ZP + (Z0 + 0.03 - ZP) * t), V(PX1 - 0.028, PY1 - 0.002 + 0.012 * t, ZP + (Z0 + 0.03 - ZP) * t),
          0.0025, 'ahsap')
# a railing of posts round the pit's rim
for (a, b) in ((V(PX0, PY0), V(PX1, PY0)), (V(PX1, PY0), V(PX1, PY1)), (V(PX0, PY1), V(PX0, PY0))):
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    m = int(L / 0.08)
    for k in range(m + 1):
        p = a.lerp(b, k / m) + nn * 0.015
        cubuk(y, p + Z * Z0, p + Z * (Z0 + 0.03), 0.005, 'ahsap')
    boru(y, [a + nn * 0.015 + Z * (Z0 + 0.026), b + nn * 0.015 + Z * (Z0 + 0.026)], 0.002, 'kumas', n=4, kapat=False)


# ---------------- the high-terrace hall ----------------
y.bolum('Qin yüksek teras salonu')
TC = V(0.05, 0.5)
TER = [(0.4, 0.3, 0.12), (0.3, 0.22, 0.11), (0.21, 0.15, 0.08)]
z = Z0
for k, (hw, hd, hh) in enumerate(TER):
    k4 = dikdortgen(TC.x - hw, TC.x + hw, TC.y - hd, TC.y + hd)
    duvarlar(y, k4, z, z + hh, 'kerpic')
    # timber posts set in the rammed earth, a lacquered beam on top
    for i in range(4):
        a, b = k4[i], k4[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        m = max(2, int(L / 0.06))
        for j in range(m + 1):
            p = a.lerp(b, j / m) + nn * 0.003
            kutu_merkez(y, (p.x, p.y), 0.008, 0.008, hh - 0.012, 'lake_koyu', z0=z)
    kornis(y, TC.x - hw, TC.x + hw, TC.y - hd, TC.y + hd, z + hh - 0.012, 0.012, 0.005, 'lake_koyu')
    kornis(y, TC.x - hw, TC.x + hw, TC.y - hd, TC.y + hd, z, 0.012, 0.006, 'granit')
    zt = z + hh
    y.yuz_yon([V(p.x, p.y, zt) for p in k4], 'zemin', Z)
    if k < 2:
        # a gallery round the next terrace's foot: a lean-to roof on posts over the walk
        hw2, hd2 = TER[k + 1][0], TER[k + 1][1]
        gk = dikdortgen(TC.x - hw2, TC.x + hw2, TC.y - hd2, TC.y + hd2)
        gd = min(hw - hw2, hd - hd2) * 0.72
        dk = disa(gk, gd)
        zr0, zr1 = zt + TER[k + 1][2] * 0.85, zt + 0.045
        for i in range(4):
            j = (i + 1) % 4
            nn = (dk[i] - gk[i]) + (dk[j] - gk[j])
            # (the front side leaves a gap for the stair)
            parts = [(0.0, 1.0)]
            if i == 0:
                L0 = (gk[j] - gk[i]).length; g = (0.09 - 0.012 * (k + 1)) / 2 + 0.014
                parts = [(0.0, 0.5 - g / L0), (0.5 + g / L0, 1.0)]
            for (u0, u1) in parts:
                gi, gj = gk[i].lerp(gk[j], u0), gk[i].lerp(gk[j], u1)
                di = dk[i] if u0 == 0 else gi + V(0, -gd, 0)
                dj = dk[j] if u1 == 1 else gj + V(0, -gd, 0)
                y.yuz_yon([gi + Z * zr0, di + Z * zr1, dj + Z * zr1, gj + Z * zr0], 'kiremit_koyu', nn + Z * 2)
                y.yuz_yon([di + Z * zr1, dj + Z * zr1, dj + Z * (zr1 - 0.008), di + Z * (zr1 - 0.008)], 'lake_koyu', nn)
                y.yuz_yon([gj + Z * (zr0 - 0.008), dj + Z * (zr1 - 0.008), di + Z * (zr1 - 0.008), gi + Z * (zr0 - 0.008)], 'ahsap_koyu', -Z)
                if i == 0:   # the cut ends
                    e_ = (gk[j] - gk[i]).normalized()
                    if u0 > 0:
                        y.yuz_yon([gi + Z * zr0, di + Z * zr1, di + Z * (zr1 - 0.008), gi + Z * (zr0 - 0.008)], 'lake_koyu', -e_)
                    if u1 < 1:
                        y.yuz_yon([gj + Z * zr0, dj + Z * zr1, dj + Z * (zr1 - 0.008), gj + Z * (zr0 - 0.008)], 'lake_koyu', e_)
            L = (dk[j] - dk[i]).length
            m = max(2, int(L / 0.07))
            for t in range(m + 1):
                p = dk[i].lerp(dk[j], t / m) - nn.normalized() * 0.006
                kutu_merkez(y, (p.x, p.y), 0.008, 0.008, zr1 - 0.008 - zt, 'lake', z0=zt)
        for i in range(4):   # hip ridges at the gallery corners
            cubuk(y, gk[i] + Z * (zr0 + 0.003), dk[i] + Z * (zr1 + 0.003), 0.007, 'kiremit_koyu2')
    z = zt
ZT = z
# the grand stair up the front of the terraces
z = Z0
for k, (hw, hd, hh) in enumerate(TER):
    yf = TC.y - hd
    en = 0.09 - 0.012 * k
    ys = yf - hh * 1.15
    merdiven(y, (TC.x, ys), math.pi / 2, en, z, z + hh, n=8, d=hh * 1.15 / 8, key='granit')
    # the cheeks: solid sloped walls with a clean vertical foot and a capping, ending flush against the terrace face
    # (the library's sloped beams overshot at both ends and stepped where the flights met)
    for sg in (-1, 1):
        xi, xo = TC.x + sg * (en / 2 - 0.001), TC.x + sg * (en / 2 + 0.013)
        ta, tb = z + 0.026, z + hh + 0.016
        for xx, yon in ((xo, V(sg, 0, 0)), (xi, V(-sg, 0, 0))):
            y.yuz_yon([V(xx, ys, z), V(xx, yf, z), V(xx, yf, tb), V(xx, ys, ta)], 'kerpic', yon)
        y.yuz_yon([V(xi, ys, z), V(xo, ys, z), V(xo, ys, ta), V(xi, ys, ta)], 'kerpic', -Y)
        # a stone capping along the slope, a hair proud
        ci, co = xi - sg * 0.002, xo + sg * 0.002
        q = [V(ci, ys - 0.002, ta), V(co, ys - 0.002, ta), V(co, yf, tb), V(ci, yf, tb)]
        y.yuz_yon(q, 'granit', Z)
        y.yuz_yon([q[0] - Z * 0.005, q[1] - Z * 0.005, q[1], q[0]], 'granit', -Y)
        for (pa, pb, yon) in ((q[1], q[2], V(sg, 0, 0)), (q[3], q[0], V(-sg, 0, 0))):
            y.yuz_yon([pa - Z * 0.005, pb - Z * 0.005, pb, pa], 'granit', yon)
        # a newel block at the foot
        kutu_merkez(y, ((xi + xo) / 2, ys + 0.008), 0.02, 0.018, ta - z + 0.012, 'granit', z0=z)
        kutu_merkez(y, ((xi + xo) / 2, ys + 0.008), 0.024, 0.022, 0.005, 'tas_acik', z0=ta + 0.012)
    z += hh
# the hall: double eaves, hipped (Qin wudian)
y.bolum('Çift saçaklı salon')
kutu_merkez(y, (TC.x, TC.y), 0.31, 0.22, 0.012, 'granit', z0=ZT)
tepe = katli_kule(y, (TC.x, TC.y), 0.27, 0.18, ZT + 0.012, [(0.085, 0.06, 0.05), (0.07, 0.11, 0.055)], key_duvar='siva_krem',
                  key_direk='lake_koyu', son_irimoya=False, balkon=False, kucul=0.74, kivrim=0.45, yukari=0.025)
for sx in (-1, 1):   # ridge-end ornaments
    p = V(TC.x + sx * 0.035, TC.y, tepe)
    boru(y, [p, p + V(sx * 0.01, 0, 0.014), p + V(sx * 0.004, 0, 0.03)], 0.006, 'kiremit_koyu2', n=6, r_son=0.003)
sancak(y, TC.x + 0.19, TC.y - 0.13, ZT, boy=0.3, en=0.12, yuk=0.07, aci=0.4)
# bronze cauldrons (ding) on the terraces
for sx in (-1, 1):
    cx = TC.x + sx * 0.16
    zz = Z0 + TER[0][2]
    donel(y, (cx, TC.y - 0.26), [(0.0, zz + 0.012), (0.016, zz + 0.012), (0.02, zz + 0.026), (0.018, zz + 0.034), (0.0, zz + 0.034)], 'bronz', n=10)
    for k in range(3):
        a = TAU * k / 3
        cubuk(y, V(cx + 0.012 * math.cos(a), TC.y - 0.26 + 0.012 * math.sin(a), zz), V(cx + 0.012 * math.cos(a), TC.y - 0.26 + 0.012 * math.sin(a), zz + 0.014), 0.004, 'bronz')


# ---------------- workshop sheds ----------------
y.bolum('Atölye sundurmaları')


def sundurma(x0, x1, y0_, y1_, h=0.07, ch=0.045, key='kiremit_koyu'):
    """an open workshop shed: posts, a gable roof, a beaten floor"""
    y.yuz_yon([V(x0, y0_, Z0 + 0.002), V(x1, y0_, Z0 + 0.002), V(x1, y1_, Z0 + 0.002), V(x0, y1_, Z0 + 0.002)], 'kum_acik', Z)
    L = max(x1 - x0, y1_ - y0_)
    m = max(2, int(L / 0.09))
    for k in range(m + 1):
        for (px, py) in (((x0 + (x1 - x0) * k / m, y0_), (x0 + (x1 - x0) * k / m, y1_)) if x1 - x0 >= y1_ - y0_ else
                         ((x0, y0_ + (y1_ - y0_) * k / m), (x1, y0_ + (y1_ - y0_) * k / m))):
            kutu_merkez(y, (px, py), 0.01, 0.01, h, 'ahsap', z0=Z0)
    for (a, b) in (((x0, y0_), (x1, y0_)), ((x0, y1_), (x1, y1_))) if x1 - x0 >= y1_ - y0_ else (((x0, y0_), (x0, y1_)), ((x1, y0_), (x1, y1_))):
        cubuk(y, V(a[0], a[1], Z0 + h - 0.005), V(b[0], b[1], Z0 + h - 0.005), 0.01, 'ahsap_koyu')
    return cati_besik(y, x0, x1, y0_, y1_, Z0 + h, ch, 0.025, key, key + '2' if key == 'kiremit_koyu' else key, 0.008, 0.25, 'ahsap_koyu',
                      'ahsap', mahya_en=0.009)


for (x0, x1, y0_, y1_) in ((-0.98, -0.52, 0.28, 0.46), (-0.98, -0.52, 0.62, 0.8)):
    sundurma(x0, x1, y0_, y1_)
    # unfinished figures, moulds, a workbench under each
    for k in range(5):
        xx = x0 + 0.05 + k * 0.085
        asker(xx, (y0_ + y1_) / 2 + 0.03, Z0 + 0.002, aci=-math.pi / 2, yarim=(k % 2 == 0))
        kalip(xx + 0.04, (y0_ + y1_) / 2 - 0.045, Z0 + 0.002, aci=0.3 * k)
    kutu(y, V(x0 + 0.02, y1_ - 0.035, Z0 + 0.025), X, x1 - x0 - 0.04, 0.025, 0.004, 'ahsap_acik')
    for xx in (x0 + 0.03, x1 - 0.03):
        cubuk(y, V(xx, y1_ - 0.022, Z0), V(xx, y1_ - 0.022, Z0 + 0.025), 0.005, 'ahsap')
    for k in range(4):
        kure(y, (x0 + 0.08 + k * 0.1, y1_ - 0.022, Z0 + 0.034), 0.007, rn.choice(['kerpic', 'kerpic_koyu', 'siva_krem']), n=6, kat=3)
# clay heaps and a mixing pit between the sheds
for (cx, cy, r) in ((-0.62, 0.55, 0.04), (-0.82, 0.54, 0.032), (-0.45, 0.95, 0.04)):
    kure(y, (cx, cy, Z0 - r * 0.35), r, 'kerpic_koyu', n=10, kat=4)
y.prizma((-0.96, 0.95), 0.05, Z0, Z0 + 0.012, 'kerpic_koyu', n=12)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0125) for p in cokgen((-0.96, 0.95), 0.042, 12)], 'toprak', Z)


# ---------------- kilns ----------------
y.bolum('Fırınlar')


def firin(cx, cy, aci, r=0.1):
    """a horseshoe (mantou) kiln: a brick dome, a stoking arch with the fire in front, two chimneys at the back"""
    with parca(y, (cx, cy, 0), aci):
        pr = [(r, Z0), (r, Z0 + 0.05), (r * 0.96, Z0 + 0.08), (r * 0.82, Z0 + 0.11), (r * 0.55, Z0 + 0.135), (r * 0.25, Z0 + 0.148), (0.0, Z0 + 0.15)]
        donel(y, (0, 0), pr, 'tugla', n=16)
        silme(y, cokgen((0, 0), r, 16), Z0 + 0.05, 0.008, 0.005, 'tugla_koyu')
        # the stoking portal: a brick block in front with an arch, the fire inside
        kutu_merkez(y, (0, -r * 0.92), r * 0.7, r * 0.5, 0.07, 'tugla', z0=Z0, yuzler='sagsolust')
        y.kemerli(V(-r * 0.35, -r * 1.17), V(r * 0.35, -r * 1.17), Z0, 0.07, ('tugla', 'tugla_koyu', 'tugla_koyu', 'koyu'), v0=0.0, en=0.5,
                  ust=0.014, derin=0.03, k_say=8, cerceve=(0.006, 'tugla_koyu'))
        for i in range(3):
            y.koni((-0.01 + 0.01 * i, -r * 1.17 + 0.03 + 0.002), 0.007, Z0, 0.02 + 0.006 * (i % 2), 'boya_sari' if i % 2 else 'boya_kirmizi', n=5)
        # chimneys
        for sx in (-1, 1):
            c = (sx * r * 0.45, r * 0.85)
            kutu_merkez(y, c, 0.05, 0.05, 0.22, 'tugla', z0=Z0)
            kornis(y, c[0] - 0.025, c[0] + 0.025, c[1] - 0.025, c[1] + 0.025, Z0 + 0.21, 0.01, 0.006, 'tugla_koyu')
            y.yuz_yon([V(p.x, p.y, Z0 + 0.2205) for p in dikdortgen(c[0] - 0.016, c[0] + 0.016, c[1] - 0.016, c[1] + 0.016)], 'koyu', Z)
            for k in range(4):
                t = k / 3
                kure(y, (c[0] + 0.03 * t * t + 0.01 * sx * t, c[1] + 0.05 * t, Z0 + 0.25 + 0.12 * t), 0.018 + 0.016 * t,
                     'granit' if k < 2 else 'tas_acik', n=8, kat=4)


for (cx, cy, a) in ((0.42, -0.62, 0.0), (0.75, -0.62, 0.0), (0.88, -0.25, -math.pi / 2)):
    firin(cx, cy, a)
# firewood stacks and charcoal
for (cx, cy, a) in ((0.25, -0.88, 0.0), (0.6, -0.9, 0.0), (0.92, -0.9, 0.0)):
    with parca(y, (cx, cy, Z0), a):
        for r in range(3):
            for k in range(5 - r):
                boru(y, [V(-0.05, -0.024 + 0.012 * k + 0.006 * r, 0.006 + r * 0.0105), V(0.05, -0.024 + 0.012 * k + 0.006 * r, 0.006 + r * 0.0105)],
                     0.0058, 'ahsap' if (k + r) % 2 else 'kutuk', n=6)


# ---------------- the finished army in the yard, the ox cart ----------------
y.bolum('Avludaki boyalı askerler, kağnı')
for r in range(3):
    for k in range(7):
        x = 0.25 + k * 0.08
        asker(x, -0.02 - r * 0.06, Z0 + 0.002, aci=math.pi, boya=PAINT[(k + r) % 4] if (k + 2 * r) % 3 else None)
for k in range(3):
    at(0.3 + k * 0.1, 0.1, Z0 + 0.002, math.pi, key=KIL if k != 1 else 'kerpic_koyu')
# the ox cart
with parca(y, (-0.0, -0.62, Z0), math.pi / 2):
    kutu_merkez(y, (0, 0), 0.1, 0.05, 0.01, 'ahsap', z0=0.022)
    for sx in (-1, 1):
        pts = [V(0.0 + 0.022 * math.cos(TAU * k / 12), sx * 0.03, 0.022 + 0.022 * math.sin(TAU * k / 12)) for k in range(13)]
        boru(y, pts, 0.003, 'ahsap_koyu', n=4, kapat=False)
        for k in range(4):
            a = TAU * k / 8
            cubuk(y, V(0.022 * math.cos(a), sx * 0.03, 0.022 + 0.022 * math.sin(a)), V(-0.022 * math.cos(a), sx * 0.03, 0.022 - 0.022 * math.sin(a)),
                  0.003, 'ahsap_koyu')
    for sx in (-1, 1):
        cubuk(y, V(0.05, sx * 0.012, 0.028), V(0.12, sx * 0.008, 0.035), 0.005, 'ahsap')
    asker(0.0, 0.0, 0.032, aci=0.0, boya=('boya_yesil', 'lacivert'))
    # the ox
    boru(y, [V(0.13, 0, 0.032), V(0.17, 0, 0.034)], 0.014, 'kaya_koyu', n=8)
    boru(y, [V(0.17, 0, 0.036), V(0.19, 0, 0.03)], 0.008, 'kaya_koyu', n=6, r_son=0.006)
    for (lx, ly) in ((0.135, -0.008), (0.135, 0.008), (0.168, -0.008), (0.168, 0.008)):
        cubuk(y, V(lx, ly, 0.0), V(lx, ly, 0.026), 0.006, 'kaya_koyu')
    for sy in (-1, 1):
        boru(y, [V(0.185, sy * 0.004, 0.038), V(0.19, sy * 0.012, 0.046)], 0.0022, 'mermer', n=4, r_son=0.001)
# drying racks with heads and limbs, a well
for (cx, cy) in ((0.05, -0.32), (0.05, -0.42)):
    for xx in (-0.07, 0.07):
        for yy in (-0.012, 0.012):
            cubuk(y, V(cx + xx, cy + yy, Z0), V(cx + xx, cy + yy, Z0 + 0.04), 0.005, 'ahsap')
    for zz in (Z0 + 0.018, Z0 + 0.038):
        kutu(y, V(cx - 0.075, cy - 0.016, zz - 0.003), X, 0.15, 0.032, 0.004, 'ahsap_acik')
        for k in range(6):
            kure(y, (cx - 0.06 + k * 0.024, cy, zz + 0.006), 0.0055, KIL if (k + int(zz * 100)) % 3 else 'kerpic_koyu', n=6, kat=3)
y.prizma((0.25, -0.35), 0.02, Z0, Z0 + 0.02, 'granit', n=10)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0205) for p in cokgen((0.25, -0.35), 0.013, 10)], 'su', Z)
for s in (-1, 1):
    cubuk(y, V(0.25 + s * 0.022, -0.35, Z0), V(0.25 + s * 0.022, -0.35, Z0 + 0.05), 0.005, 'ahsap')
cubuk(y, V(0.225, -0.35, Z0 + 0.05), V(0.275, -0.35, Z0 + 0.05), 0.005, 'ahsap_koyu')
# figures being carried to the pit: a line of finished warriors along the path
for k in range(6):
    asker(-0.4 + k * 0.08, -0.16, Z0 + 0.002, aci=-math.pi / 2, boya=PAINT[k % 4] if k % 2 else None)
# workers
for (px, py, a, eg) in ((-0.7, 0.37, 0.4, 0.6), (-0.6, 0.73, 2.0, 0.0), (0.5, -0.8, 1.2, 0.5), (0.2, -0.75, 2.5, 0.0), (-0.3, -0.25, 1.0, 0.0),
                        (0.6, -0.4, 3.0, 0.0), (-0.05, -0.55, 1.6, 0.0), (0.8, 0.0, 2.2, 0.4)):
    insan(y, px, py, Z0 + 0.002, aci=a, govde=rn.choice(['kumas', 'siva_oker', 'kaya_koyu']), egik=eg)

# ---------------- the painters' hall and the storehouse at the back right ----------------
y.bolum('Boyacı salonu, ambar, ağaçlar')
salon(y, 0.6, 0.98, 0.3, 0.5, Z0, 0.075, 0.07, sacak=0.035, tur='kirma', duvar='siva_krem', direk='lake_koyu', kapi_yon=3, kaide=0.02,
      kivrim=0.4)
salon(y, 0.62, 0.98, 0.68, 0.9, Z0, 0.07, 0.065, sacak=0.03, tur='besik', duvar='kerpic', direk='ahsap_koyu', kapi_yon=3, kaide=0.012,
      kivrim=0.25, sus='kiremit_koyu2')
# paint jars outside the painters' hall
for k in range(5):
    cx, cy = 0.54, 0.33 + k * 0.035
    donel(y, (cx, cy), [(0.0, Z0), (0.008, Z0), (0.011, Z0 + 0.01), (0.007, Z0 + 0.018), (0.008, Z0 + 0.02), (0.0, Z0 + 0.02)],
          ['boya_kirmizi', 'boya_yesil', 'lacivert', 'boya_sari', 'beyaz'][k], n=8)
for (tx, ty) in ((-0.95, 0.1), (-0.4, 0.15), (0.95, 0.12), (-0.25, 0.93), (0.45, 0.93), (0.94, 0.94), (-0.95, -0.15), (0.05, 0.93)):
    agac(y, tx, ty, Z0, boy=0.13, key='boya_yesil' if tx < 0 else 'zeytin')
for (tx, ty) in ((-0.3, 0.84), (0.3, 0.86)):
    cam(y, tx, ty, Z0, boy=0.14)
# the workshop's rammed-earth enclosure, open at the front path
y.bolum('Çevre duvarı ve kapı')
WY = GY0 + 0.035
cin_duvar(y, [V(0.2, WY), V(GX1 - 0.035, WY), V(GX1 - 0.035, GY1 - 0.035), V(GX0 + 0.035, GY1 - 0.035), V(GX0 + 0.035, WY), V(-0.12, WY)],
          Z0, 0.055, t=0.02, key='kerpic', kaide='kerpic_koyu')
for x in (-0.12, 0.2):   # gate piers with lamps
    kutu_merkez(y, (x + (0.014 if x > 0 else -0.014), WY - 0.01), 0.04, 0.04, 0.085, 'kerpic_koyu', z0=Z0)
    kornis(y, x + (0.014 if x > 0 else -0.014) - 0.02, x + (0.014 if x > 0 else -0.014) + 0.02, WY - 0.03, WY + 0.01, Z0 + 0.08, 0.008, 0.006, 'granit')
    kure(y, (x + (0.014 if x > 0 else -0.014), WY - 0.01, Z0 + 0.1), 0.01, 'boya_kirmizi', n=8, kat=4)
# stacks of fired jars and tiles by the kilns
for (cx, cy) in ((0.3, -0.42), (0.95, -0.5), (0.58, -0.35)):
    for k in range(3):
        for j in range(3 - k):
            donel(y, (cx + (j - (2 - k) / 2) * 0.022, cy), [(0.0, Z0 + k * 0.02), (0.007, Z0 + k * 0.02), (0.011, Z0 + k * 0.02 + 0.01),
                                                            (0.006, Z0 + k * 0.02 + 0.019), (0.0, Z0 + k * 0.02 + 0.019)], 'kiremit', n=8)

calistir(y, 'lm_topraksavasci')
