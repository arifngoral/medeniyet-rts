# Reference previews of Süleymaniye (the quality bar) in the same views as every other model:
#   node tools/lm-blender/uret.mjs _suleymaniye_ref   -> .blender-varlik/onizleme/_suleymaniye_ref/
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.argv = [a for a in sys.argv]
import importlib.util
_s = importlib.util.spec_from_file_location('sul', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'suleymaniye.py'))
_m = importlib.util.module_from_spec(_s)
_m.__name__ = 'sul'
_s.loader.exec_module(_m)
from bina_ortak import calistir
calistir(_m.y, '_suleymaniye_ref')
