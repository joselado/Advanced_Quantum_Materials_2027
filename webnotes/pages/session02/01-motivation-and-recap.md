## Motivation and recap {#sec-2-1 number="2.1"}

Let us recall the form of a many-body Hamiltonian once it is written in second-quantized, tight-binding form,

$$H = \sum_{ij} t_{ij}\, c_i^\dagger c_j,$$

where $t_{ij}$ are the hopping matrix elements between sites $i$ and $j$. In this language, to solve a quantum material means to diagonalize this Hamiltonian, which is to find the unitary transformation that brings it into the diagonal form

$$H = \sum_n \epsilon_n\, \Psi_n^\dagger \Psi_n, \qquad \Psi_n^\dagger = \sum_i a_{n,i}\, c_i^\dagger.$$

Symmetries allow us to find this diagonal form, or at least strong qualitative and quantitative properties of it, without doing the diagonalization explicitly. This is the motivation for everything in this session. We will use symmetry not to classify order, but to simplify how we solve a quantum many-body problem.
