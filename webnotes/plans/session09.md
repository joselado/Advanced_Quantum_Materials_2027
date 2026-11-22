# Plan of Session 9 of the web notes

This plan is filled before any page is written, and the lecturer can change it. One block per page. A
field that does not apply says "none" with the reason. The rules are in
`lecture_notes/WEB_NOTES_PLAN.md`, and the conventions of the session in
`webnotes/conventions/session09.md`. That sheet did not exist when this plan was written, so every sign,
unit and pyqula normalization below that says "the sheet confirms" waits for it.

## The pages today

| file | sections | words | eqs | key | recall | steps | lab | problem | quiz | picture options | figures (with script) | lint hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `index.md` | intro | 519 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 (0) | 0 |
| `01-response-functions-as-a-probe-of-the-ground-state.md` | 9.1 | 804 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `02-the-response-of-a-classical-magnet-as-a-first-example.md` | 9.2 | 794 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | key 1, long-paragraph 1, opener 1, quiz-long 1 |
| `03-linear-response-and-perturbation-theory-in-detail.md` | 9.3 | 1098 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | key 1, opener 1, quiz-long 1 |
| `04-the-fermi-sea-and-the-lindhard-function.md` | 9.4a | 715 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | key 1, opener 1, quiz-long 1 |
| `04b-nesting-and-the-divergence-of-the-lindhard-function.md` | 9.4b | 1426 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, long-paragraph 1, opener 1 |
| `05-interactions-as-a-perturbation-with-rpa-plasmons-and-the-stoner-instability.md` | 9.5a | 1154 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, opener 1, quiz-long 1, quiz-ref 1 |
| `05b-the-stoner-instability.md` | 9.5b | 1276 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 (0) | key 1, long-paragraph 1, opener 1 |
| `06-impurities-as-diagnostics-i-friedel-oscillations-in-a-metal.md` | 9.6a | 1154 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 3 (0) | key 1, opener 1, quiz-long 1 |
| `06b-friedel-oscillations-in-a-chain-and-the-contrast-with-an-insulator.md` | 9.6b | 763 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `07-impurities-as-diagnostics-ii-magnetic-impurities-in-a-superconductor.md` | 9.7 | 1180 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, opener 1, quiz-long 1 |
| `08-impurities-as-diagnostics-iii-vacancies-in-topological-matter.md` | 9.8 | 1356 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | long-paragraph 2, opener 1, quiz-long 1, quiz-ref 1 |
| `09-impurities-as-diagnostics-iv-screening-in-quantum-magnets.md` | 9.9 | 1518 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, opener 1, quiz-long 1, quiz-ref 1 |
| `10-disorder-and-anderson-localization.md` | 9.10a | 1213 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 (0) | key 1, quiz-long 2 |
| `10b-random-disorder-and-the-special-role-of-one-dimension.md` | 9.10b | 1182 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 1 (0) | long-paragraph 1, opener 1, quiz-long 1 |
| `11-closing-summary.md` | 9.11 | 1071 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (0) | quiz-long 1 |

Three facts hold for the whole session. `style.arrows` removes the ticks unless `ticks=True` is passed, so
most old plots of the session have named axes and no numbers. The answers of the problems and the counter
examples below were checked by number in the scratch scripts `plan_numbers.py`, `sign_checks.py` and
`lab_quotes.py` of the folder
`/tmp/claude-3291340/-u-40-ladovj1-data-Documents-programs-Advanced-Quantum-Materials-2027/bbe18649-405d-487c-83fe-fcca11e6bfea/scratchpad/webnotes/s09/plan/checks/`,
which a reboot can clear, so each number is an `assert` again in the check script of its page. A figure script is not run in place to read a number,
since `style.save` rewrites the SVG. Since 2026-11-22 `spinon_impurity.py` gives the same SVG at every run.

## Introduction of the session

File `index.md`, 519 words, no numbered equation, no lint hit.

- Question of the page, and where we arrive: the page lists what we need from before. One sentence with
  the question of the session goes first, "Can we learn which state a material is in, and which state it is
  close to, only from how it reacts to a small push?". Nothing else changes.
- Main result for the key box: none, an introduction has no result.
- Equation of another page that it starts from, for the recall box: none, the page already links (1.7) and
  the sections it needs in its text.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, an introduction.
- Pen-and-paper problem: none.
- Quizzes to rewrite, and a picture question or equations as options: none, the index has no quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none. `session_map.py` stays.
- Old figures of the page that break the plot rules: none, `session_map` is a concept map.

## 9.1 Response functions as a probe of the ground state

File `01-response-functions-as-a-probe-of-the-ground-state.md`, 804 words, numbered equations none. Mostly
a page of motivation, so it gets fewer blocks.

- Question of the page, and where we arrive: if we push a material at one place and one time, what does the
  signal at another place and time tell us about its ground state? We arrive at the response function, which
  in a clean system depends only on $x'-x$ and $t'-t$, so each $(q,\omega)$ responds alone. The opener
  replaces "Let us first set up the general experiment". The paragraph of 152 words is split before "In the
  second way".
- Main result for the key box: one box with an unnumbered display, $\delta A(x',t')=\int dx\,dt\,
  \chi(x'-x,t'-t)\,f(x,t)$, which becomes $\delta A(q,\omega)=\chi(q,\omega)\,f(q,\omega)$, and one sentence,
  "with translational symmetry in space and time a push at one $(q,\omega)$ gives a response at the same
  $(q,\omega)$ only". No new `\tag`.
- Equation of another page that it starts from, for the recall box: none, the page starts from no equation.
- Derivation told in words, for a steps fold: "From a response in real space to one in (q, omega)", three
  lines, the convolution becomes a product after the Fourier transform. Simplest case first, a static
  response on a chain.
- Lab box, with the source and the number that the source states: none, a page of motivation. The measured
  $\chi''(q,\omega)$ goes on 9.4b.
- Pen-and-paper problem: a chain with the static response $\chi(n)=e^{-|n|/\xi}$ between sites a distance
  $n$ apart. Compute $\chi(q)=\sum_n\chi(n)e^{-iqn}$ for $\xi=1$. Answer $\chi(0)=\coth(1/2)\approx2.16$ and
  $\chi(\pi)=\tanh(1/2)\approx0.46$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the clean chain has a
  question of 21 words. It is cut to short sentences, with $\chi(x,x')=\chi(x'-x)$ in the question and its
  physics kept. New picture question, "Each map shows the static response $\chi(x,x')$ of a ring of 40
  sites. Which ring is clean?". The right option has stripes parallel to the diagonal, the wrong ones are a
  ring with one impurity and a ring with a random potential. The three maps share one color scale with a
  colorbar and have the axes $x$ and $x'$. They are numpy, since this is the static density response
  matrix of a finite ring from exact diagonalization, a few lines that the quiz picture needs without a
  button.
- Figures to add, each with its pyqula script or the reason for numpy: none in the body.
- Old figures of the page that break the plot rules: none, `probe` is a drawing.

## 9.2 The response of a classical magnet as a first example

File `02-the-response-of-a-classical-magnet-as-a-first-example.md`, 794 words, numbered equations (9.1).

- Question of the page, and where we arrive: can a measurement in the disordered phase tell which order
  comes when we cool down? We arrive at the intercept of the straight line $1/\chi(T)$, positive for a
  ferromagnet and negative for an antiferromagnet, read far above any order. The question moves into the
  first three sentences. The paragraph of 229 words is split before "In experiments this is a practical
  diagnostic".
- Main result for the key box: (9.1), with "the line $1/\chi(T)$ crosses zero at $T_c$ for a ferromagnet and
  at $-T_c$ for an antiferromagnet, so its intercept gives the sign of the exchange".
- Equation of another page that it starts from, for the recall box: none. Section 1.12 gives the mean-field
  method in words and has no equation that (9.1) starts from.
- Derivation told in words, for a steps fold: "From the mean-field Ising model to (9.1)". Simplest case first,
  a free spin $\sigma=\pm1$ in a field, $m=\tanh(h/T)$, so $\chi=1/T$. Then the mean field $h+zJm$, which
  gives $\chi=1/(T-zJ)$. For an antiferromagnet on a bipartite lattice a uniform field sees $h-z|J|m$, which
  gives $1/(T+z|J|)$. The sign convention of $J$ comes from the sheet.
- Lab box, with the source and the number that the source states: ZnCu$_3$(OH)$_6$Cl$_2$, herbertsmithite,
  https://arxiv.org/abs/cond-mat/0610539, stored as `helton2007_arxivcond-mat-0610539.txt`. The abstract says
  "The susceptibility indicates a Curie-Weiss temperature of ~ -300 K; however, no magnetic order is observed
  down to 50 mK." The box gives the negative intercept and the absence of order. Our reading, marked as ours,
  is that the sign gives an antiferromagnetic exchange, while (9.1) of mean field cannot say why no order
  appears, which is the frustration of Session 8.
- Pen-and-paper problem: a fit of $1/\chi=(T-\theta)/C$ goes through $(60\text{ K},90)$ and $(90\text{ K},120)$.
  Find $\theta$, say which order is coming, and find $|J|$ for $z=4$ from the steps fold. Answer $C=1$,
  $\theta=-30$ K, an antiferromagnet, $|J|=7.5$ K.
- Quizzes to rewrite, and a picture question or equations as options: the quiz with `curie_quiz` has a
  question of 20 words. It is cut, with $1/\chi\propto T-\theta$ in the question, and its picture stays. New
  picture question, "Each line is $1/\chi(T)$ of one sample. Which sample orders as a ferromagnet?", three
  lines with intercepts $+30$ K, $0$ and $-30$ K, numpy since they are straight lines. New with equations as
  options, "In mean field, how does $\chi$ of an antiferromagnet grow as we cool it above the order?",
  options $1/(T+T_c)$, which is right, $1/(T-T_c)$ and $1/T$.
- Figures to add, each with its pyqula script or the reason for numpy: none in the body.
- Old figures of the page that break the plot rules: `curie_weiss` has no ticks or unit on the $1/\chi$
  axis, and the $T$ axis has only the labels $0$ and $\pm T_c$, which is enough for a sketch. It gets
  "arbitrary units" in the caption. `curie_quiz` quotes $T=60$ K and has no tick there. It needs ticks at
  $T=-30$, $0$, $60$ K and at $1/\chi=60$, $90$.

## 9.3 Linear response and perturbation theory in detail

File `03-linear-response-and-perturbation-theory-in-detail.md`, 1098 words, numbered equations (9.2), (9.3).

- Question of the page, and where we arrive: what is the first change of an eigenstate when we add a small
  $V$ to $H_0$? We arrive at (9.3), where each state mixes with the others with the weight
  $\langle m|V|n\rangle/(E_n-E_m)$, so close levels mix most, and at the three cases where this fails.
- Main result for the key box: (9.3), with "a perturbation mixes $|n\rangle$ with every $|m\rangle$, with the
  matrix element divided by the energy difference". (9.2) is the definition of the model and stays in the
  text. The lint needs only one key box on the page.
- Equation of another page that it starts from, for the recall box: none. The page starts from the idea of
  9.2, and not from its equation.
- Derivation told in words, for a steps fold: "From H(lambda) to the first-order state (9.3)". Simplest case
  first, two levels $H_0=\mathrm{diag}(0,\Delta)$ and $V=v\sigma_x$, then the general case by projecting
  $(H_0+\lambda V)|n(\lambda)\rangle=E_n(\lambda)|n(\lambda)\rangle$ onto $\langle m|$. It ends at the
  unnumbered $\chi_A=2\,\mathrm{Re}\sum_{m\neq n}\langle n|A|m\rangle\langle m|V|n\rangle/(E_n-E_m)$, which a
  number checks.
- Lab box, with the source and the number that the source states: none. The page is formal, and its three
  failures are named without a material number.
- Pen-and-paper problem: $H_0=\mathrm{diag}(0,\Delta)$ and $V=v\sigma_x$ with $v=0.1\Delta$. Find the first-order
  coefficient of $|2\rangle$ in the ground state and compare with the exact one. Answer $-0.1$ against the
  exact $-0.0985$, and the energy shift $-0.01\Delta$ against the exact $-0.0099\Delta$.
- Quizzes to rewrite, and a picture question or equations as options: the first quiz has a question of 16
  words, and both quizzes link (9.3). Both get the coefficient $c_m=\langle m|V|n\rangle/(E_n-E_m)$ in the
  question as a display, and the first is cut. New with equations as options, the two-level case of the
  problem, "What is the first-order coefficient of $|2\rangle$?", options $-v/\Delta$, which is right,
  $+v/\Delta$ and $-v^2/\Delta$. No picture question, since the bars of `mixing` would give the answer away.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `mixing` has an energy arrow with no numbers and no
  drawn axis for the coefficients, with the values written on the bars. It needs ticks at the energies of
  the levels, in units of the matrix element or of $t$ as the sheet says, and an axis with ticks for the
  coefficient. `degenerate` is a level drawing in a feedback and stays.

## 9.4a The Fermi sea and the Lindhard function

File `04-the-fermi-sea-and-the-lindhard-function.md`, 715 words, numbered equations (9.4).

- Question of the page, and where we arrive: which states of a Fermi sea respond to a weak local potential?
  We arrive at the static Lindhard function (9.4), built only from pairs with one state on each side of the
  Fermi surface, with $\chi_0(q\to0)=D(E_F)$.
- Main result for the key box: (9.4), with "only pairs where one state is filled and the other is empty
  contribute, so the response is built at the Fermi surface, and at $q\to0$ it is the density of states".
- Equation of another page that it starts from, for the recall box: (9.3), the mixing of Section 9.3.
- Derivation told in words, for a steps fold: "From the mixing (9.3) to the Lindhard function (9.4)". The
  one-particle states $|k\rangle$, the potential $V_q$, the change of $n_F(\varepsilon_k)$ weighted by the
  mixing, and the $q\to0$ limit last. The sign of the induced density against $\chi_0$ is item 2 of "Open for
  the lecturer", so the fold stops at (9.4) as written and does not state $\delta n=\pm\chi_0 v$ until the
  pick.
- Lab box, with the source and the number that the source states: none. No fetched source states a Pauli
  susceptibility or a compressibility, and the measured response goes on 9.4b.
- Pen-and-paper problem: for the spinless chain $\varepsilon_k=-2t\cos k$, compute $D(E_F)=1/(\pi v_F)$ at half
  filling and at quarter filling. Answer $1/(2\pi t)\approx0.159/t$ and $1/(\sqrt2\pi t)\approx0.225/t$ per
  site.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on $\chi_0(q\to0)$ has a
  question of 20 words and points to "the figure". It is cut, with the summand of (9.4) in the question and
  no reference to the figure. New picture question, "For a chain with $k_F=\pi/4$, which picture shows the
  summand of (9.4) at $q=0.3$?", the right option has two windows of width $q$ next to $\pm\pi/4$, the wrong
  ones have the windows at $\pm\pi/2$ and one window at $k=0$. numpy, the same few lines as `occupation.py`,
  since a summand is not a pyqula output.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: `occupation` has no numbers on its axes. It needs $k$
  ticks at $-\pi$, $-\pi/2$, $0$, $\pi/2$, $\pi$, energy ticks at $-2$, $0$, $2$ in units of $t$, and a scale on
  the summand.

## 9.4b Nesting and the divergence of the Lindhard function

File `04b-nesting-and-the-divergence-of-the-lindhard-function.md`, 1426 words, numbered equations (9.5).

- Question of the page, and where we arrive: at which wavevector does the Lindhard function diverge, and what
  does it predict? We arrive at the nesting vector, $2k_F$ in a chain with $\chi_0(2k_F)\sim\ln(W/T)$, and
  $Q=(\pi,\pi)$ for the half-filled square lattice, where a new order appears. The opener replaces "In the
  first part we built". The paragraph of 188 words is split after "the order that we found with mean field in
  Section 1.13".
- Main result for the key box: two boxes. The first is the nesting statement in words with
  $\chi_0(2k_F)\sim\ln(W/T)$, "a response that diverges at $q^\star$ means that the state is unstable to an
  order with that wavevector". The second is (9.5), with "at $\omega\neq0$ the same pairs build the
  particle-hole continuum".
- Equation of another page that it starts from, for the recall box: (9.4).
- Derivation told in words, for a steps fold: "The logarithm of the chain at 2kF". Linearize the band at the
  two Fermi points, the summand becomes $\tanh(v_Fp/2T)/(2v_Fp)$, and the integral of $\tanh x/x$ up to a
  cutoff gives $\ln(W/T)$. The prefactor, and the doubling at half filling where $3k_F=-k_F$, are checked
  with a number before they are written.
- Lab box, with the source and the number that the source states: optimally doped Bi$_2$Sr$_2$CaCu$_2$O$_{8+x}$,
  https://arxiv.org/abs/1708.01929, stored as `mitrano2018_arxiv1708.01929.txt`. The abstract says "Here, we
  present the first measurement of χ''(q,ω) for a cuprate, optimally doped Bi2Sr2CaCu2O8+x (Tc=91 K), using
  momentum-resolved inelastic electron scattering." and "In the medium energy range 0.1-2 eV relevant to the
  strange metal, the spectra are dominated by a featureless, temperature- and momentum-independent continuum
  persisting to the eV energy scale." The box ties this to $\mathrm{Im}\,\chi_0(q,\omega)$ of (9.5). Our
  reading, marked as ours, is that a Fermi sea gives a continuum whose edges move with $q$, so a continuum
  that does not depend on $q$ is not the Lindhard form.
- Pen-and-paper problem: a spinless chain with $1/3$ of an electron per site. Find $k_F$, the nesting vector
  and the period of the charge density wave, and show that $\varepsilon(k+Q)=-\varepsilon(k)$ for the square
  lattice with $Q=(\pi,\pi)$. Answer $k_F=\pi/3$, $q^\star=2\pi/3$, a period of 3 sites.
- Quizzes to rewrite, and a picture question or equations as options: the two quizzes pass the lint and stay,
  each checked against the page. New picture question, "Each picture shows the Fermi surface $\varepsilon(k)=\mu$
  of the square lattice. Which one is nested by one vector $Q$?", the diamond at $\mu=0$ is right, the circle
  at $\mu=-3t$ and the rounded square at $\mu=-t$ are wrong. Each picture has $k_x$, $k_y$ and the first zone
  dashed. pyqula `h.get_fermi_surface` if it gives the contour on the square lattice, else a numpy contour of
  $\varepsilon(k)=\mu$.
- Figures to add, each with its pyqula script or the reason for numpy: `lindhard_map` is redrawn to the rules.
  It is a pyqula script `lindhard_square.py` with `h.get_chi` at $\omega\to0$ only if it gives the
  normalization and the sign of (9.4) (the sheet confirms) and the ratio $2.6$ of $(\pi,\pi)$ to $q=0$ at
  $T=0.1t$. Else it stays numpy.
- Old figures of the page that break the plot rules: `lindhard_map` scales each panel to its own maximum,
  has no colorbar, and draws the zone as its frame. It needs one shared scale, for instance $\chi_0(q)/\chi_0(0)$
  from $0$ to $2.6$ with a colorbar, the extended zone with the first zone dashed, and ticks at $\pm\pi$.
  `s09f01_nesting` is a converted figure.

## 9.5a Interactions as a perturbation, with RPA, plasmons and the Stoner instability

File `05-interactions-as-a-perturbation-with-rpa-plasmons-and-the-stoner-instability.md`, 1154 words, numbered equations (9.6), (9.7).

- Question of the page, and where we arrive: what does the interaction do to the bare response $\chi_0$? We
  arrive at the RPA (9.6), $\chi=\chi_0/(1+U\chi_0)$, which screens the charge, and at the plasmon (9.7), a
  zero of its denominator that lives at $\omega_p$ where no particle-hole pair exists. The opener replaces
  "So far the perturbation has been an external impurity".
- Main result for the key box: two boxes, (9.6) with "the sum of the bubble series, which has a pole that no
  finite order of $U$ has", and (9.7) with "a collective mode at $\omega_p$, also at $q=0$".
- Equation of another page that it starts from, for the recall box: (9.5), the dynamical Lindhard function of
  Section 9.4b.
- Derivation told in words, for a steps fold: two folds. "From the bubble series to (9.6)", the first terms
  and the geometric sum. "From a zero of the denominator to the plasma frequency", the expansion of (9.5) at
  $\omega\gg v_Fq$, $\chi_0\approx-nq^2/(m\omega^2)$, so $1+v(q)\chi_0=0$ gives $\omega_p$. The sign of this
  fold depends on item 1 of "Open for the lecturer", so it is written after the pick. Here $\chi_0$ and $n$ are those
  of both spins. Since the pick of 2026-11-22 the fold writes $\chi_0\approx-n_\sigma q^2/(m\omega^2)$ for one spin,
  with $n_\sigma=n/2$, and the zero of $1+2v(q)\chi_0$, which is the same $\omega_p$.
- Lab box, with the source and the number that the source states: graphene on SiO$_2$/Si,
  https://arxiv.org/abs/1202.4993, stored as `fei2012_arxiv1202.4993.txt`. The abstract says "The wavelength of
  graphene plasmons is of the order of 200 nm at technologically relevant infrared frequencies, and they can
  propagate several times this distance." and "We have succeeded in altering both the amplitude and wavelength
  of these plasmons by gate voltage." The probe is infrared nano-imaging. Our reading, marked as ours, is
  that graphene is two-dimensional, so its plasmon goes to zero at $q\to0$ and is not the three-dimensional
  form (9.7), and that the gate changes the density and so $\chi_0$.
- Pen-and-paper problem: sum the first three terms of the series of (9.6) for $U\chi_0=0.5$ and compare with
  (9.6), then do the same for $U\chi_0=2$. Answer $0.75\chi_0$ against $0.667\chi_0$, and for $U\chi_0=2$ the
  series grows ($3\chi_0$ after three terms) while (9.6) gives $0.333\chi_0$. The point is the sentence of the
  page on a series that is summed to all orders.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the plasmon has a question
  of 20 words and refers to Figure 9.2 by number. It is cut, with (9.7) and the edge of the continuum
  $\hbar\omega_+=\hbar v_Fq+\hbar^2q^2/2m$ in the question, and no figure number. The quiz on screening links
  (9.6) and gets it as a display. New with equations as options, "Which series does (9.6) sum?", options
  $\chi_0-\chi_0U\chi_0+\chi_0U\chi_0U\chi_0-\dots$, which is right, the series with all signs positive, and
  $\chi_0-U\chi_0^2$ alone. No picture question, since Figure 9.2 is a converted figure that gives the answer.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none. `bubbles` is a diagram, and `s09f02_plasmon` is a
  converted figure, whose caption is item 1 of "Open for the lecturer".

## 9.5b The Stoner instability

File `05b-the-stoner-instability.md`, 1276 words, numbered equations (9.8).

- Question of the page, and where we arrive: when does the spin response of a metal diverge, and at which $q$?
  We arrive at $U\chi_0(q,0)=1$ (9.8), which at $q=0$ is the Stoner criterion $UD(E_F)=1$, and which at a nested
  Fermi surface is met first at $Q=(\pi,\pi)$. The opener replaces "In the first part we used". The paragraph
  of 179 words is split before "However, [(9.8)] is more general".
- Main result for the key box: (9.8), with "the paramagnet becomes unstable at the $q$ where $\chi_0(q,0)$ is
  largest, a ferromagnet at $q=0$ and an antiferromagnet at $Q=(\pi,\pi)$".
- Equation of another page that it starts from, for the recall box: (9.6), and (6.3) of Session 6 named in
  the text of the box.
- Derivation told in words, for a steps fold: "From the Hubbard term to the spin denominator". The identity
  $Un_\uparrow n_\downarrow=\tfrac U4(n^2-m^2)$, then the simplest case $q=0$, a uniform field $h$ plus the
  exchange field of the induced $m$, which gives $m\propto\chi_0h/(1-U\chi_0)$. The factors of 2 of the spin
  convention come from the sheet.
- Lab box, with the source and the number that the source states: Cr$_{1-x}$V$_x$, https://arxiv.org/abs/0807.3586,
  stored as `sokolov2008_arxiv0807.3586.txt`. The abstract says "At xc=0.037 we have found temperature
  dependent, resolution limited elastic scattering at 4 incommensurate wave vectors Q=(1+/-delta_1,2, 0,
  0)*2pi/a, which correspond to 2 SDWs with Neel temperatures of 19 K and 300 K." and "Our neutron diffraction
  measurements indicate that the electronic structure of Cr is robust, and that tuning Cr to its QCP results
  not in the suppression of antiferromagnetism, but instead enables new spin ordering due to novel nesting of
  the Fermi surface of Cr." The probe is neutron diffraction. Our reading, marked as ours, is that (9.8) is met
  first at an incommensurate nesting vector here, and not at $q=0$ or at $(\pi,\pi)$.
- Pen-and-paper problem: show $Un_\uparrow n_\downarrow=\tfrac U4(n^2-m^2)$, then find the Stoner $U$ of the
  half-filled chain, with $\chi_0(0,0)=D(E_F)=1/(2\pi t)$ per spin, and say why $q=\pi$ comes first at low
  temperature. Answer $U=2\pi t\approx6.28t$, the value of the Session 6 plan, while
  $\chi_0(\pi)\sim\ln(W/T)$ makes the threshold at $q=\pi$ go to zero as $T\to0$.
- Quizzes to rewrite, and a picture question or equations as options: the two quizzes pass the lint and stay,
  each checked against `stoner` and `rpa_factor`. New picture question, "Each curve is $\chi_0(q,0)$ along
  $\Gamma$, $X$, $M$, $\Gamma$ for one filling of the square lattice. Which metal orders as an
  antiferromagnet first?", the curve with its maximum at $M$ is right. numpy, with the code of `stoner.py`,
  for the reason of the next field.
- Figures to add, each with its pyqula script or the reason for numpy: none. `stoner` stays numpy, since
  `lindhard_map` of 9.4b is the one figure that may move to a pyqula script, and the two must give the same
  $0.26/t$ and $0.68/t$.
- Old figures of the page that break the plot rules: `stoner` quotes $0.68/t$ and $0.26/t$ and has no ticks on
  the $\chi_0$ axis and no unit. It needs ticks at $0.26$ and $0.68$ and the name "$\chi_0(q,0)$ in units of
  $1/t$". `rpa_factor` quotes $0.60$ and $3.1$ and has no ticks on $\chi/\chi_0$. It needs ticks at $0.60$, $1$
  and $3.1$. `spin_patterns` is a drawing, and the panel of `s09f01_nesting` is converted.

## 9.6a Impurities as diagnostics I, Friedel oscillations in a metal

File `06-impurities-as-diagnostics-i-friedel-oscillations-in-a-metal.md`, 1154 words, numbered equations (9.9).

- Question of the page, and where we arrive: how does the density around one impurity in a metal decay, and
  what does it tell us? We arrive at the Friedel oscillation (9.9), $\cos(2k_F|x|+\varphi_0)/|x|^d$, whose
  wavevector is the diameter of the Fermi surface. The opener replaces "We now go to the most physical
  realization".
- Main result for the key box: (9.9), with "the period is set only by the Fermi surface, and the power of the
  envelope only by the dimension".
- Equation of another page that it starts from, for the recall box: (9.4).
- Derivation told in words, for a steps fold: "From the singularity of chi0 at 2kF to the 1/x tail". The
  simplest case is the one-dimensional closed form of the page, whose Fourier transform gives
  $\pi/2-\mathrm{Si}(2k_F|x|)$ and the tail $\cos(2k_Fx)/(2k_F|x|)$. The powers for $d=2,3$ are stated, not
  derived. The overall sign waits for item 2 of "Open for the lecturer".
- Lab box, with the source and the number that the source states: Au(111), https://doi.org/10.1103/PhysRevB.103.245311,
  stored as `sotthewes2021_physrevb.103.245311.txt`, with the published abstract pasted from the PDF of the
  university repository. The abstract says "The periodicity of the standing waves is not given by λF /2 = 1.8
  nm, as expected based on the band diagram of Au(111), but rather varies between 1.5 and 2.1 nm depending on
  the exact width of the terraces." The probe is thermovoltage STM. Our reading, marked as ours, is that
  $\lambda_F/2=\pi/k_F$ is the period of (9.9).
- Pen-and-paper problem: a spinless chain with $0.2$ electrons per site. Find the period of the Friedel
  oscillation, and the factor by which the envelope falls from $x=10$ to $x=40$ in $d=1$ and in $d=2$. Answer
  $k_F=0.2\pi$, a period of 5 sites, factors 4 and 16.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the period has a question of
  20 words. It is cut, with $\delta n\propto\cos(2k_Fx)$ in the question. The quiz on $d=2$ passes the lint and
  gets (9.9) as a display. New picture question, "Each map shows the LDOS change around one impurity in a
  square lattice. Which metal has the largest Fermi circle?", the shortest rings are right. The maps come from
  the pyqula script of `friedel2d` at three energies, one color scale with a colorbar, axes in sites.
- Figures to add, each with its pyqula script or the reason for numpy: `friedel2d` is redrawn to the rules
  with a pyqula script `friedel_square.py`, `embedding.Embedding(h,m=hv).get_ldos(...)` of the notebook cell
  "Impurities in a 2d metal". It must give $k_F=0.80$ and the period $\pi/k_F\approx3.9$ at $E=-3.4t$. The
  quantity is the LDOS at one energy, as the caption says, and not the density.
- Old figures of the page that break the plot rules: `friedel2d` has both panels with the axes off. The
  $k$-space panel has no $k_x$, $k_y$ and draws the zone as a solid grey square, and the signed real-space map
  has no colorbar. `period`, in a feedback, has no ticks. It needs $x$ ticks at $0$, $4$, $8$, $12$ and ticks
  at $\pm1$.

## 9.6b Friedel oscillations in a chain, and the contrast with an insulator

File `06b-friedel-oscillations-in-a-chain-and-the-contrast-with-an-insulator.md`, 763 words, numbered equations none.

- Question of the page, and where we arrive: what does the oscillation look like in a chain, and what changes
  when the chain has a gap? We arrive at a period $\pi/k_F$ with a $1/x$ envelope in the metal, and a decay
  $e^{-x/\xi}$ within a few sites in the insulator. The opener replaces "In the first part we derived". The
  paragraph of 208 words is split before "As a complementary check".
- Main result for the key box: one box with the two forms, $\delta n\sim\cos(2k_Fx)/x$ for the metal and
  $\sim e^{-x/\xi}$ for the gapped chain, unnumbered, with "the decay law tells whether there is a Fermi
  surface".
- Equation of another page that it starts from, for the recall box: (9.9).
- Derivation told in words, for a steps fold: "Why a gap gives an exponential". A gap makes $\chi_0(q)$
  analytic in a strip $|\mathrm{Im}\,q|<1/\xi$, and the Fourier transform of such a function decays as
  $e^{-x/\xi}$. Simplest case first, the transform of $1/(q^2+\xi^{-2})$.
- Lab box, with the source and the number that the source states: none. The Au(111) box of 9.6a is the
  measured oscillation, and no fetched source holds a number for a chain.
- Pen-and-paper problem: in a gapped chain the response decays as $e^{-x/\xi}$ with $\xi=2.5$ sites. How far
  from the impurity is it below $1\%$ of its value at $x=1$, and how far for a $1/x$ envelope? Answer
  $\xi\ln100\approx11.5$ sites against $100$ sites.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the gapped chain has a
  question of 18 words. It is cut, with $e^{-x/\xi}$ in the question. New with equations as options, "Which
  envelope does one impurity give in a chain with a gap?", options $e^{-x/\xi}$, which is right, $1/x$ and
  $1/x^2$. No picture question, since 9.6a has one.
- Figures to add, each with its pyqula script or the reason for numpy: none. `friedel` stays numpy, since
  it draws the density and the pyqula embedding of the notebook gives the LDOS at one energy, which in a
  chain does not decay as $1/x$ (item 5 of "Open for the lecturer").
- Old figures of the page that break the plot rules: `friedel` has no numbers on its axes. It needs $x$ ticks
  at $0$, $20$, $40$, $60$ sites and $\delta n$ ticks, and the titles keep $k_F$ and the period.

## 9.7 Impurities as diagnostics II, magnetic impurities in a superconductor

File `07-impurities-as-diagnostics-ii-magnetic-impurities-in-a-superconductor.md`, 1180 words, numbered equations (9.10).

- Question of the page, and where we arrive: what does one impurity do to a superconductor, which has a gap
  and no Fermi surface? We arrive at a non-magnetic impurity that changes almost nothing, and a magnetic one
  that binds a state at $E_b$ of (9.10), which crosses zero at $\alpha=1$, where the fermion parity changes.
  The opener replaces "We described superconductors in Session 5".
- Main result for the key box: (9.10), with "the bound state starts at the gap edge, crosses zero at
  $\alpha=1$, and the crossing is a change of the ground state".
- Equation of another page that it starts from, for the recall box: (5.9), the BCS dispersion, whose minimum
  $|\Delta|$ at the Fermi surface is the gap.
- Derivation told in words, for a steps fold: none. The page quotes (9.10) and does not derive it, and the
  T-matrix of a classical spin is beyond the page.
- Lab box, with the source and the number that the source states: an iron atom in a superconductor,
  https://www.nature.com/articles/nphys3508, stored as `menard2015_nphys3508.txt` with the arXiv abstract
  1506.06666. The abstract says "In addition to the well-known Shiba bound state present on top of an
  impurity we reveal the existence of a star shaped pattern which extends as far as 12 nm from the impurity
  location." The probe is STM. The stored text names no host material, so the box says "a superconductor"
  and does not name it.
- Pen-and-paper problem: find $\alpha$ where $E_b=\Delta/2$, and show from (9.10) that $E_b(1/\alpha)=-E_b(\alpha)$.
  Answer $\alpha=1/\sqrt3\approx0.58$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz at $\alpha=0.5$ has a question
  of 16 words. It is cut, with (9.10) in the question. The quiz on $\alpha>1$ passes the lint and stays. New
  with equations as options, "Which formula gives a bound state that stays in the gap and crosses zero at
  $\alpha=1$?", options $(1-\alpha^2)/(1+\alpha^2)$, which is right, $1-\alpha^2$, which leaves the gap above
  $\alpha=\sqrt2$, and $1/(1+\alpha^2)$, which never crosses zero. No picture question, since the spectrum is
  symmetric in $\pm E_b$ and cannot show the crossing.
- Figures to add, each with its pyqula script or the reason for numpy: one figure from a pyqula script
  `ysr_chain.py`, the DOS of the s-wave chain against the exchange $J$ of one site, with `embedding.Embedding`
  and `eb.dos` of the notebook cell "Single magnetic impurity in a superconductor". The caption gives the $J$
  where the state crosses zero, as the script finds it. It does not draw (9.10) on top unless the sheet gives
  $\alpha$ in terms of the pyqula $J$.
- Old figures of the page that break the plot rules: none, `s09f03_ysr` is a converted figure.

## 9.8 Impurities as diagnostics III, vacancies in topological matter

File `08-impurities-as-diagnostics-iii-vacancies-in-topological-matter.md`, 1356 words, numbered equations none.

- Question of the page, and where we arrive: can one missing atom tell a topological insulator from a trivial
  one with the same gap? We arrive at the rule that a vacancy binds an in-gap state when the bulk invariant is
  not zero and the vacancy keeps the protecting symmetry. The opener replaces "The strongest local impurity".
  The paragraph of 154 words is split before "It is known that", and the one of 232 words before "The same
  logic holds for a Chern insulator".
- Main result for the key box: one box with the rule in words, as the italic sentence of the page says it. The
  "if and only if" of the page is item 4 of "Open for the lecturer", so the box keeps the words of the page
  until the pick.
- Equation of another page that it starts from, for the recall box: (3.4), the Chern number that the vacancy
  detects.
- Derivation told in words, for a steps fold: none. The argument has no equation.
- Lab box, with the source and the number that the source states: none. No source was fetched with a
  measured bound state at a vacancy of a Chern insulator or of a chiral p-wave superconductor.
- Pen-and-paper problem: for the Haldane model with $t_2=0.15t$ and phase $\pi/2$, the gap is $6\sqrt3\,t_2$.
  Compute it, and the sublattice mass $M$ of a trivial insulator with the same gap $2M$. Answer $1.56t$ and
  $M=0.78t$, the values of `vacancy_dos`.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the Haldane vacancy has a
  question of 19 words, and it is cut. The quiz on "no in-gap mode" refers to Section 3.9 by number, and the
  number goes. Its SSH counter example (a vacancy plus an onsite $2t$ on its neighbor, no state in the gap
  $\pm0.5t$) is checked with a number, and the feedback numbers of the first quiz ($\pm0.22t$, $-0.14t$,
  $0.04t$, $-0.016t$) too. New picture question, "Each plot is the LDOS next to one vacancy of a honeycomb
  insulator. Which one has $C\neq0$?", the Haldane model with $t_2=0.15t$ is right, the mass $M=0.78t$ and the
  Haldane model with $M=1.0t>3\sqrt3\,t_2$ are wrong. The builder checks that the third has no in-gap state,
  and if it has one, uses the clean torus instead. Same pyqula script as the redraw below.
- Figures to add, each with its pyqula script or the reason for numpy: `vacancy_dos` becomes a pyqula script
  `vacancy_honeycomb.py` only if it gives the gap $1.56t$, the state at $E=0$ and the $45\%$ on the three
  neighbors. `h.add_haldane(x)` is not $t_2$, and $t_2=0.15t$ is probably $x=2\cdot0.15/\sqrt3=0.173$ (the sheet
  confirms). Else it stays numpy.
- Old figures of the page that break the plot rules: `vacancy_dos` has no ticks or unit on the LDOS axis. It
  needs ticks and the unit "states per $t$, summed on three sites". `s09f04_vacancy` is converted.

## 9.9 Impurities as diagnostics IV, screening in quantum magnets

File `09-impurities-as-diagnostics-iv-screening-in-quantum-magnets.md`, 1518 words, numbered equations (9.11).

- Question of the page, and where we arrive: how do the spins of a quantum magnet screen one local field, and
  does the decay tell whether the magnet has a gap? We arrive at (9.11), a $(-1)^n/n$ law for the gapless
  $S=1/2$ chain and $(-1)^ne^{-n/\xi}$ for the gapped $S=1$ chain, and at the rule that a power law means
  gapless and an exponential means gapped. The opener replaces "The last case study brings us".
- Main result for the key box: (9.11), with the italic diagnostic sentence of the page.
- Equation of another page that it starts from, for the recall box: (8.15), the spinon Hamiltonian, and (9.9).
- Derivation told in words, for a steps fold: "From a field on one spin to the impurity of a spinon chain".
  $S^z_0=(f^\dagger_{0\uparrow}f_{0\uparrow}-f^\dagger_{0\downarrow}f_{0\downarrow})/2$, so the field gives the
  onsite energies $\mp h/2$ to the two spinon species, each species is the impurity of 9.6, and at half
  filling $2k_F=\pi$ gives the sign $(-1)^n$. The hopping sign of (8.15) does not change the moment, since the
  chain is bipartite.
- Lab box, with the source and the number that the source states: Y$_2$BaNi$_{1-x}$Mg$_x$O$_5$, spin-1 chains,
  https://arxiv.org/abs/cond-mat/0211703, stored as `kenzelmann2003_arxivcond-mat-0211703.txt`. The abstract
  says "The wave vector dependence of its intensity provides direct evidence for staggered magnetization at
  chain ends, which decays exponentially towards the bulk (xi = 8(1) at T=0.1K)." The probe is inelastic
  neutron scattering. The abstract gives no unit for $\xi$, so "in units of the spacing of the chain" is
  marked as ours.
- Pen-and-paper problem: for the staggered moment $(-1)^ne^{-n/\xi}$ with $\xi=8$, find the factor from $n=8$
  to $n=24$, and compare with $1/n$. Answer $e^{-2}\approx0.14$ against $1/3$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on $\xi\approx2.5$ has a
  question of 17 words, and it is cut with (9.11) in the question. The quiz on the logarithmic axis refers to
  Figure 9.5 by number. It becomes a picture question, "Three gapped spinon chains. Each plot shows
  $|\langle S^z_n\rangle|$ on a logarithmic axis. Which chain has the smallest gap?", the shallowest line is
  right, from the script of the redraw with three dimerizations. One color and one axis range for the three.
- Figures to add, each with its pyqula script or the reason for numpy: `spinon_impurity` becomes a pyqula
  script `spinon_chain_field.py` (a finite chain, `add_exchange` on site 0, the moment from the eigenvectors)
  only if it gives the moments of the numpy script within $10^{-6}$. This also ends the SVG that changes on
  every run. Else it stays numpy.
- Old figures of the page that break the plot rules: `spinon_impurity` has no $y$ ticks on the left panel and
  no numbers on either axis of the logarithmic panel, where the numbers are the point. It needs decades on the
  log axis and $n$ ticks. `s09f05_decay` is converted.

## 9.10a Disorder and Anderson localization

File `10-disorder-and-anderson-localization.md`, 1213 words, numbered equations (9.12).

- Question of the page, and where we arrive: the page already opens with "What happens when we put many
  impurities in the whole material?". We arrive at the IPR (9.12), $1/N$ for extended states and finite for
  localized ones, and at the self-dual point $V_0=2t$ of the Aubry-André chain, where all states change at
  once.
- Main result for the key box: (9.12), with "the IPR falls as $1/N$ for an extended state, stays finite for a
  localized one, and falls with a power between the two at the critical point".
- Equation of another page that it starts from, for the recall box: none. The page starts from the
  tight-binding chain, written on the page.
- Derivation told in words, for a steps fold: "Why the transition is at V0 = 2t". The Fourier transform
  $\psi_n=\sum_me^{2\pi iqmn}\phi_m$ maps the chain with $(t,V_0/2)$ onto the chain with $(V_0/2,t)$, so the two
  are the same model at $V_0=2t$. The page names the point without the argument, so the fold is short.
- Lab box, with the source and the number that the source states: none. Roati 2008 (0804.2609), Lahini 2009
  (0807.2845) and Lüschen 2018 (1709.03478) were fetched, and none of the abstracts states a number with a unit.
- Pen-and-paper problem: compute the IPR of $\psi_n\propto e^{-|n|/\xi}$ on an infinite chain, and show that it
  is about $1/(2\xi)$ for large $\xi$, with no $N$ in it. Answer $\coth(2/\xi)/\coth^2(1/\xi)=0.0503$ for
  $\xi=10$.
- Quizzes to rewrite, and a picture question or equations as options: both quizzes have questions of 17 and
  18 words. They are cut, with (9.12) in the question. New picture question, "Each picture shows $|\psi_i|^2$ of
  one eigenstate of the Aubry-André chain. Which state keeps its IPR when the chain grows?", the state at
  $V_0=3t$ is right, $V_0=t$ and $V_0=2t$ are wrong. The pictures share the axes and are drawn from the pyqula
  script below if it gives the eigenvectors, else from numpy.
- Figures to add, each with its pyqula script or the reason for numpy: `aah_ipr` becomes a pyqula script
  `aah_ipr.py` with `h.get_ipr()` only if it returns the IPR of each state on a ring with $q=F_{k-1}/F_k$ and
  gives $N\cdot\mathrm{IPR}\approx2$ below $V_0=2t$. Else it stays numpy.
- Old figures of the page that break the plot rules: `aah_ipr` has no numbers on its logarithmic IPR axis,
  since `style.arrows` removes them. It needs decades at $10^{-3}$, $10^{-2}$, $10^{-1}$, $1$. `s09f06_localization`
  is converted.

## 9.10b Random disorder and the special role of one dimension

File `10b-random-disorder-and-the-special-role-of-one-dimension.md`, 1182 words, numbered equations none.

- Question of the page, and where we arrive: what does truly random disorder do, and why is one dimension
  special? We arrive at the Anderson insulator in $d\geq3$, with a mobility edge and no spectral gap, and at
  $\xi\propto(t/W)^2$ in one dimension, where any disorder localizes every state. The opener replaces "In the
  first part we met". The paragraph of 184 words is split before "Above it, there are states at every energy".
- Main result for the key box: one box, unnumbered, with $\xi(W)\propto(t/W)^2$ and "in one dimension any
  $W>0$ localizes every state, and a sample shorter than $\xi$ still looks metallic". No prefactor.
- Equation of another page that it starts from, for the recall box: (9.12).
- Derivation told in words, for a steps fold: none. The scaling theory is quoted, not derived.
- Lab box, with the source and the number that the source states: none. Billy 2008 (0804.1621), Kondov 2011
  (1105.5368), Jendrzejewski 2012 (1108.0137), Semeghini 2015 (1404.3528), White 2019 (1911.04858) and Yu 2026
  (2602.07654) were fetched, and none of the abstracts states a number with a unit.
- Pen-and-paper problem: with $\xi=100$ sites at $W=0.5t$ and $\xi\propto W^{-2}$, find $\xi$ at $W=0.25t$ and
  the $W$ where $\xi$ is $1000$ sites. Answer $400$ sites and $W\approx0.16t$.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the Anderson insulator has
  a question of 18 words, and it is cut. Its first feedback says that the density of states at $W=20t$ is
  "about $1/W=0.05/t$". For $w_n$ in $[-W,W]$ it is $1/(2W)=0.025/t$, which a cube of $10^3$ sites gives, so the
  rewrite uses $0.025/t$ with an assert and reports it. The quiz on halving $W$ stays. New with equations as
  options, "Which law gives the localization length of a chain at weak disorder?", options $(t/W)^2$, which is
  right, $t/W$ and $e^{t/W}$.
- Figures to add, each with its pyqula script or the reason for numpy: none. `localization_length` stays numpy,
  since a transfer matrix over $2\cdot10^5$ sites at $E=0$ has no pyqula call, and `h.get_tails()` works on the
  eigenvectors of a finite chain.
- Old figures of the page that break the plot rules: `mobility` quotes the band edges $\pm(6t+W)$ and
  $W_c\approx8t$ and has no ticks. It needs $W$ ticks at $0$, $4$, $8$, $12$ and $E$ ticks at $\pm6$, $\pm12$.
  `localization_length` follows the rules. The panel of `s09f06_localization` is converted.

## 9.11 Closing summary

File `11-closing-summary.md`, 1071 words, numbered equations none. A closing page.

- Question of the page, and where we arrive: the page opens with what we started from and keeps its form. It
  gets the list "After this session we can do the following tasks", each task with its section. Read the sign
  of the exchange from the intercept of $1/\chi(T)$, in Section 9.2. Write the first-order mixing of a state
  and name the three cases where it fails, in Section 9.3. Compute $\chi_0(q\to0)=D(E_F)$, in Section 9.4a,
  and find the nesting vector of a band, in Section 9.4b. Sum the RPA series and tell a plasmon from the
  particle-hole continuum, in Section 9.5a. Decide at which $q$ and at which $U$ a metal orders first, in
  Section 9.5b. Predict the period $\pi/k_F$ and the envelope of a Friedel oscillation, in Sections 9.6a and
  9.6b. Compute the Shiba energy and say where the fermion parity changes, in Section 9.7. Use a vacancy to
  test a gapped phase for topology, in Section 9.8. Tell a gapped magnet from a gapless one by the decay of an
  impurity response, in Section 9.9. Compute the IPR and use its scaling with $N$, in Section 9.10a, and
  estimate $\xi(W)$ of a chain, in Section 9.10b.
- Main result for the key box: none, a closing page.
- Equation of another page that it starts from, for the recall box: none, the bullets already link the
  numbered equations.
- Derivation told in words, for a steps fold: none.
- Lab box, with the source and the number that the source states: none, a closing page.
- Pen-and-paper problem: none, a closing page.
- Quizzes to rewrite, and a picture question or equations as options: the quiz on the $1/|x|$ decay has a
  question of 22 words. It is cut, with $1/|x|$ and $e^{-x/\xi}$ in the question, and its panel of
  `s09f05_decay` stays. No new quiz.
- Figures to add, each with its pyqula script or the reason for numpy: none.
- Old figures of the page that break the plot rules: none, the panel of `s09f05_decay` is converted.

## Candidates for the lab boxes

The notebook of the session has no "In the lab" cell. Every source was fetched on 2026-11-21 with
`webnotes/labsource.py --session 9`. Each quoted sentence above was checked by the scratch script
`lab_quotes.py` of this plan to be a substring of the abstract block of its file in
`webnotes/sources/.full/session09/`, never of an editor summary, and to hold the number. `labsource.py --check 9`
reads the boxes of the pages, so it runs after the builders.

Planned, one per page.

- 9.2, herbertsmithite, `helton2007_arxivcond-mat-0610539.txt`, $-300$ K and 50 mK.
- 9.4b, Bi$_2$Sr$_2$CaCu$_2$O$_{8+x}$, `mitrano2018_arxiv1708.01929.txt`, 91 K and 0.1 to 2 eV.
- 9.5a, graphene, `fei2012_arxiv1202.4993.txt`, 200 nm.
- 9.5b, Cr$_{1-x}$V$_x$, `sokolov2008_arxiv0807.3586.txt`, 19 K and 300 K.
- 9.6a, Au(111), `sotthewes2021_physrevb.103.245311.txt`, 1.8 nm, 1.5 to 2.1 nm. The text was pasted from the
  published PDF, since Crossref has no abstract of APS.
- 9.7, an iron atom in a superconductor, `menard2015_nphys3508.txt`, 12 nm, with no host material named.
- 9.9, Y$_2$BaNi$_{1-x}$Mg$_x$O$_5$, `kenzelmann2003_arxivcond-mat-0211703.txt`, $\xi=8(1)$ at 0.1 K.

Fetched and not used, since the abstract has no number with a unit for the page: Tedoldi 1999
(cond-mat/9902084, the NMR of the same Haldane chain), Roati 2008, Billy 2008, Farinacci 2018 (1807.01344),
Lee 2004 (cond-mat/0402016), Kondov 2011, Semeghini 2015, Yu 2026, Ruby 2016 (1608.03457), Ruby 2015
(1502.05048), Chen 2012 (1202.4996, "over 40 times smaller" is a ratio with no unit), Lüschen 2018, Jeckelmann
2016 (1509.08296), Khotkevych-Sanina 2013 (1311.7624), Fransson 2007 (cond-mat/0701606), Lahini 2009, Choi 2016
(1608.03752), Moca 2008 (0805.0700), Simon 2011 (1107.3648), Dendzik 2016 (1610.01736), Jendrzejewski 2012 and
White 2019. `mestre2008_arxiv0807.2632.txt` was fetched by a wrong id and is not about the session.

## Builder groups

Six groups, in the order of the pages. Two rules hold for all of them. A pyqula redraw must give the numbers
that the old script asserts or prints and that the page quotes, or the figure stays numpy and the builder
reports it. A quantity that two groups state is looked up on the page of the other group before it is
written. `g2_` and `g3_` both state $\chi_0$ of the half-filled square lattice at $T=0.1t$, $0.26/t$ at $q=0$,
$0.68/t$ at $(\pi,\pi)$ and their ratio $2.6$. `g4_`, `g5_` and `g6_` all state the $1/x$ against
$e^{-x/\xi}$ diagnostic and the $\xi\approx2.5$ sites of their quizzes, on 9.6b, 9.9 and 9.11.

- `g1_`: `index.md`, `01-response-functions-as-a-probe-of-the-ground-state.md`,
  `02-the-response-of-a-classical-magnet-as-a-first-example.md`. The index gets one opening question. The
  picture quiz of 9.1 is numpy. The sign of $J$ in the fold of 9.2 comes from the sheet.
- `g2_`: `03-linear-response-and-perturbation-theory-in-detail.md`,
  `04-the-fermi-sea-and-the-lindhard-function.md`, `04b-nesting-and-the-divergence-of-the-lindhard-function.md`.
  They share (9.3), (9.4) and the chain of `occupation`. The fold of 9.4a stops at (9.4) until item 2 of "Open
  for the lecturer" is picked. `lindhard_map` is the only figure of the session that may move to `h.get_chi`,
  and the normalization against (9.4) comes from the sheet.
- `g3_`: `05-interactions-as-a-perturbation-with-rpa-plasmons-and-the-stoner-instability.md`,
  `05b-the-stoner-instability.md`. They share (9.6) and its two channels. The plasma-frequency fold of 9.5a
  waits for item 1. `stoner` stays numpy and gets its ticks.
- `g4_`: `06-impurities-as-diagnostics-i-friedel-oscillations-in-a-metal.md`,
  `06b-friedel-oscillations-in-a-chain-and-the-contrast-with-an-insulator.md`. They share (9.9), `friedel`,
  `friedel2d` and the widget. The pyqula embedding gives the LDOS at one energy, which is right for `friedel2d`
  and wrong for `friedel`, so `friedel` stays numpy. Items 2 and 5 touch these pages.
- `g5_`: `07-impurities-as-diagnostics-ii-magnetic-impurities-in-a-superconductor.md`,
  `08-impurities-as-diagnostics-iii-vacancies-in-topological-matter.md`,
  `09-impurities-as-diagnostics-iv-screening-in-quantum-magnets.md`. Three impurity diagnostics, with the
  superconductors of pyqula on 9.7 and 9.8. `h.add_haldane(x)` is not $t_2$. The Ménard box names no host.
  Items 3, 4 and 6 touch these pages. After a redraw of `spinon_impurity`, read `git status` for SVGs that
  changed by accident.
- `g6_`: `10-disorder-and-anderson-localization.md`, `10b-random-disorder-and-the-special-role-of-one-dimension.md`,
  `11-closing-summary.md`. They share (9.12) and the IPR. The notebook draws its random potential as
  `v*(random-0.5)`, a box of width $v$, while the page has $[-W,W]$, a box of width $2W$, so a try-it number of
  `v` is not a $W$ of the page (item 7). Page 11 gets the list of tasks.

## Open for the lecturer

The lecturer decided on 2026-11-22 how to handle the points that the builders, the fixers and the rechecks left ("Fix
old-text errors, ask the rest"), and for the questions "ask me the top 5, other you decide by yourself". The 66 entries
of their lists and the seven items of the former version of this section were merged into 45 distinct points. The
sentences that were false as written, or that contradicted another sentence of the session, are corrected on the web
with the smallest change that makes them true. The points that were a choice were decided by the coordinator with the
rule of that day. The rule takes the option that makes the text true with the smallest change, and between two true
wordings the shorter and clearer one. It reduces a claim that no stored source or calculation supports to what is
supported, redraws an old plot under its name, and rewrites a box that does not match its notebook cell. It does not
touch a converted Blender figure or its overlay, while the caption of such a figure is text of the page, as point d1 of
the plan of Session 2 records. Four points would change a numbered equation, a convention or a rule that the .tex states,
and they were the list "For the lecturer". An independent check of the three lists on 2026-11-22 gave twelve findings.
Two of them sent a change back to the lecturer, the change of the key box of page `08` and the denominator of page `04`,
which were points 4 and 1 of that list, and the others are in the lists below. On the same day the lecturer picked
points 1 and 2, the definition of the response and the factor 2 of the spins. They are now the last two points of the
list "Decided on 2026-11-22", their changes are the last entries of the first list, and the two other points, now
numbered 1 and 2, stay for the lecturer. The blocks of the pages above say that a fold or a sign waits for these picks,
as they were written before them. Each change was checked first with a
calculation of its own, by two routes where a number is involved,
and the check script of its page, or the figure script that draws it, asserts it. The conventions sheet is up to date
since 2026-11-22, and its last section gives each point of the old text with what happened to it.

The seven items of the former version of this section went as follows. Item 1, the sign of the plasmon denominator, and
item 2, the sign of the induced density, were sentences that contradicted (9.6), (9.4) and the caption of `friedel`, so
they are corrected on the web. Item 3, "in the Born approximation", is corrected on the web. Item 4, "if and only if",
is corrected in the caption of Figure 9.4, and the italic rule of the key box is point 2 of "For the lecturer". Item 5,
the word LDOS of Section 9.6b, is corrected where the sentence was false. Item 6, the quantity of (9.11), is in "For the
lecturer". Item 7, the width of the random potential, was decided.

### Corrected on the web, to carry over to the .tex

The lines are those of `lecture_notes/src/sessions/session09.tex` on 2026-11-22, or of the figure file that is named.
The `.tex` is not changed in this pass, so until this list is carried over the PDF keeps the old wording.

- Page `01`, Section 9.1, third bullet. Old "A local change of temperature, measured as a change of temperature at
  another place, which gives the **thermal conductance**." New "..., which gives the **thermal diffusivity**, the thermal
  conductivity divided by the heat capacity per unit volume." Line 43. Asserted in `g1_01`, by finite differences of the
  heat equation and by its Gaussian, where the response depends on $\kappa$ and $C$ only through $\kappa/C$, and by the
  units, since $\kappa/C$ is in m$^2$/s only for a heat capacity per unit volume.
- Page `02`, Section 9.2, the paragraph after Figure `curie_weiss`. Old "In the ferromagnetic case the fluctuations
  *reinforce* the applied field ... In the antiferromagnetic case the fluctuations *oppose* the applied field, since they
  favor staggered order and not uniform order". New "In the ferromagnetic case the exchange field of the neighbors
  *reinforces* the applied field ... In the antiferromagnetic case the exchange field of the neighbors *opposes* the
  applied field, since the exchange favors staggered order and not uniform order". The paragraph, now of 151 words, is
  split before "In the antiferromagnetic case". Lines 89 to 92. Asserted in `g1_02`, the self-consistent $zJm$ is $+2h$
  and $-0.4h$ at $T=1.5T_c$.
- Page `02`, first quiz, the feedback of the right option, changed by the builder. Old "The exchange favors staggered
  order, which the uniform $\chi$ does not feel, so it does not diverge for $T>0$." New "The exchange favors staggered
  order, and a uniform field does not couple to this order. So the uniform $\chi$ does not diverge for $T>0$, and the
  exchange only makes it smaller than the $\chi$ of a free spin." Not in the .tex.
- Page `04b`, Section 9.4b, first paragraph. Old "This divergence is the Peierls instability, which drives
  one-dimensional metals to dimerize into a charge density wave, the order that we found with mean field in Section
  1.13." New "This divergence is the Peierls instability, which drives one-dimensional metals into a charge density wave
  with the period $\pi/k_F$. At half filling this period is two sites, as in the order that we found with mean field in
  Section 1.13." Lines 200 and 201. Asserted in `g2_04b`, the maximum of $\chi_0(q)$ at $2\pi/3$ for $\mu=-t$ and at
  $\pi$ at half filling.
- Page `04b`, caption of `lindhard_map`. Old "It uses the triangle integration of `h.get_chi`, which needs the pyqula of
  GitHub." New "It uses the triangle integration of `h.get_chi`." The release 0.0.97 of PyPI has it and 0.0.96 does not,
  which a version number on the page could not assert offline. Not in the .tex.
- Page `05`, Section 9.5a, after the steps fold. Old "which is a real pole, meaning a real phase transition." New "which
  is a real pole. A pole at $\omega=0$ is a phase transition, and a pole at a finite frequency, such as the plasmon, is a
  collective mode." Line 276. Asserted in `g3_05`, the static $\chi_0(q,0)>0$ at every $q$, so $1+U\chi_0>1$ for $U>0$,
  and the plasmon zero at $\omega_p$.
- Page `05`, caption of Figure 9.2. Old "It is a zero of the RPA *denominator* $1-v(q)\chi_0$". New "It is a zero of
  the RPA *denominator* $1+2v(q)\chi_0$". The first correction of 2026-11-22 gave $1+v(q)\chi_0$, the denominator of
  (9.6), and the factor 2 came with the pick of the lecturer of the same day, see the last entries of this list. `lecture_notes/src/figures/s09f02_plasmon.tex`, line
  12. The render and its overlay hold no formula and are not changed. Asserted in `g3_05`, $\chi_0<0$ above the continuum
  by the sum over the Fermi sphere and by $-nq^2/m\omega^2$, so $1-v\chi_0>1$ there.
- Page `05`, solution of the problem, new text of the builder. Old "Beyond this range the series does not converge ...
  It also has the pole at $U\chi_0=-1$, which no truncation has." New "For $|U\chi_0|\geq1$ the series does not
  converge ... The one exception is its pole at $U\chi_0=-1$, which no truncation has." Not in the .tex. Asserted in
  `g3_05`, the partial sums go to $1/1.9$ at $U\chi_0=0.9$.
- Page `05`, first quiz, by the rule. Old "$\chi_0(\pi,\pi)=0.68/t$". New "$\chi_0(q,0)=0.68/t$ at $q=(\pi,\pi)$", since
  on this page the two arguments of $\chi_0$ are $q$ and $\omega$. Not in the .tex.
- Page `05b`, Section 9.5b. Old "where it is already logarithmically enhanced." New "where it is already enhanced.", since
  the next sentence gives $\ln^2(1/T)$. Line 322.
- Page `05b`, try-it box. Old "which adds the interaction $U$ to a dimerized chain." New "which adds the interaction $U$
  to the chain of `geometry.bichain()`, a chain with two sites in its cell and equal hoppings, and solves it in mean
  field." Not in the .tex. Asserted in `g3_05b`, by the cell itself, at `U = 2.0` RPA raises the low-energy peak near
  $q=0$ from 0.69 to 14.9 and at `U = 0.5` only from 0.23 to 0.34.
- Page `05b`, notebook box. Old "You add a Hubbard interaction $U$ and an external staggered, antiferromagnetic field to
  a dimerized chain, and you look at what happens to the response as $U$ increases." New "You add a Hubbard interaction
  $U$ to the chain of `geometry.bichain()`, which has two sites in its cell and equal hoppings. You solve it in mean
  field from an antiferromagnetic starting guess, and you look at what happens to the response as $U$ increases." Lines
  357 and 358. Asserted in `g3_05b`.
- Page `05b`, notebook box, last sentence. Old "This is the version of equation (9.8) on the scale of a notebook, where
  the Stoner instability appears when $U$ goes above the threshold set by $\chi_0$." New "This is the version of equation
  (9.8) on the scale of a notebook. At half filling $\chi_0$ of this chain diverges at $q=\pi$ as $T\to0$, so in mean
  field it orders at any $U>0$, as the problem above finds. At small $U$ the gap is then set by the k-mesh of the cell,
  `nk = 100`, and it becomes smaller as the mesh grows." Lines 358 to 360. Asserted in `g3_05b`, the gap equation of the
  infinite chain gives the gap $16t\,e^{-2\pi t/U}$, $5.6\cdot10^{-5}t$ at $U=0.5t$, and the loop of the cell gives
  $0.0081t$, $0.0045t$ and $0.0025t$ for `nk` 100, 200 and 400, and $0.0011t$ at $U=0.1t$, so its mesh holds the Fermi
  point and shows no threshold. The bands of the cell were read on 2001 points, since the default path of
  `h.get_bands()` gives $0.016t$ to $0.018t$ at any small $U$, and the check that gave $0.018t$ at $U=0.5t$ now reads
  $0.0081t$.
- Page `06`, Section 9.6a. Old "$\delta n(x) = \int \frac{dq}{2\pi}\, e^{iqx}\, \chi_0(q)\, v_0$". New
  "$\delta n(x) = -\int \frac{dq}{2\pi}\, e^{iqx}\, \chi_0(q)\, v_0$", which agrees with (9.4) and with
  $\delta n(0)=-0.15$ and $-0.19$ of the caption of `friedel`. Line 392. Asserted in `g4_06`, the exact density of a
  ring of 400 sites against the Fourier sum, $\delta n(0)/v_0=-0.25$.
- Page `06`, the widget text. Old "This is the pattern that an STM map shows around a single impurity." New "An STM map
  at low bias around a single impurity shows the same period.", since the LDOS at the Fermi level has the period
  $\pi/k_F$ and not the envelope $1/x$ of the density, and at the bias $V$ the period is $\pi/k(E_F+eV)$. Not in the .tex.
  Asserted in `g4_06`, the period 4.89 sites by the closed form and by a sum over momenta, against $\pi/k_F=4.90$, and
  3.2 sites at the bias $0.5t$, against $\pi/k(E_F+0.5t)=3.19$.
- Page `06b`, Section 9.6b, second paragraph. Old "An impurity placed in a gapped 1D chain gives an LDOS that converges
  very quickly to its uniform value, instead of oscillating with a slow power-law envelope." New "An impurity placed in a
  gapped 1D chain changes the LDOS at the energies inside the gap, such as $E=0$ of the notebook, and there the change
  decays exponentially. In a metallic chain the LDOS at the Fermi energy instead keeps oscillating with the period
  $\pi/k_F$ far from the impurity." Lines 420 to 422. Asserted in `g4_06b`, the same amplitude at $x=10$, 40 and 160 by
  the closed form of the T-matrix of the metal at the Fermi energy, with the period 3 sites at $\mu=-t$. In the gapped
  chain of the cell, $m=0.1t$, the T-matrix gives at $E=0$ a fall from $3.7\cdot10^{-5}$ at 20 sites to
  $5.7\cdot10^{-13}$ at 200 sites, at the rate $2\,\mathrm{asinh}(m/2t)$, while at $E=0.5t$, inside its band, the
  envelope falls from 400 to 800 sites only by the factor 0.657 of the broadening.
- Page `06b`, caption of `friedel`, by the rule. Old "in a chain of 4001 sites". New "in a spinless chain of 4001 sites",
  since $-0.15$ and $-0.19$ are the values of one state per site. Not in the .tex.
- Page `06b`, notebook box. Old "Check that the LDOS now converges to its bulk value within one or two sites". New "Check
  that the change of the LDOS now decays exponentially, over about $10$ sites for the gap $0.2$ and about $3.3$ sites for
  the gap $0.6$". Lines 430 to 432. Asserted in `g4_06b`, the cell itself gives 9.96 and 3.34 sites, and
  $1/(2\,\mathrm{asinh}(m/2t))$ gives 10.00 and 3.35.
- Page `07`, Section 9.7. Old "In the approximation of a classical spin, in the Born approximation, this is the
  **Yu-Shiba-Rusinov** problem." New "In the approximation of a classical spin, this is the **Yu-Shiba-Rusinov**
  problem." Line 453. Asserted in `g5_07`, at $JS=3t$ the lattice is within $0.004\Delta$ of (9.10), while its first
  order $1-2\alpha^2$ gives $-3.5\Delta$.
- Page `08`, caption of Figure 9.4. Old "The rule is as direct as it looks. Vacancies produce in-gap modes if and only
  if the bulk invariant is non-zero". New "Vacancies produce in-gap modes when the bulk invariant is non-zero".
  `lecture_notes/src/figures/s09f04_vacancy.tex`, lines 12 and 13. The converse fails for the SSH ring, and close to the
  closing of the gap no separate mode is seen, which `g5_08` asserts.
- Page `08`, second quiz. Old right option "The bulk is trivial, or the vacancy breaks the symmetry that protects the
  invariant." with "We can conclude only one of two cases.", and old third feedback "A small gap does not prevent the
  mode. ... and a vacancy still gives a state at $-0.016t$." New right option "The bulk is trivial, the vacancy breaks the
  symmetry that protects the invariant, or the gap is too small to separate the mode from the bands.", with the feedback
  "Each of the three cases gives no separate mode ...", and new third feedback "A small gap can hide the mode, as in the
  Haldane model with $t_2=0.1t$, $\varphi=\pi/2$ and $M=0.5t$, which has $C=1$ and a gap of only $0.04t$. A vacancy there
  gives no level that is separated from the band edges. But a small gap is not the only reason. The trivial insulator
  with $t_2=0$ and the sublattice mass $M=0.78t$ has the large gap $1.56t$, and its vacancy leaves no level inside it."
  This agrees with the opener of the page and with the key box, whose SSH ring has a zero level in its trivial order.
  Not in the .tex. Asserted in `g5_08` on k-meshes of 600 and 1200, and for $M=0.78t$ on the torus of $18\times18$ cells
  and by $G_{AA}$ of the infinite lattice, which keeps its sign over the gap.
- Page `08`, second quiz, first feedback, the sentence added by the fixer. New "This holds for the neighbor joined to the
  vacancy by the strong bond $t$, since on the other neighbor the level at zero stays." Not in the .tex. Asserted in
  `g5_08`.
- Page `08`, box "Where this comes back", second bullet. Old "a network must find a non-local quantity, since there the
  phases have no local order parameter". New "a network must find a quantity of four spins, the plaquette product, since
  there the two regimes have no local order parameter", since in Section 10.6b the Boltzmann weight depends only on the
  plaquette products, and its two regimes are separated by a crossover. Not in the .tex.
- Page `index` of Session 9, box "Where this comes back". Old "a phase with no local order parameter must be found from
  a non-local quantity". New "a regime with no local order parameter must be found from a quantity of four spins, the
  plaquette product", for the same reason. Not in the .tex.
- Page `09`, try-it box. Old "Run the cell, which compares a gap of `0.1` with a gap of `0.3`. The LDOS reaches its bulk
  value after about 25 sites for the smaller gap and after about 10 sites for the larger one." New "Run the cell, which
  compares the gaps $0.2$ and $0.6$, since `gaps = [0.1,0.3]` are the onsite energies $\pm m$ and the gap is $2m$. The
  change of the LDOS decays as $e^{-x/\xi}$, with $\xi\approx10$ sites for the smaller gap and $\xi\approx3.3$ sites for
  the larger one." Not in the .tex. Asserted in `g5_09` and `g4_06b`.
- Page `09`, notebook box. Old "This is not a spin model, but it is the closest exercise in its logic. It compares how a
  dimerized chain, with a stronger or a weaker gap, responds to a strong local impurity. Run it with (9.11) in mind ...".
  New "This is not a spin model. The cell puts one impurity of growing strength into three gapped chains built on
  `geometry.bichain()`, which has two sites in its cell and equal hoppings. These are an s-wave superconductor, an
  insulator with a sublattice imbalance and a topological p-wave superconductor. The cell plots the density of
  states summed over four sites, the impurity site and the next three sites of the chain. Look at which of the three
  gaps get a state inside them as the impurity grows, which is the question of Section 9.8 for one strong impurity. The
  decay length of this page, which is shorter for the larger gap, is in the cell "Impurity in an electronic insulator"
  that the box above runs." Lines 591 to 593. Read from the cell in `g5_09`, and asserted there with pyqula, since
  `Embedding.multidos` sums the LDOS over the four sites of `get_supercell(2)`, with the impurity on the site at its end.
- Page `09`, solution of the problem, new text of the builder. Old "where the exponential tends to a straight line of
  slope $-1/\xi$". New "where the exponential of this problem is a straight line of slope $-1/\xi$". Not in the .tex.
- Page `10`, Section 9.10a, the list of the three regimes. Old "Critical means localized with a power law, so that the
  state is not even normalizable in the strict sense." New "Critical means neither extended nor localized, with an IPR
  that falls as a power of $N$ slower than $1/N$.", as the caption of Figure 9.6 and the key box say. Lines 612 and 613.
  Asserted in `g6_10`, $\tau=0.53$ for the mean over the states at $V_0=2t$, 0.98 at $t$ and 0.00 at $3t$.
- Page `10`, last line before the box "Where this comes back". Old "The second regime, with random disorder". New "The
  third regime, with random disorder", the third of the numbered list. Not in the .tex.
- Page `10`, solution of the problem, by the rule. Old "while a fit of its tail gives $\xi$ between $2.1$ and $2.4$
  sites." New "while fits of its tail that reach $30$ to $60$ sites from the center give $\xi$ between $2.1$ and $2.4$
  sites.", the windows of the assert in `g6_10`. Not in the .tex.
- Page `10`, caption of `aah_ipr`, changed by the builder. Old "Below $V_0=2t$ the three curves are apart, and
  $N\cdot\mathrm{IPR}\approx2$ for all of them". New "Below $V_0=2t$ the three curves are apart, and at $V_0=t$ the
  product $N\cdot\mathrm{IPR}$ is about $2$ for all of them". Not in the .tex.
- Page `10b`, Section 9.10b, the quiz on halving $W$. Old "By which factor does the localization length $\xi$ change?"
  New "By which factor does the localization length $\xi$ close to the band center change?", the condition of the key
  box. Not in the .tex. Asserted in `g6_10b`, at the band edge halving $W$ multiplies $\xi$ by 1.59.
- Page `10b`, the quiz on the Anderson insulator, first feedback, changed by the builder. Old "about $1/W=0.05/t$". New
  "about $1/(2W)=0.025/t$", with the sentence "Eight cubes of $10^3$ sites give between about $0.022/t$ and $0.027/t$ in
  the window $|E|<5t$." in place of "between $0.023/t$ and $0.027/t$", a range that depends on the seeds. Not in the
  .tex. Asserted in `g6_10b` with bounds on the eight cubes, which give 0.0229 to 0.0270, and 24 other cubes gave 0.0222
  to 0.0265.
- Page `10b`, the same quiz, second and third feedback, by the rule. Old "falls as $e^{-L/\xi}$, where $\xi$ is the decay
  length of $|\psi|^2$. With the decay length of the amplitude, $|\psi|\sim e^{-x/\xi}$, it falls as $e^{-2L/\xi}$." and
  "decays as $e^{-L/\xi}$, with $\xi$ the decay length of $|\psi|^2$". New "falls as $e^{-2L/\xi}$, with $\xi$ the decay
  length of the amplitude, $|\psi|\sim e^{-x/\xi}$." and "decays as $e^{-2L/\xi}$, with $\xi$ the decay length of the
  amplitude", the $\xi$ of the rest of the page. Not in the .tex. Asserted in `g6_10b` in one dimension only, a slope of
  $\langle\ln T\rangle$ equal to $2/\xi$ within 10 percent at $W=t$.
- Page `10b`, caption of `localization_length`, by the rule. Old "The localization length $\xi$ of the random chain".
  New "The localization length $\xi$ of the amplitude, $|\psi|\sim e^{-x/\xi}$, of the random chain". Not in the .tex.
- Page `10b`, figure and caption of `mobility`, redrawn under the same name. The old guide $6\sqrt{1-(W/W_c)^2}$ stood at
  $4.7t$ for $W=5t$, where the level statistics of cubes of $10^3$ and $12^3$ sites are those of extended states up to
  $E=7t$. The new guide is $(6+0.8W)\sqrt{1-(W/W_c)^2}$, inside the band edges, with $E_c=8.0t$ at $W=5t$. The old SVG
  is kept in the scratch folder of this pass. Old "The blue curve is a guide for the eye, and only its end point,
  $W_c\approx8t$, is taken from numerical work. States inside the curve are extended and all others are localized". New
  "The blue curve is a guide for the eye. Its end point, $W_c\approx8t$, is taken from numerical work. At $W=5t$ it lies
  above $E=7t$, since our level statistics of cubes of $10^3$ and $12^3$ sites there are those of extended states
  up to $E=7t$. Roughly, states inside the curve are extended and all others are localized". Not in the .tex. Asserted
  in `g6_10b`, the ratio of neighboring spacings 0.52 to 0.55 for $5t<|E|<7t$, and in `mobility.py`. The window from
  $7t$ to $8t$ gives 0.51 to 0.53 with about 200 levels, close to the edge, and it is not asserted. At $W=6t$ the guide
  stands at $7.4t$, while the same statistics find extended states between $7t$ and $8t$, which "Roughly" covers.
- Page `10b`, notebook box, by the rule. Old "and separately the strength $W$ of the random disorder". New "and
  separately the strength of the random disorder", followed by the new sentence "The random potential of the cells has
  the full width `v` or `w`, which is $2W$ of this page." Lines 674 and 675. Read from the cells in `g6_10b`.
- Page `11`, Section 9.11, the bullet on the vacancy, by the rule. Old "gives an in-gap mode only because of the
  bulk-boundary correspondence." New "gives an in-gap mode because of the bulk-boundary correspondence.", which is what
  Section 9.8 says. Lines 711 and 712.
- Page `11`, the list of tasks. Old "Use a vacancy to test a gapped phase for topology, when the vacancy keeps the
  symmetry that protects the invariant." New "Use a vacancy to test a gapped phase for topology, and say when the test
  fails.", since an SSH ring keeps its chiral symmetry and has the zero level in both phases. Not in the .tex.
- Page `04`, Section 9.4a, the sentence before (9.4), picked by the lecturer on 2026-11-22. Old "where each term comes
  from a matrix element $\langle k+q|V|k\rangle$ divided by the energy denominator $\varepsilon(k+q)-\varepsilon(k)$,
  with the same structure as (9.3)". New "... divided by the energy denominator $\varepsilon(k)-\varepsilon(k+q)$, with the
  same structure as (9.3)", the denominator of the mixing (9.3) and of the steps fold, $a=v_q/(\varepsilon(k)-
  \varepsilon(k+q))$. Lines 177 to 179. Asserted in `g2_04`, on the exact eigenvectors of a ring of 16 sites.
- Page `04`, Section 9.4a, after the key box, a new paragraph, picked by the lecturer on 2026-11-22. "The density then
  changes by $\delta n(q)=-\chi_0(q)\,v_q$, with $v_q=\langle k+q|V|k\rangle$ the matrix element of the potential. With
  the density as the observable $A$, this is the response $\chi_A=\partial A/\partial\lambda$ of Section 9.3, so
  $\chi_A=-\chi_0(q)\,v_q$, and $\chi_0$ is the response to the local chemical potential $-v_q$. The minus sign comes
  from the denominator $\varepsilon(k)-\varepsilon(k+q)$ of the mixing (9.3), which is minus the one of (9.4), and it
  means that a higher onsite energy pushes the electrons away. Like (9.4), this counts one spin. For spinful electrons
  each spin responds in the same way, and the total density changes by $-2\chi_0(q)\,v_q$." The last two sentences
  were added after the independent check of 2026-11-22, so that page `04` agrees with "Here $\chi_0$ counts one spin" of
  page `05`, and they are not in the wording of the pick. In the .tex after (9.4), whose `\end{equation}` is line
  184. (9.4) does not change.
  Asserted in `g2_04` by three routes, the exact density of a ring of 400 sites at $\mu=-t$ and $T=0.05t$, where
  $\delta n_q/v_q$ is $-0.18636$, $-0.2609$ and $-0.25894$ against $\chi_0=0.18636$, 0.2609 and 0.25894 of (9.4), and on
  a ring of 16 sites with a flux, where (9.3) taken state by state and the exact density both give $-0.222376$, minus
  the $\chi_0$ of (9.4) on the same momenta. The ring of 400 sites with the two spins gives $-0.37271$, $-0.52179$ and
  $-0.51787$ for the total density, which is $-2\chi_0$.
- Page `05`, Section 9.5a, after the key box of (9.6), two new sentences, picked by the lecturer on 2026-11-22. "Here
  $\chi_0$ counts one spin. For an interaction that couples to the total density, the denominator is
  $1+2v(q)\chi_0$." In the .tex after (9.6), line 272. (9.6) does not change. Asserted in `g3_05` with a self-consistent
  Hartree loop on a spinful ring of 200 sites at $\mu=-t$ and $T=0.1t$: a pair interaction $0.4e^{-|r|}$ on the total
  density gives the response $-2\chi_0/(1+2v_q\chi_0)$ at three $q$, and not $-2\chi_0/(1+v_q\chi_0)$, and the Hubbard
  $U=t$, which couples only opposite spins, gives $-2\chi_0/(1+U\chi_0)$.
- Page `05`, Section 9.5a, the paragraph on the RPA denominator, by the same pick. Old "For a long-range Coulomb
  interaction, $U \to v(q)$". New "For a long-range Coulomb interaction, $U \to 2v(q)$", which agrees with the new
  sentences. Line 286. Asserted in `g3_05`, the zero of $1+2v(q)\chi_0$ with the $\chi_0$ of one spin of the 3D gas is
  at $\omega_p$ for $q=0.02k_F$ and $0.04k_F$, while the zero of $1+v(q)\chi_0$ is at $\omega_p/\sqrt2$.
- Page `05`, Section 9.5a, the first paragraph on the RPA, by the same pick. Old "Let us take a contact interaction of
  the Hubbard type of (1.7), with strength $U$, which couples to the density." New "..., which couples the densities of
  the two spins.", since the new sentences give $1+2v(q)\chi_0$ for an interaction on the total density and the Hubbard
  term $Un_\uparrow n_\downarrow$ couples opposite spins only, which gives $1+U\chi_0$. Line 258, where the .tex has
  "a contact interaction, of Hubbard type, with strength $U$, which couples to the density". Asserted in `g3_05` by the
  same Hartree loop.
- Page `05`, a new steps fold after the key box of (9.7), "From a zero of the denominator to the plasma frequency", the
  fold that the block of 9.5a planned for the time after the two picks. It expands (9.5) at $\hbar\omega$ far above the
  pair energies, where the first term vanishes and the shift $k\to k-q$ gives the bracket
  $\varepsilon(k+q)+\varepsilon(k-q)-2\varepsilon(k)=\hbar^2q^2/m$ of free electrons, so
  $\chi_0\approx-n_\sigma q^2/(m\omega^2)$ with $n_\sigma=n/2$ per unit volume, and the zero of $1+2v(q)\chi_0$ is at
  $\omega_p^2=4\pi ne^2/m$, in Gaussian units, while $1+v(q)\chi_0$ would give $\omega_p/\sqrt2$. Not in the .tex.
  Asserted in `g3_05`: the first term and the shift on a chain, the second term against (9.5) at $\omega=9t$ within
  $10^{-3}$, the bracket for random $\mathbf k$, the $\chi_0$ of one spin of the 3D gas at $q=0.1k_F$ and
  $\omega=1.2\hbar k_F^2/m$ against $-n_\sigma q^2/(m\omega^2)$ within two percent, and the two zeros.

### Decided on 2026-11-22

One bullet per point that was a choice, with the choice. The coordinator decided all of them with the rule above,
except the last two, which the lecturer picked on 2026-11-22.

- The first quiz of page `05`, $\chi_0(\pi,\pi)$ with two arguments that read as $(q,\omega)$. Written as
  $\chi_0(q,0)$ at $q=(\pi,\pi)$, the clearer of two true wordings.
- The caption of `friedel`, which did not say spinless. "spinless" is added, the smallest change.
- The conductance of the quiz on the Anderson insulator, written with the $\xi$ of $|\psi|^2$ a few lines from the
  $\xi$ of the amplitude of the rest of the page. Both feedbacks now use the $\xi$ of the amplitude, and the caption of
  `localization_length` names it. The factor 2 of $e^{-2L/\xi}$ is checked in one dimension only, for a quiz on $d=3$.
- The fit of the tail in the solution of page `10`, whose range depended on a window that the page did not name. The
  windows of the assert, which reach 30 to 60 sites, are named, and no new number is added.
- The pyqula sentence of the caption of `lindhard_map`. The clause "which needs the pyqula of GitHub" is dropped, which
  is shorter than a version number that no offline check can assert. `webnotes/scripts/RECIPES.md` and line 216 of
  `lecture_notes/WEB_NOTES_PLAN.md` say the same about PyPI and are not files of this session, so they are not changed.
- The width of the random potential, item 7 of the former list. The notebook box of page `10b` now says that `v` and
  `w` of the cells are $2W$. The try-it box quotes only `v` and no $W$, so it is not changed.
- The bullet of page `11` that says "only because of the bulk-boundary correspondence". "only" is dropped, which reduces
  the claim to what Section 9.8 says.
- The figure `mobility`, whose guide put extended states outside the curve. It is redrawn under its name with a guide
  that contains the extended states that the level statistics find, and the caption says so.
- The assert of the condition of the first key box of page `04b`, which tested the axis and the diagonal and not the
  maximum of $\chi_0$ at $\mu=-t$. `g2_04b` now finds the maximum on the zone boundary near $(\pi,1.83)$ and asserts
  that its steps shrink, 0.011, 0.0067 and 0.0039, over three halvings of $T$. The page is not changed.
- "exactly at the gap edges" and "exactly solvable" in the caption of Figure 9.3. They state physics, so they stay, and
  the lint gives them as warnings and not as hits.
- "a vacancy is guaranteed to host an in-gap bound state" in Section 9.8. Close to the closing of the gap the state is
  still in the gap, exponentially close to its edge, and the opener of the page says that no separate peak is seen
  then. No change.
- $\xi=2.5$ of Figure 9.5, which is not the value of the spin-1 chain. The caption says "drawn for $\xi=2.5$" and claims
  no material, and the lab box gives the measured $\xi=8(1)$. No change.
- The steps fold of the plasma frequency planned for page `05`. It was not written, since it needed the factor 2 of the
  spins for $v(q)$, then the second point of "For the lecturer". It is written since the pick of that point, and it is
  the last entry of the first list.
- The conventions sheet. Its lines on `h.get_dos`, on the mesh of `lindhard_map`, on `vacancy_dos`, on the floor of
  `spinon_impurity` and on the SVG of that script are corrected, the crossing $JS=2.01t$ of `g5_ysr_dos` is added, and
  its last section now gives the points of the old text with what happened to them. Its line on the density of states of
  the 3D Anderson model now uses the eight cubes and the window $|E|<5t$ of the quiz of page `10b`, in place of four
  other cubes and $|E|<2t$, and its last section has the rule of page `08` as a point of the lecturer.
  `conventions.py` checks each line.
- The notebook box of page `09`, whose cell "The impact of a strong impurity" asks the question of Section 9.8 and has no
  decay length. The box stays on page `09`, where the .tex has it, and one sentence points to the cell "Impurity in an
  electronic insulator" of the try-it box for the decay length of the page. Moving it to the list of page `08` would
  change the blocks of two pages.
- The stored source of the lab box of page `06`. `webnotes/sources/session09/sotthewes2021_physrevb.103.245311.txt`
  holds only the two clauses with a number, as `labsource.py` writes the tracked copy of a text of a journal. The three
  sentences of the box without a number are in the abstract of the full copy,
  `webnotes/sources/.full/session09/sotthewes2021_physrevb.103.245311.txt`, which git ignores, so the box is not changed
  and the tracked file is not written by hand.

- The definition of the response of Section 9.3 against (9.4), the former point 1 for the lecturer. Picked by the
  lecturer on 2026-11-22: keep (9.4) and add in Section 9.4a, after the key box, "The density then changes by
  $\delta n(q)=-\chi_0(q)\,v_q$", in the form that fits the definition $\chi_A=\partial A/\partial\lambda$ of Section 9.3.
  The sentence before (9.4) gets the denominator $\varepsilon(k)-\varepsilon(k+q)$ of (9.3), as the point said for each
  of its candidates. The changes are two entries of the first list, asserted in `g2_04`.
- The factor 2 of the spins in (9.6), the former point 2 for the lecturer. Picked by the lecturer on 2026-11-22: keep
  (9.6) and add after it "Here $\chi_0$ counts one spin. For an interaction that couples to the total density, the
  denominator is $1+2v(q)\chi_0$." The sentences of page `05` that wrote the Coulomb denominator without the factor 2, $U
  \to v(q)$ and the caption of Figure 9.2, and the sentence that said that the Hubbard $U$ couples to the density, now
  agree with it, and the steps fold of the plasma frequency is written. These are four new entries at the end of the
  first list, and the entry of the caption of Figure 9.2 is updated, all asserted in `g3_05`. Four of these changes go
  beyond the wording of the pick. The caption, the Hubbard sentence and $U\to2v(q)$ were changed so that they do not
  contradict the picked sentences. The fold is new text with no counterpart in the .tex, which the block of 9.5a planned for the time after
  the pick, so the lecturer can keep it or drop it.

### For the lecturer

These two points would change a numbered equation, a convention or a rule that the .tex states, so the rule leaves them
to the lecturer. Each one comes with candidate texts, and the pages keep their present wording until the pick. The
lecturer picked the two first points of the former list on 2026-11-22, and they are the last two points of the list
above.

1. The quantity of (9.11). (9.11) is written for the correlation $\langle S_0\cdot S_n\rangle$, while the text of
   Section 9.9, its steps fold and the figure `spinon_impurity` follow the moment $\langle S^z_n\rangle$ that a field on
   site 0 induces, and the bullet of Section 9.11 calls (9.11) "the induced spin correlation". In the spinon mean field
   the two do not decay in the same way. The induced moment goes as $(-1)^n/n$, as `g5_09` asserts, while at half
   filling $\langle S^z_0S^z_n\rangle=-\sin^2(\pi n/2)/(2\pi^2n^2)$, $0.0507/n^2$ for odd $n$, as the former version of
   this list checked. The $1/n$ of $\langle S_0\cdot S_n\rangle$ for the true $S=1/2$ chain, up to a logarithm, is a
   result of numerical work that is not checked here. The candidates are these.
   - Change the left side of (9.11) to the induced moment $\langle S^z_n\rangle$, which the text, the fold and the
     figure compute, and write "the induced moment" in Sections 9.9 and 9.11.
   - Keep (9.11) for $\langle S_0\cdot S_n\rangle$ of the true chains, and add after it "The spinon mean field of the
     steps fold gives this law for the moment induced by a field, and not for the correlation, which it gives as
     $1/n^2$." The figure and the fold stay.
   - Keep (9.11) and write in Sections 9.9 and 9.11 "the impurity response" in place of "the induced spin correlation",
     with no claim on which of the two quantities the spinon mean field gives.
2. The italic rule of the key box of Section 9.8, lines 510 to 512 of the .tex, "If vacancies produce in-gap modes, the
   underlying phase is topological, and if they do not, the phase is trivial". The box adds the symmetry sentence and
   the SSH ring, where a vacancy leaves a zero level in both orders of the hoppings, as `g5_08` asserts on a ring of 80
   sites, so an in-gap mode does not always mean a topological phase. Close to the closing of the gap the second half
   fails too. For $t_2=0.1t$, $\varphi=\pi/2$ and $M=0.5t$ the Haldane model has $C=1$ and the gap $0.039t$, and
   $G_{AA}$ and $G_{BB}$ of the infinite lattice have no zero in the gap away from its edges, on meshes of 600 and 1200.
   The opener and the second quiz of the page give this case, and the box does not. A clause of the gap was added to the
   box on 2026-11-22 and taken back, since it changes the rule of the .tex. The candidates are these.
   - Write the rule as a condition, "When the vacancy keeps the symmetry that protects the invariant and the gap is not
     close to closing, an in-gap mode means a topological phase, and no mode means a trivial phase." The SSH sentence
     stays as the case of a chiral chain, where the vacancy changes the count of the two sublattices.
   - Keep the italic rule, and add to the box "and close to the closing of the gap the mode can sit too close to a band
     edge to be seen" after the symmetry sentence.
   - Keep the box as it is, with the case of the gap in the opener and in the second quiz only.
