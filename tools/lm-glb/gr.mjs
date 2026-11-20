// minimal Gradio HTTP client: node gr.mjs <space-host> <api_name> '<json data array>'  -> prints the completed data
export async function call(host, api, data, { timeout = 600000 } = {}) {
  const base = `https://${host}/gradio_api`;
  const r = await fetch(`${base}/call/${api}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ data }) });
  if (!r.ok) throw new Error(api + ' POST ' + r.status + ' ' + (await r.text()).slice(0, 300));
  const { event_id } = await r.json();
  const ac = new AbortController(); const t = setTimeout(() => ac.abort(), timeout);
  const s = await fetch(`${base}/call/${api}/${event_id}`, { signal: ac.signal });
  const txt = await s.text(); clearTimeout(t);
  const ev = [...txt.matchAll(/event: (\w+)\ndata: (.*)/g)].map(m => [m[1], m[2]]);
  const done = ev.find(e => e[0] === 'complete'), err = ev.find(e => e[0] === 'error');
  if (!done) throw new Error(api + ' failed: ' + (err ? err[1] : txt.slice(-400)));
  return JSON.parse(done[1]);
}
export async function upload(host, file, buf, type = 'image/png') {
  const fd = new FormData(); fd.append('files', new Blob([buf], { type }), file);
  const r = await fetch(`https://${host}/gradio_api/upload`, { method: 'POST', body: fd });
  if (!r.ok) throw new Error('upload ' + r.status); const [p] = await r.json();
  return { path: p, meta: { _type: 'gradio.FileData' }, orig_name: file };
}
export async function download(host, f) { const url = f.url || `https://${host}/gradio_api/file=${f.path}`; const r = await fetch(url); if (!r.ok) throw new Error('download ' + r.status); return Buffer.from(await r.arrayBuffer()); }
