# The end of every building script in tools/lm-blender/bina/<id>.py: the Yapi becomes one welded, smooth-shaded
# mesh, its colours and baked shadow go into the vertex colours (doku.py detayli_aktar), the GLB is written, and
# previews are rendered from three sides plus a close-up (EEVEE, the same material the game draws).
#   blender -b --factory-startup --python tools/lm-blender/bina/<id>.py -- <out.glb> [preview folder]
# (node tools/lm-blender/uret.mjs <id> runs that, then compresses the file into assets/models/lm/<id>.glb)
import os, sys, math
import bpy
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import temizle, argumanlar
from doku import nesne_dokulu, detayli_aktar


def _sahne_isik():
    sc = bpy.context.scene
    for e in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE'):
        try:
            sc.render.engine = e; break
        except TypeError:
            continue
    w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.55, 0.5, 0.45, 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
    sun_d = bpy.data.lights.new('gunes', 'SUN'); sun_d.energy = 3.2; sun_d.angle = math.radians(8)
    sun = bpy.data.objects.new('gunes', sun_d); sc.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(-40))
    cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'
    cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam)
    sc.camera = cam
    return cam


def onizlemeler(ob, klasor, ad):
    """four PNGs: front-left (the game's usual view), back-right, side, and a 2.6x close-up of the front"""
    os.makedirs(klasor, exist_ok=True)
    sc = bpy.context.scene
    cam = _sahne_isik()
    bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb)))
    hi = Vector((max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)))
    m = (lo + hi) / 2
    boy = max(hi.x - lo.x, hi.y - lo.y, hi.z - lo.z) * 1.45
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1000
    sc.render.image_settings.file_format = 'PNG'
    goruntu = [('1_on', -35, 32, 1.0, m), ('2_arka', 145, 32, 1.0, m), ('3_yan', 70, 22, 1.0, m),
               ('4_yakin', -25, 24, 2.6, Vector((m.x - (hi.x - lo.x) * 0.12, lo.y + (hi.y - lo.y) * 0.25, lo.z + (hi.z - lo.z) * 0.3)))]
    def cek(yol, mm, az, el, olcek):
        a, e = math.radians(az), math.radians(el)
        yon = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
        cam.data.ortho_scale = olcek
        cam.location = mm + yon * 12
        cam.rotation_euler = (-yon).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = yol
        bpy.ops.render.render(write_still=True)
    for isim, az, el, yak, mm in goruntu:
        cek(os.path.join(klasor, f'{ad}_{isim}.png'), mm, az, el, boy / yak)
    # extra close-ups on one sheet: LM_YAKIN="x,y,z,size[,azimuth];..." (model units)
    yk = os.environ.get('LM_YAKIN')
    if yk:
        import numpy as np
        sc.render.resolution_x, sc.render.resolution_y = 600, 450
        parcalar = []
        for i, s in enumerate(yk.split(';')):
            v = [float(t) for t in s.split(',')]
            yol = os.path.join(klasor, f'_yakin_{i}.png')
            cek(yol, Vector(v[:3]), v[4] if len(v) > 4 else -35, 28, v[3])
            im = bpy.data.images.load(yol)
            parcalar.append(np.array(im.pixels[:], np.float32).reshape(450, 600, 4))
            bpy.data.images.remove(im); os.remove(yol)
        sut = 4
        sat = (len(parcalar) + sut - 1) // sut
        pafta = np.ones((sat * 450, sut * 600, 4), np.float32)
        for i, p in enumerate(parcalar):
            r, c = sat - 1 - i // sut, i % sut          # (Blender images start at the bottom row)
            pafta[r * 450:(r + 1) * 450, c * 600:(c + 1) * 600] = p
        out = bpy.data.images.new('pafta', sut * 600, sat * 450)
        out.pixels[:] = pafta.ravel()
        out.filepath_raw = os.path.join(klasor, f'{ad}_5_pafta.png'); out.file_format = 'PNG'; out.save()


def calistir(y, ad):
    """build, export (argv: out.glb [preview folder]) and preview"""
    tri = y.ucgen_sayisi()
    print('UCGEN', tri)
    if tri < 15000 or tri > 70000:
        print('UYARI: ucgen sayisi hedefin (20-60 bin) disinda:', tri)
    arg = argumanlar()
    temizle()
    ob, anahtar = nesne_dokulu(y, ad)
    if 'mavi' not in anahtar:
        print('UYARI: sancak (mavi) yok')
    # footprint check (the game scales the longest side to 1)
    bb = [Vector(c) for c in ob.bound_box]
    wx = max(v.x for v in bb) - min(v.x for v in bb); wy = max(v.y for v in bb) - min(v.y for v in bb)
    hz = max(v.z for v in bb)
    print('BOYUT x %.2f y %.2f z %.2f (oran %.2f)' % (wx, wy, hz, max(wx, wy) / max(1e-6, min(wx, wy))))
    if arg:
        detayli_aktar(ob, anahtar, os.path.abspath(arg[0]))
    if len(arg) > 1:
        onizlemeler(ob, os.path.abspath(arg[1]), ad)
