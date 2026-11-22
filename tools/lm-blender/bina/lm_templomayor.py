# Büyük Tapınak (lm_templomayor): the Templo Mayor of Tenochtitlan (phase VI/VII): a four-tier talud pyramid with twin
# stairs on its west face, alfardas ending in dados and serpent heads at their feet; on top the red shrine of
# Huitzilopochtli (skull-studded roof, shell merlons) and the blue-white striped shrine of Tlaloc (chacmool in front);
# the platform with the Coyolxauhqui stone, braziers, a tzompantli, a temalacatl and the serpent wall of the precinct.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mexika_ortak import *

y = Yapi()
R = random.Random(11)
Z0 = 0.04                      # precinct floor

# ---------------------------------------------------------------- helpers
def cati_kabartma(a, b, s, t, n, fn):
    """call fn(point, normal) at (s along, t up) on the sloped roof face a (bottom edge) -> b (top edge)"""
    p = a[0].lerp(a[1], s).lerp(b[0].lerp(b[1], s), t)
    fn(p, n)


def kafa_kabartma(p, n, r=0.011):
    """a carved white skull on a face (normal n)"""
    kabartma(y, p, n, daire(r, 10, 0, r * 0.15) + [], 0.0, 0.0025, 'beyaz')
    kabartma(y, p, n, [(-r * 0.62, -r * 0.65), (r * 0.62, -r * 0.65), (r * 0.62, -r * 1.25), (-r * 0.62, -r * 1.25)], 0.0, 0.0025, 'beyaz')
    for sg in (-1, 1):
        kabartma(y, p, n, daire(r * 0.27, 6, sg * r * 0.4, r * 0.05), 0.0, 0.0032, 'koyu')
    kabartma(y, p, n, [(-r * 0.12, -r * 0.35), (r * 0.12, -r * 0.35), (0, -r * 0.1)], 0.0, 0.0032, 'koyu')


def disk_kabartma(p, n, r=0.012, key='lacivert', kenar='beyaz'):
    kabartma(y, p, n, daire(r * 1.35, 12), 0.0, 0.002, kenar)
    kabartma(y, p, n, daire(r, 12), 0.0, 0.0035, key)


def chacmool(x, yy, z, aci, s=0.1):
    """a reclining chacmool: knees drawn up, propped on its elbows, head turned to the front, a bowl on its belly"""
    with parca(y, (x, yy, z), aci, s):
        kutu_merkez(y, (0, 0), 1.0, 0.5, 0.12, 'bazalt')
        b = 0.12
        cubuk(y, V(-0.3, 0, b + 0.18), V(0.05, 0, b + 0.1), 0.26, 'kirec', 0.18)          # torso, leaning back
        for sg in (-1, 1):
            cubuk(y, V(0.05, sg * 0.1, b + 0.1), V(0.22, sg * 0.1, b + 0.32), 0.1, 'kirec')  # thighs up
            cubuk(y, V(0.22, sg * 0.1, b + 0.32), V(0.4, sg * 0.1, b + 0.02), 0.09, 'kirec')  # shins down
            kutu_merkez(y, (0.43, sg * 0.1), 0.12, 0.08, 0.05, 'kirec', z0=b)                 # feet
            cubuk(y, V(-0.28, sg * 0.15, b + 0.24), V(-0.3, sg * 0.17, b + 0.02), 0.07, 'kirec')   # arms to the elbows
        kure(y, (-0.38, 0.0, b + 0.34), 0.13, 'kirec', n=8, kat=4)                            # head
        kutu_merkez(y, (-0.4, 0), 0.08, 0.3, 0.1, 'boya_kirmizi', z0=b + 0.38)                # headband
        donel(y, (-0.08, 0), [(0.0, b + 0.2), (0.12, b + 0.2), (0.14, b + 0.27), (0.1, b + 0.27), (0.0, b + 0.24)], 'boya_kirmizi', n=10)   # the bowl
        for sg in (-1, 1):
            kure(y, (-0.28, sg * 0.1, b + 0.37), 0.03, 'koyu', n=5, kat=3)


def techcatl(x, yy, z):
    kesik(y, (x, yy), 0.05, 0.035, 0.022, 0.02, z, z + 0.035, 'bazalt')


def tapinak(cx, cy, w, d, z, tur):
    """a shrine on the summit: a plinth, white walls with a dark doorway facing -y, a painted frieze, an overhanging
    slab, a tall battered roof (Huitzilopochtli: red with carved skulls; Tlaloc: blue-white stripes and discs) and a
    crest of merlons. Returns the top z"""
    vurgu = 'boya_kirmizi' if tur == 'huitzilopochtli' else 'turkuaz'
    # plinth with a short stair
    kutu_merkez(y, (cx, cy), w + 0.05, d + 0.05, 0.025, 'kirec', z0=z)
    silme(y, dikdortgen(cx - (w + 0.05) / 2, cx + (w + 0.05) / 2, cy - (d + 0.05) / 2, cy + (d + 0.05) / 2), z + 0.019, 0.006, 0.003, vurgu)
    for k in range(3):
        kutu(y, V(cx - 0.06, cy - (d + 0.05) / 2 - 0.012 * (3 - k), z), X, 0.12, 0.012 * (3 - k) + 0.001, 0.025 * (k + 1) / 3.5, 'kirec', 'onsagsolust')
    zw = z + 0.025; H = 0.15
    kose = dikdortgen(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2)
    dikdortgen_kapi(y, kose[0], kose[1], zw, H, 0.32, 0.68, 0.112, 'siva', 'koyu', cerceve=(0.012, vurgu), derin=0.03)
    for i in (1, 2, 3):
        duz_duvar(y, kose[i], kose[(i + 1) % 4], zw, zw + H, 'siva')
    silme(y, kose, zw, 0.022, 0.003, vurgu)                                    # painted dado
    # the frieze under the slab: a painted band with discs (Tlaloc) or carved skulls (Huitzilopochtli)
    fz = zw + H - 0.034
    silme(y, kose, fz, 0.03, 0.002, vurgu if tur == 'huitzilopochtli' else 'lacivert')
    for i in range(4):
        a, b = kose[i], kose[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
        m = int(L / 0.04)
        for k in range(m):
            p = a.lerp(b, (k + 0.5) / m) + nn * 0.002 + Z * (fz + 0.015)
            if tur == 'huitzilopochtli': kafa_kabartma(p, nn, 0.008)
            else: disk_kabartma(p, nn, 0.0065, 'turkuaz', 'beyaz')
    # slab
    zs = zw + H
    kutu_merkez(y, (cx, cy), w + 0.035, d + 0.035, 0.016, 'kirec', z0=zs)
    # tall roof
    z0r, z1r = zs + 0.016, zs + 0.016 + 0.23
    w0, d0, w1, d1 = w + 0.02, d + 0.02, w - 0.02, d - 0.03
    if tur == 'huitzilopochtli':
        A, B = kesik(y, (cx, cy), w0, d0, w1, d1, z0r, z1r, 'boya_kirmizi')
    else:
        A, B = kesik(y, (cx, cy), w0, d0, w1, d1, z0r, z1r, ['turkuaz', 'beyaz'], n_dilim=11, ust_key='beyaz')
    for i in range(4):
        j = (i + 1) % 4
        a, b = (A[i], A[j]), (B[i], B[j])
        e = (A[j] - A[i]).normalized(); nn = V(e.y, -e.x)
        # the face normal: across the face's bottom edge and up its slope
        up = (B[i].lerp(B[j], 0.5) - A[i].lerp(A[j], 0.5)).normalized()
        n = e.cross(up).normalized()
        if n.dot(nn) < 0: n = -n
        L = (A[j] - A[i]).length
        if tur == 'huitzilopochtli':
            m = int(L / 0.042)
            for row, t in enumerate((0.22, 0.5, 0.78)):
                for k in range(m - (row % 2)):
                    s = (k + 0.5 + 0.5 * (row % 2)) / m
                    cati_kabartma(a, b, s, t, n, lambda p, n_: kafa_kabartma(p + n_ * 0.0005, n_, 0.0105))
        else:
            m = int(L / 0.05)
            for k in range(m):
                s = (k + 0.5) / m
                cati_kabartma(a, b, s, 0.3, n, lambda p, n_: disk_kabartma(p + n_ * 0.0006, n_, 0.011, 'lacivert', 'beyaz'))
    # a thin cornice on the roof's top and the crest
    ust = dikdortgen(cx - w1 / 2, cx + w1 / 2, cy - d1 / 2, cy + d1 / 2)
    silme(y, ust, z1r - 0.008, 0.008, 0.004, 'kirec')
    ic = disa(ust, -0.006)
    if tur == 'huitzilopochtli':
        almena_halka(y, ic, z1r, 0.055, 0.009, 'beyaz', en=0.038, bosluk=0.012, bicim=SALYANGOZ)
    else:
        almena_halka(y, ic, z1r, 0.055, 0.009, 'siva', en=0.04, bosluk=0.012)
    return z1r + 0.055


# ---------------------------------------------------------------- ground
y.bolum('Kutsal alan')
zemin(y, -1.2, 1.2, -1.2, 1.18, Z0, 'tas_koyu', 'zemin', basamak=(), silmeli=True)
# a painted processional way from the front to the platform stair
y.yuz_yon([V(-0.26, -1.2, Z0 + 0.0015), V(0.26, -1.2, Z0 + 0.0015), V(0.26, -0.87, Z0 + 0.0015), V(-0.26, -0.87, Z0 + 0.0015)], 'kirec', Z)
for k in range(6):
    yy0 = -1.18 + k * 0.055
    for sx in (-1, 1):
        y.yuz_yon([V(sx * 0.25, yy0, Z0 + 0.0025), V(sx * 0.21, yy0, Z0 + 0.0025), V(sx * 0.21, yy0 + 0.03, Z0 + 0.0025), V(sx * 0.25, yy0 + 0.03, Z0 + 0.0025)],
                  'boya_kirmizi', Z)

# ---------------------------------------------------------------- platform
y.bolum('Platform')
PC = (0.0, 0.13)
bw, bd, ZP = kademe(y, PC, 0.95, 0.91, Z0, 0.075, 0.022, talud=0.5, key='siva', bant_key='siva', ust_key='zemin', cizgi='boya_kirmizi')
PF = PC[1] - bd                                     # the platform's front edge
ayak = alfarda_merdiven(y, 0.0, PF - 0.1, PF, Z0, ZP, 0.56, n=5, key='kirec', alf_key='siva', alf_en=0.04, dado=0.2, dado_h=0.015)
for p in ayak:
    yilan_basi(y, (p.x, p.y + 0.012 - 0.055, Z0), -math.pi / 2, 0.075, 'kirec')
# serpent heads at the platform's front corners and bodies undulating along its band
for sx in (-1, 1):
    yilan_basi(y, (sx * (bw - 0.02), PF - 0.045, Z0), -math.pi / 2, 0.08, 'kirec', tuy='boya_yesil')
for sx in (-1, 1):
    pts = []
    for k in range(25):
        t = k / 24
        xx = sx * (0.33 + t * (bw - 0.42))
        pts.append(V(xx, PF - 0.006, Z0 + 0.052 + 0.012 * math.sin(t * TAU * 2.5)))
    boru(y, pts, 0.009, 'turkuaz', n=6)
    for k in range(0, 24, 3):
        p = pts[k].lerp(pts[k + 1], 0.5)
        kure(y, (p.x, p.y - 0.004, p.z), 0.0065, 'boya_sari', n=6, kat=3)

# ---------------------------------------------------------------- the pyramid
y.bolum('Piramit')
CY = 0.36
hw, hd = 0.78, 0.62
z = ZP
TH = 0.17
bantlar = []
for k in range(4):
    bw_, bd_, z1 = kademe(y, (0, CY), hw, hd, z, TH, 0.082, talud=0.74, key='tas', bant_key='siva', ust_key='zemin' if k < 3 else 'kirec',
                          cizgi='boya_kirmizi')
    bantlar.append((bw_, bd_, z + TH * 0.74, z1))
    hw, hd = bw_ - 0.016, bd_ - 0.016
    z = z1
ZT = z                                               # the summit
TOPW, TOPD = bantlar[-1][0], bantlar[-1][1]
# discs on the bands: turquoise on Tlaloc's (north, -x) half, red on Huitzilopochtli's
for bw_, bd_, zm, z1 in bantlar:
    bant_diskleri(y, (0, CY), bw_, bd_, (zm + z1) / 2 - 0.004, 0.0105, 0.075, lambda p: 'turkuaz' if p.x < 0 else 'boya_kirmizi', 'beyaz',
                  atla=lambda p: abs(p.x) < 0.42 and p.y < CY)
# a painted line down the middle of the front (the two halves)
# serpent heads jutting from the front corners of every tier's band (turquoise-scaled on Tlaloc's half, red on Huitzilopochtli's)
for bw_, bd_, zm, z1 in bantlar:
    for sx in (-1, 1):
        d_ = V(sx, -1).normalized()
        c_ = V(sx * bw_, CY - bd_) + d_ * 0.016
        yilan_basi(y, (c_.x, c_.y, zm - 0.004), math.atan2(d_.y, d_.x), 0.052, 'kirec', pul='turkuaz' if sx < 0 else 'boya_kirmizi')
# the twin stairs
y.bolum('Ikiz merdiven')
YB = CY - 0.62 - 0.29
YS = CY - TOPD
for sx in (-1, 1):
    ayak = alfarda_merdiven(y, sx * 0.195, YB, YS, ZP, ZT, 0.3, key='kirec', alf_key='siva', alf_en=0.045, dado=0.13, dado_h=0.05,
                            basamak_key='siva')
    for p in ayak:
        xx = (0.047 if p.x > 0 else -0.047) if abs(p.x) < 0.1 else p.x
        yilan_basi(y, (xx, p.y + 0.012 - 0.06, ZP), -math.pi / 2, 0.105, 'kirec', tuy='boya_yesil' if sx < 0 else None)
# the dados' painted faces
RUN = YS - YB
YD = YS - RUN * 0.13
P1 = V(0, YD, ZP + (ZT - ZP) * (YD - YB) / RUN + 0.026); P2 = V(0, YD + RUN * 0.13 * 0.3, ZT + 0.05)
dd = (P2 - P1); nd = V(0, -dd.z, dd.y).normalized()
for xx in (-0.3675, -0.0225, 0.0225, 0.3675):
    m_ = (P1 + P2) / 2 + V(xx, 0, 0)
    L_ = dd.length
    kabartma(y, m_, nd, [(-0.017, -L_ * 0.36), (0.017, -L_ * 0.36), (0.017, L_ * 0.36), (-0.017, L_ * 0.36)], 0.0, 0.0015,
             'turkuaz' if xx < 0 else 'boya_kirmizi', u=X)
    kabartma(y, m_, nd, daire(0.009, 10), 0.0, 0.0025, 'beyaz', u=X)

# ---------------------------------------------------------------- the twin shrines
y.bolum('Tapinaklar')
SW, SD = 0.36, 0.3
SCY = CY + 0.04
zt_h = tapinak(0.215, SCY, SW, SD, ZT, 'huitzilopochtli')
zt_t = tapinak(-0.215, SCY, SW, SD, ZT, 'tlaloc')
chacmool(-0.215, SCY - SD / 2 - 0.085, ZT, 0.0, 0.085)
techcatl(0.215, SCY - SD / 2 - 0.075, ZT)
for sx in (-1, 1):
    mangal(y, sx * (TOPW - 0.035), CY - TOPD + 0.04, ZT, 0.05, 'siva_oker', 'boya_kirmizi')
sancak(y, -TOPW + 0.03, CY + TOPD - 0.04, ZT, boy=0.24, en=0.11, yuk=0.07, aci=0.4)
sancak(y, TOPW - 0.03, CY + TOPD - 0.04, ZT, boy=0.24, en=0.11, yuk=0.07, aci=0.4)
# priests on the summit and on the stairs
kisi(y, 0.12, SCY - SD / 2 - 0.08, ZT, -math.pi / 2, 0.045, 'koyu', 'koyu', kol='kalk', pelerin='boya_kirmizi')
kisi(y, 0.30, SCY - SD / 2 - 0.08, ZT, -math.pi / 2 - 0.3, 0.045, 'koyu', 'koyu', kol='one', pelerin='koyu')
kisi(y, -0.11, SCY - SD / 2 - 0.06, ZT, -math.pi / 2 + 0.4, 0.045, 'koyu', 'koyu', kol='asa', pelerin='lacivert')
for (sx, t, a_) in ((-1, 0.35, math.pi / 2), (1, 0.6, math.pi / 2), (-1, 0.75, -math.pi / 2)):
    yy = YB + (YS - YB) * t
    kisi(y, sx * (0.195 + 0.05 * (1 if t > 0.5 else -1)), yy, ZP + (ZT - ZP) * t + 0.002, a_, 0.045, 'kiremit', 'beyaz', kol='yan', bas='boya_yesil' if t > 0.5 else None)

# ---------------------------------------------------------------- the Coyolxauhqui stone at the foot of Huitzilopochtli's stair
y.bolum('Coyolxauhqui')
CC = V(0.2, (PF + YB) / 2 - 0.005, ZP)
RC = 0.082
halka_disk(y, CC, Z, 0.0, RC, 0.0, 0.012, 'kirec', m=28)
silme(y, cokgen(CC, RC, 28), ZP + 0.009, 0.003, 0.003, 'boya_kirmizi')
def cy_parca(uv, key, d=0.016):
    kabartma(y, CC, Z, uv, 0.012, d, key)
# torso, head with its headdress, the severed arms and legs, bells on the cheeks, a skull at the belt
cy_parca([(-0.02, -0.025), (0.022, -0.028), (0.026, 0.018), (-0.024, 0.02)], 'siva_oker')
cy_parca(daire(0.018, 10, -0.004, 0.036), 'siva_oker')
cy_parca([(-0.024, 0.05), (0.018, 0.05), (0.028, 0.068), (-0.03, 0.066)], 'turkuaz', 0.018)
cy_parca(daire(0.006, 8, 0.012, 0.034), 'turkuaz', 0.019)
cy_parca(daire(0.007, 8, 0.0, -0.016), 'beyaz', 0.018)
for (a0, a1, w_) in (((-0.026, 0.008), (-0.055, 0.03), 0.011), ((0.028, 0.0), (0.05, -0.012), 0.011), ((-0.016, -0.028), (-0.04, -0.06), 0.012),
                     ((0.016, -0.03), (0.046, -0.05), 0.012)):
    # each limb cut off at the joint (a gap, a red cut) and bent at the knee / elbow
    m = ((a0[0] + a1[0]) / 2 + (0.006 if a1[1] > a0[1] else -0.006), (a0[1] + a1[1]) / 2 + 0.006)
    for p, q in ((a0, m), (m, a1)):
        ex, ey = q[0] - p[0], q[1] - p[1]; L = math.hypot(ex, ey); nx, ny = -ey / L * w_ / 2, ex / L * w_ / 2
        dx, dy = ex / L * 0.006, ey / L * 0.006
        p2 = (p[0] + dx, p[1] + dy) if p is a0 else p
        cy_parca([(p2[0] + nx, p2[1] + ny), (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny), (p2[0] - nx, p2[1] - ny)], 'siva_oker')
    cy_parca(daire(w_ * 0.45, 8, a0[0] + (a1[0] - a0[0]) * 0.08, a0[1] + (a1[1] - a0[1]) * 0.08), 'boya_kirmizi', 0.0175)
    cy_parca(daire(w_ * 0.55, 8, a1[0], a1[1]), 'kirec', 0.0175)
# braziers flanking the stairs on the platform
for sx in (-1, 1):
    mangal(y, sx * 0.47, YB + 0.03, ZP, 0.06, 'siva_oker', 'boya_kirmizi')
    mangal(y, sx * 0.66, PF + 0.05, ZP, 0.05, 'siva_oker', 'turkuaz')
# a chacmool and a cuauhxicalli on the Tlaloc side of the platform foot
donel(y, (-0.21, CC.y), [(0.0, ZP), (0.045, ZP), (0.05, ZP + 0.012), (0.04, ZP + 0.03), (0.035, ZP + 0.03), (0.0, ZP + 0.022)], 'bazalt', n=16)
halka_disk(y, V(-0.21, CC.y, ZP + 0.03), Z, 0.022, 0.034, 0.0, 0.0008, 'boya_kirmizi', m=16)
for k in range(8):
    t = TAU * k / 8
    kabartma(y, V(-0.21 + 0.0505 * math.cos(t) * 0.94, CC.y + 0.0505 * math.sin(t) * 0.94, ZP + 0.018), V(math.cos(t), math.sin(t), 0.08),
             daire(0.005, 8), 0.0, 0.002, 'turkuaz')

# ---------------------------------------------------------------- tzompantli
y.bolum('Tzompantli')
tzompantli(y, -0.73, -1.03, Z0, 0.56, 0.0, satir=4, adim=0.021, h=0.13)
for xx in (-1.06, -0.4):
    mangal(y, xx, -1.03, Z0, 0.05, 'siva_oker', 'boya_kirmizi')

# ---------------------------------------------------------------- temalacatl (the round gladiatorial stone) on a low platform
y.bolum('Temalacatl')
TX, TY = 0.72, -1.02
kademe(y, (TX, TY), 0.17, 0.14, Z0, 0.045, 0.012, talud=0.5, key='siva', ust_key='kirec', cizgi='boya_kirmizi')
for k in range(3):
    kutu(y, V(TX - 0.06, TY - 0.14 - 0.012 * (3 - k), Z0), X, 0.12, 0.012 * (3 - k) + 0.001, 0.045 * (k + 1) / 3.5, 'kirec', 'onsagsolust')
ZTm = Z0 + 0.045
donel(y, (TX, TY + 0.01), [(0, ZTm), (0.075, ZTm), (0.075, ZTm + 0.028), (0, ZTm + 0.028)], 'bazalt', n=24)
halka_disk(y, V(TX, TY + 0.01, ZTm + 0.028), Z, 0.035, 0.068, 0, 0.003, 'kirec', m=24)
for k in range(12):
    t = TAU * k / 12
    kabartma(y, V(TX + 0.0515 * math.cos(t), TY + 0.01 + 0.0515 * math.sin(t), ZTm + 0.031), Z, daire(0.007, 6), 0, 0.002, 'boya_kirmizi' if k % 2 else 'turkuaz')
halka_disk(y, V(TX, TY + 0.01, ZTm + 0.028), Z, 0.0, 0.012, 0, 0.002, 'koyu', m=10)
kisi(y, TX - 0.02, TY + 0.0, ZTm + 0.028, -math.pi / 2 + 0.5, 0.045, 'kiremit', 'beyaz', kol='kalk', bas='boya_sari')
kisi(y, TX + 0.04, TY + 0.03, ZTm + 0.028, math.pi + 0.3, 0.045, 'boya_sari', 'boya_sari', kol='one', bas='boya_yesil')
for xx in (TX - 0.2, TX + 0.2):
    mangal(y, xx, TY - 0.08, Z0, 0.05, 'siva_oker', 'boya_kirmizi')

# ---------------------------------------------------------------- coatepantli: the serpent wall round the back of the precinct
y.bolum('Yilan duvari')
WH = 0.075
yol = [V(-1.14, -0.2), V(-1.14, 1.12), V(1.14, 1.12), V(1.14, -0.2)]
for i in range(3):
    a, b = yol[i], yol[i + 1]
    e = (b - a).normalized(); nn = V(e.y, -e.x)   # (nn: outward, to the right of travel ... inward here: walk is CW)
    # the wall: a box along a->b, 0.03 thick
    kutu(y, a - nn * 0.0 + V(0, 0, Z0), e, (b - a).length, -0.03, WH, 'siva', 'onarkasagsolust')
for i in range(3):
    a, b = yol[i], yol[i + 1]
    e = (b - a).normalized()
    nin = V(e.y, -e.x)     # into the precinct (the walk is clockwise)
    nout = -nin
    almenalar(y, a + nin * 0.023, b + nin * 0.023, Z0 + WH, 0.035, 0.016, 'siva', en=0.03, bosluk=0.012)
    # inside: turquoise discs; outside: serpent heads
    L = (b - a).length
    m = int(L / 0.12)
    for k in range(m):
        p = a.lerp(b, (k + 0.5) / m)
        disk_kabartma(V(p.x, p.y, Z0 + WH * 0.55) + nin * 0.0302, nin, 0.01, 'turkuaz', 'beyaz')
        if k % 3 == 1:
            yilan_basi(y, (p.x + nout.x * 0.0, p.y + nout.y * 0.0, Z0 + 0.012), math.atan2(nout.y, nout.x), 0.05, 'kirec')
# end caps of the wall runs at the front
for xx in (-1.14, 1.14):
    kutu_merkez(y, (xx - (0.015 if xx < 0 else -0.015), -0.2), 0.05, 0.05, WH + 0.04, 'siva', z0=Z0)
    mangal(y, xx - (0.015 if xx < 0 else -0.015), -0.2, Z0 + WH + 0.04, 0.045, 'siva_oker', 'boya_kirmizi')

calistir(y, 'lm_templomayor')
