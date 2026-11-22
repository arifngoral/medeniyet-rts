# Shared helpers for the Chinese landmarks (lm_seddkalesi, lm_buyukkanal, lm_pirincteras, lm_topraksavasci): a
# multi-storey timber tower (gate tower, pavilion) with the storeys standing on the roof below, a hall on a stone
# plinth, pines, bamboo clumps and small human figures with conical hats.
import math
from parcalar import *


def katli_kule(y, c, w, d, z, katlar, key_duvar='lake', key_direk='lake', key_cati='kiremit_koyu', mahya='kiremit_koyu2',
               kivrim=0.5, yukari=0.03, kucul=0.8, sus=None, son_irimoya=True, balkon=True, dilim=None):
    """storeys of an East Asian tower one above the other: katlar = [(h, cati_h, sacak), ...] from the bottom; each storey
    kucul x the one below, standing on its roof; the top one hip-and-gable (son_irimoya). Returns the ridge z"""
    tepe = z
    for i, (h, ch, sk) in enumerate(katlar):
        son = i == len(katlar) - 1
        tepe, _ = pagoda_kati(y, c, w, z, h, ch, sk, key_duvar, key_direk, key_cati, mahya, kivrim, yukari,
                              korkuluk=balkon and i > 0, kafesli=True, d=d, alt_key='lake_koyu', dilim=dilim,
                              irimoya=son and son_irimoya, sus=sus if son else None, balkon=0.02 if (balkon and i > 0) else 0)
        if not son:
            w2, d2 = w * kucul, d * kucul
            # (the next storey's foot: the roof's height where its walls stand, a hair into it)
            a, b = w / 2 + sk, d / 2 + sk
            m = min(a, b)
            t = max(0.0, min(1.0, min(a - w2 / 2, b - d2 / 2) / m))
            z = z + h + 0.018 + ch * ((1 - kivrim) * t + kivrim * t * t) - 0.004
            w, d = w2, d2
    return tepe


def cam(y, x, yy, z, boy=0.14, key='yesil_koyu', govde='ahsap'):
    """a pine: a short trunk and three stacked cones"""
    y.prizma((x, yy), boy * 0.035, z - 0.01, z + boy * 0.3, govde, n=5)
    for k, (r, z0, hh) in enumerate(((0.3, 0.18, 0.4), (0.23, 0.42, 0.34), (0.15, 0.63, 0.37))):
        y.koni((x, yy), boy * r, z + boy * z0, boy * hh, key, n=8)
        # (the cone's underside, seen from below its rim on a slope)
        y.yuz_yon([V(x + boy * r * math.cos(TAU * i / 8), yy + boy * r * math.sin(TAU * i / 8), z + boy * z0) for i in range(8)], key, -Z)


def bambu(y, x, yy, z, boy=0.12, n=7, tohum=0, key='boya_yesil', yaprak='zeytin', serpinti=False):
    """a bamboo clump: thin leaning culms with leaf tufts (serpinti: fans of drooping lance leaves at the top and a node
    instead of the round tufts)"""
    import random
    r = random.Random(tohum)
    for i in range(n):
        a = r.uniform(0, TAU); d = r.uniform(0, 0.02)
        p0 = V(x + math.cos(a) * d, yy + math.sin(a) * d, z - 0.005)
        lean = V(math.cos(a) * 0.025, math.sin(a) * 0.025, 0)
        hh = boy * r.uniform(0.75, 1.1)
        p1 = p0 + lean * 0.4 + Z * hh * 0.6
        p2 = p0 + lean + Z * hh
        boru(y, [p0, p1, p2], 0.0022, key, n=4, r_son=0.0012)
        if serpinti:
            for (q, m, L) in ((p2, 6, 0.024), (p1 + lean * 0.3 + Z * 0.01, 4, 0.018)):
                a0 = r.uniform(0, TAU)
                for l in range(m):
                    a_ = a0 + TAU * l / m + r.uniform(-0.3, 0.3)
                    d_ = V(math.cos(a_), math.sin(a_))
                    dr = r.uniform(0.5, 1.0)
                    boru(y, [q, q + d_ * (L * 0.5) + Z * (L * 0.1), q + d_ * L - Z * (L * 0.35 * dr)], 0.0032, yaprak if l % 2 else key,
                         n=3, r_son=0.0006)
            continue
        kure(y, (p2.x, p2.y, p2.z - 0.008), 0.014, yaprak, n=6, kat=3)
        kure(y, (p1.x + lean.x * 0.3, p1.y + lean.y * 0.3, p1.z + 0.01), 0.01, yaprak, n=6, kat=3)


def insan(y, x, yy, z, aci=0.0, govde='kumas', sapka='saz', boy=0.05, egik=0.0):
    """a small figure: legs, a tunic, a head and a wide conical straw hat (egik: bent forward, as when planting)"""
    with parca(y, (x, yy, z), aci):
        s = boy / 0.05
        for sx in (-1, 1):
            cubuk(y, V(0, sx * 0.004 * s, 0), V(0, sx * 0.004 * s, 0.018 * s), 0.004 * s, 'ahsap_koyu')
        govde_ust = V(egik * 0.012 * s, 0, 0.04 * s - egik * 0.008 * s)
        donel(y, (0, 0), [(0.0085 * s, 0.016 * s), (0.0075 * s, 0.026 * s), (0.0055 * s, 0.036 * s), (0, 0.038 * s)], govde, n=8)
        if egik:
            boru(y, [V(0, 0, 0.032 * s), govde_ust], 0.0055 * s, govde, n=6)
        bas = govde_ust + V(0.002 * s * egik, 0, 0.004 * s)
        kure(y, (bas.x, bas.y, bas.z), 0.0048 * s, 'siva_krem', n=8, kat=4)
        y.koni((bas.x, bas.y), 0.012 * s, bas.z + 0.002 * s, 0.008 * s, sapka, n=10)
        y.yuz_yon([V(bas.x + 0.012 * s * math.cos(TAU * i / 10), bas.y + 0.012 * s * math.sin(TAU * i / 10), bas.z + 0.002 * s) for i in range(10)], sapka, -Z)
        for sy in (-1, 1):   # arms
            cubuk(y, V(0, sy * 0.008 * s, 0.033 * s), V(0.006 * s + egik * 0.01 * s, sy * 0.009 * s, 0.02 * s - egik * 0.006 * s), 0.003 * s, govde)


def salon(y, x0, x1, y0, y1, z, h, cati_h, sacak=0.04, duvar='siva_kirmizi', direk='lake', cati='kiremit_koyu', mahya='kiremit_koyu2',
          tur='irimoya', kivrim=0.4, yukari=0.025, kaide=0.02, kaide_key='granit', sus=None, kapi_yon=0, basamak=True):
    """a timber hall on a stone plinth: red walls between lacquered posts, lattice windows, a door, brackets, roof tur
    'irimoya' (xieshan), 'kirma' (hipped), 'besik' (gable). kapi_yon: side of the door (0 front -y, 1 +x, 2 back, 3 -x).
    Returns the ridge z"""
    kx0, kx1, ky0, ky1 = x0 - 0.02, x1 + 0.02, y0 - 0.02, y1 + 0.02
    if kaide:
        kutu(y, V(kx0, ky0, z), X, kx1 - kx0, ky1 - ky0, kaide, kaide_key)
        silme(y, dikdortgen(kx0, kx1, ky0, ky1), z + kaide - 0.004, 0.004, 0.003, 'tas_acik', 'duz')
        if basamak:
            cx = (x0 + x1) / 2
            for k in range(2):
                hh = kaide * (2 - k) / 3
                kutu(y, V(cx - 0.035, ky0 - 0.012 * (k + 1), z), X, 0.07, 0.012 * (k + 1) + 0.001, hh, kaide_key, 'onsagsolust')
    zb = z + kaide
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        L = (b - a).length
        nb = max(1, int(round(L / 0.07)))
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for j in range(nb):
            p, q = a.lerp(b, j / nb), a.lerp(b, (j + 1) / nb)
            if i == kapi_yon and j == nb // 2:
                dikdortgen_acik(y, p, q, zb, h, 0.2, 0.8, 0.0, h * 0.78, (duvar, 'lake_koyu', 'lake_koyu', 'lake_koyu'), derin=0.008)
                kafes(y, p, q, zb, 0.2, 0.8, 0.0, h * 0.78, 'lake', 4, 3, 0.0025, 0.004)
            elif nb > 1 or i % 2 == 1:
                dikdortgen_acik(y, p, q, zb, h, 0.2, 0.8, h * 0.3, h * 0.78, (duvar, 'lake_koyu', 'lake_koyu', 'koyu'), derin=0.008)
                kafes(y, p, q, zb, 0.2, 0.8, h * 0.3, h * 0.78, 'lake', 3, 3, 0.0022, 0.004)
            else:
                duz_duvar(y, p, q, zb, zb + h, duvar)
        for j in range(nb + 1):
            p = a.lerp(b, j / nb) + nn * 0.004
            kutu_merkez(y, (p.x, p.y), 0.012, 0.012, h, direk, z0=zb)
        kutu(y, a + nn * 0.007 + Z * (zb + h * 0.84) - e * 0.006, e, L + 0.012, 0.012, h * 0.16, direk, 'onust')
    zc = zb + h
    y.yuz_yon([V(p.x, p.y, zc) for p in k], 'ahsap_koyu', Z)
    if tur == 'irimoya':
        return cati_irimoya(y, x0, x1, y0, y1, zc, cati_h, sacak, cati, mahya, kivrim, yukari, 'lake_koyu', 'siva_kirmizi', sus=sus)
    if tur == 'besik':
        return cati_besik(y, x0, x1, y0, y1, zc, cati_h, sacak, cati, mahya, 0.01, kivrim, 'lake_koyu', duvar, sus=sus)
    return cati_kirma(y, x0, x1, y0, y1, zc, cati_h, sacak, cati, mahya, 0.01, kivrim, yukari, 'lake_koyu', ns=8, nr=5)


def yogun_pagoda(y, c, r, z, h1, n_kat=13, kat_h=0.03, sacak=None, govde='tas_acik', cati='kiremit_koyu', kaide_key='mermer',
                 kapi_key='lake_koyu', konsol='lake_koyu', uc='bronz', daralma=0.55, kaideli=True):
    """an octagonal dense-eave brick pagoda (Randeng / Tianning type): a sumeru base, a tall first storey (radius r, h1
    high) with doors on four faces and blind windows on the other four, n_kat close-set eaves each over a short drum, the
    drums narrowing to daralma x r at the top, a finial. Returns the tip z"""
    sk = sacak or r * 0.32
    kat = math.pi / 8
    if kaideli:
        pr = [(r * 1.5, z), (r * 1.5, z + 0.03), (r * 1.42, z + 0.034), (r * 1.34, z + 0.04), (r * 1.34, z + 0.06), (r * 1.42, z + 0.066),
              (r * 1.42, z + 0.074), (r * 1.25, z + 0.078)]
        donel(y, c, pr, kaide_key, n=8, kat=kat)
        y.yuz_yon([V(p.x, p.y, z + 0.078) for p in cokgen(c, r * 1.25, 8, kat)], kaide_key, Z)
        z += 0.078
        # a lotus seat under the body
        donel(y, c, [(r * 1.12, z), (r * 1.18, z + 0.008), (r * 1.08, z + 0.02), (r * 1.0, z + 0.022)], 'tas_acik', n=8, kat=kat)
        z += 0.022
    # the first storey: arched doors / blind windows on its eight faces, corner pilasters
    k8 = cokgen(c, r, 8, kat)
    for i in range(8):
        a, b = k8[i], k8[(i + 1) % 8]
        if i % 2 == 0:
            y.kemerli(a, b, z, h1, (govde, 'tas_koyu', 'tas_acik', kapi_key), v0=0.0, en=0.5, ust=h1 * 0.22, derin=0.012, k_say=8,
                      cerceve=(0.005, 'tas_acik'))
        else:
            dikdortgen_acik(y, a, b, z, h1, 0.3, 0.7, h1 * 0.25, h1 * 0.7, (govde, 'tas_koyu', 'tas_acik', 'ahsap_koyu'), derin=0.008)
            kafes(y, a, b, z, 0.3, 0.7, h1 * 0.25, h1 * 0.7, 'ahsap_koyu', 3, 4, 0.0025, 0.003)
    for p in k8:
        y.prizma((p.x, p.y), 0.008, z, z + h1, 'tas_acik', n=6)
    z += h1
    z_ilk = z + kat_h * 1.6 * 0.26
    # the eaves: bracket band, eave slab with its tiles, a drum; one surface of revolution
    rad = lambda k: r * (1 - (1 - daralma) * (k / max(1, n_kat - 1)) ** 1.3)
    for k in range(n_kat):
        rk = rad(k)
        rn = rad(k + 1) if k < n_kat - 1 else rk * 0.8
        e = sk * (1.0 if k == 0 else 0.75) * rk / r
        hh = kat_h * (1.6 if k == 0 else 1.0) * (1 - 0.25 * k / n_kat)
        pr = [(rk, z), (rk + e * 0.25, z + hh * 0.18), (rk + e, z + hh * 0.26), (rk + e, z + hh * 0.36), (rn, z + hh * 0.72)]
        # bracket band and soffit, fascia, the tiled slope (each band its own key)
        for j, key in enumerate((konsol, 'ahsap_koyu', 'ahsap_koyu', cati)):
            donel(y, c, [pr[j], pr[j + 1]], key, n=8, kat=kat)
        z += hh * 0.72
        if k < n_kat - 1:
            donel(y, c, [(rn, z), (rn, z + hh * 0.28)], govde, n=8, kat=kat)   # the drum up to the next eave
            z += hh * 0.28
    zt = z
    y.yuz_yon([V(p.x, p.y, zt) for p in cokgen(c, rad(n_kat - 1) * 0.8, 8, kat)], cati, Z)
    # bells at the first eave's corners
    for p in cokgen(c, r + sk, 8, kat):
        y.prizma((p.x, p.y), 0.004, z_ilk - 0.012, z_ilk, uc, n=5)
    # the finial: lotus, jewel
    donel(y, c, [(r * 0.35, zt - 0.004), (r * 0.42, zt + 0.012), (r * 0.25, zt + 0.02), (0.0, zt + 0.02)], uc, n=8, kat=kat)
    return sorin(y, c[0], c[1], zt + 0.012, r * 0.9, uc, halka=5)


def kosk(y, c, w, z, h, cati_h, sacak=0.04, direk='lake', cati='kiremit_koyu', mahya='kiremit_koyu2', kivrim=0.55, yukari=0.03,
         kaide='granit', korkuluk=True, aci=0.0, sorinli=True):
    """an open square pavilion (ting): a stone base, four lacquered posts with a frieze and seats, a curved pyramid roof
    and a knob. Returns the tip z"""
    with parca(y, (c[0], c[1], 0), aci):
        kutu_merkez(y, (0, 0), w + 0.03, w + 0.03, 0.02, kaide, z0=z)
        silme(y, dikdortgen(-(w + 0.03) / 2, (w + 0.03) / 2, -(w + 0.03) / 2, (w + 0.03) / 2), z + 0.016, 0.004, 0.003, 'tas_acik')
        zb = z + 0.02
        for sx in (-1, 1):
            for sy in (-1, 1):
                kutu_merkez(y, (sx * (w / 2 - 0.007), sy * (w / 2 - 0.007)), 0.012, 0.012, h, direk, z0=zb)
        k = dikdortgen(-w / 2, w / 2, -w / 2, w / 2)
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            e = (b - a).normalized(); L = (b - a).length
            kutu(y, a + Z * (zb + h * 0.82), e, L, 0.012, h * 0.18, direk)
            # a fretwork band under the frieze
            for j in range(1, 6):
                p = a.lerp(b, j / 6)
                cubuk(y, p + Z * (zb + h * 0.7), p + Z * (zb + h * 0.82), 0.003, 'altin')
            if korkuluk and i != 0:
                kutu(y, a + e * 0.012 + Z * (zb + 0.022), e, L - 0.024, 0.01, 0.006, direk)
                for j in range(1, 5):
                    p = a.lerp(b, j / 5) + V(-e.y, e.x) * 0.005
                    cubuk(y, p + Z * zb, p + Z * (zb + 0.022), 0.004, direk)
        y.yuz_yon([V(p.x, p.y, zb + h) for p in k], 'ahsap_koyu', -Z)
        tepe = cati_kirma(y, -w / 2, w / 2, -w / 2, w / 2, zb + h, cati_h, sacak, cati, mahya, 0.01, kivrim, yukari, 'lake_koyu', ns=8, nr=5)
        if sorinli:
            kure(y, (0, 0, tepe + 0.012), 0.012, 'altin', n=8, kat=4)
            tepe += 0.024
    return tepe


def sogut(y, x, yy, z, boy=0.16, key='zeytin', govde='ahsap', tohum=0):
    """a weeping willow: a leaning trunk, a crown and hanging strands"""
    import random
    r = random.Random(tohum)
    tepe = V(x + 0.01, yy, z + boy * 0.62)
    boru(y, [V(x, yy, z - 0.005), V(x + 0.004, yy, z + boy * 0.35), tepe], 0.007, govde, n=6, r_son=0.004)
    kure(y, (tepe.x, tepe.y, tepe.z + boy * 0.12), boy * 0.26, key, n=10, kat=5)
    for i in range(9):
        a = TAU * i / 9 + r.uniform(-0.2, 0.2)
        d = V(math.cos(a), math.sin(a))
        p0 = tepe + d * (boy * 0.2) + Z * (boy * 0.14)
        p1 = p0 + d * (boy * 0.08) - Z * (boy * 0.05)
        p2 = p1 + d * (boy * 0.02) - Z * (boy * r.uniform(0.3, 0.42))
        boru(y, [p0, p1, p2], boy * 0.03, key, n=4, r_son=boy * 0.012)


def cin_duvar(y, yol, z0, h, t=0.018, key='siva_kirmizi', cati='kiremit_koyu', kapali=False, kaide='granit'):
    """a Chinese compound wall along a polyline (or closed CCW polygon; outer face to the right of travel): plastered
    faces on a stone foot, a small tiled coping roof with a ridge, end caps on an open run"""
    O = [V(p[0], p[1]) for p in yol]
    n = len(O)
    I = disa(O, -t, kapali)
    Oe, M, Ie = disa(O, 0.011, kapali), disa(O, -t / 2, kapali), disa(O, -t - 0.011, kapali)
    m = n if kapali else n - 1
    zc, zr = z0 + h - 0.003, z0 + h + 0.016
    for i in range(m):
        j = (i + 1) % n
        e = (O[j] - O[i]); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
        duz_duvar(y, O[i], O[j], z0, z0 + h, key)
        duz_duvar(y, I[j], I[i], z0, z0 + h, key)
        duz_duvar(y, O[i] + nn * 0.003, O[j] + nn * 0.003, z0, z0 + 0.018, kaide)
        y.yuz_yon([O[i] + Z * (z0 + 0.018), O[j] + Z * (z0 + 0.018), O[j] + nn * 0.003 + Z * (z0 + 0.018), O[i] + nn * 0.003 + Z * (z0 + 0.018)], kaide, Z)
        y.yuz_yon([Oe[i] + Z * zc, Oe[j] + Z * zc, M[j] + Z * zr, M[i] + Z * zr], cati, nn + Z * 1.2)
        y.yuz_yon([Ie[j] + Z * zc, Ie[i] + Z * zc, M[i] + Z * zr, M[j] + Z * zr], cati, -nn + Z * 1.2)
        y.yuz_yon([O[i] + Z * (z0 + h), O[j] + Z * (z0 + h), Oe[j] + Z * zc, Oe[i] + Z * zc], 'ahsap_koyu', -Z)
        y.yuz_yon([I[j] + Z * (z0 + h), I[i] + Z * (z0 + h), Ie[i] + Z * zc, Ie[j] + Z * zc], 'ahsap_koyu', -Z)
        cubuk(y, M[i] + Z * (zr + 0.002), M[j] + Z * (zr + 0.002), 0.006, cati + '2' if cati + '2' in ('kiremit_koyu2', 'kiremit2') else cati)
    if not kapali:
        for k, s in ((0, -1), (n - 1, 1)):
            e = (O[1] - O[0]) if k == 0 else (O[-1] - O[-2]); e.z = 0; e.normalize()
            y.yuz_yon([O[k] + Z * z0, I[k] + Z * z0, I[k] + Z * (z0 + h), O[k] + Z * (z0 + h)], key, e * s)
            y.yuz_yon([Oe[k] + Z * zc, O[k] + Z * (z0 + h), I[k] + Z * (z0 + h), Ie[k] + Z * zc, M[k] + Z * zr], cati, e * s)


def pailou(y, c, w, h, aci=0.0, direk='lake', cati='kiremit_koyu', mahya='kiremit_koyu2', levha='lacivert'):
    """a three-bay memorial archway (pailou): four lacquered posts on stone drums with braces, lintels, a name board, and
    three small hipped roofs (the middle one higher) on bracket blocks. Returns the top z"""
    with parca(y, (c[0], c[1], 0), aci):
        xs = [-w / 2, -w / 6, w / 6, w / 2]
        z0 = 0.0
        for x in xs:
            donel(y, (x, 0), [(0.014, z0), (0.014, z0 + 0.018), (0.01, z0 + 0.022)], 'granit', n=8)
            y.yuz_yon([V(x + 0.01 * math.cos(TAU * i / 8), 0.01 * math.sin(TAU * i / 8), z0 + 0.022) for i in range(8)], 'granit', Z)
            hx = h if x in (-w / 6, w / 6) else h * 0.82
            kutu_merkez(y, (x, 0), 0.011, 0.011, hx, direk, z0=z0)
            for s in (-1, 1):   # the leaning braces
                cubuk(y, V(x, s * 0.028, z0), V(x, s * 0.004, z0 + h * 0.4), 0.004, 'ahsap_koyu')
        tepe = 0
        for (xa, xb, zt, ana) in ((-w / 6, w / 6, h, True), (-w / 2, -w / 6, h * 0.82, False), (w / 6, w / 2, h * 0.82, False)):
            kutu(y, V(xa - 0.006, -0.008, zt - 0.03), X, xb - xa + 0.012, 0.016, 0.014, direk)
            kutu(y, V(xa - 0.006, -0.008, zt - 0.06), X, xb - xa + 0.012, 0.016, 0.01, direk)
            if ana:
                kutu(y, V(-0.03, -0.0095, zt - 0.05), X, 0.06, 0.019, 0.02, levha)
                kutu(y, V(-0.024, -0.011, zt - 0.046), X, 0.048, 0.022, 0.012, 'altin')
            # bracket blocks and the roof
            nb = max(2, int((xb - xa) / 0.02))
            for k in range(nb + 1):
                kutu_merkez(y, (xa + (xb - xa) * k / nb, 0), 0.008, 0.022, 0.012, 'boya_yesil' if k % 2 else 'ahsap', z0=zt - 0.016)
            tp = cati_kirma(y, xa - 0.004, xb + 0.004, -0.012, 0.012, zt - 0.004, 0.035 if ana else 0.028, 0.022, cati, mahya, 0.006, 0.5, 0.012,
                            'lake_koyu', ns=6, nr=3)
            tepe = max(tepe, tp)
    return tepe
