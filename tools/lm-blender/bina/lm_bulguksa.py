# Bulguksa Tapınağı (lm_bulguksa): the Silla temple at Gyeongju: the great stone terrace (natural boulders below, a dressed
# granite frame filled with rough stones above), the double stair-bridges Cheongungyo / Baegungyo (an arch under the lower
# flight) up to the Jahamun gate and the smaller Yeonhwagyo / Chilbogyo up to Anyangmun; the corridors (hoerang) with the
# Beomyeongnu and Jwagyeongnu pavilions at the front corners, the Daeungjeon main hall with dancheong and chimi, the
# Museoljeon lecture hall behind, the Geungnakjeon compound to the west, and in the courtyard the two stone pagodas:
# the ornate Dabotap (east) and the plain three-storey Seokgatap (west), a stone lantern; the lotus pond and banner
# pole supports before the terrace.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kore_ortak import *
from cin_ek import cokgen_cati, korkuluk as tas_korkuluk, ornekle as ornekle_
from bina_ortak import calistir

y = Yapi()
rn = random.Random(4)
Z0 = 0.03
ZT = Z0 + 0.2                 # the terrace top
YT = -0.42                    # the terrace's front face
TX0, TX1, TY1 = -1.08, 1.02, 1.0
TAS = 'granit'


# ---------------- ground ----------------
y.bolum('Zemin, gölet, yol')
GX0, GX1, GY0, GY1 = -1.14, 1.08, -1.1, 1.06
PX0, PX1, PY0, PY1 = -0.3, 0.04, -1.0, -0.84          # the lotus pond (a hole in the ground)
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'kaya_koyu', 'onarkasagsol')
for (a0, a1, b0, b1) in ((GX0, TX0, YT + 0.01, GY1), (TX1, GX1, YT + 0.01, GY1), (TX0, TX1, TY1, GY1)):
    y.yuz_yon([V(a0, b0, Z0), V(a1, b0, Z0), V(a1, b1, Z0), V(a0, b1, Z0)], 'cimen', Z)
for (a0, a1, b0, b1) in ((GX0, GX1, GY0, PY0), (GX0, GX1, PY1, YT + 0.01), (GX0, PX0, PY0, PY1), (PX1, GX1, PY0, PY1)):
    y.yuz_yon([V(a0, b0, Z0), V(a1, b0, Z0), V(a1, b1, Z0), V(a0, b1, Z0)], 'cimen', Z)
# the pond: stone kerb, water a little down, lotus pads
pk = dikdortgen(PX0, PX1, PY0, PY1)
duvarlar(y, [pk[3], pk[2], pk[1], pk[0]], Z0 - 0.02, Z0, TAS)
y.yuz_yon([V(p.x, p.y, Z0 - 0.012) for p in pk], 'su', Z)
silme(y, pk, Z0, 0.008, 0.012, 'granit_acik', 'duz')
for k in range(9):
    x, yy = rn.uniform(PX0 + 0.03, PX1 - 0.03), rn.uniform(PY0 + 0.03, PY1 - 0.03)
    donel(y, (x, yy), [(0.0, Z0 - 0.0115), (0.014, Z0 - 0.0115), (0.0, Z0 - 0.0105)], 'boya_yesil', n=8)
    if k % 3 == 0:
        donel(y, (x + 0.006, yy), [(0.0, Z0 - 0.01), (0.006, Z0 - 0.006), (0.004, Z0 + 0.0), (0.0, Z0 + 0.002)], 'beyaz', n=6)
# paths to the stairs
for (x0, x1) in ((0.24, 0.44), (-0.78, -0.62)):
    y.yuz_yon([V(x0, GY0, Z0 + 0.002), V(x1, GY0, Z0 + 0.002), V(x1, YT - 0.2, Z0 + 0.002), V(x0, YT - 0.2, Z0 + 0.002)], 'toprak', Z)


# ---------------- terrace (seokchuk) ----------------
def tas_parcasi(o, e, nn, u, v, r, key, proud=0.003, tohum=0):
    """a rough stone set in a wall face: an irregular polygon a little proud, with its edge band"""
    rs = random.Random(tohum)
    m = 6
    pts = []
    for i in range(m):
        a = TAU * i / m + rs.uniform(-0.25, 0.25)
        rr = r * rs.uniform(0.75, 1.1)
        pts.append(o + e * (u + rr * math.cos(a) * 1.25) + Z * (v + rr * math.sin(a) * 0.85))
    on = [p + nn * proud for p in pts]
    y.yuz_yon(on, key, nn)
    for i in range(m):
        j = (i + 1) % m
        c = (pts[i] + pts[j]) / 2
        y.yuz_yon([pts[i], pts[j], on[j], on[i]], key, c - sum(pts, V(0, 0, 0)) / m + nn * 0.0)


def seokchuk(a, b, z0, z1, zm, detay=True):
    """the terrace wall a->b (facing the right): natural boulders below zm, a dressed frame of posts and beams filled with
    rough stones above"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    duz_duvar(y, a, b, z0, z1, TAS)
    if not detay:
        kutu(y, a + nn * 0.006 + Z * zm, e, L, 0.006, 0.012, 'granit_acik', 'onust')
        return
    # boulders: two rows of big irregular stones
    k = 0
    u = 0.03
    while u < L - 0.03:
        r = rn.uniform(0.026, 0.036)
        tas_parcasi(a, e, nn, u, z0 + 0.03, r, 'kaya' if k % 3 else 'granit', 0.004, k)
        tas_parcasi(a, e, nn, u + 0.035, z0 + (zm - z0) * 0.72, r * 0.85, 'granit' if k % 2 else 'kaya_koyu', 0.003, k + 500)
        u += r * 2.3
        k += 1
    # the dressed frame above: a sill beam, posts, a top beam, rough infill
    ust = z1 - 0.014
    kutu(y, a + nn * 0.007 + Z * zm, e, L, 0.007, 0.014, 'granit_acik', 'onust')
    kutu(y, a + nn * 0.007 + Z * ust, e, L, 0.007, 0.014, 'granit_acik', 'onust')
    m = max(2, int(round(L / 0.12)))
    for j in range(m + 1):
        uu = min(max(L * j / m, 0.008), L - 0.008)
        kutu(y, a + e * (uu - 0.008) + nn * 0.007 + Z * (zm + 0.014), e, 0.016, 0.007, ust - zm - 0.014, 'granit_acik', 'onsagsol')
        if j < m:
            # rough stones filling the panel
            for q in range(3):
                for p_ in range(2):
                    uq = L * (j + (q + 0.5) / 3) / m
                    vq = zm + 0.014 + (ust - zm - 0.014) * (p_ + 0.5) / 2
                    tas_parcasi(a, e, nn, uq, vq, min(0.017, (ust - zm) * 0.2), 'kaya' if (q + p_ + j) % 2 else 'granit', 0.003, j * 7 + q * 2 + p_)


y.bolum('Taş teras')
tk = dikdortgen(TX0, TX1, YT, TY1)
y.yuz_yon([V(p.x, p.y, ZT) for p in tk], 'kum_acik', Z)
ZM = Z0 + 0.09
for i in (0, 1, 2, 3):
    seokchuk(tk[i], tk[(i + 1) % 4], Z0, ZT, ZM, detay=(i in (0, 3)))
silme(y, tk, ZT - 0.006, 0.006, 0.008, 'granit_acik', 'duz')


# ---------------- stairs ----------------
def merdiven_kopru(xc, en, y_on, y_orta, y_ust, zm, kemer=True, n1=9, n2=9):
    """a double stair-bridge up the terrace: the lower flight from the ground at y_on to a landing (y_orta, height zm),
    the upper flight to the terrace edge y_ust; stone cheeks with sloping rails; an arch under the lower flight"""
    yon = math.pi / 2
    run1 = (y_orta - 0.05) - y_on
    run2 = y_ust - y_orta
    merdiven(y, V(xc, y_on), yon, en, Z0, zm, n=n1, d=run1 / n1, key='granit_acik')
    kutu(y, V(xc - en / 2, y_orta - 0.05, Z0), X, en, 0.05 + 0.001, zm - Z0, 'granit_acik', 'onsagsolust')
    merdiven(y, V(xc, y_orta), yon, en, zm, ZT, n=n2, d=run2 / n2, key='granit_acik')
    # the solid under the upper flight (its steps start at the landing height)
    kutu(y, V(xc - en / 2, y_orta, Z0), X, en, run2, zm - Z0, 'granit', 'sagsol')
    cw = 0.028
    for sx in (-1, 1):
        x0 = xc + sx * (en / 2) + (0 if sx > 0 else -cw)
        xo = x0 if sx < 0 else x0 + cw           # the outer face's x
        # the cheek block: a sloped top following the flights
        prof = [(y_on, Z0 + 0.03), (y_orta - 0.05, zm + 0.03), (y_orta, zm + 0.03), (y_ust, ZT + 0.03)]
        for xx, s in ((xo, sx), (xo - sx * cw, -sx)):
            for k in range(3):
                (ya, za), (yb, zb) = prof[k], prof[k + 1]
                y.yuz_yon([V(xx, ya, Z0), V(xx, yb, Z0), V(xx, yb, zb), V(xx, ya, za)], TAS, V(s, 0, 0))
        for k in range(3):
            (ya, za), (yb, zb) = prof[k], prof[k + 1]
            y.yuz_yon([V(x0, ya, za), V(x0 + cw, ya, za), V(x0 + cw, yb, zb), V(x0, yb, zb)], 'granit_acik', Z + V(0, -(zb - za), 0))
        y.yuz_yon([V(x0, y_on, Z0), V(x0 + cw, y_on, Z0), V(x0 + cw, y_on, Z0 + 0.03), V(x0, y_on, Z0 + 0.03)], TAS, -Y)
        # the stone rail: posts and two sloping bars
        pts = []
        for k in range(3):
            (ya, za), (yb, zb) = prof[k], prof[k + 1]
            m = max(1, int(round((yb - ya) / 0.05)))
            for j in range(m):
                pts.append((ya + (yb - ya) * j / m, za + (zb - za) * j / m))
        pts.append(prof[-1])
        xm = x0 + cw / 2
        for (yy, zz) in pts:
            kutu_merkez(y, (xm, yy), 0.012, 0.012, 0.045, 'granit_acik', z0=zz - 0.002)
            kure(y, (xm, yy, zz + 0.047), 0.0065, 'granit_acik', n=6, kat=3)
        for hh in (0.02, 0.038):
            for k in range(len(pts) - 1):
                cubuk(y, V(xm, pts[k][0], pts[k][1] + hh), V(xm, pts[k + 1][0], pts[k + 1][1] + hh), 0.006, 'granit_acik', 0.007)
        if kemer:
            # the arch through the lower flight, seen on both cheeks: a dark round-headed opening with voussoirs
            ya, yb = y_on + run1 * 0.3, y_orta - 0.05
            for xx, s in ((xo, sx),):
                aa, bb = (V(xx, ya), V(xx, yb)) if s < 0 else (V(xx, yb), V(xx, ya))
                W_ = (bb - aa).length
                ee = (bb - aa) / W_
                nn_ = V(ee.y, -ee.x)
                R = W_ * 0.36
                cc = aa.lerp(bb, 0.5) + nn_ * 0.0012
                pts_ = [cc + ee * (R * math.cos(math.pi * i / 10)) + Z * (Z0 + 0.012 + R * math.sin(math.pi * i / 10)) for i in range(11)]
                pts_ = [cc + ee * R + Z * Z0] + pts_ + [cc - ee * R + Z * Z0]
                y.yuz_yon(pts_, 'koyu', nn_)
                for i in range(10):
                    t0, t1 = math.pi * i / 10, math.pi * (i + 1) / 10
                    q = [cc + ee * ((R + rr) * math.cos(t)) + Z * (Z0 + 0.012 + (R + rr) * math.sin(t)) + nn_ * 0.0006 for rr, t in ((0, t0), (0, t1), (0.014, t1), (0.014, t0))]
                    y.yuz_yon(q, 'granit_acik' if i % 2 else 'kaya', nn_)


y.bolum('Cheongungyo / Baegungyo merdivenleri')
merdiven_kopru(0.34, 0.18, YT - 0.4, YT - 0.2, YT, Z0 + 0.1)
y.bolum('Yeonhwagyo / Chilbogyo merdivenleri')
merdiven_kopru(-0.72, 0.13, YT - 0.32, YT - 0.16, YT, Z0 + 0.1, kemer=False, n1=7, n2=7)


# ---------------- buildings ----------------
def hoerang(x0, x1, y0, y1, z, h, dis, pencere=True):
    """a covered corridor on the rectangle: the closed outer wall on side dis (0 -y, 1 +x, 2 +y, 3 -x) with lattice
    windows, red posts along the open inner side, a painted beam, a plain ceiling and a gable roof"""
    k = dikdortgen(x0, x1, y0, y1)
    kutu(y, V(x0, y0, z), X, x1 - x0, y1 - y0, 0.012, 'granit_acik', 'onarkasagsolust')
    zf = z + 0.012
    a, b = k[dis], k[(dis + 1) % 4]
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    nb = max(1, int(round(L / 0.1)))
    for j in range(nb):
        p, q = a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb)
        if pencere:
            dikdortgen_acik(y, p, q, zf, h, 0.25, 0.75, h * 0.35, h * 0.72, ('siva', 'ahsap', 'ahsap', 'kumas'), derin=0.006,
                            cerceve=(0.004, 'boya_yesil'), ic_kenar=True)
            kafes(y, p, q, zf, 0.25, 0.75, h * 0.35, h * 0.72, 'ahsap', 3, 3, 0.002, 0.004)
        else:
            duz_duvar(y, p, q, zf, zf + h, 'siva')
        kutu(y, p + nn * 0.003 + Z * zf, e, (q - p).length, 0.004, h * 0.22, 'granit', 'onust')
    # the wall's inner face and posts on it
    ic_a, ic_b = a - nn * 0.012, b - nn * 0.012
    duz_duvar(y, ic_b, ic_a, zf, zf + h, 'siva')
    for p_, q_, s_ in ((a, ic_a, -e), (b, ic_b, e)):   # (the wall's ends: open corridor ends showed the gap)
        y.yuz_yon([p_ + Z * zf, q_ + Z * zf, q_ + Z * (zf + h), p_ + Z * (zf + h)], 'siva', s_)
    for j in range(nb + 1):
        p = a.lerp(b, j / nb)
        kutu_merkez(y, (p.x + nn.x * 0.005, p.y + nn.y * 0.005), 0.012, 0.012, h, 'kirmizi', z0=zf)
    # the open side's posts
    c_, d_ = k[(dis + 2) % 4], k[(dis + 3) % 4]
    for j in range(nb + 1):
        p = c_.lerp(d_, j / nb)
        y.prizma((p.x, p.y), 0.0085, zf, zf + h, 'kirmizi', n=8, ust=False)
        donel(y, (p.x, p.y), [(0.0, zf), (0.014, zf), (0.012, zf + 0.006), (0.0085, zf + 0.007)], 'granit_acik', n=8)
    for (p, q) in ((a, b), (c_, d_)):
        ee = (q - p).normalized(); n2 = V(ee.y, -ee.x)
        if (p - a).length > 1e-6:   # the open side: a painted beam on both faces
            cubuk(y, p + Z * (zf + h - 0.012), q + Z * (zf + h - 0.012), 0.014, 'boya_yesil', 0.024)
            cubuk(y, p + Z * (zf + h - 0.026), q + Z * (zf + h - 0.026), 0.011, 'turkuaz', 0.01)
    y.yuz_yon([V(p.x, p.y, zf + h) for p in k], 'boya_yesil', -Z)
    return kore_cati(y, x0, x1, y0, y1, zf + h, 0.075, sacak=0.05, tur='matbae', kivrim=0.3, alt_key='boya_yesil', ucluk='lake_koyu',
                     sirt_h=0.013, uc=None, ns=max(4, int(L / 0.06)), nr=3)


def tapinak_salonu(x0, x1, y0, y1, z, gh, h, cati_h, sacak, bay=0.1, adim=0.05, uc='chimi', desen=None, basamak=True, cikinti=0.026):
    """a temple hall: a granite base with front steps, red posts, lattice doors, dancheong with dapo brackets, a paljak
    roof. Returns the top z"""
    bs = ((0, 0.5, min(0.18, (x1 - x0) * 0.4)),) if basamak else ()
    zb = gidan(y, x0 - 0.04, x1 + 0.04, y0 - 0.04, y1 + 0.04, z, gh, ust='granit_acik', basamak=bs)
    desen = desen or (lambda i, j, nb: 'kapi' if i == 0 else ('kapi' if (i in (1, 3) and j == 0) else 'duvar' if i != 2 else 'pencere'))
    zt = hanok_govde(y, x0, x1, y0, y1, zb, h, bay=bay, direk='kirmizi', duvar='siva', cerceve='ahsap', kagit='kumas', desen=desen,
                     yuvarlak=True, ust_bant=None, direk_en=0.02, alt_bant='boya_yesil')
    zd = dancheong(y, dikdortgen(x0, x1, y0, y1), zt, h * 0.16, adim=adim, cikinti=cikinti)
    return kore_cati(y, x0, x1, y0, y1, zd, cati_h, sacak=sacak, tur='paljak', kivrim=0.42, yukari=0.04, alt_key='boya_yesil',
                     ucluk='lake_koyu', uc=uc, sirt_h=min(0.032, cati_h * 0.12))


ZC = ZT                                   # courtyard level
MX0, MX1 = -0.3, 0.98                     # the main compound's outer walls
MY0, MY1 = YT + 0.02, 0.66                # front corridor wall, Museoljeon front
CD = 0.12                                 # corridor depth
HC = 0.1                                  # corridor wall height

y.bolum('Daeungjeon')
tepe = tapinak_salonu(0.08, 0.6, 0.24, 0.52, ZC, 0.05, 0.19, 0.27, 0.12, bay=0.104, adim=0.052)
# a name board on the front beam
kutu(y, V(0.29, 0.24 - 0.036, ZC + 0.05 + 0.19 + 0.003), X, 0.1, 0.008, 0.04, 'lake_koyu')
kutu(y, V(0.298, 0.24 - 0.0375, ZC + 0.05 + 0.19 + 0.009), X, 0.084, 0.002, 0.028, 'altin', 'onsagsolust')

y.bolum('Museoljeon')
tapinak_salonu(MX0 - 0.02, MX1 + 0.02, MY1 + 0.02, MY1 + 0.2, ZC, 0.03, 0.15, 0.18, 0.08, bay=0.13, adim=0.13, uc='mangwa', basamak=False,
               desen=lambda i, j, nb: ('kapi' if j % 3 == 1 else 'pencere') if i == 0 else 'duvar', cikinti=0.02)

y.bolum('Jahamun')
JX0, JX1 = 0.19, 0.49
tapinak_salonu(JX0, JX1, YT + 0.045, YT + 0.2, ZC, 0.02, 0.16, 0.17, 0.08, bay=0.1, adim=0.075, uc='mangwa', basamak=False,
               desen=lambda i, j, nb: ('acik' if j == 1 else 'duvar') if i in (0, 2) else 'duvar', cikinti=0.02)

y.bolum('Köşe köşkleri: Beomyeongnu, Jwagyeongnu')
for (cx, kayit) in ((MX0 + 0.05, 'Beomyeongnu'), (MX1 - 0.05, 'Jwagyeongnu')):
    # a raised pavilion standing on a tall stone pedestal that rises from the ground in front of the terrace
    bx0, bx1, by0, by1 = cx - 0.12, cx + 0.12, YT - 0.06, YT + 0.17
    duvarlar(y, dikdortgen(bx0, bx1, by0, by1), Z0, ZT + 0.03, TAS, ust='granit_acik')
    if kayit == 'Beomyeongnu':   # its famous stacked stone pillars: a stepped, waisted pedestal on the front
        for sx in (-1, 1):
            xx = cx + sx * 0.07
            for k, (w_, h_) in enumerate(((0.06, 0.05), (0.045, 0.05), (0.06, 0.03), (0.04, 0.05), (0.07, 0.025))):
                z_ = Z0 + sum(hh for _, hh in ((0.06, 0.05), (0.045, 0.05), (0.06, 0.03), (0.04, 0.05), (0.07, 0.025))[:k])
                kutu_merkez(y, (xx, by0 - 0.012), w_, 0.024, h_, 'granit_acik', z0=z_)
    for zz in (Z0 + 0.09, ZT + 0.02):
        silme(y, dikdortgen(bx0, bx1, by0, by1), zz, 0.01, 0.006, 'granit_acik', 'duz')
    tapinak_salonu(bx0 + 0.03, bx1 - 0.03, by0 + 0.03, by1 - 0.03, ZT + 0.03, 0.012, 0.13, 0.17, 0.08, bay=0.09, adim=0.08, uc='mangwa',
                   basamak=False, desen=lambda i, j, nb: 'pencere' if j == nb // 2 else 'kapi' if i == 0 else 'duvar', cikinti=0.02)

y.bolum('Revaklar (hoerang)')
hoerang(MX0 + 0.17, JX0, MY0, MY0 + CD, ZC, HC, 0)
hoerang(JX1, MX1 - 0.17, MY0, MY0 + CD, ZC, HC, 0)
hoerang(MX0, MX0 + CD, YT + 0.17, MY1, ZC, HC, 3)
hoerang(MX1 - CD, MX1, YT + 0.17, MY1, ZC, HC, 1)

y.bolum('Seokgatap')


def okgaeseok(cx, cy, w, z, sacak, h=0.024, kademe=4, key='granit_acik', ust_w=None):
    """a stone pagoda's roof stone: stepped corbels underneath, a thin eave slab, a shallow hipped top with turned-up
    corners. Returns the z for the next body stone"""
    zz = z
    for k in range(kademe):
        ww = w * (0.72 + 0.28 * (k + 1) / kademe) * 0.98
        kutu_merkez(y, (cx, cy), ww, ww, 0.004, key, z0=zz)
        zz += 0.004
    hw = w / 2 + sacak
    zt = cati_kirma(y, cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2, zz, h * 1.6, sacak, key, key, 0.006, 0.25, 0.006, key, ns=4, nr=3,
                    r_ust=0.62, mahya_en=0.004)
    uw = (ust_w or w * 0.7) / 2 + 0.006
    t = 0.62 * (w / 2 + sacak)
    y.yuz_yon([V(cx - t, cy - t, zt), V(cx + t, cy - t, zt), V(cx + t, cy + t, zt), V(cx - t, cy + t, zt)], key, Z)
    kutu_merkez(y, (cx, cy), uw * 2, uw * 2, 0.006, key, z0=zt)
    return zt + 0.006


def govde_tasi(cx, cy, w, z, h, key='granit_acik', direk=True):
    """a pagoda body stone with carved corner and middle pilasters"""
    kutu_merkez(y, (cx, cy), w, w, h, key, z0=z)
    if direk:
        k = dikdortgen(cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2)
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            e = (b - a).normalized(); nn = V(e.y, -e.x)
            for u in (0.06, 0.94) + ((0.5,) if w > 0.12 else ()):
                p = a.lerp(b, u) + nn * 0.0012
                pw = w * 0.05
                y.yuz_yon([p - e * pw + Z * z, p + e * pw + Z * z, p + e * pw + Z * (z + h), p - e * pw + Z * (z + h)], 'granit', nn)
    return z + h


def sangnyun(cx, cy, z, boy, key='granit_acik', metal='bronz'):
    """a pagoda finial: a dew basin, an inverted bowl, stacked rings, a jewel"""
    kutu_merkez(y, (cx, cy), 0.034, 0.034, 0.012, key, z0=z)
    donel(y, (cx, cy), [(0.014, z + 0.012), (0.02, z + 0.02), (0.012, z + 0.03), (0.0, z + 0.03)], key, n=10)
    y.prizma((cx, cy), 0.0035, z + 0.03, z + boy, metal, n=6)
    for i in range(4):
        zz = z + 0.04 + (boy - 0.06) * i / 3
        donel(y, (cx, cy), [(0.0, zz), (0.011 - i * 0.0012, zz + 0.003), (0.0, zz + 0.006)], metal, n=10)
    kure(y, (cx, cy, z + boy + 0.006), 0.007, metal, n=8, kat=4)
    return z + boy + 0.013


def seokgatap(cx, cy, z):
    z = gidan(y, cx - 0.11, cx + 0.11, cy - 0.11, cy + 0.11, z, 0.012, key='granit_acik', ust='granit_acik', kat=1)
    z = govde_tasi(cx, cy, 0.19, z, 0.05)
    z = okgaeseok(cx, cy, 0.19, z, 0.012, h=0.008, kademe=1, ust_w=0.15)
    z = govde_tasi(cx, cy, 0.15, z, 0.062)
    z = okgaeseok(cx, cy, 0.15, z, 0.012, h=0.008, kademe=1, ust_w=0.09)
    for w, h, s in ((0.088, 0.07, 0.036), (0.074, 0.032, 0.032), (0.066, 0.029, 0.029)):
        z = govde_tasi(cx, cy, w, z, h)
        z = okgaeseok(cx, cy, w * 1.25, z, s, h=0.022, kademe=4, ust_w=w * 0.85)
    return sangnyun(cx, cy, z, 0.075)


with parca(y, (0.06, -0.03, ZC), 0, 1.2):
    seokgatap(0, 0, 0)

y.bolum('Dabotap')


def dabotap(cx, cy, z):
    K = 'granit_acik'
    # the stylobate with a stair on each side
    z1 = gidan(y, cx - 0.1, cx + 0.1, cy - 0.1, cy + 0.1, z, 0.04, key=K, ust=K, kat=2,
               basamak=((0, 0.5, 0.045), (1, 0.5, 0.045), (2, 0.5, 0.045), (3, 0.5, 0.045)))
    # the first storey: four square corner pillars and the central pillar under a heavy roof slab
    H1 = 0.075
    for sx in (-1, 1):
        for sy in (-1, 1):
            kutu_merkez(y, (cx + sx * 0.062, cy + sy * 0.062), 0.024, 0.024, H1, K, z0=z1)
            kutu_merkez(y, (cx + sx * 0.062, cy + sy * 0.062), 0.032, 0.032, 0.008, K, z0=z1 + H1 - 0.008)
    kutu_merkez(y, (cx, cy), 0.04, 0.04, H1, K, z0=z1)
    # beams between the pillars
    for (a, b) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
        cubuk(y, V(cx + a[0] * 0.062, cy + a[1] * 0.062, z1 + H1 - 0.006), V(cx + b[0] * 0.062, cy + b[1] * 0.062, z1 + H1 - 0.006), 0.016, K, 0.012)
    z2 = okgaeseok(cx, cy, 0.15, z1 + H1, 0.022, h=0.012, kademe=3, ust_w=0.16)
    # the square railing on the roof slab
    rk = dikdortgen(cx - 0.072, cx + 0.072, cy - 0.072, cy + 0.072)
    duvarlar(y, rk, z2, z2 + 0.016, K, ust=K, kalinlik=0.005)
    for p in ornekle_(rk, 0.048):
        kutu_merkez(y, (p.x, p.y), 0.009, 0.009, 0.024, K, z0=z2)
    # the octagonal storey: a body ringed by bamboo-jointed posts, its own railing, a lotus band
    kat8 = math.pi / 8
    donel(y, (cx, cy), [(0.052, z2), (0.052, z2 + 0.012), (0.046, z2 + 0.014), (0.0, z2 + 0.014)], K, n=8, kat=kat8)
    zb = z2 + 0.014
    y.prizma((cx, cy), 0.036, zb, zb + 0.045, 'granit', n=8, kat=kat8)
    for p in cokgen((cx, cy), 0.044, 8, kat8):
        y.prizma((p.x, p.y), 0.0045, zb, zb + 0.045, K, n=6, ust=False)
        for zz in (0.015, 0.03):
            y.prizma((p.x, p.y), 0.006, zb + zz, zb + zz + 0.003, K, n=6)
    z3 = zb + 0.045
    donel(y, (cx, cy), [(0.03, z3), (0.054, z3 + 0.004), (0.054, z3 + 0.01), (0.0, z3 + 0.01)], K, n=8, kat=kat8)
    k8_ = cokgen((cx, cy), 0.052, 8, kat8)
    duvarlar(y, k8_, z3 + 0.01, z3 + 0.024, K, ust=K, kalinlik=0.004)
    for p in k8_:
        y.prizma((p.x, p.y), 0.0045, z3 + 0.01, z3 + 0.03, K, n=6)
    # lotus petals round the drum above
    z4 = z3 + 0.012
    y.prizma((cx, cy), 0.03, z4, z4 + 0.04, 'granit', n=8, kat=kat8)
    # (a closed scalloped cup: the petal tips rise, the notches between them dip)
    nP = 32
    R_ = lambda i: (0.049, 0.03) if i % 2 == 0 else (0.04, 0.019)
    alt = [V(cx + 0.03 * math.cos(TAU * i / nP), cy + 0.03 * math.sin(TAU * i / nP), z4 + 0.003) for i in range(nP)]
    ust = [V(cx + R_(i)[0] * math.cos(TAU * i / nP), cy + R_(i)[0] * math.sin(TAU * i / nP), z4 + R_(i)[1]) for i in range(nP)]
    ic = [V(cx + 0.03 * math.cos(TAU * i / nP), cy + 0.03 * math.sin(TAU * i / nP), z4 + R_(i)[1]) for i in range(nP)]
    for i in range(nP):
        j = (i + 1) % nP
        d = V(math.cos(TAU * (i + 0.5) / nP), math.sin(TAU * (i + 0.5) / nP))
        y.yuz_yon([alt[i], alt[j], ust[j], ust[i]], K, d)
        y.yuz_yon([ust[i], ust[j], ic[j], ic[i]], K, Z)
    # eight short posts round the lotus holding the octagonal roof stone
    for p in cokgen((cx, cy), 0.04, 8, kat8):
        y.prizma((p.x, p.y), 0.004, z4 + 0.025, z4 + 0.06, K, n=6, ust=False)
    z5 = z4 + 0.06
    donel(y, (cx, cy), [(0.0, z5), (0.05, z5), (0.05, z5 + 0.006), (0.0, z5 + 0.006)], K, n=8, kat=kat8)
    zt, _ = cokgen_cati(y, (cx, cy), 0.05, 8, z5 + 0.006, 0.045, sacak=0.016, key=K, mahya=K, kivrim=0.3, yukari=0.006, r_ust=0.012, sirt=False,
                        ns=1, nr=3, alt_key=K, kalinlik=0.006, mahya_en=0.004)
    y.yuz_yon([V(p.x, p.y, zt) for p in cokgen((cx, cy), 0.014, 8, kat8)], K, Z)
    return sangnyun(cx, cy, zt - 0.004, 0.1)


with parca(y, (0.62, -0.03, ZC), 0, 1.2):
    dabotap(0, 0, 0)

y.bolum('Taş fener')
LX, LY = 0.34, 0.04
z = ZC
donel(y, (LX, LY), [(0.03, z), (0.03, z + 0.01), (0.022, z + 0.012)], 'granit_acik', n=8, kat=math.pi / 8)
donel(y, (LX, LY), [(0.022, z + 0.012), (0.026, z + 0.022), (0.012, z + 0.026)], 'granit_acik', n=8, kat=math.pi / 8)   # lotus base
y.prizma((LX, LY), 0.009, z + 0.026, z + 0.07, 'granit_acik', n=8, kat=math.pi / 8)
donel(y, (LX, LY), [(0.012, z + 0.07), (0.026, z + 0.078), (0.024, z + 0.084), (0.0, z + 0.084)], 'granit_acik', n=8, kat=math.pi / 8)
k8 = cokgen((LX, LY), 0.019, 8, math.pi / 8)
for i in range(8):
    a, b = k8[i], k8[(i + 1) % 8]
    if i % 2 == 0:
        dikdortgen_acik(y, a, b, z + 0.084, 0.04, 0.2, 0.8, 0.008, 0.032, ('granit_acik', 'granit', 'granit', 'koyu'), derin=0.004)
    else:
        duz_duvar(y, a, b, z + 0.084, z + 0.124, 'granit_acik')
tz, _ = cokgen_cati(y, (LX, LY), 0.019, 8, z + 0.124, 0.03, sacak=0.014, key='granit_acik', mahya='granit_acik', kivrim=0.3, yukari=0.004, sirt=False,
                    ns=1, nr=2, alt_key='granit_acik', kalinlik=0.005, mahya_en=0.003)
kure(y, (LX, LY, tz + 0.008), 0.008, 'granit_acik', n=8, kat=4)

y.bolum('Geungnakjeon avlusu ve Anyangmun')
LX0, LX1 = TX0 + 0.02, MX0 - 0.07
hoerang(LX0, -0.83, MY0, MY0 + CD, ZC, HC, 0)
hoerang(-0.61, LX1, MY0, MY0 + CD, ZC, HC, 0)
tapinak_salonu(-0.83, -0.61, YT + 0.045, YT + 0.2, ZC, 0.02, 0.15, 0.15, 0.07, bay=0.11, adim=0.08, uc='mangwa', basamak=False,
               desen=lambda i, j, nb: ('acik' if j == 1 else 'duvar') if i in (0, 2) else 'duvar', cikinti=0.02)
tapinak_salonu(-0.86, -0.56, 0.12, 0.36, ZC, 0.04, 0.15, 0.21, 0.09, bay=0.1, adim=0.075, uc='chimi')
toprak_duvar(y, [V(MX0 - 0.012, 0.6), V(LX0, 0.6), V(LX0, MY0 + CD + 0.01)], ZC, 0.1, govde='siva', kaide='granit', kaide_h=0.03)
# a small stone lantern before it
for (x, yy) in ((-0.71, 0.02),):
    donel(y, (x, yy), [(0.02, ZC), (0.02, ZC + 0.008), (0.007, ZC + 0.01)], 'granit_acik', n=8)
    y.prizma((x, yy), 0.006, ZC + 0.01, ZC + 0.05, 'granit_acik', n=8)
    y.prizma((x, yy), 0.014, ZC + 0.05, ZC + 0.075, 'granit_acik', n=8)
    y.koni((x, yy), 0.022, ZC + 0.075, 0.02, 'granit_acik', n=8)

y.bolum('Birojeon ve taş stupa')
# the Birojeon hall up behind the Geungnakjeon court, and before it the Gwangmyeongdae: a small stone stupa (budo) with
# an octagonal lotus base, a round body and an octagonal roof stone
tapinak_salonu(-0.96, -0.64, 0.7, 0.86, ZC, 0.03, 0.14, 0.18, 0.07, bay=0.107, adim=0.16, uc='mangwa',
               desen=lambda i, j, nb: ('kapi' if j % 2 == 1 or nb == 1 else 'pencere') if i == 0 else 'duvar', cikinti=0.02)
SX_, SY_ = -0.48, 0.74
kat8 = math.pi / 8
z = gidan(y, SX_ - 0.04, SX_ + 0.04, SY_ - 0.04, SY_ + 0.04, ZC, 0.01, key='granit_acik', ust='granit_acik', kat=1)
donel(y, (SX_, SY_), [(0.032, z), (0.032, z + 0.012), (0.026, z + 0.014), (0.02, z + 0.026), (0.03, z + 0.034), (0.03, z + 0.04),
                      (0.0, z + 0.04)], 'granit_acik', n=8, kat=kat8)   # lotus base (waisted)
donel(y, (SX_, SY_), [(0.018, z + 0.04), (0.022, z + 0.055), (0.022, z + 0.075), (0.016, z + 0.088), (0.0, z + 0.09)], 'granit_acik', n=10)
tz, _ = cokgen_cati(y, (SX_, SY_), 0.02, 8, z + 0.086, 0.022, sacak=0.012, key='granit_acik', mahya='granit_acik', kivrim=0.3, yukari=0.004,
                    sirt=False, ns=1, nr=2, alt_key='granit_acik', kalinlik=0.005, mahya_en=0.003)
sangnyun(SX_, SY_, tz - 0.004, 0.05)

y.bolum('Ağaçlar')
for k, (tx, ty, boy) in enumerate(((-1.03, 0.96, 0.36), (-0.44, 0.93, 0.34), (1.02, 0.88, 0.42), (-1.06, -0.68, 0.34), (0.98, -0.72, 0.36),
                                   (0.78, -0.95, 0.3), (-0.95, -0.98, 0.3))):
    zz = ZT if ty > YT else Z0
    sonamu(y, tx, ty, zz, boy=boy, tohum=k + 20, yon=math.atan2(-ty, -tx) + rn.uniform(-0.4, 0.4))
# maples by the pond in autumn red
for (tx, ty) in ((0.12, -0.95), (-0.45, -0.75), (0.6, -0.62)):
    y.prizma((tx, ty), 0.008, Z0, Z0 + 0.1, 'ahsap', n=6)
    for k in range(5):
        a = TAU * k / 5
        kure(y, (tx + 0.04 * math.cos(a), ty + 0.04 * math.sin(a), Z0 + 0.13 + 0.02 * (k % 2)), 0.045, 'boya_kirmizi' if k % 2 else 'turuncu', n=8, kat=4)
    kure(y, (tx, ty, Z0 + 0.17), 0.05, 'boya_kirmizi', n=8, kat=4)

y.bolum('Bayrak direği taşları ve sancak')
for (x, yy) in ((0.06, -0.72),):
    for sx in (-1, 1):
        kutu_merkez(y, (x + sx * 0.016, yy), 0.014, 0.04, 0.12, 'granit_acik', z0=Z0)
        kutu_merkez(y, (x + sx * 0.016, yy), 0.016, 0.044, 0.012, 'granit_acik', z0=Z0 + 0.118)
    kutu_merkez(y, (x, yy), 0.06, 0.06, 0.012, 'granit', z0=Z0)
    sancak(y, x, yy, Z0, boy=0.62, en=0.14, yuk=0.1, aci=-0.6)

y.bolum('İnsanlar')
for (x, yy, a, g, k) in ((0.3, -0.9, math.pi / 2, 'siva_krem', 'kahve'), (0.4, -0.95, math.pi / 2, 'beyaz', 'boya_kirmizi'),
                         (0.3, 0.05, -math.pi / 2, 'kumas', 'kahve'), (-0.7, -0.85, math.pi / 2, 'beyaz', 'boya_yesil')):
    kisi(y, x, yy, Z0 if yy < YT else ZC, aci=a, boy=0.085, govde=g, kusak='lake_koyu' if k == 'kahve' else k,
         sapka='yok' if g == 'kumas' else 'gat', kol='on')

calistir(y, 'lm_bulguksa')
