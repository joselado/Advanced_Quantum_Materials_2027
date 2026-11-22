## Weakly versus strongly correlated matter, revisited {#sec-5-1 number="5.1"}

Why does a superconductor have a mean-field description, while the fractional quantum Hall state needs exact methods? We will now see that interacting matter splits into weakly and strongly correlated matter. The superconductor comes from an attractive interaction, and it is on the weak side.

Before we specialize, let us state again the general setting, since it is useful to have it clearly in mind. Every interacting Hamiltonian that we consider in this course has the same general form,

$$H = \sum_{ij} t_{ij}\, c_i^\dagger c_j \;+\; \sum_{ijkl} V_{ijkl}\, c_i^\dagger c_j^\dagger c_k c_l,$$

which is a free bilinear part plus a quartic interaction, and it is equation [(1.5)](#eq-1-5) of Session 1. When mean-field theory can turn the quartic term into a good effective bilinear Hamiltonian, we call the resulting state *weakly correlated matter*. This includes magnets, charge density waves and superconductors, which are all the states that we built in Session 1. When no single-particle mean-field Hamiltonian of this kind describes the physics, we have *strongly correlated matter*, and we need exact or numerical solutions instead. The fractional quantum Hall state of Section [4.16](#sec-4-16) is our main example of this harder case.

![The three weakly correlated states of Session 1. Each one is a mean-field decoupling of the same quartic interaction, and the superconductor on the right is the one of this session.](figures/s01f03_threechannels.svg){alt="A generic interacting Hamiltonian on the left, and three ordered states on the right, a charge density wave, a magnet and a superconductor."}

Note that superconductors and the fractional quantum Hall state are at opposite ends of this classification, even though both of them in the end host fractional excitations. A superconductor has a mean-field description, comes from an *attractive* interaction, is destroyed by a magnetic field and, as we will see soon, hosts Majorana states. The fractional quantum Hall state has no mean-field description, comes from strong *repulsive* interactions, usually needs a strong magnetic field and hosts excitations with fractional charge. Roughly speaking, both Majorana excitations and fractional quantum Hall excitations are a fraction of an electron, but these fractions come from completely different mechanisms. This is a good example of how very different microscopic physics can lead to the same qualitative phenomenon, which is emergent fractionalization. The mechanism behind it is not the same at all.

::: quiz
Two states host excitations that are a fraction of an electron. They are a superconductor and a fractional quantum Hall state. Which statement separates their origin?

- [ ] Both come from attractive interactions, and only the magnetic field is different.

    This is false. Take the fractional quantum Hall state at filling 1/3. It has no pairing term and no attraction, and the fractional charge $e/3$ appears from strong repulsion alone.

- [x] The superconductor has a mean-field description and needs attraction, while the quantum Hall state has none and needs strong repulsion.

    This is true. In a superconductor the quartic term becomes the bilinear pairing term [(5.4)](#eq-5-4), so a single-particle Hamiltonian describes the state. The quantum Hall state has no such Hamiltonian.

- [ ] Neither of them has a mean-field description, since both host fractional excitations.

    This is false. The Bogoliubov quasiparticle of a superconductor is a fraction of an electron, and it is an exact eigenstate of the mean-field Hamiltonian [(5.4)](#eq-5-4). So fractional excitations alone do not rule out a mean-field description.
:::

::: quiz
The onsite interaction is $U n_\uparrow n_\downarrow$, with $n_\sigma=c_\sigma^\dagger c_\sigma$. Mean-field theory keeps one expectation value in each term. Which term gives a superconductor?

- [ ] $U\langle c_\uparrow^\dagger c_\uparrow\rangle\, c_\downarrow^\dagger c_\downarrow$

    This is false. The term has one creation and one annihilation operator, so it keeps the number of electrons. On one site with $U=2$ and $\langle c_\uparrow^\dagger c_\uparrow\rangle=0.8$ it only moves the spin-down level up by $1.6$, and $\langle c_\downarrow c_\uparrow\rangle$ stays zero. This channel gives a charge density wave or a magnet.

- [ ] $-U\langle c_\uparrow^\dagger c_\downarrow\rangle\, c_\downarrow^\dagger c_\uparrow$

    This is false. The term flips a spin and keeps the number of electrons, so $\langle c_\downarrow c_\uparrow\rangle$ stays zero. This channel gives a magnet with its moment in the $xy$ plane.

- [x] $U\langle c_\downarrow c_\uparrow\rangle\, c_\uparrow^\dagger c_\downarrow^\dagger$

    This is true. The operator $c_\uparrow^\dagger c_\downarrow^\dagger$ creates two electrons, so the term changes the number of electrons by two. With $\Delta=U\langle c_\downarrow c_\uparrow\rangle$ it is the pairing term $\Delta\, c_\uparrow^\dagger c_\downarrow^\dagger$ of a superconductor.

The three terms come from the same quartic term, and the expectation value that we keep decides which ordered state we get.
:::

::: comesback
- In Section [6.3](#sec-6-3) the same quartic term, decoupled in the density channel with $U>0$, gives the magnets of Session 6.
- In Section [7.1](#sec-7-1) the same division into weakly and strongly correlated matter opens the study of tensor networks, which are made for the strongly correlated side.
- In Section [8.9](#sec-8-9) a quantum spin liquid, which has no mean-field description in terms of electrons, gets one in terms of spinons.
:::
