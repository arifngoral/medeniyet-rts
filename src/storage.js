// IndexedDB save storage. All functions are promise based and never throw.
const DB_NAME = 'aevum';
const STORE = 'aevum-saves';
const HISTORY = 'aevum-history';   // match history (separate store: never listed with the saves)
const DB_VERSION = 2;
export const HISTORY_CAP = 500;
let dbPromise = null;
let blockedHandler = null;
let wasBlocked = false;
// fn(true): the database upgrade waits for an older Aevum tab (the UI tells the player to close it); fn(false): done
export function onBlocked(fn) { blockedHandler = typeof fn === 'function' ? fn : null; }

function openDB() {
  if (dbPromise) return dbPromise;
  dbPromise = new Promise((resolve, reject) => {
    try {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      // only creates what is missing: existing saves stay untouched
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE);
        if (!db.objectStoreNames.contains(HISTORY)) db.createObjectStore(HISTORY);
      };
      req.onsuccess = () => {
        const db = req.result;
        if (wasBlocked) { wasBlocked = false; try { if (blockedHandler) blockedHandler(false); } catch (e) { /* ignore */ } }
        // another tab opens a newer version: let it upgrade, reopen on the next call
        db.onversionchange = () => { try { db.close(); } catch (e) { /* ignore */ } dbPromise = null; };
        resolve(db);
      };
      req.onblocked = () => {
        console.warn('[storage] upgrade waits for another Aevum tab to close');
        wasBlocked = true;
        try { if (blockedHandler) blockedHandler(true); } catch (e) { /* ignore */ }
      };
      req.onerror = () => reject(req.error);
    } catch (err) { reject(err); }
  });
  dbPromise.catch(() => { dbPromise = null; });
  return dbPromise;
}

function run(mode, fn, storeName = STORE) {
  return openDB().then(db => new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, mode);
    const store = tx.objectStore(storeName);
    let result;
    const req = fn(store);
    if (req) req.onsuccess = () => { result = req.result; };
    tx.oncomplete = () => resolve(result);
    tx.onerror = () => reject(tx.error);
    tx.onabort = () => reject(tx.error);
  }));
}

export async function put(key, value) {
  try { await run('readwrite', s => s.put(value, key)); return true; }
  catch (err) { console.warn('[storage] put failed', err); return false; }
}

export async function get(key) {
  try { return (await run('readonly', s => s.get(key))) || null; }
  catch (err) { console.warn('[storage] get failed', err); return null; }
}

export async function del(key) {
  try { await run('readwrite', s => s.delete(key)); return true; }
  catch (err) { console.warn('[storage] delete failed', err); return false; }
}

// multiplayer saves: key 'mp-<match code>-<tick|auto>', record {name, time, mp:true, code, tick, me, players, hash, data}
export const MP_PREFIX = 'mp-';
export const isMpKey = k => String(k).startsWith(MP_PREFIX);

// -> [{key,name,time}] newest first (multiplayer records also carry mp, code, tick, me, players)
export async function list() {
  try {
    const db = await openDB();
    return await new Promise((resolve, reject) => {
      const out = [];
      const tx = db.transaction(STORE, 'readonly');
      const req = tx.objectStore(STORE).openCursor();
      req.onsuccess = () => {
        const c = req.result;
        if (c) {
          const v = c.value || {};
          const item = { key: String(c.key), name: v.name || String(c.key), time: v.time || 0 };
          if (typeof v.matchId === 'string') item.matchId = v.matchId;   // (pairs the local autosave slot with its cloud copy)
          if (typeof v.owner === 'string') item.owner = v.owner;         // profile uid of the account that saved it
          if (v.mp) Object.assign(item, { mp: true, code: v.code || null, tick: v.tick | 0, me: v.me, players: Array.isArray(v.players) ? v.players : [] });
          out.push(item);
          c.continue();
        }
      };
      tx.oncomplete = () => resolve(out.sort((a, b) => b.time - a.time));
      tx.onerror = () => reject(tx.error);
    });
  } catch (err) { console.warn('[storage] list failed', err); return []; }
}

// ---------- match history (store 'aevum-history', key = record id) ----------
function getAllHistory() {
  return run('readonly', s => s.getAll(), HISTORY).then(v => (Array.isArray(v) ? v : []));
}
// newest first
export async function historyList() {
  try { return (await getAllHistory()).sort((a, b) => (b.endedAt || 0) - (a.endedAt || 0)); }
  catch (err) { console.warn('[storage] history list failed', err); return []; }
}
export async function historyGet(id) {
  try { return (await run('readonly', s => s.get(id), HISTORY)) || null; }
  catch (err) { console.warn('[storage] history get failed', err); return null; }
}
// the ids to evict: the cap is per owner profile uid, so one profile's records (an account's history pulled from
// the cloud on a shared PC) never push out another profile's (a guest's records exist nowhere else).
// all: newest first. Pure (test/cloud-test.mjs).
export function historyTrimIds(all, cap = HISTORY_CAP) {
  const n = new Map(), drop = [];
  for (const r of all || []) {
    const k = r && typeof r.uid === 'string' ? r.uid : '';
    const c = (n.get(k) || 0) + 1; n.set(k, c);
    if (c > cap) drop.push(r.id);
  }
  return drop;
}
async function trimHistory() {
  const drop = historyTrimIds(await historyList());
  if (drop.length) await run('readwrite', s => { for (const id of drop) s.delete(id); }, HISTORY);
}
// insert or replace records by id, then keep the newest HISTORY_CAP per profile
export async function historyPut(...recs) {
  try {
    recs = recs.flat().filter(r => r && typeof r.id === 'string');
    if (!recs.length) return true;
    await run('readwrite', s => { for (const r of recs) s.put(r, r.id); }, HISTORY);
    await trimHistory();
    return true;
  } catch (err) { console.warn('[storage] history put failed', err); return false; }
}
export async function historyDelete(ids) {
  try {
    ids = (ids || []).filter(id => typeof id === 'string');
    if (ids.length) await run('readwrite', s => { for (const id of ids) s.delete(id); }, HISTORY);
    return true;
  } catch (err) { console.warn('[storage] history delete failed', err); return false; }
}
export async function historyClear() {
  try { await run('readwrite', s => s.clear(), HISTORY); return true; }
  catch (err) { console.warn('[storage] history clear failed', err); return false; }
}

export default { onBlocked, put, get, delete: del, del, list, MP_PREFIX, isMpKey, historyList, historyGet, historyPut, historyDelete, historyClear, HISTORY_CAP };
