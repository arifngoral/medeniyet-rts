# Harbiye Mektebi (lm_harbiye): the 19th-century Ottoman military academy, a neoclassical quadrangle. Three-storey
# wings round a drill yard (rusticated stone ground floor, plastered upper floors with framed windows), hipped tile
# roofs, taller corner pavilions with pyramid roofs, the entrance block with a giant Ionic portico and a pediment;
# in the yard cadets drilling in ranks, a field gun and the flag; outside, steps, guns and lamps.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.04
KATLAR = (('alt', 0.15), ('ust', 0.135), ('ust2', 0.12))
DUV = 'siva_krem'
TRIM = 'tas_acik'


def nc_of(a, b):
    e = (b - a).normalized()
    return e, V(e.y, -e.x)


# ---------------------------------------------------------------- facades
def kat_cephe(a, b, z0, H, n, tur):
    """one storey a->b in n bays. alt: rusticated stone, segmental-arched windows with keystones; ust: framed windows
    with a corniced hood on consoles; ust2: framed windows with sills; kule: like ust with a triangular hood"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e, nc = nc_of(a, b)
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        W = (q - p).length
        if tur == 'alt':
            _, _, _, L = y.kemerli(p, q, z0, H, ('tas', 'tas_koyu', TRIM, 'cam'), v0=0.035, en=0.42, ust=0.03, derin=0.02, k_say=6, sivri=0,
                                   cerceve=(0.006, TRIM))
            kutu(y, L(W / 2 - 0.006, H - 0.03 - 0.002) + nc * 0.006, e, 0.012, 0.006, 0.018, TRIM, 'onsagsolust')
        else:
            u0, u1 = (0.3, 0.7) if tur != 'ust2' else (0.32, 0.68)
            v1 = H - (0.04 if tur != 'ust2' else 0.03)
            _, _, _, L = dikdortgen_acik(y, p, q, z0, H, u0, u1, 0.03, v1, (DUV, 'tas_koyu', TRIM, 'cam'), derin=0.018, cerceve=(0.006, TRIM))
            kutu(y, L(u0 - 0.06, 0.017) + nc * 0.009, e, W * (u1 - u0 + 0.12), 0.009, 0.006, TRIM, 'onsagsolust')   # sill
            if tur in ('ust', 'kule'):
                kutu(y, L(u0 - 0.07, v1 + 0.006) + nc * 0.01, e, W * (u1 - u0 + 0.14), 0.01, 0.007, TRIM, 'onsagsolust')   # hood
                for uu in (u0 - 0.04, u1 + 0.04):
                    kutu(y, L(uu, v1 - 0.012) - e * 0.003 + nc * 0.007, e, 0.006, 0.007, 0.018, TRIM, 'onsagsol')        # consoles
            if tur == 'kule':
                A = L(u0 - 0.07, v1 + 0.013) + nc * 0.006; B = L(u1 + 0.07, v1 + 0.013) + nc * 0.006
                T = (A + B) / 2 + Z * 0.02
                y.yuz_yon([A, B, T], TRIM, nc)
                for pp, qq in ((B, T), (T, A)):
                    y.yuz_yon([pp, qq, qq - nc * 0.006, pp - nc * 0.006], TRIM, (pp + qq) / 2 - (A + B) / 2)


def kanat(x0, x1, y0, y1, nx, ny, yanlar=(0, 1, 2, 3), cati=True):
    """a three-storey block; yanlar: which sides get facades (the others are hidden inside a neighbour)"""
    k = dikdortgen(x0, x1, y0, y1)
    say = [nx, ny, nx, ny]
    z = Z0
    for j, (tur, h) in enumerate(KATLAR):
        for i in range(4):
            if i in yanlar:
                kat_cephe(k[i], k[(i + 1) % 4], z, h, say[i], tur)
        z += h
        if j == 0:
            silme(y, k, z - 0.008, 0.016, 0.012, TRIM, 'duz')
        elif j < len(KATLAR) - 1:
            silme(y, k, z - 0.004, 0.008, 0.007, TRIM, 'duz')
    silme(y, k, Z0, 0.025, 0.012, 'tas_koyu', 'kaide')
    kornis(y, x0, x1, y0, y1, z, 0.014, 0.004, TRIM, 'duz')
    silme(y, k, z + 0.014, 0.018, 0.02, TRIM, 'tac')
    zt = z + 0.032
    if cati:
        cati_kirma(y, x0, x1, y0, y1, zt, 0.13, 0.035, 'kiremit', mahya='kiremit2', alt_key='ahsap_koyu')
    return zt


def kule(cx, cy, w):
    """a corner pavilion: one storey higher, quoins, a pyramid roof with a finial and dormers"""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2
    k = dikdortgen(x0, x1, y0, y1)
    z = Z0
    for j, (tur, h) in enumerate(KATLAR + (('ust2', 0.11),)):
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            for bb in range(3):   # bays hidden behind an adjoining wing (lower storeys) are plain wall
                p, q = a.lerp(b, bb / 3), a.lerp(b, (bb + 1) / 3)
                m = (p + q) / 2
                ic_x = abs(a.x - b.x) < 1e-6 and (a.x - cx) * cx < 0     # the side facing the yard in x
                ic_y = abs(a.y - b.y) < 1e-6 and (a.y - cy) * cy < 0
                gizli = j < len(KATLAR) and ((ic_x and WY - D < abs(m.y) < WY) or (ic_y and WX - D < abs(m.x) < WX))
                if gizli:
                    duz_duvar(y, p, q, z, z + h, 'tas' if j == 0 else DUV)
                else:
                    kat_cephe(p, q, z, h, 1, 'kule' if j == 1 else tur)
        z += h
        silme(y, k, z - 0.006, 0.012, 0.01, TRIM, 'duz')
    silme(y, k, Z0, 0.025, 0.014, 'tas_koyu', 'kaide')
    for p in k:   # quoins: alternating long and short blocks
        for q in range(int((z - Z0 - 0.15) / 0.04)):
            s = 0.034 if q % 2 == 0 else 0.024
            kutu_merkez(y, (p.x, p.y), s, s, 0.034, TRIM, z0=Z0 + 0.15 + q * 0.04 + 0.003)
        kutu_merkez(y, (p.x, p.y), 0.03, 0.03, 0.15, 'tas', z0=Z0)
    kornis(y, x0, x1, y0, y1, z, 0.014, 0.004, TRIM, 'duz')
    silme(y, k, z + 0.014, 0.02, 0.024, TRIM, 'tac')
    zt = z + 0.034
    tepe = cati_kirma(y, x0, x1, y0, y1, zt, 0.2, 0.04, 'kiremit', mahya='kiremit2', alt_key='ahsap_koyu')
    # an oeil-de-boeuf dormer on each face
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        e, nc = nc_of(a, b)
        m = a.lerp(b, 0.5) + nc * 0.005 + Z * (zt + 0.075)
        y.oculus(m - nc * 0.03, e, nc, 0.016, 'cam', TRIM, f=0.006, k=12)
        kutu(y, m - nc * 0.03 - e * 0.028 - Z * 0.055, e, 0.056, 0.05, 0.087, DUV, 'onsagsol')
        A, B = m - nc * 0.03 - e * 0.032 + Z * 0.032, m - nc * 0.03 + e * 0.032 + Z * 0.032
        T = (A + B) / 2 + Z * 0.03
        for pp, qq in ((A, T), (T, B)):
            y.yuz_yon([pp, qq, qq - nc * 0.055, pp - nc * 0.055], 'kiremit', Z + nc * 0.3)
        y.yuz_yon([A + Z * 0.0, B, T], TRIM, nc)
    kure(y, (cx, cy, tepe + 0.012), 0.012, 'bronz', n=8, kat=4)
    y.prizma((cx, cy), 0.003, tepe, tepe + 0.05, 'bronz', n=4)
    return zt


# ---------------------------------------------------------------- platform and the quadrangle
y.bolum('Zemin')
zemin(y, -1.2, 1.2, -1.14, 0.94, Z0, 'tas_koyu', basamak=(('on', 0.5),))

y.bolum('Kanatlar')
WX, WY = 1.1, 0.85          # outer half sizes
D = 0.3                     # wing depth
P = 0.4                     # corner pavilion width
pk = WX - P / 2 + 0.02, WY - P / 2 + 0.02
xi = WX - P + 0.02          # where the front / back wings meet the pavilions
yi = WY - P + 0.02
ZW = kanat(-xi, xi, -WY, -WY + D, 13, 3, yanlar=(0, 2))  # front
kanat(-xi, xi, WY - D, WY, 13, 3, yanlar=(0, 2))         # back
kanat(WX - D, WX, -yi, yi, 3, 9, yanlar=(1, 3))          # right
kanat(-WX, -WX + D, -yi, yi, 3, 9, yanlar=(1, 3))        # left

def baca(x, yy, z0, h=0.17):
    """a brick chimney through the ridge: a stone cap and two dark flues"""
    kutu_merkez(y, (x, yy), 0.036, 0.026, h, 'tugla', z0=z0)
    kutu_merkez(y, (x, yy), 0.044, 0.034, 0.01, TRIM, z0=z0 + h - 0.012)
    for s in (-1, 1):
        kutu_merkez(y, (x + s * 0.009, yy), 0.01, 0.01, 0.008, 'koyu', z0=z0 + h - 0.002)



def orta_alinlik(c, nc, W):
    """the central accent of a long outer facade: giant pilasters over the ground floor framing the middle bays and a
    pediment rising over the cornice (with a medallion), its roof running back into the wing roof. c: the facade
    centre on the wall line, nc: outward normal, W: the width of the framed bays"""
    c = V(c[0], c[1]); e = V(-nc.y, nc.x)
    zc = ZW - 0.032
    for u in (-W / 2, -W / 6, W / 6, W / 2):
        p = c + e * u
        kutu(y, p - e * 0.011 + nc * 0.009 + Z * (Z0 + 0.15), e, 0.022, 0.009, zc - Z0 - 0.15, TRIM, 'onsagsol')   # (depth goes back into the wall)
        kutu(y, p - e * 0.014 + nc * 0.013 + Z * (zc - 0.016), e, 0.028, 0.013, 0.016, TRIM, 'onsagsolust')         # capital
    # an entablature block over the pilasters, standing in front of the cornice and the eaves
    kutu(y, c - e * (W / 2 + 0.024) + nc * 0.04 + Z * zc, e, W + 0.048, 0.04, ZW + 0.004 - zc, TRIM, 'onsagsolust')
    A, B = c - e * (W / 2 + 0.024) + nc * 0.04, c + e * (W / 2 + 0.024) + nc * 0.04
    zt = alinlik(y, A, B, ZW + 0.004, 0.075, derin=0.12, key=TRIM, ic_key=DUV, c=0.008, cati_key='kiremit')
    y.oculus(c + nc * 0.0345 + Z * (ZW + 0.036), e, nc, 0.013, 'boya_yesil', 'altin', f=0.005, k=14)
    kure(y, (c.x + nc.x * 0.034, c.y + nc.y * 0.034, zt + 0.014), 0.01, TRIM, n=8, kat=4)


def cati_penceresi(c, nc):
    """a small gabled dormer on a wing roof just behind the eaves, its window towards nc"""
    c = V(c[0], c[1]); e = V(-nc.y, nc.x)
    w, d = 0.046, 0.075
    o = c - nc * 0.03
    z0, z1 = ZW + 0.03, ZW + 0.092
    k0 = o - e * (w / 2)
    y.yuz_yon([k0 + Z * z0, k0 + e * w + Z * z0, k0 + e * w + Z * z1, k0 + Z * z1], DUV, nc)
    for s_ in (0, 1):
        p = k0 + e * (w * s_)
        y.yuz_yon([p + Z * z0, p - nc * d + Z * z0, p - nc * d + Z * z1, p + Z * z1], DUV, e * (1 if s_ else -1))
    # the window (dark pane in a stone frame)
    m = o + nc * 0.002
    y.yuz_yon([m - e * 0.016 + Z * (z0 + 0.016), m + e * 0.016 + Z * (z0 + 0.016), m + e * 0.016 + Z * (z1 - 0.008), m - e * 0.016 + Z * (z1 - 0.008)], TRIM, nc)
    m = o + nc * 0.004
    y.yuz_yon([m - e * 0.011 + Z * (z0 + 0.021), m + e * 0.011 + Z * (z0 + 0.021), m + e * 0.011 + Z * (z1 - 0.013), m - e * 0.011 + Z * (z1 - 0.013)], 'cam', nc)
    # its gable roof, a little overhang, closed at the back
    L, R_ = k0 - e * 0.008 + nc * 0.012 + Z * (z1 - 0.004), k0 + e * (w + 0.008) + nc * 0.012 + Z * (z1 - 0.004)
    T = (L + R_) / 2 + Z * 0.03
    Dv = -nc * (d + 0.012)
    y.yuz_yon([L, T, T + Dv, L + Dv], 'kiremit', -e + Z)
    y.yuz_yon([T, R_, R_ + Dv, T + Dv], 'kiremit', e + Z)
    y.yuz_yon([k0 + nc * 0.001 + Z * z1, k0 + e * w + nc * 0.001 + Z * z1, (k0 + k0 + e * w) / 2 + nc * 0.001 + Z * (z1 + 0.023)], TRIM, nc)
    y.yuz_yon([L + Dv, R_ + Dv, T + Dv], DUV, -nc)


y.bolum('Orta alınlıklar ve çatı pencereleri')
orta_alinlik((0, WY), V(0, 1), 3 * (2 * xi) / 13)
for sx in (-1, 1):
    orta_alinlik((sx * WX, 0), V(sx, 0), 3 * (2 * yi) / 9)
for x in (-0.56, -0.44, 0.44, 0.56):
    cati_penceresi((x, -WY), V(0, -1))
for x in (-0.55, -0.4, 0.4, 0.55):
    cati_penceresi((x, WY), V(0, 1))
for sx in (-1, 1):
    for yy in (-0.34, -0.25, 0.25, 0.34):
        cati_penceresi((sx * WX, yy), V(sx, 0))

y.bolum('Bacalar')
for sy in (-1, 1):
    for x in (-0.48, -0.2, 0.2, 0.48):
        baca(x, sy * (WY - D / 2), ZW)
for sx in (-1, 1):
    for yy in (-0.26, 0.0, 0.26):
        baca(sx * (WX - D / 2), yy, ZW)

y.bolum('Köşe kuleleri')
for sx in (-1, 1):
    for sy in (-1, 1):
        kule(sx * pk[0], sy * pk[1], P)

# ---------------------------------------------------------------- the entrance block and its portico
y.bolum('Giriş bloğu: revak ve alınlık')
EX, EY0 = 0.3, -WY - 0.1
ek = [V(-EX, EY0), V(EX, EY0), V(EX, -WY), V(-EX, -WY)]
z = Z0
for j, (tur, h) in enumerate(KATLAR):
    if j == 0:
        for i in range(3):   # three arched doors
            p, q = ek[0].lerp(ek[1], i / 3), ek[0].lerp(ek[1], (i + 1) / 3)
            kapi(y, p, q, z, 0.5, h, ('tas', 'tas_koyu', TRIM, 'ahsap'), sivri=0, derin=0.03, cerceve=(0.008, TRIM))
    else:
        kat_cephe(ek[0], ek[1], z, h, 3, 'ust')
    for (a, b) in ((ek[1], ek[2]), (ek[3], ek[0])):
        kat_cephe(a, b, z, h, 1, tur)
    z += h
silme(y, ek, Z0, 0.025, 0.012, 'tas_koyu', 'kaide', kapali=False)
silme(y, ek, Z0 + 0.15 - 0.008, 0.016, 0.012, TRIM, 'duz', kapali=False)
ZE = z
# the giant order: six Ionic columns on pedestals over the ground floor
CY = EY0 - 0.035
for i in range(6):
    x = -EX + 0.03 + (2 * EX - 0.06) * i / 5
    kutu_merkez(y, (x, CY), 0.04, 0.04, 0.03, TRIM, z0=Z0 + 0.15)
    sutun(y, x, CY, Z0 + 0.18, ZE - 0.004, 0.014, 'mermer', 'iyon')
korkuluk_z = Z0 + 0.15
for i in range(5):   # balustrade between the pedestals
    x0 = -EX + 0.03 + (2 * EX - 0.06) * i / 5 + 0.02
    x1 = -EX + 0.03 + (2 * EX - 0.06) * (i + 1) / 5 - 0.02
    kutu(y, V(x0, CY - 0.008, korkuluk_z + 0.022), X, x1 - x0, 0.016, 0.006, TRIM, 'onarkaust')
    for k in range(int((x1 - x0) / 0.014)):
        xx = x0 + 0.007 + k * 0.014
        kutu_merkez(y, (xx, CY), 0.005, 0.005, 0.022, TRIM, z0=korkuluk_z, yuzler='onarkasagsol')
kutu(y, V(-EX - 0.01, CY - 0.022, Z0 + 0.15 - 0.002), X, 2 * EX + 0.02, 0.022, 0.004, TRIM, 'onsagsolust')
# entablature on the columns (with the inscription frieze), the soffit back to the wall
kutu(y, V(-EX - 0.012, CY - 0.024, ZE - 0.004), X, 2 * EX + 0.024, EY0 - CY + 0.024 + 0.002 + 0.0, 0.03, TRIM, 'onsagsolust')
kutu(y, V(-EX - 0.012, EY0, ZE - 0.004), X, 2 * EX + 0.024, 0.1, 0.03, TRIM, 'sagsolust')
y.yuz_yon([V(-0.14, CY - 0.0245, ZE + 0.004), V(0.14, CY - 0.0245, ZE + 0.004), V(0.14, CY - 0.0245, ZE + 0.02), V(-0.14, CY - 0.0245, ZE + 0.02)], 'boya_yesil', -Y)
for i in range(9):
    kutu(y, V(-0.12 + i * 0.03, CY - 0.0255, ZE + 0.008), X, 0.016, 0.001, 0.008, 'altin', 'on')
silme(y, [V(-EX - 0.012, CY - 0.024), V(EX + 0.012, CY - 0.024)], ZE + 0.026, 0.012, 0.01, TRIM, 'tac', kapali=False)
zp = alinlik(y, V(-EX - 0.02, CY - 0.034), V(EX + 0.02, CY - 0.034), ZE + 0.038, 0.125, derin=0.3, key=TRIM, ic_key='siva_krem',
             c=0.01, cati_key='kiremit')
boru(y, [V(0, CY - 0.034, zp + 0.012), V(0, CY + 0.266, zp + 0.012)], 0.007, 'kiremit2', n=6)   # ridge tiles
mc = V(0, CY - 0.04, ZE + 0.085)
y.oculus(mc, X, -Y, 0.024, 'boya_yesil', 'altin', f=0.006, k=16)
# crossed sabres beside the medallion
for sx in (-1, 1):
    boru(y, [mc + V(sx * 0.03, -0.002, -0.022), mc + V(sx * 0.075, -0.002, 0.0)], 0.0025, 'altin', n=4)
    boru(y, [mc + V(sx * 0.03, -0.002, 0.0), mc + V(sx * 0.085, -0.002, -0.012)], 0.0025, 'altin', n=4)
    kure(y, (sx * (EX + 0.02), CY - 0.03, ZE + 0.05), 0.012, TRIM, n=8, kat=4)
sancak(y, 0, CY - 0.03, zp, boy=0.2, en=0.13, yuk=0.075, aci=math.pi * 1.05)

# ---------------------------------------------------------------- the drill yard
y.bolum('Talim avlusu: harbiyeliler, top, bayrak')
ix, iy = WX - D, WY - D
y.yuz_yon([V(-ix, -iy, Z0 + 0.002), V(ix, -iy, Z0 + 0.002), V(ix, iy, Z0 + 0.002), V(-ix, iy, Z0 + 0.002)], 'toprak', Z)
# a paved walk round the yard
for (a, b) in ((V(-ix, -iy), V(ix, -iy)), (V(ix, -iy), V(ix, iy)), (V(ix, iy), V(-ix, iy)), (V(-ix, iy), V(-ix, -iy))):
    e, nc = nc_of(a, b)
    L = (b - a).length
    o = a - nc * 0.0
    y.yuz_yon([a + Z * (Z0 + 0.005), b + Z * (Z0 + 0.005), b - nc * 0.06 - e * 0.06 + Z * (Z0 + 0.005), a - nc * 0.06 + e * 0.06 + Z * (Z0 + 0.005)], 'zemin', Z)


def asker(x, yy, aci=-math.pi / 2, govde='lacivert'):
    """a cadet: legs, a dark tunic with a red sash, a head with a fez, a rifle at the shoulder"""
    with parca(y, (x, yy, Z0 + 0.002), aci + math.pi / 2):
        for s in (-1, 1):
            kutu_merkez(y, (s * 0.0035, 0), 0.005, 0.006, 0.022, 'koyu')
        kutu_merkez(y, (0, 0), 0.016, 0.009, 0.022, govde, z0=0.022)
        kutu_merkez(y, (0, 0), 0.0165, 0.0095, 0.003, 'boya_kirmizi', z0=0.026)
        for s in (-1, 1):
            kutu_merkez(y, (s * 0.0105, 0), 0.005, 0.006, 0.019, govde, z0=0.024)
        kure(y, (0, 0, 0.05), 0.0055, 'kum_acik', n=6, kat=3)
        y.prizma((0, 0), 0.0045, 0.0535, 0.06, 'boya_kirmizi', n=6)
        cubuk(y, V(0.011, -0.002, 0.03), V(0.011, -0.002, 0.07), 0.003, 'ahsap_koyu')


for r in range(3):
    for c in range(8):
        asker(-0.45 + c * 0.06, -0.02 + r * 0.07)
asker(-0.12, -0.12, math.pi / 2, 'koyu')                 # the drill sergeant facing the ranks
for r in range(2):
    for c in range(6):
        asker(0.2 + c * 0.06, 0.28 + r * 0.07, 0.0)


def top_arabali(x, yy, aci, L=0.17, r=0.02):
    """a field gun on a two-wheeled carriage, muzzle towards aci"""
    with parca(y, (x, yy, Z0), aci):
        R = 0.032
        for s in (-1, 1):
            cubuk(y, V(-L * 0.6, s * 0.018, 0.006), V(0.02, s * 0.018, R + 0.004), 0.01, 'ahsap', 0.026)
        cubuk(y, V(0, -0.045, R), V(0, 0.045, R), 0.008, 'demir')
        for s in (-1, 1):
            c = V(0, s * 0.038, R)
            boru(y, [c - Y * 0.005, c + Y * 0.005], R, 'demir', n=14)
            boru(y, [c - Y * 0.006, c + Y * 0.006], R * 0.84, 'ahsap_koyu', n=14)
            boru(y, [c - Y * 0.011, c + Y * 0.011], R * 0.25, 'demir', n=8)
        a, b = V(-L * 0.4, 0, R + 0.026), V(L * 0.62, 0, R + 0.034)
        boru(y, [a, b], r, 'bronz', n=12, r_son=r * 0.75)
        boru(y, [b - X * 0.025, b], r * 0.95, 'bronz', n=12, r_son=r * 1.05)
        kure(y, a - X * 0.012, r * 0.55, 'bronz', n=8, kat=4)
        y.yuz_yon([b + Y * (r * 0.6 * math.cos(TAU * i / 8)) + Z * (r * 0.6 * math.sin(TAU * i / 8)) + X * 0.001 for i in range(8)], 'koyu', X)


top_arabali(-0.3, 0.33, -math.pi / 2)
top_arabali(-0.12, 0.36, -math.pi / 2 - 0.15)
# the yard flagpole on a stepped base
for k, w in enumerate((0.08, 0.06, 0.04)):
    kutu_merkez(y, (0.42, -0.1), w, w, 0.012, 'tas_acik', z0=Z0 + 0.002 + k * 0.012)
sancak(y, 0.42, -0.1, Z0 + 0.038, boy=0.3, en=0.11, yuk=0.065, aci=math.pi * 0.75)
# trees in the yard corners
for sx in (-1, 1):
    for sy in (-1, 1):
        agac(y, sx * (ix - 0.1), sy * (iy - 0.1), Z0, boy=0.13)

# ---------------------------------------------------------------- outside the front
y.bolum('Ön meydan: toplar ve fenerler')
for sx in (-1, 1):
    top_arabali(sx * 0.42, -1.02, -math.pi / 2)
    for k in range(3):
        kure(y, (sx * 0.52 + (k - 1) * 0.022, -1.06, Z0 + 0.011), 0.011, 'demir', n=8, kat=4)
    kure(y, (sx * 0.52, -1.06, Z0 + 0.028), 0.011, 'demir', n=8, kat=4)
    for xx in (sx * 0.24, sx * 0.7):
        y.prizma((xx, -1.04), 0.004, Z0, Z0 + 0.12, 'demir', n=6)
        kutu_merkez(y, (xx, -1.04), 0.014, 0.014, 0.008, 'demir', z0=Z0)
        donel(y, (xx, -1.04), [(0.006, Z0 + 0.12), (0.011, Z0 + 0.128), (0.011, Z0 + 0.145), (0.0, Z0 + 0.156)], 'altin', n=6)

calistir(y, 'lm_harbiye')
