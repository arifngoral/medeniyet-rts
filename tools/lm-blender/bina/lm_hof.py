# Hof Tapınağı (lm_hof): a Norse temple hall after the Uppåkra cult house and the stave churches it foreshadows: a tall
# plank hall ringed by an arcaded gallery under a shingled lean-to roof, a steep shingled gable roof with crossed boards
# and dragon heads, a central lantern tower with a skirt roof, gabled spire and gilded vane, a carved portal porch and the
# gold chain round the eaves; before it the hörgr (stone altar with a fire and a bronze bowl), three idol posts, the
# sacred ash, a rune stone, a holy well and a ring of standing stones marking the vé.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from viking_parca import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.045                       # ground top
TC = V(0.0, 0.25)                 # temple centre
ZP = Z0 + 0.04                   # temple floor (stone plinth)
HX, HY, HH = 0.28, 0.4, 0.36     # hall half sizes, wall height
GX, GY, GH = 0.42, 0.54, 0.15    # gallery half sizes, wall height
SH = ['sindira', 'sindira2']     # shingle courses

y.bolum('Zemin: kutsal alan')
zemin(y, -1.1, 1.1, -1.02, 0.98, Z0, 'granit', 'cimen', basamak=(), silmeli=False)
tas_yer = lambda pts, k='zemin': y.yuz_yon([V(p[0], p[1], Z0 + 0.002) for p in pts], k, Z)
tas_yer([(-0.09, -0.98), (0.09, -0.98), (0.09, TC.y - GY - 0.12), (-0.09, TC.y - GY - 0.12)])
tas_yer([(0.26, -0.94), (0.86, -0.94), (0.86, -0.5), (0.26, -0.5)], 'toprak')

# ---------------- plinth ----------------
y.bolum('Taş kaide')
with parca(y, (TC.x, TC.y, 0)):
    zemin(y, -GX - 0.06, GX + 0.06, -GY - 0.17, GY + 0.06, ZP, 'granit', 'zemin', basamak=(('on', 0.34),), n_basamak=3)
    # the steps start on the ground: zemin builds from 0, so lift nothing; the plinth reaches the ground (Z0 under it)

# ---------------- hall ----------------
y.bolum('Salon duvarları')
with parca(y, (TC.x, TC.y, 0)):
    hall = dikdortgen(-HX, HX, -HY, HY)
    duvarlar(y, hall, ZP, ZP + HH, 'ahsap_dikey')
    # a carved band and small round windows high up (above the gallery roof)
    silme(y, hall, ZP + HH - 0.035, 0.022, 0.006, 'boya_kirmizi', 'duz')
    silme(y, hall, ZP + HH - 0.012, 0.012, 0.01, 'ahsap_koyu', 'duz')
    for i in range(4):
        a, b = hall[i], hall[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        m = int((b - a).length / 0.16)
        for k in range(m):
            o = a.lerp(b, (k + 0.5) / m) + Z * (ZP + HH - 0.075)
            y.oculus(o, e, nn, 0.016, 'koyu', 'ahsap_koyu', f=0.006, k=10)

y.bolum('Salon çatısı ve ejder başları')
with parca(y, (TC.x, TC.y, 0)):
    zh = ZP + HH
    RH = 0.58
    zr = cati_besik(y, -HX, HX, -HY, HY, zh, RH, 0.035, 'ahsap_koyu', 'ahsap', kalinlik=0.014, alt_key='ahsap_koyu',
                    ucluk_key='ahsap_dikey', uc_sacak=0.045, nr=24, ns=10, dilim=SH, mahya_en=0.016)
    # crossed barge boards running into dragon heads at both gables
    for sy in (-1, 1):
        ye = sy * (HY + 0.045 + 0.006)
        b = HX + 0.035
        top = V(0, ye, zr - 0.004)
        for sx in (-1, 1):
            # wide carved barge boards (vindskier) down the whole verge, a red painted edge and gilt studs on them,
            # crossing over the apex into the dragon heads
            p0 = V(sx * b * 0.99, ye, zh + RH * 0.01 + 0.014)
            tp = V(0, ye, zh + RH + 0.014)
            d = (tp - p0).normalized()
            p2 = tp + d * 0.07
            cubuk(y, p0, p2, 0.034, 'ahsap_koyu', 0.012)
            cubuk(y, p0 + V(0, sy * 0.0075, -0.006), p2 + V(0, sy * 0.0075, -0.006), 0.01, 'boya_kirmizi', 0.004)
            m = 9
            for k in range(1, m):
                kure(y, p0.lerp(tp, k / m) + V(0, sy * 0.0075, 0.009), 0.0045, 'altin', n=6, kat=3)
            ejder(y, p2 - d * 0.004, V(-sx, 0), 0.15, 'ahsap_koyu')
        # a carved sun disc and a band of round windows on the gable
        o = V(0, sy * (HY + 0.003), zh + RH * 0.42)
        y.oculus(o, V(-sy, 0), V(0, sy), 0.04, 'boya_kirmizi', 'altin', f=0.01, k=14)
        y.oculus(o + V(0, sy * 0.002, 0), V(-sy, 0), V(0, sy), 0.018, 'altin', 'ahsap_koyu', f=0.006, k=10)
        cubuk(y, V(-HX, sy * (HY + 0.006), zh + 0.008), V(HX, sy * (HY + 0.006), zh + 0.008), 0.016, 'boya_kirmizi', 0.008)
        for k in (-1, 1):
            y.oculus(V(k * 0.1, sy * (HY + 0.003), zh + RH * 0.17), V(-sy, 0), V(0, sy), 0.014, 'koyu', 'ahsap_koyu', f=0.005, k=10)
    # an openwork ridge crest (stave church mønekam): a rail on pickets, every third picket a little cross
    for s2 in (-1, 1):
        ya_, yb_ = s2 * 0.15, s2 * (HY + 0.04)
        n_ = 9
        cubuk(y, V(0, ya_, zr + 0.034), V(0, yb_, zr + 0.034), 0.008, 'ahsap_koyu', 0.008)
        for k in range(n_ + 1):
            yy = ya_ + (yb_ - ya_) * k / n_
            h_ = 0.05 if k % 3 == 0 else 0.038
            cubuk(y, V(0, yy, zr - 0.004), V(0, yy, zr + h_), 0.006, 'ahsap_koyu', 0.006)
            if k % 3 == 0:
                cubuk(y, V(0, yy - 0.012, zr + h_ - 0.012), V(0, yy + 0.012, zr + h_ - 0.012), 0.006, 'altin', 0.005)
    # the gold chain hanging in swags under the eaves (Adam of Bremen)
    ze = zh - 0.02
    yol = []
    kose = [V(-HX - 0.03, -HY - 0.04), V(HX + 0.03, -HY - 0.04), V(HX + 0.03, HY + 0.04), V(-HX - 0.03, HY + 0.04)]
    for i in range(4):
        a, b = kose[i], kose[(i + 1) % 4]
        m = int((b - a).length / 0.11)
        for k in range(m):
            for t in (0.0, 0.25, 0.5, 0.75):
                u = (k + t) / m
                yol.append(a.lerp(b, u) + Z * (ze - 0.025 * math.sin(math.pi * t)))
    yol.append(yol[0])
    boru(y, yol, 0.0032, 'altin', n=4, kapat=False)

# ---------------- gallery ----------------
y.bolum('Revaklı galeri')
with parca(y, (TC.x, TC.y, 0)):
    RENK = ('ahsap_dikey', 'ahsap_koyu', 'ahsap', 'koyu')
    PW = 0.11                       # half width of the porch
    segs = [((-GX, -GY), (-PW, -GY), 2), ((PW, -GY), (GX, -GY), 2), ((GX, -GY), (GX, GY), 7), ((GX, GY), (-GX, GY), 5), ((-GX, GY), (-GX, -GY), 7)]
    for a, b, n in segs:
        pencereli_duvar(y, [V(*a), V(*b)], ZP, GH, [n], kapali=False, renk=RENK, v0=0.035, en=0.56, ust=0.025, derin=0.02,
                        sivri=0.0, cerceve=(0.006, ['boya_kirmizi', 'ahsap']), k_say=8)
    # posts at the corners and a sill beam
    for (cx_, cy_) in ((-GX, -GY), (GX, -GY), (GX, GY), (-GX, GY)):
        kutu_merkez(y, (cx_, cy_), 0.026, 0.026, GH + 0.01, 'ahsap_koyu', z0=ZP)
    silme(y, dikdortgen(-GX, GX, -GY, GY), ZP, 0.02, 0.008, 'ahsap_koyu', 'duz')
    # the lean-to roof round the hall (a hipped ring stopping at the hall walls)
    sac = 0.04
    rs = (GY - HY + sac) / (min(GX, GY) + sac)
    ring_h = 0.1 / rs
    cati_kirma(y, -GX, GX, -GY, GY, ZP + GH, ring_h, sac, 'ahsap_koyu', 'ahsap', kalinlik=0.012, r_ust=rs, nr=10, ns=12, dilim=SH)
    # small dragon heads on the four hip corners
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = V(sx * (GX + sac), sy * (GY + sac), ZP + GH + 0.004)
            ejder(y, p, V(sx, sy), 0.07, 'ahsap_koyu')

# ---------------- portal porch ----------------
y.bolum('Oymalı kapı sundurması')
with parca(y, (TC.x, TC.y, 0)):
    PD = 0.12                        # porch depth beyond the gallery
    PH = 0.2
    y0_, y1_ = -GY - PD, -GY + 0.02
    duz_duvar(y, V(PW, y0_), V(PW, y1_), ZP, ZP + PH, 'ahsap_dikey')
    duz_duvar(y, V(-PW, y1_), V(-PW, y0_), ZP, ZP + PH, 'ahsap_dikey')
    kapi(y, V(-PW, y0_), V(PW, y0_), ZP, 0.56, PH, ('ahsap_dikey', 'ahsap_koyu', 'ahsap', 'ahsap_koyu'), sivri=0.0, derin=0.025,
         cerceve=(0.014, ['boya_kirmizi', 'altin']), k_say=10)
    # carved jamb planks with a twisting beast band, iron strap hinges on the doors
    for sx in (-1, 1):
        x = sx * 0.075
        kutu(y, V(x - 0.014, y0_ - 0.006, ZP), X, 0.028, 0.006, PH * 0.66, 'ahsap', 'onsagsolust')
        for k in range(6):
            zz = ZP + 0.012 + k * PH * 0.105
            kutu(y, V(x - 0.011, y0_ - 0.0075, zz), X, 0.022, 0.0015, 0.012, 'boya_kirmizi' if k % 2 else 'altin', 'on')
    for zz in (0.05, 0.11):
        kutu(y, V(-0.05, y0_ + 0.022, ZP + zz), X, 0.1, 0.002, 0.007, 'demir', 'on')
    kutu_merkez(y, (0, y0_ + 0.02), 0.008, 0.004, 0.012, 'altin', z0=ZP + 0.08)
    silme(y, dikdortgen(-PW, PW, y0_, y1_), ZP, 0.02, 0.008, 'ahsap_koyu', 'duz')
    zp = cati_besik(y, -PW, PW, y0_, y1_ + 0.1, ZP + PH, 0.165, 0.025, 'ahsap_koyu', 'ahsap', kalinlik=0.012, ucluk_key='ahsap_dikey',
                    uc_sacak=0.03, nr=6, ns=4, dilim=SH)
    top = V(0, y0_ - 0.036, zp - 0.004)
    for sx in (-1, 1):
        p0 = V(sx * (PW + 0.02) * 0.55, y0_ - 0.036, ZP + PH + 0.09)
        d = (top - p0).normalized()
        cubuk(y, p0, top + d * 0.045, 0.018, 'ahsap_koyu', 0.009)
        ejder(y, top + d * 0.042, V(-sx, -0.3), 0.09, 'ahsap_koyu')
    o = V(0, y0_ - 0.003, ZP + PH + 0.07)
    y.oculus(o, X, -Y, 0.026, 'altin', 'boya_kirmizi', f=0.008, k=12)

# ---------------- lantern tower and spire ----------------
y.bolum('Kule, eteklik çatı ve sivri külah')
with parca(y, (TC.x, TC.y, 0)):
    TW = 0.12
    zt0 = zr - RH * (TW + 0.02) / (HX + 0.035) - 0.01   # (down to where the slopes meet the tower walls)
    zt1 = zr + 0.07
    duvarlar(y, dikdortgen(-TW, TW, -TW, TW), zt0, zt1, 'ahsap_dikey')
    silme(y, dikdortgen(-TW, TW, -TW, TW), zt1 - 0.014, 0.014, 0.006, 'boya_kirmizi', 'duz')
    # corner staves and a pair of round lights on every face of the tower
    for sx in (-1, 1):
        for sy in (-1, 1):
            kutu_merkez(y, (sx * TW, sy * TW), 0.022, 0.022, zt1 - zt0 - 0.014, 'ahsap_koyu', z0=zt0)
    tw_ = dikdortgen(-TW, TW, -TW, TW)
    for i in range(4):
        a, b = tw_[i], tw_[(i + 1) % 4]
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        for u in (0.3, 0.7):
            y.oculus(a.lerp(b, u) + nn * 0.002 + Z * (zr + 0.02), e, nn, 0.017, 'koyu', 'boya_kirmizi', f=0.005, k=10)
    # skirt roof
    sk = 0.05
    rs2 = sk / (TW + sk + 0.03)
    cati_kirma(y, -TW - sk, TW + sk, -TW - sk, TW + sk, zt1, 0.05 / ((sk + 0.03) / (TW + sk + 0.03)),
               0.03, 'ahsap_koyu', 'ahsap', kalinlik=0.01, r_ust=(sk + 0.03) / (TW + sk + 0.03), nr=3, ns=6, dilim=SH)
    # the open lantern with an arcade on every side
    LW = 0.095
    zl0, zl1 = zt1 + 0.045, zt1 + 0.19
    y.yuz_yon([V(p.x, p.y, zt1 + 0.049) for p in dikdortgen(-TW, TW, -TW, TW)], 'sindira2', Z)
    duvarlar(y, dikdortgen(-LW - 0.004, LW + 0.004, -LW - 0.004, LW + 0.004), zt1 + 0.049, zl0, 'ahsap_dikey')
    pencereli_duvar(y, dikdortgen(-LW, LW, -LW, LW), zl0, zl1 - zl0, [2, 2, 2, 2], renk=('ahsap_dikey', 'ahsap_koyu', 'ahsap', 'koyu'),
                    v0=0.012, en=0.6, ust=0.018, derin=0.016, sivri=0.0, cerceve=(0.005, 'boya_kirmizi'), k_say=8)
    silme(y, dikdortgen(-LW, LW, -LW, LW), zl1 - 0.012, 0.012, 0.008, 'ahsap_koyu', 'duz')
    # spire with a gable on each side at its foot
    SP = 0.36
    zs = cati_kirma(y, -LW, LW, -LW, LW, zl1, SP, 0.03, 'ahsap_koyu', 'ahsap', kalinlik=0.01, nr=8, ns=6, dilim=SH, mahya_en=0.01)
    for k in range(4):
        with parca(y, (0, 0, 0), k * math.pi / 2):
            # a small gable dormer facing -y
            zg = cati_besik(y, -0.045, 0.045, -LW - 0.07, -LW + 0.03, zl1 - 0.004, 0.068, 0.012, 'ahsap_koyu', 'ahsap', kalinlik=0.008,
                            ucluk_key='ahsap_dikey', uc_sacak=0.01, nr=4, ns=3, dilim=SH)
            y.oculus(V(0, -LW - 0.071, zl1 + 0.032), X, -Y, 0.012, 'koyu', 'boya_kirmizi', f=0.004, k=8)
            ejder(y, V(0, -LW - 0.082, zg - 0.01), V(0, -1), 0.06, 'ahsap_koyu')
    # gilded finial and a weather vane
    y.prizma((0, 0), 0.005, zs - 0.01, zs + 0.09, 'altin', n=6)
    kure(y, (0, 0, zs + 0.02), 0.016, 'altin', n=10, kat=5)
    kure(y, (0, 0, zs + 0.095), 0.008, 'altin', n=8, kat=4)
    kutu(y, V(0.006, -0.002, zs + 0.048), X, 0.065, 0.004, 0.034, 'altin')

# ---------------- the hörgr, idols, sacred tree ----------------
y.bolum('Hörgr: taş sunak')
AC = V(0.52, -0.8)
for i, (dx, dy, r) in enumerate(((0, 0, 0.07), (0.07, 0.03, 0.05), (-0.07, 0.02, 0.055), (0.03, -0.06, 0.05), (-0.04, -0.05, 0.045), (0.0, 0.07, 0.05))):
    kure(y, (AC.x + dx, AC.y + dy, Z0 + r * 0.4), r, 'kaya' if i % 2 else 'kaya_koyu', n=8, kat=4)
kutu_merkez(y, (AC.x, AC.y), 0.16, 0.11, 0.022, 'granit_koyu', z0=Z0 + 0.075, aci=0.15)
donel(y, (AC.x - 0.03, AC.y), [(0.0, Z0 + 0.097), (0.024, Z0 + 0.097), (0.03, Z0 + 0.115), (0.026, Z0 + 0.117), (0.0, Z0 + 0.112)], 'bronz', n=12)
# a fire on the slab's end
for k, (r, h, key) in enumerate(((0.02, 0.06, 'boya_kirmizi'), (0.013, 0.08, 'boya_sari'), (0.007, 0.05, 'beyaz'))):
    y.koni((AC.x + 0.045, AC.y + 0.005), r, Z0 + 0.097, h, key, n=6)
for k in range(5):
    t = TAU * k / 5
    cubuk(y, V(AC.x + 0.045 + 0.025 * math.cos(t), AC.y + 0.025 * math.sin(t), Z0 + 0.097), V(AC.x + 0.045, AC.y, Z0 + 0.13), 0.006, 'ahsap_koyu')


def put(x, yy, boy, yuz_key, bant, tac):
    """an idol post: a tall carved pole with painted bands and a bearded god's head under a helmet / hat"""
    y.prizma((x, yy), 0.024, Z0, Z0 + 0.03, 'granit', n=8, ust_renk='granit')
    y.prizma((x, yy), 0.016, Z0 + 0.03, Z0 + boy, 'ahsap', n=8)
    for zz in (0.12, 0.2):
        y.prizma((x, yy), 0.0175, Z0 + boy * zz * 2.4, Z0 + boy * zz * 2.4 + 0.016, bant, n=8)
    zf = Z0 + boy
    kutu_merkez(y, (x, yy), 0.038, 0.034, 0.05, yuz_key, z0=zf)
    for sx in (-1, 1):
        kutu_merkez(y, (x + sx * 0.009, yy - 0.0175), 0.008, 0.003, 0.006, 'koyu', z0=zf + 0.03)
    kutu_merkez(y, (x, yy - 0.019), 0.006, 0.006, 0.014, yuz_key, z0=zf + 0.016)
    donel(y, (x, yy - 0.012), [(0.0, zf - 0.028), (0.016, zf + 0.012), (0.0, zf + 0.014)], 'ahsap_koyu', n=6)
    if tac == 'migfer':
        donel(y, (x, yy), [(0.0, zf + 0.05), (0.026, zf + 0.05), (0.022, zf + 0.068), (0.0, zf + 0.082)], 'demir', n=10)
    elif tac == 'boynuz':
        donel(y, (x, yy), [(0.0, zf + 0.05), (0.024, zf + 0.05), (0.02, zf + 0.064), (0.0, zf + 0.072)], 'boya_sari', n=10)
        for sx in (-1, 1):
            boru(y, [V(x + sx * 0.02, yy, zf + 0.058), V(x + sx * 0.04, yy, zf + 0.075), V(x + sx * 0.042, yy, zf + 0.1)], 0.006, 'beyaz', n=5, r_son=0.002)
    else:
        donel(y, (x, yy), [(0.0, zf + 0.05), (0.032, zf + 0.05), (0.032, zf + 0.056), (0.016, zf + 0.06), (0.0, zf + 0.09)], 'koyu', n=10)


y.bolum('Put direkleri')
put(0.34, -0.6, 0.3, 'ahsap_acik', 'boya_kirmizi', 'sapka')      # Odin
put(0.56, -0.56, 0.36, 'ahsap_acik', 'boya_sari', 'migfer')        # Thor
put(0.78, -0.62, 0.3, 'ahsap_acik', 'boya_yesil', 'boynuz')       # Freyr

y.bolum('Kutsal dişbudak')
TX, TY = -0.8, -0.12
boru(y, [V(TX, TY, Z0), V(TX + 0.01, TY, Z0 + 0.18), V(TX - 0.01, TY + 0.01, Z0 + 0.32)], 0.04, 'ahsap', n=8, r_son=0.024)
for (dx, dy, dz) in ((0.1, 0.03, 0.34), (-0.1, -0.02, 0.36), (0.02, 0.09, 0.4), (0.0, -0.08, 0.33)):
    boru(y, [V(TX, TY, Z0 + 0.24), V(TX + dx * 0.6, TY + dy * 0.6, Z0 + dz)], 0.014, 'ahsap', n=6, r_son=0.008)
for i, (dx, dy, dz, r) in enumerate(((0, 0, 0.5, 0.17), (0.13, 0.04, 0.42, 0.12), (-0.13, -0.03, 0.43, 0.13), (0.03, 0.12, 0.44, 0.12),
                                     (-0.02, -0.12, 0.42, 0.12), (0.06, -0.02, 0.6, 0.11))):
    kure(y, (TX + dx, TY + dy, Z0 + dz), r, 'boya_yesil' if i % 2 == 0 else 'zeytin', n=12, kat=6)
# roots and offerings round its foot
for k in range(5):
    t = TAU * k / 5 + 0.3
    boru(y, [V(TX, TY, Z0 + 0.03), V(TX + 0.07 * math.cos(t), TY + 0.07 * math.sin(t), Z0 + 0.004)], 0.012, 'ahsap', n=5, r_son=0.005)
for k in range(4):
    t = TAU * k / 4 + 0.8
    kutu_merkez(y, (TX + 0.12 * math.cos(t), TY + 0.12 * math.sin(t)), 0.03, 0.022, 0.018, 'ahsap_acik' if k % 2 else 'bronz', z0=Z0)

y.bolum('Runik taş ve kutsal kuyu')
runik_tas(y, (-0.52, -0.74, Z0), 0.45, en=0.17, boy=0.36, kalin=0.05, key='kaya')
WC = (-0.72, 0.62)
dis = cokgen(WC, 0.07, 14); ic = cokgen(WC, 0.05, 14)
duvarlar(y, dis, Z0, Z0 + 0.04, 'granit')
for i in range(14):
    j = (i + 1) % 14
    duz_duvar(y, ic[j], ic[i], Z0 + 0.012, Z0 + 0.04, 'granit_koyu')
    y.yuz_yon([dis[i] + Z * (Z0 + 0.04), dis[j] + Z * (Z0 + 0.04), ic[j] + Z * (Z0 + 0.04), ic[i] + Z * (Z0 + 0.04)], 'granit', Z)
y.yuz_yon([V(p.x, p.y, Z0 + 0.012) for p in ic], 'su', Z)

y.bolum('Dikili taş çemberi (vé)')
k = 0
for (x0, y0, x1, y1, n) in ((-1.02, -0.92, 1.02, -0.92, 8), (1.02, -0.92, 1.02, 0.86, 7), (1.02, 0.86, -1.02, 0.86, 8), (-1.02, 0.86, -1.02, -0.92, 7)):
    for i in range(n):
        t = i / n
        x, yy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if abs(x) < 0.15 and yy < 0: continue
        dikili_tas(y, x, yy, Z0, 0.1 + 0.05 * ((k * 7) % 3) / 2, 0.028, 'kaya', tohum=k, egik=0.05)
        k += 1
for sx in (-1, 1):   # the two gate stones by the path, taller
    dikili_tas(y, sx * 0.15, -0.92, Z0, 0.2, 0.035, 'kaya_koyu', tohum=50 + sx, egik=0.02)

y.bolum('Taş gemi (skeppssättning)')
SS = V(0.8, 0.3)
for i in range(18):
    t = TAU * i / 18
    u, w = 0.33 * math.cos(t), 0.1 * math.sin(t) * (1 - 0.35 * abs(math.cos(t)) ** 3)
    hh = 0.06 + 0.07 * abs(math.cos(t)) ** 6
    dikili_tas(y, SS.x + w, SS.y + u, Z0, hh, 0.018, 'kaya', tohum=200 + i, egik=0.03)
tas_yer([(SS.x + 0.08 * math.sin(TAU * i / 14) * (1 - 0.35 * abs(math.cos(TAU * i / 14)) ** 3), SS.y + 0.3 * math.cos(TAU * i / 14)) for i in range(14)], 'toprak_ot')

y.bolum('Meşaleli yol')
for sx in (-1, 1):
    for ty in (-0.78, -0.6):
        x = sx * 0.135
        kutu_merkez(y, (x, ty), 0.03, 0.03, 0.016, 'granit', z0=Z0)
        y.prizma((x, ty), 0.007, Z0 + 0.016, Z0 + 0.15, 'ahsap_koyu', n=6)
        y.prizma((x, ty), 0.0085, Z0 + 0.1, Z0 + 0.11, 'boya_kirmizi', n=6)
        donel(y, (x, ty), [(0.006, Z0 + 0.148), (0.018, Z0 + 0.165), (0.016, Z0 + 0.172), (0.0, Z0 + 0.168)], 'demir', n=8)
        for r, h, key in ((0.013, 0.04, 'boya_kirmizi'), (0.008, 0.05, 'boya_sari')):
            y.koni((x, ty), r, Z0 + 0.168, h, key, n=6)

y.bolum('Sancaklar')
for sx in (-1, 1):
    sancak(y, TC.x + sx * 0.25, TC.y - GY - 0.22, Z0, boy=0.42, en=0.11, yuk=0.075, aci=-math.pi / 2 + sx * 0.6, direk_key='ahsap_koyu', kuyruk=True)

calistir(y, 'lm_hof')
