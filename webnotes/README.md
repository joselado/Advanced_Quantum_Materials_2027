# Web notes toolkit

This toolkit builds the lecture notes as web pages in `docs/notes/`. The plan is
`lecture_notes/WEB_NOTES_PLAN.md` and the tracker is `lecture_notes/WEB_NOTES_PROGRESS.md`. It needs
pandoc 3, python3 and `pdftocairo`. The math check also needs node, as we will now see.

## How to run it

To rebuild the pages we run one command, and the checks run at its end.

```
python3 webnotes/build.py
```

The keyword `--session N` builds only the pages of one session, `--check-only` runs the checks on the
existing build, and `--serve` serves `docs/` on `localhost:8000` after the build. The build is
idempotent, so a second run changes nothing in `docs/`.

### Private builds

When several people work at the same time, each one builds in a folder of their own with `--out`. The
pages, `labels.json`, the figures, `notes.js` and `notes.css` are written in that folder, nothing in `docs/`
or in `webnotes/labels.json` changes, and the checks and the math check run on that folder. A link that
leaves the folder, to the video lectures or to the home page, is looked for in `docs/notes/`.

```
python3 webnotes/build.py --out /tmp/mynotes --math
google-chrome --headless --no-sandbox --virtual-time-budget=6000 --window-size=1000,3000 \
  --screenshot=/tmp/page.png file:///tmp/mynotes/session2/05-blochs-theorem-and-the-first-band-structure.html
```

With `--session N` only that session is written, and a link to another session is not an error. The Markdown
in `pages/` is shared, so a build also shows the unfinished edit of somebody else. The default build, with no
`--out`, is the one that updates `docs/notes/`, and only the coordinator runs it.

## The math check

The pages render the math in the browser with MathJax 3.2.2. The math check renders every fragment of
`docs/notes/` with the same version and the same TeX configuration, in node, and lists each fragment that
gives an error, with its page and its text. It needs node and one local package, installed once with the
command below. The packages stay in `webnotes/mathcheck/node_modules/`, which git ignores.

```
cd webnotes/mathcheck && npm install
```

After a build we run it with the command below, which is the same as `node webnotes/mathcheck/check.js`
plus the other checks. Without node or without the package, `build.py` skips the math check and says so.

```
python3 webnotes/build.py --check-only --math
```

The check does not load the `noundefined` package of the page, so an unknown macro is an error here, while
on the page it would show in red. A macro that is missing is fixed in `MATHJAX` of `template.py`, and a
mistake in the TeX of a fragment is fixed in the Markdown of the page. KaTeX is not checked, since the pages
use only MathJax.

## Converting a session

The conversion of a session from the LaTeX is done once, with the command below. It writes the Markdown of
the session in `pages/sessionNN/`, its frozen list of pages in `manifest/sessionNN.json` and its line in
`SYNC`. It refuses to overwrite a converted session, since from then on the Markdown is the master. The
keyword `--force` regenerates it and loses the web edits.

```
python3 webnotes/convert.py --session N
```

After a conversion or a change of the video pages that links the notes, we also run
`python3 docs/build_site.py`, which adds the link "Notes of this session" to the video pages of every
session that has a manifest.

## What is in the Markdown

The pages are plain pandoc Markdown, so any editor reads them. The numbers are written in the file, so
they do not move when the file is edited.

- A heading carries `{#sec-2-5 number="2.5"}`. The build writes the number before the title.
- A numbered display equation ends with `\tag{2.8}`. The build derives the anchor `eq-2-8` from the tag.
  A new equation takes the number before it with a letter, `\tag{2.8a}`, and a removed one leaves a gap.
- A figure is `![caption](figures/s02f02_cosband.svg){#fig:s02:cosband number="2.2"}`. The build adds
  "Figure 2.2." to the caption and converts `lecture_notes/src/figures/pdf/s02f02_cosband.pdf` by its date.
- A reference is a link to an anchor, `[(2.8)](#eq-2-8)`, `Section [2.11](#sec-2-11)`. The build points it
  to the page that holds the anchor, also in another session. If the session of the anchor is not built yet,
  the text stays without the link and `check.py` lists it as pending.
- The box `notebookbox` is a fenced div as converted. The blocks `quiz`, `tryit`, the schematics, the figures
  shown again and the merge and split of pages are described in the next sections. The block `widget` is described in
  `widgets/README.md`.

## Blocks added for the web

A page that has one of these blocks links `notes.css`, and a page without them is the same file as before.
Every error of a block is listed by the build with the page, and the examples below are copy-paste.

### Schematics made for the web

A figure that exists only on the web is a script `webnotes/figures/sessionNN/NAME.py` that writes
`NAME.svg` next to it. The module `webnotes/figures/style.py` gives the look of the converted figures, which
is Computer Modern text as outlines, the dark blue `style.ACCENT` for the main curve, `style.BROKEN` red for
the second, light grey guide lines, thin axes with an arrow head and no box, and a white background. The SVG is
committed, and the build runs the script again when the SVG is older than the script or than `style.py`.

```python
"""Session 2, the chain band and its fold."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
import style

fig, ax = style.figure(height_cm=5.2)            # 14.6 cm wide; ncols=2 gives two axes
k = np.linspace(-np.pi, np.pi, 400)
ax.plot(k, -2 * np.cos(k), color=style.ACCENT)
style.guide(ax, y=0)
style.arrows(ax, xlabel=r'$\varphi$', ylabel=r'$\epsilon$')
style.label(ax, 0, -2.7, r'$\epsilon_\varphi=-2t\cos\varphi$')
style.save(fig, __file__)
```

The Markdown is the line below. The id `sch:sNN:name` is required, with the session number of the page. The
build numbers the schematics of a session in the order of the pages, so that they never collide with the
numbers of the PDF figures. They have their own counter, "Schematic 2.1", "Schematic 2.2", and an anchor
`sch:s02:name`. Nobody writes the number. The `alt` is required and describes what is drawn, the caption says
what to learn from it. Both follow the voice rules.

```
![Caption, in the voice of the notes.](figures/web/session02/chain_fold.svg){#sch:s02:chain_fold alt="One sentence that says what is drawn."}
```

A reference is the link with an empty text, `[](#sch:s02:chain_fold)`, which becomes "Schematic 2.1" with the link.
A missing script and SVG, a failing script, a missing id and a missing alt are errors.

### Quiz

A multiple-choice question with 3 or 4 options. Each option starts with `[x]` for the correct one or `[ ]`,
with exactly one `[x]`. The text before the list is the question, and the text after the list is the explanation.
Without JavaScript the options are a list and the answer is in a `<details>`. With `notes.js` the options are
buttons, a wrong one is marked and can be tried again, and the right one opens the explanation. Math works.

```
::: quiz
Which energy has the state with $\varphi=\pi/2$ in the band of [(2.8)](#eq-2-8)?

- [ ] $-2t$
- [x] $0$
- [ ] $2t$

At $\varphi=\pi/2$ the cosine vanishes, so $\epsilon_\varphi=0$. This is the middle of the band.
:::
```

### Try it

A short task that points to a notebook of `jupyter-notebooks/`. The build writes the links to GitHub, Colab and
Binder of the repository `joselado/Advanced_Quantum_Materials_2027` on `main`. `notebook` is required, and the
build checks that the file exists. `cell` is optional, and it is checked to be a heading of a markdown cell.

```
::: {.tryit notebook="session2.ipynb" cell="One dimensional chain"}
Change the hopping t in the notebook and check that the width of the band is 4t.
:::
```

Binder needs a `requirements.txt` or `binder/` folder in the repository to install pyqula, and there is none yet.

### A converted figure shown again, and one panel of it

A figure of the PDF notes can be shown on another page, of the same session or of another. Write the image with
the same file and no id. The display keeps the number of the original, "Figure 2.2, shown again.", links back
to it, and has no anchor of its own, so nothing is duplicated. The caption after the number is yours, and it may
be empty, but then the `alt` is required.

```
![The chain band, now used to read the quasi-momentum.](figures/s02f02_cosband.svg){alt="A cosine band with its density of states."}
```

A Blender figure is made of one render per panel, with the labels drawn on top by TikZ. The converted SVG keeps
each render and the labels around it in the order of the overlay, so `panel="NAME"` cuts the SVG to one panel,
with its labels and without the others (`figures/panel/NAME_panel.svg`, about 70 kB, no PNG needed). The names
of the panels are the endings of the render files, which are `a`, `b` for `s06f02_dimer`, and `chains`, `log`
for `s09f05_decay`, and the build lists them when a name is wrong. The caption starts "Figure 6.2, one panel
shown again.".

```
![Superexchange between two sites.](figures/s06f02_dimer.svg){panel="a" alt="Two sites with parallel and with antiparallel spins."}
```

## Merging and splitting pages

The URL of a page is its file name in the manifest, and a URL that existed must keep working.
`manifest/frozen_urls.txt` lists all of them, `check.py` needs each one to be a page or a redirect, and
`python3 webnotes/build.py --freeze` adds the URLs of today to it (the coordinator does it after adding pages).

A merge puts several sections on one page. In the Markdown of the page that stays, append the file of the
other section and keep its heading with its own id and number, so that all anchors stay. Delete the old file
with `git rm`. In `manifest/sessionNN.json` remove the old page, add it to the kept one as `also`, and list its
old URL in `redirects` of the manifest, which is a key next to `pages`. The build writes a stub with a meta
refresh and a canonical link at the old URL. The contents and the pager show the sections of `also` as extra
rows with their anchors, and the later sections of the page start with a rule.

```
{"file": "03-symmetry-operators-in-a-formal-way.md", "id": "sec-2-3", "number": "2.3", "title": "...",
 "also": [{"id": "sec-2-4", "number": "2.4", "title": "Exercises where we guess eigenstates from symmetry only"}]}
...
"redirects": [{"from": "04-exercises-where-we-guess-eigenstates-from-symmetry-only.html",
               "to": "03-symmetry-operators-in-a-formal-way.html#sec-2-4"}]
```

A split puts one section on two pages. The first page keeps its file, its URL and its anchor `sec-2-5`, and its
number becomes `2.5a` in the heading and in the manifest. The second part is a new file `05b-slug.md` that
starts with its own heading, a clear part title with the anchor `sec-2-5b` and `number="2.5b"`, and it gets
its own entry in `pages` just after the first one. `Section [2.5](#sec-2-5)` keeps pointing to the first part.
No redirect is needed, since no URL was retired.

```
## Bloch's theorem, the second part, the dispersion {#sec-2-5b number="2.5b"}
```

`check.py` verifies that every id of the manifest is a heading of its page, that a redirect points to a page of
the manifest and to an anchor that exists, that a redirect is not also a page, and that no frozen URL is lost.

## Rules of the checks added

An image with no alt text is an error, also in a converted figure. The alt of a converted figure is the first
sentence of its caption, and a figure shown again or a schematic takes the attribute `alt`.

## Carrying over changes of the lecture notes

`SYNC` holds, for each session, the commit of `lecture_notes/src` that the Markdown was last
brought in line with. The command `python3 webnotes/texdiff.py` compares `sessionNN.tex` and
the figure files `sNNf*` with that commit, paragraph by paragraph, and lists what changed. For
each change it prints the differing lines and a guess of the page that holds the old text,
found by searching pieces of it in `pages/`, so it still works when sections are merged or split.
The option `-s N` selects a session and `--stat` gives one line per session. When the changes are
applied, `python3 webnotes/texdiff.py --mark-synced -s N` sets the SYNC line to HEAD. A page
reported as not found means the text is new or was reworded on the web.

## Files

- `convert.py`, `filters/tex2md.lua`, the one-time conversion from the LaTeX.
- `build.py`, `filters/web.lua`, `template.py`, the build, with `--out DIR` for a private build. The look is imported from `docs/build_site.py`.
- `check.py`, the checks of `docs/notes/`, which are missing files and anchors, missing images, "??", LaTeX
  left outside the math, equation numbers used twice and pages without a source in the manifest.
- `labels.json`, the map from anchor to page, written by the first pass of the build.
- `pages/`, `manifest/`, `SYNC`, the Markdown master, the frozen URLs and the commit of the `.tex` each
  session was last synced to.
- `mathcheck/check.js`, `mathcheck/package.json`, the math check above.
- `widgets/notes.js`, `widgets/notes.css`, the shared script of the pages and the style of the added blocks,
  copied to `docs/notes/`. The CSS is linked only by a page that has one of those blocks.
- `widgets/defs/`, `widgets/data/`, `widgets/blocks/`, `widgets/precompute.py`, the ten widgets, see `widgets/README.md`.
- `figures/style.py`, `figures/sessionNN/NAME.py`, the web schematics and their common look.
- `manifest/frozen_urls.txt`, the URLs that must not disappear.
