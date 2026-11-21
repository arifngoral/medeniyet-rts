# Shared actions of a foot soldier (degrees about the armature's axes, karakter.poz): bekle (idle), yuru (walk),
# saldir (attack), ol (death). The skeleton's bone names: karakter / insan units (kalca, bel, gogus, kafa, kol_ust_sol ...).

TABAN = {'kol_ust_sag': [('x', -8)], 'kol_alt_sag': [('x', -22)], 'kol_ust_sol': [('x', -6)], 'kol_alt_sol': [('x', -38)]}


def P2(*ds):
    out = {}
    for dd in ds:
        for kk, v in dd.items(): out.setdefault(kk, []).extend(v)
    return out


def bekle():
    a = P2(TABAN)
    b = P2(TABAN, {'bel': [('x', 1.5)], 'gogus': [('x', 2)], 'kafa': [('z', 5), ('x', -2)], 'kol_ust_sag': [('x', -3)], 'kol_ust_sol': [('x', 3)]})
    return [(1, a, None), (25, b, None), (49, a, None)]


def yuru():
    def kare(onde):
        arka = 'sag' if onde == 'sol' else 'sol'; sg = 1 if onde == 'sol' else -1
        return P2(TABAN, {'uyluk_' + onde: [('x', -28)], 'baldir_' + onde: [('x', 6)], 'ayak_' + onde: [('x', -8)],
                          'uyluk_' + arka: [('x', 22)], 'baldir_' + arka: [('x', 14)], 'ayak_' + arka: [('x', 12)],
                          'kol_ust_' + onde: [('x', 16)], 'kol_ust_' + arka: [('x', -16)],
                          'gogus': [('z', -6 * sg)], 'kalca': [('z', 5 * sg)], 'etek_on': [('x', -18)], 'etek_arka': [('x', 12)]})
    def gecis(salinan):
        duran = 'sag' if salinan == 'sol' else 'sol'
        return P2(TABAN, {'uyluk_' + salinan: [('x', -8)], 'baldir_' + salinan: [('x', 55)], 'ayak_' + salinan: [('x', 10)],
                          'uyluk_' + duran: [('x', 2)], 'bel': [('x', 3)], 'etek_on': [('x', -8)], 'etek_arka': [('x', 4)]})
    return [(1, kare('sol'), None), (7, gecis('sag'), (0, 0, 0.035)), (13, kare('sag'), None), (19, gecis('sol'), (0, 0, 0.035)), (25, kare('sol'), None)]


def saldir():
    hazir = P2(TABAN)
    kaldir = P2({'kol_ust_sag': [('x', -150), ('y', 15)], 'kol_alt_sag': [('x', -55)], 'gogus': [('z', -22)], 'bel': [('x', -8)],
                 'kol_ust_sol': [('x', -35)], 'kol_alt_sol': [('x', -40)], 'uyluk_sol': [('x', -12)], 'uyluk_sag': [('x', 10)]})
    vur = P2({'kol_ust_sag': [('x', -40)], 'kol_alt_sag': [('x', -8)], 'gogus': [('z', 22)], 'bel': [('x', 16)],
              'kol_ust_sol': [('x', -20), ('z', 10)], 'kol_alt_sol': [('x', -45)], 'uyluk_sag': [('x', -22)], 'baldir_sag': [('x', 18)],
              'etek_on': [('x', -16)], 'uyluk_sol': [('x', 14)], 'kafa': [('x', 8)]})
    return [(1, hazir, None), (9, kaldir, None), (12, P2(kaldir, {'kol_ust_sag': [('x', -8)]}), None), (15, vur, (0, -0.04, -0.02)),
            (19, vur, (0, -0.04, -0.02)), (27, hazir, None)]


def ol():
    sars = P2(TABAN, {'bel': [('x', -16)], 'gogus': [('x', -8)], 'kafa': [('x', -22)], 'kol_ust_sag': [('x', -40)], 'kol_ust_sol': [('x', -30)]})
    cok = P2(TABAN, {'uyluk_sol': [('x', -55)], 'uyluk_sag': [('x', -45)], 'baldir_sol': [('x', 85)], 'baldir_sag': [('x', 75)],
                     'bel': [('x', 18)], 'kafa': [('x', 15)], 'kol_ust_sag': [('x', 10)], 'kol_ust_sol': [('x', 10)], 'etek_on': [('x', -48)]})
    yat = P2({'kok': [('x', -84)], 'etek_on': [('x', -15)], 'uyluk_sol': [('x', -25)], 'uyluk_sag': [('x', -10)], 'baldir_sol': [('x', 35)],
              'baldir_sag': [('x', 15)], 'kafa': [('x', -15), ('z', 20)], 'kol_ust_sag': [('x', -70)], 'kol_ust_sol': [('x', -60)], 'kol_alt_sol': [('x', -20)]})
    return [(1, P2(TABAN), None), (7, sars, (0, 0.03, 0)), (17, cok, (0, 0.02, -0.26)), (30, yat, (0, 0.05, 0.08)),
            (34, P2(yat, {'kafa': [('x', 5)]}), (0, 0.05, 0.06)), (42, yat, (0, 0.05, 0.06))]


ANIM = [('bekle', bekle()), ('yuru', yuru()), ('saldir', saldir()), ('ol', ol())]
