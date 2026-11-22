# Plan of Session 5 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session05.md`.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 540 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 (0) | 0 |
| `01-weakly-versus-strongly-correlated-matter-revisited.md` | 5.1 | 592 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | opener 1, quiz-long 1 |
| `02-superconductivity-as-a-macroscopic-quantum-phenomenon.md` | 5.2, 5.3 | 1115 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `04-the-interacting-hamiltonian-and-the-origin-of-attractive-interactions.md` | 5.4, 5.5 | 1133 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | key 1, opener 1, quiz-long 1 |
| `06-why-pairing-does-not-conserve-the-particle-number.md` | 5.6, 5.7 | 1050 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, opener 1, quiz-long 1 |
| `08-the-nambu-spinor-and-the-bogoliubov-de-gennes-hamiltonian.md` | 5.8 | 1112 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | key 1, opener 1 |
| `09-an-example-of-a-gap-that-opens-independently-of-the-dispersion.md` | 5.9, 5.10 | 1235 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 (0) | opener 1, quiz-ref 1 |
| `11-the-general-pairing-hamiltonian-and-its-symmetry-classification.md` | 5.11 | 842 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | key 1, opener 1 |
| `12-building-a-spin-triplet-superconductor-out-of-a-magnet.md` | 5.12 | 814 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | quiz-long 1 |
| `13-nodal-singlet-order-d-wave-pairing-in-the-cuprates-and-the-angular-momentum-expansion.md` | 5.13 | 1217 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | key 1, opener 1, quiz-long 1 |
| `14-same-gap-and-different-topology-in-trivial-s-wave-and-chiral-p-wave-pairing.md` | 5.14 | 1205 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `15-majorana-bound-states-and-how-to-split-an-electron-into-two-majoranas.md` | 5.15 | 720 | 3 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1 |
| `16-the-kitaev-chain-as-the-minimal-model-with-isolated-majoranas.md` | 5.16 | 988 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1 |
| `17-topological-zero-modes-with-periodic-and-open-boundaries.md` | 5.17 | 1129 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1 |
| `18-engineering-a-topological-superconductor-from-a-quantum-spin-hall-insulator.md` | 5.18 | 984 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | opener 1 |
| `19-topological-quantum-computing-with-majoranas.md` | 5.19 | 931 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1 |
| `20-closing-summary.md` | 5.20 | 789 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | 0 |

## Before the builders start

The conventions sheet `webnotes/conventions/session05.md` does not exist yet, so this plan states no sign and no map
from a parameter of pyqula to a parameter of a page. The sheet needs these lines, each checked by a number, before a
builder writes a caption or a fold that depends on them.

- The Fourier convention of Section 2.5, $c_n^\dagger=\sum_\varphi e^{-in\varphi}\Psi_\varphi^\dagger$, and the
  sign of $\Delta(k)$ in [(5.20)](#eq-5-20) that it gives. This is open, see "Open for the lecturer".
- The Nambu basis of pyqula against [(5.6)](#eq-5-6), the sign of the hopping of `geometry.chain()`, and how
  `h.add_onsite` enters $\mu$ of [(5.4)](#eq-5-4) and [(5.8)](#eq-5-8). A run of `h.setup_nambu_spinor()` and
  `h.add_swave(0.45)` on the chain with `h.add_onsite(1.0)` gives the smallest $|E|$ equal to $0.45$.
- How the gap is read from `h.get_mean_field_hamiltonian(U=U, filling=0.1, nk=100, mix=0.5, mf="swave")`. With
  these settings, which are those of the notebook, the smallest $|E|$ is $0.103$, $0.223$ and $0.361$ at $U=-1$,
  $-1.5$ and $-2$. With `nk=10` and `mix=0.9` the value at $U=-1$ is $0.006$, so the settings of the notebook stay.
- The chirality of `h.add_pairing(mode="chiral_pwave")` against [(5.15)](#eq-5-15). On the triangular lattice with
  `h.add_onsite(-3.0)`, `h.get_chern()` gives $-2.0$ for `delta=0.4` and `0.8`, and $0.0$ for `mode="swave"`.
- The sign and the size of `h.add_exchange` against $h$ of Section 5.12, and the forms of `mode="nodal_fwave"` and
  `mode="dwave"`.
- The Kitaev chain of pyqula. The notebook builds it from a spinful chain with `h.add_onsite(4.0)` and
  `h.add_exchange([0.,0.,4.])`. A run on 40 sites with `h.add_pairing(mode="pwave", delta=0.5, d=[1.,1.,0.])` at
  $\mu=0$ gives the lowest bulk level $1.418$, while the exact chain [(5.19)](#eq-5-19) gives $1.414$ for
  $\Delta=0.707$ and $1.008$ for $\Delta=0.5$. The size of the pairing for this `d` and the shift by the remote band
  are for the sheet. Whether the Kitaev figures get a pyqula script is a pick, see "Open for the lecturer".

Every pyqula call writes files (`BANDS.OUT`, `CHERN.OUT`) in the folder where it runs, so it runs only inside a
script of `webnotes/scripts/session05/` through `style.run_script`.

The old figures stay as they are. A builder does not edit an old figure script or its SVG, and does not replace an
old figure on a page, as in Session 3, where the old figures were kept and 81 new files were added. The field "Old
figures of the page that break the plot rules" of each block is the list for the report of the final step, and the
question of fixing them is a pick in "Open for the lecturer". New figures carry the prefix of the group, and a
helper that several new scripts import starts with an underscore, as `_g1_name.py`, after
`figures/session03/_g1_flake.py`.

For the lab boxes, `labsource.py --check 5` cannot run before a box exists. In its place we ran the function `find`
of `labsource.py` on each planned number, against the tracked file and against the full copy. The texts pasted
from the APS and Nature pages show as "missing" in the tracked files until a page quotes them, so each builder runs
`python3 webnotes/labsource.py --quotes` after the box exists, and then `--check 5`. The source of Section 5.18 with
the number 100 K is the one of Session 3, in `sources/.full/session03/wu2018_science.aan6003.txt`, and it is not
stored again, since a new fetch under Session 5 would remove the file of Session 3. Two things about the tool. It
stopped with an `IndexError` on the collaboration author of the article of Section 5.19, at the line that builds
`family` before `--name` is read, so that article is stored from its arXiv id with `--url`. And it reads "1T" in
"1T′-WTe2" as one tesla, so a box writes "monolayer WTe$_2$".

## index.md, the introduction of the session

File `index.md`, 540 words, numbered equations none.

- Question of the page, and where we arrive: none. It is the map of the session and not a section page.
- Main result for the key box: none, for the same reason.
- Equation of another page that it starts from, for the recall box: none. It already names (1.9), (1.10) and (3.4) in the text.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, the lint gives no hit.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `session_map` is a concept map and not a plot.
- So the index is not edited and is in no group. The pass of Session 3 left its index unchanged too, in commit `aa080a7`.

## 5.1 Weakly versus strongly correlated matter, revisited

File `01-weakly-versus-strongly-correlated-matter-revisited.md`, 592 words, numbered equations none.

- Question of the page, and where we arrive: Why does a superconductor have a mean-field description, while the fractional quantum Hall state needs exact methods? We arrive at the split into weakly and strongly correlated matter, with the superconductor on the weak side and an attractive interaction.
- Main result for the key box: none, a page of motivation.
- Equation of another page that it starts from, for the recall box: none. The page already shows (1.5) as a display and names it, and a recall box would show it twice.
- Derivation told in words, for a steps fold: none, there is no derivation.
- Lab box, with the source and the number that the source states: none, a page of motivation.
- Pen-and-paper problem: none, a page of motivation.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz of line 14 (18 words) into two short sentences, with the same point. New quiz with equations as options, "Which decoupling of $U n_\uparrow n_\downarrow$ gives a superconductor?", with $\langle c_\uparrow^\dagger c_\uparrow\rangle c_\downarrow^\dagger c_\downarrow$, $\langle c_\uparrow^\dagger c_\downarrow\rangle c_\downarrow^\dagger c_\uparrow$ and $\langle c_\downarrow c_\uparrow\rangle c_\uparrow^\dagger c_\downarrow^\dagger$, the three channels of the figure of the page.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `s01f03_threechannels` is a converted drawing.

## 5.2 Superconductivity as a macroscopic quantum phenomenon and 5.3 Zero resistance and the Meissner effect in a superconductor

File `02-superconductivity-as-a-macroscopic-quantum-phenomenon.md`, 1115 words, numbered equations (5.1).

- Question of the page, and where we arrive: How can a measurement on a sample of many atoms give the ratio $h/2e$ of two microscopic constants? We arrive at flux quantization [(5.1)](#eq-5-1) from a single-valued phase, and at zero resistance and the Meissner effect as two signatures of the same condensate.
- Main result for the key box: [(5.1)](#eq-5-1), $\Phi=n\Phi_0$ with $\Phi_0=h/2e$. The 2 is the charge $2e$ of a pair, and no parameter of the material enters.
- Equation of another page that it starts from, for the recall box: (1.9), $\Delta=\langle c_ic_j\rangle$. The phase $\theta$ of the ring argument is the phase of this pair amplitude.
- Derivation told in words, for a steps fold: "From the phase of the condensate to flux quantization". The current of a condensate of charge $2e$ is proportional to $\hbar\nabla\theta-2e\mathbf A$, the current vanishes on the loop deep in the ring, the phase winds by $2\pi n$, and this gives [(5.1)](#eq-5-1). A thin ring first.
- Also: the paragraph of line 15 (188 words) is split before "Note the parallel with the quantum Hall state".
- Lab box, with the source and the number that the source states: the ac Josephson effect, which the text of 5.2 already names, with [this article](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.18.287), abstract pasted from the APS page. The source states "Using the ac Josephson effect, we have determined that 2e/h = 483.5912 ± 0.0030 MHz/μV." The abstract names no material, so the box names none and says that the ratio has no parameter of the material. The box does not say that the value agrees with the SI value, which is $483.5978$ MHz/μV and lies 2.2 error bars away. A conversion to $h/2e$ in Wb is our reading, in its own sentence.
- Pen-and-paper problem: A ring has a hole of radius 1 μm. Which field puts one flux quantum through it? The answer is $(h/2e)/\pi r^2=0.658$ mT. It ends on why a SQUID can count these steps.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz of line 20 (16 words) with the loop condition $\oint\nabla\theta\cdot d\boldsymbol\ell=(q/\hbar)\Phi$ in the question, same point. New quiz with equations as options for the ac Josephson frequency, $f=2eV/h$, $eV/h$ and $eV/2h$. New picture quiz for 5.3, three drawings of field lines, which cross the sample, go around it, or pass in thin bundles, with the question which one is a type-II superconductor below $T_c$ at a moderate field.
- Figures to add, each with its pyqula script or the reason for numpy: the three quiz drawings only, in numpy, with a helper `_g1_fieldlines.py` made from the code of `tc_meissner.py`. They are drawings of real space, with no calculation for pyqula.
- Old figures of the page that break the plot rules: none. Panel (a) of `tc_meissner` is marked as a schematic and has its arrows and $T_c$, and panels (b) and (c) are drawings.

## 5.4 The interacting Hamiltonian and the origin of attractive interactions and 5.5 The mean-field pairing Hamiltonian in detail

File `04-the-interacting-hamiltonian-and-the-origin-of-attractive-interactions.md`, 1133 words, numbered equations (5.2), (5.3), (5.4).

- Question of the page, and where we arrive: Electrons repel each other, so where does an attraction come from, and how does it give a pair amplitude? We arrive at an effective attraction from a phonon below $\omega_0$, and at the mean-field Hamiltonian [(5.4)](#eq-5-4) with $\Delta_n$ of [(5.3)](#eq-5-3), which is nonzero only for $U<0$.
- Main result for the key box: [(5.4)](#eq-5-4), with one sentence on $\Delta_n=U\langle c_{n\downarrow}c_{n\uparrow}\rangle$ of [(5.3)](#eq-5-3), which is self-consistent, zero for $U>0$ and the term that breaks gauge symmetry.
- Equation of another page that it starts from, for the recall box: (1.7), the Hubbard chain of Session 1. [(5.2)](#eq-5-2) is the same with $U<0$ and a chemical potential.
- Derivation told in words, for a steps fold: "From the attractive chain (5.2) to the mean-field Hamiltonian (5.4)". We write $B_n=c_{n\downarrow}c_{n\uparrow}$, the quartic term is $B_n^\dagger B_n$, we put $B_n=\langle B_n\rangle+\delta B_n$ and drop $\delta B_n^\dagger\delta B_n$, which gives the two pairing terms and the constant $-|\Delta_n|^2/U$. One site first.
- Lab box, with the source and the number that the source states: sulfur hydride under pressure, with [this article](https://www.nature.com/articles/nature14964), stored with its arXiv abstract and with the published abstract pasted from the Nature page. The published text states "On cooling, we see signatures of superconductivity: a sharp drop of the resistivity to zero and a decrease of the transition temperature with magnetic field, with magnetic susceptibility measurements confirming a Tc of 203 kelvin." and "Moreover, a pronounced isotope shift of Tc in sulfur deuteride is suggestive of an electron–phonon mechanism of superconductivity that is consistent with the Bardeen–Cooper–Schrieffer scenario." The arXiv text says "is evidence of" instead, and the box uses the weaker "suggestive of". The probes are the resistivity and the susceptibility. Our reading, marked as ours, is that a heavier isotope lowers $\omega_0$ of the phonon figure.
- Pen-and-paper problem: One site with $H=Un_\uparrow n_\downarrow-\mu(n_\uparrow+n_\downarrow)$ and $U=-2t$. For which $\mu$ are the empty and the doubly occupied site degenerate, and how far above them are the singly occupied states? The answer is $\mu=U/2=-t$, and the singly occupied states are $t$ above. It ends on the bound pair as the seed of $\Delta_n$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz of line 37 (18 words) with $\Delta_\text{new}=-Ug\,\Delta$ as a display in the question, same point. New picture quiz, three electron-hole bands of the mean-field chain at $U=-1$, $-1.5$ and $-2$ with filling $0.1$, with the question which chain has the strongest attraction, read from the gap on the energy axis.
- Figures to add, each with its pyqula script or the reason for numpy: the self-consistent gap against $U$ of the attractive chain at filling 0.1, from the pyqula script `g1_meanfield_swave_chain.py` with the settings of the notebook (`nk=100`, `mix=0.5`), which also gives the three quiz pictures. This plot backs the try-it box of the page.
- Old figures of the page that break the plot rules: `phonon_exchange` (b) has no tick numbers, and its units are only in the caption, so it lacks $V_\mathrm{eff}$ in units of $2g^2/\omega_0$ with ticks at 0 and $V_c=0.5$, and $\omega$ in units of $\omega_0$ with the tick 1. `pairing_cobweb`, in a quiz feedback, has no ticks at $\Delta_0=1$ and $0.5$. Both are left and reported.

## 5.6 Why pairing does not conserve the particle number and 5.7 The gauge transformation in explicit form

File `06-why-pairing-does-not-conserve-the-particle-number.md`, 1050 words, numbered equations (5.5).

- Question of the page, and where we arrive: What does it mean that a superconductor has a fixed parity and no fixed electron number, and why does the pairing term get the gauge phase twice? We arrive at a Hamiltonian that changes $N$ only by 0 or $\pm2$, and at the phase $e^{-2i\varphi}$ of [(5.5)](#eq-5-5).
- Main result for the key box: two boxes. For 5.6, the unnumbered display $[H_\text{MF},(-1)^{\hat N}]=0$ and $[H_\text{MF},\hat N]\neq0$, with one sentence. For 5.7, [(5.5)](#eq-5-5), with the sentence that both operators are creation operators, so a fixed phase of $\Delta$ is a choice of the ground state.
- Equation of another page that it starts from, for the recall box: (5.4) and (1.10).
- Derivation told in words, for a steps fold: "The ground state of one site with pairing". The state with one electron decouples, the problem is $2\times2$ in $|0\rangle$ and $|2\rangle$, and at $\mu=0$ the ground state is $(|0\rangle-|2\rangle)/\sqrt2$, which is the blue bars of the quiz figure.
- Lab box, with the source and the number that the source states: an aluminium island in a single-electron transistor, with [this article](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.69.1997), abstract pasted from the APS page. The source states "At low bias voltages and low temperatures we find that the I-V curve is 2e periodic with respect to the gate-induced charge." and "Remarkably, this periodicity persists up to 300 mK, a behavior which we interpret as strong evidence of an incremental free energy which depends on whether the number of electrons on the superconducting island is even or odd." The probe is transport. Our reading is that the island chooses the even parity.
- Pen-and-paper problem: One site with $\Delta=0.5$ and $\mu=0.5$. Find $P(N=0)$ and $P(N=2)$ in the ground state. The answer is $P(N=2)=0.854$ and $P(N=0)=0.146$, with the energy $-1.207$, which are the red bars of the quiz figure.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz of line 9 (19 words), same point. Keep the quiz on $\varphi=\pi$. New quiz with equations as options, "Which term changes under $c\to c\,e^{i\varphi}$?", with $c_i^\dagger c_j$, $c_i^\dagger c_ic_j^\dagger c_j$ and $c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger$.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `particle_number_weights` has no ticks on $P(N)$, where the values $0.5$ and $0.85$ of the text and of the problem would go. Left and reported.

## 5.8 The Nambu spinor and the Bogoliubov-de Gennes Hamiltonian

File `08-the-nambu-spinor-and-the-bogoliubov-de-gennes-hamiltonian.md`, 1112 words, numbered equations (5.6), (5.7), (5.8), (5.9).

- Question of the page, and where we arrive: How do we diagonalize a Hamiltonian that mixes creation and annihilation operators? We arrive at the Nambu spinor [(5.6)](#eq-5-6), the BdG matrix [(5.7)](#eq-5-7) in two identical blocks [(5.8)](#eq-5-8), and the spectrum [(5.9)](#eq-5-9).
- Main result for the key box: two boxes, [(5.8)](#eq-5-8) with one sentence on the electron and the hole entries, and [(5.9)](#eq-5-9) with the sentence that the smallest $|E|$ is $|\Delta|$, at $\varepsilon=0$.
- Equation of another page that it starts from, for the recall box: (5.4).
- Derivation told in words, for a steps fold: "From the mean-field Hamiltonian (5.4) to the BdG matrix (5.7) and the spectrum (5.9)". The Fourier transform of the onsite pairing, the factor $\tfrac12$, the $-\varepsilon$ from $cc^\dagger=1-c^\dagger c$ with its constant, and the eigenvalues of the $2\times2$ block. One block first, and every sign checked with a number.
- Lab box, with the source and the number that the source states: none. ARPES sees both branches of the Bogoliubov dispersion in Bi$_2$Sr$_2$Ca$_2$Cu$_3$O$_{10+\delta}$ (Phys. Rev. Lett. 90, 217002), but its abstract has no number, so it is not stored and there is no box.
- Pen-and-paper problem: Show that the electron weight of the upper branch of [(5.8)](#eq-5-8) is $|u|^2=\tfrac12(1+\varepsilon/E)$, and evaluate it at $\varepsilon=|\Delta|$. The answer is $0.854$. It ends on the weight $|v|^2$ that ARPES sees on the hole branch.
- Quizzes to rewrite, and a picture question or equations as options: keep the quiz on (5.9). New quiz with equations as options, the eigenvalues of [(5.8)](#eq-5-8), with $\pm\sqrt{\varepsilon^2+|\Delta|^2}$, $\varepsilon\pm|\Delta|$ and $\pm(|\varepsilon|+|\Delta|)$. New picture quiz, three BdG band plots of the square lattice with the electron weight in color, for `h.add_swave(0.2)`, `0.4` and `0.8`, the values of the try-it box, with the question which one has $|\Delta|=0.8$, read from the gap $2|\Delta|$ at the crossing.
- Figures to add, each with its pyqula script or the reason for numpy: the BdG bands of the square lattice with the electron weight as the color, from the pyqula script `g2_nambu_square.py`, the calculation of the notebook cell "Nambu electronic structure with superconductivity" (`geometry.square_lattice()`, `h.set_filling(0.2, nk=20)`, `h.setup_nambu_spinor()`, `h.add_swave(0.8)`, `h.get_bands(operator="electron")` on a path with named points). The same script gives the quiz pictures. It is a second figure next to `nambu_bands`, which shows the chain.
- Old figures of the page that break the plot rules: `nambu_bands` has no tick numbers, and its caption lacks $t=1$, $\mu=-1$ and $\Delta=0.45$ of the script. Left and reported. `nambu_blocks` is a drawing of matrices and is fine.
- Also: the sentence "Without it, the two spin blocks would mix through a Pauli matrix" stays as it is until the lecturer picks, see "Open for the lecturer".

## 5.9 An example of a gap that opens independently of the dispersion and 5.10 Metal, gapped and nodal superconductor for one Fermi surface

File `09-an-example-of-a-gap-that-opens-independently-of-the-dispersion.md`, 1235 words, numbered equations none.

- Question of the page, and where we arrive: Does the gap of a uniform $\Delta$ depend on the band structure, and what changes when $\Delta(\mathbf k)$ has nodes? We arrive at a full gap for any $\varepsilon(\mathbf k)$ and any $\mu$, and at three outcomes for one Fermi surface, which are metal, full gap and nodal.
- Main result for the key box: one box at 5.10, with the unnumbered display $\min E=\min_{\varepsilon(\mathbf k)=0}|\Delta(\mathbf k)|$ and one sentence on the three outcomes.
- Equation of another page that it starts from, for the recall box: (5.9).
- Derivation told in words, for a steps fold: none, the result is read from [(5.9)](#eq-5-9) in one line.
- Lab box, with the source and the number that the source states: magic-angle twisted trilayer graphene by STM, with [this article](https://www.nature.com/articles/s41586-022-04715-z), the notebook source of the cell "Gapped and nodal superconducting orders", stored with its arXiv abstract. The source states "More strikingly, in a density window spanning two to three holes per moire unit cell, spectroscopic signatures of superconductivity are manifest as pronounced dips in the tunneling conductance at the Fermi level accompanied by coherence peaks that become gradually suppressed at elevated temperatures and magnetic fields." and "The observed evolution of the conductance with doping is consistent with a gate-tunable transition from a gapped to a nodal superconductor, which we show theoretically is compatible with a sharp transition from a Bardeen-Cooper-Schrieffer (BCS) to a Bose-Einstein condensation (BEC) superconductor with a nodal order parameter." The box says "consistent with", as the source does. The number is a filling written in words, with no unit that `labsource.py` knows, so the lint does not check it and gives a `lab-number` warning, and the builder checks it by hand.
- Pen-and-paper problem: The square lattice at $\mu=-t$ and the d-wave gap [(5.13)](#eq-5-13). Find the points of the Fermi surface where the gap vanishes. The answer is $(\pm k_0,\pm k_0)$ with $\cos k_0=1/4$, so $k_0=1.318$. It ends on the momenta where ARPES or STM look for the gapless points.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the pocket at $X$ has a `quiz-ref`, since its feedback names Figure 5.2c. Say it in words, as the pocket picture of the right option already shows it. New picture quiz, three curves of the smallest $E$ along the Fermi surface against the angle $\theta$, flat at zero, flat at $\Delta_0$ and with four zeros, with the question which one is a nodal superconductor. New quiz with equations as options, "Which $\Delta(\mathbf k)$ gaps every Fermi surface of the square lattice?", with $\Delta_0$, $\Delta_0(\cos k_x-\cos k_y)$ and $\Delta_0(\cos k_x+\cos k_y)$.
- Figures to add, each with its pyqula script or the reason for numpy: the BdG bands of the triangular lattice with a uniform $\Delta$ at three chemical potentials, from the pyqula script `g2_swave_triangular_mu.py` (`h.add_pairing(mode="swave", delta=0.4)`, bands along $\Gamma$, $K$, $M$, $\Gamma$ with `operator="electron"`). It backs the sentence of the page on the triangular lattice. The quiz curves are numpy, since they draw a formula and are no calculation.
- Old figures of the page that break the plot rules: `gap_any_mu` has no ticks at 0, the three $k_F$ and $\pi$ on $k$, and at $0.3$ on $E$, and no unit on $E$. `pockets_nodes` is a map of the square zone with its axes switched off, with no $k_x$ and $k_y$. The zone is a square, so the rule of the hexagon does not apply. Both are left and reported.
- Also: the text names "the physical red band and the spurious blue mirror band", colors that no figure of the page has, and `nambu_bands` draws the electron band blue and the hole band red. The builder writes "electron band" and "hole band".

## 5.11 The general pairing Hamiltonian and its symmetry classification

File `11-the-general-pairing-hamiltonian-and-its-symmetry-classification.md`, 842 words, numbered equations (5.10), (5.11), (5.12).

- Question of the page, and where we arrive: $\Delta$ can depend on momentum and on spin. Which combinations does Fermi statistics allow, and what sorts them? We arrive at the antisymmetry [(5.11)](#eq-5-11) and at the rule [(5.12)](#eq-5-12), singlet with even parity and triplet with odd parity.
- Main result for the key box: [(5.12)](#eq-5-12), with one sentence that names [(5.11)](#eq-5-11) as its cause.
- Equation of another page that it starts from, for the recall box: (5.4), the onsite pairing, which is the simplest singlet.
- Derivation told in words, for a steps fold: "From the anticommutation of the operators to (5.11)". We relabel $\mathbf k\to-\mathbf k$ and exchange $\sigma_1$ and $\sigma_2$ in [(5.10)](#eq-5-10), and the symmetric part cancels. Only the antisymmetry is used, which does not depend on the sign and the factor of [(5.10)](#eq-5-10).
- Lab box, with the source and the number that the source states: Sr$_2$RuO$_4$, with [this article](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.80.161), abstract pasted from the APS page. The source states "We report measurements of chemical composition and of transport properties in the same single crystals of Sr2RuO4 which show that nonmagnetic impurities destroy superconductivity when the residual resistivity exceeds 1 μΩ cm, i.e., when the carrier mean free path falls below the superconducting coherence length." and "This behavior strongly supports models of non-s-wave (e.g., p- or d-wave) pairing in this layered perovskite oxide." The box says non-s-wave and not triplet. The tool does not know the unit μΩ cm, so the lint does not check the number and gives a `lab-number` warning. This box goes in only after the lecturer picks on the sentence of Anderson's theorem, since the source says that d-wave pairing is suppressed too.
- Pen-and-paper problem: Show that the onsite term $c_{n\uparrow}c_{n\uparrow}$ vanishes, and that the bond pairing $\Delta\sum_nc_{n\uparrow}c_{n+1,\uparrow}+\text{h.c.}$ of a chain gives $|\Delta(k)|=2\Delta|\sin k|$, which is odd, so a triplet. Only the modulus is asked, since the sign of $i$ is the open point on (5.20).
- Quizzes to rewrite, and a picture question or equations as options: keep the quiz on $\sin k_x$. New picture quiz, three stem plots of the pair amplitude $\Delta(r)$ of a chain, one stem at $r=0$, two equal stems at $\pm1$, and two stems of opposite sign at $\pm1$, with the question which one must be a spin triplet. The answer uses only that the amplitude is odd.
- Figures to add, each with its pyqula script or the reason for numpy: the three quiz pictures in numpy, since they are a Fourier transform and no calculation for pyqula, with a helper `_g3_pairfun.py`.
- Old figures of the page that break the plot rules: `pair_function` has the $r$ axis and no $\Delta(r)$ axis with ticks. Left and reported. Its p-wave panel uses $2i\Delta_0\sin k$ "as in (5.20)", so the signs of its stems follow the open point on (5.20).

## 5.12 Building a spin-triplet superconductor out of a magnet

File `12-building-a-spin-triplet-superconductor-out-of-a-magnet.md`, 814 words, numbered equations none.

- Question of the page, and where we arrive: The triplet order is fragile, so how can we build one on purpose? We arrive at an exchange field that makes a $\uparrow\downarrow$ pair cost $2h$, so that with an attraction the equal-spin pairing, odd in $k$, can win, with edge modes on a ribbon.
- Main result for the key box: the unnumbered display $\varepsilon_{\uparrow,\downarrow}(k)=\varepsilon(k)\mp h$, with one sentence that the $\downarrow$ partner of an $\uparrow$ electron on its Fermi surface sits $2h$ above the Fermi level, and two $\uparrow$ electrons do not pay this. The condition on $h$ stays out of the box until the lecturer picks, see "Open for the lecturer".
- Equation of another page that it starts from, for the recall box: (5.12).
- Derivation told in words, for a steps fold: "The energy of a singlet pair in an exchange field". Since $\varepsilon(-k)=\varepsilon(k)$, the partner at $-k_{F\uparrow}$ has $\varepsilon_\downarrow=\varepsilon_\uparrow+2h=2h$.
- Lab box, with the source and the number that the source states: magic-angle twisted trilayer graphene in an in-plane field, with [this article](https://www.nature.com/articles/s41586-021-03685-y), the notebook source of the cell "Interaction-induced spin-triplet superconductivity", stored with its arXiv abstract. The source states "Here, we show that magic-angle twisted trilayer graphene (MATTG) exhibits superconductivity up to in-plane magnetic fields in excess of 10 T, which represents a large (2~3 times) violation of the Pauli limit for conventional spin-singlet superconductors." and "These findings suggest that the superconductivity in MATTG is likely driven by a mechanism resulting in non-spin-singlet Cooper pairs, where the external magnetic field can cause transitions between phases with potentially different order parameters." The probe is transport. The box says "suggest" and "non-spin-singlet", and not triplet. Our reading, marked, is that the Pauli limit is the field where the mismatch $2h$ of the page breaks a singlet. A Zeeman energy in meV is ours and goes in `ours`.
- Pen-and-paper problem: A chain with $t=1$, $\mu=0$ and $h=0.5$. Find $k_{F\uparrow}$, $k_{F\downarrow}$ and the energy of the $\downarrow$ partner of an $\uparrow$ electron at $k_{F\uparrow}$. The answer is $1.823$, $1.318$, a difference of $0.505$, and the partner at $2h=1.0$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz of line 12 (23 words) as two short sentences with $\varepsilon_\sigma(k)=-2t\cos k-\mu\mp h$ in the question, same point. New picture quiz, three band plots of the chain with exchange fields that leave both spins, or only one, at the Fermi level, with the question in which chain only $\uparrow\uparrow$ pairs can form. The bands come from the pyqula script `g3_exchange_chain_bands.py` with `h.add_exchange`, the notebook cell of the try-it box, and the size of the splitting comes from the conventions sheet.
- Figures to add, each with its pyqula script or the reason for numpy: the quiz pictures only.
- Old figures of the page that break the plot rules: `spin_split_pairing` has no tick numbers, at 0 and $2h=1.2$ on $E$ and at the Fermi momenta on $k$, and its caption lacks $t=1$, $\mu=0$ and $h=0.6$ of the script. Left and reported.

## 5.13 Nodal singlet order, d-wave pairing in the cuprates and the angular-momentum expansion

File `13-nodal-singlet-order-d-wave-pairing-in-the-cuprates-and-the-angular-momentum-expansion.md`, 1217 words, numbered equations (5.13), (5.14).

- Question of the page, and where we arrive: Can a singlet gap vanish on part of the Fermi surface, and how do we name the patterns? We arrive at the d-wave gap [(5.13)](#eq-5-13) with nodes on the diagonals, at the expansion [(5.14)](#eq-5-14) by counting lobes, and at the f-wave order of the triangular lattice, which is odd and so a triplet.
- Main result for the key box: [(5.13)](#eq-5-13), with the sentence that it vanishes on $k_x=\pm k_y$, so the spectrum is gapless where the Fermi surface crosses the diagonals.
- Equation of another page that it starts from, for the recall box: (5.9) and (5.12).
- Derivation told in words, for a steps fold: "From pairing on the bonds to the d-wave gap (5.13)". A singlet pairing of opposite sign on the bonds along $x$ and along $y$ gives $\cos k_x-\cos k_y$ up to a factor, which vanishes where $\cos k_x=\cos k_y$. The fold uses the relative sign of the two bonds and no overall sign.
- Lab box, with the source and the number that the source states: rings of YBa$_2$Cu$_3$O$_{7-\delta}$, with [this article](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.73.593), abstract pasted from the APS page. The source states "The magnetic flux threading these rings at 4.2 K is measured by employing a scanning superconducting quantum interference device microscope." and "Spontaneous magnetization of a half magnetic flux quantum, Φ0/2 = h/4e has been observed in the 3-junction ring, but not in the 2-junction rings." It links [(5.1)](#eq-5-1). Our reading, marked, is that the sign change of $\Delta_d$ between the lobes adds a phase $\pi$ around a ring with an odd number of sign changes. The $130$ K of the page agrees with the $133$ K at ambient pressure that the stored abstract of sulfur hydride states for the cuprates, so nothing changes there.
- Pen-and-paper problem: Show that the extended s-wave gap $\Delta_0(\cos k_x+\cos k_y)$ is $\Delta_0/2$ everywhere on the Fermi surface of the square lattice at $\mu=-t$, and zero everywhere at $\mu=0$. The answer is $\Delta_0/2$ and $0$. It ends on the node ring and the Fermi surface, as the caption of the gap symmetry figure says.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz of line 30 (16 words) into two sentences, with $\Delta\propto\cos3\theta$ in the question, same point. New picture quiz, three BdG band plots of the triangular lattice along $\Gamma$, $K$, $M$, $\Gamma$, with no pairing, with `mode="swave", delta=0.4` and with `mode="nodal_fwave", delta=0.2`, with the question which one is a nodal superconductor. They come from the pyqula script `g3_triangular_pairing_bands.py`, the notebook cell of the try-it box.
- Figures to add, each with its pyqula script or the reason for numpy: the quiz pictures only.
- Old figures of the page that break the plot rules: `dwave_nodes` (a) is a map of the zone with its axes switched off, with no $k_x$ and $k_y$, and in (b) the axis $E_\min$ lacks "in units of $\Delta_0$". Left and reported.

## 5.14 Same gap and different topology in trivial s-wave and chiral p-wave pairing

File `14-same-gap-and-different-topology-in-trivial-s-wave-and-chiral-p-wave-pairing.md`, 1205 words, numbered equations (5.15).

- Question of the page, and where we arrive: Two superconductors have the same gap on the same Fermi surface. Can they still be different phases? We arrive at the Chern number of the BdG bands, $0$ for s-wave and $\pm2$ for the chiral p-wave [(5.15)](#eq-5-15), from the winding of the phase of $\Delta(\mathbf k)$, and only the second one has edge branches.
- Main result for the key box: [(5.15)](#eq-5-15), with the sentence that $C=0$ for s-wave and $C=\pm2$ for $p+ip$, one unit from each spin block.
- Equation of another page that it starts from, for the recall box: (3.4).
- Derivation told in words, for a steps fold: "Why the winding of Delta gives one Chern unit per block". Each block [(5.8)](#eq-5-8) is a $2\times2$ matrix $\mathbf d\cdot\boldsymbol\tau$, and near a pocket around $\Gamma$ the phase of $\Delta\approx\Delta_0(k_x+ik_y)$ winds once, so $\mathbf d$ covers the sphere once when $\mu$ is inside the band, as for the massive Dirac case of Section 3.10. The fold states $|C|=1$ per block, and a sign only from the conventions sheet.
- Also: the paragraph of line 31 (173 words) is split after "as a state with Chern number $\pm 2$ must have".
- Lab box, with the source and the number that the source states: none. No material has an established chiral p-wave state. The notebook source of the cell "Edge states of an artificial topological superconductor", [CrBr$_3$ on NbSe$_2$](https://www.nature.com/articles/s41586-020-2989-y), fits the edge modes, and it is stored, but its abstract, also the published one, has no number, so there is no box.
- Pen-and-paper problem: The phase of $\Delta_0(\sin k_x+i\sin k_y)$ on a circle of radius $0.3$ around $\Gamma$. Show that it winds once, and minus once for $p-ip$, and that $|\Delta|$ stays between $0.296\Delta_0$ and $0.298\Delta_0$, so the gap is the same as for an s-wave gap of $0.3\Delta_0$.
- Quizzes to rewrite, and a picture question or equations as options: rewrite the quiz of line 16 (16 words) with $\Delta_s=\Delta_0$ and $\Delta_{p+ip}=\Delta_0(\sin k_x+i\sin k_y)$ as a display, same point. Keep the quiz on $p_x-ip_y$. New picture quiz, three ribbon spectra of the triangular lattice for s-wave, chiral p-wave and nodal f-wave pairing, with the states colored by their position across the ribbon, and the question which ribbon has $C=\pm2$.
- Figures to add, each with its pyqula script or the reason for numpy: the ribbon spectra of s-wave and chiral p-wave pairing next to each other, from the pyqula script `g4_pwave_ribbon.py`, with `h.add_onsite(-3.0)`, `h.add_pairing(mode=..., delta=0.4)`, a ribbon and `operator="yposition"`, and `h.get_chern()` of the bulk in the caption. The same script gives the quiz pictures. The ribbon recipe of `RECIPES.md` is for the honeycomb lattice, so the ribbon of the triangular lattice is checked against the notebook cell "Trivial and topological superconducting order parameters, edge spectra".
- Old figures of the page that break the plot rules: none, `s05f04_topology` and `s03f01_chiraledge` are converted figures.

## 5.15 Majorana bound states and how to split an electron into two Majoranas

File `15-majorana-bound-states-and-how-to-split-an-electron-into-two-majoranas.md`, 720 words, numbered equations (5.16), (5.17), (5.18).

- Question of the page, and where we arrive: Can a quasiparticle in a material be its own antiparticle? We arrive at [(5.17)](#eq-5-17) and [(5.18)](#eq-5-18), every fermion is two Majoranas, and they can come apart only where the BdG states mix electrons and holes.
- Main result for the key box: [(5.17)](#eq-5-17), with one sentence on $\gamma^2=1$ and $\{\gamma_A,\gamma_B\}=0$, and [(5.18)](#eq-5-18) named.
- Equation of another page that it starts from, for the recall box: (5.6), the Nambu spinor, which puts $c$ and $c^\dagger$ in one spinor.
- Derivation told in words, for a steps fold: "From the anticommutator of c to the Majorana algebra". We compute $\gamma_A^2$, $\gamma_B^2$ and $\{\gamma_A,\gamma_B\}$ from $\{c,c^\dagger\}=1$ and invert to [(5.18)](#eq-5-18).
- Lab box, with the source and the number that the source states: none, the page is about operators. The measured end modes come in Section 5.17 and Section 5.19.
- Pen-and-paper problem: Two Majoranas with $H=\tfrac{i\varepsilon}{2}\gamma_A\gamma_B$. Show with $i\gamma_A\gamma_B=2c^\dagger c-1$ that the levels are $\pm\varepsilon/2$, so the splitting is $\varepsilon$. For $\varepsilon=0.2$ the levels are $\pm0.1$. It ends on the splitting of the two end modes of Section 5.17.
- Quizzes to rewrite, and a picture question or equations as options: keep both quizzes. New quiz with equations as options, "Which operator is Hermitian and squares to one?", with $c+c^\dagger$, $c-c^\dagger$ and $c^\dagger c$.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `majorana_halves` is a drawing.

## 5.16 The Kitaev chain as the minimal model with isolated Majoranas

File `16-the-kitaev-chain-as-the-minimal-model-with-isolated-majoranas.md`, 988 words, numbered equations (5.19), (5.20), (5.21).

- Question of the page, and where we arrive: What is the simplest Hamiltonian where the two halves of an electron end up far apart? We arrive at the Kitaev chain [(5.19)](#eq-5-19), its odd pairing [(5.20)](#eq-5-20), and the form [(5.21)](#eq-5-21) at $\Delta=t$ and $\mu=0$, where $\gamma_1$ and $\gamma_{2N}$ are absent.
- Main result for the key box: [(5.21)](#eq-5-21), with the sentence that $\gamma_1$ and $\gamma_{2N}$ do not appear, so they cost no energy and sit at the two ends.
- Equation of another page that it starts from, for the recall box: (5.18).
- Derivation told in words, for a steps fold: "From the Kitaev chain (5.19) to the Majorana form (5.21)". We put $c_n=\tfrac12(\gamma_{2n-1}+i\gamma_{2n})$ in one bond first, collect the terms $\gamma_{2n}\gamma_{2n+1}$ and $\gamma_{2n-1}\gamma_{2n+2}$, and the second cancels at $\Delta=t$. Each step is checked against a matrix of two sites. No fold for [(5.20)](#eq-5-20) until the lecturer picks its sign.
- Also: the paragraph of line 17 (174 words) is split after "completely decoupled from the rest of the system".
- Lab box, with the source and the number that the source states: none. A two-site Kitaev chain in InSb quantum dots, tuned to $\Delta=t$ (DOI 10.1038/s41586-022-05585-1, arXiv 2206.08045), fits exactly, but its abstract, also the published one, has no number, so it is not stored and there is no box.
- Pen-and-paper problem: With the bond fermion $d_n=\tfrac12(\gamma_{2n}+i\gamma_{2n+1})$, show that the term $it\gamma_{2n}\gamma_{2n+1}$ is $t(2d_n^\dagger d_n-1)$, so filling the bond costs $2t$. This is the flat bulk energy $E=2t$ of the quiz.
- Quizzes to rewrite, and a picture question or equations as options: keep the quiz on the flat band. New quiz with equations as options, "Which Hamiltonian is (5.19) at $\Delta=t$ and $\mu=0$?", with $it\sum\gamma_{2n}\gamma_{2n+1}$, $it\sum\gamma_{2n-1}\gamma_{2n}$ and $it\sum\gamma_{2n-1}\gamma_{2n+2}$. New picture quiz, three level spectra of open chains of 10 sites, at $\Delta=t$ and $\mu=0$, at $\Delta=0$ and $\mu=0$, and at $\Delta=t$ and $\mu=2.5t$, with the question which one has two levels pinned at zero inside a gap.
- Figures to add, each with its pyqula script or the reason for numpy: the levels of the open chain at $\Delta=t$ and $\mu=0$, two at zero and the rest at $\pm2t$, with a helper `_g5_kitaev.py` that the quiz pictures also use. Until the lecturer picks on the Kitaev figures, it is numpy from the exact chain [(5.19)](#eq-5-19).
- Old figures of the page that break the plot rules: none, `s05f05_kitaev` and `s03f03_ssh` are converted figures.

## 5.17 Topological zero modes with periodic and open boundaries

File `17-topological-zero-modes-with-periodic-and-open-boundaries.md`, 1129 words, numbered equations (5.22).

- Question of the page, and where we arrive: Do the end Majoranas survive away from $\Delta=t$ and $\mu=0$, and what sets the end of the phase? We arrive at [(5.22)](#eq-5-22), topological for $|\mu|<2t$, with end modes that a finite chain splits by an energy that falls fast with its length.
- Main result for the key box: [(5.22)](#eq-5-22), with the sentence that the bulk gap closes at $|\mu|=2t$, at $k=0$ or $k=\pi$.
- Equation of another page that it starts from, for the recall box: (5.19).
- Derivation told in words, for a steps fold: "Where the bulk gap of the Kitaev chain closes". $E(k)^2=(2t\cos k+\mu)^2+4\Delta^2\sin^2k$ vanishes only where $\sin k=0$ and $2t\cos k+\mu=0$, so at $\mu=\mp2t$, for any $\Delta\neq0$. It uses only $|\Delta(k)|$.
- Also: the paragraph of line 3 (165 words) is split after "instead of an ordinary Bloch Hamiltonian".
- Lab box, with the source and the number that the source states: InSb nanowires with a NbTiN contact, with [this article](https://www.science.org/doi/10.1126/science.1222360), stored with its arXiv abstract. The source states "In the presence of magnetic fields of order 100 mT we observe bound, mid-gap states at zero bias voltage." and "Our observations support the hypothesis of Majorana fermions in nanowires coupled to superconductors." The probe is the tunneling conductance. The box says "support the hypothesis", as the source does. Our reading, marked, is that a state that stays at zero while the gate changes is what [(5.22)](#eq-5-22) predicts inside the window.
- Pen-and-paper problem: Find the smallest bulk energy for $\Delta=0.5t$ and $\mu=t$. The answer is $\sqrt{2/3}\,t=0.82t$ at $\cos k=-2/3$, the value of the second quiz and of the first bulk level of the splitting figure.
- Quizzes to rewrite, and a picture question or equations as options: keep both quizzes. New picture quiz, three weight profiles of the lowest state of open chains with 40 sites and $\Delta=0.5t$ at three values of $\mu$, with the question which chain is in the trivial phase. The pictures come from `_g5_kitaev.py`.
- Figures to add, each with its pyqula script or the reason for numpy: none new. `kitaev_spectrum`, `zero_mode_profile` and `majorana_splitting` are numpy and assert numbers of the exact chain, $0.011t$ at $N=8$, $2\times10^{-5}t$ at $N=20$ and $0.51t$ at $\mu=2.5t$, and they stay as they are. A pyqula figure with a download here is part of the pick on the Kitaev figures.
- Old figures of the page that break the plot rules: `kitaev_spectrum` has no tick numbers on $E$ and no unit $t$ on it. `zero_mode_profile` has no ticks on the sites (1 and 40) or on the weight, and its weight axis is a free text. Both are left and reported. `majorana_splitting` has its ticks and is fine.

## 5.18 Engineering a topological superconductor from a quantum spin Hall insulator

File `18-engineering-a-topological-superconductor-from-a-quantum-spin-hall-insulator.md`, 984 words, numbered equations none.

- Question of the page, and where we arrive: Chiral and p-wave superconductors are rare. Can we build the Kitaev chain from parts that exist? We arrive at a quantum spin Hall edge with two magnets and an s-wave superconductor, a wire that is spinless when we count channels, with Majoranas where the gap of the magnet meets the gap of pairing.
- Main result for the key box: the unnumbered display $E(k=0)=\pm h\pm\Delta$ at $\mu=0$, with the sentence that the gap closes at $h=\Delta$, so a region gapped by pairing and a region gapped by the magnet are different phases, and a Majorana sits at their boundary. This is the content of `helical_edge_gap`, which asserts it.
- Equation of another page that it starts from, for the recall box: (5.19).
- Derivation told in words, for a steps fold: "The levels of the helical edge at k=0". At $k=0$ and $\mu=0$ the edge Hamiltonian is $h\sigma_x+\Delta\tau_x$, the two terms commute, and the levels are $\pm h\pm\Delta$.
- Lab box, with the source and the number that the source states: monolayer WTe$_2$, with two sources in two sentences. [This article](https://www.science.org/doi/10.1126/science.aan6003), stored for Session 3 in `sources/.full/session03/wu2018_science.aan6003.txt`, states "Here we report the observation of the QSHE in monolayer WTe2 at temperatures up to 100 Kelvin." [This article](https://www.nature.com/articles/s41567-020-0816-x), stored with its arXiv abstract, has no number and states "At the edge of the WTe2 monolayer, we show that the superconducting gap coexists with the characteristic spectroscopic signature of the QSH edge state." The 100 K is the number of the quantum spin Hall state, in another sample, and not of the proximity gap, and the box says so. The probes are transport and STM. The box writes "monolayer WTe$_2$" and not "1T′", for the reason in "Before the builders start".
- Pen-and-paper problem: The edge with $\Delta=0.3$ and $\mu=0.4$. Show that the gap closes at $h=\sqrt{\Delta^2+\mu^2}$. The answer is $0.5$, and on a grid of $k$ the gap over all momenta closes there.
- Quizzes to rewrite, and a picture question or equations as options: keep the quiz on the spinless segment. New quiz with equations as options, the levels at $k=0$ and $\mu=0$, with $\pm h\pm\Delta$, $\pm\sqrt{h^2+\Delta^2}$ and $\pm(h+\Delta)$. New picture quiz, three edge spectra, the bare helical edge, the edge with a magnet and the edge with pairing, with the question which gap comes from the magnet, in numpy from the edge model of `helical_edge_gap`.
- Figures to add, each with its pyqula script or the reason for numpy: the gap of the artificial topological superconductor of the notebook against the exchange field, with the Chern number on both sides, from the pyqula script `g6_artificial_tsc.py` (triangular lattice with `h.add_rashba`, `h.add_zeeman`, `h.add_swave(0.3)` and `h.get_chern()`), the cell "Topological phase transition as a function of the exchange field", where the try-it box says that the gap closes close to `J=0.42`. The caption says that this is the model of the notebook, a two-dimensional gas with spin-orbit coupling, and not the edge of the page. The quiz pictures are numpy, since they are a continuum edge model that pyqula does not have.
- Old figures of the page that break the plot rules: `helical_edge_gap` has no tick numbers on $E$, at $\pm0.7$ in (a) and $\pm1$ in (b), and its caption lacks $h=0.7$ of panel (a). Left and reported.

## 5.19 Topological quantum computing with Majoranas

File `19-topological-quantum-computing-with-majoranas.md`, 931 words, numbered equations (5.23).

- Question of the page, and where we arrive: Why would we want Majoranas for a quantum computer? We arrive at four Majoranas that make two modes, a qubit in the sector of even parity, the braid [(5.23)](#eq-5-23), and braids that share a Majorana and do not commute.
- Main result for the key box: [(5.23)](#eq-5-23), with the sentence that $U_{12}$ and $U_{23}$ do not commute while $U_{12}$ and $U_{34}$ do. Both are checked with matrices of two fermion modes.
- Equation of another page that it starts from, for the recall box: (5.18).
- Derivation told in words, for a steps fold: "What the braid (5.23) does". Since $(\gamma_1\gamma_2)^2=-1$, $U_{12}=(1+\gamma_1\gamma_2)/\sqrt2$, and then $U_{12}\gamma_1U_{12}^\dagger=-\gamma_2$ and $U_{12}\gamma_2U_{12}^\dagger=\gamma_1$. These are checked with matrices, and the fold takes its signs from such a check.
- Also: the paragraph of line 29 (173 words) is split after "Exchanges of disjoint pairs, such as $(1,2)$ and $(3,4)$, commute instead."
- Lab box, with the source and the number that the source states: an InAs-Al nanowire device, with [this article](https://www.nature.com/articles/s41586-024-08445-2), stored from arXiv 2401.09549 with the published abstract pasted from the Nature page. The published text states "The large capacitance shift and long poisoning time enable a parity measurement with an assignment error probability of 1%.", "From the time traces of the quantum-capacitance measurements, we extract a dwell time in the two associated states that is longer than 1 ms at in-plane magnetic fields of approximately 2 T." and "We discuss the interpretation of our measurements in terms of both topologically trivial and non-trivial origins." The probe is the quantum capacitance. The box says that the article discusses both origins and does not say that the modes are Majoranas. The separation of 3 μm and the reading as Majorana modes are only in the arXiv text, so they stay out. The unit ms is not one that the tool knows, so only $1\%$ and $2$ T are checked. The lecturer may want to see this box before it goes in, since the source itself leaves the origin open.
- Pen-and-paper problem: Show that $U_{12}^4=-1$ for [(5.23)](#eq-5-23), and that two braids send $\gamma_1$ to $-\gamma_1$. The answer is $-1$. It ends on why four exchanges give the fermion sign.
- Quizzes to rewrite, and a picture question or equations as options: keep both quizzes. New quiz with equations as options, "What is $(\gamma_1\gamma_2)^2$?", with $-1$, $1$ and $0$.
- Figures to add, each with its pyqula script or the reason for numpy: none, the braid is no calculation for pyqula.
- Old figures of the page that break the plot rules: none, `four_majoranas` and `braid_order` are drawings.

## 5.20 Closing summary

File `20-closing-summary.md`, 789 words, numbered equations none.

- Question of the page, and where we arrive: none new. The page already opens with the three tools from before, and it is the closing page.
- Main result for the key box: none, the closing page.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none.
- Pen-and-paper problem: none.
- What the student can now do, a list after the paragraph on Session 6, as on the closing page of Session 3, each item with its section. Compute the flux quantum and say where the 2 comes from (5.2). Decouple an attractive interaction in the pairing channel and say why $\Delta$ vanishes for $U>0$ (5.5). Say why a superconductor has a fixed parity and no fixed electron number (5.6, 5.7). Write the BdG matrix of one band and read the gap $2|\Delta|$ at the Fermi points (5.8, 5.9). Tell a full gap from a nodal one from where the nodes of $\Delta(\mathbf k)$ meet the Fermi surface (5.10, 5.13). Decide from the parity of $\Delta(\mathbf k)$ whether a pairing is singlet or triplet (5.11, 5.12). Tell s-wave from chiral p-wave by the winding of $\Delta(\mathbf k)$ and the Chern number (5.14). Find the end Majoranas of a Kitaev chain and the window $|\mu|<2t$ (5.16, 5.17). Name the parts that make a Kitaev chain out of a quantum spin Hall edge (5.18). Say why braids that share a Majorana do not commute (5.19).
- Quizzes to rewrite, and a picture question or equations as options: keep the quiz on the bond pairing. New quiz with equations as options, "Which pairing is a spin triplet?", with $\Delta_0$, $\Delta_0(\cos k_x-\cos k_y)$ and $\Delta_0(\sin k_x+i\sin k_y)$. New picture quiz, three drawings of the phase of $\Delta(\mathbf k)$ around a pocket, constant, winding once, and changing sign four times, with the question which one gives $C=\pm2$ with two spin blocks.
- Figures to add, each with its pyqula script or the reason for numpy: the quiz drawings only, in numpy, owned by this page.
- Old figures of the page that break the plot rules: none, `s05f04_topology` is a converted figure.

## Candidates for the lab boxes

These are the "In the lab" cells of the notebook and the articles found for the other pages. Every one that a block
uses is stored with `webnotes/labsource.py`, and each planned number was found with the function `find` of the
tool, in the tracked file for the arXiv abstracts and in the full copy for the pasted texts.

- Spin triplet superconductivity in twisted graphene trilayers under a magnetic field, https://www.nature.com/articles/s41586-021-03685-y, stored with arXiv 2103.12083, the box of Section 5.12 (10 T).
- Nodal superconductivity in twisted graphene trilayers, https://www.nature.com/articles/s41586-022-04715-z, stored with arXiv 2109.12127, the box of Section 5.10 (a filling in words, `lab-number` warning).
- Topological superconductivity in NbSe2/CrBr3, https://www.nature.com/articles/s41586-020-2989-y, stored with arXiv 2002.02141, no number, so no box.
- The ac Josephson effect, https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.18.287, abstract pasted, Section 5.2.
- Sulfur hydride, https://www.nature.com/articles/nature14964, stored with arXiv 1506.08190 and the published abstract pasted, Section 5.4.
- The parity effect of an aluminium island, https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.69.1997, abstract pasted, Section 5.6.
- Sr2RuO4 and disorder, https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.80.161, abstract pasted, Section 5.11 (μΩ cm, `lab-number` warning).
- The half flux quantum of YBa2Cu3O7, https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.73.593, abstract pasted, Section 5.13.
- Zero-bias states in InSb nanowires, https://www.science.org/doi/10.1126/science.1222360, stored with arXiv 1204.2792, Section 5.17.
- The proximity gap of the WTe2 edge, https://www.nature.com/articles/s41567-020-0816-x, stored with arXiv 1903.00493, no number, used next to the Session 3 source in Section 5.18.
- The parity measurement in InAs-Al, https://www.nature.com/articles/s41586-024-08445-2, stored from arXiv 2401.09549 with the published abstract pasted, Section 5.19.
- Two articles were read and not stored, since their abstracts have no number. They are the Bogoliubov dispersion by ARPES (Phys. Rev. Lett. 90, 217002) and the two-site Kitaev chain (DOI 10.1038/s41586-022-05585-1). The flux quantization articles of Phys. Rev. Lett. 7, 43 and 7, 51 have no abstract on the APS page.

## Builder groups

Each group is at most three pages, in the order of the pages. The index is not edited, so it is in no group. A new
file carries the prefix of its group, and no block uses a new file of another group.

- `g1`, pages 5.1, 5.2 and 5.4 (`01`, `02`, `04`). 5.1 and 5.4 start from the same Hamiltonian of Session 1, and
  5.4 owns `g1_meanfield_swave_chain.py`. 5.2 owns `_g1_fieldlines.py`.
- `g2`, pages 5.6, 5.8 and 5.9 (`06`, `08`, `09`). 5.6 and 5.8 start from [(5.4)](#eq-5-4), and 5.8 and 5.9 share
  the BdG bands and [(5.9)](#eq-5-9). 5.8 owns `g2_nambu_square.py`, and 5.9 owns `g2_swave_triangular_mu.py`.
- `g3`, pages 5.11, 5.12 and 5.13 (`11`, `12`, `13`). They share [(5.12)](#eq-5-12) and the gap symmetry figure.
  This group owns `_g3_pairfun.py`, `g3_exchange_chain_bands.py` and `g3_triangular_pairing_bands.py`. The d-wave
  formula is drawn also in 5.9, by `g2`, with no shared file.
- `g4`, pages 5.14 and 5.15 (`14`, `15`). 5.14 owns `g4_pwave_ribbon.py`.
- `g5`, pages 5.16 and 5.17 (`16`, `17`). They share the exact chain [(5.19)](#eq-5-19) and own `_g5_kitaev.py`.
- `g6`, pages 5.18, 5.19 and 5.20 (`18`, `19`, `20`). 5.18 owns `g6_artificial_tsc.py`, and 5.20 owns its own quiz
  drawings.

## Open for the lecturer

The lecturer decided on 2026-11-22 to "Fix old-text errors, ask the rest". The points of the builders, of the fixers,
of the rechecks, of this section and of the conventions sheet were merged into 42 distinct points. The 18 points of the
first list were false as written, or contradicted another sentence of the session, and their correction changes no
numbered equation, no convention, no converted figure and no decision of the lecturer. They are corrected on the web,
each checked with a calculation of its own and asserted in `webnotes/checks/session05/`. The 24 points of the second
list were the lecturer's. They were decided later on 2026-11-22, the sign of (5.20) by the lecturer and the other 23 by
the coordinator with the rule of that day, since the lecturer said "ask me the top 5, other you decide by yourself". They
are now the list "Decided on 2026-11-22", with the three points that the rule leaves out in "Not applied", and the changes
that they made on the web are at the end of the first list. An independent check of these changes, later on 2026-11-22,
found two more sentences of the old text that the decisions left false or stronger than the new text, on pages `08` and
`18`, and they are the last two items of the first list. The same check sharpened three of the new texts, on pages `12`, `16`
and `18`, and their items give the wording as it is now. No numbered equation changed. The line numbers of the `.tex`
are those of `lecture_notes/src/sessions/session05.tex` on 2026-11-22. The `.tex` is not changed in this pass, so until
the first list is carried over the PDF keeps the old wording in these places.

### Corrected on the web, to carry over to the .tex

- Page `01`, Section 5.1, third feedback of the first quiz. Old "The Bogoliubov quasiparticle of a superconductor is a
  fraction of an electron, and it is an exact eigenstate of the mean-field Hamiltonian [(5.4)](#eq-5-4)." New "A
  Majorana state of a superconductor is a fraction of an electron, and it is a zero-energy state of a mean-field
  Hamiltonian with pairing, which is bilinear as [(5.4)](#eq-5-4) is." Not in the `.tex`, since the quizzes are
  web-only. Asserted in `g1_01`.
- Pages `09`, `17` and `19`, the word "Schematic" before a link `[](#sch:...)`, which rendered as "Schematic Schematic
  5.8", "5.16" and "5.21". The word is removed. On page `09` the sentence is now "This is what [](#sch:s05:gap_any_mu)
  shows for a chain and three chemical potentials.", since the lint joins a sentence that starts with a link to the one
  before it. Not in the `.tex`, since the schematics are web figures.
- Page `09`, Section 5.9, first paragraph. Old "The gap opens at the minimum of $E(\mathbf k)$, which is where
  $\varepsilon(\mathbf k) = 0$, so on the original Fermi surface, and the minimum gap there is $|\Delta(\mathbf k)|$
  evaluated on that Fermi surface." New "For a uniform $\Delta$ the gap opens at the minimum of $E(\mathbf k)$, which is
  where $\varepsilon(\mathbf k) = 0$, so on the original Fermi surface, and the smallest quasiparticle energy there is
  $|\Delta|$." `.tex` lines 328 to 331. Asserted in `g2_09`.
- Page `09`, Section 5.10, first feedback of the quiz on the pocket at $X$. Old "so $|\Delta_d|\approx2\Delta_0$ and
  $E\geq2\Delta_0$ there." New "so $|\Delta_d|\approx2\Delta_0$ and $E$ is close to $2\Delta_0$ there." Not in the
  `.tex`. Asserted in `g2_09`, $1.876\le|\Delta_d|/\Delta_0<2$ on pockets of radius 0.1, 0.3 and 0.5.
- Page `06`, Section 5.7, changed by the builder in commit `033b84d` and listed here to carry over. Old "such as
  magnetic terms that depend on spin, spin-orbit coupling and any density-density interaction term", which put the
  quartic density term among the bilinear terms. New, in two sentences since 2026-11-22, "such as spin-orbit coupling
  and the magnetic terms that depend on spin. It also protects any density-density interaction term
  $c_i^\dagger c_i c_j^\dagger c_j$, which is quartic." `.tex` lines 236 and 237. No number, and `g2_06` checks that
  the density-density term keeps its phase.
- Page `12`, try-it box. Old "The two bands move apart from 2 to 4 at a fixed momentum, so each spin has its own Fermi
  momentum." New "The two bands move apart from 2 to 4 at a fixed momentum. At `1.0` each spin has its own Fermi
  momentum, and at `2.0` each band touches zero energy only at its edge." Not in the `.tex`. Asserted in `g3_12`.
- Page `13`, notebook box. Old header "Gapped and nodal superconducting orders" (Core), and old last sentence "The
  nodal $L=3$ (f-wave) case of the triangular lattice discussed above is also in this section of the notebook, if you
  want to see the pattern of six lobes directly." New header "Unconventional singlet superconducting orders"
  (Challenge), and "Gapped and nodal superconducting orders" (Core), since the d-wave map is in the first one. New last
  sentence "The nodal $L=3$ (f-wave) case of the triangular lattice discussed above is in the second of these sections,
  where its bands touch zero energy at a node between $M$ and $\Gamma$.", since that cell draws bands and no map, and
  its path $\Gamma$, $K$, $M$, $\Gamma$ crosses one node. `.tex` lines 532 and 535 to 537. Asserted in `g3_13` against
  the cells of `session5.ipynb`, and on the path of the cell, 0.912 on $\Gamma$-$K$, 2.0 on $K$-$M$ and zero at
  $(1/3,0)$ on $M$-$\Gamma$.
- Page `13`, try-it box. Old "even though $\Delta=0.2$ is nonzero." New "even though `delta=0.2` is nonzero.", since the
  pairing of the notes reaches $6\sqrt3\times0.2=2.078$ at $K$ for this argument of pyqula. Not in the `.tex`. Asserted
  in `g3_13`, by pyqula and by the six-neighbor formula.
- The word gap, used for $2|\Delta|$ in Sections 5.8 and 5.9 and for the smallest quasiparticle energy elsewhere. The
  builder changed the try-it box of page `13`, old "keep a gap of $|\Delta|=0.4$", new "keep a smallest quasiparticle
  energy $|\Delta|=0.4$". The third feedback of the second quiz of page `17`, old "the bulk gap is $0.82t$", is now "the
  smallest bulk energy is $0.82t$". Both are web-only. Asserted in `g3_13` and `g5_17`.
- Page `14`, text. Old "has Chern number $\pm 2$, where the sign is set by the chirality, $p_x + ip_y$ or $p_x - ip_y$."
  New "has Chern number $\pm 2$. For a pocket around $\Gamma$ or $(\pi,\pi)$ the sign is set by the chirality, $p_x +
  ip_y$ or $p_x - ip_y$, together with the side of the Fermi surface, filled or empty states inside the pocket." The
  fold of the same page has the same range. `.tex` lines 560 and 561. Asserted in `g4_14`, together with the reason for
  the range: (5.15) of $p_x+ip_y$ winds $-1$ around $(\pi,0)$, and a pocket of filled states there gives $C=-1$ per
  block.
- Page `14`, text. Old "Here there are two, one from each of the two identical spin blocks." New "Here there are two,
  one from each of the two spin blocks.", since the two blocks of this triplet carry $\Delta$ and $-\Delta$. `.tex`
  line 571. Asserted in `g4_14`.
- Page `14`, the kept quiz on $p_x-ip_y$. Old first feedback "Its Chern number is $-2$ and not $0$", new "Its Chern
  number has the opposite sign and the same size $2$, so it is not $0$". Old third feedback "The Chern number changes
  from $+2$ to $-2$.", new "The Chern number changes sign, for example from $+2$ to $-2$ for a pocket of filled
  states around $\Gamma$.", since the ribbon figure above it has $-2$ for $p_x+ip_y$. Not in the `.tex`. Asserted in
  `g4_14`.
- Page `16`, third feedback of the quiz on the flat band. Old "The value $t$ would need $\Delta=t/2$." New "No $\Delta$
  gives a band flat at $t$, since at $k=0$ the pairing vanishes and $E=2t$ for any $\Delta$." Not in the `.tex`. The
  assert of the removed $t/2$ is replaced in `g5_16`.
- Page `17`, first paragraph. Old "If we diagonalize (5.19) on a *periodic* chain, we obtain a fully gapped spectrum,
  with a superconducting gap set by $\Delta$ and a nontrivial topological invariant of the bulk." New "If we
  diagonalize (5.19) on a *periodic* chain with $\Delta\neq0$ and $|\mu|<2t$, we obtain a fully gapped spectrum, with a
  superconducting gap set by $\Delta$ and $\mu$ and a nontrivial topological invariant of the bulk." `.tex` lines 684
  and 685. Asserted in `g5_17`, with the Zak phase and the smallest bulk energy.
- Page `17`. Old "In the topological phase, on the other hand, p-wave pairing dominates over the trivial onsite
  physics." New "In the topological phase, on the other hand, the hopping dominates over the onsite term,
  $|\mu|<2t$, and any $\Delta\neq0$ is enough." `.tex` lines 704 and 705, where the sentence goes on with "and the two Majoranas
  at each site pair". Asserted in `g5_17`, with $\Delta=0.1t$ at $\mu=1.5t$ and $1.9t$.
- Page `17`, caption of `majorana_splitting`. Old "and the first bulk level stays near $0.8t$." New "and the first bulk
  level comes down from $1.02t$ at $N=4$ to $0.83t$ at $N=30$, close to the bulk value $0.82t$." Its alt text, old "a
  flat line for the first bulk level", new "a nearly flat line close to 1 for the first bulk level". Not in the `.tex`.
  Asserted in `g5_17`, with the first bulk level within 0.1 decade of 1 on the log axis.
- Page `17`, text of the widget `kitaevbdg`. After "For $|\mu|<2t$ two levels sit at zero energy inside the gap, and
  their weight is at the two ends of the chain." the sentence "On 30 sites this holds away from $|\mu|=2t$, since near
  it the two end modes overlap and the two levels move away from zero." is added. Not in the `.tex`. Asserted in
  `g5_17`, with the levels of the widget itself.
- Page `19`. Old "Braiding two Majoranas, for example $\gamma_1$ around $\gamma_2$, acts on the ground-state manifold as
  a unitary", new "Braiding two Majoranas, for example the exchange of $\gamma_1$ and $\gamma_2$, acts on the
  ground-state manifold as a unitary", since [(5.23)](#eq-5-23) is one exchange and $\gamma_1$ once around $\gamma_2$
  is two. `.tex` line 762. Asserted in `g6_19`.
- Page `16`, after (5.20), the pick of the lecturer. After "so the anomalous term is explicitly odd in $k$." the sentence
  "The sign of $i$ is a gauge choice, $\Delta\to-\Delta$, and the spectrum depends only on $2|\Delta\sin k|$." is added,
  and (5.20) stays as printed. `.tex` line 645. Asserted in `g5_16`.
- Page `16`, notebook box. Old "Build the Kitaev chain of (5.19) and diagonalize it at the fine-tuned point $\Delta=t$,
  $\mu=0$. Check directly, as the system size grows, that two states are pinned exactly to zero energy and are localized at
  the two ends." New "Build the Kitaev chain of (5.19) at the fine-tuned point $\Delta=t$, $\mu=0$, and check that two
  states sit at zero energy for every size, localized at the two ends.", then the sentence on $\gamma_1$ and $\gamma_{2N}$
  as before, then "The cell itself uses `Delta = 0.1` with `d=[1.,1.,0.]`, which is $\Delta=0.14$, and `mu = 0.3`, which is
  $\mu=-0.3$. There the two states approach zero only as the chain grows, with oscillations, since the overlap of the two end
  modes oscillates with the length of the chain." The last sentence was "There the two states reach zero only as the chain
  grows." until the independent check, since the lowest level of the cell is 0.0126 at 10 sites, 0.0449 at 14, $2.0\cdot10^{-5}$
  at 30 and $1.65\cdot10^{-3}$ at 40. `.tex` lines 676 to 679. Asserted in `g5_16` against the cell, with the complex roots of
  the end mode, of modulus $\sqrt{(t-\Delta)/(t+\Delta)}=0.867$.
- Page `11`, after (5.10). The sentence "We use (5.10) only for its symmetry, since its overall sign is the opposite of the
  one of (5.4)." is added before "The real-space and reciprocal-space pictures". `.tex` line 401. Asserted in `g3_11`.
- Page `11`, Anderson's theorem. Old "A spin-singlet superconductor is essentially insensitive to non-magnetic disorder,
  which is called Anderson's theorem, since the pair wave function only depends on time-reversed partners, and
  non-magnetic disorder preserves them." New "A spin-singlet superconductor whose gap has one sign on the whole Fermi
  surface is essentially insensitive to non-magnetic disorder, which is called Anderson's theorem. The reason is that the
  pair wave function only depends on time-reversed partners, and non-magnetic disorder preserves them." Old "this disorder
  destroys the triplet channel and leaves the singlet channel intact", new "this disorder suppresses the triplet channel
  and the singlets that change sign, such as d-wave, and leaves the s-wave singlet intact". `.tex` lines 431 to 439.
  Asserted in `g3_11`.
- Page `08`, the minus sign of (5.6). The web had "Without it, the two spin blocks would mix through a Pauli matrix.",
  the `.tex` "instead of mixing the two spin blocks through a Pauli matrix". New "Without it, the two blocks would still be
  decoupled, but with $+\Delta$ in one and $-\Delta$ in the other, so they would not be identical copies." `.tex` lines
  273 to 276. Asserted in `g2_08`.
- Page `08`, notebook box. Old "two copies of the same band structure", new "two copies of the band structure". `.tex`
  line 319. Asserted in `g2_08`.
- Page `12`. Old "The pairing that survives is necessarily spin-triplet, because the exchange field explicitly splits",
  new "The pairing that survives is spin-triplet once the exchange field is of the order of the smallest quasiparticle
  energy of the singlet, or when only one spin band crosses the Fermi level. The reason is that the exchange field
  explicitly splits". Until the independent check the condition was "when the exchange field is large compared with the
  singlet gap", which holds, but the pairing changes already at a field below the singlet gap. `.tex` line 454.
  Asserted in `g3_12`, on the bond attraction of the page with $\mu=-1.6$: for $|U|=1.5$ the pure singlet of $h=0$, with the
  smallest quasiparticle energy 0.2875, is still the ground state at $h=0.1$ and gives way to a pure equal-spin triplet at
  $h=0.3$, with both spin bands at the Fermi level, and for $|U|=3$ at $h=0.6$, where only the up band crosses it, the ground state is the up-up triplet, below
  every opposite-spin state with a pair momentum from 0 to 1.6. The clause on one spin band is not backed at $|U|=3$ just
  above $h=0.4$, see "Not applied".
- Page `13`, the list under (5.14). Old "often ferromagnetic-magnon-driven" and "often antiferromagnetic-magnon-driven",
  new "proposed to be ferromagnetic-magnon-driven" and "proposed to be antiferromagnetic-magnon-driven". `.tex` lines 505
  and 506. No number, and `g3_13` checks the wording against Section 5.4.
- Page `18`. Old "A magnet breaks time-reversal symmetry locally", new "A magnet whose magnetization has a component
  perpendicular to the spin axis of the edge breaks time-reversal symmetry locally". `.tex` line 720. Asserted in `g6_18`.
- Page `18`, notebook box. Old "Build the construction described above, with the QSH edge, the magnets and
  superconductivity, and check that zero modes localized at the ends emerge as you change the strength of the exchange
  field. Look at how the system crosses the boundary between the topological and the trivial phase, of the type of
  (5.22), as the magnetic gap changes." New "Build the two-dimensional analog of this construction, a triangular lattice
  with Rashba coupling, an exchange field and s-wave pairing. The first cell computes the Chern number of the BdG bands, and
  the second one the chiral edge states of a ribbon. These two cells use opposite signs of the exchange field, and a change
  of this sign reverses both the Chern number and the direction of the edge states. The last cell follows how the gap closes
  and opens again as the field grows." Until the independent check the box said "Then follow the Chern number of the BdG
  bands and the chiral edge states of a ribbon as you change the exchange field", while no cell follows them as the field
  changes. `.tex` lines 738 to 741. Asserted in `g6_18`, on the text of the three cells, with $C=+3$ and $-3$ from the links
  at the fields $-0.6$ and $+0.6$, and 3 right movers on the upper edge of the ribbon at $-0.6$ against 3 left movers at $+0.6$.
- Page `17`, try-it box. Old "the line `mu = 0.3` sets the chemical potential", new "the line `mu = 0.3` sets the
  chemical potential through `h.add_onsite`, which is $\mu=-0.3$ in (5.19)". Not in the `.tex`. Asserted in `g5_17`.
- Format only, with no change of content. The paragraph of page `08` after (5.6) is split before "Let us take a
  spin-singlet pairing", the paragraph of page `11` before "This symmetry classification has a direct physical
  consequence", and the paragraph of page `12` before "The pairing that survives", since the new sentences took them
  over 150 words.
- Page `08`, found by the independent check of 2026-11-22. Old "Since the spinor [(5.6)](#eq-5-6) was built with this extra
  minus sign, the $4\times 4$ problem in [(5.7)](#eq-5-7) is already block-diagonal. There is one $2\times 2$ block built
  from $(c_{\mathbf k\uparrow}, c_{-\mathbf k\downarrow}^\dagger)$ and an identical one built from $(c_{\mathbf
  k\downarrow}, -c_{-\mathbf k\uparrow}^\dagger)$." New "The $4\times 4$ problem in [(5.7)](#eq-5-7) splits into two $2\times
  2$ blocks, and it would split also without the extra minus sign of the spinor [(5.6)](#eq-5-6). There is one block built
  from $(c_{\mathbf k\uparrow}, c_{-\mathbf k\downarrow}^\dagger)$ and one built from $(c_{\mathbf k\downarrow},
  -c_{-\mathbf k\uparrow}^\dagger)$, and the minus sign is what makes the second one identical to the first." The old
  sentence gave the sign the credit for the decoupling, against the new sentence after (5.6), and in the order of (5.6)
  the two blocks are interleaved, as the caption of `nambu_blocks` says. `.tex` lines 296 to 300. Asserted in `g2_08`, as
  operators on rings of 3 and 4 sites and on the matrix (5.7) in the two orders.
- Page `18`, first feedback of the first quiz, found by the independent check of 2026-11-22. Old "A magnet only breaks
  time-reversal symmetry and opens a gap below it.", new "A magnet breaks time-reversal symmetry, and its component
  perpendicular to the spin axis of the edge opens a gap below it.", in line with the new sentence of the text of the same
  page. Not in the `.tex`. Asserted in `g6_18`, where every $\mathbf m\cdot\boldsymbol\sigma$ is odd under time
  reversal and only the perpendicular part opens a gap.

### Decided on 2026-11-22

The lecturer picked the first point. The coordinator decided the others with the rule of that day, which takes the option
that makes the text true with the smallest change and changes no numbered equation, reduces a claim to what a source or a
calculation supports, redraws an old plot under its name, and rewrites a box that does not match its notebook cell.

- The sign of (5.20), page `16`. The lecturer chose to keep (5.20) and to add "The sign of $i$ is a gauge choice,
  $\Delta\to-\Delta$, and the spectrum depends only on $2|\Delta\sin k|$." The quiz of page `20` and the stems of
  `pair_function` stay, since they follow (5.20) as printed. `g5_16` checks it on a ring of 24 sites, where $\pm\Delta$
  give the same levels and they are $\pm\sqrt{(2t\cos k+\mu)^2+4\Delta^2\sin^2k}$, on the block with $+2i\Delta\sin k$,
  $-2i\Delta\sin k$ and $2\Delta|\sin k|$, and with the gauge $c_n\to ic_n$ as a unitary. The independent check found
  the wording loose, since the spectrum also depends on $\varepsilon(k)$. Its candidate is in "Not applied", since the
  wording is the lecturer's.
- The sign and the prime of (5.10), page `11`. The coordinator chose the first option, reduced to what is supported. The
  page says "We use (5.10) only for its symmetry, since its overall sign is the opposite of the one of (5.4)." The
  clause "the prime is the sum over half of the zone" is left out, since with that sum an even $\Delta_{\mathbf
  k,\uparrow\uparrow}$ gives an operator that is not zero, which contradicts "Fermionic antisymmetry imposes (5.11)" and
  the fold, whose sum runs over the whole zone. So the prime stays undefined. `g3_11` gives
  $\Delta_{\uparrow\downarrow}=-\Delta$ with the whole zone and $-2\Delta$ with half of it, and the even
  $\Delta_{\uparrow\uparrow}$, on a ring of 4 sites.
- The minus sign of (5.6), page `08`. The coordinator chose the first option. Deleting the sentence would leave "With
  it, ... two identical and decoupled copies", which credits the sign also with the decoupling, so only the first option
  makes the text true. `g2_08` checks the spinor without the sign as operators on rings of 3 and 4 sites.
- The try-it of 5.5, page `04`. The coordinator kept "about 0.1 to 0.2 and 0.4", which is true to one digit and asserted
  in `g1_04`, so nothing changes.
- Anderson's theorem, page `11`. The coordinator chose the two sentences without the lab box, the smallest change that
  makes the page agree with Section 5.13. The first sentence is written as two, for the lint. The lab box of
  Sr$_2$RuO$_4$ of the block of 5.11 stays out. `g3_11` checks it by two routes. A uniform onsite $\Delta$ with any real
  disorder keeps the levels $\pm\sqrt{\varepsilon_n^2+\Delta^2}$, and in a self-consistent mean field on a square
  lattice of $10\times10$ sites with a box disorder of width $3t$, six realizations, each converged to $10^{-7}$, the
  s-wave order keeps more than 0.8 of its clean value, and the d-wave order and the $p_x+ip_y$ order of one spin keep
  less than half of theirs, at most 0.18 and 0.23. Until the independent check the assert took two realizations, let a
  run that had not converged pass when its order was small, and used the bound 0.25, which other couplings exceed.
- "necessarily spin-triplet", page `12`. The coordinator chose the first option, written as two sentences for the lint.
  The independent check sharpened its condition to "once the exchange field is of the order of the smallest quasiparticle
  energy of the singlet", see the first list. `g3_12` checks the singlet part on the chain with $t=1$, $\mu=0.5$ and an
  onsite $U=-2$, which has no triplet channel, where $\Delta_0=0.351$ and the field where the polarized state wins is
  0.250, about $\Delta_0/\sqrt2$. The uniform singlet, with zero pair momentum, survives at half of this field and is
  gone at 1.2 and 2 times it, and at $h=2$, where only the spin-down band crosses the Fermi level. A singlet with the pair
  momentum 0.3 still lowers the energy at 1.2 times this field, by $5.3\cdot10^{-4}$ per site. The triplet part is checked
  on the bond attraction of the page, as the first list says.
- "often magnon-driven", page `13`. The coordinator chose "proposed to be", which agrees with Section 5.4. The list is
  the unnumbered display after (5.14), so (5.14) does not change. No calculation can check it, and `g3_13` reads the two
  pages.
- The magnet on the helical edge, page `18`. The coordinator chose the first option. `g6_18` gives no gap for a magnet
  along the spin axis $z$ and a gap of $2|m_\perp|$ for a perpendicular part $m_\perp$.
  Three sentences with the same claim and no condition were found. The first feedback of the first quiz of the page was
  corrected after the independent check, see the first list, and the two others are in "Not applied".
- The Kitaev figures of 5.16 and 5.17. The coordinator kept all of them in numpy from the exact chain (5.19), as now,
  since nothing on the pages is false and this is the smallest change. The locked rule of a pyqula script for every
  calculation that pyqula can do points the other way, which is for the lecturer to weigh. The 0.3% of the question is
  the finite size of the chain of 40 sites, since the exact chain gives the same first bulk level 1.418 as pyqula,
  against the bulk value 1.414, asserted in `g5_17`.
- The old web figures that break the plot rules. The coordinator applied the rule "Redraw them, same names" of
  2026-11-21, and nothing was left to redraw. All twelve were redrawn in place in commit `033b84d`. On 2026-11-22 each
  of the twelve scripts ran with no `AXES-WARNING` and wrote an SVG identical to the committed one, and each defect
  named in the fields "Old figures of the page that break the plot rules" above is gone in the picture, so these fields
  describe the figures before that commit. `zero_mode_profile` names the site axis once, under panel (b), which shares
  it with panel (a).
- "trillions" and "billions" of atoms, page `02`. The coordinator kept both, which are true as lower bounds and asserted
  in `g1_02`.
- The notebook box of page `08`. The coordinator chose "two copies of the band structure". `g2_08` checks the cell and
  the levels $\varepsilon$ and $-\varepsilon$ at $\Gamma$ and $M$.
- "identical spin blocks" in the caption of Figure 5.4, page `14`. The coordinator left it, since the rule keeps a point
  about a converted figure listed. See "Not applied".
- "The modulus is essentially the same" in the caption of Figure 5.4, page `14`. The coordinator left it for the same
  reason. See "Not applied".
- `delta=0.4` for both ribbons, page `14`. The coordinator kept it. The caption already says "The two gaps do not have
  the same size here", so nothing changes, and 0.40 and 1.34 are asserted in `g4_14`.
- The notebook box of page `16`. The coordinator chose the first option, by the rule on boxes that do not match their
  cell, with the arguments of the cell named, `Delta = 0.1` with `d=[1.,1.,0.]` and `mu = 0.3`. `g5_16` checks the text
  of the cell, its pyqula chain against (5.19) with $\mu=-0.3$ and $\Delta=0.14$ for every length of the cell, the two
  zero levels at $\Delta=t$, $\mu=0$, and the lowest level from 0.29 at 4 sites to below 0.002 at 40. The independent check
  added that this level oscillates with the length, see the first list.
- The try-it of page `17`. The coordinator chose the first option, which matches the cell and agrees with the notebook
  box of page `16`, which points to the same cell. Asserted in `g5_17`.
- "for example with $N=100$ sites", page `17`. The coordinator kept it, since it is given as an example and holds at the
  four points asserted in `g5_17`.
- The notebook box of page `18`. The coordinator chose the first option, by the rule on boxes, written as two sentences
  for the lint. The independent check found that no cell follows the Chern number as the field changes, and the box now
  says what each cell does, see the first list. `g6_18` checks it against the three cells and the model.
- The second quiz of page `19`. The coordinator kept it. In the basis $|11\rangle$, $-|00\rangle$ of the even sector the
  two operators are $+\sigma_z$ and $+\sigma_x$, so "acts like" holds as written, asserted in `g6_19`.
- The try-it of page `18`, "near $\mathbf k=0$". The coordinator kept it. At $J=0$ the value 0.3 is reached at
  $|\mathbf k|=0.096$, on the inner Fermi line of the line `M1`, `G`, `M1` of the cell, asserted in `g6_18`.
- The lab box of page `13`, source `tsuei1994`. The coordinator kept the asserts against the full copy. The other option
  changes `labsource.py`, a file of the toolkit, which this pass does not edit.
- The line on `nodal_fwave` of the conventions sheet. The coordinator corrected it, by the rule on outdated lines, to
  "With `delta=0.2` its entry grows along $\Gamma$-$K$ up to $2.078=6\sqrt3$ `delta` at $K$". The 1.42 was the largest
  value between 0.2 and 0.7 of the way to $K$. `conventions.py` checks it by pyqula and by the six bonds of $\pm2$
  `delta`.
- The notebook text on the exchange and on the hole block. The coordinator left it, since the notebooks are not edited.
  See "Not applied".

### Not applied

- "identical spin blocks" in the caption of Figure 5.4, `s05f04_topology`, page `14`, line 15 of
  `lecture_notes/src/figures/s05f04_topology.tex`. The rule leaves a converted figure untouched and keeps a point about it
  listed, and the first list of this section already treats this caption as part of the converted figure. So the caption
  keeps "one branch from each of the two identical spin blocks of (5.8)", while the text and the fold of the same page say
  that the blocks carry $+\Delta$ and $-\Delta$. The candidate is "one branch from each of the two spin blocks of (5.8)".
- "The modulus is essentially the same in both cases, so both fully gap the same pocket by the same amount", in the same
  caption, lines 10 and 11 of the same file, for the same reason. The candidate is "On a small pocket the modulus of
  $\Delta_{p+ip}$ is almost constant, so with the amplitudes chosen for it both gap the pocket by the same amount".
  `g4_14` asserts its numbers, $|\Delta_{p+ip}|/\Delta_0$ from 0.2955 to 0.2972 on the pocket of the problem, and from
  $0.200t$ to $0.245t$ at $\mu=-2t$ with $\Delta_0=0.2t$.
- The notebook text, $-Js_z$ with $E_\uparrow=E-J$ and the hole block $-(H_0-\mu)^*$. The notebooks are not edited in this
  pass, so the two sentences stay, and the conventions sheet keeps the point.
- Not one of the 24 points, found while the magnet of page `18` was decided. Three more sentences said that a magnet or a
  disorder that breaks time reversal opens a gap in a helical edge, with no condition on the direction. The first feedback
  of the first quiz of page `18` was corrected after the independent check of 2026-11-22, see the first list, since a quiz
  is web-only and it now disagreed with the text of its own page. Two stay for the lecturer. They are the caption of Figure
  5.6, a converted figure, "A ferromagnet placed on a part of this edge breaks time-reversal symmetry locally and removes
  the Kramers protection there, which opens a gap in the edge below it", and line 45 of
  `webnotes/pages/session03/11b-kramers-protection-of-the-helical-edge.md`, a page of another session, "disorder that
  breaks time-reversal symmetry opens a real gap in the edge spectrum".
- The second clause of the sentence of page `12`, "or when only one spin band crosses the Fermi level", found while the
  independent check was applied. On the bond attraction of the page with $\mu=-1.6$ and $|U|=3$ the down band leaves the
  Fermi level at $h=0.4$, but at $h=0.45$ a state with the singlet part 0.38 is still below the pure triplet, while at
  $h=0.6$ the pure triplet wins. So the clause holds at weak coupling, as at $|U|=1.5$, and not in general. It is decided text and no finding covered it, so it
  stays for the coordinator, with the candidate "or, at weak coupling, when only one spin band crosses the Fermi level".
  `g3_12` asserts the state at $h=0.45$.
- The sentence after (5.20), page `16`, which is the lecturer's pick, "The sign of $i$ is a gauge choice,
  $\Delta\to-\Delta$, and the spectrum depends only on $2|\Delta\sin k|$." The independent check of 2026-11-22 found it
  loose, since the spectrum $\pm\sqrt{(2t\cos k+\mu)^2+4\Delta^2\sin^2k}$ also depends on $\varepsilon(k)$. The candidate
  is "The sign of $i$ is a gauge choice, $\Delta\to-\Delta$, and the spectrum depends on the pairing only through
  $2|\Delta\sin k|$." It is not applied, since the wording was picked by the lecturer, and the gauge part is asserted in
  `g5_16`.
