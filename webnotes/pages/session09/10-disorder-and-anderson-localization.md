## Disorder and Anderson localization {#sec-9-10 number="9.10a"}

So far we have only discussed a *single* impurity. What happens when we put many impurities in the whole material? We will now see that one number, the inverse participation ratio, tells an extended state from a localized one, and that in the Aubry-André chain all the states change at once at $V_0=2t$.

A single impurity changes the ground state only a little. Many impurities, in particular when they are placed at random, can change it completely, because they break translational symmetry in the whole system and not only locally. It is useful to list all the possibilities, since there are three different regimes of translational symmetry to consider, and not only the symmetric and the non-symmetric ones.

1.  **Periodic.** There is full translational symmetry. Every eigenstate is extended, with weight $\sim 1/N$ on each of $N$ sites.

2.  **Quasiperiodic.** The system is not periodic, since there is no repeating unit cell, but it is not random either, since the potential follows a fixed and deterministic rule that never repeats. Here the eigenstates can be extended, critical, or fully localized, depending on the strength of the potential. Critical means neither extended nor localized, with an IPR that falls as a power of $N$ slower than $1/N$.

3.  **Strongly (randomly) disordered.** The eigenstates are localized, and each of them has a finite localization length.

**Quasiperiodic case.** The standard model here is a 1D tight-binding chain with an onsite modulation at an irrational wavevector. It belongs to the Aubry-André-Harper family.

$$H = -t\sum_n \left(c_n^\dagger c_{n+1} + \text{h.c.}\right) + V_0 \sum_n \cos(2\pi q\, n + \phi)\, c_n^\dagger c_n, \qquad q \notin \mathbb{Q}.$$

Since $q$ is irrational, the potential never repeats exactly, so the chain has no translational symmetry at all. However, it is not random either, because the value of the potential at every site is completely fixed once we fix $q$ and $\phi$. As we increase $V_0$ from zero, the eigenstates change from extended to a marginal, critical behavior with a power law close to the self-dual point of the model. This point is $V_0 = 2t$ in the plain Aubry-André model, and for $V_0$ well above it the states are exponentially localized.

::: {.steps title="Why the transition is at V0 = 2t"}
We take the simplest case first, the phase $\phi=0$. We write an eigenstate as a sum of plane waves, whose wavevectors are the multiples $2\pi qm$ of the wavevector of the potential,

$$\psi_n=\sum_m e^{2\pi i qmn}\,a_m .$$

The hopping does not mix the plane waves, since $\psi_{n+1}+\psi_{n-1}$ gives each of them the factor $2\cos(2\pi qm)$. The potential shifts $m$ by one, since

$$\cos(2\pi qn)\,e^{2\pi iqmn}=\frac12\left(e^{2\pi iq(m+1)n}+e^{2\pi iq(m-1)n}\right).$$

For an irrational $q$ the plane waves with different $m$ are independent. So the Schrödinger equation

$$-t\left(\psi_{n+1}+\psi_{n-1}\right)+V_0\cos(2\pi qn)\,\psi_n=E\,\psi_n$$

becomes an equation for the amplitudes $a_m$,

$$\frac{V_0}{2}\left(a_{m+1}+a_{m-1}\right)-2t\cos(2\pi qm)\,a_m=E\,a_m .$$

This is the same chain again, now in the index $m$, with the hopping $V_0/2$ in the place of $t$ and the potential $2t$ in the place of $V_0$. The two signs do not change the localization, since $a_m\to(-1)^ma_m$ changes the sign of the hopping, and a phase $\pi$ in the potential changes the sign of the cosine. A phase $\phi\neq0$ of the potential only gives the new hopping a phase. So the ratio $V_0/2t$ of the first chain becomes $2t/V_0$ in the second one.

A state that is localized in $n$ is a sum of many plane waves, so it is extended in $m$, and the other way round. So when all the states of the chain with $V_0$ are localized, all the states of the chain with $4t^2/V_0$ are extended. The transformation exchanges the two regimes, and the only strength that it maps onto itself is $V_0=2t$, which is the self-dual point. On the rings of [](#sch:s09:aah_ipr), where $q$ is a ratio of two Fibonacci numbers, the same transformation is a discrete Fourier transform, and it holds exactly. On a ring the change $a_m\to(-1)^ma_m$ and the removal of the phase $\phi$ leave a mismatch on the bond that closes the ring. So the levels at $V_0$ are $V_0/2t$ times those at $4t^2/V_0$ only up to a small difference, which is $0.015t$ on $233$ sites and $0.0035t$ on $987$ sites at $V_0=3t$ and $\phi=0.3$.
:::

The tool that we use to distinguish these regimes is the **inverse participation ratio (IPR)**.

::: key
The inverse participation ratio of a normalized state $\psi$ is

$$\mathrm{IPR}(\psi) = \sum_i |\psi_i|^4, \qquad \sum_i |\psi_i|^2 = 1. \tag{9.12}$$

It falls as $1/N$ for a state that is extended over $N$ sites, it stays finite for a localized state, and at the critical point it falls with a power of $N$ between the two.
:::

An extended state with weight $\sim 1/N$ per site gives $\mathrm{IPR} \sim N\cdot(1/N)^2 = 1/N$, which vanishes as the system grows. A localized state, with $O(1)$ weight on $O(1)$ sites, gives $\mathrm{IPR} \sim O(1)$, which does not depend on the system size. A critical state is between the two, and its $\mathrm{IPR}$ follows a non-trivial power law in $N$. This is a multifractal signature, which is different from both of the two clean limits. Figure [9.6](#fig:s09:localization) shows the three eigenstates side by side, together with the scaling of [(9.12)](#eq-9-12) with $N$, which separates them in a quantitative way.

![The three regimes of Section [9.10a](#sec-9-10), shown through their effect on an eigenstate of a chain of $N=89$ sites, with the weight $|\psi_i|^2$ of each site as a column. (a) With a periodic potential every eigenstate is a Bloch wave, with weight exactly $1/N$ on every site, and this height becomes smaller as the chain grows. (b) At the self-dual point of the quasiperiodic model the state is neither extended nor localized. It has structure on every length scale at the same time, with large peaks and smaller copies of the same pattern between them, and this state is called critical, or multifractal. (c) With really random disorder the state is concentrated on a few sites and it is strictly zero, to numerical precision, over most of the chain. *Note the three different vertical scales.* For this reason we need a number and not a visual check, and this number is the inverse participation ratio [(9.12)](#eq-9-12). (d) The IPR separates the three regimes by how it scales with system size, computed here for $N=34$ to $610$. It goes as $\mathrm{IPR}\sim 1/N$ for extended states and as $\mathrm{IPR}\sim O(1)$ for localized ones, with an anomalous power $N^{-\tau}$ and $0<\tau<1$ for the critical state between them. On a log-log plot these are three straight lines with three different slopes.](figures/s09f06_localization.svg){#fig:s09:localization number="9.6"}

![The mean $\mathrm{IPR}$ of [(9.12)](#eq-9-12) over all the eigenstates of the quasiperiodic chain, against $V_0$ in units of the hopping $t$, for rings of $N=55$, $233$ and $987$ sites with $\phi=0.3$, computed with pyqula. We take $q$ as a ratio of two Fibonacci numbers, $610/987$ for the largest ring, which is close to $(\sqrt5-1)/2$ and keeps the ring periodic. Below $V_0=2t$ the three curves are apart, and at $V_0=t$ the product $N\cdot\mathrm{IPR}$ is about $2$ for all of them, which is the $1/N$ of extended states. Above $V_0=2t$ the three curves fall on top of each other, at a value that does not depend on $N$, which is the signature of localized states. All the eigenstates change at the self-dual point at the same time, since this model has no mobility edge.](figures/web/session09/aah_ipr.svg){#sch:s09:aah_ipr alt="The mean inverse participation ratio on a logarithmic scale against the strength of the potential, for three sizes. The three curves are apart on the left, rise steeply at two, and join on the right." script="g6_aah_ipr.py"}

::: quiz
The inverse participation ratio of a normalized state $\psi$ is

$$\mathrm{IPR}=\sum_i|\psi_i|^4 .$$

A state has the same weight on $10$ sites. On all the other sites it is zero. What is its $\mathrm{IPR}$, and does it change when the chain grows?

- [ ] $1/N$, and it decreases as the chain grows.

    This is false. The value $1/N$ is the IPR of an extended state. For $N=100$ our state has $0.1$, ten times more than $1/N=0.01$.

- [x] $1/10$, and it does not change as the chain grows.

    This is true. For ten sites with $|\psi_i|^2=1/10$ the sum is $10\times(1/10)^2=0.1$. If the chain grows from $N=100$ to $10^4$ sites, the value stays $0.1$.

- [ ] $10/N$, and it decreases as the chain grows.

    This is false. The value $10/N$ would be $0.001$ for $N=10^4$. The state still sits on ten sites, so its IPR is $0.1$ and not smaller.
:::

::: quiz
The inverse participation ratio of a normalized state is

$$\mathrm{IPR}=\sum_i|\psi_i|^4 .$$

We double the length of the chain. The $\mathrm{IPR}$ of a state changes by a factor $0.7$. Which regime is this?

- [ ] Extended, since the $\mathrm{IPR}$ decreases.

    This is false. An extended state has $\mathrm{IPR}=1/N$, so doubling $N$ gives a factor $0.5$. A factor $0.7$ is not this, even if the IPR decreases.

- [ ] Localized, since the $\mathrm{IPR}$ is finite.

    This is false. A localized state does not change at all, so its factor is $1$. The factor $0.7$ is not equal to one, and a finite IPR is not enough.

- [x] Critical, with $N^{-\tau}$ and $\tau\approx0.5$.

    This is true. The factor is $2^{-\tau}=0.7$, so $\tau\approx0.5$. Extended states give $\tau=1$ and a factor $0.5$, localized states give $\tau=0$ and a factor $1$, so this is between them.
:::

::: quiz
The Aubry-André chain has the onsite energy $V_0\cos(2\pi qn+\phi)$ and the hopping $t$. Each picture shows $|\psi_n|^2$ of its lowest state on a ring of $233$ sites. The three pictures have three values of $V_0$. The vertical axis is logarithmic. The inverse participation ratio is

$$\mathrm{IPR}=\sum_n|\psi_n|^4 .$$

Which state keeps its $\mathrm{IPR}$ when the ring grows?

- [ ] ![A logarithmic plot of the weight on each site, which stays in a narrow band near the same value on all the sites of the ring.](figures/web/session09/g6_quiz_aah_v1.svg)

    This is false. The weight is spread over the whole ring, and $N\cdot\mathrm{IPR}=1.20$ on rings of $55$, $233$ and $987$ sites. So the $\mathrm{IPR}$ falls as $1/N$, from $0.0052$ on $233$ sites to $0.0012$ on $987$ sites. This state is at $V_0=t$, where every state is extended.

- [x] ![A logarithmic plot of the weight on each site, with one sharp peak near one and a steep fall on both sides of it.](figures/web/session09/g6_quiz_aah_v3.svg)

    This is true. Almost all the weight sits on one site, $0.91$ of it, and the $\mathrm{IPR}$ is $0.83$ on rings of $55$, $233$ and $987$ sites. This state is at $V_0=3t$, above the self-dual point, where every state is localized.

- [ ] ![A logarithmic plot of the weight on each site, which is spread over the whole ring with many spikes of very different heights.](figures/web/session09/g6_quiz_aah_v2.svg)

    This is false. This is a critical state, at the self-dual point $V_0=2t$. Its $\mathrm{IPR}$ is $0.23$, $0.099$ and $0.062$ on rings of $55$, $233$ and $987$ sites. It falls as the ring grows, but more slowly than $1/N$. From $233$ to $987$ sites, $1/N$ falls to $0.24$ of its value, and this $\mathrm{IPR}$ only to $0.62$ of its value.
:::

:::: problem
A localized state of an infinite chain has the amplitude $\psi_n\propto e^{-|n|/\xi}$. Compute its $\mathrm{IPR}$ [(9.12)](#eq-9-12) for $\xi=10$ sites. Then show that for a large $\xi$ it is about $1/(2\xi)$, with no size of the chain in it.

::: solution
We first normalize the state. The weight on site $n$ is $|\psi_n|^2=A^2e^{-2|n|/\xi}$, and the geometric series gives

$$\sum_{n=-\infty}^{\infty}e^{-2|n|/\xi}=\frac{1+e^{-2/\xi}}{1-e^{-2/\xi}}=\coth\frac1\xi ,$$

so $A^2=1/\coth(1/\xi)$. The $\mathrm{IPR}$ needs the same sum with $4|n|/\xi$ in the exponent, which is $\coth(2/\xi)$, so

$$\mathrm{IPR}=\frac{\coth(2/\xi)}{\coth^2(1/\xi)} .$$

For $\xi=10$ this is $5.066/10.033^2=0.0503$. For a large $\xi$ we use $\coth x\approx1/x$, which gives $\mathrm{IPR}\approx(\xi/2)/\xi^2=1/(2\xi)$, here $0.05$. The number of sites does not appear, since both sums are set by a few times $\xi$ sites around the center of the state.

This is why the $\mathrm{IPR}$ of a localized state stays finite when the sample grows, while an extended state on a chain of $N$ sites has $\mathrm{IPR}\sim1/N$, which goes to zero. For this pure exponential, with $\xi$ much longer than one site, the $\mathrm{IPR}$ also gives the localization length, $\xi\approx1/(2\,\mathrm{IPR})$. This does not hold for every localized state. The lowest state of the Aubry-André ring of $233$ sites at $V_0=3t$ and $\phi=0.3$ has more weight on its center than its tail suggests. It has $1/(2\,\mathrm{IPR})=0.6$ sites, while fits of its tail that reach $30$ to $60$ sites from the center give $\xi$ between $2.1$ and $2.4$ sites.
:::
::::

::: {.tryit notebook="session9.ipynb" cell="Extended and localized states in quasicrystals"}
Run the cell and look at the average of $1/\lambda$ on the left. It stays close to zero up to $v\approx2$ and then grows fast. This is the self-dual point $V_0=2t$ of the model. Change `np.sqrt(2)` to another irrational number and check that the point stays at $v\approx2$.
:::

The third regime, with random disorder, is the content of the next part.

::: comesback
- In Section [9.10b](#sec-9-10b) the disorder is random, and in one dimension every state is localized.
- In Section [10.7](#sec-10-7) disorder realizations are hidden variables that a Hamiltonian-learning network must average over.
:::
