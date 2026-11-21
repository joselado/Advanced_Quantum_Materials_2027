# Plan of Session 8 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session08.md`.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 437 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 (0) | 0 |
| `01-two-classes-of-magnets-and-where-we-find-them.md` | 8.1, 8.2 | 1165 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `03-two-minimal-dimers-a-classical-order-parameter-and-a-quantum-singlet.md` | 8.3 | 962 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1 |
| `04-frustration-as-the-route-to-a-quantum-spin-liquid.md` | 8.4 | 1100 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `05-the-dimerized-heisenberg-model-a-first-step-before-a-spin-liquid.md` | 8.5 | 1006 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | key 1, opener 1 |
| `06-the-resonating-valence-bond-wavefunction-as-the-qsl-ground-state.md` | 8.6 | 1212 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1 |
| `07-why-the-holstein-primakoff-magnon-approach-fails-for-qsl-excitations.md` | 8.7, 8.8 | 1386 | 7 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1 |
| `09-the-mean-field-spinon-hamiltonian-and-its-dispersion-classes.md` | 8.9 | 1122 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1 |
| `10-emergent-gauge-symmetry-and-vison-excitations.md` | 8.10 | 1226 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 2, opener 1, quiz-long 1 |
| `11-from-a-single-kondo-impurity-to-the-kondo-lattice.md` | 8.11, 8.12 | 1343 | 5 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1, quiz-long 1 |
| `13-electronic-structure-of-the-kondo-lattice-and-the-kondo-insulator.md` | 8.13 | 1399 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | opener 1, quiz-long 1 |
| `14-closing-summary.md` | 8.14 | 625 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | quiz-long 1 |

## What every builder of this session needs to know

The conventions sheet `webnotes/conventions/session08.md` did not exist when this plan was written, so the facts
below were checked with a number on 2026-11-21, by runs of pyqula and numpy in the scratch folder of the plan,
except the two marked as derived by hand. A builder takes a sign from the sheet once it exists, and from here
until then.

- pyqula takes the first-neighbor hopping as $+1$. The chain gives $+2$ at $k=0$ and $-2$ at $k=\pi$, so
  $\varepsilon_k=+2\cos k$, while the pages write $-t$ and $-2t\cos k$. A caption that names the band minimum
  says which sign it uses.
- The $\pi$-flux square lattice is `geometry.square_lattice().get_supercell((1,2))` with
  `h.add_orbital_magnetic_field(0.5)`. Its top energy is $2.83=2\sqrt2$, as it should be. With
  `get_supercell((2,1))` the same call gives a top energy of $4.0$, which is the lattice with no flux.
- The dimerized spinon chain is `geometry.bichain()` with `h.intra = 0.6*h.intra`, and its gap is $0.8$,
  which is $2|\chi_1-\chi_2|$.
- `H2HFH(h, JK=g)` of `pyqula.specialhamiltonian` puts $g$ in `h.intra` as the onsite $c$-$f$ mixing, so
  `JK` is the hybridization $\gamma_K$ of (8.21) and not the Kondo coupling $J_K$ of (8.18). On a chain the
  direct gap is $2g$ ($1.0$ for $g=0.5$ and $2.0$ for $g=1$), and the indirect gap is $2(\sqrt{1+g^2}-1)$
  ($0.236$ and $0.828$). It always adds spin, so a chain gives 4 bands.
- `h.get_fermi_surface(e=0., delta=..., nk=...)` on the triangular lattice returns three flat arrays of
  `nk*nk` entries, and it writes `FERMI_MAP.OUT`, so it runs only inside the script that `style.run_script`
  runs. `style.pyqula_kmap` on its output was not tested.
- The identity (8.12) holds on the 16 states of two sites once both have one fermion, and $\chi^\dagger\chi$
  takes the values $0$ and $2$ there (checked with a Jordan-Wigner matrix calculation).
- From (8.18) with $\mathbf S=\tfrac12 f^\dagger\boldsymbol\sigma f$ and $n_f=1$, the Fierz identity gives
  $-J_K(c^\dagger f)(f^\dagger c)+\tfrac12 J_K n_c$. So (8.20) holds up to a shift of the chemical potential of
  the conduction electrons, which the "$\sim$" of the page covers (derived by hand, builder asserts).
- The many-body level diagrams of the session (dimers, four-site chain, plaquette) stay in numpy, since pyqula
  diagonalizes single-particle Hamiltonians.

## Index of the session

File `index.md`, 437 words, numbered equations none.

- Question of the page, and where we arrive: one sentence in front of the first paragraph, "In this session we
  ask what a magnet looks like when it does not break time-reversal symmetry, and what its excitations are",
  and the rest stays.
- Main result for the key box: none, the index is an overview.
- Equation of another page that it starts from, for the recall box: none, the paragraph already names
  (6.5) and (7.3) with their links.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, no quiz on an index.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `concept_map` is a sketch.

## 8.1 Two classes of magnets and where we find them and 8.2 Two emergent excitations, magnons and spinons

File `01-two-classes-of-magnets-and-where-we-find-them.md`, 1165 words, numbered equations none.

- Question of the page, and where we arrive: which magnets does mean-field theory miss, and what are their
  excitations? We arrive at two classes, and at the spinon with $S=1/2$ against the magnon with $S=1$. Section
  8.1 is motivation, 8.2 carries the result. Split the paragraph of 177 words at "Let us now take a quantum
  spin liquid".
- Main result for the key box: unnumbered. Flipping one spin of an ordered magnet changes the total spin by
  $\Delta S=1$, which is the magnon, and leaving one site of a singlet covering unpaired changes it by
  $\Delta S=1/2$, which is the spinon. With an even number of sites spinons come in pairs.
- Equation of another page that it starts from, for the recall box: none, the page starts from Section 6.1 and
  Section 6.13, which have no equation to show.
- Derivation told in words, for a steps fold: none, the counting is two sentences and the problem holds the
  parity argument.
- Lab box, with the source and the number that the source states: `mourigal2013_nphys2652.txt`, neutron
  scattering on a spin-1/2 Heisenberg chain. Quote of the published abstract, "Here, by accurate absolute
  normalization of our inelastic neutron scattering data on a spin-1/2 Heisenberg antiferromagnetic chain
  compound, we account for the full spectral weight to within 99(8)%." and "Its elementary excitations, called
  spinons, are fractional spin-1/2 quasiparticles created and detected in pairs by neutron scattering." The
  $71\%$ of the same abstract is the theory value of the two-spinon states, not a measurement. The text does
  not name the compound, so the box does not name it either. That a magnon would give a sharp line and a pair
  of spinons a continuum is our reading, marked as ours. Link `https://www.nature.com/articles/nphys2652`.
- Pen-and-paper problem: find the allowed total spins of three spin-1/2 sites and their multiplicities. The
  answer is $S=1/2$ twice and $S=3/2$ once, with $2\cdot2+4=8$ states (builder asserts), and from this, by
  adding one spin at a time, an even number of sites has an integer total spin.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 19, 17 words) shortened,
  physics kept. Q2 stays. New picture question, three chains of six sites with singlets drawn as capsules and
  free spins as arrows, "which state has $S_\text{tot}=1$?", options all paired ($S=0$), two unpaired parallel
  spins ($S=1$, correct), and a ferromagnet of six sites with one flipped spin ($S=2$).
- Figures to add, each with its pyqula script or the reason for numpy: the three quiz pictures
  `g1_quiz_spins_paired.py`, `g1_quiz_spins_two.py`, `g1_quiz_spins_flip.py` with a helper `_g1_spins.py`.
  They are sketches with no calculation, saved with `sketch=True`.
- Old figures of the page that break the plot rules: none, `total_spin_ladder` has its axes and ticks. The
  link to Figure 6.5 in the caption of Figure 8.1 and to Section 6.1 stay.

## 8.3 Two minimal dimers, a classical order parameter and a quantum singlet

File `03-two-minimal-dimers-a-classical-order-parameter-and-a-quantum-singlet.md`, 962 words, numbered equations (8.1), (8.2), (8.3).

- Question of the page, and where we arrive: what is the smallest magnet whose ground state keeps
  time-reversal symmetry? The Ising dimer has two ground states that each break it, and the Heisenberg dimer
  has one singlet, (8.3), with $\langle\mathbf S_i\rangle=0$.
- Main result for the key box: (8.3), with $\mathbf S_0\cdot\mathbf S_1=-3/4$ for the singlet and $+1/4$ for
  the triplet, and one sentence that it is unique, time-reversal symmetric and maximally entangled.
- Equation of another page that it starts from, for the recall box: `eq="6.5"`, the Heisenberg model from the
  Hubbard model at large $U$, with $J_{ij}=4t_{ij}^2/U>0$.
- Derivation told in words, for a steps fold: "From the two spins to the singlet and the triplet",
  $\mathbf S_0\cdot\mathbf S_1=\tfrac12(\mathbf S^2-\mathbf S_0^2-\mathbf S_1^2)$ with $\mathbf S_i^2=3/4$,
  which gives $-3/4$ for $S=0$ and $+1/4$ for $S=1$.
- Lab box, with the source and the number that the source states: none. The stored
  `hirjibehedin2006_science.1125398.txt` (chains of Mn atoms seen with STM) states only the count "1 to 10
  manganese atoms" and no coupling, so it has no number of a material with its probe.
- Pen-and-paper problem: show that in the singlet $\langle S_0^zS_1^z\rangle=-1/4$, and that the $x$ and $y$
  terms give $-1/4$ each, so the total is $-3/4$ while the Ising dimer reaches only $-1/4$. The solution ends
  on why the transverse terms are what the Ising dimer misses.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 30) links (8.1) in the
  question, so the question writes $\mathcal H_\text{Ising}=S_0^zS_1^z$ as a display. Q2 stays. New quiz with
  equations as options, "which state is the ground state of $H=\mathbf S_0\cdot\mathbf S_1$?", options
  $(|{\uparrow\downarrow}\rangle-|{\downarrow\uparrow}\rangle)/\sqrt2$ (correct),
  $(|{\uparrow\downarrow}\rangle+|{\downarrow\uparrow}\rangle)/\sqrt2$ (a triplet, $+1/4$) and
  $|{\uparrow\downarrow}\rangle$ (not an eigenstate, energy $-1/4$).
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `dimer_levels` has an energy arrow with no ticks, and
  `dimer_levels_signs` (in Q2) has no energy axis at all. Both get an energy axis in units of $J$ with ticks
  at $-3/4$, $-1/4$, $1/4$, $3/4$, in the helper `_dimerlevels.py`, which they share. They stay numpy, since
  the $4\times4$ spin matrices are a many-body problem.

## 8.4 Frustration as the route to a quantum spin liquid

File `04-frustration-as-the-route-to-a-quantum-spin-liquid.md`, 1100 words, numbered equations none.

- Question of the page, and where we arrive: when does the ground state of a Heisenberg magnet fail to order?
  When no configuration satisfies every bond, and on the triangular and kagome lattices the classical
  degeneracy becomes macroscopic. Split the first paragraph (154 words) at "This geometric frustration".
- Main result for the key box: unnumbered. Three Ising spins on an antiferromagnetic triangle have six ground
  states out of eight, and on the triangular and kagome lattices the number of ground states grows as
  $e^{sN}$, with $s=0.32$ and $s=0.50$, which the figure `ising_degeneracy` asserts.
- Equation of another page that it starts from, for the recall box: `eq="8.3"`, the singlet whose macroscopic
  version we look for.
- Derivation told in words, for a steps fold: "Counting the ground states of the triangle". With $M$ the total
  $S^z$, $\sum_{\langle ij\rangle}S_i^zS_j^z=\tfrac12(M^2-\tfrac34)$, so $M=\pm1/2$ gives $-1/4$ with $3+3=6$
  states and $M=\pm3/2$ gives $+3/4$ with two.
- Lab box, with the source and the number that the source states: `helton2007_physrevlett.98.107204.txt`,
  arXiv abstract, "The susceptibility indicates a Curie-Weiss temperature of ~ -300 K; however, no magnetic
  order is observed down to 50 mK." The compound is the kagome antiferromagnet ZnCu$_3$(OH)$_6$Cl$_2$ of the
  title. The text does not say "herbertsmithite", so the box names the formula. The ratio of the two
  temperatures, about $6000$, is ours (`ours="6000"`). Link `https://doi.org/10.1103/PhysRevLett.98.107204`.
- Pen-and-paper problem: count the ground states of four antiferromagnetic Ising spins on a square plaquette
  (four bonds) and on a tetrahedron (six bonds). The answers are $2$ and $6$, with
  $\sum_{i<j}S_i^zS_j^z=\tfrac12(M^2-1)$ for the tetrahedron (builder asserts).
- Quizzes to rewrite, and a picture question or equations as options: Q2 (line 31, 19 words) shortened. Q1
  stays. New picture question, three clusters of Ising spins with antiferromagnetic bonds, a triangle, a square
  plaquette and a tetrahedron, "in which cluster can every bond be satisfied?", correct the square plaquette.
- Figures to add, each with its pyqula script or the reason for numpy: the three pictures
  `g2_quiz_cluster_triangle.py`, `g2_quiz_cluster_square.py`, `g2_quiz_cluster_tetra.py` with `_g2_cluster.py`,
  sketches with `sketch=True`.
- Old figures of the page that break the plot rules: none. The links to Figure 6.3 in the text and in the
  caption of Figure 8.2, and the panel of `s06f03_frustration` in Q2, stay.

## 8.5 The dimerized Heisenberg model, a first step before a spin liquid

File `05-the-dimerized-heisenberg-model-a-first-step-before-a-spin-liquid.md`, 1006 words, numbered equations (8.4), (8.5).

- Question of the page, and where we arrive: can a macroscopic Heisenberg model have a ground state with no
  order? Yes, the product of singlets (8.5), and its excitation is the triplon with spin $1$, so this valence
  bond solid is not yet a spin liquid.
- Main result for the key box: (8.5) with $\langle\mathbf S_i\rangle=0$, where it stands, and one sentence that
  it is the exact ground state of (8.4) and that the lowest excitation turns one singlet into a triplet, costs
  $J$ and has $S=1$.
- Equation of another page that it starts from, for the recall box: `eq="8.3"`, the two-site singlet.
- Derivation told in words, for a steps fold: "From (8.4) to the ground state (8.5) and its gap". The dimer
  terms commute, so the eigenstates are products. Each bond gives $-3J/4$ or $+J/4$, the ground state has all
  singlets with $E_0=-3NJ/8$ for $N$ sites, and the reduced state of one site is $\tfrac12$ times the identity,
  so $\langle\mathbf S_i\rangle=0$.
- Lab box, with the source and the number that the source states: none, no stored text states a number of a
  dimerized magnet.
- Pen-and-paper problem: two dimers coupled by $J'\,\mathbf S_1\cdot\mathbf S_2$, the ground energy to second
  order. The answer is $E_0\approx-\tfrac32J-\tfrac{3J'^2}{32J}$, which gives $-1.500938J$ at $J'=0.1J$, against
  $-1.500961J$ of the exact diagonalization of `dimerized_levels` (both computed). The solution ends on the gap
  of order $J$ that keeps the state smooth.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 21) links (8.5) and Q2
  (line 37) links (8.4) in the question, so each writes its equation as a display. New quiz with equations as
  options, "what is the ground energy of (8.4) with $N$ sites?", options $-3NJ/8$ (correct), $-3NJ/4$ (one
  singlet per site, twice too many) and $-NJ/8$ (the Ising value $-J/4$ per dimer, without the $x$ and $y$
  terms).
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `dimerized_levels` has its axes and ticks. It stays
  numpy, as exact diagonalization of four spins.

## 8.6 The resonating valence bond wavefunction as the QSL ground state

File `06-the-resonating-valence-bond-wavefunction-as-the-qsl-ground-state.md`, 1212 words, numbered equations (8.6), (8.7).

- Question of the page, and where we arrive: how do we write a ground state in which the singlets are not
  frozen? We take a BCS state of auxiliary fermions and project it onto one fermion per site, which is the RVB
  state (8.7).
- Main result for the key box: (8.7), with $P_G=\prod_in_i(2-n_i)$ equal to $1$ for one fermion on the site and
  $0$ otherwise, and one sentence that the result is a superposition over all pairings.
- Equation of another page that it starts from, for the recall box: `eq="5.4"`, the mean-field pairing
  Hamiltonian of Section 5.5, whose ground state is the BCS state (8.6).
- Derivation told in words, for a steps fold: "Why resonance lowers the energy of a plaquette". On the square
  of four sites with sublattices $A$ and $B$, $H=\tfrac J2(\mathbf S^2-\mathbf S_A^2-\mathbf S_B^2)$, which gives
  $-2J$ for $S=0$, $S_A=S_B=1$. A single covering has two singlet bonds at $-3J/4$ and two bonds at $0$, so
  $-3J/2$. These are the values of `rvb_plaquette`.
- Lab box, with the source and the number that the source states: none. The stored `han2012_nature11659.txt`
  reports a spinon continuum in herbertsmithite with neutron scattering but states no number.
- Pen-and-paper problem: check $P_G$ on the four states of one site, show that it is a projector,
  $(n(2-n))^2=n(2-n)$ for $n=0,1,2$, and count how many of the $4^4=256$ states of four sites survive, which is
  $2^4=16$.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 22) links (8.6) in the
  question, so it writes the BCS state as a display. Q2 stays. New quiz with equations as options, "which
  operator keeps only one fermion on a site?", options $n(2-n)$ (correct), $n(n-1)/2$ (keeps the double
  occupation) and $1-n$ (keeps the empty site).
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `rvb_plaquette` has its axes and ticks, numpy as a
  many-body calculation.

## 8.7 Why the Holstein-Primakoff magnon approach fails for QSL excitations and 8.8 The parton construction with Abrikosov fermions and the single-occupancy constraint

File `07-why-the-holstein-primakoff-magnon-approach-fails-for-qsl-excitations.md`, 1386 words, numbered equations (8.8), (8.9), (8.10), (8.11), (8.12), (8.13), (8.14).

- Question of the page, and where we arrive: 8.7 asks whether magnons can describe the excitations of a spin
  liquid, and (8.9) says no. 8.8 asks how we write a spin with fermions, and arrives at (8.10) with the
  constraint (8.11) and the bond identity (8.12).
- Main result for the key box: two boxes, each around one equation where it stands, since a repeated `\tag` is
  an error of the build. In 8.7, (8.9), with one sentence that the linearization needs a boson density much
  smaller than $S$. In 8.8, (8.11), with one sentence that under this constraint (8.10) writes a spin exactly
  and the Heisenberg bond becomes (8.12).
- Equation of another page that it starts from, for the recall box: `eq="6.6"`, the exact Holstein-Primakoff
  map of Session 6, of which (8.8) is the linearized form.
- Derivation told in words, for a steps fold: "From the Fierz identity to (8.12)". The simplest case first,
  a singlet bond, where $\chi^\dagger\chi=2$, then the operator steps with the constraint on both sites. The
  builder keeps the order $\chi_{ij}^\dagger\chi_{ij}$ of the page, with $\chi_{ij}^\dagger=\chi_{ji}$, and an
  assert on the 16 states of two sites.
- Lab box, with the source and the number that the source states: none here, since the spinon measurement of
  `mourigal2013_nphys2652.txt` is planned on the page of 8.2.
- Pen-and-paper problem: with $S^+=f_\uparrow^\dagger f_\downarrow$, $S^-=f_\downarrow^\dagger f_\uparrow$ and
  $S^z=\tfrac12(n_\uparrow-n_\downarrow)$, show $[S^+,S^-]=2S^z$, and that $\mathbf S^2=3/4$ on the two singly
  occupied states and $0$ on the empty and the doubly occupied one.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 20) links (8.8) and Q2
  (line 74) links (8.12) in the question, so each writes its equation as a display. New quiz with equations as
  options, "which operator is $S_i^z$ in Abrikosov fermions?", options
  $\tfrac12(n_{i\uparrow}-n_{i\downarrow})$ (correct), $\tfrac12(n_{i\uparrow}+n_{i\downarrow})$ (this is half the
  occupation) and $f_{i\uparrow}^\dagger f_{i\downarrow}$ (this is $S_i^+$).
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `hp_boson_density` has its axes. The panel of
  `s06f05_magnon` stays.

## 8.9 The mean-field spinon Hamiltonian and its dispersion classes

File `09-the-mean-field-spinon-hamiltonian-and-its-dispersion-classes.md`, 1122 words, numbered equations (8.15).

- Question of the page, and where we arrive: what does the decoupled spin problem look like, and what spinon
  bands can it give? A tight-binding model (8.15) at half filling, with gapless, gapped or Dirac spinons. Split
  the paragraph of 172 words at "Equation (8.15) is a tight-binding model".
- Main result for the key box: (8.15), with one sentence that the spinons fill half of the bands because of
  (8.11). The sentence on time-reversal symmetry waits for the lecturer, see "Open for the lecturer".
- Equation of another page that it starts from, for the recall box: `eq="8.13 8.14"`, the quartic Hamiltonian
  and its decoupling.
- Derivation told in words, for a steps fold: "From the decoupling (8.14) to the hopping model (8.15)", with
  the coefficient of $f_i^\dagger f_j$ equal to $-\tfrac12J_{ij}\langle\chi_{ij}\rangle^*$ and the Lagrange
  multiplier of the constraint, all checked with a number before the fold states it.
- Lab box, with the source and the number that the source states: `helton2007_physrevlett.98.107204.txt`,
  arXiv abstract, "Inelastic neutron scattering reveals a spectrum of low energy spin excitations with no
  observable gap down to 0.1 meV." and "These results suggest that an unusual spin-liquid state with
  essentially gapless excitations is realized in this kagome lattice system." That this fits the class of
  gapless spinons is ours. The notebook source `ruan2021_s41567-021-01321-0.txt` (spinon Fermi surface of
  1T-TaSe$_2$ seen with STM) states no number in either abstract, "1T" is the name of the polytype, so it gives
  no box.
- Pen-and-paper problem: the self-consistent bond of the uniform chain at half filling. Per spin
  $\langle f_i^\dagger f_{i+1}\rangle=1/\pi$, so $\langle\chi\rangle=2/\pi\approx0.64$, and the spinon hopping
  is $J/\pi$ with a bandwidth $4J/\pi\approx1.27J$ (derived by hand, builder asserts). The solution says that
  this is a mean-field number.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 29) links (8.15) in the
  question, so it writes the model as a display. Q2 (line 45) waits for the lecturer, since its correct option
  reads "$\langle\mathbf S_i\rangle=0$, so the state is time-reversal symmetric". New picture question, three
  spinon band structures at half filling, "which one has Dirac spinons?", options the uniform chain, the
  dimerized chain and the $\pi$-flux square lattice (correct).
- Figures to add, each with its pyqula script or the reason for numpy: a new map
  `g3_fermi_surface_triangular.py` from the pyqula script `g3_spinon_fermi_surface.py` (the notebook cell,
  `tij=[1.,t2]`, `set_filling(0.5)`, `get_fermi_surface`), for $t_2/t_1=-0.5$, $0$, $0.5$, in the hexagonal zone
  with `kaxes` and a sequential colorbar. The three quiz pictures `g3_quiz_bands_chain.py`,
  `g3_quiz_bands_dimer.py`, `g3_quiz_bands_piflux.py` draw from the script of the redrawn figure below.
- Old figures of the page that break the plot rules: `spinon_bands` has a momentum axis with no ticks and no
  named points, and it is numpy where pyqula can do it. It is redrawn from a pyqula script
  `g3_spinon_band_classes.py` (chain, bichain with `h.intra=0.6*h.intra`, the $\pi$-flux lattice of the list
  above), with ticks at $-\pi$, $0$, $\pi$ and the Dirac point named, and the caption gives the sign of the
  hopping.

## 8.10 Emergent gauge symmetry and vison excitations

File `10-emergent-gauge-symmetry-and-vison-excitations.md`, 1226 words, numbered equations (8.16).

- Question of the page, and where we arrive: what does the fermion rewriting add that the spin did not have?
  A local phase freedom (8.16), under which the link phases change and the flux through a plaquette does not,
  and the vison as a flipped flux. Split the paragraphs of 151 words (at "This is the structure of a lattice
  gauge theory") and of 265 words (at "Let us write the mean-field Hamiltonian" and at "This single flipped
  plaquette").
- Main result for the key box: (8.16), with the flux $\Phi=\prod e^{i\theta_{ij}}$ as the quantity that does not
  change. The sentence on which flux is the ground state waits for the lecturer.
- Equation of another page that it starts from, for the recall box: `eq="8.10 8.11"`, the spin operator and the
  constraint, which do not change under (8.16).
- Derivation told in words, for a steps fold: "Why the flux does not change under (8.16)". The phase cancels in
  $f_{i\alpha}^\dagger f_{i\beta}$ on one site, and around a plaquette the sum of $\theta_i-\theta_j$ is zero.
  The fold writes which object it transforms, the operator of (8.12) or the coefficient of (8.15), see "Open
  for the lecturer".
- Lab box, with the source and the number that the source states: none. The stored
  `semeghini2021_science.abi8794.txt` detects a spin liquid of the toric code type with string operators, but
  on a quantum simulator, and its only number is the count "219-atom", which is not a number of a material
  with its probe.
- Pen-and-paper problem: a string of $n$ links with $\chi=-1$ from the edge of an open square lattice. Show
  that only the plaquette at the end of the string has $\Phi=-1$, since the plaquettes along it have two
  flipped links. For the $6\times6$ lattice of `gauge_levels` this is one of 25 plaquettes, which its assert
  checks (the fluxes sum to 23).
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 16) links (8.16) in the question,
  so it writes the rotation as a display. Q2 (line 32, 18 words) shortened. New picture question, three
  plaquettes with the sign of each link, "which plaquette has $\Phi=-1$?", options one negative link (correct),
  two negative links and four negative links.
- Figures to add, each with its pyqula script or the reason for numpy: the three pictures
  `g3_quiz_plaquette_one.py`, `g3_quiz_plaquette_two.py`, `g3_quiz_plaquette_four.py` with `_g3_plaquette.py`,
  sketches.
- Old figures of the page that break the plot rules: none. `gauge_levels` has its axes, and its axis name
  $E_n-E_n^{(0)}$ can get "in units of $|\chi|$", which the caption already says. It stays numpy, since it puts a
  chosen phase on single links.

## 8.11 From a single Kondo impurity to the Kondo lattice and 8.12 Solving the Kondo lattice with the parton method and a hybridization

File `11-from-a-single-kondo-impurity-to-the-kondo-lattice.md`, 1343 words, numbered equations (8.17), (8.18), (8.19), (8.20), (8.21).

- Question of the page, and where we arrive: 8.11 asks what a local moment does in a metal, and a lattice of
  them, and arrives at a singlet with a conduction electron and a screening that is shared. 8.12 asks how we
  solve the lattice, and arrives at the hybridization Hamiltonian (8.21).
- Main result for the key box: two boxes. In 8.11, (8.18), with one sentence on the shared screening. In 8.12,
  (8.21), with one sentence that $\gamma_K$ is the only mean-field parameter.
- Equation of another page that it starts from, for the recall box: `eq="8.10 8.11"`, the Abrikosov fermions and
  the constraint that 8.12 uses again.
- Derivation told in words, for a steps fold: "From the Kondo lattice (8.18) to the hybridization (8.21)". The
  Fierz identity with $n_f=1$ gives $-J_K(c^\dagger f)(f^\dagger c)+\tfrac12J_Kn_c$, the second term shifts the
  chemical potential, and the decoupling gives $\gamma_K=J_K\langle\sum_\sigma c_{j\sigma}^\dagger
  f_{j\sigma}\rangle$ up to the sign of (8.21), which the builder fixes with a number.
- Lab box, with the source and the number that the source states: none. The stored
  `madhavan1998_science.280.5363.567.txt` (the Kondo resonance of one cobalt atom seen with STM) and the notebook
  source `vano2021_s41586-021-04021-0.txt` state no number.
- Pen-and-paper problem: one impurity spin and one conduction electron on the same site, $H_K=J_K(c^\dagger
  \boldsymbol\sigma c)\cdot\mathbf S=2J_K\,\mathbf s\cdot\mathbf S$. The singlet is at $-3J_K/2$ and the triplet at
  $+J_K/2$, so the gap is $2J_K$ (derived by hand, builder asserts), the same algebra as (8.3).
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 57, 17 words) shortened, and it
  links (8.18), so it writes the Kondo coupling as a display. Q2 (line 73) links (8.21), so it writes the
  Hamiltonian as a display. New quiz with equations as options, "which term mixes the conduction electrons and
  the $f$ fermions?", options $-\gamma_Kf_{\mathbf k}^\dagger c_{\mathbf k}+\text{h.c.}$ (correct),
  $\varepsilon_{\mathbf k}c_{\mathbf k}^\dagger c_{\mathbf k}$ and $-J_K(c^\dagger f)(f^\dagger c)$ (quartic, before the
  decoupling).
- Figures to add, each with its pyqula script or the reason for numpy: none, the bands are on the page of 8.13.
- Old figures of the page that break the plot rules: none, `kondo_screening` is a sketch. The try-it names
  `JK`, which is $\gamma_K$, see "Open for the lecturer".

## 8.13 Electronic structure of the Kondo lattice and the Kondo insulator

File `13-electronic-structure-of-the-kondo-lattice-and-the-kondo-insulator.md`, 1399 words, numbered equations none.

- Question of the page, and where we arrive: why does a lattice of local moments turn a metal into an
  insulator? Per spin (8.21) is a two-band Bloch Hamiltonian, the flat $f$ band and the conduction band
  anti-cross, and with one $f$ fermion per site and a half-filled conduction band the lower band is full.
- Main result for the key box: unnumbered, $E_\pm(\mathbf k)=\tfrac12\big(\varepsilon_{\mathbf
  k}\pm\sqrt{\varepsilon_{\mathbf k}^2+4\gamma_K^2}\big)$, the direct gap $2\gamma_K$ at the crossing, and the
  Fermi level in the gap at this filling.
- Equation of another page that it starts from, for the recall box: `eq="8.21"`.
- Derivation told in words, for a steps fold: "From (8.21) to the gap". The $2\times2$ matrix per $\mathbf k$,
  its eigenvalues, $\pm\gamma_K$ at $\varepsilon_{\mathbf k}=0$, and for the chain the indirect gap
  $2(\sqrt{t^2+\gamma_K^2}-t)\approx\gamma_K^2/t$, which `kondo_bdg` asserts. Then the count of particles.
- Lab box, with the source and the number that the source states: `jiang2013_ncomms4010.txt`, ARPES on SmB$_6$.
  Quote of the Crossref abstract, "These states vanish simultaneously with the hybridization gap at around
  150 K.", with "SmB6, a well-known Kondo insulator, exhibits a transport anomaly at low temperature." That the
  gap of (8.21) is the gap seen here is ours. The in-gap states are surface states and not part of (8.21), and
  the box says so. Link `https://www.nature.com/articles/ncomms4010`.
- Pen-and-paper problem: for the chain with $t=1$ and $\gamma_K=0.6$, compute the indirect gap,
  $2(\sqrt{1.36}-1)=0.33$, and compare with $\gamma_K^2/t=0.36$.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 20) links (8.21), so it writes
  the Hamiltonian per $\mathbf k$ as a display. Q2 (line 36, 16 words) shortened. New picture question, three
  band structures of the chain with the Fermi level drawn, "which one is a Kondo insulator?", options no
  hybridization (metal), a hybridization with one particle per $\mathbf k$ and spin, so the Fermi level is in the
  gap (correct), and the same hybridization with fewer conduction electrons, so the Fermi level cuts the lower
  band (metal). A shift of the conduction band alone does not give the third picture, since the determinant of
  the $2\times2$ matrix is $-\gamma_K^2$ and the gap always holds the $f$ level at zero. The Fermi level of each
  picture is placed by the count of particles, and the builder asserts it.
- Figures to add, each with its pyqula script or the reason for numpy: a new figure
  `g4_kondo_lattice_bands.py` from the pyqula script `g4_kondo_lattice_bands.py` in `webnotes/scripts/session08/`
  (the notebook cell, triangular lattice, `add_onsite(-2.0)`, `H2HFH` with `JK` $=0$, $0.25$, $0.5$, path
  $\Gamma$-$K$-$M$-$\Gamma$, `operator="dispersive_electrons"`), colored by the weight of the conduction electrons
  with a colorbar from $0$ to $1$. The run of the plan gave 4 bands and a gap between the second and the third band of
  $0.028$ for `JK=0.25` and $0.111$ for `JK=0.5` on a 60 by 60 mesh, and the builder asserts where the Fermi
  level is. The three quiz pictures `g4_quiz_kondo_metal.py`, `g4_quiz_kondo_insulator.py`,
  `g4_quiz_kondo_shifted.py` draw from a pyqula script `g4_kondo_chain_bands.py` (`geometry.chain()` with
  `H2HFH`).
- Old figures of the page that break the plot rules: `hybrid_gap` (in Q2) has a momentum axis with no ticks, and
  `kondo_bdg` has an energy axis with no unit and no ticks. Both get ticks and $E/t$. The Kondo half of both can
  come from `g4_kondo_chain_bands.py`, since `JK` is $\gamma_K$. The superconducting half of `kondo_bdg` uses
  `h.add_swave` only if the conventions sheet confirms its gap, which the plan did not test, and otherwise it stays
  numpy.

## 8.14 Closing summary

File `14-closing-summary.md`, 625 words, numbered equations none.

- Question of the page, and where we arrive: what did we build, and what can we now compute? The bullets stay,
  and a list of tasks with the section of each follows them, as in Section 3.13.
  - Find the levels of the Ising and the Heisenberg dimer, and say why only the singlet keeps time reversal, in
    Section 8.3.
  - Count the classical ground states of a frustrated cluster, in Section 8.4.
  - Tell a valence bond solid from an RVB state by the spin of its excitations, in Section 8.5 and Section 8.6.
  - Say why the Holstein-Primakoff expansion fails when $\langle\mathbf S_i\rangle=0$, in Section 8.7.
  - Write a spin with Abrikosov fermions and the constraint, and get the spinon hopping model, in Section 8.8
    and Section 8.9.
  - Tell gapless, gapped and Dirac spinons apart in a band structure, in Section 8.9.
  - Say which quantity of the gauge field is physical and what a vison is, in Section 8.10.
  - Compute the bands of the Kondo lattice per spin, the gap $2\gamma_K$ at the crossing, and why the filling
    gives an insulator, in Section 8.12 and Section 8.13.
- Main result for the key box: none, a summary.
- Equation of another page that it starts from, for the recall box: none, the summary links its equations.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: Q1 (line 18, 18 words) shortened. No new
  quiz, since the plan of 2026-11-06 puts none in the closing sections.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, Figure 8.1 is shown again.

## Candidates for the lab boxes

These are the "In the lab" cells of the notebook, the first sources to use. Each one is fetched and
stored with `webnotes/labsource.py` before a box quotes it.

- Signatures of spinon Fermi surfaces in the triangular lattice have been observed with scanning tunnel microscopy https://www.nature.com/articles/s41567-021-01321-0
- Heavy fermions in a van der Waals heterostructure leading to a Kondo insulator have been observed in 1T-TaS2/1H-TaS2 heterostructures https://www.nature.com/articles/s41586-021-04021-0

Both notebook sources are stored with their published and arXiv abstracts, and neither states a number of the
material, so neither gives a box. The stored texts in `webnotes/sources/.full/session08/` are the following.

- `helton2007_physrevlett.98.107204.txt`, ZnCu$_3$(OH)$_6$Cl$_2$, $-300$ K, $50$ mK and $0.1$ meV. Used on 8.4 and 8.9.
- `mourigal2013_nphys2652.txt`, a spin-1/2 Heisenberg chain compound, $99(8)\%$. Used on 8.2.
- `jiang2013_ncomms4010.txt`, SmB$_6$, $150$ K. Used on 8.13.
- `ruan2021_s41567-021-01321-0.txt` and `vano2021_s41586-021-04021-0.txt`, the notebook sources, no number.
- `han2012_nature11659.txt`, herbertsmithite, no number. It is the only text that gives the name
  "herbertsmithite", for ZnCu$_3$(OD)$_6$Cl$_2$.
- `semeghini2021_science.abi8794.txt`, a simulator with "219-atom", not used.
- `hirjibehedin2006_science.1125398.txt`, "1 to 10 manganese atoms", not used.
- `madhavan1998_science.280.5363.567.txt`, no number, not used.

The export API of arXiv answered HTTP 429 during the fetch, so the arXiv abstracts were read at
`https://arxiv.org/abs/ID` and attached with `--paste`, and the DOI that each arXiv page gives was checked against
the article.

## Builder groups

- `g1`: `index.md`, `01-two-classes-of-magnets-and-where-we-find-them.md`,
  `03-two-minimal-dimers-a-classical-order-parameter-and-a-quantum-singlet.md`. The index gets its opening
  question. The page of 8.3 owns the helper `_dimerlevels.py` and its two figures.
- `g2`: `04-frustration-as-the-route-to-a-quantum-spin-liquid.md`,
  `05-the-dimerized-heisenberg-model-a-first-step-before-a-spin-liquid.md`,
  `06-the-resonating-valence-bond-wavefunction-as-the-qsl-ground-state.md`. They share Figure 8.3 and the
  singlet coverings, from the frustrated triangle to the resonating plaquette.
- `g3`: `07-why-the-holstein-primakoff-magnon-approach-fails-for-qsl-excitations.md`,
  `09-the-mean-field-spinon-hamiltonian-and-its-dispersion-classes.md`,
  `10-emergent-gauge-symmetry-and-vison-excitations.md`. They share Figure 8.4 and the bond variable
  $\chi_{ij}$, whose meaning in (8.12), (8.14), (8.15) and (8.16) must be the same in the three folds.
- `g4`: `11-from-a-single-kondo-impurity-to-the-kondo-lattice.md`,
  `13-electronic-structure-of-the-kondo-lattice-and-the-kondo-insulator.md`, `14-closing-summary.md`. The first
  two share the model (8.21), Figure 8.6 and the scripts `g4_kondo_chain_bands.py` and
  `g4_kondo_lattice_bands.py`, and the closing page lists the tasks of all the sections.

## Open for the lecturer

1. The vison and the flux of the ground state, in Section 8.10 and in the caption of Figure 8.5. The page says
   "let us take a square lattice where the hoppings around every elementary loop pick up the phase $\Phi=+1$,
   which is a ground state, except for one loop", and the caption says "flipping a single plaquette to
   $\Phi=-1$ costs energy". We take the uniform $|\chi|=1$ of `gauge_levels` on an open $L\times L$ square
   lattice at half filling, flip the sign of the vertical links between rows $L/2-1$ and $L/2$ for $x<L/2$, as
   `gauge_levels` does for $L=6$, and sum the lowest $L^2/2$ levels of one spin species. The flipped plaquette in
   the middle lowers this sum by $0.74$ for $L=6$, $0.72$ for $L=8$, $0.70$ for $L=10$ and $0.69$ for $L=12$, in
   units of $|\chi|$. In the bulk, on a k-mesh of 400 by 400, the $\pi$-flux state gives $-0.958$ per site
   against $-0.811$ for zero flux. So at fixed $|\chi|$ and half filling the flux $\pi$ is lower on the square
   lattice, and a flipped plaquette in the zero-flux background lowers the energy. The numbers come from a numpy
   diagonalization of about twenty lines, which the builder of the group writes again as a check script if the
   lecturer picks one of the last two options.
   - Keep the text and add that the zero-flux background is a choice for concreteness.
   - Define the vison as a plaquette whose flux differs by $\pi$ from the flux of the ground state, and say that
     on the half-filled square lattice this ground-state flux is $\pi$.
   - Take the $\pi$-flux state as the background, and the vison as one plaquette with $\Phi=+1$.
2. Time-reversal symmetry of the spinon mean field, in Section 8.9 and in its Q2. The page says "If we take the
   same $\chi_{ij}$ for spin up and spin down, we keep $\langle\mathbf S_i\rangle=0$ exactly, so the ground state
   that we obtain is time-reversal symmetric by construction", and the correct option of Q2 reads
   "$\langle\mathbf S_i\rangle=0$, so the state is time-reversal symmetric". Time reversal turns the
   spin-independent $\chi_{ij}$ into $\chi_{ij}^*$, so the state keeps it only when the fluxes are $0$ or $\pi$. A
   complex $\chi_{ij}$ with another flux gives $\langle\mathbf S_i\rangle=0$ and breaks time reversal, which is a
   chiral spin liquid (worked out by hand, not computed).
   - Add "for real $\chi_{ij}$, or fluxes $0$ and $\pi$" to the sentence and to the option.
   - Keep the sentence and change only the option to "$\langle\mathbf S_i\rangle=0$ for any $\chi_{ij}$".
3. The sign of the phase in (8.16) and the two meanings of $\chi_{ij}$. Equation (8.12) defines $\chi_{ij}$ as
   the operator $\sum_\sigma f_{i\sigma}^\dagger f_{j\sigma}$, which under (8.16) gets $e^{-i(\theta_i-\theta_j)}$,
   while in (8.15) $\chi_{ij}$ is the coefficient of $f_i^\dagger f_j$, which must get $e^{+i(\theta_i-\theta_j)}$
   for $\mathcal H_\text{MF}$ to stay the same. The page and its Q1 write $e^{i(\theta_i-\theta_j)}$ for "the
   mean-field bond variable", which is right for the coefficient.
   - Keep the symbols and add one sentence that in (8.15) and (8.16) $\chi_{ij}$ is the coefficient.
   - Give the coefficient of (8.15) its own symbol, such as $t_{ij}$, which touches a numbered equation.
4. The values of $J_K$ in Section 8.13 and in the try-it boxes of 8.11 and 8.13. The page says "At $J_K=0.25$
   there is already a visible gap at the crossing. At $J_K=0.5$ the gap is much larger", and these are the
   values of `JK` in the notebook. In pyqula `JK` is the hybridization $\gamma_K$ of (8.21), with a direct gap
   $2\,$`JK` on a chain.
   - Write $\gamma_K=0.25$ and $\gamma_K=0.5$ in the text, and keep `JK` in the try-its with "which is $\gamma_K$".
   - Keep $J_K$ and add one sentence that the notebook calls $\gamma_K$ `JK`.
5. Key boxes on pages with no numbered equation, 8.2, 8.4 and 8.13. The plan puts an unnumbered display in each
   box. A numbered one would need a new tag such as `\tag{8.21a}`.
   - Unnumbered displays in the boxes.
   - New tags with a letter for the result of 8.13 only.
