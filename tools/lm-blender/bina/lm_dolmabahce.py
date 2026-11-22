# Dolmabahce Palace (lm_dolmabahce): the neo-baroque Ottoman palace shortened into a U. The domed Muayede (ceremonial)
# hall in the middle with a columned, pedimented frontispiece; two-storey wings (Mabeyn and Harem) with pilasters,
# round-headed and pedimented framed windows, cornices and balustrades with urns; forward end pavilions; in front a
# formal garden with a fountain pool, the iron-railed boundary, the Imperial Gate (Saltanat Kapisi) and the clock tower.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.045
FH = 0.19            # storey height
DUV = 'siva'
PEN = (DUV, 'tas_koyu', 'tas_acik', 'cam')


# ---------------------------------------------------------------- helpers
def nc_of(a, b):
    e = (b - a).normalized()
    return e, V(e.y, -e.x)


def pilaster(p, e, nc, z0, h, w=0.022, d=0.008, key='mermer'):
    """a flat pilaster on the wall at p (e along the wall, nc out): base, shaft, capital"""
    o = p - e * (w / 2)
    kutu(y, o + nc * d + Z * z0, e, w, d, h, key, 'onsagsolust')
    kutu(y, o - e * 0.004 + nc * (d + 0.004) + Z * z0, e, w + 0.008, d + 0.004, 0.018, key, 'onsagsolust')
    kutu(y, o - e * 0.005 + nc * (d + 0.005) + Z * (z0 + h - 0.016), e, w + 0.01, d + 0.005, 0.016, key, 'onsagsolust')


def ucgen_alinlik(L, e, nc, u0, u1, v, h, key='mermer', c=0.006):
    """a small triangular window pediment over u0..u1 at height v (absolute), set c in front of the wall"""
    A, B = L(u0, 0) , L(u1, 0)
    A = V(A.x, A.y, v); B = V(B.x, B.y, v)
    T = (A + B) / 2 + Z * h
    o = nc * c
    y.yuz_yon([A + o, B + o, T + o], key, nc)
    for p, q in ((B, T), (T, A)):
        y.yuz_yon([p, q, q + o, p + o], key, (p + q) / 2 - (A + B) / 2 + Z * 0.001 + nc * 0)
    y.yuz_yon([A, B, B + o, A + o], key, -Z)


def kemerli_pencere(p, q, z0, H, kilit=True):
    W, e, nc, L = y.kemerli(p, q, z0, H, PEN, v0=0.03, en=0.4, ust=0.035, derin=0.02, k_say=6, sivri=0, cerceve=(0.007, 'mermer'))
    if kilit:   # keystone
        kutu(y, L(W / 2 - 0.007, H - 0.035 - 0.004) + nc * 0.006, e, 0.014, 0.006, 0.02, 'mermer', 'onsagsolust')
    return W, e, nc, L


def cephe(a, b, z0, H, n, kat, ilk=True, son=True):
    """one storey of facade a->b in n bays: kat 'alt' round-headed windows, 'ust' square windows with alternating
    triangular / flat hoods, 'cati' small attic windows; pilasters between the bays"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e, nc = nc_of(a, b)
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        W = (q - p).length
        if kat == 'alt':
            kemerli_pencere(p, q, z0, H)
        elif kat == 'ust':
            _, _, _, L = dikdortgen_acik(y, p, q, z0, H, 0.31, 0.69, 0.04, H - 0.055, PEN, derin=0.02, cerceve=(0.007, 'mermer'))
            # sill ledge
            kutu(y, L(0.31 - 0.1, 0.04 - 0.013) + nc * 0.01, e, W * 0.58, 0.01, 0.006, 'mermer', 'onsagsolust')
            vh = z0 + H - 0.055 + 0.007
            if k % 2 == 0:
                ucgen_alinlik(lambda u, v: p + e * (u * W), e, nc, 0.26 - 0.0, 0.74, vh + 0.004, 0.022)
            kutu(y, L(0.26, H - 0.055 + 0.007) + nc * 0.008, e, W * 0.48, 0.008, 0.005, 'mermer', 'onsagsolust')
        else:
            dikdortgen_acik(y, p, q, z0, H, 0.36, 0.64, 0.015, H - 0.018, PEN, derin=0.012, cerceve=(0.005, 'mermer'))
    # pilasters on the bay lines (not at the ends: the corners get quoins)
    for k in range(1, n):
        pp = a.lerp(b, k / n)
        if kat == 'cati':
            kutu(y, pp - e * 0.008 + nc * 0.005 + Z * z0, e, 0.016, 0.005, H, 'mermer', 'onsagsolust')
        else:
            pilaster(pp, e, nc, z0, H)


def blok(x0, x1, y0, y1, n, katlar, korkuluklu=True, cati_h=0.05, yanlar=None, arka=True):
    """a palace block: storeys given as a list of kinds, string courses, a crowning cornice, quoins, a balustrade
    with urns and a low lead hipped roof behind it. n = (bays along x, bays along y). Returns the cornice top z"""
    k = dikdortgen(x0, x1, y0, y1)
    sayi = [n[0], n[1], n[0], n[1]]
    z = Z0
    kornis(y, x0, x1, y0, y1, Z0, 0.035, 0.01, 'mermer', 'kaide')
    for j, kat in enumerate(katlar):
        h = FH if kat != 'cati' else 0.075
        for i in range(4):
            if (yanlar is not None and i not in yanlar):
                duz_duvar(y, k[i], k[(i + 1) % 4], z, z + h, DUV)
                continue
            cephe(k[i], k[(i + 1) % 4], z, h, sayi[i], kat)
        z += h
        if j < len(katlar) - 1:
            kornis(y, x0, x1, y0, y1, z - 0.006, 0.012, 0.01, 'mermer', 'duz')
    # entablature: frieze band and crowning cornice
    kornis(y, x0, x1, y0, y1, z, 0.016, 0.004, 'tas_acik', 'duz')
    silme(y, k, z + 0.016, 0.02, 0.022, 'mermer', 'tac')
    zt = z + 0.036
    for p in k:   # quoins
        kutu_merkez(y, (p.x, p.y), 0.034, 0.034, z - Z0, 'mermer', z0=Z0)
    y.yuz_yon([V(p.x, p.y, zt) for p in disa(k, 0.022)], 'kursun', Z)
    if cati_h:
        ic = disa(k, -0.035)
        cati_kirma(y, ic[0].x, ic[1].x, ic[0].y, ic[2].y, zt, cati_h, 0.0, 'kursun', alt_key='kursun', kalinlik=0.002)
    if korkuluklu:
        korkuluk(disa(k, 0.012), zt, 0.045)
    return zt


def vazo(x, yy, z, s=1.0, key='mermer'):
    """an urn finial on a pier"""
    donel(y, (x, yy), [(0, z), (0.009 * s, z), (0.006 * s, z + 0.006 * s), (0.011 * s, z + 0.014 * s), (0.01 * s, z + 0.022 * s),
                       (0.005 * s, z + 0.026 * s), (0.007 * s, z + 0.029 * s), (0.002 * s, z + 0.036 * s), (0, z + 0.04 * s)], key, n=6)


def baca(x, yy, z, w=0.034, d=0.022, h=0.1):
    """a stuccoed chimney stack rising through the roof: a moulded cap and dark flues"""
    kutu_merkez(y, (x, yy), w, d, h, DUV, z0=z)
    kutu_merkez(y, (x, yy), w + 0.008, d + 0.008, 0.008, 'mermer', z0=z + h - 0.016)
    kutu_merkez(y, (x, yy), w + 0.004, d + 0.004, 0.006, 'mermer', z0=z + h - 0.008)
    for s in (-1, 1):
        kutu_merkez(y, (x + s * w * 0.22, yy), 0.008, 0.008, 0.008, 'koyu', z0=z + h - 0.002)


def korkuluk(kose, z, h, kapali=True, key='mermer', aralik=0.025, ayak=0.16, vazolu=True):
    """a balustrade along a CCW polygon (or polyline): plinth, box balusters, a top rail, piers with urns"""
    m = len(kose)
    for i in range(m if kapali else m - 1):
        a, b = V(kose[i].x, kose[i].y), V(kose[(i + 1) % m].x, kose[(i + 1) % m].y)
        L = (b - a).length
        e, nc = nc_of(a, b)
        t = 0.016
        kutu(y, a + nc * (t / 2) + Z * z, e, L, t, 0.01, key, 'onarkaust')
        kutu(y, a + nc * (t / 2 + 0.002) + Z * (z + h - 0.008), e, L, t + 0.004, 0.008, key, 'onarkaustsagsol')
        np = max(1, int(round(L / ayak)))
        for j in range(np + 1):
            pp = a.lerp(b, j / np)
            kutu_merkez(y, (pp.x, pp.y), 0.022, 0.022, h + 0.006, key, z0=z, aci=math.atan2(e.y, e.x))
            if vazolu and (j % 2 == 0 or j == np):
                vazo(pp.x, pp.y, z + h + 0.006, 0.9)
        nb = int(L / aralik)
        for j in range(nb):
            u = (j + 0.5) / nb * L
            pp = a + e * u
            if min(abs(u - L * jj / np) for jj in range(np + 1)) < 0.016: continue
            kutu_merkez(y, (pp.x, pp.y), 0.006, 0.006, h - 0.018, key, z0=z + 0.01, aci=math.atan2(e.y, e.x), yuzler='onarkasagsol')


def demir_parmaklik(a, b, z, h, ayak=0.14, vazo_adim=1):
    """an iron railing between marble piers with urns, on a low marble kerb"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e, nc = nc_of(a, b)
    L = (b - a).length
    kutu(y, a + nc * 0.012 + Z * z, e, L, 0.024, 0.025, 'mermer', 'onarkaust')
    np = max(1, int(round(L / ayak)))
    for j in range(np + 1):
        pp = a.lerp(b, j / np)
        kutu_merkez(y, (pp.x, pp.y), 0.032, 0.032, h, 'mermer', z0=z, aci=math.atan2(e.y, e.x))
        kutu_merkez(y, (pp.x, pp.y), 0.04, 0.04, 0.008, 'mermer', z0=z + h, aci=math.atan2(e.y, e.x))
        if j % vazo_adim == 0 or j == np: vazo(pp.x, pp.y, z + h + 0.008, 1.0)
    for j in range(np):
        p0, p1 = a.lerp(b, j / np) + e * 0.016, a.lerp(b, (j + 1) / np) - e * 0.016
        Lj = (p1 - p0).length
        for rz in (z + 0.035, z + h - 0.014):
            cubuk(y, p0 + Z * rz, p1 + Z * rz, 0.004, 'demir')
        nb = int(Lj / 0.012)
        for q in range(1, nb):
            pp = p0.lerp(p1, q / nb)
            for sg in (1, -1):
                y.yuz_yon([pp - e * 0.0013 + nc * (sg * 0.001) + Z * (z + 0.025), pp + e * 0.0013 + nc * (sg * 0.001) + Z * (z + 0.025),
                           pp + e * 0.0013 + nc * (sg * 0.001) + Z * (z + h - 0.006), pp - e * 0.0013 + nc * (sg * 0.001) + Z * (z + h - 0.006)], 'demir', nc * sg)
            y.yuz_yon([pp - e * 0.003 + nc * 0.002 + Z * (z + h - 0.006), pp + e * 0.003 + nc * 0.002 + Z * (z + h - 0.006), pp + Z * (z + h + 0.002)], 'altin', nc)
            y.yuz_yon([pp - e * 0.003 - nc * 0.002 + Z * (z + h - 0.006), pp + e * 0.003 - nc * 0.002 + Z * (z + h - 0.006), pp + Z * (z + h + 0.002)], 'altin', -nc)


# ---------------------------------------------------------------- platform
y.bolum('Zemin')
zemin(y, -1.16, 1.16, -0.98, 0.82, Z0, 'tas_koyu', basamak=(('on', 0.36),), n_basamak=3)

# ---------------------------------------------------------------- the wings
y.bolum('Kanatlar (Mabeyn ve Harem)')
WY0, WY1 = 0.12, 0.6
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.38, sx * 0.8))
    zw = blok(x0, x1, WY0, WY1, (4, 4), ['alt', 'ust'], cati_h=0.05)
    for xx in (x0 + 0.1, (x0 + x1) / 2, x1 - 0.1):
        for yy in (WY0 + 0.12, WY1 - 0.12):
            baca(xx, yy, zw)
# end pavilions, projecting forward, one storey higher (attic)
PV0, PV1 = -0.34, 0.66
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.8, sx * 1.1))
    zt = blok(x0, x1, PV0, PV1, (2, 6), ['alt', 'ust', 'cati'], cati_h=0.06)
    for yy in (PV0 + 0.2, (PV0 + PV1) / 2, PV1 - 0.2):
        baca((x0 + x1) / 2, yy, zt)
    # a pediment on the pavilion's garden front
    xc = (x0 + x1) / 2
    alinlik(y, V(x0 + 0.02, PV0 - 0.012), V(x1 - 0.02, PV0 - 0.012), zt, 0.06, derin=0.08, key='mermer', ic_key='tas_acik', c=0.008, cati_key='kursun')
    y.oculus(V(xc, PV0 - 0.0185, zt + 0.022), X, -Y, 0.014, 'altin', 'mermer', f=0.004)

# ---------------------------------------------------------------- the Muayede hall
y.bolum('Muayede salonu')
MX, MY0, MY1 = 0.38, 0.0, 0.74
ZM = blok(-MX, MX, MY0, MY1, (6, 6), ['alt', 'ust', 'cati'], korkuluklu=True, cati_h=0)
# frontispiece: projecting, with two storeys of Corinthian columns and a pediment
FX = 0.22
FY0 = MY0 - 0.07
y.bolum('Ön cephe: sütunlar ve alınlık')
fk = [V(-FX, FY0), V(FX, FY0), V(FX, MY0), V(-FX, MY0)]
for j, kat in enumerate(('alt', 'ust')):
    z = Z0 + j * FH
    cephe(fk[0], fk[1], z, FH, 3, kat)
    duz_duvar(y, fk[1], fk[2], z, z + FH, DUV)
    duz_duvar(y, fk[3], fk[0], z, z + FH, DUV)
zf = Z0 + 2 * FH
silme(y, fk, Z0, 0.035, 0.01, 'mermer', 'kaide', kapali=False)
y.yuz_yon([V(p.x, p.y, zf + 0.036) for p in fk], 'kursun', Z)
for j in range(2):
    z = Z0 + j * FH
    for i in range(4):
        x = -FX + 2 * FX * i / 3
        for dx in (0.0,):
            xx = max(-FX + 0.014, min(FX - 0.014, x + dx))
            kutu_merkez(y, (xx, FY0 - 0.026), 0.034, 0.034, 0.012, 'mermer', z0=z + (0.0 if j == 0 else 0.004))
            sutun(y, xx, FY0 - 0.026, z + 0.012 + (0 if j == 0 else 0.004), z + FH - 0.012, 0.011, 'mermer', 'korint', yiv=14)
    # entablature over each column row
    kutu(y, V(-FX - 0.01, FY0 - 0.046, z + FH - 0.014), X, 2 * FX + 0.02, 0.046 + 0.001, 0.02, 'mermer', 'onsagsolust')
    silme(y, [V(-FX - 0.01, FY0 - 0.046), V(FX + 0.01, FY0 - 0.046)], z + FH + 0.002, 0.01, 0.008, 'mermer', 'tac', kapali=False)
# balcony railing at the upper floor
korkuluk([V(-FX - 0.01, FY0 - 0.046), V(FX + 0.01, FY0 - 0.046)], Z0 + FH + 0.012, 0.032, kapali=False, vazolu=False, ayak=0.14)
alinlik(y, V(-FX - 0.02, FY0 - 0.05), V(FX + 0.02, FY0 - 0.05), zf + 0.012, 0.1, derin=0.12, key='mermer', ic_key='tas_acik', c=0.01,
        cati_key='kursun')
# the tympanum: a gilt Ottoman coat of arms (a medallion with rays)
mc = V(0, FY0 - 0.056, zf + 0.05)
y.oculus(mc, X, -Y, 0.022, 'boya_yesil', 'altin', f=0.006, k=16)
for i in range(10):
    t = math.pi * (0.08 + 0.84 * i / 9)
    d = X * math.cos(t) + Z * math.sin(t)
    q = d.cross(-Y).normalized()
    p0, p1 = mc + d * 0.03 - Y * 0.003, mc + d * 0.042 - Y * 0.003
    y.yuz_yon([p0 - q * 0.002, p0 + q * 0.002, p1 + q * 0.0008, p1 - q * 0.0008], 'altin', -Y)
for sx in (-1, 1):
    vazo(sx * (FX + 0.01), FY0 - 0.04, zf + 0.04, 1.2)

# the dome: a square drum base with corner urns, a drum with round windows and pilasters, the lead dome, a lantern
y.bolum('Muayede kubbesi')
DC = (0, (MY0 + MY1) / 2)
RD = 0.27
kutu_merkez(y, DC, 2 * RD + 0.06, 2 * RD + 0.06, 0.02, 'mermer', z0=ZM)
zd = ZM + 0.02
ND = 20
dk = cokgen(DC, RD, ND)
for i in range(ND):
    a, b = dk[i], dk[(i + 1) % ND]
    duz_duvar(y, a, b, zd, zd + 0.075, DUV)
    e, nc = nc_of(a, b)
    if i % 2 == 0:
        y.oculus(a.lerp(b, 0.5) + Z * (zd + 0.04), e, nc, 0.018, 'cam', 'mermer', f=0.005)
    else:
        m = a.lerp(b, 0.5)
        kutu(y, m - e * 0.009 + nc * 0.007 + Z * zd, e, 0.018, 0.007, 0.075, 'mermer', 'onsagsolust')
halka_kornis(y, DC, RD, zd, 0.012, 0.008, ND, 'mermer', profil='kaide')
halka_kornis(y, DC, RD, zd + 0.075, 0.018, 0.018, ND, 'mermer', profil='tac')
t = y.kubbe(DC, RD + 0.008, zd + 0.093, 0.2, 'kursun', n=48, kat=16)
# ribs on the dome
for i in range(16):
    a = TAU * i / 16
    pts = [V(DC[0] + (RD + 0.012) * math.cos(math.pi / 2 * k / 8) * math.cos(a), DC[1] + (RD + 0.012) * math.cos(math.pi / 2 * k / 8) * math.sin(a),
             zd + 0.093 + 0.2 * (RD + 0.012) / (RD + 0.008) * math.sin(math.pi / 2 * k / 8) * 0.985) for k in range(8)]
    boru(y, pts, 0.004, 'tas_acik', n=4, kapat=False)
# lantern
zl = t.z - 0.012
lk = cokgen(DC, 0.045, 8, math.pi / 8)
for i in range(8):
    y.kemerli(lk[i], lk[(i + 1) % 8], zl, 0.05, ('mermer', 'tas_koyu', 'tas_acik', 'cam'), v0=0.01, en=0.5, ust=0.008, derin=0.006, k_say=4, sivri=0)
halka_kornis(y, DC, 0.045, zl + 0.05, 0.008, 0.008, 8, 'mermer', kat=math.pi / 8, profil='tac')
t2 = y.kubbe(DC, 0.05, zl + 0.058, 0.035, 'kursun', n=24, kat=6)
alem(y, DC[0], DC[1], t2.z, 1.1)
# corner urns on the roof
for sx in (-1, 1):
    for sy in (-1, 1):
        vazo(sx * (MX - 0.05), DC[1] + sy * (MX - 0.05), ZM, 1.6)

# ---------------------------------------------------------------- garden
y.bolum('Bahçe ve havuz')
GY0, GY1 = -0.86, -0.16
for sx in (-1, 1):   # lawns with box hedges
    for (yy0, yy1) in ((GY0 + 0.07, -0.52), (-0.42, GY1)):
        x0, x1 = sorted((sx * 0.13, sx * 0.72))
        y.yuz_yon([V(x0, yy0, Z0 + 0.004), V(x1, yy0, Z0 + 0.004), V(x1, yy1, Z0 + 0.004), V(x0, yy1, Z0 + 0.004)], 'cimen', Z)
        for p, q in ((V(x0, yy0), V(x1, yy0)), (V(x1, yy0), V(x1, yy1)), (V(x1, yy1), V(x0, yy1)), (V(x0, yy1), V(x0, yy0))):
            e, nc = nc_of(p, q)
            kutu(y, p + nc * 0.006 + Z * Z0, e, (q - p).length, 0.012, 0.018, 'boya_yesil', 'onarkaust')
        for xx in (x0 + 0.07, x1 - 0.07):
            agac(y, xx, (yy0 + yy1) / 2, Z0, boy=0.13, tur='servi')
        agac(y, (x0 + x1) / 2, (yy0 + yy1) / 2, Z0, boy=0.1)
# the pool and fountain
PC = (0, -0.47)
donel(y, PC, [(0.0, Z0 + 0.012), (0.1, Z0 + 0.012), (0.1, Z0), (0.12, Z0), (0.12, Z0 + 0.025), (0.108, Z0 + 0.025), (0.108, Z0 + 0.012)], 'mermer', n=32)
y.yuz_yon([V(p.x, p.y, Z0 + 0.018) for p in cokgen(PC, 0.108, 32)], 'su', Z)
donel(y, PC, [(0.012, Z0 + 0.018), (0.012, Z0 + 0.06), (0.04, Z0 + 0.065), (0.045, Z0 + 0.075), (0.0, Z0 + 0.075)], 'mermer', n=16)
y.yuz_yon([V(p.x, p.y, Z0 + 0.0755) for p in cokgen(PC, 0.038, 16)], 'su', Z)
donel(y, PC, [(0.006, Z0 + 0.075), (0.006, Z0 + 0.1), (0.018, Z0 + 0.105), (0.0, Z0 + 0.11)], 'mermer', n=12)
# lamp posts along the way
for sx in (-1, 1):
    for yy in (-0.78, -0.2):
        x = sx * 0.1
        y.prizma((x, yy), 0.004, Z0, Z0 + 0.11, 'demir', n=6)
        kutu_merkez(y, (x, yy), 0.014, 0.014, 0.006, 'demir', z0=Z0)
        donel(y, (x, yy), [(0.006, Z0 + 0.11), (0.011, Z0 + 0.118), (0.011, Z0 + 0.134), (0.0, Z0 + 0.145)], 'altin', n=6)

# ---------------------------------------------------------------- the front: railing, Imperial Gate
y.bolum('Parmaklık ve Saltanat Kapısı')
FY = -0.92
demir_parmaklik(V(-1.12, FY), V(-0.2, FY), Z0, 0.085)
demir_parmaklik(V(0.2, FY), V(1.12, FY), Z0, 0.085)
demir_parmaklik(V(-1.12, PV0 - 0.02), V(-1.12, FY), Z0, 0.085)
demir_parmaklik(V(1.12, FY), V(1.12, PV0 - 0.02), Z0, 0.085)
# the Bosphorus quay behind the palace: a marble kerb with the iron sea railing and mooring bollards
QY = 0.79
demir_parmaklik(V(1.12, QY), V(-1.12, QY), Z0, 0.07, ayak=0.16, vazo_adim=2)
for xx in (-0.9, -0.45, 0.45, 0.9):
    donel(y, (xx, QY - 0.06), [(0.0, Z0), (0.011, Z0), (0.009, Z0 + 0.02), (0.013, Z0 + 0.026), (0.0, Z0 + 0.03)], 'demir', n=8)
# Saltanat Kapisi: a round arch between paired Corinthian columns on pedestals, an entablature, a curved attic with
# the tughra, urns
GX, GD, GH = 0.2, 0.08, 0.24
gy0, gy1 = FY - GD / 2, FY + GD / 2
y.kemerli(V(-GX, gy0), V(GX, gy0), Z0, GH, ('mermer', 'tas_koyu', 'tas_acik', 'demir'), v0=0, en=0.42, ust=0.06, derin=GD * 0.45, k_say=12, sivri=0,
          cerceve=(0.012, ['altin', 'mermer']))
y.kemerli(V(GX, gy1), V(-GX, gy1), Z0, GH, ('mermer', 'tas_koyu', 'tas_acik', 'demir'), v0=0, en=0.42, ust=0.06, derin=GD * 0.45, k_say=12, sivri=0,
          cerceve=(0.012, 'mermer'))
duz_duvar(y, V(GX, gy0), V(GX, gy1), Z0, Z0 + GH, 'mermer')
duz_duvar(y, V(-GX, gy1), V(-GX, gy0), Z0, Z0 + GH, 'mermer')
for sy, yy in ((-1, gy0), (1, gy1)):
    for sx in (-1, 1):
        for dx in (0.035, 0.085):
            x = sx * (GX - dx)
            kutu_merkez(y, (x, yy + sy * 0.018), 0.034, 0.034, 0.045, 'mermer', z0=Z0)
            sutun(y, x, yy + sy * 0.018, Z0 + 0.045, Z0 + GH - 0.02, 0.012, 'mermer', 'korint', yiv=12)
    kutu(y, V(-GX - 0.012, yy - (0.04 if sy < 0 else 0), Z0 + GH - 0.02), X, 2 * GX + 0.024, 0.04, 0.026, 'mermer', 'onarkasagsolust')
silme(y, dikdortgen(-GX - 0.012, GX + 0.012, gy0 - 0.04, gy1 + 0.04), Z0 + GH + 0.006, 0.014, 0.008, 'mermer', 'tac')
y.yuz_yon([V(p.x, p.y, Z0 + GH + 0.006) for p in dikdortgen(-GX - 0.012, GX + 0.012, gy0 - 0.04, gy1 + 0.04)], 'mermer', Z)
# the attic: a segmental crest with the tughra
za = Z0 + GH + 0.02
ap = [(-0.13, 0.0)] + [(0.13 * math.cos(math.pi - math.pi * k / 10), 0.03 + 0.05 * math.sin(math.pi * k / 10)) for k in range(11)] + [(0.13, 0.0)]
CT = 0.016   # the crest is a thin marble wall standing on the cornice, framed by a moulded edge
on = [V(u, FY - CT, za + v) for u, v in ap]
ar = [V(u, FY + CT, za + v) for u, v in ap]
kutu(y, V(-0.14, FY - CT - 0.006, za - 0.014), X, 0.28, 2 * CT + 0.012, 0.014, 'mermer', 'onarkasagsolust')   # its base course
y.yuz_yon(on, 'mermer', -Y)
y.yuz_yon(ar, 'mermer', Y)
for k in range(len(ap) - 1):
    y.yuz_yon([on[k], on[k + 1], ar[k + 1], ar[k]], 'mermer', (on[k] + on[k + 1]) / 2 - V(0, gy0, za))
for sy in (-1, 1):   # the moulded edge of the crest, front and back, ending in volutes
    kenar = [V(u, FY + sy * CT, za + v + 0.003) for u, v in ap[1:-1]]
    boru(y, kenar, 0.006, 'mermer', n=6)
    for sx in (-1, 1):
        kure(y, (sx * 0.13, FY + sy * (CT - 0.002), za + 0.03), 0.011, 'mermer', n=10, kat=5)
y.yuz_yon([V(-0.07, FY - CT - 0.003, za + 0.012), V(0.07, FY - CT - 0.003, za + 0.012), V(0.07, FY - CT - 0.003, za + 0.06), V(-0.07, FY - CT - 0.003, za + 0.06)], 'boya_yesil', -Y)
for zz_ in (za + 0.009, za + 0.06):   # gilt frame of the tughra panel
    kutu(y, V(-0.074, FY - CT - 0.005, zz_), X, 0.148, 0.005, 0.004, 'altin', 'onust')
tg = V(0, FY - CT - 0.006, za + 0.036)
y.oculus(tg, X, -Y, 0.016, 'altin', 'altin', f=0.003, k=12)
for sx in (-1, 1):
    boru(y, [tg + V(sx * 0.01, 0, -0.004), tg + V(sx * 0.03, 0, 0.004), tg + V(sx * 0.05, 0, 0.0)], 0.003, 'altin', n=4)
    vazo(sx * (GX - 0.03), gy0 - 0.02, Z0 + GH + 0.02, 1.3)
    vazo(sx * (GX - 0.03), gy1 + 0.02, Z0 + GH + 0.02, 1.3)
# gilded crown on the crest and the banner
kure(y, (0, FY, za + 0.084), 0.012, 'altin', n=10, kat=5)
sancak(y, 0, FY, za + 0.094, boy=0.2, en=0.12, yuk=0.07, aci=math.pi * 0.95)

# ---------------------------------------------------------------- the clock tower
y.bolum('Saat kulesi')
SX, SY = 0.86, -0.62
zz = Z0
kutu_merkez(y, (SX, SY), 0.17, 0.17, 0.03, 'mermer', z0=zz)
zz += 0.03
for i, (h, w) in enumerate(((0.16, 0.14), (0.14, 0.125), (0.12, 0.11), (0.08, 0.09))):
    k = dikdortgen(SX - w / 2, SX + w / 2, SY - w / 2, SY + w / 2)
    for j in range(4):
        a, b = k[j], k[(j + 1) % 4]
        e, nc = nc_of(a, b)
        if i == 0:
            y.kemerli(a, b, zz, h, (DUV, 'tas_koyu', 'tas_acik', 'ahsap' if j == 0 else 'cam'), v0=0 if j == 0 else 0.04, en=0.42, ust=0.03,
                      derin=0.016, k_say=8, sivri=0, cerceve=(0.007, 'mermer'))
        elif i == 1:
            dikdortgen_acik(y, a, b, zz, h, 0.32, 0.68, 0.03, h - 0.04, PEN, derin=0.016, cerceve=(0.006, 'mermer'))
            ucgen_alinlik(lambda u, v, a=a, b=b: a + (b - a) * u, e, nc, 0.27, 0.73, zz + h - 0.03, 0.02)
        elif i == 2:
            duz_duvar(y, a, b, zz, zz + h, DUV)
            m = a.lerp(b, 0.5) + Z * (zz + h * 0.5)
            y.oculus(m, e, nc, w * 0.36, 'beyaz', 'altin', f=0.006, k=20)
            for t, Lh, wd in ((math.radians(75), 0.55, 0.003), (math.radians(-10), 0.82, 0.002)):
                d = e * math.cos(t) + Z * math.sin(t); q = d.cross(nc).normalized()
                p0, p1 = m + nc * 0.005, m + d * (w * 0.36 * Lh) + nc * 0.005
                y.yuz_yon([p0 - q * wd, p0 + q * wd, p1 + q * wd * 0.4, p1 - q * wd * 0.4], 'koyu', nc)
            for hh in range(12):
                t = TAU * hh / 12
                d = e * math.cos(t) + Z * math.sin(t); q = d.cross(nc).normalized()
                p0, p1 = m + d * (w * 0.36 * 0.78) + nc * 0.0045, m + d * (w * 0.36 * 0.93) + nc * 0.0045
                y.yuz_yon([p0 - q * 0.0018, p0 + q * 0.0018, p1 + q * 0.0018, p1 - q * 0.0018], 'koyu', nc)
        else:
            y.kemerli(a, b, zz, h, ('mermer', 'tas_koyu', 'tas_acik', 'koyu'), v0=0.012, en=0.5, ust=0.015, derin=0.012, k_say=8, sivri=0)
    for p in k:   # chamfered corner pilasters
        kutu_merkez(y, (p.x, p.y), 0.022, 0.022, h, 'mermer', z0=zz, aci=math.pi / 4)
    zz += h
    kornis(y, SX - w / 2, SX + w / 2, SY - w / 2, SY + w / 2, zz - 0.01, 0.014, 0.012, 'mermer', 'tac')
    y.yuz_yon([V(p.x, p.y, zz + 0.004) for p in k], 'tas_acik', Z)
    for p in k:
        if i < 3: vazo(p.x + (0.008 if p.x > SX else -0.008), p.y + (0.008 if p.y > SY else -0.008), zz + 0.004, 0.8)
t = y.kubbe((SX, SY), 0.05, zz + 0.004, 0.05, 'kursun', n=24, kat=7)
alem(y, SX, SY, t.z, 0.9)

calistir(y, 'lm_dolmabahce')
