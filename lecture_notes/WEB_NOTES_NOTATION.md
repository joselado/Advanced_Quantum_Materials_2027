# Notation of the web notes

This file records the conventions as they are used in `webnotes/pages/`, checked by a grep of the Markdown
on 2026-11-07, and the bridging sentences that the text agents add where two sessions write the same thing
in two ways. The rule of the lecturer is to keep the source as it is and to add one sentence with a link. An
equation is never changed, and a bridging sentence goes in the prose next to the equation. Each sentence below
is ready to paste, and the agent of that session adapts the first words to the paragraph it goes into.

## Conventions as used

### The sign of the hopping

Every tight-binding Hamiltonian of the notes is written with a minus sign and $t>0$, as $H=-t\sum_n(c_n^\dagger
c_{n+1}+\text{h.c.})$. This is the form of equations (1.6), (1.7), (2.5), (5.2), (5.4), (5.19), (6.1), (8.17)
and (8.18), and Session 2 says it in words below (2.5), "We take $t>0$ in all of this session, the same sign
convention as in (1.6)". With this sign the band of the chain is $-2t\cos\varphi$, with its minimum at
$\varphi=0$, and the kagome flat band of Section 2.11b is at the top, at $\epsilon=2t$.

There are two places where the sign is the other one. The first is the graphene Bloch Hamiltonian (2.19),
where $f(\mathbf{k})=t\sum_j e^{i\mathbf{k}\cdot\boldsymbol{\delta}_j}$ has a plus sign. The bands are
$\pm|f(\mathbf{k})|$, so the sign of $f$ does not change any energy, and the Dirac cone (2.20) is the same. No
other session writes $f(\mathbf{k})$ for graphene, so this is a clash only inside Session 2. The second is the
notebook, where pyqula uses the opposite sign of the hopping, and the try-it box of
`session02/11b-flat-bands-from-the-geometry-of-the-lattice.md` already says that the kagome flat band is at the
bottom in the notebook.

### Units

The energies of the models are in units of the hopping $t$, and the numerics and most figures take $t=1$, so a
value such as $U=3$ in a try-it box means $U=3t$. In the SSH chain the unit is the strong hopping, and in the
Haldane model it is the first-neighbor hopping, with $t_2=0.1$ in units of it. Numbers that come from
experiment are in meV (the Landau level spacings of Session 4, the gaps in the quizzes of Session 3), and
eV does not appear as a unit. The constant $\hbar$ is written in the equations, in (2.10), (2.17), (2.18),
(2.20), (2.21), (4.6) to (4.8) and (9.5), and the figures and the numerics take $\hbar=a=1$, as the caption of
the chain velocity in Section 2.9 says. With $a=1$ the phase $\varphi$ of Session 2 is the quasi-momentum $k$,
by (2.10), and from Session 3 on the notes write $k$.

### The density of states

Session 2 writes the density of states as $g(\omega)$ in (2.16). Session 6 and Session 9 write its value at the
Fermi level as $D(E_F)$, in (6.3) and below (9.8), where $\chi_0(0,0)=D(E_F)$.

### The Stoner criterion

Session 6 derives it from the self-consistent magnetization as $U\,D(E_F)\geq 1$, equation (6.3), which is the
threshold of a ferromagnet. Session 9 derives it from the divergence of the RPA spin response as
$U\,\chi_0(q,0)=1$, equation (9.8), which at $q=0$ gives $U\,D(E_F)=1$, and at finite $q$ gives an instability
with a modulated magnetization, which is the case of nesting.

### The Chern number and the filling factor

The Chern number $C$ is an integer of the occupied bands, defined in (3.4) and again in (4.1), with
$\sigma_{xy}=C\,e^2/h$. Session 4 adds the filling factor $\nu$, the number of electrons per flux quantum,
which appears first as $\nu=1$ in Section 4.14 and as $\nu=1/m$ in (4.13). With $N$ filled Landau levels
(4.2) gives $C_\text{tot}=N$, so at integer filling $\nu=C$. On a fractional plateau $\sigma_{xy}=\nu\,e^2/h$
still holds, but $\nu$ is not the Chern number of filled single-particle bands. Session 6 uses $C$ for the
Chern number of a magnon band, (6.10), with the same integral.

### The mass of a Dirac cone and the staggered potential

Session 3 writes the Dirac mass as $m$ in (3.7) and the staggered sublattice potential of the Haldane model as
$M$ in Section 3.10b, and Session 9 also writes $M$. Two places in Session 3 write the staggered potential with
a lowercase $m$, the caption of Figure 3.5 in Section 3.10b ("with $m=0.5$ and $t_2=0.1$") and the quiz on
the two masses in the closing summary of Session 3. Changing them is a change of math, so it is left to the
lecturer, and the bridging sentence below makes the two symbols explicit. The letter $m$ is also the odd
exponent of the Laughlin state (4.13) and the angular momentum of Section 4.15, which is clear from the
context and needs no bridge.

### The second-neighbor coupling of the Haldane model

Session 3 writes it as $t_2$ and does not give its phase a symbol, Session 9 writes $t_2=0.1t$, $\varphi=\pi/2$ and
$M=0.5t$, and Session 6 maps the Dzyaloshinskii-Moriya term of a honeycomb magnet onto it with $t_2=DS$.
The Haldane mass is $3\sqrt3\,t_2$ at each valley, so the gap is $6\sqrt3\,t_2$, which is the value that
Session 6 gives.

### The sign of the exchange

The Heisenberg model (6.5) is $\sum J_{ij}\,\mathbf S_i\cdot\mathbf S_j$, with $J>0$ antiferromagnetic and
$J<0$ ferromagnetic, and Session 7 writes the same sum with no sign of its own. Session 8 uses the same sign,
since it writes the ferromagnetic dimer with $J<0$. The Ising model (10.9) of Session 10 is written as $-J\sum\sigma_i\sigma_j$, so there $J>0$ is
ferromagnetic.

### The sign of the interaction

The Hubbard term is $+U\,n_\uparrow n_\downarrow$ in (1.7), with $U>0$ repulsive in Session 1, Session 6 and
Session 9. Session 5 keeps the same form in (5.2) with $U=-|U|<0$, and says so in the text.

## Bridging sentences to add

Each item gives the page, the place in it and the sentence. The links use the reference formats of the last
section, and "Session N" is linked by the build.

- Session 2, `session02/11-the-dirac-cone-of-the-honeycomb-lattice-of-graphene-and-flat-band-lattices.md`, after
  (2.19), where $\boldsymbol\delta_j$ is explained.

  ```
  With the sign of [(2.5)](#eq-2-5) the off-diagonal element would be $-t\sum_j e^{i\mathbf{k}\cdot\boldsymbol{\delta}_j}$, and we write it with $+t$ since the overall sign of $f(\mathbf{k})$ drops out of the bands $\pm|f(\mathbf{k})|$.
  ```

- Session 6, `session06/06-the-stoner-threshold-as-a-criterion-for-magnetism.md`, after (6.3).

  ```
  Here $D(E_F)$ is the density of states $g(\omega)$ of [(2.16)](#eq-2-16) at $\omega=E_F$. In Session 9 the same criterion comes back as the divergence of the spin response, $U\chi_0(q,0)=1$ in [(9.8)](#eq-9-8), which at $q=0$ is the condition that we have here.
  ```

- Session 9, `session09/05b-the-stoner-instability.md`, the sentence after (9.8) that reads "becomes
  $U\,D(E_F) = 1$. This is exactly the Stoner criterion". The bridge is a link and a clause added to that
  sentence, not a new sentence.

  ```
  In Session 6 we wrote the same criterion as $U\,D(E_F)\geq1$ in [(6.3)](#eq-6-3), where we found it from the self-consistent magnetization.
  ```

- Session 4, `session04/13-the-symmetric-gauge-and-the-lowest-landau-level-wavefunctions.md`, after the
  sentence that ends "the integer quantum Hall state at filling $\nu=1$".

  ```
  The filling factor $\nu$ is the number of electrons per flux quantum, and with $N$ filled Landau levels it equals the total Chern number $C_\text{tot}=N$ of [(4.2)](#eq-4-2), so that $\sigma_{xy}=\nu\,e^2/h$. In Section [4.16](#sec-4-16) the same relation holds at fractional $\nu$, where $\nu$ is no longer a Chern number of filled bands.
  ```

- Session 3, `session03/10b-the-haldane-coupling-and-a-real-chern-insulator.md`, where the staggered potential
  $M$ is first written.

  ```
  The staggered potential $M$ gives the mass $m$ of [(3.7)](#eq-3-7) with the same sign at both valleys, while the Haldane coupling gives masses of opposite sign at $K$ and $K'$, and only the second one gives $C=\pm1$.
  ```

- Session 6, `session06/16-topological-magnons.md`, at "This is the Haldane model, up to a constant". The bridge
  is a link added to that sentence.

  ```
  This is the Haldane model of Section [3.10b](#sec-3-10b), up to a constant, with $t_2=DS$.
  ```

- Session 10, `session10/06-phase-classification-with-local-order-parameters-and-topological-order.md`, after
  (10.9).

  ```
  Note the sign, since here $J>0$ favors parallel spins, while in the Heisenberg model [(6.5)](#eq-6-5) of Session 6 a positive $J$ is antiferromagnetic.
  ```

- Session 9, `session09/08-impurities-as-diagnostics-iii-vacancies-in-topological-matter.md`, where the Haldane
  model is first named, a link and nothing else.

  ```
  the Haldane model of Section [3.10b](#sec-3-10b)
  ```

- Session 3, the first page that writes the quasi-momentum as $k$ for a chain, optional, a link to the
  definition.

  ```
  With the lattice constant $a=1$ the phase $\varphi$ of Session 2 is the quasi-momentum $k$, by [(2.10)](#eq-2-10).
  ```

## Reference formats

A reference is a Markdown link to an anchor, and the build points it to the page that holds the anchor, also in
another session. The text agents write the three forms below and no other.

- A section, `Section [N.M](#sec-N-M)`, for example `Section [6.6](#sec-6-6)` or `Section [2.11b](#sec-2-11b)`.
  The word is capitalised, also in the middle of a sentence.
- An equation, `equation [(N.M)](#eq-N-M)` in the middle of a sentence and `Equation [(N.M)](#eq-N-M)` at its
  start, or the bare link `[(N.M)](#eq-N-M)` when the sentence already says what it is. The forms "eq. [",
  "Eq. [" and a link without the parentheses are replaced.
- A session, the plain text `Session N`, capitalised and not linked by hand, since the build links it to the
  index page of that session. "session N" in lowercase is not linked, and the lint reports it.
- A figure, `Figure [N.M](#fig:sNN:name)`, and a schematic, the empty link `[](#sch:sNN:name)`, which the build
  writes as "Schematic N.M".

`python3 webnotes/lint.py --session N` lists the lowercase "session N" (category `session-case`) and the forms
"eq. [" and "section [" (category `ref-format`). Most of them are in Session 5, written as `eq. [1.7](#eq-1-7)` or
`section [5.9](#sec-5-9)`, with a working link but the wrong form, so only the words and the parentheses change.
