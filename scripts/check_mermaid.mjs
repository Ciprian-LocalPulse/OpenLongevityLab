// Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.
// Syntax validation only; this does not verify rendered layout or scientific content.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(process.argv[2] ?? dirname(fileURLToPath(import.meta.url)) + '/..');
const tools = resolve(process.argv[3] ?? root);
const requireTool = createRequire(resolve(tools, 'package.json'));
const { JSDOM } = requireTool('jsdom');
const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import(pathToFileURL(requireTool.resolve('mermaid')).href);
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
const names = execFileSync('git', ['ls-files', '-z', '--', '*.md'], { cwd: root })
  .toString('utf8').split('\0').filter(Boolean);
const results = [];
for (const path of names) {
  const text = readFileSync(resolve(root, path), 'utf8');
  let index = 0;
  for (const block of text.matchAll(/^```mermaid\s*\r?\n([\s\S]*?)^```\s*$/gm)) {
    index += 1;
    try {
      await mermaid.parse(block[1]);
      results.push({ path, diagram: index, status: 'pass' });
    } catch (error) {
      results.push({ path, diagram: index, status: 'fail', error: String(error) });
    }
  }
}
const failed = results.filter(result => result.status === 'fail').length;
const packageInfo = JSON.parse(readFileSync(resolve(tools, 'node_modules/mermaid/package.json')));
console.log(JSON.stringify({
  check: 'Mermaid syntax parsing; not visual layout verification',
  supported_fences: 'Column-zero triple-backtick mermaid blocks, as used in this corpus',
  mermaid: packageInfo.version,
  diagrams: results.length,
  failed,
  results,
}, null, 2));
process.exitCode = failed ? 1 : 0;
