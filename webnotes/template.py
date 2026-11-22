"""The page shell of the notes. The frame, the bar of the sessions, the tabs and the pager are those of
docs/build_site.py, imported so that the navigation of the site exists once. Here is only what the notes add."""
import html
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), 'docs')

_spec = importlib.util.spec_from_file_location('build_site', os.path.join(DOCS, 'build_site.py'))
site = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site)

REPO = site.REPO
PRIVATE = False      # a private build (build.py --out DIR) has notes.js and notes.css one folder up, not in notes/
CSS_LINK = 'notes.css">'
# the blocks and figures added for the web carry these classes, and only a page that has one links notes.css,
# so a page without them is the same file as before
NEW_BLOCKS = re.compile(r'class="[^"]*\b(quiz|tryit|schematic|again|panel|sec-next|widget|comesback|fold|problem|lab|keybox|recall|has-script)\b')

NOTES_STYLE = """
  /* a page of the notes: the list of the sections of the session at the left, the text in a column of 728 px, about
     85 characters. At 680 px 19 of the 997 display equations scrolled sideways, at 728 px 8, at the old 828 px 4. */
  .withside { display: grid; grid-template-columns: 240px minmax(0, 728px); gap: 0 40px; margin-top: 22px; }
  .withside > article { min-width: 0; }
  /* the list is as tall as the window below the head of the page, so that it is whole before the page is scrolled */
  .secnav { font-size: 0.9rem; align-self: start; position: sticky; top: 14px; max-height: calc(100vh - 200px);
            overflow-y: auto; padding-right: 6px; }
  .secnav summary { list-style: none; color: var(--muted); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.07em;
                    text-transform: uppercase; padding: 0 0 6px 10px; pointer-events: none; }
  .secnav summary::-webkit-details-marker { display: none; }
  .secnav summary .pos { display: none; }
  .secnav ol { list-style: none; margin: 0; padding: 0; }
  .secnav li { margin: 0; }
  .secnav a { display: grid; grid-template-columns: 3.3em 1fr; padding: 4px 6px 4px 8px; text-decoration: none;
              color: var(--fg); border-left: 2px solid var(--rule); line-height: 1.35; }
  .secnav a .n { color: var(--muted); }
  .secnav a:hover { background: var(--tab); }
  .secnav a[aria-current] { border-left-color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--bg));
                            font-weight: 600; }
  @media (max-width: 1039px) {
    .withside { display: block; max-width: 728px; margin-left: auto; margin-right: auto; }
    .secnav { position: static; max-height: none; border: 1px solid var(--rule); border-radius: 8px; background: var(--card);
              padding: 0; margin-bottom: 18px; }
    .secnav summary { pointer-events: auto; cursor: pointer; padding: 8px 12px; list-style: revert; text-transform: none;
                      letter-spacing: 0; font-size: 0.93rem; font-weight: 600; color: var(--fg); }
    .secnav summary::-webkit-details-marker { display: revert; }
    .secnav summary .pos { display: inline; color: var(--muted); font-weight: 400; }
    .secnav ol { padding: 0 8px 8px; }
  }
  .crumb { margin: 0 0 4px; font-size: 0.85rem; color: var(--muted); }
  .num { color: var(--muted); font-weight: 400; margin-right: 0.15em; }
  .toc ol { list-style: none; padding-left: 0; }
  .toc li { margin: 5px 0; display: grid; grid-template-columns: 3.6em 1fr; }
  .toc .n { color: var(--muted); }
  figure { margin: 24px 0; }
  figure img { width: 100%; height: auto; background: #fff; border-radius: 6px; display: block; }
  figcaption { font-size: 0.93rem; color: var(--muted); margin-top: 8px; }
  .eq { display: block; }
  .math.display { display: block; max-width: 100%; overflow-x: auto; overflow-y: hidden; }
  mjx-container[display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
  mjx-assistive-mml { max-width: 100%; }
  .notebookbox { background: color-mix(in srgb, var(--w1, #c64600) 6%, var(--card)); border: 1px solid var(--rule);
                 border-left: 3px solid var(--w1, #c64600); border-radius: 6px; padding: 8px 16px; margin: 20px 0;
                 font-size: 0.95rem; }
  .tryit { background: var(--card); border-left: 3px solid var(--muted); border-radius: 6px; padding: 8px 16px;
           margin: 20px 0; font-size: 0.95rem; }
  .quiz, .widget { border: 1px solid var(--rule); border-radius: 8px; padding: 8px 16px; margin: 24px 0; }
  table { border-collapse: collapse; margin: 16px 0; font-size: 0.95rem; }
  th, td { border-bottom: 1px solid var(--rule); padding: 4px 10px; text-align: left; }
  div.center { overflow-x: auto; }
  div.center table { margin-left: auto; margin-right: auto; }
  th { border-bottom: 2px solid var(--rule); }
  .coursecontents { max-width: 760px; }
  .coursecontents h2 { margin-top: 28px; }
  @media print { .withside { display: block; max-width: none; } }
"""

MATHJAX_DIR = 'mathjax/'     # the copy of MathJax 3.2.2 in notes/, written by build.py, so that the pages work without network
MATHJAX = ('<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]],tags:"none"},'
           'options:{skipHtmlTags:["script","noscript","style","textarea","pre","code"]}};</script>\n'
           '<script id="MathJax-script" async src="%stex-chtml.js"></script>')


def esc(s):
    return html.escape(s, quote=True)


def shell(title, body, depth):
    """A page of the notes. depth is the number of folders below docs/, 2 for notes/session2/x.html. The frame of
    the page is site.page(), the one of the video pages, and the notes add MathJax, notes.js and their style."""
    up = '../' * depth
    assets = '../' * (depth - 1) if PRIVATE else f'{up}notes/'
    css = f'<link rel="stylesheet" href="{assets}{CSS_LINK}\n' if NEW_BLOCKS.search(body) else ''
    head = f'{MATHJAX % (assets + MATHJAX_DIR)}\n{css}<script src="{assets}notes.js" defer></script>\n'
    return site.page(title, body, depth, head=head, style=NOTES_STYLE)


def top(sessions, built, n, depth):
    """The bar of the site, with the row of the sessions pointing to their notes."""
    up = '../' * depth
    return site.top(up, site.chips(sessions, n, lambda k: f'{up}notes/session{k}/index.html', ready=lambda k: k in built))


def session_head(n, title, depth, h1=True):
    """The head of a session with its two tabs, the notes being the one that is on."""
    return site.session_head(n, title, 'notes', '../' * depth, h1=h1, notes=True)


def secnav(n, pages, i):
    """The list of the pages of session n, with page i marked. It is a <details> that the reader opens on a narrow
    screen. On a wide screen it is the column at the left, opened by the line of script, with page i scrolled into view."""
    rows = []
    for j, p in enumerate(pages):
        cur = ' aria-current="page"' if j == i else ''
        num = p['number'] if j else ''
        name = title_html(p['title']) if j else 'Introduction'
        href = f'{p["file"][:-3] if j else "index"}.html'
        rows.append(f'<li><a href="{href}"{cur}><span class="n">{num}</span><span>{name}</span></a></li>')
        for x in p.get('also', []) if j else []:     # the other sections of a merged page, with the anchor of each
            rows.append(f'<li class="also"><a href="{href}#{x["id"]}"><span class="n">{x["number"]}</span>'
                        f'<span>{title_html(x["title"])}</span></a></li>')
    return (f'  <details class="secnav"><summary>Session {n} <span class="pos">· all sections</span></summary>'
            f'<ol>{"".join(rows)}</ol></details>\n'
            '  <script>(function(d){if(matchMedia("(min-width:1040px)").matches){d.open=true;'
            'var a=d.querySelector("[aria-current]");if(a)d.scrollTop=a.offsetTop-d.clientHeight/2;}})'
            '(document.currentScript.previousElementSibling);</script>\n')


def title_html(t):
    """A title of the manifest as HTML. Inline math is passed to MathJax."""
    return re.sub(r'\$([^$]+)\$', lambda m: '\\(' + m.group(1) + '\\)', html.escape(t, quote=False))
