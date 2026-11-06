## Where perturbation theory breaks down {#sec-3-3 number="3.3"}

Before we use [(3.1)](#eq-3-1), we should say when it fails, because several of the most important phenomena in this course appear in this failure. The expansion [(3.1)](#eq-3-1) assumes that we are in the *perturbative regime*, where a small change in the input, which is the strength of the perturbation, gives a small change in the output. This is not always the case. We name three cases now, because we will see each of them in detail later in the course. The simplest example is a system of two levels, which is shown in [](#sch:s03:perturb_gap).

![Two levels at $-\Delta$ and $+\Delta$ that are coupled by a perturbation $\lambda V$. The red dashed line is the amplitude of the first-order term of [(3.1)](#eq-3-1), which grows linearly with $\lambda V/\Delta$. The blue line is the exact amplitude of the upper level in the perturbed ground state, which saturates at $1/\sqrt{2}$. The two agree within a few percent only in the shaded region. Look at where the lines separate, since this is where a finite order of the expansion is not enough.](figures/web/session03/perturb_gap.svg){#sch:s03:perturb_gap alt="Two curves against the ratio of the perturbation to the level spacing, a straight dashed line for the first order and a curve that bends over and saturates for the exact result."}

- An impurity in a metal gives rise to the **orthogonality catastrophe**. The many-body ground state after the perturbation becomes exactly orthogonal to the original ground state, even for a very small perturbation, so no Taylor expansion of finite order in $\lambda$ can connect the two.

- A quantum spin, which is a local magnetic moment, coupled to a metal gives rise to the **Kondo effect**. The relevant energy scale, which is the Kondo temperature, is a non-perturbative function of the coupling constant, and no order of perturbation theory in this coupling gives it. We will study the Kondo lattice model in detail in session 8, and here we only mention it as a first sign that ordinary perturbation theory has a strict limit.

- **Superconductivity** is also non-perturbative, since the BCS gap does not appear at any finite order in the interaction strength if we start from the normal state. We will work this out in detail in session 5.

In this lecture, and for every model that we build in this session, we stay inside the regime where [(3.1)](#eq-3-1) holds. For now, it is enough to know that this is not always the case.

::: quiz
An impurity in a metal changes the ground state so that the new ground state is exactly orthogonal to the old one. Why can no finite order of the expansion in $\lambda$ describe this?

- [ ] The impurity breaks the translation symmetry of the metal.
- [x] Every finite order keeps a large overlap with the old ground state when $\lambda$ is small, while the exact overlap is zero.
- [ ] All the energy denominators of a metal are exactly zero.
- [ ] The perturbation is too strong at every order.

A truncated expansion differs from $|n\rangle$ only by terms that are small for small $\lambda$. Its overlap with the old state stays close to one, and so it can never reach a state that is orthogonal to it.
:::

## The Hall conductivity from linear response {#sec-3-4 number="3.4"}

Now we apply [(3.1)](#eq-3-1) to the measurement that will bring us to topology, which is the transverse conductivity, also called the Hall conductivity. We take a two-dimensional material, apply a voltage in the $y$ direction, and ask what current flows in the $x$ direction. In momentum space, a voltage in $y$ enters as a perturbation proportional to $\partial H/\partial k_y$, since it shifts $k_y$ through the Peierls substitution. The current operator in the $x$ direction is, up to the electron charge, the group-velocity operator $\partial H/\partial k_x$. Both are the kind of matrix element that appears in [(3.1)](#eq-3-1).

When we put [(3.1)](#eq-3-1) into the definition of the Hall conductivity, we obtain an expression with two velocity operators and an energy denominator, which is the standard Kubo formula for a filled band $n$ and empty bands $m$,

$$\sigma_{xy} \;\propto\; \sum_{n\ \text{filled}} \sum_{m\ \text{empty}} \int_{\text{BZ}}
\frac{d^2k}{(2\pi)^2}\;
\frac{\langle n|\partial_{k_x}H|m\rangle\langle m|\partial_{k_y}H|n\rangle - (x\leftrightarrow y)}
{(\varepsilon_n - \varepsilon_m)^2}. \tag{3.2}$$

At this point the expression still depends explicitly on the band energies through the denominator, so it seems that it should depend on all the details of the band structure. This is not the case, and the next section shows why.

::: quiz
The numerator of [(3.2)](#eq-3-2) contains the combination $\langle n|\partial_{k_x}H|m\rangle\langle m|\partial_{k_y}H|n\rangle-(x\leftrightarrow y)$. What happens to $\sigma_{xy}$ if we exchange the roles of $x$ and $y$?

- [ ] It doubles.
- [ ] It does not change.
- [ ] It becomes zero.
- [x] It changes sign.

The combination is antisymmetric under the exchange of $x$ and $y$. The Hall conductivity is therefore antisymmetric as well, which means that $\sigma_{yx}=-\sigma_{xy}$.
:::
