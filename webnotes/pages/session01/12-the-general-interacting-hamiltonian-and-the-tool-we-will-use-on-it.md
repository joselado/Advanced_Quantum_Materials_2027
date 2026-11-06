## The general interacting Hamiltonian, and the tool we will use on it {#sec-1-12 number="1.12"}

We can now state the problem that this whole session leads to. The Hamiltonians that we are interested in have the generic form

$$H = \sum_{ij} t_{ij}\, c_i^\dagger c_j \;+\; \sum_{ijkl} V_{ijkl}\, c_i^\dagger c_j^\dagger c_k c_l, \tag{1.5}$$

which is a free part, single-particle and exactly solvable, plus a quartic interaction. The interaction itself can come from the plain electrostatic Coulomb repulsion, or from an effective interaction mediated by some other quasiparticle, such as phonons, magnons or plasmons, which can make the total interaction attractive instead of repulsive. We will treat these interactions in a phenomenological way, as given effective models, and we will not derive them microscopically from first principles.

To solve [(1.5)](#eq-1-5) exactly is in general impossible, for the exponential reason of Section [1.9](#sec-1-9). **Mean-field theory** is the tool that still allows us to obtain systematic solutions from it, even if they are approximate, and it can predict a wide range of symmetry-broken states. In this session we will study three of them, which are the same three cases that we classified in Section [1.11](#sec-1-11).

1.  **Broken time-reversal symmetry**, which is magnetism. If we run the movie of the system backward, it looks different from the original.

2.  **Broken (lattice translational) symmetry**, which is the charge density wave. A Hamiltonian that is the same at every site at the start ends up with charge on some sites and not on others.

3.  **Broken gauge symmetry**, which is superconductivity. The system develops an order parameter with a physical phase, which the symmetry of the original Hamiltonian does not allow.

Figure [1.3](#fig:s01:channels) shows these three branches next to each other, together with the equation from which each one is developed and the session where it appears again.

![One Hamiltonian and three ordered states. The same generic interacting Hamiltonian [(1.5)](#eq-1-5), on the left, where the glow is the interaction between two electrons on neighboring sites, is decoupled with three different bilinear expectation values. This gives a charge density wave, a magnet or a superconductor, each breaking a different symmetry. The charge is drawn as columns of alternating height, the spin as alternating arrows, and the electrons bound in pairs as two balls inside one capsule. These three branches are the structure on which the rest of the course is organized.](figures/s01f03_threechannels.svg){#fig:s01:channels number="1.3"}

Two of the three cases of this session, which are magnetism and superconductivity, will come back later in the course in their own sessions, where we treat them in much more detail. You can think of what follows as a first pass, whose goal is to set up the mean-field method itself, and not as the final discussion of either of them.

::: quiz
The quartic term of [(1.5)](#eq-1-5) has four operators, and the mean-field Hamiltonian has only two. What do we do with the other two?

- [ ] We drop them, since they are small.

    This is false. Take the Hubbard dimer. If we drop the interaction, the spectrum is $\pm t$ for every $U$, and no magnetic solution can appear. The interaction is what drives the magnetization, so it cannot be dropped.

- [x] We replace them by their expectation value in the state that we are looking for.

    This is true. The expectation value is a number, so the two operators that remain form a single-particle term. The number comes from the state itself, which is why we solve the problem self-consistently.

- [ ] We replace them by their value in the vacuum.

    This is false. In the vacuum $\langle c_i^\dagger c_j\rangle=0$ for every pair. The mean field would then vanish, and the chain would have no charge modulation, while the loop of the figure ends with charges that differ from site to site.

The self-consistent loop closes because the expectation values depend on the state that they define.
:::

::: {.tryit notebook="session1.ipynb" cell="Gap opening of the Hubbard model in a chain"}
Run the cell with the antiferromagnetic guess and watch the gap open as $U$ grows. Then use the ferromagnetic guess of the commented line. The gap stays closed, so the two guesses end in different solutions of the same Hamiltonian.
:::
