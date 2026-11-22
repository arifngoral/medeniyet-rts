# Jomsborg (lm_jomsborg): the Jomsvikings' sea fortress - an earth rampart crowned with a log palisade and timber
# towers round an inner harbour, entered from the sea through a great stone water gate (a through arch with a raised
# iron grille) under a tall tower with an overhanging fighting gallery and a shingled spire. Longships lie at the
# quays inside, one more comes in from the sea; longhouses line the harbour, a timber land gate opens at the back.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05            # ground top
ZW = 0.02            # water level
SH = ['sindira', 'sindira2']
GX0, GX1, GY0, GY1 = -1.2, 1.2, -1.08, 1.06
SEA = -0.78          # the shore line (water in front of it)
RF = -0.6            # rampart line at the front
RB = 0.85            # rampart line at the back
RS = 0.95            # rampart line at the sides
BX, BY0, BY1 = 0.5, -0.4, 0.15    # harbour basin
CH = 0.155           # half width of the channel through the gate
ZR = Z0 + 0.13       # rampart crest


# ---------------------------------------------------------------- helpers
def levha(pts, key, yon, kil=0.002):
    """a thin sheet seen from both sides (sail, vane, door leaf): the face toward yon, its twin kil behind, and the
    rims between them all round (an open rim shows the twin's back at the silhouette)"""
    pts = [V(*p) for p in pts]; yon = V(*yon).normalized()
    iki_yuzlu(y, pts, key, yon, kil)
    c = sum(pts, V(0, 0, 0)) / len(pts) - yon * (kil / 2)
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        if (b - a).length < 1e-7: continue
        yuz_dis(y, [a, b, b - yon * kil, a - yon * kil], key, c)


def yuvarla(pts, r, n=6):
    """a polyline with its inner corners rounded (fillets of radius r)"""
    pts = [V(*p) for p in pts]
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        e1, e2 = (b - a).normalized(), (c - b).normalized()
        p0, p1 = b - e1 * r, b + e2 * r
        for k in range(n + 1):   # (a quadratic curve between the tangent points)
            t = k / n
            out.append(p0 * (1 - t) ** 2 + b * 2 * t * (1 - t) + p1 * t * t)
    out.append(pts[-1])
    return out


def sur_toprak(yol):
    """an earth rampart along an open polyline (outside on the right): grassy outer and inner slopes, a trodden top,
    closed ends"""
    prof = [(0.15, Z0 - 0.004), (0.035, ZR), (-0.055, ZR), (-0.17, Z0 - 0.004)]
    keys = ['cimen', 'toprak', 'cimen']
    rings = [[V(p.x, p.y, z) for p in disa(yol, o, False)] for o, z in prof]
    for k in range(len(rings) - 1):
        y.serit(rings[k], rings[k + 1], keys[k], kapali=False)
    for uc, s in ((0, -1), (-1, 1)):
        e = (yol[1] - yol[0]) if uc == 0 else (yol[-1] - yol[-2]); e.z = 0
        y.yuz_yon([r[uc] for r in rings], 'toprak', e * s)


def palisad(yol, z, h, adim=0.026, r=0.012, tohum=0):
    """a palisade of pointed upright logs along a polyline, with a rail and a wall walk behind it"""
    L = sum((yol[i + 1] - yol[i]).length for i in range(len(yol) - 1))
    n = int(L / adim)
    seg = [(yol[i], yol[i + 1]) for i in range(len(yol) - 1)]
    def at(s):
        for a, b in seg:
            l = (b - a).length
            if s <= l: return a.lerp(b, s / max(l, 1e-9)), (b - a).normalized()
            s -= l
        a, b = seg[-1]; return b, (b - a).normalized()
    for k in range(n + 1):
        p, e = at(L * k / n)
        hh = h * (0.93 + 0.07 * ((k * 7 + tohum) % 5) / 4)
        y.prizma((p.x, p.y), r, z - 0.02, z + hh, 'kutuk', n=6, ust=False)
        y.koni((p.x, p.y), r, z + hh, 0.022, 'ahsap', n=6)
    # the rail behind (inside) and the wall walk on posts
    ic = disa(yol, -r * 1.3, False)
    boru(y, [V(p.x, p.y, z + h * 0.55) for p in ic], 0.005, 'ahsap_koyu', n=4, kapat=True)
    a_, b_ = disa(yol, -r * 1.2, False), disa(yol, -r * 1.2 - 0.045, False)
    zw = z + h * 0.3
    for i in range(len(yol) - 1):
        y.yuz_yon([a_[i] + Z * zw, a_[i + 1] + Z * zw, b_[i + 1] + Z * zw, b_[i] + Z * zw], 'ahsap', Z)
        y.yuz_yon([b_[i] + Z * (zw - 0.008), b_[i + 1] + Z * (zw - 0.008), b_[i + 1] + Z * zw, b_[i] + Z * zw], 'ahsap_koyu',
                  V(-(yol[i + 1] - yol[i]).y, (yol[i + 1] - yol[i]).x))
    for k in range(0, n + 1, 4):
        p, e = at(L * k / n)
        nn = V(-e.y, e.x)
        q = p + nn * (r * 1.2 + 0.04)
        cubuk(y, V(q.x, q.y, z - 0.02), V(q.x, q.y, zw), 0.007, 'ahsap_koyu')


def ahsap_kule(c, w, z0, h, cati_h, ust=0.05, tohum=0, kalkan=True):
    """a timber tower: plank walls with slits, braced posts, an overhanging fighting gallery with openings, a steep
    shingled pyramid roof. Returns the top z"""
    cx, cy = c
    k = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
    zt = z0 + h
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        duz_duvar(y, a, b, z0, zt, 'ahsap_dikey')
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        yarik(y, a + Z * z0 + nn * 0.002, e, nn, w / 2 - 0.005, h * 0.5, 0.01, h * 0.16, 'koyu')
        kutu(y, a + nn * 0.004 + Z * (z0 + h * 0.3), e, w, 0.006, 0.01, 'ahsap_koyu', 'onust')
    for p in k:
        kutu_merkez(y, (p.x, p.y), 0.02, 0.02, h + 0.004, 'kutuk', z0=z0)
    # the gallery
    g = w / 2 + ust
    kg = dikdortgen(cx - g, cx + g, cy - g, cy + g)
    y.yuz_yon([V(p.x, p.y, zt) for p in kg], 'ahsap_koyu', -Z)
    hg = 0.07
    for i in range(4):
        a, b = kg[i], kg[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        duz_duvar(y, a, b, zt, zt + hg, 'ahsap_dikey')
        L = (b - a).length
        for u in (0.22, 0.5, 0.78):   # openings in the gallery wall
            y.pencere(a + e * (L * u - 0.014) + Z * zt, e, nn, 0, hg * 0.4, 0.028, hg * 0.42, 'koyu', kemer=False)
        for j, u in enumerate((0.36, 0.64) if kalkan else ()):   # shields hung between the openings
            sc = a + e * (L * u) + nn * 0.003 + Z * (zt + hg * 0.5)
            ring = [sc + e * (0.0135 * math.cos(TAU * k / 10)) + Z * (0.0135 * math.sin(TAU * k / 10)) for k in range(10)]
            kalkan_disk(ring, sc, nn, KALKAN[(i * 2 + j + tohum) % 4])
        kutu(y, a + nn * 0.003 + Z * zt - e * 0.002, e, L + 0.004, 0.006, 0.012, 'ahsap_koyu', 'onust')
        # braces from the tower wall out to the gallery's corners
        p = k[i]
        d = V(p.x - cx, p.y - cy).normalized()
        cubuk(y, V(p.x, p.y, zt - 0.06), V(p.x, p.y, zt) + d * (ust * 1.35), 0.009, 'ahsap_koyu')
    top = cati_kirma(y, cx - g, cx + g, cy - g, cy + g, zt + hg, cati_h, 0.025, 'sindira', 'ahsap_koyu', dilim=SH, ns=6, nr=6)
    y.prizma(c, 0.004, top - 0.005, top + 0.035, 'ahsap_koyu', n=5)
    kure(y, (cx, cy, top + 0.038), 0.007, 'altin', n=6, kat=3)
    return top


def ejder(p, d, s=1.0, key='ahsap_koyu'):
    """a carved dragon head: a neck curving out (d: outward, horizontal) and up, open jaws, a curled crest"""
    d = V(d[0], d[1]).normalized() * s
    up = Z * s
    neck = [p - d * 0.01, p + d * 0.018 + up * 0.016, p + d * 0.03 + up * 0.042, p + d * 0.026 + up * 0.068]
    boru(y, neck, 0.012 * s, key, n=8, r_son=0.01 * s)
    hp = neck[-1]
    kure(y, hp, 0.012 * s, key, n=8, kat=4)
    boru(y, [hp, hp + d * 0.026 + up * 0.004, hp + d * 0.05 + up * 0.002], 0.009 * s, key, n=6, r_son=0.005 * s)
    boru(y, [hp - up * 0.006, hp + d * 0.02 - up * 0.012, hp + d * 0.04 - up * 0.02], 0.005 * s, key, n=5, r_son=0.003 * s)
    boru(y, [hp - d * 0.006 + up * 0.008, hp - d * 0.018 + up * 0.026, hp - d * 0.034 + up * 0.028, hp - d * 0.038 + up * 0.016],
         0.005 * s, key, n=5, r_son=0.002 * s)
    w = V(-d.y, d.x).normalized()
    for sd in (-1, 1):
        kure(y, hp + d * 0.012 + up * 0.008 + w * (sd * 0.008 * s), 0.0034 * s, 'altin', n=6, kat=3)


KALKAN = ['boya_sari', 'boya_kirmizi', 'beyaz', 'koyu']


def kalkan_disk(ring, c, nn, key, kal=0.003):
    """a round shield hung flat on a wall: its painted face (ring, toward nn), a rim back to the wall, an iron boss"""
    top = [p + nn * kal for p in ring]
    y.yuz_yon(top, key, nn)
    for k in range(len(ring)):
        yuz_dis(y, [ring[k], ring[(k + 1) % len(ring)], top[(k + 1) % len(ring)], top[k]], 'ahsap_koyu', c)
    kure(y, c + nn * kal, 0.0042, 'bronz', n=6, kat=3)


def gemi(konum, aci, L=0.38, W=0.1, H=0.045, yelken=False, cizgi=('boya_kirmizi', 'beyaz')):
    """a Viking longship along its local x (bow at +x) on the water at konum: a clinker hull of strakes, a curled
    stem with a dragon head, a deck, shields along the gunwales, a mast with the yard and the sail (set and striped,
    or furled), a steering oar on the starboard quarter"""
    with parca(y, konum, aci):
        n, m = 14, 4
        T = 0.97
        zk = -0.014
        w = lambda t: W / 2 * max(0.0, 1 - abs(t) ** 2.2) ** 0.6
        zg = lambda t: H + 0.02 * t ** 4
        def P(t, v, s):
            a = v * math.pi / 2
            return V(L / 2 * t, s * w(t) * math.sin(a), zk + (zg(t) - zk) * (1 - math.cos(a)))
        ts = [-T + 2 * T * i / n for i in range(n + 1)]
        for s in (-1, 1):
            for i in range(n):
                for j in range(m):
                    q = [P(ts[i], j / m, s), P(ts[i + 1], j / m, s), P(ts[i + 1], (j + 1) / m, s), P(ts[i], (j + 1) / m, s)]
                    xm = (q[0].x + q[1].x) / 2
                    yuz_dis(y, q, 'ahsap' if j == m - 1 else 'ahsap_koyu', V(xm, 0, H))
            # gunwale top, inner side down to the deck
            zd = H - 0.014
            for i in range(n):
                t0, t1 = ts[i], ts[i + 1]
                g0, g1 = P(t0, 1, s), P(t1, 1, s)
                i0, i1 = V(g0.x, g0.y * 0.86, g0.z), V(g1.x, g1.y * 0.86, g1.z)
                y.yuz_yon([g0, g1, i1, i0], 'ahsap', Z)
                d0, d1 = V(g0.x, g0.y * 0.86, zd), V(g1.x, g1.y * 0.86, zd)
                y.yuz_yon([i0, i1, d1, d0], 'ahsap_koyu', V(0, -s, 0.3))
        y.yuz_yon([V(L / 2 * t, w(t) * 0.86 * s, H - 0.014) for s, tt in ((-1, ts), (1, ts[::-1])) for t in tt], 'ahsap_acik', Z)
        for sx in (-1, 1):   # close the hull ends
            t = T * sx
            sec = [P(t, v / m, -1) for v in range(m + 1)] + [P(t, v / m, 1) for v in range(m, -1, -1)]
            levha([q for k, q in enumerate(sec) if k != m + 1], 'ahsap_koyu', V(sx, 0, 0), 0.003)
        # stem and stern posts curling up, the dragon at the bow, a tail curl at the stern
        for sx in (-1, 1):
            x0 = L / 2 * T * sx
            post = [V(x0 - sx * 0.01, 0, zk + 0.005), V(x0 + sx * 0.012, 0, H * 0.7), V(x0 + sx * 0.024, 0, H + 0.03), V(x0 + sx * 0.022, 0, H + 0.065)]
            boru(y, post, 0.0075, 'ahsap_koyu', n=6, r_son=0.006)
            if sx > 0:
                ejder(post[-1] - Z * 0.004, X, 0.85)
            else:
                boru(y, [post[-1], post[-1] + V(-0.008, 0, 0.022), post[-1] + V(0.006, 0, 0.034), post[-1] + V(0.012, 0, 0.022)], 0.006, 'ahsap_koyu', n=5, r_son=0.003)
        # shields along both gunwales
        for s in (-1, 1):
            nk = 9
            for i in range(nk):
                t = -0.62 + 1.24 * i / (nk - 1)
                p = P(t, 0.96, s) + V(0, s * 0.004, -0.004)
                nn = V(0, s, 0.12).normalized()
                boru(y, [p - nn * 0.003, p], 0.0115, KALKAN[(i + (s > 0)) % len(KALKAN)], n=10)
                kure(y, p + nn * 0.002, 0.0035, 'demir', n=6, kat=3)
        # mast, yard, sail
        zd = H - 0.014
        hm = 0.27
        y.prizma((0.0, 0.0), 0.0055, zd, zd + hm, 'ahsap', n=6)
        ya = zd + hm - 0.02
        cubuk(y, V(0.006, -W * 0.75, ya), V(0.006, W * 0.75, ya), 0.007, 'ahsap_koyu')
        for s in (-1, 1):   # stays
            boru(y, [V(0.0, 0.0, zd + hm - 0.006), V(0.0, s * w(0) * 0.95, H)], 0.0012, 'ahsap_koyu', n=3, kapat=False)
        boru(y, [V(0.0, 0.0, zd + hm - 0.006), V(L / 2 * 0.9, 0, zg(0.9) + 0.01)], 0.0012, 'ahsap_koyu', n=3, kapat=False)
        if yelken:
            ns = 6; hs = 0.17; ws = W * 1.45
            def S(u, v):
                return V(0.012 + 0.028 * math.sin(math.pi * u) * (0.3 + 0.7 * math.sin(math.pi * (1 - v) * 0.5 + 0.3)), -ws / 2 + ws * u, ya - 0.004 - hs * v)
            for i in range(ns):
                for j in range(3):
                    q = [S(i / ns, j / 3), S((i + 1) / ns, j / 3), S((i + 1) / ns, (j + 1) / 3), S(i / ns, (j + 1) / 3)]
                    levha(q, cizgi[i % 2], X, 0.002)
            for s in (-1, 1):   # sheets to the gunwale
                boru(y, [S(0.0 if s < 0 else 1.0, 1.0), P(-0.3, 1, s)], 0.0012, 'ahsap_koyu', n=3, kapat=False)
        else:
            boru(y, [V(0.012, -W * 0.68, ya - 0.008), V(0.012, W * 0.68, ya - 0.008)], 0.009, 'kumas', n=8)
        # steering oar (starboard = right of the bow = -y)
        cubuk(y, V(-L / 2 * 0.78, -w(-0.78) - 0.006, H + 0.02), V(-L / 2 * 0.86, -w(-0.86) - 0.008, -0.02), 0.012, 'ahsap', 0.005)


# ---------------------------------------------------------------- ground and water
y.bolum('Zemin, deniz, iç liman havzası')


def zemin_parca(x0, x1, y0, y1, yan):
    """a block of ground from the bottom to Z0; yan: {side: key} for the side faces ('on' -y, 'arka', 'sol', 'sag')"""
    y.yuz_yon([V(x0, y0, Z0), V(x1, y0, Z0), V(x1, y1, Z0), V(x0, y1, Z0)], 'cimen', Z)
    for s, (a, b) in (('on', (V(x0, y0), V(x1, y0))), ('sag', (V(x1, y0), V(x1, y1))), ('arka', (V(x1, y1), V(x0, y1))), ('sol', (V(x0, y1), V(x0, y0)))):
        if s in yan:
            duz_duvar(y, a, b, 0.0, Z0, yan[s])


zemin_parca(GX0, GX1, BY1, GY1, {'arka': 'toprak', 'sol': 'toprak', 'sag': 'toprak', 'on': 'ahsap_dikey'})
zemin_parca(GX0, -BX, SEA, BY1, {'sol': 'toprak', 'on': 'toprak', 'sag': 'ahsap_dikey'})
zemin_parca(BX, GX1, SEA, BY1, {'sag': 'toprak', 'on': 'toprak', 'sol': 'ahsap_dikey'})
zemin_parca(-BX, -CH, SEA, BY0, {'on': 'toprak', 'arka': 'ahsap_dikey', 'sag': 'granit'})
zemin_parca(CH, BX, SEA, BY0, {'on': 'toprak', 'arka': 'ahsap_dikey', 'sol': 'granit'})
# the water: the sea in front, the channel and the basin (one level)
y.yuz_yon([V(GX0, GY0, ZW), V(GX1, GY0, ZW), V(GX1, SEA, ZW), V(GX0, SEA, ZW)], 'su', Z)
y.yuz_yon([V(-CH, SEA, ZW), V(CH, SEA, ZW), V(CH, BY0, ZW), V(-CH, BY0, ZW)], 'su', Z)
y.yuz_yon([V(-BX, BY0, ZW), V(BX, BY0, ZW), V(BX, BY1, ZW), V(-BX, BY1, ZW)], 'su', Z)
duz_duvar(y, V(GX0, GY0), V(GX1, GY0), 0.0, ZW, 'toprak')
duz_duvar(y, V(GX1, GY0), V(GX1, SEA), 0.0, ZW, 'toprak')
duz_duvar(y, V(GX0, SEA), V(GX0, GY0), 0.0, ZW, 'toprak')
# a pebbly strand along the shore, rocks in the shallows
for k in range(26):
    x = GX0 + 0.06 + k * (GX1 - GX0 - 0.12) / 25
    if abs(x) < CH + 0.04: continue
    kutu_merkez(y, (x, SEA - 0.012 - 0.01 * (k % 3)), 0.05 + 0.02 * (k % 2), 0.03, 0.022 + 0.008 * (k % 3), 'granit' if k % 3 else 'granit_koyu', z0=ZW - 0.012, aci=0.6 * k)

# quays round the basin: plank faces on posts, a deck at the top edge, mooring posts
y.bolum('İç liman: rıhtımlar, iskele')
for a, b in ((V(BX, BY0), V(BX, BY1)), (V(BX, BY1), V(-BX, BY1)), (V(-BX, BY1), V(-BX, BY0)), (V(-BX, BY0), V(-CH, BY0)), (V(CH, BY0), V(BX, BY0))):
    e = (b - a).normalized(); nn = V(-e.y, e.x)    # into the basin (the quay faces the water, to the left of a->b)
    L = (b - a).length
    nk = max(2, int(L / 0.07))
    for j in range(nk + 1):
        p = a.lerp(b, j / nk) + nn * 0.008
        y.prizma((p.x, p.y), 0.009, ZW - 0.01, Z0 + 0.018, 'kutuk', n=6)
    # the deck along the edge
    y.yuz_yon([a + Z * (Z0 + 0.004), b + Z * (Z0 + 0.004), b - nn * 0.05 + Z * (Z0 + 0.004), a - nn * 0.05 + Z * (Z0 + 0.004)], 'ahsap', Z)
    y.yuz_yon([a + Z * Z0, b + Z * Z0, b + Z * (Z0 + 0.004), a + Z * (Z0 + 0.004)], 'ahsap_koyu', nn)
# a jetty into the basin from the back
JX = 0.0
for yy in (BY1 - 0.02, 0.02, -0.12):
    for sx in (-1, 1):
        y.prizma((JX + sx * 0.035, yy), 0.008, ZW - 0.01, Z0 + 0.004, 'kutuk', n=6)
kutu(y, V(JX - 0.045, -0.14, Z0 - 0.004), X, 0.09, BY1 - (-0.14), 0.01, 'ahsap', 'onarkasagsolust')
for (x, yy) in ((JX - 0.045, -0.14), (JX + 0.045, -0.14)):
    y.prizma((x, yy), 0.007, Z0, Z0 + 0.04, 'kutuk', n=6)

# ---------------------------------------------------------------- rampart and palisade
y.bolum('Toprak sur, ahşap palisat')
RC = 0.22
sag = yuvarla([(0.28, RF), (RS, RF), (RS, RB), (0.12, RB)], RC)
sol = yuvarla([(-0.12, RB), (-RS, RB), (-RS, RF), (-0.28, RF)], RC)
for yl in (sag, sol):
    sur_toprak(yl)
    palisad(disa(yl, 0.0, False), ZR, 0.13)

for sx in (-1, 1):   # a shield wall hung on the seaward palisade
    k = 0
    x = 0.36
    while x < RS - 0.26:
        c = V(sx * x, RF - 0.017, ZR + 0.075)
        ring = [c + X * (0.016 * math.cos(TAU * j / 10)) + Z * (0.016 * math.sin(TAU * j / 10)) for j in range(10)]
        kalkan_disk(ring, c, -Y, KALKAN[k % 4], 0.003)
        x += 0.07; k += 1

y.bolum('Sur kuleleri')
for c in ((RS - 0.065, RF + 0.065), (-RS + 0.065, RF + 0.065), (RS, 0.12), (-RS, 0.12), (RS - 0.065, RB - 0.065), (-RS + 0.065, RB - 0.065)):
    kutu_merkez(y, c, 0.15, 0.15, ZR - Z0 + 0.012, 'granit_koyu', z0=Z0 - 0.004)
    silme(y, dikdortgen(c[0] - 0.075, c[0] + 0.075, c[1] - 0.075, c[1] + 0.075), ZR + 0.002, 0.008, 0.006, 'granit', 'duz')
    tp = ahsap_kule(c, 0.13, ZR, 0.25, 0.16, tohum=int(c[0] * 10) % 4)
    if c[1] < 0:   # a gilded weather vane (veðrviti) on the front towers
        y.prizma(c, 0.0035, tp, tp + 0.08, 'ahsap_koyu', n=5)
        vane = [V(c[0] + 0.003, c[1], tp + 0.075)] + [V(c[0] + 0.003 + 0.055 * math.cos(a), c[1], tp + 0.075 - 0.055 * math.sin(a)) for a in [math.pi / 2 * k / 6 for k in range(7)]]
        levha(vane, 'altin', -Y, 0.003)
        boru(y, [V(c[0] + 0.045, c[1], tp + 0.075), V(c[0] + 0.055, c[1], tp + 0.094), V(c[0] + 0.045, c[1], tp + 0.104)], 0.004, 'altin', n=5, r_son=0.0025)

# ---------------------------------------------------------------- the sea gate and its tower
y.bolum('Deniz kapısı: taş kemer')
GW = 0.3            # half width of the gate block
GF, GB = RF - 0.06, BY0      # its front and back
GH = 0.34
kemer_dizisi(y, V(-GW, GF), V(GW, GF), 1, ZW, GH - ZW + Z0 - 0.05, GB - GF, ('tas', 'tas_koyu', 'tas_koyu', 'koyu'), en=0.52,
             ust=0.06, sivri=0.0, acik=True, taban=False)
ZG = Z0 + GH - 0.05
# buttress piers at the front corners, a string course, voussoirs round the arch
for sx in (-1, 1):
    kutu(y, V(GW - 0.06 if sx > 0 else -GW, GF - 0.04, ZW - 0.01), X, 0.06, 0.04, ZG - ZW - 0.03, 'tas_koyu', 'onsagsolust')
silme(y, dikdortgen(-GW, GW, GF, GB), ZG - 0.02, 0.02, 0.012, 'tas_koyu', 'kaba')
R = GW * 0.52
hs = ZG - ZW - 0.06 - R
for k in range(11):   # arch stones standing a little proud of the face
    a0, a1 = math.pi * k / 11, math.pi * (k + 1) / 11
    pts = [V(R * math.cos(a), GF - 0.003, ZW + hs + R * math.sin(a)) for a in (a0, a1)]
    pts2 = [V((R + 0.035) * math.cos(a), GF - 0.003, ZW + hs + (R + 0.035) * math.sin(a)) for a in (a1, a0)]
    y.yuz_yon(pts + pts2, 'tas_acik' if k % 2 else 'tas_koyu', -Y)
kure(y, (0.0, GF - 0.01, ZW + hs + R + 0.02), 0.014, 'tas_koyu', n=8, kat=4)
# the iron grille (portcullis) half raised in the arch
for k in range(1, 9):   # the iron grille (portcullis) half raised in the arch: real bars
    x = -R + 2 * R * k / 9
    ztop = ZW + hs + math.sqrt(max(0.0, R * R - x * x)) - 0.004
    cubuk(y, V(x, GF + 0.02, ZW + hs * 0.5), V(x, GF + 0.02, ztop), 0.007, 'demir')
    donel(y, (x, GF + 0.02), [(0.0, ZW + hs * 0.5 - 0.014), (0.0045, ZW + hs * 0.5)], 'demir', n=4)
for zz in (hs * 0.62, hs * 0.85, hs + R * 0.3, hs + R * 0.6):
    xx = math.sqrt(max(0.0, R * R - max(0.0, zz - hs) ** 2)) - 0.006
    cubuk(y, V(-xx, GF + 0.02, ZW + zz), V(xx, GF + 0.02, ZW + zz), 0.007, 'demir', 0.009)

y.bolum('Deniz kapısı kulesi')
TW, TD = 0.4, 0.24
TCY = (GF + GB) / 2 + 0.01
kt = dikdortgen(-TW / 2, TW / 2, TCY - TD / 2, TCY + TD / 2)
ZT1 = ZG + 0.36
for i in range(4):
    a, b = kt[i], kt[(i + 1) % 4]
    L = (b - a).length
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    duz_duvar(y, a, b, ZG, ZG + 0.1, 'tas')
    nb = 3 if L > 0.3 else 2
    for j in range(nb):
        p, q = a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb)
        y.kemerli(p, q, ZG + 0.1, 0.16, ('tas', 'tas_koyu', 'tas_acik', 'koyu'), v0=0.03, en=0.36, ust=0.03, derin=0.025, k_say=8,
                  cerceve=(0.006, ['tas_acik', 'granit_koyu']))
    duz_duvar(y, a, b, ZG + 0.26, ZT1, 'tas')
    for zz in (ZG + 0.05, ZG + 0.2):
        yarik(y, a + Z * ZG + nn * 0.001, e, nn, L * 0.15, zz - ZG, 0.01, 0.04, 'koyu')
        yarik(y, a + Z * ZG + nn * 0.001, e, nn, L * 0.85 - 0.01, zz - ZG, 0.01, 0.04, 'koyu')
silme(y, kt, ZG + 0.255, 0.012, 0.008, 'tas_acik', 'duz')
for p in kt:   # quoins
    for j in range(6):
        s = 0.03 if j % 2 == 0 else 0.02
        kutu_merkez(y, (p.x, p.y), s, s, 0.05, 'tas_koyu', z0=ZG + 0.005 + j * 0.059)
konsol_halka(y, kt, ZT1 - 0.03, 0.03, 0.015, 'tas', 3)
# the timber gallery (hoarding) overhanging the stone, with braces, openings and shields
OV = 0.055
kg = dikdortgen(-TW / 2 - OV, TW / 2 + OV, TCY - TD / 2 - OV, TCY + TD / 2 + OV)
y.yuz_yon([V(p.x, p.y, ZT1) for p in kg], 'ahsap_koyu', -Z)
HG = 0.11
for i in range(4):
    a, b = kg[i], kg[(i + 1) % 4]
    L = (b - a).length; e = (b - a).normalized(); nn = V(e.y, -e.x)
    duz_duvar(y, a, b, ZT1, ZT1 + HG, 'ahsap_dikey')
    nb = int(L / 0.075)
    for j in range(nb):
        u = (j + 0.5) / nb
        y.pencere(a + e * (L * u - 0.017) + Z * ZT1, e, nn, 0, HG * 0.38, 0.034, HG * 0.45, 'koyu', kemer=False)
        # a shield hung under each opening
        c = a + e * (L * u) + nn * 0.004 + Z * (ZT1 + HG * 0.2)
        ring = [c + e * (0.016 * math.cos(TAU * k / 10)) + Z * (0.016 * math.sin(TAU * k / 10)) for k in range(10)]
        y.yuz_yon(ring, KALKAN[(i + j) % 4], nn)
        kure(y, c + nn * 0.002, 0.004, 'demir', n=6, kat=3)
    kutu(y, a + nn * 0.003 + Z * ZT1 - e * 0.002, e, L + 0.004, 0.007, 0.014, 'ahsap_koyu', 'onust')
    kutu(y, a + nn * 0.003 + Z * (ZT1 + HG - 0.012) - e * 0.002, e, L + 0.004, 0.007, 0.012, 'ahsap_koyu', 'onust')
for p, q in zip(kt, kg):
    cubuk(y, V(p.x, p.y, ZT1 - 0.09), V(q.x, q.y, ZT1 - 0.004), 0.012, 'ahsap_koyu')
ZT2 = ZT1 + HG
tepe = cati_kirma(y, kg[0].x, kg[1].x, kg[0].y, kg[2].y, ZT2, 0.42, 0.04, 'sindira', 'ahsap_koyu', dilim=SH, ns=8, nr=10)
# dragon heads off the roof's hips, a gilded weather vane on the top
for p in kg:
    d = V(p.x, p.y - TCY).normalized()
    ejder(V(p.x, p.y, ZT2 + 0.012) + d * 0.045, d, 0.9)

# ---------------------------------------------------------------- land gate at the back
y.bolum('Kara kapısı')
for sx in (-1, 1):
    kutu_merkez(y, (sx * 0.17, RB), 0.15, 0.15, 0.02, 'granit_koyu', z0=Z0 - 0.004)
    ahsap_kule((sx * 0.17, RB), 0.13, Z0, 0.36, 0.17)
# the bridge between the towers over the passage, with a little gable roof
kutu(y, V(-0.11, RB - 0.06, Z0 + 0.25), X, 0.22, 0.12, 0.012, 'ahsap_koyu', 'onarkasagsolust')
for sy in (-1, 1):
    duz_duvar(y, V(0.11 * sy, RB + sy * 0.06), V(0.11 * -sy, RB + sy * 0.06), Z0 + 0.262, Z0 + 0.33, 'ahsap_dikey')
cati_besik(y, -0.105, 0.105, RB - 0.06, RB + 0.06, Z0 + 0.33, 0.07, 0.02, 'sindira', 'ahsap_koyu', ucluk_key='ahsap_dikey', dilim=SH, nr=5, ns=5)
# the double doors
for sx in (-1, 1):
    levha([V(sx * 0.1, RB + 0.002, Z0), V(0.0, RB + 0.002, Z0), V(0.0, RB + 0.002, Z0 + 0.2), V(sx * 0.1, RB + 0.002, Z0 + 0.2)], 'ahsap_dikey', -Y, 0.004)
    for zz in (0.05, 0.14):
        for yy in (RB - 0.002, RB + 0.003):
            cubuk(y, V(sx * 0.095, yy, Z0 + zz), V(sx * 0.005, yy, Z0 + zz), 0.008, 'demir', 0.004)
y.yuz_yon([V(-0.1, RB + 0.002, Z0 + 0.2), V(0.1, RB + 0.002, Z0 + 0.2), V(0.1, RB + 0.002, Z0 + 0.25), V(-0.1, RB + 0.002, Z0 + 0.25)], 'ahsap_dikey', -Y)
y.yuz_yon([V(0.1, RB + 0.004, Z0 + 0.2), V(-0.1, RB + 0.004, Z0 + 0.2), V(-0.1, RB + 0.004, Z0 + 0.25), V(0.1, RB + 0.004, Z0 + 0.25)], 'ahsap_dikey', Y)

# ---------------------------------------------------------------- inside: longhouses, boardwalks
y.bolum('İç: uzun evler, tahta yollar')
for (cx, cy, aci, ck) in ((-0.72, -0.12, math.pi / 2, 'saz'), (0.72, -0.12, math.pi / 2, 'cimen'), (-0.36, 0.44, 0.0, 'sindira'), (0.36, 0.44, 0.0, 'saz')):
    with parca(y, (cx, cy, Z0), aci):
        uzun_ev(y, 0, 0, 0.44, 0.17, 0.075, 0.14, cati_key=ck, mahya_key='cimen' if ck != 'sindira' else 'ahsap_koyu')
        kutu(y, V(-0.235, -0.1, -0.012), X, 0.47, 0.2, 0.014, 'granit_koyu', 'onarkasagsolust')


def tahta_yol(pts, en=0.06):
    for k in range(len(pts) - 1):
        a, b = V(*pts[k]), V(*pts[k + 1])
        e = (b - a).normalized(); n = V(-e.y, e.x) * (en / 2)
        L = (b - a).length
        m = max(1, int(L / 0.03))
        for j in range(m):   # planks across the way
            p, q = a.lerp(b, j / m), a.lerp(b, (j + 1) / m - 0.15 / m)
            y.yuz_yon([p - n + Z * (Z0 + 0.004), q - n + Z * (Z0 + 0.004), q + n + Z * (Z0 + 0.004), p + n + Z * (Z0 + 0.004)], 'ahsap' if j % 3 else 'ahsap_acik', Z)


tahta_yol([(0.0, RB - 0.05), (0.0, BY1 + 0.05)])
tahta_yol([(-0.62, BY1 + 0.06), (0.62, BY1 + 0.06)])
tahta_yol([(-0.62, -0.38), (-0.62, BY1 + 0.06)])
tahta_yol([(0.62, -0.38), (0.62, BY1 + 0.06)])

# small huts and stacked goods in the corners
for (cx, cy, aci) in ((-0.68, 0.52, 0.3), (0.7, 0.52, -0.3)):
    with parca(y, (cx, cy, Z0), aci):
        duvarlar(y, dikdortgen(-0.06, 0.06, -0.045, 0.045), 0, 0.055, 'ahsap_dikey')
        cati_besik(y, -0.06, 0.06, -0.045, 0.045, 0.055, 0.06, 0.018, 'saz', 'saz_koyu', ucluk_key='ahsap_dikey', ns=4, nr=4)
for k, (x, yy) in enumerate(((0.42, -0.5 + 0.0), (0.5, 0.25), (-0.45, 0.26), (-0.55, 0.26))):
    for j in range(3):
        y.prizma((x + 0.03 * j, yy), 0.014, Z0, Z0 + 0.04, 'ahsap_acik' if j % 2 else 'ahsap', n=8)   # barrels

# ---------------------------------------------------------------- ships
y.bolum('Uzun gemiler')
gemi((-0.27, -0.12, ZW), -math.pi / 2)
gemi((0.27, -0.1, ZW), -math.pi / 2, L=0.36)
gemi((0.68, -0.93, ZW), math.pi + 0.05, yelken=True)
gemi((-0.72, -0.95, ZW), 0.08, L=0.32, W=0.09, yelken=True, cizgi=('boya_sari', 'boya_kirmizi'))

y.bolum('Sancak')
sancak(y, 0.0, TCY, tepe - 0.012, boy=0.2, en=0.15, yuk=0.09, aci=2.6, kuyruk=True)

calistir(y, 'lm_jomsborg')
