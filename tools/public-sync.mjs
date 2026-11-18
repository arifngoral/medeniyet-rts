// Aevum - keeps the public (open source) repository in step with this private one.
// The private repo deploys the game and holds files that may not be published (tools/public-exclude.txt).
// The public repo has its own history: each export is one snapshot commit of this repo's HEAD minus those files.
//
//   node tools/public-sync.mjs import [publicDir]   apply what was merged in the public repo since the last sync
//   node tools/public-sync.mjs export [publicDir]   copy HEAD (minus excluded files) into the public repo and commit
//
// publicDir defaults to ../aevum-public (a clone of the public repo). Export refuses while the public repo has
// changes that were not imported yet, so nothing merged there is ever overwritten. Push the public repo yourself.
// The last synced public commit is kept in .public-sync (private only).
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const STATE = path.join(ROOT, '.public-sync');
const [cmd, dirArg] = process.argv.slice(2);
const PUB = path.resolve(dirArg || path.join(ROOT, '..', 'aevum-public'));

const git = (cwd, args, opts = {}) => execFileSync('git', ['-c', 'safe.directory=*', ...args], { cwd, encoding: opts.buffer ? 'buffer' : 'utf8', maxBuffer: 1 << 30, input: opts.input, stdio: opts.input != null ? ['pipe', 'pipe', 'inherit'] : ['ignore', 'pipe', 'inherit'] });
const out = (cwd, args) => git(cwd, args).trim();
const die = (m) => { console.error(m); process.exit(1); };
const lastSync = () => (fs.existsSync(STATE) ? fs.readFileSync(STATE, 'utf8').trim() : '');
const excluded = () => fs.readFileSync(path.join(ROOT, 'tools', 'public-exclude.txt'), 'utf8').split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith('#'));

if (!fs.existsSync(path.join(PUB, '.git'))) die('Public repo clone not found: ' + PUB);
const pubBranch = out(PUB, ['symbolic-ref', '--short', 'HEAD']);   // (works on an empty clone too)
try { git(PUB, ['fetch', '-q', 'origin']); } catch { console.warn('(fetch failed: using the local public branch)'); }
const remoteRef = (() => { try { return out(PUB, ['rev-parse', '--verify', '-q', 'origin/' + pubBranch]); } catch { return ''; } })();
const pubHead = remoteRef || (() => { try { return out(PUB, ['rev-parse', '--verify', '-q', 'HEAD']); } catch { return ''; } })();

if (cmd === 'import') {
  const last = lastSync();
  if (!last) die('No previous sync recorded (.public-sync): run export first.');
  if (!pubHead || pubHead === last) { console.log('Nothing new in the public repo.'); process.exit(0); }
  const patch = git(PUB, ['diff', '--binary', last, pubHead], { buffer: true });
  if (patch.length) git(ROOT, ['apply', '--3way', '--whitespace=nowarn'], { input: patch });
  fs.writeFileSync(STATE, pubHead + '\n');
  console.log(`Imported public ${last.slice(0, 7)}..${pubHead.slice(0, 7)}. Review, run the tests, then commit (with .public-sync).`);
} else if (cmd === 'export') {
  if (out(ROOT, ['status', '--porcelain', '--untracked-files=no'])) die('Commit or stash your changes first.');
  const last = lastSync();
  if (last && pubHead && pubHead !== last) die(`The public repo has commits not imported yet (${last.slice(0, 7)} -> ${pubHead.slice(0, 7)}): run import first.`);
  if (out(PUB, ['status', '--porcelain'])) die('The public clone has local changes: clean it first.');
  if (remoteRef) git(PUB, ['reset', '-q', '--hard', remoteRef]);
  // replace the public tree with this repo's HEAD
  for (const f of out(PUB, ['ls-files', '-z']).split('\0').filter(Boolean)) fs.rmSync(path.join(PUB, f), { force: true });
  // (tar reads the archive from stdin inside the public dir: drive-letter paths confuse GNU tar on Windows)
  execFileSync('tar', ['-xf', '-'], { cwd: PUB, input: git(ROOT, ['archive', '--format=tar', 'HEAD'], { buffer: true }), maxBuffer: 1 << 30, stdio: ['pipe', 'inherit', 'inherit'] });
  for (const f of [...excluded(), '.public-sync']) fs.rmSync(path.join(PUB, f), { force: true });
  git(PUB, ['add', '-A']);
  if (!out(PUB, ['status', '--porcelain'])) { console.log('Public repo already matches HEAD.'); }
  else {
    const head = out(ROOT, ['rev-parse', '--short', 'HEAD']);
    const subj = out(ROOT, ['log', '-1', '--format=%s']);
    // same author identity as the private repo (its GitHub noreply address), never the machine's default
    const who = (k) => { try { return out(ROOT, ['config', k]); } catch { return ''; } };
    const id = who('user.email') ? ['-c', 'user.name=' + who('user.name'), '-c', 'user.email=' + who('user.email')] : [];
    git(PUB, [...id, 'commit', '-q', '-m', `${subj}\n\nSnapshot of the private repo at ${head}.`]);
    console.log('Committed in ' + PUB + '. Push it with: git -C "' + PUB + '" push');
  }
  fs.writeFileSync(STATE, out(PUB, ['rev-parse', 'HEAD']) + '\n');
  console.log('Recorded the sync in .public-sync: commit it.');
} else {
  die('usage: node tools/public-sync.mjs import|export [publicDir]');
}
