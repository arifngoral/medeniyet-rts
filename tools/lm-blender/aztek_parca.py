# Aztec / Mesoamerican parts shared by the Aztec landmark scripts (bina/lm_cinampa.py, lm_kartalevi.py,
# lm_tlatelolco.py, lm_jaguartapinagi.py): an ellipsoid, an extruded outline (slab), a stair with balustrades
# (alfardas) steepening into a dado at the top, stepped roof merlons (almenas), tiered conical and hipped thatch,
# a crouching jaguar and a perched eagle statue, an eagle head, a dugout canoe, an incense brazier, a willow
# (ahuejote), maize / bean / squash / flower plants, a market stall. Built like parcalar.py: faces wound outward,
# local origin, place with parca().
import math
from mathutils import Vector
from parcalar import *


# ---------------------------------------------------------------- primitives
def elipsoid(y, c, r, key, n=10, kat=6, aci=0.0, ust_yarim=False):
    """an ellipsoid centred at c (x, y, z), radii r = (rx, ry, rz), turned by aci about z; ust_yarim: only the top half
    (a mound sitting on the ground: its flat bottom is left open, it stands on something)"""
    c = Vector(c); rx, ry, rz = r
    ca, sa = math.cos(aci), math.sin(aci)
    k0 = kat // 2 if ust_yarim else 0
    def P(k, i):
        ph = -math.pi / 2 + math.pi * k / kat
        t = TAU * i / n
        lx, ly = rx * math.cos(ph) * math.cos(t), ry * math.cos(ph) * math.sin(t)
        return c + Vector((ca * lx - sa * ly, sa * lx + ca * ly, rz * math.sin(ph)))
    for k in range(k0, kat):
        for i in range(n):
            j = (i + 1) % n
            if k == 0:
                q = [P(0, 0), P(1, j), P(1, i)]
            elif k == kat - 1:
                q = [P(k, i), P(k, j), P(kat, 0)]
            else:
                q = [P(k, i), P(k, j), P(k + 1, j), P(k + 1, i)]
            yuz_dis(y, q, key, c)


def levha(y, o, e, uv, kalin, key, yan_key=None):
    """a slab: the outline uv = [(u along e, v up), ...] (any winding, may be concave) on the plane through o, its
    front facing the right of e, extruded kalin backwards (to the left of e); the rim faces yan_key"""
    o = Vector(o); e = Vector((e[0], e[1], 0)).normalized(); nc = V(e.y, -e.x)
    s = sum(uv[i][0] * uv[(i + 1) % len(uv)][1] - uv[(i + 1) % len(uv)][0] * uv[i][1] for i in range(len(uv)))
    if s < 0: uv = uv[::-1]              # CCW in (u, v)
    P = lambda u, v, d: o + e * u + Z * v - nc * d
    y.yuz_yon([P(u, v, 0) for u, v in uv], key, nc)
    y.yuz_yon([P(u, v, kalin) for u, v in uv], key, -nc)
    m = len(uv)
    for i in range(m):
        (ua, va), (ub, vb) = uv[i], uv[(i + 1) % m]
        out = e * (vb - va) - Z * (ub - ua)      # (the outward normal of a CCW edge in (u, v): (dv, -du))
        y.yuz_yon([P(ua, va, 0), P(ub, vb, 0), P(ub, vb, kalin), P(ua, va, kalin)], yan_key or key, out)


def kesik_piramit(y, c, w0, d0, w1, d1, z0, z1, keys, alt=False, ust=True, n_dilim=1):
    """a truncated pyramid (a battered base, a tall shrine roof): w0 x d0 at z0 to w1 x d1 at z1; keys: one key or a
    list alternating in n_dilim vertical strips per side (the striped roofs of the Tlaloc shrine)"""
    keys = keys if isinstance(keys, (list, tuple)) else [keys]
    a = dikdortgen(c[0] - w0 / 2, c[0] + w0 / 2, c[1] - d0 / 2, c[1] + d0 / 2, z0)
    b = dikdortgen(c[0] - w1 / 2, c[0] + w1 / 2, c[1] - d1 / 2, c[1] + d1 / 2, z1)
    for i in range(4):
        j = (i + 1) % 4
        out = V(a[i].x + a[j].x - 2 * c[0], a[i].y + a[j].y - 2 * c[1])
        for k in range(n_dilim):
            t0, t1 = k / n_dilim, (k + 1) / n_dilim
            y.yuz_yon([a[i].lerp(a[j], t0), a[i].lerp(a[j], t1), b[i].lerp(b[j], t1), b[i].lerp(b[j], t0)], keys[k % len(keys)], out)
    if ust: y.yuz_yon(b, keys[0], Z)
    if alt: y.yuz_yon(a, keys[0], -Z)


def talud_tablero(y, kose, z0, h, talud=0.55, ins=0.05, key='kirec', tablero_key=None, ust_key='zemin', cerceve_key=None, disk=None):
    """a platform on any CCW outline (an L too): a sloping talud from the outline at z0 inward by ins up to talud x h,
    then an upright tablero panel (tablero_key) up to z0 + h, set out a little over the talud's top; framed by bands
    (cerceve_key) at its top and foot; disk = (key, frame key, spacing): painted discs along the panels. The top
    faces ust_key. Returns the top outline (the tablero's) and the top z"""
    kose = [V(p.x, p.y) for p in kose]
    zm, z1 = z0 + h * talud, z0 + h
    alt = [p + Z * z0 for p in kose]
    ort = [p + Z * zm for p in disa(kose, -ins)]
    tb = disa(kose, -ins * 0.8)
    y.serit(alt, ort, key)
    duvarlar(y, tb, zm, z1, tablero_key or key)
    n = len(kose)
    for i in range(n):
        j = (i + 1) % n
        y.yuz_yon([ort[i], ort[j], tb[j] + Z * zm, tb[i] + Z * zm], key, -Z)
    y.yuz_yon([p + Z * z1 for p in tb], ust_key, Z)
    th = z1 - zm
    if cerceve_key:
        silme(y, tb, z1 - th * 0.22, th * 0.22, 0.006, cerceve_key)
        silme(y, tb, zm, th * 0.16, 0.006, cerceve_key)
    if disk:
        dk, fk, ara = disk
        zc = zm + th * (0.16 + (1 - 0.38) / 2) if cerceve_key else (zm + z1) / 2
        for i in range(n):
            a, b = tb[i], tb[(i + 1) % n]
            e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
            m = int(L / ara)
            for k in range(m):
                p = a.lerp(b, (k + 0.5) / m)
                y.oculus(p + nn * 0.0005 + Z * zc, e, nn, th * 0.2, dk, fk, f=0.004, k=10)
    return tb, z1


# ---------------------------------------------------------------- stairs, merlons
def alfarda_merdiven(y, cx, y_bas, y_son, z0, z1, en, n=None, key='siva', alfarda_key='siva', alfarda_en=0.035,
                     dado=0.16, dado_h=0.05, bas_key=None, yon=0.0, ox=0.0, oy=0.0):
    """an Aztec stair climbing towards +y (then turned by yon about (ox, oy)): steps from y_bas (on the ground at z0)
    to y_son (at z1), en wide, every step a block from the ground; on either side a balustrade (alfarda) whose top
    follows the slope and in the last dado share of the run turns steeper into an upright block (the dado) that
    stands dado_h above the top; bas_key: a key for a carved head at the foot of each balustrade (None: none).
    Returns the foot points of the balustrades [(x, y), (x, y)]"""
    n = n or max(6, int((z1 - z0) / 0.022))
    run = y_son - y_bas
    with parca(y, (ox, oy, 0), yon):
        for k in range(n):
            ya = y_bas + run * k / n
            # (no side faces: the balustrades cover them, back to back on one plane they flickered)
            kutu(y, V(cx - en / 2, ya, z0), X, en, run / n, (z1 - z0) * (k + 1) / n, key, 'onust')
        zs = lambda yy: z0 + (z1 - z0) * (yy - y_bas) / run
        yd = y_son - run * dado
        hh = 0.028
        for sx in (-1, 1):
            xa = cx + sx * en / 2 if sx > 0 else cx - en / 2 - alfarda_en
            prof = [(y_bas - 0.012, z0), (y_son, z0), (y_son, z1 + dado_h), (yd + run * dado * 0.35, z1 + dado_h),
                    (yd, zs(yd) + hh), (y_bas - 0.012, z0 + hh)]
            # (extruded along x from xa + alfarda_en back to xa: levha's back side is to the left of e)
            levha(y, V(xa + alfarda_en, 0, 0), Y, prof, alfarda_en, alfarda_key)
        return [V(cx - en / 2 - alfarda_en / 2, y_bas), V(cx + en / 2 + alfarda_en / 2, y_bas)]


ALMENA = [(0, 0), (1, 0), (1, 0.42), (0.78, 0.42), (0.78, 0.7), (0.62, 0.7), (0.62, 1.0), (0.38, 1.0), (0.38, 0.7),
          (0.22, 0.7), (0.22, 0.42), (0, 0.42)]      # a stepped merlon (the cut shell / fret almenas on Aztec roofs)


def almenalar(y, a, b, z, h, kalin=0.008, key='siva', en=None, bosluk=None, uclar=True, bicim=ALMENA):
    """a row of stepped merlons along a->b (their face on the line, facing the right), h high"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-6: return
    e = (b - a) / L
    w = en or h * 0.75; g = bosluk or h * 0.3
    k = max(1, int(round((L + g) / (w + g))))
    w = (L + g) / k - g if uclar else w
    for i in range(k):
        u = i * (w + g)
        levha(y, a + e * u + Z * z, e, [(p[0] * w, p[1] * h) for p in bicim], kalin, key)


def almena_halka(y, kose, z, h, kalin=0.008, key='siva', en=None, bosluk=None):
    """merlons round a CCW polygon (on its outline, facing out)"""
    for i in range(len(kose)):
        almenalar(y, kose[i], kose[(i + 1) % len(kose)], z, h, kalin, key, en, bosluk)


# ---------------------------------------------------------------- thatch
def donel_yivli(y, c, profil, key, n=24, kat=0.0):
    """a surface of revolution like donel, every ring (r, z, oran, dz) with its odd meridians at r x oran and dz
    lower: ridged straw bundles, a ragged lip. A last radius 0 closes the top in a point"""
    def P(k, i):
        r, zz, o, dz = profil[k]
        if i % 2: r, zz = r * o, zz - dz
        t = kat + TAU * i / n
        return V(c[0] + r * math.cos(t), c[1] + r * math.sin(t), zz)
    for k in range(len(profil) - 1):
        for i in range(n):
            j = (i + 1) % n
            if profil[k + 1][0] < 1e-9:
                y.yuz([P(k, i), P(k, j), V(c[0], c[1], profil[k + 1][1])], key)
            else:
                y.yuz([P(k, i), P(k, j), P(k + 1, j), P(k + 1, i)], key)


def saz_konik(y, c, r, z, h, kat=4, keys=('saz', 'saz_koyu'), n=28, sacak=0.04, kalin=0.016, alt_key='ahsap_koyu', tepe=True, puskul=0.0,
              yiv=0.0):
    """a tiered conical thatch roof: kat overlapping cones (each tier's eave a lip of kalin, its underside) from the eave
    radius r + sacak at z up to the apex at z + h; tepe: a binding knot at the top; puskul: the length of the ragged
    straw ends hanging under every tier's lip (0: none); yiv (0..0.1): ridged straw bundles and a ragged lip.
    Returns the apex z"""
    R = r + sacak
    for k in range(kat):
        t0, t1 = k / kat, (k + 1) / kat
        ra, rb = R * (1 - t0), R * (1 - t1)
        za, zb = z + h * t0, z + h * t1
        # each tier starts a little out and below the previous one's top (overlap)
        lip = kalin * (1 - 0.3 * t0)
        pr = [(ra * 0.94 if k else r * 0.98, za + (lip if k else 0)), (ra + lip * 0.6, za - lip * 0.6 + (lip if k else 0)), (rb, zb + lip)]
        if k == kat - 1: pr[-1] = (0.0, z + h)
        if yiv:
            # straw bundles: every other meridian a little in (ridges), the lip ragged (every other point hangs lower)
            pr2 = [(pr[0][0], pr[0][1], 1.0, 0.0), (pr[1][0], pr[1][1], 1 - yiv * 0.6, yiv * 0.35 * R),
                   ((pr[1][0] * 0.55 + pr[2][0] * 0.45), (pr[1][1] * 0.55 + pr[2][1] * 0.45), 1 - yiv, 0.0), (pr[2][0], pr[2][1], 1 - yiv * 0.5, 0.0)]
            donel_yivli(y, c, pr2, keys[k % len(keys)], n=n, kat=TAU / n * 0.5 * (k % 2))
        else:
            donel(y, c, pr, keys[k % len(keys)], n=n)
        if puskul:
            m = int(TAU * ra / 0.022)
            ze = za - lip * 0.6 + (lip if k else 0)
            for i in range(m):
                t = TAU * (i + 0.5 * (k % 2)) / m
                rr = ra + lip * 0.25
                L = puskul * (0.7 + 0.3 * ((i * 7) % 5) / 4) * (1 - 0.4 * t0)
                donel(y, (c[0] + rr * math.cos(t), c[1] + rr * math.sin(t)), [(0.0, ze - L), (0.007, ze + 0.004)], keys[(k + 1) % len(keys)], n=4,
                      kat=t)
        if k == 0:
            y.yuz_yon([V(p.x, p.y, z) for p in cokgen(c, r * 0.98, n)], alt_key, -Z)
    if tepe:
        donel(y, c, [(0.0, z + h - 0.02), (0.012, z + h - 0.012), (0.014, z + h + 0.006), (0.006, z + h + 0.02), (0.0, z + h + 0.024)], keys[-1], n=10)
    return z + h


def saz_cati(y, x0, x1, y0, y1, z, h, sacak=0.03, keys=('saz', 'saz_koyu'), nr=6, kalin=0.016, besik=False):
    """a steep thatched roof (hipped, or a gable roof if besik) with thick eaves and alternating thatch courses"""
    if besik:
        return cati_besik(y, x0, x1, y0, y1, z, h, sacak, keys[0], keys[1], kalinlik=kalin, ucluk_key='saz_koyu',
                          uc_sacak=sacak, nr=nr, ns=6, dilim=list(keys), mahya_en=0.016)
    return cati_kirma(y, x0, x1, y0, y1, z, h, sacak, keys[0], keys[1], kalinlik=kalin, nr=nr, ns=8, dilim=list(keys), mahya_en=0.016)


# ---------------------------------------------------------------- sculpture
def jaguar(y, x, yy, z, olcek=0.14, aci=0.0, key='boya_sari', benek='koyu', taban='bazalt', taban_h=0.12, tohum=1):
    """a recumbent jaguar on a block (the Malinalco floor jaguars, the cuauhxicalli jaguar): a long low body, the
    forepaws stretched forward, the head raised and turned a little, the tail curled along the block; facing angle aci;
    olcek its length. Returns the top z"""
    import random
    rn = random.Random(tohum)
    with parca(y, (x, yy, z), aci, olcek):
        if taban:
            kutu_merkez(y, (0.02, 0), 1.24, 0.52, taban_h, taban, z0=0)
            kornis(y, -0.6, 0.64, -0.26, 0.26, taban_h - 0.03, 0.03, 0.025, taban)
        b = taban_h
        G = [((-0.08, 0, b + 0.15), (0.36, 0.15, 0.13)),      # body
             ((-0.33, 0, b + 0.15), (0.17, 0.17, 0.15)),      # haunch
             ((0.17, 0, b + 0.17), (0.15, 0.15, 0.15))]       # shoulders
        for c_, r_ in G:
            elipsoid(y, c_, r_, key, n=12, kat=6)
        for s in (-1, 1):
            elipsoid(y, (-0.26, s * 0.15, b + 0.06), (0.17, 0.05, 0.06), key, n=8, kat=4)          # folded hind legs
            elipsoid(y, (0.36, s * 0.08, b + 0.045), (0.2, 0.045, 0.045), key, n=8, kat=4)         # forelegs stretched out
            elipsoid(y, (0.56, s * 0.08, b + 0.03), (0.055, 0.048, 0.03), key, n=8, kat=4)         # paws
            for k in (-1, 0, 1):
                kure(y, (0.605, s * 0.08 + k * 0.017, b + 0.02), 0.007, 'beyaz', n=4, kat=2)        # claws
        elipsoid(y, (0.29, 0, b + 0.26), (0.1, 0.1, 0.12), key, n=10, kat=5)                        # neck
        HC = (0.37, 0.0, b + 0.35)
        elipsoid(y, HC, (0.1, 0.118, 0.08), key, n=12, kat=6)                                        # head (broad, flat)
        elipsoid(y, (0.465, 0, b + 0.322), (0.075, 0.07, 0.045), key, n=10, kat=4)                   # muzzle
        elipsoid(y, (0.475, 0, b + 0.3), (0.045, 0.052, 0.022), 'beyaz', n=8, kat=4)                 # pale chin
        kure(y, (0.528, 0, b + 0.333), 0.015, benek, n=6, kat=3)                                     # nose
        for s in (-1, 1):
            elipsoid(y, (0.335, s * 0.09, b + 0.415), (0.02, 0.026, 0.028), key, n=6, kat=4)          # ears
            elipsoid(y, (0.338, s * 0.09, b + 0.415), (0.012, 0.017, 0.019), benek, n=6, kat=3)      # (their dark backs)
            kure(y, (0.455, s * 0.045, b + 0.37), 0.014, 'altin', n=6, kat=3)                        # eyes
            kure(y, (0.462, s * 0.045, b + 0.37), 0.007, benek, n=5, kat=3)
        boru(y, [V(-0.48, 0, b + 0.16), V(-0.58, 0.07, b + 0.04), V(-0.45, 0.2, b + 0.022), V(-0.15, 0.22, b + 0.02), V(0.0, 0.2, b + 0.03)],
             0.028, key, n=6, r_son=0.018)
        for k in range(4):   # tail rings
            p = [V(-0.45, 0.2, b + 0.022), V(-0.15, 0.22, b + 0.02)][0].lerp(V(0.0, 0.2, b + 0.03), (k + 0.5) / 4)
            kure(y, (p.x, p.y, p.z + 0.006), 0.017, benek, n=5, kat=3)
        # rosettes: dark spots on the back, flanks and head
        for i in range(34):
            c_, r_ = G[0] if i < 20 else G[1] if i < 27 else G[2] if i < 31 else (HC, (0.1, 0.118, 0.08))
            t = rn.uniform(0, TAU); ph = rn.uniform(0.0, 1.15)
            p = V(c_[0] + r_[0] * math.cos(ph) * math.cos(t), c_[1] + r_[1] * math.cos(ph) * math.sin(t), c_[2] + r_[2] * math.sin(ph))
            if i >= 31 and p.x > 0.4: continue
            kure(y, (p.x, p.y, p.z), 0.022, benek, n=6, kat=3)
    return z + olcek * (taban_h + 0.45)


def kartal_bas(y, p, yon, s=0.08, key='siva', gaga='boya_sari', goz='koyu', tuy='boya_kirmizi'):
    """a carved eagle head (on the foot of a balustrade, a lintel) looking towards yon: a round head, a hooked beak,
    a feather crest; s its size"""
    p = Vector(p); d = V(yon[0], yon[1]).normalized(); sd = Z.cross(d)
    kure(y, p, 0.45 * s, key, n=10, kat=5)
    elipsoid(y, p - d * (0.3 * s) - Z * (0.1 * s), (0.42 * s, 0.4 * s, 0.38 * s), key, n=8, kat=4, aci=math.atan2(d.y, d.x))   # neck / ruff
    a = p + d * (0.35 * s) + Z * (0.06 * s)
    boru(y, [a, a + d * (0.38 * s) + Z * (0.03 * s), a + d * (0.6 * s) - Z * (0.12 * s), a + d * (0.52 * s) - Z * (0.3 * s)], 0.2 * s, gaga, n=6, r_son=0.035 * s)
    for sg in (-1, 1):
        kure(y, p + d * (0.3 * s) + sd * (sg * 0.26 * s) + Z * (0.12 * s), 0.085 * s, goz, n=6, kat=3)
        # a heavy brow over the eye: the frown that makes it an eagle and not a bird
        q = p + sd * (sg * 0.3 * s) + Z * (0.2 * s)
        boru(y, [q - d * (0.05 * s), q + d * (0.3 * s) - sd * (sg * 0.06 * s) + Z * (0.02 * s), q + d * (0.42 * s) - sd * (sg * 0.14 * s) - Z * (0.04 * s)],
             0.07 * s, tuy, n=5, r_son=0.04 * s)
    for k in range(5):   # crest feathers swept back
        q = p + sd * ((k - 2) * 0.12 * s) + Z * (0.3 * s) - d * (0.1 * s)
        boru(y, [q, q - d * (0.4 * s) + Z * (0.1 * s), q - d * (0.78 * s) + Z * (0.04 * s)], 0.07 * s, tuy if k % 2 else key, n=4, r_son=0.02 * s)


def yilan_bas(y, p, yon, s=0.1, key='turkuaz', agiz='boya_kirmizi', dis='beyaz', kas='boya_sari', goz='koyu'):
    """a feathered serpent's head (the stair heads of the Templo Mayor) on the ground looking towards yon: a broad
    head, a blunt snout with a curled nose plate, the open red mouth with a forked tongue, two fangs, brows; s its size"""
    p = Vector(p); d = V(yon[0], yon[1]).normalized(); sd = Z.cross(d); a = math.atan2(d.y, d.x)
    elipsoid(y, p, (0.55 * s, 0.42 * s, 0.34 * s), key, n=12, kat=6, aci=a)                                        # head
    elipsoid(y, p + d * (0.42 * s) + Z * (0.06 * s), (0.3 * s, 0.33 * s, 0.2 * s), key, n=10, kat=5, aci=a)         # upper snout
    elipsoid(y, p + d * (0.32 * s) - Z * (0.22 * s), (0.36 * s, 0.3 * s, 0.1 * s), agiz, n=10, kat=4, aci=a)        # the open mouth
    elipsoid(y, p + d * (0.3 * s) - Z * (0.32 * s), (0.4 * s, 0.33 * s, 0.08 * s), key, n=10, kat=4, aci=a)         # lower jaw
    t = p + d * (0.6 * s) - Z * (0.3 * s)
    for sg in (-1, 1):
        boru(y, [t - d * (0.2 * s), t + d * (0.1 * s), t + d * (0.25 * s) + sd * (sg * 0.08 * s)], 0.035 * s, agiz, n=4, r_son=0.012 * s)   # forked tongue
        f = p + d * (0.55 * s) + sd * (sg * 0.17 * s) - Z * (0.06 * s)
        donel(y, (f.x, f.y), [(0.0, f.z - 0.2 * s), (0.05 * s, f.z)], dis, n=5)                                       # fangs
        kure(y, p + d * (0.18 * s) + sd * (sg * 0.3 * s) + Z * (0.2 * s), 0.09 * s, 'beyaz', n=8, kat=4)
        kure(y, p + d * (0.24 * s) + sd * (sg * 0.32 * s) + Z * (0.22 * s), 0.045 * s, goz, n=6, kat=3)
        q = p + sd * (sg * 0.3 * s) + Z * (0.3 * s)
        boru(y, [q - d * (0.15 * s), q + d * (0.15 * s) + Z * (0.03 * s), q + d * (0.35 * s) - sd * (sg * 0.1 * s)], 0.06 * s, kas, n=5, r_son=0.03 * s)
    # the nose curl and feathers sweeping back over the head
    n0 = p + d * (0.55 * s) + Z * (0.2 * s)
    boru(y, [n0, n0 + d * (0.08 * s) + Z * (0.12 * s), n0 - d * (0.05 * s) + Z * (0.2 * s), n0 - d * (0.1 * s) + Z * (0.1 * s)], 0.05 * s, kas, n=5)
    for k in range(5):
        q = p + sd * ((k - 2) * 0.14 * s) + Z * (0.3 * s) - d * (0.2 * s)
        boru(y, [q, q - d * (0.35 * s) + Z * (0.06 * s), q - d * (0.65 * s) - Z * (0.06 * s)], 0.06 * s, 'boya_yesil' if k % 2 else agiz, n=4, r_son=0.02 * s)


def kartal(y, x, yy, z, olcek=0.2, aci=0.0, key='ahsap', kanat='ahsap_acik', vurgu='beyaz', gaga='boya_sari', taban='bazalt',
           taban_h=0.1, bas_key='ahsap_acik'):
    """a perched eagle with spread wings (eagle warrior / cuauhxicalli eagle) on a block, facing aci; olcek its height.
    Returns the top z"""
    with parca(y, (x, yy, z), aci, olcek):
        if taban:
            kutu_merkez(y, (0, 0), 0.42, 0.34, taban_h, taban, z0=0)
            kornis(y, -0.21, 0.21, -0.17, 0.17, taban_h - 0.025, 0.025, 0.02, taban)
        b = taban_h
        elipsoid(y, (0, 0, b + 0.3), (0.13, 0.15, 0.24), key, n=12, kat=6)                  # body
        for s in (-1, 1):   # talons on the block
            elipsoid(y, (0.08, s * 0.06, b + 0.04), (0.07, 0.035, 0.04), gaga, n=6, kat=4)
        # tail: a fan of feathers down behind
        for k in range(5):
            t = (k - 2) * 0.16
            boru(y, [V(-0.08, 0, b + 0.16), V(-0.18, math.sin(t) * 0.12, b + 0.04)], 0.035, kanat if k % 2 else vurgu, n=4, r_son=0.02)
        elipsoid(y, (0.07, 0, b + 0.4), (0.07, 0.11, 0.12), bas_key, n=8, kat=4)          # pale breast
        kartal_bas(y, V(0.05, 0, b + 0.6), V(1, 0), 0.22, bas_key, gaga, 'koyu', key)
        # wings raised to take off: the arm up and out to the wrist, primaries fanning from it, secondaries hanging
        # from the arm, the leading edge pale
        for s in (-1, 1):
            o = V(-0.03, s * 0.1, b + 0.46)
            w = o + V(-0.1, s * 0.26, 0.24)
            boru(y, [o, o.lerp(w, 0.5) + V(0, 0, 0.03), w], 0.045, key, n=6, r_son=0.03)
            boru(y, [o + V(0.02, 0, 0.03), o.lerp(w, 0.5) + V(0.02, 0, 0.065), w + V(0.015, 0, 0.025)], 0.02, vurgu, n=4)
            for k in range(5):   # primaries
                th_ = math.radians(62 - 14 * k)
                d = V(-0.05, s * math.cos(th_), math.sin(th_))
                Lk = 0.24 - 0.02 * k
                boru(y, [w, w + d * (Lk * 0.5), w + d * Lk + V(0, 0, -0.02)], 0.028, kanat if k % 2 else key, n=4, r_son=0.01)
            for k in range(6):   # secondaries
                t = (k + 0.5) / 6
                p = o.lerp(w, t)
                boru(y, [p, p + V(-0.04, s * 0.05, -0.2 + 0.08 * t)], 0.03, kanat if k % 2 else key, n=4, r_son=0.012)
    return z + olcek * (taban_h + 0.95)


def daire(r, m=14, cx=0.0, cv=0.0):
    """a circle outline as (u, v) points (for levha)"""
    return [(cx + r * math.cos(TAU * i / m), cv + r * math.sin(TAU * i / m)) for i in range(m)]


def kartal_savasci(y, x, yy, z, boy=0.15, aci=0.0, takim='kiremit', tuy='siva', ten='kiremit', taban='bazalt'):
    """a standing eagle warrior (the life-size clay figures of the Casa de las Aguilas): a feather suit, wings hanging
    from the arms, talons at the knees, the head in an eagle helmet with its beak over the face, a round shield and a
    macuahuitl club; facing aci, boy high. Returns the top z"""
    with parca(y, (x, yy, z), aci, boy):
        if taban:
            kutu_merkez(y, (0, 0), 0.44, 0.44, 0.07, taban, z0=0)
        b = 0.07 if taban else 0.0
        for s in (-1, 1):
            boru(y, [V(0.0, s * 0.07, b), V(0.01, s * 0.07, b + 0.2), V(0.0, s * 0.075, b + 0.42)], 0.045, ten, n=6)
            elipsoid(y, (0.045, s * 0.07, b + 0.02), (0.075, 0.04, 0.025), ten, n=8, kat=4)
            for k in (-1, 0, 1):   # talons over the knees
                p = V(0.04, s * 0.07 + k * 0.022, b + 0.28)
                boru(y, [p, p + V(0.035, 0, -0.01), p + V(0.04, 0, -0.05)], 0.012, 'boya_sari', n=4, r_son=0.004)
            kutu_merkez(y, (0.0, s * 0.07), 0.1, 0.09, 0.03, tuy, z0=b + 0.3)       # knee feather cuff
        donel(y, (0, 0), [(0.11, b + 0.38), (0.135, b + 0.46), (0.145, b + 0.6), (0.13, b + 0.74), (0.09, b + 0.8), (0.0, b + 0.82)], takim, n=12)
        for zz in (0.42, 0.52, 0.62, 0.72):   # feather rows
            rr = 0.135 + 0.01 * math.sin(math.pi * (zz - 0.38) / 0.44)
            halka_kornis(y, (0, 0), rr, b + zz, 0.025, 0.012, 12, tuy, profil='yarim')
        for s in (-1, 1):
            sh = V(0.0, s * 0.14, b + 0.76); el = V(0.06, s * 0.21, b + 0.6); hd = V(0.14, s * 0.2, b + 0.54)
            boru(y, [sh, el, hd], 0.04, takim, n=6)
            kure(y, hd, 0.035, ten, n=6, kat=3)
            for k in range(6):   # the wing hanging from the arm
                p = sh.lerp(el, k / 5) if k < 5 else el.lerp(hd, 0.5)
                boru(y, [p, p + V(-0.05, s * 0.05, -0.2 - 0.03 * k)], 0.022, takim if k % 2 else tuy, n=4, r_son=0.01)
        # shield on the left arm, club in the right hand
        levha(y, V(0.12, -0.27, b + 0.56), X, daire(0.095, 14), 0.012, 'turkuaz', 'boya_sari')
        y.oculus(V(0.12, -0.2705, b + 0.56), X, -Y, 0.06, 'beyaz', 'boya_kirmizi', f=0.012, k=12)
        for k in range(5):
            t = -0.6 - 0.5 * k / 4
            p = V(0.12 + 0.095 * math.cos(t) * 0.0, -0.265, b + 0.56) + V(0.095 * math.cos(t), 0, 0.095 * math.sin(t))
            boru(y, [p, p + V(0.03 * math.cos(t), 0, 0.06 * math.sin(t) - 0.02)], 0.012, 'boya_yesil' if k % 2 else 'boya_kirmizi', n=4, r_son=0.005)
        hd = V(0.14, 0.2, b + 0.54)
        cubuk(y, hd - V(0, 0, 0.05), hd + V(0.06, 0.0, 0.36), 0.04, 'ahsap', 0.012)
        for k in range(6):
            t = 0.25 + 0.6 * k / 5
            p = (hd - V(0, 0, 0.05)).lerp(hd + V(0.06, 0, 0.36), t)
            for s in (-1, 1):
                kutu_merkez(y, (p.x + s * 0.024, p.y), 0.014, 0.006, 0.03, 'koyu', z0=p.z - 0.015)
        # head: the face under the eagle helmet
        kure(y, (0.06, 0, b + 0.9), 0.065, ten, n=10, kat=5)
        kartal_bas(y, V(0.0, 0, b + 0.96), V(1, 0), 0.24, takim, 'boya_sari', 'koyu', tuy)
    return z + boy * ((0.07 if taban else 0) + 1.08)


def alay_frizi(y, a, b, z0, h, adim=0.05, zemin_key='siva_oker', ileri=0.0015):
    """the procession of warriors on the Eagle House banquettes, painted just in front of the face a->b (facing its
    right) from z0, h high: on an ochre ground, figures with shields, feather headdresses and staffs, all walking
    the same way, a turquoise serpent band above"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    P = lambda u, v, d=1.0: a + e * u + Z * (z0 + v) + nc * (ileri * d)
    y.yuz_yon([P(0, h * 0.08), P(L, h * 0.08), P(L, h * 0.78), P(0, h * 0.78)], zemin_key, nc)
    y.yuz_yon([P(0, h * 0.78, 1.5), P(L, h * 0.78, 1.5), P(L, h, 1.5), P(0, h, 1.5)], 'turkuaz', nc)
    m = max(1, int(L / adim))
    renk = ('boya_kirmizi', 'turkuaz', 'boya_sari', 'beyaz')
    for i in range(m):
        u = (i + 0.5) * L / m
        w = adim * 0.16
        k = renk[i % 4]
        y.yuz_yon([P(u - w, h * 0.12, 2), P(u + w, h * 0.12, 2), P(u + w * 0.8, h * 0.55, 2), P(u - w * 0.8, h * 0.55, 2)], k, nc)       # body
        y.yuz_yon([P(u - w * 0.6, h * 0.55, 2), P(u + w * 0.6, h * 0.55, 2), P(u + w * 0.7, h * 0.66, 2), P(u - w * 0.5, h * 0.66, 2)], 'kiremit', nc)   # head
        y.yuz_yon([P(u - w * 1.6, h * 0.62, 2), P(u + w * 0.4, h * 0.66, 2), P(u - w * 0.4, h * 0.76, 2)], 'boya_yesil', nc)               # plume
        y.oculus(P(u + w * 1.3, h * 0.38, 2), e, nc, h * 0.14, 'beyaz' if k != 'beyaz' else 'boya_kirmizi', 'boya_kirmizi' if k != 'boya_kirmizi' else 'koyu', f=h * 0.04, k=8)
        y.yuz_yon([P(u - w * 1.4, h * 0.1, 2), P(u - w * 1.1, h * 0.1, 2), P(u - w * 1.1, h * 0.7, 2), P(u - w * 1.4, h * 0.7, 2)], 'ahsap_koyu', nc)   # staff


# ---------------------------------------------------------------- lake, fields, market
def kano(y, x, yy, z, L=0.22, W=0.05, D=0.025, aci=0.0, key='ahsap', ic_key='ahsap_koyu', yuk=None, kurek=True):
    """a dugout canoe (acalli) floating at z (its rim), L long, turned by aci; yuk: a list of keys for cargo
    (bundles, baskets) heaped in it"""
    with parca(y, (x, yy, z), aci):
        m = 10
        sec = lambda t, s=1.0, dz=0.0: (lambda w, d: [V(L * (t - 0.5), -w * s, dz), V(L * (t - 0.5), -w * 0.8 * s, -d * 0.7 + dz),
                                                        V(L * (t - 0.5), 0, -d + dz), V(L * (t - 0.5), w * 0.8 * s, -d * 0.7 + dz),
                                                        V(L * (t - 0.5), w * s, dz)])(W / 2 * max(0.18, math.sin(math.pi * t)) ** 0.7,
                                                                                   D * max(0.4, math.sin(math.pi * t)) ** 0.5)
        ts = [0.02 + 0.96 * k / m for k in range(m + 1)]
        dis_ = [sec(t) for t in ts]
        ic = [sec(t, 0.78, 0.004) for t in ts]
        for k in range(m):
            for i in range(4):
                q = [dis_[k][i], dis_[k + 1][i], dis_[k + 1][i + 1], dis_[k][i + 1]]
                yuz_dis(y, q, key, V(L * ((ts[k] + ts[k + 1]) / 2 - 0.5), 0, D * 0.4))
                qi = [ic[k][i], ic[k + 1][i], ic[k + 1][i + 1], ic[k][i + 1]]
                cc = sum(qi, Vector()) / 4
                y.yuz_yon(qi, ic_key, V(L * ((ts[k] + ts[k + 1]) / 2 - 0.5), 0, 0.05) - cc)
            # the rim
            for i in (0, 4):
                y.yuz_yon([dis_[k][i], dis_[k + 1][i], ic[k + 1][i], ic[k][i]], key, Z)
        for k, sg in ((0, -1), (m, 1)):   # the ends: the outer section outward, the inner one into the hull
            y.yuz_yon(dis_[k], key, V(sg, 0, 0))
            y.yuz_yon(ic[k], ic_key, V(-sg, 0, 0))
        if yuk:
            for i, kk in enumerate(yuk):
                u = (i + 0.5) / len(yuk) - 0.5
                elipsoid(y, (u * L * 0.55, 0, 0.004), (0.022, W * 0.34, 0.022), kk, n=8, kat=4)
        if kurek:
            cubuk(y, V(-L * 0.3, -W * 0.3, 0.008), V(L * 0.25, W * 0.15, 0.012), 0.004, 'ahsap_acik')
            kutu_merkez(y, (L * 0.29, W * 0.17), 0.04, 0.016, 0.003, 'ahsap_acik', z0=0.01)


def sogut(y, x, yy, z, boy=0.34, key='zeytin', key2='boya_yesil', govde='ahsap', tohum=0):
    """an ahuejote (Mexican willow) on a chinampa's edge: a slim straight trunk and a tall narrow crown of stacked tufts"""
    import random
    rn = random.Random(tohum)
    boru(y, [V(x, yy, z), V(x + rn.uniform(-0.004, 0.004), yy, z + boy * 0.5), V(x, yy, z + boy * 0.85)], 0.007, govde, n=5, r_son=0.004)
    for k in range(5):
        t = k / 4
        zz = z + boy * (0.32 + 0.6 * t)
        r = 0.032 * (1 - 0.55 * t) + 0.012
        elipsoid(y, (x + rn.uniform(-0.006, 0.006), yy + rn.uniform(-0.006, 0.006), zz), (r, r * 0.92, boy * 0.12), key if k % 2 == 0 else key2, n=7, kat=4, aci=k)


def misir(y, x, yy, z, boy=0.07, key='boya_yesil', koca='boya_sari', yon=0.0):
    """a maize plant: a stalk, two drooping leaves, a tassel and an ear"""
    cubuk(y, V(x, yy, z), V(x, yy, z + boy), 0.004, key)
    for s, h in ((1, 0.45), (-1, 0.7)):
        d = V(math.cos(yon + s * 1.3), math.sin(yon + s * 1.3))
        p = V(x, yy, z + boy * h)
        boru(y, [p, p + d * 0.014 + Z * 0.008, p + d * 0.026 - Z * 0.006], 0.0028, key, n=3, r_son=0.001)
    y.koni((x, yy), 0.004, z + boy, 0.016, koca, n=4)
    elipsoid(y, (x + 0.004, yy, z + boy * 0.55), (0.0035, 0.0035, 0.009), koca, n=5, kat=3)


def mangal(y, x, yy, z, s=0.06, key='siva_oker', bant='boya_kirmizi', ates=True):
    """a tall clay incense brazier (tlemaitl / incensario) with a burning top"""
    donel(y, (x, yy), [(0.0, z), (0.32 * s, z), (0.36 * s, z + 0.08 * s), (0.18 * s, z + 0.16 * s), (0.15 * s, z + 0.5 * s),
                       (0.2 * s, z + 0.62 * s), (0.48 * s, z + 0.8 * s), (0.5 * s, z + 0.92 * s), (0.42 * s, z + 0.92 * s), (0.0, z + 0.86 * s)], key, n=12)
    halka_kornis(y, (x, yy), 0.168 * s, z + 0.3 * s, 0.08 * s, 0.022 * s, 12, bant)
    if ates:
        for r, h, kk in ((0.32, 0.5, 'boya_kirmizi'), (0.2, 0.7, 'boya_sari'), (0.09, 0.45, 'beyaz')):
            y.koni((x, yy), r * s, z + 0.87 * s, h * s, kk, n=7)
    return z + 0.92 * s


def ince(y, pts, key, yon, kalin=0.002):
    """a thin sheet with real thickness: the face towards yon, its back kalin behind, and the rims (a cloth awning, a
    mat): seen edge-on nothing shows a back face"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    arka = [p - yon * kalin for p in pts]
    y.yuz_yon(pts, key, yon); y.yuz_yon(arka, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        m = (pts[i] + pts[j]) / 2
        y.yuz_yon([pts[i], pts[j], arka[j], arka[i]], key, m - c)


def insan(y, x, yy, z, aci=0.0, boy=0.065, giysi='beyaz', yuk=None, tohum=0):
    """a market goer: a white cotton cloak over a loincloth, brown skin, black hair; yuk: a key for a bundle carried
    on the back with a tumpline (a porter, tlameme)"""
    with parca(y, (x, yy, z), aci, boy):
        for s in (-1, 1):
            cubuk(y, V(0, s * 0.09, 0), V(0.02, s * 0.09, 0.42), 0.09, 'kiremit')
        donel(y, (0, 0), [(0.18, 0.3), (0.2, 0.45), (0.17, 0.72), (0.11, 0.8), (0.0, 0.81)], giysi, n=8)
        elipsoid(y, (0.0, 0, 0.62), (0.1, 0.19, 0.17), giysi, n=8, kat=4)
        kure(y, (0.02, 0, 0.9), 0.1, 'kiremit', n=8, kat=4)
        elipsoid(y, (-0.01, 0, 0.94), (0.1, 0.105, 0.08), 'koyu', n=8, kat=4)
        if yuk:
            elipsoid(y, (-0.2, 0, 0.62), (0.14, 0.17, 0.2), yuk, n=8, kat=4)
            boru(y, [V(-0.12, -0.1, 0.78), V(0.0, -0.08, 0.98), V(0.0, 0.08, 0.98), V(-0.12, 0.1, 0.78)], 0.012, 'ahsap_acik', n=4, kapat=False)


def tezgah(y, cx, cy, w=0.16, d=0.12, h=0.1, aci=0.0, tente=('kumas', 'boya_kirmizi'), mal=None, tohum=0, z=0.0, arka_oran=0.72):
    """a market stall: a reed mat on the ground with the goods on it (mal: 'misir' corn, 'kakao' cacao, 'tuy'
    feathers, 'comlek' pots, 'obsidyen' blades, 'kumas' cloth, 'meyve'), a bench at the back and (tente: keys of the
    strips; None: none) a lean-to shade on four poles over the back; arka_oran: height of its back poles / front
    poles (default slopes to the back; > 1 slopes to the front so a camera in front sees the shade's top)"""
    import random
    rn = random.Random(tohum)
    with parca(y, (cx, cy, z), aci):
        x0, x1, y0, y1 = -w / 2, w / 2, -d / 2, d / 2
        if tente:
            # a lean-to shade over the back of the stall, open to the aisle so the goods in front show
            yf = y0 + d * 0.7
            hf, hb = h, h * arka_oran
            for (px, py, ph) in ((x0, yf, hf), (x1, yf, hf), (x0, y1, hb), (x1, y1, hb)):
                if arka_oran > 1:   # (rising to the back: the poles stop under the shade instead of poking through it)
                    ya, yb_ = yf - 0.03, y1 + 0.012
                    ust = hf + 0.006 + (hb - hf - 0.002) * (py - ya) / (yb_ - ya) - 0.0035
                    cubuk(y, V(px, py, 0), V(px, py, ust), 0.006, 'ahsap')
                    continue
                cubuk(y, V(px, py, 0), V(px, py, ph + 0.004), 0.006, 'ahsap')
            ns = 4
            for k in range(ns):
                u0, u1 = x0 - 0.012 + (w + 0.024) * k / ns, x0 - 0.012 + (w + 0.024) * (k + 1) / ns
                ince(y, [V(u0, yf - 0.03, hf + 0.006), V(u1, yf - 0.03, hf + 0.006), V(u1, y1 + 0.012, hb + 0.004), V(u0, y1 + 0.012, hb + 0.004)],
                     tente[k % len(tente)], Z, 0.003)
            ince(y, [V(x0 - 0.012, yf - 0.03, hf - 0.012), V(x1 + 0.012, yf - 0.03, hf - 0.012), V(x1 + 0.012, yf - 0.03, hf + 0.006), V(x0 - 0.012, yf - 0.03, hf + 0.006)],
                 tente[-1], -Y, 0.003)
        # petate mat and a low bench at the back
        y.yuz_yon([V(x0 + 0.005, y0 + 0.005, 0.002), V(x1 - 0.005, y0 + 0.005, 0.002), V(x1 - 0.005, y1 - 0.005, 0.002), V(x0 + 0.005, y1 - 0.005, 0.002)], 'saz', Z)
        kutu_merkez(y, (0, y1 - 0.018), w - 0.02, 0.022, 0.02, 'ahsap_acik', z0=0.0)
        mal = mal or 'misir'
        if mal == 'misir':        # heaps of yellow and red cobs in baskets
            for i, kk in enumerate(('boya_sari', 'altin', 'boya_kirmizi')):
                px = x0 + w * (i + 0.5) / 3
                donel(y, (px, -0.022), [(0.0, 0.002), (0.022, 0.002), (0.028, 0.016), (0.026, 0.02), (0.0, 0.02)], 'saz_koyu', n=8)
                elipsoid(y, (px, -0.022, 0.02), (0.024, 0.024, 0.016), kk, n=8, kat=4, ust_yarim=True)
        elif mal == 'kakao':      # sacks and heaps of brown beans
            for i in range(3):
                px = x0 + w * (i + 0.5) / 3
                elipsoid(y, (px, -0.024, 0.002), (0.026, 0.024, 0.022), 'ahsap_acik' if i % 2 else 'kerpic_koyu', n=8, kat=4, ust_yarim=True)
            elipsoid(y, (0, y1 - 0.02, 0.02), (0.02, 0.012, 0.015), 'kumas', n=8, kat=4)
        elif mal == 'tuy':        # fans of quetzal and macaw feathers on racks
            for i, kk in enumerate(('boya_yesil', 'boya_kirmizi', 'turkuaz', 'boya_sari')):
                px = x0 + w * (i + 0.5) / 4
                for f in range(4):
                    t = (f - 1.5) * 0.25
                    boru(y, [V(px, -0.015, 0.004), V(px + math.sin(t) * 0.02, -0.022, 0.05)], 0.0035, kk, n=3, r_son=0.0015)
        elif mal == 'comlek':     # painted pots and bowls
            for i in range(4):
                px = x0 + w * (i + 0.5) / 4
                kk = ('siva_oker', 'kiremit', 'beyaz', 'kiremit2')[i]
                hh = 0.02 + 0.012 * (i % 2)
                donel(y, (px, -0.027), [(0.0, 0.002), (0.01, 0.002), (0.016, hh * 0.5), (0.011, hh), (0.013, hh + 0.004), (0.0, hh + 0.002)], kk, n=8)
                halka_kornis(y, (px, -0.027), 0.0155, 0.002 + hh * 0.42, hh * 0.1, 0.0015, 8, 'koyu' if i % 2 else 'boya_kirmizi')
        elif mal == 'obsidyen':   # black blades and cores on a cloth
            y.yuz_yon([V(x0 + 0.015, y0 + 0.015, 0.0035), V(x1 - 0.015, y0 + 0.015, 0.0035), V(x1 - 0.015, 0.02, 0.0035), V(x0 + 0.015, 0.02, 0.0035)], 'kumas', Z)
            for i in range(8):
                px = x0 + 0.025 + (w - 0.05) * i / 7
                py = y0 + 0.03 + rn.uniform(-0.008, 0.02)
                y.koni((px, py), 0.006, 0.0035, 0.012 + rn.uniform(0, 0.008), 'koyu', n=4)
        elif mal == 'kumas':      # folded cloth piles
            for i, kk in enumerate(('boya_kirmizi', 'kumas', 'turkuaz', 'boya_sari')):
                px = x0 + w * (i + 0.5) / 4
                for j in range(3):
                    kutu_merkez(y, (px, -0.022), 0.03, 0.026, 0.006, kk if j % 2 == 0 else 'beyaz', z0=0.002 + j * 0.006)
        else:                     # fruit: avocados, chillies, tomatoes in baskets
            for i, kk in enumerate(('boya_yesil', 'boya_kirmizi', 'siva_kirmizi')):
                px = x0 + w * (i + 0.5) / 3
                donel(y, (px, -0.022), [(0.0, 0.002), (0.02, 0.002), (0.026, 0.014), (0.0, 0.014)], 'saz', n=8)
                for f in range(4):
                    kure(y, (px + 0.009 * math.cos(f * 1.6), -0.022 + 0.009 * math.sin(f * 1.6), 0.018), 0.007, kk, n=5, kat=3)
