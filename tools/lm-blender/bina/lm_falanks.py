# A Macedonian phalanx camp (lm_falanks): the drill ground with a syntagma of 8 x 6 phalangites, the front ranks
# levelling their sarissas and the rear holding them raised, the officer and the trumpeter; racks of sarissas, rows of
# ridge tents with camp fires, the commander's house (tiled roof, a Doric porch with the Vergina sun in its pediment),
# the royal standard with the gilded sun, horse lines, supply wagons, the palisade with its gate towers and a tall
# timber watchtower.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from mathutils import Vector
from bina_ortak import calistir

y = Yapi()
TRI = 'lacivert'


# ================================================================ Greek helpers (this building's own)
def kiremit_kaburga(p0, p1, w=0.0055, key='mermer'):
    """a cover-tile rib along a roof slope from p0 to p1 (a low two-faced ridge)"""
    p0, p1 = Vector(p0), Vector(p1)
    t = (p1 - p0).normalized()
    s = Z.cross(t)
    if s.length < 1e-6: s = X.copy()
    s.normalize(); u = t.cross(s).normalized()
    if u.z < 0: u = -u
    h = u * (w * 0.55)
    A0, A1 = p0 - s * (w / 2), p1 - s * (w / 2)
    B0, B1 = p0 + s * (w / 2), p1 + s * (w / 2)
    y.yuz_yon([A0, A1, p1 + h, p0 + h], key, u - s)
    y.yuz_yon([p0 + h, p1 + h, B1, B0], key, u + s)
    y.yuz_yon([A0, B0, p0 + h], key, p0 - p1)


def kiremit_serit(x0, x1, y0, y1, z, h, adim=0.026, key='mermer'):
    """cover-tile ribs on a gable roof (ridge along y) from both eaves to the ridge"""
    n = max(1, int((y1 - y0) / adim))
    for j in range(n + 1):
        yy = y0 + (y1 - y0) * j / n
        for xe in (x0, x1):
            kiremit_kaburga(V(xe, yy, z + 0.0015), V((x0 + x1) / 2, yy, z + h + 0.0015), key=key)


def kolon(cx, cy, z0, z1, r, tur='dor', key='mermer', yiv=12):
    sutun(y, cx, cy, z0, z1, r, key, tur, yiv=yiv)


def figur(x, yy, z, s=1.0, key='mermer', aci=0.0, kol=1.0):
    """a draped standing figure (no pedestal), one arm raised (kol 0: both down)"""
    donel(y, (x, yy), [(0.014 * s, z), (0.016 * s, z + 0.02 * s), (0.011 * s, z + 0.055 * s), (0.013 * s, z + 0.068 * s),
                       (0.008 * s, z + 0.077 * s), (0, z + 0.079 * s)], key, n=10)
    kure(y, (x, yy, z + 0.088 * s), 0.008 * s, key, n=8, kat=4)
    e = V(math.cos(aci), math.sin(aci))
    if kol:
        boru(y, [V(x, yy, z + 0.064 * s) + e * 0.01 * s, V(x, yy, z + 0.095 * s * kol) + e * 0.022 * s], 0.0028 * s, key, n=5)


def uzanan(x, yy, z, yon, s=1.0, key='mermer'):
    """a reclining figure (river god in a pediment corner), lying along yon (+1 / -1 in x), propped on an elbow"""
    boru(y, [V(x, yy, z + 0.006 * s), V(x + yon * 0.03 * s, yy, z + 0.008 * s), V(x + yon * 0.055 * s, yy, z + 0.016 * s)], 0.0075 * s, key, n=7,
         r_son=0.006 * s)
    kure(y, (x + yon * 0.064 * s, yy, z + 0.026 * s), 0.0065 * s, key, n=8, kat=4)
    boru(y, [V(x + yon * 0.05 * s, yy, z + 0.016 * s), V(x + yon * 0.045 * s, yy, z + 0.002 * s)], 0.0025 * s, key, n=4)


def at(x, yy, z, aci=0.0, s=1.0, key='mermer'):
    """a rearing horse (pediment / chariot team), facing angle aci"""
    with parca(y, (x, yy, z), aci, s):
        boru(y, [V(-0.032, 0, 0.062), V(0, 0, 0.068), V(0.03, 0, 0.076)], 0.015, key, n=8)
        for lx, ly, up in ((0.024, 0.008, 1), (0.024, -0.008, 1), (-0.026, 0.008, 0), (-0.026, -0.008, 0)):
            if up:
                boru(y, [V(lx, ly, 0.064), V(lx + 0.018, ly, 0.05), V(lx + 0.014, ly, 0.034)], 0.0045, key, n=5)
            else:
                boru(y, [V(lx, ly, 0.058), V(lx + 0.002, ly, 0.028), V(lx, ly, 0.0)], 0.0045, key, n=5, r_son=0.0035)
        boru(y, [V(0.028, 0, 0.08), V(0.04, 0, 0.104), V(0.048, 0, 0.114)], 0.008, key, n=7, r_son=0.006)
        boru(y, [V(0.046, 0, 0.116), V(0.064, 0, 0.104)], 0.0055, key, n=6, r_son=0.004)
        boru(y, [V(-0.044, 0, 0.066), V(-0.054, 0, 0.044), V(-0.052, 0, 0.03)], 0.004, key, n=5, r_son=0.002)


def amfora(x, yy, z, s=1.0, key='siva_oker'):
    donel(y, (x, yy), [(0.0, z), (0.004 * s, z), (0.011 * s, z + 0.01 * s), (0.012 * s, z + 0.018 * s), (0.006 * s, z + 0.028 * s),
                       (0.004 * s, z + 0.034 * s), (0.0045 * s, z + 0.036 * s), (0, z + 0.036 * s)], key, n=8)


def zeytin(x, yy, z, boy=0.14, s=1.0):
    """an olive: a twisted grey trunk, a silvery crown in lumps"""
    top = V(x + 0.01 * s, yy, z + boy * 0.45)
    boru(y, [V(x, yy, z), V(x - 0.006 * s, yy + 0.003 * s, z + boy * 0.22), top], 0.007 * s, 'ahsap_acik', n=6, r_son=0.005 * s)
    for k, (dx, dy, dz, r) in enumerate(((0, 0, 0.62, 0.05), (0.035, 0.02, 0.52, 0.036), (-0.03, 0.022, 0.55, 0.035), (0.01, -0.035, 0.52, 0.036))):
        kure(y, (x + dx * s, yy + dy * s, z + boy * dz + 0.02 * s), r * s, 'zeytin', n=9, kat=5)


def kore(x, yy, z0, z1, s=1.0, key='mermer'):
    """a caryatid: a draped maiden on a low plinth carrying a polos and a capital block on her head"""
    H = z1 - z0
    kutu_merkez(y, (x, yy), 0.03 * s, 0.03 * s, H * 0.06, key, z0=z0)
    zb = z0 + H * 0.06
    donel(y, (x, yy), [(0.013 * s, zb), (0.014 * s, zb + H * 0.3), (0.011 * s, zb + H * 0.55), (0.012 * s, zb + H * 0.66), (0.008 * s, zb + H * 0.72),
                       (0.0045 * s, zb + H * 0.74)], key, n=10)
    for k in range(5):     # the folds of the chiton
        a = TAU * k / 5 + 0.3
        boru(y, [V(x + 0.0125 * s * math.cos(a), yy + 0.0125 * s * math.sin(a), zb + 0.002), V(x + 0.012 * s * math.cos(a), yy + 0.012 * s * math.sin(a), zb + H * 0.5)],
             0.0018 * s, key, n=4)
    kure(y, (x, yy, zb + H * 0.79), 0.0075 * s, key, n=8, kat=4)
    y.prizma((x, yy), 0.008 * s, zb + H * 0.83, z1 - H * 0.07, key, n=10)
    donel(y, (x, yy), [(0.008 * s, z1 - H * 0.07), (0.016 * s, z1 - H * 0.04)], key, n=10)
    kutu_merkez(y, (x, yy), 0.034 * s, 0.034 * s, H * 0.04, key, z0=z1 - H * 0.04)


def triglif_dizi(p, q, z, h, n, key=TRI, w=0.012, metop=None, rolyef=True):
    """n + 1 triglyphs on the frieze face p->q (faces its right), each with two grooves; between them metope panels
    (metop: the painted background) carrying a two-figure relief (a fight: Lapith and centaur, god and giant)"""
    W = (q - p).length; e = (q - p) / W; nc = V(e.y, -e.x)
    for i in range(n + 1):
        u = max(0.0, min(W - w, W * i / n - w / 2))
        o = p + e * u + Z * z
        kutu(y, o + nc * 0.0025, e, w, 0.0025, h, key, 'onsagsolust')
        for g in (0.33, 0.67):
            gg = o + e * (w * g) + nc * 0.0027
            y.yuz_yon([gg - e * 0.0012, gg + e * 0.0012, gg + e * 0.0012 + Z * (h * 0.85), gg - e * 0.0012 + Z * (h * 0.85)], 'koyu', nc)
        if metop and i < n:
            m0 = p + e * (W * i / n + w / 2 + 0.0015); m1 = p + e * (W * (i + 1) / n - w / 2 - 0.0015)
            mw = (m1 - m0).dot(e)
            if mw > 0.006:
                y.yuz_yon([m0 + nc * 0.001 + Z * (z + h * 0.1), m1 + nc * 0.001 + Z * (z + h * 0.1), m1 + nc * 0.001 + Z * (z + h * 0.9),
                           m0 + nc * 0.001 + Z * (z + h * 0.9)], metop, nc)
                if rolyef:
                    # two figures in relief: a leaning one and an upright one, alternating sides
                    sg = 1 if i % 2 else -1
                    fa = m0 + e * (mw * (0.3 if sg > 0 else 0.6))
                    fb = m0 + e * (mw * (0.66 if sg > 0 else 0.26))
                    kutu(y, fa + nc * 0.004 + Z * (z + h * 0.14), e, mw * 0.16, 0.0028, h * 0.68, 'mermer', 'onsagsolust')
                    kure(y, fa + e * (mw * 0.08) + nc * 0.0025 + Z * (z + h * 0.88), h * 0.09, 'mermer', n=6, kat=3)
                    # the other figure leans in (a slanted block)
                    b0 = fb + Z * (z + h * 0.14); b1 = fb + e * (-sg * mw * 0.12) + Z * (z + h * 0.72)
                    cubuk(y, b0 + nc * 0.0025, b1 + nc * 0.0025, mw * 0.14, 'mermer', 0.003)




ZG = 0.03                 # the camp ground


def kazik_cit(a, b, h=0.1, r=0.011, adim=0.024, key='kutuk'):
    """a palisade of sharpened logs from a to b, with a rail tying them on the inside"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    n = max(1, int(L / adim))
    g = random.Random(int(a.x * 100 + a.y * 37))
    for k in range(n + 1):
        p = a.lerp(b, k / n)
        hh = h * g.uniform(0.9, 1.08)
        y.prizma((p.x, p.y), r, ZG - 0.004, ZG + hh, key, n=6, ust=True, kat=g.random())
        y.koni((p.x, p.y), r, ZG + hh, 0.022, 'ahsap_acik', n=6)
    for zz in (0.35, 0.75):
        cubuk(y, a - nn * 0.014 + Z * (ZG + h * zz), b - nn * 0.014 + Z * (ZG + h * zz), 0.008, 'ahsap_koyu')


def ahsap_kule(cx, cy, w0, w1, h, cati_h=0.1, key='ahsap', merdiven_yon=None):
    """a timber watchtower: four battered posts, X braces in tiers, a planked platform with a railing, a tiled
    hipped roof on corner posts, a ladder. Returns the top z"""
    zt = ZG + h
    P0 = [V(cx + sx * w0 / 2, cy + sy * w0 / 2, ZG) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    P1 = [V(cx + sx * w1 / 2, cy + sy * w1 / 2, zt) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for a, b in zip(P0, P1):
        cubuk(y, a, b + Z * 0.005, 0.016, key)
        kutu_merkez(y, (a.x, a.y), 0.034, 0.034, 0.02, 'tas', z0=ZG - 0.004)
    tiers = 3
    for i in range(4):
        j = (i + 1) % 4
        for t in range(tiers):
            u0, u1 = t / tiers, (t + 1) / tiers
            A0, B0 = P0[i].lerp(P1[i], u0), P0[j].lerp(P1[j], u0)
            A1, B1 = P0[i].lerp(P1[i], u1), P0[j].lerp(P1[j], u1)
            cubuk(y, A0, B1, 0.008, 'ahsap_koyu')
            cubuk(y, B0, A1, 0.008, 'ahsap_koyu')
            cubuk(y, A1, B1, 0.01, key)
    # platform, railing, roof
    pw = w1 + 0.04
    kutu_merkez(y, (cx, cy), pw, pw, 0.014, 'ahsap_acik', z0=zt)
    y.yuz_yon([V(cx - pw / 2, cy - pw / 2, zt), V(cx + pw / 2, cy - pw / 2, zt), V(cx + pw / 2, cy + pw / 2, zt), V(cx - pw / 2, cy + pw / 2, zt)], 'ahsap_koyu', -Z)
    zp = zt + 0.014
    k4 = dikdortgen(cx - pw / 2 + 0.004, cx + pw / 2 - 0.004, cy - pw / 2 + 0.004, cy + pw / 2 - 0.004)
    for i in range(4):
        a, b = k4[i], k4[(i + 1) % 4]
        for u in (0.0, 0.25, 0.5, 0.75):
            p = a.lerp(b, u)
            y.prizma((p.x, p.y), 0.004, zp, zp + 0.04, key, n=4)
        cubuk(y, a + Z * (zp + 0.04), b + Z * (zp + 0.04), 0.007, key)
        cubuk(y, a + Z * (zp + 0.02), b + Z * (zp + 0.02), 0.005, key)
        # hide shields hung on the railing
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for u in (0.33, 0.67):
            c = a.lerp(b, u) + nn * 0.005 + Z * (zp + 0.026)
            boru(y, [c - nn * 0.002, c + nn * 0.002], 0.016, 'bronz', n=12)
    for p in k4:
        y.prizma((p.x, p.y), 0.006, zp, zp + 0.1, key, n=6)
    cati_kirma(y, cx - pw / 2, cx + pw / 2, cy - pw / 2, cy + pw / 2, zp + 0.1, cati_h, 0.022, 'kiremit', mahya='kiremit2', alt_key='ahsap_koyu',
               kalinlik=0.008, ns=4, nr=3)
    # two soldiers on watch
    for sx in (-1, 1):
        asker(cx + sx * 0.035, cy - 0.02, zp, -math.pi / 2, sarissa=False, s=0.9)
    if merdiven_yon is not None:
        e = V(math.cos(merdiven_yon), math.sin(merdiven_yon))
        s_ = V(-e.y, e.x)
        base = V(cx, cy) + e * (w0 / 2 + 0.09)
        top = V(cx, cy) + e * (w1 / 2 + 0.01)
        for sg in (-1, 1):
            cubuk(y, base + s_ * (sg * 0.02) + Z * ZG, top + s_ * (sg * 0.02) + Z * zt, 0.006, key)
        for k in range(1, 14):
            u = k / 14
            p = base.lerp(top, u) + Z * (ZG + (zt - ZG) * u)
            cubuk(y, p - s_ * 0.02, p + s_ * 0.02, 0.0035, 'ahsap_koyu')
    return zp + 0.1 + cati_h


def asker(x, yy, z, aci, sarissa=True, s=1.0, egim=1.1, renk='boya_kirmizi'):
    """a Macedonian phalangite: red tunic, linothorax, bronze helmet with a crest, the small round shield on his
    left with the Vergina star, and the six-metre sarissa held at the angle egim (radians above the horizontal)"""
    e = V(math.cos(aci), math.sin(aci)); sn = V(-e.y, e.x)
    with parca(y, (x, yy, z), 0.0, s):
        for sg in (-1, 1):
            boru(y, [V(0, 0, 0) + sn * (sg * 0.005), V(0, 0, 0.022) + sn * (sg * 0.005)], 0.003, 'kerpic', n=4)
            kutu_merkez(y, (sn.x * sg * 0.005 + e.x * 0.002, sn.y * sg * 0.005 + e.y * 0.002), 0.008, 0.008, 0.004, 'ahsap_koyu', z0=0, aci=aci)
        donel(y, (0, 0), [(0.0, 0.02), (0.011, 0.02), (0.009, 0.03), (0.0085, 0.045), (0.009, 0.052), (0.0, 0.054)], renk, n=7)
        donel(y, (0, 0), [(0.0094, 0.032), (0.0096, 0.048)], 'kumas', n=7)            # linothorax
        kure(y, (0, 0, 0.061), 0.0062, 'kerpic', n=6, kat=3)
        donel(y, (0, 0), [(0.0068, 0.06), (0.007, 0.066), (0.004, 0.072), (0.0, 0.074)], 'bronz', n=7)
        boru(y, [V(0, 0, 0.073) - e * 0.008, V(0, 0, 0.078), V(0, 0, 0.074) + e * 0.006], 0.002, 'beyaz', n=4)
        # the shield hanging from the left shoulder, facing forward
        c = V(0, 0, 0.036) + e * 0.011 + sn * 0.006
        boru(y, [c - e * 0.0015, c + e * 0.0015], 0.014, 'bronz', n=12)
        kure(y, c + e * 0.002, 0.003, 'altin', n=5, kat=3)
        if sarissa:
            hand = V(0, 0, 0.034) - sn * 0.008 + e * 0.006
            d = e * math.cos(egim) + Z * math.sin(egim)
            p0 = hand - d * 0.06
            if p0.z < 0.002: p0 = hand - d * ((hand.z - 0.002) / max(0.05, d.z))
            p1 = hand + d * 0.24
            cubuk(y, p0, p1, 0.0022, 'ahsap_acik')
            boru(y, [p1, p1 + d * 0.014], 0.0026, 'demir', n=4, r_son=0.0004)


def cadir_sirt(cx, cy, aci, L=0.15, W=0.1, H=0.075, key='kumas', renk=None):
    """a ridge tent: two canvas slopes over a short wall, closed ends with a door flap at the front, a pole tip, pegs"""
    with parca(y, (cx, cy, ZG), aci):
        hw = 0.012
        for sy in (-1, 1):
            y.yuz_yon([V(-L / 2, sy * W / 2, 0), V(L / 2, sy * W / 2, 0), V(L / 2, sy * W / 2, hw), V(-L / 2, sy * W / 2, hw)], key, V(0, sy, 0))
            y.yuz_yon([V(-L / 2, sy * W / 2, hw), V(L / 2, sy * W / 2, hw), V(L / 2, 0, H), V(-L / 2, 0, H)], renk or key, V(0, sy, 1))
            if renk:
                y.yuz_yon([V(-L / 2 - 0.0005, sy * W * 0.15, H * 0.85 + 0.0005), V(L / 2 + 0.0005, sy * W * 0.15, H * 0.85 + 0.0005),
                           V(L / 2 + 0.0005, 0, H + 0.001), V(-L / 2 - 0.0005, 0, H + 0.001)], key, V(0, sy, 1))
        for sx in (-1, 1):
            y.yuz_yon([V(sx * L / 2, -W / 2, 0), V(sx * L / 2, W / 2, 0), V(sx * L / 2, W / 2, hw), V(sx * L / 2, 0, H), V(sx * L / 2, -W / 2, hw)],
                      key, V(sx, 0, 0))
            y.prizma((sx * (L / 2 + 0.003), 0), 0.0025, 0, H + 0.02, 'ahsap', n=4)
        # the open door flap at the front end (+x): a dark triangle and a folded-back flap
        y.yuz_yon([V(L / 2 + 0.0008, -W * 0.18, 0), V(L / 2 + 0.0008, W * 0.18, 0), V(L / 2 + 0.0008, 0, H * 0.7)], 'koyu', X)
        for sy in (-1, 1):
            cubuk(y, V(-L * 0.3, sy * W / 2, hw), V(-L * 0.3, sy * (W / 2 + 0.04), 0), 0.0015, 'ahsap_koyu')
            cubuk(y, V(L * 0.3, sy * W / 2, hw), V(L * 0.3, sy * (W / 2 + 0.04), 0), 0.0015, 'ahsap_koyu')


def ates(x, yy, s=1.0):
    """a camp fire: a ring of stones, logs, flames; a cauldron on a tripod"""
    for k in range(8):
        a = TAU * k / 8
        kure(y, (x + 0.022 * s * math.cos(a), yy + 0.022 * s * math.sin(a), ZG + 0.003), 0.006 * s, 'kaya', n=5, kat=3)
    for k in range(3):
        a = TAU * k / 3 + 0.4
        cubuk(y, V(x - 0.016 * s * math.cos(a), yy - 0.016 * s * math.sin(a), ZG + 0.002), V(x + 0.016 * s * math.cos(a), yy + 0.016 * s * math.sin(a), ZG + 0.008),
              0.004 * s, 'ahsap_koyu')
    donel(y, (x, yy), [(0.012 * s, ZG + 0.004), (0.01 * s, ZG + 0.016 * s), (0.004 * s, ZG + 0.03 * s), (0.0, ZG + 0.04 * s)], 'boya_sari', n=6)
    donel(y, (x, yy), [(0.006 * s, ZG + 0.006), (0.005 * s, ZG + 0.02 * s), (0.0, ZG + 0.034 * s)], 'boya_kirmizi', n=5)


def mizrak_sehpa(cx, cy, aci, n=10, L=0.36):
    """a rack of sarissas: two A-frame trestles with a cross bar and the long pikes leaning on it"""
    e = V(math.cos(aci), math.sin(aci)); s_ = V(-e.y, e.x)
    hb = 0.07
    for u in (-0.4, 0.4):
        c = V(cx, cy) + e * (L * 0.3 * u * 2.2)
        for sg in (-1, 1):
            cubuk(y, c + s_ * (sg * 0.03) + Z * ZG, c + Z * (ZG + hb), 0.006, 'ahsap')
    a = V(cx, cy) - e * (L * 0.3) + Z * (ZG + hb)
    b = V(cx, cy) + e * (L * 0.3) + Z * (ZG + hb)
    cubuk(y, a, b, 0.007, 'ahsap_koyu')
    for k in range(n):
        p = a.lerp(b, (k + 0.5) / n)
        foot = p - s_ * 0.05 - Z * hb + Z * 0.002
        d = (p - foot).normalized()
        cubuk(y, foot, foot + d * L, 0.0028, 'ahsap_acik')
        boru(y, [foot + d * L, foot + d * (L + 0.016)], 0.003, 'demir', n=4, r_son=0.0004)


def vergina(c, e, nn, r, key='altin'):
    """the Vergina sun: a disc and sixteen rays, lying on a face (centre c, e along it, nn out)"""
    y.yuz_yon([c + nn * 0.0015 + e * (r * 0.32 * math.cos(TAU * a / 12)) + Z * (r * 0.32 * math.sin(TAU * a / 12)) for a in range(12)], key, nn)
    for k in range(16):
        a = TAU * k / 16
        d = e * math.cos(a) + Z * math.sin(a); q = e * math.cos(a + math.pi / 2) + Z * math.sin(a + math.pi / 2)
        w = r * (0.09 if k % 2 else 0.12)
        y.yuz_yon([c + nn * 0.0012 + d * (r * 0.3) - q * w, c + nn * 0.0012 + d * (r * 0.3) + q * w, c + nn * 0.0012 + d * r], key, nn)


# ================================================================ ground and palisade
y.bolum('Zemin ve palisad')
X0, X1, Y0, Y1 = -1.1, 1.1, -1.05, 1.05
kutu(y, V(X0, Y0, 0), X, X1 - X0, Y1 - Y0, ZG, 'toprak', 'onarkasagsol')
y.yuz_yon([V(X0, Y0, ZG), V(X1, Y0, ZG), V(X1, Y1, ZG), V(X0, Y1, ZG)], 'toprak', Z)
# grass round the outside of the palisade (a ring) and the ditch
PX0, PX1, PY0, PY1 = -1.0, 1.0, -0.95, 0.95
for (a, b, c, d) in ((V(X0, Y0), V(X1, Y0), V(PX1 + 0.06, PY0 - 0.06), V(PX0 - 0.06, PY0 - 0.06)),
                     (V(X1, Y0), V(X1, Y1), V(PX1 + 0.06, PY1 + 0.06), V(PX1 + 0.06, PY0 - 0.06)),
                     (V(X1, Y1), V(X0, Y1), V(PX0 - 0.06, PY1 + 0.06), V(PX1 + 0.06, PY1 + 0.06)),
                     (V(X0, Y1), V(X0, Y0), V(PX0 - 0.06, PY0 - 0.06), V(PX0 - 0.06, PY1 + 0.06))):
    y.yuz_yon([a + Z * (ZG + 0.001), b + Z * (ZG + 0.001), c + Z * (ZG + 0.001), d + Z * (ZG + 0.001)], 'cimen', Z)
GX = 0.13
kazik_cit((PX0, PY0), (-GX, PY0))
kazik_cit((GX, PY0), (PX1, PY0))
kazik_cit((PX1, PY0), (PX1, PY1))
kazik_cit((PX1, PY1), (PX0, PY1))
kazik_cit((PX0, PY1), (PX0, PY0))

y.bolum('Kapı kuleleri')
for sx in (-1, 1):
    ahsap_kule(sx * (GX + 0.07), PY0 + 0.02, 0.13, 0.11, 0.24, cati_h=0.06)
# the gate leaves standing open, the gate path
for sx in (-1, 1):
    with parca(y, (sx * GX, PY0, ZG), sx * 1.2 if sx < 0 else math.pi - 1.2):
        kutu(y, V(0, -0.004, 0), X, GX * 0.95, 0.008, 0.12, 'ahsap_dikey', 'onarkasagsolust')
        for zz in (0.02, 0.09):
            kutu(y, V(0.004, -0.0065, zz), X, GX * 0.9, 0.013, 0.012, 'ahsap_koyu', 'onarkasagsolust')
y.yuz_yon([V(-0.1, Y0, ZG + 0.002), V(0.1, Y0, ZG + 0.002), V(0.1, PY0 + 0.12, ZG + 0.002), V(-0.1, PY0 + 0.12, ZG + 0.002)], 'kum_acik', Z)
sancak(y, -(GX + 0.07), PY0 + 0.02, ZG + 0.24 + 0.014 + 0.16, boy=0.14, en=0.09, yuk=0.055, aci=math.pi * 0.85)
sancak(y, GX + 0.07, PY0 + 0.02, ZG + 0.24 + 0.014 + 0.16, boy=0.14, en=0.09, yuk=0.055, aci=math.pi * 0.15)

# ================================================================ the drill ground and the phalanx
y.bolum('Talim alanı ve falanks')
DX0, DX1, DY0, DY1 = -0.46, 0.46, -0.78, -0.12
y.yuz_yon([V(DX0, DY0, ZG + 0.002), V(DX1, DY0, ZG + 0.002), V(DX1, DY1, ZG + 0.002), V(DX0, DY1, ZG + 0.002)], 'kum_acik', Z)
for (a, b) in ((V(DX0, DY0), V(DX1, DY0)), (V(DX1, DY0), V(DX1, DY1)), (V(DX1, DY1), V(DX0, DY1)), (V(DX0, DY1), V(DX0, DY0))):
    e = (b - a).normalized()
    n = int((b - a).length / 0.09)
    for k in range(n + 1):
        p = a.lerp(b, k / n)
        y.prizma((p.x, p.y), 0.004, ZG, ZG + 0.03, 'ahsap', n=4)
    cubuk(y, a + Z * (ZG + 0.026), b + Z * (ZG + 0.026), 0.004, 'ahsap_koyu')
# the syntagma: 8 files x 6 ranks, the first ranks levelling their pikes, the rear holding them raised
for r in range(6):
    for c in range(8):
        x = -0.2 + c * 0.057
        yy = -0.6 + r * 0.06
        eg = 0.0 if r == 0 else (0.18 if r == 1 else (0.5 if r == 2 else 1.2 + 0.05 * r))
        asker(x, yy, ZG, -math.pi / 2, sarissa=True, egim=eg, renk='boya_kirmizi' if (r + c) % 5 else 'lacivert')
# the officer with a crested helmet before the front, a trumpeter
asker(-0.31, -0.64, ZG, -math.pi / 4, sarissa=False, s=1.1, renk='lacivert')
asker(0.3, -0.66, ZG, math.pi * 1.2, sarissa=False, s=1.0, renk='boya_sari')
boru(y, [V(0.3, -0.66, ZG + 0.07), V(0.32, -0.67, ZG + 0.09)], 0.003, 'bronz', n=5, r_son=0.007)
# racks of sarissas along the drill ground
for xx in (-0.56, 0.56):
    for yy in (-0.6, -0.3):
        mizrak_sehpa(xx, yy, math.pi / 2, n=9)

# ================================================================ tents
y.bolum('Çadır sıraları')
for side in (-1, 1):
    for row in range(5):
        for col in range(2):
            x = side * (0.72 + col * 0.17)
            yy = -0.7 + row * 0.24
            if side > 0 and row >= 4: continue
            cadir_sirt(x, yy, math.pi if side > 0 else 0.0, renk='boya_kirmizi' if (row + col) % 3 == 0 else None)
    for row in range(4):
        ates(side * 0.805, -0.58 + row * 0.24, 0.9)
        for k in range(2):
            a = TAU * k / 2 + row
            asker(side * 0.805 + 0.04 * math.cos(a), -0.58 + row * 0.24 + 0.04 * math.sin(a), ZG, a + math.pi, sarissa=False, s=0.9)

y.bolum('Komutan evi ve Vergina sancağı')
HX0, HX1, HY0, HY1 = -0.3, 0.3, 0.5, 0.82
kutu(y, V(HX0 - 0.03, HY0 - 0.12, ZG), X, HX1 - HX0 + 0.06, HY1 - HY0 + 0.15, 0.025, 'kirec', 'onarkasagsol')
y.yuz_yon([V(HX0 - 0.03, HY0 - 0.12, ZG + 0.025), V(HX1 + 0.03, HY0 - 0.12, ZG + 0.025), V(HX1 + 0.03, HY1 + 0.03, ZG + 0.025),
           V(HX0 - 0.03, HY1 + 0.03, ZG + 0.025)], 'zemin', Z)
merdiven(y, (0.0, HY0 - 0.12 - 0.03), math.pi / 2, 0.16, ZG, ZG + 0.025, n=3, d=0.01, key='kirec')
zh = ZG + 0.025
HH = 0.17
k4 = dikdortgen(HX0, HX1, HY0, HY1)
for i in range(4):
    a, b = k4[i], k4[(i + 1) % 4]
    if i == 0:
        for k in range(5):
            p, q = a.lerp(b, k / 5), a.lerp(b, (k + 1) / 5)
            if k == 2:
                dikdortgen_acik(y, p, q, zh, HH, 0.22, 0.78, 0.0, HH * 0.66, ('siva_krem', 'tas_acik', 'kirec', 'ahsap'), derin=0.012, cerceve=(0.006, 'kirec'))
            else:
                dikdortgen_acik(y, p, q, zh, HH, 0.3, 0.7, HH * 0.4, HH * 0.72, ('siva_krem', 'tas_acik', 'kirec', 'koyu'), derin=0.01, cerceve=(0.005, 'kirec'))
    else:
        n = 3 if i % 2 else 5
        for k in range(n):
            p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
            dikdortgen_acik(y, p, q, zh, HH, 0.36, 0.64, HH * 0.45, HH * 0.72, ('siva_krem', 'tas_acik', 'kirec', 'koyu'), derin=0.01)
silme(y, k4, zh, 0.03, 0.006, 'kirec', 'kaide')
silme(y, k4, zh + HH - 0.016, 0.016, 0.01, 'kirec', 'tac')
y.yuz_yon([V(p.x, p.y, zh + HH) for p in k4], 'kirec', Z)
cati_besik(y, HX0 - 0.004, HX1 + 0.004, HY0 - 0.004, HY1 + 0.004, zh + HH, 0.09, 0.03, 'kiremit', mahya='kiremit2', ucluk_key='siva_krem',
           alinlik_key='kirec', alt_key='ahsap_koyu', kalinlik=0.008, ns=10, nr=4, dilim=['kiremit', 'kiremit2'])
# the porch: four Doric columns, an entablature, a pediment with the Vergina sun
for k in range(4):
    kolon(-0.15 + k * 0.1, HY0 - 0.09, zh, zh + HH * 0.9, 0.012, 'dor', 'kirec', yiv=10)
kutu(y, V(-0.18, HY0 - 0.105, zh + HH * 0.9), X, 0.36, 0.105, 0.03, 'kirec', 'onsagsol')
y.yuz_yon([V(-0.18, HY0 - 0.105, zh + HH * 0.9), V(0.18, HY0 - 0.105, zh + HH * 0.9), V(0.18, HY0, zh + HH * 0.9), V(-0.18, HY0, zh + HH * 0.9)], 'tas_koyu', -Z)
triglif_dizi(V(-0.18, HY0 - 0.1055), V(0.18, HY0 - 0.1055), zh + HH * 0.9 + 0.012, 0.016, 10, w=0.008, metop='boya_kirmizi', rolyef=False)
zpo = zh + HH * 0.9 + 0.03
y.yuz_yon([V(-0.18, HY0 - 0.105, zpo), V(0.18, HY0 - 0.105, zpo), V(0.18, HY0, zpo), V(-0.18, HY0, zpo)], 'kirec', Z)
alinlik(y, V(-0.19, HY0 - 0.11), V(0.19, HY0 - 0.11), zpo, 0.055, derin=0.11, key='kirec', ic_key='lacivert', c=0.008, cati_key='kiremit')
vergina(V(0, HY0 - 0.11 - 0.0005, zpo + 0.026), X, -Y, 0.02)
# the royal standard: a tall pole with the gilded sixteen-rayed sun, and the banner
SPX, SPY = 0.0, 0.3
kutu_merkez(y, (SPX, SPY), 0.06, 0.06, 0.02, 'kirec', z0=ZG)
y.prizma((SPX, SPY), 0.006, ZG + 0.02, ZG + 0.42, 'ahsap', n=8)
cubuk(y, V(SPX - 0.06, SPY, ZG + 0.36), V(SPX + 0.06, SPY, ZG + 0.36), 0.006, 'ahsap')
for k in range(16):   # the sixteen rays as thin gilded blades (seen from both sides)
    a = TAU * k / 16
    d = V(math.cos(a), 0, math.sin(a))
    cubuk(y, V(SPX, SPY, ZG + 0.43) + d * 0.014, V(SPX, SPY, ZG + 0.43) + d * (0.05 if k % 2 == 0 else 0.042), 0.007, 'altin', 0.003)
boru(y, [V(SPX, SPY - 0.006, ZG + 0.43), V(SPX, SPY + 0.006, ZG + 0.43)], 0.018, 'altin', n=16)
for s_ in (-1, 1):   # tassels
    cubuk(y, V(SPX + s_ * 0.058, SPY, ZG + 0.36), V(SPX + s_ * 0.058, SPY, ZG + 0.32), 0.005, 'boya_kirmizi')
sancak(y, SPX + 0.12, SPY, ZG, boy=0.3, en=0.12, yuk=0.075, aci=math.pi * 0.1)
# guards at the porch
for sx in (-1, 1):
    asker(sx * 0.24, HY0 - 0.11, ZG + 0.025, -math.pi / 2, sarissa=True, egim=1.45, s=1.0, renk='lacivert')

y.bolum('Gözcü kulesi, atlar, arabalar')
TOP = ahsap_kule(0.78, 0.74, 0.22, 0.15, 0.6, cati_h=0.1, merdiven_yon=math.pi)
sancak(y, 0.78, 0.74, TOP - 0.02, boy=0.16, en=0.1, yuk=0.06, aci=math.pi * 0.8)
# the horse lines: a picket rope between posts, Thessalian horses, a hay pile and a trough
for x in (0.38, 0.58):
    y.prizma((x, 0.12), 0.005, ZG, ZG + 0.06, 'ahsap', n=5)
cubuk(y, V(0.38, 0.12, ZG + 0.055), V(0.58, 0.12, ZG + 0.055), 0.003, 'kumas')
for k, x in enumerate((0.41, 0.46, 0.51, 0.56)):
    at(x, 0.15, ZG, aci=math.pi / 2 + (0.15 if k % 2 else -0.1), s=0.62, key='ahsap' if k % 2 else 'kerpic_koyu')
donel(y, (0.62, 0.24), [(0.04, ZG), (0.035, ZG + 0.025), (0.0, ZG + 0.04)], 'saz', n=10)
kutu_merkez(y, (0.48, 0.07), 0.16, 0.025, 0.018, 'ahsap', z0=ZG)
y.yuz_yon([V(0.405, 0.062, ZG + 0.0185), V(0.555, 0.062, ZG + 0.0185), V(0.555, 0.078, ZG + 0.0185), V(0.405, 0.078, ZG + 0.0185)], 'su', Z)
# supply wagons and amphorae behind the left tents
for k, (x, yy) in enumerate(((-0.6, 0.62), (-0.42, 0.76))):
    with parca(y, (x, yy, ZG), 0.3 * k):
        kutu(y, V(-0.06, -0.035, 0.03), X, 0.12, 0.07, 0.03, 'ahsap', 'onarkasagsolust')
        y.yuz_yon([V(-0.06, -0.035, 0.03), V(0.06, -0.035, 0.03), V(0.06, 0.035, 0.03), V(-0.06, 0.035, 0.03)], 'ahsap_koyu', -Z)
        for sx in (-1, 1):
            for sy in (-1, 1):
                boru(y, [V(sx * 0.035, sy * 0.036, 0.022), V(sx * 0.035, sy * 0.044, 0.022)], 0.022, 'ahsap_koyu', n=10)
        cubuk(y, V(0.06, 0, 0.035), V(0.13, 0, 0.012), 0.006, 'ahsap')
        for j in range(3):
            amfora(-0.035 + j * 0.035, 0.0, 0.06, 1.1, 'siva_oker')
for k in range(6):
    amfora(-0.52 + k * 0.035, 0.3 + (k % 2) * 0.012, ZG, 1.2, 'siva_oker' if k % 2 else 'kirmizi')
for x, yy in ((-0.92, 0.85), (0.4, 0.86), (-0.15, 0.9)):
    agac(y, x, yy, ZG, 0.13, 'servi')

y.bolum('Kamp yolları, demirhane, talim kazıkları')
# trodden ways: the camp street across the camp, the way up to the commander's house, the tent lanes
ZY = ZG + 0.0015


def yol_serit(a, b, en, key='kum_acik'):
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); s_ = V(-e.y, e.x) * (en / 2)
    y.yuz_yon([a - s_ + Z * ZY, b - s_ + Z * ZY, b + s_ + Z * ZY, a + s_ + Z * ZY], key, Z)


yol_serit((-0.64, -0.04), (0.64, -0.04), 0.09)
yol_serit((0.0, 0.005), (0.0, 0.265), 0.08)
for sx in (-1, 1):   # the trampled ground round each camp fire
    for row in range(4):
        cx_, cy_ = sx * 0.805, -0.58 + row * 0.24
        y.yuz_yon([V(cx_ + 0.075 * math.cos(TAU * a / 12), cy_ + 0.05 * math.sin(TAU * a / 12), ZY) for a in range(12)], 'kum_acik', Z)
# the smithy: an open shed on posts with a tiled roof, the forge, the anvil, the quench trough, shields and helmets
FX0, FX1, FY0, FY1 = -0.5, -0.32, 0.09, 0.22
kutu(y, V(FX0 - 0.01, FY0 - 0.01, ZG), X, FX1 - FX0 + 0.02, FY1 - FY0 + 0.02, 0.008, 'tas', 'onarkasagsolust')
zf = ZG + 0.008
for px, py in ((FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1), ((FX0 + FX1) / 2, FY0), ((FX0 + FX1) / 2, FY1)):
    y.prizma((px, py), 0.006, zf, zf + 0.09, 'ahsap', n=6)
kutu(y, V(FX0, FY1 - 0.004, zf), X, FX1 - FX0, 0.008, 0.06, 'ahsap_dikey', 'onarkasagsolust')     # the plank back wall
cati_kirma(y, FX0 - 0.012, FX1 + 0.012, FY0 - 0.012, FY1 + 0.012, zf + 0.09, 0.05, 0.012, 'kiremit', mahya='kiremit2', alt_key='ahsap_koyu',
           kalinlik=0.006, ns=4, nr=3)
# the forge: a stone hearth with its chimney hood and the glowing coals, the bellows
kutu_merkez(y, (FX0 + 0.04, FY1 - 0.035), 0.06, 0.05, 0.035, 'tas', z0=zf)
y.yuz_yon([V(FX0 + 0.015, FY1 - 0.055, zf + 0.0355), V(FX0 + 0.065, FY1 - 0.055, zf + 0.0355), V(FX0 + 0.065, FY1 - 0.02, zf + 0.0355),
           V(FX0 + 0.015, FY1 - 0.02, zf + 0.0355)], 'boya_kirmizi', Z)
donel(y, (FX0 + 0.04, FY1 - 0.037), [(0.012, zf + 0.035), (0.008, zf + 0.05), (0.0, zf + 0.062)], 'boya_sari', n=6)
donel(y, (FX0 + 0.04, FY1 - 0.03), [(0.026, zf + 0.075), (0.012, zf + 0.11), (0.012, zf + 0.15)], 'tas_koyu', n=8)
kutu_merkez(y, (FX0 + 0.085, FY1 - 0.03), 0.03, 0.02, 0.012, 'ahsap_koyu', z0=zf + 0.012)
# the anvil on its stump and the smith, the quench trough, finished shields leaning on a rack
y.prizma((FX0 + 0.1, FY0 + 0.05), 0.012, zf, zf + 0.025, 'kutuk', n=8)
kutu_merkez(y, (FX0 + 0.1, FY0 + 0.05), 0.026, 0.012, 0.012, 'demir', z0=zf + 0.025)
boru(y, [V(FX0 + 0.113, FY0 + 0.05, zf + 0.031), V(FX0 + 0.126, FY0 + 0.05, zf + 0.033)], 0.004, 'demir', n=5, r_son=0.001)
asker(FX0 + 0.1, FY0 + 0.02, zf, math.pi / 2, sarissa=False, s=0.95, renk='kumas')
kutu_merkez(y, (FX1 - 0.03, FY0 + 0.03), 0.05, 0.025, 0.015, 'ahsap', z0=zf)
y.yuz_yon([V(FX1 - 0.052, FY0 + 0.02, zf + 0.0152), V(FX1 - 0.008, FY0 + 0.02, zf + 0.0152), V(FX1 - 0.008, FY0 + 0.04, zf + 0.0152),
           V(FX1 - 0.052, FY0 + 0.04, zf + 0.0152)], 'su', Z)
for k in range(4):
    c = V(FX1 - 0.025 - k * 0.028, FY1 - 0.012, zf + 0.02)
    boru(y, [c, c - Y * 0.004], 0.015, 'bronz', n=12)
    kure(y, c - Y * 0.0045, 0.003, 'altin', n=5, kat=3)
for k in range(3):   # bronze helmets drying on a bench
    donel(y, (FX1 - 0.03 - k * 0.02, FY0 + 0.075), [(0.007, zf + 0.012), (0.0075, zf + 0.018), (0.004, zf + 0.024), (0.0, zf + 0.026)], 'bronz', n=7)
kutu_merkez(y, (FX1 - 0.05, FY0 + 0.075), 0.08, 0.016, 0.012, 'ahsap_koyu', z0=zf)
# training posts: stakes with a cross bar, a wicker shield and a straw head, a soldier at each
for k, px in enumerate((0.12, 0.2, 0.28)):
    py = 0.14
    y.prizma((px, py), 0.005, ZG, ZG + 0.075, 'kutuk', n=6)
    cubuk(y, V(px - 0.022, py, ZG + 0.055), V(px + 0.022, py, ZG + 0.055), 0.006, 'ahsap')
    kure(y, (px, py, ZG + 0.085), 0.01, 'saz', n=7, kat=4)
    boru(y, [V(px, py - 0.006, ZG + 0.04), V(px, py - 0.01, ZG + 0.04)], 0.016, 'saz', n=10)
    asker(px, py - 0.06, ZG, math.pi / 2, sarissa=k != 1, egim=0.25, s=0.95)
# hay stacks and the camp well near the watchtower
for hx, hy, r in ((0.47, 0.38, 0.04), (0.53, 0.32, 0.03)):
    donel(y, (hx, hy), [(r, ZG), (r * 1.05, ZG + r * 0.5), (r * 0.7, ZG + r * 1.1), (0.0, ZG + r * 1.4)], 'saz', n=10)
WX, WY = 0.5, 0.53
donel(y, (WX, WY), [(0.034, ZG), (0.034, ZG + 0.03), (0.026, ZG + 0.03), (0.026, ZG + 0.004), (0.0, ZG + 0.004)], 'tas', n=12)
y.yuz_yon([V(WX + 0.02 * math.cos(TAU * a / 12), WY + 0.02 * math.sin(TAU * a / 12), ZG + 0.02) for a in range(12)], 'su', Z)
for sx in (-1, 1):
    y.prizma((WX + sx * 0.03, WY), 0.004, ZG + 0.03, ZG + 0.085, 'ahsap', n=5)
cubuk(y, V(WX - 0.034, WY, ZG + 0.08), V(WX + 0.034, WY, ZG + 0.08), 0.006, 'ahsap_koyu')
donel(y, (WX, WY), [(0.008, ZG + 0.045), (0.009, ZG + 0.06), (0.0, ZG + 0.06)], 'ahsap', n=7)
# the quartermaster's bell tent with its striped canvas, sacks and barrels before it
with parca(y, (-0.8, 0.56, ZG)):
    cadir(y, (0.0, 0.0), 0.095, 0.16, 'kumas', 'boya_kirmizi', n=16)
for k, (sx, sy) in enumerate(((-0.86, 0.43), (-0.83, 0.42), (-0.8, 0.44), (-0.74, 0.43))):
    if k % 2:
        donel(y, (sx, sy), [(0.012, ZG), (0.013, ZG + 0.012), (0.012, ZG + 0.025), (0.0, ZG + 0.025)], 'ahsap', n=8)
    else:
        kure(y, (sx, sy, ZG + 0.01), 0.013, 'kumas', n=8, kat=4)

calistir(y, 'lm_falanks')
