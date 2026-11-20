// Medeniyet - the world chat dock on the home screen: one public channel for everybody with the menu open
// (server: srv/world-chat.mjs, /mp/chat/live SSE + /mp/chat/say). The stream and the lines live in this module, so the
// menu can be rebuilt (_menuClear empties it) without losing them; worldChat(ui) only draws the dock again.
// With accounts on, writing needs a signed-in player (the server stamps the verified name); guests only read.
import { ACCOUNTS } from '../cloud/config.js';

const h = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = String(text); return e; };
const safe = (fn, d) => { try { return fn(); } catch (e) { return d; } };
const OPEN_KEY = 'mrts-wchat-open';
const S = { es: null, lines: [], online: 0, unread: 0, open: safe(() => localStorage.getItem(OPEN_KEY) === '1', false), ui: null, dock: null, ok: false };

const hhmm = (t) => { const d = new Date(t); return String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0'); };

function connect() {
  if (S.es || typeof EventSource === 'undefined') return;
  const es = new EventSource('/mp/chat/live');
  S.es = es;
  es.onopen = () => { S.ok = true; draw(); };
  es.onerror = () => { S.ok = false; draw(); };   // EventSource reconnects by itself
  es.onmessage = (ev) => {
    let m; try { m = JSON.parse(ev.data); } catch (e) { return; }
    if (!m) return;
    if (m.type === 'hist') { S.lines = Array.isArray(m.list) ? m.list : []; S.online = m.online | 0; draw(true); }
    else if (m.type === 'online') { S.online = m.n | 0; head(); }
    else if (m.type === 'msg') {
      if (S.lines.some((x) => x.id === m.id)) return;
      S.lines.push(m); if (S.lines.length > 120) S.lines.splice(0, S.lines.length - 120);
      if (!S.open && !mine(m)) S.unread++;
      if (!mine(m) && menuShown()) safe(() => S.ui.app.audio?.ui('chat'));
      addLine(m); head();
    }
  };
}
const menuShown = () => !!(S.ui && S.ui.mode === 'menu' && S.dock && S.dock.isConnected);
function myName() { const p = safe(() => S.ui.app.getProfile(), null); return p ? p.name : ''; }
const mine = (m) => !!m && !!myName() && m.name === myName();
function canWrite() { return ACCOUNTS ? !!safe(() => S.ui.app.cloud && S.ui.app.cloud.loggedIn, false) : true; }

function lineEl(m) {
  const l = h('div', 'wc-line' + (mine(m) ? ' mine' : ''));
  l.append(h('span', 'wc-t', hhmm(m.t)), h('b', 'wc-n' + (m.guest && ACCOUNTS ? ' guest' : ''), m.name + ':'), h('span', 'wc-x', m.text));
  return l;
}
function addLine(m) {
  const f = S.dock && S.dock.querySelector('.wc-feed'); if (!f) return;
  const near = f.scrollHeight - f.scrollTop - f.clientHeight < 40;
  f.querySelector('.wc-empty')?.remove();
  f.append(lineEl(m));
  while (f.childElementCount > 120) f.firstChild.remove();
  if (near || mine(m)) f.scrollTop = f.scrollHeight;
}
function head() {
  const d = S.dock; if (!d) return;
  d.querySelector('.wc-on').textContent = S.ok ? S.online + ' çevrim içi' : 'bağlanıyor…';
  const b = d.querySelector('.wc-badge'); b.textContent = S.unread > 99 ? '99+' : String(S.unread); b.classList.toggle('hidden', !S.unread || S.open);
}
function draw(toBottom) {
  const d = S.dock; if (!d) return;
  d.classList.toggle('open', S.open);
  const f = d.querySelector('.wc-feed');
  f.replaceChildren(...S.lines.map(lineEl));
  if (!S.lines.length) f.append(h('div', 'wc-empty', 'Henüz kimse yazmadı. İlk selamı sen ver!'));
  if (toBottom !== false) f.scrollTop = f.scrollHeight;
  head();
}
async function say(text, inp, err) {
  const app = S.ui.app, headers = { 'Content-Type': 'application/json' };
  if (ACCOUNTS) { try { headers['X-Aevum-Ticket'] = (await app.cloud.relayTicket()).ticket; } catch (e) { err.textContent = 'Yazmak için giriş yap.'; return; } }
  let r = null;
  try { r = await fetch('/mp/chat/say', { method: 'POST', headers, body: JSON.stringify({ text, name: myName() }) }); } catch (e) { err.textContent = 'Sunucuya ulaşılamadı.'; return; }
  if (r.ok) { inp.value = ''; err.textContent = ''; return; }
  err.textContent = r.status === 429 ? 'Biraz yavaş: art arda çok yazdın.' : r.status === 401 ? 'Yazmak için giriş yap.' : 'Gönderilemedi.';
}

// draws the dock into the home screen (called from ui._menuMain)
export function worldChat(ui) {
  S.ui = ui; connect();
  const d = h('aside', 'wchat');
  d.setAttribute('aria-label', 'Genel sohbet');
  const bar = h('button', 'wc-head'); bar.type = 'button';
  bar.append(h('span', 'wc-ico', '💬'), h('b', 'wc-title', 'Genel Sohbet'), h('span', 'wc-on'), h('span', 'wc-badge hidden'), h('span', 'wc-car', '▾'));
  bar.onclick = () => { S.open = !S.open; if (S.open) S.unread = 0; safe(() => localStorage.setItem(OPEN_KEY, S.open ? '1' : '0')); draw(); if (S.open) safe(() => d.querySelector('.wc-in').focus()); };
  const body = h('div', 'wc-body'), feed = h('div', 'wc-feed'), form = h('form', 'wc-form'), err = h('div', 'wc-err');
  const inp = h('input', 'wc-in mpinput'); inp.maxLength = 200; inp.autocomplete = 'off'; inp.spellcheck = false;
  const send = h('button', 'mbtn wc-send', 'Gönder'); send.type = 'submit';
  if (canWrite()) { inp.placeholder = 'Herkese yaz…'; form.append(inp, send); }
  else form.append(h('div', 'wc-ro', 'Yazmak için Google ile giriş yap.'));
  // the game's keyboard shortcuts must not fire while typing here
  for (const t of ['keydown', 'keyup', 'keypress']) inp.addEventListener(t, (e) => e.stopPropagation());
  form.onsubmit = (e) => { e.preventDefault(); const t = inp.value.trim(); if (t) say(t, inp, err); };
  body.append(feed, form, err);
  d.append(bar, body);
  S.dock = d;
  ui.menuEl.append(d);
  if (S.open) S.unread = 0;
  draw();
}
