# Çin Seddi Kalesi (lm_seddkalesi): a Ming pass fortress in the manner of Jiayuguan: a rammed-earth enclosure with a
# brick-faced gate under a three-storey timber gate tower, a barbican with a side gate, corner kiosks, barracks and a
# yamen inside; from its flanks the Great Wall climbs two mountain ridges with stepped walkways, merlons and two-storey
# brick watchtowers, and on the hill behind a beacon tower sends up smoke.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ortak import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(5)
Z0 = 0.04
SED, SED2 = 'granit', 'granit_koyu'      # Ming grey brick
TOP = 'kerpic'                           # rammed earth (Jiayuguan)
FX0, FX1, FY0, FY1 = -0.4, 0.4, -0.6, 0.1
BX0, BX1, BY0 = -0.25, 0.25, -0.93
WH = 0.16

# ---------------- the terrain: two ridges flanking the pass, a hill behind ----------------
SOL = [(-0.6, 1.02, 0.3), (-0.8, 0.84, 0.4), (-0.95, 0.56, 0.46), (-1.0, 0.25, 0.36), (-0.93, -0.03, 0.22), (-0.76, -0.2, 0.12),
       (-0.58, -0.27, 0.05), (-0.395, -0.28, 0.0)]
SAG = [(0.395, -0.28, 0.0), (0.58, -0.26, 0.05), (0.78, -0.14, 0.14), (0.96, 0.08, 0.27), (1.02, 0.35, 0.38), (0.93, 0.62, 0.44),
       (0.74, 0.85, 0.36), (0.52, 1.02, 0.3)]
BEACON = (0.08, 0.8)


def _sirt(px, py, yol, s=0.26):
    best = 0.0
    for i in range(len(yol) - 1):
        ax, ay, ah = yol[i]; bx, by, bh = yol[i + 1]
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
        qx, qy = ax + dx * t, ay + dy * t
        d2 = (px - qx) ** 2 + (py - qy) ** 2
        best = max(best, (ah + (bh - ah) * t) * math.exp(-d2 / (s * s)))
    return best


def yuk(px, py):
    """ground height"""
    h = max(_sirt(px, py, SOL), _sirt(px, py, SAG))
    # the back range joining the ridges, and the beacon hill
    h = max(h, 0.26 * math.exp(-((px / 0.75) ** 2 + ((py - 1.15) / 0.3) ** 2)))
    h = max(h, 0.33 * math.exp(-(((px - BEACON[0]) / 0.22) ** 2 + ((py - BEACON[1]) / 0.2) ** 2)))
    # keep the pass flat round the fortress and the barbican
    dx = max(0.0, abs(px) - 0.5); dy = max(0.0, py - 0.2, -0.95 - py)
    d = math.hypot(dx, dy)
    m = min(1.0, d / 0.16)
    m = m * m * (3 - 2 * m)
    h *= m
    # broken rock
    h += 0.018 * min(1.0, h / 0.08) * math.sin(9 * px + 3 * py) * math.cos(7 * py - 4 * px)
    return Z0 + h


y.bolum('Dağlar ve geçit')
GX0, GX1, GY0, GY1 = -1.18, 1.18, -1.1, 1.14
NX, NY = 34, 32
P = [[V(GX0 + (GX1 - GX0) * i / NX, GY0 + (GY1 - GY0) * j / NY, 0) for j in range(NY + 1)] for i in range(NX + 1)]
for i in range(NX + 1):
    for j in range(NY + 1):
        P[i][j].z = yuk(P[i][j].x, P[i][j].y)
# (one key for the whole terrain: its colour comes per corner from arazi_renk, so the tones flow smoothly across the
#  triangles: meadow in the pass, scrub on the lower slopes, bare rock on the ridges and the steep faces)
import doku


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def arazi_renk(x, yy, z):
    e = 0.012
    gx = (yuk(x + e, yy) - yuk(x - e, yy)) / (2 * e)
    gy = (yuk(x, yy + e) - yuk(x, yy - e)) / (2 * e)
    s = math.hypot(gx, gy)
    h = z - Z0
    # broad soft patches (a regional tone), never per triangle
    n1 = math.sin(x * 4.3 + 1.1) * math.cos(yy * 3.7 - 0.6)
    n2 = math.sin(x * 9.1 - yy * 6.3 + 2.0)
    n = n1 * 0.7 + n2 * 0.3
    c = _mix((0.42, 0.50, 0.26), (0.50, 0.52, 0.30), 0.5 + 0.5 * n)                                   # meadow, greener / drier
    c = _mix(c, (0.56, 0.50, 0.33), _ss(0.02, 0.13, h + 0.03 * n))                                    # scrub on the lower slopes
    c = _mix(c, (0.67, 0.61, 0.52), max(_ss(0.6, 1.2, s + 0.25 * n), _ss(0.2, 0.36, h + 0.05 * n)))   # bare rock
    c = _mix(c, (0.56, 0.50, 0.43), 0.7 * _ss(1.15, 1.9, s + 0.3 * n2))                              # dark crags, the steepest
    return c


doku.KOSE_RENK['toprak_ot'] = arazi_renk
for i in range(NX):
    for j in range(NY):
        dg = (i + j) % 2 == 0
        for tri in (([P[i][j], P[i + 1][j], P[i + 1][j + 1]], [P[i][j], P[i + 1][j + 1], P[i][j + 1]]) if dg else
                    ([P[i][j], P[i + 1][j], P[i][j + 1]], [P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]])):
            y.yuz(tri, 'toprak_ot')
# the skirt round the edge: the soil under the turf, then strata of rock
kenar = [P[i][0] for i in range(NX)] + [P[NX][j] for j in range(NY)] + [P[i][NY] for i in range(NX, 0, -1)] + [P[0][j] for j in range(NY, 0, -1)]
for k in range(len(kenar)):
    a, b = kenar[k], kenar[(k + 1) % len(kenar)]
    e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
    za, zb_ = a.z - 0.022, b.z - 0.022
    y.yuz_yon([V(a.x, a.y, za), V(b.x, b.y, zb_), b, a], 'toprak', nn)
    # (rock layers whose boundary wavers, thinner towards the top)
    sa = 0.012 * math.sin(a.x * 7 + a.y * 5)
    sb = 0.012 * math.sin(b.x * 7 + b.y * 5)
    m1a, m1b = min(za, 0.024 + sa), min(zb_, 0.024 + sb)
    m2a, m2b = min(za, 0.15 - sa * 1.5), min(zb_, 0.15 - sb * 1.5)
    y.yuz_yon([V(a.x, a.y, m2a), V(b.x, b.y, m2b), V(b.x, b.y, zb_), V(a.x, a.y, za)], 'kaya_koyu', nn)
    y.yuz_yon([V(a.x, a.y, m1a), V(b.x, b.y, m1b), V(b.x, b.y, m2b), V(a.x, a.y, m2a)], 'kaya', nn)
    y.yuz_yon([V(a.x, a.y, 0), V(b.x, b.y, 0), V(b.x, b.y, m1b), V(a.x, a.y, m1a)], 'kaya_koyu', nn)


# ---------------- the Great Wall along a ridge ----------------
def ornekle(yol, adim=0.022):
    pts = []
    for i in range(len(yol) - 1):
        a, b = V(yol[i][0], yol[i][1]), V(yol[i + 1][0], yol[i + 1][1])
        n = max(1, int(math.ceil((b - a).length / adim)))
        for k in range(n):
            pts.append(a.lerp(b, k / n))
    pts.append(V(yol[-1][0], yol[-1][1]))
    return pts


def sed(yol, W=0.075, HW=0.085, P_=0.026, M=0.022, t=0.013, t2=0.01, s=0.011):
    """the wall along the polyline yol (outer face to the right of travel): battered-free brick faces from below the
    ground, a stepped walkway, the outer parapet with merlons and a low inner parapet. Returns the samples and their
    walkway heights"""
    O = ornekle(yol)
    n = len(O)
    I = disa(O, -W, kapali=False)
    Op = disa(O, -t, kapali=False)
    Ip = disa(O, -(W - t2), kapali=False)
    zg = [yuk(p.x, p.y) for p in O]
    zr = []
    for k in range(n):   # a smoothed ridge line
        ks = range(max(0, k - 2), min(n, k + 3))
        zr.append(sum(zg[j] for j in ks) / len(ks))
    zt = [z + HW for z in zr]
    # (each face's foot a little below the ground at its own corners, shared with the neighbour: a deep common foot left
    #  dark baked-shadow wedges up the face)
    zb = [yuk(p.x, p.y) - 0.025 for p in O]
    zbi = [yuk(p.x, p.y) - 0.025 for p in I]
    zq = [round(((zt[k] + zt[k + 1]) / 2) / s) * s for k in range(n - 1)]   # the walkway's step levels
    for k in range(n - 1):
        j = k + 1
        nrm = V((O[j] - O[k]).y, -(O[j] - O[k]).x).normalized()
        # outer face (to the parapet top), inner face (to the low parapet top)
        # (in bands: the shadow baked at the merlons' feet stays in the parapet band instead of running down the whole face
        #  in long dark wedges)
        for (ha, hb) in ((zb, [z + 0.03 for z in zg]), ([z + 0.03 for z in zg], [z - 0.006 for z in zt]), ([z - 0.006 for z in zt], [z + P_ for z in zt])):
            y.yuz_yon([V(O[k].x, O[k].y, ha[k]), V(O[j].x, O[j].y, ha[j]), V(O[j].x, O[j].y, hb[j]), V(O[k].x, O[k].y, hb[k])], SED, nrm)
        mi = [min(zbi[q] + 0.055, zt[q]) for q in range(n)]
        for (ha, hb) in ((zbi, mi), (mi, [z + 0.014 for z in zt])):
            y.yuz_yon([V(I[j].x, I[j].y, ha[j]), V(I[k].x, I[k].y, ha[k]), V(I[k].x, I[k].y, hb[k]), V(I[j].x, I[j].y, hb[j])], SED, -nrm)
        # the dressed-stone footing courses and the brick string course at the walkway level (outer face, a little proud)
        Ok, Oj = O[k] + nrm * 0.004, O[j] + nrm * 0.004
        y.yuz_yon([V(Ok.x, Ok.y, zb[k]), V(Oj.x, Oj.y, zb[j]), V(Oj.x, Oj.y, zg[j] + 0.03), V(Ok.x, Ok.y, zg[k] + 0.03)], 'tas', nrm)
        y.yuz_yon([V(Ok.x, Ok.y, zg[k] + 0.03), V(Oj.x, Oj.y, zg[j] + 0.03), V(O[j].x, O[j].y, zg[j] + 0.03), V(O[k].x, O[k].y, zg[k] + 0.03)], 'tas', Z)
        Ok, Oj = O[k] + nrm * 0.003, O[j] + nrm * 0.003
        y.yuz_yon([V(Ok.x, Ok.y, zt[k] - 0.006), V(Oj.x, Oj.y, zt[j] - 0.006), V(Oj.x, Oj.y, zt[j]), V(Ok.x, Ok.y, zt[k])], SED2, nrm)
        y.yuz_yon([V(Ok.x, Ok.y, zt[k]), V(Oj.x, Oj.y, zt[j]), V(O[j].x, O[j].y, zt[j]), V(O[k].x, O[k].y, zt[k])], SED2, Z)
        y.yuz_yon([V(O[k].x, O[k].y, zt[k] - 0.006), V(O[j].x, O[j].y, zt[j] - 0.006), V(Oj.x, Oj.y, zt[j] - 0.006), V(Ok.x, Ok.y, zt[k] - 0.006)], SED2, -Z)
        # parapet tops
        y.yuz_yon([V(O[k].x, O[k].y, zt[k] + P_), V(O[j].x, O[j].y, zt[j] + P_), V(Op[j].x, Op[j].y, zt[j] + P_), V(Op[k].x, Op[k].y, zt[k] + P_)], SED2, Z)
        y.yuz_yon([V(Ip[k].x, Ip[k].y, zt[k] + 0.014), V(Ip[j].x, Ip[j].y, zt[j] + 0.014), V(I[j].x, I[j].y, zt[j] + 0.014), V(I[k].x, I[k].y, zt[k] + 0.014)], SED2, Z)
        # the walkway tread and the parapets' walkway-facing sides
        q = zq[k]
        y.yuz_yon([V(Op[k].x, Op[k].y, q), V(Op[j].x, Op[j].y, q), V(Ip[j].x, Ip[j].y, q), V(Ip[k].x, Ip[k].y, q)], 'zemin', Z)
        y.yuz_yon([V(Op[j].x, Op[j].y, q), V(Op[k].x, Op[k].y, q), V(Op[k].x, Op[k].y, zt[k] + P_), V(Op[j].x, Op[j].y, zt[j] + P_)], SED, -nrm)
        y.yuz_yon([V(Ip[k].x, Ip[k].y, q), V(Ip[j].x, Ip[j].y, q), V(Ip[j].x, Ip[j].y, zt[j] + 0.014), V(Ip[k].x, Ip[k].y, zt[k] + 0.014)], SED, nrm)
        # the riser up to the next tread
        if k < n - 2 and abs(zq[k + 1] - q) > 1e-6:
            lo, hi = min(q, zq[k + 1]), max(q, zq[k + 1])
            yon = (O[k] - O[j]) if zq[k + 1] > q else (O[j] - O[k])
            y.yuz_yon([V(Op[j].x, Op[j].y, lo), V(Ip[j].x, Ip[j].y, lo), V(Ip[j].x, Ip[j].y, hi), V(Op[j].x, Op[j].y, hi)], 'tas_koyu', yon)
    # merlons on the outer parapet, each with a small embrasure slit
    L_tum = sum((O[k + 1] - O[k]).length for k in range(n - 1))
    adim, mw = 0.042, 0.026
    u = 0.012
    while u + mw < L_tum - 0.01:
        # find the sample segment
        acc = 0.0
        for k in range(n - 1):
            sl = (O[k + 1] - O[k]).length
            if acc + sl >= u: break
            acc += sl
        tt = (u - acc) / sl
        e = (O[k + 1] - O[k]).normalized()
        p0 = O[k].lerp(O[k + 1], tt)
        za = zt[k] + (zt[k + 1] - zt[k]) * tt + P_
        ze = za + (zt[min(k + 2, n - 1)] - zt[k]) / max(1e-6, (O[min(k + 2, n - 1)] - O[k]).length) * mw
        kutu(y, p0 + Z * (min(za, ze) - 0.004), e, mw, t, M + abs(ze - za) * 0.5 + 0.004, SED)
        u += adim
    # end caps
    for k, j, q in ((0, 1, zq[0]), (n - 1, n - 2, zq[-1])):
        y.yuz_yon([V(O[k].x, O[k].y, zb[k]), V(I[k].x, I[k].y, zbi[k]), V(I[k].x, I[k].y, zt[k] + 0.014), V(Ip[k].x, Ip[k].y, zt[k] + 0.014),
                   V(Ip[k].x, Ip[k].y, q), V(Op[k].x, Op[k].y, q), V(Op[k].x, Op[k].y, zt[k] + P_), V(O[k].x, O[k].y, zt[k] + P_)], SED, O[k] - O[j])
    return O, zt, zq


def gozcu(c, aci, w=0.15, sancakli=False):
    """a Ming watchtower astride the wall: a solid brick base from below the ground, a storey with arched windows, a
    cornice, a merloned deck and a small tiled guard room. Returns its top z"""
    zg = min(yuk(c.x + sx * w / 2, c.y + sy * w / 2) for sx in (-1, 0, 1) for sy in (-1, 0, 1))
    zc = yuk(c.x, c.y)
    zw = zc + 0.085
    H1 = 0.1
    with parca(y, (c.x, c.y, 0), aci):
        k = dikdortgen(-w / 2, w / 2, -w / 2, w / 2)
        duvarlar(y, k, zg - 0.05, zw, SED)
        kornis(y, -w / 2, w / 2, -w / 2, w / 2, zw - 0.004, 0.008, 0.004, SED2)
        pencereli_duvar(y, k, zw + 0.004, H1, [3, 3, 3, 3], renk=(SED, SED2, SED2, 'koyu'), v0=0.02, en=0.42, ust=0.02, derin=0.014,
                        k_say=6, sivri=0.0, cerceve=(0.004, 'tas_acik'))
        duvarlar(y, k, zw, zw + 0.004, SED)
        zt = zw + 0.004 + H1
        konsol_halka(y, k, zt - 0.012, 0.012, 0.008, SED2, 2)
        kd = disa(k, 0.008)
        y.yuz_yon([V(p.x, p.y, zt) for p in kd], 'zemin', Z)
        parapet(y, kd, zt, 0.014, 0.022, 0.012, SED, ust_key=SED2)
        # the guard room
        r0 = w * 0.26
        # (the door wall is one bay with its opening: a door drawn over a plain wall face lay in the same plane)
        gk = dikdortgen(-r0, r0, -r0 * 0.8, r0 * 0.8)
        dikdortgen_acik(y, gk[0], gk[1], zt, 0.045, 0.35, 0.65, 0.0, 0.032, (SED, SED2, SED2, 'ahsap_koyu'), derin=0.006)
        for i in (1, 2, 3):
            duz_duvar(y, gk[i], gk[(i + 1) % 4], zt, zt + 0.045, SED)
        tepe = cati_besik(y, -r0, r0, -r0 * 0.8, r0 * 0.8, zt + 0.045, 0.035, 0.014, 'kiremit_koyu', 'kiremit_koyu2', 0.006, 0.35,
                          'ahsap_koyu', SED, sus=None, mahya_en=0.008)
        # small ridge-end ornaments in scale with the little roof (the library's are sized for a hall)
        for sx in (-1, 1):
            p = V(sx * (r0 + 0.014), 0, tepe - 0.004)
            boru(y, [p, p + V(sx * 0.005, 0, 0.006), p + V(sx * 0.006, 0, 0.014), p + V(sx * 0.001, 0, 0.019)], 0.004, 'kiremit_koyu2', n=6,
                 r_son=0.0018)
    if sancakli:
        sancak(y, c.x + w * 0.4, c.y + w * 0.4, zt + 0.014, boy=0.16, en=0.09, yuk=0.055, aci=0.6)
    return tepe


y.bolum('Sed: sol sırt')
O_sol, zt_sol, _ = sed(SOL)
y.bolum('Sed: sağ sırt')
O_sag, zt_sag, _ = sed(SAG)

y.bolum('Gözcü kuleleri')
for O_, idx in ((O_sol, (0.42, 0.66)), (O_sag, (0.42, 0.72))):
    for f in idx:
        k = int(len(O_) * f)
        e = (O_[k + 1] - O_[k - 1]).normalized()
        gozcu(O_[k], math.atan2(e.y, e.x), sancakli=(f == idx[1]))
# the wall's far ends stop at a tower each
for O_, k, j in ((O_sol, 1, 0), (O_sag, len(O_sag) - 2, len(O_sag) - 1)):
    e = (O_[j] - O_[k]).normalized()
    gozcu(O_[j] - e * 0.05, math.atan2(e.y, e.x))


# ---------------- the fortress ----------------
y.bolum('Kale avlusu ve surlar')
# the yard
y.yuz_yon([V(FX0 + 0.05, FY0 + 0.05, Z0 + 0.004), V(FX1 - 0.05, FY0 + 0.05, Z0 + 0.004), V(FX1 - 0.05, FY1 - 0.05, Z0 + 0.004),
           V(FX0 + 0.05, FY1 - 0.05, Z0 + 0.004)], 'zemin', Z)
sur(y, [V(0.17, FY0), V(FX1, FY0), V(FX1, FY1), V(0.14, FY1)], Z0 - 0.01, WH + 0.01, kalinlik=0.06, key=TOP, mazgal_h=0.024,
    parapet_h=0.014, ust_key='zemin')
sur(y, [V(-0.14, FY1), V(FX0, FY1), V(FX0, FY0), V(-0.17, FY0)], Z0 - 0.01, WH + 0.01, kalinlik=0.06, key=TOP, mazgal_h=0.024,
    parapet_h=0.014, ust_key='zemin')
# rammed-earth lifts: thin darker lines along the faces
for a, b in ((V(FX0, FY0), V(-0.17, FY0)), (V(0.17, FY0), V(FX1, FY0)), (V(FX1, FY0), V(FX1, FY1)), (V(FX0, FY1), V(FX0, FY0)),
             (V(FX1, FY1), V(0.14, FY1)), (V(-0.14, FY1), V(FX0, FY1)),
             (V(BX0, FY0 - 0.1), V(BX0, -0.715)), (V(BX0, -0.845), V(BX0, BY0)), (V(BX0, BY0), V(BX1, BY0)), (V(BX1, BY0), V(BX1, FY0 - 0.1))):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    hmax = WH - 0.02 if a.y < FY0 - 0.05 or b.y < FY0 - 0.05 else WH
    # a brick coping band under the merlons, drain spouts
    kutu(y, a + nn * 0.003 + Z * (Z0 - 0.01 + hmax + 0.01 - 0.022), e, (b - a).length, 0.003, 0.022, SED, 'onust')
    m = int((b - a).length / 0.13)
    for k in range(m):
        p = a.lerp(b, (k + 0.5) / m)
        kutu(y, p - e * 0.004 + nn * 0.003 + Z * (Z0 - 0.01 + hmax + 0.01 - 0.03), e, 0.008, 0.012, 0.006, SED2, 'onsagsolust')
# brick courses at the foot of the earth walls
for a, b in ((V(FX0, FY0), V(-0.17, FY0)), (V(0.17, FY0), V(FX1, FY0)), (V(FX1, FY0), V(FX1, FY1)), (V(FX0, FY1), V(FX0, FY0)),
             (V(FX1, FY1), V(0.14, FY1)), (V(-0.14, FY1), V(FX0, FY1)),
             (V(BX0, FY0 - 0.1), V(BX0, -0.715)), (V(BX0, -0.845), V(BX0, BY0)), (V(BX0, BY0), V(BX1, BY0)), (V(BX1, BY0), V(BX1, FY0 - 0.1))):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    kutu(y, a + nn * 0.004 + Z * (Z0 - 0.01), e, (b - a).length, 0.004, 0.04, SED, 'onust')
    # the rammed-earth lifts: thin darker seams where each layer of the formwork was struck
    hmax = WH - 0.02 if a.y < FY0 - 0.05 or b.y < FY0 - 0.05 else WH
    for zz in [Z0 + 0.058 + 0.03 * i for i in range(5)]:
        if zz > Z0 + hmax - 0.036: break
        kutu(y, a + nn * 0.0025 + Z * zz, e, (b - a).length, 0.0025, 0.0035, 'kerpic_koyu', 'onust')

y.bolum('Ana kapı ve üç katlı kapı kulesi')
GH = 0.19
kale_kapisi(y, 0, FY0, 0.34, Z0 - 0.01, GH, derin=0.22, key=SED, kule=None, kapi_key='lake_koyu')
zk = Z0 - 0.01 + GH
kutu_merkez(y, (0, FY0), 0.27, 0.17, 0.012, 'tas_acik', z0=zk)
tepe_g = katli_kule(y, (0, FY0), 0.24, 0.14, zk + 0.012, [(0.08, 0.05, 0.045), (0.07, 0.045, 0.04), (0.065, 0.07, 0.045)],
                    key_duvar='lake', key_direk='lake', sus='kiremit_koyu2')
for sx in (-1, 1):
    sancak(y, sx * 0.158, FY0 - 0.098, zk, boy=0.21, en=0.1, yuk=0.06, aci=(math.pi + 0.25 if sx < 0 else -0.25))
# a name plaque over the gate
kutu(y, V(-0.04, FY0 - 0.11 - 0.004, Z0 + 0.12), X, 0.08, 0.004, 0.026, 'lake_koyu', 'onsagsolust')
kutu(y, V(-0.032, FY0 - 0.11 - 0.0065, Z0 + 0.125), X, 0.064, 0.003, 0.016, 'altin', 'onsagsolust')

y.bolum('Arka kapı ve kulesi')
with parca(y, (0, FY1, 0), math.pi):
    kale_kapisi(y, 0, 0, 0.28, Z0 - 0.01, GH - 0.01, derin=0.2, key=SED, kule=None, kapi_key='lake_koyu')
    zk2 = Z0 - 0.02 + GH
    kutu_merkez(y, (0, 0), 0.22, 0.15, 0.012, 'tas_acik', z0=zk2)
    katli_kule(y, (0, 0), 0.2, 0.12, zk2 + 0.012, [(0.075, 0.045, 0.04), (0.065, 0.065, 0.04)], sus='kiremit_koyu2')

y.bolum('Köşe köşkleri')
for (cx, cy) in ((FX0, FY0), (FX1, FY0), (FX0, FY1), (FX1, FY1)):
    # (the bastion rises clear of the curtain walls' merlons: they used to poke up through its deck beside the kiosk)
    kutu_merkez(y, (cx, cy), 0.1, 0.1, WH + 0.062, SED, z0=Z0 - 0.01)
    kornis(y, cx - 0.05, cx + 0.05, cy - 0.05, cy + 0.05, Z0 + WH + 0.04, 0.008, 0.006, SED2)
    kd = dikdortgen(cx - 0.05, cx + 0.05, cy - 0.05, cy + 0.05)
    parapet(y, kd, Z0 + WH + 0.052, 0.008, 0.012, 0.008, SED, ust_key=SED2)
    salon(y, cx - 0.021, cx + 0.021, cy - 0.021, cy + 0.021, Z0 + WH + 0.052, 0.042, 0.042, sacak=0.022, kaide=0.006,
          tur='kirma', kivrim=0.5, yukari=0.02, basamak=False)

y.bolum('Barbakan (dış avlu) ve yan kapısı')
BX0, BX1, BY0 = -0.25, 0.25, -0.93
sur(y, [V(BX0, FY0 - 0.1), V(BX0, -0.715)], Z0 - 0.01, WH - 0.02, kalinlik=0.055, key=TOP, mazgal_h=0.022, parapet_h=0.012)
sur(y, [V(BX0, -0.845), V(BX0, BY0), V(BX1, BY0), V(BX1, FY0 - 0.1)], Z0 - 0.01, WH - 0.02, kalinlik=0.055, key=TOP, mazgal_h=0.022,
    parapet_h=0.012)
with parca(y, (BX0 + 0.0, -0.78, 0), -math.pi / 2):
    kale_kapisi(y, 0, 0.0, 0.16, Z0 - 0.01, WH - 0.005, derin=0.1, key=SED, kule=None, kapi_key='lake_koyu')
    salon(y, -0.05, 0.05, -0.03, 0.03, Z0 + WH - 0.015, 0.05, 0.045, sacak=0.025, kaide=0.006, tur='irimoya', basamak=False, kapi_yon=0)
y.yuz_yon([V(BX0 + 0.05, BY0 + 0.05, Z0 + 0.004), V(BX1 - 0.05, BY0 + 0.05, Z0 + 0.004), V(BX1 - 0.05, FY0 - 0.12, Z0 + 0.004),
           V(BX0 + 0.05, FY0 - 0.12, Z0 + 0.004)], 'zemin', Z)
# the road out of the side gate
yol = [V(BX0 - 0.06, -0.78), V(-0.45, -0.82), V(-0.7, -0.95), V(-0.9, -1.1)]
for i in range(len(yol) - 1):
    a, b = yol[i], yol[i + 1]
    e = (b - a).normalized(); nn = V(-e.y, e.x) * 0.045
    y.yuz_yon([a - nn + Z * (Z0 + 0.003), b - nn + Z * (Z0 + 0.003), b + nn + Z * (Z0 + 0.003), a + nn + Z * (Z0 + 0.003)], 'toprak', Z)

# the road on through the rear gate, up the pass
yol = [V(0, FY1 + 0.1), V(0.0, 0.3), V(-0.12, 0.45), V(-0.3, 0.6)]
for i in range(len(yol) - 1):
    a, b = yol[i], yol[i + 1]
    e = (b - a).normalized(); nn = V(-e.y, e.x) * 0.04
    pts = [a - nn, b - nn, b + nn, a + nn]
    y.yuz_yon([V(p.x, p.y, yuk(p.x, p.y) + 0.004) for p in pts], 'toprak', Z)
# boulders on the slopes
for k in range(26):
    bx, by = rn.uniform(-1.1, 1.1), rn.uniform(-0.6, 1.08)
    if abs(bx) < 0.55 and by < 0.25: continue
    hz = yuk(bx, by)
    if hz - Z0 < 0.04: continue
    r = rn.uniform(0.014, 0.03)
    kure(y, (bx, by, hz + r * 0.2), r, rn.choice(['kaya', 'kaya_koyu']), n=7, kat=4)
y.bolum('Avludaki yapılar')
salon(y, -0.1, 0.1, -0.12, 0.0, Z0 + 0.004, 0.065, 0.07, sacak=0.035, tur='irimoya', sus='kiremit_koyu2')
for sx in (-1, 1):
    x0 = sx * 0.3
    salon(y, x0 - 0.04, x0 + 0.04, -0.46, -0.16, Z0 + 0.004, 0.05, 0.05, sacak=0.025, tur='besik', duvar='siva', kapi_yon=(1 if sx < 0 else 3),
          kaide=0.012)
# a well and two trees
y.prizma((0.0, -0.3), 0.018, Z0 + 0.004, Z0 + 0.02, SED, n=10)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0205) for p in cokgen((0.0, -0.3), 0.012, 10)], 'su', Z)
for (tx, ty) in ((-0.2, -0.42), (0.21, -0.05)):
    agac(y, tx, ty, Z0 + 0.004, boy=0.1, key='zeytin')

y.bolum('İşaret kulesi ve duman')
bz = yuk(*BEACON)
bg = min(yuk(BEACON[0] + sx * 0.07, BEACON[1] + sy * 0.07) for sx in (-1, 1) for sy in (-1, 1))
pr = [(0.075, bg - 0.04), (0.075, bz + 0.01), (0.056, bz + 0.17)]
donel(y, BEACON, pr, TOP, n=4, kat=math.pi / 4)
# the rammed-earth lifts: thin proud seams round the battered shaft, the lowest one a brick footing
for k, zz in enumerate((bz + 0.012, bz + 0.05, bz + 0.09, bz + 0.13)):
    rz = lambda z_: 0.075 + (0.056 - 0.075) * max(0.0, (z_ - bz - 0.01) / 0.16)
    zz0 = bg - 0.01 if k == 0 else zz
    hh = bz + 0.006 - zz0 if k == 0 else 0.004
    donel(y, BEACON, [(rz(zz0) - 0.001, zz0), (rz(zz0) + 0.003, zz0), (rz(zz0 + hh) + 0.003, zz0 + hh), (rz(zz0 + hh) - 0.001, zz0 + hh)],
          SED if k == 0 else 'kerpic_koyu', n=4, kat=math.pi / 4)
kb = cokgen(BEACON, 0.056, 4, math.pi / 4)
y.yuz_yon([V(p.x, p.y, bz + 0.17) for p in kb], 'zemin', Z)
parapet(y, kb, bz + 0.17, 0.012, 0.02, 0.01, SED)
# the fire and the smoke column drifting with the wind
y.prizma(BEACON, 0.018, bz + 0.17, bz + 0.19, SED2, n=8)
rs = random.Random(3)
for k in range(10):
    t = k / 9
    c = V(BEACON[0] + 0.16 * t * t, BEACON[1] + 0.05 * t)
    r = 0.02 + 0.03 * t
    for m in range(2 if k < 3 else 3):
        a = rs.uniform(0, TAU)
        o = V(math.cos(a), math.sin(a)) * r * 0.55
        kure(y, (c.x + o.x, c.y + o.y, bz + 0.22 + 0.4 * t + rs.uniform(-0.01, 0.01)), r * rs.uniform(0.75, 1.05),
             ('granit' if t < 0.3 else 'tas_acik') if m % 2 else ('tas_acik' if t < 0.5 else 'beyaz'), n=10, kat=5)
# the fire in its brazier
for i in range(5):
    a = TAU * i / 5
    y.koni((BEACON[0] + 0.008 * math.cos(a), BEACON[1] + 0.008 * math.sin(a)), 0.009, bz + 0.19, 0.03, 'boya_kirmizi' if i % 2 else 'boya_sari', n=6)
y.koni(BEACON, 0.012, bz + 0.19, 0.045, 'boya_sari', n=6)
# pines on the slopes
for (tx, ty) in ((0.3, 0.55), (-0.25, 0.6), (-0.55, 0.42), (0.55, 0.38), (-0.35, 0.85), (0.32, 0.92), (-0.7, 0.18),
                 (0.7, 0.2), (-1.05, -0.4), (1.05, -0.3), (-0.82, 0.72), (0.82, 0.78), (-0.12, 0.42), (0.22, 0.3)):
    cam(y, tx, ty, yuk(tx, ty), boy=0.11 + rn.uniform(0, 0.05))

calistir(y, 'lm_seddkalesi')
