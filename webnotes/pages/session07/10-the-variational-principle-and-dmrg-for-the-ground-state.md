## The variational principle and DMRG for the ground state {#sec-7-10 number="7.10"}

An ansatz is only useful if we can optimize it. We take the MPS matrices $\{M_i^{s_i}\}$ as variational parameters and minimize the Rayleigh quotient

$$E[\Psi] = \frac{\langle \Psi | H | \Psi \rangle}{\langle \Psi | \Psi \rangle}, \tag{7.11}$$

or, in an equivalent way, we introduce a Lagrange multiplier $\lambda$ for the normalization and minimize $\langle
\Psi|H|\Psi\rangle - \lambda\left(\langle\Psi|\Psi\rangle - 1\right)$ with respect to every matrix in the network. In the diagrams, the derivative with respect to one tensor in the network, for example the matrix at site $k$, corresponds to "erasing" that tensor from the diagram. The reason is that each tensor appears once in the bra layer and once in the ket layer, so with the other tensors fixed the energy is a quadratic form in that tensor, and it is linear in the bra copy alone. When we erase the bra tensor of site $k$ from both the numerator and the denominator diagrams, what is left is a generalized eigenvalue problem for that single tensor, which becomes an ordinary one when the other tensors are chosen orthonormal. It involves an effective, reduced Hamiltonian that acts on the indices of site $k$, and its ground eigenvector is the locally optimal replacement for $M_k^{s_k}$. Figure [7.5](#fig:s07:dmrg) shows this erasure and the sweep that follows from it.

![How DMRG turns an exponentially large minimization into a sequence of small ones. (a) The numerator of the Rayleigh quotient [(7.11)](#eq-7-11) is a single closed network, made of the ket MPS, the Hamiltonian as an MPO and the bra MPS, all contracted together. It has no free legs, so it is a number. (b) Every tensor enters that network once in the bra layer and once in the ket layer, so the energy is a quadratic form in each tensor and linear in its bra copy, and the derivative with respect to the bra tensor at site $k$ removes it, which is the ghost. What is left has exactly three open legs, drawn in red, the two virtual bonds and the physical index of site $k$, which are the indices of the tensor $M_k^{s_k}$ that we want to find. Everything to the left and right of $k$ has been reduced to an environment, and the stationarity condition is a generalized eigenvalue problem, which is an ordinary one in an orthonormal gauge, with the size of a single tensor. (c) We solve it, move one site along, solve again, and sweep back and forth until the energy stops decreasing. This is the density matrix renormalization group, and at no point do we build an object of size $2^L$.](figures/s07f05_dmrg.svg){#fig:s07:dmrg number="7.5"}

This suggests an iterative algorithm. We fix every tensor except the one of site $1$, solve the local eigenvalue problem there, and update $M_1^{s_1}$ with the resulting eigenvector. Then we move to site $2$, fix everything else, solve the local eigenvalue problem there, and update. We continue sweeping through the chain, site by site, until the energy stops decreasing. This sweeping procedure is the **density matrix renormalization group (DMRG)** algorithm. Its efficiency comes from the property of [(7.11)](#eq-7-11) that we used to build it. At every step we optimize only one matrix at a time, which is a small linear-algebra problem that we can solve, instead of searching for the ground state in the full exponentially large space at once.

::: quiz
When DMRG updates one tensor with all the others fixed, what happens to the energy [(7.11)](#eq-7-11)?

- [ ] It can increase, and the sweeps compensate it later.

    This is false. The old tensor is one of the candidates of the local minimization with energy $E_\text{old}$. The minimum is then $E_\text{new}\le E_\text{old}$, so an increase is impossible at any step.

- [x] It cannot increase, since the update is the exact minimum over that tensor.

    This is true. The old tensor is one of the candidates of the local minimization, so the new one is at least as good. The energy [(7.11)](#eq-7-11) goes down or stays the same, and this is why the sweeps converge.

- [ ] It decreases only if the bond dimension is also increased.

    This is false. The bond dimension $M$ is fixed during the sweeps. Starting from a random MPS with energy close to zero, the first update already lowers the energy at the same $M$.
:::

::: quiz
The local eigenvalue problem at one bulk site of a spin-1/2 chain has a matrix of size

- [x] $2M^2$.

    This is true. The open legs of the erased tensor are two virtual bonds of dimension $M$ and one physical index of dimension $2$. The matrix acts on these $2M^2$ numbers, and $L$ does not appear.

- [ ] $2^L$.

    This is false. This is the exact diagonalization, which needs $2^{40}\approx10^{12}$ numbers for $L=40$. For $M=100$ the local problem has only $2M^2=2\times10^4$ numbers.

- [ ] $2M$.

    This is false. This is the size at the end of the chain, where the tensor has one bond and one physical leg. At a bulk site there are two bonds, so for $M=100$ the size is $2\times10^4$ and not $200$.
:::

::: notebookbox
**Notebook check-in:** [`session7.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session7.ipynb), "Low energy excitations of a Heisenberg model" (Core)

In this exercise you look at the matrix elements between the DMRG ground state and the first excited state of a Heisenberg chain, meaning what the sweeping procedure of Section [7.10](#sec-7-10) finds one level above the state that directly minimizes [(7.11)](#eq-7-11).
:::

::: {.tryit notebook="session7.ipynb" cell="Low energy excitations of a Heisenberg model"}
Plot the matrix element between the ground state and the first excited state along the chain, for `L=20` and for `L=12`. Is the excitation localized on a few sites or spread over the chain? Then set `Bz=0` and see whether the profile changes.
:::
