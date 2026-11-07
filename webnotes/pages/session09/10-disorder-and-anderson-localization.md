## Disorder and Anderson localization {#sec-9-10 number="9.10a"}

So far we have only discussed a *single* impurity. What happens when we put many impurities in the whole material? A single impurity changes the ground state only a little. Many impurities, in particular when they are placed at random, can change it completely, because they break translational symmetry in the whole system and not only locally. It is useful to list all the possibilities, since there are three different regimes of translational symmetry to consider, and not only the symmetric and the non-symmetric ones.

1.  **Periodic.** There is full translational symmetry. Every eigenstate is extended, with weight $\sim 1/N$ on each of $N$ sites.

2.  **Quasiperiodic.** The system is not periodic, since there is no repeating unit cell, but it is not random either, since the potential follows a fixed and deterministic rule that never repeats. Here the eigenstates can be extended, critical, or fully localized, depending on the strength of the potential. Critical means localized with a power law, so that the state is not even normalizable in the strict sense.

3.  **Strongly (randomly) disordered.** The eigenstates are localized, and each of them has a finite localization length.

**Quasiperiodic case.** The standard model here is a 1D tight-binding chain with an onsite modulation at an irrational wavevector. It belongs to the Aubry-André-Harper family.

$$H = -t\sum_n \left(c_n^\dagger c_{n+1} + \text{h.c.}\right) + V_0 \sum_n \cos(2\pi q\, n + \phi)\, c_n^\dagger c_n, \qquad q \notin \mathbb{Q}.$$

Since $q$ is irrational, the potential never repeats exactly, so the chain has no translational symmetry at all. However, it is not random either, because the value of the potential at every site is completely fixed once we fix $q$ and $\phi$. As we increase $V_0$ from zero, the eigenstates change from extended to a marginal, critical behavior with a power law close to the self-dual point of the model. This point is $V_0 = 2t$ in the plain Aubry-André model, and for $V_0$ well above it the states are exponentially localized.

The tool that we use to distinguish these regimes is the **inverse participation ratio (IPR)**,

$$\mathrm{IPR}(\psi) = \sum_i |\psi_i|^4, \qquad \sum_i |\psi_i|^2 = 1. \tag{9.12}$$

An extended state with weight $\sim 1/N$ per site gives $\mathrm{IPR} \sim N\cdot(1/N)^2 = 1/N$, which vanishes as the system grows. A localized state, with $O(1)$ weight on $O(1)$ sites, gives $\mathrm{IPR} \sim O(1)$, which does not depend on the system size. A critical state is between the two, and its $\mathrm{IPR}$ follows a non-trivial power law in $N$. This is a multifractal signature, which is different from both of the two clean limits. Figure [9.6](#fig:s09:localization) shows the three eigenstates side by side, together with the scaling of [(9.12)](#eq-9-12) with $N$, which separates them in a quantitative way.

![The three regimes of Section [9.10](#sec-9-10), shown through their effect on an eigenstate of a chain of $N=89$ sites, with the weight $|\psi_i|^2$ of each site as a column. (a) With a periodic potential every eigenstate is a Bloch wave, with weight exactly $1/N$ on every site, and this height becomes smaller as the chain grows. (b) At the self-dual point of the quasiperiodic model the state is neither extended nor localized. It has structure on every length scale at the same time, with large peaks and smaller copies of the same pattern between them, and this state is called critical, or multifractal. (c) With really random disorder the state is concentrated on a few sites and it is strictly zero, to numerical precision, over most of the chain. *Note the three different vertical scales.* For this reason we need a number and not a visual check, and this number is the inverse participation ratio [(9.12)](#eq-9-12). (d) The IPR separates the three regimes by how it scales with system size, computed here for $N=34$ to $610$. It goes as $\mathrm{IPR}\sim 1/N$ for extended states and as $\mathrm{IPR}\sim O(1)$ for localized ones, with an anomalous power $N^{-\tau}$ and $0<\tau<1$ for the critical state between them. On a log-log plot these are three straight lines with three different slopes.](figures/s09f06_localization.svg){#fig:s09:localization number="9.6"}

![The mean $\mathrm{IPR}$ of [(9.12)](#eq-9-12) over all the eigenstates of the quasiperiodic chain, against $V_0$, for rings of $N=55$, $233$ and $987$ sites with $\phi=0.3$. We take $q$ as a ratio of two Fibonacci numbers, $610/987$ for the largest ring, which is close to $(\sqrt5-1)/2$ and keeps the ring periodic. Below $V_0=2t$ the three curves are apart, and $N\cdot\mathrm{IPR}\approx2$ for all of them, which is the $1/N$ of extended states. Above $V_0=2t$ the three curves fall on top of each other, at a value that does not depend on $N$, which is the signature of localized states. All the eigenstates change at the self-dual point at the same time, since this model has no mobility edge.](figures/web/session09/aah_ipr.svg){#sch:s09:aah_ipr alt="The mean inverse participation ratio on a logarithmic scale against the strength of the potential, for three sizes. The three curves are apart on the left, rise steeply at two, and join on the right."}

::: quiz
A normalized state has the same weight on $10$ sites of a chain and zero weight elsewhere. What is its $\mathrm{IPR}$ of [(9.12)](#eq-9-12), and how does it change if the chain grows?

- [ ] $1/N$, and it decreases as the chain grows.

    This is false. The value $1/N$ is the IPR of an extended state. For $N=100$ our state has $0.1$, ten times more than $1/N=0.01$.

- [x] $1/10$, and it does not change as the chain grows.

    This is true. For ten sites with $|\psi_i|^2=1/10$ the sum is $10\times(1/10)^2=0.1$. If the chain grows from $N=100$ to $10^4$ sites, the value stays $0.1$.

- [ ] $10/N$, and it decreases as the chain grows.

    This is false. The value $10/N$ would be $0.001$ for $N=10^4$. The state still sits on ten sites, so its IPR is $0.1$ and not smaller.
:::

::: quiz
We double the size of the chain, and the $\mathrm{IPR}$ of a state changes by a factor $0.7$. Which regime is this?

- [ ] Extended, since the $\mathrm{IPR}$ decreases.

    This is false. An extended state has $\mathrm{IPR}=1/N$, so doubling $N$ gives a factor $0.5$. A factor $0.7$ is not this, even if the IPR decreases.

- [ ] Localized, since the $\mathrm{IPR}$ is finite.

    This is false. A localized state does not change at all, so its factor is $1$. The factor $0.7$ is not equal to one, and a finite IPR is not enough.

- [x] Critical, with $N^{-\tau}$ and $\tau\approx0.5$.

    This is true. The factor is $2^{-\tau}=0.7$, so $\tau\approx0.5$. Extended states give $\tau=1$ and a factor $0.5$, localized states give $\tau=0$ and a factor $1$, so this is between them.
:::

::: {.tryit notebook="session9.ipynb" cell="Extended and localized states in quasicrystals"}
Run the cell and look at the average of $1/\lambda$ on the left. It stays close to zero up to $v\approx2$ and then grows fast. This is the self-dual point $V_0=2t$ of the model. Change `np.sqrt(2)` to another irrational number and check that the point stays at $v\approx2$.
:::

The second regime, with random disorder, is the content of the next part.

::: comesback
- In Section [9.10b](#sec-9-10b) the disorder is random, and in one dimension every state is localized.
- In Section [10.7](#sec-10-7) disorder realizations are hidden variables that a Hamiltonian-learning network must average over.
:::
