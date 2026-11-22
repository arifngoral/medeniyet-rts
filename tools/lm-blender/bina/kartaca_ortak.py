# Shared helpers for the Carthaginian landmarks lm_kothon, lm_paraliasker, lm_byrsa, lm_filahirlari (not a building:
# imported by those scripts). Punic details on top of parcalar.py: the Egyptianising cavetto cornice, the sign of Tanit
# (wall relief and free-standing finial), a light Ionic column for long colonnades, whitewashed flat-roofed houses,
# a Punic warship hull (bronze ram, painted eye) that can be tilted onto a slipway, and placing / tilting helpers.
import math, random
from mathutils import Vector
from parcalar import *

# cavetto cornice (Egyptian gorge, used all over Punic architecture): a torus roll, the hollow flaring out, a flat band
KAVETTO = [(0, 0), (0.16, 0.03), (0.2, 0.1), (0.12, 0.17), (0.04, 0.19), (0.07, 0.36), (0.18, 0.56), (0.4, 0.75),
           (0.72, 0.88), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]
# a lighter cavetto (fewer profile points) for long runs of wall
KAVETTO_H = [(0, 0), (0.18, 0.1), (0.05, 0.2), (0.12, 0.5), (0.45, 0.78), (1.0, 0.94), (1.0, 1.0), (0, 1.0)]
SIVA = ('siva', 'siva_krem', 'siva', 'koyu')          # whitewashed wall, reveal, sill, dark back


def kavetto(y, kose, z, h, c, key='siva', kapali=True, ust=True):
    """a cavetto cornice on a wall polygon kose (z: its foot), its top capped (ust, closed polygons only)"""
    silme(y, kose, z, h, c, key, KAVETTO, kapali)
    if ust and kapali:
        y.yuz_yon([V(p.x, p.y, z + h) for p in kose], key, Z)


class egimli:
    """with egimli(y, konum, aci, egim): faces added inside are built round the origin (x forward, z up), then pitched
    by egim about the local y axis (positive: the +x end rises), turned by aci about z and moved to konum"""

    def __init__(self, y, konum=(0, 0, 0), aci=0.0, egim=0.0):
        self.y, self.k, self.a, self.e = y, Vector(konum), aci, egim

    def __enter__(self):
        self.bas = len(self.y.faces)
        return self

    def __exit__(self, *e):
        ca, sa, ce, se, k = math.cos(self.a), math.sin(self.a), math.cos(self.e), math.sin(self.e), self.k
        for i in range(self.bas, len(self.y.faces)):
            pts, key = self.y.faces[i]
            out = []
            for p in pts:
                x, yy, z = p[0] * ce - p[2] * se, p[1], p[0] * se + p[2] * ce
                out.append((k.x + ca * x - sa * yy, k.y + sa * x + ca * yy, k.z + z))
            self.y.faces[i] = (out, key)
        return False


def prizma2(y, pts, P, d, key, n_yon, arka=False):
    """a thin slab: the 2D outline pts (u, v; CCW seen from the front) mapped by P(u, v, d) onto a wall, its front d
    proud of the wall and its edges back to the wall (arka: the back face too, for a free-standing piece)"""
    on = [P(u, v, d) for u, v in pts]
    geri = [P(u, v, 0) for u, v in pts]
    y.yuz_yon(on, key, n_yon)
    m = len(pts)
    c = sum(on, Vector()) / m
    for i in range(m):
        j = (i + 1) % m
        q = [on[i], on[j], geri[j], geri[i]]
        mid = (on[i] + on[j]) / 2
        yon = mid - c
        yon = yon - Vector(n_yon).normalized() * yon.dot(Vector(n_yon).normalized())
        y.yuz_yon(q, key, yon)
    if arka:
        y.yuz_yon(geri, key, -Vector(n_yon))


def tanit_sekli(s):
    """the sign of Tanit as convex 2D pieces (u across, v up, base centre at 0, s tall): the triangular body, the
    arm bar with raised hands, the disc head"""
    govde = [(-0.3 * s, 0), (0.3 * s, 0), (0.06 * s, 0.55 * s), (-0.06 * s, 0.55 * s)]
    kol = [(-0.36 * s, 0.53 * s), (0.36 * s, 0.53 * s), (0.36 * s, 0.6 * s), (-0.36 * s, 0.6 * s)]
    eller = [[(-0.36 * s, 0.53 * s), (-0.29 * s, 0.53 * s), (-0.29 * s, 0.7 * s), (-0.36 * s, 0.7 * s)],
             [(0.29 * s, 0.53 * s), (0.36 * s, 0.53 * s), (0.36 * s, 0.7 * s), (0.29 * s, 0.7 * s)]]
    bas = [(0.16 * s * math.cos(TAU * k / 12), 0.78 * s + 0.16 * s * math.sin(TAU * k / 12)) for k in range(12)]
    return [govde, kol] + eller + [bas]


def tanit_kabartma(y, o, ex, nrm, s, key='altin', d=0.003):
    """the sign of Tanit in low relief on a wall: o the base centre on the wall, ex along the wall, nrm out of it"""
    o, ex, nrm = Vector(o), Vector(ex).normalized(), Vector(nrm).normalized()
    P = lambda u, v, dd: o + ex * u + Z * v + nrm * dd
    for i, pc in enumerate(tanit_sekli(s)):
        prizma2(y, pc, P, d + 0.0004 * (i % 2), key, nrm)


def tanit_heykel(y, x, yy, z, s, key='bronz', aci=0.0, kalin=None):
    """a free-standing sign of Tanit (a finial, a stele top): the pieces as slabs kalin thick, facing aci"""
    e = V(math.cos(aci), math.sin(aci)); ex = V(-e.y, e.x)
    k = kalin or s * 0.09
    o = V(x, yy, z) - e * (k / 2)
    P = lambda u, v, dd: o + ex * u + Z * v + e * dd
    for pc in tanit_sekli(s):
        prizma2(y, pc, P, k, key, e, arka=True)


def iyon_hafif(y, cx, cy, z0, z1, r, key='siva', bas_key=None, n=8, aci=0.0):
    """a light Ionic column for long colonnades (~90 triangles): a moulded base, a tapering shaft, an echinus, a volute
    block with two rolls (their eyes facing aci and back), a thin abacus"""
    bk = bas_key or key
    H = z1 - z0
    hb, hc = H * 0.06, H * 0.11
    donel(y, (cx, cy), [(r * 1.45, z0), (r * 1.4, z0 + hb * 0.6), (r, z0 + hb)], bk, n=n)
    donel(y, (cx, cy), [(r, z0 + hb), (r * 0.86, z1 - hc), (r * 1.08, z1 - hc * 0.62), (0.0, z1 - hc * 0.62)], key, n=n)
    e = V(math.cos(aci), math.sin(aci)); s = V(-e.y, e.x)
    zv = z1 - hc * 0.62
    kutu_merkez(y, (cx, cy), r * 2.5, r * 1.5, hc * 0.38, bk, z0=zv, aci=math.atan2(s.y, s.x), yuzler='onarkasagsolust')
    for sg in (-1, 1):
        c = V(cx, cy) + s * (sg * r * 1.25)
        boru(y, [c - e * (r * 0.8) + Z * (zv + hc * 0.12), c + e * (r * 0.8) + Z * (zv + hc * 0.12)], r * 0.36, bk, n=5)
    kutu_merkez(y, (cx, cy), r * 2.6, r * 2.6, hc * 0.24, bk, z0=z1 - hc * 0.24, aci=aci)
    return z1


def pencere_kutu(y, o, ex, nrm, u, v, w, h, key='koyu', cerceve=None, d=0.0012):
    """a small dark window block standing a hair proud of a wall (o on the wall at its base line, ex along, nrm out);
    cerceve: a key for a raised sill and lintel"""
    o, ex, nrm = Vector(o), Vector(ex).normalized(), Vector(nrm).normalized()
    if ex.cross(Z).dot(nrm) < 0:
        o = o + ex * (2 * u + w); ex = -ex
    kutu(y, o + ex * u + nrm * d + Z * v, ex, w, 0.006, h, key, 'onsagsolust')
    if cerceve:
        kutu(y, o + ex * (u - w * 0.15) + nrm * (d + 0.0025) + Z * (v - 0.004), ex, w * 1.3, 0.0062, 0.004, cerceve, 'onsagsolust')
        kutu(y, o + ex * (u - w * 0.15) + nrm * (d + 0.0025) + Z * (v + h), ex, w * 1.3, 0.0062, 0.005, cerceve, 'onsagsolust')


def pon_ev(y, cx, cy, z, w, d, h, aci=0.0, ust=None, tohum=0, duvar='siva', kenar='siva_krem', kapi=True, pencere=True,
           kat2=True, katlar=1):
    """a whitewashed Punic town house (katlar: storeys, a row of windows and a thin band each): a flat-roofed block with a low parapet, small dark windows high up, a door (on
    the -y side before turning by aci), and (kat2, by chance) an upper room set back on the roof with its own parapet
    and a roof-terrace awning. ust: the roof terrace's key"""
    g = random.Random(tohum)
    with parca(y, (cx, cy, z), aci):
        kutu(y, V(-w / 2, -d / 2, 0), X, w, d, h, duvar, 'onarkasagsol')
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        y.yuz_yon([V(p.x, p.y, h) for p in k], ust or 'siva_krem', Z)
        duvarlar(y, k, h, h + 0.009, duvar, ust=kenar, kalinlik=0.005)
        if pencere:
            for side in range(4):
                a, b = k[side], k[(side + 1) % 4]
                L = (b - a).length
                ex = (b - a) / L; nrm = V(ex.y, -ex.x)
                m = max(1, int(L / 0.055))
                for i in range(m):
                    if side == 0 and kapi and i == m // 2: continue
                    if g.random() < 0.45: continue
                    u = L * (i + 0.5) / m - 0.006
                    for r_ in range(katlar):
                        pencere_kutu(y, a, ex, nrm, u, h * (r_ + 0.62) / katlar, 0.012, min(0.018, h * 0.22 / katlar), 'koyu')
        for r_ in range(1, katlar):
            silme(y, k, h * r_ / katlar - 0.002, 0.004, 0.0025, kenar, 'duz')
        if kapi:
            a, b = k[0], k[1]
            pencere_kutu(y, a, X, -Y, w / 2 - 0.011, 0.0, 0.022, min(0.04, h * 0.55), 'ahsap_koyu', cerceve='kum_acik')
        if kat2 and g.random() < 0.6 and w > 0.06 and d > 0.06:
            w2, d2, h2 = w * g.uniform(0.4, 0.55), d * g.uniform(0.45, 0.6), h * g.uniform(0.45, 0.65)
            sx = g.choice((-1, 1))
            x0 = sx * (w / 2 - w2 / 2 - 0.006) - w2 / 2
            y0 = d / 2 - d2 - 0.006
            kutu(y, V(x0, y0, h), X, w2, d2, h2, duvar, 'onarkasagsol')
            k2 = dikdortgen(x0, x0 + w2, y0, y0 + d2)
            y.yuz_yon([V(p.x, p.y, h + h2) for p in k2], ust or 'siva_krem', Z)
            duvarlar(y, k2, h + h2, h + h2 + 0.007, duvar, ust=kenar, kalinlik=0.004)
            pencere_kutu(y, V(x0, y0), X, -Y, w2 / 2 - 0.007, h + h2 * 0.25, 0.014, h2 * 0.5, 'koyu')
            if g.random() < 0.5:   # an awning of reed mats on poles over the rest of the terrace
                xa0, xa1 = (-w / 2 + 0.008, x0 - 0.004) if sx > 0 else (x0 + w2 + 0.004, w / 2 - 0.008)
                if xa1 - xa0 > 0.03:
                    za = h + h2 * 0.8
                    for px in (xa0 + 0.004, xa1 - 0.004):
                        for py in (y0 + 0.004, d / 2 - 0.01):
                            y.prizma((px, py), 0.0018, h, za, 'ahsap', n=4, ust=False)
                    kutu(y, V(xa0, y0, za), X, xa1 - xa0, d / 2 - 0.006 - y0, 0.003, 'saz', 'onarkasagsolust')
                    y.yuz_yon([V(xa0, y0, za), V(xa1, y0, za), V(xa1, d / 2 - 0.006, za), V(xa0, d / 2 - 0.006, za)], 'saz', -Z)


def gemi(y, konum, aci, egim=0.0, L=0.3, B=0.05, H=0.028, kurek=True, yelken=False, tur='savas', tohum=1, ic_key='ahsap_acik', kaba=False):
    """a Punic ship, its waterline through konum, heading aci, pitched egim (bow up positive): a lofted hull (dark
    wood, a red wale, a painted eye), a bronze ram and a curling stern post (savas: a warship) or a round merchant
    hull with a horse-head prow (ticaret, a hippos / gaulos), oars in two banks, a mast with a striped sail. kaba: a
    cheap hull for a ship mostly hidden in a shed (fewer stations, no inner bulwark, no stern post)"""
    g = random.Random(tohum)
    with egimli(y, konum, aci, egim):
        n = 6 if kaba else 10
        st = []
        for i in range(n + 1):
            t = i / n
            x = -L / 2 + L * t
            if tur == 'savas':
                w = B / 2 * max(0.12, math.sin(math.pi * min(1, max(0, (t - 0.02) / 0.96))) ** 0.55)
                h = H + (0.03 * ((0.18 - t) / 0.18) ** 2 if t < 0.18 else 0) + (0.01 * ((t - 0.85) / 0.15) if t > 0.85 else 0)
            else:
                w = B / 2 * max(0.2, math.sin(math.pi * t) ** 0.4)
                h = H + 0.016 * (abs(t - 0.5) * 2) ** 3
            st.append((x, w, h))
        kz = -0.012
        for i in range(n):
            (x0, w0, h0), (x1, w1, h1) = st[i], st[i + 1]
            for s in (-1, 1):
                pk0, pk1 = V(x0, 0, kz), V(x1, 0, kz)
                m0, m1 = V(x0, s * w0, h0 * 0.45), V(x1, s * w1, h1 * 0.45)
                r0, r1 = V(x0, s * w0 * 1.02, h0 * 0.62), V(x1, s * w1 * 1.02, h1 * 0.62)
                g0, g1 = V(x0, s * w0, h0), V(x1, s * w1, h1)
                for (a0, a1, b1, b0), key in (((pk0, pk1, m1, m0), 'ahsap_koyu'), ((m0, m1, r1, r0), 'boya_kirmizi' if tur == 'savas' else 'siva_oker'),
                                              ((r0, r1, g1, g0), 'ahsap')):
                    y.yuz_yon([a0, a1, b1, b0], key, V(0, s, 0.2))
            dk = 1.0 if kaba else 0.92   # (no inner bulwark on a cheap hull: the deck at the gunwale)
            y.yuz_yon([V(x0, -w0, h0 * dk), V(x1, -w1, h1 * dk), V(x1, w1, h1 * dk), V(x0, w0, h0 * dk)], ic_key, Z)
            for s in (-1, 1) if not kaba else ():
                y.yuz_yon([V(x0, s * w0, h0 * 0.92), V(x1, s * w1, h1 * 0.92), V(x1, s * w1, h1), V(x0, s * w0, h0)], 'ahsap', V(0, -s, 0))
                y.yuz_yon([V(x0, s * w0, h0), V(x1, s * w1, h1), V(x1, s * w1 * 0.97, h1 + 0.0001), V(x0, s * w0 * 0.97, h0 + 0.0001)], 'ahsap', Z)
        for i, sg in ((0, -1), (n, 1)):
            x, w, h = st[i]
            y.yuz_yon([V(x, -w, h), V(x, -w * 1.02, h * 0.62), V(x, -w, h * 0.45), V(x, 0, kz), V(x, w, h * 0.45),
                       V(x, w * 1.02, h * 0.62), V(x, w, h)], 'ahsap_koyu', V(sg, 0, 0))
        xb, wb, hb = st[-1]
        x0, w0, h0 = st[0]
        if tur == 'savas':
            boru(y, [V(xb - 0.008, 0, -0.002), V(xb + 0.03, 0, -0.001)], 0.0065, 'bronz', n=6, r_son=0.002)       # the ram
            boru(y, [V(xb - 0.006, 0, hb * 0.55), V(xb + 0.012, 0, hb * 0.6)], 0.003, 'bronz', n=4, r_son=0.0015)  # the proembolion
            xe = xb - 0.026
            for i in range(n):   # the hull's half width and height where the eyes sit, and its taper there
                if st[i][0] <= xe <= st[i + 1][0]:
                    f_ = (xe - st[i][0]) / (st[i + 1][0] - st[i][0])
                    we = st[i][1] + (st[i + 1][1] - st[i][1]) * f_; he = st[i][2] + (st[i + 1][2] - st[i][2]) * f_
                    dw = (st[i + 1][1] - st[i][1]) / (st[i + 1][0] - st[i][0])
            for s in (-1, 1):   # the eyes, lying on the hull's side
                tx = V(1, s * dw, 0).normalized(); nn = V(-s * dw, s, 0).normalized()
                c = V(xe, s * we * 1.012, he * 0.76) + nn * 0.0012
                y.yuz_yon([c + tx * (0.007 * math.cos(TAU * k / 8)) + Z * (0.0045 * math.sin(TAU * k / 8)) for k in range(8)], 'beyaz', nn)
                y.yuz_yon([c + nn * 0.0005 + tx * (0.0028 * math.cos(TAU * k / 6)) + Z * (0.0028 * math.sin(TAU * k / 6)) for k in range(6)], 'koyu', nn)
            if not kaba: boru(y, [V(x0, 0, h0 - 0.005), V(x0 - 0.01, 0, h0 + 0.016), V(x0 - 0.002, 0, h0 + 0.034), V(x0 + 0.012, 0, h0 + 0.038)],
                 0.0035, 'ahsap', n=5, r_son=0.0018)
            for s in (-1, 1) if not kaba else ():   # steering oars
                cubuk(y, V(x0 + 0.026, s * (w0 + 0.008), h0 * 0.7), V(x0 - 0.008, s * (w0 + 0.016), -0.004), 0.003, 'ahsap_acik')
        else:
            # the horse-head prow (hippos) and the stern post
            boru(y, [V(xb - 0.004, 0, hb - 0.004), V(xb + 0.01, 0, hb + 0.012), V(xb + 0.006, 0, hb + 0.024)], 0.0035, 'ahsap', n=5)
            kure(y, (xb + 0.009, 0, hb + 0.026), 0.005, 'ahsap', n=6, kat=3)
            boru(y, [V(x0 + 0.004, 0, h0 - 0.004), V(x0 - 0.01, 0, h0 + 0.012), V(x0 - 0.003, 0, h0 + 0.026)], 0.004, 'ahsap', n=5)
        if kurek:
            m = max(6, int(L / 0.026))
            for k in range(m):
                x = -L * 0.32 + L * 0.62 * k / (m - 1)
                w = B / 2 * 1.02
                for s in (-1, 1):
                    for row, dz in enumerate((0.0, 0.008)):
                        a = V(x, s * w, H * 0.5 + dz)
                        b = V(x + 0.01 + 0.004 * row, s * (w + 0.065 + 0.01 * row), -0.002)
                        cubuk(y, a, b, 0.002, 'ahsap_acik')
        if yelken:
            mh = L * 0.6
            mx = 0.0 if tur == 'savas' else 0.008
            y.prizma((mx, 0), 0.003, H * 0.9, H + mh, 'ahsap', n=5)
            ys = H + mh - 0.01
            sw = B * 1.3
            cubuk(y, V(mx, -sw * 0.62, ys), V(mx, sw * 0.62, ys), 0.0035, 'ahsap')
            sh = mh * 0.62
            for k in range(4):
                z0_, z1_ = ys - sh * k / 4, ys - sh * (k + 1) / 4
                b0, b1 = 0.01 * math.sin(math.pi * k / 4), 0.01 * math.sin(math.pi * (k + 1) / 4)
                key = 'boya_kirmizi' if k % 2 == 1 else 'kumas'
                for d in (1, -1):
                    o0, o1 = mx + 0.0008 * d + 0.002 + b0, mx + 0.0008 * d + 0.002 + b1
                    y.yuz_yon([V(o0, -sw / 2, z0_), V(o0, sw / 2, z0_), V(o1, sw / 2, z1_), V(o1, -sw / 2, z1_)], key, V(d, 0, 0))
                for sy_ in (-1, 1):
                    y.yuz_yon([V(mx + 0.0012 + b0, sy_ * sw / 2, z0_), V(mx + 0.0028 + b0, sy_ * sw / 2, z0_), V(mx + 0.0028 + b1, sy_ * sw / 2, z1_),
                               V(mx + 0.0012 + b1, sy_ * sw / 2, z1_)], key, V(0, sy_, 0))
                if k == 3:
                    y.yuz_yon([V(mx + 0.0012 + b1, -sw / 2, z1_), V(mx + 0.0028 + b1, -sw / 2, z1_), V(mx + 0.0028 + b1, sw / 2, z1_),
                               V(mx + 0.0012 + b1, sw / 2, z1_)], key, -Z)
                if k == 0:
                    y.yuz_yon([V(mx + 0.0012 + b0, -sw / 2, z0_), V(mx + 0.0028 + b0, -sw / 2, z0_), V(mx + 0.0028 + b0, sw / 2, z0_),
                               V(mx + 0.0012 + b0, sw / 2, z0_)], key, Z)


def insan(y, x, yy, z, key='kirmizi', s=1.0, ten='kum_acik', aci=0.0, kol=0.0, sapka=None, kalkan=None, mizrak=None):
    """a small standing person (~0.045 tall at s 1): a robe, shoulders, a head; kol > 0 raises an arm; sapka a cap
    key; kalkan a key for a round shield on the left side, mizrak a key for an upright spear in the right hand"""
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0075, 0.0), (0.0085, 0.004), (0.0068, 0.024), (0.0058, 0.031), (0.0, 0.033)], key, n=7)
        kure(y, (0, 0, 0.039), 0.0052, ten, n=7, kat=4)
        if sapka:
            donel(y, (0, 0), [(0.0062, 0.0405), (0.0058, 0.044), (0.0035, 0.0475), (0.0, 0.048)], sapka, n=7)
        if kol:
            boru(y, [V(0, 0.006, 0.029), V(0.004, 0.009, 0.029 + 0.016 * kol)], 0.0018, ten, n=4)
        if kalkan:
            c =V(0.002, -0.0095, 0.02)
            ring = [c + V(0.0105 * math.cos(TAU * k / 10), 0, 0.0105 * math.sin(TAU * k / 10)) for k in range(10)]
            y.yuz_yon(ring, kalkan, -Y)
            y.yuz_yon([p + Y * 0.0018 for p in ring], kalkan, Y)
            for k in range(10):
                j = (k + 1) % 10
                yuz_dis(y, [ring[k], ring[j], ring[j] + Y * 0.0018, ring[k] + Y * 0.0018], kalkan, c + Y * 0.0009)
        if mizrak:
            cubuk(y, V(0.004, 0.009, 0.0), V(0.004, 0.009, 0.075), 0.0016, 'ahsap')
            donel(y, (0.004, 0.009), [(0.0, 0.075), (0.0022, 0.078), (0.0, 0.088)], mizrak, n=4)


def levha_kapali(y, pts, key, yon, kalin=0.0012):
    """a thin closed sheet through the (planar, convex) points: a front toward yon, a back, and its rim (a two-sided
    sheet with open edges shows a back face edge-on)"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    on = [p + yon * (kalin / 2) for p in pts]; ar = [p - yon * (kalin / 2) for p in pts]
    y.yuz_yon(on, key, yon); y.yuz_yon(ar, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        d = (pts[i] + pts[j]) / 2 - c
        d = d - yon * d.dot(yon)
        y.yuz_yon([on[i], on[j], ar[j], ar[i]], key, d)


def kanatli_gunes(y, o, ex, nrm, en, h, d=0.002):
    """the winged sun disk (Egyptian, taken over by the Phoenicians) in low relief over a door: o its centre on the
    wall, ex along the wall, nrm out of it; en the wingspan, h the height"""
    o, ex, nrm = Vector(o), Vector(ex).normalized(), Vector(nrm).normalized()
    P = lambda u, v, dd: o + ex * u + Z * v + nrm * dd
    r = h * 0.5
    prizma2(y, [(r * math.cos(TAU * i / 12), r * math.sin(TAU * i / 12)) for i in range(12)], P, d + 0.001, 'altin', nrm)
    for s in (-1, 1):
        for k, key in enumerate(('boya_kirmizi', 'turkuaz', 'altin')):
            a0 = -h * 0.42 + k * h * 0.26
            pts = [(s * r * 0.95, a0), (s * en / 2, a0 + h * 0.12), (s * en / 2, a0 + h * 0.3), (s * r * 0.95, a0 + h * 0.26)]
            if s < 0: pts = pts[::-1]
            prizma2(y, pts, P, d, key, nrm)
