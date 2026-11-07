## Closing summary {#sec-1-16 number="1.16"}

This session needed nothing from before except the Schrödinger equation of a single particle, which we wrote in two ways in Section [1.4](#sec-1-4). From it we built the language and the first tool of the course, and we saw the following.

- Quantum materials realize a very large range of phenomena, such as topological order, fractionalization and correlated superconductivity, that no single atom shows on its own. The central question of this course is how these phenomena emerge from electrons in a lattice.

- **Second quantization** is a language that treats in the same way systems with a fixed number of particles and systems where this number fluctuates. It is built from creation and annihilation operators that satisfy the anticommutation relations [(1.3)](#eq-1-3).

- The many-body Hilbert space grows as $2^L$, as we saw in Section [1.9](#sec-1-9). For this reason interacting problems need a systematic approximation and not brute-force diagonalization.

- **Spontaneous symmetry breaking** is the general phenomenon where a symmetric Hamiltonian gives an asymmetric ground state in the thermodynamic limit. We can classify states of matter by the symmetry that they break, which is time reversal for magnets, inversion for ferroelectrics and gauge symmetry for superconductors, and each case has its own emergent quasiparticle. A magnet has the formal definition of [(1.4)](#eq-1-4). Topological materials show that this classification does not cover all cases.

- **Mean-field theory** gives the practical method. We factorize the interacting Hamiltonian [(1.5)](#eq-1-5) by taking an expectation value of part of the quartic term, and then we solve the resulting single-particle problem self-consistently.

- The same procedure, applied to three different interaction channels, gives three different symmetry-broken states. The first is a charge density wave from [(1.6)](#eq-1-6), with broken translational symmetry. The second is a magnet from [(1.7)](#eq-1-7) and [(1.8)](#eq-1-8), with broken time-reversal symmetry. The third is a superconductor from [(1.9)](#eq-1-9) and [(1.10)](#eq-1-10), with broken gauge symmetry. Superconductivity has its own full session in Session 5 and magnetism in Session 6, and the versions of this session are a first pass.

![The three channels of this session, shown again. The same Hamiltonian gives a charge density wave, a magnet and a superconductor, and each one breaks a different symmetry.](figures/s01f03_threechannels.svg){alt="One interacting Hamiltonian on the left and three ordered states on the right, a charge density wave, a magnet and a superconductor."}

::: quiz
Why does a mean-field superconductor not have a fixed number of electrons?

- [x] The order parameter has a physical phase, so the gauge symmetry is broken, and this symmetry is the conservation of the particle number.

    This is true. Once $\Delta\neq 0$ it changes under the gauge transformation, and the number is not fixed anymore. Only its parity survives.

- [ ] The attractive interaction lets electrons escape from the sample.

    This is false. An isolated superconducting island has a fixed number of electrons in total, and the mean-field state still has $\Delta\neq 0$. The state is a superposition of $N$, $N+2$ and $N-2$ electrons, with no electrons leaving.

- [ ] A superconductor breaks time-reversal symmetry.

    This is false. A conventional s-wave superconductor such as aluminum has a real $\Delta$ and keeps time-reversal symmetry. Its number of electrons is still not fixed.

The phase of $\Delta$ and the number of electrons are conjugate, so a fixed phase means an uncertain number.
:::

::: comesback
- In Session 2 the single-particle part of [(1.5)](#eq-1-5) is diagonalized without any approximation, with Bloch's theorem in Section [2.5](#sec-2-5).
- Session 5 starts again from the pairing term [(1.9)](#eq-1-9), and Section [5.6](#sec-5-6) comes back to the fluctuating number of electrons of Section [1.5](#sec-1-5).
- Session 6 recaps the logic of symmetry breaking in Section [6.2](#sec-6-2) and solves the magnet of [(1.7)](#eq-1-7) again in Section [6.3](#sec-6-3).
- The charge density wave comes back in Section [9.4b](#sec-9-4b) as the Peierls instability, driven by nesting.
- The limit $2^L$ of Section [1.9](#sec-1-9) is where the tensor networks of Session 7 start, and Section [10.6](#sec-10-6) compares the local order parameters of this session with topological order.
:::
