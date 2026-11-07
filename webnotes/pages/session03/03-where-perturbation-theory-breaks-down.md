## Where perturbation theory breaks down {#sec-3-3 number="3.3"}

Before we use [(3.1)](#eq-3-1), we should say when it fails, because several of the most important phenomena in this course appear in this failure. The expansion [(3.1)](#eq-3-1) assumes that we are in the *perturbative regime*, where a small change in the input, which is the strength of the perturbation, gives a small change in the output. This is not always the case. We name three cases now, because we will see each of them in detail later in the course. The simplest example is a system of two levels, which is shown in [](#sch:s03:perturb_gap).

![Two levels at $-\Delta$ and $+\Delta$ that are coupled by a perturbation $\lambda V$. The red dashed line is the amplitude of the first-order term of [(3.1)](#eq-3-1), which grows linearly with $\lambda V/\Delta$. The blue line is the exact amplitude of the upper level in the perturbed ground state, which saturates at $1/\sqrt{2}$. The two agree within a few percent only in the shaded region. Look at where the lines separate, since this is where a finite order of the expansion is not enough.](figures/web/session03/perturb_gap.svg){#sch:s03:perturb_gap alt="Two curves against the ratio of the perturbation to the level spacing, a straight dashed line for the first order and a curve that bends over and saturates for the exact result."}

- An impurity in a metal gives rise to the **orthogonality catastrophe**. In a large metal the many-body ground state after the perturbation becomes orthogonal to the original ground state, even for a very small perturbation. So no Taylor expansion of finite order in $\lambda$ can connect the two.

- A quantum spin, which is a local magnetic moment, coupled to a metal gives rise to the **Kondo effect**. The relevant energy scale, which is the Kondo temperature, is a non-perturbative function of the coupling constant, and no order of perturbation theory in this coupling gives it. We will study the Kondo impurity and the Kondo lattice in detail in Section [8.11](#sec-8-11), and here we only mention it as a first sign that ordinary perturbation theory has a strict limit.

- **Superconductivity** is also non-perturbative, since the BCS gap does not appear at any finite order in the interaction strength if we start from the normal state. In Session 5 we will see that the gap comes instead from a mean-field Hamiltonian, the Bogoliubov-de Gennes Hamiltonian of Section [5.8](#sec-5-8).

We can see the first of these cases in a small calculation. We take a ring at half filling, we add an impurity on one site, and we compute the overlap between the two ground states. For a metal the overlap keeps falling when the ring grows, and for the same impurity in an insulator it does not, as we see in [](#sch:s03:orthogonality).

![The overlap between the ground state of a ring at half filling and the ground state with an impurity of strength $V$ on one site, against the number of sites $N$. The hopping is $1$, and the gapped ring has a staggered potential $\pm1$. In the metal the overlap keeps decreasing as a power law, with an exponent $0.05$ for $V=3$ and $0.01$ for $V=1$ from the last points. The decay is slow, so only the trend matters. In the gapped ring the overlap is constant already for the smallest ring, $N=10$. Look at the two groups of lines, since the metal has no value of $N$ where the overlap stops changing.](figures/web/session03/orthogonality.svg){#sch:s03:orthogonality alt="Overlap of the ground states with and without an impurity against the size of a ring, falling slowly for a metal and flat for a gapped ring."}

For every model that we build in this session we stay inside the regime where [(3.1)](#eq-3-1) holds. For now, it is enough to know that this is not always the case.

::: quiz
An impurity in a large metal changes the ground state so that the new ground state is orthogonal to the old one. Why can no finite order of the expansion in $\lambda$ describe this?

- [ ] The impurity breaks the translation symmetry of the metal.

    This is false. An impurity also breaks the translation symmetry of an insulator with a gap $\Delta$. There the new ground state keeps an overlap close to one with the old one, and perturbation theory works for $\lambda\ll\Delta$.

- [x] Every finite order keeps a large overlap with the old ground state when $\lambda$ is small, while the exact overlap is zero.

    This is true. A truncated expansion differs from $|n\rangle$ only by terms that are small for small $\lambda$. Its overlap with the old state stays close to one, so it never reaches a state that is orthogonal to it.

- [ ] The perturbation is too strong at every order.

    This is false. In the limit of a large metal the overlap vanishes even for $\lambda=10^{-3}$, where every term of the series is small. The problem is the missing gap and not the strength.

:::

## The Hall conductivity from linear response {#sec-3-4 number="3.4"}

Now we apply [(3.1)](#eq-3-1) to the measurement that will bring us to topology, which is the transverse conductivity, also called the Hall conductivity. We take a two-dimensional material, apply a voltage in the $y$ direction, and ask what current flows in the $x$ direction. In momentum space, a voltage in $y$ enters as a perturbation proportional to $\partial H/\partial k_y$, since it shifts $k_y$ through the Peierls substitution. The current operator in the $x$ direction is, up to the electron charge, the group-velocity operator $\partial H/\partial k_x$. Both are the kind of matrix element that appears in [(3.1)](#eq-3-1).

When we put [(3.1)](#eq-3-1) into the definition of the Hall conductivity, we obtain an expression with two velocity operators and an energy denominator. This is the Kubo formula, for filled bands $n$ and empty bands $m$,

$$\sigma_{xy} \;\propto\; \sum_{n\ \text{filled}} \sum_{m\ \text{empty}} \int_{\text{BZ}}
\frac{d^2k}{(2\pi)^2}\;
\frac{\langle n|\partial_{k_x}H|m\rangle\langle m|\partial_{k_y}H|n\rangle - (x\leftrightarrow y)}
{(\varepsilon_n - \varepsilon_m)^2}. \tag{3.2}$$

At this point the expression still depends explicitly on the band energies through the denominator, so it seems that it should depend on all the details of the band structure. This is not the case, and the next section shows why.

::: quiz
The numerator of [(3.2)](#eq-3-2) contains the combination $\langle n|\partial_{k_x}H|m\rangle\langle m|\partial_{k_y}H|n\rangle-(x\leftrightarrow y)$. What happens to $\sigma_{xy}$ if we exchange the roles of $x$ and $y$?

- [ ] It does not change.

    This is false. For a Chern insulator with $C=1$ we have $\sigma_{xy}=e^2/h$ and $\sigma_{yx}=-e^2/h$. A current along $x$ and a current along $y$ give Hall voltages of opposite sign.

- [x] It changes sign.

    This is true. The combination in the numerator of [(3.2)](#eq-3-2) is antisymmetric under the exchange, so $\sigma_{yx}=-\sigma_{xy}$.

- [ ] It becomes zero.

    This is false. For $C=1$ both $\sigma_{xy}=e^2/h$ and $\sigma_{yx}=-e^2/h$ are nonzero. The exchange flips the sign of the Hall conductivity, and it does not remove it.

:::

::: comesback
- In Section [9.3](#sec-9-3) the same three non-perturbative cases mark the limit of the linear response that we derive there in detail.
- In Section [8.11](#sec-8-11) the Kondo effect of a single impurity is built, and then the Kondo lattice.
- In Session 5 superconductivity is solved without perturbation theory, with the Nambu spinor of Section [5.8](#sec-5-8).
- In Section [4.3](#sec-4-3) the Kubo formula [(3.2)](#eq-3-2) gives the Hall conductance of the Landau levels.
:::
