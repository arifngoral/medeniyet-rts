# Uzun Gemi Tersanesi (lm_naust): a Viking shipyard on the shore: two naust boat-houses (dry-stone side walls, turf
# roof, timber gable open to the water, a boat inside on rollers), a longship being built on the stocks (keel, curving
# stems, ribs and the first clinker strakes, trestles and staging), a finished drakkar moored at a timber jetty with a
# dragon prow, a curling stern, a row of painted shields, a mast with a red-and-white striped square sail and its
# rigging; timber stacks, a sawing trestle, a tar kettle on a fire, rollers down the beach, the banner.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from viking_parca import *
from bina_ortak import calistir

y = Yapi()
XS, YF, YB = 1.05, -0.92, 0.95     # ground extents
ZW = 0.025                        # water level
Z0 = 0.075                        # land level
YK = -0.1                         # the edge of the land (top of the beach)
YS = -0.34                        # the water's edge (foot of the beach)

# ---------------------------------------------------------------- ground: land, beach, water
y.bolum('Kıyı, kumsal ve su')
kutu(y, V(-XS, YK, 0), X, 2 * XS, YB - YK, Z0, 'kaya_koyu', 'onarkasagsol')
y.yuz_yon([V(-XS, YK, Z0), V(XS, YK, Z0), V(XS, YB, Z0), V(-XS, YB, Z0)], 'cimen', Z)
kutu(y, V(-XS, YF, 0), X, 2 * XS, YS - YF, ZW - 0.004, 'kaya_koyu', 'onsagsol')
y.yuz_yon([V(-XS, YF, ZW), V(XS, YF, ZW), V(XS, YS, ZW), V(-XS, YS, ZW)], 'su', Z)
# the beach slope (sand), its side ends
y.yuz_yon([V(-XS, YS, ZW - 0.004), V(XS, YS, ZW - 0.004), V(XS, YK, Z0), V(-XS, YK, Z0)], 'kum', V(0, -0.4, 1))
for sx in (-1, 1):
    y.yuz_yon([V(sx * XS, YS, 0), V(sx * XS, YK, 0), V(sx * XS, YK, Z0), V(sx * XS, YS, ZW - 0.004)], 'kaya_koyu', V(sx, 0))
# a strip of shingle at the water line and a trodden yard
y.yuz_yon([V(-XS, YS - 0.002, ZW + 0.0008), V(XS, YS - 0.002, ZW + 0.0008), V(XS, YS + 0.05, ZW + 0.0008 + 0.05 * (Z0 - ZW) / (YK - YS)),
           V(-XS, YS + 0.05, ZW + 0.0008 + 0.05 * (Z0 - ZW) / (YK - YS))], 'kaya', V(0, -0.4, 1))
yer = lambda pts, k='toprak': y.yuz_yon([V(p[0], p[1], Z0 + 0.0015) for p in pts], k, Z)
yer([(-0.95, YK), (0.95, YK), (0.95, 0.0), (-0.95, 0.0)])
yer([(0.2, 0.0), (0.95, 0.0), (0.95, 0.88), (0.2, 0.88)], 'toprak')
# reeds and stones along the shore
for k in range(13):
    x = -0.98 + k * 0.163
    kure(y, (x + 0.03 * math.sin(k * 3.1), YS + 0.015, ZW + 0.004), 0.012 + 0.004 * (k % 3), 'kaya', n=6, kat=3)


# ---------------------------------------------------------------- the hull
def gemi(c, aci, L, B, zk, zg, uc, n=22, nv=6, vmax=1.0, ic=True, kalkanlar=True, renk=None, bas='ejder', kic='kivrim',
         guverte=True, lip=0.0028, kaburga=0, ejder_s=0.13):
    """a clinker-built Norse hull along local x round c (prow at -x): stations u -1..1, strakes v 0..1 keel to
    gunwale; B the half beam, zk the keel, zg the gunwale amidships, uc the sheer's rise at the ends. vmax < 1: only
    the lower strakes are planked (a hull being built); kaburga: that many ribs. Returns the points function"""
    renk = renk or ['ahsap_koyu', 'ahsap_koyu', 'ahsap', 'ahsap', 'ahsap_acik', 'boya_kirmizi']
    def g(u): return zg + uc * abs(u) ** 3.2
    def k(u): return zk + (g(u) - zk) * abs(u) ** 2.6
    def b(u): return B * max(0.0, 1 - u * u) ** 0.5
    def S(u, v, sy, ice=0.0):
        ph = v * math.pi / 2
        bb = b(u) * max(0.0, 1 - ice / B)
        return V(u * L / 2, sy * bb * math.sin(ph), k(u) + (g(u) - k(u)) * (1 - math.cos(ph)) + (ice * 0.6 if v < 0.02 else 0))
    def N(u, v, sy):
        ph = v * math.pi / 2
        return V(0, sy * (g(u) - k(u)) * math.sin(ph) + sy * 1e-4, -b(u) * math.cos(ph)).normalized()
    us = [-1 + 2 * i / n for i in range(n + 1)]
    def merkez(u):   # a point on a line inside the hull: outward is away from it
        return V(u * L / 2 * 0.75, 0, zk + (zg - zk) * 0.75)
    def T(u, v, sy):  # the surface's direction towards the gunwale
        return (S(u, min(1, v + 0.02), sy) - S(u, max(0, v - 0.02), sy))
    vs = [vmax * j / nv for j in range(nv + 1)]
    with parca(y, c, aci):
        for sy in (-1, 1):
            for j in range(nv):
                for i in range(n):
                    ua, ub = us[i], us[i + 1]
                    lp = lambda u: N(u, vs[j], sy) * (lip if j else 0)
                    q = [S(ua, vs[j], sy) + lp(ua), S(ub, vs[j], sy) + lp(ub), S(ub, vs[j + 1], sy), S(ua, vs[j + 1], sy)]
                    um = (ua + ub) / 2
                    dn = (q[0] + q[1] + q[2] + q[3]) / 4 - merkez(um)
                    if (q[0] - q[3]).length < 1e-6 and (q[1] - q[2]).length < 1e-6: continue
                    y.yuz_yon(q, renk[min(j * len(renk) // nv, len(renk) - 1)] if vmax >= 0.99 else 'ahsap_acik', dn)
                    if j and lip:
                        y.yuz_yon([S(ua, vs[j], sy), S(ub, vs[j], sy), S(ub, vs[j], sy) + lp(ub), S(ua, vs[j], sy) + lp(ua)],
                                  'ahsap_koyu', -T(um, vs[j], sy))
            if ic:   # the inside of the planking, and its top edge
                t_ = 0.006
                for j in range(nv):
                    for i in range(n):
                        ua, ub = us[i], us[i + 1]
                        q = [S(ua, vs[j], sy, t_), S(ub, vs[j], sy, t_), S(ub, vs[j + 1], sy, t_), S(ua, vs[j + 1], sy, t_)]
                        if (q[0] - q[3]).length < 1e-6 and (q[1] - q[2]).length < 1e-6: continue
                        um = (ua + ub) / 2
                        y.yuz_yon(q, 'ahsap' if vmax >= 0.99 else 'ahsap_acik', merkez(um) - (q[0] + q[1] + q[2] + q[3]) / 4)
                for i in range(n):
                    ua, ub = us[i], us[i + 1]
                    q = [S(ua, vmax, sy), S(ub, vmax, sy), S(ub, vmax, sy, t_), S(ua, vmax, sy, t_)]
                    if (q[0] - q[3]).length + (q[1] - q[2]).length < 1e-6: continue
                    y.yuz_yon(q, 'ahsap_koyu', V(0, 0, 1))
        if guverte and vmax >= 0.99:   # deck boards a little below the gunwale
            for i in range(1, n - 1):
                ua, ub = us[i], us[i + 1]
                def hw(u):
                    zd = g(0) - 0.03
                    cs = 1 - (zd - k(u)) / max(1e-4, g(u) - k(u))
                    cs = max(-1.0, min(1.0, cs))
                    return max(0.0, b(u) - 0.007) * math.sqrt(max(0.0, 1 - cs * cs)), zd
                (wa, zd), (wb, _) = hw(ua), hw(ub)
                if wa < 0.005 or wb < 0.005: continue
                y.yuz_yon([V(ua * L / 2, -wa, zd), V(ub * L / 2, -wb, zd), V(ub * L / 2, wb, zd), V(ua * L / 2, wa, zd)], 'ahsap_acik', Z)
            # thwarts / rowing benches
            for i in range(-5, 6):
                u = i / 7
                cubuk(y, V(u * L / 2, -b(u) * 0.92, g(0) - 0.022), V(u * L / 2, b(u) * 0.92, g(0) - 0.022), 0.012, 'ahsap', 0.005)
        # keel, stem and stern posts
        boru(y, [S(u, 0, 1) - Z * 0.004 for u in us[1:-1]], 0.006, 'ahsap_koyu', n=5)
        E0, E1 = S(-1, 1, 1), S(1, 1, 1)
        for E, sx, kind in ((E0, -1, bas), (E1, 1, kic)):
            pts = [S(sx * u, 0.5, 1) * 0 + V(sx * L / 2 * u, 0, k(sx * u) + (g(sx * u) - k(sx * u)) * 0.5) for u in (0.9, 0.97)]
            stem = [E - V(sx * 0.01, 0, 0.05), E, E + V(sx * 0.035, 0, 0.05), E + V(sx * 0.05, 0, 0.11)]
            boru(y, stem, 0.011, 'ahsap_koyu', n=6, r_son=0.009)
            top = stem[-1]
            if kind == 'ejder':
                ejder(y, top - V(0, 0, 0.01), V(sx, 0), ejder_s, 'ahsap_koyu', egim=0.3)
            elif kind == 'kivrim':
                curl = [top]
                for t in range(1, 9):
                    a = math.pi * 0.5 - t * 0.55
                    r = 0.045 * (1 - t / 11)
                    curl.append(top + V(sx * (0.0 + r * math.cos(a) - 0.0 * r), 0, r * math.sin(a) + 0.04 - 0.04 * (t / 8) * 0))
                boru(y, curl, 0.009, 'ahsap_koyu', n=5, r_son=0.004)
            elif kind == 'duz':
                pass
        if kalkanlar and vmax >= 0.99:
            renkler = (('boya_sari', 'koyu'), ('boya_kirmizi', 'beyaz'), ('beyaz', 'boya_yesil'), ('koyu', 'boya_sari'), ('boya_kirmizi', 'boya_sari'))
            for sy in (-1, 1):
                m = 15
                for i in range(m):
                    u = -0.66 + 1.32 * i / (m - 1)
                    p = S(u, 0.93, sy) + N(u, 0.93, sy) * 0.006
                    kalkan(y, p, N(u, 0.93, sy) + V(0, 0, 0.1), 0.021, renkler[i % 5], kalin=0.003)
        if kaburga:
            for i in range(kaburga):
                u = -0.8 + 1.6 * i / (kaburga - 1)
                pts = [S(u, 1 - t / 6, -1, 0.004) for t in range(7)] + [S(u, t / 6, 1, 0.004) for t in range(1, 7)]
                boru(y, pts, 0.0055, 'ahsap', n=5)
    return S


# ---------------------------------------------------------------- the moored drakkar
y.bolum('Suda uzun gemi (drakkar)')
SC = (-0.12, -0.6, 0)
SL, SB = 1.22, 0.125
gemi(SC, 0.0, SL, SB, ZW - 0.035, ZW + 0.065, 0.17, n=26, nv=6, ejder_s=0.17)
with parca(y, SC, 0.0):
    MX = 0.02
    zd = ZW + 0.03
    y.prizma((MX, 0), 0.01, zd, zd + 0.8, 'ahsap', n=8)
    kure(y, (MX, 0, zd + 0.805), 0.013, 'altin', n=8, kat=4)
    # the mast partner (kerling) and a vane at the top
    kutu_merkez(y, (MX, 0), 0.08, 0.03, 0.02, 'ahsap_koyu', z0=zd)
    iki_yuzlu(y, [V(MX + 0.01, 0, zd + 0.77), V(MX + 0.055, 0, zd + 0.78), V(MX + 0.05, 0, zd + 0.795), V(MX + 0.01, 0, zd + 0.8)], 'altin', -Y, kil=0.0015)
    # yard and the striped square sail, bellying towards the prow
    ZY = zd + 0.7
    SW, SHt = 0.28, 0.46
    BR = 0.72                     # the yard braced round (a reach)
    cb, sb = math.cos(BR), math.sin(BR)
    rot = lambda p: V(MX + (p.x - MX) * cb - p.y * sb, (p.x - MX) * sb + p.y * cb, p.z)
    cubuk(y, rot(V(MX - 0.012, -SW - 0.03, ZY)), rot(V(MX - 0.012, SW + 0.03, ZY)), 0.013, 'ahsap_koyu')
    ns, nh = 10, 6
    def sail(s, t):     # s 0..1 across (y), t 0..1 down
        yy = -SW + 2 * SW * s
        zz = ZY - 0.01 - SHt * t
        bel = 0.075 * math.sin(math.pi * s) * math.sin(math.pi * (0.15 + 0.85 * t)) + 0.02 * t
        return rot(V(MX - 0.022 - bel, yy * (1 - 0.06 * t), zz))
    for i in range(ns):
        key = 'boya_kirmizi' if (i // 2) % 2 == 0 else 'beyaz'
        if i in (0, ns - 1): key = 'boya_kirmizi'
        for j in range(nh):
            q = [sail(i / ns, j / nh), sail((i + 1) / ns, j / nh), sail((i + 1) / ns, (j + 1) / nh), sail(i / ns, (j + 1) / nh)]
            iki_yuzlu(y, list(reversed(q)), key, V(-cb, -sb, 0), kil=0.003)
    # the cloth's rims (seen edge-on the two sheets showed each other's backs)
    yk = V(-cb, -sb, 0) * 0.003
    kenar = [sail(i / ns, 0) for i in range(ns + 1)] + [sail(1, j / nh) for j in range(1, nh + 1)] +             [sail(i / ns, 1) for i in range(ns - 1, -1, -1)] + [sail(0, j / nh) for j in range(nh - 1, 0, -1)]
    orta = sail(0.5, 0.5)
    for i in range(len(kenar)):
        a, b = kenar[i], kenar[(i + 1) % len(kenar)]
        y.yuz_yon([a, b, b - yk, a - yk], 'boya_kirmizi', (a + b) / 2 - orta)
    # a bolt rope round the sail's foot and its sheets to the gunwales
    boru(y, [sail(s / ns, 1) for s in range(ns + 1)], 0.003, 'ahsap_koyu', n=4)
    for sy in (-1, 1):
        cubuk(y, sail(0 if sy < 0 else 1, 1), V(MX + 0.25, sy * SB * 0.8, ZW + 0.06), 0.0025, 'ahsap_koyu')
    # stays fore and aft
    cubuk(y, V(MX, 0, zd + 0.78), V(-SL / 2 + 0.03, 0, ZW + 0.2), 0.003, 'ahsap_koyu')
    cubuk(y, V(MX, 0, zd + 0.78), V(SL / 2 - 0.03, 0, ZW + 0.2), 0.003, 'ahsap_koyu')
    for sy in (-1, 1):
        for xo in (-0.04, 0.06):
            cubuk(y, V(MX, 0, zd + 0.74), V(MX + xo, sy * SB * 0.95, ZW + 0.07), 0.0022, 'ahsap_koyu')
    # oars run out on the far side, a steering oar at the stern quarter (starboard, +y)
    for i in range(7):
        x = -0.42 + i * 0.12
        cubuk(y, V(x, SB * 0.9, ZW + 0.06), V(x - 0.05, SB + 0.2, ZW + 0.004), 0.0045, 'ahsap_acik')
    boru(y, [V(SL / 2 - 0.14, SB + 0.005, ZW + 0.1), V(SL / 2 - 0.12, SB + 0.03, ZW - 0.01)], 0.006, 'ahsap', n=5)
    kutu_merkez(y, (SL / 2 - 0.115, SB + 0.032), 0.05, 0.008, 0.06, 'ahsap', z0=ZW - 0.03, aci=0.0)

# ---------------------------------------------------------------- jetty
y.bolum('İskele')
JX0, JX1 = 0.56, 0.72
JY0, JY1 = -0.9, YK + 0.02
JZ = ZW + 0.05
for x in (JX0 + 0.012, JX1 - 0.012):
    for k in range(6):
        yy = JY0 + 0.01 + (JY1 - JY0 - 0.02) * k / 5
        y.prizma((x, yy), 0.011, 0.0, JZ + 0.03 if k % 2 == 0 else JZ, 'kutuk', n=6)
m = 22
for k in range(m):
    ya, yb = JY0 + (JY1 - JY0) * k / m, JY0 + (JY1 - JY0) * (k + 1) / m - 0.002
    kutu(y, V(JX0, ya, JZ - 0.01), X, JX1 - JX0, yb - ya, 0.01, 'ahsap_acik' if k % 3 else 'ahsap', 'onarkasagsolust')
for x in (JX0 + 0.006, JX1 - 0.006):
    cubuk(y, V(x, JY0, JZ - 0.016), V(x, JY1, JZ - 0.016), 0.012, 'ahsap_koyu')
# a gangplank to the ship, mooring lines, coiled rope, crates
cubuk(y, V(JX0 + 0.01, -0.64, JZ), V(SC[0] + SL / 2 - 0.12, -0.66 + SB * 0.6, ZW + 0.065), 0.04, 'ahsap', 0.006)
for yy in (-0.82, -0.5):
    cubuk(y, V(JX0 + 0.012, yy, JZ + 0.03), V(SC[0] + SL / 2 - 0.08, -0.66 + SB * 0.5 * (1 if yy > -0.66 else -1), ZW + 0.07), 0.003, 'ahsap_koyu')
donel(y, (0.68, -0.3), [(0.0, JZ), (0.022, JZ), (0.022, JZ + 0.01), (0.01, JZ + 0.01), (0.01, JZ + 0.004), (0.0, JZ + 0.004)], 'saz_koyu', n=10)
kutu_merkez(y, (0.66, -0.2), 0.05, 0.05, 0.04, 'ahsap', z0=JZ)
kutu_merkez(y, (0.665, -0.2), 0.03, 0.052, 0.006, 'ahsap_koyu', z0=JZ + 0.02)


# ---------------------------------------------------------------- boat-houses
def naust(cx, y0, y1, w=0.34, h=0.11, cati='cimen', tekne=True, ch=0.25):
    """a boat-house along y: thick dry-stone side and back walls, open to the water at y0 under a timber gable, a turf
    roof; inside, a boat on rollers"""
    t = 0.045
    x0, x1 = cx - w / 2, cx + w / 2
    for (a0, a1) in ((x0 - t, x0), (x1, x1 + t)):
        kutu(y, V(a0, y0, Z0), X, a1 - a0, y1 - y0, h, 'granit', 'onarkasagsolust')
    kutu(y, V(x0, y1 - t, Z0), X, w, t, h, 'granit', 'onarkaust')
    # inside: earth floor, rollers, dark back
    y.yuz_yon([V(x0, y0, Z0 + 0.001), V(x1, y0, Z0 + 0.001), V(x1, y1 - t, Z0 + 0.001), V(x0, y1 - t, Z0 + 0.001)], 'toprak', Z)
    for k in range(5):
        yy = y0 + 0.05 + k * (y1 - y0 - 0.12) / 4
        boru(y, [V(x0 + 0.03, yy, Z0 + 0.008), V(x1 - 0.03, yy, Z0 + 0.008)], 0.007, 'kutuk', n=6)
    # roof: timber gable at the front, turf slopes, its underside
    dl = ['saz', 'saz', 'saz_koyu'] if cati == 'saz' else None
    zr = cati_besik(y, x0 - t, x1 + t, y0, y1, Z0 + h, ch, 0.03, cati, cati, kalinlik=0.02, ucluk_key='ahsap_dikey',
                    alt_key='ahsap_koyu', uc_sacak=0.03, nr=9 if dl else 5, ns=8, dilim=dl)
    bb = w / 2 + t + 0.03
    for sx in (-1, 1):
        q = [V(cx + sx * (w / 2 + t), y0, Z0 + h - 0.0), V(cx + sx * (w / 2 + t), y1, Z0 + h), V(cx, y1, zr - 0.03), V(cx, y0, zr - 0.03)]
        y.yuz_yon(q, 'ahsap_koyu', V(-sx, 0, -1))
    # rafters showing under the eaves and a carved crossed board on the gable
    top = V(cx, y0 - 0.034, zr - 0.006)
    for sx in (-1, 1):
        p0 = V(cx + sx * bb * 0.75, y0 - 0.034, Z0 + h + ch * 0.25)
        d = (top - p0).normalized()
        cubuk(y, p0, top + d * 0.05, 0.014, 'ahsap_koyu', 0.008)
        ejder(y, top + d * 0.048, V(-sx, -0.2), 0.07, 'ahsap_koyu')
    sl = lambda sx, t, yy: V(cx + sx * bb * (1 - t), yy, Z0 + h + ch * t)
    # straw / grass strokes down the slopes (the other tone, a hair above the roof)
    import random
    rg = random.Random(int(cx * 100))
    for sx in (-1, 1):
        nn = V(sx * ch, 0, bb).normalized() * 0.0025
        for k in range(70):
            yy = rg.uniform(y0 - 0.02, y1 + 0.02)
            ta = rg.uniform(0.04, 0.85); tb = min(0.97, ta + rg.uniform(0.06, 0.14))
            q = [sl(sx, ta, yy - 0.0035) + nn, sl(sx, ta, yy + 0.0035) + nn, sl(sx, tb, yy + 0.0035) + nn, sl(sx, tb, yy - 0.0035) + nn]
            y.yuz_yon(q, 'saz_koyu' if cati == 'saz' else 'cimen_kuru', V(sx * ch, 0, bb))
    # crossed rider sticks over the thatch ridge, a dark trimmed edge along the eaves
    if cati == 'saz':
        m = int((y1 - y0) / 0.12)
        for k in range(m + 1):
            yy = y0 + 0.03 + (y1 - y0 - 0.06) * k / m
            for sx in (-1, 1):
                cubuk(y, sl(sx, 0.82, yy) + Z * 0.007, sl(-sx, 1.0, yy) + V(-sx * 0.014, 0, 0.016), 0.008, 'ahsap_koyu', 0.007)
    else:   # a turf roll along the ridge
        boru(y, [V(cx, y0 - 0.03, zr - 0.004), V(cx, y1 + 0.03, zr - 0.004)], 0.016, 'cimen_kuru', n=8)
    for sx in (-1, 1):
        cubuk(y, sl(sx, 0.03, y0 - 0.03) + Z * 0.007, sl(sx, 0.03, y1 + 0.03) + Z * 0.007, 0.03, 'saz_koyu' if cati == 'saz' else 'toprak_ot', 0.01)
    # the gable's tie beam over the opening
    cubuk(y, V(x0 - t, y0 - 0.005, Z0 + h + 0.008), V(x1 + t, y0 - 0.005, Z0 + h + 0.008), 0.018, 'ahsap_koyu', 0.014)
    if tekne:
        gemi((cx, (y0 + y1) / 2 - 0.08, Z0 + 0.045), math.pi / 2, (y1 - y0) * 0.95, w * 0.3, -0.03, 0.04, 0.06, n=16, nv=5,
             kalkanlar=False, bas='kivrim', kic='kivrim', guverte=False, renk=['ahsap_koyu', 'ahsap', 'ahsap', 'ahsap_acik', 'boya_kirmizi'])
    return zr


y.bolum('Gemi barınakları (naust)')
naust(-0.62, -0.06, 0.8, w=0.32, h=0.13, ch=0.34)
naust(-0.14, -0.02, 0.84, w=0.3, h=0.12, cati='saz', tekne=True, ch=0.36)
# oars and a boat hook leaning on the first boat-house's outer wall, a net hung to dry beside them
XW = -0.62 - 0.16 - 0.045
for k in range(7):
    yy = 0.06 + k * 0.035
    a, b = V(XW - 0.07, yy, Z0), V(XW - 0.004, yy + 0.015, Z0 + 0.125)
    cubuk(y, a, b, 0.006, 'ahsap_acik', 0.006)
    e = (b - a).normalized()
    kutu_merkez(y, (a.x + e.x * 0.02, a.y), 0.012, 0.022, 0.035, 'ahsap_acik', z0=Z0 + 0.004, aci=math.atan2(e.y, e.x))
for k in range(9):
    yy = 0.38 + k * 0.03
    cubuk(y, V(XW - 0.003, yy, Z0 + 0.02), V(XW - 0.003, yy, Z0 + 0.115), 0.002, 'saz_koyu', 0.002)
for zz in (0.03, 0.055, 0.08, 0.105):
    cubuk(y, V(XW - 0.003, 0.37, Z0 + zz), V(XW - 0.003, 0.63, Z0 + zz), 0.002, 'saz_koyu', 0.002)
cubuk(y, V(XW - 0.004, 0.36, Z0 + 0.118), V(XW - 0.004, 0.64, Z0 + 0.118), 0.008, 'ahsap_koyu', 0.006)

# ---------------------------------------------------------------- beacon tower
y.bolum('Gözcü kulesi ve işaret ateşi')
TB = V(-0.95, 0.08)
HT = 0.5
for sx in (-1, 1):
    for sy in (-1, 1):
        kutu_merkez(y, (TB.x + sx * 0.06, TB.y + sy * 0.06), 0.026, 0.026, 0.016, 'granit', z0=Z0)
        cubuk(y, V(TB.x + sx * 0.06, TB.y + sy * 0.06, Z0 + 0.012), V(TB.x + sx * 0.036, TB.y + sy * 0.036, Z0 + HT), 0.014, 'kutuk', 0.014)
# cross braces on the four sides, two storeys
for i in range(4):
    c0 = [V(-1, -1), V(1, -1), V(1, 1), V(-1, 1)]
    a, b = c0[i], c0[(i + 1) % 4]
    lg = lambda c, t: V(TB.x + c.x * (0.06 - 0.024 * t), TB.y + c.y * (0.06 - 0.024 * t), Z0 + 0.012 + (HT - 0.012) * t)
    nn = V(a.x + b.x, a.y + b.y).normalized() * 0.006
    for t0, t1 in ((0.05, 0.5), (0.5, 0.95)):
        cubuk(y, lg(a, t0) + nn, lg(b, t1) + nn, 0.007, 'ahsap', 0.006)
        cubuk(y, lg(b, t0) + nn, lg(a, t1) + nn, 0.007, 'ahsap', 0.006)
    cubuk(y, lg(a, 0.5) + nn, lg(b, 0.5) + nn, 0.008, 'ahsap_koyu', 0.007)
# the platform with a railing, a fire basket and a horn on its post
kutu_merkez(y, (TB.x, TB.y), 0.12, 0.12, 0.014, 'ahsap_acik', z0=Z0 + HT)
kutu_merkez(y, (TB.x, TB.y), 0.126, 0.126, 0.006, 'ahsap_koyu', z0=Z0 + HT - 0.006)
zp = Z0 + HT + 0.014
for sx in (-1, 1):
    for sy in (-1, 1):
        y.prizma((TB.x + sx * 0.055, TB.y + sy * 0.055), 0.005, zp, zp + 0.06, 'ahsap_koyu', n=5)
for i in range(4):
    c0 = [V(-1, -1), V(1, -1), V(1, 1), V(-1, 1)]
    a, b = c0[i], c0[(i + 1) % 4]
    for zz in (0.03, 0.058):
        cubuk(y, V(TB.x + a.x * 0.055, TB.y + a.y * 0.055, zp + zz), V(TB.x + b.x * 0.055, TB.y + b.y * 0.055, zp + zz), 0.006, 'ahsap', 0.005)
y.prizma((TB.x, TB.y), 0.006, zp, zp + 0.05, 'demir', n=6)
donel(y, (TB.x, TB.y), [(0.008, zp + 0.05), (0.04, zp + 0.075), (0.042, zp + 0.1), (0.036, zp + 0.1), (0.0, zp + 0.06)], 'demir', n=12)
for k in range(5):
    t = TAU * k / 5 + 0.3
    cubuk(y, V(TB.x + 0.03 * math.cos(t), TB.y + 0.03 * math.sin(t), zp + 0.075), V(TB.x - 0.006 * math.cos(t), TB.y - 0.006 * math.sin(t), zp + 0.11), 0.007, 'kutuk', 0.007)
for r, hh, key in ((0.034, 0.11, 'boya_kirmizi'), (0.022, 0.15, 'boya_sari'), (0.01, 0.1, 'beyaz')):
    y.koni((TB.x, TB.y), r, zp + 0.08, hh, key, n=7)
boru(y, [V(TB.x + 0.055, TB.y - 0.055, zp + 0.05), V(TB.x + 0.07, TB.y - 0.06, zp + 0.06), V(TB.x + 0.085, TB.y - 0.055, zp + 0.08)], 0.008, 'beyaz', n=6, r_son=0.004)
# a ladder up the landward side
for dx in (-0.016, 0.016):
    cubuk(y, V(TB.x + dx, TB.y + 0.11, Z0), V(TB.x + dx, TB.y + 0.062, zp), 0.006, 'ahsap', 0.005)
for k in range(1, 12):
    t = k / 12
    p = V(TB.x, TB.y + 0.11 - 0.048 * t, Z0 + (zp - Z0) * t)
    cubuk(y, p - V(0.018, 0, 0), p + V(0.018, 0, 0), 0.004, 'ahsap_acik', 0.004)
# rollers down the beach from the boat-houses into the water
for cx in (-0.62, -0.14):
    for k in range(4):
        yy = -0.12 - k * 0.07
        zz = Z0 + (ZW - Z0) * (YK - yy) / (YK - YS)
        boru(y, [V(cx - 0.1, yy, max(zz, ZW) + 0.008), V(cx + 0.1, yy, max(zz, ZW) + 0.008)], 0.008, 'kutuk', n=6)

# ---------------------------------------------------------------- the ship on the stocks
y.bolum('Kızakta yapılan gemi')
BC = (0.46, 0.46, Z0 + 0.07)
BL, BB = 0.78, 0.1
# stocks under the keel and trestles with staging planks along both sides
for k in range(6):
    yy = BC[1] - BL / 2 * 0.8 + BL * 0.8 * k / 5
    kutu_merkez(y, (BC[0], yy), 0.07, 0.03, 0.05, 'kutuk', z0=Z0)
    kutu_merkez(y, (BC[0], yy), 0.045, 0.026, 0.018, 'ahsap', z0=Z0 + 0.05)
gemi(BC, math.pi / 2, BL, BB, 0.0, 0.07, 0.12, n=18, nv=5, vmax=0.42, kalkanlar=False, bas='duz', kic='duz', guverte=False, kaburga=9)
with parca(y, BC, math.pi / 2):
    # bare stem posts rising at both ends
    for sx in (-1, 1):
        E = V(sx * BL / 2, 0, 0.0)
        boru(y, [E + V(-sx * 0.06, 0, -0.02), E, E + V(sx * 0.02, 0, 0.1), E + V(sx * 0.05, 0, 0.17), E + V(sx * 0.07, 0, 0.2)], 0.009, 'ahsap', n=6)
for sx in (-1, 1):
    x = BC[0] + sx * (BB + 0.08)
    for k in range(4):
        yy = BC[1] - 0.3 + 0.2 * k
        cubuk(y, V(x - 0.02, yy, Z0), V(x, yy, Z0 + 0.11), 0.008, 'ahsap')
        cubuk(y, V(x + 0.02, yy, Z0), V(x, yy, Z0 + 0.11), 0.008, 'ahsap')
    kutu(y, V(x - 0.03, BC[1] - 0.34, Z0 + 0.11), X, 0.06, 0.68, 0.01, 'ahsap_acik')
# timber stacks, a sawing trestle with a log, a tar kettle
y.bolum('Kereste, katran kazanı')
for (cx, cy, ang, n_, kt) in ((0.86, 0.1, 0.0, 6, 3), (0.86, 0.64, 0.0, 5, 4)):
    with parca(y, (cx, cy, Z0), ang):
        for kk in range(kt):
            for i in range(n_ - kk):
                kutu_merkez(y, ((i - (n_ - kk - 1) / 2) * 0.028, 0), 0.024, 0.32, 0.012, 'ahsap_acik' if (i + kk) % 2 else 'kutuk', z0=0.012 * kk + 0.01)
        for sy in (-1, 1):
            kutu_merkez(y, (0, sy * 0.12), 0.2, 0.02, 0.01, 'ahsap_koyu', z0=0.0)
odun_yigini(y, (0.28, 0.85, Z0), 0.0, L=0.3, n=4, r=0.016, kat=3)
with parca(y, (0.24, 0.14, Z0), 0.3):
    for sx in (-1, 1):
        cubuk(y, V(sx * 0.06, -0.025, 0), V(sx * 0.06, 0.0, 0.07), 0.007, 'ahsap')
        cubuk(y, V(sx * 0.06, 0.025, 0), V(sx * 0.06, 0.0, 0.07), 0.007, 'ahsap')
    boru(y, [V(-0.12, 0, 0.08), V(0.12, 0, 0.08)], 0.014, 'kutuk', n=7)
TK = V(0.22, -0.04)
for k in range(3):
    t = TAU * k / 3
    cubuk(y, V(TK.x + 0.05 * math.cos(t), TK.y + 0.05 * math.sin(t), Z0), V(TK.x, TK.y, Z0 + 0.12), 0.005, 'ahsap_koyu')
donel(y, (TK.x, TK.y), [(0.0, Z0 + 0.03), (0.025, Z0 + 0.034), (0.03, Z0 + 0.055), (0.028, Z0 + 0.07), (0.0, Z0 + 0.07)], 'demir', n=12)
y.yuz_yon([V(TK.x + 0.024 * math.cos(TAU * i / 10), TK.y + 0.024 * math.sin(TAU * i / 10), Z0 + 0.0705) for i in range(10)], 'koyu', Z)
for r, h, key in ((0.022, 0.035, 'boya_kirmizi'), (0.012, 0.03, 'boya_sari')):
    y.koni((TK.x, TK.y), r, Z0, h, key, n=6)
for k in range(3):
    donel(y, (TK.x + 0.08 + k * 0.045, TK.y + 0.02), [(0.0, Z0), (0.016, Z0), (0.02, Z0 + 0.022), (0.016, Z0 + 0.044), (0.0, Z0 + 0.044)], 'ahsap_koyu', n=10)

y.bolum('Mancınık direkleri ve sandal')
# sheer legs over the stocks lifting a strake into place
SX_, SY_ = BC[0], BC[1] + 0.05
apex = V(SX_, SY_, Z0 + 0.6)
for sx in (-1, 1):
    boru(y, [V(SX_ + sx * 0.26, SY_ - 0.04, Z0), apex + V(sx * 0.01, 0, 0)], 0.009, 'kutuk', n=6)
boru(y, [V(SX_ + 0.02, SY_ + 0.42, Z0), apex], 0.007, 'kutuk', n=6)
cubuk(y, apex, V(SX_, SY_, Z0 + 0.3), 0.003, 'ahsap_koyu')
cubuk(y, V(SX_ - 0.16, SY_, Z0 + 0.3), V(SX_ + 0.16, SY_, Z0 + 0.29), 0.024, 'ahsap_acik', 0.006)
cubuk(y, apex, V(SX_ + 0.02, SY_ + 0.42, Z0 + 0.005), 0.0025, 'ahsap_koyu')
# a small boat (faering) at the jetty's end
gemi((0.88, -0.66, 0), math.pi / 2 + 0.2, 0.36, 0.055, ZW - 0.02, ZW + 0.035, 0.05, n=12, nv=4, kalkanlar=False, bas='kivrim', kic='kivrim',
     guverte=False, renk=['ahsap_koyu', 'ahsap', 'ahsap_acik', 'boya_kirmizi'])
for sy in (-1, 1):
    cubuk(y, V(0.88 + sy * 0.06, -0.62, ZW + 0.03), V(0.88 + sy * 0.15, -0.58, ZW + 0.002), 0.004, 'ahsap_acik')
cubuk(y, V(0.86, -0.5, ZW + 0.04), V(JX1 - 0.01, -0.46, JZ + 0.02), 0.0025, 'ahsap_koyu')

y.bolum('Kumsalda sandal, sepetler, kayalar')
# a second faering drawn up on the beach, its oars across the thwarts, fish baskets and a net float pile by it
zb_ = Z0 + (ZW - Z0) * (YK + 0.22) / (YK - YS)
gemi((0.3, -0.22, 0), 0.22, 0.34, 0.05, zb_ + 0.004, zb_ + 0.05, 0.045, n=12, nv=4, kalkanlar=False, bas='kivrim', kic='kivrim',
     guverte=False, renk=['ahsap_koyu', 'ahsap', 'boya_yesil', 'ahsap_acik'])
with parca(y, (0.3, -0.22, 0), 0.22):
    for dx in (-0.03, 0.03):
        cubuk(y, V(dx - 0.15, -0.012, zb_ + 0.045), V(dx + 0.13, 0.012, zb_ + 0.045), 0.004, 'ahsap_acik', 0.004)
for k, (bx, by) in enumerate(((0.12, -0.17), (0.155, -0.2), (0.1, -0.22))):
    zz = Z0 + (ZW - Z0) * (YK - by) / (YK - YS)
    donel(y, (bx, by), [(0.0, zz - 0.004), (0.016, zz - 0.004), (0.021, zz + 0.03), (0.017, zz + 0.03), (0.0, zz + 0.026)], 'saz' if k % 2 else 'saz_koyu', n=10)
# rocks in the shallows and two mooring posts
for (rx, ry, rr) in ((-0.86, -0.8, 0.045), (-0.8, -0.86, 0.03), (-0.5, -0.88, 0.035), (0.3, -0.87, 0.04), (0.38, -0.84, 0.025)):
    kure(y, (rx, ry, ZW - rr * 0.45), rr, 'kaya_koyu' if rr > 0.035 else 'kaya', n=8, kat=4)
for px in (-0.86, -0.4):
    y.prizma((px, -0.42), 0.011, 0.0, ZW + 0.09, 'kutuk', n=6)
    kure(y, (px, -0.42, ZW + 0.092), 0.012, 'ahsap_koyu', n=6, kat=3)

y.bolum('Ladinler ve sancak')
for (tx, ty, b) in ((-0.94, 0.86, 0.34), (-0.97, 0.36, 0.26), (0.92, 0.88, 0.3), (0.14, 0.9, 0.26), (0.96, 0.37, 0.26)):
    cam_agaci(y, tx, ty, Z0, b, 'boya_yesil')
sancak(y, 0.52, -0.06, Z0, boy=0.46, en=0.13, yuk=0.085, aci=math.pi - 0.4, direk_key='ahsap_koyu', kuyruk=True)

calistir(y, 'lm_naust')
