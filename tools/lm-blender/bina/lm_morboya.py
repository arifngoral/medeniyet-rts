# Mor Boya Atölyesi (lm_morboya): a Tyrian-purple dye works on the shore: a paved quay yard with rows of dye vats,
# bronze cauldrons boiling on hearths, racks of purple cloth drying, a colonnaded dye hall and whitewashed store
# houses under a tall Punic store tower; mountains of crushed murex shells on the beach, a wooden jetty with
# merchant boats and a fishing boat drawn up on the sand.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from kartaca_ortak import kavetto, KAVETTO, pon_ev, iyon_hafif, tanit_kabartma, kanatli_gunes, gemi, insan, pencere_kutu
from kartaca_ek import *
from bina_ortak import calistir
import doku

y = Yapi()
rn = random.Random(11)
Z0 = 0.05          # land
SU = 0.03          # water surface
PZ = Z0 + 0.014    # the paved yard
GX0, GX1, GY0, GY1 = -1.2, 1.2, -1.1, 1.1
NX, NY = 36, 33
QX, QY = 0.2, -0.5            # the quay: x <= QX, its front at y = QY
TEPELER = [(0.8, 0.36, 0.36, 0.3, 0.32), (0.98, -0.12, 0.22, 0.15, 0.2), (0.55, 0.86, 0.24, 0.17, 0.18)]   # cx, cy, R, H, Ry


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def yuk(x, yy):
    if x <= QX + 1e-6:
        return 0.0 if yy < QY - 1e-6 else Z0
    s0 = -0.72 + 0.05 * math.sin(3.1 * x + 0.4)
    z = Z0 * _ss(s0, -0.3, yy)
    z += 0.006 * math.sin(6 * x + 2) * math.cos(5 * yy) * _ss(-0.3, 0.0, yy)
    return z


# ---------------- ground: sea bed, beach, land ----------------
y.bolum('Kıyı ve deniz')


def arazi_renk(x, yy, z):
    n = 0.5 + 0.5 * (math.sin(x * 5.3 + 1.0) * math.cos(yy * 4.1 - 0.4) * 0.7 + math.sin(x * 11 - yy * 7) * 0.3)
    kuru = (0.74, 0.66, 0.48)
    c = tuple(p + (q - p) * n * 0.5 for p, q in zip(kuru, (0.68, 0.62, 0.42)))
    kum = (0.88, 0.81, 0.63)
    c = tuple(p + (q - p) * _ss(Z0 - 0.002, Z0 - 0.02, z) for p, q in zip(c, kum))     # sand towards the water
    islak = (0.58, 0.55, 0.45)
    c = tuple(p + (q - p) * _ss(SU + 0.004, SU - 0.01, z) for p, q in zip(c, islak))   # wet sand, the sea bed
    # purple-stained earth round the shell heaps (the dye works' waste)
    for cx, cy, R, H, Ry in TEPELER:
        d = math.hypot((x - cx) / (R * 1.5), (yy - cy) / (Ry * 1.5))
        c = tuple(p + (q - p) * 0.35 * (1 - _ss(0.6, 1.0, d)) for p, q in zip(c, (0.6, 0.48, 0.5)))
    return c


doku.KOSE_RENK['toprak_ot'] = arazi_renk
P = [[V(GX0 + (GX1 - GX0) * i / NX, GY0 + (GY1 - GY0) * j / NY, 0) for j in range(NY + 1)] for i in range(NX + 1)]
for i in range(NX + 1):
    for j in range(NY + 1):
        P[i][j].z = yuk(P[i][j].x, P[i][j].y)


def avlu_ici(p):
    return p.x <= QX + 1e-6 and QY - 1e-6 <= p.y <= 0.98 + 1e-6


for i in range(NX):
    for j in range(NY):
        q = [P[i][j], P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]]
        if all(avlu_ici(p) for p in q): continue          # (under the paved yard)
        dg = (i + j) % 2 == 0
        for tri in (([q[0], q[1], q[2]], [q[0], q[2], q[3]]) if dg else ([q[0], q[1], q[3]], [q[1], q[2], q[3]])):
            y.yuz_yon(tri, 'toprak_ot', Z)
# the skirt: soil / rock under the land, water face where the sea meets the edge
kenar = [P[i][0] for i in range(NX)] + [P[NX][j] for j in range(NY)] + [P[i][NY] for i in range(NX, 0, -1)] + [P[0][j] for j in range(NY, 0, -1)]
for k in range(len(kenar)):
    a, b = kenar[k], kenar[(k + 1) % len(kenar)]
    if avlu_ici(a) and avlu_ici(b) and abs(a.x - GX0) < 1e-6: continue     # (the yard's own side is the edge there)
    e = (b - a); e.z = 0; e.normalize(); nn = V(e.y, -e.x)
    if a.z > 1e-4 or b.z > 1e-4:
        y.yuz_yon([V(a.x, a.y, 0), V(b.x, b.y, 0), b, a], 'kaya_koyu', nn)
    if a.z < SU or b.z < SU:
        y.yuz_yon([V(a.x, a.y, max(0, min(a.z, SU))), V(b.x, b.y, max(0, min(b.z, SU))), V(b.x, b.y, SU), V(a.x, a.y, SU)], 'su', nn)
# the sea surface, in cells (the shadow lives in the corners)
for i in range(16):
    for j in range(6):
        x0, x1 = GX0 + (GX1 - GX0) * i / 16, GX0 + (GX1 - GX0) * (i + 1) / 16
        y0 = GY0 + (-0.28 - GY0) * j / 6; y1 = GY0 + (-0.28 - GY0) * (j + 1) / 6
        if x1 <= QX + 1e-6: y1 = min(y1, QY)
        if y1 - y0 < 1e-6: continue
        if all(yuk(px, py) > SU + 0.004 for px in (x0, x1) for py in (y0, y1)): continue
        y.yuz_yon([V(x0, y0, SU), V(x1, y0, SU), V(x1, y1, SU), V(x0, y1, SU)], 'su', Z)
# a line of surf along the beach
for k in range(40):
    x = QX + 0.02 + (GX1 - 0.02 - QX) * k / 40
    lo, hi = -1.0, -0.3
    for _ in range(30):
        m = (lo + hi) / 2
        if yuk(x, m) < SU: lo = m
        else: hi = m
    if k % 2 == 0:
        x2 = x + (GX1 - 0.02 - QX) / 40
        lo2, hi2 = -1.0, -0.3
        for _ in range(30):
            m = (lo2 + hi2) / 2
            if yuk(x2, m) < SU: lo2 = m
            else: hi2 = m
        cubuk(y, V(x, lo - 0.012, SU + 0.002), V(x2, lo2 - 0.012, SU + 0.002), 0.01, 'beyaz', 0.002)

# ---------------- the paved quay yard ----------------
y.bolum('Rıhtım avlusu')
kutu(y, V(GX0, QY, 0), X, QX - GX0, 0.98 - QY, PZ, 'tas', 'onarkasagsol')
for i in range(8):        # (the yard's top in cells)
    for j in range(8):
        xa, xb = GX0 + (QX - GX0) * i / 8, GX0 + (QX - GX0) * (i + 1) / 8
        ya, yb = QY + (0.98 - QY) * j / 8, QY + (0.98 - QY) * (j + 1) / 8
        y.yuz_yon([V(xa, ya, PZ), V(xb, ya, PZ), V(xb, yb, PZ), V(xa, yb, PZ)], 'zemin', Z)
silme(y, [V(QX, QY), V(GX0, QY)][::-1], PZ - 0.008, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
silme(y, [V(QX, QY), V(QX, 0.98)], PZ - 0.008, 0.008, 0.006, 'tas_acik', 'duz', kapali=False)
# mooring bollards and a stair down to the water
for x in (-1.05, -0.62, 0.0):
    donel(y, (x, QY + 0.025), [(0.008, PZ), (0.007, PZ + 0.014), (0.0095, PZ + 0.02), (0.0, PZ + 0.024)], 'tas_koyu', n=8)
merdiven(y, (-0.82, QY - 0.07), math.pi / 2, 0.08, 0, PZ, n=6, d=0.012, key='tas_koyu')

# ---------------- the jetty and the boats ----------------
y.bolum('İskele ve tekneler')
JX = -0.3
for k in range(6):
    for sx in (-1, 1):
        y.prizma((JX + sx * 0.032, QY - 0.06 - k * 0.065), 0.0055, 0.0, 0.047, 'ahsap_koyu', n=6, ust=False)
kutu(y, V(JX - 0.04, QY - 0.4, 0.047), X, 0.08, 0.4, 0.009, 'ahsap_acik', 'onsagsolust')
for k in range(9):    # plank seams
    cubuk(y, V(JX - 0.04, QY - 0.03 - k * 0.042, 0.0565), V(JX + 0.04, QY - 0.03 - k * 0.042, 0.0565), 0.003, 'ahsap', 0.001)
_g0 = len(y.faces)
gemi(y, (JX - 0.14, -0.78, SU), -math.pi / 2, 0.0, L=0.3, B=0.085, H=0.032, kurek=False, yelken=True, tur='ticaret', tohum=2)
for _i in range(_g0, len(y.faces)):   # (a Tyrian-purple sail: the merchant of the dye works)
    if y.faces[_i][1] == 'boya_kirmizi' and min(p[2] for p in y.faces[_i][0]) > SU + 0.05: y.faces[_i] = (y.faces[_i][0], 'mor')
gemi(y, (JX + 0.13, -0.76, SU), -math.pi / 2 + 0.06, 0.0, L=0.24, B=0.07, H=0.028, kurek=False, yelken=False, tur='ticaret', tohum=3)
gemi(y, (0.28, -0.98, SU), 0.25, 0.0, L=0.22, B=0.06, H=0.026, kurek=True, yelken=True, tur='ticaret', tohum=5)
bz = yuk(0.6, -0.45)
gemi(y, (0.6, -0.47, bz + 0.012), -1.25, 0.07, L=0.2, B=0.06, H=0.026, kurek=False, yelken=False, tur='ticaret', tohum=4)
# murex baskets and fishermen on the beach


def sepet(x, yy, z, r=0.016):
    donel(y, (x, yy), [(r * 0.75, z), (r, z + r * 0.9), (r * 1.05, z + r * 1.0), (r * 0.9, z + r * 1.0)], 'saz', n=9)
    ic_halka(y, (x, yy), r * 0.9, z + r * 0.7, z + r * 1.0, 'saz_koyu', n=9)
    y.yuz_yon([V(p.x, p.y, z + r * 0.7) for p in cokgen((x, yy), r * 0.9, 9)], 'kabuk', Z)
    for k in range(4):
        a = TAU * k / 4 + 0.3
        kure(y, (x + r * 0.45 * math.cos(a), yy + r * 0.45 * math.sin(a), z + r * 0.78), r * 0.22, 'boya_mor_acik' if k % 2 else 'kum_acik', n=5, kat=3)


for x, yy in ((0.47, -0.36), (0.5, -0.4), (0.73, -0.36), (0.36, -0.42), (0.42, -0.3)):
    sepet(x, yy, yuk(x, yy) - 0.002)
insan(y, 0.55, -0.35, yuk(0.55, -0.35), 'kumas', s=1.1, aci=2.2, kol=0.6, sapka='saz')
insan(y, 0.69, -0.42, yuk(0.69, -0.42), 'siva_oker', s=1.1, aci=-0.5)
insan(y, 0.38, -0.36, yuk(0.38, -0.36), 'kumas', s=1.1, aci=0.9, kol=0.8)

# ---------------- the murex shell heaps ----------------
y.bolum('Kabuk tepeleri')


def kabuk_renk(x, yy, z):
    n = math.sin(x * 23 + yy * 7) * math.cos(yy * 19 - x * 5) * 0.5 + 0.5
    m = math.sin(x * 9 - yy * 13 + 1.3) * 0.5 + 0.5
    c = (0.8 + 0.05 * n, 0.74 + 0.04 * n, 0.66 + 0.04 * n)        # bleached shell, greyer in the hollows
    c = tuple(p + (q - p) * (0.6 * m * m) for p, q in zip(c, (0.56, 0.44, 0.55)))   # violet stains
    c = tuple(p + (q - p) * (0.3 * _ss(Z0 + 0.06, Z0 - 0.01, z)) for p, q in zip(c, (0.58, 0.47, 0.44)))   # dark wet foot
    return c


doku.KOSE_RENK['kabuk'] = kabuk_renk
for t, (cx, cy, R, H, Ry) in enumerate(TEPELER):
    kabuk_tepe(y, cx, cy, Z0, R, H, n=40 if t == 0 else 30, nr=12 if t == 0 else 9, tohum=t + 1, Ry=Ry, kabuk_say=int(R * 420))
# workers carrying baskets of shells to the heaps, baskets and shovels at their feet
for x, yy, a, kk in ((0.4, 0.02, 0.6, 'siva_oker'), (0.55, -0.12, 1.2, 'kumas'), (0.72, -0.2, 2.0, 'siva_oker')):
    insan(y, x, yy, yuk(x, yy), kk, s=1.1, aci=a, sapka='saz', kol=0.5)
    sepet(x + 0.022, yy - 0.012, yuk(x, yy) - 0.002, 0.013)
for x, yy in ((0.46, -0.06), (0.66, -0.28)):
    zz = yuk(x, yy)
    cubuk(y, V(x, yy, zz - 0.005), V(x + 0.012, yy - 0.008, zz + 0.075), 0.004, 'ahsap')
    cubuk(y, V(x - 0.004, yy + 0.002, zz - 0.003), V(x + 0.006, yy - 0.004, zz + 0.012), 0.014, 'demir', 0.003)

# ---------------- the store tower ----------------
y.bolum('Depo kulesi')
TX, TY, TW = -0.84, 0.66, 0.28
zr, ztop = pon_kule(y, TX, TY, PZ, TW, TW, 4, 0.2, alt='kum', ust='siva', kornis='siva_krem', mazgal_h=0.03, pencere=2, kapi='ahsap_koyu')
# the rooftop room with its own cornice, the banner over it
kutu(y, V(TX - 0.07, TY - 0.03, zr), X, 0.13, 0.12, 0.09, 'siva', 'onarkasagsol')
pencere_kutu(y, V(TX - 0.07, TY - 0.03, zr), X, -Y, 0.045, 0.0, 0.03, 0.055, 'ahsap_koyu', cerceve='siva_krem')
kavetto(y, dikdortgen(TX - 0.07, TX + 0.06, TY - 0.03, TY + 0.09), zr + 0.09, 0.022, 0.013, 'siva_krem')
tanit_heykel_z = zr + 0.112
from kartaca_ortak import tanit_heykel
tanit_heykel(y, TX - 0.005, TY + 0.03, tanit_heykel_z, 0.05, 'bronz', aci=-math.pi / 2)
sancak(y, TX + 0.1, TY + 0.1, zr, boy=0.3, en=0.14, yuk=0.085, aci=-0.6)
# Tanit and the winged sun on the tower's front
tanit_kabartma(y, V(TX, TY - TW / 2, PZ + 0.62), X, -Y, 0.1, 'altin')
kanatli_gunes(y, V(TX, TY - TW / 2, PZ + 0.165), X, -Y, 0.11, 0.022)
# purple cloth hung from the upper windows
for kx, h in ((-0.07, 0.13), (0.07, 0.1)):
    levha_kapali(y, [V(TX + kx - 0.02, TY - TW / 2 - 0.004, PZ + 0.56 - h), V(TX + kx + 0.02, TY - TW / 2 - 0.004, PZ + 0.56 - h),
                     V(TX + kx + 0.02, TY - TW / 2 - 0.004, PZ + 0.56), V(TX + kx - 0.02, TY - TW / 2 - 0.004, PZ + 0.56)], 'boya_mor', -Y, 0.0016)

# ---------------- the dye hall (colonnaded) ----------------
y.bolum('Boyahane')
HX0, HX1, HY0, HY1, HH = -0.6, 0.16, 0.68, 0.95, 0.24
for k in range(6):
    a, b = V(HX0 + (HX1 - HX0) * k / 6, HY0), V(HX0 + (HX1 - HX0) * (k + 1) / 6, HY0)
    if k % 2 == 0:
        dikdortgen_acik(y, a, b, PZ, HH, 0.3, 0.7, 0.0, 0.15, ('siva', 'siva_krem', 'tas_acik', 'koyu'), derin=0.02, cerceve=(0.006, 'kum_acik'), ic_kenar=True)
    else:
        dikdortgen_acik(y, a, b, PZ, HH, 0.36, 0.64, 0.09, 0.15, ('siva', 'siva_krem', 'siva_krem', 'koyu'), derin=0.015, cerceve=(0.005, 'kum_acik'), ic_kenar=True)
duz_duvar(y, V(HX1, HY0), V(HX1, HY1), PZ, PZ + HH, 'siva')
duz_duvar(y, V(HX1, HY1), V(HX0, HY1), PZ, PZ + HH, 'siva')
duz_duvar(y, V(HX0, HY1), V(HX0, HY0), PZ, PZ + HH, 'siva')
for k in range(5):    # high windows on the sides and back
    pencere_kutu(y, V(HX1, HY0), Y, X, 0.04 + k * 0.05, 0.15, 0.014, 0.03, 'koyu', cerceve='siva_krem') if k < 4 else None
    pencere_kutu(y, V(HX1, HY1), -X, Y, 0.05 + k * 0.14, 0.15, 0.016, 0.034, 'koyu', cerceve='siva_krem')
kavetto(y, dikdortgen(HX0, HX1, HY0, HY1), PZ + HH, 0.035, 0.02, 'siva_krem')
parapet(y, disa(dikdortgen(HX0, HX1, HY0, HY1), 0.016), PZ + HH + 0.035, 0.012, 0.0, 0.012, 'siva')
# the portico in front: Ionic columns, an architrave with a cavetto cornice
PY = 0.585
NC = 9
for k in range(NC):
    x = HX0 + 0.025 + (HX1 - HX0 - 0.05) * k / (NC - 1)
    iyon_hafif(y, x, PY, PZ, PZ + 0.17, 0.011, 'siva', 'siva_krem')
kutu(y, V(HX0 - 0.005, PY - 0.018, PZ + 0.17), X, HX1 - HX0 + 0.01, HY0 - PY + 0.018, 0.026, 'siva_krem', 'onsagsolust')
silme(y, [V(HX0 - 0.005, PY - 0.018), V(HX1 + 0.005, PY - 0.018)], PZ + 0.196, 0.03, 0.018, 'siva_krem', KAVETTO, kapali=False)
y.yuz_yon([V(HX0 - 0.005, PY - 0.018, PZ + 0.226), V(HX1 + 0.005, PY - 0.018, PZ + 0.226), V(HX1 + 0.005, HY0, PZ + 0.226), V(HX0 - 0.005, HY0, PZ + 0.226)], 'zemin', Z)
y.yuz_yon([V(HX0 - 0.005, PY - 0.018, PZ + 0.17), V(HX1 + 0.005, PY - 0.018, PZ + 0.17), V(HX1 + 0.005, HY0, PZ + 0.17), V(HX0 - 0.005, HY0, PZ + 0.17)], 'siva_krem', -Z)
# the architrave's painted frieze: a purple band with gold and red rosettes
silme(y, [V(HX0 - 0.005, PY - 0.018), V(HX1 + 0.005, PY - 0.018)], PZ + 0.176, 0.008, 0.0025, 'mor', 'duz', kapali=False)
for k in range(15):
    x = HX0 + 0.02 + (HX1 - HX0 - 0.04) * k / 14
    kure(y, (x, PY - 0.018 - 0.0012, PZ + 0.189), 0.0045, 'altin' if k % 2 else 'boya_kirmizi', n=6, kat=3)
# pilasters along the sides and the back
for (a, b) in ((V(HX1, HY0), V(HX1, HY1)), (V(HX1, HY1), V(HX0, HY1)), (V(HX0, HY1), V(HX0, HY0))):
    L = (b - a).length; e = (b - a) / L; nrm = V(e.y, -e.x)
    m = max(2, int(L / 0.13))
    for k in range(m + 1):
        p = a.lerp(b, k / m)
        kutu(y, p - e * 0.011 + Z * PZ, e, 0.022, -0.008, HH, 'siva_krem', 'arkasagsolust') if 0 < k < m else None
    for k in range(m):   # a small window between the pilasters on the back
        if (b - a).x < 0:
            pencere_kutu(y, a, e, nrm, L * (k + 0.5) / m - 0.009, 0.15, 0.018, 0.034, 'koyu', cerceve='siva_krem')
# a clerestory lantern on the roof (light for the vats) and cloth drying on the roof terrace
RZ = PZ + HH + 0.035
LX0, LX1, LY0, LY1 = -0.46, -0.02, 0.75, 0.89
duvarlar(y, dikdortgen(LX0, LX1, LY0, LY1), RZ, RZ + 0.075, 'siva')
for i, (a, b) in enumerate(((V(LX0, LY0), V(LX1, LY0)), (V(LX1, LY1), V(LX0, LY1)))):
    L = (b - a).length; e = (b - a) / L
    for k in range(6):
        pencere_kutu(y, a, e, V(e.y, -e.x), L * (k + 0.5) / 6 - 0.01, 0.022, 0.02, 0.035, 'koyu', cerceve='siva_krem')
kavetto(y, dikdortgen(LX0, LX1, LY0, LY1), RZ + 0.075, 0.026, 0.015, 'siva_krem')
for k in range(2):
    xx = 0.03 + k * 0.06
    kumas_as(y, (xx, 0.73), (xx, 0.91), RZ, 0.1, ['boya_mor', 'mor', 'boya_mor_acik'], n=3, tohum=k + 9)
kumas_as(y, (-0.58, 0.72), (-0.48, 0.72), RZ, 0.09, ['mor', 'boya_mor'], n=2, tohum=4)
# a reed awning on poles shading the western end of the roof terrace, amphorae of dye under it
for x in (-0.585, -0.485):
    for yy in (0.765, 0.915):
        y.prizma((x, yy), 0.0035, RZ, RZ + 0.1, 'ahsap', n=5, ust=False)
cati_besik(y, -0.592, -0.478, 0.758, 0.922, RZ + 0.1, 0.03, sacak=0.012, key='saz', mahya='saz_koyu', ucluk_key='ahsap_acik', kalinlik=0.005,
           nr=2, ns=3)
for k in range(4):
    x0 = -0.565 + (k % 2) * 0.022
    y0 = 0.8 + (k // 2) * 0.05
    donel(y, (x0, y0), [(0.0, RZ), (0.004, RZ + 0.004), (0.009, RZ + 0.02), (0.008, RZ + 0.03), (0.004, RZ + 0.036),
                        (0.0035, RZ + 0.044), (0.005, RZ + 0.046), (0.0, RZ + 0.047)], 'kiremit', n=8)
# purple cloth hung under the portico, vats inside the doors
for k in range(4):
    x = HX0 + 0.08 + k * 0.19
    kumas_as(y, (x - 0.06, PY + 0.05), (x + 0.06, PY + 0.05), PZ, 0.13, ['boya_mor', 'mor', 'boya_mor_acik'], n=2, tohum=k)

# ---------------- store houses on the west side ----------------
y.bolum('Ambarlar')
for k, (cx, cy, w, d, h) in enumerate(((-1.07, 0.25, 0.2, 0.2, 0.17), (-1.08, 0.03, 0.18, 0.2, 0.13), (-0.48, 0.36, 0.16, 0.12, 0.12))):
    pon_ev(y, cx, cy, PZ, w, d, h, aci=-math.pi / 2 if k < 2 else 0.0, tohum=k + 3, katlar=1)
# amphorae stacked at the quay


def amfora(x, yy, z, s=1.0):
    donel(y, (x, yy), [(0.0, z), (0.003 * s, z + 0.004 * s), (0.009 * s, z + 0.02 * s), (0.008 * s, z + 0.03 * s), (0.004 * s, z + 0.036 * s),
                       (0.0035 * s, z + 0.044 * s), (0.005 * s, z + 0.046 * s), (0.0, z + 0.047 * s)], 'kiremit', n=8)


for i in range(5):
    for j in range(2):
        amfora(0.02 + i * 0.022, QY + 0.04 + j * 0.022, PZ)
for i in range(4):
    amfora(0.031 + i * 0.022, QY + 0.051, PZ + 0.03, 0.95)

# ---------------- the dye vats ----------------
y.bolum('Boya tekneleri')
SIVI = ['boya_mor', 'mor', 'lake_koyu', 'boya_mor_acik', 'mor', 'boya_mor']
for i in range(4):
    for j in range(3):
        cx, cy = -0.7 + i * 0.17, -0.37 + j * 0.105
        tekne(y, cx, cy, PZ, 0.13, 0.072, 0.034, SIVI[(i + 2 * j) % len(SIVI)], 'kum')
for k, (x, yy, a) in enumerate(((-0.62, -0.21, 2.0), (-0.36, -0.42, 1.2), (-0.2, -0.24, -2.4), (-0.45, -0.09, 0.4))):
    insan(y, x, yy, PZ, ['kumas', 'siva_oker', 'beyaz', 'kumas'][k], s=1.1, aci=a, kol=0.9, sapka='saz' if k % 2 else None)
    cubuk(y, V(x + 0.004, yy + 0.01, PZ + 0.035), V(x + 0.03 * math.cos(a), yy + 0.03 * math.sin(a), PZ + 0.02), 0.0028, 'ahsap')

# ---------------- the cauldrons ----------------
y.bolum('Kazanlar')
for i in range(3):
    for j in range(2):
        kazan(y, -0.34 + i * 0.15, 0.13 + j * 0.15, PZ, 0.036, ['boya_mor', 'mor', 'lake_koyu'][(i + j) % 3], buhar=1 + (i + j) % 2, tohum=i * 3 + j)
# firewood stacks
for k in range(3):
    for m in range(4):
        cubuk(y, V(0.05, 0.08 + k * 0.012 + m * 0.002, PZ + 0.006 + m * 0.01), V(0.14, 0.08 + k * 0.012 + m * 0.002, PZ + 0.006 + m * 0.01), 0.009, 'ahsap' if (k + m) % 2 else 'ahsap_koyu')
insan(y, -0.27, 0.06, PZ, 'siva_oker', s=1.1, aci=1.6, kol=1.0)
insan(y, -0.05, 0.36, PZ, 'kumas', s=1.1, aci=-2.2)

# ---------------- drying racks ----------------
y.bolum('Kurutma sergileri')
RENK = ['boya_mor', 'mor', 'boya_mor_acik', 'lake_koyu', 'boya_mor']
for k in range(4):
    yy = -0.42 + k * 0.12
    kumas_as(y, (-1.16, yy), (-0.84, yy), PZ, 0.15, RENK, n=4, tohum=k)
for k in range(2):
    xx = -0.06 + k * 0.12
    kumas_as(y, (xx, -0.42), (xx, -0.12), PZ, 0.14, RENK, n=3, tohum=k + 5)
insan(y, -0.78, -0.3, PZ, 'beyaz', s=1.1, aci=3.0, kol=1.0)

# ---------------- the yard wall towards the beach, a reed-roofed shed ----------------
y.bolum('Avlu duvarı ve sundurma')
WT = 0.024
for ya, yb in ((-0.3, -0.07), (0.04, 0.98)):
    kutu(y, V(QX - WT, ya, PZ), X, WT, yb - ya, 0.075, 'kum', 'onarkasagsol')
    kavetto(y, dikdortgen(QX - WT, QX, ya, yb), PZ + 0.075, 0.016, 0.008, 'siva_krem')
    for yy in (ya, yb):   # piers at the ends
        kutu_merkez(y, (QX - WT / 2, yy), 0.036, 0.036, 0.1, 'kum', z0=PZ)
        kavetto(y, dikdortgen(QX - WT / 2 - 0.018, QX - WT / 2 + 0.018, yy - 0.018, yy + 0.018), PZ + 0.1, 0.016, 0.008, 'siva_krem')
tanit_kabartma(y, V(QX + 0.018, -0.07, PZ + 0.045), Y, X, 0.04, 'altin')
SX0, SX1, SY0, SY1 = -0.13, 0.12, 0.4, 0.53
for x in (SX0, (SX0 + SX1) / 2, SX1):
    for yy in (SY0, SY1):
        y.prizma((x, yy), 0.0045, PZ, PZ + 0.11, 'ahsap', n=6, ust=False)
cati_besik(y, SX0, SX1, SY0, SY1, PZ + 0.11, 0.035, sacak=0.02, key='saz', mahya='saz_koyu', ucluk_key='ahsap_acik', kalinlik=0.006, nr=3, ns=4)
for k in range(2):
    tekne(y, SX0 + 0.065 + k * 0.12, (SY0 + SY1) / 2, PZ, 0.1, 0.07, 0.03, ['mor', 'boya_mor_acik'][k], 'kum')
insan(y, 0.0, 0.43, PZ, 'beyaz', s=1.1, aci=1.5, kol=0.8)

# ---------------- shell crushing, a fisherman's hut, nets ----------------
y.bolum('Kabuk dövme ve balıkçı')
for k, (x, yy) in enumerate(((0.29, 0.1), (0.37, 0.03), (0.28, -0.03))):
    zb = yuk(x, yy)
    donel(y, (x, yy), [(0.02, zb - 0.003), (0.024, zb + 0.012), (0.026, zb + 0.026), (0.02, zb + 0.026)], 'tas_koyu', n=10)
    ic_halka(y, (x, yy), 0.02, zb + 0.016, zb + 0.026, 'tas', n=10)
    y.yuz_yon([V(p.x, p.y, zb + 0.016) for p in cokgen((x, yy), 0.02, 10)], 'boya_mor_acik', Z)
    a = 0.8 + k * 2.1
    px, py = x + 0.035 * math.cos(a), yy + 0.035 * math.sin(a)
    insan(y, px, py, yuk(px, py), ['kumas', 'siva_oker', 'kumas'][k], s=1.1, aci=a + math.pi, kol=1.0, sapka='saz' if k == 1 else None)
    cubuk(y, V(x + 0.012 * math.cos(a), yy + 0.012 * math.sin(a), zb + 0.02), V(px - 0.008 * math.cos(a), py - 0.008 * math.sin(a), zb + 0.07), 0.005, 'ahsap')
pon_ev(y, 0.33, 0.45, yuk(0.33, 0.45) - 0.002, 0.1, 0.12, 0.085, aci=math.pi / 2, tohum=12, kat2=False)
kumas_as(y, (0.27, 0.36), (0.27, 0.27), yuk(0.27, 0.3), 0.08, ['saz', 'saz_koyu'], n=2, tohum=2, sarkma=0.9)
# a hoist on the tower: a beam out of the top storey, a rope, a bale of purple cloth on its way up
HZ = PZ + 0.72
cubuk(y, V(TX - TW / 2 + 0.02, TY, HZ), V(TX - TW / 2 - 0.11, TY, HZ), 0.016, 'ahsap_koyu')
cubuk(y, V(TX - TW / 2 - 0.002, TY, HZ - 0.1), V(TX - TW / 2 - 0.08, TY, HZ - 0.005), 0.009, 'ahsap_koyu')
donel(y, (TX - TW / 2 - 0.1, TY), [(0.0, HZ - 0.022), (0.011, HZ - 0.018), (0.011, HZ - 0.01), (0.0, HZ - 0.008)], 'ahsap', n=8)
cubuk(y, V(TX - TW / 2 - 0.1, TY, HZ - 0.02), V(TX - TW / 2 - 0.1, TY, PZ + 0.34), 0.0025, 'saz_koyu')
kutu_merkez(y, (TX - TW / 2 - 0.1, TY), 0.05, 0.04, 0.045, 'boya_mor', z0=PZ + 0.3)
for dz in (0.012, 0.033):
    kutu_merkez(y, (TX - TW / 2 - 0.1, TY), 0.052, 0.042, 0.004, 'saz_koyu', z0=PZ + 0.3 + dz)
insan(y, TX - TW / 2 - 0.06, TY - 0.08, PZ, 'siva_oker', s=1.1, aci=2.6, kol=1.0)
# bolts of finished purple cloth on the quay, a merchant weighing them
for k, (dx, dz) in enumerate(((0, 0), (0.024, 0), (0.048, 0), (0.012, 0.02), (0.036, 0.02), (0.024, 0.04))):
    x0 = -0.56 + dx
    boru(y, [V(x0, QY + 0.035, PZ + 0.011 + dz), V(x0, QY + 0.085, PZ + 0.011 + dz)], 0.011, ['boya_mor', 'mor', 'boya_mor_acik', 'lake_koyu'][k % 4], n=8)
kutu_merkez(y, (-0.45, QY + 0.06), 0.07, 0.045, 0.004, 'ahsap', z0=PZ + 0.035)
for dx in (-0.03, 0.03):
    y.prizma((-0.45 + dx, QY + 0.06), 0.004, PZ, PZ + 0.035, 'ahsap_koyu', n=4, ust=False)
y.prizma((-0.45, QY + 0.06), 0.002, PZ + 0.039, PZ + 0.07, 'bronz', n=4)
cubuk(y, V(-0.475, QY + 0.06, PZ + 0.07), V(-0.425, QY + 0.06, PZ + 0.07), 0.003, 'bronz')
for dx in (-0.025, 0.025):
    donel(y, (-0.45 + dx, QY + 0.06), [(0.0, PZ + 0.052), (0.01, PZ + 0.054), (0.011, PZ + 0.057), (0.0, PZ + 0.056)], 'bronz', n=8)
insan(y, -0.45, QY + 0.1, PZ, 'mor', s=1.15, aci=-math.pi / 2, kol=0.5, sapka='boya_mor_acik')
insan(y, -0.37, QY + 0.05, PZ, 'kumas', s=1.1, aci=math.pi, kol=0.4)
# a Punic war galley with a purple sail off the shore
_g1 = len(y.faces)
gemi(y, (0.88, -0.86, SU), -2.25, 0.0, L=0.36, B=0.075, H=0.03, kurek=True, yelken=True, tur='savas', tohum=8)
for _i in range(_g1, len(y.faces)):
    if y.faces[_i][1] == 'boya_kirmizi' and min(p[2] for p in y.faces[_i][0]) > SU + 0.05: y.faces[_i] = (y.faces[_i][0], 'mor')

# ---------------- trees ----------------
y.bolum('Ağaçlar')
for x, yy, b in ((-0.56, 0.52, 0.2), (0.27, 0.6, 0.24), (0.3, 0.25, 0.2), (0.33, -0.12, 0.22), (1.05, 0.72, 0.18), (-0.98, 0.9, 0.2)):
    agac(y, x, yy, yuk(x, yy) if x > QX else PZ, b, 'palmiye', 'zeytin', 'ahsap')

calistir(y, 'lm_morboya')
