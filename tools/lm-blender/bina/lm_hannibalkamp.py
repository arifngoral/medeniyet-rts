# Hannibal'ın Ordugâhı (lm_hannibalkamp): Hannibal's army encamped at the foot of the Alps: a stake palisade with a
# gate between wooden watch towers, the general's great red pavilion on a dais with standards, rows of Carthaginian
# ridge tents, Iberian bell tents and Numidian mapalia huts, war elephants at a picket line, Numidian horses, carts,
# campfires; behind, the mountains rise to snowy peaks.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kartaca_ortak import tanit_heykel, insan, pencere_kutu, levha_kapali
from kartaca_ek import *
from bina_ortak import calistir
from hint_ortak import fil as fil_h
import doku

y = Yapi()
rn = random.Random(17)
Z0 = 0.04
GX0, GX1, GY0, GY1 = -1.2, 1.2, -1.15, 1.15
NX, NY = 48, 46
TEPE = [(0.35, 0.8, 0.98, 0.48, 0.36), (-0.58, 0.85, 0.7, 0.42, 0.32), (0.92, 0.66, 0.55, 0.3, 0.34), (-0.98, 0.6, 0.42, 0.26, 0.3)]   # x, y, h, rx, ry
YOL = [(0.0, 0.2), (0.06, 0.36), (-0.1, 0.48), (-0.02, 0.6), (-0.18, 0.7), (-0.1, 0.82), (-0.14, 0.96), (-0.08, 1.12)]   # the army's track up the pass


def yol_uzak(x, yy):
    best = 9.0
    for (ax, ay), (bx, by) in zip(YOL, YOL[1:]):
        dx, dy = bx - ax, by - ay
        t = max(0.0, min(1.0, ((x - ax) * dx + (yy - ay) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(x - ax - dx * t, yy - ay - dy * t))
    return best


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def yuk(x, yy):
    h = 0.0
    for cx, cy, hh, rx, ry in TEPE:
        d2 = ((x - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        h = max(h, hh * math.exp(-d2 * 1.1))
    h = max(h, 0.4 * _ss(0.3, 0.8, yy) * (0.8 + 0.2 * math.sin(x * 3.1 + 0.5)))    # the range joining the peaks
    h *= (1 - 0.88 * _ss(0.86, 1.15, yy)) * (1 - 0.75 * _ss(1.0, 1.2, abs(x)))   # (falling away at the edges: the cut stays low)
    # crags: sharper ridges on the high slopes
    h += 0.04 * _ss(0.15, 0.5, h) * (math.sin(x * 11 + yy * 4) * math.cos(yy * 9 - x * 3))
    # the camp ground stays almost flat
    m = _ss(0.12, 0.42, yy)
    return Z0 + h * m + 0.006 * math.sin(x * 5 + 1) * math.cos(yy * 4) * (1 - m)


# ---------------- terrain: the camp meadow, the mountains, the snow ----------------
y.bolum('Arazi ve dağlar')


def arazi_renk(x, yy, z):
    e = 0.012
    gx = (yuk(x + e, yy) - yuk(x - e, yy)) / (2 * e)
    gy = (yuk(x, yy + e) - yuk(x, yy - e)) / (2 * e)
    s = math.hypot(gx, gy)
    h = z - Z0
    n = math.sin(x * 4.3 + 1.1) * math.cos(yy * 3.7 - 0.6) * 0.7 + math.sin(x * 9.1 - yy * 6.3 + 2.0) * 0.3
    c = tuple(p + (q - p) * (0.5 + 0.5 * n) for p, q in zip((0.45, 0.52, 0.28), (0.53, 0.53, 0.32)))       # meadow
    camp = (1 - _ss(-0.02, 0.06, max(abs(x) - 1.0, yy - 0.22, -0.98 - yy)))
    c = tuple(p + (q - p) * 0.55 * camp * (0.6 + 0.4 * n) for p, q in zip(c, (0.6, 0.53, 0.38)))          # trampled earth
    c = tuple(p + (q - p) * _ss(0.05, 0.2, h + 0.03 * n) for p, q in zip(c, (0.42, 0.47, 0.33)))           # alpine scrub
    c = tuple(p + (q - p) * max(_ss(0.18, 0.36, h + 0.04 * n), _ss(1.4, 2.2, s)) for p, q in zip(c, (0.6, 0.57, 0.53)))   # rock
    c = tuple(p + (q - p) * _ss(0.5, 0.6, h + 0.06 * n - 0.05 * _ss(1.6, 2.6, s)) for p, q in zip(c, (0.95, 0.96, 0.97)))   # snow
    c = tuple(p + (q - p) * 0.75 * (1 - _ss(0.008, 0.03, yol_uzak(x, yy))) * _ss(0.2, 0.3, yy) for p, q in zip(c, (0.6, 0.53, 0.42)))   # the track
    return c


doku.KOSE_RENK['toprak_ot'] = arazi_renk
P = [[V(GX0 + (GX1 - GX0) * i / NX, GY0 + (GY1 - GY0) * j / NY, 0) for j in range(NY + 1)] for i in range(NX + 1)]
for i in range(NX + 1):
    for j in range(NY + 1):
        P[i][j].z = yuk(P[i][j].x, P[i][j].y)
for i in range(NX):
    for j in range(NY):
        q = [P[i][j], P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]]
        dg = (q[0].z + q[2].z) < (q[1].z + q[3].z)      # (split along the lower diagonal: ridges stay ridges)
        for tri in (([q[0], q[1], q[2]], [q[0], q[2], q[3]]) if dg else ([q[0], q[1], q[3]], [q[1], q[2], q[3]])):
            y.yuz_yon(tri, 'toprak_ot', Z)
kenar = [P[i][0] for i in range(NX)] + [P[NX][j] for j in range(NY)] + [P[i][NY] for i in range(NX, 0, -1)] + [P[0][j] for j in range(NY, 0, -1)]
for k in range(len(kenar)):
    a, b = kenar[k], kenar[(k + 1) % len(kenar)]
    e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
    sa, sb = 0.015 * math.sin(a.x * 7 + a.y * 5), 0.015 * math.sin(b.x * 7 + b.y * 5)
    m1a, m1b = min(a.z - 0.015, 0.02 + sa), min(b.z - 0.015, 0.02 + sb)
    y.yuz_yon([V(a.x, a.y, m1a), V(b.x, b.y, m1b), V(b.x, b.y, b.z), V(a.x, a.y, a.z)], 'toprak', nn)
    if a.z > 0.1 or b.z > 0.1:   # strata in the mountain's cut
        m2a, m2b = max(m1a, min(a.z - 0.02, 0.2 + sa * 2)), max(m1b, min(b.z - 0.02, 0.2 + sb * 2))
        y.yuz_yon([V(a.x, a.y, m2a), V(b.x, b.y, m2b), V(b.x, b.y, b.z - 0.015), V(a.x, a.y, a.z - 0.015)], 'kaya', nn)
        y.yuz_yon([V(a.x, a.y, m1a), V(b.x, b.y, m1b), V(b.x, b.y, m2b), V(a.x, a.y, m2a)], 'kaya_koyu', nn)
    y.yuz_yon([V(a.x, a.y, 0), V(b.x, b.y, 0), V(b.x, b.y, m1b), V(a.x, a.y, m1a)], 'kaya_koyu', nn)
# pines on the lower slopes, a few boulders
for k in range(110):
    x, yy = rn.uniform(-1.15, 1.15), rn.uniform(0.25, 1.1)
    h = yuk(x, yy) - Z0
    if not (0.03 < h < 0.38): continue
    agac(y, x, yy, yuk(x, yy) - 0.004, rn.uniform(0.1, 0.16), 'servi', 'yesil_koyu', 'ahsap_koyu')
for k in range(14):
    x, yy = rn.uniform(-1.15, 1.15), rn.uniform(-1.1, 0.6)
    if abs(x) < 1.05 and -1.02 < yy < 0.27: continue
    kure(y, (x, yy, yuk(x, yy) - 0.004), rn.uniform(0.012, 0.03), rn.choice(('kaya', 'kaya_koyu')), n=7, kat=4)

# ---------------- the palisade, the gate and its towers ----------------
y.bolum('Palisad ve kapı')
CX0, CX1, CY0, CY1 = -1.06, 1.06, -1.0, 0.26
GA, GB = -0.09, 0.09
palisad(y, [(-0.07, CY1), (CX0, CY1), (CX0, CY0), (GA, CY0)], yuk, h=0.07, tohum=3)
palisad(y, [(GB, CY0), (CX1, CY0), (CX1, CY1), (0.07, CY1)], yuk, h=0.07, tohum=4)
for x in (GA - 0.05, GB + 0.05):   # watch towers: four posts, braces, a platform with a rail, a roof of hides
    zb = yuk(x, CY0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cubuk(y, V(x + sx * 0.03, CY0 + sy * 0.03, zb - 0.005), V(x + sx * 0.026, CY0 + sy * 0.026, zb + 0.2), 0.008, 'kutuk')
    for sx in (-1, 1):
        cubuk(y, V(x + sx * 0.03, CY0 - 0.03, zb + 0.01), V(x - sx * 0.03, CY0 - 0.03, zb + 0.12), 0.005, 'ahsap_koyu')
    kutu_merkez(y, (x, CY0), 0.08, 0.08, 0.01, 'ahsap_acik', z0=zb + 0.13)
    for k in range(4):
        a = TAU * k / 4 + math.pi / 4
        c0 = V(x, CY0) + V(math.cos(a), math.sin(a)) * 0.0566
        c1 = V(x, CY0) + V(math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)) * 0.0566
        cubuk(y, c0 + Z * (zb + 0.165), c1 + Z * (zb + 0.165), 0.006, 'ahsap')
    cati_kirma(y, x - 0.04, x + 0.04, CY0 - 0.04, CY0 + 0.04, zb + 0.2, 0.05, sacak=0.015, key='saz_koyu', alt_key='ahsap_koyu', ns=4, nr=3,
               kalinlik=0.006)
    insan(y, x, CY0, zb + 0.14, 'boya_kirmizi', s=1.1, aci=-math.pi / 2, mizrak='bronz')
    sancak(y, x + 0.035, CY0 - 0.035, zb + 0.25, boy=0.13, en=0.09, yuk=0.055, aci=-1.1)
cubuk(y, V(GA - 0.02, CY0, yuk(0, CY0) + 0.11), V(GB + 0.02, CY0, yuk(0, CY0) + 0.11), 0.012, 'kutuk')
for x in (-0.04, 0.04):   # guards at the gate
    insan(y, x, CY0 - 0.05, yuk(x, CY0 - 0.05), 'boya_kirmizi', s=1.15, aci=-math.pi / 2, kalkan='bronz', mizrak='bronz')

# ---------------- the general's pavilion ----------------
y.bolum('Komutan çadırı')
KX, KY = 0.0, -0.1
KZ = yuk(KX, KY) + 0.028
kutu_merkez(y, (KX, KY), 0.62, 0.5, KZ - Z0 + 0.012, 'kum_koyu', z0=Z0 - 0.012)
silme(y, dikdortgen(KX - 0.31, KX + 0.31, KY - 0.25, KY + 0.25), KZ - 0.006, 0.006, 0.005, 'kum_acik', 'duz')
merdiven(y, (KX, KY - 0.25 - 0.05), math.pi / 2, 0.16, Z0 - 0.004, KZ, n=3, d=0.05 / 3 + 0.0001, key='kum_koyu')
TW, TD, TH = 0.46, 0.3, 0.15
tk = dikdortgen(KX - TW / 2, KX + TW / 2, KY - TD / 2 + 0.04, KY + TD / 2 + 0.04)
for i in range(4):   # the walls: cloth in vertical widths, red and dark lacquer red by turns
    a, b = tk[i], tk[(i + 1) % 4]
    nw = max(2, int(round((b - a).length / 0.046)))
    for k in range(nw):
        duz_duvar(y, a.lerp(b, k / nw), a.lerp(b, (k + 1) / nw), KZ, KZ + TH, 'boya_kirmizi' if k % 2 == 0 else 'lake')
for p in tk:   # gilded corner poles
    c = p + (p - V(KX, KY + 0.04)).normalized() * 0.006
    y.prizma((c.x, c.y), 0.0055, KZ, KZ + TH + 0.006, 'ahsap_koyu', n=6, ust=False)
    kure(y, (c.x, c.y, KZ + TH + 0.006), 0.008, 'altin', n=6, kat=3)
for zz, kk in ((KZ + 0.004, 'altin'), (KZ + TH * 0.55, 'altin'), (KZ + TH - 0.014, 'boya_sari')):
    silme(y, tk, zz, 0.008, 0.003, kk, 'duz')
# tied-back door, the dark inside
pencere_kutu(y, tk[0], X, -Y, TW / 2 - 0.035, 0.0, 0.07, TH * 0.8, 'koyu')
for sx in (-1, 1):
    levha_kapali(y, [V(KX + sx * 0.035, tk[0].y - 0.006, KZ), V(KX + sx * 0.06, tk[0].y - 0.006, KZ), V(KX + sx * 0.037, tk[0].y - 0.006, KZ + TH * 0.8)],
                 'boya_sari', -Y, 0.0016)
# the roof, striped, with fringed eaves and gold tassels
zr = cati_kirma(y, tk[0].x, tk[1].x, tk[0].y, tk[2].y, KZ + TH, 0.13, sacak=0.03, key='lake', mahya='altin', alt_key='boya_sari', ns=8, nr=5,
                kalinlik=0.01, dilim=['lake', 'boya_kirmizi'], kivrim=-0.25)
for i, (a, b) in enumerate(zip(tk, tk[1:] + tk[:1])):
    e = (b - a).normalized(); nrm = V(e.y, -e.x)
    L = (b - a).length + 0.06
    a2 = a - e * 0.03 + nrm * 0.03
    m = int(L / 0.03)
    for k in range(m):
        p = a2 + e * (L * (k + 0.5) / m)
        kure(y, (p.x, p.y, KZ + TH - 0.016), 0.0045, 'altin', n=5, kat=3)
        # a scalloped valance between the tassels, gold and red by turns
        p0, p1 = a2 + e * (L * k / m) - nrm * 0.002, a2 + e * (L * (k + 1) / m) - nrm * 0.002
        levha_kapali(y, [p0 + Z * (KZ + TH - 0.001), (p0 + p1) / 2 + Z * (KZ + TH - 0.02), p1 + Z * (KZ + TH - 0.001)],
                     'altin' if k % 2 else 'boya_kirmizi', nrm, 0.0016)
tanit_heykel(y, KX, KY + 0.04, zr, 0.09, 'altin', aci=-math.pi / 2)
for sx in (-1, 1):   # pennants at the roof's ridge ends
    p = V(KX + sx * (TW / 2 - TD / 2 + 0.0), KY + 0.04)
    y.prizma((p.x, p.y), 0.003, zr - 0.01, zr + 0.08, 'ahsap', n=4)
    levha_kapali(y, [V(p.x, p.y, zr + 0.078), V(p.x + 0.05 * sx, p.y, zr + 0.066), V(p.x, p.y, zr + 0.052)], 'boya_sari', Y, 0.0016)
# the porch awning on poles, striped
AY0 = tk[0].y - 0.12
for x in (KX - 0.13, KX + 0.13):
    cubuk(y, V(x, AY0, KZ), V(x, AY0, KZ + 0.12), 0.007, 'ahsap')
    kure(y, (x, AY0, KZ + 0.126), 0.007, 'altin', n=6, kat=3)
for k in range(6):
    x0, x1 = KX - 0.15 + 0.3 * k / 6, KX - 0.15 + 0.3 * (k + 1) / 6
    levha_kapali(y, [V(x0, AY0 - 0.01, KZ + 0.115), V(x1, AY0 - 0.01, KZ + 0.115), V(x1, tk[0].y, KZ + TH - 0.02), V(x0, tk[0].y, KZ + TH - 0.02)],
                 'boya_sari' if k % 2 else 'boya_kirmizi', V(0, -0.3, 1), 0.002)
# standards and banners before the pavilion, guards, the council
for sx in (-1, 1):
    x = KX + sx * 0.25
    sancak(y, x, AY0 - 0.04, KZ, boy=0.32, en=0.14, yuk=0.085, aci=-math.pi / 2 - sx * 0.6)
    # a Punic standard: the disc and crescent on a pole
    xs = KX + sx * 0.19
    y.prizma((xs, AY0 - 0.06), 0.003, KZ, KZ + 0.24, 'ahsap', n=4)
    kure(y, (xs, AY0 - 0.06, KZ + 0.25), 0.012, 'altin', n=8, kat=4)
    boru(y, [V(xs + 0.016 * math.cos(math.pi * k / 6), AY0 - 0.06, KZ + 0.25 - 0.018 * math.sin(math.pi * k / 6)) for k in range(7)], 0.0025, 'altin', n=4)
    insan(y, KX + sx * 0.08, AY0 - 0.02, KZ, 'boya_kirmizi', s=1.15, aci=-math.pi / 2, kalkan='altin', mizrak='bronz')
insan(y, KX, AY0 + 0.05, KZ, 'mor', s=1.3, aci=-math.pi / 2, kol=0.6)          # the general
for k, a in enumerate((0.6, 2.4, -0.4)):
    insan(y, 0.2 + 0.05 * math.cos(a), -0.47 + 0.05 * math.sin(a), yuk(0.2, -0.47), ['kumas', 'boya_kirmizi', 'siva_oker'][k], s=1.15, aci=a + math.pi)

# ---------------- Carthaginian and Libyan infantry: ridge tents ----------------
y.bolum('Kartaca çadırları')
for i in range(3):
    for j in range(3):
        x, yy = -0.88 + i * 0.2, -0.82 + j * 0.2
        with parca(y, (0, 0, yuk(x, yy) - 0.003)):
            cadir_besik(y, x, yy, math.pi / 2 if j % 2 == 0 else math.pi / 2 + 0.05, 0.15, 0.1, 0.085, key='kumas', serit='boya_kirmizi')
for k, (x, yy) in enumerate(((-0.58, -0.55), (-0.77, -0.32))):
    ates(y, x, yy, yuk(x, yy), 0.02, tohum=k + 1)
    for m in range(3):
        a = TAU * m / 3 + 0.4
        insan(y, x + 0.045 * math.cos(a), yy + 0.045 * math.sin(a), yuk(x, yy), ['boya_kirmizi', 'kumas', 'siva_oker'][m], s=1.1, aci=a + math.pi)
# stacked spears and shields
for x, yy in ((-0.36, -0.75), (-0.36, -0.4)):
    zb = yuk(x, yy)
    for k in range(5):
        a = TAU * k / 5
        cubuk(y, V(x + 0.02 * math.cos(a), yy + 0.02 * math.sin(a), zb), V(x, yy, zb + 0.09), 0.003, 'ahsap')
    donel(y, (x, yy), [(0.0, zb + 0.088), (0.003, zb + 0.092), (0.0, zb + 0.105)], 'bronz', n=4)

# ---------------- Iberian bell tents ----------------
y.bolum('İber çadırları')
for i in range(3):
    for j in range(3):
        x, yy = 0.45 + i * 0.2, -0.82 + j * 0.19
        with parca(y, (0, 0, yuk(x, yy) - 0.003)):
            cadir(y, (x, yy), 0.055, 0.11, key='siva_oker' if (i + j) % 2 else 'kumas', serit_key='boya_kirmizi' if (i + j) % 3 == 0 else 'ahsap_acik', n=12)
ates(y, 0.62, -0.53, yuk(0.62, -0.53), 0.02, tohum=5)
for m in range(3):
    a = TAU * m / 3
    insan(y, 0.62 + 0.045 * math.cos(a), -0.53 + 0.045 * math.sin(a), yuk(0.62, -0.53), ['beyaz', 'boya_kirmizi', 'beyaz'][m], s=1.1, aci=a + math.pi,
          kalkan='kumas' if m == 1 else None)

# ---------------- the war elephants ----------------
y.bolum('Savaş filleri')
for x in (0.36, 0.95):
    cubuk(y, V(x, 0.16, yuk(x, 0.16) - 0.005), V(x, 0.16, yuk(x, 0.16) + 0.07), 0.01, 'kutuk')
cubuk(y, V(0.36, 0.16, yuk(0.36, 0.16) + 0.06), V(0.95, 0.16, yuk(0.95, 0.16) + 0.06), 0.003, 'ahsap_koyu', 0.003)
for k, x in enumerate((0.45, 0.6, 0.75, 0.88)):
    yy = 0.09 + (0.02 if k % 2 else 0)   # (tied by a hind leg to the picket line, heads towards the camp)
    fil_h(y, x, yy, yuk(x, yy), -math.pi / 2 + rn.uniform(-0.25, 0.25), 0.95, 'fil', cul=['boya_kirmizi', 'mor', 'boya_kirmizi', 'boya_sari'][k],
          binici='kumas' if k in (1, 2) else None, hortum=0.04 if k == 3 else 0.012 * k, afrika=True)   # (Carthage's North African elephants)
for x, yy in ((0.52, -0.08), (0.8, -0.08)):
    donel(y, (x, yy), [(0.035, yuk(x, yy) - 0.002), (0.032, yuk(x, yy) + 0.02), (0.018, yuk(x, yy) + 0.036), (0.0, yuk(x, yy) + 0.042)], 'saz', n=10)
insan(y, 0.67, -0.06, yuk(0.67, -0.06), 'kumas', s=1.1, aci=1.2, kol=0.9)

# ---------------- Numidian horsemen: mapalia and horse lines ----------------
y.bolum('Numidya obası')
for k, (x, yy, a) in enumerate(((-0.92, 0.12, 0.2), (-0.72, 0.17, -0.1), (-0.52, 0.13, 0.15), (-0.93, -0.1, 1.4))):
    with parca(y, (0, 0, yuk(x, yy) - 0.004)):
        mapalia(y, x, yy, a, 0.15, 0.09, 0.065, key='saz_koyu' if k % 2 else 'ahsap_acik', serit='ahsap_koyu' if k % 2 else 'saz_koyu')
cubuk(y, V(-0.75, -0.08, yuk(-0.75, -0.08) + 0.05), V(-0.42, -0.08, yuk(-0.42, -0.08) + 0.05), 0.003, 'ahsap_koyu', 0.003)
for x in (-0.75, -0.42):
    cubuk(y, V(x, -0.08, yuk(x, -0.08) - 0.004), V(x, -0.08, yuk(x, -0.08) + 0.06), 0.008, 'kutuk')
for k, x in enumerate((-0.7, -0.63, -0.56, -0.49)):
    at(y, x, -0.13, yuk(x, -0.13), math.pi / 2 + rn.uniform(-0.15, 0.15), s=1.25, key=['ahsap', 'koyu', 'ahsap_acik', 'kum_koyu'][k],
       bas_egik=0.6 if k % 2 else 0.0)
at(y, -0.15, -0.55, yuk(-0.15, -0.55), -1.7, s=1.25, key='beyaz', binici='beyaz', eger='boya_kirmizi')
at(y, -0.21, -0.49, yuk(-0.21, -0.49), -1.5, s=1.25, key='ahsap', binici='kumas', eger='mor')
ates(y, -0.72, 0.02, yuk(-0.72, 0.02), 0.018, tohum=9)

# ---------------- carts and stores ----------------
# ---------------- the Libyan spearmen drilling before the pavilion ----------------
y.bolum('Talim')
for i in range(5):
    for j in range(4):
        x, yy = -0.09 + i * 0.045, -0.86 + j * 0.05
        insan(y, x, yy, yuk(x, yy), 'boya_kirmizi' if j % 2 == 0 else 'kumas', s=1.1, aci=math.pi / 2, kalkan='bronz', mizrak='bronz')
insan(y, 0.16, -0.78, yuk(0.16, -0.78), 'mor', s=1.2, aci=math.pi, kol=1.0, sapka='bronz')
sancak(y, 0.14, -0.86, yuk(0.14, -0.86), boy=0.18, en=0.1, yuk=0.06, aci=-0.6)

# ---------------- the column climbing the pass ----------------
y.bolum('Geçide tırmanan kol')
yol_n = []
for (ax, ay), (bx, by) in zip(YOL, YOL[1:]):
    L = math.hypot(bx - ax, by - ay)
    m = max(1, int(L / 0.042))
    for k in range(m):
        yol_n.append((ax + (bx - ax) * k / m, ay + (by - ay) * k / m, math.atan2(by - ay, bx - ax)))
for k, (x, yy, a) in enumerate(yol_n):
    if yy < 0.34: continue
    if k % 7 == 3 and yy < 0.75:
        fil_h(y, x, yy, yuk(x, yy) - 0.004, a, 0.68, 'fil', cul='boya_kirmizi', binici='kumas', kaba=True, afrika=True); continue
    if k % 5 == 1:
        at(y, x, yy, yuk(x, yy) - 0.003, a, s=0.95, key=rn.choice(('ahsap', 'koyu', 'ahsap_acik')), binici='kumas'); continue
    for o in (-0.012, 0.012):
        px, py = x - math.sin(a) * o, yy + math.cos(a) * o
        insan(y, px, py, yuk(px, py) - 0.002, rn.choice(('boya_kirmizi', 'kumas', 'siva_oker', 'beyaz')), s=0.95, aci=a,
              mizrak='bronz' if (k + (o > 0)) % 2 else None)
sancak(y, YOL[-2][0] + 0.02, YOL[-2][1], yuk(YOL[-2][0] + 0.02, YOL[-2][1]) - 0.004, boy=0.14, en=0.08, yuk=0.05, aci=1.6)

y.bolum('Arabalar ve erzak')


def araba(x, yy, a, yuk_=True):
    zb = yuk(x, yy)
    e = V(math.cos(a), math.sin(a)); s_ = V(-e.y, e.x)
    with parca(y, (x, yy, zb), a):
        kutu_merkez(y, (0, 0), 0.1, 0.06, 0.025, 'ahsap', z0=0.025)
        for sx in (-1, 1):
            boru(y, [V(0, sx * 0.033, 0.022), V(0, sx * 0.039, 0.022)], 0.022, 'ahsap_koyu', n=10)
        cubuk(y, V(0.05, 0, 0.03), V(0.12, 0, 0.012), 0.005, 'ahsap')
        if yuk_:
            for k in range(3):
                donel(y, (-0.03 + k * 0.03, 0), [(0.014, 0.05), (0.016, 0.06), (0.01, 0.072), (0.0, 0.074)], 'kumas', n=7)


araba(-0.25, -0.75, 0.3)
araba(0.25, -0.7, -0.4)
araba(0.25, -0.45, 0.1, False)
for k in range(6):   # amphorae and sacks
    x, yy = 0.3 + (k % 3) * 0.03, -0.37 + (k // 3) * 0.03
    donel(y, (x, yy), [(0.0, Z0), (0.004, Z0 + 0.004), (0.01, Z0 + 0.02), (0.009, Z0 + 0.03), (0.004, Z0 + 0.038), (0.005, Z0 + 0.044), (0.0, Z0 + 0.045)],
          'kiremit', n=8)
for k in range(5):
    x, yy = -0.46 + (k % 3) * 0.035, -0.3 + (k // 3) * 0.035
    elipsoid(y, (x, yy, yuk(x, yy) + 0.012), 0.018, 0.014, 0.014, 'kumas', n=8, kat=4)

calistir(y, 'lm_hannibalkamp')
