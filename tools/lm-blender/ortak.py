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
        if isinstance(renk, str):   # a material key (doku.py): no jitter, the texture varies
            self.faces.append(([tuple(p) for p in pts], renk)); return
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

    # a face whose winding is turned to face direction yon
    def yuz_yon(self, pts, renk, yon, oyna=True):
        pts = [Vector(p) for p in pts]
        n = Vector((0, 0, 0))
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            n += Vector(((a.y - b.y) * (a.z + b.z), (a.z - b.z) * (a.x + b.x), (a.x - b.x) * (a.y + b.y)))
        self.yuz(pts if n.dot(Vector(yon)) >= 0 else list(reversed(pts)), renk, oyna)

    # a vertical n-sided prism (tower, drum, minaret shaft); kat: start angle
    def prizma(self, c, r, z0, z1, renk, n=8, ust=True, ust_renk=None, kat=0.0):
        ring = lambda z: [Vector((c[0] + r * math.cos(kat + 2 * math.pi * i / n), c[1] + r * math.sin(kat + 2 * math.pi * i / n), z)) for i in range(n)]
        self.serit(ring(z0), ring(z1), renk)
        if ust: self.yuz(ring(z1), ust_renk or renk)
        return ring

    # a cone (minaret cap, turret roof)
    def koni(self, c, r, z0, h, renk, n=12):
        ring = [Vector((c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n), z0)) for i in range(n)]
        tepe = Vector((c[0], c[1], z0 + h))
        for i in range(n):
            self.yuz([ring[i], ring[(i + 1) % n], tepe], renk)

    # a dome: half-ellipsoid of radius r, height h on z0; t0..t1 the part of the round it covers (a half dome: pi wide,
    # closed by a flat face on its open side)
    def kubbe(self, c, r, z0, h, renk, n=16, kat=5, t0=0.0, t1=2 * math.pi, kapak=None):
        tam = abs(t1 - t0 - 2 * math.pi) < 1e-6
        m = n if tam else n + 1
        def ring(k):
            ph = math.pi / 2 * k / kat
            return [Vector((c[0] + r * math.cos(ph) * math.cos(t0 + (t1 - t0) * i / n), c[1] + r * math.cos(ph) * math.sin(t0 + (t1 - t0) * i / n), z0 + h * math.sin(ph))) for i in range(m)]
        rings = [ring(k) for k in range(kat)]
        for k in range(kat - 1):
            self.serit(rings[k], rings[k + 1], renk, kapali=tam)
        tepe = Vector((c[0], c[1], z0 + h))
        top = rings[-1]
        for i in range(n if tam else n):
            self.yuz([top[i], top[(i + 1) % m], tepe], renk)
        if not tam:   # the open side
            yan = [rings[k][0] for k in range(kat)] + [tepe] + [rings[k][-1] for k in reversed(range(kat))]
            orta = (t0 + t1) / 2
            self.yuz_yon(yan, kapak or renk, (-math.cos(orta), -math.sin(orta), 0))
        return tepe

    # one bay of wall from a to b with a round-arched opening, seen from the right of a->b (nc); renkler: wall, reveal,
    # sill, dark back. korkuluk: sill height of a parapet in the opening
    def kemerli(self, a, b, z0, H, renkler, v0=0.0, en=0.68, ust=0.017, derin=0.03, k_say=6, korkuluk=None, sivri=0.0):
        """sivri > 0: a pointed (Ottoman) arch, its rise = sivri x span (0.6 is typical); 0: round"""
        duvar, koyu, acik, delik = renkler
        a, b = Vector(a), Vector(b)
        W = (b - a).length
        e = (b - a) / W
        nc = Vector((e.y, -e.x, 0))
        L = lambda u, v, d=0.0: a + e * u - nc * d + Vector((0, 0, z0 + v))
        x0, x1 = (1 - en) / 2 * W, (1 + en) / 2 * W
        R = (x1 - x0) / 2
        if sivri:
            w = x1 - x0; hr = sivri * w
            hs = H - ust - hr
            rho = (w * w / 4 + hr * hr) / w
            c = x0 + rho
            ta = math.atan2(hr, (x0 + w / 2) - c)
            yari = k_say // 2
            sol = [(c + rho * math.cos(math.pi - (math.pi - ta) * k / yari), hs + rho * math.sin(math.pi - (math.pi - ta) * k / yari)) for k in range(1, yari + 1)]
            sag = [(x0 + x1 - u, v) for u, v in reversed(sol[:-1])]
            kemer = sol + sag
        else:
            hs = H - ust - R
            kemer = [(x0 + R + R * math.cos(math.pi - math.pi * k / k_say), hs + R * math.sin(math.pi - math.pi * k / k_say)) for k in range(1, k_say)]
        acikl = [(x0, v0), (x0, hs)] + kemer + [(x1, hs), (x1, v0)]
        self.yuz([L(0, 0), L(x0, 0), L(x0, H), L(0, H)], duvar)
        self.yuz([L(x1, 0), L(W, 0), L(W, H), L(x1, H)], duvar)
        if v0 > 0: self.yuz([L(x0, 0), L(x1, 0), L(x1, v0), L(x0, v0)], duvar)
        tp = [(x0, hs)] + kemer + [(x1, hs)]
        for k in range(len(tp) - 1):
            (ua, va), (ub, vb) = tp[k], tp[k + 1]
            self.yuz([L(ua, va), L(ub, vb), L(ub, H), L(ua, H)], duvar)
        for k in range(len(acikl)):
            p, q = acikl[k], acikl[(k + 1) % len(acikl)]
            self.yuz([L(*p), L(*p, derin), L(*q, derin), L(*q)], acik if k == len(acikl) - 1 else koyu)
        self.yuz([L(*acikl[0], derin)] + [L(*acikl[-1], derin)] + [L(*q, derin) for q in reversed(acikl[1:-1])], delik)
        if korkuluk:
            d0, d1, h = derin * 0.35, derin * 0.6, v0 + korkuluk
            self.yuz([L(x0, v0, d0), L(x1, v0, d0), L(x1, h, d0), L(x0, h, d0)], acik)
            self.yuz([L(x0, h, d0), L(x1, h, d0), L(x1, h, d1), L(x0, h, d1)], acik)
        return W, e, nc, L

    # a dark window (round-headed if kemer) painted just in front of a wall: o a point on the wall, ex along it, n out
    def pencere(self, o, ex, n, u, v, w, h, renk, kemer=True, k_say=4):
        o, ex, n = Vector(o), Vector(ex), Vector(n)
        P = lambda uu, vv: o + ex * uu + Vector((0, 0, vv)) + n * 0.003
        R = w / 2
        pts = [P(u, v), P(u + w, v)]
        if kemer:
            pts += [P(u + R + R * math.cos(math.pi * k / k_say), v + h - R + R * math.sin(math.pi * k / k_say)) for k in range(k_say + 1)]
        else:
            pts += [P(u + w, v + h), P(u, v + h)]
        self.yuz_yon(pts, renk, n)

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
