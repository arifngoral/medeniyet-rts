# Characters on a real human body: Blender's Human Base Meshes (CC0, blender.org "Human Base Meshes" asset bundle,
# stylized male body) reshaped to the card art's proportions, fists closed by bending the fingers, clothes made from the
# body's own surface (a region copied and pushed out along its normals, given thickness), bound to the skeleton with
# Blender's automatic weights (the body) and the body's weights carried over (the clothes): one continuous skin that
# bends at the joints like a person. tools/lm-blender/README.md "Birimler".
import bpy, bmesh, math, os
import numpy as np
from mathutils import Vector, Matrix
from karakter import malzeme, yumusak

PAKET = os.environ.get('HBM_YOL', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.blender-varlik', 'human_base_meshes_bundle.blend'))


def govde_yukle():
    """the stylized male body and its eyes, transforms applied, centred on x = 0, feet on z = 0, facing -y"""
    with bpy.data.libraries.load(PAKET) as (src, dst):
        dst.objects = ['GEO-body_male_stylized', 'GEO-body_male_stylized.eye.L', 'GEO-body_male_stylized.eye.R']
    obs = []
    for o in dst.objects:
        o = o.copy(); o.data = o.data.copy()
        bpy.context.scene.collection.objects.link(o); obs.append(o)
    bpy.context.view_layer.update()
    for o in obs:     # (world matrices computed through the parent before it is cleared)
        mw = (o.parent.matrix_world @ o.matrix_parent_inverse @ o.matrix_basis) if o.parent else o.matrix_world.copy()
        o.parent = None; o.matrix_world = mw
        o.data.transform(o.matrix_world); o.matrix_world = Matrix.Identity(4)
    govde, gozler = obs[0], obs[1:]
    co = np.array([v.co[:] for v in govde.data.vertices])
    dx = -(co[:, 0].min() + co[:, 0].max()) / 2; dz = -co[:, 2].min()
    for o in obs: o.data.transform(Matrix.Translation((dx, 0, dz)))
    for o in obs:
        for p in o.data.polygons: p.use_smooth = True
    return govde, gozler


def deform(obs, f):
    """move every vertex: f(co) -> new co"""
    for o in obs:
        for v in o.data.vertices: v.co = f(v.co.copy())
        o.data.update()


def bolge_olcek(merkez, olcek, agirlik):
    """scale round merkez by olcek (a number or a 3-vector), weighted by agirlik(co) 0..1"""
    m = Vector(merkez); s = Vector(olcek) if not isinstance(olcek, (int, float)) else Vector((olcek,) * 3)
    def f(c):
        w = agirlik(c)
        if w <= 0: return c
        d = c - m
        return m + Vector((d.x * (1 + (s.x - 1) * w), d.y * (1 + (s.y - 1) * w), d.z * (1 + (s.z - 1) * w)))
    return f


def yumruk(bilek, uc, avuc, s0, R, el_mi):
    """close the fingers of a hand into a fist: the part beyond s0 (distance from the wrist along the hand) is bent
    round an axis across the knuckles, towards the palm (avuc: the palm's direction), radius R"""
    B = Vector(bilek); a = (Vector(uc) - B).normalized(); b = Vector(avuc).normalized(); b = (b - a * a.dot(b)).normalized()
    def f(c):
        if not el_mi(c): return c
        d = c - B; s = d.dot(a); t = d.dot(b); rest = d - a * s - b * t
        if s <= s0: return c
        L = s - s0; th = L / R
        # the bend tightens smoothly from the knuckles
        yeni_s = s0 + (R - t) * math.sin(th); yeni_t = R - (R - t) * math.cos(th)
        return B + a * yeni_s + b * yeni_t + rest
    return f


def bolge_kopya(govde, ad, malz, secim, ofset, kalinlik=0.006, duzle=0, kenar=6):
    """a garment: the body's faces whose vertices all pass secim(co, normal), copied and pushed out by ofset(co)
    along the normals, given kalinlik; duzle: smoothing passes (a boot hiding the toes)"""
    bm = bmesh.new(); bm.from_mesh(govde.data)
    bm.normal_update()
    sil = [f for f in bm.faces if not all(secim(v.co, v.normal) for v in f.verts)]
    bmesh.ops.delete(bm, geom=sil, context='FACES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.normal_update()
    for v in bm.verts:
        v.co = v.co + v.normal * ofset(v.co)
    # round off the ragged edge the face selection leaves (its boundary relaxed along itself)
    sinir = [v for v in bm.verts if v.is_boundary]
    for _ in range(kenar):
        yeni = {}
        for v in sinir:
            kom = [e.other_vert(v) for e in v.link_edges if e.is_boundary]
            if len(kom) == 2: yeni[v] = v.co * 0.5 + (kom[0].co + kom[1].co) * 0.25
        for v, c in yeni.items(): v.co = c
    if duzle:
        for _ in range(duzle):
            bmesh.ops.smooth_vert(bm, verts=bm.verts[:], factor=0.6, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    me = bpy.data.meshes.new(ad); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(o)
    for p in me.polygons: p.use_smooth = True
    me.materials.append(malzeme(malz))
    if kalinlik:
        sd = o.modifiers.new('kalin', 'SOLIDIFY'); sd.thickness = kalinlik; sd.offset = 1.0; sd.use_even_offset = False
        bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier='kalin')
    return o


def agirlik_aktar(kaynak, hedefler):
    """the body's bone weights onto the garments (nearest face, interpolated)"""
    for h in hedefler:
        for g in kaynak.vertex_groups:
            if g.name not in h.vertex_groups: h.vertex_groups.new(name=g.name)
        md = h.modifiers.new('aktar', 'DATA_TRANSFER'); md.object = kaynak
        md.use_vert_data = True; md.data_types_verts = {'VGROUP_WEIGHTS'}; md.vert_mapping = 'POLYINTERP_NEAREST'
        md.layers_vgroup_select_src = 'ALL'; md.layers_vgroup_select_dst = 'NAME'
        bpy.ops.object.select_all(action='DESELECT'); h.select_set(True); bpy.context.view_layer.objects.active = h
        bpy.ops.object.modifier_apply(modifier='aktar')


def sabit_agirlik(o, kemik):
    """every vertex of o on one bone (a helmet, a sword)"""
    for g in list(o.vertex_groups): o.vertex_groups.remove(g)
    g = o.vertex_groups.new(name=kemik); g.add(list(range(len(o.data.vertices))), 1.0, 'REPLACE')


def islev_agirlik(o, f):
    """weights from a function of the position: f(co) -> {bone: weight}"""
    for g in list(o.vertex_groups): o.vertex_groups.remove(g)
    gr = {}
    for v in o.data.vertices:
        for b, w in f(v.co).items():
            if w <= 1e-4: continue
            if b not in gr: gr[b] = o.vertex_groups.new(name=b)
            gr[b].add([v.index], w, 'REPLACE')


def parca_nesne(k, ad):
    """a Karakter's parts (helmet, weapons...) as one object (weights as each part asked)"""
    return k.nesne(ad)


def birlestir(obs, ad):
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active; o.name = ad; o.data.name = ad
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)
    return o


def oto_agirlik(govde, arm, haric=()):
    """Blender's automatic (heat) weights for the body; bones in haric do not deform it"""
    for b in arm.data.bones: b.use_deform = b.name not in haric
    bpy.ops.object.select_all(action='DESELECT')
    govde.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    for b in arm.data.bones: b.use_deform = True
    md = [m for m in govde.modifiers if m.type == 'ARMATURE']
    for m in md: govde.modifiers.remove(m)
    govde.parent = None
