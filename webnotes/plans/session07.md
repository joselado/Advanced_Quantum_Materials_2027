# Plan of Session 7 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session07.md`.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 554 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0) | 0 |
| `01-two-regimes-of-many-body-physics.md` | 7.1, 7.2a | 958 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1, quiz-long 1 |
| `02b-the-jordan-wigner-transformation.md` | 7.2b | 1105 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1, quiz-long 2 |
| `03-storing-the-wave-function-as-the-main-bottleneck.md` | 7.3 | 1146 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `04-the-matrix-product-state-ansatz.md` | 7.4, 7.5 | 1409 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1 |
| `06-entanglement-entropy-of-a-solvable-dimerized-chain.md` | 7.6 | 1115 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | key 1, opener 1 |
| `07-two-dimensions-and-the-area-law.md` | 7.7 | 1285 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `08-why-mps-work-in-1d-and-where-they-stop-working.md` | 7.8a | 1278 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `08b-where-mps-stop-working.md` | 7.8b | 981 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | long-paragraph 1, opener 1, quiz-long 2 |
| `09-tensor-diagrams-as-notation-for-networks-and-operators.md` | 7.9 | 932 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `10-the-variational-principle-and-dmrg-for-the-ground-state.md` | 7.10 | 1181 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1, quiz-long 2 |
| `11-mera-and-peps-beyond-mps.md` | 7.11 | 1310 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1, quiz-long 1 |
| `12-closing-summary.md` | 7.12 | 719 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | 0 |

## What holds for every page

The numbers of this plan were computed in one scratch script, and each builder computes them again in the check
script of its page. The sheet `conventions/session07.md` did not exist when this plan was written, so this plan
states no sign of its own. The signs that matter in this session are few. The Jordan-Wigner string is
$K_i=\exp(i\pi\sum_{j<i}n_j)$ with $K_1=1$, as printed in (7.2), and an entropy does not depend on the sign of a
hopping. Entropies are in nats, and a page that draws $S/\log 2$ says so on the axis.

pyqula covers only free fermions in this session. It gives the entanglement entropy of a block of a chain of free
fermions with `hf.get_entanglement_entropy(region=list_of_sites)` on an open chain made with
`h.set_finite_system(n=N)`. With `geometry.chain()` and $N=802$ this gave $S=1.491$ for a block of 10 sites in the
middle, against $1.49$ of the caption of `critical_entropy.svg`, and the dimerized `geometry.bichain()` with
`h.inter = 0.6*h.inter` gave $0.498$ for 10 sites and $0.499$ for 100, against "about $0.5$". Each call
diagonalizes the whole chain, about 9 s for $N=3002$ and a block of 1000 sites, and it wrote no file. Everything
with spins, meaning the exact diagonalizations, the quench, the variational sweeps and the Schmidt weights, is a
many-body calculation that pyqula cannot do, so it stays in numpy with no button. Whether a `dmrgpy` script can be
a download is open, see the last section.

An old figure is not overwritten. A figure that this plan marks as replaced gets a new script and a new SVG with
the prefix of its group, such as `g2_memory_scaling.py`. The image line of the page points to the new SVG and
keeps its id, and the old script and SVG stay as they are. Every replaced SVG below is used on one page only, which
was checked with grep over `webnotes/pages/`. Every use of a replaced SVG on that page points to the new file,
also inside the feedback of a quiz, which is the case for `quench_entropy.svg` in Section 7.8b,
`dmrg_sweeps.svg` in Section 7.10 and `critical_entropy.svg` in Section 7.11. A replaced figure gets its caption read again against the new
picture, and every number of the caption becomes an `assert` of the new script. The quizzes that the lint does not
flag but that are not read alone are listed in the blocks too. They are the words "in the figure" of 7.2b, "as the
figure shows" of 7.2a, "the same state" and "the previous question" of 7.6, and the questions of 7.7 and 7.10
whose sentence stops before its end.

## Index page

File `index.md`, 554 words.

- Question of the page, and where we arrive: none, the index keeps the shape of the ten index pages (from before,
  what we will see, where it comes back).
- Main result for the key box: none, the index is the introduction of the session.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, the index has no quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `concept_map.svg` is a schematic.

The third paragraph ("In this session we will build a tool ...") has 161 words, which the lint does not read on an
index page. The index of Session 3 kept its paragraph of 163 words, and the plan of Session 4 left its index out
of the groups, so this index is not edited and stays out of the builder groups.

## 7.1 Two regimes of many-body physics and 7.2a Fermions and spins, two languages for the same physics

File `01-two-regimes-of-many-body-physics.md`, 958 words, numbered equations (7.1). A page of motivation.

- Question of the page, and where we arrive: why does mean field, which worked from Session 1 to Session 6, tell
  us nothing about a quantum spin liquid? There the interaction term of (7.1) has no symmetry-broken solution, so
  we need a tool that does not assume one. The second section asks if fermions and spins are two kinds of physics,
  and the answer is that they are two languages.
- Main result for the key box: (7.1), with two sentences. When the quartic term can be replaced by a bilinear one
  with an order parameter, the matter is weakly correlated. When no decoupling gives the ground state, it is
  strongly correlated. The lint asks for this box, since (7.1) is numbered.
- Equation of another page that it starts from, for the recall box: (1.5), the same Hamiltonian with the operators
  in the order $c_i^\dagger c_j^\dagger c_k c_l$, and (6.5), the Heisenberg model that the second section uses, so
  `eq="1.5 6.5"`.
- Derivation told in words, for a steps fold: from the order of (1.5) to the order of (7.1). The text says that
  the reordering "only relabels $V_{ijkl}$ and adds a bilinear term". The steps are
  $c_i^\dagger c_j c_k^\dagger c_l=\delta_{jk}\,c_i^\dagger c_l-c_i^\dagger c_k^\dagger c_j c_l$, so the quartic
  term is (1.5) with $V$ relabeled and a sign, and the $\delta_{jk}$ term is a hopping.
- Lab box, with the source and the number that the source states: https://arxiv.org/abs/cond-mat/0307483, the
  organic Mott insulator $\kappa$-(BEDT-TTF)$_2$Cu$_2$(CN)$_3$, probe $^1$H NMR and static susceptibility. The
  stored text says "The static susceptibility is described by the spin S = 1/2 antiferromagnetic
  triangular-lattice Heisenberg model with the exchange constant J ~ 250 K." and "Regardless of the large magnetic
  interactions, the ^1H NMR spectra show no indication of long-range magnetic ordering down to 32 mK, which is
  four-orders of magnitude smaller than J." The box quotes $J\sim250$ K and $32$ mK. The source says "suggest that
  a quantum spin liquid state is realized", and the box keeps "suggest". Our reading, marked as ours, is that a
  mean-field calculation would order at a temperature of the order of $J$.
- Pen-and-paper problem: two spins 1/2 in a product state, each pointing along a unit vector
  $\mathbf n_1$, $\mathbf n_2$. Show that $\langle\mathbf S_1\cdot\mathbf S_2\rangle=\tfrac14\,\mathbf n_1\cdot\mathbf n_2$,
  so the best product state has $-1/4$, while the singlet has $-3/4$. Answer $-1/4$ and $-3/4$, the numbers of
  the existing figure `singlet_vs_product.svg`, whose script asserts them.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz stays. The second quiz is
  rewritten (17 words, and its feedback says "as the figure shows") with equations as options. The question holds
  the two rules for two different sites, $c_1^\dagger c_2^\dagger=-c_2^\dagger c_1^\dagger$ and
  $S_1^+S_2^+=S_2^+S_1^+$, and the right option is the relative sign. No picture quiz, since the page is
  motivation.
- Figures to add, each with its pyqula script or the reason for numpy: none, the page has two figures.
- Old figures of the page that break the plot rules: none. `singlet_vs_product.svg` has named axes and ticks at
  $-3/4$ and $-1/4$, and `two_languages.svg` is a schematic.

## 7.2b The Jordan-Wigner transformation

File `02b-the-jordan-wigner-transformation.md`, 1105 words, numbered equations (7.2).

- Question of the page, and where we arrive: how do we turn a spin operator into a fermion operator, when
  fermions on two sites anticommute and spins commute? A string over the sites to the left carries the missing
  sign, spin equals fermion times string, and the XX chain becomes free fermions.
- Main result for the key box: (7.2), with "the string $K_i$ is the parity of the fermions to the left of site
  $i$, so spin equals fermion times string".
- Equation of another page that it starts from, for the recall box: none. The page starts from the naive mapping
  of Section 7.2a, which has no numbered equation, and the opener links Section 7.2a.
- Derivation told in words, for a steps fold: why the string turns anticommutation into commutation, with the
  simplest case of two sites. $K_2=1-2n_1$, and $c_1^\dagger(1-2n_1)=c_1^\dagger$ while $(1-2n_1)c_1^\dagger=-c_1^\dagger$.
  So $S_1^+S_2^+=S_2^+S_1^+$, and $S_1^+S_2^-=c_1^\dagger c_2$, which is the step that the caption of
  `xx_spectrum.svg` states in one line.
- Lab box, with the source and the number that the source states: none. The transformation is an exact identity
  between operators, and no stored source measures it. The spinons of the Heisenberg chain, which a neutron
  measurement would show, belong to Session 8.
- Pen-and-paper problem: write $J(S_1^xS_2^x+S_1^yS_2^y)$ on two sites with (7.2) and find its levels. Answer
  $\tfrac J2(c_1^\dagger c_2+c_2^\dagger c_1)$, with the levels $\pm J/2$ for one fermion and $0$ for zero or two
  fermions, which is the spin result $-J/2,0,0,J/2$ (checked with numpy).
- Quizzes to rewrite, and a picture question or equations as options: the first quiz (22 words, "In the figure")
  becomes the picture question. The question writes $K_6=\exp(i\pi\sum_{j<6}n_j)$ and asks which chain gives
  $S_6^+=-c_6^\dagger$. The three options are three chains with 2, 3 and 4 fermions on sites 1 to 5, and 3 is
  right. The second quiz (19 words) is shortened, with (7.2) written in the question. It keeps its equations as
  options ($K_1=-1$, $1$, $0$). One new quiz with equations as options asks what $J(S_i^xS_{i+1}^x+S_i^yS_{i+1}^y)$
  becomes. Right is $\tfrac J2(c_i^\dagger c_{i+1}+\text{h.c.})$, wrong are $J(c_i^\dagger c_{i+1}+\text{h.c.})$
  and $\tfrac J2(c_i^\dagger c_{i+1}^\dagger+\text{h.c.})$.
- Figures to add, each with its pyqula script or the reason for numpy: `g1_xx_spectrum.py` replaces
  `xx_spectrum.svg`. The single-particle levels come from a pyqula script `xx_chain_fermions.py`, an open chain of
  6 sites with hopping $J/2$ (pyqula hopping 1 times 0.5), and the many-body spin levels stay numpy in the figure
  script, since pyqula has no spins. The caption says which part the download gives. The three picture options are
  `g1_quiz_string_2.py`, `g1_quiz_string_3.py` and `g1_quiz_string_4.py`, schematics with the helper
  `_g1_stringchain.py`.
- Old figures of the page that break the plot rules: `xx_spectrum.svg` has ticks on $N$ only and no number on the
  energy axis, so the new one has ticks at $-1$, $0$, $1$ and the name "$E$ in units of $J$". Figure 7.1 is a
  Blender schematic and stays.

## 7.3 Storing the wave function as the main bottleneck

File `03-storing-the-wave-function-as-the-main-bottleneck.md`, 1146 words, numbered equations (7.3), (7.4).

- Question of the page, and where we arrive: what makes an interacting Hamiltonian hard, the diagonalization or
  the storage of its ground state? The storage, since the exact state of $L$ spins needs $2^L$ coefficients, while
  the matrix can be computed on demand.
- Main result for the key box: (7.4), with "the number of coefficients is $2^L$, and their storage, not the
  diagonalization, is the obstruction". (7.3) stays in the text, where the singlet is built.
- Equation of another page that it starts from, for the recall box: (6.5), the Heisenberg model, since the page
  takes the dimer of Section 6.8.
- Derivation told in words, for a steps fold: the count of the nonzero elements of the Heisenberg matrix in
  the caption of `matrix_vs_vector.svg`. Each basis state has one diagonal element, which is not zero for even
  $L$, and one off-diagonal element for each antiparallel bond. On average a state has $(L-1)/2$ antiparallel
  bonds, so the total is $(L+1)\,2^{L-1}$. The old script asserts this for $L$ from 2 to 22.
- Lab box, with the source and the number that the source states: https://arxiv.org/abs/cond-mat/0312724,
  SrCuO$_2$, probe inelastic neutron scattering. The stored text says "The lower boundary of the continuum extends
  up to ≈ 360 meV, which corresponds to an exchange constant J = 226(12) meV." and that the excitations are "well
  described by the "Muller-ansatz" for the two-spinon continuum in the S=1/2 antiferromagnetic Heisenberg spin
  chain". The box quotes $J=226(12)$ meV. Ours, on the box with `ours`, is only the conversion
  $J/k_B\approx2600$ K, so that $k_BT$ at room temperature is about $0.11\,J$. The box makes no claim on how close
  the chain is to its ground state.
- Pen-and-paper problem: the Heisenberg chain conserves $S^z_\text{tot}$. Count the coefficients of the sector
  $S^z_\text{tot}=0$ for $L=4$ and for $L=30$, and compare with $2^L$. Answer 6 of 16, and
  $\binom{30}{15}=1.55\times10^8$ of $2^{30}=1.07\times10^9$, a factor 6.9. With Stirling the sector is
  $2^L\sqrt{2/(\pi L)}$, so the symmetry gains a factor of order $\sqrt L$ and the growth stays exponential.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz (17 words) is shortened, with
  the count $2^L$ and the 16 bytes in the question. The second quiz, which refers to (7.4), is rewritten with
  (7.4) written in the question and equations as options, $2^{L+1}$ right, $2^L+4$ and $L\,2^L$ wrong. No
  picture quiz.
- Figures to add, each with its pyqula script or the reason for numpy: `g2_memory_scaling.py` and
  `g2_matrix_vs_vector.py` replace the two old figures. Both stay numpy, since they are closed formulas and a count
  on bit strings, with no calculation for pyqula.
- Old figures of the page that break the plot rules: `memory_scaling.svg` has no tick at all, while its caption
  quotes $L=26$, $L=30$ and 1 GB. `matrix_vs_vector.svg` has ticks at $L=10$ and $20$ only, while its caption quotes
  $L=13$ and $L=26$, and no tick on the vertical axis. The new figures have ticks at the quoted values and the
  powers of ten. The number of gigabytes at $L=30$ is open, see the last section.

## 7.4 The matrix product state ansatz and 7.5 Measuring entanglement with the entanglement entropy

File `04-the-matrix-product-state-ansatz.md`, 1409 words, numbered equations (7.5), (7.6), (7.7).

- Question of the page, and where we arrive: can we store a state of $L$ spins with a number of parameters that
  grows only linearly with $L$? The product of matrices (7.5) does it, with $LM^2$ numbers, and the entanglement
  entropy (7.6) is the number that says when this works.
- Main result for the key box: two boxes, since the page has two sections with a result each. The first is (7.5),
  with "$2LM^2$ numbers instead of $2^L$, controlled by the bond dimension $M$". The second is (7.6), with "zero
  for a product state, and $\log 2$ for the singlet (7.7)".
- Equation of another page that it starts from, for the recall box: (7.3) and (7.4), the singlet and the exact
  state of page 7.3, so `eq="7.3 7.4"`. (7.5) to (7.7) are on this page and cannot be recalled here.
- Derivation told in words, for a steps fold: from the singlet (7.3) to (7.7). We write the four terms of
  $|\Psi\rangle\langle\Psi|$, the trace over the second spin keeps the two terms with the same second spin, and
  this gives $\rho_A=\tfrac12|{\uparrow}\rangle\langle{\uparrow}|+\tfrac12|{\downarrow}\rangle\langle{\downarrow}|$
  and then $\log 2$.
- Lab box, with the source and the number that the source states: https://arxiv.org/abs/1508.05949, two electron
  spins 1.3 km apart, probe a Bell test with spin readout. The stored text says "We perform 245 trials testing the
  CHSH-Bell inequality S ≤ 2 and find S = 2.42 ± 0.20." The box quotes $2.42\pm0.20$ against the bound 2. The S
  of the abstract is the CHSH value and not the entropy, so the box writes "the CHSH value" and never the letter S.
  The abstract does not name the host material of the spins, so the box does not name it. Ours, marked as ours, is
  that a product state gives at most 2 and the singlet gives $2\sqrt2\approx2.83$.
- Pen-and-paper problem: write the singlet (7.3) as an MPS with two vectors per site, and show that $M=1$ is not
  enough. Answer $v^\uparrow=(1,0)$, $v^\downarrow=(0,1)$, $w^\uparrow=(0,-1/\sqrt2)$,
  $w^\downarrow=(1/\sqrt2,0)$, which give $C(\uparrow\downarrow)=1/\sqrt2$ and $C(\downarrow\uparrow)=-1/\sqrt2$.
  With $M=1$ we would have $C(\uparrow\uparrow)C(\downarrow\downarrow)=C(\uparrow\downarrow)C(\downarrow\uparrow)$,
  which is $0=-1/2$, so $M=2$ is the smallest. This is the bound (7.10) of Section 7.8 seen by hand.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz is rewritten with (7.5)
  written in the question, and keeps $2LM^2=2\times10^4$. The second quiz is rewritten with the singlet and (7.6)
  written in the question. One new quiz with equations as options asks which state has $S=0$. Right is
  $\tfrac12(|{\uparrow\uparrow}\rangle+|{\uparrow\downarrow}\rangle+|{\downarrow\uparrow}\rangle+|{\downarrow\downarrow}\rangle)$,
  which is a product of two states along $x$. Wrong are $(|{\uparrow\uparrow}\rangle+|{\downarrow\downarrow}\rangle)/\sqrt2$,
  with $\log 2$, and $(|{\uparrow\uparrow}\rangle+|{\uparrow\downarrow}\rangle+|{\downarrow\uparrow}\rangle)/\sqrt3$,
  with $0.381=0.550\log2$ from the weights $0.873$ and $0.127$. No picture quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none, the page has three figures.
- Old figures of the page that break the plot rules: none. `singlet_entropy.svg` has ticks at $0$, $\pi/4$,
  $\pi/2$ and at $\log 2$, `mps_product.svg` is a schematic, and Figure 7.4 shown again is a Blender schematic.

## 7.6 Entanglement entropy of a solvable dimerized chain

File `06-entanglement-entropy-of-a-solvable-dimerized-chain.md`, 1115 words, numbered equations (7.8).

- Question of the page, and where we arrive: does the entanglement entropy of a block grow with its size? For a
  product of singlets it does not, since $S=n_\text{cut}\log2$ counts the singlets cut by the two ends of the
  block.
- Main result for the key box: (7.8), with "$S=n_\text{cut}\log 2$, which is at most $2\log2$ for a block of any
  length".
- Equation of another page that it starts from, for the recall box: (7.6) and (7.7), the entropy and its value for
  one singlet, so `eq="7.6 7.7"`.
- Derivation told in words, for a steps fold: from (7.8) to $S=n_\text{cut}\log2$. The reduced state of a product
  of pure states is the product of the reduced states of the factors. A dimer inside $A$ gives a pure factor, a
  dimer outside gives nothing, and a cut dimer gives $\tfrac12\mathbb 1$, so the entropies add.
- Lab box, with the source and the number that the source states: https://arxiv.org/abs/1406.7596, copper
  nitrate, probe inelastic neutron scattering. The stored text says "We examine the magnetic field dependent
  excitations of the dimerized spin-1/2 chain, copper nitrate, with antiferromagnetic intra-dimer exchange J1=0.44
  meV and exchange alternation α=J2/J1=0.24." and "A singlet ground state at low fields μ0H < μ0Hc1 = 2.8 T". The
  box quotes $J_1=0.44$ meV, the ratio $0.24$ and $2.8$ T. Ours, computed with exact diagonalization of an open
  chain of 16 sites with $J_2=0.24J_1$, is $S=1.00\log2$ for a cut through a strong bond and $0.035\log2$ for a
  cut through a weak bond, so copper nitrate is close to (7.8). These two values go on the box with `ours`, and the
  check script asserts them.
- Pen-and-paper problem: find the spectrum of one dimer $J\,\mathbf S_0\cdot\mathbf S_1$ with
  $\mathbf S_0\cdot\mathbf S_1=\tfrac12(\mathbf S_\text{tot}^2-\tfrac32)$. Answer $-3J/4$ for the singlet and
  $J/4$ for the three triplets, so the gap of (7.8) is $J$. The solution ties it to the $J_1$ of the lab box.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz (which block has zero
  entropy) becomes the picture question. The question writes (7.8) for the pairs (0,1), (2,3), (4,5), (6,7), and
  the three options are the chain with the block of sites 1 to 4, 2 to 5 and 3 to 6 shaded, with no singlet in
  red and no label, since the old pictures `dimer_block_14.svg` and `dimer_block_36.svg` show the answer. These two
  old pictures stay in the feedback. The second quiz says "the same state" and its feedback says "the previous
  question", so it is rewritten to stand alone, with (7.8) in the question. Its options $0$, $\log2$, $2\log2$ are
  already equations.
- Figures to add, each with its pyqula script or the reason for numpy: `g3_dimer_entropy.py` replaces
  `dimer_entropy.svg`, numpy, since it is an exact state of spins. The picture options are `g3_quiz_block_14.py`,
  `g3_quiz_block_25.py` and `g3_quiz_block_36.py`, with a new helper `_g3_dimerquiz.py`. The old helper
  `_dimerchain.py` is not changed, since a change would redraw four old SVGs.
- Old figures of the page that break the plot rules: `dimer_entropy.svg` has no tick at all, while the caption
  quotes $\ell$ from 1 to 10 and the values 1 and 2 of $S/\log2$. `dimer_chain.svg` and the block pictures are
  schematics.

## 7.7 Two dimensions and the area law

File `07-two-dimensions-and-the-area-law.md`, 1285 words, numbered equations (7.9).

- Question of the page, and where we arrive: what changes when the decoupled clusters sit on a two-dimensional
  lattice? The boundary of a region is now a line that grows with the region, so the entropy of a gapped ground
  state grows with the boundary and not with the volume, which is the area law (7.9).
- Main result for the key box: (7.9), with "for the ground state of a gapped and local Hamiltonian, and not for a
  random state, whose entropy follows the volume".
- Equation of another page that it starts from, for the recall box: (7.8), the product of singlets of Section 7.6.
- Derivation told in words, for a steps fold: the count of the cut singlets for a square region in a lattice
  covered by dimers. The dimers are horizontal, on the sites $(2m,y)$ and $(2m+1,y)$. A square of side $\ell$,
  with $\ell$ even, that starts at column 1, cuts $\ell$ dimers on its left side and $\ell$ on its right side, and
  none on the top and bottom, so $S=2\ell\log2$. Doubling $\ell$ doubles $S$, while the volume grows four times.
  The fold uses dimers, since the tetramer state of the page is not written, see the last section.
- Lab box, with the source and the number that the source states: https://arxiv.org/abs/cond-mat/0005342,
  SrCu$_2$(BO$_3$)$_2$, probe inelastic neutron scattering at 1.7 K. The stored text says "We performed inelastic
  neutron scattering on the 2D Shastry-Sutherland system SrCu2(11BO3)2 with an exact dimer ground state." and "The
  lowest excitation at 3.0 meV is almost dispersionless with a bandwidth of 0.2 meV at most". The box quotes
  $3.0$ meV and $0.2$ meV. Ours, marked as ours, is that an exact product of singlets on a 2D lattice has the
  entropy $\log 2$ times the number of singlets cut by the boundary, which is (7.9) with no approximation.
- Pen-and-paper problem: the lattice of the steps fold. Compute $S$ for the squares of side 2 and 4, and compare
  with the volume law. Answer $4\log2$ and $8\log2$, against $4\log2$ and $16\log2$ for a random state, so the two
  laws agree only for the smallest square.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz (16 words) becomes the
  picture question, with (7.9) written in the question as $S_A=\alpha\,|\partial A|$, where $|\partial A|$ is the
  number of cut bonds. Three regions of 16 sites each on a square lattice, a square $4\times4$, a rectangle
  $2\times8$ and a line $1\times16$, which cut 16, 20 and 34 bonds. The question asks which one has the largest
  entropy, and the line is right. The count of cut bonds is written in the question, since for a real state the
  entropy per cut bond can depend on the region. The old content of the first
  quiz, doubling the side doubles $S$, moves into the feedback of the square. The second quiz stops in the middle
  of its sentence ("grows as"), so it is written as a full question, and it keeps its equations as options
  ($\ell^3$, $\ell^2$, a constant).
- Figures to add, each with its pyqula script or the reason for numpy: the picture options
  `g3_quiz_region_square.py`, `g3_quiz_region_rect.py` and `g3_quiz_region_line.py`, top-view schematics with the
  helper `_g3_regions.py`, each with an assert on its number of cut bonds.
- Old figures of the page that break the plot rules: none. `random_vs_gapped.svg` has ticks at $|A|=1,7,13$ and at
  $S_A/\log2=1,7$, and Figure 7.2 is a Blender schematic.

## 7.8a Why MPS work in 1D

File `08-why-mps-work-in-1d-and-where-they-stop-working.md`, 1278 words, numbered equations (7.10).

- Question of the page, and where we arrive: why is a fixed and moderate bond dimension enough for a gapped chain
  of any length? An MPS holds at most $\log M$ across a bond, and the area law says that a gapped chain needs a
  fixed amount, so the two meet.
- Main result for the key box: (7.10), with "a gapped chain needs the same $M$ for 50 or for 500 sites, and a
  volume law would need $M\sim2^{L/2}$".
- Equation of another page that it starts from, for the recall box: (7.5) and (7.9), the ansatz and the area law,
  so `eq="7.5 7.9"`.
- Derivation told in words, for a steps fold: from the rank of $\rho_A$ to (7.10). The Schmidt sum has at most $M$
  terms, and $-\sum_\alpha p_\alpha\log p_\alpha$ with $\sum_\alpha p_\alpha=1$ is largest for equal weights
  $p_\alpha=1/M$, which gives $\log M$. The simplest case is $M=2$, with $p$ and $1-p$.
- Lab box, with the source and the number that the source states: none. The result is a bound of the ansatz and
  not a property of a material. The one stored candidate, Y$_2$BaNiO$_5$ with a correlation length of 3 nm
  (https://arxiv.org/abs/0804.0211), does not say that the chain is gapped nor at which temperature the length
  holds, so a box that ties it to a saturated entropy would say more than the abstract.
- Pen-and-paper problem: a state has the Schmidt weights $\tfrac12,\tfrac14,\tfrac18,\tfrac18$. Compute its
  entropy, compare with $\log M$ for $M=4$, and find the weight that is dropped when we keep $M=2$. Answer
  $S=1.75\log2=1.21$, below $\log4=1.39$, and a dropped weight of $0.25$.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz stays. The second quiz (17
  words) is shortened, with (7.10) written in the question, and its options become equations,
  $S\le\log16=4\log2$ right, $16\log2$ and $8\log2$ wrong. No picture quiz on this page, since the picture of
  entropy curves is on the page of Section 7.11.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: Figure 7.3 is a plot drawn as a schematic, with named axes,
  no ticks and curves that are not computed, as its caption says. It is a Blender figure and stays, see the last
  section. `schmidt_spectrum.svg` has ticks, but the two numbers of its caption, $2\times10^{-7}$ and
  $3\times10^{-11}$, have no assert in its script, so the check script of the page asserts them.

## 7.8b Where MPS stop working

File `08b-where-mps-stop-working.md`, 981 words, numbered equations none.

- Question of the page, and where we arrive: when does the bound (7.10) stop an MPS? When the entropy that the
  state needs grows, which happens after a quench, in two dimensions and in highly excited states.
- Main result for the key box: one box with an unnumbered display, $M\gtrsim e^{S}$, and two sentences. An entropy
  that grows linearly in time, or linearly with the width of a strip, needs an $M$ that grows exponentially.
- Equation of another page that it starts from, for the recall box: (7.10).
- Derivation told in words, for a steps fold: from (7.10) to the cost. With $S(t)\approx vt$ after a quench, $M\ge
  e^{vt}$. For a strip of width $W$ where each row adds the same entropy $s$ to the cut, $M\ge e^{sW}$.
- Lab box, with the source and the number that the source states: https://arxiv.org/abs/2306.00057, a chain of
  trapped ions that realizes the XXZ chain, probe learning of the entanglement Hamiltonian from measurements. The
  stored text says "We prepare ground and excited states of a 1D XXZ Heisenberg chain on a 51-ion programmable
  quantum simulator and perform sample-efficient `learning' of the entanglement Hamiltonian for subsystems of up to
  20 lattice sites." and "Our results also show the transition from area to volume-law scaling of Von Neumann
  entanglement entropies from ground to excited states." The box ties this to the third case of the page. The
  abstract gives no value of an entropy, its numbers are counts, 51 ions and 20 sites, and the system is a quantum
  simulator and not a material. So the lint gives the warning `lab-number`. The box is planned, and whether it
  stays is in the last section.
- Pen-and-paper problem: a gapped model on a strip of width $W$ where an MPS cut crosses $W$ singlets. Find the
  smallest $M$ and the numbers of one tensor, $2M^2$, for $W=10$ and $W=20$. Answer $M=2^{10}=1024$ with
  $2.1\times10^6$ numbers, and $M=2^{20}\approx10^6$ with $2.2\times10^{12}$ numbers.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz (16 words) is shortened,
  with $S(t)\propto t$ and $S\le\log M$ written in the question. The second quiz (17 words) is shortened, with the
  same three options. The paragraph of 189 words is split where the list of the four cases ends.
- Figures to add, each with its pyqula script or the reason for numpy: `g4_quench_entropy.py` replaces
  `quench_entropy.svg`, numpy, since it is an exact time evolution of 12 spins. The figure in the feedback of the
  first quiz points to the new SVG.
- Old figures of the page that break the plot rules: `quench_entropy.svg` names the time $t$ with no unit. The new
  axis is "$t$ in units of $\hbar/J$", with $J=1$ the Ising coupling of the caption. "It turns over at $t\approx4$"
  gets an assert. Figure 7.2 shown again is a Blender schematic.

## 7.9 Tensor diagrams as notation for networks and operators

File `09-tensor-diagrams-as-notation-for-networks-and-operators.md`, 932 words, numbered equations none.

- Question of the page, and where we arrive: how do we compute with an MPS without writing every index? A leg is
  an index, a joined leg is a sum, and applying an MPO multiplies the bond dimensions, which a singular value
  decomposition then cuts back.
- Main result for the key box: one box with the unnumbered rule "$M\to M D$ after an MPO of bond dimension $D$,
  and back to $M$ by keeping the $M$ largest singular values", with one sentence that this truncation is the core
  of every MPS algorithm.
- Equation of another page that it starts from, for the recall box: (7.5).
- Derivation told in words, for a steps fold: from the MPO and the MPS to a bond of dimension $MD$. We write the
  tensors with indices, $W^{\sigma\sigma'}_{ab}$ and $M^{\sigma'}_{\alpha\beta}$, and the sum over $\sigma'$ gives a
  tensor whose left index is the pair $(a,\alpha)$, with $MD$ values. The SVD keeps the largest singular values,
  and the dropped weight is the sum of the squares of the others.
- Lab box, with the source and the number that the source states: none, this is a page of notation.
- Pen-and-paper problem: an MPS with $M=10$ meets an MPO with $D=5$. Find the bond dimension after the contraction
  and the numbers of one bulk tensor of a spin-1/2 chain before, after, and after the truncation. Answer 50, and
  200, 5000, 200.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz (24 words) is shortened, and
  it keeps its equations as options ($M\cdot D$, $M+D$, $M^D$). The second quiz stays. One new picture question
  shows three diagrams of a chain of 4 sites. The question asks which one is a number, and the right picture is the
  closed network $\langle\Psi|\Psi\rangle$. The others are $|\Psi\rangle$ with open physical legs and $H|\Psi\rangle$
  with an MPO on top. The paragraph of 257 words is split where the MPO starts.
- Figures to add, each with its pyqula script or the reason for numpy: the picture options `g4_quiz_net_norm.py`,
  `g4_quiz_net_ket.py` and `g4_quiz_net_hpsi.py`, schematics with the helper `_g4_nets.py`.
- Old figures of the page that break the plot rules: none. `mpo_on_mps.svg` and Figure 7.4 are schematics.

## 7.10 The variational principle and DMRG for the ground state

File `10-the-variational-principle-and-dmrg-for-the-ground-state.md`, 1181 words, numbered equations (7.11).

- Question of the page, and where we arrive: how do we find the best MPS without searching a space of size $2^L$?
  We minimize (7.11) one tensor at a time, each step is a small eigenvalue problem, and the energy never goes up,
  which is DMRG.
- Main result for the key box: (7.11), with "$E[\Psi]\ge E_0$ for every state, and an update of one tensor cannot
  raise $E$".
- Equation of another page that it starts from, for the recall box: (7.5).
- Derivation told in words, for a steps fold: from (7.11) to the local eigenvalue problem. With the other tensors
  fixed, $E=A^\dagger H_\text{eff}A/A^\dagger NA$, where $A$ is the tensor of site $k$ as a vector of $2M^2$
  numbers. The derivative with respect to $A^\dagger$ gives $H_\text{eff}A=E\,NA$, and $N=1$ in an orthonormal
  gauge.
- Lab box, with the source and the number that the source states: none, this is a page of an algorithm.
- Pen-and-paper problem: show that $E[\Psi]\ge E_0$ by expanding $|\Psi\rangle$ in eigenstates, and evaluate it for
  $(|0\rangle+|1\rangle)/\sqrt2$ with $E_0=-1$ and $E_1=0$. Answer
  $E-E_0=\sum_n|c_n|^2(E_n-E_0)/\sum_n|c_n|^2\ge0$, and $E=-0.5$.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz (16 words, refers to (7.11))
  becomes the picture question, with (7.11) and $E[\Psi]\ge E_0$ written in the question. The three options draw
  $E$ in units of $J$ on a linear axis against the update, with a dashed line at $E_0$ and the same scale, since a
  point below $E_0$ has no place on the logarithmic axis of $E-E_0$. Right is the computed sweep for $M=4$. Wrong
  are the same data with one step that goes up and the same data shifted so that the last points fall below the
  line of $E_0$. The alt of each picture says what is drawn,
  and the feedback says that the two wrong ones are changed by hand. The second quiz stops in the middle of its
  sentence ("has a matrix of size"), so it is written as a full question, and it keeps its equations as options
  ($2M^2$, $2^L$, $2M$).
- Figures to add, each with its pyqula script or the reason for numpy: `g4_dmrg_sweeps.py` replaces
  `dmrg_sweeps.svg`, numpy, since it is a variational sweep on 10 spins. The picture options are
  `g4_quiz_sweep_ok.py`, `g4_quiz_sweep_up.py` and `g4_quiz_sweep_below.py`, with the helper `_g4_sweeps.py`, all
  three from the same sweep.
- Old figures of the page that break the plot rules: `dmrg_sweeps.svg` names $E-E_0$ with no unit, so the new axis
  is "$E-E_0$ in units of $J$". Its three caption numbers, $0.2$, $6\times10^{-3}$ and $1.5\times10^{-5}$, are
  printed by the script but not asserted, and the new script asserts them. Figure 7.5 is a Blender schematic.

## 7.11 MERA and PEPS beyond MPS

File `11-mera-and-peps-beyond-mps.md`, 1310 words, numbered equations (7.12).

- Question of the page, and where we arrive: what network describes a critical chain, whose entropy does not
  saturate, and what network describes two dimensions? MERA holds the slow growth (7.12), and PEPS put a tensor on
  every site of a 2D lattice, at the price of a hard contraction.
- Main result for the key box: (7.12), with "$c$ is the central charge, $c=1$ for the XX chain, and the growth
  is slow but has no limit".
- Equation of another page that it starts from, for the recall box: (7.9) and (7.10), so `eq="7.9 7.10"`.
- Derivation told in words, for a steps fold: from the layers of a MERA to the logarithm. A block of $\ell$ sites
  needs about $\log_2\ell$ layers, the cut crosses one bond per layer, and each bond holds at most $\log M$, so the
  bound is $\log_2\ell\cdot\log M$, which grows as $\log\ell$ like (7.12).
- Lab box, with the source and the number that the source states: https://arxiv.org/abs/cond-mat/9809068, copper
  pyrazine dinitrate, probe magnetization, specific heat and inelastic neutron scattering. The stored text says
  "The material is an ideal one-dimensional spin-1/2 Heisenberg antiferromagnet with nearest neighbor exchange
  constant J=0.90(1) meV and chains extending along the orthorhombic a-direction." and "coppyer pyrazine
  dinitrate remains gapless and paramagnetic for g mu_B H/J at least up to 1.4 and for k_B T/J at least down to
  0.03", with the misspelling of the abstract. The box quotes $J=0.90(1)$ meV and the ratio $0.03$. Ours, marked
  as ours, is that $0.03\,J$ is about $0.3$ K, and that a gapless chain is critical, so the entropy of a block
  follows (7.12) with $c=1$, the value of the notebook for the Heisenberg chain.
- Pen-and-paper problem: an MPS cut of a block in an infinite chain crosses two bonds, so $S\le2\log M$. Show with
  (7.12) that $M$ must grow as $\ell^{c/6}$, and compute the factor from $\ell=10$ to $\ell=1000$ for $c=1$.
  Answer $100^{1/6}\approx2.15$, a power law and not an exponential.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz stays, with the feedback
  numbers of the figure computed again. The second quiz (25 words) is shortened into three sentences, and it keeps
  its options. One new picture question shows three curves of $S$ against $\ell$, for a dimerized chain, a
  critical chain and a volume law $\ell\log2$, and asks which one is the critical chain. The three share a
  logarithmic axis of $\ell$ from 2 to 100 and a linear axis of $S$ from 0 to 2.5. On it the dimerized chain is
  flat near $0.5$, the critical chain is a straight rising line that reaches about $2.2$, and the volume law leaves
  the frame at $\ell\approx3.6$, so the three shapes differ.
- Figures to add, each with its pyqula script or the reason for numpy: `g5_critical_entropy.py` replaces
  `critical_entropy.svg`, with the pyqula script `entropy_critical_chain.py`. It is a block in the middle of an open
  chain of $N=3002$ sites, `geometry.chain()` for the critical chain and `geometry.bichain()` with
  `h.inter = 0.6*h.inter` for the dimerized one, with about five blocks from 10 to 1000 sites, about 9 s each. In
  this geometry $S(10)=1.49$ and $S(1000)=2.97$, against $3.03$ of the infinite chain of the old caption, so the
  caption and the feedback of the first quiz get their numbers from the new script. The picture options
  `g5_quiz_entropy_gapped.py`, `g5_quiz_entropy_critical.py` and `g5_quiz_entropy_volume.py` do not run the
  script of $N=3002$ sites, which takes about 45 s. Their helper `_g5_entropycurves.py` calls pyqula on an open
  chain of 402 sites with blocks up to 100, which takes about a second and wrote no file in the test of this plan.
  The options have no button.
- Old figures of the page that break the plot rules: `critical_entropy.svg` has its axes and ticks, and it is
  replaced only because pyqula does this calculation. Figure 7.6 is a Blender schematic.

## 7.12 Closing summary

File `12-closing-summary.md`, 719 words, numbered equations none.

- Question of the page, and where we arrive: none, it is the closing page, with the summary as it is.
- Main result for the key box: none, a closing page.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none, a closing page.
- Quizzes to rewrite, and a picture question or equations as options: the one quiz stays. One new quiz with
  equations as options asks how many numbers an MPS stores, $2LM^2$ right, $2^L$ and $M^L$ wrong.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: Figure 7.3 shown again, the same as in Section 7.8a.
- What the student can now do, a new list after the summary, each item with its section, in the form of
  Session 3.
  - Map a spin-1/2 chain to spinless fermions with the string, and see when the string cancels. This is in
    Section 7.2b.
  - Count the coefficients of an exact state and the numbers of an MPS of bond dimension $M$. This is in Section
    7.3 and Section 7.4.
  - Compute the entanglement entropy of a two-spin state and of a product of singlets. This is in Section 7.5 and
    Section 7.6.
  - Tell an area law from a volume law, and count the cut bonds of a region in one and two dimensions. This is in
    Section 7.7.
  - Find the smallest bond dimension from the Schmidt weights of a cut, with $S\le\log M$. This is in Section 7.8a.
  - Say why a quench, a 2D lattice or an excited state needs an exponentially large $M$. This is in Section 7.8b.
  - Read a tensor diagram and give the bond dimension after an MPO. This is in Section 7.9.
  - Explain why a DMRG sweep never raises the energy. This is in Section 7.10.
  - Say which network fits a critical chain and which one fits a 2D lattice. This is in Section 7.11.

## Candidates for the lab boxes

The notebook of the session has no "In the lab" cell. The articles below were read on arXiv. A box is planned
only where the text stored with `labsource.py --session 7` holds the number.

- Stored and planned: `shimizu2003_arxivcond-mat-0307483.txt` (7.1), `zaliznyak2004_arxivcond-mat-0312724.txt`
  (7.3), `hensen2015_arxiv1508.05949.txt` (7.5), `stone2014_arxiv1406.7596.txt` (7.6),
  `kageyama2000_arxivcond-mat-0005342.txt` (7.7), `joshi2023_arxiv2306.00057.txt` (7.8b),
  `hammar1998_arxivcond-mat-9809068.txt` (7.11). The last one was stored after many refusals of arXiv (HTTP 429).
- Stored and not planned: `xu2007_arxiv0804.0211.txt`, for the reason in the block of Section 7.8a.
- Read and rejected, since the abstract states no number for the page: arXiv 1509.01160 (Rényi entropy of
  bosons), 1603.04409 (thermalization through entanglement), 1806.05747 (entropy from randomized measurements),
  1805.09819 (entanglement in a many-body localized chain), 1111.0776 (light cone after a quench), 2206.10563 (area
  law of mutual information), cond-mat/0501069 (KCuF$_3$), and 1103.3694 (CoNb$_2$O$_6$, whose abstract gives the
  golden ratio in words only). arXiv 1306.4678 states 71% and 99(8)% but does not name its compound.

## Builder groups

| group | pages | what joins them |
|---|---|---|
| g1 | `01-two-regimes-of-many-body-physics.md`, `02b-the-jordan-wigner-transformation.md` | the two languages, fermions and spins |
| g2 | `03-storing-the-wave-function-as-the-main-bottleneck.md`, `04-the-matrix-product-state-ansatz.md` | $2^L$ against $LM^2$, and the singlet (7.3) that both use |
| g3 | `06-entanglement-entropy-of-a-solvable-dimerized-chain.md`, `07-two-dimensions-and-the-area-law.md`, `08-why-mps-work-in-1d-and-where-they-stop-working.md` | the dimerized chain, the counting of cut singlets, and the area law that (7.10) uses |
| g4 | `08b-where-mps-stop-working.md`, `09-tensor-diagrams-as-notation-for-networks-and-operators.md`, `10-the-variational-principle-and-dmrg-for-the-ground-state.md` | the bound (7.10) at work, the diagrams and the sweep |
| g5 | `11-mera-and-peps-beyond-mps.md`, `12-closing-summary.md` | the critical chain, and the closing list that names every section |

What is special about each group.

- g1. The index is not edited and belongs to no group. The pyqula script `xx_chain_fermions.py` is owned by g1.
  The XX chain of Section 7.2b and the critical chain of Section 7.11 are the same model, but they use different
  scripts, so g1 and g5 share no file.
- g2. Two replaced figures and the GB question of the last section, which g2 does not decide. The caption of
  `g2_memory_scaling` keeps the old wording of the memory at $L=30$ until the lecturer picks.
- g3. The new helpers `_g3_dimerquiz.py` and `_g3_regions.py`. The copper nitrate values of the lab box of 7.6
  are computed in the check script. The tetramer wording of 7.7 is open, so the fold and the problem use dimers.
- g4. The quench, the diagrams and the sweeps are numpy or schematics. The picture options of 7.10 are made from
  the sweep of `g4_dmrg_sweeps.py`, through the helper `_g4_sweeps.py`.
- g5. The pyqula script `entropy_critical_chain.py` is owned by g5 and feeds the main figure of Section 7.11. The
  three picture options call pyqula on a short chain through `_g5_entropycurves.py`, with the same models. The lab
  box of 7.11 uses the stored `hammar1998_arxivcond-mat-9809068.txt`. The closing list links every section of the
  session.

## Open for the lecturer

Each item touches a numbered equation, a statement of the old text or a convention, so a builder leaves it as it is
and reports it.

1. The symbol of the bond dimension. In (7.5) the letter $M$ is both the matrix $M_i^{s_i}$ and its size, the
   try-it boxes and the notebook write $\chi$ (`maxm`), Section 7.9 writes $D$ for the MPO, and Section 10.4
   writes $D$ for the bond dimension of an MPS.
2. The geometry of (7.12). The factor $c/3$ holds for a block of $\ell$ sites inside an infinite chain, which has
   two ends, and the notebook cell "Size dependence of the entanglement entropy" writes $\frac c6\ln L$ for half of
   an open chain, with one end. The page writes no condition next to (7.12), and the caption of the old figure
   says "a block of $\ell$ sites of an infinite chain".
3. The notebook box of Section 7.8b says that the half-chain entropy of the Heisenberg chain "grows very little
   with the system size, which is the 1D area-law saturation of Section 7.6, but this time in a gapless chain".
   A gapless chain does not saturate. With exact diagonalization of the open chain, the entropy at the middle bond
   is $0.457$, $0.537$, $0.592$ for $L=8,12,16$ and $0.738$, $0.762$, $0.784$ for $L=10,14,18$, so it grows
   slowly with $L$, as the $\frac c6\ln L$ of the notebook says.
4. The memory at $L=30$. The caption of `memory_scaling.svg` says "sixteen gigabytes", while its script draws
   1 GB as $10^9$ bytes. $2^{30}$ numbers of 16 bytes are $1.72\times10^{10}$ bytes, which is 17.2 GB or 16 GiB,
   and the first quiz of the page says $1.7\times10^{10}$ bytes and "about 17 terabytes" for $L=40$.
5. The tetramer model of Section 7.7 is not written. The text says "one contribution per cut bond", the caption
   of Figure 7.2 says "at most $\log 2$ per cut bond", and the quiz counts "cut tetramers". For a ring of four
   spins with Heisenberg bonds, a cut of one site from three gives $\log2$, a cut into two neighboring pairs gives
   $1.21\log2$ across two bonds, and a cut into the two diagonal pairs gives $\log3=1.58\log2$ across four bonds.
   So the caption is right, and "one contribution per cut bond" is not exact.
6. Download of `dmrgpy` scripts. The spin calculations of this session are what the notebook does with `dmrgpy`,
   but the build refuses a script that does not import pyqula, so they stay numpy with no button.
7. Figure 7.3 is a plot with no ticks and with curves that are not computed. On the web it could be replaced by a
   computed plot from the pyqula script of Section 7.11, with the bars $\log4$ and $\log16$, or it stays.
8. The lab box of Section 7.8b bends the locked rule of one material and one number with its unit. Its source is a
   chain of 51 trapped ions, a quantum simulator, and the abstract gives only counts, 51 ions and subsystems of up
   to 20 sites, with no value of an entropy. It is planned, since it shows the change from area law to volume law
   between ground and excited states, which is the third case of the page. It stays, or the page has no lab box.
