# The Kothon of Carthage (lm_kothon): the circular naval harbour. A ring basin round a round island; on the island the
# admiral's tall tower (a plastered drum with a cavetto cornice, an Ionic tholos, a lookout with the sign of Tanit);
# ship sheds all round the island and the outer ring (radial gabled roofs on Ionic columns, slipways with warships'
# rams in them), the high ring wall that hid the fleet, a water gate over the channel to the rectangular merchant
# harbour, its quays, warehouses and merchantmen, the sea wall with the chained harbour mouth, white Punic houses.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir
from kartaca_ortak import *

y = Yapi()
ZS = 0.025                  # the water surface
ZK = 0.075                  # the quays
C = V(0.0, 0.32)            # the round harbour's centre
RW, RS, RA = 0.58, 0.84, 0.89   # the basin's edge (shed fronts), the sheds' back (ring wall inside), the ring wall outside
RI, RT = 0.27, 0.13         # the island's shed fronts, their back (the tower)
NO, NI = 36, 16             # bays on the outer ring and on the island
ZWO, ZWI = ZK + 0.1, ZK + 0.08  # eaves of the outer and island sheds
TANP = math.tan(math.radians(30))
ZWT = ZK + 0.19             # the ring wall's top
X0, X1, Y0, Y1 = -1.2, 1.2, -1.25, 1.25
YQ = -0.66                  # the merchant harbour's back quay
HX, HY0 = 0.85, -1.0        # the merchant harbour: |x| < HX, HY0 < y < YQ
MX = 0.13                   # the harbour mouth: |x| < MX
WC = RA * math.sin(math.radians(5))   # the channel's half width at the ring wall
SIV, KUM, KUMK = 'siva', 'kum', 'kum_koyu'
D = math.radians


def P(a, r, z=0.0):
    return V(C.x + r * math.cos(a), C.y + r * math.sin(a), z)


def radyal(a):
    return V(math.cos(a), math.sin(a))


# ================================================================ the sea and the land
y.bolum('Deniz ve rıhtımlar')
kutu(y, V(X0, Y0, 0), X, X1 - X0, Y1 - Y0, ZS, 'kaya_koyu', 'onarkasagsol')
y.yuz_yon([V(X0, Y0, ZS), V(X1, Y0, ZS), V(X1, Y1, ZS), V(X0, Y1, ZS)], 'su', Z)


def rect_isin(a):
    """where the ray from C at angle a leaves the land rectangle X0..X1, YQ..Y1"""
    d = radyal(a); best = 1e9
    for t in ((X1 - C.x) / d.x if d.x > 1e-9 else 1e9, (X0 - C.x) / d.x if d.x < -1e-9 else 1e9,
              (Y1 - C.y) / d.y if d.y > 1e-9 else 1e9, (YQ - C.y) / d.y if d.y < -1e-9 else 1e9):
        if 0 < t < best: best = t
    return C + d * best


# the land round the ring wall: quads from the wall's foot out to the rectangle (corners sampled exactly)
a_bas, a_son = D(-85), D(265)
acilar = [a_bas + (a_son - a_bas) * k / 100 for k in range(101)]
for cx_, cy_ in ((X1, YQ), (X1, Y1), (X0, Y1), (X0, YQ)):
    t = math.atan2(cy_ - C.y, cx_ - C.x)
    while t < a_bas: t += TAU
    acilar.append(t)
acilar = sorted(set(round(t, 9) for t in acilar))
ic_ = [P(t, RA, ZK) for t in acilar]
dis_ = [rect_isin(t) for t in acilar]
dis_[0] = V(WC, YQ); dis_[-1] = V(-WC, YQ)
for i in range(len(acilar) - 1):
    q = [ic_[i], dis_[i] + Z * ZK, dis_[i + 1] + Z * ZK, ic_[i + 1]]
    y.yuz_yon(q, 'zemin' if (dis_[i].y < YQ + 0.12 or dis_[i + 1].y < YQ + 0.12) else 'toprak_ot', Z)
# the land's outer faces, the merchant quay and the channel's sides
duz_duvar(y, V(X0, Y1), V(X0, YQ), ZS, ZK, KUM)
duz_duvar(y, V(X1, YQ), V(X1, Y1), ZS, ZK, KUM)
duz_duvar(y, V(X1, Y1), V(X0, Y1), ZS, ZK, KUM)
for a, b in ((V(-HX, YQ), V(-WC, YQ)), (V(WC, YQ), V(HX, YQ))):
    duz_duvar(y, a, b, ZS, ZK, KUM)
    silme(y, [a, b], ZK - 0.01, 0.01, 0.006, 'kum_acik', 'tac', kapali=False)
    silme(y, [a, b], ZS - 0.004, 0.01, 0.005, 'kaya_koyu', 'duz', kapali=False)
ck = P(D(-85), RA); ck2 = P(D(-95), RA)
duz_duvar(y, V(WC, ck.y), V(WC, YQ), ZS, ZK, KUM)
duz_duvar(y, V(-WC, YQ), V(-WC, ck2.y), ZS, ZK, KUM)


def kara(x0, x1, y0, y1, yuzler):
    """a raised land block (yuzler: which sides get a stone face: on / arka / sag / sol)"""
    kutu(y, V(x0, y0, ZS), X, x1 - x0, y1 - y0, ZK - ZS, KUM, yuzler)
    y.yuz_yon([V(x0, y0, ZK), V(x1, y0, ZK), V(x1, y1, ZK), V(x0, y1, ZK)], 'zemin', Z)




def rihtim(a, b):
    """a quay face a->b (the water on its right) with a cornice on top and a dark foot at the water"""
    duz_duvar(y, a, b, ZS, ZK, KUM)
    silme(y, [a, b], ZK - 0.01, 0.01, 0.006, 'kum_acik', 'tac', kapali=False)
    silme(y, [a, b], ZS - 0.004, 0.01, 0.005, 'kaya_koyu', 'duz', kapali=False)


for s in (-1, 1):
    xa, xb = sorted((s * X1, s * HX))
    kara(xa, xb, HY0, YQ, 'sol' if s < 0 else 'sag')                     # the side quays (outer face only)
    xa, xb = sorted((s * X1, s * MX))
    kara(xa, xb, Y0, HY0, 'on' + ('sol' if s < 0 else 'sag'))             # the front strip (sea face, outer side)
    if s < 0:
        rihtim(V(-HX, HY0), V(-HX, YQ))
        rihtim(V(-MX, HY0), V(-HX, HY0))
        rihtim(V(-MX, Y0), V(-MX, HY0))
    else:
        rihtim(V(HX, YQ), V(HX, HY0))
        rihtim(V(HX, HY0), V(MX, HY0))
        rihtim(V(MX, HY0), V(MX, Y0))
# bollards along the merchant quays
for k in range(9):
    for s in (-1, 1):
        xx = s * (0.2 + 0.075 * k)
        if abs(xx) < HX - 0.03:
            y.prizma((xx, HY0 - 0.014), 0.0055, ZK, ZK + 0.014, 'kum_acik', n=6)
            if abs(xx) > WC + 0.04: y.prizma((xx, YQ + 0.014), 0.0055, ZK, ZK + 0.014, 'kum_acik', n=6)
for k in range(4):
    for s in (-1, 1):
        y.prizma((s * (HX + 0.014), HY0 + 0.05 + 0.08 * k), 0.0055, ZK, ZK + 0.014, 'kum_acik', n=6)


# ================================================================ the ship sheds
def kama_cati(a0, a1, rf, rb, zw, sacak, th=0.006, yan=(), sus=True):
    """a gabled roof over one radial shed between the angles a0..a1, its front (the water) at radius rf, its back at rb:
    the ridge runs radially at a constant pitch (it rises as the bay widens), the slopes and their undersides, the
    fascia, a ridge cap, the plastered gable over the front with a bronze disc. yan: sides (0: a0, 1: a1) left open
    (a neighbour missing) that get an edge face"""
    sg = 1 if rb > rf else -1
    ha, am = (a1 - a0) / 2, (a0 + a1) / 2
    ch, k = math.cos(ha), math.sin(ha) * TANP
    re = rf - sg * sacak
    S = lambda a, r, dz=0.0: P(a, r, zw + dz)
    R = lambda r, dz=0.0: P(am, r * ch, zw + k * r * ch + dz)
    on = radyal(am) * (-sg)
    for a, s_ in ((a0, 0), (a1, 1)):
        yan_yon = (radyal(a) - radyal(am)).normalized()
        q = [S(a, re), S(a, rb), R(rb), R(re)]
        y.yuz_yon(q, 'kiremit' if s_ == 0 else 'kiremit2', yan_yon * 0.5 + Z)
        y.yuz_yon([p - Z * th for p in q], 'ahsap_koyu', -(yan_yon * 0.5 + Z))
        y.yuz_yon([S(a, re), R(re), R(re, -th), S(a, re, -th)], 'ahsap_koyu', on)
        y.yuz_yon([S(a, rb), R(rb), R(rb, -th), S(a, rb, -th)], 'ahsap_koyu', -on)   # the back edge
        if s_ in yan:
            y.yuz_yon([S(a, re), S(a, rb), S(a, rb, -th), S(a, re, -th)], 'ahsap_koyu', yan_yon)
    for sgn in (-1, 1):   # the ridge cap: a low two-faced roll
        n_ = V(-math.sin(am), math.cos(am)) * sgn
        y.yuz_yon([R(re) + n_ * 0.005, R(rb) + n_ * 0.005, R(rb, 0.005), R(re, 0.005)], 'kiremit2', n_ + Z)
    y.yuz_yon([R(re) - V(-math.sin(am), math.cos(am)) * 0.005, R(re) + V(-math.sin(am), math.cos(am)) * 0.005, R(re, 0.005)], 'kiremit2', on)
    g = [P(a0, rf, zw - th), P(a1, rf, zw - th), P(am, rf * ch, zw + k * rf * ch - th)]
    y.yuz_yon(g, SIV, on)
    if sus:   # a bronze shield disc in the gable
        gc = (g[0] + g[1] + g[2]) / 3 - Z * 0.002
        e = (g[1] - g[0]).normalized()
        rr = min(0.011, (g[2].z - g[0].z) * 0.3)
        Pd = lambda u, v, d: gc + e * u + Z * v + on * d
        prizma2(y, [(rr * math.cos(TAU * i / 6), rr * math.sin(TAU * i / 6)) for i in range(6)], Pd, 0.002, 'bronz', on)


def rampa_z(r, rf, rb):
    t = (r - rf) / (rb - rf)
    return ZS - 0.004 + (ZK - 0.012 - ZS + 0.004) * t


def sundurmalar(rf, rb, n, a_bas, zw, sacak, kanal=(), duz=(), gemi_L=0.24, gemi_B=0.046, gemiler=()):
    """a ring of n radial ship sheds (bay i centred at a_bas + i * TAU / n): Ionic columns on pedestals in the water at
    the front, a beam between them, stone piers between the bays, slipways with runners (warships hauled up on those
    in gemiler), radial gabled roofs. kanal: bays left out (water); duz: bays with a flat paved floor (a landing)"""
    sg = 1 if rb > rf else -1
    hw = TAU / n / 2
    rcol = rf - sg * 0.014
    ch = math.cos(hw)
    for i in range(n):
        am = a_bas + TAU * i / n
        a0, a1 = am - hw, am + hw
        if i in kanal: continue
        # the piers and columns on this bay's sides (a shared side only once)
        for a in (a0, a1):
            if a == a0 and (i - 1) % n not in kanal: continue
            e = radyal(a) * sg; s = V(-e.y, e.x)
            r0 = rcol + sg * 0.004
            o = P(a, r0) - s * 0.0065 + Z * (ZS - 0.01)
            kutu(y, o, e, abs(rb - r0), 0.013, zw - 0.006 - ZS + 0.01, KUM, 'onarkasolust')
            pc = P(a, rcol)
            kutu_merkez(y, (pc.x, pc.y), 0.024, 0.024, 0.034, 'kum_acik', z0=ZS - 0.01, aci=a)
            iyon_hafif(y, pc.x, pc.y, ZS + 0.024, zw - 0.024, 0.0082, SIV, 'siva_krem', n=6, aci=a)
        # the beam over the front
        A, B = P(a0, rcol), P(a1, rcol)
        d0, d1 = rcol * ch - sg * 0.011, rf * ch + sg * 0.003      # its front and back (radial distances of the chords)
        cm = C + radyal(am) * ((d0 + d1) / 2)
        kutu_merkez(y, (cm.x, cm.y), (B - A).length + 0.02, abs(d1 - d0), 0.018, 'siva_krem', z0=zw - 0.024, aci=am + math.pi / 2)
        # the floor: a slipway (or a flat landing)
        if i in duz:
            y.yuz_yon([P(a0, rf, ZK), P(a1, rf, ZK), P(a1, rb, ZK), P(a0, rb, ZK)], 'zemin', Z)
            y.yuz_yon([P(a0, rf, ZS - 0.01), P(a1, rf, ZS - 0.01), P(a1, rf, ZK), P(a0, rf, ZK)], KUM, radyal(am) * (-sg))
        else:
            y.yuz_yon([P(a0, rf, ZS - 0.004), P(a1, rf, ZS - 0.004), P(a1, rb, ZK - 0.012), P(a0, rb, ZK - 0.012)], 'zemin', Z)
            t = V(-math.sin(am), math.cos(am))
            for sx in ():
                p0 = P(am, rf) + t * (sx * 0.011); p1 = P(am, rb) + t * (sx * 0.011)
                cubuk(y, p0 + Z * (ZS - 0.002), p1 + Z * (ZK - 0.01), 0.005, 'ahsap', 0.004)
            if i in gemiler:
                L = gemi_L
                rbow = rf - sg * 0.004
                rm = rbow + sg * L / 2
                eg = math.atan2(ZK - 0.008 - ZS, abs(rb - rf))
                zm = rampa_z(rm, rf, rb) + 0.016
                gemi(y, P(am, rm, zm), am + (math.pi if sg > 0 else 0.0), -eg, L=L, B=gemi_B, H=0.024, kurek=False, tohum=i, kaba=True)
        yan = tuple(k for k, j in ((0, (i - 1) % n), (1, (i + 1) % n)) if j in kanal)
        kama_cati(a0, a1, rf, rb, zw, sacak, yan=yan, sus=i % 2 == 0)


y.bolum('Gemi hangarları: dış halka')
KANAL_I, KOPRU_I = 0, 15
gem_dis = [i for i in range(NO) if i not in (KANAL_I, KOPRU_I) and i % 2 == 1]
sundurmalar(RW, RS, NO, D(-90), ZWO, 0.028, kanal=(KANAL_I,), duz=(KOPRU_I,), gemiler=gem_dis)
y.bolum('Gemi hangarları: ada')
gem_ada = [j for j in range(1, NI) if j % 4 == 1]
sundurmalar(RI, RT, NI, D(60), ZWI, 0.022, duz=(0,), gemi_L=0.13, gemi_B=0.034, gemiler=gem_ada)


# ================================================================ the ring wall and the water gate
y.bolum('Halka sur')
AK = [D(-85) + D(5) * k for k in range(71)]          # -85 .. 265 degrees
IN = [P(t, RS) for t in AK]
OUT = [P(t, RA) for t in AK]
ZKV = ZWT - 0.036
for k in range(len(AK) - 1):
    duz_duvar(y, OUT[k], OUT[k + 1], ZK, ZKV, SIV)
    duz_duvar(y, IN[k + 1], IN[k], ZK - 0.02, ZWT, SIV)
    y.yuz_yon([IN[k] + Z * ZWT, OUT[k] + Z * ZWT, OUT[k + 1] + Z * ZWT, IN[k + 1] + Z * ZWT], 'zemin', Z)
silme(y, OUT, ZK, 0.022, 0.01, KUM, 'kaide', kapali=False)
silme(y, OUT, ZK + 0.105, 0.007, 0.005, 'siva_krem', 'duz', kapali=False)
silme(y, OUT, ZKV, 0.036, 0.024, 'siva_krem', KAVETTO_H, kapali=False)
DK = [P(t, RA + 0.024) for t in AK]
parapet(y, DK, ZWT, 0.008, 0.02, 0.012, SIV, kapali=False)
for k in range(len(AK) - 1):
    a, b = OUT[k], OUT[k + 1]
    ex = (b - a).normalized(); nrm = V(ex.y, -ex.x)
    L = (b - a).length
    if abs(AK[k] - D(57.5)) < D(4): continue
    pencere_kutu(y, a, ex, nrm, L / 2 - 0.008, ZK + 0.122, 0.016, 0.03, 'koyu')
    if k % 4 == 0:
        pencere_kutu(y, a, ex, nrm, L / 2 - 0.004, ZK + 0.045, 0.008, 0.032, 'koyu')
    if k % 2 == 1 and k < len(AK) - 2:   # pilasters at every other corner
        t = AK[k + 1]
        pc = P(t, RA + 0.003)
        kutu_merkez(y, (pc.x, pc.y), 0.02, 0.012, ZKV - ZK - 0.022, 'siva_krem', z0=ZK + 0.022, aci=t + math.pi / 2)
# the gate through the ring wall to the island bridge
t = D(60); o = P(t, RA); ex = V(-math.sin(t), math.cos(t))
pencere_kutu(y, o - ex * 0.022, ex, radyal(t), 0.0, ZK, 0.044, 0.075, 'ahsap_koyu', cerceve='kum_acik')
tanit_kabartma(y, o + Z * (ZK + 0.088) + radyal(t) * 0.001, ex, radyal(t), 0.03, 'bronz')


def pon_kule(x0, x1, y0, y1, z0, h, key=KUM, yariklar=True, merlon=True):
    """a square Punic tower: a moulded plinth, slit windows in two storeys, a cavetto cornice, a merloned top"""
    kutu(y, V(x0, y0, z0), X, x1 - x0, y1 - y0, h - 0.04, key, 'onarkasagsol')
    k = dikdortgen(x0, x1, y0, y1)
    silme(y, k, z0, 0.025, 0.01, KUMK, 'kaide')
    silme(y, k, z0 + h * 0.48, 0.008, 0.005, 'kum_acik', 'duz')
    kavetto(y, k, z0 + h - 0.04, 0.04, 0.026, 'kum_acik')
    if merlon:
        parapet(y, disa(k, 0.026), z0 + h, 0.008, 0.022, 0.012, key)
    if yariklar:
        for side in range(4):
            a, b = k[side], k[(side + 1) % 4]
            L = (b - a).length; ex = (b - a) / L; nrm = V(ex.y, -ex.x)
            for v in (h * 0.25, h * 0.62):
                yarik(y, a, ex, nrm, L / 2 - 0.005, z0 + v, 0.01, 0.04, 'koyu')
    return z0 + h


y.bolum('Su kapısı')
GY0, GY1 = OUT[0].y - 0.075, OUT[0].y + 0.035
for s in (-1, 1):
    xa, xb = sorted((s * (WC + 0.001), s * (WC + 0.12)))
    pon_kule(xa, xb, GY0, GY1, ZK, 0.33)
kemer_dizisi(y, V(-WC, OUT[0].y), V(WC, OUT[0].y), 1, ZS - 0.01, ZWT - ZS + 0.01, IN[0].y - OUT[0].y, renk=(SIV, 'kum_koyu', 'kum_acik', 'kum_koyu'),
             en=0.72, ust=0.06, acik=True, taban=False)
silme(y, [V(-WC, OUT[0].y), V(WC, OUT[0].y)], ZKV, 0.036, 0.024, 'siva_krem', KAVETTO, kapali=False)
mazgal(y, V(-WC, OUT[0].y - 0.024), V(WC, OUT[0].y - 0.024), ZWT, 0.022, 0.012, SIV)
tanit_kabartma(y, V(0, OUT[0].y, ZWT - 0.072), X, -Y, 0.034, 'bronz')
sancak(y, -WC - 0.06, GY0 + 0.055, ZK + 0.33, boy=0.2, en=0.1, yuk=0.06, aci=D(200))


# ================================================================ the bridge to the island
y.bolum('Köprü')
t = D(60); e = radyal(t); s = V(-e.y, e.x)
a = P(t, RI - 0.004) - s * 0.026; b = P(t, RW + 0.004) - s * 0.026
kemer_dizisi(y, a, b, 3, ZS - 0.01, ZK - ZS + 0.01, 0.052, renk=(KUM, 'kum_koyu', 'kum_acik', 'kum_koyu'), en=0.62, ust=0.012, acik=True, taban=False)
for sx in (0.0, 0.052 - 0.008):
    kutu(y, a + s * sx + Z * ZK, e, (b - a).length, 0.008, 0.014, 'kum_acik', 'onarkasagsolust')


# ================================================================ the admiral's tower
y.bolum('Amiral kulesi')
c = (C.x, C.y)
KT = D(7.5)   # (24 facets turned so the windows, pilasters and door sit on facet middles)
y.prizma(c, 0.128, ZS - 0.01, ZK + 0.02, KUM, n=24, ust=False, kat=KT)
ZT1 = ZK + 0.34
R1 = 0.122
y.prizma(c, R1, ZK + 0.02, ZT1 - 0.036, SIV, n=24, ust=False, kat=KT)
y.yuz_yon(cokgen(c, 0.128, 24, KT, z=ZK + 0.02), KUM, Z)
halka_kornis(y, c, R1, ZK + 0.02, 0.014, 0.008, 24, KUM, kat=KT, profil='kaide')
halka_kornis(y, c, R1, ZK + 0.125, 0.008, 0.005, 24, 'siva_krem', kat=KT)
halka_kornis(y, c, R1, ZT1 - 0.062, 0.022, 0.0025, 24, 'boya_kirmizi', kat=KT)
kavetto(y, cokgen(c, R1, 24, KT), ZT1 - 0.036, 0.036, 0.024, 'siva_krem')
for kk in range(12):
    tp = D(30 * kk)   # pilasters on the corners
    pc = P(tp, R1 * math.cos(math.pi / 24) + 0.004)
    kutu_merkez(y, (pc.x, pc.y), 0.016, 0.01, ZT1 - 0.062 - ZK - 0.133, 'siva_krem', z0=ZK + 0.133, aci=tp + math.pi / 2)
    tw = D(30 * kk + 15)   # windows between them (on the facets' middles)
    ex = V(-math.sin(tw), math.cos(tw)); nrm = radyal(tw)
    o = C + nrm * (R1 * math.cos(math.pi / 24))
    pencere_kutu(y, o, ex, nrm, -0.011, ZK + 0.17, 0.022, 0.05, 'koyu', cerceve='kum_acik')
    if kk % 2 == 0: tanit_kabartma(y, o + Z * (ZK + 0.24), ex, nrm, 0.04, 'bronz', d=0.0025)
    else: prizma2(y, [(0.012 * math.cos(TAU * i / 8), 0.012 * math.sin(TAU * i / 8)) for i in range(8)], lambda u, v, d: o + ex * u + Z * (ZK + 0.262 + v) + nrm * d, 0.0025, 'bronz', nrm)
# the door to the bridge landing
td = D(60); o = P(td, R1 * math.cos(math.pi / 24)); ex = V(-math.sin(td), math.cos(td))
pencere_kutu(y, o - ex * 0.02, ex, radyal(td), 0.0, ZK, 0.04, 0.075, 'ahsap_koyu', cerceve='kum_acik')
# second stage: an Ionic tholos round a plastered core
ZT2 = ZT1 + 0.21
y.prizma(c, 0.108, ZT1, ZT1 + 0.01, KUM, n=24, kat=KT)
y.prizma(c, 0.062, ZT1 + 0.01, ZT2 - 0.032, SIV, n=24, ust=False)
for kk in range(24):
    if kk % 3 != 1: continue
    tw = TAU * (kk + 0.5) / 24
    ex = V(-math.sin(tw), math.cos(tw)); nrm = radyal(tw)
    o = C + nrm * (0.062 * math.cos(math.pi / 24))
    kapi_ = kk % 6 == 1
    pencere_kutu(y, o, ex, nrm, -0.009, ZT1 + 0.01 if kapi_ else ZT1 + 0.075, 0.018, 0.075 if kapi_ else 0.045, 'koyu', cerceve='kum_acik')
for kk in range(12):
    tp = D(30 * kk + 15)
    pc = P(tp, 0.094)
    iyon_hafif(y, pc.x, pc.y, ZT1 + 0.01, ZT2 - 0.032, 0.0085, SIV, 'siva_krem', n=8, aci=tp)
ring_ = cokgen(c, 0.103, 24, KT)
y.serit([p + Z * (ZT2 - 0.032) for p in ring_], [p + Z * (ZT2 - 0.014) for p in ring_], 'siva_krem')
y.yuz_yon([p + Z * (ZT2 - 0.032) for p in ring_], 'ahsap_koyu', -Z)
halka_kornis(y, c, 0.103, ZT2 - 0.027, 0.008, 0.0025, 24, 'boya_kirmizi', kat=KT)
kavetto(y, ring_, ZT2 - 0.014, 0.03, 0.02, 'siva_krem')
ZT2c = ZT2 + 0.016
# the lookout
ZT3 = ZT2c + 0.11
y.prizma(c, 0.058, ZT2c, ZT3 - 0.026, SIV, n=24, ust=False)
halka_kornis(y, c, 0.058, ZT2c, 0.012, 0.006, 24, KUM, profil='kaide')
for kk in range(24):
    if kk % 4 != 0: continue
    tw = TAU * (kk + 0.5) / 24
    ex = V(-math.sin(tw), math.cos(tw)); nrm = radyal(tw)
    o = C + nrm * (0.058 * math.cos(math.pi / 24))
    pencere_kutu(y, o, ex, nrm, -0.008, ZT2c + 0.03, 0.016, 0.042, 'koyu', cerceve='kum_acik')
halka_kornis(y, c, 0.058, ZT3 - 0.034, 0.008, 0.0025, 24, 'boya_kirmizi')
kavetto(y, cokgen(c, 0.058, 24), ZT3 - 0.026, 0.026, 0.017, 'siva_krem')
parapet(y, cokgen(c, 0.075, 24), ZT3, 0.008, 0.016, 0.01, SIV)
kutu_merkez(y, c, 0.032, 0.032, 0.018, KUM, z0=ZT3)
tanit_heykel(y, C.x, C.y, ZT3 + 0.018, 0.075, 'bronz', aci=D(-125))
sancak(y, C.x + 0.045, C.y + 0.045, ZT3, boy=0.22, en=0.11, yuk=0.065, aci=D(160))


# ================================================================ the sea wall, the harbour mouth
y.bolum('Deniz suru ve liman ağzı')
for s in (-1, 1):
    xa, xb = sorted((s * (MX + 0.12), s * (X1 - 0.12)))
    sur(y, [V(xa, Y0), V(xb, Y0)], ZK, 0.13, 0.045, KUM, mazgal_h=0.022, parapet_h=0.01)
    silme(y, [V(xa, Y0), V(xb, Y0)], ZK, 0.02, 0.008, KUMK, 'kaide', kapali=False)
    xa, xb = sorted((s * MX, s * (MX + 0.12)))
    pon_kule(xa, xb, Y0, Y0 + 0.12, ZK, 0.3)
    xa, xb = sorted((s * X1, s * (X1 - 0.12)))
    pon_kule(xa, xb, Y0, Y0 + 0.12, ZK, 0.22)
sancak(y, MX + 0.06, Y0 + 0.06, ZK + 0.3, boy=0.18, en=0.09, yuk=0.055, aci=D(150))
# the chain across the mouth
pts = [V(-MX, Y0 + 0.04, ZK + 0.05)] + [V(-MX + 2 * MX * k / 8, Y0 + 0.04, ZS + 0.004 + (ZK + 0.046 - ZS) * ((k / 4 - 1) ** 2)) for k in range(1, 8)] + \
      [V(MX, Y0 + 0.04, ZK + 0.05)]
boru(y, pts, 0.0035, 'demir', n=5)


# ================================================================ warehouses, houses, goods
def amfora(x, yy, z, s=1.0, key='siva_oker'):
    donel(y, (x, yy), [(0.004 * s, z), (0.012 * s, z + 0.014 * s), (0.006 * s, z + 0.028 * s), (0.0045 * s, z + 0.036 * s), (0, z + 0.036 * s)], key, n=6)


def ambar(x0, x1, y0, y1, h, kapi_yon=1, adim=0.075):
    """a long whitewashed warehouse: flat roof with a parapet, a small cavetto cornice, a row of doors on the side
    facing kapi_yon (+1: +y) and small windows high up"""
    kutu(y, V(x0, y0, ZK), X, x1 - x0, y1 - y0, h, SIV, 'onarkasagsol')
    k = dikdortgen(x0, x1, y0, y1)
    y.yuz_yon([V(p.x, p.y, ZK + h) for p in k], 'siva_krem', Z)
    silme(y, k, ZK, 0.012, 0.005, KUM, 'kaide')
    silme(y, k, ZK + h - 0.02, 0.02, 0.012, 'siva_krem', KAVETTO)
    duvarlar(y, disa(k, 0.012), ZK + h, ZK + h + 0.008, SIV, ust='siva_krem', kalinlik=0.008)
    n = max(1, int((x1 - x0) / adim))
    yv = y1 if kapi_yon > 0 else y0
    ex = X if kapi_yon < 0 else -X
    o = V(x1, yv) if kapi_yon > 0 else V(x0, yv)
    for i in range(n):
        u = (x1 - x0) * (i + 0.5) / n
        pencere_kutu(y, o, ex, V(0, kapi_yon), u - 0.012, 0.0 + ZK, 0.024, min(0.05, h * 0.6), 'ahsap_koyu', cerceve='kum_acik')
        pencere_kutu(y, o, ex, V(0, kapi_yon), u - 0.009, ZK + h * 0.6, 0.018, 0.028, 'koyu', cerceve='kum_acik')
    # the upper storey's windows on the back (seen over the sea wall), a string course
    yb = y0 if kapi_yon > 0 else y1
    ob = V(x0, yb) if kapi_yon > 0 else V(x1, yb)
    for i in range(n * 2):
        u = (x1 - x0) * (i + 0.5) / (n * 2)
        pencere_kutu(y, ob, -ex, V(0, -kapi_yon), u - 0.007, ZK + h * 0.58, 0.014, 0.026, 'koyu')
    silme(y, k, ZK + h * 0.48, 0.007, 0.004, 'siva_krem', 'duz')
    # stair huts and a reed-shaded loft on the roof terrace
    zr = ZK + h
    for i, f_ in enumerate((0.18, 0.55, 0.85)):
        xm = x0 + (x1 - x0) * f_
        if i == 1:
            w_, d_ = 0.14, (y1 - y0) * 0.55
            kutu(y, V(xm - w_ / 2, y0 + 0.012, zr), X, w_, d_, 0.045, SIV, 'onarkasagsol')
            kk_ = dikdortgen(xm - w_ / 2, xm + w_ / 2, y0 + 0.012, y0 + 0.012 + d_)
            y.yuz_yon([V(p.x, p.y, zr + 0.045) for p in kk_], 'siva_krem', Z)
            duvarlar(y, kk_, zr + 0.045, zr + 0.052, SIV, ust='siva_krem', kalinlik=0.005)
            for j in range(3):
                pencere_kutu(y, V(xm + w_ / 2, y0 + 0.012), -X, -Y, w_ * (j + 0.5) / 3 - 0.006, zr + 0.014, 0.012, 0.02, 'koyu')
            for px in (xm - w_ / 2 - 0.05, xm + w_ / 2 + 0.05):   # awnings on poles beside it
                for py in (y0 + 0.02, y1 - 0.02):
                    y.prizma((px, py), 0.0018, zr, zr + 0.035, 'ahsap', n=4, ust=False)
                kutu(y, V(px - 0.045, y0 + 0.012, zr + 0.035), X, 0.09, y1 - y0 - 0.024, 0.003, 'saz', 'onarkasagsolust')
                y.yuz_yon([V(px - 0.045, y0 + 0.012, zr + 0.035), V(px + 0.045, y0 + 0.012, zr + 0.035), V(px + 0.045, y1 - 0.012, zr + 0.035),
                           V(px - 0.045, y1 - 0.012, zr + 0.035)], 'saz', -Z)
        else:
            kutu(y, V(xm - 0.03, y1 - 0.06, zr), X, 0.06, 0.05, 0.035, SIV, 'onarkasagsolust')
            pencere_kutu(y, V(xm + 0.03, y1 - 0.01), -X, Y, 0.02, zr, 0.018, 0.026, 'ahsap_koyu')


y.bolum('Ticaret limanı: ambarlar, mallar')
for s in (-1, 1):
    xa, xb = sorted((s * (MX + 0.15), s * (HX - 0.02)))
    ambar(xa, xb, Y0 + 0.06, HY0 - 0.056, 0.17, 1)
    # merchants' houses on the side quays, doors to the water
    pon_ev(y, s * 1.02, -0.92, ZK, 0.13, 0.12, 0.1, aci=-s * math.pi / 2, tohum=41 + s)
    pon_ev(y, s * 1.04, -0.75, ZK, 0.15, 0.11, 0.13, aci=-s * math.pi / 2, tohum=47 + s)
# amphorae and bales on the quays, a crane
gk = random.Random(5)
for s in (-1, 1):
    for k in range(10):
        xx = s * (0.27 + 0.022 * (k % 5)); yy = HY0 - 0.03 - 0.016 * (k // 5)
        amfora(xx, yy, ZK, 1.0, 'siva_oker' if k % 3 else 'kirmizi')
    for k in range(4):
        kutu_merkez(y, (s * (0.5 + 0.05 * k), HY0 - 0.03), 0.035, 0.026, 0.022, 'kumas' if k % 2 else 'saz', z0=ZK, aci=0.3 * k)
    for k in range(6):
        amfora(s * (0.25 + 0.024 * k), YQ + 0.04, ZK, 1.0, 'siva_oker')
TP = V(-0.62, HY0 - 0.035, ZK + 0.2)
for a in (D(160), D(20)):
    cubuk(y, V(-0.62 + 0.05 * math.cos(a), HY0 - 0.035 - 0.03 * math.sin(a), ZK), TP, 0.007, 'ahsap')
cubuk(y, TP, TP + V(0, 0.09, 0.02), 0.006, 'ahsap')
boru(y, [TP + V(0, 0.09, 0.02), TP + V(0, 0.09, -0.12)], 0.0015, 'ahsap_koyu', n=4)
kutu_merkez(y, (-0.62, HY0 + 0.055), 0.03, 0.03, 0.024, 'saz', z0=ZK + 0.06)
y.yuz_yon([V(-0.635, HY0 + 0.04, ZK + 0.06), V(-0.605, HY0 + 0.04, ZK + 0.06), V(-0.605, HY0 + 0.07, ZK + 0.06), V(-0.635, HY0 + 0.07, ZK + 0.06)], 'saz', -Z)

y.bolum('Kent: Pön evleri, palmiyeler')
gh = random.Random(9)
gk_ = random.Random(19)
evler = []


def bos_mu(x0, x1, y0, y1, pay=0.02):
    for (a0, a1, b0, b1) in evler:
        if x0 < a1 + pay and x1 > a0 - pay and y0 < b1 + pay and y1 > b0 - pay: return False
    for cx_, cy_ in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        if (V(cx_, cy_) - C).length < RA + 0.045: return False
    if not (X0 + 0.03 < x0 and x1 < X1 - 0.03 and YQ + 0.05 < y0 and y1 < Y1 - 0.03): return False
    if y0 < -0.35 and abs(x0 + x1) / 2 < 0.36: return False          # the water gate
    if y1 > 0.95 and x0 < 0.52 and x1 > 0.37: return False           # the road from the island gate
    return True


for j in range(16):
    for i in range(20):
        cx_ = -1.13 + 0.12 * i + gh.uniform(-0.02, 0.02)
        cy_ = -0.58 + 0.12 * j + gh.uniform(-0.02, 0.02)
        w, d = gh.uniform(0.075, 0.115), gh.uniform(0.07, 0.1)
        if bos_mu(cx_ - w / 2, cx_ + w / 2, cy_ - d / 2, cy_ + d / 2):
            evler.append((cx_ - w / 2, cx_ + w / 2, cy_ - d / 2, cy_ + d / 2))
            # the door towards the harbour wall
            yon = math.atan2(C.y - cy_, C.x - cx_)
            aci = round((yon + math.pi / 2) / (math.pi / 2)) * (math.pi / 2)
            ww, dd = (w, d) if abs(math.sin(aci)) < 0.5 else (d, w)
            hh = gh.uniform(0.05, 0.085)
            pon_ev(y, cx_, cy_, ZK, ww, dd, hh, aci=aci, tohum=100 + len(evler),
                   duvar=gh.choice((SIV, SIV, SIV, 'siva_krem')))
            if gk_.random() < 0.4:   # a cavetto cornice under the parapet on many of them
                with parca(y, (cx_, cy_, ZK), aci):
                    silme(y, dikdortgen(-ww / 2, ww / 2, -dd / 2, dd / 2), hh - 0.012, 0.012, 0.005, 'siva_krem', KAVETTO_H)
palm = random.Random(3)
nk = 0
for _ in range(400):
    if nk >= 11: break
    px, py = palm.uniform(X0 + 0.05, X1 - 0.05), palm.uniform(YQ + 0.06, Y1 - 0.05)
    if bos_mu(px - 0.03, px + 0.03, py - 0.03, py + 0.03, pay=0.0):
        agac(y, px, py, ZK, palm.uniform(0.11, 0.15), 'palmiye', 'zeytin', 'ahsap_acik')
        evler.append((px - 0.02, px + 0.02, py - 0.02, py + 0.02)); nk += 1
# the road from the island gate
t = D(60); o = P(t, RA)
y.yuz_yon([V(o.x - 0.035, o.y, ZK + 0.002), V(o.x + 0.035, o.y - 0.02, ZK + 0.002), V(0.48, Y1, ZK + 0.002), V(0.41, Y1, ZK + 0.002)], 'zemin', Z)


# ================================================================ ships
y.bolum('Gemiler')
for t_, yon, tohum in ((D(212), 1, 3), (D(-28), 1, 4), (D(130), -1, 5)):
    p = P(t_, 0.43, ZS)
    gemi(y, p, t_ + yon * math.pi / 2, 0.0, L=0.25, B=0.045, H=0.026, kurek=True, tohum=tohum)
gemi(y, V(0.04, -0.88, ZS), D(90), 0.0, L=0.24, B=0.072, H=0.028, kurek=False, yelken=True, tur='ticaret', tohum=11)
gemi(y, V(-0.5, -0.95 + 0.0, ZS), D(0), 0.0, L=0.24, B=0.07, H=0.028, kurek=False, tur='ticaret', tohum=12)
gemi(y, V(0.55, -0.71, ZS), D(180), 0.0, L=0.22, B=0.068, H=0.026, kurek=False, tur='ticaret', tohum=13)

# the whole harbour scaled down a little (its longest side to ~2.45 like the other landmarks)
OLC = 2.45 / 2.53
for i in range(len(y.faces)):
    pts, key = y.faces[i]
    y.faces[i] = ([(p[0] * OLC, p[1] * OLC, p[2] * OLC) for p in pts], key)

calistir(y, 'lm_kothon')
