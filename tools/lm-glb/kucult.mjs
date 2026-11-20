// Shrinks a generated building model like the game's others: one mesh / one primitive, ~TRIS triangles, only the
// base colour texture at TEX px (jpeg), meshopt compressed. node kucult.mjs in.glb out.glb [tris=8000] [tex=512]
import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { dedup, flatten, join, weld, simplify, prune, textureCompress, meshopt, center } from '@gltf-transform/functions';
import { MeshoptSimplifier, MeshoptEncoder } from 'meshoptimizer';
import sharp from 'sharp';
const [inp, out, tris = '8000', tex = '512'] = process.argv.slice(2);
await MeshoptSimplifier.ready; await MeshoptEncoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.encoder': MeshoptEncoder });
const doc = await io.read(inp);
const count = () => { let n = 0; for (const m of doc.getRoot().listMeshes()) for (const p of m.listPrimitives()) n += (p.getIndices() ? p.getIndices().getCount() : p.getAttribute('POSITION').getCount()) / 3; return n | 0; };
// only the colour: no normal / roughness / occlusion / emissive maps (the game lights it its own way)
for (const m of doc.getRoot().listMaterials()) { m.setNormalTexture(null).setOcclusionTexture(null).setMetallicRoughnessTexture(null).setEmissiveTexture(null); m.setMetallicFactor(0).setRoughnessFactor(.9); }
const t0 = count();
await doc.transform(dedup(), flatten(), join(), weld());
const ratio = Math.min(1, +tris / Math.max(1, count()));
await doc.transform(simplify({ simplifier: MeshoptSimplifier, ratio, error: 0.01 }), prune(), textureCompress({ encoder: sharp, targetFormat: 'jpeg', resize: [+tex, +tex], quality: 82 }));
const prims = doc.getRoot().listMeshes().reduce((s, m) => s + m.listPrimitives().length, 0);
await doc.transform(meshopt({ encoder: MeshoptEncoder, level: 'medium' }));
await io.write(out, doc);
const fs = await import('node:fs');
console.log(`${inp}: ${t0} -> ${count()} üçgen, ${prims} parça, ${(fs.statSync(out).size / 1024).toFixed(0)} KB`);
