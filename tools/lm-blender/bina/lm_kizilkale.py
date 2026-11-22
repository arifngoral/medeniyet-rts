# Kızıl Kale (lm_kizilkale): the Red Fort of Delhi: red sandstone curtain walls with rounded bastions crowned by
# chhatris and rounded merlons behind a moat; the Lahori Gate (two octagonal towers with chhatris, a tall iwan, a row of
# seven little marble domes) and the Delhi Gate with its stone elephants; inside the Chatta Chowk, the Naubat Khana, the
# Diwan-i-Am (nine engrailed arches), the white marble Diwan-i-Khas, Rang Mahal and Musamman Burj along the river wall,
# the Nahr-i-Bihisht channel, the Hayat Bakhsh garden with its pavilions and the Moti Masjid's three marble domes.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from hint_ortak import *
from hint_ek import *
import doku

y = Yapi()
KT, KTA, MR = 'kirmizi_tas', 'kirmizi_tas_acik', 'mermer'
KRM = (KT, KT, KTA, 'koyu')
NIS = (KT, KT, KTA, 'kirmizi_tas_acik')
BYZ = (MR, 'tas_acik', MR, 'koyu')
Z0 = 0.03
WH = 0.2
WK = 0.07
GX0, GX1, GY0, GY1 = -1.2, 1.2, -1.1, 1.06
MY0, MY1 = -1.02, -0.94          # the moat (front)
W = [V(-0.7, -0.84), V(0.7, -0.84), V(1.0, -0.56), V(1.0, 0.66), V(0.76, 0.92), V(-0.76, 0.92), V(-1.0, 0.66), V(-1.0, -0.56)]


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def _mix(c0, c1, t):
    return tuple(p + (q - p) * t for p, q in zip(c0, c1))


def _icinde(x, yy, kose):
    ic = False
    n = len(kose)
    for i in range(n):
        a, b = kose[i], kose[(i + 1) % n]
        if (a.y > yy) != (b.y > yy) and x < a.x + (b.x - a.x) * (yy - a.y) / (b.y - a.y):
            ic = not ic
    return ic


def arazi_renk(x, yy, z):
    n = math.sin(x * 5.1 + 0.4) * math.cos(yy * 4.3 - 1.0) * 0.6 + math.sin(x * 11.0 - yy * 7.0) * 0.4
    if _icinde(x, yy, W):
        return _mix((0.80, 0.70, 0.54), (0.76, 0.64, 0.48), 0.5 + 0.5 * n)           # the beaten sand of the courts
    return _mix((0.44, 0.52, 0.28), (0.52, 0.53, 0.31), 0.5 + 0.5 * n)               # the lawns round the fort


doku.KOSE_RENK['toprak_ot'] = arazi_renk

# ---------------- ground and moat ----------------
y.bolum('Zemin ve hendek')
kutu(y, V(GX0, GY0, 0), X, GX1 - GX0, GY1 - GY0, Z0, 'toprak', 'onarkasagsol')
silme(y, dikdortgen(GX0, GX1, GY0, GY1), Z0 - 0.008, 0.008, 0.005, 'kum_koyu', 'duz')
S = 0.08
nx, ny = int(round((GX1 - GX0) / S)), int(round((GY1 - GY0) / S))
buyuk = set()
for i in range(0, nx - 1, 2):
    for j in range(0, ny - 1, 2):
        xa, xb, ya, yb = GX0 + S * i, GX0 + S * (i + 2), GY0 + S * j, GY0 + S * (j + 2)
        if yb > GY1 + 1e-6 or (ya < MY1 + 0.02 and yb > MY0 - 0.02): continue
        ins = [_icinde(px, py, W) for px, py in ((xa, ya), (xb, ya), (xb, yb), (xa, yb), ((xa + xb) / 2, (ya + yb) / 2))]
        dis_ = [_icinde(px, py, disa(W, 0.12)) for px, py in ((xa, ya), (xb, ya), (xb, yb), (xa, yb))]
        ic_ = [_icinde(px, py, disa(W, -0.12)) for px, py in ((xa, ya), (xb, ya), (xb, yb), (xa, yb))]
        if all(ic_) or not any(dis_):
            buyuk.add((i, j))
            y.yuz_yon([V(xa, ya, Z0), V(xb, ya, Z0), V(xb, yb, Z0), V(xa, yb, Z0)], 'toprak_ot', Z)
for i in range(nx):
    for j in range(ny):
        if (i - i % 2, j - j % 2) in buyuk: continue
        xa, xb = GX0 + S * i, GX0 + S * (i + 1)
        ya, yb = GY0 + S * j, min(GY1, GY0 + S * (j + 1))
        if ya >= MY0 - 1e-6 and yb <= MY1 + 1e-6 and -1.12 - 1e-6 <= xa and xb <= 1.12 + 1e-6 and not (-0.08 - 1e-6 <= xa and xb <= 0.08 + 1e-6):
            continue
        y.yuz_yon([V(xa, ya, Z0), V(xb, ya, Z0), V(xb, yb, Z0), V(xa, yb, Z0)], 'toprak_ot', Z)
ZS = Z0 - 0.016
for (xa, xb) in ((-1.12, -0.08), (0.08, 1.12)):
    y.yuz_yon([V(xa, MY0, ZS), V(xb, MY0, ZS), V(xb, MY1, ZS), V(xa, MY1, ZS)], 'su', Z)
    duz_duvar(y, V(xb, MY0), V(xa, MY0), ZS - 0.002, Z0, KT)          # the moat's outer revetment (faces +y)
    duz_duvar(y, V(xa, MY1), V(xb, MY1), ZS - 0.002, Z0, KT)          # inner (faces -y)
    if xa < 0: duz_duvar(y, V(xa, MY0), V(xa, MY1), ZS - 0.002, Z0, KT)      # (the moat's ends face into it)
    if xb > 0: duz_duvar(y, V(xb, MY1), V(xb, MY0), ZS - 0.002, Z0, KT)
# kerbs along the moat edges
for yy in (MY0, MY1):
    for (xa, xb) in ((-1.12, -0.08), (0.08, 1.12)):
        kutu(y, V(xa, yy - 0.006, Z0), X, xb - xa, 0.012, 0.006, KTA, 'onarkasagsolust')
# the causeway's parapets over the moat
for sx in (-1, 1):
    kutu(y, V(sx * 0.08 - (0.012 if sx > 0 else 0), MY0 - 0.02, Z0), X, 0.012, MY1 - MY0 + 0.04, 0.022, KT, 'onarkasagsolust')
    for yy in (MY0 - 0.02, MY1 + 0.02):
        kutu_merkez(y, (sx * 0.074, yy), 0.018, 0.018, 0.034, KTA, z0=Z0)
y.yuz_yon([V(-0.068, -1.1, Z0 + 0.002), V(0.068, -1.1, Z0 + 0.002), V(0.068, -0.92, Z0 + 0.002), V(-0.068, -0.92, Z0 + 0.002)], 'zemin', Z)


# ---------------- helpers ----------------
def guldasta(cx, cy, z, h, r=0.01, key=KTA, kubbe=MR):
    """a slender octagonal pinnacle with a little lotus dome"""
    y.prizma((cx, cy), r, z, z + h, key, n=8, kat=math.pi / 8, ust=False)
    halka_kornis(y, (cx, cy), r, z + h * 0.45, 0.004, 0.0025, 8, MR, kat=math.pi / 8)
    halka_kornis(y, (cx, cy), r, z + h - 0.004, 0.004, 0.004, 8, MR, kat=math.pi / 8)
    y.prizma((cx, cy), r * 1.25, z + h, z + h + 0.002, MR, n=8, kat=math.pi / 8)
    return lotus_hafif(y, (cx, cy), r * 1.05, z + h + 0.002, r * 1.1, kubbe, n=10, yaprak=MR, s_son=0.35)


def burj(c, r=0.075, h=WH + 0.03, cr=0.04):
    """a rounded bastion: a battered red shaft with string courses, a corbelled rim, rounded merlons and a chhatri"""
    zt = kule_yuvarlak(y, c, r, Z0, h, key=KT, cati='duz', mazgal_h=0, n=16, egim=0.09, yarik_say=0, bolum=2, konsol=False)
    for f in (0.5,):
        rr = r * (1 + 0.09 * (1 - f))
        donel(y, c, [(rr, Z0 + h * f), (rr + 0.004, Z0 + h * f), (rr + 0.004, Z0 + h * f + 0.008), (rr, Z0 + h * f + 0.008)], KTA, n=16)
    silme(y, cokgen(c, r, 16), Z0 + h - 0.024, 0.024, 0.014, KTA, 'duz')
    kangura_halka(y, cokgen(c, r, 10, math.pi / 10), zt, h=0.026, kal=0.012, key=KT, delik=None, n_yay=3, w=0.026, g=0.018)
    chhatri2(y, c[0], c[1], zt - 0.012, cr, n=8, kolon=KTA, kubbe=MR, kaide=KT, kat=math.pi / 8, nk=10)


def ic_cati(kose, z, key='zemin'):
    y.yuz_yon([V(p.x, p.y, z) for p in kose], key, Z)


def kosk(cx, cy, w, d, H, n_on, n_yan, aci=0.0, duvar=MR, trim='tas_acik', ph=0.025, arka_acik=False, cr=0.03, chh=4,
         kubbe=MR, korkuluk=True, kasnak_kubbe=None, derin=None, cerceve=True):
    """an open Mughal pavilion facing -y (before turning by aci): a plinth with steps, engrailed arches on its front
    (and sides; the back too if arka_acik), pilasters, a chhajja, a flat roof with a balustrade and chhatris at the
    corners (chh: 4 all corners, 2 the front ones, 0 none). Returns the roof z"""
    with parca(y, (cx, cy, 0), aci):
        x0, x1, y0, y1 = -w / 2, w / 2, -d / 2, d / 2
        zp = Z0 + ph
        kutu(y, V(x0 - 0.02, y0 - 0.02, Z0), X, w + 0.04, d + 0.04, ph, trim, 'onarkasagsolust')
        silme(y, dikdortgen(x0 - 0.02, x1 + 0.02, y0 - 0.02, y1 + 0.02), Z0, ph * 0.5, 0.006, trim, 'kaide')
        kutu(y, V(-w * 0.18, y0 - 0.05, Z0), X, w * 0.36, 0.032, ph * 0.6, trim, 'onsagsolust')
        rk = (duvar, duvar, trim, 'koyu')
        dr = derin or min(d * 0.42, 0.07)
        dilimli_sira(y, V(x0, y0), V(x1, y0), n_on, zp, H, rk, en=0.72, ust=H * 0.2, derin=dr, sivri=0.28, dilim=5, gir=0.06,
                     cerceve=(0.004, trim) if cerceve else None)
        if arka_acik:
            dilimli_sira(y, V(x1, y1), V(x0, y1), n_on, zp, H, rk, en=0.72, ust=H * 0.2, derin=dr, sivri=0.28, dilim=5, gir=0.06,
                         cerceve=(0.004, trim))
        else:
            nis_satir(y, V(x1, y1), V(x0, y1), zp, zp + H, n_on, rk, en=0.6, derin=0.006, sivri=0.3)
        for (a, b) in ((V(x1, y0), V(x1, y1)), (V(x0, y1), V(x0, y0))):
            dilimli_sira(y, a, b, n_yan, zp, H, rk, en=0.66, ust=H * 0.22, derin=0.005, sivri=0.28, dilim=5, gir=0.06)
        # pilasters on the front between the bays
        for i in range(n_on + 1):
            x = x0 + w * i / n_on
            kutu(y, V(x - 0.006, y0 - 0.005, zp), X, 0.012, 0.005, H, trim, 'onarkasagsolust')
        zt = zp + H
        k = dikdortgen(x0, x1, y0, y1)
        silme(y, k, zt - 0.014, 0.01, 0.006, trim, 'duz')
        chhajja(y, k, zt - 0.004, 0.014, 0.03, trim)
        ic_cati(k, zt + 0.01, 'zemin')
        duvarlar(y, k, zt, zt + 0.01, duvar)
        if korkuluk:
            parapet(y, k, zt + 0.01, 0.014, 0, 0.008, duvar, ust_key=trim)
            for p in k:
                kutu_merkez(y, (p.x, p.y), 0.014, 0.014, 0.03, trim, z0=zt + 0.01)
        kose = [(x0 + cr * 1.2, y0 + cr * 1.2), (x1 - cr * 1.2, y0 + cr * 1.2), (x1 - cr * 1.2, y1 - cr * 1.2), (x0 + cr * 1.2, y1 - cr * 1.2)]
        for i, (px, py) in enumerate(kose):
            if chh == 4 or (chh == 2 and i < 2):
                chhatri2(y, px, py, zt + 0.01, cr, n=8, kolon=trim if duvar == MR else KTA, kubbe=kubbe, kaide=duvar, kat=math.pi / 8, nk=12)
        if kasnak_kubbe:
            r, key = kasnak_kubbe
            y.prizma((0, 0), r * 1.02, zt + 0.01, zt + 0.04, duvar, n=24)
            halka_kornis(y, (0, 0), r * 1.02, zt + 0.034, 0.008, 0.006, 24, trim)
            lotus_kubbe(y, (0, 0), r, zt + 0.04, r * 0.95, key, n=24, kat=7, yaprak=trim, s_son=1.0)
    return zt + 0.01


def mugal_kapi(cx, cy, aci=0.0, s=1.0, GH=0.42, GT=0.52, bayrak=False, sade=False):
    """a Mughal fort gate facing -y (wall line y=0, before turning and scaling): a red block with a tall iwan framed in
    white marble, a door and windows in its back, two octagonal towers in tiers of blind arches crowned by chhatris, a
    screen of seven little domed arches over the iwan, pinnacles at its corners"""
    with parca(y, (cx, cy, 0), aci, s):
        x0, x1, y0, y1 = -0.19, 0.19, -0.08, 0.12
        z0 = Z0
        L_, a0, a1, hs, apex = kemer_nis(y, V(x0, y0), V(x1, y0), z0, GH, en=0.6, ust=0.07, sivri=0.32, derin=0.07, key=KT, yan_key=KT,
                                         alt_key=KTA, k_say=12, cerceve=(0.01, [MR, KTA]))
        # the iwan's back: a door below, a band of windows over it, its half vault seen as the soffit (kemer_nis)
        pa, pb = L_(a0, -z0, 0.07), L_(a1, -z0, 0.07)
        hd = hs * 0.62
        dilimli(y, pa, pb, z0, hd, (KT, KT, KTA, 'ahsap'), en=0.56, ust=0.02, derin=0.02, sivri=0.25, dilim=5, gir=0.05,
                cerceve=(0.006, MR))
        kat_ = [pa.lerp(pb, t) for t in (0.18, 0.82)]
        bantlar = [hd + 0.02] + ([hd + 0.13] if not sade and apex - hd > 0.17 else [])
        # (the back wall round the window bands: no wall behind them, it would flicker through)
        zz = hd
        for zb_ in ([] if sade else bantlar):
            duz_duvar(y, pa, pb, z0 + zz, z0 + zb_, KT)
            duz_duvar(y, pa, kat_[0], z0 + zb_, z0 + zb_ + 0.07, KT)
            duz_duvar(y, kat_[1], pb, z0 + zb_, z0 + zb_ + 0.07, KT)
            zz = zb_ + 0.07
        duz_duvar(y, pa, pb, z0 + zz, z0 + apex, KT)
        for zb_ in bantlar:
            for i in range(0 if sade else 3):
                p, q = kat_[0].lerp(kat_[1], i / 3), kat_[0].lerp(kat_[1], (i + 1) / 3)
                dilimli(y, p, q, z0 + zb_, 0.07, (KT, KT, KTA, 'koyu'), v0=0.008, en=0.6, ust=0.012, derin=0.008, sivri=0.3, dilim=3,
                        gir=0.05, korkuluk=0.014)
            silme(y, [pa + Z * (z0 + zb_ + 0.088), pb + Z * (z0 + zb_ + 0.088)], 0, 0.006, 0.005, KTA, 'duz', kapali=False)
        silme(y, [pa + Z * (z0 + hd), pb + Z * (z0 + hd)], 0, 0.008, 0.006, MR, 'duz', kapali=False)
        # the white marble frame (alfiz) round the iwan and inlaid panels on the piers
        for (u0, u1, v0_, v1_) in ((a0 - 0.032, a0 - 0.022, 0.0, apex + 0.03), (a1 + 0.022, a1 + 0.032, 0.0, apex + 0.03),
                                    (a0 - 0.032, a1 + 0.032, apex + 0.02, apex + 0.03)):
            p, q = L_(u0, v0_, -0.002), L_(u1, v0_, -0.002)
            y.yuz_yon([p, q, L_(u1, v1_, -0.002), L_(u0, v1_, -0.002)], MR, -Y)
            for (A, B, nn) in ((L_(u0, v1_, -0.002), L_(u1, v1_, -0.002), Z), (L_(u0, v0_, -0.002), L_(u0, v1_, -0.002), -X),
                               (L_(u1, v0_, -0.002), L_(u1, v1_, -0.002), X)):
                y.yuz_yon([A, B, B + Y * 0.002, A + Y * 0.002], MR, nn)
        satirlar = []
        v_ = 0.04
        while v_ + 0.13 <= GH - 0.05:
            satirlar.append((v_, v_ + 0.13)); v_ += 0.16
        for (u0, u1) in (() if sade else ((0.012, a0 - 0.045), (a1 + 0.045, 0.38 - 0.012))):
            for (v0_, v1_) in satirlar:
                p0, p1 = L_(u0, 0, -0.0025), L_(u1, 0, -0.0025)   # (proud of the pier face: no flicker)
                nis_satir(y, p0, p1, z0 + v0_, z0 + v1_, 1, NIS, en=0.62, derin=0.008, sivri=0.3)
                cikinti_kenar(y, p0, p1, z0 + v0_, z0 + v1_, 0.0025, KT)
        # side and back faces of the block
        duz_duvar(y, V(x1, y0), V(x1, y1), z0, z0 + GH, KT)
        duz_duvar(y, V(x0, y1), V(x0, y0), z0, z0 + GH, KT)
        y.kemerli(V(x1, y1), V(x0, y1), z0, GH * 0.7, KRM, en=0.38, ust=0.04, derin=0.05, k_say=10, sivri=0.3, cerceve=(0.008, MR))
        duz_duvar(y, V(x1, y1), V(x0, y1), z0 + GH * 0.7, z0 + GH * 0.72, KT)
        duz_duvar(y, V(x1, y1), V(x0, y1), z0 + GH - 0.03, z0 + GH, KT)
        nis_satir(y, V(x1, y1), V(x0, y1), z0 + GH * 0.72, z0 + GH - 0.03, 5, NIS, en=0.6, derin=0.006, sivri=0.3)
        # string courses and the chhajja round the top
        k = dikdortgen(x0, x1, y0, y1)
        zt = z0 + GH
        silme(y, k, z0, 0.03, 0.01, KT, 'kaide')
        chhajja(y, k, zt - 0.03, 0.016, 0.028, KTA)
        pass   # (the walls already reach zt: a second band there flickered)
        ic_cati(k, zt, 'zemin')
        parapet(y, k, zt, 0.014, 0, 0.012, KT, ust_key=KTA)
        kangura_halka(y, [k[1], k[2], k[3], k[0]], zt + 0.014, h=0.024, kal=0.01, key=KT, kapali=False)
        # the screen of seven little domed arches over the iwan
        sx0, sx1, sy0, sy1 = -0.15, 0.15, y0 + 0.012, y0 + 0.06
        zs, hs_ = zt + 0.014, 0.055
        dilimli_sira(y, V(sx0, sy0), V(sx1, sy0), 5 if sade else 7, zs, hs_, (KT, KT, KTA, 'koyu'), en=0.62, ust=0.012, derin=0.018, sivri=0.3, dilim=3,
                     gir=0.05)
        duz_duvar(y, V(sx1, sy1), V(sx0, sy1), zs, zs + hs_, KT)
        duz_duvar(y, V(sx1, sy0), V(sx1, sy1), zs, zs + hs_, KT)
        duz_duvar(y, V(sx0, sy1), V(sx0, sy0), zs, zs + hs_, KT)
        ks = dikdortgen(sx0, sx1, sy0, sy1)
        chhajja(y, ks, zs + hs_ - 0.006, 0.008, 0.012, KTA)
        ic_cati(ks, zs + hs_ + 0.002, KTA)
        duvarlar(y, ks, zs + hs_, zs + hs_ + 0.002, KT)
        nd = 5 if sade else 7
        for i in range(nd):
            xm = sx0 + (sx1 - sx0) * (i + 0.5) / nd
            ym = (sy0 + sy1) / 2
            y.prizma((xm, ym), 0.015, zs + hs_ + 0.002, zs + hs_ + 0.01, KTA, n=12, ust=False)
            lotus_hafif(y, (xm, ym), 0.0155, zs + hs_ + 0.01, 0.017, MR, n=10, yaprak=MR, s_son=0.4)
        for sx in (() if sade else (-1, 1)):
            guldasta(sx * 0.17, y0 + 0.02, zt + 0.014, 0.06, 0.011)
        # the two octagonal towers
        for sx in (-1, 1):
            c = (sx * 0.265, -0.04)
            r = 0.085
            y.prizma(c, r * 1.06, z0, z0 + 0.05, KT, n=8, kat=math.pi / 8)
            silme(y, cokgen(c, r * 1.06, 8, math.pi / 8), z0 + 0.05, 0.012, 0.008, KTA, 'kaide')
            ok = cokgen(c, r, 8, math.pi / 8)
            nt = max(1, int(round((GT - 0.05) / 0.165)))
            tiers = (0.05, GT) if sade else tuple(0.05 + (GT - 0.05) * i / nt for i in range(nt + 1))
            for t in range(len(tiers) - 1):
                za, zb = z0 + tiers[t], z0 + tiers[t + 1]
                for i in range(8):
                    p, q = ok[i], ok[(i + 1) % 8]
                    m = (p + q) / 2
                    if tiers[t + 1] <= GH - 0.02 and (m - V(c[0], c[1])).dot(V(-sx, 0)) > 0.07: continue   # (hidden in the block)
                    nis_satir(y, p, q, za, zb, 1, NIS, en=0.6, derin=0.008, sivri=0.3)
                halka_kornis(y, c, r, zb - 0.006, 0.008, 0.005, 8, MR if t % 2 == 0 else KTA, kat=math.pi / 8)
            zt2 = z0 + GT
            chhajja(y, ok, zt2 - 0.002, 0.014, 0.024, KTA)
            ic_cati(ok, zt2 + 0.012, 'zemin')
            duvarlar(y, ok, zt2, zt2 + 0.012, KT)
            kangura_halka(y, ok, zt2 + 0.012, h=0.022, kal=0.009, key=KT)
            chhatri2(y, c[0], c[1], zt2 + 0.012, 0.058, n=8, kolon=KTA, kubbe=MR, kaide=KT, kat=math.pi / 8, s_son=1.2, nk=16)
        if bayrak:
            sancak(y, 0.0, 0.08, zt + 0.014, boy=0.34, en=0.13, yuk=0.08, aci=-0.6)


# ---------------- the walls and bastions ----------------
y.bolum('Surlar')
# the curtain wall, opened at the two gates
LG, DG = (V(-0.2, -0.84), V(0.2, -0.84)), (V(1.0, -0.36), V(1.0, -0.04))
yolA = [LG[1], W[1], W[2], DG[0]]
yolB = [DG[1], W[3], W[4], W[5], W[6], W[7], W[0], LG[0]]
for yol in (yolA, yolB):
    sur(y, yol, Z0, WH, kalinlik=WK, key=KT, mazgal_h=0, parapet_h=0.012, ust_key=KTA)
    for i in range(len(yol) - 1):
        e_ = (yol[i + 1] - yol[i]).normalized()
        on_ = V(e_.y, -e_.x).dot(V(-0.57, -0.82)) > 0.3      # (loopholes only on the faces the game sees)
        kangura(y, yol[i], yol[i + 1], Z0 + WH + 0.012, h=0.03, kal=0.014, key=KT, delik='koyu' if on_ else None, n_yay=3, w=0.027, g=0.018)
    silme(y, yol, Z0, 0.05, 0.016, KT, 'kaide', kapali=False)
    silme(y, yol, Z0 + WH * 0.55, 0.008, 0.005, KTA, 'duz', kapali=False)
    silme(y, yol, Z0 + WH - 0.018, 0.01, 0.007, KTA, 'duz', kapali=False)

y.bolum('Burçlar ve köşkleri')
BURJLAR = [W[0], W[1], W[2], W[3], W[4], W[5], W[6], W[7], V(-0.46, -0.84), V(0.46, -0.84), V(-1.0, 0.05)]
for c in BURJLAR:
    burj((c.x, c.y))

y.bolum('Lahor Kapısı')
mugal_kapi(0.0, -0.84, 0.0, 1.0, GH=0.58, GT=0.74, bayrak=True)
y.bolum('Delhi Kapısı ve taş filler')
# (a plain gateway between two bastions: the Lahori Gate is the hero)
for c in ((1.0, -0.36), (1.0, -0.04)):
    burj(c, r=0.07, h=WH + 0.05, cr=0.038)
DGX0, DGX1, DGY0, DGY1 = 0.93, 1.03, -0.33, -0.07
dilimli(y, V(DGX1, DGY0), V(DGX1, DGY1), Z0, WH + 0.04, (KT, KT, KTA, 'ahsap'), en=0.5, ust=0.06, derin=0.05, sivri=0.3, dilim=5,
        gir=0.05, cerceve=(0.008, MR))
y.kemerli(V(DGX0, DGY1), V(DGX0, DGY0), Z0, WH * 0.75, KRM, en=0.5, ust=0.03, derin=0.04, k_say=8, sivri=0.3)
duz_duvar(y, V(DGX0, DGY1), V(DGX0, DGY0), Z0 + WH * 0.75, Z0 + WH + 0.04, KT)
for (a, b) in ((V(DGX0, DGY0), V(DGX1, DGY0)), (V(DGX1, DGY1), V(DGX0, DGY1))):
    duz_duvar(y, a, b, Z0, Z0 + WH + 0.04, KT)
dk = dikdortgen(DGX0, DGX1, DGY0, DGY1)
chhajja(y, dk, Z0 + WH + 0.026, 0.014, 0.02, KTA)
ic_cati(dk, Z0 + WH + 0.04, 'zemin')
parapet(y, dk, Z0 + WH + 0.04, 0.012, 0, 0.01, KT, ust_key=KTA)
kangura(y, dk[1], dk[2], Z0 + WH + 0.052, h=0.026, kal=0.01, key=KT, delik=None, n_yay=3)
silme(y, dk, Z0, 0.04, 0.012, KT, 'kaide')
for sy in (-1, 1):
    kutu_merkez(y, (1.13, -0.2 + sy * 0.12), 0.11, 0.05, 0.02, KTA, z0=Z0)
    fil(y, 1.13, -0.2 + sy * 0.12, Z0 + 0.02, aci=0.0, olcek=0.85, key='granit', az=True)
    for lx in (-0.03, 0.026):      # (the light elephant's square legs are open at the top)
        for ly in (-0.016, 0.016):
            px, py = 1.13 + lx * 0.85, -0.2 + sy * 0.12 + ly * 0.85
            y.yuz_yon([V(p.x, p.y, Z0 + 0.02 + 0.062 * 0.85) for p in dikdortgen(px - 0.0095 * 0.85, px + 0.0095 * 0.85, py - 0.0095 * 0.85, py + 0.0095 * 0.85)], 'granit', Z)
y.yuz_yon([V(1.06, -0.25, Z0 + 0.002), V(1.2, -0.25, Z0 + 0.002), V(1.2, -0.15, Z0 + 0.002), V(1.06, -0.15, Z0 + 0.002)], 'zemin', Z)

# ---------------- Chatta Chowk and Naubat Khana ----------------
y.bolum('Çatta Çarşısı ve Nevbethane')
CX0, CX1, CY0, CY1 = -0.11, 0.11, -0.72, -0.44
CH = 0.11
for (a, b) in ((V(CX1, CY0), V(CX1, CY1)), (V(CX0, CY1), V(CX0, CY0))):
    nis_satir(y, a, b, Z0, Z0 + CH * 0.62, 5, KRM, en=0.62, derin=0.01, sivri=0.3)
    duz_duvar(y, a, b, Z0 + CH * 0.96, Z0 + CH, KT)
    duz_duvar(y, a, b, Z0 + CH * 0.62, Z0 + CH * 0.66, KT)
    for i in range(5):
        if i in (0, 4): u0, u1 = (0, 0.065) if i == 0 else (0.935, 1)
        else: u0, u1 = (i - 0.5) / 4 + 0.06, (i + 0.5) / 4 - 0.06
        duz_duvar(y, a.lerp(b, u0), a.lerp(b, u1), Z0 + CH * 0.66, Z0 + CH * 0.96, KT)
    e = (b - a).normalized()
    for i in range(4):
        p, q = a.lerp(b, (i + 0.5) / 4 - 0.06), a.lerp(b, (i + 0.5) / 4 + 0.06)
        dilimli(y, p, q, Z0 + CH * 0.66, CH * 0.3, (KT, KT, KTA, 'koyu'), en=0.5, ust=0.004, derin=0.008, sivri=0.3, dilim=3, gir=0.05)
duz_duvar(y, V(CX1, CY1), V(CX0, CY1), Z0, Z0 + CH, KT)
ck = dikdortgen(CX0, CX1, CY0, CY1)
chhajja(y, ck, Z0 + CH - 0.012, 0.012, 0.018, KTA)
ic_cati(ck, Z0 + CH + 0.004, 'zemin')
duvarlar(y, ck, Z0 + CH, Z0 + CH + 0.004, KT)
parapet(y, ck, Z0 + CH + 0.004, 0.012, 0, 0.008, KT, ust_key=KTA)
# its octagonal lantern over the central court
y.prizma((0, (CY0 + CY1) / 2), 0.07, Z0 + CH + 0.004, Z0 + CH + 0.04, KT, n=8, kat=math.pi / 8, ust=False)
for i, p in enumerate(cokgen((0, (CY0 + CY1) / 2), 0.07, 8, math.pi / 8)):
    q = cokgen((0, (CY0 + CY1) / 2), 0.07, 8, math.pi / 8)[(i + 1) % 8]
    yarik(y, p + Z * (Z0 + CH + 0.004), (q - p), V((q - p).y, -(q - p).x), 0.012, 0.01, 0.03, 0.016, 'koyu')
halka_kornis(y, (0, (CY0 + CY1) / 2), 0.07, Z0 + CH + 0.036, 0.008, 0.008, 8, KTA, kat=math.pi / 8)
ic_cati(cokgen((0, (CY0 + CY1) / 2), 0.07, 8, math.pi / 8), Z0 + CH + 0.044, KTA)
# Naubat Khana: a two-storey drum house over the way to the Diwan-i-Am
NX0, NX1, NY0, NY1 = -0.17, 0.17, -0.36, -0.24
NH1, NH2 = 0.11, 0.09
for k_, (a, b) in enumerate(((V(NX0, NY0), V(NX1, NY0)), (V(NX1, NY1), V(NX0, NY1)))):
    p, q = a.lerp(b, 0.34), a.lerp(b, 0.66)
    nis_satir(y, a, p, Z0, Z0 + NH1, 1, KRM, en=0.55, derin=0.01, sivri=0.3)
    y.kemerli(p, q, Z0, NH1, KRM, en=0.62, ust=0.02, derin=(NY1 - NY0) / 2 - 0.002 * k_, k_say=10, sivri=0.3, cerceve=(0.006, MR))
    nis_satir(y, q, b, Z0, Z0 + NH1, 1, KRM, en=0.55, derin=0.01, sivri=0.3)
    dilimli_sira(y, a, b, 3, Z0 + NH1, NH2, KRM, v0=0.01, en=0.6, ust=0.02, derin=0.02, sivri=0.3, dilim=5, gir=0.05, korkuluk=0.014)
for (a, b) in ((V(NX1, NY0), V(NX1, NY1)), (V(NX0, NY1), V(NX0, NY0))):
    nis_satir(y, a, b, Z0, Z0 + NH1, 1, KRM, en=0.55, derin=0.008, sivri=0.3)
    nis_satir(y, a, b, Z0 + NH1, Z0 + NH1 + NH2, 1, KRM, en=0.55, derin=0.008, sivri=0.3)
nk = dikdortgen(NX0, NX1, NY0, NY1)
silme(y, nk, Z0 + NH1 - 0.004, 0.01, 0.008, MR, 'duz')
ZN = Z0 + NH1 + NH2
chhajja(y, nk, ZN - 0.014, 0.014, 0.024, KTA)
ic_cati(nk, ZN + 0.004, 'zemin')
duvarlar(y, nk, ZN, ZN + 0.004, KT)
parapet(y, nk, ZN + 0.004, 0.012, 0, 0.008, KT, ust_key=KTA)
kangura_halka(y, nk, ZN + 0.016, h=0.02, kal=0.008, key=KT)
y.yuz_yon([V(-0.06, -0.44, Z0 + 0.002), V(0.06, -0.44, Z0 + 0.002), V(0.06, -0.36, Z0 + 0.002), V(-0.06, -0.36, Z0 + 0.002)], 'zemin', Z)

# ---------------- Diwan-i-Am ----------------
y.bolum('Divan-ı Am')
# its paved court
y.yuz_yon([V(-0.46, -0.24, Z0 + 0.002), V(0.46, -0.24, Z0 + 0.002), V(0.46, 0.32, Z0 + 0.002), V(-0.46, 0.32, Z0 + 0.002)], 'zemin', Z)
for (a, b) in ((V(-0.46, -0.24), V(0.46, -0.24)), (V(0.46, -0.24), V(0.46, 0.32)), (V(0.46, 0.32), V(-0.46, 0.32)), (V(-0.46, 0.32), V(-0.46, -0.24))):
    duz_duvar(y, a, b, Z0, Z0 + 0.002, 'zemin')
top_da = kosk(0.0, 0.12, 0.68, 0.22, 0.13, 9, 2, duvar=KT, trim=KTA, ph=0.03, cr=0.034, chh=2, kubbe=MR, derin=0.16, cerceve=False)

# ---------------- the river front: Rang Mahal, Musamman Burj, Diwan-i-Khas ----------------
y.bolum('Rang Mahal, Müsemmen Burç, Divan-ı Has')
kosk(-0.33, 0.73, 0.42, 0.2, 0.11, 5, 3, duvar=MR, trim='tas_acik', ph=0.025, cr=0.024, chh=0, kubbe='altin', cerceve=False)
kosk(0.5, 0.73, 0.36, 0.2, 0.12, 5, 3, duvar=MR, trim='tas_acik', ph=0.03, cr=0.028, chh=4, kubbe=MR, arka_acik=False)
# Musamman Burj: an octagonal marble tower on the river wall under a gilded dome
MB = (0.12, 0.95)
y.prizma(MB, 0.1, Z0, Z0 + WH, KT, n=8, kat=math.pi / 8)
silme(y, cokgen(MB, 0.1, 8, math.pi / 8), Z0, 0.05, 0.016, KT, 'kaide')
kangura_halka(y, cokgen(MB, 0.1, 8, math.pi / 8), Z0 + WH, h=0.024, kal=0.01, key=KT)
mk = cokgen(MB, 0.07, 8, math.pi / 8)
for i in range(8):
    dilimli(y, mk[i], mk[(i + 1) % 8], Z0 + WH, 0.1, BYZ, v0=0.008, en=0.66, ust=0.02, derin=0.012, sivri=0.3, dilim=5, gir=0.06,
            cerceve=(0.003, 'tas_acik'), korkuluk=0.014)
chhajja(y, mk, Z0 + WH + 0.096, 0.012, 0.022, 'tas_acik')
y.prizma(MB, 0.07, Z0 + WH + 0.1, Z0 + WH + 0.13, MR, n=24)
halka_kornis(y, MB, 0.07, Z0 + WH + 0.124, 0.008, 0.006, 24, 'tas_acik')
lotus_hafif(y, MB, 0.068, Z0 + WH + 0.13, 0.075, 'altin', n=24, yaprak='altin', s_son=1.0)

# ---------------- Nahr-i-Bihisht ----------------
y.bolum('Nehr-i Behişt')


def kanal(a, b, z=Z0, en=0.036, kerb=0.01, h=0.012):
    """a raised marble water channel a->b (the water a little under its kerb)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); n = V(e.y, -e.x)
    L = (b - a).length
    for s in (-1, 1):
        o = a + n * (s * (en / 2 + kerb / 2)) - n * (kerb / 2) - e * kerb
        kutu(y, o + Z * z, e, L + 2 * kerb, kerb, h, MR, 'onarkasagsolust')
    y.yuz_yon([a - n * (en / 2) + Z * (z + h * 0.6), b - n * (en / 2) + Z * (z + h * 0.6), b + n * (en / 2) + Z * (z + h * 0.6),
               a + n * (en / 2) + Z * (z + h * 0.6)], 'su', Z)
    for p, s in ((a, -1), (b, 1)):
        y.yuz_yon([p - n * (en / 2) + Z * z, p + n * (en / 2) + Z * z, p + n * (en / 2) + Z * (z + h * 0.6), p - n * (en / 2) + Z * (z + h * 0.6)], MR, e * s)


kanal((-0.92, 0.55), (0.9, 0.55))
for x in (-0.6, -0.33, 0.12, 0.5, 0.8):
    kutu_merkez(y, (x, 0.55), 0.07, 0.07, 0.006, MR, z0=Z0)
    y.yuz_yon([V(p.x, p.y, Z0 + 0.008) for p in cokgen((x, 0.55), 0.026, 8, math.pi / 8)], 'su', Z)
    halka_kornis(y, (x, 0.55), 0.026, Z0 + 0.006, 0.006, 0.004, 8, MR, kat=math.pi / 8)

# ---------------- Hayat Bakhsh garden ----------------
y.bolum('Hayat Bahş Bahçesi')
HX0, HX1, HY0, HY1 = -0.94, -0.5, -0.17, 0.46
for (xa, xb) in ((HX0, -0.735), (-0.705, HX1)):
    for (ya, yb) in ((HY0, 0.095), (0.125, HY1)):
        kutu(y, V(xa, ya, Z0), X, xb - xa, yb - ya, 0.006, 'kum_koyu', 'onarkasagsol')
        y.yuz_yon([V(xa, ya, Z0 + 0.006), V(xb, ya, Z0 + 0.006), V(xb, yb, Z0 + 0.006), V(xa, yb, Z0 + 0.006)], 'cimen', Z)
        for i in range(2):
            for j in range(2):
                agac2(y, xa + (xb - xa) * (i + 0.5) / 2, ya + (yb - ya) * (j + 0.5) / 2, Z0 + 0.006, boy=0.075, key='zeytin' if (i + j) % 2 else 'boya_yesil')
kanal((-0.72, HY0 + 0.03), (-0.72, 0.04))
kanal((-0.72, 0.18), (-0.72, HY1 - 0.04))
kanal((HX0 + 0.03, 0.11), (-0.79, 0.11))
kanal((-0.65, 0.11), (HX1 - 0.03, 0.11))
# the tank with Zafar Mahal in the middle
y.yuz_yon([V(p.x, p.y, Z0 + 0.006) for p in dikdortgen(-0.79, -0.65, 0.04, 0.18)], 'su', Z)
duvarlar(y, dikdortgen(-0.8, -0.64, 0.03, 0.19), Z0, Z0 + 0.014, KTA)
duvarlar(y, [V(-0.79, 0.18), V(-0.65, 0.18), V(-0.65, 0.04), V(-0.79, 0.04)], Z0 + 0.004, Z0 + 0.014, KTA)
for i, (a, b) in enumerate(((V(-0.8, 0.03), V(-0.64, 0.03)), (V(-0.64, 0.03), V(-0.64, 0.19)), (V(-0.64, 0.19), V(-0.8, 0.19)), (V(-0.8, 0.19), V(-0.8, 0.03)))):
    c, d = [V(-0.79, 0.04), V(-0.65, 0.04), V(-0.65, 0.18), V(-0.79, 0.18)][i], [V(-0.79, 0.04), V(-0.65, 0.04), V(-0.65, 0.18), V(-0.79, 0.18)][(i + 1) % 4]
    y.yuz_yon([a + Z * (Z0 + 0.014), b + Z * (Z0 + 0.014), d + Z * (Z0 + 0.014), c + Z * (Z0 + 0.014)], KTA, Z)
# (Zafar Mahal: a small red pavilion standing in the tank)
kutu_merkez(y, (-0.72, 0.11), 0.07, 0.07, 0.012, KTA, z0=Z0)
for (px, py) in ((-0.745, 0.085), (-0.695, 0.085), (-0.745, 0.135), (-0.695, 0.135)):
    kutu_merkez(y, (px, py), 0.01, 0.01, 0.045, KT, z0=Z0 + 0.012, yuzler='onarkasagsol')
zk = dikdortgen(-0.755, -0.685, 0.075, 0.145)
duvarlar(y, zk, Z0 + 0.057, Z0 + 0.067, KT, ust=KTA)
y.yuz_yon([V(p.x, p.y, Z0 + 0.057) for p in zk], KT, -Z)
chhajja(y, zk, Z0 + 0.06, 0.008, 0.012, KTA)
lotus_hafif(y, (-0.72, 0.11), 0.026, Z0 + 0.067, 0.024, MR, n=12, yaprak=MR, s_son=0.5)
# Sawan and Bhadon pavilions at the ends of the long channel
kosk(-0.72, HY0 - 0.035, 0.12, 0.06, 0.06, 2, 1, duvar=MR, trim='tas_acik', ph=0.012, cr=0.014, chh=0, kubbe=MR, derin=0.03, korkuluk=False)
kosk(-0.72, HY1 + 0.0, 0.12, 0.06, 0.06, 2, 1, aci=math.pi, duvar=MR, trim='tas_acik', ph=0.012, cr=0.014, chh=0, kubbe=MR, derin=0.03,
     korkuluk=False)

# ---------------- Moti Masjid ----------------
y.bolum('İnci Mescit')
MX0, MX1, MY0_, MY1_ = -0.62, -0.3, -0.7, -0.38
MH = 0.085
# the enclosure: white marble walls in blind arches, its gate facing the Lahori Gate road
mk2 = dikdortgen(MX0, MX1, MY0_, MY1_)
for i in range(4):
    a, b = mk2[i], mk2[(i + 1) % 4]
    if i == 0:
        p, q = a.lerp(b, 0.38), a.lerp(b, 0.62)
        nis_satir(y, a, p, Z0, Z0 + MH, 2, BYZ, en=0.6, derin=0.006, sivri=0.3)
        y.kemerli(p, q, Z0, MH + 0.03, BYZ, en=0.5, ust=0.024, derin=0.026, k_say=8, sivri=0.3, cerceve=(0.005, 'tas_acik'))
        nis_satir(y, q, b, Z0, Z0 + MH, 2, BYZ, en=0.6, derin=0.006, sivri=0.3)
        pass   # (the arch's wall already reaches the raised top)
    else:
        nis_satir(y, a, b, Z0, Z0 + MH, 5 if i % 2 == 0 else 4, BYZ, en=0.6, derin=0.006, sivri=0.3)
ic = disa(mk2, -0.03)
for i in range(4):
    duz_duvar(y, ic[(i + 1) % 4], ic[i], Z0, Z0 + MH, MR)
    y.yuz_yon([mk2[i] + Z * (Z0 + MH), mk2[(i + 1) % 4] + Z * (Z0 + MH), ic[(i + 1) % 4] + Z * (Z0 + MH), ic[i] + Z * (Z0 + MH)], 'tas_acik', Z)
silme(y, mk2, Z0 + MH - 0.008, 0.008, 0.005, 'tas_acik', 'duz')
y.yuz_yon([V(p.x, p.y, Z0 + 0.003) for p in disa(mk2, -0.03)], MR, Z)
# the gate's raised top over the wall
gp, gq = mk2[0].lerp(mk2[1], 0.38), mk2[0].lerp(mk2[1], 0.62)
kutu(y, gp + Z * (Z0 + MH) - Y * 0.0, X, (gq - gp).length, 0.03, 0.03, MR, 'arkasagsolust')
silme(y, [gp + Z * 0, gq + Z * 0], Z0 + MH + 0.026, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
# the prayer hall at the back of the court, its three engrailed arches facing the court (-y) and three domes
PY0, PY1 = MY1_ - 0.15, MY1_ - 0.03
PX0, PX1 = MX0 + 0.03, MX1 - 0.03
PH = 0.11
dilimli_sira(y, V(PX0, PY0), V(PX1, PY0), 3, Z0, PH, BYZ, en=0.68, ust=0.022, derin=0.05, sivri=0.3, dilim=5, gir=0.06, cerceve=(0.004, 'tas_acik'))
for (a, b) in ((V(PX1, PY0), V(PX1, PY1)), (V(PX0, PY1), V(PX0, PY0))):
    duz_duvar(y, a, b, Z0 + MH, Z0 + PH, MR)
duz_duvar(y, V(PX1, PY1), V(PX0, PY1), Z0 + MH, Z0 + PH, MR)
for i in range(4):
    x = PX0 + (PX1 - PX0) * i / 3
    kutu(y, V(x - 0.005, PY0 - 0.004, Z0), X, 0.01, 0.004, PH, 'tas_acik', 'onarkasagsolust')
pk = dikdortgen(PX0, PX1, PY0, PY1)
chhajja(y, [pk[0], pk[1]], Z0 + PH - 0.012, 0.012, 0.018, 'tas_acik', kapali=False)
ic_cati(pk, Z0 + PH + 0.006, MR)
duvarlar(y, pk, Z0 + PH, Z0 + PH + 0.006, MR)
parapet(y, pk, Z0 + PH + 0.006, 0.01, 0, 0.006, MR, ust_key='tas_acik')
for i in range(3):
    xm = PX0 + (PX1 - PX0) * (i + 0.5) / 3
    ym = (PY0 + PY1) / 2
    r = 0.044 if i == 1 else 0.037
    zb = Z0 + PH + 0.006
    y.prizma((xm, ym), r * 1.02, zb, zb + (0.05 if i == 1 else 0.04), MR, n=20, ust=False)
    halka_kornis(y, (xm, ym), r * 1.02, zb + (0.044 if i == 1 else 0.034), 0.006, 0.005, 20, 'tas_acik')
    tip = sogan_kubbe(y, (xm, ym), r, zb + (0.05 if i == 1 else 0.04), h=r * 2.2, key=MR, n=20, boyun=0.75, sivri=0.2)
    donel(y, (xm, ym), [(0.0, tip - 0.004), (0.006, tip + 0.004), (0.003, tip + 0.012), (0.005, tip + 0.017), (0.0, tip + 0.034)], 'altin', n=6)
for (px, py) in ((PX0, PY0), (PX1, PY0)):
    guldasta(px, py, Z0 + PH + 0.006, 0.06, 0.009, MR, MR)
# its marble court, a little tank
havuz(y, -0.5, -0.42, -0.62, -0.575, Z0 + 0.006, derin=0.012, kenar=0.008, key=MR)

# ---------------- the south quarter: Mumtaz Mahal, gardens ----------------
y.bolum('Mümtaz Mahal ve bahçe')
for (xa, xb, ya, yb) in ((0.52, 0.88, -0.66, -0.36), (0.52, 0.88, -0.28, -0.02)):
    kutu(y, V(xa, ya, Z0), X, xb - xa, yb - ya, 0.006, 'kum_koyu', 'onarkasagsol')
    y.yuz_yon([V(xa, ya, Z0 + 0.006), V(xb, ya, Z0 + 0.006), V(xb, yb, Z0 + 0.006), V(xa, yb, Z0 + 0.006)], 'cimen', Z)
    for i in range(2):
        for j in range(2):
            agac2(y, xa + (xb - xa) * (i + 0.5) / 2, ya + (yb - ya) * (j + 0.5) / 2, Z0 + 0.006, boy=0.08, key='boya_yesil' if (i + j) % 2 else 'zeytin')
for (tx, ty) in ((-0.7, -0.62), (-0.85, -0.4), (0.3, -0.62), (0.4, -0.5), (-0.22, -0.3), (0.25, 0.42), (-0.15, 0.42)):
    agac2(y, tx, ty, Z0, boy=0.09, key='boya_yesil')

# ---------------- people, horses, an elephant ----------------
y.bolum('Halk')
for k, (px, py, a) in enumerate(((0.045, -1.05, 1.5), (-0.045, -0.95, 1.6), (0.05, -0.2, 1.7),
                                  (0.15, -0.08, 2.0), (-0.2, -0.1, 0.8), (0.3, -0.15, 2.4), (-0.32, -0.18, 0.9), (0.05, -1.085, 1.6))):
    adam(y, px, py, Z0 + 0.002, a, ('beyaz', 'boya_kirmizi', 'boya_sari', 'kumas')[k % 4], ('beyaz', 'boya_sari', 'boya_kirmizi')[k % 3], boy=0.034)
fil(y, 0.0, -1.0, Z0 + 0.002, aci=math.pi / 2, olcek=0.7, key='fil', cul='boya_kirmizi', haudah='altin', binici='beyaz')

bolum_say(y)
calistir(y, 'lm_kizilkale')
