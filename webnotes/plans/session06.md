# Plan of Session 6 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session06.md`.

The conventions sheet of the session did not exist when this plan was written. Every sign and every pyqula
parameter below that is marked "from the sheet" is taken from it by the builder, and is not stated here.
The answers of the problems and the numbers of the new quizzes were computed for this plan with the scripts
of the old figures (`_mf.py`, `_haldane.py`) and with small numpy checks.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 460 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 (0) | 0 |
| `01-two-classes-of-magnets-and-their-excitations.md` | 6.1 | 706 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | long-paragraph 1, opener 1 |
| `02-a-recap-of-symmetry-breaking-and-the-mean-field-philosophy.md` | 6.2, 6.3 | 1120 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `04-exchange-splitting-and-antiferromagnetic-order-in-numerical-mean-field-theory.md` | 6.4, 6.5 | 1127 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 3 (0) | long-paragraph 1, opener 1, quiz-long 1, quiz-ref 1 |
| `06-the-stoner-threshold-as-a-criterion-for-magnetism.md` | 6.6, 6.7 | 1374 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1 |
| `08-from-the-hubbard-dimer-to-the-heisenberg-model.md` | 6.8 | 1082 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | key 1, opener 1 |
| `09-the-heisenberg-model-on-a-general-lattice.md` | 6.9, 6.10 | 1261 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `11-superexchange-as-the-origin-of-ferromagnetic-coupling.md` | 6.11, 6.12 | 1281 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | long-paragraph 1, opener 1 |
| `13-magnons-as-fluctuations-of-the-order-parameter.md` | 6.13, 6.14 | 1222 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | key 1, long-paragraph 2, opener 1 |
| `15-magnon-dispersions-in-ferromagnets-and-antiferromagnets.md` | 6.15 | 1093 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1 |
| `16-topological-magnons.md` | 6.16 | 1090 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | key 1, long-paragraph 1 |
| `17-closing-summary.md` | 6.17 | 633 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | 0 |

## Introduction of the session

File `index.md`, 460 words, no numbered equation, no lint hit.

- Question of the page, and where we arrive: the page opens with a statement of what we need from before.
  One sentence with the question of the session goes first, "What happens on the repulsive side of the
  Hubbard model, and what are the excitations of the magnets that it gives?". Nothing else changes.
- Main result for the key box: none, since an introduction has no result.
- Equation of another page that it starts from, for the recall box: none, the page already links (1.7),
  (3.4) and Section 5.8 in its text.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, an introduction.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, the index has no quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none. `session_map.py` stays.
- Old figures of the page that break the plot rules: none, `session_map` is a concept map.

## 6.1 Two classes of magnets and their excitations

File `01-two-classes-of-magnets-and-their-excitations.md`, 706 words, numbered equations none. A page of
motivation, so it gets fewer blocks.

- Question of the page, and where we arrive: which kinds of magnets exist, and what is their elementary
  excitation? We arrive at two classes, the magnets that break time-reversal symmetry with neutral spin-1
  magnons, and the quantum magnets with spin-1/2 spinons, which wait for Session 8. The opener replaces
  "Let us start with a map". The paragraph of 163 words is split where the spinon starts.
- Main result for the key box: none, a page of motivation.
- Equation of another page that it starts from, for the recall box: none, the page starts from no equation.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none. The materials of the page (iron,
  herbertsmithite, SmB$_6$) are named without a number, and herbertsmithite gets its box on 6.10.
- Pen-and-paper problem: none, a page of motivation.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the Mott insulator passes
  the lint and stays. No new quiz, since it is a page of motivation.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `s08f01_magnon_spinon` is a drawing.

## 6.2 A recap of symmetry breaking and the mean-field philosophy and 6.3 The Hubbard model and mean-field magnetism, revisited

File `02-a-recap-of-symmetry-breaking-and-the-mean-field-philosophy.md`, 1120 words, numbered equations (6.1), (6.2).

- Question of the page, and where we arrive: what does mean field do with a repulsive $U$, and why can the
  magnet point in any direction? We arrive at the magnetization (6.2) as an exchange field of size $Um$, and
  at the identity $Un_\uparrow n_\downarrow=\tfrac U2 n-\tfrac{2U}{3}\mathbf S^2$, which does not choose an axis.
  The first paragraph of 167 words is split after "before we apply it to magnetism".
- Main result for the key box: (6.2) with one sentence, "the difference of the two spin densities acts on
  the electrons as an exchange field that splits the two spins by $Um$, and it can point along any direction
  of $\langle\mathbf S\rangle$". The Hubbard chain (6.1) stays in the text, since it is the model and not a result.
- Equation of another page that it starts from, for the recall box: none. The page writes the chain again as
  (6.1) and the magnetization as (6.2), and these are (1.7) and (1.8) of Session 1, so a recall box would
  show the same equations twice.
- Derivation told in words, for a steps fold: "From the Hubbard term to an exchange field". Simplest case
  first, one site with four states, where $\mathbf S^2=\tfrac34(n-2n_\uparrow n_\downarrow)$ gives the identity.
  Then the decoupling $n_\uparrow n_\downarrow\to\langle n_\uparrow\rangle n_\downarrow+n_\uparrow\langle n_\downarrow\rangle-\langle n_\uparrow\rangle\langle n_\downarrow\rangle$,
  which gives the onsite energies $U\langle n_\downarrow\rangle$ and $U\langle n_\uparrow\rangle$.
- Lab box, with the source and the number that the source states: graphene multilayers,
  https://www.science.org/doi/10.1126/science.aar6855, stored as `nam2018_science.aar6855.txt`, a candidate
  of the notebook. The arXiv abstract says "Here we show that a finite-temperature second order phase
  transition occurs in multilayers whose critical temperature Tc increases from 12 K in bilayers to 100 K in
  heptalayers." It also says that a model "inspired by a mean field approach" gives "a self-consistent valley-
  and spin-dependent staggered potential". The probe is not named in the arXiv abstract, only in the
  editor summary, which is not used. The box says "the measured transition" and names no probe.
- Pen-and-paper problem: decouple $Un_\uparrow n_\downarrow$ in mean field and find the energy difference
  of a spin-down and a spin-up electron on one site. Answer $Um$, which is $0.8t$ for $U=4t$ and the polarized
  chain at $n=0.2$, the value of the figure of 6.4.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on $m_x$ has a question of
  18 words. It is cut to short sentences with $S^x=\tfrac12(c_\uparrow^\dagger c_\downarrow+c_\downarrow^\dagger c_\uparrow)$
  in the question, with its physics kept. New, with equations as options, "Mean field replaces
  $Un_\uparrow n_\downarrow$ by which bilinear?", the correct option is the decoupling of the fold, the wrong
  ones are $U\langle n_\uparrow\rangle\langle n_\downarrow\rangle$ alone and $U\langle n_\uparrow n_\downarrow\rangle n$.
  New, "Which state of one site pays the energy $U$ in $\tfrac U2 n-\tfrac{2U}{3}\mathbf S^2$?", with the doubly
  occupied state as the answer. No picture question on this page, since the bars of the figure would give
  the answer away.
- Figures to add, each with its pyqula script or the reason for numpy: none. `hubbard_spin_identity` is an
  identity of operators on one site, which pyqula does not compute, so it stays numpy.
- Old figures of the page that break the plot rules: none. `hubbard_spin_identity` draws its own energy axis
  with the name "energy$/U$" and the ticks $1$, $\tfrac12$, $-\tfrac12$. `s01f02_ssb` is a converted figure.

## 6.4 Exchange splitting and antiferromagnetic order in numerical mean-field theory and 6.5 Competition between the ferromagnet and the antiferromagnet

File `04-exchange-splitting-and-antiferromagnetic-order-in-numerical-mean-field-theory.md`, 1127 words, numbered equations none.

- Question of the page, and where we arrive: does the repulsive Hubbard chain choose a ferromagnet or an
  antiferromagnet, and by how much? We arrive at the gapped antiferromagnet at half filling, lower in energy,
  with an energy difference that falls as $1/U$. The paragraph of 151 words on the two solutions is split
  after "Both are real fixed points of the self-consistency loop".
- Main result for the key box: an unnumbered display, since the page has no numbered equation. The bands
  of the antiferromagnet $E_k=\pm\sqrt{\epsilon_k^2+(Um/2)^2}$ with $\epsilon_k=-2t\cos k$, and
  $E_\mathrm{FM}-E_\mathrm{AFM}\simeq 4t^2/U$ per cell of two sites for $U\gg t$, which is $2t^2/U$ per site.
  The `mf_chain.py` asserts already check the $2t^2/U$ per site.
- Equation of another page that it starts from, for the recall box: `eq="6.1 6.2"`, the chain and the
  magnetization of 6.3.
- Derivation told in words, for a steps fold: "From the gap equation to the 1/U law". The gap equation
  $1=\tfrac U2\langle 1/E_k\rangle$, then for $U\gg t$ the expansions $m\simeq1-4t^2/U^2$, kinetic energy
  $-4t^2/U$ and interaction energy $U(1-m^2)/4\simeq2t^2/U$ per site, so $E_\mathrm{AFM}\simeq-2t^2/U$ per
  site against $0$ for the saturated ferromagnet. Simplest case first, $U=0$, where the gap is zero.
- Lab box, with the source and the number that the source states: zigzag graphene nanoribbons,
  https://www.nature.com/articles/nature13831, stored as `magda2014_nature13831.txt`. The arXiv abstract
  says "While armchair ribbons display quantum confinement gap, zigzag ribbons narrower than 7 nm reveal a
  bandgap of about 0.2 - 0.3 eV, which can be identified as a signature of interaction induced spin ordering
  along their edges." It also says that a wider ribbon shows a semiconductor to metal transition, "indicating
  the switching of the magnetic coupling between opposite ribbon edges from antiferromagnetic to
  ferromagnetic configuration". The abstract names STM as the tool that defines the ribbons. The link to
  the gapped antiferromagnet and the gapless ferromagnet of the chain is our reading, marked as ours.
- Pen-and-paper problem: show that the saturated ferromagnet of the half-filled chain is a self-consistent
  solution only for $U>4t$. Answer $4t$, since the empty spin-down band, shifted by $Um=U$, must start above
  the top of the full spin-up band, $-2t+U>2t$. The problem stops here and does not compare energies, see
  "Open for the lecturer".
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the $1/U$ law has a
  question of 20 words and a feedback that names Section 6.8. It gets short sentences, the display
  $E_\mathrm{FM}-E_\mathrm{AFM}\simeq 4t^2/U$ in the question and no section number. New, a picture question,
  "Which bands belong to the antiferromagnet of the half-filled chain at $U=4t$?", with three band structures
  as options, the split bands of the ferromagnet at $n=0.2$, the gapped bands of the antiferromagnet, and the
  crossing bands of the paramagnet. New, with equations as options, "Which dispersion has the
  antiferromagnetic chain in mean field?", the options $\pm\sqrt{\epsilon_k^2+(Um/2)^2}$, $\epsilon_k\pm Um/2$
  and $\pm|\epsilon_k|+Um/2$.
- Figures to add, each with its pyqula script or the reason for numpy: the mean field of the chain is a
  pyqula calculation (notebook cells 6, 18 and 21). `chain_meanfield.py` with
  `h.get_mean_field_hamiltonian(mf="ferro")` on `geometry.chain()` and `mf="antiferro"` on
  `geometry.bichain()` at $U=4$, for the redraw of `fm_afm_chain` (a) and `mf_chain` (a).
  `chain_energy_difference.py` with `return_total_energy=True` at $U=20$ and $40$, for `ufactor`. The
  three pictures of the quiz, `quiz_bands_fm.py`, `quiz_bands_afm.py`, `quiz_bands_pm.py`, with the shared
  code in `_quizbands.py`, drawn from the same pyqula calculation. The density of the ferromagnet and the
  energy per cell or per site of `return_total_energy` come from the sheet.
- Old figures of the page that break the plot rules: `fm_afm_chain` (a) has the axes $k$ and $E$ with no unit
  and no number, so $\mu$ and $Um=0.8t$ are not on an axis. `mf_chain` (a) is the same, and (b) has $U$ and
  $E_\mathrm{uniform}-E_\mathrm{AFM}$ with no unit and no tick on the energy. `ufactor`, the picture of the
  quiz feedback, is a log-log plot with all its ticks removed, so the two marked values cannot be read on
  the axes. Panel (b) of `mf_chain` is redrawn only after the lecturer picks, see "Open for the lecturer".

## 6.6 The Stoner threshold as a criterion for magnetism and 6.7 The strongly localized limit, where mean field breaks down

File `06-the-stoner-threshold-as-a-criterion-for-magnetism.md`, 1374 words, numbered equations (6.3).

- Question of the page, and where we arrive: does any repulsive $U$ give a magnet, or is there a threshold?
  We arrive at the Stoner criterion (6.3), and then at the large-$U$ limit, where the moment saturates and
  mean field stops being reliable. The opener turns "A natural question is whether" into the question
  itself. The paragraph of 207 words is split after "a finite $m$ appears spontaneously".
- Main result for the key box: (6.3) with one sentence, "$D(E_F)$ is the density of states per spin and per
  site at the Fermi level, and the product decides, not $U$ alone".
- Equation of another page that it starts from, for the recall box: `eq="6.2 2.16"`, the magnetization of
  6.3 and the density of states $g(\omega)$ of Session 2.
- Derivation told in words, for a steps fold: "From the self-consistency condition to the Stoner criterion
  (6.3)". Expand $n_F(E\mp Um/2)$ to first order in $m$, then at zero temperature $-\partial n_F/\partial E$
  is a delta function at $E_F$, so the sum gives $m=UmD(E_F)$. Simplest case first, a constant density of
  states. The fold says that the expansion holds for small $m$ only.
- Lab box, with the source and the number that the source states: twisted bilayer graphene at a small
  twist angle, as the abstract says, and not "magic-angle", which is only in the editor summary,
  https://www.science.org/doi/10.1126/science.aaw3780, stored as `sharpe2019_science.aaw3780.txt`. The arXiv
  abstract says "We observe emergent ferromagnetic hysteresis, with a giant anomalous Hall (AH) effect as
  large as 10.4 kΩ and signs of chiral edge states in a narrow density range around an apparent insulating
  state at 3/4." The abstract speaks of flat minibands that "enhance electron-electron interactions" and does
  not name Stoner, so the link to a large $D(E_F)$ is ours. The quote comes from the arXiv abstract, not
  from the editor summary of the same file.
- Pen-and-paper problem: a half-filled band with a constant density of states $1/W$ per spin over a width
  $W$. Find the $U$ above which the paramagnet is unstable. Answer $U_c=W$, so $4t$ for $W=4t$.
- Quizzes to rewrite, and a picture question or equations as options: the flat-band quiz links (6.3) in its
  question. The question writes $UD(E_F)\geq1$ as a display instead, and the physics stays. New, a picture
  question, "Which curve $f(m)$ gives a magnetized solution?", with three curves $f(m)$ against the diagonal
  $y=m$ as options, slopes $0.5$ and $1.5$ at the origin and one that crosses only at $m=0$. New, on 6.7,
  "At $U=16t$ the moment is $|m|=0.984$. What is $4\langle n_\uparrow n_\downarrow\rangle=1-m^2$?", answer
  $0.03$, from `_mf.moment(16)`, which is $0.9844$. With the rounded $0.98$ of the caption the answer would
  be $0.04$, so the question gives three digits.
- Figures to add, each with its pyqula script or the reason for numpy: `moment_vs_U` is redrawn from
  `chain_moment.py`, pyqula with `mf="antiferro"` on `geometry.bichain()` and `h.get_vev("mz")` over $U$, as in
  notebook cell 15, which is the chain against $U$. Cell 12 is the dimer and is not used. The three pictures
  of the Stoner quiz are numpy, `quiz_stoner_low.py`,
  `quiz_stoner_high.py`, `quiz_stoner_none.py` with `_stonerquiz.py`, since they are model functions $f(m)$
  and not a pyqula calculation. A pyqula curve of $m$ against $U$ for the chain at $n=0.2$ is not planned
  until the lecturer picks, see "Open for the lecturer".
- Old figures of the page that break the plot rules: `moment_vs_U` has no name on its vertical axis, and the
  values $0.77$ and $0.98$ of the caption have no tick. `s06f01_stoner` and the panel of `s02f05_flatbands`
  are converted figures with named axes.

## 6.8 From the Hubbard dimer to the Heisenberg model

File `08-from-the-hubbard-dimer-to-the-heisenberg-model.md`, 1082 words, numbered equations (6.4).

- Question of the page, and where we arrive: what is the energy scale of magnetism when $U\gg t$, and why
  is it antiferromagnetic? We arrive at $J=4t^2/U$, the splitting between the singlet and the triplet of the
  Hubbard dimer. The opener replaces "Let us make this precise". The sentence with no verb, "The three
  parallel or triplet-like states, ...", gets a verb and keeps its content.
- Main result for the key box: (6.4) with one sentence, "$J$ is the splitting between the triplet and the
  singlet, and it is positive, so antiparallel spins are lower, because only they can hop".
- Equation of another page that it starts from, for the recall box: `eq="6.1"`, the Hubbard chain, here on
  two sites.
- Derivation told in words, for a steps fold: "The singlet, the triplet and the matrix element $-2t$". With
  the basis states written as $c^\dagger_{0\sigma}c^\dagger_{1\sigma'}|0\rangle$ we get
  $H_t|\!\uparrow,\downarrow\rangle=-t(|\!\uparrow\downarrow,0\rangle+|0,\uparrow\downarrow\rangle)$ and
  $H_t|\!\downarrow,\uparrow\rangle=+t(\dots)$, so the triplet $|T_0\rangle$ gives zero and
  $\langle D|H_t|S\rangle=-2t$, as the page says. The sign depends on the order of the operators and the
  eigenvalues do not, which the fold says. Then the expansion of the root to $-4t^2/U$.
- Lab box, with the source and the number that the source states: the nanographene Clar's goblet,
  https://www.nature.com/articles/s41565-019-0577-9, stored as `mishra2020_s41565-019-0577-9.txt`, with
  the abstract pasted from PubMed. The abstract says "Scanning tunnelling microscopy and spin excitation
  spectroscopy of individual molecules on a gold surface reveal a robust antiferromagnetic order with an
  exchange-coupling strength of 23 meV, exceeding the Landauer limit of minimum energy dissipation at room
  temperature5." The abstract says "exchange-coupling strength" and "unpaired electrons". That the
  spin excitation sits at the singlet-triplet splitting, which is $J$ of (6.4), is ours. After the box is
  written, `python3 webnotes/labsource.py --quotes` writes the quotation into the tracked file.
- Pen-and-paper problem: expand $E_S$ to the next order in $t/U$. Answer $J\simeq4t^2/U-16t^4/U^3$, which
  is $0.469t$ at $U=8t$, against the exact $0.472t$ and the first-order $0.5t$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on doubling $t$ asks for "$J$
  of (6.4)". It writes $J=4t^2/U$ in the question instead. New, with equations as options, "The singlet
  couples to the doubly occupied state with $-2t$. What is the singlet energy?", the options
  $\tfrac U2-\sqrt{U^2/4+4t^2}$, $\tfrac U2-\sqrt{U^2/4+t^2}$ and $-4t^2/U$ exactly. New, a picture question,
  "Which level diagram is the Hubbard dimer at $U=10t$?", with three diagrams as options, the singlet at
  $-0.385t$ below the triplet at $0$, the triplet below the singlet, and four degenerate levels.
- Figures to add, each with its pyqula script or the reason for numpy: the three pictures of the quiz,
  `quiz_dimer_right.py`, `quiz_dimer_flipped.py`, `quiz_dimer_degenerate.py` with `_dimerquiz.py`, in numpy,
  since they are a diagonalization of six many-body states, which pyqula does not do.
- Old figures of the page that break the plot rules: none, the page has only the converted `s06f02_dimer`.

## 6.9 The Heisenberg model on a general lattice and 6.10 Bipartite order versus geometric frustration

File `09-the-heisenberg-model-on-a-general-lattice.md`, 1261 words, numbered equations (6.5).

- Question of the page, and where we arrive: what spin model does the large-$U$ limit give on any lattice,
  and can all its bonds be satisfied at the same time? We arrive at (6.5) with $J_{ij}>0$, the Néel state on
  a bipartite lattice and the $120^\circ$ compromise on a triangle. The opener replaces "The argument of
  Section 6.8 did not use". The paragraph of 194 words on frustration is split after "is what is called
  geometric frustration".
- Main result for the key box: two boxes, since the page has two results. The first holds (6.5) with the
  sign convention, $J_{ij}>0$ is antiferromagnetic. The second holds the classical triangle, three spins at
  $120^\circ$ with $\mathbf S_i\cdot\mathbf S_j=-S^2/2$ on every bond and $-\tfrac32JS^2$ per triangle,
  against $-JS^2$ for the collinear attempt, as an unnumbered display.
- Equation of another page that it starts from, for the recall box: `eq="6.4"`.
- Derivation told in words, for a steps fold: "From one bond to the 120 degree triangle". First, the
  second-order argument applied bond by bond, with the constant $-J_{ij}/4$ that (6.5) leaves out. Then for
  three classical spins $\sum_{\text{bonds}}\mathbf S_i\cdot\mathbf S_j=\tfrac12(\mathbf S_\text{tot}^2-3S^2)$,
  which is smallest for $\mathbf S_\text{tot}=0$, three spins at $120^\circ$ in a plane.
- Lab box, with the source and the number that the source states: the kagome magnet ZnCu$_3$(OH)$_6$Cl$_2$,
  named by its formula, since the abstract does not use the name herbertsmithite,
  https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.98.107204, stored as
  `helton2007_physrevlett.98.107204.txt`. The arXiv abstract says "The susceptibility indicates a Curie-Weiss
  temperature of ~ -300 K; however, no magnetic order is observed down to 50 mK." The probes are the
  susceptibility and neutron scattering. That $|\theta_\mathrm{CW}|$ is set by $J$ and the factor of 6000
  between the two temperatures are ours. The box says that this kagome magnet does not order at all, so it
  points to Session 8 and does not claim the $120^\circ$ order of the page.
- Pen-and-paper problem: the classical energy per site on the triangular lattice, for the $120^\circ$ state
  and for a collinear stripe state. Answer $-\tfrac32JS^2$ and $-JS^2$, since each site has three bonds in the
  first, and two parallel and four antiparallel neighbors in the second.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the ferromagnetic triangular
  lattice has a question of 20 words and cites "the convention of (6.5)". It gets short sentences with
  $H=J\sum\mathbf S_i\cdot\mathbf S_j$ in the question. New, a picture question, "For $J>0$, which lattice is
  frustrated?", with the square, the honeycomb and the triangular lattice drawn as options. New, with
  equations as options, "Three classical spins of size $S$ sit on a triangle with $J>0$. What is the lowest
  energy?", the options $-\tfrac32JS^2$, $-JS^2$ and $-3JS^2$.
- Figures to add, each with its pyqula script or the reason for numpy: the text says that the mean-field
  solution of the electrons also converges to the noncollinear order. `triangular_meanfield.py` does it with
  pyqula, `geometry.triangular_lattice()`, a supercell of 3 by 3, $U=10$ and `mf="XY"`, as in notebook cell
  37. The figure draws the moments $m_x$, $m_y$ in real space with the axes $x$ and $y$, and an assert checks
  the angle between neighbors, with the range found over a few starting guesses. The lattice pictures of the
  quiz are drawings, `quiz_lattice_square.py`, `quiz_lattice_honeycomb.py`, `quiz_lattice_triangular.py` with
  `_lattices.py`. `hubbard_to_heisenberg` stays numpy, since it is the exact diagonalization of four Hubbard
  sites.
- Old figures of the page that break the plot rules: none. `hubbard_to_heisenberg` has named axes with units
  and ticks, and `triangle_bonds` is a drawing.

## 6.11 Superexchange as the origin of ferromagnetic coupling and 6.12 Anisotropic exchange with Dzyaloshinskii-Moriya, Ising and Kitaev terms

File `11-superexchange-as-the-origin-of-ferromagnetic-coupling.md`, 1281 words, numbered equations none.

- Question of the page, and where we arrive: if the direct mechanism is always antiferromagnetic, where do
  ferromagnets come from, and which other couplings appear with spin-orbit coupling? We arrive at the ligand
  process, which can be ferromagnetic, and at the Dzyaloshinskii-Moriya, Ising and Kitaev terms. The first
  paragraph of 257 words is split after "a second virtual process", and again before "The systematic
  version".
- Main result for the key box: an unnumbered display, since the page has no numbered equation. The term
  $\mathbf D_{ij}\cdot(\mathbf S_i\times\mathbf S_j)$ needs spin-orbit coupling and a broken mirror, and on a
  chain with $J>0$ it gives a spiral with $\cos\theta=-J/\sqrt{J^2+D^2}$ between neighbors.
- Equation of another page that it starts from, for the recall box: `eq="6.5"`.
- Derivation told in words, for a steps fold: "The angle of the spiral". Two classical spins in the plane at
  the angle $\theta$ give $S^2(J\cos\theta+D\sin\theta)$ per bond, which is smallest at
  $\cos\theta=-J/\sqrt{J^2+D^2}$ with the energy $-S^2\sqrt{J^2+D^2}$. Simplest case first, $D=0$ and
  $\theta=180^\circ$. The values $135^\circ$ for $D=J$ and $101^\circ$ for $D=5J$ are those of `dm_spiral`.
- Lab box, with the source and the number that the source states: monolayer CrI$_3$,
  https://www.nature.com/articles/nature22391, stored as `huang2017_nature22391.txt`. The arXiv abstract
  says "Here, we use magneto-optical Kerr effect (MOKE) microscopy to demonstrate that monolayer chromium
  triiodide (CrI3) is an Ising ferromagnet with out-of-plane spin orientation." and "Its Curie temperature of
  45 K is only slightly lower than the 61 K of the bulk crystal, consistent with a weak interlayer coupling."
  It also says that the anisotropy removes the restriction of the Mermin-Wagner theorem, which ties the box
  to the Ising-like exchange. This abstract does not say "insulator". If the box says it, the claim comes
  from `chen2018_physrevx.8.041028.txt`.
- Pen-and-paper problem: two antiparallel spins with a small $D$. Find the canting angle away from
  $180^\circ$ and the energy gained. Answer $\epsilon\simeq D/J$, which is $5.7^\circ$ for $D=0.1J$, and a gain
  of about $D^2S^2/2J$, that is $0.005JS^2$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on spin-rotation symmetry
  passes the lint and stays. New, a picture question, "Which chain has $D=J$?", with three rows of classical
  spins at $180^\circ$, $135^\circ$ and $101^\circ$ between neighbors as options. New, with equations as
  options, "Which coupling is zero for any two collinear spins?", the options
  $\mathbf D\cdot(\mathbf S_i\times\mathbf S_j)$, $\Lambda S^z_iS^z_j$ and $J\,\mathbf S_i\cdot\mathbf S_j$.
- Figures to add, each with its pyqula script or the reason for numpy: the pictures of the quiz,
  `quiz_spiral_180.py`, `quiz_spiral_135.py`, `quiz_spiral_101.py` with `_spiral.py`, in numpy, since a
  classical spin chain is not a pyqula calculation. As an option, the electronic counterpart of the try-it box
  with pyqula, `chain_rashba_meanfield.py`, a chain of 10 sites with `h.add_rashba(1.)` at $U=10$ and
  `mf="XY"`, as in notebook cell 31, with the angle between neighbors in the caption.
- Old figures of the page that break the plot rules: none. `ligand_exchange` and `dm_spiral` are drawings,
  and `s06f02_dimer` and `s06f04_kitaev` are converted figures.

## 6.13 Magnons as fluctuations of the order parameter and 6.14 The Holstein-Primakoff transformation

File `13-magnons-as-fluctuations-of-the-order-parameter.md`, 1222 words, numbered equations (6.6), (6.7).

- Question of the page, and where we arrive: what are the low-lying excitations of an ordered ferromagnet,
  and how do we write spins as bosons? We arrive at (6.6) and (6.7), and at a bosonic tight-binding
  Hamiltonian with the hopping $|J|S$. The paragraph of 176 words of 6.13 is split after "we ask for the
  low-lying excited states", and the one of 153 words of 6.14 before "The total magnetization".
- Main result for the key box: (6.7) with the counting rule, "$S^-$ creates a magnon, $S^+$ removes one, and
  $\sum_iS_i^z=NS-\sum_ia_i^\dagger a_i$". (6.6) stays in the text above it.
- Equation of another page that it starts from, for the recall box: `eq="6.5"`, with $J<0$ for the
  ferromagnet.
- Derivation told in words, for a steps fold: "From a ferromagnetic bond to the magnon hopping". Simplest
  case first, two sites. Insert (6.7) into $J\mathbf S_i\cdot\mathbf S_j$, keep the quadratic terms, and with
  $J=-|J|$ read off the onsite energy $|J|S$ per bond and the hopping $-|J|S$.
- Lab box, with the source and the number that the source states: none. The page builds the tool, and the
  measured magnon bands are on 6.15 and 6.16. The one candidate, SrRuO$_3$ in `jenni2023_arxiv2305.05497.txt`
  with 35 meV, has a quadratic dispersion "with an anisotropy gap" that (6.8) does not have, so it would
  stretch the source.
- Pen-and-paper problem: show that one magnon $|k\rangle=N^{-1/2}\sum_je^{ikj}S^-_j|\mathrm{FM}\rangle$ on a
  ring of $N$ spins $\tfrac12$ is an exact eigenstate. Answer $E-E_0=|J|(1-\cos k)$, which is
  $2|J|S(1-\cos k)$ for $S=\tfrac12$, with the largest value $2|J|$ at $k=\pi$. Checked by diagonalization of
  eight spins.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on creating a magnon passes
  the lint and stays. New, with equations as options, "Near saturation, which form does $S^+_i$ take?", the
  options $\sqrt{2S}\,a_i$, $\sqrt{2S}\,a_i^\dagger$ and $S\,a_i$. New, a picture question, "A ferromagnetic
  ring of spins $S=1$ has $|J|=1$. Which picture is its one-magnon band?", with three bands of largest value
  2, 4 and 8 as options, and $4|J|S=4$ is the answer.
- Figures to add, each with its pyqula script or the reason for numpy: the pictures of the quiz,
  `quiz_magnon_w2.py`, `quiz_magnon_w4.py`, `quiz_magnon_w8.py` with `_onemagnon.py`, in numpy, since they are
  the band $2|J|S(1-\cos k)$ that the problem derives and pyqula has no spin operators. `one_magnon` stays
  numpy, since it is an exact diagonalization of spins.
- Old figures of the page that break the plot rules: none. `one_magnon` has $k$ and $E/|J|$ with ticks, and
  `s06f05_magnon` is a converted figure.

## 6.15 Magnon dispersions in ferromagnets and antiferromagnets

File `15-magnon-dispersions-in-ferromagnets-and-antiferromagnets.md`, 1093 words, numbered equations (6.8), (6.9).

- Question of the page, and where we arrive: how does the magnon energy go to zero, in a ferromagnet and in
  an antiferromagnet? We arrive at the quadratic law (6.8) and the linear law (6.9). The opener replaces "We
  Fourier transform". The paragraph of 152 words on the antiferromagnet is split after "which do not conserve
  the particle number".
- Main result for the key box: two boxes, (6.8) with "quadratic at small $k$" and (6.9) with "linear at small
  $k$, because of the anomalous terms".
- Equation of another page that it starts from, for the recall box: `eq="6.7"`.
- Derivation told in words, for a steps fold: "The Bogoliubov transformation of the antiferromagnet". At one
  $k$, $H_k=JSz[a_k^\dagger a_k+b_{-k}^\dagger b_{-k}+\gamma_k(a_kb_{-k}+\text{h.c.})]$. A bosonic Bogoliubov
  transformation with $u_k^2-v_k^2=1$ gives $JSz\sqrt{1-\gamma_k^2}$ and
  $v_k^2=\tfrac12(1/\sqrt{1-\gamma_k^2}-1)$, the values that `afm_bogoliubov.py` asserts. The fold notes the
  sign under the root against the fermionic (5.9). The Fourier transform to (6.8) is one line in the text
  and gets no fold.
- Lab box, with the source and the number that the source states: the square-lattice antiferromagnet
  K$_2$V$_3$O$_8$, https://arxiv.org/abs/cond-mat/0609775, stored as `lumsden2006_arxivcond-mat-0609775.txt`.
  The abstract says "A small energy gap of 72+/-9 micro-eV is observed at the antiferromagnetic zone center
  and the near-neighbor exchange constant is determined to be 1.08+/-0.03 meV." The probe is inelastic
  neutron scattering. The abstract gives no velocity and no linear law, and it says that near the zone
  boundary the spectrum deviates from linear spin-wave theory, so the box computes no band energy from $J$.
  The gap comes from an anisotropy that (6.9) does not have, and the box says so.
- Pen-and-paper problem: expand (6.8) and (6.9) at small $k$ for the chain and the square lattice. Answers
  $|J|Sk^2$ and $2JS|k|$ for the chain, $|J|Sk^2$ and $2\sqrt2\,JS|k|$ for the square lattice, with $k$ in units
  of the inverse lattice constant.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on doubling $k$ cites (6.8) and
  (6.9) in its question. It writes the two dispersions of the chain, $1-\cos k$ and $|\sin k|$, in the question.
  The quiz at $(\pi,\pi)$ writes $E=|J|Sz(1-\gamma(\mathbf k))$ in its question, since its feedback uses
  (6.8). New, a picture question, "Which dispersion is the magnon of the antiferromagnetic chain?", with a
  parabola, a linear cone and a gapped parabola near $k=0$ as options.
- Figures to add, each with its pyqula script or the reason for numpy: `square_magnon` is a tight-binding
  band, so it is redrawn from `magnon_square.py` with pyqula, `geometry.square_lattice()`, the hopping
  $-|J|S$ and the onsite energy $z|J|S=4$, along $\Gamma$, $X$, $M$, $\Gamma$. An assert checks that the band is
  zero at $\Gamma$, and the sign of the hopping argument of pyqula comes from the sheet. The pictures of the
  quiz, `quiz_disp_fm.py`, `quiz_disp_afm.py`, `quiz_disp_gapped.py` with `_dispersions.py`, are numpy, since
  they are closed forms. `afm_bogoliubov` stays numpy, since pyqula has no bosonic Bogoliubov solver.
- Old figures of the page that break the plot rules: `afm_bogoliubov` (a) names its axis $E$ with no unit,
  and the unit $JSz$ is only in the caption. `square_magnon` names its axis $E$ with no unit, and its two
  values are written as labels beside the plot and not as ticks.

## 6.16 Topological magnons

File `16-topological-magnons.md`, 1090 words, numbered equations (6.10).

- Question of the page, and where we arrive: can magnon bands carry a Chern number? We arrive at a honeycomb
  ferromagnet with the Dzyaloshinskii-Moriya term, which is the Haldane model for magnons, with $C=\pm1$ and
  chiral magnon edge modes. The paragraph of 193 words is split before "We add to the plain Heisenberg
  exchange" and before "When we put such a topological magnon Hamiltonian on a ribbon".
- Main result for the key box: (6.10) with "for the honeycomb ferromagnet with $t=|J|S$ and $t_2=DS$, the gap
  at $K$ is $6\sqrt3\,DS$ and the two bands have $C=\pm1$".
- Equation of another page that it starts from, for the recall box: `eq="3.8"`, the Chern number of one
  gapped Dirac point, which says why a mass that is odd under time reversal gives $C=\pm1$. Not (3.4), since
  (6.10) is the same integral.
- Derivation told in words, for a steps fold: "From the Dzyaloshinskii-Moriya term to a complex hopping".
  $\hat z\cdot(\mathbf S_i\times\mathbf S_j)=\tfrac i2(S_i^+S_j^--S_i^-S_j^+)$, and with (6.7) this becomes a
  hopping $\pm iDS$, which is $DS\,e^{\pm i\pi/2}$. Which sign goes with which turn comes from the sheet.
- Lab box, with the source and the number that the source states: CrI$_3$,
  https://journals.aps.org/prx/abstract/10.1103/PhysRevX.8.041028, stored as
  `chen2018_physrevx.8.041028.txt`, a candidate of the notebook. The arXiv abstract says "Using inelastic
  neutron scattering, we find that spin waves of the insulating honeycomb ferromagnet CrI3 (TC=61 K) have two
  distinctive bands of ferromagnetic excitations separated by a ~4 meV gap at the Dirac points." The
  abstract reports a gap and a model with the DM interaction. It does not report edge modes or a Chern
  number. $DS\simeq0.4$ meV from $6\sqrt3\,DS=4$ meV is ours.
- Pen-and-paper problem: show that the gap at $K$ is $6\sqrt3\,DS$. At $K$ the first-neighbor term vanishes
  and the second-neighbor term gives $\pm3\sqrt3\,DS$ on the two sublattices. Answer $1.04$ for $t_2=0.1$,
  in units of $|J|S$.
- Quizzes to rewrite, and a picture question or equations as options: the two quizzes pass the lint. The
  feedback "Reversing the vector is a mirror operation" of the second one is listed in "Open for the
  lecturer". New, a picture question, "Which ribbon has magnon bands with $C=\pm1$?", with three ribbon
  spectra as options, the DM term with an edge branch crossing the gap, a staggered onsite energy with an empty
  gap, and $t_2=0$ with no gap. This makes three quizzes.
- Figures to add, each with its pyqula script or the reason for numpy: the bands and the ribbon are pyqula
  calculations. `magnon_honeycomb.py` with `geometry.honeycomb_lattice()`, `has_spin=False`, the Haldane
  coupling, `h.add_onsite(3.)` for the constant $z|J|S$, the bands along $\Gamma$, $K$, $M$, $\Gamma$ and
  `h.get_chern()`. The Chern number of pyqula counts the states below zero energy, so `h.get_chern()` is
  called before `h.add_onsite(3.)`, since the constant does not change the states. `magnon_ribbon.py` with a zigzag ribbon and `get_bands(operator="yposition")`, as in the
  recipe of the ribbon and notebook cell 48. They replace the numpy `_haldane.py` for `dm_honeycomb` (b) and
  `ribbon_magnons`. `h.add_haldane(x)` is $t_2=(\sqrt3/2)x$, so $t_2=0.1$ with the gap $1.04$ of the caption
  needs $x=0.1155$, and the caption says which one it uses. The pictures of the quiz come from the same pyqula
  code, `quiz_ribbon_chern.py`, `quiz_ribbon_trivial.py`, `quiz_ribbon_gapless.py` with `_ribbonquiz.py`.
  Panel (a) of `dm_honeycomb`, the drawing of the phases, stays.
- Old figures of the page that break the plot rules: `dm_honeycomb` (b) names its axis $E$ with no unit and
  no number, so the gap $1.04$ is not on an axis. Its bands are symmetric around zero, since the constant
  $3|J|S$ is left out, and so the lower band has negative magnon energies. `ribbon_magnons` has $k_x$ and $E$
  with no tick and no unit, and it leaves out the same constant. With the constant the lower band starts at
  zero at $\Gamma$, the Goldstone mode of 6.15, which the redraw asserts.

## 6.17 Closing summary

File `17-closing-summary.md`, 633 words, numbered equations none. A closing page.

- Question of the page, and where we arrive: the page opens with what we started from, and it keeps its
  form. It gets the list "After this session we can do the following tasks", each task with its section.
  Write a mean-field Hubbard Hamiltonian and read the exchange splitting $Um$, in Section 6.3. Decide from the
  total energies which of two self-consistent solutions is the ground state, in Section 6.5. Check the Stoner
  criterion for a given density of states, in Section 6.6. Derive $J=4t^2/U$ from the Hubbard dimer, in
  Section 6.8. Tell a bipartite lattice from a frustrated one and find the classical $120^\circ$ state, in
  Sections 6.9 and 6.10. Say which exchange terms need spin-orbit coupling, in Section 6.12. Write a spin
  Hamiltonian as bosons with Holstein-Primakoff, in Section 6.14. Tell the ferromagnetic magnon from the
  antiferromagnetic one by its small-$k$ law, in Section 6.15. Compute the gap and the Chern number of the
  honeycomb magnon bands, in Section 6.16.
- Main result for the key box: none, a closing page.
- Equation of another page that it starts from, for the recall box: none, the bullets already link the
  numbered equations.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, a closing page.
- Pen-and-paper problem: none, a closing page.
- Quizzes to rewrite, and a picture question or equations as options: the Goldstone quiz passes the lint and
  stays. No new quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, the panel of `s06f06_dispersion` has named axes.

## Candidates for the lab boxes

Every source was fetched on 2026-11-21 with `webnotes/labsource.py --session 6`. Each quoted sentence above
was checked by a script to be a substring of the abstract block of its file in `webnotes/sources/.full/session06/`,
not of an editor summary, and to hold the number. `labsource.py --check 6` reads the boxes of the pages, so it
runs after the builders.

The first four are the cells "In the lab" of `session6.ipynb`.

- NiI$_2$, https://www.nature.com/articles/s41586-021-04337-x, `song2022_s41586-021-04337-x.txt`, with the
  arXiv abstract 2106.07661. No number with a unit, so no box.
- 1T-NbSe$_2$, https://www.science.org/doi/10.1126/sciadv.abi6339, `liu2021_sciadv.abi6339.txt`, with the
  arXiv abstract 2103.12948. No number with a unit, so no box.
- Graphene multilayers, https://www.science.org/doi/10.1126/science.aar6855, `nam2018_science.aar6855.txt`.
  12 K and 100 K, planned on 6.2 and 6.3.
- CrI$_3$ magnons, https://journals.aps.org/prx/abstract/10.1103/PhysRevX.8.041028,
  `chen2018_physrevx.8.041028.txt`. 4 meV and 61 K, planned on 6.16.

The others are articles fetched for the pages.

- Zigzag nanoribbons, `magda2014_nature13831.txt`, 0.2 to 0.3 eV and 7 nm, planned on 6.4 and 6.5.
- Twisted bilayer graphene, `sharpe2019_science.aaw3780.txt`, 10.4 kΩ, planned on 6.6 and 6.7.
- Clar's goblet, `mishra2020_s41565-019-0577-9.txt`, 23 meV, planned on 6.8.
- ZnCu$_3$(OH)$_6$Cl$_2$, `helton2007_physrevlett.98.107204.txt`, 300 K and 50 mK, planned on 6.9 and 6.10.
- Monolayer CrI$_3$, `huang2017_nature22391.txt`, 45 K and 61 K, planned on 6.11 and 6.12.
- SrRuO$_3$, `jenni2023_arxiv2305.05497.txt`, 35 meV. Not used, since its quadratic dispersion has an
  anisotropy gap that (6.8) does not have.
- K$_2$V$_3$O$_8$, `lumsden2006_arxivcond-mat-0609775.txt`, 1.08 meV and 72 µeV, planned on 6.15.
- Rhombohedral trilayer graphene, `zhou2021_s41586-021-03938-w.txt`. It names the Stoner model, but it
  has no number with a unit, so no box.
- La$_2$CuO$_4$, `coldea2001_physrevlett.86.5377.txt`, and Ba$_3$CoSb$_2$O$_9$, `shirata2011_arxiv1110.3889.txt`
  and `ma2016_arxiv1507.05702.txt`. No number with a unit in the abstracts, so no box.

## Builder groups

Five groups, in the order of the pages. Two rules hold for all of them. A pyqula redraw must give the
numbers that the old scripts assert and the pages quote, which are $0.77$, $0.98$, $0.8t$, $0.1995$, $0.0999$
and $1.04$. If it does not, the figure stays numpy and the builder reports it. A quantity that two groups
state is looked up on the page of the other group before it is written. `g2_` and `g3_` both state
$4t^2/U$ per cell of two sites, and `g4_` and `g5_` both state the magnon hopping $-|J|S$ and the constant
$z|J|S$.

- `g1_`: `index.md`, `01-two-classes-of-magnets-and-their-excitations.md`,
  `02-a-recap-of-symmetry-breaking-and-the-mean-field-philosophy.md`. The index gets one opening question.
  (6.1) and (6.2) are (1.7) and (1.8) again, so 6.3 has no recall box. The lab box of 6.3 quotes only the
  arXiv abstract of Nam, which does not name the probe.
- `g2_`: `04-exchange-splitting-and-antiferromagnetic-order-in-numerical-mean-field-theory.md`,
  `06-the-stoner-threshold-as-a-criterion-for-magnetism.md`. Both use `_mf.py` and the mean field of the chain
  in pyqula. The `filling` of pyqula counts both spins, so $n=0.2$ is probably `filling=0.1` as in notebook
  cell 21, and the sheet confirms it. The energy unit of `return_total_energy` is from the sheet. Items 1 and 2
  of "Open for the lecturer" stop panel (b) of `mf_chain` and the curve of $m$ for the chain at $n=0.2$.
- `g3_`: `08-from-the-hubbard-dimer-to-the-heisenberg-model.md`,
  `09-the-heisenberg-model-on-a-general-lattice.md`,
  `11-superexchange-as-the-origin-of-ferromagnetic-coupling.md`. They share `s06f02_dimer` and the Heisenberg
  model, and the sign convention $J>0$ antiferromagnetic of 6.9. After the Mishra box run `labsource.py
  --quotes`, since that text was pasted by hand. The 120 degree angle of the pyqula mean field depends on the
  starting guess, so it is given as a range.
- `g4_`: `13-magnons-as-fluctuations-of-the-order-parameter.md`,
  `15-magnon-dispersions-in-ferromagnets-and-antiferromagnets.md`. They share the Holstein-Primakoff
  magnon. The magnon hopping is $-|J|S$, and the sheet gives the pyqula argument that makes the square-lattice
  band zero at $\Gamma$. Page 13 gets no lab box.
- `g5_`: `16-topological-magnons.md`, `17-closing-summary.md`. `_haldane.py` stays inside 16.
  `h.add_haldane(x)` is $t_2=(\sqrt3/2)x$ and the gap is $9x$, so $t_2=0.1$ is $x=0.1155$. The magnon
  energies include $3|J|S$, and `h.get_chern()` is called before the shift. The sign of $C$ against the sign
  of $D$ comes from the sheet. Page 17 gets the list of tasks.

## Open for the lecturer

The lecturer decided on 2026-11-22 to "Fix old-text errors, ask the rest", and for the questions "ask me the top 5, other
you decide by yourself". The points of the builders, of the fixers and of the rechecks, 40 entries with repeats, and the
five points of the first version of this section were merged into 29 distinct points. None of them was marked "NOT FIXED"
or "new wrong", so the eight points of the rechecks came first. A sentence that was false, or that contradicted another
sentence of the notes, is corrected on the web with the smallest change, after a calculation of our own, by two routes
where it is a number, and every number that changed or was added is an assert in `webnotes/checks/session06/`, in a block
marked with the date, or in the figure script. A point that is a choice was decided by the coordinator with the rule of
that day. It takes the option that makes the text true with the smallest change, and between two true wordings the
shorter and clearer one, reduces a claim to what a source or a calculation supports, rewrites a box that does not match
its notebook cell, and corrects an outdated line of the conventions sheet with its check. A point whose fix would change a
numbered equation, a convention or a heading is left for the lecturer. No numbered equation changed, no converted Blender
figure was touched, and the notebooks were not edited. The fields "Old figures of the page that break the plot rules" of
the blocks above describe the figures before this pass, and panel (b) of `mf_chain` is now redrawn. The line numbers are
those of `lecture_notes/src/sessions/session06.tex` on 2026-11-22, commit `bf5b1be`. The `.tex` is not changed in this
pass, so until the first list is carried over the PDF keeps the old wording in these places.

An independent check of the same day read these corrections again and found eight points, k1 to k8. Seven of them made a
new text more exact, and they are in items 6, 11, 13, 14, 15, 17, 18 and 25 below, each with its new assert. For k2 our
runs do not confirm the cause that the check gave, and item 11 says so. The eighth, k3, showed that the change to the
solution of page `16` picks one corner of the zone, which is a convention, so that change was reverted, and it is now the
point that is left for the lecturer. The lecturer picked the two other points on 2026-11-22, items 13 and 14 of the
second list, and the change of the first one is item 27 below.

### Corrected on the web, to carry over to the .tex

1. Page `01`, Section 6.1, `.tex` lines 58 and 59. Old "Magnons have no charge, so electric fields do not affect them at
   all, and they can propagate in materials that are electronic insulators." New "Magnons have no charge, so an electric
   field does not push them as it pushes an electron, and they can propagate in materials that are electronic
   insulators." `g1_01` asserts that a potential $V_in_i$ commutes with $S^-$ of each site, and that a potential
   difference $V=4t$ between the two sites of the dimer at $U=20t$ raises the singlet-triplet splitting from $0.198t$ to
   $0.206t$, close to $4t^2U/(U^2-V^2)=0.208t$, so an electric field does change the magnon energy.
2. Page `02`, Section 6.3, `.tex` lines 114 and 115. Old "Self-consistency gives $m=0$ for $U<0$ and a magnetic solution
   with $m\neq 0$ for $U>0$, as in Section 1.14." New "Self-consistency gives $m=0$ for $U<0$, and in the half-filled
   chain a magnetic solution with $m\neq 0$ for every $U>0$, as in Section 1.14." The comesback box of the same page, not
   in the `.tex`, now reads "the threshold of $U$ above which a uniform magnetization $m$ of (6.2) appears". `g1_02`
   asserts that for $U<0$ the uniform energy grows with $m$ and the gap equation has a negative right side, and the
   staggered moment $0.0299$ at $U=t$.
3. Page `04`, Section 6.4, `.tex` line 142. Old "with a unit cell of one site at 20\% filling". New "with a unit cell of
   one site and $n=0.2$ electrons per site". The caption gives $n=0.2$, which is `filling=0.1`, 10 percent of the states.
   `g2_04` asserts $|m|=0.200$ and $Um=0.800$ for `filling=0.1`.
4. Page `04`, the notebook box of Section 6.4, `.tex` lines 159 to 161. Old "The ferromagnetic case with one site per cell
   at 20\% filling, from the same section, is the companion calculation." New "The ferromagnetic case with one site per
   cell and $n=0.2$, which is `filling=0.1`, is the companion calculation, and it is in the cell "(Exercise) Intermediate
   coupling regime and Stoner instability"." The cell of the box title is the bichain at half filling. `g2_04` reads the
   two cells.
5. Page `04`, Section 6.5, `.tex` lines 166 to 168. Old "It is the paramagnet below $U\approx 4t$ and a fully polarized
   ferromagnet above it". New "Its lowest state is the paramagnet below $U=16t/\pi\approx5.1t$ and a fully polarized
   ferromagnet above it". The saturated ferromagnet is a solution from $4t$, the problem of the page, and lower than the
   paramagnet, $-4t/\pi+U/4$ per site, only from $16t/\pi$. `g2_04` asserts the crossing $5.093t$ by the closed form and
   by a mesh of the filled bands over $m$, and the lowest $m$ at $4t$, $4.5t$, $5t$, $5.2t$ and $6t$.
6. Page `04`, Section 6.5, `.tex` lines 171 to 173. Old "Opening a gap pushes the occupied single-particle energies down,
   so the insulating configuration has a lower total energy than the gapless ferromagnetic one for every $U>0$ that we can
   reach numerically in this half-filled chain." New "Below $16t/\pi$ the lowest uniform state is the paramagnet, which has
   no gap, and opening a gap pushes the occupied single-particle energies down. Above $16t/\pi$ the lowest uniform state is
   the saturated ferromagnet, which has the gap $U-4t$ too. There the antiferromagnet stays lower by about $2t^2/U$ per
   site, the energy of the virtual hops that the Pauli principle blocks in the ferromagnet." The first correction of the
   day changed only "the gapless ferromagnetic one" to "the uniform one", and the independent check found that its reason,
   the gap, then held only below $16t/\pi$. `g2_04` asserts the gap $0.1$ at $4.1t$ and $2$ at $6t$, the antiferromagnet
   below the lowest uniform state at eight values of $U$, and the second-order energy $-2t^2/U$ of a classical Néel bond
   against zero for a parallel one, and `mf_chain.py` asserts the ratio to $2t^2/U$ above $0.96$ above the kink.
7. Page `04`, the caption and the alt text of `mf_chain` (b), not in the `.tex`. Old "(b) The energy per site that the
   antiferromagnet gains over the uniform solution. The jump at $4t$ is where the uniform solution changes from the
   paramagnet to the fully polarized ferromagnet, and above it the curve follows $2t^2/U$." New "(b) The energy per site
   that the antiferromagnet gains over the lowest uniform solution. The kink at $16t/\pi\approx5.1t$, where the curve is
   largest, is where the lowest uniform solution changes from the paramagnet to the fully polarized ferromagnet, and above
   it the curve approaches $2t^2/U$." Panel (b) is redrawn under the same name against the lowest uniform state, with $U/t$
   and $(E_\mathrm{uniform}-E_\mathrm{AFM})/t$ on its axes and ticks. `mf_chain.py` asserts no jump at the kink, the
   largest value $0.378$ there, and the ratio to $2t^2/U$ above $0.96$ above the kink and above $0.99$ from $10t$.
8. Page `04`, the solution of the problem, not in the `.tex`. Old "At $U=3.9t$ the loop leaves the saturated state, and
   where it ends depends on `mix`, the weight of the new mean field in each step. With `mix=0.9` it stops close to the
   paramagnet, ... With a smaller `mix`, such as $0.5$, it reaches the antiferromagnet, which is lower in energy." New "At
   $U=3.9t$ the loop leaves the saturated state. Where it ends depends on `mix`, the weight of the new mean field in each
   step, and on `maxerror`, the change of the mean field below which the loop stops. With `mix=0.9` and the default
   `maxerror=1e-5` it stops close to the paramagnet, ... This end is an early stop. With a smaller `mix`, such as $0.5$, or
   with `maxerror=1e-9`, the loop runs longer and reaches the antiferromagnet, which is lower in energy. In these runs its
   moment ends in the plane $xy$, so $|m|$ is read from $m_x$, $m_y$ and $m_z$." `g2_04` asserts the default `maxerror`,
   the stop rule of the loop, $|m|=0.75815$ and $-0.95905$ per cell with `maxerror=1e-9` on `nk` 40 and 41, and $m_z$
   below $10^{-4}$.
9. Pages `04`, `06` and `11`, the word "Schematic" before a link `[](#sch:...)`, which rendered as "Schematic Schematic
   6.3", "6.5" and "6.9". Not in the `.tex`. Now "The two solutions are drawn in [](#sch:s06:fm_afm_chain).", "We see in
   [](#sch:s06:moment_vs_U) how the chain gets there." and "We see in [](#sch:s06:dm_spiral) how the angle between neighbors
   depends on the strength of the term."
10. Page `06`, Section 6.6, `.tex` lines 203 and 204. Old "Below the threshold only $m=0$ is stable, and the system stays
    nonmagnetic for any perturbation." New "Below the threshold a small magnetization dies away, so the state with $m=0$ is
    stable against it." Between $1.926t$ and $1.942t$ at $n=0.2$ the saturated state is lower. `g2_06` asserts the sign of
    the curvature of $E(m)$ at $m=0$ below and above $1.94t$.
11. Page `06`, Section 6.6, `.tex` lines 209 to 213. Old "The self-consistent magnetization of the chain stays at zero
    below a critical $U$, and it grows continuously once $U$ is above this threshold. Figure 6.1 shows both parts of this
    statement together. It shows why a nontrivial solution of the self-consistency condition only exists above the
    threshold, and how the resulting magnetization curve looks." New "The self-consistent magnetization of the chain stays
    at zero below a critical $U$, and it is finite above it. In mean field it does not grow continuously, since the
    uniform chain jumps to the full moment. At $n=0.2$ it jumps from $m=0$ to $m=0.2$ at $U=1.93t$, just below the value
    $1.94t$ of (6.3). The cell of the notebook can end at a moment between $0$ and $0.2$. At $U=1.8t$ its title shows
    $0.13$, for a state above $m=0$ in energy that the finite k-mesh keeps, while it shows $0$ at $1.2t$ and $0.2$ at $2.4t$.
    Figure 6.1 shows why a nontrivial solution of the self-consistency condition only exists above the threshold, for a
    model of $f(m)$ where the magnetization grows continuously." The paragraph is split before "In the numerics", for its
    length. The sentences on the cell were added after the independent check, which called the state at $1.8t$ an early
    stop. Our runs do not confirm that cause: with `maxerror=1e-12`, or with `mix=0.5`, the loop ends in the same state,
    with $0.0867$ on the mesh of `nk=300` and $0.093$ on `nk=301`, which is $26/300$ and $28/301$, while $E(m)$ of the
    continuum has no stationary point between $0$ and $0.2$ at $1.8t$. `g2_06` asserts $1.9257t$ by the closed form and by
    the mesh, $1.9416t$, the two sides of the jump with the call of the notebook cell, below $0.015$ at $1.2t$ and $0.200$
    at $2.4t$, the titles $0.0$, $0.13$ and $0.2$ of the cell as written and $0.13$ with `nk=301`, the energy above $m=0$,
    $0.00025t$ per site by the total energy of pyqula and $0.00026t$ by the closed form, and the continuous rise of the
    model $\tanh(sm)$.
12. Page `06`, the solution of the problem, not in the `.tex`. Old "With the default `nk` and `delta` the value is off by
    more than $10$ percent close to the center of the band of the chain, above or below." New "With the default `nk` and
    `delta` the value on the chain can be off by up to $18$ percent close to the center of the band, above or below,
    depending on the energy." `g2_06` asserts $-15.2$ to $+17.9$ percent for $|E|<0.5t$, with pyqula and with a Lorentzian
    sum of our own on `nk=100` with `delta=0.05`.
13. Page `08`, the notebook box of Section 6.8, `.tex` lines 323 to 326. Old "Diagonalize the Hubbard dimer with six states
    directly, ... with a direct numerical diagonalization." New "The first cell has no interaction, and it gives the
    single-particle levels $\pm t$ of the dimer. The other three use mean field, and not the six states of this section.
    The second one solves the dimer in mean field, where a moment appears only above $U=2t$, while the exact dimer of this
    section has a singlet ground state with no ordered moment. The third one follows the mean-field gap of the chain as $U$
    grows. The last one compares the energies of the ferromagnet and the antiferromagnet at large $U$, whose difference
    falls as $1/U$, as the coupling $J$ of (6.4) does." The first two sentences and "no ordered moment" come from the
    independent check, since the first cell has no interaction and the singlet has a local moment. `g3_08` reads the four
    cells, asserts that the first one calls no mean field and the other three do, and asserts the levels $\pm1$, each
    twice.
14. Page `08`, the try-it box, not in the `.tex`. Old "In the cell, diagonalize the dimer with six states for $U/t$ equal
    to 4, 8 and 16. ... about 0.83, 0.94 and 0.98, ..." New "In the cell, the dimer is solved in mean field for `Us` from 0
    to 10. The moment of a site stays at zero up to $U=2t$ and then grows as $\sqrt{1-4t^2/U^2}$, to $0.87$ at $U=4t$ and
    $0.98$ at $10t$, and the gap goes from $2t$ to $U$. The exact dimer of this section has no ordered moment at any $U$,
    meaning that $\langle n_\uparrow-n_\downarrow\rangle=0$ on each site, since its ground state is the singlet. Its local
    moment $\langle(n_\uparrow-n_\downarrow)^2\rangle$ is still $0.85$ at $U=4t$. So the ordered moment of the cell comes
    from mean field." The ratios stay in the key box and the problem. The local moment was added after the independent
    check. `g3_08` asserts the call of the cell at five values of $U$ against the closed form, $\mathbf S^2=0$ and
    $\langle n_\uparrow-n_\downarrow\rangle=0$ in the exact ground state, and the local moment $0.854$ at $4t$ by the six
    states and by the weight $1/(1+E_S^2/4t^2)$ of the covalent singlet, with $0.765$ at $2.5t$ and $0.964$ at $10t$.
15. Page `09`, Section 6.10, `.tex` lines 358 and 359. Old "In the large-$U$ limit, the mean-field Hubbard model on a
    bipartite lattice reduces to this Heisenberg model." (the `.tex` has "reduces exactly"). New "In the large-$U$ limit,
    the mean-field Hubbard model on a bipartite lattice gives this Néel state, and not the quantum ground state of this
    Heisenberg model. Its energy is the one of classical spins once we add the constant $-J_{ij}/4$ per bond that (6.5)
    leaves out.", in a paragraph of its own for the length. The sentence on the constant comes from the independent check,
    since classical antiparallel spins $\tfrac12$ give $-J/4$ per bond in (6.5) as written. `g3_09` asserts $-J/2$ per bond at $U=20t$ and $40t$, on the chain from the gap
    equation and on the square lattice from a mean field of our own, $-J/4-J/4=-J/2$ for the classical Néel bond with the
    constant, and $-0.4515J$ per bond for the exact ring of 10 spins.
16. Page `11`, Section 6.12, `.tex` lines 416 to 418. Old "It requires broken mirror symmetry, which is the reason why it
    is strong at surfaces and interfaces, where the substrate itself breaks this mirror symmetry." New "It requires a bond
    with no inversion center, which is the reason why it is strong at surfaces and interfaces, where the substrate itself
    breaks the inversion symmetry." `g3_11` finds the allowed $\mathbf D$ for random spins, none for an inversion center at
    the middle of the bond, one direction for a mirror that contains the bond and two for a mirror normal to it.
17. Page `11`, the notebook box of Section 6.12, `.tex` lines 440 to 442. Old "Add a term of Dzyaloshinskii-Moriya type to
    the mean-field Hamiltonian, and see how the ground state tilts away from collinear order. This is the electronic
    counterpart of the statement above for the spin model." New "The cell adds the Rashba spin-orbit coupling to a Hubbard
    chain of 10 sites and solves it in mean field, starting from a random guess in the plane $xy$. The moments of the
    solution leave this plane, and the arrows of the cell show only the $x$ and $y$ components of the mean field, which
    points opposite to the moment. On this chain the Rashba hopping turns the spin by $90^\circ$ about $y$ on every bond,
    and a change of the spin axes from site to site removes it. So the mean field has the same energy for every angle
    between neighbors from $90^\circ$ to $180^\circ$, and the random guess of the cell picks one. This is not the spiral of
    the key box." The first correction of the day said "with the moments in the plane", which the independent check found
    false: in the turned frame the staggered moment is one vector $\mathbf n$, and the moments lie in the plane $xy$ only
    for $\mathbf n$ along $y$, the angle of $180^\circ$. `g3_11` asserts the bond matrix, the map onto the plain chain with
    the hopping $\sqrt2$, eight guesses with one energy within $10^{-5}$ and angles between $90^\circ$ and $180^\circ$ that differ by more than
    $20^\circ$, from $91.5^\circ$ to $126.7^\circ$ in the middle of the chain, the
    largest $|m_z|/|m|$ above $0.1$ in each of them (from $0.57$ to $0.97$), the guess of pyqula in the plane $xy$, and the
    drawn field $-\tfrac U2\mathbf m=-5\mathbf m$.
18. Page `11`, the try-it box, not in the `.tex`. Old "Without it, neighboring spins are antiparallel, and with it the
    angle between neighbors moves away from 180 degrees." New "Without it, neighboring spins are antiparallel. With it, the
    angle between neighbors moves away from 180 degrees and changes from run to run, since the random guess picks it,
    while the energy stays the same. With the default `maxite=1000` the loop stops without converging in most runs, so add
    `maxite=4000` to the call." The first correction of the day said "If the loop does not converge", and the independent
    check found that failure is the common case. `g3_11` asserts that at least five of the guesses 0 to 7 stop with
    `MeanFieldConvergenceError` at the default `maxite=1000`, seven in the development tree at commit `7567127`, all but
    the seed 1, and that all eight converge with 4000. The release 0.0.96 was not run.
19. Page `13`, Section 6.13, `.tex` lines 453 and 454. Old "since for $J<0$ no other configuration can lower $\langle
    \mathbf S_i\cdot\mathbf S_j\rangle$ further." New "since for $J<0$ no other configuration can make $\langle \mathbf
    S_i\cdot\mathbf S_j\rangle$ larger than $S^2$, its value in this state, on any bond." `g4_13` asserts the largest
    eigenvalue $S^2$ of one bond for $S$ from $\tfrac12$ to $\tfrac32$, and $-N|J|S^2$ for the exact rings, $-2.0$, $-2.5$
    and $-6.0$.
20. Page `13`, the recall box, not in the `.tex`. Old "Through the direct hop $t_{ij}$ between two sites, the Hubbard model
    gives the superexchange $J_{ij}=4t_{ij}^2/U>0$, which is antiferromagnetic." New "For $U$ much larger than $t_{ij}$ and
    one electron per site, the direct hop $t_{ij}$ between two sites gives $J_{ij}=4t_{ij}^2/U>0$, which is
    antiferromagnetic." The noun "superexchange" is dropped there, see item 14 of the decided points. `g4_13` asserts
    the exact ratio $0.828$, $0.944$ and $0.9975$ at $U=4t$, $8t$ and $40t$.
21. Page `15`, the caption of `afm_bogoliubov` (b), not in the `.tex`. Old "It is nonzero, so the magnon vacuum is not the
    boson vacuum, which is the Néel state." New "It is zero only at $k=\pm\pi/2$, where $\gamma_k=0$, and positive
    everywhere else, so the magnon vacuum is not the boson vacuum, which is the Néel state." `g4_15` asserts the two zeros
    and $1.1919$ at $k=0.3$, by the closed form and by the Bogoliubov matrix of the fold.
22. Page `16`, Section 6.16, `.tex` lines 569 and 570. Old "now to the bosonic Bogoliubov Hamiltonian of Section 6.15
    instead of an electronic tight-binding Hamiltonian." New "now to the bosonic tight-binding Hamiltonian of the magnons
    of Section 6.14 instead of an electronic one." `g5_16` asserts that the exact Hamiltonian keeps $S^z_\text{tot}$, so it
    has no anomalous term.
23. Page `16`, the solution of the problem, not in the `.tex`. Old "It survives because two parallel spins have $\mathbf
    S_i\times\mathbf S_j=0$, meaning that a uniform tilt of all the spins costs no Dzyaloshinskii-Moriya energy." New "It
    survives because each site has as many left turns as right turns to its second neighbors. So at $\Gamma$ the
    Dzyaloshinskii-Moriya hops into a site add up to zero, and a uniform tilt of all the spins costs no energy." `g5_16`
    asserts three left and three right turns on each sublattice, and an open flake of two hexagons where the uniform tilt
    has zero mean energy but the lowest one-magnon level is $-0.025|J|S$.
24. Page `16`, the try-it box, not in the `.tex`. Old "Change it to `-0.1` and compute `h.get_chern()` before building the
    ribbon. The Chern number changes sign." New "Change it to `-0.1` and run the cell again. In the ribbon the branch of
    each edge that crosses the gap now runs the other way, which is the change of sign of the Chern numbers. The cell does
    not compute the Chern number. A call of `h.get_chern()` after the line with `h.set_filling(0.0)` and `h.add_onsite(0.5)`
    gives 0.0 for both signs, since zero energy is then below both bands." `g5_16` runs the cell for both signs, with the
    bands from 0.499.
25. Page `17`, the third option of the quiz, not in the `.tex`. Old "An easy-axis anisotropy $A\,(S^z)^2$ keeps the magnon
    neutral but opens a gap of order $A$." New "An easy-axis anisotropy $A\,(S^z)^2$ with $A<0$ keeps the magnon neutral,
    but for $S\geq1$ it opens a gap. This gap is $|A|(2S-1)$ in the ferromagnet, and in linear spin waves a larger one, of
    order $S\sqrt{zJ|A|}$ for $|A|\ll zJ$, in the antiferromagnet." The first correction of the day gave only the gap of the
    ferromagnet, and the independent check found that the question names both dispersions. No number of a chain is given,
    since linear spin waves are not reliable on a chain of spins 1. `g5_17` asserts 0, 1 and 2 for $S=\tfrac12$, 1 and
    $\tfrac32$ on one site and on an exact ring of 4 spins, and for the antiferromagnet the gap
    $\sqrt{(zJS+a)^2-(zJS)^2}$ of linear spin waves by the closed form and by the Bogoliubov matrix, larger than the cost
    $a$ of one magnon on a site, $|A|(2S-1)$ or $2|A|S$, and between 1.4 and 2.1 times $S\sqrt{zJ|A|}$ for $|A|\leq0.05J$.
26. `webnotes/conventions/session06.md`, not in the `.tex`. The bullet of the uniform states now gives the end of the loop
    at $3.9t$ with `mix` and `maxerror` and reads $|m|$ from the three components, the bullet of the triangular lattice
    gives the reason of its $0.2^\circ$, the first bullet no longer says that the quiz of Section 6.3 uses the bold
    $\mathbf m$, and the section of the contradicted statements is now "settled on 2026-11-22", with each item marked.
    After the independent check, the bullet of the mean-field dimer gives no ordered moment and the local moment $0.854$ at
    $4t$, the bullet of the Rashba chain gives the moments out of the plane, the arrows of the cell as the field
    $-\tfrac U2\mathbf m$ and seven of eight seeds that raise at the default `maxite`, the bullet of the easy axis gives
    the gap of the antiferromagnet in linear spin waves, and the settled items of Sections 6.6, 6.8, 6.12 and 6.17 follow
    the pages. `conventions.py` checks the new numbers, 47 checks.
27. Page `02`, Section 6.3, `.tex` line 126, picked by the lecturer on 2026-11-22, item 13 of the second list. Old "and
    the resulting exchange field points along $\mathbf{m} \equiv \langle\mathbf{S}\rangle$, in \emph{any} direction where
    this expectation value is nonzero." New "... points along $\mathbf{m} \equiv 2\langle\mathbf{S}\rangle$, in
    \emph{any} direction where this expectation value is nonzero. With the factor 2, the component
    $m_z=2\langle S^z\rangle$ is the $m$ of (6.2)." The sentence of line 131, "noncollinear arrangements where
    $\mathbf{m}$ points in different directions on different sites", holds with the new definition and does not change,
    and no other line of the `.tex` writes the bold $\mathbf m$. The key box and the steps fold of the page, not in the
    `.tex`, write $2U|\langle\mathbf S\rangle|$ and $2\langle S^z\rangle=m$, which agree with it. No other page of the web
    notes writes the bold $\mathbf m$. `g1_02` asserts, for three mixed states of the site with the moment along $z$,
    along $x$ and along a tilted axis, that $\mathbf m=2\langle\mathbf S\rangle$ has $|\mathbf m|=0.2$ and
    $m_z=\langle n_\uparrow\rangle-\langle n_\downarrow\rangle$, equal to $0.2$, $0$ and $0.128$, that the Hartree-Fock
    field is $\tfrac U2n-\tfrac U2\mathbf m\cdot\boldsymbol\sigma$ with its lower level along $\mathbf m$ and the
    splitting $U|\mathbf m|=0.2U$ in each direction, and that the decoupling of $\mathbf S^2$ gives $\tfrac23U|\mathbf m|$.
    The first bullet of the conventions sheet and its item of Section 6.3 in the last section now give the picked
    definition, and `conventions.py` asserts $\mathbf m=(0,0,1)$ for one spin up, $(1,0,0)$ for the spinor
    $(1,1)/\sqrt2$, and the splitting $U|\mathbf m|=0.2U$ along $z$ and along $x$.

### Decided on 2026-11-22

The coordinator decided points 1 to 12 with the rule of that day, and the lecturer picked points 13 and 14 from the list
"For the lecturer". The changes of points 1 to 12 on the web are listed here and not in the list above, since the `.tex`
either has them already or does not have the sentence. The change of point 13 is item 27 of the list above.

1. "Iron for ferromagnets and antiferromagnets" on page `01`, which reads as if iron were an antiferromagnet. The
   coordinator by the rule: "iron for the family of ferromagnets and antiferromagnets", the reading of the `.tex`, lines 49
   to 51, which already says "iron for the ferromagnet and antiferromagnet family". No number.
2. The sentence of the recheck on page `06`, after "not above $4t$". The coordinator added "The saturated ferromagnet, a
   solution from $4t$ on, is already lower than the paramagnet from $16t/\pi$, about $5.1t$, so in mean field the uniform
   chain jumps to the full moment before this instability.", so that the three values $4t$, $5.1t$ and $6.3t$ of pages
   `04` and `06` agree. Asserted in `g2_06`.
3. Figure 6.1, the converted figure `s06f01_stoner`. The coordinator kept its render and its caption, since panel (a) says
   that it draws the shape $\tanh$ and for that model panel (b) does grow continuously. The text that reads it is item 11
   of the first list. Asserted in `g2_06`.
4. The caption of `dm_spiral`, "seen along $z$". The coordinator chose "seen looking along $\mathbf D$, which is from $-z$
   for $D>0$". The drawing turns each spin counterclockwise in the frame of the figure, which is the ground state seen
   from $-z$ for $D>0$ and from $+z$ for $D<0$, so the view along $\mathbf D$ holds for both signs and agrees with the
   label in the drawing. The drawing is not redrawn. Asserted in `g3_11`.
5. The third option of the second quiz of page `16`, "the phase $\varphi=+\pi/2$ gives $C=+1$", whose sign depends on
   which hops carry the phase. The coordinator chose, as the conventions sheet asks, "the phases $\varphi=+\pi/2$ and
   $\varphi=-\pi/2$ give opposite Chern numbers". Asserted in `g5_16`.
6. The feedback "Reversing the vector is a mirror operation, so the spectrum is the same" of the second quiz of page `16`.
   The coordinator kept it, since it holds. A mirror line along a first-neighbor bond keeps each sublattice and exchanges
   left and right turns, so the magnon matrix with $-D$ at $\mathbf k$ is the one with $+D$ at the mirror image of
   $\mathbf k$. `g5_16` asserts it within $10^{-12}$.
7. The notebook box of Section 6.6 on page `06`. The coordinator kept it, since the cell does compute $m$ against $U$, at
   $U$ from 0 to $3t$ in six steps.
8. The notebook box of Section 6.16, "compute its Chern number with (6.10)". The coordinator kept it, since it asks the
   student to compute it and does not say that the cell does. The try-it box, item 24 above, says that the cell does not.
9. `webnotes/scripts/RECIPES.md`, "within a quarter of a degree" in the recipe of the triangular lattice. Not edited,
   since it is a shared file of all the sessions and the sentence holds. The reason of the spread is now on the
   conventions sheet, item 26 above.
10. The folder `webnotes/figures/session06/__pycache__`, which is ignored by git. Left, since a recursive delete is not
    used in this pass.
11. The comesback box of Session 5, `session05/04-the-interacting-hamiltonian-and-the-origin-of-attractive-interactions.md`
    line 147, "in Section 6.6 we find the threshold of $U$ above which it appears", with the same reading as the old
    comesback of page `02`. Not applied, since it is a page of another session and a pointer that is true for a uniform
    magnetization. The sessions that close it can write "a uniform magnetization".
12. The phase rule "a hop along a vector $\mathbf d$ gives the phase $e^{i\mathbf k\cdot\mathbf d}$" of page `16` and of
    Section 3.10b, under which $\mathbf k$ is minus the momentum of the Bloch state, as the sheet says of `_haldane.hk`.
    Left, since it is a convention shared with Session 3 and no sentence is false with it stated. The point for the
    lecturer below holds with this rule for each of its options.
13. The bold $\mathbf m$ of Section 6.3, page `02`, `.tex` line 126, the former point 1 for the lecturer, next to the $m$
    of (6.2), which is $2\langle S^z\rangle$. Picked by the lecturer on 2026-11-22: "$\mathbf m\equiv2\langle\mathbf
    S\rangle$, so that $m_z$ is the $m$ of (6.2)", with every sentence of the session that uses the bold $\mathbf m$
    made to agree. The page and the `.tex` change in one symbol and one sentence, item 27 of the first list. The field is
    $-\tfrac U2\mathbf m\cdot\boldsymbol\sigma$ and its splitting $U|\mathbf m|$ in every direction, which `g1_02`
    asserts.
14. Which process the session calls superexchange, the former point 2 for the lecturer. Picked by the lecturer on
    2026-11-22: the word keeps both of its uses, the direct $t^2/U$ process on pages `08` and `09` and in the caption of
    Figure 6.2, and the exchange through a ligand in the heading of Section 6.11 and on page `17`. Nothing changes, and the
    recall box of page `13` keeps its wording without the noun, item 20 of the first list, since the point that the
    lecturer picked from said that this box no longer uses the noun. The independent check of the same day asked whether
    the box could take the noun back, now that the word is allowed for the direct process. It is not changed, since the
    pick says that nothing changes.

### For the lecturer

The lecturer picked the two other points of this list on 2026-11-22, and they are points 13 and 14 of the list
above. One point is left.

1. Which corner of the zone the solution of the problem of page `16` calls $\mathbf K$, not in the `.tex`. The solution
   reads "The three products $\mathbf K\cdot\mathbf b_n$ are all $2\pi/3$ modulo $2\pi$, so
   $\sum_n\sin(\mathbf K\cdot\mathbf b_n)=3\sqrt3/2$ and $m(\mathbf K)=-3\sqrt3\,DS$. The two energies are
   $3|J|S\mp3\sqrt3\,DS$". With the phase rule of the page, a hop along $\mathbf d$ gives $e^{i\mathbf k\cdot\mathbf d}$,
   and the $\mathbf b_n$ that turn left on $A$, these values hold at the point $(\mathbf B_1+\mathbf B_2)/3$ of pyqula,
   which is the corner $\mathbf K'=-\mathbf K$ of Section 2.11. At the corner $\mathbf K=(2\pi/3a,\,2\pi/3\sqrt3a)$ of
   Section 2.11 the three products are $-2\pi/3$ and $m(\mathbf K)=+3\sqrt3\,DS=+0.5196$ for $DS=0.1$, the value of
   Section 3.10b. The page does not say which corner it means, so the sentence is not false, and the gap $6\sqrt3\,DS=1.04$,
   the two levels $2.48$ and $3.52$ for $|J|S=1$ and the Chern numbers do not depend on which corner is named. A change of
   2026-11-22 to the $\mathbf K$ of Section 2.11 was reverted after the independent check of the same day, since it picks a
   convention. `g5_16` asserts the two corners, in the lattice of pyqula and in the frame of Section 2.11, and the levels
   $2.48$ and $3.52$.
   - Name the corner of Section 2.11, "For the corner $\mathbf K$ of Section 2.11, with this phase rule, the three
     products $\mathbf K\cdot\mathbf b_n$ are all $-2\pi/3$ modulo $2\pi$, as in Section 3.10b, so
     $\sum_n\sin(\mathbf K\cdot\mathbf b_n)=-3\sqrt3/2$ and $m(\mathbf K)=+3\sqrt3\,DS$. The two energies are
     $3|J|S\pm3\sqrt3\,DS$", which matches Sections 2.11 and 3.10b.
   - Keep the signs and name the other corner, "For the corner $\mathbf K'=-\mathbf K$ of Section 2.11 the three products
     ...", which keeps the numbers of the solution.
   - Keep the sentence as it is, with no corner named.
