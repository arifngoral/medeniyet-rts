# Tercio barracks (lm_tercio): a two-storey courtyard barracks (cuartel) of plastered walls with stone dressings,
# barred ground-floor windows, a stone portal with the royal arms under a bell gable (espadaña), an arcaded courtyard
# with a well and a hipped tile ring roof; a watch tower with an open loggia and the blue banner; the armoury with
# pike racks, guns and powder; on the drill ground a pike square with its colour, drum and officers, arquebusiers
# firing at butts.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from ispanyol_ek import *

y = Yapi()
X0, X1, Y0, Y1 = -1.1, 1.1, -0.78, 0.98
ZB = 0.04
DUV = ('siva_krem', 'tas_koyu', 'tas_acik', 'koyu')
TAS = 'kirec'
S = 1.25                                          # soldiers' scale

# ================================================================ ground
y.bolum('Zemin')
kutu(y, V(X0, Y0, 0), X, X1 - X0, Y1 - Y0, ZB, 'tas_koyu', 'onarkasagsol')
silme(y, dikdortgen(X0, X1, Y0, Y1), ZB - 0.008, 0.008, 0.006, 'tas_koyu', 'duz')
XD, YD = 0.56, -0.04                              # the drill ground: x < XD, y < YD
y.yuz_yon([V(X0, Y0, ZB), V(XD, Y0, ZB), V(XD, YD, ZB), V(X0, YD, ZB)], 'toprak', Z)
y.yuz_yon([V(XD, Y0, ZB), V(X1, Y0, ZB), V(X1, YD, ZB), V(XD, YD, ZB)], 'zemin', Z)
y.yuz_yon([V(X0, YD, ZB), V(X1, YD, ZB), V(X1, Y1, ZB), V(X0, Y1, ZB)], 'zemin', Z)
for a_, b_ in ((V(X0 + 0.02, YD - 0.008), V(XD - 0.008, YD - 0.008)), (V(XD - 0.008, Y0 + 0.02), V(XD - 0.008, YD - 0.008))):
    cubuk(y, a_ + Z * (ZB + 0.004), b_ + Z * (ZB + 0.004), 0.014, 'tas', 0.008)

# ================================================================ the barracks
y.bolum('Kışla cepheleri')
BX0, BX1, BY0, BY1 = -1.0, 0.44, 0.04, 0.92
DW = 0.24
H1, H2 = 0.15, 0.14
ZT = ZB + H1 + H2
dis = dikdortgen(BX0, BX1, BY0, BY1)
ic = dikdortgen(BX0 + DW, BX1 - DW, BY0 + DW, BY1 - DW)
ALT = (H1, 0.3, 0.7, 0.04, 0.105, True)
UST = (H2, 0.28, 0.72, 0.022, 0.112, False)
nbay = [13, 8, 13, 8]
PB = 6                                           # the portal's bay on the front
for i in range(4):
    a_, b_ = dis[i], dis[(i + 1) % 4]
    atla = (PB,) if i == 0 else ((3, 4) if i == 1 else ())
    cephe(y, a_, b_, ZB, [ALT, UST], nbay[i], atla=atla, renk=DUV, cerceve=(0.006, TAS))
    if i == 1:   # a cart gate on the east side
        p, q = a_.lerp(b_, 3 / 8), a_.lerp(b_, 5 / 8)
        y.kemerli(p, q, ZB, H1, (DUV[0], 'tas_koyu', 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.62, ust=0.016, derin=0.03, k_say=8, cerceve=(0.008, TAS))
silme(y, dis, ZB, 0.024, 0.008, 'tas_koyu', 'kaide')
silme(y, dis, ZB + H1 - 0.006, 0.01, 0.006, TAS, 'duz')
silme(y, dis, ZT - 0.016, 0.016, 0.012, TAS, 'tac')
for p in dis:
    kose_taslari(y, p, ZB + 0.024, ZT - 0.016, TAS)

y.bolum('Taç kapı ve çan duvarı')
pa, pb = dis[0].lerp(dis[1], PB / 13), dis[0].lerp(dis[1], (PB + 1) / 13)
y.kemerli(pa, pb, ZB, H1, (TAS, 'tas_koyu', 'tas_acik', 'ahsap_koyu'), v0=0.0, en=0.7, ust=0.012, derin=0.03, k_say=10, cerceve=(0.007, ['kirec', 'tas_koyu']))
cx = (pa.x + pb.x) / 2
PW = (pb - pa).length
for sx in (-1, 1):   # paired pilasters standing proud of the wall
    for k in (0, 1):
        xx = cx + sx * (PW / 2 + 0.006 + k * 0.016)
        kutu3(y, V(xx, BY0 - 0.008, ZB + H1 / 2), X, Y, Z, 0.014, 0.016, H1, TAS, ('+x', '-x', '-y', '+z'))
        kutu3(y, V(xx, BY0 - 0.011, ZB + 0.013), X, Y, Z, 0.019, 0.022, 0.026, 'tas_koyu', ('+x', '-x', '-y', '+z'))
# the entablature over the door, deep enough to carry the upper frontispiece
kutu3(y, V(cx, BY0 - 0.024, ZB + H1 + 0.008), X, Y, Z, PW + 0.062, 0.048, 0.016, TAS, ('+x', '-x', '-y', '+z', '-z'))
# the upper frontispiece: a stone block standing proud of the wall through the eaves (the roof's edge runs into
# its sides), the arms on its face, the bell gable on its top in front of the roof
FB = 0.044                                        # its depth: past the eaves' edge (sacak 0.034)
FW2 = 0.078                                       # (clear of the next bays' upper windows)
ZA = ZB + H1 + 0.016
ZFT = ZT + 0.008
kutu3(y, V(cx, BY0 - FB / 2, (ZA + ZFT) / 2), X, Y, Z, 2 * FW2, FB, ZFT - ZA, TAS, ('+x', '-x', '-y', '+z'))
for sx in (-1, 1):   # its corner pilasters
    kutu3(y, V(cx + sx * (FW2 - 0.007), BY0 - FB - 0.003, (ZA + ZFT) / 2), X, Y, Z, 0.014, 0.006, ZFT - ZA, 'tas_acik', ('+x', '-x', '-y'))
silme(y, dikdortgen(cx - FW2, cx + FW2, BY0 - FB, BY0 + 0.004), ZFT - 0.012, 0.012, 0.008, 'tas_koyu', 'tac')
# the arms: a framed panel with a shield (quartered red and gold), a gilt crown above
FY_ = BY0 - FB
kutu3(y, V(cx, FY_ - 0.003, ZA + 0.06), X, Y, Z, 0.07, 0.006, 0.084, 'tas_acik', ('+x', '-x', '-y', '+z', '-z'))
sp = [V(cx - 0.024, 0, ZA + 0.088), V(cx + 0.024, 0, ZA + 0.088), V(cx + 0.024, 0, ZA + 0.05), V(cx, 0, ZA + 0.03), V(cx - 0.024, 0, ZA + 0.05)]
levha(y, [p + V(0, FY_ - 0.0072, 0) for p in sp], 'boya_kirmizi', -Y, kil=0.001)
for u0, v0 in ((-1, 1), (1, -1)):
    y.yuz_yon([V(cx, FY_ - 0.0084, ZA + 0.066 + 0.0006 * v0), V(cx + 0.0225 * u0, FY_ - 0.0084, ZA + 0.066 + 0.0006 * v0),
               V(cx + 0.0225 * u0, FY_ - 0.0084, ZA + 0.066 + 0.018 * v0), V(cx, FY_ - 0.0084, ZA + 0.066 + 0.018 * v0)], 'altin', -Y)
kure(y, (cx, FY_ - 0.006, ZA + 0.098), 0.008, 'altin', n=8, kat=4)
# the bell gable (espadaña) on the frontispiece: a stone slab with two open arches and their bells, a curved top
EW, ET = 0.15, 0.034
ey0 = BY0 - FB + 0.002
z0e = ZFT
zte = kemer_dizisi(y, V(cx - EW / 2, ey0), V(cx + EW / 2, ey0), 2, z0e, 0.19, ET, renk=(TAS, 'tas_koyu', 'tas_acik', 'tas_koyu'), en=0.6, ust=0.035,
                   acik=True, taban=False)   # (it stands on the frontispiece's top)
for sx in (-0.5, 0.5):
    bx = cx + sx * EW / 2
    y.prizma((bx, ey0 + ET / 2), 0.0025, zte - 0.03, zte - 0.012, 'demir', n=4)
    donel(y, (bx, ey0 + ET / 2), [(0.0, zte - 0.075), (0.019, zte - 0.075), (0.016, zte - 0.068), (0.011, zte - 0.048), (0.009, zte - 0.033), (0.0, zte - 0.03)], 'bronz', n=10)
silme(y, dikdortgen(cx - EW / 2, cx + EW / 2, ey0, ey0 + ET), zte - 0.004, 0.012, 0.008, TAS, 'tac')
# the stepped, curved top: a slab with a round crest, three balls and an iron cross
ztp = zte + 0.008
crest = [V(cx - EW * 0.32, 0, ztp)] + [V(cx + EW * 0.32 * math.cos(math.pi * (1 - k / 8)), 0, ztp + 0.012 + 0.05 * math.sin(math.pi * k / 8)) for k in range(9)] + [V(cx + EW * 0.32, 0, ztp)]
fr = [p + V(0, ey0 + 0.006, 0) for p in crest]
bk = [p + V(0, ey0 + ET - 0.006, 0) for p in crest]
y.yuz_yon(fr, TAS, -Y); y.yuz_yon(bk, TAS, Y)
for k in range(len(crest) - 1):
    y.yuz_yon([fr[k], fr[k + 1], bk[k + 1], bk[k]], 'tas_acik', (fr[k] + fr[k + 1]) / 2 - V(cx, ey0, ztp))
for sx in (-1, 1):
    xx = cx + sx * EW * 0.42
    donel(y, (xx, ey0 + ET / 2), [(0.008, ztp), (0.008, ztp + 0.012), (0.0, ztp + 0.0121)], TAS, n=6)
    kure(y, (xx, ey0 + ET / 2, ztp + 0.022), 0.01, TAS, n=8, kat=4)
ztop = ztp + 0.062
kure(y, (cx, ey0 + ET / 2, ztop + 0.006), 0.008, TAS, n=8, kat=4)
cubuk(y, V(cx, ey0 + ET / 2, ztop + 0.012), V(cx, ey0 + ET / 2, ztop + 0.06), 0.004, 'demir')
cubuk(y, V(cx - 0.014, ey0 + ET / 2, ztop + 0.045), V(cx + 0.014, ey0 + ET / 2, ztop + 0.045), 0.004, 'demir')

# ================================================================ the courtyard
y.bolum('Avlu')
icr = list(reversed(ic))
for i in range(4):
    a_, b_ = icr[i], icr[(i + 1) % 4]
    L_ = (b_ - a_).length
    n = max(3, int(round(L_ / 0.115)))
    arkad(y, a_, b_, n, ZB, H1, en=0.72, ust=0.018, sivri=0.0, derin=0.035, cerceve=(0.007, TAS), sutunlu=False,
          renk=(DUV[0], 'tas_koyu', 'tas_acik', 'koyu'))
    e_ = (b_ - a_).normalized(); nc_ = V(e_.y, -e_.x)
    w_ = L_ / n
    hs = H1 - 0.018 - 0.72 * w_ / 2
    for k in range(n + 1):   # plain Tuscan piers: a square base, an eight-sided shaft, a block capital
        if k == n: continue
        p = a_.lerp(b_, k / n) + nc_ * 0.014
        kutu_merkez(y, (p.x, p.y), 0.026, 0.026, 0.012, TAS, z0=ZB)
        y.prizma((p.x, p.y), 0.0095, ZB + 0.012, ZB + hs - 0.012, TAS, n=8, ust=False, kat=math.pi / 8)
        kutu_merkez(y, (p.x, p.y), 0.026, 0.026, 0.012, TAS, z0=ZB + hs - 0.012)
    cephe(y, a_, b_, ZB + H1, [UST], n, renk=DUV, cerceve=(0.005, TAS))
silme(y, icr, ZB + H1 - 0.006, 0.008, 0.006, TAS, 'duz')
y.yuz_yon(dikdortgen(BX0 + DW, BX1 - DW, BY0 + DW, BY1 - DW, ZB + 0.0006), 'zemin', Z)
kuyu(y, (BX0 + BX1) / 2 + 0.2, (BY0 + BY1) / 2, ZB)
for k, (xx, yy_) in enumerate(((-0.42, 0.42), (-0.36, 0.56), (-0.15, 0.4))):
    asker(y, xx, yy_, ZB, S, 1.2 + k, silah='pike' if k else 'tufek_omuz', govde='boya_kirmizi', zirh=k == 1)

y.bolum('Kışla çatısı')
halka_cati(y, dis, ic, ZT, 0.11, sacak=0.034, key='kiremit', mahya='kiremit2')
for (xx, yy_) in ((-0.86, 0.15), (-0.45, 0.82), (0.32, 0.55), (-0.9, 0.7), (-0.1, 0.82)):   # chimneys
    kutu_merkez(y, (xx, yy_), 0.032, 0.032, 0.1, 'siva_krem', z0=ZT + 0.02)
    kutu_merkez(y, (xx, yy_), 0.04, 0.04, 0.008, TAS, z0=ZT + 0.12)

# ================================================================ the watch tower
y.bolum('Gözcü kulesi')
TX, TY, TW = 0.44, 0.04, 0.25
ZTW = ZB + 0.66
tk = dikdortgen(TX - TW / 2, TX + TW / 2, TY - TW / 2, TY + TW / 2)
for i in range(4):
    a_, b_ = tk[i], tk[(i + 1) % 4]
    cephe(y, a_, b_, ZB, [(0.22, 0.32, 0.68, 0.07, 0.15, True), (0.22, 0.32, 0.68, 0.05, 0.16, False), (0.22, 0.32, 0.68, 0.05, 0.16, False)], 1,
          renk=DUV, cerceve=(0.007, TAS))
silme(y, tk, ZB, 0.03, 0.01, 'tas_koyu', 'kaide')
for zz in (ZB + 0.22, ZB + 0.44):
    silme(y, tk, zz - 0.005, 0.01, 0.006, TAS, 'duz')
for p in tk:
    kose_taslari(y, p, ZB + 0.03, ZTW, TAS, adim=0.045, buyuk=0.036, kucuk=0.026, h=0.026)
silme(y, tk, ZTW - 0.004, 0.014, 0.012, TAS, 'tac')
tk2 = disa(tk, 0.004)
for i in range(4):
    a_, b_ = tk2[i], tk2[(i + 1) % 4]
    for k in range(2):
        y.kemerli(a_.lerp(b_, k / 2), a_.lerp(b_, (k + 1) / 2), ZTW + 0.01, 0.15, (TAS, 'tas_koyu', 'tas_acik', 'koyu'), v0=0.0, en=0.64,
                  ust=0.02, derin=0.018, k_say=8, korkuluk=0.04, cerceve=(0.006, 'tas_acik'))
ZL = ZTW + 0.16
silme(y, tk2, ZL - 0.004, 0.012, 0.012, TAS, 'tac')
cati_kirma(y, TX - TW / 2 - 0.004, TX + TW / 2 + 0.004, TY - TW / 2 - 0.004, TY + TW / 2 + 0.004, ZL + 0.008, 0.18, 0.038, 'kiremit', mahya='kiremit2', ns=6, nr=5)
y.prizma((TX, TY), 0.004, ZL + 0.185, ZL + 0.22, 'demir', n=5)
kure(y, (TX, TY, ZL + 0.222), 0.012, 'altin', n=10, kat=5)
sancak(y, TX, TY, ZL + 0.232, boy=0.2, en=0.15, yuk=0.09, aci=-math.pi * 0.82)

# ================================================================ the armoury
y.bolum('Silah deposu')
AX0, AX1, AY0, AY1 = 0.66, 1.02, -0.7, -0.2
ak = dikdortgen(AX0, AX1, AY0, AY1)
AH = 0.17
AK = ('kirec', 'tas_koyu', 'tas_acik', 'koyu')
for k in range(3):   # the west face: two big arched doors (one open), a barred window between
    p, q = ak[3].lerp(ak[0], k / 3), ak[3].lerp(ak[0], (k + 1) / 3)
    if k == 1:
        cephe(y, p, q, ZB, [(AH, 0.3, 0.7, 0.07, 0.12, True)], 1, renk=AK, cerceve=(0.006, 'tas_acik'))
    else:
        y.kemerli(p, q, ZB, AH, ('kirec', 'tas_koyu', 'tas_acik', 'koyu' if k == 0 else 'ahsap_koyu'), v0=0.0, en=0.62, ust=0.02, derin=0.03, k_say=8,
                  cerceve=(0.008, ['tas_acik', 'tas_koyu']))
for i in (0, 1, 2):
    a_, b_ = ak[i], ak[(i + 1) % 4]
    n = max(1, int(round((b_ - a_).length / 0.12)))
    cephe(y, a_, b_, ZB, [(AH, 0.36, 0.64, 0.08, 0.13, True)], n, renk=AK, cerceve=(0.005, 'tas_acik'))
silme(y, ak, ZB, 0.02, 0.008, 'tas_koyu', 'kaide')
silme(y, ak, ZB + AH - 0.012, 0.012, 0.01, 'tas_acik', 'tac')
for p in ak:
    kose_taslari(y, p, ZB + 0.02, ZB + AH - 0.012, 'tas_acik')
cati_besik(y, AX0, AX1, AY0, AY1, ZB + AH, 0.12, 0.03, 'kiremit', mahya='kiremit2', ucluk_key='kirec', ns=8, nr=5)
mizrak_sehpa(y, V(AX0 - 0.055, AY0 + 0.02), V(AX0 - 0.055, AY0 + 0.15), ZB, n=10, boy=0.26)
mizrak_sehpa(y, V(AX0 - 0.055, AY1 - 0.13), V(AX0 - 0.055, AY1), ZB, n=10, boy=0.26)
for xx, yy_ in ((AX1 + 0.03, AY0 + 0.08), (AX1 + 0.035, AY0 + 0.12), (AX1 + 0.025, AY0 + 0.16), (AX0 + 0.07, AY0 - 0.035), (AX0 + 0.105, AY0 - 0.04)):
    varil(y, xx, yy_, ZB, 0.014, 0.034)
varil(y, AX1 + 0.031, AY0 + 0.1, ZB + 0.034, 0.013, 0.032)
top_kizak(y, AX0 + 0.16, AY0 - 0.04, ZB, -math.pi / 2, L=0.12, r=0.013)
top_kizak(y, AX0 + 0.3, AY0 - 0.04, ZB, -math.pi / 2, L=0.12, r=0.013)
gulle_yigini(y, AX1 + 0.04, AY1 - 0.05, ZB, 3, 0.008)
sandik(y, AX1 + 0.04, AY1 - 0.12, ZB, aci=0.3)

# ================================================================ the drill ground
y.bolum('Mızrak karesi')
PX, PY = -0.48, -0.36
NC, NR, SP = 8, 6, 0.036 * S
REN = ('boya_kirmizi', 'boya_sari', 'boya_kirmizi', 'kumas', 'boya_yesil', 'boya_kirmizi', 'ahsap_acik')
for r in range(NR):
    for c in range(NC):
        if r == 2 and c in (3, 4): continue   # the colour stands in the middle
        xx = PX + (c - (NC - 1) / 2) * SP
        yy_ = PY + (r - (NR - 1) / 2) * SP
        asker(y, xx, yy_, ZB, S, -math.pi / 2, silah='pike_egik' if r == 0 else 'pike', govde=REN[(r * 3 + c) % len(REN)],
              pantolon=REN[(r + c * 2 + 3) % len(REN)], zirh=r < 2 or c in (0, NC - 1))
asker(y, PX, PY - SP / 2 + 0.006, ZB, S, -math.pi / 2, silah=None, govde='boya_sari', pantolon='boya_kirmizi', zirh=False)
sancak(y, PX + 0.014, PY - SP / 2 + 0.006, ZB + 0.05, boy=0.27, en=0.14, yuk=0.095, aci=math.pi * 0.15)
# officers and the drummer in front
asker(y, PX - 0.07, PY - 0.21, ZB, S * 1.05, math.pi / 2, silah='halbert', govde='boya_kirmizi', pantolon='koyu', zirh=True)
DX, DY = PX + 0.09, PY - 0.2
asker(y, DX, DY, ZB, S, math.pi / 2 + 0.3, silah=None, govde='boya_sari', pantolon='boya_kirmizi', zirh=False)
dd = V(math.cos(math.pi / 2 + 0.3), math.sin(math.pi / 2 + 0.3)) * 0.016
donel(y, (DX + dd.x, DY + dd.y), [(0.0, ZB + 0.034), (0.014, ZB + 0.034), (0.014, ZB + 0.056), (0.0, ZB + 0.056)], 'boya_kirmizi', n=10)
donel(y, (DX + dd.x, DY + dd.y), [(0.0145, ZB + 0.0555), (0.0145, ZB + 0.059), (0.0, ZB + 0.059)], 'beyaz', n=10)
# the arquebusier sleeves at the square's front corners
for sx in (-1, 1):
    for r in range(2):
        for c in range(3):
            xx = PX + sx * (NC / 2 * SP + 0.05 + c * SP)
            yy_ = PY - (NR - 1) / 2 * SP + r * SP - 0.03
            asker(y, xx, yy_, ZB, S, -math.pi / 2, silah='tufek_omuz', govde=REN[(c + r) % 4], pantolon='ahsap_koyu', zirh=False)

y.bolum('Arkebüzcüler ve hedefler')
for r in range(2):
    for c in range(5):
        xx = 0.0 + c * 0.085
        yy_ = -0.3 - r * 0.06
        asker(y, xx, yy_, ZB, S, -math.pi / 2, silah='arkebuz' if r == 1 else 'tufek_omuz', ates=(r == 1 and c % 2 == 0),
              govde=REN[(c * 2 + r) % len(REN)], pantolon='ahsap_koyu', zirh=False)
asker(y, 0.44, -0.2, ZB, S * 1.05, math.pi, silah='halbert', govde='boya_kirmizi', pantolon='koyu', zirh=True)
for c in range(3):
    hedef(y, 0.04 + c * 0.15, -0.7, ZB, math.pi / 2, r=0.036, h=0.07)

# ================================================================ the drill ground's low wall and gate
y.bolum('Talim alanı duvarı')


def alcak_duvar(a_, b_, h=0.034, t=0.02, ayak=0.2):
    """a low plastered wall a->b with a stone coping and piers every ayak"""
    ab, bb, L_, e, nc = eksen(a_, b_)
    m = (ab + bb) / 2
    an = math.atan2(e.y, e.x)
    kutu_merkez(y, (m.x, m.y), L_, t, h, 'siva_krem', z0=ZB, aci=an, yuzler='onarkasagsol')
    kutu_merkez(y, (m.x, m.y), L_ + 0.006, t + 0.008, 0.007, TAS, z0=ZB + h, aci=an)
    n = max(1, int(round(L_ / ayak)))
    for k in range(n + 1):
        p = ab.lerp(bb, k / n)
        kutu_merkez(y, (p.x, p.y), 0.028, 0.028, h + 0.016, TAS, z0=ZB, aci=an)


GX, GW_ = PX, 0.17                                # the gate in front of the pike square
YW, XW = Y0 + 0.024, X0 + 0.024
alcak_duvar(V(XW, YW), V(GX - GW_ / 2 - 0.02, YW))
alcak_duvar(V(GX + GW_ / 2 + 0.02, YW), V(XD - 0.04, YW))
alcak_duvar(V(XW, YW), V(XW, YD - 0.04))
for sx in (-1, 1):   # the gate piers with stone balls, the gate leaves standing open
    gx = GX + sx * (GW_ / 2 + 0.006)
    kutu_merkez(y, (gx, YW), 0.04, 0.04, 0.09, TAS, z0=ZB)
    kutu_merkez(y, (gx, YW), 0.048, 0.048, 0.01, 'tas_koyu', z0=ZB + 0.09)
    kure(y, (gx, YW, ZB + 0.112), 0.014, TAS, n=8, kat=4)
    kutu_merkez(y, (gx - sx * 0.025, YW + 0.035), 0.006, 0.05, 0.06, 'ahsap_koyu', z0=ZB + 0.004)
# a sentry by the gate
asker(y, GX + GW_ / 2 + 0.05, YW + 0.04, ZB, S, -math.pi / 2, silah='halbert', govde='boya_kirmizi', pantolon='boya_sari', zirh=True)

# ================================================================ trees round the compound
y.bolum('Ağaçlar')
for (xx, yy_) in ((-1.06, 0.2), (-1.06, 0.45), (-1.06, 0.7), (0.62, 0.42), (0.62, 0.72), (1.04, 0.2), (1.04, 0.5), (1.04, 0.84)):
    agac(y, xx, yy_, ZB, 0.17, 'servi', 'yesil_koyu')
for (xx, yy_) in ((0.83, 0.05), (0.83, 0.86), (-1.04, -0.72), (0.5, -0.72)):
    y.prizma((xx, yy_), 0.005, ZB, ZB + 0.035, 'ahsap', n=5)
    kure(y, (xx, yy_, ZB + 0.062), 0.032, 'zeytin', n=9, kat=5)

calistir(y, 'lm_tercio')
