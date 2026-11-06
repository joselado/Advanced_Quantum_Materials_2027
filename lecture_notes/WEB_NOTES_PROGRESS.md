# Progress of the lecture notes as web pages

The plan is `lecture_notes/WEB_NOTES_PLAN.md`. This file is the tracker that each session
updates at its end, one line per phase and one per session. Last update 2026-11-06, phase 2, first half.

Start here. The first half of phase 2 is done: the toolkit handles all ten sessions and the Markdown of
sessions 1 and 3 to 10 is converted (session 2 is the pilot). The full build gives 156 pages, 0 errors, an empty
pending list, and a second build writes nothing. What is left is the proofreading of the Markdown against the
PDF, group by group, then the math check (`mathcheck/`), the notes column of the landing page and the link in
the README. Read `webnotes/README.md` and the section "What phase 1 found" of the plan first. The Markdown of
sessions 1 and 3 to 10 is still as converted, so a toolkit fix can still be applied with `--force`, but only
until the first hand edit of a session.

## Phases

| Phase | What | Status |
|---|---|---|
| 0 | Plan, tracker, prototype in the scratchpad, conversion test, decisions | done 2026-11-06 |
| 1 | Pilot on session 2, convert once to Markdown, toolkit stage 1, link from the video pages | done 2026-11-06 |
| 2 | Convert all ten sessions, cross-session links, course contents, math check | in progress, conversion done 2026-11-06 |
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
| 1 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 2 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 3 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 4 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 5 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 6 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 7 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 8 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 9 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |
| 10 | yes, 2026-11-06 | yes, 2026-11-06 | no | no | 2ee5256 |

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
- 2026-11-06. Phase 2, first half. Sessions 1 and 3 to 10 converted with the toolkit fixes below, 156 pages
  built (session 1: 16 sections, 3: 13, 4: 21, 5: 20, 6: 17, 7: 12, 8: 14, 9: 11, 10: 8, with the
  introductions), 0 errors, no pending reference, no `??`, a second build writes nothing. Nobody has edited the
  Markdown of these sessions yet.
