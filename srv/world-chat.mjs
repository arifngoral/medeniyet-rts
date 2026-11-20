// Medeniyet - the world chat: one public channel for everybody who has the game's menu open.
// Memory only (the free host sleeps and restarts; the last KEEP lines are lost then, which is fine for small talk).
// Pure logic, no I/O: server.js streams it over SSE (/mp/chat/live) and posts to it (/mp/chat/say).

export const CHAT = Object.freeze({
  KEEP: 60,          // lines a newcomer gets
  MAX_SUBS: 400,     // open streams at once
  TEXT_MAX: 200,
  NAME_MAX: 24,
  GAP_MS: 1500,      // at least this long between two lines of one sender
  PER_MIN: 12,       // and at most this many lines a minute
});

// control characters, zero-width and bidi overrides (a name must not turn the line around) -> space
const BAD = new RegExp('[\u0000-\u001f\u007f-\u009f\u200b-\u200f\u2028-\u202e\u2060-\u2069\ufeff]', 'g');
export const clean = (s, n) => String(s ?? '').replace(BAD, ' ').replace(/\s+/g, ' ').trim().slice(0, n);

export function createWorldChat({ now = () => Date.now() } = {}) {
  const hist = [], subs = new Set(), rate = new Map();
  let seq = 0;
  const cast = (o) => { for (const f of subs) { try { f(o); } catch { /* a dead stream; its close handler removes it */ } } };
  return {
    online: () => subs.size,
    // send(obj) for one stream -> leave() | null (full)
    join(send) {
      if (subs.size >= CHAT.MAX_SUBS) return null;
      subs.add(send);
      send({ type: 'hist', list: hist.slice(), online: subs.size });
      cast({ type: 'online', n: subs.size });
      return () => { if (subs.delete(send)) cast({ type: 'online', n: subs.size }); };
    },
    // key: who is rate limited (account or address); uid: the verified account (null = guest)
    say({ key, name, uid, text }) {
      const tx = clean(text, CHAT.TEXT_MAX);
      if (!tx) return { ok: false, error: 'empty' };
      const t = now();
      const l = (rate.get(key) || []).filter((x) => t - x < 60000);
      if ((l.length && t - l[l.length - 1] < CHAT.GAP_MS) || l.length >= CHAT.PER_MIN) return { ok: false, error: 'rate' };
      l.push(t); rate.set(key, l);
      const m = { type: 'msg', id: ++seq, t, name: clean(name, CHAT.NAME_MAX) || 'Misafir', guest: !uid, text: tx };
      if (uid) m.uid = String(uid).slice(0, 128);
      hist.push(m);
      if (hist.length > CHAT.KEEP) hist.splice(0, hist.length - CHAT.KEEP);
      cast(m);
      return { ok: true, id: m.id };
    },
    sweep() { const t = now(); for (const [k, l] of rate) if (!l.some((x) => t - x < 60000)) rate.delete(k); },
  };
}
