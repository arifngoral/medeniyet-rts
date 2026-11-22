# Carcassonne (lm_carcassonne): the walled Cité on its hill. Two concentric curtain walls (the lower outer wall and the
# taller inner wall) with many round towers under Viollet-le-Duc's conical slate roofs and timber hoardings; the
# Narbonne Gate with its two great towers and the outer barbican gate; the Château Comtal with its own walls, towers,
# moat bridge and the tall Tour Pinte; the Basilica of Saint-Nazaire (Romanesque nave, Gothic choir); the town's
# tiled houses and lanes.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import *
from bina_ortak import calistir
import doku

y = Yapi()
R = random.Random(7)
ZT = 0.2                     # the plateau
TAS = 'tas'
OA, OB = 0.99, 0.83          # outer wall ellipse
IA, IB = 0.8, 0.66           # inner wall ellipse
PA, PB = 1.07, 0.91          # plateau edge


def elips(a, b, t):
    return V(a * math.cos(t), b * math.sin(t))


def elips_dis(a, b, t):
    """the outward normal of the ellipse at angle parameter t"""
    n = V(math.cos(t) / a, math.sin(t) / b)
    return n.normalized()


def icinde(p, a, b, pay=0.0):
    return (p.x / (a - pay)) ** 2 + (p.y / (b - pay)) ** 2 < 1


# ---------------------------------------------------------------- towers
def kule(c, r, z0, h, cati_h=None, cati='arduvaz', hoarding=True, n=14, yarik_say=3, duz=False, key=TAS, bayrak=False):
    """a round tower: battered base, a string course, arrow slits; a timber hoarding (wooden gallery on corbels) under a
    conical roof with a bellcast eave and a finial; duz: a flat crenellated top instead. Returns the top z"""
    c = (c[0], c[1])
    zb = z0 + h * 0.3
    # (the batter, then the string course and the shaft: the string course's underside never shows from above)
    donel(y, c, [(r * 1.08, z0), (r * 1.02, zb)], key, n=n)
    donel(y, c, [(r * 1.06, zb), (r * 1.06, zb + 0.007), (r, zb + 0.009), (r, z0 + h)], key, n=n)
    for k in range(yarik_say):
        a = TAU * (k + 0.5) / yarik_say + 0.4 + c[0] * 3
        nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
        for t in ((0.62,) if h < 0.2 else (0.5, 0.78)):
            o = V(c[0], c[1]) + nn * (r + 0.0012)
            yarik(y, o + Z * z0, e, nn, -0.003, h * t, 0.006, h * 0.08, 'koyu')
    ze = z0 + h
    if duz:
        return kule_yuvarlak(y, c, r, ze - 0.001, 0.001, key, 'duz', mazgal_h=0.024, n=n, egim=0, yarik_say=0, konsol=True)
    ch = cati_h or r * 2.6
    if hoarding:
        rh = r + 0.011
        hd = 0.03
        # the hoarding floor (underside), its corbels, the plank wall with loop-holes
        donel(y, c, [(r, ze), (rh, ze)], 'ahsap_koyu', n=n)
        for i in range(0, n if n >= 16 else 0, 2):
            a = TAU * (i + 1) / n
            d = V(math.cos(a), math.sin(a))
            p0 = V(c[0], c[1]) + d * (r - 0.002); p1 = V(c[0], c[1]) + d * (rh - 0.001)
            cubuk(y, p0 + Z * (ze - 0.006), p1 + Z * (ze - 0.003), 0.005, 'ahsap_koyu', 0.006)
        y.prizma(c, rh, ze, ze + hd, 'ahsap_dikey', n=n, ust=False)
        for i in range(n):
            if i % 2: continue
            a = TAU * (i + 0.5) / n
            d = V(math.cos(a), math.sin(a)); t = V(-d.y, d.x)
            kutu3(y, V(c[0], c[1]) + d * (rh * math.cos(math.pi / n) + 0.0008) + Z * (ze + hd * 0.55), t, d, Z, 0.006, 0.002, 0.009, 'koyu', ('+y',))
        zc = ze + hd
        re = rh + 0.012
        donel(y, c, [(rh - 0.001, zc), (re, zc)], 'ahsap_koyu', n=n)
    else:
        zc = ze
        re = r + 0.014
        konsol_halka(y, cokgen(c, r, n), ze - 0.02, 0.02, 0.008, key, 2)
        donel(y, c, [(r + 0.007, zc), (re, zc)], 'ahsap_koyu', n=n)
    donel(y, c, [(re, zc), (re * 0.86, zc + ch * 0.12), (re * 0.6, zc + ch * 0.45), (0.0, zc + ch)], cati, n=n)
    tip = zc + ch
    y.prizma(c, 0.0025, tip - 0.01, tip + 0.03, 'demir', n=4)
    kure(y, (c[0], c[1], tip + 0.012), 0.005, 'altin' if bayrak else 'demir', n=5, kat=3)
    return tip + 0.03


def kare_kule(cx, cy, w, z0, h, key=TAS, cati=None):
    """a square tower with slits, a corbelled crenellated top (or a slate pyramid roof)"""
    return kule_kare(y, cx, cy, w, z0, h, key, cati or 'duz', 'arduvaz', mazgal_h=0.022, sacak=0.012, yarik_say=2, konsol=True)


# ---------------------------------------------------------------- the hill
y.bolum('Tepe')
NH = 48
halkalar = [(1.17, 1.0, 0.0, 0.035), (1.152, 0.985, 0.035, 0.028), (1.135, 0.97, 0.07, 0.02), (1.115, 0.952, 0.11, 0.015),
            (1.095, 0.935, 0.15, 0.01), (PA, PB, ZT, 0.0)]


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def tepe_renk(x, yy, z):
    """the hill's colour per corner (doku.KOSE_RENK): meadow at the foot, dry scrub on the slope, bare limestone
    near the walls, in broad soft patches (never triangle by triangle)"""
    n = math.sin(x * 5.1 + 0.7) * math.cos(yy * 4.3 - 1.2) * 0.7 + math.sin(x * 11.0 - yy * 7.0 + 2.0) * 0.3
    h = z / ZT
    c = _mix((0.42, 0.51, 0.26), (0.49, 0.52, 0.29), 0.5 + 0.5 * n)
    c = _mix(c, (0.55, 0.50, 0.32), _ss(0.12, 0.45, h + 0.12 * n))
    c = _mix(c, (0.68, 0.62, 0.53), _ss(0.55, 0.92, h + 0.15 * n))
    return c


doku.KOSE_RENK['toprak_ot'] = tepe_renk
rings = []
for a, b, z, gur in halkalar:
    ring = []
    for i in range(NH):
        t = TAU * i / NH
        p = elips(a, b, t)
        f = 1 + gur * math.sin(3 * t + 0.7) + gur * 0.6 * math.sin(7 * t + 2.1)
        ring.append(V(p.x * f, p.y * f, z))
    rings.append(ring)
for k in range(len(rings) - 1):
    for i in range(NH):
        j = (i + 1) % NH
        key = 'toprak_ot'
        q = [rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]]
        m = (q[0] + q[1]) / 2
        y.yuz_yon(q, key, V(m.x, m.y, 0.6))
# the plateau: lists (between the walls) dry grass, the town paved
ic_k = [elips(IA - 0.01, IB - 0.01, TAU * i / NH) for i in range(NH)]
for i in range(NH):
    j = (i + 1) % NH
    y.yuz_yon([V(rings[-1][i].x, rings[-1][i].y, ZT), V(rings[-1][j].x, rings[-1][j].y, ZT), V(ic_k[j].x, ic_k[j].y, ZT), V(ic_k[i].x, ic_k[i].y, ZT)], 'cimen_kuru', Z)
y.yuz_yon([V(p.x, p.y, ZT) for p in ic_k], 'zemin', Z)
# trees and bushes round the foot of the hill
for i in range(20):
    t = TAU * (i + R.random() * 0.5) / 20
    p = elips(1.12, 0.96, t) * (1 + 0.03 * R.random())
    if abs(math.sin(t) + 1) < 0.15: continue    # keep the approach road clear
    agac(y, p.x, p.y, 0.04, boy=0.13 + 0.05 * R.random(), tur='servi' if i % 3 == 0 else 'yapraklı')

# the approach road climbing to the outer gate (-y)
y.bolum('Yol')
# a stone causeway climbing the slope to the barbican
RW = 0.065
ry0, ry1 = -1.1, -0.9
y.yuz_yon([V(-RW, ry0, 0.004), V(RW, ry0, 0.004), V(RW, ry1, ZT + 0.003), V(-RW, ry1, ZT + 0.003)], 'zemin', Z)
for sx in (-1, 1):
    y.yuz_yon([V(sx * RW, ry0, 0.004), V(sx * RW, ry1, ZT + 0.003), V(sx * RW, ry1, 0.0), V(sx * RW, ry0, 0.0)], 'tas_koyu', V(sx, 0))
    cubuk(y, V(sx * (RW - 0.004), ry0, 0.016), V(sx * (RW - 0.004), ry1, ZT + 0.015), 0.008, 'tas_koyu', 0.022)
    for k in range(3):   # buttresses along the causeway
        yy = ry0 + (ry1 - ry0) * (k + 0.5) / 3
        zz = (ZT + 0.003) * (k + 0.5) / 3
        kutu3(y, V(sx * (RW + 0.008), yy, zz / 2), X, Y, Z, 0.016, 0.02, zz, 'tas_koyu', ('+x', '-x', '+y', '-y', '+z'))
y.yuz_yon([V(-RW, ry0, 0.0), V(RW, ry0, 0.0), V(RW, ry0, 0.004), V(-RW, ry0, 0.004)], 'tas_koyu', -Y)

# ---------------------------------------------------------------- outer wall
y.bolum('Dış sur')
NO = 30
t_o = [-math.pi / 2 + TAU * i / NO for i in range(NO)]
GO = 0.07   # half width of the outer gate
yol_o = [V(GO, -OB)] + [elips(OA, OB, t) for t in t_o[1:]] + [V(-GO, -OB)]
sur(y, yol_o, ZT - 0.02, 0.13, 0.04, TAS, kapali=False, mazgal_h=0.022, parapet_h=0.01, ust_key='zemin')
for i, t in enumerate(t_o):
    if i == 0 or i % 2: continue
    p = elips(OA, OB, t) + elips_dis(OA, OB, t) * 0.02
    if i % 6 == 0:
        kule(p, 0.042, ZT - 0.02, 0.17, duz=True, n=12)
    else:
        kule(p, 0.042, ZT - 0.02, 0.17, cati_h=0.1, cati='kiremit' if i % 4 == 0 else 'arduvaz', hoarding=False, n=12, yarik_say=2)
# the barbican gate in the outer wall
kale_kapisi(y, 0, -OB, 0.15, ZT - 0.02, 0.15, derin=0.08, key=TAS, kule=None, kapi_key='ahsap_dikey')
for sx in (-1, 1):
    kule(V(sx * 0.1, -OB - 0.02), 0.045, ZT - 0.02, 0.2, cati_h=0.11, hoarding=True, n=12)

# ---------------------------------------------------------------- inner wall
y.bolum('İç sur')
NI = 24
t_i = [-math.pi / 2 + TAU * i / NI for i in range(NI)]
GI = 0.08
yol_i = [V(GI, -IB)] + [elips(IA, IB, t) for t in t_i[1:]] + [V(-GI, -IB)]
sur(y, yol_i, ZT - 0.01, 0.2, 0.05, TAS, kapali=False, mazgal_h=0.024, parapet_h=0.012, ust_key='zemin')
for i, t in enumerate(t_i):
    if i in (0, 1, NI - 1): continue
    p = elips(IA, IB, t) + elips_dis(IA, IB, t) * 0.025
    if i % 2 == 0:
        kule(p, 0.056, ZT - 0.01, 0.28, cati_h=0.15, hoarding=True, n=16)
    elif i in (5, 11, 17):
        kule(p, 0.05, ZT - 0.01, 0.26, duz=True, n=12)
# the Narbonne Gate: the gatehouse and its two great towers
y.bolum('Narbonne Kapısı')
kale_kapisi(y, 0, -IB, 0.17, ZT - 0.01, 0.24, derin=0.1, key=TAS, kule=None, kapi_key='ahsap_dikey', sivri=0.4)
for sx in (-1, 1):
    kule(V(sx * 0.13, -IB - 0.03), 0.078, ZT - 0.01, 0.34, cati_h=0.21, hoarding=True, n=20, yarik_say=4)
# the passage between the gates: paved
y.yuz_yon([V(-0.07, -OB + 0.04, ZT + 0.002), V(0.07, -OB + 0.04, ZT + 0.002), V(0.07, -IB - 0.05, ZT + 0.002), V(-0.07, -IB - 0.05, ZT + 0.002)], 'zemin', Z)

# ---------------------------------------------------------------- Château Comtal
y.bolum('Château Comtal')
CX0, CX1, CY0, CY1 = -0.6, -0.2, -0.14, 0.3
CZ = ZT
GY = 0.08
# talus (a sloped stone plinth) and the dry moat ring
tk0 = disa(dikdortgen(CX0, CX1, CY0, CY1), 0.035)
tk1 = dikdortgen(CX0, CX1, CY0, CY1)
mk = disa(dikdortgen(CX0, CX1, CY0, CY1), 0.085)
for i in range(4):
    j = (i + 1) % 4
    y.yuz_yon([V(tk0[i].x, tk0[i].y, CZ + 0.003), V(tk0[j].x, tk0[j].y, CZ + 0.003), V(tk1[j].x, tk1[j].y, CZ + 0.05), V(tk1[i].x, tk1[i].y, CZ + 0.05)],
              'tas_koyu', V((tk0[i].x + tk0[j].x) / 2 - (CX0 + CX1) / 2, (tk0[i].y + tk0[j].y) / 2 - (CY0 + CY1) / 2, 0.8))
    y.yuz_yon([V(mk[i].x, mk[i].y, CZ + 0.003), V(mk[j].x, mk[j].y, CZ + 0.003), V(tk0[j].x, tk0[j].y, CZ + 0.003), V(tk0[i].x, tk0[i].y, CZ + 0.003)], 'cimen', Z)
# curtain walls with a gap for the gate on the east side
yol_c = [V(CX1, GY + 0.05), V(CX1, CY1), V(CX0, CY1), V(CX0, CY0), V(CX1, CY0), V(CX1, GY - 0.05)]
sur(y, yol_c, CZ, 0.22, 0.04, TAS, kapali=False, mazgal_h=0.024, parapet_h=0.012, ust_key='zemin')
with parca(y, (CX1, GY, 0), math.pi / 2):
    kale_kapisi(y, 0, 0, 0.1, CZ, 0.22, derin=0.06, key=TAS, kule=None, kapi_key='ahsap_dikey')
for (px, py_) in ((CX0, CY0), (CX0, CY1), (CX1, CY1), (CX1, CY0), (CX0, (CY0 + CY1) / 2 + 0.06), ((CX0 + CX1) / 2, CY1), ((CX0 + CX1) / 2, CY0)):
    kule(V(px, py_), 0.05, CZ, 0.32, cati_h=0.16, hoarding=True, n=14)
for sy in (-1, 1):
    kule(V(CX1 + 0.01, GY + sy * 0.075), 0.045, CZ, 0.3, cati_h=0.15, hoarding=True, n=12)
# the bridge over the moat to the gate
with parca(y, (CX1 + 0.07, GY, 0), math.pi / 2):
    kemer_dizisi(y, V(-0.035, -0.05), V(0.035, -0.05), 1, CZ, 0.04, 0.1, renk=(TAS, 'tas_koyu', 'tas_acik', 'koyu'), en=0.55, ust=0.01, acik=False,
                 taban=False)
for sy in (-1, 1):
    cubuk(y, V(CX1 + 0.025, GY + sy * 0.033, CZ + 0.05), V(CX1 + 0.12, GY + sy * 0.033, CZ + 0.05), 0.006, TAS, 0.014)
# the courtyard and the residence (logis) along the north wall
y.yuz_yon([V(CX0, CY0, CZ + 0.003), V(CX1, CY0, CZ + 0.003), V(CX1, CY1, CZ + 0.003), V(CX0, CY1, CZ + 0.003)], 'zemin', Z)
LX0, LX1, LY0, LY1 = CX0 + 0.04, CX1 - 0.05, CY1 - 0.12, CY1 - 0.04
lk = dikdortgen(LX0, LX1, LY0, LY1)
pencereli_duvar(y, lk, CZ, 0.17, [5, 1, 0, 1], renk=(TAS, 'tas_koyu', 'tas_acik', 'koyu'), v0=0.06, en=0.4, ust=0.03, derin=0.01, k_say=6, sivri=0.0,
                cerceve=(0.004, 'tas_acik'))
cati_besik(y, LX0, LX1, LY0, LY1, CZ + 0.17, 0.07, 0.015, 'kiremit', 'kiremit2', ucluk_key=TAS, ns=8, nr=4)
# the Tour Pinte: the tall slender square watchtower on the west side
y.bolum('Pinte kulesi')
PX, PY = CX0 + 0.01, (CY0 + CY1) / 2 - 0.06
top = kare_kule(PX, PY, 0.08, CZ, 0.66)
for k in range(6):
    zz = CZ + 0.08 + k * 0.1
    silme(y, dikdortgen(PX - 0.04, PX + 0.04, PY - 0.04, PY + 0.04), zz, 0.006, 0.004, 'tas_koyu', 'duz')
sancak(y, PX, PY, top - 0.03, boy=0.2, en=0.11, yuk=0.065, aci=-math.pi * 0.3)

# ---------------------------------------------------------------- Basilica of Saint-Nazaire
y.bolum('Saint-Nazaire bazilikası')
BZ = ZT
NX0, NX1, NY0, NY1 = 0.2, 0.42, -0.27, -0.15     # nave
TX0, TX1, TY0, TY1 = 0.42, 0.5, -0.34, -0.08      # transept
HX1 = 0.58                                         # choir
NH_, TH_ = 0.19, 0.27
KOB = (TAS, 'tas_koyu', 'tas_acik', 'kobalt')
# nave: small round-headed Romanesque windows between buttress strips
pencereli_duvar(y, [V(NX0, NY0), V(NX1, NY0)], BZ, NH_, [4], kapali=False, renk=KOB, v0=0.09, en=0.28, ust=0.03, derin=0.01, k_say=6, sivri=0.0,
                cerceve=(0.004, 'tas_acik'))
pencereli_duvar(y, [V(NX1, NY1), V(NX0, NY1)], BZ, NH_, [4], kapali=False, renk=KOB, v0=0.09, en=0.28, ust=0.03, derin=0.01, k_say=6, sivri=0.0)
for xx in (0.255, 0.31, 0.365):
    for yy, s_ in ((NY0, -1), (NY1, 1)):
        kutu3(y, V(xx, yy + s_ * 0.008, BZ + NH_ * 0.45), X, Y, Z, 0.016, 0.016, NH_ * 0.9, TAS, ('+x', '-x', '+y', '-y', '+z'))
silme(y, [V(NX0, NY0), V(NX1, NY0)], BZ + NH_ - 0.008, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)
silme(y, [V(NX1, NY1), V(NX0, NY1)], BZ + NH_ - 0.008, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)
cati_besik(y, NX0, NX1, NY0, NY1, BZ + NH_, 0.08, 0.014, 'arduvaz', 'arduvaz', ucluk_key=TAS, ns=8, nr=4, uc_sacak=0.0)
# transept: a great lancet and a rose in each end, buttresses with pinnacles at the corners
tk = dikdortgen(TX0, TX1, TY0, TY1)
for (a, b) in ((tk[0], tk[1]), (tk[2], tk[3])):
    gotik_pencere(y, a, b, BZ, TH_ - 0.07, en=0.5, sivri=0.8, v0=0.03, cam='kobalt', duvar=TAS)
    a2, b2, L_, e, nc = eksen(a, b)
    duz_duvar(y, a2, b2, BZ + TH_ - 0.07, BZ + TH_, TAS)
    gul_pencere(y, a2.lerp(b2, 0.5) + Z * (BZ + TH_ - 0.035), e, nc, 0.022, yaprak=8, dis=1.15)
for (a, b) in ((tk[1], V(TX1, NY0 + 0.01)), (V(TX1, NY1 - 0.01), tk[2]), (tk[3], V(TX0, NY1)), (V(TX0, NY0), tk[0])):
    gotik_pencere(y, a, b, BZ + 0.06, TH_ - 0.06, en=0.45, sivri=0.8, v0=0.02, cam='kobalt', duvar=TAS, izli=False)
    duz_duvar(y, a, b, BZ, BZ + 0.06, TAS)
duz_duvar(y, V(TX0, NY1), V(TX0, NY0), BZ + NH_ - 0.01, BZ + TH_, TAS)   # (the crossing wall above the nave roof)
for p in tk:
    kutu_merkez(y, (p.x, p.y), 0.022, 0.022, TH_ + 0.01, TAS, z0=BZ)
    fiyal(y, p.x, p.y, 0.018, BZ + TH_ + 0.01, 0.02, 0.05, TAS)
cati_besik(y, TX0, TX1, TY0, TY1, BZ + TH_, 0.09, 0.014, 'arduvaz', 'arduvaz', ucluk_key=TAS, ns=6, nr=4, uc_sacak=0.01)
# choir: tall Gothic windows, a three-sided apse, buttresses with pinnacles
mid = (NY0 + NY1) / 2
ck = [V(TX1, NY0 + 0.01), V(HX1, NY0 + 0.01), V(HX1 + 0.04, mid - 0.025), V(HX1 + 0.04, mid + 0.025), V(HX1, NY1 - 0.01), V(TX1, NY1 - 0.01)]
for i in range(5):
    gotik_pencere(y, ck[i], ck[i + 1], BZ, TH_, en=0.55, sivri=0.8, v0=0.03, cam='kobalt', duvar=TAS)
for p in ck[1:5]:
    kutu_merkez(y, (p.x, p.y), 0.018, 0.018, TH_ - 0.02, TAS, z0=BZ)
    fiyal(y, p.x, p.y, 0.016, BZ + TH_ - 0.02, 0.03, 0.05, TAS)
silme(y, ck, BZ + TH_ - 0.006, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)
zr = BZ + TH_
RH = 0.07
cati_besik(y, TX1, HX1, NY0 + 0.01, NY1 - 0.01, zr, RH, 0.012, 'arduvaz', 'arduvaz', ucluk_key=TAS, ns=4, nr=4, uc_sacak=0.0)
top_c = V(HX1, mid, zr + RH)
ek = disa(ck, 0.012, kapali=False)
for i in range(1, 4):
    a, b = ek[i], ek[i + 1]
    y.yuz_yon([V(a.x, a.y, zr), V(b.x, b.y, zr), top_c], 'arduvaz', V((a.x + b.x) / 2 - top_c.x, (a.y + b.y) / 2 - top_c.y, 0.5))
    y.yuz_yon([V(a.x, a.y, zr), V(b.x, b.y, zr), V(ck[i + 1].x, ck[i + 1].y, zr), V(ck[i].x, ck[i].y, zr)], 'ahsap_koyu', -Z)
for e_, s_ in ((ek[1], -1), (ek[4], 1)):   # the slopes carried on to the apse's corners
    w = (NY1 - NY0 - 0.02) / 2 + 0.012
    y.yuz_yon([V(HX1, mid + s_ * w, zr), V(e_.x, e_.y, zr), top_c], 'arduvaz', V(0, s_, 1))
    y.yuz_yon([V(HX1, mid + s_ * w, zr), V(e_.x, e_.y, zr), V(e_.x, e_.y, zr - 0.004), V(HX1, mid + s_ * w, zr - 0.004)], 'ahsap_koyu', V(0, s_, 0))
# the fortified west front with its belfry tower
WX = NX0 - 0.055
kare_kule(WX, mid, 0.11, BZ, 0.3)
kutu3(y, V(WX - 0.055 - 0.0015, mid, BZ + 0.045), -X, Y, Z, 0.003, 0.036, 0.09, 'ahsap_koyu', ('+x', '+y', '-y', '+z'))
kutu3(y, V(WX - 0.055 - 0.003, mid, BZ + 0.094), -X, Y, Z, 0.006, 0.054, 0.008, 'tas_acik', ('+x', '+y', '-y', '+z', '-z'))
y.oculus(V(WX - 0.055, mid, BZ + 0.16), -Y, -X, 0.02, 'kobalt', 'tas_acik', f=0.005, k=12)

# ---------------------------------------------------------------- the town
y.bolum('Kasaba evleri')


def ev_cati(w, d, z, h, key, duvar, s=0.008, k=0.004):
    """a light gable roof for the small houses: two slopes with an overhang s, their thickness k (fascia, verges,
    undersides), the gable triangles and a ridge cap (ridge along x)"""
    a, b = w / 2 + s * 0.7, d / 2 + s
    T = V(0, 0, z + h)
    for sy in (-1, 1):
        eL, eR = V(-a, sy * b, z - h * s / (d / 2)), V(a, sy * b, z - h * s / (d / 2))
        rL, rR = V(-a, 0, z + h), V(a, 0, z + h)
        q = [eL, eR, rR, rL]
        y.yuz_yon(q, key, V(0, sy, 1))
        y.yuz_yon([eL, eR, eR - Z * k, eL - Z * k], 'ahsap_koyu', V(0, sy, 0))
        for sx in (-1, 1):
            e_, r_ = (eL, rL) if sx < 0 else (eR, rR)
            y.yuz_yon([e_, r_, r_ - Z * k, e_ - Z * k], 'ahsap_koyu', V(sx, 0, 0))
    for sx in (-1, 1):
        y.yuz_yon([V(sx * w / 2, -d / 2, z), V(sx * w / 2, d / 2, z), V(sx * w / 2, 0, z + h - k * 1.2)], duvar, V(sx, 0, 0))
    cubuk(y, V(-a, 0, z + h + 0.0012), V(a, 0, z + h + 0.0012), 0.006, 'kiremit2', 0.004)


def ev(cx, cy, w, d, h, aci, cati='kiremit', duvar='siva_krem'):
    """a town house: plastered or stone walls, a door and small windows, a tiled gable roof"""
    with parca(y, (cx, cy, 0), aci):
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        duvarlar(y, k, ZT, ZT + h, duvar)
        # door and windows on the long sides
        for i, s in ((0, -1), (2, 1)):
            a, b, L_, e, nc = eksen(k[i], k[(i + 1) % 4])
            for u in ((0.3, 0.7) if w > 0.06 else (0.5,)):
                c = a.lerp(b, u)
                kutu3(y, c + nc * 0.0008 + Z * (ZT + h * 0.68), e, nc, Z, 0.008, 0.0015, 0.011, 'koyu', ('+y',))
            if i == 0:
                c = a.lerp(b, 0.5 if w <= 0.06 else 0.5)
                kutu3(y, c + nc * 0.0008 + Z * (ZT + 0.011), e, nc, Z, 0.01, 0.0015, 0.022, 'ahsap_koyu', ('+y',))
        ev_cati(w, d, ZT + h, d * 0.42, cati, duvar)


def bos(p, m=0.0):
    """is the lot free: inside the inner wall, off the castle, the church, the gate and the lanes"""
    if not icinde(p, IA - 0.09 - m, IB - 0.09 - m): return False
    if CX0 - 0.13 < p.x < CX1 + 0.17 and CY0 - 0.13 < p.y < CY1 + 0.12: return False
    if NX0 - 0.1 < p.x < HX1 + 0.09 and TY0 - 0.07 < p.y < TY1 + 0.07: return False
    if abs(p.x) < 0.05 and p.y < 0.05: return False          # the main street from the gate
    if abs(p.y - GY) < 0.04 and p.x < 0.05: return False      # the street to the castle
    if abs(p.x - 0.12) < 0.03 and p.y > 0.0: return False     # a north lane
    return True


evler = 0
for gx in range(-12, 13):
    for gy in range(-10, 11):
        p = V(gx * 0.066 + R.uniform(-0.01, 0.01), gy * 0.066 + R.uniform(-0.01, 0.01))
        if not bos(p): continue
        w = R.uniform(0.045, 0.06); d = R.uniform(0.038, 0.048)
        h = R.uniform(0.05, 0.085)
        aci = (math.pi / 2 if (gx + gy) % 3 == 0 else 0.0) + R.uniform(-0.08, 0.08)
        ev(p.x, p.y, w, d, h, aci, 'kiremit', R.choice(('siva_krem', 'siva_krem', 'tas', 'siva_oker')))
        evler += 1
# a well in the little square
donel(y, (0.06, 0.2), [(0.0, ZT), (0.02, ZT), (0.02, ZT + 0.02), (0.016, ZT + 0.02), (0.016, ZT + 0.005), (0.0, ZT + 0.005)], 'tas_koyu', n=12)
for sx in (-1, 1):
    cubuk(y, V(0.06 + sx * 0.016, 0.2, ZT + 0.02), V(0.06 + sx * 0.016, 0.2, ZT + 0.05), 0.004, 'ahsap_koyu')
cubuk(y, V(0.044, 0.2, ZT + 0.05), V(0.076, 0.2, ZT + 0.05), 0.004, 'ahsap_koyu')

calistir(y, 'lm_carcassonne')
