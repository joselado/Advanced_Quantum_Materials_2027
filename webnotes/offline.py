"""Packs the site of docs/ as one zip, so that the notes can be downloaded and read without network.

    python3 webnotes/offline.py [--site DIR] [--out FILE] [--upload]

The zip holds the home page, the pages of the videos and the notes with their figures, scripts, widgets and MathJax.
It is unpacked anywhere and index.html is opened in a browser, with no server and no installation. The videos are
not inside, since they are several GB, and their pages play them from GitHub when there is a connection.

Run it after webnotes/build.py and docs/build_site.py. The same site gives the same file, byte by byte. With --upload
the zip goes to the release "offline" of the repository with gh, which is the file that the link "Download the site"
of every page points to, so it is run again after each change of docs/ that is pushed.
"""
import argparse
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'docs'))
import build_site as site

TOP = site.OFFLINE_ZIP[:-len('.zip')]
PARTS = ['index.html', 'lectures.html', 'lectures', 'landscape', 'notes']
README = f"""Advanced Quantum Materials 2027, the site of the course to read without network

Open index.html in a browser. Nothing has to be installed and no server is needed.

What works without network: the lecture notes of the ten sessions with their equations, figures, quizzes and
widgets with the precomputed curves, and the pyqula scripts of the plots in notes/scripts/.

What needs a connection: the videos of the lectures, the button "Run live in the browser" of the widgets, and the
links to the notebooks, to Colab and to the papers.

The scripts in notes/scripts/ run with python and pyqula (pip install pyqula).

The site online: https://joselado.github.io/Advanced_Quantum_Materials_2027/
The repository:  {site.REPO}
"""


def files(root):
    """The files of the site, as (path, name in the zip), sorted."""
    out = []
    for part in PARTS:
        a = os.path.join(root, part)
        if os.path.isfile(a):
            out.append((a, part))
        for r, dirs, fs in os.walk(a):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            out += [(os.path.join(r, f), os.path.relpath(os.path.join(r, f), root)) for f in fs
                    if not f.endswith('.pyc') and f != 'labels.json']
    return sorted(out, key=lambda x: x[1])


def pack(root, out):
    todo = files(root)
    for need in ('index.html', 'notes/index.html', 'notes/notes.js', 'notes/mathjax/tex-chtml.js'):
        if need not in {name for _, name in todo}:
            sys.exit(f'{need} is not in {root}, build the site first')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        def add(name, data):
            # a fixed date and fixed permissions, so that the same site gives the same zip
            info = zipfile.ZipInfo(f'{TOP}/{name}', date_time=(2027, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
        add('README.txt', README)
        for path, name in todo:
            with open(path, 'rb') as f:
                add(name.replace(os.sep, '/'), f.read())
    print(f'{out}: {len(todo) + 1} files, {os.path.getsize(out) / 1e6:.1f} MB')


def upload(out):
    tag = site.OFFLINE_TAG
    if subprocess.run(['gh', 'release', 'view', tag], cwd=ROOT, capture_output=True).returncode != 0:
        subprocess.run(['gh', 'release', 'create', tag, '--latest=false', '--title', 'Site to read without network',
                        '--notes', 'The site of the course as one zip. Unpack it and open index.html in a browser. '
                        'The notes work without network, and the videos play when there is a connection.'],
                       cwd=ROOT, check=True)
    subprocess.run(['gh', 'release', 'upload', tag, out, '--clobber'], cwd=ROOT, check=True)
    print(f'uploaded to {site.OFFLINE}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--site', metavar='DIR', default=os.path.join(ROOT, 'docs'), help='the built site, docs/ by default')
    ap.add_argument('--out', metavar='FILE', default=os.path.join(HERE, '.cache', site.OFFLINE_ZIP),
                    help='the zip to write, in webnotes/.cache/ by default, which git ignores')
    ap.add_argument('--upload', action='store_true', help='also upload the zip to the release of the repository')
    a = ap.parse_args()
    pack(os.path.abspath(a.site), a.out)
    if a.upload:
        upload(a.out)


if __name__ == '__main__':
    main()
