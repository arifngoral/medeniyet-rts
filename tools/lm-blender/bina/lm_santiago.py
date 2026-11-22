# Santiago de Compostela cathedral (lm_santiago): the baroque Obradoiro front on its podium over the Praza do
# Obradoiro: two tall towers rising in diminishing belfry stages to lanterns and cupolas, the stepped central body
# with the portal, the great window, the attic niche with St James and the crowning statue, the double stair down
# to the square with the crypt door between; behind it the Romanesque granite church (nave and aisles, transept with
# the Platerias portals, the octagonal crossing lantern, the ambulatory with radiating chapels), the Clock Tower,
# the cloister with the stepped Treasury roof, the Gelmirez palace; the Hostal and San Xerome flanking the square,
# a cruceiro and pilgrims.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import kutu3, levha, pilaster, korkuluk_hafif, heykel, piramit_cati, sutun_hafif, ucgen_alinlik, eksen
from arap_ortak import adam, halka_cati
from bina_ortak import calistir

y = Yapi()
rng = y.rng

Z0 = 0.02                     # the square
ZB = 0.12                     # the podium (church floor)
FY = -0.42                    # the front of the towers
BAR = 'kum'                   # the baroque front's warm golden granite
BAR_A = 'kum_acik'             # its mouldings and carving
ROM = 'granit'                # the Romanesque church
ROM_K = 'granit_koyu'
CATI = ('granit_koyu', 'granit')   # stepped stone roofs
PEN_R = (ROM, ROM_K, 'tas_acik', 'koyu')


def obelisk(x, yy, z, h=0.06, w=0.014, key=BAR_A):
    """a baroque obelisk pinnacle on a small plinth, a ball on top"""
    kutu_merkez(y, (x, yy), w * 1.5, w * 1.5, w * 0.8, key, z0=z)
    piramit_cati(y, (x, yy), w, w, z + w * 0.8, h, key)
    kure(y, (x, yy, z + w * 0.8 + h + 0.004), w * 0.3, key, n=6, kat=3)


def dacik(*a, **k):
    """dikdortgen_acik with the frame's inner edges closed"""
    k.setdefault('ic_kenar', True)
    return dikdortgen_acik(*a, **k)


def kornis_on(x0, x1, yy, z, h, c, key=BAR_A, profil='tac'):
    """a cornice along a front facing -y"""
    silme(y, [V(x0, yy), V(x1, yy)], z, h, c, key, profil, kapali=False)


# ---------------------------------------------------------------- the square and the podium
y.bolum('Meydan ve kaide')
GX0, GX1, GY0, GY1 = -1.12, 1.12, -1.14, 1.02
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'tas_koyu', 'onarkasagsol')
y.yuz_yon([V(GX0, GY0, Z0), V(GX1, GY0, Z0), V(GX1, GY1, Z0), V(GX0, GY1, Z0)], 'zemin', Z)

PX0, PX1, PY0, PY1 = -0.76, 0.76, -0.62, 0.98
pk = dikdortgen(PX0, PX1, PY0, PY1)
for i in range(4):
    a, b = pk[i], pk[(i + 1) % 4]
    if i == 0:   # the podium's front with the crypt door in the middle
        duz_duvar(y, a, V(-0.06, PY0), Z0, ZB, ROM_K)
        y.kemerli(V(-0.06, PY0), V(0.06, PY0), Z0, ZB - Z0, (ROM_K, ROM_K, 'tas_acik', 'koyu'), v0=0.0, en=0.6, ust=0.012, derin=0.02, k_say=8,
                  cerceve=(0.006, BAR_A))
        duz_duvar(y, V(0.06, PY0), b, Z0, ZB, ROM_K)
    else:
        duz_duvar(y, a, b, Z0, ZB, ROM_K)
y.yuz_yon([V(p.x, p.y, ZB) for p in pk], 'zemin', Z)
silme(y, pk, ZB - 0.01, 0.01, 0.007, BAR_A, 'tac')
# the double stair: two flights climbing towards the middle along the podium's front, balustrades
SW = 0.075
for s in (-1, 1):
    x_bot, x_top = s * 0.5, s * 0.16
    n = 9
    d = abs(x_bot - x_top) / n
    yon = 0.0 if s < 0 else math.pi
    merdiven(y, (x_bot, PY0 - SW / 2), yon, SW, Z0, ZB, n=n, d=d, key=BAR)
    # the outer balustrade: a sloping rail on posts
    yo = PY0 - SW - 0.006
    for k in range(n + 1):
        xx = x_bot + (x_top - x_bot) * k / n
        zz = Z0 + (ZB - Z0) * min(1.0, (k + 0.5) / n)
        kutu3(y, V(xx, yo, zz + 0.016), X, Y, Z, 0.012, 0.012, 0.032, BAR_A, ('+x', '-x', '+y', '-y', '+z'))
    cubuk(y, V(x_bot, yo, Z0 + 0.034), V(x_top, yo, ZB + 0.034), 0.014, BAR_A, 0.008)
    kutu3(y, V(x_bot, yo, Z0 + 0.025), X, Y, Z, 0.02, 0.02, 0.05, BAR, ('+x', '-x', '+y', '-y', '+z'))
    obelisk(x_bot, yo, Z0 + 0.05, 0.04, 0.012)
# the podium's front balustrade (between the stair heads and to the corners)
for (xa, xb) in ((-0.16, 0.16), (PX0, -0.5), (0.5, PX1)):
    korkuluk_hafif(y, [V(xa, PY0 + 0.01), V(xb, PY0 + 0.01)], ZB, 0.03, kapali=False, key=BAR_A, aralik=0.02, ayak=0.16)

# ---------------------------------------------------------------- the towers
y.bolum('Obradoiro kuleleri')
TW = 0.17
TZ1 = ZB + 0.56


def kare_kat(cx, cy, w, z0, z1, acik=True, en=0.55, kolon=True):
    """a square belfry stage: an arched opening each side, columns at the corners, a cornice"""
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        if acik:
            y.kemerli(a, b, z0, z1 - z0, (BAR, BAR, BAR_A, 'koyu'), v0=0.012, en=en, ust=(z1 - z0) * 0.16, derin=0.022, k_say=8, cerceve=(0.006, BAR_A))
        else:
            duz_duvar(y, a, b, z0, z1, BAR)
    for p in k:
        d = (p - V(cx, cy)).normalized()
        if kolon:
            for t in (-1, 1):
                e = V(-d.y, d.x)
                q = p + d * 0.008 + e * (t * 0.016)
                sutun_hafif(y, q.x, q.y, z0, z1 - 0.012, 0.0055, BAR_A, 'iyon', n=6)
        else:
            kutu_merkez(y, (p.x, p.y), 0.02, 0.02, z1 - z0, BAR_A, z0=z0)
    silme(y, disa(k, 0.01), z1 - 0.012, 0.012, 0.01, BAR_A, 'tac')
    y.yuz_yon([V(p.x, p.y, z1) for p in disa(k, 0.02)], 'zemin', Z)
    return k


def kule(cx, cy):
    k = dikdortgen(cx - TW / 2, cx + TW / 2, cy - TW / 2, cy + TW / 2)
    # the shaft: plain granite with corner pilasters, a window band and a niche
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        a2, b2, L, e, nc = eksen(a, b)
        duz_duvar(y, a, b, ZB, ZB + 0.24, BAR)
        dacik(y, a, b, ZB + 0.24, 0.16, 0.34, 0.66, 0.03, 0.13, (BAR, BAR, BAR_A, 'koyu'), derin=0.014, cerceve=(0.006, BAR_A))
        duz_duvar(y, a, b, ZB + 0.4, TZ1, BAR)
        ucgen_alinlik(y, lambda u, v: a2 + e * (u * L) + Z * v, e, nc, 0.3, 0.7, ZB + 0.24 + 0.143, 0.025, BAR_A, 0.008)
        y.oculus(a2.lerp(b2, 0.5) + Z * (ZB + 0.45), e, nc, 0.018, 'koyu', BAR_A, f=0.006, k=12)
        for t in (0.0, 1.0):
            pilaster(y, a2.lerp(b2, t) + e * (0.011 if t == 0 else -0.011), e, nc, ZB, TZ1 - ZB - 0.02, w=0.022, d=0.006, key=BAR_A)
        for t in (0.24, 0.76):   # paired inner pilasters on the upper shaft, framing the oculus
            pilaster(y, a2.lerp(b2, t), e, nc, ZB + 0.405, TZ1 - ZB - 0.425, w=0.016, d=0.005, key=BAR_A)
    silme(y, k, ZB, 0.03, 0.01, BAR_A, 'kaide')
    silme(y, k, ZB + 0.235, 0.01, 0.008, BAR_A, 'duz')
    silme(y, disa(k, 0.006), ZB + 0.4, 0.008, 0.008, BAR_A, 'duz')
    silme(y, disa(k, 0.006), TZ1 - 0.02, 0.02, 0.012, BAR_A, 'tac')
    y.yuz_yon([V(p.x, p.y, TZ1) for p in disa(k, 0.018)], 'zemin', Z)
    korkuluk_hafif(y, disa(k, 0.012), TZ1, 0.028, key=BAR_A, aralik=0.022, ayak=0.1)
    for p in disa(k, 0.012):
        obelisk(p.x, p.y, TZ1 + 0.032, 0.05, 0.014)
    # stage 1: the big belfry
    z1 = TZ1 + 0.19
    k1 = kare_kat(cx, cy, 0.13, TZ1, z1, en=0.5)
    korkuluk_hafif(y, disa(k1, 0.016), z1, 0.024, key=BAR_A, aralik=0.022, ayak=0.08)
    for p in disa(k1, 0.016):
        obelisk(p.x, p.y, z1 + 0.026, 0.045, 0.012)
    # stage 2
    z2 = z1 + 0.15
    k2 = kare_kat(cx, cy, 0.095, z1, z2, en=0.5, kolon=False)
    for p in disa(k2, 0.012):
        obelisk(p.x, p.y, z2, 0.035, 0.01)
    # stage 3: an octagonal lantern, a cupola, the finial with a cross
    r3 = 0.04
    ok = cokgen((cx, cy), r3, 8, math.pi / 8)
    z3 = z2 + 0.075
    for i in range(8):
        y.kemerli(ok[i], ok[(i + 1) % 8], z2, z3 - z2, (BAR, BAR, BAR_A, 'koyu'), v0=0.01, en=0.5, ust=0.012, derin=0.008, k_say=6)
    silme(y, cokgen((cx, cy), r3, 8, math.pi / 8), z3 - 0.008, 0.008, 0.007, BAR_A, 'tac')
    t = y.kubbe((cx, cy), r3 + 0.004, z3, 0.04, BAR, n=16, kat=5)
    y.prizma((cx, cy), 0.01, t.z - 0.004, t.z + 0.02, BAR_A, n=6)
    kure(y, (cx, cy, t.z + 0.03), 0.011, BAR_A, n=8, kat=4)
    cubuk(y, V(cx, cy, t.z + 0.04), V(cx, cy, t.z + 0.08), 0.005, 'demir')
    cubuk(y, V(cx - 0.012, cy, t.z + 0.066), V(cx + 0.012, cy, t.z + 0.066), 0.005, 'demir')
    return t.z + 0.08


TXs = 0.29
TY = FY + TW / 2
for s in (-1, 1):
    kule(s * TXs, TY)

# ---------------------------------------------------------------- the central body
y.bolum('Obradoiro orta gövde')
CX = TXs - TW / 2                  # its half width (0.205)
CF = FY - 0.02                     # its front, projecting
CB = FY + 0.07                     # its back (the nave starts there)
ZA, ZBb, ZC, ZD = ZB + 0.24, ZB + 0.5, ZB + 0.66, ZB + 0.76
# level A: the portal between paired columns
xs = [-CX, -0.12, -0.07, 0.07, 0.12, CX]
for j in range(5):
    p, q = V(xs[j], CF), V(xs[j + 1], CF)
    if j == 2:
        y.kemerli(p, q, ZB, ZA - ZB, (BAR, BAR, BAR_A, 'ahsap_koyu'), v0=0.0, en=0.82, ust=0.03, derin=0.03, k_say=10, cerceve=(0.008, BAR_A))
    elif j in (1, 3):
        kemer_nis(y, p, q, ZB, ZA - ZB, en=0.6, ust=0.04, sivri=0.0, derin=0.012, key=BAR, yan_key=BAR, alt_key=BAR_A, arka_key=BAR, v0=0.06, k_say=8)
        m = p.lerp(q, 0.5)
        heykel(y, m.x, m.y + 0.006, ZB + 0.06, 1.5, BAR_A, -math.pi / 2)
    else:
        duz_duvar(y, p, q, ZB, ZA, BAR)
for xx in (-0.19, -0.135, 0.135, 0.19, -0.075, 0.075):
    kutu_merkez(y, (xx, CF - 0.012), 0.026, 0.026, 0.04, BAR_A, z0=ZB)
    sutun_hafif(y, xx, CF - 0.012, ZB + 0.04, ZA - 0.014, 0.008, BAR_A, 'iyon', n=8)
kornis_on(-CX - 0.01, CX + 0.01, CF - 0.03, ZA - 0.016, 0.018, 0.012)
y.yuz_yon([V(-CX - 0.01, CF - 0.03, ZA + 0.002), V(CX + 0.01, CF - 0.03, ZA + 0.002), V(CX + 0.01, CF, ZA + 0.002), V(-CX - 0.01, CF, ZA + 0.002)], BAR_A, Z)
# level B: the great window between the giant columns, niches with statues, a balcony
xs = [-CX, -0.11, 0.11, CX]
for j in range(3):
    p, q = V(xs[j], CF), V(xs[j + 1], CF)
    if j == 1:
        y.kemerli(p, q, ZA, ZBb - ZA, (BAR, BAR, BAR_A, 'cam'), v0=0.03, en=0.9, ust=0.03, derin=0.02, k_say=10, cerceve=(0.008, BAR_A))
    else:
        kemer_nis(y, p, q, ZA, ZBb - ZA, en=0.55, ust=0.07, sivri=0.0, derin=0.012, key=BAR, yan_key=BAR, alt_key=BAR_A, arka_key=BAR, v0=0.06, k_say=8)
        m = p.lerp(q, 0.5)
        heykel(y, m.x, m.y + 0.006, ZA + 0.06, 1.7, BAR_A, -math.pi / 2)
# mullions and transoms of the great window
for xx in (-0.05, 0.0, 0.05):
    kutu3(y, V(xx, CF + 0.017, (ZA + ZBb) / 2 - 0.02), X, Y, Z, 0.006, 0.004, ZBb - ZA - 0.1, BAR_A, ('-y', '+x', '-x'))
for zz in (ZA + 0.09, ZA + 0.16):
    kutu3(y, V(0, CF + 0.017, zz), X, Y, Z, 0.17, 0.004, 0.006, BAR_A, ('-y', '+z', '-z'))
for xx in (-0.15, -0.115, 0.115, 0.15):
    sutun_hafif(y, xx, CF - 0.012, ZA + 0.004, ZBb - 0.016, 0.009, BAR_A, 'iyon', n=8)
korkuluk_hafif(y, [V(-0.1, CF - 0.035), V(0.1, CF - 0.035)], ZA + 0.004, 0.026, kapali=False, key=BAR_A, aralik=0.018, ayak=0.1)
kornis_on(-CX - 0.01, CX + 0.01, CF - 0.03, ZBb - 0.018, 0.02, 0.014)
y.yuz_yon([V(-CX - 0.01, CF - 0.03, ZBb + 0.002), V(CX + 0.01, CF - 0.03, ZBb + 0.002), V(CX + 0.01, CF, ZBb + 0.002), V(-CX - 0.01, CF, ZBb + 0.002)], BAR_A, Z)
# the sides and the top of the projecting body below ZBb
for s in (-1, 1):
    y.yuz_yon([V(s * CX, CF, ZB), V(s * CX, FY, ZB), V(s * CX, FY, ZBb), V(s * CX, CF, ZBb)], BAR, V(s, 0))
# level C: the attic with St James' niche, flanked by scroll volutes
AX = 0.12
p, q = V(-AX, CF), V(AX, CF)
kemer_nis(y, p, q, ZBb, ZC - ZBb, en=0.5, ust=0.03, sivri=0.0, derin=0.018, key=BAR, yan_key=BAR, alt_key=BAR_A, arka_key=BAR, v0=0.02, k_say=8,
          cerceve=(0.007, BAR_A))
heykel(y, 0, CF + 0.009, ZBb + 0.022, 2.4, BAR_A, -math.pi / 2)
for s in (-1, 1):
    y.yuz_yon([V(s * AX, CF, ZBb), V(s * AX, CB, ZBb), V(s * AX, CB, ZC), V(s * AX, CF, ZC)], BAR, V(s, 0))
    # the volute: a quarter-round scroll from the attic's foot out to the body's edge
    pts = [V(s * AX, 0, ZBb)] + [V(s * (AX + (CX - AX) * (1 - math.sin(math.pi / 2 * k / 6))), 0, ZBb + (ZC - ZBb) * 0.75 * (1 - math.cos(math.pi / 2 * k / 6)))
                                 for k in range(6, -1, -1)]
    pts = [V(s * AX, 0, ZBb), V(s * CX, 0, ZBb)] + [V(s * (AX + (CX - AX) * math.cos(math.pi / 2 * k / 6)), 0, ZBb + (ZC - ZBb) * 0.8 * math.sin(math.pi / 2 * k / 6))
                                                    for k in range(1, 7)]
    for (y0_, y1_) in ((CF + 0.004, CF + 0.03),):
        front = [V(p_.x, y0_, p_.z) for p_ in pts]
        back = [V(p_.x, y1_, p_.z) for p_ in pts]
        y.yuz_yon(front, BAR_A, -Y)
        y.yuz_yon(back, BAR_A, Y)
        for i in range(1, len(pts)):
            a_, b_ = front[i], front[(i + 1) % len(pts)]
            a2, b2 = back[i], back[(i + 1) % len(pts)]
            m = (a_ + b_) / 2
            y.yuz_yon([a_, b_, b2, a2], BAR_A, V(m.x - s * AX, 0, m.z - ZBb))
    kure(y, (s * (CX - 0.005), CF + 0.017, ZBb + 0.022), 0.014, BAR_A, n=8, kat=4)
    obelisk(s * (CX - 0.01), CF + 0.0, ZBb + 0.004, 0.06, 0.014)
kornis_on(-AX - 0.01, AX + 0.01, CF - 0.012, ZC - 0.016, 0.018, 0.012)
y.yuz_yon([V(-AX, CF, ZC), V(AX, CF, ZC), V(AX, CB, ZC), V(-AX, CB, ZC)], BAR, Z)
# level D: the crowning pediment, the pilgrim St James on top
DX = 0.065
y.yuz_yon([V(-DX, CF + 0.006, ZC), V(DX, CF + 0.006, ZC), V(DX, CF + 0.006, ZD - 0.02), V(0, CF + 0.006, ZD + 0.02), V(-DX, CF + 0.006, ZD - 0.02)], BAR, -Y)
y.yuz_yon([V(-DX, CB, ZC), V(DX, CB, ZC), V(DX, CB, ZD - 0.02), V(0, CB, ZD + 0.02), V(-DX, CB, ZD - 0.02)], BAR, Y)
for (a_, b_) in ((V(DX, 0, ZC), V(DX, 0, ZD - 0.02)), (V(DX, 0, ZD - 0.02), V(0, 0, ZD + 0.02)), (V(0, 0, ZD + 0.02), V(-DX, 0, ZD - 0.02)),
                 (V(-DX, 0, ZD - 0.02), V(-DX, 0, ZC))):
    m = (a_ + b_) / 2
    y.yuz_yon([V(a_.x, CF + 0.006, a_.z), V(b_.x, CF + 0.006, b_.z), V(b_.x, CB, b_.z), V(a_.x, CB, a_.z)], BAR_A, V(m.x, 0, m.z - ZC - 0.01))
y.oculus(V(0, CF + 0.006, ZC + 0.04), X, -Y, 0.016, 'koyu', BAR_A, f=0.006, k=12)
heykel(y, 0, CF + 0.03, ZD + 0.016, 1.9, BAR_A, -math.pi / 2)
for s in (-1, 1):
    obelisk(s * (DX + 0.005), CF + 0.015, ZC, 0.05, 0.012)
    obelisk(s * (AX + 0.02), CF + 0.0, ZC - 0.002, 0.04, 0.011)
# the body's back above the nave roof (seen from behind)
y.yuz_yon([V(-CX, CB, ZB), V(CX, CB, ZB), V(CX, CB, ZBb), V(-CX, CB, ZBb)], BAR, Y)
y.yuz_yon([V(-AX, CB, ZBb), V(AX, CB, ZBb), V(AX, CB, ZC), V(-AX, CB, ZC)], BAR, Y)
y.yuz_yon([V(-CX, CF, ZBb + 0.002), V(-AX, CF, ZBb + 0.002), V(-AX, CB, ZBb + 0.002), V(-CX, CB, ZBb + 0.002)], 'zemin', Z)
y.yuz_yon([V(AX, CF, ZBb + 0.002), V(CX, CF, ZBb + 0.002), V(CX, CB, ZBb + 0.002), V(AX, CB, ZBb + 0.002)], 'zemin', Z)
for s in (-1, 1):
    y.yuz_yon([V(s * CX, FY, ZB), V(s * CX, CB, ZB), V(s * CX, CB, ZBb), V(s * CX, FY, ZBb)], BAR, V(s, 0))

# ---------------------------------------------------------------- the Romanesque church: nave, aisles, transept
y.bolum('Romanesk gövde: nef, yan nefler, transept')
NX = 0.16                        # nave half width
AXo = 0.3                        # aisles' outer wall
NZ = ZB + 0.34                   # nave wall top
AZ_ = ZB + 0.2                   # aisle wall top
TY0, TY1 = 0.1, 0.32             # transept
NY1 = 0.62                       # the apse starts
TX = 0.62                        # transept ends


def nef_bolum(y0, y1, side):
    """a stretch of aisle and nave wall between y0 and y1 on side (+1 / -1): aisle wall with round windows between
    buttresses, the aisle's lean-to roof, the nave's clerestory"""
    s = side
    n = max(1, int(round((y1 - y0) / 0.09)))
    a, b = (V(s * AXo, y0), V(s * AXo, y1)) if s > 0 else (V(s * AXo, y1), V(s * AXo, y0))
    pencereli_duvar(y, [a, b], ZB, AZ_ - ZB, [n], kapali=False, renk=PEN_R, v0=0.07, en=0.32, ust=0.025, derin=0.012, k_say=6, sivri=0.0,
                    cerceve=(0.004, 'tas_acik'))
    a2, b2, L, e, nc = eksen(a, b)
    for k in range(n + 1):
        p = a2.lerp(b2, k / n)
        kutu3(y, p + nc * 0.01 + Z * (ZB + (AZ_ - ZB) * 0.46), e, nc, Z, 0.022, 0.02, (AZ_ - ZB) * 0.92, ROM, ('+y', '+x', '-x', '+z'))
    silme(y, [a, b], AZ_ - 0.008, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)
    # the lean-to roof up to the nave wall
    zl = AZ_ + 0.012
    zh = ZB + 0.25
    for j in range(2):
        u0, u1 = j / 2, (j + 1) / 2
        q = [V(s * (AXo + 0.016 - (AXo + 0.016 - NX) * u0), y0, zl + (zh - zl) * u0), V(s * (AXo + 0.016 - (AXo + 0.016 - NX) * u0), y1, zl + (zh - zl) * u0),
             V(s * (AXo + 0.016 - (AXo + 0.016 - NX) * u1), y1, zl + (zh - zl) * u1), V(s * (AXo + 0.016 - (AXo + 0.016 - NX) * u1), y0, zl + (zh - zl) * u1)]
        y.yuz_yon(q, CATI[j], V(s, 0, 2))
    y.yuz_yon([V(s * (AXo + 0.016), y0, zl), V(s * (AXo + 0.016), y1, zl), V(s * (AXo + 0.016), y1, zl - 0.01), V(s * (AXo + 0.016), y0, zl - 0.01)], ROM_K, V(s, 0))
    y.yuz_yon([V(s * (AXo + 0.016), y0, zl - 0.01), V(s * (AXo + 0.016), y1, zl - 0.01), V(s * AXo, y1, AZ_), V(s * AXo, y0, AZ_)], ROM_K, -Z)
    for yy, sg in ((y0, -1), (y1, 1)):   # the roof's end triangles
        y.yuz_yon([V(s * AXo, yy, AZ_), V(s * NX, yy, AZ_), V(s * NX, yy, zh), V(s * (AXo + 0.016), yy, zl), V(s * (AXo + 0.016), yy, zl - 0.01)], ROM, V(0, sg))
    # the clerestory: small round windows over the aisle roof
    a, b = (V(s * NX, y0), V(s * NX, y1)) if s > 0 else (V(s * NX, y1), V(s * NX, y0))
    duz_duvar(y, a, b, ZB, zh, ROM)
    pencereli_duvar(y, [a, b], zh, NZ - zh, [n], kapali=False, renk=PEN_R, v0=0.02, en=0.3, ust=0.02, derin=0.01, k_say=6, sivri=0.0)
    silme(y, [a, b], NZ - 0.008, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)


for s in (-1, 1):
    nef_bolum(CB, TY0, s)
    nef_bolum(TY1, NY1, s)
# the aisles' fronts (between the towers' backs and the aisles' end) and the nave roof
for s in (-1, 1):
    y.yuz_yon([V(s * NX, CB, ZB), V(s * AXo, CB, ZB), V(s * AXo, CB, AZ_), V(s * NX, CB, AZ_)], ROM, -Y)
cati_besik(y, -NX, NX, CB, NY1, NZ, 0.1, 0.018, CATI[0], CATI[1], ucluk_key=ROM, ns=12, nr=5, dilim=list(CATI), uc_sacak=0.0)
# the transept arms with the gable fronts (Platerias to the south / +x, Azabacheria to the north)
for s in (-1, 1):
    x0, x1 = (NX, TX) if s > 0 else (-TX, -NX)
    tk = dikdortgen(x0, x1, TY0, TY1)
    # (the side walls in two parts: over the aisle, then the arm's own windowed wall)
    for yy, sg in ((TY0, -1), (TY1, 1)):
        xa, xb = (NX, AXo) if s > 0 else (-AXo, -NX)
        pa, pb = (V(xa, yy), V(xb, yy)) if sg < 0 else (V(xb, yy), V(xa, yy))
        duz_duvar(y, pa, pb, ZB, NZ, ROM)
        xa, xb = (AXo, TX) if s > 0 else (-TX, -AXo)
        pa, pb = (V(xa, yy), V(xb, yy)) if sg < 0 else (V(xb, yy), V(xa, yy))
        pencereli_duvar(y, [pa, pb], ZB, NZ - ZB, [3], kapali=False, renk=PEN_R, v0=0.17, en=0.35, ust=0.03, derin=0.012, k_say=6, sivri=0.0,
                        cerceve=(0.004, 'tas_acik'))
        silme(y, [pa, pb], NZ - 0.008, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)
    # the gable front: twin round-arched portals, a window above, buttresses at the corners
    xe = s * TX
    a, b = (V(xe, TY0), V(xe, TY1)) if s > 0 else (V(xe, TY1), V(xe, TY0))
    a2, b2, L, e, nc = eksen(a, b)
    m = a2.lerp(b2, 0.5)
    for (p, q) in ((a2, a2.lerp(b2, 0.12)), (a2.lerp(b2, 0.88), b2)):
        duz_duvar(y, p, q, ZB, NZ, ROM)
    for (p, q) in ((a2.lerp(b2, 0.12), m), (m, a2.lerp(b2, 0.88))):
        y.kemerli(p, q, ZB, 0.15, (ROM, ROM_K, 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.7, ust=0.02, derin=0.02, k_say=10, cerceve=(0.008, ['tas_acik', ROM]))
        y.kemerli(p, q, ZB + 0.15, NZ - ZB - 0.15, PEN_R, v0=0.04, en=0.5, ust=0.03, derin=0.014, k_say=8, cerceve=(0.005, 'tas_acik'))
    for t in (0.0, 1.0):
        p = a2.lerp(b2, t)
        q = p + nc * 0.012 + e * (0.016 if t == 0 else -0.016)
        kutu3(y, q + Z * ((NZ + ZB) / 2), e, nc, Z, 0.032, 0.024, NZ - ZB, ROM, ('+y', '+x', '-x', '+z'))
        piramit_cati(y, (q.x, q.y), 0.03, 0.03, NZ, 0.06, 'tas_acik')
    silme(y, [a, b], ZB + 0.15, 0.01, 0.01, 'tas_acik', 'duz', kapali=False)
    cati_besik(y, x0, x1, TY0, TY1, NZ, 0.1, 0.018, CATI[0], CATI[1], ucluk_key=ROM, ns=8, nr=5, dilim=list(CATI), uc_sacak=0.0)

# ---------------------------------------------------------------- the crossing lantern (cimborrio)
y.bolum('Kesişim feneri (cimborrio)')
CC = (0.0, (TY0 + TY1) / 2)
RC = 0.12
oc = cokgen(CC, RC, 8, math.pi / 8)
CZ0 = NZ + 0.06
for i in range(8):
    y.kemerli(oc[i], oc[(i + 1) % 8], CZ0 - 0.1, 0.24, PEN_R, v0=0.11, en=0.45, ust=0.03, derin=0.012, k_say=6, sivri=0.45, cerceve=(0.004, 'tas_acik'))
for p in oc:   # corner buttresses with pinnacles
    d = (p - V(*CC)).normalized()
    kutu_merkez(y, (p.x + d.x * 0.006, p.y + d.y * 0.006), 0.02, 0.02, 0.25, ROM, z0=CZ0 - 0.1, aci=math.atan2(d.y, d.x))
    piramit_cati(y, (p.x + d.x * 0.006, p.y + d.y * 0.006), 0.02, 0.02, CZ0 + 0.15, 0.05, 'tas_acik')
silme(y, oc, CZ0 + 0.13, 0.012, 0.01, 'tas_acik', 'tac')
korkuluk_hafif(y, disa(oc, 0.008), CZ0 + 0.142, 0.022, key='tas_acik', aralik=0.022, ayak=0.1)
ct = donel(y, CC, [(RC * 0.98, CZ0 + 0.142), (RC * 0.8, CZ0 + 0.2), (RC * 0.45, CZ0 + 0.25), (0.03, CZ0 + 0.27)], ROM_K, n=8, kat=math.pi / 8)
y.prizma(CC, 0.03, CZ0 + 0.27, CZ0 + 0.3, 'tas_acik', n=8)
kure(y, (CC[0], CC[1], CZ0 + 0.31), 0.014, 'tas_acik', n=8, kat=4)
cubuk(y, V(CC[0], CC[1], CZ0 + 0.32), V(CC[0], CC[1], CZ0 + 0.37), 0.005, 'demir')
cubuk(y, V(CC[0] - 0.013, CC[1], CZ0 + 0.352), V(CC[0] + 0.013, CC[1], CZ0 + 0.352), 0.005, 'demir')

# ---------------------------------------------------------------- the chevet: apse, ambulatory, radiating chapels
y.bolum('Apsis, ambulatuvar, şapeller')
AC = V(0.0, NY1)
RA, RAM = NX, AXo
NA = 8
apse = [AC + V(RA * math.cos(math.pi * i / NA), RA * math.sin(math.pi * i / NA)) for i in range(NA + 1)]
amb = [AC + V(RAM * math.cos(math.pi * i / NA), RAM * math.sin(math.pi * i / NA)) for i in range(NA + 1)]
ZAM = ZB + 0.18
# the apse's upper wall over the ambulatory roof, its fan roof
pencereli_duvar(y, apse, ZB + 0.23, NZ - ZB - 0.23, [1] * NA, kapali=False, renk=PEN_R, v0=0.02, en=0.4, ust=0.02, derin=0.01, k_say=6, sivri=0.0)
for i in range(NA):
    a, b = apse[i], apse[i + 1]
    duz_duvar(y, a, b, ZB, ZB + 0.23, ROM)
silme(y, apse, NZ - 0.008, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)
ea = disa(apse, 0.018, kapali=False)
for i in range(NA):
    a, b = ea[i], ea[i + 1]
    m = (a + b) / 2
    y.yuz_yon([V(a.x, a.y, NZ), V(b.x, b.y, NZ), V(AC.x, AC.y, NZ + 0.1)], CATI[i % 2], V(m.x - AC.x, m.y - AC.y, 1.2))
    y.yuz_yon([V(a.x, a.y, NZ), V(b.x, b.y, NZ), V(apse[i + 1].x, apse[i + 1].y, NZ), V(apse[i].x, apse[i].y, NZ)], ROM_K, -Z)
# the ambulatory wall and its ring roof
pencereli_duvar(y, amb, ZB, ZAM - ZB, [1] * NA, kapali=False, renk=PEN_R, v0=0.07, en=0.35, ust=0.025, derin=0.012, k_say=6, sivri=0.0,
                cerceve=(0.004, 'tas_acik'))
silme(y, amb, ZAM - 0.008, 0.008, 0.008, 'tas_acik', 'tac', kapali=False)
eb = disa(amb, 0.016, kapali=False)
for i in range(NA):
    a, b, c, d = eb[i], eb[i + 1], apse[i + 1], apse[i]
    m = (a + b) / 2
    y.yuz_yon([V(a.x, a.y, ZAM + 0.01), V(b.x, b.y, ZAM + 0.01), V(c.x, c.y, ZB + 0.23), V(d.x, d.y, ZB + 0.23)], CATI[i % 2], V(m.x - AC.x, m.y - AC.y, 1.5))
    y.yuz_yon([V(a.x, a.y, ZAM + 0.01), V(b.x, b.y, ZAM + 0.01), V(b.x, b.y, ZAM), V(a.x, a.y, ZAM)], ROM_K, V(m.x - AC.x, m.y - AC.y, 0))
    y.yuz_yon([V(a.x, a.y, ZAM), V(b.x, b.y, ZAM), V(amb[i + 1].x, amb[i + 1].y, ZAM), V(amb[i].x, amb[i].y, ZAM)], ROM_K, -Z)
for s in (-1, 1):   # the ring roof's ends against the nave and the walls closing the ambulatory to the aisles
    p0 = amb[0] if s > 0 else amb[NA]
    q0 = apse[0] if s > 0 else apse[NA]
    y.yuz_yon([V(p0.x, NY1, ZB), V(q0.x, NY1, ZB), V(q0.x, NY1, ZB + 0.23), V(p0.x, NY1, ZAM + 0.01)], ROM, -Y)
# radiating chapels
for ang in (math.pi * 0.22, math.pi * 0.5, math.pi * 0.78):
    d = V(math.cos(ang), math.sin(ang)); e = V(-d.y, d.x)
    c = AC + d * (RAM - 0.01)
    rr = 0.07
    pts =[c - e * (rr * math.cos(math.pi * i / 6)) + d * (rr * math.sin(math.pi * i / 6)) for i in range(7)]
    for i in range(6):
        if i in (2, 3):
            y.kemerli(pts[i], pts[i + 1], ZB, 0.13, PEN_R, v0=0.06, en=0.5, ust=0.02, derin=0.008, k_say=4)
        else:
            duz_duvar(y, pts[i], pts[i + 1], ZB, ZB + 0.13, ROM)
    silme(y, pts, ZB + 0.124, 0.006, 0.006, 'tas_acik', 'tac', kapali=False)
    top = c + Z * (ZB + 0.18)
    ep = disa(pts, 0.01, kapali=False)
    for i in range(6):
        a, b = ep[i], ep[i + 1]
        m = (a + b) / 2
        y.yuz_yon([V(a.x, a.y, ZB + 0.13), V(b.x, b.y, ZB + 0.13), top], CATI[i % 2], V(m.x - c.x, m.y - c.y, 1.0))
        y.yuz_yon([V(a.x, a.y, ZB + 0.13), V(b.x, b.y, ZB + 0.13), V(pts[i + 1].x, pts[i + 1].y, ZB + 0.13), V(pts[i].x, pts[i].y, ZB + 0.13)], ROM_K, -Z)

# ---------------------------------------------------------------- the Clock Tower (Berenguela)
y.bolum('Saat kulesi (Berenguela)')
BX, BY, BW = 0.4, 0.52, 0.13
bk = dikdortgen(BX - BW / 2, BX + BW / 2, BY - BW / 2, BY + BW / 2)
BZ1 = ZB + 0.42
for i in range(4):
    a, b = bk[i], bk[(i + 1) % 4]
    duz_duvar(y, a, b, ZB, ZB + 0.28, ROM)
    dacik(y, a, b, ZB + 0.28, BZ1 - ZB - 0.28, 0.3, 0.7, 0.02, 0.1, PEN_R, derin=0.012, cerceve=(0.005, 'tas_acik'))
    a2, b2, L, e, nc = eksen(a, b)
    m = a2.lerp(b2, 0.5)
    y.oculus(m + Z * (ZB + 0.22), e, nc, 0.026, 'beyaz', 'tas_acik', f=0.007, k=16)    # the clock face
    cubuk(y, m + nc * 0.006 + Z * (ZB + 0.22), m + nc * 0.006 + Z * (ZB + 0.238), 0.003, 'koyu')
    cubuk(y, m + nc * 0.006 + Z * (ZB + 0.22), m + nc * 0.006 + e * 0.012 + Z * (ZB + 0.222), 0.003, 'koyu')
for p in bk:
    kutu_merkez(y, (p.x, p.y), 0.018, 0.018, BZ1 - ZB, ROM, z0=ZB)
silme(y, disa(bk, 0.006), BZ1 - 0.016, 0.016, 0.012, 'tas_acik', 'tac')
y.yuz_yon([V(p.x, p.y, BZ1) for p in disa(bk, 0.012)], 'zemin', Z)
korkuluk_hafif(y, disa(bk, 0.01), BZ1, 0.024, key='tas_acik', aralik=0.022, ayak=0.07)
for p in disa(bk, 0.01):
    obelisk(p.x, p.y, BZ1 + 0.026, 0.045, 0.012)
# the octagonal baroque top: an open stage, a cupola, a lantern
ob = cokgen((BX, BY), 0.05, 8, math.pi / 8)
for i in range(8):
    y.kemerli(ob[i], ob[(i + 1) % 8], BZ1, 0.1, (BAR, BAR, BAR_A, 'koyu'), v0=0.01, en=0.55, ust=0.015, derin=0.01, k_say=6)
silme(y, ob, BZ1 + 0.092, 0.008, 0.008, BAR_A, 'tac')
t = y.kubbe((BX, BY), 0.054, BZ1 + 0.1, 0.045, BAR, n=16, kat=5)
y.prizma((BX, BY), 0.012, t.z - 0.004, t.z + 0.03, BAR_A, n=6)
kure(y, (BX, BY, t.z + 0.04), 0.012, BAR_A, n=8, kat=4)
cubuk(y, V(BX, BY, t.z + 0.05), V(BX, BY, t.z + 0.085), 0.005, 'demir')

# ---------------------------------------------------------------- the cloister and the Treasury
y.bolum('Klostr ve hazine kulesi')
KD = (0.34, 0.74, -0.4, 0.06)
KI = (0.44, 0.64, -0.3, -0.04)
KZI, KZR, KZD = ZB + 0.12, ZB + 0.18, ZB + 0.14
ki = dikdortgen(*KI)
y.yuz_yon([V(p.x, p.y, ZB + 0.002) for p in ki], 'cimen', Z)
kir = [ki[1], ki[0], ki[3], ki[2]]
for i in range(4):   # Gothic galleries facing into the cloister garth
    a, b = kir[i], kir[(i + 1) % 4]
    L = (b - a).length
    arkad(y, a, b, max(3, int(round(L / 0.05))), ZB, KZI - 0.01 - ZB, en=0.78, ust=0.02, sivri=0.5, derin=0.04, sutun_key='tas_acik', sutun_r=0.005,
          renk=(ROM, ROM, 'tas_acik', ROM_K), cerceve=None)
halka_cati(y, KI, KD, KZI, KZR, KZD, sacak=0.018, sacak_dis=0.018)
kd_ = dikdortgen(*KD)
for i in range(4):
    a, b = kd_[i], kd_[(i + 1) % 4]
    if i == 3: continue      # (against the aisle)
    L = (b - a).length
    pencereli_duvar(y, [a, b], ZB, KZD - 0.01 - ZB, [max(2, int(L / 0.08))], kapali=False, renk=PEN_R, v0=0.06, en=0.3, ust=0.025, derin=0.01,
                    k_say=6, sivri=0.0)
duz_duvar(y, kd_[3], kd_[0], ZB, KZD - 0.01, ROM)
# the Treasury tower at the cloister's front corner, its stepped pyramid roof
HX_, HY_, HW = 0.66, -0.36, 0.12
hk = dikdortgen(HX_ - HW / 2, HX_ + HW / 2, HY_ - HW / 2, HY_ + HW / 2)
HZ1 = ZB + 0.3
for i in range(4):
    a, b = hk[i], hk[(i + 1) % 4]
    duz_duvar(y, a, b, ZB, ZB + 0.18, BAR)
    dacik(y, a, b, ZB + 0.18, HZ1 - ZB - 0.18, 0.32, 0.68, 0.025, 0.09, (BAR, BAR, BAR_A, 'koyu'), derin=0.012, cerceve=(0.005, BAR_A))
silme(y, hk, HZ1 - 0.012, 0.012, 0.01, BAR_A, 'tac')
for k in range(6):   # the stepped pyramid
    w = HW + 0.02 - k * 0.022
    kutu_merkez(y, (HX_, HY_), w, w, 0.02, BAR if k % 2 else BAR_A, z0=HZ1 + k * 0.02)
obelisk(HX_, HY_, HZ1 + 0.12, 0.05, 0.016)
for p in disa(hk, 0.006):
    obelisk(p.x, p.y, HZ1, 0.035, 0.01)

# ---------------------------------------------------------------- the Gelmirez palace (north of the front)
y.bolum('Gelmírez sarayı')
GPX0, GPX1, GPY0, GPY1 = -0.75, -0.47, -0.19, 0.08     # (set back and aside: the left tower's foot stays in sight)
gk = dikdortgen(GPX0, GPX1, GPY0, GPY1)
GZ = ZB + 0.13
for i in range(4):
    a, b = gk[i], gk[(i + 1) % 4]
    if i == 1: continue
    L = (b - a).length
    n = max(2, int(L / 0.07))
    pencereli_duvar(y, [a, b], ZB, 0.1, [n], kapali=False, renk=PEN_R, v0=0.04, en=0.3, ust=0.02, derin=0.01, k_say=6, sivri=0.0)
    for j in range(n):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        dacik(y, p, q, ZB + 0.1, GZ - ZB - 0.1, 0.32, 0.68, 0.004, 0.022, PEN_R, derin=0.01, cerceve=(0.004, 'tas_acik'))
duz_duvar(y, gk[1], gk[2], ZB, GZ, ROM)
silme(y, gk, ZB + 0.1, 0.006, 0.005, 'tas_acik', 'duz')
silme(y, gk, GZ - 0.01, 0.01, 0.008, 'tas_acik', 'tac')
cati_kirma(y, GPX0, GPX1, GPY0, GPY1, GZ, 0.075, 0.02, 'kiremit', 'kiremit2', ns=8, nr=4, dilim=['kiremit', 'kiremit2'])
for (xx, yy) in ((-0.66, -0.06), (-0.53, 0.0)):
    kutu_merkez(y, (xx, yy), 0.026, 0.026, 0.13, ROM, z0=GZ + 0.02)
    kutu_merkez(y, (xx, yy), 0.034, 0.034, 0.008, 'tas_acik', z0=GZ + 0.15)

# ---------------------------------------------------------------- the square: Hostal, San Xerome, cruceiro, pilgrims
y.bolum('Hostal, San Xerome, haç, hacılar')


def saray(x0, x1, y0, y1, h, on_yon, portal=True, cati='kiremit', duvar=ROM):
    """a two-storey granite building on the square: windows in rows, a portal on the side facing the square"""
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        L = (b - a).length
        n = max(2, int(round(L / 0.09)))
        for j in range(n):
            p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
            if portal and i == on_yon and j == n // 2:
                y.kemerli(p, q, Z0, h * 0.5, (duvar, ROM_K, 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.7, ust=0.02, derin=0.02, k_say=8, cerceve=(0.007, BAR_A))
            else:
                dacik(y, p, q, Z0, h * 0.5, 0.3, 0.7, h * 0.18, h * 0.4, PEN_R, derin=0.01, cerceve=(0.004, 'tas_acik'))
            dacik(y, p, q, Z0 + h * 0.5, h * 0.5, 0.3, 0.7, h * 0.08, h * 0.38, PEN_R, derin=0.01, cerceve=(0.004, 'tas_acik'))
    silme(y, k, Z0 + h * 0.5, 0.006, 0.005, 'tas_acik', 'duz')
    silme(y, k, Z0 + h - 0.012, 0.012, 0.01, 'tas_acik', 'tac')
    silme(y, k, Z0, 0.02, 0.006, ROM_K, 'kaide')
    return cati_kirma(y, x0, x1, y0, y1, Z0 + h, 0.08, 0.022, cati, cati + '2' if cati == 'kiremit' else cati, ns=8, nr=4,
                      dilim=['kiremit', 'kiremit2'] if cati == 'kiremit' else None)


# the Hostal dos Reis Catolicos on the left, its plateresque portal facing the square
saray(-1.1, -0.84, -1.1, -0.5, 0.2, 1)
pa = V(-0.84, -0.8)
for (dz, w, h) in ((0.0, 0.12, 0.16), (0.16, 0.08, 0.05)):
    kutu3(y, V(pa.x + 0.004, pa.y, Z0 + dz + h / 2), X, Y, Z, 0.008, w, h, BAR_A, ('+x', '+y', '-y', '+z'))
for dy in (-0.045, 0.045):
    sutun_hafif(y, pa.x + 0.012, pa.y + dy, Z0, Z0 + 0.12, 0.006, BAR_A, 'iyon', n=6)
sancak(y, -0.97, -0.56, Z0 + 0.25, boy=0.2, en=0.13, yuk=0.08, aci=0.3)
# San Xerome on the right
saray(0.84, 1.1, -1.1, -0.55, 0.18, 3)
# town houses behind them along the podium's sides
for hi, (cx, cy, w, d, h) in enumerate(((-0.95, -0.3, 0.2, 0.12, 0.16), (-0.95, -0.02, 0.2, 0.15, 0.18), (-0.95, 0.3, 0.2, 0.15, 0.15),
                                        (-0.95, 0.66, 0.2, 0.2, 0.17), (0.95, -0.3, 0.2, 0.14, 0.16), (0.95, 0.02, 0.2, 0.15, 0.15),
                                        (0.95, 0.36, 0.2, 0.16, 0.18), (0.95, 0.74, 0.2, 0.18, 0.16))):
    DV =('siva', ROM, 'siva_krem', ROM)[hi % 4]
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2)
    duvarlar(y, k, Z0, Z0 + h, DV)
    silme(y, k, Z0, 0.016, 0.005, ROM_K, 'kaide')
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        a2, b2, L, e, nc = eksen(a, b)
        n = max(1, int(round(L / 0.07)))
        for j in range(n):   # white-framed windows (two rows), a door on the long front
            m = a2.lerp(b2, (j + 0.5) / n)
            for zz in ((h * 0.35, h * 0.72) if h > 0.15 else (h * 0.6,)):
                if i == 0 and j == n // 2 and zz < h * 0.5: continue
                kutu3(y, m + nc * 0.002 + Z * (Z0 + zz), e, nc, Z, 0.026, 0.004, 0.032, 'beyaz', ('+y', '+x', '-x', '+z', '-z'))
                kutu3(y, m + nc * 0.0045 + Z * (Z0 + zz), e, nc, Z, 0.017, 0.001, 0.024, 'koyu', ('+y',))
        if i == 0:
            kutu3(y, a2.lerp(b2, 0.5) + nc * 0.002 + Z * (Z0 + 0.025), e, nc, Z, 0.03, 0.004, 0.05, 'ahsap_koyu', ('+y', '+x', '-x', '+z'))
    cati_besik(y, cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, Z0 + h, 0.06, 0.016, 'kiremit', 'kiremit2', ucluk_key=DV, ns=4, nr=3,
               dilim=['kiremit', 'kiremit2'])
    kutu_merkez(y, (cx + w * 0.3, cy), 0.022, 0.022, 0.09, ROM, z0=Z0 + h)
# trees on the slopes behind
for (cx, cy) in ((-0.82, 0.95), (0.82, 0.95), (-0.5, 0.92), (0.55, 0.9), (-0.66, 0.4), (0.66, 0.36)):
    agac(y, cx, cy, ZB if abs(cx) < 0.76 else Z0, boy=0.14, key='yesil_koyu')
# a cruceiro (Galician stone cross) on the square
CRX, CRY = -0.5, -0.92
for k in range(3):
    kutu_merkez(y, (CRX, CRY), 0.07 - k * 0.018, 0.07 - k * 0.018, 0.012, ROM, z0=Z0 + k * 0.012)
y.prizma((CRX, CRY), 0.007, Z0 + 0.036, Z0 + 0.16, ROM, n=8)
kutu_merkez(y, (CRX, CRY), 0.016, 0.016, 0.012, ROM, z0=Z0 + 0.16)
cubuk(y, V(CRX, CRY, Z0 + 0.172), V(CRX, CRY, Z0 + 0.21), 0.007, ROM)
cubuk(y, V(CRX - 0.018, CRY, Z0 + 0.195), V(CRX + 0.018, CRY, Z0 + 0.195), 0.007, ROM)
# pilgrims with staffs, some resting by the stair
for i in range(13):
    px = -0.65 + 1.3 * rng.random()
    py_ = -1.08 + 0.36 * rng.random()
    if abs(px - CRX) < 0.06 and abs(py_ - CRY) < 0.06: continue
    a = rng.random() * TAU
    adam(y, px, py_, Z0, a, govde=rng.choice(('kumas', 'ahsap', 'boya_kirmizi', 'kece', 'ahsap_koyu')), bas=rng.choice(('kumas', 'ahsap_koyu', 'siva_krem')),
         boy=0.05)
    cubuk(y, V(px + 0.012 * math.cos(a + 1.2), py_ + 0.012 * math.sin(a + 1.2), Z0), V(px + 0.012 * math.cos(a + 1.2), py_ + 0.012 * math.sin(a + 1.2), Z0 + 0.065),
          0.003, 'ahsap_koyu')
sancak(y, 0.7, -0.64, ZB, boy=0.2, en=0.13, yuk=0.08, aci=0.5)

calistir(y, 'lm_santiago')
