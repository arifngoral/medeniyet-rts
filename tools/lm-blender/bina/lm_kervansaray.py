# Söğüt Kervansarayı (lm_kervansaray): a Seljuk / early Ottoman caravanserai after Sultanhanı: thick cut-stone walls
# with a rhythm of triangular, square and half-round buttresses, string courses, water spouts and octagonal corner
# towers; a towering muqarnas portal framed by carved star and lozenge borders; a courtyard with an open arcade of
# stalls, room doors, the köşk mescit raised on four ablaq arches; the covered winter hall behind (stone-coursed
# pitched roofs, a raised nave, the central dome under an octagonal stone cone with a lantern); a paved forecourt
# with a caravan road, laden camels and goods.
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()

Z0 = 0.04
XW = 0.95                    # outer half width
YF, YH, YB = -0.9, 0.04, 0.88     # front wall, the hall's front wall, back wall
HW, HH = 0.27, 0.36          # court ranges' wall height, hall wall height
IX, IYF = 0.68, -0.65        # inner court: x +-IX, y IYF..YH
TAS = 'kum'
PAR = 0.024                  # the parapet's height above the roofs

y.bolum('Zemin')
zemin(y, -XW - 0.16, XW + 0.16, YF - 0.36, YB + 0.12, Z0, 'kum_koyu', 'zemin', basamak=(('on', 0.5),), n_basamak=2)


# ---------------- ornament helpers ----------------
def yildiz(o, ex, nrm, r, key, k=8, ic=0.5, d=0.0025, kat=0.0, yan_key=None):
    """a raised k-pointed star (carved Seljuk geometric ornament): o on the surface, ex along it, nrm out"""
    o, ex, nrm = V(*o), V(*ex), V(*nrm)
    up = nrm.cross(ex).normalized()
    pts = []
    for i in range(2 * k):
        rr = r if i % 2 == 0 else r * ic
        t = kat + math.pi * i / k
        pts.append(o + ex * (rr * math.cos(t)) + up * (rr * math.sin(t)))
    y.yuz_yon([p + nrm * d for p in pts], key, nrm)
    for i in range(2 * k):
        p, q = pts[i], pts[(i + 1) % (2 * k)]
        y.yuz_yon([p, q, q + nrm * d, p + nrm * d], yan_key or key, (p + q) / 2 - o)


def eskenar(o, ex, nrm, r, key, d=0.002):
    """a raised lozenge"""
    yildiz(o, ex, nrm, r, key, k=2, ic=0.55, d=d, kat=0.0)


def kemer_pano(o, ex, nrm, w, h, key='kum_koyu', cer='kum_acik', f=0.006, d=0.002):
    """a carved blind pointed niche plate (dark field, light frame) on a wall: o = bottom centre on the surface"""
    o, ex, nrm = V(*o), V(*ex), V(*nrm)
    yol = kemer_yolu(-w / 2, w / 2, h - w * 0.6, 0.6, 8)
    P = lambda u, v, dd: o + ex * u + Z * v + nrm * dd
    ic = [(-w / 2, 0)] + yol + [(w / 2, 0)]
    y.yuz_yon([P(u, v, d) for u, v in ic], key, nrm)
    # the frame: an outer outline offset by f
    def dis(u, v):
        if v <= h - w * 0.6 + 1e-9:
            return (u - f if u < 0 else u + f, v)
        kk = V(u, v - (h - w * 0.6)).normalized()
        return (u + kk.x * f, v + kk.y * f)
    for i in range(len(ic) - 1):
        (ua, va), (ub, vb) = ic[i], ic[i + 1]
        if va == 0 and vb == 0: continue
        pa, pb = dis(ua, va), dis(ub, vb)
        y.yuz_yon([P(ua, va, d + 0.001), P(ub, vb, d + 0.001), P(*pb, d + 0.001), P(*pa, d + 0.001)], cer, nrm)
        y.yuz_yon([P(*pa, 0), P(*pb, 0), P(*pb, d + 0.001), P(*pa, d + 0.001)], cer, P(*pa, 0) - P(0, h * 0.4, 0) + P(*pb, 0) - P(0, h * 0.4, 0))
    y.yuz_yon([P(-w / 2 - f, 0, 0), P(w / 2 + f, 0, 0), P(w / 2 + f, 0, d + 0.001), P(-w / 2 - f, 0, d + 0.001)], cer, -Z)


def duvar_dilim(p, q, za, zb, key=TAS, n=3):
    """a plain wall cut in n bands (more corners: the baked shadow of a cornice stays near it)"""
    for k in range(n):
        duz_duvar(y, p, q, za + (zb - za) * k / n, za + (zb - za) * (k + 1) / n, key)


# ---------------- buttresses ----------------
PAY_W = {'ucgen': 0.09, 'kare': 0.075, 'yarim': 0.1}


def payanda(p, e, h, tur, z0=Z0):
    """a buttress against the wall at p (e along the wall, outward to its right): 'ucgen' triangular with a sloped
    top, 'kare' square with a sloped cap, 'yarim' half-round (half 8-gon) with a conical cap; each on a plinth"""
    p = V(p.x, p.y); nn = V(e.y, -e.x)
    zt = z0 + h - 0.006
    if tur == 'yarim':
        zt = z0 + h - 0.036
        r = PAY_W['yarim'] / 2
        ring = [p + e * (r * math.cos(t)) + nn * (r * math.sin(t)) for t in [math.pi * (1 - i / 6) for i in range(7)]]
        for i in range(6):
            a, b = ring[i], ring[i + 1]
            duz_duvar(y, a, b, z0, z0 + 0.03, 'kum_koyu')
            duvar_dilim(a, b, z0 + 0.03, zt, n=3)
            # a ring course and the cap
            ap, bp = a + (a - p).normalized() * 0.005, b + (b - p).normalized() * 0.005
            kutu_s = [a + Z * (zt - 0.012), b + Z * (zt - 0.012), bp + Z * (zt - 0.012), ap + Z * (zt - 0.012)]
            y.yuz_yon([ap + Z * (zt - 0.012), bp + Z * (zt - 0.012), bp + Z * zt, ap + Z * zt], 'kum_acik', (a + b) / 2 - p)
            y.yuz_yon(kutu_s, 'kum_acik', -Z)
            y.yuz_yon([ap + Z * zt, bp + Z * zt, p + Z * (zt + 0.03)], 'kum_acik', (a + b) / 2 - p + Z * 0.5)
        return
    if tur == 'ucgen':
        w, d = PAY_W['ucgen'], 0.065
        a, b, t = p - e * (w / 2), p + e * (w / 2), p + nn * d
        for u, v in ((a, t), (t, b)):
            duz_duvar(y, u, v, z0, z0 + 0.03, 'kum_koyu')
            duvar_dilim(u, v, z0 + 0.03, zt - d * 0.8, n=3)
        y.yuz_yon([a + Z * zt, t + Z * (zt - d * 0.8), b + Z * zt], 'kum_acik', nn + Z)
        zs = zt - d * 0.8
        y.yuz_yon([a + Z * zs, t + Z * zs, a + Z * zt], TAS, V((t - a).y, -(t - a).x))
        y.yuz_yon([t + Z * zs, b + Z * zs, b + Z * zt], TAS, V((b - t).y, -(b - t).x))
        return
    w, d = PAY_W['kare'], 0.055
    kutu(y, p - e * (w / 2) + nn * d + Z * z0, e, w, d, 0.03, 'kum_koyu', 'onsagsol')
    kutu(y, p - e * (w / 2) + nn * d + Z * (z0 + 0.03), e, w, d, h - 0.07, TAS, 'onsagsol')
    # a projecting course under the cap
    kutu(y, p - e * (w / 2 + 0.004) + nn * (d + 0.004) + Z * (z0 + h - 0.052), e, w + 0.008, d + 0.004, 0.01, 'kum_acik', 'onsagsolust')
    o = p - e * (w / 2) + Z * (z0 + h - 0.04)
    y.yuz_yon([o + nn * d, o + nn * d + e * w, o + e * w + Z * 0.034, o + Z * 0.034], 'kum_acik', nn + Z)
    y.yuz_yon([o + nn * d, o, o + Z * 0.034], 'kum_acik', -e)
    y.yuz_yon([o + e * w, o + nn * d + e * w, o + e * w + Z * 0.034], 'kum_acik', e)


def dis_duvar(a, b, h, turler, atla=None, uc0=0.075, uc1=0.075):
    """an outer wall a->b (facing its right), h high, its buttresses of the given kinds evenly spaced; between them
    an arrow slit, a string course and a water spout (çörten) under the parapet; atla = (u0, u1): leave that
    stretch (0..1) out (a portal stands there); uc0 / uc1: what the corner towers cover at the ends"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length; e = (b - a) / L; nn = V(e.y, -e.x)
    m = len(turler) + 1
    for k in range(m):
        u0, u1 = k / m, (k + 1) / m
        if atla and u1 > atla[0] and u0 < atla[1]:
            if u0 < atla[0]: duvar_dilim(a.lerp(b, u0), a.lerp(b, atla[0]), Z0, Z0 + h)
            if u1 > atla[1]: duvar_dilim(a.lerp(b, atla[1]), a.lerp(b, u1), Z0, Z0 + h)
            continue
        duvar_dilim(a.lerp(b, u0), a.lerp(b, u1), Z0, Z0 + h)
        # the bay between two buttresses
        s0 = u0 * L + (uc0 if k == 0 else PAY_W[turler[k - 1]] / 2) + 0.004
        s1 = u1 * L - (uc1 if k == m - 1 else PAY_W[turler[k]] / 2) - 0.004
        if s1 - s0 < 0.05: continue
        mid = a + e * ((s0 + s1) / 2)
        yarik(y, mid + nn * 0.001, e, nn, -0.006, Z0 + h * 0.36, 0.012, h * 0.24, 'koyu')
        # a sill under the slit and a hood over it
        kutu(y, mid - e * 0.014 + nn * 0.012 + Z * (Z0 + h * 0.36 - 0.006), e, 0.028, 0.012, 0.006, 'kum_acik', 'onsagsolust')
        # string course
        kutu(y, a + e * s0 + nn * 0.006 + Z * (Z0 + h * 0.68), e, s1 - s0, 0.006, 0.009, 'kum_acik', 'onsagsolust')
        # water spout under the cornice, tilted down
        sp = mid + e * 0.05 + Z * (Z0 + h - 0.028)
        cubuk(y, sp - nn * 0.004, sp + nn * 0.06 - Z * 0.01, 0.016, 'kum_koyu', 0.014)
        y.yuz_yon([sp + nn * 0.01 - e * 0.004 + Z * 0.0075, sp + nn * 0.056 - e * 0.004 - Z * 0.0025,
                   sp + nn * 0.056 + e * 0.004 - Z * 0.0025, sp + nn * 0.01 + e * 0.004 + Z * 0.0075], 'koyu', Z)
    for k in range(1, m):
        u = k / m
        if atla and atla[0] - 0.02 < u < atla[1] + 0.02: continue
        payanda(a.lerp(b, u), e, h, turler[k - 1])


def parapet_hat(kose, z=Z0 + HW, kapali=False):
    """a low parapet with a light coping on the wall line (outer face flush with the wall below)"""
    parapet(y, kose, z, PAR, 0, 0.022, TAS, kapali=kapali, ust_key='kum_acik')


def kose_kule(c, h, r=0.08):
    """an octagonal corner tower with a plinth, a string course, slits, a corbelled cornice and a stone cap"""
    y.prizma(c, r * 1.1, Z0, Z0 + 0.035, 'kum_koyu', n=8, kat=math.pi / 8, ust=False)
    for k in range(4):
        y.prizma(c, r, Z0 + 0.035 + (h - 0.035) * k / 4, Z0 + 0.035 + (h - 0.035) * (k + 1) / 4, TAS, n=8, kat=math.pi / 8, ust=False)
    halka_kornis(y, c, r, Z0 + h * 0.68, 0.009, 0.006, 8, 'kum_acik', kat=math.pi / 8)
    ring = cokgen(c, r, 8, math.pi / 8)
    for i in range(8):
        p, q = ring[i], ring[(i + 1) % 8]
        e = (q - p).normalized(); nn = V(e.y, -e.x)
        m = (p + q) / 2
        if (m - V(*c)).dot(V(*c).normalized()) > 0.01:
            yarik(y, m + nn * 0.001, e, nn, -0.005, Z0 + h * 0.4, 0.01, h * 0.18, 'koyu')
    konsol_halka(y, ring, Z0 + h - 0.03, 0.03, 0.014, 'kum_acik', 3)
    r2 = disa(ring, 0.014)
    parapet(y, r2, Z0 + h, 0.03, 0, 0.018, TAS, ust_key='kum_acik')
    y.yuz_yon([V(p.x, p.y, Z0 + h + 0.004) for p in disa(r2, -0.018)], 'kum_koyu', Z)
    y.koni(c, r * 0.72, Z0 + h + 0.004, 0.07, 'tas', n=8)
    kure(y, (c[0], c[1], Z0 + h + 0.078), 0.008, 'kum_acik', n=8, kat=4)


# ---------------- outer walls ----------------
y.bolum('Dış duvarlar, payandalar, köşe kuleleri')
PW, PH, PD = 0.56, 0.68, 0.13
pu = PW / 2 / (2 * XW) + 0.005
dis_duvar((-XW, YF), (XW, YF), HW, ['kare', 'ucgen', 'kare', 'ucgen', 'ucgen', 'kare', 'ucgen', 'kare'], atla=(0.5 - pu, 0.5 + pu))
dis_duvar((XW, YF), (XW, YH), HW, ['ucgen', 'kare', 'ucgen'])
dis_duvar((-XW, YH), (-XW, YF), HW, ['ucgen', 'kare', 'ucgen'])
dis_duvar((XW, YH), (XW, YB), HH, ['yarim', 'kare', 'yarim'])
dis_duvar((XW, YB), (-XW, YB), HH, ['yarim', 'kare', 'yarim', 'kare', 'yarim', 'kare', 'yarim'])
dis_duvar((-XW, YB), (-XW, YH), HH, ['yarim', 'kare', 'yarim'])
for sx in (-1, 1):
    kose_kule((sx * XW, YF), HW + 0.05)
    kose_kule((sx * XW, YB), HH + 0.05)
    # the hall rises above the court ranges: its front wall's ends above their roofs
    a, b = (V(sx * XW, YH), V(sx * IX, YH)) if sx > 0 else (V(sx * IX, YH), V(sx * XW, YH))
    duvar_dilim(a, b, Z0 + HW, Z0 + HH, n=1)
    payanda(V(sx * XW, YH), V(0, 1) if sx > 0 else V(0, -1), HH, 'kare')
# cornices and the parapets
silme(y, [V(-XW, YH), V(-XW, YF), V(XW, YF), V(XW, YH)], Z0 + HW - 0.016, 0.02, 0.012, 'kum_acik', 'tac', kapali=False)
silme(y, [V(XW, YH), V(XW, YB), V(-XW, YB), V(-XW, YH)], Z0 + HH - 0.016, 0.02, 0.012, 'kum_acik', 'tac', kapali=False)
silme(y, [V(-XW, YH), V(-XW, YF), V(XW, YF), V(XW, YH)], Z0, 0.03, 0.012, 'kum_koyu', 'kaide', kapali=False)
silme(y, [V(XW, YH), V(XW, YB), V(-XW, YB), V(-XW, YH)], Z0, 0.03, 0.012, 'kum_koyu', 'kaide', kapali=False)
parapet_hat([V(-XW, YH), V(-XW, YF), V(-PW / 2, YF)])
parapet_hat([V(PW / 2, YF), V(XW, YF), V(XW, YH)])

# ---------------- the great portal ----------------
y.bolum('Mukarnaslı taçkapı')


def portal(cx, cy, z0, en, H, derin, mk, kenar=True):
    """a Sultanhanı-type portal: the muqarnas niche of the library plus carved star bands on the outer border,
    lozenges on the inner border, blind niches flanking the arch, rosettes in the spandrels, an inscription panel,
    corner colonnettes and a row of corbels under the crowning cornice. Returns the top z"""
    top = tackapi_mukarnas(y, cx, cy, z0, en=en, H=H, derin=derin, nis=0.5, sivri=0.6, mk_kat=mk, key=TAS,
                           bordur=('kum_acik', 'mermer'), tonlar=('kum_acik', 'kum_koyu'), cerceve=(0.014, ['mermer', 'kum_koyu']))
    bw = en * 0.07
    zb = z0 + H - 0.016
    fo = cy - 0.006                    # the outer band's front
    # stars along the outer band (sides and top)
    n = max(3, int((zb - bw - z0 - 0.02) / (bw * 1.05)))
    for sx in (-1, 1):
        for i in range(n):
            zz = z0 + 0.03 + (zb - bw - z0 - 0.04) * (i + 0.5) / n
            yildiz((cx + sx * (en / 2 - bw / 2), fo, zz), X, -Y, bw * 0.4, 'mermer', yan_key='kum_koyu', kat=math.pi / 8)
    m = max(3, int((en - 2 * bw) / (bw * 1.05)))
    for i in range(m):
        xx = cx - en / 2 + bw + (en - 2 * bw) * (i + 0.5) / m
        yildiz((xx, fo, zb - bw / 2), X, -Y, bw * 0.4, 'mermer', yan_key='kum_koyu', kat=math.pi / 8)
    # lozenges on the inner band
    nis_w = 0.5 * en
    hw = nis_w / 2 + 0.012 + bw * 0.6
    apex = H * 0.88
    bi = bw * 0.55
    zi = z0 + apex + bw * 0.7
    for sx in (-1, 1):
        k = 0
        zz = z0 + 0.03
        while zz < zi - bi:
            eskenar((cx + sx * (hw - bi / 2), cy - 0.004, zz), X, -Y, bi * 0.42, 'kum_koyu' if k % 2 else 'kum_acik')
            zz += bi * 1.1; k += 1
    xx = cx - hw + bi * 1.2
    k = 0
    while xx < cx + hw - bi:
        eskenar((xx, cy - 0.004, zi - bi / 2), X, -Y, bi * 0.42, 'kum_koyu' if k % 2 else 'kum_acik')
        xx += bi * 1.1; k += 1
    # blind niches between the two borders, two tiers a side
    gx = (en / 2 - bw + hw) / 2
    gw = (en / 2 - bw) - hw - 0.012
    if gw > 0.025:
        for sx in (-1, 1):
            for zz, hh in ((z0 + 0.05, H * 0.3), (z0 + 0.07 + H * 0.3, H * 0.28)):
                kemer_pano((cx + sx * gx, cy, zz), X, -Y, gw, hh, 'kum_koyu', 'kum_acik')
    # rosettes in the spandrels above the arch
    for sx in (-1, 1):
        yildiz((cx + sx * hw * 0.62, cy - 0.0025, z0 + apex - 0.035), X, -Y, 0.016, 'mermer', k=12, ic=0.72, yan_key='kum_koyu')
    # corner colonnettes up the block's front edges, with capitals
    for sx in (-1, 1):
        c = (cx + sx * (en / 2 + 0.002), cy + 0.002)
        y.prizma(c, 0.011, z0, z0 + 0.03, 'kum_acik', n=8)
        y.prizma(c, 0.008, z0 + 0.03, zb - 0.03, 'kum_acik', n=8, ust=False)
        y.prizma(c, 0.012, zb - 0.03, zb - 0.012, 'kum_acik', n=8)
        for zz in (z0 + (zb - z0) * 0.35, z0 + (zb - z0) * 0.7):
            y.prizma(c, 0.0105, zz, zz + 0.008, 'kum_acik', n=8)
    # corbels (a dentil row) under the crowning cornice
    nk = int(en / 0.03)
    for i in range(nk):
        xx = cx - en / 2 + en * (i + 0.5) / nk
        kutu_merkez(y, (xx, cy - 0.006), 0.012, 0.012, 0.012, 'kum_koyu', z0=zb - 0.03, yuzler='onarkasagsolust')
    return top


top_p = portal(0, YF - PD, Z0, PW, PH, PD, 7)
duz_duvar(y, V(PW / 2, YF), V(-PW / 2, YF), Z0 + HW, Z0 + PH, TAS)
# the portal's back above the roof: a blind panel and a coping, so it does not read as a bare slab from behind
kemer_pano((0, YF + 0.0005, Z0 + HW + PAR + 0.04), -X, Y, 0.18, PH - HW - PAR - 0.1, 'kum_koyu', 'kum_acik')

# ---------------- court ranges ----------------
y.bolum('Avlu: revaklı ahırlar (doğu)')
arkad(y, V(IX, YH), V(IX, IYF), 4, Z0, HW, en=0.8, ust=0.03, sivri=0.65, derin=XW - IX - 0.03, sutunlu=False,
      cerceve=(0.01, ['kum_acik', 'kum_koyu']))
y.bolum('Avlu: oda kapıları (batı ve ön)')
for k in range(4):
    p, q = V(-IX, IYF).lerp(V(-IX, YH), k / 4), V(-IX, IYF).lerp(V(-IX, YH), (k + 1) / 4)
    y.kemerli(p, q, Z0, HW, (TAS, 'kum_koyu', 'kum_acik', 'ahsap'), v0=0.0, en=0.36, ust=HW * 0.36, derin=0.02, k_say=8, sivri=0.6,
              cerceve=(0.008, ['kum_acik', 'kum_koyu']))
FR = [V(IX, IYF), V(-IX, IYF)]
for k in range(5):
    p, q = FR[0].lerp(FR[1], k / 5), FR[0].lerp(FR[1], (k + 1) / 5)
    if k == 2:      # the passage from the portal (a tall open vault)
        y.kemerli(p, q, Z0, HW, (TAS, 'kum_koyu', 'kum_acik', 'koyu'), v0=0.0, en=0.7, ust=0.03, derin=0.05, k_say=10, sivri=0.6,
                  cerceve=(0.012, ['kum_acik', 'kum_koyu']))
    else:
        y.kemerli(p, q, Z0, HW, (TAS, 'kum_koyu', 'kum_acik', 'ahsap'), v0=0.0, en=0.34, ust=HW * 0.36, derin=0.02, k_say=8, sivri=0.6,
                  cerceve=(0.008, ['kum_acik', 'kum_koyu']))
# roofs of the ranges (flat stone terraces), the court-side cornice and parapet
for (x0, x1, y0, y1) in ((-XW, XW, YF, IYF), (IX, XW, IYF, YH), (-XW, -IX, IYF, YH)):
    y.yuz_yon([V(x0, y0, Z0 + HW + 0.004), V(x1, y0, Z0 + HW + 0.004), V(x1, y1, Z0 + HW + 0.004), V(x0, y1, Z0 + HW + 0.004)], 'tas', Z)
ICK = [V(-IX, YH), V(-IX, IYF), V(IX, IYF), V(IX, YH)][::-1]
silme(y, ICK, Z0 + HW - 0.012, 0.016, 0.01, 'kum_acik', 'tac', kapali=False)
parapet(y, disa(ICK, 0.0, False), Z0 + HW, 0.014, 0, 0.016, TAS, kapali=False, ust_key='kum_acik')
# light domes (tepe pencereleri) over the rooms
for (cx, cy) in ((-0.82, -0.12), (-0.82, -0.42), (-0.5, -0.78), (0.5, -0.78), (0.82, -0.3)):
    kucuk_kubbe(y, cx, cy, Z0 + HW + 0.004, 0.034, kasnak=0.02, n=16, son=False, key='kum_acik', kasnak_key=TAS)
# the terrace roofs drain through spouts into the court
for k in range(4):
    for x, s in ((IX, -1), (-IX, 1)):
        yy = IYF + (YH - IYF) * (k + 0.5) / 4
        p = V(x, yy, Z0 + HW - 0.02)
        cubuk(y, p + V(-s * 0.004, 0, 0), p + V(s * 0.05, 0, -0.008), 0.013, 'kum_koyu', 0.012)

# ---------------- the hall's front wall (on the court) and its portal ----------------
y.bolum('Kışlık bölümün avlu cephesi ve kapısı')
HPW = 0.34
for xa, xb in ((-IX, -HPW / 2), (HPW / 2, IX)):
    for j in range(2):
        p, q = V(xa + (xb - xa) * j / 2, YH), V(xa + (xb - xa) * (j + 1) / 2, YH)
        # (running +x the face is on the right: towards the court, -y)
        L_, x0, x1, hs, apex = kemer_nis(y, p, q, Z0, HH, en=0.74, ust=0.04, sivri=0.6, derin=0.016, key=TAS, yan_key='kum_koyu',
                                         alt_key='kum_acik', arka_key=TAS, v0=0.02, k_say=10, cerceve=(0.008, ['kum_acik', 'kum_koyu']))
        m = (p + q) / 2
        yarik(y, V(m.x, YH + 0.016 - 0.001), X, -Y, -0.006, Z0 + HH * 0.45, 0.012, HH * 0.22, 'koyu')
silme(y, [V(-IX, YH), V(IX, YH)], Z0 + HH - 0.016, 0.02, 0.012, 'kum_acik', 'tac', kapali=False)
silme(y, [V(-IX, YH), V(IX, YH)], Z0, 0.02, 0.008, 'kum_koyu', 'kaide', kapali=False)
top_h = portal(0, YH - 0.08, Z0, HPW, HH + 0.1, 0.08, 5)
duz_duvar(y, V(HPW / 2, YH), V(-HPW / 2, YH), Z0 + HH, Z0 + HH + 0.1, TAS)

# ---------------- the winter hall's roofs ----------------
y.bolum('Kışlık: sırtlı taş çatılar')
NX = 0.21
ZH = Z0 + HH
y.yuz_yon([V(-XW, YH, ZH), V(XW, YH, ZH), V(XW, YB, ZH), V(-XW, YB, ZH)], 'kum_acik', Z)
for sx in (-1, 1):
    x0, x1 = sorted((sx * XW, sx * NX))
    cati_besik(y, x0, x1, YH, YB, ZH, 0.1, 0.022, 'tas', 'tas_acik', kalinlik=0.014, alt_key='kum_acik', ucluk_key=TAS, uc_sacak=0.014,
               nr=10, dilim=['tas', 'tas_acik'], mahya_en=0.016)
# the raised nave: clerestory walls with small windows, its own pitched roof
ZN = ZH + 0.13
for sx in (-1, 1):
    a, b = (V(sx * NX, YH), V(sx * NX, YB)) if sx > 0 else (V(sx * NX, YB), V(sx * NX, YH))
    n = 5
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        y.kemerli(p, q, ZH, ZN - ZH, (TAS, 'kum_koyu', 'kum_acik', 'koyu'), v0=0.05, en=0.22, ust=0.02, derin=0.012, k_say=6, sivri=0.6,
                  cerceve=(0.006, 'kum_acik'))
for yy, s in ((YH, -1), (YB, 1)):
    a, b = (V(-NX, yy), V(NX, yy)) if s < 0 else (V(NX, yy), V(-NX, yy))
    duvar_dilim(a, b, ZH, ZN, n=2)
silme(y, dikdortgen(-NX, NX, YH, YB), ZN - 0.012, 0.014, 0.01, 'kum_acik', 'tac')
cati_besik(y, -NX, NX, YH, YB, ZN, 0.11, 0.022, 'tas', 'tas_acik', kalinlik=0.014, alt_key='kum_acik', ucluk_key=TAS, uc_sacak=0.014,
           nr=10, dilim=['tas', 'tas_acik'], mahya_en=0.016)
# the gable ends: a stone finial on the apex
for (x0, x1) in ((-XW, -NX), (NX, XW), (-NX, NX)):
    zz = ZN if x0 == -NX else ZH
    hh = 0.11 if x0 == -NX else 0.1
    xm = (x0 + x1) / 2
    for yy, s in ((YH, -1), (YB, 1)):
        kure(y, (xm, yy + s * 0.004, zz + hh + 0.026), 0.009, 'kum_acik', n=8, kat=4)

# the central dome's drum (octagonal, blind-arcaded, colonnettes on the corners), its stone cone and the lantern
y.bolum('Kışlık: orta kubbe kasnağı, külah ve fener')
KC = (0.0, (YH + YB) / 2)
kr = 0.16
ok = cokgen(KC, kr, 8, math.pi / 8)
zk = ZN + 0.04
y.prizma(KC, kr, ZH, zk, TAS, n=8, kat=math.pi / 8, ust=False)
for i in range(8):
    y.kemerli(ok[i], ok[(i + 1) % 8], zk, 0.11, (TAS, 'kum_koyu', 'kum_acik', 'koyu'), v0=0.02, en=0.42, ust=0.018, derin=0.016, k_say=6,
              sivri=0.65, cerceve=(0.006, ['kum_acik', 'kum_koyu']))
    y.prizma((ok[i].x, ok[i].y), 0.008, zk, zk + 0.11, 'kum_acik', n=6)
halka_kornis(y, KC, kr, zk - 0.006, 0.01, 0.008, 8, 'kum_acik', kat=math.pi / 8)
konsol_halka(y, ok, zk + 0.11, 0.024, 0.016, 'kum_acik', 3)
zc = zk + 0.134
ok2 = disa(ok, 0.016)
y.yuz_yon([V(p.x, p.y, zc) for p in ok2], 'kum_acik', -Z)
# the cone: eight faces of stone courses, each face in alternate light / dark rows
tepe = V(KC[0], KC[1], zc + 0.17)
lr = 0.038
for i in range(8):
    p, q = ok2[i], ok2[(i + 1) % 8]
    nr = 6
    for k in range(nr):
        t0, t1 = k / nr, (k + 1) / nr
        r0, r1 = 1 - t0 * (1 - lr / kr), 1 - t1 * (1 - lr / kr)
        P = lambda pt, t, r: V(KC[0] + (pt.x - KC[0]) * r, KC[1] + (pt.y - KC[1]) * r, zc + 0.17 * t)
        y.yuz_yon([P(p, t0, r0), P(q, t0, r0), P(q, t1, r1), P(p, t1, r1)], 'tas' if k % 2 == 0 else 'tas_acik', (p + q) / 2 - V(*KC) + Z * 0.6)
    # ribs on the cone's edges
    cubuk(y, V(p.x, p.y, zc + 0.002), V(KC[0] + (p.x - KC[0]) * lr / kr, KC[1] + (p.y - KC[1]) * lr / kr, zc + 0.17), 0.006, 'kum_acik', 0.004)
# the lantern on top (the dome's oculus): eight little open arches, a cap and a knob
zl = zc + 0.17
okl = cokgen(KC, lr, 8, math.pi / 8)
for i in range(8):
    y.kemerli(okl[i], okl[(i + 1) % 8], zl, 0.05, ('kum_acik', 'kum_koyu', 'kum_acik', 'koyu'), v0=0.006, en=0.55, ust=0.008, derin=0.01, k_say=4, sivri=0.6)
halka_kornis(y, KC, lr, zl + 0.05, 0.008, 0.007, 8, 'kum_acik', kat=math.pi / 8)
y.koni(KC, lr * 1.05, zl + 0.058, 0.05, 'tas', n=8)
kure(y, (KC[0], KC[1], zl + 0.115), 0.01, 'kum_acik', n=8, kat=4)

# ---------------- the köşk mescit ----------------
y.bolum('Köşk mescit (dört kemer üstünde)')
MC = (0.0, (IYF + YH) / 2 - 0.02)
MS = 0.13          # half size
H1, H2 = 0.15, 0.1
mk = dikdortgen(MC[0] - MS, MC[0] + MS, MC[1] - MS, MC[1] + MS)
mi = disa(mk, -0.03)
kutu(y, V(MC[0] - MS - 0.02, MC[1] - MS - 0.02, Z0), X, 2 * MS + 0.04, 2 * MS + 0.04, 0.02, 'kum_koyu', 'onarkasagsolust')
z1 = Z0 + 0.02
for i in range(4):
    a, b = mk[i], mk[(i + 1) % 4]
    kemer_nis(y, a, b, z1, H1, en=0.64, ust=0.025, sivri=0.6, derin=0.03, key=TAS, yan_key='kum_acik',
              cerceve=(0.012, ['mermer', 'kum_koyu']), k_say=12)
    ai, bi = mi[i], mi[(i + 1) % 4]
    kemer_nis(y, bi, ai, z1, H1, en=0.64 * (b - a).length / (bi - ai).length, ust=0.025, sivri=0.6, derin=0.001, key='kum_koyu', yan_key='kum_koyu')
    # carved star panels on the piers' faces and a fluted capital band
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for u in (0.09, 0.91):
        p = a.lerp(b, u)
        yildiz((p.x, p.y, z1 + H1 * 0.45), e, nn, 0.014, 'mermer', yan_key='kum_koyu', kat=math.pi / 8)
y.yuz_yon([V(p.x, p.y, z1 + H1) for p in mi], 'kum_koyu', -Z)
z2 = z1 + H1
konsol_halka(y, mk, z2 - 0.012, 0.018, 0.014, 'kum_acik', 3)
pencereli_duvar(y, mk, z2 + 0.006, H2, [2, 2, 2, 2], en=0.4, v0=0.025, ust=0.02, sivri=0.6, derin=0.014, cerceve=(0.006, ['kum_acik', 'kum_koyu']))
duvarlar(y, mk, z2, z2 + 0.006, TAS)
# a carved frieze of stars under the cornice
for i in range(4):
    a, b = mk[i], mk[(i + 1) % 4]
    e = (b - a).normalized(); nn = V(e.y, -e.x)
    for k in range(7):
        p = a.lerp(b, (k + 0.5) / 7)
        yildiz((p.x, p.y, z2 + 0.006 + H2 - 0.022), e, nn, 0.0085, 'kum_acik', kat=math.pi / 8)
silme(y, mk, z2 + 0.006 + H2 - 0.01, 0.014, 0.012, 'kum_acik', 'tac')
zt = z2 + 0.006 + H2
y.yuz_yon([V(p.x, p.y, zt + 0.004) for p in mk], 'kum_koyu', Z)
parapet(y, mk, zt, 0.018, 0, 0.012, TAS, ust_key='kum_acik')
kubbe_kasnakli(y, MC, 0.085, zt + 0.004, 0.04, n_pencere=8, kubbe_h=0.075, key='kursun', duvar=(TAS, 'kum_koyu', 'kum_acik', 'koyu'), n=32, kat=8, en=0.4, alem_olcek=0.6, cerceve=None)
# its stair (up the side, to a door in the upper room)
merdiven(y, (MC[0] + MS + 0.025, MC[1] + MS - 0.01), -math.pi / 2, 0.045, Z0, z2, n=7, d=0.03, key=TAS, yanlik='kum_acik')

# ---------------- the court: paving, trough, well, goods ----------------
y.bolum('Avlu: döşeme, yalak, kuyu, yükler')
# paved walks: from the passage to the köşk and on to the hall's portal, and across
for (xa, xb, ya, yb) in ((-0.07, 0.07, IYF, MC[1] - MS - 0.02), (-0.07, 0.07, MC[1] + MS + 0.02, YH - 0.08), (-IX, -MS - 0.02, MC[1] - 0.05, MC[1] + 0.05),
                         (MS + 0.07, IX, MC[1] - 0.05, MC[1] + 0.05)):
    y.yuz_yon([V(xa, ya, Z0 + 0.002), V(xb, ya, Z0 + 0.002), V(xb, yb, Z0 + 0.002), V(xa, yb, Z0 + 0.002)], 'tas_koyu', Z)
havuz(y, -0.5, -0.32, -0.5, -0.43, Z0, derin=0.02, kenar=0.015, key=TAS)
# the well: a round stone kerb with a windlass
WC = (0.42, -0.2)
y.prizma(WC, 0.042, Z0, Z0 + 0.045, TAS, n=12, ust=False)
y.prizma(WC, 0.046, Z0 + 0.045, Z0 + 0.052, 'kum_acik', n=12, ust=False)
y.yuz_yon([V(WC[0] + 0.046 * math.cos(TAU * i / 12), WC[1] + 0.046 * math.sin(TAU * i / 12), Z0 + 0.052) for i in range(12)], 'koyu', Z)
for sx in (-1, 1):
    cubuk(y, V(WC[0] + sx * 0.038, WC[1], Z0 + 0.05), V(WC[0] + sx * 0.038, WC[1], Z0 + 0.12), 0.008, 'ahsap_koyu')
boru(y, [V(WC[0] - 0.045, WC[1], Z0 + 0.11), V(WC[0] + 0.045, WC[1], Z0 + 0.11)], 0.009, 'ahsap', n=6)
cati_besik(y, WC[0] - 0.05, WC[0] + 0.05, WC[1] - 0.035, WC[1] + 0.035, Z0 + 0.125, 0.035, 0.01, 'kiremit', 'kiremit2', kalinlik=0.006, ucluk_key='ahsap_koyu', alt_key='ahsap_koyu')


def denk(cx, cy, z, key='kumas', aci=0.0, w=0.06, d=0.045, h=0.035):
    """a corded bale of goods"""
    kutu_merkez(y, (cx, cy), w, d, h, key, z0=z, aci=aci)
    ca, sa = math.cos(aci), math.sin(aci)
    for t in (-0.25, 0.25):
        o = V(cx + ca * w * t, cy + sa * w * t)
        e = V(-sa, ca)
        cubuk(y, o - e * (d / 2 + 0.002) + Z * (z + h + 0.002), o + e * (d / 2 + 0.002) + Z * (z + h + 0.002), 0.004, 'ahsap_koyu', 0.002)


def kup(cx, cy, z, r=0.018, h=0.05, key='kiremit'):
    """a clay storage jar"""
    donel(y, (cx, cy), [(0.0, z), (r * 0.6, z), (r, z + h * 0.35), (r * 0.85, z + h * 0.75), (r * 0.45, z + h * 0.9), (r * 0.5, z + h), (0.0, z + h)], key, n=10)


# goods in the stalls: bales, crates and jars
for k, (yy, tur) in enumerate(((-0.56, 'denk'), (-0.4, 'sandik'), (-0.24, 'kup'), (-0.08, 'denk'))):
    cx = IX + 0.12
    if tur == 'denk':
        denk(cx, yy - 0.028, Z0, 'kumas'); denk(cx, yy + 0.028, Z0, 'boya_kirmizi'); denk(cx + 0.005, yy, Z0 + 0.035, 'kece')
    elif tur == 'sandik':
        kutu_merkez(y, (cx, yy), 0.06, 0.06, 0.05, 'ahsap', z0=Z0)
        kutu_merkez(y, (cx + 0.01, yy + 0.005), 0.045, 0.045, 0.04, 'ahsap_acik', z0=Z0 + 0.05, aci=0.3)
    else:
        for dx, dy in ((0, -0.03), (0.0, 0.03), (0.04, 0.0)):
            kup(cx + dx - 0.02, yy + dy, Z0)


# ---------------- camels ----------------
def deve(x, yy, aci, renk='ahsap_acik', yuk=True, cul='boya_kirmizi'):
    """a stylised dromedary (head towards +x before turning) on long legs, a hump, a curved neck; yuk: bales slung on
    both sides over a saddle cloth"""
    with parca(y, (x, yy, Z0), aci, 1.35):
        h = 0.075
        boru(y, [V(-0.045, 0, h + 0.012), V(-0.01, 0, h + 0.02), V(0.03, 0, h + 0.018), V(0.048, 0, h + 0.012)], 0.02, renk, n=8)
        kure(y, (-0.045, 0, h + 0.012), 0.019, renk, n=8, kat=4)
        kure(y, (0.046, 0, h + 0.013), 0.018, renk, n=8, kat=4)
        donel(y, (-0.004, 0), [(0.026, h + 0.02), (0.022, h + 0.04), (0.012, h + 0.054), (0.0, h + 0.058)], renk, n=10)   # hump
        boru(y, [V(0.05, 0, h + 0.016), V(0.082, 0, h + 0.004), V(0.102, 0, h + 0.026), V(0.106, 0, h + 0.05)], 0.009, renk, n=6, r_son=0.007)
        boru(y, [V(0.102, 0, h + 0.054), V(0.13, 0, h + 0.047)], 0.009, renk, n=6, r_son=0.006)      # head
        for s in (-1, 1):
            cubuk(y, V(0.104, s * 0.006, h + 0.06), V(0.101, s * 0.007, h + 0.069), 0.003, renk)
        boru(y, [V(-0.062, 0, h + 0.02), V(-0.07, 0, h - 0.005), V(-0.068, 0, h - 0.02)], 0.0025, 'ahsap_koyu', n=4, r_son=0.0015)
        for lx in (-0.04, 0.038):
            for s in (-1, 1):
                boru(y, [V(lx, s * 0.01, h + 0.004), V(lx + 0.004, s * 0.01, h * 0.5), V(lx, s * 0.01, 0.006)], 0.0055, renk, n=5, r_son=0.004)
                kutu_merkez(y, (lx + 0.003, s * 0.01), 0.012, 0.01, 0.006, 'ahsap_koyu')
        if yuk:
            kutu_merkez(y, (-0.004, 0), 0.05, 0.05, 0.004, cul, z0=h + 0.03)
            for s in (-1, 1):
                kutu_merkez(y, (-0.004, s * 0.034), 0.05, 0.026, 0.04, 'kumas' if s > 0 else 'kece', z0=h - 0.005)
                cubuk(y, V(-0.03, s * 0.048, h + 0.03), V(0.022, s * 0.048, h + 0.03), 0.003, 'ahsap_koyu', 0.003)
            denk(-0.004, 0, h + 0.056, 'boya_sari', w=0.04, d=0.03, h=0.02)


y.bolum('Kervan: yol, develer, yükler')
# the caravan road across the forecourt to the portal's steps, its kerbs
ROAD = 0.15
y.yuz_yon([V(-ROAD, YF - 0.36, Z0 + 0.002), V(ROAD, YF - 0.36, Z0 + 0.002), V(ROAD, YF - 0.16, Z0 + 0.002), V(-ROAD, YF - 0.16, Z0 + 0.002)], 'toprak', Z)
# a line of laden camels on the road, one kneeling to be unloaded before the portal
deve(-0.06, YF - 0.27, math.pi / 2 + 0.1)
deve(0.07, YF - 0.3, math.pi / 2 - 0.05, renk='kum_koyu', cul='turkuaz')
deve(-0.4, -0.3, 0.6, renk='kum_koyu', cul='turkuaz')
deve(0.34, -0.52, 2.6, yuk=False)
# goods unloaded outside, the long trough and hitching posts
for (cx, cy, key, a) in ((-0.36, YF - 0.2, 'kumas', 0.2), (-0.3, YF - 0.24, 'boya_kirmizi', -0.3), (-0.33, YF - 0.2, 'kece', 0.1)):
    denk(cx, cy, Z0, key, a)
denk(-0.33, YF - 0.21, Z0 + 0.035, 'boya_sari', 0.4, w=0.05, d=0.04, h=0.03)
for (cx, cy) in ((-0.42, YF - 0.27), (-0.39, YF - 0.3)):
    kup(cx, cy, Z0)
kutu(y, V(-0.72, YF - 0.13, Z0), X, 0.24, 0.05, 0.035, 'kum_koyu', 'onarkasagsol')
y.yuz_yon([V(-0.71, YF - 0.12, Z0 + 0.03), V(-0.49, YF - 0.12, Z0 + 0.03), V(-0.49, YF - 0.09, Z0 + 0.03), V(-0.71, YF - 0.09, Z0 + 0.03)], 'su', Z)
for k in range(4):
    x = 0.4 + k * 0.08
    y.prizma((x, YF - 0.13), 0.007, Z0, Z0 + 0.07, 'ahsap_koyu', n=6)
cubuk(y, V(0.4, YF - 0.13, Z0 + 0.06), V(0.64, YF - 0.13, Z0 + 0.06), 0.006, 'ahsap', 0.006)
for (tx, ty) in ((-0.95, YF - 0.25), (0.95, YF - 0.25), (-0.75, YF - 0.3)):
    agac(y, tx, ty, Z0, boy=0.15, tur='yaprakli')
sancak(y, PW * 0.32, YF - PD * 0.5, top_p, boy=0.2, en=0.11, yuk=0.07, aci=0.0)

calistir(y, 'lm_kervansaray')
