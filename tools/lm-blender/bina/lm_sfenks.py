# Büyük Sfenks (lm_sfenks): the Great Sphinx of Giza crouching in its rock-cut enclosure, built from lofted sections:
# the lion body with its masonry-cased flanks, folded haunches, long forepaws with the Dream Stela between them, the
# striped nemes, the worn face (broken nose, the beard's stub, the uraeus); before it the Sphinx Temple and Khafre's
# Valley Temple (granite pillar courts with seated colossi), the causeway climbing to Khafre's pyramid (stepped core,
# casing cap) and its mortuary temple, queens' pyramids and mastabas on the sand.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.05
GOV = 'kum'          # the sphinx's rock
KAS = 'kirec'        # limestone casing blocks
SX0 = 0.23           # the sphinx's axis (x)


# ---------------------------------------------------------------- lofting
# a half cross-section (x 0..1 of the half width, z 0..1 of the height) from the bottom centre round to the top centre
YUVARLAK = [(0, 0), (1, 0), (1, 0.18), (0.99, 0.34), (0.96, 0.5), (0.9, 0.64), (0.8, 0.77), (0.66, 0.88), (0.48, 0.95), (0.26, 0.99), (0, 1)]
BACAK = [(0, 0), (1, 0), (1, 0.4), (0.95, 0.66), (0.82, 0.85), (0.6, 0.97), (0.3, 1.0), (0, 1.0)]


def _cr(p0, p1, p2, p3, t):
    return tuple(0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (-a + 3 * b - 3 * c + d) * t ** 3) for a, b, c, d in zip(p0, p1, p2, p3))


def yumusat(L, k=2):
    """Catmull-Rom: k - 1 points between each pair (sections or profile points), the ends kept"""
    if len(L) < 3: return L
    out = []
    for i in range(len(L) - 1):
        p0, p1, p2, p3 = L[max(i - 1, 0)], L[i], L[i + 1], L[min(i + 2, len(L) - 1)]
        for j in range(k):
            out.append(_cr(p0, p1, p2, p3, j / k))
    out.append(tuple(L[-1]))
    return out


def loft(kesitler, profil, key, cx=0.0, kap=(True, True), satir_key=None, ince=2):
    """a body lofted through sections [(t, w, h, zb), ...] along y at x = cx, each section the profile scaled to
    w x h from zb (the sections smoothed: ince - 1 more between each pair); satir_key(j, key): the key of the j-th
    profile row (stripes, casing bands)"""
    kesitler = yumusat(kesitler, ince) if ince > 1 else kesitler
    m = len(profil)
    def ring(t, w, h, zb):
        sag = [(cx + fx * w / 2, t, zb + fz * h) for fx, fz in profil]
        sol = [(cx - fx * w / 2, t, zb + fz * h) for fx, fz in reversed(profil[1:-1])]
        return [V(*p) for p in sag + sol]
    R = [ring(*k) for k in kesitler]
    nr = len(R[0])
    for k in range(len(R) - 1):
        t0, w0, h0, z0 = kesitler[k]; t1, w1, h1, z1 = kesitler[k + 1]
        for i in range(nr):
            j = (i + 1) % nr
            q = [R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]]
            row = i if i < m - 1 else nr - i - 1
            kk = satir_key(row, key) if satir_key else key
            # outward: away from the section's centre line, in the plane of the section
            c = sum(q, Vector()) / 4
            zc = (z0 + h0 * 0.45 + z1 + h1 * 0.45) / 2
            out = V(c.x - cx, 0, c.z - zc)
            y.yuz_yon(q, kk, out)
    if kap[0]: y.yuz_yon(R[0], key, -Y if kesitler[1][0] > kesitler[0][0] else Y)
    if kap[1]: y.yuz_yon(R[-1], key, Y if kesitler[-1][0] > kesitler[-2][0] else -Y)
    return R


def kasli(j, key):     # the lower flanks: limestone casing blocks; above: the weathered rock
    return KAS if j <= 1 else key


def levha_y(x0, x1, z0, z1, yy, key, yon=-1):
    """a flat painted / carved panel on a plane y = yy facing yon (-1: -y)"""
    x0, x1 = min(x0, x1), max(x0, x1)
    y.yuz_yon([V(x0, yy, z0), V(x1, yy, z0), V(x1, yy, z1), V(x0, yy, z1)], key, V(0, yon, 0))


# ---------------------------------------------------------------- the sphinx (built facing -y at the origin)
def sfenks(tam=True):
    zs = 0.0
    # lion body, chest to rump
    govde = [(-0.2, 0.33, 0.33, zs), (-0.12, 0.355, 0.345, zs), (-0.02, 0.36, 0.34, zs), (0.08, 0.35, 0.325, zs), (0.17, 0.335, 0.305, zs),
             (0.26, 0.315, 0.29, zs), (0.35, 0.32, 0.285, zs), (0.45, 0.33, 0.28, zs), (0.56, 0.33, 0.275, zs), (0.64, 0.31, 0.255, zs),
             (0.7, 0.26, 0.21, zs), (0.745, 0.17, 0.14, zs)]
    # the flanks: restored casing courses below, then the weathered strata of the rock (deep horizontal grooves)
    GOVDE = [(0, 0), (1, 0), (1, 0.12), (0.985, 0.15), (1, 0.2), (1, 0.3), (0.975, 0.34), (0.995, 0.4), (0.99, 0.5), (0.965, 0.54),
             (0.975, 0.6), (0.93, 0.7), (0.84, 0.8), (0.7, 0.89), (0.5, 0.96), (0.26, 0.995), (0, 1)]
    def katman(j, key):
        if j <= 3: return KAS
        return 'kum_koyu' if j in (5, 8) else key
    loft(govde, GOVDE, GOV, satir_key=katman)
    # the chest, rising to the neck
    loft([(-0.31, 0.22, 0.3, zs), (-0.285, 0.29, 0.34, zs), (-0.24, 0.33, 0.37, zs), (-0.17, 0.34, 0.37, zs)], YUVARLAK, GOV, kap=(True, False), satir_key=kasli)
    for sx in (-1, 1):
        cx = sx * 0.105
        # forelegs and paws, claws
        loft([(-0.785, 0.085, 0.045, zs), (-0.765, 0.11, 0.07, zs), (-0.72, 0.118, 0.08, zs), (-0.6, 0.115, 0.083, zs), (-0.45, 0.113, 0.09, zs),
              (-0.32, 0.12, 0.12, zs), (-0.22, 0.13, 0.16, zs), (-0.12, 0.13, 0.18, zs)], BACAK, GOV, cx=cx, satir_key=kasli)
        for k in (-1.5, -0.5, 0.5, 1.5):
            xx = cx + k * 0.025
            y.yuz_yon([V(xx - 0.003, -0.776, zs + 0.054), V(xx + 0.003, -0.776, zs + 0.054), V(xx + 0.003, -0.73, zs + 0.081), V(xx - 0.003, -0.73, zs + 0.081)],
                      'kum_koyu', V(0, -0.5, 1))
            kutu_merkez(y, (xx, -0.79), 0.012, 0.012, 0.022, 'kum_acik', z0=zs)
        # hind legs folded along the flanks, the thigh swelling over the haunch, the hind paw before it
        hx = sx * 0.168
        loft([(0.16, 0.05, 0.04, zs), (0.22, 0.07, 0.06, zs), (0.34, 0.09, 0.1, zs), (0.46, 0.1, 0.13, zs), (0.56, 0.1, 0.14, zs),
              (0.64, 0.088, 0.12, zs), (0.7, 0.05, 0.065, zs)], YUVARLAK, GOV, cx=hx, satir_key=kasli)
        loft([(0.07, 0.05, 0.03, zs), (0.09, 0.07, 0.042, zs), (0.2, 0.072, 0.045, zs)], BACAK, GOV, cx=sx * 0.228, kap=(True, False), satir_key=kasli)
    # the tail curled up over the right haunch
    boru(y, [V(0.05, 0.755, zs + 0.05), V(0.15, 0.735, zs + 0.025), V(0.22, 0.66, zs + 0.018), V(0.245, 0.5, zs + 0.025), V(0.238, 0.39, zs + 0.05), V(0.222, 0.335, zs + 0.075)],
         0.016, GOV, n=8, r_son=0.012)
    kure(y, (0.222, 0.33, zs + 0.08), 0.016, GOV, n=8, kat=4)
    # the spine ridge
    boru(y, [V(0, -0.1, zs + 0.352), V(0, 0.08, zs + 0.338), V(0, 0.26, zs + 0.293), V(0, 0.45, zs + 0.302), V(0, 0.62, zs + 0.283)], 0.012, GOV, n=6)

    # nemes headcloth: striped rows, its pleated tail down the neck
    NEMES = [(0, 0), (1, 0), (0.98, 0.16), (0.96, 0.3), (0.93, 0.44), (0.88, 0.56), (0.8, 0.68), (0.7, 0.78), (0.57, 0.87), (0.4, 0.94), (0.2, 0.99), (0, 1.0)]
    serit = lambda j, key: ('kum_koyu' if j % 2 else key)
    loft([(-0.27, 0.23, 0.2, zs + 0.34), (-0.25, 0.25, 0.215, zs + 0.335), (-0.2, 0.26, 0.225, zs + 0.33), (-0.14, 0.25, 0.21, zs + 0.33),
          (-0.08, 0.2, 0.16, zs + 0.33), (-0.03, 0.11, 0.085, zs + 0.33)], NEMES, GOV, satir_key=serit)
    loft([(-0.05, 0.08, 0.07, zs + 0.3), (0.02, 0.07, 0.05, zs + 0.3), (0.08, 0.05, 0.03, zs + 0.31)], YUVARLAK, GOV, kap=(False, True),
         satir_key=lambda j, key: 'kum_koyu' if j % 2 else key)
    # the face: a carved height field in front of the headcloth's cap (y = -0.27): forehead under the headband,
    # the brow ridge, deep-set almond eyes, broad cheekbones, the broken nose's stump, full lips, a rounded chin
    YB = -0.271
    FX, FZ0, FZ1 = 0.066, zs + 0.345, zs + 0.522
    def fd(u, v):
        g = lambda a, b, sa, sb: math.exp(-((u - a) / sa) ** 2 - ((v - b) / sb) ** 2)
        cu = max(0.0, 1 - abs(u) ** 2.3 * 0.93) ** 0.5
        d = 0.027 * cu
        if v < 0.16: d *= 0.5 + 0.5 * (v / 0.16) ** 0.7                       # the jaw and chin recede below
        d += 0.0045 * g(0, 0.73, 0.75, 0.05) * cu                              # brow ridge
        d -= 0.0035 * g(0, 0.88, 0.9, 0.1)                                     # the forehead sloping back
        for sx in (-1, 1):
            d -= 0.0085 * g(sx * 0.4, 0.635, 0.2, 0.062)                       # eye sockets
            d += 0.0055 * g(sx * 0.4, 0.628, 0.12, 0.032)                      # the eyeball, lids
            d += 0.0035 * g(sx * 0.6, 0.47, 0.18, 0.1)                         # cheekbones
            d -= 0.002 * g(sx * 0.27, 0.36, 0.08, 0.07)                        # beside the nostrils
        nose = 0.016 * math.exp(-(u / 0.13) ** 2) * (1 if 0.4 < v < 0.7 else math.exp(-((v - (0.4 if v <= 0.4 else 0.7)) / 0.05) ** 2))
        d += min(nose, 0.011)                                                  # the nose (its tip broken off: flat)
        d += 0.0055 * g(0, 0.305, 0.36, 0.035) - 0.0045 * g(0, 0.262, 0.42, 0.014) + 0.0045 * g(0, 0.225, 0.3, 0.03)   # lips
        d += 0.004 * g(0, 0.08, 0.3, 0.06)                                     # chin
        return d
    def fkey(u, v):
        if abs(v - 0.262) < 0.018 and abs(u) < 0.38: return 'kum_koyu'          # the mouth's line
        if tam and abs(v - 0.656) < 0.021 and abs(abs(u) - 0.42) < 0.13: return 'kum_koyu'   # the upper lids
        if tam and abs(v - 0.604) < 0.021 and abs(abs(u) - 0.4) < 0.07: return 'kum_koyu'    # the lower lids
        if 0.4 < v < 0.7 and abs(u) < 0.07 and tam: return 'kum_acik'           # the broken nose's fresh stone
        return GOV
    NU, NV = (18, 24) if tam else (8, 10)
    fw = lambda v: FX * (0.66 + 0.34 * min(1.0, v / 0.4) ** 0.7)          # the jaw narrows to the chin
    FP = [[V(fw(j / NV) * (-1 + 2 * i / NU), YB - fd(-1 + 2 * i / NU, j / NV), FZ0 + (FZ1 - FZ0) * j / NV) for i in range(NU + 1)] for j in range(NV + 1)]
    for j in range(NV):
        for i in range(NU):
            uc, vc = -1 + 2 * (i + 0.5) / NU, (j + 0.5) / NV
            y.yuz_yon([FP[j][i], FP[j][i + 1], FP[j + 1][i + 1], FP[j + 1][i]], fkey(uc, vc), -Y)
    for i in range(NU):     # the underside of the chin, back to the cap
        a, b = FP[0][i], FP[0][i + 1]
        y.yuz_yon([a, b, V(b.x, YB + 0.004, b.z), V(a.x, YB + 0.004, a.z)], GOV, -Z)
    # the headband over the brow with the uraeus rearing at its centre
    kutu(y, V(-0.082, -0.306, FZ1 - 0.006), X, 0.164, 0.04, 0.024, GOV)
    kutu(y, V(-0.082, -0.3085, FZ1 + 0.002), X, 0.164, 0.004, 0.006, 'kum_koyu', 'onust')
    if tam:
        boru(y, [V(0, -0.307, FZ1 - 0.002), V(0, -0.318, FZ1 + 0.012), V(0, -0.312, FZ1 + 0.03), V(0, -0.3, FZ1 + 0.036)], 0.0065, GOV, n=6, r_son=0.004)
        kure(y, (0, -0.302, FZ1 + 0.036), 0.007, GOV, n=6, kat=3)
    # the nemes' wings flaring beside the face and its lappets falling over the chest: raised and sunk stripes
    OZ = [zs + 0.2, zs + 0.33, zs + 0.345, zs + 0.38, zs + 0.42, zs + 0.46, zs + 0.5, zs + 0.538]
    OI = [0.068, 0.068, 0.061, 0.057, 0.06, 0.06, 0.058, 0.06]
    OO = [0.114, 0.118, 0.122, 0.134, 0.139, 0.132, 0.112, 0.082]
    def ana(z, L):
        for k in range(len(OZ) - 1):
            if z <= OZ[k + 1] + 1e-9:
                t = (z - OZ[k]) / (OZ[k + 1] - OZ[k]); return L[k] + (L[k + 1] - L[k]) * t
        return L[-1]
    NB = 28 if tam else 10
    zb = [OZ[0] + (OZ[-1] - OZ[0]) * k / NB for k in range(NB + 1)]
    YK = -0.248
    def on_y(k):
        zc = (zb[k] + zb[k + 1]) / 2
        base = -0.326 if zc < zs + 0.345 else -0.302
        return base - (0.0028 if k % 2 == 0 else 0.0)
    for sx in (-1, 1):
        for k in range(NB):
            z0_, z1_ = zb[k], zb[k + 1]
            fy_ = on_y(k)
            key = 'kum_koyu' if k % 2 else GOV
            i0, i1, o0, o1 = sx * ana(z0_, OI), sx * ana(z1_, OI), sx * ana(z0_, OO), sx * ana(z1_, OO)
            F = [V(i0, fy_, z0_), V(o0, fy_, z0_), V(o1, fy_, z1_), V(i1, fy_, z1_)]
            y.yuz_yon(F, key, -Y)
            y.yuz_yon([V(o0, fy_, z0_), V(o0, YK, z0_), V(o1, YK, z1_), V(o1, fy_, z1_)], key, V(sx, 0, 0))
            y.yuz_yon([V(i0, fy_, z0_), V(i0, YK, z0_), V(i1, YK, z1_), V(i1, fy_, z1_)], key, V(-sx, 0, 0))
            y.yuz_yon([V(i0, YK, z0_), V(o0, YK, z0_), V(o1, YK, z1_), V(i1, YK, z1_)], key, Y)
            if k + 1 < NB:   # the step to the next stripe
                fn = on_y(k + 1)
                if abs(fn - fy_) > 1e-6:
                    y.yuz_yon([V(i1, fy_, z1_), V(o1, fy_, z1_), V(o1, fn, z1_), V(i1, fn, z1_)], key, Z if fn > fy_ else -Z)
        y.yuz_yon([V(sx * ana(zb[0], OI), on_y(0), zb[0]), V(sx * ana(zb[0], OO), on_y(0), zb[0]), V(sx * ana(zb[0], OO), YK, zb[0]), V(sx * ana(zb[0], OI), YK, zb[0])], GOV, -Z)
        y.yuz_yon([V(sx * ana(zb[-1], OI), on_y(NB - 1), zb[-1]), V(sx * ana(zb[-1], OO), on_y(NB - 1), zb[-1]), V(sx * ana(zb[-1], OO), YK, zb[-1]), V(sx * ana(zb[-1], OI), YK, zb[-1])], GOV, Z)
        # the ears, in front of the wings
        kutu_merkez(y, (sx * 0.0715, -0.309), 0.011, 0.014, 0.046, GOV, z0=zs + 0.418)
        if tam:
            levha_y(sx * 0.0685, sx * 0.0745, zs + 0.426, zs + 0.456, -0.3182, 'kum_koyu')
    # the beard's stub under the chin, on the chest
    kutu_merkez(y, (0, -0.302), 0.022, 0.016, 0.03, GOV, z0=zs + 0.315)


# ---------------------------------------------------------------- ground and the rock-cut enclosure
y.bolum('Zemin')
XW, YF, YB = 1.2, -1.2, 1.2
zemin(y, -XW, XW, YF, YB, Z0, 'kum_koyu', 'kum_acik', basamak=(('on', 0.6),), n_basamak=3)

y.bolum('Kaya cukuru')
# the bedrock banks round the sphinx on three sides (it was carved out of the plateau): a quarried face in strata
# towards the pit, a rough top, a talus of sand outside
KESIT = [(0, 0), (0, 0.36), (0.016, 0.36), (0.016, 0.7), (0.032, 0.7), (0.032, 1.0), (0.075, 1.0), (0.18, 0.0)]
KESIT_KEY = ['kum_koyu', 'kum', 'kum_koyu', 'kum', 'kum_koyu', 'kum', 'kum_acik']
def kaya_set(yol, yuk):
    """the bank along the open polyline yol (the pit on its right), node heights yuk"""
    D = {}
    for s, _ in KESIT:
        if s not in D: D[s] = disa(yol, -s, kapali=False)
    P = lambda i, k: D[KESIT[k][0]][i] + Z * (Z0 + KESIT[k][1] * yuk[i])
    for i in range(len(yol) - 1):
        e = (yol[i + 1] - yol[i]).normalized(); u = V(-e.y, e.x)      # u: away from the pit
        for k in range(len(KESIT) - 1):
            ds, dz = KESIT[k + 1][0] - KESIT[k][0], KESIT[k + 1][1] - KESIT[k][1]
            ref = u * (-dz) + Z * (ds * 6)
            y.yuz_yon([P(i, k), P(i + 1, k), P(i + 1, k + 1), P(i, k + 1)], KESIT_KEY[k], ref)
    # end caps (fans from the talus foot)
    for i, yon in ((0, -1), (len(yol) - 1, 1)):
        e = (yol[min(i + 1, len(yol) - 1)] - yol[max(i - 1, 0)]).normalized() * yon
        for k in range(len(KESIT) - 2):
            y.yuz_yon([P(i, len(KESIT) - 1), P(i, k), P(i, k + 1)], 'kum_koyu', e)
SX, SY0, SY1 = 0.36, -0.46, 0.88
yol = []
for k in range(5): yol.append(V(SX0 - SX, SY0 + (SY1 - SY0) * k / 4))
for k in range(1, 5): yol.append(V(SX0 - SX + 2 * SX * k / 4, SY1))
for k in range(1, 5): yol.append(V(SX0 + SX, SY1 - (SY1 - SY0) * k / 4))
yuk = [0.04, 0.1, 0.13, 0.12, 0.15, 0.14, 0.16, 0.15, 0.14, 0.13, 0.14, 0.11, 0.04]
kaya_set(yol, yuk)
# fallen blocks in the pit
for (bx, by, a) in ((SX0 - 0.31, 0.62, 0.3), (SX0 + 0.29, 0.1, -0.4), (SX0 - 0.3, -0.2, 0.9)):
    kutu_merkez(y, (bx, by), 0.05, 0.032, 0.028, 'kum', z0=Z0, aci=a)

y.bolum('Sfenks')
with parca(y, (SX0, 0.02, Z0)):
    sfenks()

# ---------------------------------------------------------------- between the paws: the Dream Stela and an altar
y.bolum('Ruya steli')
with parca(y, (SX0, 0.02, Z0)):
    kutu_merkez(y, (0, -0.245), 0.1, 0.02, 0.15, 'granit_kizil', z0=0)
    for k in range(9):   # the rounded top
        a0, a1 = math.pi * k / 9, math.pi * (k + 1) / 9
        y.yuz_yon([V(0, -0.255, 0.15), V(0.05 * math.cos(a0), -0.255, 0.15 + 0.03 * math.sin(a0)), V(0.05 * math.cos(a1), -0.255, 0.15 + 0.03 * math.sin(a1))], 'granit_kizil', -Y)
        y.yuz_yon([V(0.05 * math.cos(a0), -0.255, 0.15 + 0.03 * math.sin(a0)), V(0.05 * math.cos(a1), -0.255, 0.15 + 0.03 * math.sin(a1)),
                   V(0.05 * math.cos(a1), -0.235, 0.15 + 0.03 * math.sin(a1)), V(0.05 * math.cos(a0), -0.235, 0.15 + 0.03 * math.sin(a0))], 'granit_kizil',
                  V(math.cos((a0 + a1) / 2), 0, math.sin((a0 + a1) / 2)))
    kanat = lambda s: levha_y(s * 0.006, s * 0.042, 0.148, 0.156, -0.2565, 'granit_kizil_koyu')
    kanat(-1); kanat(1)
    kure(y, (0, -0.256, 0.152), 0.006, 'altin', n=6, kat=3)
    for sx in (-1, 1):   # the two sphinx figures of the lunette, offering scene
        levha_y(sx * 0.012, sx * 0.04, 0.105, 0.135, -0.2565, 'granit_kizil_koyu')
    for k in range(5):
        levha_y(-0.042, 0.042, 0.02 + k * 0.017, 0.027 + k * 0.017, -0.2565, 'granit_kizil_koyu')
    # an altar and offerings on the paved way between the paws
    kutu_merkez(y, (0, -0.58), 0.08, 0.05, 0.035, 'kirec', z0=0)
    kutu_merkez(y, (0, -0.58), 0.09, 0.06, 0.008, 'kirec', z0=0.035)
    for dx in (-0.022, 0.0, 0.022):
        donel(y, (dx, -0.58), [(0.006, 0.043), (0.009, 0.05), (0.006, 0.058), (0, 0.058)], 'kirmizi', n=6)
    y.yuz([V(-0.045, -0.8, 0.001), V(0.045, -0.8, 0.001), V(0.045, -0.27, 0.001), V(-0.045, -0.27, 0.001)], 'zemin')


# ---------------------------------------------------------------- temples
def oturan_heykel(x, yy, aci, s=1.0):
    """a seated king in nemes (Khafre's diorite statues), built facing +x"""
    with parca(y, (x, yy, Z0), aci, s):
        kutu_merkez(y, (0.0, 0), 0.05, 0.034, 0.02, 'granit_kizil_koyu', z0=0)                 # base
        kutu_merkez(y, (-0.008, 0), 0.03, 0.03, 0.03, 'bazalt', z0=0.02)                  # throne
        kutu_merkez(y, (0.012, 0), 0.026, 0.024, 0.012, 'bazalt', z0=0.035)               # thighs
        kutu_merkez(y, (0.022, 0), 0.008, 0.022, 0.035, 'bazalt', z0=0.02)                # shins
        kutu_merkez(y, (-0.008, 0), 0.016, 0.026, 0.032, 'bazalt', z0=0.047)              # torso
        kutu_merkez(y, (-0.008, 0), 0.02, 0.026, 0.012, 'bazalt', z0=0.079)               # nemes
        kutu_merkez(y, (-0.004, 0), 0.016, 0.016, 0.01, 'bazalt', z0=0.086)               # head
        kutu_merkez(y, (-0.018, 0), 0.006, 0.03, 0.06, 'bazalt', z0=0.05)                 # throne back


def tapinak(cx, cy, w, d, h, nx, ny, kapilar=(0.5,), heykel=True):
    """a Khafre-style temple: massive battered walls (red granite casing below, limestone above, a torus and a plain
    coping), projecting granite door frames, a flat roof with slab joints and a parapet round an open court whose
    ambulatory stands on square monolithic granite pillars carrying architraves; seated colossi before the pillars"""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2
    bt = 0.012                                           # batter
    B = dikdortgen(x0, x1, y0, y1, Z0); T = dikdortgen(x0 + bt, x1 - bt, y0 + bt, y1 - bt, Z0 + h)
    zr = Z0 + h
    for i in range(4):
        j = (i + 1) % 4
        e = B[j] - B[i]; nn = V(e.y, -e.x).normalized() + Z * (bt / h)
        M0, M1 = B[i].lerp(T[i], 0.62), B[j].lerp(T[j], 0.62)
        y.yuz_yon([B[i], B[j], M1, M0], 'granit_kizil', nn)
        y.yuz_yon([M0, M1, T[j], T[i]], 'kirec', nn)
    silme(y, [p.lerp(q, 0.62) for p, q in zip(B, T)], Z0 + h * 0.62 - 0.004, 0.008, 0.005, 'granit_kizil_koyu', 'yarim')
    silme(y, T, zr - 0.012, 0.012, 0.006, 'kirec', 'yarim')
    # roof ring round the court, parapet, slab joints
    t = 0.12
    ix0, ix1, iy0, iy1 = x0 + t, x1 - t, y0 + t, y1 - t
    ki = dikdortgen(ix0, ix1, iy0, iy1)
    parapet(y, T, zr, 0.018, 0, 0.014, 'kirec')
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([T[i] + Z * 0.0, T[j], ki[j] + Z * zr, ki[i] + Z * zr], 'kirec', Z)
    for i in range(4):
        a, b = T[i], T[(i + 1) % 4]
        L = (b - a).length; e = (b - a) / L; nin = V(-e.y, e.x)
        p_, q_ = ki[i], ki[(i + 1) % 4]
        dep = (p_ - V(a.x, a.y, p_.z)).dot(nin)
        n_ = max(2, int(L / 0.06))
        for m in range(1, n_):
            p = a.lerp(b, m / n_)
            u = (p - V(p_.x, p_.y, p.z)).dot(e) / (q_ - p_).length
            if not (0.02 < u < 0.98): continue
            cubuk(y, p + Z * 0.0012, V(p.x, p.y, zr) + nin * dep + Z * 0.0012, 0.004, 'kum_koyu', 0.0024)
    # the court: architraves on the pillars, the dark ambulatory behind
    za = zr - 0.028
    for i in range(4):
        a, b = ki[(i + 1) % 4], ki[i]
        duz_duvar(y, a, b, za, zr, 'granit_kizil')
    kb = disa(ki, 0.07)
    for i in range(4):
        a, b = kb[(i + 1) % 4], kb[i]
        duz_duvar(y, a, b, Z0, za, 'granit_kizil_koyu')
        y.yuz_yon([ki[i] + Z * za, ki[(i + 1) % 4] + Z * za, kb[(i + 1) % 4] + Z * za, kb[i] + Z * za], 'granit_kizil_koyu', -Z)
        y.yuz_yon([ki[i] + Z * (Z0 + 0.001), ki[(i + 1) % 4] + Z * (Z0 + 0.001), kb[(i + 1) % 4] + Z * (Z0 + 0.001), kb[i] + Z * (Z0 + 0.001)], 'mermer', Z)
    for i in range(4):
        a, b = ki[i], ki[(i + 1) % 4]
        n = nx if i % 2 == 0 else ny
        inn = (V(cx, cy) - V((a.x + b.x) / 2, (a.y + b.y) / 2)).normalized()
        for m in range(n + 1):
            p = a.lerp(b, m / n)
            kutu_merkez(y, (p.x, p.y), 0.028, 0.028, za - Z0, 'granit_kizil', z0=Z0)
            kutu_merkez(y, (p.x, p.y), 0.034, 0.034, 0.006, 'granit_kizil_koyu', z0=Z0)
            if heykel and 0 < m < n and i in (1, 2, 3):
                q = p + inn * 0.04
                oturan_heykel(q.x, q.y, math.atan2(inn.y, inn.x), 1.15)
    y.yuz([V(ix0, iy0, Z0 + 0.002), V(ix1, iy0, Z0 + 0.002), V(ix1, iy1, Z0 + 0.002), V(ix0, iy1, Z0 + 0.002)], 'mermer')
    # drain channel and an altar in the court
    kutu_merkez(y, (cx, cy), 0.05, 0.05, 0.016, 'mermer', z0=Z0)
    # the doors: projecting granite frames with cedar leaves, on the front wall
    for u in kapilar:
        px = x0 + w * u
        fw, fh = 0.1, h * 0.86
        kutu(y, V(px - fw / 2, y0 - 0.02, Z0), X, fw, 0.035, fh, 'granit_kizil', 'sagsolust')
        dikdortgen_acik(y, V(px - fw / 2, y0 - 0.02), V(px + fw / 2, y0 - 0.02), Z0, fh, 0.27, 0.73, 0.0, fh * 0.74,
                        ('granit_kizil', 'granit_kizil_koyu', 'granit_kizil', 'ahsap'), derin=0.02)
        silme(y, dikdortgen(px - fw / 2, px + fw / 2, y0 - 0.02, y0 + 0.015), Z0 + fh, 0.012, 0.006, 'granit_kizil_koyu', 'tac')
        y.yuz([V(px - fw / 2, y0 - 0.02, Z0 + fh + 0.012), V(px + fw / 2, y0 - 0.02, Z0 + fh + 0.012), V(px + fw / 2, y0 + 0.015, Z0 + fh + 0.012), V(px - fw / 2, y0 + 0.015, Z0 + fh + 0.012)], 'granit_kizil')
    return zr + 0.018


y.bolum('Sfenks tapinagi')
zr = tapinak(SX0, -0.99, 0.62, 0.34, 0.13, 5, 2, kapilar=(0.3, 0.7))
sancak(y, SX0 + 0.29, -1.14, zr, boy=0.22, en=0.13, yuk=0.075, aci=0.4)

y.bolum('Vadi tapinagi')
VX, VY = -0.8, -0.79
zv = tapinak(VX, VY, 0.5, 0.5, 0.17, 3, 3, kapilar=(0.25, 0.75))
# guardian sphinxes by the two doors
for px in (VX - 0.24, VX + 0.24):
    with parca(y, (px, VY - 0.33, Z0), 0.0, 0.105):
        sfenks(tam=False)

# ---------------------------------------------------------------- the Giza plateau: Khafre's pyramid stands on the rock above the Sphinx
y.bolum('Plato')
HP = 0.1
PLX0, PLX1, PLY0, PLY1 = -1.17, -0.33, 0.12, 1.19
def kaya_teras(x0, x1, y0, y1, h):
    """a rock-cut terrace: three strata, each set back a little over the one below (alternating shades), a rough top"""
    zs_ = [Z0, Z0 + h * 0.38, Z0 + h * 0.72, Z0 + h]
    keys = ['kum_koyu', 'kum', 'kum_koyu']
    for k in range(3):
        d = 0.012 * k
        R = dikdortgen(x0 + d, x1 - d, y0 + d, y1 - d)
        duvarlar(y, R, zs_[k], zs_[k + 1], keys[k])
        if k < 2:   # the ledge to the next stratum
            Rn = dikdortgen(x0 + d + 0.012, x1 - d - 0.012, y0 + d + 0.012, y1 - d - 0.012)
            for i in range(4):
                j = (i + 1) % 4
                y.yuz_yon([R[i] + Z * zs_[k + 1], R[j] + Z * zs_[k + 1], Rn[j] + Z * zs_[k + 1], Rn[i] + Z * zs_[k + 1]], 'kum_acik', Z)
    y.yuz_yon(dikdortgen(x0 + 0.024, x1 - 0.024, y0 + 0.024, y1 - 0.024, Z0 + h), 'kum_acik', Z)
kaya_teras(PLX0, PLX1, PLY0, PLY1, HP)
# loose scree at the foot of the cut
for (bx, by, a, s) in ((-1.0, 0.07, 0.4, 1.0), (-0.55, 0.075, -0.3, 0.8), (-0.28, 0.5, 0.9, 0.9), (-0.29, 0.85, 0.2, 0.7)):
    kutu_merkez(y, (bx, by), 0.05 * s, 0.035 * s, 0.025 * s, 'kum', z0=Z0, aci=a)
ZP = Z0 + HP

y.bolum('Gecit yolu')
# the causeway: a covered corridor of limestone climbing from the valley temple up to the pyramid temple on the plateau,
# roof slits for light
CW, cxk = 0.08, -0.74
cy0, cy1, cyp = VY + 0.25, PLY0, 0.19
WH = 0.065
def zyol(yy):
    return Z0 + HP * max(0.0, min(1.0, (yy - cy0) / (cy1 - cy0)))
YS = [cy0 + (cy1 - cy0) * k / 6 for k in range(7)] + [cyp]
for sx in (-1, 1):
    xa = cxk + sx * CW / 2
    for k in range(len(YS) - 1):
        ya, yb = YS[k], YS[k + 1]
        zb0 = Z0 if ya < cy1 - 1e-6 else ZP
        q = [V(xa, ya, zb0), V(xa, yb, zb0), V(xa, yb, zyol(yb) + WH), V(xa, ya, zyol(ya) + WH)]
        y.yuz_yon(q, 'kirec', V(sx, 0, 0))
        # the plinth course
        q = [V(xa + sx * 0.006, ya, zb0), V(xa + sx * 0.006, yb, zb0), V(xa + sx * 0.006, yb, zyol(yb) * 0 + zb0 + 0.012), V(xa + sx * 0.006, ya, zb0 + 0.012)]
        y.yuz_yon(q, 'kum_koyu', V(sx, 0, 0))
        y.yuz_yon([V(xa, ya, zb0 + 0.012), V(xa, yb, zb0 + 0.012), V(xa + sx * 0.006, yb, zb0 + 0.012), V(xa + sx * 0.006, ya, zb0 + 0.012)], 'kum_koyu', Z)
    y.yuz_yon([V(xa, cy0, Z0), V(xa + sx * 0.006, cy0, Z0), V(xa + sx * 0.006, cy0, Z0 + 0.012), V(xa, cy0, Z0 + 0.012)], 'kum_koyu', -Y)
for k in range(len(YS) - 1):
    ya, yb = YS[k], YS[k + 1]
    y.yuz_yon([V(cxk - CW / 2, ya, zyol(ya) + WH), V(cxk + CW / 2, ya, zyol(ya) + WH), V(cxk + CW / 2, yb, zyol(yb) + WH), V(cxk - CW / 2, yb, zyol(yb) + WH)], 'kirec', Z)
# the open end at the valley temple is closed by the temple's back wall; a coping along both edges
for sx in (-1, 1):
    xa = cxk + sx * CW / 2
    for k in range(len(YS) - 1):
        ya, yb = YS[k], YS[k + 1]
        za, zb_ = zyol(ya) + WH, zyol(yb) + WH
        P = [V(xa - sx * 0.008, ya, za), V(xa + sx * 0.004, ya, za), V(xa + sx * 0.004, yb, zb_), V(xa - sx * 0.008, yb, zb_)]
        y.yuz_yon([p + Z * 0.008 for p in P], 'kirec', Z)
        y.yuz_yon([P[1], P[2], P[2] + Z * 0.008, P[1] + Z * 0.008], 'kirec', V(sx, 0, 0))
        y.yuz_yon([P[0], P[3], P[3] + Z * 0.008, P[0] + Z * 0.008], 'kirec', V(-sx, 0, 0))
for k in range(10):
    yy = cy0 + 0.05 + k * (cy1 - cy0 - 0.1) / 9
    zz = zyol(yy) + WH + 0.0015
    sl = (HP / (cy1 - cy0))
    y.yuz_yon([V(cxk - 0.017, yy - 0.006, zz - sl * 0.006), V(cxk + 0.017, yy - 0.006, zz - sl * 0.006),
               V(cxk + 0.017, yy + 0.006, zz + sl * 0.006), V(cxk - 0.017, yy + 0.006, zz + sl * 0.006)], 'koyu', Z)

# ---------------------------------------------------------------- pyramids, mortuary temple, mastabas
y.bolum('Piramitler')
PX, PY, PW, PH = -0.76, 0.78, 0.78, 0.76
# Khafre's pyramid: the stripped core in rough steps, the surviving casing smooth near the top
NB = 15; TC = 0.76
for k in range(NB):
    t0, t1 = TC * k / NB, TC * (k + 1) / NB
    w0, w1 = PW * (1 - t0), PW * (1 - t1)
    kutu_merkez(y, (PX, PY), w0, w0, PH * (t1 - t0), 'kum' if k % 2 else 'kum_koyu', z0=ZP + PH * t0, yuzler='onarkasagsol')
    # the ledge (tread) of each step
    a = dikdortgen(PX - w0 / 2, PX + w0 / 2, PY - w0 / 2, PY + w0 / 2, ZP + PH * t1)
    b = dikdortgen(PX - w1 / 2, PX + w1 / 2, PY - w1 / 2, PY + w1 / 2, ZP + PH * t1)
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([a[i], a[j], b[j], b[i]], 'kum_acik', Z)
piramit(y, (PX, PY), PW * (1 - TC), PH * (1 - TC), 'kirec', uc='kirec', uc_oran=0.0, kat=3, z0=ZP + PH * TC)
# the entrance on the north face, a robbers' tunnel
kutu_merkez(y, (PX, PY + PW / 2 - 0.01), 0.035, 0.03, 0.03, 'koyu', z0=ZP + 0.005, yuzler='arkaust')
# the mortuary temple at its foot, on the plateau
with parca(y, (0, 0, HP)):
    zm = tapinak(PX, 0.285, 0.3, 0.19, 0.09, 2, 1, kapilar=(0.5,), heykel=False)
# the queens' pyramids (one stepped) and the mastaba field
piramit(y, (0.95, 1.0), 0.28, 0.22, 'kum', uc='kirec', uc_oran=0.18, kat=5, z0=Z0)
basamakli_piramit(y, (1.0, 0.66), 0.24, 0.07, 4, 0.17, key='kum_koyu', merdiven=False, z0=Z0)


def mastaba(cx, cy, w, d, h):
    B = dikdortgen(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, Z0)
    ix = 0.18 * h
    T = dikdortgen(cx - w / 2 + ix, cx + w / 2 - ix, cy - d / 2 + ix, cy + d / 2 - ix, Z0 + h)
    for i in range(4):
        j = (i + 1) % 4
        e = B[j] - B[i]; nn = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], 'kirec', nn + Z * 0.18)
    y.yuz_yon(T, 'kirec', Z)
    silme(y, T, Z0 + h - 0.006, 0.006, 0.004, 'kirec', 'yarim')
    # the false doors (offering niches) on the east (front) face, a shaft opening on the roof
    nn = V(0, -1, 0.18).normalized()
    for u in (0.25, 0.75):
        c = B[0].lerp(B[1], u)
        for k, (ww, hh) in enumerate(((0.05, 0.78), (0.034, 0.64), (0.016, 0.52))):
            dd = 0.002 + k * 0.0012
            y.yuz_yon([c + X * (-ww / 2) + nn * dd, c + X * (ww / 2) + nn * dd,
                       c + X * (ww / 2) + V(0, ix * hh, h * hh) + nn * dd, c + X * (-ww / 2) + V(0, ix * hh, h * hh) + nn * dd],
                      ['kum_koyu', 'kirec', 'koyu'][k], nn)
    kutu_merkez(y, (cx, cy), 0.025, 0.025, 0.002, 'koyu', z0=Z0 + h)


for (cx, cy, w, d, h) in ((0.95, 0.3, 0.22, 0.15, 0.07), (0.95, 0.02, 0.22, 0.14, 0.06), (0.95, -0.3, 0.22, 0.15, 0.065), (0.95, -0.62, 0.2, 0.14, 0.06)):
    mastaba(cx, cy, w, d, h)
# palms by the harbour at the front, stone blocks lying about, a sledge with a block
for (px, py, b) in ((-0.32, -1.1, 0.2), (-0.42, -0.98, 0.17), (0.62, -1.1, 0.18), (0.98, -1.05, 0.2), (1.08, -0.85, 0.16), (-1.1, -0.45, 0.19), (-1.0, -0.38, 0.15)):
    agac(y, px, py, Z0, b, 'palmiye')
for (bx, by, a) in ((0.6, -0.62, 0.3), (0.66, -0.56, -0.2), (-0.45, -0.25, 0.5), (-0.5, -0.33, 0.1)):
    kutu_merkez(y, (bx, by), 0.06, 0.035, 0.03, 'kirec', z0=Z0, aci=a)
with parca(y, (-0.38, -0.5, Z0), 0.4):
    for s in (-1, 1):
        cubuk(y, V(-0.06, s * 0.02, 0.006), V(0.06, s * 0.02, 0.006), 0.01, 'ahsap', 0.012)
        boru(y, [V(0.06, s * 0.02, 0.006), V(0.075, s * 0.02, 0.018)], 0.005, 'ahsap', n=4)
    kutu_merkez(y, (0, 0), 0.09, 0.05, 0.05, 'granit_kizil', z0=0.012)
    boru(y, [V(0.075, -0.02, 0.018), V(0.14, 0.0, 0.01), V(0.075, 0.02, 0.018)], 0.002, 'saz_koyu', n=3)

# camels resting by the palms
def deve(x, yy, aci, cok=False):
    with parca(y, (x, yy, Z0), aci):
        h = 0.0 if cok else 0.045
        if cok:   # couched: legs folded under
            kutu_merkez(y, (0, 0), 0.07, 0.034, 0.016, 'ahsap_acik', z0=0)
        else:
            for lx in (-0.025, 0.025):
                for ly in (-0.01, 0.01):
                    cubuk(y, V(lx, ly, 0), V(lx, ly, 0.05), 0.006, 'ahsap_acik')
        boru(y, [V(-0.035, 0, h + 0.022), V(0.0, 0, h + 0.026), V(0.032, 0, h + 0.024)], 0.017, 'ahsap_acik', n=8)
        kure(y, (0.0, 0, h + 0.04), 0.016, 'ahsap_acik', n=8, kat=4)
        boru(y, [V(0.03, 0, h + 0.026), V(0.05, 0, h + 0.032), V(0.058, 0, h + 0.06), V(0.072, 0, h + 0.066)], 0.0065, 'ahsap_acik', n=6)
        boru(y, [V(0.068, 0, h + 0.068), V(0.088, 0, h + 0.062)], 0.007, 'ahsap_acik', n=6, r_son=0.004)
        kutu_merkez(y, (-0.01, 0), 0.03, 0.042, 0.004, 'boya_kirmizi', z0=h + 0.025)   # saddle cloth
        boru(y, [V(-0.035, 0, h + 0.02), V(-0.042, 0, h + 0.002)], 0.002, 'ahsap_koyu', n=4)
deve(0.6, -0.86, 0.5)
deve(0.74, -0.96, 2.6, cok=True)
deve(-0.25, -0.62, -0.4)

calistir(y, 'lm_sfenks')
