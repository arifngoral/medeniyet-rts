# Parlamento ve Saat Kulesi (lm_bigben): the Palace of Westminster on the Thames. The Gothic Revival river front
# (buttressed bays, Perpendicular windows, pinnacled pavilions, steep iron-grey roofs with cresting) round two courts,
# the Elizabeth Tower (Big Ben: panelled shaft, gilded clock faces, belfry, slate spire), the great square Victoria
# Tower with the flag, the octagonal Central Tower spire, Westminster Hall; the embankment, the bridge, boats.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from ingiliz_ek import *
from bina_ortak import calistir

y = Yapi()


def agac(y, x, yy, z=0.0, boy=0.12):
    """a round-crowned tree, lighter than the library's (the budget goes to the facades)"""
    y.prizma((x, yy), 0.005, z, z + boy * 0.45, 'ahsap', n=5)
    kure(y, (x, yy, z + boy * 0.68), boy * 0.32, 'boya_yesil', n=8, kat=4)

Z0 = 0.06            # land
ZW = 0.03            # the Thames
KY = -0.88           # the embankment line
DUV = 'kum'          # Anston limestone (honey)
TR = 'kum_acik'      # dressed trim
KO = 'kum_koyu'      # recesses
CATI = 'arduvaz'
KAT = (0.1, 0.095, 0.085)
ZT = Z0 + sum(KAT)   # wall top (behind the parapet)
PH = 0.028           # parapet
RENK = (DUV, KO, TR, 'cam')

# the palace's outer rectangle and its two courts
PX0, PX1, PY0, PY1 = -0.8, 0.8, -0.74, 0.72
CY0, CY1 = -0.46, 0.5            # courts (y)
CX = ((-0.56, -0.07), (0.07, 0.56))   # courts (x)
HY0_ = -0.3                      # Westminster Hall's north end (y)


# ---------------------------------------------------------------- facades
def cephe(a, b, n, tur='tam', z0=Z0, katlar=KAT, parapet=True, cer=True):
    """a palace front a->b (faces the right) of n bays and the storeys katlar. tur: 'tam' (buttresses with pinnacles,
    mullioned windows with hood moulds, blind tracery panels), 'orta' (framed windows, plain pilasters), 'sade'
    (courts: plain pointed windows). Returns the top z of the walls"""
    a, b, L, e, nc = eksen(a, b)
    z = z0
    for j, h in enumerate(katlar):
        for k in range(n):
            p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
            if tur == 'tam':
                gotik_pencere(y, p, q, z, h, RENK, en=0.5, v0=h * 0.2, sivri=0.28, mullion=1, cerceve=(0.0035, TR) if cer else None, hood=True, derin=0.016)
            elif tur == 'orta':
                gotik_pencere(y, p, q, z, h, RENK, en=0.46, v0=h * 0.2, sivri=0.28, mullion=0, cerceve=None, hood=False, derin=0.014, k_say=4)
            elif j < len(katlar) - 1 or tur == 'bos':
                duz_duvar(y, p, q, z, z + h, DUV)
            else:
                y.kemerli(p, q, z, h, RENK, v0=h * 0.22, en=0.44, ust=h * 0.12, derin=0.012, k_say=4, sivri=0.3)
            if tur == 'tam' and j > 0:   # blind tracery panels under the sill (two pointed lights)
                W = (q - p).length
                for s in (-1, 1):
                    m = p.lerp(q, 0.5 + s * 0.13) + nc * 0.0015
                    w2, v0_, v1_ = min(W * 0.1, h * 0.05), z + 0.006, z + h * 0.16
                    y.yuz_yon([m - e * w2 + Z * v0_, m + e * w2 + Z * v0_, m + e * w2 + Z * (v1_ - w2), m + Z * v1_, m - e * w2 + Z * (v1_ - w2)], KO, nc)
        z += h
        if j < len(katlar) - 1:
            silme(y, [a, b], z - 0.004, 0.008, 0.006, TR, 'duz', kapali=False)
    if tur not in ('sade', 'bos'):   # (at the foot of the deep courts the plinth is hardly seen)
        silme(y, [a, b], z0, 0.022, 0.01, KO, 'kaide', kapali=False)
    silme(y, [a, b], z - 0.012, 0.012, 0.008, TR, 'tac', kapali=False)
    if parapet:
        kutu3(y, (a + b) / 2 - nc * 0.006 + Z * (z + PH / 2), e, nc, Z, L, 0.012, PH, DUV, ('+y', '-y', '+z', '+x', '-x'))
        kutu3(y, (a + b) / 2 + nc * 0.001 + Z * (z + PH + 0.002), e, nc, Z, L + 0.004, 0.016, 0.004, TR, ('+y', '-y', '+z', '-z', '+x', '-x'))
        # pierced-tracery look: small dark quatrefoil diamonds along the parapet
        m_ = max(2, int(L / 0.03)) if tur not in ('sade', 'bos') else 0
        for i in range(m_):
            c = a.lerp(b, (i + 0.5) / m_) + nc * 0.0012 + Z * (z + PH * 0.5)
            r = 0.0065
            y.yuz_yon([c - e * r, c - Z * r, c + e * r, c + Z * r], KO, nc)
    if tur in ('tam', 'orta'):
        for k in range(n + 1):
            p = a.lerp(b, k / n)
            if tur == 'tam':
                payanda(y, p + e * (0.0065 if k == 0 else -0.0065 if k == n else 0), e, nc, z0, z + PH + 0.006, w=0.013, d=0.011, key=DUV, pin=0.05, pin_key=TR)
            else:
                kutu3(y, p + nc * 0.004 + Z * ((z0 + z) / 2), e, nc, Z, 0.01, 0.008, z - z0, DUV, ('+x', '-x', '+y'))
    return z


def cati(x0, x1, y0, y1, z, h, kres=True, sacak=0.006):
    """a steep iron-grey roof inside the parapet with iron cresting on the ridge"""
    zr = cati_besik(y, x0, x1, y0, y1, z, h, sacak, CATI, mahya='demir', kalinlik=0.008, alt_key=KO, ucluk_key=DUV, mahya_en=0.008, nr=3, ns=4)
    if kres:
        if (x1 - x0) >= (y1 - y0):
            kresting(y, V(x0 + 0.01, (y0 + y1) / 2), V(x1 - 0.01, (y0 + y1) / 2), zr + 0.004)
        else:
            kresting(y, V((x0 + x1) / 2, y0 + 0.01), V((x0 + x1) / 2, y1 - 0.01), zr + 0.004)
    return zr


def fleche(x, yy, z, h=0.1, r=0.016):
    """a little octagonal ventilator turret with a spirelet on a roof ridge"""
    donel(y, (x, yy), [(r, z - 0.03), (r, z + h * 0.35)], 'demir', n=8)
    for i in range(8):   # louvres
        t = TAU * (i + 0.5) / 8
        p = V(x + r * 1.002 * math.cos(t), yy + r * 1.002 * math.sin(t), z + h * 0.05)
        y.yuz_yon([p - V(-math.sin(t), math.cos(t)) * r * 0.3, p + V(-math.sin(t), math.cos(t)) * r * 0.3,
                   p + V(-math.sin(t), math.cos(t)) * r * 0.3 + Z * h * 0.24, p - V(-math.sin(t), math.cos(t)) * r * 0.3 + Z * h * 0.24], 'koyu', V(math.cos(t), math.sin(t)))
    donel(y, (x, yy), [(r * 1.3, z + h * 0.35), (r * 1.05, z + h * 0.42), (0.0, z + h)], CATI, n=8)
    kure(y, (x, yy, z + h + 0.004), 0.005, 'altin', n=6, kat=3)


# ---------------------------------------------------------------- ground: the river, the embankment, the land
y.bolum('Thames, rıhtım ve zemin')
su_ve_kiyi(y, -1.2, 1.2, -1.2, KY, ZW, Z0, KY, 'granit')
kutu(y, V(-1.2, KY, 0), X, 2.4, 1.05 - KY, Z0, 'granit_koyu', 'arkasagsol')
# the land round the palace (under the palace's walls and roofs it would never be seen: left open)
_h = (PX0 + 0.02, PX1 - 0.02, PY0 + 0.02, PY1 - 0.02)
for (x0, x1, y0, y1) in ((-1.2, 1.2, KY, _h[2]), (-1.2, 1.2, _h[3], 1.05), (-1.2, _h[0], _h[2], _h[3]), (_h[1], 1.2, _h[2], _h[3])):
    y.yuz_yon([V(x0, y0, Z0), V(x1, y0, Z0), V(x1, y1, Z0), V(x0, y1, Z0)], 'zemin', Z)
yer = lambda x0, x1, y0, y1, k='cimen': y.yuz_yon([V(x0, y0, Z0 + 0.0015), V(x1, y0, Z0 + 0.0015), V(x1, y1, Z0 + 0.0015), V(x0, y1, Z0 + 0.0015)], k, Z)
yer(0.86, 1.18, -0.84, 0.02)                     # Victoria Tower Gardens
yer(0.86, 1.18, 0.42, 1.02)
yer(-0.76, 0.76, 0.78, 1.02, 'tas_koyu')         # Old Palace Yard (road)
# the river terrace: a balustrade on the embankment, lamp standards, strollers
kutu3(y, V(0.06, KY + 0.008, Z0 + 0.01), X, Y, Z, 2.26 - 0.12, 0.01, 0.02, TR, ('+x', '-x', '+y', '-y', '+z'))
for i in range(20):
    x = -1.0 + i * 0.112
    kutu_merkez(y, (x, KY + 0.008), 0.016, 0.016, 0.026, TR, z0=Z0)
for x in (-0.6, -0.15, 0.3, 0.75):
    fener(y, x, KY + 0.03, Z0, h=0.11, key='demir', kol=1)
for i, (x, yy, k) in enumerate(((-0.4, -0.82, 'koyu'), (-0.37, -0.83, 'boya_kirmizi'), (0.1, -0.8, 'lacivert'), (0.52, -0.84, 'koyu'),
                                (0.55, -0.81, 'kirmizi'), (0.95, -0.6, 'koyu'), (1.0, -0.3, 'boya_yesil'))):
    insan(y, x, yy, Z0, k, 1.0, aci=i * 1.3, sapka='koyu' if i % 2 == 0 else None)

# ---------------------------------------------------------------- Westminster Bridge (green iron arches, granite piers)
y.bolum('Westminster Köprüsü')
BX0, BX1 = -1.2, -1.07
zd = Z0 + 0.004
kemer_dizisi(y, V(BX1, -1.2), V(BX1, KY), 3, ZW - 0.004, zd - ZW + 0.004, BX1 - BX0, ('boya_yesil', 'boya_yesil', 'tas_koyu', 'boya_yesil'),
             en=0.78, ust=0.012, sivri=0.0, acik=True, taban=False)
for yy in (-1.2 + 0.32 / 3, -1.2 + 0.64 / 3):   # granite cutwaters at the piers
    for s in (-1, 1):
        x = BX1 + 0.012 if s > 0 else BX0 - 0.012
        y.yuz_yon([V(x - s * 0.012, yy - 0.014, ZW - 0.004), V(x, yy, ZW - 0.004), V(x, yy, zd - 0.024), V(x - s * 0.012, yy - 0.014, zd - 0.024)], 'granit', V(s, -1))
        y.yuz_yon([V(x, yy, ZW - 0.004), V(x - s * 0.012, yy + 0.014, ZW - 0.004), V(x - s * 0.012, yy + 0.014, zd - 0.024), V(x, yy, zd - 0.024)], 'granit', V(s, 1))
        y.yuz_yon([V(x - s * 0.012, yy - 0.014, zd - 0.024), V(x, yy, zd - 0.024), V(x - s * 0.012, yy + 0.014, zd - 0.024)], 'granit', Z)
for x in (BX0 + 0.006, BX1 - 0.006):   # green iron railings and lamps
    kutu3(y, V(x, (KY - 1.2) / 2, zd + 0.012), X, Y, Z, 0.006, 1.2 + KY, 0.022, 'boya_yesil', ('+x', '-x', '+z', '-y'))
    for yy in (-1.12, -0.98):
        fener(y, x, yy, zd, h=0.09, key='boya_yesil', kol=3)

# ---------------------------------------------------------------- boats on the river
y.bolum('Mavna ve sandallar')


def mavna(x, yy, aci):
    """a Thames sailing barge: a long dark hull, a spritsail and a foresail in red-ochre canvas"""
    with parca(y, (x, yy, ZW), aci):
        L, B = 0.26, 0.04
        hull = [V(-L / 2, -B * 0.6), V(-L / 2 + 0.03, -B), V(L / 2 - 0.05, -B), V(L / 2, 0), V(L / 2 - 0.05, B), V(-L / 2 + 0.03, B), V(-L / 2, B * 0.6)]
        for i in range(len(hull)):
            p, q = hull[i], hull[(i + 1) % len(hull)]
            y.yuz_yon([V(p.x, p.y, -0.004), V(q.x, q.y, -0.004), V(q.x, q.y, 0.02), V(p.x, p.y, 0.02)], 'ahsap_koyu', V((p + q).x / 2, (p + q).y / 2) * 1)
        y.yuz_yon([V(p.x, p.y, 0.02) for p in hull], 'ahsap', Z)
        silme(y, [V(p.x, p.y, 0) for p in hull], 0.016, 0.004, 0.003, 'boya_kirmizi', 'duz')
        kutu3(y, V(-0.08, 0, 0.026), X, Y, Z, 0.04, 0.04, 0.012, 'ahsap_acik')
        y.prizma((0.02, 0), 0.003, 0.02, 0.3, 'ahsap', n=5)
        cubuk(y, V(0.02, 0.0, 0.04), V(-0.1, 0.0, 0.27), 0.003, 'ahsap')
        levha(y, [V(0.017, 0.0, 0.04), V(-0.105, 0.0, 0.05), V(-0.1, 0.0, 0.27), V(0.017, 0.0, 0.28)], 'kiremit2', Y)
        levha(y, [V(0.026, 0.0, 0.05), V(0.12, 0.0, 0.025), V(0.026, 0.0, 0.25)], 'kiremit', Y)
        cubuk(y, V(0.02, 0, 0.29), V(0.12, 0, 0.025), 0.0015, 'koyu')


mavna(0.32, -1.04, 0.05)
sandal(y, -0.32, -1.08, ZW, 0.4)
sandal(y, 0.82, -0.98, ZW, -0.3)
sandal(y, -0.75, -1.0, ZW, 2.6)

# ---------------------------------------------------------------- the palace: outer fronts
y.bolum('Saray: ırmak cephesi ve köşkler')
KOSK = (-0.73, -0.245, 0.245, 0.73)
KW = 0.14
segs = [(KOSK[i] + KW / 2, KOSK[i + 1] - KW / 2) for i in range(3)]
for x0, x1 in segs:
    cephe(V(x0, PY0), V(x1, PY0), 4, 'tam')
# the side fronts (west towards Westminster Hall, east towards the gardens) and the back
y.bolum('Batı cephe')
# (behind Westminster Hall only the upper storey shows over its eaves: the plainer bays there save the budget)
cephe(V(PX0, PY1), V(PX0, HY0_), 7, 'orta')
cephe(V(PX0, HY0_), V(PX0, CY0 - 0.02), 1, 'tam', cer=False)
y.bolum('Doğu ve arka cephe')
cephe(V(PX1, CY0 - 0.02), V(PX1, PY1), 8, 'orta')
cephe(V(PX1, PY1), V(PX0, PY1), 9, 'orta')
y.bolum('Avlular')
# the courts (walls facing in: walk each court clockwise)
for cx0, cx1 in CX:
    k = [V(cx0, CY0), V(cx0, CY1), V(cx1, CY1), V(cx1, CY0)]
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        n = max(2, int(round((b - a).length / 0.24)))
        cephe(a, b, n, 'sade' if i % 2 == 0 else 'bos', parapet=True)
    y.yuz_yon([V(cx0, CY0, Z0 + 0.0015), V(cx1, CY0, Z0 + 0.0015), V(cx1, CY1, Z0 + 0.0015), V(cx0, CY1, Z0 + 0.0015)], 'cimen', Z)
    for (u, v) in ((0.3, 0.3), (0.7, 0.7)):
        agac(y, cx0 + (cx1 - cx0) * u, CY0 + (CY1 - CY0) * v, Z0, boy=0.09)
# the parapets' tops round the ranges (the walls' tops behind the parapets, under the roofs, are hidden)
y.bolum('Saray çatıları')
zi = ZT + 0.002
R1 = cati(PX0 + 0.012, PX1 - 0.012, PY0 + 0.012, CY0 - 0.012, zi, 0.11, kres=False)                    # river range
cati(PX0 + 0.012, PX1 - 0.012, CY1 + 0.012, PY1 - 0.012, zi, 0.11)                             # back range
for x0, x1 in ((PX0 + 0.012, CX[0][0] - 0.012), (CX[1][1] + 0.012, PX1 - 0.012), (CX[0][1] + 0.012, CX[1][0] - 0.012)):  # side wings and the cross range
    w = x1 - x0
    cati(x0, x1, (PY0 + CY0) / 2 - 0.0, (CY1 + PY1) / 2, zi, min(0.11, w * 0.5))
y.bolum("Kresting")
for x0, x1 in segs:
    kresting(y, V(x0 + 0.01, (PY0 + CY0) / 2 - 0.006), V(x1 - 0.01, (PY0 + CY0) / 2 - 0.006), R1 + 0.004)
y.bolum("Havalandırma kuleleri")
# roof ventilators on the river range
for x in (-0.48, 0.0, 0.48):
    fleche(x, (PY0 + CY0) / 2, R1 - 0.01, 0.11)
for x in (-0.6, -0.36, 0.36, 0.6):
    fleche(x, (CY1 + PY1) / 2, ZT + 0.1, 0.08, 0.012)


def kosk(cx, w=KW, yon=-1, y_on=PY0 - 0.03, y_arka=CY0 - 0.02, ek=0.1, cati_h=0.15, acik=()):
    """a pavilion of the river front: one storey higher, an oriel window over the ground floor, corner turrets with
    spirelets, a steep pyramid roof with cresting and a gilded vane"""
    x0, x1 = cx - w / 2, cx + w / 2
    katlar = KAT + (ek,)
    z = Z0
    for j, h in enumerate(katlar):
        # the front: one wide bay, a three-light window
        gotik_pencere(y, V(x0, y_on), V(x1, y_on), z, h, RENK, en=0.56, v0=h * 0.18, sivri=0.3, mullion=1, cerceve=(0.004, TR), derin=0.018)
        # the sides: plain below the palace's roof line, windowed above it
        for a, b in ((V(x1, y_on), V(x1, y_arka)), (V(x0, y_arka), V(x0, y_on))):
            if j < len(KAT) and not ((a.x < cx and 'sol' in acik) or (a.x > cx and 'sag' in acik)):
                duz_duvar(y, a, b, z, z + h, DUV)
            else:
                gotik_pencere(y, a, b, z, h, RENK, en=0.45, v0=h * 0.2, sivri=0.3, mullion=1, cerceve=(0.003, TR), derin=0.014)
        if j == len(KAT):
            gotik_pencere(y, V(x1, y_arka), V(x0, y_arka), z, h, RENK, en=0.5, v0=h * 0.2, sivri=0.3, mullion=1, cerceve=(0.003, TR), derin=0.014)
        z += h
        silme(y, [V(x0, y_arka), V(x0, y_on), V(x1, y_on), V(x1, y_arka)], z - 0.004, 0.008, 0.006, TR, 'duz', kapali=False)
    silme(y, [V(x0, y_arka), V(x0, y_on), V(x1, y_on), V(x1, y_arka)], Z0, 0.022, 0.01, KO, 'kaide', kapali=False)
    # heraldic shields between the storeys
    # (set out in front of the storey moulding and the sills, with thickness: flat on the wall they were buried)
    for j in (1, 2):
        zz = Z0 + sum(KAT[:j]) + 0.011
        for s in (-0.3, 0.0, 0.3):
            c = V(cx + s * w, y_on, zz)
            sh = [V(-0.007, 0, 0.007), V(0.007, 0, 0.007), V(0.007, 0, -0.001), V(0, 0, -0.008), V(-0.007, 0, -0.001)]
            on = [c + p - Y * 0.0085 for p in sh]
            y.yuz_yon(on, 'boya_kirmizi' if s == 0 else 'altin', -Y)
            for i in range(5):
                p, q = on[i], on[(i + 1) % 5]
                m = (p + q) / 2 - c
                y.yuz_yon([p, q, q + Y * 0.006, p + Y * 0.006], TR, V(m.x, 0, m.z))
    # parapet, corner turrets, roof
    k = dikdortgen(x0, x1, y_on, y_arka)
    duvarlar(y, k, z, z + PH, DUV, ust=TR, kalinlik=0.01)
    for p in k:
        if p.y > y_on + 1e-6:   # back corners: a plain pinnacle
            pinakl(y, p.x, p.y, z + PH, 0.02, 0.06, DUV, TR, 'altin')
            continue
        donel(y, (p.x, p.y), [(0.017, Z0 + sum(KAT) * 0.55), (0.017, z + 0.05), (0.021, z + 0.053), (0.021, z + 0.06)], DUV, n=6)
        y.yuz_yon([V(q.x, q.y, z + 0.06) for q in cokgen((p.x, p.y), 0.021, 6)], TR, Z)
        pinakl(y, p.x, p.y, z + 0.06, 0.03, 0.07, DUV, CATI, 'altin', n=6)
    zr = cati_kirma(y, x0 + 0.01, x1 - 0.01, y_on + 0.01, y_arka - 0.01, z + 0.004, cati_h, 0.004, CATI, mahya='demir', kalinlik=0.006,
                    alt_key=KO, ns=2, nr=3, mahya_en=0.006)
    y.prizma((cx, (y_on + y_arka) / 2), 0.0025, zr, zr + 0.06, 'demir', n=4)
    kure(y, (cx, (y_on + y_arka) / 2, zr + 0.03), 0.007, 'altin', n=6, kat=3)
    return zr


y.bolum("Köşkler")
for i, cx in enumerate(KOSK):
    kosk(cx, acik=('sol',) if i == 0 else ('sag',) if i == 3 else ())

# ---------------------------------------------------------------- the Central Tower (octagonal lantern and spire)
y.bolum('Merkez kule')
OC = (0.0, 0.02)
R0 = 0.135
ok = cokgen(OC, R0, 8, math.pi / 8)
z = Z0
for j, h in enumerate(KAT + (0.07,)):
    for i in range(8):
        a, b = ok[i], ok[(i + 1) % 8]
        if j < len(KAT):
            duz_duvar(y, a, b, z, z + h, DUV)     # (inside the ranges and courts: only the court faces show, plain)
        else:
            gotik_pencere(y, a, b, z, h, RENK, en=0.42, v0=h * 0.2, sivri=0.3, mullion=0, cerceve=(0.003, TR), derin=0.012, hood=False)
    z += h
silme(y, ok, z - 0.012, 0.012, 0.008, TR, 'tac')
zl = z
R1_ = 0.11
lk = cokgen(OC, R1_, 8, math.pi / 8)
y.yuz_yon([V(p.x, p.y, zl) for p in ok], TR, Z)   # (the ring between the base and the lantern: under the lantern it is hidden)
HL = 0.17
for i in range(8):
    gotik_pencere(y, lk[i], lk[(i + 1) % 8], zl, HL, RENK, en=0.56, v0=0.02, sivri=0.4, mullion=1, cerceve=(0.004, TR), derin=0.008)
for p in ok:
    pinakl(y, p.x, p.y, zl, 0.022, 0.11, DUV, TR, 'altin')
for p in lk:
    payanda(y, p, (p - V(*OC)).normalized().cross(Z) * -1, (p - V(*OC)).normalized(), zl, zl + HL, w=0.014, d=0.01, key=DUV, pin=0.06, pin_key=TR, basamak=False, arka=True)
zs = zl + HL
silme(y, lk, zs - 0.01, 0.01, 0.008, TR, 'tac')
y.yuz_yon([V(p.x, p.y, zs) for p in lk], TR, Z)
SH = 0.37
donel(y, OC, [(R1_ * 0.98, zs), (R1_ * 0.74, zs + SH * 0.3), (R1_ * 0.46, zs + SH * 0.6), (R1_ * 0.2, zs + SH * 0.85), (0.0, zs + SH)], DUV, n=8, kat=math.pi / 8)
for t, rr in ((0.3, 0.74), (0.6, 0.46), (0.85, 0.2)):   # crocket bands
    halka_kornis(y, OC, R1_ * rr, zs + SH * t - 0.004, 0.008, 0.006, 8, TR, kat=math.pi / 8)
for i in range(8):   # lucarnes at the spire's foot
    t = math.pi / 8 + TAU * (i + 0.5) / 8
    n_ = V(math.cos(t), math.sin(t)); e_ = V(-n_.y, n_.x)
    m = V(*OC) + n_ * (R1_ * 0.88)
    A, B = m - e_ * 0.018 + Z * (zs + 0.012), m + e_ * 0.018 + Z * (zs + 0.012)
    T = m + Z * (zs + 0.07)
    y.yuz_yon([A, B, T], TR, n_)
    y.yuz_yon([m - e_ * 0.009 + n_ * 0.001 + Z * (zs + 0.016), m + e_ * 0.009 + n_ * 0.001 + Z * (zs + 0.016), m + n_ * 0.001 + Z * (zs + 0.05)], 'koyu', n_)
    for P_, Q_ in ((A, T), (T, B)):
        y.yuz_yon([P_, Q_, Q_ - n_ * 0.03, P_ - n_ * 0.03], DUV, (P_ + Q_) / 2 - (A + B) / 2 + n_ * 0.3)
kure(y, (OC[0], OC[1], zs + SH + 0.01), 0.012, 'altin', n=8, kat=4)
y.prizma(OC, 0.003, zs + SH, zs + SH + 0.06, 'altin', n=4)

# ---------------------------------------------------------------- Westminster Hall
y.bolum('Westminster Hall')
HX0, HX1, HY0, HY1 = -1.15, -0.89, -0.3, 0.95
HZ = Z0 + 0.2
HT = 'tas'
nb = 9
for (a, b, tur) in ((V(HX0, HY1), V(HX0, HY0), 1), (V(HX1, HY0), V(HX1, HY1), 0)):
    a, b, L, e, nc = eksen(a, b)
    for k in range(nb):
        p, q = a.lerp(b, k / nb), a.lerp(b, (k + 1) / nb)
        duz_duvar(y, p, q, Z0, Z0 + 0.09, HT)
        if not tur:
            duz_duvar(y, p, q, Z0 + 0.09, HZ, HT); continue
        gotik_pencere(y, p, q, Z0 + 0.09, HZ - Z0 - 0.09, (HT, 'tas_koyu', 'tas_acik', 'cam'), en=0.5, v0=0.01, sivri=0.35, mullion=1 if tur else 0,
                      cerceve=(0.003, 'tas_acik') if tur else None, hood=bool(tur), derin=0.014)
    for k in range(nb + 1):
        payanda(y, a.lerp(b, k / nb) + e * (0.009 if k == 0 else -0.009 if k == nb else 0), e, nc, Z0, HZ - 0.01, w=0.018, d=0.022, key=HT, pin=0.0)
    silme(y, [a, b], Z0, 0.02, 0.01, 'tas_koyu', 'kaide', kapali=False)
    silme(y, [a, b], HZ - 0.01, 0.01, 0.008, 'tas_acik', 'tac', kapali=False)
# the south end (against the palace, seen from behind): plain with a window
gotik_pencere(y, V(HX1, HY1), V(HX0, HY1), Z0, HZ - Z0, (HT, 'tas_koyu', 'tas_acik', 'cam'), en=0.5, v0=0.06, sivri=0.4, mullion=3, derin=0.016)
# the north front: the great window over the doorway between two square towers
NW = HX1 - HX0
_, _, _, Lp = y.kemerli(V(HX0 + 0.06, HY0), V(HX1 - 0.06, HY0), Z0, HZ - Z0, (HT, 'tas_koyu', 'tas_acik', 'ahsap'), v0=0.0, en=0.45, ust=0.12,
                        derin=0.03, k_say=8, sivri=0.4, cerceve=(0.006, ['tas_acik', 'tas']))
zr_h = cati_besik(y, HX0, HX1, HY0, HY1, HZ, 0.21, 0.012, CATI, mahya='demir', kalinlik=0.01, alt_key='ahsap_koyu', ucluk_key=HT, nr=5, ns=8,
                  alinlik_key='tas_acik')
# the great north window in the gable
gw = [V(HX0 + 0.06, HY0 - 0.0018, HZ + 0.005), V(HX1 - 0.06, HY0 - 0.0018, HZ + 0.005)]
cw = (HX0 + HX1) / 2
pts = [V(HX0 + 0.075, HY0 - 0.0018, HZ - 0.06), V(HX1 - 0.075, HY0 - 0.0018, HZ - 0.06), V(HX1 - 0.075, HY0 - 0.0018, HZ + 0.04),
       V(cw + 0.03, HY0 - 0.0018, HZ + 0.12), V(cw, HY0 - 0.0018, HZ + 0.135), V(cw - 0.03, HY0 - 0.0018, HZ + 0.12), V(HX0 + 0.075, HY0 - 0.0018, HZ + 0.04)]
y.yuz_yon(pts, 'tas_acik', -Y)
pi_ = [V(p.x + (cw - p.x) * 0.1, HY0 - 0.0032, p.z + (0.006 if p.z < HZ else -0.004)) for p in pts]
y.yuz_yon(pi_, 'cam', -Y)
for k in range(1, 6):
    x = HX0 + 0.08 + (NW - 0.16) * k / 6
    cubuk(y, V(x, HY0 - 0.0045, HZ - 0.055), V(x, HY0 - 0.0045, HZ + 0.12 - abs(x - cw) * 1.4), 0.003, 'tas_acik', 0.002)
for zz in (HZ - 0.015, HZ + 0.035):
    cubuk(y, V(HX0 + 0.08, HY0 - 0.0045, zz), V(HX1 - 0.08, HY0 - 0.0045, zz), 0.003, 'tas_acik', 0.002)
for sx in (HX0 + 0.03, HX1 - 0.03):   # the towers flanking the north front
    kule_kare(y, sx, HY0 + 0.02, 0.06, Z0, HZ + 0.1 - Z0, key=HT, cati='duz', mazgal_h=0.018)
# dormers along both slopes (the slope rises 0.21 over the half span 0.13 + eave)
for yy in (-0.05, 0.2, 0.45, 0.7):
    for sx in (-1, 1):
        hw = (HX1 - HX0) / 2
        cx_ = (HX0 + HX1) / 2 + sx * hw * 0.72
        dormer(y, (cx_, yy), (sx, 0), HZ + 0.21 * (1 - hw * 0.72 / (hw + 0.012)), 0.04, 0.034, 0.06, HT, CATI, 'koyu', 'tas_acik')
# a louvre lantern on the ridge
lc = (cw, (HY0 + HY1) / 2)
donel(y, lc, [(0.03, zr_h - 0.02), (0.03, zr_h + 0.03)], HT, n=6)
for i in range(6):
    t = TAU * (i + 0.5) / 6
    p = V(lc[0] + 0.0302 * math.cos(t), lc[1] + 0.0302 * math.sin(t), zr_h)
    d_ = V(-math.sin(t), math.cos(t)) * 0.007
    y.yuz_yon([p - d_, p + d_, p + d_ + Z * 0.022, p - d_ + Z * 0.022], 'koyu', V(math.cos(t), math.sin(t)))
donel(y, lc, [(0.038, zr_h + 0.03), (0.0, zr_h + 0.075)], CATI, n=6)
kure(y, (lc[0], lc[1], zr_h + 0.08), 0.006, 'altin', n=6, kat=3)
# New Palace Yard: trees, a fountain basin, railings
for (x, yy) in ((-1.05, -0.42), (-0.86, -0.4), (-1.15, -0.5)):
    agac(y, x, yy, Z0, boy=0.1)
y.prizma((-0.84, 0.86), 0.04, Z0, Z0 + 0.014, TR, n=12)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0145) for p in cokgen((-0.84, 0.86), 0.034, 12)], 'su', Z)
y.prizma((-0.84, 0.86), 0.006, Z0, Z0 + 0.05, TR, n=6)

# ---------------------------------------------------------------- the Elizabeth Tower (Big Ben)
y.bolum('Saat Kulesi (Big Ben)')
EX, EY, EW = -0.975, -0.63, 0.165
h_ = EW / 2
ZC0 = 0.9          # clock stage
ZC1 = ZC0 + 0.17
ZB0 = ZC1 + 0.035   # belfry
ZB1 = ZB0 + 0.1
ek_ = dikdortgen(EX - h_, EX + h_, EY - h_, EY + h_)
# the plinth
kutu_merkez(y, (EX, EY), EW + 0.03, EW + 0.03, 0.03, 'granit', z0=Z0, yuzler='onarkasagsolust')
silme(y, dikdortgen(EX - h_ - 0.015, EX + h_ + 0.015, EY - h_ - 0.015, EY + h_ + 0.015), Z0 + 0.024, 0.008, 0.005, TR, 'duz')
# the shaft: tiers of narrow panelled lights between corner shafts, string courses
z = Z0 + 0.03
tiers = [0.09] + [0.13] * 6
tiers[-1] = ZC0 - z - sum(tiers[:-1])
for j, h in enumerate(tiers):
    for i in range(4):
        a, b, L, e, nc = eksen(ek_[i], ek_[(i + 1) % 4])
        a2, b2 = a + e * 0.012, b - e * 0.012
        duz_duvar(y, a, a2, z, z + h, DUV)
        duz_duvar(y, b2, b, z, z + h, DUV)
        for k in range(3):
            p, q = a2.lerp(b2, k / 3), a2.lerp(b2, (k + 1) / 3)
            if j == 0:
                y.kemerli(p, q, z, h, (DUV, KO, TR, KO), v0=0.008, en=0.62, ust=0.01, derin=0.006, k_say=4, sivri=0.4)
            else:
                lite = (j % 2 == 1)
                y.kemerli(p, q, z, h, (DUV, KO, TR, 'cam' if lite and k == 1 else KO), v0=0.006, en=0.6 if lite else 0.66, ust=0.008,
                          derin=0.008 if lite else 0.005, k_say=4, sivri=0.45, cerceve=(0.0025, TR) if lite and k == 1 else None)
    z += h
    silme(y, ek_, z - 0.004, 0.006, 0.004, TR, 'duz')
for p in ek_:   # corner shafts (clasping buttresses)
    kutu_merkez(y, (p.x, p.y), 0.022, 0.022, ZC0 - Z0 - 0.03, DUV, z0=Z0 + 0.03, yuzler='onarkasagsolust')
# the clock stage: a little wider, the four gilded clock faces, crowned by a cornice
cw2 = EW + 0.014
ck = dikdortgen(EX - cw2 / 2, EX + cw2 / 2, EY - cw2 / 2, EY + cw2 / 2)
silme(y, ck, ZC0 - 0.02, 0.02, 0.008, TR, 'kaba')
duvarlar(y, ck, ZC0, ZC1, DUV)
for i in range(4):
    a, b, L, e, nc = eksen(ck[i], ck[(i + 1) % 4])
    o = (a + b) / 2 + Z * (ZC0 + 0.088)
    kadran(y, o, e, nc, 0.052, cerceve=0.068)
    # gilded tracery band under the dial and the inscription ribbon over it
    y.yuz_yon([a + e * 0.012 + nc * 0.0012 + Z * (ZC0 + 0.006), b - e * 0.012 + nc * 0.0012 + Z * (ZC0 + 0.006), b - e * 0.012 + nc * 0.0012 + Z * (ZC0 + 0.016),
               a + e * 0.012 + nc * 0.0012 + Z * (ZC0 + 0.016)], 'altin', nc)
    for k in range(9):
        m = a.lerp(b, 0.12 + 0.76 * (k + 0.5) / 9) + nc * 0.0018 + Z * (ZC0 + 0.011)
        y.yuz_yon([m - e * 0.003 + Z * -0.003, m + e * 0.003 - Z * 0.003, m + Z * 0.004], 'kobalt', nc)
    y.yuz_yon([a + e * 0.012 + nc * 0.0012 + Z * (ZC1 - 0.012), b - e * 0.012 + nc * 0.0012 + Z * (ZC1 - 0.012), b - e * 0.012 + nc * 0.0012 + Z * (ZC1 - 0.004),
               a + e * 0.012 + nc * 0.0012 + Z * (ZC1 - 0.004)], 'altin', nc)
for p in ck:
    kutu_merkez(y, (p.x, p.y), 0.024, 0.024, ZC1 - ZC0, DUV, z0=ZC0, yuzler='onarkasagsolust')
silme(y, ck, ZC1, 0.016, 0.01, TR, 'kaba')
y.yuz_yon([V(p.x, p.y, ZC1 + 0.016) for p in disa(ck, 0.01)], TR, Z)
# a gallery of little pinnacles on the clock stage's cornice
for i in range(4):
    a, b, L, e, nc = eksen(ck[i], ck[(i + 1) % 4])
    for k in range(3):
        p = a.lerp(b, (k + 0.5) / 3) + nc * 0.004
        pinakl(y, p.x, p.y, ZC1 + 0.016, 0.01, 0.03, DUV, 'altin', None)
# the belfry: three tall open lights a side with gilded frames, the bells inside (dark)
bw = EW - 0.01
bk = dikdortgen(EX - bw / 2, EX + bw / 2, EY - bw / 2, EY + bw / 2)
duvarlar(y, bk, ZC1 + 0.016, ZB0, DUV)
for i in range(4):
    a, b, L, e, nc = eksen(bk[i], bk[(i + 1) % 4])
    for k in range(3):
        p, q = a.lerp(b, k / 3), a.lerp(b, (k + 1) / 3)
        gotik_pencere(y, p, q, ZB0, ZB1 - ZB0, (DUV, KO, 'altin', 'koyu'), en=0.64, v0=0.012, sivri=0.45, mullion=1, cerceve=(0.003, 'altin'), derin=0.007,
                      hood=False)
silme(y, bk, ZB0 - 0.004, 0.008, 0.006, TR, 'duz')
for p in bk:
    pinakl(y, p.x, p.y, ZB0, 0.022, ZB1 - ZB0 + 0.07, DUV, 'altin', 'altin')
silme(y, bk, ZB1, 0.012, 0.008, TR, 'tac')
# the spire: a steep slate pyramid with gilded ribs and lucarnes, a little open lantern, the upper spire and the finial
ZS = ZB1 + 0.012
SH1 = 0.17
zt_ = cati_kirma(y, EX - bw / 2, EX + bw / 2, EY - bw / 2, EY + bw / 2, ZS, SH1 / 0.62, 0.006, CATI, mahya='altin', kalinlik=0.006, alt_key=TR,
                 ns=6, nr=6, r_ust=0.62, mahya_en=0.006)
sw = bw * 0.38
y.yuz_yon([V(p.x, p.y, ZS + SH1) for p in dikdortgen(EX - sw, EX + sw, EY - sw, EY + sw)], CATI, Z)
for i in range(4):   # lucarnes (small gabled dormers with dark openings and gilded frames)
    a, b, L, e, nc = eksen(bk[i], bk[(i + 1) % 4])
    m = (a + b) / 2 - nc * 0.004
    zz = ZS + 0.01
    w2 = 0.022
    for (pa, pb) in ((m - e * w2, m + e * w2),):
        y.yuz_yon([pa + Z * zz, pb + Z * zz, pb + Z * (zz + 0.035), pa + Z * (zz + 0.035)], 'altin', nc)
        y.yuz_yon([pa + nc * 0.001 + e * 0.006 + Z * (zz + 0.005), pb + nc * 0.001 - e * 0.006 + Z * (zz + 0.005), pb + nc * 0.001 - e * 0.006 + Z * (zz + 0.028),
                   pa + nc * 0.001 + e * 0.006 + Z * (zz + 0.028)], 'koyu', nc)
        T = m + Z * (zz + 0.06)
        y.yuz_yon([pa + Z * (zz + 0.035), pb + Z * (zz + 0.035), T], 'altin', nc)
        for s, P_ in ((-1, pa), (1, pb)):
            y.yuz_yon([P_ + Z * zz, P_ - nc * 0.04 + Z * zz, P_ - nc * 0.04 + Z * (zz + 0.035), P_ + Z * (zz + 0.035)], CATI, e * s)
            y.yuz_yon([P_ + Z * (zz + 0.035), T, T - nc * 0.045, P_ - nc * 0.04 + Z * (zz + 0.035)], CATI, e * s + Z)
zl2 = ZS + SH1
lw = sw * 0.9
lkk = dikdortgen(EX - lw, EX + lw, EY - lw, EY + lw)
for i in range(4):   # the open lantern (the Ayrton light)
    a, b, L, e, nc = eksen(lkk[i], lkk[(i + 1) % 4])
    gotik_pencere(y, a, b, zl2, 0.05, ('altin', 'koyu', 'altin', 'koyu'), en=0.6, v0=0.004, sivri=0.45, mullion=0, cerceve=None, derin=0.006, hood=False)
silme(y, lkk, zl2 + 0.046, 0.008, 0.005, 'altin', 'duz')
z2 = zl2 + 0.054
cati_kirma(y, EX - lw, EX + lw, EY - lw, EY + lw, z2, 0.13, 0.004, CATI, mahya='altin', kalinlik=0.004, alt_key='altin', ns=3, nr=5, mahya_en=0.005)
ztop = z2 + 0.13
y.prizma((EX, EY), 0.003, ztop - 0.01, ztop + 0.05, 'altin', n=4)
kure(y, (EX, EY, ztop + 0.02), 0.009, 'altin', n=8, kat=4)
cubuk(y, V(EX - 0.012, EY, ztop + 0.04), V(EX + 0.012, EY, ztop + 0.04), 0.003, 'altin')
for p in bk:   # corner spirelets at the spire's foot
    pinakl(y, p.x, p.y, ZB1 + 0.07, 0.016, 0.06, 'altin', CATI, 'altin', n=8)
# the link from the tower to the palace
LY0, LY1 = EY - 0.035, EY + 0.05
zl_ = cephe(V(EX + h_, LY0), V(PX0, LY0), 1, 'orta', katlar=KAT[:2])
cephe(V(PX0, LY1), V(EX + h_, LY1), 1, 'sade', katlar=KAT[:2])
y.yuz_yon([V(EX + h_, LY0, zl_ + 0.002), V(PX0, LY0, zl_ + 0.002), V(PX0, LY1, zl_ + 0.002), V(EX + h_, LY1, zl_ + 0.002)], 'kursun', Z)

# ---------------------------------------------------------------- the Victoria Tower
y.bolum('Victoria Kulesi ve sancak')
VX, VY, VW = 0.99, 0.23, 0.26
vh = VW / 2
vk = dikdortgen(VX - vh, VX + vh, VY - vh, VY + vh)
ZV = 1.0
kutu_merkez(y, (VX, VY), VW + 0.024, VW + 0.024, 0.026, 'granit', z0=Z0)
z = Z0 + 0.026
# the Sovereign's Entrance (a great arch on the front and the sides)
H0 = 0.27
for i in range(4):
    a, b, L, e, nc = eksen(vk[i], vk[(i + 1) % 4])
    a2, b2 = a + e * 0.03, b - e * 0.03
    duz_duvar(y, a, a2, z, z + H0, DUV)
    duz_duvar(y, b2, b, z, z + H0, DUV)
    if i in (0, 1):
        y.kemerli(a2, b2, z, H0, (DUV, KO, TR, 'ahsap' if i == 0 else KO), v0=0.0, en=0.6, ust=0.06, derin=0.05, k_say=10, sivri=0.42,
                  cerceve=(0.008, [TR, DUV]))
        m = (a + b) / 2
        for s in (-1, 1):   # statues in niches over the arch
            c = m + e * (s * 0.045) + nc * 0.0015 + Z * (z + H0 - 0.03)
            y.yuz_yon([c - e * 0.01 - Z * 0.022, c + e * 0.01 - Z * 0.022, c + e * 0.01 + Z * 0.012, c + Z * 0.02, c - e * 0.01 + Z * 0.012], KO, nc)
            insan(y, c.x + nc.x * 0.004, c.y + nc.y * 0.004, c.z - 0.022, TR, 0.9, aci=math.atan2(nc.y, nc.x))
    else:
        gotik_pencere(y, a2, b2, z, H0, RENK, en=0.5, v0=0.08, sivri=0.4, mullion=2, cerceve=(0.004, TR), derin=0.02)
z += H0
silme(y, vk, z - 0.006, 0.012, 0.008, TR, 'kaba')
# upper tiers: tall windows (three a side), shields and panelled bands between
for j, h in enumerate((0.24, 0.21)):
    for i in range(4):
        a, b, L, e, nc = eksen(vk[i], vk[(i + 1) % 4])
        a2, b2 = a + e * 0.03, b - e * 0.03
        duz_duvar(y, a, a2, z, z + h, DUV)
        duz_duvar(y, b2, b, z, z + h, DUV)
        for k in range(3):
            p, q = a2.lerp(b2, k / 3), a2.lerp(b2, (k + 1) / 3)
            gotik_pencere(y, p, q, z, h, RENK, en=0.56, v0=0.03, sivri=0.38, mullion=1, cerceve=None, derin=0.016)
        for k in range(4):   # a row of heraldic shields at the foot of each tier
            c = a2.lerp(b2, (k + 0.5) / 4) + nc * 0.0016 + Z * (z + 0.014)
            y.yuz_yon([c + e * -0.007 + Z * 0.008, c + e * 0.007 + Z * 0.008, c + e * 0.007, c - Z * 0.008, c - e * 0.007], 'boya_kirmizi' if k % 2 else 'altin', nc)
    z += h
    silme(y, vk, z - 0.005, 0.01, 0.007, TR, 'duz')
zp = z
silme(y, vk, zp - 0.012, 0.014, 0.012, TR, 'tac')
duvarlar(y, vk, zp, zp + 0.04, DUV, ust=TR, kalinlik=0.014)
y.yuz_yon([V(p.x, p.y, zp + 0.002) for p in disa(vk, -0.014)], 'kursun', Z)
for i in range(4):   # pierced parapet look and pinnacles along it
    a, b, L, e, nc = eksen(vk[i], vk[(i + 1) % 4])
    for k in range(7):
        c = a.lerp(b, (k + 0.5) / 7) + nc * 0.0012 + Z * (zp + 0.02)
        y.yuz_yon([c - e * 0.009 - Z * 0.012, c + e * 0.009 - Z * 0.012, c + e * 0.009 + Z * 0.006, c + Z * 0.014, c - e * 0.009 + Z * 0.006], KO, nc)
    for k in (1, 2):
        p = a.lerp(b, k / 3) + nc * 0.006
        pinakl(y, p.x, p.y, zp + 0.04, 0.016, 0.07, DUV, TR, 'altin')
# corner turrets: octagonal, rising above the parapet with spirelets
for p in vk:
    donel(y, (p.x, p.y), [(0.032, Z0 + 0.026), (0.03, zp + 0.08)], DUV, n=8, kat=math.pi / 8)
    for zz in (Z0 + 0.026 + H0, zp - 0.17, zp):
        halka_kornis(y, (p.x, p.y), 0.03, zz - 0.004, 0.008, 0.005, 8, TR, kat=math.pi / 8)
    silme(y, cokgen((p.x, p.y), 0.03, 8, math.pi / 8), zp + 0.08, 0.012, 0.008, TR, 'tac')
    donel(y, (p.x, p.y), [(0.034, zp + 0.092), (0.02, zp + 0.13), (0.0, zp + 0.2)], CATI, n=8, kat=math.pi / 8)
    kure(y, (p.x, p.y, zp + 0.205), 0.008, 'altin', n=6, kat=3)
# the flagstaff
sancak(y, VX, VY, zp + 0.002, boy=0.27, en=0.18, yuk=0.11, aci=math.pi * 0.9, direk_key='beyaz', tepe_key='altin', n=7)

# ---------------------------------------------------------------- Old Palace Yard: Richard the Lionheart, lamps
y.bolum('Cromwell heykeli ve fenerler')
kutu_merkez(y, (0.1, 0.9), 0.05, 0.05, 0.06, 'granit', z0=Z0)
silme(y, dikdortgen(0.075, 0.125, 0.875, 0.925), Z0 + 0.052, 0.008, 0.005, TR, 'duz')
insan(y, 0.1, 0.9, Z0 + 0.06, 'bronz', 1.8, ten='bronz', aci=-math.pi / 2)
cubuk(y, V(0.112, 0.89, Z0 + 0.065), V(0.114, 0.89, Z0 + 0.115), 0.003, 'bronz')
for x in (-0.5, -0.2, 0.4, 0.7):
    fener(y, x, 0.76, Z0, h=0.09)
for (x, yy) in ((0.95, -0.7), (1.1, -0.5), (0.93, -0.32), (1.1, -0.15), (0.92, 0.6), (1.1, 0.8), (0.95, 0.95)):
    agac(y, x, yy, Z0, boy=0.13)

calistir(y, 'lm_bigben')
