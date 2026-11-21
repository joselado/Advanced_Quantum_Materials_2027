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

### One page in two seconds

While a page is being edited, we render only that page. The keyword `--page FILE` takes the name of its Markdown
file and needs `--session N`. It writes that page on top of an earlier build of the session in the same folder, and
the checks run on the whole folder as usual.

```
python3 webnotes/build.py --out /tmp/mynotes --session 3                 # once, the whole session
python3 webnotes/build.py --out /tmp/mynotes --session 3 --page 05-the-berry-curvature-and-why-the-hall-conductivity-is-an-integer.md
```

The first pass of the build reads every page of the ten sessions to collect the anchors. It keeps the pandoc tree
of each page in `webnotes/.cache/ast/`, which git ignores, so only a page that changed goes through pandoc again.
The folder can be deleted at any time. A full build of the 171 pages takes about 45 s, and one page about 2 s.

A schematic is drawn again only when its own script, a helper `_NAME.py` that it imports, or the pyqula script that
it runs is newer than its SVG. A change of `figures/style.py` does not redraw anything by itself, since it would
redraw every schematic of the ten sessions, which takes more than ten minutes. After a change of the look in
`style.py` we ask for it with `--redraw`, which draws every schematic again. We then read the diff of the SVGs
before committing, since a few old scripts do not give the same file twice.

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
- The box `notebookbox` is a fenced div as converted. The blocks `quiz`, `tryit`, `comesback`, `key`, `recall`, `steps`,
  `problem` and `lab`, the schematics, the figures shown again and the merge and split of pages are described in the next sections. The block `widget` is described in
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

### How a plot is drawn

The rules are in `lecture_notes/WEB_NOTES_PLAN.md`, section "Figures and captions", and this is how they are
applied in a script.

- Every plot has its axes, with their names and the unit in the name, such as "$\sigma_{xy}$ in units of $e^2/h$".
  Ticks with numbers go at the values that the text quotes. `style.arrows` draws the two arrows of a curve plot.
- A map over reciprocal space shows $k_x$, $k_y$ and the first Brillouin zone, in the extended zone with the first
  zone dashed. `style.kmap(ax, B, values)` draws a quantity given on the reduced grid, `style.pyqula_kmap(ax, g, kx,
  ky, values)` draws what pyqula returns on its own window, and both draw the dashed zone. `style.kaxes(ax, ticks=2)`
  adds the labels and the ticks, and `style.draw_zone(ax, B)` draws the zone alone. The bare rhombus of the reduced
  zone is not used.
- A signed quantity has a diverging color scale with white at zero and a colorbar with numbers. Panels that are
  compared share the scale. The high-symmetry points are named, $\Gamma$, $K$, $K'$, $M$.
- The parameters of the model are in the caption, and they are those of the script. The caption says in which
  units the axes are.
- The small pictures of a picture quiz follow the same rules, with the axes and no other text.
- The labels are read at a width of 390 px before the figure is accepted.

### A pyqula script to download

A calculation that pyqula can do is done with pyqula, and the student downloads the script with a button under
the plot. The script is `webnotes/scripts/sessionNN/NAME.py`. It is only the calculation, written as a physicist
writes it, a few calls of pyqula with a few words on each, and it ends with its results in variables with plain
names. It has no plotting.

```python
# Berry curvature and Chern number of the Haldane model
from pyqula import geometry

g = geometry.honeycomb_lattice()  # honeycomb lattice
h = g.get_hamiltonian(has_spin=False)  # Hamiltonian with first-neighbor hopping 1
h.add_haldane(0.1)  # Haldane coupling, a gap that breaks time reversal
(kx, ky, omega) = h.get_berry_curvature(nk=120)  # Berry curvature of the filled band
chern = h.get_chern(nk=60)  # Chern number, it gives 1
```

The figure script gets its data by running that script, so the figure and the download are the same calculation,
and then it only plots.

```python
d = style.run_script('session03/berry_curvature_honeycomb.py')     # the variables of the script
im, B = style.pyqula_kmap(ax, d['g'], d['kx'], d['ky'], d['omega_haldane'] / (2 * np.pi), cmap='RdBu_r', vmin=-12, vmax=12)
```

On the figure the attribute `script` names the file, and the build puts the button "Download the pyqula script"
under the plot and copies the script to `docs/notes/scripts/sessionNN/`.

```
![Caption.](figures/web/session03/berry_haldane.svg){#sch:s03:berry_haldane alt="..." script="berry_curvature_honeycomb.py"}
```

The build makes an error of a script that is missing, that does not parse, that does not import pyqula, that
imports a plotting package, that defines a function or a class, or that has more than 40 lines. It also makes an
error of a figure that names a script and does not draw from it with `style.run_script`. A figure is redrawn when
its own script, a helper `_NAME.py` that it imports or the pyqula script that it runs is newer than its SVG. The sign and the units of what pyqula returns are checked with a
number before a caption states them, and the checks stay in the figure script as `assert` lines. A picture that is
an option of a quiz has no button, but it is drawn from a script in the same way, and a figure in the question of a
quiz can have one. A calculation that pyqula cannot do stays in
numpy and has no button.

### Quiz

A multiple-choice question with exactly 3 options, one correct and two wrong. Each option starts with `[x]` for
the correct one or `[ ]`. The text before the list is the question. Under every option, indented by 4 spaces
and after an empty line, goes its feedback, in the form of the verdict first. For the correct option it is a
short reason why it is correct, for a wrong option it is a counterexample, a case with numbers where the option
fails. If one option has feedback, all three must have it. The explanation after the list is optional and is
for the general point. Math works everywhere.

```
::: quiz
What is the energy of [(2.9)](#eq-2-9) at $\varphi=\pi/2$?

- [ ] $0$

    This is false. Take $t=1$ and $\eta=0.2$. Then $\epsilon_{\pi/2}=0.4$, which is not zero.

- [x] $2\eta$

    This is true. The term with $t$ vanishes since $\cos(\pi/2)=0$, and the second term gives $+2\eta$.

- [ ] $-2\eta$

    This is false. For $\eta=0.2$ we get $+0.4$, because $\cos\pi=-1$.

Optional, the general point, for example what the energy measures.
:::
```

The student sees a block with the label "Question", the question on a tinted band, and the options as buttons.
A click marks the option "True" or "False" with a mark and a word, and opens its feedback below it, headed
"Why it is correct" or "Counterexample". The other options can be tried too, and a second click closes the
feedback. Tab and Enter or Space work, a hidden status line announces the verdict (`aria-live`), and MathJax
typesets the feedback when it opens. Without JavaScript a `<details>` lists the three verdicts with their
feedback.

All 212 quizzes of the ten sessions are in this form, each with exactly 3 options. The old form
(the options with `[x]` and `[ ]` and the explanation after the list, label "Quick check") still builds, but
`check.py` counts it, and the build prints the number of quizzes in the old form and of quizzes without 3 options.
`check.py` makes an error of a quiz with feedback that has not exactly 3 options or no correct option. A new
quiz is written with the feedback and the 3 options together.

On a screen of 480 px or less the verdict of an option goes under its text. The math inside an option is not a
tab stop (`notes.js` sets its tabindex to -1 after MathJax), so Tab goes from option to option.

### A quiz is read alone

A student may open a page in the middle of the notes and go to a question, so a quiz does not need the text
around it. This gives four rules for a new quiz, and the lint lists the old ones that do not follow them.

- The sentences of the question are short, 15 words at most with each math fragment counted as one word. The lint
  reports a longer one as `quiz-long`.
- An equation that the question needs is written in the question, as a display without `\tag`, with its symbols
  named. A question does not send the reader to "equation (2.8)".
- When a quiz still refers to a numbered equation with a link, `[(3.4)](#eq-3-4)`, the build shows that equation
  inside the quiz, with its number. An equation of the question or of an option goes under the question, and an
  equation that only the feedback of one option uses goes at the end of that feedback. An equation that the quiz
  already displays is not shown twice. Nobody writes anything for this, the TeX comes from `labels.json`.
- A quiz does not refer to a section, a figure or a schematic by its number. A figure that it needs is shown in
  it, as the next section says. The lint reports the reference as `quiz-ref`.

Some questions should have an equation in them, and some should be answered by reading a picture, since this is
how the material of the course is used.

### Picture options

The three options of a quiz can be three pictures, when the answer is to choose one of them. An option is then one
image and nothing else, a web schematic written as `![alt text](figures/web/sessionNN/NAME.svg)`, and its
feedback goes under it as usual. The `alt` is required, and it says what is drawn without saying whether the
option is right. All three options are pictures or none is.

```
::: quiz
Each map shows the Berry curvature $\Omega(k)$ of the filled band. Which lattice has $\sigma_{xy}\neq 0$?

- [ ] ![A map where the corners of the zone alternate between red and blue spots.](figures/web/session03/quiz_berrymap_staggered.svg)

    This is false. The red spots and the blue spots have the same weight, so the integral is zero.

- [x] ![A map where all the corners of the zone have a blue spot.](figures/web/session03/quiz_berrymap_haldane.svg)

    This is true. All the spots are blue, so nothing cancels, and the integral is $-2\pi$, which is not zero.

- [ ] ![A map with strong blue spots and weak red spots at the corners.](figures/web/session03/quiz_berrymap_both.svg)

    This is false. The two kinds of spots do not look the same, but their integrals have the same size.
:::
```

The student sees the three pictures side by side, also on a phone, and the feedback of a clicked option opens
under the row, with the letter of its option. The pictures have their axes and no other text, the same color scale
and the same size, and each one is a script of its own, since a script writes one SVG. The shared code goes in a file that
starts with an underscore, such as `figures/session03/_berrymap.py`.

### A figure inside a quiz

A quiz can hold a figure in its question and in the feedback of any option, of every kind: a new schematic, a
figure shown again, one panel of a Blender figure. The figure is written like any other, alone in its paragraph,
and in the feedback it is indented by 4 spaces with the text of the option. It is drawn at most 360 px wide and
centred, and it keeps its `alt`, which is required and checked. The caption is short and optional.

A figure in a quiz has no number of its own and takes no `id`. A schematic shows its caption as written, with no
"Schematic N.", so that the text never refers to a figure that is hidden until a click. A figure shown again keeps
"Figure 2.2, shown again." and its link to the original, and a figure with an id inside a quiz is an error, since
the first display of a figure belongs in the body of the page. A feedback figure is loaded only when its option
is opened, since the images are lazy and the feedback is hidden. Without JavaScript the `<details>` lists the
feedback, and its figures load when it is opened. `check.py` gives a warning for an SVG over 200 kB, and a figure
of a quiz should be a few tens of kB.

```
::: quiz
At which phase would the minimum be if the hopping had the opposite sign?

![The band for $t>0$.](figures/s02f02_cosband.svg){alt="A cosine band with its density of states."}

- [x] At $\varphi=\pi$.

    This is true. The sign change turns the band upside down.

- [ ] At $\varphi=0$.

    This is false. For $t=-1$ the energy at $\varphi=0$ is the top of the band.

    ![The mirror argument.](figures/web/session02/mirror_field.svg){alt="A charged plane with a mirror line."}

- [ ] At $\varphi=\pi/2$.

    This is false. The energy is $0$ for either sign.

    ![Panel c.](figures/s02f04_dirac.svg){panel="c" alt="A hexagonal zone with a Dirac cone."}
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

### Where this comes back

Every page ends with a small box titled "Where this comes back", which links forward to the later pages and
sessions where the concepts of the page return. Where nothing returns, the box links the next natural step. It
goes after the last paragraph and the last quiz or try-it box of the page. The shared list of the concepts and
of the pages that use them is `lecture_notes/WEB_NOTES_CONCEPTS.md`.

```
::: comesback
- In Session 4 the Landau levels are flat bands with Chern number one, in Section [4.4](#sec-4-4).
- In Section [6.6](#sec-6-6) a flat band makes the Stoner criterion true for any interaction $U>0$.
:::
```

The content is free Markdown, usually a short list with one sentence per item, or one short paragraph. The build
adds the title and the class `comesback`, and `notes.css` gives it the look of the other boxes. A box without any
link is an error of the build. A plain "Session N" counts as a link, since the build links it before it checks
the box. The example above is on `session02/11b-flat-bands-from-the-geometry-of-the-lattice.md`.

To look at the box, we build privately and take two screenshots, at the width of a laptop and of a phone. The
window is tall, so that the box at the end of the page is in the picture.

```
python3 webnotes/build.py --out /tmp/mynotes --session 2
for w in 1000 390; do
  google-chrome --headless --no-sandbox --hide-scrollbars --virtual-time-budget=8000 --window-size=$w,16000 \
    --screenshot=/tmp/box_$w.png file:///tmp/mynotes/session2/11b-flat-bands-from-the-geometry-of-the-lattice.html
done
```

### To remember

The main result of a page goes in a box, so that a reader who skims the page sees it first. The box holds the
equation, which keeps its `\tag`, and one or two sentences that say what it means, with the symbols named. A page
has one such box, or two when it has two results, and a page of motivation may have none.

```
::: key
The Hall conductivity of a set of filled bands is

$$\sigma_{xy} = \frac{e^2}{h}\, C, \qquad C = \sum_{n\ \text{filled}} \frac{1}{2\pi}\int_{\text{BZ}} \Omega_n(k)\, d^2k. \tag{3.4}$$

It is built only from the wavefunctions, and not from the band energies. For a gapped system $C$ is an integer.
:::
```

The build adds the title "To remember". The name of a new concept still comes in the text after the box, where
it is built.

### From before

A page should be readable without the pages before it. When a page starts from an equation of another page, a
box shows that equation again, with its number, and the text of the box says in words what it is and what its
symbols are. The box goes right after the opening sentences of the page.

```
::: {.recall eq="3.2"}
This is the Kubo formula of Section [3.4](#sec-3-4) for the Hall conductivity. The bands $n$ are filled and the
bands $m$ are empty.
:::
```

`eq` takes one number or several, `eq="3.2 3.3"`. The build adds the title "From before" and the equations, and
nobody copies the TeX. A number that no page holds, a box with no text and an equation of the same page are
errors of the build.

### The steps of a derivation

When the text tells a derivation in words, the steps go in a fold under the equation that they reach. The fold is
closed, so a reader who trusts the result reads on, and a reader who wants the algebra opens it. The `title` is
required and says which equations the steps join. It is plain text, with no math and no link.

```
::: {.steps title="From the Kubo formula (3.2) to the Chern number (3.4)"}
The first step is the identity [(3.3)](#eq-3-3). We take the derivative of $H|n\rangle=\varepsilon_n|n\rangle$,

$$(\partial_\mu H)|n\rangle + H|\partial_\mu n\rangle = (\partial_\mu\varepsilon_n)|n\rangle + \varepsilon_n|\partial_\mu n\rangle,$$

and we multiply it from the left by $\langle m|$.
:::
```

The student sees one line, "The steps" and the title, and a click opens the text. It is a `<details>`, so it needs
no script and it works with the keyboard. The equations inside have no `\tag`, so the numbers of the notes do not
move, and the text refers to the numbered equations of the page with the usual links. The simplest case comes
first, such as one filled band before several. Every step is recomputed by a second reader before it goes to the
site. A steps box without a title is an error of the build. The example is on
`session03/05-the-berry-curvature-and-why-the-hall-conductivity-is-an-integer.md`.

### Problem with a solution

A pen-and-paper problem, which the quizzes do not cover, since they only ask to recognize the answer. The box holds
the statement and one `solution` div, which is a fold like the steps. The outer fence has four colons, so that the
inner one closes first.

```
:::: problem
Show that the Berry curvature $\Omega_n(k)$ does not change when $|u_n(k)\rangle$ gets a phase $e^{i\varphi(k)}$.

::: solution
We write $|u'\rangle=e^{i\varphi}|u\rangle$. The derivative of the new state is ...
:::
::::
```

The statement says what to show or to compute, and the solution ends with one or two sentences on why the result
matters for a measurement or for a calculation. A problem needs exactly one solution, and a solution outside a
problem is an error of the build. The box goes after the quizzes of the page and before the try-it box.

### In the lab

A short box that ties the result of the page to a real material, with one material, one number with its unit and
the probe that measures it. It must hold a link to the measurement, since a number of a real material needs its
source, and a box without an external link is an error of the build. The first source is the "In the lab" cell of
the notebook of the session, and the number is read from the article and not from memory.

```
::: lab
In a Hall bar we measure the Hall resistance, and for $C=1$ equation [(3.4)](#eq-3-4) gives $h/e^2=25.8$ k$\Omega$.
In twisted bilayer graphene aligned to hBN this value is measured at zero magnetic field, within $0.1\%$. The
measurement is in [this article](https://www.science.org/doi/10.1126/science.aay5533).
:::
```

The box can hold a schematic of the measured quantity, written like any other schematic, with its id and its
`alt`. Such a plot is computed with the model of the page, in the form that the experiment gives, and its caption
says what is computed and what is left out. The box goes after the figure of the result and before the quizzes.

## Links to a session

A plain "Session N" in the prose, with N from 1 to 10, is linked by the build to the index page of that session,
with the right relative path, so the text writes "Session 6" and never a hand-made link. The word must be
capitalised, and "session 6" in lowercase stays plain text. The link is not made inside a heading, a link, math
or code, in a quiz option, which is a button, on the index page of the session itself, or for a session that
has no manifest. "Session 4.2" and "Sessions 6 and 9" are not linked. The pass is `SessionLinks` in `filters/web.lua`, and it runs before the pass
that resolves the anchors and renders the blocks.

## The tools around the build

Besides the build and the lint there are six tools, built on 2026-11-21 so that the next sessions cost less and
go wrong less. Each has its own page of documentation.

- `inventory.py`, the pages of a session from the manifest, with what each has and its lint hits, and the
  skeleton of the plan of the session in `plans/sessionNN.md`. `python3 webnotes/inventory.py --session N --plan`.
- `conventions/sessionNN.md`, the signs, the units and the pyqula facts of a session, each checked by a number.
- `figures/physcheck.py`, the Berry curvature, the Chern number, the Zak phase and the gap in the convention of the
  notes, and `scripts/RECIPES.md`, the pyqula recipes of the course. See `docs/helpers.md`.
- `labsource.py` and `sources/`, the stored text of the sources of the lab boxes, against which the lint checks
  every number of a real material. See `docs/gates.md`, which also describes the lint categories `opener`, `key`,
  `long-paragraph`, `lab-source` and `lab-number`.
- `layout.py`, the check of the layout in the browser at 1000 and 390 px, with no image to read. See
  `docs/layout_and_verify.md`. Headless Chrome does not make a window narrower than 500 px, so the screenshot
  commands of this file do not show a phone, and the layout check is the phone check.
- `build.py --verify`, which runs every check script of `checks/`, and the warning `AXES-WARNING` of
  `figures/style.py` for a plot without named axes. See `docs/layout_and_verify.md`.

The order in which a session is done, with the test between the steps, is the skill `aqm-webnotes-session`, and
the brief of the agents is `lecture_notes/WEB_NOTES_BRIEF.md`.

## The lint of the prose

`lint.py` reads the Markdown of the pages and lists what does not follow `lecture_notes/writing_style.md`. It
changes no file, it prints each hit as `file:line` with its category and a piece of the line, and at the end a
total per category and per session. It always exits with 0, so it is a list to work through and not a check of
the build.

```
python3 webnotes/lint.py --session 6
python3 webnotes/lint.py --summary
python3 webnotes/lint.py --session 6 --category residue --category punctuation
```

The checks run on the prose only. Headings, the fence lines of blocks with their attributes, display and inline
math, code, link targets, image sources and attribute braces are removed before a line is checked, so a heading
or an id is never reported, since both are frozen. The text of a link, a caption and the feedback of a quiz option
are prose and are checked. The categories are the following.

- `residue`, a sentence about the recording and not about the physics, "transcript", "slides", "instructor",
  "recording", "lecturer", "spoken", "narrated", "this year", "previous editions" and "raw". The sentence is
  deleted, and a fact that matters is kept as physics.
- `backslash-quote`, a literal `\"` in prose, left over from the conversion.
- `banned`, the words of `writing_style.md` and of sections 7 and 8 of `VOICE.md` ("rigorous", "it is easy to
  see", "notably", "well-known", "today", ...), contractions and exclamation marks.
- `exactly`, "exactly", "simply" and "precisely", printed as a warning, since they stay when they state a physics
  fact such as an exact mapping.
- `long-sentence`, a sentence of more than 35 words, with each math fragment counted as one word.
- `punctuation`, a colon, a semicolon or an em-dash in prose. The fixed label `**Notebook check-in:**` of a
  converted notebook box is not reported.
- `session-case`, "session N" in lowercase, which the build does not link.
- `ref-format`, "eq. [", "Eq. [", "fig. [" and "section [", which become "equation [(N.M)](#eq-N-M)" and
  "Section [N.M](#sec-N-M)", as in `lecture_notes/WEB_NOTES_NOTATION.md`.
- `comesback`, a page without a `::: comesback` block, the index pages included.
- `quiz-long`, a sentence of more than 15 words in the question of a quiz, with each math fragment as one word.
- `quiz-ref`, a quiz that refers to a section, a figure or a schematic by its number, so that it cannot be read
  alone. A numbered equation is not reported, since the build shows it inside the quiz.

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
- `lint.py`, the lint of the prose of `pages/`, read-only, described above.
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

## State of the figures (2026-11-06)

The ten sessions hold 233 figures in 171 pages. On the pages there are 59 PDF figures and 51 figures shown again
(Blender panels included), and 69 schematics drawn for the web. In the quizzes there are 47 new schematics
and 7 figures shown again, in the question or in the feedback of one option. Of the 116 scripts in
`webnotes/figures/sessionNN/`, the ones with a figure in a quiz are named by the quiz that uses them.
The default build gives 0 errors, 5435 math fragments with 0 errors, and a second build writes nothing.
The only SVG warnings are the files over 200 kB, and the largest is `figures/web/session05/nambu_bands.svg`
with 560 kB, which is a candidate for a lighter plot.
