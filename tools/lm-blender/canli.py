# Live view: opens Blender WITH its window and builds a model part by part in front of you (sections named in the
# viewport header, the view slowly circling), then bakes the texture and exports the file, and shows the result.
# blender --factory-startup --python tools/lm-blender/canli.py -- suleymaniye <out.glb> [hiz]
#   hiz: speed multiplier (1 = about a minute of building)
import bpy, sys, os, math, importlib, time
from mathutils import Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import argumanlar
import doku

arg = argumanlar()
AD, CIKIS = arg[0], os.path.abspath(arg[1])
HIZ = float(arg[2]) if len(arg) > 2 else 1.0
mod = importlib.import_module(AD)
y = mod.y
BOLUM = getattr(y, 'bolumler', [(0, AD)]) + [(len(y.faces), None)]
PARCA = max(20, int(len(y.faces) / (220 / HIZ)))      # faces per step (~220 steps)
ADIM = 0.12 / HIZ
durum = {'i': 0, 'b': 0, 'parcalar': [], 'aci': -0.6, 'bitti': False}


def gorunum():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'VIEW_3D':
                reg = next(r for r in area.regions if r.type == 'WINDOW')
                return win, area, reg
    return None, None, None


def yaz(metin):
    _, area, _ = gorunum()
    if area:
        area.header_text_set(metin)
        area.tag_redraw()


def kamera(aci, uzak=4.2, yuk=math.radians(58)):
    _, area, _ = gorunum()
    if not area: return
    r3d = area.spaces.active.region_3d
    r3d.view_perspective = 'PERSP'
    r3d.view_location = getattr(mod, 'ODAK', (0, 0.1, 0.35))
    r3d.view_distance = uzak
    r3d.view_rotation = Euler((yuk, 0, aci), 'XYZ').to_quaternion()


def hazirla():
    win, area, reg = gorunum()
    if not area:
        return 0.3          # (the window is not up yet)
    with bpy.context.temp_override(window=win, area=area, region=reg):
        for ob in list(bpy.data.objects):
            bpy.data.objects.remove(ob)
        sp = area.spaces.active
        sp.shading.type = 'MATERIAL'
        sp.overlay.show_floor = True
        sp.overlay.show_axis_x = sp.overlay.show_axis_y = False
        sp.show_gizmo = False
        for r in area.regions:
            if r.type in ('UI', 'TOOLS'):
                pass
        try:
            sp.show_region_toolbar = False; sp.show_region_ui = False
        except Exception:
            pass
    kamera(durum['aci'])
    yaz('%s · başlıyor (%d yüz)' % (AD, len(y.faces)))
    bpy.app.timers.register(adim, first_interval=1.5)
    return None


def adim():
    i = durum['i']
    if i >= len(y.faces):
        bpy.app.timers.register(bitir, first_interval=0.8)
        return None
    # the current section and where it ends
    while BOLUM[durum['b'] + 1][0] <= i: durum['b'] += 1
    bas, ad = BOLUM[durum['b']]
    son = BOLUM[durum['b'] + 1][0]
    j = min(i + PARCA, son)
    ob = doku.parca_nesne(y.faces[i:j], 'parca_%04d' % len(durum['parcalar']))
    durum['parcalar'].append(ob)
    durum['i'] = j
    durum['aci'] += 0.006 * HIZ
    kamera(durum['aci'])
    yuzde = 100 * j // len(y.faces)
    yaz('%s · %s · %%%d' % (AD, ad or '', yuzde))
    return ADIM * (6 if j == son else 1)   # a short pause at the end of each section


def bitir():
    win, area, reg = gorunum()
    yaz('%s · gölgeler pişiriliyor, taş deseni seriliyor… pencere birkaç saniye donabilir' % AD)
    bpy.app.timers.register(pisir, first_interval=0.5)
    return None


def pisir():
    win, area, reg = gorunum()
    with bpy.context.temp_override(window=win, area=area, region=reg):
        for ob in durum['parcalar']:
            bpy.data.objects.remove(ob)
        ob, anahtar = doku.nesne_dokulu(y, 'lm_' + AD)
        doku.detayli_aktar(ob, anahtar, CIKIS)
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
    yaz('%s · bitti: %d üçgen, dosya yazıldı. Fareyle çevirip bakabilirsin.' % (AD, sum(len(p.vertices) - 2 for p in ob.data.polygons)))
    durum['bitti'] = True
    bpy.app.timers.register(don, first_interval=0.05)
    return None


def don():
    durum['aci'] += 0.004
    kamera(durum['aci'])
    return 0.03 if durum['aci'] < 6.5 else None   # one slow turn round the finished model, then it is yours


bpy.app.timers.register(hazirla, first_interval=1.0)
