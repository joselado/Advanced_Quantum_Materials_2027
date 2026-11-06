# Progress of the lecture notes as web pages

The plan is `lecture_notes/WEB_NOTES_PLAN.md`. This file is the tracker that each session
updates at its end, one line per phase and one per session. Last update 2026-11-06, phases 3 to 6.

Start here. Phases 3 to 6 are built and checked, and nothing is committed yet. The notes have 126 section pages
(median 554 prose words, 292 to 934), 35 redirect stubs for the retired URLs, every page with at least one figure
(59 PDF figures, 29 shown again, 16 Blender panels, 27 new schematics), 212 quizzes, 62 try-it boxes and ten
Pyodide widgets. The full build gives 0 errors, an empty pending list, 3583 math fragments with 0 errors, and a
second build writes nothing. `python3 webnotes/texdiff.py` lists the changes of the `.tex` since `SYNC`. The next step
is the lecturer's look at the pages. Open points are in the section "Open points of phases 3 to 6" below.

## Phases

| Phase | What | Status |
|---|---|---|
| 0 | Plan, tracker, prototype in the scratchpad, conversion test, decisions | done 2026-11-06 |
| 1 | Pilot on session 2, convert once to Markdown, toolkit stage 1, link from the video pages | done 2026-11-06 |
| 2 | Convert all ten sessions, cross-session links, course contents, math check | done 2026-11-06 except the lecturer's look at the pages |
| 3 | `texdiff` and `SYNC`, the checks on numbers and sources, first web-only edits | done 2026-11-06, `texdiff.py` tested, the page layout reorganized (even lengths, 126 pages) |
| 4 | Quizzes of sessions 1 to 5, quiz renderer | done 2026-11-06, 113 quizzes |
| 5 | Quizzes of sessions 6 to 10, try-it boxes, Colab and Binder links | done 2026-11-06, 99 quizzes, 62 try-it boxes; Binder needs a `requirements.txt` |
| 6 | Pyodide feasibility test, then the widgets with the JSON fallback | done 2026-11-06, ten widgets placed, live run tested in Chrome |
| 7 | Polish, page weight, single-page version, alt texts | not started |

## Sessions

The column "synced to" is the commit of `lecture_notes/src` the Markdown of the session was
last brought in line with, the same as its line in `webnotes/SYNC`. A session whose `.tex`
changed after that commit has hunks to carry over, which `texdiff.py` lists.

| Session | Converted to Markdown | Pages built | Quizzes | Widgets | Synced to |
|---|---|---|---|---|---|
| 1 | yes, 2026-11-06, 12 pages | yes, 2026-11-06 | 19, 6 try-it | 1 | 2ee5256 |
| 2 | yes, 2026-11-06, 11 pages | yes, 2026-11-06 | 22, 6 try-it | 1 | 2ee5256 |
| 3 | yes, 2026-11-06, 16 pages | yes, 2026-11-06 | 25, 8 try-it | 1 | 2ee5256 |
| 4 | yes, 2026-11-06, 13 pages | yes, 2026-11-06 | 26, 7 try-it | 1 | 2ee5256 |
| 5 | yes, 2026-11-06, 16 pages | yes, 2026-11-06 | 21, 9 try-it | 1 | 2ee5256 |
| 6 | yes, 2026-11-06, 11 pages | yes, 2026-11-06 | 13, 5 try-it | 1 | 2ee5256 |
| 7 | yes, 2026-11-06, 12 pages | yes, 2026-11-06 | 23, 6 try-it | 1 | 2ee5256 |
| 8 | yes, 2026-11-06, 11 pages | yes, 2026-11-06 | 21, 6 try-it | 1 | 2ee5256 |
| 9 | yes, 2026-11-06, 15 pages | yes, 2026-11-06 | 25, 9 try-it | 1 | 2ee5256 |
| 10 | yes, 2026-11-06, 9 pages | yes, 2026-11-06 | 17, 0 try-it | 1 | 2ee5256 |

## Decisions taken

On 2026-11-06 the lecturer answered the eight decisions of the plan. Fork to a web Markdown
master now. One page per section. Number plus slug in the URL, frozen in a manifest. MathJax 3
from the CDN. The legacy `docs/` build, local and committed. Inline quizzes after the equation
or figure they check. Pyodide for the widgets, with a feasibility test first and precomputed
JSON as the fallback. The staged toolkit, building from the Markdown master. The full list is
the last section of the plan.

## Pyodide feasibility test

Run on 2026-11-06 in headless Chrome 151 with Pyodide v0.27.7 from the jsDelivr CDN (Python 3.12, numpy 2.0.2).

- Pyodide itself loads in 3 to 8 s on a first open (pyodide.asm.wasm is 10 MB). numpy adds 3 MB and scipy 13 MB.
- numpy, scipy and matplotlib load in 4 to 9 s more. A widget that needs numpy only is live after 4 to 6 s in
  total from the click, one that needs scipy after 8 s.
- pyqula installs with `micropip` as the pure-Python wheel `pyqula==0.0.96` from PyPI, with `deps=False`, in 2.5 s.
  No wheel built from the source folder is needed. Its dependencies `numba` and `jax` have no Pyodide package, so
  `notes.js` puts two small stand-in modules in their place (`jit` does nothing). `dill`, `threadpoolctl` and
  `multiprocess` are pure Python and install with `micropip`. The first `import pyqula.geometry` and the first
  Hamiltonian take 6.7 s. The widget with PyQula is live after 13 to 17 s in total.
- One band structure of the honeycomb lattice with a sublattice imbalance (400 k-points, 4 bands) takes 0.19 s once
  pyqula is imported. A finite chain with its eigenvectors takes 10 ms.
- One move of a slider takes 10 to 130 ms in nine widgets and 0.65 s in the network fit (4000 training steps).
- Things pyqula does in Pyodide only through the stand-ins are not tested, in particular the mean-field loop, the
  kernel polynomial method and the jax code. The widgets avoid them.

Result, the live path works, so every widget has the button "Run live in the browser" next to its precomputed JSON.

## Open points of phases 3 to 6

- Binder links do not work until the repository has a `requirements.txt` that installs pyqula.
- Pages above 750 words remain in sessions 5, 6, 9 and 10 (14 pages), and page 3.11a is below 300 words.
- The notebook of session 6 does not always converge with the installed pyqula in the mean-field cells.
- The notebook hopping sign of session 2 is opposite to the notes, and the try-it texts say so.
- Only the widget `island` uses pyqula in the page, the other nine use numpy. The stand-in modules for numba and jax are not tested for the pyqula mean-field code.
- Figure 3.3 shows panel (b) above (a) while the caption says "In front (a)".
- Display math on a phone is now scrolled inside its own block, since the page was wider than the screen.

## Log


- 2026-11-06. Conversion test in the scratchpad. Pandoc 3.8 with a Lua filter converted the
  ten sessions, MathJax rendered 1099 of 1099 math fragments, `pdftocairo -svg` converted the
  59 figures, make4ht and lwarp failed at the first `\includegraphics` of a figure PDF, dvisvgm
  dropped the raster of the figures. The Pages site deploys from `main:/docs` in the legacy
  mode with `.nojekyll` present, so the build stays local and committed. Plan and tracker
  written, then rewritten to the eight decisions of the lecturer. Nothing built in the
  repository, nothing committed.
- 2026-11-06. Phase 1, the pilot on session 2. `webnotes/` built with `convert.py`, `build.py`,
  `check.py`, `template.py`, the two filters and the README. Session 2 converted once to
  `webnotes/pages/session02/` (the introduction and 13 sections), `docs/notes/` built with the session page,
  13 section pages, the course index, 6 SVG figures. The link "Notes of this session" is on the video and
  landscape pages of session 2. The equation numbers 2.1 to 2.21 equal those of `main.pdf`, the edit test
  passed and was reverted, the check reports 0 errors and one pending reference, `(1.6)`. Nothing committed.
- 2026-11-06. Phase 2, first half. Sessions 1 and 3 to 10 converted with the toolkit fixes below, 156 pages
  built (session 1: 16 sections, 3: 13, 4: 21, 5: 20, 6: 17, 7: 12, 8: 14, 9: 11, 10: 8, with the
  introductions), 0 errors, no pending reference, no `??`, a second build writes nothing. Nobody has edited the
  Markdown of these sessions yet.
- 2026-11-06. Phase 2, toolkit part. `webnotes/mathcheck/` built (MathJax 3.2.2 in node, `build.py --math`),
  2162 fragments of the 156 pages checked with 0 errors. Third column "Lecture notes" on the landing page,
  link in the root `README.md`, notes links on the video and landscape pages of sessions 1 and 3 to 10.
  Phase 2 stays in progress until the proofreading of the Markdown of the ten sessions is finished and the
  lecturer has opened the pages.
- 2026-11-06. Phases 3 to 6. Ten agents reorganized the pages of the ten sessions (126 pages, merges and splits with 35
  redirects), added schematics, quizzes and try-it boxes, `texdiff.py` and the ten widgets. The integration inserted the
  widgets at the end of their sections, froze the 171 URLs, set the display math of the template to scroll inside its
  block (the pages were wider than a 390 px screen), and checked the pages in headless Chrome at 1400 and 390 px.
