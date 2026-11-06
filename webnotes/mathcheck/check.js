// Renders every math fragment of docs/notes/ with MathJax 3.2.2, the version and the TeX
// configuration of the pages (webnotes/template.py), and lists the fragments that fail.
// Usage: node check.js [notes_dir]     exit code 1 if there is any error.
// It uses the packages of the tex-chtml bundle, and it does not load "noundefined", so an
// unknown macro is an error here, where the page would show it in red.
const fs = require('fs');
const path = require('path');
const { mathjax } = require('mathjax-full/js/mathjax.js');
const { TeX } = require('mathjax-full/js/input/tex.js');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor.js');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html.js');
require('mathjax-full/js/input/tex/base/BaseConfiguration.js');
const PACKAGES = ['base', 'ams', 'newcommand', 'configmacros', 'action', 'bbox', 'boldsymbol',
  'cancel', 'color', 'enclose', 'extpfeil', 'html', 'mhchem', 'unicode', 'verb'];
const { AllPackages } = require('mathjax-full/js/input/tex/AllPackages.js');

const root = path.resolve(process.argv[2] || path.join(__dirname, '..', '..', 'docs', 'notes'));
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({
  packages: PACKAGES.filter(p => AllPackages.includes(p)),
  tags: 'none',
  formatError: (jax, err) => { throw err; },
});
const doc = mathjax.document('', { InputJax: tex });

function walk(d) {
  return fs.readdirSync(d, { withFileTypes: true }).flatMap(e =>
    e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.html') ? [path.join(d, e.name)] : []);
}
const unescape = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
  .replace(/&#39;/g, "'").replace(/&amp;/g, '&');

let n = 0, bad = 0;
for (const f of walk(root).sort()) {
  const src = fs.readFileSync(f, 'utf8');
  const re = /<span class="math (inline|display)">\\(?:\(|\[)([\s\S]*?)\\(?:\)|\])<\/span>/g;
  let m;
  while ((m = re.exec(src))) {
    n++;
    const text = unescape(m[2]);
    try {
      doc.convert(text, { display: m[1] === 'display' });
    } catch (err) {
      bad++;
      console.log(`${path.relative(root, f)}: ${err.message}\n    ${text.replace(/\s+/g, ' ').slice(0, 200)}`);
    }
  }
}
console.log(`mathcheck: ${n} fragments checked, ${bad} errors`);
process.exit(bad ? 1 : 0);
