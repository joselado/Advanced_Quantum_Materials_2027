## Exercises where we guess eigenstates from symmetry only {#sec-2-4 number="2.4"}

We will now see with a sequence of small examples how much [(2.3)](#eq-2-3) gives us. In each example we add sites, and at the end we take the infinite limit.

**Three sites on a ring.** We take a tight-binding Hamiltonian on three sites in a triangle, with a symmetry $R$ that rotates $1\to2\to3\to1$ by $120^\circ$. Since $R^3=\mathbb{1}$, any eigenvalue $\lambda=e^{i\varphi}$ of $R$ must satisfy $\lambda^3=1$, so

$$\varphi_n = \frac{2\pi n}{3}, \qquad n=0,1,2. \tag{2.4}$$

So we know a lot about the eigenstates of $H$ before we write $H$ explicitly. They must have the form $\alpha_1c_1^\dagger+\alpha_2c_2^\dagger+\alpha_3c_3^\dagger$. Since $R$ permutes the sites in a cyclic way and multiplies the whole state by $e^{i\varphi_n}$, the coefficients must have the same phase from one site to the next, $\alpha_j\propto e^{i\varphi_n j}$. The eigenstates of any Hamiltonian with this rotational symmetry are the three discrete Fourier modes on the ring, regardless of the values of the hopping amplitudes. Figure [2.1](#fig:s02:ring) shows the three modes explicitly, and it also shows how the set of allowed phases changes when the ring becomes larger.

![Symmetry fixes the eigenstates before we write down the Hamiltonian. On a three-site ring the rotation $R$ can only have eigenvalues $e^{2\pi i n/3}$ by [(2.4)](#eq-2-4), and so the coefficients of the state must change by this same phase from one site to the next. This means that the eigenstates are the discrete Fourier modes, for any values of the hopping amplitudes. The arrow on each site is the complex coefficient $\alpha_j\propto e^{i\varphi_n j}$, which turns by $2\pi n/3$ from one site to the next. On the right, the balls are the allowed phases for $L=3$ and $L=5$. In the limit $L\to\infty$ they fill the circle, and this circle is the first Brillouin zone.](figures/s02f01_ringmodes.svg){#fig:s02:ring number="2.1"}

::: quiz
A ring has $L=6$ sites and a rotation $R$ with $R^6=\mathbb{1}$. How many Bloch phases $\varphi$ are allowed, and what is their spacing?

- [ ] Three, spaced by $2\pi/3$.

    This is false. The state $(1,-1,1,-1,1,-1)$ is an eigenstate of $R$ with eigenvalue $-1$, so $\varphi=\pi$. This phase is not in the list $0,\pm 2\pi/3$, which means that there are more than three.

- [x] Six, spaced by $\pi/3$.

    This is true. The eigenvalue satisfies $\lambda^6=1$, so $\varphi_n=2\pi n/6$ with $n=0,\dots,5$. As $L$ grows, the allowed phases come closer and fill the circle.

- [ ] Twelve, spaced by $\pi/6$.

    This is false. The phase $\varphi=\pi/6$ gives $\lambda^6=e^{i\pi}=-1$, which is not $1$. So this phase is not allowed on a ring of six sites.

    ![The twelve phases with spacing $\pi/6$. On a ring of six sites only the six dots satisfy $\lambda^6=1$, and the crosses give $\lambda^6=-1$.](figures/web/session02/ring_six_phases.svg){alt="A circle with twelve marks, six dots at multiples of pi over three and six crosses between them."}

The number of allowed phases equals the number of sites of the ring.
:::

**Five sites on a ring.** The same argument on a five-site ring with nearest-neighbor hopping, $H=\sum_{\langle ij\rangle} c_i^\dagger c_j$, gives $\varphi_n=2\pi n/5$, $n=0,\dots,4$, and the eigenstates $|\Psi_n\rangle \propto \sum_{j=0}^4 e^{i\varphi_n j}\,c_j^\dagger|0\rangle$. With this we can already answer a quantitative question without diagonalizing anything. Let us ask what the weight of site 1 is in the lowest-energy eigenstate built from the vacuum $|\Omega\rangle$, in the sense of the overlap $\big|\langle\Omega|c_1\Psi_{\rm GS}^\dagger|\Omega\rangle\big|^2$. Every $|\Psi_n\rangle$ is a superposition over all five sites with the same modulus on each site, so this overlap is $1/5$ for every $n$, for the lowest energy and for all other states. This follows from the symmetry only, and it does not depend on the specific hopping amplitudes. The same argument stays valid if the nearest-neighbor hopping is replaced by any long-range hopping, and a six-site ring with additional long-range couplings shows the same thing. As long as the rotational symmetry of the ring is present, the symmetry eigenvalues, the eigenstates and expectation values such as this one are all fixed by symmetry only, however complicated the Hamiltonian becomes.

![The five-site ring with $H=-t\sum_j(c_j^\dagger c_{j+1}+\text{h.c.})$, in blue, and with a second-neighbor term $-t_2\sum_j(c_j^\dagger c_{j+2}+\text{h.c.})$ added, in red, for $t_2=0.8t$. Both commute with the rotation of the ring, so both have the same five Fourier modes as eigenstates, and each mode has the weight $1/5$ on every site. Only the energies change. The blue dots lie on $-2t\cos\varphi$ and the red squares on $-2t\cos\varphi-2t_2\cos2\varphi$, the two grey curves.](figures/web/session02/ring_long_range.svg){#sch:s02:ring_long_range alt="Two pentagon rings, the second with a red star of second-neighbor bonds, and the energies of the five Fourier modes of each ring against the phase, as dots and squares on two grey curves."}

::: quiz
An eigenstate on a ring of $L$ sites is a Fourier mode. What is the weight of one site in it, for any choice of the hopping amplitudes that keep the rotation symmetry?

- [x] $1/L$

    This is true. A Fourier mode has the same modulus on every site, and the weights add up to one. So each site has the weight $1/L$, regardless of the hopping.

- [ ] It depends on the hopping amplitudes.

    This is false. Take $t=1$ and a second-neighbor hopping $\eta=0.3$ on $L=6$. The eigenstates are the same Fourier modes as for $\eta=0$, and each site has the weight $1/6$.

- [ ] It is largest on the site where the state was created.

    This is false. For $L=4$ the mode $(1,i,-1,-i)/2$ has the weight $1/4$ on every site, including the first one. All the sites are equivalent by the rotation.

The weights are equal because the rotation maps every site into every other one.
:::

Note that such models with few sites are not only of academic interest. With scanning tunnelling microscopy one can place single atoms with essentially arbitrary precision, and tight-binding rings with few sites like these have been built and measured in this way. There is a famous stop-motion film made only from atoms moved with STM, which is sometimes called "the smallest film ever made", where every dot on the screen is a single atom. It shows how accurately such models can now be realized in the lab.

**The infinite chain.** Now we let the ring grow without limit, so that it becomes an infinite one-dimensional chain with nearest-neighbor hopping. The relevant symmetry is a translation by one site, $T: c_n^\dagger \to c_{n-1}^\dagger$, which shifts a wavefunction $\psi_n$ on the sites to $\psi_{n+1}$. We have $[H,T]=0$ for any Hamiltonian whose hoppings depend only on the distance between sites and not on the absolute position. By Section [2.3](#sec-2-3), $H$ and $T$ have a common eigenbasis, and by [(2.2)](#eq-2-2) the eigenvalue of $T$ in this common eigenbasis is a pure phase $e^{i\varphi}$. This $\varphi$ is called the **Bloch phase**. Applied to a system with translational symmetry, the statement that $H$ and $T$ have a common eigenbasis *is* Bloch's theorem. The relation between this phase and the corresponding energy of the Hamiltonian is what we call the **dispersion relation** of a periodic system.

::: comesback
- Section [2.5](#sec-2-5) uses the Bloch phase to derive the first band structure, $\epsilon_\varphi=-2t\cos\varphi$.
- In Section [9.10](#sec-9-10) disorder removes the translational symmetry of this section, and the eigenstates can become localized instead of Fourier modes.
:::
