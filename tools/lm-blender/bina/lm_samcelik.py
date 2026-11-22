# Damascus Steel Foundry (lm_samcelik): a walled smithy yard in Damascus. Beehive crucible furnaces of mud brick with
# glowing stoke-holes and tall tapering brick chimneys trailing smoke, leather bellows, anvils with smiths at work, a
# quench pool, a shed of racks hung with damascened blades, heaps of charcoal and crucibles; at the back the workshop
# range with forge-lit arches and wind-catchers, the master's domed hall in the middle; the yard gate with ablaq
# voussoirs and a crossed-swords plaque.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir
from arap_ortak import *

y = Yapi()

Z0 = 0.04
TAS, ACIK, KOYU, KARA = 'kum', 'kum_acik', 'kum_koyu', 'bazalt'
AB = [ACIK, KARA]
REN = (TAS, KOYU, ACIK, 'koyu')
ATES = ('kerpic_tugla', 'koyu', 'boya_kirmizi', 'koyu')          # a forge bay: dark inside, red-hot floor (a hearth is set in it)
OCAK = ('kerpic_tugla', 'koyu', 'boya_kirmizi', 'boya_sari')    # a furnace's stoke-hole: the fire behind
XO, YO0, YO1 = 0.95, -0.72, 0.82
WH = 0.22                                  # the yard wall
YB = 0.44                                  # the workshop range's court face
ZB = Z0 + 0.3                              # its roof

y.bolum('Zemin')
zemin(y, -1.1, 1.1, -0.95, 0.96, Z0, 'kum_koyu', 'zemin', basamak=(('on', 0.5),), n_basamak=2)
y.yuz_yon([V(-XO, YO0, Z0 + 0.002), V(XO, YO0, Z0 + 0.002), V(XO, YB, Z0 + 0.002), V(-XO, YB, Z0 + 0.002)], 'toprak', Z)

# ---------------- the yard wall and gate ----------------
y.bolum('Avlu duvarı ve kapı')
sur(y, [V(-XO, YB), V(-XO, YO0), V(XO, YO0), V(XO, YB)], Z0, WH, kalinlik=0.05, key=TAS, kapali=False, mazgal_h=0, parapet_h=0.0001, ust_key=ACIK)
# a merloned crest on the wall's outer edge, buttresses outside and stone spouts
for (a, b) in ((V(-XO, YB), V(-XO, YO0)), (V(-XO, YO0), V(-0.17, YO0)), (V(0.17, YO0), V(XO, YO0)), (V(XO, YO0), V(XO, YB))):
    mazgalli_kenar(y, [a, b], Z0 + WH, TAS, kal=0.014, h=0.026, kapali=False, ust_key=ACIK, dolu=0.01, w=0.026, g=0.018)
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    L_ = (b - a).length
    nb = max(1, int(round(L_ / 0.36)))
    for k in range(1, nb):
        p = a.lerp(b, k / nb)
        kutu(y, p - e * 0.016 + nn * 0.014 + Z * Z0, e, 0.032, 0.014, WH - 0.02, TAS, 'onsagsolust')
        kutu(y, p - e * 0.02 + nn * 0.018 + Z * Z0, e, 0.04, 0.018, 0.03, KOYU, 'onsagsolust')
silme(y, [V(-XO, YB), V(-XO, YO0), V(XO, YO0), V(XO, YB)], Z0, 0.02, 0.006, KOYU, 'kaide', kapali=False)
for (a, b, n) in ((V(-XO, YB), V(-XO, YO0), 6), (V(-XO, YO0), V(-0.18, YO0), 4), (V(0.18, YO0), V(XO, YO0), 4), (V(XO, YO0), V(XO, YB), 6)):
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(n):
        p = a.lerp(b, (k + 0.5) / n)
        yarik(y, p + nn * 0.001, e, nn, -0.006, Z0 + WH * 0.45, 0.012, 0.05, 'koyu')
    ablak(y, a + nn * 0.0025, b + nn * 0.0025, Z0 + WH * 0.72, Z0 + WH * 0.72 + 0.02, AB, 0.01)
# the gate: a pointed arch with ablaq voussoirs, a crossed-swords plaque, merlons
GW, GD, GH = 0.32, 0.12, 0.38
gk = dikdortgen(-GW / 2, GW / 2, YO0 - 0.05, YO0 - 0.05 + GD)
L_, x0, x1, hs, ap = kemer_nis(y, gk[0], gk[1], Z0, GH, en=0.5, ust=0.13, sivri=0.6, derin=0.035, key=TAS, yan_key=KOYU, alt_key=ACIK,
                               arka_key='ahsap', k_say=12, cerceve=(0.016, AB))
for i in (1, 2, 3):
    duvar_bant(y, gk[i], gk[(i + 1) % 4], Z0, Z0 + GH, TAS, n=3)
ablak(y, gk[0] + V(0, -0.0025), gk[1] + V(0, -0.0025), Z0, Z0 + 0.04, AB, 0.02)
# the plaque: a framed panel with two crossed blades and a shield
PZ = Z0 + ap + 0.012
pl = [V(-0.06, YO0 - 0.053, PZ), V(0.06, YO0 - 0.053, PZ), V(0.06, YO0 - 0.053, PZ + 0.075), V(-0.06, YO0 - 0.053, PZ + 0.075)]
y.yuz_yon(pl, KARA, -Y)
for i in range(4):
    p, q = pl[i], pl[(i + 1) % 4]
    y.yuz_yon([p, q, q + V(0, 0.003, 0), p + V(0, 0.003, 0)], KARA, (p + q) / 2 - (pl[0] + pl[2]) / 2)
for s in (-1, 1):
    cubuk(y, V(s * 0.045, YO0 - 0.056, PZ + 0.012), V(-s * 0.03, YO0 - 0.056, PZ + 0.064), 0.006, 'granit', 0.002)
    cubuk(y, V(s * 0.05, YO0 - 0.057, PZ + 0.006), V(s * 0.038, YO0 - 0.057, PZ + 0.018), 0.008, 'altin', 0.002)
yildiz(y, (0.0, YO0 - 0.054, PZ + 0.037), X, -Y, 0.016, 'altin', k=8, ic=0.6, yan_key='bronz')
silme(y, gk, Z0 + GH - 0.018, 0.018, 0.01, ACIK, 'tac')
mazgalli_kenar(y, disa(gk, 0.0), Z0 + GH, TAS, kal=0.016, h=0.03, ust_key=ACIK, dolu=0.012, w=0.024, g=0.014, kademe=True)
y.yuz_yon([V(p.x, p.y, Z0 + GH) for p in disa(gk, -0.016)], 'zemin', Z)
sancak(y, 0.1, YO0 + 0.0, Z0 + GH, boy=0.2, en=0.11, yuk=0.07, aci=-0.4)

# ---------------- the workshop range and the domed hall ----------------
y.bolum('Atölye kanadı ve kubbeli usta salonu')
HW_ = 0.25                                  # the hall's half width
for (xa, xb) in ((-XO, -HW_), (HW_, XO)):
    n = 4
    for j in range(n):
        p, q = V(xa + (xb - xa) * j / n, YB), V(xa + (xb - xa) * (j + 1) / n, YB)
        glow = (j + (0 if xa < 0 else 1)) % 2 == 0
        y.kemerli(p, q, Z0, ZB - Z0, ATES if glow else REN, v0=0.0, en=0.66, ust=0.06, derin=0.05, k_say=10, sivri=0.6, cerceve=(0.008, AB))
        if glow:   # a forge hearth inside the dark bay: a brick block, red coals, flames
            m = (p + q) / 2 + V(0, 0.028)
            kutu_merkez(y, (m.x, m.y), 0.07, 0.03, 0.045, 'tugla', z0=Z0)
            kutu_merkez(y, (m.x, m.y), 0.056, 0.022, 0.002, 'boya_kirmizi', z0=Z0 + 0.045)
            for dx, hh in ((-0.012, 0.03), (0.006, 0.042), (0.018, 0.026)):
                donel(y, (m.x + dx, m.y), [(0.0, Z0 + 0.046), (0.008, Z0 + 0.046), (0.005, Z0 + 0.046 + hh * 0.5), (0.0, Z0 + 0.046 + hh)], 'boya_sari', n=6)
    silme(y, [V(xa, YB), V(xb, YB)], ZB - 0.016, 0.016, 0.01, ACIK, 'tac', kapali=False)
    y.yuz_yon([V(xa, YB, ZB), V(xb, YB, ZB), V(xb, YO1, ZB), V(xa, YO1, ZB)], 'zemin', Z)
    dam_bolme(y, xa, xb, YB, YO1, ZB, ACIK)
for (a, b) in ((V(XO, YB), V(XO, YO1)), (V(XO, YO1), V(-XO, YO1)), (V(-XO, YO1), V(-XO, YB))):
    kat_pencere(y, a, b, Z0, ZB, Z0 + 0.16, Z0 + 0.24, max(2, int((b - a).length / 0.2)), REN, en=0.3, sivri=0.6, derin=0.012)
    silme(y, [a, b], ZB - 0.016, 0.016, 0.01, ACIK, 'tac', kapali=False)
for yol_ in ([V(HW_, YB), V(XO, YB), V(XO, YO1), V(HW_, YO1)], [V(-HW_, YO1), V(-XO, YO1), V(-XO, YB), V(-HW_, YB)]):   # (broken at the hall's back)
    mazgalli_kenar(y, yol_, ZB, TAS, kal=0.016, h=0.024, kapali=False, ust_key=ACIK, dolu=0.012, w=0.03, g=0.022)
for (cx, cy) in ((-0.75, 0.63), (-0.42, 0.63), (0.42, 0.63), (0.75, 0.63)):
    y.prizma((cx, cy), 0.055, ZB, ZB + 0.014, ACIK, n=12, ust=False)
    y.kubbe((cx, cy), 0.055, ZB + 0.014, 0.04, ACIK, n=12, kat=4)


for (cx, cy) in ((-0.6, 0.72), (0.6, 0.72)):
    malqaf(y, cx, cy, ZB, key=ACIK)
# the master's hall: walls rising over the range, a portal on the court, the dome on a windowed drum
ZH = Z0 + 0.44
hk = dikdortgen(-HW_, HW_, YB - 0.08, YO1)
for i in range(4):
    a, b = hk[i], hk[(i + 1) % 4]
    if i == 0:
        n = 3
        for j in range(n):
            p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
            if j == 1:
                kemer_nis(y, p, q, Z0, ZH - Z0 - 0.03, en=0.72, ust=0.03, sivri=0.6, derin=0.03, key=TAS, yan_key=KOYU, alt_key=ACIK,
                          arka_key='ahsap', k_say=10, cerceve=(0.012, AB))
                duz_duvar(y, p, q, ZH - 0.03, ZH, TAS)
            else:
                kat_pencere(y, p, q, Z0, Z0 + 0.18, Z0 + 0.08, Z0 + 0.17, 1, REN, en=0.42, derin=0.012, cerceve=(0.006, KARA))   # (up to the upper row only: overlapping walls flickered)
                kat_pencere(y, p, q, Z0 + 0.18, ZH, Z0 + 0.26, Z0 + 0.36, 1, REN, en=0.4, sivri=0.6, derin=0.012)
    else:
        if i != 2:   # (the back below the range's roof is the range's own outer wall)
            duvar_bant(y, a, b, Z0, ZB, TAS, n=2)
        kat_pencere(y, a, b, ZB, ZH, ZB + 0.03, ZH - 0.025, 2, REN, en=0.32, sivri=0.6, derin=0.01)
ablak(y, hk[0] + V(0, -0.0025), hk[1] + V(0, -0.0025), ZH - 0.05, ZH - 0.014, AB, 0.012)
# an inscription band between the window rows of the side bays (the door bay keeps its tall arch)
for (pa, pb) in ((hk[0], hk[0].lerp(hk[1], 1 / 3)), (hk[0].lerp(hk[1], 2 / 3), hk[1])):
    cini_bant(y, pa, pb, Z0 + 0.19, 0.014, (KARA, ACIK), n=6)
    oluk(y, pa, pb, 1, ZH - 0.05, KOYU)
# stone spouts on the range's outer walls
for (a, b, n) in ((V(XO, YB), V(XO, YO1), 2), (V(XO, YO1), V(-XO, YO1), 8), (V(-XO, YO1), V(-XO, YB), 2)):
    oluk(y, a, b, n, ZB - 0.016, KOYU)
silme(y, hk, ZH - 0.014, 0.014, 0.01, ACIK, 'tac')
mazgalli_kenar(y, hk, ZH, TAS, kal=0.014, h=0.026, ust_key=ACIK, dolu=0.01, w=0.024, g=0.015, kademe=True)
y.yuz_yon([V(p.x, p.y, ZH) for p in disa(hk, -0.014)], 'zemin', Z)
HC = (0.0, (YB - 0.08 + YO1) / 2)
zd = kubbe_kasnakli(y, HC, 0.18, ZH, 0.07, n_pencere=12, kubbe_h=0.2, key=ACIK, duvar=(TAS, KOYU, ACIK, 'koyu'), payanda=False,
                    alem_olcek=0, n=32, kat=10, en=0.45, cerceve=(0.004, KARA))
# ribs on the dome and a finial ball
for k in range(12):
    a = TAU * (k + 0.5) / 12
    pts = [V(HC[0] + 0.186 * math.cos(math.pi / 2 * t / 6) * math.cos(a), HC[1] + 0.186 * math.cos(math.pi / 2 * t / 6) * math.sin(a),
             ZH + 0.07 + 0.016 + 0.203 * math.sin(math.pi / 2 * t / 6)) for t in range(6)]
    boru(y, pts, 0.004, KOYU, n=3)
donel(y, HC, [(0.0, zd - 0.004), (0.02, zd - 0.004), (0.016, zd + 0.012), (0.0, zd + 0.014)], ACIK, n=10)
kure(y, (HC[0], HC[1], zd + 0.03), 0.014, 'altin', n=10, kat=5)

# ---------------- the crucible furnaces and chimneys ----------------
y.bolum('Pota fırınları ve yüksek bacalar')


def duman(x, yy, z, n=4, r=0.035, yon=(1, 0.3)):
    """a plume of smoke: billows of clustered puffs rising, swelling, drifting downwind and paling"""
    for k in range(n):
        t = k / max(1, n - 1)
        c = V(x + yon[0] * 0.045 * k * (1 + k * 0.4), yy + yon[1] * 0.045 * k, z + 0.025 + k * 0.055)
        rr = r * (0.75 + 0.6 * t)
        key = ('granit_koyu', 'granit', 'kaya', 'kaya')[min(3, k)]
        for j, (dx, dy, dz, s) in enumerate(((0.0, 0.0, 0.0, 1.0), (0.6, 0.3, -0.25, 0.72), (-0.5, -0.35, -0.15, 0.68), (0.1, -0.2, 0.45, 0.6))):
            if j == 3 and k == 0: continue
            kure(y, (c.x + dx * rr, c.y + dy * rr, c.z + dz * rr), rr * s, key, n=10, kat=5)


def firin(cx, cy, r, aci, baca_h, baca_w=0.08):
    """a beehive crucible furnace: a brick drum, a mud dome, a stoke-hole porch facing aci with the fire inside, and
    a tall tapering brick chimney rising behind it with bands, a corbelled crown and smoke"""
    c = V(cx, cy)
    d = V(math.cos(aci), math.sin(aci)); s_ = V(-d.y, d.x)
    y.prizma((cx, cy), r + 0.07, Z0 + 0.002, Z0 + 0.0035, 'granit_koyu', n=20)     # the scorched ground round it
    y.prizma((cx, cy), r, Z0, Z0 + 0.07, 'kerpic_tugla', n=20, ust=False)
    halka_kornis(y, (cx, cy), r, Z0 + 0.065, 0.01, 0.006, 20, 'tugla_koyu')
    donel(y, (cx, cy), [(r, Z0 + 0.075), (r * 0.97, Z0 + 0.11), (r * 0.82, Z0 + 0.16), (r * 0.55, Z0 + 0.2), (r * 0.25, Z0 + 0.222), (0.0, Z0 + 0.226)], 'kerpic', n=20)
    # hoops of iron round the dome's foot and a vent on top
    halka_kornis(y, (cx, cy), r * 0.98, Z0 + 0.09, 0.006, 0.004, 20, 'demir')
    y.prizma((cx, cy), r * 0.2, Z0 + 0.218, Z0 + 0.235, 'tugla_koyu', n=8, ust=False)
    y.yuz_yon([V(cx + r * 0.17 * math.cos(TAU * i / 8), cy + r * 0.17 * math.sin(TAU * i / 8), Z0 + 0.236) for i in range(8)], 'boya_kirmizi', Z)
    for i in range(8):
        p = [V(cx + r * 0.2 * math.cos(TAU * j / 8), cy + r * 0.2 * math.sin(TAU * j / 8), Z0 + 0.235) for j in (i, i + 1)]
        q = [V(cx + r * 0.17 * math.cos(TAU * j / 8), cy + r * 0.17 * math.sin(TAU * j / 8), Z0 + 0.236) for j in (i, i + 1)]
        y.yuz_yon([p[0], p[1], q[1], q[0]], 'tugla_koyu', Z)
    # the stoke-hole porch
    pw, pd, ph = 0.1, 0.07, 0.11
    o = c + d * (r - 0.03)
    a_, b_ = o + d * pd - s_ * (pw / 2), o + d * pd + s_ * (pw / 2)
    y.kemerli(a_, b_, Z0, ph, OCAK, v0=0.02, en=0.56, ust=0.016, derin=0.04, k_say=8, sivri=0.55, cerceve=(0.006, 'tugla_koyu'))
    for sg in (-1, 1):
        p, q = (o + s_ * (sg * pw / 2), o + d * pd + s_ * (sg * pw / 2))
        if sg > 0: p, q = q, p
        duz_duvar(y, p, q, Z0, Z0 + ph, 'kerpic_tugla')
    y.yuz_yon([V(p.x, p.y, Z0 + ph) for p in (o - s_ * (pw / 2), a_, b_, o + s_ * (pw / 2))], 'tugla_koyu', Z)
    # glowing embers spilling onto the ground before it
    for k in range(4):
        e_ = c + d * (r + pd + 0.012 + 0.01 * (k % 2)) + s_ * (0.02 * (k - 1.5))
        kure(y, (e_.x, e_.y, Z0 + 0.004), 0.006, 'boya_kirmizi' if k % 2 else 'boya_sari', n=6, kat=3)
    # the chimney behind
    bc = c - d * (r * 0.75)
    w0, w1 = baca_w * 0.5 * 1.414, baca_w * 0.36 * 1.414
    zt = Z0 + baca_h
    donel(y, (bc.x, bc.y), [(w0, Z0), (w0 * 0.96, Z0 + baca_h * 0.25), (w0 * 0.88, Z0 + baca_h * 0.5), (w0 * 0.8, Z0 + baca_h * 0.75), (w1, zt)],
          'tugla_koyu', n=4, kat=aci + math.pi / 4)
    for t in (0.3, 0.55, 0.8):
        halka_kornis(y, (bc.x, bc.y), w0 * (1 - 0.2 * t) + 0.0005, Z0 + baca_h * t, 0.012, 0.004, 4, ACIK, kat=aci + math.pi / 4)
    konsol_halka(y, cokgen((bc.x, bc.y), w1, 4, aci + math.pi / 4), zt - 0.02, 0.02, 0.012, 'tugla', 2)
    cr = cokgen((bc.x, bc.y), w1 + 0.012 * 1.414, 4, aci + math.pi / 4)
    parapet(y, cr, zt, 0.02, 0, 0.014, 'tugla_koyu', ust_key='tugla')
    y.yuz_yon([V(p.x, p.y, zt + 0.004) for p in disa(cr, -0.014)], 'koyu', Z)
    duman(bc.x, bc.y, zt + 0.02, n=4, r=baca_w * 0.42)
    return bc


firin(-0.6, 0.06, 0.13, 0.25, 0.92)
firin(-0.58, -0.38, 0.12, 0.6, 0.78)
firin(0.42, 0.13, 0.12, math.pi - 0.5, 1.02, 0.09)

y.bolum('Körükler, örsler, demirciler, su havuzu')


def koruk(x, yy, aci):
    """a pair of leather bellows on a wooden frame, the nozzle towards aci"""
    with parca(y, (x, yy, Z0), aci):
        for sy in (-1, 1):
            b0 = [V(0.0, sy * 0.012 - 0.008, 0.02), V(0.0, sy * 0.012 + 0.008, 0.02), V(-0.07, sy * 0.012 + 0.012, 0.02), V(-0.07, sy * 0.012 - 0.012, 0.02)]
            t0 = [V(0.0, sy * 0.012 - 0.008, 0.024), V(0.0, sy * 0.012 + 0.008, 0.024), V(-0.07, sy * 0.012 + 0.012, 0.05), V(-0.07, sy * 0.012 - 0.012, 0.05)]
            y.yuz_yon(b0, 'ahsap', -Z)
            y.yuz_yon(t0, 'ahsap', V(-0.3, 0, 1))
            for k in range(4):
                j = (k + 1) % 4
                y.yuz_yon([b0[k], b0[j], t0[j], t0[k]], 'ahsap_acik' if k != 0 else 'ahsap', (b0[k] + b0[j]) / 2 - V(-0.035, sy * 0.012, 0.02))
            cubuk(y, V(-0.07, sy * 0.012, 0.05), V(-0.09, sy * 0.012, 0.06), 0.004, 'ahsap_koyu')
        kutu_merkez(y, (-0.035, 0.0), 0.08, 0.05, 0.02, 'ahsap_koyu')
        cubuk(y, V(0.0, 0.0, 0.022), V(0.04, 0.0, 0.026), 0.007, 'demir')


def ors(x, yy, aci):
    """an anvil on a stump with a glowing blade on it"""
    with parca(y, (x, yy, Z0), aci):
        y.prizma((0, 0), 0.02, 0.0, 0.035, 'ahsap_koyu', n=8)
        kutu_merkez(y, (0, 0), 0.044, 0.018, 0.008, 'demir', z0=0.035)
        kutu_merkez(y, (0, 0), 0.026, 0.012, 0.008, 'demir', z0=0.043)
        kutu_merkez(y, (0.0, 0.0), 0.05, 0.02, 0.006, 'demir', z0=0.051)
        boru(y, [V(0.025, 0, 0.054), V(0.045, 0, 0.054)], 0.007, 'demir', n=6, r_son=0.001)
        cubuk(y, V(-0.03, 0.002, 0.0585), V(0.02, 0.002, 0.0585), 0.006, 'boya_kirmizi', 0.0015)


def demirci(x, yy, aci, govde='kumas', kaldir=True):
    """a smith in an apron raising (or resting) his hammer"""
    adam(y, x, yy, Z0, aci, govde=govde, bas='beyaz', boy=0.07)
    with parca(y, (x, yy, Z0), aci):
        kutu_merkez(y, (0.012, 0.0), 0.004, 0.022, 0.03, 'ahsap_koyu', z0=0.014)
        if kaldir:
            boru(y, [V(0.004, -0.008, 0.045), V(0.012, -0.012, 0.075), V(0.016, -0.012, 0.09)], 0.004, govde, n=4)
            cubuk(y, V(0.016, -0.012, 0.088), V(0.03, -0.012, 0.1), 0.003, 'ahsap')
            kutu_merkez(y, (0.031, -0.012), 0.012, 0.008, 0.012, 'demir', z0=0.094)
        else:
            cubuk(y, V(0.01, -0.012, 0.04), V(0.035, -0.012, 0.015), 0.003, 'ahsap')
            kutu_merkez(y, (0.036, -0.012), 0.012, 0.008, 0.012, 'demir', z0=0.008)


koruk(-0.64, 0.27, -0.6)
koruk(-0.79, -0.22, 0.3)
koruk(0.61, 0.3, 3.5)
for (x, yy, a, sx, sy, sa, g) in ((-0.22, -0.18, 0.1, -0.3, -0.18, 0.1, 'kumas'), (0.02, -0.4, -0.3, -0.06, -0.44, -0.3, 'boya_kirmizi'),
                                   (0.18, -0.08, 2.6, 0.26, -0.04, 2.6 + math.pi, 'ahsap_acik')):
    ors(x, yy, a)
    demirci(sx, sy, math.atan2(yy - sy, x - sx), govde=g)
demirci(-0.12, 0.08, 0.4, govde='lacivert', kaldir=False)
# the quench pool with a little steam
havuz(y, -0.2, 0.08, 0.2, 0.3, Z0 + 0.008, derin=0.008, kenar=0.016, key=KOYU)   # (water above the yard floor)
for (x, yy, r) in ((-0.06, 0.25, 0.022), (-0.03, 0.26, 0.016), (-0.07, 0.27, 0.013)):
    kure(y, (x, yy, Z0 + 0.04 + (0.022 - r) * 2), r, 'beyaz', n=8, kat=4)
cubuk(y, V(-0.2, 0.18, Z0 + 0.015), V(-0.12, 0.24, Z0 + 0.025), 0.004, 'boya_kirmizi', 0.0015)

y.bolum('Kılıç rafları, kömür, potalar')
# the shed on the east wall: a lean-to roof on posts sheltering the blade racks
SX0, SX1, SY0, SY1 = 0.66, XO - 0.05, -0.62, -0.12
for yy in (SY0 + 0.02, (SY0 + SY1) / 2, SY1 - 0.02):
    cubuk(y, V(SX0, yy, Z0), V(SX0, yy, Z0 + 0.16), 0.01, 'ahsap_koyu')
cubuk(y, V(SX0, SY0, Z0 + 0.16), V(SX0, SY1, Z0 + 0.16), 0.01, 'ahsap', 0.012)
fa, fb = V(SX0 - 0.025, SY0 - 0.02, Z0 + 0.163), V(SX0 - 0.025, SY1 + 0.02, Z0 + 0.163)
ba, bb = V(SX1, SY0 - 0.02, Z0 + WH - 0.01), V(SX1, SY1 + 0.02, Z0 + WH - 0.01)
dz = Z * 0.006
y.yuz_yon([fa, fb, bb, ba], 'ahsap_dikey', V(-0.4, 0, 1))
y.yuz_yon([fa - dz, fb - dz, bb - dz, ba - dz], 'ahsap_koyu', -Z)
y.yuz_yon([fa, fb, fb - dz, fa - dz], 'ahsap_koyu', -X)
y.yuz_yon([fa, ba, ba - dz, fa - dz], 'ahsap_koyu', -Y)
y.yuz_yon([fb, bb, bb - dz, fb - dz], 'ahsap_koyu', Y)


def kilic_rafi(x, y0, y1, n=7):
    """a rack of curved damascened sabres standing points-up between two rails"""
    for yy in (y0, y1):
        cubuk(y, V(x, yy, Z0), V(x, yy, Z0 + 0.12), 0.008, 'ahsap_koyu')
    for zz in (Z0 + 0.03, Z0 + 0.1):
        cubuk(y, V(x, y0, zz), V(x, y1, zz), 0.006, 'ahsap', 0.008)
    for k in range(n):
        yy = y0 + (y1 - y0) * (k + 0.5) / n
        xb = x - 0.009
        boru(y, [V(xb, yy, Z0 + 0.03), V(xb - 0.002, yy, Z0 + 0.07), V(xb - 0.008, yy, Z0 + 0.11), V(xb - 0.016, yy, Z0 + 0.135)], 0.0032, 'granit', n=3, r_son=0.0012)
        cubuk(y, V(xb, yy - 0.008, Z0 + 0.028), V(xb, yy + 0.008, Z0 + 0.028), 0.003, 'altin')
        cubuk(y, V(xb, yy, Z0 + 0.028), V(xb, yy, Z0 + 0.008), 0.004, 'ahsap_koyu')
        kure(y, (xb, yy, Z0 + 0.006), 0.004, 'altin', n=6, kat=3)


kilic_rafi(0.78, SY0 + 0.03, (SY0 + SY1) / 2 - 0.01)
kilic_rafi(0.78, (SY0 + SY1) / 2 + 0.01, SY1 - 0.03)
# blades cooling on a bench under the shed
kutu_merkez(y, (0.69, (SY0 + SY1) / 2), 0.04, 0.3, 0.04, 'ahsap', z0=Z0)
for k in range(5):
    yy = SY0 + 0.07 + k * 0.08
    cubuk(y, V(0.685, yy - 0.03, Z0 + 0.0425), V(0.685, yy + 0.03, Z0 + 0.0425), 0.006, 'granit' if k % 2 else 'boya_kirmizi', 0.0015)
# charcoal heaps, a stack of crucibles, the wootz cakes
for (x, yy, r) in ((-0.82, 0.25, 0.06), (-0.33, -0.4, 0.055), (0.62, 0.36, 0.045)):
    donel(y, (x, yy), [(r, Z0 + 0.002), (r * 0.7, Z0 + r * 0.45), (r * 0.25, Z0 + r * 0.75), (0.0, Z0 + r * 0.8)], KARA, n=10)
for k in range(9):
    x = -0.3 + (k % 3) * 0.035
    yy = -0.6 + (k // 3) * 0.035
    donel(y, (x, yy), [(0.0, Z0 + 0.002), (0.012, Z0 + 0.002), (0.016, Z0 + 0.03), (0.013, Z0 + 0.032), (0.0, Z0 + 0.03)], 'kiremit2', n=8)
for k in range(6):
    donel(y, (-0.08 + (k % 3) * 0.03, -0.62 + (k // 3) * 0.03), [(0.0, Z0 + 0.002), (0.012, Z0 + 0.002), (0.012, Z0 + 0.01), (0.0, Z0 + 0.011)], 'demir', n=8)
# firewood stack against the west wall
for k in range(4):
    for j in range(6 - k):
        boru(y, [V(-0.88, -0.05 + j * 0.022 + k * 0.011, Z0 + 0.011 + k * 0.019), V(-0.8, -0.05 + j * 0.022 + k * 0.011, Z0 + 0.011 + k * 0.019)], 0.01, 'kutuk', n=5)

y.bolum('Ambarlar, araba, bileği taşı')
# storerooms in the front corner: arched doors, a flat roof with small domes and a parapet, a stair up
S0, S1, T0, T1, HS = -XO + 0.05, -0.44, YO0 + 0.05, -0.5, 0.19
for j in range(3):
    p, q = V(S1 - (S1 - S0) * j / 3, T1), V(S1 - (S1 - S0) * (j + 1) / 3, T1)
    y.kemerli(p, q, Z0, HS, (TAS, KOYU, ACIK, 'ahsap'), v0=0.0, en=0.42, ust=0.05, derin=0.02, k_say=8, sivri=0.6, cerceve=(0.006, AB))
kat_pencere(y, V(S1, T0), V(S1, T1), Z0, Z0 + HS, Z0 + 0.08, Z0 + 0.14, 1, REN, en=0.36, sivri=0.6, derin=0.01)
silme(y, [V(S1, T0), V(S1, T1), V(S0, T1)], Z0 + HS - 0.014, 0.014, 0.008, ACIK, 'tac', kapali=False)
y.yuz_yon([V(S0, T0, Z0 + HS), V(S1, T0, Z0 + HS), V(S1, T1, Z0 + HS), V(S0, T1, Z0 + HS)], 'zemin', Z)
parapet(y, [V(S1, T0), V(S1, T1), V(S0, T1)], Z0 + HS, 0.016, 0, 0.012, TAS, kapali=False, ust_key=ACIK)
for k in range(2):
    cx = S0 + (S1 - S0) * (k + 0.5) / 2
    y.prizma((cx, (T0 + T1) / 2), 0.05, Z0 + HS, Z0 + HS + 0.012, ACIK, n=12, ust=False)
    y.kubbe((cx, (T0 + T1) / 2), 0.05, Z0 + HS + 0.012, 0.035, ACIK, n=12, kat=4)
merdiven(y, (S1 + 0.035, T1 - 0.02), -math.pi / 2, 0.04, Z0, Z0 + HS, n=8, d=0.016, key=TAS, yanlik=ACIK)
# the path from the gate to the master's hall
y.yuz_yon([V(-0.06, YO0 + 0.05, Z0 + 0.003), V(0.06, YO0 + 0.05, Z0 + 0.003), V(0.06, 0.18, Z0 + 0.003), V(-0.06, 0.18, Z0 + 0.003)], KOYU, Z)
y.yuz_yon([V(-0.06, 0.32, Z0 + 0.003), V(0.06, 0.32, Z0 + 0.003), V(0.06, YB - 0.08, Z0 + 0.003), V(-0.06, YB - 0.08, Z0 + 0.003)], KOYU, Z)
# a two-wheeled cart of charcoal by the gate
with parca(y, (0.3, -0.52, Z0), 0.35):
    kutu_merkez(y, (0.0, 0.0), 0.12, 0.07, 0.025, 'ahsap', z0=0.03)
    for sy in (-1, 1):
        boru(y, [V(0.0, sy * 0.04, 0.03), V(0.0, sy * 0.048, 0.03)], 0.03, 'ahsap_koyu', n=12)
        cubuk(y, V(-0.06, sy * 0.025, 0.04), V(-0.15, sy * 0.025, 0.02), 0.006, 'ahsap_koyu')
    donel(y, (0.0, 0.0), [(0.05, 0.055), (0.035, 0.075), (0.012, 0.087), (0.0, 0.089)], KARA, n=10)
# a grinding wheel for the blades, turned by an apprentice
GX_, GY_ = 0.56, -0.2
for sx in (-1, 1):
    cubuk(y, V(GX_ + sx * 0.02, GY_, Z0), V(GX_ + sx * 0.02, GY_, Z0 + 0.06), 0.008, 'ahsap_koyu')
boru(y, [V(GX_ - 0.008, GY_, Z0 + 0.05), V(GX_ + 0.008, GY_, Z0 + 0.05)], 0.035, 'granit', n=14)
cubuk(y, V(GX_ - 0.03, GY_, Z0 + 0.05), V(GX_ + 0.04, GY_, Z0 + 0.05), 0.004, 'demir')
cubuk(y, V(GX_ + 0.04, GY_, Z0 + 0.05), V(GX_ + 0.04, GY_ - 0.02, Z0 + 0.05), 0.004, 'demir')
kutu_merkez(y, (GX_, GY_), 0.06, 0.03, 0.012, 'ahsap', z0=Z0)
demirci(GX_ + 0.07, GY_ - 0.02, math.pi, govde='boya_sari', kaldir=False)
demirci(GX_ - 0.05, GY_ + 0.03, -0.6, govde='kumas', kaldir=False)
# iron ore and bar stock by the east furnace: a rusty heap and a crib of bars
donel(y, (0.63, -0.03), [(0.06, Z0 + 0.002), (0.045, Z0 + 0.025), (0.02, Z0 + 0.042), (0.0, Z0 + 0.046)], 'kiremit2', n=10)
for k in range(5):
    kure(y, (0.63 + 0.04 * math.cos(k * 1.3), -0.03 + 0.04 * math.sin(k * 1.3), Z0 + 0.012), 0.01, 'demir', n=6, kat=3)
for j in range(3):
    for k in range(4 - j):
        cubuk(y, V(0.52 + 0.012 * k + 0.006 * j, -0.12, Z0 + 0.006 + 0.008 * j), V(0.52 + 0.012 * k + 0.006 * j, -0.04, Z0 + 0.006 + 0.008 * j), 0.007, 'demir', 0.007)
# the smiths' bench under the west range: tongs, hammers, files laid out
kutu_merkez(y, (-0.38, 0.37), 0.16, 0.045, 0.04, 'ahsap', z0=Z0)
for k in range(4):
    x = -0.44 + k * 0.035
    cubuk(y, V(x, 0.36, Z0 + 0.042), V(x + 0.012, 0.38, Z0 + 0.042), 0.004, 'demir', 0.002)
kutu_merkez(y, (-0.3, 0.37), 0.02, 0.012, 0.008, 'demir', z0=Z0 + 0.04)
# water jars by the quench pool
for (x, yy) in ((0.13, 0.22), (0.15, 0.27), (0.12, 0.31)):
    kup(y, x, yy, Z0 + 0.002, r=0.015, h=0.042, key='kiremit')
for (x, yy) in ((-1.03, -0.88), (1.03, -0.88), (-1.03, 0.9), (1.03, 0.9)):
    agac(y, x, yy, Z0, boy=0.2, tur='palmiye', key='boya_yesil')

calistir(y, 'lm_samcelik')
