# Shared helpers for the Frankish landmarks (lm_degirmenkoy, lm_motte, lm_aachen, lm_turnuva): an oriented box,
# half-timbering that leaves the openings clear, a half-timbered village house, a timber barn, a palisade of pointed
# logs, a village church with a west tower, a horse, a knight, people, a cross, ground pieces with earthen sides.
import math
from mathutils import Vector
from parcalar import *


def kutu3(y, c, ex, ey, ez, sx, sy, sz, key, yuzler=None):
    """a box centred at c along three (any) axes, sizes sx, sy, sz; every face wound outward. yuzler: which of
    '+x -x +y -y +z -z' to draw (default all)"""
    c = Vector(c); ex, ey, ez = Vector(ex).normalized(), Vector(ey).normalized(), Vector(ez).normalized()
    P = lambda i, j, k: c + ex * (sx / 2 * i) + ey * (sy / 2 * j) + ez * (sz / 2 * k)
    yz = yuzler or ('+x', '-x', '+y', '-y', '+z', '-z')
    for ad, ax, q in (('+x', ex, [P(1, -1, -1), P(1, 1, -1), P(1, 1, 1), P(1, -1, 1)]),
                      ('-x', -ex, [P(-1, -1, -1), P(-1, 1, -1), P(-1, 1, 1), P(-1, -1, 1)]),
                      ('+y', ey, [P(-1, 1, -1), P(1, 1, -1), P(1, 1, 1), P(-1, 1, 1)]),
                      ('-y', -ey, [P(-1, -1, -1), P(1, -1, -1), P(1, -1, 1), P(-1, -1, 1)]),
                      ('+z', ez, [P(-1, -1, 1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, 1)]),
                      ('-z', -ez, [P(-1, -1, -1), P(1, -1, -1), P(1, 1, -1), P(-1, 1, -1)])):
        if ad in yz:
            y.yuz_yon(q, key, ax)


def levha(y, pts, key, yon, kil=0.0012):
    """a thin sheet (cloth, board) seen from both sides: the face, its back a hair behind and the rims"""
    pts = [Vector(p) for p in pts]; yon = Vector(yon).normalized()
    arka = [p - yon * kil for p in pts]
    y.yuz_yon(pts, key, yon)
    y.yuz_yon(arka, key, -yon)
    c = sum(pts, Vector()) / len(pts)
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        m = (pts[i] + pts[j]) / 2
        y.yuz_yon([pts[i], pts[j], arka[j], arka[i]], key, m - c)


def zemin_blok(y, x0, x1, y0, y1, z, ust='cimen', yan='toprak', yanlar='onarkasagsol', z_alt=0.0):
    """a block of ground: its top and the chosen earthen sides (on -y, arka +y, sag +x, sol -x)"""
    y.yuz_yon([V(x0, y0, z), V(x1, y0, z), V(x1, y1, z), V(x0, y1, z)], ust, Z)
    if 'on' in yanlar: duz_duvar(y, V(x0, y0), V(x1, y0), z_alt, z, yan)
    if 'sag' in yanlar: duz_duvar(y, V(x1, y0), V(x1, y1), z_alt, z, yan)
    if 'arka' in yanlar: duz_duvar(y, V(x1, y1), V(x0, y1), z_alt, z, yan)
    if 'sol' in yanlar: duz_duvar(y, V(x0, y1), V(x0, y0), z_alt, z, yan)


def yari_ahsap(y, a, b, z0, z1, bos=(), key='ahsap_koyu', aralik=0.045, en=0.006, capraz=True, orta=True):
    """half-timbering a->b standing just proud of the wall (faces the right): posts on bay lines, sill, head and mid
    rails, braces in the bays; bos: (u0, u1, v0, v1) openings (0..1 along, bottom / top above z0) that the posts,
    rails and braces keep clear of"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    o = nc * (en * 0.35)
    n = max(1, int(round(L / aralik)))
    pad = en * 0.6 / L
    us = [i / n for i in range(n + 1)]
    for u0, u1, v0, v1 in bos:   # posts at the openings' sides
        us += [u0 - pad, u1 + pad]
    us = sorted(set(round(u, 4) for u in us if -1e-6 <= u <= 1 + 1e-6))
    def acikta(u):
        return any(u0 - pad * 0.5 < u < u1 + pad * 0.5 for u0, u1, v0, v1 in bos)
    P = lambda u, zz: a + e * (u * L) + o + Z * zz
    for u in us:
        if not acikta(u):
            cubuk(y, P(u, z0), P(u, z1), en, key, en * 0.7)
    cubuk(y, P(0, z1 - en / 2), P(1, z1 - en / 2), en, key, en * 0.7)
    zm = (z0 + z1) / 2
    for zz in ([z0 + en / 2] + ([zm] if orta else [])):
        kes = sorted((u0 - pad, u1 + pad) for u0, u1, v0, v1 in bos if z0 + v0 - en < zz < z0 + v1 + en)
        bas = 0.0
        for k0, k1 in kes + [(1.0, 1.0)]:
            if k0 > bas + 1e-4:
                cubuk(y, P(bas, zz), P(min(1.0, k0), zz), en, key, en * 0.7)
            bas = max(bas, k1)
    if capraz:
        for i in range(len(us) - 1):
            ua, ub = us[i], us[i + 1]
            if ub - ua < 0.5 / n or acikta((ua + ub) / 2) or i % 2:
                continue
            cubuk(y, P(ua, z0 + en), P(ub, zm - en / 2), en * 0.85, key, en * 0.55)


def ev(y, cx, cy, z, w, d, h, aci=0.0, cati='saz', tohum=0, kapi_u=0.5, baca=True, pencere=True, cati_h=None,
       duvar='siva_krem', ahsap='ahsap_koyu', taban='granit'):
    """a half-timbered village house, w along its x (ridge along the longer side), door on its front (-y), small
    shuttered windows, a stone footing, a thatched (saz) or tiled (kiremit) or slate (arduvaz) gable roof and a
    chimney. Returns the ridge z"""
    if d > w: w, d = d, w   # (the ridge runs along x)
    with parca(y, (cx, cy, z), aci):
        kutu(y, V(-w / 2 - 0.006, -d / 2 - 0.006, -0.01), X, w + 0.012, d + 0.012, 0.022, taban, 'onarkasagsolust')
        z0 = 0.012
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        H = h - z0
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
            bos = []
            # openings: the door on the front, windows elsewhere
            if i == 0:
                du = 0.05 / L
                bos.append((kapi_u - du / 2, kapi_u + du / 2, H * 0.78, 'kapi'))
                if pencere:
                    for u in ((0.18, 0.82) if L > 0.15 else (0.2,)):
                        if abs(u - kapi_u) > du:
                            bos.append((u - 0.022 / L, u + 0.022 / L, H * 0.74, 'p'))
            elif pencere and (i == 2 and L > 0.15 or i in (1, 3) and (tohum + i) % 2 == 0):
                for u in ((0.33, 0.67) if L > 0.2 else (0.5,)):
                    bos.append((u - 0.02 / L, u + 0.02 / L, H * 0.72, 'p'))
            bos.sort()
            # the wall, bay by bay
            u = 0.0
            m = 0.006 / L
            for u0, u1, v1, tur in bos:
                if u0 - m > u: duz_duvar(y, a.lerp(b, u), a.lerp(b, u0 - m), z0, h, duvar)
                v0 = 0.0 if tur == 'kapi' else H * 0.4
                bw = u1 - u0 + 2 * m
                dikdortgen_acik(y, a.lerp(b, u0 - m), a.lerp(b, u1 + m), z0, H, m / bw, 1 - m / bw, v0, v1,
                                (duvar, ahsap, 'ahsap_acik', 'ahsap_dikey' if tur == 'kapi' else 'koyu'), derin=0.008)
                if tur == 'p':   # shutters, open against the wall
                    for s, uu in ((-1, u0), (1, u1)):
                        p = a.lerp(b, uu) + e * (s * 0.011)
                        kutu3(y, p + nc * 0.0035 + Z * (z0 + (v0 + v1) / 2), e, nc, Z, 0.017, 0.003, v1 - v0, 'ahsap' if tohum % 2 else 'boya_yesil')
                u = u1 + m
            if u < 1: duz_duvar(y, a.lerp(b, u), b, z0, h, duvar)
            yari_ahsap(y, a, b, z0, h, [(u0, u1, 0.0 if tur == 'kapi' else H * 0.4, v1) for u0, u1, v1, tur in bos], ahsap)
        mk = {'saz': 'saz_koyu', 'kiremit': 'kiremit2', 'arduvaz': 'arduvaz'}.get(cati, cati)
        ch = cati_h or d * 0.85
        zr = cati_besik(y, -w / 2, w / 2, -d / 2, d / 2, h, ch, 0.022 if cati == 'saz' else 0.016, cati, mk, ucluk_key=duvar,
                        alt_key='ahsap_koyu', ns=5, nr=5, uc_sacak=0.014, mahya_en=0.016 if cati == 'saz' else 0.01)
        # the gable's timbers: a king post and two struts
        for sx in (-1, 1):
            xg = sx * (w / 2 + 0.003)
            top = V(xg, 0, h + ch - 0.016)
            cubuk(y, V(xg, 0, h), top, 0.006, ahsap, 0.004)
            for sy in (-1, 1):
                cubuk(y, V(xg, sy * d * 0.42, h + 0.004), V(xg, 0, h + ch * 0.55), 0.005, ahsap, 0.004)
            cubuk(y, V(xg, -d / 2, h + 0.003), V(xg, d / 2, h + 0.003), 0.006, ahsap, 0.004)
        if baca:
            bx = w * (0.28 if tohum % 2 else -0.28)
            kutu_merkez(y, (bx, d * 0.12), 0.03, 0.03, ch * 0.95 + 0.03, 'tas_koyu', z0=h)
            kutu_merkez(y, (bx, d * 0.12), 0.036, 0.036, 0.008, 'tas', z0=h + ch * 0.95 + 0.03)
        return z + zr


def ambar(y, cx, cy, z, w, d, h, aci=0.0, cati='saz', cati_h=None):
    """a timber barn: a stone footing, vertical-board walls between posts, great double doors standing open on the
    long front side (a dark threshing floor inside), a high thatched roof. Returns the ridge z"""
    with parca(y, (cx, cy, z), aci):
        kutu(y, V(-w / 2 - 0.006, -d / 2 - 0.006, -0.01), X, w + 0.012, d + 0.012, 0.02, 'granit', 'onarkasagsolust')
        z0 = 0.01
        k = dikdortgen(-w / 2, w / 2, -d / 2, d / 2)
        for i in range(4):
            a, b = k[i], k[(i + 1) % 4]
            L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
            if i == 0:
                dikdortgen_acik(y, a, b, z0, h - z0, 0.36, 0.64, 0.0, (h - z0) * 0.86, ('ahsap_dikey', 'ahsap_koyu', 'ahsap', 'koyu'), derin=0.03)
                # the two door leaves swung open against the wall
                dw = L * 0.14
                for s, uu in ((-1, 0.36), (1, 0.64)):
                    p = a.lerp(b, uu)
                    kutu3(y, p + e * (s * dw / 2) + nc * 0.006 + Z * (z0 + (h - z0) * 0.43), e, nc, Z, dw, 0.006, (h - z0) * 0.84, 'ahsap_acik')
                    for t in (0.2, 0.8):
                        kutu3(y, p + e * (s * dw / 2) + nc * 0.0105 + Z * (z0 + (h - z0) * 0.86 * t), e, nc, Z, dw * 0.96, 0.003, 0.008, 'ahsap_koyu')
            else:
                duz_duvar(y, a, b, z0, h, 'ahsap_dikey')
            n = max(1, int(round(L / 0.07)))
            for j in range(n + 1):
                uu = j / n
                if i == 0 and 0.3 < uu < 0.7: continue
                p = a.lerp(b, uu) + nc * 0.003
                cubuk(y, p + Z * z0, p + Z * h, 0.009, 'ahsap_koyu', 0.006)
            cubuk(y, a + nc * 0.003 + Z * (h - 0.005), b + nc * 0.003 + Z * (h - 0.005), 0.01, 'ahsap_koyu', 0.006)
            cubuk(y, a + nc * 0.003 + Z * (z0 + 0.005), b + nc * 0.003 + Z * (z0 + 0.005), 0.01, 'ahsap_koyu', 0.006)
        ch = cati_h or d * 0.9
        zr = cati_besik(y, -w / 2, w / 2, -d / 2, d / 2, h, ch, 0.03, cati, 'saz_koyu' if cati == 'saz' else cati, ucluk_key='ahsap_dikey',
                        alt_key='ahsap_koyu', ns=7, nr=6, uc_sacak=0.018, mahya_en=0.018)
        # an owl hole in each gable and a hay door
        for sx in (-1, 1):
            xg = sx * (w / 2 + 0.002)
            y.yuz_yon([V(xg, -0.018, h + ch * 0.28), V(xg, 0.018, h + ch * 0.28), V(xg, 0.018, h + ch * 0.52), V(xg, -0.018, h + ch * 0.52)], 'koyu', V(sx, 0))
        return z + zr


def palisad(y, yol, zf, h, adim=0.024, r=0.011, tohum=0, kapali=False, gecit=(), yuruyus=True, key='kutuk'):
    """a palisade of pointed upright logs along a polyline (or closed CCW polygon, logs on the line), each standing on
    the ground zf(x, y); a rail and a wall walk on posts on the inner (left) side. gecit: (s0, s1) arc-length gaps
    left open (gates, a bridge)"""
    pts = [V(p[0], p[1]) for p in yol]
    if kapali: pts = pts + [pts[0]]
    seg = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum((b - a).length for a, b in seg)
    def at(s):
        for a, b in seg:
            l = (b - a).length
            if s <= l + 1e-9: return a.lerp(b, s / max(l, 1e-9)), (b - a).normalized()
            s -= l
        a, b = seg[-1]; return b, (b - a).normalized()
    n = int(L / adim)
    acik = lambda s: any(s0 <= s <= s1 for s0, s1 in gecit)
    for k in range(n + (0 if kapali else 1)):
        s = L * k / n
        if acik(s): continue
        p, e = at(s)
        z = zf(p.x, p.y)
        hh = h * (0.92 + 0.08 * ((k * 7 + tohum) % 5) / 4)
        y.prizma((p.x, p.y), r, z - 0.02, z + hh, key, n=6, ust=False)
        y.koni((p.x, p.y), r, z + hh, r * 2.0, 'ahsap', n=6)
    # the rails behind and the wall walk on posts, segment by segment (skipping the gaps)
    if not yuruyus: return
    m = max(2, int(L / 0.06))
    for k in range(m):
        s0, s1 = L * k / m, L * (k + 1) / m
        if acik(s0) or acik(s1) or acik((s0 + s1) / 2): continue
        p0, e0 = at(s0); p1, e1 = at(s1)
        n0, n1 = V(-e0.y, e0.x), V(-e1.y, e1.x)
        z0, z1 = zf(p0.x, p0.y), zf(p1.x, p1.y)
        ra, rb = p0 + n0 * (r * 1.3), p1 + n1 * (r * 1.3)
        cubuk(y, ra + Z * (z0 + h * 0.62), rb + Z * (z1 + h * 0.62), 0.008, 'ahsap_koyu', 0.006)
        cubuk(y, ra + Z * (z0 + h * 0.2), rb + Z * (z1 + h * 0.2), 0.008, 'ahsap_koyu', 0.006)
        wa, wb = p0 + n0 * (r * 1.3 + 0.004), p1 + n1 * (r * 1.3 + 0.004)
        ww = 0.042
        zw0, zw1 = z0 + h * 0.42, z1 + h * 0.42
        q = [wa + Z * zw0, wb + Z * zw1, wb + n1 * ww + Z * zw1, wa + n0 * ww + Z * zw0]
        y.yuz_yon(q, 'ahsap', Z)
        y.yuz_yon([q[0] - Z * 0.007, q[1] - Z * 0.007, q[2] - Z * 0.007, q[3] - Z * 0.007], 'ahsap_koyu', -Z)
        y.yuz_yon([q[3], q[2], q[2] - Z * 0.007, q[3] - Z * 0.007], 'ahsap_koyu', n0)
        y.yuz_yon([q[0], q[1], q[1] - Z * 0.007, q[0] - Z * 0.007], 'ahsap_koyu', -n0)
        y.yuz_yon([q[0], q[3], q[3] - Z * 0.007, q[0] - Z * 0.007], 'ahsap_koyu', -e0)
        y.yuz_yon([q[1], q[2], q[2] - Z * 0.007, q[1] - Z * 0.007], 'ahsap_koyu', e1)
        if k % 2 == 0:
            pp = wa + n0 * (ww - 0.006)
            cubuk(y, pp + Z * (z0 - 0.01), pp + Z * (zw0 - 0.007), 0.007, 'ahsap_koyu')


def hac(y, cx, cy, z, h=0.05, key='demir'):
    """a cross on a small knob (church spire, gable)"""
    kure(y, (cx, cy, z + h * 0.1), h * 0.12, key, n=6, kat=3)
    kutu_merkez(y, (cx, cy), h * 0.1, h * 0.1, h * 0.85, key, z0=z + h * 0.15)
    cubuk(y, V(cx - h * 0.3, cy, z + h * 0.72), V(cx + h * 0.3, cy, z + h * 0.72), h * 0.09, key)
    return z + h


def koy_kilisesi(y, cx, cy, z, aci=0.0, s=1.0, cati='arduvaz', duvar='kirec', kose='granit', kule_h=0.44, kule_cati=0.3):
    """a Romanesque village church: a nave (round-headed windows high up, a corbel table under the eaves, slate or
    tile roof), a round apse with a half-cone roof at the east (+y local), a square west tower (-y local) with a
    portal, string courses, paired belfry arches, a steep pyramid spire and a cross. Returns the spire's tip z"""
    with parca(y, (cx, cy, z), aci, s):
        nw, nl, nh = 0.11, 0.36, 0.2
        # plinth
        kutu(y, V(-nw - 0.008, -0.008, -0.01), X, 2 * nw + 0.016, nl + 0.016, 0.022, kose, 'onarkasagsolust')
        z0 = 0.012
        # nave walls: long sides with three windows, gables
        for (a, b, n) in ((V(nw, 0), V(nw, nl), 3), (V(-nw, nl), V(-nw, 0), 3)):
            pencereli_duvar(y, [a, b], z0, nh - z0, [n], kapali=False, renk=(duvar, 'tas_koyu', 'tas_acik', 'koyu'), v0=(nh - z0) * 0.45,
                            en=0.26, ust=(nh - z0) * 0.12, derin=0.014, sivri=0.0, k_say=6, cerceve=(0.005, [kose, duvar]))
            # pilaster strips between the bays
            L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
            for j in range(n + 1):
                p = a.lerp(b, j / n) + e * (0.008 if j == 0 else -0.008 if j == n else 0.0)
                kutu3(y, p + nc * 0.004 + Z * (z0 + (nh - z0) / 2), e, nc, Z, 0.016, 0.008, nh - z0, duvar, ('+y', '+x', '-x', '+z'))
        duz_duvar(y, V(nw, nl), V(-nw, nl), z0, nh, duvar)
        duz_duvar(y, V(-nw, 0), V(nw, 0), z0, nh, duvar)
        # corbel table: small blocks under the eaves
        for x in (-nw, nw):
            sx = 1 if x > 0 else -1
            for j in range(14):
                yy = 0.01 + (nl - 0.02) * (j + 0.5) / 14
                kutu_merkez(y, (x + sx * 0.005, yy), 0.01, 0.012, 0.01, kose, z0=nh - 0.014)
        silme(y, dikdortgen(-nw, nw, 0, nl), nh - 0.004, 0.006, 0.01, kose, 'duz')
        rz = cati_besik(y, -nw, nw, 0, nl, nh + 0.002, 0.13, 0.022, cati, cati if cati == 'arduvaz' else 'kiremit2', ucluk_key=duvar,
                        alt_key='ahsap_koyu', ns=6, nr=5, uc_sacak=0.014)
        hac(y, 0, nl + 0.012, rz - 0.004, 0.045)
        # apse
        ra, ha = 0.082, nh * 0.78
        yay = [V(ra * math.cos(math.pi * k / 8), nl + ra * math.sin(math.pi * k / 8)) for k in range(9)]
        for k in range(8):
            if k in (2, 5):
                y.kemerli(yay[k], yay[k + 1], z0, ha - z0, (duvar, 'tas_koyu', 'tas_acik', 'koyu'), v0=(ha - z0) * 0.4, en=0.45,
                          ust=(ha - z0) * 0.14, derin=0.01, k_say=6)
            else:
                duz_duvar(y, yay[k], yay[k + 1], z0, ha, duvar)
        silme(y, yay, ha - 0.004, 0.006, 0.008, kose, 'duz', kapali=False)
        tepe = V(0, nl, ha + 0.075)
        yr = [V(p.x, p.y) + (V(p.x, p.y - nl)).normalized() * 0.018 + Z * (ha - 0.004) for p in yay]
        for k in range(8):
            y.yuz_yon([yr[k], yr[k + 1], tepe], cati, V(yr[k].x + yr[k + 1].x, yr[k].y + yr[k + 1].y - 2 * nl, 0.5))
            y.yuz_yon([yr[k], yr[k + 1], V(yay[k + 1].x, yay[k + 1].y, ha - 0.004), V(yay[k].x, yay[k].y, ha - 0.004)], 'ahsap_koyu', -Z)
        # west tower
        tw = 0.085
        ty0, ty1 = -0.17, 0.012
        H = kule_h
        kutu(y, V(-tw - 0.008, ty0 - 0.008, -0.01), X, 2 * tw + 0.016, ty1 - ty0 + 0.008, 0.024, kose, 'onsagsol')
        kk = dikdortgen(-tw, tw, ty0, ty1)
        zb = H * 0.74
        for i in range(4):
            a, b = kk[i], kk[(i + 1) % 4]
            if i == 0:
                kapi(y, a, b, z0, 0.42, zb * 0.42, (duvar, 'tas_koyu', 'tas_acik', 'ahsap'), derin=0.02, cerceve=(0.008, [kose, duvar]))
                duz_duvar(y, a, b, z0 + zb * 0.42, zb, duvar)
                e = (b - a).normalized(); nn = V(e.y, -e.x)
                y.oculus(a.lerp(b, 0.5) + Z * (z0 + zb * 0.66), e, nn, 0.018, 'koyu', kose, 0.006)
            else:
                duz_duvar(y, a, b, z0, zb, duvar)
                e = (b - a).normalized(); nn = V(e.y, -e.x)
                if i != 2:
                    yarik(y, a + nn * 0.001, e, nn, (b - a).length / 2 - 0.004, zb * 0.55, 0.008, zb * 0.16, 'koyu')
            # belfry: two round-arched openings
            for j in range(2):
                y.kemerli(a.lerp(b, j / 2), a.lerp(b, (j + 1) / 2), zb, H - zb, (duvar, 'tas_koyu', 'tas_acik', 'koyu'), v0=(H - zb) * 0.12,
                          en=0.5, ust=(H - zb) * 0.16, derin=0.016, k_say=6, cerceve=(0.005, kose))
            m = a.lerp(b, 0.5); e = (b - a).normalized(); nn = V(e.y, -e.x)
            sutun(y, m.x + nn.x * 0.006, m.y + nn.y * 0.006, zb + (H - zb) * 0.12, zb + (H - zb) * 0.62, 0.006, kose, 'toskan')
        for zz in (zb * 0.42 + z0 + 0.03, zb - 0.002):
            silme(y, kk, zz, 0.008, 0.008, kose, 'duz')
        # quoins
        for p in kk:
            for j in range(int(H / 0.045)):
                ss = 0.02 if j % 2 == 0 else 0.013
                kutu_merkez(y, (p.x, p.y), ss, ss, 0.022, kose, z0=z0 + j * 0.045 + 0.004)
        silme(y, kk, H - 0.006, 0.012, 0.012, kose, 'tac')
        top = cati_kirma(y, -tw, tw, ty0, ty1, H + 0.004, kule_cati, 0.016, cati, cati, ns=4, nr=6, mahya_en=0.008)
        hac(y, 0, (ty0 + ty1) / 2, top - 0.004, 0.06)
        return z + (top + 0.056) * s


def insan(y, x, yy, z, key='kirmizi', s=1.0, ten='kum_acik', aci=0.0, kol=0.0, sapka=None):
    """a small standing person: a robe, shoulders, a head; kol > 0 raises an arm"""
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0075, 0.0), (0.0085, 0.004), (0.0068, 0.024), (0.0058, 0.031), (0.0, 0.033)], key, n=7)
        kure(y, (0, 0, 0.039), 0.0052, ten, n=7, kat=4)
        if sapka:
            donel(y, (0, 0), [(0.009, 0.041), (0.006, 0.043), (0.0045, 0.047), (0.0, 0.048)], sapka, n=7)
        if kol:
            boru(y, [V(0, 0.006, 0.029), V(0.004, 0.009, 0.029 + 0.016 * kol)], 0.0018, ten, n=4)


def oturan(y, x, yy, z, key, aci=0.0, s=1.0, ten='kum_acik', kol=False):
    """a seated spectator (a lump with a head), facing angle aci; kol: an arm raised in a cheer"""
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0072, 0.0), (0.0068, 0.012), (0.0, 0.019)], key, n=6)
        kure(y, (0.001, 0, 0.0235), 0.0048, ten, n=6, kat=3)
        if kol:
            boru(y, [V(0.0, 0.005, 0.014), V(0.002, 0.008, 0.032)], 0.0017, ten, n=4)


def at(y, x, yy, z, aci=0.0, s=1.0, key='ahsap', yele='ahsap_koyu', kosu=0.0, faz=0.0, cul=None, cul2=None, dokum=False):
    """a horse facing aci (+x local), hooves at z, ~0.1 s long, withers ~0.062 s. kosu > 0: a gallop; cul: a
    caparison (two keys: cul, cul2 alternate in panels) hanging from the back to the knees; dokum: a draped caparison
    (domed back, swelling barrel, flared dagged hem) instead of the plain skirt"""
    with parca(y, (x, yy, z), aci, s):
        H = 0.062
        boru(y, [V(-0.04, 0, H - 0.012), V(-0.01, 0, H - 0.014), V(0.028, 0, H - 0.01)], 0.017, key, n=10)
        kure(y, (-0.041, 0, H - 0.012), 0.017, key, n=10, kat=5)
        kure(y, (0.03, 0, H - 0.008), 0.017, key, n=10, kat=5)
        f = faz * TAU
        for lx, front, k0 in ((-0.038, False, 2.4), (0.028, True, 0.0)):
            for s_ in (-1, 1):
                t = math.sin(f + k0 + (0.8 if s_ > 0 else 0))
                sw = kosu * (0.028 if front else -0.026) * t
                top = V(lx, s_ * 0.009, H - 0.018)
                knee = V(lx + sw * 0.6 + (kosu * 0.01 if front else -kosu * 0.006), s_ * 0.009, H * 0.45 + kosu * 0.004 * max(0, t))
                hoof = V(lx + sw, s_ * 0.009, 0.004 + kosu * 0.012 * max(0, t if front else -t))
                boru(y, [top, knee, hoof], 0.0045, key, n=5, r_son=0.003)
                kutu_merkez(y, (hoof.x, hoof.y), 0.008, 0.007, 0.006, 'koyu', z0=hoof.z - 0.004)
        boru(y, [V(0.033, 0, H - 0.004), V(0.048, 0, H + 0.016 - kosu * 0.006), V(0.058, 0, H + 0.028 - kosu * 0.01)], 0.01, key, n=8, r_son=0.008)
        hb = V(0.056, 0, H + 0.032 - kosu * 0.01)
        boru(y, [hb, hb + V(0.022, 0, -0.012 + kosu * 0.004)], 0.0075, key, n=8, r_son=0.0055)
        for s_ in (-1, 1):
            boru(y, [hb + V(-0.002, s_ * 0.004, 0.006), hb + V(-0.004, s_ * 0.005, 0.016)], 0.0022, key, n=4, r_son=0.001)
        boru(y, [V(0.03, 0, H + 0.004), V(0.046, 0, H + 0.024 - kosu * 0.006), hb + V(-0.002, 0, 0.008)], 0.004, yele, n=5)
        boru(y, [V(-0.056, 0, H - 0.008), V(-0.07, 0, H - 0.016 + kosu * 0.012), V(-0.078, 0, H - 0.04 + kosu * 0.03)], 0.0045, yele, n=5, r_son=0.002)
        if cul and dokum:
            # (dokum) a draped caparison: domed over the back, swelling round the barrel, flaring to a dagged hem at
            # the knees (blown back in a gallop), alternating panels, the hem's tongues in the other colour
            n = 16
            R = [(H + 0.011, 0.034, 0.008, 0.0), (H + 0.005, 0.05, 0.017, 0.0), (H - 0.008, 0.059, 0.024, 0.15),
                 (H * 0.66, 0.064, 0.027, 0.5), (H * 0.43, 0.068, 0.03, 1.0)]
            def PD(t, k):
                zz, rx, ry, w = R[k]
                return V(-0.006 - kosu * 0.012 * w + rx * math.cos(t), ry * math.sin(t), zz)
            for i in range(n):
                t0, t1 = TAU * i / n, TAU * (i + 1) / n
                tm = (t0 + t1) / 2
                d = V(math.cos(tm), math.sin(tm) * 2.2, 0).normalized()
                kk = cul if (i // 2) % 2 == 0 or not cul2 else cul2
                for k in range(len(R) - 1):
                    q = [PD(t1, k), PD(t0, k), PD(t0, k + 1), PD(t1, k + 1)]
                    nrm = (q[1] - q[0]).cross(q[2] - q[1])
                    if nrm.dot(d + Z * 0.2) < 0: nrm = -nrm
                    nrm.normalize()
                    y.yuz_yon(q, kk, nrm)
                    y.yuz_yon([p - nrm * 0.0012 for p in q], kk, -nrm)
                a, b = PD(t0, len(R) - 1), PD(t1, len(R) - 1)
                m = (a + b) / 2 + d * 0.002 - Z * 0.011
                kd = (cul2 or cul) if kk == cul else cul
                y.yuz_yon([a, b, m], kd, d)
                y.yuz_yon([a - d * 0.0012, b - d * 0.0012, m - d * 0.0012], kd, -d)
            y.yuz_yon([PD(TAU * i / n, 0) for i in range(n)], cul, Z)
            boru(y, [hb + V(0.002, 0, 0.003), hb + V(0.02, 0, -0.008 + kosu * 0.004)], 0.0082, cul, n=8, r_son=0.006)
        elif cul:
            # a caparison: a skirt round the body from the back down to the knees, in panels
            n = 14
            for i in range(n):
                t0, t1 = TAU * i / n, TAU * (i + 1) / n
                kk = cul if (i // 2) % 2 == 0 or not cul2 else cul2
                def P(t, zz, r_):
                    return V(-0.006 + 0.06 * math.cos(t), r_ * math.sin(t), zz)
                q = [P(t0, H * 0.4, 0.024), P(t1, H * 0.4, 0.024), P(t1, H + 0.006, 0.02), P(t0, H + 0.006, 0.02)]
                y.yuz_yon(q, kk, V(math.cos((t0 + t1) / 2), math.sin((t0 + t1) / 2), 0))
                y.yuz_yon([p - V(math.cos((t0 + t1) / 2), math.sin((t0 + t1) / 2), 0) * 0.0012 for p in q], kk, -V(math.cos((t0 + t1) / 2), math.sin((t0 + t1) / 2), 0))
            y.yuz_yon([V(-0.006 + 0.06 * math.cos(TAU * i / n), 0.02 * math.sin(TAU * i / n), H + 0.006) for i in range(n)], cul, Z)
            # the head's chanfron cloth
            boru(y, [hb + V(0.002, 0, 0.003), hb + V(0.02, 0, -0.008 + kosu * 0.004)], 0.0082, cul, n=8, r_son=0.006)


def sovalye(y, x, yy, z, aci=0.0, s=1.0, cul='boya_kirmizi', cul2='boya_sari', kalkan=None, mizrak=True, kosu=1.0, faz=0.0,
            sorguc=None, mizrak_egim=0.0, dokum=False):
    """a mounted knight on a caparisoned horse facing aci: mail and surcoat, a great helm with a crest, a heater
    shield on the left arm, a couched lance (mizrak_egim lifts its tip). dokum: the draped caparison (see at)"""
    at(y, x, yy, z, aci, s, 'ahsap', 'ahsap_koyu', kosu, faz, cul, cul2, dokum)
    with parca(y, (x, yy, z), aci, s):
        H = 0.062 + 0.006
        # saddle and legs
        if dokum:   # (on the draped cloth: a narrower saddle sitting on its crown)
            kutu_merkez(y, (-0.004, 0), 0.03, 0.026, 0.007, 'ahsap_koyu', z0=H + 0.004)
        else:
            kutu_merkez(y, (-0.004, 0), 0.03, 0.044, 0.008, 'ahsap_koyu', z0=H)
        for s_ in (-1, 1):
            boru(y, [V(0.0, s_ * 0.014, H + 0.008), V(0.01, s_ * 0.026, H - 0.012), V(0.006, s_ * 0.026, H - 0.032)], 0.0045, 'demir', n=5)
        # body: mail + surcoat
        donel(y, (0.0, 0), [(0.012, H + 0.004), (0.013, H + 0.014), (0.011, H + 0.034), (0.008, H + 0.04)], cul, n=8)
        kure(y, (0.0, 0, H + 0.036), 0.0095, 'demir', n=8, kat=4)
        # great helm
        donel(y, (0.001, 0), [(0.0075, H + 0.042), (0.0078, H + 0.056), (0.006, H + 0.06), (0.0, H + 0.061)], 'demir', n=8)
        kutu3(y, V(0.0085, 0, H + 0.051), X, Y, Z, 0.0015, 0.011, 0.0018, 'koyu')
        if sorguc:
            boru(y, [V(0.0, 0, H + 0.06), V(-0.004, 0, H + 0.072), V(-0.012, 0, H + 0.076)], 0.003, sorguc, n=5, r_son=0.001)
        # arms
        boru(y, [V(0.0, -0.011, H + 0.03), V(0.01, -0.016, H + 0.02), V(0.022, -0.012, H + 0.024)], 0.0032, 'demir', n=5)
        boru(y, [V(0.0, 0.011, H + 0.03), V(0.008, 0.018, H + 0.022)], 0.0032, 'demir', n=5)
        # heater shield on the left (+y local) arm
        kk = kalkan or cul
        sh = [V(0.012, 0.024, H + 0.036), V(-0.012, 0.024, H + 0.036), V(-0.012, 0.024, H + 0.016), V(0.0, 0.024, H + 0.002), V(0.012, 0.024, H + 0.016)]
        levha(y, sh, kk, Y, 0.002)
        kutu3(y, V(0.0, 0.0262, H + 0.024), X, Y, Z, 0.004, 0.0015, 0.026, cul2 or 'beyaz')
        kutu3(y, V(0.0, 0.0262, H + 0.026), X, Y, Z, 0.02, 0.0015, 0.004, cul2 or 'beyaz')
        if mizrak:
            a = V(-0.02, -0.015, H + 0.024)
            b = V(0.17, -0.004, H + 0.032 + mizrak_egim)
            boru(y, [a, b], 0.0026, 'boya_sari' if cul != 'boya_sari' else 'beyaz', n=6, r_son=0.0016)
            donel(y, (0, 0), [], 'demir') if False else None
            # vamplate (hand guard) cone
            d = (b - a).normalized()
            p = a + d * 0.03
            u = d.cross(Z).normalized(); w = d.cross(u)
            ring = [p + (u * math.cos(TAU * i / 8) + w * math.sin(TAU * i / 8)) * 0.007 for i in range(8)]
            tip = p + d * 0.014
            for i in range(8):
                y.yuz_yon([ring[i], ring[(i + 1) % 8], tip], 'demir', (ring[i] + ring[(i + 1) % 8]) / 2 - p)
                y.yuz_yon([ring[i], ring[(i + 1) % 8], p - d * 0.001], 'demir', -d)


def zf_sabit(z):
    return lambda x, yy: z


def alcak_duvar(y, yol, z0, h, t, key='granit', ust_key=None):
    """a low wall (churchyard, atrium) along an open polyline: the face on the right of travel, the back t to the left,
    a top and the end caps, mitred corners (no parapet: sur() with parapet_h=0 left a zero-height band flat on its top)"""
    yol = [V(p[0], p[1]) for p in yol]
    ic = disa(yol, -t, False)
    n = len(yol)
    for i in range(n - 1):
        duz_duvar(y, yol[i], yol[i + 1], z0, z0 + h, key)
        duz_duvar(y, ic[i + 1], ic[i], z0, z0 + h, key)
        y.yuz_yon([yol[i] + Z * (z0 + h), yol[i + 1] + Z * (z0 + h), ic[i + 1] + Z * (z0 + h), ic[i] + Z * (z0 + h)], ust_key or key, Z)
    for i, s in ((0, -1), (n - 1, 1)):
        e = (yol[1] - yol[0]) if i == 0 else (yol[-1] - yol[-2])
        y.yuz_yon([yol[i] + Z * z0, ic[i] + Z * z0, ic[i] + Z * (z0 + h), yol[i] + Z * (z0 + h)], key, e * s)


def _ss(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def cayir_renk(G, kuru=0.0):
    """a corner-colour function for doku.KOSE_RENK['cimen']: a meadow in broad soft patches (greener / drier, never
    per triangle), drying towards the top of mounds above the ground level G; kuru > 0 shifts the whole towards hay"""
    def f(x, yy, z):
        n1 = math.sin(x * 4.3 + 1.1) * math.cos(yy * 3.7 - 0.6)
        n2 = math.sin(x * 9.1 - yy * 6.3 + 2.0)
        n = n1 * 0.7 + n2 * 0.3
        c0, c1 = (0.38, 0.49, 0.24), (0.50, 0.53, 0.30)
        t = max(0.0, min(1.0, 0.5 + 0.5 * n + kuru))
        c = tuple(p + (q - p) * t for p, q in zip(c0, c1))
        h = _ss(0.03, 0.3, z - G + 0.03 * n2)
        return tuple(p + (q - p) * h * 0.55 for p, q in zip(c, (0.52, 0.52, 0.32)))
    return f
