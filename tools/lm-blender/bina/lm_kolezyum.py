# The Colosseum (lm_kolezyum): an oval travertine amphitheatre of four storeys - three arcaded tiers with Tuscan,
# Ionic and Corinthian engaged half-columns and deep barrel-vaulted arches, a windowed attic with corbels, shields
# and velarium masts - stepped seating with vomitoria and radial stairs, a podium wall, a sand arena with part of the
# hypogeum laid open. The south side is ruined down to the second tier, the inner ring and a brick buttress showing.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi(tohum=11)

# ---------------------------------------------------------------- dimensions
A, B = 1.14, 0.95          # outer ellipse half-axes (wall face)
N = 48                     # bays round
Dk = 0.07                  # outer shell (arch tunnel) depth
G = 0.13                   # inner ring (top of the seating) inward offset
Z0 = 0.05                  # ground floor on the plinth
TIER = [0.17, 0.16, 0.155]
ATTIC = 0.15
z1 = Z0 + TIER[0]; z2 = z1 + TIER[1]; z3 = z2 + TIER[2]; ZT = z3 + ATTIC
ZSEAT = ZT - 0.11          # top of the seating (floor of the top portico)
HP = 0.055                 # portico columns
ZPC = ZSEAT + HP + 0.012   # portico beam top (roof eave)
S_T, S_POD = 0.60, 0.635   # podium terrace, podium wall (inward offsets)
Z_FLOOR, Z_POD = 0.065, 0.135
ENT = 0.034                # entablature height on each tier
R_COL = 0.0105


def elips_noktalari(a, b, n):
    """n points at equal arc length, CCW, a bay boundary half a bay off the front (-y) so a bay faces south"""
    M = 4000
    pts = [(a * math.cos(-math.pi / 2 + TAU * i / M), b * math.sin(-math.pi / 2 + TAU * i / M)) for i in range(M + 1)]
    L = [0]
    for i in range(M):
        L.append(L[-1] + math.dist(pts[i], pts[i + 1]))
    out, j = [], 0
    for k in range(n):
        s = L[-1] * (k + 0.5) / n
        while L[j + 1] < s: j += 1
        f = (s - L[j]) / (L[j + 1] - L[j])
        out.append(V(pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f))
    return out


P = elips_noktalari(A, B, N)
NRM = [V(p.x / A ** 2, p.y / B ** 2).normalized() for p in P]
TAN = [V(-n.y, n.x) for n in NRM]          # CCW tangent


def R(s, i, z=0.0):
    """a point s inward of the wall face at bay boundary i, height z"""
    p = P[i % N] - NRM[i % N] * s
    return V(p.x, p.y, z)


def ust(pts, key): y.yuz_yon(pts, key, Z)
def alt(pts, key): y.yuz_yon(pts, key, -Z)


def ic_yon(i, j):   # inward direction of a bay
    m = (NRM[i % N] + NRM[j % N]); return -m.normalized()


# ---------------------------------------------------------------- the ruin: which bays still stand how high
def bay_aci(i):
    m = (P[i] + P[(i + 1) % N]) / 2
    return math.degrees(math.atan2(m.y, m.x))


DURUM = []
for i in range(N):
    a = bay_aci(i)
    if -124 <= a <= -60: DURUM.append('yikik')          # outer ring down to the 2nd tier
    elif -139 <= a < -124: DURUM.append('t3')           # a stub of the 3rd tier
    elif -60 < a <= -50: DURUM.append('payanda')        # the brick buttress (Stern's) at the east end
    else: DURUM.append('tam')
D = lambda i: DURUM[i % N]
has_t3 = lambda i: D(i) in ('tam', 't3')
has_at = lambda i: D(i) == 'tam'


def kosular(kosul):
    """runs of consecutive bays meeting kosul: [(start, length)], or None if every bay does"""
    ok = [kosul(i) for i in range(N)]
    if all(ok): return None
    s0 = ok.index(False)
    out = []; i = 0
    while i < N:
        k = (s0 + i) % N
        if ok[k]:
            L = 0
            while i < N and ok[(s0 + i) % N]: L += 1; i += 1
            out.append((k, L))
        else:
            i += 1
    return out


def halka_silme(kosul, z, h, c, key='kum_acik', profil='duz'):
    runs = kosular(kosul)
    if runs is None:
        silme(y, [V(p.x, p.y) for p in P], z, h, c, key, profil); return
    for k, L in runs:
        silme(y, [V(P[(k + j) % N].x, P[(k + j) % N].y) for j in range(L + 1)], z, h, c, key, profil, kapali=False)


# ---------------------------------------------------------------- engaged half-columns
def yarim_donel(c, n, profil, key, m=6):
    e = n.cross(Z)
    # a little more than a half circle: the ends tuck behind the wall (the column stands on the corner where two bay
    # walls meet at an angle; a plain half left a slit through which its open back showed)
    ue = 0.3
    A = [-ue + (math.pi + 2 * ue) * k / m for k in range(m + 1)]
    rings = [[V(c.x, c.y, zz) + e * (r * math.cos(t)) + n * (r * math.sin(t)) for t in A] for r, zz in profil]
    for a, b in zip(rings, rings[1:]):
        y.serit(a, b, key, kapali=False)
    # (no top cap: every ring here is covered by the piece above it - shaft, capital, abacus)


ICSIZ = 'arkasagsolust'   # a box centred on the wall face: its 'on' side is inside the wall


def yarim_sutun(c, n, za, zb, r, tur, key='kum_acik'):
    """a half column standing on the wall face at c (n out of the wall) from za to zb (top of the capital)"""
    H = zb - za
    e = n.cross(Z)
    hb = H * 0.07
    yarim_donel(c, n, [(r * 1.4, za), (r * 1.0, za + hb)], key, m=4)   # (a bevelled plinth: one ring, the file is at its limit)
    hc = H * (0.08 if tur == 'toskan' else 0.1 if tur == 'iyon' else 0.15)
    zc = zb - hc
    yarim_donel(c, n, [(r * 1.0, za + hb), (r * 0.9, zc)], key, m=4)   # (m as base and capital: the rings meet edge to edge)
    if tur == 'toskan':
        yarim_donel(c, n, [(r * 0.9, zc), (r * 1.0, zc + hc * 0.25), (r * 1.3, zc + hc * 0.6)], key, m=4)
        kutu_merkez(y, c, r * 2.8, r * 2.8, hc * 0.4, key, z0=zc + hc * 0.6, aci=math.atan2(e.y, e.x), yuzler=ICSIZ)
    elif tur == 'iyon':
        yarim_donel(c, n, [(r * 0.9, zc), (r * 1.15, zc + hc * 0.45)], key, m=4)
        kutu_merkez(y, c, r * 2.6, r * 2.4, hc * 0.25, key, z0=zc + hc * 0.45, aci=math.atan2(e.y, e.x), yuzler=ICSIZ)
        for sg in (-1, 1):   # volutes: short rolls seen end-on from the front
            p = V(c.x, c.y, zc + hc * 0.42) + e * (sg * r * 1.2)
            boru(y, [p, p + n * (r * 1.25)], r * 0.42, key, n=4)
        kutu_merkez(y, c, r * 2.9, r * 2.9, hc * 0.3, key, z0=zc + hc * 0.7, aci=math.atan2(e.y, e.x), yuzler=ICSIZ)
    else:   # korint: a bell with two rows of leaves
        yarim_donel(c, n, [(r * 0.9, zc), (r * 1.1, zc + hc * 0.72), (r * 1.3, zc + hc * 0.82)], key, m=4)
        for row, (h0, h1, k0) in enumerate(((0.0, 0.42, 0.5), (0.22, 0.68, 0.0))):
            for k in range(4 if row == 0 else 5):
                a = math.pi * (k + k0) / 4 if row == 0 else math.pi * k / 4
                d = e * math.cos(a) + n * math.sin(a)
                if d.dot(n) < 0.05: continue
                t = Z.cross(d)
                p0 = V(c.x, c.y) + d * (r * 0.92)
                w = r * 0.42; tip = p0 + d * (r * 0.32)
                y.yuz_yon([p0 - t * w + Z * (zc + hc * h0), p0 + t * w + Z * (zc + hc * h0), tip + t * w * 0.7 + Z * (zc + hc * h1),
                           tip - t * w * 0.7 + Z * (zc + hc * h1)], key, d)
        kutu_merkez(y, c, r * 3.0, r * 3.0, hc * 0.18, key, z0=zc + hc * 0.82, aci=math.atan2(e.y, e.x), yuzler=ICSIZ)


def pilastr(c, n, za, zb, w, key='kum_acik'):
    """a flat Corinthian pilaster on the wall face (attic)"""
    e = n.cross(Z); aci = math.atan2(e.y, e.x)
    kutu_merkez(y, c, w * 1.25, 0.014, 0.008, key, z0=za, aci=aci, yuzler=ICSIZ)
    kutu_merkez(y, c, w, 0.01, zb - za - 0.02, key, z0=za + 0.008, aci=aci, yuzler=ICSIZ)
    kutu_merkez(y, c, w * 1.3, 0.015, 0.011, key, z0=zb - 0.011, aci=aci, yuzler=ICSIZ)


# ---------------------------------------------------------------- plinth, paving, bollards
y.bolum('zemin')
def halka(s, z): return [R(s, i, z) for i in range(N)]
for s0, s1, zz, kk in ((-0.17, -0.065, 0.02, 'zemin'), (-0.065, -0.032, 0.035, 'kirec'), (-0.032, 0.0, Z0, 'kirec')):
    for i in range(N):
        ust([R(s0, i, zz), R(s0, i + 1, zz), R(s1, i + 1, zz), R(s1, i, zz)], kk)
    zb_ = 0.0 if s0 < -0.1 else (0.02 if s0 < -0.05 else 0.035)
    for i in range(N):
        y.yuz_yon([R(s0, i, zb_), R(s0, i + 1, zb_), R(s0, i + 1, zz), R(s0, i, zz)], 'kirec', NRM[i] + NRM[(i + 1) % N])
# travertine bollards (cippi) round the paving
for i in range(0, N, 2):
    p = R(-0.135, i)
    kutu_merkez(y, p, 0.016, 0.016, 0.045, 'kirec', z0=0.02, aci=math.atan2(TAN[i].y, TAN[i].x))

# ---------------------------------------------------------------- the outer arcades
y.bolum('dis kemerler')
TAS4 = ('kum', 'kum_koyu', 'kum_acik', 'kum_koyu')


def kemer_kat(i, za, H, v0, ust_, korkuluk, ic_en=0.62):
    a, b = P[i], P[(i + 1) % N]
    W, e, nc, L = y.kemerli(a, b, za, H, TAS4, v0=v0, en=0.6, ust=ust_, derin=Dk, k_say=5, korkuluk=korkuluk,
                            cerceve=(0.006, ['kum_acik']))
    # the radial passage glimpsed at the back of the vault
    w = W * 0.6 * ic_en
    hh = (H - ust_ - v0) * 0.78
    o = a - nc * Dk + Z * za
    y.pencere(o, e, nc, W / 2 - w / 2, v0, w, hh, 'koyu', kemer=True, k_say=4)


zs = [Z0, z1, z2]
for t in range(3):
    za, H = zs[t], TIER[t]
    for i in range(N):
        if t == 2 and not has_t3(i): continue
        kemer_kat(i, za, H, 0.0 if t == 0 else 0.024, 0.048 if t == 0 else 0.045, None if t == 0 else 0.022)

# plinth band of tiers 2 and 3 (column pedestals), entablatures
y.bolum('silmeler')
halka_silme(lambda i: True, Z0, 0.012, 0.01, 'kum_acik', 'duz')
for t, (za, H) in enumerate(zip(zs, TIER)):
    kos = (lambda i: True) if t < 2 else has_t3
    zt = za + H
    if t > 0: halka_silme(kos, za, 0.02, 0.013, 'kum_acik', 'kaide')
    halka_silme(kos, zt - ENT, 0.010, 0.016, 'kum_acik', 'duz')
    halka_silme(kos, zt - ENT + 0.010, 0.012, 0.011, 'kum', 'duz')
    halka_silme(kos, zt - ENT + 0.022, 0.012, 0.025, 'kum_acik', 'tac')

y.bolum('yarim sutunlar')
for t, tur in enumerate(('toskan', 'iyon', 'korint')):
    za = zs[t] + (0.0 if t == 0 else 0.02)
    zb = zs[t] + TIER[t] - ENT
    for k in range(N):
        if t == 2 and not (has_t3(k) or has_t3(k - 1)): continue
        yarim_sutun(P[k], NRM[k], za, zb, R_COL, tur)

# ---------------------------------------------------------------- attic
y.bolum('attika')
for i in range(N):
    if not has_at(i): continue
    a, b = P[i], P[(i + 1) % N]
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    if i % 2 == 0:
        dikdortgen_acik(y, a, b, z3, ATTIC, 0.39, 0.61, 0.05, 0.088, ('kum', 'kum_koyu', 'kum_acik', 'koyu'), derin=0.022,
                        cerceve=(0.004, 'kum_acik'))
    else:
        duz_duvar(y, a, b, z3, ZT, 'kum')
        # a gilded bronze shield (clipeus)
        y.oculus(a.lerp(b, 0.5) + Z * (z3 + 0.07), e, nc, 0.016, 'bronz', 'altin', f=0.004, k=10)
    # corbels for the velarium masts
    for u in (0.25, 0.5, 0.75):
        p = a.lerp(b, u)
        kutu(y, V(p.x, p.y, ZT - 0.052) - e * 0.005 + nc * 0.012, e, 0.01, 0.012, 0.012, 'kum_acik', 'onsagsolust')
halka_silme(has_at, z3, 0.022, 0.012, 'kum_acik', 'kaide')
halka_silme(has_at, ZT - 0.036, 0.012, 0.012, 'kum', 'duz')
halka_silme(has_at, ZT - 0.024, 0.024, 0.028, 'kum_acik', 'tac')
for k in range(N):
    if has_at(k) or has_at(k - 1):
        pilastr(P[k], NRM[k], z3 + 0.022, ZT - 0.036, 0.021)
# velarium masts on every other corbel
for i in range(0, N, 2):
    if not has_at(i): continue
    p = P[i].lerp(P[(i + 1) % N], 0.5) + NRM[i] * 0.0
    nn = (NRM[i] + NRM[(i + 1) % N]).normalized()
    c = p + nn * 0.006
    y.prizma((c.x, c.y), 0.0038, ZT - 0.04, ZT + 0.065, 'ahsap', n=6)
# the attic's top and the parapet face inside
for i in range(N):
    if not has_at(i): continue
    ust([R(0, i, ZT), R(0, i + 1, ZT), R(Dk, i + 1, ZT), R(Dk, i, ZT)], 'kum_acik')

# ---------------------------------------------------------------- top portico (inside, over the seating)
y.bolum('ust revak')
for i in range(N):
    if not has_at(i): continue
    j = i + 1
    inw = ic_yon(i, j)
    # back wall (the attic's inner face) with doors
    y.yuz_yon([R(Dk, j, ZSEAT), R(Dk, i, ZSEAT), R(Dk, i, ZT), R(Dk, j, ZT)], 'kum', inw)
    a, b = R(Dk, j), R(Dk, i)
    e = (b - a).normalized()
    y.pencere(V(a.x, a.y, ZSEAT) + inw * 0.0, e, inw, (b - a).length * 0.38, 0.0, (b - a).length * 0.24, 0.042, 'koyu', kemer=True)
    # floor
    ust([R(Dk, i, ZSEAT), R(Dk, j, ZSEAT), R(G, j, ZSEAT), R(G, i, ZSEAT)], 'zemin')
    # roof: tiles above, timber below, the eave
    ro = 0.016
    zr0, zr1 = ZT - 0.02, ZPC
    y.yuz_yon([R(Dk, i, zr0), R(Dk, j, zr0), R(G + ro, j, zr1), R(G + ro, i, zr1)], 'kiremit2', Z + inw * 0.3)
    y.yuz_yon([R(Dk, i, zr0 - 0.006), R(Dk, j, zr0 - 0.006), R(G + ro, j, zr1 - 0.006), R(G + ro, i, zr1 - 0.006)], 'ahsap_koyu', -Z)
    y.yuz_yon([R(G + ro, i, zr1 - 0.006), R(G + ro, j, zr1 - 0.006), R(G + ro, j, zr1), R(G + ro, i, zr1)], 'ahsap', inw)
    # the beam on the columns
    y.yuz_yon([R(G + 0.008, i, ZSEAT + HP), R(G + 0.008, j, ZSEAT + HP), R(G + 0.008, j, ZPC - 0.006), R(G + 0.008, i, ZPC - 0.006)], 'kum_acik', inw)
    alt([R(G - 0.008, i, ZSEAT + HP), R(G - 0.008, j, ZSEAT + HP), R(G + 0.008, j, ZSEAT + HP), R(G + 0.008, i, ZSEAT + HP)], 'kum_acik')
    # columns
    for u in (0.0, 0.5):
        c = R(G, i).lerp(R(G, j), u)
        y.prizma((c.x, c.y), 0.0062, ZSEAT + 0.006, ZSEAT + HP - 0.006, 'mermer', n=6, ust=False)
        kutu_merkez(y, c, 0.017, 0.017, 0.006, 'mermer', z0=ZSEAT + HP - 0.006, yuzler='onarkasagsol')
    if not has_at(j):   # the last column of the run
        c = R(G, j)
        y.prizma((c.x, c.y), 0.0062, ZSEAT + 0.006, ZSEAT + HP - 0.006, 'mermer', n=8, ust=False)
        kutu_merkez(y, c, 0.017, 0.017, 0.006, 'mermer', z0=ZSEAT + HP - 0.006, yuzler='onarkasagsol')

# ---------------------------------------------------------------- the ruined side: caps, the inner ring, buttress
y.bolum('yikik yan')
rng = y.rng
for i in range(N):
    d = D(i)
    if d == 'tam': continue
    j = i + 1
    zc = z3 if d == 't3' else z2
    if d in ('yikik', 't3'):
        ust([R(0, i, zc), R(0, j, zc), R(Dk, j, zc), R(Dk, i, zc)], 'kum')
    if d == 't3':   # (the buttress bay has its own inner faces: a full-height panel here stood free above its low steps)
        y.yuz_yon([R(Dk, j, z2), R(Dk, i, z2), R(Dk, i, z3), R(Dk, j, z3)], 'kum_koyu', ic_yon(i, j))
    ust([R(Dk, i, z2), R(Dk, j, z2), R(G, j, z2), R(G, i, z2)], 'zemin')
    # the inner ring: an arcade facing out, a low parapet on its top
    y.kemerli(R(G, i), R(G, j), z2, ZSEAT + 0.02 - z2, ('kum', 'kum_koyu', 'kum_acik', 'koyu'), v0=0.0, en=0.5, ust=0.05,
              derin=0.03, k_say=6)
    ust([R(G, i, ZSEAT + 0.02), R(G, j, ZSEAT + 0.02), R(G + 0.012, j, ZSEAT + 0.02), R(G + 0.012, i, ZSEAT + 0.02)], 'kum_acik')
    y.yuz_yon([R(G + 0.012, j, ZSEAT), R(G + 0.012, i, ZSEAT), R(G + 0.012, i, ZSEAT + 0.02), R(G + 0.012, j, ZSEAT + 0.02)], 'kum', ic_yon(i, j))
    # broken stone lying on the cut
    if d == 'yikik':
        for _ in range(2):
            u = rng.uniform(0.15, 0.85); s = rng.uniform(0.01, Dk - 0.02)
            p = R(s, i).lerp(R(s, j), u)
            kutu_merkez(y, p, rng.uniform(0.02, 0.04), rng.uniform(0.018, 0.03), rng.uniform(0.01, 0.022), 'kum_koyu', z0=zc,
                        aci=rng.uniform(0, math.pi))
    if d == 'payanda':
        # the brick buttress at the end of the standing ring: three sloping steps (as Valadier's / Stern's)
        lo, hi = (i, j) if has_at(j) else (j, i)
        nd = NRM[i] + NRM[j % N]
        BAS = [(0.0, 0.36, z2 + 0.03, z2 + 0.075), (0.36, 0.7, z3 - 0.01, z3 + 0.04), (0.7, 1.0, ZT - 0.05, ZT)]
        for u0, u1, za_, zb_ in BAS:
            q = lambda s_, u, zz: R(s_, lo, zz).lerp(R(s_, hi, zz), u)
            so = -0.008
            y.yuz_yon([q(so, u0, z2), q(so, u1, z2), q(so, u1, zb_), q(so, u0, za_)], 'tugla_koyu', nd)
            y.yuz_yon([q(Dk, u0, z2), q(Dk, u1, z2), q(Dk, u1, zb_), q(Dk, u0, za_)], 'tugla_koyu', -nd)
            y.yuz_yon([q(so, u0, za_), q(so, u1, zb_), q(Dk, u1, zb_), q(Dk, u0, za_)], 'kum', Z)
            y.yuz_yon([q(so, u0, z2), q(Dk, u0, z2), q(Dk, u0, za_), q(so, u0, za_)], 'tugla_koyu', P[lo] - P[hi])
        # the bit standing proud of the facade at the end against the full ring
        y.yuz_yon([R(so, hi, z2), R(0, hi, z2), R(0, hi, ZT), R(so, hi, ZT)], 'tugla_koyu', P[hi] - P[lo])

# end faces where the standing height changes from one bay to the next (radial sections)
BOLGE = {
    'k3': [(0, z2), (Dk, z2), (Dk, z3), (0, z3)],
    'kA': [(0, z3), (Dk, z3), (Dk, ZT), (0, ZT)],
    'gal': [(Dk, z2), (G, z2), (G, ZSEAT + HP), (G + 0.008, ZSEAT + HP), (G + 0.008, ZPC - 0.006), (G + 0.016, ZPC - 0.006), (G + 0.016, ZPC), (Dk, ZT - 0.02)],   # (closes the eave's end too)
}
def bolgeler(d, sinir_tam_yanda):
    if d == 'tam': return {'k3', 'kA', 'gal'}
    if d == 't3': return {'k3'}
    if d == 'payanda': return {'k3', 'kA'} if sinir_tam_yanda else set()
    return set()
for k in range(N):
    a, b = D(k - 1), D(k)
    if a == b: continue
    sa = bolgeler(a, b == 'tam'); sb = bolgeler(b, a == 'tam')
    for ad in sa - sb:
        y.yuz_yon([R(s, k, zz) for s, zz in BOLGE[ad]], 'kum_koyu' if ad == 'gal' else 'kum', TAN[k])
    for ad in sb - sa:
        y.yuz_yon([R(s, k, zz) for s, zz in BOLGE[ad]], 'kum_koyu' if ad == 'gal' else 'kum', -TAN[k])
# fallen blocks at the foot of the ruin
for i in range(N):
    if D(i) != 'yikik' or i % 2: continue
    for _ in range(2):
        p = R(rng.uniform(-0.14, -0.07), i).lerp(R(rng.uniform(-0.14, -0.07), i + 1), rng.uniform(0, 1))
        kutu_merkez(y, p, rng.uniform(0.02, 0.035), rng.uniform(0.015, 0.03), rng.uniform(0.012, 0.022), 'kum_koyu', z0=0.02,
                    aci=rng.uniform(0, math.pi))

# ---------------------------------------------------------------- seating
y.bolum('oturma yerleri')
SIRA = [(1, 1, '')] * 4 + [(1, 2.4, 'v'), (1.6, 1, 'w')] + [(1, 1, '')] * 6 + [(1, 2.4, 'v'), (1.6, 1, 'w')] + [(1, 1, '')] * 5
ud = (S_T - G) / sum(r[0] for r in SIRA)
uh = (ZSEAT - Z_POD) / sum(r[1] for r in SIRA)
MERDIVEN = 4      # a radial stair at every 4th bay boundary, a vomitorium in a bay between
ST_W = 0.024
s, z = G, ZSEAT
kutu_alti = False  # did the row above leave a half step on this tread?
for r, (dd, hh, tur) in enumerate(SIRA):
    s1, zn = s + dd * ud, z - hh * uh
    tread = 'zemin' if tur == 'w' else 'kirec'
    for i in range(N):
        j = i + 1
        ust([R(s, i, z), R(s, j, z), R(s1, j, z), R(s1, i, z)], tread)
        inw = ic_yon(i, j)
        if tur == 'v' and i % MERDIVEN == 1:
            dikdortgen_acik(y, R(s1, j), R(s1, i), zn, z - zn, 0.3, 0.7, 0.0, (z - zn) * 0.78,
                            ('kum', 'kum_koyu', 'kum_acik', 'koyu'), derin=0.03, cerceve=(0.004, 'kum_acik'))
        else:
            y.yuz_yon([R(s1, j, zn), R(s1, i, zn), R(s1, i, z), R(s1, j, z)], 'kum' if tur == 'v' else 'kum_koyu', inw)
    # radial stairs (not across the tall walls or the walkways)
    nxt = SIRA[r + 1] if r + 1 < len(SIRA) else None
    for k in range(0, N, MERDIVEN):
        t = TAN[k]; inw = -NRM[k]
        def Q(ss, zz, sg): return R(ss, k, zz) + t * (sg * ST_W / 2)
        if tur == '':
            # the strip over this tread (behind the half step the row above may have left)
            sa = s + (dd * ud / 2 if kutu_alti else 0.0)
            ust([Q(sa, z + 0.0012, -1), Q(sa, z + 0.0012, 1), Q(s1, z + 0.0012, 1), Q(s1, z + 0.0012, -1)], 'mermer')
            if nxt and nxt[2] == '':
                # a half step on the next tread, and the strip on this riser above it
                sb = s1 + nxt[0] * ud / 2; zh = zn + hh * uh / 2
                ust([Q(s1, zh, -1), Q(s1, zh, 1), Q(sb, zh, 1), Q(sb, zh, -1)], 'mermer')
                y.yuz_yon([Q(sb, zn, -1), Q(sb, zn, 1), Q(sb, zh, 1), Q(sb, zh, -1)], 'tas_acik', inw)
    kutu_alti = (tur == '' and nxt is not None and nxt[2] == '')
    s, z = s1, zn

# ---------------------------------------------------------------- podium, boxes, arena
y.bolum('podyum')
for i in range(N):
    j = i + 1; inw = ic_yon(i, j)
    ust([R(S_T, i, Z_POD), R(S_T, j, Z_POD), R(S_POD - 0.009, j, Z_POD), R(S_POD - 0.009, i, Z_POD)], 'mermer')
    # low marble parapet on the podium edge
    y.yuz_yon([R(S_POD - 0.009, j, Z_POD), R(S_POD - 0.009, i, Z_POD), R(S_POD - 0.009, i, Z_POD + 0.016), R(S_POD - 0.009, j, Z_POD + 0.016)], 'mermer', -inw)
    ust([R(S_POD - 0.009, i, Z_POD + 0.016), R(S_POD - 0.009, j, Z_POD + 0.016), R(S_POD, j, Z_POD + 0.016), R(S_POD, i, Z_POD + 0.016)], 'mermer')
    a_ = bay_aci(i)
    if min(abs(a_), abs(abs(a_) - 180)) < 5:   # the gates on the long axis
        dikdortgen_acik(y, R(S_POD, j), R(S_POD, i), Z_FLOOR, Z_POD + 0.016 - Z_FLOOR, 0.22, 0.78, 0.0, 0.058,
                        ('mermer', 'kum_koyu', 'kum_acik', 'ahsap_koyu'), derin=0.02, cerceve=(0.005, 'kum_acik'))
    else:
        y.yuz_yon([R(S_POD, j, Z_FLOOR), R(S_POD, i, Z_FLOOR), R(S_POD, i, Z_POD + 0.016), R(S_POD, j, Z_POD + 0.016)], 'mermer', inw)
# a painted band along the podium face
for i in range(N):
    j = i + 1; inw = ic_yon(i, j)
    a_ = bay_aci(i)
    if min(abs(a_), abs(abs(a_) - 180)) < 5: continue
    y.yuz_yon([R(S_POD + 0.0015, j, Z_FLOOR + 0.03), R(S_POD + 0.0015, i, Z_FLOOR + 0.03), R(S_POD + 0.0015, i, Z_FLOOR + 0.042),
               R(S_POD + 0.0015, j, Z_FLOOR + 0.042)], 'kirmizi', inw)

# the emperor's and the consuls' boxes on the short axis
for yon in (1, -1):
    k = min(range(N), key=lambda q: abs(bay_aci(q) - 90 * yon))
    c0 = (R(S_POD, k) + R(S_POD, k + 1)) / 2
    inw = ic_yon(k, k + 1); t = V(-inw.y, inw.x)
    w, dd = 0.1, 0.06
    o = c0 - inw * dd
    kutu_merkez(y, o + inw * (dd / 2), w, dd, 0.03, 'mermer', z0=Z_POD, aci=math.atan2(t.y, t.x))
    for sg in (-1, 1):
        for f in (0.15, 0.85):
            c = o + inw * (dd * f) + t * (sg * w * 0.42)
            y.prizma((c.x, c.y), 0.0045, Z_POD + 0.03, Z_POD + 0.085, 'mermer', n=8, ust=False)
    kutu_merkez(y, o + inw * (dd / 2), w + 0.012, dd + 0.008, 0.008, 'mermer', z0=Z_POD + 0.085, aci=math.atan2(t.y, t.x))
    kutu_merkez(y, o + inw * (dd / 2), w + 0.004, dd, 0.01, 'boya_kirmizi', z0=Z_POD + 0.093, aci=math.atan2(t.y, t.x))
    # a little gable to the arena
    a1, b1 = o + inw * dd + t * (w / 2 + 0.006), o + inw * dd - t * (w / 2 + 0.006)
    if (b1 - a1).cross(Z).dot(inw) < 0: a1, b1 = b1, a1
    alinlik(y, a1, b1, Z_POD + 0.103, 0.028, dd, 'mermer', cati_key='kiremit', c=0.004)

y.bolum('arena')
HX, HY = 0.3, 0.2          # the arena's central rectangle: timber floor on the south half, the hypogeum open on the north
Z_PIT = Z_FLOOR - 0.06


def isin_kesis(poly, th):
    d = V(math.cos(th), math.sin(th))
    best = None
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        e = b - a
        den = d.x * e.y - d.y * e.x
        if abs(den) < 1e-12: continue
        tt = (a.x * e.y - a.y * e.x) / den
        u = (a.x * d.y - a.y * d.x) / den
        if tt > 0 and -1e-9 <= u <= 1 + 1e-9 and (best is None or tt < best): best = tt
    return d * best


POD = [R(S_POD, i) for i in range(N)]
DIK = [V(HX, -HY), V(HX, HY), V(-HX, HY), V(-HX, -HY)]
acilar = sorted({math.atan2(p.y, p.x) for p in POD} | {math.atan2(p.y, p.x) for p in DIK})
dis_ = [isin_kesis(POD, a) for a in acilar]
ic_ = [isin_kesis(DIK, a) for a in acilar]
for i in range(len(acilar)):
    j = (i + 1) % len(acilar)
    ust([V(ic_[i].x, ic_[i].y, Z_FLOOR), V(ic_[j].x, ic_[j].y, Z_FLOOR), V(dis_[j].x, dis_[j].y, Z_FLOOR), V(dis_[i].x, dis_[i].y, Z_FLOOR)], 'kum_acik')
# the reconstructed timber floor (south half) and its cut edge
ust([V(-HX, -HY, Z_FLOOR), V(HX, -HY, Z_FLOOR), V(HX, 0, Z_FLOOR), V(-HX, 0, Z_FLOOR)], 'ahsap_acik')
y.yuz_yon([V(-HX, 0, Z_FLOOR - 0.008), V(HX, 0, Z_FLOOR - 0.008), V(HX, 0, Z_FLOOR), V(-HX, 0, Z_FLOOR)], 'ahsap', Y)
y.yuz_yon([V(-HX, 0, Z_PIT), V(HX, 0, Z_PIT), V(HX, 0, Z_FLOOR - 0.008), V(-HX, 0, Z_FLOOR - 0.008)], 'tugla_koyu', Y)
# the open hypogeum: pit walls, floor, brick corridor walls with arches
for a, b in ((V(HX, 0), V(HX, HY)), (V(HX, HY), V(-HX, HY)), (V(-HX, HY), V(-HX, 0))):
    y.yuz_yon([V(a.x, a.y, Z_PIT), V(b.x, b.y, Z_PIT), V(b.x, b.y, Z_FLOOR), V(a.x, a.y, Z_FLOOR)], 'tugla_koyu', V(0, 0.1) - (a + b) / 2)
ust([V(-HX, 0, Z_PIT), V(HX, 0, Z_PIT), V(HX, HY, Z_PIT), V(-HX, HY, Z_PIT)], 'toprak')
ZW = Z_FLOOR - 0.008
for yy in (0.05, 0.1, 0.15):
    kutu_merkez(y, (0, yy), 2 * HX, 0.012, ZW - Z_PIT, 'tugla', z0=Z_PIT, yuzler='onarkaust')
    for xx in (-0.19, 0.09):
        for sg in (-1, 1):
            y.pencere(V(xx, yy + sg * 0.006, Z_PIT), V(1, 0), V(0, sg), 0, 0.0, 0.034, 0.04, 'koyu', kemer=True)
for xx in (-0.19, -0.05, 0.09, 0.23):   # cross walls, every other bay
    for (ya, yb) in ((0.0, 0.044), (0.106, 0.144)) if xx in (-0.19, 0.09) else ((0.056, 0.094), (0.156, HY)):
        kutu_merkez(y, (xx, (ya + yb) / 2), 0.012, yb - ya, ZW - Z_PIT, 'tugla', z0=Z_PIT, yuzler='sagsolust')

# ---------------------------------------------------------------- the north porch (imperial entrance)
y.bolum('kuzey giris')
k = min(range(N), key=lambda q: abs(bay_aci(q) - 90))
a, b = P[k], P[k + 1]
nn = (NRM[k] + NRM[k + 1]).normalized()
e = (b - a).normalized()
m = (a + b) / 2
w, dp = 0.13, 0.085
fa, fb = m - e * (w / 2) + nn * dp, m + e * (w / 2) + nn * dp
for p in (fa, fb):
    kutu_merkez(y, p, 0.026, 0.026, 0.02, 'kum_acik', z0=Z0, aci=math.atan2(e.y, e.x))
    for sg in (1, -1):   # a free column: two half columns back to back
        yarim_sutun(p, nn * sg, Z0 + 0.02, Z0 + 0.12, 0.0095, 'korint', 'mermer')
for p in (a.lerp(b, 0.5) - e * (w / 2), a.lerp(b, 0.5) + e * (w / 2)):
    yarim_sutun(p, nn, Z0 + 0.0, Z0 + 0.12, 0.0095, 'korint', 'mermer')
oa = m - e * (w / 2 + 0.012) + nn * 0.0
kutu(y, oa + nn * (dp + 0.016) + Z * (Z0 + 0.12), e, w + 0.024, dp + 0.016, 0.026, 'mermer', 'onsagsolust')
alinlik(y, fa - e * 0.012 + nn * 0.016, fb + e * 0.012 + nn * 0.016, Z0 + 0.146, 0.04, dp + 0.016, 'mermer', 'kum_acik', c=0.006,
        cati_key='kiremit')
kutu(y, m - e * (w / 2 + 0.03) + nn * (dp + 0.03), e, w + 0.06, dp + 0.03, Z0, 'kirec', 'onsagsolust')
kutu(y, m - e * (w / 2 + 0.03) + nn * (dp + 0.03) + Z * (Z0 - 0.006), e, w + 0.06, dp + 0.03, 0.006, 'zemin', 'ust')
merdiven(y, m + nn * (dp + 0.066), math.atan2(-nn.y, -nn.x), w, 0.02, Z0, n=3)

# ---------------------------------------------------------------- banners on the standing attic
y.bolum('sancak')
for hedef in (100, 175):
    k = min(range(N), key=lambda q: abs(bay_aci(q) - hedef))
    p = R(Dk * 0.5, k)
    sancak(y, p.x, p.y, ZT, boy=0.24, en=0.13, yuk=0.08, aci=math.atan2(-NRM[k].y, -NRM[k].x) + 0.6)

if os.environ.get('LM_BOLUM'):
    bl = y.bolumler + [(len(y.faces), 'son')]
    for (a, ad), (b, _) in zip(bl, bl[1:]): print('UCGEN', ad, sum(len(p) - 2 for p, _ in y.faces[a:b]))
calistir(y, 'lm_kolezyum')
