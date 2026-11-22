# Uzun Ev (lm_uzunev): a Viking chieftain's longhouse farm (Borg / Trelleborg type): the bow-sided plank hall on a stone
# footing with leaning outer posts, a tall swaybacked thatch roof with a turf ridge, smoke louvres and crossed gable
# boards ending in dragon heads, porched doors; round it a wattle-fenced yard with a raised log storehouse, woodpiles,
# fish-drying racks, a well with a sweep, a sheep pen, a smithy lean-to, hay ricks, spruces and the banner.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from viking_parca import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.03
XS, YS = 1.15, 0.95          # ground half sizes
FX, FY = 1.08, 0.88          # the fence line

y.bolum('Zemin: çimenli çiftlik')
zemin(y, -XS, XS, -YS, YS, Z0, 'granit', 'cimen', basamak=(), silmeli=False)
# trodden earth: the yard before the hall and the path from the gate
yer = lambda pts: y.yuz_yon([V(p[0], p[1], Z0 + 0.002) for p in pts], 'toprak', Z)
yer([(-0.07, -FY), (0.07, -FY), (0.07, -0.42), (-0.07, -0.42)])
yer([(-0.62, -0.42), (0.62, -0.42), (0.66, -0.16), (-0.66, -0.16)])
yer([(0.66, 0.55), (0.98, 0.55), (0.98, 0.82), (0.66, 0.82)])

# ---------------- the hall ----------------
y.bolum('Uzun ev')
HC = (0.0, 0.2)
with parca(y, (HC[0], HC[1], 0)):
    zr = langhus(y, 1.72, 0.6, 0.22, 0.44, z0=Z0, bombe=0.15, sacak=0.05, cati='saz', mahya='cimen', kalin=0.03,
                 kapilar=((-0.3, -1), (0.3, -1), (0.05, 1)), dumanlik=(-0.38, 0.38), ejder_s=0.17, sirt=0.09, nr=12,
                 kalkanlar=(-1, 1), egri=0.1, sundurma_h=0.68, sundurma_c=0.065, kroker=0.075, uc_kapi=(-1,),
                 yama=12, tohum=3, cati_merdiven=((0.6, -1),), saz_cizgi=3,
                 dilim=['saz_koyu'] + ['saz', 'saz', 'saz_koyu'] * 3 + ['saz', 'cimen'])

# ---------------- fence and gate ----------------
y.bolum('Örgü çit ve kapı')
GW = 0.1
for a, b in (((-FX, -FY), (-GW, -FY)), ((GW, -FY), (FX, -FY)), ((FX, -FY), (FX, FY)), ((FX, FY), (-FX, FY)), ((-FX, FY), (-FX, -FY))):
    cit_orgu(y, a, b, Z0, 0.065)
for sx in (-1, 1):
    y.prizma((sx * GW, -FY), 0.012, Z0, Z0 + 0.17, 'kutuk', n=8)
    kure(y, (sx * GW, -FY, Z0 + 0.176), 0.014, 'ahsap_koyu', n=8, kat=4)
cubuk(y, V(-GW - 0.03, -FY, Z0 + 0.15), V(GW + 0.03, -FY, Z0 + 0.15), 0.016, 'ahsap_koyu', 0.016)
kutu_merkez(y, (0, -FY - 0.009), 0.1, 0.004, 0.022, 'boya_kirmizi', z0=Z0 + 0.118)
kutu_merkez(y, (0, -FY - 0.0112), 0.08, 0.002, 0.008, 'boya_sari', z0=Z0 + 0.125)
for sx in (-1, 1):   # the gate's two hurdles, swung open
    d = V(sx * 0.35, 1).normalized()
    kutu(y, V(sx * GW, -FY, Z0 + 0.01) + V(-d.y, d.x) * 0.003 * sx, d, GW * 0.95, 0.006, 0.06, 'ahsap_acik')


# ---------------- storehouse on stones ----------------
def stabbur(c, aci):
    with parca(y, (c[0], c[1], 0), aci):
        w, d, zf = 0.2, 0.15, Z0 + 0.06
        for sx in (-1, 1):
            for sy in (-1, 1):
                kutu_merkez(y, (sx * w * 0.42, sy * d * 0.4), 0.04, 0.04, 0.03, 'granit', z0=Z0)
                y.prizma((sx * w * 0.42, sy * d * 0.4), 0.012, Z0 + 0.03, zf, 'kutuk', n=6)
        kutu_merkez(y, (0, 0), w + 0.03, d + 0.03, 0.012, 'ahsap', z0=zf)
        kutuk_ev(y, -w / 2, w / 2, -d / 2, d / 2, zf + 0.012, 0.11, r=0.011, key='kutuk', cati_key='cimen', cati_h=0.08, sacak=0.03)
        merdiven(y, (0, -d / 2 - 0.1), math.pi / 2, 0.05, Z0, zf + 0.012, n=4, key='ahsap')


y.bolum('Ambar')
stabbur((-0.8, -0.55), 0.0)

y.bolum('Odun yığınları')
odun_yigini(y, (-0.45, -0.22, Z0), math.pi / 2, L=0.2, n=6, kat=4)
odun_yigini(y, (0.55, 0.62, Z0), math.pi / 2, L=0.24, n=6, kat=5)
odun_yigini(y, (-0.98, 0.56, Z0), 0.0, L=0.18, n=5, kat=4)
# a chopping block with an axe
y.prizma((-0.3, -0.33), 0.022, Z0, Z0 + 0.03, 'kutuk', n=8, ust_renk='ahsap_acik')
cubuk(y, V(-0.3, -0.33, Z0 + 0.03), V(-0.33, -0.36, Z0 + 0.08), 0.005, 'ahsap')
kutu_merkez(y, (-0.3, -0.33), 0.02, 0.004, 0.018, 'demir', z0=Z0 + 0.026, aci=0.8)

y.bolum('Bostan ve araba')
GX0, GX1, GY0, GY1 = -0.56, -0.2, -0.8, -0.56
yer([(GX0, GY0), (GX1, GY0), (GX1, GY1), (GX0, GY1)])
for k in range(4):
    yy = GY0 + 0.035 + k * 0.057
    kutu(y, V(GX0 + 0.02, yy - 0.012, Z0), X, GX1 - GX0 - 0.04, 0.024, 0.012, 'toprak', 'onarkasagsolust')
    for i in range(7):
        x = GX0 + 0.04 + i * 0.047
        kure(y, (x, yy, Z0 + 0.019), 0.011 if k % 2 else 0.009, 'boya_yesil' if k != 2 else 'zeytin', n=6, kat=3)
cit_orgu(y, (GX0, GY1 + 0.02), (GX0, GY0), Z0, 0.045)
cit_orgu(y, (GX1, GY1 + 0.02), (GX0, GY1 + 0.02), Z0, 0.045)
with parca(y, (-0.5, -0.4, 0), math.pi - 0.35):
    for sy in (-1, 1):
        boru(y, [V(0, sy * 0.045, Z0 + 0.032), V(0, sy * 0.053, Z0 + 0.032)], 0.032, 'ahsap_koyu', n=10)
        kure(y, (0, sy * 0.056, Z0 + 0.032), 0.007, 'demir', n=6, kat=3)
    cubuk(y, V(0, -0.05, Z0 + 0.032), V(0, 0.05, Z0 + 0.032), 0.008, 'ahsap_koyu')
    kutu_merkez(y, (0.0, 0), 0.13, 0.08, 0.012, 'ahsap', z0=Z0 + 0.045)
    for sy in (-1, 1):
        kutu_merkez(y, (0.0, sy * 0.037), 0.13, 0.006, 0.025, 'ahsap_acik', z0=Z0 + 0.057)
    for sy in (-1, 1):
        cubuk(y, V(0.06, sy * 0.025, Z0 + 0.05), V(0.2, sy * 0.022, Z0 + 0.008), 0.007, 'ahsap')
    odun_yigini(y, (0.0, 0.0, Z0 + 0.057), math.pi / 2, L=0.1, n=3, r=0.009, kat=2)

y.bolum('Balık kurutma rafları')
hjell(y, (0.42, -0.68, Z0), 0.0, L=0.28, h=0.13)
hjell(y, (0.78, -0.72, Z0), 0.0, L=0.26, h=0.13, mal='siva_krem', n=5)


# ---------------- well with a sweep ----------------
def kuyu(c):
    cx, cy = c
    r0, r1, hh = 0.045, 0.03, 0.045
    dis = cokgen(c, r0, 12); ic = cokgen(c, r1, 12)
    duvarlar(y, dis, Z0, Z0 + hh, 'granit')
    for i in range(12):
        j = (i + 1) % 12
        duz_duvar(y, ic[j], ic[i], Z0 + 0.01, Z0 + hh, 'granit_koyu')
        y.yuz_yon([dis[i] + Z * (Z0 + hh), dis[j] + Z * (Z0 + hh), ic[j] + Z * (Z0 + hh), ic[i] + Z * (Z0 + hh)], 'granit', Z)
    y.yuz_yon([V(p.x, p.y, Z0 + 0.01) for p in ic], 'su', Z)
    # the sweep: a forked post, a long pole on it, a rope and a bucket
    px = cx + 0.1
    y.prizma((px, cy), 0.008, Z0, Z0 + 0.17, 'kutuk', n=6)
    a, b = V(cx + 0.2, cy, Z0 + 0.06), V(cx - 0.01, cy, Z0 + 0.25)
    cubuk(y, a, b, 0.008, 'ahsap')
    kutu_merkez(y, (a.x - 0.01, a.y), 0.03, 0.03, 0.03, 'granit', z0=a.z - 0.03)
    cubuk(y, b, V(cx - 0.01, cy, Z0 + 0.09), 0.002, 'ahsap_koyu')
    donel(y, (cx - 0.01, cy), [(0.0, Z0 + 0.07), (0.012, Z0 + 0.07), (0.014, Z0 + 0.09), (0.0, Z0 + 0.09)], 'ahsap_acik', n=8)


y.bolum('Kuyu')
kuyu((0.2, -0.62))

y.bolum('Koyun ağılı')
PX0, PX1, PY0, PY1 = 0.66, 1.0, -0.44, -0.12
for a, b in (((PX0, PY0), (PX1, PY0)), ((PX0, PY1), (PX0, PY0))):
    cit_orgu(y, a, b, Z0, 0.05)
yer([(PX0, PY0), (PX1, PY0), (PX1, PY1), (PX0, PY1)])
for i, (sx, sy, a) in enumerate(((0.74, -0.3, 0.4), (0.85, -0.22, 2.5), (0.92, -0.36, -0.6), (0.78, -0.18, 3.6), (0.95, -0.25, 1.2))):
    koyun(y, sx, sy, Z0, a, 'kece' if i != 2 else 'siva_krem')
# a hay rack in the pen
for sx in (-1, 1):
    cubuk(y, V(0.93 + sx * 0.03, -0.42, Z0), V(0.93, -0.42 + 0.025 * 0, Z0 + 0.07), 0.006, 'ahsap')
donel(y, (0.93, -0.405), [(0.03, Z0), (0.026, Z0 + 0.03), (0.0, Z0 + 0.04)], 'saz', n=8)


# ---------------- smithy lean-to ----------------
y.bolum('Demirci sundurması')
with parca(y, (-0.72, 0.72, 0), 0.0):
    w, d = 0.26, 0.16
    for sx in (-1, 1):
        y.prizma((sx * w / 2, -d / 2), 0.01, Z0, Z0 + 0.12, 'kutuk', n=6)
        y.prizma((sx * w / 2, d / 2), 0.01, Z0, Z0 + 0.16, 'kutuk', n=6)
    duz_duvar(y, V(w / 2, d / 2), V(-w / 2, d / 2), Z0, Z0 + 0.16, 'ahsap_dikey')
    duz_duvar(y, V(-w / 2, d / 2 - 0.004), V(w / 2, d / 2 - 0.004), Z0, Z0 + 0.16, 'ahsap_koyu')
    # the turf shed roof: slope from the back down to the front
    ra, rb = Z0 + 0.175, Z0 + 0.125
    q = [V(-w / 2 - 0.03, -d / 2 - 0.04, rb), V(w / 2 + 0.03, -d / 2 - 0.04, rb), V(w / 2 + 0.03, d / 2 + 0.03, ra), V(-w / 2 - 0.03, d / 2 + 0.03, ra)]
    y.yuz_yon(q, 'cimen', Z)
    y.yuz_yon([q[0], q[1], q[1] - Z * 0.02, q[0] - Z * 0.02], 'ahsap_koyu', -Y)
    y.yuz_yon([q[2], q[3], q[3] - Z * 0.02, q[2] - Z * 0.02], 'ahsap_koyu', Y)
    y.yuz_yon([p - Z * 0.02 for p in q], 'ahsap_koyu', -Z)
    for sx in (-1, 1):
        y.yuz_yon([V(sx * (w / 2 + 0.03), -d / 2 - 0.04, rb), V(sx * (w / 2 + 0.03), d / 2 + 0.03, ra), V(sx * (w / 2 + 0.03), d / 2 + 0.03, ra - 0.02), V(sx * (w / 2 + 0.03), -d / 2 - 0.04, rb - 0.02)], 'ahsap_koyu', V(sx, 0))
    # hearth with glowing coals, bellows, anvil on a stump
    kutu_merkez(y, (-0.05, 0.03), 0.09, 0.07, 0.05, 'granit', z0=Z0)
    kutu_merkez(y, (-0.05, 0.03), 0.06, 0.04, 0.004, 'boya_kirmizi', z0=Z0 + 0.05)
    kutu_merkez(y, (-0.05, 0.03), 0.03, 0.02, 0.004, 'boya_sari', z0=Z0 + 0.053)
    y.prizma((0.07, -0.02), 0.018, Z0, Z0 + 0.035, 'kutuk', n=8)
    kutu_merkez(y, (0.07, -0.02), 0.04, 0.018, 0.016, 'demir', z0=Z0 + 0.035)
    kutu_merkez(y, (-0.12, 0.04), 0.04, 0.03, 0.02, 'ahsap_koyu', z0=Z0 + 0.02, aci=0.3)
    # a chimney hood of stone through the roof
    kutu_merkez(y, (-0.05, 0.05), 0.05, 0.04, 0.18, 'granit', z0=Z0 + 0.05)
    kutu_merkez(y, (-0.05, 0.05), 0.026, 0.018, 0.003, 'koyu', z0=Z0 + 0.23)

y.bolum('Saman tınazları')
for (hx, hy, s) in ((0.78, 0.66, 1.0), (0.9, 0.76, 0.85)):
    donel(y, (hx, hy), [(0.0, Z0), (0.06 * s, Z0), (0.065 * s, Z0 + 0.06 * s), (0.045 * s, Z0 + 0.12 * s), (0.0, Z0 + 0.15 * s)], 'saz', n=12)
    y.prizma((hx, hy), 0.004, Z0 + 0.14 * s, Z0 + 0.19 * s, 'ahsap', n=4)
    for k in range(4):   # ropes round the rick
        t = TAU * k / 4 + 0.4
        cubuk(y, V(hx + 0.066 * s * math.cos(t), hy + 0.066 * s * math.sin(t), Z0 + 0.04 * s), V(hx + 0.02 * s * math.cos(t), hy + 0.02 * s * math.sin(t), Z0 + 0.145 * s), 0.003, 'ahsap_koyu')

y.bolum('Ladinler')
for (tx, ty, b) in ((-1.0, 0.82, 0.36), (-0.82, 0.88, 0.3), (1.02, 0.12, 0.32), (-1.02, -0.82, 0.3), (0.3, 0.84, 0.28), (-0.3, 0.86, 0.26)):
    cam_agaci(y, tx, ty, Z0, b, 'boya_yesil')

y.bolum('Sancak')
sancak(y, -0.12, -0.34, Z0, boy=0.5, en=0.13, yuk=0.08, aci=math.pi + 0.5, direk_key='ahsap_koyu', kuyruk=True)
# a carved post pair flanking the path, topped with heads
for sx in (-1, 1):
    y.prizma((sx * 0.1, -0.5), 0.01, Z0, Z0 + 0.14, 'ahsap_koyu', n=6)
    kutu_merkez(y, (sx * 0.1, -0.5), 0.026, 0.026, 0.008, 'boya_kirmizi', z0=Z0 + 0.1)
    ejder(y, V(sx * 0.1, -0.5, Z0 + 0.135), V(0, -1), 0.06)

calistir(y, 'lm_uzunev')
