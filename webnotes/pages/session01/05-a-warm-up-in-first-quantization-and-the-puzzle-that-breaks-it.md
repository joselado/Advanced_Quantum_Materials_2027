## A warm-up in first quantization, and the puzzle that breaks it {#sec-1-5 number="1.5"}

Let us take the simplest single-particle system, which is a lattice of sites with one level each and one electron, that forms a finite island such as a quantum dot. Without many-body interactions this is an ordinary diagonalization problem, in the same way as a particle in a box, with a lowest energy state, a first excited state and so on. In this language, "one electron in the ground level" and "one electron in the first excited level" are two different single-particle states, and we can also take superpositions of the two. In every case, however, there is exactly one electron in the system.

Now let us say that we want to describe a quantum dot in a coherent superposition of zero electrons and two electrons, each with 50% probability. We cannot write this as an ordinary wave function. A wave function needs a fixed number of coordinates, and it makes no sense to have zero coordinates and two coordinates at the same time. This example is not artificial. Reasoning about a number of electrons that fluctuates is what allows us to understand how local magnetic moments couple to each other in real oxides. This is the basis of the Goodenough-Kanamori rules, which predict ferromagnetism or antiferromagnetism. It is also part of the definition of a superconductor, whose mean-field order parameter conserves only the *parity* of the electron number and not the number itself. This description of superconductors, which does not conserve the number of particles, has its own name, the Bogoliubov-de Gennes formalism. We use it in practice from Section [5.8](#sec-5-8) on.

## Building second quantization with creation and annihilation operators {#sec-1-6 number="1.6"}

To describe systems of this kind we introduce two operators at every site $i$. The first one is the annihilation operator $c_i$, which destroys an electron at site $i$, and the second one is the creation operator $c_i^\dagger$, which creates one. The Hamiltonian, and all the dynamics of the system, is written only in terms of these operators.

We define the vacuum state, which is the empty state $|0\rangle$, by

$$c_i|0\rangle = 0 \quad \text{for every site } i. \tag{1.1}$$

A hopping term between two sites, which describes an electron that can jump between sites 0 and 1, is then written as

$$H_\text{hop} = t\left(c_0^\dagger c_1 + c_1^\dagger c_0\right), \tag{1.2}$$

and we read it as "destroy an electron at 1 and create one at 0" plus the reverse process. If we start from the vacuum and apply creation operators, we obtain all the states of the two-site system. These are $|0\rangle$, then $c_0^\dagger|0\rangle$ with one electron at site 0, then $c_1^\dagger|0\rangle$ with one electron at site 1, and finally $c_0^\dagger c_1^\dagger|0\rangle$ with both sites occupied. [](#sch:s01:dimer_fock) lists these four states with their energies.

![The four states of the two-site problem sorted by electron number, with the energies of [(1.2)](#eq-1-2). One electron gives the levels $-t$ and $+t$, which are the antisymmetric and the symmetric combination of the two sites. With two electrons the hopping cannot move anything, and the energy is $(-t)+(+t)=0$.](figures/web/session01/dimer_fock.svg){#sch:s01:dimer_fock alt="Energy levels of the two-site problem grouped by the number of electrons, with the occupied sites drawn as discs."}

::: quiz
Both sites are occupied, and the state is $c_0^\dagger c_1^\dagger|0\rangle$. What is its energy for the hopping of [(1.2)](#eq-1-2)?

- [ ] $-t$

    This is false. The energy $-t$ belongs to one electron in the lower level. Here both levels, $-t$ and $+t$, are filled, and the sum is $0$.

- [x] $0$

    This is true. The hopping needs an empty site, and none is empty, so $H_\text{hop}$ gives zero on this state. The same follows from adding the two levels, $(-t)+(+t)=0$.

- [ ] $2t$

    This is false. It would need both electrons in the level $+t$. The Pauli principle forbids this, since $(c_+^\dagger)^2=0$, so the largest energy of two electrons here is still $0$.

Hopping an electron onto an occupied site gives zero, because $(c_0^\dagger)^2=0$.
:::

::: notebookbox
**Notebook check-in:** [`session1.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb), "The spectra of a dimer" (Core)

Build this two-site system and diagonalize it. Check that the Fock states above give the same spectrum that you would obtain from an ordinary two-level treatment in first quantization, before we add any interactions.
:::

::: {.tryit notebook="session1.ipynb" cell="The spectra of a dimer"}
Run the cell and count the eigenvalues of the dimer with spin. Set `has_spin=False` and check that two remain, at $-t$ and $+t$. These are the levels of the column with one electron in the figure above.
:::

## Enforcing fermionic statistics {#sec-1-7 number="1.7"}

Up to now nothing distinguishes fermions from bosons, and everything above applies to both in the same way. The difference is introduced through the algebra of the operators. Fermi statistics requires that the many-body wave function changes sign when we exchange two particles, and a direct consequence is that a given single-particle level can have zero fermions or one fermion, but never two. We impose this with anticommutation relations,

$$\{c_i, c_j^\dagger\} = \delta_{ij}, \qquad \{c_i, c_j\} = \{c_i^\dagger, c_j^\dagger\} = 0. \tag{1.3}$$

The second relation is the important one. If we take $i=j$ it gives $(c_i^\dagger)^2 = 0$, which means that we cannot create two electrons in the same level. At the same time it imposes the antisymmetry of the wave function, so the Pauli exclusion principle is part of the algebra itself and we do not need to add it by hand.

![Two particles on the two sites of [(1.2)](#eq-1-2), from exact diagonalization in the Fock space. For fermions $(c_i^\dagger)^2=0$, so the only state has one particle on each site, and its energy is $0$. Bosons commute, so two of them can also share a site. This gives three states, with the energies $-2t$, $0$ and $+2t$. The Hamiltonian is the same in both cases, and only the algebra of the operators is different.](figures/web/session01/boson_fermion_pair.svg){#sch:s01:boson_fermion_pair alt="Two level diagrams. Two fermions have one level at zero. Two bosons have three levels at minus 2t, zero and plus 2t. Below each diagram are the ways to put two particles on two sites, one way for fermions and three for bosons."}

::: quiz
Suppose $c_i^\dagger$ and $c_j^\dagger$ commuted instead of anticommuting. What would change?

- [x] The operator $(c_i^\dagger)^2$ would not vanish, so two particles could sit in the same level.

    This is true. The statement $(c_i^\dagger)^2=0$ follows only from the anticommutation relation. Without it, nothing stops a second particle from entering the same level, and we describe bosons.

- [ ] The vacuum would not be annihilated by $c_i$.

    This is false. For bosons the vacuum still satisfies $b_i|0\rangle=0$, since there is no particle to remove. The vacuum condition does not depend on the statistics.

- [ ] The hopping term would not be Hermitian.

    This is false. The term $t(b_0^\dagger b_1+b_1^\dagger b_0)$ of bosons is Hermitian, because it is written with its own Hermitian conjugate. Its levels are $\pm t$ in the one-particle sector, as for fermions.

Bosons and fermions differ in the algebra of the operators, and not in the vacuum or in the Hermiticity.
:::

::: comesback
- Section [5.6](#sec-5-6) comes back to the dot in a superposition of zero and two electrons, now for the pairing Hamiltonian of a superconductor.
- Virtual hops that change the number of electrons on a site give the superexchange of Section [6.8](#sec-6-8) and the Goodenough-Kanamori rules of Section [6.11](#sec-6-11).
- The anticommutation relations [(1.3)](#eq-1-3) come back in Section [7.2b](#sec-7-2b), where the Jordan-Wigner transformation needs a string to build fermions from spins.
:::
