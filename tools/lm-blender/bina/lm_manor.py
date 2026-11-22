# Malikane (lm_manor): a Tudor manor house. An E-plan house (stone ground floor, jettied close-studded upper storey,
# steep tiled roofs with dormers, a three-storey porch, two-storey bay windows, clusters of twisted brick chimneys)
# behind a walled court entered through a brick gatehouse with octagonal turrets (the banner); the stable with its
# cupola and a paddock, a round dovecote, a knot garden and a clipped hedge maze, an orchard and a fishpond.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from ingiliz_ortak import *
from bina_ortak import calistir
import doku

y = Yapi()
G = 0.03
doku.KOSE_RENK['cimen'] = cayir_renk(G)
XA, XB, YA, YB = -1.2, 1.2, -1.0, 1.0
Z1 = G + 0.17           # ground floor top = the jetty
ZU = Z1 + 0.15          # upper storey top = the eaves
JT = 0.024              # the jetty's overhang
HX = 0.33               # the hall range's ends (the wings' inner walls)
HY0, HY1 = 0.25, 0.5    # the hall's ground front and back
WX = 0.57               # the wings' outer walls
WY0 = -0.15             # the wings' ground fronts
TAS, SIVA, AHS = 'tas', 'siva', 'ahsap_koyu'
CATI, CATI2 = 'kiremit', 'kiremit2'


def sirala(a, b, dis):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized()
    return (a, b) if V(e.y, -e.x).dot(V(dis[0], dis[1])) > 0 else (b, a)


def tas_duvar(a, b, dis, pencereler, z0=G, z1=Z1, hood=True):
    """a stone ground-floor wall facing dis with mullioned windows [(u, w, v0, v1)] (u measured from the lower x / y
    end); returns the openings"""
    a2, b2 = sirala(a, b, dis)
    ters = (a2 - V(a[0], a[1])).length > 1e-9
    ps = [((1 - u) if ters else u, w, v0, v1) for (u, w, v0, v1) in pencereler]
    acs = acikli_duvar(y, a2, b2, z0, z1, ps, (TAS, 'tas_koyu', 'tas_acik', 'cam'), derin=0.014, cerceve=(0.005, 'tas_acik'))
    for ac in acs:
        tudor_pencere(y, ac, z0, 0.014, 'tas_acik', hood=hood)
    return acs


def ust_duvar(a, b, dis, pencereler, z0=Z1, z1=ZU, ek_bos=()):
    a2, b2 = sirala(a, b, dis)
    ters = (a2 - V(a[0], a[1])).length > 1e-9
    ps = [((1 - u) if ters else u, w, v0, v1) for (u, w, v0, v1) in pencereler]
    eb = [((1 - u) if ters else u, w) for (u, w) in ek_bos]
    return ahsap_kat(y, a2, b2, z0, z1, ps, SIVA, AHS, aralik=0.024, ek_bos=eb)


def kirislik(pts_dis, pts_ic, z, yon_listesi):
    """a jetty: the soffit between the upper storey's outline and the ground floor's, the bressumer along the upper
    line and joist ends under it"""
    y.yuz_yon([V(p.x, p.y, z) for p in pts_dis + pts_ic[::-1]], AHS, -Z)


def bressumer(a, b, dis):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    d = V(dis[0], dis[1])
    cubuk(y, a + d * 0.004 + Z * (Z1 + 0.004), b + d * 0.004 + Z * (Z1 + 0.004), 0.012, AHS, 0.01)
    L = (b - a).length
    n = int(L / 0.028)
    for k in range(1, n):
        p = a.lerp(b, k / n) - d * 0.012
        kutu_merkez(y, (p.x, p.y), 0.008 if abs(d.y) > 0.5 else 0.034, 0.034 if abs(d.y) > 0.5 else 0.008, 0.008, AHS, z0=Z1 - 0.008)


def kalkan_sus(xc, yg, wb, z, h, sacak, us, dis):
    """the gable's dressing (gable on the plane y = yg facing dis.y): close studs under the roof line, a collar, a
    carved bargeboard under each verge and a pendant finial at the apex"""
    s = 1 if dis > 0 else -1
    b = wb + sacak
    yp = yg + s * 0.003
    alt = lambda dx: z + h * (1 - abs(dx) / b) - 0.012
    n = int(2 * wb / 0.024)
    for k in range(1, n):
        dx = -wb + 2 * wb * k / n
        zt = alt(dx) - 0.004
        if zt - z > 0.012:
            cubuk(y, V(xc + dx, yp, z), V(xc + dx, yp, zt), 0.006, AHS, 0.004)
    zc = z + h * 0.42
    dxc = b * (1 - (zc + 0.016 - z) / h)
    cubuk(y, V(xc - dxc, yp, zc), V(xc + dxc, yp, zc), 0.007, AHS, 0.005)
    cubuk(y, V(xc - wb, yp, z + 0.004), V(xc + wb, yp, z + 0.004), 0.008, AHS, 0.005)
    # bargeboards
    yb = yg + s * (us - 0.004)
    for sg in (-1, 1):
        p0 = V(xc + sg * b, yb, alt(b) - 0.004)
        p1 = V(xc, yb, alt(0) - 0.004)
        cubuk(y, p0, p1, 0.004, AHS, 0.014)
    # pendant and finial
    pz = alt(0) + 0.012
    cubuk(y, V(xc, yb, pz - 0.05), V(xc, yb, pz + 0.04), 0.008, AHS)
    kure(y, (xc, yb, pz - 0.052), 0.006, AHS, n=6, kat=3)
    kure(y, (xc, yb, pz + 0.044), 0.007, 'ahsap', n=6, kat=3)


# ---------------------------------------------------------------- ground
y.bolum('Zemin')
zemin_blok(y, XA, XB, YA, YB, G)
# the gravel court, the flagged path from the gate to the porch, the drive out to the road
y.yuz_yon([V(-0.55, -0.72, G + 0.002), V(0.55, -0.72, G + 0.002), V(0.55, WY0, G + 0.002), V(-0.55, WY0, G + 0.002)], 'zemin', Z)
y.yuz_yon([V(-0.33, WY0, G + 0.002), V(0.33, WY0, G + 0.002), V(0.33, 0.12, G + 0.002), V(-0.33, 0.12, G + 0.002)], 'zemin', Z)
y.yuz_yon([V(-0.05, -0.72, G + 0.004), V(0.05, -0.72, G + 0.004), V(0.05, 0.12, G + 0.004), V(-0.05, 0.12, G + 0.004)], 'tas_acik', Z)
y.yuz_yon([V(-0.07, YA + 0.002, G + 0.003), V(0.07, YA + 0.002, G + 0.003), V(0.07, -0.8, G + 0.003), V(-0.07, -0.8, G + 0.003)], 'toprak', Z)
# lawns in the court with a sundial
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.1, sx * 0.45))
    zz = G + 0.006
    y.yuz_yon([V(x0, -0.62, zz), V(x1, -0.62, zz), V(x1, -0.25, zz), V(x0, -0.25, zz)], 'cimen', Z)
    duvarlar(y, dikdortgen(x0, x1, -0.62, -0.25), G + 0.002, zz, 'tas_acik')
cx_, cy_ = -0.275 * 1, -0.435
for sx in (-1, 1):
    donel(y, (sx * 0.275, cy_), [(0.0, G + 0.006), (0.016, G + 0.006), (0.016, G + 0.012), (0.008, G + 0.016), (0.006, G + 0.05), (0.011, G + 0.054),
                                (0.011, G + 0.058), (0.0, G + 0.058)], 'tas_acik', n=10)
    y.yuz_yon([V(sx * 0.275 - 0.001, cy_ - 0.008, G + 0.058), V(sx * 0.275 + 0.001, cy_ - 0.008, G + 0.058), V(sx * 0.275 + 0.001, cy_ + 0.006, G + 0.068)], 'bronz', X)
    y.yuz_yon([V(sx * 0.275 - 0.001, cy_ - 0.008, G + 0.058), V(sx * 0.275 + 0.001, cy_ - 0.008, G + 0.058), V(sx * 0.275 - 0.001, cy_ + 0.006, G + 0.068)], 'bronz', -X)

# ---------------------------------------------------------------- the house: plinth
y.bolum('Malikane: taban ve taş zemin kat')
PL = [V(-WX, WY0), V(-HX, WY0), V(-HX, HY0), V(-0.07, HY0), V(-0.07, 0.12), V(0.07, 0.12), V(0.07, HY0), V(HX, HY0), V(HX, WY0), V(WX, WY0),
      V(WX, HY1), V(-WX, HY1)]
silme(y, PL, G, 0.024, 0.008, 'granit', 'kaide')

# wings: ground floor
for sx in (-1, 1):
    xi, xo = sx * HX, sx * WX
    xc = (xi + xo) / 2
    # front (the two-storey bay in the middle)
    tas_duvar(V(xi, WY0), V(xo, WY0), (0, -1), [])
    # outer side: two windows, the chimney between
    tas_duvar(V(xo, WY0), V(xo, HY1), (sx, 0), [(0.2, 0.09, 0.05, 0.135), (0.84, 0.09, 0.05, 0.135)])
    # inner side, towards the court
    tas_duvar(V(xi, WY0), V(xi, HY0), (-sx, 0), [(0.45, 0.08, 0.05, 0.135)])
    # back
    tas_duvar(V(xi, HY1), V(xo, HY1), (0, 1), [(0.5, 0.08, 0.05, 0.135)])
    a_, b_ = sirala(V(xc - 0.085, WY0), V(xc + 0.085, WY0), (0, -1))
    cumba(y, (a_ + b_) / 2, (b_ - a_), G + 0.006, Z1 - G - 0.006, 0.17, 0.05, TAS, 'tas_koyu', 'cam', 'tas_acik', 'kursun', parapet=False,
          n_on=4, v0=0.03, v1=Z1 - G - 0.03)

# hall: ground floor front (two tall windows on the screens side, the great bay window at the dais end) and back
y.bolum('Malikane: büyük salon')
tas_duvar(V(-HX, HY0), V(HX, HY0), (0, -1), [(0.14, 0.08, 0.035, 0.145), (0.31, 0.06, 0.035, 0.145)])
tas_duvar(V(-HX, HY1), V(HX, HY1), (0, 1), [(0.12, 0.07, 0.05, 0.14), (0.5, 0.07, 0.05, 0.14), (0.7, 0.07, 0.05, 0.14), (0.88, 0.07, 0.05, 0.14)])
a_, b_ = sirala(V(0.13, HY0), V(0.29, HY0), (0, -1))
cumba(y, (a_ + b_) / 2, (b_ - a_), G + 0.006, Z1 - G + 0.006, 0.16, 0.06, TAS, 'tas_koyu', 'cam', 'tas_acik', 'kursun', parapet=True, n_on=4,
      v0=0.028, v1=Z1 - G - 0.02)

# the porch: three storeys, a four-centred arched door with the arms over it
y.bolum('Malikane: giriş kulesi (porch)')
PX, PY0 = 0.07, 0.12
kapi(y, *sirala(V(-PX, PY0), V(PX, PY0), (0, -1)), G, 0.55, Z1 - G - 0.03, (TAS, 'tas_koyu', 'tas_acik', 'ahsap'), sivri=0.22, derin=0.02,
     cerceve=(0.007, 'tas_acik'))
duz_duvar(y, *sirala(V(-PX, PY0), V(PX, PY0), (0, -1)), Z1 - 0.03, Z1, TAS)
for sx in (-1, 1):
    tas_duvar(V(sx * PX, PY0), V(sx * PX, HY0), (sx, 0), [(0.5, 0.04, 0.06, 0.12)], hood=False)
# the arms panel over the door: a Tudor rose
kutu3(y, V(0, PY0 - 0.004, Z1 - 0.016), X, Y, Z, 0.07, 0.008, 0.024, 'tas_acik')
for r_, key in ((0.009, 'boya_kirmizi'), (0.005, 'beyaz'), (0.002, 'altin')):
    y.yuz_yon([V(p.x, PY0 - 0.0082 - (0.009 - r_) * 0.1, p.z) for p in [V(0 + r_ * math.cos(TAU * i / 10), 0, Z1 - 0.016 + r_ * math.sin(TAU * i / 10)) for i in range(10)]],
              key, -Y)
ZP = ZU + 0.06
ust_duvar(V(-PX, PY0), V(PX, PY0), (0, -1), [(0.5, 0.075, 0.04, 0.115)], Z1, ZU)
ust_duvar(V(-PX, PY0), V(PX, PY0), (0, -1), [(0.5, 0.05, 0.012, 0.048)], ZU, ZP)
for sx in (-1, 1):
    ust_duvar(V(sx * PX, PY0), V(sx * PX, 0.27), (sx, 0), [(0.3, 0.035, 0.05, 0.11)], Z1, ZU)
    ust_duvar(V(sx * PX, PY0), V(sx * PX, 0.27), (sx, 0), [], ZU, ZP)
cubuk(y, V(-PX - 0.002, PY0 - 0.004, Z1 + 0.004), V(PX + 0.002, PY0 - 0.004, Z1 + 0.004), 0.012, AHS, 0.01)
cati_besik(y, -PX, PX, PY0, 0.355, ZP, 0.075, 0.016, CATI, CATI2, ucluk_key=SIVA, uc_sacak=0.016, ns=4, nr=5, mahya_en=0.009)
kalkan_sus(0, PY0, PX, ZP, 0.075, 0.016, 0.016, -1)

# ---------------------------------------------------------------- upper storey (close-studded, jettied)
y.bolum('Malikane: çıkmalı ahşap üst kat')
for sx in (-1, 1):
    xi, xo, xoj = sx * HX, sx * WX, sx * (WX + JT)
    yf = WY0 - JT
    xc = (xi + xoj) / 2
    ust_duvar(V(xi, yf), V(xoj, yf), (0, -1), [], ek_bos=[(abs(xc - xi) / abs(xoj - xi), 0.2)])
    ust_duvar(V(xoj, yf), V(xoj, HY1), (sx, 0), [(0.14, 0.1, 0.035, 0.11), (0.34, 0.06, 0.035, 0.11), (0.86, 0.1, 0.035, 0.11)],
              ek_bos=[(0.53, 0.12)])
    ust_duvar(V(xi, yf), V(xi, HY0 - JT), (-sx, 0), [(0.45, 0.1, 0.035, 0.11)])
    ust_duvar(V(xi, HY1), V(xoj, HY1), (0, 1), [(0.5, 0.09, 0.035, 0.11)])
    # the jetty: soffit, bressumers, joist ends; a dragon bracket at the corner
    y.yuz_yon([V(xi, yf, Z1), V(xoj, yf, Z1), V(xoj, HY1, Z1), V(xo, HY1, Z1), V(xo, WY0, Z1), V(xi, WY0, Z1)], AHS, -Z)
    bressumer(V(xi, yf), V(xoj, yf), (0, -1))
    bressumer(V(xoj, yf), V(xoj, HY1), (sx, 0))
    cubuk(y, V(xo, WY0, Z1 - 0.05), V(xoj - sx * 0.004, yf + 0.004, Z1 - 0.004), 0.008, AHS, 0.008)
    # the oriel over the bay
    a_, b_ = sirala(V(xc - 0.09, yf), V(xc + 0.09, yf), (0, -1))
    cumba(y, (a_ + b_) / 2, (b_ - a_), Z1 + 0.002, 0.11, 0.18, 0.04, SIVA, AHS, 'cam', AHS, 'kursun', parapet=False, n_on=4, v0=0.014, v1=0.1,
          ahsap=True, taban=AHS)
    # the roof and its gables
    x0, x1 = sorted((xi, xoj))
    cati_besik(y, x0, x1, yf, HY1, ZU, 0.23, 0.022, CATI, CATI2, ucluk_key=SIVA, uc_sacak=0.02, ns=6, nr=7, mahya_en=0.011)
    wb = (x1 - x0) / 2
    kalkan_sus(xc, yf, wb, ZU, 0.23, 0.022, 0.02, -1)
    kalkan_sus(xc, HY1, wb, ZU, 0.23, 0.022, 0.02, 1)
    # a window in the front gable
    acs = acikli_duvar(y, *sirala(V(xc - 0.03, yf - 0.0035), V(xc + 0.03, yf - 0.0035), (0, -1)), ZU + 0.03, ZU + 0.08, [(0.5, 0.05, 0.004, 0.046)],
                       (SIVA, AHS, 'ahsap_acik', 'cam'), derin=0.006, pay=0.002)
    for ac in acs:
        tudor_pencere(y, ac, ZU + 0.03, 0.006, AHS, hood=False, transom=False)

# hall: upper storey
yh = HY0 - JT
ust_duvar(V(-HX, yh), V(HX, yh), (0, -1), [(0.13, 0.11, 0.035, 0.11), (0.31, 0.06, 0.035, 0.11), (0.7, 0.07, 0.035, 0.11), (0.87, 0.1, 0.035, 0.11)])
ust_duvar(V(-HX, HY1), V(HX, HY1), (0, 1), [(0.3, 0.09, 0.035, 0.11), (0.72, 0.09, 0.035, 0.11)], ek_bos=[(0.27, 0.13)])
y.yuz_yon([V(-HX, yh, Z1), V(HX, yh, Z1), V(HX, HY0, Z1), V(-HX, HY0, Z1)], AHS, -Z)
bressumer(V(-HX, yh), V(HX, yh), (0, -1))

y.bolum('Malikane: çatılar ve çatı pencereleri')
HR = 0.17
cati_besik(y, -(HX + JT / 2 + 0.12), HX + JT / 2 + 0.12, yh, HY1 - 0.019, ZU, HR, 0.022, CATI, CATI2, ucluk_key=SIVA, uc_sacak=0.0, ns=10, nr=6, mahya_en=0.011)
# gabled dormers on the hall's front slope
for dx in (-0.2, 0.2):
    w2 = 0.045
    k_ = [V(dx - w2, yh), V(dx + w2, yh)]
    ust_duvar(V(dx - w2, yh), V(dx + w2, yh), (0, -1), [(0.5, 0.05, 0.012, 0.058)], ZU, ZU + 0.075)
    for s in (-1, 1):
        duz_duvar(y, *sirala(V(dx + s * w2, yh), V(dx + s * w2, yh + 0.1), (s, 0)), ZU, ZU + 0.075, SIVA)
    cati_besik(y, dx - w2, dx + w2, yh, yh + 0.13, ZU + 0.075, 0.055, 0.012, CATI, CATI2, ucluk_key=SIVA, uc_sacak=0.012, ns=3, nr=4, mahya_en=0.008)
    kalkan_sus(dx, yh, w2, ZU + 0.075, 0.055, 0.012, 0.012, -1)

# the great hall's louvre on the ridge: a hexagonal timber lantern, a lead cap and a vane
LC = V(-0.1, (yh + HY1 - 0.019) / 2)
zl = ZU + HR - 0.02
k6 = cokgen(LC, 0.034, 6, math.pi / 6)
duvarlar(y, k6, zl - 0.03, zl + 0.012, 'ahsap_dikey')
for i in range(6):
    y.kemerli(k6[i], k6[(i + 1) % 6], zl + 0.012, 0.05, ('ahsap_dikey', AHS, 'ahsap', 'koyu'), v0=0.006, en=0.62, ust=0.008, derin=0.006, k_say=6, sivri=0.4)
    a_, b_, L_, e_, n_ = eksen(k6[i], k6[(i + 1) % 6])
    for j in range(3):
        kutu3(y, a_.lerp(b_, 0.5) - n_ * 0.003 + Z * (zl + 0.026 + j * 0.011), e_, n_, Z, L_ * 0.55, 0.003, 0.004, AHS, ('+y', '+z'))
halka_kornis(y, LC, 0.034, zl + 0.058, 0.006, 0.006, 6, AHS, kat=math.pi / 6)
lt = donel(y, LC, [(0.042, zl + 0.064), (0.03, zl + 0.08), (0.012, zl + 0.1), (0.0, zl + 0.112)], 'kursun', n=6, kat=math.pi / 6)
y.yuz_yon([V(p.x, p.y, zl + 0.064) for p in cokgen(LC, 0.042, 6, math.pi / 6)], AHS, -Z)
y.prizma((LC.x, LC.y), 0.002, lt.z - 0.004, lt.z + 0.05, 'altin', n=4)
kure(y, (LC.x, LC.y, lt.z + 0.012), 0.005, 'altin', n=6, kat=3)
levha(y, [V(LC.x, LC.y, lt.z + 0.028), V(LC.x + 0.03, LC.y, lt.z + 0.022), V(LC.x + 0.03, LC.y, lt.z + 0.036)], 'altin', Y, 0.0015)

# ---------------------------------------------------------------- chimneys
y.bolum('Malikane: burgulu tuğla bacalar')
for sx in (-1, 1):
    xo = sx * WX
    # an external stack on the wing's outer side: a wide breast below, set-offs, the shafts above the ridge
    yc = 0.165
    kutu_merkez(y, (xo + sx * 0.04, yc), 0.08, 0.13, Z1 - G, 'tugla', z0=G)
    y.yuz_yon([V(xo + sx * 0.08, yc - 0.065, Z1), V(xo + sx * 0.08, yc + 0.065, Z1), V(xo + sx * 0.064, yc + 0.065, Z1 + 0.02),
               V(xo + sx * 0.064, yc - 0.065, Z1 + 0.02)], 'tas_acik', V(sx, 0, 1))
    for s in (-1, 1):
        y.yuz_yon([V(xo + sx * 0.064, yc + s * 0.065, Z1), V(xo + sx * 0.08, yc + s * 0.065, Z1), V(xo + sx * 0.064, yc + s * 0.065, Z1 + 0.02)], 'tugla', V(0, s))
    kutu_merkez(y, (xo + sx * 0.044, yc), 0.04 + 0.002, 0.11, ZU + 0.235 - Z1, 'tugla', z0=Z1)
    for zz in (Z1 + 0.06, ZU + 0.02):
        silme(y, dikdortgen(xo + sx * 0.044 - 0.021, xo + sx * 0.044 + 0.021, yc - 0.055, yc + 0.055), zz, 0.01, 0.005, 'tas_acik', 'duz')
    for k in range(3):   # diaper lozenges in darker brick
        c = V(xo + sx * 0.0652, yc, Z1 + 0.1 + k * 0.05)
        y.yuz_yon([c - Z * 0.014, c + V(0, 0.012), c + Z * 0.014, c - V(0, 0.012)], 'tugla_koyu', V(sx, 0))
    baca(y, xo + sx * 0.044, yc, ZU + 0.18, ZU + 0.235, 0.11, 0.044, 3, 0.11, aci=math.pi / 2)
# the hall's back stack
kutu_merkez(y, (-0.15, HY1 + 0.03), 0.14, 0.06, Z1 - G, 'tugla', z0=G)
kutu_merkez(y, (-0.15, HY1 + 0.026), 0.11, 0.052, ZU + HR + 0.02 - Z1, 'tugla', z0=Z1)
baca(y, -0.15, HY1 + 0.026, ZU + HR - 0.02, ZU + HR + 0.02, 0.11, 0.052, 3, 0.1)
# a ridge stack on the hall
baca(y, 0.1, (yh + HY1) / 2, ZU + 0.05, ZU + HR + 0.035, 0.09, 0.05, 2, 0.1)

# ---------------------------------------------------------------- the court wall and the gatehouse
y.bolum('Avlu duvarı')
CW = 0.55
GY0, GY1 = -0.80, -0.64
GXW = 0.15
CY = -0.72
for sx in (-1, 1):
    # brick wall (outer face on the right of travel), stone coping
    yol = [V(sx * (GXW - 0.005), CY - 0.012), V(sx * (CW + 0.012), CY - 0.012), V(sx * (CW + 0.012), WY0 - 0.002)]
    if sx < 0: yol = yol[::-1]
    alcak_duvar(y, yol, G, 0.075, 0.024, 'tugla', 'tugla')
    # coping and piers
    pts = [V(sx * (GXW - 0.005), CY), V(sx * CW, CY), V(sx * CW, WY0)]
    for i in range(2):
        a, b = pts[i], pts[i + 1]
        L = (b - a).length
        n = max(1, int(L / 0.1))
        for k in range(n + 1):
            p = a.lerp(b, k / n)
            if i == 1 and k == 0: continue
            kutu_merkez(y, (p.x, p.y), 0.036, 0.036, 0.094, 'tugla', z0=G)
            kutu_merkez(y, (p.x, p.y), 0.044, 0.044, 0.008, 'tas_acik', z0=G + 0.094)
            kure(y, (p.x, p.y, G + 0.112), 0.01, 'tas_acik', n=8, kat=4)
    for i in range(2):
        a, b = pts[i], pts[i + 1]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        kutu3(y, a.lerp(b, 0.5) + Z * (G + 0.079), e, nn, Z, (b - a).length, 0.03, 0.008, 'tas_acik', ('+x', '-x', '+y', '-y', '+z', '-z'))

y.bolum('Kapı evi: tuğla, sekizgen kuleli')
ZGT = G + 0.5
gk = dikdortgen(-GXW, GXW, GY0, GY1)
# front and back with the four-centred archway, doors open inside
for (a, b) in ((V(-GXW, GY0), V(GXW, GY0)), (V(GXW, GY1), V(-GXW, GY1))):
    y.kemerli(a, b, G, 0.24, ('tugla', 'tas_koyu', 'tas_acik', 'koyu'), v0=0.0, en=0.42, ust=0.05, derin=0.04, k_say=10, sivri=0.22,
              cerceve=(0.01, ['tas_acik', 'tas']))
    duz_duvar(y, a, b, G + 0.24, ZGT, 'tugla')
for (a, b) in ((V(GXW, GY0), V(GXW, GY1)), (V(-GXW, GY1), V(-GXW, GY0))):
    acs = acikli_duvar(y, a, b, G, ZGT, [(0.5, 0.05, 0.3, 0.38)], ('tugla', 'tas_koyu', 'tas_acik', 'cam'), derin=0.012, cerceve=(0.005, 'tas_acik'))
    for ac in acs: tudor_pencere(y, ac, G, 0.012, 'tas_acik')
# the passage's walls and vault beyond the doors
y.yuz_yon([V(-0.03, GY0 + 0.04, G + 0.001), V(0.03, GY0 + 0.04, G + 0.001), V(0.03, GY1 - 0.04, G + 0.001), V(-0.03, GY1 - 0.04, G + 0.001)], 'tas_koyu', Z)
# the gate front: an oriel over the arch, the arms, diaper patterning, string courses
cumba(y, (0, GY0), (1, 0), G + 0.27, 0.13, 0.15, 0.04, 'tas_acik', 'tas_koyu', 'cam', 'tas_acik', 'kursun', parapet=True, n_on=4,
      v0=0.014, v1=0.112, alt='tas_acik')
kutu3(y, V(0, GY0 - 0.003, G + 0.44), X, Y, Z, 0.08, 0.006, 0.05, 'tas_acik')
for r_, key in ((0.016, 'boya_kirmizi'), (0.009, 'beyaz'), (0.004, 'altin')):
    y.yuz_yon([V(r_ * math.cos(TAU * i / 12), GY0 - 0.0062 - (0.016 - r_) * 0.05, G + 0.44 + r_ * math.sin(TAU * i / 12)) for i in range(12)], key, -Y)
for zz in (G + 0.25, ZGT - 0.03):
    silme(y, gk, zz, 0.01, 0.007, 'tas_acik', 'duz')
# diaper: darker brick lozenges on the flanks
for (a, b) in ((V(GXW, GY0), V(GXW, GY1)), (V(-GXW, GY1), V(-GXW, GY0))):
    a, b, L, e, nc = eksen(a, b)
    for row in range(3):
        for k in range(2):
            c = a.lerp(b, (k + 0.5 + 0.5 * (row % 2)) / 2.5) + nc * 0.0015 + Z * (G + 0.07 + row * 0.07)
            q = [c - Z * 0.016, c + e * 0.014, c + Z * 0.016, c - e * 0.014]
            y.yuz_yon(q, 'tugla_koyu', nc)
silme(y, gk, ZGT - 0.004, 0.014, 0.01, 'tas_acik', 'tac')
parapet(y, disa(gk, 0.008), ZGT + 0.01, 0.012, 0.024, 0.014, 'tugla', ust_key='tas_acik')
y.yuz_yon([V(p.x, p.y, ZGT + 0.006) for p in gk], 'kursun', Z)
# the four octagonal turrets
for (tx, ty, hh) in ((-GXW, GY0, 0.68), (GXW, GY0, 0.68), (-GXW, GY1, 0.6), (GXW, GY1, 0.6)):
    r = 0.04
    zt = G + hh
    y.prizma((tx, ty), r, G, zt, 'tugla', n=8, ust=False, kat=math.pi / 8)
    for zz in (G + 0.25, ZGT - 0.03, zt - 0.05):
        halka_kornis(y, (tx, ty), r, zz, 0.01, 0.007, 8, 'tas_acik', kat=math.pi / 8)
    for zz in (G + 0.12, G + 0.36, zt - 0.12):
        a_ = math.atan2(ty, tx) + math.pi / 8 * 0
        nn = V(math.cos(math.atan2(ty - (GY0 + GY1) / 2, tx)), math.sin(math.atan2(ty - (GY0 + GY1) / 2, tx)))
        o = V(tx, ty) + nn * (r * math.cos(math.pi / 8) + 0.001)
        yarik(y, o + Z * 0, V(-nn.y, nn.x), nn, -0.004, zz, 0.008, 0.035, 'koyu')
    # a crenellated top and a lead ogee cupola with a gilded vane
    silme(y, cokgen((tx, ty), r, 8, math.pi / 8), zt - 0.01, 0.012, 0.008, 'tas_acik', 'tac')
    ring = cokgen((tx, ty), r + 0.008, 8, math.pi / 8)
    for i in range(8):
        mazgal(y, ring[i], ring[(i + 1) % 8], zt + 0.002, 0.016, 0.008, 'tugla', dis_en=0.014, bosluk=0.03)
    y.yuz_yon([V(p.x, p.y, zt + 0.002) for p in ring], 'kursun', Z)
    rr = r * 0.82
    top = donel(y, (tx, ty), [(rr, zt), (rr, zt + 0.03), (rr * 1.05, zt + 0.038), (rr * 0.95, zt + 0.06), (rr * 0.55, zt + 0.085), (rr * 0.22, zt + 0.105),
                              (0.004, zt + 0.125), (0.0, zt + 0.128)], 'kursun', n=8, kat=math.pi / 8, dilim=['kursun', 'kursun2'])
    y.prizma((tx, ty), 0.0025, top.z - 0.004, top.z + 0.04, 'altin', n=4)
    kure(y, (tx, ty, top.z + 0.012), 0.006, 'altin', n=6, kat=3)
    levha(y, [V(tx, ty, top.z + 0.022), V(tx + 0.03, ty, top.z + 0.022), V(tx + 0.03, ty, top.z + 0.036), V(tx, ty, top.z + 0.038)], 'altin', Y, 0.0015)
y.bolum('Sancak')
sancak(y, 0.0, (GY0 + GY1) / 2, ZGT + 0.006, boy=0.26, en=0.14, yuk=0.085, aci=math.pi * 0.15)

# ---------------------------------------------------------------- the stable with its cupola, the paddock
y.bolum('Ahır, kubbecik ve padok')
SX0, SX1, SY0, SY1 = -1.1, -0.86, -0.42, 0.38
ZS = G + 0.13
sk = dikdortgen(SX0, SX1, SY0, SY1)
# +x side: four stable doors and windows between
acs = acikli_duvar(y, V(SX1, SY0), V(SX1, SY1), G, ZS, [(0.12, 0.05, 0.0, 0.1), (0.37, 0.05, 0.0, 0.1), (0.63, 0.05, 0.0, 0.1), (0.88, 0.05, 0.0, 0.1),
                                                         (0.245, 0.035, 0.05, 0.095), (0.5, 0.035, 0.05, 0.095), (0.755, 0.035, 0.05, 0.095)],
                   ('tugla', AHS, 'tas_acik', 'koyu'), derin=0.012, cerceve=(0.005, 'tas_acik'))
for ac in acs:
    pa, pb, v0, v1, e, nc = ac
    if v0 == 0.0:
        # split doors: the lower leaf shut, a horse looking out over it
        w = (pb - pa).length
        kutu3(y, (pa + pb) / 2 - nc * 0.008 + Z * (G + 0.03), e, nc, Z, w, 0.006, 0.06, 'ahsap')
        for t in (0.25, 0.75):
            kutu3(y, (pa + pb) / 2 - nc * 0.0045 + Z * (G + 0.06 * t), e, nc, Z, w * 0.9, 0.002, 0.004, 'demir', ('+y', '+z', '-z', '+x', '-x'))
acikli_duvar(y, V(SX0, SY1), V(SX0, SY0), G, ZS, [(0.2, 0.035, 0.05, 0.095), (0.5, 0.035, 0.05, 0.095), (0.8, 0.035, 0.05, 0.095)],
             ('tugla', AHS, 'tas_acik', 'koyu'), derin=0.01)
acikli_duvar(y, V(SX0, SY0), V(SX1, SY0), G, ZS, [(0.5, 0.06, 0.0, 0.105)], ('tugla', AHS, 'tas_acik', 'ahsap_dikey'), derin=0.012, cerceve=(0.005, 'tas_acik'))
duz_duvar(y, V(SX1, SY1), V(SX0, SY1), G, ZS, 'tugla')
# the long back (seen from the approach): dark-brick pilasters between the bays, a stone band at sill height,
# hay-loft vents high up (a plain brick side read as an empty wall)
for u in (0.05, 0.35, 0.65, 0.95):
    yy = SY1 + (SY0 - SY1) * u
    kutu3(y, V(SX0 - 0.004, yy, (G + ZS) / 2), X, Y, Z, 0.008, 0.022, ZS - G, 'tugla_koyu', ('-x', '+y', '-y'))
    kutu3(y, V(SX0 - 0.007, yy, G + 0.012), X, Y, Z, 0.014, 0.028, 0.024, 'tas_acik', ('-x', '+y', '-y', '+z'))
for u in (0.2, 0.5, 0.8):
    yy = SY1 + (SY0 - SY1) * u
    for dz in (0.105, 0.113):
        kutu3(y, V(SX0 - 0.002, yy, G + dz), X, Y, Z, 0.004, 0.03, 0.004, 'ahsap_koyu', ('-x', '+z', '-z', '+y', '-y'))
silme(y, sk, G, 0.018, 0.006, 'granit', 'kaide')
silme(y, sk, ZS - 0.008, 0.008, 0.005, 'tas_acik', 'duz')
cati_besik(y, SX0, SX1, SY0, SY1, ZS, 0.15, 0.02, 'arduvaz', 'arduvaz', ucluk_key='ahsap_dikey', uc_sacak=0.016, ns=8, nr=6, mahya_en=0.01)
# the hayloft door in the front gable with its hoist beam
kutu3(y, V((SX0 + SX1) / 2, SY0 - 0.003, ZS + 0.04), X, Y, Z, 0.05, 0.004, 0.05, 'ahsap_koyu')
cubuk(y, V((SX0 + SX1) / 2, SY0 + 0.02, ZS + 0.088), V((SX0 + SX1) / 2, SY0 - 0.05, ZS + 0.088), 0.009, AHS)
boru(y, [V((SX0 + SX1) / 2, SY0 - 0.045, ZS + 0.084), V((SX0 + SX1) / 2, SY0 - 0.045, ZS + 0.02)], 0.0012, 'kumas', n=3)
# the cupola on the ridge: an open louvred lantern, a lead ogee cap, the vane
CX_, CY_ = (SX0 + SX1) / 2, -0.02
zr = ZS + 0.15
kutu_merkez(y, (CX_, CY_), 0.06, 0.06, 0.04, 'ahsap_dikey', z0=zr - 0.03)
kk = dikdortgen(CX_ - 0.03, CX_ + 0.03, CY_ - 0.03, CY_ + 0.03)
silme(y, kk, zr + 0.008, 0.006, 0.004, 'beyaz', 'duz')
for i in range(4):
    y.kemerli(kk[i], kk[(i + 1) % 4], zr + 0.014, 0.05, ('beyaz', 'ahsap_koyu', 'beyaz', 'koyu'), v0=0.006, en=0.6, ust=0.006, derin=0.006, k_say=6)
top = cati_kirma(y, CX_ - 0.03, CX_ + 0.03, CY_ - 0.03, CY_ + 0.03, zr + 0.064, 0.05, 0.008, 'kursun', 'kursun2', ns=3, nr=4, mahya_en=0.005)
y.prizma((CX_, CY_), 0.002, top - 0.004, top + 0.05, 'altin', n=4)
kure(y, (CX_, CY_, top + 0.01), 0.005, 'altin', n=6, kat=3)
levha(y, [V(CX_, CY_, top + 0.036), V(CX_, CY_ + 0.032, top + 0.03), V(CX_, CY_ + 0.032, top + 0.042)], 'altin', X, 0.0015)
cubuk(y, V(CX_ - 0.016, CY_, top + 0.024), V(CX_ + 0.016, CY_, top + 0.024), 0.0018, 'altin')
cubuk(y, V(CX_, CY_ - 0.016, top + 0.024), V(CX_, CY_ + 0.016, top + 0.024), 0.0018, 'altin')
# the stable yard: horses, a groom, a mounting block, a water trough
for k, (x, yy, a, key) in enumerate(((-0.78, -0.25, math.pi, 'ahsap'), (-0.74, 0.12, math.pi * 1.1, 'koyu'), (-0.8, 0.3, 0.2, 'beyaz'))):
    at(y, x, yy, G, a, 0.85, key, 'koyu' if key != 'koyu' else 'ahsap_koyu')
insan(y, -0.76, -0.17, G, 'boya_kirmizi', aci=math.pi, kol=0.6, sapka='kece')
kutu_merkez(y, (-0.82, -0.05), 0.03, 0.1, 0.02, 'granit', z0=G)
kutu_merkez(y, (-0.82, 0.2), 0.035, 0.12, 0.024, 'ahsap_koyu', z0=G)
y.yuz_yon([V(-0.835, 0.145, G + 0.02), V(-0.805, 0.145, G + 0.02), V(-0.805, 0.255, G + 0.02), V(-0.835, 0.255, G + 0.02)], 'su', Z)
# the paddock in front: a post-and-rail fence and grazing horses
PK = [V(-1.14, -0.96), V(-0.64, -0.96), V(-0.64, -0.56), V(-1.14, -0.56)]
for i in range(4):
    a, b = PK[i], PK[(i + 1) % 4]
    L = (b - a).length
    n = int(L / 0.06)
    for k in range(n + 1):
        p = a.lerp(b, k / n)
        if i == 1 and 0.4 < k / n < 0.6: continue
        cubuk(y, p + Z * G, p + Z * (G + 0.045), 0.007, AHS)
    for zz in (G + 0.02, G + 0.04):
        if i == 1:
            cubuk(y, a + Z * zz, a.lerp(b, 0.4) + Z * zz, 0.005, 'ahsap', 0.004)
            cubuk(y, a.lerp(b, 0.6) + Z * zz, b + Z * zz, 0.005, 'ahsap', 0.004)
        else:
            cubuk(y, a + Z * zz, b + Z * zz, 0.005, 'ahsap', 0.004)
at(y, -1.0, -0.82, G, 0.6, 0.85, 'ahsap_acik', 'ahsap_koyu')
at(y, -0.82, -0.7, G, 2.4, 0.85, 'kerpic_koyu', 'koyu')
at(y, -0.92, -0.62, G, -0.4, 0.75, 'beyaz', 'granit')

# ---------------------------------------------------------------- the dovecote
y.bolum('Güvercinlik')
DC, DR = V(0.9, 0.42), 0.075
ZD = G + 0.17
donel(y, (DC.x, DC.y), [(DR * 1.08, G), (DR, G + 0.02), (DR, ZD)], 'kirec', n=20)
halka_kornis(y, (DC.x, DC.y), DR, G + 0.09, 0.008, 0.006, 20, 'tas_acik')
halka_kornis(y, (DC.x, DC.y), DR, ZD - 0.01, 0.01, 0.008, 20, 'tas_acik', profil='tac')
# the door (facing -x) and flight holes in rows
for a in (math.pi + 0.0,):
    nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
    kutu3(y, DC + nn * (DR + 0.001) + Z * (G + 0.045), e, nn, Z, 0.032, 0.004, 0.07, 'ahsap')
    kutu3(y, DC + nn * (DR + 0.002) + Z * (G + 0.083), e, nn, Z, 0.04, 0.006, 0.006, 'tas_acik')
for row, zz in enumerate((G + 0.115, G + 0.14)):
    for k in range(9):
        a = TAU * (k + 0.5 * row) / 9 + 0.2
        nn = V(math.cos(a), math.sin(a))
        p = DC + nn * (DR + 0.0012) + Z * zz
        y.yuz_yon([p - V(-nn.y, nn.x) * 0.005 - Z * 0.005, p + V(-nn.y, nn.x) * 0.005 - Z * 0.005, p + V(-nn.y, nn.x) * 0.005 + Z * 0.004,
                   p - V(-nn.y, nn.x) * 0.005 + Z * 0.004], 'koyu', nn)
# the conical tiled roof and the open glover (lantern)
donel(y, (DC.x, DC.y), [(DR * 0.98, ZD), (DR + 0.02, ZD), (DR * 0.5, ZD + 0.07), (0.022, ZD + 0.1)], 'kiremit', n=20)
y.yuz_yon([V(p.x, p.y, ZD) for p in cokgen(DC, DR + 0.02, 20)], AHS, -Z)
for i in range(6):
    a = TAU * i / 6
    p = DC + V(math.cos(a), math.sin(a)) * 0.018
    cubuk(y, p + Z * (ZD + 0.098), p + Z * (ZD + 0.13), 0.004, 'ahsap')
y.yuz_yon([V(p.x, p.y, ZD + 0.1) for p in cokgen(DC, 0.022, 6)], 'koyu', Z)
donel(y, (DC.x, DC.y), [(0.0, ZD + 0.128), (0.028, ZD + 0.128), (0.018, ZD + 0.145), (0.0, ZD + 0.158)], 'kursun', n=8)
y.prizma((DC.x, DC.y), 0.002, ZD + 0.155, ZD + 0.18, 'altin', n=4)
# pigeons on the roof and the ground
for k, (a, r_, zz) in enumerate(((0.4, 0.06, ZD + 0.03), (2.1, 0.05, ZD + 0.045), (4.0, 0.065, ZD + 0.022), (0.3, 0.11, G), (0.7, 0.12, G),
                                 (5.6, 0.12, G))):
    p = DC + V(math.cos(a), math.sin(a)) * r_
    with parca(y, (p.x, p.y, zz), a + 1.4):
        kure(y, (0, 0, 0.005), 0.005, 'beyaz' if k % 2 else 'granit', n=6, kat=3)
        kure(y, (0.005, 0, 0.009), 0.003, 'beyaz' if k % 2 else 'granit', n=5, kat=3)

# ---------------------------------------------------------------- knot garden and maze
y.bolum('Düğüm bahçesi ve budanmış çit labirenti')
ZG_ = G + 0.003


def bahce_cerceve(x0, x1, y0, y1):
    y.yuz_yon([V(x0, y0, ZG_), V(x1, y0, ZG_), V(x1, y1, ZG_), V(x0, y1, ZG_)], 'zemin', Z)
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, G, ZG_, 'tas_acik')
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        p, q = a - nn * 0.012 + e * 0.012, b - nn * 0.012 - e * 0.012
        if i == 3 or i == 2:   # a gap for the path in the left (-x) side and the back
            m = p.lerp(q, 0.5)
            cit(y, p, m - e * 0.03, 0.035, 0.022, 'yesil_koyu', ZG_)
            cit(y, m + e * 0.03, q, 0.035, 0.022, 'yesil_koyu', ZG_)
        else:
            cit(y, p, q, 0.035, 0.022, 'yesil_koyu', ZG_)
    for p in k:
        c = p + (V((x0 + x1) / 2, (y0 + y1) / 2) - p).normalized() * 0.017
        topiari(y, c.x, c.y, ZG_ + 0.035, 0.06, 'yesil_koyu', 'top')


# the knot garden (front): interlaced low box hedges, coloured gravels in the beds, a central fountain
KX0, KX1, KY0, KY1 = 0.66, 1.14, -0.94, -0.46
bahce_cerceve(KX0, KX1, KY0, KY1)
kc = V((KX0 + KX1) / 2, (KY0 + KY1) / 2)
# the four beds: a diamond and a ring in each, low hedges
for sx in (-1, 1):
    for sy in (-1, 1):
        bc = kc + V(sx * 0.105, sy * 0.105)
        y.yuz_yon([V(p.x, p.y, ZG_ + 0.0015) for p in cokgen(bc, 0.085, 4, math.pi / 4)], 'kiremit' if sx * sy > 0 else 'kum_acik', Z)
        d4 = cokgen(bc, 0.085, 4, 0.0)
        for i in range(4):
            cit(y, d4[i], d4[(i + 1) % 4], 0.016, 0.012, 'boya_yesil', ZG_)
        r8 = cokgen(bc, 0.04, 10, 0.0)
        for i in range(10):
            cit(y, r8[i], r8[(i + 1) % 10], 0.016, 0.01, 'yesil_koyu', ZG_)
        topiari(y, bc.x, bc.y, ZG_, 0.05, 'yesil_koyu', 'koni')
# a fountain in the middle
donel(y, (kc.x, kc.y), [(0.0, ZG_), (0.035, ZG_), (0.035, ZG_ + 0.014), (0.03, ZG_ + 0.014), (0.03, ZG_ + 0.008)], 'tas_acik', n=16)
y.yuz_yon([V(p.x, p.y, ZG_ + 0.01) for p in cokgen(kc, 0.03, 16)], 'su', Z)
donel(y, (kc.x, kc.y), [(0.006, ZG_ + 0.01), (0.005, ZG_ + 0.04), (0.016, ZG_ + 0.044), (0.0, ZG_ + 0.05)], 'tas_acik', n=8)

# the maze (behind the knot garden): clipped yew walls in a square spiral
MX0, MX1, MY0, MY1 = 0.66, 1.14, -0.36, 0.12
bahce_cerceve(MX0, MX1, MY0, MY1)
mc = V((MX0 + MX1) / 2, (MY0 + MY1) / 2)
HM = 0.04
for k, r_ in enumerate((0.17, 0.125, 0.08, 0.04)):
    k4 = [mc + V(-r_, -r_), mc + V(r_, -r_), mc + V(r_, r_), mc + V(-r_, r_)]
    gap = k % 4   # each ring's gap on another side
    for i in range(4):
        a, b = k4[i], k4[(i + 1) % 4]
        if i == gap:
            m = a.lerp(b, 0.5 if k % 2 == 0 else 0.3)
            e = (b - a).normalized()
            cit(y, a, m - e * 0.02, HM, 0.022, 'yesil_koyu', ZG_)
            cit(y, m + e * 0.02, b, HM, 0.022, 'yesil_koyu', ZG_)
        else:
            cit(y, a, b, HM, 0.022, 'yesil_koyu', ZG_)
    # a cross wall to make dead ends
    if k < 3:
        c = k4[(gap + 2) % 4].lerp(k4[(gap + 3) % 4], 0.5)
        d_ = (mc - c).normalized()
        cit(y, c, c + d_ * 0.045, HM, 0.02, 'yesil_koyu', ZG_)
# the centre: an arbour (a small timber pavilion)
for sx in (-1, 1):
    for sy in (-1, 1):
        cubuk(y, V(mc.x + sx * 0.018, mc.y + sy * 0.018, ZG_), V(mc.x + sx * 0.018, mc.y + sy * 0.018, ZG_ + 0.06), 0.005, 'beyaz')
cati_kirma(y, mc.x - 0.022, mc.x + 0.022, mc.y - 0.022, mc.y + 0.022, ZG_ + 0.06, 0.035, 0.006, 'kursun', 'kursun2', ns=3, nr=3, mahya_en=0.004)
# visitors in the gardens
insan(y, 0.64, -0.7, G, 'lacivert', aci=0.0, s=1.0, sapka='koyu')
insan(y, 0.64, -0.62, G, 'boya_kirmizi', aci=0.2, s=0.95)
insan(y, 0.98, -0.12, ZG_, 'kumas', aci=2.0, s=0.95, sapka='kece')
# the household: the lord and lady at the porch, servants in the court, a porter with a halberd at the gate
insan(y, -0.03, 0.06, G + 0.004, 'lacivert', aci=-math.pi / 2, sapka='koyu')
insan(y, 0.03, 0.07, G + 0.004, 'boya_kirmizi', aci=-math.pi / 2, s=0.95)
insan(y, -0.2, -0.18, G + 0.002, 'kumas', aci=0.4, kol=0.5)
insan(y, 0.5, -0.68, G + 0.002, 'ahsap_acik', aci=2.0, sapka='saz')
insan(y, 0.06, -0.86, G + 0.003, 'boya_kirmizi', aci=-math.pi / 2, sapka='demir')
cubuk(y, V(0.07, -0.86, G + 0.003), V(0.07, -0.86, G + 0.085), 0.0025, 'ahsap')
y.koni((0.07, -0.86), 0.004, G + 0.085, 0.014, 'demir', n=4)

# ---------------------------------------------------------------- orchard, kitchen garden, fishpond
y.bolum('Meyve bahçesi, sebze bahçesi, balık havuzu')
for i, x in enumerate((-0.95, -0.75, -0.55, -0.35, -0.15, 0.05, 0.25)):
    for j, yy in enumerate((0.66, 0.84)):
        agac(y, x + 0.04 * (j % 2), yy, G, boy=0.15 + 0.02 * ((i + j) % 3), key='boya_yesil' if (i + j) % 2 else 'zeytin')
        if (i + j) % 3 == 0:
            for k in range(3):
                a = TAU * k / 3 + i
                kure(y, (x + 0.04 * (j % 2) + 0.03 * math.cos(a), yy + 0.03 * math.sin(a), G + 0.11), 0.005, 'boya_kirmizi', n=5, kat=3)
# beehives (skeps) at the orchard's edge
for k in range(4):
    donel(y, (-1.08 + 0.04 * k, 0.55), [(0.0, G), (0.014, G), (0.015, G + 0.012), (0.01, G + 0.026), (0.0, G + 0.03)], 'saz', n=8)
# the fishpond: a raised stone tank, water in it
havuz(y, 0.5, 0.88, 0.66, 0.9, G + 0.018, derin=0.02, kenar=0.016, key='tas_acik')
for k in range(3):
    kure(y, (0.58 + 0.12 * k, 0.74 + 0.04 * (k % 2), G + 0.012), 0.012, 'boya_yesil', n=6, kat=2)
# the road out of the gate and a few trees along the drive
for (tx, ty) in ((-0.3, -0.9), (0.3, -0.9), (-0.52, -0.9), (0.52, -0.9), (1.12, 0.62), (1.12, 0.88), (-1.14, 0.9)):
    agac(y, tx, ty, G, boy=0.17, key='yesil_koyu' if tx > 0 else 'boya_yesil')

calistir(y, 'lm_manor')
