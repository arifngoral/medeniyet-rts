# Shared helpers for the Arab landmarks lm_elhamra, lm_memlukkisla, lm_kervanhani, lm_samcelik (not a building:
# imported by those scripts). Nasrid / Mamluk / Syrian details on top of parcalar.py: pointed merlons, horseshoe arches,
# ring roofs round a courtyard, courtyard arcades, ablaq (striped) walls, tile bands, carved stars, camels and goods.
import math
from mathutils import Vector
from parcalar import *


def sivri_mazgal(y, a, b, z, h=0.026, kal=0.018, key='kirmizi_tas', w=0.022, g=0.015, uc=0.013, kademe=False):
    """merlons along a->b, their outer face on the line (facing its right), each a box with a pyramid cap (Nasrid,
    Mamluk); kademe: a stepped (Mamluk / Ayyubid) merlon - a narrower step on the box under the cap"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-6: return
    e = (b - a) / L; l = Z.cross(e)
    k = max(1, int(round((L + g) / (w + g))))
    w2 = (L + g) / k - g
    if w2 <= 0.004: return
    for i in range(k):
        o = a + e * (i * (w2 + g)) + Z * z
        hh = h * (0.62 if kademe else 1.0)
        kutu(y, o, e, w2, kal, hh, key, 'onarkasagsol')
        ww, kk, oo = w2, kal, o + Z * hh
        if kademe:
            ww, kk = w2 * 0.62, kal * 0.7
            oo = o + e * ((w2 - ww) / 2) + l * ((kal - kk) / 2) + Z * hh
            # the ledge round the step
            ring = [o + Z * hh, o + e * w2 + Z * hh, o + e * w2 + l * kal + Z * hh, o + l * kal + Z * hh]
            inr = [oo, oo + e * ww, oo + e * ww + l * kk, oo + l * kk]
            for j in range(4):
                y.yuz_yon([ring[j], ring[(j + 1) % 4], inr[(j + 1) % 4], inr[j]], key, Z)
            kutu(y, oo, e, ww, kk, h - hh, key, 'onarkasagsol')
            oo = oo + Z * (h - hh)
        t = [oo, oo + e * ww, oo + e * ww + l * kk, oo + l * kk]
        c = (t[0] + t[2]) / 2 + Z * uc
        for j in range(4):
            yuz_dis(y, [t[j], t[(j + 1) % 4], c], key, c - Z * (uc * 3))


def mazgalli_kenar(y, kose, z, key, kal=0.018, h=0.026, kapali=True, ust_key=None, dolu=0.012, **kw):
    """a solid parapet band dolu high round a CCW polygon (or along a polyline) with pointed merlons on it"""
    parapet(y, kose, z, dolu, 0, kal, key, kapali=kapali, ust_key=ust_key)
    n = len(kose)
    for i in range(n if kapali else n - 1):
        sivri_mazgal(y, kose[i], kose[(i + 1) % n], z + dolu, h, kal, key, **kw)


def kat_pencere(y, a, b, z0, z1, zp0, zp1, n, renk, en=0.42, sivri=0.0, cerceve=None, derin=0.012, ust=0.012, sutuncuk=None,
                k_say=6, v0=0.0):
    """a wall a->b from z0 to z1 with a row of n arched windows between zp0 and zp1 (plain wall below and above).
    sutuncuk: a key for a slim mullion colonnette in each window (the Nasrid ajimez: a paired window)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    duz_duvar(y, a, b, z0, zp0, renk[0])
    duz_duvar(y, a, b, zp1, z1, renk[0])
    for i in range(n):
        p, q = a.lerp(b, i / n), a.lerp(b, (i + 1) / n)
        y.kemerli(p, q, zp0, zp1 - zp0, renk, v0=v0, en=en, ust=ust, derin=derin, k_say=k_say, sivri=sivri, cerceve=cerceve)
        if sutuncuk:
            e = (q - p).normalized(); nc = V(e.y, -e.x)
            m = (p + q) / 2 - nc * (derin * 0.45)
            W = (q - p).length
            hs = (zp1 - zp0) - ust - (sivri * en * W if sivri else en * W / 2)
            y.prizma((m.x, m.y), 0.0032, zp0 + v0, zp0 + hs + en * W * 0.18, sutuncuk, n=6)


def duvar_bant(y, a, b, z0, z1, key, n=2):
    for k in range(n):
        duz_duvar(y, a, b, z0 + (z1 - z0) * k / n, z0 + (z1 - z0) * (k + 1) / n, key)


def nal_kemerli(y, a, b, z0, H, renk, en=0.5, ust=0.03, derin=0.03, alfa=0.42, n_yay=12, alfiz=None, tas=None, v0=0.0):
    """a wall bay a->b (facing its right) with a horseshoe-arched opening derin deep (Moorish / Nasrid): the arc of a
    circle carried past the half round by alfa (radians) each side, the jambs narrower than the arc. renk: wall,
    reveal, sill, back. alfiz = (width, key): the raised rectangular frame round the arch; tas: keys alternating on
    the voussoirs (a band round the arch). Returns the crown height above z0"""
    duvar, koyu, acik, delik = renk
    a, b = V(a[0], a[1]), V(b[0], b[1])
    W = (b - a).length; e = (b - a) / W; nc = V(e.y, -e.x)
    L = lambda u, v, d=0.0: a + e * u - nc * d + Z * (z0 + v)
    xm = W / 2
    jw = en * W / 2
    R = jw / math.cos(alfa)
    hc = H - ust - R
    hj = hc - R * math.sin(alfa)
    tc = math.atan2(H - hc, W - xm)
    ts = sorted({-alfa + (math.pi + 2 * alfa) * k / n_yay for k in range(n_yay + 1)} | {tc, math.pi - tc})
    ic = [(xm + jw, v0), (xm + jw, hj)] + [(xm + R * math.cos(t), hc + R * math.sin(t)) for t in ts[1:-1]] + [(xm - jw, hj), (xm - jw, v0)]
    def dis(t):
        c, s = math.cos(t), math.sin(t)
        k = (W - xm) / abs(c) if abs(c) > 1e-9 else 1e9
        if s > 1e-9: k = min(k, (H - hc) / s)
        return (xm + c * k, hc + s * k)
    dk = [(W, v0), (W, hj)] + [dis(t) for t in ts[1:-1]] + [(0.0, hj), (0.0, v0)]
    for i in range(len(ic) - 1):
        y.yuz_yon([L(*ic[i]), L(*ic[i + 1]), L(*dk[i + 1]), L(*dk[i])], duvar, nc)
    if v0 > 0:
        y.yuz_yon([L(0, 0), L(W, 0), L(W, v0), L(0, v0)], duvar, nc)
    # reveals, the sill and the back
    yol = ic + [ic[0]]
    for i in range(len(yol) - 1):
        p, q = yol[i], yol[i + 1]
        vm = min(max((p[1] + q[1]) / 2, v0), hc)
        mid = (L(*p) + L(*q)) / 2
        hedef = L(xm, vm) if i < len(yol) - 2 else L(xm, v0 + 1)
        y.yuz_yon([L(*p), L(*q), L(*q, derin), L(*p, derin)], acik if i == len(yol) - 2 else koyu, hedef - mid)
    y.yuz_yon([L(u, v, derin) for u, v in ic], delik, nc)
    if tas:   # voussoirs: a raised band round the arc
        f = R * 0.22
        arc = [(xm + R * math.cos(t), hc + R * math.sin(t)) for t in ts]
        arc2 = [(xm + (R + f) * math.cos(t), hc + (R + f) * math.sin(t)) for t in ts]
        for i in range(len(arc) - 1):
            k_ = tas[i % len(tas)]
            y.yuz_yon([L(*arc[i], -0.002), L(*arc[i + 1], -0.002), L(*arc2[i + 1], -0.002), L(*arc2[i], -0.002)], k_, nc)
            y.yuz_yon([L(*arc2[i], -0.002), L(*arc2[i + 1], -0.002), L(*arc2[i + 1]), L(*arc2[i])], tas[0], L(*arc2[i]) - L(xm, hc))
    if alfiz:
        f, k_ = alfiz
        x0, x1 = xm - R - f * 1.6, xm + R + f * 1.6
        top = min(H - 0.002, hc + R + f * 2.6)
        lo = hj
        for (u0, v0_, u1, v1_) in ((x0, lo, x0 + f, top), (x1 - f, lo, x1, top), (x0 + f, top - f, x1 - f, top)):
            q = [L(u0, v0_, -0.003), L(u1, v0_, -0.003), L(u1, v1_, -0.003), L(u0, v1_, -0.003)]
            y.yuz_yon(q, k_, nc)
            for j in range(4):
                p1, p2 = q[j], q[(j + 1) % 4]
                y.yuz_yon([p1, p2, p2 - nc * 0.003, p1 - nc * 0.003], k_, (p1 + p2) / 2 - (q[0] + q[2]) / 2)   # (back to the wall)
    return hc + R


def halka_cati(y, ic, dis, z_ic, z_sirt, z_dis, sacak=0.03, sacak_dis=None, key='kiremit', dilim=('kiremit', 'kiremit2'), f=0.01,
               mahya='kiremit2', alt_key='ahsap_koyu'):
    """a ring of tiled roofs round a courtyard: ic = the court's wall line (x0, x1, y0, y1), dis = the wings' outer
    wall line; a ridge ring half way, slopes down to an inner eave over the court (z_ic, sacak out) and to an outer eave
    (z_dis). Fascias and flat soffits at both eaves (their undersides at z - f: the walls stop there). Hips at the
    corners fall out of the rectangles"""
    sd = sacak if sacak_dis is None else sacak_dis
    ix0, ix1, iy0, iy1 = ic; dx0, dx1, dy0, dy1 = dis
    E_i = dikdortgen(ix0 + sacak, ix1 - sacak, iy0 + sacak, iy1 - sacak)
    W_i = dikdortgen(ix0, ix1, iy0, iy1)
    R = dikdortgen((ix0 + dx0) / 2, (ix1 + dx1) / 2, (iy0 + dy0) / 2, (iy1 + dy1) / 2)
    W_d = dikdortgen(dx0, dx1, dy0, dy1)
    E_d = dikdortgen(dx0 - sd, dx1 + sd, dy0 - sd, dy1 + sd)
    kk = lambda j: dilim[j % len(dilim)] if dilim else key
    zr = lambda p, z: V(p.x, p.y, z)
    for i in range(4):
        j = (i + 1) % 4
        # inner slope in 3 courses, outer slope in 2 (the tile pattern and the baked shadow follow them)
        for s in range(3):
            t0, t1 = s / 3, (s + 1) / 3
            P = lambda p, q, t: p.lerp(q, t)
            q = [P(zr(E_i[i], z_ic), zr(R[i], z_sirt), t0), P(zr(E_i[j], z_ic), zr(R[j], z_sirt), t0),
                 P(zr(E_i[j], z_ic), zr(R[j], z_sirt), t1), P(zr(E_i[i], z_ic), zr(R[i], z_sirt), t1)]
            y.yuz_yon(q, kk(s), Z)
        for s in range(2):
            t0, t1 = s / 2, (s + 1) / 2
            P = lambda p, q, t: p.lerp(q, t)
            q = [P(zr(R[i], z_sirt), zr(E_d[i], z_dis), t0), P(zr(R[j], z_sirt), zr(E_d[j], z_dis), t0),
                 P(zr(R[j], z_sirt), zr(E_d[j], z_dis), t1), P(zr(R[i], z_sirt), zr(E_d[i], z_dis), t1)]
            y.yuz_yon(q, kk(s + 1), Z)
        # inner fascia (faces the court) and soffit
        c_in = V((ix0 + ix1) / 2, (iy0 + iy1) / 2)
        m = (E_i[i] + E_i[j]) / 2
        y.yuz_yon([zr(E_i[i], z_ic), zr(E_i[j], z_ic), zr(E_i[j], z_ic - f), zr(E_i[i], z_ic - f)], alt_key, c_in - m)
        y.yuz_yon([zr(E_i[i], z_ic - f), zr(E_i[j], z_ic - f), zr(W_i[j], z_ic - f), zr(W_i[i], z_ic - f)], alt_key, -Z)
        m = (E_d[i] + E_d[j]) / 2
        y.yuz_yon([zr(E_d[i], z_dis), zr(E_d[j], z_dis), zr(E_d[j], z_dis - f), zr(E_d[i], z_dis - f)], alt_key, m - c_in)
        y.yuz_yon([zr(E_d[i], z_dis - f), zr(E_d[j], z_dis - f), zr(W_d[j], z_dis - f), zr(W_d[i], z_dis - f)], alt_key, -Z)
        # ridge and hips
        cubuk(y, zr(R[i], z_sirt + 0.004), zr(R[j], z_sirt + 0.004), 0.011, mahya)
        cubuk(y, zr(R[i], z_sirt + 0.004), zr(E_i[i], z_ic + 0.004), 0.008, mahya)
        cubuk(y, zr(R[i], z_sirt + 0.004), zr(E_d[i], z_dis + 0.004), 0.008, mahya)


def avlu_revak(y, rect, z0, H, sayilar, renk, en=0.78, ust=0.03, derin=0.06, sivri=0.0, sutun_r=0.006, sutun_key='mermer',
               cerceve=None, k_say=8, korkuluk=None, v0=0.0, sutunlu=True, atla=()):
    """an arcade facing INTO a court (rect = x0, x1, y0, y1): each side split in its count of arched bays (kemerli,
    derin deep: the gallery), colonnettes in front of the piers. atla: side indices (0 south, 1 east, 2 north,
    3 west) left out"""
    k = dikdortgen(*rect)
    for i in range(4):
        if i in atla: continue
        a, b = k[(i + 1) % 4], k[i]
        n = sayilar[i]
        e = (b - a).normalized(); nc = V(e.y, -e.x)
        for j in range(n):
            p, q = a.lerp(b, j / n), a.lerp(b, (j + 1) / n)
            y.kemerli(p, q, z0, H, renk, v0=v0, en=en, ust=ust, derin=derin, k_say=k_say, sivri=sivri, cerceve=cerceve, korkuluk=korkuluk)
        if sutunlu:
            W = (b - a).length / n
            hs = H - ust - (sivri * en * W if sivri else en * W / 2)
            for j in range(0, n + 1):
                p = a.lerp(b, j / n) + nc * (sutun_r * 1.2) + (e * sutun_r * 1.3 if j == 0 else -e * sutun_r * 1.3 if j == n else V(0, 0))
                sutun(y, p.x, p.y, z0 + v0, z0 + v0 + hs - v0, sutun_r, sutun_key, 'osmanli')


def cini_bant(y, a, b, z, h, keys=('turkuaz', 'lacivert'), n=None, d=0.0025):
    """a glazed tile band on a wall a->b (facing its right), a hair in front: alternating squares"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nc = V(e.y, -e.x)
    n = n or max(2, int(round(L / h)))
    for i in range(n):
        p, q = a.lerp(b, i / n) + nc * d, a.lerp(b, (i + 1) / n) + nc * d
        y.yuz_yon([p + Z * z, q + Z * z, q + Z * (z + h), p + Z * (z + h)], keys[i % len(keys)], nc)
    # the band's top and bottom edges
    p, q = a + nc * d, b + nc * d
    y.yuz_yon([a + Z * (z + h), b + Z * (z + h), q + Z * (z + h), p + Z * (z + h)], keys[0], Z)


def ablak(y, a, b, z0, z1, keys=('kirec', 'kirmizi_tas'), sira=0.022, on=0.0):
    """an ablaq wall a->b (facing its right): horizontal courses of alternating light and dark stone. on > 0: a band
    laid that far in front of a wall already on the line (no coplanar faces), with its top and bottom edges"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    if on:
        e = (b - a).normalized(); nc = V(e.y, -e.x)
        a2, b2 = a + nc * on, b + nc * on
        y.yuz_yon([a2 + Z * z1, b2 + Z * z1, b + Z * z1, a + Z * z1], keys[-1], Z)
        y.yuz_yon([a + Z * z0, b + Z * z0, b2 + Z * z0, a2 + Z * z0], keys[0], -Z)
        a, b = a2, b2
    n = max(1, int(round((z1 - z0) / sira)))
    for k in range(n):
        duz_duvar(y, a, b, z0 + (z1 - z0) * k / n, z0 + (z1 - z0) * (k + 1) / n, keys[k % len(keys)])


def yildiz(y, o, ex, nrm, r, key, k=8, ic=0.5, d=0.0025, kat=0.0, yan_key=None):
    """a raised k-pointed star (carved geometric ornament): o on the surface, ex along it, nrm out"""
    o, ex, nrm = V(*o), V(*ex), V(*nrm)
    up = nrm.cross(ex).normalized()
    pts = [o + ex * ((r if i % 2 == 0 else r * ic) * math.cos(kat + math.pi * i / k)) + up * ((r if i % 2 == 0 else r * ic) * math.sin(kat + math.pi * i / k)) for i in range(2 * k)]
    y.yuz_yon([p + nrm * d for p in pts], key, nrm)
    for i in range(2 * k):
        p, q = pts[i], pts[(i + 1) % (2 * k)]
        y.yuz_yon([p, q, q + nrm * d, p + nrm * d], yan_key or key, (p + q) / 2 - o)


def malqaf(y, cx, cy, z, aci=0.0, w=0.07, d=0.05, h=0.11, key='kum_acik', tahta='ahsap_dikey'):
    """a Cairene / Syrian wind-catcher on a flat roof: a wedge rising from a low kerb at the south to a tall open mouth
    at the north (+y before turning), a planked slope with stone copings, the mouth framed with a dark inside and a
    mullion. (A wedge, not a box under a gable: the old one read as a little hut)"""
    b, f = 0.014, 0.008
    with parca(y, (cx, cy, z), aci):
        P = lambda u, v, t: V(u, v, t)
        y.yuz_yon([P(-w / 2, -d / 2, 0), P(w / 2, -d / 2, 0), P(w / 2, -d / 2, b), P(-w / 2, -d / 2, b)], key, -Y)
        for s in (-1, 1):
            y.yuz_yon([P(s * w / 2, -d / 2, 0), P(s * w / 2, d / 2, 0), P(s * w / 2, d / 2, h), P(s * w / 2, -d / 2, b)], key, X * s)
            cubuk(y, P(s * (w / 2 - 0.003), -d / 2, b + 0.003), P(s * (w / 2 - 0.003), d / 2, h + 0.003), 0.0045, key)
        y.yuz_yon([P(-w / 2, -d / 2, b), P(w / 2, -d / 2, b), P(w / 2, d / 2, h), P(-w / 2, d / 2, h)], tahta, V(0, -(h - b), d))
        # the mouth: a stone frame, the dark inside a little recessed, its reveals, a timber mullion
        yd, r = d / 2, 0.003
        for q in ([P(-w / 2, yd, 0), P(w / 2, yd, 0), P(w / 2, yd, 0.02), P(-w / 2, yd, 0.02)],
                  [P(-w / 2, yd, 0.02), P(-w / 2 + f, yd, 0.02), P(-w / 2 + f, yd, h), P(-w / 2, yd, h)],
                  [P(w / 2 - f, yd, 0.02), P(w / 2, yd, 0.02), P(w / 2, yd, h), P(w / 2 - f, yd, h)],
                  [P(-w / 2 + f, yd, h - f), P(w / 2 - f, yd, h - f), P(w / 2 - f, yd, h), P(-w / 2 + f, yd, h)]):
            y.yuz_yon(q, key, Y)
        o = [P(-w / 2 + f, yd, 0.02), P(w / 2 - f, yd, 0.02), P(w / 2 - f, yd, h - f), P(-w / 2 + f, yd, h - f)]
        y.yuz_yon([p - Y * r for p in o], 'koyu', Y)
        for i in (0, 1, 3):     # (no top reveal: the sloping hood dips under it)
            p, q = o[i], o[(i + 1) % 4]
            y.yuz_yon([p, q, q - Y * r, p - Y * r], key, (o[0] + o[2]) / 2 - (p + q) / 2)
        cubuk(y, P(0, yd - r / 2, 0.02), P(0, yd - r / 2, h - f), 0.003, 'ahsap_koyu')


def dam_bolme(y, x0, x1, y0, y1, z, key, aralik=0.17):
    """raised stone copings across a flat roof x0..x1, y0..y1 (at z), dividing it into drainage bays"""
    uzun_x = (x1 - x0) > (y1 - y0)
    n = max(1, int(round(max(x1 - x0, y1 - y0) / aralik)))
    for k in range(1, n):
        t = k / n
        if uzun_x:
            xx = x0 + (x1 - x0) * t
            kutu(y, V(xx + 0.004, y0 + 0.012, z), Y, y1 - y0 - 0.024, 0.008, 0.005, key, 'onarkasagsolust')
        else:
            yy = y0 + (y1 - y0) * t
            kutu(y, V(x0 + 0.012, yy - 0.004, z), X, x1 - x0 - 0.024, 0.008, 0.005, key, 'onarkasagsolust')


def oluk(y, a, b, n, z, key):
    """n stone water spouts sticking out of the wall a->b (facing its right) just under z"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(n):
        p = a.lerp(b, (k + 1) / (n + 1)) + nn * 0.03
        kutu(y, p - e * 0.005 + Z * (z - 0.014), e, 0.01, 0.03, 0.009, key, 'onsagsolust')


def denk(y, cx, cy, z, key='kumas', aci=0.0, w=0.06, d=0.045, h=0.035):
    """a corded bale of goods"""
    kutu_merkez(y, (cx, cy), w, d, h, key, z0=z, aci=aci)
    ca, sa = math.cos(aci), math.sin(aci)
    for t in (-0.25, 0.25):
        o = V(cx + ca * w * t, cy + sa * w * t)
        e = V(-sa, ca)
        cubuk(y, o - e * (d / 2 + 0.002) + Z * (z + h + 0.002), o + e * (d / 2 + 0.002) + Z * (z + h + 0.002), 0.004, 'ahsap_koyu', 0.002)


def kup(y, cx, cy, z, r=0.018, h=0.05, key='kiremit'):
    """a clay storage jar"""
    donel(y, (cx, cy), [(0.0, z), (r * 0.6, z), (r, z + h * 0.35), (r * 0.85, z + h * 0.75), (r * 0.45, z + h * 0.9), (r * 0.5, z + h), (0.0, z + h)], key, n=10)


def deve(y, x, yy, z, aci, renk='ahsap_acik', yuk=True, cul='boya_kirmizi', olcek=1.35, cok=False):
    """a stylised dromedary (head towards +x before turning); yuk: bales over a saddle cloth; cok: kneeling"""
    with parca(y, (x, yy, z), aci, olcek):
        h = 0.075 if not cok else 0.03
        boru(y, [V(-0.045, 0, h + 0.012), V(-0.01, 0, h + 0.02), V(0.03, 0, h + 0.018), V(0.048, 0, h + 0.012)], 0.02, renk, n=10)
        kure(y, (-0.045, 0, h + 0.012), 0.019, renk, n=10, kat=5)
        kure(y, (0.046, 0, h + 0.013), 0.018, renk, n=10, kat=5)
        donel(y, (-0.004, 0), [(0.026, h + 0.02), (0.025, h + 0.03), (0.021, h + 0.042), (0.014, h + 0.052), (0.006, h + 0.057), (0.0, h + 0.058)], renk, n=12)
        if not cok:
            boru(y, [V(0.05, 0, h + 0.016), V(0.082, 0, h + 0.004), V(0.102, 0, h + 0.026), V(0.106, 0, h + 0.05)], 0.009, renk, n=6, r_son=0.007)
            boru(y, [V(0.102, 0, h + 0.054), V(0.13, 0, h + 0.047)], 0.009, renk, n=6, r_son=0.006)
            for s in (-1, 1):
                cubuk(y, V(0.104, s * 0.006, h + 0.06), V(0.101, s * 0.007, h + 0.069), 0.003, renk)
        else:
            # kneeling: the neck held up in an S, the head high and level, a muzzle and small ears
            boru(y, [V(0.05, 0, h + 0.018), V(0.07, 0, h + 0.02), V(0.086, 0, h + 0.044), V(0.09, 0, h + 0.07)], 0.009, renk, n=8, r_son=0.0072)
            boru(y, [V(0.087, 0, h + 0.074), V(0.105, 0, h + 0.071), V(0.118, 0, h + 0.064)], 0.0085, renk, n=8, r_son=0.0055)
            kure(y, (0.119, 0, h + 0.063), 0.0056, renk, n=8, kat=4)
            for s in (-1, 1):
                cubuk(y, V(0.088, s * 0.006, h + 0.078), V(0.085, s * 0.008, h + 0.086), 0.0028, renk)
                kure(y, (0.101, s * 0.0068, h + 0.076), 0.0018, 'koyu', n=5, kat=3)      # the eyes
            # the hairy pad on the throat and the mouth line
            kure(y, (0.08, 0, h + 0.03), 0.0075, renk, n=8, kat=4)
        boru(y, [V(-0.062, 0, h + 0.02), V(-0.07, 0, h - 0.005), V(-0.068, 0, h - 0.02 if not cok else h - 0.01)], 0.0025, 'ahsap_koyu', n=4, r_son=0.0015)
        if not cok:
            for lx in (-0.04, 0.038):
                for s in (-1, 1):
                    boru(y, [V(lx, s * 0.01, h + 0.004), V(lx + 0.004, s * 0.01, h * 0.5), V(lx, s * 0.01, 0.006)], 0.0055, renk, n=5, r_son=0.004)
                    kutu_merkez(y, (lx + 0.003, s * 0.01), 0.012, 0.01, 0.006, 'ahsap_koyu')
        else:
            # the body sinks onto its chest pad and folded legs: a belly mass down to the ground, the forelegs
            # folded with the knees forward, the hind legs folded with the haunches bulging out and the feet back
            boru(y, [V(-0.042, 0, h - 0.006), V(0.0, 0, h - 0.01), V(0.036, 0, h - 0.008)], 0.017, renk, n=8, r_son=0.015)
            kure(y, (0.04, 0, h - 0.016), 0.012, renk, n=8, kat=4)      # the chest pad on the ground
            for s in (-1, 1):
                boru(y, [V(0.034, s * 0.014, h - 0.002), V(0.06, s * 0.012, 0.007), V(0.03, s * 0.0135, 0.005)], 0.006, renk, n=6, r_son=0.0048)
                kure(y, (0.06, s * 0.012, 0.0075), 0.0068, renk, n=6, kat=4)                                  # the knee
                kure(y, (0.027, s * 0.0135, 0.0052), 0.0058, renk, n=6, kat=3)                               # the padded foot
                kure(y, (-0.04, s * 0.012, h - 0.004), 0.016, renk, n=8, kat=4)                              # the haunch
                boru(y, [V(-0.03, s * 0.022, 0.012), V(-0.052, s * 0.022, 0.007), V(-0.072, s * 0.016, 0.005)], 0.0062, renk, n=6, r_son=0.0045)
                kure(y, (-0.073, s * 0.016, 0.0052), 0.0056, renk, n=6, kat=3)
        if yuk:
            kutu_merkez(y, (-0.004, 0), 0.05, 0.05, 0.004, cul, z0=h + 0.03)
            for s in (-1, 1):
                kutu_merkez(y, (-0.004, s * 0.034), 0.05, 0.026, 0.04, 'kumas' if s > 0 else 'kece', z0=h - 0.005)
                cubuk(y, V(-0.03, s * 0.048, h + 0.03), V(0.022, s * 0.048, h + 0.03), 0.003, 'ahsap_koyu', 0.003)
            denk(y, -0.004, 0, h + 0.056, 'boya_sari', w=0.04, d=0.03, h=0.02)


def adam(y, x, yy, z, aci=0.0, govde='kumas', bas='beyaz', boy=0.05, kol=None):
    """a small stylised figure (robe, head, turban); kol = (dx, dz) a raised arm end (a smith's hammer arm)"""
    with parca(y, (x, yy, z), aci):
        donel(y, (0, 0), [(0.0, 0.0), (boy * 0.2, 0.0), (boy * 0.17, boy * 0.45), (boy * 0.13, boy * 0.72), (boy * 0.07, boy * 0.78), (0.0, boy * 0.78)], govde, n=8)
        kure(y, (0, 0, boy * 0.86), boy * 0.1, 'ahsap_acik', n=8, kat=4)
        donel(y, (0, 0), [(boy * 0.11, boy * 0.88), (boy * 0.12, boy * 0.94), (boy * 0.07, boy * 1.0), (0.0, boy * 1.01)], bas, n=8)
        if kol:
            boru(y, [V(0, boy * 0.1, boy * 0.65), V(kol[0], boy * 0.12, boy * 0.65 + kol[1])], boy * 0.04, govde, n=4)
