## Frustration as the route to a quantum spin liquid {#sec-8-4 number="8.4"}

Before we build a macroscopic version of [(8.3)](#eq-8-3), we need to know when the ground state of a Heisenberg model stays time-reversal symmetric in this way. The magnets of Session 1 and Session 6 did not, since they ordered spontaneously. The general rule is **frustration**, which we first met in Section [6.10](#sec-6-10). The standard example is a triangular plaquette with antiferromagnetic coupling on all three bonds. Any two spins can point in opposite directions, but then the third spin is parallel to one of the two. So one of the two remaining bonds is not satisfied, and no spin configuration can satisfy all three bonds at the same time. This geometric frustration gives many classical ground states that are degenerate, which means that they have the same energy and different spin configurations. When we add quantum fluctuations, they mix these degenerate configurations into one quantum superposition, which in general does not break time-reversal symmetry.

This is the reason why the **triangular** and **kagome** lattices, which are both built only from triangles, are the standard place to look for quantum spin liquid physics. An antiferromagnetic Heisenberg model on either lattice is a real candidate for a QSL ground state, in the right range of couplings. This is also the reason why herbertsmithite, a compound with spin-$1/2$ sites on a kagome lattice, is the main real candidate material. A second route to frustration, from the bond-dependent Kitaev interaction on the honeycomb lattice, is in Section [6.12](#sec-6-12). Figure [8.2](#fig:s08:frustration) shows the geometry behind the whole argument. It is a frustrated triangle with its degenerate configurations, and the kagome lattice that is built only from such triangles. The plaquette without frustration and the single frustrated triangle are the ones of Figure [6.3](#fig:s06:frustration).

![Frustration, with the spins drawn as collinear Ising variables, which is how the argument in the text is written. If the spins can rotate freely, the triangle goes instead into the $120^\circ$ noncollinear state of Figure [6.3](#fig:s06:frustration), and the degeneracy that we discuss here is the Ising one. The plaquette without frustration and the single frustrated triangle are panels (a) and (b) of Figure [6.3](#fig:s06:frustration). On a bipartite plaquette every antiferromagnetic bond can be satisfied at the same time. The ground state is then the Néel state, with two configurations related by a global flip, and each of them breaks time-reversal symmetry. On a triangle this is not possible, since once two spins are antiparallel the third bond cannot be satisfied for both directions of the last spin. (a) The frustrated bond, in red, can be on any of the three edges, so the classical ground state is degenerate and not unique. Quantum fluctuations mix the degenerate configurations into one superposition with $\langle\mathbf
S_i\rangle=\mathbf 0$, which does *not* break time-reversal symmetry. (b) The kagome lattice of herbertsmithite is built only from corner-sharing triangles, so all of them are frustrated at the same time, here with one frustrated bond on every triangle. The classical degeneracy then becomes macroscopic. This is why triangular and kagome lattices are the standard place to look for quantum spin liquids.](figures/s08f02_frustration.svg){#fig:s08:frustration number="8.2"}

![How large the classical degeneracy is. We count by brute force the ground states of the antiferromagnetic Ising model on small periodic clusters of $N$ sites. On the square lattice there are always two, the two Néel states. On the triangular and kagome lattices the number grows exponentially with $N$. The dashed lines have the slopes $0.32$ and $0.50$, which are the entropies per site of the infinite lattices. This is what a macroscopic degeneracy means, and quantum fluctuations mix the states of this large set.](figures/web/session08/ising_degeneracy.svg){#sch:s08:ising_degeneracy alt="The logarithm of the number of Ising ground states against the number of sites, flat at ln 2 for the square lattice and rising along two dashed lines for the triangular and kagome lattices."}

::: quiz
Three Ising spins sit on a triangle with antiferromagnetic bonds. How many of the 8 configurations are classical ground states?

- [ ] 2, the two Néel-like configurations.

    This is false. There is no Néel configuration on a triangle. The state $\uparrow\downarrow\uparrow$ has one unsatisfied bond, with energy $-1/4$, and so do its five partners, so there are six degenerate states and not two.

    ![The eight Ising configurations of an antiferromagnetic triangle. A red bond joins two parallel spins and costs energy. Six configurations have one red bond and the lowest energy.](figures/web/session08/triangle_configs.svg){alt="Eight triangles with an arrow up or down on each corner, red bonds between parallel spins, and the energies minus one quarter for six of them and plus three quarters for two."}

- [x] 6, the ones with exactly one unsatisfied bond.

    This is true. The two fully aligned configurations have three unsatisfied bonds and energy $+3/4$. Each of the other six has one unsatisfied bond and energy $-1/4$, which is the minimum, so the ground state is sixfold degenerate.

- [ ] 3, one for each bond.

    This is false. The unsatisfied bond can be any of the three, but for each choice there are two states, the configuration and its spin flip. So $\uparrow\uparrow\downarrow$ and $\downarrow\downarrow\uparrow$ are both ground states, giving 6.
:::

::: quiz
Why is the square lattice with antiferromagnetic Heisenberg coupling not a good place to look for a spin liquid?

- [x] It is bipartite, so the Néel state satisfies every bond and breaks time-reversal symmetry.

    This is true. On a bipartite lattice all bonds are satisfied at the same time by two sublattices of opposite spin. There is then no frustration and no macroscopic degeneracy for the quantum fluctuations to mix.

    ![Look at panel (a), where all bonds of the bipartite plaquette are satisfied.](figures/s06f03_frustration.svg){alt="Three plaquettes, a bipartite one where every bond is satisfied, a frustrated triangle, and the 120 degree state."}

- [ ] It has too many neighbors for singlets to form.

    This is false. The kagome lattice also has four neighbors, like the square lattice, and it is a leading candidate for a spin liquid. The number of neighbors is not what decides it.

- [ ] It is two-dimensional, and spin liquids need three dimensions.

    This is false. The triangular and kagome lattices are two-dimensional and they are the standard places to look for spin liquids. Frustration and not the dimension is what matters.
:::

::: comesback
- In Section [8.6](#sec-8-6) quantum fluctuations mix the degenerate coverings of a frustrated lattice into the resonating valence bond state.
- In Section [9.9](#sec-9-9) a frustrated Heisenberg model with a ground state close to a spin liquid is probed with a local magnetic impurity.
:::
