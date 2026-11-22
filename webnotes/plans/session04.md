# Plan of Session 4 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session04.md`.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 482 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0) | 0 |
| `01-where-the-quantum-hall-state-shows-up.md` | 4.1, 4.2 | 1048 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | opener 1, quiz-long 1 |
| `03-from-the-kubo-formula-to-the-chern-number-briefly.md` | 4.3, 4.4 | 1122 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-ref 1 |
| `05-edge-states-and-why-an-insulating-bulk-still-conducts.md` | 4.5 | 1163 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | long-paragraph 1, opener 1, quiz-long 1, quiz-ref 1 |
| `06-quantized-hall-plateaus-in-experiment.md` | 4.6, 4.7 | 1158 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1, quiz-long 1 |
| `08-the-landau-gauge-and-the-symmetric-gauge.md` | 4.8 | 734 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | opener 1, quiz-long 2 |
| `09-landau-levels-of-schrodinger-electrons.md` | 4.9 | 920 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, opener 1 |
| `10-landau-levels-of-dirac-electrons.md` | 4.10 | 1296 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `11-numerical-check-of-the-landau-levels-and-edge-states-on-the-lattice.md` | 4.11, 4.12 | 1226 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `13-the-symmetric-gauge-and-the-lowest-landau-level-wavefunctions.md` | 4.13, 4.14, 4.15 | 1334 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 2, opener 1, quiz-long 1 |
| `16-fractional-filling-and-the-laughlin-wavefunction.md` | 4.16, 4.17 | 1194 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `18-berry-phase-fractional-charge-and-anyonic-statistics.md` | 4.18 | 955 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `19-the-haldane-model-and-the-quantum-hall-effect-without-landau-levels.md` | 4.19 | 864 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | opener 1, quiz-long 1 |
| `20-real-materials-realizing-chern-and-fractional-chern-physics.md` | 4.20, 4.21 | 1361 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | opener 1, quiz-long 1 |

## What holds for every page

The numbers of this plan were computed in one scratch script, and each builder computes them again in the check
script of its page. A sign of a page comes from the conventions sheet of the session, and this plan states no such
sign, only the signs of the pyqula calls that were checked here. The sheet `conventions/session04.md` did not
exist when this plan was written. The sheet
of Session 3 says that (4.1) stays as printed, with the plus sign, and that a page does not derive an absolute
direction of the current from the sign of $C$.

Two pyqula facts were checked for this plan, and the builders use them.

- A bulk magnetic cell of the square lattice works with the supercell along $y$. With
  `geometry.square_lattice().get_supercell((1, 20))`, `tij=[-1.]` and `h.add_orbital_magnetic_field(1/20)` the
  lowest bands are flat at $-3.698$ and $-3.118$, against $-3.686$ and $-3.058$ of the continuum levels
  $-4t+\hbar\omega_c(n+\tfrac12)$, and `h.get_anomalous_hall_conductivity` gives $1$, $2$ and $3$ in the first
  three gaps. The supercell `(20, 1)` does not give flat bands.
- The flat Chern band of Section 4.20 is reproduced by `geometry.honeycomb_lattice()` with
  `tij=[1., 0.3*cos(0.4*pi), -0.2]` and `h.add_haldane(0.3295)`, which is the imaginary amplitude
  $0.3\sin(0.4\pi)$ times $2/\sqrt3$. The lower band has the width $0.212$ and the gap $2.965$, the ratio $14.0$
  of the numpy helper, and the Hall conductivity in the gap is $+1$. `add_haldane(-0.3295)` gives $-1$.

An old figure is not overwritten. A figure that this plan marks as replaced gets a new script and a new SVG with the
prefix of the group, such as `g1_landau_chern.py`, the image line of the page points to the new SVG and keeps its
id, and the old script and SVG stay as they are. A replaced figure gets a new caption, read against the new
picture, with the parameters and the axis names of its script. The pyqula ribbons are periodic along $x$, as the
fold of Section 3.6b says, while the pages write $k_y$ and the left and right edges, so the caption names the
direction of the ribbon of the script. A figure marked as left stays and is reported.

## Index page

File `index.md`, 482 words.

- Question of the page, and where we arrive: none. The index of Session 3 was not changed for the new shape, and
  this index already has the shape of the ten index pages (from before, what we will see, where it comes back).
- Main result for the key box: none, the index is the introduction of the session.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, the index has no quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `concept_map.svg` is a schematic and not a plot.

The index stays out of the builder groups.

## 4.1 Where the quantum Hall state shows up and 4.2 Measuring the Hall conductance

File `01-where-the-quantum-hall-state-shows-up.md`, 1048 words, numbered equations none. A page of motivation.

- Question of the page, and where we arrive: why does the same quantized Hall conductance appear in GaAs and in
  graphene, but up to very different temperatures? The value is fixed by topology, and the material sets only the
  spacing of the Landau levels, which grows as $B$ in GaAs and as $\sqrt B$ in graphene.
- Main result for the key box: none, since this is a page of motivation. The order of $x$ and $y$ in Section 4.2
  is open, see "Open for the lecturer", and the builder writes no new copy of $I_x=N(e^2/h)V_y$.
- Equation of another page that it starts from, for the recall box: (3.4), which the page calls "the common
  point".
- Derivation told in words, for a steps fold: none, the page derives nothing.
- Lab box, with the source and the number that the source states: `https://arxiv.org/abs/1504.06511`, graphene
  grown on SiC, probe the quantized Hall resistance. The stored text says "In
  graphene, the spacing between the lowest discrete energy levels occupied by the charge carriers under magnetic
  field is exceptionally large." and "the Hall resistance is accurately quantized within 1× 10^-9 over a 10-T wide
  range of magnetic field with a remarkable lower bound at 3.5 T, temperatures as high as 10 K, or measurement
  currents as high as 0.5 mA." The box quotes $10$ K and $3.5$ T.
- Pen-and-paper problem: compute the level spacing $\hbar\omega_c$ of GaAs with $m^*=0.067\,m_e$ and the first
  Dirac level $E_1=v\sqrt{2\hbar eB}$ of graphene with $v=10^6$ m/s, both at $10$ T, in meV and in kelvin. Answer
  $17.3$ meV or $201$ K, and $115$ meV or $1331$ K, so a ratio of $6.6$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the second quiz (21 words, "Why do
  the quantum Hall plateaus of graphene survive..."). Rewrite the first quiz with equations as options, such as
  $\hbar\omega_c\to4\hbar\omega_c$ and $E_1\to2E_1$, with the two laws written in the question. No picture quiz,
  since the page is motivation.
- Figures to add, each with its pyqula script or the reason for numpy: `g1_energy_scales.py`, $\hbar\omega_c$ of GaAs
  and $E_1$ of graphene against $B$ from $0$ to $10$ T in meV, with ticks at $1$, $4$, $10$ T and at $17$ and
  $115$ meV, numpy since it is two closed formulas with the constants of the two materials. It serves the
  problem and the second quiz.
- Old figures of the page that break the plot rules: `hall_setup.svg` is a schematic and is fine. The PDF figure
  `s04f04_ladders` shown again has named axes but no ticks and no units, see the last block of this list.

## 4.3 From the Kubo formula to the Chern number, briefly and 4.4 Landau levels as Chern-number-one flat bands

File `03-from-the-kubo-formula-to-the-chern-number-briefly.md`, 1122 words, numbered equations (4.1), (4.2).

- Question of the page, and where we arrive: a Landau level is flat and has no group velocity, so how can it carry
  a Hall current? Its Chern number is $1$, since the Chern number is built from the wavefunctions only, and $N$
  filled levels give $\sigma_{xy}=N e^2/h$.
- Main result for the key box: (4.2), with one sentence that the integer counts the filled Landau levels. (4.1)
  stays in the text as it is, since it is (3.4) printed again.
- Equation of another page that it starts from, for the recall box: none. (4.1) is (3.4) on this page already,
  and a recall of (3.4) would show the same equation twice. The opener links Section 3.5.
- Derivation told in words, for a steps fold: none for (4.1), whose steps are the fold of Section 3.5, which the
  page links. The paragraph of 161 words is split where it goes from the Kubo formula to the Berry curvature.
- Lab box, with the source and the number that the source states: none. This page is the recap of a derivation,
  and the measured plateaus are in the boxes of Sections 4.1 and 4.6.
- Pen-and-paper problem: a disc in a gapped state with $N$ filled levels, each with $eB/h$ states per unit area.
  The field grows slowly. Faraday's law gives an azimuthal electric field, the Hall current carries charge into the
  disc, and the levels stay filled. Show that the charge balance needs $|\sigma_{xy}|=e\,\partial n/\partial B=N
  e^2/h$. Answer $N e^2/h$, for $N=3$ the value $3$ in units of $e^2/h$. The builder writes magnitudes only.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the first quiz, whose feedback refers
  to Section 3.5 by its number. The second quiz already has equations as options. New picture quiz, three
  staircases of $\sigma_{xy}$ against $E_F$ for the flux $1/40$, $1/20$ and $1/10$, with the question which one has
  the strongest field. The step width in $E_F$ is $\hbar\omega_c\propto B$.
- Figures to add, each with its pyqula script or the reason for numpy: `landau_chern.svg` is replaced by
  `g1_landau_chern.py`, drawn from the pyqula script `g1_landau_levels_square.py` with the bulk magnetic cell of "What holds for every page", the bands and
  `h.get_anomalous_hall_conductivity`. The $C=1$ of each band is read from the steps of $\sigma_{xy}$. The three
  quiz staircases come from the same script with three fluxes.
- Old figures of the page that break the plot rules: `landau_chern.svg` has ticks, but the axis of panel (b) has
  no unit, which should be $\sigma_{xy}$ in units of $e^2/h$, and $k_y$ has no unit. It is numpy for a calculation
  that pyqula does. Replaced, as above. The PDF figure `s04f03_guidingcenter` is left.

## 4.5 Edge states and why an insulating bulk still conducts

File `05-edge-states-and-why-an-insulating-bulk-still-conducts.md`, 1163 words, numbered equations none.

- Question of the page, and where we arrive: the opening question exists in the first paragraph ("how can such a
  system carry a finite, quantized current?"), and it is moved into the first three sentences. We arrive at $N$
  chiral modes at each edge, one per filled level, that cannot backscatter.
- Main result for the key box: an unnumbered display, the number of chiral modes at an interface is
  $|C_1-C_2|$, which is $N$ at the edge of a sample with $N$ filled levels. One sentence on why the modes do not
  backscatter.
- Equation of another page that it starts from, for the recall box: (4.2).
- Derivation told in words, for a steps fold: none. The count of the current of the edge modes is the problem of
  Section 3.6b, which the page links, so it is not written twice.
- Lab box, with the source and the number that the source states: `https://arxiv.org/abs/1412.3758`, stored in
  Session 3, films of V-doped (Bi,Sb)$_2$Te$_3$ in the quantum anomalous Hall state at zero field, probe the
  longitudinal resistance. That this state is a Chern insulator with $C=1$ is our reading. The
  stored text says "the zero-field longitudinal resistance down to 0.00013+-0.00007h/e2 (~3.35+-1.76 ohm)". The box
  quotes $3.35$ $\Omega$ against $h/e^2=25.8$ k$\Omega$, as the sign that the edge carries the current with no
  dissipation. Box 3.10b cites the same article for another number, the Hall conductance $0.9998$, and gives no
  value of the longitudinal resistance. The box says that this is a Chern insulator and not a Landau level,
  with the same chiral edge by the argument of Section 3.7.
- Pen-and-paper problem: a gate sets $N=2$ filled levels on the left half of a sample and $N=5$ on the right half.
  How many chiral modes run along the line between the two halves? Answer $3$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the first quiz, whose feedback refers
  to Section 3.11b by its number, and the second quiz (18 words). New picture quiz, three spectra of the continuum
  ribbon with the chemical potential in the first, second and third gap, with the question which one has
  $\sigma_{xy}=2e^2/h$.
- Figures to add, each with its pyqula script or the reason for numpy: the three quiz spectra, one script each with
  the prefix `g2_` and a shared helper `_g2_qhribbon.py`, numpy since they are the continuum ribbon with hard walls of `ribbon_three.py`,
  which pyqula does not model.
- Old figures of the page that break the plot rules: `ribbon_three.svg` (in a quiz feedback) has no ticks. It needs
  ticks at $E/\hbar\omega_c=0.5$ to $3.5$ and at $\mu=3$, and at $k_y\ell_B=0$ and $12$ for the two walls. Replaced by
  `g2_ribbon_three.py`, on the helper of the quiz. The PDF figure `s04f01_ribbon` is left.

## 4.6 Quantized Hall plateaus in experiment and 4.7 Coupling electrons to a magnetic field with minimal coupling and the Peierls substitution

File `06-quantized-hall-plateaus-in-experiment.md`, 1158 words, numbered equations (4.3), (4.4).

- Question of the page, and where we arrive: what does a field sweep show at fixed density, and how do we put the
  field into a Hamiltonian to compute it? A staircase of plateaus at $h/(Ne^2)$, and the field enters through the
  canonical momentum (4.3) or, on a lattice, through the Peierls phases (4.4).
- Main result for the key box: two boxes. For Section 4.6 an unnumbered display, $R_{xy}=h/(Ne^2)$ on the plateau
  with $N$ filled levels. For Section 4.7 the box holds (4.4) as printed, with one sentence that it is the lattice form
  of (4.3). (4.3) stays in the text. The factor of (4.4) is open, see "Open for the lecturer", so no new text
  writes that factor.
- Equation of another page that it starts from, for the recall box: (4.2).
- Derivation told in words, for a steps fold: under (4.4), from the Peierls phases to minimal coupling at low
  energy. Simplest case first, a chain with the same bond phase $\theta$ on every bond, so
  $E=-2t\cos(ka-\theta)\simeq-2t+t(ka-\theta)^2$, the band shifted in $k$ by $\theta/a$, then the square lattice.
  The fold writes the phase as the symbol $\theta$ of a bond, or as the flux $\varphi$ per plaquette as Figure 4.2
  does, so that no factor of $\hbar$ appears before the lecturer picks.
- Lab box, with the source and the number that the source states: `https://arxiv.org/abs/1504.06511`, the same
  article as the box of Section 4.1 with another number, probe the quantized Hall resistance of graphene against
  that of GaAs/AlGaAs.
  The stored text says "We also measured an agreement of the quantized Hall resistance in graphene and
  GaAs/AlGaAs with an ultimate relative uncertainty of 8.2× 10^-11." The box quotes $8.2\times10^{-11}$, so the
  plateau has the same value in two materials. The number has no unit, so the lint may give the warning
  `lab-number`, which is accepted here, since a relative uncertainty is the number of this measurement.
- Pen-and-paper problem: a 2DEG has the density $n=3\times10^{11}$ cm$^{-2}$. Show that the classical Hall
  resistance $B/(ne)$ is $h/(\nu e^2)$ with $\nu=nh/(eB)$, and find the field where $N=2$ levels are just filled.
  Answer $B=6.20$ T, where $B/(ne)=h/2e^2=12.9$ k$\Omega$. This is why every plateau crosses the classical line of
  the figure.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the first quiz (17 words). New quiz
  with equations as options, the phase of the vertical bond in column $x$ in the Landau gauge, written with the
  flux $\varphi$ per plaquette as Figure 4.2 does, $x\varphi$, $y\varphi$ or $0$. New picture quiz, three curves of $R_{xy}$
  against $B$, plateaus at $1/N$, a rising staircase at $N$ and a straight line, with the question which one is a
  2DEG at fixed density in the quantum regime.
- Figures to add, each with its pyqula script or the reason for numpy: the three quiz curves, numpy, since they
  are the closed formulas of `plateaus.py`, with the prefix `g2_`.
- Old figures of the page that break the plot rules: `plateaus.svg` has $B$ with no unit and no ticks, and
  $R_{xy}e^2/h$ with no tick numbers (the levels carry "N=1" labels only). It needs $B/B_1$, with $B_1$ the field of
  $\nu=1$, ticks at $1/4$, $1/3$, $1/2$ and $1$ on both axes. Replaced by `g2_plateaus.py`. `plaquette_gauge.svg` (in a quiz feedback) is a
  schematic and is fine.

## 4.8 The Landau gauge and the symmetric gauge

File `08-the-landau-gauge-and-the-symmetric-gauge.md`, 734 words, numbered equations none.

- Question of the page, and where we arrive: the same field has many vector potentials, so which one do we take?
  The Landau gauge keeps the translation along $y$, which a band structure needs, and the symmetric gauge keeps the
  rotation, which the many-body states need. Only the sum of the phases around a loop is physical.
- Main result for the key box: an unnumbered display of the two gauges, $\mathbf A_L=(0,Bx,0)$ and
  $\mathbf A_S=\tfrac B2(-y,x,0)$, with one sentence that the sum of the Peierls phases around any plaquette is the
  flux through it in both.
- Equation of another page that it starts from, for the recall box: (4.4).
- Derivation told in words, for a steps fold: from the two vector potentials to the bond phases of Figure 4.2 and
  to the loop sum, on one plaquette with its lower left corner at $(x,y)$, by Stokes. The figure is drawn for
  $\varphi=\pi/4$.
- Lab box, with the source and the number that the source states: none. A gauge is not measured, and the page has
  no result that a probe reads.
- Pen-and-paper problem: find the function $\chi$ with $\mathbf A_S=\mathbf A_L+\nabla\chi$. Answer
  $\chi=-Bxy/2$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite both quizzes (17 and 20 words). New
  quiz with equations as options, which vector potential gives $B\hat z$, $(-By,0,0)$, $(By,0,0)$ or $(0,By,0)$.
  No picture quiz, since the picture of this page is Figure 4.2 and the quiz of Section 4.7 already shows a
  plaquette.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none. Figure 4.2 is a schematic of the bond phases.

## 4.9 Landau levels of Schrödinger electrons

File `09-landau-levels-of-schrodinger-electrons.md`, 920 words, numbered equations (4.5), (4.6).

- Question of the page, and where we arrive: what is the spectrum of a free electron in a uniform field? Each
  $k_y$ gives the same harmonic oscillator at another place, so the levels (4.6) are flat and each holds one state
  per flux quantum.
- Main result for the key box: (4.6), with one sentence that the energy does not depend on $k_y$ and that the
  level holds $BA/(h/e)$ states.
- Equation of another page that it starts from, for the recall box: (4.3).
- Derivation told in words, for a steps fold: from (4.5) to (4.6), the square completed in $x$, the guiding center
  $x_0=\hbar k_y/B$ and $\omega_c=B/m$.
- Lab box, with the source and the number that the source states: none. No fetched source states the level
  spacing of GaAs, and the GaAs scale is the problem of Section 4.1, with our own numbers.
- Pen-and-paper problem: a sample of size $L_x\times L_y$, periodic along $y$. Count the values of $k_y$ whose
  guiding center lies inside the sample. Answer $BL_xL_y/(h/e)$, which is $242$ for $1\,\mu$m$^2$ at $1$ T.
- Quizzes to rewrite, and a picture question or equations as options: no lint hit. New quiz with equations as
  options, the number of states of one level per unit area, $eB/h$, $h/eB$ or $eB/2\pi m$.
- Figures to add, each with its pyqula script or the reason for numpy: `g3_landau_fan.py`, drawn from the pyqula script
  `g3_landau_fan_square.py`
  with the bulk magnetic cell of "What holds for every page" for the fluxes $1/q$, $q=10$ to $60$, the lowest
  levels against the flux, with the lines $-4t+4\pi\phi t(n+\tfrac12)$. This is the "imaging" cell of the
  notebook, and its try-it box stays.
- Old figures of the page that break the plot rules: the PDF figure `s04f03_guidingcenter` has named axes and no
  ticks.

## 4.10 Landau levels of Dirac electrons

File `10-landau-levels-of-dirac-electrons.md`, 1296 words, numbered equations (4.7).

- Question of the page, and where we arrive: what changes when the electrons have a Dirac cone? The square of $H$
  is an oscillator, so the levels are $\pm\sqrt{|n|}$ times $E_1$, they grow as $\sqrt B$, and a level stays at
  zero energy.
- Main result for the key box: (4.7), with one sentence on the zero mode and on the scaling with $\sqrt{|n|B}$.
- Equation of another page that it starts from, for the recall box: (4.6).
- Derivation told in words, for a steps fold: from $H$ to $H^2$ and to (4.7), with $[a,a^\dagger]=1$ from
  $[\pi_x,\pi_y]=i\hbar^2/\ell_B^2$ and the zero mode with $a\psi=0$ in the upper component. The paragraph of 170
  words after (4.7) is split where it goes from the zero mode to the scaling.
- Lab box, with the source and the number that the source states: `https://arxiv.org/abs/cond-mat/0703822`,
  graphene, probe the infrared transmission between Landau levels. The stored text says "Infrared transmission is
  measured in magnetic fields up to B=18 T at selected LL fillings." and "Their transition energies are
  proportional to √B and the deduced band velocity is c≈1.1×10^6 m/s." The box quotes $18$ T and
  $1.1\times10^6$ m/s. If it gives $E_1$ at $18$ T, the value $169$ meV is ours (`ours="169 meV"`).
- Pen-and-paper problem: each level of graphene holds two spins and two valleys, and at zero density the level
  $n=0$ is half filled. Show that the plateaus are $\sigma_{xy}=\pm4(n+\tfrac12)e^2/h$. Answer $\pm2$, $\pm6$ and
  $\pm10$ in units of $e^2/h$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the second quiz (16 words, the ratio
  $E_4/E_1$), with (4.7) written in the question. New picture quiz, three ladders at one field, equally spaced,
  $\pm\sqrt n$ with a zero level and $\pm\sqrt n$ without one, with the question which one is graphene.
- Figures to add, each with its pyqula script or the reason for numpy: `g3_dirac_fan.py`, drawn from the pyqula script
  `g3_landau_fan_honeycomb.py` with the levels of the honeycomb lattice against the flux and the curves $\pm\sqrt{|n|}E_1$. The builder first
  tries a bulk magnetic cell of the honeycomb lattice, and else takes the peaks of the bulk density of states of
  the armchair ribbon of the notebook. The unit of the field of pyqula on the honeycomb lattice is checked with a
  number, by $E_1$ against (4.7), before a caption states it. The three ladders of the quiz are numpy, since they
  are closed formulas.
- Old figures of the page that break the plot rules: `dirac_levels.svg` has the axis $E$ with no unit and no ticks,
  while panel (a) is in units of $\hbar\omega_c$ and panel (b) in units of $E_1$. It needs $E/\hbar\omega_c$ with
  ticks at $0.5$ to $4.5$ and $E/E_1$ with ticks at $0$, $\pm1$ and $\pm2$. Replaced by `g3_dirac_levels.py`. The
  PDF figure `s04f04_ladders` is left.

## 4.11 Numerical check of the Landau levels and edge states on the lattice and 4.12 Ladder operators and the many-body Landau Hamiltonian

File `11-numerical-check-of-the-landau-levels-and-edge-states-on-the-lattice.md`, 1226 words, numbered equations (4.8).

- Question of the page, and where we arrive: do a square lattice and a honeycomb lattice in a field give the two
  ladders of the continuum, and is the oscillator only a property of the Landau gauge? The lattice gives both
  ladders with their edge branches, and the ladder operators built from $\boldsymbol\pi$ give (4.8) in any gauge.
- Main result for the key box: (4.8), with one sentence that it uses only $[\pi_x,\pi_y]$.
- Equation of another page that it starts from, for the recall box: (4.4), (4.6) and (4.7), in one box at the start
  of Section 4.11.
- Derivation told in words, for a steps fold: from $H=(\pi_x^2+\pi_y^2)/2m$ to (4.8), with $[a,a^\dagger]=1$. The
  fold of the lattice level spacing $4\pi\alpha t$ is in Section 3.6b and is not written again. The first paragraph
  of 222 words is split at the honeycomb ribbon.
- Lab box, with the source and the number that the source states: none. The measurement of the Dirac levels is the
  box of Section 4.10, and this page is the numerical check.
- Pen-and-paper problem: show that $[\pi_x,\pi_y]=i\hbar B$ in the Landau gauge and in the symmetric gauge. Answer
  $i\hbar B$ in both, which is $i\hbar^2/\ell_B^2$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the first quiz (21 words). New
  picture quiz, three ribbon spectra from the pyqula script below (square, honeycomb, honeycomb with no field),
  with the question which ribbon has Dirac electrons in a field. The level at zero energy decides.
- Figures to add, each with its pyqula script or the reason for numpy: `lattice_ribbons.svg` is replaced by
  `g3_lattice_ribbons.py`, drawn from the pyqula script `g3_ribbons_in_field.py`, with `geometry.square_ribbon` and `geometry.honeycomb_armchair_ribbon`,
  `h.add_orbital_magnetic_field` and `operator="yposition"`, as in the recipe "A ribbon in a magnetic field". Its
  square panel differs from the figure of Section 3.6b by showing the two lattices side by side. The quiz spectra
  come from the same script.
- Old figures of the page that break the plot rules: `lattice_ribbons.svg` has no ticks on $k_y$ and is numpy for a
  calculation that pyqula does. Replaced, as above. `wall_squeeze.svg` (in a quiz feedback) has no ticks at all, and its $x$ axis is a
  text under the middle panel. It needs ticks at $E/\hbar\omega_c=0.5$ and $1.5$ and an $x/\ell_B$ axis with the
  wall at $0$. Replaced by `g3_wall_squeeze.py`. The PDF figure `s04f01_ribbon` (panel a) is left.

## 4.13 The symmetric gauge and the lowest-Landau-level wavefunctions and 4.14 The many-body wavefunction of the filled lowest Landau level and 4.15 Angular momentum, enclosed flux, and the uniform electron gas

File `13-the-symmetric-gauge-and-the-lowest-landau-level-wavefunctions.md`, 1334 words, numbered equations (4.9), (4.10), (4.11).

- Question of the page, and where we arrive: what do the states of the lowest Landau level look like, and what is
  the state where all of them are filled? They are a holomorphic function times a Gaussian, the orbital $z^m$ sits
  on a ring of radius $\sqrt{2m}\,\ell_B$, and the filled level is one Slater determinant with a flat density.
- Main result for the key box: two boxes. The first holds (4.9), the second (4.11). (4.10) stays in the text.
- Equation of another page that it starts from, for the recall box: (4.8).
- Derivation told in words, for a steps fold: from the ladder operator in the symmetric gauge to (4.9),
  $\pi_x+i\pi_y=-2i\hbar(\partial_{\bar z}+z/4\ell_B^2)$, which holds for the charge $+e$ of the page. The two
  paragraphs of 183 and 174 words are split, the first at the Vandermonde identity.
- Lab box, with the source and the number that the source states: none. No fetched source measures a wavefunction
  of the lowest level, and the measured filling $1/3$ is the box of Section 4.17.
- Pen-and-paper problem: sum the densities $|\psi_m|^2$ of all the orbitals, normalized, and show that the filled
  level has the density $1/(2\pi\ell_B^2)$, which is one electron per flux quantum. Answer $1/(2\pi\ell_B^2)$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the droplet radius quiz (17 words).
  New quiz with equations as options, which function is a state of the lowest level in this gauge,
  $z^2e^{-|z|^2/4\ell_B^2}$, $\bar z^2e^{-|z|^2/4\ell_B^2}$ or $|z|^2e^{-|z|^2/4\ell_B^2}$. The convention of the
  charge decides the answer, so the question says "with the convention of this page".
- Figures to add, each with its pyqula script or the reason for numpy: none. The page has `droplet_density.svg`
  and Figure 4.5, and pyqula has no continuum lowest level.
- Old figures of the page that break the plot rules: `lll_radius.svg` (in a quiz feedback) has no ticks on its $y$
  axis, which needs $0$ and $1$. Replaced by `g4_lll_radius.py`. `droplet_density.svg` is fine. The PDF figure
  `s04f05_droplet` is left.

## 4.16 Fractional filling and the Laughlin wavefunction and 4.17 Quasiholes and quasielectrons

File `16-fractional-filling-and-the-laughlin-wavefunction.md`, 1194 words, numbered equations (4.12), (4.13), (4.14).

- Question of the page, and where we arrive: how do we fill only a third of a Landau level and keep the electron
  gas uniform? The Laughlin state (4.12) at $\nu=1/m$, and a quasihole that removes a charge $e/m$.
- Main result for the key box: two boxes. The first holds (4.12), with one sentence that its filling is (4.13). The
  second holds (4.14). (4.13) stays in the text. The opening argument about lumps is open, see "Open for the
  lecturer", and the builder leaves it.
- Equation of another page that it starts from, for the recall box: (4.11).
- Derivation told in words, for a steps fold: from the highest power $m(N-1)$ to (4.13), for $N=2$ first, where
  $(z_1-z_2)^m$ uses the orbitals $0$ to $m$, then any $N$ and the limit of large $N$.
- Lab box, with the source and the number that the source states: `https://arxiv.org/abs/cond-mat/9706307`, a 2D
  electron system at filling $1/3$, probe the shot noise of tunneling. The stored text says "we measure the shot
  noise associated with tunneling in the fractional quantum Hall regime at Landau level filling factor 1/3" and
  "The noise gives a direct determination of the quasiparticle charge, which is found to be e*=e/3 as predicted by
  Laughlin." The box quotes $e^*=e/3$. It has no unit, so the warning `lab-number` is accepted. The box goes in
  Section 4.17.
- Pen-and-paper problem: for $N=3$ electrons and $m=3$, find the highest power of $z_1$ in (4.12), the number of
  orbitals that the state uses and its filling. Answer the power $6$, $7$ orbitals and the filling $3/7$, which goes
  to $1/3$ for large $N$. The most likely distance of two electrons is not used, since the caption of
  `laughlin_pair.svg` already gives it.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quasihole quiz (16 words). New
  quiz with equations as options, which state has $\nu=1/5$, $\prod(z_i-z_j)^5$, $\prod(z_i-z_j)^{1/5}$ or
  $\prod(z_i-z_j)^4$, each times the Gaussian. New picture quiz, three density profiles (the filled level, the
  Laughlin state, the Laughlin state with a quasihole at the center), with the question which one has a quasihole.
- Figures to add, each with its pyqula script or the reason for numpy: `g4_quasihole_dimple.py`, the density of the
  Laughlin state at $m=3$ and $N=20$ with and without a quasihole at the origin, by the Metropolis method of
  `droplet_density.py` moved to a helper `_g4_laughlin_mc.py`. The deficit integrates to $1/3$, given as a range over
  several seeds. numpy, since pyqula has no continuum many-body state. The picture quiz uses the same helper.
- Old figures of the page that break the plot rules: `laughlin_pair.svg` has no ticks on either axis. It needs the
  maxima $2.45$, $3.74$ and $4.69$ on $|z_1-z_2|/\ell_B$ and a $y$ axis in units of $1/\ell_B$. Replaced by `g4_laughlin_pair.py`. The PDF
  figure `s04f05_droplet` shown again is left.

## 4.18 Berry phase, fractional charge, and anyonic statistics

File `18-berry-phase-fractional-charge-and-anyonic-statistics.md`, 955 words, numbered equations (4.15), (4.16).

- Question of the page, and where we arrive: how can a Berry phase measure a charge and a statistics? Moving a
  quasihole around a loop gives the Aharonov-Bohm phase of a charge $e/m$, and moving it around a second quasihole
  adds $2\pi/m$, which is neither a boson nor a fermion.
- Main result for the key box: two boxes, (4.15) and (4.16), the second with one sentence that the exchange phase
  is $\pi/m$.
- Equation of another page that it starts from, for the recall box: (4.14) and (4.12).
- Derivation told in words, for a steps fold: from the Berry phase of a quasihole that goes once around a loop to
  (4.15), the phase is $2\pi$ times the mean number of electrons inside the loop, which is $\nu$ times the flux in
  flux quanta. The overall sign depends on the sense of the loop and on the charge, and the fold says so. The
  paragraph of 168 words is split at "These quasiparticles are what are called anyons".
- Lab box, with the source and the number that the source states: `https://arxiv.org/abs/2006.14115`, an
  electronic Fabry-Perot interferometer at $\nu=1/3$, probe the Aharonov-Bohm interference of the edge mode. The stored text
  says "Strong Aharonov-Bohm interference of the ν=1/3 edge mode is punctuated by discrete phase slips consistent
  with an anyonic phase of θ anyon=2π/3." The box quotes $2\pi/3$, which is (4.16) for $m=3$. It has no unit, so the
  warning `lab-number` is accepted.
- Pen-and-paper problem: a second quasihole inside the loop removes a charge $e/m$ from the region that the loop
  encloses. With the result of the fold, show that the phase changes by $2\pi/m$. Answer $2\pi/3$ for $m=3$, up to
  the sign of the fold.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the first quiz (20 words), which
  already has phases as options. No new quiz, since the page has two and the picture is Figure 4.6.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: the PDF figure `s04f06_quasihole` is a schematic and has no
  axis to fix.

## 4.19 The Haldane model and the quantum Hall effect without Landau levels

File `19-the-haldane-model-and-the-quantum-hall-effect-without-landau-levels.md`, 864 words, numbered equations
none. This page was cut on 2026-11-07 to a recap that links Sections 3.10 and 3.10b, and it stays short.

- Question of the page, and where we arrive: does a quantized Hall conductance need a magnetic field? It does not,
  since the Haldane model at zero field and the Landau levels are the same phase.
- Main result for the key box: none, the page is a recap.
- Equation of another page that it starts from, for the recall box: none, the page stays short.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none. The measurements at zero field are on
  Sections 3.5 and 3.10b and in the box of Section 4.20.
- Pen-and-paper problem: none, the page is a recap.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the first quiz (20 words). Nothing
  new.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none. The panel of `s03f05_masses` is a figure of the PDF of Session 3, which no builder changes.

## 4.20 Real materials realizing Chern and fractional Chern physics and 4.21 Closing summary

File `20-real-materials-realizing-chern-and-fractional-chern-physics.md`, 1361 words, numbered equations none.

- Question of the page, and where we arrive: where do we find a flat band with a Chern number at zero field, and
  does it give the fractional states of a Landau level? In magnetic topological insulators, in twisted graphene on
  hBN and in twisted MoTe$_2$, where fractional plateaus are measured at zero field.
- Main result for the key box: none for Section 4.20, a survey of materials. The closing summary has no key box.
- Equation of another page that it starts from, for the recall box: (4.1).
- Derivation told in words, for a steps fold: none, the page derives nothing.
- Lab box, with the source and the number that the source states: `https://arxiv.org/abs/2308.02657`, twisted
  bilayer MoTe$_2$, probe the Hall resistance at zero field. The stored text says "At zero magnetic field, near
  filling factor ν= -1 (one hole per moiré unit cell) we see an extended integer QAH plateau in the Hall resistance
  Rxy that is quantized to h/e^2 ± 0.1 % while the longitudinal resistance Rxx vanishes." and "at ν=-2/3 and -3/5 we
  see plateau features in Rxy at 3h/2e^2 ± 1% and 5h/3e^2 ± 3%, respectively". The box quotes $3h/2e^2$ within
  $1\%$. If it gives $38.7$ k$\Omega$, that value is ours.
- Pen-and-paper problem: none, the page is a survey and the closing summary.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the closing quiz (16 words). New
  picture quiz in Section 4.20, three honeycomb band structures, a dispersive band with $C=1$, a flat band with
  $C=1$ and a flat band with $C=0$, with the question which band can host a fractional Chern state. The builder
  finds the flat band with $C=0$ with pyqula and asserts its $C$.
- Figures to add, each with its pyqula script or the reason for numpy: `flat_chern_band.svg` is replaced by
  `g5_flat_chern_band.py`, drawn from the pyqula script `g5_haldane_t3_bands.py`, with the calls of "What holds for every page", and panel (a) with
  `add_haldane` of the page. The caption says which parameter of pyqula it quotes, as in the conventions sheet of
  Session 3. The quiz pictures come from the same script.
- Old figures of the page that break the plot rules: `flat_chern_band.svg` has its axes, but it is numpy for a
  calculation that pyqula does. Replaced, as above. The PDF figure `s04f06_quasihole` shown again is a schematic.

The closing summary 4.21 ends with the list of what the student can now do, each with its section, as Section 3.13
does.

- Count the filled Landau levels and give the Hall conductance and the plateau resistance (Sections 4.4 and 4.6).
- Count the chiral modes at an edge or at an interface between two fillings (Section 4.5).
- Write the Peierls phases of a uniform field in the two gauges and check the flux through a plaquette (Sections
  4.7 and 4.8).
- Derive the Landau levels of parabolic electrons and their degeneracy of one state per flux quantum (Section 4.9).
- Derive the Dirac levels with their zero mode, and compare the energy scales of GaAs and graphene at one field
  (Sections 4.10 and 4.1).
- Build a ribbon in a field with pyqula and tell the edge branches from the bulk levels (Section 4.11).
- Write the states of the lowest level in the symmetric gauge and the state of the filled level (Sections 4.13 and
  4.14).
- Write the Laughlin state at $\nu=1/m$, find its filling by counting, and give the charge and the exchange phase of
  its quasiholes (Sections 4.16 to 4.18).
- Say why a Chern insulator at zero field and the quantum Hall state are the same phase (Section 4.19).

## Old figures of the PDF, left as they are

The six Blender figures of the session, `s04f01_ribbon` to `s04f06_quasihole`, have named axes where they have
axes, and no ticks and no units. They are figures of the PDF notes, so no builder changes them, as in Session 3.

## The lab sources of the session

All were stored on 2026-11-21 with `labsource.py`. Every planned number was found with a search in the stored text.

- `https://arxiv.org/abs/1504.06511`, graphene Hall resistance standard, for Sections 4.1 and 4.6.
- `https://arxiv.org/abs/cond-mat/0703822`, infrared Landau levels of graphene, for Section 4.10.
- `https://arxiv.org/abs/cond-mat/9706307`, the charge $e/3$ from shot noise, for Section 4.17.
- `https://arxiv.org/abs/2006.14115`, the braiding phase $2\pi/3$, for Section 4.18.
- `https://arxiv.org/abs/2308.02657`, fractional plateaus in twisted MoTe$_2$, for Section 4.20.
- `https://arxiv.org/abs/1412.3758`, stored in Session 3, for Section 4.5.
- `https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.48.1559`, the plateau at $\nu=1/3$, stored with no
  abstract. Crossref has none, and the public abstract of the journal page was not read, so no box uses it. Its
  entry stays in `sources/index.json`.
- `https://www.science.org/doi/10.1126/science.1137201`, the "In the lab" cell of `session4.ipynb`, stored in
  Session 3. Its abstract says "room temperature" and has no number, so no box of this session uses it.

The arXiv text of two sources lost its TeX in the store. Jiang 2007 read "proportional to B" for $\sqrt B$, and
Nakamura 2020 read "2π3" for $2\pi/3$. The raw arXiv record has `$\sqrt{B}$` and `\frac{2π}{3}`, so the two
abstracts were attached again as plain text with `--paste`, with the arXiv API as the origin. The stored texts now
say "proportional to √B" and "θ anyon=2π/3". The conversion of `labsource.py` drops `\sqrt` and `\frac`, which is
a fault of the toolkit to fix.

## Builder groups

Five groups, in the order of the pages. The index gets no edit and is in no group. Every new file of a group has
the prefix of the group.

- g1, `01-where-the-quantum-hall-state-shows-up.md` and `03-from-the-kubo-formula-to-the-chern-number-briefly.md`.
  The energy scales of the two materials and the count of the filled levels. What is special is the new numpy
  figure `g1_energy_scales.py`, the pyqula bulk magnetic cell of "What holds for every page" for
  `g1_landau_levels_square.py`, and no new copy of $I_x=N(e^2/h)V_y$ until the lecturer picks the order of $x$
  and $y$.
- g2, `05-edge-states-and-why-an-insulating-bulk-still-conducts.md`,
  `06-quantized-hall-plateaus-in-experiment.md` and `08-the-landau-gauge-and-the-symmetric-gauge.md`. The edge
  count, the plateaus, the Peierls phases and the gauges, which share (4.2), (4.4) and the plaquette. What is
  special is that the factor of (4.4) is open, so the fold of Section 4.7 and the new quiz write the bond phase as
  $\theta$ or as the flux $\varphi$ per plaquette, and no new text writes a factor of $\hbar$. The box of Section
  4.5 cites the Session 3 article `1412.3758` for a number that box 3.10b does not give.
- g3, `09-landau-levels-of-schrodinger-electrons.md`, `10-landau-levels-of-dirac-electrons.md` and
  `11-numerical-check-of-the-landau-levels-and-edge-states-on-the-lattice.md`. The two ladders and the two lattice
  ribbons, which share the levels of `dirac_levels.svg`, the fans and the ribbons in a field. What is special is
  three pyqula scripts (`g3_landau_fan_square.py`, `g3_landau_fan_honeycomb.py`, `g3_ribbons_in_field.py`) and
  the unit of the field on the honeycomb lattice, checked by $E_1$ before a caption states it. The fold of
  $4\pi\alpha t$ is in Section 3.6b and is not repeated.
- g4, `13-the-symmetric-gauge-and-the-lowest-landau-level-wavefunctions.md`,
  `16-fractional-filling-and-the-laughlin-wavefunction.md` and
  `18-berry-phase-fractional-charge-and-anyonic-statistics.md`. The lowest level, the Laughlin state and its
  quasiholes, which share `droplet_density.py` and the new helper `_g4_laughlin_mc.py`. What is special is that
  the Monte Carlo numbers are given as a range over several seeds, that the sentences of Section 4.16 on lumps and
  on the exact ground state stay until the lecturer picks, and that the convention of the charge $+e$ decides the
  holomorphic quiz.
- g5, `19-the-haldane-model-and-the-quantum-hall-effect-without-landau-levels.md` and
  `20-real-materials-realizing-chern-and-fractional-chern-physics.md`. The Haldane model and the materials at zero
  field. What is special is that page 4.19 gets only its opener and the fix of the long quiz, that the closing
  summary gets the list of what the student can now do, and that `g5_haldane_t3_bands.py` uses the pyqula calls
  checked above.

## Open for the lecturer

The builders, the physics checkers and the fixers left the points of the old text that they found, as their brief says.
The lecturer decided on 2026-11-22 how to handle them ("Fix old-text errors, ask the rest"). The old list of this
section, the reports of the groups and the open points of `webnotes/conventions/session04.md` were merged into 31
distinct points. Sixteen are errors of the old text, which are now corrected on the web, and fifteen are for the
lecturer. A correction changes no numbered equation, no convention and no render of the PDF, and every number that it
adds is an assert in the check script of its page, in the block marked "corrected on 2026-11-22". An independent check
of the corrections on the same day made five of them more precise, entries 1, 2, 4, 10 and 12, and gave four more
points for the lecturer, 16 to 19. Two of these are on files that this pass does not edit, the toolkit and the
conventions sheet.

The nineteen points for the lecturer were decided on 2026-11-22. The lecturer picked point 3 and said for the others
"ask me the top 5, other you decide by yourself". The coordinator decided the other eighteen by a rule. It takes the
option that makes the text true with the smallest change and changes no numbered equation, and between two true
wordings the shorter and clearer one. A claim that no stored source or calculation supports is reduced to what is
supported, a notebook box that does not match its cell is rewritten to match it, and an outdated line of the
conventions sheet is corrected with its check. The notebooks, the Blender figures, the toolkit and a sign of Session 3
are not edited. The list "Decided on 2026-11-22" below gives each choice, entries 17 to 27 of the next list carry the
changes that the `.tex` shares, and "Not applied" gives what the rule leaves out. Every number that these changes add is
an assert in the block marked "decided on 2026-11-22" of the check script of its page, and in
`webnotes/checks/session04/conventions.py` for the sheet. The only numbered equation that changed is (4.2), which keeps its tag.

A second independent check on the same day read the applied decisions and gave eight findings. All eight were applied,
after a calculation of our own for each. The caption of `hall_setup` now says where the current of the charge $+e$ goes,
point 2. The factor $1/\hbar$ of (4.4) is now also in the sentence before it and in the first quiz of Section 4.7, point
1. The graphene bullet says what the stored abstract says, point 6. The magnitude of $C$ is written on page 05 too,
point 3, and the charge $e/m$ of a quasihole is written as a magnitude on pages 16, 18 and 20, point 4. The width 30 is
back on page 11, since the Core cells of the notebook have it, point 9. The range of the lumps is taken over 210 seeds,
point 7, and the bullet of the conventions sheet on the square ribbons of the notebook names the cells and their widths.

### Corrected on the web, to carry over to the .tex

The line numbers are those of `lecture_notes/src/sessions/session04.tex` on 2026-11-22.

1. Page 01, Section 4.1, the GaAs bullet, .tex lines 29 to 31. Old "For the fields that we can reach in a laboratory
   this gives roughly one millielectronvolt, and this is the reason why quantum Hall physics in GaAs needs temperatures
   of the order of one kelvin." New "This gives $1.7$ meV per tesla, so a few millielectronvolts at a few tesla and
   $17$ meV at $10$ T. This is the reason why quantum Hall physics in GaAs needs temperatures of the order of one
   kelvin." The pointer of Section 4.9 to "the millielectronvolt scale that we gave in Section 4.1" agrees with the new
   sentence and is not changed. The sentence on the kelvin was changed on the same day by the decision on point 18, entry 21 below. `g1_01` asserts
   1.73 meV per tesla by the SI constants and by $2\mu_B/0.067$, 3.5 to 8.6 meV for 2 to 5 T and 17 meV at 10 T. The
   assert of the old number, 1 meV at 0.58 T, is removed.
2. Page 10, Section 4.10, .tex lines 310 to 312. Old "while for Dirac electrons the levels are spaced as $\sqrt{n}$ and
   grow as $\sqrt{B}$, and this is the reason why, at the same field, the Landau levels of graphene are roughly two
   orders of magnitude higher in energy than the ones of a GaAs 2DEG." New "For Dirac electrons the levels are spaced
   as $\sqrt{n}$ and grow as $\sqrt{B}$. With $v_F=10^6$ m/s for graphene and $m^*=0.067\,m_e$ for GaAs, at the same
   field the Landau levels of graphene are roughly one order of magnitude higher in energy than the ones of a GaAs 2DEG.
   The first level $E_1$ of graphene is $21$ times the spacing $\hbar\omega_c$ of GaAs at $1$ T and $6.6$ times at
   $10$ T, and this ratio falls as $1/\sqrt{B}$." The old "this is the reason why" made the $\sqrt{B}$ law the cause of
   the factor, while the factor $m^*v_F\sqrt{2/\hbar eB}$ is set by $v_F$ and $m^*$, and the $\sqrt{B}$ law only makes it
   fall, to 1 at 440 T. The paragraph is now split before "Figure 4.4 shows", for its length. The caption of Figure 4.4 has the same error in its
   text, `lecture_notes/src/figures/s04f04_ladders.tex` line 11, and only the text changed, not the render. Old "This is
   still enough to put the level spacing of graphene about two orders of magnitude above the one of a GaAs quantum well
   at the same field." New "This is still enough to put the level spacing of graphene about one order of magnitude
   above the one of a GaAs quantum well at the same field." The .tex of Section 4.1, line 35, also says "roughly two
   orders of magnitude larger", where the web already reads "roughly one order of magnitude larger, around 100
   millielectronvolts at 10 T". `g3_10` asserts the ratio 21 at 1 T and 6.6 at 10 T, by the SI constants and by the
   rates of the conventions sheet, within half a decade of 10, and that it is $m^*v_F\sqrt{2/\hbar eB}$, falls as
   $1/\sqrt{B}$ and is 1 at 440 T.
3. Page 05, Section 4.5, .tex lines 128 to 130. Old "So an impurity on the left edge cannot scatter a left-moving
   electron into a right-moving one, because the right edge is at a macroscopic distance." New "So an impurity on the
   left edge cannot scatter an electron into a state that moves the other way along $y$, because these states are on
   the right edge, at a macroscopic distance." The ribbon is finite along $x$, so its edge states move along $y$. The
   paragraph is now split before "Figure 4.1 shows", for its length. `g2_05` asserts that at $\mu=1$, 2 and 3 every
   branch of the left wall has $dE/dk_y<0$ and every branch of the right wall $dE/dk_y>0$.
4. Page 06, Section 4.6, .tex lines 151 and 152. Old "When the field increases further, the cyclotron energy
   $\hbar\omega_c$ grows, so fewer Landau levels stay below a fixed chemical potential." New "When the field increases
   further, the cyclotron energy $\hbar\omega_c$ grows and each Landau level holds more states, $eB/h$ per unit area, so
   at fixed density fewer Landau levels are filled." The paragraph ends with the result at fixed density of the figure,
   and the opener and the key box of the page are at fixed density too. The paragraph is now split before this sentence,
   for its length. `g2_06` asserts that at the density $3\times10^{11}$ cm$^{-2}$ of the problem the fully filled
   levels are 1 from 6.20 to 12.4 T and 2 from 4.14 to 6.20 T, which is the clean count, and that the plateaus of the
   figure cross the classical line at $B/B_1=1/N$ while its jumps, with the broadening of its model, are at
   $B/B_1=1/(N+\tfrac12)$. An earlier version of this entry said that the jumps of the figure are at $1/N$, and it is
   corrected.
5. Pages 06 and 11, Sections 4.7 and 4.12. The old text called $\boldsymbol\pi=\mathbf p-e\mathbf A$ the canonical
   momentum, while it is the kinetic momentum $m\mathbf v$ and $\mathbf p$ is the canonical one, as the recall box of
   Section 4.9 and the key box and the problem of Section 4.12 say. Page 06, .tex lines 160 and 161, old "enters the
   equations of motion through the canonical momentum," new "enters the equations of motion through the kinetic
   momentum, also called the mechanical momentum,". Page 11, .tex line 352, old "if we define the ladder operators
   directly from the canonical momentum," new "if we define the ladder operators directly from the kinetic momentum,".
   Page 11, a quiz feedback, not in the .tex, old "The ladder operators are built from the canonical momentum
   $\boldsymbol{\pi}$." new "The ladder operators are built from the kinetic momentum $\boldsymbol{\pi}$." The
   "canonical bosonic commutation relation" of .tex line 358 is another use of the word and stays. `g2_06` asserts with
   sympy that Hamilton's equations give $m\dot x=\pi_x$ and $m\dot y=\pi_y$, and that $[p_x,p_y]=0$ while
   $[\pi_x,\pi_y]=i\hbar B$.
6. Page 06, Section 4.7, .tex lines 188 and 189. Old "In concrete terms, the hopping amplitude $t_{ij}$ is by
   definition an overlap between the orbital wavefunctions at sites $i$ and $j$." New "In concrete terms, the hopping
   amplitude $t_{ij}$ is the matrix element of the Hamiltonian between the orbital wavefunctions at sites $i$ and $j$."
   `g2_06` asserts on a double well that the two orthonormal orbitals have the overlap 0, while $|\langle1|H|2\rangle|$
   is half the splitting of the two levels.
7. Page 09, Section 4.9, .tex lines 240 to 242. Old "For an electron, which has charge $-e$, every cyclotron orbit and
   every edge current below goes around in the other direction, and nothing else changes." New "For an electron, which
   has charge $-e$, every cyclotron orbit and every edge current below goes around in the other direction. The states of
   the lowest Landau level in the symmetric gauge of Section 4.13 are then functions of $\bar z$ and not of $z$. The zero
   mode of the Dirac levels of Section 4.10 also moves, from the upper component of the spinor to the lower one."
   The sign of the Chern number for the charge $-e$ is not written, since the sign of $C$ is the third point for the
   lecturer. `g3_09` asserts with sympy that $z^2$ and $\bar z^2$ times the Gaussian have $\tfrac12$ and $\tfrac52$ in
   units of $\hbar\omega_c$ for $+e$ and the reverse for $-e$, and in an oscillator basis that the Dirac zero mode is in
   the upper component for $+e$ and in the lower one for $-e$.
8. Page 11, the text of the widget `landaufan`, not in the .tex. Old "and the dashed lines are the Landau levels
   $(n+\tfrac12)\hbar\omega_c$ with $\hbar\omega_c=4\pi\phi t$ of Section 4.9." New "and the dashed lines are the Landau
   levels $-4t+(n+\tfrac12)\hbar\omega_c$ with $\hbar\omega_c=4\pi\phi t$ of Section 4.9, measured from the bottom of the
   band at $-4t$." The widget draws its dashed lines at `-4 + wc*(j + 0.5)`. Its legend label "(n+1/2) hbar omega_c" in
   `webnotes/widgets/defs/landaufan.py` and the old text in `webnotes/widgets/blocks/landaufan.md` are files of the
   toolkit and were not changed, and they are point 16 for the lecturer. `g3_11` asserts the dashed lines from the code of the widget and the lowest band
   within 5 percent of a spacing of the first line, by the widget and by a Harper matrix of its own.
9. Page 13, the caption of `droplet_density`, not in the .tex. Old "It is flat at $\nu=1$ up to the radius
   $\sqrt{2N}\,\ell_B$, where it drops to zero." New "It is flat at $\nu=1$ up to about $2\,\ell_B$ inside the radius
   $\sqrt{2N}\,\ell_B$, and around this radius it drops to zero." The old caption disagreed with the solution of the
   same page. `g4_13` asserts 0.998, 0.92, 0.47 and 0.003 at 2 and 1 $\ell_B$ inside, at and 2 $\ell_B$ outside the
   radius for 20 electrons, by the sum of the orbitals and by the incomplete gamma function.
10. Page 16, Section 4.16, .tex lines 474 to 476. Old "From them we arrive at the exact ground state of a strongly
    interacting many-body problem, which will give us fractional charge in the next section." New "From them we arrive
    at an exact ground state of a repulsion of very short range. Among the states of zero energy of this repulsion it is
    the densest one. For the Coulomb repulsion and $m=3$ we compare at the same total angular momentum,
    $3N(N-1)\hbar/2$. There the Laughlin state is very close to the ground state but not equal to it, with an overlap of
    $0.99$ for three electrons and $0.98$ for four on a disc. This state will give us fractional charge in the next
    section." The paragraph is now split before "So we start only", for its length. On a disc with no confinement the
    Coulomb energy keeps falling with the angular momentum, so the comparison holds only in the sector of the Laughlin
    state, and the short-range repulsion has states of zero energy at every larger angular momentum, so the Laughlin
    state is the densest of them and not the only one. `g4_16` diagonalizes 3 and 4 electrons in the lowest level at a
    fixed total angular momentum. With $V_1$ alone there is no negative energy and no state of zero energy below
    $3N(N-1)/2$, which is 9 and 18, one at it, the Laughlin state, and for three electrons 1, 1, 2 and 3 at 9 to 12.
    With the Coulomb pseudopotentials the overlap at 9 and 18 is 0.990997 and 0.978804, the first one also in the full
    product space of three particles.
11. Page 16, Section 4.17, .tex lines 504 and 505. Old "This moves charge inward instead of outward, and it gives an excitation
    with the opposite, negative, fractional charge." New "This moves charge inward instead of outward, and it gives an
    excitation with the opposite fractional charge, which has the sign of the charge of the electrons." The old word
    "negative" holds for the charge $-e$ and not for the charge $+e$ of these pages, and it disagreed with the key box of
    the same page. `g4_16` asserts for 4 electrons that the quasielectron holds more electrons than the Laughlin state in
    the discs of radius 1.5 to 2.5 $\ell_B$ and the quasihole fewer, with the angular momentum 14 and 22 against 18.
    The sign of (4.15) is the fourth point for the lecturer.
12. Pages 19 and 20, Sections 4.19 and 4.21. Page 19, .tex lines 581 and 582, old "At every step of this path the bulk
    gap stays open and the chiral edge state survives." new "For the parameters of the notebook, where the field and the
    Haldane coupling give the same Chern number, the bulk gap stays open at every step of this path and the chiral edge
    state survives." Page 20, the closing summary, .tex lines 638 to 640, which there read "adiabatically and
    topologically equivalent to the quantum Hall state driven by the field", old "It is adiabatically connected to the
    quantum Hall state driven by the field, so the two are the same topological phase" new "It is adiabatically
    connected to the quantum Hall state driven by the field with the same Chern number, so the two are the same
    topological phase". The try-it box of page 19, not in the .tex, now says what the cell does: "The cell follows the
    straight line $\nu H_\mathrm{QH}+(1-\nu)H_\mathrm{C}$ between the two, and only $H_\mathrm{QH}$ carries the Peierls
    phases, so the Hamiltonians in between are not those of a uniform field. This line keeps the gap open on the ribbon
    of the cell in the gauge of pyqula, but not in every gauge." `g5_19` asserts on the path of the text, with
    `add_haldane(0.07)` added before the field 0.01 and the onsite energy $-0.2$ all along, that no bulk state comes
    closer to zero energy than 0.135 at zero field, 0.404 at full field and 0.198 at the end, and that at every one of
    its 11 steps one edge branch crosses zero energy on each edge, rising on the upper edge and falling on the lower one.
    It asserts that on the straight line of the notebook the bulk gap stays above 0.198, that with `add_haldane(-0.07)`
    a bulk state comes to zero energy, and that after a pure gauge change of $H_\mathrm{QH}$, the ribbon moved by 40 in
    $y$, which shifts its spectrum by $-0.2$ in $k$, the straight line brings a bulk state below 0.01 at $\nu=0.5$,
    0.0003 on the mesh of 41 $k$. `g5_20` asserts that the field and `add_haldane(+0.07)` have $C=+1$ while
    `add_haldane(-0.07)` has $C=-1$.
13. Page 19, the notebook box, .tex lines 591 and 592. Old "The "topological domains" exercise lets you study spatial
    regions where the two couplings compete directly, which is a practical version of the equivalence argument that we
    just gave." New "The "topological domains" exercise puts the two halves of a ribbon in a field at onsite energies of
    opposite sign. The two halves then have Chern numbers of opposite sign, and the wall between them carries the chiral
    modes that the count of Section 4.5 gives." The cell has a field and the onsite energies $\pm3.5$ and no Haldane
    coupling. `g5_19` asserts $C=+2$ and $-2$ for the two halves, by `get_chern` and by the link variables, and 4
    branches across zero energy at the wall and 2 at each outer edge.
14. Page 10, a quiz feedback, not in the .tex, corrected earlier in the new shape. Old "$E_4=580\,\mathrm{meV}$" for
    $E_n\propto n^2$, new "$E_4=581\,\mathrm{meV}$", which is $16\times36.3$. `g3_10` asserts it.
15. Page 03, the caption of `landau_chern`, not in the .tex, corrected earlier when the figure was redrawn. Old "The
    small shift of the upper levels from the dashed lines comes from the lattice", new "The bands sit below the dashed
    lines, by $0.01\,t$ for the lowest and by $0.30\,t$, about half a spacing, for the fourth, which is the effect of the
    lattice".
16. Page 06, the caption of `plateaus`, not in the .tex, corrected earlier when the figure was redrawn. Old "Look at how
    every plateau crosses the classical line at its center", new "Look at the dots, where every plateau crosses the
    classical line at $B/B_1=1/N$". The old sentence held in $1/B$ and not on the axis $B$ of the figure.
17. Page 03, Section 4.4, .tex lines 94 to 101, decided by the lecturer on 2026-11-22, point 3. Old "which is also the
    smallest nonzero value, $C=1$." new "with the smallest nonzero magnitude, $|C_n|=1$. For the charge $+e$ of these
    pages in the field $B\hat z$, each level has $C_n=-1$ with the $\Omega$ of Session 3, and for an electron in the same
    field $C_n=+1$." Old "the sum of $N$ contributions equal to $1$," new "the sum of $N$ contributions of the same sign
    and of magnitude $1$,". Equation (4.2), old $C_{\text{tot}} = \sum_{n=0}^{N-1} C_n = N \Longrightarrow \sigma_{xy} =
    N\,e^2/h$, new $|C_{\text{tot}}| = \big|\sum_{n=0}^{N-1} C_n\big| = N \Longrightarrow |\sigma_{xy}| = N\,e^2/h$,
    with the same number. The heading of Section 4.4, .tex line 89, is not changed, see "Not applied". `g1_03` asserts
    $|C_n|=1$ and $|C_\text{tot}|=N$ for $N=1$ to 4 with both signs, and $C_n=-1$ for the charge $+e$ in $B\hat z$ and $+1$
    for an electron, by pyqula and by a numpy cell with the phase (4.4).
18. Page 20, the closing summary, .tex lines 618 to 620, point 3. Old "each with Chern number one, so the Hall
    conductivity is quantized to $N e^2/h$ for $N$ filled Landau levels" new "each with a Chern number of magnitude one,
    $|C_n|=1$. So the Hall conductivity is quantized to $|\sigma_{xy}|=Ne^2/h$ for $N$ filled Landau levels". The same
    choice changed the web text of the index, of Section 4.14, of the caption of `s04f03_guidingcenter` on page 03, of
    the second quiz of page 03 and of the first quiz of page 06, which the `.tex` does not have. `g5_20` and `g4_13`
    assert $|C_n|=1$ and $|C_\text{tot}|=N$.
19. Page 06, Section 4.7, .tex lines 190 to 195, point 1. Old "a complex phase, which is equal to the line integral of
    $\mathbf{A}$ between the two sites," new "a complex phase, which is equal to the line integral of $\mathbf{A}$ between
    the two sites, divided by $\hbar$." Under (4.4), after .tex line 195, new "This form is written with $\hbar=1$. In the
    units of this session, with $e=1$ and $\hbar$ kept, the phase is $(1/\hbar)\int\mathbf{A}\cdot d\boldsymbol{\ell}$."
    (4.4) stays as printed. The first quiz of Section 4.7, not in the `.tex`, now takes $\chi=\hbar\theta x/a$ in place of
    $\chi=\theta x/a$, writes $(1/\hbar)$ in front of the sum of the added phases of its second option, and says in its third
    option that the sum around a loop is "the flux through it divided by $\hbar$, which is $2\pi$ times the flux in flux
    quanta". `g2_06` asserts that the bond phase $Aa/\hbar$ puts the minimum of the chain at the $k=A/\hbar$ of minimal
    coupling, that $(e/\hbar)Ba^2$ is $2\pi\alpha$, that the new $\chi$ adds $\theta$ to every bond along $x$, that the
    gauge changes around a plaquette add to 0 and that the loop sum is the flux over $\hbar$, $2\pi$ times the flux in flux
    quanta $2\pi\hbar$. The sentence before (4.4) and the sentence under it were changed after the second independent
    check.
20. Page 01, Section 4.1, the graphene bullet, .tex lines 35 to 37, point 6. Old "This is high enough that the quantum
    Hall plateaus of graphene survive up to about 100 K, and in the best samples up to almost room temperature." new
    "This is high enough that the quantum Hall effect of graphene can be measured even at room temperature." No stored
    source gives the 100 K or the best samples, and the stored abstract of `science.1137201` says "the QHE can reliably be
    measured even at room temperature", which `g1_01` asserts, with 115 meV at 10 T as $4.4\,k_BT$ at 300 K for "high
    enough", the number of Session 3. A first wording of the same day, "survive in the best samples up to almost room
    temperature", was replaced after the second independent check. The rest of the bullet is kept by point 5.
21. Page 01, Section 4.1, the GaAs bullet, .tex lines 29 to 31, point 18. Old "This is the reason why quantum Hall
    physics in GaAs needs temperatures of the order of one kelvin." new "A plateau needs a thermal energy much smaller
    than this spacing, and disorder broadens the levels, so quantum Hall physics in GaAs needs temperatures of the order
    of one kelvin." This is the reason of the problem of the same page. `g1_01` asserts that 1.73 meV is 20 K and that
    $k_B$ times 1 K is 1/20 of the spacing at 1 T.
22. Page 16, Section 4.16, .tex lines 442 to 445, point 7. Old "for example two out of every three" new "for example
    one out of every three". Old "If we only leave some orbitals empty, we obtain" new "If we leave the orbitals empty in
    an irregular way, we obtain". `g4_16` asserts that every third orbital of 20 electrons gives 0.324 to 0.333 between
    $2\,\ell_B$ and $2\,\ell_B$ inside the edge, and that the 210 irregular choices of 20 of the orbitals 0 to 57 with the
    seeds 0 to 209 deviate there from $1/3$ by more than 20 percent. Their range is 24.0 to 185.2 percent, with 22 above
    100 percent, and it depends on the seeds, so only the lower bound is asserted. An earlier version of this entry gave
    27 to 100 percent from ten seeds, and over 1000 seeds the lowest deviation is 19.5 percent.
23. Page 11, Section 4.11, .tex lines 343 to 346, point 9. Nothing to carry over. The web sentence "The notebook box of
    Section 4.10 asks you to build both ribbons yourself, for example with a width of 30 sites." was first shortened, on
    the ground that the notebook has no width 30. The second independent check found `N = 30` in the Core cells
    "Landau levels of conventional electrons" with `square_ribbon` and "Landau levels of the Dirac equation" with
    `honeycomb_armchair_ribbon`, which the notebook box of Section 4.10 names. The sentence is now "The notebook box of
    Section 4.10 asks you to build both ribbons yourself, for example with the width `N = 30` of its Core cells." It
    gives the width parameter and not a number of sites, since the armchair ribbon of 30 has 60 rows of sites and the
    square one 30. The `.tex` phrase "shown for a width of 30 in the slides" agrees with the notebook and stays. `g3_11`
    reads `N = 30` from the two cells and counts the rows.
24. Page 19, the notebook box, .tex lines 589 and 590, point 19. Old "Build the Haldane model, switch a magnetic field on
    and off numerically together with the Haldane coupling, and follow the bulk gap and the Chern number along the
    adiabatic path described above." new "Build the Haldane model and a quantum Hall ribbon, follow the straight line
    between the two Hamiltonians, and watch the bulk gap and the edge branches of the ribbon." `g5_19` reads the code cell
    of the notebook and asserts that it builds the two Hamiltonians on one armchair ribbon, takes
    `H_hall*nu + H_chern*(1-nu)`, plots the bands with `operator="yposition"` and calls no `get_chern`.
25. Page 05, Section 4.5, .tex lines 114 to 118, point 3, after the second independent check. Old "a sample with Chern
    number $N$" new "a sample with a Chern number of magnitude $N$". Old "is equal to the difference in Chern number
    across it" new "is equal to the magnitude of the difference in Chern number across it". The second quiz of the page,
    not in the `.tex`, now asks for $|\sigma_{xy}|$, and its feedback says "The number of modes is $|C|$, and
    $|\sigma_{xy}|=|C|e^2/h$" and "equal to the magnitude of the Chern number of the bulk". `g2_05` asserts that $N=1$, 2
    and 3 filled levels of a Harper cell with the flux $1/12$ have $C_\text{tot}=-N$ for the charge $+e$ in $B\hat z$ and
    $+N$ for an electron, so $|C_\text{tot}|=N$, the number of modes at each wall.
26. Page 20, the closing summary, .tex line 634, point 4, after the second independent check. Old "have fractional charge
    $e/m$, equation (4.15)," new "have a fractional charge of magnitude $e/m$, equation (4.15),". The same change is in the
    web text of the opener of page 16, the caption of `g4_quasihole_dimple`, the first quiz of Section 4.17 ("What is the
    magnitude of the charge of one quasihole?", and "removes" in two feedbacks), the comesback box of page 16, the opener
    of page 18 and the caption of `s04f06_quasihole` on page 20, which the `.tex` does not have. `g4_16`, `g4_18` and
    `g5_20` assert the wording, and that for $m=1$ the quasihole leaves 1 electron fewer in the discs of 4 to 6
    $\ell_B$, so its charge is $-e/m$ for the charge $+e$.
27. Page 18, the caption of Figure 4.6, `lecture_notes/src/figures/s04f06_quasihole.tex` lines 10 and 11, point 4, after
    the second independent check. Old "so one quasihole has the charge of an electron divided by $m$, which is $q=e/m$."
    new "so one quasihole removes the charge of an electron divided by $m$, and its charge has the magnitude $q=e/m$."
    Only the text changes, not the render. `g4_18` asserts it with the count of entry 26.

### Decided on 2026-11-22

One bullet per point of the old list "For the lecturer", in its order, with the choice and who chose it.

1. The factor of the Peierls phase (4.4). The coordinator by the rule: keep (4.4) and add under it "In the units of this
   session the phase is $(1/\hbar)\int\mathbf{A}\cdot d\boldsymbol{\ell}$", since the other form changes a numbered
   equation. To keep the text true, the first quiz of Section 4.7 takes $\chi=\hbar\theta x/a$. The sheet gives the
   factor in its first line of units. After the second independent check the key box also says that (4.4) is written
   with $\hbar=1$, the sentence before (4.4) divides the line integral by $\hbar$, and the second and third options of the
   quiz write the factor. Entry 19.
2. The order of $x$ and $y$ in Section 4.2 and the sense of `hall_setup`. The coordinator by the rule: keep the order,
   which holds in magnitude, and add to the caption "The arrows are drawn for electrons, and for the charge $+e$ of these
   pages they go around the other way". `g1_01` asserts the sense with an island of 14 by 14 sites, $+0.196$ along $x$ in
   the upper half for the charge $+e$ and $-0.196$ for an electron, and reads the counterclockwise arrows from the
   coordinates of `hall_setup.py`. After the second independent check the caption reads "The arrows are drawn for
   electrons. For the charge $+e$ of these pages they go around the other way, and the channels of the top contact then
   end in the right contact, so the current is read there." `g1_01` counts the four contacts with Landauer-Buttiker, the
   top one at $V_y$ and the others at 0. For the drawn sense the left contact takes $N(e^2/h)V_y$ and the right one 0, and
   for the charge $+e$ the reverse, or the bottom contact takes it when the right one floats. Web text only.
3. The sign of the Chern number of a Landau level. The lecturer: $|C_n|=1$ in the text and $|\sigma_{xy}|=Ne^2/h$ in
   (4.2), with $|C_\text{tot}|=N$ on its left side and the tag 4.2, and one sentence of Section 4.4 that the charge $+e$
   in $B\hat z$ has $C_n=-1$ with the $\Omega$ of Session 3 and an electron $+1$. Applied in the text of Section 4.4, in
   (4.2), in the web caption of `s04f03_guidingcenter`, in the second quiz of page 03, in Section 4.14, in the closing
   bullet of Section 4.21, in the index and in the first quiz of page 06, which quotes (4.2). After the second
   independent check also in the second paragraph and in the second quiz of page 05. The heading of Section 4.4 is not
   changed, see "Not applied". Entries 17, 18 and 25.
4. The sign of (4.15). The coordinator by the rule: keep (4.15) as printed, since the other two forms change it, and the
   lead sentence of the key box now reads "has a charge of magnitude", so that the box is true for the charge $+e$. The
   key box of Section 4.17 gives the sign. `g4_18` asserts that the quasihole leaves 1 electron fewer for $m=1$ and 0.32
   to 0.34 for $m=3$. After the second independent check every other place that gives a quasihole the charge $e/m$
   writes it as a magnitude too, on pages 16, 18 and 20. Entries 26 and 27.
5. The graphene bullet of Section 4.1. The coordinator by the rule: keep it as it is, since it holds. `g1_01` asserts the
   ratio 10 at 4.4 T and 115 meV at 10 T.
6. "Survive up to about 100 K". The coordinator by the rule: remove "up to about 100 K, and", since no stored source
   gives it. After the second independent check the sentence says what the stored abstract says, "This is high enough
   that the quantum Hall effect of graphene can be measured even at room temperature". Entry 20.
7. The opening argument of Section 4.16. The coordinator by the rule: the smallest change, "one out of every three" and
   the lumps of an irregular choice of the empty orbitals. Entry 22.
8. The geometry of the third paragraph of Section 4.5. The coordinator by the rule: keep it, since it holds for the
   Hall bar of Section 4.2.
9. "For example with a width of 30 sites". The coordinator by the rule first removed it, on the ground that no source
   gives the width. The second independent check found `N = 30` in the two Core cells of the notebook box of Section
   4.10, so by the same rule the width stays, written as the width parameter `N = 30` of the Core cells. Entry 23.
10. The origin of $k_y$ in `ribbon_three` and in the three quiz ribbons of page 05. The coordinator by the rule: keep
    them, since their captions name the walls and the plots have their axes.
11. The sign of the fold of Section 3.6b. Not applied, see below.
12. The bullet of `landau_chern.py` in the conventions sheet. The coordinator by the rule: the bullet of the fixer of g1
    is applied, the open point on the "small" shift is dropped, and the first open point no longer names the figure.
    `conventions.py` now checks the pyqula cell of `g1_landau_levels_square.py`, $C=+1$ for each of the four bands with
    the flux $1/20$ and $-1$ with $-1/20$.
13. The bullet of `flat_chern_band.py` in the conventions sheet. The coordinator by the rule: the bullet and the two
    extra bullets of the fixer of g5 are applied. `conventions.py` checks with pyqula the arguments 0.1155, 0.0927 and
    0.3295, $C=+1$ from the links and from `get_chern`, the widths 2.48 and 0.212, the gaps 1.04 and 2.97, the ratio
    14.0, the spectra of `_honeycomb.bloch` within $2\cdot10^{-15}$, and the width 0.200 and the gap 3.000 of the band
    with $C=0$.
14. The comments of `mufun` in `session4.ipynb`. Not applied, see below.
15. Ticks and units on the six figures of the PDF. Not applied, see below.
16. The legend of the widget `landaufan` and its template. Not applied, see below.
17. The open points of the conventions sheet. The coordinator by the rule: each bullet is kept and marked with how it was
    settled, the section is now "Open points of the old text, settled on 2026-11-22", and the bullet on the caption of
    `landau_chern` is dropped by point 12. The bullets on the sign of $C$, on the order of $x$ and $y$ and on the lumps
    are marked with the decisions of points 3, 2 and 7.
18. The temperature of the GaAs bullet. The coordinator by the rule: "A plateau needs a thermal energy much smaller than
    this spacing, and disorder broadens the levels, so quantum Hall physics in GaAs needs temperatures of the order of one
    kelvin". The present sentence did not follow from 1.7 meV, which is 20 K, and of the two new wordings this one gives
    the reason of the kelvin, while the shorter one states it with no reason. Entry 21.
19. The notebook box of Section 4.19. The coordinator by the rule: "Build the Haldane model and a quantum Hall ribbon,
    follow the straight line between the two Hamiltonians, and watch the bulk gap and the edge branches of the ribbon",
    which matches the cell. Entry 24.

### Not applied

- Point 11, the fold of Section 3.6b. It is a sign on a page of Session 3, which this pass does not edit.
- Point 14, the comments of `mufun`. The notebooks are not edited. The conventions sheet keeps the open point.
- Point 15, the six figures of the PDF. A converted Blender figure and its overlay are not touched, and the point stays
  for the next Blender pass of the session.
- Point 16, the legend of `landaufan`. The widget and its template are files of the toolkit, which this pass does not
  edit. The text of page 11 is true, and the legend is read from the bottom of the band.
- The heading of Section 4.4, part of point 3. "Landau levels as Chern-number-one flat bands" is also the title of the
  manifest, which this pass does not edit, and in words it names the magnitude.
- Other places that write $C=1$ for a Landau level, outside the list of point 3. Session 3 writes "each of them has
  $C=1$" in `session03/05-the-berry-curvature-and-why-the-hall-conductivity-is-an-integer.md` and "flat bands with
  $C=1$" in `session03/index.md`, a sign of Session 3. Session 2 writes "flat bands with Chern number one" in its index
  and in two comesback boxes, edited at the same time by another run. The places of page 05 were applied after the
  second independent check, entry 25.
- The lab box of page 16 keeps "which is the charge $e/m$ of a quasihole for $m=3$". Its electron system has the
  charge $-e$, where a quasihole has the charge $+e/m$, and the box is the reading of a stored source. The sentences that
  say that a quasihole removes the charge $e/m$ hold as they are.
- The caption of Figure 4.2 on page 08, "add up to the same $\varphi$, which is the flux through that plaquette", and
  the same words in `lecture_notes/src/figures/s04f02_gauge.tex`. The caption draws the phases of (4.4), which is
  written with $\hbar=1$, and in that form $\varphi$ is the flux. The second independent check named it as old text of
  the same kind as the quiz of Section 4.7 and gave no correction.
