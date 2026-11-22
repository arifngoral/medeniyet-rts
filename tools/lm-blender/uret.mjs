// Builds one landmark from its Blender script and compresses it into the game's folder:
//   node tools/lm-blender/uret.mjs <id> [--onizlemesiz]
// tools/lm-blender/bina/<id>.py -> Blender (background) -> .blender-varlik/ham/<id>.glb + previews in
// .blender-varlik/onizleme/<id>/ (not in git) -> gltf-transform jpeg + meshopt (colour / normal 12 bit) ->
// assets/models/lm/<id>.glb. Prints the triangle count, the size and the file size.
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, statSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const KOK = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const id = process.argv[2];
if (!id) { console.error('kullanım: node tools/lm-blender/uret.mjs <id> [--onizlemesiz]'); process.exit(1); }
const onizle = !process.argv.includes('--onizlemesiz');
const BLENDER = process.env.BLENDER || (process.platform === 'win32'
  ? 'C:/Program Files/Blender Foundation/Blender 5.3/blender.exe'
  : '/Applications/Blender.app/Contents/MacOS/Blender');
const betik = join(KOK, 'tools/lm-blender/bina', id + '.py');
if (!existsSync(betik)) { console.error('betik yok:', betik); process.exit(1); }
const ham = join(KOK, '.blender-varlik/ham'), oniz = join(KOK, '.blender-varlik/onizleme', id);
mkdirSync(ham, { recursive: true });
// (an id starting with _ is a test sheet: it stays out of the game's folder)
const g0 = join(ham, id + '.glb'), g1 = join(ham, id + '_j.glb'), son = id.startsWith('_') ? join(ham, id + '_son.glb') : join(KOK, 'assets/models/lm', id + '.glb');
const t0 = Date.now();
const args = ['-b', '--factory-startup', '--python', betik, '--', g0];
if (onizle) args.push(oniz);
let out;
try {
  out = execFileSync(BLENDER, args, { encoding: 'utf8', maxBuffer: 64 << 20 });
} catch (e) {
  console.error((e.stdout || '').split('\n').filter((l) => /Error|Traceback|File "|line \d|^\s+\S/.test(l)).slice(-30).join('\n'));
  console.error(e.stderr || ''); process.exit(1);
}
const satir = out.split('\n').filter((l) => /^(UCGEN|BOLUNMUS|UYARI|BOYUT|TERS_YUZ|BOLUM )|Error|Traceback/.test(l));
console.log(satir.join('\n'));
if (/Traceback/.test(out)) { console.error(out.split('Traceback').pop().slice(0, 3000)); process.exit(1); }
const gtYol = join(KOK, '.blender-varlik/gt/node_modules/.bin', process.platform === 'win32' ? 'gltf-transform.cmd' : 'gltf-transform');
const gt = (...a) => execFileSync(gtYol, a, { encoding: 'utf8', shell: process.platform === 'win32' });
gt('jpeg', g0, g1, '--quality', '80');
gt('meshopt', g1, son, '--level', 'medium', '--quantize-color', '12', '--quantize-normal', '12');
rmSync(g1, { force: true });
const kb = (statSync(son).size / 1024).toFixed(0);
console.log(`DOSYA ${son} ${kb} KB  (${((Date.now() - t0) / 1000).toFixed(0)} sn)` + (kb > 2100 ? '  UYARI: 2 MB üstü' : ''));
if (onizle) console.log('ONIZLEME', oniz);
