# Norse timber parts shared by the Viking landmark scripts (bina/lm_uzunev.py, lm_hof.py, lm_thing.py, lm_naust.py):
# a bow-sided longhouse with a swaybacked roof (thatch / turf / shingles), leaning outer posts, porches, crossed gable
# boards ending in dragon heads and smoke louvres; a carved dragon head, a round shield, a rune stone, a wattle fence,
# a woodpile, a drying rack, a pine. Built like parcalar.py: faces wound outward, local origin, place with parca().
import math
from mathutils import Vector
from parcalar import *


def ejder(y, p, yon, s=0.1, key='ahsap_koyu', goz='altin', dil='boya_kirmizi', egim=0.0):
    """a carved dragon head on a curving neck rising from p, looking towards yon (horizontal); s its size.
    egim: the neck leans that much further forward (a prow post: 0.3)"""
    p = Vector(p); d = Vector((yon[0], yon[1], 0)).normalized(); sd = Z.cross(d)
    a = p
    b = p + d * (0.10 + egim * 0.2) * s + Z * 0.32 * s
    c = p + d * (0.34 + egim * 0.4) * s + Z * 0.60 * s
    h = p + d * (0.66 + egim * 0.5) * s + Z * 0.70 * s
    boru(y, [a, b, c, h], 0.12 * s, key, n=8, r_son=0.09 * s)
    kure(y, h, 0.115 * s, key, n=10, kat=5)
    # upper jaw (snout) and the open lower jaw, a tongue between
    boru(y, [h, h + d * 0.24 * s + Z * 0.02 * s, h + d * 0.46 * s - Z * 0.03 * s], 0.085 * s, key, n=7, r_son=0.045 * s)
    kure(y, h + d * 0.46 * s - Z * 0.02 * s, 0.05 * s, key, n=6, kat=3)
    boru(y, [h - Z * 0.05 * s, h + d * 0.2 * s - Z * 0.13 * s, h + d * 0.36 * s - Z * 0.15 * s], 0.045 * s, key, n=5, r_son=0.024 * s)
    boru(y, [h + d * 0.12 * s - Z * 0.06 * s, h + d * 0.34 * s - Z * 0.07 * s, h + d * 0.44 * s - Z * 0.12 * s], 0.012 * s, dil, n=4, r_son=0.006 * s)
    # a crest curling back over the neck, and two ears
    boru(y, [h + Z * 0.06 * s, h - d * 0.1 * s + Z * 0.22 * s, h - d * 0.3 * s + Z * 0.22 * s, h - d * 0.36 * s + Z * 0.1 * s],
         0.045 * s, key, n=5, r_son=0.016 * s)
    for sg in (-1, 1):
        boru(y, [h + sd * sg * 0.05 * s + Z * 0.04 * s, h + sd * sg * 0.09 * s - d * 0.1 * s + Z * 0.14 * s], 0.02 * s, key, n=4, r_son=0.006 * s)
        kure(y, h + d * 0.12 * s + Z * 0.04 * s + sd * sg * 0.09 * s, 0.03 * s, goz, n=6, kat=3)


def kalkan(y, c, yon, r=0.03, renk=('boya_kirmizi', 'boya_sari'), umbo='demir', n=12, kalin=0.004):
    """a round shield standing on its rim edge, its face towards yon (any 3D direction): painted halves or quarters
    (renk keys alternate), a rim and an iron boss"""
    c = Vector(c); f = Vector(yon).normalized()
    u = Z.cross(f)
    if u.length < 1e-4: u = X.copy()
    u.normalize(); w = f.cross(u)
    P = lambda rr, t, d: c + (u * math.cos(t) + w * math.sin(t)) * rr + f * d
    m = len(renk)
    for i in range(n):
        t0, t1 = TAU * i / n, TAU * (i + 1) / n
        k = renk[(i * m * 2 // n) % m]   # (halves / quarters)
        y.yuz_yon([P(0, 0, kalin), P(r, t0, kalin * 0.6), P(r, t1, kalin * 0.6)], k, f)
        y.yuz_yon([P(r, t0, kalin * 0.6), P(r, t1, kalin * 0.6), P(r, t1, -kalin * 0.4), P(r, t0, -kalin * 0.4)], 'ahsap_koyu', u * math.cos((t0 + t1) / 2) + w * math.sin((t0 + t1) / 2))
        y.yuz_yon([P(0, 0, -kalin * 0.4), P(r, t0, -kalin * 0.4), P(r, t1, -kalin * 0.4)], 'ahsap', -f)
    kure(y, c + f * (kalin + 0.002), r * 0.22, umbo, n=8, kat=3)


def runik_tas(y, c, aci=0.0, en=0.17, boy=0.42, kalin=0.05, key='granit', bant='boya_kirmizi', yazi='koyu', ikinci='boya_sari'):
    """a raised rune stone (Jelling style): a thick slab with a rounded, slightly lopsided top; on both faces a painted
    serpent band runs round the edge with rune strokes in it, a cross-knot in the middle. Faces -y before turning"""
    with parca(y, (c[0], c[1], c[2] if len(c) > 2 else 0.0), aci):
        def kontur(i_):   # outline inset by i_
            pts = []
            w0, w1 = en / 2 - i_, en / 2 * 0.86 - i_
            hs = boy * 0.62
            pts.append((-w0, i_ * 0.5)); pts.append((w0, i_ * 0.5))
            pts.append((w1, hs))
            for k in range(1, 8):
                t = math.pi * k / 8
                pts.append((w1 * math.cos(t) + 0.01 * math.sin(t), hs + (boy - hs - i_) * math.sin(t) * (1 + 0.08 * math.cos(t))))
            pts.append((-w1, hs))
            return pts
        dis = kontur(0.0)
        for sy in (-1, 1):
            yy = sy * kalin / 2
            y.yuz_yon([V(u, yy, v) for u, v in dis], key, V(0, sy))
        n = len(dis)
        for i in range(n):
            (ua, va), (ub, vb) = dis[i], dis[(i + 1) % n]
            if va < 1e-6 and vb < 1e-6: continue
            m = V((ua + ub) / 2, 0, (va + vb) / 2) - V(0, 0, boy * 0.4)
            y.yuz_yon([V(ua, -kalin / 2, va), V(ub, -kalin / 2, vb), V(ub, kalin / 2, vb), V(ua, kalin / 2, va)], key, V(m.x, 0, m.z))
        # the serpent band (between two insets) on both faces, and rune strokes in it
        a_, b_ = kontur(0.012), kontur(0.04)
        for sy in (-1, 1):
            yy = sy * (kalin / 2 + 0.0025)
            for i in range(1, len(a_) - 1):
                j = i + 1
                if j >= len(a_): break
                q = [V(a_[i][0], yy, a_[i][1]), V(a_[j][0], yy, a_[j][1]), V(b_[j][0], yy, b_[j][1]), V(b_[i][0], yy, b_[i][1])]
                y.yuz_yon(q, bant, V(0, sy))
            # (the band's last side, back down to the foot)
            q = [V(a_[-1][0], yy, a_[-1][1]), V(a_[0][0], yy, a_[0][1] + 0.02), V(b_[0][0], yy, b_[0][1] + 0.02), V(b_[-1][0], yy, b_[-1][1])]
            y.yuz_yon(q, bant, V(0, sy))
            yy2 = sy * (kalin / 2 + 0.0035)
            for i in range(1, len(a_) - 1, 1):
                (ua, va), (ub, vb) = a_[i], b_[i]
                mu, mv = (ua + ub) / 2, (va + vb) / 2
                for k in range(2):
                    du = 0.003 if k else -0.003
                    y.yuz_yon([V(mu + du - 0.0015, yy2, mv - 0.009), V(mu + du + 0.0015, yy2, mv - 0.009), V(mu + du + 0.0015, yy2, mv + 0.009), V(mu + du - 0.0015, yy2, mv + 0.009)], yazi, V(0, sy))
            # a ring-cross knot in the middle (a beast on the other face would need more polygons than it is worth)
            cz = boy * 0.5
            for i in range(10):
                t0, t1 = TAU * i / 10, TAU * (i + 1) / 10
                q = [V(0.028 * math.cos(t0), yy, cz + 0.028 * math.sin(t0)), V(0.028 * math.cos(t1), yy, cz + 0.028 * math.sin(t1)),
                     V(0.019 * math.cos(t1), yy, cz + 0.019 * math.sin(t1)), V(0.019 * math.cos(t0), yy, cz + 0.019 * math.sin(t0))]
                y.yuz_yon(q, ikinci, V(0, sy))
            for (u0, v0, u1, v1) in ((-0.004, cz - 0.045, 0.004, cz + 0.045), (-0.045, cz - 0.004, 0.045, cz + 0.004)):
                y.yuz_yon([V(u0, yy2, v0), V(u1, yy2, v0), V(u1, yy2, v1), V(u0, yy2, v1)], bant, V(0, sy))


def dikili_tas(y, x, yy, z, h, r=0.03, key='granit', tohum=0, egik=0.0):
    """a rough standing stone: a flattened, tapering block (six-sided), tilted a little"""
    import random
    rg = random.Random(tohum)
    a0 = rg.uniform(0, math.pi)
    sx, sy = math.cos(a0), math.sin(a0)
    tx, ty = rg.uniform(-1, 1) * egik, rg.uniform(-1, 1) * egik
    def halka(zz, rr):
        out = []
        for i in range(6):
            t = TAU * i / 6
            u, v = rr * math.cos(t) * (1 + 0.1 * rg.uniform(-1, 1)), rr * 0.55 * math.sin(t)
            out.append(V(x + u * sx - v * sy + tx * zz, yy + u * sy + v * sx + ty * zz, z + zz))
        return out
    rs = [halka(0, r), halka(h * 0.5, r * 0.96), halka(h * 0.85, r * 0.8)]
    for k in range(2):
        y.serit(rs[k], rs[k + 1], key)
    tepe = V(x + tx * h, yy + ty * h, z + h)
    for i in range(6):
        y.yuz([rs[2][i], rs[2][(i + 1) % 6], tepe], key)


def cit_orgu(y, a, b, z0, h=0.06, key='ahsap_acik', direk='kutuk', adim=0.07):
    """a wattle fence a->b: stakes and a woven panel (a thin box) with rails on both faces"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-4: return
    e = (b - a) / L; nn = V(e.y, -e.x)
    kutu(y, a - nn * 0.003 + Z * (z0 + 0.008), e, L, 0.006, h * 0.85, key, 'onarkasagsolust')
    for s in (-1, 1):
        for zz in (0.3, 0.62):
            cubuk(y, a + nn * s * 0.0045 + Z * (z0 + 0.008 + h * 0.85 * zz), b + nn * s * 0.0045 + Z * (z0 + 0.008 + h * 0.85 * zz), 0.004, 'ahsap', 0.002)
    n = max(1, int(round(L / adim)))
    for k in range(n + 1):
        p = a.lerp(b, k / n)
        y.prizma((p.x, p.y), 0.0055, z0, z0 + h * 1.08, direk, n=5, kat=k)


def odun_yigini(y, c, aci=0.0, L=0.14, n=5, r=0.011, kat=4, key='kutuk', uc='ahsap_acik'):
    """a stack of split logs: rows getting shorter up the pile, log ends light (cut wood)"""
    with parca(y, (c[0], c[1], c[2] if len(c) > 2 else 0.0), aci):
        for k in range(kat):
            m = n - k
            for i in range(m):
                x = (i - (m - 1) / 2) * r * 2.05
                zz = r + k * r * 1.75
                a, b = V(x, -L / 2, zz), V(x, L / 2, zz)
                boru(y, [a, b], r, key, n=6, kapat=False)
                for p, s in ((a, -1), (b, 1)):
                    y.yuz_yon([p + (X * math.cos(TAU * j / 6) + Z * math.sin(TAU * j / 6)) * r for j in range(6)], uc, V(0, s))
        # two stakes holding the ends
        for sx in (-1, 1):
            x = sx * (n * r * 1.05 + 0.004)
            for sy in (-0.4, 0.4):
                y.prizma((x, sy * L), 0.004, 0, kat * r * 1.9, 'ahsap_koyu', n=4)


def hjell(y, c, aci=0.0, L=0.26, h=0.13, key='ahsap', mal='granit', n=9):
    """a drying rack (hjell): A-frames at both ends carrying a ridge pole and a lower pole, fish / hides hung over them"""
    with parca(y, (c[0], c[1], c[2] if len(c) > 2 else 0.0), aci):
        for sx in (-1, 1):
            x = sx * L / 2
            cubuk(y, V(x, -0.05, 0), V(x, 0.008, h + 0.012), 0.008, key)
            cubuk(y, V(x, 0.05, 0), V(x, -0.008, h + 0.012), 0.008, key)
        cubuk(y, V(-L / 2 - 0.02, 0, h), V(L / 2 + 0.02, 0, h), 0.009, 'ahsap_koyu')
        for sy in (-1, 1):
            cubuk(y, V(-L / 2, sy * 0.028, h * 0.45), V(L / 2, sy * 0.028, h * 0.45), 0.006, 'ahsap_koyu')
        for i in range(n):
            x = -L / 2 + L * (i + 0.5) / n
            for sy in (-1, 1):
                kutu_merkez(y, (x, sy * 0.008), 0.016, 0.004, 0.05, mal, z0=h - 0.052)
                kutu_merkez(y, (x, sy * 0.008), 0.008, 0.005, 0.012, 'ahsap_acik', z0=h - 0.064)


def cam_agaci(y, x, yy, z=0.0, boy=0.3, key='boya_yesil', govde='ahsap', kat=4):
    """a spruce / pine: a trunk and stacked drooping cones"""
    y.prizma((x, yy), boy * 0.035, z, z + boy * 0.3, govde, n=6)
    for k in range(kat):
        t = k / kat
        r = boy * (0.3 - 0.2 * t)
        z0 = z + boy * (0.18 + 0.68 * t)
        donel(y, (x, yy), [(0.0, z0 + 0.005), (r, z0), (r * 0.55, z0 + boy * 0.12), (0.0, z0 + boy * 0.3)], key, n=10, kat=k * 0.4)


def koyun(y, x, yy, z, aci=0.0, renk='kece'):
    """a sheep: a woolly body, a dark head and legs"""
    with parca(y, (x, yy, z), aci):
        for sx in (-1, 1):
            for sy in (-1, 1):
                y.prizma((sx * 0.012, sy * 0.007), 0.0028, 0, 0.016, 'koyu', n=4)
        kure(y, (0, 0, 0.026), 0.017, renk, n=8, kat=4)
        kure(y, (0.006, 0, 0.03), 0.015, renk, n=8, kat=4)
        boru(y, [V(0.016, 0, 0.03), V(0.03, 0, 0.034), V(0.038, 0, 0.028)], 0.007, 'koyu', n=5, r_son=0.005)


# ---------------------------------------------------------------- the longhouse
def langhus(y, L, W, h, H, z0=0.0, bombe=0.14, sacak=0.055, cati='saz', mahya='cimen', kalin=0.032, n=18, nr=8,
            duvar='ahsap_dikey', ayak='granit', dikme=0.11, kapilar=((-0.2, -1), (0.2, -1)), ejder_s=0.11, ejder_key='ahsap_koyu',
            dumanlik=(0.0,), ext=0.05, sirt=0.08, dilim=None, sus='boya_kirmizi', ucluk='ahsap_dikey', sundurma=True,
            kat_lip=0.008, kalkanlar=None, egri=0.15, sundurma_h=0.82, sundurma_c=0.09, kroker=0.0, uc_kapi=(),
            yama=0, yama_key=None, tohum=0, cati_merdiven=(), saz_cizgi=0):
    """a Norse longhouse along x round the origin: bow-sided plank walls (bombe: how much narrower the ends are) on a
    stone footing, leaning outer posts under the eaves every dikme (Trelleborg), a steep roof H high with a swayback
    ridge (sirt: the ends that much higher), a thick eave (thatch saz / turf cimen / shingles), gables of vertical boards,
    crossed barge boards ending in dragon heads, smoke louvres on the ridge (x positions), porched doors at
    kapilar = ((x, side), ...) (side -1 front -y, +1 back). Returns the ridge z at the middle"""
    zw = z0 + h
    hw = lambda x: W / 2 * (1 - bombe * (2 * max(-L / 2, min(L / 2, x)) / L) ** 2)
    zr = lambda x: zw + H * (1 + sirt * (2 * max(-L / 2, min(L / 2, x)) / L) ** 2)
    g = lambda t: t * (1 + egri - egri * t)      # (a bulging slope: steeper at the eave)

    def ze(x):   # the eave height that puts the roof just over the wall top at the wall line
        tw = sacak / (hw(x) + sacak)
        return (zw + 0.004 - zr(x) * g(tw)) / (1 - g(tw))

    def P(x, sy, t):
        return V(x, sy * (hw(x) + sacak) * (1 - t), ze(x) + (zr(x) - ze(x)) * g(t))

    # walls on a footing
    xs = [-L / 2 + L * i / n for i in range(n + 1)]
    poly = [V(x, -hw(x)) for x in xs] + [V(x, hw(x)) for x in reversed(xs)]
    duvarlar(y, poly, z0, zw, duvar)
    silme(y, poly, z0, 0.03, 0.012, ayak, 'kaide')
    # a wall plate under the eave (reads as the top of the timber frame)
    silme(y, poly, zw - 0.018, 0.012, 0.006, 'ahsap_koyu', 'duz')

    # roof slopes
    xr = [-L / 2 - ext + (L + 2 * ext) * i / n for i in range(n + 1)]
    kk = (lambda j: dilim[j % len(dilim)]) if dilim else (lambda j: cati)
    # courses: each row starts a lip proud of the one below (layered thatch / overlapping shingles)
    NL = lambda sy: V(0, sy * 0.55, 0.83).normalized() * kat_lip
    for sy in (-1, 1):
        for j in range(nr):
            lp = NL(sy) if j else V(0, 0, 0)
            for i in range(n):
                q = [P(xr[i], sy, j / nr) + lp, P(xr[i + 1], sy, j / nr) + lp, P(xr[i + 1], sy, (j + 1) / nr), P(xr[i], sy, (j + 1) / nr)]
                y.yuz_yon(q, kk(j), Z + V(0, sy * 0.5))
                if j and kat_lip:
                    y.yuz_yon([P(xr[i], sy, j / nr), P(xr[i + 1], sy, j / nr), P(xr[i + 1], sy, j / nr) + lp, P(xr[i], sy, j / nr) + lp], kk(j), V(0, sy, -0.6))
            if j and kat_lip:
                for sx, xx in ((-1, xr[0]), (1, xr[-1])):
                    y.yuz_yon([P(xx, sy, j / nr), P(xx, sy, j / nr) + lp, P(xx, sy, (j + 1) / nr)], kk(j), V(sx, 0))
        # the eave: thick edge and the soffit back to the wall top
        kenar = cati if cati in ('saz', 'saz_koyu', 'cimen') else 'ahsap_koyu'
        for i in range(n):
            p0, p1 = P(xr[i], sy, 0), P(xr[i + 1], sy, 0)
            y.yuz_yon([p0, p1, p1 - Z * kalin, p0 - Z * kalin], kenar, V(0, sy))
            w0, w1 = V(xr[i], sy * hw(xr[i]), zw), V(xr[i + 1], sy * hw(xr[i + 1]), zw)
            y.yuz_yon([p0 - Z * kalin, p1 - Z * kalin, w1, w0], 'ahsap_koyu', -Z)
        if cati == 'saz':   # a darker trimmed band along the thatch eave
            for i in range(n):
                p0, p1 = P(xr[i], sy, 0), P(xr[i + 1], sy, 0)
                q0, q1 = P(xr[i], sy, 0.08), P(xr[i + 1], sy, 0.08)
                y.yuz_yon([p0 + Z * 0.0, p1, q1 + Z * 0.002, q0 + Z * 0.002], 'saz_koyu', Z + V(0, sy * 0.5))
    # verges, their undersides and the gables
    ts = [k / nr for k in range(nr + 1)]
    for sx in (-1, 1):
        xe, xg = sx * (L / 2 + ext), sx * L / 2
        for sy in (-1, 1):
            pts = [P(xe, sy, t) for t in ts]
            for k in range(nr):
                y.yuz_yon([pts[k], pts[k + 1], pts[k + 1] - Z * kalin, pts[k] - Z * kalin], 'ahsap_koyu' if cati != 'saz' else 'saz', V(sx, 0))
                ga, gb = P(xg, sy, ts[k]) - Z * 0.004, P(xg, sy, ts[k + 1]) - Z * 0.004
                y.yuz_yon([pts[k] - Z * kalin, pts[k + 1] - Z * kalin, gb, ga], 'ahsap_koyu', -Z + V(sx * 0.2, 0))
        tw = sacak / (hw(xg) + sacak)
        tg = [tw + (1 - tw) * k / nr for k in range(nr + 1)]
        gable = [V(xg, -hw(xg), zw)] + [P(xg, -1, t) - Z * 0.004 for t in tg[1:]] + [P(xg, 1, t) - Z * 0.004 for t in reversed(tg[1:-1])] + [V(xg, hw(xg), zw)]
        y.yuz_yon(gable, ucluk, V(sx, 0))
        # a smoke hole near the apex and a carved board across the gable foot
        ap = P(xg, 1, 1).z
        hz = ap - 0.06
        y.yuz_yon([V(xg + sx * 0.002, -0.025, hz - 0.03), V(xg + sx * 0.002, 0.025, hz - 0.03), V(xg + sx * 0.002, 0, hz + 0.012)], 'koyu', V(sx, 0))
        cubuk(y, V(xg + sx * 0.006, -hw(xg) - 0.01, zw + 0.004), V(xg + sx * 0.006, hw(xg) + 0.01, zw + 0.004), 0.014, sus, 0.01)
        # crossed barge boards running past the apex into dragon heads
        top = P(xe, 1, 1)
        for sy in (-1, 1):
            p0 = P(xe, sy, 0.3) + V(sx * 0.008, 0, 0.012)
            p1 = top + V(sx * 0.008, 0, 0.012)
            d = (p1 - p0).normalized()
            p2 = p1 + d * 0.05
            cubuk(y, p0, p2, 0.022, ejder_key, 0.011)
            if ejder_s:
                ejder(y, p2 - d * 0.004, V(0, -sy), ejder_s, ejder_key)
    # ridge cap
    pts = [P(x, 1, 1) + Z * 0.008 for x in xr]
    for i in range(n):
        cubuk(y, pts[i], pts[i + 1], 0.034 if mahya in ('cimen', 'saz', 'saz_koyu') else 0.016, mahya, 0.014)
    # doors in the gable ends (uc_kapi: sides -1 / 1), framed in carved red posts under a little pent roof
    for sx in uc_kapi:
        xg = sx * (L / 2 + 0.003)
        dw, dh = 0.045, h * 0.78
        y.yuz_yon([V(xg, -dw, z0 + 0.02), V(xg, dw, z0 + 0.02), V(xg, dw, z0 + dh), V(xg, -dw, z0 + dh)], 'ahsap_koyu', V(sx, 0))
        for s2 in (-1, 1):
            cubuk(y, V(xg + sx * 0.004, s2 * (dw + 0.006), z0), V(xg + sx * 0.004, s2 * (dw + 0.006), z0 + dh + 0.012), 0.011, sus, 0.008)
            cubuk(y, V(xg + sx * 0.007, s2 * dw * 0.45, z0 + 0.03), V(xg + sx * 0.007, s2 * dw * 0.45, z0 + dh - 0.01), 0.004, 'demir', 0.003)
        cubuk(y, V(xg + sx * 0.004, -dw - 0.02, z0 + dh + 0.012), V(xg + sx * 0.004, dw + 0.02, z0 + dh + 0.012), 0.014, sus, 0.01)
        q = [V(xg, -dw - 0.03, z0 + dh + 0.045), V(xg, dw + 0.03, z0 + dh + 0.045), V(xg + sx * 0.05, dw + 0.03, z0 + dh + 0.02), V(xg + sx * 0.05, -dw - 0.03, z0 + dh + 0.02)]
        y.yuz_yon(q, cati if cati != 'saz' else 'ahsap_koyu', Z + V(sx, 0))
        y.yuz_yon([p - Z * 0.008 for p in q], 'ahsap_koyu', -Z)
        y.yuz_yon([q[2], q[3], q[3] - Z * 0.008, q[2] - Z * 0.008], 'ahsap_koyu', V(sx, 0))
        for s2 in (-1, 1):
            i0, i1 = (1, 2) if s2 > 0 else (0, 3)
            y.yuz_yon([q[i0], q[i1], q[i1] - Z * 0.008, q[i0] - Z * 0.008], 'ahsap_koyu', V(0, s2))
        merdiven(y, (xg + sx * 0.06, 0), math.pi if sx > 0 else 0.0, dw * 2.2, z0, z0 + 0.02, n=2, key=ayak)
    # crossed rider sticks pinning the ridge (thatch "kroker")
    if kroker:
        m = int((L + 2 * ext) / kroker)
        for k in range(m + 1):
            x = -L / 2 - ext * 0.6 + (L + ext * 1.2) * k / m
            if any(abs(x - dx) < 0.06 for dx in dumanlik): continue
            for sy in (-1, 1):
                a = P(x, sy, 0.8) + Z * 0.004
                b = P(x, -sy, 1) + Z * 0.012 + V(0, -sy * 0.03, 0.02)
                cubuk(y, a, b, 0.01, "ahsap_koyu", 0.009)
    # smoke louvres on the ridge
    for x in dumanlik:
        zt = zr(x)
        kutu_merkez(y, (x, 0), 0.075, 0.05, 0.05, 'ahsap_dikey', z0=zt - 0.025)
        for sy in (-1, 1):
            y.yuz_yon([V(x - 0.025, sy * 0.0255, zt + 0.0), V(x + 0.025, sy * 0.0255, zt + 0.0), V(x + 0.025, sy * 0.0255, zt + 0.018), V(x - 0.025, sy * 0.0255, zt + 0.018)], 'koyu', V(0, sy))
        cati_besik(y, x - 0.042, x + 0.042, -0.033, 0.033, zt + 0.025, 0.035, 0.01, 'ahsap_koyu', 'ahsap', kalinlik=0.006, ucluk_key='ahsap_dikey')
    # leaning outer posts carrying the eave (each on a stone)
    if dikme:
        m = int(L * 0.9 / dikme)
        for sy in (-1, 1):
            for k in range(m + 1):
                x = -L * 0.45 + L * 0.9 * k / m
                if any(abs(x - kx) < 0.07 and ks == sy for kx, ks in kapilar): continue
                foot = V(x, sy * (hw(x) + sacak * 0.85), z0)
                tp = V(x, sy * (hw(x) + 0.006), zw - 0.02)
                cubuk(y, foot + Z * 0.012, tp, 0.014, 'ahsap_koyu', 0.012)
                kutu_merkez(y, (foot.x, foot.y), 0.026, 0.026, 0.014, ayak, z0=z0)
    # shields hung along the long walls under the eaves
    if kalkanlar:
        renkler = (('boya_kirmizi', 'boya_sari'), ('beyaz', 'boya_kirmizi'), ('boya_sari', 'koyu'), ('boya_yesil', 'beyaz'))
        for sy in kalkanlar:
            m = int(L * 0.9 / dikme)
            for k in range(m):
                x = -L * 0.45 + L * 0.9 * (k + 0.5) / m
                if any(abs(x - kx) < 0.09 and ks == sy for kx, ks in kapilar): continue
                kalkan(y, V(x, sy * (hw(x) + 0.006), z0 + h * 0.4), V(0, sy, 0.15), 0.026, renkler[k % 4])
    # porched doors
    for x, sy in kapilar:
        wy = sy * hw(x)
        dp = 0.1                                  # porch depth beyond the wall
        pw = 0.055                                # porch half width
        ph = h * sundurma_h
        ya, yb = wy - sy * 0.02, wy + sy * dp
        # side walls and the front with the door
        ylo, yhi = min(ya, yb), max(ya, yb)
        duz_duvar(y, V(x + pw, ylo), V(x + pw, yhi), z0, z0 + ph, duvar)
        duz_duvar(y, V(x - pw, yhi), V(x - pw, ylo), z0, z0 + ph, duvar)
        a_, b_ = (V(x - pw, yb), V(x + pw, yb)) if sy < 0 else (V(x + pw, yb), V(x - pw, yb))
        dikdortgen_acik(y, a_, b_, z0, ph, 0.25, 0.75, 0.02, ph * 0.9, (duvar, 'ahsap_koyu', 'ahsap', 'ahsap_koyu'), derin=0.012)
        e = (b_ - a_).normalized(); nn = V(e.y, -e.x)
        # the carved, painted door frame
        for u in (0.23, 0.77):
            p = a_.lerp(b_, u) + nn * 0.004
            cubuk(y, p + Z * z0, p + Z * (z0 + ph * 0.93), 0.01, sus, 0.006)
        cubuk(y, a_.lerp(b_, 0.18) + nn * 0.004 + Z * (z0 + ph * 0.93), a_.lerp(b_, 0.82) + nn * 0.004 + Z * (z0 + ph * 0.93), 0.012, sus, 0.007)
        kutu_merkez(y, (a_.lerp(b_, 0.5).x + nn.x * 0.004, a_.lerp(b_, 0.5).y + nn.y * 0.004), 0.03, 0.004, 0.02, 'altin', z0=z0 + ph * 0.95)
        silme(y, [V(x - pw, ya), V(x + pw, ya), V(x + pw, yb), V(x - pw, yb)] if sy > 0 else [V(x - pw, yb), V(x + pw, yb), V(x + pw, ya), V(x - pw, ya)],
              z0, 0.025, 0.008, ayak, 'kaide')
        y0_, y1_ = min(ya, yb), max(ya, yb)
        cati_besik(y, x - pw, x + pw, y0_ - (0.03 if sy < 0 else 0), y1_ + (0.03 if sy > 0 else 0), z0 + ph, sundurma_c, 0.02,
                   cati, mahya if mahya != 'cimen' or cati == 'cimen' else cati, kalinlik=0.016, ucluk_key=ucluk, uc_sacak=0.0)
        # a little dragon / crossed board on the porch gable
        ge = V(x, yb + sy * 0.03, z0 + ph + sundurma_c)
        for s2 in (-1, 1):
            cubuk(y, ge + V(s2 * 0.05, sy * 0.004, -0.06), ge + V(-s2 * 0.012, sy * 0.004, 0.018), 0.008, ejder_key, 0.006)
    # yama: that many weathered / mossy patches on each slope (ragged strips lying on one course, yama_key keys,
    # seeded by tohum); cati_merdiven = ((x, side), ...): a ladder up the roof
    import random
    dolu = set()
    if yama:
        rg = random.Random(tohum)
        keys = yama_key or (('saz_koyu', 'cimen_kuru', 'saz_koyu') if cati in ('saz', 'saz_koyu') else ('cimen_kuru', 'toprak_ot', 'cimen_kuru'))
        for sy in (-1, 1):
            nrm = V(0, sy * 0.55, 0.83).normalized() * 0.003
            for _ in range(yama):
                j = rg.randrange(1, max(2, nr - 1))
                i0 = rg.randrange(0, n - 1)
                i1 = min(n, i0 + rg.choice((2, 3, 3, 4)))
                if any((sy, j, i) in dolu for i in range(i0, i1)): continue
                if any(abs(xr[i0] - dx) < 0.07 or abs(xr[i1] - dx) < 0.07 for dx in dumanlik): continue
                for i in range(i0, i1): dolu.add((sy, j, i))
                t0, t1 = j / nr, (j + 1) / nr
                lp = NL(sy)
                Q = lambda x, s: (P(x, sy, t0) + lp).lerp(P(x, sy, t1), s) + nrm
                sa = [rg.uniform(0.02, 0.22) for _ in range(i0, i1 + 1)]
                sb = [rg.uniform(0.78, 0.97) for _ in range(i0, i1 + 1)]
                key = rg.choice(keys)
                for k, i in enumerate(range(i0, i1)):
                    q = [Q(xr[i], sa[k]), Q(xr[i + 1], sa[k + 1]), Q(xr[i + 1], sb[k + 1]), Q(xr[i], sb[k])]
                    y.yuz_yon(q, key, Z + V(0, sy * 0.5))
    # saz_cizgi: that many straw strokes (thin strips down the slope, the other thatch tone) per course and roof bay
    if saz_cizgi:
        rg2 = random.Random(tohum + 101)
        for sy in (-1, 1):
            nrm = V(0, sy * 0.55, 0.83).normalized() * 0.0025
            lp0 = NL(sy)
            for j in range(nr):
                if kk(j) not in ('saz', 'saz_koyu', 'cimen'): continue
                t0, t1 = j / nr, (j + 1) / nr
                lp = lp0 if j else V(0, 0, 0)
                for i in range(n):
                    if (sy, j, i) in dolu: continue
                    A0, A1 = P(xr[i], sy, t0) + lp, P(xr[i], sy, t1)
                    B0, B1 = P(xr[i + 1], sy, t0) + lp, P(xr[i + 1], sy, t1)
                    Qu = lambda uu, s: A0.lerp(A1, s).lerp(B0.lerp(B1, s), uu) + nrm
                    du = 0.0035 / (xr[i + 1] - xr[i])
                    for _ in range(saz_cizgi):
                        u = rg2.uniform(0.06, 0.94)
                        sa_, sb_ = rg2.uniform(0.08, 0.35), rg2.uniform(0.68, 0.94)
                        q = [Qu(u - du, sa_), Qu(u + du, sa_), Qu(u + du, sb_), Qu(u - du, sb_)]
                        y.yuz_yon(q, {'saz': 'saz_koyu', 'saz_koyu': 'saz', 'cimen': 'cimen_kuru'}[kk(j)], Z + V(0, sy * 0.5))
    for mx, msy in cati_merdiven:
        nrm = V(0, msy * 0.55, 0.83).normalized()
        tt = 0.78
        for dx in (-0.019, 0.019):
            pts = [P(mx + dx, msy, t) + nrm * 0.016 for t in (0.0, tt * 0.33, tt * 0.66, tt)]
            for k in range(3):
                cubuk(y, pts[k], pts[k + 1], 0.007, 'ahsap', 0.006)
        m_ = 11
        for k in range(1, m_ + 1):
            t = tt * k / (m_ + 0.5)
            cubuk(y, P(mx - 0.024, msy, t) + nrm * 0.02, P(mx + 0.024, msy, t) + nrm * 0.02, 0.005, 'ahsap_acik', 0.005)
    return zr(0)
