# Plan of Session 1 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session01.md`.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 400 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 (0) | 0 |
| `01-why-quantum-materials-and-why-now.md` | 1.1 | 806 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | long-paragraph 1, opener 1 |
| `02-a-tour-of-the-quantum-materials-we-will-meet.md` | 1.2 | 1191 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | opener 1 |
| `03-emergent-quasiparticles-and-what-the-lattice-gives-us.md` | 1.3 | 1028 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | opener 1 |
| `04-setting-up-the-formalism-with-the-schrodinger-equation-in-two-ways.md` | 1.4 | 701 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `05-a-warm-up-in-first-quantization-and-the-puzzle-that-breaks-it.md` | 1.5, 1.6, 1.7 | 1257 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1 |
| `08-first-versus-second-quantization-for-the-same-problem.md` | 1.8, 1.9, 1.10 | 1467 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | opener 1 |
| `11-spontaneous-symmetry-breaking-and-why-a-symmetric-hamiltonian-can-have-an-asymmetric-ground-state.md` | 1.11a | 959 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 3 (0) | long-paragraph 1, opener 1 |
| `11b-classifying-states-of-matter-by-the-symmetry-they-break.md` | 1.11b | 1232 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1 |
| `12-the-general-interacting-hamiltonian-and-the-tool-we-will-use-on-it.md` | 1.12 | 917 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | key 1, opener 1 |
| `13-worked-example-1-the-charge-density-wave.md` | 1.13 | 1215 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1, quiz-long 1 |
| `14-worked-example-2-magnetism.md` | 1.14, 1.15 | 1433 | 4 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1 |
| `16-closing-summary.md` | 1.16 | 670 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | 0 |

The numbered equations live in these files, so a recall box can only show an equation of another file. (1.1),
(1.2) and (1.3) are in `05`, (1.4) is in `11b`, (1.5) in `12`, (1.6) in `13`, and (1.7) to (1.10) in `14`. Every
number given below for a problem or a quiz was computed on 2026-11-21 in the scratch folder of the plan, or it is
an `assert` of a figure script that exists today. The builder keeps it as an `assert` in the check script of its
page.

## What the builders need from the conventions sheet

The sheet `webnotes/conventions/session01.md` does not exist yet, and `webnotes/scripts/RECIPES.md` has no
mean-field recipe. The pyqula scripts below are named with what they compute, and their calls are taken from the
notebook `session1.ipynb`. The sheet has to fix these facts with a number before a builder writes a caption.

- The default first-neighbor hopping of pyqula is $+1$, as (1.2) writes it, while (1.6) and (1.7) write $-t$. On
  the chain, the two-site cell and the honeycomb lattice the set of levels and the densities do not depend on this
  sign, but the band against $k$ and the sign pattern of a state do. Checked on 2026-11-21, `geometry.chain()` gives
  $E(k)=+2\cos k$, with $E=2$ at $k=0$ and $-2$ at $k=\pi$, the mirror of $-2t\cos k$ of `filling_bands.svg`. For the
  pyqula island the lowest state changes sign on every bond, and only for $-t$ is it the state with no node.
  `geometry.bichain()` with `add_sublattice_imbalance(0.6)` gives the onsite energies $+0.6$ and $-0.6$ and the
  levels $\pm0.6$ at the zone edge, so the gap is $2m$.
- `h.get_mean_field_hamiltonian(U=..., mf="antiferro")`, which $U$ it means (the term $U n_\uparrow n_\downarrow$
  of (1.7) or a shifted one), and how `get_vev("mz")` relates to $m$ of (1.8), $m$ or $m/2$.
- `h.get_mean_field_hamiltonian(V1=..., mf="CDW", filling=0.5)`, whether it keeps only the Hartree term, as the
  text of Section 1.13 says, or also the Fock term on the bond. The gap is $2V\delta$ only for the Hartree term.
- `h.add_sublattice_imbalance(m)`, whether it gives onsite energies $\pm m$, so that the gap is $2m$.
- Time reversal of one spin as $\hat T = i\sigma_y K$, with $\hat T^2=-1$, and the gauge transformation (1.10).

## Index of the session

File `index.md`, 400 words, no numbered equation.

- Question of the page, and where we arrive: there already, "How do we go from a single atom ... to a quantum
  material". No edit is needed. The lint does not check the opener of an index page.
- Main result for the key box: none, the index is the plan of the session.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, the index has no quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none. `session_map.svg` is a concept map, not a plot.

## 1.1 Why quantum materials, and why now

File `01-why-quantum-materials-and-why-now.md`, 806 words, numbered equations none. A page of motivation.

- Question of the page, and where we arrive: why do the materials of the next technologies need quantum
  mechanics and not classical physics? We arrive at two gaps that look alike, one that single electrons feel and
  one that exists only because electrons pair. The first sentence today is "Before we start ...", which the lint
  reports.
- Main result for the key box: none, a page of motivation.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, a page of motivation, and the
  technologies of the text (MRI, solar cells) are not a measurement with a number.
- Pen-and-paper problem: none, a page of motivation.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the one quiz, "Both gaps in the
  figure remove the states around $E=0$". It leans on "the figure", which the lint does not see. Show
  `gap_two_origins.svg` again inside the question, with no id, so that the picture gives the information. Its
  physics point stays. No new quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `gap_two_origins.svg`. The axes are $k$ and $E$ with no unit
  and no tick, the left panel runs over $-\pi/2$ to $\pi/2$ and the right one over $-\pi$ to $\pi$ with no word on
  it, and the caption lacks the parameters of the script, $t=1$, $m=0.6\,t$, $\Delta=0.6\,t$. Fix in this pass,
  together with `filling_bands.svg` of Section 1.2, since both draw the same chain with two sites per cell.
- Paragraphs: split line 7, 171 words, after the sentence on quantum computing.

## 1.2 A tour of the quantum materials we will meet

File `02-a-tour-of-the-quantum-materials-we-will-meet.md`, 1191 words, numbered equations none. A page of
motivation.

- Question of the page, and where we arrive: which materials will the tools of this session describe? We arrive
  at a list of six families, and at the remark that the first two differ only in how the bands are filled.
- Main result for the key box: none, a page of motivation.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, a page of motivation. Each family has
  its lab box in its own session.
- Pen-and-paper problem: none, a page of motivation.
- Quizzes to rewrite, and a picture question or equations as options: the two quizzes stay, they are short and
  hold no reference by number. One new picture question, "Which picture shows an n-doped semiconductor?", with
  three pictures of band filling, an insulator, an n-doped semiconductor and a metal. The feedback gives the
  position of $E_F$ in units of $t$.
- Figures to add, each with its pyqula script or the reason for numpy: the three pictures
  `g1_quiz_fill_insulator.svg`, `g1_quiz_fill_ndoped.svg`, `g1_quiz_fill_metal.svg`, with the shared code in
  `figures/session01/_g1_fill.py`. They draw from the pyqula script `scripts/session01/g1_chain_bands.py`, the bands
  of `geometry.chain()` and of `geometry.bichain()` with `add_sublattice_imbalance(0.6)`, in units of the
  hopping. Each picture has its axes $k$ and $E/t$. The chain of pyqula gives $+2\cos k$, so the metal picture is
  the mirror of the band $-2t\cos k$ of `filling_bands.svg` on the same page. The builder sets `tij=[-1.]` or says
  which sign the picture draws.
- Old figures of the page that break the plot rules: `filling_bands.svg`, axis $E$ with no unit and no tick, the
  metal over $-\pi$ to $\pi$ and the other panels over the reduced zone, and the Fermi levels $\pm(m+0.35)$ of
  the script not in the caption. Fix together with `gap_two_origins.svg`. `ssh_pair.svg`, inside a quiz, has
  ticks on $E$ with no unit and bonds $1$ and $2$ with no unit, a minor break that is left. The panel of
  `s02f04_dirac` is a Blender render and is left.

## 1.3 Emergent quasiparticles and what the lattice gives us

File `03-emergent-quasiparticles-and-what-the-lattice-gives-us.md`, 1028 words, numbered equations none. A page of
motivation.

- Question of the page, and where we arrive: the question exists, "how can a lattice of identical atoms give rise
  to so many different kinds of collective behavior?", but it is the fourth sentence. Move it first. We arrive at
  a list of quasiparticles, with the vortex drawn as a winding of the phase.
- Main result for the key box: none, a page of motivation.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: magnons carry spin through a magnetic
  insulator, which is the statement of the text "a magnetic insulator can still carry spin and heat". Source
  https://www.nature.com/articles/nphys3465, stored in `sources/session01/cornelissen2015_nphys3465.txt`, with the
  published abstract pasted from the page of the journal. The sentences are "Here we show experimentally that
  these magnons can be excited and detected fully electrically5,6,7 in a linear response, and can transport spin
  angular momentum through the magnetic insulator yttrium iron garnet (YIG) over distances as large as 40 μm." and
  "we extract the magnon spin diffusion length λ = 9.4 ± 0.6 μm in a thin 200 nm YIG film at room temperature."
  The box writes the lengths in μm, as the published text does, since the arXiv text writes "micrometer" and
  `UNIT_WORDS` of `labsource.py` has no such word. The μm sentences are in the pasted block, which the tracked file
  quotes only after a page quotes them, so the builder runs `python3 webnotes/labsource.py --quotes` once the box is
  written. Our own reading, marked as ours, is that YIG is a magnetic insulator and not a Mott insulator, so the box
  says "magnetic insulator" as the source does.
- Pen-and-paper problem: none, a page of motivation.
- Quizzes to rewrite, and a picture question or equations as options: the two quizzes stay. One new picture
  question, "Each picture shows the phase of $\Delta=|\Delta|e^{i\theta}$ as arrows. Which one holds a vortex?",
  with a uniform phase, one vortex and a smooth bend of the phase. The feedback gives the winding along the loop,
  $0$, $1$ and $0$.
- Figures to add, each with its pyqula script or the reason for numpy: `g1_quiz_phase_uniform.svg`,
  `g1_quiz_phase_vortex.svg`, `g1_quiz_phase_bend.svg`, shared code `_g1_phase.py`. numpy, since a phase field is
  not a pyqula calculation. The winding is an `assert`, as in `vortex_phase.py`.
- Old figures of the page that break the plot rules: `vortex_phase.svg` has its axes switched off, so the plane
  has no $x$ and $y$, and the caption does not give the coherence length $\xi=0.9$ of the script. A small fix,
  axes $x/\xi$ and $y/\xi$. `s08f01_magnon_spinon` and the panel of `s06f02_dimer` are Blender renders.

## 1.4 Setting up the formalism with the Schrödinger equation in two ways

File `04-setting-up-the-formalism-with-the-schrodinger-equation-in-two-ways.md`, 701 words, numbered equations
none.

- Question of the page, and where we arrive: why is the Schrödinger equation of one electron easy and the one of
  many electrons hard? We arrive at the two languages, and at the one property that separates them, which is
  whether the number of particles is fixed.
- Main result for the key box: one box with no equation, the contrast. "A wave function has a fixed number of
  coordinates, so first quantization keeps $N$ fixed. Second quantization also describes states where $N$
  fluctuates."
- Equation of another page that it starts from, for the recall box: none, it is the first page of the formalism.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, the page sets up the language and has no
  result that a material measures.
- Pen-and-paper problem: a dot with $L$ spinless levels holds $\binom{L}{N}$ states with $N$ electrons. For
  $L=4$ there are $6$ states with $N=2$, and $16$ states in total, which is $2^4$. This is the counting of Section
  1.9 in its simplest case.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz "Which of these states can
  we write as an ordinary wave function with a fixed number of coordinates?", 18 words in a sentence, to at most 15.
  Its third option, "the dot with three electrons", does not exist for the dot of `fixed_vs_free_number.svg`, which
  has two spinless levels. Replace it by "a superposition of one electron and two electrons", whose terms have one
  and two coordinates, with a mean of $1.5$ electrons. No new quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `fixed_vs_free_number.svg` is a schematic of states.
- Paragraphs: split line 3, 177 words, after "as we will see in a concrete way below". The warning on "exactly"
  stays, it states that single-particle problems are exactly solvable.

## 1.5 A warm-up in first quantization, and the puzzle that breaks it and 1.6 Building second quantization with creation and annihilation operators and 1.7 Enforcing fermionic statistics

File `05-a-warm-up-in-first-quantization-and-the-puzzle-that-breaks-it.md`, 1257 words, numbered equations (1.1),
(1.2), (1.3).

- Question of the page, and where we arrive: can a wave function describe a dot in a superposition of zero and two
  electrons? It cannot, so we build creation and annihilation operators, and we arrive at the anticommutation
  relations (1.3), which hold the Pauli principle.
- Main result for the key box: (1.3), with the sentence that $i=j$ gives $(c_i^\dagger)^2=0$, so a level holds
  zero or one fermion, and the antisymmetry of the wave function comes with it.
- Equation of another page that it starts from, for the recall box: none, (1.1) to (1.3) are the first equations
  of the session.
- Derivation told in words, for a steps fold: "From the anticommutation relations (1.3) to the Pauli principle".
  $\{c_i^\dagger,c_i^\dagger\}=0$ gives $(c_i^\dagger)^2=0$, and $n_i=c_i^\dagger c_i$ gives $n_i^2=n_i$, so the
  occupation is $0$ or $1$. Then the two-site Fock states of [](#sch:s01:dimer_fock) with their energies, $0$, $\pm
  t$ and $0$.
- Lab box, with the source and the number that the source states: none. The natural source is the single-Cooper-pair
  box, with two charge states that differ by $2e$ in a coherent superposition, https://arxiv.org/abs/cond-mat/9904003.
  Its abstract and the abstract of the published article state no measured number with a unit, so the rule leaves
  it out. It was not stored.
- Pen-and-paper problem: for two sites, compute $\langle N\rangle$ and $(\Delta N)^2$ in the state
  $(|0\rangle+c_0^\dagger c_1^\dagger|0\rangle)/\sqrt2$, with $N=c_0^\dagger c_0+c_1^\dagger c_1$. The answer is
  $\langle N\rangle=1$ and $(\Delta N)^2=1$, so the number fluctuates by one electron around its mean, which is the
  puzzle of Section 1.5 written with operators.
- Quizzes to rewrite, and a picture question or equations as options: rewrite "What is its energy for the hopping
  of (1.2)?" with $H_\text{hop}$ written in the question. The boson quiz stays. One new quiz with equations as
  options, "Which identity follows from (1.3)?", with $(c_i^\dagger)^2=0$ (true), $c_ic_i^\dagger=1$ (false, it is
  $1-c_i^\dagger c_i$, which is $0$ on an occupied site) and $c_i^\dagger c_j=c_jc_i^\dagger$ for $i\neq j$ (false,
  the sign is minus). The relations are written in the question.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `dimer_fock.svg` and `boson_fermion_pair.svg` are level
  diagrams with no energy axis, where each level carries its value. A minor break, an arrow $E/t$ would fix it.
  Both stay numpy, since they are exact diagonalizations in the Fock space with the fermionic and the bosonic
  algebra, which pyqula does not do.
- Paragraphs: split line 5, 159 words, before "This example is not artificial". The tryit and the notebook box
  stay.

## 1.8 First versus second quantization for the same problem and 1.9 Where the two formalisms differ and the exponential growth of the many-body problem and 1.10 A first look at eigenstates in finite tight-binding islands

File `08-first-versus-second-quantization-for-the-same-problem.md`, 1467 words, numbered equations none.

- Question of the page, and where we arrive: when does second quantization cost more than first quantization? For
  a single-particle Hamiltonian never, and with interactions the Fock space grows as $2^L$. We end with the levels
  of a finite island, which STM can map.
- Main result for the key box: the counting, with no number. "For $L$ sites the single-particle problem is an
  $L\times L$ matrix, and the many-body problem is a $2^L\times 2^L$ matrix for spinless fermions, $4^L\times4^L$
  for spinful ones."
- Equation of another page that it starts from, for the recall box: (1.2), the two-site hopping, since
  $\sum_{ij}t_{ij}c_i^\dagger c_j$ is its sum over all pairs.
- Derivation told in words, for a steps fold: "Counting the Fock space of L sites". Each site is empty or
  occupied, $\sum_N\binom{L}{N}=2^L$, and for $L=3$ this is $1+3+3+1=8$, as in Figure 1.1.
- Lab box, with the source and the number that the source states: STM maps the confined states of graphene islands,
  which is the comparison of Section 1.10. Source https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.107.236803,
  stored in `sources/session01/hamalainen2011_physrevlett.107.236803.txt` (arXiv 1110.4208). The sentences are "We
  measure the atomic structure and local density of states (LDOS) of individual GQDs as a function of their size
  and shape in the range from a couple of nanometers up to ca. 20 nm." and "The observed states are analogous to
  the solutions of the text book "particle-in-a-box" problem applied to relativistic massless fermions." The dots
  are graphene on Ir(111) with zigzag edges, measured with STM and STS.
- Pen-and-paper problem: how much memory does one state of $20$ spinful sites take, with $8$ bytes per real
  coefficient? $4^{20}\approx1.1\times10^{12}$ coefficients, which is $8.8$ TB. With $N=20$ and $S_z=0$ fixed it is
  $\binom{20}{10}^2\approx3.4\times10^{10}$, which is $273$ GB, still out of reach. For $20$ spinless sites
  $2^{20}$ coefficients take $8.4$ MB.
- Quizzes to rewrite, and a picture question or equations as options: the two quizzes stay, they are short and
  their numbers are `assert` lines of `levels_vs_size.py` ($0.57t$, $0.062t$). One new picture question, "Each map
  shows the density of one level of a honeycomb island. Which one is the lowest level?", with the lowest, the
  second and the sixth level. The feedback says that the lowest level has no node, by the theorem of
  Perron-Frobenius, and gives its energy. This holds for the hopping $-t$ of the caption. With the $+1$ of pyqula
  the lowest state changes sign on every bond and has the same density, so the feedback speaks of the density or
  the script uses $-t$.
- Figures to add, each with its pyqula script or the reason for numpy: `g2_quiz_island_lowest.svg`,
  `g2_quiz_island_second.svg`, `g2_quiz_island_sixth.svg`, shared code `_g2_island.py`. They use the pyqula island
  `islands.get_geometry(name="honeycomb", ..., nedges=6)` through a script `scripts/session01/g2_honeycomb_island.py`
  if it gives the island of 96 sites with zigzag edges of `island_states.py`. If it does not, they stay numpy and
  reuse the construction of `island_states.py`, and the builder says why. Each map has $x$ and $y$ in units of the
  bond length.
- Old figures of the page that break the plot rules: `island_states.svg` has real-space maps with the axes off,
  with no $x$ and $y$, and no scale for the area of a disc. Fix with the quiz pictures, from the same code.
  `levels_vs_size.svg` is fine. `s01f01_fockspace` is a Blender render.
- The widget, the two notebook boxes and the tryit stay. The warning on "exactly" in the widget stays, it is a
  statement about the box wavefunction.

## 1.11a Spontaneous symmetry breaking and why a symmetric Hamiltonian can have an asymmetric ground state

File `11-spontaneous-symmetry-breaking-and-why-a-symmetric-hamiltonian-can-have-an-asymmetric-ground-state.md`,
959 words, numbered equations none.

- Question of the page, and where we arrive: why do the symmetries of the Hamiltonian so often not survive in the
  ground state? The question is the fifth sentence today, move it first. We arrive at the answer that a finite
  system tunnels between the two asymmetric states, with a splitting that goes to zero only in the thermodynamic
  limit.
- Main result for the key box: no numbered equation. "The minima of a symmetric energy are not symmetric. In a
  finite system the splitting $\Delta$ between the even and the odd combination is finite, so the ground state is
  symmetric. For the Ising chain $\Delta$ falls roughly as $(g/J)^L$, so it vanishes only when $L\to\infty$."
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: "Why the splitting falls as (g/J)^L". To go from all spins up to
  all spins down the transverse field flips $L$ spins, each step gives a factor $g$ and costs an energy of order
  $J$, so the lowest order of perturbation theory that joins the two states is the order $L$. This gives roughly
  $J(g/J)^L$, up to a prefactor. The number that checks it is the slope of `ising_splitting.py`, within $0.15$ of
  $\log(g/J)$, and the splitting for $g=0.3J$ falls by about $11$ for every two sites added, from $1.33\times10^{-3}J$
  at $L=6$ to $1.19\times10^{-4}J$ at $L=8$.
- Lab box, with the source and the number that the source states: none. The two natural sources state no number
  with a unit in their abstracts. The Néel states of a few Fe atoms on a surface switch by quantum tunneling of the
  magnetization for the smallest structures (Science 335, 196, read on PubMed), and the transverse-field Ising chain
  is realized in CoNb2O6 (arXiv 1103.3694) with no field value in the abstract. Neither was stored.
- Pen-and-paper problem: the two minima with a bias $h$ that breaks the symmetry, $H=\begin{pmatrix}-h&-\Delta\\
  -\Delta&h\end{pmatrix}$. Show that the weight of the ground state in the first minimum is
  $\tfrac12\big(1+h/\sqrt{h^2+\Delta^2}\big)$. It is $0.85$ for $h=\Delta$ and $0.998$ for $h=10\Delta$, so in a
  large system, where $\Delta$ is tiny, any small field chooses one minimum.
- Quizzes to rewrite, and a picture question or equations as options: the quiz stays. `tunnel_split.py` prints
  $2\Delta=0.92$ of its feedback without an `assert`, so the builder adds one. One new quiz with equations as
  options, "How does the splitting of the open Ising chain depend on its length $L$, for $g\ll J$?", with
  $\Delta\propto(g/J)^L$ (true), $\Delta\propto1/L$ (false, from $L=6$ to $L=8$ the splitting falls by a factor
  $11$ for $g=0.3J$, not by $4/3$), and $\Delta\propto g$ with no $L$ (false, same numbers).
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `tunnel_split.svg` has no name on the $x$ axis, no tick, and
  an axis $E$ with no number, while the quiz quotes $2\Delta=0.92$. Fix the axes and add the `assert`.
  `ising_splitting.svg` is fine and stays numpy, since it is an exact diagonalization of a spin chain, which
  pyqula does not do. `s01f02_ssb` is a Blender render.
- Paragraphs: split line 7, 182 words, before "The requirement of the thermodynamic limit is essential".

## 1.11b Classifying states of matter by the symmetry that they break

File `11b-classifying-states-of-matter-by-the-symmetry-they-break.md`, 1232 words, numbered equations (1.4).

- Question of the page, and where we arrive: which symmetry does a magnet, a ferroelectric or a superconductor
  break? We arrive at a classification with its quasiparticles, at the probes of broken time reversal, and at the
  definition (1.4) of a magnet.
- Main result for the key box: (1.4), with one sentence, a magnet is a state that time reversal changes. See the
  open point on (1.4) at the end, the box keeps the equation as printed.
- Equation of another page that it starts from, for the recall box: none, the page continues Section 1.11a,
  which has no equation.
- Derivation told in words, for a steps fold: none, the page gives definitions and a table, and the problem
  carries the one calculation.
- Lab box, with the source and the number that the source states: the Kerr effect of the text detects broken time
  reversal in a monolayer magnet. Source https://www.nature.com/articles/nature22391, already stored by Session 6 in
  `sources/session06/huang2017_nature22391.txt` (arXiv 1703.05892), so the two sessions link the same article. The
  sentences are "Here, we use magneto-optical Kerr effect (MOKE) microscopy to demonstrate that monolayer chromium
  triiodide (CrI3) is an Ising ferromagnet with out-of-plane spin orientation." and "Its Curie temperature of 45 K
  is only slightly lower than the 61 K of the bulk crystal, consistent with a weak interlayer coupling." Our
  reading, marked as ours, is that the Kerr signal of the ferromagnet below $45$ K is the test of the quiz on the
  Kerr rotation. The abstract does not state the size of the rotation, so the box gives none.
- Pen-and-paper problem: with $\hat T=i\sigma_yK$ on each spin, show that the singlet
  $(|{\uparrow\downarrow}\rangle-|{\downarrow\uparrow}\rangle)/\sqrt2$ passes the test (1.4), and that the Néel
  state does not, $\hat T|{\uparrow\downarrow}\rangle=-|{\downarrow\uparrow}\rangle$, which is another state. This
  is the exact ground state of the dimer against the mean-field state of Section 1.12.
- Quizzes to rewrite, and a picture question or equations as options: the two quizzes stay. One new picture
  question, "Which dispersion is a magnon with an easy-axis anisotropy?", with $\omega=1-\cos k$, $\omega=1-\cos
  k+0.45$ (true) and the phonon $\omega=2|\sin(k/2)|$. The feedback reads the value at $k=0$.
- Figures to add, each with its pyqula script or the reason for numpy: `g3_quiz_disp_magnon.svg`,
  `g3_quiz_disp_magnon_gap.svg`, `g3_quiz_disp_phonon.svg`, shared code `_g3_disp.py`. numpy, since they are the
  closed forms of `gapless_gapped.py` and no pyqula calculation. Axes $k$ and $\omega$ with ticks at $0$ and
  $0.45$.
- Old figures of the page that break the plot rules: `gapless_gapped.svg` has no tick, and the gap $0.45$ of the
  caption has no number on the axis. A small fix. The panel of `s06f05_magnon` is a Blender render.

## 1.12 The general interacting Hamiltonian, and the tool we will use on it

File `12-the-general-interacting-hamiltonian-and-the-tool-we-will-use-on-it.md`, 917 words, numbered equations
(1.5).

- Question of the page, and where we arrive: which Hamiltonian do we want to solve, and with which tool? We arrive
  at (1.5), and at mean-field theory as a variational method that can give a ground state with less symmetry than
  the Hamiltonian.
- Main result for the key box: (1.5), with the sentence that the quartic term makes it many-body, and that mean
  field replaces it by a bilinear term with expectation values that are solved self-consistently.
- Equation of another page that it starts from, for the recall box: (1.2), the two-site hopping, of which the
  first term of (1.5) is the sum over all pairs.
- Derivation told in words, for a steps fold: "From the quartic term of (1.5) to a bilinear Hamiltonian". We
  write a product of two bilinears as $AB=\langle A\rangle B+A\langle B\rangle-\langle A\rangle\langle B\rangle$ plus
  $(A-\langle A\rangle)(B-\langle B\rangle)$, and drop the last term, the fluctuations. The simplest case first,
  the Hubbard term $Un_\uparrow n_\downarrow$, then the three choices of $A$ and $B$ that give the three channels of
  Figure 1.3. Unnumbered displays only.
- Lab box, with the source and the number that the source states: none, the page sets up the method, and the lab
  boxes come with the examples of Sections 1.13 and 1.14.
- Pen-and-paper problem: the Hubbard dimer with two electrons and $S_z=0$, four states. Show that the exact
  ground-state energy is $U/2-\sqrt{U^2/4+4t^2}$. At $U=4t$ it is $-0.83\,t$, and at large $U$ it goes as $-4t^2/U$.
  This is the exact curve of [](#sch:s01:dimer_meanfield), and `dimer_meanfield.py` asserts the closed form.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz "The quartic term of (1.5)
  has four operators ...". Its question sends the reader to (1.5), so the question writes the quartic term as a
  display. The feedback of its third option ends "while the loop of the figure ends with charges that differ from
  site to site", which is a figure of Section 1.13, so it gets the numbers instead. Its physics point stays.
  One new quiz with equations as options, "Which bilinear replaces $Un_\uparrow n_\downarrow$ in mean field?", with
  $U(\langle n_\uparrow\rangle n_\downarrow+n_\uparrow\langle n_\downarrow\rangle-\langle n_\uparrow\rangle\langle
  n_\downarrow\rangle)$ (true), the same without the constant (false, it counts the interaction energy twice, at
  $U=4t$ the AF dimer is off by $U\sum_i\langle n_{i\uparrow}\rangle\langle n_{i\downarrow}\rangle=0.5\,t$), and
  $U\langle n_\uparrow\rangle\langle n_\downarrow\rangle$ (false, a number with no operator, so the spectrum is the
  one of $U=0$). The builder checks the $0.5\,t$ with a number.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none. `dimer_meanfield.svg` has its axes, ticks and names. It
  stays numpy, since the exact curve is a diagonalization in the Fock space. Note that its mean-field energy is
  $-2t^2/U$ for every $U>2t$, and not only at large $U$, which the caption may say. `s01f03_threechannels` is a
  Blender render.

## 1.13 Worked example 1, the charge density wave

File `13-worked-example-1-the-charge-density-wave.md`, 1215 words, numbered equations (1.6).

- Question of the page, and where we arrive: can a chain with the same Hamiltonian at every site end with its
  charge on every second site? We arrive at the charge density wave of (1.6) in mean field, with a charge
  imbalance and a gap that grow with $V$.
- Main result for the key box: (1.6), with the sentence that in mean field the repulsion becomes an onsite energy
  $V(\langle n_{n-1}\rangle+\langle n_{n+1}\rangle)$, which can differ from site to site, so the solution can break
  the translational symmetry of (1.6).
- Equation of another page that it starts from, for the recall box: (1.5), since (1.6) is its case with a
  first-neighbor $V$.
- Derivation told in words, for a steps fold: "From the repulsion of (1.6) to a staggered onsite energy". Hartree
  decoupling of $Vn_nn_{n+1}$, then the guess $\langle n\rangle=(1\pm\delta)/2$ on even and odd sites, which gives
  onsite energies $V(1\mp\delta)$, a staggered potential $\pm V\delta$ and a gap $2V\delta$. Only the Hartree term,
  as the text says. Unnumbered displays.
- Lab box, with the source and the number that the source states: a CDW and its gap in one layer of NbSe2. Source
  https://www.nature.com/articles/nphys3527, stored in `sources/session01/ugeda2016_nphys3527.txt` (arXiv
  1506.08460). The sentences are "We demonstrate that 3x3 CDW order in NbSe2 remains intact in 2D." and "Our STS
  measurements at 5 K reveal a CDW gap of Δ = 4 meV at the Fermi energy, which is accessible via STS due to the
  removal of bands crossing the Fermi level for a single layer." and "In bulk NbSe2 a CDW sets in at TCDW = 33 K".
  The source also says that the mechanisms "remain controversial". So the box does not tie this gap to the repulsion
  $V$ of (1.6). Our reading, marked as ours, is that the order has a period of three lattice constants and the model
  of the page a period of two, and both open a gap at the Fermi energy.
- Pen-and-paper problem: one pass of the loop of Figure 1.4 by hand, the periodic ring of four sites with $V=3t$,
  from the charges $0.6$ and $0.4$. The onsite energies are $2.4\,t$ and $3.6\,t$, the two lowest levels are
  $0.91\,t$ and $2.4\,t$, and the new charges are $0.82$ and $0.18$, as in the caption of Figure 1.4. The check
  script of the page asserts them, since the figure is a Blender render with no script.
- Quizzes to rewrite, and a picture question or equations as options: rewrite "In the figure the guessed charges
  are $0.6$ and $0.4$ ...", 17 words in a sentence and a reference to "the figure". The question states the ring of
  four sites, $V=3t$ and the two sets of charges, with no figure. The quiz on the number of degenerate states stays.
  One new picture question, "Each picture shows the mean-field charges $\langle n_i\rangle$ of the chain (1.6) at
  half filling. Which one is at $V=3t$?", with three bar plots for three values of $V$. The feedback gives the
  imbalance of each.
- Figures to add, each with its pyqula script or the reason for numpy: `g4_cdw_meanfield.svg`, the charge imbalance
  and the gap against $V$, which the text describes in words ("When $V$ grows, a gap opens ..."), with axes
  $V/t$, imbalance and gap$/t$. It draws from the pyqula script `scripts/session01/g4_cdw_chain.py`, the calls of
  the notebook cells "Symmetry breaking in the spinless fermionic chain" and "Gap opening in a spinless interacting
  model", `geometry.bichain()`, `has_spin=False`, `get_mean_field_hamiltonian(V1=V, mf="CDW", filling=0.5)`,
  `get_vev()` and `get_gap()`. The three quiz pictures `g4_quiz_cdw_*.svg` draw from the same script, with axes
  site and $\langle n_i\rangle$. Whether the gap is $2V\delta$ depends on the Fock term, see the conventions sheet.
- Old figures of the page that break the plot rules: none of the page are web plots. `s01f05_selfconsistency` and
  `s01f04_cdw` are Blender renders. `cdw_patterns.svg`, in a quiz, is a schematic.

## 1.14 Worked example 2, magnetism and 1.15 Worked example 3, superconductivity and broken gauge symmetry

File `14-worked-example-2-magnetism.md`, 1433 words, numbered equations (1.7), (1.8), (1.9), (1.10). The page has
two results, so it gets two key boxes.

- Question of the page, and where we arrive: what changes when the electrons have spin and the interaction is
  onsite? For $U>0$ we arrive at a magnet with a moment $m$ and a gap $Um$, and for $U<0$ at a pairing term that
  breaks gauge symmetry.
- Main result for the key box: first box, (1.7) and (1.8), with the sentence that the antiferromagnetic mean field
  gives a staggered moment $m$ and a gap $Um$, which approaches $U$ at large $U$. Second box, (1.9) and (1.10), with
  the sentence that $\Delta$ turns by $e^{2i\varphi}$, so a state with $\Delta\neq0$ has no fixed number of
  electrons, only a fixed parity.
- Equation of another page that it starts from, for the recall box: `eq="1.4 1.6"`. The page uses (1.4) to say
  which symmetry is broken, and its decoupling is "done in the same way as before", which is the one of (1.6).
  Section 1.15 cannot recall (1.7), which is on the same file.
- Derivation told in words, for a steps fold: "From the Hubbard term of (1.7) to the gap Um". The decoupling of
  $n_\uparrow n_\downarrow$, the guess $\langle n_{\uparrow}\rangle=(1\pm m)/2$ on the two sublattices, an onsite
  energy $\mp Um/2$ for spin up, the opposite for spin down, and a gap $Um$. Unnumbered displays. No fold for Section
  1.15, its argument is three lines.
- Lab box, with the source and the number that the source states: the Hubbard model (1.7) with $U>0$, realized with
  fermionic atoms in an optical lattice. Source https://www.nature.com/articles/nature22362, stored in
  `sources/session01/mazurenko2017_nature22362.txt` (arXiv 1612.08436). The sentences are "Here we report the
  realization of an antiferromagnet in a repulsively interacting Fermi gas on a 2D square lattice of approximately 80
  sites." and "At our lowest temperature of T/t = 0.25(2) we find strong order across the entire sample." and "In
  this regime we find that the antiferromagnetic LRO persists to hole dopings of about 15%, providing a guideline for
  computational methods." The probe is site-resolved imaging with a quantum gas microscope. This is a quantum
  simulator and not one material, and the lattice is square and not the chain of the page, so the lecturer may
  strike it. No source with a number was found for Section 1.15, see the parity sources at the end.
- Pen-and-paper problem: the antiferromagnetic mean field of the Hubbard dimer. Show that self-consistency gives
  $m=\sqrt{1-(2t/U)^2}$ for $U>2t$ and $m=0$ below, so the moment appears at $U=2t$, as the tryit says. At $U=4t$
  this is $m=0.87$, with the mean-field energy $-0.50\,t$ against the exact $-0.83\,t$, and the mean-field energy is
  $-2t^2/U$ for every $U>2t$. Computed by iterating the loop of `dimer_meanfield.py`.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz on $U<0$. Its question uses
  $U$ and $m$ with no equation, so it writes the onsite term $Un_\uparrow n_\downarrow$ and the definition (1.8) of
  $m$ as displays. The feedback of its second option says "The Hamiltonian (1.7) is real for both signs of $U$, so
  it is invariant under time reversal". For spinful electrons a real Hamiltonian is invariant under $K$, not under
  $\hat T=i\sigma_yK$. The conclusion stays, and the reason becomes that (1.7) does not change when we exchange up
  and down and take the complex conjugate. Rewrite the gauge quiz with $c\to c\,e^{i\varphi}$ written in the
  question, its options and feedback stay. Two new quizzes. One with equations as options, "What is the
  antiferromagnetic mean-field gap of the chain at half filling?", with $Um$ (true), $U$ (false, at $U=3t$ the gap
  is $1.86\,t$ with $m=0.62$) and $2t$ (false, at $U=t$ the gap is $0.03\,t$), numbers of `afm_gap.py`. One picture
  question, "Which picture shows $\Delta$ after a gauge transformation with $\varphi=\pi/4$?", with $\Delta$ turned
  by $\pi/2$ (true), by $\pi/4$, and not turned.
- Figures to add, each with its pyqula script or the reason for numpy: `afm_gap.svg` draws from a new pyqula script
  `scripts/session01/g4_hubbard_chain.py`, the calls of the notebook cell "Gap opening of the Hubbard model in a
  chain", `geometry.bichain()`, `get_mean_field_hamiltonian(U=U, mf="antiferro")`, `get_gap()` and
  `get_vev("mz")`, so that the plot gets its download button. The numpy self-consistency of `afm_gap.py` stays as an
  `assert` against it. The convention of `U` and of `mz` comes from the sheet. The three gauge pictures
  `g4_quiz_gauge_*.svg`, shared code `_g4_gauge.py`, are numpy, a turn in the complex plane, with the axes Re and
  Im.
- Old figures of the page that break the plot rules: `afm_gap.svg` has named axes and no tick, while the caption
  quotes the limits $1$ and $U$ and the check at $U=3t$. Add ticks at $0,2,4,6,8$ and $0,0.5,1$. `gauge_phase.svg`
  draws the complex plane with no names Re and Im. A small fix. The panel of `s06f02_dimer` is a Blender render.

## 1.16 Closing summary

File `16-closing-summary.md`, 670 words, numbered equations none.

- Question of the page, and where we arrive: none, the closing summary is not checked for an opener. It keeps its
  first sentence.
- Main result for the key box: none, a closing page.
- Equation of another page that it starts from, for the recall box: none, the list links the equations of every
  page.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- What the student can now do, a new list after the summary, one line per task with the section that teaches it.
  Say why a state with a fluctuating number of electrons needs second quantization (1.4, 1.5). Write a hopping with
  creation and annihilation operators and find the levels of the two-site problem (1.6). Show $(c^\dagger)^2=0$ from
  (1.3) and count the two-particle states of fermions and of bosons (1.7). Count the Fock space, $2^L$ or $4^L$, and
  say why exact diagonalization stops near $L\approx20$ (1.9). Relate the levels of a finite island to an STM map,
  and say how the spacing shrinks with the size (1.10). Explain why the splitting of a finite system vanishes only
  in the thermodynamic limit (1.11a). Say which symmetry a magnet, a ferroelectric and a superconductor break, and
  apply the test (1.4) to a state of two spins (1.11b). Decouple a quartic term and run one pass of the loop by hand
  (1.12, 1.13). Solve the antiferromagnetic mean field of the Hubbard dimer, with the moment from $U=2t$ (1.14).
  Show that a pairing term changes by $e^{2i\varphi}$ under a gauge transformation (1.15).
- Quizzes to rewrite, and a picture question or equations as options: the quiz stays, it is short and correct.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `s01f03_threechannels` is a Blender render.

## Candidates for the lab boxes

The notebook of the session has no "In the lab" cell and no link. The sources below were fetched on 2026-11-21
with `labsource.py --session 1`, and each planned sentence was found by a grep of its stored full text.

| page | source as linked | stored file | number of the box |
|---|---|---|---|
| 1.3 | https://www.nature.com/articles/nphys3465 | `session01/cornelissen2015_nphys3465.txt` | 40 μm, 9.4 ± 0.6 μm, 200 nm |
| 1.10 | https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.107.236803 | `session01/hamalainen2011_physrevlett.107.236803.txt` | 20 nm |
| 1.11b | https://www.nature.com/articles/nature22391 | `session06/huang2017_nature22391.txt`, stored by Session 6 | 45 K, 61 K |
| 1.13 | https://www.nature.com/articles/nphys3527 | `session01/ugeda2016_nphys3527.txt` | 4 meV, 5 K, 33 K |
| 1.14 | https://www.nature.com/articles/nature22362 | `session01/mazurenko2017_nature22362.txt` | T/t = 0.25(2), 15% |

Read and left out, since the abstract states no number with a unit. The single-Cooper-pair box (arXiv
cond-mat/9904003), CoNb2O6 near its critical field (arXiv 1103.3694 and the Science abstract on PubMed), the
Néel states of a few Fe atoms (Science 335, 196, on PubMed), Fe8 molecular magnets (Science 284, 133, on PubMed),
KCuF3 (arXiv cond-mat/0501069, 1307.4071), the $2e$ period of a Cooper-pair transistor (arXiv cond-mat/0308253) and
triangulene dimers (arXiv 2003.00753). The spinon weight of arXiv 1306.4678, "99(8)%", has a number but no
material named in the abstract. The old PRL papers on Mn12 tunneling, on the vortex lattice seen by STM and on
aluminum grains have no abstract on Crossref or PubMed. None of these was stored.

## Builder groups

The groups follow the order of the pages, with at most three section pages each.

- `g1`, `01`, `02`, `03`. The pages of motivation. `index.md` needs no edit, and if one turns up it goes to `g1`. `01` and `02` share the
  chain with two sites per cell, $m=0.6\,t$, in `gap_two_origins.py`, `filling_bands.py` and the new quiz of `02`.
- `g2`, `04`, `05`, `08`. Second quantization. `04` and `05` share the dot with zero and two electrons, `05` and
  `08` the hopping (1.2) and the counting of the Fock space.
- `g3`, `11`, `11b`. Symmetry breaking, the Ising chain and time reversal.
- `g4`, `12`, `13`, `14`. Mean field. The three pages share the loop, the Hubbard dimer (`dimer_meanfield.py` and
  the two problems), the decoupling and the pyqula mean-field calls, which need the conventions sheet first.
- `g5`, `16`. The closing list, which links every other page. It is small, and it can go to the builder of `g3` as
  a second task once `g3` is done, or to a builder that starts after the others, so that the list matches the pages.

## Old SVGs that the plan changes on purpose

The gate of step 5 asks that no old SVG changes. These are the ones that the plan redraws on purpose, so that the
coordinator can tell them from an accidental redraw. Any other old SVG that changes is an accident.

- `figures/session01/gap_two_origins.svg` and `filling_bands.svg`, group `g1`, units, ticks and the zone.
- `figures/session01/vortex_phase.svg`, group `g1`, the axes $x/\xi$ and $y/\xi$.
- `figures/session01/island_states.svg`, group `g2`, the axes $x$ and $y$.
- `figures/session01/tunnel_split.svg` and `gapless_gapped.svg`, group `g3`, axes and ticks.
- `figures/session01/afm_gap.svg` and `gauge_phase.svg`, group `g4`, ticks, the pyqula script, and Re and Im.

`dimer_fock.svg`, `boson_fermion_pair.svg` and `ssh_pair.svg` have minor breaks and are left.

## Open for the lecturer

These touch a numbered equation, a statement of the old text or a convention. A builder leaves them as they are.

1. The sign of the hopping. (1.2) writes $+t$, and so do `dimer_fock.py`, `boson_fermion_pair.py` and the caption of
   the dimer, where $-t$ is the antisymmetric combination. (1.6), (1.7), `island_states.py`, `levels_vs_size.py`
   and `dimer_meanfield.py` write $-t$. pyqula uses $+1$. On the bipartite lattices of the session the set of levels
   and the densities do not depend on the sign, but the band against $k$ does, pyqula gives $+2\cos k$ for the chain
   where Section 1.2 draws $-2t\cos k$, and so does the sign pattern of the lowest state of an island. A reader sees
   two conventions. Keep both with one sentence, or move (1.2) to $-t$, which changes a numbered equation and the
   labels of the two combinations. In both cases the new pyqula scripts say which sign they use.
2. The definition of a magnet (1.4), $\hat T|\Psi\rangle=|\Psi\rangle$. A state is invariant only up to a phase, and
   for an odd number of electrons $\hat T^2=-1$, so $\hat T|\Psi\rangle$ is orthogonal to $|\Psi\rangle$ and no state
   passes the test, also with no magnetism (Kramers). A number confirms $\hat T^2=-1$ for one spin with
   $\hat T=i\sigma_yK$, and that the singlet of two spins passes. A sentence next to (1.4) or a new form of it is the
   lecturer's.
3. The pairing amplitude (1.9), $\Delta=\langle c_ic_j\rangle$, has no spin, while Section 1.15 decouples the onsite
   term of (1.7), where it is $\langle c_{i\downarrow}c_{i\uparrow}\rangle$. For one spin species $c_ic_i=0$. Adding
   the spin changes a numbered equation.
4. The table of Section 1.11b pairs the broken gauge symmetry with the Higgs mode, while the other two rows give the
   Goldstone mode. The amplitude mode is gapped, and the phase mode of a neutral superfluid is gapless, while in a
   charged superconductor it moves up to the plasma frequency. The sentence "only the phonon is gapless in every
   material" holds for acoustic phonons. These are statements of the old text.
5. The mean-field decoupling is told in words on pages `12` to `14`. The plan puts it in unnumbered displays inside
   the steps folds, and the key boxes keep (1.5), (1.6) and (1.7). Giving it its own number, such as (1.6a), is the
   lecturer's.
6. Section 1.3 says that flux quantization and the Josephson effect are the basis of "some of our most precise
   measurements of the ratio between Planck's constant and the electron charge". Since 2019 both constants are
   exact in the SI, and the Josephson effect realizes the volt. A statement of the old text.
7. The lab box of Section 1.14 is a gas of atoms on a square lattice, not one material and not the chain of the
   page. Keep it, or leave Section 1.14 without a lab box.
8. Section 1.11b and Session 6 would link the same CrI3 article. Keep it in both, or give Session 1 another source.
