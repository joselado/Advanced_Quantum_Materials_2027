# Progress of the lecture notes as web pages

The plan is `lecture_notes/WEB_NOTES_PLAN.md`. This file is the tracker that each session
updates at its end, one line per phase and one per session. Last update 2026-11-06.

Start here. The next session does phase 1, the pilot on session 2, directly, since the lecturer
answered every open decision on 2026-11-06 and the plan is written to them. It reads the plan,
in particular "How a change reaches the page", "The toolkit", the phases and the appendix with
the prototype filter, then creates `webnotes/` with stage 1 of the toolkit, converts session 2
once into `webnotes/pages/session02/` and builds `docs/notes/session2/`. The first thing to
check is that `pandoc -t markdown` keeps the math, the tables and the boxes of the notes as
cleanly as the HTML writer did in the test.

## Phases

| Phase | What | Status |
|---|---|---|
| 0 | Plan, tracker, prototype in the scratchpad, conversion test, decisions | done 2026-11-06 |
| 1 | Pilot on session 2, convert once to Markdown, toolkit stage 1, link from the video pages | not started |
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
| 2 | no, pilot of phase 1 | no | no | no | |
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
