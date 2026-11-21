# Opens Blender WITH its window on a rigged unit and plays its actions one after another (the name in the viewport
# header), looping; the armature is shown over the body so the bones can be seen moving.
# blender --factory-startup --python tools/lm-blender/birim_canli.py -- piyade
import bpy, sys, os, importlib, math
from mathutils import Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import argumanlar
from karakter import iskelet, bagla, eylem

AD = argumanlar()[0]
mod = importlib.import_module(AD)
durum = {'i': 0, 'aci': -0.5}
ADLAR = {'bekle': 'Bekleme', 'yuru': 'Yürüme', 'saldir': 'Saldırı', 'ol': 'Ölüm'}


def gorunum():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'VIEW_3D':
                return win, area, next(r for r in area.regions if r.type == 'WINDOW')
    return None, None, None


def kur():
    win, area, reg = gorunum()
    if not area: return 0.3
    with bpy.context.temp_override(window=win, area=area, region=reg):
        for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)
        govde = mod.k.nesne(AD)
        arm = iskelet(AD, mod.kemik)
        bagla(govde, arm)
        for ad, kr in mod.ANIM: eylem(arm, ad, kr)
        arm.show_in_front = True
        arm.data.display_type = 'STICK'
        sp = area.spaces.active
        sp.shading.type = 'MATERIAL'
        sp.show_gizmo = False
        try:
            sp.show_region_toolbar = False; sp.show_region_ui = False
        except Exception:
            pass
        r3d = sp.region_3d
        r3d.view_perspective = 'PERSP'
        r3d.view_location = (0, 0, 0.95)
        r3d.view_distance = 4.2
        r3d.view_rotation = Euler((math.radians(75), 0, durum['aci']), 'XYZ').to_quaternion()
        sc = bpy.context.scene
        sc.render.fps = 24
        durum['arm'] = arm
        sirada()
        bpy.ops.screen.animation_play()
    bpy.app.timers.register(degistir, first_interval=5.0)
    bpy.app.timers.register(don, first_interval=0.05)
    return None


def sirada():
    arm = durum['arm']; ad, kr = mod.ANIM[durum['i'] % len(mod.ANIM)]
    act = bpy.data.actions[ad]
    arm.animation_data.action = act
    sc = bpy.context.scene
    sc.frame_start = int(kr[0][0]); sc.frame_end = int(kr[-1][0]) + (12 if ad == 'ol' else 0)
    sc.frame_current = sc.frame_start
    _, area, _ = gorunum()
    if area:
        area.header_text_set('%s · %s animasyonu  (iskelet çizgileri görünür; orta tuş: çevir, tekerlek: yakınlaş)' % (AD.capitalize(), ADLAR.get(ad, ad)))


def degistir():
    durum['i'] += 1
    sirada()
    return 5.0


def don():
    _, area, _ = gorunum()
    if not area: return 0.05
    durum['aci'] += 0.002
    area.spaces.active.region_3d.view_rotation = Euler((math.radians(75), 0, durum['aci']), 'XYZ').to_quaternion()
    return 0.03


bpy.app.timers.register(kur, first_interval=1.0)
