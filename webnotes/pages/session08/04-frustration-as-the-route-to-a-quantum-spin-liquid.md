## Frustration as the route to a quantum spin liquid {#sec-8-4 number="8.4"}

When can the ground state of a Heisenberg magnet avoid magnetic order? We will now see that the route is frustration, meaning that no spin configuration satisfies every bond at the same time. For Ising spins on the triangular and kagome lattices this gives a number of classical ground states that grows exponentially with the number of sites, and this large set is what quantum fluctuations can mix.

::: {.recall eq="8.3"}
This is the singlet of two spins one half, the ground state of the Heisenberg dimer $J\,\mathbf S_0\cdot\mathbf S_1$ with $J>0$, at the energy $-3J/4$. It is unique and has $\langle\mathbf S_i\rangle=0$ on both sites. Time reversal maps it to itself, so it does not break time-reversal symmetry. In this section we ask when a lattice of many spins can have a ground state of this kind.
:::

Before we build a macroscopic version of [(8.3)](#eq-8-3), we need to know when the ground state of a Heisenberg model stays time-reversal symmetric in this way. The magnets of Session 1 and Session 6 did not, since they ordered spontaneously. The general rule is **frustration**, which we first met in Section [6.10](#sec-6-10). The standard example is a triangular plaquette with antiferromagnetic coupling on all three bonds. Any two spins can point in opposite directions, but then the third spin is parallel to one of the two. So one of the two remaining bonds is not satisfied, and no spin configuration can satisfy all three bonds at the same time.

::: {.steps title="Counting the ground states of the triangle"}
Let us take the simplest case first, two Ising spins $S^z_0,S^z_1=\pm\tfrac12$ with one bond, $H=J\,S^z_0S^z_1$. We write $M=S^z_0+S^z_1$ for the total $S^z$. Since $(S^z_i)^2=\tfrac14$ for every spin,

$$M^2=\frac12+2\,S^z_0S^z_1, \qquad\text{so}\qquad H=\frac J2\Big(M^2-\frac12\Big).$$

The energy depends only on $M$. It is lowest for $M=0$, the two antiparallel states at $-J/4$, and the bond is satisfied.

On the triangle every pair of sites is a bond, so the same step works with three spins and $M=S^z_0+S^z_1+S^z_2$,

$$M^2=\frac34+2\sum_{\langle ij\rangle}S^z_iS^z_j, \qquad\text{so}\qquad H=\frac J2\Big(M^2-\frac34\Big).$$

Three spins one half cannot have $M=0$, since $M$ is a sum of three half-integers. The lowest value is $|M|=\tfrac12$, with two spins up and one down, or the opposite. Each case has 3 configurations, one for each position of the minority spin, so there are $3+3=6$ ground states at $\frac J2\big(\frac14-\frac34\big)=-\frac J4$. The two aligned configurations have $M=\pm\tfrac32$ and the energy $\frac J2\big(\frac94-\frac34\big)=+\frac34J$. Three satisfied bonds would give $3\cdot(-\tfrac J4)=-\tfrac34J$, and no configuration reaches it.
:::

This geometric frustration gives many classical ground states that are degenerate, which means that they have the same energy and different spin configurations. When we add quantum fluctuations, they mix these degenerate configurations into one quantum superposition, which in general does not break time-reversal symmetry.

This is the reason why the **triangular** and **kagome** lattices, which are both built only from triangles, are the standard place to look for quantum spin liquid physics. An antiferromagnetic Heisenberg model on either lattice is a real candidate for a QSL ground state, in the right range of couplings. This is also the reason why herbertsmithite, a compound with spin-$1/2$ sites on a kagome lattice, is the main real candidate material. A second route to frustration, from the bond-dependent Kitaev interaction on the honeycomb lattice, is in Section [6.12](#sec-6-12). Figure [8.2](#fig:s08:frustration) shows the geometry behind the whole argument. It is a frustrated triangle with its degenerate configurations, and the kagome lattice that is built only from such triangles. The plaquette without frustration and the single frustrated triangle are the ones of Figure [6.3](#fig:s06:frustration).

![Frustration, with the spins drawn as collinear Ising variables, which is how the argument in the text is written. If the spins can rotate freely, the triangle goes instead into the $120^\circ$ noncollinear state of Figure [6.3](#fig:s06:frustration), and the degeneracy that we discuss here is the Ising one. The plaquette without frustration and the single frustrated triangle are panels (a) and (b) of Figure [6.3](#fig:s06:frustration). On a bipartite plaquette every antiferromagnetic bond can be satisfied at the same time. The ground state is then the Néel state, with two configurations related by a global flip, and each of them breaks time-reversal symmetry. On a triangle this is not possible, since once two spins are antiparallel the third bond cannot be satisfied for both directions of the last spin. (a) The frustrated bond, in red, can be on any of the three edges, so the classical ground state is degenerate and not unique. Quantum fluctuations mix the degenerate configurations. The three spins one half of one triangle keep a fourfold ground level, and with an even number of sites the mixing can give one superposition with $\langle\mathbf S_i\rangle=\mathbf 0$, which does *not* break time-reversal symmetry. (b) The kagome lattice of herbertsmithite is built only from corner-sharing triangles, so all of them are frustrated at the same time, here with one frustrated bond on every triangle. The classical degeneracy then becomes macroscopic. This is why triangular and kagome lattices are the standard place to look for quantum spin liquids.](figures/s08f02_frustration.svg){#fig:s08:frustration number="8.2"}

::: key
On a triangle of Ising spins with antiferromagnetic bonds, no configuration satisfies all three bonds, and six of the eight configurations are ground states. On a lattice built from triangles this degeneracy becomes macroscopic, meaning that the number $W$ of classical ground states of $N$ sites grows exponentially,

$$W\sim e^{sN}, \qquad s\approx0.32 \ \text{(triangular)}, \qquad s\approx0.50 \ \text{(kagome)},$$

while the square lattice, which is bipartite, has only the two Néel states.
:::

[](#sch:s08:ising_degeneracy) shows this count on small periodic clusters.

![How large the classical degeneracy is. We count by brute force the ground states of the antiferromagnetic Ising model on small periodic clusters of $N$ sites. On the square lattice there are always two, the two Néel states. On the triangular and kagome lattices the number grows exponentially with $N$. The dashed lines have the slopes $0.32$ and $0.50$, which are the entropies per site of the infinite lattices. This is what a macroscopic degeneracy means, and quantum fluctuations mix the states of this large set.](figures/web/session08/ising_degeneracy.svg){#sch:s08:ising_degeneracy alt="The logarithm of the number of Ising ground states against the number of sites, flat at ln 2 for the square lattice and rising along two dashed lines for the triangular and kagome lattices."}

::: {.lab ours="6000"}
In the kagome antiferromagnet ZnCu$_3$(OH)$_6$Cl$_2$, with spin-$1/2$ sites, the magnetic susceptibility gives a Curie-Weiss temperature of about $-300$ K, and no magnetic order is observed down to $50$ mK. The measurement is in [this article](https://doi.org/10.1103/PhysRevLett.98.107204). What follows is our own reading. The size of the Curie-Weiss temperature is set by the antiferromagnetic exchange, and in mean field a magnet without frustration orders at a temperature of this order. Here the order is still absent at a temperature about $6000$ times lower, which fits a lattice made only of frustrated triangles.
:::

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
We take the Heisenberg model on the square lattice,

$$H=J\sum_{\langle ij\rangle}\mathbf S_i\cdot\mathbf S_j, \qquad J>0.$$

Why is it not a good place to look for a spin liquid?

- [x] It is bipartite, so the classical Néel state satisfies every bond and breaks time-reversal symmetry.

    This is true. On a bipartite lattice all bonds are satisfied at the same time by two sublattices of opposite spin. There is then no frustration and no macroscopic degeneracy for the quantum fluctuations to mix.

    ![Look at panel (a), where all bonds of the bipartite plaquette are satisfied.](figures/s06f03_frustration.svg){alt="Three plaquettes, a bipartite one where every bond is satisfied, a frustrated triangle, and the 120 degree state."}

- [ ] It has too many neighbors for singlets to form.

    This is false. The kagome lattice also has four neighbors, like the square lattice, and it is a leading candidate for a spin liquid. The number of neighbors is not what decides it.

- [ ] It is two-dimensional, and spin liquids need three dimensions.

    This is false. The triangular and kagome lattices are two-dimensional and they are the standard places to look for spin liquids. Frustration and not the dimension is what matters.
:::

::: quiz
Each picture is a cluster of Ising spins $S^z_i=\pm\tfrac12$, one on each circle. Every line, solid or dashed, is a bond. The energy is

$$H=J\sum_{\langle ij\rangle}S^z_iS^z_j, \qquad J>0.$$

In which cluster can every bond be satisfied?

- [ ] ![A triangle of three sites joined by three bonds.](figures/web/session08/g2_quiz_cluster_triangle.svg)

    This is false. Two spins of the triangle can be antiparallel, but the third one is then parallel to one of them. The lowest energy is $-J/4$, with one unsatisfied bond, and not the $-3J/4$ of three satisfied bonds.

- [x] ![A square of four sites joined by four bonds along its edges.](figures/web/session08/g2_quiz_cluster_square.svg)

    This is true. The square is bipartite. With up spins on one diagonal and down spins on the other, every bond joins two antiparallel spins, and the energy is $4\cdot(-J/4)=-J$.

- [ ] ![A tetrahedron of four sites with a bond between every pair, drawn in perspective with the bond behind dashed.](figures/web/session08/g2_quiz_cluster_tetra.svg)

    This is false. Every pair of the four sites is a bond, so the cluster is made of four triangles. The best we can do is two spins up and two down, and the two parallel pairs cost energy. The lowest energy is $-J/2$, and not the $-3J/2$ of six satisfied bonds.
:::

:::: problem
Four Ising spins $S^z_i=\pm\tfrac12$ have the energy $H=J\sum S^z_iS^z_j$ with $J>0$, summed over the bonds of a cluster. Find the lowest energy and count the ground states on the square plaquette, with its four bonds around the square, and on the tetrahedron, where all six pairs of sites are bonds. In which of the two is every bond satisfied?

::: solution
On the square we label the sites $0,1,2,3$ around it. A bond is satisfied by two antiparallel spins, with $-J/4$. If site $0$ is up, the bonds $(01)$ and $(30)$ put the sites $1$ and $3$ down, and the bonds $(12)$ and $(23)$ then put site $2$ up. This configuration satisfies all four bonds, with $E=-J$, and its flip is the only other one. So the square has $2$ ground states, the two Néel states, and no frustration.

On the tetrahedron every pair is a bond, as on the triangle, so we can use the total $M=\sum_iS^z_i$. Since $\sum_i(S^z_i)^2=1$,

$$M^2=1+2\sum_{i<j}S^z_iS^z_j, \qquad\text{so}\qquad H=\frac J2\big(M^2-1\big).$$

The energy is lowest at $M=0$, with two spins up and two down, at $-J/2$. There are $\binom42=6$ such configurations, and in each of them the two parallel pairs are unsatisfied bonds. Six satisfied bonds would give $6\cdot(-\tfrac J4)=-\tfrac32J$, so the tetrahedron is frustrated, with a sixfold ground state like the triangle.

The two clusters have the same four sites, and only the bonds differ. The square is bipartite, and the tetrahedron is made of triangles. In a calculation this tells us what to expect before we run it. A bipartite lattice has only the two Néel states, as the square clusters of [](#sch:s08:ising_degeneracy) show, while a lattice of triangles has a degenerate ground state.
:::
::::

::: comesback
- In Section [8.6](#sec-8-6) quantum fluctuations mix the degenerate coverings of a frustrated lattice into the resonating valence bond state.
- In Section [9.9](#sec-9-9) a frustrated Heisenberg model with a ground state close to a spin liquid is probed with a local magnetic impurity.
:::
