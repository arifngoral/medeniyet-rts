# Piyade (infantry swordsman) in the card art's style: friendly bearded face, kettle helmet, mail shirt under a blue
# tabard (team colour), belt with pouch, leather bracers and gloves, boots, a short sword and a round shield.
# Rigged (17 bones) with four actions: bekle (idle), yuru (walk), saldir (attack), ol (death).
# blender -b --python tools/lm-blender/piyade.py -- <out.glb> [preview folder]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector, Matrix
from karakter import Karakter, iskelet, bagla, eylem, disa_aktar, poz
from ortak import argumanlar

TEN = (0.95, 0.73, 0.58); SAKAL = (0.45, 0.27, 0.15); GOZ = (0.09, 0.07, 0.06)
CELIK = (0.72, 0.74, 0.77); CELIK_K = (0.46, 0.48, 0.52); ZIRH = (0.56, 0.58, 0.61)
MAVI = (0.12, 0.36, 0.86)       # team colour
DERI = (0.50, 0.31, 0.17); DERI_K = (0.34, 0.20, 0.11); PANTOLON = (0.40, 0.45, 0.38); ALT = (0.38, 0.42, 0.36)
AHSAP = (0.56, 0.36, 0.20); AHSAP_K = (0.42, 0.26, 0.14)

k = Karakter()
Z = Vector((0, 0, 1))


def don_z(w):
    """a rotation taking +z to w"""
    return Vector((0, 0, 1)).rotation_difference(Vector(w).normalized()).to_matrix()


# ---------------- skeleton layout ----------------
OMUZ_Z, KALCA_Z = 1.33, 0.95
A = math.radians(33)                       # arms out from the body (A-pose)
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
for s, ad in ((1, 'sol'), (-1, 'sag')):          # (sol = the character's left = +x: it faces -y)
    d = kol_yon(s)
    o = Vector((s * 0.27, 0, OMUZ_Z)); e = o + d * L_UST; w = e + d * L_ALT; h = w + d * L_EL
    P[ad] = dict(d=d, omuz=o, dirsek=e, bilek=w, el=h)
    kemik += [('kol_ust_' + ad, o, e, 'gogus'), ('kol_alt_' + ad, e, w, 'kol_ust_' + ad), ('el_' + ad, w, h, 'kol_alt_' + ad)]
    x = s * 0.12
    kemik += [('uyluk_' + ad, (x, 0, KALCA_Z), (x, 0, 0.53), 'kalca'), ('baldir_' + ad, (x, 0, 0.53), (x, 0, 0.13), 'uyluk_' + ad),
              ('ayak_' + ad, (x, 0, 0.13), (x, -0.17, 0.04), 'baldir_' + ad)]

# ---------------- head ----------------
k.kure((0, 0, 1.61), 0.17, TEN, 'kafa', n=16, k=12, olcek=(1, 0.95, 1.05))
for s in (1, -1):
    k.kure((s * 0.165, 0.0, 1.6), 0.042, TEN, 'kafa', n=8, k=6, olcek=(0.5, 1, 1.25))
    k.kure((s * 0.062, -0.153, 1.645), 0.022, GOZ, 'kafa', n=8, k=6, olcek=(1, 0.7, 1.15))
    k.kutu((s * 0.066, -0.157, 1.678), (0.068, 0.024, 0.022), SAKAL, 'kafa', don=Matrix.Rotation(math.radians(-12 * s), 3, 'Y'))
    k.kure((s * 0.1, -0.13, 1.585), 0.04, (0.97, 0.62, 0.52), 'kafa', n=8, k=6, olcek=(1, 0.6, 0.8))     # rosy cheeks
k.kure((0, -0.168, 1.6), 0.044, TEN, 'kafa', n=10, k=8, olcek=(1, 1, 1.15))                       # nose
k.kure((0, -0.04, 1.525), 0.152, SAKAL, 'kafa', n=16, k=8, olcek=(1.02, 0.9, 0.8), alt=-1.0, ust=0.08)   # short beard round the jaw
k.tup((-0.075, -0.165, 1.565), (0.075, -0.165, 1.565), 0.024, 0.024, SAKAL, 'kafa', n=8, ex=1.0, ey=0.8)  # moustache
k.kure((0, 0.03, 1.6), 0.172, SAKAL, 'kafa', n=14, k=8, olcek=(1.02, 0.95, 0.95), alt=-0.55, ust=0.35)  # hair at the back
# kettle helmet: dome, ridge, brim, knob
k.kure((0, 0, 1.70), 0.19, CELIK, 'kafa', n=20, k=8, olcek=(1, 1, 0.92), alt=0.0, ust=1.0)
k.halka((0, 0, 1.705), (0, 0, 1), 0.19, 0.012, CELIK_K, 'kafa', n=20, m=5)                       # band round the crown
k.tup((0, 0, 1.69), (0, 0, 1.712), 0.3, 0.25, CELIK, 'kafa', n=28)
k.halka((0, 0, 1.692), (0, 0, 1), 0.297, 0.012, CELIK_K, 'kafa', n=28, m=5)
k.kure((0, 0, 1.872), 0.024, CELIK_K, 'kafa', n=8, k=5)

# ---------------- neck, body ----------------
k.tup((0, 0, 1.36), (0, 0, 1.5), 0.075, 0.07, TEN, 'boyun', n=10)
k.tup((0, 0, 1.33), (0, 0, 1.42), 0.15, 0.1, ZIRH, 'gogus', n=14)                                  # mail collar
k.tup((0, 0, 1.1), (0, 0, 1.36), 0.2, 0.235, ZIRH, 'gogus', n=14, ex=1.15, ey=0.72)                 # chest (mail)
k.tup((0, 0, 0.93), (0, 0, 1.12), 0.205, 0.2, ZIRH, 'bel', n=14, ex=1.12, ey=0.75)                  # belly (mail)
for s in (1, -1):
    k.kure((s * 0.255, 0, 1.31), 0.105, ZIRH, 'gogus', n=12, k=8)                                  # shoulders
# tabard: chest panels and the skirt to the knees (front and back: the legs show at the sides)
for a0, a1, etek in ((-148, -32, 'etek_on'), (32, 148, 'etek_arka')):
    k.yay(1.1, 1.37, 0.228, 0.256, a0, a1, MAVI, 'gogus', ex=1.15, ey=0.74, n=10)
    k.yay(0.97, 1.11, 0.226, 0.228, a0, a1, MAVI, 'bel', ex=1.13, ey=0.77, n=10)
    k.yay(0.48, 0.97, 0.252, 0.232, a0 + 3, a1 - 3, MAVI, etek, ex=1.12, ey=0.84, n=10, egim=0.05, kalin=0.016)
# belt, buckle, pouch
k.tup((0, 0, 0.93), (0, 0, 0.995), 0.215, 0.215, DERI, 'kalca', n=16, ex=1.13, ey=0.82)
k.kutu((0, -0.178, 0.962), (0.075, 0.02, 0.058), CELIK, 'kalca')
k.kutu((0.15, -0.15, 0.88), (0.1, 0.065, 0.1), DERI, 'kalca', don=Matrix.Rotation(math.radians(-15), 3, 'Z'))
k.kutu((0.15, -0.155, 0.915), (0.105, 0.07, 0.035), DERI_K, 'kalca', don=Matrix.Rotation(math.radians(-15), 3, 'Z'))
k.tup((0, 0, 0.8), (0, 0, 0.95), 0.19, 0.2, PANTOLON, 'kalca', n=14, ex=1.1, ey=0.8)                # seat of the trousers

# ---------------- legs ----------------
for s, ad in ((1, 'sol'), (-1, 'sag')):
    x = s * 0.12
    k.tup((x, 0, 0.93), (x, 0, 0.55), 0.1, 0.082, PANTOLON, 'uyluk_' + ad, n=12)
    k.kure((x, 0, 0.53), 0.082, PANTOLON, 'baldir_' + ad, n=10, k=6)
    k.tup((x, 0, 0.53), (x, 0, 0.36), 0.078, 0.07, PANTOLON, 'baldir_' + ad, n=12)
    k.tup((x, 0, 0.41), (x, 0, 0.08), 0.095, 0.088, DERI_K, 'baldir_' + ad, n=12)                  # boot shaft
    k.tup((x, 0, 0.36), (x, 0, 0.43), 0.112, 0.11, DERI, 'baldir_' + ad, n=12)                     # turned-down cuff
    k.kure((x, -0.065, 0.065), 0.1, DERI_K, 'ayak_' + ad, n=12, k=8, olcek=(0.95, 1.75, 0.62), alt=-0.45)  # foot
    k.kutu((x, -0.065, 0.012), (0.18, 0.33, 0.025), (0.22, 0.14, 0.08), 'ayak_' + ad)            # sole

# ---------------- arms ----------------
for s, ad in ((1, 'sol'), (-1, 'sag')):
    p = P[ad]; d = p['d']
    k.tup(p['omuz'], p['dirsek'], 0.088, 0.072, ZIRH, 'kol_ust_' + ad, n=12)                     # mail sleeve
    k.tup(p['omuz'] + d * 0.17, p['dirsek'] + d * 0.01, 0.075, 0.065, ALT, 'kol_ust_' + ad, n=12)  # undertunic
    k.kure(p['dirsek'], 0.068, ALT, 'kol_alt_' + ad, n=10, k=6)
    k.tup(p['dirsek'] + d * 0.04, p['bilek'], 0.072, 0.088, DERI, 'kol_alt_' + ad, n=12)          # bracer (flared)
    k.halka(p['bilek'] - d * 0.01, d, 0.088, 0.012, DERI_K, 'kol_alt_' + ad, n=12, m=4)
    c = p['bilek'] + d * 0.075
    k.kure(c, 0.078, DERI, 'el_' + ad, n=12, k=8, olcek=(1.0, 0.9, 1.15), don=don_z(d))           # glove
    k.kure(c + Vector((-s * 0.05, -0.05, 0.02)), 0.03, DERI, 'el_' + ad, n=8, k=5)               # thumb
    P[ad]['avuc'] = c

# ---------------- sword (right hand) ----------------
c = P['sag']['avuc']
w = (P['sag']['d'] * 0.55 + Vector((0, -0.45, 0)) + Vector((0, 0, -0.35))).normalized()   # down and forward
R = don_z(w)
k.tup(c - w * 0.08, c + w * 0.07, 0.022, 0.022, DERI_K, 'el_sag', n=8)                     # grip
k.kure(c - w * 0.095, 0.032, CELIK_K, 'el_sag', n=8, k=6)                                  # pommel
k.kutu(c + w * 0.085, (0.2, 0.035, 0.03), CELIK_K, 'el_sag', don=R)                         # crossguard
k.kutu(c + w * 0.37, (0.065, 0.016, 0.54), CELIK, 'el_sag', don=R)                          # blade
k.kutu(c + w * 0.37, (0.012, 0.018, 0.5), CELIK_K, 'el_sag', don=R)                         # fuller
k.tup(c + w * 0.64, c + w * 0.72, 0.034, 0.002, CELIK, 'el_sag', n=4, ex=1.0, ey=0.24, yon=R @ Vector((1, 0, 0)))  # tip

# ---------------- shield (left forearm) ----------------
p = P['sol']
n = Vector((1, -0.4, 0.05)).normalized()
sc = p['dirsek'].lerp(p['bilek'], 0.55) + n * 0.08
k.tup(sc - n * 0.022, sc + n * 0.022, 0.27, 0.27, AHSAP, 'kol_alt_sol', n=24)
k.tup(sc + n * 0.021, sc + n * 0.027, 0.2, 0.2, MAVI, 'kol_alt_sol', n=24)
k.tup(sc + n * 0.026, sc + n * 0.031, 0.115, 0.115, AHSAP_K, 'kol_alt_sol', n=20)
k.halka(sc, n, 0.268, 0.02, CELIK_K, 'kol_alt_sol', n=24, m=6)
k.kure(sc + n * 0.028, 0.06, CELIK, 'kol_alt_sol', n=12, k=5, alt=0.0, don=don_z(n))       # boss
for t in range(6):                                                                         # rivets on the rim
    a = 2 * math.pi * t / 6
    u = n.cross(Vector((0, 0, 1))).normalized(); v = n.cross(u)
    k.kure(sc + n * 0.025 + (u * math.cos(a) + v * math.sin(a)) * 0.235, 0.014, CELIK_K, 'kol_alt_sol', n=6, k=4)

# ---------------- poses (degrees about the armature's axes; see karakter.poz) ----------------
TABAN = {'kol_ust_sag': [('x', -8)], 'kol_alt_sag': [('x', -22)], 'kol_ust_sol': [('x', -6)], 'kol_alt_sol': [('x', -38)]}


def P2(*ds):
    out = {}
    for d in ds:
        for kk, v in d.items(): out.setdefault(kk, []).extend(v)
    return out


def bekle():
    a = P2(TABAN)
    b = P2(TABAN, {'bel': [('x', 1.5)], 'gogus': [('x', 2)], 'kafa': [('z', 5), ('x', -2)],
                   'kol_ust_sag': [('x', -3)], 'kol_ust_sol': [('x', 3)]})
    return [(1, a, None), (25, b, None), (49, a, None)]


def yuru():
    def kare(onde):   # onde: the leg in front ('sol' or 'sag')
        arka = 'sag' if onde == 'sol' else 'sol'
        sg = 1 if onde == 'sol' else -1
        return P2(TABAN, {'uyluk_' + onde: [('x', -28)], 'baldir_' + onde: [('x', 6)], 'ayak_' + onde: [('x', -8)],
                          'uyluk_' + arka: [('x', 22)], 'baldir_' + arka: [('x', 14)], 'ayak_' + arka: [('x', 12)],
                          'kol_ust_' + onde: [('x', 16)], 'kol_ust_' + arka: [('x', -16)],
                          'gogus': [('z', -6 * sg)], 'kalca': [('z', 5 * sg)], 'etek_on': [('x', -18)], 'etek_arka': [('x', 12)]})
    def gecis(salinan):   # the swinging leg passes under the body, knee bent
        duran = 'sag' if salinan == 'sol' else 'sol'
        return P2(TABAN, {'uyluk_' + salinan: [('x', -8)], 'baldir_' + salinan: [('x', 55)], 'ayak_' + salinan: [('x', 10)],
                          'uyluk_' + duran: [('x', 2)], 'bel': [('x', 3)], 'etek_on': [('x', -8)], 'etek_arka': [('x', 4)]})
    return [(1, kare('sol'), None), (7, gecis('sag'), (0, 0, 0.035)), (13, kare('sag'), None),
            (19, gecis('sol'), (0, 0, 0.035)), (25, kare('sol'), None)]


def saldir():
    hazir = P2(TABAN)
    kaldir = P2({'kol_ust_sag': [('x', -150), ('y', 15)], 'kol_alt_sag': [('x', -55)], 'gogus': [('z', -22)], 'bel': [('x', -8)],
                 'kol_ust_sol': [('x', -35)], 'kol_alt_sol': [('x', -40)], 'uyluk_sol': [('x', -12)], 'uyluk_sag': [('x', 10)]})
    vur = P2({'kol_ust_sag': [('x', -40)], 'kol_alt_sag': [('x', -8)], 'gogus': [('z', 22)], 'bel': [('x', 16)],
              'kol_ust_sol': [('x', -20), ('z', 10)], 'kol_alt_sol': [('x', -45)], 'uyluk_sag': [('x', -22)], 'baldir_sag': [('x', 18)], 'etek_on': [('x', -16)],
              'uyluk_sol': [('x', 14)], 'kafa': [('x', 8)]})
    return [(1, hazir, None), (9, kaldir, None), (12, P2(kaldir, {'kol_ust_sag': [('x', -8)]}), None), (15, vur, (0, -0.04, -0.02)),
            (19, vur, (0, -0.04, -0.02)), (27, hazir, None)]


def ol():
    sars = P2(TABAN, {'bel': [('x', -16)], 'gogus': [('x', -8)], 'kafa': [('x', -22)], 'kol_ust_sag': [('x', -40)], 'kol_ust_sol': [('x', -30)]})
    cok = P2(TABAN, {'uyluk_sol': [('x', -55)], 'uyluk_sag': [('x', -45)], 'baldir_sol': [('x', 85)], 'baldir_sag': [('x', 75)],
                     'bel': [('x', 18)], 'kafa': [('x', 15)], 'kol_ust_sag': [('x', 10)], 'kol_ust_sol': [('x', 10)], 'etek_on': [('x', -48)]})
    yat = P2({'kok': [('x', -84)], 'etek_on': [('x', -15)], 'uyluk_sol': [('x', -25)], 'uyluk_sag': [('x', -10)], 'baldir_sol': [('x', 35)], 'baldir_sag': [('x', 15)],
              'kafa': [('x', -15), ('z', 20)], 'kol_ust_sag': [('x', -70)], 'kol_ust_sol': [('x', -60)], 'kol_alt_sol': [('x', -20)]})
    return [(1, P2(TABAN), None), (7, sars, (0, 0.03, 0)), (17, cok, (0, 0.02, -0.26)), (30, yat, (0, 0.05, 0.08)),
            (34, P2(yat, {'kafa': [('x', 5)]}), (0, 0.05, 0.06)), (42, yat, (0, 0.05, 0.06))]


ANIM = [('bekle', bekle()), ('yuru', yuru()), ('saldir', saldir()), ('ol', ol())]

if __name__ == '__main__':
    arg = argumanlar()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    govde = k.nesne('piyade')
    arm = iskelet('piyade', kemik)
    bagla(govde, arm)
    for ad, kr in ANIM:
        eylem(arm, ad, kr)
    print('UCGEN', sum(len(p.vertices) - 2 for p in govde.data.polygons), 'KEMIK', len(arm.data.bones))
    if arg:
        disa_aktar(arm, govde, os.path.abspath(arg[0]))
    if len(arg) > 1:
        # preview frames (workbench, vertex colours): front, side and a frame of each action
        from ortak import onizle
        klasor = os.path.abspath(arg[1])
        sc = bpy.context.scene
        def kare(ad, kr_ad, kr, aci):
            act = bpy.data.actions.get(kr_ad) if kr_ad else None
            arm.animation_data.action = act
            sc.frame_set(kr)
            onizle(os.path.join(klasor, ad + '.png'), merkez=(0, 0, 0.95), boy=2.3, aci=aci, cozunurluk=(700, 820))
        kare('on', None, 1, (0, 8))
        kare('yan', None, 1, (90, 8))
        kare('yuru7', 'yuru', 7, (-40, 15))
        kare('yuru1', 'yuru', 1, (-40, 15))
        kare('saldir9', 'saldir', 9, (-40, 15))
        kare('saldir15', 'saldir', 15, (-40, 15))
        kare('ol17', 'ol', 17, (-40, 15))
        kare('ol42', 'ol', 42, (-60, 25))
