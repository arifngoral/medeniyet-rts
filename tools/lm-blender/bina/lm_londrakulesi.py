# Londra Kulesi (lm_londrakulesi): the Tower of London. The White Tower in the middle (whitewashed Norman keep with
# pilaster strips, round-headed windows, battlements, three square corner turrets and the round north-east one, all
# with lead ogee cupolas and gilt vanes, the apse of St John's chapel, the timber forebuilding stair); the inner
# curtain with its towers (the Bloody Tower gate, Wakefield, Beauchamp, the Bell Tower's timber belfry...), the Queen's
# House (Tudor half-timbering) and the Chapel of St Peter on the green; the lower outer curtain with round bastions,
# the Byward gatehouse and causeway from the Middle Tower; the grassed moat, wet along the river front where
# St Thomas's Tower opens Traitors' Gate onto the Thames; the wharf with its cannon; Yeoman Warders and ravens.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from ingiliz_ortak import *
from bina_ortak import calistir
import doku

y = Yapi()
G = 0.07                         # ground
ZM = G - 0.05                    # moat floor
ZS = ZM + 0.008                  # water (moat front, river)
doku.KOSE_RENK['cimen'] = cayir_renk(G)
XA, XB, YA, YB = -1.15, 1.15, -1.1, 1.08
QY = -0.82                       # the quay (river edge)
M1 = (-0.92, 0.92, -0.7, 0.98)   # the moat's outer edge (counterscarp)
O_ = (-0.78, 0.78, -0.58, 0.88)  # the outer curtain
I_ = (-0.55, 0.55, -0.36, 0.68)  # the inner curtain
CH = 0.07                        # the channel under the wharf (half width)
TAS = 'kirec'
SUR = 'tas'


def sirala(a, b, dis):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized()
    return (a, b) if V(e.y, -e.x).dot(V(dis[0], dis[1])) > 0 else (b, a)


def duvar(a, b, z0, z1, dis, key='granit'):
    duz_duvar(y, *sirala(a, b, dis), z0, z1, key)


def ust(x0, x1, y0, y1, z, key):
    y.yuz_yon([V(x0, y0, z), V(x1, y0, z), V(x1, y1, z), V(x0, y1, z)], key, Z)


def kubbecik(c, r, z, key='kursun', vane=True):
    """a lead ogee cupola on a turret: a low drum, a swelling ogee cap, a finial and a gilt vane"""
    # the real caps (1660s) are ogee: a swelling bulb on a short drum, curving in to a slim waisted neck (not a spike)
    q = r / 0.04
    top = donel(y, c, [(r, z), (r, z + 0.01 * q), (r * 1.08, z + 0.016 * q), (r * 1.15, z + 0.028 * q), (r * 1.1, z + 0.04 * q),
                       (r * 0.9, z + 0.052 * q), (r * 0.58, z + 0.062 * q), (r * 0.3, z + 0.07 * q), (r * 0.16, z + 0.079 * q),
                       (r * 0.11, z + 0.088 * q), (r * 0.16, z + 0.093 * q), (r * 0.09, z + 0.099 * q), (0.0, z + 0.101 * q)], key, n=16,
                dilim=['kursun', 'kursun2'])
    y.prizma((c[0], c[1]), 0.0025, top.z - 0.004, top.z + 0.06, 'altin', n=4)
    kure(y, (c[0], c[1], top.z + 0.008), 0.006, 'altin', n=6, kat=3)
    if vane:
        levha(y, [V(c[0], c[1], top.z + 0.03), V(c[0] + 0.032, c[1], top.z + 0.026), V(c[0] + 0.032, c[1], top.z + 0.042), V(c[0], c[1], top.z + 0.046)],
              'altin', Y, 0.0015)
        cubuk(y, V(c[0] - 0.015, c[1], top.z + 0.02), V(c[0] + 0.015, c[1], top.z + 0.02), 0.0018, 'altin')
        cubuk(y, V(c[0], c[1] - 0.015, top.z + 0.02), V(c[0], c[1] + 0.015, top.z + 0.02), 0.0018, 'altin')
    return top.z + 0.06


# ---------------------------------------------------------------- ground, moat, river, wharf
y.bolum('Zemin, hendek, Thames ve rıhtım')
x0, x1, y0, y1 = M1
ox0, ox1, oy0, oy1 = O_
# outside the moat
for (a0, a1, b0, b1) in ((XA, x0, QY, YB), (x1, XB, QY, YB), (x0, x1, y1, YB)):
    ust(a0, a1, b0, b1, G, 'cimen')
# the wharf (paved), cut by the channel to Traitors' Gate
for (a0, a1) in ((x0, -CH), (CH, x1)):
    ust(a0, a1, QY, y0, G, 'zemin')
# the moat's grassed floor on the three dry sides
for (a0, a1, b0, b1) in ((x0, ox0, oy0, y1), (ox1, x1, oy0, y1), (ox0, ox1, oy1, y1)):
    ust(a0, a1, b0, b1, ZM, 'cimen')
# the wet front of the moat and the channel, the river
ust(x0, x1, y0, oy0, ZS, 'su')
ust(-CH, CH, QY, y0, ZS, 'su')
ust(XA, XB, YA, QY, ZS, 'su')
for (a0, a1) in ((x0, ox0), (ox1, x1)):   # the little step where the water meets the dry moat floor
    duvar(V(a0, oy0), V(a1, oy0), ZM, ZS, (0, 1), 'cimen')
# the counterscarp walls
duvar(V(x0, y0), V(x0, y1), ZM, G, (1, 0))
duvar(V(x1, y0), V(x1, y1), ZM, G, (-1, 0))
duvar(V(x0, y1), V(x1, y1), ZM, G, (0, -1))
for (a0, a1) in ((x0, -CH), (CH, x1)):
    duvar(V(a0, y0), V(a1, y0), ZS, G, (0, 1))
# the channel's walls and the quay
duvar(V(-CH, QY), V(-CH, y0), ZS, G, (1, 0))
duvar(V(CH, QY), V(CH, y0), ZS, G, (-1, 0))
for (a0, a1) in ((XA, -CH), (CH, XB)):
    duvar(V(a0, QY), V(a1, QY), ZS - 0.004, G, (0, -1))
# the block's sides
for (a, b, dis, zt) in ((V(XA, YA), V(XA, QY), (-1, 0), ZS), (V(XA, QY), V(XA, YB), (-1, 0), G), (V(XB, YA), V(XB, QY), (1, 0), ZS),
                        (V(XB, QY), V(XB, YB), (1, 0), G), (V(XA, YB), V(XB, YB), (0, 1), G), (V(XA, YA), V(XB, YA), (0, -1), ZS)):
    duvar(a, b, 0, zt, dis, 'toprak')
# the wharf: a bridge over the channel, cannon along the river, bollards
for k in range(7):
    xx = -CH - 0.01 + (2 * CH + 0.02) * k / 6
    cubuk(y, V(xx, QY + 0.02, G + 0.004), V(xx, y0 - 0.02, G + 0.004), 0.016, 'ahsap', 0.008)
for s in (-1, 1):
    cubuk(y, V(-CH - 0.02, QY + 0.02 + s * 0.0, G + 0.0), V(CH + 0.02, QY + 0.02, G + 0.0), 0.012, 'ahsap_koyu', 0.016)
    cubuk(y, V(-CH - 0.02, y0 - 0.02, G + 0.0), V(CH + 0.02, y0 - 0.02, G + 0.0), 0.012, 'ahsap_koyu', 0.016)
for xx in (-0.8, -0.62, -0.44, -0.26, 0.26, 0.44, 0.62, 0.8):
    with parca(y, (xx, QY + 0.04, G), -math.pi / 2):
        for s in (-1, 1):
            levha(y, [V(p.x, s * 0.012, p.z) for p in [V(-0.02, 0, 0), V(0.02, 0, 0), V(0.016, 0, 0.022), V(-0.012, 0, 0.022)]], 'ahsap_koyu', V(0, s), 0.003)
        for s in (-1, 1):
            cubuk(y, V(-0.01, s * 0.016, 0.012), V(-0.01, -s * 0.016, 0.012), 0.006, 'demir')
        boru(y, [V(-0.024, 0, 0.022), V(0.05, 0, 0.026)], 0.008, 'demir', n=8, r_son=0.006)
        for s in (-1, 1):
            with parca(y, (-0.004, s * 0.014, 0.012), 0.0):
                for i in range(8):
                    t0, t1 = TAU * i / 8, TAU * (i + 1) / 8
                    P = lambda t, d: V(0.012 * math.cos(t), d, 0.012 * math.sin(t))
                    y.yuz_yon([P(t0, -0.002), P(t1, -0.002), P(t1, 0.002), P(t0, 0.002)], 'ahsap_koyu', V(math.cos((t0 + t1) / 2), 0, math.sin((t0 + t1) / 2)))
                y.yuz_yon([V(0.012 * math.cos(TAU * i / 8), s * 0.002, 0.012 * math.sin(TAU * i / 8)) for i in range(8)], 'ahsap_koyu', V(0, s))
# a few boats on the river
for (bx, by, a) in ((-0.55, -0.98, 0.1), (0.6, -1.0, -0.2), (0.12, -0.92, math.pi / 2 - 0.2)):
    with parca(y, (bx, by, ZS), a):
        L_, W_ = 0.11, 0.032
        rim = [V(-L_ / 2, 0, 0.014), V(-L_ * 0.3, -W_ / 2, 0.012), V(L_ * 0.3, -W_ / 2, 0.012), V(L_ / 2, 0, 0.016), V(L_ * 0.3, W_ / 2, 0.012),
               V(-L_ * 0.3, W_ / 2, 0.012)]
        bot = [V(p.x * 0.85, p.y * 0.7, -0.002) for p in rim]
        for i in range(6):
            j = (i + 1) % 6
            m = (rim[i] + rim[j]) / 2
            y.yuz_yon([bot[i], bot[j], rim[j], rim[i]], 'ahsap', V(m.x, m.y, 0))
            ic = lambda p: V(p.x * 0.9, p.y * 0.82, p.z)
            y.yuz_yon([ic(bot[i]), ic(bot[j]), ic(rim[j]), ic(rim[i])], 'ahsap_koyu', -V(m.x, m.y, 0))
            y.yuz_yon([rim[i], rim[j], ic(rim[j]), ic(rim[i])], 'ahsap_acik', Z)
        y.yuz_yon([V(p.x * 0.96, p.y * 0.9, 0.009) for p in rim], 'ahsap_koyu', Z)
        insan(y, 0.0, 0.0, 0.008, 'kumas', s=0.9, aci=0.0, kol=0.6)

# ---------------------------------------------------------------- the outer curtain
y.bolum('Dış sur, burçlar')
ok_ = dikdortgen(ox0, ox1, oy0, oy1)
ZO = G + 0.06                    # the outer curtain's walk
sur(y, ok_, ZM, ZO - ZM, kalinlik=0.04, key=SUR, kapali=True, mazgal_h=0.022, parapet_h=0.01, ust_key='zemin')
for p in ok_:
    kule_yuvarlak(y, (p.x, p.y), 0.065, ZM, ZO - ZM + 0.03, SUR, cati='duz', mazgal_h=0.022, n=14, yarik_say=3)
for (cx, cy) in ((-0.3, oy1), (0.3, oy1), (ox1, 0.15), (ox0, 0.3)):
    kule_yuvarlak(y, (cx, cy), 0.045, ZM, ZO - ZM + 0.015, SUR, cati='duz', mazgal_h=0.02, n=10, yarik_say=2)
# the outer ward's ground (cobbles) between the curtains
ust(ox0, ox1, oy0, oy1, G, 'zemin')

# ---------------------------------------------------------------- St Thomas's Tower and Traitors' Gate
y.bolum("St Thomas Kulesi ve Hainler Kapısı (Traitors' Gate)")
TX, TYF, TYB = 0.15, oy0 - 0.05, oy0 + 0.08
ZT = G + 0.2
tk = dikdortgen(-TX, TX, TYF, TYB)
# the front: the great water arch (a wide segmental arch) with the portcullis-grid gates, water running in
W, e, nc, L = y.kemerli(V(-TX, TYF), V(TX, TYF), ZS, ZT - ZS, (SUR, 'tas_koyu', 'tas_acik', 'koyu'), v0=0.0, en=0.66, ust=ZT - ZS - 0.13, derin=0.05,
                        k_say=12, sivri=0.0, cerceve=(0.014, ['tas_acik', SUR]))
xa, xb = (1 - 0.66) / 2 * W, (1 + 0.66) / 2 * W
for k in range(9):   # the gate's grid of timbers
    u = xa + (xb - xa) * (k + 0.5) / 9
    cubuk(y, L(u, 0.0, 0.04), L(u, 0.1, 0.04), 0.004, 'ahsap_koyu', 0.004)
for v in (0.02, 0.045, 0.07, 0.095):
    cubuk(y, L(xa, v, 0.04), L(xb, v, 0.04), 0.004, 'ahsap_koyu', 0.004)
for (a, b) in ((V(TX, TYF), V(TX, TYB)), (V(-TX, TYB), V(-TX, TYF))):
    acs = acikli_duvar(y, a, b, ZS, ZT, [(0.5, 0.04, 0.1, 0.15)], (SUR, 'tas_koyu', 'tas_acik', 'cam'), derin=0.01, cerceve=(0.004, 'tas_acik'))
    for ac in acs: tudor_pencere(y, ac, ZS, 0.01, 'tas_acik', hood=True)
duvar(V(-TX, TYB), V(TX, TYB), G, ZT, (0, 1), SUR)
# upper storey: windows, string course, battlements and the half-timbered gable front over the gate
silme(y, tk, ZT - 0.006, 0.01, 0.008, 'tas_acik', 'duz')
parapet(y, disa(tk, 0.006), ZT + 0.004, 0.012, 0.02, 0.012, SUR, ust_key='tas_acik')
ust(-TX, TX, TYF, TYB, ZT + 0.004, 'kursun')
for (cx, cy) in ((-TX, TYF), (TX, TYF)):
    tz = kule_yuvarlak(y, (cx, cy), 0.04, ZS, ZT - ZS + 0.06, SUR, cati='duz', mazgal_h=0.02, n=12, yarik_say=2)
# a little timber-framed gabled lantern on the roof
with parca(y, (0, (TYF + TYB) / 2, ZT + 0.004), 0.0):
    for (a, b) in ((V(-0.06, -0.04), V(0.06, -0.04)), (V(0.06, -0.04), V(0.06, 0.04)), (V(0.06, 0.04), V(-0.06, 0.04)), (V(-0.06, 0.04), V(-0.06, -0.04))):
        ahsap_kat(y, a, b, 0.0, 0.06, [(0.5, 0.04, 0.012, 0.048)] if abs(a.y - b.y) < 1e-6 else [], 'siva', 'ahsap_koyu', aralik=0.02)
    cati_besik(y, -0.06, 0.06, -0.04, 0.04, 0.06, 0.05, 0.012, 'kiremit', 'kiremit2', ucluk_key='siva', uc_sacak=0.01, ns=4, nr=4, mahya_en=0.008)

# ---------------------------------------------------------------- the Byward gatehouse, causeway, Middle Tower
y.bolum('Byward kapısı, geçit ve Orta Kule')
BY = -0.38
with parca(y, (ox0, BY, G - 0.0), -math.pi / 2):
    kale_kapisi(y, 0, 0, 0.13, 0.0, 0.14, derin=0.12, key=SUR, kule='yuvarlak', kule_r=0.045, kule_h=0.18, cati='duz', kapi_key='ahsap', kule_n=14)
    duz_duvar(y, V(-0.12, -0.06), V(0.12, -0.06), ZM - G, 0.0, SUR)
with parca(y, (x0 - 0.06, BY, G), -math.pi / 2):
    kale_kapisi(y, 0, 0, 0.11, 0.0, 0.12, derin=0.1, key=SUR, kule='yuvarlak', kule_r=0.038, kule_h=0.15, cati='duz', kapi_key='ahsap', kule_n=12)
# the causeway over the moat: a stone bridge on two arches
kemer_dizisi(y, V(x0, BY - 0.04), V(ox0 - 0.05, BY - 0.04), 2, ZM, G - ZM, 0.08, renk=(SUR, 'tas_koyu', 'tas_acik', 'koyu'), en=0.7, ust=0.012, acik=True,
             taban=False)
for s in (-1, 1):
    kutu3(y, V((x0 + ox0 - 0.05) / 2, BY + s * 0.036, G + 0.014), X, Y, Z, ox0 - 0.05 - x0, 0.008, 0.028, SUR)
# the inner side: walls from the gate to the inner curtain enclosing the outer ward's west passage (Water Lane)
y.yuz_yon([V(XA + 0.001, BY - 0.04, G + 0.002), V(x0 - 0.12, BY - 0.04, G + 0.002), V(x0 - 0.12, BY + 0.04, G + 0.002), V(XA + 0.001, BY + 0.04, G + 0.002)],
          'toprak', Z)

# ---------------------------------------------------------------- the inner curtain and its towers
y.bolum('İç sur ve kuleleri')
ik = dikdortgen(*I_)
ZI = G + 0.17
sur(y, ik, G, ZI - G, kalinlik=0.045, key=SUR, kapali=True, mazgal_h=0.024, parapet_h=0.012, ust_key='zemin')
ix0, ix1, iy0, iy1 = I_
# corner towers: round (Bell Tower with its timber belfry; Devereux, Martin, Salt)
for (cx, cy, nm) in ((ix0, iy0, 'bell'), (ix0, iy1, ''), (ix1, iy1, ''), (ix1, iy0, '')):
    t = kule_yuvarlak(y, (cx, cy), 0.07, G, 0.26, SUR, cati="duz", mazgal_h=0.024, n=14, yarik_say=3)
    if nm == 'bell':
        # the Bell Tower's little white timber belfry with a lead cupola
        bc = V(cx, cy)
        for i in range(6):
            a = TAU * i / 6
            p = bc + V(math.cos(a), math.sin(a)) * 0.022
            cubuk(y, p + Z * (G + 0.272), p + Z * (G + 0.32), 0.005, 'beyaz')
        y.yuz_yon([V(p.x, p.y, G + 0.272) for p in cokgen(bc, 0.028, 6)], 'ahsap', Z)
        y.prizma((bc.x, bc.y), 0.012, G + 0.28, G + 0.31, 'ahsap_koyu', n=8)
        kubbecik(bc, 0.03, G + 0.318, vane=False)
# the Wakefield Tower (big and round) and the Bloody Tower gate on the south side
kule_yuvarlak(y, (0.05, iy0), 0.085, G, 0.3, SUR, cati='duz', mazgal_h=0.026, n=16, yarik_say=4)
kale_kapisi(y, 0.26, iy0, 0.13, G, 0.24, derin=0.13, key=SUR, kule=None, kapi_key='koyu')
# the gate's portcullis showing in the arch
for k in range(6):
    u = 0.26 - 0.026 + 0.052 * k / 5
    cubuk(y, V(u, iy0 - 0.065 + 0.03, G + 0.0), V(u, iy0 - 0.065 + 0.03, G + 0.09), 0.003, 'demir', 0.003)
# square wall towers: Beauchamp (west), Flint / Bowyer / Brick (north), Constable / Broad Arrow (east)
for (cx, cy, w, d) in ((ix0, 0.12, 0.13, 0.16), (-0.25, iy1, 0.11, 0.1), (0.05, iy1, 0.11, 0.1), (0.3, iy1, 0.11, 0.1), (ix1, 0.3, 0.1, 0.12),
                       (ix1, 0.0, 0.1, 0.12)):
    kule_kare(y, cx, cy, w, G, 0.24, SUR, cati='duz', mazgal_h=0.024, d=d, yarik_say=2)

# ---------------------------------------------------------------- the White Tower
y.bolum('Beyaz Kule (White Tower)')
WC = V(-0.02, 0.17)
WX, WY = 0.22, 0.19
wk = dikdortgen(WC.x - WX, WC.x + WX, WC.y - WY, WC.y + WY)
ZW = G + 0.46
KAT = [(G, G + 0.1, 0), (G + 0.1, G + 0.22, 1), (G + 0.22, G + 0.34, 1), (G + 0.34, ZW, 2)]
# a battered plinth
silme(y, wk, G, 0.04, 0.012, 'tas_acik', 'kaide')
for (z0, z1, tur) in KAT:
    for i in range(4):
        a, b = wk[i], wk[(i + 1) % 4]
        a2, b2, L_, e2, n2 = eksen(a, b)
        nb = 4 if L_ > 0.4 else 3
        for j in range(nb):
            p, q = a2.lerp(b2, j / nb), a2.lerp(b2, (j + 1) / nb)
            if tur == 0:
                duz_duvar(y, p, q, z0, z1, TAS)
                yarik(y, p.lerp(q, 0.5) + n2 * 0.001, e2, n2, -0.004, z0 + 0.04, 0.008, 0.04, 'koyu')
            elif tur == 1:
                y.kemerli(p, q, z0, z1 - z0, (TAS, 'tas_koyu', 'tas_acik', 'cam'), v0=0.035, en=0.26, ust=0.025, derin=0.014, k_say=6, sivri=0.0,
                          cerceve=(0.005, 'tas_acik'))
            else:   # the top floor: paired round-headed windows
                for m in range(2):
                    y.kemerli(p.lerp(q, m / 2), p.lerp(q, (m + 1) / 2), z0, z1 - z0, (TAS, 'tas_koyu', 'tas_acik', 'cam'), v0=0.03, en=0.42, ust=0.025,
                              derin=0.014, k_say=4, sivri=0.0, cerceve=(0.004, 'tas_acik'))
# pilaster strips on the bay lines, string courses
for i in range(4):
    a2, b2, L_, e2, n2 = eksen(wk[i], wk[(i + 1) % 4])
    nb = 4 if L_ > 0.4 else 3
    for j in range(1, nb):
        p = a2.lerp(b2, j / nb)
        kutu3(y, p + n2 * 0.006 + Z * ((G + ZW) / 2), e2, n2, Z, 0.022, 0.012, ZW - G, TAS, ('+x', '-x', '+y'))
for zz in (G + 0.1, G + 0.22, G + 0.34):
    silme(y, wk, zz - 0.004, 0.008, 0.008, 'tas_acik', 'duz')
silme(y, wk, ZW - 0.012, 0.014, 0.012, 'tas_acik', 'tac')
wd = disa(wk, 0.012)
parapet(y, wd, ZW + 0.002, 0.016, 0.03, 0.016, TAS, ust_key='tas_acik')
ust(WC.x - WX, WC.x + WX, WC.y - WY, WC.y + WY, ZW + 0.002, 'kursun')
# the roof's ridges behind the parapet (two parallel lead roofs, as on the real keep)
for dx in (-WX / 2, WX / 2):
    cati_besik(y, WC.x + dx - WX / 2 + 0.03, WC.x + dx + WX / 2 - 0.03, WC.y - WY + 0.03, WC.y + WY - 0.03, ZW + 0.002, 0.035, 0.0, 'kursun', 'kursun2',
               ucluk_key='kursun2', uc_sacak=0.0, ns=6, nr=3, mahya_en=0.006)
# the turrets: three square, the north-east one round; lead ogee cupolas with vanes
ZK = ZW + 0.12
for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
    p = V(WC.x + sx * WX, WC.y + sy * WY)
    if (sx, sy) == (1, 1):
        r = 0.065
        y.prizma((p.x, p.y), r, G, ZK, TAS, n=24, ust=False)
        for zz in (G + 0.1, G + 0.22, G + 0.34, ZW - 0.012):
            halka_kornis(y, p, r, zz - 0.004, 0.008, 0.008, 24, 'tas_acik')
        for zz in (G + 0.15, G + 0.28, ZW + 0.04):
            for a in (0.4, 1.2):
                nn = V(math.cos(a), math.sin(a))
                yarik(y, p + nn * (r + 0.001), V(-nn.y, nn.x), nn, -0.005, zz, 0.01, 0.04, 'koyu')
        silme(y, cokgen(p, r, 24), ZK - 0.012, 0.014, 0.01, 'tas_acik', 'tac')
        ring = cokgen(p, r + 0.01, 24)
        for i in range(0, 24, 2):
            kutu(y, ring[i] + Z * (ZK + 0.002), ring[(i + 1) % 24] - ring[i], (ring[(i + 1) % 24] - ring[i]).length, 0.012, 0.02, TAS)
        ust_ = [V(q.x, q.y, ZK + 0.002) for q in ring]
        y.yuz_yon(ust_, 'kursun', Z)
        kubbecik(p, r * 0.85, ZK + 0.002)
    else:
        w = 0.085
        kc = p + V(sx, sy) * 0.012
        kutu_merkez(y, (kc.x, kc.y), w, w, ZK - G, TAS, z0=G, yuzler='onarkasagsolust')
        kk = dikdortgen(kc.x - w / 2, kc.x + w / 2, kc.y - w / 2, kc.y + w / 2)
        for zz in (G + 0.1, G + 0.22, G + 0.34, ZW - 0.012):
            silme(y, kk, zz - 0.004, 0.008, 0.008, 'tas_acik', 'duz')
        for i in range(4):
            a2, b2, L_, e2, n2 = eksen(kk[i], kk[(i + 1) % 4])
            for zz in (G + 0.15, G + 0.28, ZW + 0.03):
                yarik(y, a2.lerp(b2, 0.5) + n2 * 0.001, e2, n2, -0.005, zz, 0.01, 0.045, 'koyu')
        silme(y, kk, ZK - 0.012, 0.014, 0.01, 'tas_acik', 'tac')
        parapet(y, disa(kk, 0.01), ZK + 0.002, 0.008, 0.02, 0.012, TAS, ust_key='tas_acik')
        ust(kc.x - w / 2, kc.x + w / 2, kc.y - w / 2, kc.y + w / 2, ZK + 0.002, 'kursun')
        kubbecik(kc, w * 0.48, ZK + 0.004)
# the apse of St John's chapel on the east face's south end
AC = V(WC.x + WX, WC.y - WY + 0.1)
RA = 0.09
ap = [AC + V(math.cos(t), math.sin(t)) * RA for t in [-math.pi / 2 + math.pi * k / 6 for k in range(7)]]
for k in range(6):
    for (z0, z1, tur) in KAT:
        if tur == 0:
            duz_duvar(y, ap[k], ap[k + 1], z0, z1, TAS)
        else:
            y.kemerli(ap[k], ap[k + 1], z0, z1 - z0, (TAS, 'tas_koyu', 'tas_acik', 'cam'), v0=0.035, en=0.4, ust=0.025, derin=0.012, k_say=6)
silme(y, ap, ZW - 0.012, 0.014, 0.012, 'tas_acik', 'tac', kapali=False)
silme(y, ap, G, 0.04, 0.012, 'tas_acik', 'kaide', kapali=False)
y.yuz_yon([V(p.x, p.y, ZW + 0.002) for p in ap], 'kursun', Z)
parapet(y, disa(ap, 0.012, kapali=False), ZW + 0.002, 0.016, 0.03, 0.016, TAS, kapali=False, ust_key='tas_acik')
# the forebuilding: a timber stair on the south face up to the first-floor door
FX = WC.x - 0.1
merdiven(y, V(FX + 0.17, WC.y - WY - 0.045), math.pi, 0.05, G, G + 0.1, n=10, d=0.016, key='ahsap_acik', yanlik='ahsap')
kutu_merkez(y, (FX - 0.005, WC.y - WY - 0.045), 0.05, 0.05, 0.1, 'ahsap_dikey', z0=G)
for (dx, dy) in ((-0.025, -0.022), (0.02, -0.022)):
    cubuk(y, V(FX + dx, WC.y - WY - 0.045 + dy, G + 0.1), V(FX + dx, WC.y - WY - 0.045 + dy, G + 0.16), 0.005, 'ahsap_koyu')
cati_besik(y, FX - 0.03, FX + 0.025, WC.y - WY - 0.07, WC.y - WY, G + 0.16, 0.03, 0.01, 'kursun', 'kursun2', ucluk_key='ahsap', uc_sacak=0.008, ns=3, nr=3,
           mahya_en=0.005)
y.bolum('Sancak')
sancak(y, WC.x, WC.y, ZW + 0.04, boy=0.28, en=0.16, yuk=0.095, aci=math.pi * 0.85)

# ---------------------------------------------------------------- inside the inner ward
y.bolum("İç avlu: Queen's House, St Peter şapeli, Waterloo kışlası, yeşil")
# Tower Green (the lawn on the west side) and the paved parade
y.yuz_yon([V(ix0 + 0.06, -0.1, G + 0.003), V(-0.3, -0.1, G + 0.003), V(-0.3, 0.5, G + 0.003), V(ix0 + 0.06, 0.5, G + 0.003)], 'cimen', Z)
duvarlar(y, dikdortgen(ix0 + 0.06, -0.3, -0.1, 0.5), G, G + 0.003, 'tas_acik')
# the Queen's House: a Tudor timber-framed house in the south-west corner
QX0, QX1, QY0, QY1 = ix0 + 0.06, -0.24, iy0 + 0.05, -0.2
QZ1, QZU = G + 0.08, G + 0.17
for (a, b, dis, ps) in ((V(QX0, QY0), V(QX1, QY0), (0, 1), [(0.25, 0.04, 0.02, 0.065), (0.6, 0.03, 0.0, 0.07), (0.85, 0.04, 0.02, 0.065)]),
                        (V(QX1, QY0), V(QX1, QY1), (1, 0), [(0.5, 0.04, 0.02, 0.065)]), (V(QX1, QY1), V(QX0, QY1), (0, 1), [(0.3, 0.05, 0.02, 0.065), (0.7, 0.05, 0.02, 0.065)]),
                        (V(QX0, QY1), V(QX0, QY0), (-1, 0), [])):
    a2, b2 = sirala(a, b, dis)
    ahsap_kat(y, a2, b2, G, QZ1, [p for p in ps], 'siva', 'ahsap_koyu', aralik=0.022)
    ahsap_kat(y, a2, b2, QZ1, QZU, [(u, w, 0.02, 0.07) for (u, w, v0, v1) in ps if w < 0.045] + [(0.5, 0.05, 0.02, 0.07)], 'siva', 'ahsap_koyu', aralik=0.022)
cati_besik(y, QX0, QX1, QY0, QY1, QZU, 0.09, 0.016, 'kiremit', 'kiremit2', ucluk_key='siva', uc_sacak=0.012, ns=6, nr=5, mahya_en=0.008)
for gx in (-0.42, -0.32):   # gables onto the green
    cati_besik(y, gx - 0.035, gx + 0.035, QY1 - 0.06, QY1 + 0.012, QZU, 0.075, 0.012, 'kiremit', 'kiremit2', ucluk_key='siva', uc_sacak=0.01, ns=3, nr=4,
               mahya_en=0.007)
    duz_duvar(y, *sirala(V(gx - 0.035, QY1 + 0.012), V(gx + 0.035, QY1 + 0.012), (0, 1)), G, QZU, 'siva')
    for s in (-1, 1):
        duz_duvar(y, *sirala(V(gx + s * 0.035, QY1), V(gx + s * 0.035, QY1 + 0.012), (s, 0)), G, QZU, 'siva')
    yari_ahsap(y, *sirala(V(gx - 0.035, QY1 + 0.012), V(gx + 0.035, QY1 + 0.012), (0, 1)), G, QZU, [], 'ahsap_koyu', aralik=0.018, en=0.005, capraz=False)
baca(y, -0.36, (QY0 + QY1) / 2, QZU + 0.02, QZU + 0.11, 0.05, 0.03, 2, 0.06)
kutu_merkez(y, (-0.36, (QY0 + QY1) / 2), 0.05, 0.03, 0.1, 'tugla', z0=QZU + 0.01)
# the Chapel of St Peter ad Vincula (north-west): a flint church with a small bell turret
CX0, CX1, CY0, CY1 = ix0 + 0.06, -0.2, 0.52, iy1 - 0.05
for (a, b, dis, n) in ((V(CX0, CY0), V(CX1, CY0), (0, -1), 3), (V(CX1, CY0), V(CX1, CY1), (1, 0), 1), (V(CX1, CY1), V(CX0, CY1), (0, 1), 0),
                       (V(CX0, CY1), V(CX0, CY0), (-1, 0), 1)):
    pencereli_duvar(y, [*sirala(a, b, dis)], G, 0.12, [n], kapali=False, renk=('granit', 'tas_koyu', 'tas_acik', 'cam'), v0=0.03, en=0.4, ust=0.015,
                    derin=0.012, sivri=0.6, k_say=6, cerceve=(0.004, 'tas_acik'))
cati_besik(y, CX0, CX1, CY0, CY1, G + 0.12, 0.08, 0.014, 'arduvaz', 'kursun', ucluk_key='granit', uc_sacak=0.01, ns=6, nr=4, mahya_en=0.008)
kutu_merkez(y, (CX0 + 0.03, (CY0 + CY1) / 2), 0.04, 0.04, 0.24 - 0.0, 'granit', z0=G)
parapet(y, disa(dikdortgen(CX0 + 0.01, CX0 + 0.05, (CY0 + CY1) / 2 - 0.02, (CY0 + CY1) / 2 + 0.02), 0.004), G + 0.24, 0.006, 0.014, 0.008, 'granit')
ust(CX0 + 0.01, CX0 + 0.05, (CY0 + CY1) / 2 - 0.02, (CY0 + CY1) / 2 + 0.02, G + 0.24, 'kursun')
for i in range(6):
    a = TAU * i / 6
    p = V(CX0 + 0.03, (CY0 + CY1) / 2) + V(math.cos(a), math.sin(a)) * 0.01
    cubuk(y, p + Z * (G + 0.24), p + Z * (G + 0.27), 0.003, 'beyaz')
kubbecik(V(CX0 + 0.03, (CY0 + CY1) / 2), 0.016, G + 0.27, vane=False)
# the Waterloo Barracks along the north: a long castellated range
BX0, BX1, BY0_, BY1_ = -0.12, 0.42, 0.46, iy1 - 0.05
for (a, b, dis, n) in ((V(BX0, BY0_), V(BX1, BY0_), (0, -1), 9), (V(BX1, BY0_), V(BX1, BY1_), (1, 0), 2), (V(BX1, BY1_), V(BX0, BY1_), (0, 1), 0),
                       (V(BX0, BY1_), V(BX0, BY0_), (-1, 0), 2)):
    pencereli_duvar(y, [*sirala(a, b, dis)], G, 0.15, [n], kapali=False, renk=('tas_acik', 'tas_koyu', 'tas_acik', 'cam'), v0=0.03, en=0.42, ust=0.02,
                    derin=0.012, sivri=0.3, k_say=6)
bk = dikdortgen(BX0, BX1, BY0_, BY1_)
silme(y, bk, G + 0.14, 0.012, 0.008, 'tas_acik', 'duz')
parapet(y, disa(bk, 0.006), G + 0.15, 0.008, 0.016, 0.01, 'tas_acik')
ust(BX0, BX1, BY0_, BY1_, G + 0.15, 'kursun')
for xx in (BX0, (BX0 + BX1) / 2, BX1):
    kutu_merkez(y, (xx, BY0_ + 0.005), 0.03, 0.03, 0.19, 'tas_acik', z0=G)
    parapet(y, disa(dikdortgen(xx - 0.015, xx + 0.015, BY0_ - 0.01, BY0_ + 0.02), 0.003), G + 0.19, 0.006, 0.012, 0.006, 'tas_acik')
    ust(xx - 0.015, xx + 0.015, BY0_ - 0.01, BY0_ + 0.02, G + 0.19, 'kursun')
# the scaffold site memorial on the green: a glass cushion on a granite square
kutu_merkez(y, (-0.42, 0.25), 0.06, 0.06, 0.006, 'granit', z0=G + 0.003)
kutu_merkez(y, (-0.42, 0.25), 0.024, 0.024, 0.012, 'cam', z0=G + 0.009)
# trees on the green
for (tx, ty) in ((-0.46, 0.0), (-0.46, 0.42), (-0.36, 0.1)):
    agac(y, tx, ty, G + 0.003, boy=0.16, key='boya_yesil')

# ---------------------------------------------------------------- Yeoman Warders and ravens
y.bolum('Kule muhafızları (Beefeater) ve kuzgunlar')


def beefeater(x, yy, z, aci):
    """a Yeoman Warder: a scarlet tunic, a black Tudor bonnet, a partisan"""
    insan(y, x, yy, z, 'boya_kirmizi', s=1.15, aci=aci, sapka=None)
    with parca(y, (x, yy, z), aci, 1.15):
        donel(y, (0, 0), [(0.0, 0.043), (0.0095, 0.043), (0.0085, 0.048), (0.006, 0.05), (0.0, 0.051)], 'koyu', n=8)
        kutu3(y, V(0.0075, 0, 0.02), X, Y, Z, 0.002, 0.009, 0.012, 'altin')
        cubuk(y, V(0.004, 0.01, 0.0), V(0.004, 0.01, 0.075), 0.0022, 'ahsap')
        y.koni((0.004, 0.01), 0.004, 0.075, 0.014, 'demir', n=4)


for (x, yy, a) in ((-0.06, iy0 - 0.11, -math.pi / 2), (0.3, iy0 - 0.12, -math.pi / 2), (0.22, iy0 - 0.12, -math.pi / 2), (ox0 - 0.02, BY + 0.06, math.pi),
                   (-0.2, -0.05, 0.3), (0.15, -0.12, -1.2), (0.0, QY + 0.06, -math.pi / 2), (-0.12, QY + 0.06, -math.pi / 2)):
    beefeater(x, yy, G + 0.002, a)
# visitors
for k, (x, yy, a) in enumerate(((0.05, QY + 0.05, 1.5), (-0.5, QY + 0.06, 1.4), (0.1, -0.15, 2.5))):
    insan(y, x, yy, G + 0.002, ['kumas', 'boya_yesil', 'lacivert', 'ahsap_acik', 'kece'][k], s=1.05, aci=a)


def kuzgun(x, yy, z, aci):
    with parca(y, (x, yy, z), aci):
        boru(y, [V(-0.012, 0, 0.008), V(0.0, 0, 0.01), V(0.008, 0, 0.013)], 0.0055, 'koyu', n=6, r_son=0.004)
        kure(y, (0.011, 0, 0.016), 0.0042, 'koyu', n=6, kat=3)
        cubuk(y, V(0.014, 0, 0.016), V(0.022, 0, 0.0145), 0.0022, 'koyu')
        for s in (-1, 1):
            cubuk(y, V(-0.002, s * 0.002, 0.004), V(-0.002, s * 0.002, -0.0005), 0.0015, 'koyu')
        cubuk(y, V(-0.012, 0, 0.008), V(-0.022, 0, 0.005), 0.006, 'koyu', 0.0015)


for k, (x, yy, a) in enumerate(((-0.4, 0.05, 0.3), (-0.37, 0.18, 2.0), (-0.44, 0.33, 4.0), (-0.34, 0.4, 1.0), (0.1, -0.08, 2.6), (-0.28, -0.08, 5.0))):
    kuzgun(x, yy, G + 0.003, a)
kuzgun(WC.x + WX - 0.04, WC.y - WY + 0.014, ZW + 0.034, 1.0)

calistir(y, 'lm_londrakulesi')
