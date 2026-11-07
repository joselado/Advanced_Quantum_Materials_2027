## Closing summary {#sec-7-12 number="7.12"}

We started from three things that we built before. These were the general interacting Hamiltonian and the mean-field method of Section [1.12](#sec-1-12), the Heisenberg model [(6.5)](#eq-6-5) of Session 6, and the frustrated magnets of Section [6.10](#sec-6-10), where no order parameter appears. In this session we saw the following.

- Strongly correlated matter, which includes quantum spin liquids and fractional Chern insulators, is the regime where mean field has no order parameter to converge to. We saw this with [(7.1)](#eq-7-1) in Section [7.1](#sec-7-1).

- The **Jordan-Wigner transformation** [(7.2)](#eq-7-2) is an exact mapping between fermionic and spin-1/2 Hamiltonians, and in short spin equals fermion times string. It links the fermionic language of Sessions 1 to 5 with the spin language of Session 6 and Session 8. For this reason we could work in the spin representation for the rest of the session.

- The real obstruction to solving many-body Hamiltonians is **storage**, since a system of $L$ spins needs $2^L$ coefficients [(7.4)](#eq-7-4) to describe its wave function exactly.

- The **matrix product state** ansatz [(7.5)](#eq-7-5) replaces these $2^L$ coefficients with $O(LM^2)$ parameters. We give up exactness and get an approximation that we control with the bond dimension $M$.

- The **entanglement entropy** [(7.6)](#eq-7-6), which we computed for the singlet in [(7.7)](#eq-7-7), measures how entangled a state is. Exactly solvable dimer and tetramer models show that gapped ground states follow an **area law** [(7.9)](#eq-7-9), with an entropy set by the length of the boundary and not by the volume of the subsystem.

- The entanglement of an MPS is itself bounded, $S \le \log M$ [(7.10)](#eq-7-10). This is the reason why MPS work so well in 1D, where the area law saturates, and why they need an exponentially large $M$ in higher dimensions or away from the ground state.

- Ground states are found variationally, by minimizing [(7.11)](#eq-7-11) one tensor at a time, and this sweeping procedure is the **DMRG** algorithm.

- **MERA** extends tensor networks to criticality, through the logarithmic correction to the entropy [(7.12)](#eq-7-12), and **PEPS** extend them to real 2D lattices. MERA can still be optimized tensor by tensor. For PEPS the contraction is the hard step, so the simple local optimization of DMRG is lost.

- Neural network quantum states are a second answer to the same storage problem, and we did not develop them in this session.

![The summary of the session in one picture. Look at where the gapped curve, the critical curve and the volume law meet the horizontal bars set by $M$, since this is where an MPS of that bond dimension stops being enough.](figures/s07f03_entropyceiling.svg){alt="Entropy against the size of the subsystem for a gapped, a critical and a generic state, with horizontal bars for two bond dimensions."}

::: quiz
An MPS with $M=20$ describes a gapped chain of 200 sites very well. We now move to a gapped model on a $20\times20$ lattice. What do we expect?

- [ ] The same $M$ is enough, since the model is gapped.

    This is false. Being gapped fixes the entropy per bond. The cut of the $20\times20$ lattice crosses 20 bonds, so the entropy is about 20 times larger and the needed $M$ is of the order of $20^{20}\approx10^{26}$.

- [x] The same $M$ is not enough, since the boundary grows with the width.

    This is true. A gapped state obeys the area law in both cases, but in two dimensions the boundary has 20 bonds and not one. The entropy grows in proportion, and the bond dimension that it needs grows exponentially.

- [ ] The MPS fails only because there are more sites.

    This is false. A gapped chain of 2000 sites needs the same $M=20$ as the one of 200, so the number of sites alone does not matter. A $20\times20$ lattice has just 400 sites.
:::

::: comesback
- In Session 8 the singlet [(7.3)](#eq-7-3) becomes the resonating valence bond state of a frustrated lattice, in Section [8.6](#sec-8-6), and the dimerized chain comes back as the valence bond solid of Section [8.5](#sec-8-5).
- In Section [10.3](#sec-10-3) neural network quantum states replace the table of $2^L$ coefficients, and they are trained with the variational energy as the loss.
- In Section [10.4](#sec-10-4) the MPS, MERA and PEPS of this session are used as architectures for machine-learning classifiers.
:::
