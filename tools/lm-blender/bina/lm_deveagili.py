# Deve Ağılı (lm_deveagili): an Arabian camel and horse yard in the Najdi mud-brick manner: a battered adobe enclosure
# with triangular crenellations, plaster bands and round corner towers, a timber gate between tapering buttresses; a
# tall tapering watchtower (after the Masmak towers) with rows of triangular vents, water spouts and a crenellated
# crown; the owner's two-storey mud house with a roof terrace; palm-frond shade sheds along the walls, camels standing,
# kneeling and drinking at the troughs, a horse; a draw-well with its pulley frame; a black goat-hair Bedouin tent
# with striped cloth, palms and fodder.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.03
K, KK, SV = 'kerpic', 'kerpic_koyu', 'siva_krem'
XW, YF, YB = 0.95, -0.6, 0.92      # the enclosure
HW = 0.2                            # its wall height
TW = 0.055                          # wall thickness
EG = 0.012                          # batter (the top is set back by that)
GX, GW = 0.22, 0.2                  # the gate: centre x, width

y.bolum('Zemin')
zemin(y, -1.12, 1.12, -1.08, 1.04, Z0, KK, 'kum_acik', basamak=(), silmeli=True)


# ---------------- helpers ----------------
def ucgen_prizma(a, b, z, h, d, key, yon):
    """a triangular merlon: base a->b on the wall top at z, apex h above, d deep (towards -yon from the a-b line)"""
    a, b = V(a[0], a[1], z), V(b[0], b[1], z)
    yon = V(yon[0], yon[1], 0).normalized()
    t = (a + b) / 2 + Z * h
    a2, b2, t2 = a - yon * d, b - yon * d, t - yon * d
    y.yuz_yon([a, b, t], key, yon)
    y.yuz_yon([a2, b2, t2], key, -yon)
    e = (b - a).normalized()
    y.yuz_yon([a, t, t2, a2], key, -e + Z)
    y.yuz_yon([t, b, b2, t2], key, e + Z)


def ucgen_dizi(a, b, z, h=0.032, w=0.042, g=0.014, d=0.016, key=K):
    """triangular crenellations (shurafat) along a->b, their front on the line facing right"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < w: return
    e = (b - a) / L; nn = V(e.y, -e.x)
    k = max(1, int((L + g) / (w + g)))
    w2 = (L + g) / k - g
    for i in range(k):
        p = a + e * (i * (w2 + g))
        ucgen_prizma(p, p + e * w2, z, h, d, key, nn)


def uc_delik(o, ex, nrm, w, h, key='koyu', gom=0.0012, d=0.0028):
    """a small triangular vent: a dark triangular prism sunk gom into the surface and standing d out of it"""
    o, ex, nrm = V(*o), V(*ex).normalized(), V(*nrm).normalized()
    up = nrm.cross(ex).normalized()
    if up.z < 0: up = -up
    tri = [o - ex * (w / 2), o + ex * (w / 2), o + up * h]
    alt = [p - nrm * gom for p in tri]; ust = [p + nrm * (d - gom) for p in tri]
    y.yuz_yon(ust, key, nrm)
    c = sum(tri, V(0, 0, 0)) / 3
    for i in range(3):
        j = (i + 1) % 3
        y.yuz_yon([alt[i], alt[j], ust[j], ust[i]], key, (tri[i] + tri[j]) / 2 - c)


def levha(pts, key, yon, t=0.003):
    """a thin sheet: both faces and the rims all round (yon: which side is the front; the thickness goes along the
    true normal)"""
    pts = [V(*p) for p in pts]
    nw = V(0, 0, 0)
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        nw += V((a.y - b.y) * (a.z + b.z), (a.z - b.z) * (a.x + b.x), (a.x - b.x) * (a.y + b.y))
    nw.normalize()
    yon = nw if nw.dot(V(*yon)) >= 0 else -nw
    ust = [p + yon * (t / 2) for p in pts]; alt = [p - yon * (t / 2) for p in pts]
    y.yuz_yon(ust, key, yon)
    y.yuz_yon(alt, key, -yon)
    c = sum(pts, V(0, 0, 0)) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        y.yuz_yon([ust[i], ust[j], alt[j], alt[i]], key, (pts[i] + pts[j]) / 2 - c)


def kerpic_hat(kose, z0, h, kapali=False, uc=(True, True)):
    """a battered mud-brick wall along a polyline (outer face on the right): the outer face leaning in by EG, the
    inner face upright TW behind, the top, a plaster band near the top, triangular crenellations on the outer edge"""
    n = len(kose)
    dis0 = [V(p.x, p.y, z0) for p in kose]
    dis1 = [V(p.x, p.y, z0 + h) for p in disa(kose, -EG, kapali)]
    ic = disa(kose, -TW, kapali)
    m = n if kapali else n - 1
    for i in range(m):
        j = (i + 1) % n
        e = (kose[j] - kose[i]); e.z = 0; e.normalize(); nc = V(e.y, -e.x)
        # the outer face in two bands (the lower one a darker plinth)
        mid = [dis0[i].lerp(dis1[i], 0.12), dis0[j].lerp(dis1[j], 0.12)]
        y.yuz_yon([dis0[i], dis0[j], mid[1], mid[0]], KK, nc + Z * 0.06)
        y.yuz_yon([mid[0], mid[1], dis1[j], dis1[i]], K, nc + Z * 0.06)
        duz_duvar(y, ic[j], ic[i], z0, z0 + h, K)
        y.yuz_yon([dis1[i], dis1[j], ic[j] + Z * (z0 + h), ic[i] + Z * (z0 + h)], SV, Z)
        # a plaster band a little under the top, standing proud of the face
        b0, b1 = dis0[i].lerp(dis1[i], 0.8), dis0[j].lerp(dis1[j], 0.8)
        b2, b3 = dis0[j].lerp(dis1[j], 0.88), dis0[i].lerp(dis1[i], 0.88)
        y.yuz_yon([b0 + nc * 0.003, b1 + nc * 0.003, b2 + nc * 0.003, b3 + nc * 0.003], SV, nc)
        y.yuz_yon([b3, b2, b2 + nc * 0.003, b3 + nc * 0.003], SV, Z)
        y.yuz_yon([b0, b1, b1 + nc * 0.003, b0 + nc * 0.003], SV, -Z)
        ucgen_dizi(disa([kose[i], kose[j]], -EG - 0.0, False)[0], disa([kose[i], kose[j]], -EG, False)[1], z0 + h)
        # wooden water spouts through the top of the wall
        L = (kose[j] - kose[i]).length
        for k in range(int(L / 0.32)):
            sp = dis1[i].lerp(dis1[j], (k + 0.5) / int(L / 0.32)) - Z * 0.012
            cubuk(y, sp - nc * 0.01, sp + nc * 0.045 - Z * 0.006, 0.009, 'ahsap_acik', 0.008)
        # rows of little triangular vents under the band
        L = (kose[j] - kose[i]).length
        nv = int(L / 0.12)
        for k in range(nv):
            p = dis0[i].lerp(dis0[j], (k + 0.5) / nv).lerp(dis1[i].lerp(dis1[j], (k + 0.5) / nv), 0.62)
            uc_delik(p, e, nc + Z * 0.06, 0.014, 0.012)
    if not kapali:
        for i, s in ((0, -1), (n - 1, 1)):
            if not uc[0 if i == 0 else 1]: continue
            e = (kose[1] - kose[0]) if i == 0 else (kose[-1] - kose[-2]); e.z = 0
            y.yuz_yon([dis0[i], ic[i] + Z * z0, ic[i] + Z * (z0 + h), dis1[i]], K, e * s)


def burc(c, r0, r1, z0, h, key=K, n=16, uclu=True):
    """a round tapering mud tower (Najdi burj): a darker foot, plaster bands, vents, a crown of triangular merlons"""
    donel(y, c, [(r0 * 1.04, z0), (r0 * 1.02, z0 + h * 0.1), (r0 + (r1 - r0) * 0.1, z0 + h * 0.1)], KK, n=n)
    nb = 4
    pr = [(r0 + (r1 - r0) * (0.1 + 0.9 * k / nb), z0 + h * (0.1 + 0.9 * k / nb)) for k in range(nb + 1)]
    donel(y, c, pr, key, n=n)
    R = lambda zz: r0 + (r1 - r0) * (zz - z0) / h
    for f in (0.55, 0.86):
        zz = z0 + h * f
        donel(y, c, [(R(zz), zz), (R(zz) + 0.004, zz), (R(zz + 0.014) + 0.004, zz + 0.014), (R(zz + 0.014), zz + 0.014)], SV, n=n)
    # the top: a ring walk and the crown
    zt = z0 + h
    y.yuz_yon([V(p.x, p.y, zt) for p in cokgen(c, r1, n)], SV, Z)
    if uclu:
        ring = cokgen(c, r1, n)
        for i in range(n):
            p, q = ring[i], ring[(i + 1) % n]
            nn = (p + q) / 2 - V(c[0], c[1]); nn.z = 0
            ucgen_prizma(p, q, zt, 0.03, 0.014, K, nn)
    return zt


def palmiye(x, yy, z, boy=0.3, egik=(0.012, 0.006)):
    """a date palm: a slightly curved trunk, a crown of arching fronds and date clusters"""
    tepe = V(x + egik[0], yy + egik[1], z + boy)
    boru(y, [V(x, yy, z), V(x + egik[0] * 0.3, yy + egik[1] * 0.3, z + boy * 0.5), tepe], 0.009, 'ahsap_acik', n=6, r_son=0.007)
    for i in range(8):
        a = TAU * i / 8 + 0.3 + 0.2 * (i % 2)
        d = V(math.cos(a), math.sin(a))
        L = 0.085 + 0.02 * (i % 2)
        boru(y, [tepe, tepe + d * (L * 0.45) + Z * 0.03, tepe + d * L - Z * 0.015, tepe + d * (L * 1.12) - Z * 0.045], 0.009,
             'boya_yesil' if i % 3 else 'zeytin', n=3, r_son=0.002)
    for i in range(3):
        a = TAU * i / 3
        kure(y, (tepe.x + 0.013 * math.cos(a), tepe.y + 0.013 * math.sin(a), tepe.z - 0.014), 0.009, 'siva_oker', n=6, kat=3)
    kure(y, (tepe.x, tepe.y, tepe.z + 0.004), 0.012, 'boya_yesil', n=8, kat=4)


# ---------------- camels and a horse ----------------
def deve(x, yy, aci, renk='siva_oker', yuk=False, cul='boya_kirmizi', olcek=1.35, egil=False):
    """a stylised dromedary (head towards +x before turning) on long legs; egil: the neck down to drink"""
    with parca(y, (x, yy, Z0), aci, olcek):
        h = 0.075
        boru(y, [V(-0.045, 0, h + 0.012), V(-0.01, 0, h + 0.02), V(0.03, 0, h + 0.018), V(0.048, 0, h + 0.012)], 0.02, renk, n=8)
        kure(y, (-0.045, 0, h + 0.012), 0.019, renk, n=8, kat=4)
        kure(y, (0.046, 0, h + 0.013), 0.018, renk, n=8, kat=4)
        donel(y, (-0.004, 0), [(0.026, h + 0.02), (0.022, h + 0.04), (0.012, h + 0.054), (0.0, h + 0.058)], renk, n=10)
        if egil:
            boru(y, [V(0.05, 0, h + 0.016), V(0.08, 0, h + 0.0), V(0.1, 0, h - 0.03), V(0.108, 0, h - 0.05)], 0.009, renk, n=6, r_son=0.007)
            boru(y, [V(0.106, 0, h - 0.048), V(0.124, 0, h - 0.064)], 0.009, renk, n=6, r_son=0.006)
        else:
            boru(y, [V(0.05, 0, h + 0.016), V(0.082, 0, h + 0.004), V(0.102, 0, h + 0.026), V(0.106, 0, h + 0.05)], 0.009, renk, n=6, r_son=0.007)
            boru(y, [V(0.102, 0, h + 0.054), V(0.13, 0, h + 0.047)], 0.009, renk, n=6, r_son=0.006)
            for s in (-1, 1):
                cubuk(y, V(0.104, s * 0.006, h + 0.06), V(0.101, s * 0.007, h + 0.069), 0.003, renk)
        boru(y, [V(-0.062, 0, h + 0.02), V(-0.07, 0, h - 0.005), V(-0.068, 0, h - 0.02)], 0.0025, 'ahsap_koyu', n=4, r_son=0.0015)
        for lx in (-0.04, 0.038):
            for s in (-1, 1):
                boru(y, [V(lx, s * 0.01, h + 0.004), V(lx + 0.004, s * 0.01, h * 0.5), V(lx, s * 0.01, 0.006)], 0.0055, renk, n=5, r_son=0.004)
                kutu_merkez(y, (lx + 0.003, s * 0.01), 0.012, 0.01, 0.006, 'ahsap_koyu')
        if yuk:
            kutu_merkez(y, (-0.004, 0), 0.05, 0.05, 0.004, cul, z0=h + 0.03)
            for s in (-1, 1):
                kutu_merkez(y, (-0.004, s * 0.034), 0.05, 0.026, 0.04, 'kumas' if s > 0 else 'kece', z0=h - 0.005)
        else:
            # a saddle cloth with tassels over the hump
            kutu_merkez(y, (-0.004, 0), 0.044, 0.046, 0.003, cul, z0=h + 0.031)


def deve_cok(x, yy, aci, renk='siva_oker', olcek=1.35):
    """a kneeling camel: the body on folded legs, the neck up, the head turned forward"""
    with parca(y, (x, yy, Z0), aci, olcek):
        h = 0.03
        boru(y, [V(-0.045, 0, h + 0.01), V(-0.01, 0, h + 0.016), V(0.03, 0, h + 0.014), V(0.046, 0, h + 0.01)], 0.022, renk, n=8)
        kure(y, (-0.045, 0, h + 0.01), 0.021, renk, n=8, kat=4)
        kure(y, (0.045, 0, h + 0.011), 0.02, renk, n=8, kat=4)
        donel(y, (-0.004, 0), [(0.028, h + 0.018), (0.023, h + 0.04), (0.012, h + 0.055), (0.0, h + 0.06)], renk, n=10)
        boru(y, [V(0.05, 0, h + 0.014), V(0.075, 0, h + 0.02), V(0.088, 0, h + 0.05), V(0.09, 0, h + 0.075)], 0.009, renk, n=6, r_son=0.007)
        boru(y, [V(0.088, 0, h + 0.078), V(0.115, 0, h + 0.072)], 0.009, renk, n=6, r_son=0.006)
        for s in (-1, 1):
            cubuk(y, V(0.09, s * 0.006, h + 0.083), V(0.088, s * 0.007, h + 0.092), 0.003, renk)
            # the folded legs (round, tapering): the forearm out to the knee in front, the shin tucked back under the
            # chest; the hind thigh down to the hock behind, the shank folded forward along the ground
            boru(y, [V(0.034, s * 0.018, h + 0.004), V(0.058, s * 0.022, 0.016), V(0.068, s * 0.023, 0.007)], 0.0075, renk, n=6, r_son=0.0065)
            boru(y, [V(0.068, s * 0.023, 0.007), V(0.045, s * 0.025, 0.0055), V(0.022, s * 0.024, 0.005)], 0.0062, renk, n=6, r_son=0.0048)
            kure(y, (0.068, s * 0.023, 0.0075), 0.0078, 'kerpic_koyu', n=6, kat=3)
            boru(y, [V(-0.036, s * 0.02, h + 0.012), V(-0.058, s * 0.026, 0.018), V(-0.074, s * 0.027, 0.008)], 0.0105, renk, n=6, r_son=0.007)
            boru(y, [V(-0.074, s * 0.027, 0.008), V(-0.05, s * 0.029, 0.0055), V(-0.024, s * 0.028, 0.005)], 0.006, renk, n=6, r_son=0.0045)
            kure(y, (-0.022, s * 0.028, 0.005), 0.0055, 'ahsap_koyu', n=6, kat=3)
        # the chest pad it rests on
        kure(y, (0.03, 0, 0.012), 0.014, renk, n=8, kat=4)
        kutu_merkez(y, (-0.004, 0), 0.044, 0.05, 0.003, 'boya_kirmizi', z0=h + 0.032)


def at(x, yy, aci, renk='ahsap', yele='ahsap_koyu', olcek=1.3):
    """a stylised Arabian horse: a compact body, the high-carried tail, the arched neck and a fine head"""
    with parca(y, (x, yy, Z0), aci, olcek):
        h = 0.06
        boru(y, [V(-0.035, 0, h + 0.012), V(0.0, 0, h + 0.014), V(0.035, 0, h + 0.014)], 0.017, renk, n=8)
        kure(y, (-0.035, 0, h + 0.012), 0.016, renk, n=8, kat=4)
        kure(y, (0.036, 0, h + 0.014), 0.016, renk, n=8, kat=4)
        boru(y, [V(0.04, 0, h + 0.02), V(0.055, 0, h + 0.042), V(0.062, 0, h + 0.056)], 0.009, renk, n=6, r_son=0.007)
        boru(y, [V(0.06, 0, h + 0.058), V(0.085, 0, h + 0.046)], 0.008, renk, n=6, r_son=0.005)
        boru(y, [V(0.036, 0, h + 0.03), V(0.05, 0, h + 0.05), V(0.058, 0, h + 0.064)], 0.004, yele, n=4)
        boru(y, [V(-0.05, 0, h + 0.022), V(-0.064, 0, h + 0.03), V(-0.072, 0, h + 0.0)], 0.005, yele, n=4, r_son=0.002)
        for s in (-1, 1):
            cubuk(y, V(0.058, s * 0.004, h + 0.064), V(0.058, s * 0.005, h + 0.074), 0.003, renk)
        for lx in (-0.032, 0.032):
            for s in (-1, 1):
                boru(y, [V(lx, s * 0.009, h + 0.002), V(lx, s * 0.009, h * 0.45), V(lx + 0.002, s * 0.009, 0.004)], 0.0045, renk, n=5, r_son=0.0032)
                kutu_merkez(y, (lx + 0.002, s * 0.009), 0.008, 0.008, 0.005, 'koyu')
        kutu_merkez(y, (0.004, 0), 0.03, 0.04, 0.003, 'lacivert', z0=h + 0.029)


# ---------------- the enclosure ----------------
y.bolum('Kerpiç ağıl duvarı, köşe burçları, kapı')
gx0, gx1 = GX - GW / 2, GX + GW / 2
CW = [V(gx1, YF), V(XW, YF), V(XW, YB), V(-XW, YB), V(-XW, YF), V(gx0, YF)]
kerpic_hat(CW, Z0, HW)
for p in (V(XW, YF), V(XW, YB), V(-XW, YB), V(-XW, YF)):
    burc((p.x, p.y), 0.085, 0.068, Z0, HW + 0.08, n=14)
# half-round buttresses along the walls (their inner halves are hidden in the wall)
for (bx, by) in ((-0.6, YF), (-0.22, YF), (0.64, YF), (XW, -0.12), (XW, 0.4), (0.5, YB), (-0.1, YB), (-0.58, YB), (-XW, -0.12), (-XW, 0.4)):
    burc((bx, by), 0.05, 0.04, Z0, HW + 0.045, n=10)
# the yard: trodden earth inside the walls
y.yuz_yon([V(-XW + TW, YF + TW, Z0 + 0.001), V(XW - TW, YF + TW, Z0 + 0.001), V(XW - TW, YB - TW, Z0 + 0.001), V(-XW + TW, YB - TW, Z0 + 0.001)], 'siva_krem', Z)
# the gate: tapering buttresses, a timber lintel, a plastered crest and the double door
for sx in (-1, 1):
    x = GX + sx * (GW / 2 + 0.035)
    B = dikdortgen(x - 0.04, x + 0.04, YF - 0.035, YF + 0.025, Z0)
    T = dikdortgen(x - 0.028, x + 0.028, YF - 0.022, YF + 0.02, Z0 + HW + 0.11)
    for i in range(4):
        j = (i + 1) % 4
        e = B[j] - B[i]; nn = V(e.y, -e.x).normalized()
        y.yuz_yon([B[i], B[j], T[j], T[i]], K, nn + Z * 0.1)
    y.yuz_yon(T, SV, Z)
    for i in range(4):
        p, q = T[i], T[(i + 1) % 4]
        nn = (p + q) / 2 - V(x, (YF - 0.022 + YF + 0.02) / 2, p.z); nn.z = 0
        ucgen_prizma(p, q, T[0].z, 0.03, 0.014, K, nn)
    for f in (0.45, 0.75):
        zz = Z0 + (HW + 0.11) * f
        P = [B[i].lerp(T[i], f) for i in range(4)]
        silme(y, [V(p.x, p.y) for p in P], zz, 0.012, 0.004, SV, 'duz')
# the lintel beam and the wall over the gate
ZL = Z0 + HW * 0.78
for zz in (ZL, ZL + 0.016):
    cubuk(y, V(gx0 - 0.03, YF - 0.012, zz), V(gx1 + 0.03, YF - 0.012, zz), 0.016, 'ahsap_koyu', 0.016)
kutu(y, V(gx0, YF + 0.0, ZL + 0.024), X, GW, TW, HW - (ZL + 0.024 - Z0), K, 'onarkaust')
ucgen_dizi(V(gx0, YF + EG), V(gx1, YF + EG), Z0 + HW)
# the door leaves (one half open), studs, and the threshold
for sx, ac in ((-1, 0.0), (1, 1.1)):
    hx = GX + sx * GW / 2
    with parca(y, (hx, YF + 0.02, Z0), (0 if sx < 0 else math.pi) + (-ac if sx < 0 else ac)):
        kutu(y, V(0, -0.006, 0), X, GW / 2, 0.012, ZL - Z0 - 0.002, 'ahsap', 'onarkasagsolust')
        for zz in (0.03, 0.08, 0.13):
            cubuk(y, V(0.004, -0.008, zz), V(GW / 2 - 0.004, -0.008, zz), 0.008, 'ahsap_koyu', 0.004)
        # Najdi painted door: rows of coloured triangles between the battens
        for r_, zz in enumerate((0.044, 0.094)):
            for i in range(4):
                uc_delik(V(GW / 2 * (i + 0.5) / 4, -0.006, zz), X, -Y, 0.018, 0.024, ('boya_kirmizi', 'boya_sari', 'turkuaz', 'siva_krem')[(i + r_) % 4], gom=0.0008, d=0.0016)
y.yuz_yon([V(gx0, YF - 0.03, Z0 + 0.003), V(gx1, YF - 0.03, Z0 + 0.003), V(gx1, YF + TW, Z0 + 0.003), V(gx0, YF + TW, Z0 + 0.003)], 'tas_koyu', Z)


# ---------------- the house ----------------
y.bolum('Sahibinin iki katlı kerpiç evi')
HX0, HX1, HY0, HY1 = -XW + TW + 0.002, 0.22, 0.5, YB - TW - 0.002
H1, H2 = 0.24, 0.2
UX1, UY0 = -0.22, 0.62      # the upper storey


def ev_cephe(a, b, z0, H, pencere_say, kapi_k=None, ust=False):
    """a house wall a->b: plastered plinth, square windows with wooden shutters (or a studded door), a vent row and
    a plaster band at the top"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    n = max(1, pencere_say)
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if kapi_k == k:
            dikdortgen_acik(y, p, q, z0, H, 0.3, 0.7, 0.0, H * 0.62, (K, KK, SV, 'ahsap'), derin=0.02, cerceve=(0.008, SV))
            # door studs
            W = (q - p).length
            for i in range(3):
                for j in range(4):
                    o = p + e * (W * (0.36 + 0.28 * (i + 0.5) / 3)) - nn * 0.019 + Z * (z0 + H * 0.62 * (j + 0.6) / 4.5)
                    kutu_merkez(y, (o.x, o.y), 0.005, 0.005, 0.005, 'koyu', z0=o.z, aci=math.atan2(e.y, e.x))
        elif pencere_say:
            W_, e_, nc, L_ = dikdortgen_acik(y, p, q, z0, H, 0.36, 0.64, H * 0.36, H * 0.68, (K, KK, SV, 'koyu'), derin=0.018, cerceve=(0.007, SV))
            # an open shutter on each side
            for s, u in ((-1, 0.36), (1, 0.64)):
                pp = p.lerp(q, u) + nn * 0.004
                levha([pp + Z * (z0 + H * 0.36), pp + e * (s * 0.028) + nn * 0.01 + Z * (z0 + H * 0.36),
                       pp + e * (s * 0.028) + nn * 0.01 + Z * (z0 + H * 0.68), pp + Z * (z0 + H * 0.68)], 'ahsap_koyu', nn * (-s) + e * 0.0, t=0.004)
        else:
            duz_duvar(y, p, q, z0, z0 + H, K)
    # the plaster band and the vent row
    kutu(y, a + Z * (z0 + H - 0.03) + nn * 0.004, e, L, 0.004, 0.012, SV, 'onust')
    nv = int(L / 0.07)
    for k in range(nv):
        uc_delik(a + e * (L * (k + 0.5) / nv) + Z * (z0 + H - 0.05), e, nn, 0.012, 0.011)
    # a wooden water spout at the roof line
    for u in (0.25, 0.75):
        sp = a + e * (L * u) + Z * (z0 + H - 0.01)
        cubuk(y, sp - nn * 0.004, sp + nn * 0.05 - Z * 0.008, 0.009, 'ahsap_acik', 0.008)


HK = dikdortgen(HX0, HX1, HY0, HY1)
ev_cephe(HK[0], HK[1], Z0, H1, 4, kapi_k=2)
ev_cephe(HK[1], HK[2], Z0, H1, 2)
ev_cephe(HK[2], HK[3], Z0, H1, 0)
ev_cephe(HK[3], HK[0], Z0, H1, 0)
silme(y, HK, Z0, 0.02, 0.006, KK, 'kaide')
y.yuz_yon([V(p.x, p.y, Z0 + H1) for p in HK], SV, Z)
# the terrace parapet (front and right edges), with crenellations
PT = [V(UX1, HY0), V(HX1, HY0), V(HX1, HY1)]
parapet(y, [V(HX0, HY0)] + PT, Z0 + H1, 0.03, 0, 0.016, K, kapali=False, ust_key=SV)
dk = [V(HX0, HY0)] + PT
for i in range(len(dk) - 1):
    ucgen_dizi(dk[i], dk[i + 1], Z0 + H1 + 0.03, h=0.026, w=0.034, g=0.012, d=0.014)
# the upper storey
UK = dikdortgen(HX0, UX1, UY0, HY1)
ev_cephe(UK[0], UK[1], Z0 + H1, H2, 3, kapi_k=2)
ev_cephe(UK[1], UK[2], Z0 + H1, H2, 1)
ev_cephe(UK[2], UK[3], Z0 + H1, H2, 3)
ev_cephe(UK[3], UK[0], Z0 + H1, H2, 1)
y.yuz_yon([V(p.x, p.y, Z0 + H1 + H2) for p in UK], SV, Z)
parapet(y, UK, Z0 + H1 + H2, 0.026, 0, 0.016, K, ust_key=SV)
for i in range(4):
    ucgen_dizi(UK[i], UK[(i + 1) % 4], Z0 + H1 + H2 + 0.026, h=0.026, w=0.034, g=0.012, d=0.014)
# a palm-frond awning (rafters and matting) over part of the terrace, and a stair up the front
for i in range(4):
    x = -0.18 + 0.1 * i
    cubuk(y, V(x, UY0 + 0.01, Z0 + H1 + 0.13), V(x, HY0 + 0.03, Z0 + H1 + 0.1), 0.008, 'ahsap_acik')
    y.prizma((x, HY0 + 0.03), 0.0045, Z0 + H1, Z0 + H1 + 0.1, 'ahsap_acik', n=5)
levha([V(-0.2, HY0 + 0.025, Z0 + H1 + 0.108), V(0.14, HY0 + 0.025, Z0 + H1 + 0.108), V(0.14, UY0 + 0.01, Z0 + H1 + 0.138), V(-0.2, UY0 + 0.01, Z0 + H1 + 0.138)],
      'saz', V(0, -0.03, 0.12), t=0.006)
merdiven(y, (HX1 + 0.035, HY0 + 0.02), math.pi / 2, 0.05, Z0, Z0 + H1, n=8, d=0.04, key=K, yanlik=KK)

# ---------------- the watchtower ----------------
y.bolum('Gözcü kulesi (Mismak burcu)')
TC = (0.44, 0.7)
TR0, TR1, TH = 0.13, 0.088, 0.86
nb = 10
donel(y, TC, [(TR0 * 1.06, Z0), (TR0 * 1.06, Z0 + 0.04), (TR0, Z0 + 0.045)], KK, n=20)
pr = [(TR0 + (TR1 - TR0) * k / nb, Z0 + 0.045 + (TH - 0.045) * k / nb) for k in range(nb + 1)]
donel(y, TC, pr, K, n=20)
TRz = lambda zz: TR0 + (TR1 - TR0) * (zz - Z0 - 0.045) / (TH - 0.045)
for f in (0.3, 0.58, 0.84):
    zz = Z0 + TH * f
    donel(y, TC, [(TRz(zz), zz), (TRz(zz) + 0.005, zz), (TRz(zz + 0.016) + 0.005, zz + 0.016), (TRz(zz + 0.016), zz + 0.016)], SV, n=20)
# rows of triangular vents, offset row to row, and wooden spouts
for r_, (f, nv) in enumerate(((0.44, 6), (0.7, 7), (0.93, 9))):
    zz = Z0 + TH * f
    for i in range(nv):
        a = TAU * (i + 0.5 * (r_ % 2)) / nv + 0.2
        nrm = V(math.cos(a), math.sin(a), (TR0 - TR1) / TH)
        o = V(TC[0], TC[1], zz) + V(math.cos(a), math.sin(a), 0) * TRz(zz)
        uc_delik(o, V(-math.sin(a), math.cos(a), 0), nrm, 0.018, 0.016)
for a in (0.6, 2.4, 4.2):
    d = V(math.cos(a), math.sin(a), 0)
    zz = Z0 + TH - 0.02
    cubuk(y, V(TC[0], TC[1], zz) + d * (TR1 - 0.004), V(TC[0], TC[1], zz) + d * (TR1 + 0.055) - Z * 0.008, 0.011, 'ahsap_acik', 0.01)
# the door at the foot (towards the yard)
a = -math.pi / 2 - 0.35
d = V(math.cos(a), math.sin(a), 0); e = V(-d.y, d.x, 0)
o = V(TC[0], TC[1], 0) + d * (TR0 - 0.004)
kutu(y, o - e * 0.028 + Z * Z0, e, 0.056, 0.012, 0.11, 'ahsap', 'onsagsolust')
kutu(y, o - e * 0.036 + d * 0.004 + Z * (Z0 + 0.11), e, 0.072, 0.02, 0.014, 'ahsap_koyu', 'onsagsolust')
# the crown: corbelled out, crenellated, a lookout hut with a palm roof
zt = Z0 + TH
konsol_halka(y, cokgen(TC, TR1, 20), zt - 0.03, 0.03, 0.022, SV, 3)
RC = TR1 + 0.022
y.yuz_yon([V(p.x, p.y, zt) for p in cokgen(TC, RC, 20)], SV, Z)
donel(y, TC, [(RC, zt), (RC, zt + 0.04)], K, n=20)
donel(y, TC, [(RC - 0.014, zt + 0.04), (RC - 0.014, zt)], K, n=20)
donel(y, TC, [(RC, zt + 0.04), (RC - 0.014, zt + 0.04)], SV, n=20)
ring = cokgen(TC, RC, 20)
for i in range(20):
    p, q = ring[i], ring[(i + 1) % 20]
    nn = (p + q) / 2 - V(TC[0], TC[1]); nn.z = 0
    ucgen_prizma(p, q, zt + 0.04, 0.036, 0.014, K, nn)
for i in range(4):
    a = TAU * i / 4 + math.pi / 4
    y.prizma((TC[0] + 0.045 * math.cos(a), TC[1] + 0.045 * math.sin(a)), 0.005, zt, zt + 0.11, 'ahsap_acik', n=5)
cati_kirma(y, TC[0] - 0.05, TC[0] + 0.05, TC[1] - 0.05, TC[1] + 0.05, zt + 0.11, 0.045, 0.014, 'saz', 'saz_koyu', kalinlik=0.008, ns=4, nr=2)
top_t = zt + 0.11 + 0.045
sancak(y, TC[0] + 0.0, TC[1] + 0.0, top_t - 0.005, boy=0.18, en=0.11, yuk=0.07, aci=-0.4)

# ---------------- shade sheds ----------------
y.bolum('Hurma dalı gölgelikler, yemlikler')


def golgelik(x0, x1, y0, y1, yon, n):
    """a shed against a wall: palm-trunk posts in a row on the open side, beams, rafters to the wall, a palm-frond
    roof falling to the open side; yon: +1 the wall at x1 (open towards -x), -1 the wall at x0"""
    xa, xb = (x0, x1) if yon > 0 else (x1, x0)          # xa open side, xb the wall
    zo, zw = Z0 + 0.19, Z0 + 0.21
    for k in range(n + 1):
        yy = y0 + (y1 - y0) * k / n
        y.prizma((xa, yy), 0.008, Z0, zo, 'ahsap_acik', n=6)
        cubuk(y, V(xa, yy, zo), V(xb, yy, zw), 0.008, 'ahsap', 0.008)
    cubuk(y, V(xa, y0 - 0.01, zo), V(xa, y1 + 0.01, zo), 0.012, 'ahsap_koyu', 0.012)
    so = 1 if xa < xb else -1
    # the roof: palm-frond mats (arish) laid side by side with gaps of light between, ragged at the eave
    nm = int((y1 - y0 + 0.06) / 0.05)
    for k in range(nm):
        ya = y0 - 0.03 + (y1 - y0 + 0.06) * k / nm
        yb = ya + (y1 - y0 + 0.06) / nm - 0.012
        uz = 0.03 + 0.012 * ((k * 7) % 3)
        p = [V(xa - so * uz, ya, zo + 0.009), V(xa - so * uz, yb, zo + 0.009), V(xb, yb, zw + 0.013), V(xb, ya, zw + 0.013)]
        levha(p, 'saz' if k % 3 else 'saz_koyu', Z, t=0.007)
    # the purlins under the mats
    for f in (0.35, 0.7):
        xx = xa + (xb - xa) * f
        cubuk(y, V(xx, y0 - 0.02, zo + (zw - zo) * f), V(xx, y1 + 0.02, zo + (zw - zo) * f), 0.008, 'ahsap', 0.008)
    # the trodden, darker floor under the shed (straw and dung)
    xl, xr = sorted((xa - so * 0.035, xb))
    y.yuz_yon([V(xl, y0 - 0.025, Z0 + 0.0018), V(xr, y0 - 0.025, Z0 + 0.0018), V(xr, y1 + 0.025, Z0 + 0.0018), V(xl, y1 + 0.025, Z0 + 0.0018)], 'toprak', Z)
    # a feed manger along the wall
    xm = xb - so * 0.04
    kutu_merkez(y, (xm, (y0 + y1) / 2), 0.05, y1 - y0 - 0.04, 0.045, KK, z0=Z0, yuzler='onarkasagsol')
    y.yuz_yon([V(xm - 0.025, y0 + 0.02, Z0 + 0.045), V(xm + 0.025, y0 + 0.02, Z0 + 0.045), V(xm + 0.025, y1 - 0.02, Z0 + 0.045), V(xm - 0.025, y1 - 0.02, Z0 + 0.045)], 'saz', Z)


golgelik(-XW + TW, -0.66, YF + TW + 0.03, HY0 - 0.06, -1, 4)
golgelik(0.66, XW - TW, YF + TW + 0.03, 0.4, 1, 4)
# camels and the horse under the sheds
deve_cok(-0.78, -0.35, 0.3)
deve(-0.78, 0.0, math.pi * 0.05, renk='toprak', cul='lacivert')
deve_cok(-0.8, 0.3, -0.4, renk='kaya')
at(0.8, -0.3, math.pi, renk='kerpic_koyu')
at(0.79, -0.44, math.pi * 0.95, renk='kaya', yele='koyu')
deve_cok(0.4, -0.22, 2.4, renk='kaya')
deve_cok(0.5, -0.05, 3.6, renk='siva_oker')
deve(0.8, 0.05, math.pi * 1.02, renk='siva_oker', cul='boya_kirmizi')
deve_cok(0.8, 0.28, math.pi * 1.1, renk='toprak', olcek=1.0)

# ---------------- the well and troughs ----------------
y.bolum('Çıkrıklı kuyu, yalaklar')
WC = (-0.12, 0.08)
y.prizma(WC, 0.075, Z0, Z0 + 0.055, KK, n=14, ust=False)
donel(y, WC, [(0.075, Z0 + 0.055), (0.08, Z0 + 0.055), (0.08, Z0 + 0.065), (0.06, Z0 + 0.065), (0.06, Z0 + 0.02)], SV, n=14)
y.yuz_yon([V(p.x, p.y, Z0 + 0.02) for p in cokgen(WC, 0.06, 14)], 'su', Z)
# the pulley frame: two posts, a crossbeam, the wheel and the rope; a second frame for the other rope
for sx in (-1, 1):
    cubuk(y, V(WC[0] + sx * 0.07, WC[1], Z0 + 0.06), V(WC[0] + sx * 0.06, WC[1], Z0 + 0.25), 0.014, 'ahsap', 0.012)
cubuk(y, V(WC[0] - 0.085, WC[1], Z0 + 0.25), V(WC[0] + 0.085, WC[1], Z0 + 0.25), 0.016, 'ahsap_koyu', 0.016)
for sx in (-0.03, 0.03):
    c = V(WC[0] + sx, WC[1], Z0 + 0.225)
    pts = [c + V(0.004, 0.022 * math.cos(TAU * i / 12), 0.022 * math.sin(TAU * i / 12)) for i in range(12)]
    y.yuz_yon(pts, 'ahsap_acik', X)
    y.yuz_yon([p - V(0.008, 0, 0) for p in pts], 'ahsap_acik', -X)
    y.serit([p - V(0.008, 0, 0) for p in pts], pts, 'ahsap_acik')
    cubuk(y, c + V(0, -0.02, -0.006), V(c.x, WC[1] - 0.02, Z0 + 0.03), 0.003, 'kumas')
    # the rope runs out to the draw path
    cubuk(y, c + V(0, 0.02, 0.004), V(c.x, WC[1] + 0.32, Z0 + 0.09), 0.003, 'kumas')
# the leather bucket at the rim and the draw path
donel(y, (WC[0] + 0.03, WC[1] - 0.02), [(0.0, Z0 + 0.065), (0.012, Z0 + 0.065), (0.016, Z0 + 0.09), (0.0, Z0 + 0.09)], 'ahsap', n=8)
y.yuz_yon([V(WC[0] - 0.08, WC[1] + 0.09, Z0 + 0.002), V(WC[0] + 0.08, WC[1] + 0.09, Z0 + 0.002), V(WC[0] + 0.08, WC[1] + 0.38, Z0 + 0.002), V(WC[0] - 0.08, WC[1] + 0.38, Z0 + 0.002)], 'kerpic', Z)
deve(WC[0], WC[1] + 0.33, math.pi / 2, renk='siva_oker', cul='boya_sari')


def yalak(x0, x1, y0, y1):
    """a stone trough: kerb walls, rim, the water a little below"""
    dk = dikdortgen(x0, x1, y0, y1); ik = disa(dk, -0.012)
    duvarlar(y, dk, Z0, Z0 + 0.04, 'tas_koyu')
    for i in range(4):
        j = (i + 1) % 4
        y.yuz_yon([dk[i] + Z * (Z0 + 0.04), dk[j] + Z * (Z0 + 0.04), ik[j] + Z * (Z0 + 0.04), ik[i] + Z * (Z0 + 0.04)], 'tas', Z)
        duz_duvar(y, ik[j], ik[i], Z0 + 0.026, Z0 + 0.04, 'tas_koyu')
    y.yuz_yon([V(p.x, p.y, Z0 + 0.026) for p in ik], 'su', Z)


yalak(-0.38, 0.12, -0.2, -0.15)
yalak(0.14, 0.2, -0.05, 0.25)
deve(-0.25, -0.3, math.pi / 2, renk='toprak', cul='turkuaz', egil=True)
deve(0.0, -0.31, math.pi / 2 - 0.1, renk='siva_oker', egil=True)
deve(-0.5, -0.42, 0.3, olcek=0.9, renk='kaya')
deve(0.32, 0.08, math.pi, renk='toprak', cul='boya_kirmizi', egil=True)

# ---------------- fodder ----------------
y.bolum('Yem: saman yığınları, çuvallar, eyerler')
for (cx, cy, r) in ((0.45, 0.35, 0.06), (0.56, 0.3, 0.045), (-0.55, 0.38, 0.05)):
    donel(y, (cx, cy), [(r, Z0), (r * 1.05, Z0 + r * 0.5), (r * 0.7, Z0 + r * 1.05), (0.0, Z0 + r * 1.3)], 'saz', n=10)
for (cx, cy, a) in ((0.42, -0.45, 0.2), (0.48, -0.48, -0.3), (0.45, -0.41, 1.2)):
    kutu_merkez(y, (cx, cy), 0.045, 0.03, 0.025, 'kumas', z0=Z0, aci=a)
# saddles on a rail by the house
cubuk(y, V(-0.5, HY0 - 0.06, Z0 + 0.07), V(-0.2, HY0 - 0.06, Z0 + 0.07), 0.01, 'ahsap', 0.01)
for x in (-0.5, -0.2):
    cubuk(y, V(x, HY0 - 0.06, Z0), V(x, HY0 - 0.06, Z0 + 0.075), 0.01, 'ahsap_koyu')
for i, (x, key) in enumerate(((-0.42, 'boya_kirmizi'), (-0.33, 'lacivert'), (-0.26, 'boya_sari'))):
    kutu_merkez(y, (x, HY0 - 0.06), 0.05, 0.04, 0.004, key, z0=Z0 + 0.076)
    for s in (-1, 1):
        levha([V(x - 0.024, HY0 - 0.06 + s * 0.02, Z0 + 0.078), V(x + 0.024, HY0 - 0.06 + s * 0.02, Z0 + 0.078),
               V(x + 0.024, HY0 - 0.06 + s * 0.026, Z0 + 0.03), V(x - 0.024, HY0 - 0.06 + s * 0.026, Z0 + 0.03)], key, V(0, s, 0), t=0.003)
    cubuk(y, V(x, HY0 - 0.06, Z0 + 0.08), V(x, HY0 - 0.06, Z0 + 0.1), 0.012, 'ahsap', 0.01)

# ---------------- the Bedouin tent outside ----------------
y.bolum('Bedevi kıl çadırı (beyt eş-şa\'r)')
CX0, CX1, CY0, CY1 = -0.95, -0.3, -1.0, -0.74
# poles: three on the ridge line, a row along the open front
NP = 3
zr, zf = Z0 + 0.17, Z0 + 0.1
ym = (CY0 + CY1) / 2 + 0.02
NU, NV = 12, 8


def cadir_z(u, v):
    """the roof cloth: ridge peaks at the poles, sagging between, falling to the open front (v=0) and the back (v=1)"""
    x = CX0 + (CX1 - CX0) * u
    tepe = 0.0
    for k in range(NP):
        px = CX0 + (CX1 - CX0) * (k + 0.5) / NP
        tepe = max(tepe, math.exp(-((x - px) / 0.07) ** 2))
    sag = 0.02 * (1 - tepe)
    vm = 0.55
    if v < vm:
        z = zf + (zr - zf) * (v / vm) ** 0.8 - sag * (v / vm)
    else:
        z = zr - (zr - Z0 - 0.06) * ((v - vm) / (1 - vm)) ** 1.1 - sag
    return z


P = [[V(CX0 + (CX1 - CX0) * i / NU, CY0 + (CY1 - CY0) * j / NV, cadir_z(i / NU, j / NV)) for j in range(NV + 1)] for i in range(NU + 1)]
TK = 0.004
for i in range(NU):
    for j in range(NV):
        renk = 'kumas' if j in (2, 6) else ('kece' if j == 4 else 'koyu')
        q = [P[i][j], P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]]
        nrm = (q[1] - q[0]).cross(q[3] - q[0]).normalized()
        if nrm.z < 0: nrm = -nrm
        y.yuz_yon([p + Z * (TK / 2) for p in q], renk, nrm)
        y.yuz_yon([p - Z * (TK / 2) for p in q], 'koyu', -nrm)
# the cloth's rims (front and back edges, the two ends)
def rim(p, q, dis):
    y.yuz_yon([p + Z * (TK / 2), q + Z * (TK / 2), q - Z * (TK / 2), p - Z * (TK / 2)], 'koyu', dis)
for i in range(NU):
    rim(P[i][0], P[i + 1][0], -Y); rim(P[i][NV], P[i + 1][NV], Y)
for j in range(NV):
    rim(P[0][j], P[0][j + 1], -X); rim(P[NU][j], P[NU][j + 1], X)
# the back curtain down to the ground and the side walls (two-sided)
for i in range(NU):
    a, b = P[i][NV], P[i + 1][NV]
    levha([V(a.x, a.y, Z0), V(b.x, b.y, Z0), b - Z * 0.002, a - Z * 0.002], 'koyu', Y, t=0.004)
for s, i in ((-1, 0), (1, NU)):
    pts = [V(P[i][j].x, P[i][j].y, Z0) for j in range(NV // 2, NV + 1)] + [P[i][j] - Z * 0.002 for j in range(NV, NV // 2 - 1, -1)]
    levha(pts, 'koyu', X * s, t=0.004)
# poles and guy ropes
for k in range(NP):
    px = CX0 + (CX1 - CX0) * (k + 0.5) / NP
    vm = 0.55
    cubuk(y, V(px, CY0 + (CY1 - CY0) * vm, Z0), V(px, CY0 + (CY1 - CY0) * vm, zr - 0.002), 0.007, 'ahsap_acik')
for k in range(4):
    px = CX0 + (CX1 - CX0) * k / 3
    zz = cadir_z(k / 3, 0.0)
    cubuk(y, V(px, CY0, Z0), V(px, CY0, zz - 0.003), 0.006, 'ahsap_acik')
    cubuk(y, V(px, CY0, zz), V(px, CY0 - 0.07, Z0), 0.002, 'kumas')
for k in range(4):
    px = CX0 + (CX1 - CX0) * k / 3
    cubuk(y, V(px, CY1, Z0 + 0.06), V(px, CY1 + 0.07, Z0), 0.002, 'kumas')
# inside: carpets, cushions, the coffee hearth and pots
for (x0, x1, key, kn) in ((-0.9, -0.68, 'boya_kirmizi', 'lacivert'), (-0.65, -0.36, 'lacivert', 'boya_kirmizi')):
    kutu(y, V(x0, CY0 + 0.02, Z0), X, x1 - x0, 0.17, 0.003, key, 'onarkasagsolust')
    kutu(y, V(x0 + 0.012, CY0 + 0.032, Z0 + 0.003), X, x1 - x0 - 0.024, 0.146, 0.0012, kn, 'ust')
    kutu(y, V(x0 + 0.024, CY0 + 0.044, Z0 + 0.0042), X, x1 - x0 - 0.048, 0.122, 0.001, key, 'ust')
for x in (-0.88, -0.8, -0.72, -0.6, -0.5, -0.42):
    boru(y, [V(x - 0.03, CY0 + 0.16, Z0 + 0.016), V(x + 0.03, CY0 + 0.16, Z0 + 0.016)], 0.014, 'boya_kirmizi' if int(x * 100) % 2 else 'boya_sari', n=6)
HC = (-0.27, -0.88)
y.prizma(HC, 0.035, Z0, Z0 + 0.012, 'tas_koyu', n=8)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0125) for p in cokgen(HC, 0.025, 8)], 'koyu', Z)
for (dx, dy, key) in ((0.0, 0.0, 'bronz'), (0.045, 0.02, 'altin'), (0.04, -0.03, 'bronz')):
    donel(y, (HC[0] + dx, HC[1] + dy), [(0.0, Z0 + 0.012), (0.012, Z0 + 0.012), (0.014, Z0 + 0.025), (0.006, Z0 + 0.036), (0.004, Z0 + 0.046), (0.009, Z0 + 0.05), (0.0, Z0 + 0.05)], key, n=8)
    cubuk(y, V(HC[0] + dx + 0.01, HC[1] + dy, Z0 + 0.03), V(HC[0] + dx + 0.025, HC[1] + dy, Z0 + 0.046), 0.003, key)

# water skins on tripods and firewood by the tent
for (qx, qy) in ((-0.22, -0.78), (-0.16, -0.84)):
    for i in range(3):
        a = TAU * i / 3 + 0.4
        cubuk(y, V(qx + 0.03 * math.cos(a), qy + 0.03 * math.sin(a), Z0), V(qx, qy, Z0 + 0.1), 0.004, 'ahsap_koyu')
    donel(y, (qx, qy), [(0.0, Z0 + 0.03), (0.016, Z0 + 0.036), (0.02, Z0 + 0.055), (0.012, Z0 + 0.075), (0.004, Z0 + 0.085), (0.0, Z0 + 0.09)], 'ahsap', n=8)
for i in range(6):
    a = 0.3 + 0.25 * i
    cubuk(y, V(-0.3 + 0.004 * i, -0.66 - 0.004 * i, Z0 + 0.006 + 0.008 * (i % 3)), V(-0.18 + 0.004 * i, -0.68 - 0.004 * i, Z0 + 0.006 + 0.008 * (i % 3)), 0.008, 'ahsap' if i % 2 else 'ahsap_koyu', 0.008)
# clay jars for grain by the house
for (jx, jy) in ((0.12, HY0 - 0.04), (0.17, HY0 - 0.05), (0.145, HY0 - 0.09)):
    donel(y, (jx, jy), [(0.012, Z0), (0.022, Z0 + 0.02), (0.02, Z0 + 0.045), (0.01, Z0 + 0.058), (0.011, Z0 + 0.064), (0.0, Z0 + 0.064)], 'kiremit', n=8)

# ---------------- palms and the outside ----------------
y.bolum('Hurmalar, dış yalak')
for (tx, ty, b) in ((-1.05, -0.86, 0.34), (-0.18, -0.95, 0.3), (0.86, -0.97, 0.36), (1.04, -0.45, 0.3), (1.03, 0.3, 0.33),
                    (-0.98, 0.98, 0.3), (0.25, 0.3, 0.38), (-0.45, -0.25, 0.32), (0.7, -1.02, 0.28), (1.05, 0.95, 0.34), (0.3, -1.0, 0.3)):
    palmiye(tx, ty, Z0, boy=b)
yalak(0.4, 0.75, -0.8, -0.74)
deve(0.5, -0.92, math.pi / 2, renk='kaya', cul='turkuaz', yuk=True, egil=True)
y.yuz_yon([V(gx0, -1.08, Z0 + 0.002), V(gx1, -1.08, Z0 + 0.002), V(gx1, YF - 0.03, Z0 + 0.002), V(gx0, YF - 0.03, Z0 + 0.002)], 'kerpic_koyu', Z)

calistir(y, 'lm_deveagili')
