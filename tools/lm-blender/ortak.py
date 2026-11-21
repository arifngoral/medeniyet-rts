# Shared helpers for the Blender-built age-up building models (tools/lm-blender/README.md).
# A model is built face by face into one mesh with a per-corner colour (no texture): the game reads such a file
# (render/glb-models.js, untextured path) and repaints the saturated banner blue in the player's colour.
import bpy, bmesh, math, random, sys, os
from mathutils import Vector


def srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


class Yapi:
    """Collects faces: each face is a list of (x, y, z) points (Blender: z up) and an sRGB colour."""

    def __init__(self, tohum=1, oynama=0.04):
        self.faces = []
        self.rng = random.Random(tohum)
        self.oynama = oynama   # per-face brightness jitter (hand-painted look)

    def yuz(self, pts, renk, oyna=True):
        k = 1 + (self.rng.uniform(-self.oynama, self.oynama) if oyna else 0)
        self.faces.append(([tuple(p) for p in pts], tuple(min(1, c * k) for c in renk)))

    def ters(self, pts, renk, oyna=True):   # the same face seen from the other side
        self.yuz(list(reversed(pts)), renk, oyna)

    # a band of quads between two closed rings of 3D points (same length)
    def serit(self, r1, r2, renk, kapali=True, oyna=True):
        n = len(r1)
        for i in range(n if kapali else n - 1):
            j = (i + 1) % n
            self.yuz([r1[i], r1[j], r2[j], r2[i]], renk, oyna)

    # axis-aligned-in-a-frame box: origin o, unit axes ex, ey (horizontal), size w x d x h; which faces
    def kutu(self, o, ex, ey, w, d, h, renk, yuzler='onarkasagsolust'):
        o, ex, ey, ez = Vector(o), Vector(ex), Vector(ey), Vector((0, 0, 1))
        P = lambda a, b, c: o + ex * a + ey * b + ez * c
        if 'on' in yuzler: self.yuz([P(0, 0, 0), P(w, 0, 0), P(w, 0, h), P(0, 0, h)], renk)
        if 'arka' in yuzler: self.yuz([P(w, d, 0), P(0, d, 0), P(0, d, h), P(w, d, h)], renk)
        if 'sol' in yuzler: self.yuz([P(0, d, 0), P(0, 0, 0), P(0, 0, h), P(0, d, h)], renk)
        if 'sag' in yuzler: self.yuz([P(w, 0, 0), P(w, d, 0), P(w, d, h), P(w, 0, h)], renk)
        if 'ust' in yuzler: self.yuz([P(0, 0, h), P(w, 0, h), P(w, d, h), P(0, d, h)], renk)

    # a vertical cylinder (pole)
    def silindir(self, c, r, z0, z1, renk, n=6):
        ring = lambda z: [Vector((c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n), z)) for i in range(n)]
        self.serit(ring(z0), ring(z1), renk)
        self.yuz(ring(z1), renk)

    def ucgen_sayisi(self):
        return sum(len(p) - 2 for p, _ in self.faces)

    def nesne(self, ad, dikey=1.0):   # dikey: vertical stretch (a game reads a squat building better taller)
        me = bpy.data.meshes.new(ad)
        bm = bmesh.new()
        lay = bm.loops.layers.float_color.new('Col')
        for pts, renk in self.faces:
            vs = [bm.verts.new((p[0], p[1], p[2] * dikey)) for p in pts]
            try:
                f = bm.faces.new(vs)
            except ValueError:
                continue
            lin = (srgb2lin(renk[0]), srgb2lin(renk[1]), srgb2lin(renk[2]), 1.0)
            for l in f.loops:
                l[lay] = lin
        bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='EAR_CLIP')
        bm.to_mesh(me)
        bm.free()
        me.color_attributes.active_color = me.color_attributes['Col']
        me.color_attributes.render_color_index = me.color_attributes.active_color_index
        ob = bpy.data.objects.new(ad, me)
        bpy.context.scene.collection.objects.link(ob)
        mat = bpy.data.materials.new(ad + '_mat')
        mat.use_nodes = True
        nt = mat.node_tree
        bsdf = nt.nodes.get('Principled BSDF')
        ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
        nt.links.new(ca.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.92
        me.materials.append(mat)
        return ob


def temizle():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def disa_aktar(ob, yol):
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    kw = dict(filepath=yol, export_format='GLB', use_selection=True, export_materials='EXPORT', export_yup=True,
              export_normals=False, export_texcoords=False)
    try:
        bpy.ops.export_scene.gltf(**kw, export_vertex_color='ACTIVE')
    except TypeError:
        bpy.ops.export_scene.gltf(**kw, export_colors=True)


def onizle(yol, merkez=(0, 0, 0.2), boy=2.4, aci=(-35, 0, 0), cozunurluk=(1200, 800)):
    """Orthographic workbench render with the vertex colours on a white background.
    aci: (azimuth degrees around z, ...) - camera looks from azimuth az, elevation el."""
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading
    sh.light = 'STUDIO'
    sh.color_type = 'VERTEX'
    sh.show_cavity = True
    sh.cavity_type = 'WORLD'
    sh.show_shadows = True
    sc.render.resolution_x, sc.render.resolution_y = cozunurluk
    sc.render.film_transparent = False
    sc.world = sc.world or bpy.data.worlds.new('W')
    sh.background_type = 'VIEWPORT'
    sh.background_color = (1, 1, 1)
    az, el = math.radians(aci[0]), math.radians(aci[1] if len(aci) > 1 and aci[1] else 30)
    cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'; cam_d.ortho_scale = boy
    cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam)
    m = Vector(merkez)
    yon = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.location = m + yon * 10
    cam.rotation_euler = (-yon).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam
    sc.render.filepath = yol
    sc.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)


def argumanlar():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    return a
