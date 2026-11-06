## Entanglement entropy of a solvable dimerized chain {#sec-7-6 number="7.6"}

There are two exactly solvable models that show how [(7.6)](#eq-7-6)-[(7.7)](#eq-7-7) scale with the system size. They are the key to the whole session, so let us go through them carefully.

Let us take a one-dimensional chain of spin-1/2's, but we couple the spins only in separate pairs. There is an antiferromagnetic bond between sites $0$ and $1$, another one between $2$ and $3$, another one between $4$ and $5$, and so on, and there is *no* coupling between different pairs,

$$H = \sum_n J\,\mathbf{S}_{2n}\cdot\mathbf{S}_{2n+1}.$$

This Hamiltonian is easy to solve exactly, because it is a sum of independent Heisenberg dimers. Its ground state is therefore an exact tensor product of singlets, with one singlet per dimer bond,

$$|\Psi\rangle = |\text{singlet}\rangle_{01} \otimes |\text{singlet}\rangle_{23} \otimes
|\text{singlet}\rangle_{45} \otimes \cdots. \tag{7.8}$$

Physically, this is a valence-bond product state, also called a dimer product state, which is the simplest example of a gapped state with short-range entanglement, and not a spin liquid. The ground state does not break any symmetry of this Hamiltonian, and it is separated from the lowest triplet excitation by a large gap, which is the singlet-triplet splitting of a single dimer. For this reason it is as far from criticality as a spin model can be.

Now we divide the chain into two parts and ask for the entanglement entropy. Since [(7.8)](#eq-7-8) is a tensor product over separate bonds, the reduced density matrix $\rho_A$ factorizes bond by bond. A dimer that is fully inside $A$, or fully inside $B$, gives a pure state in $\rho_A$, and therefore it gives exactly zero to $S$, with the same argument as for the product state in Section [7.5](#sec-7-5). The only bonds that contribute are the ones that are cut by the boundary between the two parts. Each cut bond gives the single-dimer result [(7.7)](#eq-7-7), $\log 2$, since tracing out one half of a singlet always leaves the same maximally mixed single-site density matrix, regardless of what happens in the rest of the chain. So if the boundary cuts $n_\text{cut}$ bonds, $S = n_\text{cut} \log 2$.

Let us take a small subsystem $A$ whose two ends cut through two dimers, one on each side. Then two singlet bonds cross the boundary, so $S = 2\log 2$. Let us now take a much larger subsystem $A$, with a width of many dimers, whose ends again cut through one dimer each. The boundary still crosses only two singlet bonds, the ones at its two edges, so we get again $S = 2\log 2$, with no change. **The entanglement entropy of this state does not grow with the size of the subsystem**. It is fully determined by the two points where the one-dimensional boundary is, for any distance between these two points.

![We compute the entropy of a block of $\ell$ sites, starting at site 1, in the dimer product state [(7.8)](#eq-7-8). The chain has 12 sites and the numbers come from the exact state. The entropy alternates between one and two times $\log 2$, since the block cuts one or two singlets, and it never grows with $\ell$. The dashed line is the volume law that a generic state would follow. Look at the odd blocks, which cut only the singlet at their left end.](figures/web/session07/dimer_entropy.svg){#sch:s07:dimer_entropy alt="The entropy of a block of sites against its length for a dimer product state, which alternates between one and two times log 2, and a dashed straight line for the volume law."}

::: quiz
The dimers are the pairs of sites $(0,1)$, $(2,3)$, $(4,5)$ and so on. Which block of sites has exactly zero entanglement entropy in the state [(7.8)](#eq-7-8)?

- [ ] Sites 1 to 4.
- [x] Sites 2 to 5.
- [ ] Sites 3 to 6.

The block of sites 2 to 5 contains the dimers $(2,3)$ and $(4,5)$ completely, so no singlet is cut. The other two blocks cut two singlets and give $2\log2$.
:::

::: quiz
A block of sites 1 to 3 is taken from the same state. What is its entropy?

- [ ] $0$, since the block contains one full dimer.
- [ ] $2\log 2$, since the block has two boundaries.
- [ ] $3\log 2$, since the block has three sites.
- [x] $\log 2$, since only the singlet $(0,1)$ is cut.

The dimer $(2,3)$ is inside the block, and the dimer $(0,1)$ is cut at the left end. The right end falls between two dimers and cuts nothing, so there is one cut singlet.
:::

::: {.widget name="dimerentropy"}
Move the coupling $J_2$ between the dimers of a Heisenberg chain with 12 spins, with $J_1=1$ inside the dimers. We find the ground state by exact diagonalization and compute the entropy of the first $l$ spins. At $J_2=0$ this is the product of singlets of [(7.8)](#eq-7-8), and the entropy is $\log 2$ for a cut through a dimer and zero for a cut between dimers. Switch on $J_2$ and see how each cut changes.
:::

