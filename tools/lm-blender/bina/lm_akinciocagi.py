# Akıncı Ocağı (lm_akinciocagi): the frontier post of the akıncı horsemen: a yard of packed earth fenced by a timber
# palisade on a stone footing with a roofed gate, long tiled stables open to the yard (posts, stalls, hay), the
# stone barracks with its hearth chimneys, a tall timber watchtower, the commander's otağ tent with the tuğ standards
# (horsetail plumes) and banners before it, bell tents, hitching rails, a fire with a cauldron and archery targets.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.035
XW, YF, YB = 1.0, -0.9, 0.9

y.bolum('Zemin: toprak avlu')
zemin(y, -XW - 0.12, XW + 0.12, YF - 0.16, YB + 0.1, Z0, 'tas_koyu', 'toprak', basamak=(('on', 0.36),), n_basamak=2)
# a stone-paved way from the gate to the tent
y.yuz_yon([V(-0.07, YF, Z0 + 0.003), V(0.07, YF, Z0 + 0.003), V(0.07, -0.22, Z0 + 0.003), V(-0.07, -0.22, Z0 + 0.003)], 'zemin', Z)


# ---------------- palisade ----------------
def cit(a, b, h=0.17, taban=0.05, adim=0.024):
    """a palisade a->b (outside to its right): a stone footing, pointed stakes, two rails on the inside"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    sur(y, [a, b], Z0, taban, 0.05, 'tas', mazgal_h=0, parapet_h=0.0001, ust_key='tas_acik')
    n = int(L / adim)
    for k in range(n + 1):
        p = a.lerp(b, k / n) - nn * 0.022
        hh = h * (1 + 0.06 * math.sin(k * 2.7))
        y.prizma((p.x, p.y), 0.0105, Z0 + taban, Z0 + taban + hh, 'kutuk', n=5, ust=False, kat=k * 0.7)
        y.koni((p.x, p.y), 0.0105, Z0 + taban + hh, 0.024, 'ahsap_koyu', n=5)
    for zz in (0.35, 0.8):
        cubuk(y, a - nn * 0.038 + Z * (Z0 + taban + h * zz), b - nn * 0.038 + Z * (Z0 + taban + h * zz), 0.008, 'ahsap_koyu', 0.006)


y.bolum('Ahşap çit ve taş temel')
GW = 0.13          # half the gate's width
cit((-XW, YF), (-GW, YF))
cit((GW, YF), (XW, YF))
cit((XW, YF), (XW, YB))
cit((XW, YB), (-XW, YB))
cit((-XW, YB), (-XW, YF))
for sx in (-1, 1):
    for yy in (YF, YB):
        y.prizma((sx * XW, yy), 0.024, Z0, Z0 + 0.25, 'kutuk', n=8)
        y.koni((sx * XW, yy), 0.026, Z0 + 0.25, 0.04, 'ahsap_koyu', n=8)

# ---------------- gate ----------------
y.bolum('Kapı')
GH = 0.27
for sx in (-1, 1):
    kutu_merkez(y, (sx * (GW + 0.01), YF - 0.02), 0.06, 0.08, 0.06, 'tas', z0=Z0)
    y.prizma((sx * (GW + 0.01), YF - 0.02), 0.018, Z0 + 0.06, Z0 + GH, 'kutuk', n=8)
cubuk(y, V(-GW - 0.05, YF - 0.02, Z0 + GH - 0.02), V(GW + 0.05, YF - 0.02, Z0 + GH - 0.02), 0.03, 'ahsap', 0.03)
cubuk(y, V(-GW - 0.03, YF - 0.02, Z0 + GH - 0.075), V(GW + 0.03, YF - 0.02, Z0 + GH - 0.075), 0.018, 'ahsap_koyu', 0.018)
# a board with carved border over the gate
kutu(y, V(-0.07, YF - 0.035, Z0 + GH - 0.065), X, 0.14, 0.006, 0.036, 'boya_kirmizi', 'onust')
kutu(y, V(-0.06, YF - 0.0375, Z0 + GH - 0.06), X, 0.12, 0.003, 0.026, 'altin', 'on')
cati_besik(y, -GW - 0.07, GW + 0.07, YF - 0.08, YF + 0.04, Z0 + GH, 0.07, 0.025, 'kiremit', 'kiremit2', kalinlik=0.01, ucluk_key='ahsap_dikey')
# the two leaves, swung open into the yard
for sx in (-1, 1):
    hinge = V(sx * GW, YF)
    d = V(-sx * 0.3, 1).normalized()
    for k in range(5):
        o = hinge + d * (k * GW / 5)
        kutu(y, o + Z * (Z0 + 0.01), d, GW / 5 - 0.002, 0.014, 0.2, 'ahsap_dikey')
    cubuk(y, hinge + Z * (Z0 + 0.06) + V(0, 0, 0), hinge + d * GW + Z * (Z0 + 0.06), 0.012, 'ahsap_koyu', 0.018)
    cubuk(y, hinge + Z * (Z0 + 0.17), hinge + d * GW + Z * (Z0 + 0.17), 0.012, 'ahsap_koyu', 0.018)


# ---------------- stables ----------------
def ahir(c, aci, L, D=0.26, H=0.15, n=8):
    """a long stable, open to the yard on its front (-y before turning): stone footing and plank walls, posts along
    the front with stall boards between, a ceiling, a tiled gable roof overhanging the front; hay in the stalls"""
    with parca(y, (c[0], c[1], 0), aci):
        x0, x1, y0, y1 = -L / 2, L / 2, -D / 2, D / 2
        for (p, q) in ((V(x1, y1), V(x0, y1)), (V(x0, y1), V(x0, y0)), (V(x1, y0), V(x1, y1))):
            duz_duvar(y, p, q, Z0, Z0 + 0.05, 'tas')
            duz_duvar(y, p, q, Z0 + 0.05, Z0 + H, 'ahsap_dikey')
            e = (q - p).normalized(); nn = V(e.y, -e.x)
            kutu(y, p + nn * 0.004 + Z * (Z0 + 0.048), e, (q - p).length, 0.004, 0.008, 'ahsap_koyu', 'onust')
        # inside faces (seen through the open front)
        for (p, q) in ((V(x0, y1), V(x1, y1)), (V(x0, y0), V(x0, y1)), (V(x1, y1), V(x1, y0))):
            duz_duvar(y, p, q, Z0, Z0 + H, 'ahsap_koyu')
        y.yuz_yon([V(x0, y0, Z0 + H), V(x1, y0, Z0 + H), V(x1, y1, Z0 + H), V(x0, y1, Z0 + H)], 'ahsap_koyu', -Z)
        y.yuz_yon([V(x0, y0, Z0 + 0.002), V(x1, y0, Z0 + 0.002), V(x1, y1, Z0 + 0.002), V(x0, y1, Z0 + 0.002)], 'saz_koyu', Z)
        # front posts, lintel, stall boards and partitions
        yf = y0 - 0.0
        for k in range(n + 1):
            x = x0 + L * k / n
            kutu_merkez(y, (x, yf), 0.018, 0.018, H + 0.004, 'ahsap', z0=Z0)
            if 0 < k < n:
                kutu_merkez(y, (x, (y0 + y1) / 2), 0.006, D * 0.95, 0.07, 'ahsap', z0=Z0)
        cubuk(y, V(x0 - 0.01, yf, Z0 + H - 0.012), V(x1 + 0.01, yf, Z0 + H - 0.012), 0.022, 'ahsap_koyu', 0.022)
        for k in range(n):
            xa, xb = x0 + L * k / n + 0.01, x0 + L * (k + 1) / n - 0.01
            if k % 3 != 1:
                kutu(y, V(xa, yf, Z0 + 0.012), X, xb - xa, 0.01, 0.045, 'ahsap_acik')
            # hay at the back of the stall and a manger
            xm = (xa + xb) / 2
            donel(y, (xm, y1 - 0.05), [(0.035, Z0), (0.03, Z0 + 0.02), (0.016, Z0 + 0.034), (0.0, Z0 + 0.038)], 'saz', n=8)
            kutu(y, V(xa + 0.01, y1 - 0.02, Z0 + 0.03), X, xb - xa - 0.02, 0.02, 0.02, 'ahsap')
        cati_besik(y, x0, x1, y0 - 0.05, y1, Z0 + H, 0.12, 0.03, 'kiremit', 'kiremit2', kalinlik=0.012, ucluk_key='ahsap_dikey',
                   alt_key='ahsap_koyu', uc_sacak=0.025)
        # (the roof's front slope reaches past the posts: close the gap above the lintel)


y.bolum('Ahırlar')
ahir((-0.82, 0.02), math.pi / 2, 1.3, n=9)       # west side, open to the east
ahir((-0.08, 0.74), 0.0, 0.95, n=7)            # back, open to the south

# ---------------- barracks with hearths ----------------
y.bolum('Ocak: taş kışla ve bacalar')
with parca(y, (0.84, -0.12, 0), math.pi / 2):
    L, D, H = 0.86, 0.24, 0.17
    k = dikdortgen(-L / 2, L / 2, -D / 2, D / 2)
    kutu(y, V(-L / 2 - 0.01, -D / 2 - 0.01, Z0), X, L + 0.02, D + 0.02, 0.02, 'tas_koyu', 'onarkasagsolust')
    zb = Z0 + 0.02
    # the yard front (-y here, west after turning): doors and windows; the other sides plain with small windows
    n = 6
    for j in range(n):
        p, q = k[0].lerp(k[1], j / n), k[0].lerp(k[1], (j + 1) / n)
        if j in (1, 4):
            kapi(y, p, q, zb, 0.5, H, ('tas', 'tas_koyu', 'tas_acik', 'ahsap'), sivri=0.0, derin=0.02, cerceve=(0.006, 'tas_acik'))
        else:
            dikdortgen_acik(y, p, q, zb, H, 0.3, 0.7, H * 0.35, H * 0.75, ('tas', 'tas_koyu', 'tas_acik', 'cam'), derin=0.015,
                            cerceve=(0.005, 'ahsap'))
            kafes(y, p, q, zb, 0.3, 0.7, H * 0.35, H * 0.75, 'ahsap_koyu', 3, 2, 0.004, 0.006)
    for i in (1, 2, 3):
        a, b = k[i], k[(i + 1) % 4]
        m = max(1, int((b - a).length / 0.15))
        for j in range(m):
            p, q = a.lerp(b, j / m), a.lerp(b, (j + 1) / m)
            dikdortgen_acik(y, p, q, zb, H, 0.38, 0.62, H * 0.5, H * 0.75, ('tas', 'tas_koyu', 'tas_acik', 'koyu'), derin=0.012)
    silme(y, k, zb + H - 0.01, 0.012, 0.012, 'ahsap_koyu', 'duz')
    # a timber eave on brackets along the yard front
    for j in range(n + 1):
        p = k[0].lerp(k[1], j / n)
        cubuk(y, p + V(0, 0, zb + H - 0.03), p + V(0, -0.045, zb + H - 0.004), 0.01, 'ahsap_koyu')
    cati_kirma(y, -L / 2, L / 2, -D / 2, D / 2, zb + H, 0.12, 0.045, 'kiremit', 'kiremit2', alt_key='ahsap_koyu')
    for x in (-0.28, 0.0, 0.28):
        kutu_merkez(y, (x, 0.05), 0.04, 0.04, 0.18, 'tas', z0=zb + H + 0.02)
        kutu_merkez(y, (x, 0.05), 0.054, 0.054, 0.012, 'tas_acik', z0=zb + H + 0.2)
        kutu_merkez(y, (x, 0.05), 0.026, 0.026, 0.012, 'koyu', z0=zb + H + 0.212, yuzler='onarkasagsol')
        cati_kirma(y, x - 0.022, x + 0.022, 0.028, 0.072, zb + H + 0.224, 0.02, 0.006, 'kiremit', alt_key='ahsap_koyu')
        for sx in (-1, 1):
            for sy in (-1, 1):
                y.prizma((x + sx * 0.02, 0.05 + sy * 0.02), 0.003, zb + H + 0.212, zb + H + 0.226, 'tas', n=4)

# ---------------- watchtower ----------------
y.bolum('Gözcü kulesi')
TC = (0.8, 0.7)
TH = 0.62
w0, w1 = 0.1, 0.075
def kp(sx, sy, z):
    t = (z - Z0) / TH
    w = w0 + (w1 - w0) * t
    return V(TC[0] + sx * w, TC[1] + sy * w, z)
for sx in (-1, 1):
    for sy in (-1, 1):
        kutu_merkez(y, (kp(sx, sy, Z0).x, kp(sx, sy, Z0).y), 0.04, 0.04, 0.04, 'tas', z0=Z0)
        boru(y, [kp(sx, sy, Z0 + 0.04), kp(sx, sy, Z0 + TH + 0.13)], 0.011, 'kutuk', n=6)
# braces in three levels on every side
kose = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
for lv in range(3):
    za, zb_ = Z0 + 0.05 + lv * TH / 3, Z0 + 0.05 + (lv + 1) * TH / 3 - 0.02
    for i in range(4):
        (ax, ay), (bx, by) = kose[i], kose[(i + 1) % 4]
        cubuk(y, kp(ax, ay, za), kp(bx, by, zb_), 0.008, 'ahsap', 0.008)
        cubuk(y, kp(bx, by, za), kp(ax, ay, zb_), 0.008, 'ahsap', 0.008)
        cubuk(y, kp(ax, ay, zb_ + 0.01), kp(bx, by, zb_ + 0.01), 0.01, 'ahsap_koyu', 0.01)
# platform, railing, roof
zp = Z0 + TH
pw = 0.13
kutu_merkez(y, TC, 2 * pw, 2 * pw, 0.02, 'ahsap', z0=zp)
for i in range(4):
    (ax, ay), (bx, by) = kose[i], kose[(i + 1) % 4]
    a, b = V(TC[0] + ax * pw, TC[1] + ay * pw), V(TC[0] + bx * pw, TC[1] + by * pw)
    for k in range(5):
        p = a.lerp(b, k / 5)
        cubuk(y, p + Z * (zp + 0.02), p + Z * (zp + 0.07), 0.006, 'ahsap_koyu')
    cubuk(y, a + Z * (zp + 0.07), b + Z * (zp + 0.07), 0.009, 'ahsap', 0.007)
    cubuk(y, a + Z * (zp + 0.045), b + Z * (zp + 0.045), 0.005, 'ahsap', 0.005)
cati_kirma(y, TC[0] - w1, TC[0] + w1, TC[1] - w1, TC[1] + w1, zp + 0.13, 0.12, 0.07, 'kiremit', 'kiremit2', alt_key='ahsap_koyu')
# a ladder up the yard side
lx0 = TC[0] - 0.03
for sx in (0, 0.06):
    cubuk(y, V(lx0 + sx, TC[1] - 0.2, Z0), V(lx0 + sx, TC[1] - w1 - 0.01, zp + 0.02), 0.007, 'ahsap')
for k in range(1, 12):
    t = k / 12
    p = V(lx0, TC[1] - 0.2, Z0).lerp(V(lx0, TC[1] - w1 - 0.01, zp + 0.02), t)
    cubuk(y, p, p + V(0.06, 0, 0), 0.005, 'ahsap_koyu')
sancak(y, TC[0], TC[1], zp + 0.13 + 0.12, boy=0.16, en=0.11, yuk=0.07, aci=-0.4)

# ---------------- the otağ and the tuğ standards ----------------
y.bolum('Otağ çadırı ve tuğlar')
OC = (0.12, 0.12)
y.yuz_yon([V(OC[0] - 0.27, OC[1] - 0.27, Z0 + 0.004), V(OC[0] + 0.27, OC[1] - 0.27, Z0 + 0.004), V(OC[0] + 0.27, OC[1] + 0.27, Z0 + 0.004),
           V(OC[0] - 0.27, OC[1] + 0.27, Z0 + 0.004)], 'boya_kirmizi', Z)        # a carpet before / under the tent

def otag(c, W=0.21, D=0.15, H=0.12):
    """an Ottoman otağ (the commander's pavilion): a rectangular tent of white cloth with a red skirt and red
    appliqué arches round its walls, a hipped roof of striped cloth on two poles with gilded finials, a scalloped
    valance along the eaves, a door with the flaps tied back and guy ropes to pegs"""
    cx, cy = c
    k = dikdortgen(cx - W, cx + W, cy - D, cy + D)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
        duz_duvar(y, a, b, Z0, Z0 + 0.022, 'boya_kirmizi')
        duz_duvar(y, a, b, Z0 + 0.022, Z0 + H, 'kumas')
        kutu(y, a + Z * (Z0 + H - 0.014) + nn * 0.002, e, L, 0.002, 0.012, 'boya_kirmizi', 'on')
        n = max(2, int(L / 0.07))
        for j in range(n):
            if i == 0 and j in (n // 2 - (1 if n % 2 == 0 else 0), n // 2): continue
            m = a + e * (L * (j + 0.5) / n)
            ww, hh = L / n * 0.55, H * 0.62
            arc = [(-ww / 2, 0)] + kemer_yolu(-ww / 2, ww / 2, hh - ww * 0.6, 0.6, 8) + [(ww / 2, 0)]
            y.yuz_yon([m + e * u + Z * (Z0 + 0.03 + v) + nn * 0.002 for u, v in arc], 'boya_kirmizi', nn)
            arc2 = [(-ww / 2 + 0.006, 0.006)] + kemer_yolu(-ww / 2 + 0.006, ww / 2 - 0.006, hh - ww * 0.6, 0.6, 8)[1:-1] + [(ww / 2 - 0.006, 0.006)]
            y.yuz_yon([m + e * u + Z * (Z0 + 0.03 + v) + nn * 0.003 for u, v in arc2], 'boya_sari', nn)
    # the door on the front (-y): a dark opening, the flaps tied back
    dw = 0.07
    y.yuz_yon([V(cx - dw / 2, cy - D - 0.003, Z0), V(cx + dw / 2, cy - D - 0.003, Z0), V(cx + dw / 2, cy - D - 0.003, Z0 + H * 0.85), V(cx - dw / 2, cy - D - 0.003, Z0 + H * 0.85)], 'koyu', -Y)
    for sx in (-1, 1):
        x0 = cx + sx * dw / 2
        y.yuz_yon([V(x0, cy - D - 0.005, Z0 + H * 0.85), V(x0 + sx * 0.03, cy - D - 0.005, Z0 + H * 0.85), V(x0 + sx * 0.012, cy - D - 0.005, Z0 + 0.01)], 'boya_kirmizi', -Y)
    # the roof
    zr = cati_kirma(y, cx - W, cx + W, cy - D, cy + D, Z0 + H, 0.1, 0.025, 'kumas', 'boya_kirmizi', kalinlik=0.006, kivrim=0.35,
                    alt_key='boya_kirmizi', ns=8, nr=6, mahya_en=0.008, dilim=['kumas', 'kece'])
    # scalloped valance hanging from the eaves (both faces)
    a_, b_ = W + 0.025, D + 0.025
    ek = [V(cx - a_, cy - b_), V(cx + a_, cy - b_), V(cx + a_, cy + b_), V(cx - a_, cy + b_)]
    for i in range(4):
        a, b = ek[i], ek[(i + 1) % 4]
        L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
        n = int(L / 0.03)
        zt = Z0 + H - 0.006
        for j in range(n):
            p, q = a + e * (L * j / n), a + e * (L * (j + 1) / n)
            pts = [p + Z * zt, q + Z * zt] + [p.lerp(q, t) + Z * (zt - 0.016 * math.sin(math.pi * t)) for t in (0.8, 0.5, 0.2)]
            pts = [pp + nn * 0.001 for pp in pts]
            y.yuz_yon(pts, 'boya_kirmizi' if j % 2 else 'boya_sari', nn)
            y.yuz_yon(pts, 'boya_kirmizi', -nn)
    # poles and finials above the ridge
    for sx in (-1, 1):
        px = cx + sx * (W - D) * 0.9
        y.prizma((px, cy), 0.005, zr - 0.01, zr + 0.05, 'ahsap_koyu', n=6)
        kure(y, (px, cy, zr + 0.06), 0.012, 'altin', n=10, kat=5)
        y.koni((px, cy), 0.005, zr + 0.07, 0.03, 'altin', n=6)
    # guy ropes and pegs
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = V(cx + sx * a_, cy + sy * b_, Z0 + H - 0.008)
            g = V(cx + sx * (a_ + 0.06), cy + sy * (b_ + 0.06), Z0)
            boru(y, [p, g], 0.0018, 'ahsap_koyu', n=4)
            y.prizma((g.x, g.y), 0.004, Z0, Z0 + 0.012, 'ahsap', n=4)


otag(OC)
# an awning on poles before the door
cubuk(y, V(OC[0] - 0.09, OC[1] - 0.29, Z0), V(OC[0] - 0.09, OC[1] - 0.29, Z0 + 0.13), 0.007, 'ahsap_koyu')
cubuk(y, V(OC[0] + 0.09, OC[1] - 0.29, Z0), V(OC[0] + 0.09, OC[1] - 0.29, Z0 + 0.13), 0.007, 'ahsap_koyu')
for s, key in ((1, 'boya_kirmizi'), (-1, 'kece')):
    y.yuz_yon([V(OC[0] - 0.1, OC[1] - 0.3, Z0 + 0.13), V(OC[0] + 0.1, OC[1] - 0.3, Z0 + 0.13), V(OC[0] + 0.1, OC[1] - 0.18, Z0 + 0.15),
               V(OC[0] - 0.1, OC[1] - 0.18, Z0 + 0.15)], key, Z * s)


def tug(x, yy, boy=0.42, renk='koyu'):
    """a tuğ: a tall pole on a stone foot, a gilded ball and spike, a horsetail plume hanging below"""
    y.prizma((x, yy), 0.02, Z0, Z0 + 0.025, 'tas', n=8)
    y.prizma((x, yy), 0.0055, Z0 + 0.025, Z0 + boy, 'ahsap', n=6)
    t = Z0 + boy
    # the horsetail: a cluster of hair hanging from the cap, flaring towards its ragged end; a red tuft at the top
    donel(y, (x, yy), [(0.03, t - 0.19), (0.032, t - 0.17), (0.026, t - 0.11), (0.016, t - 0.06), (0.008, t - 0.035), (0.0, t - 0.03)], renk, n=12,
          dilim=[renk, 'ahsap_koyu' if renk == 'koyu' else 'kece'])
    donel(y, (x, yy), [(0.006, t - 0.04), (0.016, t - 0.036), (0.014, t - 0.026), (0.0, t - 0.02)], 'boya_kirmizi', n=10)
    y.prizma((x, yy), 0.012, t - 0.03, t - 0.02, 'altin', n=8)
    kure(y, (x, yy, t + 0.004), 0.014, 'altin', n=10, kat=5)
    y.koni((x, yy), 0.006, t + 0.016, 0.04, 'altin', n=6)


for k, x in enumerate((-0.1, 0.12, 0.34)):
    tug(OC[0] + x - 0.12, OC[1] - 0.42, boy=0.44 if k == 1 else 0.38, renk='beyaz' if k == 1 else 'koyu')
sancak(y, OC[0] - 0.33, OC[1] - 0.12, Z0, boy=0.36, en=0.13, yuk=0.08, aci=0.2, kuyruk=True)
sancak(y, OC[0] + 0.33, OC[1] - 0.12, Z0, boy=0.36, en=0.13, yuk=0.08, aci=0.2, kuyruk=True)

# ---------------- yard life ----------------
y.bolum('Avlu: çadırlar, bağlama direkleri, ocak, nişan')
for (cx, cy, r, sk) in ((0.48, 0.42, 0.075, 'boya_kirmizi'), (0.55, 0.18, 0.065, 'boya_yesil'), (-0.3, 0.45, 0.07, 'boya_yesil')):
    with parca(y, (cx, cy, Z0)):
        cadir(y, (0, 0), r, r * 1.7, key='kumas', serit_key=sk, n=16)
# a spear rack: a bar on two posts with lances leaning on it, pennons on their heads
for sx in (-1, 1):
    y.prizma((-0.2 + sx * 0.09, -0.66), 0.006, Z0, Z0 + 0.1, 'ahsap_koyu', n=5)
cubuk(y, V(-0.3, -0.66, Z0 + 0.095), V(-0.1, -0.66, Z0 + 0.095), 0.008, 'ahsap', 0.008)
for k in range(7):
    x = -0.28 + k * 0.027
    a, b = V(x, -0.63, Z0), V(x + 0.004, -0.67, Z0 + 0.22)
    cubuk(y, a, b, 0.004, 'ahsap')
    y.koni((b.x, b.y), 0.005, b.z, 0.022, 'demir', n=4)
    if k % 2 == 0:
        y.yuz_yon([b - Z * 0.004, b - Z * 0.022, b + V(0.03, 0.0, -0.016)], 'boya_kirmizi', -Y)
        y.yuz_yon([b - Z * 0.004, b - Z * 0.022, b + V(0.03, 0.0, -0.016)], 'boya_kirmizi', Y)
# firewood stacked by the fire
for k in range(3):
    for j in range(4 - k):
        z = Z0 + 0.008 + k * 0.014
        yy = -0.42 + (j - (3 - k) / 2) * 0.016
        boru(y, [V(0.3, yy, z), V(0.38, yy, z)], 0.007, 'kutuk', n=6)
# hitching rails before the west stable
for (x, ya, yb) in ((-0.55, -0.55, -0.15), (-0.55, 0.05, 0.42)):
    for k in range(5):
        yy = ya + (yb - ya) * k / 4
        y.prizma((x, yy), 0.008, Z0, Z0 + 0.075, 'kutuk', n=6)
    cubuk(y, V(x, ya, Z0 + 0.065), V(x, yb, Z0 + 0.065), 0.008, 'ahsap', 0.008)
    kutu(y, V(x + 0.065, ya, Z0), Y, yb - ya, 0.035, 0.03, 'ahsap', 'onarkasagsol')      # a water trough
    y.yuz_yon([V(x + 0.032, ya + 0.004, Z0 + 0.025), V(x + 0.062, ya + 0.004, Z0 + 0.025), V(x + 0.062, yb - 0.004, Z0 + 0.025),
               V(x + 0.032, yb - 0.004, Z0 + 0.025)], 'su', Z)
# the fire with a cauldron on a tripod
FC = (0.42, -0.3)
for k in range(8):
    a = TAU * k / 8
    kutu_merkez(y, (FC[0] + 0.05 * math.cos(a), FC[1] + 0.05 * math.sin(a)), 0.022, 0.018, 0.015, 'tas_koyu', z0=Z0, aci=a)
for k in range(5):
    a = TAU * k / 5
    cubuk(y, V(FC[0] + 0.025 * math.cos(a), FC[1] + 0.025 * math.sin(a), Z0 + 0.006), V(FC[0] - 0.02 * math.cos(a), FC[1] - 0.02 * math.sin(a), Z0 + 0.02), 0.007, 'ahsap_koyu')
donel(y, FC, [(0.0, Z0 + 0.008), (0.018, Z0 + 0.014), (0.0, Z0 + 0.05)], 'boya_sari', n=7)
donel(y, FC, [(0.0, Z0 + 0.05), (0.028, Z0 + 0.055), (0.036, Z0 + 0.075), (0.034, Z0 + 0.095), (0.03, Z0 + 0.095)], 'demir', n=12)
y.yuz_yon([V(FC[0] + 0.03 * math.cos(TAU * i / 12), FC[1] + 0.03 * math.sin(TAU * i / 12), Z0 + 0.09) for i in range(12)], 'kirmizi', Z)
for k in range(3):
    a = TAU * k / 3 + 0.4
    cubuk(y, V(FC[0] + 0.07 * math.cos(a), FC[1] + 0.07 * math.sin(a), Z0), V(FC[0], FC[1], Z0 + 0.16), 0.006, 'ahsap')
# archery targets
for (tx, ty) in ((0.55, -0.66), (0.75, -0.66)):
    for sx in (-1, 1):
        cubuk(y, V(tx + sx * 0.03, ty + 0.02, Z0), V(tx + sx * 0.022, ty, Z0 + 0.1), 0.006, 'ahsap')
    for k, (r, key) in enumerate(((0.045, 'saz'), (0.032, 'beyaz'), (0.02, 'boya_kirmizi'), (0.009, 'altin'))):
        c = V(tx, ty - 0.008 - k * 0.002, Z0 + 0.09)
        y.yuz_yon([c + X * (r * math.cos(TAU * i / 16)) + Z * (r * math.sin(TAU * i / 16)) for i in range(16)], key, -Y)
    c = V(tx, ty, Z0 + 0.09)
    y.yuz_yon([c + X * (0.045 * math.cos(TAU * i / 16)) + Z * (0.045 * math.sin(TAU * i / 16)) for i in range(16)], 'saz_koyu', Y)
    rim = [c + X * (0.045 * math.cos(TAU * i / 16)) + Z * (0.045 * math.sin(TAU * i / 16)) for i in range(16)]
    for i in range(16):
        p, q = rim[i], rim[(i + 1) % 16]
        y.yuz_yon([p, q, q - Y * 0.008, p - Y * 0.008], 'saz', (p + q) / 2 - c)


def at(x, yy, aci, renk='ahsap', yele='koyu', eyer='boya_kirmizi'):
    """a small stylised horse (head towards +x before turning): barrel body, neck and head, four legs, mane, tail and
    a saddle cloth"""
    with parca(y, (x, yy, Z0), aci):
        h = 0.05                                    # the legs' length
        boru(y, [V(-0.04, 0, h + 0.012), V(-0.015, 0, h + 0.016), V(0.015, 0, h + 0.017), V(0.038, 0, h + 0.014)], 0.017, renk, n=8)
        kure(y, (-0.04, 0, h + 0.013), 0.017, renk, n=8, kat=4)
        kure(y, (0.038, 0, h + 0.015), 0.016, renk, n=8, kat=4)
        boru(y, [V(0.04, 0, h + 0.018), V(0.058, 0, h + 0.045)], 0.01, renk, n=6, r_son=0.008)            # neck
        boru(y, [V(0.056, 0, h + 0.05), V(0.08, 0, h + 0.035)], 0.008, renk, n=6, r_son=0.0055)          # head
        for s in (-1, 1):
            cubuk(y, V(0.058, s * 0.004, h + 0.056), V(0.06, s * 0.004, h + 0.066), 0.003, renk)          # ears
        boru(y, [V(0.036, 0, h + 0.03), V(0.052, 0, h + 0.058)], 0.004, yele, n=4)                      # mane
        boru(y, [V(-0.055, 0, h + 0.022), V(-0.064, 0, h + 0.0), V(-0.062, 0, h - 0.025)], 0.006, yele, n=5, r_son=0.003)
        for lx in (-0.038, 0.032):
            for s in (-1, 1):
                cubuk(y, V(lx, s * 0.009, h + 0.006), V(lx + 0.002, s * 0.009, 0.004), 0.007, renk, 0.008)
                kutu_merkez(y, (lx + 0.003, s * 0.009), 0.009, 0.008, 0.006, 'koyu')
        kutu_merkez(y, (-0.002, 0), 0.034, 0.04, 0.004, eyer, z0=h + 0.028)
        kutu_merkez(y, (-0.002, 0), 0.026, 0.026, 0.006, 'ahsap_koyu', z0=h + 0.031)
# hay stacks and a cart by the barracks
for (hx, hy) in ((0.62, -0.05), (-0.5, 0.62)):
    donel(y, (hx, hy), [(0.06, Z0), (0.062, Z0 + 0.04), (0.045, Z0 + 0.08), (0.02, Z0 + 0.1), (0.0, Z0 + 0.105)], 'saz', n=12)
    y.prizma((hx, hy), 0.003, Z0 + 0.1, Z0 + 0.13, 'ahsap_koyu', n=4)

y.bolum('Atlar')
for (hx, hy, ha, hr) in ((-0.43, -0.45, math.pi, 'ahsap'), (-0.43, -0.27, math.pi, 'beyaz'), (-0.43, 0.15, math.pi, 'koyu'), (-0.43, 0.32, math.pi, 'ahsap_acik'), (0.2, -0.62, 2.2, 'ahsap')):
    at(hx, hy, ha, hr, yele='beyaz' if hr == 'koyu' else 'koyu')

calistir(y, 'lm_akinciocagi')
