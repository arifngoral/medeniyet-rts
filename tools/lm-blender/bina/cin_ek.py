# Helpers for the imperial Chinese landmarks (lm_yasaksehir, lm_cennettapinagi, lm_porselenkule, lm_barutatolye):
# white marble balustrades and terraces (any polygon: square or round), a double-eaved imperial hall with chiwen and
# roof beasts, curved polygonal / round roofs, an octagonal pagoda storey, and small pieces (pavilion, side hall,
# pine, cypress, bronze vessels, stone gateway). Independent of cin_ortak.py (another set of models uses that).
import math
from parcalar import *
from parcalar import _cati_z


# ---------------------------------------------------------------- balustrades and terraces
def ornekle(kose, adim, kapali=True):
    """points along a polygon (kapali) or polyline, no step longer than adim; the corners are kept"""
    pts = []
    m = len(kose)
    for i in (range(m) if kapali else range(m - 1)):
        a, b = V(kose[i][0], kose[i][1]), V(kose[(i + 1) % m][0], kose[(i + 1) % m][1])
        n = max(1, int(math.ceil((b - a).length / adim - 1e-6)))
        for k in range(n):
            pts.append(a.lerp(b, k / n))
    if not kapali:
        pts.append(V(kose[-1][0], kose[-1][1]))
    return pts


def dikme(y, p, e, z, h, key='mermer', w=0.0075, bas=0.008):
    """a balustrade post: a square shaft turned to e and a pointed (lotus-bud) cap"""
    e = V(e.x, e.y).normalized(); n = V(e.y, -e.x)
    kutu_merkez(y, (p.x, p.y), w, w, h, key, z0=z, aci=math.atan2(e.y, e.x), yuzler='onarkasagsol')
    hw = w / 2 * 1.08
    q = [V(p.x, p.y) + e * sx * hw + n * sy * hw for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    zt = z + h
    tepe = V(p.x, p.y, zt + bas)
    for i in range(4):
        a, b = q[i], q[(i + 1) % 4]
        yuz_dis(y, [V(a.x, a.y, zt), V(b.x, b.y, zt), tepe], key, V(p.x, p.y, zt))
    # (the cap's slight overhang: its underside)
    y.yuz_yon([V(c.x, c.y, zt) for c in q], key, -Z)


def korkuluk(y, kose, z, h=0.026, key='mermer', adim=0.045, kapali=True, bosluk=(), w=0.0075, t=0.0045, uc_dikme=True):
    """a Chinese white-marble balustrade along a CCW polygon (kapali) or a polyline: square posts with pointed caps every
    ~adim, a solid panel between each pair (closed boxes, seen from both sides). bosluk: [((x, y), width)] gaps (stairs)"""
    P = ornekle(kose, adim, kapali)
    n = len(P)
    acik = [any((p - V(g[0][0], g[0][1])).length < g[1] / 2 for g in bosluk) for p in P]
    for i in (range(n) if kapali else range(n - 1)):
        j = (i + 1) % n
        if acik[i] or acik[j]:
            continue
        a, b = P[i], P[j]
        L = (b - a).length
        if L < w * 1.6:
            continue
        e = (b - a) / L; nc = V(e.y, -e.x)
        o = a + e * (w / 2) + nc * (t / 2) + Z * z
        kutu(y, o, e, L - w, t, h * 0.66, key, 'onarkaust')
        # the panel's top rail, a little proud
        kutu(y, o + Z * (h * 0.66) + nc * 0.0012, e, L - w, t + 0.0024, h * 0.1, key, 'onarkaust')
    for i, p in enumerate(P):
        if acik[i]:
            continue
        # (turned to the incoming panel: at a corner the outgoing panel meets its side square)
        e = (P[i] - P[i - 1]) if (kapali or i > 0) else (P[1] - P[0])
        if not kapali and not uc_dikme and (i == 0 or i == n - 1):
            continue
        dikme(y, p, e, z, h, key, w)


def teras(y, kose, z0, h, key='mermer', ust='zemin', korkuluklu=True, bosluk=(), adim=0.045, kh=0.026, ic=0.008,
          oluk=None, kaideli=True):
    """one tier of a marble terrace round the CCW polygon kose: walls, a plinth moulding at its foot, a cornice under the
    paved top (ust key), a balustrade ic inside the edge (gaps bosluk). oluk: a key for dragon-head spouts under the
    cornice at every other post. Returns the top z"""
    zt = z0 + h
    duvarlar(y, kose, z0, zt, key, ust=ust)
    if kaideli:
        silme(y, kose, z0 + 0.001, min(0.014, h * 0.25), 0.005, key, 'kaide')
    silme(y, kose, zt - 0.009, 0.009, 0.006, key, 'kaba')
    if korkuluklu:
        ici = [V(p.x, p.y) for p in disa(kose, -ic)]
        korkuluk(y, ici, zt, kh, key, adim, True, bosluk)
        if oluk:
            P = ornekle(ici, adim)
            for k, p in enumerate(P):
                if k % 2 or any((p - V(g[0][0], g[0][1])).length < g[1] / 2 for g in bosluk):
                    continue
                d = V(p.x, p.y) - sum((V(q.x, q.y) for q in kose), V(0, 0)) / len(kose)
                # the outward normal of the nearest edge
                best = None
                for i in range(len(kose)):
                    a, b = V(kose[i].x, kose[i].y), V(kose[(i + 1) % len(kose)].x, kose[(i + 1) % len(kose)].y)
                    ee = (b - a).normalized(); nn = V(ee.y, -ee.x)
                    dd = (p - a).dot(nn)
                    if best is None or abs(dd) < best[0]:
                        best = (abs(dd), nn)
                nn = best[1]
                q0 = V(p.x, p.y) + nn * (ic - 0.002)
                cubuk(y, q0 + Z * (zt - 0.014), q0 + nn * 0.016 + Z * (zt - 0.016), 0.006, oluk, 0.007)
    return zt


def teras_merdiven(y, a, yon, en, z0, z1, n=6, key='mermer', rampa=None, rampa_en=None, yanlik=True):
    """the stair up one terrace tier, its foot centred at a, climbing towards angle yon: two flights either side of a
    carved central ramp (the imperial dragon way; rampa = its key, None: one plain flight), side cheeks"""
    e = V(math.cos(yon), math.sin(yon)); s = V(-e.y, e.x)
    a = V(a[0], a[1])
    d = (z1 - z0) * 1.15 / n
    if rampa:
        re = rampa_en or en * 0.36
        fe = (en - re) / 2
        for sg in (-1, 1):
            merdiven(y, a + s * (sg * (re / 2 + fe / 2)), yon, fe, z0, z1, n, d, key)
        # the ramp: a sloping slab with a relief panel
        L = d * n
        p0, p1 = a - s * (re / 2), a + s * (re / 2)
        A, B, C, D = p0 + Z * z0, p1 + Z * z0, p1 + e * L + Z * z1, p0 + e * L + Z * z1
        nr = (C - B).cross(B - A)   # (up and towards the foot)
        y.yuz_yon([A, B, C, D], rampa, -(e) * (z1 - z0) + Z * L)
        for p, sg in ((p0, -1), (p1, 1)):
            y.yuz_yon([p + Z * z0, p + e * L + Z * z0, p + e * L + Z * z1], key, s * sg)
        # relief: low raised clouds-and-dragon panel on the ramp
        for k in range(3):
            t0, t1 = 0.15 + k * 0.27, 0.15 + k * 0.27 + 0.2
            q = [A.lerp(D, t0) + s * 0.0, B.lerp(C, t0), B.lerp(C, t1), A.lerp(D, t1)]
            q = [q[0] + s * (re * 0.18), q[1] - s * (re * 0.18), q[2] - s * (re * 0.18), q[3] + s * (re * 0.18)]
            nn = (-(e) * (z1 - z0) + Z * L).normalized()
            q = [p + nn * 0.0025 for p in q]
            y.yuz_yon(q, 'tas_acik', nn)
            for i in range(4):
                u, v = q[i], q[(i + 1) % 4]
                y.yuz_yon([u, v, v - nn * 0.0025, u - nn * 0.0025], 'tas_acik', (u + v) / 2 - sum(q, V(0, 0, 0)) / 4)
    else:
        merdiven(y, a, yon, en, z0, z1, n, d, key)
    if yanlik:
        L = d * n
        for sg in (-1, 1):
            p = a + s * (sg * (en / 2 + 0.005))
            # a solid cheek wall: a wedge block
            A0, A1 = p - s * 0.005, p + s * 0.005
            pts_s = lambda q: [q + Z * z0, q + e * (L + 0.004) + Z * z0, q + e * (L + 0.004) + Z * (z1 + 0.01), q + Z * (z0 + 0.012)]
            for q, sg2 in ((A0, -1), (A1, 1)):
                y.yuz_yon(pts_s(q), key, s * sg2)
            y.yuz_yon([A0 + Z * (z0 + 0.012), A1 + Z * (z0 + 0.012), A1 + e * (L + 0.004) + Z * (z1 + 0.01), A0 + e * (L + 0.004) + Z * (z1 + 0.01)],
                      key, Z * L - e * (z1 - z0))
            y.yuz_yon([A0 + Z * z0, A1 + Z * z0, A1 + Z * (z0 + 0.012), A0 + Z * (z0 + 0.012)], key, -e)
            y.yuz_yon([A0 + e * (L + 0.004) + Z * z0, A1 + e * (L + 0.004) + Z * z0, A1 + e * (L + 0.004) + Z * (z1 + 0.01),
                       A0 + e * (L + 0.004) + Z * (z1 + 0.01)], key, e)
    return d * n


# ---------------------------------------------------------------- roofs: polygonal and round
def cokgen_cati(y, c, r, n, z, h, sacak=0.06, key='kiremit_koyu', mahya=None, kivrim=0.5, yukari=0.0, r_ust=0.0, kat=None,
                ns=2, nr=6, alt_key='ahsap_koyu', kalinlik=0.012, sirt=True, mahya_en=0.01, dilim=None, cann=None):
    """a curved roof over a regular n-gon of corner radius r (the wall top at z): the eaves sacak beyond the corners,
    rising h to the apex; r_ust > 0 stops it at that corner radius (a pent roof round the storey above). kivrim: concave
    slope; yukari: the corners turned up (polygonal roofs; 0 for a round one). Fascia, soffit, hip ridges (sirt).
    cann: (key, length) little bells hung at the eave corners. Returns (top z, function t->z at the corners)"""
    kat = (math.pi / n) if kat is None else kat
    Re = r + sacak
    tw = sacak / Re
    tu = 1.0 - r_ust / Re
    C = [V(c[0] + Re * math.cos(kat + TAU * i / n), c[1] + Re * math.sin(kat + TAU * i / n)) for i in range(n)]
    cc = V(c[0], c[1])

    def P(i, s, t):
        p = C[i].lerp(C[(i + 1) % n], s)
        q = cc + (p - cc) * (1 - t)
        zz = z + h * ((1 - kivrim) * t + kivrim * t * t)
        if yukari:
            zz += yukari * max(0.0, 1 - t / 0.5) ** 2.2 * abs(2 * s - 1) ** 5
        return V(q.x, q.y, zz)

    rr = sorted({0.0, tw, *[tw + (tu - tw) * k / nr for k in range(nr + 1)]})
    rr = [t for t in rr if t <= tu + 1e-9]
    kk = (lambda j: dilim[j % len(dilim)]) if dilim else (lambda j: key)
    for i in range(n):
        for m in range(ns):
            s0, s1 = m / ns, (m + 1) / ns
            for j in range(len(rr) - 1):
                q = [P(i, s0, rr[j]), P(i, s1, rr[j]), P(i, s1, rr[j + 1]), P(i, s0, rr[j + 1])]
                if rr[j + 1] > 1 - 1e-9:
                    q = q[:3]
                y.yuz_yon(q, kk(j), Z)
            p0, p1 = P(i, s0, 0), P(i, s1, 0)
            out = V(p0.x + p1.x - 2 * cc.x, p0.y + p1.y - 2 * cc.y)
            y.yuz_yon([p0, p1, p1 - Z * kalinlik, p0 - Z * kalinlik], alt_key, out)
            w0, w1 = P(i, s0, tw), P(i, s1, tw)
            y.yuz_yon([p0 - Z * kalinlik, p1 - Z * kalinlik, V(w1.x, w1.y, z), V(w0.x, w0.y, z)], alt_key, -Z)
    if sirt:
        mk = mahya or key
        ts = [tu * k / 6 for k in range(7)]
        for i in range(n):
            pts = [P(i, 0, t) + Z * (mahya_en * 0.35) for t in ts]
            for k in range(len(pts) - 1):
                cubuk(y, pts[k], pts[k + 1], mahya_en, mk)
            # the upturned tip at the corner
            d = (pts[0] - V(cc.x, cc.y, pts[0].z)).normalized()
            cubuk(y, pts[0], pts[0] + d * 0.012 + Z * 0.01, mahya_en * 0.8, mk)
    if cann:
        ck, cl = cann
        for i in range(n):
            p = P(i, 0, 0) - Z * kalinlik
            p = V(cc.x, cc.y, p.z) + (p - V(cc.x, cc.y, p.z)) * 0.985
            cubuk(y, p, p - Z * cl * 0.5, 0.0018, ck)
            donel(y, (p.x, p.y), [(0.0, p.z - cl), (0.0055, p.z - cl), (0.0035, p.z - cl * 0.55), (0.0, p.z - cl * 0.45)], ck, n=6)
    zt = z + h * ((1 - kivrim) * tu + kivrim * tu * tu)
    return zt, (lambda t: z + h * ((1 - kivrim) * t + kivrim * t * t))


def egim_icin(h_rise, t, kivrim):
    """the full roof height that makes a slope rise h_rise by the parameter t (cati_kirma / cokgen_cati curves)"""
    return h_rise / max(1e-6, (1 - kivrim) * t + kivrim * t * t)


# ---------------------------------------------------------------- roof ornaments
def chiwen(y, p, yon, s=1.0, key='kiremit_sari', ic_key=None):
    """a chiwen (dragon fish) at a ridge end p (on the ridge cap), its mouth swallowing the ridge, the tail curling up and
    out; yon: the outward direction along the ridge (a 2D vector)"""
    e = V(yon[0], yon[1]).normalized(); n = V(-e.y, e.x)
    ik = ic_key or key
    p = V(p[0], p[1], p[2])
    # the body: a tall block, narrower at the top, set on the ridge end
    b0 = [p + e * (sx * 0.013 * s) + n * (sy * 0.0065 * s) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    b1 = [p + e * (0.004 * s + sx * 0.009 * s) + n * (sy * 0.005 * s) + Z * (0.042 * s) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for i in range(4):
        j = (i + 1) % 4
        yuz_dis(y, [b0[i], b0[j], b1[j], b1[i]], key, p + Z * (0.02 * s) + e * 0.002 * s)
    y.yuz_yon(b1, key, Z)
    # the open jaw towards the ridge
    cubuk(y, p - e * (0.012 * s) + Z * (0.012 * s), p - e * (0.022 * s) + Z * (0.006 * s), 0.008 * s, ik, 0.012 * s)
    # the curled tail
    t0 = p + e * (0.006 * s) + Z * (0.04 * s)
    boru(y, [t0, t0 + e * (0.006 * s) + Z * (0.014 * s), t0 + e * (0.016 * s) + Z * (0.016 * s), t0 + e * (0.02 * s) + Z * (0.006 * s)],
         0.0055 * s, key, n=6, r_son=0.003 * s)
    # the fin / sword hilt behind the head
    cubuk(y, p - e * (0.004 * s) + Z * (0.04 * s), p - e * (0.006 * s) + Z * (0.055 * s), 0.003 * s, ik)


def sacak_hayvanlari(y, x0, x1, y0, y1, z, h, sacak, kivrim, yukari, mahya_en, sayi=5, key='altin', on_key=None, t0=0.07, t1=0.3):
    """the little glazed beasts in a row along each hip of a cati_kirma roof (the same arguments as the roof), led by
    the immortal on a hen (on_key)"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2 + sacak, (y1 - y0) / 2 + sacak
    sw = a < b
    if sw:
        a, b = b, a
    for sx in (-1, 1):
        for sy in (-1, 1):
            for k in range(sayi):
                r = t0 + (t1 - t0) * k / max(1, sayi - 1)
                px, py = sx * (a - b * r), sy * b * (1 - r)
                zz = z + _cati_z(px, py, a, b, h, kivrim, yukari) + mahya_en * 1.0
                if sw:
                    px, py = -py, px
                kk = on_key if (k == 0 and on_key) else key
                kutu_merkez(y, (cx + px, cy + py), 0.007, 0.007, 0.007, kk, z0=zz, yuzler='onarkasagsolust')
                kure(y, (cx + px, cy + py, zz + 0.0105), 0.0042, kk, n=6, kat=3)


# ---------------------------------------------------------------- an imperial hall
def salon(y, cx, cy, w, d, z, h, cati_h, sacak=0.08, cati_key='kiremit_sari', mahya='boya_sari', kivrim=0.45, yukari=0.035,
          cift=True, alt_yuk=0.05, alt_sacak=None, ic=None, ust_h=None, duvar='siva_kirmizi', direk='lake', kapi='lake_koyu',
          kafes_key='altin', boya=('turkuaz', 'boya_yesil'), cati='kirma', chiwenli=True, hayvan=5, mahya_en=0.016,
          on_tum_kapi=True, bay=0.09, kaide=None, ust_kafes=True, sus=None):
    """a timber hall w x d (w along x, the front to -y) on z: red lacquered columns, lattice doors along the front, red
    walls with lattice windows, painted beams (boya: two keys), bracket sets, a lower eave (cift: double-eaved, the
    upper storey ic inside the walls) and the main roof: cati 'kirma' (wudian, with chiwen and roof beasts) or
    'irimoya' (xieshan). kaide: (height, key) a stone base course. Returns the ridge z"""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2
    if kaide:
        kh, kk = kaide
        kutu(y, V(x0 - 0.012, y0 - 0.012, z), X, w + 0.024, d + 0.024, kh, kk)
        z += kh
    k = dikdortgen(x0, x1, y0, y1)
    zt = z + h

    def govde(k, z0, H, kapili, pencere_v=(0.3, 0.76), r=0.0105, band=0.14):
        for i in range(4):
            a_, b_ = k[i], k[(i + 1) % 4]
            L = (b_ - a_).length
            nb = max(1, int(round(L / bay)))
            e = (b_ - a_).normalized(); nn = V(e.y, -e.x)
            for j in range(nb):
                p, q = a_.lerp(b_, j / nb), a_.lerp(b_, (j + 1) / nb)
                if kapili and i == 0 and (on_tum_kapi or j == nb // 2):
                    dikdortgen_acik(y, p, q, z0, H, 0.12, 0.88, 0.0, H * (1 - band) - 0.004, (duvar, direk, direk, kapi), derin=0.01)
                    kafes(y, p, q, z0, 0.12, 0.88, H * 0.04, H * (1 - band) - 0.004, kafes_key, 4, 6, 0.0024, 0.004)
                    y.yuz_yon([p + e * ((q - p).length * 0.12) - nn * 0.0035 + Z * (z0 + H * 0.3),
                               p + e * ((q - p).length * 0.88) - nn * 0.0035 + Z * (z0 + H * 0.3),
                               p + e * ((q - p).length * 0.88) - nn * 0.0035 + Z * (z0 + H * 0.3 + 0.006),
                               p + e * ((q - p).length * 0.12) - nn * 0.0035 + Z * (z0 + H * 0.3 + 0.006)], kapi, nn)   # (the door's solid lower half)
                elif pencere_v and (nb <= 2 or j not in (0, nb - 1)):
                    v0, v1 = H * pencere_v[0], H * pencere_v[1]
                    dikdortgen_acik(y, p, q, z0, H, 0.16, 0.84, v0, v1, (duvar, direk, direk, kapi), derin=0.01)
                    kafes(y, p, q, z0, 0.16, 0.84, v0, v1, kafes_key, 4, 4, 0.0022, 0.004)
                else:
                    duz_duvar(y, p, q, z0, z0 + H, duvar)
            for j in range(nb + 1):
                p = a_.lerp(b_, j / nb) + nn * 0.004
                y.prizma((p.x, p.y), r, z0 + 0.006, z0 + H * (1 - band), direk, n=8, ust=True)
                kutu_merkez(y, (p.x, p.y), r * 3.0, r * 3.0, 0.006, 'mermer', z0=z0, yuzler='onarkasagsolust')
            # the painted beams (lintel and architrave) round the top
            hb = H * band
            kutu(y, a_ + nn * 0.009 + Z * (z0 + H - hb) - e * 0.009, e, L + 0.018, 0.018, hb * 0.5, boya[1], 'onust')
            kutu(y, a_ + nn * 0.011 + Z * (z0 + H - hb * 0.5) - e * 0.011, e, L + 0.022, 0.022, hb * 0.5, boya[0], 'onust')
            # gilt dots along the beam
            for j in range(nb):
                p = a_.lerp(b_, (j + 0.5) / nb) + nn * 0.0115 + Z * (z0 + H - hb * 0.25)
                y.yuz_yon([p - e * 0.012 - Z * 0.004, p + e * 0.012 - Z * 0.004, p + e * 0.012 + Z * 0.004, p - e * 0.012 + Z * 0.004], 'altin', nn)

    def konsol(k, zz, adim=0.05):
        # bracket sets: a frieze band closing the gap to the roof, and stepped blocks
        duvarlar(y, k, zz, zz + 0.02, boya[1])
        for i in range(4):
            a_, b_ = k[i], k[(i + 1) % 4]
            e = (b_ - a_).normalized(); nn = V(e.y, -e.x); L = (b_ - a_).length
            nb = max(2, int(round(L / adim)))
            for j in range(nb + 1):
                p = a_.lerp(b_, j / nb)
                kutu_merkez(y, (p.x + nn.x * 0.009, p.y + nn.y * 0.009), 0.012, 0.018, 0.009, 'ahsap', z0=zz, aci=math.atan2(e.y, e.x), yuzler='onarkasagsolust')
                kutu_merkez(y, (p.x + nn.x * 0.016, p.y + nn.y * 0.016), 0.024, 0.012, 0.011, boya[0], z0=zz + 0.009, aci=math.atan2(e.y, e.x), yuzler='onarkasagsolust')
        return zz + 0.02

    govde(k, z, h, True)
    zc = konsol(k, zt)
    if cift:
        ic = ic if ic is not None else min(w, d) * 0.12
        ust_h = ust_h if ust_h is not None else h * 0.42
        asx = alt_sacak if alt_sacak is not None else sacak * 0.9
        # the pent roof stops just inside the upper storey's walls (they rise through it)
        a_, b_ = w / 2 + asx, d / 2 + asx
        m = min(a_, b_)
        r_ust = 1 - (min(w, d) / 2 - ic - 0.012) / m
        hfull = egim_icin(alt_yuk, r_ust, kivrim * 0.6)
        cati_kirma(y, x0, x1, y0, y1, zc, hfull, asx, cati_key, mahya, 0.012, kivrim * 0.6, yukari, 'lake_koyu', ns=max(4, int(w / 0.075)), nr=3,
                   r_ust=r_ust, mahya_en=mahya_en)
        k2 = dikdortgen(x0 + ic, x1 - ic, y0 + ic, y1 - ic)
        z2 = zc + alt_yuk
        # the upper storey: a plain wall up to the pent roof, then a clerestory of lattice windows
        duvarlar(y, k2, zc, z2 + 0.004, duvar)
        govde(k2, z2 + 0.004, ust_h, False, (0.12, 0.7) if ust_kafes else None, r=0.008, band=0.22)
        zc = konsol(k2, z2 + 0.004 + ust_h)
        x0, x1, y0, y1 = x0 + ic, x1 - ic, y0 + ic, y1 - ic
    if cati == 'irimoya':
        ns = max(4, int((x1 - x0) / 0.05))
        return cati_irimoya(y, x0, x1, y0, y1, zc, cati_h, sacak, cati_key, mahya, kivrim, yukari, 'lake_koyu', duvar, sus=sus,
                            ns=ns, nr=4 if ns < 8 else 6, ns2=max(3, ns * 2 // 3), nr2=3 if ns < 8 else 5)
    ns = max(4, int((x1 - x0) / 0.05))
    tepe = cati_kirma(y, x0, x1, y0, y1, zc, cati_h, sacak, cati_key, mahya, 0.012, kivrim, yukari, 'lake_koyu', ns=ns, nr=4 if ns < 8 else 6,
                      mahya_en=mahya_en)
    a, b = (x1 - x0) / 2 + sacak, (y1 - y0) / 2 + sacak
    if chiwenli and abs(a - b) > 1e-6:
        zr = zc + _cati_z(0, 0, max(a, b), min(a, b), cati_h, kivrim, yukari) + mahya_en * 0.3 + mahya_en * 0.5
        L = abs(a - b)
        for sg in (-1, 1):
            if a > b:
                chiwen(y, ((x0 + x1) / 2 + sg * L, (y0 + y1) / 2, zr), (sg, 0), min(2.2, max(0.8, cati_h / 0.09)), mahya, cati_key)
            else:
                chiwen(y, ((x0 + x1) / 2, (y0 + y1) / 2 + sg * L, zr), (0, sg), min(2.2, max(0.8, cati_h / 0.09)), mahya, cati_key)
        tepe = zr + 0.055 * min(2.2, max(0.8, cati_h / 0.09))
    if hayvan:
        sacak_hayvanlari(y, x0, x1, y0, y1, zc, cati_h, sacak, kivrim, yukari, mahya_en, hayvan, 'altin', 'boya_sari')
    return tepe


# ---------------------------------------------------------------- an octagonal pagoda storey
def sekizgen_kat(y, c, r, z, h, govde='beyaz', cer=('kiremit_yesil', 'kiremit_sari'), kose_key='kiremit_sari', n=8,
                 kapi=(0, 2, 4, 6), derin=0.02):
    """the walls of one storey of an octagonal pagoda (corner radius r) from z, h high: an arched opening on every face
    (doors on the faces in kapi, blind windows on the others) with glazed frames, corner pilasters, a frieze band.
    Returns the wall top z"""
    k = cokgen(c, r, n, kat=math.pi / n)
    for i in range(n):
        a, b = k[i], k[(i + 1) % n]
        if i in kapi:
            y.kemerli(V(a.x, a.y), V(b.x, b.y), z, h, (govde, 'tas_acik', 'tas_acik', 'koyu'), v0=0.0, en=0.36, ust=h * 0.24, derin=derin,
                      k_say=8, cerceve=(0.007, list(cer)))
        else:
            y.kemerli(V(a.x, a.y), V(b.x, b.y), z, h, (govde, 'tas_acik', 'tas_acik', 'lake_koyu'), v0=h * 0.16, en=0.3, ust=h * 0.3,
                      derin=derin * 0.5, k_say=8, cerceve=(0.006, list(cer)))
    for p in k:
        y.prizma((p.x, p.y), 0.009, z, z + h, kose_key, n=6, ust=False)
    return z + h


# ---------------------------------------------------------------- small pieces
def kosk(y, c, w, z, h, cati_h, sacak=0.04, direk='lake', cati='kiremit_koyu', mahya='kiremit_koyu2', kivrim=0.55, yukari=0.03,
         kaide='mermer', aci=0.0, tepe_key='altin', n=4, boya='turkuaz'):
    """an open pavilion (ting) on a stone base: posts, a painted frieze with gilt fretwork, a curved roof (n = 4: square
    pyramid; 6 / 8: polygonal), a knob. Returns the tip z"""
    with parca(y, (c[0], c[1], 0), aci):
        if n == 4:
            kutu_merkez(y, (0, 0), w + 0.03, w + 0.03, 0.02, kaide, z0=z)
            silme(y, dikdortgen(-(w + 0.03) / 2, (w + 0.03) / 2, -(w + 0.03) / 2, (w + 0.03) / 2), z + 0.016, 0.004, 0.003, 'tas_acik')
            k = dikdortgen(-w / 2, w / 2, -w / 2, w / 2)
        else:
            kb = cokgen((0, 0), w / 2 + 0.02, n, math.pi / n)
            duvarlar(y, kb, z, z + 0.02, kaide, ust='zemin')
            k = cokgen((0, 0), w / 2, n, math.pi / n)
        zb = z + 0.02
        for p in k:
            q = p * (1 - 0.012 / max(1e-6, p.length))
            sutun(y, q.x, q.y, zb, zb + h * 0.82, 0.0065, direk, 'ahsap', bas_key='mermer')
        m = len(k)
        for i in range(m):
            a, b = k[i], k[(i + 1) % m]
            e = (b - a).normalized(); L = (b - a).length
            kutu(y, a + Z * (zb + h * 0.82) - e * 0.004 + V(e.y, -e.x) * 0.006, e, L + 0.008, 0.012, h * 0.18, boya)
            for j in range(1, 6):
                p = a.lerp(b, j / 6)
                cubuk(y, p + Z * (zb + h * 0.7), p + Z * (zb + h * 0.82), 0.003, 'altin')
        y.yuz_yon([V(p.x, p.y, zb + h) for p in k], 'ahsap_koyu', -Z)
        if n == 4:
            tepe = cati_kirma(y, -w / 2, w / 2, -w / 2, w / 2, zb + h, cati_h, sacak, cati, mahya, 0.01, kivrim, yukari, 'lake_koyu', ns=8, nr=5)
        else:
            tepe, _ = cokgen_cati(y, (0, 0), w / 2, n, zb + h, cati_h, sacak, cati, mahya, kivrim, yukari, ns=2, nr=5, alt_key='lake_koyu',
                                  kalinlik=0.01, mahya_en=0.008)
        kure(y, (0, 0, tepe + 0.012), 0.012, tepe_key, n=8, kat=4)
        tepe += 0.024
    return tepe


def kucuk_salon(y, x0, x1, y0, y1, z, h, cati_h, sacak=0.04, duvar='siva_kirmizi', direk='lake', cati='kiremit_koyu', mahya='kiremit_koyu2',
                tur='irimoya', kivrim=0.4, yukari=0.025, kaide=0.02, kaide_key='mermer', kapi_yon=0, bay=0.07, sus=None, arka_duz=False):
    """a smaller timber hall on a stone base: red walls between posts, lattice windows, a door on side kapi_yon (0 front
    -y, 1 +x, 2 back, 3 -x), a painted lintel, roof tur 'irimoya' / 'kirma' / 'besik'. arka_duz: the side opposite the
    door plain (against a wall). Returns the ridge z"""
    kx0, kx1, ky0, ky1 = x0 - 0.016, x1 + 0.016, y0 - 0.016, y1 + 0.016
    if kaide:
        kutu(y, V(kx0, ky0, z), X, kx1 - kx0, ky1 - ky0, kaide, kaide_key)
        silme(y, dikdortgen(kx0, kx1, ky0, ky1), z + kaide - 0.004, 0.004, 0.003, 'tas_acik', 'duz')
    zb = z + kaide
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        L = (b - a).length
        nb = max(1, int(round(L / bay)))
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for j in range(nb):
            p, q = a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb)
            if i == kapi_yon and (j == nb // 2 or (nb >= 5 and j in (nb // 2 - 1, nb // 2 + 1))):
                dikdortgen_acik(y, p, q, zb, h, 0.18, 0.82, 0.0, h * 0.8, (duvar, 'lake_koyu', 'lake_koyu', 'lake_koyu'), derin=0.008)
                kafes(y, p, q, zb, 0.18, 0.82, 0.0, h * 0.8, 'altin' if kapi_yon == i else 'lake', 4, 4, 0.0022, 0.004)
            elif (not arka_duz or i != (kapi_yon + 2) % 4) and (nb > 1 and j not in (0, nb - 1) or (nb <= 2)):
                dikdortgen_acik(y, p, q, zb, h, 0.2, 0.8, h * 0.32, h * 0.78, (duvar, 'lake_koyu', 'lake_koyu', 'koyu'), derin=0.008)
                kafes(y, p, q, zb, 0.2, 0.8, h * 0.32, h * 0.78, 'lake', 3, 3, 0.0022, 0.004)
            else:
                duz_duvar(y, p, q, zb, zb + h, duvar)
        for j in range(nb + 1):
            p = a.lerp(b, j / nb) + nn * 0.004
            kutu_merkez(y, (p.x, p.y), 0.011, 0.011, h, direk, z0=zb)
        kutu(y, a + nn * 0.007 + Z * (zb + h * 0.84) - e * 0.007, e, L + 0.014, 0.014, h * 0.16, 'turkuaz', 'onust')
    zc = zb + h
    y.yuz_yon([V(p.x, p.y, zc) for p in k], 'ahsap_koyu', Z)
    ns = max(4, int(max(x1 - x0, y1 - y0) / 0.06))
    if tur == 'irimoya':
        return cati_irimoya(y, x0, x1, y0, y1, zc, cati_h, sacak, cati, mahya, kivrim, yukari, 'lake_koyu', duvar, sus=sus, ns=ns, nr=4,
                            ns2=max(3, ns * 2 // 3), nr2=3)
    if tur == 'besik':
        return cati_besik(y, x0, x1, y0, y1, zc, cati_h, sacak, cati, mahya, 0.01, kivrim, 'lake_koyu', duvar, sus=sus, ns=ns, nr=4)
    return cati_kirma(y, x0, x1, y0, y1, zc, cati_h, sacak, cati, mahya, 0.01, kivrim, yukari, 'lake_koyu', ns=ns, nr=4)


def cam(y, x, yy, z, boy=0.14, key='yesil_koyu', govde='ahsap'):
    """a pine: a short trunk and three stacked cones"""
    y.prizma((x, yy), boy * 0.035, z - 0.01, z + boy * 0.3, govde, n=5)
    for k, (r, z0, hh) in enumerate(((0.3, 0.18, 0.4), (0.23, 0.42, 0.34), (0.15, 0.63, 0.37))):
        y.koni((x, yy), boy * r, z + boy * z0, boy * hh, key, n=8)
        y.yuz_yon([V(x + boy * r * math.cos(TAU * i / 8), yy + boy * r * math.sin(TAU * i / 8), z + boy * z0) for i in range(8)], key, -Z)


def servi(y, x, yy, z, boy=0.16, key='yesil_koyu', govde='ahsap_koyu'):
    """an old Chinese cypress (Tiantan): a stout trunk and a tall, lumpy dark crown"""
    y.prizma((x, yy), boy * 0.05, z - 0.01, z + boy * 0.25, govde, n=6)
    donel(y, (x, yy), [(0.0, z + boy * 0.18), (boy * 0.2, z + boy * 0.26), (boy * 0.24, z + boy * 0.45), (boy * 0.19, z + boy * 0.66),
                       (boy * 0.12, z + boy * 0.86), (0.0, z + boy)], key, n=9)


def kazan(y, x, yy, z, s=1.0, key='bronz'):
    """a bronze cauldron (water vat / ding) on short legs with two handles"""
    for i in range(3):
        a = TAU * i / 3 + 0.5
        y.prizma((x + 0.013 * s * math.cos(a), yy + 0.013 * s * math.sin(a)), 0.0028 * s, z, z + 0.008 * s, key, n=5, ust=False)
    donel(y, (x, yy), [(0.0, z + 0.006 * s), (0.014 * s, z + 0.008 * s), (0.02 * s, z + 0.018 * s), (0.019 * s, z + 0.028 * s),
                       (0.021 * s, z + 0.031 * s), (0.016 * s, z + 0.031 * s), (0.0, z + 0.024 * s)], key, n=8)
    for sg in (-1, 1):
        boru(y, [V(x + sg * 0.015 * s, yy, z + 0.03 * s), V(x + sg * 0.017 * s, yy, z + 0.04 * s), V(x + sg * 0.009 * s, yy, z + 0.04 * s),
                 V(x + sg * 0.008 * s, yy, z + 0.031 * s)], 0.002 * s, key, n=4)


def tutsu(y, x, yy, z, s=1.0, key='bronz'):
    """a tall bronze incense burner: a round body on legs, a pierced roofed lid"""
    for i in range(3):
        a = TAU * i / 3
        cubuk(y, V(x + 0.012 * s * math.cos(a), yy + 0.012 * s * math.sin(a), z), V(x + 0.009 * s * math.cos(a), yy + 0.009 * s * math.sin(a), z + 0.016 * s), 0.004 * s, key)
    donel(y, (x, yy), [(0.0, z + 0.014 * s), (0.016 * s, z + 0.018 * s), (0.018 * s, z + 0.03 * s), (0.014 * s, z + 0.036 * s),
                       (0.008 * s, z + 0.04 * s), (0.006 * s, z + 0.05 * s), (0.016 * s, z + 0.054 * s), (0.0, z + 0.068 * s)], key, n=8)
    kure(y, (x, yy, z + 0.072 * s), 0.004 * s, 'altin', n=6, kat=3)


def aslan(y, x, yy, z, aci=0.0, s=1.0, key='bronz', kaide_key='mermer'):
    """a guardian lion on a pedestal (stylised: haunches, chest, curly head)"""
    with parca(y, (x, yy, z), aci, s):
        kutu_merkez(y, (0, 0), 0.034, 0.024, 0.022, kaide_key)
        silme(y, dikdortgen(-0.017, 0.017, -0.012, 0.012), 0.018, 0.004, 0.003, kaide_key)
        kutu_merkez(y, (0.006, 0), 0.02, 0.018, 0.012, key, z0=0.022)               # haunches
        cubuk(y, V(-0.002, 0, 0.026), V(-0.008, 0, 0.046), 0.014, key, 0.016)       # chest
        kure(y, (-0.01, 0, 0.052), 0.011, key, n=8, kat=4)                          # mane / head
        kure(y, (-0.019, 0, 0.05), 0.005, key, n=6, kat=3)                          # muzzle
        cubuk(y, V(-0.012, 0.006, 0.022), V(-0.013, 0.006, 0.036), 0.005, key)      # forelegs
        cubuk(y, V(-0.012, -0.006, 0.022), V(-0.013, -0.006, 0.036), 0.005, key)


def tas_kapi(y, cx, cy, z, en, h, key='mermer', ust_key=None, n=3, kalin=0.012, aci=0.0, cati=None):
    """a stone gateway (pailou / lingxing gate): n openings between square posts with cloud caps, a lintel over each
    opening; cati: a key for small tiled roofs over the lintels (None: plain stone)"""
    uk = ust_key or key
    # (each opening its own gate on two posts, the middle one higher and wider, open gaps between them: a run of posts
    #  joined by continuous rails read as a fence)
    with parca(y, (cx, cy, z), aci):
        w1 = en / n
        for i in range(n):
            orta = n == 3 and i == 1 or n == 1
            xc = -en / 2 + w1 * (i + 0.5)
            ow = w1 * (0.72 if orta else 0.6)
            hp = h * (1.0 if orta else 0.86)
            xs = (xc - ow / 2, xc + ow / 2)
            for x in xs:
                kutu_merkez(y, (x, 0), kalin, kalin, hp, key, yuzler='onarkasagsol')
                # the cloud cap: a drum with a rounded crown
                donel(y, (x, 0), [(kalin * 0.62, hp), (kalin * 0.68, hp + 0.003), (kalin * 0.68, hp + 0.008), (kalin * 0.45, hp + 0.012),
                                  (0.0, hp + 0.014)], key, n=8)
                # the cloud board through the post under the cap
                kutu_merkez(y, (x, 0), kalin * 0.5, kalin * 3.4, h * 0.09, uk, z0=hp - h * 0.2)
                # a drum-stone at its foot
                kutu_merkez(y, (x, 0), kalin * 1.4, kalin * 2.6, h * 0.14, key)
            xa, xb = xs[0] + kalin / 2, xs[1] - kalin / 2
            hh = hp * 0.86
            # the top lintel, a recessed panel, the lower lintel, and a flaming jewel on top
            kutu(y, V(xa, -kalin * 0.45, hh - h * 0.13), X, xb - xa, kalin * 0.9, h * 0.13, uk, 'onarkaustsagsol')
            kutu(y, V(xa, -kalin * 0.25, hh - h * 0.31), X, xb - xa, kalin * 0.5, h * 0.18, key, 'onarkasagsol')
            kutu(y, V(xa, -kalin * 0.4, hh - h * 0.38), X, xb - xa, kalin * 0.8, h * 0.07, uk, 'onarkaustsagsol')
            xm = (xa + xb) / 2
            donel(y, (xm, 0), [(0.0, hh), (kalin * 0.45, hh + 0.004), (kalin * 0.55, hh + 0.01), (kalin * 0.3, hh + 0.017), (0.0, hh + 0.024)],
                  'altin' if cati else uk, n=6)
            if cati:
                cati_besik(y, xa - 0.004, xb + 0.004, -kalin * 0.5, kalin * 0.5, hh, 0.012, 0.008, cati, cati, 0.004, 0.3, 'lake_koyu', uk,
                           uc_sacak=0.006, mahya_en=0.005)


def kirmizi_sur(y, kose, z, h, kalin=0.03, duvar='siva_kirmizi', cati='kiremit_sari', mahya='boya_sari', kapali=True, baslik=0.03,
                kaide_key='mermer'):
    """a palace / temple enclosure wall: red plaster, a stone base course, a little tiled coping roof along its top
    (the polygon / polyline kose is the wall's middle line). Returns the coping top z"""
    dis_ = [V(p.x, p.y) for p in disa(kose, kalin / 2, kapali)]
    ic_ = [V(p.x, p.y) for p in disa(kose, -kalin / 2, kapali)]
    m = len(kose)
    segs = range(m) if kapali else range(m - 1)
    zt = z + h
    for i in segs:
        j = (i + 1) % m
        duz_duvar(y, dis_[i], dis_[j], z, zt, duvar)
        duz_duvar(y, ic_[j], ic_[i], z, zt, duvar)
        # the base course
        e = (dis_[j] - dis_[i]); L = e.length; e = e / L; nn = V(e.y, -e.x)
        y.yuz_yon([dis_[i] + nn * 0.003 + Z * z, dis_[j] + nn * 0.003 + Z * z, dis_[j] + nn * 0.003 + Z * (z + h * 0.12), dis_[i] + nn * 0.003 + Z * (z + h * 0.12)], kaide_key, nn)
        y.yuz_yon([dis_[i] + nn * 0.003 + Z * (z + h * 0.12), dis_[j] + nn * 0.003 + Z * (z + h * 0.12), dis_[j] + Z * (z + h * 0.12), dis_[i] + Z * (z + h * 0.12)], kaide_key, Z)
        ei = (ic_[i] - ic_[j]).normalized(); ni = V(ei.y, -ei.x)
        y.yuz_yon([ic_[j] + ni * 0.003 + Z * z, ic_[i] + ni * 0.003 + Z * z, ic_[i] + ni * 0.003 + Z * (z + h * 0.12), ic_[j] + ni * 0.003 + Z * (z + h * 0.12)], kaide_key, ni)
        y.yuz_yon([ic_[j] + ni * 0.003 + Z * (z + h * 0.12), ic_[i] + ni * 0.003 + Z * (z + h * 0.12), ic_[i] + Z * (z + h * 0.12), ic_[j] + Z * (z + h * 0.12)], kaide_key, Z)
    if not kapali:
        for k, j in ((0, 1), (m - 1, m - 2)):
            y.yuz_yon([dis_[k] + Z * z, ic_[k] + Z * z, ic_[k] + Z * zt, dis_[k] + Z * zt], duvar, kose[k] - kose[j])
    # the coping: a small gable roof along each segment (ends mitred by overlapping a little)
    s = kalin * 0.45
    for i in segs:
        j = (i + 1) % m
        a, b = V(kose[i].x, kose[i].y), V(kose[j].x, kose[j].y)
        e = (b - a); L = e.length; e = e / L; nn = V(e.y, -e.x)
        ek0 = s if (kapali or i > 0) else s
        A, B = a - e * ek0, b + e * s
        o = [A + nn * (kalin / 2 + s), B + nn * (kalin / 2 + s), B - nn * (kalin / 2 + s), A - nn * (kalin / 2 + s)]
        R0, R1 = A + Z * (zt + baslik), B + Z * (zt + baslik)
        y.yuz_yon([o[0] + Z * zt, o[1] + Z * zt, R1, R0], cati, nn + Z)
        y.yuz_yon([o[2] + Z * zt, o[3] + Z * zt, R0, R1], cati, -nn + Z)
        y.yuz_yon([o[0] + Z * zt, o[3] + Z * zt, R0], cati, -e)
        y.yuz_yon([o[1] + Z * zt, o[2] + Z * zt, R1], cati, e)
        y.yuz_yon([o[0] + Z * zt, o[1] + Z * zt, o[2] + Z * zt, o[3] + Z * zt], 'lake_koyu', -Z)
        cubuk(y, R0 + Z * 0.002, R1 + Z * 0.002, 0.008, mahya)
    return zt + baslik


def sayim(y):
    """print the triangle count of every section (y.bolum)"""
    b = getattr(y, 'bolumler', [])
    for i, (s, ad) in enumerate(b):
        e = b[i + 1][0] if i + 1 < len(b) else len(y.faces)
        print('BOLUM %-22s %6d' % (ad, sum(len(p) - 2 for p, _ in y.faces[s:e])))


# ---------------------------------------------------------------- round halls (Tiantan)
def yuvarlak_govde(y, c, r, n, z, H, duvar='siva_kirmizi', direk='lake', kapi='lake_koyu', kafes_key='altin',
                   boya=('turkuaz', 'boya_yesil'), band=0.16, pencere=(0.0, 1.0), kat=None, direk_r=0.011, kafesli=True):
    """the walls of a round (n-gon) hall of corner radius r from z, H high: a lattice panel in every bay between
    lacquered columns (pencere: its sill / head as parts of the height under the beams; kafesli=False: plain red
    walls), the painted beams as two mouldings round the top. Returns the top z"""
    kat = (math.pi / n) if kat is None else kat
    k = cokgen(c, r, n, kat)
    zb = z + H * (1 - band)
    for i in range(n):
        a, b = k[i], k[(i + 1) % n]
        if kafesli:
            v0, v1 = (zb - z) * pencere[0], (zb - z) * pencere[1] - 0.004
            dikdortgen_acik(y, a, b, z, H, 0.12, 0.88, v0, v1, (duvar, direk, direk, kapi), derin=0.008)
            kafes(y, a, b, z, 0.12, 0.88, max(v0, H * 0.04), v1, kafes_key, 3, 5 if v1 - v0 > 0.08 else 3, 0.0022, 0.0035)
        else:
            duz_duvar(y, a, b, z, z + H, duvar)
    for p in k:
        q = V(c[0], c[1]) + (p - V(c[0], c[1])) * (1 + 0.004 / r)
        y.prizma((q.x, q.y), direk_r, z + 0.006, zb, direk, n=8, ust=True)
        kutu_merkez(y, (q.x, q.y), direk_r * 3, direk_r * 3, 0.006, 'mermer', z0=z, yuzler='onarkasagsolust')
    hb = z + H - zb
    silme(y, cokgen(c, r, n, kat), zb, hb * 0.5, 0.012, boya[1], 'duz')
    silme(y, cokgen(c, r, n, kat), zb + hb * 0.5, hb * 0.5, 0.015, boya[0], 'duz')
    return z + H


def yuvarlak_konsol(y, c, r, n, z, boya=('turkuaz', 'boya_yesil'), adim=0.05, h=0.02, kat=None):
    """a ring of bracket sets under a round eave, with a frieze band closing the gap to the roof. Returns the top z"""
    kat = (math.pi / n) if kat is None else kat
    duvarlar(y, cokgen(c, r, n, kat), z, z + h, boya[1])
    m = max(8, int(round(TAU * r / adim)))
    for j in range(m):
        a = TAU * j / m
        d = V(math.cos(a), math.sin(a))
        p = V(c[0], c[1]) + d * r
        kutu_merkez(y, (p.x + d.x * 0.008, p.y + d.y * 0.008), 0.018, 0.012, h * 0.45, 'ahsap', z0=z, aci=a, yuzler='onarkasagsolust')
        kutu_merkez(y, (p.x + d.x * 0.014, p.y + d.y * 0.014), 0.012, 0.024, h * 0.55, boya[0], z0=z + h * 0.45, aci=a, yuzler='onarkasagsolust')
    return z + h


def cokgen_konsol(y, c, r, n, z, boya=('kiremit_yesil', 'lake_koyu'), adim=0.05, h=0.02, kat=None, frize='beyaz'):
    """bracket sets along the faces of an n-gon (corner radius r) under its eave, a frieze closing the gap to the roof.
    Returns the top z"""
    kat = (math.pi / n) if kat is None else kat
    k = cokgen(c, r, n, kat)
    duvarlar(y, k, z, z + h, frize)
    for i in range(n):
        a_, b_ = k[i], k[(i + 1) % n]
        e = (b_ - a_).normalized(); nn = V(e.y, -e.x); L = (b_ - a_).length
        m = max(2, int(round(L / adim)))
        for j in range(m):   # (the corner set belongs to the next face)
            p = a_.lerp(b_, j / m)
            an = math.atan2(e.y, e.x)
            kutu_merkez(y, (p.x + nn.x * 0.008, p.y + nn.y * 0.008), 0.012, 0.018, h * 0.45, boya[1], z0=z, aci=an, yuzler='onarkasagsolust')
            kutu_merkez(y, (p.x + nn.x * 0.015, p.y + nn.y * 0.015), 0.024, 0.012, h * 0.55, boya[0], z0=z + h * 0.45, aci=an, yuzler='onarkasagsolust')
    return z + h


def insan(y, x, yy, z, aci=0.0, govde='kumas', sapka='saz', boy=0.05, egik=0.0):
    """a small figure: legs, a tunic, a head and a wide conical straw hat (egik: bent forward, at work)"""
    with parca(y, (x, yy, z), aci):
        s = boy / 0.05
        for sx in (-1, 1):
            cubuk(y, V(0, sx * 0.004 * s, 0), V(0, sx * 0.004 * s, 0.018 * s), 0.004 * s, 'ahsap_koyu')
        govde_ust = V(egik * 0.012 * s, 0, 0.04 * s - egik * 0.008 * s)
        donel(y, (0, 0), [(0.0085 * s, 0.016 * s), (0.0075 * s, 0.026 * s), (0.0055 * s, 0.036 * s), (0, 0.038 * s)], govde, n=8)
        y.yuz_yon([V(0.0085 * s * math.cos(TAU * i / 8), 0.0085 * s * math.sin(TAU * i / 8), 0.016 * s) for i in range(8)], govde, -Z)
        if egik:
            boru(y, [V(0, 0, 0.032 * s), govde_ust], 0.0055 * s, govde, n=6)
        bas = govde_ust + V(0.002 * s * egik, 0, 0.004 * s)
        kure(y, (bas.x, bas.y, bas.z), 0.0048 * s, 'siva_krem', n=8, kat=4)
        y.koni((bas.x, bas.y), 0.012 * s, bas.z + 0.002 * s, 0.008 * s, sapka, n=10)
        y.yuz_yon([V(bas.x + 0.012 * s * math.cos(TAU * i / 10), bas.y + 0.012 * s * math.sin(TAU * i / 10), bas.z + 0.002 * s) for i in range(10)], sapka, -Z)
        for sy in (-1, 1):
            cubuk(y, V(0, sy * 0.008 * s, 0.033 * s), V(0.006 * s + egik * 0.01 * s, sy * 0.009 * s, 0.02 * s - egik * 0.006 * s), 0.003 * s, govde)


def fici(y, x, yy, z, s=1.0, key='ahsap', bant='demir', yatik=None):
    """a barrel (upright; yatik = angle: lying on its side, its axis along that angle)"""
    pr = [(0.0, 0.0), (0.016, 0.0), (0.019, 0.012), (0.02, 0.022), (0.019, 0.032), (0.016, 0.044), (0.0, 0.044)]
    if yatik is None:
        donel(y, (x, yy), [(r * s, z + h * s) for r, h in pr], key, n=10)
        for h in (0.008, 0.036):
            halka_kornis(y, (x, yy), 0.0185 * s, z + h * s, 0.003 * s, 0.0012 * s, 10, bant)
    else:
        d = V(math.cos(yatik), math.sin(yatik))
        a = V(x, yy, z + 0.02 * s) - d * (0.022 * s)
        pts = [a + d * (h * s) for _, h in pr[1:-1]]
        rr = [r * s for r, _ in pr[1:-1]]
        n = 10
        u = V(-d.y, d.x, 0); w = Z
        rings = [[pts[k] + (u * math.cos(TAU * i / n) + w * math.sin(TAU * i / n)) * rr[k] for i in range(n)] for k in range(len(pts))]
        for k in range(len(rings) - 1):
            for i in range(n):
                j = (i + 1) % n
                yuz_dis(y, [rings[k][i], rings[k + 1][i], rings[k + 1][j], rings[k][j]], key, (pts[k] + pts[k + 1]) / 2)
        y.yuz_yon(rings[0], key, -d)
        y.yuz_yon(rings[-1], key, d)
