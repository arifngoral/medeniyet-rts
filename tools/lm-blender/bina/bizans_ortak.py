# Shared helpers for the Byzantine landmarks lm_bukoleon, lm_hipodrom, lm_theodosius, lm_darphane (not a building:
# imported by those scripts). Byzantine details on top of parcalar.py: banded (stone + brick) walls with round-arched
# windows and striped voussoirs, horses (bronze quadriga, racing teams), people, a dromon (war galley with lateen
# sails and the Greek-fire siphon), statues on columns.
import math, random
from mathutils import Vector
from parcalar import *

BIZ_PENCERE = ('kirec', 'tas_koyu', 'mermer', 'cam')
BIZ_CER = (0.008, ['tugla_roma', 'kirec'])            # alternating brick / stone voussoirs


def serit_tas(y, p, q, z0, u0, u1, zb, hb, key='tugla_roma', d=0.003):
    """a raised course on the wall p->q (faces its right) from u0..u1 (distance along) and zb..zb+hb above z0 (a
    closed little box, d proud of the wall)"""
    if u1 - u0 < 0.004: return
    p, q = V(p[0], p[1]), V(q[0], q[1])
    W = (q - p).length; e = (q - p) / W; nc = V(e.y, -e.x)
    A = p + e * u0 + Z * (z0 + zb); B = p + e * u1 + Z * (z0 + zb)
    up = Z * hb; o = nc * d
    y.yuz_yon([A + o, B + o, B + o + up, A + o + up], key, nc)
    y.yuz_yon([A + up, B + up, B + o + up, A + o + up], key, Z)
    y.yuz_yon([A, B, B + o, A + o], key, -Z)
    y.yuz_yon([A, A + o, A + o + up, A + up], key, -e)
    y.yuz_yon([B, B + o, B + o + up, B + up], key, e)


def bantlar(H, adim=0.075, h=0.02, bas=0.035):
    """brick band heights (zb, hb) up a wall H high: a band every adim"""
    out = []
    zb = bas
    while zb + h < H - 0.012:
        out.append((zb, h)); zb += adim
    return out


def almasik(y, a, b, z0, H, n, en=0.4, v0=0.04, ust=0.03, sivri=0.0, kapi_bay=None, duvar='kirec', bant='tugla_roma',
            bant_list=None, pencere='cam', cer=BIZ_CER, derin=0.025, k_say=6, kapi_key='ahsap', kapi_en=0.6, bos=()):
    """a Byzantine banded wall a->b (faces its right): n bays with round-arched windows (sivri > 0: pointed) and
    brick bands between them; n = 0: a plain banded wall. kapi_bay: the bay holding a door; bos: bays left plain
    (no window)"""
    a, b = V(a[0], a[1]), V(b[0], b[1])
    bl = bant_list if bant_list is not None else bantlar(H)
    if n == 0:
        duz_duvar(y, a, b, z0, z0 + H, duvar)
        L = (b - a).length
        for zb, hb in bl:
            serit_tas(y, a, b, z0, 0, L, zb, hb, bant)
        return
    for k in range(n):
        p, q = a.lerp(b, k / n), a.lerp(b, (k + 1) / n)
        W = (q - p).length
        kapi_mi = (k == kapi_bay)
        if k in bos:
            duz_duvar(y, p, q, z0, z0 + H, duvar)
            for zb, hb in bl:
                serit_tas(y, p, q, z0, 0, W, zb, hb, bant)
            continue
        ee, vv = (kapi_en, 0.0) if kapi_mi else (en, v0)
        uu = max(0.01, H * 0.08) if kapi_mi else ust
        if kapi_mi:
            y.kemerli(p, q, z0, H, (duvar, 'tas_koyu', 'mermer', kapi_key), v0=0.0, en=ee, ust=uu, derin=derin + 0.005, k_say=k_say, sivri=sivri,
                      cerceve=(cer[0] * 1.3, cer[1]) if cer else None)
        else:
            y.kemerli(p, q, z0, H, (duvar, 'tas_koyu', 'mermer', pencere), v0=vv, en=ee, ust=uu, derin=derin, k_say=k_say, sivri=sivri,
                      cerceve=cer)
        x0, x1 = (1 - ee) / 2 * W, (1 + ee) / 2 * W
        m = (cer[0] if cer else 0) + 0.004
        tepe = H - uu
        for zb, hb in bl:
            hb = min(hb, H - 0.004 - zb)
            if hb <= 0: continue
            if zb + hb <= vv - 0.014 or zb >= tepe + m:
                serit_tas(y, p, q, z0, 0, W, zb, hb, bant)
            else:
                serit_tas(y, p, q, z0, 0, x0 - m, zb, hb, bant)
                serit_tas(y, p, q, z0, x1 + m, W, zb, hb, bant)


def almasik_kutu(y, x0, x1, y0, y1, z0, H, sayilar, ust='kursun', kapilar=(None, None, None, None), **kw):
    """four banded walls round a rectangle (sides: front -y, right +x, back +y, left -x), a flat top, a cornice;
    returns the top z"""
    k = dikdortgen(x0, x1, y0, y1)
    for i in range(4):
        almasik(y, k[i], k[(i + 1) % 4], z0, H, sayilar[i], kapi_bay=kapilar[i], **kw)
    zt = z0 + H
    silme(y, k, zt - 0.014, 0.018, 0.012, 'kirec', 'tac')
    if ust:
        y.yuz_yon([V(p.x, p.y, zt + 0.004) for p in k], ust, Z)
    return zt + 0.004


def kiremit_cati(y, x0, x1, y0, y1, z, h, sacak=0.025, kirma=False):
    """a Byzantine red-tile roof: gable (ridge along the longer side) or hipped"""
    if kirma:
        return cati_kirma(y, x0, x1, y0, y1, z, h, sacak, 'kiremit', 'kiremit2', alt_key='ahsap_koyu', kalinlik=0.01)
    return cati_besik(y, x0, x1, y0, y1, z, h, sacak, 'kiremit', 'kiremit2', kalinlik=0.01, ucluk_key='kirec', alinlik_key='mermer')


def biz_kubbe(y, c, r, z, kasnak_h=0.05, n_pencere=12, kubbe_h=None, key='kursun', alem_=True, duvar=('tugla_roma', 'tas_koyu', 'mermer', 'cam')):
    """a Byzantine dome: a brick drum with round-arched windows between pilasters, the lead dome, a cross on top.
    Returns the top z"""
    t = kubbe_kasnakli(y, c, r, z, kasnak_h, n_pencere, kubbe_h=kubbe_h or r * 0.78, key=key, duvar=duvar, alem_olcek=0,
                       sivri=0.0, n=36, kat=10, en=0.5, cerceve=(0.004, 'kirec'))
    if alem_:
        hac(y, c[0], c[1], t, 0.05)
    return t


def hac(y, cx, cy, z, h=0.05, key='altin'):
    """a gilded cross on a small knob"""
    kure(y, (cx, cy, z + h * 0.12), h * 0.14, key, n=8, kat=4)
    y.prizma((cx, cy), h * 0.05, z + h * 0.2, z + h, key, n=4, kat=math.pi / 4)
    cubuk(y, V(cx - h * 0.3, cy, z + h * 0.72), V(cx + h * 0.3, cy, z + h * 0.72), h * 0.08, key)
    return z + h


# ---------------------------------------------------------------- horses, people, statues
def at(y, x, yy, z, aci=0.0, s=1.0, key='bronz', poz='dur', yele=None, faz=0.0):
    """a horse facing angle aci, hooves at z, ~0.075 s long and 0.07 s high at the head. poz: 'dur' (standing, one
    foreleg raised: the bronze quadriga), 'kos' (gallop, faz 0..1 shifts the stride), 'sah' (rearing)"""
    yk = yele or key
    with parca(y, (x, yy, z), aci, s):
        gz = 0.042   # back of the body
        if poz == 'sah':
            boru(y, [V(-0.026, 0, 0.034), V(0.0, 0, 0.05), V(0.022, 0, 0.068)], 0.0115, key, n=7)
            kure(y, (0.022, 0, 0.068), 0.012, key, n=7, kat=3)
            kure(y, (-0.026, 0, 0.034), 0.0125, key, n=7, kat=3)
            boyun = [V(0.024, 0, 0.074), V(0.032, 0, 0.096)]
            bas = [V(0.03, 0, 0.098), V(0.046, 0, 0.09)]
            on_ = [((0.02, 0.006, 0.06), (0.04, 0.006, 0.058), (0.042, 0.006, 0.044)), ((0.02, -0.006, 0.06), (0.036, -0.006, 0.066), (0.044, -0.006, 0.056))]
            ar_ = [((-0.03, 0.007, 0.03), (-0.024, 0.007, 0.014), (-0.03, 0.007, 0.0)), ((-0.03, -0.007, 0.03), (-0.02, -0.007, 0.016), (-0.024, -0.007, 0.0))]
            kuyruk = [V(-0.036, 0, 0.036), V(-0.048, 0, 0.022), V(-0.05, 0, 0.008)]
        else:
            boru(y, [V(-0.027, 0, gz), V(0.0, 0, gz + 0.001), V(0.025, 0, gz + 0.003)], 0.0115, key, n=7)
            kure(y, (0.025, 0, gz + 0.002), 0.0125, key, n=7, kat=3)
            kure(y, (-0.027, 0, gz + 0.001), 0.0125, key, n=7, kat=3)
            if poz == 'kos':
                boyun = [V(0.03, 0, gz + 0.008), V(0.046, 0, gz + 0.022)]
                bas = [V(0.045, 0, gz + 0.026), V(0.064, 0, gz + 0.016)]
                f = faz * TAU
                sw = lambda k: math.sin(f + k)
                on_ = []
                for sy, k in ((0.006, 0.0), (-0.006, 0.7)):
                    t = sw(k)
                    on_.append(((0.024, sy, gz - 0.006), (0.034 + 0.012 * t, sy, 0.02 + 0.006 * abs(t)), (0.044 + 0.018 * t, sy, 0.004 + 0.008 * max(0, t))))
                ar_ = []
                for sy, k in ((0.007, 2.6), (-0.007, 3.3)):
                    t = sw(k)
                    ar_.append(((-0.026, sy, gz - 0.006), (-0.034 - 0.01 * t, sy, 0.022), (-0.03 - 0.022 * t, sy, 0.002 + 0.006 * max(0, -t))))
                kuyruk = [V(-0.037, 0, gz + 0.004), V(-0.05, 0, gz + 0.006), V(-0.062, 0, gz + 0.002)]
            else:
                boyun = [V(0.028, 0, gz + 0.008), V(0.04, 0, gz + 0.03)]
                bas = [V(0.038, 0, gz + 0.034), V(0.056, 0, gz + 0.022)]
                on_ = [((0.024, 0.006, gz - 0.006), (0.026, 0.006, 0.02), (0.026, 0.006, 0.0)),
                       ((0.024, -0.006, gz - 0.006), (0.04, -0.006, 0.03), (0.044, -0.006, 0.018))]
                ar_ = [((-0.026, 0.007, gz - 0.006), (-0.03, 0.007, 0.02), (-0.028, 0.007, 0.0)),
                       ((-0.026, -0.007, gz - 0.006), (-0.026, -0.007, 0.02), (-0.03, -0.007, 0.0))]
                kuyruk = [V(-0.037, 0, gz + 0.004), V(-0.044, 0, gz - 0.008), V(-0.043, 0, gz - 0.026)]
        boru(y, boyun, 0.0078, key, n=7, r_son=0.0062)
        boru(y, bas, 0.0062, key, n=7, r_son=0.0042)
        h0 = bas[0]
        for sy in (-1, 1):   # ears
            boru(y, [h0 + V(-0.002, sy * 0.003, 0.003), h0 + V(-0.004, sy * 0.004, 0.011)], 0.0018, key, n=4, r_son=0.0006)
        d = (boyun[1] - boyun[0]).normalized()
        cubuk(y, boyun[0] + V(-0.004, 0, 0.006), boyun[1] + V(-0.005, 0, 0.004), 0.0032, yk, 0.006)   # mane
        for p in on_ + ar_:
            boru(y, [V(*q) for q in p], 0.0036, key, n=4, r_son=0.0026)
            kure(y, (p[-1][0], p[-1][1], p[-1][2] + 0.002), 0.003, key, n=4, kat=2)
        boru(y, kuyruk, 0.003, yk, n=5, r_son=0.0012)


def insan(y, x, yy, z, key='kirmizi', s=1.0, ten='kum_acik', aci=0.0, kol=0.0, sapka=None):
    """a small standing person: a robe (cone-ish), shoulders, a head; kol > 0 raises an arm that much"""
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0075, 0.0), (0.0085, 0.004), (0.0068, 0.024), (0.0058, 0.031), (0.0, 0.033)], key, n=7)
        kure(y, (0, 0, 0.039), 0.0052, ten, n=7, kat=4)
        if sapka:
            y.prizma((0, 0), 0.0055, 0.041, 0.046, sapka, n=7)
        if kol:
            boru(y, [V(0, 0.006, 0.029), V(0.004, 0.009, 0.029 + 0.016 * kol)], 0.0018, ten, n=4)


def oturan(y, x, yy, z, key, aci=0.0, s=1.0, ten='kum_acik'):
    """a seated spectator (a lump with a head), facing angle aci"""
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.0072, 0.0), (0.0068, 0.012), (0.0, 0.019)], key, n=5)
        kure(y, (0.001, 0, 0.0235), 0.0048, ten, n=5, kat=2)


def heykel(y, x, yy, z, s=1.0, key='mermer', aci=0.0, kol=0.7):
    """a draped standing statue (emperor, saint) with one arm raised"""
    with parca(y, (x, yy, z), aci, s):
        donel(y, (0, 0), [(0.012, 0.0), (0.014, 0.018), (0.0095, 0.05), (0.011, 0.06), (0.007, 0.068), (0.0, 0.07)], key, n=10)
        kure(y, (0, 0, 0.078), 0.0072, key, n=8, kat=4)
        if kol:
            boru(y, [V(0.004, 0.008, 0.058), V(0.012, 0.012, 0.058 + 0.03 * kol)], 0.0026, key, n=5)
            kure(y, (0.013, 0.012, 0.058 + 0.032 * kol), 0.0035, key, n=6, kat=3)


def sutun_heykel(y, x, yy, z, h=0.2, s=1.0, key='mermer', heykel_key='bronz', aci=0.0):
    """an honorific column: a stepped base, a plain shaft, a capital and a statue"""
    kutu_merkez(y, (x, yy), 0.05 * s, 0.05 * s, 0.02 * s, key, z0=z)
    kutu_merkez(y, (x, yy), 0.038 * s, 0.038 * s, 0.03 * s, key, z0=z + 0.02 * s)
    kornis(y, x - 0.019 * s, x + 0.019 * s, yy - 0.019 * s, yy + 0.019 * s, z + 0.044 * s, 0.006 * s, 0.004 * s, key, 'tac')
    t = sutun(y, x, yy, z + 0.05 * s, z + h, 0.011 * s, key, 'korint', yiv=12)
    heykel(y, x, yy, t, 0.8 * s, heykel_key, aci)
    return t + 0.08 * s


# ---------------------------------------------------------------- the dromon
def dromon(y, cx, cy, ZS, aci, L=0.42, B=0.06, H=0.034, tohum=1, yelken=True, kurek=True, sifon=True):
    """a Byzantine dromon on the water (surface ZS) heading towards aci: a long low hull (dark wood, a red wale),
    a spur at the bow over the bronze Greek-fire siphon, a forecastle, a stern cabin under an awning, two banks of
    oars, two masts with lateen sails (red bands), stern rudders"""
    g = random.Random(tohum)
    with parca(y, (cx, cy, 0), aci):
        n = 14
        st = []
        for i in range(n + 1):
            t = i / n
            x = -L / 2 + L * t
            w = B / 2 * max(0.14, math.sin(math.pi * min(1, max(0, (t - 0.01) / 0.98))) ** 0.5)
            h = H + 0.014 * ((0.2 - t) / 0.2) ** 2 * (t < 0.2) + 0.016 * ((t - 0.82) / 0.18) ** 2 * (t > 0.82)
            st.append((x, w, h))
        kz = ZS - 0.01
        for i in range(n):
            (x0, w0, h0), (x1, w1, h1) = st[i], st[i + 1]
            for s in (-1, 1):
                pk0, pk1 = V(x0, 0, kz), V(x1, 0, kz)
                m0, m1 = V(x0, s * w0, ZS + h0 * 0.4), V(x1, s * w1, ZS + h1 * 0.4)
                r0, r1 = V(x0, s * w0 * 1.03, ZS + h0 * 0.6), V(x1, s * w1 * 1.03, ZS + h1 * 0.6)
                g0, g1 = V(x0, s * w0, ZS + h0), V(x1, s * w1, ZS + h1)
                for (a0, a1, b1, b0), key in (((pk0, pk1, m1, m0), 'ahsap_koyu'), ((m0, m1, r1, r0), 'boya_kirmizi'), ((r0, r1, g1, g0), 'ahsap')):
                    y.yuz_yon([a0, a1, b1, b0], key, V(0, s, 0.2))
            y.yuz_yon([V(x0, -w0, ZS + h0 * 0.9), V(x1, -w1, ZS + h1 * 0.9), V(x1, w1, ZS + h1 * 0.9), V(x0, w0, ZS + h0 * 0.9)], 'ahsap_acik', Z)
            for s in (-1, 1):
                y.yuz_yon([V(x0, s * w0, ZS + h0 * 0.9), V(x1, s * w1, ZS + h1 * 0.9), V(x1, s * w1, ZS + h1), V(x0, s * w0, ZS + h0)], 'ahsap', V(0, -s, 0))
                y.yuz_yon([V(x0, s * w0, ZS + h0), V(x1, s * w1, ZS + h1), V(x1, s * w1 * 0.95, ZS + h1 + 0.0001), V(x0, s * w0 * 0.95, ZS + h0 + 0.0001)],
                          'ahsap', Z)
        for i, sg in ((0, -1), (n, 1)):
            x, w, h = st[i]
            y.yuz_yon([V(x, -w, ZS + h), V(x, -w * 1.03, ZS + h * 0.6), V(x, -w, ZS + h * 0.4), V(x, 0, kz), V(x, w, ZS + h * 0.4),
                       V(x, w * 1.03, ZS + h * 0.6), V(x, w, ZS + h)], 'ahsap_koyu', V(sg, 0, 0))
        xb, wb, hb = st[-1]
        x0s, w0s, h0s = st[0]
        # the spur (above the water) and the siphon under a small platform
        boru(y, [V(xb - 0.01, 0, ZS + hb * 0.55), V(xb + 0.05, 0, ZS + hb * 0.62)], 0.005, 'ahsap_koyu', n=6, r_son=0.002)
        if sifon:
            boru(y, [V(xb - 0.03, 0, ZS + hb + 0.008), V(xb + 0.012, 0, ZS + hb + 0.004)], 0.0035, 'bronz', n=6, r_son=0.0045)
            kure(y, (xb - 0.03, 0, ZS + hb + 0.009), 0.006, 'bronz', n=6, kat=4)
        # forecastle (a small timber tower) and the stern cabin with an awning
        kutu_merkez(y, (xb - 0.07, 0), 0.04, B * 0.62, 0.026, 'ahsap', z0=ZS + H * 0.9)
        for sx in (-1, 1):
            for sy in (-1, 1):
                y.prizma((xb - 0.07 + sx * 0.017, sy * B * 0.28), 0.0022, ZS + H * 0.9 + 0.026, ZS + H * 0.9 + 0.038, 'ahsap_koyu', n=4, ust=True)
        cubuk(y, V(xb - 0.09, -B * 0.31, ZS + H * 0.9 + 0.038), V(xb - 0.05, -B * 0.31, ZS + H * 0.9 + 0.038), 0.003, 'ahsap_koyu')
        cubuk(y, V(xb - 0.09, B * 0.31, ZS + H * 0.9 + 0.038), V(xb - 0.05, B * 0.31, ZS + H * 0.9 + 0.038), 0.003, 'ahsap_koyu')
        kutu_merkez(y, (x0s + 0.06, 0), 0.05, B * 0.6, 0.022, 'ahsap_acik', z0=ZS + H * 0.9)
        zc = ZS + H * 0.9 + 0.022
        cz = zc + 0.016
        for sy in (-1, 1):   # awning (red), two-sided
            iki_yuzlu(y, [V(x0s + 0.035, sy * B * 0.34, zc + 0.004), V(x0s + 0.085, sy * B * 0.34, zc + 0.004), V(x0s + 0.085, 0, cz), V(x0s + 0.035, 0, cz)],
                      'boya_kirmizi', V(0, sy * 0.6, 1))
        for sx in (0.035, 0.085):
            for sy in (-1, 1):
                y.prizma((x0s + sx, sy * B * 0.34), 0.0018, zc, zc + 0.005, 'ahsap_koyu', n=4, ust=True)
        # stern post curling, the two steering oars
        boru(y, [V(x0s, 0, ZS + h0s - 0.004), V(x0s - 0.014, 0, ZS + h0s + 0.016), V(x0s - 0.006, 0, ZS + h0s + 0.034), V(x0s + 0.008, 0, ZS + h0s + 0.036)],
             0.004, 'ahsap_koyu', n=6, r_son=0.002)
        for s in (-1, 1):
            cubuk(y, V(x0s + 0.04, s * (w0s + 0.012), ZS + h0s * 0.8), V(x0s - 0.004, s * (w0s + 0.022), ZS - 0.004), 0.004, 'ahsap_acik')
            # shields along the bulwark
            for k in range(7):
                xx = -L * 0.28 + L * 0.5 * k / 6
                ww = B / 2 * math.sin(math.pi * (xx + L / 2) / L) ** 0.5 * 1.02
                c = V(xx, s * (ww + 0.0015), ZS + H * 0.86)
                iki_yuzlu(y, [c + V(0.007 * math.cos(TAU * j / 8), 0, 0.007 * math.sin(TAU * j / 8)) for j in range(8)],
                          ('boya_kirmizi', 'boya_sari', 'beyaz')[k % 3], V(0, s, 0))
        if kurek:
            m = 12
            for k in range(m):
                x = -L * 0.3 + L * 0.58 * k / (m - 1)
                for s in (-1, 1):
                    for row, dz in enumerate((0.0, 0.01)):
                        ww = B / 2 * 1.03
                        a = V(x, s * ww, ZS + H * 0.48 + dz)
                        b = V(x - 0.01 - 0.004 * row, s * (ww + 0.07 + 0.012 * row), ZS - 0.002)
                        cubuk(y, a, b, 0.0022, 'ahsap_acik')
        if yelken:
            for xm, mh, sw in ((L * 0.16, 0.22, 0.2), (-L * 0.12, 0.17, 0.15)):
                y.prizma((xm, 0), 0.0035, ZS + H * 0.9, ZS + H + mh, 'ahsap', n=6)
                # the lateen yard: slanting fore-and-aft, its forward end low
                top = V(xm - sw * 0.42, 0, ZS + H + mh + 0.02)
                low = V(xm + sw * 0.58, 0, ZS + H + mh * 0.32)
                cubuk(y, low, top, 0.0035, 'ahsap')
                # the triangular sail between the yard and the clew (aft, low), in bands, bellied to +y
                clew = V(xm - sw * 0.2, 0, ZS + H + mh * 0.16)
                P = lambda t, s_: low.lerp(top, t).lerp(clew, s_) + V(0, 0.01 * math.sin(math.pi * s_) * math.sin(math.pi * t) + 0.003, 0)
                N = 4
                for k in range(N):
                    s0, s1 = k / N, (k + 1) / N
                    key = 'boya_kirmizi' if k == 1 else 'kumas'
                    for j in range(3):
                        t0, t1 = j / 3, (j + 1) / 3
                        quad = [P(t0, s0), P(t1, s0), P(t1, s1), P(t0, s1)]
                        # each triangle on its own true normal (the bellied quads are not flat: offset along +y the
                        # twin poked through at a slant)
                        for tri in ([quad[0], quad[1], quad[2]],) if k == N - 1 else ([quad[0], quad[1], quad[2]], [quad[0], quad[2], quad[3]]):
                            nn = (tri[1] - tri[0]).cross(tri[2] - tri[0])
                            if nn.y < 0: nn = -nn
                            iki_yuzlu(y, tri, key, nn, kil=0.0025)
