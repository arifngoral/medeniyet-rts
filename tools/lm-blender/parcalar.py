# Shared building parts for the detail-path landmark models (tools/lm-blender/README.md, "Parça kütüphanesi").
# Every function takes the Yapi (ortak.py) first and adds faces with material keys (doku.py MALZEME). Blender axes:
# z up; a wall from a to b faces the RIGHT of a->b, so walking a CCW polygon (seen from above) faces outward.
# Faces are one-sided in the game (back faces are culled): every function here winds its faces outward.
# Scale: the models are built with their longest side ~2.2-2.6 units (Süleymaniye 2.5): the stone pattern
# (doku.py KARO), the baked shadow distance and the default sizes here assume that.
#
#   with parca(y, konum, aci, olcek): ...   build a part at the origin, then move / turn / scale it into place
#
import math
from mathutils import Vector

X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
PENCERE = ('tas', 'tas_koyu', 'tas_acik', 'cam')          # kemerli(): wall, reveal, sill, glass
REVAK = ('tas', 'tas', 'tas_acik', 'tas_koyu')            # an open arcade: dark back
TAU = 2 * math.pi


def V(x, y, z=0.0):
    return Vector((x, y, z))


def dikdortgen(x0, x1, y0, y1, z=0.0):
    """rectangle corners CCW"""
    return [V(x0, y0, z), V(x1, y0, z), V(x1, y1, z), V(x0, y1, z)]


def cokgen(c, r, n, kat=0.0, z=0.0):
    """regular polygon corners CCW (kat: start angle)"""
    return [V(c[0] + r * math.cos(kat + TAU * i / n), c[1] + r * math.sin(kat + TAU * i / n), z) for i in range(n)]


def disa(kose, d, kapali=True):
    """a CCW polygon (or an open polyline) offset outward (to the right of travel) by d, mitred corners"""
    n = len(kose); out = []
    for i in range(n):
        p = kose[i]
        a = kose[i - 1] if (kapali or i > 0) else None
        b = kose[(i + 1) % n] if (kapali or i < n - 1) else None
        ns = []
        if a is not None:
            e = (p - a); e.z = 0; e.normalize(); ns.append(V(e.y, -e.x))
        if b is not None:
            e = (b - p); e.z = 0; e.normalize(); ns.append(V(e.y, -e.x))
        if len(ns) == 1:
            m = ns[0]
        else:
            m = (ns[0] + ns[1]) / max(0.2, 1 + ns[0].dot(ns[1]))
        out.append(p + m * d)
    return out


# ---------------------------------------------------------------- placing parts
class parca:
    """with parca(y, (x, y, z), aci=radians, olcek=1): faces added inside are built round the origin, then turned by
    aci about z, scaled and moved to konum"""

    def __init__(self, y, konum=(0, 0, 0), aci=0.0, olcek=1.0):
        self.y, self.k, self.a, self.s = y, Vector(konum), aci, olcek

    def __enter__(self):
        self.bas = len(self.y.faces)
        return self

    def __exit__(self, *e):
        c, s, k, o = math.cos(self.a), math.sin(self.a), self.k, self.s
        for i in range(self.bas, len(self.y.faces)):
            pts, key = self.y.faces[i]
            self.y.faces[i] = ([(k.x + o * (c * p[0] - s * p[1]), k.y + o * (s * p[0] + c * p[1]), k.z + o * p[2]) for p in pts], key)
        return False


def yuz_dis(y, pts, key, merkez):
    """a face wound to face away from the point merkez"""
    pts = [Vector(p) for p in pts]
    c = sum(pts, Vector()) / len(pts)
    y.yuz_yon(pts, key, c - Vector(merkez))


def iki_yuzlu(y, pts, key, yon, kil=0.0005):
    """a face toward yon and its back a hair (kil) behind it: a thin sheet that is seen from both sides (an exact
    reversed twin flickers in the preview's back-face check)"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    y.yuz_yon(pts, key, yon)
    y.yuz_yon([p - yon * kil for p in pts], key, -yon)


def kutu(y, o, ex, w, d, h, key, yuzler='onarkasagsolust'):
    """a box from o: w along ex (horizontal), d to its LEFT (Z x ex), h up. 'on' faces the right of ex"""
    ex = Vector(ex); ex.z = 0; ex.normalize()
    y.kutu(o, ex, Z.cross(ex), w, d, h, key, yuzler)


def kutu_merkez(y, c, w, d, h, key, z0=0.0, aci=0.0, yuzler='onarkasagsolust'):
    """a box centred on (c.x, c.y), w along the turned x axis, d along y"""
    ex = V(math.cos(aci), math.sin(aci)); ey = Z.cross(ex)
    o = V(c[0], c[1], z0) - ex * (w / 2) - ey * (d / 2)
    y.kutu(o, ex, ey, w, d, h, key, yuzler)


def duz_duvar(y, a, b, z0, z1, key='tas'):
    """a plain wall quad from a to b facing the right of a->b"""
    a, b = Vector(a), Vector(b)
    e = (b - a); e.z = 0; e.normalize()
    a = V(a.x, a.y); b = V(b.x, b.y)
    y.yuz_yon([a + Z * z0, b + Z * z0, b + Z * z1, a + Z * z1], key, V(e.y, -e.x))


def duvarlar(y, kose, z0, z1, key='tas', ust=None, kalinlik=0.0):
    """plain walls round a CCW polygon; ust: a top face (flat roof) of that key; kalinlik > 0: an inner face too"""
    n = len(kose)
    for i in range(n):
        duz_duvar(y, kose[i], kose[(i + 1) % n], z0, z1, key)
    if kalinlik:
        ic = disa(kose, -kalinlik)
        for i in range(n):
            duz_duvar(y, ic[(i + 1) % n], ic[i], z0, z1, key)
        for i in range(n):
            j = (i + 1) % n
            y.yuz_yon([kose[i] + Z * z1, kose[j] + Z * z1, ic[j] + Z * z1, ic[i] + Z * z1], ust or key, Z)
    elif ust:
        y.yuz_yon([V(p.x, p.y, z1) for p in kose], ust, Z)


def serit_yol(y, alt, ust, key, kapali=False):
    """a band of quads between two point lists (bottom row, top row), wound outward like Yapi.serit"""
    y.serit(alt, ust, key, kapali=kapali)


# ---------------------------------------------------------------- mouldings
SILME = {
    'duz':    [(0, 0), (1, 0), (1, 1), (0, 1)],                       # plain band (kornis)
    'kaba':   [(0, 0), (0.35, 0), (0.35, 0.3), (1, 0.62), (1, 1), (0, 1)],   # bed moulding + corona
    'tac':    [(0, 0), (0.3, 0.25), (0.55, 0.3), (0.55, 0.55), (1, 0.75), (1, 1), (0, 1)],   # crowning cornice
    'kaide':  [(1, 0), (1, 0.45), (0.5, 0.65), (0.5, 1), (0, 1)],      # plinth: wide foot, set back above
    'yarim':  [(0, 0)] + [(math.sin(math.pi * k / 6), 0.5 - 0.5 * math.cos(math.pi * k / 6)) for k in range(1, 6)] + [(0, 1)],   # torus
}


def silme(y, kose, z, h, c, key='tas_acik', profil='duz', kapali=True):
    """a moulding round a CCW polygon (kapali) or along an open polyline (faces the right), profile from SILME (or a
    list of (out 0..1, up 0..1)) scaled by c (projection) and h (height)"""
    pr = SILME[profil] if isinstance(profil, str) else profil
    rings = [[V(p.x, p.y, z + u * h) for p in disa(kose, o * c, kapali)] for o, u in pr]
    for k in range(len(rings) - 1):
        y.serit(rings[k], rings[k + 1], key, kapali=kapali)
    # the back (on the wall line), and the top / bottom back to it: closes the profile, so a moulding standing off
    # its wall or seen past a wall's end shows no open inside (on a wall it lies against the wall, facing into it)
    kap = ([(0, pr[-1][1])] if pr[-1][0] else []) + ([(0, pr[0][1])] if pr[0][0] else [])
    zr = [rings[-1]] + [[V(p.x, p.y, z + u * h) for p in disa(kose, o * c, kapali)] for o, u in kap] + [rings[0]]
    for k in range(len(zr) - 1):
        if abs(zr[k][0].z - zr[k + 1][0].z) + (zr[k][0] - zr[k + 1][0]).length > 1e-7:
            y.serit(zr[k], zr[k + 1], key, kapali=kapali)
    rings = rings + zr[1:-1]
    if not kapali:   # end caps
        for uc, yon in ((0, -1), (-1, 1)):
            pts = [r[uc] for r in rings]
            e = (kose[1] - kose[0]) if uc == 0 else (kose[-1] - kose[-2])
            e.z = 0
            if len(pts) >= 3: y.yuz_yon(pts, key, e * yon)


def kornis(y, x0, x1, y0, y1, z, h, c, key='tas_acik', profil='duz'):
    """a moulding round a rectangle"""
    silme(y, dikdortgen(x0, x1, y0, y1), z, h, c, key, profil)


def halka_kornis(y, c, r, z, h, c2, n, key='tas_acik', kat=0.0, profil='duz'):
    silme(y, cokgen(c, r, n, kat), z, h, c2, key, profil)


# ---------------------------------------------------------------- surfaces of revolution, tubes, spheres
def donel(y, c, profil, key, n=24, kat=0.0, dilim=None):
    """a surface of revolution round (c.x, c.y): profil = [(radius, z), ...] from bottom to top (outside). A last
    radius 0 closes the top in a point, a first radius 0 the bottom. dilim: list of keys for alternate meridian strips"""
    rings = [[V(c[0] + r * math.cos(kat + TAU * i / n), c[1] + r * math.sin(kat + TAU * i / n), zz) for i in range(n)] for r, zz in profil]
    kk = (lambda i: dilim[i % len(dilim)]) if dilim else (lambda i: key)
    for k in range(len(profil) - 1):
        r0, r1 = profil[k][0], profil[k + 1][0]
        A, B = rings[k], rings[k + 1]
        for i in range(n):
            j = (i + 1) % n
            if r1 < 1e-9 and r0 < 1e-9: continue
            if r1 < 1e-9: y.yuz([A[i], A[j], B[i]], kk(i))
            elif r0 < 1e-9: y.yuz([A[i], B[j], B[i]], kk(i))
            else: y.yuz([A[i], A[j], B[j], B[i]], kk(i))
    return Vector((c[0], c[1], profil[-1][1]))


def kure(y, c, r, key, n=12, kat=6, z=None):
    """a sphere (finial knob) centred at c (x, y, z)"""
    cz = c[2] if z is None else z
    pr = [(r * math.sin(math.pi * k / kat), cz - r * math.cos(math.pi * k / kat)) for k in range(kat + 1)]
    pr[0] = (0.0, pr[0][1]); pr[-1] = (0.0, pr[-1][1])
    donel(y, c, pr, key, n=n)


def boru(y, pts, r, key, n=6, kapat=True, r_son=None):
    """a tube along a polyline (railing, rope, rafter, finial horn); r_son: tapered end radius"""
    pts = [Vector(p) for p in pts]
    m = len(pts)
    rings = []
    for k in range(m):
        t = (pts[min(k + 1, m - 1)] - pts[max(k - 1, 0)]).normalized()
        u = Z.cross(t)
        if u.length < 1e-4: u = X.cross(t)
        u.normalize()
        if rings and u.dot(u0) < 0: u = -u   # (the frame must not flip where the tube turns past vertical: the quads twisted)
        u0 = u; w = t.cross(u)
        rr = r if r_son is None else r + (r_son - r) * k / (m - 1)
        rings.append([pts[k] + (u * math.cos(TAU * i / n) + w * math.sin(TAU * i / n)) * rr for i in range(n)])
    for k in range(m - 1):
        for i in range(n):
            j = (i + 1) % n
            q = [rings[k][i], rings[k + 1][i], rings[k + 1][j], rings[k][j]]
            yuz_dis(y, q, key, (pts[k] + pts[k + 1]) / 2)
    if kapat:
        y.yuz_yon(rings[0], key, pts[0] - pts[1])
        y.yuz_yon(rings[-1], key, pts[-1] - pts[-2])


def cubuk(y, a, b, en, key, kalin=None):
    """a square beam from a to b (en wide, kalin deep)"""
    a, b = Vector(a), Vector(b)
    t = (b - a).normalized()
    u = Z.cross(t)
    if u.length < 1e-4: u = X.copy()
    u.normalize(); w = t.cross(u).normalized()
    hw, hk = en / 2, (kalin or en) / 2
    k4 = [u * hw + w * hk, -u * hw + w * hk, -u * hw - w * hk, u * hw - w * hk]
    A = [a + q for q in k4]; B = [b + q for q in k4]
    for i in range(4):
        j = (i + 1) % 4
        yuz_dis(y, [A[i], A[j], B[j], B[i]], key, (a + b) / 2)
    y.yuz_yon(A, key, a - b); y.yuz_yon(B, key, b - a)


# ---------------------------------------------------------------- windows, doors, walls with openings
def pencereli_duvar(y, kose, z0, H, sayilar, kapali=True, **kw):
    """walls round a CCW polygon (or polyline), each side split into its count of arched bays (Yapi.kemerli);
    a count of 0 gives a plain wall. kw: renk (4 keys), v0, en, ust, derin, k_say, sivri, cerceve, korkuluk"""
    m = len(kose)
    for i, n in enumerate(sayilar):
        if not kapali and i >= m - 1: break
        a, b = kose[i], kose[(i + 1) % m]
        a = V(a.x, a.y); b = V(b.x, b.y)
        if n == 0:
            duz_duvar(y, a, b, z0, z0 + H, kw.get('renk', PENCERE)[0]); continue
        for k in range(n):
            y.kemerli(a.lerp(b, k / n), a.lerp(b, (k + 1) / n), z0, H, kw.get('renk', PENCERE),
                      v0=kw.get('v0', 0.03), en=kw.get('en', 0.45), ust=kw.get('ust', 0.03), derin=kw.get('derin', 0.025),
                      k_say=kw.get('k_say', 6), sivri=kw.get('sivri', 0.6), cerceve=kw.get('cerceve', (0.008, 'mermer')),
                      korkuluk=kw.get('korkuluk'))


def dikdortgen_acik(y, a, b, z0, H, u0, u1, v0, v1, renkler, derin=0.025, cerceve=None):
    """a wall bay a->b with a square-headed opening (window, door) from u0..u1 (0..1 along) and v0..v1 (height above
    z0): wall around it, the reveal faces, the dark (or wooden) back. cerceve = (width, key): a raised frame"""
    duvar, koyu, acik, delik = renkler
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v, d=0.0: a + e * (u * W) - nc * d + Z * (z0 + v)
    y.yuz_yon([L(0, 0), L(u0, 0), L(u0, H), L(0, H)], duvar, nc)
    y.yuz_yon([L(u1, 0), L(1, 0), L(1, H), L(u1, H)], duvar, nc)
    if v0 > 0: y.yuz_yon([L(u0, 0), L(u1, 0), L(u1, v0), L(u0, v0)], duvar, nc)
    y.yuz_yon([L(u0, v1), L(u1, v1), L(u1, H), L(u0, H)], duvar, nc)
    ic = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    for k in range(4):
        p, q = ic[k], ic[(k + 1) % 4]
        mid = L((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, derin / 2)
        merk = L((u0 + u1) / 2, (v0 + v1) / 2, derin / 2)
        y.yuz_yon([L(*p), L(*q), L(*q, derin), L(*p, derin)], acik if k == 0 else koyu, merk - mid)
    y.yuz_yon([L(u0, v0, derin), L(u1, v0, derin), L(u1, v1, derin), L(u0, v1, derin)], delik, nc)
    if cerceve:
        f, mk = cerceve; fu = f / W; d = -0.0025
        for (pu0, pv0, pu1, pv1) in ((u0 - fu, v0 - f, u0, v1 + f), (u1, v0 - f, u1 + fu, v1 + f), (u0, v1, u1, v1 + f), (u0, v0 - f, u1, v0)):
            y.yuz_yon([L(pu0, pv0, d), L(pu1, pv0, d), L(pu1, pv1, d), L(pu0, pv1, d)], mk, nc)
        # the frame's edges (top, sides) so it reads raised
        y.yuz_yon([L(u0 - fu, v1 + f, d), L(u1 + fu, v1 + f, d), L(u1 + fu, v1 + f, 0), L(u0 - fu, v1 + f, 0)], mk, Z)
        y.yuz_yon([L(u0 - fu, v0 - f, d), L(u0 - fu, v1 + f, d), L(u0 - fu, v1 + f, 0), L(u0 - fu, v0 - f, 0)], mk, -e)
        y.yuz_yon([L(u1 + fu, v0 - f, d), L(u1 + fu, v1 + f, d), L(u1 + fu, v1 + f, 0), L(u1 + fu, v0 - f, 0)], mk, e)
        y.yuz_yon([L(u0 - fu, v0 - f, d), L(u1 + fu, v0 - f, d), L(u1 + fu, v0 - f, 0), L(u0 - fu, v0 - f, 0)], mk, -Z)
    return W, e, nc, L


def kafes(y, a, b, z0, u0, u1, v0, v1, key='ahsap_koyu', nu=4, nv=3, en=0.004, ileri=0.004):
    """a lattice of thin bars in front of an opening (East Asian window, mashrabiya), a->b the wall line"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v: a + e * (u * W) + nc * (-ileri) + Z * (z0 + v)
    for i in range(1, nu):
        u = u0 + (u1 - u0) * i / nu
        du = en / 2 / W
        y.yuz_yon([L(u - du, v0), L(u + du, v0), L(u + du, v1), L(u - du, v1)], key, nc)
    for j in range(1, nv):
        v = v0 + (v1 - v0) * j / nv
        y.yuz_yon([L(u0, v - en / 2), L(u1, v - en / 2), L(u1, v + en / 2), L(u0, v + en / 2)], key, nc)


def yarik(y, o, ex, n, u, v, w, h, key='koyu'):
    """an arrow slit: a thin dark block set into the wall (o on the wall, ex along it, n out), standing a hair proud of
    it (a flat painted quad showed its back where it overhung a round tower's curve)"""
    o, ex, n = Vector(o), Vector(ex), Vector(n)
    ex.z = 0; ex.normalize(); n = V(n.x, n.y); n.normalize()
    if ex.cross(Z).dot(n) < 0:   # (kutu's front faces ex x Z: turn the run so it faces out)
        o = o + ex * (2 * u + w); ex = -ex
    d = 0.008
    kutu(y, o + ex * u + n * 0.0012 + Z * v, ex, w, d, h, key, 'onsagsolust')   # (front 0.0012 proud, d deep into the wall)


def kapi(y, a, b, z0, en, H, renkler=('tas', 'tas_koyu', 'tas_acik', 'ahsap'), sivri=0.0, derin=0.03, cerceve=None, k_say=8):
    """one bay a->b holding a door (arched; sivri > 0 pointed); the door leaf is renkler[3]"""
    return y.kemerli(V(a[0], a[1]), V(b[0], b[1]), z0, H, renkler, v0=0.0, en=en, ust=max(0.01, H * 0.08), derin=derin,
                     k_say=k_say, sivri=sivri, cerceve=cerceve)


# ---------------------------------------------------------------- columns, colonnades, pediments
def _yivli(c, r, n, z, oran=0.86):
    return [V(c[0] + (r if i % 2 == 0 else r * oran) * math.cos(TAU * i / n), c[1] + (r if i % 2 == 0 else r * oran) * math.sin(TAU * i / n), z) for i in range(n)]


def sutun(y, cx, cy, z0, z1, r=0.015, key='mermer', tur='osmanli', bas_key=None, bant_key=None, yiv=None):
    """a column from z0 to z1 (top of the capital). tur: osmanli (plain, block base and capital), dor, iyon, korint,
    toskan (Roman plain), misir (papyrus bundle with open bell capital; bant_key painted bands), pers (tall fluted,
    bell base, double-bull capital), ahsap (lacquered post on a stone disc). yiv: flute count of a dor / iyon / korint shaft
    (default 20 / 24; fewer for small, many columns). Returns z1"""
    bk = bas_key or key
    H = z1 - z0
    c = (cx, cy)
    if tur == 'osmanli':
        y.prizma(c, r, z0 + 0.012, z1 - 0.014, key, n=10, ust=False)
        y.kutu(V(cx - r * 1.45, cy - r * 1.45, z0), X, Y, r * 2.9, r * 2.9, 0.012, bk)
        y.kutu(V(cx - r * 1.45, cy - r * 1.45, z1 - 0.016), X, Y, r * 2.9, r * 2.9, 0.016, bk)
    elif tur in ('dor', 'iyon', 'korint', 'toskan'):
        hb = 0 if tur == 'dor' else H * 0.05           # base
        hc = H * (0.075 if tur in ('dor', 'toskan') else 0.09 if tur == 'iyon' else 0.13)
        za, zb = z0 + hb, z1 - hc
        if hb:
            donel(y, c, [(r * 1.42, z0), (r * 1.42, z0 + hb * 0.25), (r * 1.3, z0 + hb * 0.55), (r * 1.12, z0 + hb * 0.75), (r * 1.05, z0 + hb)], bk, n=20)
            y.yuz_yon(cokgen(c, r * 1.05, 20, z=z0 + hb), bk, Z)   # the base's top round the shaft's foot (else a back-face ring)
        # shaft with entasis, fluted (Greek) or plain (Toscan)
        nk = 6
        nf = 0 if tur == 'toskan' else (yiv or (20 if tur == 'dor' else 24))
        prev = None
        for k in range(nk + 1):
            t = k / nk
            rr = r * (1 - 0.16 * t + 0.05 * math.sin(math.pi * t))
            ring = _yivli(c, rr, nf, za + (zb - za) * t) if nf else [V(c[0] + rr * math.cos(TAU * i / 16), c[1] + rr * math.sin(TAU * i / 16), za + (zb - za) * t) for i in range(16)]
            if prev: y.serit(prev, ring, key)
            prev = ring
        rt = r * 0.89
        if tur in ('dor', 'toskan'):
            donel(y, c, [(rt, zb), (rt * 1.04, zb + hc * 0.15), (r * 1.32, zb + hc * 0.5), (r * 1.36, zb + hc * 0.55)], bk, n=20)
            kutu_merkez(y, c, r * 2.9, r * 2.9, hc * 0.45, bk, z0=zb + hc * 0.55)
        elif tur == 'iyon':
            donel(y, c, [(rt, zb), (r * 1.1, zb + hc * 0.45)], bk, n=20)
            kutu_merkez(y, c, r * 2.6, r * 2.1, hc * 0.3, bk, z0=zb + hc * 0.4)
            kutu_merkez(y, c, r * 2.5, r * 2.5, hc * 0.3, bk, z0=zb + hc * 0.7)
            for s in (-1, 1):   # volutes: short rolls at either side (seen front and back)
                zc = zb + hc * 0.38
                boru(y, [V(cx + s * r * 1.25, cy - r * 1.15, zc), V(cx + s * r * 1.25, cy + r * 1.15, zc)], r * 0.42, bk, n=10)
        else:   # korint: a bell wrapped in two rows of leaves, a concave abacus
            donel(y, c, [(rt, zb), (rt * 1.02, zb + hc * 0.3), (r * 1.1, zb + hc * 0.65), (r * 1.3, zb + hc * 0.82)], bk, n=20)
            for row, (h0, h1, rr) in enumerate(((0.0, 0.42, 1.0), (0.25, 0.68, 1.06))):
                for i in range(8):
                    a = TAU * (i + 0.5 * row) / 8
                    d = V(math.cos(a), math.sin(a)); t = V(-d.y, d.x)
                    p0 = V(cx, cy) + d * (rt * rr * 1.01)
                    w = r * 0.42
                    tip = p0 + d * (r * 0.32)
                    yp = [p0 - t * w + Z * (zb + hc * h0), p0 + t * w + Z * (zb + hc * h0), tip + t * w * 0.7 + Z * (zb + hc * h1), tip - t * w * 0.7 + Z * (zb + hc * h1)]
                    y.yuz_yon(yp, bk, d)
                    y.yuz_yon([q - d * 0.0005 for q in yp[::-1]], bk, -d)   # (two-sided: a leaf is seen from behind; the back a hair in, or the welder drops it)
            kutu_merkez(y, c, r * 2.8, r * 2.8, hc * 0.18, bk, z0=zb + hc * 0.82)
    elif tur == 'misir':
        hc = H * 0.2
        zb = z1 - hc
        donel(y, c, [(r * 1.35, z0), (r * 1.35, z0 + H * 0.03), (r * 1.15, z0 + H * 0.045), (r * 0.7, z0 + H * 0.045)], bk, n=16)   # (closed: the disc's top round the shaft's foot)
        # bundle shaft: 8 lobes, narrowing at the foot
        prev = None
        for k, t in enumerate((0, 0.06, 0.2, 0.6, 1.0)):
            rr = r * (0.88 + 0.12 * min(1, t / 0.2)) * (1 - 0.08 * t)
            ring = [V(cx + rr * (1 if i % 2 == 0 else 0.84) * math.cos(TAU * i / 16), cy + rr * (1 if i % 2 == 0 else 0.84) * math.sin(TAU * i / 16), z0 + H * 0.045 + (zb - z0 - H * 0.045) * t) for i in range(16)]
            if prev: y.serit(prev, ring, key)
            prev = ring
        # (the shaft's top: its lobes stand out past the bell's foot, the open tube showed from above)
        for i in range(16):
            y.yuz_yon([V(cx, cy, prev[i].z), prev[i], prev[(i + 1) % 16]], key, Z)
        for j in range(3):   # tie bands under the capital
            zz = zb - H * 0.06 + j * H * 0.022
            halka_kornis(y, c, r * 0.9, zz, H * 0.012, r * 0.12, 16, bant_key or bk)
        # open papyrus capital (bell), painted lobes
        donel(y, c, [(r * 0.82, zb), (r * 1.15, zb + hc * 0.45), (r * 1.55, zb + hc * 0.85), (r * 1.62, zb + hc * 0.9)], bk, n=16,
              dilim=[bk, bant_key] if bant_key else None)
        y.yuz_yon(cokgen(c, r * 1.62, 16, z=zb + hc * 0.9), bk, Z)   # the bell's top (seen from above when free-standing)
        kutu_merkez(y, c, r * 1.7, r * 1.7, hc * 0.1, bk, z0=zb + hc * 0.9)
    elif tur == 'pers':
        hc = H * 0.14
        zb = z1 - hc
        donel(y, c, [(r * 1.7, z0), (r * 1.6, z0 + H * 0.02), (r * 1.2, z0 + H * 0.06), (r * 1.05, z0 + H * 0.08)], bk, n=20)   # bell base
        prev = None
        for k in range(5):
            t = k / 4
            ring = _yivli(c, r * (1 - 0.08 * t), 32, z0 + H * 0.08 + (zb - z0 - H * 0.08) * t, 0.9)
            if prev: y.serit(prev, ring, key)
            prev = ring
        donel(y, c, [(r * 0.95, zb), (r * 1.25, zb + hc * 0.3), (r * 1.2, zb + hc * 0.45)], bk, n=16)
        # the double bull: a block with two rounded fore-parts
        kutu_merkez(y, c, r * 5.0, r * 1.6, hc * 0.38, bk, z0=zb + hc * 0.45)
        for s in (-1, 1):
            boru(y, [V(cx + s * r * 1.6, cy - r * 0.8, zb + hc * 0.64), V(cx + s * r * 1.6, cy + r * 0.8, zb + hc * 0.64)], hc * 0.22, bk, n=10)
            kutu_merkez(y, (cx + s * r * 2.3, cy), r * 0.5, r * 1.0, hc * 0.35, bk, z0=zb + hc * 0.15)   # the bent legs
        kutu_merkez(y, c, r * 5.4, r * 2.0, hc * 0.17, bk, z0=zb + hc * 0.83)
    elif tur == 'ahsap':
        donel(y, c, [(r * 1.6, z0), (r * 1.6, z0 + H * 0.03), (r * 1.25, z0 + H * 0.05)], bas_key or 'tas', n=12)
        y.prizma(c, r, z0 + H * 0.05, z1, key, n=12, ust=True)
    return z1


def saciklik(i, n):   # helper: positions 0..n
    return i / n


def sutunlu_revak(y, a, b, n, z0, H, tur='dor', r=None, key='mermer', ust_key=None, triglif=None, derin=None, kornis_c=None):
    """a straight colonnade a->b (column centre line; faces the right of a->b): n bays (n + 1 columns) and the
    entablature (architrave, frieze, cornice). triglif: key of the Doric triglyphs (None: plain frieze). Returns the top z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    r = r or min(0.03, W / n * 0.16)
    uk = ust_key or key
    for i in range(n + 1):
        p = a.lerp(b, i / n)
        sutun(y, p.x, p.y, z0, z0 + H, r, key, tur)
    he = H * 0.26
    D = derin or r * 3.2
    z = z0 + H
    o = a - e * (r * 1.6) + nc * (D / 2)
    L = W + r * 3.2
    oz = o + Z * z                                             # (the entablature stands on the capitals)
    kutu(y, oz, e, L, D, he * 0.42, uk)                        # architrave
    kutu(y, oz + Z * (he * 0.42) - nc * 0.002, e, L, D - 0.004, he * 0.4, uk)   # frieze (set back a hair)
    if triglif:
        k = n * 2
        for i in range(k + 1):
            p = oz + e * (r * 1.6 + W * i / k) + Z * (he * 0.42)
            kutu(y, p - e * (r * 0.45) + nc * 0.0005, e, r * 0.9, 0.004, he * 0.4, triglif, 'onsagsolust')
    zc = z + he * 0.82
    c = kornis_c or r * 0.9
    silme(y, [o + Z * 0, o + e * L], zc, he * 0.18, c, uk, 'tac', kapali=False)
    silme(y, [o + e * L - nc * D, o - nc * D], zc, he * 0.18, c, uk, 'tac', kapali=False)
    y.yuz_yon([o + Z * (zc + he * 0.18), o + e * L + Z * (zc + he * 0.18), o + e * L - nc * D + Z * (zc + he * 0.18), o - nc * D + Z * (zc + he * 0.18)], uk, Z)
    return zc + he * 0.18


def peristil(y, x0, x1, y0, y1, nx, ny, z0, H, tur='dor', r=None, key='mermer', triglif=None):
    """columns all round a rectangle (Greek temple peristyle) with a continuous entablature; returns the top z"""
    r = r or min(0.03, (x1 - x0) / nx * 0.16)
    sx, sy = (x1 - x0) / nx, (y1 - y0) / ny
    pts = [V(x0 + sx * i, y0) for i in range(nx)] + [V(x1, y0 + sy * j) for j in range(ny)] + \
          [V(x1 - sx * i, y1) for i in range(nx)] + [V(x0, y1 - sy * j) for j in range(ny)]
    for p in pts:
        sutun(y, p.x, p.y, z0, z0 + H, r, key, tur)
    he = H * 0.26
    z = z0 + H
    dk = dikdortgen(x0, x1, y0, y1)
    D = r * 1.7
    dis_ = disa(dk, D); ic = disa(dk, -D)
    duvarlar(y, dis_, z, z + he * 0.42, key)
    duvarlar(y, [V(p.x, p.y) for p in disa(dk, D - 0.003)], z + he * 0.42, z + he * 0.82, key)
    for i in range(4):   # soffit under the architrave
        j = (i + 1) % 4
        y.yuz_yon([dis_[i] + Z * z, dis_[j] + Z * z, ic[j] + Z * z, ic[i] + Z * z], key, -Z)
    if triglif:
        for i in range(4):
            p, q = disa(dk, D - 0.003)[i], disa(dk, D - 0.003)[(i + 1) % 4]
            L = (q - p).length; e = (q - p) / L; nc = V(e.y, -e.x)
            k = max(2, int(round(L / (sx / 2))))
            for m in range(k + 1):
                cc = p.lerp(q, m / k)
                kutu(y, cc - e * (r * 0.45) + Z * (z + he * 0.42) + nc * 0.0005, e, r * 0.9, 0.004, he * 0.4, triglif, 'onsagsolust')
    silme(y, disa(dk, D - 0.003), z + he * 0.82, he * 0.2, r * 0.9, key, 'tac')
    # the entablature's inner face (towards the cella) and its top: seen from above and from the back they were open
    fz = disa(dk, D - 0.003)
    for i in range(4):
        j = (i + 1) % 4
        duz_duvar(y, ic[j], ic[i], z, z + he * 1.02, key)
        y.yuz_yon([fz[i] + Z * (z + he * 1.02), fz[j] + Z * (z + he * 1.02), ic[j] + Z * (z + he * 1.02), ic[i] + Z * (z + he * 1.02)], key, Z)
    return z + he * 1.02


def alinlik(y, a, b, z, h, derin=0.06, key='mermer', ic_key=None, c=0.012, cati_key=None):
    """a pediment over the front a->b (faces the right of a->b) at height z, h high: the raking cornices, the
    recessed tympanum, the horizontal cornice, and the roof slopes behind it running derin back (cati_key)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    m = (a + b) / 2
    T = m + Z * (z + h)
    A, B = a + Z * z, b + Z * z
    ik = ic_key or key
    # tympanum (set back), the raking cornice frame in front
    s = c * 1.6
    Ai, Bi = A + e * (s * 1.6) + Z * s, B - e * (s * 1.6) + Z * s
    Ti = T - Z * (s * 1.9)
    y.yuz_yon([Ai - nc * 0.006, Bi - nc * 0.006, Ti - nc * 0.006], ik, nc)
    # frame: three bands round the tympanum (front faces) and their reveals
    for p, q, pi, qi in ((A, B, Ai, Bi), (B, T, Bi, Ti), (T, A, Ti, Ai)):
        y.yuz_yon([p, q, qi, pi], key, nc)
        y.yuz_yon([pi, qi, qi - nc * 0.006, pi - nc * 0.006], key, ((pi + qi) / 2 - (p + q) / 2))   # (faces the tympanum: the reveal round the recess)
    # the raking cornices project (front lip)
    for p, q in ((B, T), (T, A)):
        d = (q - p).normalized()
        out = nc * c
        lift = (Z - d * d.z).normalized() * (c * 0.8)
        y.yuz_yon([p + out, q + out, q + out + lift, p + out + lift], key, nc)
        y.yuz_yon([p, q, q + out, p + out], key, -(lift))
        y.yuz_yon([p + lift, q + lift, q + out + lift, p + out + lift], key, lift)
        y.yuz_yon([p, q, q + lift, p + lift], key, -nc)   # (its back: seen past the roof's end)    # roof slopes and the back gable
    D = -nc * derin
    ck = cati_key or key
    for p, q in ((A, T), (T, B)):
        n_out = (q - p).cross(D)
        y.yuz_yon([p + Z * (c * 0.8), q + Z * (c * 0.8), q + D + Z * (c * 0.8), p + D + Z * (c * 0.8)], ck, Z)
    y.yuz_yon([A + D, B + D, T + D], key, -nc)
    y.yuz_yon([A, A + D, A + D + Z * (c * 0.8), A + Z * (c * 0.8)], key, -e)
    y.yuz_yon([B, B + D, B + D + Z * (c * 0.8), B + Z * (c * 0.8)], key, e)
    return T.z


# ---------------------------------------------------------------- arcades (Ottoman / Roman)
def arkad(y, a, b, n, z0, H, en=0.8, ust=0.03, sivri=0.5, derin=0.1, korkuluk=None, cerceve=(0.011, ['mermer', 'kirmizi']),
          son_sutun=True, renk=REVAK, sutun_key='mermer', sutun_tur='osmanli', sutun_r=0.015, sutunlu=True):
    """an open arcade from a to b (facing the right of a->b): arches (pointed if sivri > 0, round if 0) on columns"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        W = (q - p).length
        y.kemerli(p + Z * z0, q + Z * z0, 0, H, renk, en=en, ust=ust, derin=derin, k_say=10, sivri=sivri, korkuluk=korkuluk, cerceve=cerceve)
        hs = H - ust - (sivri * en * W if sivri else en * W / 2)
        e = (q - p).normalized(); nc = V(e.y, -e.x)
        if sutunlu:
            for u in ([0.0, 1.0] if (i == n - 1 and son_sutun) else [0.0]):
                cc = p.lerp(q, u) + nc * 0.016
                sutun(y, cc.x, cc.y, z0, z0 + hs, sutun_r, sutun_key, sutun_tur)


def kemer_dizisi(y, a, b, n, z0, H, kalinlik, renk=('tas', 'tas_koyu', 'tas_acik', 'tas_koyu'), en=0.62, ust=0.05, sivri=0.0,
                 ayak_key=None, acik=False, taban=True):
    """a free-standing row of arches (aqueduct tier, viaduct, open gallery) with real depth: the arched front a->b,
    the same arches on the back, piers between, the soffits of the arches and a top. Returns the top z.
    acik: no dark plate at the back of the openings (see-through arches, a bridge); taban=False: no floor face in
    the passages (the tier stands on something that already shows a top there: no z-fighting)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    on, k_, ac, dl = renk
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        # front and back: openings through the whole thickness (the back opening is the front's reveal end)
        y.kemerli(p, q, z0, H, (on, k_, ac, dl), v0=0.0, en=en, ust=ust, derin=kalinlik, k_say=10, sivri=sivri)
        # kemerli's last two faces: the passage floor, then the back plate
        if acik: y.faces.pop()
        if not taban: y.faces.pop(-1 if acik else -2)
    # back face: a second set facing the other way, reveals short (they meet the front's), no back plate
    pb, qb = b - nc * kalinlik, a - nc * kalinlik
    for i in range(n):
        p, q = pb.lerp(qb, i / n), pb.lerp(qb, (i + 1) / n)
        _kemer_yuzu(y, p, q, z0, H, en, ust, sivri, on)
    y.yuz_yon([a + Z * (z0 + H), b + Z * (z0 + H), b - nc * kalinlik + Z * (z0 + H), a - nc * kalinlik + Z * (z0 + H)], ac, Z)
    for p, s in ((a, -1), (b, 1)):
        y.yuz_yon([p + Z * z0, p - nc * kalinlik + Z * z0, p - nc * kalinlik + Z * (z0 + H), p + Z * (z0 + H)], on, e * s)
    return z0 + H


def _kemer_yuzu(y, a, b, z0, H, en, ust, sivri, key, k_say=10):
    """only the wall face round a through-arch (no reveal, no back): the back side of a kemer_dizisi"""
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v: a + e * u + Z * (z0 + v)
    x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
    R = (x1 - x0) / 2
    if sivri:
        w = x1 - x0; hr = sivri * w; hs = H - ust - hr
        rho = (w * w / 4 + hr * hr) / w; c = x0 + rho
        ta = math.atan2(hr, (x0 + w / 2) - c); yari = k_say // 2
        sol = [(c + rho * math.cos(math.pi - (math.pi - ta) * k / yari), hs + rho * math.sin(math.pi - (math.pi - ta) * k / yari)) for k in range(1, yari + 1)]
        kemer = sol + [(x0 + x1 - u, v) for u, v in reversed(sol[:-1])]
    else:
        hs = H - ust - R
        kemer = [(x0 + R + R * math.cos(math.pi - math.pi * k / k_say), hs + R * math.sin(math.pi - math.pi * k / k_say)) for k in range(1, k_say)]
    y.yuz_yon([L(0, 0), L(x0, 0), L(x0, H), L(0, H)], key, nc)
    y.yuz_yon([L(x1, 0), L(W, 0), L(W, H), L(x1, H)], key, nc)
    tp = [(x0, hs)] + kemer + [(x1, hs)]
    for k in range(len(tp) - 1):
        (ua, va), (ub, vb) = tp[k], tp[k + 1]
        y.yuz_yon([L(ua, va), L(ub, vb), L(ub, H), L(ua, H)], key, nc)


# ---------------------------------------------------------------- domes, finials, minarets (Ottoman / Islamic)
def alem(y, cx, cy, z, olcek=1.0, key='altin', hilal=True):
    """a finial: rod, knobs and (hilal) a crescent"""
    s = olcek
    y.prizma((cx, cy), 0.005 * s, z, z + 0.03 * s, key, n=6)
    y.kubbe((cx, cy), 0.012 * s, z + 0.03 * s, 0.012 * s, key, n=8, kat=3)
    y.prizma((cx, cy), 0.003 * s, z + 0.04 * s, z + 0.07 * s, key, n=4)
    if hilal:
        pts = [V(cx, cy + 0.0, z + 0.082 * s + 0.014 * s * math.cos(math.pi * k / 6)) + V(0.014 * s * math.sin(math.pi * k / 6), 0) for k in range(7)]
        boru(y, pts, 0.0022 * s, key, n=4)
    return z + 0.1 * s


def kucuk_kubbe(y, cx, cy, z, r, kasnak=0.025, n=28, son=True, key='kursun', kasnak_key='tas'):
    """a small dome on a low drum with a moulding, and an alem"""
    y.prizma((cx, cy), r * 1.02, z, z + kasnak, kasnak_key, n=28, ust=False)
    halka_kornis(y, (cx, cy), r * 1.02, z + kasnak - 0.006, 0.006, 0.006, 28)
    t = y.kubbe((cx, cy), r, z + kasnak, r * 0.9, key, n=n, kat=8)
    if son: alem(y, cx, cy, t.z, 0.7)
    return t.z


def kubbe_kasnakli(y, c, r, z, kasnak_h, n_pencere=16, kubbe_h=None, key='kursun', duvar=PENCERE, payanda=True, alem_olcek=1.2,
                   sivri=0.5, n=64, kat=18, en=0.5, cerceve=(0.005, 'mermer')):
    """a dome on a windowed drum: n_pencere arched windows round a polygonal drum, buttresses between, a moulding,
    the dome (lead sheets if key='kursun'), an alem. Returns the top z"""
    dk = cokgen(c, r, n_pencere)
    for i in range(n_pencere):
        y.kemerli(dk[i], dk[(i + 1) % n_pencere], z, kasnak_h, duvar, v0=kasnak_h * 0.2, en=en, ust=kasnak_h * 0.15, derin=0.02,
                  k_say=4, sivri=sivri, cerceve=cerceve)
    if payanda:
        for i in range(n_pencere):
            a = math.atan2(dk[i].y - c[1], dk[i].x - c[0])
            e = V(-math.sin(a), math.cos(a)); nn = V(math.cos(a), math.sin(a))
            w = min(0.024, TAU * r / n_pencere * 0.25)
            o = dk[i] - e * (w / 2) + nn * (w * 0.8)
            y.kutu(o + Z * z, e, -nn, w, w * 0.85, kasnak_h * 0.92, duvar[2], 'onsagsolust')
    halka_kornis(y, c, r, z + kasnak_h, 0.016, 0.02, n_pencere)
    y.prizma(c, r, z + kasnak_h + 0.016, z + kasnak_h + 0.017, 'tas_acik', n=n_pencere)
    tepe = y.kubbe(c, r + 0.005, z + kasnak_h + 0.016, kubbe_h or r * 0.86, key, n=n, kat=kat)
    if alem_olcek: alem(y, c[0], c[1], tepe.z, alem_olcek)
    return tepe.z


def yarim_kubbe(y, c, R, z, aci, kasnak_h=0.1, kubbe_h=None, n_pencere=8, key='kursun', duvar=PENCERE, kapak='tas'):
    """a half dome bulging towards angle aci (radians; -pi/2 = towards -y) on a windowed half drum"""
    t0 = aci - math.pi / 2
    yay = [V(c[0] + R * math.cos(t0 + math.pi * i / n_pencere), c[1] + R * math.sin(t0 + math.pi * i / n_pencere)) for i in range(n_pencere + 1)]
    for i in range(n_pencere):
        y.kemerli(yay[i], yay[i + 1], z, kasnak_h, duvar, v0=kasnak_h * 0.22, en=0.45, ust=kasnak_h * 0.18, derin=0.02, k_say=4, sivri=0.5)
    zh = z + kasnak_h
    hy = lambda rr, zz: [V(c[0] + rr * math.cos(t0 + math.pi * i / n_pencere), c[1] + rr * math.sin(t0 + math.pi * i / n_pencere), zz) for i in range(n_pencere + 1)]
    y.serit(hy(R, zh), hy(R + 0.01, zh), 'tas_acik', kapali=False)
    y.serit(hy(R + 0.01, zh), hy(R + 0.01, zh + 0.01), 'tas_acik', kapali=False)
    y.serit(hy(R + 0.01, zh + 0.01), hy(R + 0.003, zh + 0.01), 'tas_acik', kapali=False)   # (the moulding's top: left open, its underside showed from above)
    y.kubbe(c, R + 0.005, zh + 0.01, kubbe_h or R * 0.74, key, n=48, kat=14, t0=t0, t1=t0 + math.pi, kapak=kapak)
    return zh + 0.01 + (kubbe_h or R * 0.74)


def sogan_kubbe(y, c, r, z, h=None, key='altin', n=32, boyun=0.35, sivri=0.25, dilim=None):
    """an onion dome (Russian, Mughal): neck radius boyun x r, bulging to ~1.12 r, drawn to a point; dilim: list of
    keys for the striped Russian domes (twisted stripes are not modelled). Returns the tip z"""
    h = h or r * 1.7
    pr = [(r * boyun * 1.6, z), (r * 0.95, z + h * 0.06), (r * 1.12, z + h * 0.24), (r * 1.1, z + h * 0.36), (r * 0.92, z + h * 0.5),
          (r * 0.62, z + h * 0.64), (r * 0.34, z + h * 0.77), (r * 0.14, z + h * (0.88 - sivri * 0.1)), (r * 0.05, z + h * 0.95), (0, z + h)]
    donel(y, c, pr, key, n=n, dilim=dilim)
    return z + h


def minare(y, cx, cy, z0, boy, serefe=2, kaide=0.2, r=0.036, key='tas', govde_key='tas_acik', cati_key='kursun', kare=True):
    """an Ottoman minaret: square base to kaide height, a fluted shaft, serefe corbelled balconies, the petek, a
    pencil cap and an alem. Returns the tip z"""
    zt = z0 + kaide
    if kare:
        y.kutu((cx - r * 1.67, cy - r * 1.67, z0), X, Y, r * 3.33, r * 3.33, kaide, key)
        kornis(y, cx - r * 1.67, cx + r * 1.67, cy - r * 1.67, cy + r * 1.67, zt - 0.01, 0.012, 0.008)
    y.prizma((cx, cy), r * 1.45, zt, zt + 0.03, key, n=8, kat=math.pi / 8)
    top = z0 + boy
    yiv = lambda zq: [V(cx + (r if i % 2 == 0 else r * 0.89) * math.cos(TAU * i / 24), cy + (r if i % 2 == 0 else r * 0.89) * math.sin(TAU * i / 24), zq) for i in range(24)]
    y.serit(yiv(zt + 0.03), yiv(top - 0.07), govde_key)
    y.prizma((cx, cy), r * 1.05, top - 0.07, top, govde_key, n=16, ust=False)
    for k in range(serefe):
        zz = zt + 0.03 + (top - zt - 0.12) * (k + 1) / (serefe + 0.25)
        for j, (rr, hh) in enumerate(((r * 1.17, 0.01), (r * 1.39, 0.01), (r * 1.61, 0.008))):
            y.prizma((cx, cy), rr, zz - 0.028 + j * 0.01, zz - 0.028 + j * 0.01 + hh, key, n=16, ust=False)
            y.serit([V(cx + rr * math.cos(TAU * i / 16), cy + rr * math.sin(TAU * i / 16), zz - 0.028 + j * 0.01) for i in range(16)],
                    [V(cx + (rr - 0.008) * math.cos(TAU * i / 16), cy + (rr - 0.008) * math.sin(TAU * i / 16), zz - 0.028 + j * 0.01) for i in range(16)], 'tas_koyu')
        y.prizma((cx, cy), r * 1.72, zz - 0.004, zz, 'tas_acik', n=16)
        dis = lambda zq: [V(cx + r * 1.67 * math.cos(TAU * i / 16), cy + r * 1.67 * math.sin(TAU * i / 16), zq) for i in range(16)]
        ic = lambda zq: [V(cx + r * 1.56 * math.cos(TAU * i / 16), cy + r * 1.56 * math.sin(TAU * i / 16), zq) for i in range(16)]
        y.serit(dis(zz), dis(zz + 0.02), 'tas_acik')
        y.serit(ic(zz + 0.02), ic(zz), 'tas_acik')
        y.serit(dis(zz + 0.02), ic(zz + 0.02), 'tas_acik')
    halka_kornis(y, (cx, cy), r, top - 0.004, 0.008, 0.006, 16)
    y.koni((cx, cy), r * 1.11, top + 0.004, boy * 0.18, cati_key, n=24)
    return alem(y, cx, cy, top + 0.004 + boy * 0.18, 0.8)


def sadirvan(y, cx, cy, z0, olcek=1.0):
    """an ablution fountain kiosk: octagonal basin, eight posts, a wide lead eave and a small dome"""
    s = olcek
    y.prizma((cx, cy), 0.08 * s, z0, z0 + 0.035 * s, 'mermer', n=8, kat=math.pi / 8)
    for k in range(8):
        a = math.pi / 8 + TAU * k / 8
        y.prizma((cx + 0.065 * s * math.cos(a), cy + 0.065 * s * math.sin(a)), 0.006 * s, z0 + 0.035 * s, z0 + 0.11 * s, 'mermer', n=6, ust=False)
    y.prizma((cx, cy), 0.105 * s, z0 + 0.11 * s, z0 + 0.122 * s, 'kursun', n=8, kat=math.pi / 8)
    t = y.kubbe((cx, cy), 0.065 * s, z0 + 0.122 * s, 0.06 * s, 'kursun', n=28, kat=8)
    alem(y, cx, cy, t.z, 0.8 * s)


def tackapi(y, cx, cy, z0, en=0.28, H=0.31, derin=0.07, kapi_key='ahsap', cerceve=(0.014, ['mermer', 'kirmizi']), kuleli=True):
    """a monumental portal (pishtaq) on the line y = cy, facing -y: a tall pointed niche with a framed arch, side
    pilasters with small cones, a cornice. Returns the top z"""
    y0, y1 = cy - derin / 2, cy + derin / 2
    y.kemerli(V(cx - en / 2, y0, 0), V(cx + en / 2, y0, 0), z0, H, ('tas', 'tas_koyu', 'tas_acik', kapi_key), v0=0.0, en=0.6, ust=0.05,
              derin=derin * 0.48, k_say=10, sivri=0.6, cerceve=cerceve)
    y.kutu((cx - en / 2, y0, z0), X, Y, en, y1 - y0, H, 'tas', 'sagsol')
    kornis(y, cx - en / 2, cx + en / 2, y0, y1, z0 + H - 0.014, 0.016, 0.012)
    y.yuz([V(cx - en / 2, y0, z0 + H), V(cx + en / 2, y0, z0 + H), V(cx + en / 2, y1, z0 + H), V(cx - en / 2, y1, z0 + H)], 'tas_acik')
    duz_duvar(y, V(cx + en / 2, y1), V(cx - en / 2, y1), z0, z0 + H, 'tas')   # (its back: open when the portal stands proud of a wall)
    if kuleli:
        for sx in (-1, 1):
            y.kutu((cx + sx * en / 2 - 0.02, y0 - 0.01, z0), X, Y, 0.04, 0.04, H + 0.03, 'tas_acik')
            y.koni((cx + sx * en / 2, y0 + 0.01), 0.02, z0 + H + 0.03, 0.04, 'kursun', n=8)
    return z0 + H


# ---------------------------------------------------------------- fortification
def mazgal(y, a, b, z, h, kalinlik=0.02, key='tas', dis_en=None, bosluk=None, uclar=True):
    """merlons along a->b (their outer face on the line, facing the right), h high, kalinlik deep: real boxes with
    gaps between. dis_en: merlon width (default ~1.2 h), bosluk: gap width (default ~0.8 h)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-6: return
    e = (b - a) / L
    w = dis_en or h * 1.2; g = bosluk or h * 0.8
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g if uclar else w
    if w <= 0: return
    for i in range(k):
        u = i * (w + g)
        kutu(y, a + e * u + Z * z, e, min(w, L - u), kalinlik, h, key)


def parapet(y, kose, z, h_dolu, h_dis, kalinlik=0.02, key='tas', kapali=True, ust_key=None):
    """a parapet along a CCW polygon (or polyline) on the outer edge: a solid band h_dolu high (outer, inner and top
    faces) and merlons h_dis above it"""
    ic = disa(kose, -kalinlik, kapali)
    n = len(kose)
    for i in range(n if kapali else n - 1):
        j = (i + 1) % n
        a, b, ai, bi = kose[i], kose[j], ic[i], ic[j]
        duz_duvar(y, a, b, z, z + h_dolu, key)
        duz_duvar(y, bi, ai, z, z + h_dolu, key)
        y.yuz_yon([V(a.x, a.y, z + h_dolu), V(b.x, b.y, z + h_dolu), V(bi.x, bi.y, z + h_dolu), V(ai.x, ai.y, z + h_dolu)], ust_key or key, Z)
        if h_dis:
            mazgal(y, a, b, z + h_dolu, h_dis, kalinlik, key)
    if not kapali:
        for i, s in ((0, -1), (n - 1, 1)):
            p, q = kose[i], ic[i]
            e = (kose[1] - kose[0]) if i == 0 else (kose[-1] - kose[-2]); e.z = 0
            y.yuz_yon([V(p.x, p.y, z), V(q.x, q.y, z), V(q.x, q.y, z + h_dolu), V(p.x, p.y, z + h_dolu)], key, e * s)


def konsol_halka(y, kose, z, h, c, key='tas', adim=3, kapali=True):
    """corbelling (machicolation look): adim stepped mouldings, each projecting further, ending at c"""
    for k in range(adim):
        silme(y, kose, z + h * k / adim, h / adim, c * (k + 1) / adim, key, 'duz', kapali)


def sur(y, yol, z0, h, kalinlik=0.06, key='tas', kapali=False, mazgal_h=0.03, parapet_h=0.012, ust_key=None, ic=True,
        konsol=False):
    """a curtain wall along a polyline (or closed CCW polygon): the outer face on the right of the travel, the inner
    face kalinlik to the left, the wall walk on top with a merloned parapet on the outer edge, end faces if open.
    konsol: a corbelled lip under the parapet"""
    yol = [V(p[0], p[1]) for p in yol]
    n = len(yol)
    icy = disa(yol, -kalinlik, kapali)
    m = n if kapali else n - 1
    for i in range(m):
        j = (i + 1) % n
        duz_duvar(y, yol[i], yol[j], z0, z0 + h, key)
        if ic: duz_duvar(y, icy[j], icy[i], z0, z0 + h, key)
        y.yuz_yon([yol[i] + Z * (z0 + h), yol[j] + Z * (z0 + h), icy[j] + Z * (z0 + h), icy[i] + Z * (z0 + h)], ust_key or 'zemin', Z)
    if not kapali:
        for i, s in ((0, -1), (n - 1, 1)):
            e = (yol[1] - yol[0]) if i == 0 else (yol[-1] - yol[-2])
            y.yuz_yon([yol[i] + Z * z0, icy[i] + Z * z0, icy[i] + Z * (z0 + h), yol[i] + Z * (z0 + h)], key, e * s)
    zt = z0 + h
    if konsol:
        konsol_halka(y, yol, zt - 0.03, 0.03, 0.012, key, 3, kapali)
        dis_ = disa(yol, 0.012, kapali)
        parapet(y, dis_, zt, parapet_h, mazgal_h, 0.012 + kalinlik * 0.3, key, kapali)
    else:
        parapet(y, yol, zt, parapet_h, mazgal_h, kalinlik * 0.3, key, kapali)
    return zt


def kule_yuvarlak(y, c, r, z0, h, key='tas', cati='konik', cati_key='kiremit', cati_h=None, mazgal_h=0.03, n=24, egim=0.06,
                  sacak=0.012, yarik_say=3, konsol=True, sivri=None, ust_kat=None, bolum=1):
    """a round tower: a slightly battered shaft (egim: bottom radius r * (1 + egim)), arrow slits, a corbelled
    parapet with merlons, and cati: 'konik' (cone with an eave), 'duz' (open top behind the merlons), 'kubbe',
    'sogan' (onion) or None; bolum: the shaft in that many bands. Returns the top z"""
    r0 = r * (1 + egim)
    pr = [(r0 + (r - r0) * k / bolum, z0 + h * k / bolum) for k in range(bolum + 1)]   # (bolum > 1: bands, the baked shadow of the crown stays up there)
    donel(y, c, pr, key, n=n)
    zt = z0 + h
    # slits on n/3 sides, at two heights
    for k in range(yarik_say):
        a = TAU * (k + 0.5) / yarik_say + 0.3
        nn = V(math.cos(a), math.sin(a)); e = V(-nn.y, nn.x)
        for t in (0.35, 0.68):
            rr = r0 + (r - r0) * t
            o = V(c[0], c[1]) + nn * (rr + 0.001)
            yarik(y, o + Z * z0, e, nn, -0.005, h * t, 0.01, h * 0.1, 'koyu')
    ring = cokgen(c, r, n)
    if konsol:
        konsol_halka(y, ring, zt - 0.035, 0.035, 0.016, key, 3)
        ring = cokgen(c, r + 0.016, n)
    if cati in ('duz', None) or mazgal_h:
        parapet(y, ring, zt, 0.012, mazgal_h if cati in ('duz', None) else 0, 0.016, key)
        if cati in ('duz', None):
            y.yuz_yon([V(p.x, p.y, zt + 0.0005) for p in disa(ring, -0.016)], 'zemin', Z)
    rr = r + (0.016 if konsol else 0)
    # (no parapet drawn - a roof with mazgal_h=0 - the roof sits right on the shaft: it left an open ring of 0.012)
    zb = zt + 0.012 if (cati in ('duz', None) or mazgal_h) else zt
    if cati == 'konik':
        hh = cati_h or r * 2.1
        ze = zb
        donel(y, c, [(rr * 0.98, ze), (rr + sacak, ze), (rr * 0.6, ze + hh * 0.45), (0, ze + hh)], cati_key, n=n)
        y.yuz_yon([V(p.x, p.y, ze) for p in cokgen(c, rr + sacak, n)], 'ahsap_koyu', -Z)
        return ze + hh
    if cati == 'kubbe':
        return y.kubbe(c, rr, zb, cati_h or rr * 0.9, cati_key, n=n, kat=8).z
    if cati == 'sogan':
        y.yuz_yon([V(p.x, p.y, zb) for p in cokgen(c, rr, n)], 'zemin', Z)   # (the onion's neck is narrower than the shaft)
        return sogan_kubbe(y, c, rr * 0.8, zb, cati_h, cati_key)
    return zt + 0.012 + (mazgal_h or 0)


def kule_kare(y, cx, cy, w, z0, h, key='tas', cati='piramit', cati_key='kiremit', cati_h=None, mazgal_h=0.03, sacak=0.015,
              yarik_say=2, konsol=True, d=None, kose_tas=None, cati_ns=10, cati_nr=6):
    """a square (w x d) tower: slits, corbelled merloned parapet, cati: 'piramit' (hipped / pyramid roof), 'duz',
    'cadir' (steep spire) or None; kose_tas: a key for quoin stones at the corners; cati_ns / cati_nr: the roof's subdivision
    (cati_kirma ns / nr: a small straight roof needs few). Returns the top z"""
    d = d or w
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, z0, z0 + h, key)
    if kose_tas:
        for p in k:
            for j in range(int(h / 0.05)):
                s = 0.022 if j % 2 == 0 else 0.014
                kutu_merkez(y, (p.x, p.y), s, s, 0.025, kose_tas, z0=z0 + j * 0.05 + 0.005)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        for j in range(yarik_say):
            u = L * (j + 1) / (yarik_say + 1)
            yarik(y, a + Z * z0 + nn * 0.001, e, nn, u - 0.005, h * 0.45, 0.01, h * 0.12, 'koyu')
    zt = z0 + h
    ring = k
    if konsol:
        konsol_halka(y, k, zt - 0.035, 0.035, 0.014, key, 3)
        ring = disa(k, 0.014)
    if cati in ('duz', None) or (mazgal_h and cati != 'piramit'):
        parapet(y, ring, zt, 0.012, mazgal_h, 0.016, key)
        y.yuz_yon([V(p.x, p.y, zt + 0.0005) for p in disa(ring, -0.016)], 'zemin', Z)
    if cati == 'piramit':
        xs = [p.x for p in ring]; ys = [p.y for p in ring]
        return cati_kirma(y, min(xs), max(xs), min(ys), max(ys), zt, cati_h or w * 0.7, sacak, cati_key, ns=cati_ns, nr=cati_nr)
    if cati == 'cadir':
        xs = [p.x for p in ring]; ys = [p.y for p in ring]
        return cati_kirma(y, min(xs), max(xs), min(ys), max(ys), zt + 0.012, cati_h or w * 1.8, sacak * 0.5, cati_key, ns=cati_ns, nr=cati_nr)
    return zt + 0.012 + (mazgal_h or 0)


def kale_kapisi(y, cx, cy, en, z0, h, derin=0.12, key='tas', kule='yuvarlak', kule_r=None, kule_h=None, cati='duz',
                cati_key='kiremit', kapi_key='ahsap', sivri=0.0, kule_n=24):
    """a gatehouse on the line y = cy facing -y: a block en wide and derin deep with an arched passage (doors set in),
    merlons, and two flanking towers (kule: 'yuvarlak', 'kare' or None; kule_n: the round towers' sides). Returns the top z"""
    y0, y1 = cy - derin / 2, cy + derin / 2
    x0, x1 = cx - en / 2, cx + en / 2
    # front and back faces with the passage
    y.kemerli(V(x0, y0), V(x1, y0), z0, h, (key, 'tas_koyu', 'tas_koyu', kapi_key), v0=0.0, en=0.42, ust=h * 0.3, derin=derin * 0.35,
              k_say=10, sivri=sivri, cerceve=(0.012, 'tas_acik'))
    y.kemerli(V(x1, y1), V(x0, y1), z0, h, (key, 'tas_koyu', 'tas_koyu', kapi_key), v0=0.0, en=0.42, ust=h * 0.3, derin=derin * 0.35,
              k_say=10, sivri=sivri)
    duz_duvar(y, V(x1, y0), V(x1, y1), z0, z0 + h, key)
    duz_duvar(y, V(x0, y1), V(x0, y0), z0, z0 + h, key)
    zt = z0 + h
    k = dikdortgen(x0, x1, y0, y1)
    konsol_halka(y, k, zt - 0.03, 0.03, 0.012, key, 3)
    parapet(y, disa(k, 0.012), zt, 0.012, 0.03, 0.016, key)
    y.yuz_yon([V(p.x, p.y, zt + 0.0005) for p in k], 'zemin', Z)
    tepe = zt + 0.042
    if kule:
        r = kule_r or en * 0.26
        hh = kule_h or h * 1.35
        for sx in (-1, 1):
            if kule == 'yuvarlak':
                t = kule_yuvarlak(y, (cx + sx * (en / 2 + r * 0.55), cy - derin * 0.1), r, z0, hh, key, cati, cati_key, n=kule_n)
            else:
                t = kule_kare(y, cx + sx * (en / 2 + r * 0.7), cy - derin * 0.1, r * 2, z0, hh, key, cati if cati != 'konik' else 'piramit', cati_key)
            tepe = max(tepe, t)
    return tepe


# ---------------------------------------------------------------- roofs
def _cati_z(x, yy, a, b, H, kivrim, yukari):
    m = min(a, b)
    t = max(0.0, min(1.0, min(a - abs(x), b - abs(yy)) / m))
    z = H * ((1 - kivrim) * t + kivrim * t * t)
    if yukari:
        z += yukari * (1 - t) ** 2 * (abs(x) / a) ** 5 * (abs(yy) / b) ** 5 * 0 + yukari * (1 - t) ** 2.2 * ((abs(x) / a) * (abs(yy) / b)) ** 6
    return z


def cati_kirma(y, x0, x1, y0, y1, z, h, sacak=0.03, key='kiremit', mahya=None, kalinlik=0.012, kivrim=0.0, yukari=0.0,
               alt_key='ahsap_koyu', ns=10, nr=6, r_ust=1.0, mahya_en=0.012, dilim=None):
    """a hipped roof over the wall rectangle x0..x1, y0..y1 (wall top z), its eaves sacak beyond the walls, h high at the
    ridge. A square plan gives a pyramid. kivrim 0..1: a concave (East Asian) slope, flat at the eaves; yukari: the
    corners turned up by that much. Eave fascia and soffit (alt_key), ridge and hip caps (mahya key). r_ust < 1 stops
    the slopes part-way up (the lower part of an irimoya / xieshan roof: cati_irimoya). dilim: two keys alternating
    in courses up the slope. Returns the ridge z"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2 + sacak, (y1 - y0) / 2 + sacak
    if a < b:   # build with the ridge along x, then turn
        with parca(y, (cx, cy, 0), math.pi / 2):
            return cati_kirma(y, -b + sacak, b - sacak, -a + sacak, a - sacak, z, h, sacak, key, mahya, kalinlik, kivrim, yukari, alt_key, ns, nr, r_ust, mahya_en, dilim)
    m = b
    zf = lambda px, py: z + _cati_z(px, py, a, b, h, kivrim, yukari)
    rs = sacak / m           # the wall line
    rr = sorted({0.0, rs, *[rs + (r_ust - rs) * k / nr for k in range(nr + 1)]})
    rr = [r for r in rr if r <= r_ust + 1e-9]
    kk = (lambda j: dilim[j % len(dilim)]) if dilim else (lambda j: key)

    def P(fc, s, r):   # face fc (0 front -y, 1 right +x, 2 back +y, 3 left -x): eave (s 0..1) to ridge
        if fc == 0: E = V(-a + 2 * a * s, -b); R = V(-(a - b) + 2 * (a - b) * s, 0)
        elif fc == 2: E = V(a - 2 * a * s, b); R = V((a - b) - 2 * (a - b) * s, 0)
        elif fc == 1: E = V(a, -b + 2 * b * s); R = V(a - b, 0)
        else: E = V(-a, b - 2 * b * s); R = V(-(a - b), 0)
        p = E.lerp(R, r)
        return V(cx + p.x, cy + p.y, zf(p.x, p.y))

    for fc in range(4):
        nss = ns if fc in (0, 2) else max(4, int(ns * b / a + 0.5))
        for j in range(len(rr) - 1):
            for i in range(nss):
                q = [P(fc, i / nss, rr[j]), P(fc, (i + 1) / nss, rr[j]), P(fc, (i + 1) / nss, rr[j + 1]), P(fc, i / nss, rr[j + 1])]
                if (q[2] - q[3]).length < 1e-7: q = q[:3]
                y.yuz_yon(q, kk(j), Z)
        # fascia and soffit
        for i in range(nss):
            p0, p1 = P(fc, i / nss, 0), P(fc, (i + 1) / nss, 0)
            w0, w1 = P(fc, i / nss, rs), P(fc, (i + 1) / nss, rs)
            out = V(p0.x - cx, p0.y - cy) + V(p1.x - cx, p1.y - cy)
            y.yuz_yon([p0, p1, p1 - Z * kalinlik, p0 - Z * kalinlik], alt_key, out)
            wz = lambda w: V(w.x, w.y, z)
            y.yuz_yon([p0 - Z * kalinlik, p1 - Z * kalinlik, wz(w1), wz(w0)], alt_key, -Z)
    mk = mahya or key
    if r_ust >= 1 - 1e-9:
        zr = zf(0, 0)
        if a - b > 1e-6:
            cubuk(y, V(cx - (a - b), cy, zr + mahya_en * 0.3), V(cx + (a - b), cy, zr + mahya_en * 0.3), mahya_en, mk)
        for sx in (-1, 1):   # hips
            for sy in (-1, 1):
                pts = [V(cx + sx * (a - b * r), cy + sy * b * (1 - r), zf(sx * (a - b * r), sy * b * (1 - r)) + mahya_en * 0.3) for r in (0, 0.25, 0.5, 0.75, 1.0)]
                for k in range(4):
                    cubuk(y, pts[k], pts[k + 1], mahya_en * 0.8, mk)
        return zr + mahya_en * 0.8
    return zf(0, b * (1 - r_ust))


def cati_besik(y, x0, x1, y0, y1, z, h, sacak=0.03, key='kiremit', mahya=None, kalinlik=0.012, kivrim=0.0, alt_key='ahsap_koyu',
               ucluk_key='tas', alinlik_key=None, uc_sacak=None, nr=6, ns=8, mahya_en=0.012, dilim=None, sus=None):
    """a gable roof over x0..x1, y0..y1 with the ridge along the LONGER side (wall top z, ridge h above): two slopes,
    fascia and soffit, the gable walls (ucluk_key; alinlik_key: a moulded pediment edge), ridge cap. kivrim: concave
    slopes. sus: a key for upturned ridge-end ornaments (East Asian). Returns the ridge z"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if (x1 - x0) < (y1 - y0):
        with parca(y, (cx, cy, 0), math.pi / 2):
            return cati_besik(y, -(y1 - y0) / 2, (y1 - y0) / 2, -(x1 - x0) / 2, (x1 - x0) / 2, z, h, sacak, key, mahya, kalinlik, kivrim,
                              alt_key, ucluk_key, alinlik_key, uc_sacak, nr, ns, mahya_en, dilim, sus)
    us = sacak if uc_sacak is None else uc_sacak
    a = (x1 - x0) / 2 + us
    wb = (y1 - y0) / 2
    b = wb + sacak
    zf = lambda t: z + h * ((1 - kivrim) * t + kivrim * t * t) - (sacak / b) * h * 0.0
    rs = sacak / b
    kk = (lambda j: dilim[j % len(dilim)]) if dilim else (lambda j: key)
    rr = sorted({0.0, rs, *[rs + (1 - rs) * k / nr for k in range(nr + 1)]})
    for sy in (-1, 1):
        for j in range(len(rr) - 1):
            for i in range(ns):
                xa, xb = -a + 2 * a * i / ns, -a + 2 * a * (i + 1) / ns
                ya, yb = sy * b * (1 - rr[j]), sy * b * (1 - rr[j + 1])
                q = [V(cx + xa, cy + ya, zf(rr[j])), V(cx + xb, cy + ya, zf(rr[j])), V(cx + xb, cy + yb, zf(rr[j + 1])), V(cx + xa, cy + yb, zf(rr[j + 1]))]
                y.yuz_yon(q, kk(j), Z)
        # fascia + soffit along the eave
        p0, p1 = V(cx - a, cy + sy * b, z), V(cx + a, cy + sy * b, z)
        y.yuz_yon([p0, p1, p1 - Z * kalinlik, p0 - Z * kalinlik], alt_key, V(0, sy))
        iki_yuzlu(y, [p0 - Z * kalinlik, p1 - Z * kalinlik, V(cx + a, cy + sy * wb, z), V(cx - a, cy + sy * wb, z)], alt_key, -Z)   # (two-sided: its top shows past the verge)
        # the roof's edge at the gables (verge) and the underside of the overhang
        for sx in (-1, 1):
            pts = [V(cx + sx * a, cy + sy * b * (1 - r), zf(r)) for r in rr]
            for k in range(len(pts) - 1):
                y.yuz_yon([pts[k], pts[k + 1], pts[k + 1] - Z * kalinlik, pts[k] - Z * kalinlik], alt_key, V(sx, 0))
            if us > 0.001:
                for k in range(len(pts) - 1):
                    qa, qb = pts[k] - Z * kalinlik, pts[k + 1] - Z * kalinlik
                    iki_yuzlu(y, [qa, qb, qb - V(sx * us, 0), qa - V(sx * us, 0)], alt_key, -Z)
            # (the wedge between the eave soffit and the roof's underside, open at the verge end: close it)
            e_ = zf(rs) - kalinlik - z
            if e_ > 0.0005:
                y.yuz_yon([V(cx + sx * a, cy + sy * b, z - kalinlik), V(cx + sx * a, cy + sy * wb, z), V(cx + sx * a, cy + sy * wb, z + e_)], alt_key, V(sx, 0))
                if us > 0.001:   # (and its side towards the open air under the gable overhang)
                    xi, xo = cx + sx * (a - us), cx + sx * a
                    y.yuz_yon([V(xi, cy + sy * wb, z), V(xo, cy + sy * wb, z), V(xo, cy + sy * wb, z + e_), V(xi, cy + sy * wb, z + e_)], alt_key, V(0, -sy))
    # gable walls (the triangle above the wall top, on the wall line)
    for sx in (-1, 1):
        xg = cx + sx * (a - us)
        tri = [V(xg, cy - wb, z), V(xg, cy + wb, z), V(xg, cy, zf(1) - kalinlik)]
        # (the roof's underside crosses the wall line above the wall top: close that wedge, it showed the inside)
        e_ = h * rs - kalinlik
        if e_ > 0.0005:
            tri = [V(xg, cy - wb, z), V(xg, cy + wb, z), V(xg, cy + wb, z + e_), V(xg, cy, zf(1) - kalinlik), V(xg, cy - wb, z + e_)]
        # follow the roof's curve with a few points
        if kivrim:
            tri = [V(xg, cy - wb, z)] + [V(xg, cy - wb * (1 - r), zf(r) - kalinlik) for r in (0.25, 0.5, 0.75)] + [V(xg, cy, zf(1) - kalinlik)] + \
                  [V(xg, cy + wb * (1 - r), zf(r) - kalinlik) for r in (0.75, 0.5, 0.25)] + [V(xg, cy + wb, z)]
        y.yuz_yon(tri, ucluk_key, V(sx, 0))
        if alinlik_key:
            for s2 in (-1, 1):
                pa, pb = V(xg, cy + s2 * wb, z), V(xg, cy, zf(1) - kalinlik)
                d = V(sx * 0.01, 0)
                y.yuz_yon([pa + d, pb + d, pb + d - Z * 0.012, pa + d - Z * 0.012], alinlik_key, V(sx, 0))
    zr = zf(1)
    mk = mahya or key
    cubuk(y, V(cx - a, cy, zr + mahya_en * 0.3), V(cx + a, cy, zr + mahya_en * 0.3), mahya_en, mk)
    if sus:
        for sx in (-1, 1):
            p = V(cx + sx * a, cy, zr + mahya_en * 0.3)
            boru(y, [p, p + V(sx * 0.012, 0, 0.012), p + V(sx * 0.014, 0, 0.032), p + V(sx * 0.004, 0, 0.045)], mahya_en * 0.7, sus, n=6, r_son=mahya_en * 0.3)
    return zr + mahya_en * 0.8


def cati_irimoya(y, x0, x1, y0, y1, z, h, sacak=0.05, key='kiremit_koyu', mahya='kiremit_koyu2', kivrim=0.45, yukari=0.03,
                 alt_key='ahsap_koyu', ucluk_key='ahsap', oran=0.55, sus=None, dilim=None):
    """a hip-and-gable roof (Japanese irimoya, Chinese xieshan, Korean paljak): hipped below up to oran of the
    height, a small gable roof on top with its triangular gable walls. Returns the ridge z"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2 + sacak, (y1 - y0) / 2 + sacak
    if a < b:
        with parca(y, (cx, cy, 0), math.pi / 2):
            return cati_irimoya(y, -(y1 - y0) / 2, (y1 - y0) / 2, -(x1 - x0) / 2, (x1 - x0) / 2, z, h, sacak, key, mahya, kivrim, yukari, alt_key, ucluk_key, oran, sus, dilim)
    m = b
    # the lower slopes stop at r_ust (t = r_ust): the hip ring's top edge
    r_ust = 0.5
    zt = cati_kirma(y, x0, x1, y0, y1, z, h * 1.0, sacak, key, mahya, 0.012, kivrim, yukari, alt_key, r_ust=r_ust, dilim=dilim)
    # upper gable roof: covers the opening (half sizes a - b r_ust, b (1 - r_ust)) plus a small overhang
    ai, bi = a - m * r_ust, b * (1 - r_ust)
    ho = h * ((1 - kivrim) + kivrim) - (zt - z)
    # the hip ring's top opening closed by a ledge (seen in front of the gable)
    y.yuz_yon([V(cx - ai, cy - bi, zt - 0.001), V(cx + ai, cy - bi, zt - 0.001), V(cx + ai, cy + bi, zt - 0.001), V(cx - ai, cy + bi, zt - 0.001)], key, Z)
    # (steeper than the hips, its verges projecting over the hip slopes: the gable reads as a raised triangle, not a
    #  hole in the roof)
    zr = cati_besik(y, cx - ai + sacak * 0.6, cx + ai - sacak * 0.6, cy - bi + 0.012, cy + bi - 0.012, zt - 0.004, max(0.02, ho * 1.45), 0.016, key, mahya,
                    0.008, kivrim * 0.5, alt_key, ucluk_key, None, sacak * 0.6, sus=sus, dilim=dilim)
    return zr


# ---------------------------------------------------------------- East Asian storeys
def pagoda_kati(y, c, w, z, h, cati_h, sacak=0.06, key_duvar='siva', key_direk='lake', key_cati='kiremit_koyu', mahya='kiremit_koyu2',
                kivrim=0.5, yukari=0.035, korkuluk=True, kafesli=True, d=None, kat_sayisi_kapi=1, alt_key='lake_koyu', dilim=None,
                irimoya=False, sus=None, balkon=0.025):
    """one storey of an East Asian hall or pagoda, w x d (d = w: square) centred on c from z: plastered (or wooden)
    walls between lacquered posts with a lintel, lattice windows, an optional balcony with a railing, bracket
    blocks under the eaves and a curved hipped roof (irimoya: hip-and-gable). Returns (roof ridge z, z for a storey
    above standing on this roof)"""
    d = d or w
    cx, cy = c
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2
    k = dikdortgen(x0, x1, y0, y1)
    zt = z + h
    # walls with lattice openings (one bay in the middle of each side), set behind the posts
    for i in range(4):
        a_, b_ = k[i], k[(i + 1) % 4]
        L = (b_ - a_).length
        nb = max(1, int(round(L / 0.12)))
        for j in range(nb):
            p, q = a_.lerp(b_, j / nb), a_.lerp(b_, (j + 1) / nb)
            if kafesli and (j == nb // 2 or (nb >= 5 and j in (1, nb - 2))):
                dikdortgen_acik(y, p, q, z, h, 0.18, 0.82, h * (0.0 if j == nb // 2 and i == 0 else 0.25), h * 0.82,
                                (key_duvar, 'ahsap', 'ahsap', 'koyu'), derin=0.01)
                kafes(y, p, q, z, 0.18, 0.82, h * (0.0 if j == nb // 2 and i == 0 else 0.25), h * 0.82, 'ahsap_koyu', 4, 4, 0.003, 0.005)
            else:
                duz_duvar(y, p, q, z, zt, key_duvar)
        # posts on the bay lines, and the lintel
        for j in range(nb + 1):
            p = a_.lerp(b_, j / nb)
            if j < nb or True:
                kutu_merkez(y, (p.x, p.y), 0.014, 0.014, h, key_direk, z0=z)
        e = (b_ - a_).normalized(); nn = V(e.y, -e.x)
        kutu(y, a_ + nn * 0.008 + Z * (zt - h * 0.13) - e * 0.007, e, L + 0.014, 0.016, h * 0.13, key_direk, 'onust')
        kutu(y, a_ + nn * 0.008 + Z * z - e * 0.007, e, L + 0.014, 0.016, h * 0.05, key_direk, 'onust')
    # brackets (dougong) under the eaves: a row of small stepped blocks
    for i in range(4):
        a_, b_ = k[i], k[(i + 1) % 4]
        e = (b_ - a_).normalized(); nn = V(e.y, -e.x); L = (b_ - a_).length
        nb = max(2, int(round(L / 0.05)))
        for j in range(nb + 1):
            p = a_.lerp(b_, j / nb) + nn * 0.004
            kutu_merkez(y, (p.x + nn.x * 0.008, p.y + nn.y * 0.008), 0.014, 0.014, 0.01, 'ahsap', z0=zt)
            kutu_merkez(y, (p.x + nn.x * 0.016, p.y + nn.y * 0.016), 0.02, 0.012, 0.008, alt_key, z0=zt + 0.01)
    if korkuluk and balkon:
        kb = disa(k, balkon)
        # the balcony floor and its railing
        for i in range(4):
            j = (i + 1) % 4
            y.yuz_yon([k[i] + Z * z, k[j] + Z * z, kb[j] + Z * z, kb[i] + Z * z], 'ahsap', Z)
            duz_duvar(y, kb[i], kb[j], z - 0.008, z, 'ahsap_koyu')
            y.yuz_yon([k[i] + Z * (z - 0.008), kb[i] + Z * (z - 0.008), kb[j] + Z * (z - 0.008), k[j] + Z * (z - 0.008)], 'ahsap_koyu', -Z)
            boru(y, [kb[i] + Z * (z + 0.03), kb[j] + Z * (z + 0.03)], 0.0025, key_direk, n=4, kapat=False)
            L = (kb[j] - kb[i]).length
            nb = max(2, int(L / 0.03))
            for m in range(nb):
                p = kb[i].lerp(kb[j], m / nb)
                cubuk(y, p + Z * z, p + Z * (z + 0.03), 0.004, key_direk)
    zc = zt + 0.018
    if irimoya:
        tepe = cati_irimoya(y, x0, x1, y0, y1, zc, cati_h, sacak, key_cati, mahya, kivrim, yukari, alt_key, 'ahsap', sus=sus, dilim=dilim)
    else:
        tepe = cati_kirma(y, x0, x1, y0, y1, zc, cati_h, sacak, key_cati, mahya, 0.012, kivrim, yukari, alt_key, dilim=dilim)
    # the next storey stands on the roof: inset by ~15%
    a = w / 2 + sacak; b = d / 2 + sacak
    w2 = w * 0.78
    t = (min(a, b) - w2 / 2) / min(a, b)
    z_ust = zc + cati_h * ((1 - kivrim) * t + kivrim * t * t)
    return tepe, z_ust


def sorin(y, cx, cy, z, boy, key='bronz', halka=7):
    """a pagoda finial (sorin / chatra): a base, a mast with stacked rings, a jewel on top"""
    donel(y, (cx, cy), [(0.025, z), (0.025, z + 0.012), (0.018, z + 0.02), (0.02, z + 0.03), (0.01, z + 0.035)], key, n=12)
    y.prizma((cx, cy), 0.005, z + 0.035, z + boy, key, n=8)
    for i in range(halka):
        zz = z + 0.05 + (boy - 0.09) * i / max(1, halka - 1)
        y.prizma((cx, cy), 0.012 - i * 0.0006, zz, zz + 0.004, key, n=12)
    kure(y, (cx, cy, z + boy + 0.006), 0.008, key)
    return z + boy + 0.014


# ---------------------------------------------------------------- pyramids, obelisks, stepped temples
def piramit(y, c, w, h, key='kum', uc='altin', uc_oran=0.07, kat=6, z0=0.0):
    """a smooth pyramid (square base w) with a gilded pyramidion; split in kat bands so the baked shadow and the
    stone courses follow it. Returns the apex z"""
    cx, cy = c
    def P(t, sx, sy):
        r = w / 2 * (1 - t)
        return V(cx + sx * r, cy + sy * r, z0 + h * t)
    kose = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    tu = 1 - uc_oran
    ts = [tu * k / kat for k in range(kat + 1)]
    for i in range(4):
        (ax, ay), (bx, by) = kose[i], kose[(i + 1) % 4]
        out = V(ax + bx, ay + by)
        for k in range(kat):
            y.yuz_yon([P(ts[k], ax, ay), P(ts[k], bx, by), P(ts[k + 1], bx, by), P(ts[k + 1], ax, ay)], key, out)
        apex = V(cx, cy, z0 + h)
        y.yuz_yon([P(tu, ax, ay), P(tu, bx, by), apex], uc or key, out)
    return z0 + h


def basamakli_piramit(y, c, w0, w1, n, h, key='kirec', talud=0.6, tablero_key=None, merdiven=True, merdiven_en=None,
                      merdiven_key=None, alfarda_key=None, yon=0.0, z0=0.0, d0=None, d1=None):
    """a stepped pyramid / ziggurat of n tiers from a w0 x d0 base to a w1 x d1 top, h high: each tier a sloped
    talud (talud: its share of the tier height) under an upright tablero panel (tablero_key: a framed, painted panel),
    a front stair (facing -y, then turned by yon) with side balustrades. Returns the top z and half sizes"""
    d0 = d0 or w0; d1 = d1 or w1
    cx, cy = c
    with parca(y, (cx, cy, 0), yon):
        th = h / n
        for k in range(n):
            t0, t1 = k / n, (k + 1) / n
            hw0, hd0 = (w0 + (w1 - w0) * t0) / 2, (d0 + (d1 - d0) * t0) / 2
            hw1, hd1 = (w0 + (w1 - w0) * t1) / 2, (d0 + (d1 - d0) * t1) / 2
            za, zb = z0 + th * k, z0 + th * (k + 1)
            zm = za + th * talud
            # talud: from the tier's foot (hw0) sloping in to (hw0 - inset)
            ins = (hw0 - hw1) * 0.75
            alt = dikdortgen(-hw0, hw0, -hd0, hd0, za)
            ort = dikdortgen(-hw0 + ins, hw0 - ins, -hd0 + ins, hd0 - ins, zm)
            y.serit(alt, ort, key)
            # tablero: upright from zm to zb, slightly projecting (a frame and a recessed panel)
            tw, td = hw0 - ins * 0.85, hd0 - ins * 0.85
            tb = dikdortgen(-tw, tw, -td, td)
            duvarlar(y, tb, zm, zb, tablero_key or key)
            # the ledge under the tablero (its bottom) and the terrace on top
            for i in range(4):
                j = (i + 1) % 4
                y.yuz_yon([ort[i], ort[j], tb[j] + Z * zm, tb[i] + Z * zm], key, -Z)
            nxt = dikdortgen(-hw1, hw1, -hd1, hd1)
            for i in range(4):
                j = (i + 1) % 4
                y.yuz_yon([tb[i] + Z * zb, tb[j] + Z * zb, nxt[j] + Z * zb, nxt[i] + Z * zb], 'zemin' if k < n - 1 else key, Z)
            if tablero_key:   # a frame band round the panel
                silme(y, tb, zb - th * 0.08, th * 0.08, 0.006, key)
                silme(y, tb, zm, th * 0.06, 0.006, key)
        y.yuz_yon([V(p.x, p.y, z0 + h) for p in dikdortgen(-w1 / 2, w1 / 2, -d1 / 2, d1 / 2)], key, Z)
        if merdiven:
            me = merdiven_en or w1 * 0.5
            mk = merdiven_key or key
            ns = n * 5
            y_bot, y_top = -d0 / 2 - 0.0, -d1 / 2
            run = (y_top - y_bot)
            for s in range(ns):
                t = (s + 1) / ns
                ya = y_bot + run * s / ns - 0.02 * (1 - s / ns)
                zt = z0 + h * t
                kutu(y, V(-me / 2, ya, z0), X, me, run / ns + 0.02, zt - z0, mk, 'onsagsolust')
            # balustrades: sloping blocks on either side of the stair
            ak = alfarda_key or key
            for sx in (-1, 1):
                xa, xb = sx * me / 2, sx * (me / 2 + 0.03)
                xa, xb = min(xa, xb), max(xa, xb)
                p0, p1 = V(0, y_bot - 0.02, z0), V(0, y_top, z0 + h)
                hh = 0.025
                for u0, u1 in ((xa, xb),):
                    A = [V(u0, p0.y, z0), V(u1, p0.y, z0), V(u1, p0.y, z0 + hh), V(u0, p0.y, z0 + hh)]
                    B = [V(u0, p1.y, z0 + h - 0.001), V(u1, p1.y, z0 + h - 0.001), V(u1, p1.y, z0 + h + hh), V(u0, p1.y, z0 + h + hh)]
                    y.yuz_yon([A[3], A[2], B[2], B[3]], ak, Z + V(0, -0.5))
                    y.yuz_yon([A[0], A[1], A[2], A[3]], ak, -Y)
                    y.yuz_yon([A[1], B[1], B[2], A[2]], ak, X)
                    y.yuz_yon([B[0], A[0], A[3], B[3]], ak, -X)
                    # the side down to the ground
                    y.yuz_yon([A[1], V(u1, p1.y, z0), B[1]], ak, X)
                    y.yuz_yon([A[0], B[0], V(u0, p1.y, z0)], ak, -X)
    return z0 + h, w1 / 2, d1 / 2


def dikilitas(y, c, w, h, key='granit', uc_key='altin', z0=0.0, kaide=True, yazi_key=None):
    """an obelisk: square base w, tapering to 0.65 w, a gilded pyramidion; yazi_key: carved bands of glyphs (small
    dark marks) down each face. Returns the tip z"""
    cx, cy = c
    if kaide:
        kutu_merkez(y, c, w * 1.9, w * 1.9, w * 0.35, key, z0=z0)
        kutu_merkez(y, c, w * 1.6, w * 1.6, w * 0.2, key, z0=z0 + w * 0.35)
        z0 += w * 0.55
    hs = h * 0.9
    a0, a1 = dikdortgen(-w / 2 + cx, w / 2 + cx, -w / 2 + cy, w / 2 + cy, z0), dikdortgen(-w * 0.33 + cx, w * 0.33 + cx, -w * 0.33 + cy, w * 0.33 + cy, z0 + hs)
    ring = [a0]
    for k in range(1, 5):
        t = k / 4
        ring.append([p0.lerp(p1, t) for p0, p1 in zip(a0, a1)])
    for k in range(4):
        y.serit(ring[k], ring[k + 1], key)
    for i in range(4):
        y.yuz_yon([a1[i], a1[(i + 1) % 4], V(cx, cy, z0 + h)], uc_key, V(a1[i].x + a1[(i + 1) % 4].x - 2 * cx, a1[i].y + a1[(i + 1) % 4].y - 2 * cy))
    if yazi_key:
        for i in range(4):
            p, q = a0[i], a0[(i + 1) % 4]
            e = (q - p).normalized(); nn = V(e.y, -e.x)
            for j in range(9):
                t = 0.08 + j * 0.09
                wt = w * (1 - 0.34 * t)
                m = p.lerp(q, 0.5).lerp(V(cx, cy, z0 + hs), 0) + V(0, 0, 0)
                cc = V(cx, cy) + nn * (wt / 2 + 0.0015) + Z * (z0 + hs * t)
                y.yuz_yon([cc - e * wt * 0.18, cc + e * wt * 0.18, cc + e * wt * 0.18 + Z * hs * 0.035, cc - e * wt * 0.18 + Z * hs * 0.035], yazi_key, nn + Z * 0.33 * w / hs)
    return z0 + h


# ---------------------------------------------------------------- timber: logs, longhouses
def kutuk_duvar(y, a, b, z0, z1, r=0.014, key='kutuk', uzanti=0.02, ic=True):
    """a wall of horizontal logs a->b (outer side to the right): half-round log faces, ends sticking out uzanti
    past a and b (the crossed corners of a log house)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    n = max(1, int(round((z1 - z0) / (2 * r))))
    rr = (z1 - z0) / n / 2
    for k in range(n):
        zc = z0 + rr * (2 * k + 1)
        p = a - e * uzanti + Z * zc - nc * rr * 0.2
        q = b + e * uzanti + Z * zc - nc * rr * 0.2
        boru(y, [p, q], rr * 1.04, key, n=8)
    if ic:
        duz_duvar(y, b - nc * rr * 1.3, a - nc * rr * 1.3, z0, z1, key)


def kutuk_ev(y, x0, x1, y0, y1, z0, h, r=0.014, key='kutuk', cati_key='ahsap_koyu', cati_h=None, sacak=0.03, kapi_yon=0):
    """a log house: four log walls with crossed ends, a gable roof (boards or shingles: cati_key), gables of
    vertical boards, a door on the front (-y). Returns the ridge z"""
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        # the two walls of a pair sit half a log apart, so the ends interlock
        off = r if i % 2 else 0
        kutuk_duvar(y, k[i], k[(i + 1) % 4], z0 + off, z0 + h + off, r, key, uzanti=r * 2.5)
    # door
    cx = (x0 + x1) / 2
    y.yuz_yon([V(cx - 0.035, y0 - r * 1.2, z0), V(cx + 0.035, y0 - r * 1.2, z0), V(cx + 0.035, y0 - r * 1.2, z0 + h * 0.75), V(cx - 0.035, y0 - r * 1.2, z0 + h * 0.75)], 'ahsap_dikey', -Y)
    return cati_besik(y, x0 - r, x1 + r, y0 - r, y1 + r, z0 + h + r, cati_h or (min(x1 - x0, y1 - y0) * 0.45), sacak, cati_key,
                      ucluk_key='ahsap_dikey')


def uzun_ev(y, cx, cy, L, W, h, cati_h, key='ahsap_dikey', cati_key='saz', mahya_key='cimen', bombe=0.16, sacak=0.04,
            ejder=True, ejder_key='ahsap_koyu', kapi=True, n=12, kirlangic=True):
    """a Viking / Norse longhouse along x: bow-sided (bombe: how much narrower the ends are), low plank walls, a
    steep roof with a sagging ridge (thatch / turf / shingles), carved crossed gable boards (ejder: dragon-head
    finials), doors on the long sides. Returns the ridge z"""
    def hw(x):
        return W / 2 * (1 - bombe * (2 * x / L) ** 2)
    xs = [-L / 2 + L * i / n for i in range(n + 1)]
    for sy in (-1, 1):   # long walls
        for i in range(n):
            xa, xb = xs[i], xs[i + 1]
            pa, pb = V(cx + xa, cy + sy * hw(xa)), V(cx + xb, cy + sy * hw(xb))
            if sy > 0: pa, pb = pb, pa
            duz_duvar(y, pa, pb, 0, h, key)
        # a low stone footing
        pts = [V(cx + x, cy + sy * (hw(x) + 0.006)) for x in (xs if sy < 0 else list(reversed(xs)))]
    # gable-end walls
    for sx in (-1, 1):
        x = sx * L / 2
        a, b = V(cx + x, cy + sx * hw(x)), V(cx + x, cy - sx * hw(x))
        p, q = (V(cx + x, cy - hw(x)), V(cx + x, cy + hw(x))) if sx > 0 else (V(cx + x, cy + hw(x)), V(cx + x, cy - hw(x)))
        duz_duvar(y, p, q, 0, h, key)
    # roof: rows from the eave (beyond the wall by sacak, at the wall top) to the sagging ridge
    nr = 6
    ext = L * 0.04
    def rp(x, sy, t):
        zr = h + cati_h * (1 - 0.1 * (2 * x / L) ** 2)
        yy = sy * (hw(max(-L / 2, min(L / 2, x))) + sacak) * (1 - t)
        return V(cx + x, cy + yy, h - sacak * 0.4 + (zr - h + sacak * 0.4) * t)
    xr = [-L / 2 - ext + (L + 2 * ext) * i / n for i in range(n + 1)]
    for sy in (-1, 1):
        for j in range(nr):
            for i in range(n):
                q = [rp(xr[i], sy, j / nr), rp(xr[i + 1], sy, j / nr), rp(xr[i + 1], sy, (j + 1) / nr), rp(xr[i], sy, (j + 1) / nr)]
                y.yuz_yon(q, cati_key, Z + V(0, sy * 0.3))
        # roof thickness at the eave and the soffit
        for i in range(n):
            p0, p1 = rp(xr[i], sy, 0), rp(xr[i + 1], sy, 0)
            y.yuz_yon([p0, p1, p1 - Z * 0.02, p0 - Z * 0.02], cati_key if cati_key in ('saz', 'saz_koyu', 'cimen') else 'ahsap_koyu', V(0, sy))
            w0, w1 = V(p0.x, cy + sy * hw(max(-L / 2, min(L / 2, xr[i] - cx + cx - cx))), h), V(p1.x, cy + sy * hw(max(-L / 2, min(L / 2, xr[i + 1]))), h)
            y.yuz_yon([p0 - Z * 0.02, p1 - Z * 0.02, w1, w0], 'ahsap_koyu', -Z)
    # the roof's ends (verges) and gables
    for sx in (-1, 1):
        x = sx * (L / 2 + ext)
        for sy in (-1, 1):
            pts = [rp(x, sy, t / nr) for t in range(nr + 1)]
            for k in range(nr):
                y.yuz_yon([pts[k], pts[k + 1], pts[k + 1] - Z * 0.02, pts[k] - Z * 0.02], 'ahsap_koyu', V(sx, 0))
                y.yuz_yon([pts[k] - Z * 0.02, pts[k + 1] - Z * 0.02, pts[k + 1] - Z * 0.02 - V(sx * ext, 0), pts[k] - Z * 0.02 - V(sx * ext, 0)], 'ahsap_koyu', -Z)
        # gable triangle on the end wall
        xg = sx * L / 2
        tri = [V(cx + xg, cy - sx * hw(xg), h), V(cx + xg, cy + sx * hw(xg), h), V(cx + xg, cy, rp(xg, 1, 1).z - 0.02)]
        # (the roof's underside meets the end wall above its top at the eaves: a slit there showed the inside; close it)
        e_ = rp(xg, 1, sacak / (hw(xg) + sacak)).z - 0.02 - h
        if e_ > 0.0005:
            tri = [tri[0], tri[1], tri[1] + Z * e_, tri[2], tri[0] + Z * e_]
            for sy in (-1, 1):   # (and the same wedge between the eave soffit and the roof's underside at the roof's end)
                yw = V(cx + x, cy + sy * hw(xg), h)
                y.yuz_yon([rp(x, sy, 0) - Z * 0.02, yw, yw + Z * e_], 'ahsap_koyu', V(sx, 0))
        y.yuz_yon(tri, key, V(sx, 0))
        if ejder:   # crossed barge boards ending in carved heads
            top = rp(x, 1, 1)
            for sy in (-1, 1):
                p0 = rp(x, sy, 0.45) + V(sx * 0.006, 0, 0.012)
                p1 = top + V(sx * 0.006, 0, 0.012)
                cubuk(y, p0, p1, 0.012, ejder_key, 0.008)
                d = (p1 - p0).normalized()
                hd = [p1, p1 + d * 0.03, p1 + d * 0.05 + V(0, 0, 0.015), p1 + d * 0.056 + V(sx * 0.012, 0, 0.026)]
                boru(y, hd, 0.007, ejder_key, n=6, r_son=0.004)
    # ridge: turf / sod ridge
    pts = [rp(x, 1, 1) + Z * 0.006 for x in xr]
    for i in range(n):
        cubuk(y, pts[i], pts[i + 1], 0.024, mahya_key or cati_key, 0.012)
    if kapi:
        for sy in (-1, 1):
            x = L * 0.12 * sy
            yy = hw(x) + 0.002
            p = V(cx + x, cy + sy * yy)
            e = V(-sy, 0) * -1
            y.yuz_yon([p + V(-0.03, 0, 0), p + V(0.03, 0, 0), p + V(0.03, 0, h * 0.8), p + V(-0.03, 0, h * 0.8)], 'ahsap_koyu', V(0, sy))
            cubuk(y, p + V(-0.034, sy * 0.003, 0), p + V(-0.034, sy * 0.003, h * 0.86), 0.008, 'ahsap')
            cubuk(y, p + V(0.034, sy * 0.003, 0), p + V(0.034, sy * 0.003, h * 0.86), 0.008, 'ahsap')
            cubuk(y, p + V(-0.04, sy * 0.003, h * 0.86), p + V(0.04, sy * 0.003, h * 0.86), 0.008, 'ahsap')
    return rp(0, 1, 1).z


def kirma_dikme(y, a, b, z0, z1, key='ahsap_koyu', aralik=0.06, en=0.008, capraz=True):
    """half-timbering on a wall a->b: posts, a mid rail and braces, just in front of the wall (faces the right)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    o = nc * (en * 0.5)
    n = max(1, int(round(L / aralik)))
    for i in range(n + 1):
        p = a.lerp(b, i / n) + o
        cubuk(y, p + Z * z0, p + Z * z1, en, key, en * 0.6)
    for zz in (z0 + en / 2, (z0 + z1) / 2, z1 - en / 2):
        cubuk(y, a + o + Z * zz, b + o + Z * zz, en, key, en * 0.6)
    if capraz:
        for i in range(n):
            if i % 2: continue
            p, q = a.lerp(b, i / n) + o, a.lerp(b, (i + 1) / n) + o
            cubuk(y, p + Z * z0, q + Z * ((z0 + z1) / 2), en * 0.8, key, en * 0.5)


# ---------------------------------------------------------------- tents
def cadir_otag(y, c, r, h_duvar, h_cati, key='kece', bant='kirmizi', kapi_yon=-math.pi / 2, tepe_key='altin', kapi_key='lake',
               n=32, ip_key='ahsap_koyu', sacak=0.012):
    """a Mongol ger: a round felt wall (bulging a little), rope girths and a painted band, a door frame, a shallow
    conical roof rising to a raised crown ring with a finial. Returns the top z"""
    cx, cy = c
    donel(y, c, [(r, 0), (r * 1.03, h_duvar * 0.5), (r, h_duvar)], key, n=n)
    for zz in (h_duvar * 0.25, h_duvar * 0.75):   # girths (just outside the wall)
        donel(y, c, [(r * 1.035, zz - 0.003), (r * 1.04, zz), (r * 1.035, zz + 0.003)], ip_key, n=n)
    if bant:
        donel(y, c, [(r * 1.034, h_duvar * 0.42), (r * 1.034, h_duvar * 0.58)], bant, n=n)
    # roof: from the eave just past the wall, slightly convex, to the crown
    rc = r * 0.2
    pr = [(r + sacak, h_duvar - 0.004), (r * 0.7, h_duvar + h_cati * 0.42), (r * 0.42, h_duvar + h_cati * 0.78), (rc, h_duvar + h_cati)]
    donel(y, c, pr, key, n=n)
    y.yuz_yon([V(p.x, p.y, h_duvar - 0.004) for p in cokgen(c, r + sacak, n)], 'kece', -Z)
    # roof bands (radial straps)
    for i in range(8):
        a = TAU * i / 8 + 0.2
        d = V(math.cos(a), math.sin(a))
        pts = [V(cx, cy) + d * (rr + 0.002) + Z * (zz + 0.002) for rr, zz in pr]
        boru(y, pts, 0.003, ip_key, n=4, kapat=False)
    # the crown ring and finial
    zc = h_duvar + h_cati
    donel(y, c, [(rc, zc), (rc * 1.1, zc + 0.01), (rc * 0.9, zc + 0.018), (rc * 0.5, zc + 0.02), (0, zc + 0.03)], tepe_key if tepe_key else key, n=16)
    top = zc + 0.03
    if tepe_key:
        y.prizma(c, 0.004, top, top + 0.04, tepe_key, n=6)
        kure(y, (cx, cy, top + 0.048), 0.009, tepe_key)
        top += 0.06
    # door: a painted frame and leaf on the wall
    d = V(math.cos(kapi_yon), math.sin(kapi_yon)); e = V(-d.y, d.x)
    o = V(cx, cy) + d * (r * 1.025)
    w, hh = r * 0.32, h_duvar * 0.82
    cubuk(y, o - e * w / 2 + Z * 0, o - e * w / 2 + Z * hh, 0.012, kapi_key, 0.01)
    cubuk(y, o + e * w / 2 + Z * 0, o + e * w / 2 + Z * hh, 0.012, kapi_key, 0.01)
    cubuk(y, o - e * (w / 2 + 0.006) + Z * hh, o + e * (w / 2 + 0.006) + Z * hh, 0.012, kapi_key, 0.01)
    y.yuz_yon([o - e * w / 2 + d * 0.004, o + e * w / 2 + d * 0.004, o + e * w / 2 + d * 0.004 + Z * hh, o - e * w / 2 + d * 0.004 + Z * hh], 'boya_sari' if kapi_key == 'lake' else 'ahsap', d)
    return top


def cadir(y, c, r, h, key='kumas', serit_key='kirmizi', n=16, direk_key='ahsap', ip=True):
    """a conical army tent (bell tent): a cone with a short wall, a pole tip, stripes and guy ropes"""
    cx, cy = c
    donel(y, c, [(r, 0), (r, h * 0.15), (r * 0.45, h * 0.6), (0.004, h)], key, n=n, dilim=[key, serit_key] if serit_key else None)
    y.prizma(c, 0.003, h, h + 0.035, direk_key, n=5)
    if ip:
        for i in range(6):
            a = TAU * i / 6
            d = V(math.cos(a), math.sin(a))
            cubuk(y, V(cx, cy) + d * r + Z * (h * 0.15), V(cx, cy) + d * (r * 1.5), 0.0025, 'ahsap_koyu')


# ---------------------------------------------------------------- mud brick (Sahel)
def kerpic_duvar(y, kose, z0, h, key='kerpic', kapali=True, payanda=0.12, toron=True, sivri_tepe=True, egim=0.04, ust_key=None):
    """Sudano-Sahelian mud walls along a CCW polygon (or polyline): battered (egim: the wall leans in by that much),
    pilasters every `payanda` units rising above the top into rounded cone pinnacles, rows of toron palm beams
    sticking out, a rounded parapet. Returns the top z"""
    m = len(kose)
    ust_ = disa(kose, -egim * h, kapali)
    for i in range(m if kapali else m - 1):
        j = (i + 1) % m
        a, b, a2, b2 = kose[i], kose[j], ust_[i], ust_[j]
        e = (b - a); e.z = 0; L = e.length; e.normalize(); nc = V(e.y, -e.x)
        y.yuz_yon([V(a.x, a.y, z0), V(b.x, b.y, z0), V(b2.x, b2.y, z0 + h), V(a2.x, a2.y, z0 + h)], key, nc + Z * egim)
        # rounded crest: a low ridge on the wall top
        y.yuz_yon([V(a2.x, a2.y, z0 + h), V(b2.x, b2.y, z0 + h), V(b2.x, b2.y, z0 + h) - nc * 0.012 + Z * 0.012, V(a2.x, a2.y, z0 + h) - nc * 0.012 + Z * 0.012], ust_key or key, nc + Z)
        # the crest's back slope and the wall's inner face (the walls were one-sided: open from inside a court)
        ia, ib = V(a2.x, a2.y) - nc * 0.024, V(b2.x, b2.y) - nc * 0.024
        y.yuz_yon([V(b2.x, b2.y, z0 + h) - nc * 0.012 + Z * 0.012, V(a2.x, a2.y, z0 + h) - nc * 0.012 + Z * 0.012, ia + Z * (z0 + h), ib + Z * (z0 + h)], ust_key or key, -nc + Z)
        y.yuz_yon([ib + Z * z0, ia + Z * z0, ia + Z * (z0 + h), ib + Z * (z0 + h)], key, -nc)
        npy = max(1, int(round(L / payanda)))
        for k in range(npy + 1):
            if k == 0 and (kapali or i > 0): continue
            t = k / npy
            p0 = a.lerp(b, t); p1 = a2.lerp(b2, t)
            w = 0.028
            # pilaster: a tapering buttress on the face
            ex = e * (w / 2)
            q0 = [V(p0.x, p0.y, z0) - ex, V(p0.x, p0.y, z0) + ex, V(p1.x, p1.y, z0 + h) + ex * 0.8, V(p1.x, p1.y, z0 + h) - ex * 0.8]
            d0, d1 = nc * 0.018, nc * 0.012
            fr = [q0[0] + d0, q0[1] + d0, q0[2] + d1, q0[3] + d1]
            y.yuz_yon(fr, key, nc + Z * egim)
            y.yuz_yon([q0[1], q0[2], fr[2], fr[1]], key, e)
            y.yuz_yon([q0[3], q0[0], fr[0], fr[3]], key, -e)
            if sivri_tepe:
                cc = (fr[2] + fr[3]) / 2 - nc * 0.01
                donel(y, (cc.x, cc.y), [(w * 0.55, z0 + h - 0.002), (w * 0.5, z0 + h + 0.025), (w * 0.3, z0 + h + 0.045), (0, z0 + h + 0.06)], key, n=8)
        if toron:
            nt = max(1, int(round(L / 0.05)))
            for rr in (0.38, 0.7):
                for k in range(nt):
                    t = (k + 0.5) / nt
                    p = a.lerp(b, t).lerp(a2.lerp(b2, t), rr) + Z * (z0 + h * rr)
                    cubuk(y, p - nc * 0.004, p + nc * 0.022, 0.005, 'ahsap_acik', 0.005)
    return z0 + h


def kerpic_kule(y, c, w, z0, h, key='kerpic', egim=0.25, toron=True, tepe=True):
    """a tapering square Sahel tower (Djinguereber / Sankore minaret): torons in rows, a ribbed top with pinnacles
    and an ostrich-egg finial. Returns the top z"""
    cx, cy = c
    w1 = w * (1 - egim)
    a0 = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2, z0)
    a1 = dikdortgen(cx - w1 / 2, cx + w1 / 2, cy - w1 / 2, cy + w1 / 2, z0 + h)
    nk = 4
    rings = [[p0.lerp(p1, k / nk) for p0, p1 in zip(a0, a1)] for k in range(nk + 1)]
    for k in range(nk):
        y.serit(rings[k], rings[k + 1], key)
    y.yuz_yon(a1, key, Z)
    if toron:
        for i in range(4):
            for rr in [0.15 + 0.15 * j for j in range(6)]:
                p, q = rings[0][i].lerp(a1[i], rr), rings[0][(i + 1) % 4].lerp(a1[(i + 1) % 4], rr)
                e = (q - p).normalized(); nc = V(e.y, -e.x)
                for k in range(4):
                    t = (k + 0.5) / 4
                    pp = p.lerp(q, t)
                    cubuk(y, pp - nc * 0.004, pp + nc * 0.02, 0.005, 'ahsap_acik', 0.005)
    zt = z0 + h
    if tepe:
        for p in a1:   # corner pinnacles
            cc = V(cx, cy).lerp(V(p.x, p.y), 0.85)
            donel(y, (cc.x, cc.y), [(w1 * 0.1, zt), (w1 * 0.09, zt + w1 * 0.25), (w1 * 0.05, zt + w1 * 0.38), (0, zt + w1 * 0.45)], key, n=8)
        donel(y, (cx, cy), [(w1 * 0.16, zt), (w1 * 0.13, zt + w1 * 0.4), (w1 * 0.07, zt + w1 * 0.62), (0, zt + w1 * 0.7)], key, n=10)
        kure(y, (cx, cy, zt + w1 * 0.74), w1 * 0.05, 'beyaz')
        return zt + w1 * 0.8
    return zt


# ---------------------------------------------------------------- banners, platforms, stairs
def sancak(y, x, yy, z, boy=0.2, en=0.1, yuk=0.065, aci=0.0, direk_key='ahsap', tepe_key='altin', dalga=0.012, n=6, kuyruk=False):
    """a banner: a pole from z (boy high) with a knob, and a waving flag in the team colour (key 'mavi': the game
    repaints it) flying towards angle aci. kuyruk: a swallow-tailed pennant"""
    y.silindir((x, yy), 0.006, z, z + boy, direk_key)
    kure(y, (x, yy, z + boy + 0.008), 0.009, tepe_key, n=8, kat=4)
    e = V(math.cos(aci), math.sin(aci)); nn = V(-e.y, e.x)
    o = V(x, yy, z + boy - 0.012 - yuk)
    def P(u, v, s):
        w = math.sin(u * math.pi * 1.6) * dalga * u
        return o + e * (0.006 + u * en) + nn * (w + s * 0.0015) + Z * v
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        if kuyruk and i >= n - 2:
            for v0, v1 in ((0, yuk * 0.45), (yuk * 0.55, yuk)):
                c0, c1 = (v0 + v1) / 2, (v0 + v1) / 2
                tip = 1 if i == n - 1 else 0
                q = [P(u0, v0, 1), P(u1, v0 + (c0 - v0) * 0.4 * tip, 1), P(u1, v1 - (v1 - c1) * 0.4 * tip, 1), P(u0, v1, 1)]
                y.yuz_yon(q, 'mavi', nn)
                y.yuz_yon([P(u0, v0, -1), P(u1, v0 + (c0 - v0) * 0.4 * tip, -1), P(u1, v1 - (v1 - c1) * 0.4 * tip, -1), P(u0, v1, -1)], 'mavi', -nn)   # (the back cut like the front)
                qb = [P(u0, v0, -1), P(u1, v0 + (c0 - v0) * 0.4 * tip, -1), P(u1, v1 - (v1 - c1) * 0.4 * tip, -1), P(u0, v1, -1)]
                for k, yon in ((0, -Z), (2, Z)) + (((1, e),) if tip else ()):   # (the rims, as on the plain flag)
                    y.yuz_yon([q[k], q[k + 1], qb[k + 1], qb[k]], 'mavi', yon)
            if i == n - 2:   # the notch's inner edge
                y.yuz_yon([P(u0, yuk * 0.45, 1), P(u0, yuk * 0.55, 1), P(u0, yuk * 0.55, -1), P(u0, yuk * 0.45, -1)], 'mavi', e)
            continue
        y.yuz_yon([P(u0, 0, 1), P(u1, 0, 1), P(u1, yuk, 1), P(u0, yuk, 1)], 'mavi', nn)
        y.yuz_yon([P(u0, 0, -1), P(u1, 0, -1), P(u1, yuk, -1), P(u0, yuk, -1)], 'mavi', -nn)
        # the cloth's rims (top, bottom, free end): seen edge-on the two sheets otherwise show each other's backs
        y.yuz_yon([P(u0, yuk, 1), P(u1, yuk, 1), P(u1, yuk, -1), P(u0, yuk, -1)], 'mavi', Z)
        y.yuz_yon([P(u0, 0, 1), P(u1, 0, 1), P(u1, 0, -1), P(u0, 0, -1)], 'mavi', -Z)
        if i == n - 1:
            y.yuz_yon([P(1, 0, 1), P(1, yuk, 1), P(1, yuk, -1), P(1, 0, -1)], 'mavi', e)
        if i == 0:   # the edge at the pole (the pole's flats leave a gap there)
            y.yuz_yon([P(0, 0, 1), P(0, yuk, 1), P(0, yuk, -1), P(0, 0, -1)], 'mavi', -e)
    return z + boy


def zemin(y, x0, x1, y0, y1, h=0.05, key='tas_koyu', ust='zemin', basamak=(('on', 0.4),), n_basamak=3, silmeli=True):
    """a platform (plinth) with a paved top and steps: basamak = ((side, width), ...), side 'on' (-y), 'arka' (+y),
    'sol' (-x), 'sag' (+x), width centred. Returns the top z"""
    kutu(y, V(x0, y0, 0), X, x1 - x0, y1 - y0, h, key, 'onarkasagsol')
    y.yuz([V(x0, y0, h), V(x1, y0, h), V(x1, y1, h), V(x0, y1, h)], ust)
    if silmeli:
        silme(y, dikdortgen(x0, x1, y0, y1), h - 0.008, 0.008, 0.006, key, 'duz')
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for side, w in basamak:
        d = 0.03
        for k in range(n_basamak):
            hh = h * (n_basamak - k) / (n_basamak + 1)
            if side == 'on': kutu(y, V(cx - w / 2, y0 - d * (k + 1), 0), X, w, d * (k + 1) + 0.001, hh, key, 'onsagsolust')
            elif side == 'arka': kutu(y, V(cx + w / 2, y1 + d * (k + 1), 0), -X, w, d * (k + 1) + 0.001, hh, key, 'onsagsolust')
            elif side == 'sol': kutu(y, V(x0 - d * (k + 1), cy + w / 2, 0), -Y, w, d * (k + 1) + 0.001, hh, key, 'onsagsolust')
            else: kutu(y, V(x1 + d * (k + 1), cy - w / 2, 0), Y, w, d * (k + 1) + 0.001, hh, key, 'onsagsolust')
    return h


def merdiven(y, a, yon, en, z0, z1, n=8, d=None, key='tas', yanlik=None):
    """a straight stair: its bottom front edge centred at a, climbing towards angle yon (radians), en wide, from z0
    to z1 in n steps of depth d; yanlik: a key for side walls (cheeks)"""
    e = V(math.cos(yon), math.sin(yon)); s = V(-e.y, e.x)
    d = d or (z1 - z0) * 1.1 / n
    a = V(a[0], a[1])
    for k in range(n):
        # each step a block from the ground up (so no gap shows beneath)
        p = a + e * (d * k)
        kutu_merkez(y, (p.x + e.x * d / 2, p.y + e.y * d / 2), d, en, (z1 - z0) * (k + 1) / n, key, z0=z0, aci=yon)
    if yanlik:
        for sg in (-1, 1):
            p0 = a + s * (sg * (en / 2 + 0.006))
            p1 = p0 + e * (d * n)
            cubuk(y, p0 + Z * (z0 + 0.012), p1 + Z * (z1 + 0.012), 0.012, yanlik, 0.024)


def havuz(y, x0, x1, y0, y1, z, derin=0.02, kenar=0.02, key='mermer', su='su'):
    """a rectangular pool: a raised kerb and the water surface a little below it"""
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, disa(k, kenar), z, z + 0.012, key)
    duvarlar(y, [k[3], k[2], k[1], k[0]], z - derin * 0.4, z + 0.012, key)
    for i in range(4):
        j = (i + 1) % 4
        o = disa(k, kenar)
        y.yuz_yon([o[i] + Z * (z + 0.012), o[j] + Z * (z + 0.012), k[j] + Z * (z + 0.012), k[i] + Z * (z + 0.012)], key, Z)
    y.yuz_yon([V(p.x, p.y, z - derin * 0.4) for p in k], su, Z)


def agac(y, x, yy, z=0.0, boy=0.12, tur='yapraklı', key='boya_yesil', govde='ahsap'):
    """a stylised tree for courtyards and gardens: yapraklı (round crown), servi (cypress), palmiye (palm)"""
    if tur == 'servi':
        y.prizma((x, yy), 0.004, z, z + boy * 0.15, govde, n=5)
        donel(y, (x, yy), [(0.012, z + boy * 0.1), (0.022, z + boy * 0.35), (0.018, z + boy * 0.7), (0, z + boy)], key, n=8)
    elif tur == 'palmiye':
        boru(y, [V(x, yy, z), V(x + 0.006, yy, z + boy * 0.5), V(x + 0.012, yy + 0.004, z + boy * 0.9)], 0.005, govde, n=5)
        top = V(x + 0.012, yy + 0.004, z + boy * 0.9)
        for i in range(7):
            a = TAU * i / 7
            d = V(math.cos(a), math.sin(a))
            boru(y, [top, top + d * 0.03 + Z * 0.01, top + d * 0.055 - Z * 0.012], 0.006, key, n=3, r_son=0.001)
    else:
        y.prizma((x, yy), 0.005, z, z + boy * 0.45, govde, n=5)
        kure(y, (x, yy, z + boy * 0.68), boy * 0.32, key, n=10, kat=5)


# ---------------------------------------------------------------- blind arches, muqarnas, muqarnas portal (Seljuk / Ottoman)
def kemer_yolu(x0, x1, hs, sivri=0.0, k_say=10):
    """the outline of an arch from (x0, hs) over the crown to (x1, hs) as (u, v) points, the same curve as Yapi.kemerli
    (sivri > 0: pointed, its rise sivri x span; 0: round)"""
    if sivri:
        w = x1 - x0; hr = sivri * w
        rho = (w * w / 4 + hr * hr) / w; c = x0 + rho
        ta = math.atan2(hr, (x0 + w / 2) - c); yari = k_say // 2
        sol = [(c + rho * math.cos(math.pi - (math.pi - ta) * k / yari), hs + rho * math.sin(math.pi - (math.pi - ta) * k / yari)) for k in range(1, yari + 1)]
        kemer = sol + [(x0 + x1 - u, v) for u, v in reversed(sol[:-1])]
    else:
        R = (x1 - x0) / 2
        kemer = [(x0 + R + R * math.cos(math.pi - math.pi * k / k_say), hs + R * math.sin(math.pi - math.pi * k / k_say)) for k in range(1, k_say)]
    return [(x0, hs)] + kemer + [(x1, hs)]


def kemer_nis(y, a, b, z0, H, en=0.8, ust=0.03, sivri=0.5, derin=0.015, key='tas', yan_key='tas_koyu', alt_key='tas_acik',
              arka_key=None, v0=0.0, k_say=10, cerceve=None):
    """a wall bay a->b (facing the right of a->b) with an arched opening that only goes derin deep: the wall face round
    the arch, the reveal (jambs and soffit) and, with arka_key, a flat back. Without arka_key the back is left open for
    the caller to fill (a back wall with windows, a door, a muqarnas hood). cerceve = (width, key or [keys]): a raised
    frame round the arch. Returns (L, x0, x1, hs, apex): L(u, v, d) the point u along, v above z0, d behind the line;
    x0..x1 the opening, hs the springing height, apex the crown height (both above z0)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v, d=0.0: a + e * u - nc * d + Z * (z0 + v)
    x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
    w = x1 - x0
    hs = H - ust - (sivri * w if sivri else w / 2)
    tp = kemer_yolu(x0, x1, hs, sivri, k_say)
    y.yuz_yon([L(0, 0), L(x0, 0), L(x0, H), L(0, H)], key, nc)
    y.yuz_yon([L(x1, 0), L(W, 0), L(W, H), L(x1, H)], key, nc)
    if v0 > 0: y.yuz_yon([L(x0, 0), L(x1, 0), L(x1, v0), L(x0, v0)], key, nc)
    for k in range(len(tp) - 1):
        (ua, va), (ub, vb) = tp[k], tp[k + 1]
        y.yuz_yon([L(ua, va), L(ub, vb), L(ub, H), L(ua, H)], key, nc)
    yol = [(x0, v0)] + tp + [(x1, v0)]
    xm = (x0 + x1) / 2
    for k in range(len(yol) - 1):
        p, q = yol[k], yol[k + 1]
        vm = min(max((p[1] + q[1]) / 2, v0), hs)
        mid = (L(*p) + L(*q)) / 2
        y.yuz_yon([L(*p), L(*q), L(*q, derin), L(*p, derin)], yan_key, L(xm, vm) - mid)
    if v0 > 0:
        y.yuz_yon([L(x0, v0), L(x1, v0), L(x1, v0, derin), L(x0, v0, derin)], alt_key, Z)
    if arka_key:
        y.yuz_yon([L(*p, derin) for p in yol], arka_key, nc)
    if cerceve:
        f, mlz = cerceve
        mlz = mlz if isinstance(mlz, (list, tuple)) else [mlz]
        d = -0.0025
        def dis(p):
            u, v = p
            if v <= hs + 1e-9:
                return (u - f if u < xm else u + f, v)
            kk = Vector((u - xm, v - hs)).normalized()
            return (u + kk.x * f, v + kk.y * f)
        for k in range(len(yol) - 1):
            p, q = yol[k], yol[k + 1]
            tas = mlz[0] if (p[1] <= hs + 1e-9 and q[1] <= hs + 1e-9) else mlz[k % len(mlz)]
            y.yuz_yon([L(*p, d), L(*q, d), L(*dis(q), d), L(*dis(p), d)], tas, nc)
            orta = (L(*dis(p), 0) + L(*dis(q), 0)) / 2
            y.yuz_yon([L(*dis(p), d), L(*dis(q), d), L(*dis(q), 0), L(*dis(p), 0)], mlz[0], orta - L(xm, (v0 + hs) / 2, 0))
    return L, x0, x1, hs, H - ust


def mukarnas(y, a, b, z0, h, derin, kat=4, hucre=None, keys=('tas_acik', 'tas', 'tas_koyu'), cep=None, sivri=0.72):
    """a muqarnas hood (stalactite vault) filling a niche behind the line a->b (the niche opens to the right of a->b
    and is derin deep): kat tiers corbelling forward from the back (at z0) to the line (at z0 + h); each tier a row of
    hucre small pointed cells (default: about square ones) recessed cep deep, alternate tiers offset by half a cell,
    stepped soffits between the tiers. keys: cell fronts, cell backs, reveals and soffits. The caller draws the
    niche's sides (up to z0 + h) and its back (up to z0)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    th = h / kat
    hucre = hucre or max(2, int(round(W / (th * 1.05))))
    cw = W / hucre
    cep = min(derin / kat * 0.85, cw * 0.4) if cep is None else cep
    Q = lambda u, d: a + e * u - nc * d          # (2D, z added by the callee)
    for k in range(kat):
        za, zb = z0 + th * k, z0 + th * (k + 1)
        dk, dn = derin * (1 - k / kat), derin * (1 - (k + 1) / kat)
        if k % 2 == 0:
            hucreler = [(i * cw, (i + 1) * cw, True) for i in range(hucre)]
        else:
            hucreler = [(0.0, cw / 2, False)] + [(cw / 2 + i * cw, cw / 2 + (i + 1) * cw, True) for i in range(hucre - 1)] + [(W - cw / 2, W, False)]
        for ua, ub, tam in hucreler:
            if not tam:
                duz_duvar(y, Q(ua, dk), Q(ub, dk), za, zb, keys[0]); continue
            L, x0, x1, hs, apex = kemer_nis(y, Q(ua, dk), Q(ub, dk), za, th, en=0.78, ust=th * 0.06, sivri=sivri, derin=cep,
                                            key=keys[0], yan_key=keys[2], arka_key=keys[1], k_say=6)
            y.yuz_yon([L(x0, 0), L(x1, 0), L(x1, 0, cep), L(x0, 0, cep)], keys[2], Z)       # the cell's floor
        # the soffit stepping forward to the next tier
        zs = zb - 0.0004   # (a hair below the cells' floors above it: back to back on one plane they flickered)
        y.yuz_yon([Q(0, dk) + Z * zs, Q(W, dk) + Z * zs, Q(W, dn) + Z * zs, Q(0, dn) + Z * zs], keys[2], -Z)


def tackapi_mukarnas(y, cx, cy, z0, en=0.3, H=0.45, derin=0.07, nis=0.6, sivri=0.5, kapi_key='ahsap', key='tas',
                     bordur=("tas_acik", "mermer"), mk_kat=4, kuleli=False, cerceve=(0.012, ["mermer", "tas_koyu"]), tonlar=("tas_acik", "tas_koyu")):
    """a Seljuk / Ottoman muqarnas portal (Sultanhanı, Bursa Ulu Camii) on the line y = cy facing -y, its block going
    derin back (+y): a tall frame with raised border bands, a pointed-arched niche (nis: its width share) whose head is a
    muqarnas hood, a framed rectangular door in the niche's back, colonnettes at the niche's edges and a crowning
    cornice. tonlar: the light and dark stone of the niche and mouldings. Returns the top z"""
    x0b, x1b = cx - en / 2, cx + en / 2
    ra = 0.01                                   # the arch's own depth
    nd = derin * 0.78                           # the niche's back, behind the front
    L, u0, u1, hs, apex = kemer_nis(y, V(x0b, cy), V(x1b, cy), z0, H, en=nis, ust=H * 0.12, sivri=sivri, derin=ra, key=key,
                                    yan_key=tonlar[0], k_say=12, cerceve=cerceve)
    # the niche: sides (up to the crown), the back with the door (up to the muqarnas), the hood
    zs = z0 + hs * 0.72
    for u, s in ((u0, 1), (u1, -1)):
        y.yuz_yon([L(u, 0, ra), L(u, 0, nd), L(u, apex + 0.002, nd), L(u, apex + 0.002, ra)], tonlar[1], V(s, 0))
    dikdortgen_acik(y, L(u0, 0, nd), L(u1, 0, nd), z0, zs - z0, 0.24, 0.76, 0.0, (zs - z0) * 0.62, (key, tonlar[1], tonlar[0], kapi_key),
                    derin=0.012, cerceve=(0.008, 'mermer'))
    pw = u1 - u0
    L2 = lambda u, v: L(u0 + u * pw, v, nd - 0.002)
    y.yuz_yon([L2(0.2, (zs - z0) * 0.72), L2(0.8, (zs - z0) * 0.72), L2(0.8, (zs - z0) * 0.9), L2(0.2, (zs - z0) * 0.9)], tonlar[0], -Y)
    mukarnas(y, L(u0, 0, ra), L(u1, 0, ra), zs, apex + 0.002 - (zs - z0), nd - ra, kat=mk_kat, keys=(tonlar[0], key, tonlar[1]))
    # the block's sides and top
    y.yuz_yon([V(x1b, cy, z0), V(x1b, cy + derin, z0), V(x1b, cy + derin, z0 + H), V(x1b, cy, z0 + H)], key, X)
    y.yuz_yon([V(x0b, cy + derin, z0), V(x0b, cy, z0), V(x0b, cy, z0 + H), V(x0b, cy + derin, z0 + H)], key, -X)
    # raised border bands: an outer band round the frame, an inner one round the arch's rectangle
    def bant(xa, xb, zb, w, key_, d):
        for (ua, va, ub, vb) in ((xa, z0, xa + w, zb), (xb - w, z0, xb, zb), (xa + w, zb - w, xb - w, zb)):
            kutu(y, V(ua, cy - d, va), X, ub - ua, d, vb - va, key_, 'onsagsolust')
    bw = en * 0.07
    bant(x0b, x1b, z0 + H - 0.016, bw, bordur[0], 0.006)
    hw = (u1 - u0) / 2 + 0.012 + bw * 0.6
    bant(cx - hw, cx + hw, z0 + apex + bw * 0.7, bw * 0.55, bordur[1], 0.004)
    # colonnettes at the niche's edges
    for u, s in ((u0, 1), (u1, -1)):
        p = L(u, 0, 0)
        c = (p.x + s * 0.006, cy - 0.003)
        y.prizma(c, 0.006, z0 + 0.014, z0 + hs, 'mermer', n=8, ust=False)
        y.prizma(c, 0.009, z0, z0 + 0.014, 'mermer', n=8)
        y.prizma(c, 0.009, z0 + hs, z0 + hs + 0.012, 'mermer', n=8)
    # cornice and top
    kornis(y, x0b, x1b, cy, cy + derin, z0 + H - 0.016, 0.018, 0.012, tonlar[0], 'tac')
    y.yuz_yon([V(x0b, cy, z0 + H + 0.002), V(x1b, cy, z0 + H + 0.002), V(x1b, cy + derin, z0 + H + 0.002), V(x0b, cy + derin, z0 + H + 0.002)], tonlar[0], Z)
    top = z0 + H + 0.002
    if kuleli:
        for sx in (-1, 1):
            y.prizma((cx + sx * en / 2, cy + 0.01), 0.018, z0 + H, z0 + H + 0.03, tonlar[0], n=8)
            y.koni((cx + sx * en / 2, cy + 0.01), 0.02, z0 + H + 0.03, 0.045, 'kursun', n=8)
            top = z0 + H + 0.075
    return top
