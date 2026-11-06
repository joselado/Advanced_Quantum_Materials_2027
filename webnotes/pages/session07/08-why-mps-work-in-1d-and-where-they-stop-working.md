## Why MPS work in 1D {#sec-7-8 number="7.8a"}

The area law is the missing piece that explains why the ansatz [(7.5)](#eq-7-5) is a good one. Let us take an MPS at a given bond, and use it to build the Schmidt decomposition of the state for a division of the system at that bond.

$$|\Psi\rangle = \sum_{\alpha=1}^{M} \lambda_\alpha\, |\alpha\rangle_A \otimes |\alpha\rangle_B,$$

This sum has at most $M$ terms, because the internal index, also called virtual index, that runs through that bond only takes $M$ values. Therefore the reduced density matrix $\rho_A = \sum_\alpha
\lambda_\alpha^2 |\alpha\rangle_A
\langle\alpha|_A$ has rank at most $M$. Among all density matrices with rank $\le M$, the entropy [(7.6)](#eq-7-6) is maximal when all the eigenvalues are equal, $\lambda_\alpha^2 = 1/M$, which gives

$$S \;\le\; \log M. \tag{7.10}$$

In other words, an MPS with bond dimension $M$ can have an entanglement entropy of at most $\log M$ across any bond, which grows only logarithmically with $M$. Let us compare this with [(7.9)](#eq-7-9). A 1D gapped ground state has an entanglement entropy that *saturates* at a finite value, which does not depend on the size of the subsystem, so a moderate and fixed bond dimension is already enough to describe it almost exactly. This is the precise and quantitative reason why matrix product states are such a good ansatz in one dimension, since the area law limits the same quantity that the bond dimension limits. Geometrically, we can think of the full many-body Hilbert space as a large set, and MPS describe only a very small part of it, which is the part of area-law states. This part is reached with a bond dimension that stays moderate ($M \sim 10$, $100$) as long as we stay in the area-law regime. To reach a general state with a volume law, the bond dimension would have to become very large, $M \sim 2^{L/2}$, which is exponential in $L$. Figure [7.3](#fig:s07:ceiling) shows this comparison directly. It shows the upper limit $\log M$ given by [(7.10)](#eq-7-10) and the entropy that a gapped, a critical and a general state need when the subsystem grows.

![The bond dimension is an upper limit on the entanglement, and this determines when matrix product states work. An MPS with bond dimension $M$ has at most $M$ Schmidt terms across any bond, so by [(7.10)](#eq-7-10) it can have at most $S=\log M$ there, which is shown by the two horizontal bars, for $M=4$ and $M=16$. A gapped one-dimensional ground state follows the area law of Section [7.6](#sec-7-6), and its entropy saturates at a value set by the correlation length and not by the subsystem size, so it stays below a fixed and moderate limit for any chain length. A critical chain violates the area law logarithmically, [(7.12)](#eq-7-12), so it goes above any fixed limit at some point, here the lower bar, and $M$ must be increased as the system grows, slowly but without bound. A general state of the Hilbert space of dimension $2^L$ follows a volume law, $S=\ell\log 2$, and it goes above any usable $M$ after a few sites. This is why time evolution over long times, highly excited states and two-dimensional systems are all out of reach. The entropy is drawn in bits, $S/\log 2$, with central charge $c=1$, and the curves are schematic and not fits to a specific model.](figures/s07f03_entropyceiling.svg){#fig:s07:ceiling number="7.3"}

::: quiz
A gapped chain of 50 sites is described accurately with a bond dimension $M$. What do we need for a gapped chain of 500 sites in the same phase?

- [ ] About ten times larger $M$.
- [x] About the same $M$, since the entropy saturates.
- [ ] An $M$ that is exponentially larger.
- [ ] A smaller $M$, since the chain is longer.

In a gapped state the entropy across a bond is set by the correlation length and not by the length of the chain. The bound [(7.10)](#eq-7-10) then asks for the same $M$.
:::

::: quiz
An MPS has $M=16$. What is the largest entanglement entropy that it can hold across one bond, in units of $\log 2$?

- [ ] $16$, since there are 16 terms.
- [ ] $8$, since it is half of $M$.
- [x] $4$, since $\log 16=4\log 2$.
- [ ] $2$, since it is the square root of $M$.

The bound [(7.10)](#eq-7-10) is $S\le\log M$, and $\log 16=4\log 2$. The number of Schmidt terms is $16$ but the entropy grows only as its logarithm.
:::

::: notebookbox
**Notebook check-in:** [`session7.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session7.ipynb), "Near linear scaling with system size with matrix product states" (Core) and "The role of the bond dimension in tensor networks" (Core)

In the first exercise you check directly that the cost of the DMRG ground-state calculation in `dmrgpy` grows linearly with the system size, which is the $L\times M^2$ scaling of [(7.5)](#eq-7-5) and not the $2^L$ scaling of [(7.4)](#eq-7-4). In the second exercise you change the bond dimension and see how the fluctuation of the ground-state energy becomes smaller and then saturates. The point where it saturates is where $M$ is large enough to satisfy the bound [(7.10)](#eq-7-10) for that state.
:::

::: {.tryit notebook="session7.ipynb" cell="Entanglement entropy of the ground state"}
Run the loop over `maxm` in `[2,4,8,20]` and look at the bond entropy. For `maxm=2` the curve cannot go above $\ln 2\approx0.69$, while for `maxm=20` it follows the true ground state. Check that the central bonds have the largest entropy.
:::
