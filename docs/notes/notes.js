// Shared script of the notes pages.
// The build writes the fenced divs of the Markdown as plain HTML, so that every block reads without this
// script. Here the quiz gets its buttons, and every widget div gets its sliders and its plots.
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var BASE = (document.currentScript && document.currentScript.src || '').replace(/[^\/]*$/, '');

  // Quiz. The page holds <div class="quiz" data-correct="B"> with an <ol> of options in .quiz-options and the
  // answer in a closed <details>. Without this script the options stay a list and the answer is one click away.
  function initQuiz(q) {
    var correct = (q.getAttribute('data-correct') || '').charCodeAt(0) - 65;
    var items = q.querySelectorAll('.quiz-options > ol > li');
    if (!items.length || correct < 0) return;
    var status = document.createElement('div');
    status.className = 'quiz-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    var buttons = [];
    var done = false;
    items.forEach(function (li, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'quiz-opt';
      var letter = document.createElement('span');
      letter.className = 'quiz-letter';
      letter.textContent = String.fromCharCode(65 + i);
      var body = document.createElement('span');
      body.className = 'quiz-text';
      while (li.firstChild) body.appendChild(li.firstChild);
      b.appendChild(letter);
      b.appendChild(body);
      li.appendChild(b);
      buttons.push(b);
      b.addEventListener('click', function () {
        if (done) return;
        if (i === correct) {
          done = true;
          b.classList.add('right');
          buttons.forEach(function (x) { x.disabled = true; });
          status.textContent = 'This is correct. The explanation is below.';
          var d = q.querySelector('details.quiz-answer');
          if (d) d.open = true;
        } else {
          b.classList.add('wrong');
          b.disabled = true;
          status.textContent = 'This is not the one. Try another option, or open the answer below.';
        }
      });
    });
    q.querySelector('.quiz-options').appendChild(status);
  }

  // ---------------------------------------------------------------------------------------------------------------
  // Widgets. <div class="widget" data-widget="ID"> holds the introduction written in the Markdown. This script adds
  // the sliders and the plots. The curves come from widgets/ID.json, computed by webnotes/widgets/precompute.py with
  // the code of widgets/ID.py, so that they appear at once and without network. The button "Run live" loads Pyodide
  // from the CDN, installs what ID.py needs, and runs the same code in the browser for any value of the sliders.
  // ---------------------------------------------------------------------------------------------------------------
  var PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
  var PYQULA = 'pyqula==0.0.96';
  var SVGNS = 'http://www.w3.org/2000/svg';

  var GLUE = [
    'import json, numpy as np',
    '_W = {}',
    'def _clean(o):',
    '    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items() if v is not None}',
    '    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]',
    '    if isinstance(o, np.ndarray): return _clean(o.tolist())',
    '    if isinstance(o, (float, np.floating)):',
    '        x = float("%.5g" % float(o))',
    '        return 0.0 if x == 0 else x',
    '    if isinstance(o, np.integer): return int(o)',
    '    return o',
    'def _w_load(name, src):',
    '    ns = {}',
    '    exec(compile(src, name + ".py", "exec"), ns)',
    '    _W[name] = ns',
    'def _w_run(name, params):',
    '    return json.dumps(_clean(_W[name]["compute"](json.loads(params))))'
  ].join('\n');

  // pyqula asks for numba and jax at import. Pyodide has neither, so two small stand-ins are put in their place.
  // They are enough for the band structures and the finite systems of the widgets, where no jit code is needed.
  var SHIMS = [
    'import sys, types, numpy',
    'def _jit(*a, **k):',
    '    if len(a) == 1 and callable(a[0]) and not k: return a[0]',
    '    return lambda f: f',
    'nb = types.ModuleType("numba")',
    'nb.jit = nb.njit = _jit; nb.prange = range',
    'nb.config = types.SimpleNamespace(NUMBA_NUM_THREADS=1)',
    'jx = types.ModuleType("jax")',
    'jx.config = types.SimpleNamespace(update=lambda *a, **k: None)',
    'jx.jit = _jit; jx.grad = lambda f: f; jx.numpy = numpy; jx.devices = lambda *a, **k: []',
    'sys.modules.update({"numba": nb, "jax": jx, "jax.numpy": numpy})'
  ].join('\n');

  var pyPromise = null, pyInstalled = {};

  function loadScript(src) {
    return new Promise(function (ok, bad) {
      var s = document.createElement('script');
      s.src = src; s.onload = ok;
      s.onerror = function () { bad(new Error('the script ' + src + ' did not load')); };
      document.head.appendChild(s);
    });
  }

  function getPyodide(say) {
    if (!pyPromise) {
      pyPromise = (async function () {
        say('Loading Pyodide from the CDN');
        await loadScript(PYODIDE + 'pyodide.js');
        var py = await loadPyodide({ indexURL: PYODIDE });
        say('Loading numpy');
        await py.loadPackage('numpy');
        py.runPython(GLUE);
        return py;
      })();
      pyPromise.catch(function () { pyPromise = null; });
    }
    return pyPromise;
  }

  async function preparePython(meta, say) {
    var py = await getPyodide(say);
    var pk = (meta.packages || []).filter(function (p) { return !pyInstalled[p]; });
    if (pk.length) {
      say('Loading ' + pk.join(', '));
      await py.loadPackage(pk);
      pk.forEach(function (p) { pyInstalled[p] = true; });
    }
    if (meta.pyqula && !pyInstalled.pyqula) {
      say('Installing pyqula');
      await py.loadPackage('micropip');
      py.runPython(SHIMS);
      await py.runPythonAsync('import micropip\nawait micropip.install(["dill", "threadpoolctl", "multiprocess", "' +
                              PYQULA + '"], deps=False)');
      pyInstalled.pyqula = true;
    }
    return py;
  }

  // ----- plots -----
  var GREEK = [[/\bphi\b/g, '\u03c6'], [/\bpsi\b/g, '\u03c8'], [/\bDelta\b/g, '\u0394'], [/\bomega_c\b/g, '\u03c9_c'], [/\bgamma_K\b/g, '\u03b3_K'], [/\bomega\b/g, '\u03c9'], [/\bgamma\b/g, '\u03b3'],
               [/\bmu\b/g, '\u03bc'], [/\bpi\b/g, '\u03c0'], [/(\d)pi\b/g, '$1\u03c0'], [/\bhbar\b/g, '\u0127'],
               [/\+-/g, '\u00b1'], [/\^2/g, '\u00b2']];
  function pretty(s) {
    GREEK.forEach(function (g) { s = s.replace(g[0], g[1]); });
    return s;
  }

  function el(tag, attrs, text) {
    var e = document.createElementNS(SVGNS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }

  function niceStep(raw) {
    var p = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / p;
    return (f < 1.5 ? 1 : f < 3.5 ? 2 : f < 7.5 ? 5 : 10) * p;
  }
  function ticksOf(lo, hi, n) {
    var st = niceStep((hi - lo) / n), out = [];
    for (var v = Math.ceil(lo / st - 1e-9) * st; v <= hi + st * 1e-6; v += st) out.push(Math.abs(v) < st * 1e-9 ? 0 : v);
    var dec = Math.max(0, -Math.floor(Math.log10(st) + 1e-9));
    return out.map(function (v) { return [v, v.toFixed(dec)]; });
  }

  var plotId = 0;
  function drawPanel(P) {
    var hasLeg = (P.series || []).some(function (s) { return s.label; });
    var W = 420, Hh = (P.equal ? 330 : 300) + (hasLeg ? 18 : 0), L = 54, R = 14, T = 30, B = 44 + (hasLeg ? 18 : 0);
    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + Hh, role: 'img', 'class': 'wplot' });
    var title = P.title ? pretty(P.title) : '';
    svg.setAttribute('aria-label', title);
    var xs = [], ys = [];
    (P.series || []).forEach(function (s) {
      s.x.forEach(function (v) { xs.push(v); });
      s.y.forEach(function (v) { ys.push(v); });
    });
    (P.marks || []).forEach(function (m) { xs.push(m.x); ys.push(m.y); });
    function span(a, lim) {
      if (lim) return lim;
      var lo = Math.min.apply(null, a), hi = Math.max.apply(null, a);
      if (hi - lo < 1e-12) { lo -= 1; hi += 1; }
      var pad = 0.06 * (hi - lo);
      return [lo - pad, hi + pad];
    }
    var xl = span(xs, P.xlim), yl = span(ys, P.ylim);
    var pw = W - L - R, ph = Hh - T - B;
    if (P.equal) {                                   // the same length for one unit on x and on y
      var sx = pw / (xl[1] - xl[0]), sy = ph / (yl[1] - yl[0]), s = Math.min(sx, sy);
      var cx = (xl[0] + xl[1]) / 2, cy = (yl[0] + yl[1]) / 2;
      xl = [cx - pw / 2 / s, cx + pw / 2 / s]; yl = [cy - ph / 2 / s, cy + ph / 2 / s];
    }
    function X(v) { return L + (v - xl[0]) / (xl[1] - xl[0]) * pw; }
    function Y(v) { return T + ph - (v - yl[0]) / (yl[1] - yl[0]) * ph; }
    var cid = 'wc' + (++plotId);
    var clip = el('clipPath', { id: cid });
    clip.appendChild(el('rect', { x: L, y: T, width: pw, height: ph }));
    svg.appendChild(clip);
    svg.appendChild(el('rect', { x: L, y: T, width: pw, height: ph, 'class': 'wframe' }));
    var xt = P.xticks || ticksOf(xl[0], xl[1], 5), yt = ticksOf(yl[0], yl[1], 5);
    xt.forEach(function (t) {
      svg.appendChild(el('line', { x1: X(t[0]), x2: X(t[0]), y1: T, y2: T + ph, 'class': 'wgrid' }));
      svg.appendChild(el('text', { x: X(t[0]), y: T + ph + 15, 'class': 'wtick', 'text-anchor': 'middle' }, pretty(t[1])));
    });
    yt.forEach(function (t) {
      svg.appendChild(el('line', { x1: L, x2: L + pw, y1: Y(t[0]), y2: Y(t[0]), 'class': 'wgrid' }));
      svg.appendChild(el('text', { x: L - 6, y: Y(t[0]) + 4, 'class': 'wtick', 'text-anchor': 'end' }, t[1]));
    });
    if (xl[0] < 0 && xl[1] > 0) svg.appendChild(el('line', { x1: X(0), x2: X(0), y1: T, y2: T + ph, 'class': 'waxis' }));
    if (yl[0] < 0 && yl[1] > 0) svg.appendChild(el('line', { x1: L, x2: L + pw, y1: Y(0), y2: Y(0), 'class': 'waxis' }));
    var g = el('g', { 'clip-path': 'url(#' + cid + ')' });
    var legend = [];
    (P.series || []).forEach(function (s) {
      var col = 'var(--w' + (s.color || 0) + ')', kind = s.kind || 'line';
      if (kind !== 'points') {
        var d = '';
        for (var i = 0; i < s.x.length; i++) d += (i ? 'L' : 'M') + X(s.x[i]).toFixed(1) + ' ' + Y(s.y[i]).toFixed(1);
        var path = el('path', { d: d, 'class': 'wline' + (kind === 'dash' ? ' dash' : ''), stroke: col });
        g.appendChild(path);
      }
      if (kind === 'points' || kind === 'both') {
        var r = kind === 'both' ? 2.2 : 2.8;
        for (var j = 0; j < s.x.length; j++)
          g.appendChild(el('circle', { cx: X(s.x[j]).toFixed(1), cy: Y(s.y[j]).toFixed(1), r: r, fill: col }));
      }
      if (s.label) legend.push([s.label, col, kind]);
    });
    (P.marks || []).forEach(function (m) {
      g.appendChild(el('circle', { cx: X(m.x), cy: Y(m.y), r: 5.5, 'class': 'wmark' }));
    });
    svg.appendChild(g);
    var lx = L;
    legend.forEach(function (l) {
      var txt = pretty(l[0]), ly = Hh - 9;
      svg.appendChild(el('line', { x1: lx, x2: lx + 18, y1: ly - 4, y2: ly - 4, stroke: l[1],
                                    'class': 'wline' + (l[2] === 'dash' ? ' dash' : '') }));
      svg.appendChild(el('text', { x: lx + 23, y: ly, 'class': 'wleg' }, txt));
      lx += 23 + txt.length * 5.6 + 16;
    });
    if (title) svg.appendChild(el('text', { x: L, y: 18, 'class': 'wtitle' }, title));
    if (P.xlabel) svg.appendChild(el('text', { x: L + pw / 2, y: Hh - B + 40, 'class': 'wlabel', 'text-anchor': 'middle' }, pretty(P.xlabel)));
    if (P.ylabel) svg.appendChild(el('text', { x: 13, y: T + ph / 2, 'class': 'wlabel', 'text-anchor': 'middle',
                                                transform: 'rotate(-90 13 ' + (T + ph / 2) + ')' }, pretty(P.ylabel)));
    return svg;
  }

  // ----- one widget -----
  function initWidget(root) {
    var id = root.getAttribute('data-widget');
    var box = document.createElement('div');
    box.className = 'widget-ui';
    root.appendChild(box);
    var controls = document.createElement('div'); controls.className = 'widget-controls';
    var plots = document.createElement('div'); plots.className = 'widget-plots';
    var readout = document.createElement('p'); readout.className = 'widget-text';
    readout.setAttribute('role', 'status'); readout.setAttribute('aria-live', 'polite');
    var actions = document.createElement('div'); actions.className = 'widget-actions';
    var live = document.createElement('button'); live.type = 'button'; live.className = 'widget-live';
    var say = document.createElement('span'); say.className = 'widget-status';
    var code = document.createElement('details'); code.className = 'widget-code';
    code.innerHTML = '<summary>Show the Python code</summary><pre><code></code></pre>';
    actions.appendChild(live); actions.appendChild(say);
    box.appendChild(controls); box.appendChild(plots); box.appendChild(readout); box.appendChild(actions);
    box.appendChild(code);
    plots.textContent = 'Loading the curves.';

    var data = null, meta = null, liveReady = false, seq = 0, timer = null, srcText = null;
    var inputs = [], outputs = [];

    function values() { return inputs.map(function (i) { return parseFloat(i.value); }); }
    function key() {
      return meta.params.map(function (p, k) {
        return Math.round((parseFloat(inputs[k].value) - p.min) / p.step);
      }).join(',');
    }
    function show(res) {
      plots.textContent = '';
      var n = res.panels.length;
      plots.className = 'widget-plots' + (n === 1 ? ' one' : '');
      res.panels.forEach(function (P) { plots.appendChild(drawPanel(P)); });
      readout.textContent = pretty(res.text || '');
    }
    function refresh() {
      meta.params.forEach(function (p, k) { outputs[k].textContent = parseFloat(inputs[k].value).toFixed(p.fmt); });
      if (liveReady) {
        var mine = ++seq, par = {};
        meta.params.forEach(function (p, k) { par[p.name] = parseFloat(inputs[k].value); });
        clearTimeout(timer);
        timer = setTimeout(function () {
          try {
            var res = JSON.parse(window.__aqmPy.globals.get('_w_run')(id, JSON.stringify(par)));
            if (mine === seq) show(res);
          } catch (e) { say.textContent = 'The live run failed (' + e.message.split('\n').slice(-2)[0] + '). Back to the precomputed curves.'; goOffline(); }
        }, 60);
        return;
      }
      var r = data.grid[key()];
      if (r) show(r);
    }
    function goOffline() {
      liveReady = false;
      meta.params.forEach(function (p, k) { inputs[k].step = p.step; });
      live.disabled = false; live.textContent = 'Run live in the browser';
      refresh();
    }
    function build() {
      meta.params.forEach(function (p, k) {
        var row = document.createElement('label'); row.className = 'widget-row';
        var name = document.createElement('span'); name.className = 'widget-name'; name.textContent = pretty(p.label);
        var inp = document.createElement('input');
        inp.type = 'range'; inp.min = p.min; inp.max = p.max; inp.step = p.step; inp.value = p.value;
        var out = document.createElement('output'); out.className = 'widget-value';
        inp.addEventListener('input', refresh);
        row.appendChild(name); row.appendChild(inp); row.appendChild(out);
        controls.appendChild(row);
        inputs.push(inp); outputs.push(out);
      });
      var seconds = meta.pyqula ? 25 : 8;
      live.textContent = 'Run live in the browser';
      live.title = 'Loads Python (Pyodide) from the CDN, about ' + seconds + ' s the first time';
      say.textContent = 'The curves are precomputed on the grid of the sliders.';
      live.addEventListener('click', function () {
        live.disabled = true;
        preparePython(meta, function (m) { say.textContent = m + '.'; }).then(async function (py) {
          window.__aqmPy = py;
          if (!srcText) srcText = await (await fetch(BASE + 'widgets/' + id + '.py')).text();
          say.textContent = 'Running the code once.';
          py.globals.get('_w_load')(id, srcText);
          var par = {};
          meta.params.forEach(function (p, k) { par[p.name] = parseFloat(inputs[k].value); });
          py.globals.get('_w_run')(id, JSON.stringify(par));
          liveReady = true;
          meta.params.forEach(function (p, k) { if (p.step < 1) inputs[k].step = p.step / 5; });
          live.textContent = 'Live: Python runs in your browser';
          say.textContent = 'Any value of the sliders is computed with the code below.';
          refresh();
        }).catch(function (e) {
          say.textContent = 'Python could not start here (' + (e && e.message ? e.message.split('\n').slice(-1)[0] : e) +
                            '). The precomputed curves still work.';
          live.disabled = false;
        });
      });
      code.addEventListener('toggle', async function () {
        if (!code.open || code.getAttribute('data-done')) return;
        try {
          if (!srcText) srcText = await (await fetch(BASE + 'widgets/' + id + '.py')).text();
          code.querySelector('code').textContent = srcText;
          code.setAttribute('data-done', '1');
        } catch (e) { code.querySelector('code').textContent = 'The code could not be loaded.'; }
      });
      refresh();
    }
    function start() {
      fetch(BASE + 'widgets/' + id + '.json').then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      }).then(function (d) { data = d; meta = d.meta; build(); }).catch(function () {
        plots.textContent = 'The data of this widget could not be loaded. Open the notes from the web page and not from a file.';
      });
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); start(); }
      }, { rootMargin: '400px' });
      io.observe(root);
    } else start();
  }

  function init() {
    document.querySelectorAll('.quiz').forEach(initQuiz);
    document.querySelectorAll('.widget[data-widget]').forEach(initWidget);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
