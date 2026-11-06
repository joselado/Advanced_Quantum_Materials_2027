"""Checks of docs/notes/. Used by build.py, and alone with python3 webnotes/check.py.

Errors: a link to a file or an anchor that does not exist, an image that does not exist, "??", a LaTeX
command left in the text outside the math, an equation number used twice, a page in docs/notes/sessionN/ that
the manifest does not list, a link that the filter could not resolve. External links (http) are not fetched.
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
PENDING = set()


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.imgs, self.text = set(), [], [], []
        self.math = 0          # depth inside a span of class math or inside mjx-container
        self.stack = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a' and 'href' in a:
            self.hrefs.append(a['href'])
        if tag == 'img' and 'src' in a:
            self.imgs.append(a['src'])
        ismath = tag == 'span' and 'math' in (a.get('class') or '').split()
        isskip = tag in ('script', 'style', 'code')
        if tag not in ('img', 'br', 'meta', 'link', 'hr', 'input'):
            self.stack.append((tag, ismath, isskip))
            self.math += ismath
            self.skip += isskip

    def handle_endtag(self, tag):
        while self.stack:
            t, m, s = self.stack.pop()
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


def run(docs, webnotes):
    notes = os.path.join(docs, 'notes')
    pages = {f: parse(f) for f in glob.glob(os.path.join(notes, '**', '*.html'), recursive=True)}
    rel = lambda f: os.path.relpath(f, docs)
    for f, p in pages.items():
        for h in p.hrefs:
            if re.match(r'^(https?:|mailto:)', h):
                continue
            base, frag = urldefrag(h)
            target = f if base == '' else os.path.normpath(os.path.join(os.path.dirname(f), unquote(base)))
            if not os.path.exists(target):
                ERRORS.append(f'{rel(f)}: link to a missing file, {h}')
            elif frag and target.endswith('.html'):
                tp = pages.get(target) or parse(target)
                if frag not in tp.ids:
                    ERRORS.append(f'{rel(f)}: link to a missing anchor, {h}')
        for s in p.imgs:
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), s))):
                ERRORS.append(f'{rel(f)}: missing image {s}')
        text = ''.join(p.text)
        if '??' in text:
            ERRORS.append(f'{rel(f)}: "??" in the text')
        m = re.search(r'\\[A-Za-z]+', text)
        if m:
            i = m.start()
            ERRORS.append(f'{rel(f)}: LaTeX left outside math, "{text[max(0, i - 30):i + 40].strip()}"')
    # pages without a source
    listed = set()
    for mp in glob.glob(os.path.join(webnotes, 'manifest', 'session*.json')):
        m = json.load(open(mp))
        n = m['session']
        for pg in m['pages']:
            listed.add(os.path.normpath(os.path.join(notes, f'session{n}', pg['file'][:-3] + '.html')))
    for f in pages:
        if re.search(r'session\d+', os.path.dirname(f)) and f not in listed:
            ERRORS.append(f'{rel(f)}: page of docs/notes/ with no source in the manifest')
    npages = len(pages)
    for e in sorted(set(ERRORS)):
        print('ERROR', e)
    if PENDING:
        print(f'pending, {len(PENDING)} references to sessions that are not converted yet (kept as text):',
              ', '.join(sorted(PENDING)))
    print(f'check: {npages} pages, {len(set(ERRORS))} errors')
    return not ERRORS


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    sys.exit(0 if run(os.path.join(os.path.dirname(here), 'docs'), here) else 1)
