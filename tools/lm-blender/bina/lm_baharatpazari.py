# Baharat Pazarı (lm_baharatpazari): a Mughal-era spice market square in the manner of Delhi's Khari Baoli / Chandni
# Chowk: a paved chowk ringed by colour-washed havelis (shops under striped awnings, jharokha balconies, jali windows,
# chhatris on the roofs); at its head a red sandstone Mughal gate with an iwan, a row of little marble domes and two tall
# banded minarets; in the square spice stalls with conical heaps (chilli red, turmeric yellow, green cardamom, brown
# cumin, saffron orange) in baskets and sacks, bullock carts, camels and a crowd.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from hint_ortak import *
from hint_ek import *
from arap_ortak import deve

y = Yapi()
rn = random.Random(11)
KT, KTA, MR = 'kirmizi_tas', 'kirmizi_tas_acik', 'mermer'
KRM = (KT, KT, KTA, 'koyu')
NIS = (KT, KT, KTA, KTA)
Z0 = 0.03
GX0, GX1, GY0, GY1 = -1.08, 1.08, -1.0, 1.0
BAHARAT = ['boya_kirmizi', 'boya_sari', 'boya_yesil', 'ahsap_acik', 'siva_oker', 'kerpic_koyu', 'lake']
TENTE = [('boya_kirmizi', 'beyaz'), ('boya_sari', 'boya_kirmizi'), ('boya_yesil', 'beyaz'), ('lacivert', 'boya_sari'), ('siva_oker', 'beyaz')]

# ---------------- the paved square ----------------
y.bolum('Meydan')
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'tas_koyu', 'onarkasagsol')
y.yuz_yon([V(GX0, GY0, Z0), V(GX1, GY0, Z0), V(GX1, GY1, Z0), V(GX0, GY1, Z0)], 'zemin', Z)
silme(y, dikdortgen(GX0, GX1, GY0, GY1), Z0 - 0.008, 0.008, 0.005, 'tas_koyu', 'duz')
# a raised kerb walk in front of the shops, a drain channel down the middle of the square
for (x0, x1, y0, y1) in ((-0.73, -0.66, -0.8, 0.52), (0.66, 0.73, -0.8, 0.52)):
    kutu(y, V(x0, y0, Z0), X, x1 - x0, y1 - y0, 0.012, 'tas', 'onarkasagsolust')


# ---------------- helpers ----------------
def cephe(a, b, z, h, k, renk, trim, n, tohum, kubbe_key, tk, tenteli=True):
    """one storey of a haveli street front a->b (facing its right): shops with an awning on the ground floor (k 0),
    jharokhas and jali windows above"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    if k == 0:
        for i in range(n):
            p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
            dikdortgen_acik(y, p, q, z, h, 0.1, 0.9, 0.0, h * 0.78, (renk, 'ahsap_koyu', 'ahsap', 'koyu'), derin=0.03, cerceve=(0.004, trim), ic_kenar=True)
            m = p.lerp(q, 0.14)
            kutu(y, m + nc * 0.004 + Z * z, e, (q - p).length * 0.72, 0.014, 0.012, 'ahsap', 'onsagsolust')
        if tenteli:
            tente_z0(y, a + e * 0.004, b - e * 0.004, z + h * 0.92, 0.05, 0.022, Z0, tk)
        return
    nb = max(2, int(round(L / 0.09)))
    for i in range(nb):
        p, q = a.lerp(b, i / nb), a.lerp(b, (i + 1) / nb)
        if (i + k + tohum) % 3 == 1 and h > 0.07:
            duz_duvar(y, p, q, z, z + h, renk)
            jharokha2(y, p, q, z + h * 0.18, min(0.07, (q - p).length * 0.8), h * 0.62, 0.032, renk, trim,
                      cati='bangla' if (i + tohum) % 2 else 'kubbe', cati_key=kubbe_key or trim, perde=trim if i % 2 else None, bicim='dochala')
        else:
            dikdortgen_acik(y, p, q, z, h, 0.25, 0.75, h * 0.2, h * 0.78, (renk, renk, trim, 'koyu'), derin=0.01, cerceve=(0.004, trim), ic_kenar=True)
            if (i + k) % 2 == 0:
                kafes(y, p, q, z, 0.25, 0.75, h * 0.2, h * 0.78, trim, 3, 3, 0.002, 0.0015)


def haveli(cx, cy, w, d, katlar, aci, renk, trim='siva', n=3, tente_k=None, tohum=0, chh=False, kubbe_key=None, cati='kangura', arka=False):
    """a haveli facing -y (before turning by aci) centred at (cx, cy): w wide, d deep, storeys of the heights katlar.
    Ground floor: n shop openings with a striped awning; upper floors: jharokhas and jali windows; chhajjas between
    the storeys; a parapet (rounded merlons or a plain one) and, chh, a chhatri on the roof. arka: the back is a street
    front too. Returns the roof z"""
    r = random.Random(tohum)
    tk = tente_k or TENTE[tohum % len(TENTE)]
    with parca(y, (cx, cy, 0), aci):
        x0, x1, y0, y1 = -w / 2, w / 2, -d / 2, d / 2
        z = Z0
        on, ar = (V(x0, y0), V(x1, y0)), (V(x1, y1), V(x0, y1))
        for k, h in enumerate(katlar):
            cephe(on[0], on[1], z, h, k, renk, trim, n, tohum, kubbe_key, tk)
            if arka:
                cephe(ar[0], ar[1], z, h, k, renk, trim, n, tohum + 1, kubbe_key, TENTE[(tohum + 2) % len(TENTE)])
            elif k == 0:
                duz_duvar(y, ar[0], ar[1], z, z + h, renk)
            else:   # (the back: plain windows on the upper floors, no big blank wall)
                nb = max(2, int(round(w / 0.1)))
                for i in range(nb):
                    p, q = ar[0].lerp(ar[1], i / nb), ar[0].lerp(ar[1], (i + 1) / nb)
                    dikdortgen_acik(y, p, q, z, h, 0.3, 0.7, h * 0.25, h * 0.75, (renk, renk, trim, 'koyu'), derin=0.008)
            for (a, b) in ((V(x1, y0), V(x1, y1)), (V(x0, y1), V(x0, y0))):
                if k == 0:
                    duz_duvar(y, a, b, z, z + h, renk)
                    continue
                ns = max(1, int(round(d / 0.1)))   # (small windows on the upper floors' end walls)
                for i in range(ns):
                    dikdortgen_acik(y, a.lerp(b, i / ns), a.lerp(b, (i + 1) / ns), z, h, 0.32, 0.68, h * 0.28, h * 0.72,
                                    (renk, renk, trim, 'koyu'), derin=0.008)
            if k > 0:
                silme(y, dikdortgen(x0, x1, y0, y1), z - 0.004, 0.008, 0.005, trim, 'duz')
            z += h
            if k < len(katlar) - 1:
                chhajja(y, [on[0], on[1]], z - 0.012, 0.012, 0.022, trim, kapali=False)
                if arka: chhajja(y, [ar[0], ar[1]], z - 0.012, 0.012, 0.022, trim, kapali=False)
        hk = dikdortgen(x0, x1, y0, y1)
        chhajja(y, [on[0], on[1]], z - 0.012, 0.012, 0.024, trim, kapali=False)
        if arka: chhajja(y, [ar[0], ar[1]], z - 0.012, 0.012, 0.024, trim, kapali=False)
        y.yuz_yon([V(p.x, p.y, z) for p in hk], 'zemin', Z)
        if cati == 'kangura':
            parapet(y, hk, z, 0.01, 0, 0.008, renk, ust_key=trim)
            kangura(y, on[0], on[1], z + 0.01, h=0.02, kal=0.008, key=renk, delik=None, n_yay=3)
            if arka: kangura(y, ar[0], ar[1], z + 0.01, h=0.02, kal=0.008, key=renk, delik=None, n_yay=3)
        else:
            parapet(y, hk, z, 0.018, 0, 0.008, renk, ust_key=trim)
        if chh:
            chhatri2(y, x0 + 0.05, y0 + 0.05, z, 0.03, n=6, kolon=trim, kubbe=kubbe_key or trim, kaide=renk, kat=0.0, nk=12)
        if r.random() < 0.6:
            kutu_merkez(y, (x1 - 0.05, y1 - 0.05), 0.04, 0.04, 0.025, trim, z0=z)
        # spices drying on the roof: chillies, turmeric, coriander spread on mats
        for m_ in range(1 + (w > 0.25)):
            mx = x0 + w * (0.3 + 0.38 * m_) + r.uniform(-0.02, 0.02)
            my = r.uniform(y0 + 0.06, y1 - 0.115)
            kk = BAHARAT[r.randrange(len(BAHARAT))]
            kutu_merkez(y, (mx, my), 0.07, 0.05, 0.002, ('kece', 'kumas', 'boya_sari')[r.randrange(3)], z0=z, aci=r.uniform(-0.2, 0.2))
            for j in range(3):
                yigin(y, mx - 0.022 + 0.022 * j, my, z + 0.002, 0.012, 0.006, kk if j != 1 else BAHARAT[(BAHARAT.index(kk) + 2) % len(BAHARAT)],
                      sepetli=False, n=8)
    return z


def minar(cx, cy, h=0.7, r=0.045):
    """a Mughal minaret: an octagonal red shaft banded with white marble, two corbelled balconies, an open chhatri on top"""
    y.prizma((cx, cy), r * 1.25, Z0, Z0 + 0.06, KT, n=8, kat=math.pi / 8, ust=True)
    silme(y, cokgen((cx, cy), r * 1.25, 8, math.pi / 8), Z0 + 0.06, 0.012, 0.008, KTA, 'kaide')
    zs = Z0 + 0.06
    seg = [(zs, zs + h * 0.38, r), (zs + h * 0.38, zs + h * 0.68, r * 0.88), (zs + h * 0.68, zs + h * 0.86, r * 0.78)]
    for i, (za, zb, rr) in enumerate(seg):
        y.prizma((cx, cy), rr, za, zb, KT, n=8, kat=math.pi / 8, ust=False)
        for f in (0.33, 0.66):
            halka_kornis(y, (cx, cy), rr, za + (zb - za) * f, 0.006, 0.003, 8, MR, kat=math.pi / 8)
        # balcony: corbels, a floor ring and a little railing
        ring = cokgen((cx, cy), rr, 8, math.pi / 8)
        konsol_halka(y, ring, zb - 0.02, 0.02, 0.022, KTA, 2)
        dis = disa(ring, 0.022)
        y.yuz_yon([V(p.x, p.y, zb) for p in dis], KTA, Z)
        parapet(y, dis, zb, 0.014, 0, 0.004, MR, ust_key=MR)
    zt = zs + h * 0.86
    return chhatri2(y, cx, cy, zt, r * 0.95, n=8, kolon=MR, kubbe=MR, kaide=KT, kat=math.pi / 8, nk=16, s_son=1.2)


# ---------------- the Mughal gate ----------------
y.bolum('Babür kapısı ve minareler')
GY = 0.62
gx0, gx1, gy0, gy1 = -0.22, 0.22, GY, GY + 0.26
GH = 0.4
L_, a0, a1, hs, apex = kemer_nis(y, V(gx0, gy0), V(gx1, gy0), Z0, GH, en=0.56, ust=0.08, sivri=0.32, derin=0.08, key=KT, yan_key=KT,
                                 alt_key=KTA, k_say=12, cerceve=(0.01, [MR, KTA]))
pa, pb = L_(a0, -Z0, 0.08), L_(a1, -Z0, 0.08)
hd = hs * 0.6
dilimli(y, pa, pb, Z0, hd, (KT, KT, KTA, 'ahsap'), en=0.6, ust=0.02, derin=0.02, sivri=0.25, dilim=5, gir=0.05, cerceve=(0.006, MR))
kat_ = [pa.lerp(pb, t) for t in (0.16, 0.84)]
# (the back wall round the window band, not behind it: it flickered through)
duz_duvar(y, pa, pb, Z0 + hd, Z0 + hd + 0.02, KT)
duz_duvar(y, pa, kat_[0], Z0 + hd + 0.02, Z0 + hd + 0.095, KT)
duz_duvar(y, kat_[1], pb, Z0 + hd + 0.02, Z0 + hd + 0.095, KT)
duz_duvar(y, pa, pb, Z0 + hd + 0.095, Z0 + apex, KT)
for i in range(3):
    p, q = kat_[0].lerp(kat_[1], i / 3), kat_[0].lerp(kat_[1], (i + 1) / 3)
    dilimli(y, p, q, Z0 + hd + 0.02, 0.075, KRM, v0=0.008, en=0.6, ust=0.012, derin=0.008, sivri=0.3, dilim=3, gir=0.05, korkuluk=0.014)
# alfiz frame
for (u0, u1, v0_, v1_) in ((a0 - 0.034, a0 - 0.024, 0.0, apex + 0.03), (a1 + 0.024, a1 + 0.034, 0.0, apex + 0.03),
                            (a0 - 0.034, a1 + 0.034, apex + 0.02, apex + 0.03)):
    p, q = L_(u0, v0_, -0.002), L_(u1, v0_, -0.002)
    y.yuz_yon([p, q, L_(u1, v1_, -0.002), L_(u0, v1_, -0.002)], MR, -Y)
    for (A, B, nn) in ((L_(u0, v1_, -0.002), L_(u1, v1_, -0.002), Z), (L_(u0, v0_, -0.002), L_(u0, v1_, -0.002), -X),
                       (L_(u1, v0_, -0.002), L_(u1, v1_, -0.002), X)):
        y.yuz_yon([A, B, B + Y * 0.002, A + Y * 0.002], MR, nn)
for (u0, u1) in ((0.012, a0 - 0.048), (a1 + 0.048, 0.44 - 0.012)):
    for (v0_, v1_) in ((0.04, 0.18), (0.21, 0.35)):
        nis_satir(y, L_(u0, 0, -0.0025), L_(u1, 0, -0.0025), Z0 + v0_, Z0 + v1_, 1, NIS, en=0.62, derin=0.008, sivri=0.3)
        cikinti_kenar(y, L_(u0, 0, -0.0025), L_(u1, 0, -0.0025), Z0 + v0_, Z0 + v1_, 0.0025, KT)
for (a, b) in ((V(gx1, gy0), V(gx1, gy1)), (V(gx1, gy1), V(gx0, gy1)), (V(gx0, gy1), V(gx0, gy0))):
    nis_satir(y, a, b, Z0, Z0 + GH, 3 if a.x == b.x else 5, NIS, en=0.6, derin=0.006, sivri=0.3)
gk = dikdortgen(gx0, gx1, gy0, gy1)
zt = Z0 + GH
silme(y, gk, Z0, 0.03, 0.01, KT, 'kaide')
chhajja(y, gk, zt - 0.03, 0.016, 0.028, KTA)
# (the walls reach zt: no second band, it flickered)
y.yuz_yon([V(p.x, p.y, zt) for p in gk], 'zemin', Z)
parapet(y, gk, zt, 0.014, 0, 0.012, KT, ust_key=KTA)
kangura_halka(y, gk, zt + 0.014, h=0.024, kal=0.01, key=KT, delik=None, n_yay=3)
# the screen of little domed arches over the iwan
sx0, sx1, sy0, sy1 = -0.16, 0.16, gy0 + 0.012, gy0 + 0.06
zs, hs_ = zt + 0.014, 0.055
dilimli_sira(y, V(sx0, sy0), V(sx1, sy0), 7, zs, hs_, KRM, en=0.62, ust=0.012, derin=0.018, sivri=0.3, dilim=3, gir=0.05)
for (a, b) in ((V(sx1, sy1), V(sx0, sy1)), (V(sx1, sy0), V(sx1, sy1)), (V(sx0, sy1), V(sx0, sy0))):
    duz_duvar(y, a, b, zs, zs + hs_, KT)
ks = dikdortgen(sx0, sx1, sy0, sy1)
chhajja(y, ks, zs + hs_ - 0.006, 0.008, 0.012, KTA)
y.yuz_yon([V(p.x, p.y, zs + hs_ + 0.002) for p in ks], KTA, Z)
duvarlar(y, ks, zs + hs_, zs + hs_ + 0.002, KT)
for i in range(7):
    xm = sx0 + (sx1 - sx0) * (i + 0.5) / 7
    ym = (sy0 + sy1) / 2
    y.prizma((xm, ym), 0.016, zs + hs_ + 0.002, zs + hs_ + 0.01, KTA, n=10, ust=False)
    lotus_hafif(y, (xm, ym), 0.0165, zs + hs_ + 0.01, 0.018, MR, n=10, yaprak=MR, s_son=0.4)
# a big central dome behind the screen
y.prizma((0, gy0 + 0.16), 0.07, zt + 0.014, zt + 0.05, KT, n=24)
halka_kornis(y, (0, gy0 + 0.16), 0.07, zt + 0.044, 0.008, 0.006, 24, KTA)
lotus_hafif(y, (0, gy0 + 0.16), 0.068, zt + 0.05, 0.075, MR, n=24, yaprak=MR, s_son=1.2)
# the minarets
for sx in (-1, 1):
    minar(sx * 0.27, GY + 0.04, h=0.72, r=0.045)
sancak(y, 0.0, gy0 + 0.16, zt + 0.14, boy=0.2, en=0.11, yuk=0.065, aci=-0.6)

# ---------------- havelis round the square ----------------
y.bolum('Havelîler')
RENK = ['siva_oker', 'siva_krem', 'siva', 'siva_kirmizi', 'kum', 'siva_oker', 'siva_krem', 'siva']
# left row (facing +x)
sol = [(-0.62, 0.27, (0.12, 0.1)), (-0.33, 0.29, (0.12,)), (-0.03, 0.29, (0.12, 0.1)), (0.26, 0.27, (0.12, 0.1, 0.09))]
for k, (yc, w, kat) in enumerate(sol):
    haveli(-0.84, yc, w, 0.22, kat, math.pi / 2, RENK[k], n=3, tohum=k, chh=(k == 2), kubbe_key=MR if k == 2 else None,
           cati='kangura' if k % 2 == 0 else 'duz', arka=True)
sag = [(-0.62, 0.27, (0.12, 0.1)), (-0.33, 0.29, (0.12, 0.1, 0.09)), (-0.03, 0.29, (0.12, 0.1)), (0.26, 0.27, (0.12, 0.1, 0.09, 0.07))]
for k, (yc, w, kat) in enumerate(sag):
    haveli(0.84, yc, w, 0.22, kat, -math.pi / 2, RENK[k + 4], n=3, tohum=k + 4, chh=(k == 3), kubbe_key=MR if k == 3 else None,
           cati='duz' if k % 2 == 0 else 'kangura')
# the back row beside the gate (facing -y)
for k, (xc, w, kat) in enumerate(((-0.6, 0.38, (0.12, 0.1, 0.08)), (0.6, 0.38, (0.12, 0.1)))):
    haveli(xc, 0.8, w, 0.24, kat, 0.0, ('siva_kirmizi', 'siva_oker')[k], n=4, tohum=k + 8, chh=True, kubbe_key=MR)
# front corners: low shop sheds
for k, xc in enumerate((-0.84, 0.84)):
    haveli(xc, -0.86, 0.22, 0.16, (0.11,), -math.pi / 2 if xc > 0 else math.pi / 2, ('siva_krem', 'kum')[k], n=2, tohum=k + 2, cati='duz', arka=True)

# ---------------- the spice stalls ----------------
y.bolum('Baharat tezgâhları')


def tezgah(cx, cy, w=0.2, d=0.1, tohum=0, aci=0.0):
    """a spice stall: a low wooden platform with rows of baskets of conical heaps, sacks round it and a striped
    awning on four poles"""
    r = random.Random(tohum)
    with parca(y, (cx, cy, 0), aci):
        kutu(y, V(-w / 2, -d / 2, Z0), X, w, d, 0.016, 'ahsap', 'onarkasagsolust')
        for i in range(4):
            for j in range(2):
                px, py = -w / 2 + w * (i + 0.5) / 4, -d / 2 + d * (j + 0.5) / 2
                yigin(y, px, py, Z0 + 0.016, 0.016, 0.026 + r.random() * 0.008, BAHARAT[(i + j * 3 + tohum) % len(BAHARAT)], n=8)
        for i in range(3):
            cuval(y, -w / 2 + w * (i + 0.5) / 3, -d / 2 - 0.018, Z0, 'kumas', r=0.01, h=0.02, ag=BAHARAT[(i + tohum + 2) % len(BAHARAT)])
        tk = TENTE[tohum % len(TENTE)]
        for (px, py) in ((-w / 2, -d / 2 - 0.02), (w / 2, -d / 2 - 0.02), (-w / 2, d / 2), (w / 2, d / 2)):
            y.prizma((px, py), 0.0025, Z0, Z0 + (0.085 if py < 0 else 0.1), 'ahsap_koyu', n=4)
        tente(y, V(-w / 2 - 0.006, d / 2), V(w / 2 + 0.006, d / 2), Z0 + 0.1, d + 0.03, 0.015, tk, direkli=False)


for k, (cx, cy) in enumerate(((-0.35, -0.4), (0.0, -0.45), (0.35, -0.4), (-0.35, -0.05), (0.35, -0.05), (-0.4, 0.32), (0.4, 0.32))):
    tezgah(cx, cy, tohum=k)
# heaps straight on mats in the open
for k in range(8):
    px, py = -0.15 + 0.1 * (k % 4), 0.12 + 0.12 * (k // 4)
    kutu_merkez(y, (px, py), 0.07, 0.07, 0.002, ('boya_kirmizi', 'kece', 'lacivert', 'boya_sari')[k % 4], z0=Z0)
    yigin(y, px, py, Z0 + 0.002, 0.028, 0.04, BAHARAT[(k * 2) % len(BAHARAT)], sepetli=False, n=10)
# a spice seller's corner near the entrance: heaps on mats, sacks, a weighing scale
for k in range(6):
    px, py = -0.3 + 0.12 * k, -0.8 + 0.05 * (k % 2)
    kutu_merkez(y, (px, py), 0.075, 0.06, 0.002, ('kece', 'boya_kirmizi', 'lacivert')[k % 3], z0=Z0)
    for j, dx in enumerate((-0.018, 0.018)):
        yigin(y, px + dx, py, Z0 + 0.002, 0.016, 0.026, BAHARAT[(k + j * 3) % len(BAHARAT)], n=8)
    cuval(y, px, py + 0.04, Z0, 'kumas', r=0.01, h=0.02, ag=BAHARAT[(k + 5) % len(BAHARAT)])
# sacks stacked by the shops
for k in range(10):
    side = -1 if k < 5 else 1
    py = -0.7 + 0.3 * (k % 5)
    cuval(y, side * 0.62, py, Z0 + 0.012 if False else Z0, 'kumas', r=0.012, h=0.024, ag=BAHARAT[k % len(BAHARAT)])

# ---------------- carts, camels, people ----------------
y.bolum('Arabalar, develer, kalabalık')
araba(y, 0.15, -0.72, Z0, aci=math.pi * 0.55, s=1.0, yuk=['kumas', 'kece', 'boya_sari'], okuz='beyaz')
araba(y, -0.13, 0.03, Z0, aci=-0.3, s=0.95, yuk=['kumas', 'boya_kirmizi'], okuz='kum_acik')
deve(y, 0.52, -0.72, Z0, math.pi * 0.6, renk='ahsap_acik', yuk=True, cul='boya_kirmizi', olcek=1.2)
deve(y, -0.52, 0.5, Z0, -0.4, renk='kum_acik', yuk=True, cul='lacivert', olcek=1.2)
deve(y, 0.2, 0.42, Z0, math.pi, renk='ahsap_acik', yuk=False, cok=True, cul='boya_sari', olcek=1.2)
GOV = ['beyaz', 'boya_kirmizi', 'boya_sari', 'kumas', 'boya_yesil', 'siva_oker', 'lacivert', 'beyaz']
BAS = ['beyaz', 'boya_sari', 'boya_kirmizi', 'siva_oker']
for k in range(42):
    px, py = rn.uniform(-0.62, 0.62), rn.uniform(-0.95, 0.5)
    if any(abs(px - cx) < 0.14 and abs(py - cy) < 0.09 for cx, cy in ((-0.35, -0.4), (0.0, -0.45), (0.35, -0.4), (-0.35, -0.05),
                                                                         (0.35, -0.05), (-0.4, 0.32), (0.4, 0.32))):
        continue
    adam(y, px, py, Z0, rn.uniform(0, TAU), GOV[k % len(GOV)], BAS[k % len(BAS)], boy=0.034 + rn.uniform(-0.003, 0.004))
for (tx, ty) in ((-0.55, -0.25), (0.55, 0.15), (0.55, -0.62)):
    agac2(y, tx, ty, Z0, boy=0.16, key='boya_yesil', n=8)
    donel(y, (tx, ty), [(0.05, Z0), (0.05, Z0 + 0.016), (0.042, Z0 + 0.016), (0.0, Z0 + 0.016)], 'tas', n=12)

bolum_say(y)
calistir(y, 'lm_baharatpazari')
