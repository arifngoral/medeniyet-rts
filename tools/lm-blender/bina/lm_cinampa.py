# Çinampa Bahçeleri (lm_cinampa): the floating gardens of Lake Xochimilco / Tenochtitlan: long raised plots of black lake mud
# held by wattle and stakes, rows of maize, beans, squash, amaranth, chillies and marigolds, ahuejote willows along their
# edges, canals with laden canoes between them; in the middle a stone-faced island with a small stepped pyramid and a
# Tlaloc shrine under a tall thatch, a landing pier, farmers' thatched huts and a wooden lookout tower.
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from aztek_parca import *
from bina_ortak import calistir

y = Yapi()
rn = random.Random(11)
ZW = 0.03                         # water level (the lake)
ZC = ZW + 0.035                   # top of a chinampa
ZI = ZW + 0.045                   # top of the temple island

y.bolum('Göl')
zemin(y, -1.15, 1.15, -1.12, 1.12, ZW, 'kaya_koyu', 'su', basamak=(), silmeli=False)


# ---------------- a chinampa ----------------
def tarla(x0, x1, y0, y1, tur, sogutler=(), kazik=True, bos=None):
    """one raised plot: mud walls, a wattle band at the waterline, stakes, crop rows of the given kind"""
    k = dikdortgen(x0, x1, y0, y1)
    duvarlar(y, k, ZW - 0.004, ZC, 'toprak', ust='toprak')
    silme(y, k, ZW - 0.002, 0.016, 0.004, 'saz_koyu')
    if kazik:
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
            m = max(1, int(L / 0.11))
            for j in range(m):
                p = a.lerp(b, j / m) + nn * 0.006
                cubuk(y, V(p.x, p.y, ZW - 0.004), V(p.x, p.y, ZC + 0.01), 0.008, 'ahsap')
    L = x1 - x0
    nr = 3 if (y1 - y0) < 0.22 else 4
    sir = [y0 + (y1 - y0) * (j + 0.5) / nr for j in range(nr)]
    bosta = lambda x: bos is not None and bos[0] - 0.01 < x < bos[1] + 0.01
    for yy in sir:   # the ridges the crops stand on (broken where a hut stands)
        parcalar_ = [(x0 + 0.02, x1 - 0.02)] if bos is None else [(x0 + 0.02, bos[0]), (bos[1], x1 - 0.02)]
        for a_, b_ in parcalar_:
            if b_ - a_ > 0.03: kutu_merkez(y, ((a_ + b_) / 2, yy), b_ - a_, 0.026, 0.007, 'kerpic_koyu', z0=ZC)
    z = ZC + 0.007
    for j, yy in enumerate(sir):
        if tur == 'misir':
            m = int((L - 0.06) / 0.065)
            for i in range(m + 1):
                x = x0 + 0.03 + (L - 0.06) * i / m + rn.uniform(-0.005, 0.005)
                if bosta(x): continue
                misir(y, x, yy + rn.uniform(-0.004, 0.004), z, 0.075 + rn.uniform(-0.01, 0.012), yon=rn.uniform(0, TAU))
        elif tur == 'fasulye':     # beans climbing on cane tripods
            m = int((L - 0.06) / 0.08)
            for i in range(m + 1):
                x = x0 + 0.03 + (L - 0.06) * i / m
                if bosta(x): continue
                for a in (0, 2.1, 4.2):
                    cubuk(y, V(x + 0.012 * math.cos(a), yy + 0.012 * math.sin(a), z), V(x, yy, z + 0.055), 0.003, 'ahsap_acik')
                for (dx, dy, dz, r_, kk) in ((0.008, 0.004, 0.012, 0.011, 'boya_yesil'), (-0.007, -0.004, 0.026, 0.01, 'zeytin'), (0.003, -0.006, 0.042, 0.008, 'boya_yesil')):
                    elipsoid(y, (x + dx, yy + dy, z + dz), (r_, r_ * 0.9, r_ * 0.8), kk, n=6, kat=4, aci=i)
                kure(y, (x - 0.008, yy + 0.006, z + 0.034), 0.004, 'beyaz', n=4, kat=2)
        elif tur == 'kabak':       # squash: big leaves and the gourds
            m = int((L - 0.06) / 0.07)
            for i in range(m + 1):
                x = x0 + 0.03 + (L - 0.06) * i / m
                if bosta(x): continue
                elipsoid(y, (x, yy, z), (0.024, 0.02, 0.012), 'yesil_koyu' if i % 2 else 'boya_yesil', n=7, kat=4, aci=rn.uniform(0, 3), ust_yarim=True)
                if i % 2 == 0:
                    elipsoid(y, (x + 0.012, yy + 0.008, z + 0.006), (0.014, 0.011, 0.01), 'boya_sari' if j % 2 else 'siva_oker', n=7, kat=4)
        elif tur == 'amarant':     # amaranth (huauhtli): tall red plumes
            m = int((L - 0.06) / 0.05)
            for i in range(m + 1):
                x = x0 + 0.03 + (L - 0.06) * i / m
                if bosta(x): continue
                h = 0.05 + rn.uniform(0, 0.02)
                cubuk(y, V(x, yy, z), V(x, yy, z + h * 0.6), 0.004, 'boya_yesil')
                donel(y, (x, yy), [(0.0, z + h * 0.45), (0.011, z + h * 0.6), (0.008, z + h * 0.85), (0.0, z + h)], 'boya_kirmizi' if (i + j) % 3 else 'siva_kirmizi', n=5)
        elif tur == 'cicek':       # marigolds (cempasuchil) and dahlias on green mounds
            m = int((L - 0.06) / 0.04)
            for i in range(m + 1):
                x = x0 + 0.03 + (L - 0.06) * i / m
                if bosta(x): continue
                elipsoid(y, (x, yy, z), (0.016, 0.014, 0.012), 'boya_yesil', n=6, kat=4, ust_yarim=True)
                kure(y, (x, yy, z + 0.014), 0.009, ('altin', 'boya_sari', 'boya_kirmizi')[(i + 2 * j) % 3] if j != 1 else 'siva_kirmizi', n=6, kat=3)
        else:                      # chillies and tomatoes: low bushes dotted red
            m = int((L - 0.06) / 0.045)
            for i in range(m + 1):
                x = x0 + 0.03 + (L - 0.06) * i / m
                if bosta(x): continue
                elipsoid(y, (x, yy, z), (0.015, 0.015, 0.018), 'yesil_koyu', n=6, kat=4, ust_yarim=True)
                for a in (0.5, 2.6, 4.5):
                    kure(y, (x + 0.01 * math.cos(a), yy + 0.01 * math.sin(a), z + 0.01), 0.004, 'boya_kirmizi', n=4, kat=2)
    for (sx, sy) in sogutler:
        sogut(y, sx, sy, ZC, 0.3 + rn.uniform(-0.04, 0.06), tohum=int(sx * 100 + sy * 1000))


y.bolum('Çinampalar ve ekinler')
COL = [(-1.08, -0.4), (-0.32, 0.32), (0.4, 1.08)]
ROW = [(-1.06 + 0.275 * k, -1.06 + 0.275 * k + 0.2) for k in range(8)]
TURLER = ['misir', 'fasulye', 'cicek', 'misir', 'kabak', 'amarant', 'misir', 'biber', 'misir', 'kabak', 'cicek', 'misir', 'fasulye', 'amarant',
          'misir', 'biber', 'kabak', 'misir', 'cicek', 'fasulye']
ti = 0
for ci, (x0, x1) in enumerate(COL):
    for ri, (y0, y1) in enumerate(ROW):
        if ci == 1 and 2 <= ri <= 5: continue           # the temple island and the landing
        tur = TURLER[ti % len(TURLER)]; ti += 1
        # willows: along the outer edge of the side columns, a pair on the centre plots
        so = []
        if ci != 1:
            xe = x0 + 0.02 if ci == 0 else x1 - 0.02
            so = [(xe, (y0 + y1) / 2)] if ri % 2 == 0 else []
            if ri in (1, 5): so.append((x1 - 0.02 if ci == 0 else x0 + 0.02, y0 + 0.02))
        elif ri in (0, 7):
            so = [(x0 + 0.02, (y0 + y1) / 2), (x1 - 0.02, (y0 + y1) / 2)]
        # (plots with a hut or the lookout tower: no crops under them)
        bos = {(0, 3): (-0.97, -0.75), (2, 6): (0.75, 0.97), (2, 2): (0.53, 0.71), (2, 1): (0.4, 0.56)}.get((ci, ri))
        if (ci, ri) == (2, 1): so = [s for s in so if s[0] > 0.6]
        tarla(x0, x1, y0, y1, tur, so, bos=bos)


# ---------------- farmers' huts ----------------
def kulube(cx, cy, aci=0.0, w=0.15, d=0.1, ZC=ZC):
    """a farmer's hut: wattle-and-daub walls with a door, a steep thatched gable roof"""
    with parca(y, (cx, cy, 0), aci):
        x0, x1, y0, y1 = -w / 2, w / 2, -d / 2, d / 2
        h = 0.065
        kutu_merkez(y, (0, 0), w + 0.03, d + 0.03, 0.014, 'toprak', z0=ZC)
        z0 = ZC + 0.014
        dikdortgen_acik(y, V(x0, y0), V(x1, y0), z0, h, 0.4, 0.62, 0.0, 0.05, ('siva_krem', 'kerpic_koyu', 'kerpic', 'koyu'), derin=0.012)
        for a, b in ((V(x1, y0), V(x1, y1)), (V(x1, y1), V(x0, y1)), (V(x0, y1), V(x0, y0))):
            duz_duvar(y, a, b, z0, z0 + h, 'siva_krem')
        silme(y, dikdortgen(x0, x1, y0, y1), z0, 0.014, 0.003, 'kerpic')
        saz_cati(y, x0, x1, y0, y1, z0 + h, 0.085, sacak=0.022, nr=5, kalin=0.012, besik=True)
        # a granary jar and a grinding stone by the door
        donel(y, (x1 + 0.02, y0 - 0.02), [(0.0, z0 - 0.0), (0.012, z0), (0.018, z0 + 0.02), (0.012, z0 + 0.035), (0.014, z0 + 0.04), (0.0, z0 + 0.038)], 'kiremit', n=8)
        kutu_merkez(y, (x0 + 0.01, y0 - 0.025), 0.03, 0.018, 0.008, 'bazalt', z0=z0 - 0.014)


y.bolum('Çiftçi kulübeleri')
kulube(-0.86, ROW[3][0] + 0.1, 0.0)
kulube(0.86, ROW[6][0] + 0.1, math.pi)
kulube(0.62, ROW[2][0] + 0.1, 0.0, 0.13, 0.09)

# ---------------- temple island ----------------
y.bolum('Tapınak adası')
IX0, IX1, IY0, IY1 = -0.32, 0.32, -0.29, ROW[5][1] - 0.05
ik = dikdortgen(IX0, IX1, IY0, IY1)
duvarlar(y, ik, ZW - 0.004, ZI, 'kirec', ust='zemin')
silme(y, ik, ZI - 0.008, 0.008, 0.006, 'kirec')
PC = V(0.0, 0.2)
PH = 0.36
basamakli_piramit(y, (PC.x, PC.y), 0.48, 0.21, 3, PH, 'kirec', talud=0.55, tablero_key='boya_kirmizi', merdiven=False, z0=ZI, d0=0.46, d1=0.19)
YS = PC.y - 0.095
YB = YS - 0.33
alfarda_merdiven(y, PC.x, YB, YS, ZI, ZI + PH, 0.13, n=14, key='kirec', alfarda_key='siva', alfarda_en=0.03, dado=0.15, dado_h=0.045)
ZT = ZI + PH
y.bolum('Tlaloc türbesi')
sx0, sx1, sy0, sy1 = -0.085, 0.085, PC.y - 0.075, PC.y + 0.08
SH = 0.1
dikdortgen_acik(y, V(sx0, sy0), V(sx1, sy0), ZT, SH, 0.32, 0.68, 0.0, 0.075, ('siva', 'koyu', 'kirec', 'koyu'), derin=0.02, cerceve=(0.008, 'turkuaz'))
for a, b in ((V(sx1, sy0), V(sx1, sy1)), (V(sx1, sy1), V(sx0, sy1)), (V(sx0, sy1), V(sx0, sy0))):
    duz_duvar(y, a, b, ZT, ZT + SH, 'siva')
# Tlaloc's colours: turquoise and white bands, the rain god's goggle eyes over the door
sk = dikdortgen(sx0, sx1, sy0, sy1)
silme(y, sk, ZT, 0.02, 0.003, 'turkuaz')
silme(y, sk, ZT + SH - 0.03, 0.022, 0.003, 'turkuaz')
for i in range(4):
    a, b = sk[i], sk[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x); L = (b - a).length
    m = int(L / 0.03)
    for k in range(m):
        y.oculus(a.lerp(b, (k + 0.5) / m) + nn * 0.003 + Z * (ZT + SH - 0.019), e, nn, 0.006, 'beyaz', 'turkuaz', f=0.002, k=8)
for s in (-1, 1):
    y.oculus(V(s * 0.04, sy0 - 0.0005, ZT + 0.06), X, -Y, 0.011, 'beyaz', 'turkuaz', f=0.005, k=10)
    y.oculus(V(s * 0.04, sy0 - 0.0025, ZT + 0.06), X, -Y, 0.004, 'koyu', 'koyu', f=0.001, k=6)
# the rain god's tall roof: a truncated pyramid in turquoise and white stripes, a crown of merlons
kutu(y, V(sx0 - 0.018, sy0 - 0.018, ZT + SH), X, sx1 - sx0 + 0.036, sy1 - sy0 + 0.036, 0.018, 'siva', 'onarkasagsol')
silme(y, dikdortgen(sx0 - 0.018, sx1 + 0.018, sy0 - 0.018, sy1 + 0.018), ZT + SH + 0.003, 0.012, 0.003, 'turkuaz')
zr = ZT + SH + 0.018
w0, d0 = sx1 - sx0 + 0.036, sy1 - sy0 + 0.036
zk = zr + 0.22
SC_ = ((sx0 + sx1) / 2, (sy0 + sy1) / 2)
kesik_piramit(y, SC_, w0, d0, w0 * 0.6, d0 * 0.52, zr, zk, ['turkuaz', 'beyaz'], n_dilim=9)
kornis(y, SC_[0] - w0 * 0.3, SC_[0] + w0 * 0.3, SC_[1] - d0 * 0.26, SC_[1] + d0 * 0.26, zk - 0.01, 0.01, 0.005, 'turkuaz')
almena_halka(y, dikdortgen(SC_[0] - w0 * 0.3, SC_[0] + w0 * 0.3, SC_[1] - d0 * 0.26, SC_[1] + d0 * 0.26), zk, 0.045, 0.009, 'siva', bosluk=0.016)
for s in (-1, 1):
    mangal(y, s * 0.085, PC.y - 0.088, ZT, 0.04)

y.bolum('Ada: rahip evi, sunak, iskele')
kulube(-0.235, -0.18, 0.0, 0.11, 0.09, ZC=ZI)
# a round altar with maize offerings
y.prizma((0.22, -0.17), 0.05, ZI, ZI + 0.03, 'siva', n=16)
halka_kornis(y, (0.22, -0.17), 0.05, ZI + 0.02, 0.01, 0.004, 16, 'turkuaz')
for k in range(5):
    t = TAU * k / 5
    elipsoid(y, (0.22 + 0.025 * math.cos(t), -0.17 + 0.025 * math.sin(t), ZI + 0.03), (0.009, 0.006, 0.006), 'boya_sari', n=6, kat=4, aci=t)
mangal(y, 0.22, -0.17, ZI + 0.03, 0.05, ates=True)
for (x, yy) in ((-0.285, 0.42), (0.285, 0.42), (-0.285, 0.0), (0.285, 0.0)):
    sogut(y, x, yy, ZI, 0.32, tohum=int(x * 50 + yy * 70))
# the landing pier
for k in range(9):
    yy = IY0 - 0.012 - k * 0.022
    kutu_merkez(y, (0.0, yy), 0.11, 0.018, 0.006, 'ahsap_acik' if k % 2 else 'ahsap', z0=ZI - 0.008)
for sx in (-1, 1):
    for yy in (IY0 - 0.03, IY0 - 0.12, IY0 - 0.19):
        cubuk(y, V(sx * 0.05, yy, ZW - 0.004), V(sx * 0.05, yy, ZI + 0.012), 0.01, 'ahsap_koyu')

# ---------------- lookout tower ----------------
y.bolum('Gözcü kulesi')
TX, TY = COL[2][0] + 0.07, ROW[1][1] - 0.06
TH = 0.4
for (dx, dy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
    cubuk(y, V(TX + dx * 0.045, TY + dy * 0.045, ZC), V(TX + dx * 0.035, TY + dy * 0.035, ZC + TH + 0.12), 0.01, 'ahsap_koyu')
for i in range(4):   # cross braces
    p0 = [(-1, -1), (1, -1), (1, 1), (-1, 1)][i]; p1 = [(-1, -1), (1, -1), (1, 1), (-1, 1)][(i + 1) % 4]
    for z_a, z_b in ((0.05, 0.2), (0.2, 0.05), (0.22, 0.36), (0.36, 0.22)):
        cubuk(y, V(TX + p0[0] * 0.043, TY + p0[1] * 0.043, ZC + z_a), V(TX + p1[0] * 0.043, TY + p1[1] * 0.043, ZC + z_b), 0.005, 'ahsap')
kutu_merkez(y, (TX, TY), 0.12, 0.12, 0.012, 'ahsap', z0=ZC + TH)
for i in range(4):   # railing
    p0 = [(-1, -1), (1, -1), (1, 1), (-1, 1)][i]; p1 = [(-1, -1), (1, -1), (1, 1), (-1, 1)][(i + 1) % 4]
    cubuk(y, V(TX + p0[0] * 0.058, TY + p0[1] * 0.058, ZC + TH + 0.045), V(TX + p1[0] * 0.058, TY + p1[1] * 0.058, ZC + TH + 0.045), 0.006, 'ahsap_acik')
    for t in (0.33, 0.67):
        p = V(TX + (p0[0] + (p1[0] - p0[0]) * t) * 0.058, TY + (p0[1] + (p1[1] - p0[1]) * t) * 0.058)
        cubuk(y, V(p.x, p.y, ZC + TH + 0.012), V(p.x, p.y, ZC + TH + 0.045), 0.005, 'ahsap_acik')
# ladder
for sx in (-1, 1):
    cubuk(y, V(TX + sx * 0.018, TY - 0.11, ZC), V(TX + sx * 0.018, TY - 0.06, ZC + TH + 0.012), 0.006, 'ahsap_acik')
for k in range(8):
    t = (k + 0.5) / 8
    p = V(TX, TY - 0.11 + 0.05 * t, ZC + (TH + 0.012) * t)
    cubuk(y, p - V(0.018, 0, 0), p + V(0.018, 0, 0), 0.004, 'ahsap_acik')
saz_cati(y, TX - 0.05, TX + 0.05, TY - 0.05, TY + 0.05, ZC + TH + 0.12, 0.1, sacak=0.03, nr=5, kalin=0.012)
sancak(y, TX + 0.0, TY, ZC + TH + 0.21, boy=0.13, en=0.09, yuk=0.055, aci=-math.pi / 2 - 0.5, direk_key='ahsap_koyu', kuyruk=True)

# ---------------- canoes and reeds ----------------
y.bolum('Kanolar')
for (x, yy, a, yuk) in ((0.03, IY0 - 0.08, math.pi / 2 + 0.1, ['boya_sari', 'altin', 'boya_yesil']), (-0.13, IY0 - 0.12, math.pi / 2 - 0.15, ['boya_kirmizi', 'kerpic']),
                        (-0.36, -0.2, math.pi / 2, ['boya_yesil', 'boya_sari']), (0.36, 0.25, math.pi / 2 + 0.05, ['siva_oker', 'kiremit', 'boya_sari']),
                        (-0.6, ROW[4][0] - 0.037, 0.05, ['boya_sari', 'boya_sari']), (0.75, ROW[1][0] - 0.037, math.pi - 0.04, ['kerpic', 'boya_yesil', 'boya_kirmizi']),
                        (0.0, ROW[7][0] - 0.037, 0.0, None), (-0.75, ROW[6][0] - 0.037, math.pi, ['boya_kirmizi'])):
    kano(y, x, yy, ZW + 0.012, 0.2, 0.046, 0.02, a, yuk=yuk)
y.bolum('Sazlar')
for (x, yy) in ((-1.12, -0.5), (-1.12, 0.3), (1.12, -0.2), (1.12, 0.55), (-0.5, -1.1), (0.55, -1.1), (-0.36, 1.1), (0.36, 1.08), (-1.11, -1.08), (1.11, 1.08)):
    for k in range(9):
        t = rn.uniform(0, TAU); r = rn.uniform(0, 0.03)
        p = V(x + r * math.cos(t), yy + r * math.sin(t))
        h = rn.uniform(0.05, 0.09)
        cubuk(y, V(p.x, p.y, ZW), V(p.x + rn.uniform(-0.01, 0.01), p.y + rn.uniform(-0.01, 0.01), ZW + h), 0.004, 'zeytin' if k % 3 else 'saz')
        if k % 3 == 0:
            elipsoid(y, (p.x, p.y, ZW + h * 0.85), (0.004, 0.004, 0.012), 'ahsap', n=4, kat=3)

y.bolum('Sancaklar')
for sx in (-1, 1):
    sancak(y, sx * 0.12, IY0 + 0.025, ZI, boy=0.3, en=0.1, yuk=0.065, aci=-math.pi / 2 + sx * 0.6, direk_key='ahsap_koyu')

calistir(y, 'lm_cinampa')
