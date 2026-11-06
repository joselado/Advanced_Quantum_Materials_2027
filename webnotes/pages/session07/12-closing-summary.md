## Closing summary {#sec-7-12 number="7.12"}

- Strongly correlated matter, including quantum spin liquids and fractional Chern insulators, is the regime where the mean-field methods of sessions 1 to 6 have no order parameter to converge to, as we saw with [(7.1)](#eq-7-1) and in Section [7.1](#sec-7-1).

- The **Jordan-Wigner transformation** [(7.2)](#eq-7-2) is an exact mapping between fermionic and spin-1/2 Hamiltonians, summarized as "spin equals fermion times string." It is the link between the fermionic language of sessions 1-5 and the spin language of sessions 6 and 8, and it is the reason why we can work in the spin representation for the rest of the session.

- The real obstruction to solving many-body Hamiltonians is **storage**, since a system of $L$ spins needs $2^L$ coefficients [(7.4)](#eq-7-4) to describe its wave function exactly.

- The **matrix product state** ansatz [(7.5)](#eq-7-5) replaces these $2^L$ coefficients with $O(LM^2)$ parameters, so we give up exactness in exchange for an approximation that we control with the bond dimension $M$.

- The **entanglement entropy** [(7.6)](#eq-7-6), which we computed for the singlet in [(7.7)](#eq-7-7), measures how entangled a state is. Exactly solvable dimer and tetramer models show that gapped ground states follow an **area law** [(7.9)](#eq-7-9), with an entropy set by the length of the boundary and not by the volume of the subsystem.

- The entanglement of an MPS is itself bounded, $S \le \log M$ [(7.10)](#eq-7-10). This is the reason why MPS work so well in 1D, where the area law saturates, and why they need an exponentially large $M$ in higher dimensions or away from the ground state.

- Ground states are found variationally, by minimizing [(7.11)](#eq-7-11) one tensor at a time, and this sweeping procedure is the **DMRG** algorithm. **MERA** and **PEPS** extend the idea of tensor networks to criticality, through the logarithmic correction to the entropy [(7.12)](#eq-7-12), and to real 2D lattices, respectively. MERA can still be optimized tensor by tensor, while for PEPS the contraction is the hard step, so the simple local optimization of DMRG is lost.

- Neural network quantum states were mentioned once, together with tensor networks, as a second answer to the same storage problem, but they were not developed in this session. In session 10 we will study them in detail from the point of view of machine learning, and we will also come back to the MPS, MERA and PEPS methods of this session as architectures for machine-learning classifiers.

![The summary of the session in one picture. Look at where the gapped curve, the critical curve and the volume law meet the horizontal bars set by $M$, since this is where an MPS of that bond dimension stops being enough.](figures/s07f03_entropyceiling.svg){alt="Entropy against the size of the subsystem for a gapped, a critical and a generic state, with horizontal bars for two bond dimensions."}

::: quiz
An MPS with $M=20$ describes a gapped chain of 200 sites very well. We now move to a gapped model on a $20\times20$ lattice. What do we expect?

- [ ] The same $M$ is enough, since the model is gapped.
- [x] The same $M$ is not enough, since the boundary grows with the width.
- [ ] A smaller $M$ is enough, since there are more neighbors.
- [ ] The MPS fails only because there are more sites.

A gapped state obeys the area law in both cases, but in two dimensions the boundary has 20 bonds and not one. The entropy grows in proportion, and the bond dimension that it needs grows exponentially.
:::
