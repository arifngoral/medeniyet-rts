# The triumphal arch (lm_zafertaki), after the Arch of Constantine: a marble arch of three passages with four detached
# Corinthian columns (giallo antico) on sculpted pedestals on each face, entablature breaks carrying statues of
# captives, roundels and a frieze over the side arches, Victories in the spandrels, an attic with the inscription and
# relief panels, a bronze quadriga on top; on a paved square crossed by the triumphal road, with the Meta Sudans
# fountain, the colossal statue and umbrella pines.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
import parcalar
from parcalar import *
from bina_ortak import calistir

y = Yapi(tohum=21)
rng = y.rng

ZF = 0.02                    # square paving
XA = 0.75                    # half width of the arch
DA = 0.43                    # depth
HB = 0.72                    # body (up to the top of the main entablature)
ZB = ZF + HB
ZE0 = ZB - 0.1               # main entablature bottom
ZAT = ZB + 0.32              # attic top (below its cornice)
CX = (-0.7, -0.3, 0.3, 0.7)  # column axes
BODY, ORN, KOLON = 'kirec', 'mermer', 'kum_acik'
COL_Y = 0.05                 # columns stand this far in front of the wall
RC = 0.028


def kabartma(o, ex, n, w, h, nfig=4, key=ORN, zemin_key='tas', derin=0.006):
    """a relief panel on a wall: o = bottom-left on the wall face, ex along it, n out: a frame, a recessed ground and
    a row of figures (bodies with heads, some with raised arms) in low relief"""
    o, ex, n = V(*o), V(*ex), V(*n)
    P = lambda u, v, d: o + ex * u + Z * v + n * d
    f = min(w, h) * 0.08
    for (u0, v0, u1, v1) in ((0, 0, w, f), (0, h - f, w, h), (0, f, f, h - f), (w - f, f, w, h - f)):
        q = [P(u0, v0, derin), P(u1, v0, derin), P(u1, v1, derin), P(u0, v1, derin)]
        y.yuz_yon(q, key, n)
    for (u0, u1, v0, v1, yon) in ((0, w, h, h, Z), (0, w, 0, 0, -Z)):
        y.yuz_yon([P(u0, v0, 0), P(u1, v0, 0), P(u1, v0, derin), P(u0, v0, derin)], key, yon)
    for u_, yon in ((0, -ex), (w, ex)):
        y.yuz_yon([P(u_, 0, 0), P(u_, h, 0), P(u_, h, derin), P(u_, 0, derin)], key, yon)
    y.yuz_yon([P(f, f, 0.0015), P(w - f, f, 0.0015), P(w - f, h - f, 0.0015), P(f, h - f, 0.0015)], zemin_key, n)
    # the frame's inner edges, down to the recessed ground (or the outer edges' backs show through the gap)
    ic = [(f, f), (w - f, f), (w - f, h - f), (f, h - f)]
    mc = P(w / 2, h / 2, derin)
    for k in range(4):
        (ua, va), (ub, vb) = ic[k], ic[(k + 1) % 4]
        q = [P(ua, va, 0.0015), P(ub, vb, 0.0015), P(ub, vb, derin), P(ua, va, derin)]
        y.yuz_yon(q, key, mc - (q[0] + q[1]) / 2)
    fw = (w - 2 * f) / nfig
    for i in range(nfig):
        u = f + fw * (i + 0.5) + rng.uniform(-0.15, 0.15) * fw
        hh = (h - 2 * f) * rng.uniform(0.6, 0.8)
        bw = fw * 0.34
        q = [P(u - bw / 2, f + 0.002, 0.0055), P(u + bw / 2, f + 0.002, 0.0055), P(u + bw * 0.4, f + hh * 0.78, 0.0055), P(u - bw * 0.4, f + hh * 0.78, 0.0055)]
        y.yuz_yon(q, key, n)
        for (a, b) in ((0, 1), (1, 2), (2, 3), (3, 0)):
            pa, pb = q[a], q[b]
            y.yuz_yon([pa, pb, pb - n * 0.004, pa - n * 0.004], key, ((pa + pb) / 2 - sum(q, V(0, 0, 0)) / 4))
        hr = bw * 0.36
        c = P(u, f + hh * 0.78 + hr * 1.1, 0.0015)
        y.yuz_yon([c + ex * (hr * math.cos(TAU * k / 8)) + Z * (hr * math.sin(TAU * k / 8)) + n * 0.004 for k in range(8)], key, n)
        if rng.random() < 0.5:   # a raised arm / spear
            s = 1 if rng.random() < 0.5 else -1
            pa = P(u + s * bw * 0.4, f + hh * 0.7, 0.004); pb = P(u + s * bw * 1.1, f + hh * 1.0, 0.004)
            cubuk(y, pa, pb, bw * 0.22, key, 0.003)


HARF = {
    'I': [((0.5, 0), (0.5, 1))], 'M': [((0, 0), (0, 1)), ((0, 1), (0.5, 0.4)), ((0.5, 0.4), (1, 1)), ((1, 1), (1, 0))],
    'P': [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0.5)), ((1, 0.5), (0, 0.5))],
    'C': [((1, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (1, 0))], 'A': [((0, 0), (0.5, 1)), ((0.5, 1), (1, 0)), ((0.25, 0.45), (0.75, 0.45))],
    'E': [((1, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (1, 0)), ((0, 0.5), (0.8, 0.5))],
    'S': [((1, 1), (0, 1)), ((0, 1), (0, 0.5)), ((0, 0.5), (1, 0.5)), ((1, 0.5), (1, 0)), ((1, 0), (0, 0))],
    'F': [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((0, 0.5), (0.8, 0.5))], 'L': [((0, 1), (0, 0)), ((0, 0), (1, 0))],
    'O': [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0)), ((1, 0), (0, 0))],
    'N': [((0, 0), (0, 1)), ((0, 1), (1, 0)), ((1, 0), (1, 1))], 'T': [((0, 1), (1, 1)), ((0.5, 1), (0.5, 0))],
    'X': [((0, 0), (1, 1)), ((0, 1), (1, 0))], 'V': [((0, 1), (0.5, 0)), ((0.5, 0), (1, 1))],
    'G': [((1, 1), (0, 1)), ((0, 1), (0, 0)), ((0, 0), (1, 0)), ((1, 0), (1, 0.45)), ((1, 0.45), (0.55, 0.45))],
    'Q': [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0)), ((1, 0), (0, 0)), ((0.6, 0.3), (1.1, -0.15))],
    'R': [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0.5)), ((1, 0.5), (0, 0.5)), ((0.4, 0.5), (1, 0))],
    'D': [((0, 0), (0, 1)), ((0, 1), (0.7, 1)), ((0.7, 1), (1, 0.6)), ((1, 0.6), (1, 0.4)), ((1, 0.4), (0.7, 0)), ((0.7, 0), (0, 0))],
}


def yazi(P, metin, um, v, uw, vh, n, key='bronz', w=0.0032):
    """a line of capitals in bronze strokes, centred on um, on a face given by P(u, v, d)"""
    u0 = um - len(metin) * uw / 2
    for i, ch in enumerate(metin):
        for (a, b) in HARF.get(ch, []):
            pa = V(u0 + i * uw + uw * 0.18 + a[0] * uw * 0.64, v + a[1] * vh)
            pb = V(u0 + i * uw + uw * 0.18 + b[0] * uw * 0.64, v + b[1] * vh)
            d = pb - pa; L = d.length
            if L < 1e-9: continue
            d /= L; s_ = V(-d.y, d.x) * (w / 2)
            q = [pa - s_ - d * (w / 2), pb - s_ + d * (w / 2), pb + s_ + d * (w / 2), pa + s_ - d * (w / 2)]
            y.yuz_yon([P(p.x, p.y, 0.0035) for p in q], key, n)


def plaka(W, pts, d, key, n):
    """a low-relief shape: the outline pts [(x, z)] on the wall W(x, z, d), raised d with its edges"""
    on = [W(px, pz, d) for px, pz in pts]
    y.yuz_yon(on, key, n)
    m = sum(on, V(0, 0, 0)) / len(on)
    for i in range(len(pts)):
        a, b = on[i], on[(i + 1) % len(on)]
        y.yuz_yon([a, b, b - n * d, a - n * d], key, (a + b) / 2 - m)


def zafer_tanrica(W, n, cx, cz, sx, s=1.0, key=ORN):
    """a winged Victory flying towards the keystone (sx = -1 left spandrel, +1 right): trailing robe, body, head,
    two wings swept back, an arm reaching out with a wreath"""
    dx, dz = -sx * 0.78, 0.62                       # flight direction (towards the arch's crown)
    # u along the flight, v to the figure's back (the wing side)
    P = lambda u, v: (cx + (dx * u + sx * dz * v) * s, cz + (dz * u + abs(dx) * v) * s)
    # robe and body: a long tapering shape along the flight line
    plaka(W, [P(-0.05, -0.006), P(-0.038, -0.016), P(0.02, -0.011), P(0.034, -0.006), P(0.034, 0.007), P(0.02, 0.011),
              P(-0.03, 0.012)], 0.005, key, n)
    # head
    hx, hz = P(0.047, 0.0)
    plaka(W, [(hx + 0.0085 * s * math.cos(TAU * k / 8), hz + 0.0085 * s * math.sin(TAU * k / 8)) for k in range(8)], 0.006, key, n)
    # wings: two feathered triangles from the shoulders, swept back and up
    for (u1, v1, u2, v2) in ((-0.03, 0.05, 0.0, 0.03), (-0.045, 0.034, -0.015, 0.012)):
        plaka(W, [P(0.026, 0.006), P(u1, v1), P(u2, v2)], 0.004, key, n)
    # the arm and the wreath held out in front
    ax, az = P(0.03, -0.008); bx, bz = P(0.07, -0.02)
    cubuk(y, W(ax, az, 0.005), W(bx, bz, 0.005), 0.005 * s, key, 0.004)
    y.oculus(W(bx, bz, 0.0), V(1, 0), n, 0.009 * s, key, key, f=0.003, k=8)


def heykel(x, yy, z, s=1.0, key=ORN, kol=1):
    """a standing figure (a captive in a cloak, or a driver)"""
    donel(y, (x, yy), [(0.022 * s, z), (0.02 * s, z + 0.06 * s), (0.016 * s, z + 0.1 * s), (0.012 * s, z + 0.112 * s), (0, z + 0.112 * s)], key, n=10)
    kure(y, (x, yy, z + 0.126 * s), 0.012 * s, key, n=8, kat=4)
    cubuk(y, V(x + 0.014 * s * kol, yy, z + 0.1 * s), V(x + 0.02 * s * kol, yy - 0.006 * s, z + 0.055 * s), 0.008 * s, key)
    cubuk(y, V(x - 0.014 * s * kol, yy, z + 0.1 * s), V(x - 0.004 * s * kol, yy - 0.016 * s, z + 0.07 * s), 0.008 * s, key)


# ---------------------------------------------------------------- the square
y.bolum('meydan')
PX, PY = 1.15, 0.92
RD = 0.2                      # half width of the triumphal road (basalt)
kutu(y, V(-PX, -PY, 0), X, 2 * PX, 2 * PY, ZF, 'kirec', 'onarkasagsol')
for x0, x1 in ((-PX, -RD), (RD, PX)):
    y.yuz_yon([V(x0, -PY, ZF), V(x1, -PY, ZF), V(x1, PY, ZF), V(x0, PY, ZF)], 'zemin', Z)
y.yuz_yon([V(-RD, -PY, ZF), V(RD, -PY, ZF), V(RD, PY, ZF), V(-RD, PY, ZF)], 'granit_koyu', Z)
for sx in (-1, 1):   # kerbs along the road
    kutu(y, V(sx * RD - 0.012, -PY, ZF), X, 0.024, 2 * PY, 0.008, 'kirec', 'onarkasagsolust')
silme(y, dikdortgen(-PX, PX, -PY, PY), ZF - 0.006, 0.006, 0.005, 'kirec', 'duz')

# ---------------------------------------------------------------- the arch body with its three passages
y.bolum('govde')
KEM = [(-XA, -0.25, 0.2 / 0.5, HB - 0.38), (-0.25, 0.25, 0.38 / 0.5, HB - 0.58), (0.25, XA, 0.2 / 0.5, HB - 0.38)]
RENK = (BODY, 'kirec', 'kirec', 'koyu')
for x0, x1, en, ust in KEM:
    y.kemerli(V(x0, -DA / 2), V(x1, -DA / 2), ZF, HB, RENK, v0=0.0, en=en, ust=ust, derin=DA, k_say=12)
    y.faces.pop(); y.faces.pop()            # no back plate, no floor: open passages on the road / paving
    parcalar._kemer_yuzu(y, V(x1, DA / 2), V(x0, DA / 2), ZF, HB, en, ust, 0.0, BODY, k_say=12)
for sx in (-1, 1):
    duz_duvar(y, V(sx * XA, -sx * DA / 2), V(sx * XA, sx * DA / 2), ZF, ZB, BODY)
y.yuz_yon([V(-XA, -DA / 2, ZB), V(XA, -DA / 2, ZB), V(XA, DA / 2, ZB), V(-XA, DA / 2, ZB)], BODY, Z)
# the plinth round the piers (not across the passages)
for x0, x1 in ((-XA, -0.6), (-0.4, -0.19), (0.19, 0.4), (0.6, XA)):
    kornis(y, x0, x1, -DA / 2, DA / 2, ZF, 0.03, 0.012, ORN, 'kaide')

# the vault coffers of the central passage (seen from the road) and the side passages' imposts
for x0, x1, en, ust in KEM:
    W = x1 - x0; R = en * W / 2; xc = (x0 + x1) / 2; zs = ZF + HB - ust - R
    for sx in (-1, 1):
        kutu_merkez(y, (xc + sx * (R - 0.004), 0), 0.012, DA + 0.004, 0.014, ORN, z0=zs - 0.014)
    for k in range(1, 6):
        t = math.pi * k / 6
        p = V(xc + (R - 0.0015) * math.cos(t), 0, zs + (R - 0.0015) * math.sin(t))
        nn = V(-math.cos(t), 0, -math.sin(t))
        for yy in (-0.12, 0.0, 0.12):
            c = p + V(0, yy, 0)
            ex = V(-math.sin(t), 0, math.cos(t))
            q = [c + ex * 0.018 + V(0, 0.04, 0), c - ex * 0.018 + V(0, 0.04, 0), c - ex * 0.018 - V(0, 0.04, 0), c + ex * 0.018 - V(0, 0.04, 0)]
            y.yuz_yon(q, 'tas_koyu', nn)


# ---------------------------------------------------------------- one face (sg = -1 front, +1 back)
def cephe(sg):
    yw = sg * DA / 2                  # wall plane
    n = V(0, sg)
    ex = V(-sg, 0)                     # along the wall, left to right as seen from outside

    def W(x, z, d=0.0):
        return V(x, yw + sg * d, z)

    y.bolum('sutunlar %s' % ('on' if sg < 0 else 'arka'))
    yc = yw + sg * COL_Y
    for cx in CX:
        # the pedestal with a relief of a Victory and captives
        zp = ZF + 0.17
        kutu_merkez(y, (cx, yc - sg * 0.01), 0.1, 0.12, 0.022, ORN, z0=ZF)
        kutu_merkez(y, (cx, yc - sg * 0.01), 0.084, 0.104, zp - ZF - 0.04, BODY, z0=ZF + 0.022)
        kornis(y, cx - 0.042, cx + 0.042, yc - sg * 0.01 - 0.052, yc - sg * 0.01 + 0.052, zp - 0.018, 0.018, 0.008, ORN, 'tac')
        py0, py1 = yc - sg * 0.01 - 0.052, yc - sg * 0.01 + 0.052   # the pedestal's top inside its cap moulding
        y.yuz_yon([V(cx - 0.042, py0, zp), V(cx + 0.042, py0, zp), V(cx + 0.042, py1, zp), V(cx - 0.042, py1, zp)], ORN, Z)
        kabartma(W(cx + sg * 0.034, ZF + 0.03, COL_Y + 0.042), ex, n, 0.068, 0.09, nfig=2)
        sutun(y, cx, yc, zp, ZE0, RC, KOLON, 'korint', bas_key=ORN)
        # the entablature break over the column, its cornice and the captive statue
        bx0, bx1 = cx - 0.044, cx + 0.044
        by0, by1 = (yw - (COL_Y + 0.04), yw) if sg < 0 else (yw, yw + COL_Y + 0.04)
        kutu(y, V(bx0, by0, ZE0), X, bx1 - bx0, by1 - by0, 0.04, ORN, 'onarkasagsolust')
        kutu(y, V(bx0 + 0.002, by0 + 0.002, ZE0 + 0.04), X, bx1 - bx0 - 0.004, by1 - by0 - 0.004, 0.035, BODY, 'onarkasagsol')
        kornis(y, bx0, bx1, by0, by1, ZB - 0.025, 0.025, 0.014, ORN, 'tac')
        y.yuz_yon([V(bx0, by0, ZB), V(bx1, by0, ZB), V(bx1, by1, ZB), V(bx0, by1, ZB)], ORN, Z)
        kutu_merkez(y, (cx, yc), 0.06, 0.06, 0.03, BODY, z0=ZB)
        heykel(cx, yc, ZB + 0.03, 1.25, ORN, kol=1 if cx > 0 else -1)

    y.bolum('susler %s' % ('on' if sg < 0 else 'arka'))
    # the main entablature along the face: architrave, frieze, cornice
    a, b = (V(-XA, yw), V(XA, yw)) if sg < 0 else (V(XA, yw), V(-XA, yw))
    silme(y, [a, b], ZE0, 0.035, 0.012, ORN, 'duz', kapali=False)
    silme(y, [a, b], ZE0 + 0.035, 0.04, 0.006, BODY, 'duz', kapali=False)
    silme(y, [a, b], ZB - 0.025, 0.025, 0.024, ORN, 'tac', kapali=False)
    # the frieze band over the side arches and round the piers (Constantine's frieze)
    for x0, x1 in ((-XA, -0.25), (0.25, XA)):
        p, q = (V(x0, yw), V(x1, yw)) if sg < 0 else (V(x1, yw), V(x0, yw))
        kabartma(W(x0 if sg < 0 else x1, ZF + 0.405, 0), ex, n, x1 - x0 - 0.0, 0.05, nfig=9)
    # roundels (tondi) in pairs over the side arches
    for xc in (-0.5, 0.5):
        for dx in (-0.06, 0.06):
            o = W(xc + dx, ZF + 0.52, 0.0)
            y.oculus(o, ex, n, 0.048, 'kirec', ORN, f=0.008, k=16)
            for k in range(3):   # figures in the roundel (a hunt: two figures and the one in the middle taller)
                fx = xc + dx + (k - 1) * 0.024
                hh = 0.042 if k != 1 else 0.05
                z0_ = ZF + 0.52 - 0.032
                plaka(W, [(fx - 0.007, z0_), (fx + 0.007, z0_), (fx + 0.005, z0_ + hh), (fx - 0.005, z0_ + hh)], 0.006, ORN, n)
                plaka(W, [(fx + 0.0055 * math.cos(TAU * q / 8), z0_ + hh + 0.007 + 0.0055 * math.sin(TAU * q / 8)) for q in range(8)],
                      0.006, ORN, n)
    # Victories in the spandrels of the central arch, river gods over the side arches, keystones
    for sx in (-1, 1):
        zafer_tanrica(W, n, sx * 0.215, ZF + 0.55, sx, 1.0)
    for x0, x1, en, ust in KEM:
        xc = (x0 + x1) / 2; zt = ZF + HB - ust
        kutu(y, V(xc - 0.018, yw + (0 if sg > 0 else -0.012), zt - 0.012), X, 0.036, 0.012, 0.05, ORN, 'onarkasagsolust')
    # archivolts round the three arches
    for x0, x1, en, ust in KEM:
        W_ = x1 - x0; R = en * W_ / 2; xc = (x0 + x1) / 2; zs = ZF + HB - ust - R
        f = 0.016
        for k in range(12):
            t0, t1 = math.pi * k / 12, math.pi * (k + 1) / 12
            pts = [V(xc + R * math.cos(t0), yw + sg * 0.003, zs + R * math.sin(t0)), V(xc + R * math.cos(t1), yw + sg * 0.003, zs + R * math.sin(t1)),
                   V(xc + (R + f) * math.cos(t1), yw + sg * 0.003, zs + (R + f) * math.sin(t1)), V(xc + (R + f) * math.cos(t0), yw + sg * 0.003, zs + (R + f) * math.sin(t0))]
            y.yuz_yon(pts, ORN, n)
            y.yuz_yon([pts[3], pts[2], pts[2] - n * 0.003, pts[3] - n * 0.003], ORN, V(math.cos((t0 + t1) / 2), 0, math.sin((t0 + t1) / 2)))
        # impost mouldings on the piers
        for xx in (xc - R - 0.03, xc + R):
            kutu(y, V(xx, yw + (0 if sg > 0 else -0.01), zs - 0.012), X, 0.03, 0.01, 0.012, ORN, 'onarkasagsolust')

    y.bolum('attika %s' % ('on' if sg < 0 else 'arka'))
    ya = yw - sg * 0.012                  # attic face (set back a little)
    # ressauts on the attic behind the statues
    for cx in CX:
        y0_, y1_ = (ya - 0.03, ya) if sg < 0 else (ya, ya + 0.03)
        kutu(y, V(cx - 0.04, y0_, ZB), X, 0.08, y1_ - y0_, ZAT - ZB, BODY, 'onarkasagsolust')
    # the inscription panel
    o = V(-0.26 if sg < 0 else 0.26, ya, ZB + 0.06)
    P = lambda u, v, d: o + ex * u + Z * v + n * d
    fr = 0.02
    for (u0, v0, u1, v1) in ((0, 0, 0.52, fr), (0, 0.2 - fr, 0.52, 0.2), (0, fr, fr, 0.2 - fr), (0.52 - fr, fr, 0.52, 0.2 - fr)):
        y.yuz_yon([P(u0, v0, 0.008), P(u1, v0, 0.008), P(u1, v1, 0.008), P(u0, v1, 0.008)], ORN, n)
    for u_, yon in ((0, -ex), (0.52, ex)):
        y.yuz_yon([P(u_, 0, 0), P(u_, 0.2, 0), P(u_, 0.2, 0.008), P(u_, 0, 0.008)], ORN, yon)
    y.yuz_yon([P(0, 0.2, 0), P(0.52, 0.2, 0), P(0.52, 0.2, 0.008), P(0, 0.2, 0.008)], ORN, Z)
    y.yuz_yon([P(fr, fr, 0.002), P(0.52 - fr, fr, 0.002), P(0.52 - fr, 0.2 - fr, 0.002), P(fr, 0.2 - fr, 0.002)], ORN, n)
    # lines of bronze letters
    for v, satir in ((0.14, 'IMP CAES FL CONSTANTINO'), (0.1, 'MAXIMO P F AVGVSTO'), (0.06, 'S P Q R QVOD INSTINCTV'), (0.025, 'DIVINITATIS ARCVM')):
        yazi(P, satir, 0.26, v, 0.0192, 0.026, n)
    # relief panels between the ressauts
    for x0, x1 in ((-0.66, -0.34), (0.34, 0.66)):
        kabartma(V(x0 if sg < 0 else x1, ya, ZB + 0.05), ex, n, x1 - x0, 0.22, nfig=5)


cephe(-1)
cephe(1)

# the attic as a block, its cornice, the ends of the arch with reliefs and roundels
y.bolum('attika')
duvarlar(y, dikdortgen(-XA, XA, -DA / 2 + 0.012, DA / 2 - 0.012), ZB, ZAT + 0.03, BODY, ust=BODY)   # (top flush with the cornice's top)
kornis(y, -XA, XA, -DA / 2 + 0.012, DA / 2 - 0.012, ZAT - 0.005, 0.035, 0.03, ORN, 'tac')
kornis(y, -XA, XA, -DA / 2 + 0.012, DA / 2 - 0.012, ZB, 0.025, 0.01, ORN, 'kaide')
# the cornice wraps round the ends of the body too
for sx in (-1, 1):
    a, b = (V(sx * XA, -DA / 2), V(sx * XA, DA / 2)) if sx > 0 else (V(sx * XA, DA / 2), V(sx * XA, -DA / 2))
    silme(y, [a, b], ZE0, 0.035, 0.012, ORN, 'duz', kapali=False)
    silme(y, [a, b], ZB - 0.025, 0.025, 0.024, ORN, 'tac', kapali=False)
    exx = (b - a).normalized(); nn = V(sx, 0)
    kabartma(V(a.x, a.y + exx.y * 0.06, ZB + 0.05), exx, nn, DA - 0.12, 0.22, nfig=4)
    y.oculus(V(sx * XA, 0, ZF + 0.42), exx, nn, 0.07, 'tas', ORN, f=0.01, k=18)
    # the tondo of Sol / Luna in a chariot: horses' bodies, the figure and its halo
    M = lambda u, z, d, sx=sx, exx=exx, nn=nn: V(sx * XA, 0, 0) + exx * u + Z * z + nn * d
    zc_ = ZF + 0.42
    for k in range(2):
        u0 = -0.045 + k * 0.012; z0_ = zc_ - 0.022 + k * 0.006
        plaka(M, [(u0, z0_), (u0 + 0.04, z0_ + 0.004), (u0 + 0.042, z0_ + 0.016), (u0 + 0.002, z0_ + 0.014)], 0.006, ORN, nn)
        plaka(M, [(u0 + 0.036, z0_ + 0.012), (u0 + 0.05, z0_ + 0.03), (u0 + 0.044, z0_ + 0.034), (u0 + 0.032, z0_ + 0.018)], 0.006, ORN, nn)
    plaka(M, [(0.012, zc_ - 0.035), (0.038, zc_ - 0.035), (0.036, zc_ - 0.012), (0.014, zc_ - 0.012)], 0.006, ORN, nn)     # chariot
    plaka(M, [(0.018, zc_ - 0.012), (0.03, zc_ - 0.012), (0.028, zc_ + 0.03), (0.02, zc_ + 0.03)], 0.006, ORN, nn)         # figure
    plaka(M, [(0.024 + 0.014 * math.cos(TAU * q / 10), zc_ + 0.04 + 0.014 * math.sin(TAU * q / 10)) for q in range(10)], 0.004, ORN, nn)
    kabartma(V(a.x, a.y + exx.y * 0.08, ZF + 0.1), exx, nn, DA - 0.16, 0.2, nfig=3)

# ---------------------------------------------------------------- the quadriga
y.bolum('quadriga')
ZQ = ZAT + 0.03
kutu_merkez(y, (0, 0), 0.56, 0.3, 0.05, ORN, z0=ZQ)
kornis(y, -0.28, 0.28, -0.15, 0.15, ZQ + 0.035, 0.015, 0.01, ORN, 'tac')
zq = 0.0
QS = 1.3   # the group is built at the origin and scaled up onto its base
Q = 'bronz'


def at(x, yy, z, s=1.0, adim=0.0):
    """a horse facing -y, rearing a little: round body, tapering neck and head, mane, legs (one foreleg raised), tail"""
    P = lambda dy, dz: V(x, yy + dy * s, z + dz * s)
    boru(y, [P(0.05, 0.078), P(0.0, 0.082), P(-0.048, 0.088)], 0.021 * s, Q, n=10)
    kure(y, (x, yy + 0.05 * s, z + 0.078 * s), 0.021 * s, Q, n=10, kat=5)
    kure(y, (x, yy - 0.048 * s, z + 0.088 * s), 0.022 * s, Q, n=10, kat=5)
    boru(y, [P(-0.055, 0.1), P(-0.075, 0.13), P(-0.085, 0.15)], 0.014 * s, Q, n=8, r_son=0.01 * s)
    boru(y, [P(-0.083, 0.155), P(-0.1, 0.142), P(-0.115, 0.125)], 0.011 * s, Q, n=8, r_son=0.007 * s)
    cubuk(y, P(-0.05, 0.112), P(-0.08, 0.162), 0.006 * s, Q, 0.012 * s)          # mane
    for dx in (-0.006, 0.006):                                                    # ears
        boru(y, [V(x + dx * s, yy - 0.085 * s, z + 0.16 * s), V(x + dx * s, yy - 0.08 * s, z + 0.178 * s)], 0.003 * s, Q, n=4, r_son=0.001 * s)
    for (dy, kalk) in ((-0.04, adim), (0.04, 0.0)):
        for dx in (-0.011, 0.011):
            top = V(x + dx * s, yy + dy * s, z + 0.07 * s)
            if kalk and dx < 0:
                diz = top + V(0, -0.028 * s, -0.018 * s)
                boru(y, [top, diz, diz + V(0, 0.012 * s, -0.026 * s)], 0.006 * s, Q, n=5)
            else:
                diz = V(x + dx * s, yy + (dy + (0.006 if dy > 0 else -0.004)) * s, z + 0.035 * s)
                boru(y, [top, diz, V(x + dx * s, yy + dy * s, z)], 0.006 * s, Q, n=5, r_son=0.005 * s)
    boru(y, [P(0.068, 0.085), P(0.085, 0.07), P(0.092, 0.035)], 0.007 * s, Q, n=5, r_son=0.004 * s)


_q = parca(y, (0, 0, ZQ + 0.05), 0.0, QS); _q.__enter__()
for i, xx in enumerate((-0.135, -0.045, 0.045, 0.135)):
    at(xx, -0.04, zq, 1.0, adim=1.0 if i in (0, 3) else 0.0)
# the chariot and the driver
kutu_merkez(y, (0, 0.085), 0.12, 0.06, 0.05, Q, z0=zq + 0.03)
for sx in (-1, 1):
    c = V(sx * 0.066, 0.095, zq + 0.04)
    boru(y, [c - V(0.004 * sx, 0, 0), c + V(0.004 * sx, 0, 0)], 0.04, Q, n=12)
heykel(0, 0.08, zq + 0.08, 0.85, Q, kol=1)
_q.__exit__(None, None, None)
sancak(y, 0.04, 0.14, ZQ + 0.05 + 0.15, boy=0.2, en=0.13, yuk=0.08, aci=math.radians(190))
# trophies of arms on the attic corners
for sx in (-1, 1):
    for sy in (-1, 1):
        tx, ty = sx * (XA - 0.07), sy * (DA / 2 - 0.07)
        kutu_merkez(y, (tx, ty), 0.06, 0.06, 0.03, ORN, z0=ZAT + 0.03)
        zt_ = ZAT + 0.06
        y.prizma((tx, ty), 0.005, zt_, zt_ + 0.12, Q, n=6)
        donel(y, (tx, ty), [(0.0, zt_ + 0.03), (0.02, zt_ + 0.035), (0.022, zt_ + 0.07), (0.018, zt_ + 0.085), (0.0, zt_ + 0.087)], Q, n=10)
        kure(y, (tx, ty, zt_ + 0.1), 0.013, Q, n=8, kat=4)
        cubuk(y, V(tx - 0.035, ty, zt_ + 0.075), V(tx + 0.035, ty, zt_ + 0.075), 0.006, Q)
        boru(y, [V(tx + 0.03 * sx, ty - 0.004, zt_ + 0.03), V(tx + 0.03 * sx, ty + 0.004, zt_ + 0.03)], 0.022, Q, n=10)

# ---------------------------------------------------------------- the Meta Sudans, the colossus, pines
y.bolum('cevre')
# Meta Sudans: a conical fountain in a round basin
mx, my = 0.78, -0.58
donel(y, (mx, my), [(0.17, ZF), (0.17, ZF + 0.03), (0.155, ZF + 0.03), (0.155, ZF + 0.012)], ORN, n=32)
y.yuz_yon([V(mx + 0.155 * math.cos(TAU * i / 32), my + 0.155 * math.sin(TAU * i / 32), ZF + 0.012) for i in range(32)], 'su', Z)
donel(y, (mx, my), [(0.07, ZF + 0.012), (0.07, ZF + 0.07), (0.06, ZF + 0.08), (0.05, ZF + 0.2), (0.03, ZF + 0.33), (0.022, ZF + 0.34), (0.0, ZF + 0.37)], 'kirec', n=16)
for k in range(8):   # niches round its drum
    a = TAU * k / 8
    y.pencere(V(mx + 0.0705 * math.cos(a), my + 0.0705 * math.sin(a), ZF + 0.02), V(-math.sin(a), math.cos(a)), V(math.cos(a), math.sin(a)), -0.012, 0, 0.024, 0.04, 'tas_koyu', kemer=True)
kure(y, (mx, my, ZF + 0.38), 0.016, 'bronz', n=10, kat=5)
# the colossus of Sol on its base
cx_, cy_ = -0.82, 0.56
kutu_merkez(y, (cx_, cy_), 0.2, 0.2, 0.03, 'kirec', z0=ZF)
kutu_merkez(y, (cx_, cy_), 0.16, 0.16, 0.12, BODY, z0=ZF + 0.03)
kornis(y, cx_ - 0.08, cx_ + 0.08, cy_ - 0.08, cy_ + 0.08, ZF + 0.13, 0.02, 0.012, ORN, 'tac')
heykel(cx_, cy_, ZF + 0.15, 2.6, 'bronz', kol=-1)
for k in range(7):   # the radiate crown
    a = math.pi * (0.15 + 0.7 * k / 6)
    p = V(cx_, cy_, ZF + 0.15 + 0.126 * 2.6)
    cubuk(y, p + V(0.022 * math.cos(a), 0, 0.022 * math.sin(a)), p + V(0.06 * math.cos(a), 0, 0.06 * math.sin(a)), 0.006, 'altin', 0.004)


def cam(x, yy, boy=0.32):
    """an umbrella pine"""
    boru(y, [V(x, yy, ZF), V(x + 0.012, yy, ZF + boy * 0.45), V(x + 0.03, yy + 0.01, ZF + boy * 0.8)], 0.014, 'ahsap', n=6, r_son=0.008)
    tepe = V(x + 0.03, yy + 0.01)
    for (dx, dy, r, dz) in ((0, 0, 0.1, 0.0), (0.07, 0.03, 0.065, -0.025), (-0.06, 0.04, 0.06, -0.02), (0.02, -0.07, 0.065, -0.015), (-0.03, -0.04, 0.05, 0.02)):
        c = (tepe.x + dx, tepe.y + dy); z0 = ZF + boy * 0.8 + dz
        donel(y, c, [(0.0, z0), (r * 0.85, z0 + 0.008), (r, z0 + 0.03), (r * 0.8, z0 + 0.052), (r * 0.35, z0 + 0.062), (0.0, z0 + 0.064)], 'boya_yesil', n=12)
    for a in (0.6, 2.4, 4.2):   # branches
        cubuk(y, V(tepe.x, tepe.y, ZF + boy * 0.78), V(tepe.x + 0.05 * math.cos(a), tepe.y + 0.05 * math.sin(a), ZF + boy * 0.81), 0.006, 'ahsap')


for (x, yy, b) in ((-0.95, -0.7, 0.36), (0.98, 0.62, 0.34), (-0.98, 0.05, 0.3), (0.55, 0.75, 0.28)):
    cam(x, yy, b)
for (x, yy) in ((-0.55, -0.72), (-0.35, 0.72), (0.98, -0.12)):
    kutu_merkez(y, (x, yy), 0.05, 0.05, 0.06, 'kirec', z0=ZF)
    kornis(y, x - 0.025, x + 0.025, yy - 0.025, yy + 0.025, ZF + 0.05, 0.01, 0.006, ORN, 'tac')
    heykel(x, yy, ZF + 0.06, 0.8, 'bronz', kol=1)

calistir(y, 'lm_zafertaki')
