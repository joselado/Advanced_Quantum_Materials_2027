# Progress of the lecture notes as web pages

The plan is `lecture_notes/WEB_NOTES_PLAN.md`. This file is the tracker that each session
updates at its end, one line per phase and one per session. Last update 2026-11-06, phase 1.

Start here. The next session does phase 2, all ten sessions. Phase 1 is done, and the toolkit is
`webnotes/`, read `webnotes/README.md` and the section "What phase 1 found" of the plan first. For each
session N from 1 and 3 to 10 run `python3 webnotes/convert.py --session N`, then
`python3 webnotes/build.py` and `python3 docs/build_site.py`. Look at what the conversion log says about
numbers left as text and about `??`, and at the pending list of `check.py`, which must become empty. The
things the pilot did not meet and phase 2 has to handle are the tables of session 1 and 9, `\subsection`
headings, the cross-session figure references of session 8 and the `Equation C.n` forms. Then add the
notes column to the landing page, the link in the README, and `mathcheck/`.

## Phases

| Phase | What | Status |
|---|---|---|
| 0 | Plan, tracker, prototype in the scratchpad, conversion test, decisions | done 2026-11-06 |
| 1 | Pilot on session 2, convert once to Markdown, toolkit stage 1, link from the video pages | done 2026-11-06 |
| 2 | Convert all ten sessions, cross-session links, course contents, math check | not started |
| 3 | `texdiff` and `SYNC`, the checks on numbers and sources, first web-only edits | not started |
| 4 | Quizzes of sessions 1 to 5, quiz renderer | not started |
| 5 | Quizzes of sessions 6 to 10, try-it boxes, Colab and Binder links | not started |
| 6 | Pyodide feasibility test, then the widgets with the JSON fallback | not started |
| 7 | Polish, page weight, single-page version, alt texts | not started |

## Sessions

The column "synced to" is the commit of `lecture_notes/src` the Markdown of the session was
last brought in line with, the same as its line in `webnotes/SYNC`. A session whose `.tex`
changed after that commit has hunks to carry over, which `texdiff.py` lists.

| Session | Converted to Markdown | Pages built | Quizzes | Widgets | Synced to |
|---|---|---|---|---|---|
| 1 | no | no | no | no | |
| 2 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 3 | no | no | no | no | |
| 4 | no | no | no | no | |
| 5 | no | no | no | no | |
| 6 | no | no | no | no | |
| 7 | no | no | no | no | |
| 8 | no | no | no | no | |
| 9 | no | no | no | no | |
| 10 | no | no | no | no | |

## Decisions taken

On 2026-11-06 the lecturer answered the eight decisions of the plan. Fork to a web Markdown
master now. One page per section. Number plus slug in the URL, frozen in a manifest. MathJax 3
from the CDN. The legacy `docs/` build, local and committed. Inline quizzes after the equation
or figure they check. Pyodide for the widgets, with a feasibility test first and precomputed
JSON as the fallback. The staged toolkit, building from the Markdown master. The full list is
the last section of the plan.

## Pyodide feasibility test

Not run yet. Phase 6 writes here the load time of a first open, whether pyqula imports with
`micropip` and which dependency is missing if not, and the time of one band structure of the
honeycomb lattice.

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
