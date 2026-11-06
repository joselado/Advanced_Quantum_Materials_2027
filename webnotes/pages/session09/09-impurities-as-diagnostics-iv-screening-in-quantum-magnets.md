## Impurities as diagnostics IV, screening in quantum magnets {#sec-9-9 number="9.9"}

The last case study brings us directly back to the construction of session 8. We take a frustrated Heisenberg model with a ground state similar to a quantum spin liquid. This ground state has zero net magnetization on every site, and it does not break time-reversal symmetry. We add one local magnetic perturbation, and we ask how the spins around it screen it.

For $S=1/2$ we do not need to repeat the construction from the beginning, since session 8 already built the tool that we need. We write each spin with a pair of auxiliary (Abrikosov) fermions, $S_i =
\tfrac{1}{2}\sum_{\alpha\beta} f_{i\alpha}^\dagger \boldsymbol{\sigma}_{\alpha\beta} f_{i\beta}$, with the single-occupancy constraint $\sum_\sigma f_{i\sigma}^\dagger f_{i\sigma} = 1$ at every site, and we make a mean-field decoupling of the quartic Hamiltonian that we obtain. As we derived in session 8, this turns the Heisenberg model with a local magnetic perturbation into a bilinear Hamiltonian for the spinons, similar to a tight-binding one, with an effective onsite term at the impurity site that mixes with the spinon band. We will not derive this mapping again here, and the notes of session 8, in the part on the Abrikosov-fermion construction, give the full mean-field decoupling.

What matters for us in this session is what this mapping gives us. It turns the problem of screening a magnetic moment inside a quantum spin liquid into *exactly* the same mathematical problem as the impurity in a one-dimensional electron gas of Section [9.6](#sec-9-6), where the electrons are replaced by spinons. The induced spin correlation $\langle S_0 \cdot S_n\rangle$, as a function of the distance $n$ from the impurity, therefore has the same structure as [(9.9)](#eq-9-9). It has an oscillation set by the antiferromagnetic exchange, and it decays with distance in a way that depends on whether the spinon band is gapped or gapless.

Here the comparison between the $S=1/2$ and $S=1$ Heisenberg chains becomes clear. Both have a ground state similar to a spin liquid, with zero onsite magnetization when there is no impurity, and both develop an oscillating induced moment once the impurity is switched on. However, the decay is qualitatively different in the two cases.

$$\langle S_0 \cdot S_n \rangle \;\sim\;
\begin{cases}
\dfrac{(-1)^n}{n} & S = 1/2 \quad \text{(power-law, gapless)}, \\[6pt]
(-1)^n\, e^{-n/\xi} & S = 1 \quad \text{(exponential, gapped)}.
\end{cases} \tag{9.11}$$

The reason is the same reasoning as for [(9.9)](#eq-9-9). Through the Abrikosov-fermion construction, the spin-$1/2$ Heisenberg chain maps onto a gapless tight-binding chain of spinons, with a real Fermi surface of two points, as for the 1D metal of Section [9.4](#sec-9-4). So the impurity response must decay algebraically, in the same way as the Friedel oscillations of a metal. The spin-1 chain, on the other hand, has an excitation gap. This is the Haldane gap, which is not named explicitly in the transcript, but it is the gap that opens for antiferromagnetic chains with integer spin. This gap sets a finite correlation length $\xi$, and it forces the impurity response to decay exponentially, in the same way as charge screening inside a band insulator.

This gives us a completely general diagnostic, which connects all the case studies of this session, namely that *a power-law decay of an impurity response signals a gapless ground state, and an exponential decay signals a gapped one, where the decay length in the exponent is the correlation length.* The metal of Section [9.6](#sec-9-6), which has a power law, the insulating chain at the end of that section, which has an exponential, and the two quantum-magnet cases here are all examples of the same statement, and they are drawn side by side in figure [9.5](#fig:s09:decay).

![The diagnostic that connects the whole session, drawn for the two Heisenberg chains of [(9.11)](#eq-9-11). Close to the impurity both look the same, with an induced moment that changes sign from site to site, because the exchange is antiferromagnetic. The only difference between them is how the envelope decays. (a) The $S=1/2$ chain maps, through the Abrikosov-fermion construction of session 8, onto a *gapless* spinon band with a real Fermi surface of two points, so its envelope decays as the power law $1/n$. This is the same mathematics, and the same reason, as for the Friedel oscillations [(9.9)](#eq-9-9) of a metal. (b) The $S=1$ chain has the Haldane gap, which fixes a finite correlation length $\xi$ and gives an exponential envelope $e^{-n/\xi}$, drawn for $\xi=2.5$, in the same way as charge screening decays inside a band insulator. (c) On a logarithmic vertical scale the two are easy to distinguish, since an exponential is a straight line of slope $-1/\xi$ and a power law is not. The statement can be read in both directions, so a measured decay law is a measurement of whether the ground state is gapped.](figures/s09f05_decay.svg){#fig:s09:decay number="9.5"}

This specific topic, the screening in quantum magnets, is only in the slides and in the lecture, and it has no direct counterpart in `session9.ipynb`. None of the sections of the notebook build a chain of spinons or Abrikosov fermions, so there is no hands-on exercise that reproduces [(9.11)](#eq-9-11) itself.

::: notebookbox
**Notebook check-in:** [`session9.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session9.ipynb), "The impact of a strong impurity" (Core)

This is not a spin model, but it is the closest exercise in its logic. It compares how a dimerized chain, with a stronger or a weaker gap, responds to a strong local impurity. Run it with [(9.11)](#eq-9-11) in mind, and check the same principle in the fermionic language, where the chain with the stronger gap screens the impurity over a shorter length.
:::
