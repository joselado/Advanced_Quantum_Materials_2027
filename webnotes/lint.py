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
  quiz-long      a sentence of more than 15 words in the question of a quiz, with each math fragment as one word
  quiz-ref       a quiz that refers to a section, a figure or a schematic by its number, so it cannot be read alone
                 (a numbered equation is not reported, since the build shows it inside the quiz)

The shape of a page, checked on the section pages (not on index.md, the introduction of the session):
  opener         the first three sentences of prose under the first heading hold no question (the closing summary
                 is not checked either)
  key            a page with a numbered equation (\\tag{) and no ::: key box, a page of motivation has no \\tag
  long-paragraph a paragraph of more than 150 words outside the blocks, with each math fragment counted as one word,
                 a list item counted alone and the figures left out
  lab-source     in a ::: lab box, an external link that is not in sources/index.json, or a number of a real
                 material that is not in the stored text of its sources (see labsource.py). A number of a real
                 material is a number followed by a unit (K, mK, meV, eV, T, nm, GHz, %, ...) or a number with an
                 error bar, 0.97(2) or 0.9998\\pm0.0006. h/e^2 = 25.8 kOhm, h/2e^2 = 12.9 kOhm and e^2/h are exact
                 and need no source, the figures of the box show the model and are not read, and a number that is
                 our own conversion is listed in the box, ::: {.lab ours="2.3 meV"}. A value that the source gives
                 without the unit, with another one or with another error bar is a hit that says so.
  lab-number     a lab box with no number of a real material, only a warning, since the locked rule asks for one
"""
import argparse
import glob
import os
import re
import sys
from collections import Counter, defaultdict

import labsource

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, 'pages')
MAXWORDS = 35
MAXPARA = 150

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
              'ref-format', 'comesback', 'quiz-long', 'quiz-ref', 'opener', 'key', 'long-paragraph', 'lab-source',
              'lab-number']
QUIZ_MAXWORDS = 15
QUIZ_REF = re.compile(r'\]\(#(sec-[\w-]+|fig:[\w:]+|sch:[\w:]+)\)')


def quiz_lines(path):
    """For every line of a quiz its role, 'q' for the question and 'o' for the options with their feedback."""
    role, state = {}, None
    for i, raw in enumerate(open(path, encoding='utf-8'), start=1):
        st = raw.strip()
        if re.match(r'^:::+\s*quiz\b', st):
            state = 'q'
        elif state and re.match(r'^:::+\s*$', st):
            state = None
        elif state:
            if state == 'q' and re.match(r'^[-*+]\s+\[[ xX]\]', st):
                state = 'o'
            role[i] = state
    return role
WARNINGS = {'exactly', 'lab-number'}


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


def page_kind(path, text):
    """'index' for the introduction of a session, 'closing' for its closing summary, 'section' for the others."""
    name = os.path.basename(path)
    if name == 'index.md':
        return 'index'
    head = re.search(r'^#{1,6}\s+(.*)$', text, re.M)
    if 'closing-summary' in name or (head and re.match(r'closing summary\b', head.group(1), re.I)):
        return 'closing'
    return 'section'


def outline(path):
    """The top level of a page, outside the blocks, as ('heading', line) and ('para', line, prose, words).
    A paragraph ends at a blank line, a fence, a heading, a figure or a new list item. A display equation inside
    a paragraph counts as one word, and a figure with its caption is not a paragraph."""
    out, cur = [], []
    depth, infence, indisplay, infig = 0, False, False, False

    def flush():
        if cur:
            words = sum(len(t.split()) for _, t in cur)
            out.append(('para', cur[0][0], ' '.join(t for _, t in cur), words))
            cur.clear()

    for i, raw in enumerate(open(path, encoding='utf-8'), start=1):
        line = raw.rstrip('\n')
        st = line.strip()
        if st.startswith('```') or st.startswith('~~~'):
            flush()
            infence = not infence
            continue
        if infence:
            continue
        fence = re.match(r'^:{3,}\s*(\S.*)?$', st)
        if fence:
            flush()
            infig = False
            depth = depth + 1 if fence.group(1) else max(0, depth - 1)
            continue
        if depth:
            continue
        if indisplay:
            if line.count('$$') % 2 == 1:
                indisplay = False
                cur.append((i, 'X'))
            continue
        if re.sub(r'\$\$.*?\$\$', '', line).count('$$') % 2 == 1:
            indisplay = True
            cur.append((i, strip_inline(line[:line.rfind('$$')])))
            continue
        if not st:
            flush()
            infig = False
            continue
        if st.startswith('#'):
            flush()
            out.append(('heading', i))
            continue
        if st.startswith('!['):
            flush()
            infig = True
        if infig or st.startswith('<') or st.startswith('|'):
            continue
        if re.match(r'^(?:[-*+]|\d+\.)\s+', st):
            flush()
        cur.append((i, strip_inline(line)))
    flush()
    return out


def opening(items):
    """(line, first three sentences) of the prose under the first heading, skipping the blocks such as recall."""
    seen, line, text = False, None, []
    for it in items:
        if it[0] == 'heading':
            if seen:
                break
            seen = True
        elif seen:
            line = line or it[1]
            text.append(it[2])
            if len(sentences(' '.join(text))) >= 3:
                break
    return line, sentences(' '.join(text))[:3]


KEYBOX = re.compile(r'^:{3,}\s*(?:key\b|\{[^}]*(?<![\w-])\.key(?![\w-]))', re.M)
LAB_INDEX = None


def lab_hits(path):
    """The hits of the lab boxes of a page, from labsource.check_box."""
    global LAB_INDEX
    if LAB_INDEX is None:
        LAB_INDEX = labsource.load_index()
    sess = int(re.search(r'session(\d+)', path).group(1))
    hits = []
    for box in labsource.lab_boxes(path):
        for state, n, what, detail in labsource.check_box(box, LAB_INDEX):
            if state == 'unstored':
                hits.append(('lab-source', n, f'{what} is not stored, run python3 webnotes/labsource.py '
                                              f'--session {sess} {what}'))
            elif state == 'nolink':
                hits.append(('lab-source', n, 'a lab box with no external link'))
            elif state == 'missing':
                hits.append(('lab-source', n, f'{what} is not in the stored text of the sources of this box'))
            elif state == 'nounit':
                hits.append(('lab-source', n, f'{what}, the source has the value but not with this unit or error '
                                              f'bar: {detail[:80]}'))
            elif state == 'nonumber':
                hits.append(('lab-number', n, 'a lab box with no number of a real material and its unit'))
    return list(dict.fromkeys(hits))


def shape_hits(path, text):
    """The hits of the shape of a page, opener, key and long-paragraph. The index page is not a section page and
    is not checked, and the closing summary is not checked for its opener."""
    kind = page_kind(path, text)
    if kind == 'index':
        return []
    hits = []
    items = outline(path)
    if kind == 'section':
        line, first = opening(items)
        if not any('?' in s for s in first):
            snip = first[0][:60].strip() + ' ...' if first else 'no prose under the first heading'
            hits.append(('opener', line or 1, f'no question in the first three sentences: {snip}'))
    nocode = re.sub(r'^(```|~~~).*?^\1', '', text, flags=re.M | re.S)
    tag = re.search(r'\\tag\{([^}]*)\}', nocode)
    if tag and not KEYBOX.search(text):
        n = text[:text.find(tag.group(0))].count('\n') + 1
        hits.append(('key', n, f'a numbered equation ({tag.group(1)}) and no ::: key box'))
    for it in items:
        if it[0] == 'para' and it[3] > MAXPARA:
            hits.append(('long-paragraph', it[1], f'{it[3]} words: {it[2][:60].strip()} ...'))
    return hits


def lint_page(path):
    hits = []
    text = open(path, encoding='utf-8').read()
    inquiz = quiz_lines(path)
    for n, raw, prose in prose_lines(path):
        if n in inquiz:
            for m in QUIZ_REF.finditer(raw):
                hits.append(('quiz-ref', n, f'a quiz refers to {m.group(1)} by its number'))
            if inquiz[n] == 'q' and not raw.lstrip().startswith('!['):
                for s in sentences(prose):
                    w = len(s.split())
                    if w > QUIZ_MAXWORDS:
                        hits.append(('quiz-long', n, f'{w} words in a question: {s[:60].strip()} ...'))
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
    hits += shape_hits(path, text)
    hits += lab_hits(path)
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
