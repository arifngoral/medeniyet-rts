# Bursa Ulu Camii (lm_ulucami): a 5 x 4 grid of twenty equal domes on square bases and windowed octagonal drums over
# a rectangular cut-stone hall; the walls in tall pointed blind arches, each holding two rectangular windows below
# and a pointed window above; a muqarnas portal on the north (front), smaller portals on the sides, the lantern
# (aydınlık feneri) over the second dome of the middle axis, and two minarets at the front corners.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.05                    # platform top
B = 0.38                     # bay (dome) size
NX, NY = 5, 4
XW, YW = B * NX / 2, B * NY / 2
HW = 0.44                  # wall height
ZR = Z0 + HW                 # roof
V0 = 0.03                    # the niches start above the plinth
ALT = 0.2                  # the line between the lower (rectangular) and upper (pointed) windows

# ---------------- ornament helpers ----------------
def yildiz(o, ex, nrm, r, key, k=8, ic=0.5, d=0.0025, kat=0.0, yan_key=None):
    """a raised k-pointed star (carved geometric ornament): o on the surface, ex along it, nrm out"""
    o, ex, nrm = V(*o), V(*ex), V(*nrm)
    up = nrm.cross(ex).normalized()
    pts = [o + ex * ((r if i % 2 == 0 else r * ic) * math.cos(kat + math.pi * i / k)) + up * ((r if i % 2 == 0 else r * ic) * math.sin(kat + math.pi * i / k)) for i in range(2 * k)]
    y.yuz_yon([p + nrm * d for p in pts], key, nrm)
    for i in range(2 * k):
        p, q = pts[i], pts[(i + 1) % (2 * k)]
        y.yuz_yon([p, q, q + nrm * d, p + nrm * d], yan_key or key, (p + q) / 2 - o)


def portal_sus(cx, cy, z0, en, H, nis, nrm=None):
    """carved stars along the outer border of a tackapi_mukarnas (front on y = cy, facing -y), lozenges on its inner
    border, rosettes in the spandrels and a dentil row under the cornice"""
    bw = en * 0.07
    zb = z0 + H - 0.016
    n = max(3, int((zb - bw - z0 - 0.02) / (bw * 1.1)))
    for sx in (-1, 1):
        for i in range(n):
            zz = z0 + 0.03 + (zb - bw - z0 - 0.04) * (i + 0.5) / n
            yildiz((cx + sx * (en / 2 - bw / 2), cy - 0.006, zz), X, -Y, bw * 0.4, 'tas_acik', yan_key='tas_koyu', kat=math.pi / 8)
    m = max(3, int((en - 2 * bw) / (bw * 1.1)))
    for i in range(m):
        xx = cx - en / 2 + bw + (en - 2 * bw) * (i + 0.5) / m
        yildiz((xx, cy - 0.006, zb - bw / 2), X, -Y, bw * 0.4, 'tas_acik', yan_key='tas_koyu', kat=math.pi / 8)
    hw = nis * en / 2 + 0.012 + bw * 0.6
    bi = bw * 0.55
    zi = z0 + H * 0.88 + bw * 0.7
    for sx in (-1, 1):
        zz, k = z0 + 0.03, 0
        while zz < zi - bi:
            yildiz((cx + sx * (hw - bi / 2), cy - 0.004, zz), X, -Y, bi * 0.42, 'tas_koyu' if k % 2 else 'tas', k=2, ic=0.55, d=0.002)
            zz += bi * 1.1; k += 1
        yildiz((cx + sx * hw * 0.62, cy - 0.0025, z0 + H * 0.88 - 0.03), X, -Y, 0.014, 'mermer', k=12, ic=0.72, yan_key='tas_koyu')
    nk = int(en / 0.028)
    for i in range(nk):
        kutu_merkez(y, (cx - en / 2 + en * (i + 0.5) / nk, cy - 0.006), 0.011, 0.011, 0.011, 'tas_koyu', z0=zb - 0.028)


# ---------------- platform ----------------
y.bolum('Zemin, meydan ve basamaklar')
zemin(y, -XW - 0.2, XW + 0.2, -YW - 0.28, YW + 0.14, Z0, 'tas_koyu', 'zemin', basamak=(('on', 0.56),), n_basamak=3)


# ---------------- walls ----------------
def bay(a, b):
    """one wall bay: a tall pointed blind arch holding two framed rectangular windows and a pointed window above"""
    L, x0, x1, hs, apex = kemer_nis(y, a, b, Z0, HW, en=0.72, ust=0.03, sivri=0.74, derin=0.016, key='tas', yan_key='tas_acik',
                                    v0=V0, k_say=12, cerceve=(0.008, 'tas_acik'))
    d = 0.016
    a2, b2 = L(x0, -Z0, d), L(x1, -Z0, d)          # (on the ground plane: kemerli adds its own z)
    m2 = a2.lerp(b2, 0.5)
    for p, q in ((a2, m2), (m2, b2)):
        dikdortgen_acik(y, p, q, Z0 + V0, ALT - V0, 0.22, 0.78, 0.035, 0.125, ('tas', 'tas_koyu', 'tas_acik', 'cam'), derin=0.014,
                        cerceve=(0.006, 'mermer'))
    # the upper pointed window, framed, with a small sill
    y.kemerli(a2, b2, Z0 + ALT, apex - ALT, ('tas', 'tas_koyu', 'tas_acik', 'cam'), v0=0.02, en=0.34, ust=0.04, derin=0.016, k_say=8,
              sivri=0.75, cerceve=(0.006, 'mermer'))
    # a thin string course across the niche between the two tiers
    e = (b2 - a2).normalized(); nc = V(e.y, -e.x)
    kutu(y, a2 + Z * (Z0 + ALT - 0.004) + nc * 0.006, e, (b2 - a2).length, 0.006, 0.006, 'tas_acik', 'onust')


def duvar_hatti(a, b, n, atla=()):
    for k in range(n):
        if k in atla: continue
        bay(a.lerp(b, k / n), a.lerp(b, (k + 1) / n))


y.bolum('Duvarlar: kör kemerler ve iki sıra pencere')
K = dikdortgen(-XW, XW, -YW, YW)
duvar_hatti(K[0], K[1], NX, atla=(2,))          # front (north)
duvar_hatti(K[1], K[2], NY, atla=(1,))          # east
duvar_hatti(K[2], K[3], NX)                     # back (qibla wall)
duvar_hatti(K[3], K[0], NY, atla=(2,))          # west

# ---------------- portals ----------------
y.bolum('Kuzey taçkapısı (mukarnaslı)')
PW, PH, PD = 0.34, 0.6, 0.07
# the wall left and right of the portal in the middle bay
for xa, xb in ((-B / 2, -PW / 2), (PW / 2, B / 2)):
    duz_duvar(y, V(xa, -YW), V(xb, -YW), Z0, ZR, 'tas')
top_p = tackapi_mukarnas(y, 0, -YW - PD, Z0, en=PW, H=PH, derin=PD, nis=0.56, sivri=0.55, mk_kat=6)
portal_sus(0, -YW - PD, Z0, PW, PH, 0.56)
duz_duvar(y, V(PW / 2, -YW), V(-PW / 2, -YW), ZR, Z0 + PH, 'tas')       # the portal's back above the roof

y.bolum('Yan kapılar')
SW, SH, SD = 0.22, 0.37, 0.045


def yan_kapi(x, yy, aci):
    with parca(y, (x, yy, 0), aci):
        tackapi_mukarnas(y, 0, -SD, Z0, en=SW, H=SH, derin=SD, nis=0.58, sivri=0.55, mk_kat=5)
        portal_sus(0, -SD, Z0, SW, SH, 0.58)


# east side, bay 1 (from the front) ; west side, bay 2 counted from the back = bay 1 from the front
yc = -YW + B * 1.5
yan_kapi(XW, yc, math.pi / 2)
yan_kapi(-XW, yc, -math.pi / 2)
for sx in (-1, 1):
    x = sx * XW
    ya, yb = yc - B / 2, yc + B / 2
    for p, q in ((ya, yc - SW / 2), (yc + SW / 2, yb)):
        a, b = (V(x, p), V(x, q)) if sx > 0 else (V(x, q), V(x, p))
        duz_duvar(y, a, b, Z0, ZR, 'tas')
    a, b = (V(x, yc - SW / 2), V(x, yc + SW / 2)) if sx > 0 else (V(x, yc + SW / 2), V(x, yc - SW / 2))
    duz_duvar(y, a, b, Z0 + SH, ZR, 'tas')

# ---------------- mouldings, corners, roof ----------------
y.bolum('Silmeler, köşe payeleri, çatı')
silme(y, K, Z0, 0.026, 0.012, 'tas_koyu', 'kaide')
silme(y, K, ZR - 0.022, 0.026, 0.018, 'tas_acik', 'tac')
for sx in (-1, 1):
    kutu_merkez(y, (sx * XW, YW), 0.04, 0.04, HW + 0.012, 'tas', z0=Z0)
y.yuz_yon([V(p.x, p.y, ZR + 0.004) for p in K], 'kursun', Z)

# ---------------- the twenty domes ----------------
y.bolum('Yirmi kubbe: kare kaideler, sekizgen kasnaklar')
LANTERN = (2, 1)
for j in range(NY):
    for i in range(NX):
        cx, cy = -XW + B * (i + 0.5), -YW + B * (j + 0.5)
        orta = (i == 2)
        # the middle axis stands higher on stone bases (the mihrab dome highest); every bay has a low lead skirt
        # (a pyramid roof) round the foot of its octagonal drum
        hb = (0.04 if orta else 0.0) + (0.02 if (i, j) == (2, 3) else 0.0)
        zb = ZR + 0.004
        s = 0.155
        if hb:
            kutu_merkez(y, (cx, cy), 2 * s, 2 * s, hb, 'tas', z0=zb, yuzler='onarkasagsol')
            kornis(y, cx - s, cx + s, cy - s, cy + s, zb + hb - 0.008, 0.01, 0.008, 'tas_acik', 'kaba')
        zs = zb + hb + (0.006 if hb else 0.0)
        cati_kirma(y, cx - s, cx + s, cy - s, cy + s, zs, 0.05, 0.012, 'kursun', 'kursun', kalinlik=0.008, alt_key='tas_acik',
                   ns=4, nr=2, mahya_en=0.006)
        r = 0.132
        kh = 0.07 if orta else 0.065
        tepe = kubbe_kasnakli(y, (cx, cy), r, zs + 0.006, kh, n_pencere=8, kubbe_h=r * (0.95 if orta else 0.88), n=32, kat=9,
                              en=0.42, alem_olcek=(0 if (i, j) == LANTERN else 0.85), cerceve=None)
        if (i, j) == LANTERN:
            # the lantern over the (open) dome above the fountain: a ring of arched windows, a small dome
            y.bolum('Aydınlık feneri')
            zl = tepe - 0.012
            lr = 0.045
            ok = cokgen((cx, cy), lr, 8, math.pi / 8)
            y.prizma((cx, cy), lr * 1.15, zl - 0.004, zl + 0.006, 'tas_acik', n=16)
            for k in range(8):
                y.kemerli(ok[k], ok[(k + 1) % 8], zl + 0.006, 0.05, ('tas_acik', 'tas_koyu', 'tas_acik', 'cam'), v0=0.006, en=0.55,
                          ust=0.008, derin=0.008, k_say=4, sivri=0.5)
            halka_kornis(y, (cx, cy), lr, zl + 0.056, 0.008, 0.008, 8, kat=math.pi / 8)
            t = y.kubbe((cx, cy), lr * 1.02, zl + 0.064, lr * 0.85, 'kursun', n=24, kat=6)
            alem(y, cx, cy, t.z, 0.8)

# ---------------- minarets ----------------
y.bolum('Minareler')
# (the west minaret of Yıldırım Bayezid with two balconies, the east one of Çelebi Mehmed with one)
for sx in (-1, 1):
    minare(y, sx * (XW + 0.012), -YW + 0.0, Z0, 1.08 if sx < 0 else 1.0, serefe=2 if sx < 0 else 1, kaide=HW + 0.03, r=0.036)

# ---------------- forecourt ----------------
y.bolum('Meydan: çınarlar, şadırvan, yollar, sancak')
# paved walks to the three portals, an ablution fountain in the square, old plane trees and cypresses, stone benches
y.yuz_yon([V(-0.09, -YW - 0.28, Z0 + 0.002), V(0.09, -YW - 0.28, Z0 + 0.002), V(0.09, -YW - PD, Z0 + 0.002), V(-0.09, -YW - PD, Z0 + 0.002)], 'tas_koyu', Z)
for sx in (-1, 1):
    x0, x1 = sorted((sx * (XW + SD), sx * (XW + 0.2)))
    yc_ = -YW + B * 1.5
    y.yuz_yon([V(x0, yc_ - 0.07, Z0 + 0.002), V(x1, yc_ - 0.07, Z0 + 0.002), V(x1, yc_ + 0.07, Z0 + 0.002), V(x0, yc_ + 0.07, Z0 + 0.002)], 'tas_koyu', Z)
sadirvan(y, -0.42, -YW - 0.15, Z0, olcek=0.9)
for sx, xx in ((-1, -0.78), (1, 0.6)):
    agac(y, xx, -YW - 0.16, Z0, boy=0.3, tur='yaprakli')
for (tx, ty) in ((0.86, -YW - 0.18), (-0.98, YW + 0.06), (0.98, YW + 0.06), (-0.98, 0.4), (0.98, 0.4)):
    agac(y, tx, ty, Z0, boy=0.2, tur='servi')
for xx in (0.3, 0.42):
    kutu_merkez(y, (xx, -YW - 0.2), 0.08, 0.03, 0.02, 'tas_acik', z0=Z0)
sancak(y, 0.1, -YW - PD * 0.5, top_p, boy=0.2, en=0.11, yuk=0.07, aci=0.0)

calistir(y, 'lm_ulucami')
