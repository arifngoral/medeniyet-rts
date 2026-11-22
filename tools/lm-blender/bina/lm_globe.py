# Globe Tiyatrosu (lm_globe): Shakespeare's Globe on Bankside. A twenty-sided open-air playhouse: three jettied storeys of
# lime-plastered timber framing outside, open galleries with balustrades and seated playgoers inside, a thatched ring
# roof; in the yard the groundlings round the stage with its painted pillars and the "heavens" roof, the frons scenae of
# the tiring house, the hut with the flag; two stair turrets, the Thames bank with a wharf, river stairs and wherries.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from ingiliz_ek import *
from frank_ortak import ev
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04                    # ground
ZW = 0.012                   # the Thames
KY = -0.97                   # the bank
N = 20
T0 = math.radians(9)         # vertex angles: facets are centred on 18 + 18 i degrees (90: the stage, 270: the entrance)
RO, RI, RB = 0.84, 0.62, 0.81  # outer wall, gallery front, gallery back
JET = 0.012                  # jetty of each upper storey
ZG = Z0 + 0.03               # ground gallery floor (a brick footing below)
KH = (0.17, 0.14, 0.13)    # storeys
ZK = [ZG, ZG + KH[0], ZG + KH[0] + KH[1], ZG + sum(KH)]
ZE = ZK[3]                   # eaves
ZR = ZE + 0.17               # ring roof ridge
RM = (RO + RI) / 2 + 0.01
SAH = range(2, 7)            # stage facets (tiring house)
SIVA, AH = 'siva', 'ahsap_koyu'


def P(r, i, z=0.0):
    t = T0 + TAU * i / N
    return V(r * math.cos(t), r * math.sin(t), z)


def ac(i):   # facet centre angle
    return T0 + TAU * (i + 0.5) / N


# ---------------------------------------------------------------- ground and river
y.bolum('Zemin, Thames kıyısı')
su_ve_kiyi(y, -1.15, 1.15, -1.2, KY, ZW, Z0, KY, 'ahsap_dikey', rihtim=False)
kutu(y, V(-1.15, KY, 0), X, 2.3, 1.12 - KY, Z0, 'toprak', 'arkasagsol')
# the bank: a timber revetment of planks between piles
duz_duvar(y, V(-1.15, KY), V(1.15, KY), ZW - 0.006, Z0, 'ahsap_dikey')
for k in range(24):
    x = -1.12 + k * 0.097
    y.prizma((x, KY - 0.004), 0.0055, ZW - 0.004, Z0 + 0.012, 'kutuk', n=6)
y.yuz_yon([V(-1.15, KY, Z0), V(1.15, KY, Z0), V(1.15, 1.12, Z0), V(-1.15, 1.12, Z0)], 'cimen', Z)
yer = lambda pts, k='toprak', dz=0.0012: y.yuz_yon([V(p[0], p[1], Z0 + dz) for p in pts], k, Z)
yer([(-0.09, KY), (0.09, KY), (0.07, -0.8), (-0.07, -0.8)])                  # the path from the river stairs
yer([(-0.6, -0.86), (0.6, -0.86), (0.6, -0.78), (-0.6, -0.78)])              # Bankside lane
# a timber wharf and river stairs down to the water
kutu(y, V(-0.6, KY - 0.1, ZW + 0.006), X, 0.36, 0.1, Z0 - ZW - 0.006 + 0.004, 'ahsap', 'onsagsolust')
for k in range(5):
    y.prizma((-0.58 + k * 0.08, KY - 0.094), 0.006, 0.0, Z0 + 0.008, 'kutuk', n=6)
for k in range(4):
    yy = KY - 0.004 - k * 0.018
    kutu(y, V(-0.06, yy - 0.018, 0.0), X, 0.12, 0.018, Z0 - (k + 1) * (Z0 - ZW) / 5, 'ahsap_acik', 'onsagsolust')
# wherries with their watermen
for (x, yy, a) in ((0.15, -1.06, 0.3), (0.55, -1.1, -0.2), (-0.95, -1.08, 2.8)):
    sandal(y, x, yy, ZW, a, L=0.1, B=0.024)
    insan(y, x, yy, ZW + 0.004, 'boya_kirmizi' if x > 0.3 else 'koyu', 0.85, aci=a)
sandal(y, -0.15, -1.0, ZW, 0.05, L=0.1, B=0.024, kurek=False)

# ---------------------------------------------------------------- outer walls: plastered timber framing, jettied
y.bolum('Dış duvarlar: sıvalı ahşap çatma')


def cerceve_serit(a, b, z0, z1, pencere=None, aralik=2, ileri=0.0015, en=0.006):
    """timber framing painted on a plastered wall a->b as thin strips standing a hair proud of it: sill and head rails,
    posts at the window and between, braces in the outer panels; pencere = (u0, u1, v0, v1) the opening it frames"""
    a, b, L, e, nc = eksen(a, b)
    o = nc * ileri
    Pq = lambda u, zz: a + e * (u * L) + o + Z * zz
    h = en / 2
    def serit(p, q, yon_n=nc):
        d = (q - p); d.normalize()
        s = d.cross(nc).normalized() * h
        y.yuz_yon([p - s, q - s, q + s, p + s], AH, nc)
    serit(Pq(0, z0 + h), Pq(1, z0 + h))
    serit(Pq(0, z1 - h), Pq(1, z1 - h))
    us = [0.0, 1.0]
    if pencere:
        u0, u1, v0, v1 = pencere
        us += [u0 - en / L, u1 + en / L]
        serit(Pq(0, z0 + v0 - h), Pq(u0 - en / L, z0 + v0 - h)); serit(Pq(u1 + en / L, z0 + v0 - h), Pq(1, z0 + v0 - h))
        serit(Pq(u0 - en / L, z0 + v1 + h), Pq(u1 + en / L, z0 + v1 + h))
        # braces in the two outer panels
        serit(Pq(0.06, z0 + en), Pq(u0 - en / L - 0.02, z0 + v0 - en))
        serit(Pq(1 - 0.06, z0 + en), Pq(u1 + en / L + 0.02, z0 + v0 - en))
    for u in us[2:]:
        serit(Pq(u, z0 + en), Pq(u, z1 - en))


for i in range(N):
    t = ac(i)
    for k in range(3):
        r = RO + JET * k
        a, b = P(r, i), P(r, i + 1)
        z0, z1 = ZK[k], ZK[k + 1]
        h = z1 - z0
        if i == 14 and k == 0:   # the entrance: a wide door under a carved board
            dikdortgen_acik(y, a, b, z0, h, 0.32, 0.68, 0.0, h * 0.78, (SIVA, AH, 'ahsap_acik', 'ahsap'), derin=0.014, cerceve=(0.006, AH))
            m = (a + b) / 2; _, _, _, e, nc = eksen(a, b)
            kutu3(y, m + nc * 0.006 + Z * (z0 + h * 0.9), e, nc, Z, 0.12, 0.006, 0.022, 'ahsap', ('+x', '-x', '+y', '+z', '-z'))
            y.yuz_yon([m + nc * 0.0092 + e * s1 + Z * (z0 + h * 0.9 + s2) for s1, s2 in ((-0.05, -0.006), (0.05, -0.006), (0.05, 0.006), (-0.05, 0.006))], 'altin', nc)
            continue
        if i in (12, 16) and k < 2:   # behind the stair turrets
            duz_duvar(y, a, b, z0, z1, SIVA); continue
        w = 0.05 if k else 0.044
        v0, v1 = h * 0.34, h * 0.78
        acs = acikli_duvar(y, a, b, z0, z1, [(0.5, w, v0, v1)], (SIVA, AH, 'ahsap_acik', 'cam'), derin=0.008, pay=0.0)
        L = (b - a).length
        for acx in acs:
            pa, pb = acx[0], acx[1]
            _, _, _, e, nc = eksen(a, b)
            cubuk3(y, (pa + pb) / 2 - nc * 0.004 + Z * (z0 + v0), (pa + pb) / 2 - nc * 0.004 + Z * (z0 + v1), 0.004, AH, nc, 0.003)
        cerceve_serit(a, b, z0, z1, (0.5 - w / 2 / L, 0.5 + w / 2 / L, v0, v1))
        if k:   # the jetty's bressumer beam and its soffit
            ai, bi = P(r - JET, i), P(r - JET, i + 1)
            _, _, _, e, nc = eksen(a, b)
            y.yuz_yon([a + Z * (z0 - 0.012), b + Z * (z0 - 0.012), b + Z * z0, a + Z * z0], AH, nc)
            y.yuz_yon([ai + Z * (z0 - 0.012), bi + Z * (z0 - 0.012), b + Z * (z0 - 0.012), a + Z * (z0 - 0.012)], AH, -Z)
# corner posts at the outer vertices, the brick footing
for i in range(N):
    for k in range(3):
        r = RO + JET * k + 0.003
        cubuk(y, P(r, i, ZK[k]), P(r, i, ZK[k + 1] - (0.012 if k < 2 else 0)), 0.009, AH)
donel(y, (0, 0), [(RO + 0.012, 0.0), (RO + 0.012, ZG), (RO, ZG + 0.002)], 'tugla', n=N, kat=T0)

# ---------------------------------------------------------------- the thatched ring roof
y.bolum('Saz çatı halkası')
RE = RO + 2 * JET + 0.05
donel(y, (0, 0), [(RE, ZE - 0.03), (RE, ZE)], 'saz_koyu', n=N, kat=T0)
for i in range(N):   # the eave soffit (seen from below)
    y.yuz_yon([P(RE, i, ZE - 0.03), P(RE, i + 1, ZE - 0.03), P(RO + 2 * JET, i + 1, ZE - 0.03), P(RO + 2 * JET, i, ZE - 0.03)], 'ahsap_koyu', -Z)


def saz_yamac(E, T, nr, lip, dis, cizgi=4, tohum=0):
    """a thatched slope of the ring from the eave E to the top T ((r, z) pairs), laid in nr courses: each course's butt
    stands lip proud of the one below (a step facing down the slope), straw strokes in the darker tone run down every
    course on every facet. dis: +1 the slope faces away from the yard, -1 towards it. Returns T as moved out by the
    courses (where the ridge thatch starts)"""
    import random
    rg = random.Random(tohum)
    dr, dz = T[0] - E[0], T[1] - E[1]
    ln = math.hypot(dr, dz)
    nn = (dz / ln, -dr / ln) if dis > 0 else (-dz / ln, dr / ln)   # (away from the roof's body, upwards)
    # (the courses' base line ends that much under T, so the last course ends on T: the ridge keeps its steep flank
    # and the far slope stays hidden behind it)
    dr -= nn[0] * lip * (nr - 1); dz -= nn[1] * lip * (nr - 1)
    Q = lambda t, k: (E[0] + dr * t + nn[0] * lip * k, E[1] + dz * t + nn[1] * lip * k)
    pts = [E]
    for j in range(1, nr):
        pts += [Q(j / nr, j - 1), Q(j / nr, j)]
    pts.append(Q(1.0, nr - 1))
    donel(y, (0, 0), pts if dis > 0 else pts[::-1], 'saz', n=N, kat=T0)
    # straw strokes on each course (a hair above it)
    for j in range(nr):
        A, B = Q(j / nr, j), Q((j + 1) / nr, j)
        if j == 0: A = E
        for i in range(N):
            for _ in range(cizgi):
                u = rg.uniform(0.06, 0.94)
                s0, s1 = rg.uniform(0.02, 0.2), rg.uniform(0.7, 0.98)
                du = rg.uniform(0.0018, 0.003)
                def K(uu, s):
                    r_ = A[0] + (B[0] - A[0]) * s + nn[0] * 0.0018
                    z_ = A[1] + (B[1] - A[1]) * s + nn[1] * 0.0018
                    return P(r_, i, z_).lerp(P(r_, i + 1, z_), uu)
                Lf = (P(1.0, i) - P(1.0, i + 1)).length
                d_ = du / (Lf * (A[0] + B[0]) / 2)
                q = [K(u - d_, s0), K(u + d_, s0), K(u + d_, s1), K(u - d_, s1)]
                yn = V(math.cos(ac(i)) * nn[0], math.sin(ac(i)) * nn[0], nn[1])
                y.yuz_yon(q, 'saz_koyu', yn)
    return Q(1.0, nr - 1)


Tdis = saz_yamac((RE, ZE), (RM + 0.045, ZR - 0.05), 6, 0.0055, 1, cizgi=9, tohum=1)
donel(y, (0, 0), [Tdis, (RM + 0.012, ZR - 0.004)], 'saz_koyu', n=N, kat=T0)   # the darker ridge thatch
donel(y, (0, 0), [(RM + 0.012, ZR - 0.004), (RM, ZR + 0.01), (RM - 0.012, ZR - 0.004)], 'saz_koyu', n=N, kat=T0)
RIE = RI - 0.035
Tic = saz_yamac((RIE, ZE + 0.012), (RM - 0.04, ZR - 0.05), 4, 0.005, -1, cizgi=6, tohum=2)
donel(y, (0, 0), [(RM - 0.012, ZR - 0.004), Tic], 'saz_koyu', n=N, kat=T0)
donel(y, (0, 0), [(RIE, ZE + 0.012), (RIE, ZE - 0.014)], 'saz_koyu', n=N, kat=T0)
for i in range(N):   # the inner eave's soffit, out to the gallery front
    y.yuz_yon([P(RIE, i, ZE - 0.014), P(RIE, i + 1, ZE - 0.014), P(RI, i + 1, ZE - 0.014), P(RI, i, ZE - 0.014)], 'ahsap_koyu', -Z)

# ---------------------------------------------------------------- the galleries (inside)
y.bolum('Galeriler ve seyirciler')
RENKLER = ['boya_kirmizi', 'koyu', 'boya_yesil', 'lacivert', 'kirmizi', 'ahsap_acik', 'boya_sari', 'kece', 'ahsap']
rs = __import__('random').Random(5)
for i in range(N):
    if i in SAH: continue
    t = ac(i)
    seyirci = True                         # every gallery is full of playgoers
    for k in range(3):
        z0, z1 = ZK[k], ZK[k + 1]
        a, b = P(RI, i + 1), P(RI, i)       # facing the yard
        ab, bb = P(RB, i + 1), P(RB, i)
        _, _, L, e, nc = eksen(a, b)
        # floor, back wall
        y.yuz_yon([a + Z * z0, b + Z * z0, bb + Z * z0, ab + Z * z0], 'ahsap', Z)
        duz_duvar(y, ab, bb, z0, z1, SIVA)
        # two raked benches
        for s, (d0, d1, hh) in enumerate(((0.06, 0.12, 0.022), (0.12, 0.19, 0.044))):
            p0, p1 = a.lerp(ab, d0 / (RB - RI)), b.lerp(bb, d0 / (RB - RI))
            q0, q1 = a.lerp(ab, d1 / (RB - RI)), b.lerp(bb, d1 / (RB - RI))
            y.yuz_yon([p0 + Z * (z0 + hh), p1 + Z * (z0 + hh), q1 + Z * (z0 + hh), q0 + Z * (z0 + hh)], 'ahsap_acik', Z)
            y.yuz_yon([p0 + Z * z0, p1 + Z * z0, p1 + Z * (z0 + hh), p0 + Z * (z0 + hh)], 'ahsap', nc)
            if seyirci:
                for m in range(3):
                    u = (m + 0.5 + rs.uniform(-0.15, 0.15)) / 3
                    pp = p0.lerp(p1, u).lerp(q0.lerp(q1, u), 0.45)
                    if rs.random() < 0.8:
                        oturan(y, pp.x, pp.y, z0 + hh, rs.choice(RENKLER), aci=t + math.pi, s=1.05, kol=rs.random() < 0.12)
        # the balustrade: a panelled front, a rail
        if k == 0:
            y.yuz_yon([a + Z * Z0, b + Z * Z0, b + Z * z0, a + Z * z0], AH, nc)   # (the ground gallery's raised floor edge)
        hp = 0.034
        y.yuz_yon([a + nc * 0.003 + Z * z0, b + nc * 0.003 + Z * z0, b + nc * 0.003 + Z * (z0 + hp), a + nc * 0.003 + Z * (z0 + hp)], 'ahsap_acik', nc)
        for m in range(4):   # turned balusters painted on it
            c = a.lerp(b, (m + 0.5) / 4) + nc * 0.0042 + Z * (z0 + hp * 0.5)
            y.yuz_yon([c - e * 0.009 - Z * 0.012, c + e * 0.009 - Z * 0.012, c + e * 0.009 + Z * 0.012, c - e * 0.009 + Z * 0.012], AH, nc)
        kutu3(y, a.lerp(b, 0.5) + nc * 0.001 + Z * (z0 + hp + 0.003), e, nc, Z, L, 0.008, 0.006, 'ahsap_acik', ('+y', '-y', '+z'))
        y.yuz_yon([a + nc * 0.003 + Z * (z0 - 0.014), b + nc * 0.003 + Z * (z0 - 0.014), b + nc * 0.003 + Z * z0, a + nc * 0.003 + Z * z0], AH, nc) if k else None
        y.yuz_yon([a + Z * (z0 - 0.014), b + Z * (z0 - 0.014), b + nc * 0.003 + Z * (z0 - 0.014), a + nc * 0.003 + Z * (z0 - 0.014)], AH, -Z) if k else None
    # the gallery's head beam under the roof
    a, b = P(RI, i + 1), P(RI, i)
    _, _, L, e, nc = eksen(a, b)
    y.yuz_yon([a + nc * 0.003 + Z * (ZE - 0.02), b + nc * 0.003 + Z * (ZE - 0.02), b + nc * 0.003 + Z * ZE, a + nc * 0.003 + Z * ZE], AH, nc)
    y.yuz_yon([a + Z * (ZE - 0.02), b + Z * (ZE - 0.02), b + nc * 0.003 + Z * (ZE - 0.02), a + nc * 0.003 + Z * (ZE - 0.02)], AH, -Z)
# gallery posts at the inner vertices, the end walls against the tiring house
for i in range(N):
    if 2 < i < 7: continue
    cubuk(y, P(RI + 0.004, i, Z0), P(RI + 0.004, i, ZE), 0.012, AH)
for i, s in ((2, -1), (7, 1)):
    a, b = P(RI, i), P(RB, i)
    t = T0 + TAU * i / N
    duz_duvar(y, a if s < 0 else b, b if s < 0 else a, Z0, ZE, 'siva_krem')

# ---------------------------------------------------------------- the yard and the groundlings
y.bolum('Avlu ve ayakta seyirciler')
donel(y, (0, 0), [(RI, Z0 + 0.0015), (RI * 0.66, Z0 + 0.0015), (RI * 0.33, Z0 + 0.0015), (0.0, Z0 + 0.0015)], 'toprak', n=N, kat=T0)
YF = RI * math.sin(math.radians(45))      # the frons scenae (chord between the stage facets)
SX, SY0 = 0.28, 0.07                      # the stage: half width, front edge
ZS = Z0 + 0.065
for k in range(80):
    rr = 0.14 + 0.4 * math.sqrt(rs.random())
    tt = rs.uniform(0, TAU)
    x, yy = rr * math.cos(tt), rr * math.sin(tt)
    if abs(x) < SX + 0.04 and yy > SY0 - 0.04: continue
    if x * x + yy * yy > (RI - 0.04) ** 2: continue
    insan(y, x, yy, Z0 + 0.0015, rs.choice(RENKLER), 1.05, aci=math.atan2(SY0 + 0.1 - yy, -x) + rs.uniform(-0.4, 0.4),
          sapka=rs.choice((None, 'koyu', 'kece')), kol=1.0 if rs.random() < 0.15 else 0.0)

# ---------------------------------------------------------------- the stage, the heavens, the frons scenae
y.bolum('Sahne, cennet sayvanı, sahne arkası')
# the stage platform
kutu(y, V(-SX, SY0, Z0), X, 2 * SX, YF - SY0, ZS - Z0, 'ahsap', 'onsagsol')
y.yuz_yon([V(-SX, SY0, ZS), V(SX, SY0, ZS), V(SX, YF, ZS), V(-SX, YF, ZS)], 'ahsap_acik', Z)
for k in range(5):   # marbled panels round the stage front
    x0 = -SX + 0.02 + k * (2 * SX - 0.04) / 5
    y.yuz_yon([V(x0 + 0.01, SY0 - 0.0015, Z0 + 0.01), V(x0 + (2 * SX - 0.04) / 5 - 0.01, SY0 - 0.0015, Z0 + 0.01),
               V(x0 + (2 * SX - 0.04) / 5 - 0.01, SY0 - 0.0015, ZS - 0.012), V(x0 + 0.01, SY0 - 0.0015, ZS - 0.012)], 'mermer', -Y)
silme(y, [V(SX, YF), V(SX, SY0), V(-SX, SY0), V(-SX, YF)], ZS - 0.006, 0.008, 0.005, 'ahsap_koyu', 'duz', kapali=False)
y.yuz_yon([V(-0.04, 0.3, ZS + 0.0008), V(0.04, 0.3, ZS + 0.0008), V(0.04, 0.36, ZS + 0.0008), V(-0.04, 0.36, ZS + 0.0008)], 'koyu', Z)   # the trap
# the players
insan(y, -0.08, 0.16, ZS, 'boya_kirmizi', 1.25, aci=-0.6, sapka='altin', kol=1.0)      # a king
insan(y, 0.1, 0.18, ZS, 'koyu', 1.2, aci=math.pi + 0.5, kol=1.0)                     # Hamlet
cubuk(y, V(0.09, 0.165, ZS + 0.04), V(0.03, 0.15, ZS + 0.055), 0.003, 'demir')
insan(y, 0.0, 0.34, ZS, 'boya_yesil', 1.15, aci=-math.pi / 2, sapka='kece')
# the heavens: two great painted pillars and the gabled roof over the stage, running back into the hut
ZH = ZE - 0.01
PY = 0.25                                 # the pillars
HXW = 0.2                                 # the heavens: half width
for sx in (-1, 1):
    kutu_merkez(y, (sx * (HXW - 0.035), PY), 0.05, 0.05, 0.03, 'mermer', z0=ZS)
    sutun(y, sx * (HXW - 0.035), PY, ZS + 0.03, ZH - 0.03, 0.019, 'mermer', 'korint', bas_key='altin', yiv=12)
kutu3(y, V(0, PY, ZH - 0.015), X, Y, Z, 2 * HXW + 0.03, 0.03, 0.03, 'ahsap_koyu', ('+x', '-x', '+y', '-y', '-z'))
y.yuz_yon([V(-HXW + 0.03, PY - 0.015 - 0.0015, ZH - 0.026), V(HXW - 0.03, PY - 0.015 - 0.0015, ZH - 0.026), V(HXW - 0.03, PY - 0.015 - 0.0015, ZH - 0.006),
           V(-HXW + 0.03, PY - 0.015 - 0.0015, ZH - 0.006)], 'altin', -Y)
for k in range(7):
    c = V(-0.135 + k * 0.045, PY - 0.015 - 0.0025, ZH - 0.016)
    y.yuz_yon([c - X * 0.006, c - Z * 0.006, c + X * 0.006, c + Z * 0.006], 'boya_kirmizi', -Y)
HY0, HY1 = PY - 0.03, 0.68
zr_ = cati_besik(y, -HXW, HXW, HY0, HY1, ZH, 0.17, 0.025, 'saz', mahya='saz_koyu', kalinlik=0.014, alt_key='ahsap_koyu',
                 ucluk_key=SIVA, alinlik_key='ahsap_koyu', nr=4, ns=6)
# thatch on the heavens' roof: course lines along the slopes and straw strokes down them (a hair above the roof)
_rg = __import__('random').Random(7)
_b = HXW + 0.025
_zf = lambda d: ZH + 0.17 * (1 - d / _b)
for sx in (-1, 1):
    nrm = V(sx * 0.17, 0, _b).normalized()
    off = nrm * 0.0016
    Pq = lambda d, yy: V(sx * d, yy, _zf(d)) + off
    for d in (0.06, 0.12, 0.18):   # course lines
        y.yuz_yon([Pq(d - 0.002, HY0 - 0.02), Pq(d - 0.002, HY1), Pq(d + 0.002, HY1), Pq(d + 0.002, HY0 - 0.02)], 'saz_koyu', nrm)
    for k in range(70):
        yy = _rg.uniform(HY0 - 0.015, HY1 - 0.01)
        d0, d1 = _rg.uniform(0.012, 0.09), _rg.uniform(0.11, 0.215)
        w = _rg.uniform(0.0015, 0.0025)
        y.yuz_yon([Pq(d0, yy - w), Pq(d1, yy - w), Pq(d1, yy + w), Pq(d0, yy + w)], 'saz_koyu', nrm)
# the painted heavens under the roof (a starry sky, seen from the yard) and the front gable's framing
y.yuz_yon([V(-HXW, HY0, ZH - 0.0005), V(HXW, HY0, ZH - 0.0005), V(HXW, YF, ZH - 0.0005), V(-HXW, YF, ZH - 0.0005)], 'lacivert', -Z)
cerceve_serit(V(-HXW + 0.03, HY0), V(HXW - 0.03, HY0), ZH, ZH + 0.05)
y.oculus(V(0, HY0 - 0.0005, ZH + 0.1), X, -Y, 0.03, 'altin', 'ahsap_koyu', f=0.006, k=14)
# the frons scenae: doors and the discovery space below, the lords' rooms above, a painted frieze
fa, fb = V(-YF, YF), V(YF, YF)
NB = 7
ZF1 = ZS + 0.16
ZT = ZE + 0.03
for kk in range(NB):
    p, q = fa.lerp(fb, kk / NB), fa.lerp(fb, (kk + 1) / NB)
    duz_duvar(y, p, q, Z0, ZS, 'ahsap')
    if kk == 3:
        y.kemerli(p, q, ZS, ZF1 - ZS, ('ahsap', 'ahsap_koyu', 'altin', 'boya_kirmizi'), v0=0.0, en=0.74, ust=0.016, derin=0.03, k_say=8, sivri=0,
                  cerceve=(0.006, 'altin'))
    elif kk in (1, 5):
        y.kemerli(p, q, ZS, ZF1 - ZS, ('ahsap', 'ahsap_koyu', 'altin', 'ahsap_koyu'), v0=0.0, en=0.5, ust=0.03, derin=0.016, k_say=6, sivri=0,
                  cerceve=(0.005, 'altin'))
    else:
        duz_duvar(y, p, q, ZS, ZF1, 'ahsap')
        m = (p + q) / 2 + V(0, -0.0015) + Z * (ZS + (ZF1 - ZS) * 0.5)
        y.yuz_yon([m - X * 0.03 - Z * 0.05, m + X * 0.03 - Z * 0.05, m + X * 0.03 + Z * 0.05, m - X * 0.03 + Z * 0.05], 'mermer', -Y)
        y.yuz_yon([m - X * 0.014 - V(0, 0.001), m - Z * 0.03 - V(0, 0.001), m + X * 0.014 - V(0, 0.001), m + Z * 0.03 - V(0, 0.001)], 'boya_kirmizi', -Y)
    y.kemerli(p, q, ZF1, ZE - 0.025 - ZF1, ('ahsap', 'ahsap_koyu', 'altin', 'koyu'), v0=0.0, en=0.62, ust=0.012, derin=0.03, k_say=6, sivri=0,
              korkuluk=0.03, cerceve=(0.004, 'altin'))
    duz_duvar(y, p, q, ZE - 0.025, ZT, 'boya_kirmizi')
for kk in range(NB + 1):   # marbled pilasters between the bays
    p = fa.lerp(fb, kk / NB)
    kutu3(y, p + V(0, -0.005) + Z * ((ZS + ZT) / 2), X, Y, Z, 0.014, 0.01, ZT - ZS, 'mermer', ('+x', '-x', '-y', '+z'))
silme(y, [fa, fb], ZF1 - 0.004, 0.008, 0.008, 'altin', 'duz', kapali=False)
silme(y, [fa, fb], ZT - 0.004, 0.01, 0.012, 'ahsap_koyu', 'tac', kapali=False)
for kk in range(NB):   # gilded panels in the frieze
    c = fa.lerp(fb, (kk + 0.5) / NB) + V(0, -0.0015) + Z * (ZE + 0.003)
    y.yuz_yon([c - X * 0.03 - Z * 0.008, c + X * 0.03 - Z * 0.008, c + X * 0.03 + Z * 0.008, c - X * 0.03 + Z * 0.008], 'altin', -Y)
# musicians in the gallery over the stage
for x in (-0.02, 0.03):
    oturan(y, x, YF + 0.015, ZF1, 'boya_kirmizi' if x < 0 else 'koyu', aci=-math.pi / 2, s=1.1)
# the tiring house's roof deck between the frons and the ring
arc = [P(RIE, i) for i in range(2, 8)]
y.yuz_yon([V(p.x, p.y, ZT) for p in [fb] + arc[1:-1] + [fa]], 'ahsap', Z)

# ---------------------------------------------------------------- the hut and the flag
y.bolum('Kulübe ve sancak')
HX, HY, HW = 0.0, 0.56, 0.12
zh0 = ZH + 0.1
hk = dikdortgen(HX - HW / 2, HX + HW / 2, HY - HW / 2, HY + HW / 2)
for i in range(4):
    a, b = hk[i], hk[(i + 1) % 4]
    acs = acikli_duvar(y, a, b, zh0, ZH + 0.3, [(0.5, 0.04, 0.12, 0.17)], (SIVA, AH, 'ahsap_acik', 'cam'), derin=0.006, pay=0.0)
    L = (b - a).length
    _, _, _, e, nc = eksen(a, b)
    for u in (0.12, 0.88):
        cubuk3(y, a + e * (u * L) + nc * 0.003 + Z * (ZH + 0.21), a + e * (u * L) + nc * 0.003 + Z * (ZH + 0.3), 0.006, AH, nc, 0.003)
    y.yuz_yon([a + nc * 0.0015 + Z * (ZH + 0.3 - 0.006), b + nc * 0.0015 + Z * (ZH + 0.3 - 0.006), b + nc * 0.0015 + Z * (ZH + 0.3), a + nc * 0.0015 + Z * (ZH + 0.3)], AH, nc)
zt_h = cati_kirma(y, HX - HW / 2, HX + HW / 2, HY - HW / 2, HY + HW / 2, ZH + 0.3, 0.1, 0.018, 'kiremit', mahya='kiremit2', kalinlik=0.008,
                  alt_key='ahsap_koyu', ns=2, nr=3, mahya_en=0.008)
sancak(y, HX, HY, zt_h - 0.01, boy=0.2, en=0.15, yuk=0.09, aci=math.pi * 0.85, direk_key='ahsap')

# ---------------------------------------------------------------- stair turrets
y.bolum('Merdiven kuleleri')
for i in (12, 16):
    t = ac(i)
    c = V(math.cos(t), math.sin(t)) * (RO + 0.005)
    hk6 = cokgen((c.x, c.y), 0.085, 6, t + math.pi / 6)
    for j in range(6):
        a, b = hk6[j], hk6[(j + 1) % 6]
        m = (a + b) / 2
        if (m - c).dot(V(math.cos(t), math.sin(t))) < -0.03:   # the sides inside the ring wall
            continue
        for k, (z0, z1) in enumerate(((ZG, ZK[1] + 0.03), (ZK[1] + 0.03, ZE + 0.03))):
            L = (b - a).length
            if k == 0 and abs((m - c).normalized().dot(V(math.cos(t), math.sin(t)))) > 0.9:
                dikdortgen_acik(y, a, b, z0, z1 - z0, 0.3, 0.7, 0.0, (z1 - z0) * 0.72, (SIVA, AH, 'ahsap_acik', 'ahsap'), derin=0.012, cerceve=(0.005, AH))
                continue
            acikli_duvar(y, a, b, z0, z1, [(0.5, 0.022, (z1 - z0) * 0.45, (z1 - z0) * 0.75)], (SIVA, AH, 'ahsap_acik', 'cam'), derin=0.006, pay=0.0)
            cerceve_serit(a, b, z0, z1, (0.5 - 0.011 / L, 0.5 + 0.011 / L, (z1 - z0) * 0.45, (z1 - z0) * 0.75))
        cubuk(y, V(a.x, a.y, ZG), V(a.x, a.y, ZE + 0.03), 0.008, AH)
    donel(y, (c.x, c.y), [(0.087, 0.0), (0.087, ZG), (0.085, ZG + 0.002)], 'tugla', n=6, kat=t + math.pi / 6)
    # the thatched cone in three courses (each butt a step proud of the one below)
    pr = [(0.11, ZE + 0.01), (0.11, ZE + 0.03)]
    for j in (1, 2):
        tt = j / 3
        br, bz = 0.11 - 0.11 * tt + 0.84 * 0.006 * (j - 1), ZE + 0.03 + 0.17 * tt + 0.54 * 0.006 * (j - 1)
        pr += [(br, bz), (br + 0.84 * 0.006, bz + 0.54 * 0.006)]
    pr.append((0.0, ZE + 0.2))
    donel(y, (c.x, c.y), pr, 'saz', n=6, kat=t + math.pi / 6)
    y.yuz_yon([V(p.x, p.y, ZE + 0.01) for p in cokgen((c.x, c.y), 0.11, 6, t + math.pi / 6)], 'ahsap_koyu', -Z)
    y.prizma((c.x, c.y), 0.004, ZE + 0.19, ZE + 0.24, 'ahsap', n=4)
    kure(y, (c.x, c.y, ZE + 0.245), 0.008, 'altin', n=6, kat=3)

# ---------------------------------------------------------------- Bankside: houses, trees, playgoers coming
y.bolum('Bankside: evler, ağaçlar, gelenler')
ev(y, -0.92, 0.82, Z0, 0.26, 0.16, 0.15, aci=-0.6, cati='kiremit', tohum=1)
ev(y, 0.94, 0.78, Z0, 0.24, 0.15, 0.14, aci=0.7, cati='saz', tohum=2)
ev(y, -0.98, -0.72, Z0, 0.2, 0.13, 0.13, aci=0.15, cati='saz', tohum=3)
for (x, yy) in ((0.92, -0.6), (1.02, -0.38), (-1.02, 0.35), (-0.95, 0.15), (0.98, 0.3), (0.3, 0.98), (-0.4, 1.0), (1.05, 1.02)):
    agac(y, x, yy, Z0, boy=0.14)
for k, (x, yy) in enumerate(((0.02, -0.9), (-0.03, -0.86), (0.04, -0.83), (-0.25, -0.82), (0.3, -0.81), (0.45, -0.84), (-0.5, -0.83))):
    insan(y, x, yy, Z0, RENKLER[k % len(RENKLER)], 1.0, aci=math.pi / 2 + (k % 3 - 1) * 0.4, sapka='koyu' if k % 2 else None)
# a paling fence round the back gardens, a well
for (a, b) in (((-1.1, 0.5), (-1.1, 1.08)), ((-1.1, 1.08), (1.1, 1.08)), ((1.1, 1.08), (1.1, 0.45))):
    a, b, L, e, nc = eksen(a, b)
    n = int(L / 0.03)
    for k in range(n + 1):
        p = a.lerp(b, k / n)
        y.prizma((p.x, p.y), 0.003, Z0, Z0 + 0.03, 'ahsap', n=4)
    for zz in (Z0 + 0.01, Z0 + 0.024):
        cubuk(y, a + Z * zz, b + Z * zz, 0.003, 'ahsap_koyu')
y.prizma((0.7, 0.98), 0.025, Z0, Z0 + 0.022, 'granit', n=10)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0205) for p in cokgen((0.7, 0.98), 0.019, 10)], 'su', Z)
for s_ in (-1, 1):
    cubuk(y, V(0.7 + s_ * 0.022, 0.98, Z0 + 0.02), V(0.7 + s_ * 0.022, 0.98, Z0 + 0.08), 0.004, 'ahsap')
cubuk(y, V(0.67, 0.98, Z0 + 0.075), V(0.73, 0.98, Z0 + 0.075), 0.004, 'ahsap')
donel(y, (0.7, 0.98), [(0.034, Z0 + 0.08), (0.0, Z0 + 0.11)], 'saz', n=6)
# a playbill post by the door
y.prizma((0.18, -0.86), 0.005, Z0, Z0 + 0.09, 'ahsap_koyu', n=5)
levha(y, [V(0.16, -0.866, Z0 + 0.05), V(0.2, -0.866, Z0 + 0.05), V(0.2, -0.866, Z0 + 0.085), V(0.16, -0.866, Z0 + 0.085)], 'kece', -Y)

calistir(y, 'lm_globe')
