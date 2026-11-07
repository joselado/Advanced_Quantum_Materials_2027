## Two dimensions and the area law {#sec-7-7 number="7.7"}

Let us now do the same construction in one more dimension. We take a two-dimensional lattice and we group the sites into separate clusters of four sites, called tetramers, instead of pairs. The sites inside a cluster are coupled, but different clusters are not coupled, so the ground state is again an exact tensor product, now of tetramer ground states instead of dimer singlets. The same factorization argument applies. A cluster fully inside $A$ or fully inside $B$ gives nothing, and only the clusters that cross the boundary between the two parts contribute to $S$.

The only difference is geometric. Let us compare a small region $A$, whose boundary cuts eight bonds, with a much larger region $A'$, whose longer boundary cuts many more bonds. Since the entropy again gets one contribution per cut bond, $S$ is now set by the *length of the boundary*. In two dimensions this length grows when the subsystem grows. This is different from the 1D case of Section [7.6](#sec-7-6), where the boundary was always two points for any size of the subsystem. This is the central contrast. **In one dimension the entanglement entropy of a gapped ground state saturates**, and it does not depend on the size of the subsystem. **In two or more dimensions it grows with the size of the boundary**, $S_A \sim
L_A \sim \partial A$ and $S_{A'} \sim L_{A'} \sim \partial A'$, so $S_{A'} > S_A$ for the larger region. Figure [7.2](#fig:s07:arealaw) shows the two cases next to each other, with the cut bonds marked, so that we can count them by eye in each case.

![Why the entanglement entropy counts the boundary and not the volume, seen from above. In both panels the ground state is an exact product of the ground states of decoupled clusters. So a cluster that is fully inside $A$ or fully inside $B$ is in a pure state and gives nothing. Only the clusters that are cut by the division contribute, and the cut bonds are the red ones. (a) The dimerized chain. Each cut singlet gives the single-dimer result $\log 2$ of [(7.7)](#eq-7-7), and the boundary of a block is two points for any length of the block. Each end of $A$ cuts through one dimer, so making $A$ larger, from two interior dimers to five, leaves two cut singlets and $S_A = 2\log 2$ unchanged. The entropy saturates. (b) The same construction with clusters of four sites on a square lattice. Each cluster that crosses the boundary still gives a bounded amount, at most $\log 2$ per cut bond, but now the boundary is a curve whose length grows with the subsystem. When we double the linear size of $A$, the number of cut bonds doubles, from eight to sixteen, and $S_A$ grows in proportion. This is the area law [(7.9)](#eq-7-9), $S_A \sim
\alpha\,|\partial A|$, and the contrast between the two panels is the reason why matrix product states are a one-dimensional tool.](figures/s07f02_arealaw.svg){#fig:s07:arealaw number="7.2"}

This behavior is called the **area law**. The boundary between a subsystem and the rest of the system is a fixed number of points in 1D, a length in 2D and an area in 3D. For the ground state of a gapped and local Hamiltonian, the entanglement entropy of a subsystem scales with the size of this boundary,

$$S_A \;\sim\; \alpha\, |\partial A|, \tag{7.9}$$

and not with the *volume* of $A$. This is a strong restriction. A random state taken uniformly from the full Hilbert space of dimension $2^L$ would usually have $S_A$ close to its maximum value. This maximum is $|A|\log 2$ for a spin-1/2 subsystem of size $|A|$, and this behavior is called a volume law. In this sense, gapped ground states are very far from typical states. They live only in the very small part of the Hilbert space that satisfies the area law. The ground states of the dimer and tetramer models above are in this part without any approximation, and the ones of realistic gapped Hamiltonians are approximately in it.

![Volume law against area law, computed for a chain of $L=14$ spins, where $A$ is the block of the first $|A|$ sites. The red points are a random state of the full Hilbert space. Its entropy follows the maximum $\min(|A|,L-|A|)\log 2$, with a small deficit at the middle, so it grows with the volume of $A$. The blue points are the ground state of a dimerized Heisenberg chain, with $J=1$ on the strong bonds and $J=0.5$ on the weak ones, which is gapped. Its entropy is close to $\log 2$ when the cut breaks a strong bond and about $0.15\log 2$ when it breaks a weak bond, for any $|A|$. This is the chain of Section [7.6](#sec-7-6) with the weak bonds switched on, and it stays far below the random state.](figures/web/session07/random_vs_gapped.svg){#sch:s07:random_vs_gapped alt="The entropy of the left block against its size for 14 spins, in units of log 2, a red tent that rises to about 6 at the middle and a blue zigzag between about 0.15 and 1."}

::: quiz
In the tetramer model of two dimensions we double the linear size of the region $A$. How does $S_A$ change?

- [x] It roughly doubles, since the boundary length doubles.

    This is true. The entropy counts the cut tetramers, and in two dimensions their number is proportional to the length of the boundary. For a square of side 2 or 4 the perimeter is 8 or 16, so the entropy doubles.

- [ ] It roughly quadruples, since the area quadruples.

    This is false. The square of side 2 has 4 sites and the one of side 4 has 16, but the clusters inside the square are not cut. Only the perimeter, 8 and then 16, counts, so the factor is 2 and not 4.

    ![A square of side 2 and one of side 4 on a square lattice. The red bonds are cut, and their number follows the perimeter.](figures/web/session07/square_regions.svg){alt="Two square regions on a lattice of dots, with 4 and 16 sites inside, and the bonds that cross their boundary in red, 8 and 16 of them."}

- [ ] It does not change, since the state is gapped.

    This is false. In one dimension the boundary is two points and the entropy is constant. In two dimensions the boundary grows with the size, so a gapped state still has an entropy that grows.
:::

::: quiz
A gapped ground state in three dimensions follows the area law [(7.9)](#eq-7-9). A cube of side $\ell$ has an entropy that grows as

- [ ] $\ell^3$.

    This is false. This is the volume law. For $\ell=100$ the cube has $10^6$ sites but its surface cuts only $6\times10^4$ bonds, and the area law lets each bond carry at most $\log2$.

- [x] $\ell^2$.

    This is true. The boundary of a cube is made of its six faces, which have an area proportional to $\ell^2$. In [(7.9)](#eq-7-9) the entropy follows this area and not the volume $\ell^3$.

- [ ] a constant.

    This is false. A constant is the result in one dimension, where the boundary of a block is two points. For a cube of side 2 and of side 4 the surface cuts 24 and 96 bonds, so the number of cut bonds grows.
:::

::: comesback
- In Section [7.8](#sec-7-8) the area law is the reason why an MPS with a moderate bond dimension describes a gapped chain.
- In Section [7.8b](#sec-7-8b) the growing boundary in two dimensions is the reason why an MPS fails there.
- In Section [7.11](#sec-7-11) PEPS put one tensor on every site of a 2D lattice, which is the natural network for two dimensions.
:::
