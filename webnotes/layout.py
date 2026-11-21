"""Measures the layout of built pages of the notes in headless Chrome, without reading any image.

    python3 webnotes/layout.py BUILD_DIR --session N [--page FILE] [--width 1000 390] [--jobs 4] [-v]

BUILD_DIR is the folder of a private build (build.py --out BUILD_DIR). For each page and each width, a copy of the
page with one added script is loaded in headless Chrome. The script waits for MathJax and the images, opens every
<details>, clicks the first option of every quiz so that a feedback is open, measures, and writes a JSON report that
is read back with --dump-dom. Chrome does not make a window narrower than 500 px, so the page is loaded in an iframe
of the width asked for, inside a small wrapper page, and the report comes back to the wrapper by postMessage.

What is reported, one line per finding with the page, the width and the pixels.
- The page is wider than the window, so the document scrolls sideways. The elements that cause it are listed too.
- An element sticks out of the window, or out of its box: figures and their images, quiz options and their pictures,
  the boxes (keybox, recall, lab, problem, fold, comesback, tryit, quiz), tables, code and math. An element cut by
  a box with overflow hidden (a quiz) gives no scroll and is reported as cut.
- Two sibling elements inside a quiz overlap.
- An image did not load.
A display equation that scrolls inside its own block (overflow-x: auto) is intended and is not reported, and the
same holds for anything inside a block that scrolls. The text inside the SVG of a picture is not measured.

The copies are written in a new folder next to the page, with a <base> to the folder of the page so that every
relative link works, and they are removed at the end (os.remove of each file, then os.rmdir of the folder). The exit
code is 1 when there is a finding or a page that could not be measured, else 0.
"""
import argparse
import concurrent.futures
import glob
import html
import json
import os
import re
import subprocess
import sys
import tempfile

CHROME = 'google-chrome'
WINDOW_H = 1000          # height of the window and of the iframe, in px
BUDGET_MS = 120000       # virtual time of Chrome; it does not run while a file or the CDN is being fetched
TIMEOUT_S = 180          # real time for one page and one width
TOL = 1                  # px of rounding that is not a finding

# The script added to the copy of the page. It runs after notes.js, which turns the quizzes into buttons.
PROBE = r"""
<script>
(function () {
  'use strict';
  var BOXES = '.keybox, .recall, .lab, .problem, .fold-details, .comesback, .tryit, .quiz';
  var HOLDERS = 'button.quiz-opt, ' + BOXES + ', figure, .widget, .notebookbox, table, main';
  var TARGETS = 'figure, figure img, .quiz-opt, .quiz-opt img, ' + BOXES + ', table, pre, code, mjx-container';
  var TOL = %(tol)s;
  var HTMLNS = 'http://www.w3.org/1999/xhtml';
  var info = { layout: 1 };
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  async function until(f, ms) { for (var t = 0; !f() && t < ms; t += 50) await sleep(50); return !!f(); }
  function cs(el) { return getComputedStyle(el); }
  function clip(s, n) { return s.length > n ? s.slice(0, n - 3) + '...' : s; }

  async function settle(els) {
    if (info.mathjax && els.length) { try { await MathJax.typesetPromise(els); } catch (e) {} }
    try { await document.fonts.ready; } catch (e) {}
    await until(function () { return Array.prototype.every.call(document.images, function (i) { return i.complete; }); }, 20000);
    await sleep(500);              // timers only: Chrome's virtual time does not wait for a frame or a decode
  }

  function measure() {
    var de = document.documentElement, vw = de.clientWidth, out = [];
    info.vw = vw; info.sw = de.scrollWidth; info.findings = out;
    var tex = new Map();
    try { for (var m of MathJax.startup.document.math) if (m.typesetRoot) tex.set(m.typesetRoot, m.math); } catch (e) {}
    var heads = Array.prototype.slice.call(document.querySelectorAll('h1[id], h2[id], h3[id], h4[id]'));
    function where(el) {
      var s = '';
      heads.forEach(function (h) { if (h === el || (h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) s = h.id; });
      return s;
    }
    function label(el) {
      var t = el.tagName.toLowerCase(), s = t + (el.classList.length ? '.' + Array.prototype.join.call(el.classList, '.') : '');
      if (t === 'img') return 'image ' + (el.getAttribute('src') || '').split('/').pop();
      if (t === 'mjx-container') {
        var x = tex.get(el);
        return (el.getAttribute('display') === 'true' ? 'display math' : 'inline math') + (x ? ' "' + clip(x.replace(/\s+/g, ' ').trim(), 60) + '"' : '');
      }
      var img = t === 'figure' && el.querySelector('img');
      if (img) return s + ' (' + (img.getAttribute('src') || '').split('/').pop() + ')';
      var mj = el.classList.contains('math') && el.querySelector('mjx-container');
      if (mj) return label(mj);
      if (el.id) return s + '#' + el.id;
      var txt = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
      return s + (txt ? ' "' + clip(txt, 40) + '"' : '');
    }
    function inside(el, stop, re) {            // the nearest ancestor below stop whose overflow-x matches re
      for (var p = el.parentElement; p && p !== stop && p !== document.body; p = p.parentElement)
        if (re.test(cs(p).overflowX)) return p;
      return null;
    }
    var SCROLL = /auto|scroll/, CLIP = /hidden|clip/;
    function inner(el) {                       // the box inside the border, where the content may go
      var r = el.getBoundingClientRect(), s = cs(el);
      return { left: r.left + parseFloat(s.borderLeftWidth), right: r.right - parseFloat(s.borderRightWidth),
               top: r.top + parseFloat(s.borderTopWidth), bottom: r.bottom - parseFloat(s.borderBottomWidth) };
    }
    function rect(el) { var r = el.getBoundingClientRect(); return (r.width < 0.5 && r.height < 0.5) ? null : r; }
    function shown(el) {
      for (var p = el; p; p = p.parentElement) if (cs(p).visibility !== 'visible') return false;
      return true;
    }

    if (de.scrollWidth - vw > TOL) out.push({ kind: 'page', px: de.scrollWidth - vw });

    // out of the window: the outermost elements past the edge, that no scrolling block holds. A part of a formula
    // (a glyph, or the MathML that MathJax hides for screen readers) is counted for its mjx-container, since it can
    // make the page scroll while the formula itself fits.
    var past = new Map(), reported = new Set(), viaparts = new Map();
    var all = document.body.getElementsByTagName('*');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      var r = rect(el);
      if (!r) continue;
      var over = Math.max(r.right - vw, -r.left);
      if (over <= TOL) continue;
      if (el.namespaceURI !== HTMLNS || (/^MJX-/.test(el.tagName) && el.tagName !== 'MJX-CONTAINER')) {
        var mc = el.closest('mjx-container');
        if (!mc) continue;
        for (var q = el.parentElement; q && q !== mc; q = q.parentElement) {   // what a box inside the formula hides
          if (!CLIP.test(cs(q).overflowX)) continue;
          var qr = q.getBoundingClientRect();
          over = Math.min(over, Math.max(Math.min(r.right, qr.right) - vw, -Math.max(r.left, qr.left)));
        }
        if (over <= TOL) continue;
        if (!viaparts.has(mc) || viaparts.get(mc).over < over)
          viaparts.set(mc, { over: over, aria: !!el.closest('mjx-assistive-mml') });
      } else past.set(el, over);
    }
    viaparts.forEach(function (v, mc) {
      if (past.has(mc)) return;                  // the formula sticks out itself, see below
      if (inside(mc, null, CLIP)) return;        // a part of a formula hidden by a box does not move the page
      past.set(mc, v.over);
      v.note = v.aria ? ', its MathML hidden for screen readers' : ', a part of it';
    });
    past.forEach(function (over, el) {
      var r = el.getBoundingClientRect(), note = '';
      if (past.has(el.parentElement) || inside(el, null, SCROLL) || !shown(el)) return;
      var mc = el.tagName === 'MJX-CONTAINER' ? el : (el.classList.contains('math') && el.querySelector('mjx-container'));
      var v = mc && viaparts.get(mc);
      if (v && v.note) note = v.note;            // the formula fits, a part of it does not
      else if (v && v.over > over + TOL) {       // the formula sticks out, and a part of it further
        over = v.over; note = v.aria ? ', with its MathML hidden for screen readers' : '';
      }
      var c = inside(el, null, CLIP);
      reported.add(el);
      if (c && !past.has(c)) {
        var ci = inner(c);
        out.push({ kind: 'cut', el: label(el), box: label(c), px: Math.ceil(Math.max(r.right - ci.right, ci.left - r.left)), at: where(el) });
      }
      else out.push({ kind: 'window', el: label(el) + note, px: Math.ceil(over), at: where(el) });
    });

    // out of its box: each target against the nearest box that holds it
    document.querySelectorAll(TARGETS).forEach(function (el) {
      for (var p = el; p; p = p.parentElement) if (reported.has(p)) return;   // one line per defect
      var r = rect(el), holder = el.parentElement && el.parentElement.closest(HOLDERS);
      if (!r || !holder || !shown(el)) return;
      if (inside(el, holder, SCROLL) || SCROLL.test(cs(holder).overflowX)) return;
      var hs = cs(holder), h = inner(holder);
      var sides = [['right', r.right - h.right], ['left', h.left - r.left], ['bottom', r.bottom - h.bottom], ['top', h.top - r.top]];
      sides.sort(function (a, b) { return b[1] - a[1]; });
      if (sides[0][1] <= TOL) return;
      var cut = /right|left/.test(sides[0][0]) ? CLIP.test(hs.overflowX) : CLIP.test(hs.overflowY);
      reported.add(el);
      out.push({ kind: cut ? 'cut' : 'box', el: label(el), box: label(holder), side: sides[0][0],
                 px: Math.ceil(sides[0][1]), at: where(el) });
    });

    // two sibling elements of a quiz that overlap; display: contents is looked through, as the grid of the
    // picture options does with its <li>
    function kids(el) {
      var o = [];
      for (var c of el.children) {
        if (c.namespaceURI !== HTMLNS || (/^MJX-/.test(c.tagName) && c.tagName !== 'MJX-CONTAINER')) continue;
        if (cs(c).display === 'contents') o = o.concat(kids(c)); else o.push(c);
      }
      return o;
    }
    function boxy(el) {
      var s = cs(el);
      if (s.display === 'none' || /^inline/.test(s.display) || s.visibility !== 'visible' ||
          s.position === 'absolute' || s.position === 'fixed') return null;
      var r = el.getBoundingClientRect();
      return (r.width < 1 || r.height < 1) ? null : r;
    }
    document.querySelectorAll('.quiz').forEach(function (q) {
      var stack = [q];
      while (stack.length) {
        var x = stack.pop(), ks = kids(x), rs = ks.map(boxy);
        for (var a = 0; a < ks.length; a++) for (var b = a + 1; b < ks.length; b++) {
          if (!rs[a] || !rs[b]) continue;
          var ox = Math.min(rs[a].right, rs[b].right) - Math.max(rs[a].left, rs[b].left);
          var oy = Math.min(rs[a].bottom, rs[b].bottom) - Math.max(rs[a].top, rs[b].top);
          if (ox > TOL + 0.5 && oy > TOL + 0.5)
            out.push({ kind: 'overlap', el: label(ks[a]), box: label(ks[b]), px: Math.ceil(Math.min(ox, oy)),
                       w: Math.ceil(ox), h: Math.ceil(oy), at: where(ks[a]) });
        }
        ks.forEach(function (k) { if (k.tagName !== 'MJX-CONTAINER') stack.push(k); });
      }
    });
  }

  async function run() {
    info.tex = document.querySelectorAll('span.math').length;
    info.mathjax = await until(function () {
      return window.MathJax && MathJax.startup && MathJax.startup.promise && MathJax.startup.document; }, 30000);
    if (info.mathjax) { try { await MathJax.startup.promise; } catch (e) { info.mathjax = false; } }
    var det = document.querySelectorAll('details');
    det.forEach(function (d) { d.open = true; });
    info.details = det.length;
    var qs = document.querySelectorAll('.quiz');
    info.quizzes = qs.length; info.clicked = 0;
    qs.forEach(function (q) { var b = q.querySelector('.quiz-opt'); if (b) { b.click(); info.clicked++; } });
    var fbs = Array.prototype.slice.call(document.querySelectorAll('.quiz-fb:not([hidden])'));
    info.feedbacks = fbs.length;
    var ws = document.querySelectorAll('.widget[data-widget]');
    info.widgets = ws.length; info.drawn = 0;
    for (let w of ws) {                         // a widget starts when it comes into view
      w.scrollIntoView();
      if (await until(function () { return w.querySelector('.widget-plots svg'); }, 10000)) info.drawn++;
    }
    window.scrollTo(0, 0);
    await settle(fbs);
    var imgs = Array.prototype.slice.call(document.images);
    info.images = imgs.length;
    var bad = imgs.map(function (im) { return (im.complete && !im.naturalWidth && !im.naturalHeight) ? im : null; });
    info.mjx = document.querySelectorAll('mjx-container').length;
    measure();
    bad.forEach(function (im) {
      if (im) info.findings.push({ kind: 'image', el: (im.getAttribute('src') || ''), px: 0, at: '' });
    });
  }
  run().catch(function (e) { info.error = String(e && e.stack || e); }).then(function () {
    parent.postMessage(JSON.stringify(info), '*');
  });
})();
</script>
""".replace('%(tol)s', str(TOL))

WRAPPER = """<!doctype html>
<html><head><meta charset="utf-8"><style>html, body {{ margin: 0; padding: 0; }}</style></head>
<body><iframe src="{copy}" style="display: block; border: 0; width: {w}px; height: {h}px"></iframe>
<pre id="layout-report"></pre>
<script>
window.addEventListener('message', function (e) {{
  if (typeof e.data === 'string' && e.data.indexOf('{{"layout"') === 0) document.getElementById('layout-report').textContent = e.data;
}});
</script>
</body></html>
"""


def file_url(path):
    """The file:// URL of a local path."""
    import pathlib
    return pathlib.Path(os.path.abspath(path)).as_uri()


def copy_of(text, folder):
    """The HTML of the page with a <base> to its own folder, images loaded at once, and the probe at the end."""
    base = '<base href="%s/">' % file_url(folder)
    text = re.sub(r'<head>', lambda m: m.group(0) + '\n' + base, text, count=1, flags=re.I)
    text = text.replace(' loading="lazy"', ' loading="eager"')
    i = text.lower().rfind('</body>')
    return (text[:i] + PROBE + text[i:]) if i >= 0 else text + PROBE


def measure(page, width):
    """Loads one page at one width and returns (report or None, reason when there is no report, number of runs)."""
    folder = os.path.dirname(os.path.abspath(page))
    tmp = tempfile.mkdtemp(prefix='.layout-', dir=folder)
    copy, frame = os.path.join(tmp, 'page.html'), os.path.join(tmp, f'frame-{width}.html')
    made = []
    try:
        with open(page, encoding='utf-8') as f:
            text = copy_of(f.read(), folder)
        for path, body in ((copy, text), (frame, WRAPPER.format(copy='page.html', w=width, h=WINDOW_H))):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(body)
            made.append(path)
        cmd = [CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--mute-audio',
               '--allow-file-access-from-files', f'--window-size={max(width, 500)},{WINDOW_H}',
               f'--virtual-time-budget={BUDGET_MS}', '--dump-dom', file_url(frame)]
        why = None
        for attempt in range(2):                # a second try, since a run of Chrome can end before the report
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
            except subprocess.TimeoutExpired:
                why = f'Chrome did not finish in {TIMEOUT_S} s'
                continue
            m = re.search(r'<pre id="layout-report">(.*?)</pre>', r.stdout, re.S)
            if m and m.group(1).strip():
                return json.loads(html.unescape(m.group(1))), None, attempt + 1
            why = 'no report came back (the page did not finish in the time budget of Chrome)'
        return None, why, 2
    finally:
        for path in made:
            os.remove(path)
        os.rmdir(tmp)


def message(f):
    """One finding as words."""
    k = f['kind']
    if k == 'page':
        return f'the page is wider than the window by {f["px"]} px (it scrolls sideways)'
    if k == 'window':
        return f'{f["el"]} sticks out of the window by {f["px"]} px'
    if k == 'cut':
        return f'{f["el"]} is cut by {f["box"]}, {f["px"]} px of it are hidden'
    if k == 'box':
        return f'{f["el"]} sticks out of its box {f["box"]} by {f["px"]} px on the {f["side"]}'
    if k == 'overlap':
        return f'in a quiz, {f["el"]} and {f["box"]} overlap by {f["w"]} x {f["h"]} px'
    if k == 'image':
        return f'the image {f["el"]} did not load'
    return json.dumps(f)


def problems(rep, width):
    """The reasons why a report does not measure what it should, as a list of strings."""
    out = []
    if rep.get('error'):
        out.append('the probe failed, ' + rep['error'].splitlines()[0])
    if rep.get('vw') != width:
        out.append(f'the window was {rep.get("vw")} px wide, not {width} px')
    if rep.get('tex') and (not rep.get('mathjax') or not rep.get('mjx')):
        out.append('MathJax did not load (no network?), so the math was not measured')
    return out


def pages_of(build, session, page):
    """The built pages to check: session N, or all sessions of the build, without the redirect stubs."""
    dirs = [os.path.join(build, f'session{session}')] if session else sorted(
        glob.glob(os.path.join(build, 'session*')), key=lambda d: int(re.sub(r'\D', '', os.path.basename(d)) or 0))
    out = []
    for d in dirs:
        if not os.path.isdir(d):
            sys.exit(f'{d} is not a folder of the build')
        if page:
            name = os.path.basename(page)
            name = name[:-3] + '.html' if name.endswith('.md') else name
            p = os.path.join(d, name)
            if not os.path.exists(p):
                sys.exit(f'--page: {name} is not a page of {d}')
            out.append(p)
            continue
        for p in sorted(glob.glob(os.path.join(d, '*.html'))):
            with open(p, encoding='utf-8') as f:
                if 'http-equiv="refresh"' not in f.read(2000):
                    out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('build', metavar='BUILD_DIR', help='folder of a private build, build.py --out BUILD_DIR')
    ap.add_argument('--session', type=int, help='check the pages of this session only (default: every session of the build)')
    ap.add_argument('--page', metavar='FILE', help='with --session: one page, by the name of its Markdown or HTML file')
    ap.add_argument('--width', type=int, nargs='+', default=[1000, 390], help='widths of the window in px (default 1000 390)')
    ap.add_argument('--jobs', type=int, default=4, help='Chrome runs at the same time (default 4)')
    ap.add_argument('-v', '--verbose', action='store_true', help='also print what was opened and counted on each page')
    a = ap.parse_args()
    if a.page and not a.session:
        sys.exit('--page needs --session N')
    build = os.path.abspath(a.build)
    pages = pages_of(build, a.session, a.page)
    tasks = [(p, w) for p in pages for w in a.width]
    with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
        results = list(ex.map(lambda t: measure(*t), tasks))
    nfind, nbad, tot = 0, 0, dict(images=0, quizzes=0, clicked=0, feedbacks=0, details=0, widgets=0, drawn=0)
    retries = sum(r[2] - 1 for r in results)
    for (p, w), (rep, why, _) in zip(tasks, results):
        rel = os.path.relpath(p, build)
        if rep is None:
            nbad += 1
            print(f'{rel} {w}px: not measured, {why}')
            continue
        for k in tot:
            tot[k] += rep.get(k, 0)
        for why in problems(rep, w):
            nbad += 1
            print(f'{rel} {w}px: not measured, {why}')
        for f in rep.get('findings', []):
            nfind += 1
            at = f' [{f["at"]}]' if f.get('at') else ''
            print(f'{rel} {w}px{at}: {message(f)}')
        if a.verbose:
            print(f'  {rel} {w}px: {rep.get("images")} images, {rep.get("mjx")} math, {rep.get("details")} details opened, '
                  f'{rep.get("clicked")} of {rep.get("quizzes")} quizzes clicked, {rep.get("feedbacks")} feedbacks open, '
                  f'{rep.get("drawn")} of {rep.get("widgets")} widgets drawn')
    print(f'layout: {len(pages)} pages at {" and ".join(f"{w} px" for w in a.width)}, {nfind} findings, '
          f'{nbad} not measured ({tot["images"]} images, {tot["details"]} details opened, '
          f'{tot["clicked"]} of {tot["quizzes"]} quizzes clicked, {tot["drawn"]} of {tot["widgets"]} widgets drawn, '
          f'{retries} runs of Chrome repeated)')
    sys.exit(1 if nfind or nbad else 0)


if __name__ == '__main__':
    main()
