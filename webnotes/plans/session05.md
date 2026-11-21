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

These touch a numbered equation, a statement of the old text, a convention or an old figure. A builder leaves them
as they are.

- The sign of [(5.20)](#eq-5-20). The page writes $\Delta(k)=2i\Delta\sin k$. With the convention of Section 2.5,
  $c_n^\dagger=\sum_k e^{-ikn}c_k^\dagger$, and $\Delta(k)$ as the coefficient of $c_k^\dagger c_{-k}^\dagger$, as in the
  upper right of [(5.8)](#eq-5-8), the Fourier transform of [(5.19)](#eq-5-19) gives $-2i\Delta\sin k$. On a ring
  of 8 sites with $\Delta=0.3$ the coefficient at $k=\pi/2$ is $-0.6i$, and with the opposite Fourier sign it is
  $+0.6i$. The sign of $i$ is a gauge choice and the spectrum depends only on $2\Delta|\sin k|$. The choices are to
  keep (5.20) with a sentence on the convention, to write $-2i\Delta\sin k$, or to say which coefficient is called
  $\Delta(k)$. The figure `pair_function` follows this choice.
- The sign and the factor of [(5.10)](#eq-5-10). It has $-\tfrac12\sum'$, and the prime is not defined on the page,
  while [(5.4)](#eq-5-4) has $+\Delta_n$. For the onsite singlet of (5.4), a sum over all $\mathbf k$ in (5.10) gives
  $\Delta_{\mathbf k,\uparrow\downarrow}=-\Delta$, checked on the operators of a ring of 3 sites with
  $\Delta=0.37$, and a sum over half of the zone gives $-2\Delta$. The classification (5.11) and (5.12) does not
  depend on this.
- The sentence of Section 5.8, "Without it, the two spin blocks would mix through a Pauli matrix". A check on the
  operators of $\pm\mathbf k$ with $\Delta=0.7$ shows that without the minus sign the matrix stays block diagonal,
  with $\Delta$ in one block and $-\Delta$ in the other, so the pairing block is $\Delta\sigma_z$ and the blocks do
  not mix. They are only not identical copies. The mixing through $i\sigma_y$ appears when the hole entries keep the
  order of the spins.
- Anderson's theorem in Section 5.11. The page says that a spin-singlet superconductor is insensitive to
  non-magnetic disorder, and that disorder "destroys the triplet channel and leaves the singlet channel intact".
  The protection holds for a gap with no change of sign, and the d-wave singlet of Section 5.13 is suppressed too.
  The stored abstract of Sr2RuO4 states "A key signature of unconventional or non-s-wave superconductivity is a
  strong suppression of Tc by nonmagnetic as well as by magnetic impurities." The lab box of 5.11 waits for this.
- "The pairing that survives is necessarily spin-triplet" in Section 5.12. This holds when the exchange field is
  large compared with the singlet gap, or when only one spin band crosses the Fermi level. A weak field leaves a
  singlet, and the source of the lab box of 5.12 reports superconductivity above the Pauli limit of a singlet,
  which is a finite field. The choice is to write the condition next to the sentence, or to keep it.
- The magnet of Section 5.18. The page says that a magnet opens a gap in the helical edge. In `helical_edge_gap`
  the field is along $x$, while a term $h\sigma_z$ along the spin axis of the edge gives $(vk+h)\sigma_z$, which only
  shifts the crossing in $k$ and opens no gap. The choice is to write that the magnetization needs a component
  perpendicular to the spin axis of the edge, or to keep the sentence.
- The list under [(5.14)](#eq-5-14) calls p-wave "often ferromagnetic-magnon-driven" and the d-wave of the cuprates
  "often antiferromagnetic-magnon-driven", while Section 5.4 says that the mediator of an unconventional
  superconductor is often an open question. The choice is "proposed to be" or to keep it.
- The try-it box of Section 5.5 says that the gap grows "from about 0.1 to 0.2 and 0.4". With the settings of the
  notebook the values are $0.103$, $0.223$ and $0.361$. The choice is to write $0.36$ or to keep "about 0.4".
- The Kitaev figures of 5.16 and 5.17. The rule asks for a pyqula script when pyqula can do the calculation, and
  the notebook does it with pyqula, but its chain is spinful with a remote band, and a run with `d=[1,1,0]` differs
  from the exact chain by 0.3% in the lowest bulk level. The choices are all numpy from the exact chain, or numpy
  for the figures that assert the numbers of the pages plus one pyqula figure with a download, whose caption quotes
  the numbers of its own run. Until the pick the builder of `g5` uses numpy.
- The old web figures that break the plot rules, listed in the blocks. These are `phonon_exchange`,
  `pairing_cobweb`, `particle_number_weights`, `nambu_bands`, `gap_any_mu`, `pockets_nodes`, `pair_function`,
  `spin_split_pairing`, `dwave_nodes`, `kitaev_spectrum`, `zero_mode_profile` and `helical_edge_gap`, with ticks
  missing, maps with no $k_x$ and $k_y$, or parameters missing in the caption. The builders leave them, as in
  Session 3. The choices are a separate pass that fixes them in place, followed by a look at `git status`, or to
  leave them.
