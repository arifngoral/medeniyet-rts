# İskenderiye Feneri (lm_feneri): the Pharos of Alexandria on its island: a walled, turreted court on a rocky islet
# with a stone mole and a moored merchant ship; the three-stage tower of Sostratus (a tall square shaft of white
# limestone in two setbacks with rows of windows, an arched ramp to its door, Tritons blowing conches at its corners;
# an octagonal middle stage; a round colonnaded lantern with the beacon fire and its bronze mirror) crowned by a
# gilded Zeus Soter; a small Ionic temple of Isis Pharia on the island.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
ZS = 0.02            # the sea
Z0 = 0.07            # the island
ZC = Z0 + 0.1        # the court
TAS = 'kirec'
AK = 'mermer'


def levha(P, s0, s1, t0, t1, key, n, d=0.003):
    y.yuz_yon([P(s0, t0, d), P(s1, t0, d), P(s1, t1, d), P(s0, t1, d)], key, n)


def plaka(pts, key, yon, kalin=0.003):
    """a thin closed plate: the face pts toward yon, its back kalin behind, the rims round it"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    arka = [p - yon * kalin for p in pts]
    y.yuz_yon(pts, key, yon); y.yuz_yon(arka, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        y.yuz_yon([pts[i], pts[j], arka[j], arka[i]], key, (pts[i] + pts[j]) / 2 - c)


def yazi_bandi(P, n, s0, s1, t0, h, key='tas_koyu', d=0.003, tohum=0):
    """a band of (Greek) lettering: small marks of varying shape"""
    w = h * 0.6; s = s0; k = 0
    while s + w < s1:
        r = (tohum * 5 + k * 7) % 4
        if r == 0: levha(P, s, s + w * 0.3, t0, t0 + h, key, n, d); levha(P, s + w * 0.7, s + w, t0, t0 + h, key, n, d)
        elif r == 1: levha(P, s, s + w, t0, t0 + h * 0.25, key, n, d); levha(P, s + w * 0.35, s + w * 0.65, t0, t0 + h, key, n, d)
        elif r == 2: y.yuz_yon([P(s, t0, d), P(s + w, t0, d), P(s + w * 0.5, t0 + h, d)], key, n)
        else: levha(P, s, s + w, t0 + h * 0.75, t0 + h, key, n, d); levha(P, s + w * 0.35, s + w * 0.65, t0, t0 + h, key, n, d)
        s += w * 1.5; k += 1


def kat_pencereli(cx, cy, w, z0, h, nu, nv, key=TAS, pencere=('koyu', 0.38, 0.62, 0.22, 0.8), kapi=None):
    """a square stage w wide from z0, h high: on every face nu x nv window bays (square-headed, deep); kapi: a door
    bay (face 0, the front) as (u0, u1, v1)"""
    K = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
    dk, u0, u1, v0, v1 = pencere
    hh = h / nv
    for i in range(4):
        a, b = K[i], K[(i + 1) % 4]
        for r in range(nv):
            for c in range(nu):
                pa, pb = a.lerp(b, c / nu), a.lerp(b, (c + 1) / nu)
                if kapi and i == 0 and r == kapi[3] and c == nu // 2:
                    dikdortgen_acik(y, pa, pb, z0 + r * hh, hh, kapi[0], kapi[1], 0.0, kapi[2], (key, key, AK, 'ahsap'), derin=0.03, cerceve=(0.01, AK))
                else:
                    dikdortgen_acik(y, pa, pb, z0 + r * hh, hh, u0, u1, v0 * hh, v1 * hh, (key, key, AK, dk), derin=0.022, cerceve=(0.006, AK))
    return K


def figur(px, py, pz, s, aci, tur='zeus', key='altin'):
    """a statue (1 = its height) built facing -y then turned by aci: 'zeus' (robed, the right arm raised with a
    thunderbolt, a sceptre in the left), 'triton' (a merman on his coiled tail blowing a conch)"""
    with parca(y, (px, py, pz), aci, s):
        if tur == 'zeus':
            kutu_merkez(y, (0, 0), 0.3, 0.3, 0.06, AK)
            kornis(y, -0.15, 0.15, -0.15, 0.15, 0.06, 0.02, 0.015, AK, 'tac')
            y.yuz_yon([V(p.x, p.y, 0.08) for p in dikdortgen(-0.15, 0.15, -0.15, 0.15)], AK, Z)
            z = 0.08
            donel(y, (0, 0), [(0, z), (0.1, z), (0.1, z + 0.25), (0.09, z + 0.45), (0.11, z + 0.62), (0.13, z + 0.7), (0.06, z + 0.75), (0, z + 0.76)], key, n=12)
            boru(y, [V(-0.12, 0.0, z + 0.68), V(-0.02, -0.08, z + 0.48), V(0.08, -0.06, z + 0.22)], 0.035, key, n=6)   # the himation's fold
            kure(y, (0, -0.005, z + 0.82), 0.065, key, n=10, kat=5)
            kure(y, (0, -0.035, z + 0.78), 0.05, key, n=8, kat=4)   # the beard
            boru(y, [V(0.12, 0, z + 0.68), V(0.2, -0.02, z + 0.82), V(0.22, -0.03, z + 0.96)], 0.03, key, n=6)   # the raised arm
            boru(y, [V(0.2, -0.03, z + 0.98), V(0.25, -0.04, z + 1.04), V(0.2, -0.05, z + 1.08), V(0.26, -0.06, z + 1.14)], 0.016, key, n=5)   # the thunderbolt
            boru(y, [V(-0.12, 0, z + 0.68), V(-0.18, -0.03, z + 0.55)], 0.03, key, n=6)
            y.silindir((-0.19, -0.04), 0.012, 0.08, z + 1.0, key, n=6)                       # the sceptre
            kure(y, (-0.19, -0.04, z + 1.02), 0.025, key, n=8, kat=4)
        else:
            kutu_merkez(y, (0, 0), 0.5, 0.5, 0.08, AK)
            z = 0.08
            pts = [V(0.18 * math.cos(a), 0.18 * math.sin(a), z + 0.06 + 0.02 * a) for a in [k * 0.5 for k in range(13)]]
            boru(y, pts, 0.09, key, n=8, r_son=0.03)                                         # the coiled fish tail
            boru(y, [pts[-1], pts[-1] + V(0.08, 0.06, 0.05)], 0.03, key, n=5, r_son=0.005)
            for sg in (-1, 1):   # the tail fin
                plaka([pts[-1] + V(0.08, 0.06, 0.05), pts[-1] + V(0.2, 0.1 + sg * 0.08, 0.14), pts[-1] + V(0.1, 0.06 + sg * 0.12, 0.03)], key, V(0, sg, 0.3), 0.02)
            donel(y, (0, 0), [(0.12, z + 0.25), (0.13, z + 0.4), (0.14, z + 0.55), (0.08, z + 0.62), (0, z + 0.63)], key, n=10)   # the torso
            kure(y, (0, -0.01, z + 0.7), 0.075, key, n=10, kat=5)
            # the conch held up to the lips with both hands
            boru(y, [V(0, -0.08, z + 0.69), V(0.06, -0.2, z + 0.75), V(0.12, -0.3, z + 0.85)], 0.025, key, n=6, r_son=0.065)
            for sg in (-1, 1):
                boru(y, [V(sg * 0.13, 0, z + 0.58), V(sg * 0.12, -0.12, z + 0.62), V(0.05, -0.18, z + 0.72)], 0.032, key, n=6)


# ---------------------------------------------------------------- the sea and the island
y.bolum('Deniz ve ada')
GX0, GX1, GY0, GY1 = -1.2, 1.2, -1.2, 1.2
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, ZS, 'su', 'onarkasagsol')
y.yuz_yon([V(GX0, GY0, ZS), V(GX1, GY0, ZS), V(GX1, GY1, ZS), V(GX0, GY1, ZS)], 'su', Z)
IC = (0.05, 0.1)
NI = 36


def ada_r(a):
    return 1.0 + 0.06 * math.sin(3 * a + 0.4) + 0.04 * math.sin(5 * a + 1.3) + 0.02 * math.sin(9 * a)


kiyi = [V(IC[0] + ada_r(TAU * i / NI) * math.cos(TAU * i / NI), IC[1] + ada_r(TAU * i / NI) * 0.95 * math.sin(TAU * i / NI), ZS - 0.004) for i in range(NI)]
ust = [V(IC[0] + (ada_r(TAU * i / NI) - 0.1) * math.cos(TAU * i / NI), IC[1] + (ada_r(TAU * i / NI) - 0.1) * 0.95 * math.sin(TAU * i / NI), Z0) for i in range(NI)]
orta = [V(p.x, p.y, (ZS + Z0) / 2 + 0.008) for p in [a.lerp(b, 0.45) for a, b in zip(kiyi, ust)]]
y.serit(kiyi, orta, 'kaya_koyu')
y.serit(orta, ust, 'kaya')
y.yuz_yon(ust, 'kum_acik', Z)
# rocks along the shore, surf
for i in range(NI):
    a = TAU * (i + 0.4) / NI
    r_ = ada_r(a)
    for (dr, rr) in ((0.02, 0.035 + 0.015 * math.sin(i * 1.7)), (0.07, 0.025)):
        if (i + int(dr * 100)) % 3 == 0: continue
        p = V(IC[0] + (r_ + dr - 0.03) * math.cos(a), IC[1] + (r_ + dr - 0.03) * 0.95 * math.sin(a))
        donel(y, (p.x, p.y), [(rr, ZS - 0.01), (rr * 0.9, ZS + rr * 0.4), (rr * 0.5, ZS + rr * 0.8), (0, ZS + rr * 0.9)], 'kaya_koyu' if i % 2 else 'kaya', n=6, kat=i)
for i in range(NI):
    a0, a1 = TAU * i / NI, TAU * (i + 1) / NI
    if i % 4 == 1: continue
    p0, p1 = kiyi[i], kiyi[(i + 1) % NI]
    n0 = (p0 - V(IC[0], IC[1], p0.z)).normalized(); n1 = (p1 - V(IC[0], IC[1], p1.z)).normalized()
    y.yuz_yon([p0 + n0 * 0.01 + Z * 0.0025, p1 + n1 * 0.01 + Z * 0.0025, p1 + n1 * 0.035 + Z * 0.0025, p0 + n0 * 0.035 + Z * 0.0025], 'beyaz', Z)

# ---------------------------------------------------------------- the mole and the harbour
y.bolum('Dalgakiran')
mol = [V(-0.7, -0.5), V(-0.95, -0.85), V(-1.1, -1.08)]
MW = 0.09
sag = disa(mol, MW / 2, kapali=False); sol = disa(mol, -MW / 2, kapali=False)
for k in range(len(mol) - 1):
    duz_duvar(y, sag[k], sag[k + 1], 0.0, Z0 - 0.015, 'granit')
    duz_duvar(y, sol[k + 1], sol[k], 0.0, Z0 - 0.015, 'granit')
    y.yuz_yon([sag[k] + Z * (Z0 - 0.015), sag[k + 1] + Z * (Z0 - 0.015), sol[k + 1] + Z * (Z0 - 0.015), sol[k] + Z * (Z0 - 0.015)], 'zemin', Z)
    for (pa, pb) in ((sag[k], sag[k + 1]), (sol[k + 1], sol[k])):
        L_ = (pb - pa).length
        for m in range(int(L_ / 0.06)):
            p = pa.lerp(pb, (m + 0.5) / int(L_ / 0.06))
            kutu_merkez(y, (p.x, p.y), 0.022, 0.022, 0.012, 'granit', z0=Z0 - 0.015)   # bollards / merlons
# the mole's head: a small round beacon tower
kule_yuvarlak(y, (mol[-1].x, mol[-1].y), 0.07, 0.0, 0.2, 'granit', 'kubbe', 'bakir', mazgal_h=0.0, n=16, yarik_say=2)
y.yuz_yon([V(p.x, p.y, 0.0) for p in cokgen((mol[-1].x, mol[-1].y), 0.075, 16)], 'granit', -Z)
sancak(y, mol[-1].x, mol[-1].y, 0.27, boy=0.2, en=0.12, yuk=0.07, aci=-0.6)
# a merchant ship moored along the mole
with parca(y, (-0.76, -0.9, ZS), 0.95):
    hal = []
    for k in range(11):
        t = -1 + 2 * k / 10
        w_ = 0.065 * (1 - t * t) ** 0.55 + 0.003
        z_ = 0.03 + 0.025 * t * t + (0.02 * t if t > 0.6 else 0)
        xx = t * 0.24
        hal.append([V(xx, -w_, z_), V(xx, -w_ * 0.75, -0.006), V(xx, 0, -0.012), V(xx, w_ * 0.75, -0.006), V(xx, w_, z_)])
    for k in range(10):
        for m in range(4):
            q = [hal[k][m], hal[k + 1][m], hal[k + 1][m + 1], hal[k][m + 1]]
            yuz_dis(y, q, 'ahsap', V((q[0].x + q[1].x) / 2, 0, 0.04))
        y.yuz_yon([hal[k][0], hal[k][4], hal[k + 1][4], hal[k + 1][0]], 'ahsap_acik', Z)
    for uc, sg in ((0, -1), (10, 1)):
        y.yuz_yon([hal[uc][m] for m in range(5)], 'ahsap', V(sg, 0, 0))
    boru(y, [V(0.24, 0, 0.07), V(0.28, 0, 0.11), V(0.26, 0, 0.14)], 0.01, 'ahsap', n=5, r_son=0.004)   # the swan-neck stern
    y.silindir((0.0, 0), 0.006, 0.02, 0.42, 'ahsap', n=6)
    cubuk(y, V(0, -0.15, 0.39), V(0, 0.15, 0.39), 0.008, 'ahsap_koyu')
    pl = [V(0.004, -0.14, 0.385), V(0.004, 0.14, 0.385), V(0.03, 0.15, 0.16), V(0.03, -0.15, 0.16)]
    plaka(pl, 'kumas', X, 0.004)
    for k in range(3):
        cubuk(y, V(0.03, -0.15 + 0.1 * (k + 0.5), 0.17), V(0.005, -0.15 + 0.1 * (k + 0.5), 0.38), 0.003, 'boya_kirmizi', 0.0045)
    for sg in (-1, 1):
        boru(y, [V(0, sg * 0.15, 0.39), V(0.22 * sg, 0, 0.05)], 0.002, 'saz_koyu', n=4)
    kutu_merkez(y, (-0.14, 0), 0.08, 0.07, 0.035, 'ahsap_koyu', z0=0.035)
    for k in range(4):
        donel(y, (0.08 + k * 0.03, 0.02 * (-1) ** k), [(0, 0.04), (0.012, 0.042), (0.014, 0.06), (0.006, 0.074), (0.007, 0.08), (0, 0.08)], 'kerpic', n=6)

# ---------------------------------------------------------------- the walled court
y.bolum('Avlu')
CX, CY = 0.12, 0.2
CW = 0.5           # half size
K = dikdortgen(CX - CW, CX + CW, CY - CW, CY + CW)
B0 = dikdortgen(CX - CW - 0.03, CX + CW + 0.03, CY - CW - 0.03, CY + CW + 0.03)
for i in range(4):   # battered platform sides
    j = (i + 1) % 4
    e = B0[j] - B0[i]; n = V(e.y, -e.x).normalized()
    y.yuz_yon([B0[i] + Z * Z0, B0[j] + Z * Z0, K[j] + Z * ZC, K[i] + Z * ZC], TAS, n + Z * 0.3)
y.yuz_yon([V(p.x, p.y, ZC) for p in K], 'zemin', Z)
silme(y, K, ZC - 0.012, 0.012, 0.008, AK, 'tac')
parapet(y, K, ZC, 0.03, 0.022, 0.025, TAS)
for p in K:
    kule_yuvarlak(y, (p.x, p.y), 0.06, Z0, 0.2, TAS, 'konik', 'kiremit', cati_h=0.08, mazgal_h=0.0, n=16, yarik_say=3)
# the court gate (front) with its stair down to the island
GW = 0.1
kutu(y, V(CX - GW, CY - CW - 0.05, Z0), X, 2 * GW, 0.08, ZC - Z0 + 0.12, TAS, 'arkasagsolust')
dikdortgen_acik(y, V(CX - GW, CY - CW - 0.05), V(CX + GW, CY - CW - 0.05), Z0, ZC - Z0 + 0.12, 0.3, 0.7, 0.0, 0.13, (TAS, TAS, AK, 'ahsap'),
                derin=0.025, cerceve=(0.01, AK))
mazgal(y, V(CX - GW, CY - CW - 0.05), V(CX + GW, CY - CW - 0.05), ZC + 0.12, 0.025, 0.02, TAS)
mazgal(y, V(CX + GW, CY - CW + 0.03), V(CX - GW, CY - CW + 0.03), ZC + 0.12, 0.025, 0.02, TAS)
# fuel stores and the keepers' house round the inside of the wall, firewood, amphorae
for (x0, x1, y0, y1, h) in ((CX - CW + 0.03, CX - CW + 0.2, CY + 0.1, CY + CW - 0.03, 0.09), (CX + CW - 0.2, CX + CW - 0.03, CY + 0.1, CY + CW - 0.03, 0.09),
                            (CX - CW + 0.03, CX - CW + 0.16, CY - CW + 0.03, CY - 0.18, 0.07)):
    kk = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = kk[i], kk[(i + 1) % 4]
        if (b - a).length > 0.2:
            n_ = int((b - a).length / 0.12)
            for m in range(n_):
                dikdortgen_acik(y, a.lerp(b, m / n_), a.lerp(b, (m + 1) / n_), ZC, h, 0.35, 0.65, 0.0 if m == n_ // 2 else h * 0.45, h * 0.75,
                                ('siva_krem', 'siva_krem', AK, 'ahsap' if m == n_ // 2 else 'koyu'), derin=0.012)
        else:
            duz_duvar(y, a, b, ZC, ZC + h, 'siva_krem')
    cati_kirma(y, x0, x1, y0, y1, ZC + h, 0.05, 0.02, 'kiremit', 'kiremit2')
for k in range(6):
    xx = CX + 0.3 + (k % 3) * 0.05
    yy = CY - 0.4 + (k // 3) * 0.035
    boru(y, [V(xx - 0.02, yy, ZC + 0.008), V(xx + 0.02, yy, ZC + 0.008)], 0.007, 'kutuk', n=6)
    boru(y, [V(xx - 0.02, yy + 0.017, ZC + 0.02), V(xx + 0.02, yy + 0.017, ZC + 0.02)], 0.007, 'kutuk', n=6)
for k in range(5):
    donel(y, (CX + 0.3 + 0.025 * k, CY - 0.28 - 0.01 * (k % 2)), [(0, ZC), (0.008, ZC + 0.004), (0.012, ZC + 0.02), (0.006, ZC + 0.04), (0.007, ZC + 0.046), (0, ZC + 0.046)], 'kerpic', n=6)

# ---------------------------------------------------------------- the tower: first stage (square, two setbacks)
y.bolum('Kule birinci kat')
TX, TY = CX, CY + 0.06
W1, H1a = 0.5, 0.46
W2, H1b = 0.44, 0.38
z = ZC
kutu_merkez(y, (TX, TY), W1 + 0.06, W1 + 0.06, 0.035, AK, z0=z)
silme(y, dikdortgen(TX - W1 / 2 - 0.03, TX + W1 / 2 + 0.03, TY - W1 / 2 - 0.03, TY + W1 / 2 + 0.03), z + 0.035, 0.01, 0.006, AK, 'tac')
y.yuz_yon([V(p.x, p.y, z + 0.045) for p in dikdortgen(TX - W1 / 2 - 0.036, TX + W1 / 2 + 0.036, TY - W1 / 2 - 0.036, TY + W1 / 2 + 0.036)], AK, Z)
z += 0.045
K1 = kat_pencereli(TX, TY, W1, z, H1a, 3, 4, kapi=(0.3, 0.7, 0.085, 1))
for p in K1:   # quoins
    kutu_merkez(y, (p.x, p.y), 0.03, 0.03, H1a, AK, z0=z)
for r in range(1, 4):   # string courses between the window storeys
    silme(y, K1, z + r * H1a / 4 - 0.004, 0.007, 0.004, AK, 'duz')
z += H1a
silme(y, K1, z, 0.02, 0.012, AK, 'tac')
y.yuz_yon([V(p.x, p.y, z + 0.02) for p in disa(K1, 0.012)], TAS, Z)
# the dedication of Sostratus along the first cornice
for i in range(4):
    a, b = K1[i], K1[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    Pd = lambda s_, t_, d=0.002, a=a, e=e, nn=nn: V(a.x, a.y) + e * s_ + Z * (z - 0.04 + t_) + nn * d
    levha(Pd, 0.03, W1 - 0.03, 0.0, 0.034, AK, nn, 0.0015)
    yazi_bandi(Pd, nn, 0.04, W1 - 0.04, 0.008, 0.018, 'tas_koyu', 0.003, tohum=i)
z += 0.02
K2 = kat_pencereli(TX, TY, W2, z, H1b, 3, 3)
for p in K2:
    kutu_merkez(y, (p.x, p.y), 0.028, 0.028, H1b, AK, z0=z)
for r in range(1, 3):
    silme(y, K2, z + r * H1b / 3 - 0.004, 0.007, 0.004, AK, 'duz')
z += H1b
konsol_halka(y, K2, z, 0.03, 0.022, AK, 3)
Z1 = z + 0.03
KP = disa(K2, 0.022)
y.yuz_yon([V(p.x, p.y, Z1) for p in KP], 'zemin', Z)
parapet(y, KP, Z1, 0.03, 0.022, 0.02, TAS)
# Tritons blowing conches at the four corners
for p, a in zip(KP, (-math.pi * 0.75, -math.pi * 0.25, math.pi * 0.25, math.pi * 0.75)):
    d = (p - V(TX, TY)).normalized()
    q = p - d * 0.04
    figur(q.x, q.y, Z1, 0.2, a + math.pi / 2, 'triton', 'bronz')

# the arched ramp up to the door
y.bolum('Rampa')
RY0, RY1 = CY - CW + 0.035, TY - W1 / 2
RZ1 = ZC + 0.045 + H1a / 4          # the door is in the second window row
RW = 0.05
nr = 4
for k in range(nr):
    ya, yb = RY0 + (RY1 - RY0) * k / nr, RY0 + (RY1 - RY0) * (k + 1) / nr
    za, zb = ZC + (RZ1 - ZC) * k / nr, ZC + (RZ1 - ZC) * (k + 1) / nr
    for sx in (-1, 1):
        xx = TX + sx * RW
        a, b = (V(xx, ya), V(xx, yb)) if sx > 0 else (V(xx, yb), V(xx, ya))
        y.yuz_yon([V(a.x, a.y, ZC), V(b.x, b.y, ZC), V(b.x, b.y, (zb if sx > 0 else za) + 0.02), V(a.x, a.y, (za if sx > 0 else zb) + 0.02)], TAS, V(sx, 0))
        # an arch under each span (dark, on the side), the parapet's top
        if k:
            y.pencere(V(xx, ya, ZC), Y, V(sx, 0, 0), (yb - ya) * 0.15, 0.0, (yb - ya) * 0.7, (za - ZC) * 0.85, 'koyu', kemer=True, k_say=6)
        xi = TX + sx * (RW - 0.012)
        a2, b2 = (V(xi, yb), V(xi, ya)) if sx > 0 else (V(xi, ya), V(xi, yb))
        y.yuz_yon([V(a2.x, a2.y, (zb if sx > 0 else za)), V(b2.x, b2.y, (za if sx > 0 else zb)), V(b2.x, b2.y, (za if sx > 0 else zb) + 0.02), V(a2.x, a2.y, (zb if sx > 0 else za) + 0.02)], TAS, V(-sx, 0))
        y.yuz_yon([V(xx, ya, za + 0.02), V(xx, yb, zb + 0.02), V(xi, yb, zb + 0.02), V(xi, ya, za + 0.02)], AK, Z)
    y.yuz_yon([V(TX - RW, ya, za), V(TX + RW, ya, za), V(TX + RW, yb, zb), V(TX - RW, yb, zb)], 'zemin', Z)
for sx in (-1, 1):   # (the parapets' front ends only: the ramp's walk between them stays open)
    xa, xb = sorted((TX + sx * RW, TX + sx * (RW - 0.012)))
    y.yuz_yon([V(xa, RY0, ZC), V(xb, RY0, ZC), V(xb, RY0, ZC + 0.02), V(xa, RY0, ZC + 0.02)], TAS, -Y)

# ---------------------------------------------------------------- second stage: octagonal
y.bolum('Kule ikinci kat')
R2 = 0.17
z = Z1 + 0.012
ko = cokgen((TX, TY), R2, 8, kat=math.pi / 8)
donel(y, (TX, TY), [(0, z - 0.012), (R2 * 1.12, z - 0.012), (R2 * 1.12, z), (0, z)], AK, n=8, kat=math.pi / 8)
z0 = z
for r in range(3):
    hh = 0.13
    pencereli_duvar(y, ko, z, hh, [1] * 8, renk=(TAS, TAS, AK, 'koyu'), en=0.34, sivri=0.0, cerceve=(0.006, AK), v0=0.025, ust=0.02, derin=0.02)
    z += hh
    if r < 2:
        silme(y, ko, z - 0.008, 0.008, 0.006, AK, 'duz')
for p in ko:
    y.silindir((p.x, p.y), 0.012, z0, z, AK, n=8)
silme(y, ko, z, 0.03, 0.025, AK, 'tac')
z += 0.03
ko2 = disa(ko, 0.025)
y.yuz_yon([V(p.x, p.y, z) for p in ko2], 'zemin', Z)
parapet(y, ko2, z, 0.025, 0, 0.014, TAS)
Z2 = z

# ---------------------------------------------------------------- third stage: the round lantern with the fire
y.bolum('Fener')
R3 = 0.1
z = Z2
donel(y, (TX, TY), [(0, z), (R3 * 1.15, z), (R3 * 1.15, z + 0.02), (R3, z + 0.03), (0, z + 0.03)], AK, n=16)
z += 0.03
HL = 0.14
for i in range(8):
    a = TAU * (i + 0.5) / 8
    sutun(y, TX + R3 * 0.9 * math.cos(a), TY + R3 * 0.9 * math.sin(a), z, z + HL, 0.01, AK, 'iyon')
# the beacon: a fire basin and tongues of flame, the bronze mirror behind it
donel(y, (TX, TY), [(0, z), (0.05, z + 0.01), (0.06, z + 0.03), (0.055, z + 0.032), (0, z + 0.03)], 'bronz', n=12)
for k, (rr, hh, key) in enumerate(((0.045, 0.09, 'boya_kirmizi'), (0.032, 0.11, 'boya_sari'), (0.018, 0.13, 'altin'))):
    for m in range(5):
        a = TAU * (m + k * 0.3) / 5
        c = V(TX + rr * 0.6 * math.cos(a), TY + rr * 0.6 * math.sin(a))
        donel(y, (c.x, c.y), [(0, z + 0.03), (rr * 0.55, z + 0.03), (rr * 0.4, z + 0.03 + hh * 0.5), (0, z + 0.03 + hh * (0.8 + 0.2 * ((m + k) % 2)))], key, n=6, kat=a)
mir = V(TX, TY + 0.045)
ring = [mir + V(0.05 * math.cos(TAU * i / 14), 0, 0.05 * math.sin(TAU * i / 14)) + Z * (z + 0.085) for i in range(14)]
plaka(ring, 'altin', -Y, 0.008)
z += HL
# entablature, a little dome, Zeus Soter
donel(y, (TX, TY), [(0, z), (R3 * 1.08, z), (R3 * 1.08, z + 0.025), (R3 * 1.18, z + 0.035), (R3 * 1.18, z + 0.04), (0, z + 0.04)], AK, n=16)
z += 0.04
y.kubbe((TX, TY), R3 * 0.95, z, 0.06, 'bronz', n=16, kat=5)
z += 0.06
figur(TX, TY, z - 0.005, 0.15, 0.0, 'zeus', 'altin')

# ---------------------------------------------------------------- the temple of Isis Pharia
y.bolum('Isis tapinagi')
with parca(y, (-0.25, -0.62, Z0), 0.0):
    zemin(y, -0.17, 0.17, -0.1, 0.1, 0.03, AK, 'zemin', basamak=(('on', 0.14),), n_basamak=3)
    zt = sutunlu_revak(y, V(-0.1, -0.075), V(0.1, -0.075), 3, 0.03, 0.12, 'iyon', 0.011, AK)
    duvarlar(y, dikdortgen(-0.1, 0.1, -0.05, 0.08), 0.03, zt - 0.02, AK)
    kapi(y, V(-0.04, -0.05), V(0.04, -0.05), 0.03, 0.6, 0.09, (AK, AK, AK, 'ahsap'), derin=0.015)
    kutu(y, V(-0.115, -0.09, zt - 0.02), X, 0.23, 0.18, 0.02, AK)
    alinlik(y, V(-0.12, -0.092), V(0.12, -0.092), zt, 0.05, 0.18, AK, 'lacivert', 0.008, 'kiremit')
    kure(y, (0, -0.09, zt + 0.058), 0.01, 'altin', n=8, kat=4)
# palms and a little garden by the temple
for (px, py, b) in ((0.55, -0.55, 0.16), (0.88, -0.55, 0.15), (0.6, 0.7, 0.17), (-0.62, 0.68, 0.16), (-0.7, 0.45, 0.14), (0.8, 0.5, 0.15)):
    agac(y, px, py, Z0, b, 'palmiye')

# ---------------------------------------------------------------- the colossi of Ptolemy II and Arsinoe II before the gate
y.bolum('Kolos heykeller')


def kolos(px, py, pz, H, tur='kral', aci=0.0, K='granit_kizil'):
    """a colossal standing statue in Egyptian style (1 = its height) facing -y, turned by aci, on a moulded pedestal:
    'kral' (Ptolemy as pharaoh: kilt, nemes, double crown, left foot forward), 'kralice' (Arsinoe as Isis: sheath
    dress, wig, the crown of disk and horns)"""
    with parca(y, (px, py, pz), aci, H):
        kutu_merkez(y, (0, -0.02), 0.3, 0.34, 0.12, AK)
        kornis(y, -0.15, 0.15, -0.19, 0.15, 0.12, 0.02, 0.016, AK, 'tac')
        y.yuz_yon([V(p.x, p.y, 0.14) for p in dikdortgen(-0.15, 0.15, -0.19, 0.15)], AK, Z)
        Pk = lambda s_, t_, d=0.002: V(s_, -0.19, t_) - Y * d
        levha(Pk, -0.1, 0.1, 0.03, 0.09, 'tas_koyu', -Y, 0.0015)
        yazi_bandi(Pk, -Y, -0.09, 0.09, 0.045, 0.03, AK, 0.003, tohum=3 if tur == 'kral' else 5)
        z0 = 0.14
        kutu_merkez(y, (0, 0.04), 0.16, 0.05, 0.6, K, z0=z0)                                # back pillar
        if tur == 'kral':
            for sg, yf in ((-1, -0.1), (1, 0.0)):
                kutu_merkez(y, (sg * 0.04, yf - 0.02), 0.045, 0.1, 0.028, K, z0=z0)
                boru(y, [V(sg * 0.04, yf, z0 + 0.03), V(sg * 0.04, yf * 0.55, z0 + 0.24), V(sg * 0.045, -0.01, z0 + 0.42)], 0.026, K, n=6, r_son=0.038)
            kutu_merkez(y, (0, -0.025), 0.05, 0.1, 0.34, K, z0=z0)                                   # (the stone left between the legs)
            donel(y, (0, -0.01), [(0, z0 + 0.33), (0.07, z0 + 0.33), (0.082, z0 + 0.35), (0.075, z0 + 0.46), (0, z0 + 0.46)], K, n=10)
            y.yuz_yon([V(-0.02, -0.092, z0 + 0.45), V(0.02, -0.092, z0 + 0.45), V(0.026, -0.098, z0 + 0.34), V(-0.026, -0.098, z0 + 0.34)], 'boya_sari', -Y)
            hs = [[V(hw * math.cos(TAU * i / 12), -0.01 + hd * math.sin(TAU * i / 12), z0 + zz) for i in range(12)]
                  for zz, hw, hd in ((0.45, 0.068, 0.048), (0.56, 0.09, 0.052), (0.66, 0.115, 0.052), (0.69, 0.085, 0.042), (0.71, 0.035, 0.03))]
            for k in range(len(hs) - 1):
                y.serit(hs[k], hs[k + 1], K)
            y.yuz_yon(hs[-1], K, Z)
            for sg in (-1, 1):
                kure(y, (sg * 0.112, -0.01, z0 + 0.655), 0.032, K, n=8, kat=4)
                boru(y, [V(sg * 0.115, -0.01, z0 + 0.65), V(sg * 0.122, -0.015, z0 + 0.54), V(sg * 0.11, -0.02, z0 + 0.42)], 0.024, K, n=6, r_son=0.02)
                kutu_merkez(y, (sg * 0.055, -0.04), 0.024, 0.03, 0.09, 'boya_sari', z0=z0 + 0.6)    # the nemes lappets
            donel(y, (0, -0.02), [(0, z0 + 0.71), (0.04, z0 + 0.715), (0.05, z0 + 0.75), (0.046, z0 + 0.79), (0, z0 + 0.81)], K, n=8)
            cubuk(y, V(0, -0.066, z0 + 0.77), V(0, -0.076, z0 + 0.745), 0.012, K, 0.01)                 # the nose
            cubuk(y, V(0, -0.055, z0 + 0.725), V(0, -0.06, z0 + 0.69), 0.014, K, 0.012)                  # the beard
            donel(y, (0, -0.02), [(0, z0 + 0.77), (0.054, z0 + 0.77), (0.056, z0 + 0.83), (0.04, z0 + 0.835), (0, z0 + 0.835)], 'boya_kirmizi', n=10)
            donel(y, (0, -0.02), [(0.04, z0 + 0.83), (0.04, z0 + 0.88), (0.028, z0 + 0.915), (0, z0 + 0.925)], 'beyaz', n=10)
            kure(y, (0, -0.02, z0 + 0.93), 0.014, 'beyaz', n=8, kat=4)
            boru(y, [V(0, -0.07, z0 + 0.79), V(0, -0.078, z0 + 0.81)], 0.006, 'altin', n=5)
        else:
            donel(y, (0, -0.01), [(0, z0), (0.07, z0), (0.074, z0 + 0.2), (0.082, z0 + 0.42), (0.078, z0 + 0.55), (0.1, z0 + 0.66), (0.04, z0 + 0.7), (0, z0 + 0.705)], K, n=10)
            for sg in (-1, 1):
                boru(y, [V(sg * 0.09, -0.01, z0 + 0.65), V(sg * 0.1, -0.02, z0 + 0.52), V(sg * 0.07, -0.06, z0 + 0.46 if sg < 0 else z0 + 0.56)], 0.022, K, n=6)
            donel(y, (0, -0.005), [(0, z0 + 0.65), (0.062, z0 + 0.66), (0.064, z0 + 0.74), (0.052, z0 + 0.8), (0, z0 + 0.81)], 'koyu', n=10)
            donel(y, (0, -0.02), [(0, z0 + 0.68), (0.042, z0 + 0.69), (0.046, z0 + 0.73), (0.04, z0 + 0.77), (0, z0 + 0.78)], K, n=8)
            cubuk(y, V(0, -0.064, z0 + 0.74), V(0, -0.072, z0 + 0.72), 0.011, K, 0.009)
            kutu_merkez(y, (0, -0.07), 0.13, 0.008, 0.04, 'turkuaz', z0=z0 + 0.58)                         # the broad collar
            donel(y, (0, -0.005), [(0.045, z0 + 0.8), (0.05, z0 + 0.84), (0, z0 + 0.845)], 'altin', n=10)
            for sg in (-1, 1):   # cow horns round the sun disk
                boru(y, [V(sg * 0.012, -0.005, z0 + 0.84), V(sg * 0.06, -0.005, z0 + 0.87), V(sg * 0.064, -0.005, z0 + 0.93), V(sg * 0.04, -0.005, z0 + 0.97)], 0.008, 'altin', n=5)
            ring = [V(0.045 * math.cos(TAU * i / 14), -0.012, z0 + 0.9 + 0.045 * math.sin(TAU * i / 14)) for i in range(14)]
            plaka(ring, 'boya_kirmizi', -Y, 0.008)


GY_ = CY - CW - 0.13
kolos(CX - 0.175, GY_, Z0, 0.34, 'kral')
kolos(CX + 0.175, GY_, Z0, 0.32, 'kralice')
# the paved way from the landing to the gate, sphinxes along it
y.yuz_yon([V(CX - 0.07, -0.76, Z0 + 0.0015), V(CX + 0.07, -0.76, Z0 + 0.0015), V(CX + 0.07, CY - CW - 0.05, Z0 + 0.0015), V(CX - 0.07, CY - CW - 0.05, Z0 + 0.0015)], 'zemin', Z)
for sx in (-1, 1):
    for k, yy in enumerate((-0.58, -0.68)):
        with parca(y, (CX + sx * 0.1, yy, Z0), 0 if sx < 0 else math.pi):   # (facing the way)
            kutu_merkez(y, (0, 0), 0.07, 0.03, 0.015, AK)
            boru(y, [V(-0.028, 0, 0.024), V(0.0, 0, 0.026), V(0.012, 0, 0.029)], 0.009, 'granit', n=6, r_son=0.01)
            for s2 in (-1, 1):
                cubuk(y, V(0.012, s2 * 0.006, 0.018), V(0.032, s2 * 0.006, 0.018), 0.006, 'granit', 0.005)
            donel(y, (0.015, 0), [(0.012, 0.019), (0.013, 0.033), (0.01, 0.042), (0, 0.045)], 'granit', n=8)
            kure(y, (0.019, 0, 0.047), 0.008, 'granit', n=8, kat=4)

# ---------------------------------------------------------------- the landing quay with its cargo
y.bolum('Iskele')
QX0, QX1, QY0, QY1 = CX - 0.15, CX + 0.2, -1.0, -0.73
kutu(y, V(QX0, QY0, 0.0), X, QX1 - QX0, QY1 - QY0, Z0, 'granit', 'onsagsolust')
y.yuz_yon([V(QX0, QY0, Z0), V(QX1, QY0, Z0), V(QX1, QY1, Z0), V(QX0, QY1, Z0)], 'zemin', Z)
silme(y, [V(QX0, QY1), V(QX0, QY0), V(QX1, QY0), V(QX1, QY1)], Z0 - 0.008, 0.008, 0.005, 'granit', 'duz', kapali=False)
for (bx, by) in ((QX0 + 0.015, QY0 + 0.02), (QX1 - 0.015, QY0 + 0.02), (QX0 + 0.015, QY0 + 0.14), (QX1 - 0.015, QY0 + 0.14)):
    donel(y, (bx, by), [(0, Z0), (0.007, Z0), (0.007, Z0 + 0.012), (0.009, Z0 + 0.016), (0, Z0 + 0.017)], 'bronz', n=8)
merdiven(y, (QX1 + 0.05, QY0 + 0.08), math.pi, 0.06, ZS, Z0, n=4, key='granit')
# amphorae in stacks, bales, a crate, porters
for k in range(9):
    ax_, ay_ = QX1 - 0.07 + (k % 3) * 0.018, QY0 + 0.05 + (k // 3) * 0.02
    donel(y, (ax_, ay_), [(0, Z0), (0.004, Z0 + 0.004), (0.008, Z0 + 0.016), (0.006, Z0 + 0.03), (0.003, Z0 + 0.034), (0.0035, Z0 + 0.04), (0, Z0 + 0.04)], 'kerpic', n=6)
for (bx, by, a_) in ((QX0 + 0.05, QY0 + 0.1, 0.2), (QX0 + 0.08, QY0 + 0.06, -0.1)):
    kutu_merkez(y, (bx, by), 0.03, 0.022, 0.02, 'kumas', z0=Z0, aci=a_)
kutu_merkez(y, (QX0 + 0.06, QY0 + 0.17), 0.028, 0.028, 0.024, 'ahsap', z0=Z0, aci=0.3)
# a merchant galley moored at the quay head and two fishing skiffs out on the water


def tekne(px, py, aci, L=0.16, w=0.035, key='ahsap', yelken=None):
    """a small open boat (built along +x, turned to aci): hull, thwarts, oars; yelken: a sail of that key"""
    with parca(y, (px, py, ZS), aci):
        hal = []
        for k in range(9):
            t = -1 + 2 * k / 8
            w_ = w * (1 - t * t) ** 0.55 + 0.002
            z_ = 0.012 + 0.014 * t * t
            hal.append([V(t * L / 2, -w_, z_), V(t * L / 2, -w_ * 0.6, -0.003), V(t * L / 2, 0, -0.005), V(t * L / 2, w_ * 0.6, -0.003), V(t * L / 2, w_, z_)])
        for k in range(8):
            for m in range(4):
                q = [hal[k][m], hal[k + 1][m], hal[k + 1][m + 1], hal[k][m + 1]]
                yuz_dis(y, q, key, V((q[0].x + q[1].x) / 2, 0, 0.03))
            y.yuz_yon([hal[k][0], hal[k][4], hal[k + 1][4], hal[k + 1][0]], 'ahsap_koyu', Z)
        for uc, sg in ((0, -1), (8, 1)):   # (the stem and stern posts close the hull's ends)
            y.yuz_yon(hal[uc], key, V(sg, 0, 0))
        for k in (-1, 0, 1):
            cubuk(y, V(k * L * 0.22, -w * 0.8, 0.012), V(k * L * 0.22, w * 0.8, 0.012), 0.004, 'ahsap_acik')
        for sg in (-1, 1):
            cubuk(y, V(-L * 0.05, sg * w * 0.9, 0.016), V(-L * 0.2, sg * (w + 0.05), -0.002), 0.0025, 'ahsap_acik')
        if yelken:
            y.silindir((0.0, 0), 0.003, 0.0, 0.16, 'ahsap', n=5)
            plaka([V(0.002, -0.06, 0.15), V(0.002, 0.06, 0.15), V(0.012, 0.055, 0.05), V(0.012, -0.055, 0.05)], yelken, X, 0.003)


tekne(QX1 + 0.09, QY0 - 0.04, 1.4, 0.2, 0.04, 'ahsap', 'kumas')
tekne(0.78, -0.88, 0.6, 0.13, 0.028, 'ahsap_koyu')
tekne(0.98, 0.6, 2.2, 0.13, 0.028, 'ahsap', 'kumas')
for (ax, ay, a_) in ((CX - 0.02, -0.8, -math.pi / 2), (CX + 0.03, -0.6, math.pi / 2)):
    with parca(y, (ax, ay, Z0), a_, 0.9):   # porters carrying amphorae
        donel(y, (0, 0), [(0, 0), (0.007, 0.0), (0.008, 0.02), (0.006, 0.032), (0, 0.034)], 'beyaz', n=6)
        kure(y, (0, 0, 0.04), 0.006, 'kirmizi', n=6, kat=3)
        donel(y, (0.0, 0.0), [(0, 0.046), (0.005, 0.048), (0.007, 0.058), (0.003, 0.066), (0, 0.067)], 'kerpic', n=6)

# ---------------------------------------------------------------- warehouses for the beacon's fuel, a cistern with a shaduf
y.bolum('Ambarlar')
for (wy0, wy1) in ((-0.2, 0.08), (0.18, 0.42)):
    wx0, wx1 = 0.7, 0.86
    KW_ = dikdortgen(wx0, wx1, wy0, wy1)
    for i in range(4):
        a, b = KW_[i], KW_[(i + 1) % 4]
        nb = max(1, round((b - a).length / 0.07))
        for k in range(nb):
            kapi_ = i == 3 and k == nb // 2
            dikdortgen_acik(y, a.lerp(b, k / nb), a.lerp(b, (k + 1) / nb), Z0, 0.085, 0.34, 0.66, 0.0 if kapi_ else 0.05, 0.06 if kapi_ else 0.07,
                            ('siva_krem', 'siva_krem', AK, 'ahsap' if kapi_ else 'koyu'), derin=0.012, cerceve=(0.005, AK) if kapi_ else None)
    silme(y, KW_, Z0, 0.01, 0.005, TAS, 'duz')
    cati_kirma(y, wx0, wx1, wy0, wy1, Z0 + 0.085, 0.05, 0.02, 'kiremit', 'kiremit2')
    for k in range(3):   # firewood stacked against the wall
        boru(y, [V(wx0 - 0.012, wy0 + 0.03 + k * 0.004, Z0 + 0.006 + k * 0.009), V(wx0 - 0.012, wy0 + 0.11 + k * 0.004, Z0 + 0.006 + k * 0.009)], 0.0055, 'kutuk', n=6)
        boru(y, [V(wx0 - 0.024, wy0 + 0.03, Z0 + 0.006 + k * 0.009), V(wx0 - 0.024, wy0 + 0.11, Z0 + 0.006 + k * 0.009)], 0.0055, 'kutuk', n=6)
# the cistern on the west side, a shaduf over it, a keeper
havuz(y, -0.56, -0.42, -0.08, 0.16, Z0 + 0.02, derin=0.02, kenar=0.015, key=TAS)
kutu(y, V(-0.575, -0.095, Z0), X, 0.17, 0.27, 0.02, TAS, 'onarkasagsol')
y.silindir((-0.4, 0.2), 0.005, Z0, Z0 + 0.09, 'ahsap', n=5)
cubuk(y, V(-0.36, 0.24, Z0 + 0.06), V(-0.47, 0.1, Z0 + 0.11), 0.004, 'ahsap')
kure(y, (-0.36, 0.24, Z0 + 0.055), 0.01, 'kaya_koyu', n=6, kat=3)
boru(y, [V(-0.47, 0.1, Z0 + 0.11), V(-0.47, 0.1, Z0 + 0.05)], 0.0012, 'saz_koyu', n=4)
donel(y, (-0.47, 0.1), [(0, Z0 + 0.04), (0.006, Z0 + 0.042), (0.007, Z0 + 0.05), (0, Z0 + 0.05)], 'kerpic', n=6)

calistir(y, 'lm_feneri')
