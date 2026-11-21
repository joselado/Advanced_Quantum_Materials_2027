# Plan of Session 10 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session10.md`.

The conventions sheet of the session did not exist when this plan was written. The plan names pyqula calls
but states no sign of them, and a builder takes every sign from the sheet, or from `webnotes/scripts/RECIPES.md`
where the sheet is silent. The answers of the problems and the numbers of the new quizzes were computed for this
plan with small numpy checks and with copies of the numeric parts of the figure scripts, run in a scratch
folder, so that no SVG of `webnotes/figures/session10/` was written again. A builder computes them again in its
check script.

There is no notebook of Session 10, so every lab box comes from an arXiv abstract that was fetched with
`webnotes/labsource.py` and is stored in `webnotes/sources/session10/`. Each sentence quoted below was checked
by script to be in the stored full text. The tool checks only a number with a unit of its list, such as %, K,
meV or nm. Most numbers of this session are counts of atoms or spins, so the tool does not read them, and the
builder checks them by reading against the quoted sentence. A box with only such counts gives the warning
`lab-number` of the lint, and not a hit. Where the source writes a number as a word, the box keeps the word.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 461 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0) | 0 |
| `01-machine-learning-and-many-body-physics-in-two-directions.md` | 10.1, 10.2 | 1531 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, long-paragraph 4, opener 1, quiz-long 1 |
| `03-neural-network-quantum-states.md` | 10.3a | 943 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, opener 1, quiz-long 2 |
| `03b-training-the-network-and-quantum-state-tomography.md` | 10.3b | 1369 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `04-tensor-networks-for-machine-learning-and-the-many-body-wavefunction-as-a-big-data-problem.md` | 10.4 | 1350 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 2, opener 1, quiz-ref 1 |
| `05-machine-learning-in-density-functional-theory.md` | 10.5 | 1484 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, opener 1, quiz-long 1 |
| `06-phase-classification-with-local-order-parameters-and-topological-order.md` | 10.6a | 950 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 2, opener 1, quiz-ref 1 |
| `06b-the-hard-case-the-ising-gauge-theory.md` | 10.6b | 1322 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 2, opener 1, quiz-long 1 |
| `07-hamiltonian-learning-as-the-inverse-of-the-first-step-of-session-1.md` | 10.7 | 1496 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, long-paragraph 2, opener 1, quiz-long 1 |
| `08-closing-summary.md` | 10.8 | 1021 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 (0) | long-paragraph 1, quiz-long 1 |

## Introduction of the session

File `index.md`, 461 words, no numbered equation, no lint hit.

- Question of the page, and where we arrive: one sentence with the question of the session goes at the start of
  the second paragraph, "Can a neural network take the place of a many-body wavefunction, and can the forward
  methods of the course be run backwards?". Nothing else changes.
- Main result for the key box: none, since an introduction has no result.
- Equation of another page that it starts from, for the recall box: none. The page links Sections 1.4, 1.11,
  1.12, 3.5, 7.4, 7.10 and 7.11 in its text, and Section 1.4 has no numbered equation.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, an introduction.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, the index has no quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none. `session_map.py` stays.
- Old figures of the page that break the plot rules: none, `session_map` is a concept map.

## 10.1 Machine learning and many-body physics in two directions and 10.2 Neural networks as function approximators

File `01-machine-learning-and-many-body-physics-in-two-directions.md`, 1531 words, numbered equations (10.1).

- Question of the page, and where we arrive: in which two directions does machine learning meet many-body
  physics, and what does it mean to train a network? The opener replaces "Let us first give the plan of this
  session". We arrive at (10.1), the one template of the session, where each use is a choice of input, output
  and loss. Four paragraphs are split, the plan of 218 words before "Under both directions there is a third
  theme", the one of 171 words before "In this session we will not develop", the one of 205 words before "To
  train a network means", and the one of 192 words before "This template can be used in many cases".
- Main result for the key box: (10.1), with "Every use of a network in this session is a choice of the input
  $x_n$, the output $y_n$ and the loss. The training is always the same gradient descent with the learning rate
  $\eta$."
- Equation of another page that it starts from, for the recall box: none, the page starts from no equation.
- Derivation told in words, for a steps fold: "From the squared loss to its gradient by the chain rule", under
  (10.1). Simplest case first, one neuron $f=\tanh(wx+b)$ and one example, where
  $\partial\mathcal L/\partial w=2(f-y)(1-f^2)x$. Then one hidden layer, where the derivative of the output
  layer is used again for the layer before it, which is what backpropagation means. The fold ends with
  $\mathcal L(\theta-\eta\nabla\mathcal L)\approx\mathcal L-\eta|\nabla\mathcal L|^2$, so a small step lowers the
  loss.
- Lab box, with the source and the number that the source states: none, a page of method with no material and
  no measurement.
- Pen-and-paper problem: gradient descent on $\mathcal L=a\theta^2/2$ with $a>0$. Show that
  $\theta_n=(1-\eta a)^n\theta_0$, and find the learning rates that converge. Answer $0<\eta<2/a$, with the
  minimum in one step at $\eta=1/a$. For $a=4$ the limit is $0.5$ and one step is $0.25$ (checked, $\eta=0.5$
  jumps between $\pm\theta_0$ and $\eta=0.6$ grows by $1.4$ per step). The solution ends on the curvature, since
  the steepest direction of a loss sets the largest $\eta$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the hidden layer has a question
  of 18 words and links (10.1). It gets short sentences and (10.1) as a display, and its physics stays. Its
  feedback figure `xor` is redrawn, see below. The quiz on the learning rate passes the lint and stays. New, a
  picture question, "A network with one hidden layer of $H$ neurons is fitted to $y=\sin(3\pi x)$. Which fit has
  $H=1$?", with the fits of the widget `netfit` for $H=1$, $3$ and $12$ as the options. One neuron gives a
  monotonic curve with no extremum and a mean squared error of $0.46$, $H=3$ gives two extrema and $0.23$, and
  $H=12$ follows all six extrema with $2.3\times10^{-4}$, from `compute` of the widget.
- Figures to add, each with its pyqula script or the reason for numpy: the three pictures `quiz_netfit_h1.py`,
  `quiz_netfit_h3.py` and `quiz_netfit_h12.py`, with the shared `_netfitquiz.py` that calls `compute` of
  `webnotes/widgets/defs/netfit.py`, so that the pictures are the curves of the widget. Numpy, since pyqula does
  not train networks. Axes $x$ and $y$ with ticks at $-1$, $0$ and $1$, the same scale for the three.
- Old figures of the page that break the plot rules: `xor` has no axes at all, so $x_1$, $x_2$ and the corners
  $0$ and $1$ are not named, and the two classes are told only by the alt text. `lrate` names the step and
  $\theta$ but has no ticks, so the values $\pm1$ and the factor $1.5$ of its caption cannot be read on the axes.
  `s10f01_networktemplate` is a converted drawing.

## 10.3a Neural network quantum states

File `03-neural-network-quantum-states.md`, 943 words, numbered equations (10.2), (10.3).

- Question of the page, and where we arrive: can a network take the place of the $2^L$ coefficients of a
  wavefunction, and what is its loss? The opener replaces "In this section we meet neural network quantum states
  (NNQS) for the first time in the course". We arrive at (10.3), the variational energy as the loss, which is
  never below $E_0$. No paragraph is over 150 words.
- Main result for the key box: (10.3), with "The variational energy is the loss of the network. It is never below
  the ground-state energy $E_0$, and it is equal to $E_0$ only when $|\psi_\theta\rangle$ is the ground state."
  The sentence of the old text after (10.3) is in "Open for the lecturer".
- Equation of another page that it starts from, for the recall box: `eq="10.1"`, the loss and the update of
  10.2, since the page says that (10.3) is the loss of (10.1). Not (7.4) or (7.11), which are the same as (10.2)
  and as the first part of (10.3), so the box would show one equation twice.
- Derivation told in words, for a steps fold: "From the expansion in eigenstates to the variational bound", under
  (10.3). Simplest case first, two levels $E_0<E_1$, where
  $E=(|c_0|^2E_0+|c_1|^2E_1)/(|c_0|^2+|c_1|^2)\geq E_0$. Then all the eigenstates, and the sum over
  configurations of (10.3), which comes from inserting $\sum_s|s\rangle\langle s|$ twice.
- Lab box, with the source and the number that the source states: Bernien et al.,
  https://arxiv.org/abs/1707.04344, stored as `bernien2017_arxiv1707.04344.txt`. The abstract says "We realize
  a programmable Ising-type quantum spin model with tunable interactions and system sizes of up to 51 qubits."
  The material is the array of individually trapped cold atoms excited to Rydberg states, in the words of the
  abstract, which names no probe, so the box names none. Ours, marked with `ours`, the table (10.2) of 51 spins
  has $2^{51}\approx2.3\times10^{15}$ coefficients, which is $3.6\times10^{16}$ bytes at 16 bytes each. The box
  goes after the figure `memory`.
- Pen-and-paper problem: the two-site Heisenberg model $H=J\,\mathbf S_1\cdot\mathbf S_2$ and the trial state
  $\cos\alpha|\uparrow\downarrow\rangle+\sin\alpha|\downarrow\uparrow\rangle$. Compute $E(\alpha)$ and show that
  it is never below $E_0$. Answer $E(\alpha)=J(-\tfrac14+\tfrac12\sin2\alpha)$, with the minimum $-3J/4$ at
  $\alpha=-\pi/4$, the singlet (7.3), and the maximum $J/4$, a triplet state (checked against the eigenvalues
  $-0.75$ and $0.25$). This is the $E_0$ that the second quiz uses.
- Quizzes to rewrite, and a picture question or equations as options: the memory quiz has a question sentence of
  16 words. It is cut into short sentences, with the expansion (10.2) written in the question. The quiz on an
  energy below $E_0$ has 22 words and links (10.3). It gets $E[\theta]\geq E_0$ as a display and short
  sentences, and its physics stays. New, a picture question, "Each plot shows a memory in bytes against $L$ on a
  logarithmic axis. Which one is the table of $2^L$ complex numbers?", with the options $16\times2^L$, a
  straight line and the right one, $16\times L^4$, which bends down, and the MPS $16\,L\,d\,D^2$ with $d=2$ and
  $D=10$, which is almost flat. The feedback says that only an exponential is a straight line on this axis. The
  table passes 16 GB at $L=30$ and 1 TB at $L=36$.
- Figures to add, each with its pyqula script or the reason for numpy: `quiz_memory_table.py`,
  `quiz_memory_power.py` and `quiz_memory_mps.py`, with the shared `_memoryquiz.py`. Numpy, since this is
  arithmetic and not a pyqula calculation. Axes $L$ and bytes, ticks at the decades, the same scale for the three.
- Old figures of the page that break the plot rules: `memory` names $L$ and bytes but has no tick on the bytes
  axis, only the two guides, and its numbers on $L$ are text labels and not ticks. Its caption quotes $L=29$ and
  $L=35$, which are not marked, and "below a megabyte up to $L=300$", which lies outside the plot, since it ends
  at $L=60$. The redraw marks the two values, and the caption says that the value at $L=300$ is computed and not
  drawn. `s10f01_networktemplate`, shown again, is a drawing.

## 10.3b Training the network and quantum state tomography

File `03b-training-the-network-and-quantum-state-tomography.md`, 1369 words, numbered equations (10.4), (10.5).

- Question of the page, and where we arrive: how do we compute (10.3) without a sum over $2^L$ configurations,
  and can the same network learn a state from measurements? The opener replaces "In the first part we met the
  ansatz and the variational loss". We arrive at the local energy (10.4), sampled from the Born distribution, at
  its gradient (10.5), and at tomography by maximum likelihood. The paragraph of 191 words is split before
  "Equation (10.3) is the loss function".
- Main result for the key box: two boxes. (10.4), with "The energy is an average of the local energy over
  configurations drawn from $|C_\theta(s)|^2$. Each local energy needs only the few $s'$ that $H$ connects to
  $s$." In Section 10.3.1, the likelihood as an unnumbered display, $\max_\theta\sum_s n(s)\ln p_\theta(s)$, with
  "Counts in one basis fix $|C(s)|$ and not its phase."
- Equation of another page that it starts from, for the recall box: `eq="10.3"`, the variational energy of
  10.3a, with $C_\theta(s)$ and $H_{ss'}$ named.
- Derivation told in words, for a steps fold: "From the variational energy to the sampled local energy and its
  gradient", under (10.5). Simplest case first, (10.4) by multiplying and dividing each term of (10.3) by
  $C_\theta(s)$. Then (10.5) for one real parameter and a real $C_\theta$, where $\partial_\theta C=O\,C$ gives
  $2(\langle E_{\rm loc}O\rangle-\langle E_{\rm loc}\rangle\langle O\rangle)$, and then the complex case, where the
  two terms are complex conjugates because $H$ is Hermitian. The factor $2$ and the real part were checked for this plan.
- Lab box, with the source and the number that the source states: Torlai et al.,
  https://arxiv.org/abs/1904.08441, stored as `torlai2019_arxiv1904.08441.txt`. The abstract says
  "Specifically, we extract restricted Boltzmann machine (RBM) wavefunctions from data produced by a Rydberg
  quantum simulator with eight and nine atoms in a single measurement basis". The box keeps "eight and nine
  atoms" in words. Ours, $2^9=512$ configurations. The abstract does not say why one basis is enough here, so the
  box does not say it, and it does not join this sentence to the quiz on the phase. The box goes in Section
  10.3.1, after the second key box.
- Pen-and-paper problem: show that $E_{\rm loc}(s)$ is the same for every $s$ when the state is an eigenstate,
  so the sampled energy has no statistical error. Check it on the singlet of $H=J\,\mathbf S_1\cdot\mathbf S_2$.
  Answer $E_{\rm loc}=-3J/4$ for both $\uparrow\downarrow$ and $\downarrow\uparrow$, while the product state
  $|\uparrow\downarrow\rangle$ gives $-J/4$ (both checked). The solution ends on the use, since the spread of
  $E_{\rm loc}$ over the samples tells how far the network is from an eigenstate.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the short sum links (10.4) in
  its question. It passes the lint, and it gets (10.4) as a display. The tomography quiz has a question of 19
  words and is cut. Its feedback figure `tomo_phase` is redrawn. New, with equations as options, "Which
  expression is the local energy $E_{\rm loc}(s)$?", with the options $\sum_{s'}H_{ss'}C_\theta(s')/C_\theta(s)$,
  $\sum_{s'}H_{ss'}C_\theta(s')C_\theta(s)$ and $\sum_{s'}H_{ss'}|C_\theta(s')|^2/|C_\theta(s)|^2$. On the singlet
  with $C=\pm1/\sqrt2$ the three give $-3J/4$, $-3J/8$ and $+J/4$ at $s=\uparrow\downarrow$, so the third loses
  the sign and gives the triplet energy.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `tomo_phase` has no name and no tick on the probability
  axis, so the $50\%$ of the feedback is not on an axis, and the key of the two colors is a line of text under
  the panels. `local_energy` is a drawing, and `s10f02_nnqs` is converted.

## 10.4 Tensor networks for machine learning and the many-body wavefunction as a big-data problem

File `04-tensor-networks-for-machine-learning-and-the-many-body-wavefunction-as-a-big-data-problem.md`, 1350 words, numbered equations (10.6).

- Question of the page, and where we arrive: can the matrix product state, built to compress a wavefunction, be
  used as a machine-learning model? The opener replaces "We now follow the logic of the previous section in the
  reverse direction". We arrive at (10.6) with $L\,d\,D^2$ numbers, and at a classifier that is a linear map on
  the $2^N$-dimensional space of the pixels. The paragraph of 235 words is split before "The same compression can
  be generalized", and the one of 259 words before "We map each pixel" and before "A tensor network, and here a
  tree tensor network works well".
- Main result for the key box: two boxes. (10.6), with "The $2^L$ coefficients are a product of $D\times D$
  matrices, one for each site and each local state. The state has $L\,d\,D^2$ numbers, linear in $L$, and the
  bond dimension $D$ is ours to choose." The classifier as an unnumbered display,
  $f_\ell(x)=W_\ell\cdot\big(\varphi(x_1)\otimes\cdots\otimes\varphi(x_N)\big)$, with "The output is linear in the
  tensor product of the pixels, and the tensor network writes $W_\ell$ with few numbers."
- Equation of another page that it starts from, for the recall box: `eq="10.2"`, the table of 10.3a that (10.6)
  factorizes. Not (7.5), which is the same product as (10.6).
- Derivation told in words, for a steps fold: "Counting the numbers of a matrix product state", under (10.6).
  Simplest case first, $D=1$, a product state with $L\,d$ numbers. Then $D\times D$ matrices, which give
  $L\,d\,D^2$, so $20000$ for $L=100$, $d=2$ and $D=10$, against $2^{100}\approx1.3\times10^{30}$. One coefficient
  costs $L$ products of $D\times D$ matrices.
- Lab box, with the source and the number that the source states: Lanyon et al.,
  https://arxiv.org/abs/1612.08000, stored as `lanyon2017_arxiv1612.08000.txt`. The abstract says "Here we
  demonstrate Matrix Product State (MPS) tomography" and "We then use the technique to reconstruct the dynamical
  state of a trapped-ion quantum simulator comprising up to 14 entangled spins (qubits): a size far beyond the
  reach of QST." Ours, the table of 14 spins has $2^{14}=16384$ amplitudes. The box goes after Figure 10.3 and
  before the quizzes, since it ties (10.6) to a measured state, and the image classification has no lab.
- Pen-and-paper problem: show that the singlet $(|\uparrow\downarrow\rangle-|\downarrow\uparrow\rangle)/\sqrt2$
  needs $D=2$. For $D=1$ the coefficients are $C(s_1,s_2)=a^{s_1}b^{s_2}$, so
  $C(\uparrow\downarrow)C(\downarrow\uparrow)=C(\uparrow\uparrow)C(\downarrow\downarrow)$, and the singlet gives
  $-\tfrac12\neq0$. For $D=2$ the vectors $a^\uparrow=(1,0)$, $a^\downarrow=(0,1)$, $b^\uparrow=(0,-1)$ and
  $b^\downarrow=(1,0)$ give $C=0,1,-1,0$ for $\uparrow\uparrow$, $\uparrow\downarrow$, $\downarrow\uparrow$,
  $\downarrow\downarrow$ (checked), times $1/\sqrt2$. This is the open form, with vectors at the two ends, and the
  solution says so, since (10.6) is written with a trace.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the number of parameters
  passes the lint, and it links (10.6) in its question, so it gets (10.6) as a display. The quiz on the classifier refers to Figure 10.3b, so it gets the display
  $f(x)=W\cdot\big(\varphi(x_1)\otimes\cdots\otimes\varphi(x_N)\big)$ in the question and no figure number. New,
  with equations as options, "Which expression gives the coefficient $C(s_1,\dots,s_L)$ of a matrix product
  state?", with the options $\mathrm{Tr}[A^{s_1}\cdots A^{s_L}]$, $\prod_i\mathrm{Tr}\,A^{s_i}$ and
  $\sum_i\mathrm{Tr}\,A^{s_i}$. The product of traces is a product state, which cannot give the singlet of the
  problem. The sum cannot even give the product state $|\uparrow\uparrow\rangle$, since for two sites it forces
  $C(\uparrow\uparrow)=C(\downarrow\downarrow)$ when the other two coefficients vanish (checked by hand).
- Figures to add, each with its pyqula script or the reason for numpy: none. The page has no pyqula calculation,
  and `mps_chain` is a drawing.
- Old figures of the page that break the plot rules: none. `mps_chain` is a drawing and `s10f03_tnml` is
  converted. The Fashion-MNIST sentence is in "Open for the lecturer".

## 10.5 Machine learning in density functional theory

File `05-machine-learning-in-density-functional-theory.md`, 1484 words, numbered equations (10.7), (10.8).

- Question of the page, and where we arrive: where can machine learning enter density functional theory, and
  which entry changes the systems that we can compute? The opener replaces "We now turn to a different problem".
  We arrive at the Hohenberg-Kohn functional (10.7), the Kohn-Sham loop (10.8) with one diagonalization per
  iteration, and the two routes. No paragraph is over 150 words.
- Main result for the key box: two boxes. (10.7), with "The ground-state energy is a functional of the density
  alone. $F[n]$ is the same for every material, and its exact form is unknown." (10.8), with "Each iteration of
  the loop diagonalizes $H_{\rm KS}$. A learned $v_{\rm xc}$ keeps this step, and a learned map
  $v_{\rm ext}\mapsto n$ removes it."
- Equation of another page that it starts from, for the recall box: none. The page writes its Hamiltonian in
  full, and the mean-field decoupling of Section 1.12 has no number. (1.5) is the general Hamiltonian, which the
  first display of the page already gives in the continuum.
- Derivation told in words, for a steps fold: "From the energy functional to the Kohn-Sham equations", under
  (10.8). We write $E[n]=T_s[n]+\int v_{\rm ext}n+E_H[n]+E_{\rm xc}[n]$, which defines $E_{\rm xc}$, put
  $n=\sum_i|\phi_i|^2$, and vary with respect to $\phi_i^*$ with the normalization as a constraint. Simplest case
  first, one orbital with two electrons of opposite spin.
- Lab box, with the source and the number that the source states: Deringer et al.,
  https://arxiv.org/abs/1912.07344, stored as `deringer2019_arxiv1912.07344.txt`. This is a machine-learned
  interatomic potential, which the page calls related to route 2 and not route 2 itself, and its numbers are of
  a calculation, since nothing in the abstract is measured. The abstract says "Combining a model system size of
  100,000 atoms (ten-nanometre length scale) with a prediction accuracy of a few meV per atom", and it ends with
  "ultimately leading to the formation of a poly-crystalline, simple-hexagonal structure, consistent with
  experiments but not seen in earlier simulations." The material is amorphous silicon under pressure. The box
  keeps "ten-nanometre" in words, since "10 nm" would match the bare 10 of "10-11 GPa" in the same abstract. That
  a direct Kohn-Sham calculation of this size is out of reach is ours. If the lecturer wants only measured numbers
  in a lab box, this page has none.
- Pen-and-paper problem: the Hartree term screens a potential, on the smallest lattice. Two sites with hopping
  $t$, two electrons of opposite spin, an onsite difference $\Delta$, and $v_{\rm eff}(i)=v_{\rm ext}(i)+U\,n(i)$.
  Find $n_1-n_2$ to first order in $\Delta$. Answer $-\Delta/t$ without $U$ and $-\Delta/(t+U)$ with it, so a
  third for $U=2t$ (checked with a self-consistent loop, ratio $0.333$). The solution ties this to `ks_loop`,
  where the Hartree term lowers the density at the center from $1.21$ to $0.99$ (both checked).
- Quizzes to rewrite, and a picture question or equations as options: the quiz on $v_{\rm xc}$ has a question of
  21 words. It is cut, with $H_{\rm KS}=-\nabla^2/2+v_{\rm ext}+v_H+v_{\rm xc}$ written in the question. The quiz
  on the two arrows passes and stays. New, with equations as options, "Which term of $v_{\rm eff}$ is the mean
  field of the Coulomb interaction?", with the options the Hartree integral
  $e^2\int d^3r'\,n(\mathbf r')/|\mathbf r-\mathbf r'|$, $v_{\rm xc}=\delta E_{\rm xc}/\delta n$ and
  $v_{\rm ext}$. The counterexamples come from `ks_loop`, which has no $v_{\rm xc}$ and still has the mean field
  $U\,n(i)$ with $U=2t$, and whose $v_{\rm ext}$ is the same well at every iteration.
- Figures to add, each with its pyqula script or the reason for numpy: none. The toy of `ks_loop` stays numpy,
  since what it shows is the history of the iterations with a linear mixing of $0.3$, which the self-consistent
  call of pyqula does not return.
- Old figures of the page that break the plot rules: none. `ks_loop` names its axes with ticks on both panels,
  and its caption numbers ($36$ iterations, $0.99$ and $1.21$ at the center) agree with a copy of the script.
  `s10f04_dftml` is converted.

## 10.6a Phase classification with local order parameters and topological order

File `06-phase-classification-with-local-order-parameters-and-topological-order.md`, 950 words, numbered equations (10.9).

- Question of the page, and where we arrive: can a network trained on snapshots find a phase transition, and
  what does it learn for the Ising model? The opener replaces "We now come to a section that is, in a real sense,
  a review". We arrive at the local order parameter (10.9), at $T_c=2J/\ln(1+\sqrt2)\approx2.27J$, and at a drop
  at $T_c$ that sharpens with $L$. The paragraph of 182 words is split before "Session 3 and Session 4 instead
  used", and the one of 156 words before "We train the same cat-versus-dog architecture".
- Main result for the key box: (10.9), with "$m$ is a local order parameter. Well below
  $T_c=2J/\ln(1+\sqrt2)\approx2.27J$ a snapshot has $|m|$ close to one, and far above it $|m|$ is of order
  $1/\sqrt N$, so one number per snapshot tells the phase."
- Equation of another page that it starts from, for the recall box: `eq="10.1"`, the loss of the classifier of
  10.2, with the one-hot label as $y_n$.
- Derivation told in words, for a steps fold: none. $T_c$ comes from the exact solution, which the page quotes,
  and the size of $|m|$ above $T_c$ is the problem.
- Lab box, with the source and the number that the source states: Zhang et al.,
  https://arxiv.org/abs/1808.00479, stored as `zhang2019_arxiv1808.00479.txt`. The abstract says "These ANNs are
  used to analyze an experimentally-derived EQM image archive from carrier-doped cuprate Mott insulators." and
  "Throughout these noisy and complex data, the ANNs discover the existence of a lattice-commensurate,
  four-unit-cell periodic, translational-symmetry-breaking EQM state." The probe is the atomic-scale
  visualization of the abstract, an imaging experiment, and the box does not name STM unless it marks it as ours.
  The box keeps "four-unit-cell" in words. Ours, this order breaks translation, as the charge density wave of
  Section 1.13 does, so it is the easy case of this page.
- Pen-and-paper problem: $N$ independent spins $\sigma_i=\pm1$. Show that $\langle m\rangle=0$ and
  $\langle m^2\rangle=1/N$, and find the typical $|m|$ for $N=64^2=4096$. Answer $1/\sqrt N=0.016$ (checked, a
  sample gives a spread of $0.016$), against $|m|=0.99$ from the exact result at $k_BT=1.5J$. This is why one
  snapshot is enough.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on $|m|=0.93$ passes and stays.
  The quiz on the input and the output refers to Section 10.2, so it names the classifier of cats and dogs in
  words, with its input and its output, and no number. New, a picture question, "Each histogram shows $|m|$ of
  single snapshots of a $16\times16$ Ising lattice. Which one was taken at $k_BT=1.5J$?", with Monte Carlo
  histograms at $1.5J$, $2.27J$ and $3.5J$ as the options. A run in the scratch folder gave $\langle|m|\rangle$ of
  $0.99$ with a spread of $0.01$, then $0.73$ spread over $0.36$ to $0.91$, and $0.13$ spread over $0.02$ to
  $0.30$, as 5 and 95 percent points. The builder computes them again with the seed of its script.
- Figures to add, each with its pyqula script or the reason for numpy: `quiz_ising_hist_low.py`,
  `quiz_ising_hist_tc.py` and `quiz_ising_hist_high.py`, with the shared `_isinghist.py`, a numpy Monte Carlo as
  in `igt_hist.py`, since pyqula has no classical Monte Carlo. Axes $|m|$ and the probability density, with ticks,
  and the same scale for the three.
- Old figures of the page that break the plot rules: `onsager` names $T/J$ and $|m|$ but has no tick, so $|m|=1$
  is not on the axis and $T_c$ is a text label under it. It also names the axis $T/J$, while `ising_sizes` on the
  same page names it $k_BT/J$, and the redraw uses $k_BT/J$. `ising_sizes` follows the rules.

## 10.6b The hard case, the Ising gauge theory

File `06b-the-hard-case-the-ising-gauge-theory.md`, 1322 words, numbered equations (10.10).

- Question of the page, and where we arrive: what does the classifier do when the magnetization is near zero in
  both regimes? The opener replaces "In the first part we saw that for the Ising model". We arrive at the
  plaquette model (10.10), its gauge flips, a magnetization that vanishes at every temperature, and a crossover
  that does not sharpen. The paragraph that starts "where the sum runs over the plaquettes" is split before "At
  infinite temperature, instead" and before "Note that in two dimensions this model", and the one of 183 words
  before "We should state one more physical point".
- Main result for the key box: (10.10), with "Only the plaquette products enter the energy. A flip of the four
  bonds at a vertex keeps every product, so $\langle\sigma_i\rangle=0$ at every temperature and $|m|$ is of order
  $1/\sqrt N$ in both regimes." The box does not say "no local quantity", see "Open for the lecturer".
- Equation of another page that it starts from, for the recall box: `eq="10.9"`, the Ising model and $m$ of
  10.6a.
- Derivation told in words, for a steps fold: "Why every single-spin average vanishes", under (10.10). Simplest
  case first, one plaquette, where the flip of $\sigma_1$ and of a neighbor bond at the same vertex keeps the
  energy. Then the lattice, where the flip at an end of bond $i$ maps a configuration with $\sigma_i=+1$ to one
  with $\sigma_i=-1$ and the same energy, so the two have the same weight and $\langle\sigma_i\rangle=0$. The
  check is the enumeration of one plaquette, which gives $\langle\sigma_1\rangle=0$ at $k_BT=0.2J$, $J$ and $5J$.
- Lab box, with the source and the number that the source states: Semeghini et al.,
  https://arxiv.org/abs/2104.04119, stored as `semeghini2021_arxiv2104.04119.txt`. The abstract says "We use a
  219-atom programmable quantum simulator to probe quantum spin liquid states.", "In our approach, arrays of
  atoms are placed on the links of a kagome lattice and evolution under Rydberg blockade creates frustrated
  quantum states with no local order." and "The onset of a quantum spin liquid phase of the paradigmatic toric
  code type is detected by evaluating topological string operators that provide direct signatures of topological
  order and quantum correlations." Ours, as in (10.10) the degrees of freedom live on the links and the order is
  seen only by a quantity of many spins. The abstract is of a quantum state on a kagome lattice and not of the
  classical model of the page, and the box says so.
- Pen-and-paper problem: one plaquette of four bond spins with $H=-J\sigma_1\sigma_2\sigma_3\sigma_4$. Compute
  $\langle\sigma_1\sigma_2\sigma_3\sigma_4\rangle$ at the temperature $T$. Answer $\tanh(J/k_BT)$, which is
  $0.76$ at $k_BT=J$, $0.9999$ at $0.2J$ and $0.197$ at $5J$, the two temperatures of `igt_hist` (checked by
  enumeration, and on an open lattice of $2\times2$ plaquettes each plaquette gives the same value). The value is
  smooth in $T$, which is why the crossover does not sharpen.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the vertex flip passes and
  stays. The quiz on the crossover has a question of 18 words. It is cut, with $H_{\rm IGT}$ as a display, and
  its physics stays. New, a picture question, "Each picture shows the bond spins of a small lattice. Which one is
  a ground state of $H_{\rm IGT}=-J\sum_p\prod_{i\in\partial p}\sigma_i$?", with three bond configurations of
  $3\times3$ plaquettes and no crosses drawn. The right one is a gauge transform of the uniform state, random
  from bond to bond with every product $+1$. One wrong option is the uniform state with one bond flipped, two
  products $-1$ and an energy $4J$ above. The other is a random configuration with several products $-1$, whose
  number the builder counts on its drawing.
- Figures to add, each with its pyqula script or the reason for numpy: `quiz_igt_ground.py`,
  `quiz_igt_oneflip.py` and `quiz_igt_hot.py`, with the shared `_igtlattice.py`, drawings with `sketch=True`,
  since a bond configuration is not a plot and not a pyqula calculation.
- Old figures of the page that break the plot rules: `igt_hist` has no name and no tick on the vertical axis,
  which is the probability density of $|m|$, and the legend says low and high $T$ while the temperatures differ
  between the two panels and are given only in the caption. `s10f05_phaseclassification` is converted.

## 10.7 Hamiltonian learning as the inverse of the first step of session 1

File `07-hamiltonian-learning-as-the-inverse-of-the-first-step-of-session-1.md`, 1496 words, numbered equations (10.11), (10.12).

- Question of the page, and where we arrive: can we run the forward arrow of Section 1.4 backwards, from a
  measured observable to the Hamiltonian? The opener replaces "We come at the end to the part of this session".
  We arrive at the forward map (10.11) with hidden variables $\mu$, at the loss (10.12) on simulated pairs, and at
  the toy, where the training set must cover $\mu$. The paragraph of 157 words is split before "**Hamiltonian
  learning** writes this explicitly", and the one of 159 words before "Hamiltonian learning does not leave any of
  these behind".
- Main result for the key box: (10.12), with "The pairs of an observable and its $\lambda_n$ are simulated, so
  every pair has its answer. The trained network is then applied to a measured observable, and the hidden
  variables $\mu$ must be covered by the training set."
- Equation of another page that it starts from, for the recall box: `eq="10.1"`, since (10.12) is the squared
  loss of 10.2 with the observable as the input and $\lambda$ as the label. Section 1.4 has no numbered equation.
- Derivation told in words, for a steps fold: "Why the squared loss gives the average of the labels", under
  (10.12). Simplest case first, one input with two labels $\lambda_a$ and $\lambda_b$, where
  $(y-\lambda_a)^2+(y-\lambda_b)^2$ is smallest at $y=(\lambda_a+\lambda_b)/2$. Then many pairs, where the best
  output for an input is the average of $\lambda$ over all the $\lambda$ and $\mu$ of the training set that give
  it. This says what a network trained with disorder returns. It does not explain the error of the network
  trained on clean rings, which comes from test inputs that lie outside its training set, and the fold does not
  claim it. The mean error of that network on the disordered test rings, $-0.03$ to $-0.05$ over ten seeds, is a
  number for the picture quiz.
- Lab box, with the source and the number that the source states: Wang et al.,
  https://arxiv.org/abs/1703.05402, stored as `wang2017_arxiv1703.05402.txt`. The abstract says that a
  silicon-photonics quantum simulator and "an electron spin in a diamond nitrogen-vacancy centre" are joined,
  and they "use the former to learn the latter's Hamiltonian via Bayesian inference." It then says "We learn the
  salient Hamiltonian parameter with an uncertainty of approximately 10^-5.", which the box writes $10^{-5}$. The method is
  Bayesian inference and not a network, and the box says so. The abstract does not say whether the uncertainty is
  relative or which parameter it is, so the box says neither. Ours, the simulator runs the forward arrow, as the
  simulated pairs of (10.12) do.
- Pen-and-paper problem: show that the chains with first-neighbor hopping $t$ and $-t$ have the same density of
  states, and that a second-neighbor hopping $t_2$ keeps its sign. Answer, with
  $\epsilon_k=-2t\cos k-2t_2\cos2k$, the shift $k\to k+\pi$ maps $t$ to $-t$ and leaves $t_2$, so the band of
  width $4|t|$ for $t_2=0$ is the same set of energies, while $t_2$ and $-t_2$ give different densities of states
  (both checked on a fine k-mesh). So the toy can learn $t_2$, and no density of states gives the sign of $t$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on simulated data has a question
  of 16 words and links (10.12). It gets (10.12) as a display and short sentences. The quiz on many $\lambda$
  passes the lint, and it stays with its physics. Its third feedback says that the loss is $t^2$, which is the
  mean over the two pairs, while (10.12) is a sum and gives $2t^2$, see "Open for the lecturer". Its feedback
  figure `dos_sign` is redrawn. New, a picture question, "Each plot shows the predicted $t_2$ against the true
  one for disordered test rings. Which network was trained on rings with disorder?", with the options from the
  toy, the points on the diagonal (trained with disorder, error $0.0040$ to $0.0054$ over ten seeds), the points
  below the diagonal (trained on clean rings, $0.058$ to $0.074$), and a flat line at $0.2$, a network that
  ignores its input, with the error $0.115$.
- Figures to add, each with its pyqula script or the reason for numpy: `ring_dos.py`, a pyqula script of the
  forward map for one ring, with `geometry.chain().get_supercell(200)`, `tij=[-1., -t2]` as in the recipe "The
  chain with a second-neighbor hopping", `disorder.anderson(h, w=W)`, a seed for `np.random` since this call
  draws from it, and the eigenvalues of `h.get_hk_gen()` at $k=0$ in 40 bins. These calls were run once for this
  plan with `has_spin=False`. At $W=0$ and $t_2=0.3$ they give the eigenvalues of the numpy ring of
  `ham_learning` to $10^{-14}$, with the same sign, `disorder.anderson` gives onsite energies in $[-W,W]$, and no
  file is written. The calls of `chain_sign_dos.py` were not run. The left panel of `ham_learning`
  draws from it, and the fit of the right panel stays numpy, since least squares is not a pyqula call. The figure
  gets the button. `chain_sign_dos.py`, pyqula, the bands of the chain for $t=\pm1$ and the density of states with
  `h.get_dos(mode="Green")` as in the recipe "The density of states", for the redraw of `dos_sign`, with no button
  since it is a quiz feedback. The three pictures `quiz_hl_disorder.py`, `quiz_hl_clean.py` and `quiz_hl_flat.py`
  with the shared `_hlquiz.py`, numpy, the training of the toy. After a redraw of `ham_learning` the builder reads
  `git status`, since this script does not give the same SVG twice.
- Old figures of the page that break the plot rules: `ham_learning` has no tick and no unit on the axis of
  $\mathcal O$, which is the fraction of the eigenvalues in each bin. `dos_sign` has no ticks, so $\pm\pi$ and the
  band edges $\pm2t$ are not on the axes, the density of states has no unit, and its two panels call the same
  energy $\epsilon$ and $E$. `s10f06_hamiltonianlearning` is converted.

## 10.8 Closing summary

File `08-closing-summary.md`, 1021 words, numbered equations none.

- Question of the page, and where we arrive: the closing page has no opener question, as in Session 3. It gets,
  after the list of results, the sentence "After this session we can do the following tasks, and each of them has
  the section that teaches it." and a list, one task per line with its section.
  - Write a use of a network as a choice of input, output and loss, and train it with (10.1). Section 10.2.
  - Estimate the memory of a wavefunction of $L$ spins, and compare it with an MPS of bond dimension $D$.
    Sections 10.3a and 10.4.
  - Write the energy (10.3) as an average of the local energy (10.4), and say why it is never below $E_0$.
    Sections 10.3a and 10.3b.
  - Say which part of a state tomography in one basis cannot give. Section 10.3.1.
  - Say why a learned $v_{\rm xc}$ keeps the diagonalization of (10.8), and a learned map $v_{\rm ext}\mapsto n$
    removes it. Section 10.5.
  - Tell the local order parameter of the Ising model (10.9) from the plaquette products of the gauge theory
    (10.10). Sections 10.6a and 10.6b.
  - Build a training set for Hamiltonian learning (10.12) that covers the hidden variables. Section 10.7.
  The paragraph of 225 words is split before "This session closed the arc in two ways".
- Main result for the key box: none, a closing page.
- Equation of another page that it starts from, for the recall box: none.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, a closing page.
- Pen-and-paper problem: none, a closing page.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the template has a question of
  18 words. It is cut, with (10.1) as a display, and its physics stays. New, with equations as options, "Which
  input, output and loss make a neural network quantum state?", with the options $(s,\,C_\theta(s),\,E[\theta])$,
  $(s,\ \text{one-hot label},\ \text{squared error})$ and $(\mathcal O,\ \lambda,\ \text{squared error})$. The
  wrong two are the phase classifier of 10.6a and Hamiltonian learning of 10.7. No picture question, since the
  page has no plot of its own.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, `s10f06_hamiltonianlearning` and
  `s10f01_networktemplate` are converted drawings shown again.

## Candidates for the lab boxes

The session has no notebook. These sources were fetched and stored, one per page that gets a box.

- 10.3a, `bernien2017_arxiv1707.04344.txt`, 51 qubits of Rydberg atoms.
- 10.3b, `torlai2019_arxiv1904.08441.txt`, eight and nine atoms, one measurement basis.
- 10.4, `lanyon2017_arxiv1612.08000.txt`, up to 14 trapped-ion spins, MPS tomography.
- 10.5, `deringer2019_arxiv1912.07344.txt`, 100,000 atoms of amorphous silicon, a calculation.
- 10.6a, `zhang2019_arxiv1808.00479.txt`, a four-unit-cell periodic state in cuprate images.
- 10.6b, `semeghini2021_arxiv2104.04119.txt`, 219 atoms on the links of a kagome lattice.
- 10.7, `wang2017_arxiv1703.05402.txt`, an NV spin, an uncertainty of about $10^{-5}$.

These abstracts were read on arXiv before the fetch and not stored, since they state no number for a page or a
number that is not of a material. 1606.02318 (neural network quantum states) and 1703.05334 (tomography with
networks) state no number. 1605.05775 gives less than 1% error on MNIST and 1906.06329 gives 88% on
Fashion-MNIST with an MPS, both not of a material. 1609.02815 gives 30,000 papers, 2210.11343 a speedup of three
orders of magnitude in words, 1811.08630 a computed 0.2 meV per molecule for ice, 2102.04804 a model range of
2400 K and 50 GPa for water, and 2005.00223 names no material. 1605.01735, 1809.05519, 2101.05712 and 1906.11275
state no number, and 2002.06169 gives success rates up to 86% for experiment and numerics together. 2104.01180
measures a topological entanglement entropy near $\ln2$ on a superconducting processor, and it is the second
choice for 10.6b.

## Builder groups

The names of the new figure and script files in the blocks above are stems. Each builder adds the prefix of its
group, so `quiz_netfit_h1.py` of group 1 becomes `g1_quiz_netfit_h1.py`, as in Session 3.

- Group 1, `index.md` and `01-machine-learning-and-many-body-physics-in-two-directions.md`. The index gets its
  question. The page has the widget `netfit` and the figures `xor` and `lrate`.
- Group 2, `03-neural-network-quantum-states.md`, `03b-training-the-network-and-quantum-state-tomography.md` and
  `04-tensor-networks-for-machine-learning-and-the-many-body-wavefunction-as-a-big-data-problem.md`. They share
  the table (10.2), the energy (10.3), the count $L\,d\,D^2$ of `memory` and of (10.6), and the singlet of the
  three problems.
- Group 3, `05-machine-learning-in-density-functional-theory.md`. It shares nothing with its neighbors. If four
  builders are preferred, it can join group 4 as its first page.
- Group 4, `06-phase-classification-with-local-order-parameters-and-topological-order.md` and
  `06b-the-hard-case-the-ising-gauge-theory.md`. They share the Monte Carlo of `igt_hist`, the $16\times16$
  lattice, the order parameter (10.9), and the open point on locality.
- Group 5, `07-hamiltonian-learning-as-the-inverse-of-the-first-step-of-session-1.md` and
  `08-closing-summary.md`. They share Figure 10.6, (10.11) and (10.12), and the closing page summarizes the
  numbers of every page, so it is built last.

## Open for the lecturer

No change of a numbered equation is planned. These are statements of the old text, one convention and one rule,
each with what was found. A builder leaves them as they are until the lecturer picks.

- The lab boxes of this session, a rule. All seven hold counts with no unit (qubits, atoms, spins, unit cells) or
  a bare $10^{-5}$, so the tool checks none of them and each box gives the warning `lab-number`. The box of 10.5
  is a calculation and nothing in its abstract is measured, and the box of 10.3a names no probe, since its
  abstract names none. The locked rule asks for one material, one number with its unit and the probe. The
  options are the seven boxes as planned, the boxes without 10.5, or no lab boxes in this session.

- 10.3a, the sentence after (10.3), "where the equality holds only when $|\psi_\theta\rangle$ is the true ground
  state, or in practice the closest state that the ansatz can reach". It reads as if the equality held for the
  best state of the ansatz, which is false unless the ansatz contains the ground state. The best state of the
  ansatz has the lowest $E[\theta]$, and it is still above $E_0$. The options are "the equality holds only for the
  ground state, and in practice the training reaches the best state of the ansatz, whose energy is above $E_0$",
  or the old sentence.
- 10.3b and 10.8, "NNQS is therefore the most expressive of the variational families of this course" and "NNQS is
  above the matrix product states ... and the PEPS ... in the variational hierarchy" are written without the
  condition that the caption of Figure 10.2 gives, "a statement about networks that are expressive enough and not
  about every architecture". The options are to add this condition to the two sentences, or to leave them.
- 10.4 and 10.8, the Fashion-MNIST numbers $95.38\%$ and $88.97\%$ have no link, and the slides of the lecture
  have none either. They are in the body of arXiv 1801.00315, "Learning Relevant Features of Data with
  Multi-scale Tensor Networks", in Section VI on the tree curtain model, "The optimized model reaches 95.38%
  accuracy on the training set, and 88.97% accuracy on the testing set." Its abstract does not hold them, so the
  store does not have them, and they were read in the PDF of arXiv. The model there classifies ten kinds of
  clothes with four tree layers under a matrix product state, while the page tells the example as a purse against
  a shirt. The same section gives XGBoost at 89.8%, AlexNet at 89.9% and a two-layer convolutional network at
  87.6%, so "comparable" holds. The options are the link and "ten kinds of clothes", the link only, or the old
  text.
- 10.6b, "no local quantity can distinguish the two regimes", twice in the text, and "it learns a nonlocal
  function". The plaquette product is a local quantity of four spins. Its average is $\tanh(J/k_BT)$ on an open
  lattice, which is $0.9999$ at $k_BT=0.2J$ and $0.197$ at $5J$, the temperatures of `igt_hist`, so the energy
  per plaquette tells the two regimes apart. No quantity of a single spin does, and the caption of Figure 10.5
  says "no quantity on a single bond", which is right. The abstract of 1605.01735, read and not stored, says only
  that a convolutional network detects "topological phases with no conventional order parameter". The options are
  "no quantity of a single spin", "no local order parameter, a local quantity that is zero in one regime and not
  in the other", or the old text. The new blocks of 10.6b are planned to hold for every option.
- 10.7, the caption of `ham_learning` gives the errors of one seed, $0.06$, $0.10$ for $W>1$, and $0.004$. Ten
  seeds of a copy of the script give $0.058$ to $0.074$, $0.093$ to $0.121$, and $0.0040$ to $0.0054$, and the
  brief asks for a range. The options are "$0.06$ to $0.07$", "about $0.1$" and "$0.004$ to $0.005$", or the old
  values with "for one realization".
- 10.7, the third feedback of the quiz on many $\lambda$ says "the loss is $t^2$". With two pairs the sum (10.12)
  gives $2t^2$, which is $t^2$ per pair. The options are "$2t^2$, which is $t^2$ per pair", or the old text.
- 10.2, the box of the widget `netfit` says "trained for 4000 steps of gradient descent, with the loss of
  (10.1)". The widget uses Adam with a falling step size and the mean of the squared error, not its sum. The
  options are "4000 steps of Adam, a form of gradient descent, with the mean squared error", or the old text.
- 10.4, a convention. (10.6) is written with a trace, the periodic form, while (7.5) of Session 7 is the open
  product. The problem of 10.4 uses the open form and says so. The options are one sentence after (10.6) that
  names the two forms, or nothing.
- 10.6a and 10.6b, the sizes "from $L=10$ up to $L=60$" and "from $L=4$ up to $L=28$" have no source on the page,
  and the abstract of 1605.01735 does not state them. No change is proposed, and they stay as the lecture gives
  them.
