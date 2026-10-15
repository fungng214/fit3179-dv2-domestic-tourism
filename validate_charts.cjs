/* Compile every chart and render a static SVG using the same bundled runtime. */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const root = __dirname;
const ctx = { console, setTimeout, clearTimeout, URL, TextDecoder, performance, structuredClone };
vm.createContext(ctx);
for (const name of ['vega', 'vega-lite']) {
  vm.runInContext(fs.readFileSync(path.join(root, 'assets/vendor', name + '.min.js'), 'utf8'), ctx);
}
const out = path.join(root, 'assets/static');
fs.mkdirSync(out, { recursive: true });
(async () => {
  const report = [];
  for (const file of fs.readdirSync(path.join(root, 'chart-specs')).filter(f => f.endsWith('.json')).sort()) {
    try {
      const spec = JSON.parse(fs.readFileSync(path.join(root, 'chart-specs', file), 'utf8'));
      const compiled = spec.$schema.includes('vega-lite') ? ctx.vegaLite.compile(spec).spec : spec;
      const view = new ctx.vega.View(ctx.vega.parse(compiled), { renderer: 'none' });
      const svg = await view.toSVG();
      if (!svg.includes('<svg') || svg.includes('NaN')) throw new Error('Invalid SVG geometry');
      fs.writeFileSync(path.join(out, file.replace('.json', '.svg')), svg);
      // Validate the interactions used by the page, including both purpose datasets.
      for (const param of (spec.params || [])) {
        for (const value of param.bind?.options || []) {
          await view.signal(param.name, value).runAsync();
          const changed = await view.toSVG();
          if (changed.includes('NaN')) throw new Error('Invalid geometry after ' + param.name + '=' + value);
        }
      }
      view.finalize();
      report.push({ file, status: 'pass', bytes: Buffer.byteLength(svg) });
      console.log('PASS ' + file);
    } catch (error) {
      report.push({ file, status: 'fail', error: error.message });
      console.error('FAIL ' + file + ': ' + error.message);
    }
  }
  fs.writeFileSync(path.join(root, 'data/chart-validation.json'), JSON.stringify(report, null, 2) + '\n');
  if (report.some(r => r.status !== 'pass')) process.exitCode = 1;
})();
