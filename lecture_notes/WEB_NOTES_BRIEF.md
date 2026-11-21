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
6. `webnotes/plans/sessionNN.md`, the blocks of your pages, which say what to build on each page.
7. `webnotes/conventions/sessionNN.md`, the signs and units of the session, checked by number. A sign comes from
   this sheet.
8. `webnotes/scripts/RECIPES.md` for the pyqula calls and `webnotes/docs/helpers.md` for the module
   `webnotes/figures/physcheck.py`, which gives the Berry curvature, the Chern number, the Zak phase and the gap.
   This code is not written again.

The pages of a session are taken from `python3 webnotes/inventory.py --session N`, which reads the manifest. A
group is at most three pages.

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

## What went wrong in Session 3

These are the real mistakes of the first session that was done, found by the independent checks. Each one is a
kind of mistake, and the same kind will come up in the other sessions. Read them before you write.

- A sign stated from memory. Two figure scripts summed the plaquette phases with the opposite sign of the formula
  of the page, for a Haldane coupling of opposite sign, so their picture was right by accident. A sign goes on a
  page only after a number confirms it, and it is taken from the conventions sheet of the session.
- A continuum result quoted for a lattice. "Each Dirac point gives about $\pi$" was written for a staggered
  potential of 0.5, where each valley gives $0.7\pi$. The first correction, $0.6\pi$, was wrong too, and only an
  assert found it. The number is computed on the model of the page, and the assert is kept.
- A formula without its range. The gap $6\sqrt3\,t_2$ holds only for $t_2<0.19$, the factor nine between two
  Landau levels holds for energies measured from the bottom of the band, and the splitting of the end states holds
  when $t^L$ is small. The condition is written next to the formula.
- A lab box that says more than its source. Two separate sentences of an abstract were joined into one claim, a
  resistance per mode was given that the abstract does not state, and a property of the sample came from an editor
  summary. The box says what the fetched text says, and our own reading is a separate sentence that is marked as ours.
- A parameter of pyqula taken for the parameter of the page. `h.add_haldane(0.1)` is a second-neighbor hopping of
  0.087 with a gap of 0.90, while $t_2=0.1$ of the text gives 1.04. The page says which one it quotes.
- A number from one random realization. "A gap of about $0.2\,t$" was one seed, and ten seeds gave 0.1 to 0.4. A
  number that depends on a realization is given as a range, from several realizations.
- A sentence that reads as its converse. "The Chern number vanishes, so time-reversal symmetry is kept" suggests
  that a zero Chern number implies the symmetry. The cause is written first and the consequence second.
- A statement that a renaming changes the physics. "Which point we call $K$ fixes the sign of $C$" is false, since
  the two quantities that change sign cancel. Before a convention is blamed, the result is recomputed with it changed.
- Two pages that disagree. The folds of two sections gave the same constant with opposite signs. A quantity that
  another page also states is looked up there before it is written.
- A caption or an alt text that says more than the picture shows. A gap was said to close on a grid with no point
  at the closing, and a band was counted that the window cut. The caption is read against the drawn figure.
- An old quiz that contradicts the page. Three old quizzes were wrong, one against the figure of its own page. An
  existing quiz is checked like a new one when it is rewritten.
- A figure script that writes files. A call of `h.get_bands()` in a figure script left output files next to the
  figures. pyqula is called inside the script that `style.run_script` runs, or with no file written.
- A page list from memory. Section 3.9a lives in the file of Section 3.8. The pages are taken from the manifest.

## Checks before the report

- Every number that a page quotes, in a caption, a feedback, a fold or a solution, is an `assert`, in the figure
  script that draws it or in the check script of the page, `webnotes/checks/sessionNN/PREFIX_PAGE.py`. The check
  script finds the repository from its own path and writes no file.
- Every number of a lab box is found in its stored source. The source is fetched with
  `python3 webnotes/labsource.py --session N URL`, and `python3 webnotes/labsource.py --check N` shows the
  sentence behind each number. A value that is our own conversion is marked on the box with `ours="..."`.
- `python3 webnotes/build.py --out YOUR_SCRATCH/notes --session N` once, and then
  `--page FILE` for each edit, which takes about two seconds. At the end `--math` gives 0 errors on your pages.
- `python3 webnotes/lint.py --session N` gives no hit on your pages, with the categories `opener`, `key`,
  `long-paragraph`, `lab-source`, `quiz-long` and `quiz-ref` included.
- `python3 webnotes/layout.py YOUR_SCRATCH/notes --session N --page FILE` gives no finding at 1000 and 390 px. It
  measures the layout in the browser, with the folds open and a quiz option clicked. A screenshot below 500 px is
  not possible with headless Chrome, so this is the phone check, and a screenshot is only for the look.
- `python3 webnotes/build.py --verify --session N` gives all OK.

## The report

Per page, the blocks added, the quizzes rewritten and added, the figures and scripts added, each lab source with
the quoted sentence, the checks with their numbers, the result of the build and of the lint, what you could not
verify, and the errors found in the existing text.
