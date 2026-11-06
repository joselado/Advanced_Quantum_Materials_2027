## Weakly versus strongly correlated matter, revisited {#sec-5-1 number="5.1"}

Before we specialize, let us state again the general setting, since it is useful to have it clearly in mind. Every interacting Hamiltonian that we consider in this course has the same general form,

$$H = \sum_{ij} t_{ij}\, c_i^\dagger c_j \;+\; \sum_{ijkl} V_{ijkl}\, c_i^\dagger c_j^\dagger c_k c_l,$$

which is a free bilinear part plus a quartic interaction, and it is exactly eq. [1.5](#eq-1-5) of session 1. When mean-field theory can turn the quartic term into a good effective bilinear Hamiltonian, we call the resulting state *weakly correlated matter*. This includes magnets, charge density waves and superconductors, which are all the states that we built in session 1. When no single-particle mean-field Hamiltonian of this kind describes the physics, we have *strongly correlated matter*, and we need exact or numerical solutions instead. The fractional quantum Hall state from the quantum-Hall session is our main example of this harder case.

![The three weakly correlated states of session 1. Each one is a mean-field decoupling of the same quartic interaction, and the superconductor on the right is the one of this session.](figures/s01f03_threechannels.svg){alt="A generic interacting Hamiltonian on the left, and three ordered states on the right, a charge density wave, a magnet and a superconductor."}

Note that superconductors and the fractional quantum Hall state are at opposite ends of this classification, even though both of them in the end host fractional excitations. A superconductor has a mean-field description, comes from an *attractive* interaction, is destroyed by a magnetic field and, as we will see soon, hosts Majorana states. The fractional quantum Hall state has no mean-field description, comes from strong *repulsive* interactions, usually needs a strong magnetic field and hosts excitations with fractional charge. Roughly speaking, both Majorana excitations and fractional quantum Hall excitations are a fraction of an electron, but these fractions come from completely different mechanisms. This is one of the good examples in this course of how very different microscopic physics can lead to the same qualitative phenomenon, which is emergent fractionalization, while the mechanism behind it is not the same at all.

::: quiz
A superconductor and a fractional quantum Hall state both host excitations that are a fraction of an electron. Which statement separates their origin?

- [ ] Both come from attractive interactions, and only the magnetic field is different.

    This is false. Take the fractional quantum Hall state at filling 1/3. It has no pairing term and no attraction, and the fractional charge $e/3$ appears from strong repulsion alone.

- [x] The superconductor has a mean-field description and needs attraction, while the quantum Hall state has none and needs strong repulsion.

    This is true. In a superconductor the quartic term becomes the bilinear pairing term [(5.4)](#eq-5-4), so a single-particle Hamiltonian describes the state. The quantum Hall state has no such Hamiltonian.

- [ ] Neither of them has a mean-field description, since both host fractional excitations.

    This is false. The Bogoliubov quasiparticle of a superconductor is a fraction of an electron, and it is an exact eigenstate of the mean-field Hamiltonian [(5.4)](#eq-5-4). So fractional excitations alone do not rule out a mean-field description.
:::
