## The interacting Hamiltonian and the origin of attractive interactions {#sec-5-4 number="5.4"}

As in session 1, we start from the general interacting Hamiltonian $H = \sum_{ij}t_{ij}c_i^\dagger
c_j + \sum_{ijkl}V_{ijkl}c_i^\dagger c_j^\dagger c_k c_l$. The interaction $V_{ijkl}$ can come from the plain electrostatic Coulomb repulsion, which is repulsive, but it can also be an *effective* interaction mediated by another quasiparticle in the material. Examples are phonons, which are lattice vibrations, magnons, which are fluctuations of a magnetic moment, plasmons, which are collective charge fluctuations, and even more exotic mediators such as skyrmion fluctuations or valence fluctuations. For superconductivity, what matters is not the microscopic origin of $V_{ijkl}$ but its net sign in the channel that turns out to be relevant, and superconductivity requires this channel to be effectively *attractive*. Schematic [](#sch:s05:phonon_exchange) shows the simplest case, where two electrons interact through a phonon. At frequencies below the phonon frequency $\omega_0$ the phonon term is attractive, and above it the term is repulsive.

![Interaction mediated by a phonon. (a) One electron deforms the lattice, and the second one feels it. (b) The effective interaction $V_\mathrm{eff}(\omega)=V_c-(2g^2/\omega_0)/[1-(\omega/\omega_0)^2]$ is plotted in units of $2g^2/\omega_0$, with $V_c=0.5$. It is negative for $\omega<\omega_0$, so the net sign of the channel is attractive.](figures/web/session05/phonon_exchange.svg){#sch:s05:phonon_exchange alt="Two electron lines joined by a wavy phonon line, and the effective interaction against frequency, which is negative below the phonon frequency and positive above it."}

This is the natural point to distinguish the two families of superconductors.

- **Conventional superconductors**, where the attractive channel is mediated by phonons. This is the case that we understand best. Mean-field theory, which is called BCS theory, works well at the quantitative level, and the critical temperatures of simple conventional superconductors such as aluminum or lead can be predicted from theory.

- **Unconventional superconductors**, where the attraction is mediated by anything that is not a phonon, such as antiferromagnetic or ferromagnetic magnons, plasmons, valence fluctuations, charge fluctuations and others. Here we do not have a predictive theory that is equally reliable. Even to identify *which* quasiparticle mediates the attraction in a given unconventional superconductor is often still an open research question, and it is one of the major unsolved problems that the field is working on today.

## The mean-field pairing Hamiltonian in detail {#sec-5-5 number="5.5"}

Let us now build the mean-field pairing Hamiltonian with the same care that we used in session 1 for the charge-density-wave and magnetic examples, instead of only pointing at $\Delta = \langle
cc\rangle$. We take the simplest interacting Hamiltonian that can give superconductivity, which is a one-dimensional tight-binding chain with an attractive onsite interaction between opposite spins,

$$H = -t\sum_{n,\sigma}\left(c_{n\sigma}^\dagger c_{n+1,\sigma} + \text{h.c.}\right) - \mu\sum_{n\sigma}c_{n\sigma}^\dagger c_{n\sigma} + U\sum_n c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger c_{n\downarrow} c_{n\uparrow}, \qquad U<0. \tag{5.2}$$

This is exactly eq. [1.7](#eq-1-7) of session 1, now with $U = -|U| < 0$. It is the attractive branch of the same Hamiltonian, and its repulsive branch gives rise to magnetism, which is the topic of session 6. This time we do the mean-field decoupling of the quartic term in the *pairing* channel, also called the particle-particle channel, instead of the density channel. We define the order parameter

$$\Delta_n \equiv U\langle c_{n\downarrow}c_{n\uparrow}\rangle, \tag{5.3}$$

and we factorize $c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger c_{n\downarrow}c_{n\uparrow} \approx
\langle c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger\rangle c_{n\downarrow}c_{n\uparrow} +
c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger \langle c_{n\downarrow}c_{n\uparrow}\rangle - \langle
c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger\rangle\langle c_{n\downarrow}c_{n\uparrow}\rangle$. This is the same Wick-type factorization that we used in all of session 1, now applied to a different pair of operators. The resulting mean-field Hamiltonian is

$$H_{\text{MF}} = -t\sum_{n\sigma}\left(c_{n\sigma}^\dagger c_{n+1,\sigma}+\text{h.c.}\right) - \mu\sum_{n\sigma}c_{n\sigma}^\dagger c_{n\sigma} + \sum_n\left(\Delta_n\, c_{n\uparrow}^\dagger c_{n\downarrow}^\dagger + \Delta_n^*\, c_{n\downarrow}c_{n\uparrow}\right) - \sum_n\frac{|\Delta_n|^2}{U}. \tag{5.4}$$

When we solve it self-consistently, $\Delta_n$ is exactly zero for $U>0$, the repulsive case, and it can become nonzero for $U<0$, the attractive case. This is the superconducting order parameter, and it is the term that breaks gauge symmetry.

![The mean-field loop of session 1, drawn there for a charge density wave. For the pairing channel of [(5.4)](#eq-5-4) the guess is $\Delta_n$, and the new expectation value is $\langle c_{n\downarrow}c_{n\uparrow}\rangle$.](figures/s01f05_selfconsistency.svg){alt="A loop of four stations, a guess of the expectation values, the mean-field Hamiltonian, its diagonalization and the new expectation values, with a return arrow until the result stops changing."}

::: quiz
We start the loop for the attractive chain [(5.2)](#eq-5-2) with a small guess $\Delta_n\neq0$, but now with $U>0$. Which self-consistent solution does the loop find?

- [ ] A finite $\Delta_n$, since any pair amplitude sustains itself.

    This is false. For one site with $U=+t$ and $\mu=0$, the doubly occupied state costs $+t$, while the empty and the singly occupied states have energy $0$. The ground states have $\langle c_\downarrow c_\uparrow\rangle=0$, so there is no pair amplitude to sustain.

- [x] Only $\Delta_n=0$.

    This is true. The pair susceptibility $g>0$ of the bands gives $\Delta_\text{new}=-U g\Delta$ in [(5.3)](#eq-5-3). For $U>0$ the factor is negative, so every finite guess comes back with the opposite sign, and no finite $\Delta_n$ reproduces itself. For $U<0$ the factor is positive and a finite $\Delta_n$ can be self-consistent.

- [ ] The loop keeps the guess, since [(5.3)](#eq-5-3) does not depend on the sign of $U$.

    This is false. The sign of $U$ enters [(5.3)](#eq-5-3) as a prefactor. If $Ug=0.5$ at $U>0$, the loop gives $\Delta_\text{new}=-0.5\,\Delta$ in each step, so the guess does not stay.

    ![The loop for $Ug=0.5$ and $\Delta_0=1$. Each step flips the sign and halves the guess, so the iteration goes to zero.](figures/web/session05/pairing_cobweb.svg){alt="A staircase between a line of slope minus one half and the diagonal, which spirals into the origin."}
:::

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "s-wave superconductivity driven by attractive interactions" (Core), and "Dependence on the strength of the attractive interaction" (Challenge)

Build the attractive-Hubbard chain of [(5.2)](#eq-5-2), run the pairing self-consistency loop that gives $\Delta$ in [(5.3)](#eq-5-3)-[(5.4)](#eq-5-4), and look at how $\Delta$ grows from zero as you make $U$ more negative. This is the same behavior as in session 1, where the charge imbalance grew with $V$ and the magnetization grew with $U>0$.
:::

::: {.tryit notebook="session5.ipynb" cell="Dependence on the strength of the attractive interaction"}
Run the loop with `U=-1.0`, `-1.5` and `-2.0` at `filling=0.1`. The smallest energy of the electron bands is $|\Delta|$, and it grows from about 0.1 to 0.2 and 0.4. The gap grows fast with $|U|$.
:::
