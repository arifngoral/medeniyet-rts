# Shared helpers for the English landmarks (lm_manor, lm_okcutalim, lm_westminster, lm_londrakulesi): walls with
# square-headed openings, Tudor mullioned windows with hood moulds, close-studded timber storeys, twisted brick
# chimney shafts on a stack, canted bay windows (oriels), hedges, a Perpendicular church tower, longbowmen.
import math
from mathutils import Vector
from parcalar import *
from frank_ortak import kutu3, levha, yari_ahsap, insan, at, hac, zemin_blok, cayir_renk, alcak_duvar


def eksen(a, b):
    """a, b as 2D points, the length, the unit direction and the outward normal (right of a->b)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    e = (b - a) / L
    return a, b, L, e, V(e.y, -e.x)


def acikli_duvar(y, a, b, z0, z1, aciklar, renk=('tas', 'tas_koyu', 'tas_acik', 'cam'), derin=0.012, cerceve=None, pay=0.003):
    """a wall a->b (facing the right) from z0 to z1 with square-headed openings: aciklar = [(u, w, v0, v1), ...]
    u the centre (0..1 along), w the width, v0..v1 the height above z0. Plain wall between them. Returns, for each
    opening, (pa, pb, v0, v1, e, nc): its two jambs (2D, on the wall line)"""
    a, b, L, e, nc = eksen(a, b)
    out = []
    u = 0.0
    m = pay / L
    for (uc, w, v0, v1) in sorted(aciklar):
        u0, u1 = uc - w / 2 / L, uc + w / 2 / L
        b0, b1 = u0 - m, u1 + m
        if b0 > u + 1e-6:
            duz_duvar(y, a.lerp(b, u), a.lerp(b, b0), z0, z1, renk[0])
        bw = b1 - b0
        dikdortgen_acik(y, a.lerp(b, b0), a.lerp(b, b1), z0, z1 - z0, m / bw, 1 - m / bw, v0, v1, renk, derin=derin, cerceve=cerceve)
        out.append((a.lerp(b, u0), a.lerp(b, u1), v0, v1, e, nc))
        u = b1
    if u < 1 - 1e-6:
        duz_duvar(y, a.lerp(b, u), b, z0, z1, renk[0])
    return out


def tudor_pencere(y, ac, z0, derin=0.012, key='tas_acik', n=None, transom=True, hood=True, kalin=0.0045, hood_key=None):
    """mullions (and a transom) in an opening from acikli_duvar, set in its reveal; hood: a label moulding over it with
    returned ends (stone walls)"""
    pa, pb, v0, v1, e, nc = ac
    w = (pb - pa).length
    n = n or max(1, int(round(w / 0.024)))
    d = derin * 0.45
    for k in range(1, n):
        p = pa.lerp(pb, k / n) - nc * d
        cubuk(y, p + Z * (z0 + v0), p + Z * (z0 + v1), kalin, key, kalin * 0.9)
    if transom and v1 - v0 > 0.05:
        vt = v0 + (v1 - v0) * 0.64
        cubuk(y, pa - nc * d + Z * (z0 + vt), pb - nc * d + Z * (z0 + vt), kalin, key, kalin * 0.9)
    if hood:
        hk = hood_key or key
        m = (pa + pb) / 2
        kutu3(y, m + nc * 0.004 + Z * (z0 + v1 + 0.007), e, nc, Z, w + 0.016, 0.008, 0.006, hk, ('+x', '-x', '+y', '+z', '-z'))
        for p, s in ((pa, -1), (pb, 1)):
            kutu3(y, p + e * (s * 0.006) + nc * 0.004 + Z * (z0 + v1 - 0.002), e, nc, Z, 0.004, 0.008, 0.012, hk, ('+x', '-x', '+y', '-z'))


def ahsap_kat(y, a, b, z0, z1, aciklar, duvar='siva', ahsap='ahsap_koyu', aralik=0.026, derin=0.01, capraz=False, mullion=True,
              ek_bos=()):
    """a close-studded timber storey a->b: plastered infill, the openings (timber reveals, dark glass), studs, rails,
    mullions in the openings. ek_bos: (u, w) stretches kept clear of timbers without an opening (an oriel in front)"""
    acs = acikli_duvar(y, a, b, z0, z1, aciklar, (duvar, ahsap, 'ahsap_acik', 'cam'), derin=derin)
    a2, b2, L, e, nc = eksen(a, b)
    bos = []
    for (pa, pb, v0, v1, e_, nc_) in acs:
        bos.append(((pa - a2).length / L, (pb - a2).length / L, v0, v1))
    for (u, w) in ek_bos:
        bos.append((u - w / 2 / L, u + w / 2 / L, -0.01, z1 - z0 + 0.01))
    yari_ahsap(y, a2, b2, z0, z1, bos, ahsap, aralik=aralik, en=0.006, capraz=capraz, orta=True)
    if mullion:
        for ac in acs:
            tudor_pencere(y, ac, z0, derin, ahsap, hood=False)
    return acs


def burgu(y, cx, cy, z0, h, r, tur=0.75, kat=10, keys=('tugla', 'tugla_koyu'), n=8, oran=0.78, faz=0.0):
    """one twisted (spiral-fluted) brick chimney shaft: a star section turning tur times as it rises, a moulded base
    and a flared, corbelled cap. Returns the top z"""
    ring = lambda k: [V(cx + (r if i % 2 == 0 else r * oran) * math.cos(faz + TAU * (i / n + tur * k / kat)),
                        cy + (r if i % 2 == 0 else r * oran) * math.sin(faz + TAU * (i / n + tur * k / kat)), z0 + h * k / kat) for i in range(n)]
    rs = [ring(k) for k in range(kat + 1)]
    for k in range(kat):
        for i in range(n):
            j = (i + 1) % n
            y.yuz([rs[k][i], rs[k][j], rs[k + 1][j], rs[k + 1][i]], keys[(i // 2) % 2] if n > 4 else keys[i % 2])
    # foot: a round moulding
    donel(y, (cx, cy), [(r * 1.18, z0 - 0.006), (r * 1.22, z0), (r * 1.02, z0 + 0.006)], keys[0], n=n * 2)
    zt = z0 + h
    donel(y, (cx, cy), [(r * 0.96, zt - 0.002), (r * 1.25, zt + 0.006), (r * 1.25, zt + 0.012), (r * 1.08, zt + 0.015), (r * 1.4, zt + 0.022),
                         (r * 1.4, zt + 0.028), (r * 1.1, zt + 0.03)], keys[0], n=n)
    y.yuz_yon([V(p.x, p.y, zt + 0.03) for p in cokgen((cx, cy), r * 1.1, n)], 'koyu', Z)
    return zt + 0.03


def baca(y, cx, cy, z_alt, z_ust, w, d, n_sutun=3, sutun_h=0.11, aci=0.0, key='tugla', tas='tas_acik', r=None):
    """a brick chimney stack w x d (w along the turned x) from z_alt to z_ust with a stone weathering band, and a row
    of n_sutun twisted shafts on it (each with its own pattern). Returns the top z"""
    with parca(y, (cx, cy, 0), aci):
        kutu_merkez(y, (0, 0), w, d, z_ust - z_alt, key, z0=z_alt)
        silme(y, dikdortgen(-w / 2, w / 2, -d / 2, d / 2), z_ust - 0.008, 0.008, 0.005, tas, 'duz')
        y.yuz_yon([V(-w / 2 + 0.002, -d / 2 + 0.002, z_ust + 0.0005), V(w / 2 - 0.002, -d / 2 + 0.002, z_ust + 0.0005),
                   V(w / 2 - 0.002, d / 2 - 0.002, z_ust + 0.0005), V(-w / 2 + 0.002, d / 2 - 0.002, z_ust + 0.0005)], tas, Z)
        rr = r or min(d * 0.36, w / n_sutun * 0.36)
        top = z_ust
        for k in range(n_sutun):
            x = -w / 2 + w * (k + 0.5) / n_sutun
            pat = [(0.75, 8, 0.78), (-0.6, 8, 0.8), (1.0, 6, 0.72), (0.0, 8, 0.82)][k % 4]
            top = burgu(y, x, 0, z_ust + 0.001, sutun_h, rr, tur=pat[0], n=pat[1], oran=pat[2], faz=0.3 * k,
                        keys=(key, 'tugla_koyu') if k % 2 == 0 else ('tugla_koyu', key))
    return top


def cumba(y, c, e, z0, h, w, d, duvar='tas', ic='tas_koyu', cam='cam', mullion='tas_acik', ust='kursun', parapet=True,
          alt=None, n_on=None, v0=0.012, v1=None, ahsap=False, taban=None):
    """a canted bay window (oriel) on a wall at c (2D, on the wall line), e along the wall (the wall faces right of
    e), from z0 h high, w wide at the wall, d deep: three windowed faces, a flat lead top with a moulded (and, if
    parapet, crenellated) edge; alt: a key for a corbelled underside (an oriel standing out from an upper storey)"""
    c = V(c[0], c[1]); e = V(e[0], e[1]).normalized(); nc = V(e.y, -e.x)
    k = d * 0.65
    P = [c - e * (w / 2), c - e * (w / 2 - k) + nc * d, c + e * (w / 2 - k) + nc * d, c + e * (w / 2)]
    v1 = v1 if v1 is not None else h - 0.012
    renk = (duvar, ic, mullion if not ahsap else 'ahsap_acik', cam)
    for i in range(3):
        pa, pb = P[i], P[i + 1]
        L = (pb - pa).length
        ww = L * (0.72 if i == 1 else 0.56)
        acs = acikli_duvar(y, pa, pb, z0, z0 + h, [(0.5, ww, v0, v1)], renk, derin=0.008, pay=0.002)
        for ac in acs:
            tudor_pencere(y, ac, z0, 0.008, mullion, n=(n_on if i == 1 and n_on else None), hood=False, kalin=0.004)
    top = [V(p.x, p.y, z0 + h) for p in P]
    y.yuz_yon(top, ust, Z)
    silme(y, P, z0 + h - 0.008, 0.01, 0.006, mullion if not ahsap else 'ahsap_koyu', 'tac', kapali=False)
    if parapet:
        pd = disa(P, 0.006, kapali=False)
        for i in range(3):
            mazgal(y, pd[i], pd[i + 1], z0 + h + 0.002, 0.016, 0.008, duvar, dis_en=0.014, bosluk=0.01)
    if alt:
        # corbelled underside: a sloping soffit down to a point on the wall
        tip = c + Z * (z0 - d * 1.3)
        for i in range(3):
            pa, pb = V(P[i].x, P[i].y, z0), V(P[i + 1].x, P[i + 1].y, z0)
            m = (pa + pb) / 2
            y.yuz_yon([pa, pb, tip], alt, V(m.x - c.x, m.y - c.y, -0.8))
    elif taban:
        y.yuz_yon([V(p.x, p.y, z0) for p in P], taban, -Z)
    return z0 + h


def cit(y, a, b, h, t=0.022, key='yesil_koyu', z=0.0):
    """a clipped box hedge a->b (a block with its sides and top)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    L = (b - a).length
    if L < 1e-6: return
    e = (b - a) / L; nc = V(e.y, -e.x)
    kutu3(y, a.lerp(b, 0.5) + Z * (z + h / 2), e, nc, Z, L, t, h, key, ('+x', '-x', '+y', '-y', '+z'))


def topiari(y, x, yy, z, h=0.05, key='yesil_koyu', tur='koni'):
    """a clipped topiary: a cone, a ball on a stem or a stack of balls, in a little tub"""
    if tur == 'koni':
        donel(y, (x, yy), [(0.0, z), (h * 0.28, z), (h * 0.3, z + h * 0.12), (0.0, z + h)], key, n=8)
    elif tur == 'top':
        y.prizma((x, yy), 0.003, z, z + h * 0.5, 'ahsap', n=5)
        kure(y, (x, yy, z + h * 0.68), h * 0.3, key, n=8, kat=4)
    else:
        for k, (zz, rr) in enumerate(((0.22, 0.24), (0.58, 0.18), (0.86, 0.12))):
            kure(y, (x, yy, z + h * zz), h * rr, key, n=8, kat=4)


def okcu(y, x, yy, z, aci=0.0, s=1.0, key='boya_yesil', cek=1.0, sapka='kece'):
    """an English longbowman facing aci (local +x): a tunic, a hood or cap, the tall bow held out, drawing (cek)"""
    insan(y, x, yy, z, key, s, aci=aci, sapka=sapka)
    with parca(y, (x, yy, z), aci, s):
        # the bow arm held out and the bow (a tall arc in the local x-z plane)
        boru(y, [V(0.0, 0.006, 0.03), V(0.016, 0.004, 0.031)], 0.0018, 'kum_acik', n=4)
        bx = 0.018
        yay = [V(bx + 0.007 * math.cos(math.pi * (k / 8 - 0.5)), 0.004, 0.031 + 0.034 * math.sin(math.pi * (k / 8 - 0.5))) for k in range(9)]
        boru(y, yay, 0.0012, 'ahsap_acik', n=4, kapat=True)
        # the string drawn back to the cheek, an arrow on it
        tel = bx - 0.012 * cek
        boru(y, [yay[0], V(tel, 0.004, 0.031), yay[-1]], 0.0004, 'beyaz', n=3)
        boru(y, [V(tel, 0.004, 0.031), V(bx + 0.006, 0.004, 0.031)], 0.0006, 'ahsap', n=3)
        boru(y, [V(0.0, -0.005, 0.03), V(tel, 0.0, 0.031)], 0.0017, 'kum_acik', n=4)
        # a quiver at the hip
        boru(y, [V(-0.006, -0.006, 0.01), V(-0.007, -0.006, 0.026)], 0.0028, 'ahsap_koyu', n=5)
