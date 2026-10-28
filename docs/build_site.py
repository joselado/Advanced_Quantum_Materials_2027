"""Builds the course webpage from sessions.json: the landing page index.html, split into the video lectures and the
landscape lectures, and one page per session and format in lectures/ and landscape/.

Run from anywhere with python3 docs/build_site.py after changing sessions.json. A session's video lecture is shown
when "lecture" is true in sessions.json; otherwise its page says the video is in preparation.
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
        'release': 'lectures',
        'blurb': ('The prerecorded lectures with slides that follow the voice. Each step of a calculation is written '
                  'when it is said. Next to the formulas there is a schematic or a plot, computed with the codes of '
                  'the course.'),
    },
    'landscape': {
        'name': 'Landscape lectures',
        'release': 'films',
        'blurb': ('A lighter version of the same lectures, with the same voice. There is less content on the screen, '
                  'and the physics is shown while we travel through 3D landscapes.'),
    },
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
  main { max-width: 960px; margin: 0 auto; padding: 28px 16px 64px; }
  h1 { font-size: 1.7rem; margin: 0 0 4px; line-height: 1.25; }
  h2 { font-size: 1.25rem; margin: 40px 0 8px; }
  h3 { font-size: 1.02rem; margin: 24px 0 4px; }
  a { color: var(--link); }
  .course { color: var(--muted); margin: 0 0 16px; }
  .tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--rule); margin: 16px 0 0; flex-wrap: wrap; }
  .tabs a { padding: 8px 14px; text-decoration: none; color: var(--muted); border-radius: 6px 6px 0 0; }
  .tabs a.on { color: var(--fg); background: var(--tab); font-weight: 600; }
  .sub { display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 0 20px; }
  .sub a { min-width: 2.4em; text-align: center; padding: 4px 8px; border: 1px solid var(--rule); border-radius: 6px;
           text-decoration: none; color: var(--fg); }
  .sub a.on { background: var(--accent); border-color: var(--accent); color: var(--bg); font-weight: 600; }
  .sub a.off { color: var(--muted); border-style: dashed; }
  video { width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: 6px; display: block; }
  .pending { width: 100%; aspect-ratio: 16 / 9; border: 1px dashed var(--rule); border-radius: 6px; display: flex;
             align-items: center; justify-content: center; color: var(--muted); text-align: center; padding: 16px; }
  .note { color: var(--muted); font-size: 0.95rem; }
  ul { padding-left: 1.3em; margin: 4px 0; }
  li { margin: 2px 0; }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 720px) { .cols { grid-template-columns: 1fr; } }
  .half { background: var(--card); border: 1px solid var(--rule); border-radius: 8px; padding: 4px 18px 16px; }
  .half h2 { margin-top: 14px; }
  .half ol { padding-left: 1.6em; margin: 8px 0; }
  .half li { margin: 4px 0; }
  .soon { color: var(--muted); }
  .pager { display: flex; justify-content: space-between; margin-top: 36px; padding-top: 12px;
           border-top: 1px solid var(--rule); gap: 12px; }
"""


def esc(s):
    return html.escape(s, quote=True)


def page(title, body, depth):
    up = '../' * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{STYLE}</style>
</head>
<body>
<main>
  <p class="course"><a href="{REPO}">Advanced Quantum Materials 2027</a> · <a href="{up}index.html">All lectures</a></p>
{body}
</main>
</body>
</html>
"""


def has_video(s, fmt):
    return s.get('lecture', False) if fmt == 'lectures' else True


def tabs(fmt, n):
    out = []
    for f, F in FORMATS.items():
        out.append(f'<a class="{"on" if f == fmt else ""}" href="../{f}/session{n}.html">{F["name"]}</a>')
    return '  <nav class="tabs">' + ''.join(out) + '</nav>\n'


def subtabs(fmt, sessions, n):
    out = []
    for s in sessions:
        k = s['session']
        cls = 'on' if k == n else ('' if has_video(s, fmt) else 'off')
        out.append(f'<a class="{cls}" href="session{k}.html" title="{esc(s["title"])}">{k}</a>')
    return '  <nav class="sub">' + ''.join(out) + '</nav>\n'


def bullets(head, items):
    if not items:
        return ''
    lis = ''.join(f'<li>{esc(i)}</li>' for i in items)
    return f'  <h3>{head}</h3>\n  <ul>{lis}</ul>\n'


def session_page(fmt, sessions, s):
    n, F = s['session'], FORMATS[fmt]
    b = tabs(fmt, n) + subtabs(fmt, sessions, n)
    b += f'  <h1>Session {n}. {esc(s["title"])}</h1>\n'
    if has_video(s, fmt):
        src = f'{RELEASE}/{F["release"]}/session{n}.mp4#t=0.1'
        b += f'  <video controls playsinline preload="metadata" src="{src}"></video>\n'
    else:
        b += '  <div class="pending">The video lecture of this session is not ready yet. The landscape lecture of this session is in the other tab.</div>\n'
    b += bullets('Learning outcomes', s.get('outcomes'))
    b += bullets('Contents', s.get('contents'))
    b += bullets('Simulations shown', s.get('simulations'))
    if fmt == 'landscape' and s.get('floating'):
        src = f'{RELEASE}/films-floating/session{n}.mp4#t=0.1'
        b += ('  <h2 id="floating">With floating formulas</h2>\n'
              '  <p class="note">A second version of the same film. When the voice talks over a still picture, short '
              'formulas and steps of the derivation float in the landscape.</p>\n'
              f'  <video controls playsinline preload="metadata" src="{src}"></video>\n')
    b += f'  <p class="note">Slides of this session: <a href="{REPO}/blob/main/slides_prerecordings/lecture{n}.pdf">lecture{n}.pdf</a>'
    if s.get('notebook'):
        b += f' · exercises: <a href="{REPO}/blob/main/jupyter-notebooks/session{n}.ipynb">session{n}.ipynb</a>'
    b += f' · <a href="{REPO}/blob/main/lecture_notes/main.pdf">lecture notes</a></p>\n'
    ns = [x['session'] for x in sessions]
    i = ns.index(n)
    prev = f'<a href="session{ns[i - 1]}.html">Session {ns[i - 1]}</a>' if i > 0 else '<span></span>'
    nxt = f'<a href="session{ns[i + 1]}.html">Session {ns[i + 1]}</a>' if i + 1 < len(ns) else '<span></span>'
    b += f'  <nav class="pager">{prev}{nxt}</nav>\n'
    return page(f'Session {n}, {F["name"].lower()}', b, 1)


def landing(sessions):
    b = '  <h1>Advanced Quantum Materials 2027</h1>\n'
    b += ('  <p>The ten lectures of the course are here in two versions, with the same recorded voice. The video '
          'lectures write every step of the calculations. The landscape lectures show the same physics with less '
          'on the screen. Each session has its own page, with the learning outcomes, the contents and the '
          'simulations of the lecture.</p>\n')
    b += '  <div class="cols">\n'
    for fmt, F in FORMATS.items():
        b += f'  <section class="half" id="{fmt}">\n    <h2>{F["name"]}</h2>\n    <p class="note">{F["blurb"]}</p>\n    <ol>\n'
        for s in sessions:
            n = s['session']
            if has_video(s, fmt):
                b += f'      <li value="{n}"><a href="{fmt}/session{n}.html">{esc(s["title"])}</a></li>\n'
            else:
                b += f'      <li value="{n}"><a class="soon" href="{fmt}/session{n}.html">{esc(s["title"])}</a> <span class="soon">(not ready yet)</span></li>\n'
        b += '    </ol>\n  </section>\n'
    b += '  </div>\n'
    b += ('  <section id="versions">\n    <h2>The rules each landscape film follows</h2>\n'
          '    <p class="note">The way we make the films changes from one film to the next. The chart shows which '
          'version of the rules each film follows.</p>\n'
          '    <img src="film_rules.png" alt="Matrix of films 1 to 10 against rule iterations v1 to v8" '
          'style="width:100%;height:auto">\n  </section>\n')
    # the old single-page links (index.html#session3, #session2-floating) land on the new pages
    b += ('  <script>\n    (function () {\n      var m = location.hash.match(/^#session(\\d+)(-floating)?$/);\n'
          '      if (m) location.replace("landscape/session" + m[1] + ".html" + (m[2] ? "#floating" : ""));\n'
          '    })();\n  </script>\n')
    return page('Advanced Quantum Materials 2027, lectures', b, 0).replace(
        '<p class="course"><a href="' + REPO + '">Advanced Quantum Materials 2027</a> · <a href="index.html">All lectures</a></p>',
        '<p class="course"><a href="' + REPO + '">Course repository on GitHub</a></p>')


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
    with open(os.path.join(HERE, 'sessions.json')) as f:
        sessions = json.load(f)
    for fmt in FORMATS:
        os.makedirs(os.path.join(HERE, fmt), exist_ok=True)
        for s in sessions:
            with open(os.path.join(HERE, fmt, f'session{s["session"]}.html'), 'w') as f:
                f.write(session_page(fmt, sessions, s))
    with open(os.path.join(HERE, 'index.html'), 'w') as f:
        f.write(landing(sessions))
    with open(os.path.join(HERE, 'lectures.html'), 'w') as f:
        f.write(old_lectures_page())
    print('wrote', 1 + 1 + len(FORMATS) * len(sessions), 'pages')


if __name__ == '__main__':
    main()
