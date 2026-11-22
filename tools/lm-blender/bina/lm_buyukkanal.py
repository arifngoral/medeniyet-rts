# Büyük Kanal Limanı (lm_buyukkanal): a Grand Canal port in the manner of Tongzhou / Hangzhou: the stone-walled canal
# with a lock (two piers, a plank gate, a windlass gantry, the water a step higher above it), a high three-arched humpback
# bridge (Gongchen type) with stepped deck and balustrades, junks with battened lug sails, quays with warehouses, a
# treadmill crane and cargo, the walled customs house, a waterside pavilion with a curved roof, willows, and on the far
# bank the octagonal dense-eave Randeng pagoda that marked the canal's northern end.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ortak import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(4)
Z0 = 0.05
CY0, CY1 = -0.25, 0.19            # the canal's walls
CM = (CY0 + CY1) / 2
ZW = Z0 - 0.04                    # water below the lock
ZW2 = ZW + 0.016                  # above it
LX = 0.5                          # the lock
GX0, GX1, GY0, GY1 = -1.15, 1.15, -1.12, 1.12
TAS = 'granit'

# ---------------- ground, canal, water ----------------
y.bolum('Rıhtımlar ve kanal')
for (y0_, y1_, ust) in ((GY0, CY0, 'zemin'), (CY1, GY1, 'cimen_kuru')):
    kutu(y, V(GX0, y0_, 0), X, GX1 - GX0, y1_ - y0_, Z0, 'kaya_koyu', 'onarkasagsol')
    y.yuz_yon([V(GX0, y0_, Z0), V(GX1, y0_, Z0), V(GX1, y1_, Z0), V(GX0, y1_, Z0)], ust, Z)
# (the canal walls: the slabs' canal-facing faces are kaya_koyu; a stone revetment just in front of them)
for yy, s in ((CY0, 1), (CY1, -1)):
    a_, b_ = (V(GX1, yy + 0.003), V(GX0, yy + 0.003)) if s > 0 else (V(GX0, yy - 0.003), V(GX1, yy - 0.003))
    duz_duvar(y, a_, b_, ZW - 0.012, Z0, TAS)
    # coping stones
    kutu(y, V(GX0, yy + s * 0.012, Z0), X, GX1 - GX0, -s * 0.028, 0.008, 'tas_acik', 'onarkasagsolust')
# the canal bed under the water and the water surfaces (a step at the lock)
kutu(y, V(GX0, CY0, 0), X, GX1 - GX0, CY1 - CY0, ZW - 0.012, 'kaya_koyu', 'sagsol')
for (x0, x1, zw) in ((GX0, LX, ZW), (LX, GX1, ZW2)):
    y.yuz_yon([V(x0, CY0, zw), V(x1, CY0, zw), V(x1, CY1, zw), V(x0, CY1, zw)], 'su', Z)
for x, zw, s in ((GX0, ZW, -1), (GX1, ZW2, 1)):
    y.yuz_yon([V(x, CY0, ZW - 0.012), V(x, CY1, ZW - 0.012), V(x, CY1, zw), V(x, CY0, zw)], 'su', V(s, 0, 0))
y.yuz_yon([V(LX, CY0, ZW), V(LX, CY1, ZW), V(LX, CY1, ZW2), V(LX, CY0, ZW2)], 'su', -X)
# water steps (a landing stair down to the water) on both quays
for (sx, yy, s) in ((-0.78, CY0, 1), (0.05, CY1, -1)):
    for k in range(4):
        zz = Z0 - (Z0 - ZW) * (k + 1) / 5
        d = 0.02 * (k + 1)
        kutu(y, V(sx, yy + s * 0.0, ZW - 0.01), X, 0.16, s * min(d, 0.07), zz - ZW + 0.01 + 0.0, 'tas_acik' if k % 2 else TAS,
             'onarkasagsolust')


# ---------------- the humpback bridge ----------------
y.bolum('Üç kemerli kambur köprü')
BX = -0.3
BW = 0.13                           # width
BY0, BY1 = CM - 0.46, CM + 0.46     # deck ends on the quays
KEMER = [(CM, 0.105), (CM - 0.172, 0.042), (CM + 0.172, 0.042)]
ZS = ZW - 0.002                     # the springing


def deck(yy):
    t = (yy - CM) / (BY1 - CM)
    return Z0 + 0.145 * max(0.0, math.cos(math.pi / 2 * min(1.0, abs(t)))) ** 0.85


def alt(yy):
    for (c, r) in KEMER:
        if abs(yy - c) < r:
            return ZS + math.sqrt(r * r - (yy - c) ** 2)
    return ZW - 0.012 if CY0 < yy < CY1 else Z0


ys = sorted(set([BY0 + (BY1 - BY0) * i / 92 for i in range(93)] + [c + r * math.cos(math.pi * k / 10) for (c, r) in KEMER for k in range(11)] +
                [CY0, CY1]))
ys = [v for v in ys if BY0 - 1e-9 <= v <= BY1 + 1e-9]
xa, xb = BX - BW / 2, BX + BW / 2
PH = 0.028           # balustrade height
for i in range(len(ys) - 1):
    ya, yb = ys[i], ys[i + 1]
    ym = (ya + yb) / 2
    # (inside an arch both ends lie on its curve; at an arch's edge the solid pier's foot is used)
    def bot(v):
        for (c, r) in KEMER:
            if abs(ym - c) < r:
                return ZS + math.sqrt(max(0.0, r * r - (v - c) ** 2))
        return ZW - 0.012 if CY0 < ym < CY1 else Z0
    ba, bb = bot(ya), bot(yb)
    ta, tb = deck(ya) + PH, deck(yb) + PH
    for x, s in ((xa, -1), (xb, 1)):
        y.yuz_yon([V(x, ya, ba), V(x, yb, bb), V(x, yb, tb), V(x, ya, ta)], TAS, V(s, 0, 0))
    # the arch soffit
    if any(abs(ym - c) < r for (c, r) in KEMER):
        y.yuz_yon([V(xa, ya, ba), V(xb, ya, ba), V(xb, yb, bb), V(xa, yb, bb)], 'tas_koyu', -Z)
    # balustrade tops and inner faces, the stepped deck
    t2 = 0.012
    for x0, x1 in ((xa, xa + t2), (xb - t2, xb)):
        y.yuz_yon([V(x0, ya, ta), V(x1, ya, ta), V(x1, yb, tb), V(x0, yb, tb)], 'tas_acik', Z)
# deck treads and risers
st = 0.012
nq = len(ys) - 1
zq = [round(((deck(ys[i]) + deck(ys[i + 1])) / 2) / st) * st + 0.002 for i in range(nq)]
for i in range(nq):
    ya, yb = ys[i], ys[i + 1]
    q = zq[i]
    y.yuz_yon([V(xa + 0.012, ya, q), V(xb - 0.012, ya, q), V(xb - 0.012, yb, q), V(xa + 0.012, yb, q)], 'zemin', Z)
    for x, s in ((xa + 0.012, 1), (xb - 0.012, -1)):
        y.yuz_yon([V(x, ya, min(q, deck(ya))), V(x, yb, min(q, deck(yb))), V(x, yb, deck(yb) + PH), V(x, ya, deck(ya) + PH)], TAS, V(s, 0, 0))
    if i < nq - 1 and abs(zq[i + 1] - q) > 1e-6:
        lo, hi = min(q, zq[i + 1]), max(q, zq[i + 1])
        yon = V(0, -1, 0) if zq[i + 1] > q else V(0, 1, 0)
        y.yuz_yon([V(xa + 0.012, yb, lo), V(xb - 0.012, yb, lo), V(xb - 0.012, yb, hi), V(xa + 0.012, yb, hi)], 'tas_koyu', yon)
# the ends
for yy, s in ((BY0, -1), (BY1, 1)):
    for x0, x1 in ((xa, xa + 0.012), (xb - 0.012, xb)):
        y.yuz_yon([V(x0, yy, Z0), V(x1, yy, Z0), V(x1, yy, Z0 + PH), V(x0, yy, Z0 + PH)], TAS, V(0, s, 0))
# arch rings: raised voussoir bands round the arches on both faces
for (c, r) in KEMER:
    m = 14
    for x, s in ((xa, -1), (xb, 1)):
        for k in range(m):
            a0, a1 = math.pi * k / m, math.pi * (k + 1) / m
            P_ = lambda rr, a: V(x + s * 0.003, c + rr * math.cos(a), ZS + rr * math.sin(a))
            key = 'tas_acik' if k % 2 else 'mermer'
            y.yuz_yon([P_(r, a0), P_(r, a1), P_(r + 0.014, a1), P_(r + 0.014, a0)], key, V(s, 0, 0))
            y.yuz_yon([P_(r + 0.014, a0), P_(r + 0.014, a1), P_(r + 0.014, a1) - V(s * 0.003, 0, 0), P_(r + 0.014, a0) - V(s * 0.003, 0, 0)],
                      key, V(0, math.cos((a0 + a1) / 2), math.sin((a0 + a1) / 2)))
            y.yuz_yon([P_(r, a0), P_(r, a1), P_(r, a1) - V(s * 0.003, 0, 0), P_(r, a0) - V(s * 0.003, 0, 0)],
                      key, V(0, -math.cos((a0 + a1) / 2), -math.sin((a0 + a1) / 2)))
        # the keystone dragon head
        kutu_merkez(y, (x + s * 0.006, c), 0.012, 0.02, 0.016, 'mermer', z0=ZS + r + 0.004)
# a string course along the faces under the balustrade, and balustrade posts with knobs
for x, s in ((xa, -1), (xb, 1)):
    for i in range(len(ys) - 1):
        ya, yb = ys[i], ys[i + 1]
        za, zb_ = deck(ya), deck(yb)
        y.yuz_yon([V(x + s * 0.004, ya, za - 0.006), V(x + s * 0.004, yb, zb_ - 0.006), V(x + s * 0.004, yb, zb_), V(x + s * 0.004, ya, za)],
                  'tas_acik', V(s, 0, 0))
        y.yuz_yon([V(x, ya, za), V(x, yb, zb_), V(x + s * 0.004, yb, zb_), V(x + s * 0.004, ya, za)], 'tas_acik', Z)
        y.yuz_yon([V(x, ya, za - 0.006), V(x, yb, zb_ - 0.006), V(x + s * 0.004, yb, zb_ - 0.006), V(x + s * 0.004, ya, za - 0.006)], 'tas_acik', -Z)
    for k in range(17):
        yy = BY0 + 0.02 + (BY1 - BY0 - 0.04) * k / 16
        xx = x - s * 0.006
        kutu_merkez(y, (xx, yy), 0.012, 0.012, 0.012, 'tas_acik', z0=deck(yy) + PH - 0.002)
        kure(y, (xx, yy, deck(yy) + PH + 0.013), 0.006, 'mermer', n=6, kat=3)
# lion posts at the ends
for yy in (BY0 + 0.01, BY1 - 0.01):
    for x in (xa + 0.006, xb - 0.006):
        kutu_merkez(y, (x, yy), 0.02, 0.02, 0.05, 'mermer', z0=Z0)
        kure(y, (x, yy, Z0 + 0.062), 0.013, 'tas_acik', n=8, kat=4)


# ---------------- the lock ----------------
y.bolum('Kilit (savak) ve vinç köprüsü')
GAP0, GAP1 = CM - 0.07, CM + 0.07
ZP = Z0 + 0.016                     # the piers' top under the coping
YP = (GAP0 - 0.024, GAP1 + 0.024)   # the gantry's post lines on the two piers
for n_, (ya_, yb_) in enumerate(((CY0, GAP0), (GAP1, CY1))):
    # a water-stained plinth, the dressed body, a moulded cornice, the coping
    kutu(y, V(LX - 0.065, ya_, ZW - 0.012), X, 0.13, yb_ - ya_, ZW2 + 0.008 - (ZW - 0.012), 'tas_koyu')
    kutu(y, V(LX - 0.06, ya_, ZW2 + 0.008), X, 0.12, yb_ - ya_, ZP - 0.004 - (ZW2 + 0.008), TAS)
    kutu(y, V(LX - 0.063, ya_, ZP - 0.004), X, 0.126, yb_ - ya_, 0.004, 'tas_acik')
    kutu(y, V(LX - 0.067, ya_, ZP), X, 0.134, yb_ - ya_, 0.008, 'tas_acik')
    # pointed cutwaters, downstream and upstream
    for s in (-1, 1):
        with parca(y, (LX + s * 0.065, (ya_ + yb_) / 2, 0)):
            hw = (yb_ - ya_) / 2
            for (zz0, zz1, key, ins) in ((ZW - 0.012, ZW2 + 0.008, 'tas_koyu', 0.0), (ZW2 + 0.008, ZP, TAS, 0.005)):
                pts = [V(-s * ins, -hw), V(s * (0.045 - ins), 0), V(-s * ins, hw)]
                for i in range(2):
                    a, b = pts[i], pts[i + 1]
                    y.yuz_yon([V(a.x, a.y, zz0), V(b.x, b.y, zz0), V(b.x, b.y, zz1), V(a.x, a.y, zz1)], key, V(s * abs((b - a).y), -s * 0 + (b - a).x * 0, 0) +
                              V(0, (1 if i == 1 else -1), 0) * 0.6)
                y.yuz_yon([V(p.x, p.y, zz1) for p in pts], 'tas_acik' if key == TAS else 'tas_koyu', Z)
    # the gate slot in the pier's gap face (a dark groove a hair proud)
    if n_ == 0:
        kutu(y, V(LX - 0.009, GAP0, ZW - 0.012), X, 0.018, 0.002, ZP - (ZW - 0.012), 'koyu', 'arkasagsolust')
    else:
        kutu(y, V(LX - 0.009, GAP1 - 0.002, ZW - 0.012), X, 0.018, 0.002, ZP - (ZW - 0.012), 'koyu', 'onsagsolust')
    # mooring bollards on the coping
    for bx in (LX - 0.05, LX + 0.05):
        by = (ya_ + yb_) / 2 + (0.02 if n_ == 0 else -0.02)
        y.prizma((bx, by), 0.006, ZP + 0.008, ZP + 0.02, 'granit', n=8)
        donel(y, (bx, by), [(0.008, ZP + 0.02), (0.008, ZP + 0.023), (0.0, ZP + 0.025)], 'granit', n=8)
# the stop logs dropped in the slots, the water held a step higher behind them
for k in range(4):
    zz = ZW - 0.006 + k * 0.0115
    boru(y, [V(LX, GAP0 - 0.003, zz), V(LX, GAP1 + 0.003, zz)], 0.0058, 'ahsap_koyu' if k % 2 else 'ahsap', n=8)
# the gantry: four posts on stone drums, braced, two beams across the gap, cross-ties, the windlass under a small roof
ZB = Z0 + 0.168
for yp in YP:
    for px in (LX - 0.032, LX + 0.032):
        donel(y, (px, yp), [(0.012, ZP + 0.008), (0.012, ZP + 0.014), (0.009, ZP + 0.018), (0.0, ZP + 0.018)], 'granit', n=8)
        kutu_merkez(y, (px, yp), 0.012, 0.012, ZB - (ZP + 0.018), 'ahsap_koyu', z0=ZP + 0.018)
    # a tie along x between the post pair (low and high) and an X of braces
    kutu(y, V(LX - 0.038, yp - 0.005, ZP + 0.062), X, 0.076, 0.01, 0.008, 'ahsap')
    kutu(y, V(LX - 0.038, yp - 0.005, ZB - 0.018), X, 0.076, 0.01, 0.01, 'ahsap')
    for s in (-1, 1):
        cubuk(y, V(LX + s * 0.026, yp, ZP + 0.07), V(LX - s * 0.026, yp, ZB - 0.018), 0.005, 'ahsap')
for px in (LX - 0.032, LX + 0.032):
    # the beams spanning the gap, with bracket arms under them at the posts
    kutu(y, V(px + 0.007, YP[0] - 0.03, ZB), Y, YP[1] - YP[0] + 0.06, 0.014, 0.014, 'ahsap_koyu')
    for (yp, s) in ((YP[0], 1), (YP[1], -1)):
        cubuk(y, V(px, yp + s * 0.005, ZB - 0.03), V(px, yp + s * 0.03, ZB), 0.006, 'ahsap')
        # (the beam's carved end)
        kutu(y, V(px + 0.006, yp - s * 0.03 - (0.006 if s > 0 else 0.0), ZB - 0.008), Y, 0.006, 0.012, 0.008, 'lake_koyu')
ZD = ZB + 0.014 + 0.009 + 0.004
for yp in YP:   # cross-ties on the beams carrying the drum's bearings
    kutu(y, V(LX - 0.042, yp - 0.007, ZB + 0.014), X, 0.084, 0.014, 0.01, 'ahsap')
    kutu_merkez(y, (LX, yp), 0.02, 0.016, 0.008, 'ahsap_koyu', z0=ZB + 0.024)
boru(y, [V(LX, YP[0] - 0.012, ZD), V(LX, YP[1] + 0.012, ZD)], 0.009, 'ahsap', n=10)
for yy in (YP[0] + 0.01, (YP[0] + YP[1]) / 2, YP[1] - 0.01):   # rope coils round the drum
    boru(y, [V(LX, yy - 0.006, ZD), V(LX, yy + 0.006, ZD)], 0.0105, 'kumas', n=10)
for (yy, s) in ((YP[0] - 0.016, -1), (YP[1] + 0.016, 1)):   # the handspikes at both ends
    boru(y, [V(LX, yy + s * 0.004, ZD), V(LX, yy - s * 0.004, ZD)], 0.012, 'ahsap_koyu', n=8)
    for k in range(4):
        a = TAU * k / 4 + 0.4
        cubuk(y, V(LX, yy, ZD), V(LX + 0.034 * math.cos(a), yy, ZD + 0.034 * math.sin(a)), 0.004, 'ahsap')
# the ropes down to the top stop log
for yy in (GAP0 + 0.035, GAP1 - 0.035):
    boru(y, [V(LX, yy, ZD - 0.009), V(LX, yy, ZW - 0.006 + 3 * 0.0115 + 0.005)], 0.0016, 'kumas', n=4)
# the canopy over the windlass: four short posts and a little curved gable roof
ZC = ZD + 0.03
for yp in YP:
    for px in (LX - 0.036, LX + 0.036):
        kutu_merkez(y, (px, yp), 0.008, 0.008, ZC - (ZB + 0.024), 'lake_koyu', z0=ZB + 0.024)
tep = cati_besik(y, LX - 0.036, LX + 0.036, YP[0] - 0.006, YP[1] + 0.006, ZC, 0.034, 0.02, 'kiremit_koyu', 'kiremit_koyu2', 0.006, 0.45,
                 'ahsap_koyu', 'ahsap', mahya_en=0.008)
for s in (-1, 1):   # ridge-end ornaments in the roof's scale
    p = V(LX, (YP[1] if s > 0 else YP[0]) + s * 0.026, tep - 0.004)
    boru(y, [p, p + V(0, s * 0.005, 0.006), p + V(0, s * 0.006, 0.014), p + V(0, s * 0.001, 0.019)], 0.004, 'kiremit_koyu2', n=6, r_son=0.0018)
# a lock keeper at the windlass's foot
insan(y, LX + 0.045, YP[0] - 0.05, ZP + 0.008, aci=math.pi, govde='lacivert')


# ---------------- junks ----------------
def junk(cx, cy, aci, L=0.3, W=0.085, zw=ZW, yelkenli=True, yelken='kirmizi'):
    with parca(y, (cx, cy, 0), aci):
        n = 12
        tt = [k / n for k in range(n + 1)]
        X_ = lambda t: -L / 2 + L * t
        B = lambda t: W / 2 * (0.62 + 0.38 * math.sin(math.pi * (0.15 + 0.8 * t)))
        S = lambda t: zw + 0.026 + 0.04 * max(0.0, (0.28 - t) / 0.28) ** 1.6 + 0.014 * max(0.0, (t - 0.78) / 0.22) ** 2
        zb = zw - 0.01
        for k in range(n):
            t0, t1 = tt[k], tt[k + 1]
            for s in (-1, 1):
                # the side in three bands: hull, the lacquered wale near the sheer, the top strake
                def H(t, zz):
                    f = (zz - zb) / (S(t) - zb)
                    return V(X_(t), s * B(t) * (0.68 + 0.32 * f), zz)
                for (za0, za1, zb0, zb1, key) in ((zb, S(t0) - 0.012, zb, S(t1) - 0.012, 'ahsap_koyu'),
                                                  (S(t0) - 0.012, S(t0) - 0.005, S(t1) - 0.012, S(t1) - 0.005, 'lake'),
                                                  (S(t0) - 0.005, S(t0), S(t1) - 0.005, S(t1), 'ahsap_koyu')):
                    y.yuz_yon([H(t0, za0), H(t1, zb0), H(t1, zb1), H(t0, za1)], key, V(0, s, 0))
            # deck (a hair below the sheer: bulwarks)
            dz = 0.007
            y.yuz_yon([V(X_(t0), -B(t0) + 0.004, S(t0) - dz), V(X_(t1), -B(t1) + 0.004, S(t1) - dz), V(X_(t1), B(t1) - 0.004, S(t1) - dz),
                       V(X_(t0), B(t0) - 0.004, S(t0) - dz)], 'ahsap_acik', Z)
            for s in (-1, 1):
                y.yuz_yon([V(X_(t0), s * (B(t0) - 0.004), S(t0) - dz), V(X_(t1), s * (B(t1) - 0.004), S(t1) - dz),
                           V(X_(t1), s * (B(t1) - 0.004), S(t1)), V(X_(t0), s * (B(t0) - 0.004), S(t0))], 'ahsap', V(0, -s, 0))
                y.yuz_yon([V(X_(t0), s * (B(t0) - 0.004), S(t0)), V(X_(t1), s * (B(t1) - 0.004), S(t1)), V(X_(t1), s * B(t1), S(t1)),
                           V(X_(t0), s * B(t0), S(t0))], 'ahsap', Z)
        # transoms (square bow and stern)
        for t, s in ((0, -1), (1, 1)):
            y.yuz_yon([V(X_(t), -B(t) * 0.68, zb), V(X_(t), B(t) * 0.68, zb), V(X_(t), B(t), S(t)), V(X_(t), -B(t), S(t))], 'lake_koyu', V(s, 0, 0))
            # its inside above the deck
            xi = X_(t) - s * 0.0008
            y.yuz_yon([V(xi, -B(t) + 0.004, S(t) - 0.007), V(xi, B(t) - 0.004, S(t) - 0.007), V(xi, B(t) - 0.004, S(t)), V(xi, -B(t) + 0.004, S(t))],
                      'ahsap', V(-s, 0, 0))
        # the stern house with a mat roof
        hx0, hx1 = X_(0.04), X_(0.3)
        zh = S(0.3) - 0.007
        duvarlar(y, dikdortgen(hx0, hx1, -W * 0.3, W * 0.3), zh, zh + 0.035, 'ahsap_dikey')
        for s in (-1, 1):
            kafes(y, V(hx0 + 0.01, s * W * 0.3) if s < 0 else V(hx1 - 0.01, s * W * 0.3), V(hx1 - 0.01, s * W * 0.3) if s < 0 else V(hx0 + 0.01, s * W * 0.3),
                  zh, 0.15, 0.85, 0.012, 0.03, 'lake', 4, 2, 0.002, 0.002)
        cati_besik(y, hx0, hx1, -W * 0.3, W * 0.3, zh + 0.035, 0.022, 0.012, 'saz', 'saz_koyu', 0.005, 0.4, 'ahsap_koyu', 'ahsap_dikey', mahya_en=0.006)
        # a rudder post and a lantern
        cubuk(y, V(X_(0) - 0.006, 0, zb + 0.01), V(X_(0) - 0.006, 0, S(0) + 0.01), 0.008, 'ahsap_koyu')
        kure(y, (X_(0.02), 0, S(0) + 0.03), 0.007, 'boya_kirmizi', n=6, kat=3)
        # masts and sails
        for xm, hm, sw in ((X_(0.48), 0.32, 0.15), (X_(0.78), 0.22, 0.1)):
            zm = S(0.5) - 0.007
            y.prizma((xm, 0), 0.0045, zm, zm + hm, 'ahsap', n=6)
            if yelkenli:
                zl, zh2 = zm + 0.05, zm + hm - 0.01
                ka = [V(xm + sw * 0.3, 0.007, zl), V(xm - sw * 0.7, 0.007, zl), V(xm - sw * 0.78, 0.007, zh2 + 0.03), V(xm + sw * 0.22, 0.007, zh2)]
                # the sail in a few horizontal panels, bellied a little, battens between them
                nb = 5
                kil = 0.0012
                iki_yuzlu(y, ka, yelken, V(0, 1, 0), kil=kil)
                for j in range(4):   # the cloth's rims, so seen edge-on it shows no gap
                    p, q = ka[j], ka[(j + 1) % 4]
                    out = (p + q) / 2 - (ka[0] + ka[1] + ka[2] + ka[3]) / 4; out.y = 0
                    y.yuz_yon([p, q, q - V(0, kil, 0), p - V(0, kil, 0)], yelken, out)
                for j in range(nb + 1):
                    u = j / nb
                    pa, pb = ka[0].lerp(ka[3], u), ka[1].lerp(ka[2], u)
                    cubuk(y, pa + (pb - pa).normalized() * 0.004, pb + (pa - pb).normalized() * 0.002, 0.003, 'ahsap_koyu', 0.005)
            else:
                # sails lowered: the bundle of battens on the yard
                cubuk(y, V(xm - sw * 0.7, 0.008, zm + 0.04), V(xm + sw * 0.3, 0.008, zm + 0.04), 0.012, yelken, 0.01)
                cubuk(y, V(xm - sw * 0.75, 0.008, zm + 0.05), V(xm + sw * 0.25, 0.008, zm + 0.05), 0.004, 'ahsap_koyu')
            # a pennant atop
            boru(y, [V(xm, 0, zm + hm), V(xm - 0.03, 0, zm + hm - 0.006)], 0.003, 'boya_kirmizi', n=4, r_son=0.0008)
        # cargo on deck
        for k in range(3):
            kutu_merkez(y, (X_(0.58 + 0.08 * k), 0.012 * (1 if k % 2 else -1)), 0.024, 0.026, 0.016, 'ahsap_acik' if k % 2 else 'kumas',
                        z0=S(0.6) - 0.007)


y.bolum('Ceonklar (yelkenli yük gemileri)')
junk(0.08, CM + 0.04, 0.0, L=0.32, yelkenli=True)
junk(-0.85, CY0 + 0.07, math.pi, L=0.3, yelkenli=False, yelken='siva_oker')
junk(0.88, CM - 0.02, math.pi, L=0.26, W=0.08, zw=ZW2, yelkenli=True, yelken='siva_oker')
# moored sampans
for (sx, sy, a) in ((-0.6, CY1 - 0.04, 0.1), (0.3, CY0 + 0.04, -0.05), (-1.0, CY1 - 0.045, 0.0)):
    with parca(y, (sx, sy, 0), a):
        pts = [V(-0.06, 0), V(-0.045, -0.018), V(0.045, -0.018), V(0.07, 0), V(0.045, 0.018), V(-0.045, 0.018)]
        for i in range(6):
            p, q = pts[i], pts[(i + 1) % 6]
            nn = V((q - p).y, -(q - p).x, 0)
            # outer side, the gunwale's top, the inner side down to the floor
            y.yuz_yon([V(p.x * 0.85, p.y * 0.85, ZW - 0.006), V(q.x * 0.85, q.y * 0.85, ZW - 0.006), V(q.x, q.y, ZW + 0.012), V(p.x, p.y, ZW + 0.012)], 'ahsap', nn)
            y.yuz_yon([V(p.x, p.y, ZW + 0.012), V(q.x, q.y, ZW + 0.012), V(q.x * 0.9, q.y * 0.9, ZW + 0.012), V(p.x * 0.9, p.y * 0.9, ZW + 0.012)], 'ahsap_koyu', Z)
            y.yuz_yon([V(q.x * 0.9, q.y * 0.9, ZW + 0.004), V(p.x * 0.9, p.y * 0.9, ZW + 0.004), V(p.x * 0.9, p.y * 0.9, ZW + 0.012), V(q.x * 0.9, q.y * 0.9, ZW + 0.012)], 'ahsap', -nn)
        y.yuz_yon([V(p.x * 0.9, p.y * 0.9, ZW + 0.004) for p in pts], 'ahsap_koyu', Z)
        # a woven mat hood
        for k in range(5):
            a0, a1 = math.pi * k / 5, math.pi * (k + 1) / 5
            iki_yuzlu(y, [V(-0.02, 0.017 * math.cos(a0), ZW + 0.012 + 0.016 * math.sin(a0)), V(0.02, 0.017 * math.cos(a0), ZW + 0.012 + 0.016 * math.sin(a0)),
                          V(0.02, 0.017 * math.cos(a1), ZW + 0.012 + 0.016 * math.sin(a1)), V(-0.02, 0.017 * math.cos(a1), ZW + 0.012 + 0.016 * math.sin(a1))],
                      'saz', V(0, math.cos((a0 + a1) / 2), math.sin((a0 + a1) / 2)))


# ---------------- the near quay: warehouses, crane, cargo ----------------
y.bolum('Ambarlar, dükkânlar, tak')
pailou(y, (BX, BY0 - 0.07), 0.24, 0.15)
for k in range(3):
    x0 = -0.58 + k * 0.23
    salon(y, x0, x0 + 0.16, -1.0, -0.88, Z0, 0.06 + 0.008 * (k % 2), 0.06, sacak=0.025, duvar='ahsap_dikey', direk='ahsap_koyu', tur='besik',
          kapi_yon=2, kaide=0.01, kivrim=0.3, basamak=False)
    for j in range(3):   # red lanterns under the eaves
        lx = x0 + 0.03 + j * 0.055
        boru(y, [V(lx, -0.855, Z0 + 0.07), V(lx, -0.855, Z0 + 0.055)], 0.0012, 'koyu', n=3, kapat=False)
        kure(y, (lx, -0.855, Z0 + 0.048), 0.008, 'boya_kirmizi', n=8, kat=4)
    # an awning on poles over the goods
    with parca(y, (x0 + 0.085, -0.835, Z0 + 0.046)):
        o = V(-0.075, -0.035, 0)
        ac = math.atan2(0.012, 0.07)
        P_ = lambda u, v, w: V(-0.075 + u, -0.035 + v * math.cos(ac), 0.006 - v * math.sin(ac) + w)
        kk = ('kumas', 'siva_oker', 'kumas')[k]
        for (a, b, c_, d_, yon) in ((P_(0, 0, 0.003), P_(0.15, 0, 0.003), P_(0.15, 0.071, 0.003), P_(0, 0.071, 0.003), Z),
                                     (P_(0, 0, 0), P_(0, 0.071, 0), P_(0.15, 0.071, 0), P_(0.15, 0, 0), -Z)):
            y.yuz_yon([a, b, c_, d_], kk, yon)
        for (a, b, yon) in ((P_(0, 0.071, 0), P_(0.15, 0.071, 0), Y), (P_(0, 0, 0), P_(0.15, 0, 0), -Y), (P_(0, 0, 0), P_(0, 0.071, 0), -X),
                            (P_(0.15, 0, 0), P_(0.15, 0.071, 0), X)):
            y.yuz_yon([a, b, b + Z * 0.003, a + Z * 0.003], kk, yon)
    for xx in (x0 + 0.015, x0 + 0.155):
        cubuk(y, V(xx, -0.8, Z0), V(xx, -0.8, Z0 + 0.04), 0.004, 'ahsap')
    for j in range(3):
        kutu_merkez(y, (x0 + 0.04 + j * 0.045, -0.83), 0.03, 0.022, 0.014, 'ahsap_acik', z0=Z0)
        kure(y, (x0 + 0.04 + j * 0.045, -0.83, Z0 + 0.018), 0.008, ('boya_sari', 'boya_kirmizi', 'boya_yesil')[(j + k) % 3], n=6, kat=3)
for (tx, ty) in ((-0.95, -0.66), (0.0, -0.62), (-0.4, -0.7), (0.98, -0.3), (0.98, -0.95)):
    agac(y, tx, ty, Z0, boy=0.12, key='boya_yesil')
for (x0, x1, y0_, y1_, yon) in ((-1.06, -0.78, -0.56, -0.38, 2), (-0.72, -0.46, -0.56, -0.38, 2), (-1.06, -0.66, -0.98, -0.76, 0)):
    salon(y, x0, x1, y0_, y1_, Z0, 0.07, 0.07, sacak=0.03, duvar='siva', direk='ahsap_koyu', tur='besik', kapi_yon=yon, kaide=0.014,
          kivrim=0.3, sus='kiremit_koyu2')
y.bolum('Vinç ve yükler')
# a treadmill crane at the quay's edge
CR = V(-0.12, CY0 - 0.08)
for s in (-1, 1):
    cubuk(y, CR + V(s * 0.03, -0.03, Z0), CR + V(s * 0.012, 0.0, Z0 + 0.2), 0.01, 'ahsap')
    cubuk(y, CR + V(s * 0.03, 0.03, Z0), CR + V(s * 0.012, 0.0, Z0 + 0.2), 0.01, 'ahsap')
cubuk(y, CR + V(0, -0.02, Z0 + 0.19), CR + V(0, 0.2, Z0 + 0.25), 0.012, 'ahsap_koyu')
boru(y, [CR + V(0, 0.19, Z0 + 0.245), CR + V(0, 0.19, Z0 + 0.06)], 0.0018, 'kumas', n=4)
kutu_merkez(y, (CR.x, CR.y + 0.19), 0.03, 0.03, 0.025, 'ahsap_acik', z0=Z0 + 0.035)
# the treadwheel beside it
for s in (-1, 1):
    pts = [CR + V(s * 0.04, -0.06 + 0.045 * math.cos(TAU * k / 16), Z0 + 0.05 + 0.045 * math.sin(TAU * k / 16)) for k in range(17)]
    boru(y, pts, 0.004, 'ahsap', n=4, kapat=False)
for k in range(8):
    a = TAU * k / 8
    p = CR + V(0, -0.06 + 0.045 * math.cos(a), Z0 + 0.05 + 0.045 * math.sin(a))
    cubuk(y, p - V(0.042, 0, 0), p + V(0.042, 0, 0), 0.004, 'ahsap_koyu')
boru(y, [CR + V(-0.05, -0.06, Z0 + 0.05), CR + V(0.05, -0.06, Z0 + 0.05)], 0.005, 'ahsap_koyu', n=6)
for s in (-1, 1):
    cubuk(y, CR + V(s * 0.05, -0.06, Z0), CR + V(s * 0.05, -0.06, Z0 + 0.05), 0.008, 'ahsap')
# cargo: crates, sacks, jars
for k in range(22):
    cx, cy = rn.uniform(-1.05, 0.0), rn.uniform(-0.36, -0.3)
    if abs(cx - BX) < 0.12 or abs(cx + 0.78 - 0.08) < 0.1: continue
    tur = rn.random()
    if tur < 0.4:
        kutu_merkez(y, (cx, cy), 0.026, 0.026, 0.022, 'ahsap_acik', z0=Z0, aci=rn.uniform(0, 1))
    elif tur < 0.75:
        kure(y, (cx, cy, Z0 + 0.008), 0.014, 'kumas', n=8, kat=4)
    else:
        donel(y, (cx, cy), [(0.0, Z0), (0.01, Z0), (0.014, Z0 + 0.014), (0.009, Z0 + 0.026), (0.006, Z0 + 0.03), (0.0, Z0 + 0.03)], 'kiremit', n=8)
for k, (px, py) in enumerate(((-0.95, -0.33), (-0.5, -0.34), (-0.08, -0.4), (0.0, -0.34), (-0.6, -0.65), (-0.35, CM + 0.1))):
    insan(y, px, py, Z0 if k < 5 else deck(py) + 0.002, aci=rn.uniform(0, TAU), govde=rn.choice(['kumas', 'lacivert', 'siva_oker']))


# ---------------- the customs house ----------------
y.bolum('Gümrük binası')
GX_0, GX_1, GY_0, GY_1 = 0.08, 0.86, -1.0, -0.42
GCX = (GX_0 + GX_1) / 2
cin_duvar(y, [V(GCX + 0.08, GY_1), V(GX_0, GY_1), V(GX_0, GY_0), V(GX_1, GY_0), V(GX_1, GY_1), V(GCX - 0.08, GY_1)], Z0, 0.075)
y.yuz_yon([V(GX_0 + 0.018, GY_0 + 0.018, Z0 + 0.002), V(GX_1 - 0.018, GY_0 + 0.018, Z0 + 0.002), V(GX_1 - 0.018, GY_1 - 0.018, Z0 + 0.002),
           V(GX_0 + 0.018, GY_1 - 0.018, Z0 + 0.002)], 'zemin', Z)
# the gate house
GCX = (GX_0 + GX_1) / 2
salon(y, GCX - 0.08, GCX + 0.08, GY_1 - 0.03, GY_1 + 0.03, Z0, 0.07, 0.055, sacak=0.03, tur='irimoya', kapi_yon=2, kaide=0.012,
      sus='kiremit_koyu2', basamak=False)
for s in (-1, 1):   # stone lions by the gate
    kutu_merkez(y, (GCX + s * 0.07, GY_1 + 0.07), 0.024, 0.03, 0.018, 'granit', z0=Z0)
    kure(y, (GCX + s * 0.07, GY_1 + 0.07, Z0 + 0.03), 0.013, 'tas_acik', n=8, kat=4)
# the main hall and side halls
salon(y, GCX - 0.2, GCX + 0.2, GY_0 + 0.08, GY_0 + 0.26, Z0 + 0.002, 0.085, 0.095, sacak=0.04, tur='irimoya', kapi_yon=2, kaide=0.03,
      sus='kiremit_koyu2')
for s in (-1, 1):
    x0 = GCX + s * 0.28
    salon(y, x0 - 0.055, x0 + 0.055, GY_0 + 0.3, GY_1 - 0.1, Z0 + 0.002, 0.06, 0.05, sacak=0.025, tur='besik', duvar='siva',
          kapi_yon=(1 if s < 0 else 3), kaide=0.012)
# the flagpole of the customs (team banner) and a bronze incense burner
sancak(y, GCX + 0.12, GY_1 + 0.1, Z0, boy=0.32, en=0.12, yuk=0.075, aci=0.3)
y.prizma((GCX, GY_0 + 0.36), 0.018, Z0 + 0.002, Z0 + 0.03, 'bronz', n=8)
y.koni((GCX, GY_0 + 0.36), 0.026, Z0 + 0.03, 0.022, 'bronz', n=8)


# ---------------- the far bank: pagoda, temple hall, pavilion, willows ----------------
y.bolum('Randeng pagodası')
PC = (0.5, 0.66)
y.yuz_yon([V(p.x, p.y, Z0 + 0.002) for p in cokgen(PC, 0.32, 8, math.pi / 8)], 'zemin', Z)
tepe_p = yogun_pagoda(y, PC, 0.105, Z0, 0.16, n_kat=13, kat_h=0.042, govde='tas_acik', cati='kiremit_koyu', kaide_key='granit')

y.bolum('Tapınak salonu, su köşkü, söğütler')
cin_duvar(y, [V(0.25, 0.4), V(0.12, 0.4), V(0.12, 1.04), V(0.88, 1.04), V(0.88, 0.4), V(0.75, 0.4)][::-1], Z0, 0.07)
# village houses and a well behind the pavilion
for (x0, y0_, w_, d_, yon) in ((-1.05, 0.5, 0.2, 0.12, 0), (-0.75, 0.78, 0.16, 0.12, 0), (-1.05, 0.88, 0.16, 0.12, 1)):
    salon(y, x0, x0 + w_, y0_, y0_ + d_, Z0, 0.055, 0.05, sacak=0.025, duvar='siva', direk='ahsap_koyu', tur='besik', kapi_yon=yon,
          kaide=0.01, basamak=False)
y.prizma((-0.45, 0.72), 0.018, Z0, Z0 + 0.018, 'granit', n=10)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0185) for p in cokgen((-0.45, 0.72), 0.012, 10)], 'su', Z)
salon(y, 0.25, 0.75, 0.24, 0.38, Z0, 0.075, 0.08, sacak=0.035, tur='irimoya', kapi_yon=0, kaide=0.022, sus='kiremit_yesil',
      cati='kiremit_yesil', mahya='kiremit_yesil')   # (green glaze: a temple's tiles; imperial yellow was the court's)
salon(y, -0.2, 0.08, 0.6, 0.78, Z0, 0.065, 0.06, sacak=0.03, tur='kirma', kapi_yon=0, kaide=0.015)
# the waterside pavilion on a terrace jutting over the canal edge
kosk(y, (-0.72, CY1 + 0.12), 0.13, Z0, 0.085, 0.1, sacak=0.045)
for (tx, ty, b) in ((-1.02, 0.32, 0.17), (-0.5, 0.3, 0.16), (-0.08, 0.32, 0.15), (0.92, 0.3, 0.16), (1.0, 0.62, 0.15), (-0.95, 0.7, 0.16),
                    (-0.5, 0.9, 0.14), (0.15, 0.98, 0.15), (0.9, 0.98, 0.14)):
    sogut(y, tx, ty, Z0, boy=b, tohum=int(tx * 100))
for (tx, ty) in ((-0.62, 0.62), (-0.35, 0.55), (0.12, 0.42), (0.85, 0.42), (-0.75, 0.95)):
    agac(y, tx, ty, Z0, boy=0.11, key='boya_yesil')
# a path from the bridge to the temple
for (a, b) in ((V(BX, BY1), V(BX, 0.5)), (V(BX, 0.5), V(0.08, 0.5))):
    e = (b - a).normalized(); nn = V(-e.y, e.x) * 0.04
    y.yuz_yon([a - nn + Z * (Z0 + 0.002), b - nn + Z * (Z0 + 0.002), b + nn + Z * (Z0 + 0.002), a + nn + Z * (Z0 + 0.002)], 'zemin', Z)
insan(y, -0.6, 0.45, Z0, aci=1.0, govde='siva_oker')
insan(y, 0.3, 0.5, Z0, aci=2.0, govde='kumas')

calistir(y, 'lm_buyukkanal')
