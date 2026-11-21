# Rigged characters (units) built in Blender, stylized but detailed (in the manner of hand-painted hero shooters):
# each part is a low cage smoothed by subdivision, bound to its bone (rigid) or blended between bones by a weight
# function (the body and the clothes over it bend together, so nothing pokes through); procedural materials (mail
# rings, cloth weave, leather, wood planks, worn steel) are baked with ambient occlusion into one texture; an
# armature and actions (idle, walk, attack, death) go into one glTF. tools/lm-blender/README.md "Birimler".
import bpy, bmesh, math
import numpy as np
from mathutils import Vector, Quaternion, Matrix


def srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _dik(a):
    a = Vector(a).normalized()
    t = Vector((0, 0, 1)) if abs(a.z) < 0.9 else Vector((0, 1, 0))
    u = a.cross(t).normalized()
    return u, a.cross(u).normalized()


def yumusak(a, b, x):
    """0 below a, 1 above b, smooth between"""
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


class Karakter:
    def __init__(self):
        self.parcalar = []          # (verts, faces, material, weights, subdivision levels)

    def ekle(self, vs, fs, malz, kemik, alt=1):
        self.parcalar.append(([Vector(v) for v in vs], fs, malz, kemik, alt))

    # ---- primitives (alt: subdivision levels; 0 = hard) ----
    def tup(self, p0, p1, r0, r1, malz, kemik, n=10, ex=1.0, ey=1.0, kapak=True, yon=None, alt=1):
        p0, p1 = Vector(p0), Vector(p1)
        a = (p1 - p0).normalized()
        if yon is not None:
            u = (Vector(yon) - a * a.dot(Vector(yon))).normalized(); v = a.cross(u)
        else:
            u, v = _dik(a)
        vs = []
        for p, r in ((p0, r0), (p1, r1)):
            for i in range(n):
                t = 2 * math.pi * i / n
                vs.append(p + u * (math.cos(t) * r * ex) + v * (math.sin(t) * r * ey))
        fs = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        if kapak:
            fs.append(tuple(reversed(range(n)))); fs.append(tuple(range(n, 2 * n)))
        self.ekle(vs, fs, malz, kemik, alt)

    def yol(self, noktalar, yaricap, malz, kemik, n=8, alt=1, ex=1.0, ey=1.0, yon=None):
        """a tube along a polyline; yaricap: one radius or one per point (fingers, moustache, brows)"""
        P = [Vector(p) for p in noktalar]
        R = yaricap if isinstance(yaricap, (list, tuple)) else [yaricap] * len(P)
        vs = []
        u0 = None
        for i, p in enumerate(P):
            t = (P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]).normalized()
            if u0 is None:
                if yon is not None: u0 = (Vector(yon) - t * t.dot(Vector(yon))).normalized()
                else: u0, _ = _dik(t)
            u = (u0 - t * t.dot(u0)).normalized(); v = t.cross(u); u0 = u
            for j in range(n):
                s = 2 * math.pi * j / n
                vs.append(p + u * (math.cos(s) * R[i] * ex) + v * (math.sin(s) * R[i] * ey))
        m = len(P)
        fs = []
        for i in range(m - 1):
            for j in range(n):
                a, b = i * n + j, i * n + (j + 1) % n
                fs.append((a, b, b + n, a + n))
        fs.append(tuple(reversed(range(n)))); fs.append(tuple(range((m - 1) * n, m * n)))
        self.ekle(vs, fs, malz, kemik, alt)

    def kure(self, c, r, malz, kemik, n=12, k=8, olcek=(1, 1, 1), alt=-1.0, ust=1.0, don=None, sub=1):
        c = Vector(c)
        lat = [math.asin(alt) + (math.asin(ust) - math.asin(alt)) * j / k for j in range(k + 1)]
        vs, fs = [], []
        for j, ph in enumerate(lat):
            for i in range(n):
                t = 2 * math.pi * i / n
                p = Vector((math.cos(ph) * math.cos(t) * r * olcek[0], math.cos(ph) * math.sin(t) * r * olcek[1], math.sin(ph) * r * olcek[2]))
                if don is not None: p = don @ p
                vs.append(c + p)
        for j in range(k):
            for i in range(n):
                a, b = j * n + i, j * n + (i + 1) % n
                fs.append((a, b, b + n, a + n))
        fs.append(tuple(reversed(range(n)))); fs.append(tuple(range(k * n, k * n + n)))
        self.ekle(vs, fs, malz, kemik, sub)

    def kabuk(self, c, rx, ry, rz, lon0, lon1, lat0, lat1, kalinlik, malz, kemik, n=14, k=8, sub=1):
        """a patch of an ellipsoid shell (lon round z from +x, degrees, -90 = the front; lat -90..90), its thickness a
        function kalinlik(lon, lat) -> outward offset (a beard hugging the jaw, hair)"""
        c = Vector(c)
        def p(lo, la, d):
            lo_r, la_r = math.radians(lo), math.radians(la)
            nrm = Vector((math.cos(la_r) * math.cos(lo_r) / rx, math.cos(la_r) * math.sin(lo_r) / ry, math.sin(la_r) / rz)).normalized()
            base = c + Vector((math.cos(la_r) * math.cos(lo_r) * rx, math.cos(la_r) * math.sin(lo_r) * ry, math.sin(la_r) * rz))
            return base + nrm * d
        vs = []
        for j in range(k + 1):
            for i in range(n + 1):
                lo = lon0 + (lon1 - lon0) * i / n; la = lat0 + (lat1 - lat0) * j / k
                vs.append(p(lo, la, kalinlik(lo, la)))
        for j in range(k + 1):
            for i in range(n + 1):
                lo = lon0 + (lon1 - lon0) * i / n; la = lat0 + (lat1 - lat0) * j / k
                vs.append(p(lo, la, -0.004))
        N1 = n + 1; off = (k + 1) * N1
        fs = []
        for j in range(k):
            for i in range(n):
                a = j * N1 + i
                fs.append((a, a + 1, a + 1 + N1, a + N1))
                fs.append((off + a + N1, off + a + 1 + N1, off + a + 1, off + a))
        for i in range(n):          # edges
            fs.append((i + 1, i, off + i, off + i + 1))
            a = k * N1 + i; fs.append((a, a + 1, off + a + 1, off + a))
        for j in range(k):
            a = j * N1; fs.append((a + N1, a, off + a, off + a + N1))
            b = j * N1 + n; fs.append((b, b + N1, off + b + N1, off + b))
        self.ekle(vs, fs, malz, kemik, sub)

    def kutu(self, c, boyut, malz, kemik, don=None, alt=0):
        c = Vector(c); sx, sy, sz = [b / 2 for b in boyut]
        vs = []
        for x in (-sx, sx):
            for y in (-sy, sy):
                for z in (-sz, sz):
                    p = Vector((x, y, z))
                    if don is not None: p = don @ p
                    vs.append(c + p)
        fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        self.ekle(vs, fs, malz, kemik, alt)

    def halka(self, c, eksen, R, r, malz, kemik, n=20, m=6, alt=0):
        c = Vector(c); a = Vector(eksen).normalized(); u, v = _dik(a)
        vs, fs = [], []
        for i in range(n):
            t = 2 * math.pi * i / n
            d = u * math.cos(t) + v * math.sin(t)
            for j in range(m):
                s = 2 * math.pi * j / m
                vs.append(c + d * (R + r * math.cos(s)) + a * (r * math.sin(s)))
        for i in range(n):
            for j in range(m):
                a0, a1 = i * m + j, i * m + (j + 1) % m
                b0, b1 = ((i + 1) % n) * m + j, ((i + 1) % n) * m + (j + 1) % m
                fs.append((a0, b0, b1, a1))
        self.ekle(vs, fs, malz, kemik, alt)

    def yay(self, z0, z1, r0, r1, a0, a1, malz, kemik, ex=1.0, ey=1.0, kalin=0.018, n=10, merkez=(0, 0), egim=0.0, alt=1, kat=1):
        """a curved panel (part a0..a1 degrees of an elliptic tube from z0 to z1), kalin thick; kat: rows up its height"""
        cx, cy = merkez
        orta = math.radians((a0 + a1) / 2); om = Vector((math.cos(orta) * ex, math.sin(orta) * ey, 0)).normalized()
        rows = []
        for j in range(kat + 1):
            f = j / kat
            z = z0 + (z1 - z0) * f; r = r0 + (r1 - r0) * f; it = egim * (1 - f)
            for d in (0.0, -kalin):
                rows.append([Vector((cx + math.cos(math.radians(a0 + (a1 - a0) * i / n)) * (r + d) * ex,
                                     cy + math.sin(math.radians(a0 + (a1 - a0) * i / n)) * (r + d) * ey, z)) + om * it for i in range(n + 1)])
        vs = [p for row in rows for p in row]
        m = n + 1
        O = lambda j: (2 * j) * m; I = lambda j: (2 * j + 1) * m
        fs = []
        for j in range(kat):
            for i in range(n):
                fs.append((O(j) + i, O(j) + i + 1, O(j + 1) + i + 1, O(j + 1) + i))
                fs.append((I(j) + i + 1, I(j) + i, I(j + 1) + i, I(j + 1) + i + 1))
            fs.append((O(j), O(j + 1), I(j + 1), I(j)))
            fs.append((O(j) + n, I(j) + n, I(j + 1) + n, O(j + 1) + n))
        for i in range(n):
            fs.append((O(0) + i + 1, O(0) + i, I(0) + i, I(0) + i + 1))
            fs.append((O(kat) + i, O(kat) + i + 1, I(kat) + i + 1, I(kat) + i))
        self.ekle(vs, fs, malz, kemik, alt)

    # ---- the object: parts smoothed one by one, weighted, joined ----
    def nesne(self, ad, aci=40):
        sc = bpy.context.scene
        obs = []
        kemikler = []
        for vs, fs, malz, kemik, alt in self.parcalar:
            me = bpy.data.meshes.new('p')
            bm = bmesh.new()
            bv = [bm.verts.new(v) for v in vs]
            for f in fs:
                try: bm.faces.new([bv[i] for i in f])
                except ValueError: pass
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new('p', me); sc.collection.objects.link(ob)
            me.materials.append(malzeme(malz))
            # weights: one bone, or a function of the position -> {bone: weight}
            agir = {}
            for v in me.vertices:
                w = {kemik: 1.0} if isinstance(kemik, str) else kemik(v.co)
                for b, x in w.items():
                    if x <= 1e-4: continue
                    if b not in agir: agir[b] = ob.vertex_groups.new(name=b)
                    agir[b].add([v.index], x, 'REPLACE')
            if alt:
                md = ob.modifiers.new('sub', 'SUBSURF'); md.levels = alt; md.render_levels = alt
                bpy.context.view_layer.objects.active = ob
                bpy.ops.object.modifier_apply(modifier='sub')
            obs.append(ob)
        bpy.ops.object.select_all(action='DESELECT')
        for o in obs: o.select_set(True)
        bpy.context.view_layer.objects.active = obs[0]
        bpy.ops.object.join()
        ob = bpy.context.view_layer.objects.active
        ob.name = ad; ob.data.name = ad
        bpy.ops.object.vertex_group_normalize_all(lock_active=False)
        for p in ob.data.polygons: p.use_smooth = True
        ob.data.set_sharp_from_angle(angle=math.radians(aci))
        return ob


# ---------------- materials ----------------
# key -> (kind, sRGB colour, options)
MALZEME = {
    'ten':      ('ten', (0.98, 0.78, 0.65), {}),
    'dudak':    ('duz', (0.80, 0.48, 0.42), {}),
    'sakal':    ('sac', (0.43, 0.26, 0.14), {}),
    'goz_ak':   ('duz', (0.98, 0.97, 0.95), {'leke': 0.0}),
    'goz':      ('duz', (0.06, 0.04, 0.03), {'leke': 0.0}),
    'iris':     ('duz', (0.36, 0.24, 0.13), {'leke': 0.0}),
    'celik':    ('metal', (0.70, 0.72, 0.76), {}),
    'celik_k':  ('metal', (0.45, 0.47, 0.51), {}),
    'zirh':     ('orgu', (0.58, 0.60, 0.64), {}),
    'mavi':     ('kumas', (0.12, 0.36, 0.86), {}),        # team colour (the game repaints it)
    'sirma':    ('desen', (0.88, 0.68, 0.28), {}),
    'deri':     ('deri', (0.52, 0.32, 0.18), {}),
    'deri_k':   ('deri', (0.36, 0.22, 0.12), {}),
    'pantolon': ('kumas', (0.40, 0.45, 0.37), {}),
    'astar':    ('kumas', (0.36, 0.40, 0.33), {}),
    'ahsap':    ('ahsap', (0.60, 0.40, 0.23), {}),
    'pirinc':   ('metal', (0.82, 0.62, 0.28), {}),
    'taban':    ('duz', (0.22, 0.14, 0.08), {}),
}
_ONB = {}


def malzeme(ad):
    if ad in _ONB: return _ONB[ad]
    tur, renk, o = MALZEME[ad]
    m = bpy.data.materials.new('m_' + ad); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    bsdf = N.get('Principled BSDF'); bsdf.inputs['Roughness'].default_value = 0.8
    lin = [srgb2lin(c) for c in renk]
    tc = N.new('ShaderNodeTexCoord')
    def rgb(c, k=1.0):
        n = N.new('ShaderNodeRGB'); n.outputs[0].default_value = [x * k for x in c] + [1]; return n.outputs[0]
    def carp(a, b):
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1
        Lk.new(a, mx.inputs['A']); Lk.new(b, mx.inputs['B']); return mx.outputs['Result']
    def karis(a, b, fac):
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        Lk.new(fac, mx.inputs['Factor']); Lk.new(a, mx.inputs['A']); Lk.new(b, mx.inputs['B']); return mx.outputs['Result']
    def aralik(s, a0, a1, b0, b1):
        mr = N.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = a0; mr.inputs['From Max'].default_value = a1
        mr.inputs['To Min'].default_value = b0; mr.inputs['To Max'].default_value = b1; Lk.new(s, mr.inputs['Value']); return mr.outputs['Result']
    def gurultu(olcek, detay=4.0, puruz=0.5):
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = olcek; nz.inputs['Detail'].default_value = detay
        nz.inputs['Roughness'].default_value = puruz; Lk.new(tc.outputs['Object'], nz.inputs['Vector']); return nz.outputs['Fac']
    def gri(fac):
        c = N.new('ShaderNodeCombineColor'); Lk.new(fac, c.inputs[0]); Lk.new(fac, c.inputs[1]); Lk.new(fac, c.inputs[2]); return c.outputs[0]
    renk_c = rgb(lin)
    if tur == 'ten':
        out = carp(renk_c, gri(aralik(gurultu(18), 0.3, 0.7, 0.95, 1.04)))
    elif tur == 'sac':
        wv = N.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'
        wv.inputs['Scale'].default_value = 70; wv.inputs['Distortion'].default_value = 6; wv.inputs['Detail'].default_value = 3
        Lk.new(tc.outputs['Object'], wv.inputs['Vector'])
        out = carp(renk_c, gri(aralik(wv.outputs['Fac'], 0, 1, 0.72, 1.18)))
    elif tur == 'metal':
        # worn steel: faint scratches, bright worn edges (pointiness)
        gm = N.new('ShaderNodeNewGeometry')
        kenar = aralik(gm.outputs['Pointiness'], 0.5, 0.56, 0.0, 1.0)
        tem = carp(renk_c, gri(aralik(gurultu(40, 8, 0.7), 0.35, 0.65, 0.88, 1.08)))
        out = karis(tem, rgb([min(1, x * 1.5 + 0.08) for x in lin]), kenar)
    elif tur == 'orgu':
        # mail: rows of rings (voronoi cells, dark rims)
        vr = N.new('ShaderNodeTexVoronoi'); vr.feature = 'DISTANCE_TO_EDGE'; vr.inputs['Scale'].default_value = 140
        Lk.new(tc.outputs['Object'], vr.inputs['Vector'])
        halka = aralik(vr.outputs['Distance'], 0.02, 0.12, 0.0, 1.0)
        out = karis(rgb(lin, 0.45), carp(renk_c, gri(aralik(gurultu(30), 0.3, 0.7, 0.9, 1.15))), halka)
    elif tur == 'kumas':
        # cloth: a fine weave (two wave sets) and soft mottling
        def dalga(yon):
            wv = N.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = yon; wv.inputs['Scale'].default_value = 260
            Lk.new(tc.outputs['Object'], wv.inputs['Vector']); return aralik(wv.outputs['Fac'], 0, 1, 0.95, 1.04)
        out = carp(carp(carp(renk_c, gri(dalga('X'))), gri(dalga('Z'))), gri(aralik(gurultu(9), 0.3, 0.7, 0.93, 1.05)))
    elif tur == 'desen':
        br = N.new('ShaderNodeTexBrick'); br.inputs['Scale'].default_value = 90
        br.inputs['Color1'].default_value = lin + [1]; br.inputs['Color2'].default_value = [x * 0.8 for x in lin] + [1]
        br.inputs['Mortar'].default_value = [x * 0.5 for x in lin] + [1]; br.inputs['Mortar Size'].default_value = 0.04
        Lk.new(tc.outputs['Object'], br.inputs['Vector']); out = br.outputs['Color']
    elif tur == 'deri':
        mg = gurultu(60, 10, 0.8)
        cizik = aralik(gurultu(12, 2, 0.5), 0.55, 0.62, 1.0, 0.75)
        out = carp(carp(renk_c, gri(aralik(mg, 0.3, 0.7, 0.88, 1.1))), gri(cizik))
    elif tur == 'ahsap':
        # planks along y with dark seams, grain along the planks
        sep = N.new('ShaderNodeSeparateXYZ'); Lk.new(tc.outputs['Object'], sep.inputs[0])
        mt = N.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = 12.0; Lk.new(sep.outputs['Y'], mt.inputs[0])
        fr = N.new('ShaderNodeMath'); fr.operation = 'FRACT'; Lk.new(mt.outputs[0], fr.inputs[0])
        dikis = aralik(fr.outputs[0], 0.0, 0.06, 0.45, 1.0)
        wv = N.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Y'; wv.inputs['Scale'].default_value = 40
        wv.inputs['Distortion'].default_value = 8; Lk.new(tc.outputs['Object'], wv.inputs['Vector'])
        out = carp(carp(renk_c, gri(aralik(wv.outputs['Fac'], 0, 1, 0.82, 1.1))), gri(dikis))
    else:
        out = carp(renk_c, gri(aralik(gurultu(20), 0.3, 0.7, 1 - o.get('leke', 0.04), 1 + o.get('leke', 0.04))))
    Lk.new(out, bsdf.inputs['Base Color'])
    _ONB[ad] = m
    return m


def pisir(ob, boyut=2048, ornek=32, ao_guc=0.6, ao_mesafe=0.12):
    """UV unwrap, bake the materials' colour and AO into one texture, give the object that one material"""
    sc = bpy.context.scene
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(55), island_margin=0.003, scale_to_bounds=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    sc.render.engine = 'CYCLES'; sc.cycles.samples = ornek; sc.cycles.device = 'CPU'
    imgs = {}
    for ad in ('renk', 'ao'):
        im = bpy.data.images.new('b_' + ad, boyut, boyut, alpha=False, float_buffer=True)
        im.colorspace_settings.name = 'Non-Color' if ad == 'ao' else 'Linear Rec.709'; imgs[ad] = im
    def hedef(im):
        for m in ob.data.materials:
            n = m.node_tree.nodes.get('hedef') or m.node_tree.nodes.new('ShaderNodeTexImage')
            n.name = 'hedef'; n.image = im; m.node_tree.nodes.active = n
    hedef(imgs['renk'])
    sc.render.bake.use_pass_direct = False; sc.render.bake.use_pass_indirect = False; sc.render.bake.use_pass_color = True
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, margin=8)
    hedef(imgs['ao'])
    sc.world = sc.world or bpy.data.worlds.new('W'); sc.world.light_settings.distance = ao_mesafe
    bpy.ops.object.bake(type='AO', margin=8)
    W = boyut
    renk = np.array(imgs['renk'].pixels[:], np.float32).reshape(W, W, 4)
    ao = np.array(imgs['ao'].pixels[:], np.float32).reshape(W, W, 4)[..., :1]
    son = renk.copy(); son[..., :3] = renk[..., :3] * ((1 - ao_guc) + ao_guc * ao)
    son = np.clip(son, 0, 1); rgb = son[..., :3]
    son[..., :3] = np.where(rgb <= 0.0031308, rgb * 12.92, 1.055 * np.power(rgb, 1 / 2.4) - 0.055)
    out = bpy.data.images.new('doku', W, W, alpha=False); out.pixels[:] = son.ravel()
    m = bpy.data.materials.new('pismis'); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes.get('Principled BSDF'); bsdf.inputs['Roughness'].default_value = 0.8
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = out; nt.links.new(tx.outputs['Color'], bsdf.inputs['Base Color'])
    ob.data.materials.clear(); ob.data.materials.append(m)
    return out


# ---------------- skeleton and actions ----------------
def iskelet(ad, kemikler):
    arm = bpy.data.armatures.new(ad + '_iskelet')
    ob = bpy.data.objects.new(ad + '_iskelet', arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    for n, h, t, p in kemikler:
        eb = arm.edit_bones.new(n); eb.head = Vector(h); eb.tail = Vector(t); eb.roll = 0
        if p: eb.parent = arm.edit_bones[p]
    bpy.ops.object.mode_set(mode='OBJECT')
    for pb in ob.pose.bones: pb.rotation_mode = 'QUATERNION'
    return ob


def bagla(govde, arm):
    govde.parent = arm
    md = govde.modifiers.new('iskelet', 'ARMATURE'); md.object = arm


def poz(arm, aciler, kok=None):
    for pb in arm.pose.bones:
        pb.rotation_quaternion = Quaternion()
        if pb.name in aciler:
            M = pb.bone.matrix_local.to_3x3().inverted()
            q = Quaternion()
            for ax, deg in aciler[pb.name]:
                v = {'x': Vector((1, 0, 0)), 'y': Vector((0, 1, 0)), 'z': Vector((0, 0, 1))}[ax]
                q = Quaternion((M @ v).normalized(), math.radians(deg)) @ q
            pb.rotation_quaternion = q
    k = arm.pose.bones.get('kok')
    if k is not None:
        k.location = Vector((0, 0, 0))
        if kok: k.location = k.bone.matrix_local.to_3x3().inverted() @ Vector(kok)


def eylem(arm, ad, kareler):
    ad_ = arm.animation_data or arm.animation_data_create()
    act = bpy.data.actions.new(ad); act.use_fake_user = True
    ad_.action = act
    for f, aci, kok in kareler:
        poz(arm, aci, kok)
        for pb in arm.pose.bones:
            pb.keyframe_insert('rotation_quaternion', frame=f)
            if pb.name == 'kok': pb.keyframe_insert('location', frame=f)
    tr = ad_.nla_tracks.new(); tr.name = ad
    tr.strips.new(ad, int(kareler[0][0]), act); tr.mute = True
    ad_.action = None
    return act


def disa_aktar(arm, govde, yol):
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True); govde.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=yol, export_format='GLB', use_selection=True, export_yup=True, export_normals=True,
                              export_texcoords=True, export_materials='EXPORT', export_skins=True, export_animations=True,
                              export_animation_mode='ACTIONS', export_force_sampling=True, export_frame_step=1,
                              export_image_format='JPEG', export_jpeg_quality=88)
