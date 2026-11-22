# Back-face diagnosis: blender -b --factory-startup --python tools/lm-blender/teshis.py -- tools/lm-blender/bina/<id>.py <out.json>
# Finds faces seen from behind (Cycles, Backfacing) from many views and groups them by the source line that made them.
import sys, os, math, json, traceback, runpy
import bpy, bmesh
import numpy as np
from mathutils import Vector

arg = sys.argv[sys.argv.index('--') + 1:]
betik, cikti = os.path.abspath(arg[0]), arg[1]
LM = os.path.join(os.path.dirname(betik), '..')
sys.path.insert(0, os.path.abspath(LM)); sys.path.insert(0, os.path.dirname(betik))
if os.environ.get('TESHIS_TABAN'): sys.path.insert(0, os.environ['TESHIS_TABAN'])
import ortak, bina_ortak, doku

KAY = []
class TagList(list):
    def append(self, v):
        st = traceback.extract_stack()[:-1]
        fr = [f for f in st if os.path.basename(f.filename) not in ('ortak.py', 'teshis.py', 'runpy.py', '<frozen runpy>')]
        fr = [f for f in fr if not f.filename.startswith('<')]
        ic = fr[-1] if fr else None
        dis = [f for f in fr if os.path.abspath(f.filename) == betik]
        tag = '%s:%d %s' % (os.path.basename(ic.filename), ic.lineno, ic.name) if ic else '?'
        if dis and dis[-1] is not ic: tag += '  <  %s:%d' % (os.path.basename(dis[-1].filename), dis[-1].lineno)
        super().append(v); KAY.append(tag)
    def pop(self, i=-1):
        KAY.pop(i); return super().pop(i)
    def __setitem__(self, i, v):
        if isinstance(i, slice): raise RuntimeError('slice set')
        super().__setitem__(i, v)

_init = ortak.Yapi.__init__
def init(self, *a, **k):
    _init(self, *a, **k); self.faces = TagList()
ortak.Yapi.__init__ = init

def teshis(y, ad):
    ortak.temizle()
    ob, anahtar = doku.nesne_dokulu(y, ad, kimlik=True)
    me = ob.data
    kim = [0] * len(me.polygons)
    me.attributes['kim'].data.foreach_get('value', kim)
    at = me.attributes.new('kimf', 'FLOAT', 'FACE')
    at.data.foreach_set('value', [float(k + 1) for k in kim])
    mat = bpy.data.materials.new('tm'); mat.use_nodes = True
    N = mat.node_tree.nodes; L = mat.node_tree.links
    for n in list(N): N.remove(n)
    a = N.new('ShaderNodeAttribute'); a.attribute_name = 'kimf'
    g = N.new('ShaderNodeNewGeometry')
    cc = N.new('ShaderNodeCombineColor')
    L.new(a.outputs['Fac'], cc.inputs[0]); L.new(g.outputs['Backfacing'], cc.inputs[1])
    em = N.new('ShaderNodeEmission'); L.new(cc.outputs[0], em.inputs[0])
    o = N.new('ShaderNodeOutputMaterial'); L.new(em.outputs[0], o.inputs[0])
    me.materials.clear(); me.materials.append(mat)
    for p in me.polygons: p.material_index = 0
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 1; sc.cycles.use_denoising = False
    sc.cycles.pixel_filter_type = 'BOX'; sc.cycles.filter_width = 0.01
    sc.cycles.max_bounces = 0
    sc.view_settings.view_transform = 'Raw'
    sc.render.film_transparent = True
    w = bpy.data.worlds.new('W'); sc.world = w
    RX, RY = (1400, 1000) if os.environ.get('TESHIS_UC') else (1000, 720)
    sc.render.resolution_x, sc.render.resolution_y = RX, RY
    sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '32'
    cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'
    cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
    bb = [Vector(c) for c in ob.bound_box]
    lo = Vector((min(v.x for v in bb), min(v.y for v in bb), min(v.z for v in bb)))
    hi = Vector((max(v.x for v in bb), max(v.y for v in bb), max(v.z for v in bb)))
    m = (lo + hi) / 2; boy = max(hi - lo) * 1.45
    goruntu = [(-35, 32), (145, 32), (70, 22)] + ([] if os.environ.get('TESHIS_UC') else [(az, el) for el in (20, 40, 60) for az in range(0, 360, 45)])
    nf = len(y.faces)
    on = np.zeros(nf + 1, np.int64); ar = np.zeros(nf + 1, np.int64)
    bakis = {}
    yol = os.path.abspath(cikti).replace('.json', '_t.exr')
    for vi, (az, el) in enumerate(goruntu):
        A, E = math.radians(az), math.radians(el)
        yon = Vector((math.sin(A) * math.cos(E), -math.cos(A) * math.cos(E), math.sin(E)))
        cam_d.ortho_scale = boy; cam.location = m + yon * 12
        cam.rotation_euler = (-yon).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = yol; bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(yol)
        px = np.array(im.pixels[:], np.float32).reshape(-1, 4); bpy.data.images.remove(im)
        ids = np.rint(px[:, 0]).astype(np.int64); bk = px[:, 1] > 0.5
        ok = (ids > 0) & (ids <= nf)
        on += np.bincount(ids[ok & ~bk], minlength=nf + 1); b = np.bincount(ids[ok & bk], minlength=nf + 1); ar += b
        for i in np.nonzero(b)[0]:
            if b[i] > bakis.get(int(i), (0, 0))[0]: bakis[int(i)] = (int(b[i]), az)
    os.remove(yol)
    # faces with a reversed twin on the same corners (double-sided sheets) are fine in the game: skip them
    anah = {}
    def _n(pts):
        n = Vector((0, 0, 0))
        for j in range(len(pts)):
            a_, b_ = Vector(pts[j]), Vector(pts[(j + 1) % len(pts)])
            n += Vector(((a_.y - b_.y) * (a_.z + b_.z), (a_.z - b_.z) * (a_.x + b_.x), (a_.x - b_.x) * (a_.y + b_.y)))
        return n
    for j, (pts, k) in enumerate(y.faces):
        anah.setdefault(tuple(sorted(tuple(round(c * 1e5) for c in p) for p in pts)), []).append(j)
    ikizli = set()
    for js in anah.values():
        if len(js) > 1:
            ns = [_n(y.faces[j][0]) for j in js]
            for a_ in range(len(js)):
                if any(ns[a_].dot(ns[b_]) < 0 for b_ in range(len(js))): ikizli.add(js[a_])
    if os.environ.get('TESHIS_IKIZ'):
        for j in ikizli: ar[j + 1] = 0
    grup = {}
    for i in range(1, nf + 1):
        if ar[i] == 0: continue
        t = KAY[i - 1]
        g_ = grup.setdefault(t, {'arka': 0, 'on': 0, 'yuz': 0, 'ornek': None, 'anahtar': set()})
        g_['arka'] += int(ar[i]); g_['on'] += int(on[i]); g_['yuz'] += 1; g_['anahtar'].add(y.faces[i - 1][1])
        if g_['ornek'] is None or ar[i] > g_['ornek'][0]:
            pts = [Vector(p) for p in y.faces[i - 1][0]]
            c = sum(pts, Vector()) / len(pts)
            g_['ornek'] = (int(ar[i]), [round(c.x, 3), round(c.y, 3), round(c.z, 3)], bakis[i][1], i - 1)
    sira = sorted(grup.items(), key=lambda kv: -kv[1]['arka'])
    with open(cikti, 'w', encoding='utf8') as f:
        json.dump([{'kaynak': k, **{a: (sorted(b) if isinstance(b, set) else b) for a, b in v.items()}} for k, v in sira], f, ensure_ascii=False, indent=1)
    print('TESHIS_TOPLAM', int(ar.sum()))
    for gi, (k, v) in enumerate(sira[:40]):
        print('T%d %7d arka %7d on %4d yuz  %-60s %s orn %s az%s' % (gi, v['arka'], v['on'], v['yuz'], k, ','.join(sorted(v['anahtar']))[:30], v['ornek'][1], v['ornek'][2]))
    yakinlar(sira, nf, kim, me, ob, cikti, cam, cam_d, sc)

def yakinlar(sira, nf, kim, me, ob, cikti, cam, cam_d, sc):
    # close-ups of the worst groups: grey = front faces, magenta = this group's faces seen from behind, orange = other back faces
    NG = int(os.environ.get('TESHIS_YAKIN', '8'))
    if not NG: return
    gr = me.attributes.new('grp', 'FLOAT', 'FACE')
    mat = me.materials[0]; N = mat.node_tree.nodes; L = mat.node_tree.links
    N.clear()
    a = N.new('ShaderNodeAttribute'); a.attribute_name = 'grp'
    g = N.new('ShaderNodeNewGeometry')
    lw = N.new('ShaderNodeVectorMath'); lw.operation = 'DOT_PRODUCT'; lw.inputs[1].default_value = (0.35, -0.5, 0.8)
    L.new(g.outputs['Normal'], lw.inputs[0])
    mr = N.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = -1.2; mr.inputs['From Max'].default_value = 1.2
    mr.inputs['To Min'].default_value = 0.12; mr.inputs['To Max'].default_value = 0.9
    L.new(lw.outputs['Value'], mr.inputs['Value'])
    gri = N.new('ShaderNodeCombineColor')
    for k in range(3): L.new(mr.outputs[0], gri.inputs[k])
    m1 = N.new('ShaderNodeMix'); m1.data_type = 'RGBA'; L.new(a.outputs['Fac'], m1.inputs['Factor'])
    m1.inputs['A'].default_value = (1, 0.45, 0, 1); m1.inputs['B'].default_value = (1, 0, 1, 1)
    m2 = N.new('ShaderNodeMix'); m2.data_type = 'RGBA'; L.new(g.outputs['Backfacing'], m2.inputs['Factor'])
    L.new(gri.outputs[0], m2.inputs['A']); L.new(m1.outputs['Result'], m2.inputs['B'])
    em = N.new('ShaderNodeEmission'); L.new(m2.outputs['Result'], em.inputs[0])
    o = N.new('ShaderNodeOutputMaterial'); L.new(em.outputs[0], o.inputs[0])
    sc.view_settings.view_transform = 'Standard'; sc.render.film_transparent = False
    sc.world.color = (1, 1, 1)
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '8'
    sc.render.resolution_x, sc.render.resolution_y = 520, 400
    sc.cycles.samples = 4
    ciz = []
    olcek = float(os.environ.get('TESHIS_BOY', '0.45'))
    for gi, (k, v) in enumerate(sira[:NG]):
        uyan = set(i for i in range(nf) if KAY[i] == k)
        gr.data.foreach_set('value', [1.0 if (kim[f] in uyan) else 0.0 for f in range(len(kim))])
        me.update()
        c = Vector(v['ornek'][1]); az = v['ornek'][2]
        A, E = math.radians(az), math.radians(30)
        yon = Vector((math.sin(A) * math.cos(E), -math.cos(A) * math.cos(E), math.sin(E)))
        cam_d.ortho_scale = olcek; cam.location = c + yon * 12
        cam.rotation_euler = (-yon).to_track_quat('-Z', 'Y').to_euler()
        yp = os.path.abspath(cikti).replace('.json', '_ty%d.png' % gi)
        sc.render.filepath = yp; bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(yp); ciz.append(np.array(im.pixels[:], np.float32).reshape(400, 520, 4)); bpy.data.images.remove(im); os.remove(yp)
    sut = 4; sat = (len(ciz) + sut - 1) // sut
    pf = np.ones((sat * 400, sut * 520, 4), np.float32)
    for i, p_ in enumerate(ciz):
        r_, c_ = sat - 1 - i // sut, i % sut
        pf[r_ * 400:(r_ + 1) * 400, c_ * 520:(c_ + 1) * 520] = p_
    out = bpy.data.images.new('pf', sut * 520, sat * 400); out.pixels[:] = pf.ravel()
    out.filepath_raw = cikti.replace('.json', '.png'); out.file_format = 'PNG'; out.save()

bina_ortak.calistir = teshis
sys.argv = [sys.argv[0]]
runpy.run_path(betik, run_name='__main__')
