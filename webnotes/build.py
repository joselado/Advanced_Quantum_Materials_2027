"""Renders the web Markdown master in webnotes/pages/ to docs/notes/ and runs the checks.

    python3 webnotes/build.py [--session N] [--out DIR] [--serve] [--check-only] [--math] [--freeze]

Two passes. The first reads every page of every converted session and writes labels.json, the map from
each anchor (section, numbered equation, figure) to the page that holds it. The second renders each page
with pandoc and filters/web.lua, which resolves the links with that map, also across sessions. The build is
idempotent, a file is written only when its content changes.

With --out DIR the pages, labels.json, the figures and notes.js are written in DIR instead of docs/notes/ and
webnotes/labels.json, and the checks run on DIR. Several people can build in parallel, each in a DIR of their own.
"""
import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys

import template as T
import check

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, 'docs')
NOTES = os.path.join(DOCS, 'notes')
FIGPDF = os.path.join(ROOT, 'lecture_notes', 'src', 'figures', 'pdf')
OVERLAYS = os.path.join(ROOT, 'lecture_notes', 'src', 'figures', 'overlays')
NOTEBOOKS = os.path.join(ROOT, 'jupyter-notebooks')
WEBFIG = os.path.join(HERE, 'figures')
LABELS = os.path.join(HERE, 'labels.json')
SITE = 'https://joselado.github.io/Advanced_Quantum_Materials_2027/notes/'
PRIVATE = False           # set by --out


def write(path, text):
    """Writes only when the content changes, so that a second build leaves git status as it was."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        with open(path) as f:
            if f.read() == text:
                return False
    with open(path, 'w') as f:
        f.write(text)
    return True


def pandoc_ok():
    out = subprocess.run(['pandoc', '--version'], capture_output=True, text=True).stdout
    m = re.search(r'pandoc (\d+)\.', out)
    if not m or int(m.group(1)) < 3:
        sys.exit('pandoc 3 or newer is needed')


def manifests():
    out = {}
    for p in sorted(glob.glob(os.path.join(HERE, 'manifest', 'session*.json'))):
        m = json.load(open(p))
        out[m['session']] = m
    return out


def page_url(n, p):
    """notes-relative URL of a page of the manifest."""
    if p['file'] == 'index.md':
        return f'session{n}/index.html'
    return f'session{n}/{p["file"][:-3]}.html'


def md_path(n, p):
    return os.path.join(HERE, 'pages', f'session{n:02d}', p['file'])


def walk(x, f):
    if isinstance(x, dict):
        f(x)
        for v in x.values():
            walk(v, f)
    elif isinstance(x, list):
        for v in x:
            walk(v, f)


def attrs(a):
    """[id, classes, [[k, v], ...]] of the pandoc JSON as (id, classes, dict)."""
    return a[0], a[1], dict(a[2])


def find_image(blocks):
    found = []

    def v(d):
        if d.get('t') == 'Image':
            found.append(d)
    walk(blocks, v)
    return found[0] if found else None


def notebook_cells(nb):
    """Plain text of the markdown cells of a notebook, for the check of the cell heading of a try-it box."""
    try:
        d = json.load(open(os.path.join(NOTEBOOKS, nb)))
    except (OSError, ValueError):
        return None
    return '\n'.join(''.join(c['source']) for c in d.get('cells', []) if c['cell_type'] == 'markdown').lower()


def collect_labels(mans):
    """First pass. Sections, figures and numbered equations of every page, as anchor -> page.

    It also numbers the web schematics ("Schematic 2.1", one counter per session), finds the figures that are
    shown again (a figure of the PDF notes without an id, whose id is that of its first display), and checks
    the manifest (ids of the pages, of the sections of a merged page) and the notebooks of the try-it boxes.
    Returns a dict with anchors, numbers, figsrc, webfigs (the files figures/web/...), pdffigs (names) and
    panels ((name, panel) pairs)."""
    anchors, tags = {}, {}
    numbers, figsrc, recycled = {}, {}, []
    webfigs, pdffigs, panels = set(), set(), set()
    nsch = {}
    cells = {}
    for n, m in mans.items():
        for p in m['pages']:
            r = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'json', md_path(n, p)], capture_output=True,
                               text=True, check=True)
            url = page_url(n, p)
            ast = json.loads(r.stdout)

            def visit(d):
                t = d.get('t')
                if t in ('Header', 'Figure'):
                    ident = d['c'][1][0] if t == 'Header' else d['c'][0][0]
                    if ident:
                        if t == 'Figure' and ident in anchors:
                            check.ERRORS.append(f'{url}: the figure id {ident} is already used')
                        anchors[ident] = url
                if t == 'Figure':
                    _, _, kv = attrs(d['c'][0])
                    img = find_image(d['c'][2])
                    if img is None:
                        return
                    src = img['c'][2][0]
                    iid, icls, ikv = attrs(img['c'][0])
                    ident = d['c'][0][0]
                    mm = re.match(r'figures/web/(session\d+/[A-Za-z0-9_]+)\.svg$', src)
                    if mm:
                        webfigs.add(src)
                        if not re.match(r'sch:s\d+:[A-Za-z0-9_]+$', ident):
                            check.ERRORS.append(f'{url}: the schematic {src} needs an id such as {{#sch:s{n:02d}:name}}')
                        else:
                            if int(ident.split(':')[1][1:]) != n:
                                check.ERRORS.append(f'{url}: the id {ident} is not of session {n}')
                            nsch[n] = nsch.get(n, 0) + 1
                            numbers[ident] = f'{n}.{nsch[n]}'
                        return
                    mm = re.match(r'figures/([A-Za-z0-9_]+)\.svg$', src)
                    if not mm:
                        return
                    name = mm.group(1)
                    pdffigs.add(name)
                    if ident:
                        figsrc[name] = ident
                        numbers.setdefault('~' + ident, ikv.get('number') or kv.get('number') or '')
                    else:
                        recycled.append((name, ikv.get('panel'), url))
                        if ikv.get('panel'):
                            panels.add((name, ikv['panel']))
                elif t == 'Div':
                    i, cl, kv = attrs(d['c'][0])
                    if 'tryit' in cl:
                        nb = kv.get('notebook', '')
                        if not nb or not os.path.exists(os.path.join(NOTEBOOKS, nb)):
                            check.ERRORS.append(f'{url}: try-it box with a missing notebook, "{nb}" is not in jupyter-notebooks/')
                        elif kv.get('cell'):
                            if nb not in cells:
                                cells[nb] = notebook_cells(nb)
                            if cells[nb] is None or kv['cell'].lower() not in cells[nb]:
                                check.ERRORS.append(f'{url}: the cell "{kv["cell"]}" is not a heading of {nb}')
                elif t == 'Math' and d['c'][0]['t'] == 'DisplayMath':
                    for tag in re.findall(r'\\tag\{([^}]*)\}', d['c'][1]):
                        a = 'eq-' + tag.replace('.', '-')
                        if tags.get(a, 0):
                            print(f'error: the equation number {tag} is used twice (page {url})')
                            check.ERRORS.append(f'equation number {tag} used twice')
                        anchors[a] = url
                        tags[a] = tags.get(a, 0) + 1
            walk(ast, visit)
    # the manifest: a page holds its own id and the ids of its other sections
    for n, m in mans.items():
        for p in m['pages'][1:]:
            url = page_url(n, p)
            for s in [p] + p.get('also', []):
                if anchors.get(s['id']) != url:
                    check.ERRORS.append(f'{url}: the manifest lists the section {s["id"]}, which is not a heading of the page')
    # the figures shown again need their first display
    need, nums = {}, {}
    for name, panel, url in recycled:
        if name not in figsrc:
            check.ERRORS.append(f'{url}: the figure {name} is shown again, but no page holds it with an id')
            continue
        need[name] = figsrc[name]
        nums[figsrc[name]] = numbers.get('~' + figsrc[name], '')
    for k in [k for k in numbers if k.startswith('~')]:
        del numbers[k]
    numbers.update(nums)
    return dict(anchors=anchors, numbers=numbers, figsrc=need, webfigs=webfigs, pdffigs=pdffigs, panels=panels)


def labels_json(built, info):
    d = {'built': sorted(built), 'anchors': info['anchors']}
    if info['numbers']:
        d['numbers'] = info['numbers']
    if info['figsrc']:
        d['figsrc'] = info['figsrc']
    return json.dumps(d, indent=1, sort_keys=True) + '\n'


def convert_figures(names):
    """pdftocairo of the PDF figures used. A private build copies the SVG of docs/notes/ when it is up to date."""
    os.makedirs(os.path.join(NOTES, 'figures'), exist_ok=True)
    done = 0
    for nm in sorted(names):
        pdf, svg = os.path.join(FIGPDF, nm + '.pdf'), os.path.join(NOTES, 'figures', nm + '.svg')
        if not os.path.exists(pdf):
            check.ERRORS.append(f'figure PDF missing: {nm}.pdf')
            continue
        if not os.path.exists(svg) or os.path.getmtime(svg) < os.path.getmtime(pdf):
            ref = os.path.join(DOCS, 'notes', 'figures', nm + '.svg')
            if PRIVATE and os.path.exists(ref) and os.path.getmtime(ref) >= os.path.getmtime(pdf):
                shutil.copyfile(ref, svg)
            else:
                subprocess.run(['pdftocairo', '-svg', pdf, svg], check=True)
            done += 1
    return done


def panel_suffixes(name):
    """Panels of a PDF figure in the order of the images in the SVG, from the overlay of the figure:
    s06f02_dimer gives ['a', 'b'], s09f05_decay gives ['chains', 'log']."""
    path = os.path.join(OVERLAYS, name + '.tex')
    if not os.path.exists(path):
        return []
    tex = open(path).read()
    files = re.findall(r'\{\.\./blender/out/([A-Za-z0-9_]+)\.(?:jpg|png)\}', tex)
    return [f[len(name) + 1:] if f.startswith(name + '_') else '' for f in files]


SVGNS = '{http://www.w3.org/2000/svg}'
XLINK = '{http://www.w3.org/1999/xlink}href'


def _box(d, m=(1, 0, 0, 1, 0, 0)):
    """Bounding box of the numbers of a path d (absolute commands, as pdftocairo writes them), moved by a matrix."""
    v = [float(x) for x in re.findall(r'-?\d+\.?\d*(?:e-?\d+)?', d)]
    xs, ys = v[0::2], v[1::2]
    if not xs or not ys:
        return None
    a, dd, e, f = m[0], m[3], m[4], m[5]
    return (a * min(xs) + e, dd * min(ys) + f, a * max(xs) + e, dd * max(ys) + f)


def _matrix(el):
    t = el.get('transform') or ''
    mm = re.match(r'matrix\(([^)]*)\)', t)
    return tuple(float(x) for x in mm.group(1).split(',')) if mm else (1, 0, 0, 1, 0, 0)


def crop_panel(svg_text, index):
    """The SVG of the whole figure cut to the window of its image number index, as (svg text, window width, width).

    pdftocairo writes each embedded render as one <image> in <defs> and one <use> of it with a matrix, and
    it writes the labels (glyph outlines) and the strokes in the order of the TikZ file, which draws a panel as
    its image first and its labels after. So everything between the image k and the image k+1 belongs to
    panel k. The new file keeps the elements of this panel only, with a window that is the box around them,
    which is the render and the labels around it. The weight of the file is that of one panel."""
    import xml.etree.ElementTree as ET
    ET.register_namespace('', SVGNS[1:-1])
    ET.register_namespace('xlink', XLINK[1:XLINK.index('}')])
    root = ET.fromstring(svg_text)
    W, H = float(root.get('width')), float(root.get('height'))
    defs = root.find(SVGNS + 'defs')
    images = {i.get('id'): (float(i.get('width')), float(i.get('height'))) for i in defs.iter(SVGNS + 'image')}
    glyph = {}
    for g in defs.iter(SVGNS + 'g'):
        if g.get('id', '').startswith('glyph-'):
            p = g.find(SVGNS + 'path')
            if p is not None and p.get('d'):
                glyph[g.get('id')] = _box(p.get('d'))
    owner, k = None, -1
    items = []                       # (element, panel or None, boxes)
    sources = []
    for el in list(root):
        if el is defs or el.tag == SVGNS + 'defs':
            continue
        boxes = []
        for u in el.iter():
            h = (u.get(XLINK) or '')[1:]
            if u.tag == SVGNS + 'use' and h in images:
                k += 1
                sources.append(h)
                w, hh = images[h]
                m = _matrix(u)
                boxes.append((m[4], m[5], m[4] + m[0] * w, m[5] + m[3] * hh))
                owner = k
            elif u.tag == SVGNS + 'use' and h in glyph and glyph[h]:
                g = glyph[h]
                x, y = float(u.get('x', 0)), float(u.get('y', 0))
                boxes.append((x + g[0], y + g[1], x + g[2], y + g[3]))
            elif u.tag == SVGNS + 'path' and u.get('d') and el.tag != SVGNS + 'clipPath':
                bb = _box(u.get('d'), _matrix(u))
                if bb:
                    boxes.append(bb)
        items.append((el, owner, boxes))
    if index >= len(sources):
        raise ValueError('the figure has fewer panels')
    x0, y0, x1, y1 = W, H, 0.0, 0.0
    for el, ow, boxes in items:
        if ow != index:
            root.remove(el)
            continue
        for b in boxes:
            x0, y0, x1, y1 = min(x0, b[0]), min(y0, b[1]), max(x1, b[2]), max(y1, b[3])
    for sid in (s for i, s in enumerate(sources) if i != index):
        for im in list(defs):
            if im.get('id') == sid:
                defs.remove(im)
    pad = 3.0
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
    scale = 860.0 / W                              # the width in px of the whole figure on a page
    root.set('width', '%.2f' % ((x1 - x0) * scale))
    root.set('height', '%.2f' % ((y1 - y0) * scale))
    root.set('viewBox', '%.2f %.2f %.2f %.2f' % (x0, y0, x1 - x0, y1 - y0))
    return ET.tostring(root, encoding='unicode', xml_declaration=False) + '\n', x1 - x0, W


def make_panels(panels):
    """Writes figures/panel/NAME_PANEL.svg for every (name, panel) used. Returns the number written."""
    done = 0
    for name, panel in sorted(panels):
        sfx = panel_suffixes(name)
        if panel not in sfx:
            check.ERRORS.append(f'figure {name} has no panel "{panel}", the panels are {", ".join(sfx) or "none (one image)"}')
            continue
        src = os.path.join(NOTES, 'figures', name + '.svg')
        if not os.path.exists(src):
            continue
        out, _, _ = crop_panel(open(src).read(), sfx.index(panel))
        out = '<?xml version="1.0" encoding="UTF-8"?>\n' + out
        done += write(os.path.join(NOTES, 'figures', 'panel', f'{name}_{panel}.svg'), out)
    return done


def build_web_figures(webfigs):
    """Runs the stale scripts webnotes/figures/sessionNN/NAME.py and copies NAME.svg to figures/web/. A script is
    stale when its SVG is missing or older than the script or than figures/style.py."""
    done = 0
    style = os.path.join(WEBFIG, 'style.py')
    for src in sorted(webfigs):
        rel = src[len('figures/web/'):]
        py, svg = os.path.join(WEBFIG, rel[:-4] + '.py'), os.path.join(WEBFIG, rel)
        if os.path.exists(py):
            if not os.path.exists(svg) or os.path.getmtime(svg) < max(os.path.getmtime(py), os.path.getmtime(style)):
                r = subprocess.run([sys.executable, os.path.basename(py)], cwd=os.path.dirname(py),
                                   capture_output=True, text=True)
                if r.returncode:
                    check.ERRORS.append(f'schematic script {rel[:-4]}.py failed: {r.stderr.strip().splitlines()[-1:]}')
                    continue
                done += 1
        if not os.path.exists(svg):
            check.ERRORS.append(f'schematic {rel} has no script and no SVG in webnotes/figures/')
            continue
        write(os.path.join(NOTES, 'figures', 'web', rel), open(svg).read())
    return done


def render(n, p, url, labels_path, kind):
    r = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html5', '--mathjax', '--wrap=none', '--lua-filter',
                        os.path.join(HERE, 'filters', 'web.lua'), '-M', f'labels={labels_path}',
                        '-M', f'page={url}', '-M', f'kind={kind}', md_path(n, p)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'pandoc failed on {md_path(n, p)}: {r.stderr[:1500]}')
    for line in r.stderr.splitlines():
        if line.startswith('PENDING'):
            check.PENDING.add(line.split()[1])
        elif line.strip():
            check.ERRORS.append(f'{url}: {line.strip()}')
    return r.stdout


def title_html(t):
    """A title of the manifest as HTML. Inline math is passed to MathJax."""
    return re.sub(r'\$([^$]+)\$', lambda m: '\\(' + m.group(1) + '\\)', html.escape(t, quote=False))


def toc(pages, prefix=''):
    """The list of the pages of a session. A merged page lists its other sections, with the anchor of each."""
    rows = []
    for p in pages[1:]:
        href = f'{prefix}{p["file"][:-3]}.html'
        rows.append(f'<li><span class="n">{p["number"]}</span><a href="{href}">{title_html(p["title"])}</a></li>')
        for x in p.get('also', []):
            rows.append(f'<li class="also"><span class="n">{x["number"]}</span>'
                        f'<a href="{href}#{x["id"]}">{title_html(x["title"])}</a></li>')
    return '<nav class="toc"><ol>' + ''.join(rows) + '</ol></nav>'


def pager_link(p):
    return f'<a href="{p["file"][:-3]}.html">{p["number"]} {title_html(p["title"])}</a>'


def build_session(n, m, sessions, built, labels_path):
    titles = {s['session']: s['title'] for s in sessions}
    pages = m['pages']
    intro = pages[0]
    sdir = os.path.join(NOTES, f'session{n}')
    head = intro['title']
    links = (f'<p class="links"><a href="../../lectures/session{n}.html">Video lecture</a> · '
             f'<a href="../../landscape/session{n}.html">Landscape lecture</a> · '
             f'<a href="{T.REPO}/blob/main/jupyter-notebooks/session{n}.ipynb">session{n}.ipynb</a> · '
             f'<a href="{T.REPO}/blob/main/lecture_notes/main.pdf">PDF of the notes</a></p>\n')
    body = T.tabs(n, 2) + T.session_row(sessions, built, n, 2)
    body += f'  <h1>Session {n}. {title_html(head)}</h1>\n  {links}'
    body += render(n, intro, page_url(n, intro), labels_path, 'index')
    body += '\n  <h2>Contents</h2>\n  ' + toc(pages) + '\n'
    first = pages[1]
    body += f'  <nav class="pager"><a href="../index.html">Lecture notes</a>{pager_link(first)}</nav>\n'
    out = {os.path.join(sdir, 'index.html'): T.shell(f'Session {n}, lecture notes', body, 2)}
    for i, p in enumerate(pages[1:], start=1):
        url = page_url(n, p)
        prev = pages[i - 1]
        pv = f'<a href="index.html">Session {n}</a>' if i == 1 else pager_link(prev)
        if i + 1 < len(pages):
            nv = pager_link(pages[i + 1])
        elif n + 1 in built:
            nv = f'<a href="../session{n + 1}/index.html">Session {n + 1}. {esc_t(titles[n + 1])}</a>'
        else:
            nv = '<span></span>'
        b = T.tabs(n, 2) + T.session_row(sessions, built, n, 2)
        b += (f'  <p class="crumb"><a href="index.html">Session {n}. {title_html(head)}</a></p>\n')
        b += render(n, p, url, labels_path, 'section')
        b += f'\n  <nav class="pager">{pv}{nv}</nav>\n'
        out[os.path.join(NOTES, url)] = T.shell(f'{p["number"]} {re.sub(r"[$]", "", p["title"])}, session {n}', b, 2)
    for r in m.get('redirects', []):
        out[os.path.join(sdir, r['from'])] = redirect_stub(n, r, pages)
    return out


def redirect_stub(n, r, pages):
    """The page that stands at a retired URL. It has a meta refresh, a canonical link to the new page, and the
    link as text for a browser that does not refresh."""
    to = r['to']
    page = to.split('#')[0]
    title = next((p['title'] for p in pages if p['file'][:-3] + '.html' == page), page)
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Moved</title>\n'
            f'<link rel="canonical" href="{SITE}session{n}/{to}">\n'
            f'<meta http-equiv="refresh" content="0; url={to}">\n<meta name="robots" content="noindex">\n</head>\n'
            f'<body>\n<p>This page has moved to <a href="{to}">{esc_t(re.sub(r"[$]", "", title))}</a>.</p>\n</body>\n</html>\n')


def esc_t(s):
    return html.escape(s, quote=False)


def course_index(sessions, mans):
    b = '  <nav class="tabs"><a class="on" href="index.html">Lecture notes</a></nav>\n'
    b += '  <h1>Lecture notes</h1>\n'
    b += ('  <p>The lecture notes of the course, one page per section, with the equations numbered as in the PDF '
          'of the notes. A session whose notes are not on the page yet is listed without a link.</p>\n')
    b += '  <div class="coursecontents">\n'
    for s in sessions:
        n = s['session']
        if n in mans:
            pages = mans[n]['pages']
            b += f'  <h2><a href="session{n}/index.html">Session {n}. {esc_t(s["title"])}</a></h2>\n'
            b += '  ' + toc(pages, f'session{n}/') + '\n'
        else:
            b += f'  <h2 class="soon">Session {n}. {esc_t(s["title"])} <span class="note">(not on the page yet)</span></h2>\n'
    b += '  </div>\n'
    return T.shell('Lecture notes, Advanced Quantum Materials 2027', b, 1)


def copy_widgets(outputs):
    """For every widget the pages use (data-widget="ID"), checks that widgets/defs/ID.py and widgets/data/ID.json exist
    and match, and copies both to notes/widgets/. The JSON is made by widgets/precompute.py."""
    import hashlib
    ids = sorted({m for t in outputs.values() for m in re.findall(r'data-widget="([^"]+)"', t)})
    for wid in ids:
        py = os.path.join(HERE, 'widgets', 'defs', wid + '.py')
        js = os.path.join(HERE, 'widgets', 'data', wid + '.json')
        if not os.path.exists(py) or not os.path.exists(js):
            check.ERRORS.append(f'widget {wid}: needs widgets/defs/{wid}.py and widgets/data/{wid}.json (run widgets/precompute.py {wid})')
            continue
        sha = hashlib.sha1(open(py, 'rb').read()).hexdigest()[:12]
        if json.load(open(js))['meta'].get('sha') != sha:
            check.ERRORS.append(f'widget {wid}: widgets/defs/{wid}.py changed after its JSON, run widgets/precompute.py {wid}')
        write(os.path.join(NOTES, 'widgets', wid + '.py'), open(py).read())
        write(os.path.join(NOTES, 'widgets', wid + '.json'), open(js).read())


def build(only=None):
    pandoc_ok()
    sessions = json.load(open(os.path.join(DOCS, 'sessions.json')))
    mans = manifests()
    built = set(mans)
    info = collect_labels(mans)
    write(LABELS, labels_json(built, info))
    nfig = convert_figures(info['pdffigs'])
    nfig += make_panels(info['panels'])
    nweb = build_web_figures(info['webfigs'])
    written, outputs = 0, {}
    for n, m in mans.items():
        if only and n != only:
            continue
        outputs.update(build_session(n, m, sessions, built, LABELS))
    outputs[os.path.join(NOTES, 'index.html')] = course_index(sessions, mans)
    for path, text in outputs.items():
        written += write(path, text)
    write(os.path.join(NOTES, 'notes.js'), open(os.path.join(HERE, 'widgets', 'notes.js')).read())
    if any(T.CSS_LINK in t for t in outputs.values()):
        write(os.path.join(NOTES, 'notes.css'), open(os.path.join(HERE, 'widgets', 'notes.css')).read())
    copy_widgets(outputs)
    # a page of a built session that the manifest does not know is stale
    if not only:
        known = set(outputs)
        for n in mans:
            for f in glob.glob(os.path.join(NOTES, f'session{n}', '*.html')):
                if f not in known:
                    os.unlink(f)
                    print('removed stale page', os.path.relpath(f, NOTES))
    print(f'{len(outputs)} pages, {written} written, {nfig} figures converted, {nweb} schematics run, '
          f'labels.json has {len(info["anchors"])} anchors')


def frozen_urls(mans):
    """Every URL of the notes today, relative to notes/: index.html, sessionN/index.html and the pages."""
    urls = {'index.html'}
    for n, m in mans.items():
        urls.update(page_url(n, p) for p in m['pages'])
    return urls


def freeze():
    """Adds the URLs of today to manifest/frozen_urls.txt. The list only grows, check.py needs each one to stay."""
    path = os.path.join(HERE, 'manifest', 'frozen_urls.txt')
    old = set(open(path).read().split()) if os.path.exists(path) else set()
    new = old | frozen_urls(manifests())
    write(path, ''.join(u + '\n' for u in sorted(new)))
    print(f'frozen_urls.txt has {len(new)} URLs, {len(new - old)} added')


def mathcheck():
    """Runs mathcheck/check.js on the notes folder. Skipped with a warning when node or its packages are missing."""
    d = os.path.join(HERE, 'mathcheck')
    if not shutil.which('node') or not os.path.isdir(os.path.join(d, 'node_modules', 'mathjax-full')):
        print('math check skipped: needs node and `npm install` in webnotes/mathcheck/')
        return True
    return subprocess.run(['node', os.path.join(d, 'check.js'), NOTES]).returncode == 0


def main():
    global NOTES, LABELS, PRIVATE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--session', type=int, help='build the pages of this session only')
    ap.add_argument('--out', metavar='DIR', help='private build: write everything in DIR instead of docs/notes/ '
                    'and webnotes/labels.json, and check DIR')
    ap.add_argument('--serve', action='store_true', help='serve docs/ (or DIR) on localhost:8000 after the build')
    ap.add_argument('--check-only', action='store_true', help='run the checks on the existing build without building')
    ap.add_argument('--math', action='store_true', help='also render every math fragment with MathJax (mathcheck/)')
    ap.add_argument('--freeze', action='store_true', help='add the URLs of today to manifest/frozen_urls.txt and stop')
    a = ap.parse_args()
    if a.freeze:
        freeze()
        return
    if a.out:
        NOTES = os.path.abspath(a.out)
        LABELS = os.path.join(NOTES, 'labels.json')
        PRIVATE = True
        T.PRIVATE = True
    if not a.check_only:
        build(a.session)
    skip = set(range(1, 100)) - {a.session} if (a.out and a.session) else set()
    ok = check.run(DOCS, HERE, notes=NOTES, skip_sessions=skip)
    if a.math:
        ok = mathcheck() and ok
    if a.serve:
        root = NOTES if a.out else DOCS
        print(f'serving {root} at http://localhost:8000/' + ('index.html' if a.out else 'notes/index.html'))
        os.chdir(root)
        subprocess.run([sys.executable, '-m', 'http.server', '8000'])
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
