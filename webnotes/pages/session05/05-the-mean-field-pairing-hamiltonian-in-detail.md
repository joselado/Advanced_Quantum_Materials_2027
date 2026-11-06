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

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "s-wave superconductivity driven by attractive interactions" (Core), and "Dependence on the strength of the attractive interaction" (Challenge)

Build the attractive-Hubbard chain of [(5.2)](#eq-5-2), run the pairing self-consistency loop that gives $\Delta$ in [(5.3)](#eq-5-3)-[(5.4)](#eq-5-4), and look at how $\Delta$ grows from zero as you make $U$ more negative. This is the same behavior as in session 1, where the charge imbalance grew with $V$ and the magnetization grew with $U>0$.
:::
