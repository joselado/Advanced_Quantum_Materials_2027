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

![The number of coefficients of the exact state [(7.4)](#eq-7-4) doubles with every site, so on this logarithmic scale it is a straight line. The matrix product state [(7.5)](#eq-7-5) needs only $LM^2$ numbers, which is an almost flat curve. Look at the dashed line, which marks one gigabyte of complex numbers. The exact state crosses it at about $L=26$ and has reached sixteen gigabytes at $L=30$.](figures/web/session07/memory_scaling.svg){#sch:s07:memory_scaling alt="The logarithm of the number of coefficients against the number of sites, with a steep straight line for the exact state and two almost flat curves for matrix product states."}

::: quiz
We store the exact ground state of $L=40$ spin-1/2 sites as complex numbers of 16 bytes each. What memory do we need?

- [x] About 17 terabytes, since $2^{40}\approx 10^{12}$ coefficients are needed.

    This is true. The number of coefficients is $2^{40}\approx1.1\times10^{12}$ and each one takes 16 bytes. This is already far above the memory of a computer, and ten more sites would multiply it by one thousand.

- [ ] About 17 gigabytes, since $2^{40}$ is of the order of $10^9$.

    This is false. The value $2^{30}\approx10^9$ is the one for a chain of 30 sites, which does need $1.7\times10^{10}$ bytes. For $L=40$ the number is $2^{40}\approx10^{12}$, a thousand times more.

- [ ] About 640 bytes, since there are 40 sites.

    This is false. This would be the storage of a product state, one 16-byte number per site. Already for $L=2$ the singlet has two nonzero coefficients that cannot be written as a product of two single-site states.
:::

::: quiz
We add one more spin-1/2 site to the chain. How does the storage of the exact state [(7.4)](#eq-7-4) change?

- [ ] It grows by a fixed number of coefficients.

    This is false. Going from $L=2$ to $L=3$ adds 4 coefficients, from $L=3$ to $L=4$ adds 8, and from $L=10$ to $L=11$ adds 1024. The increase is not fixed.

- [ ] It is multiplied by $L$.

    This is false. From $L=2$ to $L=3$ the number of coefficients goes from 4 to 8, and this is a factor 2 and not 3. The factor is 2 for every $L$.

- [x] It doubles.

    This is true. Each new site doubles the dimension of the Hilbert space, so $2^L$ becomes $2^{L+1}$. This is the exponential wall, and the MPS ansatz replaces it with a growth that is linear in $L$.
:::

::: notebookbox
**Notebook check-in:** [`session7.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session7.ipynb), "Energy of the Heisenberg model as a function of the system size" (Core)

In this exercise you compute the ground-state energy per site of the Heisenberg chain with exact diagonalization, for growing system sizes. For this you use the `dmrgpy` library, which is new in this session, together with `pyqula`. You will see how fast exact diagonalization stops being possible, and this limit is the $2^L$ scaling of [(7.4)](#eq-7-4) in a concrete calculation.
:::

::: {.tryit notebook="session7.ipynb" cell="Energy of the Heisenberg model as a function of the system size"}
Increase the sizes in the list `Ns` and plot the energy per site. For $J=1$ it should approach the value $1/4-\ln 2\approx-0.443$ of the infinite chain. At which size does the calculation become slow, and how does this compare with the $2^L$ of [(7.4)](#eq-7-4)?
:::
