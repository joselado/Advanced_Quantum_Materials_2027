"""Renders the web Markdown master in webnotes/pages/ to docs/notes/ and runs the checks.

    python3 webnotes/build.py [--session N] [--serve] [--check-only] [--math]

Two passes. The first reads every page of every converted session and writes labels.json, the map from
each anchor (section, numbered equation, figure) to the page that holds it. The second renders each page
with pandoc and filters/web.lua, which resolves the links with that map, also across sessions. The build is
idempotent, a file is written only when its content changes.
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


def collect_labels(mans):
    """First pass. Sections, figures and numbered equations of every page, as anchor -> page."""
    anchors, tags = {}, {}
    for n, m in mans.items():
        for p in m['pages']:
            r = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'json', md_path(n, p)], capture_output=True,
                               text=True, check=True)
            url = page_url(n, p)

            def visit(d):
                t = d.get('t')
                if t in ('Header', 'Figure'):
                    ident = d['c'][1][0] if t == 'Header' else d['c'][0][0]
                    if ident:
                        anchors[ident] = url
                elif t == 'Math' and d['c'][0]['t'] == 'DisplayMath':
                    for tag in re.findall(r'\\tag\{([^}]*)\}', d['c'][1]):
                        a = 'eq-' + tag.replace('.', '-')
                        if tags.get(a, 0):
                            print(f'error: the equation number {tag} is used twice (page {url})')
                            check.ERRORS.append(f'equation number {tag} used twice')
                        anchors[a] = url
                        tags[a] = tags.get(a, 0) + 1
            walk(json.loads(r.stdout), visit)
    return anchors


def figures_used(mans):
    names = set()
    for n, m in mans.items():
        for p in m['pages']:
            with open(md_path(n, p)) as f:
                names.update(re.findall(r'\]\(figures/([A-Za-z0-9_]+)\.svg', f.read()))
    return names


def convert_figures(names):
    os.makedirs(os.path.join(NOTES, 'figures'), exist_ok=True)
    done = 0
    for nm in sorted(names):
        pdf, svg = os.path.join(FIGPDF, nm + '.pdf'), os.path.join(NOTES, 'figures', nm + '.svg')
        if not os.path.exists(pdf):
            check.ERRORS.append(f'figure PDF missing: {nm}.pdf')
            continue
        if not os.path.exists(svg) or os.path.getmtime(svg) < os.path.getmtime(pdf):
            subprocess.run(['pdftocairo', '-svg', pdf, svg], check=True)
            done += 1
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


def build_session(n, m, sessions, built, labels_path):
    titles = {s['session']: s['title'] for s in sessions}
    pages = m['pages']
    intro = pages[0]
    sdir = os.path.join(NOTES, f'session{n}')
    head = intro['title']
    toc = '<nav class="toc"><ol>' + ''.join(
        f'<li><span class="n">{p["number"]}</span><a href="{p["file"][:-3]}.html">{title_html(p["title"])}</a></li>'
        for p in pages[1:]) + '</ol></nav>'
    links = (f'<p class="links"><a href="../../lectures/session{n}.html">Video lecture</a> · '
             f'<a href="../../landscape/session{n}.html">Landscape lecture</a> · '
             f'<a href="{T.REPO}/blob/main/jupyter-notebooks/session{n}.ipynb">session{n}.ipynb</a> · '
             f'<a href="{T.REPO}/blob/main/lecture_notes/main.pdf">PDF of the notes</a></p>\n')
    body = T.tabs(n, 2) + T.session_row(sessions, built, n, 2)
    body += f'  <h1>Session {n}. {title_html(head)}</h1>\n  {links}'
    body += render(n, intro, page_url(n, intro), labels_path, 'index')
    body += '\n  <h2>Contents</h2>\n  ' + toc + '\n'
    first = pages[1]
    body += f'  <nav class="pager"><a href="../index.html">Lecture notes</a><a href="{first["file"][:-3]}.html">{first["number"]} {title_html(first["title"])}</a></nav>\n'
    out = {os.path.join(sdir, 'index.html'): T.shell(f'Session {n}, lecture notes', body, 2)}
    for i, p in enumerate(pages[1:], start=1):
        url = page_url(n, p)
        prev = pages[i - 1]
        if i == 1:
            pv = f'<a href="index.html">Session {n}</a>'
        else:
            pv = f'<a href="{prev["file"][:-3]}.html">{prev["number"]} {title_html(prev["title"])}</a>'
        if i + 1 < len(pages):
            nx = pages[i + 1]
            nv = f'<a href="{nx["file"][:-3]}.html">{nx["number"]} {title_html(nx["title"])}</a>'
        elif n + 1 in built:
            nv = f'<a href="../session{n + 1}/index.html">Session {n + 1}. {esc_t(titles[n + 1])}</a>'
        else:
            nv = '<span></span>'
        b = T.tabs(n, 2) + T.session_row(sessions, built, n, 2)
        b += (f'  <p class="crumb"><a href="index.html">Session {n}. {title_html(head)}</a></p>\n')
        b += render(n, p, url, labels_path, 'section')
        b += f'\n  <nav class="pager">{pv}{nv}</nav>\n'
        out[os.path.join(NOTES, url)] = T.shell(f'{p["number"]} {re.sub(r"[$]", "", p["title"])}, session {n}', b, 2)
    return out


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
            b += '  <nav class="toc"><ol>' + ''.join(
                f'<li><span class="n">{p["number"]}</span><a href="session{n}/{p["file"][:-3]}.html">{title_html(p["title"])}</a></li>'
                for p in pages[1:]) + '</ol></nav>\n'
        else:
            b += f'  <h2 class="soon">Session {n}. {esc_t(s["title"])} <span class="note">(not on the page yet)</span></h2>\n'
    b += '  </div>\n'
    return T.shell('Lecture notes, Advanced Quantum Materials 2027', b, 1)


def build(only=None):
    pandoc_ok()
    sessions = json.load(open(os.path.join(DOCS, 'sessions.json')))
    mans = manifests()
    built = set(mans)
    anchors = collect_labels(mans)
    lab = os.path.join(HERE, 'labels.json')
    write(lab, json.dumps({'built': sorted(built), 'anchors': anchors}, indent=1, sort_keys=True) + '\n')
    nfig = convert_figures(figures_used(mans))
    written, outputs = 0, {}
    for n, m in mans.items():
        if only and n != only:
            continue
        outputs.update(build_session(n, m, sessions, built, lab))
    outputs[os.path.join(NOTES, 'index.html')] = course_index(sessions, mans)
    for path, text in outputs.items():
        written += write(path, text)
    write(os.path.join(NOTES, 'notes.js'), open(os.path.join(HERE, 'widgets', 'notes.js')).read())
    # a page of a built session that the manifest does not know is stale
    if not only:
        known = set(outputs)
        for n in mans:
            for f in glob.glob(os.path.join(NOTES, f'session{n}', '*.html')):
                if f not in known:
                    os.unlink(f)
                    print('removed stale page', os.path.relpath(f, DOCS))
    print(f'{len(outputs)} pages, {written} written, {nfig} figures converted, labels.json has {len(anchors)} anchors')


def mathcheck():
    """Runs mathcheck/check.js on docs/notes/. Skipped with a warning when node or its packages are missing."""
    d = os.path.join(HERE, 'mathcheck')
    if not shutil.which('node') or not os.path.isdir(os.path.join(d, 'node_modules', 'mathjax-full')):
        print('math check skipped: needs node and `npm install` in webnotes/mathcheck/')
        return True
    return subprocess.run(['node', os.path.join(d, 'check.js'), os.path.join(DOCS, 'notes')]).returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--session', type=int, help='build the pages of this session only')
    ap.add_argument('--serve', action='store_true', help='serve docs/ on localhost:8000 after the build')
    ap.add_argument('--check-only', action='store_true', help='run the checks on docs/notes/ without building')
    ap.add_argument('--math', action='store_true', help='also render every math fragment with MathJax (mathcheck/)')
    a = ap.parse_args()
    if not a.check_only:
        build(a.session)
    ok = check.run(DOCS, HERE)
    if a.math:
        ok = mathcheck() and ok
    if a.serve:
        print('serving docs/ at http://localhost:8000/notes/index.html')
        os.chdir(DOCS)
        subprocess.run([sys.executable, '-m', 'http.server', '8000'])
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
