## Tensor diagrams as notation for networks and operators {#sec-7-9 number="7.9"}

Matrix product states come with a convenient graphical notation, which makes it much easier to think about both the ansatz and the algorithms built on it. A scalar, which is a tensor of rank 0, is drawn as a point. A vector, of rank 1, is a point with one free leg. A matrix, of rank 2, is a point with two legs. A tensor of rank 3 is a point with three legs, and so on for any rank. Each leg represents one index of the tensor, and when we join two legs of two tensors, this means that we sum over the shared index, which is called a contraction.

An MPS is then a horizontal chain of such points, with one point per site. Each point has one *physical* leg pointing down, which is the index $s_i$, the local spin value. It also has one or two *virtual* legs that connect it to its neighbors in the chain, and these carry the bond-dimension index that is summed over. A **matrix product operator** (MPO) represents an operator, in particular the Hamiltonian, in the same way. Now each site has *two* physical legs instead of one, which correspond to the two indices $\sigma_i,\sigma_i'$ of the operator, and the same virtual legs that link neighboring sites. To apply an MPO to an MPS, for example to compute $H|\Psi\rangle$, we join the two diagrams along the physical legs and contract them. This means that we multiply every pair of matrices that share an index and sum over that index. If we do this in a naive way, the bond dimensions of the two objects are multiplied, which would remove the advantage of the method. In practice, we do a singular value decomposition of the result and keep only the largest singular values. In this way we truncate back to a bond dimension that we can handle, and we remove the least important part of the Hilbert space that is represented. This truncation step is the practical core of almost every MPS algorithm, including the ground-state search of the next section. Figure [7.4](#fig:s07:tensors) shows together the notation, the ansatz [(7.5)](#eq-7-5) drawn in this notation, and this step of contraction and truncation.

![The graphical notation, and the MPS ansatz drawn in it. (a) A tensor is a block and each of its indices is a leg, so a scalar has no leg, a vector has one leg, a matrix has two, and so on. Joining two legs means summing over the shared index. (b) The exact coefficient tensor of [(7.4)](#eq-7-4) is a single object with one leg per site, and it contains $2^L$ independent numbers. The matrix product state [(7.5)](#eq-7-5) replaces it with a chain of small tensors. Each of them has one physical leg pointing down and virtual legs of dimension $M$ that link it to its neighbors. In total this is $\sim 2LM^2$ numbers, so the exponential growth is replaced by a linear one. (c) An operator, in particular the Hamiltonian, becomes a matrix product operator, the darker row, with two physical legs per site. To apply it to a state we join the diagrams along the shared physical legs and contract them, which multiplies the two bond dimensions. A singular value decomposition that keeps only the largest singular values then truncates the result back to a usable $M$. This truncation is the core of every MPS algorithm, including DMRG.](figures/s07f04_tensordiagram.svg){#fig:s07:tensors number="7.4"}

::: quiz
An MPS of bond dimension $M$ is acted on by an MPO of bond dimension $D$, and we contract the physical legs without truncating. What is the bond dimension of the result?

- [x] $M\cdot D$.

    This is true. Each bond of the result carries one index of the state and one of the operator, so the dimensions multiply. This growth is the reason why a truncation by singular value decomposition follows each operation.

    ![An MPO acts on an MPS. Each bond of the result joins one bond of the MPO and one of the MPS, so it has the dimension $M\cdot D$.](figures/web/session07/mpo_on_mps.svg){alt="A row of squares joined to a row of circles by their physical legs, then one row of tensors whose bonds are labelled M times D."}

- [ ] $M+D$.

    This is false. Take a product state, $M=1$, and a product operator, $D=1$. The sum gives 2, but the result is again a product state with bond dimension 1.

- [ ] $M^D$.

    This is false. For a product state, $M=1$, acted on by an operator with $D=5$ the formula gives $1^5=1$. The result has a bond that can be as large as $1\cdot5=5$.
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

::: comesback
- In Section [7.10](#sec-7-10) the same diagrams turn the derivative of the energy into the erasure of one tensor, which is the step of DMRG.
- In Section [10.4](#sec-10-4) the same diagrams draw MPS, trees, MERA and PEPS as machine-learning architectures.
:::
