# Rigged characters (units) built in Blender: parts from smooth primitives, each part bound wholly to one bone (rigid
# skinning: no stretching, the joints hidden by round elbows / knees), vertex colours, an armature and actions
# (idle, walk, attack, death) exported in one glTF. tools/lm-blender/README.md "Birimler".
import bpy, bmesh, math
from mathutils import Vector, Quaternion, Matrix


def srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _dik(a):
    """two unit vectors perpendicular to a (and to each other)"""
    a = Vector(a).normalized()
    t = Vector((0, 0, 1)) if abs(a.z) < 0.9 else Vector((0, 1, 0))
    u = a.cross(t).normalized()
    return u, a.cross(u).normalized()


class Karakter:
    def __init__(self):
        self.bm = bmesh.new()
        self.col = self.bm.loops.layers.float_color.new('Col')
        self.dl = self.bm.verts.layers.deform.verify()
        self.gruplar = []

    def _grup(self, ad):
        if ad not in self.gruplar: self.gruplar.append(ad)
        return self.gruplar.index(ad)

    def ekle(self, vs, fs, renk, kemik):
        gi = self._grup(kemik)
        bv = [self.bm.verts.new(v) for v in vs]
        for v in bv: v[self.dl][gi] = 1.0
        lin = (srgb2lin(renk[0]), srgb2lin(renk[1]), srgb2lin(renk[2]), 1.0)
        for f in fs:
            try:
                face = self.bm.faces.new([bv[i] for i in f])
            except ValueError:
                continue
            for l in face.loops: l[self.col] = lin

    # ---- primitives ----
    def tup(self, p0, p1, r0, r1, renk, kemik, n=10, ex=1.0, ey=1.0, kapak=True, yon=None):
        """a tapered tube from p0 (radius r0) to p1 (r1); ex / ey stretch the section along its two cross axes;
        yon: a vector the first cross axis leans to"""
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
        self.ekle(vs, fs, renk, kemik)

    def kure(self, c, r, renk, kemik, n=12, k=8, olcek=(1, 1, 1), alt=-1.0, ust=1.0, don=None):
        """an ellipsoid; alt / ust: the part kept, as sin of latitude (-1..1: whole); don: a Matrix to turn it"""
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
        fs.append(tuple(reversed(range(n))))
        fs.append(tuple(range(k * n, k * n + n)))
        self.ekle(vs, fs, renk, kemik)

    def kutu(self, c, boyut, renk, kemik, don=None):
        c = Vector(c); sx, sy, sz = [b / 2 for b in boyut]
        vs = []
        for x in (-sx, sx):
            for y in (-sy, sy):
                for z in (-sz, sz):
                    p = Vector((x, y, z))
                    if don is not None: p = don @ p
                    vs.append(c + p)
        fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        self.ekle(vs, fs, renk, kemik)

    def yay(self, z0, z1, r0, r1, a0, a1, renk, kemik, ex=1.0, ey=1.0, kalin=0.018, n=10, merkez=(0, 0), egim=0.0):
        """a curved panel: the part a0..a1 (degrees round z, -90 = the front, -y) of an elliptic tube from z0 (r0) to
        z1 (r1), kalin thick, closed at its edges (a tabard, a skirt flap). egim: the bottom pushed out along the
        panel's middle direction"""
        cx, cy = merkez
        orta = math.radians((a0 + a1) / 2); om = Vector((math.cos(orta) * ex, math.sin(orta) * ey, 0)).normalized()
        vs = []
        for z, r, it in ((z0, r0, egim), (z1, r1, 0.0)):
            for d in (0.0, -kalin):
                for i in range(n + 1):
                    t = math.radians(a0 + (a1 - a0) * i / n)
                    vs.append(Vector((cx + math.cos(t) * (r + d) * ex, cy + math.sin(t) * (r + d) * ey, z)) + om * it)
        m = n + 1
        O0, I0, O1, I1 = 0, m, 2 * m, 3 * m          # outer/inner rows at z0 and z1
        fs = []
        for i in range(n):
            fs.append((O0 + i, O0 + i + 1, O1 + i + 1, O1 + i))
            fs.append((I0 + i + 1, I0 + i, I1 + i, I1 + i + 1))
            fs.append((O0 + i + 1, O0 + i, I0 + i, I0 + i + 1))
            fs.append((O1 + i, O1 + i + 1, I1 + i + 1, I1 + i))
        fs.append((O0, O1, I1, I0)); fs.append((O0 + n, I0 + n, I1 + n, O1 + n))
        self.ekle(vs, fs, renk, kemik)

    def halka(self, c, eksen, R, r, renk, kemik, n=20, m=6):
        """a torus round axis eksen (major radius R, tube r)"""
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
        self.ekle(vs, fs, renk, kemik)

    # ---- the object ----
    def nesne(self, ad, aci=48):
        bm = self.bm
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
        me = bpy.data.meshes.new(ad)
        bm.to_mesh(me); bm.free()
        for p in me.polygons: p.use_smooth = True
        me.set_sharp_from_angle(angle=math.radians(aci))
        me.color_attributes.active_color = me.color_attributes['Col']
        me.color_attributes.render_color_index = me.color_attributes.active_color_index
        ob = bpy.data.objects.new(ad, me)
        bpy.context.scene.collection.objects.link(ob)
        for g in self.gruplar: ob.vertex_groups.new(name=g)
        m = bpy.data.materials.new(ad + '_mat'); m.use_nodes = True
        nt = m.node_tree; bsdf = nt.nodes.get('Principled BSDF')
        bsdf.inputs['Roughness'].default_value = 0.85
        ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
        nt.links.new(ca.outputs['Color'], bsdf.inputs['Base Color'])
        me.materials.append(m)
        return ob


def iskelet(ad, kemikler):
    """kemikler: [(name, head, tail, parent or None)] -> armature object"""
    arm = bpy.data.armatures.new(ad + '_iskelet')
    ob = bpy.data.objects.new(ad + '_iskelet', arm)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
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


# ---- animation: rotations given about the armature's own axes (x: pitch, forward is -x for a bone hanging down;
#      z: turn), turned into each bone's local space ----
def poz(arm, aciler, kok=None):
    """aciler: {bone: [(axis 'x'|'y'|'z', degrees), ...]} -> sets the pose (bones not named: rest)"""
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
        if kok:
            # kok: (dx, dy, dz) in armature space (the root bone points up: local y = armature z)
            M = k.bone.matrix_local.to_3x3().inverted()
            k.location = M @ Vector(kok)


def anahtar(arm, kare):
    for pb in arm.pose.bones:
        pb.keyframe_insert('rotation_quaternion', frame=kare)
        if pb.name == 'kok': pb.keyframe_insert('location', frame=kare)


def eylem(arm, ad, kareler, dongu=True):
    """kareler: [(frame, {bone: [(axis, deg)]}, root offset or None)] -> an action stashed on its own NLA track"""
    ad_ = arm.animation_data or arm.animation_data_create()
    act = bpy.data.actions.new(ad); act.use_fake_user = True
    ad_.action = act
    for f, aci, kok in kareler:
        poz(arm, aci, kok)
        anahtar(arm, f)
    tr = ad_.nla_tracks.new(); tr.name = ad
    st = tr.strips.new(ad, int(kareler[0][0]), act)
    tr.mute = True
    ad_.action = None
    return act


def disa_aktar(arm, govde, yol):
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True); govde.select_set(True)
    bpy.context.view_layer.objects.active = arm
    kw = dict(filepath=yol, export_format='GLB', use_selection=True, export_yup=True, export_normals=True,
              export_texcoords=False, export_materials='EXPORT', export_skins=True, export_animations=True,
              export_animation_mode='ACTIONS', export_force_sampling=True, export_frame_step=1)
    try:
        bpy.ops.export_scene.gltf(**kw, export_vertex_color='ACTIVE')
    except TypeError:
        bpy.ops.export_scene.gltf(**kw, export_colors=True)
