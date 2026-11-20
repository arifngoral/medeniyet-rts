// Medeniyet - the world chat's lasting copy in Firestore (collection `chat`), so a restart / sleep of the free host does
// not empty it. No service account: a line is written with its sender's own Firebase ID token (the rules in
// firestore.rules let a player create only lines with their own uid and profile name), and the history is read without
// a token (the chat is public: `chat` is readable by everybody).
//   chat/{id}  { t: ms, uid: Firebase uid, name, text }

const FS = 'https://firestore.googleapis.com/v1/';

const str = (v) => ({ stringValue: String(v) });
const fields = (m) => ({ t: { integerValue: String(Math.trunc(m.t)) }, uid: str(m.uid), name: str(m.name), text: str(m.text) });
function unfields(f) {
  if (!f) return null;
  const s = (k) => (f[k] && typeof f[k].stringValue === 'string' ? f[k].stringValue : '');
  const t = Number(f.t && f.t.integerValue);
  if (!Number.isFinite(t) || !s('text')) return null;
  return { t, uid: s('uid'), name: s('name'), text: s('text') };
}

// opts: { projectId, fetch, log(tag, err) }
export function createChatStore({ projectId, fetch: fetchFn = globalThis.fetch, log = () => {} }) {
  const root = `projects/${projectId}/databases/(default)/documents`;
  return {
    // the last `n` lines, oldest first -> [{t, uid, name, text}]
    async load(n = 60) {
      const r = await fetchFn(FS + root + ':runQuery', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ structuredQuery: { from: [{ collectionId: 'chat' }], orderBy: [{ field: { fieldPath: 't' }, direction: 'DESCENDING' }], limit: n } }),
      });
      if (!r.ok) throw new Error('chat load ' + r.status + ' ' + (await r.text()).slice(0, 200));
      const arr = await r.json();
      const out = [];
      for (const x of Array.isArray(arr) ? arr : []) { const m = x && x.document && unfields(x.document.fields); if (m) out.push(m); }
      return out.reverse();
    },
    // writes one line with the sender's ID token; never throws (the line is already shown live)
    async save(m, idToken) {
      if (!idToken || !m || !m.uid) return false;
      const id = m.t.toString(36) + '-' + Math.random().toString(36).slice(2, 10);
      try {
        const r = await fetchFn(FS + root + '/chat?documentId=' + id, {
          method: 'POST', headers: { Authorization: 'Bearer ' + idToken, 'Content-Type': 'application/json' },
          body: JSON.stringify({ fields: fields(m) }),
        });
        if (!r.ok) { log('chat save', new Error(r.status + ' ' + (await r.text()).slice(0, 200))); return false; }
        return true;
      } catch (e) { log('chat save', e); return false; }
    },
  };
}
