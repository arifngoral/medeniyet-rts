# Hedeby (lm_hedeby): the great Viking trading town on the Schlei, inside its semicircular earth rampart (joined to
# the Danevirke) crowned with a palisade and entered by a timber gate: plank-paved streets, a plank-lined brook with
# little bridges, rows of wattle-and-daub houses under thatch, a market of striped stalls by the waterfront, a tall
# timber watchtower with a lookout gallery beside the great hall; jetties, a pile stockade out in the water and moored
# knarrs and longships.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05            # ground top
ZW = 0.02            # water level
ZR = Z0 + 0.12       # rampart crest
SH = ['sindira', 'sindira2']
GX0, GX1, GY0, GY1 = -1.18, 1.18, -1.1, 1.05


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


def ahsap_kule(c, w, z0, h, cati_h, ust=0.05, tohum=0):
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


def gemi(konum, aci, L=0.38, W=0.1, H=0.045, yelken=False, cizgi=('boya_kirmizi', 'beyaz'), kalkan=True, yuk=False):
    """a Viking longship along its local x (bow at +x) on the water at konum: a clinker hull of strakes, a curled
    stem with a dragon head, a deck, shields along the gunwales, a mast with the yard and the sail (set and striped,
    or furled), a steering oar on the starboard quarter; kalkan=False, yuk=True: a broad trading knarr with cargo amidships"""
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
            nk = 9 if kalkan else 0
            for i in range(nk):
                t = -0.62 + 1.24 * i / (nk - 1)
                p = P(t, 0.96, s) + V(0, s * 0.004, -0.004)
                nn = V(0, s, 0.12).normalized()
                boru(y, [p - nn * 0.003, p], 0.0115, KALKAN[(i + (s > 0)) % len(KALKAN)], n=10)
                kure(y, p + nn * 0.002, 0.0035, 'demir', n=6, kat=3)
        if yuk:   # cargo lashed amidships: crates, barrels, bales under a hide
            for i, (x, s_) in enumerate(((-0.07, -1), (-0.05, 1), (0.05, -1), (0.07, 1))):
                kutu_merkez(y, (x, s_ * W * 0.15), 0.035, 0.03, 0.03, 'ahsap_acik' if i % 2 else 'ahsap', z0=H - 0.016, aci=0.1 * i)
            for x in (-0.11, 0.1):
                y.prizma((x, 0.0), 0.014, H - 0.016, H + 0.016, 'ahsap_acik', n=10)
            kutu_merkez(y, (0.0, 0.0), 0.05, W * 0.5, 0.034, 'kerpic_koyu', z0=H - 0.016)
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


def etek_cati(c, h_out, h_in, h_duvar, z0, z1, nr=5, kal=0.012):
    """a skirt (lean-to) roof round a square: its eave h_out from the centre at z0, rising to h_in at z1; a fascia
    and a soffit back to the wall (half size h_duvar) under it; hip caps on the corners"""
    kare = lambda h, z=0.0: dikdortgen(c[0] - h, c[0] + h, c[1] - h, c[1] + h, z)
    out = kare(h_out); inn = kare(h_in)
    rings = [[o.lerp(i, k / nr) + Z * (z0 + (z1 - z0) * k / nr) for o, i in zip(out, inn)] for k in range(nr + 1)]
    for k in range(nr):
        y.serit(rings[k], rings[k + 1], SH[k % 2])
    y.serit([p - Z * kal for p in rings[0]], rings[0], 'ahsap_koyu')
    wall = kare(h_duvar, z0 - kal)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([rings[0][i] - Z * kal, rings[0][j] - Z * kal, wall[j], wall[i]], 'ahsap_koyu', -Z)
    for i in range(4):
        cubuk(y, rings[0][i] + Z * 0.004, rings[-1][i] + Z * 0.004, 0.008, 'ahsap_koyu', 0.006)


def tahta_yol(pts, en=0.07, z=None):
    """a plank-paved street: planks laid across the way on two stringers (Hedeby's timber streets)"""
    z = Z0 + 0.004 if z is None else z
    for k in range(len(pts) - 1):
        a, b = V(*pts[k]), V(*pts[k + 1])
        e = (b - a).normalized(); n = V(-e.y, e.x) * (en / 2)
        L = (b - a).length
        m = max(1, int(L / 0.028))
        for j in range(m):
            p, q = a.lerp(b, j / m), a.lerp(b, (j + 1) / m - 0.18 / m)
            sh = n * (0.06 * ((j * 5) % 3 - 1))
            y.yuz_yon([p - n + sh + Z * z, q - n + sh + Z * z, q + n + sh + Z * z, p + n + sh + Z * z], 'ahsap' if j % 3 else 'ahsap_acik', Z)
        for s in (-1, 1):
            cubuk(y, a + n * s * 0.8 + Z * (z - 0.003), b + n * s * 0.8 + Z * (z - 0.003), 0.008, 'ahsap_koyu', 0.006)


def ev(c, aci, w=0.17, d=0.11, h=0.06, cati='saz', kapi=True, tohum=0):
    """a Hedeby town house: wattle-and-daub walls with slanting outer props, a door in the gable end, a steep
    thatched (or shingled) gable roof"""
    with parca(y, (c[0], c[1], Z0), aci):
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        kutu(y, V(-w / 2 - 0.006, -d / 2 - 0.006, -0.008), X, w + 0.012, d + 0.012, 0.012, 'toprak', 'onarkasagsolust')
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            if i == 1 and kapi:   # the gable end at +x: a door
                dikdortgen_acik(y, a, b, 0.004, h - 0.004, 0.36, 0.64, 0.0, h * 0.8, ('siva_krem', 'ahsap_koyu', 'ahsap', 'ahsap_dikey'), derin=0.008,
                                cerceve=(0.004, 'ahsap_koyu'))
            else:
                duz_duvar(y, a, b, 0.004, h, 'siva_krem')
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            L = (b - a).length
            kutu(y, a + nn * 0.002 + Z * (h - 0.008) - e * 0.003, e, L + 0.006, 0.006, 0.008, 'ahsap_koyu', 'onust')   # wall plate
            if i % 2 == 0:   # props along the long walls
                for j in range(1, 4):
                    p = a.lerp(b, j / 4)
                    cubuk(y, p + nn * 0.02 + Z * 0.004, p + nn * 0.003 + Z * (h - 0.006), 0.007, 'ahsap_koyu', 0.006)
                y.pencere(a + e * (L * 0.5 - 0.01) + Z * 0.0, e, nn, 0, h * 0.45, 0.02, h * 0.28, 'koyu', kemer=False)
        cati_besik(y, -w / 2, w / 2, -d / 2, d / 2, h, h * 1.25, 0.022, cati, 'saz_koyu' if cati == 'saz' else 'ahsap_koyu',
                   ucluk_key='ahsap_dikey', ns=5, nr=5, uc_sacak=0.012)
        # a smoke hole hood on the ridge
        kutu_merkez(y, (w * 0.18, 0), 0.03, 0.02, 0.012, 'ahsap_koyu', z0=h + h * 1.25 - 0.004)


def tezgah(c, aci, renk, mal):
    """a market stall: four posts, a striped cloth awning, a trestle counter with wares"""
    with parca(y, (c[0], c[1], Z0), aci):
        w, d = 0.13, 0.08
        for (x, yy, hh) in ((-w / 2, -d / 2, 0.085), (w / 2, -d / 2, 0.085), (-w / 2, d / 2, 0.105), (w / 2, d / 2, 0.105)):
            kutu_merkez(y, (x, yy), 0.008, 0.008, hh, 'ahsap', z0=0.0)
        ns = 4
        for i in range(ns):
            x0, x1 = -w / 2 - 0.008 + (w + 0.016) * i / ns, -w / 2 - 0.008 + (w + 0.016) * (i + 1) / ns
            q = [V(x0, -d / 2 - 0.025, 0.08), V(x1, -d / 2 - 0.025, 0.08), V(x1, d / 2 + 0.005, 0.108), V(x0, d / 2 + 0.005, 0.108)]
            levha(q, renk if i % 2 == 0 else 'beyaz', V(0, -0.3, 1), 0.0025)
        # a scalloped valance along the front
        for i in range(ns * 2):
            x0, x1 = -w / 2 - 0.008 + (w + 0.016) * i / (ns * 2), -w / 2 - 0.008 + (w + 0.016) * (i + 1) / (ns * 2)
            levha([V(x0, -d / 2 - 0.026, 0.08), V(x1, -d / 2 - 0.026, 0.08), V((x0 + x1) / 2, -d / 2 - 0.026, 0.066)], renk if i % 2 else 'beyaz', -Y, 0.002)
        kutu(y, V(-w / 2 + 0.006, -d / 2 + 0.004, 0.0), X, w - 0.012, 0.035, 0.034, 'ahsap_dikey', 'onarkasagsolust')
        y.yuz_yon([V(-w / 2, -d / 2 - 0.004, 0.034), V(w / 2, -d / 2 - 0.004, 0.034), V(w / 2, -d / 2 + 0.043, 0.034), V(-w / 2, -d / 2 + 0.043, 0.034)], 'ahsap_acik', Z)
        zt = 0.0345
        if mal == 'kup':      # pots and jugs
            for i, x in enumerate((-0.04, -0.012, 0.016, 0.042)):
                donel(y, (x, -d / 2 + 0.018), [(0.0, zt), (0.008, zt + 0.004), (0.011, zt + 0.014), (0.006, zt + 0.024), (0.005, zt + 0.03), (0.0, zt + 0.03)],
                      'kerpic' if i % 2 else 'kerpic_koyu', n=8)
        elif mal == 'kumas':  # bolts of cloth
            for i, (x, r) in enumerate(((-0.035, 'boya_kirmizi'), (-0.008, 'boya_sari'), (0.02, 'boya_yesil'), (0.044, 'lacivert'))):
                boru(y, [V(x, -d / 2 + 0.004, zt + 0.009), V(x, -d / 2 + 0.034, zt + 0.009)], 0.009, r, n=8)
        elif mal == 'kurk':   # furs and amber
            for i, x in enumerate((-0.03, 0.0, 0.03)):
                kutu_merkez(y, (x, -d / 2 + 0.02), 0.026, 0.03, 0.008 + 0.003 * i, 'kerpic_koyu' if i % 2 else 'ahsap_acik', z0=zt, aci=0.2 * i)
            for i in range(5):
                kure(y, (0.035 + 0.006 * (i % 3), -d / 2 + 0.012 + 0.006 * (i // 3), zt + 0.016), 0.0045, 'boya_sari', n=6, kat=3)
        else:                 # barrels and sacks
            for i, x in enumerate((-0.036, -0.006)):
                y.prizma((x, -d / 2 + 0.02), 0.012, zt, zt + 0.026, 'ahsap_acik', n=10)
            for i, x in enumerate((0.022, 0.044)):
                donel(y, (x, -d / 2 + 0.02), [(0.0, zt), (0.012, zt + 0.004), (0.011, zt + 0.018), (0.004, zt + 0.026), (0.0, zt + 0.028)], 'kumas', n=8)


# ---------------------------------------------------------------- ground, harbour, stream
y.bolum('Zemin, liman suyu, dere')
SX0, SX1, SY1 = -0.455, -0.385, 0.3     # the brook (plank-lined) from its spring down to the harbour
SHORE = -0.6


def zemin_parca(x0, x1, y0, y1, yan):
    y.yuz_yon([V(x0, y0, Z0), V(x1, y0, Z0), V(x1, y1, Z0), V(x0, y1, Z0)], 'cimen', Z)
    for s, (a, b) in (('on', (V(x0, y0), V(x1, y0))), ('sag', (V(x1, y0), V(x1, y1))), ('arka', (V(x1, y1), V(x0, y1))), ('sol', (V(x0, y1), V(x0, y0)))):
        if s in yan:
            duz_duvar(y, a, b, 0.0, Z0, yan[s])


zemin_parca(GX0, SX0, SHORE, SY1, {'sol': 'toprak', 'on': 'ahsap_dikey', 'sag': 'ahsap_dikey'})
zemin_parca(SX1, GX1, SHORE, SY1, {'sag': 'toprak', 'on': 'ahsap_dikey', 'sol': 'ahsap_dikey'})
zemin_parca(GX0, GX1, SY1, GY1, {'sol': 'toprak', 'sag': 'toprak', 'arka': 'toprak'})
duz_duvar(y, V(SX0, SY1), V(SX1, SY1), ZW + 0.008, Z0, 'ahsap_dikey')
y.yuz_yon([V(SX0, SHORE, ZW + 0.008), V(SX1, SHORE, ZW + 0.008), V(SX1, SY1, ZW + 0.008), V(SX0, SY1, ZW + 0.008)], 'su', Z)
y.yuz_yon([V(GX0, GY0, ZW), V(GX1, GY0, ZW), V(GX1, SHORE, ZW), V(GX0, SHORE, ZW)], 'su', Z)
duz_duvar(y, V(GX0, GY0), V(GX1, GY0), 0.0, ZW, 'toprak')
duz_duvar(y, V(GX1, GY0), V(GX1, SHORE), 0.0, ZW, 'toprak')
duz_duvar(y, V(GX0, SHORE), V(GX0, GY0), 0.0, ZW, 'toprak')
# the waterfront: a plank quay on posts
for k in range(int((GX1 - GX0) / 0.06) + 1):
    x = GX0 + 0.03 + k * 0.06
    if SX0 - 0.01 < x < SX1 + 0.01 or x > GX1: continue
    y.prizma((x, SHORE - 0.008), 0.008, ZW - 0.01, Z0 + 0.012, 'kutuk', n=6)
# the spring: a small pool lined with stones where the brook rises
for k in range(7):
    a = math.pi * k / 6
    kutu_merkez(y, ((SX0 + SX1) / 2 + 0.055 * math.cos(a), SY1 + 0.02 + 0.03 * math.sin(a)), 0.028, 0.02, 0.014, 'granit' if k % 2 else 'granit_koyu', z0=Z0 - 0.004, aci=a)
# planks lining the brook's banks: posts
for x in (SX0, SX1):
    for k in range(int((SY1 - SHORE) / 0.07)):
        yy = SHORE + 0.035 + k * 0.07
        y.prizma((x + (0.004 if x == SX0 else -0.004), yy), 0.006, ZW, Z0 + 0.01, 'kutuk', n=5)

# ---------------------------------------------------------------- the semicircular rampart (Danevirke)
y.bolum('Yarım daire toprak sur ve palisat')
EC, ERX, ERY = (0.0, SHORE + 0.02), 1.0, 1.44
GAP = 0.11


def yay(a0, a1, n):
    return [V(EC[0] + ERX * math.cos(a0 + (a1 - a0) * k / n), EC[1] + ERY * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]


def kazik_uc(yol, uc):
    """the rampart's end at the shore faced with a revetment of upright logs (the bare earth cut read as a flat
    brown triangle): logs across the end from the outer foot to the inner, each as tall as the bank behind it"""
    prof = [(0.15, Z0 - 0.004), (0.035, ZR), (-0.055, ZR), (-0.17, Z0 - 0.004)]
    e = (yol[0] - yol[1]) if uc == 0 else (yol[-1] - yol[-2]); e.z = 0; e.normalize()
    n = 14
    for k in range(n + 1):
        o = 0.15 - 0.32 * k / n
        z = Z0
        for (o0, z0_), (o1, z1_) in zip(prof, prof[1:]):
            if o1 <= o <= o0:
                z = z0_ + (z1_ - z0_) * (o0 - o) / max(o0 - o1, 1e-9); break
        p = disa(yol, o, False)[uc] + e * 0.01
        hh = z + 0.018 + 0.006 * (k % 2)
        y.prizma((p.x, p.y), 0.0115, ZW - 0.01, hh, 'kutuk', n=6, ust=False)
        y.koni((p.x, p.y), 0.0115, hh, 0.016, 'ahsap', n=6)


ga = math.asin(GAP / ERX)
sag_yay = yay(-0.02, math.pi / 2 - ga, 16)
sol_yay = yay(math.pi / 2 + ga, math.pi + 0.02, 16)
for yl in (sag_yay, sol_yay):
    sur_toprak(yl)
    palisad(yl, ZR, 0.12, tohum=3)
kazik_uc(sag_yay, 0)
kazik_uc(sol_yay, -1)

# the Danevirke running off west from the town rampart
dv = [V(EC[0] + ERX * math.cos(2.45), EC[1] + ERY * math.sin(2.45)), V(-1.02, 0.52), V(-1.17, 0.6)]
sur_toprak(dv)
palisad(dv, ZR, 0.12, tohum=5)

y.bolum('Sur dışı: mezar höyükleri, tarla, ağaçlar')
for (hx, hy, R, H) in ((0.95, 0.72, 0.085, 0.06), (1.07, 0.58, 0.07, 0.05), (0.82, 0.86, 0.065, 0.045), (1.08, 0.86, 0.06, 0.04)):
    donel(y, (hx, hy), [(R * 1.05, Z0 - 0.003), (R, Z0 + H * 0.2), (R * 0.78, Z0 + H * 0.62), (R * 0.42, Z0 + H * 0.92), (0.0, Z0 + H)], 'cimen', n=16)
for k in range(6):   # a little stone ship among the graves
    t = TAU * k / 6
    kutu_merkez(y, (0.93 + 0.03 * math.sin(t), 0.45 + 0.07 * math.cos(t)), 0.016, 0.012, 0.022, 'granit', z0=Z0 - 0.003, aci=t)
# a ploughed field (furrows) in the back-left corner
for k in range(7):
    y0_ = 0.66 + k * 0.045
    y.yuz_yon([V(-1.12, y0_, Z0 + 0.002), V(-0.62, y0_, Z0 + 0.002), V(-0.62, y0_ + 0.026, Z0 + 0.002), V(-1.12, y0_ + 0.026, Z0 + 0.002)], 'toprak', Z)


def cam(x, yy, boy):
    r = boy * 0.3
    y.prizma((x, yy), 0.007, Z0 - 0.004, Z0 + boy * 0.25, 'ahsap_koyu', n=5)
    for k in range(3):
        z = Z0 + boy * (0.14 + 0.26 * k)
        rr = r * (1 - 0.24 * k)
        donel(y, (x, yy), [(rr * 0.35, z), (rr, z + 0.012), (rr * 0.45, z + boy * 0.3), (0.0, z + boy * (0.42 if k == 2 else 0.34))], 'yesil_koyu', n=10)
        y.yuz_yon([V(p.x, p.y, z) for p in cokgen((x, yy), rr * 0.35, 10)], 'yesil_koyu', -Z)


for (tx, ty, tb) in ((-1.08, 0.22, 0.24), (1.08, 0.25, 0.25), (1.07, 0.44, 0.2), (0.55, 0.92, 0.24), (-0.42, 0.93, 0.22), (0.3, 0.98, 0.2)):
    cam(tx, ty, tb)

y.bolum('Kuzey kapısı')
GY = EC[1] + ERY
for sx in (-1, 1):
    ahsap_kule((sx * (GAP + 0.07), GY - 0.005), 0.13, Z0, 0.3, 0.15)
kutu(y, V(-GAP - 0.01, GY - 0.065, Z0 + 0.22), X, 2 * GAP + 0.02, 0.12, 0.012, 'ahsap_koyu', 'onarkasagsolust')
for sy in (-1, 1):
    duz_duvar(y, V(GAP * sy, GY + sy * 0.055), V(-GAP * sy, GY + sy * 0.055), Z0 + 0.232, Z0 + 0.29, 'ahsap_dikey')
cati_besik(y, -GAP + 0.005, GAP - 0.005, GY - 0.055, GY + 0.055, Z0 + 0.29, 0.06, 0.02, 'sindira', 'ahsap_koyu', ucluk_key='ahsap_dikey', dilim=SH, nr=5, ns=5)
tahta_yol([(0.0, GY + 0.16), (0.0, GY - 0.1)], 0.09)

# ---------------------------------------------------------------- streets
y.bolum('Tahta yollar ve dere köprüleri')
tahta_yol([(0.0, GY - 0.1), (0.0, SHORE + 0.02)], 0.09)
YC = (0.32, -0.16)
for yc in YC:
    xm = ERX * math.sqrt(max(0.0, 1 - ((yc - EC[1]) / ERY) ** 2)) - 0.2
    tahta_yol([(-xm, yc), (SX0 - 0.01, yc)], 0.075)
    tahta_yol([(SX1 + 0.01, yc), (xm, yc)], 0.075)
    if yc < SY1:   # a little bridge over the brook
        kutu(y, V(SX0 - 0.012, yc - 0.045, Z0 - 0.002), X, SX1 - SX0 + 0.024, 0.09, 0.01, 'ahsap', 'onarkasagsolust')
        for s in (-1, 1):
            boru(y, [V(SX0 - 0.012, yc + s * 0.045, Z0 + 0.03), V(SX1 + 0.012, yc + s * 0.045, Z0 + 0.03)], 0.003, 'ahsap_koyu', n=4)
            for x in (SX0 - 0.01, SX1 + 0.01):
                cubuk(y, V(x, yc + s * 0.045, Z0), V(x, yc + s * 0.045, Z0 + 0.03), 0.006, 'ahsap_koyu')
    else:
        tahta_yol([(SX0 - 0.01, yc), (SX1 + 0.01, yc)], 0.075)
# the street along the brook
tahta_yol([((SX0 + SX1) / 2 + 0.07, SY1 - 0.02), ((SX0 + SX1) / 2 + 0.07, SHORE + 0.03)], 0.05)

# ---------------------------------------------------------------- the watchtower and the great hall
y.bolum('Gözcü kulesi')
TC = (0.2, 0.08)
kutu_merkez(y, TC, 0.27, 0.27, 0.03, 'granit', z0=Z0 - 0.006)
H1 = 0.12
k1 = dikdortgen(TC[0] - H1, TC[0] + H1, TC[1] - H1, TC[1] + H1)
Z1 = Z0 + 0.024
Z2 = Z1 + 0.28
for i in range(4):
    a, b = k1[i], k1[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    if i == 3:
        dikdortgen_acik(y, a, b, Z1, Z2 - Z1, 0.36, 0.64, 0.0, 0.15, ('ahsap_dikey', 'ahsap_koyu', 'ahsap', 'ahsap_koyu'), derin=0.015, cerceve=(0.008, 'ahsap_koyu'))
    else:
        duz_duvar(y, a, b, Z1, Z2, 'ahsap_dikey')
        yarik(y, a + Z * Z1 + nn * 0.002, e, nn, 2 * H1 * 0.5 - 0.005, 0.15, 0.01, 0.05, 'koyu')
    for zz in (Z1 + 0.09, Z1 + 0.19):
        kutu(y, a + nn * 0.004 + Z * zz - e * 0.004, e, 2 * H1 + 0.008, 0.007, 0.012, 'ahsap_koyu', 'onust')
    cubuk(y, a + nn * 0.004 + Z * Z1, a.lerp(b, 0.5) + nn * 0.004 + Z * (Z1 + 0.09), 0.008, 'ahsap_koyu', 0.005)
    cubuk(y, b + nn * 0.004 + Z * Z1, a.lerp(b, 0.5) + nn * 0.004 + Z * (Z1 + 0.09), 0.008, 'ahsap_koyu', 0.005)
for p in k1:
    kutu_merkez(y, (p.x, p.y), 0.026, 0.026, Z2 - Z1 + 0.004, 'kutuk', z0=Z1)
# a stair up to the door
merdiven(y, (TC[0] - H1 - 0.11, TC[1]), 0.0, 0.07, Z0, Z1 + 0.0, n=3, d=0.03, key='ahsap')
etek_cati(TC, H1 + 0.055, H1 - 0.03, H1, Z2, Z2 + 0.06)
H2 = H1 - 0.03
Z3 = Z2 + 0.05
Z4 = Z3 + 0.24
k2 = dikdortgen(TC[0] - H2, TC[0] + H2, TC[1] - H2, TC[1] + H2)
for i in range(4):
    a, b = k2[i], k2[(i + 1) % 4]
    for j in range(2):
        p, q = a.lerp(b, j / 2), a.lerp(b, (j + 1) / 2)
        y.kemerli(p, q, Z3, Z4 - Z3, ('ahsap_dikey', 'ahsap_koyu', 'ahsap_acik', 'koyu'), v0=0.1, en=0.42, ust=0.04, derin=0.02, k_say=6,
                  cerceve=(0.005, 'ahsap_acik'))
for p in k2:
    kutu_merkez(y, (p.x, p.y), 0.022, 0.022, Z4 - Z3, 'kutuk', z0=Z3)
# the lookout gallery, overhanging on braces, its rail hung with shields
OV = 0.05
g = H2 + OV
kg = dikdortgen(TC[0] - g, TC[0] + g, TC[1] - g, TC[1] + g)
y.yuz_yon([V(p.x, p.y, Z4) for p in kg], 'ahsap_koyu', -Z)
HG = 0.085
for i in range(4):
    a, b = kg[i], kg[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    duz_duvar(y, a, b, Z4, Z4 + HG, 'ahsap_dikey')
    for j in range(4):
        u = (j + 0.5) / 4
        y.pencere(a + e * (L * u - 0.014) + Z * Z4, e, nn, 0, HG * 0.4, 0.028, HG * 0.45, 'koyu', kemer=False)
    for j in range(3):
        cc = a + e * (L * (j + 1) / 4) + nn * 0.002 + Z * (Z4 + HG * 0.24)
        boru(y, [cc, cc + nn * 0.004], 0.015, KALKAN[(i + j) % 4], n=10)
    kutu(y, a + nn * 0.003 + Z * Z4 - e * 0.002, e, L + 0.004, 0.007, 0.012, 'ahsap_koyu', 'onust')
for p, q in zip(k2, kg):
    cubuk(y, V(p.x, p.y, Z4 - 0.08), V(q.x, q.y, Z4 - 0.004), 0.011, 'ahsap_koyu')
Z5 = Z4 + HG
tepe = cati_kirma(y, kg[0].x, kg[1].x, kg[0].y, kg[2].y, Z5, 0.3, 0.035, 'sindira', 'ahsap_koyu', dilim=SH, ns=6, nr=8)
for p in kg:
    d = V(p.x - TC[0], p.y - TC[1]).normalized()
    ejder(V(p.x, p.y, Z5 + 0.012) + d * 0.04, d, 0.85)
sancak(y, TC[0], TC[1], tepe - 0.012, boy=0.22, en=0.15, yuk=0.09, aci=2.4, kuyruk=True)

y.bolum('Büyük salon')
with parca(y, (0.57, 0.1, Z0), math.pi / 2):
    kutu(y, V(-0.24, -0.13, -0.01), X, 0.48, 0.26, 0.016, 'granit_koyu', 'onarkasagsolust')
    uzun_ev(y, 0, 0, 0.42, 0.22, 0.095, 0.2, cati_key='sindira', mahya_key='ahsap_koyu', bombe=0.14)

# ---------------------------------------------------------------- houses
y.bolum('Kasaba evleri')
EV = []
for j in range(12):
    yy = -0.47 + 0.135 * j
    for i in range(15):
        x = -1.05 + 0.16 * i + (0.06 if j % 2 else 0.0)
        cx = x + 0.012 * ((i * 3 + j * 5) % 3 - 1)
        cy = yy + 0.01 * ((i + j) % 3 - 1)
        # inside the rampart's inner foot, clear of the streets, the brook, the tower and the hall, the market
        if ((cx - EC[0]) / (ERX - 0.22)) ** 2 + ((cy - EC[1]) / (ERY - 0.21)) ** 2 > 1: continue
        if abs(cx) < 0.12: continue
        if SX0 - 0.1 < cx < SX1 + 0.12: continue
        if abs(cy - YC[0]) < 0.075 or abs(cy - YC[1]) < 0.075: continue
        if 0.0 < cx < 0.4 and -0.1 < cy < 0.26: continue
        if 0.42 < cx < 0.72 and -0.13 < cy < 0.33: continue
        if cx > 0.06 and cy < -0.25: continue
        EV.append((cx, cy, (math.pi if (i + j) % 2 else 0.0)))
CATI = ['saz', 'saz', 'sindira', 'saz', 'saz_koyu']
for k, (cx, cy, a) in enumerate(EV):
    ev((cx, cy), a + 0.05 * ((k % 3) - 1), w=0.145 - 0.015 * (k % 2), d=0.098, h=0.055 + 0.008 * (k % 3), cati=CATI[k % len(CATI)])

# wattle fences round a few yards, wells, woodpiles
for (cx, cy) in ((-0.74, 0.6), (-0.15, -0.36), (0.74, 0.62)):
    for i in range(10):
        a = TAU * i / 10
        p = V(cx + 0.05 * math.cos(a), cy + 0.05 * math.sin(a))
        y.prizma((p.x, p.y), 0.004, Z0, Z0 + 0.03, 'ahsap_koyu', n=4)
    boru(y, [V(cx + 0.05 * math.cos(TAU * i / 10), cy + 0.05 * math.sin(TAU * i / 10), Z0 + 0.022) for i in range(11)], 0.004, 'ahsap', n=4, kapat=False)

y.bolum('Pazar tezgâhları')
RENK = ['boya_kirmizi', 'boya_sari', 'boya_yesil', 'lacivert', 'boya_kirmizi', 'boya_sari', 'boya_yesil', 'lacivert']
MAL = ['kup', 'kumas', 'kurk', 'fici']
k = 0
for yy in (-0.31, -0.47):
    for x in (0.2, 0.37, 0.54, 0.71):
        if ((x - EC[0]) / (ERX - 0.2)) ** 2 + ((yy - EC[1]) / (ERY - 0.2)) ** 2 > 1: continue
        tezgah((x, yy), math.pi if yy > -0.4 else 0.0, RENK[k % len(RENK)], MAL[k % 4]); k += 1
# a pile of crates and barrels by the quay
for i, (x, yy) in enumerate(((0.12, -0.53), (0.15, -0.55), (0.13, -0.5), (-0.13, -0.52), (-0.16, -0.54))):
    if i < 3: kutu_merkez(y, (x, yy), 0.035, 0.035, 0.03 + 0.01 * (i % 2), 'ahsap_acik' if i % 2 else 'ahsap', z0=Z0, aci=0.3 * i)
    else: y.prizma((x, yy), 0.016, Z0, Z0 + 0.034, 'ahsap_acik', n=10)

# ---------------------------------------------------------------- harbour: jetties, stockade, ships
y.bolum('Liman: iskeleler, kazıklı dalgakıran, gemiler')
for jx, L in ((0.0, 0.3), (-0.72, 0.24), (0.62, 0.26)):
    for yy in [SHORE - 0.02 - 0.07 * k for k in range(int(L / 0.07) + 1)]:
        for s in (-1, 1):
            y.prizma((jx + s * 0.038, yy), 0.008, ZW - 0.01, Z0 + 0.004, 'kutuk', n=6)
    kutu(y, V(jx - 0.048, SHORE - L - 0.01, Z0 - 0.004), X, 0.096, L + 0.012, 0.01, 'ahsap', 'onarkasagsolust')
    for s in (-1, 1):
        y.prizma((jx + s * 0.048, SHORE - L), 0.007, Z0, Z0 + 0.035, 'kutuk', n=6)
# the stockade of piles out in the water, in an arc with a gap for the ships
for k in range(60):
    t = k / 59
    x = GX0 + 0.08 + (GX1 - GX0 - 0.16) * t
    if abs(x - 0.28) < 0.14: continue
    yy = GY0 + 0.07 + 0.09 * (1 - (2 * t - 1) ** 2)
    for j in range(2):
        y.prizma((x + 0.01 * j, yy + 0.022 * j), 0.0085, ZW - 0.01, ZW + 0.05 + 0.012 * ((k + j) % 3), 'kutuk', n=6)
        y.koni((x + 0.01 * j, yy + 0.022 * j), 0.0085, ZW + 0.05 + 0.012 * ((k + j) % 3), 0.012, 'ahsap', n=6)
gemi((0.19, SHORE - 0.21, ZW), math.pi / 2 + 0.03, L=0.34, W=0.14, H=0.055, kalkan=False, yuk=True)
gemi((-0.18, SHORE - 0.2, ZW), -math.pi / 2 + 0.05, L=0.36, W=0.1)
gemi((-0.95, SHORE - 0.23, ZW), math.pi / 2, L=0.32, W=0.13, H=0.055, kalkan=False, yuk=True)
gemi((0.72, GY0 + 0.27, ZW), math.pi + 0.15, L=0.36, W=0.1, yelken=True, cizgi=('boya_kirmizi', 'beyaz'))

calistir(y, 'lm_hedeby')
