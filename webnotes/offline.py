"""Packs the web notes of docs/notes/ as one zip, so that they can be downloaded and read without network.

    python3 webnotes/offline.py [--site DIR] [--out FILE] [--upload]

The zip holds only the notes: their pages with the figures, the scripts, the widgets and MathJax. It is unpacked
anywhere and index.html, the contents of the notes, is opened in a browser, with no server and no installation.
The videos and their pages are not inside. A link of a page that leaves the notes, which is the name of the course
and the tab "Video lecture", points to the site online.

Run it after webnotes/build.py and docs/build_site.py. The same notes give the same file, byte by byte. With --upload
the zip goes to the release "offline" of the repository with gh, which is the file that the link "Download the
notes" of every page points to, so it is run again after each change of docs/notes/ that is pushed.
"""
import argparse
import os
import re
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'docs'))
import build_site as site

TOP = site.OFFLINE_ZIP[:-len('.zip')]
ONLINE = 'https://joselado.github.io/Advanced_Quantum_Materials_2027/'
README = f"""Advanced Quantum Materials 2027, the lecture notes to read without network

Open index.html in a browser. Nothing has to be installed and no server is needed.

What works without network: the lecture notes of the ten sessions with their equations, figures, quizzes and
widgets with the precomputed curves, and the pyqula scripts of the plots in scripts/.

What needs a connection: the videos of the lectures, which are not in this folder and stay on the site, the button
"Run live in the browser" of the widgets, and the links to the notebooks, to Colab and to the papers.

The scripts in scripts/ run with python and pyqula (pip install pyqula).

The site online, with the videos: {ONLINE}
The repository: {site.REPO}
"""


def files(notes):
    """The files of the notes, as (path, name in the zip), sorted."""
    out = []
    for r, dirs, fs in os.walk(notes):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        out += [(os.path.join(r, f), os.path.relpath(os.path.join(r, f), notes).replace(os.sep, '/')) for f in fs
                if not f.endswith('.pyc') and f != 'labels.json']
    return sorted(out, key=lambda x: x[1])


def alone(html, name):
    """A page of docs/notes/ as a page of the zip, where the folder of the notes is the top one. A link to
    docs/notes/ through the folder above (../../notes/notes.js) becomes a link inside the zip, and a link that leaves
    the notes (../../index.html, ../../lectures/session2.html) becomes a link to the site online."""
    depth = name.count('/') + 1
    up = '../' * depth

    def fix(m):
        url = m.group(2)
        if url.startswith(up + 'notes/'):
            url = '../' * (depth - 1) + url[len(up + 'notes/'):]
        elif url.startswith(up):
            url = ONLINE + url[len(up):]
        return f'{m.group(1)}="{url}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, html)


def pack(root, out):
    notes = os.path.join(root, 'notes')
    todo = files(notes)
    for need in ('index.html', 'notes.js', 'mathjax/tex-chtml.js'):
        if need not in {name for _, name in todo}:
            sys.exit(f'notes/{need} is not in {root}, build the site first')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        def add(name, data):
            # a fixed date and fixed permissions, so that the same notes give the same zip
            info = zipfile.ZipInfo(f'{TOP}/{name}', date_time=(2027, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
        add('README.txt', README)
        for path, name in todo:
            with open(path, 'rb') as f:
                data = f.read()
            add(name, alone(data.decode(), name).encode() if name.endswith('.html') else data)
    print(f'{out}: {len(todo) + 1} files, {os.path.getsize(out) / 1e6:.1f} MB')


def upload(out):
    tag = site.OFFLINE_TAG
    if subprocess.run(['gh', 'release', 'view', tag], cwd=ROOT, capture_output=True).returncode != 0:
        subprocess.run(['gh', 'release', 'create', tag, '--latest=false', '--title', 'Lecture notes to read without network',
                        '--notes', 'The web notes of the course as one zip. Unpack it and open index.html in a browser. '
                        'The notes work without network. The videos are not inside, they stay on the site.'],
                       cwd=ROOT, check=True)
    subprocess.run(['gh', 'release', 'upload', tag, out, '--clobber'], cwd=ROOT, check=True)
    print(f'uploaded to {site.OFFLINE}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--site', metavar='DIR', default=os.path.join(ROOT, 'docs'), help='the built site, docs/ by default; its folder notes/ is packed')
    ap.add_argument('--out', metavar='FILE', default=os.path.join(HERE, '.cache', site.OFFLINE_ZIP),
                    help='the zip to write, in webnotes/.cache/ by default, which git ignores')
    ap.add_argument('--upload', action='store_true', help='also upload the zip to the release of the repository')
    a = ap.parse_args()
    pack(os.path.abspath(a.site), a.out)
    if a.upload:
        upload(a.out)


if __name__ == '__main__':
    main()
