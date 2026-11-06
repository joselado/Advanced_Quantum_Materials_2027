## Storing the wave function as the main bottleneck {#sec-7-3 number="7.3"}

Now that we use the language of spins, let us ask why a general interacting many-body Hamiltonian is hard to solve. A first answer would be "because the diagonalization of a huge matrix is slow," but the main problem is more basic, and it is the *storage* of the wave function.

Let us take the simplest nontrivial case, which is the antiferromagnetic Heisenberg dimer, $H =
\mathbf{S}_0\cdot
\mathbf{S}_1$ on two spin-1/2 sites. Its ground state is the unique singlet,

$$|\Psi\rangle = \frac{1}{\sqrt{2}}\left(|{\uparrow\downarrow}\rangle -
|{\downarrow\uparrow}\rangle\right), \tag{7.3}$$

which is a state that does not break any symmetry, since the expectation value of every single-site spin vanishes. As we will show below, it is also maximally entangled. The question of the whole session is how this kind of state generalizes to a macroscopic system with many sites.

Let us write a general spin-1/2 wave function in the natural product basis, with one up or down label $s_i$ per site.

$$|\Psi\rangle = \sum_{s_1,\dots,s_L} C(s_1,\dots,s_L)\, |s_1,\dots,s_L\rangle, \qquad
s_i \in \{\uparrow,\downarrow\}. \tag{7.4}$$

For $L=2$ there are four basis states, up-up, up-down, down-up and down-down, so there are four coefficients $C$, and the Hamiltonian is a $4\times4$ matrix. If we add one site, $L=3$, the number doubles to eight. If we add one more site, $L=4$, it doubles again to sixteen. In general, the dimension of the Hilbert space is $d = 2^L$, and this is also the number of coefficients $C(s_1,\dots,s_L)$ that we need to write the ground state exactly. This exponential growth is the main limitation. Even if we never build the full $2^L\times2^L$ Hamiltonian matrix, and we only compute the matrix elements when we need them, we still have to store the $2^L$ coefficients of the ground state once we have found it. This storage cost, and not the cost of the diagonalization, is the real obstruction, and it is the most important point of the whole session. Tensor networks are one answer to this storage problem. In the lecture, **neural network quantum states** are also mentioned briefly as a second answer to the same problem, which comes from machine learning, but this second tool is not developed in this session. In session 10 we will come back to neural network quantum states in detail, from the point of view of machine learning. The material of this session is only about the first answer, tensor networks, and in particular matrix product states.

::: notebookbox
**Notebook check-in:** [`session7.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session7.ipynb), "Energy of the Heisenberg model as a function of the system size" (Core)

In this exercise you compute the ground-state energy per site of the Heisenberg chain with exact diagonalization, for growing system sizes. For this you use the `dmrgpy` library, which is new in this session, together with `pyqula`. You will see how fast exact diagonalization stops being possible, and this limit is the $2^L$ scaling of [(7.4)](#eq-7-4) in a concrete calculation.
:::
