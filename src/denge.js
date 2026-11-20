// The balance page (denge.html): the matchup table of the bot league's round robin (tools/lig.mjs --rr writes
// assets/denge/lig.json; ?f=<path> reads another file). Rows and columns sorted by the total win rate.
import { CIVS } from './civs.js';

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const short = (id) => (CIVS[id] ? CIVS[id].name.replace(/\s*\(.*\)$/, '') : id);
const pct = (w, n) => (n ? 100 * w / n : null);
// green above 50, red below, stronger the further from 50 (full at 25 points away)
function tint(p) {
  if (p == null) return '';
  const d = Math.max(-1, Math.min(1, (p - 50) / 25)), a = (.12 + .73 * Math.abs(d)).toFixed(2), rgb = d >= 0 ? 'var(--win)' : 'var(--lose)';
  const txt = Math.abs(d) < .08 ? '#f3e6c8' : d > 0 ? '#c9f5c0' : '#ffd2c8';
  return `background: rgba(${rgb}, ${Math.abs(d) < .04 ? .06 : a}); color: ${txt};`;
}
const pic = (id) => `<img class="pic" style="--c:${CIVS[id] ? CIVS[id].color : '#6b4a1e'}" src="${esc(CIVS[id] && CIVS[id].art ? CIVS[id].art : '')}" alt="" title="${esc(short(id))}" loading="lazy">`;

async function load() {
  const f = new URLSearchParams(location.search).get('f') || 'assets/denge/lig.json';
  let d;
  try { const r = await fetch(f, { cache: 'no-store' }); if (!r.ok) throw new Error(r.status); d = await r.json(); }
  catch (e) {
    $('wrap').innerHTML = `<div class="empty">Henüz ölçüm yok. Bot ligini çalıştır: <code>node tools/lig.mjs --rr</code> (bu tabloyu <code>assets/denge/lig.json</code>'a yazar).</div>`;
    return;
  }
  draw(d);
}

function draw(d) {
  const civs = d.civs.filter((c) => d.total[c]);
  const tot = (c) => pct(d.total[c].w, d.total[c].n);
  civs.sort((a, b) => tot(b) - tot(a));
  const cell = (a, b) => {   // a's record against b (the file holds each pair once)
    const x = d.pairs[a + '|' + b], y = d.pairs[b + '|' + a];
    if (x) return { n: x.n, w: x.w }; if (y) return { n: y.n, w: y.n - y.w }; return { n: 0, w: 0 };
  };
  const all = civs.map(tot), mean = all.reduce((s, v) => s + v, 0) / all.length, spread = Math.max(...all) - Math.min(...all);
  $('meta').innerHTML = [
    ['Tarih', d.date], ['Oyun sürümü', d.version], ['Bot zorluğu', d.diff], ['Haritalar', (d.maps || []).join(', ')],
    ['Eşleşme başına', d.perPair + ' maç'], ['Toplam', Object.values(d.pairs).reduce((s, p) => s + p.n, 0) + ' maç'],
    ['En iyi – en kötü', spread.toFixed(1) + ' puan'], ...(d.sets && d.sets.length ? [['Deneme ayarları', d.sets.join(' ')]] : []),
  ].map(([k, v]) => `<span>${esc(k)}: <b>${esc(v)}</b></span>`).join('');
  const per = d.perPair || 0;
  if (per && per < 20) { $('warn').hidden = false; $('warn').innerHTML = `<b>Dikkat:</b> her eşleşmede yalnızca ${per} maç var; tek bir hücre çok oynaktır (bir iki maç oranı 25 puan oynatır). Karar için <b>Toplam</b> sütununa bak; tek eşleşmeye bakmak için o ikiliyi daha çok maçla ayrıca ölç (<code>node tools/lig.mjs --vs ${esc(civs[0])} --only ${esc(civs[civs.length - 1])}</code>).`; }
  let h = '<table><thead><tr><th class="corner">Medeniyet</th><th class="tot">Toplam</th>';
  for (const b of civs) h += `<th data-c="${esc(b)}">${pic(b)}</th>`;
  h += '</tr></thead><tbody>';
  for (const a of civs) {
    const t = d.total[a], p = tot(a);
    h += `<tr data-r="${esc(a)}"><th><div class="rowc">${pic(a)}<div>${esc(short(a))}<small>${esc(CIVS[a] ? CIVS[a].icon : '')} ${t.min ? t.min + ' dk ort.' : ''}</small></div></div></th>`;
    h += `<td class="tot"><div class="cell" style="${tint(p)}" title="${esc(short(a))}: öteki bütün medeniyetlere karşı ${p.toFixed(1)} % (${t.n} maç${t.d ? ', ' + t.d + ' berabere' : ''})"><b>${p.toFixed(1)}%</b><i>${t.n}</i></div></td>`;
    for (const b of civs) {
      if (a === b) { h += `<td data-c="${esc(b)}"><div class="cell self"><b>—</b></div></td>`; continue; }
      const c = cell(a, b), q = pct(c.w, c.n);
      h += q == null ? `<td data-c="${esc(b)}"><div class="cell none">·</div></td>`
        : `<td data-c="${esc(b)}"><div class="cell" style="${tint(q)}" title="${esc(short(a))} – ${esc(short(b))}: ${q.toFixed(0)} % (${c.n} maçta ${String(+c.w.toFixed(1)).replace('.', ',')} galibiyet)"><b>${q.toFixed(0)}%</b><i>${c.n}</i></div></td>`;
    }
    h += '</tr>';
  }
  h += '</tbody></table>';
  $('wrap').innerHTML = h;
  $('note').textContent = `ortalama ${mean.toFixed(1)} % (kendi aralarında: 50 olmalı)`;
  // the sticky total column sits right after the (sticky) civilization column
  const th = $('wrap').querySelector('tbody th'); if (th) $('wrap').style.setProperty('--rowh', th.getBoundingClientRect().width + 2 + 'px');
  // hover: highlight the row's and the column's cells
  const tb = $('wrap').querySelector('table');
  tb.addEventListener('mouseover', (e) => {
    const td = e.target.closest('td[data-c]'), tr = e.target.closest('tr[data-r]');
    tb.querySelectorAll('.hl').forEach((x) => x.classList.remove('hl'));
    if (!td || !tr) return;
    tb.querySelectorAll(`[data-c="${td.dataset.c}"]`).forEach((x) => x.classList.add('hl'));
    tr.querySelectorAll('td').forEach((x) => x.classList.add('hl'));
  });
}
load();
