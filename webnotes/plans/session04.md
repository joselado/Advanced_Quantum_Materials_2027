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

A builder does not decide these. Each is a numbered equation, a statement of the old text or a convention.

1. The factor of the Peierls phase (4.4). Section 4.7 sets $e=1$ and keeps $\hbar$, and (4.5) to (4.8) use
   $\ell_B=\sqrt{\hbar/B}$ and $x_0=\hbar k_y/B$. With these units the phase of minimal coupling (4.3) is
   $(1/\hbar)\int\mathbf A\cdot d\boldsymbol\ell$, while (4.4) prints $\int\mathbf A\cdot d\boldsymbol\ell$. The
   fold of Section 3.6b uses the phase $2\pi\alpha$ per plaquette with $\alpha=Ba^2/(h/e)$, which needs the
   $1/\hbar$.
2. The order of $x$ and $y$ in Section 4.2. The page and the caption of `hall_setup.svg` put the voltage along $y$
   and the current along $x$, and write $I_x=N(e^2/h)V_y$. By the conventions sheet of Session 3 this is the case
   where the $\Omega$ of the notes gives $\sigma_{xy}=-(e^2/h)C$. (4.1) and (3.4) stay as printed, and the sheet
   says that a page does not derive an absolute direction of the current.
3. "Roughly two orders of magnitude" in Section 4.10, in the text after (4.7) and in the caption of Figure 4.4,
   which is a caption of the PDF. With $m^*=0.067\,m_e$ and $v=10^6$ m/s the ratio of $E_1$ of graphene to
   $\hbar\omega_c$ of GaAs is $21$ at $1$ T, $10.5$ at $4$ T and $6.6$ at $10$ T. Section 4.1 says "roughly one
   order of magnitude", and its quiz says "roughly seven times" at $10$ T. The sheet of Session 3 already lists this.
4. "Roughly one millielectronvolt" for GaAs in Section 4.1, "for the fields that we can reach in a laboratory".
   The level spacing is $1.7$ meV at $1$ T and $17.3$ meV at $10$ T, which the quiz of the same file states.
5. The opening argument of Section 4.16. It says that leaving some orbitals empty gives a density "clearly not
   uniform" with lumps. `droplet_density.py` prints the density of the Slater determinant of every third orbital,
   and for $N=20$ it is between $0.324$ and $0.333$ of the full value for $2\ell_B<r<\sqrt{6N}\ell_B-2\ell_B$. Two
   of every three orbitals give $0.665$ to $0.690$. The example "two out of every three" is also the filling
   $2/3$, while the state that the page builds has $1/m$.
6. "The exact ground state of a strongly interacting many-body problem" in Section 4.16. The Laughlin state is the
   exact ground state of a short-range model interaction, the first Haldane pseudopotential, and for the Coulomb
   interaction it is a very accurate trial state and not the exact one. This was not computed here.
7. The charge $+e$ of Section 4.9. The page says that for an electron "every cyclotron orbit and every edge current
   below goes around in the other direction, and nothing else changes". For the charge $-e$ the states of the
   lowest level in the symmetric gauge are functions of $\bar z$, unless the field is reversed. A check by hand gives
   $\pi_x+i\pi_y=-2i\hbar(\partial_{\bar z}+z/4\ell_B^2)$ for $+e$, so (4.9) is right for the convention of
   the page.
8. The text of the widget of Section 4.11 says that the dashed lines are $(n+\tfrac12)\hbar\omega_c$, while the
   levels of the square lattice are $-4t+\hbar\omega_c(n+\tfrac12)$. Whether the widget draws the energy from the
   bottom of the band was not read.
9. The six PDF figures of the session have no ticks and no units, as listed above. They stay as they are unless
   the lecturer asks for a redraw.
