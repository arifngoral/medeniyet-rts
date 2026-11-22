# Paralı Asker Kampı (lm_paraliasker): Carthage's camp of hired soldiers from many peoples inside a palisade of pointed
# logs with a timber gate and corner towers: the general's purple-striped marquee with Tanit standards and a tall timber
# watchtower beside it, the pay table heaped with silver and gold before a queue of mercenaries, Celtic round huts,
# Iberian ridge tents, Libyan hide tents, Numidian mapalia (upturned-boat huts) with a horse pen, a training ground with
# pells and targets, a smithy, a Tanit shrine, spear stacks, shield racks and cooking fires.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir
from kartaca_ortak import *
from frank_ortak import at, oturan

y = Yapi()
ZG = 0.04                     # the ground
X0, X1, Y0, Y1 = -1.12, 1.12, -1.12, 1.12
PL = 1.0                      # the palisade's half size
PH = 0.125                    # the palisade's height
GX = 0.1                      # the gate's half width
D = math.radians
g = random.Random(7)
MOR = 'mor'

# ================================================================ ground
y.bolum('Zemin')
kutu(y, V(X0, Y0, 0), X, X1 - X0, Y1 - Y0, ZG, 'toprak', 'onarkasagsol')
ic = PL + 0.03
y.yuz_yon([V(-ic, -ic, ZG), V(ic, -ic, ZG), V(ic, ic, ZG), V(-ic, ic, ZG)], 'toprak', Z)
dis_ = dikdortgen(X0, X1, Y0, Y1, ZG); ic_ = dikdortgen(-ic, ic, -ic, ic, ZG)
for i in range(4):
    j = (i + 1) % 4
    y.yuz_yon([dis_[i], dis_[j], ic_[j], ic_[i]], 'cimen_kuru', Z)
silme(y, dikdortgen(X0, X1, Y0, Y1), ZG - 0.008, 0.008, 0.005, 'toprak_ot', 'duz')


def yol(pts, key='kum_acik', dz=0.004):
    y.yuz_yon([V(p[0], p[1], ZG + dz) for p in pts], key, Z)


def leke(cx, cy, r, key='toprak_ot', n=9, tohum=0, dz=0.002):
    gg = random.Random(tohum)
    y.yuz_yon([V(cx + r * gg.uniform(0.7, 1.15) * math.cos(TAU * i / n), cy + r * gg.uniform(0.7, 1.15) * math.sin(TAU * i / n), ZG + dz) for i in range(n)],
              key, Z)


# the main street from the gate to the general's tent, the cross street, the road outside
yol([(-0.075, -PL - 0.12), (0.075, -PL - 0.12), (0.075, 0.0), (-0.075, 0.0)])
yol([(-0.88, -0.2), (-0.075, -0.2), (-0.075, -0.11), (-0.88, -0.11)])
yol([(0.075, -0.2), (0.88, -0.2), (0.88, -0.11), (0.075, -0.11)])
yol([(-0.075, -1.12), (0.075, -1.12), (0.075, -PL - 0.12), (-0.075, -PL - 0.12)], 'toprak_ot')
# trampled patches
for k, (cx, cy, r) in enumerate(((-0.55, -0.62, 0.16), (0.52, 0.6, 0.15), (-0.5, -0.33, 0.12), (0.3, 0.06, 0.1), (-0.16, 0.62, 0.1))):
    leke(cx, cy, r, tohum=k)


# ================================================================ helpers (this camp's own)
def kazik_cit(yol_, h, adim=0.03, r=0.013, gecit=(), tohum=0):
    """a palisade of pointed logs along a polyline (logs on the line), two rails on the inside (left); gecit: arc-length
    gaps (s0, s1)"""
    pts = [V(p[0], p[1]) for p in yol_]
    seg = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum((b - a).length for a, b in seg)
    gg = random.Random(tohum)
    def at_(s):
        for a, b in seg:
            l = (b - a).length
            if s <= l + 1e-9: return a.lerp(b, s / l), (b - a).normalized()
            s -= l
        a, b = seg[-1]; return b, (b - a).normalized()
    acik = lambda s: any(s0 <= s <= s1 for s0, s1 in gecit)
    n = int(L / adim)
    for k in range(n + 1):
        s = L * k / n
        if acik(s): continue
        p, e = at_(s)
        hh = h * gg.uniform(0.88, 1.0)
        y.prizma((p.x, p.y), r, ZG - 0.005, ZG + hh, 'kutuk', n=5, ust=False)
        y.koni((p.x, p.y), r, ZG + hh, r * 2.2, 'ahsap', n=5)
    sinir = [0.0] + [v for gp in gecit for v in gp] + [L]
    for i in range(0, len(sinir), 2):
        s0, s1 = sinir[i], sinir[i + 1]
        if s1 - s0 < 0.05: continue
        ss = [s0]; acc = 0.0
        for a, b in seg:
            acc += (b - a).length
            if s0 < acc < s1: ss.append(acc)
        ss.append(s1)
        for k in range(len(ss) - 1):
            p0, e0 = at_(ss[k] + 1e-6); p1, _ = at_(ss[k + 1] - 1e-6)
            nn = V(-e0.y, e0.x)
            for zr in (0.3, 0.72):
                cubuk(y, p0 + nn * (r + 0.004) + Z * (ZG + h * zr), p1 + nn * (r + 0.004) + Z * (ZG + h * zr), 0.008, 'ahsap_koyu', 0.006)


def kalkan_levha(c, ex, up, rx, ry, key, kalin=0.003, n=10, gobek=None):
    """a shield as a thin closed slab: centre c, its face spanned by ex (width) and up (height), the boss (gobek) a knob"""
    c, ex, up = Vector(c), Vector(ex).normalized(), Vector(up).normalized()
    nn = ex.cross(up).normalized()
    P = lambda u, v, d: c + ex * u + up * v + nn * d
    prizma2(y, [(rx * math.cos(TAU * i / n), ry * math.sin(TAU * i / n)) for i in range(n)], P, kalin, key, nn, arka=True)
    if gobek:
        kure(y, tuple(c + nn * (kalin + 0.0012)), min(rx, ry) * 0.25, gobek, n=6, kat=3)


def ahsap_kule(cx, cy, w, h, cati='saz', tabela=None, sancak_=None, olcek_cati=1.0, kalkanlar=None):
    """a timber tower: four posts, cross-bracing, a plank platform with a plank parapet (kalkanlar: keys of shields hung
    on it), four short posts carrying a pyramid roof. Returns the platform's floor z"""
    zf = ZG + h - 0.1
    hw = w / 2
    ks = [V(cx - hw, cy - hw), V(cx + hw, cy - hw), V(cx + hw, cy + hw), V(cx - hw, cy + hw)]
    for p in ks:
        cubuk(y, p + Z * (ZG - 0.005), p + Z * (zf + 0.1), 0.018, 'kutuk')
    for i in range(4):
        a, b = ks[i], ks[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for z0, z1 in ((ZG + 0.02, (ZG + zf) / 2), ((ZG + zf) / 2, zf - 0.01)):
            cubuk(y, a + nn * 0.01 + Z * z0, b + nn * 0.01 + Z * z1, 0.008, 'ahsap_koyu', 0.005)
            cubuk(y, b + nn * 0.01 + Z * z0, a + nn * 0.01 + Z * z1, 0.008, 'ahsap_koyu', 0.005)
        cubuk(y, a + nn * 0.011 + Z * ((ZG + zf) / 2), b + nn * 0.011 + Z * ((ZG + zf) / 2), 0.009, 'ahsap', 0.006)
    po = w + 0.05
    kutu_merkez(y, (cx, cy), po, po, 0.014, 'ahsap_acik', z0=zf)
    y.yuz_yon([V(cx - po / 2, cy - po / 2, zf), V(cx + po / 2, cy - po / 2, zf), V(cx + po / 2, cy + po / 2, zf), V(cx - po / 2, cy + po / 2, zf)], 'ahsap_koyu', -Z)
    for i in range(4):
        a = ks[i]
        cubuk(y, a + Z * (zf - 0.012), V(cx, cy) + (a - V(cx, cy)) * (po / w) + Z * (zf - 0.002), 0.008, 'ahsap', 0.008)
    k = dikdortgen(cx - po / 2, cx + po / 2, cy - po / 2, cy + po / 2)
    duvarlar(y, k, zf + 0.014, zf + 0.06, 'ahsap_dikey', ust='ahsap', kalinlik=0.008)
    if kalkanlar:
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            for j in range(2):
                c = a.lerp(b, (j + 1) / 3) + nn * 0.0035 + Z * (zf + 0.037)
                kalkan_levha(c, e, Z, 0.016, 0.016, kalkanlar[(i + j) % len(kalkanlar)], kalin=0.003, n=8, gobek='bronz')
    for p in ks:
        q = V(cx, cy) + (p - V(cx, cy)) * ((po / 2 - 0.006) / hw)
        cubuk(y, q + Z * (zf + 0.06), q + Z * (zf + 0.11), 0.01, 'kutuk')
    zt = cati_kirma(y, cx - po / 2 + 0.006, cx + po / 2 - 0.006, cy - po / 2 + 0.006, cy + po / 2 - 0.006, zf + 0.11, po * 0.55 * olcek_cati,
                    sacak=0.025, key=cati, mahya='ahsap', kalinlik=0.008, ns=3, nr=2, dilim=[cati, cati + '_koyu'] if cati == 'saz' else None)
    if tabela:
        tanit_kabartma(y, V(cx, cy - po / 2, zf + 0.018), X, -Y, 0.036, tabela, d=0.002)
    if sancak_ is not None:
        sancak(y, cx, cy, zt, boy=0.16, en=0.09, yuk=0.055, aci=sancak_)
    return zf


def yuvarlak_kulube(cx, cy, r, hw, hr, aci=0.0, duvar='ahsap_acik', cati='saz'):
    """a Celtic round house: a wattle wall, a dark door, a steep conical thatch with deep eaves"""
    n = 10
    y.prizma((cx, cy), r, ZG - 0.004, ZG + hw, duvar, n=n, ust=False)
    halka_kornis(y, (cx, cy), r, ZG + hw * 0.55, 0.006, 0.002, n, 'ahsap')
    sa = 0.022
    donel(y, (cx, cy), [(r + sa, ZG + hw - 0.006), (r * 0.35, ZG + hw + hr * 0.7), (0.0, ZG + hw + hr)], cati, n=n)
    ring0 = cokgen((cx, cy), r + sa, n, z=ZG + hw - 0.006); ring1 = cokgen((cx, cy), r, n, z=ZG + hw)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([ring0[i], ring0[j], ring1[j], ring1[i]], 'saz_koyu', -Z)
    td = math.pi * (2 * round((aci - math.pi / n) / (TAU / n)) + 1) / n   # the facet nearest aci
    ex = V(-math.sin(td), math.cos(td)); nrm = V(math.cos(td), math.sin(td))
    o = V(cx, cy) + nrm * (r * math.cos(math.pi / n))
    pencere_kutu(y, o, ex, nrm, -0.011, ZG, 0.022, hw * 0.8, 'koyu')
    donel(y, (cx, cy), [(r * 0.12, ZG + hw + hr * 0.95), (0.0, ZG + hw + hr + 0.008)], 'ahsap_koyu', n=5)


def cadir_a(cx, cy, aci, L, W, H, key='kece', serit='boya_kirmizi'):
    """an A-frame ridge tent along aci: two slopes, the gable ends (a dark door flap at the front), a painted hem band, poles"""
    with parca(y, (cx, cy, ZG), aci):
        hl, hw_ = L / 2, W / 2
        f = 0.22
        for s in (-1, 1):
            # the slope: the hem band below, the cloth above
            y.yuz_yon([V(-hl, s * hw_, 0), V(hl, s * hw_, 0), V(hl, s * hw_ * (1 - f), H * f), V(-hl, s * hw_ * (1 - f), H * f)], serit, V(0, s, 0.6))
            y.yuz_yon([V(-hl, s * hw_ * (1 - f), H * f), V(hl, s * hw_ * (1 - f), H * f), V(hl, 0, H), V(-hl, 0, H)], key, V(0, s, 0.6))
        for xx, sx in ((hl, 1), (-hl, -1)):
            y.yuz_yon([V(xx, -hw_, 0), V(xx, hw_, 0), V(xx, 0, H)], key, V(sx, 0, 0))
        y.yuz_yon([V(hl + 0.001, -hw_ * 0.32, 0), V(hl + 0.001, hw_ * 0.32, 0), V(hl + 0.001, 0, H * 0.62)], 'koyu', X)
        for xx in (-hl - 0.004, hl + 0.004):
            cubuk(y, V(xx, 0, 0), V(xx, 0, H + 0.016), 0.005, 'ahsap')
        cubuk(y, V(-hl - 0.004, 0, H + 0.002), V(hl + 0.004, 0, H + 0.002), 0.005, 'ahsap')


def mapalia(cx, cy, aci, L, W, H, key='saz', bant='ahsap_koyu'):
    """a Numidian mapalia: a long, low hut of reeds and hides shaped like an upturned boat (Sallust: 'oblong, with curved
    sides roofed over like the keels of ships'): a half-round vault that runs nearly straight and then draws in, in
    plan and in height, to a low point at each end; arched poles, a ridge bundle like a keel, a reed-hooded doorway in
    the middle of the long side"""
    n = 8
    ts = [-1.0, -0.94, -0.8, -0.55, -0.2, 0.2, 0.55, 0.8, 0.94, 1.0]
    hl = L / 2
    wf = lambda t: W / 2 * max(0.0, 1 - abs(t) ** 2.6) ** 0.42
    hf = lambda t: H * max(0.0, 1 - abs(t) ** 3.2) ** 0.3
    kes = lambda t, th, k=1.0: V(hl * t, wf(t) * math.cos(th) * k, hf(t) * math.sin(th) ** 0.85 * k)
    with parca(y, (cx, cy, ZG - 0.003), aci):
        rs = [[kes(t, math.pi * i / n) for i in range(n + 1)] for t in ts]
        for k in range(len(ts) - 1):
            for i in range(n):
                q = [rs[k][i], rs[k + 1][i], rs[k + 1][i + 1], rs[k][i + 1]]
                if abs(ts[k]) == 1.0: q = [rs[k][0], rs[k + 1][i], rs[k + 1][i + 1]]
                elif abs(ts[k + 1]) == 1.0: q = [rs[k][i], rs[k + 1][0], rs[k][i + 1]]
                c = sum(q, Vector()) / len(q)
                y.yuz_yon(q, key if (i // 2) % 2 == 0 else 'saz_koyu', V(c.x * 0.15, c.y, c.z + 0.002))
        # arched poles over the vault and the ridge bundle along the top like a keel
        for t in (-0.62, -0.22, 0.22, 0.62):
            boru(y, [kes(t, math.pi * i / n, 1.04) for i in range(n + 1)], 0.0024, bant, n=4)
        boru(y, [kes(t, math.pi / 2, 1.0) + Z * 0.002 for t in (-0.9, -0.7, -0.4, 0.0, 0.4, 0.7, 0.9)], 0.0036, bant, n=5)
        # the doorway on the long side (+y): a short reed hood over a dark opening, poles either side
        dw, dr = W * 0.16, H * 0.56
        y0, y1 = W * 0.2, W / 2 + 0.016
        ring = [V(dw * math.cos(math.pi * i / 6), 0, dr * math.sin(math.pi * i / 6)) for i in range(7)]
        for i in range(6):
            q = [ring[i] + Y * y0, ring[i + 1] + Y * y0, ring[i + 1] + Y * y1, ring[i] + Y * y1]
            c = sum(q, Vector()) / 4
            y.yuz_yon(q, key, V(c.x, 0, c.z))
        y.yuz_yon([p + Y * y1 for p in ring], 'saz_koyu', Y)
        y.yuz_yon([V(p.x * 0.72, y1 + 0.0015, p.z * 0.82) for p in ring], 'koyu', Y)
        boru(y, [ring[i] * 1.06 + Y * (y1 + 0.001) for i in range(7)], 0.0024, bant, n=4)
        for s in (-1, 1):   # a hide flap tied back
            y.yuz_yon([V(s * dw * 0.72, y1 + 0.003, 0.0), V(s * dw * 0.98, y1 + 0.003, 0.0), V(s * dw * 0.9, y1 + 0.003, dr * 0.7),
                       V(s * dw * 0.6, y1 + 0.003, dr * 0.62)][::s], 'kerpic_koyu', Y)


def mizrak_yigini(cx, cy, n=7, h=0.11, r=0.035, tohum=0):
    """spears stacked in a cone (their butts in a ring, the heads crossing above)"""
    gg = random.Random(tohum)
    top = V(cx, cy, ZG + h * 0.72)
    for k in range(n):
        a = TAU * k / n + gg.uniform(-0.15, 0.15)
        b = V(cx + r * math.cos(a), cy + r * math.sin(a), ZG)
        d = (top - b).normalized()
        tip = b + d * h
        cubuk(y, b, tip, 0.0035, 'ahsap')
        donel(y, (tip.x, tip.y), [(0.003, tip.z), (0.0, tip.z + 0.014)], 'demir', n=4)


def ates(cx, cy, s=1.0, kazan=True):
    """a cooking fire: a ring of stones, crossed logs, the flame, a bronze cauldron on a tripod"""
    for k in range(7):
        a = TAU * k / 7
        kure(y, (cx + 0.024 * s * math.cos(a), cy + 0.024 * s * math.sin(a), ZG + 0.002), 0.008 * s, 'kaya_koyu', n=5, kat=2)
    for a in (0.3, 1.9):
        cubuk(y, V(cx - 0.02 * s * math.cos(a), cy - 0.02 * s * math.sin(a), ZG + 0.004), V(cx + 0.02 * s * math.cos(a), cy + 0.02 * s * math.sin(a), ZG + 0.006),
              0.006 * s, 'ahsap_koyu')
    donel(y, (cx, cy), [(0.012 * s, ZG + 0.004), (0.009 * s, ZG + 0.016 * s), (0.0, ZG + 0.034 * s)], 'boya_sari', n=6)
    donel(y, (cx, cy), [(0.0065 * s, ZG + 0.012), (0.0, ZG + 0.028 * s)], 'boya_kirmizi', n=5)
    if kazan:
        zt = ZG + 0.07 * s
        for k in range(3):
            a = TAU * k / 3 + 0.4
            cubuk(y, V(cx + 0.035 * s * math.cos(a), cy + 0.035 * s * math.sin(a), ZG), V(cx, cy, zt), 0.004, 'ahsap_koyu')
        donel(y, (cx, cy), [(0.0, zt - 0.045 * s), (0.012 * s, zt - 0.043 * s), (0.016 * s, zt - 0.032 * s), (0.014 * s, zt - 0.022 * s),
                            (0.0, zt - 0.022 * s)], 'bronz', n=8)


def asker(x, yy, aci, halk, s=1.0, kol=0.0, kalkan=True, mizrak=True, z=None):
    """a mercenary by his people: robe, cap / helmet and shield colours"""
    giysi, sapka, kal = {
        'kelt': (g.choice(('boya_yesil', 'kirmizi', 'siva_oker')), None, g.choice(('boya_yesil', 'boya_kirmizi', 'ahsap_acik'))),
        'iber': ('beyaz', 'boya_kirmizi', 'bronz'),
        'numid': (g.choice(('kumas', 'siva_oker')), None, 'ahsap_acik'),
        'libya': ('kumas', 'kece', 'bronz'),
        'pon': (MOR, 'bronz', 'bronz'),
    }[halk]
    insan(y, x, yy, ZG if z is None else z, giysi, s, 'kerpic' if halk in ('numid', 'libya') else 'kum_acik', aci, kol, sapka,
          kalkan=kal if kalkan else None, mizrak='demir' if mizrak else None)


def sandik(cx, cy, aci, acik=False):
    """a strongbox with bronze bands: shut (a rounded lid) or open and heaped with silver"""
    kutu_merkez(y, (cx, cy), 0.05, 0.035, 0.03, 'ahsap_koyu', z0=ZG, aci=aci)
    for zz in (ZG + 0.006, ZG + 0.022):
        kutu_merkez(y, (cx, cy), 0.052, 0.037, 0.004, 'bronz', z0=zz, aci=aci)
    if acik:
        donel(y, (cx, cy), [(0.0172, ZG + 0.0302), (0.012, ZG + 0.037), (0.0, ZG + 0.04)], 'kursun', n=7)
    else:
        e = V(math.cos(aci), math.sin(aci))
        boru(y, [V(cx, cy, ZG + 0.03) - e * 0.025, V(cx, cy, ZG + 0.03) + e * 0.025], 0.0175, 'ahsap_koyu', n=6)


# ================================================================ the palisade, gate and corner towers
y.bolum('Palisad, kapı, köşe kuleleri')
cevre = [(-PL, -PL), (PL, -PL), (PL, PL), (-PL, PL), (-PL, -PL)]
kazik_cit(cevre, PH, gecit=((PL - GX - 0.13, PL + GX + 0.13),), tohum=3)
KALK = ('boya_kirmizi', 'bronz', 'boya_yesil', 'ahsap_acik')
for s in (-1, 1):
    ahsap_kule(s * (GX + 0.07), -PL, 0.12, 0.44, tabela='bronz', sancak_=D(160) if s < 0 else None, kalkanlar=KALK)
for sx in (-1, 1):
    for sy in (-1, 1):
        ahsap_kule(sx * (PL - 0.01), sy * (PL - 0.01), 0.11, 0.32, cati='ahsap_koyu')
# the gate: a double lintel with the sign of Tanit, the two leaves swung open
zl = ZG + 0.28
for dz in (0.0, 0.03):
    cubuk(y, V(-GX - 0.07, -PL, zl + dz), V(GX + 0.07, -PL, zl + dz), 0.018, 'kutuk')
kutu_merkez(y, (0, -PL - 0.004), 0.1, 0.006, 0.05, 'ahsap_koyu', z0=zl + 0.04)
tanit_kabartma(y, V(0, -PL - 0.007, zl + 0.044), X, -Y, 0.04, 'altin', d=0.002)
for s in (-1, 1):
    hinge = V(s * GX, -PL)
    d = V(-s * math.cos(D(70)), math.sin(D(70)))
    c_ = hinge + d * (GX * 0.95 / 2)
    kutu_merkez(y, (c_.x, c_.y), GX * 0.95, 0.012, 0.19, 'ahsap_dikey', z0=ZG, aci=math.atan2(d.y, d.x))
    for zz in (ZG + 0.04, ZG + 0.14):
        kutu_merkez(y, (c_.x, c_.y), GX * 0.9, 0.016, 0.014, 'ahsap_koyu', z0=zz, aci=math.atan2(d.y, d.x))
for s in (-1, 1):
    asker(s * 0.11, -PL + 0.05, D(-90), 'pon')
# grass tufts along the palisade, outside and in
gt = random.Random(11)
for k in range(70):
    side = k % 4
    t = gt.uniform(-1.05, 1.05)
    d = gt.choice((gt.uniform(1.04, 1.1), gt.uniform(0.9, 0.96)))
    x, yy = [(t, -d), (d, t), (t, d), (-d, t)][side]
    if abs(x) < 0.3 and yy < 0: continue
    for j in range(3):
        a = TAU * j / 3 + gt.uniform(0, 1)
        donel(y, (x + 0.008 * math.cos(a), yy + 0.008 * math.sin(a)), [(0.006, ZG), (0.0, ZG + gt.uniform(0.014, 0.024))], 'cimen', n=4)

# ================================================================ the general's pavilion and the watchtower
y.bolum('Komutan çadırı')
TX0, TX1, TY0, TY1 = -0.28, 0.28, 0.12, 0.48
HW_, HR_ = 0.13, 0.15
kutu(y, V(TX0 - 0.03, TY0 - 0.06, ZG), X, TX1 - TX0 + 0.06, TY1 - TY0 + 0.09, 0.012, 'ahsap', 'onarkasagsolust')
zb = ZG + 0.012
zw = zb + HW_
k = dikdortgen(TX0, TX1, TY0, TY1)
m0 = 14
for i in range(4):
    a, b = k[i], k[(i + 1) % 4]
    L = (b - a).length; m = m0 if i % 2 == 0 else max(2, int(L / 0.04))
    for j in range(m):
        p, q = a.lerp(b, j / m), a.lerp(b, (j + 1) / m)
        if i == 0 and m // 2 - 1 <= j <= m // 2: continue
        duz_duvar(y, p, q, zb, zw, MOR if j % 2 == 0 else 'kumas')
# the door: an opening with a dark inside, its flaps tied back
xa, xb = k[0].lerp(k[1], (m0 // 2 - 1) / m0), k[0].lerp(k[1], (m0 // 2 + 1) / m0)
DD = 0.03
y.yuz_yon([V(xa.x, TY0 + DD, zb), V(xb.x, TY0 + DD, zb), V(xb.x, TY0 + DD, zw), V(xa.x, TY0 + DD, zw)], 'koyu', -Y)
duz_duvar(y, V(xa.x, TY0), V(xa.x, TY0 + DD), zb, zw, 'kumas')
duz_duvar(y, V(xb.x, TY0 + DD), V(xb.x, TY0), zb, zw, 'kumas')
for xx, sg in ((xa.x, -1), (xb.x, 1)):
    levha_kapali(y, [V(xx, TY0 - 0.003, zb), V(xx + sg * 0.035, TY0 - 0.008, zb), V(xx, TY0 - 0.003, zw - 0.004)], MOR, -Y)
y.yuz_yon([V(xa.x, TY0, zw), V(xb.x, TY0, zw), V(xb.x, TY0 + DD, zw), V(xa.x, TY0 + DD, zw)], 'kumas', -Z)
y.yuz_yon([V(xa.x, TY0, zb + 0.001), V(xb.x, TY0, zb + 0.001), V(xb.x, TY0 + DD, zb + 0.001), V(xa.x, TY0 + DD, zb + 0.001)], 'boya_kirmizi', Z)
# the roof: a pitched canvas roof, ridge along x, deep overhang with a scalloped valance
sa = 0.032
zr = zw + HR_
ym = (TY0 + TY1) / 2
EG = HR_ / ((TY1 - TY0) / 2)
ze = zw - sa * EG
for s in (-1, 1):
    ye = (TY0 - sa) if s < 0 else (TY1 + sa)
    q = [V(TX0 - sa, ye, ze), V(TX1 + sa, ye, ze), V(TX1 + sa, ym, zr), V(TX0 - sa, ym, zr)]
    nrm = V(0, s, 1 / EG)
    nb = 14
    for j in range(nb):
        a0, a1 = q[0].lerp(q[1], j / nb), q[0].lerp(q[1], (j + 1) / nb)
        b0, b1 = q[3].lerp(q[2], j / nb), q[3].lerp(q[2], (j + 1) / nb)
        y.yuz_yon([a0, a1, b1, b0], MOR if j % 2 == 0 else 'kumas', nrm)
        y.yuz_yon([a0 - Z * 0.003, a1 - Z * 0.003, b1 - Z * 0.003, b0 - Z * 0.003], 'kumas', -nrm)
        mid = (a0 + a1) / 2 - Z * 0.024
        levha_kapali(y, [a0 - Z * 0.0016, a1 - Z * 0.0016, mid], 'boya_kirmizi' if j % 2 == 0 else 'altin', V(0, s, 0))
    y.yuz_yon([q[0], q[1], q[1] - Z * 0.003, q[0] - Z * 0.003], 'kumas', V(0, s, 0))
for xx, sx in ((TX0, -1), (TX1, 1)):
    y.yuz_yon([V(xx, TY0, zw), V(xx, TY1, zw), V(xx, ym, zr - 0.002)], 'kumas', V(sx, 0, 0))
    xe = TX0 - sa if sx < 0 else TX1 + sa
    for ye in (TY0 - sa, TY1 + sa):
        y.yuz_yon([V(xe, ye, ze), V(xe, ym, zr), V(xe, ym, zr - 0.003), V(xe, ye, ze - 0.003)], MOR, V(sx, 0, 0))
    # a purple roundel with the sign of Tanit on the gable
    kalkan_levha(V(xx, ym, zw + 0.05), V(0, -sx, 0), Z, 0.028, 0.028, MOR, kalin=0.002, n=12)
    tanit_kabartma(y, V(xx + sx * 0.002, ym, zw + 0.031), V(0, -sx, 0), V(sx, 0, 0), 0.036, 'altin', d=0.0015)
boru(y, [V(TX0 - sa - 0.012, ym, zr + 0.003), V(TX1 + sa + 0.012, ym, zr + 0.003)], 0.005, 'ahsap', n=5)
for xx in (TX0 + 0.07, TX1 - 0.07):
    cubuk(y, V(xx, ym, zr - 0.01), V(xx, ym, zr + 0.055), 0.008, 'ahsap')
    kure(y, (xx, ym, zr + 0.064), 0.011, 'altin', n=8, kat=4)
tanit_heykel(y, 0.0, ym, zr + 0.004, 0.075, 'altin', aci=D(-90))
# the porch: an awning on two poles over the door (below the roof's eave), a carpet, two Tanit standards
PY = TY0 - 0.11
zaw0, zaw1 = ze - 0.03, ze - 0.008
for xx in (-0.085, 0.085):
    cubuk(y, V(xx, PY, zb), V(xx, PY, zaw0 + 0.012), 0.008, 'ahsap')
    kure(y, (xx, PY, zaw0 + 0.018), 0.007, 'altin', n=6, kat=3)
aw = [V(-0.1, PY - 0.008, zaw0), V(0.1, PY - 0.008, zaw0), V(0.1, TY0 - sa - 0.004, zaw1), V(-0.1, TY0 - sa - 0.004, zaw1)]
y.yuz_yon(aw, MOR, Z + V(0, -0.3, 0))
y.yuz_yon([p - Z * 0.003 for p in aw], 'kumas', -Z)
for a_, b_, yon in ((aw[0], aw[1], -Y), (aw[1], aw[2], X), (aw[3], aw[0], -X), (aw[2], aw[3], Y)):
    y.yuz_yon([a_, b_, b_ - Z * 0.003, a_ - Z * 0.003], 'boya_kirmizi', yon)
for j in range(8):
    a0, a1 = aw[0].lerp(aw[1], j / 8), aw[0].lerp(aw[1], (j + 1) / 8)
    levha_kapali(y, [a0 - Z * 0.0035, a1 - Z * 0.0035, (a0 + a1) / 2 - Z * 0.018], 'boya_kirmizi' if j % 2 else 'altin', -Y)
y.yuz_yon([V(-0.1, PY - 0.03, zb + 0.0012), V(0.1, PY - 0.03, zb + 0.0012), V(0.1, TY0, zb + 0.0012), V(-0.1, TY0, zb + 0.0012)], 'boya_kirmizi', Z)
for xx in (-0.15, 0.15):
    cubuk(y, V(xx, PY - 0.02, ZG), V(xx, PY - 0.02, ZG + 0.22), 0.007, 'ahsap')
    kutu_merkez(y, (xx, PY - 0.02), 0.045, 0.006, 0.014, MOR, z0=ZG + 0.185)
    tanit_heykel(y, xx, PY - 0.02, ZG + 0.22, 0.05, 'altin', aci=D(-90))
for s in (-1, 1):
    asker(s * 0.11, PY - 0.06, D(-90), 'pon', kalkan=True)

y.bolum('Gözcü kulesi')
WX, WY = 0.5, 0.36
zf = ahsap_kule(WX, WY, 0.16, 0.8, cati='saz', tabela='bronz', olcek_cati=1.1, sancak_=D(170), kalkanlar=KALK)
for zz in (ZG + 0.25, ZG + 0.5):
    kutu_merkez(y, (WX, WY), 0.17, 0.17, 0.01, 'ahsap_acik', z0=zz)
    y.yuz_yon([V(WX - 0.085, WY - 0.085, zz), V(WX + 0.085, WY - 0.085, zz), V(WX + 0.085, WY + 0.085, zz), V(WX - 0.085, WY + 0.085, zz)], 'ahsap_koyu', -Z)
for s in (-1, 1):
    cubuk(y, V(WX + s * 0.02, WY - 0.135, ZG), V(WX + s * 0.02, WY - 0.095, zf + 0.012), 0.006, 'ahsap')
for k in range(16):
    t = (k + 0.5) / 16
    p = V(WX, WY - 0.135, ZG).lerp(V(WX, WY - 0.095, zf + 0.012), t)
    cubuk(y, p - X * 0.02, p + X * 0.02, 0.004, 'ahsap_acik')
insan(y, WX - 0.03, WY - 0.05, zf + 0.014, MOR, 1.0, 'kum_acik', D(-110), 0.0, 'bronz', mizrak='demir')
insan(y, WX + 0.03, WY + 0.03, zf + 0.014, 'kumas', 1.0, 'kerpic', D(30), 0.8, None)

# ================================================================ the pay table
y.bolum('Ödeme masası')
MXC, MYC = 0.0, -0.075
kutu_merkez(y, (MXC, MYC), 0.2, 0.06, 0.03, 'ahsap', z0=ZG)
kutu_merkez(y, (MXC, MYC), 0.21, 0.07, 0.004, 'ahsap_acik', z0=ZG + 0.03)
zt = ZG + 0.034
for k in range(9):
    xx = MXC - 0.085 + 0.021 * k
    hh = 0.004 + 0.003 * ((k * 5) % 4)
    y.prizma((xx, MYC - 0.012), 0.0055, zt, zt + hh, 'kursun' if k % 3 else 'altin', n=6)
    if k % 2 == 0:
        y.prizma((xx + 0.008, MYC + 0.012), 0.0055, zt, zt + hh * 0.7, 'altin' if k % 4 else 'kursun', n=6)
cubuk(y, V(MXC + 0.07, MYC + 0.012, zt), V(MXC + 0.07, MYC + 0.012, zt + 0.035), 0.003, 'bronz')
cubuk(y, V(MXC + 0.05, MYC + 0.012, zt + 0.035), V(MXC + 0.09, MYC + 0.012, zt + 0.035), 0.0025, 'bronz')
for xx in (MXC + 0.05, MXC + 0.09):
    donel(y, (xx, MYC + 0.012), [(0.0, zt + 0.012), (0.009, zt + 0.014), (0.0, zt + 0.014)], 'bronz', n=6)
    cubuk(y, V(xx, MYC + 0.012, zt + 0.014), V(xx, MYC + 0.012, zt + 0.035), 0.0012, 'ahsap_koyu')
sandik(MXC - 0.13, MYC + 0.01, 0.2, acik=True)
sandik(MXC + 0.14, MYC + 0.0, -0.15)
sandik(MXC + 0.15, MYC + 0.05, 0.1, acik=True)
oturan(y, MXC - 0.03, MYC + 0.045, ZG, MOR, aci=D(-90), s=1.2)
oturan(y, MXC + 0.04, MYC + 0.045, ZG, 'beyaz', aci=D(-90), s=1.1)
for k, halk in enumerate(('kelt', 'iber', 'numid', 'libya', 'kelt', 'iber', 'numid', 'kelt', 'libya')):
    asker(g.uniform(-0.025, 0.025), MYC - 0.075 - 0.05 * k, D(90), halk, kol=0.6 if k == 0 else 0.0)

# ================================================================ the peoples' quarters
y.bolum('Keltler: yuvarlak kulübeler')
for (x, yy, r) in ((0.74, 0.8, 0.075), (0.86, 0.52, 0.065), (0.7, 0.58, 0.07), (0.22, 0.82, 0.07), (0.47, 0.82, 0.065), (0.85, 0.24, 0.065),
                   (0.27, 0.6, 0.06)):
    yuvarlak_kulube(x, yy, r, 0.055, 0.09 + r * 0.3, aci=math.atan2(-yy, -x))
for (x, yy, a) in ((0.58, 0.7, 0.3), (0.38, 0.68, 2.0), (0.9, 0.7, 4.0), (0.74, 0.4, 1.2), (0.6, 0.22, 2.5)):
    asker(x, yy, a, 'kelt')
ates(0.56, 0.66)
for kk in range(4):   # oval Celtic shields leaning on a rail
    c = V(0.33 + 0.032 * kk, 0.468, ZG + 0.03)
    kalkan_levha(c, X, V(0, 0.35, 1), 0.012, 0.03, ('boya_yesil', 'boya_kirmizi', 'siva_oker', 'boya_yesil')[kk], gobek='bronz')
cubuk(y, V(0.3, 0.485, ZG + 0.05), V(0.44, 0.485, ZG + 0.05), 0.005, 'ahsap')
for xx in (0.3, 0.44):
    cubuk(y, V(xx, 0.485, ZG), V(xx, 0.485, ZG + 0.054), 0.005, 'ahsap')

y.bolum('İberler ve Libyalılar: çadırlar')
for i in range(3):
    for j in range(3):
        x = -0.84 + 0.17 * i + (0.03 if j % 2 else 0.0)
        yy = -0.87 + 0.15 * j
        cadir_a(x, yy, D(90), 0.12, 0.085, 0.07, key=('kece', 'kumas', 'kece')[(i + j) % 3], serit=('boya_kirmizi', MOR, 'boya_kirmizi')[(i * 2 + j) % 3])
for j in range(3):
    cadir_a(-0.3, -0.87 + 0.15 * j, D(90), 0.12, 0.085, 0.07, key='kece', serit='boya_kirmizi')
for (x, yy, a) in ((-0.62, -0.5, 0.4), (-0.46, -0.52, 2.6), (-0.2, -0.6, 1.2)):
    asker(x, yy, a, 'iber')
ates(-0.38, -0.5)
for kk in range(3):   # round bronze caetrae on a stand
    kalkan_levha(V(-0.62 + 0.026 * kk, -0.43, ZG + 0.024), X, V(0, -0.3, 1), 0.016, 0.016, 'bronz', gobek='altin')
mizrak_yigini(-0.2, -0.45, tohum=1)
for i in range(4):   # the Libyans' hide tents
    cadir_a(-0.8 + 0.17 * i, -0.3, D(90) + (0.15 if i % 2 else -0.1), 0.13, 0.1, 0.075, key='kerpic', serit='kerpic_koyu')
for (x, yy, a) in ((-0.72, -0.4, 1.0), (-0.3, -0.4, 2.2)):
    asker(x, yy, a, 'libya')

y.bolum('Numidyalılar: mapalia, at ağılı')
for (x, yy, a) in ((-0.8, 0.1, 0.18), (-0.56, 0.05, -0.14), (-0.32, 0.12, 0.1), (-0.83, 0.33, 1.52 + math.pi), (-0.24, 0.39, 1.4)):
    mapalia(x, yy, a, 0.215, 0.088, 0.066)
PX0, PX1, PY0, PY1 = -0.92, -0.38, 0.52, 0.92
pk = [V(PX0, PY0), V(PX1, PY0), V(PX1, PY1), V(PX0, PY1)]
for i in range(4):
    a, b = pk[i], pk[(i + 1) % 4]
    m = max(1, int((b - a).length / 0.1))
    for j in range(m):
        p = a.lerp(b, j / m)
        cubuk(y, p + Z * (ZG - 0.004), p + Z * (ZG + 0.05), 0.008, 'kutuk')
    if i == 0:
        mid = a.lerp(b, 0.5)
        segs = [(a, mid - X * 0.04), (mid + X * 0.04, b)]
    else:
        segs = [(a, b)]
    for p, q in segs:
        for zr in (0.02, 0.042):
            cubuk(y, p + Z * (ZG + zr), q + Z * (ZG + zr), 0.006, 'ahsap', 0.005)
leke(-0.65, 0.72, 0.2, 'toprak_ot', tohum=9, dz=0.003)
tk = dikdortgen(-0.57, -0.43, 0.85, 0.885)
duvarlar(y, tk, ZG, ZG + 0.022, 'ahsap', ust='ahsap_acik', kalinlik=0.005)
y.yuz_yon([V(p.x, p.y, ZG + 0.016) for p in disa(tk, -0.005)], 'su', Z)
for kk, (x, yy, a, key) in enumerate(((-0.8, 0.62, 0.4, 'ahsap'), (-0.66, 0.74, 2.4, 'ahsap_acik'), (-0.5, 0.62, 3.6, 'koyu'),
                                      (-0.8, 0.84, -0.6, 'ahsap_acik'), (-0.62, 0.86, 0.1, 'ahsap'), (-0.45, 0.76, 1.7, 'beyaz'))):
    at(y, x, yy, ZG, a, 1.05, key, 'ahsap_koyu', faz=0.2 * kk)
asker(-0.36, 0.64, 2.8, 'numid', kalkan=False)
asker(-0.42, 0.28, 1.0, 'numid')
asker(-0.66, 0.2, -0.4, 'numid', mizrak=False)
ates(-0.5, 0.26, 0.9)

y.bolum('Talim alanı')
SX0, SX1, SY0, SY1 = 0.18, 0.86, -0.88, -0.34
yol([(SX0, SY0), (SX1, SY0), (SX1, SY1), (SX0, SY1)], 'kum_acik', 0.006)
sk = [V(SX0, SY0), V(SX1, SY0), V(SX1, SY1), V(SX0, SY1)]
for i in range(4):
    a, b = sk[i], sk[(i + 1) % 4]
    m = max(1, int((b - a).length / 0.12))
    for j in range(m + 1):
        p = a.lerp(b, j / m)
        cubuk(y, p + Z * ZG, p + Z * (ZG + 0.035), 0.007, 'ahsap')
    if i == 3:
        mid = a.lerp(b, 0.5)
        segs = [(a, mid + Y * 0.05), (mid - Y * 0.05, b)]
    else:
        segs = [(a, b)]
    for p, q in segs:
        cubuk(y, p + Z * (ZG + 0.03), q + Z * (ZG + 0.03), 0.005, 'ahsap', 0.005)
for kk in range(4):
    x = SX0 + 0.1 + 0.1 * kk
    py = SY1 - 0.08
    cubuk(y, V(x, py, ZG), V(x, py, ZG + 0.07), 0.01, 'kutuk')
    if kk % 2 == 0:
        donel(y, (x, py), [(0.0, ZG + 0.03), (0.011, ZG + 0.032), (0.012, ZG + 0.06), (0.0, ZG + 0.064)], 'saz', n=6)
        kure(y, (x, py, ZG + 0.073), 0.008, 'saz', n=6, kat=3)
    asker(x, py - 0.04, D(90), ('kelt', 'iber', 'libya', 'pon')[kk], kol=1.0, kalkan=kk % 2 == 1, mizrak=False)
nn_ = V(-1, 0, 0.25).normalized()
for kk in range(2):
    x = SX1 - 0.07
    py = SY0 + 0.1 + 0.16 * kk
    for s in (-1, 1):
        cubuk(y, V(x - 0.012, py + s * 0.02, ZG), V(x + 0.004, py + s * 0.012, ZG + 0.06), 0.005, 'ahsap')
    c = V(x + 0.006, py, ZG + 0.05)
    for rr, key, d, kl in ((0.03, 'saz', 0.0, 0.004), (0.02, 'beyaz', 0.0042, 0.0015), (0.01, 'boya_kirmizi', 0.0059, 0.0015)):
        kalkan_levha(c + nn_ * d, -Y, V(0.25, 0, 1), rr, rr, key, kalin=kl, n=10)
    for j in range(2):
        insan(y, SX0 + 0.14 + 0.05 * j, py + 0.02 * j, ZG, 'kumas' if j else 'boya_kirmizi', 1.0, 'kerpic', 0.0, 0.7, None)
for (x, yy) in ((0.46, -0.66), (0.58, -0.56), (0.4, -0.48)):
    asker(x - 0.02, yy, 0.0, 'iber', kol=0.9)
    asker(x + 0.02, yy, math.pi, 'kelt', kol=0.6)
cubuk(y, V(SX0 + 0.04, SY0 + 0.03, ZG + 0.06), V(SX0 + 0.04, SY0 + 0.22, ZG + 0.06), 0.006, 'ahsap')
for yy in (SY0 + 0.03, SY0 + 0.22):
    cubuk(y, V(SX0 + 0.04, yy, ZG), V(SX0 + 0.04, yy, ZG + 0.064), 0.007, 'ahsap')
for kk in range(9):
    yy = SY0 + 0.045 + 0.018 * kk
    cubuk(y, V(SX0 + 0.05, yy, ZG), V(SX0 + 0.034, yy, ZG + 0.12), 0.0035, 'ahsap')
    donel(y, (SX0 + 0.034 - 0.0016, yy), [(0.003, ZG + 0.12), (0.0, ZG + 0.135)], 'demir', n=4)

y.bolum('Demirci, sunak, silah yığınları, ikmal')
# the smithy: an open shed on four posts with a thatched lean-to roof, a clay forge with its fire, an anvil, the smith
FX0, FX1, FY0, FY1 = 0.6, 0.84, -0.06, 0.1
for (x, yy) in ((FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)):
    cubuk(y, V(x, yy, ZG), V(x, yy, ZG + (0.11 if yy == FY0 else 0.15)), 0.012, 'kutuk')
q = [V(FX0 - 0.02, FY0 - 0.03, ZG + 0.105), V(FX1 + 0.02, FY0 - 0.03, ZG + 0.105), V(FX1 + 0.02, FY1 + 0.02, ZG + 0.155), V(FX0 - 0.02, FY1 + 0.02, ZG + 0.155)]
y.yuz_yon(q, 'saz', V(0, -0.3, 1))
y.yuz_yon([p - Z * 0.008 for p in q], 'saz_koyu', -Z)
qc = sum(q, Vector()) / 4
for a_, b_ in ((q[0], q[1]), (q[1], q[2]), (q[2], q[3]), (q[3], q[0])):
    d_ = (a_ + b_) / 2 - qc; d_.z = 0
    y.yuz_yon([a_, b_, b_ - Z * 0.008, a_ - Z * 0.008], 'saz_koyu', d_)
kutu_merkez(y, (FX0 + 0.06, FY1 - 0.03), 0.08, 0.05, 0.035, 'kerpic', z0=ZG)
donel(y, (FX0 + 0.06, FY1 - 0.03), [(0.012, ZG + 0.035), (0.007, ZG + 0.05), (0.0, ZG + 0.062)], 'boya_sari', n=6)
y.prizma((FX0 + 0.06, FY1 - 0.01), 0.012, ZG + 0.035, ZG + 0.17, 'kerpic_koyu', n=6)
kutu_merkez(y, (FX1 - 0.07, FY0 + 0.06), 0.02, 0.02, 0.022, 'kutuk', z0=ZG)
kutu_merkez(y, (FX1 - 0.07, FY0 + 0.06), 0.034, 0.016, 0.01, 'demir', z0=ZG + 0.022)
insan(y, FX1 - 0.1, FY0 + 0.06, ZG, 'ahsap_koyu', 1.05, 'kum_acik', 0.0, 1.0, None)
kutu_merkez(y, (FX0 + 0.1, FY0 - 0.05), 0.18, 0.02, 0.025, 'ahsap', z0=ZG)
for kk in range(4):   # finished blades on the bench
    kutu_merkez(y, (FX0 + 0.04 + 0.04 * kk, FY0 - 0.05), 0.03, 0.008, 0.003, 'demir', z0=ZG + 0.025, aci=0.2)
# the Tanit shrine: a stepped altar with a stele, an incense burner, a worshipper
SX, SY = -0.12, 0.66
for kk, (w, h) in enumerate(((0.12, 0.012), (0.09, 0.024), (0.06, 0.034))):
    kutu_merkez(y, (SX, SY), w, w * 0.8, h, 'kum_acik' if kk % 2 else 'kum', z0=ZG)
kutu_merkez(y, (SX, SY + 0.012), 0.034, 0.012, 0.085, 'kum_acik', z0=ZG + 0.034)
kavetto(y, dikdortgen(SX - 0.017, SX + 0.017, SY + 0.006, SY + 0.018), ZG + 0.119, 0.012, 0.006, 'kum_acik')
tanit_kabartma(y, V(SX, SY + 0.006, ZG + 0.06), X, -Y, 0.04, 'boya_kirmizi', d=0.0015)
donel(y, (SX + 0.03, SY - 0.03), [(0.006, ZG + 0.034), (0.004, ZG + 0.045), (0.009, ZG + 0.052), (0.0, ZG + 0.052)], 'bronz', n=6)
oturan(y, SX - 0.05, SY - 0.07, ZG, MOR, aci=D(60), s=1.0)
for (x, yy, t) in ((0.25, -0.04, 2), (-0.2, -0.04, 3), (0.4, 0.15, 4), (0.08, 0.6, 5), (0.86, -0.28, 6), (-0.9, -0.6, 7), (-0.12, -0.88, 8)):
    mizrak_yigini(x, yy, tohum=t)
for (x, yy) in ((0.62, -0.27), (0.12, 0.7)):
    ates(x, yy)
# supply: amphorae, sacks and a cart
for kk in range(8):
    x = -0.92 + 0.024 * (kk % 4); yy = -0.06 + 0.024 * (kk // 4)
    donel(y, (x, yy), [(0.004, ZG), (0.011, ZG + 0.014), (0.006, ZG + 0.028), (0.0045, ZG + 0.034), (0, ZG + 0.034)], 'siva_oker', n=6)
for kk in range(5):
    kutu_merkez(y, (-0.8 + 0.03 * kk, -0.05 + 0.01 * (kk % 2)), 0.028, 0.022, 0.02, 'kumas' if kk % 2 else 'saz', z0=ZG, aci=0.3 * kk)
cx, cy = 0.4, -0.27
kutu_merkez(y, (cx, cy), 0.1, 0.06, 0.02, 'ahsap', z0=ZG + 0.03)
for s in (-1, 1):
    kalkan_levha(V(cx, cy + s * 0.035, ZG + 0.028), X, Z, 0.026, 0.026, 'ahsap_koyu', kalin=0.004, n=10)
cubuk(y, V(cx - 0.05, cy, ZG + 0.035), V(cx - 0.13, cy, ZG + 0.012), 0.006, 'ahsap')
for kk in range(4):
    donel(y, (cx - 0.03 + 0.02 * kk, cy), [(0.006, ZG + 0.05), (0.011, ZG + 0.06), (0.006, ZG + 0.07), (0, ZG + 0.072)], 'siva_oker', n=6)

y.bolum('Ağaçlar, yayalar')
for (x, yy, tur, b) in ((-0.9, 0.46, 'palmiye', 0.15), (0.92, 0.04, 'palmiye', 0.14), (0.05, 0.9, 'palmiye', 0.16), (-0.42, 0.92, 'palmiye', 0.13),
                        (0.93, 0.92, 'yaprakli', 0.12), (-0.93, -0.93, 'yaprakli', 0.11), (0.66, 0.92, 'palmiye', 0.14)):
    agac(y, x, yy, ZG, b, tur, 'zeytin', 'ahsap_acik')
for k, (cx, cy, r) in enumerate(((0.12, 0.92, 0.12), (-0.88, 0.48, 0.1), (0.92, 0.9, 0.1), (-0.15, 0.32, 0.1))):
    leke(cx, cy, r, 'cimen_kuru', tohum=20 + k, dz=0.0025)
gw = random.Random(23)
for (x, yy) in ((-0.5, -0.155), (-0.3, -0.16), (0.3, -0.15), (0.55, -0.165), (0.75, -0.14), (-0.7, -0.15), (0.03, -0.6), (-0.03, -0.85),
                (0.15, 0.04), (-0.18, 0.08), (0.2, 0.36), (-0.4, 0.5)):
    asker(x, yy, gw.uniform(0, TAU), gw.choice(('kelt', 'iber', 'numid', 'libya', 'pon')), kalkan=gw.random() < 0.5, mizrak=gw.random() < 0.6)
for (x, yy, a) in ((-0.15, 0.2, 0.3), (0.2, 0.2, -0.2), (-0.86, -0.75, 0.0)):
    for j in range(2):
        kutu_merkez(y, (x + 0.032 * j, yy), 0.03, 0.03, 0.028, 'ahsap' if j else 'ahsap_acik', z0=ZG, aci=a)
    y.prizma((x + 0.016, yy + 0.034), 0.013, ZG, ZG + 0.034, 'ahsap_koyu', n=8)

calistir(y, 'lm_paraliasker')
