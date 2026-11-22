# Thing Meydanı (lm_thing): the Norse assembly field: a stepped law hill (Tynwald / Lögberg) of grassed stone-kerbed
# tiers with a stair cut up its front and on the top the lawspeaker's open pavilion (carved posts, shingled pyramid
# roof with dragon heads, the high seat inside) under the banner; round it the búðir - turf-walled booths roofed with
# striped awnings - a great painted rune stone, a judgment ring of standing stones, banner poles, barrels and a fire,
# and behind the hill the turf-roofed assembly hall.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from viking_parca import *
from bina_ortak import calistir

y = Yapi()
Z0 = 0.035
MC = V(0.0, -0.06)               # the law hill's centre
KAT = [(0.56, 0.085), (0.46, 0.085), (0.37, 0.085), (0.29, 0.085), (0.22, 0.08)]   # (radius, height) of the tiers
SH = ['sindira', 'sindira2']

y.bolum('Zemin: meclis alanı')
zemin(y, -1.1, 1.1, -1.02, 1.0, Z0, 'granit', 'cimen', basamak=(), silmeli=False)
yer = lambda pts, k='toprak': y.yuz_yon([V(p[0], p[1], Z0 + 0.002) for p in pts], k, Z)
yer([(-0.08, -1.0), (0.08, -1.0), (0.08, MC.y - 0.5), (-0.08, MC.y - 0.5)])
# a trodden ring round the hill
n = 40
for i in range(n):
    t0, t1 = TAU * i / n, TAU * (i + 1) / n
    q = [V(MC.x + r * math.cos(t), MC.y + r * math.sin(t), Z0 + 0.0015) for r, t in ((0.5, t0), (0.5, t1), (0.66, t1), (0.66, t0))]
    y.yuz_yon(q, 'toprak_ot', Z)

# ---------------- the law hill ----------------
y.bolum('Kanun tepesi')
z = Z0
BANK = 0.04                      # how far the turf bank above each tier's stone kerb leans back
UST = []                          # (inner radius, outer radius, z) of each grassed tier top
for k, (r, h) in enumerate(KAT):
    r2 = KAT[k + 1][0] if k + 1 < len(KAT) else 0.0
    if r2 > 0:
        # a low dry-stone kerb with coping stones, the turf bank leaning back above it
        zs = z + h * 0.4
        donel(y, MC, [(r, z), (r - 0.004, zs)], 'granit' if k % 2 == 0 else 'granit_koyu', n=40)
        halka_kornis(y, MC, r - 0.004, zs - 0.006, 0.009, 0.006, 40, 'granit', profil='duz')
        donel(y, MC, [(r - 0.004, zs + 0.003), (r - 0.02, z + h * 0.78), (r - BANK + 0.004, z + h - 0.003), (r - BANK, z + h)], 'cimen', n=40)
        ro = r - BANK
    else:
        donel(y, MC, [(r, z), (r - 0.012, z + h * 0.8), (r - 0.014, z + h)], 'granit' if k % 2 == 0 else 'granit_koyu', n=40)
        halka_kornis(y, MC, r - 0.014, z + h - 0.008, 0.008, 0.006, 40, 'granit', profil='duz')
        ro = r - 0.014
    zt = z + h
    for i in range(40):
        t0, t1 = TAU * i / 40, TAU * (i + 1) / 40
        if r2 > 0:
            q = [V(MC.x + rr * math.cos(t), MC.y + rr * math.sin(t), zt) for rr, t in ((r2 - 0.005, t0), (ro, t0), (ro, t1), (r2 - 0.005, t1))]
        else:
            q = [V(MC.x, MC.y, zt), V(MC.x + ro * math.cos(t0), MC.y + ro * math.sin(t0), zt), V(MC.x + ro * math.cos(t1), MC.y + ro * math.sin(t1), zt)]
        y.yuz_yon(q, 'cimen' if r2 > 0 else 'zemin', Z)
    if r2 > 0: UST.append((r2, ro, zt))
    z = zt
ZT = z
# plank benches round the grassed tiers (the assembly sat on the hill), clear of the stair and the banner poles
ACIK = [-90.0] + [-90 + s * math.degrees(t * 2.2) for t in (0.25, 0.55) for s in (-1, 1)]
for k, (ri, ro, zt) in enumerate(UST[:3]):
    rm = (ri + ro) / 2 + 0.006
    m = int(TAU * rm / 0.12)
    for i in range(m):
        ad = 360.0 * (i + 0.5) / m - 90
        if any(abs((ad - a + 180) % 360 - 180) < (17 if a == -90 else 7) for a in ACIK): continue
        a = math.radians(ad)
        with parca(y, (MC.x + rm * math.cos(a), MC.y + rm * math.sin(a), 0), a + math.pi / 2):
            kutu_merkez(y, (0, 0), 0.07, 0.018, 0.005, 'ahsap_acik' if i % 2 else 'ahsap', z0=zt + 0.014)
            for sx in (-1, 1):
                kutu_merkez(y, (sx * 0.026, 0), 0.007, 0.014, 0.014, 'ahsap_koyu', z0=zt)
# the stair up the front, with stone cheeks
merdiven(y, (MC.x, MC.y - KAT[0][0] - 0.06), math.pi / 2, 0.14, Z0, ZT, n=14, d=(KAT[0][0] - KAT[-1][0] + 0.06) / 14, key='granit',
         yanlik='granit_koyu')
# banner poles on the first tier
for t in (-0.55, -0.25, 0.25, 0.55):
    a = -math.pi / 2 + t * 2.2
    r = KAT[0][0] - 0.05
    px, py = MC.x + r * math.cos(a), MC.y + r * math.sin(a)
    sancak(y, px, py, Z0 + KAT[0][1], boy=0.26, en=0.08, yuk=0.055, aci=a + 1.2, direk_key='ahsap_koyu', kuyruk=True)

# ---------------- the lawspeaker's pavilion ----------------
y.bolum('Kanun sözcüsünün köşkü')
PW = 0.125
PH = 0.2
with parca(y, (MC.x, MC.y, 0)):
    kutu_merkez(y, (0, 0), 0.31, 0.31, 0.02, 'granit_koyu', z0=ZT)
    zb = ZT + 0.02
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = V(sx * PW, sy * PW)
            kutu_merkez(y, (p.x, p.y), 0.03, 0.03, 0.02, 'granit', z0=zb)
            y.prizma((p.x, p.y), 0.011, zb + 0.02, zb + PH, 'ahsap', n=8)
            for zz in (0.06, 0.11):
                y.prizma((p.x, p.y), 0.0125, zb + zz, zb + zz + 0.012, 'boya_kirmizi', n=8)
            # carved brackets
            for d in (V(-sx, 0), V(0, -sy)):
                cubuk(y, p + Z * (zb + PH - 0.05), p + d * 0.045 + Z * (zb + PH - 0.005), 0.008, 'ahsap_koyu')
    for i, (a, b) in enumerate(((V(-PW, -PW), V(PW, -PW)), (V(PW, -PW), V(PW, PW)), (V(PW, PW), V(-PW, PW)), (V(-PW, PW), V(-PW, -PW)))):
        cubuk(y, a + Z * (zb + PH), b + Z * (zb + PH), 0.022, 'ahsap_koyu', 0.018)
        e = (b - a).normalized(); nn = V(e.y, -e.x)
        kutu(y, a + e * 0.02 + nn * 0.0115 + Z * (zb + PH - 0.006), e, 2 * PW - 0.04, 0.002, 0.012, 'boya_sari', 'on')
    zr = cati_kirma(y, -PW, PW, -PW, PW, zb + PH + 0.011, 0.34, 0.055, 'sindira', 'ahsap', kalinlik=0.012, nr=10, ns=6, dilim=SH, mahya_en=0.012)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ejder(y, V(sx * (PW + 0.055), sy * (PW + 0.055), zb + PH + 0.006), V(sx, sy), 0.1, 'ahsap_koyu')
    kure(y, (0, 0, zr + 0.012), 0.014, 'altin', n=8, kat=4)
    # the high seat: a carved chair with tall posts (öndvegissúlur)
    kutu_merkez(y, (0, 0.03), 0.08, 0.06, 0.035, 'ahsap', z0=zb)
    kutu_merkez(y, (0, 0.058), 0.08, 0.012, 0.09, 'ahsap', z0=zb)
    for sx in (-1, 1):
        y.prizma((sx * 0.045, 0.06), 0.007, zb, zb + 0.13, 'ahsap_koyu', n=6)
        kure(y, (sx * 0.045, 0.06, zb + 0.135), 0.01, 'altin', n=6, kat=3)
    kutu_merkez(y, (0, 0.03), 0.07, 0.05, 0.004, 'boya_kirmizi', z0=zb + 0.035)
    sancak(y, 0.0, -0.06, zb, boy=0.5, en=0.14, yuk=0.09, aci=-math.pi / 2 - 0.7, direk_key='ahsap_koyu')

# ---------------- the vébond and the stair posts ----------------
y.bolum('Vébond: kutsal ip çiti')
# hazel posts and ropes round the court (the vébond), open at the stair, kept clear of the hall, the rune stone, the fire
RV, NV = 0.69, 44
FC = V(-0.42, -0.74)
dik = []
for i in range(NV):
    a = -math.pi / 2 + TAU * i / NV
    p = V(MC.x + RV * math.cos(a), MC.y + RV * math.sin(a))
    ok = (abs(i) > 1 and abs(i - NV) > 1 and p.y < 0.36 and (p - V(0.2, -0.78)).length > 0.17 and (p - FC).length > 0.22)
    dik.append(p if ok else None)
    if ok:
        y.prizma((p.x, p.y), 0.0055, Z0, Z0 + 0.085, 'ahsap', n=5)
        kure(y, (p.x, p.y, Z0 + 0.087), 0.0065, 'ahsap_koyu', n=5, kat=3)
for i in range(NV):
    a, b = dik[i], dik[(i + 1) % NV]
    if a is None or b is None: continue
    for zz in (0.075, 0.045):
        m = (a + b) / 2
        boru(y, [V(a.x, a.y, Z0 + zz), V(m.x, m.y, Z0 + zz - 0.008), V(b.x, b.y, Z0 + zz)], 0.0018, 'kece', n=4, kapat=False)
# carved posts with dragon heads and painted bands flanking the stair foot
for sx in (-1, 1):
    px, py = MC.x + sx * 0.1, MC.y - KAT[0][0] - 0.1
    kutu_merkez(y, (px, py), 0.034, 0.034, 0.02, 'granit', z0=Z0)
    y.prizma((px, py), 0.012, Z0 + 0.02, Z0 + 0.19, 'ahsap_koyu', n=8)
    for zz in (0.07, 0.14):
        y.prizma((px, py), 0.0135, Z0 + zz, Z0 + zz + 0.014, 'boya_kirmizi' if zz < 0.1 else 'boya_sari', n=8)
    ejder(y, V(px, py, Z0 + 0.185), V(0, -1), 0.075)

# ---------------- the great rune stone and the judgment ring ----------------
y.bolum('Büyük runik taş')
runik_tas(y, (0.2, -0.78, Z0), -0.55, en=0.24, boy=0.5, kalin=0.07, key='kaya')
kutu_merkez(y, (0.2, -0.78), 0.3, 0.13, 0.012, 'granit_koyu', z0=Z0, aci=-0.55)

y.bolum('Yargı çemberi')
JC = V(0.6, -0.72)
for i in range(9):
    t = TAU * i / 9 + 0.2
    dikili_tas(y, JC.x + 0.15 * math.cos(t), JC.y + 0.15 * math.sin(t), Z0, 0.07 + 0.02 * (i % 3), 0.022, 'kaya', tohum=10 + i, egik=0.06)
dikili_tas(y, JC.x, JC.y, Z0, 0.05, 0.03, 'kaya_koyu', tohum=99)
yer([(JC.x + 0.19 * math.cos(TAU * i / 12), JC.y + 0.19 * math.sin(TAU * i / 12)) for i in range(12)], 'toprak_ot')


# ---------------- booths ----------------
def budir(c, aci, w=0.26, d=0.16, renk='kumas', serit='boya_kirmizi'):
    """a booth: low turf walls on a stone footing, open at the end facing the hill (local -x), roofed with a striped
    awning on a ridge pole; a bench and a barrel by the door"""
    with parca(y, (c[0], c[1], 0), aci):
        t, hw = 0.026, 0.05
        # turf walls (stone sides, grass tops)
        for (x0, x1, y0, y1) in ((-w / 2, w / 2, d / 2 - t, d / 2), (-w / 2, w / 2, -d / 2, -d / 2 + t), (w / 2 - t, w / 2, -d / 2 + t, d / 2 - t),
                                 (-w / 2, -w / 2 + t, -d / 2 + t, -d / 2 + t + 0.035), (-w / 2, -w / 2 + t, d / 2 - t - 0.035, d / 2 - t)):
            kutu(y, V(x0, y0, Z0), X, x1 - x0, y1 - y0, hw, 'granit_koyu', 'onarkasagsol')
            y.yuz_yon([V(x0, y0, Z0 + hw), V(x1, y0, Z0 + hw), V(x1, y1, Z0 + hw), V(x0, y1, Z0 + hw)], 'cimen', Z)
        y.yuz_yon([V(-w / 2 + t, -d / 2 + t, Z0 + 0.002), V(w / 2 - t, -d / 2 + t, Z0 + 0.002), V(w / 2 - t, d / 2 - t, Z0 + 0.002), V(-w / 2 + t, d / 2 - t, Z0 + 0.002)], 'toprak', Z)
        # the awning: ridge pole on two forked posts, cloth strips down to the wall tops
        zr = Z0 + 0.17
        for sx in (-1, 1):
            y.prizma((sx * (w / 2 + 0.01), 0), 0.006, Z0, zr + 0.02, 'ahsap_koyu', n=6)
        cubuk(y, V(-w / 2 - 0.03, 0, zr + 0.004), V(w / 2 + 0.03, 0, zr + 0.004), 0.01, 'ahsap_koyu')
        m = 6
        for i in range(m):
            xa, xb = -w / 2 - 0.01 + (w + 0.02) * i / m, -w / 2 - 0.01 + (w + 0.02) * (i + 1) / m
            k = renk if i % 2 == 0 else serit
            for sy in (-1, 1):
                q = [V(xa, sy * (d / 2 + 0.012), Z0 + hw - 0.004), V(xb, sy * (d / 2 + 0.012), Z0 + hw - 0.004), V(xb, 0, zr), V(xa, 0, zr)]
                iki_yuzlu(y, q, k, V(0, sy, 0.6), kil=0.001)
        # the closed back gable (+x), a cloth flap tied back at the door (-x)
        y.yuz_yon([V(w / 2 + 0.01, -d / 2 - 0.012, Z0 + hw - 0.004), V(w / 2 + 0.01, d / 2 + 0.012, Z0 + hw - 0.004), V(w / 2 + 0.01, 0, zr)], renk, X)
        y.yuz_yon([V(w / 2 + 0.009, d / 2 + 0.012, Z0 + hw - 0.004), V(w / 2 + 0.009, -d / 2 - 0.012, Z0 + hw - 0.004), V(w / 2 + 0.009, 0, zr)], 'kumas', -X)
        for sy in (-1, 1):
            iki_yuzlu(y, [V(-w / 2 - 0.01, sy * (d / 2 + 0.012), Z0 + hw - 0.004), V(-w / 2 - 0.01, sy * 0.02, Z0 + 0.13), V(-w / 2 - 0.01, 0, zr)], serit, -X, kil=0.001)
        # bench, barrel
        kutu_merkez(y, (-w / 2 - 0.05, d / 2 - 0.01), 0.07, 0.022, 0.022, 'ahsap', z0=Z0)
        donel(y, (-w / 2 - 0.05, -d / 2 + 0.005), [(0.0, Z0), (0.017, Z0), (0.021, Z0 + 0.022), (0.017, Z0 + 0.044), (0.0, Z0 + 0.044)], 'ahsap_acik', n=10)
        for zz in (0.008, 0.034):
            halka_kornis(y, (-w / 2 - 0.05, -d / 2 + 0.005), 0.019 if zz < 0.02 else 0.0185, Z0 + zz, 0.004, 0.002, 10, 'demir')


y.bolum('Çardaklı barakalar (búðir)')
RB = 0.84
for i, (ang, renk, serit) in enumerate(((35, 'kumas', 'boya_kirmizi'), (5, 'beyaz', 'boya_yesil'), (-25, 'kumas', 'lacivert'),
                                        (145, 'beyaz', 'boya_kirmizi'), (175, 'kumas', 'boya_sari'), (205, 'beyaz', 'lacivert'))):
    a = math.radians(ang)
    budir((MC.x + RB * math.cos(a), MC.y + RB * math.sin(a)), a, renk=renk, serit=serit)

# ---------------- the assembly hall ----------------
y.bolum('Meclis salonu')
with parca(y, (0.0, 0.76, 0)):
    langhus(y, 1.12, 0.38, 0.15, 0.3, z0=Z0, bombe=0.12, sacak=0.045, cati='cimen', mahya='cimen', kalin=0.026, n=14, nr=7,
            kapilar=((-0.2, -1), (0.2, -1)), dumanlik=(0.0,), ejder_s=0.12, sirt=0.1, kat_lip=0.006, egri=0.12,
            sundurma_h=0.72, sundurma_c=0.06, dikme=0.1, kalkanlar=(-1,), tohum=5, saz_cizgi=2)

# ---------------- fire, barrels, carts ----------------
y.bolum('Ateş ve fıçılar')
FC = V(-0.42, -0.74)
for k in range(8):
    t = TAU * k / 8
    kure(y, (FC.x + 0.05 * math.cos(t), FC.y + 0.05 * math.sin(t), Z0 + 0.008), 0.014, 'granit', n=6, kat=3)
for r, h, key in ((0.03, 0.07, 'boya_kirmizi'), (0.019, 0.09, 'boya_sari'), (0.01, 0.06, 'beyaz')):
    y.koni((FC.x, FC.y), r, Z0 + 0.004, h, key, n=7)
for sx in (-1, 1):
    y.prizma((FC.x + sx * 0.07, FC.y), 0.004, Z0, Z0 + 0.12, 'ahsap_koyu', n=4)
cubuk(y, V(FC.x - 0.075, FC.y, Z0 + 0.115), V(FC.x + 0.075, FC.y, Z0 + 0.115), 0.005, 'ahsap_koyu')
donel(y, (FC.x, FC.y), [(0.0, Z0 + 0.06), (0.026, Z0 + 0.065), (0.03, Z0 + 0.09), (0.0, Z0 + 0.09)], 'demir', n=10)
# log benches round the fire
for k in range(3):
    t = TAU * k / 3 + 0.5
    c_ = V(FC.x + 0.15 * math.cos(t), FC.y + 0.15 * math.sin(t), Z0 + 0.014)
    e_ = V(-math.sin(t), math.cos(t), 0) * 0.07
    boru(y, [c_ - e_, c_ + e_], 0.014, 'kutuk', n=7)
yer([(FC.x + 0.1 * math.cos(TAU * i / 10), FC.y + 0.1 * math.sin(TAU * i / 10)) for i in range(10)], 'toprak')
for (bx, by) in ((0.6, 0.3), (0.65, 0.36), (0.56, 0.37)):
    donel(y, (bx, by), [(0.0, Z0), (0.02, Z0), (0.025, Z0 + 0.027), (0.02, Z0 + 0.054), (0.0, Z0 + 0.054)], 'ahsap_acik', n=10)
    for zz in (0.01, 0.042):
        halka_kornis(y, (bx, by), 0.023, Z0 + zz, 0.004, 0.002, 10, 'demir')

y.bolum('Ağaçlar')
for (tx, ty, b) in ((-1.0, 0.9, 0.32), (1.0, 0.9, 0.3), (-1.02, -0.3, 0.28), (1.02, -0.35, 0.3), (-0.9, -0.9, 0.26), (0.95, -0.92, 0.27)):
    cam_agaci(y, tx, ty, Z0, b, 'boya_yesil')

calistir(y, 'lm_thing')
