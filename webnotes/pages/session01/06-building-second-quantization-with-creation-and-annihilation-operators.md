## Building second quantization with creation and annihilation operators {#sec-1-6 number="1.6"}

To describe systems of this kind we introduce two operators at every site $i$. The first one is the annihilation operator $c_i$, which destroys an electron at site $i$, and the second one is the creation operator $c_i^\dagger$, which creates one. The Hamiltonian, and all the dynamics of the system, is written only in terms of these operators.

We define the vacuum state, which is the empty state $|0\rangle$, by

$$c_i|0\rangle = 0 \quad \text{for every site } i. \tag{1.1}$$

A hopping term between two sites, which describes an electron that can jump between sites 0 and 1, is then written as

$$H_\text{hop} = t\left(c_0^\dagger c_1 + c_1^\dagger c_0\right), \tag{1.2}$$

and we read it as "destroy an electron at 1 and create one at 0" plus the reverse process. If we start from the vacuum and apply creation operators, we obtain all the states of the two-site system. These are $|0\rangle$, then $c_0^\dagger|0\rangle$ with one electron at site 0, then $c_1^\dagger|0\rangle$ with one electron at site 1, and finally $c_0^\dagger c_1^\dagger|0\rangle$ with both sites occupied.

::: notebookbox
**Notebook check-in:** [`session1.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb), "The spectra of a dimer" (Core)

Build this two-site system and diagonalize it. Check that the Fock states above give the same spectrum that you would obtain from an ordinary two-level treatment in first quantization, before we add any interactions.
:::
