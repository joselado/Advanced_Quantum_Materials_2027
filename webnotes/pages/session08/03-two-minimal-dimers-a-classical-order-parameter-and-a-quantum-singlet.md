## Two minimal dimers, a classical order parameter and a quantum singlet {#sec-8-3 number="8.3"}

The simplest way to start with quantum magnetism is to look first at the smallest possible magnet, which has two spins, and to compare two different Hamiltonians for it.

The first one is the **Ising dimer**,

$$\mathcal H_\text{Ising} = S_0^z S_1^z, \tag{8.1}$$

which couples only the $z$-components of two spin-$1/2$'s. This Hamiltonian has two degenerate ground states, which are related by time reversal.

$$|GS_1\rangle = |{\uparrow\downarrow}\rangle, \qquad |GS_2\rangle = |{\downarrow\uparrow}\rangle.$$

Both are eigenstates with the same energy, but each one of them *alone* breaks time-reversal symmetry, since time reversal flips every spin and so it turns $|GS_1\rangle$ into $|GS_2\rangle$ and the other way around. Only the degenerate pair of the two states together respects the symmetry. A macroscopic symmetry-broken antiferromagnet, of the same kind as the one we built in Session 6, is the version of this same problem with an infinite number of sites, and the same argument also works for ferromagnets and spin spirals.

Let us now replace the Ising coupling by the full **quantum Heisenberg dimer**, which has rotational symmetry,

$$\mathcal H_\text{Heis} = \mathbf S_0 \cdot \mathbf S_1. \tag{8.2}$$

This is the model that we obtain from a half-filled Hubbard model with strong interactions in the large-$U$ limit, as we derived in Session 6. When we solve it with $\mathbf S_0, \mathbf S_1$ as real spin-$1/2$ operators, the two spin-$1/2$'s combine into a singlet ($S=0$) and a triplet ($S=1$). The value is $\mathbf S_0\cdot\mathbf S_1 = -3/4$ for the singlet and $+1/4$ for the triplet, so the unique ground state is the **singlet**,

$$|GS\rangle = \frac{1}{\sqrt2}\Big(|{\uparrow\downarrow}\rangle -
|{\downarrow\uparrow}\rangle\Big), \qquad \langle \mathbf S_i \rangle = 0. \tag{8.3}$$

This ground state is different from the Ising case in three ways, and these three points are important for the rest of the session. First, it is the *unique* ground state, so there is no degeneracy and no spontaneous choice between states. Second, it is *time-reversal symmetric*, since its net magnetization is exactly zero and time reversal maps $|GS\rangle$ to itself. Third, it is *maximally entangled*, since the two terms in [(8.3)](#eq-8-3) have the same weight, which is the largest entanglement that two qubits can have. Can we have a macroscopic version of this ground state? This question is the origin of quantum spin liquids.

![Where the Heisenberg dimer comes from. With parallel spins the hop of an electron is blocked by the Pauli principle, which the cross shows. With antiparallel spins the electron can hop to the neighbor and come back, and this virtual process lowers the energy of the singlet. Look at the lower part of the figure, since this process is the origin of the antiferromagnetic coupling $J$ of [(8.2)](#eq-8-2).](figures/s06f02_dimer.svg){panel="a" alt="Two sites with parallel spins, where the hop is forbidden, and with antiparallel spins, where the hop is allowed."}

::: quiz
What is the energy of the state $|{\uparrow\downarrow}\rangle$ of the Ising dimer [(8.1)](#eq-8-1)?

- [ ] $-3/4$, which is the energy of the singlet.

    This is false. The Ising dimer [(8.1)](#eq-8-1) only has $S^z_0S^z_1=\pm\tfrac14$, so its energies are $\pm1/4$. The value $-3/4$ needs the $x$ and $y$ terms of the Heisenberg dimer.

- [x] $-1/4$, since $S^z_0S^z_1=(\tfrac12)(-\tfrac12)$.

    This is true. The product of the two $z$ components is $-1/4$ for antiparallel spins and $+1/4$ for parallel ones. The two antiparallel states are degenerate, and each symmetry-broken state chooses one of them.

- [ ] $+1/4$, since the spins are antiparallel.

    This is false. The state $|{\uparrow\uparrow}\rangle$ has $S^z_0S^z_1=+\tfrac14$, and it is the one with energy $+1/4$. For antiparallel spins the product is $(\tfrac12)(-\tfrac12)=-\tfrac14$.
:::

::: quiz
We change the sign of the coupling, $H=J\,\mathbf S_0\cdot\mathbf S_1$ with $J<0$. What is the ground state of the dimer?

- [ ] The singlet, as for $J>0$.

    This is false. Take $J=-1$. The singlet has energy $-3J/4=+3/4$ and the triplet has $J/4=-1/4$, so the triplet is lower.

- [ ] A single state $|{\uparrow\uparrow}\rangle$ that breaks time-reversal symmetry.

    This is false. The Hamiltonian commutes with the total spin, so $|{\downarrow\downarrow}\rangle$ and $(|{\uparrow\downarrow}\rangle+|{\downarrow\uparrow}\rangle)/\sqrt2$ have the same energy $J/4$. The ground state is threefold degenerate and not a single state.

- [x] The triplet, which is threefold degenerate.

    This is true. The value of $\mathbf S_0\cdot\mathbf S_1$ is $-3/4$ for the singlet and $+1/4$ for the triplet. For $J<0$ the energy $J/4$ of the triplet is below $-3J/4$ of the singlet, and the three triplet states are degenerate.
:::
