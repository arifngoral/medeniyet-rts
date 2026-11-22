# Beytülhikme (lm_beytulhikme): the Abbasid House of Wisdom as a four-iwan court of yellow brick: a towering muqarnas
# pishtaq between two slender tiled minarets, two-storey ranges of blind arches outside; round the court the four
# iwans rising above the roofs, the lower galleries opened as reading rooms with shelves of coloured books, upper
# windows with lattices; the domed hall behind the qibla iwan under a pointed turquoise dome; the observatory tower
# with its loggia and a gilded armillary sphere; a court with a fountain pool and garden beds, a front garden of pools,
# cypresses and palms.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.05
T, TK, TA = 'tugla_sari', 'tugla_sari_koyu', 'kum_acik'
XW, YF, YB = 0.72, -0.62, 0.72          # the block
IX, IYF, IYB = 0.48, -0.39, 0.47        # the court (wide: the iwans need room round it)
H1, H2 = 0.17, 0.15
HW = H1 + H2                            # range height
HI = 0.54                               # iwans
IW = 0.3                                # iwan width

y.bolum('Zemin ve bahçe')
zemin(y, -1.12, 1.12, -1.12, 1.06, Z0, 'kum_koyu', 'zemin', basamak=(('on', 0.5),), n_basamak=3)


# ---------------- helpers ----------------
def yildiz(o, ex, nrm, r, key, k=8, ic=0.5, d=0.0015, kat=0.0, yan_key=None):
    """a raised star / lozenge: o on the surface, ex along it, nrm out (d < 0.002: a flat inlay)"""
    o, ex, nrm = V(*o), V(*ex), V(*nrm)
    up = nrm.cross(ex).normalized()
    pts = [o + ex * ((r if i % 2 == 0 else r * ic) * math.cos(kat + math.pi * i / k)) + up * ((r if i % 2 == 0 else r * ic) * math.sin(kat + math.pi * i / k)) for i in range(2 * k)]
    y.yuz_yon([p + nrm * d for p in pts], key, nrm)
    if d < 0.002: return
    for i in range(2 * k):
        p, q = pts[i], pts[(i + 1) % (2 * k)]
        y.yuz_yon([p, q, q + nrm * d, p + nrm * d], yan_key or key, (p + q) / 2 - o)


def kademeli_mazgal(a, b, z, t=0.018, key=T, w=0.058, g=0.026):
    """stepped merlons along a->b (outer face on the line): a wide block and a narrow one on it"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g
    for i in range(k):
        o = a + e * (i * (w + g))
        kutu(y, o + Z * z, e, w, t, 0.016, key)
        kutu(y, o + e * (w * 0.22) + Z * (z + 0.016), e, w * 0.56, t, 0.012, key)


def ust_bitis(kose, z, kapali=False, key=T, mazgal=True):
    """a crowning cornice under z, a solid parapet band and stepped merlons"""
    silme(y, kose, z - 0.018, 0.02, 0.012, TA, 'tac', kapali=kapali)
    parapet(y, kose, z, 0.014, 0, 0.018, key, kapali=kapali, ust_key=TA)
    if mazgal:
        n = len(kose)
        for i in range(n if kapali else n - 1):
            kademeli_mazgal(kose[i], kose[(i + 1) % n], z + 0.014)


def havuz2(ic, kenar, z0, key, h=0.02):
    """a pool: a kerb round the CCW polygon ic, its inner faces down to the water a little below the top"""
    dis = disa(ic, kenar)
    zt, zs = z0 + h, z0 + h * 0.45
    duvarlar(y, dis, z0, zt, key)
    n = len(ic)
    for i in range(n):
        j = (i + 1) % n
        duz_duvar(y, ic[j], ic[i], zs, zt, key)
        y.yuz_yon([dis[i] + Z * zt, dis[j] + Z * zt, ic[j] + Z * zt, ic[i] + Z * zt], key, Z)
    y.yuz_yon([V(p.x, p.y, zs) for p in ic], 'su', Z)


def palmiye(x, yy, z, boy=0.3):
    tepe = V(x + 0.012, yy + 0.006, z + boy)
    boru(y, [V(x, yy, z), V(x + 0.004, yy + 0.002, z + boy * 0.5), tepe], 0.009, 'ahsap_acik', n=6, r_son=0.007)
    for i in range(7):
        a = TAU * i / 7 + 0.3
        d = V(math.cos(a), math.sin(a))
        L = 0.085 + 0.015 * (i % 2)
        boru(y, [tepe, tepe + d * (L * 0.45) + Z * 0.03, tepe + d * L - Z * 0.02, tepe + d * (L * 1.12) - Z * 0.05], 0.009, 'boya_yesil', n=3, r_son=0.002)
    kure(y, (tepe.x, tepe.y, tepe.z + 0.004), 0.012, 'boya_yesil', n=8, kat=4)


def bant(o, ex, nrm, L, h, key='turkuaz', d=0.0015, lozenge='beyaz', n=None):
    """a glazed band on a flat wall (o = its bottom-left on the wall), white lozenges along it"""
    o, ex, nrm = V(*o), V(*ex).normalized(), V(*nrm).normalized()
    y.yuz_yon([o + nrm * d, o + ex * L + nrm * d, o + ex * L + Z * h + nrm * d, o + Z * h + nrm * d], key, nrm)
    if lozenge:
        n = n or max(1, int(L / (h * 1.8)))
        for i in range(n):
            yildiz(o + ex * (L * (i + 0.5) / n) + Z * (h / 2) + nrm * d, ex, nrm, h * 0.38, lozenge, k=2, ic=0.45, d=0.0008)


# ---------------- outer ranges ----------------
y.bolum('Dış cepheler: iki katlı kör kemerler')
BK = dikdortgen(-XW, XW, YF, YB)
PW, PH, PD = 0.48, 0.74, 0.09


def dis_bay(p, q):
    """an outer bay: a tall blind pointed niche through both storeys, a square window below, an arched one above
    with a glazed spandrel roundel"""
    L_, x0, x1, hs, apex = kemer_nis(y, p, q, Z0, HW - 0.02, en=0.7, ust=0.025, sivri=0.5, derin=0.016, key=T, yan_key=TK,
                                     alt_key=TA, v0=0.03, k_say=10, cerceve=(0.006, [TA, 'turkuaz']))
    a2, b2 = L_(x0, -Z0, 0.016), L_(x1, -Z0, 0.016)
    dikdortgen_acik(y, a2, b2, Z0 + 0.03, H1 - 0.03, 0.3, 0.7, 0.03, 0.1, (T, TK, TA, 'koyu'), derin=0.012, cerceve=(0.005, TA))
    y.kemerli(a2, b2, Z0 + H1, apex - H1, (T, TK, TA, 'koyu'), v0=0.02, en=0.34, ust=0.02, derin=0.012, k_say=6, sivri=0.55)
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    kutu(y, L_(0, H1 - 0.004, 0) + nn * 0.004, e, (q - p).length, 0.004, 0.007, TA, 'onust')
    duz_duvar(y, p, q, Z0 + HW - 0.02, Z0 + HW, T)


for i in range(4):
    a, b = BK[i], BK[(i + 1) % 4]
    n = (6, 7, 8, 7)[i]
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if i == 0 and k in (2, 3):
            continue
        if i == 2 and k in (3, 4):
            duz_duvar(y, p, q, Z0, Z0 + HW, T)        # (the domed hall stands against it)
            continue
        dis_bay(p, q)
silme(y, BK, Z0, 0.024, 0.012, TK, 'kaide')
ust_bitis([V(-XW, YF), V(-PW / 2, YF)], Z0 + HW)
ust_bitis([V(PW / 2, YF), V(XW, YF), V(XW, YB), V(0.18, YB)], Z0 + HW)
ust_bitis([V(-0.18, YB), V(-XW, YB), V(-XW, YF)], Z0 + HW)
# corner towers: round, a glazed band, a little turquoise dome
for p in BK:
    c = (p.x, p.y)
    donel(y, c, [(0.075, Z0), (0.075, Z0 + 0.03), (0.066, Z0 + 0.034), (0.062, Z0 + HW + 0.06)], T, n=16)
    R = lambda zz: 0.066 + (0.062 - 0.066) * (zz - Z0 - 0.034) / (HW + 0.026)
    zb = Z0 + HW + 0.012
    donel(y, c, [(R(zb), zb), (R(zb) + 0.0015, zb), (R(zb + 0.03) + 0.0015, zb + 0.03), (R(zb + 0.03), zb + 0.03)], 'turkuaz', n=16)
    halka_kornis(y, c, 0.062, Z0 + HW + 0.06, 0.012, 0.01, 16, TA)
    t = y.kubbe(c, 0.066, Z0 + HW + 0.072, 0.07, 'turkuaz', n=16, kat=5)
    kure(y, (c[0], c[1], t.z + 0.008), 0.008, 'altin', n=6, kat=3)

# ---------------- the portal ----------------
y.bolum('Mukarnaslı büyük taçkapı ve iki ince minare')
top_p = tackapi_mukarnas(y, 0, YF - PD, Z0, en=PW, H=PH, derin=PD, nis=0.56, sivri=0.55, mk_kat=6, kapi_key='ahsap', key=T,
                         bordur=('turkuaz', 'kobalt'), tonlar=(TA, TK), cerceve=(0.014, ['turkuaz', TA]))
duz_duvar(y, V(PW / 2, YF), V(-PW / 2, YF), Z0, Z0 + HW, T)
# the portal's back above the roof: a blind pointed niche in a glazed frame, a star in its head
kemer_nis(y, V(PW / 2, YF), V(-PW / 2, YF), Z0 + HW, PH - HW, en=0.62, ust=0.05, sivri=0.5, derin=0.005, key=T, yan_key=TK,
          alt_key=TA, arka_key=TK, v0=0.03, k_say=10, cerceve=(0.01, ['turkuaz', TA]))
yildiz((0, YF - 0.0048, Z0 + PH - 0.16), -X, Y, 0.035, 'turkuaz', k=8, ic=0.55)
bw = PW * 0.07
zb = Z0 + PH - 0.016
for sx in (-1, 1):
    n = 9
    for i in range(n):
        zz = Z0 + 0.04 + (zb - bw - Z0 - 0.06) * (i + 0.5) / n
        yildiz((sx * (PW / 2 - bw / 2), YF - PD - 0.006, zz), X, -Y, bw * 0.4, 'beyaz', k=6, kat=math.pi / 6)
for i in range(7):
    xx = -PW / 2 + bw + (PW - 2 * bw) * (i + 0.5) / 7
    yildiz((xx, YF - PD - 0.006, zb - bw / 2), X, -Y, bw * 0.4, 'beyaz', k=6, kat=math.pi / 6)
# an inscription panel (white kufic on lacivert) over the door, rosettes in the spandrels
hw = 0.56 * PW / 2 + 0.012 + bw * 0.6
for sx in (-1, 1):
    yildiz((sx * hw * 0.62, YF - PD - 0.0025, Z0 + PH * 0.88 - 0.035), X, -Y, 0.018, 'turkuaz', k=12, ic=0.72)


def minarecik(cx, cy, z0, h, r=0.03):
    """a slender tiled minaret: a brick shaft with glazed bands, a corbelled balcony, a lantern and a little dome"""
    donel(y, (cx, cy), [(r * 1.3, z0), (r * 1.3, z0 + 0.04), (r, z0 + 0.05), (r * 0.9, z0 + h)], T, n=12)
    R = lambda zz: r + (r * 0.9 - r) * (zz - z0 - 0.05) / (h - 0.05)
    for f in (0.35, 0.6, 0.8):
        zz = z0 + h * f
        donel(y, (cx, cy), [(R(zz), zz), (R(zz) + 0.0015, zz), (R(zz + 0.03) + 0.0015, zz + 0.03), (R(zz + 0.03), zz + 0.03)], 'turkuaz', n=12)
    zt = z0 + h
    ring = cokgen((cx, cy), r * 0.9, 12)
    konsol_halka(y, ring, zt - 0.025, 0.025, 0.018, TA, 3)
    rb = disa(ring, 0.018)
    y.yuz_yon([V(p.x, p.y, zt + 0.0008) for p in rb], TA, Z)
    parapet(y, rb, zt, 0.018, 0, 0.006, T, ust_key=TA)
    y.prizma((cx, cy), r * 0.7, zt, zt + 0.06, T, n=12, ust=False)
    for i in range(4):
        a = TAU * i / 4 + math.pi / 12
        kutu_merkez(y, (cx + math.cos(a) * r * 0.66, cy + math.sin(a) * r * 0.66), 0.006, 0.01, 0.03, 'koyu', z0=zt + 0.015, aci=a)
    halka_kornis(y, (cx, cy), r * 0.7, zt + 0.06, 0.008, 0.006, 12, TA)
    t = y.kubbe((cx, cy), r * 0.78, zt + 0.068, r * 1.1, 'turkuaz', n=12, kat=5)
    return alem(y, cx, cy, t.z, 0.5, hilal=False)


for sx in (-1, 1):
    minarecik(sx * (PW / 2 + 0.035), YF - 0.05, Z0, 0.92)

# ---------------- the court ----------------
y.bolum('Avlu: kitap salonları, üst kat pencereleri')


def kitap_bay(p, q, z0, H):
    """a reading-room bay opening on the court: a pointed arch, a wooden back of bookcases, three shelves of
    coloured books, a carpet on the floor"""
    L_, x0, x1, hs, apex = kemer_nis(y, p, q, z0, H, en=0.72, ust=0.018, sivri=0.5, derin=0.05, key=T, yan_key=TK, alt_key=TA,
                                     arka_key='ahsap_koyu', k_say=8, cerceve=(0.006, ['turkuaz', TA]))
    e = (q - p).normalized()
    w = x1 - x0
    renk = (('boya_kirmizi', 'lacivert', 'boya_yesil'), ('siva_oker', 'boya_kirmizi', 'ahsap'), ('lacivert', 'boya_sari', 'boya_kirmizi'))
    for j, v in enumerate((0.012, 0.045, 0.078)):
        kutu(y, L_(x0, v, 0.026), e, w, 0.024, 0.003, 'ahsap', 'onsagsolust')
        for i in range(3):
            ua, ub = x0 + w * i / 3 + 0.001, x0 + w * (i + 1) / 3 - 0.001
            hh = 0.024 - 0.004 * ((i + j) % 2)
            kutu(y, L_(ua, v + 0.003, 0.028), e, ub - ua, 0.02, hh, renk[j][i], 'onsagsolust')
    # a carpet on the gallery floor in front of the shelves
    y.yuz_yon([L_(x0 + 0.004, 0.003, 0.0), L_(x1 - 0.004, 0.003, 0.0), L_(x1 - 0.004, 0.003, 0.024), L_(x0 + 0.004, 0.003, 0.024)], 'boya_kirmizi', Z)


def ust_pencere(p, q, z0, H):
    """an upper-storey bay: an arched window with a turned-wood lattice"""
    W_, e, nc, L_ = y.kemerli(p, q, z0, H, (T, TK, TA, 'koyu'), v0=0.03, en=0.5, ust=0.02, derin=0.016, k_say=8, sivri=0.5,
                              cerceve=(0.006, [TA, 'turkuaz']))
    w = (q - p).length
    kafes(y, p, q, z0, 0.25 + 0.03, 0.75 - 0.03, 0.03, H * 0.55, 'ahsap_koyu', nu=3, nv=3, en=0.003, ileri=-0.008)


def iwan(D, H=HI, W=IW, arka='kitap'):
    """an iwan in local coordinates: the court line along x at y = 0 (the vault opens to -y), going D deep: the
    pishtaq frame with a glazed border, the tunnel vault, the back wall (a door and bookcases), the block above the
    roofs with its cornice and merlons"""
    L_, x0, x1, hs, apex = kemer_nis(y, V(-W / 2, 0), V(W / 2, 0), Z0, H, en=0.7, ust=0.07, sivri=0.55, derin=D, key=T, yan_key=TK,
                                     alt_key=TA, k_say=12, cerceve=(0.012, ['turkuaz', TA]))
    # the back wall: a framed door, a window over it
    y.kemerli(V(x0 - W / 2, D), V(x1 - W / 2, D), Z0, apex, (T, TK, TA, 'ahsap'), v0=0.0, en=0.42, ust=apex * 0.42, derin=0.012,
              k_say=8, sivri=0.5, cerceve=(0.007, 'turkuaz'))
    # the block above the ranges' roofs (its back a hair behind the vault's back wall: back to back they flickered)
    D2 = D + 0.004
    for xx, s in ((-W / 2, -1), (W / 2, 1)):
        a, b = (V(xx, D2), V(xx, 0)) if s < 0 else (V(xx, 0), V(xx, D2))
        duz_duvar(y, a, b, Z0 + HW, Z0 + H, T)
    duz_duvar(y, V(W / 2, D2), V(-W / 2, D2), Z0 + HW, Z0 + H, T)
    y.yuz_yon([V(-W / 2, 0, Z0 + H), V(W / 2, 0, Z0 + H), V(W / 2, D2, Z0 + H), V(-W / 2, D2, Z0 + H)], TA, Z)
    # the frame: raised glazed border round the pishtaq, rosettes, a kufic band under the cornice
    bw_ = 0.018
    for (u0, u1, v0, v1) in ((-W / 2, -W / 2 + bw_, 0.0, H - 0.03), (W / 2 - bw_, W / 2, 0.0, H - 0.03), (-W / 2, W / 2, H - 0.03 - bw_, H - 0.03)):
        kutu(y, V(u0, -0.005, Z0 + v0), X, u1 - u0, 0.005, v1 - v0, 'turkuaz', 'onsagsolust')
    for sx in (-1, 1):
        yildiz((sx * W * 0.3, -0.002, Z0 + apex - 0.012), X, -Y, 0.014, 'beyaz', k=8, ic=0.6)
    ust_bitis(dikdortgen(-W / 2, W / 2, 0, D2), Z0 + H, kapali=True)
    return L_


CK = dikdortgen(-IX, IX, IYF, IYB)
DI = {0: 0.18, 1: 0.17, 2: 0.12, 3: 0.17}       # iwan depths (the back one opens into the domed hall)
for i, aci in enumerate((math.pi, -math.pi / 2, 0.0, math.pi / 2)):
    # court side i (CCW corners), walked CW so it faces the court; the iwan in the middle
    a, b = CK[(i + 1) % 4], CK[i]
    e = (b - a).normalized()
    L = (b - a).length
    m = (a + b) / 2
    for (p0, p1) in ((a, m - e * (IW / 2)), (m + e * (IW / 2), b)):
        n = 2
        for k in range(n):
            p, q = p0.lerp(p1, k / n), p0.lerp(p1, (k + 1) / n)
            kitap_bay(p, q, Z0, H1)
            ust_pencere(p, q, Z0 + H1, H2)
    with parca(y, (m.x, m.y, 0), aci):
        iwan(DI[i], H=HI + (0.06 if i == 2 else 0.0) - (0.04 if i in (1, 3) else 0.0))
# a string course between the storeys, the roof terraces and the court's cornice / parapet
CKW = [CK[3], CK[2], CK[1], CK[0]]


def kenar(k):
    """the court's sides as L-shaped runs from one iwan round the corner CK[k] to the next (walked CW)"""
    a1, b1 = CK[(k + 1) % 4], CK[k]                  # the side ending at the corner
    a2, b2 = CK[k], CK[(k - 1) % 4]                  # the side starting there
    e1, e2 = (b1 - a1).normalized(), (b2 - a2).normalized()
    return [(a1 + b1) / 2 + e1 * (IW / 2 + 0.004), b1, (a2 + b2) / 2 - e2 * (IW / 2 + 0.004)]


for k in range(4):
    silme(y, kenar(k), Z0 + H1 - 0.004, 0.01, 0.008, TA, 'duz', kapali=False)
for i in range(4):
    a, b, ai, bi = BK[i], BK[(i + 1) % 4], CK[i], CK[(i + 1) % 4]
    y.yuz_yon([a + Z * (Z0 + HW), b + Z * (Z0 + HW), bi + Z * (Z0 + HW), ai + Z * (Z0 + HW)], 'siva_krem', Z)
for k in range(4):
    silme(y, kenar(k), Z0 + HW - 0.014, 0.016, 0.01, TA, 'tac', kapali=False)
    parapet(y, kenar(k), Z0 + HW, 0.022, 0, 0.012, T, kapali=False, ust_key=TA)
# the roofs: little turquoise domes over the corner reading rooms, Baghdadi wind catchers (badgir) over the side ranges
ZR = Z0 + HW
for (cx, cy) in ((-0.33, (YF + IYF) / 2), (0.33, (YF + IYF) / 2), (-0.43, (IYB + YB) / 2 + 0.01), (0.43, (IYB + YB) / 2 + 0.01)):
    y.prizma((cx, cy), 0.07, ZR, ZR + 0.012, TA, n=8, kat=math.pi / 8)
    kucuk_kubbe(y, cx, cy, ZR + 0.012, 0.055, kasnak=0.028, n=16, son=False, key='turkuaz', kasnak_key=T)
    kure(y, (cx, cy, ZR + 0.012 + 0.028 + 0.055 * 0.9 + 0.006), 0.007, 'altin', n=6, kat=3)


def badgir(cx, cy, yon):
    """a wind catcher: a brick shaft standing on the roof, its open slatted mouth turned to the wind (yon), a cap"""
    w, h = 0.06, 0.15
    kutu_merkez(y, (cx, cy), w, w, h, T, z0=ZR, yuzler='onarkasagsol')
    kornis(y, cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2, ZR + h - 0.004, 0.01, 0.007, TA, 'tac')
    y.yuz_yon([V(p.x, p.y, ZR + h + 0.006) for p in dikdortgen(cx - w / 2 - 0.007, cx + w / 2 + 0.007, cy - w / 2 - 0.007, cy + w / 2 + 0.007)], TA, Z)
    d = V(math.cos(yon), math.sin(yon), 0); e = V(-d.y, d.x, 0)
    o = V(cx, cy, 0) + d * (w / 2)
    # the slatted mouth: dark openings between brick fins, a glazed band under it
    for i in range(3):
        u = -w / 2 + w * (i + 0.5) / 3
        kutu(y, o + e * (u - 0.007) + d * 0.0015 + Z * (ZR + 0.07), e, 0.014, 0.0075, 0.055, 'koyu', 'onsagsolust')
    kutu(y, o - e * (w / 2) + d * 0.002 + Z * (ZR + 0.05), e, w, 0.004, 0.012, 'turkuaz', 'onsagsolust')


for (cx, cy, yon) in ((-0.6, -0.2, math.pi), (0.6, -0.2, 0.0), (-0.6, 0.3, math.pi), (0.6, 0.3, 0.0)):
    badgir(cx, cy, yon)
# the court: paving, the fountain pool and four garden beds
y.yuz_yon([V(p.x, p.y, Z0 + 0.001) for p in CK], 'tas_koyu', Z)
FC = (0.0, (IYF + IYB) / 2)
havuz2(cokgen(FC, 0.1, 8, math.pi / 8), 0.014, Z0 + 0.001, 'mermer', h=0.025)
y.prizma(FC, 0.012, Z0 + 0.012, Z0 + 0.06, 'mermer', n=8)
donel(y, FC, [(0.0, Z0 + 0.06), (0.035, Z0 + 0.062), (0.038, Z0 + 0.07), (0.0, Z0 + 0.068)], 'mermer', n=12)
kure(y, (FC[0], FC[1], Z0 + 0.078), 0.01, 'turkuaz', n=8, kat=4)
for sx in (-1, 1):
    for sy in (-1, 1):
        cx, cy = FC[0] + sx * 0.27, FC[1] + sy * 0.22
        kutu_merkez(y, (cx, cy), 0.2, 0.15, 0.018, 'tugla_sari_koyu', z0=Z0 + 0.001, yuzler='onarkasagsol')
        y.yuz_yon([V(cx - 0.1, cy - 0.075, Z0 + 0.019), V(cx + 0.1, cy - 0.075, Z0 + 0.019), V(cx + 0.1, cy + 0.075, Z0 + 0.019), V(cx - 0.1, cy + 0.075, Z0 + 0.019)], 'cimen', Z)
        agac(y, cx, cy, Z0 + 0.019, boy=0.15, tur='yaprakli', key='boya_yesil')
        for dx in (-0.065, 0.065):
            kure(y, (cx + dx, cy + 0.04 * sy, Z0 + 0.03), 0.014, 'zeytin' if dx > 0 else 'boya_yesil', n=8, kat=4)

# ---------------- the domed hall ----------------
y.bolum('Kubbeli salon (kıble eyvanının ardında)')
DC = (0.0, 0.77)
DR = 0.18
HD = 0.48
DK = dikdortgen(-DR, DR, DC[1] - DR, DC[1] + DR)
for i in range(4):
    a, b = DK[i], DK[(i + 1) % 4]
    if i == 0:
        continue          # the front face: against the iwan / above the range it is drawn below
    z_alt = Z0 if i == 2 else Z0
    n = 2
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if i in (1, 3):
            # the side faces: the part inside the block is hidden under the range roof
            pass
        L_, x0, x1, hs, apex = kemer_nis(y, p, q, Z0, HD - 0.02, en=0.7, ust=0.03, sivri=0.55, derin=0.016, key=T, yan_key=TK,
                                         alt_key=TA, v0=0.03, k_say=10, cerceve=(0.007, ['turkuaz', TA]))
        a2, b2 = L_(x0, -Z0, 0.016), L_(x1, -Z0, 0.016)
        dikdortgen_acik(y, a2, b2, Z0 + 0.03, 0.2, 0.3, 0.7, 0.04, 0.15, (T, TK, TA, 'koyu'), derin=0.012, cerceve=(0.005, TA))
        y.kemerli(a2, b2, Z0 + 0.23, apex - 0.23, (T, TK, TA, 'koyu'), v0=0.02, en=0.36, ust=0.02, derin=0.012, k_say=6, sivri=0.55,
                  cerceve=(0.005, 'turkuaz'))
    duz_duvar(y, a, b, Z0 + HD - 0.02, Z0 + HD, T)
# the front face beside the iwan, above the back range
duz_duvar(y, DK[0], V(-IW / 2, DK[0].y), Z0 + HW, Z0 + HD, T)
duz_duvar(y, V(IW / 2, DK[0].y), DK[1], Z0 + HW, Z0 + HD, T)
y.yuz_yon([V(p.x, p.y, Z0 + HD) for p in DK], 'siva_krem', Z)
for i in range(1, 4):
    a, b = DK[i], DK[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    bant(a + Z * (Z0 + HD - 0.06) + e * 0.02, e, nn, (b - a).length - 0.04, 0.026, 'kobalt')
ust_bitis(DK, Z0 + HD, kapali=True)
# the zone of transition: an octagon with small windows, then the pointed dome
ZO = Z0 + HD
ok = cokgen(DC, 0.17, 8, math.pi / 8)
for i in range(8):
    y.kemerli(ok[i], ok[(i + 1) % 8], ZO, 0.07, (T, TK, TA, 'koyu'), v0=0.015, en=0.4, ust=0.012, derin=0.012, k_say=6, sivri=0.5)
halka_kornis(y, DC, 0.17, ZO + 0.07, 0.014, 0.012, 8, TA, kat=math.pi / 8)
ZK = ZO + 0.084
y.yuz_yon([V(p.x, p.y, ZK) for p in cokgen(DC, 0.17, 8, math.pi / 8)], TA, Z)
r = 0.155
pr = [(r, ZK), (r * 0.985, ZK + 0.2 * r), (r * 0.93, ZK + 0.45 * r), (r * 0.8, ZK + 0.72 * r), (r * 0.58, ZK + 0.98 * r),
      (r * 0.3, ZK + 1.2 * r), (r * 0.08, ZK + 1.33 * r), (0.0, ZK + 1.36 * r)]
donel(y, DC, pr, 'turkuaz', n=36)
# white ribs and a lacivert ring at the foot
for i in range(12):
    a = TAU * i / 12
    d = V(math.cos(a), math.sin(a), 0)
    pts = [V(DC[0], DC[1], zz) + d * (rr + 0.002) for rr, zz in pr[:-2]]
    boru(y, pts, 0.003, 'beyaz', n=4)
donel(y, DC, [(r, ZK), (r + 0.002, ZK), (r * 0.985 + 0.002, ZK + 0.2 * r), (r * 0.985, ZK + 0.2 * r)], 'kobalt', n=36)
alem(y, DC[0], DC[1], ZK + 1.36 * r - 0.004, 0.9, hilal=False)
top_k = ZK + 1.36 * r

# ---------------- the observatory ----------------
y.bolum('Rasathane kulesi ve armiller küre')
OC = (-0.9, 0.84)
OB = 0.13
OKB = dikdortgen(OC[0] - OB, OC[0] + OB, OC[1] - OB, OC[1] + OB)
y.yuz_yon([V(p.x, p.y, Z0 + 0.14) for p in OKB], T, Z)
for i in range(4):
    a, b = OKB[i], OKB[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    if i == 1:
        kapi(y, a, b, Z0, 0.4, 0.14, (T, TK, TA, 'ahsap'), sivri=0.5, derin=0.012, cerceve=(0.006, 'turkuaz'))
    else:
        duz_duvar(y, a, b, Z0, Z0 + 0.14, T)
    bant(a + Z * (Z0 + 0.1) + e * 0.01, e, nn, (b - a).length - 0.02, 0.022, 'turkuaz')
kornis(y, OC[0] - OB, OC[0] + OB, OC[1] - OB, OC[1] + OB, Z0 + 0.13, 0.014, 0.01, TA, 'tac')
y.yuz_yon([V(p.x, p.y, Z0 + 0.144) for p in dikdortgen(OC[0] - OB - 0.01, OC[0] + OB + 0.01, OC[1] - OB - 0.01, OC[1] + OB + 0.01)], TA, Z)
z1, z2 = Z0 + 0.144, Z0 + 0.86
r1, r2 = 0.095, 0.078
nb = 6
donel(y, OC, [(r1 + (r2 - r1) * k / nb, z1 + (z2 - z1) * k / nb) for k in range(nb + 1)], T, n=20)
OR = lambda zz: r1 + (r2 - r1) * (zz - z1) / (z2 - z1)
for f in (0.25, 0.5, 0.75):
    zz = z1 + (z2 - z1) * f
    donel(y, OC, [(OR(zz), zz), (OR(zz) + 0.004, zz + 0.003), (OR(zz) + 0.004, zz + 0.011), (OR(zz + 0.014), zz + 0.014)], TA, n=20)
    zt_ = zz + 0.03
    donel(y, OC, [(OR(zt_), zt_), (OR(zt_) + 0.0015, zt_), (OR(zt_ + 0.03) + 0.0015, zt_ + 0.03), (OR(zt_ + 0.03), zt_ + 0.03)], 'turkuaz', n=20)
    for i in range(10):
        a = TAU * i / 10
        nrm = V(math.cos(a), math.sin(a), 0)
        yildiz(V(OC[0], OC[1], zt_ + 0.015) + nrm * (OR(zt_ + 0.015) + 0.0005), V(-nrm.y, nrm.x, 0), nrm, 0.01, 'beyaz', k=2, ic=0.45, d=0.0025)
for f, nw in ((0.38, 4), (0.62, 4), (0.87, 6)):
    zz = z1 + (z2 - z1) * f
    for i in range(nw):
        a = TAU * (i + 0.5 * (nw == 4 and f > 0.5)) / nw + 0.4
        kutu_merkez(y, (OC[0] + math.cos(a) * (OR(zz) - 0.004), OC[1] + math.sin(a) * (OR(zz) - 0.004)), 0.012, 0.016, 0.05, 'koyu', z0=zz, aci=a)
# the loggia on top: corbelled balcony, a ring of open arches, the observing platform with a parapet
ring = cokgen(OC, r2, 20)
konsol_halka(y, ring, z2 - 0.04, 0.04, 0.035, TA, 4)
RB = r2 + 0.035
y.yuz_yon([V(p.x, p.y, z2 + 0.001) for p in cokgen(OC, RB, 20)], TA, Z)
ol = cokgen(OC, r2 * 0.92, 10)
for i in range(10):
    y.kemerli(ol[i], ol[(i + 1) % 10], z2, 0.11, (T, TK, TA, 'koyu'), v0=0.0, en=0.62, ust=0.012, derin=0.012, k_say=6, sivri=0.5,
              cerceve=(0.004, 'turkuaz'))
parapet(y, cokgen(OC, RB, 20), z2, 0.025, 0, 0.008, T, ust_key=TA)
zl = z2 + 0.11
halka_kornis(y, OC, r2 * 0.92, zl, 0.014, 0.022, 10, TA)
y.yuz_yon([V(p.x, p.y, zl + 0.014) for p in disa(cokgen(OC, r2 * 0.92, 10), 0.022)], 'siva_krem', Z)
parapet(y, disa(cokgen(OC, r2 * 0.92, 10), 0.022), zl + 0.014, 0.022, 0, 0.008, T, ust_key=TA)
# the armillary sphere: a pedestal, a meridian ring, an equator, the ecliptic tilted, a globe in the middle
zp = zl + 0.014
y.prizma(OC, 0.02, zp, zp + 0.035, 'mermer', n=8)
y.prizma(OC, 0.008, zp + 0.035, zp + 0.06, 'bronz', n=6)
AC = V(OC[0], OC[1], zp + 0.13)
RA = 0.07


def halka(eks1, eks2, r, key='altin', n=24, kal=0.004):
    pts = [AC + (eks1 * math.cos(TAU * i / n) + eks2 * math.sin(TAU * i / n)) * r for i in range(n + 1)]
    boru(y, pts, kal, key, n=4, kapat=False)


halka(X, Z, RA)                                         # meridian
halka(V(0.7071, 0.7071, 0), Z, RA * 0.96)
eg = math.radians(23.5)
halka(X, V(0, math.cos(eg), math.sin(eg)), RA * 0.92)  # ecliptic
halka(X, Y, RA * 0.92, 'bronz')                         # equator
cubuk(y, AC - V(0, 0.0, RA * 1.15), AC + V(0, 0.0, RA * 1.15), 0.004, 'bronz')
kure(y, AC, 0.022, 'kobalt', n=10, kat=6)
cubuk(y, V(OC[0], OC[1], zp + 0.06), AC - V(0, 0, RA), 0.006, 'bronz')
top_o = AC.z + RA * 1.15
# a sundial gnomon and a bench of instruments at the foot (a quadrant arc on the platform)
qpts = [V(OC[0] + 0.21 + 0.09 * math.cos(math.pi / 2 * i / 8), OC[1] - 0.12, Z0 + 0.012 + 0.09 * math.sin(math.pi / 2 * i / 8)) for i in range(9)]
boru(y, qpts, 0.005, 'bronz', n=4)
cubuk(y, qpts[0], V(qpts[0].x - 0.09, qpts[0].y, qpts[0].z), 0.006, 'bronz')
cubuk(y, V(qpts[0].x - 0.09, qpts[0].y, Z0), V(qpts[0].x - 0.09, qpts[0].y, qpts[-1].z), 0.008, 'mermer')
sancak(y, OC[0] + RB - 0.012, OC[1], zl + 0.036, boy=0.2, en=0.11, yuk=0.07, aci=0.4)

# ---------------- the front garden ----------------
y.bolum('Ön bahçe: havuzlar, serviler, hurmalar')
y.yuz_yon([V(-0.11, -1.12, Z0 + 0.0015), V(0.11, -1.12, Z0 + 0.0015), V(0.11, YF - PD, Z0 + 0.0015), V(-0.11, YF - PD, Z0 + 0.0015)], 'tas_koyu', Z)
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.2, sx * 0.72))
    havuz2(dikdortgen(x0, x1, -0.98, -0.86), 0.016, Z0, 'mermer', h=0.022)
    for k in range(5):
        xx = x0 + (x1 - x0) * (k + 0.5) / 5
        for yy in (-1.04, -0.8):
            agac(y, xx, yy, Z0, boy=0.2 if k % 2 == 0 else 0.16, tur='servi', key='yesil_koyu' if k % 2 else 'boya_yesil')
# the side garden: a water rill with basins and a domed reading kiosk on slender columns
y.bolum('Yan bahçe: su kanalı ve okuma köşkü')
KX, KY = 0.93, 0.42
y.yuz_yon([V(KX - 0.012, -0.5, Z0 + 0.0015), V(KX + 0.012, -0.5, Z0 + 0.0015), V(KX + 0.012, KY - 0.09, Z0 + 0.0015), V(KX - 0.012, KY - 0.09, Z0 + 0.0015)], 'su', Z)
for yy in (-0.5, KY - 0.09):
    kutu_merkez(y, (KX, yy), 0.04, 0.008, 0.008, 'mermer', z0=Z0)
for xx in (KX - 0.02, KX + 0.02):
    kutu_merkez(y, (xx, (-0.5 + KY - 0.09) / 2), 0.008, KY - 0.09 + 0.5, 0.006, 'mermer', z0=Z0)
havuz2(cokgen((KX, -0.1), 0.04, 8, math.pi / 8), 0.01, Z0, 'mermer', h=0.018)
kutu_merkez(y, (KX, KY), 0.17, 0.17, 0.02, 'mermer', z0=Z0)
for i in range(8):
    a = TAU * i / 8 + math.pi / 8
    y.prizma((KX + 0.068 * math.cos(a), KY + 0.068 * math.sin(a)), 0.006, Z0 + 0.02, Z0 + 0.14, 'mermer', n=6, ust=False)
ko = cokgen((KX, KY), 0.078, 8, math.pi / 8)
y.prizma((KX, KY), 0.082, Z0 + 0.14, Z0 + 0.16, T, n=8, kat=math.pi / 8)
for i in range(8):
    p, q = cokgen((KX, KY), 0.082, 8, math.pi / 8)[i], cokgen((KX, KY), 0.082, 8, math.pi / 8)[(i + 1) % 8]
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    yildiz((p + q) / 2 + Z * (Z0 + 0.15) + nn * 0.0005, e, nn, 0.006, 'turkuaz', k=4, ic=0.5)
halka_kornis(y, (KX, KY), 0.082, Z0 + 0.16, 0.008, 0.01, 8, TA, kat=math.pi / 8)
tk = y.kubbe((KX, KY), 0.078, Z0 + 0.168, 0.075, 'turkuaz', n=16, kat=6)
alem(y, KX, KY, tk.z, 0.5, hilal=False)
for (bx, by) in ((KX - 0.03, KY - 0.02), (KX + 0.03, KY + 0.02)):
    kutu_merkez(y, (bx, by), 0.05, 0.03, 0.004, 'boya_kirmizi', z0=Z0 + 0.02)
for yy in (-0.38, -0.22, 0.02, 0.16):
    for sx in (-1, 1):
        kure(y, (KX + sx * 0.06, yy, Z0 + 0.016), 0.02, 'boya_yesil' if sx > 0 else 'zeytin', n=8, kat=4)
for (tx, ty) in ((-0.95, -0.95), (0.95, -0.95), (0.85, -0.3), (0.85, 0.25), (0.95, 0.8), (-0.96, -0.3), (-0.96, 0.25), (0.4, 0.95)):
    palmiye(tx, ty, Z0, boy=0.3)
# a reading bench under the palms by the observatory and scrolls on it
kutu_merkez(y, (-0.6, 0.92), 0.2, 0.05, 0.03, 'mermer', z0=Z0)
for i, key in enumerate(('kumas', 'kece', 'siva_oker')):
    boru(y, [V(-0.66 + i * 0.05, 0.91, Z0 + 0.038), V(-0.66 + i * 0.05, 0.94, Z0 + 0.038)], 0.007, key, n=6)

sancak(y, PW * 0.3, YF - PD * 0.5, top_p, boy=0.2, en=0.11, yuk=0.07, aci=0.0)

calistir(y, 'lm_beytulhikme')
