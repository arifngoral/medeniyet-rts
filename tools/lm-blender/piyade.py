# Piyade (infantry swordsman) in the card art's manner, detailed: shaped face (eyes with whites, arched brows, nose
# bridge, a beard hugging the jaw, a drooping moustache), kettle helmet with a rolled brim and rivets, mail shirt,
# a blue tabard (team colour) with gold trim that bends with the body, belt with brass buckle and pouch, bracers
# with straps, gloved hands with fingers closed round the sword grip and the shield's strap, boots with turned cuffs,
# a sword with a diamond blade, a plank shield with a painted centre, iron rim, rivets and boss.
# 20 bones; actions bekle (idle), yuru (walk), saldir (attack), ol (death). Textures baked (karakter.pisir).
# blender -b --python tools/lm-blender/piyade.py -- <out.glb> [preview folder]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector, Matrix
from karakter import Karakter, iskelet, bagla, eylem, disa_aktar, pisir, yumusak
from ortak import argumanlar

k = Karakter()


def don_z(w):
    return Vector((0, 0, 1)).rotation_difference(Vector(w).normalized()).to_matrix()


def eksenler(a, b, c):
    """a rotation whose x, y, z columns are a, b, c"""
    return Matrix((a, b, c)).transposed()


# ---------------- skeleton ----------------
OMUZ_Z, KALCA_Z = 1.33, 0.95
A = math.radians(33)
def kol_yon(s): return Vector((math.sin(A) * s, -0.06, -math.cos(A))).normalized()
L_UST, L_ALT, L_EL = 0.28, 0.25, 0.11
kemik = [('kok', (0, 0, 0), (0, 0, 0.25), None),
         ('kalca', (0, 0, KALCA_Z), (0, 0, 1.08), 'kok'),
         ('bel', (0, 0, 1.08), (0, 0, 1.22), 'kalca'),
         ('gogus', (0, 0, 1.22), (0, 0, 1.38), 'bel'),
         ('boyun', (0, 0, 1.38), (0, 0, 1.46), 'gogus'),
         ('kafa', (0, 0, 1.46), (0, 0, 1.86), 'boyun'),
         ('etek_on', (0, -0.17, 0.95), (0, -0.2, 0.5), 'kalca'), ('etek_arka', (0, 0.17, 0.95), (0, 0.2, 0.5), 'kalca')]
P = {}
for s, ad in ((1, 'sol'), (-1, 'sag')):          # sol = the character's left = +x (it faces -y)
    d = kol_yon(s)
    o = Vector((s * 0.27, 0, OMUZ_Z)); e = o + d * L_UST; w = e + d * L_ALT; h = w + d * L_EL
    P[ad] = dict(d=d, omuz=o, dirsek=e, bilek=w, el=h)
    kemik += [('kol_ust_' + ad, o, e, 'gogus'), ('kol_alt_' + ad, e, w, 'kol_ust_' + ad), ('el_' + ad, w, h, 'kol_alt_' + ad)]
    x = s * 0.12
    kemik += [('uyluk_' + ad, (x, 0, KALCA_Z), (x, 0, 0.53), 'kalca'), ('baldir_' + ad, (x, 0, 0.53), (x, 0, 0.13), 'uyluk_' + ad),
              ('ayak_' + ad, (x, 0, 0.13), (x, -0.17, 0.04), 'baldir_' + ad)]


# weights: the trunk and the tabard over it blend kalca -> bel -> gogus up the body (they bend together)
def govde(p):
    a = yumusak(1.0, 1.14, p.z); b = yumusak(1.14, 1.28, p.z)
    return {'kalca': 1 - a, 'bel': a * (1 - b), 'gogus': a * b}
def etek(bone):
    return lambda p: {'kalca': yumusak(0.8, 0.94, p.z), bone: 1 - yumusak(0.8, 0.94, p.z)}


# ---------------- head ----------------
HC = Vector((0, 0, 1.61))
k.kure(HC, 0.165, 'ten', 'kafa', n=16, k=12, olcek=(1, 0.96, 1.08))
k.kure((0, -0.045, 1.525), 0.12, 'ten', 'kafa', n=14, k=8, olcek=(1.05, 0.95, 0.72))            # jaw
k.tup((0, -0.15, 1.665), (0, -0.177, 1.603), 0.017, 0.024, 'ten', 'kafa', n=8)                   # nose bridge
k.kure((0, -0.178, 1.597), 0.032, 'ten', 'kafa', n=12, k=8, olcek=(1.15, 0.85, 0.9))              # nose tip
for s in (1, -1):
    # eyes set into the face under a lid, brows over them
    k.kure((s * 0.056, -0.136, 1.643), 0.024, 'goz_ak', 'kafa', n=12, k=8, olcek=(1.1, 0.55, 0.75))
    k.kure((s * 0.054, -0.1465, 1.642), 0.011, 'goz', 'kafa', n=10, k=6, olcek=(1, 0.45, 1.15))
    k.yol([(s * 0.028, -0.143, 1.652), (s * 0.056, -0.153, 1.66), (s * 0.084, -0.142, 1.651)], [0.008, 0.011, 0.008], 'ten', 'kafa', n=8, ey=0.8)
    k.yol([(s * 0.02, -0.157, 1.671), (s * 0.056, -0.163, 1.68), (s * 0.092, -0.149, 1.672)], [0.011, 0.014, 0.009], 'sakal', 'kafa', n=8, ey=0.7)
    k.kure((s * 0.162, 0.0, 1.6), 0.042, 'ten', 'kafa', n=10, k=6, olcek=(0.45, 0.85, 1.25))      # ears
# a beard hugging the jaw (thick at the chin, thin up the cheeks), the moustache, a lower lip
def sakal_kalin(lo, la):
    on = 1 - 0.6 * min(1, abs(lo + 90) / 70)
    return 0.004 + 0.04 * yumusak(25, 75, -la) * on + 0.006 * on
k.kure((0, -0.085, 1.495), 0.1, 'sakal', 'kafa', n=16, k=10, olcek=(1.15, 0.95, 0.85))                # chin
cene = [(math.cos(math.radians(a)) * 0.132, math.sin(math.radians(a)) * 0.112 - 0.025, 1.56 - 0.075 * math.sin(math.radians(-a))) for a in range(-10, -171, -20)]
k.yol(cene, [0.03, 0.036, 0.042, 0.048, 0.048, 0.042, 0.036, 0.03, 0.028][:len(cene)], 'sakal', 'kafa', n=10)   # along the jaw
k.kure((0, -0.178, 1.54), 0.02, 'dudak', 'kafa', n=10, k=6, olcek=(1.4, 0.6, 0.55))
k.yol([(-0.088, -0.146, 1.527), (-0.052, -0.17, 1.553), (-0.017, -0.181, 1.567), (0.017, -0.181, 1.567), (0.052, -0.17, 1.553), (0.088, -0.146, 1.527)],
      [0.007, 0.015, 0.019, 0.019, 0.015, 0.007], 'sakal', 'kafa', n=8, ey=0.75)
k.kabuk(HC, 0.168, 0.163, 0.178, 15, 165, -45, 8, lambda lo, la: 0.013, 'sakal', 'kafa', n=14, k=5)    # hair at the back
# kettle helmet: crown, band with rivets, rolled brim
k.kure((0, 0, 1.715), 0.19, 'celik', 'kafa', n=24, k=8, olcek=(1, 1, 0.9), alt=0.0, ust=1.0)
k.halka((0, 0, 1.722), (0, 0, 1), 0.192, 0.012, 'celik_k', 'kafa', n=24, m=6, alt=1)
for i in range(10):
    a = 2 * math.pi * i / 10
    k.kure((math.cos(a) * 0.205, math.sin(a) * 0.205, 1.727), 0.008, 'celik_k', 'kafa', n=6, k=4, sub=0)
k.tup((0, 0, 1.705), (0, 0, 1.725), 0.3, 0.25, 'celik', 'kafa', n=40, alt=0)
k.halka((0, 0, 1.707), (0, 0, 1), 0.3, 0.013, 'celik_k', 'kafa', n=40, m=6, alt=1)
k.kure((0, 0, 1.887), 0.022, 'celik_k', 'kafa', n=8, k=5)

# ---------------- neck, trunk, tabard ----------------
k.tup((0, 0, 1.36), (0, 0, 1.5), 0.072, 0.068, 'ten', 'boyun', n=12)
k.tup((0, 0, 1.33), (0, 0, 1.43), 0.16, 0.105, 'zirh', 'gogus', n=16)                               # mail collar
k.tup((0, 0, 1.1), (0, 0, 1.37), 0.2, 0.235, 'zirh', govde, n=16, ex=1.15, ey=0.72)
k.tup((0, 0, 0.92), (0, 0, 1.12), 0.205, 0.2, 'zirh', govde, n=16, ex=1.12, ey=0.75)
for s in (1, -1):
    k.kure((s * 0.255, 0, 1.31), 0.105, 'zirh', 'gogus', n=12, k=8)
for a0, a1, bone in ((-150, -30, 'etek_on'), (30, 150, 'etek_arka')):
    k.yay(0.95, 1.355, 0.232, 0.262, a0, a1, 'mavi', govde, ex=1.14, ey=0.77, kalin=0.016, n=12, kat=6)
    k.yay(1.335, 1.37, 0.266, 0.266, a0 + 4, a1 - 4, 'sirma', 'gogus', ex=1.15, ey=0.76, kalin=0.02, n=12)           # neckline trim
    k.yay(0.48, 0.96, 0.256, 0.234, a0 + 3, a1 - 3, 'mavi', etek(bone), ex=1.12, ey=0.84, kalin=0.016, n=12, egim=0.05, kat=4)
    k.yay(0.47, 0.515, 0.262, 0.259, a0 + 3, a1 - 3, 'sirma', etek(bone), ex=1.12, ey=0.84, kalin=0.022, n=12, egim=0.05)  # hem trim
# belt, brass buckle, pouch
k.tup((0, 0, 0.93), (0, 0, 0.995), 0.235, 0.235, 'deri', 'kalca', n=28, ex=1.13, ey=0.83, alt=0)
k.halka((0, 0, 0.93), (0, 0, 1), 0.235, 0.006, 'deri_k', 'kalca', n=28, m=4)
k.kutu((0, -0.198, 0.962), (0.08, 0.016, 0.066), 'pirinc', 'kalca', alt=1)
k.kutu((0, -0.204, 0.962), (0.044, 0.01, 0.034), 'deri', 'kalca')
R15 = Matrix.Rotation(math.radians(-18), 3, 'Z')
k.kutu((0.16, -0.17, 0.875), (0.1, 0.06, 0.11), 'deri', 'kalca', don=R15, alt=1)
k.kutu((0.16, -0.176, 0.91), (0.106, 0.064, 0.045), 'deri_k', 'kalca', don=R15, alt=1)
k.kure(Vector((0.16, -0.176, 0.9)) + R15 @ Vector((0, -0.034, 0)), 0.01, 'pirinc', 'kalca', n=6, k=4)
k.tup((0, 0, 0.78), (0, 0, 0.95), 0.19, 0.2, 'pantolon', 'kalca', n=16, ex=1.1, ey=0.8)

# ---------------- legs ----------------
for s, ad in ((1, 'sol'), (-1, 'sag')):
    x = s * 0.12
    k.tup((x, 0, 0.93), (x, 0, 0.55), 0.1, 0.082, 'pantolon', 'uyluk_' + ad, n=12)
    k.kure((x, 0, 0.53), 0.082, 'pantolon', 'baldir_' + ad, n=10, k=6)
    k.tup((x, 0, 0.53), (x, 0, 0.36), 0.078, 0.07, 'pantolon', 'baldir_' + ad, n=12)
    k.tup((x, 0, 0.42), (x, 0, 0.09), 0.094, 0.088, 'deri_k', 'baldir_' + ad, n=14)
    k.tup((x, 0, 0.36), (x, 0, 0.445), 0.114, 0.109, 'deri', 'baldir_' + ad, n=14)                  # turned cuff
    k.kure((x, -0.065, 0.075), 0.1, 'deri_k', 'ayak_' + ad, n=14, k=8, olcek=(0.95, 1.75, 0.68), alt=-0.4)
    k.kutu((x, -0.068, 0.02), (0.185, 0.34, 0.03), 'taban', 'ayak_' + ad, alt=1)


# ---------------- arms and hands ----------------
def yumruk(ad, c, g, d):
    """a gloved fist closed round an axis g at c (a grip, a strap); d: the forearm's direction"""
    g = Vector(g).normalized(); q = (d - g * d.dot(g)).normalized(); p = g.cross(q)
    bone = 'el_' + ad
    k.kutu(c - q * 0.03 + p * 0.012, (0.09, 0.095, 0.075), 'deri', bone, don=eksenler(q, g, p), alt=1)  # back of the hand
    for i in range(4):                                                                                 # fingers closed round it
        o = c + g * (-0.033 + 0.022 * i)
        pts = [o + (q * math.cos(a) + p * math.sin(a)) * 0.034 for a in (math.radians(x) for x in (100, 40, -20, -80, -130))]
        k.yol(pts, [0.0165, 0.0165, 0.016, 0.0155, 0.015], 'deri', bone, n=8)
    tb = c - q * 0.02 + p * 0.035 - g * 0.05
    k.yol([tb, c + q * 0.01 + p * 0.042 - g * 0.04, c + q * 0.035 + p * 0.03 - g * 0.025], [0.019, 0.017, 0.015], 'deri', bone, n=8)  # thumb over the fingers
    k.tup(c - q * 0.1, c - q * 0.055, 0.058, 0.064, 'deri_k', bone, n=12)                              # glove cuff


for s, ad in ((1, 'sol'), (-1, 'sag')):
    p = P[ad]; d = p['d']
    k.tup(p['omuz'], p['dirsek'] - d * 0.05, 0.09, 0.074, 'zirh', 'kol_ust_' + ad, n=12)
    k.halka(p['dirsek'] - d * 0.05, d, 0.074, 0.008, 'celik_k', 'kol_ust_' + ad, n=12, m=4)
    k.tup(p['dirsek'] - d * 0.08, p['dirsek'] + d * 0.01, 0.07, 0.065, 'astar', 'kol_ust_' + ad, n=12)
    k.kure(p['dirsek'], 0.06, 'astar', 'kol_alt_' + ad, n=10, k=6)
    k.tup(p['dirsek'] + d * 0.04, p['bilek'], 0.072, 0.086, 'deri', 'kol_alt_' + ad, n=14)
    for f in (0.3, 0.75):                                                                              # bracer straps
        k.tup(p['dirsek'].lerp(p['bilek'], f - 0.035), p['dirsek'].lerp(p['bilek'], f + 0.035), 0.077 + 0.0135 * f, 0.078 + 0.0135 * f, 'deri_k', 'kol_alt_' + ad, n=14, alt=0)

# sword in the right fist: down and forward
pr = P['sag']; c = pr['bilek'] + pr['d'] * 0.07
w = Vector((-0.12, -0.85, -0.5)).normalized()
yumruk('sag', c, w, pr['d'])
q = (pr['d'] - w * pr['d'].dot(w)).normalized()
k.tup(c - w * 0.07, c + w * 0.075, 0.019, 0.019, 'deri_k', 'el_sag', n=8)
k.kure(c - w * 0.09, 0.028, 'pirinc', 'el_sag', n=10, k=6)
cg = c + w * 0.085
k.yol([cg - q * 0.11 + w * 0.012, cg - q * 0.05, cg, cg + q * 0.05, cg + q * 0.11 + w * 0.012], [0.012, 0.014, 0.016, 0.014, 0.012], 'celik_k', 'el_sag', n=6)
for sg in (-1, 1): k.kure(cg + q * 0.112 * sg + w * 0.014, 0.017, 'celik_k', 'el_sag', n=8, k=5)
k.tup(c + w * 0.095, c + w * 0.62, 0.034, 0.027, 'celik', 'el_sag', n=4, ey=0.2, yon=q, alt=0)
k.tup(c + w * 0.62, c + w * 0.71, 0.027, 0.002, 'celik', 'el_sag', n=4, ey=0.2, yon=q, alt=0)

# shield on the left arm: the fist holds its strap behind the boards
pl = P['sol']; n = Vector((1, -0.4, 0.05)).normalized()
c = pl['bilek'] + pl['d'] * 0.06
kol = n.cross(Vector((0, 0, 1))).normalized()       # the handle runs across the shield
yumruk('sol', c, kol, pl['d'])
sc = c + n * 0.09
k.tup(sc - n * 0.02, sc + n * 0.02, 0.28, 0.28, 'ahsap', 'kol_alt_sol', n=36, alt=0)
k.tup(sc + n * 0.019, sc + n * 0.024, 0.205, 0.205, 'mavi', 'kol_alt_sol', n=36, alt=0)
k.tup(sc + n * 0.023, sc + n * 0.028, 0.115, 0.115, 'ahsap', 'kol_alt_sol', n=30, alt=0)
k.halka(sc, n, 0.28, 0.022, 'celik_k', 'kol_alt_sol', n=36, m=8, alt=1)
k.halka(sc + n * 0.026, n, 0.205, 0.006, 'sirma', 'kol_alt_sol', n=36, m=4)
k.halka(sc + n * 0.028, n, 0.072, 0.012, 'celik_k', 'kol_alt_sol', n=20, m=6, alt=1)
k.kure(sc + n * 0.028, 0.064, 'celik', 'kol_alt_sol', n=16, k=6, alt=0.0, don=don_z(n))
u = n.cross(Vector((0, 0, 1))).normalized(); v = n.cross(u)
for t in range(10):
    a = 2 * math.pi * t / 10
    k.kure(sc + n * 0.024 + (u * math.cos(a) + v * math.sin(a)) * 0.245, 0.012, 'celik', 'kol_alt_sol', n=6, k=4)
# arm strap round the forearm, behind the shield
k.tup(pl['dirsek'].lerp(pl['bilek'], 0.45), pl['dirsek'].lerp(pl['bilek'], 0.58), 0.088, 0.09, 'deri_k', 'kol_alt_sol', n=14, alt=0)

# ---------------- actions (degrees about the armature's axes; see karakter.poz) ----------------
TABAN = {'kol_ust_sag': [('x', -8)], 'kol_alt_sag': [('x', -22)], 'kol_ust_sol': [('x', -6)], 'kol_alt_sol': [('x', -38)]}


def P2(*ds):
    out = {}
    for dd in ds:
        for kk, v in dd.items(): out.setdefault(kk, []).extend(v)
    return out


def bekle():
    a = P2(TABAN)
    b = P2(TABAN, {'bel': [('x', 1.5)], 'gogus': [('x', 2)], 'kafa': [('z', 5), ('x', -2)], 'kol_ust_sag': [('x', -3)], 'kol_ust_sol': [('x', 3)]})
    return [(1, a, None), (25, b, None), (49, a, None)]


def yuru():
    def kare(onde):
        arka = 'sag' if onde == 'sol' else 'sol'; sg = 1 if onde == 'sol' else -1
        return P2(TABAN, {'uyluk_' + onde: [('x', -28)], 'baldir_' + onde: [('x', 6)], 'ayak_' + onde: [('x', -8)],
                          'uyluk_' + arka: [('x', 22)], 'baldir_' + arka: [('x', 14)], 'ayak_' + arka: [('x', 12)],
                          'kol_ust_' + onde: [('x', 16)], 'kol_ust_' + arka: [('x', -16)],
                          'gogus': [('z', -6 * sg)], 'kalca': [('z', 5 * sg)], 'etek_on': [('x', -18)], 'etek_arka': [('x', 12)]})
    def gecis(salinan):
        duran = 'sag' if salinan == 'sol' else 'sol'
        return P2(TABAN, {'uyluk_' + salinan: [('x', -8)], 'baldir_' + salinan: [('x', 55)], 'ayak_' + salinan: [('x', 10)],
                          'uyluk_' + duran: [('x', 2)], 'bel': [('x', 3)], 'etek_on': [('x', -8)], 'etek_arka': [('x', 4)]})
    return [(1, kare('sol'), None), (7, gecis('sag'), (0, 0, 0.035)), (13, kare('sag'), None), (19, gecis('sol'), (0, 0, 0.035)), (25, kare('sol'), None)]


def saldir():
    hazir = P2(TABAN)
    kaldir = P2({'kol_ust_sag': [('x', -150), ('y', 15)], 'kol_alt_sag': [('x', -55)], 'gogus': [('z', -22)], 'bel': [('x', -8)],
                 'kol_ust_sol': [('x', -35)], 'kol_alt_sol': [('x', -40)], 'uyluk_sol': [('x', -12)], 'uyluk_sag': [('x', 10)]})
    vur = P2({'kol_ust_sag': [('x', -40)], 'kol_alt_sag': [('x', -8)], 'gogus': [('z', 22)], 'bel': [('x', 16)],
              'kol_ust_sol': [('x', -20), ('z', 10)], 'kol_alt_sol': [('x', -45)], 'uyluk_sag': [('x', -22)], 'baldir_sag': [('x', 18)],
              'etek_on': [('x', -16)], 'uyluk_sol': [('x', 14)], 'kafa': [('x', 8)]})
    return [(1, hazir, None), (9, kaldir, None), (12, P2(kaldir, {'kol_ust_sag': [('x', -8)]}), None), (15, vur, (0, -0.04, -0.02)),
            (19, vur, (0, -0.04, -0.02)), (27, hazir, None)]


def ol():
    sars = P2(TABAN, {'bel': [('x', -16)], 'gogus': [('x', -8)], 'kafa': [('x', -22)], 'kol_ust_sag': [('x', -40)], 'kol_ust_sol': [('x', -30)]})
    cok = P2(TABAN, {'uyluk_sol': [('x', -55)], 'uyluk_sag': [('x', -45)], 'baldir_sol': [('x', 85)], 'baldir_sag': [('x', 75)],
                     'bel': [('x', 18)], 'kafa': [('x', 15)], 'kol_ust_sag': [('x', 10)], 'kol_ust_sol': [('x', 10)], 'etek_on': [('x', -48)]})
    yat = P2({'kok': [('x', -84)], 'etek_on': [('x', -15)], 'uyluk_sol': [('x', -25)], 'uyluk_sag': [('x', -10)], 'baldir_sol': [('x', 35)],
              'baldir_sag': [('x', 15)], 'kafa': [('x', -15), ('z', 20)], 'kol_ust_sag': [('x', -70)], 'kol_ust_sol': [('x', -60)], 'kol_alt_sol': [('x', -20)]})
    return [(1, P2(TABAN), None), (7, sars, (0, 0.03, 0)), (17, cok, (0, 0.02, -0.26)), (30, yat, (0, 0.05, 0.08)),
            (34, P2(yat, {'kafa': [('x', 5)]}), (0, 0.05, 0.06)), (42, yat, (0, 0.05, 0.06))]


ANIM = [('bekle', bekle()), ('yuru', yuru()), ('saldir', saldir()), ('ol', ol())]


def kur(doku=True):
    govde_ob = k.nesne('piyade')
    if doku: pisir(govde_ob)
    arm = iskelet('piyade', kemik)
    bagla(govde_ob, arm)
    for a, kr in ANIM: eylem(arm, a, kr)
    return govde_ob, arm


if __name__ == '__main__':
    arg = argumanlar()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    govde_ob, arm = kur()
    print('UCGEN', sum(len(p.vertices) - 2 for p in govde_ob.data.polygons), 'KEMIK', len(arm.data.bones))
    if arg:
        disa_aktar(arm, govde_ob, os.path.abspath(arg[0]))
    if len(arg) > 1:
        from ortak import onizle
        klasor = os.path.abspath(arg[1]); sc = bpy.context.scene
        def kare(ad, kr_ad, kr, aci, boy=2.3, merkez=(0, 0, 0.95)):
            arm.animation_data.action = bpy.data.actions.get(kr_ad or 'bekle')
            sc.frame_set(kr)
            onizle(os.path.join(klasor, ad + '.png'), merkez=merkez, boy=boy, aci=aci, cozunurluk=(700, 820), renk='TEXTURE')
        kare('on', None, 1, (0, 8)); kare('yan', None, 1, (90, 8))
        kare('yuru1', 'yuru', 1, (-40, 15)); kare('yuru7', 'yuru', 7, (-40, 15))
        kare('saldir9', 'saldir', 9, (-40, 15)); kare('saldir15', 'saldir', 15, (-40, 15))
        kare('ol17', 'ol', 17, (-40, 15)); kare('yuz', None, 1, (-25, 5), boy=0.55, merkez=(0, -0.1, 1.62))
