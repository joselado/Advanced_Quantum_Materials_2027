# Brief for an agent that edits pages of the web notes

This is the generic brief for an agent that brings pages of `webnotes/pages/sessionNN/` to the shape that
the lecturer locked on 2026-11-21. The coordinator adds to it the list of pages, a prefix for new files and a
scratch folder. The students are master students with a bachelor course in materials physics and in quantum
mechanics.

## Read first, in this order

1. `lecture_notes/WEB_NOTES_PLAN.md`, the sections "Figures and captions", "The shape of a page" and "Quizzes".
   These are the rules, and they win over this brief.
2. `webnotes/README.md`, the section "Blocks added for the web", whole, and "The lint of the prose".
3. The model page, `webnotes/pages/session03/05-the-berry-curvature-and-why-the-hall-conductivity-is-an-integer.md`,
   with its figure scripts in `webnotes/figures/session03/` and its script in `webnotes/scripts/session03/`.
4. `lecture_notes/writing_style.md`, which wins, and `VOICE.md` sections 2, 4.3, 5, 7 and 8. Every sentence that
   you write follows them.
5. Your pages, whole, and the pages that they refer to when you need an equation.

## What each page gets

- An opener of two or three sentences under the heading, with the question of the page and where we arrive.
- Paragraphs over about 150 words split where the idea changes. Every existing physics statement, number, link
  and figure stays, and text that is fine is not rewritten.
- A `recall` box after the opener when the page starts from a numbered equation of another page.
- A `key` box around the main result, one per page, two if the page has two results, none on a page of motivation.
- A `steps` fold under a result whose derivation the text tells in words, with unnumbered displays and the
  simplest case first.
- A `problem` with one `solution`, of five to fifteen lines, where something can be computed by hand.
- A `lab` box only with a verified source. The sources are the "In the lab" cells of the notebook of the session,
  or an article whose abstract you fetched and that states the number. Every number of a real material in the box
  is in the fetched text, and you quote that sentence in your report. No verified source means no box.
- Every quiz in the form of "A quiz is read alone", with question sentences of at most 15 words, the equation in
  the question, no reference by number to a section or a figure, and 3 options with feedback. The physics point of
  an existing quiz stays. Some quizzes have picture options and some have equations as options.
- Figures by the rules of "Figures and captions" of the plan. Every plot has its axes. A map over reciprocal space
  shows $k_x$, $k_y$ and the first Brillouin zone. A calculation that pyqula can do is a small script in
  `webnotes/scripts/sessionNN/`, which the figure script runs with `style.run_script` and which the student
  downloads with the attribute `script="NAME.py"` of the figure.
- The `comesback` box as the last block.

The order on a page is the heading, the opener, the recall box, the text with the key box and the steps folds at
their results, the figure of the result, the lab box, the quizzes, the problem, the try-it box and the comesback box.

## Hard rules

- Headings, ids, `\tag` numbers, file names, the manifest and the files of the toolkit are not changed. If a block
  misbehaves, report it.
- Only your pages and your own new files are edited. No default build, meaning no `build.py` without `--out`. No
  commit and no push.
- No recursive delete in the shell, since a safety check blocks it. Use new names.
- Physics is not changed silently. An error in the existing text is listed in the report and left.
- A sign is claimed only after you checked the convention with a number. The Berry curvature of the notes is
  $\Omega_n=-2\,\mathrm{Im}\langle\partial_{k_x}u_n|\partial_{k_y}u_n\rangle$, and the usual link-variable plaquette
  phase is minus this. The overall sign of $\sigma_{xy}$ is a convention.

## Checks before the report

- Every step of a fold, every solution and every number of a feedback is recomputed with a script of your own.
- Every figure script asserts the numbers that its caption or its quiz quotes.
- `python3 webnotes/build.py --out YOUR_SCRATCH/notes --session N --math` gives 0 errors on your pages.
- `python3 webnotes/lint.py --session N` gives no hit on your pages.
- Each page is looked at in a screenshot at 1000 px and at 390 px.

## The report

Per page, the blocks added, the quizzes rewritten and added, the figures and scripts added, each lab source with
the quoted sentence, the checks with their numbers, the result of the build and of the lint, what you could not
verify, and the errors found in the existing text.
