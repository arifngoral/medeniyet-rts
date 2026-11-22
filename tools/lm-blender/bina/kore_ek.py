# Helpers for the Joseon (Korean) landmarks lm_gyeongbok, lm_hwachaatolye, lm_kaplumbaga, lm_komutanlik: a timber hall
# on a granite stylobate (round red columns on granite bases, lattice doors with paper behind, white plaster walls framed
# in red timber, dancheong-painted beams and bracket sets, a green soffit), the roofs (paljak hip-and-gable, ujingak
# hipped, matbae gable) in grey tiles with white-plastered ridges, chwidu ridge-end ornaments and japsang figures on the
# hips; a roofed cloister gallery (heonggak), a ground slab with holes (ponds, docks), a pond with a granite embankment.
# Independent of kore_ortak.py (the other Korean set uses that).
import math
from parcalar import *
from parcalar import _cati_z
import parcalar as _parcalar
_parcalar.CATI_US = 3          # Korean eaves curve up gently along their whole length (parcalar._cati_z)
from cin_ek import korkuluk, dikme, chiwen, sacak_hayvanlari, egim_icin, aslan, cam, insan, fici, teras, teras_merdiven, sayim, ornekle, kazan

_parcalar.KALCA_N = 10         # hip caps sampled closely (in 4 chords they left the lifted, concave hip and floated)
PALJAK_UST, PALJAK_DIK = 0.68, 0.78  # paljak: how far up the hips run, how steep the small gable on top
CATI, CATI2 = 'kiremit_koyu', 'kiremit_koyu2'     # grey tiles
MAHYA = 'siva'                                     # white-plastered ridges (yangseong)
ALT = 'boya_yesil'                                 # the green-painted soffit and rafters (dancheong)
BOYA = ('boya_yesil', 'turkuaz')                   # dancheong beams: green ground, blue-green bands
DIREK = 'lake'                                     # red-brown columns
DUVAR = 'siva'                                     # white plaster walls
KAFES = 'lake'                                     # door and window lattice
KAGIT = 'siva_krem'                                   # hanji paper behind the lattice
TAS = 'granit'                                     # stylobate, bases
TAS2 = 'granit_acik'


# ---------------------------------------------------------------- roofs
def kore_cati(y, x0, x1, y0, y1, z, h, sacak, tur='paljak', kivrim=0.34, yukari=0.04, japsang=0, chwidu=1.0, mahya_en=0.014,
              ns=None, nr=None, cati=CATI, mahya=MAHYA, alt=ALT, ucluk='ahsap_koyu', yongmaru=True, j_key=CATI2):
    """a Korean roof over the wall rectangle x0..x1, y0..y1 (wall top z): tur 'paljak' (hip-and-gable), 'ujingak' (hipped),
    'matbae' (gable). A softer curve than the Chinese ones (kivrim), the corners lifted (yukari), white ridges, a heavier
    main ridge (yongmaru) with chwidu at its ends (chwidu = their scale, 0 none), japsang figures on the hips. Returns
    the top z"""
    long_ = max(x1 - x0, y1 - y0); short = min(x1 - x0, y1 - y0)
    ns = ns or max(4, int(long_ / 0.05)); nr = nr or (4 if ns < 8 else 6)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = long_ / 2 + sacak, short / 2 + sacak
    ex = V(1, 0) if (x1 - x0) >= (y1 - y0) else V(0, 1)
    if tur == 'paljak':
        # (the Korean hapgak: the hips run further up than on a Japanese irimoya, the gable on top small and low)
        zr = cati_irimoya(y, x0, x1, y0, y1, z, h, sacak, cati, mahya, kivrim, yukari, alt, ucluk, ns=ns, nr=nr,
                          ns2=max(3, ns * 2 // 3), nr2=3 if ns < 8 else 5, r_ust=PALJAK_UST, dik=PALJAK_DIK)
        L = a - b * PALJAK_UST
        # the white-plastered hip ridges of the lower roof (cati_kirma leaves them off when it stops part-way up)
        for sx in (-1, 1):
            for sy in (-1, 1):
                pts = []
                for k in range(11):
                    r = PALJAK_UST * k / 10
                    px, py = sx * (a - b * r), sy * b * (1 - r)
                    zz = z + _cati_z(px, py, a, b, h, kivrim, yukari) + 0.004
                    if ex.x < 0.5:
                        px, py = -py, px
                    pts.append(V(cx + px, cy + py, zz))
                kw = max(0.0065, min(0.0105, short * 0.03))
                for k in range(10):
                    cubuk(y, pts[k], pts[k + 1], kw, mahya)
        zt = zr - 0.0096           # (the gable roof's ridge cap top: zr; its ridge line a little below)
        hm = 0.012
    elif tur == 'ujingak':
        zr = cati_kirma(y, x0, x1, y0, y1, z, h, sacak, cati, mahya, 0.012, kivrim, yukari, alt, ns=ns, nr=nr, mahya_en=mahya_en)
        L = a - b
        zt = zr - mahya_en * 0.8
        hm = mahya_en
    else:
        zr = cati_besik(y, x0, x1, y0, y1, z, h, sacak, cati, mahya, 0.01, kivrim, alt, ucluk, nr=nr, ns=ns, mahya_en=mahya_en)
        L = long_ / 2 + sacak
        zt = zr - mahya_en * 0.8
        hm = mahya_en
    tepe = zr
    if tur == 'ujingak' and L < 0.02:
        # a square pavilion's pyramid roof (mo-im): a stoneware finial (jeolbyeongtong) on the apex
        s = max(0.6, min(1.6, short / 0.18))
        zt0 = zr - mahya_en * 0.8
        donel(y, (cx, cy), [(0.0, zt0 - 0.004), (0.014 * s, zt0 - 0.002), (0.016 * s, zt0 + 0.008 * s), (0.01 * s, zt0 + 0.02 * s),
                            (0.005 * s, zt0 + 0.028 * s), (0.009 * s, zt0 + 0.034 * s), (0.0, zt0 + 0.046 * s)], CATI2, n=10)
        tepe = zt0 + 0.046 * s
    if yongmaru and L > 0.02:
        # the main ridge: a white-plastered body with a grey tile cap (it stands proud of the small ridge cap)
        w = hm * 1.5
        c0 = V(cx, cy) - ex * (L + 0.003); c1 = V(cx, cy) + ex * (L + 0.003)
        cubuk(y, V(c0.x, c0.y, zt + w * 0.45), V(c1.x, c1.y, zt + w * 0.45), w, mahya, w * 1.2)
        cubuk(y, V(c0.x, c0.y, zt + w * 1.12), V(c1.x, c1.y, zt + w * 1.12), w * 1.25, CATI2, w * 0.3)
        tepe = max(tepe, zt + w * 1.3)
        if chwidu:
            for sg in (-1, 1):
                p = V(cx, cy) + ex * (sg * L)
                chiwen(y, (p.x, p.y, zt + w * 0.9), (ex.x * sg, ex.y * sg), chwidu, CATI2, CATI)
            tepe = max(tepe, zt + w + 0.055 * chwidu)
    if japsang and tur in ('paljak', 'ujingak'):
        sacak_hayvanlari(y, x0, x1, y0, y1, z, h, sacak, kivrim, yukari, 0.012 if tur == 'paljak' else mahya_en, japsang, j_key, j_key,
                         0.06, 0.06 + 0.04 * japsang)
    return tepe


# ---------------------------------------------------------------- the hall's body
def kiris(y, a, b, z, hb, boya=BOYA, t=0.009):
    """the dancheong beams over a run of columns (changbang green, pyeongbang blue-green above), standing t proud"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    kutu(y, a + nn * t + Z * z - e * t, e, L + 2 * t, 2 * t, hb * 0.55, boya[0], 'onust')
    kutu(y, a + nn * (t * 1.25) + Z * (z + hb * 0.55) - e * (t * 1.25), e, L + 2.5 * t, 2.5 * t, hb * 0.45, boya[1], 'onust')
    # painted end panels (meori-cho): red-and-white bands near the columns, gilt dots in the middle
    nb = max(1, int(round(L / 0.08)))
    for j in range(nb):
        p = a.lerp(b, (j + 0.5) / nb) + nn * (t + 0.0006) + Z * (z + hb * 0.27)
        y.yuz_yon([p - e * 0.01 - Z * hb * 0.12, p + e * 0.01 - Z * hb * 0.12, p + e * 0.01 + Z * hb * 0.12, p - e * 0.01 + Z * hb * 0.12], 'boya_kirmizi', nn)


def gongpo(y, k, zz, h=0.022, adim=0.045, boya=BOYA, kapali=True):
    """bracket sets (gongpo, dapo style: between the columns too) round a CCW rectangle / polygon k from zz: a frieze band
    closing the gap to the roof, stepped blocks projecting from it. Returns the top z"""
    duvarlar(y, k, zz, zz + h, boya[0])
    m = len(k)
    for i in range(m if kapali else m - 1):
        a_, b_ = k[i], k[(i + 1) % m]
        e = (b_ - a_).normalized(); nn = V(e.y, -e.x); L = (b_ - a_).length
        nb = max(2, int(round(L / adim)))
        an = math.atan2(e.y, e.x)
        for j in range(nb + 1):
            p = a_.lerp(b_, j / nb)
            kutu_merkez(y, (p.x + nn.x * 0.006, p.y + nn.y * 0.006), 0.011, 0.012, h * 0.4, boya[1], z0=zz, aci=an, yuzler='onarkasagsolust')
            kutu_merkez(y, (p.x + nn.x * 0.011, p.y + nn.y * 0.011), 0.02, 0.014, h * 0.32, boya[0], z0=zz + h * 0.4, aci=an, yuzler='onarkasagsolust')
            kutu_merkez(y, (p.x + nn.x * 0.016, p.y + nn.y * 0.016), 0.026, 0.012, h * 0.28, 'lake', z0=zz + h * 0.72, aci=an, yuzler='onarkasagsolust')
    return zz + h


def bolme(y, p, q, z0, H, tur, duvar=DUVAR, direk=DIREK, kafes_n=(3, 3)):
    """one bay between two columns: tur 'kapi' (lattice doors, paper behind, a solid panel below), 'pencere' (plaster
    with a lattice window), 'duvar' (plaster framed in red timber), 'acik' (nothing), 'tas' (plain)"""
    p, q = V(p[0], p[1]), V(q[0], q[1])
    e = (q - p).normalized(); nn = V(e.y, -e.x); W = (q - p).length
    if tur == 'acik':
        return
    if tur == 'kapi':
        dikdortgen_acik(y, p, q, z0, H, 0.1, 0.9, 0.0, H - 0.003, (duvar, direk, direk, KAGIT), derin=0.01)
        kafes(y, p, q, z0, 0.1, 0.9, H * 0.3, H - 0.003, KAFES, kafes_n[0] * 2 + 2, kafes_n[1], 0.002, 0.004)
        # the doors' solid lower panels and the mid rail between the two leaves
        L = lambda u, v, d: p + e * (u * W) - nn * d + Z * (z0 + v)
        y.yuz_yon([L(0.1, 0, 0.006), L(0.9, 0, 0.006), L(0.9, H * 0.3, 0.006), L(0.1, H * 0.3, 0.006)], 'lake_koyu', nn)
        y.yuz_yon([L(0.497, H * 0.3, 0.0045), L(0.503, H * 0.3, 0.0045), L(0.503, H - 0.003, 0.0045), L(0.497, H - 0.003, 0.0045)], KAFES, nn)
    elif tur == 'tahta':   # a gate's red plank doors with gilt studs
        dikdortgen_acik(y, p, q, z0, H, 0.08, 0.92, 0.0, H * 0.94, (duvar, direk, direk, 'lake'), derin=0.012)
        L = lambda u, v, d: p + e * (u * W) - nn * d + Z * (z0 + v)
        y.yuz_yon([L(0.497, 0, 0.0115), L(0.503, 0, 0.0115), L(0.503, H * 0.94, 0.0115), L(0.497, H * 0.94, 0.0115)], 'koyu', nn)
        for v in (0.25, 0.5, 0.75):
            for u in (0.2, 0.35, 0.65, 0.8):
                c = L(u, H * 0.94 * v, 0.0112)
                y.yuz_yon([c - e * 0.0025 - Z * 0.0025, c + e * 0.0025 - Z * 0.0025, c + e * 0.0025 + Z * 0.0025, c - e * 0.0025 + Z * 0.0025], 'altin', nn)
    elif tur == 'karanlik':   # an open doorway into the dark inside
        dikdortgen_acik(y, p, q, z0, H, 0.1, 0.9, 0.0, H * 0.86, (duvar, direk, 'ahsap_koyu', 'koyu'), derin=0.014, cerceve=(0.004, direk),
                        ic_kenar=True)
    elif tur == 'pencere':
        dikdortgen_acik(y, p, q, z0, H, 0.16, 0.84, H * 0.36, H * 0.86, (duvar, direk, direk, KAGIT), derin=0.008)
        kafes(y, p, q, z0, 0.16, 0.84, H * 0.36, H * 0.86, KAFES, kafes_n[0] * 2, max(2, kafes_n[1] - 1), 0.002, 0.003)
        cerceve_serit(y, p, q, z0, H, [H * 0.3], direk)
    elif tur == 'duvar':
        duz_duvar(y, p, q, z0, z0 + H, duvar)
        cerceve_serit(y, p, q, z0, H, [H * 0.3, H * 0.7], direk)
    else:
        duz_duvar(y, p, q, z0, z0 + H, duvar)


def cerceve_serit(y, p, q, z0, H, vs, key=DIREK, h=0.006, d=0.0022):
    """horizontal timber rails (inbang) a little proud of a plaster bay at the heights vs"""
    e = (q - p).normalized(); nn = V(e.y, -e.x)
    for v in vs:
        A, B = p + nn * d + Z * (z0 + v - h / 2), q + nn * d + Z * (z0 + v - h / 2)
        y.yuz_yon([A, B, B + Z * h, A + Z * h], key, nn)
        y.yuz_yon([A + Z * h, B + Z * h, B + Z * h - nn * d, A + Z * h - nn * d], key, Z)
        y.yuz_yon([A, B, B - nn * d, A - nn * d], key, -Z)


def govde(y, k, z0, H, bolmeler, r=0.0095, boya=BOYA, band=0.16, direk=DIREK, taban=TAS2, kafes_n=(3, 3), duvar=DUVAR):
    """the walls of a hall round the CCW rectangle k from z0, H high: bolmeler[i] a list of bay types (bolme) along side
    i (its length the bay count), round red columns on square granite bases at the bay lines, painted beams on top"""
    for i in range(4):
        a_, b_ = k[i], k[(i + 1) % 4]
        L = (b_ - a_).length
        tipler = bolmeler[i]
        nb = len(tipler)
        e = (b_ - a_).normalized(); nn = V(e.y, -e.x)
        hb = H * band
        for j, t in enumerate(tipler):
            p, q = a_.lerp(b_, j / nb), a_.lerp(b_, (j + 1) / nb)
            bolme(y, p, q, z0, H - hb, t, duvar, direk, kafes_n)
            if t != 'acik':
                duz_duvar(y, p, q, z0 + H - hb, z0 + H, duvar)   # (behind the beams)
        for j in range(nb):
            pc = a_.lerp(b_, j / nb) + nn * 0.004
            y.prizma((pc.x, pc.y), r, z0 + 0.006, z0 + H - hb * 0.5, direk, n=8, ust=True)
            kutu_merkez(y, (pc.x, pc.y), r * 2.8, r * 2.8, 0.006, taban, z0=z0, yuzler='onarkasagsolust')
        kiris(y, a_, b_, z0 + H - hb, hb, boya)


# ---------------------------------------------------------------- a hall
def kore_salon(y, cx, cy, w, d, z, h, cati_h, sacak=0.08, tur='paljak', kivrim=0.34, yukari=0.04, nx=5, ny=3,
               on='kapi', yan='pencere', arka='duvar', cift=False, alt_yuk=0.05, alt_sacak=None, ic=None, ust_h=None,
               gidan=None, japsang=0, chwidu=1.0, levha=True, mahya_en=0.014, r=0.0095, acik_taban='ahsap_acik', duvar=DUVAR,
               direk=DIREK, ust_bolme='pencere', gongpo_h=0.022, ic_direk=True):
    """a Joseon timber hall w x d (front to -y) from z: optional granite stylobate gidan = (height, key, steps), the
    walls (on / yan / arka: bay types of the front, the sides, the back; 'acik' = an open hall with a wooden floor and
    inner columns), bracket sets, the roof (tur), cift: a second storey over a pent roof (Geunjeongjeon). Returns the top z"""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2
    if gidan:
        gh, gk, adim = gidan
        m = 0.035
        kutu(y, V(x0 - m, y0 - m, z), X, w + 2 * m, d + 2 * m, gh, gk)
        silme(y, dikdortgen(x0 - m, x1 + m, y0 - m, y1 + m), z + gh - 0.005, 0.005, 0.004, TAS2, 'duz')
        silme(y, dikdortgen(x0 - m, x1 + m, y0 - m, y1 + m), z, 0.008, 0.004, gk, 'kaide')
        if adim:
            for sx in ([0.0] if adim == 1 else [-w / 3, 0.0, w / 3]):
                merdiven(y, (cx + sx, y0 - m - gh * 1.15), math.pi / 2, 0.08 if sx == 0 else 0.06, z, z + gh, max(2, int(gh / 0.012)), key=gk)
        z += gh
    k = dikdortgen(x0, x1, y0, y1)
    tip = lambda t, n: [t] * n if isinstance(t, str) else list(t)
    bol = [tip(on, nx), tip(yan, ny), tip(arka, nx), tip(yan, ny)]
    acik = all(t == 'acik' for t in bol[0] + bol[1] + bol[2] + bol[3])
    if acik:
        # an open hall: a raised wooden floor, the inner columns, a coffered ceiling seen from below
        kutu(y, V(x0 - 0.004, y0 - 0.004, z), X, w + 0.008, d + 0.008, 0.008, acik_taban, 'ust')
        z += 0.008
        if ic_direk:
            for i in range(1, nx):
                for j in range(1, ny):
                    if i in (1, nx - 1) or j in (1, ny - 1):
                        px, py = x0 + w * i / nx, y0 + d * j / ny
                        y.prizma((px, py), r * 1.05, z, z + h * 0.9, direk, n=8)
    govde(y, k, z, h, bol, r, direk=direk, duvar=duvar)
    zt = z + h
    if acik:
        y.yuz_yon([V(p.x, p.y, zt - h * 0.16 * 0.5) for p in k], ALT, -Z)
    zc = gongpo(y, k, zt, gongpo_h)
    if levha and not acik and not cift:
        hyeonpan(y, (cx, y0), zt - h * 0.08, min(0.08, w * 0.16))
    if cift:
        ic = ic if ic is not None else min(w, d) * 0.12
        ust_h = ust_h if ust_h is not None else h * 0.42
        asx = alt_sacak if alt_sacak is not None else sacak * 0.9
        a_, b_ = w / 2 + asx, d / 2 + asx
        mm = min(a_, b_)
        r_ust = 1 - (min(w, d) / 2 - ic - 0.012) / mm
        hfull = egim_icin(alt_yuk, r_ust, kivrim * 0.6)
        cati_kirma(y, x0, x1, y0, y1, zc, hfull, asx, CATI, MAHYA, 0.012, kivrim * 0.6, yukari, ALT, ns=max(4, int(w / 0.06)), nr=3,
                   r_ust=r_ust, mahya_en=0.012)
        k2 = dikdortgen(x0 + ic, x1 - ic, y0 + ic, y1 - ic)
        z2 = zc + alt_yuk
        duvarlar(y, k2, zc, z2 + 0.004, 'lake_koyu')
        n2x, n2y = max(3, nx - 2), max(1, ny - 2)
        govde(y, k2, z2 + 0.004, ust_h, [[ust_bolme] * n2x, [ust_bolme] * n2y, [ust_bolme] * n2x, [ust_bolme] * n2y], r * 0.8, band=0.24,
              kafes_n=(3, 2))
        zc = gongpo(y, k2, z2 + 0.004 + ust_h, gongpo_h)
        if levha:
            hyeonpan(y, (cx, y0 + ic), z2 + 0.004 + ust_h * 0.86, min(0.09, w * 0.14))
        x0, x1, y0, y1 = x0 + ic, x1 - ic, y0 + ic, y1 - ic
    return kore_cati(y, x0, x1, y0, y1, zc, cati_h, sacak, tur, kivrim, yukari, japsang, chwidu, mahya_en)


def hyeonpan(y, p, z, en, key='koyu', cer='altin', yon=-math.pi / 2):
    """the name board under the eaves (hyeonpan): a dark board in a gilt frame, hung a little forward and tilted"""
    nn = V(math.cos(yon), math.sin(yon)); e = V(-nn.y, nn.x)
    c = V(p[0], p[1]) + nn * 0.022
    hh = en * 0.42
    kutu(y, c - e * (en / 2 + 0.003) + nn * 0.004 + Z * (z - hh / 2 - 0.003), e, en + 0.006, 0.008, hh + 0.006, cer, 'onsagsolust')
    kutu(y, c - e * (en / 2 - 0.002) + nn * 0.0055 + Z * (z - hh / 2 + 0.002), e, en - 0.004, 0.002, hh - 0.004, key, 'on')
    for k in range(3):   # the gilt characters
        q = c - e * (en * 0.3 - k * en * 0.3) + nn * 0.0058 + Z * z
        y.yuz_yon([q - e * 0.006 - Z * hh * 0.28, q + e * 0.006 - Z * hh * 0.28, q + e * 0.006 + Z * hh * 0.28, q - e * 0.006 + Z * hh * 0.28], cer, nn)


# ---------------------------------------------------------------- a cloister gallery
def heonggak(y, a, b, en, z, h, cati_h, adim=0.075, sacak=0.03, dis='duvar', uc_kapat=(False, False), taban_h=0.012, alcak=False,
             cati=True):
    """a roofed corridor a->b: its outer wall on the line a->b (facing the right, outward: plaster in red frames with small
    windows), open on the inner side (left) with a row of columns, a granite floor, a hipped grey roof. alcak: the roof a
    little lower and flatter (a run crossing another at a corner: it hides under the other's roof). Returns the top z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    ic = -nn
    t = 0.012
    # the floor slab (granite) a little proud of the courtyard
    kutu(y, a - e * 0.002 + nn * 0.004 + Z * z, e, L + 0.004, en + 0.008, taban_h, TAS, 'onarkasagsolust')
    zb = z + 0.012
    nb = max(1, int(round(L / adim)))
    for j in range(nb):
        p, q = a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb)
        bolme(y, p, q, zb, h * 0.84, 'pencere' if (dis == 'pencere' and j % 2) else 'duvar')
        duz_duvar(y, q + ic * t, p + ic * t, zb, zb + h, DUVAR)   # the wall's inner face
    duz_duvar(y, a, b, zb + h * 0.84, zb + h, DUVAR)
    for s, uc in ((0, uc_kapat[0]), (1, uc_kapat[1])):   # wall ends (uc: a full end wall across the corridor)
        p = a if s == 0 else b
        yon = -e if s == 0 else e
        w_ = en if uc else t
        pts = [p + Z * zb, p + ic * w_ + Z * zb, p + ic * w_ + Z * (zb + h), p + Z * (zb + h)]
        y.yuz_yon(pts, DUVAR, yon)
        if uc:
            y.yuz_yon([q - yon * t for q in pts], DUVAR, -yon)
            if s == 1: cerceve_serit(y, p, p + ic * w_, zb, h * 0.84, [h * 0.3, h * 0.6])
            else: cerceve_serit(y, p + ic * w_, p, zb, h * 0.84, [h * 0.3, h * 0.6])
    # inner columns and the beam over them, posts against the wall
    for j in range(nb + 1):
        pc = a.lerp(b, j / nb) + ic * (en - 0.008)
        y.prizma((pc.x, pc.y), 0.0065, zb, zb + h, DIREK, n=6)
        kutu_merkez(y, (pc.x, pc.y), 0.017, 0.017, 0.005, TAS2, z0=zb, yuzler='onarkasagsolust')
        pw = a.lerp(b, j / nb) + nn * 0.003
        kutu_merkez(y, (pw.x, pw.y), 0.01, 0.006, h, DIREK, z0=zb, aci=math.atan2(e.y, e.x), yuzler='onarkasagsol')
    ai, bi = a + ic * (en - 0.008), b + ic * (en - 0.008)
    kiris(y, bi, ai, zb + h * 0.84, h * 0.16, BOYA, 0.007)
    # the ceiling (seen through the open side) and the roof
    zt_ = zb + h * 0.84 - (0.002 if alcak else 0.0)
    y.yuz_yon([a + Z * zt_, b + Z * zt_, bi + Z * zt_, ai + Z * zt_], ALT, -Z)
    if not cati:   # (one roof over the whole run of galleries: heonggak_cati)
        return zb + h
    xs, ys = [a.x, b.x, ai.x, bi.x], [a.y, b.y, ai.y, bi.y]
    return kore_cati(y, min(xs), max(xs), min(ys), max(ys), zb + h - (0.006 if alcak else 0.0), cati_h * (0.82 if alcak else 1.0), sacak, 'ujingak', 0.3, 0.012, 0, 0, 0.008,
                     ns=max(4, int(L / 0.09)), nr=3, yongmaru=False, mahya=CATI2 if alcak else MAHYA)


def heonggak_cati(y, yol, en, z, h, sacak=0.03, kivrim=0.3, yukari=0.014, cati=CATI, mahya=MAHYA, alt=ALT, mahya_en=0.008,
                  nr=4, adim=0.05, kal=0.01, uclar=(True, True)):
    """one continuous roof over a run of cloister galleries (heonggak(..., cati=False)) along the polyline yol of their
    outer wall lines (outward to the right, as heonggak's a->b): the slopes mitred at the corners (a hip on the outer
    corner, a valley on the inner one: a real L-shaped gallery roof), hipped at the open ends (uclar), the outer corners
    and the ends lifted a little (yukari); the ridge and the hips capped (mahya). en: the gallery depth as given to
    heonggak, z: the wall top. Returns the top z"""
    P = [V(p[0], p[1]) for p in yol]
    n = len(P)
    W = en - 0.008
    E = []
    for i in range(n - 1):
        e = P[i + 1] - P[i]; e.z = 0; e.normalize(); E.append(e)
    Oe, Wo, R, Wi, Ie = (disa(P, d, False) for d in (sacak, 0.0, -W / 2, -W, -(W + sacak)))
    for k, e, s in ((0, E[0], -1), (n - 1, E[-1], 1)):
        if uclar[0 if k == 0 else 1]:
            Oe[k] = Oe[k] + e * (s * sacak); Ie[k] = Ie[k] + e * (s * sacak)
            R[k] = R[k] - e * (s * W / 2)
    disbukey = [i for i in range(1, n - 1) if E[i - 1].x * E[i].y - E[i - 1].y * E[i].x > 0]
    kalk = [Oe[i] for i in disbukey]
    if uclar[0]: kalk += [Oe[0], Ie[0]]
    if uclar[1]: kalk += [Oe[-1], Ie[-1]]
    Lr = 0.11

    def zf(p, r):
        lift = sum(max(0.0, 1 - (V(p.x, p.y) - V(c.x, c.y)).length / Lr) ** 2 for c in kalk)
        return z + h * ((1 - kivrim) * r + kivrim * r * r) + yukari * min(1.0, lift) * (1 - r) ** 1.5

    b = W / 2 + sacak
    rs = sacak / b
    rr = sorted({0.0, rs, *[rs + (1 - rs) * k / nr for k in range(nr + 1)]})
    S = lambda p, r: V(p.x, p.y, zf(p, r))

    def yamac(E0, E1, R0, R1, W0, W1, dis):
        """one slope: eave E0->E1 up to the ridge R0->R1, its soffit back to the wall line W0->W1; dis: outward"""
        L = max((E1 - E0).length, (R1 - R0).length)
        ns = max(2, int(round(L / adim)))
        G = [[S(E0.lerp(E1, u / ns).lerp(R0.lerp(R1, u / ns), r), r) for r in rr] for u in range(ns + 1)]
        for u in range(ns):
            for j in range(len(rr) - 1):
                q = [G[u][j], G[u + 1][j], G[u + 1][j + 1], G[u][j + 1]]
                if (q[2] - q[3]).length < 1e-7: q = q[:3]
                y.yuz_yon(q, cati, Z)
            e0, e1 = G[u][0], G[u + 1][0]
            y.yuz_yon([e0, e1, e1 - Z * kal, e0 - Z * kal], alt, dis)
            w0, w1 = W0.lerp(W1, u / ns), W0.lerp(W1, (u + 1) / ns)
            y.yuz_yon([e0 - Z * kal, e1 - Z * kal, V(w1.x, w1.y, z), V(w0.x, w0.y, z)], alt, -Z)

    for i in range(n - 1):
        nn = V(E[i].y, -E[i].x)
        yamac(Oe[i], Oe[i + 1], R[i], R[i + 1], Wo[i], Wo[i + 1], nn)
        yamac(Ie[i + 1], Ie[i], R[i + 1], R[i], Wi[i + 1], Wi[i], -nn)
    for k, e, s in ((0, E[0], -1), (n - 1, E[-1], 1)):
        if uclar[0 if k == 0 else 1]:   # the hipped end
            A, B, WA, WB = (Ie[k], Oe[k], Wi[k], Wo[k]) if s < 0 else (Oe[k], Ie[k], Wo[k], Wi[k])
            yamac(A, B, R[k], R[k], WA, WB, e * s)
    # the caps: the ridge, the outer hips, the end hips (closely sampled: they follow the curve and the lift)
    zr = z + h
    for i in range(n - 1):
        pa = V(R[i].x, R[i].y, zr + mahya_en * 0.3) - E[i] * (mahya_en * 0.5 if i else 0.0)
        pb = V(R[i + 1].x, R[i + 1].y, zr + mahya_en * 0.3) + E[i] * (mahya_en * 0.5 if i < n - 2 else 0.0)
        cubuk(y, pa, pb, mahya_en, mahya)
    kalcalar = [(Oe[i], R[i]) for i in disbukey]
    if uclar[0]: kalcalar += [(Oe[0], R[0]), (Ie[0], R[0])]
    if uclar[1]: kalcalar += [(Oe[-1], R[-1]), (Ie[-1], R[-1])]
    for c, r_ in kalcalar:
        pts = [S(c.lerp(r_, t), t) + Z * (mahya_en * 0.3) for t in [k / 10 for k in range(11)]]
        for k in range(10):
            cubuk(y, pts[k], pts[k + 1], mahya_en * 0.8, mahya)
    return zr + mahya_en * 0.8


# ---------------------------------------------------------------- ground and water
def zemin_delikli(y, x0, x1, y0, y1, h, delikler=(), key='tas_koyu', ust='zemin', ust_fn=None):
    """a ground slab with rectangular holes (ponds, docks): the sides, and the top as the grid cells outside the holes.
    ust_fn(cx, cy) -> key: a key for each cell (courtyards, paths). Returns h"""
    kutu(y, V(x0, y0, 0), X, x1 - x0, y1 - y0, h, key, 'onarkasagsol')
    silme(y, dikdortgen(x0, x1, y0, y1), h - 0.008, 0.008, 0.006, key, 'duz')
    xs = sorted({x0, x1, *[d[0] for d in delikler], *[d[1] for d in delikler]})
    ys = sorted({y0, y1, *[d[2] for d in delikler], *[d[3] for d in delikler]})
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            mx, my = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
            if any(d[0] < mx < d[1] and d[2] < my < d[3] for d in delikler):
                continue
            y.yuz_yon([V(xs[i], ys[j], h), V(xs[i + 1], ys[j], h), V(xs[i + 1], ys[j + 1], h), V(xs[i], ys[j + 1], h)],
                      ust_fn(mx, my) if ust_fn else ust, Z)
    return h


def gol(y, x0, x1, y0, y1, z, zs, key=TAS, su='su', taban='kaya_koyu'):
    """a pond in a hole of the ground slab: granite embankment walls facing the water from z down to below the water at zs,
    the water surface, and a coping round the rim"""
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, [k[3], k[2], k[1], k[0]], zs - 0.01, z, key)
    y.yuz_yon([V(p.x, p.y, zs) for p in k], su, Z)
    silme(y, disa(k, 0.006), z, 0.006, 0.006, TAS2, 'duz')


def dalgalar(y, x0, x1, y0, y1, zw, n=20, tohum=3, boy=0.03, haric=()):
    """light ripple strokes on a water surface (flat slivers a hair above it); haric: rectangles to keep clear"""
    import random
    r = random.Random(tohum)
    k = 0
    while k < n:
        x, yy = r.uniform(x0, x1), r.uniform(y0, y1)
        if any(h[0] - 0.03 < x < h[1] + 0.03 and h[2] - 0.01 < yy < h[3] + 0.01 for h in haric):
            continue
        L = boy * r.uniform(0.6, 1.3)
        y.yuz_yon([V(x - L / 2, yy, zw + 0.0012), V(x + L / 2, yy, zw + 0.0012), V(x + L * 0.3, yy + 0.003, zw + 0.0012),
                   V(x - L * 0.3, yy + 0.003, zw + 0.0012)], 'beyaz', Z)
        k += 1


# ---------------------------------------------------------------- small pieces
def kore_korkuluk(y, kose, z, h=0.024, kapali=True, adim=0.05, key='lake', ust=BOYA[0]):
    """a timber railing (gyeranan) along a polyline / polygon: posts with knobs, a top rail, a lower rail and baluster
    panels (closed boxes)"""
    P = ornekle(kose, adim, kapali)
    n = len(P)
    for i in (range(n) if kapali else range(n - 1)):
        a_, b_ = P[i], P[(i + 1) % n]
        Ln = (b_ - a_).length
        if Ln < 0.008:
            continue
        e = (b_ - a_) / Ln
        cubuk(y, V(a_.x, a_.y, z + h * 0.92), V(b_.x, b_.y, z + h * 0.92), 0.004, key, 0.004)
        cubuk(y, V(a_.x, a_.y, z + h * 0.3), V(b_.x, b_.y, z + h * 0.3), 0.003, ust, 0.006)
        m = a_.lerp(b_, 0.5)
        cubuk(y, V(m.x, m.y, z + h * 0.3), V(m.x, m.y, z + h * 0.9), 0.004, ust, 0.003)
    for i, p in enumerate(P):
        cubuk(y, V(p.x, p.y, z), V(p.x, p.y, z + h), 0.0055, key)
        kure(y, (p.x, p.y, z + h + 0.003), 0.0035, key, n=6, kat=3)


def haetae(y, x, yy, z, aci=0.0, s=1.0, key=TAS2, kaide_key=TAS):
    """a haetae (guardian beast) sitting on a pedestal, a little bulkier than the Chinese lion, a horn on the head"""
    with parca(y, (x, yy, z), aci, s):
        kutu_merkez(y, (0, 0), 0.038, 0.026, 0.02, kaide_key)
        silme(y, dikdortgen(-0.019, 0.019, -0.013, 0.013), 0.016, 0.004, 0.003, kaide_key)
        kutu_merkez(y, (0.007, 0), 0.022, 0.02, 0.012, key, z0=0.02)
        cubuk(y, V(-0.002, 0, 0.024), V(-0.009, 0, 0.044), 0.016, key, 0.018)
        kure(y, (-0.011, 0, 0.05), 0.012, key, n=8, kat=4)
        kure(y, (-0.021, 0, 0.047), 0.0055, key, n=6, kat=3)
        cubuk(y, V(-0.012, 0, 0.06), V(-0.016, 0, 0.067), 0.003, key)
        for sy in (-1, 1):
            cubuk(y, V(-0.013, sy * 0.006, 0.02), V(-0.014, sy * 0.006, 0.034), 0.0055, key)
            kure(y, (-0.007, sy * 0.009, 0.059), 0.003, key, n=5, kat=3)   # the curls of the mane


def sonamu(y, x, yy, z, boy=0.16, tohum=0, govde='ahsap', key='yesil_koyu'):
    """a Korean red pine (sonamu): a leaning, twisting reddish trunk and flat, layered cloud-like crowns"""
    import random
    r = random.Random(tohum)
    a = r.uniform(0, TAU)
    d = V(math.cos(a), math.sin(a))
    p0 = V(x, yy, z - 0.004)
    p1 = p0 + d * (boy * 0.08) + Z * (boy * 0.4)
    p2 = p1 - d * (boy * 0.05) + V(-d.y, d.x) * (boy * 0.05) + Z * (boy * 0.35)
    boru(y, [p0, p1, p2], boy * 0.035, 'kirmizi', n=6, r_son=boy * 0.02)
    for (q, rr, hh) in ((p2 + Z * (boy * 0.04), 0.3, 0.1), (p1 + d * (boy * 0.15) + Z * (boy * 0.08), 0.22, 0.08),
                        (p1 - d * (boy * 0.12) + Z * (boy * 0.2), 0.2, 0.08)):
        donel(y, (q.x, q.y), [(0.0, q.z - boy * hh * 0.4), (boy * rr, q.z - boy * hh * 0.2), (boy * rr * 0.9, q.z + boy * hh * 0.3),
                              (boy * rr * 0.4, q.z + boy * hh * 0.6), (0.0, q.z + boy * hh * 0.65)], key, n=8, kat=r.uniform(0, 1))
        boru(y, [p1 if q.z < p2.z else p2, q - Z * (boy * hh * 0.2)], boy * 0.012, 'kirmizi', n=4)


def kore_sur(y, yol, z0, h, t=0.032, key=TAS, ust=DUVAR, kapali=False, cati=CATI):
    """a palace wall along a polyline (outer face to the right): dressed granite below, a plastered top band, a small
    grey-tiled coping with a white ridge; end caps on an open run"""
    O = [V(p[0], p[1]) for p in yol]
    n = len(O)
    I = disa(O, -t, kapali)
    Oe, M, Ie = disa(O, 0.013, kapali), disa(O, -t / 2, kapali), disa(O, -t - 0.013, kapali)
    m = n if kapali else n - 1
    zu = z0 + h * 0.62
    zc, zr = z0 + h - 0.003, z0 + h + 0.02
    for i in range(m):
        j = (i + 1) % n
        e = (O[j] - O[i]); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
        duz_duvar(y, O[i], O[j], z0, zu, key)
        duz_duvar(y, I[j], I[i], z0, zu, key)
        duz_duvar(y, O[i], O[j], zu, z0 + h, ust)
        duz_duvar(y, I[j], I[i], zu, z0 + h, ust)
        y.yuz_yon([Oe[i] + Z * zc, Oe[j] + Z * zc, M[j] + Z * zr, M[i] + Z * zr], cati, nn + Z * 1.2)
        y.yuz_yon([Ie[j] + Z * zc, Ie[i] + Z * zc, M[i] + Z * zr, M[j] + Z * zr], cati, -nn + Z * 1.2)
        y.yuz_yon([O[i] + Z * (z0 + h), O[j] + Z * (z0 + h), Oe[j] + Z * zc, Oe[i] + Z * zc], ALT, -Z)
        y.yuz_yon([I[j] + Z * (z0 + h), I[i] + Z * (z0 + h), Ie[i] + Z * zc, Ie[j] + Z * zc], ALT, -Z)
        cubuk(y, M[i] + Z * (zr + 0.003), M[j] + Z * (zr + 0.003), 0.008, MAHYA)
    if not kapali:
        for k, s in ((0, -1), (n - 1, 1)):
            e = (O[1] - O[0]) if k == 0 else (O[-1] - O[-2]); e.z = 0; e.normalize()
            y.yuz_yon([O[k] + Z * z0, I[k] + Z * z0, I[k] + Z * zu, O[k] + Z * zu], key, e * s)
            y.yuz_yon([O[k] + Z * zu, I[k] + Z * zu, I[k] + Z * (z0 + h), O[k] + Z * (z0 + h)], ust, e * s)
            y.yuz_yon([Oe[k] + Z * zc, O[k] + Z * (z0 + h), I[k] + Z * (z0 + h), Ie[k] + Z * zc, M[k] + Z * zr], cati, e * s)


def tas_kopru(y, c, L, en, z, kemer_h=0.018, key=TAS2, yan_key=TAS, aci=math.pi / 2, dibe=0.03, korkuluklu=True):
    """a humped granite bridge (Yeongjegyo) at c along angle aci (L long, en wide, ends at z): the deck rising over a
    rainbow arch painted dark on its sides, solid parapets with lotus-capped posts, the piers going down dibe"""
    n = 8
    pr = [(-L / 2 + L * k / n, kemer_h * math.sin(math.pi * k / n)) for k in range(n + 1)]
    with parca(y, (c[0], c[1], z), aci - math.pi / 2):
        # (local: the bridge runs along y, its width along x)
        for k in range(n):
            (ya, za), (yb, zb) = pr[k], pr[k + 1]
            y.yuz_yon([V(-en / 2, ya, za + 0.006), V(en / 2, ya, za + 0.006), V(en / 2, yb, zb + 0.006), V(-en / 2, yb, zb + 0.006)], key, Z)
        for sx in (-1, 1):
            prof = [V(sx * en / 2, pr[0][0], -dibe)] + [V(sx * en / 2, ya, za + 0.006) for ya, za in pr] + [V(sx * en / 2, pr[-1][0], -dibe)]
            y.yuz_yon(prof, yan_key, V(sx, 0, 0))
            arc = [V(sx * (en / 2 + 0.0015), -L * 0.3 + L * 0.6 * k / 8, -dibe + (dibe + kemer_h * 0.6) * math.sin(math.pi * k / 8)) for k in range(9)]
            y.yuz_yon(arc, 'koyu', V(sx, 0, 0))
            if korkuluklu:
                for k in range(n):
                    (ya, za), (yb, zb) = pr[k], pr[k + 1]
                    cubuk(y, V(sx * (en / 2 - 0.004), ya, za + 0.014), V(sx * (en / 2 - 0.004), yb, zb + 0.014), 0.006, key, 0.014)
                for k in (0, 2, 4, 6, 8):
                    ya, za = pr[k]
                    dikme(y, V(sx * (en / 2 - 0.004), ya), V(0, 1), za + 0.006, 0.02, key, 0.0075)
        for ya, s in ((-L / 2, -1), (L / 2, 1)):
            y.yuz_yon([V(-en / 2, ya, -dibe), V(en / 2, ya, -dibe), V(en / 2, ya, 0.006), V(-en / 2, ya, 0.006)], key, V(0, s, 0))


def kutu3(y, c, ex, ey, ez, sx, sy, sz, key, yuzler=None):
    """a box centred at c along three axes, sizes sx, sy, sz; every face wound outward. yuzler: which of
    '+x -x +y -y +z -z' to draw (default all)"""
    c = Vector(c); ex, ey, ez = Vector(ex).normalized(), Vector(ey).normalized(), Vector(ez).normalized()
    P = lambda i, j, k: c + ex * (sx / 2 * i) + ey * (sy / 2 * j) + ez * (sz / 2 * k)
    yz = yuzler or ('+x', '-x', '+y', '-y', '+z', '-z')
    for ad, ax, q in (('+x', ex, [P(1, -1, -1), P(1, 1, -1), P(1, 1, 1), P(1, -1, 1)]),
                      ('-x', -ex, [P(-1, -1, -1), P(-1, 1, -1), P(-1, 1, 1), P(-1, -1, 1)]),
                      ('+y', ey, [P(-1, 1, -1), P(1, 1, -1), P(1, 1, 1), P(-1, 1, 1)]),
                      ('-y', -ey, [P(-1, -1, -1), P(1, -1, -1), P(1, -1, 1), P(-1, -1, 1)]),
                      ('+z', ez, [P(-1, -1, 1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, 1)]),
                      ('-z', -ez, [P(-1, -1, -1), P(1, -1, -1), P(1, 1, -1), P(-1, 1, -1)])):
        if ad in yz:
            y.yuz_yon(q, key, ax)


def levha(y, pts, key, yon, kalin=0.0012, kenar=None):
    """a thin closed slab (sail, sign, target): the polygon pts as a front toward yon and a back kalin behind it, with its rim"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    on = [p + yon * (kalin / 2) for p in pts]; ar = [p - yon * (kalin / 2) for p in pts]
    y.yuz_yon(on, key, yon); y.yuz_yon(ar, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        y.yuz_yon([on[i], on[j], ar[j], ar[i]], kenar or key, (pts[i] + pts[j]) / 2 - c)


def teker(y, c, eks, r, en=0.006, key='ahsap', jant='ahsap_koyu', parmak=8, n=14):
    """a spoked cart wheel at c, its axle along eks: a rim (tread, inner face, both sides), a hub, spokes"""
    c = Vector(c); eks = Vector(eks).normalized()
    u = Z.cross(eks)
    if u.length < 1e-4: u = X.copy()
    u.normalize(); w = eks.cross(u).normalized()
    R = lambda rr, i, s: c + (u * math.cos(TAU * i / n) + w * math.sin(TAU * i / n)) * rr + eks * (s * en / 2)
    r0 = r * 0.82
    for i in range(n):
        j = (i + 1) % n
        yuz_dis(y, [R(r, i, -1), R(r, j, -1), R(r, j, 1), R(r, i, 1)], jant, c)
        y.yuz_yon([R(r0, i, 1), R(r0, j, 1), R(r0, j, -1), R(r0, i, -1)], key, c - (R(r0, i, 0) + R(r0, j, 0)) / 2)
        for s in (-1, 1):
            y.yuz_yon([R(r0, i, s), R(r0, j, s), R(r, j, s), R(r, i, s)], key, eks * s)
    boru(y, [c - eks * (en * 0.9), c + eks * (en * 0.9)], r * 0.18, jant, n=8)
    for k in range(parmak):
        a = TAU * k / parmak
        d = u * math.cos(a) + w * math.sin(a)
        cubuk(y, c + d * (r * 0.15), c + d * (r0 * 1.02), r * 0.07, key)


def hwacha(y, x, yy, z, aci=0.0, egim=0.55, s=1.0, oklu=True, ates=False, rafli=True, tohum=0):
    """a hwacha: a two-wheeled cart, its long handles resting on the ground behind, the launcher box (100 singijeon
    tubes in a 10 x 10 grid) tilted up egim on the frame, the arrows poking out (rafli=False: the bare cart). Faces +x
    (aci turns it). Returns the launcher's mouth centre and its direction (world), or None"""
    import random
    rr = random.Random(tohum)
    r = 0.028
    sonuc = None
    with parca(y, (x, yy, z), aci, s):
        for sy in (-1, 1):
            teker(y, V(0, sy * 0.04, r), Y, r, 0.006)
        cubuk(y, V(0, -0.046, r), V(0, 0.046, r), 0.006, 'ahsap_koyu')
        for sy in (-1, 1):   # the frame: two rails over the axle, the handles resting on the ground behind
            cubuk(y, V(0.045, sy * 0.028, r + 0.008), V(-0.03, sy * 0.028, r + 0.002), 0.008, 'ahsap', 0.007)
            cubuk(y, V(-0.03, sy * 0.028, r + 0.002), V(-0.12, sy * 0.022, 0.004), 0.007, 'ahsap', 0.006)
        for xx in (0.035, -0.015):
            cubuk(y, V(xx, -0.03, r + 0.008), V(xx, 0.03, r + 0.008), 0.006, 'ahsap_koyu', 0.005)
        cubuk(y, V(0.04, 0, r + 0.008), V(0.05, 0, 0.0), 0.006, 'ahsap_koyu')   # the front prop
        if rafli:
            f = V(math.cos(egim), 0, math.sin(egim))          # the launcher's axis (the tubes)
            up = V(-math.sin(egim), 0, math.cos(egim))
            c = V(0.008, 0, r + 0.034)
            L, B, H = 0.07, 0.058, 0.05
            kutu3(y, c, f, Y, up, L, B, H, 'ahsap')
            for t in (-0.3, 0.3):   # iron bands
                kutu3(y, c + f * (L * t), f, Y, up, 0.004, B + 0.003, H + 0.003, 'demir', ('+y', '-y', '+z', '-z'))
            mf = c + f * (L / 2 + 0.0006)
            for i in range(10):   # the mouth: a grid of dark tube ends
                for j in range(10):
                    q = mf + Y * (-B / 2 + B * (i + 0.5) / 10) + up * (-H / 2 + H * (j + 0.5) / 10)
                    hw, hh = B / 10 * 0.32, H / 10 * 0.32
                    y.yuz_yon([q - Y * hw - up * hh, q + Y * hw - up * hh, q + Y * hw + up * hh, q - Y * hw + up * hh], 'koyu', f)
            for sy in (-1, 1):   # the props holding it up
                cubuk(y, V(-0.02, sy * 0.022, r + 0.008), c - f * (L * 0.3) - up * (H * 0.5) + Y * (sy * 0.022), 0.005, 'ahsap_koyu')
            if oklu:
                for i in range(5):
                    for j in range(5):
                        if rr.random() < 0.3:
                            continue
                        q = mf + Y * (-B / 2 + B * (2 * i + 0.9) / 10) + up * (-H / 2 + H * (2 * j + 0.9) / 10)
                        ln = 0.012 + rr.uniform(0, 0.01)
                        cubuk(y, q - f * 0.002, q + f * ln, 0.0022, 'kece')
                        cubuk(y, q + f * ln, q + f * (ln + 0.006), 0.0012, 'demir')
            sonuc = (c + f * (L / 2), f)
            if ates:   # smoke billowing from the rear of the launcher
                for k in range(7):
                    kure(y, (c.x - f.x * (L / 2 + 0.008 + k * 0.011), rr.uniform(-0.016, 0.016) * (1 + k * 0.3), c.z - f.z * (L / 2) + k * 0.007 + k * k * 0.0012),
                         0.006 + k * 0.0026, 'duman', n=7, kat=4)
    if sonuc:
        ca, sa = math.cos(aci), math.sin(aci)
        W = lambda p: V(x + s * (ca * p.x - sa * p.y), yy + s * (sa * p.x + ca * p.y), z + s * p.z)
        return W(sonuc[0]), V(ca * sonuc[1].x, sa * sonuc[1].x, sonuc[1].z)
    return None


def alev(y, p, yon, L, r):
    """a little flame cone at p pointing along yon"""
    p = Vector(p); yon = Vector(yon).normalized()
    u = Z.cross(yon)
    if u.length < 1e-4: u = X.copy()
    u.normalize(); w = yon.cross(u)
    ring = [p + (u * math.cos(TAU * i / 6) + w * math.sin(TAU * i / 6)) * r for i in range(6)]
    tip = p + yon * L
    for i in range(6):
        yuz_dis(y, [ring[i], ring[(i + 1) % 6], tip], 'turuncu', p + yon * (L * 0.3))
    y.yuz_yon(ring, 'boya_sari', -yon)


def ok_izi(y, p0, p1, tepe, n=10, r0=0.0035, r1=0.0012, duman='kece', ok=True):
    """a rocket arrow's flight: a smoke trail on a parabola from p0 over the height tepe to p1, the arrow at its end
    trailing a flame. The trail is soft: a chain of overlapping puffs, broad and loose where the smoke is old (near the
    launcher), narrowing to a thin wisp behind the arrow (r0: the scale of the old puffs, r1 of the young end; duman
    'kece' (the old call) is drawn as the soft-shadowed 'buhar'). Returns the end point"""
    import random
    p0, p1 = Vector(p0), Vector(p1)
    duman = 'buhar' if duman == 'kece' else duman
    d = p1 - p0
    yol = lambda t: V(p0.x + d.x * t, p0.y + d.y * t, p0.z + d.z * t + tepe * 4 * t * (1 - t))
    pts = [yol(k / n) for k in range(n + 1)]
    rr = random.Random(int(abs(p0.x * 1000 + p1.x * 7919 + p1.y * 104729)) % 100000)
    # the trail: one tube narrowing from the broad old smoke to a thin wisp behind the arrow
    t0 = 0.02
    ra, rb = r0 * 1.5, r1 * 0.45
    boru(y, [yol(t0 + (1 - t0) * k / 16) for k in range(17)], ra, duman, n=7, r_son=rb)
    # billows on its old part: overlapping puffs a little broader than the tube, drifting up and aside as they age
    L = sum((pts[k + 1] - pts[k]).length for k in range(n))
    t = t0
    while t < 0.32:
        yas = 1 - t / 0.32
        r = (ra + (rb - ra) * (t - t0) / (1 - t0)) * rr.uniform(1.2, 1.6)
        q = yol(t) + V(rr.uniform(-1, 1), rr.uniform(-1, 1), rr.uniform(0, 1.0)) * (r * 0.3 * yas)
        kure(y, (q.x, q.y, q.z), r, duman, n=7, kat=4)
        t += r * 0.9 / L
    if ok:
        e = (pts[-1] - pts[-2]).normalized()
        a = pts[-1]
        cubuk(y, a, a + e * 0.032, 0.0022, 'ahsap_acik')
        cubuk(y, a + e * 0.016, a + e * 0.028, 0.0048, 'kece')
        cubuk(y, a + e * 0.032, a + e * 0.038, 0.0016, 'demir')
        alev(y, a, -e, 0.014, 0.0045)
    return pts[-1]


def ok_demeti(y, x, yy, z, aci=0.0, n=3, L=0.08):
    """bundles of finished arrows on a low rack"""
    with parca(y, (x, yy, z), aci):
        for sx in (-1, 1):
            kutu_merkez(y, (sx * L * 0.3, 0), 0.008, 0.05, 0.01, 'ahsap_koyu')
        for k in range(n):
            yc = -0.016 + k * 0.016
            boru(y, [V(-L / 2, yc, 0.016), V(L / 2, yc, 0.016)], 0.0055, 'ahsap_acik', n=6)
            for xx in (-L * 0.38, L * 0.38):
                boru(y, [V(xx - 0.003, yc, 0.016), V(xx + 0.003, yc, 0.016)], 0.0062, 'kece', n=6)
            boru(y, [V(L / 2, yc, 0.016), V(L / 2 + 0.006, yc, 0.016)], 0.004, 'demir', n=6)


def hedef(y, x, yy, z, aci=0.0, r=0.04, h=0.07):
    """a round target on two posts (painted rings), its face towards local -x (aci turns it)"""
    with parca(y, (x, yy, z), aci):
        for sy in (-1, 1):
            cubuk(y, V(0.008, sy * r * 0.7, 0), V(0.008, sy * r * 0.7, h + r * 0.6), 0.006, 'ahsap_koyu')
        c = V(0, 0, h)
        n = 14
        C = lambda rr, i, dx: c + V(dx, rr * math.cos(TAU * i / n), rr * math.sin(TAU * i / n))
        for k, (rr, key) in enumerate(((r, 'saz'), (r * 0.75, 'beyaz'), (r * 0.5, 'boya_kirmizi'), (r * 0.25, 'koyu'))):
            y.yuz_yon([C(rr, i, -0.0012 * k) for i in range(n)], key, -X)
        y.yuz_yon([C(r, i, 0.006) for i in range(n)], 'saz_koyu', X)
        for i in range(n):
            j = (i + 1) % n
            yuz_dis(y, [C(r, i, 0), C(r, j, 0), C(r, j, 0.006), C(r, i, 0.006)], 'saz_koyu', c + X * 0.003)


def havan(y, x, yy, z, s=1.0, tokmak=True):
    """a stone mortar (jeolgu) with a wooden pestle"""
    donel(y, (x, yy), [(0.0, z), (0.02 * s, z), (0.022 * s, z + 0.012 * s), (0.02 * s, z + 0.026 * s), (0.014 * s, z + 0.026 * s),
                       (0.012 * s, z + 0.014 * s), (0.0, z + 0.014 * s)], TAS, n=10)
    if tokmak:
        cubuk(y, V(x, yy, z + 0.014 * s), V(x + 0.012 * s, yy, z + 0.06 * s), 0.006 * s, 'ahsap')


def sundurma(y, x0, x1, y0, y1, z, h, cati_h, tur='matbae', sacak=0.035, arka_duvar=False, direk='ahsap', adim=0.11, kivrim=0.3,
             yukari=0.02, taban='toprak', mahya=CATI2):
    """an open-sided work shed: posts on stone bases round x0..x1, y0..y1, tie beams, a ceiling closing the roof's
    inside, the roof (tur), arka_duvar: a plastered back wall (+y side). Returns the top z"""
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a_, b_ = k[i], k[(i + 1) % 4]
        L = (b_ - a_).length
        nb = max(1, int(round(L / adim)))
        e = (b_ - a_).normalized()
        for j in range(nb):
            p = a_.lerp(b_, j / nb)
            kutu_merkez(y, (p.x, p.y), 0.011, 0.011, h, direk, z0=z + 0.004)
            kutu_merkez(y, (p.x, p.y), 0.02, 0.02, 0.005, TAS, z0=z, yuzler='onarkasagsolust')
        kiris(y, a_, b_, z + h * 0.86, h * 0.14, ('ahsap', 'ahsap_koyu'), 0.007)
        if arka_duvar and i == 2:
            duz_duvar(y, a_, b_, z, z + h * 0.86, DUVAR)
            duz_duvar(y, b_ - V(e.y, -e.x) * 0.008, a_ - V(e.y, -e.x) * 0.008, z, z + h * 0.86, DUVAR)
            cerceve_serit(y, a_, b_, z, h * 0.86, [h * 0.35], direk)
    y.yuz_yon([V(p.x, p.y, z + h * 0.86) for p in k], 'ahsap_koyu', -Z)
    return kore_cati(y, x0, x1, y0, y1, z + h, cati_h, sacak, tur, kivrim, yukari, 0, 0, 0.01, ns=max(4, int(max(x1 - x0, y1 - y0) / 0.08)),
                     nr=3, yongmaru=False, alt='ahsap_koyu', mahya=mahya)


def cuval(y, x, yy, z, s=1.0, key='saz'):
    """a rice-straw sack (a squat round bag)"""
    donel(y, (x, yy), [(0.0, z), (0.013 * s, z + 0.002 * s), (0.016 * s, z + 0.01 * s), (0.013 * s, z + 0.022 * s), (0.006 * s, z + 0.027 * s),
                       (0.0, z + 0.028 * s)], key, n=8)


# ---------------------------------------------------------------- ships
def kore_gemi_govde(L, B, D, n=12, bas_egim=0.03, kic_egim=0.02):
    """the hull shape of a Joseon warship (flat bottom, no keel, flaring sides, a square raked bow and stern): returns
    P(u, s, k) -> local point (u -1 stern .. 1 bow, s side -1 / 1, k 0 bottom .. 1 deck edge) and D(u) the deck height"""
    hb = lambda u: B * (1 - 0.14 * u ** 4)
    Du = lambda u: D * (1 + 0.22 * max(0.0, u) ** 4 + 0.12 * max(0.0, -u) ** 4)
    def P(u, s, k):
        xb = u * L / 2
        xt = xb + (bas_egim * u ** 6 if u > 0 else -kic_egim * u ** 6)
        x = xb + (xt - xb) * k
        w = hb(u) * (0.7 + 0.3 * k ** 0.7)
        return V(x, s * w, Du(u) * k)
    return P, Du, hb


def geobukseon(y, c, aci=0.0, s=1.0, z0=0.0, su=None, direk=True, yelken=True, kurek=True, duman=True, tohum=0, sancakli=True):
    """a geobukseon (turtle ship) at c (keel bottom at z0, bow towards angle aci): the flat-bottomed hull with its
    strakes and a ghost face on the bow, the deck house with gun ports, the armoured turtle-back roof (hexagonal plates,
    iron spikes, a cross-shaped walkway), the dragon head breathing smoke at the bow, the rudder; optional masts with
    battened sails and a banner, and ten oars a side (su: the waterline height above the keel, for the oar blades).
    Returns the top z (world)"""
    import random
    rr = random.Random(tohum)
    L, B, D = 0.62, 0.085, 0.075
    P, Du, hb = kore_gemi_govde(L, B, D)
    n = 12
    us = [-1 + 2 * i / n for i in range(n + 1)]
    hw, hr = 0.034, 0.05
    tepe = 0.0
    with parca(y, (c[0], c[1], z0), aci, s):
        # ---- hull: two bands a side, a black wale between, bottom, deck, transoms
        for sd in (-1, 1):
            for i in range(n):
                ua, ub = us[i], us[i + 1]
                for (k0, k1, key) in ((0.0, 0.45, 'ahsap_koyu'), (0.45, 1.0, 'ahsap')):
                    q = [P(ua, sd, k0), P(ub, sd, k0), P(ub, sd, k1), P(ua, sd, k1)]
                    m = sum(q, Vector()) / 4
                    for tri in ((q[0], q[1], q[2]), (q[0], q[2], q[3])): y.yuz_yon(tri, key, V(0, sd, 0))   # (twisted near the raked ends)
            for kk in (0.45, 0.75):   # strakes standing proud
                pts = [P(u, sd, kk) + V(0, sd * 0.002, 0) for u in us[1:-1]]
                boru(y, pts, 0.0028, 'ahsap_koyu', n=4)
        y.yuz_yon([P(u, -1, 0.0) for u in us] + [P(u, 1, 0.0) for u in reversed(us)], 'ahsap_koyu', -Z)
        for i in range(n):
            ua, ub = us[i], us[i + 1]
            y.yuz_yon([P(ua, -1, 1.0), P(ub, -1, 1.0), P(ub, 1, 1.0), P(ua, 1, 1.0)],
                      'ahsap_acik', Z)
        for u, sg in ((1.0, 1), (-1.0, -1)):
            ks = [0.0, 0.45, 1.0]
            for j in range(2):
                q = [P(u, -1, ks[j]), P(u, 1, ks[j]), P(u, 1, ks[j + 1]), P(u, -1, ks[j + 1])]
                y.yuz_yon(q, 'ahsap_koyu' if j == 0 else 'ahsap', V(sg, 0, 0.3 * sg))
        # the ghost face (gwimyeon) on the bow
        bc = (P(1.0, -1, 0.72) + P(1.0, 1, 0.72)) / 2
        nb = (V(1, 0, 0) + V(0, 0, -0.35)).normalized()
        nb = V(1, 0, 0.0)
        e2, up2 = V(0, 1, 0), (P(1.0, 1, 1.0) - P(1.0, 1, 0.45)).normalized()
        nbo = e2.cross(up2).normalized()
        if nbo.x < 0: nbo = -nbo
        F = lambda dy, dz, d=0.0015: bc + e2 * dy + up2 * dz + nbo * d
        y.yuz_yon([F(0.03 * math.cos(TAU * i / 12), 0.022 * math.sin(TAU * i / 12)) for i in range(12)], 'boya_kirmizi', nbo)
        for sy in (-1, 1):
            y.yuz_yon([F(sy * 0.011 + 0.006 * math.cos(TAU * i / 8), 0.006 + 0.005 * math.sin(TAU * i / 8), 0.0025) for i in range(8)], 'beyaz', nbo)
            y.yuz_yon([F(sy * 0.011 + 0.0025 * math.cos(TAU * i / 6), 0.006 + 0.0025 * math.sin(TAU * i / 6), 0.0032) for i in range(6)], 'koyu', nbo)
        y.yuz_yon([F(-0.016, -0.012, 0.0025), F(0.016, -0.012, 0.0025), F(0.016, -0.005, 0.0025), F(-0.016, -0.005, 0.0025)], 'beyaz', nbo)
        for k in range(5):
            dy = -0.012 + k * 0.006
            y.yuz_yon([F(dy - 0.0012, -0.0115, 0.003), F(dy + 0.0012, -0.0115, 0.003), F(dy + 0.0012, -0.0055, 0.003), F(dy - 0.0012, -0.0055, 0.003)], 'koyu', nbo)
        # ---- the deck house: walls with gun ports
        u0, u1 = -0.8, 0.8
        x0, x1 = u0 * L / 2, u1 * L / 2
        wh = B * 0.9
        zd = Du(0)
        zw = zd + hw
        for sd in (-1, 1):
            a, b = (V(x0, sd * wh), V(x1, sd * wh)) if sd < 0 else (V(x1, sd * wh), V(x0, sd * wh))
            duz_duvar(y, a, b, zd - 0.004, zw, 'ahsap_koyu')
            for k in range(11):
                xx = x0 + (x1 - x0) * (k + 0.5) / 11
                o = V(xx, sd * (wh + 0.0012))
                for (w_, h_, zc, key) in ((0.013, 0.013, zd + hw * 0.5, 'boya_kirmizi'), (0.008, 0.008, zd + hw * 0.5, 'koyu')):
                    d = 0.0008 if key == 'koyu' else 0.0
                    y.yuz_yon([V(xx - w_ / 2, o.y + sd * d, zc - h_ / 2), V(xx + w_ / 2, o.y + sd * d, zc - h_ / 2), V(xx + w_ / 2, o.y + sd * d, zc + h_ / 2),
                               V(xx - w_ / 2, o.y + sd * d, zc + h_ / 2)], key, V(0, sd, 0))
        # ---- the turtle-back roof
        wr = wh + 0.01
        nt = 8
        ox = 0.012
        Rf = lambda t, th: V(x0 - ox + (x1 - x0 + 2 * ox) * t, wr * math.cos(th), zw + hr * (0.88 + 0.12 * math.sin(math.pi * t)) * math.sin(th))
        nu = 12
        for i in range(nu):
            for j in range(nt):
                ta, tb = i / nu, (i + 1) / nu
                ha, hb_ = math.pi * j / nt, math.pi * (j + 1) / nt
                q = [Rf(ta, ha), Rf(tb, ha), Rf(tb, hb_), Rf(ta, hb_)]
                yol = j in (3, 4) or i in (nu // 2 - 1, nu // 2)
                m = sum(q, Vector()) / 4
                nrm = (q[1] - q[0]).cross(q[3] - q[0]).normalized()
                if nrm.dot(m - V(m.x, 0, zw)) < 0: nrm = -nrm
                yuz_dis(y, q, 'ahsap_acik' if yol else 'ahsap_koyu', V(m.x, 0, zw - 0.02))
                if not yol:
                    # a raised hexagonal plate and an iron spike in its middle
                    ex_ = (q[1] - q[0]).normalized(); ey_ = nrm.cross(ex_).normalized()
                    rx, ry = (q[1] - q[0]).length * 0.42, (q[3] - q[0]).length * 0.42
                    hx = [m + nrm * 0.0016 + ex_ * (rx * math.cos(TAU * k / 6)) + ey_ * (ry * math.sin(TAU * k / 6)) for k in range(6)]
                    y.yuz_yon(hx, 'lake_koyu', nrm)
                    for k in range(6):
                        y.yuz_yon([hx[k], hx[(k + 1) % 6], hx[(k + 1) % 6] - nrm * 0.0016, hx[k] - nrm * 0.0016], 'lake_koyu',
                                  (hx[k] + hx[(k + 1) % 6]) / 2 - m)
                    # (the spikes: iron, a stud of a collar and a sharp four-sided point standing well proud, read from afar)
                    base = [m + nrm * 0.0016 + ex_ * (0.0036 * math.cos(TAU * k / 4 + 0.785)) + ey_ * (0.0036 * math.sin(TAU * k / 4 + 0.785)) for k in range(4)]
                    tip = m + nrm * 0.019
                    for k in range(4):
                        yuz_dis(y, [base[k], base[(k + 1) % 4], tip], 'demir', m + nrm * 0.005)
        # the roof's eave undersides and its end caps
        for sd, th in ((1, 0.0), (-1, math.pi)):
            p0, p1 = Rf(0, th), Rf(1, th)
            y.yuz_yon([p0, p1, V(p1.x, sd * wh, zw), V(p0.x, sd * wh, zw)], 'ahsap_koyu', -Z)
        for t, sg in ((0.0, -1), (1.0, 1)):
            sec = [Rf(t, math.pi * j / nt) for j in range(nt + 1)]
            y.yuz_yon(sec, 'ahsap_koyu', V(sg, 0, 0))
            xe = sec[0].x
            xw = x0 if sg < 0 else x1
            y.yuz_yon([V(xe, -wr, zw), V(xe, wr, zw), V(xw, wr, zw), V(xw, -wr, zw)], 'ahsap_koyu', -Z)
            # the house's end wall under the roof (a door at the stern)
            y.yuz_yon([V(xw, -wh, zd - 0.004), V(xw, wh, zd - 0.004), V(xw, wh, zw), V(xw, -wh, zw)], 'ahsap_koyu', V(sg, 0, 0))
        y.yuz_yon([V(x0 - 0.0012, -0.014, zd), V(x0 - 0.0012, 0.014, zd), V(x0 - 0.0012, 0.014, zw - 0.004), V(x0 - 0.0012, -0.014, zw - 0.004)], 'koyu', -X)
        ztop = zw + hr
        tepe = ztop
        # ---- the dragon head at the bow (the ship's signature: drawn large, a little bigger than the hull would give)
        nk0 = V(x1 + 0.004, 0, zw + hr * 0.25)
        with parca(y, (nk0.x, nk0.y, nk0.z), 0.0, 1.3):
            nk = V(0, 0, 0)
            hc = V(0.07, 0, hr * 0.72)
            # the neck rising from the bow, scaled (green-edged scales along its back)
            boru(y, [nk, nk + V(0.028, 0, 0.012), hc - V(0.014, 0, 0.004)], 0.016, 'lake', n=8, r_son=0.012)
            f_ = V(1, 0, 0.18).normalized()
            upd = f_.cross(Y).normalized() * -1
            if upd.z < 0: upd = -upd
            # skull, brow ridge, upper snout with the nose knob, the gaping lower jaw, the dark mouth inside
            kutu3(y, hc, f_, Y, upd, 0.03, 0.028, 0.026, 'lake')
            kutu3(y, hc + upd * 0.011 + f_ * 0.006, f_, Y, upd, 0.02, 0.032, 0.007, 'lake_koyu')
            kutu3(y, hc + f_ * 0.025 + upd * 0.003, f_ + upd * 0.18, Y, upd, 0.026, 0.022, 0.01, 'lake')
            kure(y, tuple(hc + f_ * 0.038 + upd * 0.009), 0.0065, 'lake', n=8, kat=4)
            kutu3(y, hc + f_ * 0.022 - upd * 0.012, f_ - upd * 0.45, Y, upd, 0.024, 0.02, 0.007, 'lake')
            kutu3(y, hc + f_ * 0.02 - upd * 0.005, f_, Y, upd, 0.02, 0.016, 0.006, 'koyu')
            for k in range(4):   # the fangs, upper and lower
                for sy in (-1, 1):
                    p = hc + f_ * (0.014 + k * 0.007) + Y * (sy * 0.0085)
                    cubuk(y, p - upd * 0.001, p - upd * 0.007, 0.0022, 'beyaz')
                    cubuk(y, p - upd * 0.012, p - upd * 0.006, 0.0018, 'beyaz')
            for sy in (-1, 1):
                # eyes: white globes with dark pupils under the brow
                e_ = hc + f_ * 0.009 + upd * 0.006 + Y * (sy * 0.0135)
                kure(y, tuple(e_), 0.0055, 'beyaz', n=8, kat=4)
                kure(y, tuple(e_ + Y * (sy * 0.0035) + f_ * 0.002), 0.0028, 'koyu', n=6, kat=3)
                # nostrils, gilt antlers sweeping back, whiskers
                kure(y, tuple(hc + f_ * 0.042 + upd * 0.011 + Y * (sy * 0.005)), 0.0022, 'koyu', n=5, kat=3)
                boru(y, [hc - f_ * 0.006 + upd * 0.012 + Y * (sy * 0.007), hc - f_ * 0.022 + upd * 0.03 + Y * (sy * 0.013),
                         hc - f_ * 0.042 + upd * 0.036 + Y * (sy * 0.016)], 0.0032, 'altin', n=5, r_son=0.0015)
                cubuk(y, hc - f_ * 0.022 + upd * 0.03 + Y * (sy * 0.013), hc - f_ * 0.02 + upd * 0.042 + Y * (sy * 0.02), 0.002, 'altin')
                boru(y, [hc + f_ * 0.036 + Y * (sy * 0.009), hc + f_ * 0.046 + Y * (sy * 0.022) - upd * 0.004, hc + f_ * 0.04 + Y * (sy * 0.032) - upd * 0.014],
                     0.0014, 'beyaz', n=3)
                # gilt ears / fins at the back of the head
                cubuk(y, hc - f_ * 0.012 + Y * (sy * 0.014), hc - f_ * 0.024 + Y * (sy * 0.024) + upd * 0.006, 0.004, 'boya_yesil', 0.002)
            for k in range(5):   # the green mane down the neck
                p = nk + (hc - nk) * (0.1 + k * 0.2) + upd * 0.015
                cubuk(y, p, p - f_ * 0.012 + upd * 0.013, 0.0045, 'boya_yesil')
            if duman:   # sulphur smoke pouring from the jaws (soft puffs, swelling as they drift)
                for k in range(6):
                    kure(y, tuple(hc + f_ * (0.05 + k * 0.016) + upd * (-0.002 + k * 0.005) + Y * rr.uniform(-0.004, 0.004)), 0.007 + k * 0.0032,
                         'duman' if k < 2 else 'buhar', n=8, kat=4)
        # ---- rudder and tiller at the stern
        rp = P(-1.0, 1, 1.0); rp = V(rp.x - 0.012, 0, rp.z)
        levha(y, [rp + V(0, 0, 0.01), rp + V(-0.004, 0, -D * 1.05), rp + V(-0.05, 0, -D * 1.05), rp + V(-0.03, 0, -D * 0.3)], 'ahsap_koyu', Y, 0.004)
        cubuk(y, rp + V(0, 0, 0.01), rp + V(0.06, 0, 0.022), 0.004, 'ahsap_koyu')
        # ---- masts, sails and the banner
        if direk:
            for (xm, hm, sw, sh) in ((0.0, 0.4, 0.2, 0.22), (0.13, 0.32, 0.15, 0.17)):
                zb = ztop - 0.01
                boru(y, [V(xm, 0, zd), V(xm, 0, zb + hm)], 0.0055, 'ahsap', n=6, r_son=0.0035)
                if yelken:
                    zs0, zs1 = zb + hm * 0.25, zb + hm * 0.25 + sh
                    bel = 0.018
                    # (two planar panels, the lower one leaning forward: a little belly)
                    zm = (zs0 + zs1) / 2
                    levha(y, [V(xm + 0.007 + bel * 0.5, -sw / 2, zs0), V(xm + 0.007 + bel * 0.5, sw / 2, zs0), V(xm + 0.007, sw * 0.48, zm),
                              V(xm + 0.007, -sw * 0.48, zm)], 'saz', X, 0.003)
                    levha(y, [V(xm + 0.007, -sw * 0.48, zm), V(xm + 0.007, sw * 0.48, zm), V(xm + 0.007, sw / 2 * 0.92, zs1),
                              V(xm + 0.007, -sw / 2 * 0.92, zs1)], 'saz', X, 0.003)
                    mid = V(xm + 0.007 + bel, 0, (zs0 + zs1) / 2)
                    for k in range(7):   # the bamboo battens
                        zz = zs0 + (zs1 - zs0) * k / 6
                        cubuk(y, V(xm + 0.0095, -sw / 2 * (1 - 0.08 * k / 6), zz), V(xm + 0.0095, sw / 2 * (1 - 0.08 * k / 6), zz), 0.0022, 'ahsap_koyu')
                    cubuk(y, V(xm, -sw / 2 * 0.92, zs1), V(xm, sw / 2 * 0.92, zs1), 0.004, 'ahsap')
                tepe = max(tepe, zb + hm)
            if sancakli:
                sancak(y, 0.0, 0.0, ztop - 0.01 + 0.4 - 0.03, boy=0.07, en=0.07, yuk=0.04, aci=math.pi * 0.85, direk_key='ahsap', kuyruk=True)
                tepe += 0.04
        # ---- oars
        if kurek:
            sz = su if su is not None else D * 0.3
            for sd in (-1, 1):
                for k in range(10):
                    u = -0.62 + k * 0.13
                    p0 = P(u, sd, 0.62) + V(0, sd * 0.002, 0)
                    p1 = V(p0.x - 0.035, sd * (hb(u) + 0.12), sz - 0.004)
                    cubuk(y, p0, p1, 0.0035, 'ahsap_acik')
                    d_ = (p1 - p0).normalized()
                    kutu3(y, p1 - d_ * 0.012, d_, V(0, 0, 1).cross(d_).normalized() if abs(d_.z) < 0.99 else X, V(0, 0, 1), 0.028, 0.012, 0.002, 'ahsap_acik')
    return z0 + tepe * s


def panokseon(y, c, aci=0.0, s=1.0, z0=0.0, su=None, yelken=True, kurek=True, sancakli=True, tohum=0):
    """a panokseon (the Joseon two-decked battleship): the flat-bottomed hull, a raised bulwark storey with gun ports
    and the open upper deck with its railing, the command pavilion (jangdae) under a small hipped roof, two masts with
    battened sails, oars. Returns the top z (world)"""
    L, B, D = 0.66, 0.1, 0.07
    P, Du, hb = kore_gemi_govde(L, B, D, bas_egim=0.035)
    n = 12
    us = [-1 + 2 * i / n for i in range(n + 1)]
    tepe = 0.0
    with parca(y, (c[0], c[1], z0), aci, s):
        for sd in (-1, 1):
            for i in range(n):
                ua, ub = us[i], us[i + 1]
                for (k0, k1, key) in ((0.0, 0.45, 'ahsap_koyu'), (0.45, 1.0, 'ahsap')):
                    q = [P(ua, sd, k0), P(ub, sd, k0), P(ub, sd, k1), P(ua, sd, k1)]
                    m = sum(q, Vector()) / 4
                    for tri in ((q[0], q[1], q[2]), (q[0], q[2], q[3])): y.yuz_yon(tri, key, V(0, sd, 0))   # (twisted near the raked ends)
            for kk in (0.45, 0.8):
                boru(y, [P(u, sd, kk) + V(0, sd * 0.002, 0) for u in us[1:-1]], 0.0028, 'ahsap_koyu', n=4)
        y.yuz_yon([P(u, -1, 0.0) for u in us] + [P(u, 1, 0.0) for u in reversed(us)], 'ahsap_koyu', -Z)
        for i in range(n):
            ua, ub = us[i], us[i + 1]
            y.yuz_yon([P(ua, -1, 1.0), P(ub, -1, 1.0), P(ub, 1, 1.0), P(ua, 1, 1.0)],
                      'ahsap_acik', Z)
        for u, sg in ((1.0, 1), (-1.0, -1)):
            ks = [0.0, 0.45, 1.0]
            for j in range(2):
                q = [P(u, -1, ks[j]), P(u, 1, ks[j]), P(u, 1, ks[j + 1]), P(u, -1, ks[j + 1])]
                y.yuz_yon(q, 'ahsap_koyu' if j == 0 else 'ahsap', V(sg, 0, 0.3 * sg))
        # the bulwark storey: a box on the deck, gun ports along it, the upper deck on top
        x0, x1 = -0.84 * L / 2, 0.84 * L / 2
        wh = B * 0.96
        zd = Du(0)
        hw = 0.036
        zu = zd + hw
        kutu(y, V(x0, -wh, zd - 0.004), X, x1 - x0, 2 * wh, hw + 0.004, 'ahsap_koyu', 'onarkasagsol')
        y.yuz_yon(dikdortgen(x0 - 0.006, x1 + 0.006, -wh - 0.006, wh + 0.006, zu), 'ahsap_acik', Z)
        for sd in (-1, 1):
            y.yuz_yon([V(x0 - 0.006, sd * (wh + 0.006), zu), V(x1 + 0.006, sd * (wh + 0.006), zu), V(x1 + 0.006, sd * (wh + 0.006), zu - 0.006),
                       V(x0 - 0.006, sd * (wh + 0.006), zu - 0.006)], 'ahsap', V(0, sd, 0))
            y.yuz_yon([V(x0 - 0.006, sd * (wh + 0.006), zu - 0.006), V(x1 + 0.006, sd * (wh + 0.006), zu - 0.006), V(x1 + 0.006, sd * wh, zu - 0.006),
                       V(x0 - 0.006, sd * wh, zu - 0.006)], 'ahsap_koyu', -Z)
            for k in range(12):
                xx = x0 + (x1 - x0) * (k + 0.5) / 12
                for (w_, d, key) in ((0.012, 0.0008, 'boya_kirmizi'), (0.007, 0.0016, 'koyu')):
                    yy = sd * (wh + d)
                    zc = zd + hw * 0.45
                    y.yuz_yon([V(xx - w_ / 2, yy, zc - w_ / 2), V(xx + w_ / 2, yy, zc - w_ / 2), V(xx + w_ / 2, yy, zc + w_ / 2), V(xx - w_ / 2, yy, zc + w_ / 2)],
                              key, V(0, sd, 0))
        for xs_, sg in ((x0 - 0.006, -1), (x1 + 0.006, 1)):
            y.yuz_yon([V(xs_, -wh - 0.006, zu - 0.006), V(xs_, wh + 0.006, zu - 0.006), V(xs_, wh + 0.006, zu), V(xs_, -wh - 0.006, zu)], 'ahsap', V(sg, 0, 0))
        kore_korkuluk(y, dikdortgen(x0, x1, -wh + 0.002, wh - 0.002), zu, 0.02, adim=0.045, key='lake_koyu', ust='lake_koyu')
        # the command pavilion over the stern half
        jc = V(-0.1, 0)
        for sx in (-1, 1):
            for sy in (-1, 1):
                kutu_merkez(y, (jc.x + sx * 0.04, sy * 0.04), 0.008, 0.008, 0.06, 'lake', z0=zu)
        kutu_merkez(y, (jc.x, 0), 0.1, 0.1, 0.012, 'boya_yesil', z0=zu + 0.06, yuzler='onarkasagsol')
        y.yuz_yon(dikdortgen(jc.x - 0.05, jc.x + 0.05, -0.05, 0.05, zu + 0.06), 'boya_yesil', -Z)
        tp = kore_cati(y, jc.x - 0.05, jc.x + 0.05, -0.05, 0.05, zu + 0.072, 0.06, 0.03, 'ujingak', 0.35, 0.02, 0, 0, 0.008, ns=4, nr=3,
                       yongmaru=False)
        tepe = tp
        for (xm, hm, sw, sh) in ((0.08, 0.42, 0.22, 0.23), (0.2, 0.33, 0.16, 0.18)):
            boru(y, [V(xm, 0, zd), V(xm, 0, zu + hm)], 0.0055, 'ahsap', n=6, r_son=0.0035)
            if yelken:
                zs0, zs1 = zu + hm * 0.28, zu + hm * 0.28 + sh
                zm = (zs0 + zs1) / 2
                levha(y, [V(xm + 0.016, -sw / 2, zs0), V(xm + 0.016, sw / 2, zs0), V(xm + 0.007, sw * 0.48, zm), V(xm + 0.007, -sw * 0.48, zm)], 'saz', X, 0.003)
                levha(y, [V(xm + 0.007, -sw * 0.48, zm), V(xm + 0.007, sw * 0.48, zm), V(xm + 0.007, sw / 2 * 0.92, zs1), V(xm + 0.007, -sw / 2 * 0.92, zs1)],
                      'saz', X, 0.003)
                for k in range(7):
                    zz = zs0 + (zs1 - zs0) * k / 6
                    dx = (0.016 if k < 3 else 0.007) + 0.0028 - (0.009 * k / 3 if k < 3 else 0)
                    cubuk(y, V(xm + dx, -sw / 2 * (1 - 0.08 * k / 6), zz), V(xm + dx, sw / 2 * (1 - 0.08 * k / 6), zz), 0.0022, 'ahsap_koyu')
            tepe = max(tepe, zu + hm)
        if sancakli:
            sancak(y, 0.08, 0.0, zu + 0.42 - 0.03, boy=0.07, en=0.07, yuk=0.04, aci=math.pi * 0.85, kuyruk=True)
            tepe += 0.04
        rp = P(-1.0, 1, 1.0); rp = V(rp.x - 0.012, 0, rp.z)
        levha(y, [rp + V(0, 0, 0.01), rp + V(-0.004, 0, -D * 1.05), rp + V(-0.05, 0, -D * 1.05), rp + V(-0.03, 0, -D * 0.3)], 'ahsap_koyu', Y, 0.004)
        if kurek:
            sz = su if su is not None else D * 0.3
            for sd in (-1, 1):
                for k in range(9):
                    u = -0.6 + k * 0.15
                    p0 = P(u, sd, 0.62) + V(0, sd * 0.002, 0)
                    p1 = V(p0.x - 0.035, sd * (hb(u) + 0.12), sz - 0.004)
                    cubuk(y, p0, p1, 0.0035, 'ahsap_acik')
                    d_ = (p1 - p0).normalized()
                    kutu3(y, p1 - d_ * 0.012, d_, V(0, 0, 1).cross(d_).normalized(), V(0, 0, 1), 0.028, 0.012, 0.002, 'ahsap_acik')
    return z0 + tepe * s


def hongsalmun(y, x, yy, z, en=0.16, h=0.16, aci=0.0):
    """a hongsalmun: the red arrow gate before a shrine: two tall red posts, two beams, a row of red spikes between
    them and the taegeuk with its trident in the middle"""
    with parca(y, (x, yy, z), aci):
        for sx in (-1, 1):
            kutu_merkez(y, (sx * en / 2, 0), 0.026, 0.026, 0.01, TAS, yuzler='onarkasagsolust')
            y.prizma((sx * en / 2, 0), 0.0065, 0.0, h, 'lake', n=8)
            kure(y, (sx * en / 2, 0, h + 0.005), 0.007, 'koyu', n=6, kat=3)
        for zz in (h * 0.72, h * 0.9):
            cubuk(y, V(-en / 2 - 0.006, 0, zz), V(en / 2 + 0.006, 0, zz), 0.008, 'lake', 0.006)
        for k in range(1, 12):
            xx = -en / 2 + en * k / 12
            cubuk(y, V(xx, 0, h * 0.72), V(xx, 0, h * 0.9 + 0.022), 0.0028, 'lake')
        c = V(0, 0, h * 0.81)
        for sg in (-1, 1):
            y.yuz_yon([c + V(0.013 * math.cos(TAU * i / 12), sg * 0.0045, 0.013 * math.sin(TAU * i / 12)) for i in range(12)], 'boya_kirmizi', V(0, sg, 0))
            y.yuz_yon([c + V(0.013 * math.cos(TAU * i / 12), sg * 0.005, 0.013 * math.sin(TAU * i / 12)) for i in range(6, 13)], 'kobalt', V(0, sg, 0))
        for dx in (-0.008, 0.0, 0.008):
            cubuk(y, V(dx, 0, h * 0.9), V(dx * 1.4, 0, h * 0.9 + 0.035 + (0.008 if dx == 0 else 0)), 0.003, 'lake')


def bigak(y, x, yy, z, w=0.1, h=0.07, aci=0.0):
    """a stele pavilion (bigak): a tortoise-based stone tablet under a small open pavilion with a pyramid roof"""
    with parca(y, (x, yy, 0), aci):
        kutu_merkez(y, (0, 0), w + 0.03, w + 0.03, 0.014, TAS, z0=z)
        zb = z + 0.014
        for sx in (-1, 1):
            for sy in (-1, 1):
                y.prizma((sx * w / 2, sy * w / 2), 0.005, zb, zb + h, DIREK, n=6)
        k = dikdortgen(-w / 2, w / 2, -w / 2, w / 2)
        for i in range(4):
            kiris(y, k[i], k[(i + 1) % 4], zb + h * 0.82, h * 0.18, BOYA, 0.006)
        y.yuz_yon([V(p.x, p.y, zb + h * 0.82) for p in k], ALT, -Z)
        donel(y, (0, 0), [(0.0, zb), (0.024, zb), (0.022, zb + 0.008), (0.012, zb + 0.014), (0.0, zb + 0.015)], 'granit_koyu', n=10)
        kure(y, (0.026, 0, zb + 0.006), 0.006, 'granit_koyu', n=6, kat=3)
        kutu3(y, V(0, 0, zb + 0.014 + 0.025), X, Y, Z, 0.006, 0.026, 0.05, 'granit_koyu')
        kutu3(y, V(0, 0, zb + 0.064 + 0.004), X, Y, Z, 0.008, 0.03, 0.008, 'granit_koyu')
        kore_cati(y, -w / 2, w / 2, -w / 2, w / 2, zb + h, 0.07, 0.035, 'ujingak', 0.35, 0.03, 0, 0, 0.008, ns=4, nr=3, yongmaru=False)
