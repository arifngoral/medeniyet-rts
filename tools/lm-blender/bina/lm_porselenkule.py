# Porselen Kule (lm_porselenkule): the Porcelain Tower of Nanjing (Bao'en temple, Ming): a nine-storey octagonal
# pagoda faced with white porcelain bricks, glazed green eaves with yellow ridges and bells at every corner, arched
# doors framed in coloured glaze, a gilt finial; at its foot an encircling porch on a railed marble podium, and round it
# the Bao'en temple court: the gate, bell and drum towers, the main hall, side halls, pines and an incense burner.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from cin_ek import *
from bina_ortak import calistir

y = Yapi()
YES, SAR = 'kiremit_yesil', 'kiremit_sari'
KIR = 'siva_kirmizi'
BEYAZ = 'porselen'

# ---------------------------------------------------------------- ground and the temple wall
y.bolum('Zemin')
Z0 = zemin(y, -1.15, 1.15, -1.18, 1.15, 0.03, 'tas_koyu', 'zemin', basamak=(('on', 0.4),), n_basamak=2)
y.bolum('Tapınak duvarı')
kirmizi_sur(y, [V(0.2, -1.06), V(1.08, -1.06), V(1.08, 1.08), V(-1.08, 1.08), V(-1.08, -1.06), V(-0.2, -1.06)], Z0, 0.09, 0.03, KIR,
            YES, SAR, kapali=False, baslik=0.026)
# the mountain gate: three arched doors in a masonry front under a green hip-and-gable roof
y.bolum('Dağ kapısı')
GX, GY0, GY1, GH = 0.24, -1.12, -1.0, 0.13
for i in range(5):
    a, b = V(-GX + 2 * GX * i / 5, GY0), V(-GX + 2 * GX * (i + 1) / 5, GY0)
    if i in (1, 2, 3):
        y.kemerli(a + Z * Z0, b + Z * Z0, 0, GH, (KIR, KIR, 'mermer', 'lake_koyu'), v0=0.0, en=0.62 if i == 2 else 0.52, ust=0.035,
                  derin=0.03, k_say=8, cerceve=(0.005, 'mermer'))
    else:
        duz_duvar(y, a, b, Z0, Z0 + GH, KIR)
for i in range(5):
    a, b = V(GX - 2 * GX * i / 5, GY1), V(GX - 2 * GX * (i + 1) / 5, GY1)
    if i == 2:
        y.kemerli(a + Z * Z0, b + Z * Z0, 0, GH, (KIR, KIR, 'mermer', 'lake_koyu'), v0=0.0, en=0.6, ust=0.035, derin=0.03, k_say=8)
    else:
        duz_duvar(y, a, b, Z0, Z0 + GH, KIR)
for s in (-1, 1):
    duz_duvar(y, V(s * GX, GY0 if s > 0 else GY1), V(s * GX, GY1 if s > 0 else GY0), Z0, Z0 + GH, KIR)
silme(y, dikdortgen(-GX, GX, GY0, GY1), Z0 + 0.001, 0.016, 0.005, 'mermer', 'kaide')
silme(y, dikdortgen(-GX, GX, GY0, GY1), Z0 + GH - 0.012, 0.012, 0.005, 'lake_koyu', 'duz')
cati_irimoya(y, -GX, GX, GY0, GY1, Z0 + GH, 0.1, 0.05, YES, SAR, 0.45, 0.03, 'lake_koyu', KIR, ns=8, nr=5, ns2=5, nr2=4)
for s in (-1, 1):
    aslan(y, s * 0.15, GY0 - 0.04, Z0, math.pi / 2, 1.1)
sancak(y, -0.3, -1.12, Z0, boy=0.32, en=0.13, yuk=0.08, aci=math.pi * 0.85)

# ---------------------------------------------------------------- bell and drum towers
y.bolum('Çan ve davul kuleleri')
for s in (-1, 1):
    cx, cy = s * 0.68, -0.62
    kutu(y, V(cx - 0.11, cy - 0.11, Z0), X, 0.22, 0.22, 0.09, 'granit', 'onarkasagsol')
    y.yuz_yon(dikdortgen(cx - 0.11, cx + 0.11, cy - 0.11, cy + 0.11, Z0 + 0.09), 'zemin', Z)
    y.kemerli(V(cx - 0.11, cy - 0.11, Z0), V(cx + 0.11, cy - 0.11, Z0), 0, 0.09, ('granit', 'granit_koyu', 'mermer', 'koyu'), en=0.45,
              ust=0.02, derin=0.012, k_say=8)
    silme(y, dikdortgen(cx - 0.11, cx + 0.11, cy - 0.11, cy + 0.11), Z0 + 0.082, 0.008, 0.005, 'mermer', 'kaba')
    korkuluk(y, disa(dikdortgen(cx - 0.11, cx + 0.11, cy - 0.11, cy + 0.11), -0.007), Z0 + 0.09, 0.018, 'mermer', 0.05)
    salon(y, cx, cy, 0.13, 0.13, Z0 + 0.09, 0.07, 0.07, sacak=0.045, cati_key=YES, mahya=SAR, kivrim=0.5, yukari=0.03, cift=True,
          alt_yuk=0.025, ic=0.018, ust_h=0.03, bay=0.065, chiwenli=False, hayvan=0, cati='irimoya', mahya_en=0.008, ust_kafes=False)

# ---------------------------------------------------------------- main hall and side halls
y.bolum('Ana salon')
salon(y, 0, 0.86, 0.66, 0.24, Z0 + 0.003, 0.12, 0.13, sacak=0.06, cati_key=YES, mahya=SAR, kivrim=0.45, yukari=0.035, cift=False,
      bay=0.083, hayvan=4, mahya_en=0.012, kaide=(0.04, 'mermer'))
teras_merdiven(y, (0, 0.86 - 0.12 - 0.012 - 0.046), math.pi / 2, 0.16, Z0 + 0.003, Z0 + 0.043, 4, 'mermer', yanlik=False)
for s in (-1, 1):
    x0, x1 = (0.82, 0.98) if s > 0 else (-0.98, -0.82)
    kucuk_salon(y, x0, x1, -0.32, 0.55, Z0, 0.07, 0.055, 0.035, KIR, 'lake', 'kiremit_koyu', 'kiremit_koyu2', 'besik', 0.4, 0.02, 0.014,
                'mermer', kapi_yon=3 if s > 0 else 1, bay=0.08, arka_duz=True)
# the court paving: a marble axis from the gate to the hall
kutu(y, V(-0.05, GY1, Z0), X, 0.1, 0.86 - 0.12 - 0.012 - 0.046 - GY1, 0.003, 'mermer', 'onarkasagsolust')

# ---------------------------------------------------------------- the pagoda's podium and porch
y.bolum('Kaide')
PC = (0.0, -0.02)
KAT8 = math.pi / 8
YON = (-math.pi / 2, 0.0, math.pi / 2, math.pi)
z = Z0
for i, r in enumerate((0.58, 0.5)):
    k = cokgen(PC, r, 8, KAT8)
    ap = r * math.cos(math.pi / 8)
    bos = [((PC[0] + (ap - 0.01) * math.cos(a), PC[1] + (ap - 0.01) * math.sin(a)), 0.2) for a in YON]
    zt = teras(y, k, z, 0.05, 'mermer', 'zemin', True, bos, 0.05, 0.022, 0.008, oluk='tas_acik' if i == 1 else None)
    for a in YON:
        d = V(math.cos(a), math.sin(a))
        teras_merdiven(y, V(PC[0], PC[1]) + d * (ap + 0.05 * 1.15 - 0.006), a + math.pi, 0.17, z, zt, 4, 'mermer', yanlik=(i == 0))
    z = zt
ZP = z
# the encircling porch round the ground storey: columns, a lean-to green roof
R0 = 0.31
RP = R0 + 0.09
for p in cokgen(PC, RP, 16, math.pi / 16):
    y.prizma((p.x, p.y), 0.009, ZP + 0.006, ZP + 0.11, 'lake', n=8)
    kutu_merkez(y, (p.x, p.y), 0.026, 0.026, 0.006, 'mermer', z0=ZP, yuzler='onarkasagsolust')
silme(y, cokgen(PC, RP, 16, math.pi / 16), ZP + 0.1, 0.016, 0.006, 'lake_koyu', 'duz')
silme(y, cokgen(PC, RP, 16, math.pi / 16), ZP + 0.11, 0.008, 0.01, 'kiremit_yesil', 'duz')
y.yuz_yon([V(p.x, p.y, ZP + 0.1) for p in cokgen(PC, RP, 16, math.pi / 16)], 'lake_koyu', -Z)   # (the porch ceiling)

# ---------------------------------------------------------------- the nine storeys
y.bolum('Kule')
N_KAT = 9
rad = lambda k: R0 - (R0 - 0.18) * k / (N_KAT - 1)
yuk = lambda k: 0.165 - 0.045 * k / (N_KAT - 1)
z = ZP
for k in range(N_KAT):
    r, h = rad(k), yuk(k)
    zt = sekizgen_kat(y, PC, r, z, h, BEYAZ, (YES, SAR), SAR, 8, kapi=(1, 3, 5, 7), derin=0.018)
    # a glazed band at the foot of the storey
    silme(y, cokgen(PC, r, 8, KAT8), z, 0.01, 0.006, YES if k % 2 else SAR, 'duz')
    zc = cokgen_konsol(y, PC, r, 8, zt, (YES, 'lake_koyu'), 0.045, 0.018, frize=BEYAZ)
    sk = 0.078 - 0.022 * k / (N_KAT - 1)
    if k == 0:
        # the porch roof leans against the ground storey under its own eave
        ro = r * math.cos(math.pi / 8) - 0.01   # (inside the octagon's faces: its corners rise through the porch roof)
        tp = 1 - ro / (RP + 0.05)
        cokgen_cati(y, PC, RP, 16, ZP + 0.118, egim_icin(0.05, tp, 0.3), 0.05, YES, SAR, 0.3, 0.0, ro, kat=math.pi / 16,
                    ns=1, nr=3, alt_key='lake_koyu', sirt=False, kalinlik=0.01)
    if k < N_KAT - 1:
        rn = rad(k + 1)
        t = 1 - (rn - 0.008) / (r + sk)
        zo, _ = cokgen_cati(y, PC, r, 8, zc, egim_icin(0.04, t, 0.5), sk, YES, SAR, 0.5, 0.03, rn - 0.008, kat=KAT8, ns=2, nr=3,
                            alt_key='lake_koyu', kalinlik=0.011, mahya_en=0.008, cann=('bronz', 0.028))
        duvarlar(y, cokgen(PC, rn, 8, KAT8), zc, zo + 0.004, BEYAZ)
        z = zo + 0.004
    else:
        tepe, _ = cokgen_cati(y, PC, r, 8, zc, 0.15, sk, YES, SAR, 0.5, 0.035, 0.0, kat=KAT8, ns=2, nr=5, alt_key='lake_koyu',
                              kalinlik=0.011, mahya_en=0.009, cann=('bronz', 0.028))
# the gilt finial: a lotus, the mast with its rings, the jewel
donel(y, PC, [(0.045, tepe - 0.03), (0.05, tepe - 0.012), (0.034, tepe + 0.004), (0.022, tepe + 0.01), (0.0, tepe + 0.012)], 'altin', n=8,
      kat=KAT8)
with parca(y, (PC[0], PC[1], tepe), 0, 1.7):
    son = sorin(y, 0, 0, 0.0, 0.17, 'altin', 7)
kure(y, (PC[0], PC[1], tepe + son * 1.7 - 0.005), 0.022, 'altin', n=10, kat=5)

# paved walks from the podium's side stairs to the side halls
for s in (-1, 1):
    x0_, x1_ = (0.6, 0.8) if s > 0 else (-0.8, -0.6)
    kutu(y, V(x0_, PC[1] - 0.05, Z0), X, x1_ - x0_, 0.1, 0.003, 'mermer', 'onarkasagsolust')


def stel_kosku(cx, cy):
    """a stele pavilion: an open square ting over a stone tortoise (bixi) carrying an inscribed tablet"""
    kosk(y, (cx, cy), 0.12, Z0, 0.09, 0.07, 0.035, 'lake', YES, SAR, 0.5, 0.025, 'mermer', n=4, boya='turkuaz')
    z = Z0 + 0.02
    donel(y, (cx, cy), [(0.0, z), (0.034, z), (0.036, z + 0.008), (0.028, z + 0.016), (0.0, z + 0.019)], 'granit', n=10)
    kure(y, (cx, cy - 0.036, z + 0.01), 0.009, 'granit', n=8, kat=4)
    kutu_merkez(y, (cx, cy + 0.004), 0.04, 0.012, 0.075, 'granit_koyu', z0=z + 0.014)
    donel(y, (cx, cy + 0.004), [(0.024, z + 0.089), (0.024, z + 0.096), (0.012, z + 0.104), (0.0, z + 0.106)], 'granit_koyu', n=8)


for s in (-1, 1):
    stel_kosku(s * 0.52, 0.42)
# ---------------------------------------------------------------- court furniture and trees
y.bolum('Avlu')
tutsu(y, 0, -0.68, Z0 + 0.003, 1.5)
for s in (-1, 1):
    kazan(y, s * 0.3, -0.72, Z0, 1.3)
for (x, yy) in ((-0.62, 0.22), (0.62, 0.22), (-0.66, -0.28), (0.66, -0.28), (-0.38, 0.6), (0.4, 0.64), (-0.95, 0.85), (0.95, 0.85),
                (-0.92, -0.88), (0.92, -0.88), (-0.35, -0.9), (0.35, -0.9)):
    cam(y, x, yy, Z0, 0.17)
kosk(y, (0.7, 0.68), 0.1, Z0, 0.07, 0.055, 0.035, 'lake', YES, SAR, 0.5, 0.025, 'mermer', n=6)

sayim(y)
calistir(y, 'lm_porselenkule')
