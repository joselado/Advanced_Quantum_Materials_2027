"""The page shell of the notes. The look is the one of docs/build_site.py, imported so that it stays one."""
import html
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), 'docs')

_spec = importlib.util.spec_from_file_location('build_site', os.path.join(DOCS, 'build_site.py'))
site = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site)

REPO = site.REPO

NOTES_STYLE = """
  main { max-width: 860px; }
  .sub span { min-width: 2.4em; text-align: center; padding: 4px 8px; border: 1px dashed var(--rule);
              border-radius: 6px; color: var(--muted); }
  .crumb { margin: 0 0 4px; font-size: 0.95rem; }
  .num { color: var(--muted); font-weight: 400; margin-right: 0.15em; }
  .toc ol { list-style: none; padding-left: 0; } .toc li { margin: 5px 0; }
  .toc .n { display: inline-block; min-width: 2.6em; color: var(--muted); }
  .links { color: var(--muted); font-size: 0.95rem; margin: 6px 0 18px; }
  figure { margin: 24px 0; }
  figure img { width: 100%; height: auto; background: #fff; border-radius: 6px; display: block; }
  figcaption { font-size: 0.93rem; color: var(--muted); margin-top: 8px; }
  .eq { display: block; }
  .math.display { overflow-x: auto; overflow-y: hidden; }
  mjx-container[display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
  .notebookbox { background: color-mix(in srgb, var(--accent) 8%, var(--card)); border-left: 3px solid var(--accent);
                 border-radius: 6px; padding: 8px 16px; margin: 20px 0; font-size: 0.95rem; }
  .tryit { background: var(--card); border-left: 3px solid var(--muted); border-radius: 6px; padding: 8px 16px;
           margin: 20px 0; font-size: 0.95rem; }
  .quiz, .widget { border: 1px solid var(--rule); border-radius: 8px; padding: 8px 16px; margin: 24px 0; }
  table { border-collapse: collapse; margin: 16px 0; font-size: 0.95rem; }
  th, td { border-bottom: 1px solid var(--rule); padding: 4px 10px; text-align: left; }
  .coursecontents h2 { margin-top: 28px; }
"""

MATHJAX = ('<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]],tags:"none"},'
           'options:{skipHtmlTags:["script","noscript","style","textarea","pre","code"]}};</script>\n'
           '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>')


def esc(s):
    return html.escape(s, quote=True)


def shell(title, body, depth):
    """A page of the notes. depth is the number of folders below docs/, 2 for notes/session2/x.html."""
    up = '../' * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{site.STYLE}{NOTES_STYLE}</style>
{MATHJAX}
<script src="{up}notes/notes.js" defer></script>
</head>
<body>
<main>
  <p class="course"><a href="{REPO}">Advanced Quantum Materials 2027</a> · <a href="{up}index.html">All lectures</a> · <a href="{up}notes/index.html">Lecture notes</a></p>
{body}
</main>
</body>
</html>
"""


def tabs(n, depth):
    """The three tabs of a session: the two lectures and the notes, the notes being the one that is on."""
    up = '../' * depth
    out = [f'<a href="{up}{f}/session{n}.html">{F["name"]}</a>' for f, F in site.FORMATS.items()]
    out.append(f'<a class="on" href="{up}notes/session{n}/index.html">Lecture notes</a>')
    return '  <nav class="tabs">' + ''.join(out) + '</nav>\n'


def session_row(sessions, built, n, depth):
    """The row of session numbers. A session whose notes are not built is shown, but it is not a link."""
    up = '../' * depth
    out = []
    for s in sessions:
        k = s['session']
        t = esc(s['title'])
        if k in built:
            out.append(f'<a class="{"on" if k == n else ""}" href="{up}notes/session{k}/index.html" title="{t}">{k}</a>')
        else:
            out.append(f'<span title="{t} (notes not on the page yet)">{k}</span>')
    return '  <nav class="sub">' + ''.join(out) + '</nav>\n'
