"""Checks of docs/notes/. Used by build.py, and alone with python3 webnotes/check.py.

Errors: a link to a file or an anchor that does not exist, an image that does not exist, "??", a LaTeX
command left in the text outside the math, an equation number used twice, a page in docs/notes/sessionN/ that
the manifest does not list, a link that the filter could not resolve, an image without alt text, a retired URL
(listed in manifest/frozen_urls.txt) that has neither a page nor a redirect, a redirect that points to a page or
an anchor that does not exist, a quiz with feedback that has not exactly 3 options or no correct option.
A figure inside a quiz is checked like any other (it exists, it has alt text). An SVG over 200 kB is a warning.
A quiz in the old form (no feedback per option) is only counted. External links (http) are not fetched.
Pending: references to a session that is not converted yet. They stay as text and are listed, not an error.
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urldefrag

ERRORS = []
WARNINGS = []
BIG_SVG = 200 * 1024   # an SVG over this size is a warning, a figure in a quiz should be light
PENDING = set()
OLD_QUIZZES = [0, 0]   # quizzes without feedback per option, and of them those that do not have 3 options


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.imgs, self.alts, self.text = set(), [], [], [], []
        self.math = 0          # depth inside a span of class math or inside mjx-container
        self.stack = []
        self.qimgs = []        # images inside a quiz (question or feedback)
        self.skip = 0
        self.quizzes = []      # per quiz: [options, marked correct, has feedback]
        self.inq = None        # the quiz being read
        self.optdepth = None   # stack depth of the div of the options

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get('class') or '').split()
        if tag == 'div' and 'quiz' in cls:
            self.inq = [0, 1 if a.get('data-correct') else 0, 'data-fb' in a, len(self.stack)]
            self.quizzes.append(self.inq)
        if tag == 'div' and 'quiz-options' in cls and self.inq is not None:
            self.optdepth = len(self.stack)
        if tag == 'li' and self.optdepth is not None and not any(t == 'li' for t, _, _ in self.stack[self.optdepth:]):
            self.inq[0] += 1
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a' and 'href' in a:
            self.hrefs.append(a['href'])
        if tag == 'img' and 'src' in a:
            self.imgs.append(a['src'])
            if self.inq is not None:
                self.qimgs.append(a['src'])
            if not (a.get('alt') or '').strip():
                self.alts.append(a['src'])
        ismath = tag == 'span' and 'math' in (a.get('class') or '').split()
        isskip = tag in ('script', 'style', 'code')
        if tag not in ('img', 'br', 'meta', 'link', 'hr', 'input'):
            self.stack.append((tag, ismath, isskip))
            self.math += ismath
            self.skip += isskip

    def handle_startendtag(self, tag, attrs):
        # <img ... /> is not pushed on the stack by handle_starttag, so it must not pop anything either
        self.handle_starttag(tag, attrs)
        if tag not in ('img', 'br', 'meta', 'link', 'hr', 'input'):
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        while self.stack:
            t, m, s = self.stack.pop()
            if self.optdepth is not None and len(self.stack) <= self.optdepth:
                self.optdepth = None
            if self.inq is not None and len(self.stack) <= self.inq[3]:
                self.inq = None
            self.math -= m
            self.skip -= s
            if t == tag:
                break

    def handle_data(self, data):
        if not self.math and not self.skip:
            self.text.append(data)


def parse(path):
    p = Page()
    with open(path) as f:
        p.feed(f.read())
    return p


def run(docs, webnotes, notes=None, skip_sessions=()):
    """Checks the pages of notes (docs/notes by default). For a private build notes is another folder, and a link
    that leaves it (to the video lectures, to the home page) is looked for in docs/notes/ at the same relative
    place. skip_sessions are sessions that the build did not write, so that a link to them is not an error."""
    real = os.path.join(docs, 'notes')
    notes = notes or real
    pages = {f: parse(f) for f in glob.glob(os.path.join(notes, '**', '*.html'), recursive=True)}
    rel = lambda f: os.path.relpath(f, notes if notes != real else docs)
    skipped = lambda t: any(os.path.normpath(t).startswith(os.path.join(notes, f'session{k}') + os.sep)
                            for k in skip_sessions)
    for f, p in pages.items():
        for h in p.hrefs:
            if re.match(r'^(https?:|mailto:)', h):
                continue
            base, frag = urldefrag(h)
            target = f if base == '' else os.path.normpath(os.path.join(os.path.dirname(f), unquote(base)))
            if notes != real and not target.startswith(notes + os.sep) and target != notes:
                target = os.path.normpath(os.path.join(real, os.path.relpath(target, notes)))
            if skipped(target):
                continue
            if not os.path.exists(target):
                ERRORS.append(f'{rel(f)}: link to a missing file, {h}')
            elif frag and target.endswith('.html'):
                tp = pages.get(target) or parse(target)
                if frag not in tp.ids:
                    ERRORS.append(f'{rel(f)}: link to a missing anchor, {h}')
        for s in p.imgs:
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), s))):
                ERRORS.append(f'{rel(f)}: missing image {s}')
        for s in p.alts:
            ERRORS.append(f'{rel(f)}: image without alt text, {s}' + (' (in a quiz)' if s in p.qimgs else ''))
        for s in sorted(set(p.imgs)):
            t = os.path.normpath(os.path.join(os.path.dirname(f), s))
            if t.endswith('.svg') and os.path.exists(t) and os.path.getsize(t) > BIG_SVG:
                WARNINGS.append(f'{rel(f)}: the SVG {s} is {os.path.getsize(t) // 1024} kB, over {BIG_SVG // 1024} kB'
                                + (' and sits in a quiz' if s in p.qimgs else ''))
        for n, ok, fb, _ in p.quizzes:
            if not ok:
                ERRORS.append(f'{rel(f)}: a quiz with no correct option')
            if fb and n != 3:
                ERRORS.append(f'{rel(f)}: a quiz with feedback has {n} options, it needs exactly 3')
            if not fb:
                OLD_QUIZZES[0] += 1
                OLD_QUIZZES[1] += n != 3
        text = ''.join(p.text)
        if '??' in text:
            ERRORS.append(f'{rel(f)}: "??" in the text')
        m = re.search(r'\\[A-Za-z]+', text)
        if m:
            i = m.start()
            ERRORS.append(f'{rel(f)}: LaTeX left outside math, "{text[max(0, i - 30):i + 40].strip()}"')
    # pages without a source, redirects, and URLs that must not disappear
    listed, frozen_ok = set(), set()
    for mp in glob.glob(os.path.join(webnotes, 'manifest', 'session*.json')):
        m = json.load(open(mp))
        n = m['session']
        files = {pg['file'][:-3] + '.html' for pg in m['pages']}
        for pg in m['pages']:
            listed.add(os.path.normpath(os.path.join(notes, f'session{n}', pg['file'][:-3] + '.html')))
        for r in m.get('redirects', []):
            old, (new, _, frag) = r['from'], r['to'].partition('#')
            listed.add(os.path.normpath(os.path.join(notes, f'session{n}', old)))
            if old in files:
                ERRORS.append(f'session{n}: the redirect from {old} is also a page of the manifest')
            tgt = os.path.normpath(os.path.join(notes, f'session{n}', new))
            if new not in files:
                ERRORS.append(f'session{n}: the redirect {old} points to {new}, which is not a page of the manifest')
            elif skipped(tgt):
                pass
            elif frag and frag not in (pages.get(tgt) or parse(tgt)).ids:
                ERRORS.append(f'session{n}: the redirect {old} points to the missing anchor {r["to"]}')
    for f in pages:
        if re.search(r'session\d+', os.path.dirname(f)) and f not in listed:
            ERRORS.append(f'{rel(f)}: page of the notes with no source in the manifest')
    fz = os.path.join(webnotes, 'manifest', 'frozen_urls.txt')
    if os.path.exists(fz):
        for u in open(fz).read().split():
            t = os.path.normpath(os.path.join(notes, u))
            if not os.path.exists(t) and not skipped(t):
                ERRORS.append(f'{u}: a URL of the site has no page and no redirect (manifest/frozen_urls.txt)')
    npages = len(pages)
    for e in sorted(set(ERRORS)):
        print('ERROR', e)
    for w in sorted(set(WARNINGS)):
        print('WARNING', w)
    if PENDING:
        print(f'pending, {len(PENDING)} references to sessions that are not converted yet (kept as text):',
              ', '.join(sorted(PENDING)))
    nq = sum(len(p.quizzes) for p in pages.values())
    if nq:
        print(f'quizzes: {nq}, of them {OLD_QUIZZES[0]} still in the old form (no feedback per option), '
              f'{OLD_QUIZZES[1]} without exactly 3 options (kept, not an error)')
    print(f'check: {npages} pages, {len(set(ERRORS))} errors')
    return not ERRORS


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    notes = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(0 if run(os.path.join(os.path.dirname(here), 'docs'), here, notes=notes and os.path.abspath(notes)) else 1)
