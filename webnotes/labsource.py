"""Stores the abstract of an article that an "In the lab" box links, so that its numbers can be checked by script.

    python3 webnotes/labsource.py --session N URL_OR_ID [--also ARXIV_ID] [--name NAME] [--url URL] [--force]
    python3 webnotes/labsource.py --session N URL --paste FILE [--origin URL_READ]
    python3 webnotes/labsource.py --quotes
    python3 webnotes/labsource.py --check N

The first form fetches the abstract and adds the URL to sources/index.json, the map from the URL written in a
page to the stored file. URL_OR_ID is the URL as written in the page, or a bare id. The article is written twice.
The full copy sources/.full/sessionNN/NAME.txt, which git ignores, holds every text whole. The tracked file
sources/sessionNN/NAME.txt holds the URL, the ids, the date, the title and every arXiv abstract whole, and of a
text written by a publisher or a journal only the clauses that hold a number that a page quotes, one short
quotation each. The lint reads only the tracked file, so it gives the same result on a fresh clone.
  - An arXiv id or URL (1805.06635, cond-mat/0702408, https://arxiv.org/abs/1212.0572) is fetched from
    https://export.arxiv.org/api/query?id_list=ID.
  - A DOI, or a publisher URL that holds one (https://www.science.org/doi/10.1126/..., https://doi.org/...,
    https://www.nature.com/articles/nmat2003, which is the DOI 10.1038/nmat2003), is fetched from
    https://api.crossref.org/works/DOI.
When Crossref has no abstract of the authors, which is common for Nature and Science, the file keeps what Crossref
has (title, journal and an editor summary when there is one) and the script says so. The keyword --also ARXIV_ID
then attaches the arXiv abstract of the same article, and the script compares the DOI that arXiv gives. A page URL
that holds no id (a sciencedirect pii, say) is stored by passing the DOI as URL_OR_ID and the page URL as --url.

The second form attaches a text copied or fetched by hand, such as the published abstract of a journal page, with
the address where it was read (--origin, by default the URL) and the date. The third form writes the quotations of
the tracked files again from the full copies, which is needed after a lab box gets a new number. The fourth form
prints every number of a real material in the lab boxes of a session, with the sentence of the source where it is
found. The lint (lint.py, category lab-source) uses the same functions.

The fetch uses curl with a timeout and a generic client name, and it sends nothing but the id.
"""
import argparse
import datetime
import glob
import html
import json
import os
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, 'pages')
SOURCES = os.path.join(HERE, 'sources')
INDEX = os.path.join(SOURCES, 'index.json')
FULL = os.path.join(SOURCES, '.full')          # ignored by git, the whole texts for --check and --quotes
TIMEOUT = 30
AGENT = 'labsource/1.0'
ARXIV_API = 'https://export.arxiv.org/api/query?id_list='
CROSSREF_API = 'https://api.crossref.org/works/'
ATOM = {'a': 'http://www.w3.org/2005/Atom', 'x': 'http://arxiv.org/schemas/atom'}

# ---------------------------------------------------------------------------------------------------- ids


ARXIV_ID = re.compile(r'(\d{4}\.\d{4,5}|[a-z][a-z-]*(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?')


def classify(arg):
    """('arxiv', id) or ('doi', doi) for an id or a URL, or None when it holds neither."""
    s = arg.strip()
    m = re.match(r'^(?:https?://)?(?:www\.|export\.)?arxiv\.org/(?:abs|pdf)/' + ARXIV_ID.pattern + r'(?:\.pdf)?/?$',
                 s, re.I)
    if m or re.match(r'^(?:arxiv:)?' + ARXIV_ID.pattern + r'$', s, re.I):
        return 'arxiv', ARXIV_ID.search(s.split('arxiv.org/')[-1]).group(1)
    m = re.search(r'(10\.\d{4,9}/[^\s?#"<>]+)', s)
    if m:
        doi = re.sub(r'/(?:full|abstract|pdf|epdf)$', '', m.group(1).rstrip('.,;)'))
        a = re.match(r'^10\.48550/arxiv\.(.+)$', doi, re.I)      # the DOI that arXiv gives to its own papers
        return ('arxiv', a.group(1)) if a else ('doi', doi)
    m = re.match(r'^(?:https?://)?(?:www\.)?nature\.com/articles/([\w.-]+?)/?(?:\.pdf)?$', s)
    if m:   # a nature.com article URL is the suffix of its DOI
        return 'doi', '10.1038/' + m.group(1)
    return None


def article_id(arg):
    """A key that is the same for every spelling of the URL of an article, 'arxiv:ID' or 'doi:doi'."""
    c = classify(arg)
    return c and f'{c[0]}:{c[1].lower()}'


def page_url(arg, kind, ident):
    """The key of the index, the URL as written in the page, or a canonical URL for a bare id."""
    if re.match(r'^https?://', arg.strip()):
        return arg.strip()
    return f'https://arxiv.org/abs/{ident}' if kind == 'arxiv' else f'https://doi.org/{ident}'


# ---------------------------------------------------------------------------------------------------- fetch


def fetch(url):
    """The body of a URL fetched with curl, or a clear exit when the network gives nothing."""
    try:
        p = subprocess.run(['curl', '-sS', '-L', '--max-time', str(TIMEOUT), '-A', AGENT,
                            '-w', '\n%{http_code}', url], capture_output=True, timeout=TIMEOUT + 10)
    except FileNotFoundError:
        sys.exit('labsource: curl is not installed')
    except subprocess.TimeoutExpired:
        sys.exit(f'labsource: no answer from {url} within {TIMEOUT} s')
    if p.returncode != 0:
        sys.exit(f'labsource: the network gave nothing for {url}\n  curl: {p.stderr.decode(errors="replace").strip()}')
    body, _, code = p.stdout.rpartition(b'\n')
    code = code.decode().strip()
    if code == '404':
        sys.exit(f'labsource: {url} answers 404, the id is not known there. Check it against the page.')
    if code != '200' or not body.strip():
        sys.exit(f'labsource: {url} answers HTTP {code} with {len(body)} bytes, nothing is stored')
    return body.decode('utf-8', errors='replace')


def fetch_arxiv(ident):
    """Title, authors, year, DOI, journal and abstract of an arXiv id."""
    url = ARXIV_API + quote(ident, safe='/.')
    try:
        root = ET.fromstring(fetch(url))
    except ET.ParseError as e:
        sys.exit(f'labsource: arXiv did not answer with XML for {ident} ({e})')
    entries = root.findall('a:entry', ATOM)
    if not entries:
        sys.exit(f'labsource: arXiv has no entry for {ident}')
    e = entries[0]
    title = ' '.join(e.findtext('a:title', '', ATOM).split())
    if '/api/errors' in e.findtext('a:id', '', ATOM) or title == 'Error':
        sys.exit(f'labsource: arXiv says {" ".join(e.findtext("a:summary", "", ATOM).split())}')
    authors = [' '.join(a.findtext('a:name', '', ATOM).split()) for a in e.findall('a:author', ATOM)]
    journal = ' '.join(e.findtext('x:journal_ref', '', ATOM).split())
    years = re.findall(r'\b(19\d\d|20\d\d)\b', journal)      # the year of the journal, not of the preprint
    return {'source': url, 'kind': 'abstract', 'arxiv': ident, 'title': tex_to_text(title), 'authors': authors,
            'year': years[-1] if years else e.findtext('a:published', '', ATOM)[:4],
            'doi': e.findtext('x:doi', '', ATOM).strip(), 'journal': journal,
            'text': tex_to_text(e.findtext('a:summary', '', ATOM))}


def fetch_crossref(doi):
    """Title, authors, year, journal and the abstract (or editor summary) that Crossref holds for a DOI."""
    url = CROSSREF_API + quote(doi, safe='/')
    try:
        m = json.loads(fetch(url))['message']
    except (ValueError, KeyError) as e:
        sys.exit(f'labsource: Crossref did not answer with a record for {doi} ({e})')
    year = ''
    for k in ('published-print', 'published', 'issued', 'published-online'):
        parts = (m.get(k) or {}).get('date-parts') or [[None]]
        if parts[0][0]:
            year = str(parts[0][0])
            break
    journal = ' '.join(filter(None, [(m.get('container-title') or [''])[0], m.get('volume'),
                                     m.get('page') and m['page'].split('-')[0]]))
    journal = re.sub(r' (\d+) (\d+)$', r' \1, \2', journal) + (f' ({year})' if year else '')
    raw = m.get('abstract') or ''
    kind = None
    if raw:
        kind = 'editor summary' if ('related-article' in raw or 'this issue p.' in raw) else 'abstract'
    authors = [' '.join(filter(None, [a.get('given'), a.get('family')])) for a in m.get('author', [])]
    return {'source': url, 'kind': kind, 'doi': doi, 'title': jats_to_text((m.get('title') or [''])[0]),
            'authors': authors, 'year': year, 'journal': journal, 'text': jats_to_text(raw) if raw else '',
            'family': (m.get('author') or [{}])[0].get('family', '')}


# ---------------------------------------------------------------------------------------------------- markup

GREEK = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε', 'varepsilon': 'ε', 'zeta': 'ζ',
         'eta': 'η', 'theta': 'θ', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'pi': 'π',
         'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'phi': 'φ', 'varphi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
         'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ', 'Lambda': 'Λ', 'Sigma': 'Σ', 'Phi': 'Φ', 'Psi': 'Ψ',
         'Omega': 'Ω', 'hbar': 'ħ', 'pm': '±', 'mp': '∓', 'times': '×', 'cdot': '·', 'approx': '≈', 'sim': '~',
         'simeq': '≃', 'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥', 'lesssim': '≲', 'gtrsim': '≳', 'circ': '°',
         'infty': '∞', 'AA': 'Å', 'langle': '⟨', 'rangle': '⟩', 'rightarrow': '→', 'to': '→', 'uparrow': '↑',
         'downarrow': '↓', 'propto': '∝', 'neq': '≠', 'ne': '≠', 'deg': '°', 'textdegree': '°', 'ell': 'ℓ'}
ACCENT = {'"': '\u0308', "'": '\u0301', '`': '\u0300', '^': '\u0302', '~': '\u0303', 'c': '\u0327'}


def tex_to_text(s):
    """Plain text of an arXiv title or abstract: the TeX markup is removed and the symbols become Unicode."""
    s = re.sub(r'\\([%&_#$])', lambda m: {'$': '\x01'}.get(m.group(1), m.group(1)), s)
    s = re.sub(r'\{?\\(["\'`^~]|c )\{?([A-Za-z])\}?\}?',
               lambda m: unicodedata.normalize('NFC', m.group(2) + ACCENT[m.group(1).strip()]), s)
    s = re.sub(r'(?<=[\w$.)])~(?=[\w$\\])', ' ', s)                  # a TeX tie between two tokens is a space
    s = re.sub(r'\\[,;:! ]', ' ', s)
    for _ in range(3):
        s = re.sub(r'\\(?:mathrm|text|textrm|textit|textbf|mathbf|mathit|emph|it|bf|rm|mbox|mathcal)\s*\{([^{}]*)\}',
                   r'\1', s)
    s = re.sub(r'\\([A-Za-z]+)', lambda m: GREEK.get(m.group(1), ''), s)

    def math(m):   # inside $...$ a subscript is written on the line (WTe2, kB) and a superscript keeps its ^
        t = re.sub(r'_\{([^{}]*)\}|_(\w)', lambda k: k.group(1) or k.group(2), m.group(1))
        return re.sub(r'\^\{([^{}]*)\}', r'^\1', t)
    s = re.sub(r'\$([^$]*)\$', math, s)
    s = s.replace('$', '').replace('{', '').replace('}', '').replace('\x01', '$')
    return ' '.join(s.split())


def jats_to_text(s):
    """Plain text of a Crossref title or abstract, with the JATS and MathML markup removed, one paragraph a line.
    The pretty-printing of Crossref puts a newline around every inline tag, so a newline next to a subscript
    or before punctuation is no space (Bi2Se3, MnBi2Te4.) and any other newline is one space."""
    s = re.sub(r'\s*\n\s*', '\x00', s)
    s = re.sub(r'<jats:p>(?:(?!</jats:p>).)*related-article(?:(?!</jats:p>).)*</jats:p>', '', s)  # "this issue p."
    s = re.sub(r'\x00?<jats:(sub|inf)>\x00?(.*?)\x00?</jats:\1>(\x00(?=[A-Z(.,;:)])|)', r'\2', s)
    s = re.sub(r'\x00?<jats:sup>\x00?(.*?)\x00?</jats:sup>(\x00(?=[A-Z(.,;:)])|)', r'^\1', s)
    s = re.sub(r'</?jats:(?:p|title|sec)\b[^>]*>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\x00(?=[.,;:)])', '', s).replace('\x00', ' ')
    s = html.unescape(s)
    return '\n'.join(' '.join(p.split()) for p in s.split('\n') if p.strip())


# ---------------------------------------------------------------------------------------------------- store


def slug(text):
    """Lowercase ASCII letters, digits, dots and hyphens."""
    t = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9.-]+', '-', t).strip('-')


def load_index():
    """The map from the URL written in a page to the stored file, relative to sources/."""
    try:
        return json.load(open(INDEX, encoding='utf-8'))
    except FileNotFoundError:
        return {}


def write_atomic(path, text):
    """Writes a file through a temporary name, so that an interrupted run leaves the old file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(text)
    os.replace(tmp, path)


# The stored file of an article exists twice. sources/sessionNN/NAME.txt is tracked by git. It holds the header,
# every arXiv abstract whole, and of a text written by a publisher or a journal only the clauses that hold a number
# that a page quotes, so that the public repository carries no more of it than the numbers need. The full copy
# sources/.full/sessionNN/NAME.txt is ignored by git and holds every text whole, for --check and --quotes. The lint
# reads only the tracked file, so it gives the same result on a fresh clone.

PASTED = 'text pasted by hand'
HEAD_KEYS = ['url', 'doi', 'arxiv', 'fetched', 'title', 'authors', 'journal']


def new_block(rec, label):
    """A block of a stored file, one text with the address that it came from."""
    return {'label': label, 'source': rec['source'], 'extra': [], 'arxiv': rec.get('arxiv', ''),
            'title': rec.get('title', ''), 'text': rec.get('text', '')}


def publisher(b):
    """True for a text that a publisher or a journal wrote, which the tracked file only quotes."""
    return b['label'] != 'no abstract' and 'arxiv.org' not in b['source']


def make_head(url, main, today):
    """The header of a stored file, with the URL of the page, the ids, the date and the title."""
    a = main['authors']
    return {'url': [url], 'doi': main.get('doi', ''), 'arxiv': main.get('arxiv', ''), 'fetched': today,
            'title': main['title'], 'journal': main.get('journal', ''),
            'authors': ', '.join(a[:6]) + (f' and {len(a) - 6} more' if len(a) > 6 else '')}


def render(head, blocks, quotes=None):
    """The text of a stored file. Without quotes it is the full copy. With quotes, one list of quotations per
    block, it is the tracked file, where a publisher text is replaced by its quotations and where the authors
    and the journal are left out when the file holds a publisher text."""
    pub = quotes is not None and any(publisher(b) for b in blocks)
    rows = []
    for k in HEAD_KEYS:
        vals = head.get(k) or []
        if not (pub and k in ('authors', 'journal')):
            rows += [f'{k}: {v}' for v in (vals if isinstance(vals, list) else [vals]) if v]
    out = ['\n'.join(rows)]
    for i, b in enumerate(blocks):
        quoted = quotes is not None and publisher(b)
        extra = b['extra'] + (['quotations'] if quoted else [])
        lines = [f'[{b["label"]}, from {b["source"]}' + ''.join(', ' + e for e in extra) + ']']
        if b['arxiv']:
            lines.append(f'arxiv: {b["arxiv"]}')
        if b['title'] and not quoted:
            lines.append(f'title: {b["title"]}')
        if quoted:
            lines += [f'"{q}"' for q in quotes[i]] or ['(no number that a page quotes is in this text)']
        else:
            lines.append(b['text'] or '(no text)')
        out.append('\n'.join(lines))
    return '\n\n'.join(out) + '\n'


def parse(path):
    """The header and the blocks of a stored file, the full copy or the tracked one."""
    chunks = open(path, encoding='utf-8').read().strip('\n').split('\n\n')
    head = {'url': []}
    for line in chunks[0].splitlines():
        k, _, v = line.partition(': ')
        if k == 'url':
            head['url'].append(v)
        else:
            head[k] = v
    blocks = []
    for ch in chunks[1:]:
        rows = ch.splitlines()
        m = re.match(r'^\[(.+?), from (\S+?)((?:, [^,\]]+)*)\]$', rows[0])
        if not m and blocks:             # a blank line inside a text, left by a hand edit
            blocks[-1]['text'] += '\n' + ch
            continue
        extra = [e for e in m.group(3).split(', ') if e]
        b = {'label': m.group(1), 'source': m.group(2), 'extra': [e for e in extra if e != 'quotations'],
             'arxiv': '', 'title': '', 'text': ''}
        body = rows[1:]
        while body and re.match(r'^(arxiv|title): ', body[0]):
            k, _, v = body[0].partition(': ')
            b[k] = v
            body = body[1:]
        if 'quotations' in extra:
            body = [l[1:-1] for l in body if l.startswith('"') and l.endswith('"')]
        b['text'] = '\n'.join(body)
        blocks.append(b)
    return head, blocks


def load(rel, quiet=False):
    """The header and the blocks of a stored article, from the full copy, or from the tracked file with a
    warning when this machine has no full copy (a fresh clone)."""
    full = os.path.join(FULL, rel)
    if os.path.exists(full):
        return parse(full)
    if not quiet:
        print(f'labsource: no full copy of sources/{rel} on this machine, its publisher texts are only quotations')
    return parse(os.path.join(SOURCES, rel))


def stored_text(rel, full=False):
    """The titles and the texts of a stored file, without the URLs and the dates, which hold no physics. The lint
    reads the tracked file, and --check reads the full copy when this machine has one."""
    path = os.path.join(FULL if full else SOURCES, rel)
    keep = []
    for l in open(path, encoding='utf-8').read().splitlines():
        if re.match(r'^(url|doi|arxiv|fetched|authors|journal): |^\[', l):
            continue
        l = re.sub(r'^title: ', '', l)
        keep.append(l[1:-1] if l.startswith('"') and l.endswith('"') else l)
    return '\n'.join(keep)


def quotations(text, nums):
    """One short quotation of a text for each number of a page that it holds, the clause with the number, so that
    the tracked file gives the same match as the whole text."""
    out = []
    for n in nums:
        state, sent = find(n, text)
        if state == 'missing':
            continue
        q = next((c.rstrip(',;') for c in re.split(r'(?<=[,;])\s+', sent) if find(n, c)[0] == state), sent)
        words = q.split()
        if len(words) > 25:                 # a long clause is cut to about 20 words around the number
            k = next((i for i, w in enumerate(words)
                      if any(m.value == n.value for m in numbers(w, all_numbers=True))), 0)
            a, b = max(0, k - 12), min(len(words), k + 8)
            cut = ('... ' if a else '') + ' '.join(words[a:b]) + (' ...' if b < len(words) else '')
            q = cut if find(n, cut)[0] == state else q
        if q not in out:
            out.append(q)
    return out


def all_boxes():
    """Every lab box of every page, read once."""
    return [b for f in sorted(glob.glob(os.path.join(PAGES, 'session*', '*.md'))) for b in lab_boxes(f)]


def page_numbers(rel, index, boxes):
    """The numbers of real materials that the lab boxes of all the sessions quote from the article in rel."""
    by_id = {article_id(k): v for k, v in index.items() if article_id(k)}
    out = []
    for box in boxes:
        if any((index.get(u) or by_id.get(article_id(u))) == rel for _, u in box['links']):
            ours = numbers(box['ours'])
            out += [x for _, x in box_numbers(box) if not any(o.value == x.value and o.unit == x.unit for o in ours)]
    return out


def save(rel, head, blocks, index, boxes=None):
    """Writes the full copy and the tracked file of an article, and returns the quotations of the tracked one."""
    head['url'] = sorted(k for k, v in index.items() if v == rel) or head['url']
    write_atomic(os.path.join(FULL, rel), render(head, blocks))
    nums = page_numbers(rel, index, all_boxes() if boxes is None else boxes)
    quotes = [quotations(b['text'], nums) if publisher(b) else [] for b in blocks]
    write_atomic(os.path.join(SOURCES, rel), render(head, blocks, quotes))
    return [q for qs in quotes for q in qs]


def write_index(index):
    """Writes sources/index.json, sorted, so that its diff shows only the URLs that changed."""
    write_atomic(INDEX, json.dumps(index, indent=1, sort_keys=True, ensure_ascii=False) + '\n')


def report(rel, quotes):
    """Prints what the stored article holds for the lint."""
    nums = dict.fromkeys(n.show() for n in numbers(stored_text(rel, full=True)))
    print('numbers with a unit or an error bar in it: ' + (', '.join(nums) or 'none'))
    for q in quotes:
        print(f'  quoted in the tracked file: "{q}"')


def page_key(args):
    """The URL of the index for the arguments, the URL of the page as written, or a canonical URL for an id."""
    c = classify(args.source)
    if args.url:
        return args.url, c
    if not c:
        sys.exit(f'labsource: no arXiv id and no DOI in {args.source}. Pass the DOI of the article and the URL of '
                 f'the page with --url.')
    return page_url(args.source, *c), c


def store(args):
    """Fetches one article and writes its two files and its line of the index."""
    url, c = page_key(args)
    if not c:
        sys.exit(f'labsource: no arXiv id and no DOI in {args.source}. Pass the DOI of the article instead.')
    kind, ident = c
    ca = classify(args.also) if args.also else None
    if args.also and (not ca or ca[0] != 'arxiv'):
        sys.exit(f'labsource: --also takes an arXiv id, and {args.also} is not one')
    index = load_index()
    if url in index and not args.force:
        print(f'{url} is stored in sources/{index[url]}, use --force to fetch it again')
        return
    main = fetch_arxiv(ident) if kind == 'arxiv' else fetch_crossref(ident)
    also = None
    if ca:
        also = fetch_arxiv(ca[1])
        if main.get('doi') and also['doi']:
            same = also['doi'].lower() == main['doi'].lower()
            print(f'arXiv {ca[1]} names the DOI {also["doi"]}, ' +
                  ('which is the same article' if same else f'and not {main["doi"]}. Check that it is the same article'))
        else:
            print(f'arXiv {ca[1]} names no DOI. Compare the titles:\n  {main["title"]}\n  {also["title"]}')
    family = main.get('family') or (main['authors'][0].split()[-1] if main['authors'] else '')
    idslug = slug(ident.split('/', 1)[1]) if kind == 'doi' else 'arxiv' + slug(ident)
    name = args.name or slug(family + main['year']) + '_' + idslug
    rel = f'session{args.session:02d}/{name}.txt'
    today = datetime.date.today().isoformat()
    if main['kind']:
        blocks = [new_block(main, main['kind'])]
    else:
        blocks = [{'label': 'no abstract', 'source': main['source'], 'extra': [], 'arxiv': '', 'title': '',
                   'text': 'Crossref holds the title and the journal only.'}]
    if also:
        blocks.append(new_block(also, 'abstract'))
    old = index.get(url)
    if old and os.path.exists(os.path.join(SOURCES, old)):
        kept = [b for b in load(old, quiet=True)[1] if b['label'] == PASTED]   # a new fetch keeps them
        blocks += kept
        if kept:
            print(f'kept {len(kept)} text pasted by hand from the file before')
    index[url] = rel
    if old and old != rel and old not in index.values():
        for d in (SOURCES, FULL):            # the file that no URL of the index points to any more
            if os.path.exists(os.path.join(d, old)):
                os.remove(os.path.join(d, old))
        print(f'removed sources/{old}, which the new name replaces')
    write_index(index)
    quotes = save(rel, make_head(url, main, today), blocks, index)
    print(f'stored {url}\n    in sources/{rel}')
    if kind == 'doi' and main['kind'] != 'abstract' and not also:
        what = 'only an editor summary' if main['kind'] else 'no abstract'
        print(f'Crossref has {what} for {ident}, so the file holds the title and the journal'
              f'{" and that summary" if main["kind"] else ""}. Pass --also ARXIV_ID to attach the arXiv abstract,'
              f' or --paste FILE to attach the published abstract read by hand.')
    report(rel, quotes)


def paste(args):
    """Attaches a text copied or fetched by hand to an article, with the address where it was read and the date.
    An article that is not stored yet is fetched first."""
    url, _ = page_key(args)
    try:
        raw = open(args.paste, encoding='utf-8').read()
    except OSError as e:
        sys.exit(f'labsource: cannot read {args.paste} ({e})')
    text = '\n'.join(' '.join(html.unescape(p).split()) for p in re.split(r'\n\s*\n', raw) if p.strip())
    if not text:
        sys.exit(f'labsource: {args.paste} is empty, nothing is attached')
    index = load_index()
    if url not in index:
        store(args)
        index = load_index()
    rel = index[url]
    head, blocks = load(rel)
    origin = args.origin or url
    today = datetime.date.today().isoformat()
    blocks = [b for b in blocks if not (b['label'] == PASTED and b['source'] == origin)]
    blocks.append({'label': PASTED, 'source': origin, 'extra': [f'read {today}'], 'arxiv': '', 'title': '',
                   'text': text})
    quotes = save(rel, head, blocks, index)
    print(f'attached the text of {args.paste}, read at {origin} on {today}\n    to sources/{rel}')
    report(rel, quotes)


def requote():
    """Writes again the quotations of every tracked file from its full copy, for the numbers that the pages quote
    now. It is run after a lab box gets a new number."""
    index = load_index()
    boxes = all_boxes()
    for rel in sorted(set(index.values())):
        full = os.path.join(FULL, rel)
        if not any(publisher(b) for b in parse(os.path.join(SOURCES, rel))[1]):
            continue                         # only arXiv texts, which the tracked file holds whole
        if not os.path.exists(full):
            print(f'sources/{rel}: no full copy on this machine, the quotations stay. Fetch it again with --force.')
            continue
        before = open(os.path.join(SOURCES, rel), encoding='utf-8').read()
        head, blocks = parse(full)
        save(rel, head, blocks, index, boxes)
        after = open(os.path.join(SOURCES, rel), encoding='utf-8').read()
        print(f'sources/{rel}: ' + ('quotations written again' if after != before else 'no change'))


# ---------------------------------------------------------------------------------------------------- numbers

UNITS = ['K', 'mK', 'μK', 'eV', 'meV', 'μeV', 'keV', 'T', 'mT', 'nm', 'μm', 'Å', 'Hz', 'kHz', 'MHz', 'GHz', 'THz',
         '%', 'Ω', 'kΩ', 'MΩ', 'S', 'mS', 'μS', 'nA', 'μA', 'mA', 'mV', 'μV', 'cm^-1', 'cm-1']
UNIT_WORDS = [(r'millikelvins?', 'mK'), (r'kelvins?', 'K'), (r'milli-?electron ?volts?', 'meV'),
              (r'electron ?volts?', 'eV'), (r'millitesla', 'mT'), (r'teslas?', 'T'), (r'per ?cent', '%'),
              (r'nanomet(?:er|re)s?', 'nm'), (r'gigahertz', 'GHz'), (r'megahertz', 'MHz'), (r'terahertz', 'THz'),
              (r'kilo-?ohms?|kohms?', 'kΩ'), (r'ohms?', 'Ω')]
NUMBER = re.compile(r'(?<![\w.^])(\d+\.\d+|\d+|\.\d+)(?![\d])'
                    r'(?:\((\d+)\)|\s?±\s?(\d+\.\d+|\d+|\.\d+))?'
                    r'(?:\s?(' + '|'.join(re.escape(u) for u in sorted(UNITS, key=len, reverse=True)) + r')(?![\w]))?')
RK = Decimal('25.81280745')    # h/e^2 in kOhm, exact in the SI


def normalize(text):
    """Text in which the page and the stored source write a number and its unit in the same way. Spaces of TeX,
    thin spaces, "~", "≈" and "\\sim" become one space, "+-" and "\\pm" become "±", and the unit words become
    their symbols."""
    s = text.replace('\\%', '%').replace('\\pm', '±').replace('+/-', '±').replace('+-', '±')
    s = re.sub(r'\\mathrm\{([^{}]*)\}|\\text\{([^{}]*)\}', lambda m: m.group(1) or m.group(2), s)
    s = re.sub(r'\\(Omega|mu|pi)(?![A-Za-z])', lambda m: GREEK[m.group(1)], s)
    s = s.replace('µ', 'μ').replace('Ω', 'Ω')     # the micro sign and the ohm sign
    s = re.sub(r'\\[,;:! ]|\\(?:approx|sim|simeq|lesssim|gtrsim)(?![A-Za-z])|[~≈∼≃\u00a0\u2009\u202f\u2002\u2003]',
               ' ', s)
    s = s.replace('$', '').replace('{', '').replace('}', '')
    for pat, sym in UNIT_WORDS:
        s = re.sub(r'(?<=[\d\s])' + pat + r'(?![A-Za-z])', sym, s, flags=re.I)
    return re.sub(r'[ \t]+', ' ', s)


class Num:
    """A number of a text, with its error bar and its unit when they follow it."""
    def __init__(self, m):
        self.text = m.group(0).strip()
        self.value = Decimal(m.group(1))
        self.err = m.group(2) or m.group(3)
        self.unit = m.group(4)

    def show(self):
        return ' '.join(self.text.split())

    def constant(self):
        """True for h/e^2 = 25.8 kOhm and h/2e^2 = 12.9 kOhm, written with at least one decimal (or 25812.8 Ohm).
        Another plateau, such as h/3e^2 = 8.6 kOhm, is marked by the author with ours, so that a measured
        resistance is never let through by the rounding."""
        digits = -self.value.as_tuple().exponent
        if self.unit not in ('kΩ', 'Ω') or digits < 1 or self.err:
            return False
        base = RK if self.unit == 'kΩ' else RK * 1000
        return any(round(base / n, digits) == self.value for n in (1, 2))


def numbers(text, all_numbers=False):
    """The numbers of a text that carry a unit or an error bar, or with all_numbers=True every number."""
    out = []
    for m in NUMBER.finditer(normalize(text)):
        try:
            n = Num(m)
        except InvalidOperation:
            continue
        if all_numbers or n.unit or n.err:
            out.append(n)
    return out


def find(n, text):
    """Where a number of a page stands in a source text: ('found', sentence) when the source has the same value
    with the same unit and the same error bar, ('nounit', sentence) when it has the value with another unit, with
    none or with another error bar, or ('missing', ''). An error bar of the page must be in the source, while a
    source may give an error bar that the page leaves out."""
    sents = re.split(r'(?<=[.?!])\s+(?=[A-Z])|\n', text)
    weak = None
    for s in sents:
        for m in numbers(s, all_numbers=True):
            if m.value != n.value:
                continue
            err = not n.err or (m.err and Decimal(m.err) == Decimal(n.err))
            if err and (n.unit is None or m.unit == n.unit):
                return 'found', s.strip()
            weak = weak or s.strip()
    return ('nounit', weak) if weak else ('missing', '')


# ---------------------------------------------------------------------------------------------------- lab boxes

LAB_FENCE = re.compile(r'^(:{3,})\s*(?:lab|\{([^}]*)\})\s*$')
LINK = re.compile(r'\]\((https?://[^)\s]+)\)|<(https?://[^>\s]+)>|(?<![(<])(https?://[^\s)>\]]+)')


def lab_boxes(path):
    """The lab boxes of a page, each with its first line, its attribute ours, its external links and the lines of
    its prose. The figures inside the box are left out, since they show the model of the page and not the
    material."""
    boxes, stack, cur, infence, infig = [], [], None, False, False
    for i, raw in enumerate(open(path, encoding='utf-8'), start=1):
        st = raw.strip()
        if st.startswith('```') or st.startswith('~~~'):
            infence = not infence
        if infence:
            continue
        m = re.match(r'^(:{3,})\s*(\S.*)?$', st)
        if m:
            infig = False
            if m.group(2):                       # an opening fence, ::: lab or ::: {.lab ours="..."}
                lm = LAB_FENCE.match(st)
                islab = bool(lm) and (lm.group(2) is None or
                                      bool(re.search(r'(?<![\w-])\.lab(?![\w-])', lm.group(2))))
                stack.append(islab)
                if islab and cur is None:
                    ours = re.search(r'\bours="([^"]*)"', lm.group(2) or '')
                    cur = {'line': i, 'ours': ours.group(1) if ours else '', 'links': [], 'lines': []}
            elif stack and stack.pop() and cur is not None:
                boxes.append(cur)
                cur = None
            continue
        if cur is None:
            continue
        for lk in LINK.finditer(raw):
            cur['links'].append((i, next(g for g in lk.groups() if g)))
        if st.startswith('!['):
            infig = True
        if not st:
            infig = False
            cur['lines'].append((i, ''))
        elif not infig:
            cur['lines'].append((i, re.sub(r'\]\(#[^)]*\)', ']', LINK.sub(']', raw.rstrip('\n')))))
    return boxes


def box_numbers(box):
    """(line, number) for each number of a real material in a lab box, the exact constants left out. The lines of
    a paragraph are read together, so that a number and its unit on two lines are seen, and the number is given
    the first line of its paragraph when it is not on one line alone."""
    paras, cur = [], []
    for n, line in box['lines'] + [(0, '')]:
        if line.strip():
            cur.append((n, re.sub(r'`[^`]*`', '', line)))
        elif cur:
            paras.append(cur)
            cur = []
    out = []
    for p in paras:
        for x in numbers(' '.join(t for _, t in p)):
            if not x.constant():
                n = next((k for k, t in p if any(y.show() == x.show() for y in numbers(t))), p[0][0])
                out.append((n, x))
    return out


def check_box(box, index=None):
    """The state of every link and every number of a lab box, as a list of (state, line, what, detail) with the
    states 'stored', 'unstored', 'nolink', 'found', 'nounit', 'missing', 'ours' and 'nonumber'."""
    index = load_index() if index is None else index
    by_id = {article_id(k): v for k, v in index.items() if article_id(k)}
    out, files = [], []
    for n, url in box['links']:
        rel = index.get(url) or by_id.get(article_id(url))
        if rel and os.path.exists(os.path.join(SOURCES, rel)):
            files.append(rel)
            out.append(('stored', n, url, rel))
        else:
            out.append(('unstored', n, url, ''))
    if not box['links']:
        out.append(('nolink', box['line'], 'no external link', ''))
    text = '\n'.join(stored_text(r) for r in dict.fromkeys(files))
    ours = numbers(box['ours'])
    nums = box_numbers(box)
    for n, x in nums:
        if any(o.value == x.value and o.unit == x.unit for o in ours):
            out.append(('ours', n, x.show(), 'marked as our own number'))
            continue
        state, sent = find(x, text) if files else ('missing', '')
        out.append((state, n, x.show(), sent))
    if not nums:
        out.append(('nonumber', box['line'], 'no number of a material', ''))
    return out


def check_session(session):
    """Prints every link and every number of the lab boxes of a session with its state. The state comes from the
    tracked files, as in the lint, and the sentence shown comes from the full copy when this machine has one."""
    index = load_index()
    files = sorted(glob.glob(os.path.join(PAGES, f'session{session:02d}', '*.md')))
    count = {}
    for f in files:
        for box in lab_boxes(f):
            print(f'{os.path.relpath(f, os.path.dirname(HERE))}:{box["line"]}: lab box')
            rows = check_box(box, index)
            rels = [d for st, _, _, d in rows if st == 'stored']
            full = '\n'.join(stored_text(r, full=True) for r in dict.fromkeys(rels)
                             if os.path.exists(os.path.join(FULL, r)))
            for state, n, what, detail in rows:
                count[state] = count.get(state, 0) + 1
                if state in ('found', 'nounit', 'missing') and full:
                    fstate, fsent = find(numbers(what)[0], full)
                    detail = fsent or detail
                    if fstate != state:
                        detail += (f'\n            ({fstate} in the full copy, run python3 webnotes/labsource.py '
                                   f'--quotes)')
                print(f'  {n}: {state:8s} {what}' + (f'\n            {detail}' if detail else ''))
    print('\n' + ', '.join(f'{k} {v}' for k, v in sorted(count.items())) if count else 'no lab box')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source', nargs='?', help='the URL as written in the page, or an arXiv id or a DOI')
    ap.add_argument('--session', type=int, help='the session whose page links the article')
    ap.add_argument('--also', help='an arXiv id of the same article, attached when Crossref has no abstract')
    ap.add_argument('--paste', metavar='FILE', help='attach the text of FILE, copied or fetched by hand')
    ap.add_argument('--origin', help='with --paste, the address where the text was read (default: the URL)')
    ap.add_argument('--name', help='the name of the stored file, without .txt (default: author, year and id)')
    ap.add_argument('--url', help='the URL as written in the page, when it holds no id and the id is given apart')
    ap.add_argument('--force', action='store_true', help='fetch again a URL that is already stored')
    ap.add_argument('--check', type=int, metavar='N', help='print the numbers of the lab boxes of Session N')
    ap.add_argument('--quotes', action='store_true',
                    help='write again the quotations of the tracked files, after a lab box got a new number')
    a = ap.parse_args()
    if a.check:
        check_session(a.check)
        return
    # Every other form reads sources/index.json at the start and writes it at the end, so two runs at the same
    # time would lose one of the URLs. The lock in the ignored folder sources/.full/ makes them wait for each other.
    import fcntl
    os.makedirs(FULL, exist_ok=True)
    lock = open(os.path.join(FULL, '.lock'), 'w')
    fcntl.flock(lock, fcntl.LOCK_EX)
    if a.quotes:
        requote()
    elif a.source and a.session and a.paste:
        paste(a)
    elif a.source and a.session:
        store(a)
    else:
        ap.error('give --session N and a URL or an id, or --check N, or --quotes')


if __name__ == '__main__':
    main()
