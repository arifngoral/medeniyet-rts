import fs from 'node:fs'; import { call, download } from './gr.mjs';
const [out, prompt, seed = '42'] = process.argv.slice(2), H = 'black-forest-labs-flux-1-schnell.hf.space';
const d = await call(H, 'infer', [prompt, +seed, false, 1024, 1024, 4]);
fs.writeFileSync(out, await download(H, d[0])); console.log('ok', out);
