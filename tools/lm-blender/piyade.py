# Piyade (infantry swordsman) on a real human body (insan.py: Blender's Human Base Meshes, stylized male, CC0),
# after the card-style turnaround: kettle helmet, a short beard and moustache, mail shirt with sleeves to the elbow,
# undertunic, flared leather gauntlets, a narrow blue tabard (team colour) front and back with gold trim, belt with a
# brass buckle and a pouch, trousers, boots with turned cuffs, a sword in the right fist, a plank shield on the left.
# Skin and clothes bend together (automatic weights carried over to the clothes); textures baked (karakter.pisir).
# blender -b --python tools/lm-blender/piyade.py -- <out.glb> [preview folder]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix
from karakter import Karakter, iskelet, bagla, eylem, disa_aktar, pisir, yumusak, malzeme
from insan import govde_yukle, deform, bolge_olcek, yumruk, it, bolge_kopya, agirlik_aktar, sabit_agirlik, islev_agirlik, birlestir, oto_agirlik
from animasyon import ANIM
from ortak import argumanlar

# ---------------- the body, reshaped ----------------
GENIS = 1.12             # trunk and limbs a little stockier
BAS = 1.2                # bigger head
EL = 1.0                 # hands as they are (the gloves add a little)
J = {}                   # joints (after the reshaping)
for s, ad in ((1, 'sol'), (-1, 'sag')):
    J['omuz_' + ad] = Vector((s * 0.19 * GENIS, 0.015 * GENIS, 1.39))
    J['dirsek_' + ad] = Vector((s * 0.335 * GENIS, 0.035 * GENIS, 1.12))
    J['bilek_' + ad] = Vector((s * 0.40 * GENIS, 0.0, 0.93))
    J['uc_' + ad] = J['bilek_' + ad] + (Vector((s * 0.397 * GENIS, -0.02, 0.72)) - J['bilek_' + ad]) * EL
    J['kalca_' + ad] = Vector((s * 0.095 * GENIS, -0.01, 0.88))
    J['diz_' + ad] = Vector((s * 0.088 * GENIS, -0.012, 0.50))
    J['topuk_' + ad] = Vector((s * 0.098 * GENIS, 0.014, 0.10))
    J['parmak_' + ad] = Vector((s * 0.13 * GENIS, -0.17, 0.03))
S0, R0 = 0.1, 0.037       # the fist: where the fingers start to bend (from the wrist), bend radius


def kur_govde():
    govde, gozler = govde_yukle()
    hep = [govde] + gozler
    deform(hep, bolge_olcek((0, -0.02, 1.47), BAS, lambda c: yumusak(1.43, 1.53, c.z)))
    deform(hep, bolge_olcek((0, 0, 0), (GENIS, GENIS, 1), lambda c: 1 - yumusak(1.42, 1.5, c.z)))
    # the face (landmarks measured on the reshaped head: eyes (+-0.05, -0.112, 1.667) r 0.046, nose tip (0, -0.207, 1.613),
    # mouth line z 1.525, chin 1.465): a bigger round nose, a smile, full cheeks, eyes smiling under the lids
    on = lambda c: c.y < -0.11
    deform([govde], bolge_olcek((0, -0.172, 1.613), 1.12, lambda c: (1 - yumusak(0.03, 0.06, (c - Vector((0, -0.19, 1.613))).length)) if c.y < -0.13 else 0))
    for s in (1, -1):
        deform([govde], it((s * 0.042, -0.165, 1.527), (s * 0.002, 0.003, 0.008), 0.012, 0.032, on))      # corners of the mouth up
        deform([govde], it((s * 0.068, -0.158, 1.585), (0, -0.006, 0.006), 0.01, 0.036, on))              # cheeks
        deform([govde], it((s * 0.05, -0.15, 1.627), (0, -0.003, 0.012), 0.008, 0.026, on))               # lower lid up
        deform([govde], it((s * 0.05, -0.152, 1.71), (0, -0.002, -0.011), 0.008, 0.026, on))                   # upper lid down
    for s, ad in ((1, 'sol'), (-1, 'sag')):
        B = J['bilek_' + ad]
        deform([govde], bolge_olcek(B, EL, lambda c, s=s: yumusak(0.95, 0.9, c.z) * (1 if c.x * s > 0.37 else 0)))
        deform([govde], yumruk(B, J['uc_' + ad], (-s, 0, 0), S0, R0, lambda c, s=s: c.x * s > 0.34 and c.z < 0.93))
    return govde, gozler


def avuc(ad):
    """the fist's grip: its centre and axis"""
    s = 1 if ad == 'sol' else -1
    B = J['bilek_' + ad]; a = (J['uc_' + ad] - B).normalized(); b = Vector((-s, 0, 0)); b = (b - a * a.dot(b)).normalized()
    return B + a * (S0 + 0.012) + b * R0 * 0.95, a.cross(b).normalized()


# ---------------- regions of the body (for the clothes) ----------------
def kol_t(c, ad):
    """0 at the shoulder, 1 at the wrist (beyond: the hand); None off the arm"""
    s = 1 if ad == 'sol' else -1
    if c.x * s < 0.2 or c.z > 1.46: return None
    A, W = J['omuz_' + ad], J['bilek_' + ad]
    return (c - A).dot(W - A) / (W - A).length_squared


def kol(c):
    for ad in ('sol', 'sag'):
        t = kol_t(c, ad)
        if t is not None: return t
    return None


def gomlek(c, n):          # mail shirt: the trunk and the arms to above the elbow
    t = kol(c)
    if t is not None: return t < 0.55
    return 0.84 < c.z < 1.445 and abs(c.x) < 0.24


def astar(c, n):           # undertunic sleeve between the mail and the gauntlet
    t = kol(c); return t is not None and 0.5 < t < 0.7


def eldiven(c, n):         # gauntlet and glove
    t = kol(c); return t is not None and t > 0.64


def pantolon(c, n):
    return 0.3 < c.z < 0.96 and abs(c.x) < 0.27 and kol(c) is None


def cizme(c, n):
    return c.z < 0.42 and abs(c.x) < 0.27


def cizme_agiz(c, n):
    return 0.31 < c.z < 0.43 and abs(c.x) < 0.27


def tunik(c, n):           # the narrow tabard over the chest and back, open at the sides
    return 0.9 < c.z < 1.445 and abs(c.x) < 0.165 and not (abs(c.x) < 0.085 and c.z > 1.40 and c.y < 0.04)


def ortulu(c, n):          # skin hidden under the clothes (removed)
    return (gomlek(c, n) and c.z < 1.42) or pantolon(c, n) or cizme(c, n) or (eldiven(c, n)) or astar(c, n)


# ---------------- build ----------------
def kur(doku=True):
    govde, gozler = kur_govde()
    w = np.array([v.co[:] for v in govde.data.vertices if abs(v.co.z - 0.93) < 0.02 and abs(v.co.x) < 0.26])
    hco = np.array([v.co[:] for v in govde.data.vertices if v.co.z > 1.5])
    giysi = []
    giysi.append(bolge_kopya(govde, 'gomlek', 'zirh', gomlek, lambda c: 0.016, 0.008, duzle=4))
    giysi.append(bolge_kopya(govde, 'astar', 'astar', astar, lambda c: 0.009, 0.004))
    def eld_ofset(c):
        t = kol(c) or 1
        return 0.004 if t > 1.0 else 0.016 + 0.026 * yumusak(0.76, 0.66, t)          # the gauntlet flares at its cuff
    giysi.append(bolge_kopya(govde, 'eldiven', 'deri', eldiven, eld_ofset, 0.005))
    giysi.append(bolge_kopya(govde, 'pantolon', 'pantolon', pantolon, lambda c: 0.01, 0.005))
    giysi.append(bolge_kopya(govde, 'cizme_agiz', 'deri', cizme_agiz, lambda c: 0.04, 0.006, duzle=3))
    giysi.append(bolge_kopya(govde, 'tunik', 'mavi', tunik, lambda c: 0.042, 0.008, duzle=8, kenar=16))
    # ---- the head: measure the face, add beard, moustache, brows, hair ----
    burun = hco[hco[:, 1].argmin()]                      # the nose tip (frontmost point)
    tepe = hco[:, 2].max()
    gm = [Vector(np.array([v.co[:] for v in g.data.vertices]).mean(0)) for g in gozler]
    gr = [np.ptp(np.array([v.co[:] for v in g.data.vertices])[:, 0]) / 2 for g in gozler]
    zb = burun[2]
    def sakal(c, n):
        ax = abs(c.x)
        if c.z < 1.455 or c.z > 1.66 or c.y > 0.02: return False
        if ax > 0.132 and c.y > -0.035: return False                                  # the ears
        if c.z > 1.556 + 0.55 * max(0.0, ax - 0.03): return False                     # up the cheeks (the lips under it)
        if c.z < 1.49 and c.y > -0.06: return False                                   # stops at the neck
        return True
    def sakal_kal(c):
        ust = 1.556 + 0.55 * max(0.0, abs(c.x) - 0.03)
        kenar = yumusak(0.0, 0.03, ust - c.z)
        return (0.002 + 0.013 * kenar) + 0.022 * yumusak(1.535, 1.47, c.z) * (1 - 0.4 * min(1.0, abs(c.x) / 0.1))
    giysi.append(bolge_kopya(govde, 'sakal', 'sakal', sakal, sakal_kal, 0.003, kenar=8))
    def sac(c, n):
        return 1.5 < c.z < 1.745 and c.y > 0.035 and abs(c.x) < 0.175 and kol(c) is None
    giysi.append(bolge_kopya(govde, 'sac', 'sakal', sac, lambda c: 0.012, 0.006))
    # weights while the whole skin is there (the clothes take theirs from the skin right under them)
    arm = iskelet('piyade', kemikler())
    oto_agirlik(govde, arm, haric=('etek_on', 'etek_arka'))
    agirlik_aktar(govde, giysi)
    # then the skin hidden under the clothes goes (lighter, and nothing pokes through)
    bm = bmesh.new(); bm.from_mesh(govde.data); bm.normal_update()
    dl = bm.verts.layers.deform.verify()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if all(ortulu(v.co, v.normal) for v in f.verts)], context='FACES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(govde.data); bm.free()
    govde.data.materials.append(malzeme('ten'))
    # eyes: white with a dark iris at the front
    for g, m, r in zip(gozler, gm, gr):
        g.data.materials.append(malzeme('goz_ak')); g.data.materials.append(malzeme('goz'))
        g.data.materials.append(malzeme('iris'))
        for p in g.data.polygons:      # front: pupil, a brown iris round it, white elsewhere
            on = p.center.y < m.y - 0.3 * r
            rr = math.hypot(p.center.x - m.x, p.center.z - m.z)
            p.material_index = (1 if rr < 0.27 * r else 2 if rr < 0.6 * r else 0) if on else 0
    # ---- parts made of primitives: moustache, brows, helmet, belt, pouch, sword, shield, skirt flaps ----
    k = Karakter()
    xn, yn = burun[0], burun[1]
    for s in (1, -1):
        k.yol([(s * 0.014, -0.181, 1.716), (s * 0.05, -0.186, 1.728), (s * 0.09, -0.166, 1.72)], [0.013, 0.016, 0.009], 'sakal', 'kafa', n=8, ey=0.75)   # brows (standing out of the brow ridge)
    bp = [(-0.088, -0.155, 1.556), (-0.07, -0.18, 1.543), (-0.046, -0.199, 1.545), (-0.022, -0.211, 1.552), (0, -0.214, 1.556),
          (0.022, -0.211, 1.552), (0.046, -0.199, 1.545), (0.07, -0.18, 1.543), (0.088, -0.155, 1.556)]
    k.yol(bp, [0.008, 0.015, 0.02, 0.022, 0.022, 0.022, 0.02, 0.015, 0.008], 'sakal', 'kafa', n=12, ey=0.8)
    for m, r in zip(gm, gr):
        s = 1 if m.x > 0 else -1
        k.kure(m + Vector((-s * 0.12 * r, -0.985 * r, 0.22 * r)), 0.0055, 'goz_ak', 'kafa', n=8, k=5, sub=0)   # catchlight
    # kettle helmet: crown over the head, a ridge, a narrow brim
    # kettle hat: the crown hugs the skull (measured: brow level z 1.73, centre y -0.021, half widths 0.161 / 0.153, top 1.864),
    # a ridge front to back, a band with rivets, a brim sloping down all round with a rolled edge
    HY, HZ, CR, CRY, CT = -0.021, 1.794, 0.166, 0.16, tepe + 0.06
    k.kure((0, HY, HZ - 0.004), CR, 'celik', 'kafa', n=36, k=12, olcek=(1, CRY / CR, (CT - HZ) / CR), alt=0.0, ust=1.0)
    k.yol([(0, HY + CRY * math.cos(a), HZ + (CT - HZ) * math.sin(a) + 0.004) for a in [math.radians(x) for x in range(12, 170, 12)]],
          0.012, 'celik_k', 'kafa', n=8)
    k.halka((0, HY, HZ + 0.008), (0, 0, 1), CR + 0.003, 0.01, 'celik_k', 'kafa', n=36, m=6, alt=1)
    for i in range(12):
        a = 2 * math.pi * i / 12
        k.kure((math.cos(a) * (CR + 0.012), HY + math.sin(a) * (CRY + 0.012), HZ + 0.008), 0.0065, 'celik_k', 'kafa', n=6, k=4, sub=0)
    k.siperlik((0, HY, 0), CR - 0.004, HZ, CR + 0.058, HZ - 0.04, 0.008, 'celik', 'kafa', n=48, ey=CRY / CR, alt=1)
    k.halka((0, HY, HZ - 0.044), (0, 0, 1), CR + 0.058, 0.009, 'celik_k', 'kafa', n=48, m=6, alt=1)
    k.tup((0, HY, HZ - 0.045), (0, HY, HZ + 0.01), CR - 0.012, CR - 0.01, 'deri_k', 'kafa', n=36, ey=CRY / CR, alt=0)   # leather liner inside the brim
    # belt round the waist (measured), brass buckle, pouch
    bx = np.abs(w[:, 0]).max(); by0, by1 = w[:, 1].min(), w[:, 1].max(); byc = (by0 + by1) / 2; bry = (by1 - by0) / 2
    k.tup((0, byc, 0.9), (0, byc, 0.965), bx + 0.05, bx + 0.05, 'deri', 'kalca', n=32, ey=(bry + 0.05) / (bx + 0.05), alt=1)
    k.kutu((0, by0 - 0.05, 0.932), (0.08, 0.018, 0.064), 'pirinc', 'kalca', alt=1)
    k.kutu((0, by0 - 0.057, 0.932), (0.044, 0.01, 0.034), 'deri_k', 'kalca')
    R = Matrix.Rotation(math.radians(-25), 3, 'Z')
    k.kutu((bx * 0.75, by0 - 0.02, 0.855), (0.11, 0.065, 0.11), 'deri', 'kalca', don=R, alt=1)
    k.kutu((bx * 0.75, by0 - 0.025, 0.89), (0.116, 0.07, 0.045), 'deri_k', 'kalca', don=R, alt=1)
    # skirt flaps of the tabard (front and back, to above the knee) with a gold hem
    def etek(bone):
        return lambda p: {'kalca': yumusak(0.78, 0.92, p.z), bone: 1 - yumusak(0.78, 0.92, p.z)}
    for a0, a1, bone, yy in ((-113, -67, 'etek_on', by0), (67, 113, 'etek_arka', by1)):
        ey = abs(yy - byc + (-0.035 if yy < byc else 0.035)) / 0.4
        k.yay(0.52, 0.95, 0.41, 0.4, a0, a1, 'mavi', etek(bone), ex=1.0, ey=ey, merkez=(0, byc), kalin=0.014, n=12, egim=0.03, kat=4)
        k.yay(0.505, 0.545, 0.418, 0.417, a0, a1, 'sirma', etek(bone), ex=1.0, ey=ey * 1.02, merkez=(0, byc), kalin=0.02, n=12, egim=0.03)
    # boots: lofted over the measured foot (heel y 0.073 to toes -0.218, widest 0.15 at the ball, instep 0.195 high at the
    # ankle), a sole under them; the heel follows the shin, the rest the foot
    AYAK = [(0.098, 0.112, 0.056, 0.022, 0.15), (0.055, 0.116, 0.072, 0.022, 0.205), (0.005, 0.124, 0.079, 0.022, 0.19),
            (-0.05, 0.136, 0.083, 0.022, 0.135), (-0.11, 0.146, 0.082, 0.022, 0.1), (-0.17, 0.146, 0.074, 0.022, 0.08),
            (-0.215, 0.138, 0.058, 0.022, 0.064), (-0.245, 0.13, 0.032, 0.026, 0.048)]
    for s, ad in ((1, 'sol'), (-1, 'sag')):
        ag = lambda p, ad=ad: {'baldir_' + ad: yumusak(0.0, 0.06, p.y), 'ayak_' + ad: 1 - yumusak(0.0, 0.06, p.y)}
        k.bot([(y, s * cx, w, z0, z1) for y, cx, w, z0, z1 in AYAK], 'deri_k', ag, n=18)
        k.tup((s * 0.114, 0.03, 0.1), (s * 0.112, 0.022, 0.4), 0.078, 0.074, 'deri_k', 'baldir_' + ad, n=28, ey=1.08, kapak=True, alt=0)   # the shaft
        k.bot([(y, s * cx, w + 0.008, 0.0, 0.026 if y > 0.0 else 0.022) for y, cx, w, z0, z1 in AYAK[:-1]] + [(-0.252, s * 0.13, 0.03, 0.0, 0.02)],
              'taban', ag, n=18, duz=0.002)
    # sword in the right fist, pointing forward and down
    c, g = avuc('sag')
    wv = (g + Vector((0, 0, -0.45))).normalized()
    q = Vector((0, 0, 1)) - wv * wv.z; q.normalize()      # the blade's flat faces sideways: broad from the front
    k.tup(c - wv * 0.085, c + wv * 0.09, 0.02, 0.02, 'deri_k', 'el_sag', n=8)
    k.kure(c - wv * 0.105, 0.03, 'pirinc', 'el_sag', n=10, k=6)
    cg = c + wv * 0.1
    k.yol([cg - q * 0.12 + wv * 0.015, cg - q * 0.05, cg, cg + q * 0.05, cg + q * 0.12 + wv * 0.015], [0.013, 0.015, 0.017, 0.015, 0.013], 'celik_k', 'el_sag', n=6)
    k.tup(c + wv * 0.112, c + wv * 0.8, 0.058, 0.048, 'celik', 'el_sag', n=4, ey=0.18, yon=q, alt=0)
    k.tup(c + wv * 0.8, c + wv * 0.92, 0.048, 0.002, 'celik', 'el_sag', n=4, ey=0.18, yon=q, alt=0)
    # shield: the left fist holds its handle behind the boards
    c, g = avuc('sol')
    n = Vector((1, -0.3, 0.05)).normalized()
    sc = c + n * 0.085
    k.tup(sc - n * 0.02, sc + n * 0.02, 0.29, 0.29, 'ahsap', 'kol_alt_sol', n=40, alt=0)
    k.tup(sc + n * 0.019, sc + n * 0.024, 0.215, 0.215, 'mavi', 'kol_alt_sol', n=40, alt=0)
    k.tup(sc + n * 0.023, sc + n * 0.028, 0.13, 0.13, 'ahsap', 'kol_alt_sol', n=32, alt=0)
    k.halka(sc, n, 0.29, 0.022, 'celik_k', 'kol_alt_sol', n=40, m=8, alt=1)
    k.halka(sc + n * 0.028, n, 0.075, 0.012, 'celik_k', 'kol_alt_sol', n=20, m=6, alt=1)
    k.kure(sc + n * 0.028, 0.066, 'celik', 'kol_alt_sol', n=16, k=6, alt=0.0, don=Vector((0, 0, 1)).rotation_difference(n).to_matrix())
    u = n.cross(Vector((0, 0, 1))).normalized(); v = n.cross(u)
    for t in range(10):
        a = 2 * math.pi * t / 10
        k.kure(sc + n * 0.024 + (u * math.cos(a) + v * math.sin(a)) * 0.255, 0.012, 'celik', 'kol_alt_sol', n=6, k=4)
    k.tup(c - g * 0.06, c + g * 0.06, 0.018, 0.018, 'ahsap', 'kol_alt_sol', n=8)            # the handle in the fist
    parcalar = k.nesne('parcalar')
    # ---- skeleton, weights ----
    for g in gozler: sabit_agirlik(g, 'kafa')
    hepsi = birlestir([govde] + giysi + gozler + [parcalar], 'piyade')
    if doku: pisir(hepsi)
    bagla(hepsi, arm)
    for a, kr in ANIM: eylem(arm, a, kr)
    return hepsi, arm


def kemikler():
    L = [('kok', (0, 0, 0), (0, 0, 0.25), None),
         ('kalca', (0, 0, 0.88), (0, 0, 1.02), 'kok'),
         ('bel', (0, 0, 1.02), (0, 0, 1.18), 'kalca'),
         ('gogus', (0, 0, 1.18), (0, 0, 1.40), 'bel'),
         ('boyun', (0, 0, 1.42), (0, 0, 1.52), 'gogus'),
         ('kafa', (0, 0, 1.52), (0, 0, 1.9), 'boyun'),
         ('etek_on', (0, -0.15, 0.93), (0, -0.17, 0.5), 'kalca'), ('etek_arka', (0, 0.14, 0.93), (0, 0.16, 0.5), 'kalca')]
    for ad in ('sol', 'sag'):
        L += [('kol_ust_' + ad, J['omuz_' + ad], J['dirsek_' + ad], 'gogus'),
              ('kol_alt_' + ad, J['dirsek_' + ad], J['bilek_' + ad], 'kol_ust_' + ad),
              ('el_' + ad, J['bilek_' + ad], J['bilek_' + ad] + (J['uc_' + ad] - J['bilek_' + ad]) * 0.6, 'kol_alt_' + ad),
              ('uyluk_' + ad, J['kalca_' + ad], J['diz_' + ad], 'kalca'),
              ('baldir_' + ad, J['diz_' + ad], J['topuk_' + ad], 'uyluk_' + ad),
              ('ayak_' + ad, J['topuk_' + ad], J['parmak_' + ad], 'baldir_' + ad)]
    return L


if __name__ == '__main__':
    arg = argumanlar()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ob, arm = kur()
    print('UCGEN', sum(len(p.vertices) - 2 for p in ob.data.polygons), 'KEMIK', len(arm.data.bones))
    if arg:
        disa_aktar(arm, ob, os.path.abspath(arg[0]))
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
        kare('ol17', 'ol', 17, (-40, 15)); kare('yuz', None, 1, (-20, 5), boy=0.6, merkez=(0, -0.08, 1.62))
