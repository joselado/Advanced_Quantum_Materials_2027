## Tensor diagrams as notation for networks and operators {#sec-7-9 number="7.9"}

How do we compute with an MPS without writing every index? We will now see a graphical notation, where a leg is an index and two joined legs are a sum over that index. In this notation an operator that acts on a state multiplies the bond dimensions, and a singular value decomposition cuts them back.

::: {.recall eq="7.5"}
This is the matrix product state of Section [7.4](#sec-7-4). The coefficient $C(s_1,\dots,s_L)$ of the state is a product of matrices, one for each site. Each $M^{s_i}_i$ is a $\chi\times \chi$ matrix for each value of the spin $s_i$, and $\chi$ is the bond dimension. At the two ends of an open chain the matrices are vectors.
:::

Matrix product states come with a convenient graphical notation, which makes it much easier to think about both the ansatz and the algorithms built on it. A scalar, which is a tensor of rank 0, is drawn as a point. A vector, of rank 1, is a point with one free leg. A matrix, of rank 2, is a point with two legs. A tensor of rank 3 is a point with three legs, and so on for any rank. Each leg represents one index of the tensor, and when we join two legs of two tensors, this means that we sum over the shared index, which is called a contraction.

An MPS is then a horizontal chain of such points, with one point per site. Each point has one *physical* leg pointing down, which is the index $s_i$, the local spin value. It also has one or two *virtual* legs that connect it to its neighbors in the chain, and these carry the bond-dimension index that is summed over.

A **matrix product operator** (MPO) represents an operator, in particular the Hamiltonian, in the same way. Now each site has *two* physical legs instead of one, which correspond to the two indices $\sigma_i,\sigma_i'$ of the operator, and the same virtual legs that link neighboring sites. To apply an MPO to an MPS, for example to compute $H|\Psi\rangle$, we join the two diagrams along the physical legs and contract them. This means that we multiply every pair of matrices that share an index and sum over that index. If we do this in a naive way, the bond dimensions of the two objects are multiplied, which would remove the advantage of the method.

In practice, we do a singular value decomposition of the result and keep only the largest singular values. In this way we truncate back to a bond dimension that we can handle, and we remove the least important part of the Hilbert space that is represented. This truncation step is the practical core of almost every MPS algorithm, including the two-site update of the ground-state search of the next section. Figure [7.4](#fig:s07:tensors) shows together the notation, the ansatz [(7.5)](#eq-7-5) drawn in this notation, and this step of contraction and truncation.

::: key
An MPO of bond dimension $D$ that acts on an MPS of bond dimension $\chi$ gives an MPS of bond dimension $\chi D$, so the new state has at most $\chi D$ Schmidt terms at a bond. A singular value decomposition at each bond brings it back,

$$\chi \;\to\; \chi D \;\to\; \chi,$$

by keeping the $\chi$ largest singular values. This truncation is the core of almost every MPS algorithm.
:::

::: {.steps title="From an MPO and an MPS to a bond of dimension chi times D, and back to chi"}
We write the tensor of the MPS at one site as $M^{\sigma'}_{\alpha\beta}$, with the physical index $\sigma'$ and the two virtual indices $\alpha,\beta$, which take $\chi$ values. The tensor of the MPO at the same site is $W^{\sigma\sigma'}_{ab}$, with two physical indices and two virtual indices $a,b$, which take $D$ values. Joining the physical legs is the sum over $\sigma'$,

$$N^{\sigma}_{(a\alpha),(b\beta)}=\sum_{\sigma'}W^{\sigma\sigma'}_{ab}\,M^{\sigma'}_{\alpha\beta}.$$

The new tensor has one physical index $\sigma$. Its left index is the pair $(a,\alpha)$, which takes $D\cdot \chi$ values, and so does its right index. So the result is again an MPS, with the bond dimension $\chi D$. The new state has at most $\chi D$ Schmidt terms at a bond, and it can have fewer. For the MPO of the Heisenberg chain, with $D=5$, and a random MPS with $\chi=4$ on 10 sites, the bonds in the bulk are 20. The new state has at most 12 Schmidt terms at a bond. The simplest case is a product state, $\chi=1$, and a product operator, $D=1$, such as $\prod_i\sigma^x_i$, which flips every spin, and then the result is again a product state.

To cut the bond back, we write the state at one bond in its Schmidt form,

$$|\Psi\rangle=\sum_{k=1}^{\chi D}s_k\,|L_k\rangle\otimes|R_k\rangle, \qquad s_1\ge s_2\ge\dots\ge0,$$

where the states $|L_k\rangle$ on the left are orthonormal, and so are the states $|R_k\rangle$ on the right. This is the singular value decomposition of the coefficients, with the sites on the left as rows and the sites on the right as columns. In an MPS it is done on the tensors next to the bond, once the others are in an orthonormal form, so it never builds the $2^L$ coefficients. We keep the $\chi$ largest $s_k$. For a normalized state the squared distance between $|\Psi\rangle$ and the truncated state, before it is normalized again, is the dropped weight

$$\varepsilon=\sum_{k>\chi}s_k^2,$$

and no other state with at most $\chi$ Schmidt terms at this bond is closer. When the Schmidt weights fall fast, as for a gapped chain, $\varepsilon$ is small already for a moderate $\chi$.
:::

![The graphical notation, and the MPS ansatz drawn in it. (a) A tensor is a block and each of its indices is a leg, so a scalar has no leg, a vector has one leg, a matrix has two, and so on. Joining two legs means summing over the shared index. (b) The exact coefficient tensor of [(7.4)](#eq-7-4) is a single object with one leg per site, and it contains $2^L$ independent numbers. The matrix product state [(7.5)](#eq-7-5) replaces it with a chain of small tensors. Each of them has one physical leg pointing down and virtual legs of dimension $\chi$ that link it to its neighbors. In total this is $\sim 2L\chi^2$ numbers, so the exponential growth is replaced by a linear one. (c) An operator, in particular the Hamiltonian, becomes a matrix product operator, the darker row, with two physical legs per site. To apply it to a state we join the diagrams along the shared physical legs and contract them, which multiplies the two bond dimensions. A singular value decomposition that keeps only the largest singular values then truncates the result back to a usable $\chi$. This truncation is the core of almost every MPS algorithm, including DMRG. The labels of the drawing write the bond dimension as $M$.](figures/s07f04_tensordiagram.svg){#fig:s07:tensors number="7.4"}

::: quiz
An MPO of bond dimension $D$ acts on an MPS of bond dimension $\chi$. We contract the physical legs and do not truncate. What is the bond dimension of the result?

- [x] $\chi\cdot D$.

    This is true. Each bond of the result carries one index of the state and one of the operator, so the dimensions multiply. This growth is the reason why a truncation by singular value decomposition follows each operation.

    ![An MPO acts on an MPS. Each bond of the result joins one bond of the MPO and one of the MPS, so it has the dimension $\chi\cdot D$.](figures/web/session07/mpo_on_mps.svg){alt="A row of squares joined to a row of circles by their physical legs, then one row of tensors whose bonds are labelled chi times D."}

- [ ] $\chi+D$.

    This is false. Take a product state, $\chi=1$, and a product operator, $D=1$. The sum gives 2, but the result is again a product state with bond dimension 1.

- [ ] $\chi^D$.

    This is false. For a product state, $\chi=1$, acted on by an operator with $D=5$ the formula gives $1^5=1$. The result has a bond that can be as large as $1\cdot5=5$.
:::

::: quiz
A tensor has three legs, and each leg has dimension $4$. How many numbers does it contain?

- [ ] $12$.

    This is false. The sum counts three separate vectors of 4 entries. A tensor has one number for each combination of the indices, and the tensor with legs $2,2,2$ has 8 entries and not 6.

- [x] $64$.

    This is true. The number of entries is the product of the dimensions of the legs, $4\times4\times4=64$.

- [ ] $256$.

    This is false. The value $4^4$ is the number of entries of a tensor with four legs. With three legs the indices $(i,j,k)$ take $4\times4\times4=64$ values.
:::

::: quiz
Each diagram is built from the tensors of a chain of four sites. A joined leg is a sum over its index. Which diagram is a number?

- [ ] ![One row of four circles joined by horizontal bonds, where each circle has one leg that points down and ends free.](figures/web/session07/g4_quiz_net_ket.svg)

    This is false. The four free legs are the spins $s_1,\dots,s_4$, so the diagram is the tensor $C(s_1,\dots,s_4)$ of the state $|\Psi\rangle$, with $2^4=16$ entries.

- [x] ![Two rows of four circles, where the leg of each circle of the upper row joins the leg of the circle below it.](figures/web/session07/g4_quiz_net_norm.svg)

    This is true. Every leg joins two tensors, so every index is summed and nothing is left. The diagram is the norm $\langle\Psi|\Psi\rangle$, with the MPS on top and its complex conjugate below.

- [ ] ![A row of four squares above a row of four circles. The leg of each circle joins the square above it, and each square has one more leg that points up and ends free.](figures/web/session07/g4_quiz_net_hpsi.svg)

    This is false. The legs between the circles and the squares are summed, but the four upper legs of the squares are free. The diagram is the state $H|\Psi\rangle$, again with $2^4=16$ entries.
:::

:::: problem
An MPS of a spin-1/2 chain has the bond dimension $\chi=10$, and an MPO with $D=5$ acts on it, which is the bond dimension of the MPO of the Heisenberg chain. Find the bond dimension of the result before any truncation. Then count the numbers of one bulk tensor before the contraction, after it, and after the truncation back to $\chi=10$.

::: solution
Each bond of the result carries one index of the MPS and one of the MPO, so its dimension is $\chi D=10\times5=50$. A bulk tensor has one physical leg of dimension 2 and two virtual legs. Before the contraction it has $2\chi^2=2\times10^2=200$ numbers, after it $2\times50^2=5000$, and after the truncation $200$ again.

One application of the MPO makes each tensor $D^2=25$ times larger, and a second one without truncation would give $2\times250^2=1.25\times10^5$ numbers. This is why MPS algorithms truncate after each application of an operator, so that the cost stays set by $\chi$.
:::
::::

::: comesback
- In Section [7.10](#sec-7-10) the same diagrams turn the derivative of the energy into the erasure of one tensor, which is the step of DMRG.
- In Section [10.4](#sec-10-4) the same diagrams draw MPS, trees, MERA and PEPS as machine-learning architectures.
:::
