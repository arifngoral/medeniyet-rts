// Aevum - the cloud account flow against the REAL Firebase project (src/cloud/config.js).
// Runs only with AEVUM_LIVE=1 (otherwise it skips): AEVUM_LIVE=1 node test/cloud-live-test.mjs
// Creates throwaway accounts aevum-test-<random>@example.com and ALWAYS deletes them and every document they wrote
// (users/<uid>/..., names/<name>, profiles/<uid>) at the end. Never prints id / refresh tokens.
// The game signs in with Google only, and a Google popup cannot run headless: the test accounts are created with a
// raw REST accounts:signUp (needs the Email/Password provider enabled in the console; skipped otherwise) and then
// enter the game through the same Google hand-off (GoogleSignIn with a stub SDK that returns their refresh token).
import * as P from '../src/profile.js';
import { FIREBASE } from '../src/cloud/config.js';
import { CloudSync, mergeSaveLists, nameKey } from '../src/cloud/sync.js';
import { Auth } from '../src/cloud/auth.js';
import { GoogleSignIn } from '../src/cloud/google.js';
import { firestoreApi, call, IDT } from '../src/cloud/rest.js';
import { Game } from '../src/sim/game.js';

if (process.env.AEVUM_LIVE !== '1') { console.log('cloud-live-test: skipped (set AEVUM_LIVE=1 to run against the real project)'); process.exit(0); }

let failed = 0;
const ok = (c, msg) => { if (c) console.log('  ok   ' + msg); else { failed++; console.log('  FAIL ' + msg); } return !!c; };
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const rnd = () => Math.random().toString(36).slice(2, 10);
const memLS = () => { const m = new Map(); return { getItem: (k) => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), removeItem: (k) => m.delete(k), key: (i) => [...m.keys()][i] ?? null, get length() { return m.size; } }; };
// raw Identity Toolkit (test-account plumbing only; the game itself has no e-mail sign in)
const idt = (method, body) => call(fetch, IDT + 'accounts:' + method + '?key=' + encodeURIComponent(FIREBASE.apiKey), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(Object.assign({ returnSecureToken: true }, body)) });
const creds = new Map();   // email -> {uid, email, refreshToken}
async function signIn(email) { const r = await idt('signInWithPassword', { email, password: PASSWORD }); return { uid: r.localId, email: r.email, refreshToken: r.refreshToken }; }
// the stub Firebase SDK: its popup "signs in" as the account queued in `next`
let next = null;
const stubSdk = async () => ({
  app: { getApps: () => [], initializeApp: (o, name) => ({ o, name }) },
  auth: {
    browserSessionPersistence: {}, browserPopupRedirectResolver: {}, initializeAuth: () => ({ currentUser: null }), getAuth: () => ({}),
    GoogleAuthProvider: class { setCustomParameters() {} },
    signInWithPopup: async (a) => { const c = next; next = null; a.currentUser = { uid: c.uid, email: c.email, displayName: null, refreshToken: c.refreshToken, providerData: [] }; return { user: a.currentUser }; },
    signInWithRedirect: async () => {}, getRedirectResult: async () => null, signOut: async (a) => { a.currentUser = null; },
  },
});
async function gLogin(X, email, opts = {}) { next = creds.get(email) || await signIn(email); return X.cloud.loginGoogle(Object.assign({ allowRedirect: false }, opts)); }
function pc(name) {
  const ls = memLS(), hist = new Map(), saves = new Map();
  if (name) P.createProfile(ls, name);
  const profile = { get: () => P.loadProfile(ls), set: (p) => P.saveProfile(ls, p), create: (n) => P.createProfile(ls, n) };
  const history = { list: async () => [...hist.values()], get: async (id) => hist.get(id) || null, put: async (r) => { for (const x of [r].flat()) hist.set(x.id, x); return true; }, del: async (ids) => { for (const i of ids) hist.delete(i); return true; } };
  const store = { list: async () => [...saves.entries()].map(([key, v]) => ({ key, name: v.name, time: v.time, matchId: v.matchId, mp: v.mp })), get: async (k) => (saves.has(k) ? structuredClone(saves.get(k)) : null), put: async (k, v) => { saves.set(k, structuredClone(v)); return true; }, del: async (k) => { saves.delete(k); return true; } };
  const google = new GoogleSignIn({ config: FIREBASE, loader: stubSdk, ss: memLS() });
  const cloud = new CloudSync({ fetch, apiKey: FIREBASE.apiKey, projectId: FIREBASE.projectId, ls, profile, history, saves: store, google });
  return { ls, hist, saves, profile, cloud };
}
function rec(uid, i) {
  return {
    v: 1, id: 'sp-' + (0xabc000 + i).toString(16).padStart(16, '0'), uid, me: 0, endedAt: Date.now() - i * 60000, mode: 'sp', mapType: 'river', mapSize: 128, difficulty: 'normal',
    gameTime: 100 + i, result: i % 2 ? 'lost' : 'won', myAge: 1, stats: { gathered: { food: 1, wood: 1, stone: 1, gold: 1 }, unitsTrained: 1, unitsLost: 0, kills: 0, buildingsBuilt: 1, buildingsLost: 0, razed: 0, techs: 0 },
    players: [{ name: 'Ben', uid, team: 1, ai: false, difficulty: null, won: !(i % 2) }, { name: 'YZ', uid: null, team: 2, ai: true, difficulty: 'normal', won: !!(i % 2) }],
  };
}

const PASSWORD = 'Aevum-' + rnd();
const created = [];   // {email}
const tag = rnd();
const emailA = `aevum-test-${tag}a@example.com`, emailB = `aevum-test-${tag}b@example.com`;
const nameA = 'Test' + tag.slice(0, 8), nameA2 = 'Tst2' + tag.slice(0, 8);

// delete every document of one account, then the account itself
async function wipe(email) {
  const auth = new Auth({ fetch, apiKey: FIREBASE.apiKey, ls: memLS() });
  try { await auth.adopt(await signIn(email)); } catch (e) { return { email, deleted: 'already gone (' + e.code + ')' }; }
  const fb = auth.user.uid;
  const fs = firestoreApi({ fetch, projectId: FIREBASE.projectId, token: (f) => auth.token(f) });
  const del = [];
  for (const d of await fs.query(`users/${fb}`, { collection: 'matches', structured: {} })) del.push(`users/${fb}/matches/${d.id}`);
  for (const d of await fs.query(`users/${fb}`, { collection: 'saves', structured: {} })) {
    del.push(`users/${fb}/saves/${d.id}`);
    for (const c of await fs.query(`users/${fb}/saves/${d.id}`, { collection: 'chunks', structured: {} })) del.push(`users/${fb}/saves/${d.id}/chunks/${c.id}`);
  }
  for (const d of await fs.query(`users/${fb}`, { collection: 'meta', structured: {} })) del.push(`users/${fb}/meta/${d.id}`);
  for (const d of await fs.query('', { collection: 'names', structured: { where: { fieldFilter: { field: { fieldPath: 'uid' }, op: 'EQUAL', value: { stringValue: fb } } } } })) del.push('names/' + d.id);
  if (await fs.get('profiles/' + fb)) del.push('profiles/' + fb);
  for (let i = 0; i < del.length; i += 400) await fs.commit(del.slice(i, i + 400).map((p) => ({ del: p })));
  // verify: nothing left that this account can see
  const left = (await fs.query(`users/${fb}`, { collection: 'matches', structured: {} })).length + (await fs.query(`users/${fb}`, { collection: 'saves', structured: {} })).length +
    (await fs.query(`users/${fb}`, { collection: 'meta', structured: {} })).length + (await fs.query('', { collection: 'names', structured: { where: { fieldFilter: { field: { fieldPath: 'uid' }, op: 'EQUAL', value: { stringValue: fb } } } } })).length + ((await fs.get('profiles/' + fb)) ? 1 : 0);
  await auth.deleteAccount();
  let gone = false;
  try { await signIn(email); } catch (e) { gone = e.code === 'INVALID_LOGIN_CREDENTIALS' || e.code === 'EMAIL_NOT_FOUND'; }
  return { email, uid: fb, docsDeleted: del.length, docsLeft: left, accountGone: gone };
}

try {
  for (const em of [emailA, emailB]) {
    try { const r = await idt('signUp', { email: em, password: PASSWORD }); creds.set(em, { uid: r.localId, email: r.email, refreshToken: r.refreshToken }); created.push(em); } catch (e) {
      if (e.code === 'OPERATION_NOT_ALLOWED') { console.log('cloud-live-test: skipped (Email/Password provider disabled: no headless way to create test accounts)'); process.exit(0); }
      throw e;
    }
  }
  console.log('New account on PC 1 (Google hand-off)');
  const A = pc('Misafir');
  const aUid = A.profile.get().uid;
  await A.cloud.o.history.put([rec(aUid, 1), rec(aUid, 2)]);
  let r = await gLogin(A, emailA, { askName: async () => nameA });
  ok(r.ok && r.newAccount, 'signed up as ' + nameA + (r.ok ? '' : ': ' + r.error));
  const fb = A.cloud.user.uid;
  const fs = A.cloud.fs;
  ok((await fs.get('names/' + nameKey(nameA))).data.uid === fb, 'name claimed');
  ok((await fs.get(`users/${fb}/meta/profile`)).data.uid === aUid, 'cloud profile carries the local 32-hex uid');
  ok((await fs.query(`users/${fb}`, { collection: 'matches', structured: {} })).length === 2, 'local history uploaded');
  ok((await fs.get('profiles/' + fb)).data.games === 2, 'public card written');
  ok(A.cloud.status === 'synced', 'status ' + A.cloud.statusText);

  console.log('Name uniqueness');
  const B = pc('Baska');
  const asked = [];
  r = await gLogin(B, emailB, { askName: async (q) => { asked.push(q); return asked.length === 1 ? nameA.toUpperCase() : null; } });
  ok(!r.ok && r.cancelled && asked.length === 2 && asked[1].error === 'Bu ad alınmış. Başka bir ad seç.', 'same name in other case refused: ' + (asked[1] && asked[1].error));
  ok(!B.cloud.loggedIn && B.profile.get().name === 'Baska', 'cancelled: B stays a guest');

  console.log('Save upload (a real game state)');
  const g = new Game({ mapSize: 128, enemies: 1, difficulty: 'normal', startRes: 'normal', startAge: 0, sandbox: false, seed: 4242 });
  for (let i = 0; i < 30 * 60; i++) g.update(1 / 30);
  const mid = '0123456789abcdef';
  let save = { name: 'Kayıt — canlı test', time: Date.now(), matchId: mid, data: g.serialize() };
  await A.cloud.o.saves.put('manual-live', save);
  A.cloud.onSaved('manual-live', { game: mid });
  await A.cloud.flush();
  const meta = (await fs.get(`users/${fb}/saves/manual-live`)).data;
  ok(meta && meta.chunks >= 1 && meta.enc === 'gzip', `uploaded: ${JSON.stringify(save).length} bytes JSON -> ${meta.chunks} chunk(s), sha ${meta.sha.slice(0, 12)}…`);
  // re-upload a newer version: one atomic commit (new chunks + meta + the old version's chunks deleted)
  save = Object.assign({}, save, { name: 'Kayıt — canlı test 2', time: save.time + 1000 });
  await A.cloud.o.saves.put('manual-live', save);
  A.cloud.onSaved('manual-live', { game: mid });
  await A.cloud.flush();
  const meta2 = (await fs.get(`users/${fb}/saves/manual-live`)).data;
  const chunkDocs = await fs.query(`users/${fb}/saves/manual-live`, { collection: 'chunks', structured: {} });
  ok(meta2.gen && meta2.gen !== meta.gen && chunkDocs.length === meta2.chunks && chunkDocs.every((c) => c.id.startsWith(meta2.gen + '-')), 're-upload replaced the version atomically, old chunks gone');

  console.log('Refresh + rename');
  const t1 = await A.cloud.auth.token(true);
  ok(typeof t1 === 'string' && t1.length > 100, 'id token refreshed via securetoken.googleapis.com');
  r = await A.cloud.rename(nameA2);
  ok(r.ok && (await fs.get('names/' + nameKey(nameA2))).data.uid === fb && !(await fs.get('names/' + nameKey(nameA))), 'renamed: new name claimed, old released');

  console.log('Login on PC 2');
  const C = pc('Konuk');
  const cUid = C.profile.get().uid;
  await C.cloud.o.history.put([rec(cUid, 7)]);
  let mergeAsked = 0;
  r = await gLogin(C, emailA, { askMerge: async (n) => { mergeAsked = n; return true; }, askName: async () => { throw new Error('not asked for an existing account'); } });
  ok(r.ok && r.switched && C.profile.get().uid === aUid && C.profile.get().name === nameA2, 'PC 2 adopts the account profile (uid + name)');
  ok(mergeAsked === 1 && r.merged === 1, 'asked to merge the 1 guest record');
  ok(C.hist.size === 3 && [...C.hist.values()].every((x) => x.uid === aUid), 'history pulled + guest record re-owned');
  ok((await fs.query(`users/${fb}`, { collection: 'matches', structured: {} })).length === 3, 'merged record uploaded');
  const list = mergeSaveLists(await C.cloud.o.saves.list(), await C.cloud.listCloudSaves({ force: true }));
  const it = list.find((x) => x.key === 'manual-live');
  ok(it && it.cloud === 'only', 'PC 2 lists the save as ☁ cloud-only');
  const got = await C.cloud.downloadSave(it.ck, it.key);
  ok(eq(got, save), 'downloaded + verified, identical to the upload');
  const g2 = Game.deserialize(got.data);
  ok(g2.tick === g.tick && g2.players.length === g.players.length, 'the downloaded state deserializes (tick ' + g2.tick + ')');
  C.cloud.logout();
  ok(C.profile.get().uid === cUid && !C.cloud.loggedIn, 'sign out on PC 2 -> its guest profile again');
} catch (e) {
  failed++; console.log('  FAIL exception: ' + (e && (e.code || '') + ' ' + (e && e.message)));
} finally {
  console.log('Cleanup');
  for (const email of created) {
    try { const w = await wipe(email); console.log('  ' + JSON.stringify(w)); if (w.docsLeft) failed++; if (w.accountGone === false) failed++; } catch (e) { failed++; console.log('  CLEANUP FAILED for ' + email + ': ' + (e && e.message)); }
  }
}
console.log(failed ? `\n${failed} FAILED` : '\nALL OK');
process.exit(failed ? 1 : 0);
