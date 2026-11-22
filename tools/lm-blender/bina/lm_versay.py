# The Palace of Versailles (lm_versay): the stepped U of courts opening to the front (-y) - the Place d'Armes with
# the equestrian Louis XIV, the gilded Grille d'Honneur and Grille Royale, the Cour d'Honneur with the ministers'
# wings, the Cour Royale and the black-and-white Cour de Marbre framed by Louis XIII's brick-and-stone chateau
# under slate Mansart roofs, dormers and gilded ornaments; the Royal Chapel's tall roof; behind, the long flat-roofed
# garden front (rusticated ground floor, arched piano nobile, Ionic avant-corps, attic, balustrade with urns and
# statues), the Parterre d'Eau, the Latona stairs and fountain and the box-hedge parterres.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from frank_ek import *
from bina_ortak import calistir
import doku

# Versailles' lead flats a weathered grey rather than the stock pale blue
doku.MALZEME['kursun'] = ('kursun', (0.47, 0.495, 0.535), {})
doku.MALZEME['kursun2'] = ('kursun', (0.43, 0.455, 0.495), {})

y = Yapi()
R = random.Random(3)
Z0 = 0.04
TAS = 'kirec'                       # the pale cream limestone
PEN = (TAS, 'tas_koyu', 'tas_acik', 'cam')
H0, H1, H2 = 0.11, 0.15, 0.07       # garden front storeys: rusticated ground, piano nobile, attic
ZG = Z0 + H0 + H1 + H2              # the garden front's top (under the entablature)


def nc_of(a, b):
    a, b, L, e, nc = eksen(a, b)
    return e, nc


# ---------------------------------------------------------------- the garden front (stone, flat roof)
def bahce_cephesi(a, b, n, kose_bas=True, kose_son=True, onde=None):
    """a stretch of the garden front a->b in n bays: rusticated ground floor with arched windows, the piano nobile's
    tall arched windows with keystones between Ionic pilasters, the attic's square windows. onde: bay indexes of an
    avant-corps (columns before the piano nobile carrying statues on the balustrade)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e, nc = nc_of(a, b)
    W = (b - a).length / n
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        _, _, _, L = y.kemerli(p, q, Z0, H0, PEN, v0=0.008, en=0.46, ust=0.014, derin=0.012, k_say=4, sivri=0.0)
        kutu3(y, L(W / 2, H0 - 0.016) + nc * 0.003, e, nc, Z, 0.01, 0.006, 0.014, 'tas_acik', ('+x', '-x', '+y'))
        _, _, _, L = y.kemerli(p, q, Z0 + H0, H1, PEN, v0=0.004, en=0.5, ust=0.018, derin=0.012, k_say=6, sivri=0.0)
        kutu3(y, L(W / 2, H1 - 0.02) + nc * 0.003, e, nc, Z, 0.012, 0.006, 0.018, 'tas_acik', ('+x', '-x', '+y'))
        duz_duvar(y, p, q, Z0 + H0 + H1, Z0 + H0 + H1 + H2, TAS)
        kutu3(y, p.lerp(q, 0.5) + nc * 0.0015 + Z * (Z0 + H0 + H1 + H2 * 0.5 - 0.003), e, nc, Z, W * 0.34, 0.003, H2 - 0.03, 'cam', ('+y', '+z'))
    for k in range(n + 1):
        if (k == 0 and not kose_bas) or (k == n and not kose_son): continue
        pp = a.lerp(b, k / n)
        # a rusticated pier (two blocks), a pilaster with its capital, the attic strip
        ky = ('-y',) if k in (0, n) else ()   # (at a corner the block stands past the side wall: its back shows)
        kutu3(y, pp + nc * 0.003 + Z * (Z0 + H0 / 2), e, nc, Z, 0.024, 0.006, H0 - 0.012, 'tas_acik', ('+x', '-x', '+y') + ky)
        kutu3(y, pp + nc * 0.0025 + Z * (Z0 + H0 + H1 / 2), e, nc, Z, 0.018, 0.005, H1 - 0.004, 'tas_acik', ('+x', '-x', '+y') + ky)
        kutu3(y, pp + nc * 0.004 + Z * (Z0 + H0 + H1 - 0.012), e, nc, Z, 0.026, 0.008, 0.01, 'tas_acik', ('+x', '-x', '+y', '+z') + ky)
        kutu3(y, pp + nc * 0.0025 + Z * (Z0 + H0 + H1 + H2 / 2), e, nc, Z, 0.016, 0.005, H2, 'tas_acik', ('+x', '-x', '+y') + ky)
    if onde:
        us = sorted(set(round(u, 6) for k in onde for u in (k / n, (k + 1) / n)))
        for u in us:
            pp = a.lerp(b, u) + nc * 0.02
            kutu3(y, pp + Z * (Z0 + H0 + 0.012), e, nc, Z, 0.024, 0.024, 0.024, 'tas_acik', ('+x', '-x', '+y', '-y', '+z'))
            sutun_hafif(y, pp.x, pp.y, Z0 + H0 + 0.024, Z0 + H0 + H1, 0.0085, 'tas_acik', 'iyon', n=6)
            heykel(y, pp.x, pp.y, ZG + 0.034 + 0.004, 0.85, 'tas_acik', math.atan2(nc.y, nc.x) + math.pi / 2, n=4)
        # the ressaut of the entablature over the columns: one block per run of neighbouring bays (separate blocks
        # overlapped on the shared columns: coplanar faces flickered)
        kos = sorted(onde)
        runs, bas_ = [], kos[0]
        for i_, k in enumerate(kos):
            if i_ == len(kos) - 1 or kos[i_ + 1] != k + 1:
                runs.append((bas_, k)); bas_ = kos[i_ + 1] if i_ < len(kos) - 1 else None
        for k0, k1 in runs:
            p0, p1 = a.lerp(b, k0 / n) - e * 0.016, a.lerp(b, (k1 + 1) / n) + e * 0.016
            kutu3(y, (p0 + p1) / 2 + nc * 0.016 + Z * (Z0 + H0 + H1 + 0.006), e, nc, Z, (p1 - p0).length, 0.032, 0.012, 'tas_acik',
                  ('+x', '-x', '+y', '-y', '+z'))


def tas_blok(x0, x1, y0, y1, sayilar, onde=None, korkuluk=True):
    """a flat-roofed stone block of the garden front: its four sides (sayilar = bays per side, 0 = plain wall),
    string courses, entablature, a low lead roof behind a balustrade with urns and trophies"""
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        parcalar_ = sayilar[i] if isinstance(sayilar[i], list) else [(0.0, 1.0, sayilar[i])]
        for u0, u1, n in parcalar_:
            if n:
                bahce_cephesi(a.lerp(b, u0), a.lerp(b, u1), n, onde=(onde or {}).get(i))
            else:
                duz_duvar(y, a.lerp(b, u0), a.lerp(b, u1), Z0, ZG, TAS)
    kornis(y, x0, x1, y0, y1, Z0, 0.012, 0.008, 'tas_acik', 'kaide')
    kornis(y, x0, x1, y0, y1, Z0 + H0 - 0.006, 0.01, 0.008, 'tas_acik', 'duz')
    kornis(y, x0, x1, y0, y1, Z0 + H0 + H1 - 0.004, 0.008, 0.006, 'tas_acik', 'duz')
    kornis(y, x0, x1, y0, y1, ZG - 0.002, 0.014, 0.004, TAS, 'duz')
    silme(y, k, ZG + 0.012, 0.016, 0.018, 'tas_acik', 'tac')
    zt = ZG + 0.028
    ki = disa(k, -0.02)
    y.yuz_yon([V(p.x, p.y, zt) for p in disa(k, 0.018)], 'kursun', Z)
    kirma_basit(y, ki[0].x, ki[1].x, ki[0].y, ki[2].y, zt, 0.035, 'kursun', 'kursun2')
    if korkuluk:
        korkuluk_hafif(y, disa(k, 0.006), zt, 0.034, True, 'tas_acik', ayak=0.13, ust='vazo', ust_key='tas_acik', aralik=0.03, ust_adim=3)
    return zt


# ---------------------------------------------------------------- the brick-and-stone chateau
def tugla_cephe(a, b, z0, H, n, katlar=2, kapi=None):
    """a brick front a->b with n bays per storey: tall windows with stone surrounds and keystones, stone chains
    (vertical bands) between the bays, a stone string course; kapi: bay index of a door on the ground floor"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e, nc = nc_of(a, b)
    W = (b - a).length / n
    h = H / katlar
    for j in range(katlar):
        zz = z0 + j * h
        for k in range(n):
            p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
            if j == 0 and kapi == k:
                _, _, _, L = y.kemerli(p, q, zz, h, ('tugla', 'tas_koyu', 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.5, ust=0.014, derin=0.012, k_say=6,
                                       sivri=0.0, cerceve=(0.005, TAS))
            else:
                _, _, _, L = dikdortgen_acik(y, p, q, zz, h, 0.3, 0.7, 0.012 if j else 0.016, h - 0.02, ('tugla', 'tas_koyu', 'tas_acik', 'cam'),
                                             derin=0.01)
                kutu3(y, L(0.5, h - 0.012) + nc * 0.0035, e, nc, Z, (L(0.7, 0) - L(0.3, 0)).length + 0.01, 0.007, 0.014, TAS,
                      ('+y', '+z', '-z', '+x', '-x'))   # (the stone lintel with its keystone)
        silme(y, [a, b], zz + h - 0.004, 0.008, 0.006, TAS, 'duz', kapali=False)
    for k in range(n + 1):
        pp = a.lerp(b, k / n)
        kutu3(y, pp + nc * 0.002 + Z * (z0 + H / 2), e, nc, Z, 0.018, 0.004, H, TAS, ('+x', '-x', '+y') + (('-y',) if k in (0, n) else ()))


def tugla_blok(x0, x1, y0, y1, H, sayilar, h1=0.1, h2=0.035, lukarn_adim=2, kapilar=None, baca=True, yaldiz='altin', cephe_kosul=None):
    """a brick-and-stone range: brick fronts (sayilar bays per side, 0 = plain brick), quoins, a cornice, a slate
    Mansart roof with dormers over the bays, a gilt crest, chimneys. Returns the roof's top z"""
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        a, b = k[i], k[(i + 1) % 4]
        if sayilar[i]:
            tugla_cephe(a, b, Z0, H, sayilar[i], kapi=(kapilar or {}).get(i))
        else:
            duz_duvar(y, a, b, Z0, Z0 + H, 'tugla')
    kornis(y, x0, x1, y0, y1, Z0, 0.012, 0.006, TAS, 'kaide')
    for p in k:   # quoins
        for j in range(int(H / 0.07)):
            s = 0.022 if j % 2 == 0 else 0.016
            # (only the two outer faces and the top: the others are inside the walls)
            yz = ('sag' if p.x > (x0 + x1) / 2 else 'sol') + ('arka' if p.y > (y0 + y1) / 2 else 'on') + 'ust'
            kutu_merkez(y, (p.x, p.y), s, s, 0.062, TAS, z0=Z0 + 0.002 + j * 0.07, yuzler=yz)
    silme(y, k, Z0 + H - 0.004, 0.012, 0.012, TAS, 'tac')
    zt = Z0 + H + 0.008
    zb, kb, top = mansard(y, x0, x1, y0, y1, zt, h1, h2, 'arduvaz', 'kursun', egim=0.36, sacak=0.012, yaldiz=yaldiz)
    kk = (0.012 + 0.36 * h1) / h1
    for i in range(4):
        n = sayilar[i]
        if not n: continue
        a, b = disa(k, 0.012)[i], disa(k, 0.012)[(i + 1) % 4]
        e, nc = nc_of(a, b)
        L_ = (b - a).length
        for j in range(n):
            if j % lukarn_adim: continue
            u = (j + 0.5) / n
            if u * L_ < 0.035 or (1 - u) * L_ < 0.035: continue
            lukarn(y, a.lerp(b, u), e, nc, zt, 0.028, 0.045, kk, TAS, 'kursun', 'cam', yuvarlak=(abs(x0 + x1) < 0.3 and y0 > -0.2), yaldiz='altin')
    if yaldiz:   # a gilt crest along the ridge
        xs0, xs1, ys0, ys1 = kb
        if xs1 - xs0 > ys1 - ys0:
            cy = (ys0 + ys1) / 2
            for xx in [xs0 + (ys1 - ys0) / 2 + (xs1 - xs0 - (ys1 - ys0)) * t / 6 for t in range(7)]:
                kure(y, (xx, cy, top + 0.004), 0.004, yaldiz, n=4, kat=2)
        else:
            cx = (xs0 + xs1) / 2
            for yy in [ys0 + (xs1 - xs0) / 2 + (ys1 - ys0 - (xs1 - xs0)) * t / 6 for t in range(7)]:
                kure(y, (cx, yy, top + 0.004), 0.004, yaldiz, n=4, kat=2)
    if baca:
        L_ = max(x1 - x0, y1 - y0)
        nb = max(2, int(L_ / 0.18))
        for t in range(nb):
            f = (t + 0.5) / nb
            bx, by = ((x0 + (x1 - x0) * f, (y0 + y1) / 2) if x1 - x0 > y1 - y0 else ((x0 + x1) / 2, y0 + (y1 - y0) * f))
            kutu_merkez(y, (bx, by), 0.028, 0.02, top - zt + 0.03, 'tugla', z0=zt + 0.02)
            kutu_merkez(y, (bx, by), 0.034, 0.026, 0.008, TAS, z0=top + 0.044)
    return top


def parmaklik(a, b, z, h, ayak=0.1, yaldiz=0.5, key='demir'):
    """a wrought-iron railing a->b between stone piers, the bars' spearheads and a frieze gilded"""
    a, b, L, e, nc = eksen(a, b)
    np_ = max(1, int(round(L / ayak)))
    for j in range(np_ + 1):
        pp = a.lerp(b, j / np_)
        kutu3(y, pp + Z * (z + h * 0.55), e, nc, Z, 0.022, 0.022, h * 1.1, TAS, ('+x', '-x', '+y', '-y', '+z'))
        vazo(y, pp.x, pp.y, z + h * 1.1, 0.7, TAS, n=4)
    kutu3(y, a.lerp(b, 0.5) + Z * (z + 0.006), e, nc, Z, L, 0.02, 0.012, TAS, ('+y', '-y', '+z'))
    for rz in (z + 0.02, z + h - 0.008):
        cubuk(y, a + Z * rz, b + Z * rz, 0.003, 'altin' if rz > z + 0.03 else key)
    nbar = int(L / 0.016)
    for j in range(1, nbar):
        pp = a.lerp(b, j / nbar)
        if min(abs(j / nbar - jj / np_) for jj in range(np_ + 1)) * L < 0.014: continue
        kutu3(y, pp + Z * (z + 0.012 + (h - 0.012) / 2), e, nc, Z, 0.0022, 0.0022, h - 0.012, key, ('+x', '-x', '+y', '-y'))
        piramit_cati(y, (pp.x, pp.y), 0.0045, 0.0045, z + h, 0.008, 'altin')


# ---------------------------------------------------------------- ground
y.bolum('Zemin ve teraslar')
X0_, X1_ = -1.06, 1.06
YF, YT, YB = -1.12, 0.9, 1.2     # the front, the terrace's edge, the back
ZL = 0.015                        # the lower garden
kutu(y, V(X0_, YF, 0), X, X1_ - X0_, YT - YF, Z0, 'tas_koyu', 'onsagsol')
y.yuz_yon([V(X0_, YF, Z0), V(X1_, YF, Z0), V(X1_, YT, Z0), V(X0_, YT, Z0)], 'zemin', Z)
silme(y, [V(X0_, YT), V(X0_, YF), V(X1_, YF), V(X1_, YT)], Z0 - 0.008, 0.008, 0.006, 'tas_koyu', 'duz', kapali=False)
kutu(y, V(X0_, YT, 0), X, X1_ - X0_, YB - YT, ZL, 'tas_koyu', 'sagsolarka')
y.yuz_yon([V(X0_, YT, ZL), V(X1_, YT, ZL), V(X1_, YB, ZL), V(X0_, YB, ZL)], 'kum_acik', Z)
# the terrace's retaining wall and balustrade, with the Latona stair in the middle
SW = 0.34
for x0, x1 in ((X0_, -SW), (SW, X1_)):
    duz_duvar(y, V(x1, YT), V(x0, YT), ZL, Z0, TAS)
    korkuluk_hafif(y, [V(x1, YT - 0.008), V(x0, YT - 0.008)], Z0, 0.03, False, TAS, ayak=0.14, ust='vazo', ust_adim=2, aralik=0.03)
merdiven(y, (0, YT + 0.075), -math.pi / 2, 2 * SW, ZL, Z0, n=6, d=0.0125, key=TAS)
for sx in (-1, 1):
    kutu3(y, V(sx * (SW + 0.012), YT + 0.035, (ZL + Z0) / 2 + 0.01), X, Y, Z, 0.024, 0.08, Z0 - ZL + 0.02, TAS, ('+x', '-x', '+y', '-y', '+z'))
    vazo(y, sx * (SW + 0.012), YT + 0.07, Z0 + 0.016, 1.1, TAS, n=6)
# the courts: the Place d'Armes, Cour d'Honneur and Cour Royale paved, the Cour de Marbre in a marble checkerboard
y.yuz_yon([V(-0.14, -0.08, Z0 + 0.008), V(0.14, -0.08, Z0 + 0.008), V(0.14, 0.18, Z0 + 0.008), V(-0.14, 0.18, Z0 + 0.008)], 'mermer', Z)
duz_duvar(y, V(-0.14, -0.08), V(0.14, -0.08), Z0, Z0 + 0.008, 'mermer')
NK = 10
for i in range(NK):
    for j in range(9):
        if (i + j) % 2: continue
        x0, x1 = -0.14 + 0.28 * i / NK, -0.14 + 0.28 * (i + 1) / NK
        y0, y1 = -0.08 + 0.26 * j / 9, -0.08 + 0.26 * (j + 1) / 9
        y.yuz_yon([V(x0, y0, Z0 + 0.0105), V(x1, y0, Z0 + 0.0105), V(x1, y1, Z0 + 0.0105), V(x0, y1, Z0 + 0.0105)], 'koyu', Z)
for x0, x1, y0, y1 in ((-0.28, 0.28, -0.42, -0.08), (-0.58, 0.58, -0.82, -0.42)):
    for k in range(5):
        xx = x0 + (x1 - x0) * (k + 0.5) / 5
        y.yuz_yon([V(xx - 0.006, y0 + 0.01, Z0 + 0.002), V(xx + 0.006, y0 + 0.01, Z0 + 0.002), V(xx + 0.006, y1 - 0.01, Z0 + 0.002), V(xx - 0.006, y1 - 0.01, Z0 + 0.002)],
                  'tas_acik', Z)

# ---------------------------------------------------------------- the garden front
y.bolum('Bahçe cephesi')
# central block (with the Hall of Mirrors behind the middle of the garden side)
CY0, CY1 = 0.28, 0.62
zt_c = tas_blok(-0.5, 0.5, CY0, CY1, [0, [(0, 0.765, 0), (0.765, 1, 1)], 15, [(0, 0.235, 1), (0.235, 1, 0)]], onde={2: [1, 2, 6, 7, 8, 12, 13]})
# the two long wings
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.5, sx * 1.02))
    if sx < 0:
        tas_blok(x0, x1, 0.3, 0.54, [8, 0, 8, 3], onde={2: [3, 4]})
    else:
        tas_blok(x0, x1, 0.3, 0.54, [8, 3, 8, 0], onde={2: [3, 4]})

# ---------------------------------------------------------------- the old chateau round the Cour de Marbre and the Cour Royale wings
y.bolum('Mermer avlu (eski şato)')
HB = 0.25
# the back range (the King's apartment) with the balcony and clock
top_b = tugla_blok(-0.28, 0.28, 0.18, 0.28, HB, [7, 0, 0, 0], h1=0.11, h2=0.04, kapilar={0: 3})
# its central pavilion: a balcony on eight marble columns, a clock with Mars and Hercules, a higher roof
PX0, PX1 = -0.07, 0.07
for k_ in range(4):
    for s_ in (-1, 1):
        xx = s_ * (0.018 + 0.017 * k_)
        sutun_hafif(y, xx, 0.18 - 0.03, Z0 + 0.008, Z0 + HB * 0.5 - 0.004, 0.0065, 'kirmizi_tas', 'dor', bas_key=TAS, n=6)
kutu3(y, V(0, 0.18 - 0.024, Z0 + HB * 0.5), X, Y, Z, 0.15, 0.05, 0.01, TAS, ('+x', '-x', '+y', '-y', '+z', '-z'))
cubuk(y, V(-0.075, 0.18 - 0.048, Z0 + HB * 0.5 + 0.026), V(0.075, 0.18 - 0.048, Z0 + HB * 0.5 + 0.026), 0.004, 'altin')
for k_ in range(16):
    xx = -0.072 + 0.144 * k_ / 15
    kutu3(y, V(xx, 0.18 - 0.048, Z0 + HB * 0.5 + 0.017), X, Y, Z, 0.002, 0.002, 0.018, 'altin', ('+x', '-x', '+y', '-y'))
zc = Z0 + HB + 0.008
cz = zc + 0.11
y.oculus(V(0, 0.18 - 0.014, zc + 0.05), X, -Y, 0.024, 'beyaz', 'altin', f=0.006, k=16)
for t_ in range(12):
    an = TAU * t_ / 12
    d_ = X * math.cos(an) + Z * math.sin(an)
    q_ = d_.cross(-Y).normalized()
    p0 = V(0, 0.18 - 0.0175, zc + 0.05) + d_ * 0.026
    p1 = V(0, 0.18 - 0.0175, zc + 0.05) + d_ * (0.038 if t_ % 2 else 0.032)
    y.yuz_yon([p0 - q_ * 0.0025, p0 + q_ * 0.0025, p1], 'altin', -Y)
# the clock's pediment frame standing up from the roof, with two reclining figures
kutu3(y, V(0, 0.18 - 0.008, zc + 0.04), X, Y, Z, 0.12, 0.016, 0.08, TAS, ('+x', '-x', '-y', '+y', '+z'))
alinlik(y, V(-0.064, 0.18 - 0.016), V(0.064, 0.18 - 0.016), zc + 0.08, 0.035, derin=0.02, key=TAS, ic_key='tas_acik', c=0.006, cati_key='kursun')
for s_ in (-1, 1):
    boru(y, [V(s_ * 0.05, 0.18 - 0.02, zc + 0.084), V(s_ * 0.02, 0.18 - 0.02, zc + 0.1)], 0.006, 'altin', n=6)
sancak(y, 0, 0.21, zc + 0.115, boy=0.2, en=0.11, yuk=0.065, aci=math.pi * 0.95)
# the side ranges of the Cour de Marbre and the Cour Royale wings
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.14, sx * 0.28))
    tugla_blok(x0, x1, -0.08, 0.18, HB, [2, 4, 0, 0] if sx < 0 else [2, 0, 0, 4], h1=0.1, h2=0.035)   # (inner side faces the court)
    x0, x1 = sorted((sx * 0.28, sx * 0.48))
    tugla_blok(x0, x1, -0.42, 0.28, HB, [3, 10, 0, 8] if sx < 0 else [3, 8, 0, 10], h1=0.1, h2=0.035, lukarn_adim=2)

y.bolum('Bakanlar kanatları ve şapel')
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.58, sx * 0.8))
    tugla_blok(x0, x1, -0.82, -0.3, 0.2, [3, 6, 0, 6], h1=0.1, h2=0.03)
    # the pavilions' heads toward the Place d'Armes: a stone frontispiece rising from the cornice in front of the
    # roof, crowned by a pediment with the royal arms, trophies on its corners
    FX0, FX1, FYf = x0 + 0.03, x1 - 0.03, -0.836
    kutu3(y, V((FX0 + FX1) / 2, (FYf - 0.78) / 2, Z0 + 0.218), X, Y, Z, FX1 - FX0, -0.78 - FYf, 0.04, TAS, ('+x', '-x', '-y'))
    silme(y, [V(FX0, FYf), V(FX1, FYf)], Z0 + 0.234, 0.006, 0.005, 'tas_acik', 'duz', kapali=False)
    y.oculus(V((FX0 + FX1) / 2, FYf, Z0 + 0.218), X, -Y, 0.012, 'cam', 'tas_acik', f=0.004, k=12)
    alinlik(y, V(FX0 - 0.004, FYf), V(FX1 + 0.004, FYf), Z0 + 0.238, 0.05, derin=0.056, key=TAS, ic_key='tas_acik', c=0.006, cati_key='arduvaz')
    kutu3(y, V((FX0 + FX1) / 2, FYf - 0.002, Z0 + 0.258), X, Y, Z, 0.022, 0.004, 0.016, 'altin', ('+x', '-x', '-y', '+z'))
    for xx in (FX0, FX1):
        vazo(y, xx, FYf + 0.006, Z0 + 0.238, 0.8, 'altin', n=5)
# on the south side a stone range, on the north the Royal Chapel
tugla_blok(-0.84, -0.6, -0.24, 0.3, 0.22, [2, 4, 0, 8], h1=0.1, h2=0.035)

# the Royal Chapel: two tiers of tall arched windows between buttress piers with statues, a steep slate roof
# with a gilt crest and a gilt lantern spire, a round apse
y.bolum('Kraliyet şapeli')
KX0, KX1, KY0, KY1 = 0.62, 0.84, -0.22, 0.2
KH = 0.44
kp = [V(KX0, KY0), V(KX1, KY0), V(KX1, KY1), V(KX0, KY1)]
for i, n in ((0, 3), (1, 7), (3, 7)):
    a, b = kp[i], kp[(i + 1) % 4]
    e, nc = nc_of(a, b)
    for j in range(n):
        p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
        if i == 0 and j == 1:
            y.kemerli(p, q, Z0, KH * 0.42, (TAS, 'tas_koyu', 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.5, ust=0.02, derin=0.014, k_say=8, sivri=0.0,
                      cerceve=(0.006, 'tas_acik'))
        else:
            y.kemerli(p, q, Z0, KH * 0.42, PEN, v0=0.02, en=0.5, ust=0.02, derin=0.012, k_say=6, sivri=0.0)
        y.kemerli(p, q, Z0 + KH * 0.42, KH * 0.58, PEN, v0=0.02, en=0.56, ust=0.026, derin=0.012, k_say=6, sivri=0.0)
    for j in range(n + 1):
        pp = a.lerp(b, j / n)
        kutu3(y, pp + nc * 0.009 + Z * (Z0 + KH / 2), e, nc, Z, 0.022, 0.018, KH, TAS, ('+x', '-x', '+y', '+z'))
        heykel(y, pp.x + nc.x * 0.009, pp.y + nc.y * 0.009, Z0 + KH + 0.012, 0.9, TAS, math.atan2(nc.y, nc.x) + math.pi / 2, n=4)
    silme(y, [a, b], Z0 + KH * 0.42 - 0.004, 0.008, 0.008, 'tas_acik', 'duz', kapali=False)
silme(y, [kp[3], kp[0], kp[1], kp[2]], Z0 + KH - 0.004, 0.016, 0.014, 'tas_acik', 'tac', kapali=False)
ZE = Z0 + KH + 0.012
RI = 0.016                         # the lead walk between the balustrade and the roof's foot
for xa, xb in ((KX0, KX0 + RI), (KX1 - RI, KX1)):
    y.yuz_yon([V(xa, KY0, ZE), V(xb, KY0, ZE), V(xb, KY1, ZE), V(xa, KY1, ZE)], 'kursun', Z)
korkuluk_hafif(y, [V(KX1 - 0.006, KY0 + 0.006), V(KX1 - 0.006, KY1)], ZE, 0.03, False, 'tas_acik', ayak=0.1)
korkuluk_hafif(y, [V(KX0 + 0.006, KY1), V(KX0 + 0.006, KY0 + 0.006)], ZE, 0.03, False, 'tas_acik', ayak=0.1)
korkuluk_hafif(y, [V(KX0 + 0.006, KY0 + 0.006), V(KX1 - 0.006, KY0 + 0.006)], ZE, 0.03, False, 'tas_acik', ayak=0.1)
# the steep roof, the gilt crest
zr = cati_besik(y, KX0 + RI, KX1 - RI, KY0, KY1, ZE, 0.24, 0.004, 'arduvaz', 'altin', ucluk_key=TAS, alt_key='ahsap_koyu', ns=8, nr=6,
                uc_sacak=0.0, mahya_en=0.01)
for k_ in range(11):
    yy = KY0 + 0.01 + (KY1 - KY0 - 0.02) * k_ / 10
    levha(y, [V((KX0 + KX1) / 2, yy - 0.006, zr), V((KX0 + KX1) / 2, yy + 0.006, zr), V((KX0 + KX1) / 2, yy, zr + 0.016)], 'altin', X, 0.0015)
# the gable toward the court: an oculus and a gilt group on the apex
y.oculus(V((KX0 + KX1) / 2, KY0, ZE + 0.07), X, -Y, 0.022, 'cam', 'tas_acik', f=0.006, k=14)
heykel(y, (KX0 + KX1) / 2, KY0 + 0.004, zr - 0.012, 1.0, 'altin', 0, n=4)
# the apse (+y) under a half cone, the lead walk round it
AC = V((KX0 + KX1) / 2, KY1)
RA = (KX1 - KX0) / 2
ak = [V(AC.x + RA * math.cos(math.pi * k / 6), AC.y + RA * math.sin(math.pi * k / 6)) for k in range(7)]
for k in range(6):
    a, b = ak[k], ak[k + 1]
    y.kemerli(a, b, Z0, KH, PEN, v0=0.04, en=0.5, ust=0.03, derin=0.012, k_say=6, sivri=0.0)
silme(y, ak, Z0 + KH - 0.004, 0.016, 0.014, 'tas_acik', 'tac', kapali=False)
RC = RA - RI + 0.004
tepe = V(AC.x, AC.y, zr - 0.008)
cr = [V(AC.x + RC * math.cos(math.pi * k / 10), AC.y + RC * math.sin(math.pi * k / 10)) for k in range(11)]
ir = [V(AC.x + RA * math.cos(math.pi * k / 10), AC.y + RA * math.sin(math.pi * k / 10)) for k in range(11)]
for k in range(10):
    a, b = cr[k], cr[k + 1]
    m = (a + b) / 2
    y.yuz_yon([V(a.x, a.y, ZE), V(b.x, b.y, ZE), tepe], 'arduvaz', V(m.x - AC.x, m.y - AC.y, 0.4))
    y.yuz_yon([V(ir[k].x, ir[k].y, ZE), V(ir[k + 1].x, ir[k + 1].y, ZE), V(b.x, b.y, ZE), V(a.x, a.y, ZE)], 'kursun', Z)
korkuluk_hafif(y, [V(AC.x + (RA - 0.006) * math.cos(math.pi * k / 6), AC.y + (RA - 0.006) * math.sin(math.pi * k / 6)) for k in range(7)], ZE, 0.03, False,
               'tas_acik', ayak=0.06)
# the lantern spire
LC = V((KX0 + KX1) / 2, -0.02)
k6 = cokgen(LC, 0.022, 8, math.pi / 8)
for i in range(8):
    y.kemerli(k6[i], k6[(i + 1) % 8], zr - 0.03, 0.06, ('altin', 'koyu', 'altin', 'koyu'), v0=0.03, en=0.5, ust=0.006, derin=0.004, k_say=6, sivri=0.0)
donel(y, LC, [(0.026, zr + 0.03), (0.018, zr + 0.05), (0.004, zr + 0.17), (0.0, zr + 0.19)], 'altin', n=8, kat=math.pi / 8)
kure(y, (LC.x, LC.y, zr + 0.195), 0.007, 'altin', n=6, kat=3)

# ---------------------------------------------------------------- the gates
y.bolum('Kral kapısı ve parmaklıklar')
# the Grille Royale between the Cour d'Honneur and the Cour Royale: gilded, with its central gate and the crown
for x0, x1 in ((-0.28, -0.06), (0.06, 0.28)):
    parmaklik(V(x0, -0.42), V(x1, -0.42), Z0, 0.07, ayak=0.11, key='altin')
for s_ in (-1, 1):
    kutu3(y, V(s_ * 0.06, -0.42, Z0 + 0.055), X, Y, Z, 0.026, 0.026, 0.11, TAS, ('+x', '-x', '+y', '-y', '+z'))
    heykel(y, s_ * 0.06, -0.42, Z0 + 0.11, 0.9, 'altin', 0, n=4)
for k_ in range(10):
    xx = -0.047 + 0.094 * k_ / 9
    kutu3(y, V(xx, -0.42, Z0 + 0.05), X, Y, Z, 0.0028, 0.0028, 0.09, 'altin', ('+x', '-x', '+y', '-y'))
cubuk(y, V(-0.05, -0.42, Z0 + 0.094), V(0.05, -0.42, Z0 + 0.094), 0.004, 'altin')
boru(y, [V(-0.05, -0.42, Z0 + 0.094), V(-0.025, -0.42, Z0 + 0.118), V(0, -0.42, Z0 + 0.124), V(0.025, -0.42, Z0 + 0.118), V(0.05, -0.42, Z0 + 0.094)],
     0.0025, 'altin', n=4)
kure(y, (0, -0.42, Z0 + 0.134), 0.01, 'altin', n=8, kat=4)   # the crown
# the Grille d'Honneur at the Place d'Armes, between the ministers' wings
for x0, x1 in ((-0.58, -0.07), (0.07, 0.58)):
    parmaklik(V(x0, -0.84), V(x1, -0.84), Z0, 0.065, ayak=0.12)
for s_ in (-1, 1):
    kutu3(y, V(s_ * 0.07, -0.84, Z0 + 0.06), X, Y, Z, 0.03, 0.03, 0.12, TAS, ('+x', '-x', '+y', '-y', '+z'))
    heykel(y, s_ * 0.07, -0.84, Z0 + 0.12, 1.1, TAS, 0, n=4)
for k_ in range(12):
    xx = -0.056 + 0.112 * k_ / 11
    kutu3(y, V(xx, -0.84, Z0 + 0.05), X, Y, Z, 0.0026, 0.0026, 0.09, 'demir', ('+x', '-x', '+y', '-y'))
cubuk(y, V(-0.058, -0.84, Z0 + 0.092), V(0.058, -0.84, Z0 + 0.092), 0.004, 'altin')
kure(y, (0, -0.84, Z0 + 0.106), 0.009, 'altin', n=8, kat=4)
# Louis XIV on horseback in the Place d'Armes
atli_heykel(y, 0, -0.98, Z0, -math.pi / 2, 1.5, 'bronz')

# ---------------------------------------------------------------- the gardens
y.bolum('Bahçeler: su parteri, Latona')
# the Parterre d'Eau: two great pools with bronze figures on their rims
for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.06, sx * 0.42))
    havuz(y, x0, x1, 0.68, 0.84, Z0 + 0.012, derin=0.02, kenar=0.016, key=TAS)
    duvarlar(y, disa(dikdortgen(x0, x1, 0.68, 0.84), 0.016), Z0, Z0 + 0.012, TAS)
    for k_ in range(4):
        xx = x0 + (x1 - x0) * (k_ + 0.5) / 4
        for yy in (0.68 - 0.008, 0.84 + 0.008):
            boru(y, [V(xx - 0.012, yy, Z0 + 0.027), V(xx, yy, Z0 + 0.031), V(xx + 0.012, yy, Z0 + 0.028)], 0.0035, 'bronz', n=4)
    donel(y, ((x0 + x1) / 2, 0.76), [(0.012, Z0 + 0.004), (0.012, Z0 + 0.024), (0.006, Z0 + 0.032), (0.0, Z0 + 0.036)], TAS, n=8)
# the parterres before the wings: lawns cut by gravel walks, box scrolls, topiary cones
def parter(x0, x1, y0, y1, z, desen=0):
    zz = z + 0.003
    for (a0, a1, b0, b1) in ((x0, (x0 + x1) / 2 - 0.012, y0, y1), ((x0 + x1) / 2 + 0.012, x1, y0, y1)):
        y.yuz_yon([V(a0, b0, zz), V(a1, b0, zz), V(a1, b1, zz), V(a0, b1, zz)], 'cimen', Z)
        duvarlar(y, dikdortgen(a0, a1, b0, b1), z, zz, 'boya_yesil')
        # a box border and a scroll (an oval loop of box) in each bed
        for p_, q_ in zip(dikdortgen(a0, a1, b0, b1), dikdortgen(a0, a1, b0, b1)[1:] + dikdortgen(a0, a1, b0, b1)[:1]):
            pa, pb, L_, e, nc = eksen(p_, q_)
            kutu3(y, pa.lerp(pb, 0.5) - nc * 0.004 + Z * (zz + 0.004), e, nc, Z, L_ - 0.008, 0.007, 0.008, 'boya_yesil', ('+x', '-x', '+y', '-y', '+z'))
        cx, cy = (a0 + a1) / 2, (b0 + b1) / 2
        rx, ry = (a1 - a0) * 0.3, (b1 - b0) * 0.3
        pts = [V(cx + rx * math.cos(TAU * k / 9), cy + ry * math.sin(TAU * k / 9), zz + 0.004) for k in range(10)]
        boru(y, pts, 0.0035, 'boya_yesil', n=3, kapat=False)
        if desen:
            agac(y, cx, cy, zz, boy=0.07, tur='servi', key='boya_yesil')
        for px, py in ((a0 + 0.012, b0 + 0.012), (a1 - 0.012, b0 + 0.012), (a0 + 0.012, b1 - 0.012), (a1 - 0.012, b1 - 0.012)):
            donel(y, (px, py), [(0.0, zz), (0.008, zz), (0.0, zz + 0.04)], 'boya_yesil', n=4)


for sx in (-1, 1):
    x0, x1 = sorted((sx * 0.52, sx * 1.0))
    parter(x0, x1, 0.58, 0.86, Z0, 1)
    x0, x1 = sorted((sx * 0.4, sx * 1.0))
    parter(x0, x1, 0.96, 1.16, ZL, 0)
# the Latona Fountain: tiered marble basins, the goddess in gilt lead, frogs round the rims, and the lawn walk
LC2 = V(0, 1.06)
for (r_, z_, h_) in ((0.15, ZL, 0.014), (0.1, ZL + 0.014, 0.016), (0.062, ZL + 0.03, 0.016), (0.032, ZL + 0.046, 0.016)):
    donel(y, LC2, [(r_, max(ZL, z_ - 0.006)), (r_, z_ + h_), (r_ - 0.008, z_ + h_), (r_ - 0.008, z_ + h_ - 0.006)], 'mermer', n=20)
    y.yuz_yon([V(LC2.x + (r_ - 0.008) * math.cos(TAU * k / 20) * 1.0, LC2.y + (r_ - 0.008) * math.sin(TAU * k / 20), z_ + h_ - 0.006) for k in range(20)],
              'su', Z)
heykel(y, LC2.x, LC2.y, ZL + 0.056, 1.1, 'altin', 0, n=6)
for k in range(10):
    an = TAU * k / 10
    for r_, z_ in ((0.135, ZL + 0.014), (0.088, ZL + 0.03)):
        kure(y, (LC2.x + r_ * math.cos(an), LC2.y + r_ * math.sin(an), z_ + 0.003), 0.0045, 'altin', n=4, kat=2)
# bosquets: tree masses at the sides of the lower garden and along the terrace
for sx in (-1, 1):
    for yy in (0.64, 0.84):
        agac(y, sx * 1.03, yy, Z0, boy=0.12)
    agac(y, sx * 0.3, 1.17, ZL, boy=0.13)
# the Place d'Armes: paving lines radiating from the statue, lamp posts
for k_ in range(-3, 4):
    an = -math.pi / 2 + k_ * 0.32
    d_ = V(math.cos(an), math.sin(an))
    p0, p1 = V(0, -0.98) + d_ * 0.06, V(0, -0.98) + d_ * (0.14 / max(0.2, abs(d_.y)))
    p1 = V(max(-1.0, min(1.0, p1.x)), max(-1.1, p1.y))
    s_ = V(-d_.y, d_.x) * 0.005
    y.yuz_yon([p0 - s_ + Z * (Z0 + 0.002), p1 - s_ + Z * (Z0 + 0.002), p1 + s_ + Z * (Z0 + 0.002), p0 + s_ + Z * (Z0 + 0.002)], 'tas_acik', Z)
for xx in (-0.5, -0.25, 0.25, 0.5):
    y.prizma((xx, -0.9), 0.0035, Z0, Z0 + 0.075, 'demir', n=4)
    donel(y, (xx, -0.9), [(0.005, Z0 + 0.075), (0.009, Z0 + 0.082), (0.009, Z0 + 0.094), (0.0, Z0 + 0.102)], 'altin', n=4)

calistir(y, 'lm_versay')
