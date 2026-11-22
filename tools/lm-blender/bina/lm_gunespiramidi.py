# Güneş Piramidi (lm_gunespiramidi): the Pyramid of the Sun at Teotihuacan: five stone talud tiers (red-plastered rims)
# with flights of stairs up the west face, the adosada platform in front (talud-tablero with framed red panels), a
# small flat-roofed temple with merlons on the summit, the paved Avenue of the Dead along the front, small
# talud-tablero platform temples on the Plaza of the Sun, pilgrims and priests.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mexika_ortak import *

y = Yapi()
R = random.Random(5)
Z0 = 0.045


# ---------------------------------------------------------------- helpers
def teo_kademe(c, hw, hd, z0, h, ins, panel='siva_kirmizi', key='kirec', ust_key='kirec', disk=None):
    """a Teotihuacan talud-tablero tier: a short talud, a tall tablero framed by projecting bands round a recessed red
    panel; disk: a key for painted discs on the panels. Returns the band half sizes and the top z"""
    bw, bd, z1 = kademe(y, c, hw, hd, z0, h, ins, talud=0.36, key=key, bant_key=panel, ust_key=ust_key, cikinti=0.0)
    zm = z0 + h * 0.36; th = z1 - zm
    k = dikdortgen(c[0] - bw, c[0] + bw, c[1] - bd, c[1] + bd)
    silme(y, k, z1 - th * 0.24, th * 0.24, 0.008, key)       # the frame: top band (cornice)
    silme(y, k, zm, th * 0.16, 0.008, key)                     # bottom band
    for i in range(4):   # the frame's upright ends at the corners
        a, b = k[i], k[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for p, s in ((a, 1), (b, -1)):
            kutu(y, p + Z * (zm + th * 0.16), nn, 0.008, 0.016 * s, th * 0.6, key, 'onarkasagust')
        if disk:
            L = (b - a).length; m = max(1, int(L / 0.06))
            for j in range(m):
                pp = a.lerp(b, (j + 0.5) / m)
                y.oculus(pp + nn * 0.0006 + Z * (zm + th * 0.46), e, nn, th * 0.16, disk, 'kirec', f=th * 0.05, k=10)
    return bw, bd, z1


def teo_tapinak(cx, cy, w, d, z, kapi_yon=-math.pi / 2, sancakli=False):
    """a small Teotihuacan temple: red walls on a white plinth, a dark doorway, a painted frieze, a flat slab roof
    with a crest of merlons. kapi_yon: the doorway side. Returns the top z"""
    with parca(y, (cx, cy, z), kapi_yon + math.pi / 2):
        kutu_merkez(y, (0, 0), w + 0.03, d + 0.03, 0.016, 'kirec')
        H = 0.085 * (w / 0.22) ** 0.5
        kose = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        dikdortgen_kapi(y, kose[0], kose[1], 0.016, H, 0.33, 0.67, H * 0.68, 'siva_kirmizi', 'koyu', cerceve=(0.008, 'kirec'), derin=0.02)
        for i in (1, 2, 3):
            duz_duvar(y, kose[i], kose[(i + 1) % 4], 0.016, 0.016 + H, 'siva_kirmizi')
        silme(y, kose, 0.016 + H - 0.022, 0.022, 0.004, 'kirec')
        for i in range(4):
            a, b = kose[i], kose[(i + 1) % 4]
            e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
            m = max(2, int(L / 0.035))
            for j in range(m):
                pp = a.lerp(b, (j + 0.5) / m)
                y.oculus(pp + nn * 0.0045 + Z * (0.016 + H - 0.011), e, nn, 0.006, 'turkuaz', 'boya_sari', f=0.002, k=8)
        zs = 0.016 + H
        kutu_merkez(y, (0, 0), w + 0.024, d + 0.024, 0.014, 'kirec', z0=zs)
        ic = disa(dikdortgen(-w / 2 - 0.004, w / 2 + 0.004, -d / 2 - 0.004, d / 2 + 0.004), -0.004)
        almena_halka(y, ic, zs + 0.014, 0.04, 0.008, 'kirec', en=0.03, bosluk=0.01)
        top = zs + 0.054
        if sancakli:
            sancak(y, w / 2 - 0.01, d / 2 - 0.01, zs + 0.014, boy=0.2, en=0.1, yuk=0.06, aci=-0.6)
    return z + top


# ---------------------------------------------------------------- ground and the Avenue of the Dead
y.bolum('Zemin')
GX0, GX1, GY0, GY1 = -1.2, 1.2, -1.25, 1.27
zemin(y, GX0, GX1, GY0, GY1, Z0, 'kaya_koyu', 'cimen_kuru', basamak=(), silmeli=True)
# the Plaza of the Sun: paved in white lime plaster
PZ = Z0 + 0.004
kutu(y, V(-1.16, -0.98, Z0), X, 2.32, 2.21, 0.004, 'kirec', 'onarkasagsolust')
y.bolum('Oluler Caddesi')
# the avenue: a broad sunken way paved in stone, a low talud wall along its far side with stairs, a drain down the middle
kutu(y, V(GX0, GY0, Z0), X, GX1 - GX0, 0.27, 0.0015, 'zemin', 'onarkasagsolust')
for xx in (-0.82, 0.0, 0.82):
    # crossing stairs between the avenue and the plaza
    for k in range(2):
        kutu(y, V(xx - 0.16, -0.98 - 0.014 * (2 - k), Z0), X, 0.32, 0.014 * (2 - k) + 0.001, 0.004 * (k + 1) / 2.2 + 0.0015, 'kirec', 'onsagsolust')
for x0, x1 in ((GX0 + 0.02, -0.98), (-0.66, -0.16), (0.16, 0.66), (0.98, GX1 - 0.02)):
    # a low talud-tablero kerb along the plaza edge
    kutu(y, V(x0, -1.0, Z0), X, x1 - x0, 0.02, 0.022, 'kirec', 'onarkasagsolust')
    silme(y, [V(x0, -1.0), V(x1, -1.0)], Z0 + 0.012, 0.01, 0.004, 'siva_kirmizi', kapali=False)
# little platform shrines on the avenue's far edge (seen from behind the pyramid view: low, so they do not hide it)
for xx in (-0.75, 0.75):
    bw_, bd_, zt = teo_kademe((xx, -1.17), 0.16, 0.055, Z0, 0.05, 0.012)
    teo_tapinak(xx, -1.17, 0.14, 0.07, zt, kapi_yon=math.pi / 2)

# ---------------------------------------------------------------- the pyramid
y.bolum('Piramit')
CY = 0.27
hw = hd = 0.8
z = PZ
TIERS = [0.185, 0.16, 0.13, 0.11, 0.095]
H_TOP = sum(TIERS)
toplam_ins = 0.8 - 0.18 - 4 * 0.035
kat = []
for k, th in enumerate(TIERS):
    ins = toplam_ins * th / H_TOP / 0.92
    key = 'tas_volkan'
    bw_, bd_, z1 = kademe(y, (0, CY), hw, hd, z, th, ins, talud=0.9, key=key, bant_key='siva_kirmizi', ust_key='kirec', cikinti=0.08)
    kat.append((hw, hd, z, z1, bw_, bd_))
    # a white coping on the tier's rim
    silme(y, dikdortgen(-bw_, bw_, CY - bd_, CY + bd_), z1 - 0.006, 0.006, 0.004, 'kirec')
    hw, hd = bw_ - 0.035, bd_ - 0.035
    z = z1
ZT = z
TW = kat[-1][4]
# drain spouts and protruding tenon stones on the taluds (the face reads as built stone, not a smooth slope)
for k, (hw_, hd_, za, zb, bw_, bd_) in enumerate(kat):
    th = zb - za
    for i in range(4):
        kk = dikdortgen(-hw_, hw_, CY - hd_, CY + hd_)
        a, b = kk[i], kk[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        ins = hw_ - bw_
        L = (b - a).length
        m = int(L / 0.07)
        for r_, t in enumerate((0.2, 0.46, 0.72)):
            for j in range(1, m):
                u = (j + 0.5 * (r_ % 2)) / m
                if min(u, 1 - u) * L < ins * t + 0.025: continue
                p = a.lerp(b, u)
                if i == 0 and abs(p.x) < 0.2: continue
                if (j * 7 + r_ * 3 + k * 5 + i) % 5 == 0: continue
                q = p - nn * (ins * 0.9 * t) + Z * (za + th * 0.9 * t)
                w_ = 0.013 + 0.006 * ((j * 13 + r_ * 7 + i) % 3) / 2
                kutu(y, q - nn * 0.012 - e * (w_ / 2), e, w_, -0.019, 0.008 + 0.002 * ((j + r_) % 2), 'tas_volkan_koyu', 'onarkasagsolust')

# ---------------------------------------------------------------- the adosada
y.bolum('Adosada')
AF = CY - 0.8 - 0.3          # its front
AB = CY - kat[0][5]            # its back: the first tier's band (their tops abut)
z1a = PZ
for k, (hh, f, wx) in enumerate(((0.095, AF, 0.47), (0.09, AF + 0.06, 0.42))):
    bw_, bd_, z1a = teo_kademe((0.0, (f + AB + 0.018) / 2), wx, (AB + 0.018 - f) / 2, z1a, hh, 0.018, disk='turkuaz' if k == 1 else None)
    afr = (f + AB + 0.018) / 2 - bd_
ZA = z1a
ayak = alfarda_merdiven(y, 0.0, AF - (ZA - PZ) * 0.9, afr, PZ, ZA, 0.26, key='kirec', alf_key='kirec', alf_en=0.032, dado=0.12, dado_h=0.025,
                        basamak_key='kirec')
for p in ayak:
    yilan_basi(y, (p.x, p.y - 0.035, PZ), -math.pi / 2, 0.06, 'kirec', agiz='siva_kirmizi')
for sx in (-1, 1):
    mangal(y, sx * 0.3, afr + 0.04, ZA, 0.05, 'siva_oker', 'siva_kirmizi')

# ---------------------------------------------------------------- the stairs up the face, tier by tier
y.bolum('Merdivenler')
for k in range(1, len(kat)):
    hw_, hd_, za, zb, bw_, bd_ = kat[k]
    y_son = CY - bd_
    y_bas = y_son - (zb - za) * 0.86
    if k == 1:   # the lowest flight above the adosada: twin flights
        for sx in (-1, 1):
            alfarda_merdiven(y, sx * 0.1, y_bas, y_son, za, zb, 0.13, key='kirec', alf_key='tas_volkan_koyu', alf_en=0.026, dado=0.1, dado_h=0.018)
    else:
        alfarda_merdiven(y, 0.0, y_bas, y_son, za, zb, 0.2, key='kirec', alf_key='tas_volkan_koyu', alf_en=0.028, dado=0.1, dado_h=0.018)

# ---------------------------------------------------------------- the summit temple
y.bolum('Tapinak')
bw_, bd_, zt = teo_kademe((0, CY), 0.16, 0.16, ZT, 0.045, 0.012, disk='turkuaz')
alfarda_merdiven(y, 0.0, CY - bd_ - 0.045, CY - bd_, ZT, zt, 0.1, key='kirec', alf_key='kirec', alf_en=0.018, dado=0.15, dado_h=0.01)
ztop = teo_tapinak(0, CY + 0.02, 0.2, 0.17, zt, sancakli=True)
for sx in (-1, 1):
    mangal(y, sx * (TW - 0.03), CY - TW + 0.03, ZT, 0.045, 'siva_oker', 'siva_kirmizi')
kisi(y, -0.05, CY - bd_ - 0.06, ZT, -math.pi / 2, 0.045, 'koyu', 'koyu', kol='kalk', pelerin='siva_kirmizi', bas='boya_yesil')
kisi(y, 0.12, CY - bd_ - 0.03, ZT, -math.pi / 2 - 0.4, 0.045, 'koyu', 'koyu', kol='asa', pelerin='koyu')

# ---------------------------------------------------------------- the enclosure: a broad U-shaped platform on three sides
y.bolum('Cevre platformu')
U = [V(-1.17, -0.45), V(-0.93, -0.45), V(-0.93, 1.1), V(0.93, 1.1), V(0.93, -0.45), V(1.17, -0.45), V(1.17, 1.24), V(-1.17, 1.24)]
tb, ZU = kademe_kose(y, U, PZ, 0.075, 0.012, talud=0.38, key='kirec', bant_key='siva_kirmizi', ust_key='kirec', cerceve='kirec')
for sx in (-1, 1):
    cx = sx * 1.05
    # a stair up the front end of each arm, small temples and altars along its top
    alfarda_merdiven(y, cx, -0.45 - 0.07, -0.45 + 0.012, PZ, ZU, 0.12, key='kirec', alf_key='kirec', alf_en=0.02, dado=0.15, dado_h=0.01)
    teo_tapinak(cx, 0.2, 0.17, 0.15, ZU, kapi_yon=math.pi if sx > 0 else 0.0)
    teo_tapinak(cx, 0.75, 0.17, 0.15, ZU, kapi_yon=math.pi if sx > 0 else 0.0)
    for yy in (-0.2, 0.47, 1.0):
        mangal(y, cx, yy, ZU, 0.04, 'siva_oker', 'siva_kirmizi')
    # a stair down the inner face to the pyramid's court
    with parca(y, (sx * (0.93 + 0.012), 0.47, 0), -sx * math.pi / 2):
        alfarda_merdiven(y, 0.0, -0.07, 0.0, PZ, ZU, 0.14, key='kirec', alf_key='kirec', alf_en=0.02, dado=0.15, dado_h=0.01)
for xx in (-0.5, 0.5):
    teo_tapinak(xx, 1.17, 0.17, 0.11, ZU, kapi_yon=-math.pi / 2)

# ---------------------------------------------------------------- the platform temples flanking the plaza
y.bolum('Kucuk platformlar')
for sx in (-1, 1):
    cx, cy = sx * 0.9, -0.72
    bw_, bd_, z1p = teo_kademe((cx, cy), 0.22, 0.2, PZ, 0.075, 0.016)
    bw2, bd2, z2p = teo_kademe((cx, cy + 0.02), bw_ - 0.04, bd_ - 0.05, z1p, 0.065, 0.014, disk='turkuaz')
    alfarda_merdiven(y, cx, cy - bd_ - 0.11, cy - bd_, PZ, z1p, 0.14, key='kirec', alf_key='kirec', alf_en=0.022, dado=0.15, dado_h=0.012)
    alfarda_merdiven(y, cx, cy + 0.02 - bd2 - 0.07, cy + 0.02 - bd2, z1p, z2p, 0.1, key='kirec', alf_key='kirec', alf_en=0.02, dado=0.15, dado_h=0.01)
    teo_tapinak(cx, cy + 0.05, 0.2, 0.15, z2p, sancakli=(sx > 0))
    mangal(y, cx - sx * 0.17, cy - bd_ - 0.03, PZ, 0.045, 'siva_oker', 'siva_kirmizi')
y.bolum('Sunak')
for sx in (-1, 1):
    # stelae (the Teotihuacan ball-court markers) on the plaza
    xx = sx * 0.55
    donel(y, (xx, -0.9), [(0, PZ), (0.03, PZ), (0.03, PZ + 0.012), (0.012, PZ + 0.016), (0.012, PZ + 0.075), (0.02, PZ + 0.085), (0.018, PZ + 0.1),
                          (0.024, PZ + 0.11), (0.0, PZ + 0.12)], 'bazalt', n=12)

# ---------------------------------------------------------------- pilgrims
y.bolum('Insanlar')
for (px, py, a_, kol, ten, giysi) in ((-0.42, -1.12, 0.0, 'yan', 'kiremit', 'beyaz'), (-0.36, -1.1, 0.0, 'asa', 'kiremit', 'beyaz'),
                                      (0.28, -1.15, math.pi, 'yan', 'kiremit', 'siva_oker'), (0.33, -1.13, math.pi, 'one', 'kiremit', 'beyaz'),
                                      (0.06, -1.05, math.pi / 2, 'yan', 'kiremit', 'beyaz'), (-0.08, -0.92, math.pi / 2, 'kalk', 'koyu', 'koyu'),
                                      (0.2, -0.84, 2.0, 'yan', 'kiremit', 'beyaz')):
    kisi(y, px, py, PZ if py > -0.98 else Z0 + 0.0015, a_, 0.048, ten, giysi, kol=kol)
# climbers on the stairs
for k, t in ((2, 0.4), (3, 0.6), (4, 0.3)):
    hw_, hd_, za, zb, bw_, bd_ = kat[k]
    y_son = CY - bd_; y_bas = y_son - (zb - za) * 0.86
    kisi(y, 0.04 if k % 2 else -0.05, y_bas + (y_son - y_bas) * t, za + (zb - za) * t + 0.003, math.pi / 2, 0.048, 'kiremit', 'beyaz')

calistir(y, 'lm_gunespiramidi')
