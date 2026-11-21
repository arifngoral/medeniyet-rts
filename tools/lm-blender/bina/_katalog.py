# A test sheet of every part in parcalar.py (not a game model): node tools/lm-blender/uret.mjs _katalog
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import Yapi
from parcalar import *
from bina_ortak import calistir

y = Yapi()
G = 0.75   # grid step


def yer(i, j):
    return (i * G, j * G, 0)


# row 0: columns of every kind and a colonnade + pediment
for k, tur in enumerate(('osmanli', 'dor', 'iyon', 'korint', 'toskan', 'misir', 'pers', 'ahsap')):
    sutun(y, -0.3 + k * 0.09, -0.3, 0, 0.3, 0.018, 'lake' if tur == 'ahsap' else ('kum' if tur in ('misir', 'pers') else 'mermer'), tur,
          bant_key='boya_kirmizi' if tur == 'misir' else None)
with parca(y, yer(1, 0)):
    zemin(y, -0.3, 0.3, -0.2, 0.2, 0.04, 'kirec', basamak=(('on', 0.3),))
    zt = sutunlu_revak(y, V(-0.25, -0.15), V(0.25, -0.15), 5, 0.04, 0.22, 'dor', key='kirec', triglif='tas_koyu')
    alinlik(y, V(-0.27, -0.17), V(0.27, -0.17), zt, 0.08, 0.3, 'kirec', cati_key='kiremit')
with parca(y, yer(2, 0)):
    peristil(y, -0.25, 0.25, -0.18, 0.18, 6, 4, 0, 0.2, 'iyon', key='mermer', triglif=None)
with parca(y, yer(3, 0)):
    arkad(y, V(-0.25, 0), V(0.25, 0), 4, 0, 0.2)
    kemer_dizisi(y, V(-0.25, 0.2), V(0.25, 0.2), 4, 0, 0.18, 0.05, sivri=0)

# row 1: domes, minaret, portal, fountain
with parca(y, yer(0, 1)):
    duvarlar(y, dikdortgen(-0.2, 0.2, -0.2, 0.2), 0, 0.15, 'tas', ust='tas_acik')
    kubbe_kasnakli(y, (0, 0), 0.16, 0.15, 0.07, 16)
    yarim_kubbe(y, (0, -0.2), 0.12, 0.15, -math.pi / 2, 0.05)
with parca(y, yer(1, 1)):
    minare(y, 0, 0, 0, 0.7, 2, kaide=0.12)
    sadirvan(y, 0.2, 0, 0)
with parca(y, yer(2, 1)):
    tackapi(y, 0, 0, 0)
    sogan_kubbe(y, (0.22, 0), 0.07, 0.2, dilim=['boya_kirmizi', 'boya_yesil', 'altin'])
    y.prizma((0.22, 0), 0.05, 0, 0.2, 'siva', n=16)
with parca(y, yer(3, 1)):
    kucuk_kubbe(y, 0, 0, 0, 0.08)
    agac(y, 0.15, 0.1, boy=0.15, tur='servi'); agac(y, 0.2, -0.1, boy=0.15, tur='palmiye'); agac(y, -0.15, 0.15, boy=0.15)

# row 2: fortification
with parca(y, yer(0, 2)):
    sur(y, [V(-0.3, -0.1), V(0.3, -0.1)], 0, 0.15, 0.05, 'granit')
    kule_yuvarlak(y, (-0.3, 0.05), 0.07, 0, 0.25, 'granit', 'konik', 'arduvaz')
    kule_kare(y, (0.3), 0.05, 0.12, 0, 0.25, 'granit', 'piramit', 'kiremit')
with parca(y, yer(1, 2)):
    kale_kapisi(y, 0, 0, 0.2, 0, 0.16, kule='yuvarlak', cati='konik', cati_key='kiremit')
with parca(y, yer(2, 2)):
    kule_yuvarlak(y, (0, 0), 0.09, 0, 0.3, 'tas', 'duz')
    kule_kare(y, 0.22, 0.1, 0.1, 0, 0.2, 'tugla', 'duz', kose_tas='tas_acik')
with parca(y, yer(3, 2)):
    duvarlar(y, dikdortgen(-0.2, 0.2, -0.12, 0.12), 0, 0.12, 'siva_krem')
    cati_besik(y, -0.2, 0.2, -0.12, 0.12, 0.12, 0.1, 0.03, 'kiremit', ucluk_key='siva_krem')

# row 3: roofs
with parca(y, yer(0, 3)):
    duvarlar(y, dikdortgen(-0.2, 0.2, -0.14, 0.14), 0, 0.1, 'siva')
    cati_kirma(y, -0.2, 0.2, -0.14, 0.14, 0.1, 0.12, 0.06, 'kiremit_koyu', 'kiremit_koyu2', kivrim=0.5, yukari=0.04)
with parca(y, yer(1, 3)):
    duvarlar(y, dikdortgen(-0.2, 0.2, -0.14, 0.14), 0, 0.1, 'siva')
    cati_irimoya(y, -0.2, 0.2, -0.14, 0.14, 0.1, 0.13, 0.06, sus='kiremit_koyu2')
with parca(y, yer(2, 3)):
    z = 0
    w = 0.3
    for k in range(3):
        tepe, z = pagoda_kati(y, (0, 0), w, z, 0.09, 0.07, 0.05, korkuluk=(k > 0), balkon=0.02 if k else 0)
        w *= 0.78
    sorin(y, 0, 0, tepe - 0.005, 0.12)
with parca(y, yer(3, 3)):
    duvarlar(y, dikdortgen(-0.15, 0.15, -0.15, 0.15), 0, 0.12, 'tugla')
    cati_kirma(y, -0.15, 0.15, -0.15, 0.15, 0.12, 0.15, 0.03, 'bakir', 'bakir2')

# row 4: pyramids, obelisk, stepped temple
with parca(y, yer(0, 4)):
    piramit(y, (0, 0), 0.5, 0.32)
with parca(y, yer(1, 4)):
    zt, hw, hd = basamakli_piramit(y, (0, 0), 0.55, 0.2, 4, 0.3, 'kirec', tablero_key='boya_kirmizi', alfarda_key='kirec')
    duvarlar(y, dikdortgen(-0.07, 0.07, -0.06, 0.06), zt, zt + 0.08, 'boya_kirmizi', ust='saz')
with parca(y, yer(2, 4)):
    dikilitas(y, (0, 0), 0.05, 0.4, yazi_key='koyu')
with parca(y, yer(3, 4)):
    kerpic_duvar(y, dikdortgen(-0.25, 0.25, -0.15, 0.15), 0, 0.12)
    kerpic_kule(y, (0, 0.05), 0.12, 0, 0.3)

# row 5: timber, tents, banner
with parca(y, yer(0, 5)):
    kutuk_ev(y, -0.15, 0.15, -0.1, 0.1, 0, 0.1)
with parca(y, yer(1, 5)):
    uzun_ev(y, 0, 0, 0.5, 0.2, 0.07, 0.14)
with parca(y, yer(2, 5)):
    cadir_otag(y, (0, 0), 0.15, 0.09, 0.08)
    cadir(y, (0.22, 0.1), 0.06, 0.12)
with parca(y, yer(3, 5)):
    duvarlar(y, dikdortgen(-0.15, 0.15, -0.1, 0.1), 0, 0.15, 'siva_krem')
    kirma_dikme(y, V(-0.15, -0.1), V(0.15, -0.1), 0, 0.15)
    sancak(y, 0.1, 0, 0.15, kuyruk=True)
    merdiven(y, (-0.25, -0.1), math.pi / 2, 0.06, 0, 0.1, 6, yanlik='tas')
    havuz(y, -0.3, -0.18, 0.15, 0.3, 0.01)

calistir(y, '_katalog')
