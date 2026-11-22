# Textured, smooth-shaded models (tools/lm-blender/README.md, "Dokulu yol"): faces carry a material key instead of a
# colour; the mesh is welded, shaded smooth with sharp edges by angle, unwrapped, and its procedural materials (ashlar
# stone, lead, gold...) baked with ambient occlusion into one texture. The file asks the game to keep its normals
# (extras yumusak = 1, glb-models.js plainGeo).
import bpy, bmesh, math
import numpy as np

# material key -> (kind, sRGB colour, options)
# (team blue: the game repaints every colour of hue 200-245 with saturation > 0.55 in the player's colour (glb-models.js
#  isTeamBlue), so a blue that must stay blue (glazed tile, paint) is kept out of that range: 'lacivert', 'turkuaz')
MALZEME = {
    # stone
    'tas':      ('tas',  (0.87, 0.82, 0.71), {'tugla': 9.0}),
    'tas_koyu': ('tas',  (0.70, 0.65, 0.56), {'tugla': 9.0}),
    'tas_acik': ('duz',  (0.92, 0.89, 0.82), {}),
    'mermer':   ('duz',  (0.95, 0.94, 0.90), {'leke': 0.04}),
    'kirec':    ('tas',  (0.89, 0.87, 0.81), {}),          # light limestone (Greek, Roman, Egyptian casing)
    'kum':      ('tas',  (0.86, 0.73, 0.52), {}),          # sandstone (Egypt, India, Persia)
    'kum_koyu': ('tas',  (0.72, 0.58, 0.40), {}),
    'kum_acik': ('duz',  (0.92, 0.83, 0.65), {}),
    'kirmizi_tas': ('tas', (0.70, 0.36, 0.27), {}),        # red sandstone (Red Fort, Amber)
    'granit':   ('tas',  (0.63, 0.60, 0.58), {}),          # grey castle stone (England, France, Korea walls)
    'granit_koyu': ('tas', (0.46, 0.44, 0.43), {}),
    'bazalt':   ('duz',  (0.34, 0.33, 0.32), {}),
    'zemin':    ('tas',  (0.80, 0.77, 0.70), {'tugla': 5.0, 'yatay': True}),
    'toprak':   ('duz',  (0.58, 0.47, 0.34), {'leke': 0.08}),
    'cimen':    ('duz',  (0.42, 0.52, 0.27), {'leke': 0.08}),   # turf roof, lawn
    'su':       ('duz',  (0.28, 0.46, 0.52), {'leke': 0.03}),
    # brick, earth, plaster
    'tugla':    ('tas',  (0.68, 0.37, 0.26), {}),
    'tugla_koyu': ('tas', (0.52, 0.28, 0.20), {}),
    'tugla_roma': ('tas', (0.76, 0.53, 0.38), {}),     # Roman fired brick: paler, orange-tan (Pantheon, castra)
    'tugla_roma_koyu': ('tas', (0.60, 0.40, 0.29), {}),
    'kerpic':   ('duz',  (0.74, 0.53, 0.35), {'leke': 0.09}),   # mud brick (Mali, Persia, Mesopotamia)
    'kerpic_koyu': ('duz', (0.60, 0.41, 0.27), {'leke': 0.09}),
    'siva':     ('duz',  (0.94, 0.92, 0.87), {'leke': 0.03}),   # white plaster (Japan, Korea, Spain, Greece)
    'siva_krem': ('duz', (0.91, 0.84, 0.68), {'leke': 0.04}),
    'siva_oker': ('duz', (0.85, 0.63, 0.37), {'leke': 0.05}),
    'siva_kirmizi': ('duz', (0.66, 0.26, 0.20), {'leke': 0.04}),  # Chinese / Kremlin red walls
    # metal, roofs
    'kursun':   ('kursun', (0.55, 0.60, 0.67), {}),
    'kursun2':  ('kursun', (0.50, 0.545, 0.61), {}),     # every other lead sheet (ortak.py kubbe)
    'bakir':    ('duz',  (0.45, 0.66, 0.57), {'leke': 0.06}),   # green copper roof (patina)
    'bakir2':   ('duz',  (0.41, 0.61, 0.53), {'leke': 0.06}),
    'altin':    ('duz',  (0.90, 0.70, 0.28), {'leke': 0.03}),
    'bronz':    ('duz',  (0.62, 0.45, 0.25), {'leke': 0.04}),
    'demir':    ('duz',  (0.30, 0.30, 0.32), {'leke': 0.03}),
    'kiremit':  ('duz',  (0.68, 0.34, 0.22), {}),          # terracotta roof tiles (patterned as courses)
    'kiremit2': ('duz',  (0.62, 0.30, 0.20), {}),
    'kiremit_koyu': ('duz', (0.33, 0.34, 0.37), {'leke': 0.04}),   # dark grey East Asian tiles
    'kiremit_koyu2': ('duz', (0.29, 0.30, 0.33), {'leke': 0.04}),
    'kiremit_sari': ('duz', (0.88, 0.66, 0.20), {'leke': 0.04}),   # imperial yellow glaze (China)
    'kiremit_yesil': ('duz', (0.30, 0.52, 0.36), {'leke': 0.04}),  # green glaze
    'arduvaz':  ('duz',  (0.36, 0.38, 0.43), {'leke': 0.04}),      # slate (France, England)
    'saz':      ('duz',  (0.72, 0.60, 0.37), {'leke': 0.08}),      # thatch
    'saz_koyu': ('duz',  (0.58, 0.47, 0.29), {'leke': 0.08}),
    # wood, lacquer, cloth
    'ahsap':    ('duz',  (0.40, 0.27, 0.17), {}),
    'ahsap_acik': ('duz', (0.62, 0.46, 0.30), {}),
    'ahsap_koyu': ('duz', (0.27, 0.18, 0.12), {}),
    'ahsap_dikey': ('duz', (0.48, 0.33, 0.21), {}),        # vertical boards
    'kutuk':    ('duz',  (0.52, 0.37, 0.24), {}),          # logs
    'lake':     ('duz',  (0.68, 0.17, 0.12), {'leke': 0.03}),     # red lacquer (China, Japan, Korea)
    'lake_koyu': ('duz', (0.42, 0.10, 0.08), {'leke': 0.03}),
    'kece':     ('duz',  (0.93, 0.90, 0.83), {'leke': 0.04}),     # felt (Mongol ger)
    'kumas':    ('duz',  (0.85, 0.80, 0.68), {'leke': 0.04}),     # canvas tent
    # paint, glaze
    'kirmizi':  ('duz',  (0.66, 0.30, 0.22), {'leke': 0.05}),
    'boya_kirmizi': ('duz', (0.72, 0.22, 0.16), {'leke': 0.03}),
    'boya_sari': ('duz', (0.90, 0.72, 0.30), {'leke': 0.03}),
    'boya_yesil': ('duz', (0.24, 0.50, 0.38), {'leke': 0.03}),
    'turkuaz':  ('duz',  (0.18, 0.60, 0.58), {'leke': 0.03}),     # glazed tile (Persia, Timurid)
    'lacivert': ('duz',  (0.28, 0.22, 0.52), {'leke': 0.03}),     # deep blue glaze / paint (kept off team blue)
    'beyaz':    ('duz',  (0.96, 0.95, 0.92), {'leke': 0.02}),
    'koyu':     ('duz',  (0.13, 0.11, 0.10), {'leke': 0.02}),
    'cam':      ('duz',  (0.22, 0.30, 0.34), {'leke': 0.03}),
    'mavi':     ('duz',  (0.10, 0.32, 0.88), {'leke': 0.0, 'aosuz': True}),   # TEAM COLOUR (banners)
}


def srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


_ONBELLEK = {}


def _malzeme(ad):
    m = _ONBELLEK.get(ad)
    try:
        if m and m.name in bpy.data.materials: return m
    except ReferenceError:
        pass
    m = _malzeme_yap(ad); _ONBELLEK[ad] = m; return m


def _malzeme_yap(ad):
    tur, renk, o = MALZEME[ad]
    m = bpy.data.materials.new('m_' + ad)
    m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    bsdf = N.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = 0.9
    lin = [srgb2lin(c) for c in renk] + [1]
    tc = N.new('ShaderNodeTexCoord')
    # colour variation: soft 3D noise
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6.0; nz.inputs['Detail'].default_value = 4.0
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    leke = o.get('leke', 0.07)
    ramp = N.new('ShaderNodeMapRange'); ramp.inputs['To Min'].default_value = 1 - leke; ramp.inputs['To Max'].default_value = 1 + leke
    Lk.new(nz.outputs['Fac'], ramp.inputs['Value'])
    taban = N.new('ShaderNodeRGB'); taban.outputs[0].default_value = lin
    if tur == 'tas':
        # ashlar courses on the walls: brick texture on (x + y, z) (the walls run along the axes); a floor: (x, y)
        sep = N.new('ShaderNodeSeparateXYZ'); Lk.new(tc.outputs['Object'], sep.inputs[0])
        com = N.new('ShaderNodeCombineXYZ')
        if o.get('yatay'):
            Lk.new(sep.outputs['X'], com.inputs['X']); Lk.new(sep.outputs['Y'], com.inputs['Y'])
        else:
            add = N.new('ShaderNodeMath'); add.operation = 'ADD'
            Lk.new(sep.outputs['X'], add.inputs[0]); Lk.new(sep.outputs['Y'], add.inputs[1])
            Lk.new(add.outputs[0], com.inputs['X']); Lk.new(sep.outputs['Z'], com.inputs['Y'])
        br = N.new('ShaderNodeTexBrick')
        br.inputs['Scale'].default_value = o.get('tugla', 9.0)
        br.inputs['Mortar Size'].default_value = 0.012
        br.inputs['Bias'].default_value = 0.0
        br.inputs['Color1'].default_value = [c * 0.97 for c in lin[:3]] + [1]
        br.inputs['Color2'].default_value = [c * 1.05 for c in lin[:3]] + [1]
        br.inputs['Mortar'].default_value = [c * 0.72 for c in lin[:3]] + [1]
        br.offset = 0.5; br.squash = 1.0
        Lk.new(com.outputs[0], br.inputs['Vector'])
        renk_cikis = br.outputs['Color']
    elif tur == 'kursun':
        # lead sheets: faint vertical seams (wave bands on the angle round z) over the noise
        renk_cikis = taban.outputs[0]
        wv = N.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.rings_direction = 'Z'
        wv.inputs['Scale'].default_value = 14.0; wv.inputs['Distortion'].default_value = 0.0
        Lk.new(tc.outputs['Object'], wv.inputs['Vector'])
        mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.93; mr.inputs['To Max'].default_value = 1.03
        Lk.new(wv.outputs['Fac'], mr.inputs['Value'])
        mx0 = N.new('ShaderNodeMix'); mx0.data_type = 'RGBA'; mx0.blend_type = 'MULTIPLY'; mx0.inputs['Factor'].default_value = 1
        Lk.new(taban.outputs[0], mx0.inputs['A']); Lk.new(mr.outputs[0], mx0.inputs['B'])
        renk_cikis = mx0.outputs['Result']
    else:
        renk_cikis = taban.outputs[0]
    mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1
    Lk.new(renk_cikis, mx.inputs['A']); Lk.new(ramp.outputs[0], mx.inputs['B'])
    Lk.new(mx.outputs['Result'], bsdf.inputs['Base Color'])
    return m


def nesne_dokulu(yapi, ad, aci=38):
    """the faces of a Yapi whose colours are material keys -> one welded, smooth-shaded, unwrapped object"""
    anahtarlar = sorted({k for _, k in yapi.faces})
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    for pts, k in yapi.faces:
        vs = [bm.verts.new(p) for p in pts]
        try:
            f = bm.faces.new(vs)
        except ValueError:
            continue
        f.material_index = anahtarlar.index(k)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges[:], dist=1e-7)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='EAR_CLIP')
    bm.to_mesh(me); bm.free()
    for k in anahtarlar:
        me.materials.append(_malzeme(k))
    for p in me.polygons: p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(aci))
    ob = bpy.data.objects.new(ad, me)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.004, area_weight=0.0, scale_to_bounds=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    return ob, anahtarlar


def pisir_ve_aktar(ob, anahtarlar, yol, boyut=2048, ornek=48, ao_guc=0.75):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = ornek
    sc.cycles.device = 'CPU'
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    imgs = {}
    for ad in ('renk', 'ao'):
        im = bpy.data.images.new('pis_' + ad, boyut, boyut, alpha=False, float_buffer=True)
        im.colorspace_settings.name = 'Non-Color' if ad == 'ao' else 'Linear Rec.709'
        imgs[ad] = im
    def hedef(im):
        for m in ob.data.materials:
            nt = m.node_tree
            n = nt.nodes.get('pis_hedef') or nt.nodes.new('ShaderNodeTexImage')
            n.name = 'pis_hedef'; n.image = im
            nt.nodes.active = n
    hedef(imgs['renk'])
    sc.render.bake.use_pass_direct = False; sc.render.bake.use_pass_indirect = False; sc.render.bake.use_pass_color = True
    sc.render.bake.margin = 6
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, margin=6)
    hedef(imgs['ao'])
    sc.world = sc.world or bpy.data.worlds.new('W')
    sc.world.light_settings.distance = 0.35
    bpy.ops.object.bake(type='AO', margin=6)
    W = boyut
    renk = np.array(imgs['renk'].pixels[:], dtype=np.float32).reshape(W, W, 4)
    ao = np.array(imgs['ao'].pixels[:], dtype=np.float32).reshape(W, W, 4)[..., 0:1]
    # team blue (the banner) keeps its colour (the game finds it by colour)
    lin_mavi = np.array([srgb2lin(c) for c in MALZEME['mavi'][1]], dtype=np.float32)
    mavi = (np.abs(renk[..., :3] - lin_mavi).sum(-1, keepdims=True) < 0.06)
    carp = (1 - ao_guc) + ao_guc * ao
    son = renk.copy()
    son[..., :3] = np.where(mavi, renk[..., :3], renk[..., :3] * carp)
    out = bpy.data.images.new('doku', W, W, alpha=False)
    son = np.clip(son, 0, 1)
    rgb = son[..., :3]
    son[..., :3] = np.where(rgb <= 0.0031308, rgb * 12.92, 1.055 * np.power(rgb, 1 / 2.4) - 0.055)   # (a byte image holds sRGB)
    out.pixels[:] = son.ravel()
    # one plain material with the baked texture for the export
    m = bpy.data.materials.new('pismis'); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = 0.9
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = out
    nt.links.new(tx.outputs['Color'], bsdf.inputs['Base Color'])
    ob.data.materials.clear(); ob.data.materials.append(m)
    ob.data['yumusak'] = 1; ob['yumusak'] = 1
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=yol, export_format='GLB', use_selection=True, export_materials='EXPORT', export_yup=True,
                              export_normals=True, export_texcoords=True, export_extras=True,
                              export_image_format='JPEG', export_jpeg_quality=72)
    return out


def onizle_dokulu(yol, merkez, boy, aci=(-35, 32), cozunurluk=(1400, 900)):
    """an EEVEE render with a sun and soft sky (closer to the game than workbench)"""
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
    from mathutils import Vector
    az, el = math.radians(aci[0]), math.radians(aci[1])
    cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'; cam_d.ortho_scale = boy
    cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam)
    m = Vector(merkez)
    yon = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.location = m + yon * 10
    cam.rotation_euler = (-yon).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = cozunurluk
    sc.render.filepath = yol
    sc.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)


def parca_nesne(yuzler, ad, aci=38):
    """a few faces (material keys) as their own welded, smooth-shaded object (the live view builds the model from these)"""
    anahtarlar = sorted({k for _, k in yuzler})
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    for pts, k in yuzler:
        try:
            f = bm.faces.new([bm.verts.new(p) for p in pts])
        except ValueError:
            continue
        f.material_index = anahtarlar.index(k)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    bm.to_mesh(me); bm.free()
    for k in anahtarlar:
        me.materials.append(_malzeme(k))
    for p in me.polygons: p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(aci))
    ob = bpy.data.objects.new(ad, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


# ---------------- detail mode (sharp at any zoom) ----------------
# Colours and baked AO go into the vertex colours; the texture is one small tiling pattern of stone courses (512 px)
# box-projected in model units over the stone faces; every other material samples a plain spot of it (white), so
# only its vertex colour shows. The game multiplies the two (glb-models.js, extras detay = 1).
# key -> (pattern scale, stretch along the course, vertical): the one tile serves every coursed material - ashlar at
# scale 1, bricks small, roof tiles as thin courses running along the eaves, boards and logs stretched long, upright
# boards turned. A wall / roof face lays its courses along its own horizontal edge (u: along it, v: up the slope), a
# flat face in plan (x, y): the courses stay level on any wall and parallel to the eaves on any roof.
DESENLI = {
    'tas': (1.0, 1, 0), 'tas_koyu': (1.0, 1, 0), 'zemin': (1.6, 1, 0),
    'kirec': (1.1, 1, 0), 'kum': (1.2, 1, 0), 'kum_koyu': (1.2, 1, 0), 'kirmizi_tas': (1.0, 1, 0),
    'granit': (0.9, 1, 0), 'granit_koyu': (0.9, 1, 0),
    'tugla': (0.42, 1, 0), 'tugla_koyu': (0.42, 1, 0), 'tugla_roma': (0.42, 1, 0), 'tugla_roma_koyu': (0.42, 1, 0),
    'kiremit': (0.36, 1.6, 0), 'kiremit2': (0.36, 1.6, 0), 'kiremit_koyu': (0.36, 1.6, 0), 'kiremit_koyu2': (0.36, 1.6, 0),
    'kiremit_sari': (0.36, 1.6, 0), 'kiremit_yesil': (0.36, 1.6, 0), 'arduvaz': (0.3, 1.3, 0),
    'ahsap': (0.5, 4, 0), 'ahsap_acik': (0.5, 4, 0), 'ahsap_koyu': (0.5, 4, 0), 'kutuk': (0.6, 6, 0),
    'ahsap_dikey': (0.5, 4, 1),
}
DUZ_TON = ('tas', 'tas_koyu', 'tas_acik', 'zemin', 'kirec', 'kum', 'kum_koyu', 'kum_acik', 'kirmizi_tas', 'granit',
           'granit_koyu', 'tugla', 'tugla_koyu', 'tugla_roma', 'tugla_roma_koyu', 'siva', 'siva_krem', 'kerpic', 'kerpic_koyu')   # (a shade per flat face)
KARO = 0.11                                              # model units per tile (4 courses)
DUZ_UV = (40 / 512, 1 - 25 / 512)                        # the plain (white, grainless) spot of the tile's first block (Blender UV: v up)


def karo_desen(boyut=512, tohum=5):
    """a seamless tile of ashlar: 4 courses of blocks with offset joints, light mortar lines, faint grain (grey ~1)"""
    rng = np.random.default_rng(tohum)
    S = boyut
    img = np.ones((S, S), np.float32)
    sira = S // 4
    harc = max(3, S // 128)
    for r in range(4):
        y0 = r * sira
        # block widths for this course (wrap round), first joint offset per course
        x = int(rng.integers(0, S // 3)) if r else 0
        bloklar = []
        while True:
            w = int(rng.integers(S // 6, S // 3))
            bloklar.append((x, w)); x += w
            if x - bloklar[0][0] >= S - S // 6: break
        # last block closes the course exactly
        bas = bloklar[0][0]
        x_son, _ = bloklar[-1]
        bloklar[-1] = (x_son, bas + S - x_son)
        for i, (bx, bw) in enumerate(bloklar):
            ton = 1.0 if (r == 0 and i == 0) else float(rng.uniform(0.9, 1.04))
            xs = (np.arange(bx, bx + bw) % S)
            img[y0:y0 + sira, xs] = ton
            img[y0:y0 + sira, (bx + np.arange(harc)) % S] = 0.74           # vertical joint
        img[y0:y0 + harc, :] = 0.74                                          # bed joint
    # grain (kept off the plain spot of block 0)
    tane = rng.normal(0, 0.018, (S, S)).astype(np.float32)
    tane[harc + 2:harc + 40, harc + 2:harc + 70] = 0
    img = np.clip(img + tane, 0, 1)
    im = bpy.data.images.new('karo', S, S, alpha=False)
    rgba = np.ones((S, S, 4), np.float32)
    s = np.where(img <= 0.0031308, img * 12.92, 1.055 * np.power(img, 1 / 2.4) - 0.055)   # (the pattern is sRGB)
    rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = s[::-1]    # (Blender images start at the bottom row)
    im.pixels[:] = rgba.ravel()
    im.file_format = 'PNG'
    im.pack()
    return im


def detayli_aktar(ob, anahtarlar, yol, ornek=96, ao_guc=0.72, tohum=9):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = ornek; sc.cycles.device = 'CPU'
    me = ob.data
    rng = np.random.default_rng(tohum)
    # base colour per face corner (material colour, a little per-face variation)
    n_loop = len(me.loops)
    renk = np.zeros((n_loop, 4), np.float32); renk[:, 3] = 1
    mavi = np.zeros(n_loop, bool)
    lin = {k: np.array([srgb2lin(c) for c in MALZEME[k][1]], np.float32) for k in anahtarlar}
    for p in me.polygons:
        k = anahtarlar[p.material_index]
        # (a shade per face only on flat stone: on a curved surface it made a mosaic of triangles)
        oy = MALZEME[k][2].get('leke', 0.05) * 0.6 if k in DUZ_TON else 0
        c = lin[k] * float(1 + rng.uniform(-oy, oy))
        renk[p.loop_start:p.loop_start + p.loop_total, :3] = c
        if k == 'mavi': mavi[p.loop_start:p.loop_start + p.loop_total] = True
    # ambient occlusion baked into the vertex colours
    for a in list(me.color_attributes): me.color_attributes.remove(a)
    ao = me.color_attributes.new('AO', 'FLOAT_COLOR', 'CORNER')
    me.color_attributes.active_color = ao
    sc.render.bake.target = 'VERTEX_COLORS'
    sc.world = sc.world or bpy.data.worlds.new('W')
    sc.world.light_settings.distance = 0.3
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.bake(type='AO')
    a = np.zeros(n_loop * 4, np.float32); ao.data.foreach_get('color', a)
    a = a.reshape(-1, 4)[:, :1]
    carp = (1 - ao_guc) + ao_guc * a
    son = renk.copy()
    son[:, :3] = np.where(mavi[:, None], renk[:, :3], renk[:, :3] * carp)
    me.color_attributes.remove(ao)
    col = me.color_attributes.new('Col', 'FLOAT_COLOR', 'CORNER')
    col.data.foreach_set('color', son.ravel())
    me.color_attributes.active_color = col
    me.color_attributes.render_color_index = me.color_attributes.active_color_index
    # UVs: stone faces box-projected in model units, the rest on the plain spot
    while me.uv_layers: me.uv_layers.remove(me.uv_layers[0])
    uvl = me.uv_layers.new(name='UV')
    uv = np.zeros((n_loop, 2), np.float32)
    co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    lv = np.zeros(n_loop, np.int32); me.loops.foreach_get('vertex_index', lv)
    for p in me.polygons:
        k = anahtarlar[p.material_index]
        s, e = p.loop_start, p.loop_start + p.loop_total
        if k in DESENLI:
            olc, uzat, dikey = DESENLI[k]
            n = p.normal
            c = co[lv[s:e]] / (KARO * olc)
            if abs(n.z) > 0.94:          # flat (paving, a flat roof): in plan
                q = c[:, [0, 1]].copy()
            else:                        # wall / roof: u along the face's level edge, v up its slope
                t = np.array([-n.y, n.x], np.float32); t /= max(1e-6, float(np.hypot(t[0], t[1])))
                q = np.stack([c[:, 0] * t[0] + c[:, 1] * t[1], c[:, 2] / max(0.3, (1 - n.z * n.z) ** 0.5)], 1)
            q[:, 0] /= uzat              # (stretch: longer blocks / boards)
            uv[s:e] = q[:, ::-1] if dikey else q
        else:
            uv[s:e] = DUZ_UV
    uvl.data.foreach_set('uv', uv.ravel())
    # one material: the tile as base colour (the exporter writes the vertex colours as COLOR_0, which multiplies it)
    m = bpy.data.materials.new('detay'); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = 0.92
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = karo_desen()
    ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1
    nt.links.new(tx.outputs['Color'], mx.inputs['A']); nt.links.new(ca.outputs['Color'], mx.inputs['B'])
    nt.links.new(mx.outputs['Result'], bsdf.inputs['Base Color'])
    me.materials.clear(); me.materials.append(m)
    for p in me.polygons: p.material_index = 0
    me['yumusak'] = 1; me['detay'] = 1; ob['yumusak'] = 1; ob['detay'] = 1
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True)
    kw = dict(filepath=yol, export_format='GLB', use_selection=True, export_materials='EXPORT', export_yup=True,
              export_normals=True, export_texcoords=True, export_extras=True, export_image_format='AUTO')
    try:
        bpy.ops.export_scene.gltf(**kw, export_vertex_color='ACTIVE')
    except TypeError:
        bpy.ops.export_scene.gltf(**kw, export_colors=True)
    return ob
