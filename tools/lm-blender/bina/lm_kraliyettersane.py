# Kraliyet Tersanesi (lm_kraliyettersane): the Royal Dockyard at Chatham. A three-decker ship of the line in black and
# yellow ochre moored at the quay (masts, yards with furled sails and loosed topsails, shrouds, the ensign); a new
# ship on the slip in frame (keel, ribs, the lower strakes planked) inside scaffolding with shipwrights; a stone dry
# dock with stepped altars, a caisson gate and a copper-bottomed frigate on shores; the long brick ropery; the
# clock-tower storehouse; timber sheds and stacks; sheer legs and a treadwheel crane; the Medway.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from ingiliz_ek import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.06
ZW = 0.025
KY = -0.75
TUG, TS, CATI = 'tugla', 'tas_acik', 'arduvaz'
rs = __import__('random').Random(7)

# ---------------------------------------------------------------- the hull
VS = [0.0, 0.12, 0.3, 0.48, 0.64, 0.8, 1.0]       # levels, keel to rail
SS = [0.12, 0.55, 0.88, 1.0, 0.98, 0.93, 0.86]    # half breadth at each level (tumblehome above)
SIYAH, SARI = 'koyu', 'boya_sari'


PORTLAR = ((2, 12, -0.72, 0.62, 0.32), (4, 13, -0.78, 0.68, 0.32))


def govde(c, aci, L, B, D, z0, bantlar, plank=6, n=16, port=True, ic_renk='ahsap_acik', portlar=PORTLAR, wale=()):
    """a ship's hull along local x (bow +x) round c at keel height z0: L long, B half beam, D keel to rail amidships.
    bantlar: a key for each of the six bands between the levels; plank < 6: only the bands below that level are
    planked (a ship in frame: ribs, keel, stem and sternpost above). portlar: rows of gunports (band, count, u0, u1,
    height share); wale: levels where a black wale strake runs proud of the side. Returns P(u, j, s) (local points)
    and the transform"""
    def bb(u):
        return (1 - min(1.0, u) ** 2.4) ** 0.55 if u >= 0 else 1 - 0.32 * (-u) ** 2.2
    def zz(u, j):
        v = VS[j]
        z = D * v + D * 0.38 * (1 - v) ** 2 * max(0.0, u - 0.55) / 0.45 + D * 0.12 * (1 - v) ** 2 * max(0.0, -u - 0.75) / 0.25
        z += D * (0.07 * u * u + 0.12 * max(0.0, min(1.0, (-u - 0.4) / 0.15))) * v ** 3   # sheer, the quarterdeck
        return z
    P = lambda u, j, s, k=1.0: V(u * L / 2, s * B * bb(u) * SS[j] * k, zz(u, j))
    us = [-1 + 2 * i / n for i in range(n + 1)]
    with parca(y, (c[0], c[1], z0), aci):
        for s in (-1, 1):
            for i in range(n):
                ua, ub = us[i], us[i + 1]
                for j in range(min(plank, 6)):
                    q = [P(ua, j + 1, s), P(ub, j + 1, s), P(ub, j, s), P(ua, j, s)]
                    m = (q[0] + q[1] + q[2] + q[3]) / 4
                    yuz_dis(y, q, bantlar[j], V(m.x, 0, m.z + D * 0.05))
                    if plank < 6:   # the inside of the planking
                        qi = [P(ua, j + 1, s, 0.96), P(ub, j + 1, s, 0.96), P(ub, j, s, 0.9), P(ua, j, s, 0.9)]
                        yuz_dis(y, qi, ic_renk, V(m.x, s * B * 3, m.z))
                if plank < 6:   # the top edge of the planking
                    y.yuz_yon([P(ua, plank, s), P(ub, plank, s), P(ub, plank, s, 0.96), P(ua, plank, s, 0.96)], 'ahsap', Z)
                else:
                    # the bulwark's inside above the deck, the rail
                    y.yuz_yon([P(ua, 5, s, 0.96), P(ub, 5, s, 0.96), P(ub, 6, s, 0.96), P(ua, 6, s, 0.96)], 'ahsap_koyu', V(0, -s, 0.2))
                    y.yuz_yon([P(ua, 6, s, 0.96), P(ub, 6, s, 0.96), P(ub, 6, s), P(ua, 6, s)], 'ahsap', Z)
        if plank >= 6:
            for i in range(n):   # the deck
                ua, ub = us[i], us[i + 1]
                y.yuz_yon([P(ua, 5, -1, 0.96), P(ub, 5, -1, 0.96), P(ub, 5, 1, 0.96), P(ua, 5, 1, 0.96)], 'ahsap_acik', Z)
            # the transom with the stern windows, galleries and carvings
            y.yuz_yon([P(-1, j, 1) for j in range(7)] + [P(-1, j, -1) for j in reversed(range(7))], SIYAH, -X)
            ix = X * 0.004   # (the bulwark's inside at the stern, a little in from the transom: back to back they flickered)
            y.yuz_yon([P(-1, 5, 1, 0.96) + ix, P(-1, 6, 1, 0.96) + ix, P(-1, 6, -1, 0.96) + ix, P(-1, 5, -1, 0.96) + ix], 'ahsap_koyu', X)
            y.yuz_yon([P(-1, 6, 1, 0.96), P(-1, 6, -1, 0.96), P(-1, 6, -1, 0.96) + ix, P(-1, 6, 1, 0.96) + ix], 'ahsap', Z)
            w = B * bb(-1)
            for row, (za, zb) in enumerate(((zz(-1, 4) + D * 0.03, zz(-1, 5) - D * 0.02), (zz(-1, 5) + D * 0.03, zz(-1, 6) - D * 0.04))):
                y.yuz_yon([V(-L / 2 - 0.0015, -w * 0.78, za - 0.004), V(-L / 2 - 0.0015, w * 0.78, za - 0.004), V(-L / 2 - 0.0015, w * 0.78, zb + 0.004),
                           V(-L / 2 - 0.0015, -w * 0.78, zb + 0.004)], 'altin', -X)
                for k in range(5):
                    yc = -w * 0.62 + k * w * 0.31
                    y.yuz_yon([V(-L / 2 - 0.0025, yc - w * 0.1, za), V(-L / 2 - 0.0025, yc + w * 0.1, za), V(-L / 2 - 0.0025, yc + w * 0.1, zb),
                               V(-L / 2 - 0.0025, yc - w * 0.1, zb)], 'cam', -X)
            for s in (-1, 1):   # quarter galleries
                q0 = P(-0.86, 4, s)
                kutu3(y, V(q0.x, q0.y + s * 0.006, q0.z + D * 0.12), X, Y, Z, L * 0.08, 0.014, D * 0.26, 'altin', ('+x', '-x', '+y' if s > 0 else '-y', '+z', '-z'))
                kutu3(y, V(q0.x, q0.y + s * 0.0135, q0.z + D * 0.12), X, Y, Z, L * 0.05, 0.002, D * 0.14, 'cam', ('+y' if s > 0 else '-y',))
            for k in (-1, 0, 1):   # stern lanterns
                p = P(-1, 6, 1)
                kure(y, (p.x - 0.006, k * B * 0.35, p.z + 0.02), 0.008, 'altin', n=6, kat=3)
                y.prizma((p.x - 0.006, k * B * 0.35), 0.0018, p.z, p.z + 0.014, 'altin', n=4)
            # the figurehead and the beakhead
            p = P(1, 4, 1)
            kure(y, (p.x + 0.012, 0, p.z), D * 0.09, 'altin', n=8, kat=4)
            # gunports: two rows of black ports in the yellow bands, a row of small ports on the quarterdeck
            if port:
                for s in (-1, 1):
                    for (j, nport, u0, u1, hp) in portlar:
                        for k in range(nport):
                            u = u0 + (u1 - u0) * (k + 0.5) / nport
                            pa, pb = P(u, j, s), P(u, j + 1, s)
                            m = (pa + pb) / 2 + V(0, s * 0.0018, 0)
                            hh = (pb.z - pa.z) * hp; ww = L * 0.016
                            y.yuz_yon([m + V(-ww, 0, -hh), m + V(ww, 0, -hh), m + V(ww, 0, hh), m + V(-ww, 0, hh)], SIYAH, V(0, s, 0))
                # wales: black strakes standing a little proud of the side, along the whole length
                for lv in wale:
                    j0 = int(lv)
                    lp = lambda u, t, s, k=1.0: P(u, j0, s, k).lerp(P(u, j0 + 1, s, k), t)
                    t0, t1 = lv - j0 - 0.07, lv - j0 + 0.07
                    for s in (-1, 1):
                        for i in range(n):
                            ua, ub = us[i], us[i + 1]
                            q = [lp(ua, t1, s, 1.025), lp(ub, t1, s, 1.025), lp(ub, t0, s, 1.025), lp(ua, t0, s, 1.025)]
                            m = (q[0] + q[1] + q[2] + q[3]) / 4
                            yuz_dis(y, q, SIYAH, V(m.x, 0, m.z))
                            for (t_, yon) in ((t1, Z), (t0, -Z)):   # its top and bottom edges back to the side
                                e = [lp(ua, t_, s, 1.025), lp(ub, t_, s, 1.025), lp(ub, t_, s), lp(ua, t_, s)]
                                y.yuz_yon(e, SIYAH, yon + V(0, s * 0.3, 0))
                        for (u_, yon) in ((-1.0, -X), (1.0, X)):   # its ends at the stem and the stern
                            y.yuz_yon([lp(u_, t0, s), lp(u_, t1, s), lp(u_, t1, s, 1.025), lp(u_, t0, s, 1.025)], SIYAH, yon)
        else:
            # in frame: the planking's raw end at the stern (outer and inner skin joined: through the gap
            # the backs of the planks showed)
            for s in (-1, 1):
                for j in range(min(plank, 6)):
                    y.yuz_yon([P(-1, j, s), P(-1, j + 1, s), P(-1, j + 1, s, 0.96), P(-1, j, s, 0.9)], 'ahsap_koyu', -X)
            # ribs above the planking, keel, stem, sternpost, deck beams
            for i in range(1, n):
                u = us[i]
                for s in (-1, 1):
                    boru(y, [P(u, j, s) for j in range(plank, 7)], 0.0035, 'ahsap_acik', n=4)
                if i % 2 == 0:
                    cubuk(y, P(u, 5, -1, 0.97), P(u, 5, 1, 0.97), 0.006, 'ahsap', 0.005)
            boru(y, [P(1, j, 1) for j in range(7)], 0.005, 'ahsap', n=5)
            boru(y, [V(-L / 2, 0, zz(-1, 0)), V(-L / 2, 0, zz(-1, 6) + 0.02)], 0.005, 'ahsap', n=5)
            for s in (-1, 1):
                boru(y, [P(-1, j, s) for j in range(plank, 7)], 0.0035, 'ahsap_acik', n=4)
        cubuk(y, V(-L / 2, 0, -0.003), V(L / 2, 0, zz(1, 0) - 0.003), 0.012, 'ahsap_koyu', 0.008)   # the keel
    return P, bb, zz


def direkler(c, aci, L, B, D, z0, P, bb, zz, yelken=True):
    """three masts with tops, yards with furled sails (the topsails loosed), the bowsprit, shrouds and stays"""
    k_ = (math.cos(aci), math.sin(aci))
    W = lambda p: V(c[0] + k_[0] * p.x - k_[1] * p.y, c[1] + k_[1] * p.x + k_[0] * p.y, z0 + p.z)
    tops = []
    for (u, hh, yl) in ((0.5, 0.88, 0.44), (0.02, 1.0, 0.5), (-0.52, 0.72, 0.34)):
        x = u * L / 2
        zd = zz(u, 5)
        H = hh * L
        mast = [V(x, 0, zd), V(x, 0, zd + H * 0.48), V(x, 0, zd + H * 0.5), V(x, 0, zd + H * 0.82), V(x, 0, zd + H * 0.84), V(x, 0, zd + H)]
        boru(y, [W(mast[0]), W(mast[1])], 0.0085, 'ahsap', n=6)
        boru(y, [W(mast[2] - Z * 0.03), W(mast[3])], 0.0058, 'ahsap', n=6)
        boru(y, [W(mast[4] - Z * 0.03), W(mast[5])], 0.0038, 'ahsap', n=5)
        # the top (platform) and the crosstrees
        tc = W(mast[1])
        kutu3(y, tc, V(k_[0], k_[1]), V(-k_[1], k_[0]), Z, 0.04, 0.06, 0.006, 'ahsap_koyu')
        kutu3(y, W(mast[3]), V(k_[0], k_[1]), V(-k_[1], k_[0]), Z, 0.014, 0.04, 0.004, 'ahsap_koyu')
        tops.append((W(mast[1]), W(mast[3]), W(mast[5])))
        # yards: course, topsail, topgallant
        for (t, ln, loose) in ((0.4, yl, False), (0.68, yl * 0.74, yelken), (0.9, yl * 0.5, False)):
            zy = zd + H * t
            a, b = W(V(x, -ln * L / 2, zy)), W(V(x, ln * L / 2, zy))
            boru(y, [a, b], 0.0032, 'ahsap_koyu', n=4)
            if loose:   # a topsail let fall to dry: a slightly bellied sheet down to the yard below
                zb = zd + H * 0.42
                lb = yl * L / 2 * 0.95
                # (clear of the masts: nearer, the topmast poked through the sail as a dark slot)
                pts = [W(V(x + 0.009, -ln * L / 2, zy - 0.006)), W(V(x + 0.009, ln * L / 2, zy - 0.006)), W(V(x + 0.017, lb, zb + 0.008)), W(V(x + 0.017, -lb, zb + 0.008))]
                ort = (pts[0] + pts[1] + pts[2] + pts[3]) / 4 + (W(V(x + 0.03, 0, (zy + zb) / 2)) - W(V(x, 0, (zy + zb) / 2)))
                yon = W(V(x + 1, 0, 0)) - W(V(x, 0, 0))
                levha(y, [pts[0], pts[1], (pts[1] + pts[2]) / 2 + yon * 0.012, pts[2], pts[3], (pts[3] + pts[0]) / 2 + yon * 0.012], 'kece', yon)
            else:
                boru(y, [W(V(x + 0.006, -ln * L / 2 * 0.9, zy - 0.006)), W(V(x + 0.006, 0, zy - 0.01)), W(V(x + 0.006, ln * L / 2 * 0.9, zy - 0.006))],
                     0.0075 if t < 0.5 else 0.0058, 'kece', n=5)
        # shrouds from the channels to the top and the topmast crosstrees
        for s in (-1, 1):
            for k in range(4):
                ub = u - 0.06 + k * 0.03
                ch = P(ub, 6, s, 1.08)
                boru(y, [W(ch), W(V(x, s * 0.024, zd + H * 0.47))], 0.0011, 'koyu', n=3, kapat=False)
            boru(y, [W(V(x, s * 0.028, zd + H * 0.5)), W(V(x, s * 0.006, zd + H * 0.8))], 0.0009, 'koyu', n=3, kapat=False)
    # the bowsprit and jib boom
    bs = P(1, 6, 1); bs = V(bs.x - 0.04, 0, bs.z)
    be = bs + V(L * 0.3, 0, L * 0.12)
    boru(y, [W(bs), W(be)], 0.0065, 'ahsap', n=6, r_son=0.004)
    boru(y, [W(be - V(0.02, 0, 0.01)), W(be + V(L * 0.12, 0, L * 0.04))], 0.003, 'ahsap', n=4)
    # stays: fore topmast to the jib boom, main to fore, mizzen to main
    (f1, f2, f3), (m1, m2, m3), (z1_, z2_, z3_) = tops
    for a, b in ((f2, W(be)), (f3, W(be + V(L * 0.11, 0, L * 0.035))), (m2, f1), (m3, f2), (z2_, m1), (z3_, m2), (f1, W(bs))):
        boru(y, [a, b], 0.0009, 'koyu', n=3, kapat=False)
    return tops


# ---------------------------------------------------------------- ground, the Medway, the quay
y.bolum('Zemin, Medway ve rıhtım')
DX0, DX1 = -0.47, -0.05          # the dry dock (top edges)
SLX0, SLX1 = -1.02, -0.62        # the slip
su_ve_kiyi(y, -1.2, 1.2, -1.2, KY, ZW, Z0, KY, 'granit', rihtim=False)
kutu(y, V(-1.2, KY, 0), X, 2.4, 1.02 - KY, Z0, 'granit_koyu', 'arkasagsol')
for (x0, x1) in ((-1.2, SLX0), (SLX1, DX0), (DX1, 1.2)):   # the quay wall, broken by the slip and the dock
    duz_duvar(y, V(x0, KY), V(x1, KY), ZW - 0.006, Z0, 'granit')
    silme(y, [V(x0, KY), V(x1, KY)], Z0 - 0.007, 0.009, 0.007, TS, 'duz', kapali=False)
yt = lambda x0, x1, y0, y1, k='zemin', dz=0.0: y.yuz_yon([V(x0, y0, Z0 + dz), V(x1, y0, Z0 + dz), V(x1, y1, Z0 + dz), V(x0, y1, Z0 + dz)], k, Z)
yt(-1.2, DX0, KY, 1.02, 'toprak')
yt(DX1, 1.2, KY, 1.02, 'toprak')
yt(DX0, DX1, 0.3, 1.02, 'toprak')
yt(DX1, 1.2, KY, -0.6, 'zemin', 0.0012)         # the paved quay
yt(-0.6, DX0, KY, -0.6, 'zemin', 0.0012)
for k in range(9):   # bollards along the quay
    x = 0.05 + k * 0.12
    y.prizma((x, KY + 0.02), 0.008, Z0, Z0 + 0.022, 'demir', n=8)
    kure(y, (x, KY + 0.02, Z0 + 0.024), 0.009, 'demir', n=8, kat=3)

# ---------------------------------------------------------------- the dry dock
y.bolum('Kuru havuz ve fırkateyn')
DY0, DY1 = KY, 0.3
ZB = 0.006
ADIM = 4
dz_ = (Z0 - ZB) / ADIM
for k in range(ADIM):   # stepped altars down both sides and the head
    o = 0.026 * k
    za, zb_ = Z0 - k * dz_, Z0 - (k + 1) * dz_
    x0, x1, y1 = DX0 + o, DX1 - o, DY1 - o
    duz_duvar(y, V(x0, DY0), V(x0, y1), zb_, za, 'granit')
    duz_duvar(y, V(x1, y1), V(x1, DY0), zb_, za, 'granit')
    duz_duvar(y, V(x0, y1), V(x1, y1), zb_, za, 'granit')
    if k < ADIM - 1:
        o2 = 0.026 * (k + 1)
        y.yuz_yon([V(x0, DY0, zb_), V(x0 + 0.026, DY0, zb_), V(x0 + 0.026, y1 - 0.026, zb_), V(x0, y1, zb_)], 'tas', Z)
        y.yuz_yon([V(x1 - 0.026, DY0, zb_), V(x1, DY0, zb_), V(x1, y1, zb_), V(x1 - 0.026, y1 - 0.026, zb_)], 'tas', Z)
        y.yuz_yon([V(x0 + 0.026, y1 - 0.026, zb_), V(x1 - 0.026, y1 - 0.026, zb_), V(x1, y1, zb_), V(x0, y1, zb_)], 'tas', Z)
xb0, xb1, yb1 = DX0 + 0.026 * ADIM, DX1 - 0.026 * ADIM, DY1 - 0.026 * ADIM
y.yuz_yon([V(xb0, DY0, ZB), V(xb1, DY0, ZB), V(xb1, yb1, ZB), V(xb0, yb1, ZB)], 'tas_koyu', Z)
# the dock's ends at the river: the stepped profile closed by the caisson
for k in range(ADIM):
    o = 0.026 * k
    za, zb_ = Z0 - k * dz_, Z0 - (k + 1) * dz_
    for (xa, xb_, s) in ((DX0, DX0 + o, -1), (DX1 - o, DX1, 1)):
        if xb_ - xa > 1e-6:
            y.yuz_yon([V(xa, DY0, zb_), V(xb_, DY0, zb_), V(xb_, DY0, za), V(xa, DY0, za)], 'granit', -Y)
kutu(y, V(DX0, DY0 - 0.03, ZW - 0.008), X, DX1 - DX0, 0.03, Z0 - ZW + 0.008 + 0.004, 'ahsap_koyu', 'onarkasagsolust')   # the caisson
for k in range(4):
    x = DX0 + 0.04 + k * (DX1 - DX0 - 0.08) / 3
    y.yuz_yon([V(x - 0.003, DY0 - 0.0315, ZW), V(x + 0.003, DY0 - 0.0315, ZW), V(x + 0.003, DY0 - 0.0315, Z0), V(x - 0.003, DY0 - 0.0315, Z0)], 'demir', -Y)
# keel blocks and the frigate on her shores
FC = ((DX0 + DX1) / 2, (DY0 + DY1) / 2 + 0.02)
for k in range(9):
    yy = FC[1] - 0.34 + k * 0.085
    kutu_merkez(y, (FC[0], yy), 0.03, 0.02, 0.014, 'ahsap', z0=ZB)
FL, FB, FD = 0.74, 0.07, 0.12
Pf, bbf, zzf = govde(FC, math.pi / 2, FL, FB, FD, ZB + 0.017, ['bronz', 'bronz', SIYAH, SIYAH, SARI, SIYAH], plank=6, n=14,
                     portlar=((4, 11, -0.7, 0.62, 0.3),))
for k in range(5):   # the shores from the altars to the hull
    u = -0.6 + k * 0.3
    for s in (-1, 1):
        p = Pf(u, 3, s)
        hp = V(FC[0] - p.y, FC[1] + p.x, ZB + 0.017 + p.z)
        if s < 0: foot = V(DX1 - 0.04, hp.y, Z0 - 2 * dz_ + 0.002)
        else: foot = V(DX0 + 0.04, hp.y, Z0 - 2 * dz_ + 0.002)
        cubuk(y, foot, hp, 0.005, 'ahsap_acik')
# the frigate under refit keeps only her lower masts (with their tops) and the bowsprit
for (u, hh) in ((0.5, 0.24), (0.02, 0.28), (-0.52, 0.2)):
    zd = ZB + 0.017 + zzf(u, 5)
    mx, my = FC[0], FC[1] + u * FL / 2
    boru(y, [V(mx, my, zd), V(mx, my, zd + hh)], 0.0075, 'ahsap', n=6)
    kutu3(y, V(mx, my, zd + hh * 0.86), Y, -X, Z, 0.034, 0.05, 0.005, 'ahsap_koyu')
    boru(y, [V(mx, my, zd + hh * 0.86), V(mx, my, zd + hh + 0.05)], 0.0045, 'ahsap', n=5)
    for s in (-1, 1):   # shrouds to the channels
        ch = Pf(u, 6, s, 1.08)
        boru(y, [V(FC[0] - ch.y, FC[1] + ch.x, ZB + 0.017 + ch.z), V(mx + s * 0.02, my, zd + hh * 0.85)], 0.001, 'koyu', n=3, kapat=False)
_b = Pf(1, 6, 1)
boru(y, [V(FC[0], FC[1] + _b.x - 0.03, ZB + 0.017 + _b.z), V(FC[0], FC[1] + _b.x + 0.12, ZB + 0.017 + _b.z + 0.05)], 0.005, 'ahsap', n=6, r_son=0.003)
# shipwrights in the dock
for (x, yy) in ((FC[0] + 0.05, FC[1] - 0.2), (FC[0] - 0.06, FC[1] + 0.1), (FC[0] + 0.07, FC[1] + 0.25)):
    insan(y, x, yy, ZB, 'ahsap', 1.05, aci=rs.uniform(0, 6), sapka='kece')

# ---------------------------------------------------------------- the slip and the ship in frame
y.bolum('Kızak ve yapımdaki gemi')
SC = ((SLX0 + SLX1) / 2, -0.3)
# the slipway: a timber ramp running down into the river, the ground ways
ry0 = KY - 0.22
y.yuz_yon([V(SLX0, ry0, ZW - 0.012), V(SLX1, ry0, ZW - 0.012), V(SLX1, KY, Z0), V(SLX0, KY, Z0)], 'ahsap', V(0, -0.25, 1))
for (xa, s) in ((SLX0, -1), (SLX1, 1)):
    y.yuz_yon([V(xa, ry0, 0.0), V(xa, KY, 0.0), V(xa, KY, Z0), V(xa, ry0, ZW - 0.012)], 'granit', V(s, 0))
y.yuz_yon([V(SLX0, ry0, 0.0), V(SLX1, ry0, 0.0), V(SLX1, ry0, ZW - 0.012), V(SLX0, ry0, ZW - 0.012)], 'granit', -Y)
yt(SLX0, SLX1, KY, 0.25, 'ahsap', 0.0012)
for s in (-1, 1):
    cubuk(y, V(SC[0] + s * 0.05, ry0 + 0.02, ZW - 0.004), V(SC[0] + s * 0.05, KY, Z0 + 0.006), 0.016, 'ahsap_koyu', 0.008)
    cubuk(y, V(SC[0] + s * 0.05, KY, Z0 + 0.006), V(SC[0] + s * 0.05, 0.2, Z0 + 0.006), 0.016, 'ahsap_koyu', 0.008)
for k in range(9):
    yy = SC[1] - 0.36 + k * 0.09
    kutu_merkez(y, (SC[0], yy), 0.03, 0.03, 0.02, 'ahsap', z0=Z0)
SL_, SB_, SD_ = 0.86, 0.085, 0.17
Ps, bbs, zzs = govde(SC, math.pi / 2, SL_, SB_, SD_, Z0 + 0.024, ['ahsap'] * 6, plank=3, n=16)
# scaffolding: poles both sides, two staging levels with planks, ladders
for s in (-1, 1):
    xx = SC[0] + s * (SB_ + 0.04)
    for k in range(7):
        yy = SC[1] - 0.38 + k * 0.125
        y.prizma((xx, yy), 0.0035, Z0, Z0 + SD_ + 0.09, 'ahsap_acik', n=4)
    for zz_ in (Z0 + 0.09, Z0 + 0.17):
        kutu3(y, V(xx - s * 0.012, SC[1], zz_), X, Y, Z, 0.03, 0.76, 0.004, 'ahsap', ('+x', '-x', '+y', '-y', '+z'))
        cubuk(y, V(xx, SC[1] - 0.38, zz_ + 0.035), V(xx, SC[1] + 0.37, zz_ + 0.035), 0.003, 'ahsap_acik')
    for k in range(3):
        ya = SC[1] - 0.3 + k * 0.3
        cubuk(y, V(xx, ya, Z0 + 0.09), V(xx, ya + 0.12, Z0 + SD_ + 0.09), 0.003, 'ahsap_koyu')
    for k in range(3):   # shipwrights on the staging
        insan(y, xx - s * 0.012, SC[1] - 0.25 + k * 0.22, Z0 + 0.094 + (0.08 if k == 1 else 0), 'kece' if k % 2 else 'ahsap', 1.05, aci=math.pi if s > 0 else 0.0)
# planks waiting, a saw pit, a steam box
kereste(y, SLX0 - 0.1, -0.05, Z0, L=0.24, n=3, kat=2, en=0.012, aci=math.pi / 2)
kereste(y, SLX0 - 0.1, 0.25, Z0, L=0.2, n=2, kat=3, en=0.016, aci=math.pi / 2)
insan(y, SLX0 - 0.06, 0.4, Z0, 'kece', 1.05, aci=0.3)

# ---------------------------------------------------------------- the ship of the line at the quay
y.bolum('Rıhtımdaki savaş gemisi')
GC = (0.48, KY - 0.15)
GL, GB, GD = 0.98, 0.1, 0.17
# (a three-decker: three yellow gun-deck bands with their rows of ports, the upper two parted by a black wale)
Pg, bbg, zzg = govde(GC, math.pi, GL, GB, GD, ZW - GD * 0.3, ['bronz', 'bronz', SARI, SIYAH, SARI, SARI], plank=6, n=18,
                     portlar=((2, 12, -0.72, 0.62, 0.3), (4, 13, -0.78, 0.68, 0.27), (5, 13, -0.74, 0.64, 0.22)), wale=(5.0,))
tops = direkler(GC, math.pi, GL, GB, GD, ZW - GD * 0.3, Pg, bbg, zzg, yelken=True)
# the ensign at the taffrail, the pennant at the main truck
st = Pg(-1, 6, 1)
sancak(y, GC[0] + GL / 2 + 0.01, GC[1], ZW - GD * 0.3 + st.z, boy=0.13, en=0.11, yuk=0.07, aci=0.25, direk_key='ahsap_koyu')
mt = tops[1][2]
sancak(y, mt.x, mt.y, mt.z - 0.005, boy=0.045, en=0.09, yuk=0.03, aci=0.1, direk_key='ahsap_koyu', kuyruk=True)
# on deck: hammock nettings along the rails, the ship's boats on the booms amidships, the capstan
zg0 = ZW - GD * 0.3
Wg = lambda p: V(GC[0] - p.x, GC[1] - p.y, zg0 + p.z)       # (local -> world: the ship lies along -x)
for s in (-1, 1):
    boru(y, [Wg(Pg(u, 6, s, 0.97)) + Z * 0.006 for u in [-0.92 + k * 0.1 for k in range(17)]], 0.0042, 'kece', n=5)


def kapstan(x, yy, z, r=0.014, h=0.026):
    """a capstan: a waisted drum with a cap, the bars across it"""
    donel(y, (x, yy), [(r * 1.1, z), (r * 0.8, z + h * 0.5), (r, z + h * 0.8), (r * 1.25, z + h * 0.85), (r * 1.25, z + h), (0.0, z + h + 0.004)], 'ahsap', n=8)
    for a in (0.0, math.pi / 2):
        cubuk(y, V(x - math.cos(a) * r * 3.2, yy - math.sin(a) * r * 3.2, z + h * 0.92), V(x + math.cos(a) * r * 3.2, yy + math.sin(a) * r * 3.2, z + h * 0.92),
              0.003, 'ahsap_acik')


for k, s in enumerate((-1, 1)):
    q = Wg(Pg(0.22, 5, 0, 0.0))
    sandal(y, q.x, q.y + s * 0.03, q.z + 0.016, 0.0, L=0.085, B=0.019, kurek=False)
    cubuk(y, Wg(Pg(0.22 - 0.08, 5, s, 0.6)) + Z * 0.004, Wg(Pg(0.22 + 0.08, 5, s, 0.6)) + Z * 0.004, 0.005, 'ahsap_koyu', 0.008)
q = Wg(Pg(-0.3, 5, 0, 0.0))
kapstan(q.x, q.y, q.z, 0.012, 0.024)
# capstans at the dock head and on the quay (warping ships in and out)
for (x, yy) in ((DX0 - 0.05, DY1 - 0.04), (DX1 + 0.05, DY1 - 0.04), (DX1 + 0.05, -0.6)):
    kapstan(x, yy, Z0 + 0.001)
# casks and cordage on the quay
for k in range(6):
    varil(y, 1.08 + (k % 3) * 0.026, -0.68 + (k // 3) * 0.026, Z0 + 0.0012, 0.011, 0.028)
for k in range(3):
    donel(y, (1.1 + k * 0.04, -0.6), [(0.012, Z0 + 0.0012), (0.018, Z0 + 0.005), (0.018, Z0 + 0.012), (0.007, Z0 + 0.015), (0.0, Z0 + 0.015)], 'saz_koyu', n=10)
# the gangway to the quay
cubuk(y, V(0.62, KY - 0.06, ZW + 0.1), V(0.66, KY + 0.04, Z0 + 0.004), 0.022, 'ahsap', 0.004)
# a boat and a lighter alongside
sandal(y, 0.0, -1.0, ZW, 0.1, L=0.11, B=0.026)
sandal(y, 1.05, -1.0, ZW, 3.0, L=0.1, B=0.024)

# ---------------------------------------------------------------- sheer legs for masting, a treadwheel crane
y.bolum('Makara ve vinçler')
# sheer legs on the quay leaning over the water
for s in (-1, 1):
    cubuk(y, V(0.06 + s * 0.04, KY + 0.06, Z0), V(0.06, KY - 0.07, Z0 + 0.5), 0.008, 'ahsap')
boru(y, [V(0.06, KY - 0.07, Z0 + 0.5), V(0.06, KY + 0.25, Z0)], 0.0012, 'koyu', n=3)
boru(y, [V(0.06, KY - 0.07, Z0 + 0.49), V(0.06, KY - 0.07, Z0 + 0.22)], 0.0012, 'koyu', n=3)
kutu_merkez(y, (0.06, KY - 0.07), 0.016, 0.016, 0.02, 'ahsap_koyu', z0=Z0 + 0.2)
# the treadwheel crane: a weatherboarded house round the wheel, the jib over the dock
TCX, TCY = DX1 + 0.12, KY + 0.1
donel(y, (TCX, TCY), [(0.06, Z0), (0.06, Z0 + 0.1)], 'ahsap_dikey', n=8)
donel(y, (TCX, TCY), [(0.072, Z0 + 0.1), (0.066, Z0 + 0.11), (0.0, Z0 + 0.17)], 'kiremit', n=8)
y.yuz_yon([V(p.x, p.y, Z0 + 0.1) for p in cokgen((TCX, TCY), 0.072, 8)], 'ahsap_koyu', -Z)
cubuk(y, V(TCX - 0.03, TCY, Z0 + 0.12), V(TCX - 0.22, TCY - 0.1, Z0 + 0.25), 0.01, 'ahsap')
boru(y, [V(TCX - 0.215, TCY - 0.098, Z0 + 0.245), V(TCX - 0.215, TCY - 0.098, Z0 + 0.08)], 0.0012, 'koyu', n=3)
kutu_merkez(y, (TCX - 0.215, TCY - 0.098), 0.02, 0.05, 0.015, 'ahsap_acik', z0=Z0 + 0.065)
dikdortgen_acik(y, cokgen((TCX, TCY), 0.0601, 8)[5], cokgen((TCX, TCY), 0.0601, 8)[6], Z0, 0.09, 0.2, 0.8, 0.0, 0.07,
                ('ahsap_dikey', 'ahsap_koyu', 'ahsap', 'koyu'), derin=0.006)

# ---------------------------------------------------------------- the clock-tower storehouse
y.bolum('Saat kuleli ambar')


def cephe(a, b, z0, katlar, n, plain=False):
    a, b, L, e, nc = eksen(a, b)
    z = z0
    for j, h in enumerate(katlar):
        if n:
            sabun_pencere(y, a, b, z, z + h, n, h * 0.24, h * 0.8, (TUG, 'tugla_koyu', TS, 'cam'), nu=2, nv=2)
        else:
            duz_duvar(y, a, b, z, z + h, TUG)
        z += h
        if j < len(katlar) - 1:
            silme(y, [a, b], z - 0.005, 0.008, 0.005, TS, 'duz', kapali=False)
    silme(y, [a, b], z0, 0.02, 0.008, 'tas', 'kaide', kapali=False)
    silme(y, [a, b], z - 0.012, 0.014, 0.012, TS, 'tac', kapali=False)
    return z


AX0, AX1, AY0, AY1 = 0.22, 1.0, -0.56, -0.28
KA = (0.13, 0.11)
ak = dikdortgen(AX0, AX1, AY0, AY1)
for i, n in enumerate((9, 3, 9, 3)):
    cephe(ak[i], ak[(i + 1) % 4], Z0, KA, n)
ZA = Z0 + sum(KA)
# the central pediment and the arched loading door
m0, m1 = 0.52, 0.7
y.kemerli(V(m0, AY0 - 0.003), V(m1, AY0 - 0.003), Z0, KA[0], (TUG, 'tugla_koyu', TS, 'ahsap'), v0=0.0, en=0.5, ust=0.02, derin=0.02, k_say=8, sivri=0,
          cerceve=(0.007, TS))
alinlik(y, V(m0 - 0.02, AY0 - 0.004), V(m1 + 0.02, AY0 - 0.004), ZA + 0.002, 0.06, derin=0.08, key=TS, ic_key=TUG, c=0.007, cati_key=CATI)
zr_a = cati_kirma(y, AX0, AX1, AY0, AY1, ZA, 0.13, 0.018, CATI, mahya='kursun', kalinlik=0.008, alt_key=TS, ns=4, nr=3, mahya_en=0.008)
# the clock cupola: a white timber stage with dials, an open bell stage, a lead dome, the vane
CCX, CCY = (AX0 + AX1) / 2, (AY0 + AY1) / 2
kutu_merkez(y, (CCX, CCY), 0.09, 0.09, zr_a - ZA + 0.06, 'beyaz', z0=ZA + 0.02)
zc = zr_a + 0.08
for a, b in [(dikdortgen(CCX - 0.045, CCX + 0.045, CCY - 0.045, CCY + 0.045)[i], dikdortgen(CCX - 0.045, CCX + 0.045, CCY - 0.045, CCY + 0.045)[(i + 1) % 4]) for i in range(4)]:
    a2, b2, L, e, nc = eksen(a, b)
    kadran(y, (a2 + b2) / 2 + Z * (zc - 0.035), e, nc, 0.024, kare=False)
silme(y, dikdortgen(CCX - 0.045, CCX + 0.045, CCY - 0.045, CCY + 0.045), zc, 0.008, 0.008, 'beyaz', 'tac')
ok = cokgen((CCX, CCY), 0.036, 8, math.pi / 8)
y.yuz_yon([V(p.x, p.y, zc + 0.008) for p in dikdortgen(CCX - 0.053, CCX + 0.053, CCY - 0.053, CCY + 0.053)], 'kursun', Z)
for i in range(8):
    y.kemerli(ok[i], ok[(i + 1) % 8], zc + 0.008, 0.065, ('beyaz', 'beyaz', 'beyaz', 'koyu'), v0=0.0, en=0.58, ust=0.01, derin=0.005, k_say=6, sivri=0)
silme(y, ok, zc + 0.073, 0.007, 0.006, 'beyaz', 'tac')
zd = zc + 0.08
donel(y, (CCX, CCY), [(0.04, zd), (0.036, zd + 0.015), (0.024, zd + 0.035), (0.008, zd + 0.05), (0.0, zd + 0.06)], 'kursun', n=8, kat=math.pi / 8)
y.prizma((CCX, CCY), 0.002, zd + 0.055, zd + 0.11, 'demir', n=4)
levha(y, [V(CCX, CCY, zd + 0.095), V(CCX + 0.035, CCY, zd + 0.095), V(CCX + 0.028, CCY, zd + 0.106), V(CCX, CCY, zd + 0.106)], 'altin', Y)
for bx in (AX0 + 0.1, AX1 - 0.1):
    kutu_merkez(y, (bx, CCY), 0.05, 0.03, 0.15, TUG, z0=ZA)
    kutu_merkez(y, (bx, CCY), 0.058, 0.038, 0.008, TS, z0=ZA + 0.15)

# ---------------------------------------------------------------- timber sheds and stacks
y.bolum('Kereste ambarları')


def sundurma(x0, x1, y0, y1, h, cati_h):
    """an open-sided timber seasoning shed: posts, a wall plate, a tiled gable roof; timber stacked inside"""
    nx = max(2, int((x1 - x0) / 0.12))
    for (yy) in (y0, y1):
        for k in range(nx + 1):
            x = x0 + (x1 - x0) * k / nx
            kutu_merkez(y, (x, yy), 0.012, 0.012, h, 'ahsap_koyu', z0=Z0, yuzler='onarkasagsol')
            if 0 < k < nx:
                cubuk(y, V(x, yy, Z0 + h * 0.6), V(x + 0.04, yy, Z0 + h - 0.004), 0.006, 'ahsap_koyu')
        kutu3(y, V((x0 + x1) / 2, yy, Z0 + h + 0.006), X, Y, Z, x1 - x0 + 0.012, 0.014, 0.012, 'ahsap_koyu')
    for x in (x0, x1):
        kutu3(y, V(x, (y0 + y1) / 2, Z0 + h + 0.006), X, Y, Z, 0.014, y1 - y0, 0.012, 'ahsap_koyu', ('+x', '-x', '+z', '-z'))
    cati_besik(y, x0, x1, y0, y1, Z0 + h + 0.012, cati_h, 0.025, 'kiremit', mahya='kiremit2', kalinlik=0.008, alt_key='ahsap_koyu',
               ucluk_key='ahsap_dikey', nr=3, ns=4, mahya_en=0.008)
    for k in range(nx):
        kereste(y, x0 + (x1 - x0) * (k + 0.5) / nx, (y0 + y1) / 2, Z0, L=(y1 - y0) * 0.8, n=4, kat=3 if k % 2 else 4, en=0.016,
                aci=math.pi / 2, key='ahsap_acik')


yt(0.2, 1.15, -0.2, 0.62, 'toprak', 0.0012)
sundurma(0.25, 0.75, -0.12, 0.16, 0.13, 0.09)
sundurma(0.25, 0.75, 0.26, 0.54, 0.13, 0.09)
sundurma(0.85, 1.12, -0.12, 0.54, 0.12, 0.09)
for (x, yy) in ((0.8, 0.2), (0.12, 0.05), (0.12, 0.42)):
    kereste(y, x, yy, Z0, L=0.16, n=3, kat=2, en=0.018, aci=0.0 if x > 0.5 else math.pi / 2, key='kutuk')

# ---------------------------------------------------------------- the mould loft, the yard
y.bolum('Kalıp çatısı ve tersane avlusu')
yt(-0.62, 0.2, 0.3, 0.66, 'zemin', 0.0012)
yt(DX1, 0.2, -0.6, 0.3, 'zemin', 0.0012)
MX0, MX1, MY0, MY1 = -0.6, 0.12, 0.36, 0.56
mk = dikdortgen(MX0, MX1, MY0, MY1)
for i, n in enumerate((7, 2, 7, 2)):
    a, b, L, e, nc = eksen(mk[i], mk[(i + 1) % 4])
    acikli_duvar(y, a, b, Z0, Z0 + 0.11, [((k + 0.5) / n, 0.05 if (i == 0 and k == 3) else 0.03, 0.0 if (i == 0 and k == 3) else 0.04, 0.09) for k in range(n)],
                 ('ahsap', 'ahsap_koyu', 'ahsap_acik', 'koyu' if (i == 0) else 'cam'), derin=0.008, pay=0.0)
    acikli_duvar(y, a, b, Z0 + 0.11, Z0 + 0.2, [((k + 0.5) / n, 0.026, 0.03, 0.07) for k in range(n)], ('ahsap', 'ahsap_koyu', 'ahsap_acik', 'cam'),
                 derin=0.008, pay=0.0)
    silme(y, [a, b], Z0 + 0.108, 0.006, 0.005, 'ahsap_koyu', 'duz', kapali=False)
    silme(y, [a, b], Z0, 0.016, 0.006, 'tugla', 'kaide', kapali=False)
cati_besik(y, MX0, MX1, MY0, MY1, Z0 + 0.2, 0.11, 0.02, 'kiremit', mahya='kiremit2', kalinlik=0.008, alt_key='ahsap_koyu', ucluk_key='ahsap',
           nr=3, ns=6, mahya_en=0.008)
# louvred ventilators on the mould loft's ridge, a hoist loft (lucam) with its beam over the front
for x in (-0.44, -0.04):
    kutu_merkez(y, (x, (MY0 + MY1) / 2), 0.05, 0.04, 0.03, 'ahsap_dikey', z0=Z0 + 0.2 + 0.09)
    cati_besik(y, x - 0.03, x + 0.03, (MY0 + MY1) / 2 - 0.025, (MY0 + MY1) / 2 + 0.025, Z0 + 0.2 + 0.12, 0.025, 0.006, 'kiremit', kalinlik=0.004,
               alt_key='ahsap_koyu', ucluk_key='ahsap_dikey', nr=1, ns=1, mahya_en=0.004)
_zc = Z0 + 0.2 + 0.11 * (0.05 / 0.12)
dormer(y, (-0.24, MY0 + 0.03), (0, -1), _zc, 0.05, 0.045, 0.07, 'ahsap', 'kiremit', 'koyu', 'ahsap_koyu')
cubuk(y, V(-0.24, MY0 + 0.03, _zc + 0.06), V(-0.24, MY0 - 0.04, _zc + 0.06), 0.006, 'ahsap_koyu')
boru(y, [V(-0.24, MY0 - 0.035, _zc + 0.057), V(-0.24, MY0 - 0.035, Z0 + 0.06)], 0.001, 'koyu', n=3)
kutu_merkez(y, (-0.24, MY0 - 0.035), 0.03, 0.03, 0.02, 'ahsap_acik', z0=Z0 + 0.04)


def capa(x, yy, aci, s=1.0):
    '''a great anchor lying on the quay: shank, curved arms with flukes, the wooden stock'''
    with parca(y, (x, yy, Z0 + 0.006), aci, s):
        cubuk(y, V(-0.07, 0, 0), V(0.07, 0, 0), 0.01, 'demir', 0.008)
        arc = [V(0.07 - 0.03 * (1 - math.cos(t)), 0.045 * math.sin(t), 0.0) for t in [k * math.pi / 8 for k in range(-4, 5)]]
        boru(y, arc, 0.005, 'demir', n=5)
        for p in (arc[0], arc[-1]):
            kutu3(y, p + V(0.006, 0, 0), X, Y, Z, 0.022, 0.018, 0.004, 'demir')
        kutu3(y, V(-0.06, 0, 0.004), X, Y, Z, 0.014, 0.12, 0.012, 'ahsap')
        boru(y, [V(-0.075, 0, 0), V(-0.08, 0, 0.0)], 0.009, 'demir', n=6)


for k, (x, yy, a) in enumerate(((0.3, -0.66, 0.2), (0.48, -0.68, -0.1), (0.66, -0.66, 0.3))):
    capa(x, yy, a)
for k in range(4):
    top_kizak(y, 0.82 + k * 0.08, -0.66, Z0 + 0.0012, -math.pi / 2, L=0.1, r=0.011, key='demir')
gulle_yigini(y, 0.12, -0.66, Z0 + 0.0012, n=4, r=0.008)
for (x, yy, kk) in ((0.0, -0.4, 'kece'), (0.05, -0.1, 'ahsap'), (-0.2, 0.62, 'kece'), (0.35, -0.62, 'lacivert'), (0.95, -0.62, 'boya_kirmizi')):
    insan(y, x, yy, Z0 + 0.0012, kk, 1.05, aci=rs.uniform(0, 6), sapka='koyu')
kereste(y, 0.0, 0.1, Z0, L=0.22, n=3, kat=3, en=0.016, aci=0.3, key='kutuk')

# ---------------------------------------------------------------- the ropery
y.bolum('Halat evi')
RX0, RX1, RY0, RY1 = -1.17, 1.17, 0.7, 0.94
KR = (0.12, 0.1, 0.09)
rk = dikdortgen(RX0, RX1, RY0, RY1)
for i, n in enumerate((26, 2, 26, 2)):
    a, b, L, e, nc = eksen(rk[i], rk[(i + 1) % 4])
    z = Z0
    for j, h in enumerate(KR):
        if j == 0 and i == 0:   # doors on the long side, small windows between
            acikli_duvar(y, a, b, z, z + h, [((k + 0.5) / n, 0.026 if k % 6 else 0.04, 0.0 if k % 6 == 0 else h * 0.35, h * 0.78) for k in range(n)],
                         (TUG, 'tugla_koyu', TS, 'cam'), derin=0.008, pay=0.0)
        else:
            acs = acikli_duvar(y, a, b, z, z + h, [((k + 0.5) / n, 0.024, h * 0.3, h * 0.78) for k in range(n)], (TUG, 'tugla_koyu', TS, 'cam'),
                               derin=0.008, pay=0.0)
        z += h
        if j < len(KR) - 1:
            silme(y, [a, b], z - 0.004, 0.006, 0.004, TS, 'duz', kapali=False)
    silme(y, [a, b], Z0, 0.018, 0.007, 'tas', 'kaide', kapali=False)
ZRP = Z0 + sum(KR)
cati_besik(y, RX0, RX1, RY0, RY1, ZRP, 0.1, 0.018, CATI, mahya='kursun', kalinlik=0.008, alt_key=TS, ucluk_key=TUG, alinlik_key=TS, nr=3, ns=16,
           mahya_en=0.008)
for k in range(6):   # ventilators along the ridge
    x = RX0 + 0.2 + k * (RX1 - RX0 - 0.4) / 5
    kutu_merkez(y, (x, (RY0 + RY1) / 2), 0.05, 0.04, 0.03, 'ahsap_dikey', z0=ZRP + 0.08)
    cati_besik(y, x - 0.03, x + 0.03, (RY0 + RY1) / 2 - 0.025, (RY0 + RY1) / 2 + 0.025, ZRP + 0.11, 0.025, 0.006, CATI, kalinlik=0.004, alt_key='ahsap_koyu',
               ucluk_key='ahsap_dikey', nr=1, ns=1, mahya_en=0.004)
# rope coils and a rope being walked out in front of the ropery
for k in range(5):
    x = -0.9 + k * 0.08
    donel(y, (x, 0.62), [(0.014, Z0), (0.02, Z0 + 0.004), (0.02, Z0 + 0.012), (0.008, Z0 + 0.016), (0.0, Z0 + 0.016)], 'saz_koyu', n=10)
boru(y, [V(-1.1, 0.56, Z0 + 0.03), V(-0.1, 0.56, Z0 + 0.028), V(0.1, 0.56, Z0 + 0.03)], 0.004, 'saz', n=5)
for x in (-1.1, 0.1):
    kutu_merkez(y, (x, 0.56), 0.03, 0.04, 0.045, 'ahsap', z0=Z0)
for k in range(4):
    kutu_merkez(y, (-0.9 + k * 0.25, 0.56), 0.008, 0.03, 0.03, 'ahsap_koyu', z0=Z0)
for k in range(3):
    insan(y, -0.85 + k * 0.3, 0.6, Z0, 'kece', 1.05, aci=0.0, sapka='koyu')
for (x, yy) in ((-1.12, -0.6), (-1.12, -0.3), (-1.14, 0.1), (-1.12, 0.45)):
    agac(y, x, yy, Z0, boy=0.12)

calistir(y, 'lm_kraliyettersane')
