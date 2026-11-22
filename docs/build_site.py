"""Builds the course webpage from sessions.json: the landing page index.html, with one row per session, and one page
per session and recording in lectures/ (the video lecture with slides) and landscape/ (its landscape version).

Run from anywhere with python3 docs/build_site.py after changing sessions.json. A session's video lecture is shown
when "lecture" is true in sessions.json; otherwise its page says the video is in preparation. With --out DIR the pages
are written in DIR and docs/ does not change.

The shell of every page of the site is here: top() with chips(), session_head() with session_tabs(), pager(), footer()
and page(). The notes (webnotes/template.py) import them, so the navigation exists once.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = 'https://github.com/joselado/Advanced_Quantum_Materials_2027'
RELEASE = REPO + '/releases/download'

FORMATS = {
    'lectures': {
        'name': 'Video lectures',
        'mode': 'Slides',
        'release': 'lectures',
        'blurb': ('The prerecorded lectures with slides that follow the voice. Each step of a calculation is written '
                  'when it is said. Next to the formulas there is a schematic or a plot, computed with the codes of '
                  'the course.'),
    },
    'landscape': {
        'name': 'Landscape lectures',
        'mode': 'Landscape',
        'release': 'films',
        'blurb': ('A lighter version of the same lectures, with the same voice. There is less content on the screen, '
                  'and the physics is shown while we travel through 3D landscapes.'),
    },
}
FLOATING = {
    'mode': 'Landscape with floating formulas',
    'release': 'films-floating',
    'blurb': ('A second version of the landscape lecture. When the voice talks over a still picture, short formulas and '
              'steps of the derivation float in the landscape.'),
}

STYLE = """
  :root { --bg: #fbfbfa; --fg: #1d1d1f; --muted: #5f6368; --rule: #dadce0; --link: #1a5fb4;
          --card: #ffffff; --tab: #eef0f3; --accent: #1a5fb4; }
  @media (prefers-color-scheme: dark) {
    :root { --bg: #16171a; --fg: #e8e8ea; --muted: #a0a3a8; --rule: #33363b; --link: #8ab4f8;
            --card: #1e2024; --tab: #25282d; --accent: #8ab4f8; }
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--fg);
         font: 17px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }
  main { max-width: 1040px; margin: 0 auto; padding: 18px 16px 40px; }
  h1 { font-size: 1.7rem; margin: 0 0 4px; line-height: 1.25; }
  h2 { font-size: 1.25rem; margin: 40px 0 8px; }
  h3 { font-size: 1.02rem; margin: 24px 0 4px; }
  a { color: var(--link); text-underline-offset: 2px; }
  /* the shell: the bar of the course with the sessions, the head of a session with its two tabs, the footer */
  .top { display: flex; align-items: center; justify-content: space-between; gap: 8px 24px; flex-wrap: wrap;
         padding-bottom: 12px; border-bottom: 1px solid var(--rule); margin-bottom: 22px; }
  .brand { font-weight: 700; font-size: 1.05rem; color: var(--fg); text-decoration: none; }
  .brand span { color: var(--muted); font-weight: 400; }
  .sub { display: flex; gap: 5px; flex-wrap: wrap; align-items: center; }
  .sub .sublab { color: var(--muted); font-size: 0.9rem; margin-right: 4px; }
  .sub a, .sub span.no { min-width: 2.1em; text-align: center; padding: 2px 6px; border: 1px solid var(--rule);
           border-radius: 6px; text-decoration: none; color: var(--fg); font-size: 0.95rem; }
  .sub a:hover { border-color: var(--accent); }
  .sub a.on { background: var(--accent); border-color: var(--accent); color: var(--bg); font-weight: 600; }
  .sub a.off, .sub span.no { color: var(--muted); border-style: dashed; }
  .eyebrow { margin: 0; color: var(--muted); font-size: 0.82rem; font-weight: 700; letter-spacing: 0.07em;
             text-transform: uppercase; }
  .sess { margin: 0; font-weight: 600; font-size: 1.05rem; }
  .sess a { color: var(--fg); text-decoration: none; } .sess a:hover { text-decoration: underline; }
  .sess .k { color: var(--muted); font-weight: 400; }
  .tabs { display: flex; gap: 2px 22px; border-bottom: 1px solid var(--rule); margin: 10px 0 0; flex-wrap: wrap; }
  .tabs a, .tabs span { padding: 6px 1px 7px; text-decoration: none; color: var(--muted); border-bottom: 3px solid transparent;
            margin-bottom: -1px; }
  .tabs a:hover { color: var(--fg); }
  .tabs a.on { color: var(--fg); font-weight: 600; border-bottom-color: var(--accent); }
  .tabs span { opacity: 0.6; }
  .links { color: var(--muted); font-size: 0.93rem; margin: 10px 0 16px; }
  /* the version of a video lecture, slides or landscape, chosen above the video */
  .mode { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin: 4px 0 6px; }
  .mode .sublab { color: var(--muted); font-size: 0.9rem; margin-right: 4px; }
  .mode a { padding: 3px 14px; border: 1px solid var(--rule); border-radius: 999px; text-decoration: none; color: var(--fg);
            background: var(--card); font-size: 0.93rem; }
  .mode a:hover { border-color: var(--accent); }
  .mode a.on { background: var(--accent); border-color: var(--accent); color: var(--bg); font-weight: 600; }
  .modenote { color: var(--muted); font-size: 0.93rem; margin: 0 0 12px; }
  video { width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: 6px; display: block; }
  .pending { width: 100%; aspect-ratio: 16 / 9; border: 1px dashed var(--rule); border-radius: 6px; display: flex;
             align-items: center; justify-content: center; color: var(--muted); text-align: center; padding: 16px; }
  .note { color: var(--muted); font-size: 0.95rem; }
  ul { padding-left: 1.3em; margin: 4px 0; }
  li { margin: 2px 0; }
  .soon { color: var(--muted); }
  /* the home page: what the three formats are, then one row per session */
  .formats { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 40px; margin: 18px 0 8px; }
  @media (max-width: 800px) { .formats { grid-template-columns: 1fr; } }
  .formats h2 { font-size: 1rem; margin: 0 0 2px; }
  .formats p { margin: 0; color: var(--muted); font-size: 0.93rem; }
  .sessions { list-style: none; padding: 0; margin: 26px 0 0; border-top: 1px solid var(--rule); }
  .sessions > li { display: grid; grid-template-columns: 2.6rem 1fr; gap: 0 8px; padding: 14px 0; margin: 0;
                   border-bottom: 1px solid var(--rule); }
  .sessions .k { font-size: 1.5rem; font-weight: 700; color: var(--muted); line-height: 1.3; }
  .sessions h2 { font-size: 1.12rem; margin: 0 0 8px; line-height: 1.35; }
  .go { display: flex; flex-wrap: wrap; gap: 6px 8px; align-items: center; margin: 0; }
  .go a { text-decoration: none; padding: 3px 12px; border: 1px solid var(--rule); border-radius: 6px; background: var(--card);
          color: var(--link); font-size: 0.93rem; font-weight: 600; }
  .go a:hover { border-color: var(--accent); }
  .go a.minor { border-color: transparent; background: none; font-weight: 400; padding: 3px 4px; text-decoration: underline; }
  .go .soon { font-size: 0.93rem; padding: 3px 4px; }
  /* previous and next, with what each one is */
  .pager { display: grid; grid-template-columns: 1fr 1fr; margin-top: 40px; gap: 12px; }
  .pager a { display: block; border: 1px solid var(--rule); border-radius: 8px; padding: 8px 14px; text-decoration: none;
             background: var(--card); color: var(--fg); }
  .pager a:hover { border-color: var(--accent); }
  .pager a.next { text-align: right; grid-column: 2; }
  .pager small { display: block; color: var(--muted); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.07em;
                 text-transform: uppercase; }
  .pager .t { color: var(--link); }
  @media (max-width: 560px) { .pager { grid-template-columns: 1fr; } .pager a.next { grid-column: 1; } }
  .foot { margin-top: 48px; padding-top: 14px; border-top: 1px solid var(--rule); color: var(--muted); font-size: 0.88rem; }
  @media print {
    .top, .tabs, .pager, .foot, .secnav, .links, .mode, .modenote, video { display: none !important; }
    body { background: #fff; color: #000; font-size: 11.5pt; } main { max-width: none; padding: 0; }
    a { color: inherit; text-decoration: none; }
  }
"""

FAVICON = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E'
           '%3Cpath d=%27M16 3l11.3 6.5v13L16 29 4.7 22.5v-13z%27 fill=%27none%27 stroke=%27%231a5fb4%27 stroke-width=%273%27/%3E'
           '%3Ccircle cx=%2716%27 cy=%2716%27 r=%273.5%27 fill=%27%231a5fb4%27/%3E%3C/svg%3E">')


def esc(s):
    return html.escape(s, quote=True)


def top(up, chips=''):
    """The bar of every page of the site: the name of the course, which is the link to the home page, and the row of
    the sessions. up is the path from the page to docs/."""
    return (f'  <header class="top"><a class="brand" href="{up}index.html">Advanced Quantum Materials <span>2027</span></a>'
            f'{chips}</header>\n')


def chips(sessions, n, href, ready=lambda k: True, off=lambda k: False):
    """The row of the session numbers. href(k) is the page of session k in the format of the page we are on, a session
    that is not ready is shown without a link, and off(k) marks a page that exists but has no video yet."""
    out = ['<span class="sublab">Session</span>']
    for s in sessions:
        k, t = s['session'], esc(s['title'])
        if not ready(k):
            out.append(f'<span class="no" title="{t} (not on the page yet)">{k}</span>')
        else:
            cls = 'on' if k == n else ('off' if off(k) else '')
            cur = ' aria-current="true"' if k == n else ''
            out.append(f'<a class="{cls}" href="{href(k)}" title="{t}"{cur}>{k}</a>')
    return '<nav class="sub" aria-label="Sessions">' + ''.join(out) + '</nav>'


def session_tabs(n, on, up, notes=None):
    """The two views of session n, the video lecture and the notes. on is 'lectures', 'landscape' or 'notes'. The
    landscape lecture is a version of the video lecture, chosen above the video with modes(), so both recordings
    have the tab of the video lecture on. Every page of a session has the same tabs, from this one function."""
    video = on if on in FORMATS else 'lectures'
    out = [f'<a class="{"on" if on in FORMATS else ""}" href="{up}{video}/session{n}.html">Video lecture</a>']
    if has_notes(n) if notes is None else notes:
        out.append(f'<a class="{"on" if on == "notes" else ""}" href="{up}notes/session{n}/index.html">Lecture notes</a>')
    else:
        out.append('<span title="The notes of this session are not on the page yet">Lecture notes</span>')
    return '  <nav class="tabs" aria-label="Video lecture and notes of this session">' + ''.join(out) + '</nav>\n'


def modes(fmt, s):
    """The versions of the video lecture of a session, as a row of links above the video, and one line that says what
    the chosen version is. The landscape lecture with floating formulas is the landscape page with #floating, and the
    script of that page changes the video, the chosen link and the line when the hash changes."""
    n = s['session']
    out = ['<span class="sublab">Version</span>']
    for f, F in FORMATS.items():
        out.append(f'<a class="{"on" if f == fmt else ""}" data-mode="{f}" href="../{f}/session{n}.html">{F["mode"]}</a>')
    if s.get('floating'):
        out.append(f'<a data-mode="floating" href="../landscape/session{n}.html#floating">{FLOATING["mode"]}</a>')
    b = '  <nav class="mode" aria-label="Version of the video lecture">' + ''.join(out) + '</nav>\n'
    b += f'  <p class="modenote">{FORMATS[fmt]["blurb"]}</p>\n'
    return b


FLOATING_SCRIPT = """  <script>
    (function () {
      var video = document.querySelector('video'), note = document.querySelector('.modenote');
      var links = document.querySelectorAll('.mode a');
      var V = {landscape: [%s, %s], floating: [%s, %s]};
      function set() {
        var m = location.hash === '#floating' ? 'floating' : 'landscape';
        if (video.getAttribute('src') !== V[m][0]) video.setAttribute('src', V[m][0]);
        note.textContent = V[m][1];
        links.forEach(function (a) { a.classList.toggle('on', a.dataset.mode === m); });
      }
      window.addEventListener('hashchange', set);
      set();
    })();
  </script>
"""


def session_head(n, title, on, up, h1=True, notes=None):
    """The head of a page of session n: its number, its title and the two tabs. On a page of one section of the
    notes the title of the page is the section, so h1 is False and the session is a line that links to its notes."""
    if h1:
        b = f'  <p class="eyebrow">Session {n}</p>\n  <h1>{esc(title)}</h1>\n'
    else:
        b = f'  <p class="sess"><a href="index.html"><span class="k">Session {n}.</span> {esc(title)}</a></p>\n'
    return b + session_tabs(n, on, up, notes)


def pager(prev=None, nxt=None):
    """Previous and next. Each one is (href, title), or None at an end."""
    a = f'<a class="prev" href="{prev[0]}"><small>← Previous</small><span class="t">{prev[1]}</span></a>' if prev else ''
    b = f'<a class="next" href="{nxt[0]}"><small>Next →</small><span class="t">{nxt[1]}</span></a>' if nxt else ''
    return f'  <nav class="pager" aria-label="Previous and next">{a}{b}</nav>\n'


def footer(up):
    return (f'  <footer class="foot">Teaching material of the course Advanced Quantum Materials at Aalto University, 2027 · '
            f'<a href="{REPO}">Course repository on GitHub</a> · <a href="{up}notes/index.html">Contents of the notes</a> · '
            f'<a href="{REPO}/blob/main/lecture_notes/main.pdf">PDF of the notes</a></footer>\n')


def page(title, body, depth, head='', style=''):
    """A page of the site. body starts with top(). head and style are what the notes add."""
    up = '../' * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
{FAVICON}
<style>{STYLE}{style}</style>
{head}</head>
<body>
<main>
{body}{footer(up)}</main>
</body>
</html>
"""


def has_video(s, fmt):
    return s.get('lecture', False) if fmt == 'lectures' else True


def has_notes(n):
    # the notes of a session are on the page once webnotes/convert.py has written its manifest
    return os.path.exists(os.path.join(HERE, '..', 'webnotes', 'manifest', f'session{n:02d}.json'))


def bullets(head, items):
    if not items:
        return ''
    lis = ''.join(f'<li>{esc(i)}</li>' for i in items)
    return f'  <h3>{head}</h3>\n  <ul>{lis}</ul>\n'


def session_page(fmt, sessions, s):
    n, F = s['session'], FORMATS[fmt]
    by = {x['session']: x for x in sessions}
    b = top('../', chips(sessions, n, lambda k: f'session{k}.html', off=lambda k: not has_video(by[k], fmt)))
    b += session_head(n, s['title'], fmt, '../')
    b += f'  <p class="links">Slides <a href="{REPO}/blob/main/slides_prerecordings/lecture{n}.pdf">lecture{n}.pdf</a>'
    if s.get('notebook'):
        b += f' · Exercises <a href="{REPO}/blob/main/jupyter-notebooks/session{n}.ipynb">session{n}.ipynb</a>'
    b += f' · <a href="{REPO}/blob/main/lecture_notes/main.pdf">PDF of the notes</a></p>\n'
    b += modes(fmt, s)
    src = lambda release: f'{RELEASE}/{release}/session{n}.mp4#t=0.1'
    if has_video(s, fmt):
        b += f'  <video controls playsinline preload="metadata" src="{src(F["release"])}"></video>\n'
    else:
        b += ('  <div class="pending">The video lecture with slides of this session is not ready yet. The landscape '
              'version is ready, and it is chosen above.</div>\n')
    if fmt == 'landscape' and s.get('floating'):
        b += FLOATING_SCRIPT % tuple(json.dumps(x) for x in (src(F['release']), F['blurb'],
                                                             src(FLOATING['release']), FLOATING['blurb']))
    b += bullets('Learning outcomes', s.get('outcomes'))
    b += bullets('Contents', s.get('contents'))
    b += bullets('Simulations shown', s.get('simulations'))
    ns = [x['session'] for x in sessions]
    i = ns.index(n)
    link = lambda k: (f'session{k}.html', f'Session {k}. {esc(by[k]["title"])}')
    b += pager(link(ns[i - 1]) if i > 0 else None, link(ns[i + 1]) if i + 1 < len(ns) else None)
    return page(f'Session {n}, {"video lecture" if fmt == "lectures" else "landscape lecture"}', b, 1)


def landing(sessions):
    b = top('', chips(sessions, 0, lambda k: f'#s{k}'))
    b += '  <h1>Advanced Quantum Materials 2027</h1>\n'
    b += ('  <p>The ten lectures of the course are here as two recorded versions with the same voice, and as written '
          'notes. Each session has its own page, with the learning outcomes, the contents and the simulations of the '
          'lecture, so the whole course can be studied from this site.</p>\n')
    b += '  <div class="formats">\n'
    b += (f'    <section id="lectures"><h2>Video lectures</h2><p>{FORMATS["lectures"]["blurb"]} <span id="landscape">Each '
          'lecture has a second version, the landscape lecture, which is chosen above the video. It is lighter, with '
          'less content on the screen, and the physics is shown while we travel through 3D landscapes.</span></p></section>\n')
    b += ('    <section id="notes"><h2>Lecture notes</h2><p>The written version of the lectures, with the equations of the '
          'PDF. Each session is split in pages of one section, and the boxes point to the notebook of the session.</p>'
          '</section>\n  </div>\n')
    b += '  <ol class="sessions">\n'
    for s in sessions:
        n = s['session']
        b += f'    <li id="s{n}"><span class="k">{n}</span><div><h2>{esc(s["title"])}</h2><p class="go">'
        video = 'lectures' if has_video(s, 'lectures') else 'landscape'
        b += f'<a href="{video}/session{n}.html">Video lecture</a>'
        if has_notes(n):
            b += f'<a href="notes/session{n}/index.html">Lecture notes</a>'
        else:
            b += '<span class="soon">Lecture notes (not ready yet)</span>'
        if s.get('notebook'):
            b += f'<a class="minor" href="{REPO}/blob/main/jupyter-notebooks/session{n}.ipynb">Notebook</a>'
        b += f'<a class="minor" href="{REPO}/blob/main/slides_prerecordings/lecture{n}.pdf">Slides</a>'
        b += '</p></div></li>\n'
    b += '  </ol>\n'
    b += ('  <p class="note"><a href="notes/index.html">Contents of the notes</a> · '
          f'<a href="{REPO}/blob/main/lecture_notes/main.pdf">PDF of the notes</a></p>\n')
    # the old single-page links (index.html#session3, #session2-floating) land on the new pages
    b += ('  <script>\n    (function () {\n      var m = location.hash.match(/^#session(\\d+)(-floating)?$/);\n'
          '      if (m) location.replace("landscape/session" + m[1] + ".html" + (m[2] ? "#floating" : ""));\n'
          '    })();\n  </script>\n')
    return page('Advanced Quantum Materials 2027, lectures', b, 0)


def old_lectures_page():
    # lectures.html was the single page of the video lectures; its links keep working
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Video lectures</title>
<script>
  var m = location.hash.match(/^#session(\\d+)$/);
  location.replace(m ? "lectures/session" + m[1] + ".html" : "index.html#lectures");
</script>
</head>
<body><p><a href="index.html#lectures">Video lectures</a></p></body>
</html>
"""


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', metavar='DIR', help='private build: write the pages in DIR instead of docs/')
    out = os.path.abspath(ap.parse_args().out or HERE)
    with open(os.path.join(HERE, 'sessions.json')) as f:
        sessions = json.load(f)
    for fmt in FORMATS:
        os.makedirs(os.path.join(out, fmt), exist_ok=True)
        for s in sessions:
            with open(os.path.join(out, fmt, f'session{s["session"]}.html'), 'w') as f:
                f.write(session_page(fmt, sessions, s))
    pages = {'index.html': landing(sessions), 'lectures.html': old_lectures_page()}
    for name, text in pages.items():
        with open(os.path.join(out, name), 'w') as f:
            f.write(text)
    print('wrote', len(pages) + len(FORMATS) * len(sessions), 'pages in', out)


if __name__ == '__main__':
    main()
