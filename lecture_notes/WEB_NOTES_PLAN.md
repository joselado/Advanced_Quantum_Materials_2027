# Plan for the lecture notes as web pages

This file is the plan for putting the lecture notes on the course webpage, next to the videos, as
pages and subpages with the equations, the figures and the cross-references working, so that a
student can study the whole course from the webpage alone. It is written for a session that
starts with no other context. It fixes the target, the pipeline, the toolkit that later sessions
will build and use, the order of the work, and the decisions the lecturer took on 2026-11-06,
which are listed at the end. The tracker is `lecture_notes/WEB_NOTES_PROGRESS.md`, and it says
which phase comes next.

The lecturer fixed three things on 2026-11-06. The web pages do not have to be identical to the
lecture notes, in their words "the webpage materials does not have to be identical to the lecture
notes, we can make modifications fitting for the webpage, as zeroth order the lecture notes
material is good, but we may tweak things to improve their pedagogical value, maybe adding
quizzes, etc". A software toolkit may be built if it makes the iteration easier, "in case is
needed to develop some software toolkit for this to iterate easier in the future, we can of
course do it". And every new sentence written for the web, a quiz, a check or a box, follows
`VOICE.md` and `lecture_notes/writing_style.md`, since it is prose of the notes.

## What exists today

The site is `docs/`, served by GitHub Pages from the branch `main` and the folder `/docs` in the
legacy mode, with no Actions workflow tracked in the repository (checked with the Pages API on
2026-11-06, `build_type: legacy`, `source: main:/docs`). The file `docs/.nojekyll` is present, so
Jekyll does not touch the pages. The build is local. `docs/build_site.py` reads
`docs/sessions.json` and writes `docs/index.html`, `docs/lectures/sessionN.html` and
`docs/landscape/sessionN.html`, and the result is committed. The notes pages follow the same
rule, a local build whose output is committed, which is what the lecturer decided.

The notes are `lecture_notes/src/main.tex`, which inputs `preamble.tex`, `figures_preamble.tex`
and `sessions/session01.tex` to `session10.tex`. The compiled result is `lecture_notes/main.pdf`.
The LaTeX they use is small, and this is what makes the conversion possible. The sessions use
`\chapter`, `\section` (145 of them) and three `\subsection`, the environments `equation` (146,
numbered) and `equation*` (33), `itemize`, `enumerate`, `pmatrix`, `cases`, `aligned`, two
`tabular` tables, `\emph`, `\textbf`, `\texttt`, and the two custom things of `preamble.tex`,
the `notebookbox` callout, a `tcolorbox` with a title that names the notebook and its section,
and the two markers `\slidesonly` and `\transcriptonly`, which are not used in any session. Each
session inputs five or six figure files `figures/sNNfMM_name.tex`. Every one of the 59 figure
files is the `aqmfigure` environment of `figures_preamble.tex` with a label, a caption and one
`\includegraphics` of `figures/pdf/sNNfMM_name.pdf`, the Blender render with its TikZ overlay of
labels. There is no TikZ drawing left in the figure files, so a TikZ to SVG step is not needed.
There are no citations, no footnotes and no `\label` outside the figures.

The cross-references are the main constraint. The 64 `\ref` all point to figures, and four of
them cross sessions, since session 8 refers to `fig:s06:magnon` and `fig:s06:frustration`.
Everything else is written as plain text. There are 521 equation references written as `(2.8)`,
146 section references written as `Section 2.11`, and 108 `session N`. The numbering of the web
pages has to reproduce the numbering of the PDF exactly, chapter by chapter, or these strings go
stale. The PDF numbers equations as `chapter.n` with `\numberwithin{equation}{chapter}`. The
check of 2026-11-06 showed that counting `\begin{equation}` in each session file gives the
highest equation number printed in that chapter of `main.pdf`, for all ten chapters (10, 21, 9,
16, 23, 10, 12, 21, 12, 12), so a build that counts the numbered equations in order reproduces
the PDF.

## The target

The notes become a third part of the site, `docs/notes/`, in the look of the existing pages,
with the same colors, the same header line and the same tabs. Nothing of `docs/lectures/` and
`docs/landscape/` changes except one added link to the notes of the session.

The pages are the following.

- `docs/notes/index.html`, the table of contents of the whole course, one block per session
  with its sections.
- `docs/notes/sessionN/index.html`, the page of session N. It has the introduction of the
  chapter, the text before the first section, the list of the sections, and the links to the
  video lecture, the landscape lecture, the notebook `sessionN.ipynb` and the PDF.
- `docs/notes/sessionN/KK-slug.html`, one page per section, for instance
  `notes/session2/05-blochs-theorem-and-the-first-band-structure.html`. The page has the
  section with its subsections, its equations, figures and notebook boxes, the quiz and widget
  blocks added for the web, and a pager with the previous and the next section. The last
  section of a session points to the next session.
- `docs/notes/figures/sNNfMM_name.svg`, the figures.
- `docs/notes/notes.js`, the small scripts for the quizzes and the widgets, shared by all
  pages. The style is inline in each page, as in the existing pages, taken from the `STYLE` of
  `docs/build_site.py` with the few rules the notes add.

The navigation is the header line of the site, then the row of session numbers as on the video
pages, then the title of the session as a link back to its page, then the section. Equation
references `(2.8)` become links to the equation, also across sessions, section references
`Section 2.11` become links to the section page, figure references become links to the figure on
its page, and the notebook name in a notebook box links to the notebook on GitHub. The video
pages get a link "Notes of this session" next to the slides and the notebook.

## The pipeline, and what the test showed

The recommendation is pandoc with one Lua filter, assembled by a Python script, with MathJax in
the browser and the figures converted by `pdftocairo`. The reason is that pandoc read all ten
sessions with the two preambles with zero warnings, expanded the `\newenvironment` of
`aqmfigure` and the `tcolorbox` of `notebookbox` into a `<figure>` and a `<div>` by itself, kept
the `equation` environments, the tables and the quotes, and left nothing for a filter except
the numbering, the box title and the figure file name. The test ran on 2026-11-06 in the
scratchpad `webnotes_test/` of this session, with a prototype of the filter and of the build.
The filter becomes `filters/tex2md.lua` of the toolkit in phase 1, with the output changed from
HTML to Markdown, since the lecturer decided that the first conversion writes a web Markdown
master in `webnotes/pages/` and the pages are built from that master from then on. The test
converted to HTML directly, and the Markdown writer of pandoc was not run on the notes, so the
first thing phase 1 checks is that `pandoc -t markdown` keeps the math, the tables and the
fenced divs of the boxes as cleanly as the HTML writer did.

The installed tools are pandoc 3.8 (from the anaconda environment), make4ht 0.3m with tex4ht,
lwarp 0.915, dvisvgm 3.2.1, pdftocairo 24.02, inkscape, pdflatex of TeX Live 2023, node 18 with
npm, python3.14 with PyMuPDF and Pillow, and headless Chrome. LaTeXML, plasTeX, pylatexenc,
TexSoup and panflute are not installed.

What worked, with the numbers of the test.

- Pandoc converted the ten sessions in one command each, `pandoc -f latex -t html5 --mathjax
  --wrap=none --lua-filter aqm.lua -M chapter=N` on a four-line wrapper that inputs the two
  preambles and the session. With `--wrap=none` there is no LaTeX command left outside the math
  spans in any page.
- The Lua filter numbers the sections `C.K`, counts the `equation` environments and appends
  `\tag{C.n}` to each, numbers the figures `C.m` and rewrites the `\ref` links, turns the first
  span of a `notebookbox` into its title "Notebook check-in: session2.ipynb, ..." with the
  notebook linked, drops the `adjustbox` wrapper that pandoc leaves as a stray paragraph
  `max width=`, and points the image to `../figures/name.svg`.
- MathJax 3 rendered all 1099 math fragments of the 156 pages with zero errors, checked with the
  node API of `mathjax-full`. The constructs that matter are `\tag`, `\boxed`, `pmatrix`,
  `cases`, `aligned`, `\rm`, `\text`, `\big`, `\Big`, `\tfrac`, `\boldsymbol` and `\underbrace`.
  KaTeX 0.16 rendered all of them too once the `\label{}` that the prototype puts inside the
  math is removed, since KaTeX has no `\label`. So both renderers are possible. Note that the
  node check loads every MathJax package at once, while the browser build loads them on
  demand, so the screenshot of one page is the only evidence from a browser.
- `pdftocairo -svg` turns a figure PDF into an SVG of about 150 kB that keeps the embedded JPEG
  of the render and the labels as glyph outlines, so there is no font dependency. All 59 figures
  give 8.9 MB. A PNG at 200 dpi is about 110 kB per figure. The rendered SVG was checked by eye
  and matches the PDF.
- A headless Chrome screenshot of the page of Section 2.5 showed the numbered equations, the
  links `(2.5)`, `(2.7)`, `(2.8)`, Figure 2.2 with its caption, two notebook boxes, in the dark
  mode of the site.

What broke, with the error text.

- `make4ht main.tex "mathjax"` fails with 100 errors in the TeX pass. The first is `! Missing
  endcsname inserted` inside `figures/s01f01_fockspace.tex`, followed by `Argument of
  __file_name_expand_cleanup:Nw has an extra }` and `Use of ??? doesn't match its definition`,
  which is tex4ht failing on the file name of `\includegraphics{figures/pdf/...pdf}` inside the
  `adjustbox`. It is fatal, no HTML is written.
- `lwarpmk html` first needs a `pdflatex` pass to write `lwarpmk.conf`, and then stops at the
  same line with `! LaTeX Error: File 'figures/pdf/s01f01_fockspace' not found`, since lwarp
  strips the extension and wants its own converted images from `lwarpmk pdftosvg`. It was not
  pursued further, since it needs the document modified with `\usepackage{lwarp}` and a second
  pipeline for the images, for the same result pandoc gives in one command.
- `dvisvgm --pdf` drops the embedded raster of the figure PDFs. The SVG has the glyph outlines
  of the labels and nothing else, so it is not usable for these figures.
- LaTeXML and plasTeX were not tested, since they are not installed. LaTeXML is the one
  alternative that would also handle a future TikZ figure natively, so it stays the fallback if
  pandoc ever meets a construct it does not read.

Two things the prototype does not do, and the toolkit must. The label map has to be global
across sessions, since session 8 refers to two figures of session 6 and session 2 refers to
equation `(1.6)` of session 1. The prototype printed `??` for the four cross-session figure
references and left `(1.6)` as plain text. And twelve of the 75 figure references point to a
figure on another subpage of the same session, so the link needs the page of the figure and not
only its anchor. The fix is a two-pass build, first collect every label with its session, page
and display number, then convert.

The rule for the toolkit, learned in the test, is that everything that changes the content runs
inside the Lua filter on the pandoc tree, and the Python script only assembles pages. A regular
expression on the HTML broke once already, when pandoc wrapped a `<span class="math">` over two
lines, and `--wrap=none` is set for that reason.

## Math

MathJax 3 from the jsDelivr CDN, `tex-chtml`, with `tags: "none"` and the explicit
`\tag{C.n}` written by the build, so that the numbers are fixed at build time and equal to the
PDF, and do not depend on the order in which the browser renders the page. The inline delimiters
are `\(` `\)` and the display ones `\[` `\]`, as pandoc writes them. Display equations scroll
horizontally on a phone instead of overflowing. This is the renderer the lecturer chose.
Vendoring MathJax into `docs/` stays the way out if the CDN becomes a problem.

## Figures and captions

Each `figures/pdf/sNNfMM_name.pdf` becomes `docs/notes/figures/sNNfMM_name.svg` with
`pdftocairo -svg`, rebuilt only when the PDF is newer. The caption is the second argument of
`aqmfigure`, converted by pandoc with its math, and shown under the figure as "Figure C.m." in
bold followed by the caption. The alt text is the first sentence of the caption. The figures sit
on a white card, since the renders are flattened on white by `build_figure.sh`, and in the dark
mode of the site the white card stays. When the Blender plan of `BLENDER_FIGURES_PLAN.md`
replaces a figure, the rebuild picks up the new PDF by its date.

## Numbering and cross-references

The web numbers follow the PDF at the moment of the conversion. Sections are numbered `C.K` in
the order of the file, subsections `C.K.J`, numbered equations `C.n` by counting `equation`
environments in the order of the file, figures `C.m` in the order the session inputs them. The
conversion writes these numbers explicitly into the Markdown, as the heading attribute
`{#sec-2-5 number="2.5"}`, as `\tag{2.8}` in the display math with the anchor `{#eq-2-8}`, and
as the attribute `{#fig:s02:cosband number="2.2"}` of the figure, so that the number of an
equation is visible in the file next to the equation and does not depend on where the file is
later edited. The plain-text references of the notes become links at the conversion, `(2.8)`
to `#eq-2-8`, `Section 2.11` to the page of `sec-2-11`, `Figure 2.2` to `#fig:s02:cosband`,
with the original string kept as the link text. The build collects every anchor of every page
into a global map and resolves the links across pages and across sessions.

Once the Markdown is the master, a web-side edit can add or remove numbered things, and the
rule is that the numbers of the notes are not reused. A new equation added on the web takes
the number of the equation before it with a letter, `\tag{2.8a}`, a new section is added without
a number or with `2.5a`, and a removed equation leaves a gap. In this way a number that appears
on the web and in the PDF means the same equation in both, and a student who reads the two can
go from one to the other. The check reports a number used twice in a session and a link whose
anchor does not exist.

## How a change reaches the page

The `.tex` notes are the starting content, and the conversion is done once per session. The
lecturer decided on 2026-11-06 to fork, meaning that `convert.py` writes the Markdown of a
session into `webnotes/pages/sessionNN/`, one file per section plus `index.md` for the
introduction of the chapter, and from that moment these files are the source of the web pages.
`convert.py` refuses to overwrite a page that exists, so a converted session is never
regenerated by accident, and a conscious regeneration needs `--force` and loses the web edits
of that session.

From then on there are two sources, the `.tex` for the PDF and the Markdown for the web, and a
change in one does not reach the other by itself. A fix of the physics or of a sentence in
`lecture_notes/src/sessions/sessionNN.tex` has to be applied a second time in
`webnotes/pages/sessionNN/`, and the other way round when the web wording is better. The
reminder is `texdiff.py`. The file `webnotes/SYNC` holds one line per session with the commit
of `lecture_notes/src` the Markdown was last brought in line with, and `texdiff.py` prints the
diff of `sessions/sessionNN.tex` and of the figure files of that session since that commit,
hunk by hunk, so that a session that comes back to the site after weeks of work on the notes
sees what it has to carry over. When the hunks are applied, the session updates the line in
`SYNC` to the current commit. A new render of a figure needs no carrying over, since the build
converts the PDF of the figure by its date.

A change made for the web, a rewording, a split section, a quiz, a try-it box or a widget,
is an edit of the Markdown and reaches the site by running the build, which renders
`webnotes/pages/` to `docs/notes/`, runs the checks, and the result is committed with the
Markdown. Every web edit of prose follows `VOICE.md` and `writing_style.md`.

## Quizzes

A quiz is an inline multiple-choice question in a section page, with the choices as buttons,
the answer hidden, and after the click one line that says right or wrong and the explanation.
It is plain HTML and a few lines of JavaScript in `notes.js`, with no server and nothing stored,
so it works on GitHub Pages as it is. The source is a block in the Markdown page itself, placed
right after the equation or the figure it checks, as the lecturer decided, in the fenced-div
syntax that pandoc already reads, so the same converter handles the prose and the math of the
quiz.

```
::: quiz
Q: The band of the chain is $\epsilon_\varphi=-2t\cos\varphi$. Where is the group velocity largest?
- At $\varphi=0$, the bottom of the band.
- * At $\varphi=\pi/2$, the middle of the band.
- At $\varphi=\pi$, the top of the band.
A: The group velocity is the slope of the band, $v=\partial\epsilon_\varphi/\partial\varphi=2t\sin\varphi$.
It is largest at $\varphi=\pi/2$, where the dispersion is locally linear, and it is zero at the two
band edges, which is the same place where the density of states diverges.
:::
```

The asterisk marks the right choice. The question and the explanation are prose of the notes
and follow `VOICE.md` and `writing_style.md`, so simple English, "we" as the default pronoun,
the physics first and the name after, no colons and no em-dashes. Each quiz checks one idea of
the section, and the explanation ties it to something that can be computed or measured in one
clause, as the example does with the density of states. The physics of every quiz is checked
with the `aqm-physics-checker` agent before it goes to the site, in the same way the films are
checked. Three quizzes per section are enough at the start, in the sections that carry a
derivation, and none in the motivation and closing sections.

A second kind of block, the "try it" box, points to one cell of the notebook with a concrete
thing to change, for instance "set `eta=0.3` in the cell of the chain and look where the second
extremum of the band appears". It uses the same syntax with the class `tryit`, and it renders
as the notebook box of the notes with a different title.

## Where the widgets and simulations plug in

The lecturer chose Pyodide, meaning that the calculation runs in the browser with the Python
of the course. A widget is a block of the Markdown page with the pyqula code that computes it
and the parameters the student can move.

```
::: {.widget name="chainband" params="eta:0:1:0.05"}
```python
import numpy as np
phi = np.linspace(-np.pi, np.pi, 201)
result = {"x": phi.tolist(), "y": (-2*np.cos(phi) - 2*eta*np.cos(2*phi)).tolist()}
```
:::
```

The build renders this as a hook

```
<div class="widget" data-widget="chainband" data-params="eta:0:1:0.05"
     data-src="../widgets/chainband.json"><script type="text/python">...</script></div>
```

and `notes.js` does two things with it. It shows at once the curve of `data-src`, a JSON
written by `webnotes/widgets/precompute.py`, which runs the same code block with the Python of
the machine over the grid of the parameters. And it offers a "Run live" button, which loads
Pyodide from its CDN on the first click, installs pyqula with `micropip` and runs the code
block in the browser for the value of the slider, so that every parameter is possible and not
only the precomputed grid. The JSON is the fallback for a widget that turns out too slow or
that needs a package Pyodide does not have, and for the student without network to the Pyodide
CDN. Pyodide with pyqula was not tested in this run. Phase 6 starts with that test, the import
of pyqula in Pyodide, the load time on a first open, and one band structure, and only after it
passes is the live path built.

The simplest widgets, such as the band of the chain above, need numpy only and are the pilot.
The widgets that call pyqula, for instance the bands of the honeycomb lattice along the k-path
with a slider on the sublattice mass, come after the feasibility test. Links to Colab and
Binder for the notebooks cost one line per notebook and are added in phase 5 with the try-it
boxes.

## The toolkit

The toolkit lives in `webnotes/` at the root of the repository, not in `docs/`, since `docs/`
is served. It depends on pandoc 3, python3, `pdftocairo` from poppler, and git. The math check
needs node with `katex` and `mathjax-full` installed in `webnotes/mathcheck/` by `npm install`,
and it is skipped with a warning when node or the packages are missing. It is built in stages,
one per phase, and the first stage is the smallest thing that builds the pages of one session in
one command.

```
webnotes/
  convert.py             python3 webnotes/convert.py --session N [--force]
                         one-time: the .tex of a session to pages/sessionNN/*.md, the manifest
                         and the SYNC line; refuses to overwrite an existing page
  build.py               python3 webnotes/build.py [--session N] [--serve] [--check-only]
                         renders pages/ to docs/notes/, runs the checks
  filters/tex2md.lua     the conversion filter, numbering, boxes, figures, links to anchors
                         (the prototype of the appendix, with Markdown output)
  filters/web.lua        the build filter: the quiz, tryit, widget and notebookbox divs, the
                         link resolution with labels.json
  template.py            the page shell, imports STYLE from docs/build_site.py so the look
                         stays one
  labels.json            the global anchor map written by the first pass, read by the second
  manifest/sessionNN.json the frozen list of pages of a session, slug and title, so a retitled
                         section keeps its URL
  pages/sessionNN/index.md, KK-slug.md   the web Markdown master, one file per section
  widgets/               notes.js, the Pyodide loader, precompute.py and its JSON data
  check.py               dangling anchors, missing images, "??", numbers used twice, pages
                         changed outside docs/notes/, pages in docs/notes/ with no source
  mathcheck/check.js     every math fragment through MathJax and KaTeX, with package.json
  texdiff.py             git diff of the .tex of a session since its commit in SYNC
  SYNC                   one line per session, the commit of lecture_notes/src its Markdown
                         was last brought in line with
  README.md              how to run it, written in phase 1
```

The preview server is `build.py --serve`, which runs `python3 -m http.server` in `docs/` and
prints the URL of the notes. The build is idempotent, running it twice changes nothing in
`docs/`, and `git status` after a build shows only the pages that changed. The Markdown pages
are plain pandoc Markdown with `$` math and fenced divs, so they can be edited in any editor,
and the build filter is the only place that knows the four block kinds.

## Phases

Each phase is one unit that a later session can finish, and each ends with a commit. "Done"
is mechanical where it can be.

Phase 0, this run. The plan, the tracker and the prototype in the scratchpad. Done.

Phase 1, the pilot on session 2. Stage 1 of the toolkit, `convert.py` with
`filters/tex2md.lua`, `build.py` with `filters/web.lua` and `template.py`, the figures to SVG,
the global anchor map, the manifest of session 2, and `check.py` with the anchor, image and
`??` checks. The conversion writes `webnotes/pages/session02/`, which is then the master of
session 2, and the build writes `docs/notes/session2/` and `docs/notes/index.html` listing
session 2 only, and adds the link to the notes on the video and landscape pages of session 2
through `build_site.py`. Session 2 is the pilot because it has hard-coded equation references,
`(1.6)` from another session, and the first figures. Done means the conversion and the build
each run in one command, the Markdown of session 2 reads cleanly in an editor with its math,
tables and boxes, a test edit of one sentence in the Markdown shows on the page after a build,
the checks pass, a screenshot of two pages was looked at, `git diff docs/lectures
docs/landscape` shows only the added link, and `webnotes/README.md` says how to run it.

Phase 2, all ten sessions. The conversion of the other nine sessions with their manifests and
`SYNC` lines, the cross-session links, the `Section C.K` links, the course table of contents,
the notes column on the landing page, the README link, and the math check in `mathcheck/`.
Done means every section of the ten sessions and the index pages build in one command, zero
`??`, zero dangling anchors, every image exists, the math check reports zero errors, the ten
Markdown sessions are committed as the master, and the lecturer has opened the pages.

Phase 3, the two sources kept together. `texdiff.py` with `SYNC`, the check for a number used
twice and for a page in `docs/notes/` without a source, and the first web-only edits, a try-it
box on sessions 1 and 2 and one rewording the lecturer wants on the web only. Done means a
test commit that edits one `.tex` session is listed by `texdiff` for that session and no
other, the hunk was carried over to the Markdown by hand and `SYNC` updated, and the web-only
edits survive a rebuild, which is now trivially true since nothing regenerates them.

Phase 4, quizzes of sessions 1 to 5. The quiz renderer in `notes.js`, and the quiz blocks
written into the Markdown pages in the voice and checked by `aqm-physics-checker`. Done means
every derivation section of these sessions has at least one quiz, each quiz was answered once
in the browser, and the texts passed the physics check.

Phase 5, quizzes of sessions 6 to 10, the try-it boxes of all sessions that point to the
notebook cells, and the Colab and Binder links of the notebooks. Done as in phase 4.

Phase 6, the widgets with Pyodide. It starts with the feasibility test, in the scratchpad,
of pyqula in Pyodide. The test loads Pyodide in headless Chrome, measures the load time of a
first open, installs pyqula with `micropip` and records whether every dependency of pyqula has
a Pyodide package, and computes one band structure, the honeycomb lattice along the k-path,
with its time. If the import fails or the band takes longer than a few seconds, the test
reports it, and the widgets of this phase are built on the precomputed JSON alone with the
"Run live" button hidden. Then the hook, `notes.js` with the Pyodide loader and the JSON
fallback, `precompute.py`, and the pilot widget of the band of the chain on the page of
Section 2.5. Done means the test result is written in the tracker with its numbers, the pilot
renders on the site without an error in the console from the JSON, and the live path runs in
the browser when the test passed.

Phase 7, polish. Page weight if the SVGs are too slow on a phone, a single-page version of
each session for printing and search, the alt texts, and whatever the lecturer noted while
reading. Done when the lecturer closes the list.

Later sessions keep the loop of the section "How a change reaches the page", and the tracker
records to which commit of the `.tex` each session's Markdown is synced.

## Risks

The two sources are the first risk, and the lecturer accepted it with the fork. A fix in the
`.tex` after the conversion does not reach the web, and a better sentence on the web does not
reach the PDF, unless someone carries it over. `texdiff.py` and the `SYNC` lines are the only
reminder, and they work only if every session that edits the notes also runs `texdiff` and
updates `SYNC`, so this step goes into the workflow of the notes and into the tracker.

The hard-coded numbers are the second. A new equation in a `.tex` file after the conversion
shifts the numbers after it in the PDF but not on the web, since the web numbers are explicit
in the Markdown. A `(2.9)` carried over from the `.tex` then means a different equation on the
web than in the PDF. The rule of the section on numbering, letters for new numbers and gaps for
removed ones, keeps the two readable side by side, and the check reports every link whose
anchor does not exist and every number used twice.

The CDN is the third risk. With MathJax from jsDelivr a page without network shows raw LaTeX,
and with Pyodide from its CDN the live widgets need the network too. Vendoring MathJax in
`docs/` costs about 2 MB in git and removes the first dependency, and the precomputed JSON
removes the second for the widgets.

Pandoc is the fourth. The conversion and the build depend on pandoc 3.8 of the anaconda
environment, and a different machine with pandoc 2 would write different Markdown and HTML. The
toolkit checks the version and refuses to run with pandoc below 3. Since the conversion runs
once per session, the Markdown it wrote does not depend on pandoc afterwards, and only the
build does.

The figure pipeline is the fifth. The SVGs embed a JPEG, so a figure page of six figures is
about 1 MB. If the Blender plan changes the renders, `build_figure.sh` and this build run in
sequence, and the dates decide which SVGs are redone.

Pyodide is the sixth. It was not tested with pyqula. pyqula may need a package that Pyodide
does not ship, the first load is tens of seconds and tens of MB, and a phone may not have the
memory. The feasibility test of phase 6 decides it with numbers before anything is built on
it, and every widget keeps its precomputed JSON as the fallback, so a widget that is too slow
live still shows its curves at once and only loses the slider between the precomputed values.

## Decisions taken on 2026-11-06

The lecturer answered the eight open decisions of the first version of this plan, and the
sections above are written to them. One line each, with the choice.

1. Source of truth. Fork to a web Markdown master now. `convert.py` writes
   `webnotes/pages/sessionNN/` once per session, and the pages are built from that Markdown
   from then on, with `texdiff.py` as the reminder that a `.tex` fix is applied a second time.
2. Page tree. One page per section, with the session page holding the introduction and the
   contents.
3. URL of a section page. Number plus slug, `notes/session2/05-blochs-theorem-and-the-first-
   band-structure.html`, frozen in the manifest.
4. Math renderer. MathJax 3 from the jsDelivr CDN with the explicit `\tag{C.n}`.
5. Deployment. The legacy Pages build from `docs/` on `main`, built locally and committed, as
   the video pages are.
6. Quiz format. Inline multiple choice placed after the equation or the figure it checks, with
   the explanation hidden until the click.
7. Widgets. Pyodide running pyqula in the browser, with phase 6 starting from a feasibility
   test of the import, the load time and one band structure, and precomputed JSON as the
   fallback of every widget.
8. Toolkit. The staged toolkit of this plan, building from the Markdown master.

## Appendix, the prototype filter of the test

The scratchpad of the session that ran the test is temporary, so the Lua filter of the
prototype is kept here, since it is the part that took the work. Phase 1 starts from it. The
Python assembly around it is 170 lines that run pandoc per session with this filter, split the
HTML at the `<h2>` headings, link the `(C.n)` references with the equation map, and wrap each
page in the shell of `docs/build_site.py`, and it is rewritten with the global label map of
phase 1. The build of the test was `pandoc --resource-path=lecture_notes/src -f latex -t html5
--mathjax --wrap=none --lua-filter aqm.lua -M chapter=N` on a wrapper that inputs `preamble`,
`figures_preamble` and `sessions/sessionNN`.

```lua
-- Prototype pandoc filter for the web notes of Advanced Quantum Materials.
-- Reads the metadata field "chapter" (the session number) and
--   numbers the sections and subsections as in the PDF (C.K, C.K.J),
--   numbers the equation environments as in the PDF (C.n) with an explicit \tag,
--   numbers the figures (C.m) and rewrites \ref{fig:...} to that number,
--   turns the notebookbox Div into a titled callout and links the notebook,
--   replaces the figure PDF by the SVG of the same name and drops the adjustbox junk.

local chapter = 0
local sec, subsec, eq, fig = 0, 0, 0, 0
local figures = {}       -- label -> number, filled in the first pass
local REPO = 'https://github.com/joselado/Advanced_Quantum_Materials_2027'

local function slug(s)
  s = s:lower():gsub('[^%w%s-]', ''):gsub('%s+', '-')
  return s
end

function Meta(m)
  chapter = tonumber(pandoc.utils.stringify(m.chapter or '0'))
end

local function number_figures(doc)
  for _, b in ipairs(doc.blocks) do
    if b.t == 'Figure' then
      fig = fig + 1
      figures[b.identifier] = string.format('%d.%d', chapter, fig)
    end
  end
end

function Header(h)
  if h.level == 2 then
    sec = sec + 1; subsec = 0
    h.identifier = 'sec-' .. chapter .. '-' .. sec
    h.attributes['data-number'] = string.format('%d.%d', chapter, sec)
    h.attributes['data-slug'] = slug(pandoc.utils.stringify(h.content))
    table.insert(h.content, 1, pandoc.Str(string.format('%d.%d ', chapter, sec)))
  elseif h.level == 3 then
    subsec = subsec + 1
    h.identifier = 'sec-' .. chapter .. '-' .. sec .. '-' .. subsec
    table.insert(h.content, 1, pandoc.Str(string.format('%d.%d.%d ', chapter, sec, subsec)))
  elseif h.level == 1 then
    h.identifier = 'session-' .. chapter
    table.insert(h.content, 1, pandoc.Str(string.format('Session %d. ', chapter)))
  end
  return h
end

function Math(m)
  if m.mathtype ~= 'DisplayMath' then return nil end
  local body = m.text
  local numbered = body:match('^%s*\\begin{equation}')
  body = body:gsub('^%s*\\begin{equation%*?}', ''):gsub('\\end{equation%*?}%s*$', '')
  if numbered then
    eq = eq + 1
    local n = string.format('%d.%d', chapter, eq)
    body = body .. string.format(' \\tag{%s}\\label{eq-%s}', n, n:gsub('%.', '-'))
  end
  m.text = body
  return m
end

function Link(l)
  if l.attributes['reference-type'] == 'ref' then
    local n = figures[l.attributes['reference']]
    if n then
      l.content = { pandoc.Str(n) }
    else
      l.content = { pandoc.Str('??') }
      io.stderr:write('unresolved reference ' .. l.attributes['reference'] .. '\n')
    end
    l.attributes = {}
  end
  return l
end

function Figure(f)
  local n = figures[f.identifier]
  local blocks = {}
  for _, b in ipairs(f.content) do
    if b.t == 'Div' and b.classes[1] == 'adjustbox' then
      for _, c in ipairs(b.content) do
        if c.t == 'Para' and #c.content == 1 and c.content[1].t == 'Image' then
          table.insert(blocks, c)
        elseif c.t == 'Plain' or c.t == 'Para' then
          for _, i in ipairs(c.content) do
            if i.t == 'Image' then table.insert(blocks, pandoc.Plain({ i })) end
          end
        end
      end
    else
      table.insert(blocks, b)
    end
  end
  f.content = blocks
  f.caption.long = { pandoc.Para({ pandoc.Strong({ pandoc.Str('Figure ' .. n .. '.') }), pandoc.Space(),
                                   table.unpack(pandoc.utils.blocks_to_inlines(f.caption.long)) }) }
  return f
end

function Image(img)
  local name = img.src:match('figures/pdf/(.*)%.pdf$')
  if name then
    img.src = '../figures/' .. name .. '.svg'
    img.attributes['loading'] = 'lazy'
  end
  return img
end

function Div(d)
  if d.classes[1] ~= 'notebookbox' then return nil end
  local first = d.content[1]
  if first and first.t == 'Para' and first.content[1] and first.content[1].t == 'Span' then
    local title = first.content[1].content
    table.remove(first.content, 1)
    while first.content[1] and (first.content[1].t == 'SoftBreak' or first.content[1].t == 'Space') do
      table.remove(first.content, 1)
    end
    local t = { pandoc.Strong({ pandoc.Str('Notebook check-in: ') }) }
    for _, i in ipairs(title) do
      if i.t == 'Code' and i.text:match('^session%d+%.ipynb$') then
        i = pandoc.Link({ i }, REPO .. '/blob/main/jupyter-notebooks/' .. i.text)
      end
      table.insert(t, i)
    end
    table.insert(d.content, 1, pandoc.Div({ pandoc.Para(t) }, pandoc.Attr('', { 'boxtitle' })))
  end
  return d
end

return {
  { Meta = Meta },
  { Pandoc = function(doc) number_figures(doc); return nil end },
  { Header = Header, Math = Math, Figure = Figure, Image = Image, Div = Div },
  { Link = Link },
}
```
