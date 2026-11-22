# Progress of the lecture notes as web pages

The plan is `lecture_notes/WEB_NOTES_PLAN.md`. This file is the tracker that each session
updates at its end, one line per phase and one per session. Last update 2026-11-22, the pedagogical pass of
Sessions 1, 2, 4 and 5.

Start here on 2026-11-22. Sessions 1 to 5 are in the shape locked on 2026-11-21 and published on the site. Sessions 6
to 10 have their conventions sheet, plan and recipes, committed, and wait for the lecturer to read 1, 4 and 5. The
errors of the old text of Sessions 1, 2, 4 and 5 are corrected on the web or listed for the lecturer in the section
"Open for the lecturer" of each `webnotes/plans/sessionNN.md`. The log entries of 2026-11-21 and 2026-11-22 at the
end say what was done and what is open.

The paragraph below is the state of 2026-11-06. Phases 3 to 6 are built and checked, and nothing is committed yet. The notes have 126 section pages
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
| 4 | Quizzes of sessions 1 to 5, quiz renderer | done 2026-11-06, 113 quizzes; renderer with a verdict and a counterexample per option, 2026-11-06 |
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
- 2026-11-06. Quizzes with a verdict per option. The lecturer asked that each answer can be clicked, that a correct
  answer gives a short reason and that a wrong answer gives a counterexample, with 3 options per question. All 212
  quizzes were cut to 3 options and given feedback under every option, then five verifiers recomputed the numbers
  and corrected 37 faults (4 of wrong physics, 19 weak counterexamples, the rest numbers, signs and wording). The
  full build gives 0 errors, 4946 math fragments with 0 errors, and a second build writes nothing. In headless Chrome
  one quiz per session was shot at 1400 and 390 px, light and dark, unanswered, with the correct click and with a
  wrong click. At 390 px the verdict now goes under the option text, and the math in an option is no longer a
  second tab stop. The no-JS view is not tested in a browser. The lecturer has not looked at the quizzes yet.
- 2026-11-06. More schematics, also in quizzes. The lecturer asked for more schematics in the notes, in the
  questions and in the answers. Ten agents added 69 schematics on the pages and 47 in quizzes (7 more figures shown
  again in quizzes), five verifiers rendered each one and recomputed the curves, and corrected 3 wrong-physics or
  mislabelled figures, 8 caption mismatches and 10 unreadable labels. Default build: 171 pages, 0 errors,
  5435 math fragments with 0 errors, a second build writes nothing, `docs/build_site.py` runs. `docs/notes/` weighs 19 MB.
  Checked in headless Chrome at 1400 and 390 px, light and dark: one page per session and three quizzes with a figure,
  before and after the click. Not done: the SVGs over 200 kB (the largest is `nambu_bands.svg`, 560 kB), and the
  small text of some schematics at 390 px. Nothing committed.
- 2026-11-07. Voice and links pass on all ten sessions. The lecturer decided six things for this pass. Every page
  ends with a "Where this comes back" box that links forward, or links the next natural step when nothing returns.
  A notation clash keeps the source and gets one bridging sentence with a link. The ten index pages and the ten
  closing summaries follow one shape, which is what we need from before, what we will see and where it comes back,
  all linked. Sentences about the recording and the lecture are deleted, and a fact that matters stays as physics.
  Page 4.19 on the Haldane model is cut to a recap of about 220 words of prose, with links to Sections 3.10 and
  3.10b. A plain "Session N" is linked by the build, in `SessionLinks` of `filters/web.lua`. The text agents edited
  the Markdown of the ten sessions, and then the coordinator ran the default build. It gives 171 pages, 137 written,
  498 anchors in `labels.json`, 0 errors and no pending link, and a second build writes nothing. The math check gives
  5908 fragments with 0 errors. `lint.py` reads 136 pages and gives 0 hits, with 63 warnings of the category
  `exactly`, a list to read through, since the word stays when it states a physics fact. Every Markdown page has its box,
  and the 34 HTML files without one are the redirect stubs. `docs/build_site.py` wrote 22 pages. No mechanical fault needed
  a fix. Still open are the 7 SVGs at or over 200 kB (9 warnings), with `nambu_bands.svg` at 560 kB the largest, and nobody
  has read the pages in a browser after this pass. Nothing committed.
- 2026-11-21. Pedagogical pass, pilot on one page, Section 3.5. The lecturer picked four things for the notes, the
  steps of a derivation on demand, a box "In the lab" with a real number and its source, an opening question on each
  page with shorter paragraphs, and worked problems. The same day the lecturer asked for boxes around the main results,
  for pages that can be read from the middle, and for quiz questions that are short, hold their equation and sometimes
  use pictures. The toolkit got the blocks `key`, `recall`, `steps`, `problem` with `solution` and `lab`, picture
  options in a quiz, the display inside a quiz of every numbered equation that it links (the TeX is the new key
  `equations` of `labels.json`), and the lint categories `quiz-long` and `quiz-ref`. All are described in
  `webnotes/README.md`. Page 3.5 has one of each, with a new schematic of the Hall plateau and three small maps for a
  picture quiz. Only private builds were run (`--out`), with 171 pages, 0 errors and 6108 math fragments with 0 errors.
  The default build was not run, so `docs/notes/` and `webnotes/labels.json` are as before. At the next default build
  105 equations appear inside quizzes on 70 pages. The lint lists 83 `quiz-long` and 11 `quiz-ref` hits in the ten
  sessions, as the work list for the questions. Not done: the other 16 pages of Session 3, the checklist of the closing
  summary 3.13, and the lecturer has not read the page yet. Nothing committed.
- 2026-11-21, later. The lecturer picked the full set of blocks for every page and locked the rules of the day, which
  are now in `WEB_NOTES_PLAN.md` (sections "Figures and captions", "The shape of a page", "Quizzes"), in
  `WEB_NOTES_BRIEF.md` for the agents and in `CLAUDE.md`, commit c7532ef. New rules of the same day: every plot has
  its axes, a map over reciprocal space shows the first Brillouin zone dashed in the extended zone, and a
  calculation that pyqula can do is a small script of `webnotes/scripts/sessionNN/` with a download button under the
  plot (attribute `script` of the figure, helpers `run_script`, `kmap`, `pyqula_kmap`, `kaxes`, `draw_zone` of
  `figures/style.py`). The three figures of Section 3.5 are redrawn from pyqula scripts with these rules. Four agents
  are bringing the other 16 pages of Session 3 to the shape of Section 3.5. Still only private builds, nothing of
  the toolkit or of the pages committed.
- 2026-11-21, end of the day. Session 3 is in the new shape on all its pages. Four agents edited the 16 other pages
  (the file of Section 3.8 also holds 3.9a), and four independent physics checks recomputed the new material, with
  their findings applied by the agent of each group. The last private build gives 171 pages, 0 errors and 7678 math
  fragments with 0 errors, and the lint has no hit on Session 3. Session 3 has 45 new figure scripts and 17 pyqula
  scripts in `webnotes/scripts/session03/`, 6 of them with a download button. The conventions that were checked by
  number are in `webnotes/conventions/session03.md`. Open for the lecturer: how (3.4) is printed, since for a voltage
  along $y$ and a current along $x$ the result is $\sigma_{xy}=-(e^2/h)C$ with the $\Omega$ of the notes, and the two
  folds of Sections 3.4 and 3.5 now say so while (3.4) is untouched. Also open: about ten older figures of Session 3
  without ticks or named axes, the try-it box of Section 3.7 with an empty figure reference, and `ham_learning.py` of
  Session 10, which is not reproducible. The lint lists 70 `quiz-long` and 9 `quiz-ref` hits in the other nine
  sessions. The lecturer picked four toolkit parts to build before the next session: a fast build per page with
  dependencies per figure, the conventions sheet with shared helpers and pyqula recipes, mechanical gates with a
  check suite, and a skill with two agent types and a plan per session. Only the conventions sheet exists so far.
  The default build was not run and nothing of the toolkit or of the pages is committed.
- 2026-11-21, toolkit part 1 of 4, the fast build. `build.py` keeps the pandoc tree of each page in
  `webnotes/.cache/ast/` (git ignores it), a schematic is stale only against its own script, the helpers `_NAME.py`
  that it imports and its pyqula script, and `figures/style.py` no longer makes anything stale (`--redraw` draws all
  again). `--page FILE` with `--session N` renders one page. Measured: 46 s for a full build of 171 pages, 30 s for
  a second one, 2.3 s for one page, 0 errors, and no tracked SVG changed. `style.save` writes through a temporary
  file per process, so parallel builds no longer collide. Parts 2 to 4 are not built yet.
- 2026-11-21, toolkit parts 2 to 4. The lecturer kept (3.4) as printed, and the fold of Section 3.5 says once that
  it is the current along $y$ for a voltage along $x$. Built and run on Session 3: `figures/physcheck.py` with
  `scripts/RECIPES.md` (13 recipes) and the checks `checks/test_physcheck.py`, `checks/test_recipes.py` and
  `checks/session03/conventions.py`; the lint categories `opener`, `key`, `long-paragraph`, `lab-source` and
  `lab-number` with `labsource.py` and `sources/` (9 stored sources, publisher text kept only as short quotations,
  full copies in the ignored `sources/.full/`); `layout.py`, `build.py --verify`, and the `AXES-WARNING` of
  `style.save`; `inventory.py` with the plan skeleton `plans/sessionNN.md`; the documentation in `docs/`. On
  Session 3 the build gives 0 errors, the lint 0 hits and 7 warnings, the layout check 0 findings at 1000 and at
  a true 390 px, and `--verify` 3 of 3 OK. Headless Chrome does not go below 500 px, so the earlier "390 px"
  screenshots were not a phone. The work lists for the other nine sessions: 100 pages without an opening question,
  73 with a numbered equation and no key box, 64 paragraphs over 150 words, 70 long question sentences, 9 quizzes
  that refer by number. The layout check finds 4 pages that scroll sideways on a phone (4.13, 5.4, 7.10, 9.10b;
  the rule `mjx-assistive-mml { max-width: 100% }` of the template fixes three, and 5.4 needs its formula split).
  The axes audit of the old figures gives 11 warnings in 7 scripts, and 80 axes drawn with the axis off in 51
  scripts that need `sketch=True` or a look. Outside the repository: the skill `aqm-webnotes-session` and the agent
  types `aqm-notes-builder` and `aqm-notes-checker`, set to Opus at xhigh as the lecturer said for the next
  sessions. The brief has the mistakes of Session 3 and the new commands. Nothing of this is committed, and the
  default build was not run.
- 2026-11-21, last checks of the toolkit. The first check script per page, `checks/session03/main_05_berry_curvature.py`,
  found a wrong number on its first run: the feedback of the picture quiz of 3.5 said that each color of the
  staggered map weighs about $0.6\pi$, and two independent routes give $0.71\pi$ for a staggered potential of 0.5.
  The page now says $0.7\pi$. That number came from a physics check and was never asserted, so the other 15 pages
  of Session 3, which have no check script of their own, can hold the same kind of error. `--verify` gives 4 of 4
  OK. With the real template the layout check of the ten sessions gives one page left, 5.4, whose inline formula
  is 194 px too wide on a phone. The agent types `aqm-notes-builder` and `aqm-notes-checker` could not be launched
  in the session that wrote them, so they are untested. The film agent `aqm-physics-checker` states the Berry
  connection as $i\langle\partial_k u|u\rangle$, the opposite sign of the notes, and this is not changed.
- 2026-11-21 to 2026-11-22, the pedagogical pass of Sessions 1, 2, 4 and 5, with the skill `aqm-webnotes-session` run
  as workflows. The lecturer asked for all the other sessions with up to 20 agents, then picked 20 at a time in
  waves, a lighter check (the recheck only where a finding is wrong) after the cost came out higher than estimated,
  and three sessions first. Session 2 was the pilot of the agent type `aqm-notes-builder`. For every session two
  agents wrote the conventions sheet with no sight of each other and a third settled each disagreement by a
  calculation (10 to 20 per session), and one more agent made the nine sheets agree with each other. The plans of
  all sessions are in `webnotes/plans/`, with 60 lab boxes backed by stored sources. `RECIPES.md` holds 81 recipes,
  and its test runs in about 90 s. The lecturer picked on 2026-11-21 that the old figures that break the plot rules
  are redrawn under the same names, and said that the PyPI release of pyqula will be updated to the GitHub version,
  so the scripts target that version (both are in `WEB_NOTES_PLAN.md`). `labsource.py` takes a lock, since parallel
  fetches lost entries of the index. Session 2 and 3 were published first, then 1, 4 and 5: the default build gives
  171 pages, 0 errors, 12425 math fragments with 0 errors, and a second build writes nothing. Every group of pages
  went through an independent physics check and a fix. Cost: about 35 million subagent tokens for the preparation of
  all sessions and the pages of 1, 2, 4 and 5. Known and open: the Session 7 check of the Ising chain of the notebook
  quiz failed once in three runs, so it is flaky; release 0.0.96 of PyPI lacks `get_anomalous_hall_conductivity`,
  which `scripts/session03/hall_conductivity_haldane.py` needs until PyPI is updated; the sheets agent found that the
  "flux per plaquette" line of the Session 3 sheet holds only on the square lattice, and that Session 3 puts "about
  seven times at 10 T" in Section 4.1 while that quiz is in Section 4.2. A subagent cannot write a report file, so the
  reports are the answers of the agents, kept in the workflow journals of the session.
- 2026-11-22, running at the time of writing, in case the session stops. Three workflows of the Claude Code session
  run in the background. (1) The correction of the old text of Sessions 1, 2, 4 and 5, run `wf_3db0c3d3-c48`, which
  edits their pages and check scripts and rewrites the section "Open for the lecturer" of each plan as two lists,
  "Corrected on the web, to carry over to the .tex" and "For the lecturer". (2) Session 6, run `wf_74e82c0a-9c0`, and
  (3) Session 7, run `wf_cda36960-673`, each with builder, gate, physics check, fix and a recheck where a finding is
  wrong, one chain per group of the section "Builder groups" of the plan. The scripts are in
  `~/.claude/projects/-u-40-ladovj1-data-Documents-programs-Advanced-Quantum-Materials-2027/bbe18649-405d-487c-83fe-fcca11e6bfea/workflows/scripts/`,
  and a run resumes only in the same Claude session (`Workflow` with `scriptPath` and `resumeFromRunId`). If the
  session is gone, `git status` shows what each run left. A page with changes but no check script
  `webnotes/checks/sessionNN/gK_*.py` was stopped in the middle, and its group is built again by a new builder on the
  page as it is. When a run is finished, the steps are the gate of the skill on the session (the build with
  `--out DIR --math`, `lint.py`, `layout.py`, `--verify`, `labsource.py --check`, an unfiltered `git status`), then a
  commit, and the default build and push only on the lecturer's word. The flaky check of the Ising chain in
  `checks/session07/conventions.py` now accepts any state of the two-fold ground level, which is what DMRG returns.
  Sessions 8, 9 and 10 have not started.
- 2026-11-22, later in the morning. The old-text corrections of Sessions 1, 2, 4 and 5 finished (54 corrections,
  checked, not committed). The lecturer picked five open points: keep +t in (1.2) with a bridge sentence, turn the ring
  rotation of 2.3 around, put 1/sqrt(L) in (2.7), write |C_n|=1 and |sigma_xy| in (4.2), keep (5.20) and say that the
  sign of i is a gauge choice. The other 81 points are decided by the coordinator with the rule written in the
  workflow, run `wf_1a0244e4-53c`, and each plan ends with the list "Decided on 2026-11-22". Session 7 was paused at
  07:52 and resumed at 09:01 (same run `wf_cda36960-673`). Sessions 8, 9 and 10 run as `wf_26730ac0-c6d`, with at most
  7 groups at once so that all the runs together stay near 20 agents. The README was rewritten and pushed (80ab324).
