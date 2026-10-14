# Plan for the Blender figures of the lecture notes

This file is the plan for redoing the sixty-one figures of the lecture notes as Blender renders,
in the way the notes of the sibling course, Advanced Computational Methods in Physics, were done.
It is written for a session that starts with no other context, so it fixes the pipeline, the page
metrics, the look, the order of the work, and then gives one entry per figure. The session that
executes it reads `CLAUDE.md`, `VOICE.md` and `lecture_notes/writing_style.md` first, since every
caption it touches is prose of the notes.

## What we are doing and what stays fixed

Every figure of `lecture_notes/src/figures/sNNfMM_name.tex` is today a TikZ or pgfplots drawing
inside the `aqmfigure` environment of `src/figures_preamble.tex`. We will replace the drawing by a
rendered image with the labels set in LaTeX on top of it, as the sibling course did, and we will do
it for all sixty-one figures, including the ones whose content is a plotted curve, so that the whole
set has one look. A curve becomes a tube in the scene and a density of states or a filled region
becomes a thin slab, with the numbers behind it computed inside the figure script rather than
sketched.

Three things do not change. The file `sNNfMM_name.tex` keeps its name, keeps the `aqmfigure`
environment and keeps its label, so that every `\ref{fig:...}` of the sessions stays valid and
`sessions/*.tex` is not edited, with one exception given below. The placement in the text, recorded
in the header comment of every figure file as `% Placement: ...`, stays where it is. And every
physics statement of the caption stays, since the captions were checked against the text in the
last rewrite.

The exceptions are the six figures of the section "Figures that are better replaced than redrawn",
whose pointing sentence in the text changes with the drawing, and a panel letter or a position word. When the prose says "figure 8.4a" or the
caption of another figure says "as in figure 6.3(a)", the new drawing has to keep that panel under
that letter, or the prose has to be edited with it. The places are found with

```
grep -n 'ref{fig:[^}]*}[ ~]*(\?[a-e]\b' src/sessions/*.tex src/figures/*.tex
grep -n 'ref{fig:[^}]*}(' src/sessions/*.tex src/figures/*.tex
```

and today they are `fig:s09:nesting` panels a and b, `fig:s08:parton` panels a and b,
`fig:s06:frustration` panel a from the caption of `s06f04`, `fig:s08:magnonspinon` panel b from
the caption of `s08f03`, and the words "on the left", "on the right", "at the top", "at the bottom"
inside several captions, which must describe the new layout.

## The pipeline, taken from the sibling course

The reference implementation is in
`/u/40/ladovj1/unix/Documents/programs/Advanced_Computational_Methods_Physics_2026/lecture_notes/src/figures/`,
and its two commits are `bc533cc` (the pilot and the pipeline) and `efdc3f9` (the other
twenty-four figures). Read `blender/figlib.py`, `blender/s1_2_two_interactions.py`,
`src/two_interactions.tex` and `blender/build_figure.sh` there before writing anything here. The
idea is the following. A Python script builds one scene in Blender, renders it with Cycles onto a
shadow catcher with a transparent background so that it sits on the white page, and writes the
camera position of every point where a label will go. No text is rendered. A standalone TikZ file,
the overlay, places the image and sets every label at those points in the fonts of the notes, and
a shell script turns the overlay into the figure PDF that the notes include. The labels stay vector
text at the size of the notes, the image carries the shapes, and a label can be moved or reworded
without rendering again.

Here the layout is

```
lecture_notes/src/figures/
  sNNfMM_name.tex          the wrapper the session \input{}s: aqmfigure, label, caption,
                           and one \includegraphics of the figure PDF, nothing else
  blender/
    figlib.py              the shared helpers, copied from the sibling and extended (below)
    figlib_sNN.py          helpers used by one session only
    sNNfMM_name.py         one script per figure, renders one or several images
    build_figure.sh        render to PDF, adapted to the paths here
    check_sizes.sh         prints the size on the page of every figure PDF and flags the tall ones
    out/                   the renders: *.jpg and *_anchors.tex are tracked, *.png is ignored
  overlays/
    sNNfMM_name.tex        the standalone TikZ overlay with the labels
  pdf/
    sNNfMM_name.pdf        the figure as included by the wrapper
```

The sibling kept its overlays in `figures/src/` and its PDFs in `figures/<session>/`, which would
collide with the wrappers that live directly in `figures/` here, so the names above are the ones to
use. The wrapper becomes

```latex
% Session 3 -- the SSH chain: the same bulk, two dimerizations, two spectra.
% Placement: sec. "The SSH model", after the dangling-site paragraph.
% Rendered by figures/blender/s03f03_ssh.py, labels in figures/overlays/s03f03_ssh.tex.
\begin{aqmfigure}{fig:s03:ssh}{<caption>}
\includegraphics{figures/pdf/s03f03_ssh.pdf}
\end{aqmfigure}
```

with no `width=` on the `\includegraphics`, since the size of the PDF is the size on the page and
a rescaling would shrink the label fonts. `aqmfigure` wraps the body in `adjustbox{max
width=\linewidth}`, which leaves a PDF of width `\linewidth` or less alone, so nothing is scaled as
long as the width rule below is respected. The overlays are standalone documents and do not load
`figures_preamble.tex`, so the three colors they need live in `overlays/aqmcolors.tex`, which every
overlay `\input`s, and `figures_preamble.tex` itself stays as it is.

The render runs with Blender 5.2.2, which is at
`/u/40/ladovj1/unix/apps/blender-5.2.2-linux-x64/blender`. The `blender` on the PATH is 2.79 and
does not run `figlib.py` at all. The command, as in the sibling, is

```
B=/u/40/ladovj1/unix/apps/blender-5.2.2-linux-x64/blender
$B -b --factory-startup --python blender/s03f03_ssh.py -- still     # 50 %, few samples, quick look
$B -b --factory-startup --python blender/s03f03_ssh.py -- final     # full size, 256 samples
$B -b --factory-startup --python blender/s03f03_ssh.py -- anchors   # only the anchors file
./blender/build_figure.sh s03f03_ssh                                 # jpg, overlay, pdf/s03f03_ssh.pdf
```

This host has no GPU and the D22 machine that rendered the sibling's figures does not resolve from
here, so `FIGLIB_GPU` stays unset and Cycles runs on the fourteen cores of this machine. Time the
`final` of the pilot and budget the rest from that number, and run the finals of a session as one
background batch rather than one at a time in the foreground. If the pilot's `final` at 256 samples
is slow, 128 samples with the denoiser on is enough for print at this size, and the number goes into
`setup_render` once rather than into each script. Blender's own Python has numpy
(2.3.4), so the scripts compute their curves and eigenstates themselves and import nothing beyond
`numpy`, `bpy`, `bmesh` and `mathutils`. `build_figure.sh` needs `PIL`, `pdflatex` and `ps2pdf`,
which are all present.

## Page metrics and the size rule

The notes are A4 with 2.7 cm margins, so the text width is 15.6 cm and the text height is 24.3 cm.
The sibling is letter with a 16.19 cm text width, and its overlays hard-code that number, so the
first thing to change in every overlay is `\setlength{\figw}{15.6cm}`. The anchors are written in
units of `\figw`, so `\figw` in the overlay is the width at which the image is placed, and the
wrapper includes the PDF at its natural size, meaning that the three widths, the camera, the overlay
and the page, agree by construction.

The figures of the sibling run across the full text width and several of them are tall. Here the
figures have to sit with the text, so the hard rule is that the image is at most 7 cm high. The
image with its caption then stays under half of the text height, which is 12 cm, so that a figure
never takes a page for itself and the paragraph that refers to it stays on the same spread. Several
captions run twelve to fourteen lines of `\small`, which is 5 to 6 cm on their own, and the entries
of those figures (`s03f05`, `s05f03`, `s05f05`, `s06f02`, `s07f02`, `s10f05`, `s10f06`) give a
larger aspect so that their image lands at 5 to 5.5 cm. At the full width of 15.6 cm the 7 cm bound
means a camera `aspect` of at least 2.2, and the entries below give an aspect for every figure. A scene that is not wide by nature is not stretched. It is rendered
narrower, at 0.6 to 0.8 of the text width, with `\figw` set to that width in the overlay (9.4 cm,
10.9 cm or 12.5 cm), and it is still centered by `aqmfigure`. The check is `check_sizes.sh`, which
runs `pdfinfo` on `pdf/*.pdf`, converts the page size to centimeters (72 bp per inch, so 28.35 bp
per centimeter), counts the lines of the caption in the wrapper, and prints every figure whose
height is above 7 cm or whose width is above 15.6 cm together with its caption length. Run it before
every checkpoint.

Every label stays inside the rectangle of the image. The overlay is a `standalone` with
`border=0pt`, so its page is the bounding box of the TikZ picture, and a label anchored outside the
image makes the PDF wider than the image, `adjustbox` then shrinks it to `\linewidth`, and the fonts
shrink with it. A width above 15.6 cm in the output of `check_sizes.sh` is a label that sticks out,
not a camera problem, and the fix is to move the label or to leave room for it in the scene.

## Several images per figure

The default is the sibling's one scene with its panels side by side, since one camera and one
light keep the scale and the shading the same across the panels, and one anchors file is simpler.
Panels that stand at different depths in the same scene, a front row and a back row as in the
sibling's `cdw_limits`, are the cheapest way to put two states of the same chain in one image.

A figure uses several renders when its panels need different cameras, for instance a side view and
a top view of the same magnon, or different scales, for instance a lattice next to a band structure
whose energy axis would otherwise be squeezed, or when a curve panel and a real-space panel have
nothing to share. For this `figlib.py` gains a second entry point, `main_panels`, which takes a
list of named panels,

```python
F.main_panels(NAME, [('a', build_a), ('b', build_b)])
```

and resets, builds and renders each panel on its own into `out/<NAME>_<panel>.png` with its anchors
in `out/<NAME>_<panel>_anchors.tex`, where the anchor names carry the panel as a prefix. Each
`build` sets its own camera and aspect. The sibling's `F.main(build, NAME)` is kept exactly as it
is, with the same argument order, so that a one-panel script reads as in the sibling. In the overlay every panel is
placed in its own scope,

```latex
\begin{scope}[shift={(0,0)}]
  \setlength{\figw}{7.6cm}
  \node[anchor=south west, inner sep=0pt] at (0,0)
    {\includegraphics[width=\figw]{../blender/out/s06f05_magnon_a.jpg}};
  \input{../blender/out/s06f05_magnon_a_anchors.tex}
  ...labels of panel a...
\end{scope}
\begin{scope}[shift={(8.0cm,0)}]
  \setlength{\figw}{7.6cm}
  ...
\end{scope}
```

and since the `\coordinate` lines of the anchors file are evaluated when they are read, each one
lands in the scope of its panel at the right width without any change to the writer in `figlib.py`
beyond the prefix. The widths of the panels and their gaps add up to the figure width, and the
tallest panel fixes the height, so the height rule is applied to the panels and not only to the
figure.

## The look

The materials, the lights, the orthographic camera and the shapes come from the sibling's
`figlib.py`, so that the notes of the two courses read as one family. The spin arrows keep their
up and down gradients, the electrons their cyan, the sites their dark discs, the bonds their grey
rods, the tensors their teal rounded cubes with rods for legs, the occupations their glass cups,
and the ghosts their translucent copies. Copy `figlib.py` as it is and extend it, do not fork its
style. The docstring reference to the course films (`videos/common/scene.py`) is removed, since this
course has no films.

The labels in the overlays follow `figures_preamble.tex` and not the sibling's `coursedark` and
`costamber`. Normal labels are black in `\small`, panel letters `(a)`, `(b)` are `\small\bfseries`
as `aqmpanel` is, the accent text is `aqmaccent` (31,78,121), the anomalous or broken element is
`aqmbroken` (168,42,34), and the de-emphasized text is `aqmmuted` (125,125,125). These three
colors are defined once in `overlays/aqmcolors.tex` with the same values as in the preamble. Inside the scene the same roles are kept.
`figlib.py` gains `ACCENT_AQM` and `BROKEN` as the linear-RGB versions of the two colors (convert
with the sRGB to linear formula in a helper `srgb(r, g, b)` taking the 0 to 255 values), and the
broken color marks the one element that is anomalous in a figure, the frustrated bond, the
unpaired Majorana, the flipped plaquette, the impurity. The rule of the preamble holds in the
scene as well, meaning that every distinction carried by a color is also carried by a shape, a
height or a weight, so that the figures survive a greyscale print.

Curves need a few shapes that the sibling did not have, and they go into `figlib.py` so that
every session uses the same ones. `tube(name, points, r, rgb)` sweeps a thin cylinder with spheres
at the joints along a list of points, which is the sibling's `figlib_s3.arc` made general, and is
how every band, dispersion, response function and envelope is drawn. `axis(name, p0, p1)` is a thin
rod with a small cone at its end, in the bond grey, and the tick and axis labels are anchors.
`profile(name, xs, ys, depth, rgb)` is a thin slab whose top edge follows a curve, for a density of
states or a particle-hole continuum. `surface(name, f, xr, yr, nx, ny, rgb)` is a mesh of a height
function, for an energy landscape, a paraboloid or a Dirac cone. `marker(name, loc, kind)` is a
small ball, a ghost ball or a cross for a point on a curve. A level ladder, the single-particle
spectrum that several sessions draw, is a column of short rods, in the accent color for the levels
in a gap and in the site color otherwise.

Numbers are computed, not drawn by hand. The Lieb and kagome bands come from diagonalizing the
Bloch Hamiltonian along the k-path, the localized states from diagonalizing the N = 89 chain, the
Stoner function and the Lindhard function from their closed forms, the Yu-Shiba-Rusinov energy from
equation (9.10), the lowest-Landau-level orbitals from their formula, and the Ising snapshots from
the same rule the header of `s10f05` records. Where the old figure file carries a numerical
provenance note, the script reproduces that computation.

## The order of the work

First the pilot, which is `s03f03_ssh`, since it has a lattice, a ladder of levels, two states of
one chain and a label at every site, so it exercises all of the pipeline. Copy `figlib.py`, write
`build_figure.sh` and `check_sizes.sh` for the paths above, write the script, the overlay and the
wrapper, render `still`, then `final`, build the PDF, compile `main.tex` with `latexmk -pdf` in
`src/`, and look at the page. Measure the height, check that the labels print at the size of the
text, and only then start the others. The pilot is the first checkpoint, to be shown and committed
once it is approved, as the sibling did with its pilot.

Then one session at a time, in order from 1 to 10, with one checkpoint per session, which is shown
before it is committed, and whose commit message says which figures of the session it adds and what
physics check corrected what. Within a session, write
all the scripts first and run the stills, fix the layouts, then run the finals as one background
batch, build the PDFs, and only then rewrite the captions, since the caption describes the drawing
that exists. The caption follows `writing_style.md`, with no colon, no semicolon and no dash in the
prose, and it says what the reader looks at, "the height of the column", "the ghost arrow", "the
glowing plaquette", in the register of the notes. Every physics statement, every equation number and
every cross reference of the old caption is kept.

At every checkpoint, `check_sizes.sh`, then `latexmk -pdf main.tex` in `src/`, then a grep for `??`
in `main.log`, then `cp src/main.pdf main.pdf`, and a look at every new figure on its page. At the
end, compare the page count of `main.pdf` before and after. It should not grow, since the figures
become shorter, and if it does, the sizes are the first thing to look at.

The old TikZ figure files are the only record of the drawings they contain, so before a wrapper is
rewritten its old body is kept in git history and nowhere else. Do not keep a copy in the tree.

## Figures that are better replaced than redrawn

Redrawing a figure in three dimensions does not make it a better figure, so before the catalogue we
ask, for each of the sixty-one, whether the drawing is the one the paragraph needs. The test is the
one the notes use for the figures already. A figure earns its place when it shows a mechanism that a
sentence cannot carry and when a reader who skips the text still sees the point. A schematic passes
this test as well as a computed curve does, since the self-consistency loop, the three channels of
one Hamiltonian, the Majorana pairings or the tensor diagrams are mechanisms drawn rather than
computed, and most of the figures of the notes are schematics of this kind and stay so. What does
not pass is a schematic that restates a list or a table, a row of boxes naming four uses, a counting
of signs that is already an equation, or a drawing repeated from an earlier session, and a render
makes those heavier rather than clearer. When the notebook of the session computes the thing in
question, the figure that shows that thing is the better one, since the reader will see it again on
the screen. Most figures pass, and the following ones do not, or pass with a change. Each item says what is weak, what to
draw instead, and what it costs in the text. These are decisions for the lecturer, and the catalogue
below carries the replacement for each of them, since all six were accepted by the lecturer on
2026-10-14.

- `s02f03_blochrecipe`. The figure is a recipe for reading a matrix off a lattice, which is a table
  with arrows, and the one physics statement in it, that the intracell hopping goes off the
  diagonal, is one sentence of the text. What the section is about is the two-band chain, and the
  notebook computes exactly the thing that makes it visible, "One dimensional chain, band folding".
  Replace it by the band folding figure. Left, the chain with the one-site cell and with the two-site
  cell as two translucent slabs. Middle, the single cosine band of the one-site cell folded into the
  half zone of the two-site cell, where the two branches touch at the zone edge for $\eta=1$. Right,
  the same two branches for $\eta\neq1$ with the gap open. The recipe stays in the text as the
  sentence about the off-diagonal entry, the label `fig:s02:recipe` stays, and the sentence of the
  text that points at the figure says that it shows the folding and the gap.
- `s03f05_masses`. The figure draws the Chern-number counting of equation (3.8) as sign tiles, and
  the counting is already the equation. What a reader cannot get from the equation is what the two
  masses look like on the lattice and what each does to a ribbon, which is what the notebook
  computes in "The quantum anomalous Hall effect" and "Edge states of the quantum anomalous Hall
  state". Replace the tiles by two columns. Left, the honeycomb patch with the staggered potential
  as raised and lowered sites, and under it the ribbon spectrum with a gap and nothing in it. Right,
  the honeycomb patch with the second-neighbor hoppings as arrows circulating around a hexagon, and
  under it the ribbon spectrum with the chiral branch crossing the gap. The two spectra are computed
  in the script. The caption keeps the counting in words, one sentence per column, and the label
  stays.
- `s04f04_ladders`. Two static ladders at one field show the pattern, but the point of the section is
  how each ladder moves with $B$, linear against square root, and that is what the notebook images in
  "Magnetic field dependence of Landau levels" and its Dirac counterpart. Replace the ladders by the
  two fans $E_n(B)$, straight lines through the origin on the left and square-root curves with a
  flat $n=0$ line in the accent color on the right, with the ladder at one field drawn as a vertical
  cut through each fan, so that the old figure is contained in the new one. The caption keeps every
  statement and adds the one about the fan.
- `s08f02_frustration`. Panels (a) and (b), the satisfied square plaquette and the triangle with one
  unsatisfied bond, repeat panels (a) and (b) of `s06f03_frustration` two sessions earlier with
  collinear arrows. What is new in session 8 is the counting of the degenerate Ising states and the
  kagome lattice. Drop (a) and (b), keep the three inequivalent placements of the unsatisfied bond
  and the kagome patch as the two panels, and let the caption and the prose point back to figure
  6.3 for the first two. The letters change, so the prose of session 8 that names the panels is
  edited with it. Width 0.8 instead of full.
- `s10f01_networktemplate`. The bottom row, the four later uses of the template as four small input
  and output tiles, is a table, and the text already lists the four uses. Drop the row and keep the
  network and its training loop, which is the one mechanism of the session. The caption loses its
  last sentence and the label stays.
- `s10f04_dftml`. The top row, the Hohenberg-Kohn reduction as a wide slab becoming a narrow one
  with a missing return arrow, is a statement rather than a mechanism, and it is one sentence of the
  text. Keep only the Kohn-Sham loop with the two routes, which is where the two ways of using
  machine learning differ. The caption's "Top" paragraph becomes the first sentence of the text
  before the figure, and the label stays.

Two more are weak but stay. `s04f02_gauge`, the Peierls phases in two gauges, is a bookkeeping
figure, but the Peierls substitution is what the notebook of the session runs on the lattice, so it
stays at a narrow width. `s05f02_fsgap`, `s05f03_gapsymmetry` and `s05f04_topology` draw the pairing
function on the same pocket three times in three sections, which is right for the three questions
they answer, and the cost is only that the pocket, its ring and its dials have the same style and
the same size in all three so that the reader sees one object.

## The catalogue

One entry per figure. The label and the placement are the ones in the file today, verbatim. "One
render" means one scene with its panels side by side or front to back, and "n renders" means the
multi-panel call. The width is the width of the PDF on the page, "full" being 15.6 cm, and the
aspect is the camera `aspect` of the render or of the whole composed figure. The notes carry
forward the constraints recorded in the header comments of the old files, and the entry says which
panels the prose refers to by letter.

### Session 1

- `s01f01_fockspace`, `fig:s01:fockspace`. Placement: sec. "Where the two formalisms diverge",
  after the three-site paragraph. Left, a three-site chain with its 3 by 3 hopping matrix as a grid
  of nine tiles, the nonzero entries raised. Right, the eight Fock states of three sites as eight
  short slabs of three sites with a filled ball on every occupied site, grouped by particle number
  in rows of 1, 3, 3, 1, as in the sibling's `exponential_wall`. One render, full width, aspect 2.6.
  Overlay labels: "$L\times L$", "$2^L$ states", $N=0,1,2,3$.
- `s01f02_ssb`, `fig:s01:ssb`. Placement: sec. "Spontaneous symmetry breaking", after the Ising
  paragraph. The double well $E(m)$ as a tube over an $m$ axis, twice side by side, a shallow
  barrier for a small system and a high barrier for a large one, with a ball resting at $+m_0$ and a
  ghost ball at $-m_0$. One render, width 0.7, aspect 2.0. Labels: $m$, $E$, $\pm m_0$, "small $L$",
  "large $L$".
- `s01f03_threechannels`, `fig:s01:channels`. Placement: sec. "The general interacting
  Hamiltonian", alongside the enumerated list. One four-site chain on the left with a glow for the
  interaction, and three chains on the right in the three ordered states, charge columns of
  alternating height, alternating spin arrows, and pairs of electrons joined by a capsule. The
  broken symmetry of each is an overlay label. One render, full width, aspect 2.8. Keep the
  header's note: no quasiparticle row.
- `s01f04_cdw`, `fig:s01:cdw`. Placement: sec. "Worked example 1", at the "numerically, this
  shows up..." paragraph. Front row, the chain at $V=0$ with every cup half full and its level
  ladder to the right with no gap. Back row, the alternating cups 1, 0, 1, 0 and the ladder with a
  gap, the doubled unit cell as a translucent slab. One render, full width, aspect 2.6. The
  caption's "at the top" and "at the bottom" become "in front" and "behind". Keep the note: no band
  folding panel.
- `s01f05_selfconsistency`, `fig:s01:mfloop`. Placement: sec. "Worked example 1", at the "more
  rigorously, mean-field theory is a variational search..." paragraph. The four steps as four
  stations on a ring, each a four-site chain in that step, guessed arrows, the mean-field
  Hamiltonian as raised and lowered sites, the level ladder filled up to $N$, and the new arrows, as
  in the sibling's `scf_loop` panel (a). The flow arrows and "converged?" are drawn in the overlay
  between anchors so that they stay crisp. One render, full width, aspect 2.4. Keep the note: no
  side column of the three channels.

### Session 2

- `s02f01_ringmodes`, `fig:s02:ring`. Placement: sec. "Worked exercises", at the three-site ring /
  eq. (2.4). Left, three copies of the three-site ring with an in-plane arrow on each site turning
  by $2\pi n/3$ from site to site, for $n=0,1,2$. Right, the allowed phases as balls on a unit ring
  for $L=3$, $L=5$ and a full ring for $L\to\infty$. One render, full width, aspect 2.8. Labels:
  $n$, $e^{2\pi i n/3}$, $L=3$, $L=5$, $L\to\infty$, "first Brillouin zone".
- `s02f02_cosband`, `fig:s02:cosband`. Placement: sec. "Bloch's theorem and the first band
  structure", after eq. (2.8). The band $-2t\cos\varphi$ as a tube with its minimum at $\varphi=0$,
  ghost tubes for the parabola at the bottom, the inverted parabola at the top and the straight
  line at midband, and the density of states as a profile slab to the right, diverging at both
  edges. One render, full width, aspect 2.8. Keep the sign convention of the header, $t>0$ and
  the minimum at $\varphi=0$.
- `s02f03_blochrecipe`, `fig:s02:recipe`. Replaced by the band folding figure, the file name and
  the label stay. Placement: sec. "Multi-orbital band structures", between eqs. (2.12) and (2.13).
  Left, the chain with the one-site cell and the two-site cell as two translucent slabs, the
  intracell and intercell bonds as two rod styles. Middle, the cosine band of the one-site cell as a
  ghost tube over the full zone and its folding into the half zone as two tubes that touch at the
  zone edge, for $\eta=1$. Right, the two bands $\pm|1+\eta e^{-i\varphi}|$ for $\eta\neq1$ with the
  gap open at the zone edge. The bands are computed in the script. One render, full width, aspect
  2.8. The caption says that the folding is the recipe in a picture, keeps the sentence that the
  intracell hopping enters off the diagonal, and the pointing sentence at line 335 of
  `session02.tex` says that the figure shows the folding and the gap. The notebook box "One
  dimensional chain, band folding" is the one this figure now serves.
- `s02f04_dirac`, `fig:s02:dirac`. Placement: sec. "The Dirac cone", between eqs. (2.19) and
  (2.20). (a) A honeycomb patch with the three vectors $\boldsymbol\delta_j$ as arrows from one $A$
  site. (b) The three phasors placed one after the other, closing a triangle at $K$ and not closing
  at a generic $\mathbf k$. (c) The hexagonal zone as a tile with two cones standing at $K$ and
  $K'$. One render, full width, aspect 2.8. Keep (a) in real space and (b) in the complex plane,
  as the header asks.
- `s02f05_flatbands`, `fig:s02:flatbands`. Placement: sec. "The Dirac cone ... and flat-band
  lattices", at the flat-band passage. One row of five: (a) the Lieb lattice, (b) its three bands
  as tubes along a k-path, (c) the kagome lattice, (d) its bands, (e) one kagome hexagon with
  amplitudes of alternating sign as up and down balls and two cancelling paths to an outside site.
  The bands are diagonalized in the script. One render, full width, aspect 3.0, height about
  5.2 cm.
- `s02f06_archetypes`, `fig:s02:archetypes`. Placement: sec. "Three archetypes of dispersion",
  alongside the enumerated list. Three two-dimensional dispersions as surfaces, a paraboloid, a
  Dirac cone and a flat plane, each with its density of states as a profile slab beside it, a
  step, a linear vanishing and a spike. One render, full width, aspect 3.0. Keep the note: every
  panel is two-dimensional.

### Session 3

- `s03f01_chiraledge`, `fig:s03:chiraledge`. Placement: sec. "The quantum Hall state", after the
  chirality/backscattering paragraph. (a) A flat rectangular sample with closed cyclotron orbits
  as rings in the bulk and skipping orbits along the edges with direction arrows, opposite on the
  two edges. (b) One edge with an impurity as a bump and the mode going around it. One render,
  full width, aspect 2.6. Keep the sign convention of the header, electrons with $B$ out of the
  page orbit counter-clockwise in the bulk.
- `s03f02_bulkboundary`, `fig:s03:bulkboundary`. Placement: sec. "What topology means for a
  Hamiltonian", after the interpolating-Hamiltonian paragraph. A slab along $x$ whose color goes
  from $H_1$ to $H_2$, and above it at three depths the Chern number as a step tube from 1 to 0,
  the local gap as a tube that dips to zero at the interface, and the bound state as a glow at
  the interface. One render, width 0.75, aspect 2.0. The caption's "top", "middle" and "bottom"
  panels become the three rows from back to front.
- `s03f03_ssh`, `fig:s03:ssh`. The pilot. Placement: sec. "The SSH model", after the
  dangling-site paragraph. Front row, the chain with strong intracell bonds, the cells as
  translucent slabs, and its ladder to the right with the gap. Back row, the shifted chain with the
  two end sites uncoupled and its ladder with two levels at zero in the broken color, and a glow on
  the two end sites. Eight sites in both rows. One render, full width, aspect 2.6. Panels (a) and
  (b) stay as front and back.
- `s03f04_winding`, `fig:s03:winding`. Placement: sec. "The SSH model", after equation (3.6). Top
  row, $d(k)$ as a ring standing on a floor tile with the origin as a post, centered at $(t,0)$,
  for $t<1$ enclosing the post and for $t>1$ not. Bottom row, $E_\pm(k)$ as tubes with the gap
  $2|1-t|$. One render, full width, aspect 2.6, the rings and the bands drawn as four small panels
  side by side so that the height stays below 6 cm.
- `s03f05_masses`, `fig:s03:masses`. Replaced, the file name and the label stay. Placement: sec.
  "Gapping the Dirac cone", after equation (3.8). Two columns. (a) The honeycomb patch with the
  staggered potential as $A$ sites raised and $B$ sites lowered, and below it the ribbon spectrum
  of that model as tubes, a gap with nothing in it. (b) The honeycomb patch with the
  second-neighbor hoppings as arrows circulating around one hexagon, and below it the ribbon
  spectrum with the chiral branch crossing the gap in the accent color. Both spectra are computed in
  the script from the tight-binding ribbon. Two renders, the lattices in one and the two spectra in
  the other, full width, aspect 2.8 overall. The caption keeps the counting of (3.8) in words, one
  sentence per column, and says which column is boron nitride and which is the Chern insulator.
  This figure now serves the notebook boxes "The quantum anomalous Hall effect" and "Edge states
  of the quantum anomalous Hall state".
- `s03f06_helical`, `fig:s03:helical`. Placement: sec. "Quantum spin Hall insulators", after the
  Kramers paragraph. Three schematic edge dispersions, the bulk bands as two slabs and the edge
  branches as tubes crossing the gap, one branch, two counter-propagating branches in the two spin
  colors, and the same two branches with a gap at the crossing. One render, full width, aspect
  3.0. Keep the note: schematic, not computed.

### Session 4

- `s04f01_ribbon`, `fig:s04:ribbon`. Placement: sec. "Why an insulating bulk still conducts:
  edge states", after the ribbon / no-backscattering paragraph. (a) The ribbon spectrum as flat
  tubes over $k_y$ that bend up at both ends, with the chemical potential as a translucent slab
  crossing them, for $N=2$. (b) The strip in real space with the edge modes as arrows in opposite
  directions and an impurity bump. One render, full width, aspect 2.6.
- `s04f02_gauge`, `fig:s04:gauge`. Placement: sec. "Choosing a gauge: Landau versus symmetric",
  after the two bullets. Two square-lattice patches of three by three plaquettes with the Peierls
  phase of every bond as a small dial, (a) only the vertical bonds, growing with $x$, (b) every
  bond, and one plaquette highlighted in both with the same sum. The phases are the ones in the
  header. One render, width 0.8, aspect 2.2.
- `s04f03_guidingcenter`, `fig:s04:guidingcenter`. Placement: sec. "Landau levels of
  Schroedinger electrons", after equation (4.6). (a) Parabolic wells as tubes displaced along
  $x$ for several $k_y$, each with the same ladder of rods and a Gaussian bump for the ground
  state. (b) The flat bands over $k_y$ as tubes. One render, full width, aspect 2.6.
- `s04f04_ladders`, `fig:s04:ladders`. Replaced by the Landau fans, the file name and the label
  stay. Placement: sec. "Landau levels of Dirac electrons", after equation (4.7). (a) $E_n(B)$ for
  Schr\"odinger electrons as straight tubes through the origin, $n=0$ to $5$. (b) $E_n(B)$ for
  Dirac electrons as square-root tubes, $n=0,\pm1,\pm2,\pm3$, with the flat $n=0$ line in the
  accent color. In both a translucent slab at one field $B_0$ cuts the fan, and the rods where it
  cuts the tubes are the ladder of the old figure. One render, full width, aspect 2.6. The caption
  keeps every statement of the old one and adds that the ladder at a fixed field is the vertical cut
  through the fan, which is what the notebook images in "Magnetic field dependence of Landau
  levels" and "Magnetic field dependence of Dirac Landau levels".
- `s04f05_droplet`, `fig:s04:droplet`. Placement: sec. "Angular momentum, enclosed flux, and the
  uniform electron gas". (a) The orbitals $|\psi_m|^2$ as nested rings, surfaces of revolution
  each normalized to the same height. (b) The $\nu=1$ droplet and the wider $\nu=1/3$ droplet as
  two flat-top surfaces of revolution. One render, full width, aspect 2.6. Keep the note that (a)
  is computed and (b) is a schematic profile.
- `s04f06_quasihole`, `fig:s04:quasihole`. Placement: sec. "Berry phase, fractional charge, and
  anyonic statistics", after equation (4.16). (a) The droplet surface with a dimple at $w$. (b)
  Two dimples, one carried once around the other on a tube path, with the Aharonov-Bohm and the
  statistical parts of the phase as overlay labels. One render, full width, aspect 2.6. Keep the
  phase note of the header, a full loop is two exchanges and the exchange phase is $\pi/m$.

### Session 5

- `s05f01_flux`, `fig:s05:flux`. Placement: sec. "Superconductivity as a macroscopic quantum
  phenomenon", after eq. (5.1). Left, a superconducting ring as a torus with the contour deep
  inside as a dashed tube and the flux through the hole as vertical arrows. Right, the phase
  $\theta$ winding once around as a helix, or a dial that turns by $2\pi n$. One render, width 0.7,
  aspect 2.0.
- `s05f02_fsgap`, `fig:s05:fsgap`. Placement: sec. "Three scenarios for one Fermi surface",
  after the enumerated list. Three columns. In each, the zone as a tile with the small pocket
  around $\Gamma$ as a ring, and the minimum of $E(\mathbf k)$ around the pocket as a tube
  standing on the ring, flat at zero, lifted by $\Delta_0$, and $|\cos2\phi|$ touching zero at the
  four nodes. This folds the two rows of the old figure into one. One render, full width, aspect
  2.8. Keep the header's form of $\Delta_d$ on a small pocket.
- `s05f03_gapsymmetry`, `fig:s05:gapsymmetry`. Placement: sec. "Nodal singlet order: d-wave,
  cuprates, and the angular-momentum expansion", after the extended-s-wave paragraph. Five zone
  tiles, the sign of $\Delta(\mathbf k)$ as raised and sunken regions with the nodal lines as
  grooves, $s$, extended $s$, $p$, $d$ on the square lattice and $f$ on the hexagonal one. Panels
  (a) to (e) keep their letters. One render, full width, aspect 3.2, which with the long caption
  keeps the block short.
- `s05f04_topology`, `fig:s05:topology`. Placement: sec. "Same gap, different topology", after
  the bulk-boundary paragraph. Two pockets as rings with a dial for the phase of $\Delta$ at
  several points of the ring, (a) all dials pointing the same way, (b) the dials turning with
  $\mathbf k$. One render, width 0.8, aspect 2.2. Keep the note that the dial is in the complex
  plane but placed at the momentum.
- `s05f05_kitaev`, `fig:s05:kitaev`. Placement: sec. "The Kitaev chain", after the
  SSH-recognition paragraph. $N=5$ sites with two Majorana balls on each, front row bound inside
  each site by a capsule, back row bound between sites with $\gamma_1$ and $\gamma_{10}$ left
  alone in the broken color. One render, full width, aspect 3.0, since the caption is long. Keep the numbering of the header,
  site $n$ carries $\gamma_{2n-1}$ and $\gamma_{2n}$.
- `s05f06_qsh`, `fig:s05:qsh`. Placement: sec. "Engineering a topological superconductor from a
  quantum spin Hall insulator", after the proximity-coupling paragraph. A quantum spin Hall slab
  with the two spins running in opposite directions along the free edge, two ferromagnet blocks on
  the edge, a superconductor block between them, and the two Majoranas at the two interfaces. One
  render, full width, aspect 2.8.

### Session 6

- `s06f01_stoner`, `fig:s06:stoner`. Placement: sec. "A criterion for magnetism: the Stoner
  threshold", right after eq. (6.3). (a) $f(m)$ as two tubes, one with slope below one and one
  above, against the line $y=m$, the crossings as balls. (b) $m_0$ against $UD(E_F)$ leaving zero
  at one. One render, full width, aspect 2.8.
- `s06f02_dimer`, `fig:s06:dimer`. Placement: sec. "From the Hubbard dimer to the Heisenberg
  model", after the 2x2 matrix and its eigenvalues. (a) Two sites, parallel spins with the hop
  blocked as a ghost arrow with a cross, antiparallel spins with the virtual doubly occupied
  state as a ghost and the hop back. (b) $E_S(U)$ and $E_T=0$ as tubes with the $-4t^2/U$ ghost.
  One render, full width, aspect 3.0, since the caption is long. The sibling's `superexchange` is
  the model for (a).
- `s06f03_frustration`, `fig:s06:frustration`. Placement: sec. "Bipartite order versus geometric
  frustration", after the triangular-plaquette paragraph. (a) A square plaquette with Néel arrows
  and the two sublattices as two disc colors and sizes. (b) A triangle with two antiparallel spins
  and two ghost arrows for the third. (c) The $120^\circ$ state with three in-plane arrows in one
  color. One render, full width, aspect 3.0. Panel (a) is referred to by `s06f04`. The sibling's
  `neel_vs_spiral` is the model.
- `s06f04_kitaev`, `fig:s06:kitaev`. Placement: sec. "Anisotropic exchange", in the Kitaev
  paragraph. A honeycomb patch with the three bond directions as three rod styles, and one site
  with three ghost arrows along $\hat x$, $\hat y$ and $\hat z$ that cannot all be satisfied. One
  render, width 0.7, aspect 1.8.
- `s06f05_magnon`, `fig:s06:magnon`. Placement: sec. "The Holstein-Primakoff transformation",
  after eq. (6.7). (a) The ferromagnet with every arrow up. (b) The magnon as tilted arrows on
  cones, the phase advancing by $45^\circ$ per site, seen from the side, and the same chain seen
  from above with the in-plane component turning. Two renders, one at a low elevation and one from
  the top, full width, aspect 2.6 overall.
- `s06f06_dispersion`, `fig:s06:dispersion`. Placement: sec. "Magnon dispersions: ferromagnets
  versus antiferromagnets", after eq. (6.9). $1-\cos ka$ and $|\sin ka|$ as two tubes in the same
  units, and the zone center magnified as a second small panel. Two renders, width 0.8, aspect 2.4
  overall.

### Session 7

- `s07f01_jwstring`, `fig:s07:jwstring`. Placement: sec. "Fermions and spins are the same
  physics", after equation (7.2). Two chains, front and back, with fermion balls on the occupied
  sites and the spin arrow of each site beside it, the string $K_6$ as a translucent ribbon over
  sites 1 to 5, holding three fermions in one chain and two in the other. One render, full width,
  aspect 2.8.
- `s07f02_arealaw`, `fig:s07:arealaw`. Placement: sec. "Two dimensions and the area law", after
  the dimer/tetramer comparison. (a) The dimerized chain with the block $A$ as a translucent box,
  twice, for two block sizes, with the cut dimers in the broken color. (b) The tetramer lattice
  with a square region $A$ and the cut tetramers in the broken color. The counts 2, 2, 8, 16 are
  overlay labels and match the highlighted ones. Two renders, full width, aspect 3.0 overall, since
  the caption is long.
- `s07f03_entropyceiling`, `fig:s07:ceiling`. Placement: sec. "Why MPS work in 1D, and where
  they stop working", after (7.10). $S$ against $L$ as two tubes, one saturating and one growing
  as a logarithm, with two horizontal slabs at $\log M_1$ and $\log M_2$. One render, width 0.65,
  aspect 1.7.
- `s07f04_tensordiagram`, `fig:s07:tensors`. Placement: sec. "Tensor diagrams: notation for
  networks and operators", after the MPO paragraph. (a) Tensors as rounded cubes with rods for
  legs, a scalar, a vector, a matrix and a contraction. (b) The one big coefficient tensor with $L$
  legs next to the MPS chain. (c) The MPO row applied to the MPS. One render, full width, aspect
  2.6. The sibling's `tensor_notation` and `mps_chain` are the models.
- `s07f05_dmrg`, `fig:s07:dmrg`. Placement: sec. "Finding the ground state: the variational
  principle and DMRG", after the "erasing that tensor from the diagram" paragraph. (a) The closed
  network as three layers, bra, MPO, ket. (b) The same with one tensor removed and its three open
  legs left. (c) The sweep as an arrow along the chain in the overlay. One render, full width,
  aspect 2.8. The sibling's `mps_algorithm` is the model.
- `s07f06_merapeps`, `fig:s07:merapeps`. Placement: sec. "Beyond MPS: MERA and PEPS", after the
  PEPS paragraph. Left, the MERA as layers of cubes for the disentanglers and triangular prisms
  for the isometries, with a cut crossing one bond in every layer. Right, the PEPS as a grid of
  cubes with a physical leg down from each. One render, full width, aspect 2.6.

### Session 8

- `s08f01_magnon_spinon`, `fig:s08:magnonspinon`. Placement: sec. "Two emergent excitations:
  magnons versus spinons", right after the "simple pictorial argument" paragraph. (a) A Néel chain
  with one arrow flipped in the broken color. (b) A chain of singlet capsules with one capsule
  broken into two unpaired sites drawn as open balls. One render, full width, aspect 2.8. Panel (b)
  is referred to by `s08f03`. Keep the note that an even chain gives two unpaired sites.
- `s08f02_frustration`, `fig:s08:frustration`. Reduced to two panels, the file name and the label
  stay. Placement: sec. "Frustration: the route to a quantum spin liquid", after the
  triangular-plaquette paragraph. (a) The three inequivalent placements of the unsatisfied bond on
  a triangle, the bond in the broken color, with collinear arrows. (b) A kagome patch of
  corner-sharing triangles with one Ising configuration on it. The square plaquette and the single
  frustrated triangle are not drawn again, and the caption and the prose point to figure
  `fig:s06:frustration` for them. The old (c) and (d) become (a) and (b), so the prose of
  `session08.tex` around line 145 that names panels is edited with it. One render, width 0.8,
  aspect 2.4.
- `s08f03_vbs_rvb`, `fig:s08:vbsrvb`. Placement: end of sec. "The QSL ground state: the
  resonating valence bond wavefunction". Four rows of a chain at four depths, (a1) the fixed
  covering of capsules on the strong bonds, (a2) two spinons separated with the empty strong
  bonds between them glowing as the confining string, (b1) a superposition of coverings as stacked
  translucent ghost chains, (b2) the two spinons free with the capsules re-paired behind them. One
  render, full width, aspect 2.4. The row labels keep (a1), (a2), (b1), (b2).
- `s08f04_parton`, `fig:s08:parton`. Placement: sec. "The parton construction", after the
  single-occupancy constraint (8.11). (a) The four states of one site as four discs, empty, up,
  down, doubly occupied, the two unphysical ones as ghosts with a cross. (b) A small lattice of
  spinons hopping on bonds whose radius is $|\chi_{ij}|$. One render, full width, aspect 2.8. The
  prose refers to (a) and (b) by letter.
- `s08f05_gauge_vison`, `fig:s08:gauge`. Placement: sec. "Emergent gauge symmetry and vison
  excitations", after the square-lattice example. (a) One plaquette with a dial on every link,
  before and after a phase rotation on one site, the flux unchanged. (b) A lattice with
  $\Phi=+1$ on every plaquette and one flipped plaquette glowing in the broken color. One render,
  full width, aspect 2.6.
- `s08f06_kondo_bands`, `fig:s08:kondobands`. Placement: sec. "Electronic structure of the Kondo
  lattice: the Kondo insulator", after the anti-crossing paragraph. Left, a dispersive band tube
  crossing a flat $f$ tube at the Fermi level, which is a translucent slab. Right, the two
  hybridized bands with the gap. From (8.21) per spin, in one dimension. One render, width 0.8,
  aspect 2.4.

### Session 9

- `s09f01_nesting`, `fig:s09:nesting`. Placement: sec. "The Fermi sea and the Lindhard
  function", at the "Instabilities and nesting" paragraph. (a) $-2t\cos k$ with the occupied part
  as a thick tube and $q^\star=2k_F$ as an arrow between the Fermi points. (b) $\chi_0(q)$ as a
  tube diverging at $2k_F$. (c) The diamond Fermi surface of the half-filled square lattice as a
  slab on the zone tile with the nesting vector. One render, full width, aspect 3.0. The prose
  refers to (a) and (b) by letter.
- `s09f02_plasmon`, `fig:s09:plasmon`. Placement: sec. "Interactions as a perturbation", after
  equation (9.7). The $(q,\omega)$ plane as a floor tile, the particle-hole continuum as a
  translucent slab between $\omega_-$ and $\omega_+$, and the plasmon as a tube starting at
  $\omega_p$ and entering the continuum. One render, width 0.65, aspect 1.6.
- `s09f03_ysr`, `fig:s09:ysr`. Placement: sec. "Impurities as diagnostics II", after equation
  (9.10). (a) The BCS density of states as a profile slab with its gap and coherence peaks, and
  the two in-gap peaks at $\pm E_b$ in the broken color, the non-magnetic case as a ghost that
  coincides with the clean one. (b) $E_b(\alpha)$ as a tube crossing zero at $\alpha=1$. One
  render, full width, aspect 2.8.
- `s09f04_vacancy`, `fig:s09:vacancy`. Placement: sec. "Impurities as diagnostics III", after the
  bulk-boundary paragraph. Top, a slab with a large hole and the edge mode running around it as a
  glowing tube, then a small hole, then a single missing site with a glow. Bottom, two ladders,
  trivial and topological, with and without the vacancy, the in-gap rod in the broken color. Two
  renders, full width, aspect 2.4 overall. The caption's "Top" and "Bottom" stay.
- `s09f05_decay`, `fig:s09:decay`. Placement: sec. "Impurities as diagnostics IV", after
  equation (9.11). Two chains, front and back, with an impurity at the end and induced moments as
  arrows of alternating sign, the envelope as a ghost tube, $1/n$ in front and $e^{-n/\xi}$
  behind. One render, full width, aspect 2.8.
- `s09f06_localization`, `fig:s09:localization`. Placement: sec. "Disorder and Anderson
  localization", after equation (9.12). Three chains of $N=89$ sites at three depths with
  $|\psi_i|^2$ as columns, the Bloch wave flat at $1/N$, the critical state of the quasiperiodic
  model, and the localized state of the random chain, computed in the script for the states
  nearest the band center as the header records. One render, full width, aspect 2.6.

### Session 10

- `s10f01_networktemplate`, `fig:s10:template`. Simplified, the file name and the label stay.
  Placement: sec. "Neural networks as function approximators", after equation (10.1). Left, the
  network as layers of balls joined by rods, with the input and the output as tiles. Right, the
  training loop as four stations, evaluate, loss, gradient, step, with the loop arrows in the
  overlay. The row of four later uses is dropped, since the text lists them. One render, full
  width, aspect 2.8. The caption's "Left" and "Right" stay and its "Bottom" sentence goes.
- `s10f02_nnqs`, `fig:s10:nnqs`. Placement: sec. "Neural network quantum states", at the
  paragraph describing the slides' nested picture. (a) A configuration as a row of up and down
  tiles entering the network and one coefficient coming out. (b) Sampled configurations as a
  stack of rows and the local energy averaged. (c) The families as nested translucent slabs. One
  render, full width, aspect 2.8.
- `s10f03_tnml`, `fig:s10:tnml`. Placement: sec. "The many-body wavefunction as a big-data
  problem", after the paragraph naming MPS / tree / MERA / PEPS. (a) The four geometries as four
  small tensor diagrams of cubes and rods. (b) A tree tensor network reading a row of pixel
  vectors and giving one label. One render, full width, aspect 2.6.
- `s10f04_dftml`, `fig:s10:dft`. Simplified, the file name and the label stay. Placement: sec.
  "Machine learning in density functional theory", at the itemized list. The Kohn-Sham loop as
  stations, density, effective potential, diagonalization, new density, with route 1 as a network
  inside the loop in place of the exchange-correlation part and route 2 as a network that goes
  from the input to the output around the loop. The Hohenberg-Kohn row is dropped and its content,
  the $3N\to3$ reduction and the missing return formula, becomes one sentence of the text before
  the figure. One render, full width, aspect 2.8. The caption's "Route 1" and "Route 2" stay and
  its "Top" and "Bottom" go.
- `s10f05_phaseclassification`, `fig:s10:phaseclass`. Placement: sec. "Phase classification",
  after the Ising-gauge-theory paragraph. (a, b) Two 6 by 6 Ising snapshots as tiles of two
  heights, ordered and disordered. (c, d) Two Ising gauge snapshots with the spins on the bonds as
  short rods of two heights and one plaquette highlighted with its product. The configurations
  are generated in the script with the rule of the header, not copied. One render, full width,
  aspect 3.2, since the caption is long.
- `s10f06_hamiltonianlearning`, `fig:s10:hamlearning`. Placement: sec. "Hamiltonian learning",
  after equation (10.12). Top, a Hamiltonian tile and a spectrum tile with the forward arrow and
  the missing inverse. (a) Many known Hamiltonian tiles feeding a network together with their
  $\lambda_n$. (b) The trained network applied to one measured spectrum. One render, full width,
  aspect 3.0, since the caption is long. The caption's "Top", "(a)" and "(b)" stay.

## What to report at the end

The session that executes this reports, per session of the notes, which figures went in, the
render time of the batch, the heights of the figures on the page, which captions changed and why,
and which physics check corrected a drawing or a caption, in the way the commit message of
`efdc3f9` in the sibling does. It also reports what it could not verify, for instance a figure whose
labels it could not check on the page, rather than leaving it out of the report.
