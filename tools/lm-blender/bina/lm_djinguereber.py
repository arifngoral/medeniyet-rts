# Djinguereber Mosque, Timbuktu (lm_djinguereber): a low, long mud mosque in the Sudano-Sahelian manner - a wide
# prayer hall with a flat roof dotted with skylight lanterns, its walls ribbed with stepped buttresses rising into
# cone pinnacles and bristling with toron beams; one great tapering minaret over the courtyard, the conical mihrab
# tower on the east wall, a walled court with arched openings into the dark hall, gates, a salt caravan outside.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from mali_ortak import *
from arap_ortak import deve

y = Yapi()
Z0 = 0.03

# the plan: hall behind (north, +y), court in front of it (south), the minaret on the hall's court front
HX0, HX1, HY0, HY1 = -1.02, 0.74, -0.04, 0.78
HH = 0.25                     # hall wall height
CY0 = -0.86                   # court front wall line
CH = 0.16                     # court wall height
MX, MY, MW0, MW1, MH = 0.3, -0.13, 0.36, 0.25, 0.78    # the minaret

y.bolum('Zemin')
zemin(y, -1.2, 1.0, -1.04, 0.95, Z0, KK, 'kum_acik', basamak=(), silmeli=True)

# ---------------- the prayer hall ----------------
y.bolum('Ibadet salonu')
L_on = HX1 - HX0
n_on = 14
acik_on = {}
for b in range(n_on):
    xc = HX0 + L_on * (b + 0.5) / n_on
    if abs(xc - MX) < MW0 * 0.62: continue
    acik_on[b] = dict(tip='nis', en=0.56, v0=0.012, v1=0.17, kemer=0.42, derin=0.05, arka='koyu')
acik_bati = {1: dict(tip='kapi', en=0.5, v0=0, v1=0.15, kemer=0.3), 4: dict(tip='kapi', en=0.5, v0=0, v1=0.15, kemer=0.3)}
for b in (0, 2, 3, 5):
    acik_bati[b] = dict(tip='pencere', en=0.28, v0=0.1, v1=0.16, kafes=True)
yan_hall = [dict(n=n_on, acik=acik_on),
            dict(n=6, acik={0: dict(tip='pencere', en=0.3, v0=0.1, v1=0.16, kafes=True), 5: dict(tip='pencere', en=0.3, v0=0.1, v1=0.16, kafes=True)}),
            dict(n=n_on, acik={b: dict(tip='pencere', en=0.3, v0=0.1, v1=0.16, kafes=True) for b in range(1, n_on, 3)}),
            dict(n=6, acik=acik_bati)]
kose_hall = dikdortgen(HX0, HX1, HY0, HY1)
DAM = Z0 + HH - 0.035
sahel_kutu(y, kose_hall, Z0, HH, K, kalin=0.035, dam=DAM, dam_key='toprak', yanlar=yan_hall, payanda_w=0.034,
           payanda_d=0.026, payanda_tepe=0.05, kose_w=0.075, kose_tepe=0.1, kose_ust=0.045, payanda_ust=0.03,
           toron_sira=(0.5, 0.82), kademe=True)

y.bolum('Dam fenerleri')
# rows of skylight lanterns across the flat roof, and copings dividing it into bays
for i in range(10):
    for j in range(4):
        fx = HX0 + 0.12 + (L_on - 0.24) * i / 9
        fy = HY0 + 0.14 + (HY1 - HY0 - 0.28) * j / 3
        if abs(fx - MX) < 0.22 and j == 0: continue
        fener(y, fx + 0.04 * (j % 2) - 0.02, fy, DAM, 0.036)
# the roof grid: low mud ridges dividing the flat roof into drainage bays (N-S ridges between pairs of lantern
# columns, E-W ridges between the lantern rows; the E-W ones a little lower and narrower so the crossings do not
# share faces), little cone pinnacles where they cross, and a wooden / terracotta spout at the low end of each bay
RX = [HX0 + 0.2045 + 0.169 * i for i in (1, 3, 5, 7)]
RY = [HY0 + 0.19, HY0 + 0.55]
KL = 0.035
for xx in RX:
    kutu_merkez(y, (xx, (HY0 + HY1) / 2), 0.018, HY1 - HY0 - 2 * KL, 0.02, KK, z0=DAM)
    kutu_merkez(y, (xx, (HY0 + HY1) / 2), 0.008, HY1 - HY0 - 2 * KL, 0.004, K, z0=DAM + 0.02)        # its rounded cap
for yy in RY:
    kutu_merkez(y, ((HX0 + HX1) / 2, yy), HX1 - HX0 - 2 * KL, 0.015, 0.016, KK, z0=DAM)
    for xx in RX:
        tepecik(y, (xx, yy), 0.011, DAM + 0.023, 0.03, K, n=7)
# the spouts: in the middle of every other bay between the pilasters (clear of them), wood and terracotta in turn
bwx = L_on / n_on
for b in range(1, n_on, 2):
    xx = HX0 + bwx * (b + 0.5)
    k_ = 'ahsap_acik' if (b // 2) % 2 else 'kiremit'
    oluk(y, V(xx, HY1), V(0, 1), Z0 + HH - 0.008, 0.06, k_)
    if abs(xx - MX) > MW0 * 0.62 + 0.03:
        oluk(y, V(xx, HY0), V(0, -1), Z0 + HH - 0.008, 0.06, k_)
bwy = (HY1 - HY0) / 6
for b in (0, 3, 5):
    oluk(y, V(HX0, HY1 - bwy * (b + 0.5)), V(-1, 0), Z0 + HH - 0.008, 0.06, 'kiremit')
for b in (0, 1, 4, 5):
    oluk(y, V(HX1, HY0 + bwy * (b + 0.5)), V(1, 0), Z0 + HH - 0.008, 0.06, 'ahsap_acik')

# ---------------- the mihrab tower on the east wall ----------------
y.bolum('Mihrap kulesi')
mc = (HX1 + 0.005, (HY0 + HY1) / 2 + 0.02)
donel(y, mc, [(0.12, Z0), (0.112, Z0 + 0.12), (0.095, Z0 + 0.24), (0.072, Z0 + 0.33), (0.045, Z0 + 0.39), (0.02, Z0 + 0.425), (0.0, Z0 + 0.435)], K, n=16)
kure(y, (mc[0], mc[1], Z0 + 0.445), 0.014, 'beyaz', n=8, kat=4)
for k in range(5):
    zz = Z0 + 0.06 + 0.065 * k
    rr = 0.12 - 0.075 * (zz - Z0) / 0.4
    for t in range(-3, 4):
        a = t * 0.38
        d = V(math.cos(a), math.sin(a))
        toron(y, V(mc[0], mc[1]) + d * (rr - 0.002) + Z * zz, d, 0.022)
# its ribs
for t in (-2, -1, 0, 1, 2):
    a = t * 0.5
    d = V(math.cos(a), math.sin(a))
    pts = [V(mc[0], mc[1]) + d * (r - 0.002) + Z * zz for r, zz in ((0.122, Z0), (0.104, Z0 + 0.2), (0.074, Z0 + 0.33))]
    boru(y, pts, 0.01, K, n=5, r_son=0.007)

# ---------------- the court ----------------
y.bolum('Avlu duvarlari')
kose_avlu = [V(HX0, CY0), V(HX1, CY0), V(HX1, HY0 + 0.05), V(HX0, HY0 + 0.05)]
n_av = 12
acik_avon = {5: dict(tip='gecit', en=0.85, v0=0, v1=0.12, kemer=0.3), 6: dict(tip='gecit', en=0.85, v0=0, v1=0.12, kemer=0.3)}
yan_avlu = [dict(n=n_av, acik=acik_avon, payanda=True),
            dict(n=6),
            dict(yok=True, kose=False),
            dict(n=6, acik={2: dict(tip='gecit', en=0.7, v0=0, v1=0.11, kemer=0.3)}, kose=False)]
sahel_kutu(y, kose_avlu, Z0, CH, K, kalin=0.032, dam=None, yanlar=yan_avlu, payanda_w=0.03, payanda_d=0.022,
           payanda_tepe=0.042, kose_w=0.065, kose_tepe=0.08, kose_ust=0.035, payanda_ust=0.022, toron_sira=(0.55,),
           ic_payanda=True)

# the main gate's portal: two great pilasters over the double opening, a lintel block with pinnacles
y.bolum('Kapi')
gx = HX0 + L_on * 6 / n_av
for s in (-1, 1):
    payanda(y, V(gx + s * L_on / n_av * 0.98, CY0), X, -Y, Z0, Z0 + CH + 0.11, 0.05, 0.04, K, 0.08, taper=0.8, arka_z=Z0 + CH)
kutu_merkez(y, (gx, CY0 - 0.012), L_on / n_av * 1.9, 0.028, 0.05, K, z0=Z0 + CH, yuzler='onarkasagsolust')
for k in range(5):
    tepecik(y, (gx - L_on / n_av * 0.72 + L_on / n_av * 0.36 * k, CY0 - 0.012), 0.011, Z0 + CH + 0.05, 0.04, K, n=6)
for k in range(7):
    toron(y, V(gx - L_on / n_av * 0.8 + L_on / n_av * 0.267 * k, CY0 - 0.026, Z0 + CH + 0.03), -Y, 0.016, 0.005)
# the threshold steps before the two passages
for s in (-1, 1):
    xc = gx + s * L_on / n_av * 0.5
    w = L_on / n_av * 0.85
    kutu_merkez(y, (xc, CY0 - 0.03), w * 1.05, 0.03, 0.008, KK, z0=Z0)
y.bolum('Minare')
# the great minaret
sahel_minare(y, (MX, MY), MW0, MW1, Z0, MH, K, kaburga=3, toron_sira=8,
             pencereler=((-Y, (0.3, 0.5, 0.68, 0.84)), (-X, (0.45, 0.72))), ust=0.07, kapi=-Y)
kisi(y, MX + 0.02, MY - 0.07, Z0 + MH - 0.008, -math.pi / 2, 'beyaz', 'beyaz', kol=0.9)   # the muezzin
sancak(y, MX - MW1 / 2 + 0.03, MY - MW1 / 2 + 0.03, Z0 + MH + 0.07, boy=0.2, en=0.11, yuk=0.07, aci=math.pi * 0.85)

# ---------------- the court's life ----------------
y.bolum('Avlu')
# a sand-filled court, worshippers in rows on mats before the hall, trees, a well
hasir(y, -0.35, -0.2, Z0, 0.7, 0.16, 0.0, 'saz', 'saz_koyu')
renk = ['beyaz', 'kumas', 'beyaz', 'boya_sari', 'beyaz', 'kobalt', 'beyaz', 'kumas']
for i in range(8):
    oturan(y, -0.64 + i * 0.085, -0.2, Z0 + 0.003, math.pi / 2, renk[i], 'beyaz')
for i in range(5):
    oturan(y, -0.56 + i * 0.1, -0.32, Z0, math.pi / 2, renk[(i + 3) % 8], 'beyaz')
agac(y, -0.85, -0.55, Z0, boy=0.22, key='zeytin')
agac(y, 0.6, -0.6, Z0, boy=0.2, key='zeytin')
agac(y, -0.15, -0.68, Z0, boy=0.18, key='boya_yesil')
# the well: a mud ring with a wooden frame
donel(y, (0.12, -0.55), [(0.045, Z0), (0.045, Z0 + 0.035), (0.038, Z0 + 0.04), (0.032, Z0 + 0.036), (0.032, Z0 + 0.02)], K, n=12)
y.yuz_yon([V(0.12 + 0.032 * math.cos(TAU * i / 12), -0.55 + 0.032 * math.sin(TAU * i / 12), Z0 + 0.02) for i in range(12)], 'su', Z)
for s in (-1, 1):
    cubuk(y, V(0.12 + s * 0.04, -0.55, Z0 + 0.035), V(0.12 + s * 0.038, -0.55, Z0 + 0.1), 0.006, 'ahsap')
cubuk(y, V(0.12 - 0.05, -0.55, Z0 + 0.098), V(0.12 + 0.05, -0.55, Z0 + 0.098), 0.006, 'ahsap_koyu')
kisi(y, 0.19, -0.53, Z0, math.pi, 'boya_kirmizi', 'boya_sari', yuk='kiremit')
kisi(y, -0.3, -0.62, Z0, 0.4, 'beyaz', 'beyaz')
kisi(y, -0.26, -0.6, Z0, 3.4, 'kumas', 'beyaz', kol=0.7)

# the yearly re-plastering (crepissage): a mud pit, masons climbing the torons of the west wall on a palm ladder,
# porters bringing baskets of mud on their heads, one on the roof smoothing it
y.bolum('Siva senligi')
cx_, cy_ = -0.7, -0.62
donel(y, (cx_, cy_), [(0.085, Z0), (0.088, Z0 + 0.012), (0.075, Z0 + 0.016), (0.07, Z0 + 0.006)], KK, n=14)
y.yuz_yon([V(cx_ + 0.07 * math.cos(TAU * i / 14), cy_ + 0.07 * math.sin(TAU * i / 14), Z0 + 0.006) for i in range(14)], 'toprak', Z)
for k in range(3):
    kure(y, (cx_ - 0.03 + 0.03 * k, cy_ + 0.01 * (k - 1), Z0 + 0.006), 0.016, 'kerpic_koyu', n=7, kat=3)
kisi(y, cx_ + 0.02, cy_, Z0 + 0.006, 0.8, 'kumas', 'beyaz', kol=0.4)
for k, (px, py, a) in enumerate(((-0.86, -0.4, 1.9), (-0.9, -0.24, 1.7), (-0.6, -0.48, 2.3))):
    kisi(y, px, py, Z0, a, ('beyaz', 'boya_sari', 'kumas')[k], 'beyaz', yuk='saz')
# the ladder against the hall's west end (a notched palm trunk) and masons on it and on the torons
lx, ly = HX0 - 0.03, 0.2
cubuk(y, V(lx - 0.035, ly, Z0), V(HX0 - 0.004, ly, Z0 + HH + 0.02), 0.012, 'kutuk', 0.01)
for k in range(5):
    t = (k + 1) / 6
    cubuk(y, V(lx - 0.035 + (lx + 0.031 - lx + 0.035) * t, ly - 0.012, Z0 + (HH + 0.02) * t), V(lx - 0.035 + (0.066) * t, ly + 0.012, Z0 + (HH + 0.02) * t), 0.004, 'ahsap_koyu')
kisi(y, lx - 0.05, ly - 0.03, Z0, 0.0, 'kumas', 'beyaz', kol=1.0)        # handing up a basket at the foot
t_ = 3 / 6                                                                   # a mason standing on the third rung
kisi(y, lx - 0.035 + 0.066 * t_ - 0.012, ly, Z0 + (HH + 0.02) * t_ + 0.003, 0.0, 'boya_kirmizi', 'beyaz', kol=0.8)
# a mason working off a plank laid over the upper row of torons (the torons are the scaffold)
pz = Z0 + HH * 0.82 + 0.0028
kutu_merkez(y, (HX0 - 0.014, 0.44), 0.024, 0.1, 0.004, 'ahsap', z0=pz)
kisi(y, HX0 - 0.0135, 0.43, pz + 0.004, 0.0, 'beyaz', 'beyaz', kol=1.0)
sepet(y, HX0 - 0.014, 0.475, pz + 0.004, 0.009, 0.008, dolu='kerpic_koyu')
kisi(y, HX0 + 0.12, 0.3, DAM, 0.3, 'kumas', 'beyaz', kol=0.6)
sepet(y, HX0 + 0.16, 0.25, DAM, 0.014, 0.012, dolu='kerpic_koyu')

# market mats outside the gate: Timbuktu's traders of salt, cloth, books and kola
y.bolum('Kapi onu pazari')
for k, (px, py, mal) in enumerate(((0.62, -0.99, ('kumas', 'kola')), (0.9, -0.38, ('kabak', 'tahil')))):
    hasir(y, px, py, Z0, 0.16, 0.07, 0.0)
    for j, m in enumerate(mal):
        mal_koy(y, m, px - 0.04 + 0.08 * j, py, Z0 + 0.003)
    oturan(y, px, py + 0.06, Z0, -math.pi / 2, ('lacivert', 'boya_yesil')[k], 'beyaz')

# ---------------- outside: the salt caravan and townsfolk ----------------
y.bolum('Kervan')
for k, (dx, dy, a, cok) in enumerate(((-0.62, -0.98, 0.1, False), (-0.42, -0.95, 0.0, True), (0.4, -0.97, math.pi, False))):
    deve(y, dx, dy, Z0, a, renk='ahsap_acik' if k != 1 else 'kum_koyu', yuk=not cok, cok=cok, olcek=1.0)
    if not cok:
        continue
# salt slabs unloaded by the gate
for k in range(3):
    mal_koy(y, 'tuz', -0.15 + 0.08 * k, -0.97, Z0)
kisi(y, -0.26, -0.98, Z0, 0.0, 'kobalt', 'beyaz', mizrak='ahsap')
kisi(y, 0.08, -0.95, Z0, 2.6, 'beyaz', 'beyaz')
kisi(y, 0.25, -1.0, Z0, 1.9, 'boya_sari', 'boya_kirmizi', yuk='saz')
kisi(y, -1.1, -0.3, Z0, -0.3, 'kumas', 'beyaz')
kisi(y, -1.12, 0.4, Z0, 0.6, 'beyaz', 'beyaz', kol=0.5)
akasya(y, -1.08, -0.85, Z0, boy=0.26, tohum=3)
akasya(y, 0.88, -0.75, Z0, boy=0.22, tohum=5)
akasya(y, 0.86, 0.78, Z0, boy=0.24, tohum=7)

calistir(y, 'lm_djinguereber')
