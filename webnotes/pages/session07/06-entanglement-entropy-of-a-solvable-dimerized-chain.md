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
