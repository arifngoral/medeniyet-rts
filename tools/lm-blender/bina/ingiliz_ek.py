# Helpers for the later English landmarks (lm_globe, lm_kraliyettersane, lm_bigben, lm_woolwich): copies of the
# square-headed openings from ingiliz_ortak.py (kept separate, that file belongs to the first four), Gothic Revival
# bays with buttresses and pinnacles, a clock dial, iron cresting, lamp standards, Georgian sash windows, river ground
# (water, embankment), barrels, cannon, stacks of shot and timber, small boats.
import math
from mathutils import Vector
from parcalar import *
from frank_ortak import kutu3, levha, insan, oturan


def eksen(a, b):
    """a, b as 2D points, the length, the unit direction and the outward normal (right of a->b)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    e = (b - a) / L
    return a, b, L, e, V(e.y, -e.x)


def acikli_duvar(y, a, b, z0, z1, aciklar, renk=('tas', 'tas_koyu', 'tas_acik', 'cam'), derin=0.012, cerceve=None, pay=0.003):
    """a wall a->b (facing the right) from z0 to z1 with square-headed openings: aciklar = [(u, w, v0, v1), ...]
    u the centre (0..1 along), w the width, v0..v1 the height above z0. Plain wall between them. Returns, for each
    opening, (pa, pb, v0, v1, e, nc): its two jambs (2D, on the wall line)"""
    a, b, L, e, nc = eksen(a, b)
    out = []
    u = 0.0
    m = pay / L
    for (uc, w, v0, v1) in sorted(aciklar):
        u0, u1 = uc - w / 2 / L, uc + w / 2 / L
        b0, b1 = u0 - m, u1 + m
        if b0 > u + 1e-6:
            duz_duvar(y, a.lerp(b, u), a.lerp(b, b0), z0, z1, renk[0])
        bw = b1 - b0
        dikdortgen_acik(y, a.lerp(b, b0), a.lerp(b, b1), z0, z1 - z0, m / bw, 1 - m / bw, v0, v1, renk, derin=derin, cerceve=cerceve)
        out.append((a.lerp(b, u0), a.lerp(b, u1), v0, v1, e, nc))
        u = b1
    if u < 1 - 1e-6:
        duz_duvar(y, a.lerp(b, u), b, z0, z1, renk[0])
    return out


def kayit(y, ac, z0, derin=0.012, key='beyaz', nu=2, nv=2, kalin=0.0035):
    """glazing bars of a sash window (Georgian): nu panes across, nv up, set in the reveal of an acikli_duvar opening"""
    pa, pb, v0, v1, e, nc = ac
    d = derin * 0.5
    for k in range(1, nu):
        p = pa.lerp(pb, k / nu) - nc * d
        cubuk3(y, p + Z * (z0 + v0), p + Z * (z0 + v1), kalin, key, nc, kalin * 0.8)
    for k in range(1, nv):
        v = v0 + (v1 - v0) * k / nv
        cubuk3(y, pa - nc * d + Z * (z0 + v), pb - nc * d + Z * (z0 + v), kalin * (1.4 if k * 2 == nv else 1), key, nc, kalin * 0.8)


def cubuk3(y, a, b, en, key, nc, kalin=None):
    """a bar a->b seen only from the front (nc) and its two sides: mullions and transoms in a reveal (half a cubuk)"""
    a, b, nc = Vector(a), Vector(b), Vector(nc).normalized()
    t = (b - a).normalized()
    u = nc.cross(t).normalized() * (en / 2)
    f = nc * ((kalin or en) / 2)
    y.yuz_yon([a - u + f, b - u + f, b + u + f, a + u + f], key, nc)
    for s in (-1, 1):
        y.yuz_yon([a + u * s + f, b + u * s + f, b + u * s - f, a + u * s - f], key, u * s)


# ---------------------------------------------------------------- Gothic Revival
def pinakl(y, cx, cy, z, w, h, key='kum', uc_key='kum_acik', tepe='altin', n=4):
    """a pinnacle: a w-wide shaft (square, or n-sided) for 0.42 h, a little cornice, a steep spirelet and a knob"""
    hs = h * 0.42
    if n == 4:
        kutu_merkez(y, (cx, cy), w, w, hs, key, z0=z, yuzler='onarkasagsolust')
        donel(y, (cx, cy), [(w * 0.78, z + hs), (w * 0.5, z + hs + (h - hs) * 0.5), (0.0, z + h)], uc_key, n=4, kat=math.pi / 4)
    else:
        donel(y, (cx, cy), [(w / 2, z), (w / 2, z + hs), (w * 0.62, z + hs + 0.003), (w * 0.4, z + hs + (h - hs) * 0.45), (0.0, z + h)], key, n=n)
    if tepe:
        kure(y, (cx, cy, z + h + w * 0.18), w * 0.22, tepe, n=4, kat=2)
    return z + h


def payanda(y, p, e, nc, z0, z1, w=0.014, d=0.01, key='kum', pin=0.05, pin_key='kum_acik', tepe='altin', basamak=True, arka=False):
    """a buttress on a wall line at p (2D), standing out d towards nc, w wide, z0..z1, its top a pinnacle pin high;
    basamak: a weathered set-off half-way (a sloping step)"""
    p = V(p[0], p[1])
    h = z1 - z0
    kutu3(y, p + nc * (d / 2) + Z * (z0 + h / 2), e, nc, Z, w, d, h, key, ('+x', '-x', '+y', '+z') + (('-y',) if arka else ()))
    if basamak:
        zm = z0 + h * 0.45
        kutu3(y, p + nc * (d * 0.8) + Z * (zm - 0.012), e, nc, Z, w * 1.12, d * 0.6, 0.024, key, ('+x', '-x', '+y', '-z'))
        A, B = p + nc * (d * 1.1) - e * (w * 0.56) + Z * zm, p + nc * (d * 1.1) + e * (w * 0.56) + Z * zm
        y.yuz_yon([A, B, B - nc * (d * 0.6) + Z * 0.012, A - nc * (d * 0.6) + Z * 0.012], key, nc + Z)
    if pin:
        pc = p + nc * (d / 2)
        pinakl(y, pc.x, pc.y, z1, w * 0.9, pin, key, pin_key, tepe)


def gotik_pencere(y, a, b, z0, H, renk=('kum', 'kum_koyu', 'kum_acik', 'cam'), en=0.5, v0=None, sivri=0.3, mullion=2,
                  cerceve=(0.0035, 'kum_acik'), hood=True, derin=0.016, k_say=4):
    """a Perpendicular Gothic window bay a->b (faces the right): a pointed opening with a raised frame, mullions and
    a transom in the reveal, a hood mould over it. Returns (L, W)"""
    a, b, L_, e, nc = eksen(a, b)
    v0 = H * 0.16 if v0 is None else v0
    ust = H * 0.1
    W, e_, nc_, L = y.kemerli(a, b, z0, H, renk, v0=v0, en=en, ust=ust, derin=derin, k_say=k_say, sivri=sivri, cerceve=cerceve)
    x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
    w = x1 - x0
    hs = H - ust - sivri * w
    if mullion:
        for k in range(1, mullion + 1):
            u = x0 + w * k / (mullion + 1)
            cubuk3(y, L(u, v0, derin * 0.5), L(u, hs + sivri * w * 0.55, derin * 0.5), 0.003, renk[2], nc, 0.0025)
        cubuk3(y, L(x0, v0 + (hs - v0) * 0.6, derin * 0.5), L(x1, v0 + (hs - v0) * 0.6, derin * 0.5), 0.003, renk[2], nc, 0.0025)
    if hood:
        top = H - ust * 0.35
        kutu3(y, L((x0 + x1) / 2, top, -0.004), e, nc, Z, w + 0.012, 0.006, 0.0045, renk[2], ('+x', '-x', '+y', '+z', '-z'))
    return L, W


def kresting(y, a, b, z, h=0.014, adim=0.034, key='demir', tepe='altin'):
    """iron cresting along a roof ridge a->b (3D points at the ridge height z): a rail and little spikes"""
    a, b = V(a[0], a[1], z), V(b[0], b[1], z)
    L = (b - a).length
    n = max(1, int(L / adim))
    e = (b - a).normalized(); nc = V(e.y, -e.x)
    for s in (-1, 1):   # a thin pierced-looking iron band (two faces back to back, closed on top)
        y.yuz_yon([a + nc * (s * 0.0008), b + nc * (s * 0.0008), b + nc * (s * 0.0008) + Z * (h * 0.6), a + nc * (s * 0.0008) + Z * (h * 0.6)], key, nc * s)
    y.yuz_yon([a + nc * 0.0008 + Z * (h * 0.6), b + nc * 0.0008 + Z * (h * 0.6), b - nc * 0.0008 + Z * (h * 0.6), a - nc * 0.0008 + Z * (h * 0.6)], key, Z)
    for i in range(n + 1):   # spikes, every third a gilded knob
        p = a.lerp(b, i / n) + Z * (h * 0.6)
        donel(y, (p.x, p.y), [(0.0022, p.z), (0.0, p.z + h * 0.6)], key, n=4)
        if tepe and i % 3 == 0:
            kure(y, (p.x, p.y, p.z + h * 0.6 + 0.002), 0.0026, tepe, n=4, kat=2)


def kadran(y, o, e, nc, r, cerceve=0.072, kare=True):
    """a clock face on a wall: o its centre on the wall plane, e along the wall, nc out. A gilded square surround
    (kare) with dark spandrels, a black iron ring, the white dial with hour marks and the hands"""
    o = Vector(o)
    up = Z
    P = lambda u, v, d: o + e * u + up * v + nc * d
    if kare:
        s = cerceve
        y.yuz_yon([P(-s, -s, 0.002), P(s, -s, 0.002), P(s, s, 0.002), P(-s, s, 0.002)], 'altin', nc)
        for (u0, v0, u1, v1, yon) in ((-s, s, s, s, up), (-s, -s, s, -s, -up), (-s, -s, -s, s, -e), (s, -s, s, s, e)):
            y.yuz_yon([P(u0, v0, 0), P(u1, v1, 0), P(u1, v1, 0.002), P(u0, v0, 0.002)], 'altin', yon)
        for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):   # dark spandrels in the corners
            k = s * 0.86
            y.yuz_yon([P(su * k, sv * k, 0.0028), P(su * k * 0.52, sv * k, 0.0028), P(su * k, sv * k * 0.52, 0.0028)], 'kobalt', nc)
    n = 24
    halka = lambda rr, d: [P(rr * math.cos(TAU * i / n), rr * math.sin(TAU * i / n), d) for i in range(n)]
    dis, ic = halka(r * 1.12, 0.0035), halka(r * 1.0, 0.0035)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([dis[i], dis[j], ic[j], ic[i]], 'koyu', nc)
    y.yuz_yon(halka(r, 0.004), 'beyaz', nc)
    for i in range(12):   # hour marks
        t = TAU * i / 12
        c, s_ = math.cos(t), math.sin(t)
        q = lambda rr, w: P(rr * c - w * s_, rr * s_ + w * c, 0.0046)
        ww = r * 0.05
        y.yuz_yon([q(r * 0.78, -ww), q(r * 0.94, -ww), q(r * 0.94, ww), q(r * 0.78, ww)], 'koyu', nc)
    for (t, l, w) in ((math.radians(60), 0.55, 0.06), (math.radians(-80), 0.82, 0.04)):   # the hands (ten past two)
        c, s_ = math.cos(t), math.sin(t)
        q = lambda rr, ww: P(rr * c - ww * s_, rr * s_ + ww * c, 0.0052)
        y.yuz_yon([q(-r * 0.12, -r * w), q(r * l, -r * w * 0.5), q(r * l, r * w * 0.5), q(-r * 0.12, r * w)], 'koyu', nc)
    y.yuz_yon([P(r * 0.07 * math.cos(TAU * i / 8), r * 0.07 * math.sin(TAU * i / 8), 0.0056) for i in range(8)], 'altin', nc)


def fener(y, x, yy, z, h=0.1, key='demir', isik='altin', kol=1):
    """a cast-iron lamp standard: a fluted post on a base, kol lanterns (1, or 3 on arms)"""
    kutu_merkez(y, (x, yy), 0.012, 0.012, 0.012, key, z0=z)
    y.prizma((x, yy), 0.0032, z + 0.012, z + h, key, n=6)
    tops = [(x, yy)] if kol == 1 else [(x + 0.016 * math.cos(TAU * k / 3), yy + 0.016 * math.sin(TAU * k / 3)) for k in range(3)]
    if kol != 1:
        for (px, py) in tops:
            cubuk(y, V(x, yy, z + h - 0.004), V(px, py, z + h), 0.0025, key)
    for (px, py) in tops:
        donel(y, (px, py), [(0.003, z + h), (0.0065, z + h + 0.004), (0.0065, z + h + 0.016), (0.008, z + h + 0.018), (0.0, z + h + 0.026)], isik, n=6)


# ---------------------------------------------------------------- Georgian / industrial
def sabun_pencere(y, a, b, z0, z1, n, v0, v1, renk=('tugla', 'tugla_koyu', 'tas_acik', 'cam'), kemer=False, nu=2, nv=3, derin=0.012,
                  lento=True, lento_key='tas_acik'):
    """a brick wall a->b with n evenly spaced Georgian sash windows (v0..v1 above z0), white glazing bars, stone sills
    and (lento) flat gauged-brick / stone lintels. Returns the openings"""
    a, b, L, e, nc = eksen(a, b)
    w = min(L / n * 0.5, (v1 - v0) * 0.62)
    acs = acikli_duvar(y, a, b, z0, z1, [((k + 0.5) / n, w, v0, v1) for k in range(n)], renk, derin=derin)
    for ac in acs:
        kayit(y, ac, z0, derin, 'beyaz', nu, nv)
        pa, pb = ac[0], ac[1]
        m = (pa + pb) / 2
        kutu3(y, m + nc * 0.004 + Z * (z0 + v0 - 0.003), e, nc, Z, w + 0.01, 0.008, 0.005, renk[2], ('+x', '-x', '+y', '+z', '-z'))
        if lento:
            kutu3(y, m + nc * 0.0015 + Z * (z0 + v1 + 0.006), e, nc, Z, w + 0.012, 0.003, 0.012, lento_key, ('+x', '-x', '+y', '+z', '-z'))
    return acs


def varil(y, x, yy, z, r=0.012, h=0.03, key='ahsap', cember='demir', yatik=None):
    """a powder barrel (bulging staves, iron hoops); yatik: lying on its side along angle yatik"""
    pr = [(r * 0.82, 0.0), (r * 0.95, h * 0.2), (r, h * 0.5), (r * 0.95, h * 0.8), (r * 0.82, h)]
    if yatik is None:
        donel(y, (x, yy), [(0.0, z)] + [(rr, z + zz) for rr, zz in pr] + [(0.0, z + h)], key, n=8)
        for zz in (0.18, 0.82):
            donel(y, (x, yy), [(r * 0.955, z + h * zz - 0.0015), (r * 0.975, z + h * zz), (r * 0.955, z + h * zz + 0.0015)], cember, n=8)
    else:
        e = V(math.cos(yatik), math.sin(yatik))
        o = V(x, yy, z + r)
        a = o - e * (h / 2)
        pts = [a + e * zz for rr, zz in pr]
        boru(y, pts, r * 0.95, key, n=8)


def gulle_yigini(y, x, yy, z, n=4, r=0.008, key='demir', aci=0.0):
    """a square pyramid of round shot, n balls a side"""
    c, s = math.cos(aci), math.sin(aci)
    for k in range(n):
        m = n - k
        for i in range(m):
            for j in range(m):
                u = (i - (m - 1) / 2) * 2 * r
                v = (j - (m - 1) / 2) * 2 * r
                kure(y, (x + c * u - s * v, yy + s * u + c * v, z + r + k * r * 1.414), r, key, n=6, kat=3)


def top_namlu(y, o, yon, L=0.12, r=0.014, key='bronz', agiz=True):
    """a gun barrel lying along yon from its breech knob at o (3D): tapered, reinforced rings, a dark muzzle"""
    o = Vector(o); yon = Vector(yon).normalized()
    b = o + yon * L
    boru(y, [o, o + yon * (L * 0.35), b], r, key, n=10, r_son=r * 0.72)
    for t, rr in ((0.04, 1.12), (0.35, 1.06), (0.97, 0.86)):
        p = o + yon * (L * t)
        boru(y, [p - yon * 0.004, p + yon * 0.004], r * rr * (1 - 0.28 * t), key, n=10)
    kure(y, o - yon * (r * 0.5), r * 0.5, key, n=6, kat=3)
    if agiz:
        u = Z.cross(yon)
        if u.length < 1e-4: u = X.copy()
        u.normalize(); w = yon.cross(u)
        y.yuz_yon([b + yon * 0.0008 + (u * math.cos(TAU * i / 8) + w * math.sin(TAU * i / 8)) * (r * 0.42) for i in range(8)], 'koyu', yon)


def top_kizak(y, x, yy, z, aci, L=0.12, r=0.013, key='bronz', govde='ahsap'):
    """a naval / garrison gun on a four-truck carriage (stepped cheeks, small wheels), muzzle towards aci"""
    with parca(y, (x, yy, z), aci):
        for s in (-1, 1):
            for k, (u0, u1, h) in enumerate(((-0.04, 0.035, 0.016), (-0.04, 0.012, 0.026), (-0.04, -0.012, 0.034))):
                kutu3(y, V((u0 + u1) / 2, s * 0.013, h / 2 + 0.006), X, Y, Z, u1 - u0, 0.006, h, govde)
        kutu3(y, V(0.0, 0.0, 0.009), X, Y, Z, 0.07, 0.02, 0.006, govde, ('+x', '-x', '+y', '-y', '+z'))
        for u in (-0.03, 0.026):
            boru(y, [V(u, -0.022, 0.006), V(u, 0.022, 0.006)], 0.0025, 'demir', n=5)
            for s in (-1, 1):
                boru(y, [V(u, s * 0.017, 0.006), V(u, s * 0.021, 0.006)], 0.006, govde, n=8)
    with parca(y, (x, yy, z), aci):
        top_namlu(y, V(-0.035, 0, 0.03), V(1, 0, 0.04), L, r, key)


def kereste(y, x, yy, z, L=0.14, n=4, kat=3, en=0.014, key='ahsap_acik', aci=0.0, uc='ahsap'):
    """a stack of squared timbers along angle aci: kat layers of n baulks, crossed sticks between"""
    with parca(y, (x, yy, z), aci):
        for k in range(kat):
            zz = k * (en + 0.004)
            for i in range(n):
                v = (i - (n - 1) / 2) * en * 1.15
                kutu3(y, V(0, v, zz + 0.004 + en / 2), X, Y, Z, L, en, en, key, ('+y', '-y', '+z'))
                for s in (-1, 1):
                    y.yuz_yon([V(s * L / 2, v - en / 2, zz + 0.004), V(s * L / 2, v + en / 2, zz + 0.004), V(s * L / 2, v + en / 2, zz + 0.004 + en),
                               V(s * L / 2, v - en / 2, zz + 0.004 + en)], uc, V(s, 0, 0))
            for s in (-0.35, 0.35):
                kutu3(y, V(s * L, 0, zz + 0.002), X, Y, Z, 0.006, n * en * 1.15 + 0.004, 0.004, 'ahsap_koyu', ('+x', '-x', '+y', '-y', '+z'))


def sandal(y, x, yy, z, aci=0.0, L=0.09, B=0.022, key='ahsap', ic='ahsap_acik', kurek=True):
    """a small rowing boat floating at z (waterline), along aci: a pointed hull, thwarts, oars"""
    def hb(u):   # half beam along -1..1
        return B * max(0.05, 1 - abs(u) ** 2.2)
    n = 8
    us = [-1 + 2 * i / n for i in range(n + 1)]
    with parca(y, (x, yy, z), aci):
        g, k = 0.012, -0.006
        for s in (-1, 1):
            for i in range(n):
                ua, ub = us[i], us[i + 1]
                q = [V(ua * L / 2, s * hb(ua), g), V(ub * L / 2, s * hb(ub), g), V(ub * L / 2, s * hb(ub) * 0.45, k), V(ua * L / 2, s * hb(ua) * 0.45, k)]
                yuz_dis(y, q, key, V((ua + ub) * L / 4 * 0.5, 0, g * 1.5))
        P = lambda u, f, zz: V(u * L / 2, f * hb(u), zz)
        for i in range(n):   # the floor, the inner side of the gunwale above it and the gunwale's top, quad by quad
            ua, ub = us[i], us[i + 1]
            y.yuz_yon([P(ua, -0.78, g * 0.6), P(ub, -0.78, g * 0.6), P(ub, 0.78, g * 0.6), P(ua, 0.78, g * 0.6)], ic, Z)
            for s in (-1, 1):
                y.yuz_yon([P(ua, s * 0.78, g * 0.6), P(ub, s * 0.78, g * 0.6), P(ub, s * 0.95, g), P(ua, s * 0.95, g)], key, V(0, -s, 0.3))
                y.yuz_yon([P(ua, s * 0.95, g), P(ub, s * 0.95, g), P(ub, s, g), P(ua, s, g)], 'ahsap_koyu', Z)
        for u in (-0.3, 0.25):
            kutu3(y, V(u * L / 2, 0, g * 0.75), X, Y, Z, 0.008, 2 * hb(u) * 0.92, 0.003, 'ahsap_koyu')
        if kurek:
            for s in (-1, 1):
                cubuk(y, V(0.0, s * B * 0.9, g), V(-0.012, s * B * 2.6, -0.002), 0.0022, 'ahsap_acik')


def su_ve_kiyi(y, x0, x1, y0, y1, zw, z_kara, kiyi_y, kenar_key='granit', rihtim=True):
    """a strip of water (river) x0..x1, y0..kiyi_y with its surface at zw, the bed's sides down to 0 (front and ends),
    and the embankment face at kiyi_y rising from below the water to z_kara (rihtim: stone, with a coping)"""
    kutu(y, V(x0, y0, 0), X, x1 - x0, kiyi_y - y0, zw - 0.0005, 'kaya_koyu', 'onsagsol')
    y.yuz_yon([V(x0, y0, zw), V(x1, y0, zw), V(x1, kiyi_y, zw), V(x0, kiyi_y, zw)], 'su', Z)
    if rihtim:
        duz_duvar(y, V(x0, kiyi_y), V(x1, kiyi_y), zw - 0.006, z_kara, kenar_key)
        silme(y, [V(x0, kiyi_y), V(x1, kiyi_y)], z_kara - 0.006, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)



def dalga(y, x0, x1, y0, y1, zw, n=30, tohum=3, key='beyaz', boy=0.03):
    """small light ripple strokes on a water surface (flat slivers a hair above it)"""
    import random
    r = random.Random(tohum)
    for i in range(n):
        x, yy = r.uniform(x0, x1), r.uniform(y0, y1)
        L = boy * r.uniform(0.6, 1.3)
        y.yuz_yon([V(x - L / 2, yy, zw + 0.0012), V(x + L / 2, yy, zw + 0.0012), V(x + L * 0.3, yy + 0.003, zw + 0.0012), V(x - L * 0.3, yy + 0.003, zw + 0.0012)],
                  'su_acik' if key == 'su_acik' else key, Z)


def bolum_say(y):
    """prints the triangles of each section (y.bolum) — to see where the budget goes"""
    b = getattr(y, 'bolumler', [])
    for i, (bas, ad) in enumerate(b):
        son = b[i + 1][0] if i + 1 < len(b) else len(y.faces)
        print('BOLUM %6d  %s' % (sum(len(p) - 2 for p, _ in y.faces[bas:son]), ad))


def dormer(y, c, nc, zc, w=0.03, h=0.03, d=0.05, duvar='kum', cati_key='arduvaz', cam='cam', cerceve='kum_acik'):
    """a small gabled dormer on a roof slope: c (2D) where its front stands on the slope at height zc, nc the
    horizontal direction down the slope; its sides and roof run back d into the roof (deep enough to be buried)"""
    c = V(c[0], c[1]); nc = V(nc[0], nc[1]).normalized(); e = V(-nc.y, nc.x)
    z0, z1 = zc - 0.012, zc + h
    A, B = c - e * (w / 2), c + e * (w / 2)
    y.yuz_yon([A + Z * z0, B + Z * z0, B + Z * z1, A + Z * z1], duvar, nc)
    for P_, s in ((A, -1), (B, 1)):
        y.yuz_yon([P_ + Z * z0, P_ - nc * d + Z * z0, P_ - nc * d + Z * z1, P_ + Z * z1], duvar, e * s)
    m = c + nc * 0.0015
    y.yuz_yon([m - e * (w * 0.34) + Z * (zc + 0.002), m + e * (w * 0.34) + Z * (zc + 0.002), m + e * (w * 0.34) + Z * (z1 - 0.004), m - e * (w * 0.34) + Z * (z1 - 0.004)], cerceve, nc)
    m = c + nc * 0.0025
    y.yuz_yon([m - e * (w * 0.24) + Z * (zc + 0.005), m + e * (w * 0.24) + Z * (zc + 0.005), m + e * (w * 0.24) + Z * (z1 - 0.008), m - e * (w * 0.24) + Z * (z1 - 0.008)], cam, nc)
    T = c + Z * (z1 + w * 0.45)
    y.yuz_yon([A + Z * z1, B + Z * z1, T], duvar, nc)
    L, R = A - e * 0.004 + nc * 0.005 + Z * (z1 - 0.003), B + e * 0.004 + nc * 0.005 + Z * (z1 - 0.003)
    T2 = T + nc * 0.005 + Z * 0.002
    Dv = -nc * (d + 0.005)
    y.yuz_yon([L, T2, T2 + Dv, L + Dv], cati_key, -e + Z)
    y.yuz_yon([T2, R, R + Dv, T2 + Dv], cati_key, e + Z)
    # the undersides of the overhanging eaves (seen from below they showed as holes)
    dz = Z * -0.0025   # (a hair under the roof plane: back to back with it they flickered)
    y.yuz_yon([L + dz, T2 + dz, T2 - nc * 0.012 + dz, L - nc * 0.012 + dz], cati_key, e - Z)
    y.yuz_yon([T2 + dz, R + dz, R - nc * 0.012 + dz, T2 - nc * 0.012 + dz], cati_key, -e - Z)
    for P_ in (L, R):   # the roof's thin edges at the eave corners
        y.yuz_yon([P_, P_ + dz, P_ - nc * 0.012 + dz, P_ - nc * 0.012], cati_key, (P_ - T2).normalized())
    for P_, Q_ in ((L, T2), (T2, R)):   # and along the front verges
        y.yuz_yon([P_, Q_, Q_ + dz, P_ + dz], cati_key, nc)
