## Two dimensions and the area law {#sec-7-7 number="7.7"}

Let us now do the same construction in one more dimension. We take a two-dimensional lattice and we group the sites into separate clusters of four sites, called tetramers, instead of pairs. The sites inside a cluster are coupled, but different clusters are not coupled, so the ground state is again an exact tensor product, now of tetramer ground states instead of dimer singlets. The same factorization argument applies. A cluster fully inside $A$ or fully inside $B$ gives nothing, and only the clusters that cross the boundary between the two parts contribute to $S$.

The only difference is geometric. Let us compare a small region $A$, whose boundary cuts eight bonds, with a much larger region $A'$, whose longer boundary cuts many more bonds. Since the entropy again gets one contribution per cut bond, $S$ is now set by the *length of the boundary*. In two dimensions this length grows when the subsystem grows. This is different from the 1D case of Section [7.6](#sec-7-6), where the boundary was always two points for any size of the subsystem. This is the central contrast. **In one dimension the entanglement entropy of a gapped ground state saturates**, and it does not depend on the size of the subsystem. **In two or more dimensions it grows with the size of the boundary**, $S_A \sim
L_A \sim \partial A$ and $S_{A'} \sim L_{A'} \sim \partial A'$, so $S_{A'} > S_A$ for the larger region. Figure [7.2](#fig:s07:arealaw) shows the two cases next to each other, with the cut bonds marked, so that we can count them by eye in each case.

![Why the entanglement entropy counts the boundary and not the volume, seen from above. In both panels the ground state is an exact product of the ground states of decoupled clusters, so a cluster that is fully inside $A$ or fully inside $B$ is in a pure state and gives nothing. Only the clusters that are cut by the division contribute, and the cut bonds are the red ones. (a) The dimerized chain. Each cut singlet gives exactly the single-dimer result $\log 2$ of [(7.7)](#eq-7-7), and the boundary of a block is two points for any length of the block. Each end of $A$ cuts through one dimer, so making $A$ larger, from two interior dimers to five, leaves two cut singlets and $S_A = 2\log 2$ unchanged. The entropy saturates. (b) The same construction with clusters of four sites on a square lattice. Each cluster that crosses the boundary still gives a bounded amount, at most $\log 2$ per cut bond, but now the boundary is a curve whose length grows with the subsystem. When we double the linear size of $A$, the number of cut bonds doubles, from eight to sixteen, and $S_A$ grows in proportion. This is the area law [(7.9)](#eq-7-9), $S_A \sim
\alpha\,|\partial A|$, and the contrast between the two panels is the reason why matrix product states are a one-dimensional tool.](figures/s07f02_arealaw.svg){#fig:s07:arealaw number="7.2"}

This behavior is called the **area law**. For the ground state of a gapped and local Hamiltonian, the entanglement entropy of a subsystem scales with the size of the boundary between the subsystem and the rest of the system, which is a fixed number of points in 1D, a length in 2D and an area in 3D,

$$S_A \;\sim\; \alpha\, |\partial A|, \tag{7.9}$$

and not with the *volume* of $A$. This is a strong restriction. A random state taken uniformly from the full Hilbert space of dimension $2^L$ would usually have $S_A$ close to its maximum value, which is $|A|\log 2$ for a spin-1/2 subsystem of size $|A|$, and this is called a volume law. In this sense, gapped ground states are very far from typical states. They live only in the very small part of the Hilbert space that satisfies the area law. The dimer and tetramer models above are exactly in this part, and realistic gapped Hamiltonians are approximately in it.

::: quiz
In the tetramer model of two dimensions we double the linear size of the region $A$. How does $S_A$ change?

- [x] It roughly doubles, since the boundary length doubles.
- [ ] It roughly quadruples, since the area quadruples.
- [ ] It does not change, since the state is gapped.
- [ ] It grows only as the logarithm of the size.

The entropy counts the cut bonds, and in two dimensions their number is proportional to the length of the boundary. The area of $A$ does not enter.
:::

::: quiz
A gapped ground state in three dimensions follows the area law [(7.9)](#eq-7-9). A cube of side $\ell$ has an entropy that grows as

- [ ] $\ell$.
- [x] $\ell^2$.
- [ ] $\ell^3$.
- [ ] a constant.

The boundary of a cube is made of its faces, which have an area proportional to $\ell^2$. The volume $\ell^3$ would be the volume law.
:::
