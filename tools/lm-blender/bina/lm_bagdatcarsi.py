# Bağdat Çarşısı (lm_bagdatcarsi): an Abbasid covered bazaar of yellow baked brick on a cross plan: four vaulted arms
# of shops (pointed shop arches with counters, shelves, striped awnings) roofed by a row of brick domes with light
# lanterns, the tall chahar-su crossing under a turquoise glazed dome on a windowed drum; a towered main gate with a
# muqarnas pishtaq, smaller portals at the other arm ends; a two-storey han round an arcaded court, a brick minaret
# after the Suq al-Ghazl one with its small mosque, and open markets of spice stalls, carpet racks and laden camels.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.04
T, TK, TA = 'tugla_sari', 'tugla_sari_koyu', 'kum_acik'
AW = 0.17            # arm half width
C = 0.25             # crossing half size
YF = -0.91           # an arm's outer end (local, the front arm)
HW = 0.3             # arm wall height
HS = 0.2             # the shop arches' height
HC = 0.5             # crossing wall height
BAY = (-YF - C) / 2  # the arms' bays (one dome each)

y.bolum('Zemin')
zemin(y, -1.12, 1.12, -1.13, 1.08, Z0, 'kum_koyu', 'zemin', basamak=(('on', 0.6),), n_basamak=2)


# ---------------- ornament helpers ----------------
def yildiz(o, ex, nrm, r, key, k=8, ic=0.5, d=0.0015, kat=0.0, yan_key=None):
    """a raised k-pointed star / lozenge / rosette: o on the surface, ex along it, nrm out (a thin one, d < 0.002,
    is a flat inlay without edges: glazed tile, painted)"""
    o, ex, nrm = V(*o), V(*ex), V(*nrm)
    up = nrm.cross(ex).normalized()
    pts = [o + ex * ((r if i % 2 == 0 else r * ic) * math.cos(kat + math.pi * i / k)) + up * ((r if i % 2 == 0 else r * ic) * math.sin(kat + math.pi * i / k)) for i in range(2 * k)]
    y.yuz_yon([p + nrm * d for p in pts], key, nrm)
    if d < 0.002: return
    for i in range(2 * k):
        p, q = pts[i], pts[(i + 1) % (2 * k)]
        y.yuz_yon([p, q, q + nrm * d, p + nrm * d], yan_key or key, (p + q) / 2 - o)


def kademeli_mazgal(a, b, z, t=0.018, key=T, w=0.058, g=0.026):
    """Mesopotamian stepped merlons along a->b (outer face on the line, facing right): a wide block, a narrow one on it"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g
    for i in range(k):
        o = a + e * (i * (w + g))
        kutu(y, o + Z * z, e, w, t, 0.016, key)
        kutu(y, o + e * (w * 0.22) + Z * (z + 0.016), e, w * 0.56, t, 0.012, key)


def ust_bitis(kose, z, kapali=False, key=T):
    """a crowning cornice under z, a solid parapet band and stepped merlons along a polyline (or polygon)"""
    silme(y, kose, z - 0.018, 0.02, 0.012, TA, 'tac', kapali=kapali)
    dk = disa(kose, 0.0, kapali)
    parapet(y, dk, z, 0.014, 0, 0.018, key, kapali=kapali, ust_key=TA)
    n = len(dk)
    for i in range(n if kapali else n - 1):
        kademeli_mazgal(dk[i], dk[(i + 1) % n], z + 0.014)


def levha(pts, key, yon, t=0.003):
    """a thin sheet (cloth, board) of thickness t: the face towards yon, its back, and the rims all round (seen edge-on
    the two faces must not show each other's backs)"""
    pts = [V(*p) for p in pts]; yon = V(*yon).normalized()
    ust = [p + yon * (t / 2) for p in pts]; alt = [p - yon * (t / 2) for p in pts]
    y.yuz_yon(ust, key, yon)
    y.yuz_yon(alt, key, -yon)
    c = sum(pts, V(0, 0, 0)) / len(pts)
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([ust[i], ust[j], alt[j], alt[i]], key, (pts[i] + pts[j]) / 2 - c)


def serit_tente(p0, p1, q0, q1, renkler=('kumas', 'boya_kirmizi'), n=6):
    """a striped cloth awning p0-p1 (the edge at the wall) to q0-q1 (the free edge), seen from both sides"""
    p0, p1, q0, q1 = V(*p0), V(*p1), V(*q0), V(*q1)
    nrm = (p1 - p0).cross(q0 - p0).normalized()
    if nrm.z < 0: nrm = -nrm
    for i in range(n):
        a, b = p0.lerp(p1, i / n), p0.lerp(p1, (i + 1) / n)
        c, d = q0.lerp(q1, (i + 1) / n), q0.lerp(q1, i / n)
        levha([a, b, c, d], renkler[i % len(renkler)], nrm)
    # a scalloped valance hanging from the free edge
    out = (q0 - p0); out.z = 0; out.normalize()
    for i in range(n):
        a, b = q0.lerp(q1, i / n), q0.lerp(q1, (i + 1) / n)
        m = (a + b) / 2 - Z * 0.014
        levha([a - Z * 0.0015, b - Z * 0.0015, m], renkler[(i + 1) % len(renkler)], out)


def cuval(cx, cy, z, r=0.016, h=0.026, ic='boya_kirmizi', key='kumas'):
    """an open spice sack: a bulging canvas sack with a rolled rim, heaped with coloured spice"""
    donel(y, (cx, cy), [(r * 0.9, z), (r * 1.1, z + h * 0.45), (r * 1.06, z + h), (r * 0.92, z + h)], key, n=5)
    donel(y, (cx, cy), [(r * 0.92, z + h), (0.0, z + h + r * 0.7)], ic, n=5)


def kup(cx, cy, z, r=0.016, h=0.045, key='kiremit'):
    """a clay jar"""
    donel(y, (cx, cy), [(r * 0.6, z), (r, z + h * 0.4), (r * 0.45, z + h * 0.88), (r * 0.5, z + h), (0.0, z + h)], key, n=5)


def hali(o, ex, w, h, zemin_k='boya_kirmizi', kenar='lacivert', orta='boya_sari', t=0.004):
    """a hanging carpet: a thin slab (o = top-left on its front face line, ex along, hanging down h) with a border and a
    medallion on both faces"""
    o, ex = V(*o), V(*ex).normalized()
    nn = V(ex.y, -ex.x)
    kutu(y, o - Z * h + nn * (t / 2), ex, w, t, h, zemin_k)   # (d is to the left of ex: the slab sits on the line)
    for s in (1, -1):
        f = nn * (s * (t / 2 + 0.0012))
        c = o + ex * (w / 2) - Z * (h / 2) + f
        P = lambda u, v: o + ex * u - Z * v + f
        b = min(w, h) * 0.12
        for (u0, u1, v0, v1) in ((0, w, 0, b), (0, w, h - b, h), (0, b, b, h - b), (w - b, w, b, h - b)):
            y.yuz_yon([P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)], kenar, nn * s)
        yildiz(c, ex if s > 0 else -ex, nn * s, min(w, h) * 0.26, orta, k=4, ic=0.45, d=0.0008)
    # fringes at the bottom
    for i in range(4):
        u = w * (i + 0.5) / 4
        cubuk(y, o + ex * u - Z * h, o + ex * u - Z * (h + 0.01), 0.002, 'kumas')


def palmiye(x, yy, z, boy=0.3):
    """a date palm: a ringed, slightly curved trunk, a crown of arching fronds and date clusters"""
    tepe = V(x + 0.012, yy + 0.006, z + boy)
    boru(y, [V(x, yy, z), V(x + 0.004, yy + 0.002, z + boy * 0.5), tepe], 0.009, 'ahsap_acik', n=6, r_son=0.007)
    for i in range(6):
        a = TAU * i / 6 + 0.3
        d = V(math.cos(a), math.sin(a))
        L = 0.085 + 0.015 * (i % 2)
        boru(y, [tepe, tepe + d * (L * 0.45) + Z * 0.03, tepe + d * L - Z * 0.02, tepe + d * (L * 1.12) - Z * 0.05], 0.009, 'boya_yesil', n=3, r_son=0.002)
    for i in range(3):
        a = TAU * i / 3
        kure(y, (tepe.x + 0.014 * math.cos(a), tepe.y + 0.014 * math.sin(a), tepe.z - 0.014), 0.009, 'siva_oker', n=6, kat=3)
    kure(y, (tepe.x, tepe.y, tepe.z + 0.004), 0.012, 'boya_yesil', n=8, kat=4)


def denk(cx, cy, z, key='kumas', aci=0.0, w=0.06, d=0.045, h=0.035):
    """a corded bale of goods"""
    kutu_merkez(y, (cx, cy), w, d, h, key, z0=z, aci=aci)
    ca, sa = math.cos(aci), math.sin(aci)
    for t in (-0.25, 0.25):
        o = V(cx + ca * w * t, cy + sa * w * t)
        e = V(-sa, ca)
        cubuk(y, o - e * (d / 2 + 0.002) + Z * (z + h + 0.002), o + e * (d / 2 + 0.002) + Z * (z + h + 0.002), 0.004, 'ahsap_koyu', 0.002)


def deve(x, yy, aci, renk='ahsap_acik', yuk=True, cul='boya_kirmizi'):
    """a stylised dromedary (head towards +x before turning), laden with bales over a saddle cloth"""
    with parca(y, (x, yy, Z0), aci, 1.35):
        h = 0.075
        boru(y, [V(-0.045, 0, h + 0.012), V(-0.01, 0, h + 0.02), V(0.03, 0, h + 0.018), V(0.048, 0, h + 0.012)], 0.02, renk, n=8)
        kure(y, (-0.045, 0, h + 0.012), 0.019, renk, n=8, kat=4)
        kure(y, (0.046, 0, h + 0.013), 0.018, renk, n=8, kat=4)
        donel(y, (-0.004, 0), [(0.026, h + 0.02), (0.022, h + 0.04), (0.012, h + 0.054), (0.0, h + 0.058)], renk, n=10)
        boru(y, [V(0.05, 0, h + 0.016), V(0.082, 0, h + 0.004), V(0.102, 0, h + 0.026), V(0.106, 0, h + 0.05)], 0.009, renk, n=6, r_son=0.007)
        boru(y, [V(0.102, 0, h + 0.054), V(0.13, 0, h + 0.047)], 0.009, renk, n=6, r_son=0.006)
        for s in (-1, 1):
            cubuk(y, V(0.104, s * 0.006, h + 0.06), V(0.101, s * 0.007, h + 0.069), 0.003, renk)
        boru(y, [V(-0.062, 0, h + 0.02), V(-0.07, 0, h - 0.005), V(-0.068, 0, h - 0.02)], 0.0025, 'ahsap_koyu', n=4, r_son=0.0015)
        for lx in (-0.04, 0.038):
            for s in (-1, 1):
                boru(y, [V(lx, s * 0.01, h + 0.004), V(lx + 0.004, s * 0.01, h * 0.5), V(lx, s * 0.01, 0.006)], 0.0055, renk, n=5, r_son=0.004)
                kutu_merkez(y, (lx + 0.003, s * 0.01), 0.012, 0.01, 0.006, 'ahsap_koyu')
        if yuk:
            kutu_merkez(y, (-0.004, 0), 0.05, 0.05, 0.004, cul, z0=h + 0.03)
            for s in (-1, 1):
                kutu_merkez(y, (-0.004, s * 0.034), 0.05, 0.026, 0.04, 'kumas' if s > 0 else 'kece', z0=h - 0.005)
                cubuk(y, V(-0.03, s * 0.048, h + 0.03), V(0.022, s * 0.048, h + 0.03), 0.003, 'ahsap_koyu', 0.003)
            denk(-0.004, 0, h + 0.056, 'boya_sari', w=0.04, d=0.03, h=0.02)


def havuz2(ic, kenar, z0, key, h=0.02):
    """a pool: a kerb round the CCW polygon ic (kenar wide, h high), its inner faces down to the water a little below the top"""
    dis = disa(ic, kenar)
    zt, zs = z0 + h, z0 + h * 0.45
    duvarlar(y, dis, z0, zt, key)
    n = len(ic)
    for i in range(n):
        j = (i + 1) % n
        duz_duvar(y, ic[j], ic[i], zs, zt, key)
        y.yuz_yon([dis[i] + Z * zt, dis[j] + Z * zt, ic[j] + Z * zt, ic[i] + Z * zt], key, Z)
    y.yuz_yon([V(p.x, p.y, zs) for p in ic], 'su', Z)


# ---------------- shops ----------------
MAL = [('boya_kirmizi', 'boya_sari', 'siva_oker'), ('bakir', 'kiremit', 'altin'), ('lacivert', 'boya_kirmizi', 'kumas'),
       ('boya_yesil', 'siva_oker', 'boya_kirmizi'), ('kumas', 'boya_sari', 'kece')]
TENTE = [('kumas', 'boya_kirmizi'), ('kumas', 'boya_yesil'), ('kece', 'kobalt'), ('kumas', 'siva_oker')]


def dukkan(p, q, k, tente=True):
    """one shop bay p->q (facing right): a pointed brick arch on the street, the wooden back with two shelves of goods,
    a counter in front heaped with wares, a turquoise roundel above and (tente) a striped awning on poles"""
    L_, x0, x1, hs, apex = kemer_nis(y, p, q, Z0, HS, en=0.74, ust=0.016, sivri=0.45, derin=0.045, key=T, yan_key=TK, alt_key=TA,
                                     arka_key='ahsap_koyu', k_say=6, cerceve=(0.007, [TA, TK]))
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    mal = MAL[k % len(MAL)]
    w = x1 - x0
    # shelves on the back wall, goods on them
    for j, zz in enumerate((0.105,) if k % 2 == 0 else ()):
        kutu(y, L_(x0, zz, 0.031), e, w, 0.014, 0.004, 'ahsap', 'onsagsolust')
        for i in range(3):
            u = x0 + w * (i + 0.5) / 3
            o = L_(u, zz + 0.004, 0.036)
            kutu_merkez(y, (o.x, o.y), 0.011, 0.009, 0.012 + 0.004 * ((i + j) % 2), mal[(i + j) % 3], z0=o.z,
                        aci=math.atan2(e.y, e.x))
    # the counter (half in the niche, half on the street) and its wares
    cu0, cu1 = x0 + 0.006, x1 - 0.006
    o = L_(cu0, 0, 0.022)
    kutu(y, o - nn * 0.0, e, cu1 - cu0, -0.05, 0.05, 'ahsap', 'onarkasagsolust')
    kutu(y, L_(cu0 - 0.002, 0.05, 0.024), e, cu1 - cu0 + 0.004, -0.054, 0.005, 'ahsap_acik', 'onarkasagsolust')
    for i in range(2):
        u = cu0 + (cu1 - cu0) * (i + 0.5) / 2
        c = L_(u, 0.055, -0.004)
        if k % 2 == 0:
            cuval(c.x, c.y, c.z, r=0.011, h=0.016, ic=mal[i], key='kumas')
        else:
            kup(c.x, c.y, c.z, r=0.009, h=0.026, key=mal[i] if mal[i] in ('bakir', 'kiremit', 'altin') else 'kiremit')
    # sacks on the ground before the counter
    if k % 4 == 0:
        for i, u in enumerate((cu0 + 0.012,)):
            c = L_(u, 0, -0.045)
            cuval(c.x, c.y, Z0, r=0.013, h=0.022, ic=mal[(i + k) % 3])
    # the band above: two string courses, a glazed roundel over the arch, brick lozenges between
    kutu(y, L_(0, HS + 0.004, -0.004), e, (q - p).length, 0.004, 0.006, TA, 'onust')
    m = L_((x0 + x1) / 2, HS + 0.048, -0.0005)
    yildiz(m, e, nn, 0.013, 'turkuaz', k=6, ic=0.62)
    for u in (0.04, (q - p).length - 0.04):
        yildiz(L_(u, HS + 0.048, -0.0005), e, nn, 0.01, TK, k=2, ic=0.55, d=0.0015)
    if tente:
        tk = TENTE[k % len(TENTE)]
        zt, zd, out = Z0 + HS + 0.002, Z0 + HS - 0.05, 0.085
        a0, a1 = L_(x0 - 0.008, HS + 0.002 - 0.0, -0.006), L_(x1 + 0.008, HS + 0.002, -0.006)
        b0, b1 = a0 + nn * out - Z * 0.05, a1 + nn * out - Z * 0.05
        serit_tente(a0, a1, b0, b1, tk, n=5)
        for b in (b0, b1):
            cubuk(y, V(b.x, b.y, Z0), V(b.x, b.y, b.z + 0.004), 0.0045, 'ahsap_koyu')


def dukkan_cephe(a, b, n, bas=0.0, son=0.0, tente=True, k0=0):
    """a shop front a->b: plain wall for bas / son at the ends, n shops between, the plain band up to the cornice"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L
    if bas: duz_duvar(y, a, a + e * bas, Z0, Z0 + HW, T)
    if son: duz_duvar(y, b - e * son, b, Z0, Z0 + HW, T)
    pa, pb = a + e * bas, b - e * son
    for k in range(n):
        p, q = pa.lerp(pb, k / n), pa.lerp(pb, (k + 1) / n)
        dukkan(p, q, k + k0, tente and (k + k0) % 2 == 0)
        duz_duvar(y, p, q, Z0 + HS, Z0 + HW, T)


# ---------------- domes ----------------
def carsi_kubbe(cx, cy, z, r=0.14):
    """a bay dome of the covered street: a low drum with little lights, a brick dome with a glazed band, the lantern
    (ışıklık) with open arches and a turquoise cap"""
    y.prizma((cx, cy), r * 1.03, z, z + 0.024, T, n=16)
    y.prizma((cx, cy), r * 1.03 + 0.005, z + 0.024, z + 0.03, TA, n=16)
    for i in range(4):
        a = TAU * (4 * i + 0.5) / 16
        nrm = V(math.cos(a), math.sin(a)); e = V(-nrm.y, nrm.x)
        yarik(y, V(cx, cy) + nrm * (r * 1.03 * math.cos(math.pi / 16) + 0.001) + Z * z, e, nrm, -0.006, 0.006, 0.012, 0.016, 'koyu')
    t = y.kubbe((cx, cy), r, z + 0.03, r * 0.6, T, n=16, kat=5)
    # a turquoise band round the dome's foot
    ph = math.pi / 12
    donel(y, (cx, cy), [(r + 0.002, z + 0.03), (r * math.cos(ph) + 0.002 * math.cos(ph), z + 0.03 + r * 0.6 * math.sin(ph) + 0.002 * math.sin(ph)), (r * math.cos(ph), z + 0.03 + r * 0.6 * math.sin(ph))], 'turkuaz', n=16)
    # the lantern
    lr = r * 0.22
    zl = t.z - 0.006
    ok = cokgen((cx, cy), lr, 6)
    y.prizma((cx, cy), lr * 1.25, zl - 0.006, zl + 0.004, TA, n=6)
    y.prizma((cx, cy), lr, zl + 0.004, zl + 0.03, T, n=6, ust=False)
    for i in range(6):
        p, q = ok[i], ok[(i + 1) % 6]
        e = (q - p).normalized(); nn = V(e.y, -e.x)
        y.pencere(p + Z * 0, e, nn, (q - p).length * 0.25, zl + 0.008, (q - p).length * 0.5, 0.018, 'koyu', k_say=3)
    t2 = y.kubbe((cx, cy), lr * 1.12, zl + 0.03, lr * 0.9, 'turkuaz', n=8, kat=4)
    kure(y, (cx, cy, t2.z + 0.004), 0.004, 'altin', n=6, kat=3)


# ---------------- the four arms ----------------
def kol(ana):
    """one arm in local coordinates (the front arm: x +-AW, y from -C out to YF): shop fronts on both long sides, the
    flat roof with its bay domes, cornice and stepped merlons, and the portal at the outer end"""
    s0 = 0.1 if ana else 0.04
    dukkan_cephe((-AW, -C), (-AW, YF), 3, bas=0.02, son=s0, k0=0)
    dukkan_cephe((AW, YF), (AW, -C), 3, bas=s0, son=0.02, k0=1)
    y.yuz_yon([V(-AW, YF, Z0 + HW), V(AW, YF, Z0 + HW), V(AW, -C, Z0 + HW), V(-AW, -C, Z0 + HW)], 'siva_krem', Z)
    pw = 0.0 if ana else 0.15
    ust_bitis([V(-AW, -C), V(-AW, YF + 0.002)] + ([V(-pw, YF + 0.002)] if pw else []), Z0 + HW)
    ust_bitis(([V(pw, YF + 0.002)] if pw else []) + [V(AW, YF + 0.002), V(AW, -C)], Z0 + HW)
    silme(y, [V(-AW, -C), V(-AW, YF), V(AW, YF), V(AW, -C)], Z0, 0.016, 0.008, TK, 'kaide', kapali=False)
    for k in range(2):
        carsi_kubbe(0, -C - BAY * (k + 0.5), Z0 + HW)
    # the end: a muqarnas portal into the street
    if ana:
        PW, PH, PD = 0.36, 0.6, 0.075
        top = tackapi_mukarnas(y, 0, YF - PD, Z0, en=PW, H=PH, derin=PD, nis=0.56, sivri=0.55, mk_kat=4, kapi_key='koyu', key=T,
                               bordur=('turkuaz', TA), tonlar=(TA, TK), cerceve=(0.012, ['turkuaz', TA]))
        portal_sus(0, YF - PD, Z0, PW, PH, 0.56, dis=True)
        duz_duvar(y, V(PW / 2, YF), V(-PW / 2, YF), Z0, Z0 + HW, T)
        portal_arka(-PW / 2, PW / 2, YF, Z0 + HW, Z0 + PH, 0.034)
        # the gate towers: battered round brick towers, brick bands, a glazed frieze and turquoise domes
        for sx in (-1, 1):
            c = (sx * (AW + 0.085), YF - 0.035)
            kule_yuvarlak(y, c, 0.075, Z0, 0.58, key=T, cati='kubbe', cati_key='turkuaz', cati_h=0.075, mazgal_h=0.001, n=16, egim=0.1,
                          yarik_say=3, bolum=5)
            for zz in (0.16, 0.32):
                rr = 0.075 * (1 + 0.1 * (1 - zz / 0.58))
                donel(y, c, [(rr, Z0 + zz), (rr + 0.006, Z0 + zz + 0.004), (rr + 0.006, Z0 + zz + 0.01), (rr, Z0 + zz + 0.014)], TA, n=16)
            rr = 0.075 * (1 + 0.1 * (1 - 0.47 / 0.58))
            ra, rb = 0.075 * (1 + 0.1 * (1 - 0.462 / 0.58)), 0.075 * (1 + 0.1 * (1 - 0.5 / 0.58))
            donel(y, c, [(ra, Z0 + 0.462), (ra + 0.0015, Z0 + 0.462), (rb + 0.0015, Z0 + 0.5), (rb, Z0 + 0.5)], 'turkuaz', n=16)
            for i in range(12):
                a = TAU * i / 12
                nrm = V(math.cos(a), math.sin(a))
                yildiz(V(c[0], c[1], Z0 + 0.481) + nrm * (rr + 0.0005), V(-nrm.y, nrm.x), nrm, 0.009, 'beyaz', k=2, ic=0.5, d=0.0025)
        return top
    PW, PH, PD = 0.3, 0.44, 0.055
    top = tackapi_mukarnas(y, 0, YF - PD, Z0, en=PW, H=PH, derin=PD, nis=0.56, sivri=0.55, mk_kat=3, kapi_key='koyu', key=T,
                           bordur=('turkuaz', TA), tonlar=(TA, TK), cerceve=(0.01, ['turkuaz', TA]))
    portal_sus(0, YF - PD, Z0, PW, PH, 0.56)
    for xa, xb in ((-AW, -PW / 2), (PW / 2, AW)):
        duz_duvar(y, V(xa, YF), V(xb, YF), Z0, Z0 + HW, T)
    portal_arka(-PW / 2, PW / 2, YF, Z0 + HW, Z0 + PH, 0.022)
    return top


def portal_arka(x0, x1, yy, z0, z1, yildiz_r=0.03):
    """the back of a portal block where it rises above the roofs (x1 -> x0 along y = yy, facing +y): a blind pointed
    niche in a glazed frame with a tile star in its head and a glazed band of lozenges at the top (not a bare slab)"""
    H = z1 - z0
    L_, a0, a1, hs, apex = kemer_nis(y, V(x1, yy), V(x0, yy), z0, H, en=0.62, ust=min(0.05, H * 0.2), sivri=0.5, derin=0.006,
                                     key=T, yan_key=TK, alt_key=TA, arka_key=TK, v0=0.02, k_say=10,
                                     cerceve=(0.009, ['turkuaz', TA]))
    m = L_((a0 + a1) / 2, 0, 0.0055)
    yildiz(V(m.x, m.y, z0 + hs * 0.72), -X, Y, yildiz_r, 'turkuaz', k=8, ic=0.55)
    W = abs(x1 - x0)
    o = V(x1, yy + 0.0015, z1 - 0.034)
    y.yuz_yon([o, o - X * W, o - X * W + Z * 0.018, o + Z * 0.018], 'turkuaz', Y)
    n_ = max(3, int(W / 0.05))
    for j in range(n_):
        yildiz(V(x1 - W * (j + 0.5) / n_, yy + 0.0015, z1 - 0.025), -X, Y, 0.0075, 'beyaz', k=2, ic=0.45, d=0.001)


def portal_sus(cx, cy, z0, en, H, nis, dis=False):
    """glazed stars along the portal's outer border, a dentil row under its cornice, rosettes in the spandrels"""
    bw = en * 0.07
    zb = z0 + H - 0.016
    n = max(3, int((zb - bw - z0 - 0.02) / (bw * 1.6)))
    for sx in (-1, 1):
        for i in range(n):
            zz = z0 + 0.03 + (zb - bw - z0 - 0.04) * (i + 0.5) / n
            yildiz((cx + sx * (en / 2 - bw / 2), cy - 0.006, zz), X, -Y, bw * 0.4, 'beyaz', k=6, kat=math.pi / 6)
    m = max(3, int((en - 2 * bw) / (bw * 1.6)))
    for i in range(m):
        xx = cx - en / 2 + bw + (en - 2 * bw) * (i + 0.5) / m
        yildiz((xx, cy - 0.006, zb - bw / 2), X, -Y, bw * 0.4, 'beyaz', k=6, kat=math.pi / 6)
    hw = nis * en / 2 + 0.012 + bw * 0.6
    for sx in (-1, 1):
        yildiz((cx + sx * hw * 0.62, cy - 0.0025, z0 + H * 0.88 - 0.03), X, -Y, 0.014, 'turkuaz', k=12, ic=0.72, yan_key=TA)
    if not dis: return
    nk = int(en / 0.028)
    for i in range(nk):
        kutu_merkez(y, (cx - en / 2 + en * (i + 0.5) / nk, cy - 0.006), 0.011, 0.011, 0.011, TK, z0=zb - 0.028)


y.bolum('Çarşı kolları: dükkânlar, kubbeler, kapılar')
top_ana = None
for i, aci in enumerate((0.0, math.pi / 2, math.pi, -math.pi / 2)):
    with parca(y, (0, 0, 0), aci):
        t = kol(i == 0)
        if i == 0: top_ana = t

# ---------------- the crossing ----------------
y.bolum('Çaharsu: yüksek kare gövde, kasnak, turkuaz kubbe')
K = dikdortgen(-C, C, -C, C)
for i in range(4):
    a, b = K[i], K[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    L = (b - a).length
    # below the arms' roofs only the corners show; above, the full face with two tall windows and a tile frieze
    duz_duvar(y, a, a + e * (C - AW), Z0, Z0 + HW, T)
    duz_duvar(y, b - e * (C - AW), b, Z0, Z0 + HW, T)
    zf = Z0 + HW
    for k in range(2):
        p, q = a.lerp(b, k / 2), a.lerp(b, (k + 1) / 2)
        y.kemerli(p, q, zf, HC - HW - 0.06, (T, TK, TA, 'koyu'), v0=0.03, en=0.42, ust=0.016, derin=0.022, k_say=8, sivri=0.55,
                  cerceve=(0.007, ['turkuaz', TA]))
        m = (p + q) / 2
        # a lattice screen in the window
    duz_duvar(y, a + Z * 0, b, Z0 + HC - 0.06, Z0 + HC, T)
    # the frieze: a turquoise band with white lozenges (an inscription read from afar)
    o = a + nn * 0.0015
    y.yuz_yon([o + Z * (Z0 + HC - 0.05), o + e * L + Z * (Z0 + HC - 0.05), o + e * L + Z * (Z0 + HC - 0.026), o + Z * (Z0 + HC - 0.026)], 'turkuaz', nn)
    for j in range(9):
        yildiz(a + e * (L * (j + 0.5) / 9) + Z * (Z0 + HC - 0.038) + nn * 0.0015, e, nn, 0.01, 'beyaz', k=2, ic=0.45, d=0.001)
silme(y, K, Z0 + HW, 0.012, 0.008, TA, 'duz')
y.yuz_yon([V(p.x, p.y, Z0 + HC) for p in K], 'siva_krem', Z)
ust_bitis(K, Z0 + HC, kapali=True)
# corner turrets
for p in K:
    c = (p.x, p.y)
    y.prizma(c, 0.034, Z0, Z0 + HC + 0.06, T, n=8, kat=math.pi / 8, ust=False)
    halka_kornis(y, c, 0.034, Z0 + HC + 0.04, 0.01, 0.008, 8, TA, kat=math.pi / 8)
    y.prizma(c, 0.036, Z0 + HC + 0.06, Z0 + HC + 0.064, TA, n=8, kat=math.pi / 8)
    t = y.kubbe(c, 0.03, Z0 + HC + 0.064, 0.036, 'turkuaz', n=12, kat=4)
    kure(y, (c[0], c[1], t.z + 0.005), 0.005, 'altin', n=6, kat=3)
# the drum and dome
ZD = Z0 + HC
RD = 0.2
tepe = kubbe_kasnakli(y, (0, 0), RD, ZD, 0.12, n_pencere=12, kubbe_h=0.24, key='turkuaz', duvar=(T, TK, TA, 'koyu'), payanda=True,
                      alem_olcek=1.1, sivri=0.5, n=32, kat=10, en=0.45, cerceve=(0.005, 'turkuaz'))
zk = ZD + 0.12 + 0.016
# lacivert ribs and a white band of script round the dome's foot
rd, hd = RD + 0.005, 0.24
for i in range(12):
    a = TAU * i / 12
    pts = [V(rd * math.cos(ph) * math.cos(a) * 1.0 + 0.003 * math.cos(ph) * math.cos(a), rd * math.cos(ph) * math.sin(a) + 0.003 * math.cos(ph) * math.sin(a),
             zk + hd * math.sin(ph) + 0.003 * math.sin(ph)) for ph in [math.pi / 2 * k / 5 * 0.92 for k in range(6)]]
    boru(y, pts, 0.0034, 'kobalt', n=4)
donel(y, (0, 0), [(rd * math.cos(ph) + 0.002 * math.cos(ph), zk + hd * math.sin(ph) + 0.002 * math.sin(ph)) for ph in (0.0, math.pi / 48, math.pi / 24)] + [(rd * math.cos(math.pi / 24), zk + hd * math.sin(math.pi / 24))], 'kobalt', n=36)
for i in range(24):
    a = TAU * i / 24
    nrm = V(math.cos(a), math.sin(a), 0)
    ph = 0.065
    o = V(rd * math.cos(ph) * nrm.x, rd * math.cos(ph) * nrm.y, zk + hd * math.sin(ph)) + nrm * 0.0028
    yildiz(o - nrm * 0.0013, V(-nrm.y, nrm.x, 0), nrm, 0.011, 'beyaz', k=2, ic=0.4, d=0.0025)

# ---------------- the han (back right) ----------------
y.bolum('Han: iki katlı avlulu kervansaray')
HX0, HX1, HY0, HY1 = 0.32, 1.0, 0.32, 1.0
HH = 0.34
IX0, IX1, IY0, IY1 = 0.5, 0.82, 0.5, 0.82
HK = dikdortgen(HX0, HX1, HY0, HY1)
for i in range(4):
    a, b = HK[i], HK[(i + 1) % 4]
    e = (b - a).normalized()
    n = 4
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if i == 0 and k in (1, 2):
            continue   # the portal
        L_, x0, x1, hs, apex = kemer_nis(y, p, q, Z0, HH - 0.02, en=0.66, ust=0.03, sivri=0.5, derin=0.014, key=T, yan_key=TK,
                                         alt_key=TA, arka_key=None, v0=0.02, k_say=8, cerceve=(0.006, TA))
        # the niche back: two little windows, one above the other
        a2, b2 = L_(x0, -Z0, 0.014), L_(x1, -Z0, 0.014)
        duz_duvar(y, a2, b2, Z0 + 0.02, Z0 + 0.17, T)
        yildiz((a2 + b2) / 2 + Z * (Z0 + 0.1), (b2 - a2).normalized(), V((b2 - a2).y, -(b2 - a2).x).normalized(), 0.022, 'turkuaz', k=8, ic=0.55)
        y.kemerli(a2, b2, Z0 + 0.17, apex - 0.17, (T, TK, TA, 'koyu'), v0=0.02, en=0.3, ust=0.02, derin=0.01, k_say=6, sivri=0.55)
    duz_duvar(y, a, b, Z0 + HH - 0.02, Z0 + HH, T)
PX = (HX0 + HX1) / 2
ptop = tackapi_mukarnas(y, PX, HY0 - 0.05, Z0, en=0.34, H=0.48, derin=0.05, nis=0.55, sivri=0.55, mk_kat=4, kapi_key='ahsap', key=T,
                        bordur=('turkuaz', TA), tonlar=(TA, TK), cerceve=(0.01, ['turkuaz', TA]))
portal_sus(PX, HY0 - 0.05, Z0, 0.34, 0.48, 0.55)
portal_arka(PX - 0.17, PX + 0.17, HY0, Z0 + HH, Z0 + 0.48, 0.022)
silme(y, HK, Z0, 0.02, 0.01, TK, 'kaide')
# half-round corner towers (Ukhaidir)
for p in HK:
    donel(y, (p.x, p.y), [(0.06, Z0), (0.06, Z0 + 0.03), (0.052, Z0 + 0.034), (0.052, Z0 + HH + 0.04)], T, n=12)
    halka_kornis(y, (p.x, p.y), 0.052, Z0 + HH * 0.55, 0.01, 0.006, 12, TA)
    parapet(y, cokgen((p.x, p.y), 0.058, 12), Z0 + HH + 0.04, 0.016, 0, 0.012, T, ust_key=TA)
    silme(y, cokgen((p.x, p.y), 0.052, 12), Z0 + HH + 0.028, 0.012, 0.006, TA, 'tac')
    y.yuz_yon([V(q.x, q.y, Z0 + HH + 0.0405) for q in cokgen((p.x, p.y), 0.052, 12)], 'siva_krem', Z)
# roof terraces round the court, the cornice and stepped merlons
IK = dikdortgen(IX0, IX1, IY0, IY1)
for i in range(4):
    a, b, ai, bi = HK[i], HK[(i + 1) % 4], IK[i], IK[(i + 1) % 4]
    y.yuz_yon([a + Z * (Z0 + HH), b + Z * (Z0 + HH), bi + Z * (Z0 + HH), ai + Z * (Z0 + HH)], 'siva_krem', Z)
ust_bitis(HK, Z0 + HH, kapali=True)
# the court: two storeys of arcades
for i in range(4):
    a, b = IK[(i + 1) % 4], IK[i]          # (walking CW round the court: the faces look into it)
    arkad(y, a, b, 2, Z0, 0.17, en=0.74, ust=0.02, sivri=0.5, derin=0.06, sutunlu=False, renk=(T, TK, TA, 'koyu'),
          cerceve=(0.006, [TA, TK]))
    arkad(y, a, b, 2, Z0 + 0.17, HH - 0.17, en=0.66, ust=0.03, sivri=0.5, derin=0.05, sutunlu=False, renk=(T, TK, TA, 'koyu'),
          korkuluk=0.035, cerceve=(0.006, [TA, 'turkuaz']))
ICW = [IK[3], IK[2], IK[1], IK[0]]
silme(y, ICW, Z0 + 0.17, 0.01, 0.008, TA, 'duz')
parapet(y, ICW, Z0 + HH, 0.016, 0, 0.014, T, ust_key=TA)
# the court: a pool, a well, bales
havuz2(dikdortgen(0.6, 0.72, 0.6, 0.72), 0.014, Z0 + 0.001, TA)
y.yuz_yon([V(IX0, IY0, Z0 + 0.001), V(IX1, IY0, Z0 + 0.001), V(IX1, IY1, Z0 + 0.001), V(IX0, IY1, Z0 + 0.001)], 'tas_koyu', Z)
for (cx, cy, key, a) in ((0.55, 0.77, 'kumas', 0.2), (0.6, 0.78, 'boya_kirmizi', -0.3), (0.77, 0.55, 'kece', 0.1)):
    denk(cx, cy, Z0, key, a, w=0.045, d=0.035, h=0.028)
sancak(y, PX + 0.11, HY0 - 0.025, ptop, boy=0.16, en=0.09, yuk=0.055, aci=0.0)

# ---------------- minaret and mosque (back left) ----------------
y.bolum('Minare (Suk el-Gazl) ve mescit')
MX, MY = -0.42, 0.44
# the small mosque behind it
QX0, QX1, QY0, QY1 = -0.98, -0.5, 0.5, 0.98
QK = dikdortgen(QX0, QX1, QY0, QY1)
for i in range(4):
    a, b = QK[i], QK[(i + 1) % 4]
    for k in range(3):
        p, q = a.lerp(b, k / 3), a.lerp(b, (k + 1) / 3)
        if i != 1 and k == 1:
            duz_duvar(y, p, q, Z0, Z0 + 0.3, T)
            yildiz((p + q) / 2 + Z * (Z0 + 0.17), (q - p).normalized(), V((q - p).y, -(q - p).x).normalized(), 0.03, 'turkuaz', k=8, ic=0.55)
            continue
        if i == 1 and k == 1:
            kapi(y, p, q, Z0, 0.5, 0.24, (T, TK, TA, 'ahsap'), sivri=0.5, derin=0.03, cerceve=(0.008, ['turkuaz', TA]), k_say=10)
            duz_duvar(y, p, q, Z0 + 0.24, Z0 + 0.3, T)
            continue
        y.kemerli(p, q, Z0, 0.3, (T, TK, TA, 'koyu'), v0=0.07, en=0.4, ust=0.05, derin=0.02, k_say=6, sivri=0.55, cerceve=(0.006, TA))
silme(y, QK, Z0, 0.02, 0.01, TK, 'kaide')
y.yuz_yon([V(p.x, p.y, Z0 + 0.3) for p in QK], 'siva_krem', Z)
ust_bitis(QK, Z0 + 0.3, kapali=True)
QC = ((QX0 + QX1) / 2, (QY0 + QY1) / 2)
y.prizma(QC, 0.17, Z0 + 0.3, Z0 + 0.34, T, n=8, kat=math.pi / 8)
halka_kornis(y, QC, 0.17, Z0 + 0.335, 0.01, 0.008, 8, TA, kat=math.pi / 8)
kubbe_kasnakli(y, QC, 0.15, Z0 + 0.34, 0.06, n_pencere=8, kubbe_h=0.14, key=T, duvar=(T, TK, TA, 'koyu'), payanda=False, alem_olcek=0.8,
               sivri=0.5, n=20, kat=8, en=0.4, cerceve=(0.005, 'turkuaz'))
zq = Z0 + 0.34 + 0.06 + 0.016
donel(y, QC, [(0.155 * math.cos(ph) + 0.002 * math.cos(ph), zq + 0.14 * math.sin(ph) + 0.002 * math.sin(ph)) for ph in (0.0, math.pi / 20)] + [(0.155 * math.cos(math.pi / 20), zq + 0.14 * math.sin(math.pi / 20))], 'turkuaz', n=20)
# the minaret: an octagonal plinth with blind niches, a round brick shaft with bands of raised brick lozenges and
# glazed inscriptions, a muqarnas-corbelled balcony, the slim upper shaft and a turquoise cap
MP = 0.085
MK = cokgen((MX, MY), MP, 8, math.pi / 8)
for i in range(8):
    kemer_nis(y, MK[i], MK[(i + 1) % 8], Z0, 0.2, en=0.6, ust=0.02, sivri=0.5, derin=0.008, key=T, yan_key=TK, arka_key=TK, k_say=6)
silme(y, MK, Z0, 0.016, 0.008, TK, 'kaide')
silme(y, MK, Z0 + 0.2, 0.016, 0.01, TA, 'tac')
y.yuz_yon([V(p.x, p.y, Z0 + 0.216) for p in MK], TA, Z)
z1, z2 = Z0 + 0.216, Z0 + 0.9
r1, r2 = 0.06, 0.048
nb = 7
pr = [(r1 + (r2 - r1) * k / nb, z1 + (z2 - z1) * k / nb) for k in range(nb + 1)]
donel(y, (MX, MY), pr, T, n=20)
R = lambda zz: r1 + (r2 - r1) * (zz - z1) / (z2 - z1)
for k, zz in enumerate([z1 + (z2 - z1) * f for f in (0.12, 0.3, 0.48, 0.66)]):
    # a band of raised lozenges
    for i in range(14):
        a = TAU * (i + 0.5 * (k % 2)) / 14
        nrm = V(math.cos(a), math.sin(a), 0)
        yildiz(V(MX, MY, zz) + nrm * (R(zz) + 0.0005), V(-nrm.y, nrm.x, 0), nrm, 0.011, TK, k=2, ic=0.55, d=0.0018)
    donel(y, (MX, MY), [(R(zz - 0.03), zz - 0.03), (R(zz - 0.03) + 0.005, zz - 0.027), (R(zz - 0.03) + 0.005, zz - 0.022), (R(zz - 0.019), zz - 0.019)], TA, n=20)
for zz in (z1 + (z2 - z1) * 0.82,):
    donel(y, (MX, MY), [(R(zz), zz), (R(zz) + 0.0012, zz), (R(zz + 0.035) + 0.0012, zz + 0.035), (R(zz + 0.035), zz + 0.035)], 'turkuaz', n=20)
    for i in range(16):
        a = TAU * i / 16
        nrm = V(math.cos(a), math.sin(a), 0)
        yildiz(V(MX, MY, zz + 0.0175) + nrm * (R(zz + 0.0175) + 0.0004), V(-nrm.y, nrm.x, 0), nrm, 0.009, 'beyaz', k=2, ic=0.4, d=0.0018)
# the balcony: corbelled out in muqarnas steps, a parapet
ring = cokgen((MX, MY), r2, 16)
konsol_halka(y, ring, z2, 0.045, 0.04, TA, 4)
zb = z2 + 0.045
rb = disa(ring, 0.04)
y.yuz_yon([V(p.x, p.y, zb + 0.001) for p in rb], TA, Z)
parapet(y, rb, zb, 0.028, 0, 0.008, T, ust_key=TA)
for i in range(16):
    p, q = rb[i], rb[(i + 1) % 16]
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    yildiz((p + q) / 2 + Z * (zb + 0.014) + nn * 0.0005, e, nn, 0.008, 'turkuaz', k=4, ic=0.5, d=0.001)
# the upper shaft
z3 = zb + 0.15
donel(y, (MX, MY), [(0.036, zb), (0.034, z3)], T, n=16)
for i in range(6):
    a = TAU * i / 6
    nrm = V(math.cos(a), math.sin(a), 0)
    kutu_merkez(y, (MX + nrm.x * 0.034, MY + nrm.y * 0.034), 0.008, 0.012, 0.04, 'koyu', z0=zb + 0.06, aci=a)
halka_kornis(y, (MX, MY), 0.034, z3, 0.01, 0.01, 16, TA)
t = y.kubbe((MX, MY), 0.042, z3 + 0.01, 0.06, 'turkuaz', n=16, kat=6)
alem(y, MX, MY, t.z, 0.6, hilal=False)

# ---------------- the open markets ----------------
y.bolum('Baharat pazarı (ön sol)')


def tezgah(cx, cy, aci, k):
    """a market stall: four posts, a counter with sacks of spice and jars, a striped awning roof"""
    with parca(y, (cx, cy, Z0), aci):
        w, d, h = 0.17, 0.11, 0.15
        for sx in (-1, 1):
            for sy in (-1, 1):
                cubuk(y, V(sx * w / 2, sy * d / 2, 0), V(sx * w / 2, sy * d / 2, h + (0.02 if sy > 0 else 0)), 0.006, 'ahsap_koyu')
        kutu_merkez(y, (0, -d * 0.1), w * 0.92, d * 0.5, 0.045, 'ahsap')
        kutu_merkez(y, (0, -d * 0.1), w * 0.96, d * 0.56, 0.004, 'ahsap_acik', z0=0.045)
        for i in range(4):
            u = -w * 0.36 + w * 0.24 * i
            cuval(u, -d * 0.1, 0.049, r=0.012, h=0.016, ic=MAL[k % 5][i % 3])
        for i in range(3):
            cuval(-w * 0.3 + w * 0.3 * i, -d * 0.62, 0.0, r=0.015, h=0.026, ic=MAL[(k + 1) % 5][i % 3])
        kup(w * 0.42, d * 0.3, 0.0, key='kiremit')
        kup(w * 0.32, d * 0.36, 0.0, r=0.013, h=0.035, key='bakir')
        tk = TENTE[k % len(TENTE)]
        serit_tente((w / 2 + 0.01, d / 2 + 0.01, h + 0.02), (-w / 2 - 0.01, d / 2 + 0.01, h + 0.02),
                    (w / 2 + 0.01, -d / 2 - 0.03, h - 0.005), (-w / 2 - 0.01, -d / 2 - 0.03, h - 0.005), tk, n=7)


for k, (cx, cy, a) in enumerate(((-0.58, -0.36, 0.0), (-0.84, -0.36, 0.0), (-0.36, -0.62, math.pi / 2), (-0.36, -0.88, math.pi / 2))):
    tezgah(cx, cy, a, k)
# the fountain in the square
FC = (-0.7, -0.75)
havuz2(cokgen(FC, 0.078, 8, math.pi / 8), 0.012, Z0, TA, h=0.03)
y.prizma(FC, 0.018, Z0 + 0.03, Z0 + 0.08, 'turkuaz', n=8)
donel(y, FC, [(0.0, Z0 + 0.08), (0.04, Z0 + 0.082), (0.044, Z0 + 0.09), (0.0, Z0 + 0.088)], TA, n=12)
kure(y, (FC[0], FC[1], Z0 + 0.1), 0.012, 'turkuaz', n=8, kat=4)
for (tx, ty) in ((-0.98, -0.6), (-1.0, -0.98), (-0.98, -0.22)):
    palmiye(tx, ty, Z0, boy=0.3)
y.yuz_yon([V(-0.14, -1.13, Z0 + 0.0015), V(0.14, -1.13, Z0 + 0.0015), V(0.14, YF - 0.075, Z0 + 0.0015), V(-0.14, YF - 0.075, Z0 + 0.0015)], 'tas_koyu', Z)

y.bolum('Halı pazarı ve kervan (ön sağ)')


def hali_iskele(cx, cy, aci, renkler):
    """a carpet rack: two posts and a rail with carpets hung over it"""
    with parca(y, (cx, cy, Z0), aci):
        w, h = 0.26, 0.16
        for sx in (-1, 1):
            cubuk(y, V(sx * w / 2, 0, 0), V(sx * w / 2, 0, h + 0.01), 0.008, 'ahsap_koyu')
        boru(y, [V(-w / 2 - 0.01, 0, h), V(w / 2 + 0.01, 0, h)], 0.004, 'ahsap', n=6)
        n = len(renkler)
        cw = (w - 0.03) / n
        for i, (z_, k_, o_) in enumerate(renkler):
            hali(V(-w / 2 + 0.015 + i * cw + 0.004, 0.0, h - 0.004), X, cw - 0.008, 0.12, z_, k_, o_)


hali_iskele(0.6, -0.36, 0.0, [('boya_kirmizi', 'lacivert', 'boya_sari'), ('lacivert', 'boya_kirmizi', 'kece'), ('siva_oker', 'boya_kirmizi', 'lacivert')])
hali_iskele(0.36, -0.66, math.pi / 2, [('boya_kirmizi', 'kece', 'lacivert'), ('boya_yesil', 'boya_sari', 'boya_kirmizi')])
# rolled and stacked carpets
for i, (key, kk) in enumerate((('boya_kirmizi', 'lacivert'), ('lacivert', 'boya_kirmizi'), ('siva_oker', 'boya_kirmizi'))):
    zz = Z0 + 0.013 + i * 0.024
    xx = 0.82 - (i % 2) * 0.012
    boru(y, [V(xx - 0.07, -0.34 + i * 0.003, zz), V(xx + 0.07, -0.34 + i * 0.003, zz)], 0.012, key, n=8)
    for s in (-1, 1):
        y.yuz_yon([V(xx + s * 0.0705, -0.34 + i * 0.003 + 0.007 * math.cos(TAU * j / 8), zz + 0.007 * math.sin(TAU * j / 8)) for j in range(8)], kk, V(s, 0, 0))
for i, key in enumerate(('boya_kirmizi', 'lacivert', 'siva_oker', 'boya_yesil')):
    kutu_merkez(y, (0.62, -0.58), 0.16 - i * 0.012, 0.11 - i * 0.008, 0.007, key, z0=Z0 + i * 0.007, aci=0.15 * i)
deve(0.6, -0.86, math.pi * 0.92)
for (cx, cy, key, a) in ((0.4, -0.95, 'kumas', 0.3), (0.44, -0.99, 'boya_kirmizi', -0.2), (0.86, -0.72, 'kece', 0.5), (0.9, -0.66, 'kumas', -0.4)):
    denk(cx, cy, Z0, key, a)
for (tx, ty) in ((1.0, -0.98), (1.02, -0.36)):
    palmiye(tx, ty, Z0, boy=0.32)
palmiye(-0.98, 0.3, Z0, boy=0.3)

sancak(y, 0.12, YF - 0.04, top_ana, boy=0.22, en=0.12, yuk=0.075, aci=0.0)

calistir(y, 'lm_bagdatcarsi')
