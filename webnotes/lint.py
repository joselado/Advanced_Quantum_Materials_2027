"""Lints the prose of the web Markdown master in webnotes/pages/ against lecture_notes/writing_style.md.

    python3 webnotes/lint.py [--session N] [--category NAME] [--summary]

It only reads the pages. Each hit is printed as file:line, its category and a piece of the line, and at the end
a total per category (and per session when several sessions are linted). It always exits with 0.

The checks run on the prose only. Before a line is checked, the lint removes headings (their text and ids are
frozen), fence lines of blocks (::: quiz, ::: {.tryit ...}), display math, fenced code, inline math, inline code,
link targets, image sources, attribute braces {...}, bare URLs, raw HTML lines, table rules and the quiz marks
[x] and [ ]. The text of a link, a figure caption and the feedback of a quiz option stay, since they are prose.

Categories:
  residue        words about the recording and not about the physics (transcript, slides, instructor, spoken, ...)
  backslash-quote a literal \\" in prose, left over from the conversion
  banned         the words and phrases that writing_style.md and VOICE.md exclude, contractions and "!"
  exactly        "exactly", "simply", "precisely", only a warning, since they can be physics (an exact mapping)
  long-sentence  a sentence of more than 35 words, with each math fragment counted as one word
  punctuation    a colon, a semicolon or an em-dash in prose, except the fixed label **Notebook check-in:**
  session-case   "session N" in lowercase, which the build does not link, write "Session N"
  ref-format     "eq. [", "Eq. [", "fig. [" or "section [", write "equation [(N.M)](#eq-N-M)" or "Section [N.M](#sec-N-M)"
  comesback      a page without a ::: comesback block
"""
import argparse
import glob
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, 'pages')
MAXWORDS = 35

RESIDUE = re.compile(r'\b(transcripts?|slides?|instructors?|recordings?|recorded|lecturers?|this year|'
                     r'previous editions?|next recording|spoken|narrated|raw)\b', re.I)

BANNED_WORDS = [
    # writing_style.md
    'exploit', 'exploits', 'exploited', 'exploiting', 'throw away', 'rigorous', 'rigorously',
    'visually indistinguishable', 'set the stage', 'cautionary note', 'practical upshot',
    'made good on', 'dialed', 'breaks nothing at all', 'honest',
    # VOICE.md, sections 7 and 8, and the global word list
    'delve', 'delves', 'unpack', 'showcase', 'showcases', 'highlight', 'highlights', 'highlighted', 'highlighting',
    'underscore', 'underscores', 'leverage', 'leverages', 'elegant', 'elegantly', 'intriguing', 'nuanced',
    'robustly', 'seamlessly', 'holistic', 'journey', 'dive', 'dives', 'novel', 'cutting-edge', 'under the hood',
    'out of the box', 'battle-tested', 'first-class', 'well-known', 'well known', 'textbook', 'the literature',
    'it is easy to see', 'easy to see that', 'it is worth noting', 'worth noting', 'notably', 'crucially',
    'importantly', 'interestingly', 'remarkably', 'remarkable', 'arguably', 'to some extent',
    'it could be argued', 'by virtue of', 'owing to', 'notwithstanding', 'for the sake of clarity',
    'in summary', 'key takeaways', 'full stop', 'rich zoo', 'extremely', 'incredibly', 'today',
    # contractions
    "let's", "don't", "doesn't", "isn't", "aren't", "can't", "won't", "we'll", "it's", "that's", "we're",
    "you're", "didn't", "wasn't", "weren't", "shouldn't", "wouldn't", "couldn't", "there's", "here's",
    "what's", "haven't", "hasn't", "we've", "you'll",
]
BANNED = re.compile(r'(?<![\w-])(' + '|'.join(re.escape(w) for w in BANNED_WORDS) + r')(?![\w-])|!(?!\[)', re.I)
EXACTLY = re.compile(r'\b(exactly|simply|precisely)\b', re.I)
PUNCT = re.compile(r'[:;—]| -- | – ')
SESSION_CASE = re.compile(r'\bsessions? \d+')
REF_FORMAT = re.compile(r'\b(?:[Ee]qs?|[Ff]igs?)\.\s*\[|\bsection \[|\beq\.?\s*\(')
BACKSLASH_QUOTE = re.compile(r'\\"')

CATEGORIES = ['residue', 'backslash-quote', 'banned', 'exactly', 'long-sentence', 'punctuation', 'session-case',
              'ref-format', 'comesback']
WARNINGS = {'exactly'}


def strip_inline(line):
    """The prose of one line, with math as the token X, links as their text and the rest removed."""
    s = re.sub(r'\\\$', '', line)
    s = re.sub(r'\$\$.*?\$\$', ' X ', s)
    s = re.sub(r'\$[^$]+\$', 'X', s)
    s = re.sub(r'`[^`]*`', 'C', s)
    s = re.sub(r'<!--.*?-->', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\]\([^)]*\)', ']', s)           # link and image targets
    s = re.sub(r'\{[^{}]*\}', '', s)             # attributes {#id number="2.1"} and {.class key="v"}
    s = re.sub(r'https?://\S+', 'U', s)
    s = re.sub(r'^\s*(?:[-*+]|\d+\.)\s+\[[ xX]\]\s*', '', s)   # quiz options
    s = re.sub(r'^\s*(?:[-*+]|\d+\.)\s+', '', s)
    s = s.replace('![', '').replace('[', '').replace(']', '')
    return s


def prose_lines(path):
    """(line number, raw line, prose) for every line of prose of a page."""
    out = []
    infence = indisplay = False
    for i, raw in enumerate(open(path, encoding='utf-8'), start=1):
        line = raw.rstrip('\n')
        st = line.strip()
        if st.startswith('```') or st.startswith('~~~'):
            infence = not infence
            continue
        if infence:
            continue
        if indisplay:
            if line.count('$$') % 2 == 1:
                indisplay = False
                line = line.split('$$', 1)[1]
                st = line.strip()
            else:
                continue
        if re.sub(r'\$\$.*?\$\$', '', line).count('$$') % 2 == 1:
            # a display that opens on this line and closes later
            line = line[:line.rfind('$$')]
            indisplay = True
            st = line.strip()
        if not st or st.startswith('#') or st.startswith(':::') or st.startswith('<') or \
                re.match(r'^\|?\s*:?-{3,}', st):
            continue
        out.append((i, raw.rstrip('\n'), strip_inline(line)))
    return out


def sentences(text):
    """Splits prose at a period, question mark or exclamation mark followed by a space and a capital letter."""
    return [s for s in re.split(r'(?<=[.?!])\s+(?=[A-Z(*"])', text) if s.strip()]


def lint_page(path):
    hits = []
    text = open(path, encoding='utf-8').read()
    for n, raw, prose in prose_lines(path):
        def hit(cat, m, src=prose):
            a = max(0, m.start() - 30)
            hits.append((cat, n, src[a:m.end() + 30].strip()))
        for m in RESIDUE.finditer(prose):
            hit('residue', m)
        nomath = re.sub(r'\$[^$]+\$', 'X', re.sub(r'`[^`]*`', 'C', raw))
        for m in BACKSLASH_QUOTE.finditer(nomath):
            hit('backslash-quote', m, nomath)
        for m in BANNED.finditer(prose):
            hit('banned', m)
        for m in EXACTLY.finditer(prose):
            hit('exactly', m)
        # the label of a converted notebook box, "**Notebook check-in:**", is a fixed title and not prose
        for m in PUNCT.finditer(re.sub(r'^\s*\*\*Notebook check-in:\*\*', '', prose)):
            hit('punctuation', m)
        for m in SESSION_CASE.finditer(prose):
            hit('session-case', m)
        nolinks = re.sub(r'\]\([^)]*\)', ']', nomath)
        for m in REF_FORMAT.finditer(nolinks):
            hit('ref-format', m, nolinks)
        for s in sentences(prose):
            w = len(s.split())
            if w > MAXWORDS:
                hits.append(('long-sentence', n, f'{w} words: {s[:60].strip()} ...'))
    if not re.search(r'^:::\s*\{?\s*\.?comesback\b', text, re.M):
        hits.append(('comesback', 1, 'no ::: comesback block'))
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--session', type=int, help='lint the pages of this session only')
    ap.add_argument('--category', choices=CATEGORIES, action='append', help='only this category (repeatable)')
    ap.add_argument('--summary', action='store_true', help='print only the totals')
    a = ap.parse_args()
    pat = f'session{a.session:02d}' if a.session else 'session*'
    files = sorted(glob.glob(os.path.join(PAGES, pat, '*.md')))
    if not files:
        sys.exit(f'no pages for {pat}')
    total = Counter()
    per_session = defaultdict(Counter)
    for f in files:
        rel = os.path.relpath(f, os.path.dirname(HERE))
        sess = int(re.search(r'session(\d+)', f).group(1))
        for cat, n, snip in lint_page(f):
            if a.category and cat not in a.category:
                continue
            total[cat] += 1
            per_session[sess][cat] += 1
            if not a.summary:
                kind = 'warning' if cat in WARNINGS else cat
                print(f'{rel}:{n}: {kind}{" (" + cat + ")" if cat in WARNINGS else ""}: {snip}')
    cats = [c for c in CATEGORIES if not a.category or c in a.category]
    print()
    if len(per_session) > 1 or a.summary:
        w = max(len(c) for c in cats)
        print('session  ' + ' '.join(c[:w].rjust(len(c)) for c in cats) + '  total (with warnings)')
        for s in sorted(per_session):
            row = per_session[s]
            print(f'{s:7d}  ' + ' '.join(str(row[c]).rjust(len(c)) for c in cats) + f'  {sum(row.values()):5d}')
    print('totals: ' + ', '.join(f'{c}{" (warning)" if c in WARNINGS else ""} {total[c]}' for c in cats))
    print(f'{len(files)} pages, {sum(total[c] for c in cats if c not in WARNINGS)} hits and '
          f'{sum(total[c] for c in cats if c in WARNINGS)} warnings')


if __name__ == '__main__':
    main()
