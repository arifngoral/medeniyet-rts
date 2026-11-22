# Les Invalides (lm_invalides): the Dome des Invalides facing the front (-y) - its two-storey classical front with
# Doric and Corinthian columns and a pediment, the drum with paired columns and buttresses, the attic, the lead dome
# with its gilded ribs, garlands and trophy dormers, the gilded lantern and spire; behind it the Saint-Louis nave and
# the Hotel des Invalides round the arcaded Cour d'Honneur and its side courts under Mansart roofs with dormers;
# before the dome the dry moat, the garden and the row of bronze cannons.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import *
from bina_ortak import calistir
import doku

# the Invalides' lead is dark (the gilding stands out on it): this building's own lead shades
doku.MALZEME['kursun'] = ('kursun', (0.35, 0.37, 0.42), {})
doku.MALZEME['kursun2'] = ('kursun', (0.315, 0.335, 0.385), {})

y = Yapi()
Z0 = 0.035
TAS = 'kirec'
PEN = (TAS, 'tas_koyu', 'tas_acik', 'cam')
DC = V(0, -0.31)
DX, DY0, DY1 = 0.27, -0.58, -0.04          # the dome church's square block
L1, L2 = 0.15, 0.13                        # its two orders
ZB = Z0 + L1 + L2                          # its top (under the entablature)


def nc_of(a, b):
    a, b, L, e, nc = eksen(a, b)
    return e, nc


# ---------------------------------------------------------------- ground: the dry moat, the garden
y.bolum('Zemin, hendek ve bahçe')
GX = 0.88
YF, MY0, MY1, YB = -1.06, -0.78, -0.69, 1.22
ZM = 0.008
kutu(y, V(-GX, MY1, 0), X, 2 * GX, YB - MY1, Z0, 'tas_koyu', 'sagsolarka')
y.yuz_yon([V(-GX, MY1, Z0), V(GX, MY1, Z0), V(GX, YB, Z0), V(-GX, YB, Z0)], 'zemin', Z)
duz_duvar(y, V(-GX, MY1), V(GX, MY1), ZM, Z0, 'tas')          # the moat's inner wall (faces the moat, -y)
kutu(y, V(-GX, YF, 0), X, 2 * GX, MY0 - YF, Z0, 'tas_koyu', 'onsagsol')
y.yuz_yon([V(-GX, YF, Z0), V(GX, YF, Z0), V(GX, MY0, Z0), V(-GX, MY0, Z0)], 'cimen_kuru', Z)
duz_duvar(y, V(GX, MY0), V(-GX, MY0), ZM, Z0, 'tas')           # the outer wall (faces +y)
y.yuz_yon([V(-GX, MY0, ZM), V(GX, MY0, ZM), V(GX, MY1, ZM), V(-GX, MY1, ZM)], 'cimen', Z)
for sx in (-1, 1):
    duz_duvar(y, *((V(-GX, MY1), V(-GX, MY0)) if sx < 0 else (V(GX, MY0), V(GX, MY1))), 0, ZM, 'tas_koyu')
# the causeway over the moat to the dome
for sx in (-1, 1):
    duz_duvar(y, *((V(-0.07, MY1), V(-0.07, MY0)) if sx < 0 else (V(0.07, MY0), V(0.07, MY1))), ZM, Z0, 'tas')
y.yuz_yon([V(-0.07, MY0, Z0), V(0.07, MY0, Z0), V(0.07, MY1, Z0), V(-0.07, MY1, Z0)], 'zemin', Z)
# a low parapet on the moat's edges
for yy, s in ((MY0 - 0.006, 1), (MY1 + 0.006, -1)):
    for x0, x1 in ((-GX, -0.07), (0.07, GX)):
        kutu3(y, V((x0 + x1) / 2, yy, Z0 + 0.008), X, Y, Z, x1 - x0, 0.012, 0.016, 'tas', ('+y', '-y', '+z', '+x', '-x'))
# the garden before the moat: lawns with clipped yews and a gravel walk on the axis
y.yuz_yon([V(-0.07, YF + 0.01, Z0 + 0.002), V(0.07, YF + 0.01, Z0 + 0.002), V(0.07, MY0 - 0.02, Z0 + 0.002), V(-0.07, MY0 - 0.02, Z0 + 0.002)], 'kum_acik', Z)
for sx in (-1, 1):
    for x0, x1 in ((0.12, 0.42), (0.48, 0.82)):
        a0, a1 = sorted((sx * x0, sx * x1))
        zz = Z0 + 0.004
        y.yuz_yon([V(a0, YF + 0.04, zz), V(a1, YF + 0.04, zz), V(a1, MY0 - 0.04, zz), V(a0, MY0 - 0.04, zz)], 'cimen', Z)
        duvarlar(y, dikdortgen(a0, a1, YF + 0.04, MY0 - 0.04), Z0, zz, 'boya_yesil')
        for px in (a0 + 0.03, (a0 + a1) / 2, a1 - 0.03):
            for py in (YF + 0.07, MY0 - 0.07):
                donel(y, (px, py), [(0.0, zz), (0.014, zz), (0.0, zz + 0.06)], 'boya_yesil', n=6)
# the paved esplanade between the moat and the dome
y.yuz_yon([V(-0.34, MY1 + 0.02, Z0 + 0.002), V(0.34, MY1 + 0.02, Z0 + 0.002), V(0.34, DY0 - 0.06, Z0 + 0.002), V(-0.34, DY0 - 0.06, Z0 + 0.002)], 'tas_acik', Z)
# the lawns flanking the dome church: box-edged beds, clipped yews, a basin, a box scroll, and a row of lime trees
# along the outer edge
for sx in (-1, 1):
    for (b0, b1) in ((-0.6, -0.17), (-0.11, 0.31)):
        a0, a1 = sorted((sx * 0.36, sx * 0.74))
        zz = Z0 + 0.004
        y.yuz_yon([V(a0, b0, zz), V(a1, b0, zz), V(a1, b1, zz), V(a0, b1, zz)], 'cimen', Z)
        kb = dikdortgen(a0, a1, b0, b1)
        duvarlar(y, kb, Z0, zz, 'boya_yesil')
        for i in range(4):
            pa, pb, L_, e, nc = eksen(kb[i], kb[(i + 1) % 4])
            kutu3(y, pa.lerp(pb, 0.5) - nc * 0.005 + Z * (zz + 0.005), e, nc, Z, L_ - 0.01, 0.008, 0.01, 'yesil_koyu', ('+x', '-x', '+y', '-y', '+z'))
        for px in (a0 + 0.03, a1 - 0.03):
            for py in (b0 + 0.03, b1 - 0.03):
                donel(y, (px, py), [(0.0, zz), (0.013, zz), (0.0, zz + 0.055)], 'yesil_koyu', n=6)
        cx_, cy_ = (a0 + a1) / 2, (b0 + b1) / 2
        if b0 < -0.3:   # a round basin in the front bed
            donel(y, (cx_, cy_), [(0.058, zz), (0.058, zz + 0.012), (0.051, zz + 0.012), (0.051, zz + 0.0085)], 'tas_acik', n=16)
            y.yuz_yon([V(cx_ + 0.051 * math.cos(TAU * k / 16), cy_ + 0.051 * math.sin(TAU * k / 16), zz + 0.0085) for k in range(16)], 'su', Z)
            donel(y, (cx_, cy_), [(0.0, zz + 0.008), (0.008, zz + 0.008), (0.004, zz + 0.03), (0.007, zz + 0.034), (0.0, zz + 0.04)], 'tas_acik', n=6)
        else:           # a box scroll round a tall clipped yew
            pts = [V(cx_ + 0.07 * math.cos(TAU * k / 14), cy_ + 0.1 * math.sin(TAU * k / 14), zz + 0.004) for k in range(15)]
            boru(y, pts, 0.004, 'yesil_koyu', n=3, kapat=False)
            donel(y, (cx_, cy_), [(0.0, zz), (0.016, zz), (0.0, zz + 0.08)], 'yesil_koyu', n=6)
    for yy in (-0.52, -0.38, -0.24, -0.1, 0.04, 0.18, 0.31):   # the lime avenue
        agac(y, sx * 0.81, yy, Z0, boy=0.15)


# ---------------------------------------------------------------- the cannons
y.bolum('Top sırası')


def top(x, yy, z, aci=-math.pi / 2):
    """a bronze cannon on a wooden field carriage with two wheels, its muzzle toward aci"""
    with parca(y, (x, yy, z), aci):
        cubuk(y, V(-0.03, 0, 0.004), V(0.008, 0, 0.017), 0.016, 'ahsap_koyu', 0.008)          # the trail
        boru(y, [V(-0.012, 0, 0.022), V(0.022, 0, 0.024), V(0.046, 0, 0.026)], 0.0065, 'bronz', n=6, r_son=0.0045)
        kure(y, (-0.014, 0, 0.022), 0.006, 'bronz', n=6, kat=3)
        for s in (-1, 1):
            with parca(y, (0.0, s * 0.013, 0.0), 0):
                pts = [V(0.016 * math.cos(TAU * k / 8), 0, 0.016 + 0.016 * math.sin(TAU * k / 8)) for k in range(8)]
                for sg in (-1, 1):
                    y.yuz_yon([p + V(0, sg * 0.002, 0) for p in pts], 'ahsap', V(0, sg, 0))
                for k in range(8):
                    a, b = pts[k], pts[(k + 1) % 8]
                    y.yuz_yon([a + V(0, -0.002, 0), b + V(0, -0.002, 0), b + V(0, 0.002, 0), a + V(0, 0.002, 0)], 'demir', (a + b) / 2 - V(0, 0, 0.016))
        cubuk(y, V(0, -0.016, 0.016), V(0, 0.016, 0.016), 0.004, 'demir')


for k in range(14):
    x = -0.8 + 1.6 * k / 13
    if abs(x) < 0.1: continue
    top(x, MY1 + 0.045, Z0)
# pyramids of cannon balls
for x in (-0.12, 0.12):
    for i, (dx, dy, dz) in enumerate(((0, 0, 0), (0.01, 0, 0), (-0.01, 0, 0), (0, 0.01, 0), (0, -0.01, 0), (0.005, 0.005, 0.008), (-0.005, -0.005, 0.008),
                                     (0.005, -0.005, 0.008), (-0.005, 0.005, 0.008), (0, 0, 0.015))):
        kure(y, (x + dx, MY1 + 0.05 + dy, Z0 + 0.006 + dz), 0.006, 'demir', n=5, kat=3)


# ---------------------------------------------------------------- the dome church's square block
y.bolum('Kubbeli kilise: cephe')


def iki_kat(a, b, n, ilk=True, son=True, kapi=None):
    """two orders of a front a->b in n bays: arched windows below, square windows above, Doric and Corinthian pilasters"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e, nc = nc_of(a, b)
    W = (b - a).length / n
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        if kapi == k:
            y.kemerli(p, q, Z0, L1, (TAS, 'tas_koyu', 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.5, ust=0.03, derin=0.02, k_say=8, sivri=0.0,
                      cerceve=(0.006, 'tas_acik'))
        else:
            _, _, _, L = y.kemerli(p, q, Z0, L1, PEN, v0=0.03, en=0.42, ust=0.03, derin=0.014, k_say=6, sivri=0.0, cerceve=(0.005, 'tas_acik'))
        _, _, _, L = dikdortgen_acik(y, p, q, Z0 + L1, L2, 0.3, 0.7, 0.025, L2 - 0.03, PEN, derin=0.012, cerceve=(0.005, 'tas_acik'))
        ucgen_alinlik(y, lambda u, v: L(u / W, 0) + Z * (v - Z0 - L1), e, nc, W * 0.26, W * 0.74, Z0 + L1 + L2 - 0.022, 0.016, 'tas_acik', 0.006)
    for k in range(n + 1):
        if (k == 0 and not ilk) or (k == n and not son): continue
        pp = a.lerp(b, k / n)
        ky = ('-y',) if k in (0, n) else ()
        kutu3(y, pp + nc * 0.003 + Z * (Z0 + L1 / 2), e, nc, Z, 0.02, 0.006, L1, 'tas_acik', ('+x', '-x', '+y') + ky)
        kutu3(y, pp + nc * 0.003 + Z * (Z0 + L1 + L2 / 2), e, nc, Z, 0.018, 0.006, L2, 'tas_acik', ('+x', '-x', '+y') + ky)
        kutu3(y, pp + nc * 0.005 + Z * (Z0 + L1 + L2 - 0.008), e, nc, Z, 0.026, 0.01, 0.014, 'tas_acik', ('+x', '-x', '+y', '+z', '-z') + ky)


AVX, AVY = 0.13, DY0 - 0.04                 # the central avant-corps
blok = dikdortgen(-DX, DX, DY0, DY1)
# the front: side parts and the avant-corps
iki_kat(V(-DX, DY0), V(-AVX, DY0), 2)
iki_kat(V(AVX, DY0), V(DX, DY0), 2)
iki_kat(V(-AVX, AVY), V(AVX, AVY), 3, kapi=1)
for s in (-1, 1):
    a, b = (V(-AVX, DY0), V(-AVX, AVY)) if s < 0 else (V(AVX, AVY), V(AVX, DY0))
    duz_duvar(y, a, b, Z0, ZB, TAS)
# the other three sides
iki_kat(blok[1], blok[2], 5)
iki_kat(blok[3], blok[0], 5)
iki_kat(blok[2], blok[3], 5)
# mouldings, entablature, the flat roof and its balustrade with fire-pots
cevre = [V(-DX, DY1), V(-DX, DY0), V(-AVX, DY0), V(-AVX, AVY), V(AVX, AVY), V(AVX, DY0), V(DX, DY0), V(DX, DY1)]
cevre_k = cevre + [cevre[0]]
silme(y, cevre, Z0, 0.014, 0.008, 'tas_acik', 'kaide')
silme(y, cevre, Z0 + L1 - 0.004, 0.014, 0.008, 'tas_acik', 'duz')
silme(y, cevre, ZB - 0.002, 0.012, 0.006, TAS, 'duz')
silme(y, cevre, ZB + 0.01, 0.016, 0.016, 'tas_acik', 'tac')
ZT = ZB + 0.026
y.yuz_yon([V(p.x, p.y, ZT) for p in cevre], 'kursun', Z)
korkuluk_hafif(y, [V(-DX + 0.006, DY1), V(-DX + 0.006, DY0 + 0.006), V(-AVX - 0.004, DY0 + 0.006)], ZT, 0.032, False, 'tas_acik', ayak=0.09,
               ust='vazo', ust_key='altin', ust_adim=1)
korkuluk_hafif(y, [V(AVX + 0.004, DY0 + 0.006), V(DX - 0.006, DY0 + 0.006), V(DX - 0.006, DY1)], ZT, 0.032, False, 'tas_acik', ayak=0.09,
               ust='vazo', ust_key='altin', ust_adim=1)
# the free-standing columns of the avant-corps: Doric below, Corinthian above, entablatures, the pediment
y.bolum('Kubbeli kilise: sütunlar ve alınlık')
CY_ = AVY - 0.026
for xx in (-0.118, -0.082, -0.042, 0.042, 0.082, 0.118):
    kutu3(y, V(xx, CY_, Z0 + 0.008), X, Y, Z, 0.026, 0.026, 0.016, 'tas_acik', ('+x', '-x', '+y', '-y', '+z'))
    sutun_hafif(y, xx, CY_, Z0 + 0.016, Z0 + L1 - 0.012, 0.009, 'tas_acik', 'dor')
for xx in (-0.082, -0.042, 0.042, 0.082):
    sutun_hafif(y, xx, CY_, Z0 + L1 + 0.012, ZB - 0.012, 0.008, 'tas_acik', 'iyon')
for zz in (Z0 + L1 - 0.012, ZB - 0.012):
    kutu3(y, V(0, (CY_ + AVY) / 2 - 0.004, zz + 0.012), X, Y, Z, 2 * AVX + 0.012, AVY - CY_ + 0.026, 0.024, 'tas_acik', ('+x', '-x', '-y', '+z', '-z'))
    silme(y, [V(-AVX - 0.006, CY_ - 0.017), V(AVX + 0.006, CY_ - 0.017)], zz + 0.022, 0.01, 0.006, 'tas_acik', 'tac', kapali=False)
# the balcony balustrade over the lower order
korkuluk_hafif(y, [V(-AVX, CY_ - 0.008), V(AVX, CY_ - 0.008)], Z0 + L1 + 0.012, 0.024, False, 'tas_acik', ayak=0.08)
tz = alinlik(y, V(-AVX - 0.008, CY_ - 0.02), V(AVX + 0.008, CY_ - 0.02), ZB + 0.012, 0.075, derin=AVY - CY_ + 0.04, key='tas_acik', ic_key=TAS, c=0.009,
             cati_key='kursun')
# the royal arms in the tympanum
y.oculus(V(0, CY_ - 0.0265, ZB + 0.042), X, -Y, 0.016, 'altin', 'altin', f=0.004, k=12)
for k in range(9):
    t = math.pi * (0.1 + 0.8 * k / 8)
    d_ = X * math.cos(t) + Z * math.sin(t)
    q_ = d_.cross(-Y).normalized()
    p0, p1 = V(0, CY_ - 0.027, ZB + 0.042) + d_ * 0.021, V(0, CY_ - 0.027, ZB + 0.042) + d_ * 0.03
    y.yuz_yon([p0 - q_ * 0.002, p0 + q_ * 0.002, p1], 'altin', -Y)
for s in (-1, 1):
    heykel(y, s * (AVX + 0.004), CY_ - 0.01, ZB + 0.024, 1.1, 'tas_acik', 0, n=5)
heykel(y, 0, CY_ - 0.006, tz - 0.002, 1.0, 'tas_acik', 0, n=5)
# statues in niches beside the door (Charlemagne and Saint Louis)
for s in (-1, 1):
    heykel(y, s * 0.062, AVY - 0.008, Z0 + 0.03, 1.35, 'tas_acik', 0, n=5)

# ---------------------------------------------------------------- the drum, the dome, the lantern
y.bolum('Kasnak')
ZD0 = ZT
# a stepped round pedestal and four gilded fire-pots on the corners of the terrace
donel(y, DC, [(0.225, ZD0), (0.225, ZD0 + 0.02), (0.212, ZD0 + 0.02), (0.212, ZD0 + 0.045), (0.205, ZD0 + 0.045)], 'tas_acik', n=24)
for sx in (-1, 1):
    for sy in (-1, 1):
        p = DC + V(sx * 0.2, sy * 0.2)
        kutu_merkez(y, (p.x, p.y), 0.05, 0.05, 0.05, TAS, z0=ZD0)
        silme(y, dikdortgen(p.x - 0.025, p.x + 0.025, p.y - 0.025, p.y + 0.025), ZD0 + 0.044, 0.01, 0.006, 'tas_acik', 'tac')
        donel(y, (p.x, p.y), [(0.0, ZD0 + 0.054), (0.014, ZD0 + 0.054), (0.018, ZD0 + 0.07), (0.01, ZD0 + 0.08), (0.006, ZD0 + 0.1), (0.0, ZD0 + 0.12)], 'altin', n=6)
RD, ND = 0.175, 12
ZK0 = ZD0 + 0.045
HK = 0.2
dk = cokgen(DC, RD, ND, math.pi / ND)
for i in range(ND):
    a, b = dk[i], dk[(i + 1) % ND]
    y.kemerli(a, b, ZK0, HK, PEN, v0=0.03, en=0.42, ust=0.03, derin=0.016, k_say=6, sivri=0.0, cerceve=(0.005, 'tas_acik'))
    e, nc = nc_of(a, b)
    m = a.lerp(b, 0.5)
    kutu3(y, m + nc * 0.0035 + Z * (ZK0 + HK - 0.026), e, nc, Z, 0.012, 0.007, 0.016, 'tas_acik', ('+x', '-x', '+y', '+z', '-z'))
# buttresses with paired Corinthian columns before them, an entablature ring
for i in range(ND):
    t = math.pi / ND + TAU * i / ND
    r_ = V(math.cos(t), math.sin(t)); t_ = V(-r_.y, r_.x)
    c = DC + r_ * (RD + 0.014)
    kutu3(y, c + Z * (ZK0 + HK / 2), r_, t_, Z, 0.03, 0.026, HK, TAS, ('+x', '-x', '+y', '-y'))
    for s in (-1, 1):
        cc = DC + r_ * (RD + 0.036) + t_ * (s * 0.014)
        sutun_hafif(y, cc.x, cc.y, ZK0, ZK0 + HK - 0.012, 0.0075, 'tas_acik', 'iyon', n=6)
    # the volute console on the buttress's top: a concave scroll from the entablature's edge up to the attic's top,
    # a roll at its foot and a gilt flame-pot on it
    R0, R1, zb, Hc, w2 = RD + 0.04, RD - 0.009, ZK0 + HK + 0.0015, 0.048, 0.011
    pr = [(R1 + (R0 - R1) * (1 - math.sin(math.pi / 2 * k / 6)), zb + Hc * (1 - math.cos(math.pi / 2 * k / 6))) for k in range(7)]
    Pc = lambda rr, zz, s: DC + r_ * rr + t_ * (s * w2) + Z * zz
    for s in (-1, 1):
        y.yuz_yon([Pc(rr, zz, s) for rr, zz in pr] + [Pc(R1, zb, s)], 'tas_acik', t_ * s)
    for k in range(6):
        (ra, za), (rb, zb_) = pr[k], pr[k + 1]
        y.yuz_yon([Pc(ra, za, -1), Pc(rb, zb_, -1), Pc(rb, zb_, 1), Pc(ra, za, 1)], 'tas_acik', r_ * (zb_ - za) + Z * (ra - rb))
    boru(y, [Pc(R0 - 0.005, zb + 0.006, -1.15), Pc(R0 - 0.005, zb + 0.006, 1.15)], 0.0065, 'tas_acik', n=6)
    cc = DC + r_ * (RD - 0.002)
    donel(y, (cc.x, cc.y), [(0.0, zb + Hc), (0.008, zb + Hc), (0.006, zb + Hc + 0.008), (0.009, zb + Hc + 0.016), (0.004, zb + Hc + 0.024),
                            (0.0, zb + Hc + 0.034)], 'altin', n=6)
silme(y, cokgen(DC, RD + 0.012, ND * 2, math.pi / ND / 2), ZK0 + HK - 0.012, 0.014, 0.04, 'tas_acik', 'tac')
donel(y, DC, [(RD + 0.013, ZK0 + HK + 0.0015), (RD - 0.012, ZK0 + HK + 0.0015)], 'tas_acik', n=ND * 2, kat=math.pi / ND / 2)   # (the drum's top ring under the attic)
# the attic with its small windows
y.bolum('Kubbe')
ZA0 = ZK0 + HK + 0.002
HA = 0.05
ak = cokgen(DC, RD - 0.004, ND * 2, math.pi / ND / 2)
for i in range(ND * 2):
    a, b = ak[i], ak[(i + 1) % (ND * 2)]
    if i % 2 == 1:   # (windows over the drum's windows, the consoles over the buttresses)
        dikdortgen_acik(y, a, b, ZA0, HA, 0.25, 0.75, 0.012, HA - 0.012, PEN, derin=0.008)
    else:
        duz_duvar(y, a, b, ZA0, ZA0 + HA, TAS)
silme(y, ak, ZA0 + HA - 0.008, 0.01, 0.01, 'tas_acik', 'tac')
# the dome: lead, gilded ribs, gilded garlands, the twelve trophy dormers
ZK = ZA0 + HA
RK, HKB = RD + 0.002, 0.27
tepe = y.kubbe(DC, RK, ZK, HKB, 'kursun', n=48, kat=16)


def kubbe_nokta(t, ph, ek=0.0):
    return V(DC.x + (RK + ek) * math.cos(ph) * math.cos(t), DC.y + (RK + ek) * math.cos(ph) * math.sin(t), ZK + (HKB + ek) * math.sin(ph))


for i in range(ND):
    t = math.pi / ND + TAU * i / ND
    boru(y, [kubbe_nokta(t, math.pi / 2 * k / 14, 0.004) for k in range(14)], 0.0065, 'altin', n=4, kapat=False)
    # garlands: a gilded swag between this rib and the next, a medallion over it
    t2 = t + TAU / ND
    sw = [kubbe_nokta(t + (t2 - t) * j / 6, 0.62 - 0.12 * math.sin(math.pi * j / 6), 0.004) for j in range(7)]
    boru(y, sw, 0.0035, 'altin', n=4)
    tm = (t + t2) / 2
    mc = kubbe_nokta(tm, 0.8, 0.002)
    nn = (mc - V(DC.x, DC.y, ZK)).normalized()
    ex = V(-math.sin(tm), math.cos(tm), 0)
    upv = nn.cross(ex).normalized()
    Pm = lambda rr, tt, d, mc=mc, ex=ex, upv=upv, nn=nn: mc + ex * (rr * math.cos(tt)) + upv * (rr * math.sin(tt)) + nn * d
    halka(y, Pm, 0.0, 0.009, 0.002, 'altin', nn, 8)
    # the trophy dormer at the dome's foot: a small framed window with a gilded helmet
    p0 = kubbe_nokta(tm, 0.1, 0.0)
    rr_ = V(math.cos(tm), math.sin(tm)); tt_ = V(-rr_.y, rr_.x)
    c0 = V(DC.x, DC.y) + rr_ * (RK * math.cos(0.1) + 0.006)
    kutu3(y, c0 - rr_ * 0.01 + Z * (ZK + 0.03), rr_, tt_, Z, 0.04, 0.034, 0.05, 'kursun2', ('+x', '+y', '-y', '+z'))
    y.oculus(c0 + rr_ * 0.01 + Z * (ZK + 0.032), tt_, rr_, 0.009, 'koyu', 'altin', f=0.004, k=10)
    for s in (-1, 1):   # gilded strips framing the dormer's face
        kutu3(y, c0 + rr_ * 0.0115 + tt_ * (s * 0.0145) + Z * (ZK + 0.03), rr_, tt_, Z, 0.003, 0.005, 0.05, 'altin', ('+x', '+y', '-y', '+z'))
    kure(y, (c0.x, c0.y, ZK + 0.062), 0.012, 'altin', n=6, kat=4)
    cubuk(y, V(c0.x, c0.y, ZK + 0.07), V(c0.x, c0.y, ZK + 0.086), 0.004, 'altin')
# the lantern: a ring of gilded columns round a dark core, a small gilded dome, the spire, the globe and the cross
y.bolum('Fener ve sivri tepe')
ZL0 = tepe.z - 0.012
donel(y, DC, [(0.05, ZL0 - 0.004), (0.05, ZL0 + 0.008), (0.046, ZL0 + 0.008)], 'kursun2', n=16)
y.prizma((DC.x, DC.y), 0.03, ZL0 + 0.008, ZL0 + 0.07, 'koyu', n=8, ust=False)
for i in range(8):
    t = TAU * i / 8
    sutun_hafif(y, DC.x + 0.042 * math.cos(t), DC.y + 0.042 * math.sin(t), ZL0 + 0.008, ZL0 + 0.07, 0.0042, 'altin', 'iyon', n=5)
halka_kornis(y, DC, 0.046, ZL0 + 0.07, 0.008, 0.006, 16, 'altin')
y.yuz_yon([V(DC.x + 0.046 * math.cos(TAU * k / 16), DC.y + 0.046 * math.sin(TAU * k / 16), ZL0 + 0.078) for k in range(16)], 'kursun', Z)
t2 = y.kubbe(DC, 0.036, ZL0 + 0.078, 0.03, 'altin', n=16, kat=5)
donel(y, DC, [(0.014, t2.z - 0.004), (0.012, t2.z + 0.02), (0.006, t2.z + 0.14), (0.0, t2.z + 0.17)], 'altin', n=8)
kure(y, (DC.x, DC.y, t2.z + 0.17), 0.012, 'altin', n=8, kat=4)
cubuk(y, V(DC.x, DC.y, t2.z + 0.18), V(DC.x, DC.y, t2.z + 0.23), 0.005, 'altin')
cubuk(y, V(DC.x - 0.016, DC.y, t2.z + 0.212), V(DC.x + 0.016, DC.y, t2.z + 0.212), 0.005, 'altin')

# ---------------------------------------------------------------- the Saint-Louis church (the soldiers' nave)
y.bolum('Saint-Louis kilisesi')
NX_, NY0_, NY1_ = 0.12, DY1, 0.38
NH_ = 0.25
for (a, b) in ((V(NX_, NY0_), V(NX_, NY1_)), (V(-NX_, NY1_), V(-NX_, NY0_))):
    e, nc = nc_of(a, b)
    for k in range(5):
        p, q = a.lerp(b, k / 5), a.lerp(b, (k + 1) / 5)
        y.kemerli(p, q, Z0, NH_, PEN, v0=0.12, en=0.45, ust=0.03, derin=0.012, k_say=6, sivri=0.0)
    for k in range(6):
        pp = a.lerp(b, k / 5)
        kutu3(y, pp + nc * 0.006 + Z * (Z0 + NH_ / 2), e, nc, Z, 0.022, 0.012, NH_, TAS, ('+x', '-x', '+y', '+z'))
    silme(y, [a, b], Z0 + NH_ - 0.006, 0.012, 0.01, 'tas_acik', 'tac', kapali=False)
cati_besik(y, -NX_, NX_, NY0_, NY1_, Z0 + NH_, 0.1, 0.02, 'arduvaz', 'kursun', ucluk_key=TAS, ns=8, nr=4, uc_sacak=0.0)


# ---------------------------------------------------------------- the Hotel des Invalides
y.bolum('Askerî hastane (Invalides)')
HX0, HX1, HY0, HY1 = -0.82, 0.82, 0.38, 1.12
W_ = 0.1
H3 = 0.08                     # one storey
HH = 3 * H3
ZH = Z0 + HH


def pencereler(a, b, n, z0=Z0, katlar=3, kapi=None, bos=None):
    """a plain stone front a->b of n bays and three storeys: square-headed windows, string courses; kapi: a bay with
    an arched door; bos: (u0, u1) a stretch left plain"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e, nc = nc_of(a, b)
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        um = (k + 0.5) / n
        if bos and bos[0] < um < bos[1]:
            duz_duvar(y, p, q, z0, z0 + katlar * H3, TAS); continue
        for j in range(katlar):
            if j == 0 and kapi == k:
                y.kemerli(p, q, z0, H3, (TAS, 'tas_koyu', 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.5, ust=0.012, derin=0.012, k_say=6, sivri=0.0)
            else:
                dikdortgen_acik(y, p, q, z0 + j * H3, H3, 0.32, 0.68, 0.016, H3 - 0.016, PEN, derin=0.008)
    for j in (1, 2):
        silme(y, [a, b], z0 + j * H3 - 0.003, 0.006, 0.005, 'tas_acik', 'duz', kapali=False)


def revak(a, b, n):
    """the Cour d'Honneur's two tiers of arcades (deep arches on piers) and a top storey of windows"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    for j in range(2):
        kemer_dizisi(y, a, b, n, Z0 + j * H3, H3, 0.035, renk=(TAS, 'tas_koyu', 'tas_acik', 'koyu'), en=0.66, ust=0.012, sivri=0.0, acik=False,
                     taban=(j == 0))
    e, nc = nc_of(a, b)
    a2, b2 = a - nc * 0.035 - e * 0.035, b - nc * 0.035 + e * 0.035   # (run on into the court's corners)
    for k in range(n):
        p, q = a2.lerp(b2, k / n), a2.lerp(b2, (k + 1) / n)
        dikdortgen_acik(y, p, q, Z0 + 2 * H3, H3, 0.3, 0.7, 0.016, H3 - 0.016, PEN, derin=0.008)
    # the tiers' cornices and the parapet of the upper gallery
    for j in (1, 2):
        silme(y, [a, b], Z0 + j * H3 - 0.004, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
    a1, b1 = a - e * 0.035, b + e * 0.035
    y.yuz_yon([V(a.x, a.y, Z0 + 2 * H3), V(b.x, b.y, Z0 + 2 * H3), V(b2.x, b2.y, Z0 + 2 * H3), V(a2.x, a2.y, Z0 + 2 * H3)], 'zemin', Z)
    y.yuz_yon([V(a.x, a.y, ZH), V(b.x, b.y, ZH), V(b2.x, b2.y, ZH), V(a2.x, a2.y, ZH)], TAS, -Z)   # (the eave's soffit over the set-back top storey)


O = dikdortgen(HX0, HX1, HY0, HY1)
I = dikdortgen(HX0 + W_, HX1 - W_, HY0 + W_, HY1 - W_)
# outer fronts
pencereler(O[0], O[1], 24, bos=(0.4, 0.6))
pencereler(O[1], O[2], 11)
pencereler(O[2], O[3], 25, kapi=12)
pencereler(O[3], O[0], 11)
# the Cour d'Honneur: arcades on all four sides (the south and north ranges' court faces, the dividers' inner faces)
CX = 0.34
revak(V(CX, HY0 + W_), V(-CX, HY0 + W_), 11)
revak(V(-CX, HY1 - W_), V(CX, HY1 - W_), 11)
revak(V(-CX, HY0 + W_), V(-CX, HY1 - W_), 9)
revak(V(CX, HY1 - W_), V(CX, HY0 + W_), 9)
# the side courts
for sx in (-1, 1):
    xa, xb = sorted((sx * (CX + W_), sx * (HX1 - W_)))
    cm = V((xa + xb) / 2, (HY0 + HY1) / 2)
    def ice(p, q, n):
        p, q = V(p[0], p[1]), V(q[0], q[1])
        e = (q - p).normalized()
        if V(e.y, -e.x).dot(cm - (p + q) / 2) < 0: p, q = q, p
        pencereler(p, q, n)
    ice(V(xa, HY0 + W_), V(xb, HY0 + W_), 5)
    ice(V(xa, HY1 - W_), V(xb, HY1 - W_), 5)
    ice(V(xa, HY0 + W_), V(xa, HY1 - W_), 9)
    ice(V(xb, HY0 + W_), V(xb, HY1 - W_), 9)
    y.yuz_yon([V(xa, HY0 + W_, Z0 + 0.003), V(xb, HY0 + W_, Z0 + 0.003), V(xb, HY1 - W_, Z0 + 0.003), V(xa, HY1 - W_, Z0 + 0.003)], 'cimen', Z)
# the court's gravel and the statue of the Emperor over the church door on the south side
y.yuz_yon([V(-CX + 0.035, HY0 + W_ + 0.035, Z0 + 0.002), V(CX - 0.035, HY0 + W_ + 0.035, Z0 + 0.002), V(CX - 0.035, HY1 - W_ - 0.035, Z0 + 0.002),
           V(-CX + 0.035, HY1 - W_ - 0.035, Z0 + 0.002)], 'kum_acik', Z)
kutu3(y, V(0, HY0 + W_ + 0.01, ZH + 0.03), X, Y, Z, 0.07, 0.02, 0.06, TAS, ('+x', '-x', '+y', '+z'))
heykel(y, 0, HY0 + W_ + 0.016, ZH + 0.06, 1.3, 'bronz', math.pi, n=5)
# the roofs: a Mansart ring round the courts with dormers, the dividers' Mansart roofs
y.bolum('Hastane çatıları')


def mansard_halka(O, I, z, h1, h2, s=0.012, egim=0.36):
    di = egim * h1
    w = (I[0] - O[0]).length / math.sqrt(2)
    o0, o1 = disa(O, s), disa(O, -di)
    i0, i1 = disa(I, -s), disa(I, di)
    mid = disa(O, -w / 2)
    cc = sum(O, Vector()) / 4
    for i in range(4):
        j = (i + 1) % 4
        m = (O[i] + O[j]) / 2; mi = (I[i] + I[j]) / 2
        out = V(m.x - cc.x, m.y - cc.y).normalized()
        y.yuz_yon([o0[i] + Z * z, o0[j] + Z * z, o1[j] + Z * (z + h1), o1[i] + Z * (z + h1)], 'arduvaz', out + Z * 0.3)
        y.yuz_yon([i0[j] + Z * z, i0[i] + Z * z, i1[i] + Z * (z + h1), i1[j] + Z * (z + h1)], 'arduvaz', -out + Z * 0.3)
        y.yuz_yon([o1[i] + Z * (z + h1), o1[j] + Z * (z + h1), mid[j] + Z * (z + h1 + h2), mid[i] + Z * (z + h1 + h2)], 'kursun', out + Z * 2)
        y.yuz_yon([i1[j] + Z * (z + h1), i1[i] + Z * (z + h1), mid[i] + Z * (z + h1 + h2), mid[j] + Z * (z + h1 + h2)], 'kursun', -out + Z * 2)
        for a_, b_, d_ in ((o0[i], o0[j], out), (i0[j], i0[i], -out)):
            y.yuz_yon([a_ + Z * z, b_ + Z * z, b_ + Z * (z - 0.007), a_ + Z * (z - 0.007)], TAS, d_)
        y.yuz_yon([o0[i] + Z * (z - 0.007), o0[j] + Z * (z - 0.007), O[j] + Z * z, O[i] + Z * z], TAS, -Z)
        y.yuz_yon([i0[j] + Z * (z - 0.007), i0[i] + Z * (z - 0.007), I[i] + Z * z, I[j] + Z * z], TAS, -Z)
    silme(y, o1, z + h1 - 0.006, 0.006, 0.004, 'kursun', 'yarim')
    return (s + di) / h1


silme(y, O, ZH - 0.004, 0.012, 0.012, 'tas_acik', 'tac')
kk = mansard_halka(O, I, ZH + 0.008, 0.1, 0.03)
# dormers on the outer slopes over every other bay, and on the court side
oo = disa(O, 0.012)
for i, n in ((0, 24), (1, 11), (2, 25), (3, 11)):
    a, b = oo[i], oo[(i + 1) % 4]
    e, nc = nc_of(a, b)
    for k in range(n):
        if k % 2: continue
        u = (k + 0.5) / n
        if i == 0 and 0.4 < u < 0.6: continue
        lukarn(y, a.lerp(b, u), e, nc, ZH + 0.008, 0.026, 0.045, kk, TAS, 'kursun', 'cam', yaldiz='altin')
for sx in (-1, 1):
    x0, x1 = sorted((sx * CX, sx * (CX + W_)))
    mansard(y, x0, x1, HY0 + W_, HY1 - W_, ZH + 0.008, 0.1, 0.03, 'arduvaz', 'kursun', egim=0.36, sacak=0.012, yaldiz=None)
    silme(y, dikdortgen(x0, x1, HY0 + W_, HY1 - W_), ZH - 0.004, 0.012, 0.012, 'tas_acik', 'tac')
# chimneys
for (bx, by) in ((-0.6, HY0 + 0.05), (0.6, HY0 + 0.05), (-0.6, HY1 - 0.05), (0.6, HY1 - 0.05), (-HX1 + 0.05, 0.75), (HX1 - 0.05, 0.75), (-0.2, HY1 - 0.05),
                 (0.2, HY1 - 0.05)):
    kutu_merkez(y, (bx, by), 0.03, 0.02, 0.16, TAS, z0=ZH + 0.03)
    kutu_merkez(y, (bx, by), 0.036, 0.026, 0.008, 'tas_acik', z0=ZH + 0.19)
# the north front's central portal pavilion: the great arch rising into the roof with the king's relief
y.bolum('Kuzey kapısı ve bayrak')
PY = HY1
kutu3(y, V(0, PY - 0.022, Z0 + 0.16), X, Y, Z, 0.16, 0.076, 0.32, TAS, ('+x', '-x', '-y', '+z'))
for xa, xb in ((0.08, 0.05), (-0.05, -0.08)):
    duz_duvar(y, V(xa, PY + 0.016), V(xb, PY + 0.016), Z0, Z0 + 0.2, TAS)
duz_duvar(y, V(0.08, PY + 0.016), V(-0.08, PY + 0.016), Z0 + 0.2, Z0 + 0.32, TAS)
y.kemerli(V(0.05, PY + 0.016), V(-0.05, PY + 0.016), Z0, 0.2, (TAS, 'tas_koyu', 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.8, ust=0.02, derin=0.012,
          k_say=8, sivri=0.0, cerceve=(0.006, 'tas_acik'))
y.oculus(V(0, PY + 0.0165, Z0 + 0.26), -X, Y, 0.035, 'altin', 'tas_acik', f=0.008, k=16)
alinlik(y, V(0.085, PY + 0.016), V(-0.085, PY + 0.016), Z0 + 0.32, 0.05, derin=0.076, key=TAS, ic_key='tas_acik', c=0.007, cati_key='kursun')
for s in (-1, 1):
    vazo(y, s * 0.075, PY + 0.008, Z0 + 0.32, 1.4, 'altin', n=6)
sancak(y, 0, PY - 0.005, Z0 + 0.37, boy=0.2, en=0.11, yuk=0.065, aci=math.pi * 0.95)

calistir(y, 'lm_invalides')
