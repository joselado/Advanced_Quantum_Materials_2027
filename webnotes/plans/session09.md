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
since `style.save` rewrites the SVG, and `spinon_impurity.py` does not give the same SVG twice.

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
  fold depends on item 1 of "Open for the lecturer", so it is written after the pick.
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

These change a numbered equation, a statement of the old text, a caption that states it, or a convention, so a
builder does not decide them. The numbers come from the scratch scripts `plan_numbers.py` and `sign_checks.py`
named at the top of this plan.

1. The sign of the plasmon denominator. The caption of Figure 9.2 says that the plasmon "is a zero of the RPA
   *denominator* $1-v(q)\chi_0$", while (9.6) has $1+U\chi_0$. With $\chi_0$ of (9.5), at $\omega\gg v_Fq$ we get
   $\chi_0\approx-nq^2/(m\omega^2)$, which is negative. On the half-filled chain at $q=0.3$ and $\omega=6t$, (9.5)
   gives $-0.00160$ and the expansion $-0.00158$. So with the signs of the page the plasmon is a zero of
   $1+v(q)\chi_0$, and the minus of the caption belongs to the other sign of $\chi_0$.
2. The sign of the induced density in 9.6a. The page writes $\delta n(x)=\int\frac{dq}{2\pi}e^{iqx}\chi_0(q)v_0$,
   with $\chi_0>0$ from (9.4). A repulsive impurity lowers the density on its site. On a chain at $\mu=-t$ with
   $v_0=0.1t$ we get $\delta n(0)=-0.024$. So in the convention of (9.4) the relation is
   $\delta n(q)=-\chi_0(q)v_0$. The period and the envelope of (9.9) do not change.
3. "In the approximation of a classical spin, in the Born approximation" in 9.7. (9.10) is the exact energy of
   the bound state of a classical spin, from the scattering to all orders in $J$. Expanded in $\alpha$, (9.10)
   gives $E_b=\Delta(1-2\alpha^2+\dots)$, so at first order in $J$, the Born approximation, there is no state
   below the gap edge.
4. "If and only if" in 9.8 and in the caption of Figure 9.4. The converse fails when the vacancy leaves a
   lattice with chiral symmetry and one more site on one sublattice. An SSH ring of 200 sites with one site
   removed has a state at $E=0$ in the trivial phase (hoppings $1$ inside the cell, $0.5$ between) and in the
   topological phase, and the next state is at $0.50$ in both. The second quiz of 9.8 uses the topological SSH
   chain with a vacancy as its example. The honeycomb models of the page are not affected, since $M$ and $t_2$
   both break the chiral symmetry.
5. "Local density of states" in 9.6b. The text says that the LDOS oscillates with $\pi/k_F$ and contrasts the
   insulator with "a slow power-law envelope", next to a figure of the density with a $1/x$ envelope. In a
   chain the LDOS at one energy does not fall as $1/x$. At $\mu=-t$, $v_0=t$ and a broadening $0.01t$, its change
   is $0.082$, $0.058$ and $0.014$ near $x=10$, $40$ and $160$, a decay set by the broadening, while the density
   falls as $1/x$, with $0.0062$, $0.0017$ and $0.00043$. The period $\pi/k_F$ is the same for both.
6. The quantity of (9.11). (9.11) is written for the correlation $\langle S_0\cdot S_n\rangle$, while the text
   and `spinon_impurity` follow the moment $\langle S^z_n\rangle$ induced by a field on site 0. In the spinon
   mean field they do not decay in the same way. At half filling $\langle S^z_0S^z_n\rangle=-\sin^2(\pi n/2)/(2\pi^2n^2)$,
   which I checked to $0.0507/n^2$ for odd $n$, while the induced moment goes as $(-1)^n/n$. The $1/n$ of
   $\langle S_0\cdot S_n\rangle$ for the true $S=1/2$ chain is a known result up to a logarithm, which I did not
   check with a number.
7. The width of the random potential. The page takes $w_n$ uniform in $[-W,W]$, and `mobility` uses
   $W_c\approx8t$ for it. The notebook cells "Localization due to random disorder" and "The impact of disorder in
   different systems" use `v*(random-0.5)`, a box of width $v$, so the `v` of a try-it box is $2W$ of the page.
   A sentence in the try-it box of 9.10b would say so.
