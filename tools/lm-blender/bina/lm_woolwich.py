# Kraliyet Cephaneliği (lm_woolwich): the Royal Arsenal at Woolwich. The Georgian brick quadrangle of Dial Square with
# Portland-stone dressings and sash windows, its gateway (rusticated arch, pediment with the dial, royal arms, a lead
# cupola with clock faces); the Royal Brass Foundry (giant arched door, quoins, hipped slate roof, louvred lantern,
# furnace stacks and a tall factory chimney); the parade with ranks of guns, mortars and shot pyramids, the flagstaff,
# gunners; a Thames pier with a crane, powder barrels and a hoy; storehouses and timber at the back.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from ingiliz_ek import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.045
ZW = 0.015
KY = -0.95
TUG, TS = 'tugla', 'tas_acik'
CATI = 'arduvaz'


def kenarlar(x0, x1, y0, y1):
    k = dikdortgen(x0, x1, y0, y1)
    return [(k[i], k[(i + 1) % 4]) for i in range(4)]


def cephe(a, b, z0, katlar, n, kemer=False, plinth=True):
    """a Georgian brick front a->b: n sash windows a storey (0: plain), a stone plinth, string courses and a cornice.
    Returns the top z"""
    a, b, L, e, nc = eksen(a, b)
    z = z0
    for j, h in enumerate(katlar):
        if n:
            if kemer and j == 0:   # round-headed ground-floor windows in stone surrounds
                for k in range(n):
                    p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
                    y.kemerli(p, q, z, h, (TUG, 'tugla_koyu', TS, 'cam'), v0=h * 0.18, en=0.42, ust=h * 0.14, derin=0.012, k_say=6, sivri=0,
                              cerceve=(0.005, TS))
            else:
                sabun_pencere(y, a, b, z, z + h, n, h * 0.22, h * 0.8, (TUG, 'tugla_koyu', TS, 'cam'), nu=2, nv=3 if h > 0.1 else 2)
        else:
            duz_duvar(y, a, b, z, z + h, TUG)
        z += h
        if j < len(katlar) - 1:
            silme(y, [a, b], z - 0.005, 0.008, 0.005, TS, 'duz', kapali=False)
    if plinth:
        silme(y, [a, b], z0, 0.022, 0.008, 'tas', 'kaide', kapali=False)
    silme(y, [a, b], z - 0.012, 0.014, 0.012, TS, 'tac', kapali=False)
    return z


def blok(x0, x1, y0, y1, katlar, pen, cati='kirma', cati_h=0.12, kemer=False, baca=()):
    """a Georgian block: pen = windows a storey on each side (front -y, right +x, back +y, left -x; None: hidden,
    no wall), a hipped (or gabled: 'besik') slate roof, brick chimney stacks at baca = [(x, y)]"""
    zt = Z0
    for i, (a, b) in enumerate(kenarlar(x0, x1, y0, y1)):
        if pen[i] is None: continue
        zt = cephe(a, b, Z0, katlar, pen[i], kemer=kemer)
    zt = Z0 + sum(katlar)
    if cati == 'kirma':
        zr = cati_kirma(y, x0, x1, y0, y1, zt, cati_h, 0.018, CATI, mahya='kursun', kalinlik=0.008, alt_key=TS, ns=4, nr=3, mahya_en=0.008)
    elif cati == 'besik':
        zr = cati_besik(y, x0, x1, y0, y1, zt, cati_h, 0.018, CATI, mahya='kursun', kalinlik=0.008, alt_key=TS, ucluk_key=TUG,
                        alinlik_key=TS, nr=3, ns=4, mahya_en=0.008)
    else:
        zr = zt
    for (bx, by) in baca:
        kutu_merkez(y, (bx, by), 0.05, 0.03, cati_h * 0.9 + 0.06, TUG, z0=zt)
        kutu_merkez(y, (bx, by), 0.058, 0.038, 0.008, TS, z0=zt + cati_h * 0.9 + 0.06)
        for s in (-1, 0, 1):
            y.prizma((bx + s * 0.015, by), 0.005, zt + cati_h * 0.9 + 0.068, zt + cati_h * 0.9 + 0.085, 'kiremit', n=6)
    return zt, zr


# ---------------------------------------------------------------- ground, the river, the embankment
y.bolum('Zemin, Thames ve iskele')
su_ve_kiyi(y, -1.2, 1.2, -1.2, KY, ZW, Z0, KY, 'granit')
kutu(y, V(-1.2, KY, 0), X, 2.4, 1.15 - KY, Z0, 'granit_koyu', 'arkasagsol')
y.yuz_yon([V(-1.2, KY, Z0), V(1.2, KY, Z0), V(1.2, 1.15, Z0), V(-1.2, 1.15, Z0)], 'toprak', Z)
yer = lambda x0, x1, y0, y1, k='zemin', dz=0.0012: y.yuz_yon([V(x0, y0, Z0 + dz), V(x1, y0, Z0 + dz), V(x1, y1, Z0 + dz), V(x0, y1, Z0 + dz)], k, Z)
yer(-1.15, 1.15, -0.9, -0.36)          # the parade (paved)
yer(-0.8, 0.05, -0.1, 0.55, 'cimen')   # the Dial Square lawn
yer(-1.18, -1.05, -0.3, 1.1, 'cimen')
# the pier: a timber deck on piles running out into the river, a hand crane, barrels, a hoy alongside
PX0, PX1 = 0.28, 0.48
kutu(y, V(PX0, -1.17, ZW + 0.008), X, PX1 - PX0, KY + 1.17, Z0 - ZW - 0.008 + 0.003, 'ahsap', 'onsagsolust')
for k in range(4):
    for x in (PX0 + 0.008, PX1 - 0.008):
        y.prizma((x, -1.162 + k * 0.07), 0.0065, 0.0, Z0 + 0.01, 'kutuk', n=6)
for k in range(9):   # deck planks
    yy = -1.165 + k * 0.024
    y.yuz_yon([V(PX0, yy, Z0 + 0.0035), V(PX1, yy, Z0 + 0.0035), V(PX1, yy + 0.003, Z0 + 0.0035), V(PX0, yy + 0.003, Z0 + 0.0035)], 'ahsap_koyu', Z)
# the crane: a timber post with a jib and a gun hanging from its tackle
cx_, cy_ = PX1 - 0.03, -1.12
y.prizma((cx_, cy_), 0.012, Z0 + 0.003, Z0 + 0.2, 'ahsap', n=8)
kutu_merkez(y, (cx_, cy_), 0.05, 0.05, 0.02, 'ahsap_koyu', z0=Z0 + 0.003)
cubuk(y, V(cx_, cy_, Z0 + 0.1), V(cx_ + 0.14, cy_ - 0.04, Z0 + 0.21), 0.008, 'ahsap')
cubuk(y, V(cx_, cy_, Z0 + 0.2), V(cx_ + 0.14, cy_ - 0.04, Z0 + 0.21), 0.004, 'ahsap_koyu')
boru(y, [V(cx_ + 0.135, cy_ - 0.04, Z0 + 0.205), V(cx_ + 0.135, cy_ - 0.04, Z0 + 0.1)], 0.0012, 'koyu', n=4)
top_namlu(y, V(cx_ + 0.09, cy_ - 0.04, Z0 + 0.09), V(1, 0, 0.05), 0.1, 0.012, 'demir')
for k, (x, yy) in enumerate(((PX0 + 0.03, -1.0), (PX0 + 0.055, -1.0), (PX0 + 0.08, -1.0), (PX0 + 0.04, -1.03), (PX0 + 0.065, -1.03))):
    varil(y, x, yy, Z0 + 0.003, 0.011, 0.028)
for (x, yy) in ((PX0 + 0.03, -1.07), (PX0 + 0.055, -1.07)):
    varil(y, x, yy, Z0 + 0.003, 0.011, 0.028)
varil(y, PX0 + 0.042, -1.07, Z0 + 0.031, 0.011, 0.028)


def hoy(x, yy, aci):
    """a hoy (a small single-masted cargo vessel of the Ordnance): a bluff dark hull with a red sheer strake, a gaff
    mainsail and a jib"""
    with parca(y, (x, yy, ZW), aci):
        L, B = 0.3, 0.055
        n = 10
        us = [-1 + 2 * i / n for i in range(n + 1)]
        hb = lambda u: max(0.0006, B * max(0.0, 1 - abs(u) ** 2.4) ** 0.5)
        H0, HD, HS, HT = -0.004, 0.03, 0.036, 0.045        # bottom, deck, sheer strake, rail
        f = lambda z: 0.6 + 0.4 * (z - H0) / (HT - H0)      # the hull's half beam at height z (share of hb)
        Pt = lambda u, s, k, z: V(u * L / 2, s * hb(u) * k, z)
        mrk = lambda ua, ub: V((ua + ub) * L / 4 * 0.4, 0, 0.08)
        for s in (-1, 1):
            for i in range(n):
                ua, ub = us[i], us[i + 1]
                yuz_dis(y, [Pt(ua, s, f(HS), HS), Pt(ub, s, f(HS), HS), Pt(ub, s, 0.6, H0), Pt(ua, s, 0.6, H0)], 'ahsap_koyu', mrk(ua, ub))
                yuz_dis(y, [Pt(ua, s, 1.0, HT), Pt(ub, s, 1.0, HT), Pt(ub, s, f(HS), HS), Pt(ua, s, f(HS), HS)], 'boya_kirmizi', mrk(ua, ub))
                # inside the bulwark, the rail's top
                y.yuz_yon([Pt(ua, s, 0.86, HD), Pt(ub, s, 0.86, HD), Pt(ub, s, 0.95, HT), Pt(ua, s, 0.95, HT)], 'ahsap', V(0, -s, 0.3))
                y.yuz_yon([Pt(ua, s, 0.95, HT), Pt(ub, s, 0.95, HT), Pt(ub, s, 1.0, HT), Pt(ua, s, 1.0, HT)], 'ahsap_acik', Z)
                if s > 0:
                    y.yuz_yon([Pt(ua, -1, 0.86, HD), Pt(ub, -1, 0.86, HD), Pt(ub, 1, 0.86, HD), Pt(ua, 1, 0.86, HD)], 'ahsap_acik', Z)
        kutu3(y, V(-0.09, 0, HD + 0.012), X, Y, Z, 0.05, 0.05, 0.024, 'ahsap')
        for k in range(3):
            varil(y, 0.02 + k * 0.026, -0.012 + (k % 2) * 0.024, HD, 0.01, 0.024)
        y.prizma((0.0, 0), 0.0045, HD, 0.36, 'ahsap', n=6)
        cubuk(y, V(0.0, 0, 0.07), V(-0.15, 0, 0.09), 0.004, 'ahsap')          # boom
        cubuk(y, V(0.0, 0, 0.3), V(-0.12, 0, 0.34), 0.004, 'ahsap')           # gaff
        levha(y, [V(-0.004, 0, 0.075), V(-0.145, 0, 0.093), V(-0.118, 0, 0.335), V(-0.004, 0, 0.295)], 'kumas', Y)
        levha(y, [V(0.012, 0, 0.07), V(0.15, 0, 0.04), V(0.012, 0, 0.3)], 'kumas', Y)
        cubuk(y, V(0.0, 0, 0.35), V(0.16, 0, 0.038), 0.0015, 'koyu')


hoy(PX0 - 0.09, -1.08, math.pi / 2)
sandal(y, 0.85, -1.06, ZW, 0.25, L=0.1, B=0.024)
sandal(y, -0.7, -1.1, ZW, 2.9, L=0.1, B=0.024)
# the river gate: two stone piers with ball finials and railings along the embankment
for x in (PX0 - 0.03, PX1 + 0.03):
    kutu_merkez(y, (x, KY + 0.02), 0.04, 0.04, 0.09, 'tas', z0=Z0)
    kutu_merkez(y, (x, KY + 0.02), 0.048, 0.048, 0.01, TS, z0=Z0 + 0.09)
    kure(y, (x, KY + 0.02, Z0 + 0.118), 0.016, TS, n=8, kat=4)
for (x0_, x1_) in ((-1.15, PX0 - 0.05), (PX1 + 0.05, 1.15)):
    cubuk(y, V(x0_, KY + 0.012, Z0 + 0.04), V(x1_, KY + 0.012, Z0 + 0.04), 0.004, 'demir')
    for k in range(int((x1_ - x0_) / 0.06) + 1):
        y.prizma((x0_ + k * 0.06, KY + 0.012), 0.0025, Z0, Z0 + 0.045, 'demir', n=4)

# ---------------------------------------------------------------- Dial Square (the quadrangle)
y.bolum('Dial Square avlusu')
K2 = (0.13, 0.11)
QX0, QX1, QY0, QY1 = -1.0, 0.25, -0.3, 0.75
D = 0.2
P = 0.26          # corner pavilions
GX0, GX1 = -0.53, -0.22   # the gateway
ZQ = Z0 + sum(K2)
# ranges between the corner pavilions (outer and court fronts), gable roofs buried in the pavilions
rng = [((QX0 + P, GX0, QY0, QY0 + D), (3, None, 3, None)), ((GX1, QX1 - P, QY0, QY0 + D), (3, None, 3, None)),
       ((QX0 + P, QX1 - P, QY1 - D, QY1), (5, None, 7, None)),
       ((QX0, QX0 + D, QY0 + P, QY1 - P), (None, 4, None, 4)), ((QX1 - D, QX1, QY0 + P, QY1 - P), (None, 4, None, 4))]
for (x0, x1, y0, y1), pen in rng:
    blok(x0, x1, y0, y1, K2, pen, cati='besik', cati_h=0.1)
for (x0, x1, y0, y1) in ((QX0, QX0 + P, QY0, QY0 + P), (QX1 - P, QX1, QY0, QY0 + P), (QX0, QX0 + P, QY1 - P, QY1), (QX1 - P, QX1, QY1 - P, QY1)):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    inside = [x0 > QX0 + 0.01 or y0 > QY0 + 0.01, x1 < QX1 - 0.01 or y0 > QY0 + 0.01]
    pen = [2 if y0 < QY0 + 0.01 else 1, 2 if x1 > QX1 - 0.01 else 1, 2 if y1 > QY1 - 0.01 else 1, 2 if x0 < QX0 + 0.01 else 1]
    blok(x0, x1, y0, y1, K2 + (0.1,), pen, cati='kirma', cati_h=0.14, baca=[(cx, cy)])
# court: gravel walks, a statue of a gunner, two guns on display
y.bolum('Avlu: heykel ve sergi topları')
yer(-0.44, -0.31, -0.1, 0.55, 'zemin', 0.0025)
yer(-0.8, 0.05, 0.16, 0.28, 'zemin', 0.0025)
kutu_merkez(y, (-0.375, 0.22), 0.07, 0.07, 0.05, 'tas', z0=Z0)
silme(y, dikdortgen(-0.41, -0.34, 0.185, 0.255), Z0 + 0.044, 0.008, 0.005, TS, 'duz')
insan(y, -0.375, 0.22, Z0 + 0.05, 'bronz', 1.8, ten='bronz', aci=-math.pi / 2)
for x in (-0.65, -0.1):
    top_kizak(y, x, 0.05, Z0, -math.pi / 2, L=0.11, r=0.012, key='bronz')
    gulle_yigini(y, x, 0.13, Z0, n=3, r=0.008)

# ---------------------------------------------------------------- the Dial Square gateway
y.bolum('Dial Square kapısı ve kubbeciği')
GY0, GY1 = QY0 - 0.04, QY0 + D
K3 = (0.15, 0.12, 0.11)
ZG = Z0 + sum(K3)
gk = kenarlar(GX0, GX1, GY0, GY1)
# the front: a stone frontispiece in the middle (rusticated arch, columns, the pediment with the dial), brick bays beside
fx0, fx1 = -0.44, -0.31
cephe(V(GX0, GY0), V(fx0, GY0), Z0, K3, 1)
cephe(V(fx1, GY0), V(GX1, GY0), Z0, K3, 1)
for (a, b) in (gk[1], gk[3]):
    cephe(a, b, Z0, K3, 2)
cephe(V(GX1, GY1), V(GX0, GY1), Z0, K3, 0)
# frontispiece: the carriage arch (through, with doors), rustication bands, Doric columns, a pediment
_, _, _, L_ = y.kemerli(V(fx0, GY0), V(fx1, GY0), Z0, K3[0] + K3[1] * 0.3, ('tas', 'tas_koyu', TS, 'ahsap_koyu'), v0=0.0, en=0.62, ust=0.03,
                        derin=0.05, k_say=10, sivri=0, cerceve=(0.008, [TS, 'tas']))
for k in range(5):   # rustication grooves on the frontispiece's lower part
    zz = Z0 + 0.012 + k * 0.034
    for (u0, u1) in ((fx0, fx0 + 0.022), (fx1 - 0.022, fx1)):
        y.yuz_yon([V(u0, GY0 - 0.0012, zz), V(u1, GY0 - 0.0012, zz), V(u1, GY0 - 0.0012, zz + 0.003), V(u0, GY0 - 0.0012, zz + 0.003)], 'tas_koyu', -Y)
zf = Z0 + K3[0] + K3[1] * 0.3
dikdortgen_acik(y, V(fx0, GY0), V(fx1, GY0), zf, ZG - zf, 0.33, 0.67, 0.03, ZG - zf - 0.04, ('tas', 'tas_koyu', TS, 'cam'), derin=0.01,
                cerceve=(0.005, TS))
for sx in (fx0 - 0.004, fx1 + 0.004):
    sutun(y, sx, GY0 - 0.016, Z0 + 0.012, ZG - 0.004, 0.011, TS, 'toskan')
    kutu_merkez(y, (sx, GY0 - 0.016), 0.03, 0.03, 0.012, 'tas', z0=Z0)
kutu3(y, V((fx0 + fx1) / 2, GY0 - 0.012, ZG + 0.006), X, Y, Z, fx1 - fx0 + 0.04, 0.03, 0.014, TS, ('+x', '-x', '-y', '+z', '-z'))
zp = alinlik(y, V(fx0 - 0.02, GY0 - 0.027), V(fx1 + 0.02, GY0 - 0.027), ZG + 0.013, 0.07, derin=0.06, key=TS, ic_key='tas', c=0.008, cati_key=CATI)
kadran(y, V((fx0 + fx1) / 2, GY0 - 0.026, ZG + 0.04), X, -Y, 0.019, kare=False)
# royal arms over the arch (a shield, lion and unicorn as gilded lumps, the crown)
ra = V((fx0 + fx1) / 2, GY0 - 0.0016, Z0 + K3[0] + 0.012)
y.yuz_yon([ra + V(-0.014, 0, 0.016), ra + V(0.014, 0, 0.016), ra + V(0.014, 0, -0.004), ra + V(0, 0, -0.016), ra + V(-0.014, 0, -0.004)], 'boya_kirmizi', -Y)
for s in (-1, 1):
    kure(y, (ra.x + s * 0.024, ra.y - 0.004, ra.z), 0.008, 'altin', n=6, kat=3)
kure(y, (ra.x, ra.y - 0.004, ra.z + 0.024), 0.007, 'altin', n=6, kat=3)
# the parapet round the gate block's top, the roof and the cupola
duvarlar(y, dikdortgen(GX0, GX1, GY0, GY1), ZG, ZG + 0.03, TUG, ust=TS, kalinlik=0.012)
zr_g = cati_kirma(y, GX0 + 0.012, GX1 - 0.012, GY0 + 0.012, GY1 - 0.012, ZG + 0.004, 0.11, 0.002, CATI, mahya='kursun', kalinlik=0.006,
                  alt_key=TS, ns=3, nr=3, mahya_en=0.008)
CX_, CY_ = (GX0 + GX1) / 2, (GY0 + GY1) / 2
zc = ZG + 0.11        # (the clock stage stands clear of the hipped roof: lower, its dials were half buried)
kutu_merkez(y, (CX_, CY_), 0.1, 0.1, zc + 0.07 - (ZG + 0.02), 'tas', z0=ZG + 0.02)
for a, b in kenarlar(CX_ - 0.05, CX_ + 0.05, CY_ - 0.05, CY_ + 0.05):
    a2, b2, L, e, nc = eksen(a, b)
    kadran(y, (a2 + b2) / 2 + Z * (zc + 0.035), e, nc, 0.026, kare=False)
silme(y, dikdortgen(CX_ - 0.05, CX_ + 0.05, CY_ - 0.05, CY_ + 0.05), zc + 0.07, 0.01, 0.008, TS, 'tac')
y.yuz_yon([V(p.x, p.y, zc + 0.08) for p in dikdortgen(CX_ - 0.058, CX_ + 0.058, CY_ - 0.058, CY_ + 0.058)], 'kursun', Z)
ok = cokgen((CX_, CY_), 0.042, 8, math.pi / 8)
for i in range(8):   # the open octagonal lantern with the bell
    y.kemerli(ok[i], ok[(i + 1) % 8], zc + 0.08, 0.08, (TS, 'tas', TS, 'koyu'), v0=0.0, en=0.58, ust=0.012, derin=0.006, k_say=6, sivri=0)
silme(y, ok, zc + 0.16, 0.008, 0.006, TS, 'tac')
zd = zc + 0.168
donel(y, (CX_, CY_), [(0.046, zd), (0.044, zd + 0.012), (0.036, zd + 0.03), (0.02, zd + 0.05), (0.008, zd + 0.06), (0.012, zd + 0.07), (0.0, zd + 0.08)], 'kursun',
      n=8, kat=math.pi / 8)
kure(y, (CX_, CY_, zd + 0.088), 0.01, 'altin', n=8, kat=4)
y.prizma((CX_, CY_), 0.002, zd + 0.09, zd + 0.14, 'demir', n=4)
levha(y, [V(CX_, CY_, zd + 0.12), V(CX_ + 0.04, CY_, zd + 0.12), V(CX_ + 0.03, CY_, zd + 0.135), V(CX_, CY_, zd + 0.135)], 'altin', Y)   # vane

# ---------------------------------------------------------------- the Royal Brass Foundry
y.bolum('Kraliyet Pirinç Dökümhanesi')
FX0, FX1, FY0, FY1 = 0.42, 1.02, 0.05, 0.7
KF = (0.2, 0.15)
ZF = Z0 + sum(KF)
fk = kenarlar(FX0, FX1, FY0, FY1)
# sides and back: tall round-headed windows below, square above
for (a, b), n in ((fk[1], 4), (fk[2], 4), (fk[3], 4)):
    cephe(a, b, Z0, KF, n, kemer=True)
# the front: brick bays with arched windows, the stone-dressed centre with the giant door, quoins
mx0, mx1 = 0.62, 0.82
for (a, b) in ((V(FX0, FY0), V(mx0, FY0)), (V(mx1, FY0), V(FX1, FY0))):
    cephe(a, b, Z0, KF, 2, kemer=True)
y.kemerli(V(mx0, FY0), V(mx1, FY0), Z0, KF[0] + 0.05, (TUG, 'tugla_koyu', TS, 'ahsap'), v0=0.0, en=0.66, ust=0.03, derin=0.05, k_say=12, sivri=0,
          cerceve=(0.012, [TS, 'tas']))
duz_duvar(y, V(mx0, FY0), V(mx1, FY0), Z0 + KF[0] + 0.05, ZF, TUG)
silme(y, [V(mx0, FY0), V(mx1, FY0)], Z0, 0.022, 0.008, 'tas', 'kaide', kapali=False)
silme(y, [V(mx0, FY0), V(mx1, FY0)], ZF - 0.012, 0.014, 0.012, TS, 'tac', kapali=False)
# royal arms and a stone panel over the door
ra = V(0.72, FY0 - 0.0016, Z0 + KF[0] + 0.09)
y.yuz_yon([ra + V(-0.05, 0, -0.03), ra + V(0.05, 0, -0.03), ra + V(0.05, 0, 0.04), ra + V(-0.05, 0, 0.04)], TS, -Y)
y.yuz_yon([ra + V(-0.018, -0.001, 0.02), ra + V(0.018, -0.001, 0.02), ra + V(0.018, -0.001, -0.006), ra + V(0, -0.001, -0.022), ra + V(-0.018, -0.001, -0.006)], 'boya_kirmizi', -Y)
for s in (-1, 1):
    kure(y, (ra.x + s * 0.03, ra.y - 0.004, ra.z), 0.01, 'altin', n=6, kat=3)
kure(y, (ra.x, ra.y - 0.004, ra.z + 0.03), 0.008, 'altin', n=6, kat=3)
# stone quoins at the corners and at the centre bay
for (qx, qy) in ((FX0, FY0), (FX1, FY0), (FX0, FY1), (FX1, FY1), (mx0, FY0), (mx1, FY0)):
    for q in range(int((ZF - Z0 - 0.03) / 0.034)):
        s = 0.03 if q % 2 == 0 else 0.02
        kutu_merkez(y, (qx, qy), s, s if qy == FY1 or qx in (FX0, FX1) else 0.012, 0.03, TS, z0=Z0 + 0.025 + q * 0.034)
# a pediment over the centre bay
zp2 = alinlik(y, V(mx0 - 0.01, FY0 - 0.006), V(mx1 + 0.01, FY0 - 0.006), ZF + 0.002, 0.08, derin=0.1, key=TS, ic_key=TUG, c=0.008, cati_key=CATI)
y.oculus(V(0.72, FY0 - 0.006, ZF + 0.035), X, -Y, 0.016, 'koyu', TS, f=0.005, k=12)
# the hipped roof, the louvred lantern, furnace stacks
zr_f = cati_kirma(y, FX0, FX1, FY0, FY1, ZF, 0.2, 0.02, CATI, mahya='kursun', kalinlik=0.008, alt_key=TS, ns=4, nr=4, mahya_en=0.009)
LX, LY = (FX0 + FX1) / 2, (FY0 + FY1) / 2
kutu_merkez(y, (LX, LY), 0.14, 0.14, zr_f - ZF + 0.03, 'beyaz', z0=ZF + 0.05)
zl = zr_f + 0.08
for a, b in kenarlar(LX - 0.07, LX + 0.07, LY - 0.07, LY + 0.07):
    a2, b2, L, e, nc = eksen(a, b)
    for k in range(2):
        p, q = a2.lerp(b2, k / 2), a2.lerp(b2, (k + 1) / 2)
        y.kemerli(p, q, zr_f, 0.08, ('beyaz', 'ahsap_acik', 'beyaz', 'koyu'), v0=0.008, en=0.6, ust=0.008, derin=0.008, k_say=6, sivri=0)
        for zz in (zr_f + 0.025, zr_f + 0.045):   # louvre boards
            m = p.lerp(q, 0.5) - nc * 0.004
            cubuk3(y, m - e * 0.017 + Z * zz, m + e * 0.017 + Z * zz, 0.004, 'beyaz', nc, 0.003)
silme(y, dikdortgen(LX - 0.07, LX + 0.07, LY - 0.07, LY + 0.07), zl, 0.01, 0.01, TS, 'tac')
donel(y, (LX, LY), [(0.085, zl + 0.01), (0.07, zl + 0.03), (0.04, zl + 0.06), (0.012, zl + 0.08), (0.0, zl + 0.09)], 'kursun', n=4, kat=math.pi / 4)
kure(y, (LX, LY, zl + 0.096), 0.01, 'altin', n=6, kat=3)
for (bx, by) in ((FX0 + 0.1, FY1 - 0.12), (FX1 - 0.1, FY1 - 0.12)):
    kutu_merkez(y, (bx, by), 0.06, 0.06, 0.26, TUG, z0=ZF - 0.02)
    kutu_merkez(y, (bx, by), 0.07, 0.07, 0.012, TS, z0=ZF + 0.24)
    y.yuz_yon([V(p.x, p.y, ZF + 0.2525) for p in dikdortgen(bx - 0.022, bx + 0.022, by - 0.022, by + 0.022)], 'koyu', Z)
    for k in range(3):   # smoke
        kure(y, (bx + 0.01 * k, by + 0.02 * k, ZF + 0.29 + k * 0.05), 0.022 + 0.01 * k, 'granit', n=8, kat=4)
# the gun factory's tall tapering chimney
TX, TY = 1.1, 0.9
donel(y, (TX, TY), [(0.075, Z0), (0.075, Z0 + 0.05), (0.06, Z0 + 0.06), (0.05, Z0 + 0.92), (0.06, Z0 + 0.93), (0.06, Z0 + 0.95), (0.048, Z0 + 0.955)],
      TUG, n=4, kat=math.pi / 4)
y.yuz_yon([V(p.x, p.y, Z0 + 0.955) for p in cokgen((TX, TY), 0.048, 4, math.pi / 4)], 'koyu', Z)
for zz in (Z0 + 0.3, Z0 + 0.6):
    halka_kornis(y, (TX, TY), 0.056 if zz < 0.5 else 0.053, zz, 0.012, 0.006, 4, TS, kat=math.pi / 4)
for k in range(4):
    kure(y, (TX - 0.02 * k, TY + 0.02 * k, Z0 + 1.0 + k * 0.045), 0.03 + 0.012 * k, 'granit', n=8, kat=4)
# a furnace house against the chimney
blok(0.9, 1.04, 0.78, 1.02, (0.14,), (1, 0, 0, 1), cati='besik', cati_h=0.08)

# ---------------------------------------------------------------- the parade: guns, mortars, shot, the flagstaff, gunners
y.bolum('Tören alanı: toplar, havanlar, gülleler')
for r, yy in enumerate((-0.52, -0.7)):
    for k in range(6):
        x = -0.98 + k * 0.17 + (0.085 if r else 0)
        top_kizak(y, x, yy, Z0 + 0.001, -math.pi / 2, L=0.13, r=0.014, key='bronz' if (k + r) % 2 else 'demir')
for x in (-0.9, -0.56, -0.22):
    gulle_yigini(y, x + 0.085, -0.82, Z0 + 0.001, n=4, r=0.009)
for x in (0.2, 0.38):
    # a sea-service mortar on its bed
    kutu_merkez(y, (x, -0.6), 0.07, 0.06, 0.02, 'ahsap', z0=Z0 + 0.001)
    top_namlu(y, V(x, -0.595, Z0 + 0.03), V(0, -0.7, 0.7), 0.06, 0.02, 'demir')
    gulle_yigini(y, x, -0.7, Z0 + 0.001, n=3, r=0.012)
for k in range(4):   # stacks of powder barrels
    varil(y, 0.6 + k * 0.026, -0.48, Z0 + 0.001, 0.011, 0.028)
    if k < 3: varil(y, 0.613 + k * 0.026, -0.48, Z0 + 0.029, 0.011, 0.028)
for k in range(3):
    varil(y, 0.62 + k * 0.03, -0.54, Z0 + 0.001, 0.011, 0.028, yatik=0.0)
# gun barrels waiting on skids
for k in range(4):
    top_namlu(y, V(0.62 + k * 0.004, -0.66 - k * 0.035, Z0 + 0.016), V(1, 0, 0), 0.16, 0.014, 'bronz' if k % 2 else 'demir')
for x in (0.6, 0.78):
    kutu_merkez(y, (x + 0.01, -0.72), 0.012, 0.15, 0.006, 'ahsap', z0=Z0 + 0.001)
# the flagstaff with its cross-tree
FSX, FSY = 0.05, -0.62
for k, w in enumerate((0.09, 0.07, 0.05)):
    kutu_merkez(y, (FSX, FSY), w, w, 0.014, TS, z0=Z0 + k * 0.014)
cubuk(y, V(FSX - 0.06, FSY, Z0 + 0.46), V(FSX + 0.06, FSY, Z0 + 0.46), 0.004, 'beyaz')
for s in (-1, 1):
    cubuk(y, V(FSX + s * 0.058, FSY, Z0 + 0.46), V(FSX + s * 0.12, FSY, Z0 + 0.04), 0.0012, 'koyu')
sancak(y, FSX, FSY, Z0 + 0.042, boy=0.66, en=0.17, yuk=0.105, aci=math.pi * 0.95, direk_key='beyaz')
# the Guard House by the river gate (1788): a low brick block with a Tuscan portico and a pediment, a hipped roof,
# sentry boxes beside it, a gravel forecourt
y.bolum('Nöbetçi evi')
GHX0, GHX1, GHY0, GHY1 = 0.86, 1.12, -0.66, -0.47
yer(GHX0 - 0.03, GHX1 + 0.02, -0.8, GHY0, 'tas_koyu', 0.0024)
zgh, _ = blok(GHX0, GHX1, GHY0, GHY1, (0.13,), (3, 2, 3, 2), cati='kirma', cati_h=0.09, kemer=True, baca=[(GHX0 + 0.04, (GHY0 + GHY1) / 2)])
# the portico: four Tuscan columns on a stone step, an entablature and a pediment over them
pc0, pc1 = GHX0 + 0.05, GHX1 - 0.05
kutu(y, V(pc0 - 0.012, GHY0 - 0.07, Z0), X, pc1 - pc0 + 0.024, 0.07, 0.012, 'tas', 'onsagsolust')
kutu(y, V(pc0 - 0.02, GHY0 - 0.08, Z0), X, pc1 - pc0 + 0.04, 0.012, 0.006, TS, 'onsagsol')
for k in range(4):
    sutun(y, pc0 + (pc1 - pc0) * k / 3, GHY0 - 0.055, Z0 + 0.012, zgh - 0.012, 0.009, TS, 'toskan')
kutu3(y, V((pc0 + pc1) / 2, GHY0 - 0.035, zgh - 0.006), X, Y, Z, pc1 - pc0 + 0.03, 0.074, 0.016, TS, ('+x', '-x', '-y', '+z', '-z'))
alinlik(y, V(pc0 - 0.015, GHY0 - 0.072), V(pc1 + 0.015, GHY0 - 0.072), zgh + 0.002, 0.05, derin=0.075, key=TS, ic_key=TS, c=0.006, cati_key=CATI)
y.oculus(V((pc0 + pc1) / 2, GHY0 - 0.0725, zgh + 0.02), X, -Y, 0.009, 'koyu', TS, f=0.003, k=10)
for x in (GHX0 - 0.03, GHX1 + 0.005):   # sentry boxes (timber, painted, with little pitched tops)
    kutu_merkez(y, (x, GHY0 - 0.04), 0.03, 0.03, 0.065, 'boya_kirmizi', z0=Z0 + 0.0024)
    y.yuz_yon([V(x - 0.009, GHY0 - 0.0568, Z0 + 0.008), V(x + 0.009, GHY0 - 0.0568, Z0 + 0.008), V(x + 0.009, GHY0 - 0.0568, Z0 + 0.055),
               V(x - 0.009, GHY0 - 0.0568, Z0 + 0.055)], 'koyu', -Y)
    donel(y, (x, GHY0 - 0.04), [(0.024, Z0 + 0.067), (0.0, Z0 + 0.09)], 'kursun', n=4, kat=math.pi / 4)
    insan(y, x, GHY0 - 0.065, Z0 + 0.0024, 'boya_kirmizi', 1.05, aci=-math.pi / 2, sapka='koyu')
# gunners of the Royal Artillery (blue coats) and a red-coated sentry
rs = __import__('random').Random(4)
for k in range(14):
    x = -1.0 + (k % 7) * 0.17 + 0.04
    yy = -0.6 if k < 7 else -0.78
    insan(y, x, yy, Z0 + 0.001, 'lacivert', 1.05, aci=-math.pi / 2 + rs.uniform(-0.3, 0.3), sapka='koyu')
insan(y, -0.15, -0.88, Z0 + 0.001, 'boya_kirmizi', 1.1, aci=math.pi / 2, sapka='koyu', kol=1.0)
for (x, yy) in ((PX0 - 0.04, -0.9), (PX1 + 0.05, -0.92)):
    insan(y, x, yy, Z0, 'boya_kirmizi', 1.05, aci=math.pi / 2, sapka='koyu')
    cubuk(y, V(x + 0.006, yy, Z0 + 0.02), V(x + 0.006, yy, Z0 + 0.065), 0.0025, 'ahsap_koyu')
for (x, yy) in ((PX0 + 0.06, -1.1), (PX0 + 0.12, -1.05)):
    insan(y, x, yy, Z0 + 0.003, 'lacivert', 1.0, aci=rs.uniform(0, 6), sapka='koyu')

# ---------------------------------------------------------------- the foundry yard: carriages being built, a limber, wheels
y.bolum('Dökümhane avlusu')
yer(0.32, 1.15, -0.36, 0.05, 'zemin', 0.0012)
yer(0.6, 0.84, -0.36, 0.05, 'tas_koyu', 0.0024)          # the cart road to the great door


def araba(x, yy, aci, yuk=True):
    '''a two-wheeled ammunition cart with powder barrels'''
    with parca(y, (x, yy, Z0), aci):
        kutu3(y, V(0, 0, 0.04), X, Y, Z, 0.1, 0.05, 0.008, 'ahsap')
        for s in (-1, 1):
            kutu3(y, V(0, s * 0.024, 0.052), X, Y, Z, 0.1, 0.004, 0.02, 'ahsap_koyu')
            c = V(0, s * 0.033, 0.03)
            boru(y, [c - Y * 0.003, c + Y * 0.003], 0.03, 'ahsap_koyu', n=12)
            boru(y, [c - Y * 0.0035, c + Y * 0.0035], 0.006, 'demir', n=6)
        cubuk(y, V(0.05, 0.012, 0.04), V(0.16, 0.012, 0.025), 0.005, 'ahsap')
        cubuk(y, V(0.05, -0.012, 0.04), V(0.16, -0.012, 0.025), 0.005, 'ahsap')
    if yuk:
        for k in range(3):
            varil(y, x + math.cos(aci) * (k - 1) * 0.028, yy + math.sin(aci) * (k - 1) * 0.028, Z0 + 0.044, 0.01, 0.024)


araba(0.45, -0.2, 0.3)
araba(0.95, -0.12, 2.6, yuk=False)
for k in range(2):   # new carriages
    top_kizak(y, 0.5 + k * 0.12, -0.05 + 0.0, Z0 + 0.0024, -math.pi / 2, L=0.0001 + 0.14, r=0.015, key='bronz')
for k in range(4):   # a stack of carriage wheels
    c = V(1.02, -0.26, Z0 + 0.004 + k * 0.007)
    y.prizma((c.x, c.y), 0.03, c.z, c.z + 0.006, 'ahsap_koyu', n=12)
for (x, yy, k) in ((0.7, -0.2, 'lacivert'), (0.74, -0.18, 'lacivert'), (0.9, -0.3, 'koyu'), (1.05, -0.05, 'lacivert')):
    insan(y, x, yy, Z0 + 0.0024, k, 1.05, aci=rs.uniform(0, 6), sapka='koyu')

# ---------------------------------------------------------------- the back: storehouses, timber, guns waiting
y.bolum('Ambarlar ve kereste')
blok(-1.0, 0.3, 0.85, 1.08, (0.13,), (6, 1, 0, 1), cati='besik', cati_h=0.1)
for k in range(3):
    kereste(y, 0.48 + k * 0.17, 0.88, Z0, L=0.15, n=3, kat=3, en=0.014, aci=0.0)
for k in range(5):
    top_namlu(y, V(0.42 + k * 0.03, 1.0 + (k % 2) * 0.004, Z0 + 0.016), V(0, -1, 0), 0.0001 + 0.13, 0.013, 'demir')
for (x, yy) in ((-1.12, -0.2), (-1.12, 0.2), (-1.12, 0.6), (-1.1, 1.0), (0.35, 0.45)):
    agac(y, x, yy, Z0, boy=0.13)

calistir(y, 'lm_woolwich')
