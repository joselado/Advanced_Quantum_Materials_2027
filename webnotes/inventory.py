"""The inventory of a session of the web notes, and the skeleton of its plan.

    python3 webnotes/inventory.py --session N            # a table of the pages, printed
    python3 webnotes/inventory.py --session N --plan     # also writes webnotes/plans/sessionNN.md, if it is not there

The pages come from the manifest, so a section that lives in the file of another section is listed with its file,
and nobody writes a page list from memory. For each page the table gives its sections, its size, the numbered
equations, the blocks that it already has, the figures with and without a pyqula script, and the hits of the lint.
The plan is one block per page with the fields that the author fills before any page is written: the question of
the page, its main result, the equation that it starts from, the fold, the lab source, the problem, the picture
question and the figures. The candidates for the lab boxes are the "In the lab" cells of the notebook of the
session, which are listed at the end of the plan. It only reads the pages, and it never overwrites a plan.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint  # noqa: E402

NOTEBOOKS = os.path.join(os.path.dirname(HERE), 'jupyter-notebooks')
BLOCKS = [('key', r'^:::+\s*key\b'), ('recall', r'^:::+\s*\{\.recall'), ('steps', r'^:::+\s*\{\.steps'),
          ('lab', r'^:::+\s*(?:lab\b|\{\.lab)'), ('problem', r'^:::+\s*problem\b'), ('quiz', r'^:::+\s*quiz\b'),
          ('tryit', r'^:::+\s*\{\.tryit'), ('widget', r'^:::+\s*\{\.widget')]


def pages(n):
    """The pages of a session from its manifest, each with its file and its sections."""
    m = json.load(open(os.path.join(HERE, 'manifest', f'session{n:02d}.json')))
    out = []
    for p in m['pages']:
        secs = [p] + p.get('also', [])
        out.append(dict(file=p['file'], sections=[(s.get('number', ''), s.get('title', '')) for s in secs]))
    return out


def measure(n, page):
    path = os.path.join(HERE, 'pages', f'session{n:02d}', page['file'])
    text = open(path, encoding='utf-8').read()
    d = dict(page, path=path, words=len(text.split()), tags=re.findall(r'\\tag\{([^}]*)\}', text))
    for name, pat in BLOCKS:
        d[name] = len(re.findall(pat, text, re.M))
    figs = re.findall(r'!\[[^\]]*\]\((figures/[^)]+)\)(\{[^}]*\})?', text, re.S)
    d['figures'] = len(figs)
    d['scripts'] = sum('script="' in (a or '') for _, a in figs)
    d['pictures'] = len(re.findall(r'^- \[[ xX]\] !\[', text, re.M))
    d['hits'] = Counter(c for c, _, _ in lint.lint_page(path) if c not in lint.WARNINGS)
    return d


def lab_candidates(n):
    """The statements and links of the "In the lab" cells of the notebook of the session."""
    path = os.path.join(NOTEBOOKS, f'session{n}.ipynb')
    if not os.path.exists(path):
        return None
    out = []
    for c in json.load(open(path)).get('cells', []):
        s = ''.join(c.get('source', []))
        if c.get('cell_type') == 'markdown' and re.search(r'^#+\s*In the lab', s, re.M | re.I):
            body = re.sub(r'^#+\s*In the lab\s*', '', s, flags=re.M | re.I).strip()
            out.append(' '.join(l.strip('- ').strip() for l in body.splitlines() if l.strip()))
    return out


def table(n, rows):
    lines = [f'| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | '
             f'figures (with script) | lint hits |', '|' + '---|' * 13]
    for d in rows:
        secs = ', '.join(num for num, _ in d['sections'] if num) or 'intro'
        hits = ', '.join(f'{c} {k}' for c, k in sorted(d['hits'].items())) or '0'
        lines.append(f"| `{d['file']}` | {secs} | {d['words']} | {len(d['tags'])} | {d['key']} | {d['recall']} | "
                     f"{d['steps']} | {d['lab']} | {d['problem']} | {d['quiz']} | {d['pictures']} | "
                     f"{d['figures']} ({d['scripts']}) | {hits} |")
    return '\n'.join(lines)


def plan(n, rows):
    out = [f'# Plan of Session {n} of the web notes', '',
           'This plan is filled before any page is written, and the lecturer can change it. One block per page. A',
           'field that does not apply says "none" with the reason. The rules are in',
           '`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in',
           f'`webnotes/conventions/session{n:02d}.md`.', '', '## The pages today', '', table(n, rows), '']
    for d in rows:
        if d['file'] == 'index.md':
            continue
        title = ' and '.join(f'{num} {t}'.strip() for num, t in d['sections'])
        out += [f'## {title}', '', f"File `{d['file']}`, {d['words']} words, numbered equations "
                f"{', '.join('(' + t + ')' for t in d['tags']) or 'none'}.", '',
                '- Question of the page, and where we arrive:',
                '- Main result for the key box:',
                '- Equation of another page that it starts from, for the recall box:',
                '- Derivation told in words, for a steps fold:',
                '- Lab box, with the source and the number that the source states:',
                '- Pen-and-paper problem:',
                '- Quizzes to rewrite, and a picture question or equations as options:',
                '- Figures to add, each with its pyqula script or the reason for numpy:',
                '- Old figures of the page that break the plot rules:', '']
    cands = lab_candidates(n)
    out += ['## Candidates for the lab boxes', '']
    if cands is None:
        out += ['The session has no notebook.', '']
    elif not cands:
        out += ['The notebook of the session has no "In the lab" cell.', '']
    else:
        out += ['These are the "In the lab" cells of the notebook, the first sources to use. Each one is fetched and',
                'stored with `webnotes/labsource.py` before a box quotes it.', ''] + [f'- {c}' for c in cands] + ['']
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--session', type=int, required=True)
    ap.add_argument('--plan', action='store_true', help='write webnotes/plans/sessionNN.md if it does not exist')
    a = ap.parse_args()
    rows = [measure(a.session, p) for p in pages(a.session)]
    print(table(a.session, rows))
    total = Counter()
    for d in rows:
        total.update(d['hits'])
    print(f"\n{len(rows)} files, {sum(d['words'] for d in rows)} words, {sum(d['quiz'] for d in rows)} quizzes, "
          f"lint hits: {', '.join(f'{c} {k}' for c, k in sorted(total.items())) or 'none'}")
    if a.plan:
        path = os.path.join(HERE, 'plans', f'session{a.session:02d}.md')
        if os.path.exists(path):
            print(f'the plan {os.path.relpath(path)} exists and is not overwritten')
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(plan(a.session, rows))
            print(f'wrote {os.path.relpath(path)}')


if __name__ == '__main__':
    main()
