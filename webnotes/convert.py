"""One-time conversion of the LaTeX of one session to the web Markdown master.

    python3 webnotes/convert.py --session N [--force]

Writes webnotes/pages/sessionNN/index.md (the introduction of the chapter) and one KK-slug.md per
section, the frozen list of pages in webnotes/manifest/sessionNN.json and the line of the session in
webnotes/SYNC. It refuses to overwrite a session that was converted, since from the conversion on the
Markdown is the master and may carry edits that exist only on the web. --force regenerates and loses them.
"""
import argparse
import json
import os
import unicodedata
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'lecture_notes', 'src')
NSESSIONS = 10


def pandoc_version():
    out = subprocess.run(['pandoc', '--version'], capture_output=True, text=True, check=True).stdout
    return tuple(int(x) for x in re.search(r'pandoc (\d+)\.(\d+)', out).groups())


def session_tex(n):
    return os.path.join(SRC, 'sessions', f'session{n:02d}.tex')


def counts():
    """Numbered equations and sections of each session, counted in the .tex in the order of the file."""
    eq, sec = [], []
    for n in range(1, NSESSIONS + 1):
        with open(session_tex(n)) as f:
            t = f.read()
        eq.append(len(re.findall(r'\\begin\{equation\}', t)))
        sec.append(len(re.findall(r'^\\section\{', t, re.M)))
    return eq, sec


def figure_numbers():
    """Label to number of every figure of the ten sessions, in the order of the file: the figure 3 of session 6 is 6.3."""
    out = []
    for n in range(1, NSESSIONS + 1):
        with open(session_tex(n)) as f:
            t = f.read()
        # the figures live in their own files, read where the session inputs them
        t = re.sub(r'\\input\{(figures/[^}]*)\}', lambda m: open(os.path.join(SRC, m.group(1) + '.tex')).read(), t)
        for k, m in enumerate(re.finditer(r'\\begin\{aqmfigure\}\{([^}]*)\}', t), 1):
            out.append(f'{m.group(1)}={n}.{k}')
    return out


def slugify(title):
    t = re.sub(r'\$[^$]*\$', ' ', title)
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r"[^a-z0-9\s-]", '', t)
    return re.sub(r'[\s-]+', '-', t).strip('-')


def to_markdown(blocks, meta, api):
    doc = {'pandoc-api-version': api, 'meta': meta, 'blocks': blocks}
    r = subprocess.run(['pandoc', '-f', 'json', '-t', 'markdown', '--wrap=none'], input=json.dumps(doc),
                       capture_output=True, text=True, check=True)
    return r.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--session', type=int, required=True)
    ap.add_argument('--force', action='store_true', help='overwrite a converted session, losing its web edits')
    a = ap.parse_args()
    n = a.session
    if pandoc_version() < (3, 0):
        sys.exit('pandoc 3 or newer is needed')
    pdir = os.path.join(HERE, 'pages', f'session{n:02d}')
    mpath = os.path.join(HERE, 'manifest', f'session{n:02d}.json')
    if (os.path.exists(pdir) and os.listdir(pdir)) or os.path.exists(mpath):
        if not a.force:
            sys.exit(f'session {n} is already converted ({os.path.relpath(pdir, ROOT)}). The Markdown is the master '
                     'and may hold web edits. Use --force to regenerate it and lose them.')
    eq, sec = counts()
    wrap = ('\\documentclass{report}\n\\input{preamble}\n\\input{figures_preamble}\n\\begin{document}\n'
            f'\\input{{sessions/session{n:02d}}}\n\\end{{document}}\n')
    r = subprocess.run(['pandoc', '--resource-path=' + SRC, '-f', 'latex', '-t', 'json', '--wrap=none',
                        '--lua-filter', os.path.join(HERE, 'filters', 'tex2md.lua'),
                        '-M', f'chapter={n}', '-M', 'eqmax=' + ','.join(map(str, eq)),
                        '-M', 'secmax=' + ','.join(map(str, sec)),
                        '-M', 'figmap=' + ';'.join(figure_numbers())],
                       input=wrap, capture_output=True, text=True, cwd=SRC)
    if r.returncode:
        sys.exit('pandoc failed: ' + r.stderr[:2000])
    print(r.stderr.strip())
    doc = json.loads(r.stdout)
    api, meta = doc['pandoc-api-version'], {}
    groups, cur = [], []
    for b in doc['blocks']:
        if b['t'] == 'Header' and b['c'][0] == 2:
            groups.append(cur)
            cur = []
        cur.append(b)
    groups.append(cur)
    os.makedirs(pdir, exist_ok=True)
    for old in os.listdir(pdir):  # a forced run leaves no page of an earlier slug behind
        if old.endswith('.md'):
            os.remove(os.path.join(pdir, old))
    os.makedirs(os.path.dirname(mpath), exist_ok=True)
    pages = []
    for i, g in enumerate(groups):
        md = to_markdown(g, meta, api)
        head = re.match(r'#+ (.*?) \{#([^ }]+)(?: number="([^"]*)")?\}', md)
        title, ident, number = head.group(1), head.group(2), head.group(3) or ''
        if i == 0:
            fname = 'index.md'
        else:
            fname = f'{int(number.split(".")[1]):02d}-{slugify(title)}.md'
        with open(os.path.join(pdir, fname), 'w') as f:
            f.write(md)
        pages.append({'file': fname, 'id': ident, 'number': number, 'title': title})
    with open(mpath, 'w') as f:
        json.dump({'session': n, 'pages': pages}, f, indent=1, ensure_ascii=False)
        f.write('\n')
    commit = subprocess.run(['git', 'log', '-1', '--format=%h', '--', 'lecture_notes/src'], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git', 'status', '--porcelain', '--', 'lecture_notes/src'], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        print('warning: lecture_notes/src has uncommitted changes, so SYNC records', commit, 'only approximately')
    sync = os.path.join(HERE, 'SYNC')
    lines = {}
    if os.path.exists(sync):
        for ln in open(sync).read().splitlines():
            if ln.strip():
                k, v = ln.split(None, 1)
                lines[k] = v
    lines[f'session{n:02d}'] = commit
    with open(sync, 'w') as f:
        for k in sorted(lines):
            f.write(f'{k} {lines[k]}\n')
    print(f'session {n}: {len(pages) - 1} sections and the introduction written to {os.path.relpath(pdir, ROOT)}')


if __name__ == '__main__':
    main()
